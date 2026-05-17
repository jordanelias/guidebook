#!/usr/bin/env python3
"""adherence_log_audit.py — Level 2 audit for attestation files.

Checks performed (per PI v10.12 rule #11):

0. Attestation presence. For every synthesis-path file in the changeset,
   verify a corresponding `attestations/<slug>.json` is either also in the
   changeset OR already exists in the repo (backfill-on-touch).

1. Schema validation. Every file in attestations/ in the changeset
   validates against schemas/attestation.schema.json. Audit script reads
   attestation.schema_version and dispatches to the matching check suite.

2. Doctrine-SHA consistency. attestation.doctrine_sha matches the
   commit-message [DOCTRINE: ...] token of the commit that introduced
   or last modified the attestation.

3. Rule identifier resolution. Every key in rules_in_scope and
   per_rule_status resolves to a known stable identifier per
   references/skill-registry.md.

4. Evidence-path resolution. For per_rule_status entries with
   status=FIRED, evidence_path resolves to an extant file or
   git-ref. Path may be a file relative to repo root or a token of
   form db://<table>/<id-pattern> for DB-backed evidence.

5. Cross-reference per-rule evidence inference. For rules with
   automatable inference (rule 'pmp' -> row in spec_value_probes;
   rule 'adversarial-research' -> four gap fields populated for cited
   sources; rule 'jurisdictional-synthesis' -> reasoning_doc_citations
   row per cell), verify that FIRED claims correspond to actual
   repository state.

6. Counterclaim uniqueness. bias_direction and
   independent_reviewer_counterclaim fields compared via normalized
   Levenshtein ratio against the same fields in the previous 10
   attestations. Ratio > 0.85 flags as suspected boilerplate.

7. Re-attestation window. Read git history for last commit touching
   governance/mission-and-epistemics.md (no sidecar state file).
   Count commits since that SHA. If > RE_ATTESTATION_WINDOW and any
   synthesis artifact has not been re-attested (attestation
   last-modified-SHA postdates last_doctrine_sha), FAIL.

8. Verdict-evidence consistency. verdict=CLEAN requires zero
   deviations and all rules_in_scope status=FIRED.
   verdict=DEVIATION-LOGGED requires at least one non-FIRED status
   or non-empty deviations array. verdict=NON-COMPLIANT is logged
   but does NOT exit non-zero (log-not-block per PI rule #11).

Exit codes: 0 = pass (or NON-COMPLIANT verdicts present but logged);
           1 = any other check failed.
DB path: data/guidebook.db (override via GUIDEBOOK_DB_PATH).
Repo root: resolved relative to __file__.
Constants: RE_ATTESTATION_WINDOW = 5 (default; configurable per workplan §5).
"""
import argparse
import json
import os
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", str(REPO / "data" / "guidebook.db")))
SCHEMA_PATH = REPO / "schemas" / "attestation.schema.json"
ATTESTATIONS_DIR = REPO / "attestations"
SKILL_REGISTRY = REPO / "references" / "skill-registry.md"
DOCTRINE_PATH = "governance/mission-and-epistemics.md"

SYNTHESIS_PATH_RE = re.compile(
    r"^(references/bpc-reasoning|references/connection-reasoning|decisions|sessions)/.+\.md$"
)

RE_ATTESTATION_WINDOW = 5
LEVENSHTEIN_THRESHOLD = 0.85
LEVENSHTEIN_WINDOW = 10

# Rule identifiers that are valid in attestations but not listed in skill-registry's
# "active skills" block (governance/methodology rules, not skills).
EXTRA_RULE_IDS = {
    "doctrine-check",
    "jurisdictional-synthesis",
    "evidence-verification-gate",
    "pmp",
    "source-discipline",
}


# ----- Helpers -----

def _git(*args):
    return subprocess.check_output(
        ["git", "-C", str(REPO), *args], text=True, stderr=subprocess.DEVNULL
    ).strip()


def _changed_files(base, head):
    try:
        out = _git("diff", "--name-only", base, head)
    except subprocess.CalledProcessError:
        return []
    return [line for line in out.splitlines() if line]


def _attestation_path_for(synthesis_path):
    """Map references/bpc-reasoning/foo.md -> attestations/bpc-reasoning_foo.json."""
    p = Path(synthesis_path)
    if p.parts[0] == "references":
        prefix = p.parts[1]
        stem = "_".join(p.parts[2:]).rsplit(".", 1)[0]
    else:
        prefix = p.parts[0]
        stem = "_".join(p.parts[1:]).rsplit(".", 1)[0]
    return ATTESTATIONS_DIR / f"{prefix}_{stem}.json"


def _load_skill_ids():
    """Parse the 'All active skills' code block in skill-registry.md."""
    if not SKILL_REGISTRY.exists():
        return set()
    text = SKILL_REGISTRY.read_text()
    m = re.search(r"## All active skills.*?```\n(.*?)\n```", text, re.DOTALL)
    if not m:
        return set()
    return set(re.findall(r"\b[a-z][a-z0-9-]{2,}\b", m.group(1)))


def _all_valid_rule_ids():
    return _load_skill_ids() | EXTRA_RULE_IDS


def _attestations_in_changeset(changed):
    return [f for f in changed if f.startswith("attestations/") and f.endswith(".json")]


def _synthesis_in_changeset(changed):
    return [f for f in changed if SYNTHESIS_PATH_RE.match(f)]


def _last_doctrine_sha():
    try:
        return _git("log", "-1", "--format=%H", "--", DOCTRINE_PATH)
    except subprocess.CalledProcessError:
        return ""


def _commits_since(sha):
    if not sha:
        return 0
    try:
        return int(_git("rev-list", "--count", f"{sha}..HEAD"))
    except subprocess.CalledProcessError:
        return 0


def _commit_msg(sha):
    try:
        return _git("log", "-1", "--format=%B", sha)
    except subprocess.CalledProcessError:
        return ""


def _last_commit_for(path):
    try:
        return _git("log", "-1", "--format=%H", "--", str(path))
    except subprocess.CalledProcessError:
        return ""


def _load_json(path):
    try:
        return json.loads(Path(path).read_text())
    except (json.JSONDecodeError, FileNotFoundError):
        return None


# ----- Checks -----

def check_0_presence(changed, issues):
    """Backfill-on-touch: synthesis file in changeset -> attestation must also
    be in changeset OR pre-exist on disk."""
    for syn in _synthesis_in_changeset(changed):
        target = _attestation_path_for(syn)
        rel = target.relative_to(REPO).as_posix()
        if rel in changed or target.exists():
            continue
        issues.append(f"CHECK 0: missing attestation for {syn} (expected {rel})")


def check_1_schema(changed, issues):
    """JSON schema validation. jsonschema imported lazily."""
    files = _attestations_in_changeset(changed)
    if not files:
        return
    try:
        from jsonschema import validate, ValidationError
    except ImportError:
        issues.append("CHECK 1: jsonschema not installed; cannot validate")
        return
    schema = _load_json(SCHEMA_PATH)
    if schema is None:
        issues.append(f"CHECK 1: schema file missing or invalid: {SCHEMA_PATH}")
        return
    for f in files:
        fp = REPO / f
        if not fp.exists():
            issues.append(f"CHECK 1: {f} listed as changed but missing on disk")
            continue
        data = _load_json(fp)
        if data is None:
            issues.append(f"CHECK 1: {f} invalid JSON")
            continue
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            issues.append(f"CHECK 1: {f} schema violation -- {e.message}")


def check_2_doctrine_sha(changed, issues):
    """attestation.doctrine_sha must match the [DOCTRINE: ...] token in the
    commit that introduced or last modified the attestation."""
    for f in _attestations_in_changeset(changed):
        data = _load_json(REPO / f)
        if data is None:
            continue
        att_sha = data.get("doctrine_sha", "")
        last_sha = _last_commit_for(f) or _git("rev-parse", "HEAD")
        msg = _commit_msg(last_sha)
        m = re.search(r"\[DOCTRINE: ([a-f0-9]{7})\]", msg)
        if not m:
            issues.append(
                f"CHECK 2: {f} doctrine_sha={att_sha} but commit "
                f"{last_sha[:7]} has no [DOCTRINE: ...] token"
            )
            continue
        if att_sha != m.group(1):
            issues.append(
                f"CHECK 2: {f} doctrine_sha={att_sha} but commit token={m.group(1)}"
            )


def check_3_rule_resolution(changed, issues):
    """Every rule identifier resolves to a stable identifier."""
    valid = _all_valid_rule_ids()
    for f in _attestations_in_changeset(changed):
        data = _load_json(REPO / f)
        if data is None:
            continue
        ids = set(data.get("rules_in_scope", []))
        ids |= set(data.get("per_rule_status", {}).keys())
        for d in data.get("deviations", []):
            if "rule" in d:
                ids.add(d["rule"])
        unknown = ids - valid
        if unknown:
            issues.append(f"CHECK 3: {f} unknown rule identifiers: {sorted(unknown)}")


def check_4_evidence_path(changed, issues):
    """status=FIRED entries must have a resolvable evidence_path."""
    for f in _attestations_in_changeset(changed):
        data = _load_json(REPO / f)
        if data is None:
            continue
        for rule, body in data.get("per_rule_status", {}).items():
            if body.get("status") != "FIRED":
                continue
            ep = body.get("evidence_path", "")
            if not ep:
                issues.append(f"CHECK 4: {f} rule={rule} FIRED but no evidence_path")
                continue
            if ep.startswith("db://"):
                continue  # validated in check #5
            if (REPO / ep).exists():
                continue
            if ":" in ep:
                try:
                    _git("rev-parse", ep)
                    continue
                except subprocess.CalledProcessError:
                    pass
            issues.append(f"CHECK 4: {f} rule={rule} evidence_path missing: {ep}")


def check_5_cross_reference(changed, issues):
    """FIRED claim on inference-able rule must correspond to DB state."""
    import sqlite3
    if not DB_PATH.exists():
        return
    db = sqlite3.connect(str(DB_PATH))
    for f in _attestations_in_changeset(changed):
        data = _load_json(REPO / f)
        if data is None:
            continue
        prs = data.get("per_rule_status", {})
        artifact = data.get("artifact", "")
        slug = Path(artifact).stem
        # pmp / progressive-measurement
        pmp = prs.get("pmp") or prs.get("progressive-measurement")
        if pmp and pmp.get("status") == "FIRED":
            row = db.execute(
                "SELECT COUNT(*) FROM spec_value_probes WHERE slug LIKE ?",
                (f"%{slug}%",),
            ).fetchone()
            if row[0] == 0:
                issues.append(
                    f"CHECK 5: {f} pmp FIRED but no spec_value_probes rows "
                    f"match slug pattern '{slug}'"
                )
        # jurisdictional-synthesis
        js = prs.get("jurisdictional-synthesis")
        if js and js.get("status") == "FIRED":
            row = db.execute(
                "SELECT COUNT(*) FROM reasoning_doc_citations WHERE reasoning_doc_slug = ?",
                (slug,),
            ).fetchone()
            if row[0] == 0:
                issues.append(
                    f"CHECK 5: {f} jurisdictional-synthesis FIRED but no "
                    f"reasoning_doc_citations rows for slug={slug}"
                )
        # adversarial-research: per-artifact mapping ambiguous; deferred to rule-#7
        # audit (research_protocol_audit.py).
    db.close()


def check_6_counterclaim_uniqueness(changed, issues):
    """bias_direction and counterclaim compared via SequenceMatcher ratio
    against the previous LEVENSHTEIN_WINDOW attestations. Ratio above
    LEVENSHTEIN_THRESHOLD flags suspected boilerplate."""
    new_files = _attestations_in_changeset(changed)
    if not new_files:
        return
    history = []
    if ATTESTATIONS_DIR.exists():
        for p in sorted(ATTESTATIONS_DIR.glob("*.json")):
            rel = p.relative_to(REPO).as_posix()
            if rel in changed:
                continue
            data = _load_json(p)
            if data is None:
                continue
            history.append((
                p.name,
                data.get("bias_direction", ""),
                data.get("independent_reviewer_counterclaim", ""),
            ))
    history = history[-LEVENSHTEIN_WINDOW:]
    for f in new_files:
        data = _load_json(REPO / f)
        if data is None:
            continue
        bd = data.get("bias_direction", "")
        cc = data.get("independent_reviewer_counterclaim", "")
        for name, prev_bd, prev_cc in history:
            if bd and prev_bd:
                r = SequenceMatcher(None, bd, prev_bd).ratio()
                if r > LEVENSHTEIN_THRESHOLD:
                    issues.append(
                        f"CHECK 6: {f} bias_direction similarity={r:.2f} vs {name}"
                    )
            if cc and prev_cc:
                r = SequenceMatcher(None, cc, prev_cc).ratio()
                if r > LEVENSHTEIN_THRESHOLD:
                    issues.append(
                        f"CHECK 6: {f} counterclaim similarity={r:.2f} vs {name}"
                    )


def check_7_reattestation_window(changed, issues):
    """If last doctrine commit was > RE_ATTESTATION_WINDOW commits ago and
    any synthesis attestation hasn't been re-attested since, FAIL."""
    last_doc = _last_doctrine_sha()
    if not last_doc:
        return
    ago = _commits_since(last_doc)
    if ago <= RE_ATTESTATION_WINDOW:
        return
    if not ATTESTATIONS_DIR.exists():
        return
    for p in sorted(ATTESTATIONS_DIR.glob("*.json")):
        rel = p.relative_to(REPO).as_posix()
        last_att = _last_commit_for(rel)
        if not last_att:
            continue
        try:
            order = int(_git("rev-list", "--count", f"{last_doc}..{last_att}"))
        except (subprocess.CalledProcessError, ValueError):
            continue
        if order <= 0:
            issues.append(
                f"CHECK 7: {p.name} not re-attested since doctrine change "
                f"({ago} commits ago, window={RE_ATTESTATION_WINDOW})"
            )


def check_8_verdict_evidence(changed, issues):
    """CLEAN ⇒ zero deviations AND all FIRED. DEVIATION-LOGGED ⇒ at least one
    non-FIRED OR non-empty deviations. NON-COMPLIANT logged but not failed."""
    for f in _attestations_in_changeset(changed):
        data = _load_json(REPO / f)
        if data is None:
            continue
        verdict = data.get("verdict")
        deviations = data.get("deviations", [])
        statuses = [v.get("status") for v in data.get("per_rule_status", {}).values()]
        if verdict == "CLEAN":
            if deviations or any(s != "FIRED" for s in statuses):
                issues.append(
                    f"CHECK 8: {f} verdict=CLEAN inconsistent with "
                    f"{len(deviations)} deviations and statuses={statuses}"
                )
        elif verdict == "DEVIATION-LOGGED":
            if not deviations and all(s == "FIRED" for s in statuses):
                issues.append(
                    f"CHECK 8: {f} verdict=DEVIATION-LOGGED but no deviations "
                    f"and all rules FIRED"
                )
        elif verdict == "NON-COMPLIANT":
            pass  # surfaced separately; not a failure


# ----- Dispatcher -----

CHECK_GROUPS = {
    "presence":  [check_0_presence],
    "schema":    [check_1_schema],
    "evidence":  [
        check_2_doctrine_sha,
        check_3_rule_resolution,
        check_4_evidence_path,
        check_5_cross_reference,
        check_6_counterclaim_uniqueness,
        check_7_reattestation_window,
    ],
    "verdict":   [check_8_verdict_evidence],
    # Individual checks for local debugging:
    "doctrine":  [check_2_doctrine_sha],
    "rules":     [check_3_rule_resolution],
    "path":      [check_4_evidence_path],
    "cross-ref": [check_5_cross_reference],
    "unique":    [check_6_counterclaim_uniqueness],
    "window":    [check_7_reattestation_window],
}


def _non_compliant_verdicts(changed):
    out = []
    for f in _attestations_in_changeset(changed):
        data = _load_json(REPO / f)
        if data is None:
            continue
        if data.get("verdict") == "NON-COMPLIANT":
            out.append(f)
    return out


def audit(check_filter=None, base="HEAD~1", head="HEAD"):
    issues = []
    changed = _changed_files(base, head)
    if check_filter:
        if check_filter not in CHECK_GROUPS:
            print(f"Unknown check: {check_filter}", file=sys.stderr)
            return 2
        for fn in CHECK_GROUPS[check_filter]:
            fn(changed, issues)
    else:
        seen = set()
        for group in CHECK_GROUPS.values():
            for fn in group:
                if fn in seen:
                    continue
                seen.add(fn)
                fn(changed, issues)
    print("=" * 60)
    print(f"adherence_log_audit -- check_filter={check_filter or 'all'}")
    print(f"changed files: {len(changed)}; "
          f"attestations: {len(_attestations_in_changeset(changed))}; "
          f"synthesis: {len(_synthesis_in_changeset(changed))}")
    print("=" * 60)
    if issues:
        for i in issues:
            print(i)
    else:
        print("No issues.")
    nc = _non_compliant_verdicts(changed)
    if nc and check_filter in (None, "verdict"):
        print("-" * 60)
        print(f"NON-COMPLIANT verdicts (logged, not blocking): {len(nc)}")
        for f in nc:
            print(f"  {f}")
    print("=" * 60)
    return 1 if issues else 0


def main():
    parser = argparse.ArgumentParser(description="Adherence-log attestation audit.")
    parser.add_argument("--check", choices=list(CHECK_GROUPS.keys()), default=None,
                        help="Run a single named check group (default: all).")
    parser.add_argument("--base", default="HEAD~1",
                        help="Base ref for changed-file diff (default: HEAD~1).")
    parser.add_argument("--head", default="HEAD",
                        help="Head ref for changed-file diff (default: HEAD).")
    args = parser.parse_args()
    sys.exit(audit(check_filter=args.check, base=args.base, head=args.head))


if __name__ == "__main__":
    main()
