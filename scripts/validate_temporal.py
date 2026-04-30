#!/usr/bin/env python3
"""
scripts/validate_temporal.py — Validate temporal entities and supersedence chains.

Per governance/time-model.md (A9):
- All temporal date strings format-compliant
- No future dates (24h skew tolerance)
- Supersedence chains acyclic; targets resolve
- Guidebook version filenames match pattern; exactly one ACTIVE
- LaunchPhaseRecord exists as singleton
- Source publication-year / iso-date consistency
- Tier 1–3 sources without last_verified flagged
- Freshness windows on EvidenceSource records
- ProjectRule pre-session normalisation correctness
- Transition-period citation flag (best-effort prose scan)

Usage:
    python3 scripts/validate_temporal.py                # full scan
    python3 scripts/validate_temporal.py --rules        # ProjectRule extraction only
    python3 scripts/validate_temporal.py --supersedence # supersedence chains only
    python3 scripts/validate_temporal.py --versions     # guidebook versions only
    python3 scripts/validate_temporal.py --report       # summary; exit 0 always

Exit codes: 0 = pass, 1 = errors, 2 = config error.
"""

import argparse
import datetime as dt
import glob
import os
import re
import sys
from collections import defaultdict

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.temporal import (
    DATETIME_PATTERN,
    DATE_ONLY_PATTERN,
    PRE_SESSION_LITERAL,
    PRE_SESSION_NORMALISED,
    VERSION_FILENAME_PATTERN,
    FRESHNESS_WINDOWS,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRACE_HOURS = 24


# --- T-01: Date string format ---

def _format_ok(s: str, *, allow_date_only: bool = False, allow_pre_session: bool = False) -> bool:
    if allow_pre_session and s == PRE_SESSION_LITERAL:
        return True
    if DATETIME_PATTERN.match(s):
        return True
    if allow_date_only and DATE_ONLY_PATTERN.match(s):
        return True
    return False


def t01_date_format(records: list[tuple[str, dict]]) -> tuple[list, list]:
    """T-01: every date field across all temporal records is format-compliant."""
    errors: list[str] = []
    warnings: list[str] = []
    DATE_FIELDS = {
        "effective_date": True,
        "effective_date_normalized": False,
        "since": False,
        "last_checked": False,
        "last_verified": False,
        "transition_until_date": True,
        "publication_date": True,
    }
    for path, rec in records:
        for field, allow_date_only in DATE_FIELDS.items():
            v = rec.get(field)
            if v is None:
                continue
            if not isinstance(v, str):
                errors.append(f"T-01 {path}: {field} not a string: {v!r}")
                continue
            allow_pre = field == "effective_date"
            if not _format_ok(v, allow_date_only=allow_date_only, allow_pre_session=allow_pre):
                errors.append(
                    f"T-01 {path}: {field}='{v}' not in expected format "
                    f"(YYYY-MM-DD HH:MM"
                    f"{' or YYYY-MM-DD' if allow_date_only else ''}"
                    f"{' or pre-session' if allow_pre else ''})"
                )
    return errors, warnings


# --- T-02: No future dates ---

def t02_no_future(records: list[tuple[str, dict]]) -> tuple[list, list]:
    """T-02: effective dates and last_verified must not exceed now+grace."""
    errors: list[str] = []
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    cutoff = now + dt.timedelta(hours=GRACE_HOURS)
    DATE_FIELDS_TO_CHECK = ("effective_date", "since", "last_checked", "last_verified")
    for path, rec in records:
        for field in DATE_FIELDS_TO_CHECK:
            v = rec.get(field)
            if not v or not isinstance(v, str):
                continue
            if v == PRE_SESSION_LITERAL:
                continue
            try:
                if DATETIME_PATTERN.match(v):
                    parsed = dt.datetime.strptime(v, "%Y-%m-%d %H:%M")
                elif DATE_ONLY_PATTERN.match(v):
                    parsed = dt.datetime.strptime(v, "%Y-%m-%d")
                else:
                    continue  # T-01 will catch
            except ValueError:
                continue  # T-01 will catch
            if parsed > cutoff:
                errors.append(
                    f"T-02 {path}: {field}='{v}' is in the future "
                    f"(now={now.strftime('%Y-%m-%d %H:%M')} UTC)"
                )
    return errors, []


# --- T-03 / T-04: Supersedence chains ---

def t03_t04_supersedence(records_by_kind: dict[str, list]) -> tuple[list, list]:
    """T-03 cycles + T-04 orphans across all SupersedenceLink records.

    Each link_type forms its own directed graph: from_id → to_id.
    Cycles within a type are errors. Targets that don't resolve to a known
    entity ID of that type are orphans.
    """
    errors: list[str] = []
    warnings: list[str] = []

    links = records_by_kind.get("supersedence", [])
    rules_known = {r["rule_id"] for r in records_by_kind.get("rules", []) if "rule_id" in r}
    versions_known = {r["version_tag"] for r in records_by_kind.get("guidebook_versions", []) if "version_tag" in r}
    standards_known = {r["edition"] for r in records_by_kind.get("standards", []) if "edition" in r}

    # Build per-type graph
    graph: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for link in links:
        lt = link.get("link_type")
        from_id = link.get("from_id")
        to_id = link.get("to_id")
        if not (lt and from_id and to_id):
            continue
        graph[lt][from_id].append(to_id)

    # T-04 orphan check (only ACTIVE links — PROVISIONAL is by-design incomplete)
    KNOWN = {
        "rule": rules_known,
        "version": versions_known,
        "standard": standards_known,
    }
    for link in links:
        if link.get("status") != "ACTIVE":
            continue
        lt = link.get("link_type")
        if lt in KNOWN and KNOWN[lt]:
            link_id = link.get("link_id", "?")
            from_id = link.get("from_id")
            to_id = link.get("to_id")
            # Standards orphan check is loose because edition strings vary in the registry
            severity = "warning" if lt == "standard" else "error"
            if from_id not in KNOWN[lt]:
                msg = f"T-04 {link_id}: from_id='{from_id}' not found in known {lt} records"
                (warnings if severity == "warning" else errors).append(msg)
            if to_id not in KNOWN[lt]:
                msg = f"T-04 {link_id}: to_id='{to_id}' not found in known {lt} records"
                (warnings if severity == "warning" else errors).append(msg)

    # T-03 cycle check (Tarjan/DFS)
    for lt, adj in graph.items():
        WHITE, GRAY, BLACK = 0, 1, 2
        color: dict[str, int] = defaultdict(lambda: WHITE)
        cycles: list[list[str]] = []

        def dfs(node: str, path: list[str]) -> None:
            if color[node] == GRAY:
                cycle_start = path.index(node) if node in path else 0
                cycles.append(path[cycle_start:] + [node])
                return
            if color[node] == BLACK:
                return
            color[node] = GRAY
            path.append(node)
            for nxt in adj.get(node, []):
                dfs(nxt, path)
            path.pop()
            color[node] = BLACK

        for n in list(adj.keys()):
            dfs(n, [])

        for c in cycles:
            errors.append(f"T-03 {lt}: cycle detected: {' → '.join(c)}")

    return errors, warnings


# --- T-05: Version filename pattern ---

def t05_version_filenames() -> tuple[list, list]:
    """T-05: every file under versions/**/*.md matches the pattern."""
    errors: list[str] = []
    warnings: list[str] = []
    versions_dir = os.path.join(REPO_ROOT, "versions")
    if not os.path.isdir(versions_dir):
        return [], []
    for path in sorted(glob.glob(os.path.join(versions_dir, "**", "*.md"), recursive=True)):
        name = os.path.basename(path)
        if not VERSION_FILENAME_PATTERN.match(name):
            errors.append(
                f"T-05 versions/.../{name}: filename does not match "
                f"Guidebook_for_Accessible_Design_v{{tag}}_{{YYYY-MM-DD}}.md "
                f"(or -prep.md)"
            )
    return errors, warnings


# --- T-06: Exactly one ACTIVE GuidebookVersion ---

def t06_one_active(versions: list[dict]) -> tuple[list, list]:
    """T-06: exactly one record has status=ACTIVE."""
    errors: list[str] = []
    actives = [v for v in versions if v.get("status") == "ACTIVE"]
    if not versions:
        return [], []  # empty corpus is fine
    if len(actives) != 1:
        errors.append(
            f"T-06: expected exactly 1 ACTIVE GuidebookVersion, found {len(actives)}: "
            f"{[v.get('version_tag') for v in actives]}"
        )
    return errors, []


# --- T-07: Year vs publication_date_iso consistency on EvidenceSource ---

def t07_source_year_consistency() -> tuple[list, list]:
    """T-07: EvidenceSource.year (string) consistent with publication_date_iso."""
    warnings: list[str] = []
    sources_dir = os.path.join(REPO_ROOT, "data", "sources")
    if not os.path.isdir(sources_dir):
        return [], []
    for path in sorted(glob.glob(os.path.join(sources_dir, "*.yaml"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        year = data.get("year")
        iso = data.get("publication_date_iso")
        if year and iso:
            iso_year = iso[:4]
            if str(year).strip() != iso_year:
                warnings.append(
                    f"T-07 {os.path.basename(path)}: year='{year}' vs "
                    f"publication_date_iso='{iso}' (year mismatch)"
                )
    return [], warnings


# --- T-08: Tier 1–3 sources without last_verified ---

def t08_last_verified_coverage() -> tuple[list, list]:
    """T-08: Tier 1–3 EvidenceSource records without last_verified are flagged."""
    warnings: list[str] = []
    sources_dir = os.path.join(REPO_ROOT, "data", "sources")
    if not os.path.isdir(sources_dir):
        return [], []
    flagged = 0
    for path in sorted(glob.glob(os.path.join(sources_dir, "*.yaml"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        tier = data.get("tier")
        if tier in (1, 2, 3) and not data.get("last_verified"):
            flagged += 1
    if flagged:
        warnings.append(
            f"T-08: {flagged} Tier 1–3 EvidenceSource records lack last_verified "
            f"(populate incrementally; not blocking)"
        )
    return [], warnings


# --- T-09: Exactly one LaunchPhaseRecord ---

def t09_launch_phase() -> tuple[list, list]:
    """T-09: data/temporal/launch_phase.yaml exists as a singleton."""
    errors: list[str] = []
    path = os.path.join(REPO_ROOT, "data", "temporal", "launch_phase.yaml")
    if not os.path.isdir(os.path.dirname(path)):
        return [], []  # data/temporal not yet built
    if not os.path.exists(path):
        errors.append("T-09: data/temporal/launch_phase.yaml missing (singleton required)")
    return errors, []


# --- T-10: Transition-period citation flag (best-effort) ---

def t10_transition_citations(supersedence: list[dict]) -> tuple[list, list]:
    """T-10: warn when prose cites a SUPERSEDED standard outside the registry.

    Best-effort: scan all .md files outside references/standards-registry.md
    for occurrences of any from_id that has a transition_until_date set.
    Warn once per (file, edition) pair.
    """
    warnings: list[str] = []
    transitions = [
        (l["from_id"], l.get("transition_until_date"))
        for l in supersedence
        if l.get("transition_until_date") and l.get("link_type") == "standard"
    ]
    if not transitions:
        return [], []

    # Walk markdown files
    skip_paths = {
        "references/standards-registry.md",
        "governance/time-model.md",
    }
    seen: set[tuple[str, str]] = set()
    for root, _, files in os.walk(REPO_ROOT):
        if "/.git" in root or "/node_modules" in root or "/data/" in root:
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, REPO_ROOT)
            if rel in skip_paths:
                continue
            try:
                with open(full, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue
            for from_id, until in transitions:
                if from_id in content and (rel, from_id) not in seen:
                    warnings.append(
                        f"T-10 {rel}: cites superseded edition '{from_id}' "
                        f"(transition until {until}); verify acknowledgment"
                    )
                    seen.add((rel, from_id))
    return [], warnings


# --- T-11: Freshness window exceeded ---

def t11_freshness_windows() -> tuple[list, list]:
    """T-11: EvidenceSource records older than the freshness window for their tier+type."""
    warnings: list[str] = []
    sources_dir = os.path.join(REPO_ROOT, "data", "sources")
    if not os.path.isdir(sources_dir):
        return [], []
    now_year = dt.datetime.now(dt.timezone.utc).year
    flagged = 0
    for path in sorted(glob.glob(os.path.join(sources_dir, "*.yaml"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        tier = data.get("tier")
        et = data.get("evidence_type")
        if tier is None or et is None:
            continue
        window = FRESHNESS_WINDOWS.get((tier, et))
        if window is None:
            continue  # edition-driven; no clock window
        # Reference year: last_verified > publication_date_iso > year
        ref_year = None
        if data.get("last_verified"):
            ref_year = int(data["last_verified"][:4])
        elif data.get("publication_date_iso"):
            ref_year = int(data["publication_date_iso"][:4])
        elif data.get("year"):
            try:
                ref_year = int(str(data["year"])[:4])
            except (ValueError, TypeError):
                continue
        if ref_year is None:
            continue
        age = now_year - ref_year
        if age > window:
            flagged += 1
    if flagged:
        warnings.append(
            f"T-11: {flagged} EvidenceSource records exceed their freshness window; "
            f"re-verification suggested"
        )
    return [], warnings


# --- T-12: Pre-session normalisation correctness ---

def t12_pre_session_norm(rules: list[dict]) -> tuple[list, list]:
    """T-12: pre-session rules normalise to the canonical anchor."""
    errors: list[str] = []
    for r in rules:
        ed = r.get("effective_date")
        edn = r.get("effective_date_normalized")
        if ed == PRE_SESSION_LITERAL and edn != PRE_SESSION_NORMALISED:
            errors.append(
                f"T-12 {r.get('rule_id', '?')}: pre-session must normalise to "
                f"'{PRE_SESSION_NORMALISED}', got '{edn}'"
            )
    return errors, []


# --- Loading ---

def _load_yaml_dir(subdir: str) -> list[tuple[str, dict]]:
    """Load all YAML files from data/temporal/{subdir}/. Returns (path, dict) tuples."""
    out: list[tuple[str, dict]] = []
    full = os.path.join(REPO_ROOT, "data", "temporal", subdir)
    if not os.path.isdir(full):
        return []
    for path in sorted(glob.glob(os.path.join(full, "*.yaml"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"WARN: could not parse {path}: {e}", file=sys.stderr)
            continue
        if isinstance(data, dict):
            out.append((os.path.relpath(path, REPO_ROOT), data))
    return out


def load_all_records() -> dict:
    """Load every temporal record kind into a structured dict."""
    return {
        "rules": [r for _, r in _load_yaml_dir("rules")],
        "rules_with_paths": _load_yaml_dir("rules"),
        "standards": [r for _, r in _load_yaml_dir("standards")],
        "standards_with_paths": _load_yaml_dir("standards"),
        "guidebook_versions": [r for _, r in _load_yaml_dir("guidebook_versions")],
        "guidebook_versions_with_paths": _load_yaml_dir("guidebook_versions"),
        "supersedence": [r for _, r in _load_yaml_dir("supersedence")],
        "supersedence_with_paths": _load_yaml_dir("supersedence"),
    }


def all_records_flat(records: dict) -> list[tuple[str, dict]]:
    """Flatten records for cross-cutting checks (T-01, T-02)."""
    out: list[tuple[str, dict]] = []
    for kind in ("rules", "standards", "guidebook_versions", "supersedence"):
        out.extend(records.get(f"{kind}_with_paths", []))
    return out


# --- Main ---

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--rules", action="store_true", help="ProjectRule checks only")
    ap.add_argument("--supersedence", action="store_true", help="Supersedence checks only")
    ap.add_argument("--versions", action="store_true", help="GuidebookVersion checks only")
    ap.add_argument("--report", action="store_true", help="Summary; exit 0 always")
    args = ap.parse_args()

    records = load_all_records()
    flat = all_records_flat(records)

    all_errors: list[str] = []
    all_warnings: list[str] = []

    def run(check_id: str, fn, *fargs):
        e, w = fn(*fargs)
        all_errors.extend(e)
        all_warnings.extend(w)

    # Determine which checks to run
    run_rules = args.rules or not (args.supersedence or args.versions)
    run_supersedence = args.supersedence or not (args.rules or args.versions)
    run_versions = args.versions or not (args.rules or args.supersedence)
    run_all = not (args.rules or args.supersedence or args.versions)

    if run_all or run_rules or run_supersedence or run_versions:
        # T-01, T-02 always run on whatever is loaded
        run("T-01", t01_date_format, flat)
        run("T-02", t02_no_future, flat)

    if run_all or run_supersedence:
        run("T-03/T-04", t03_t04_supersedence, records)
        run("T-10", t10_transition_citations, records["supersedence"])

    if run_all or run_versions:
        run("T-05", t05_version_filenames)
        run("T-06", t06_one_active, records["guidebook_versions"])

    if run_all:
        run("T-07", t07_source_year_consistency)
        run("T-08", t08_last_verified_coverage)
        run("T-09", t09_launch_phase)
        run("T-11", t11_freshness_windows)

    if run_all or run_rules:
        run("T-12", t12_pre_session_norm, records["rules"])

    # Report
    print(f"Temporal validation: {len(records['rules'])} rules, "
          f"{len(records['standards'])} standards, "
          f"{len(records['guidebook_versions'])} versions, "
          f"{len(records['supersedence'])} supersedence links")
    if all_errors:
        print(f"\nERRORS ({len(all_errors)}):")
        for e in all_errors:
            print(f"  {e}")
    if all_warnings:
        print(f"\nWARNINGS ({len(all_warnings)}):")
        for w in all_warnings:
            print(f"  {w}")
    if not all_errors and not all_warnings:
        print("All checks passed.")

    if args.report:
        return 0
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
