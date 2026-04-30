#!/usr/bin/env python3
"""
scripts/convert/version_retrofit.py — Retrofit temporal records from existing markdown.

Per governance/time-model.md (A9) §7. Walks:
  - references/project-standards.md  → data/temporal/rules/
  - references/standards-registry.md → data/temporal/standards/
  - versions/                        → data/temporal/guidebook_versions/
  - sessions/session_*.md            → data/temporal/sessions/
  - (computed)                       → data/temporal/supersedence/
  - (singleton)                      → data/temporal/launch_phase.yaml

Idempotent: a second run produces identical output. Source markdown is
never modified.

Usage:
    python3 scripts/convert/version_retrofit.py                    # full retrofit
    python3 scripts/convert/version_retrofit.py --dry-run          # report only
    python3 scripts/convert/version_retrofit.py --diff             # write to data/temporal_new/
    python3 scripts/convert/version_retrofit.py --kinds rules,versions
"""

import argparse
import os
import re
import sys
from collections import defaultdict

import yaml

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from schemas.temporal import (
    DATETIME_PATTERN,
    DATE_ONLY_PATTERN,
    PRE_SESSION_LITERAL,
    PRE_SESSION_NORMALISED,
    VERSION_TAG_PATTERN,
)

REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


# --- Slug helpers ---

def _slug(s: str, max_len: int = 40) -> str:
    """Lowercase, alphanumerics + hyphens only."""
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:max_len].rstrip("-")


# --- Date normalisation ---

def normalise_date(raw: str) -> tuple[str, str]:
    """Return (canonical_input, normalised_YYYY-MM-DD HH:MM).

    pre-session → ('pre-session', PRE_SESSION_NORMALISED)
    YYYY-MM-DD HH:MM → unchanged twice
    YYYY-MM-DD → (raw, 'YYYY-MM-DD 00:00')
    """
    raw = raw.strip()
    if raw.lower().startswith("established"):
        return PRE_SESSION_LITERAL, PRE_SESSION_NORMALISED
    if DATETIME_PATTERN.match(raw):
        return raw, raw
    if DATE_ONLY_PATTERN.match(raw):
        return raw, f"{raw} 00:00"
    # Common variants — try to coerce
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})\s+(\d{1,2}):(\d{2})", raw)
    if m:
        canonical = f"{m.group(1)}-{m.group(2)}-{m.group(3)} {int(m.group(4)):02d}:{m.group(5)}"
        return canonical, canonical
    # Unparseable; return raw twice and let the validator complain
    return raw, raw


# --- 1. Rule extraction from project-standards.md ---

RULE_KEYWORDS = ("RULE:", "CONDITION:", "ACTION:", "DATE:")


def extract_rules(path: str) -> tuple[list[dict], list[str]]:
    """Walk project-standards.md and emit one record per RULE block.

    State machine:
      idle → in_rule (RULE:) → may include CONDITION: ACTION: → DATE: closes block.
    """
    if not os.path.exists(path):
        return [], [f"project-standards.md not found at {path}"]

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    records: list[dict] = []
    warnings: list[str] = []

    current_section = "Top"
    current: dict | None = None
    field: str | None = None  # which keyword we are accumulating into

    section_seq: dict[str, int] = defaultdict(int)

    def flush(rec: dict | None) -> None:
        if rec is None:
            return
        if "rule_text" not in rec or not rec["rule_text"].strip():
            warnings.append(
                f"line {rec.get('source_line', '?')}: RULE without body skipped"
            )
            return
        if "effective_date" not in rec:
            warnings.append(
                f"line {rec.get('source_line', '?')}: RULE without DATE: skipped "
                f"(text starts: {rec['rule_text'][:60]!r})"
            )
            return
        # Synthesize rule_id
        section_slug = _slug(rec["section"]) or "section"
        section_seq[section_slug] += 1
        rec["rule_id"] = f"RULE-{section_slug}-{section_seq[section_slug]}"
        # Normalise date
        ed, edn = normalise_date(rec["effective_date"])
        rec["effective_date"] = ed
        rec["effective_date_normalized"] = edn
        # Status default
        rec.setdefault("status", "ACTIVE")
        rec.setdefault("source_file", "references/project-standards.md")
        # Trim text
        for k in ("rule_text", "condition", "action"):
            if k in rec and isinstance(rec[k], str):
                rec[k] = rec[k].strip()
        records.append(rec)

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Track section
        h_match = re.match(r"^(#{1,6})\s+(.+?)(?:\s*<!--.*-->)?\s*$", stripped)
        if h_match and h_match.group(1) in ("##", "###", "####"):
            # New section: close any open rule
            flush(current)
            current = None
            field = None
            current_section = h_match.group(2).strip()
            continue

        # Check for keyword start
        keyword_match = None
        for kw in RULE_KEYWORDS:
            if stripped.startswith(kw):
                keyword_match = kw
                break

        if keyword_match == "RULE:":
            flush(current)
            current = {
                "rule_text": stripped[len("RULE:"):].strip(),
                "section": current_section,
                "source_line": i,
            }
            field = "rule_text"
            continue

        if keyword_match == "CONDITION:" and current is not None:
            current["condition"] = stripped[len("CONDITION:"):].strip()
            field = "condition"
            continue

        if keyword_match == "ACTION:" and current is not None:
            current["action"] = stripped[len("ACTION:"):].strip()
            field = "action"
            continue

        if keyword_match == "DATE:" and current is not None:
            current["effective_date"] = stripped[len("DATE:"):].strip()
            flush(current)
            current = None
            field = None
            continue

        # Continuation lines: append to current field
        if current is not None and field and stripped:
            # Skip continuation if line is HR or comment
            if stripped.startswith("---") or stripped.startswith("<!--"):
                # HR closes the rule context
                flush(current)
                current = None
                field = None
                continue
            current[field] = (current.get(field, "") + " " + stripped).strip()

    # End-of-file flush
    flush(current)

    return records, warnings


# --- 2. Standards extraction from standards-registry.md ---

def extract_standards(path: str) -> tuple[list[dict], list[str]]:
    """Parse standards-registry.md YAML blocks into StandardEdition records."""
    if not os.path.exists(path):
        return [], [f"standards-registry.md not found at {path}"]

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    records: list[dict] = []
    warnings: list[str] = []

    blocks = re.findall(r"```yaml\s*\n(.*?)```", content, re.DOTALL)
    for i, block in enumerate(blocks, start=1):
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError as e:
            warnings.append(f"block {i}: YAML parse error: {e}")
            continue
        if not isinstance(data, dict):
            continue
        # Skip template/placeholder entries (jurisdiction is non-string or contains template wording)
        jur = data.get("jurisdiction")
        if not isinstance(jur, str):
            continue
        if "letter code" in jur.lower() or "or full name" in jur.lower():
            continue

        # standard_cited IS the canonical edition string (e.g. "AS 1428.1:2021").
        # current_version describes the latest state (may differ when SUPERSEDED/UPDATED).
        edition = data.get("standard_cited") or data.get("standard_family")
        if not edition or not isinstance(edition, str):
            warnings.append(f"block {i}: missing standard_cited (input: {data!r})")
            continue
        edition = edition.strip()

        # Family: text before first colon or paren in edition
        family_split = re.split(r"[:(]", edition, maxsplit=1)
        family = family_split[0].strip()

        # Normalize date-only last_checked to datetime (00:00)
        lc = data.get("last_checked")
        if isinstance(lc, str) and DATE_ONLY_PATTERN.match(lc.strip()):
            lc = f"{lc.strip()} 00:00"
        rec = {
            "jurisdiction": jur,
            "standard_family": family,
            "edition": edition,
            "status": data.get("status"),
            "last_checked": lc,
        }
        # current_version differs from standard_cited when SUPERSEDED — capture as supersedes target
        cv = data.get("current_version")
        if isinstance(cv, str) and cv.strip() and cv.strip() != edition:
            # For SUPERSEDED entries, current_version names the successor
            rec["current_version_text"] = cv.strip()
        # Optional fields
        if "publication_date" in data:
            rec["publication_date"] = data["publication_date"]
        if "transition_until_date" in data:
            rec["transition_until_date"] = data["transition_until_date"]
        notes_parts = []
        for k in ("key_changes", "source_url"):
            if data.get(k):
                notes_parts.append(f"{k}: {data[k]}")
        if notes_parts:
            rec["notes"] = " | ".join(notes_parts)
        records.append(rec)

    return records, warnings


# --- 3. Version directory walk ---

def extract_versions(versions_root: str) -> tuple[list[dict], list[str]]:
    """Walk versions/ tree and emit GuidebookVersion records."""
    records: list[dict] = []
    warnings: list[str] = []
    if not os.path.isdir(versions_root):
        return [], [f"versions/ directory not found at {versions_root}"]

    # Each subdirectory becomes a record
    for entry in sorted(os.listdir(versions_root)):
        full = os.path.join(versions_root, entry)
        if not os.path.isdir(full):
            continue

        # Find the document file
        md_files = sorted(
            f for f in os.listdir(full)
            if f.endswith(".md") and f.startswith("Guidebook_for_Accessible_Design_")
        )
        if not md_files:
            warnings.append(f"versions/{entry}/: no Guidebook_for_Accessible_Design_*.md")
            continue
        if len(md_files) > 1:
            warnings.append(
                f"versions/{entry}/: multiple document files: {md_files}; using first"
            )
        doc = md_files[0]

        # Parse version + effective_date from filename
        # Pattern: Guidebook_for_Accessible_Design_v{tag}_{YYYY-MM-DD}.md
        # Or:      Guidebook_for_Accessible_Design_v{tag}-prep.md
        m = re.match(
            r"^Guidebook_for_Accessible_Design_v(\d+)-(\d+)(?:_(\d{4}-\d{2}-\d{2}))?(?:-prep)?\.md$",
            doc,
        )
        if not m:
            warnings.append(f"versions/{entry}/{doc}: unparseable filename")
            continue
        version_tag = f"v{m.group(1)}.{m.group(2)}"
        effective_date = m.group(3)
        is_prep = doc.endswith("-prep.md") or "-prep" in doc

        # Determine status
        if entry == "current":
            status = "ACTIVE"
        elif is_prep:
            status = "IN_PREP"
        else:
            status = "ARCHIVED"

        rec = {
            "version_tag": version_tag,
            "effective_date": effective_date,
            "file_path": f"versions/{entry}/{doc}",
            "status": status,
        }
        records.append(rec)

    # Compute supersedence chain by version order (string-sortable for major.minor up to single-digit minors;
    # use tuple ordering for safety)
    def vtag_key(rec: dict) -> tuple[int, int]:
        m = VERSION_TAG_PATTERN.match(rec["version_tag"])
        if m:
            return (int(m.group(1)), int(m.group(2)))
        return (0, 0)

    sorted_recs = sorted(records, key=vtag_key)
    for prev, curr in zip(sorted_recs, sorted_recs[1:]):
        if curr.get("status") in {"ACTIVE", "ARCHIVED"} and prev.get("status") != "IN_PREP":
            curr["supersedes"] = prev["version_tag"]

    return records, warnings


# --- 4. Session walk ---

def extract_sessions(sessions_dir: str) -> tuple[list[dict], list[str]]:
    """Extract session_close from each session_*.md file."""
    records: list[dict] = []
    warnings: list[str] = []
    if not os.path.isdir(sessions_dir):
        return [], []  # not error — sessions/ may not exist in test corpus

    YAML_BLOCK = re.compile(r"```yaml\s*\n(.*?)```", re.DOTALL)
    for fn in sorted(os.listdir(sessions_dir)):
        if not (fn.startswith("session_") and fn.endswith(".md")):
            continue
        path = os.path.join(sessions_dir, fn)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            warnings.append(f"sessions/{fn}: read error: {e}")
            continue
        # Take the LAST yaml block (session-close convention)
        blocks = YAML_BLOCK.findall(content)
        if not blocks:
            continue
        try:
            data = yaml.safe_load(blocks[-1])
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        rec = {
            "session_id": fn,
            "session_close": data.get("session_close"),
            "next_action_skill": (data.get("next_action") or {}).get("skill"),
        }
        if data.get("github_writes"):
            # Capture commit_oid if present
            for w in data["github_writes"]:
                if isinstance(w, dict) and "commit_oid" in w:
                    rec["commit_oid"] = w["commit_oid"]
                    break
        records.append(rec)

    return records, warnings


# --- 5. Supersedence detection ---

def detect_supersedence(
    rules: list[dict],
    standards: list[dict],
    versions: list[dict],
) -> tuple[list[dict], list[str]]:
    """Compute SupersedenceLink records from extracted entities."""
    links: list[dict] = []
    warnings: list[str] = []

    # 5a. Standards: every SUPERSEDED entry produces a link to its successor
    # The registry encodes successor in current_version when status is SUPERSEDED.
    rule_seq = 0
    standard_seq = 0
    version_seq = 0

    # Build a lookup: jurisdiction → list of standards
    by_jur: dict[str, list[dict]] = defaultdict(list)
    for s in standards:
        jur = s.get("jurisdiction")
        if isinstance(jur, str):
            by_jur[jur].append(s)

    for s in standards:
        if s.get("status") != "SUPERSEDED":
            continue
        jur = s.get("jurisdiction")
        if not isinstance(jur, str):
            continue
        # current_version_text names the successor for SUPERSEDED entries.
        # Try to extract an edition string from it: alphanumeric/punct up to first '('
        cvt = s.get("current_version_text", "")
        successor_edition = None
        if cvt:
            # Take prefix up to first '(' or 'supersedes' or end
            cand = re.split(r"\s*\(|supersedes|—", cvt, maxsplit=1)[0].strip()
            # Look for matching CURRENT entry in same jurisdiction
            for o in by_jur.get(jur, []):
                if o.get("status") == "CURRENT" and (
                    o.get("edition") == cand or
                    cand.startswith(o.get("standard_family", ""))
                ):
                    successor_edition = o.get("edition")
                    break
        # Fall back: if exactly one CURRENT in jurisdiction and same family
        if successor_edition is None:
            same_fam = [
                o for o in by_jur.get(jur, [])
                if o.get("status") == "CURRENT"
                and o.get("standard_family") == s.get("standard_family")
            ]
            if len(same_fam) == 1:
                successor_edition = same_fam[0].get("edition")
        if successor_edition is None:
            warnings.append(
                f"standards: SUPERSEDED entry '{s.get('edition')}' "
                f"({jur}) — no successor identified"
            )
            continue
        # Skip self-link
        if successor_edition == s.get("edition"):
            continue
        standard_seq += 1
        link = {
            "link_id": f"SUP-standard-{standard_seq:04d}",
            "link_type": "standard",
            "from_id": s.get("edition"),
            "to_id": successor_edition,
            "effective_date": (s.get("last_checked") or "2026-01-01 00:00").split()[0],
            "rationale": f"{successor_edition} supersedes {s.get('edition')} per registry",
            "source": "registry",
            "status": "ACTIVE",
        }
        if s.get("transition_until_date"):
            link["transition_until_date"] = s["transition_until_date"]
        links.append(link)

    # 5b. Versions: chain supersedence built into version records → emit links
    for v in versions:
        if v.get("supersedes"):
            version_seq += 1
            links.append({
                "link_id": f"SUP-version-{version_seq:04d}",
                "link_type": "version",
                "from_id": v["supersedes"],
                "to_id": v["version_tag"],
                "effective_date": v.get("effective_date") or "1970-01-01",
                "rationale": f"{v['version_tag']} supersedes {v['supersedes']}",
                "source": "version_directory",
                "status": "ACTIVE",
            })

    # 5c. Rules: explicit "supersedes"/"replaces" detection in rule_text
    EXPLICIT = re.compile(
        r"\b(supersedes|replaces|retires|consolidat\w*\s+from)\b", re.IGNORECASE
    )
    for r in rules:
        text = (r.get("rule_text") or "") + " " + (r.get("condition") or "")
        if EXPLICIT.search(text):
            rule_seq += 1
            links.append({
                "link_id": f"SUP-rule-{rule_seq:04d}",
                "link_type": "rule",
                "from_id": "UNRESOLVED",
                "to_id": r["rule_id"],
                "effective_date": r["effective_date_normalized"],
                "rationale": (
                    "Rule text contains explicit supersedence cue "
                    "('supersedes', 'replaces', etc.); from_id requires manual resolution"
                ),
                "source": "textual_cue",
                "status": "PROVISIONAL",
            })

    return links, warnings


# --- 6. Launch phase singleton ---

def emit_launch_phase() -> dict:
    """Emit the launch_phase singleton record per A5."""
    return {
        "phase": "pre_launch",
        "since": "2026-04-26 03:45",
        "triggers_met": {
            "launch_event": False,
            "resources_available": False,
            "co_designed_recruitment_spec": False,
        },
        "history": [],
    }


# --- Writing ---

def _yaml_dump(data: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(
            data, f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )


def write_records(
    records: list[dict],
    subdir: str,
    name_fn,
    out_root: str,
) -> int:
    """Write each record to {out_root}/{subdir}/{name_fn(rec)}.yaml."""
    target_dir = os.path.join(out_root, subdir)
    os.makedirs(target_dir, exist_ok=True)
    n = 0
    for rec in records:
        name = name_fn(rec)
        if not name:
            continue
        _yaml_dump(rec, os.path.join(target_dir, f"{name}.yaml"))
        n += 1
    return n


# --- Main ---

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument("--dry-run", action="store_true", help="report only, no writes")
    ap.add_argument("--diff", action="store_true",
                    help="write to data/temporal_new/ instead of data/temporal/")
    ap.add_argument("--kinds", default="all",
                    help="comma-separated subset: rules,standards,versions,sessions,supersedence,launch_phase")
    args = ap.parse_args()

    out_root = os.path.join(
        args.repo_root,
        "data/temporal_new" if args.diff else "data/temporal",
    )
    kinds = set(args.kinds.split(",")) if args.kinds != "all" else {
        "rules", "standards", "versions", "sessions", "supersedence", "launch_phase"
    }

    all_warnings: list[str] = []
    summary: list[str] = []

    rules: list[dict] = []
    standards: list[dict] = []
    versions: list[dict] = []
    sessions: list[dict] = []

    if "rules" in kinds:
        rules, w = extract_rules(
            os.path.join(args.repo_root, "references/project-standards.md")
        )
        all_warnings.extend(w)
        summary.append(f"rules: {len(rules)}")

    if "standards" in kinds:
        standards, w = extract_standards(
            os.path.join(args.repo_root, "references/standards-registry.md")
        )
        all_warnings.extend(w)
        summary.append(f"standards: {len(standards)}")

    if "versions" in kinds:
        versions, w = extract_versions(os.path.join(args.repo_root, "versions"))
        all_warnings.extend(w)
        summary.append(f"versions: {len(versions)}")

    if "sessions" in kinds:
        sessions, w = extract_sessions(os.path.join(args.repo_root, "sessions"))
        all_warnings.extend(w)
        summary.append(f"sessions: {len(sessions)}")

    supersedence: list[dict] = []
    if "supersedence" in kinds:
        # Need rules+standards+versions loaded to compute
        if not rules and "rules" not in kinds:
            rules, _ = extract_rules(
                os.path.join(args.repo_root, "references/project-standards.md")
            )
        if not standards and "standards" not in kinds:
            standards, _ = extract_standards(
                os.path.join(args.repo_root, "references/standards-registry.md")
            )
        if not versions and "versions" not in kinds:
            versions, _ = extract_versions(os.path.join(args.repo_root, "versions"))
        supersedence, w = detect_supersedence(rules, standards, versions)
        all_warnings.extend(w)
        summary.append(f"supersedence: {len(supersedence)}")

    print("Retrofit summary: " + ", ".join(summary))
    if all_warnings:
        print(f"\nWarnings ({len(all_warnings)}):")
        for w in all_warnings[:50]:
            print(f"  {w}")
        if len(all_warnings) > 50:
            print(f"  ... ({len(all_warnings) - 50} more)")

    if args.dry_run:
        print("\n--dry-run: no files written")
        return 0

    written = 0
    if "rules" in kinds and rules:
        written += write_records(
            rules, "rules", lambda r: r["rule_id"], out_root
        )
    if "standards" in kinds and standards:
        def std_name(r):
            jur = r.get("jurisdiction", "X")
            fam = _slug(r.get("standard_family", "x"), 30)
            ed = _slug(r.get("edition", "x"), 50)
            return f"{jur}_{fam}_{ed}"
        written += write_records(standards, "standards", std_name, out_root)
    if "versions" in kinds and versions:
        def version_name(r):
            # Name by source directory to avoid collisions when prep file in a
            # named-after-prior-version folder shares its tag with the active.
            fp = r.get("file_path", "")
            parts = fp.split("/")
            # versions/{folder}/...
            folder = parts[1] if len(parts) >= 3 and parts[0] == "versions" else r["version_tag"].replace(".", "-")
            return folder.replace(".", "-")
        written += write_records(
            versions, "guidebook_versions", version_name, out_root,
        )
    if "sessions" in kinds and sessions:
        written += write_records(
            sessions, "sessions",
            lambda r: r["session_id"].replace(".md", ""),
            out_root,
        )
    if "supersedence" in kinds and supersedence:
        written += write_records(
            supersedence, "supersedence", lambda r: r["link_id"], out_root,
        )
    if "launch_phase" in kinds:
        _yaml_dump(emit_launch_phase(), os.path.join(out_root, "launch_phase.yaml"))
        written += 1

    print(f"\nWrote {written} files to {out_root}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
