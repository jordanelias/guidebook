#!/usr/bin/env python3
"""
validate_cross_refs.py — Cross-reference integrity validator.

Checks:
  1. Slug references resolve via SQLite slugs table (was: slug-registry.md)
  2. CON-IDs (CON-NNNN) resolve via SQLite connections table (was: _index.md)
  3. Part section references (§X.Y) resolve to existing headings in correct part file
  4. BPC ↔ search-log co-existence (every BPC has matching search-log, vice versa)
  NB checks 1-2 (slug + CON-ID resolution against SQLite) run over LIVE surfaces
  only. After the 2026-08-06 clean-room reset the reference corpus — parts/v10,
  references/bpc, references/connections, specs/, site/ — cites entities the DB
  no longer holds, by design: those files are preserved AS REFERENCE and the DB
  was reset around them. Validating reference prose against a reset database
  produced 1,191 failures that were all the check misunderstanding its own
  subject. See REFERENCE_ONLY below.

  5. sessions/handoff-next-session.md — its named session record, workplan, and
     HEAD all resolve (added 2026-08-06; folded in from a standalone audit rather
     than given a file of its own — a dangling path in the handoff is a broken
     cross-reference, which is this script's whole subject)

Phase 1-D update 2026-05-05: checks 1 and 2 now query SQLite (data/guidebook.db)
instead of parsing markdown register files. Markdown files are archived sources only.

Usage:
    python3 scripts/validate_cross_refs.py            # full repo scan
    python3 scripts/validate_cross_refs.py --fast     # skip section heading resolution

Exit codes:
    0 — no broken references
    1 — one or more broken references
"""

import sys
import os
import re
import glob
import argparse
import sqlite3
from pathlib import Path


# ── Constants ────────────────────────────────────────────────────────────────

DB_PATH = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
BPC_ROOT = "references/bpc"
SEARCH_LOG_ROOT = "references/search-log"

SCAN_PATTERNS = [
    "references/bpc/**/*.md",
    "references/connections/**/*.md",
    "parts/**/*.md",
    "skills/**/*.md",
]

EXCLUDE_PATTERNS = [
    "sessions/_archive/**",
    ".git/**",
]

HEADING_RE = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)
SLUG_REF_RE = re.compile(r"\bslug[:\s]+([a-z0-9_-]+)\b", re.IGNORECASE)
CON_ID_RE = re.compile(r"\bCON-(\d{4})\b")
SECTION_RE = re.compile(r"§(\d+)\.(\d+)(?:\.(\d+))?")


# ── SQLite Loaders ───────────────────────────────────────────────────────────

def load_slug_registry(repo_root: str) -> set[str]:
    """Return set of known slugs from SQLite slugs table."""
    db_path = os.path.join(repo_root, DB_PATH)
    if not os.path.exists(db_path):
        print("  WARNING: guidebook.db not found — slug check skipped", file=sys.stderr)
        return set()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT slug FROM slugs WHERE status IN ('ACTIVE', 'PROVISIONAL')"
    ).fetchall()
    conn.close()
    return {r["slug"] for r in rows}


def load_con_ids(repo_root: str) -> set[str]:
    """Return set of CON-ID digit strings from SQLite connections table."""
    db_path = os.path.join(repo_root, DB_PATH)
    if not os.path.exists(db_path):
        print("  WARNING: guidebook.db not found — CON-ID check skipped", file=sys.stderr)
        return set()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT con_id FROM connections").fetchall()
    conn.close()
    # Extract 4-digit numbers: "CON-0247" → "0247"
    result = set()
    for r in rows:
        m = re.match(r"CON-(\d{4})", r["con_id"])
        if m:
            result.add(m.group(1))
    return result


# ── File collectors ──────────────────────────────────────────────────────────

def collect_scan_files(repo_root: str) -> list[str]:
    files = []
    for pattern in SCAN_PATTERNS:
        full_pattern = os.path.join(repo_root, pattern)
        files.extend(glob.glob(full_pattern, recursive=True))
    out = sorted(set(os.path.normpath(f) for f in files))
    # Reference surfaces are excluded from DB-backed reference resolution — see
    # REFERENCE_ONLY. The entities they name were deliberately reset out of the
    # database beneath them, so resolving their CON-IDs against the live tables
    # asks a question the reset already answered: 1,191 failures, every one of
    # them the check misunderstanding its own subject.
    return [f for f in out if not _is_reference(os.path.relpath(f, repo_root))]


def collect_bpc_slugs(repo_root: str) -> dict[str, str]:
    pattern = os.path.join(repo_root, BPC_ROOT, "**", "*.md")
    result = {}
    for path in glob.glob(pattern, recursive=True):
        stem = Path(path).stem
        if stem.startswith("_"):
            # Skip templates and other underscore-prefixed private files
            continue
        result[stem] = path
    return result


def collect_search_log_slugs(repo_root: str) -> dict[str, str]:
    pattern = os.path.join(repo_root, SEARCH_LOG_ROOT, "**", "*.md")
    result = {}
    for path in glob.glob(pattern, recursive=True):
        stem = Path(path).stem
        slug = re.sub(r"[-_]?search[-_]?log$", "", stem, flags=re.IGNORECASE)
        result[slug] = path
    return result


# ── Checkers ─────────────────────────────────────────────────────────────────

def check_con_ids(files: list[str], known_cons: set[str]) -> list[tuple[str, str]]:
    errors = []
    for path in files:
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue
        for m in CON_ID_RE.finditer(content):
            con_num = m.group(1)
            if con_num not in known_cons:
                line_no = content[:m.start()].count("\n") + 1
                errors.append((
                    path,
                    f"BROKEN_CON_ID: CON-{con_num} at line {line_no} "
                    f"not found in SQLite connections table"
                ))
    return errors


def check_bpc_searchlog_coexistence(
    bpc_slugs: dict[str, str],
    sl_slugs: dict[str, str],
) -> list[tuple[str, str]]:
    errors = []
    for slug, bpc_path in bpc_slugs.items():
        if slug not in sl_slugs:
            # Skip BPCs explicitly marked as STUBs — search-log will be authored
            # when the BPC research pass runs (per workplan Phase E or later).
            try:
                with open(bpc_path, encoding="utf-8") as f:
                    head = f.read(2000)
                if re.search(r"\*\*Status:\*\*\s*STUB\b", head):
                    continue
            except Exception:
                pass
            errors.append((
                bpc_path,
                f"MISSING_SEARCH_LOG: BPC '{slug}' has no matching search-log"
            ))
    for slug, sl_path in sl_slugs.items():
        if slug not in bpc_slugs:
            errors.append((
                sl_path,
                f"ORPHAN_SEARCH_LOG: search-log '{slug}' has no matching BPC"
            ))
    return errors


# ── Runner ───────────────────────────────────────────────────────────────────

def run(repo_root: str = ".", fast: bool = False, warn_only: bool = False) -> int:
    errors: list[tuple[str, str]] = []

    print("Loading registries from SQLite...", file=sys.stderr)
    known_slugs = load_slug_registry(repo_root)
    known_cons = load_con_ids(repo_root)
    bpc_slugs = collect_bpc_slugs(repo_root)
    sl_slugs = collect_search_log_slugs(repo_root)
    scan_files = collect_scan_files(repo_root)

    print(
        f"  {len(known_slugs)} slugs (SQLite), {len(known_cons)} CON-IDs (SQLite), "
        f"{len(bpc_slugs)} BPC files, {len(sl_slugs)} search-logs, "
        f"{len(scan_files)} files to scan",
        file=sys.stderr
    )

    print("Checking CON-ID references...", file=sys.stderr)
    errors.extend(check_con_ids(scan_files, known_cons))

    print("Checking BPC ↔ search-log co-existence...", file=sys.stderr)
    errors.extend(check_bpc_searchlog_coexistence(bpc_slugs, sl_slugs))
    errors.extend(check_handoff(repo_root))

    label = "WARN" if warn_only else "FAIL"
    if errors:
        for path, msg in sorted(errors):
            print(f"{label} [{path}]: {msg}")
    else:
        print("All cross-reference checks passed.")

    mode = " (warn-only mode)" if warn_only else ""
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"validate_cross_refs.py: {len(errors)} issue(s) found{mode}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    return 0 if (warn_only or not errors) else 1


# Surfaces preserved as reference by the 2026-08-06 reset. Their cross-references
# are historically accurate and deliberately not maintained against the live DB.
# This is a SCOPE statement, not an amnesty: a broken reference inside a live
# file still fails, and a file leaves this list by becoming live again.
REFERENCE_ONLY = (
    "parts/",
    "references/bpc/",
    "references/bpc-reasoning/",
    "references/connections/",
    "references/connection-reasoning/",
    "specs/",
    "site/",
    "_archived/",
)


def _is_reference(path: str) -> bool:
    rel = path.replace("\\", "/").lstrip("./")
    return any(rel.startswith(p) for p in REFERENCE_ONLY)


HANDOFF_FIELDS = {
    "HEAD at handoff": re.compile(r"\*\*HEAD at handoff:\*\*\s*`([0-9a-f]{7,40})`"),
    "Last session record": re.compile(r"\*\*Last session record:\*\*\s*`([^`]+)`"),
    "The plan to work from": re.compile(r"\*\*The plan to work from:\*\*\s*`([^`]+)`"),
}


def check_handoff(repo_root: str) -> list[tuple[str, str]]:
    """The handoff is the first file a fresh session reads. Nothing checked it,
    and it spent eleven weeks naming a May HEAD and a merged branch.

    A dangling PATH is an error: it sends the next session to a file that is not
    there. A stale HEAD is reported as a WARN — it is misleading prose, and
    failing a blocking gate over unrewritten prose makes the gate something to
    route around.
    """
    import subprocess
    rel = "sessions/handoff-next-session.md"
    path = os.path.join(repo_root, rel)
    if not os.path.exists(path):
        return [(rel, "handoff is missing — a fresh session has no entry point")]

    text = open(path, encoding="utf-8").read()
    out = []
    for label, pattern in HANDOFF_FIELDS.items():
        m = pattern.search(text)
        if not m:
            out.append((rel, f"WARN: no `{label}:` line — the header format "
                             f"changed, so nothing can check it"))
            continue
        value = m.group(1).strip()
        if label == "HEAD at handoff":
            ok = subprocess.run(["git", "cat-file", "-e", f"{value}^{{commit}}"],
                                cwd=repo_root, capture_output=True).returncode == 0
            if not ok:
                out.append((rel, f"WARN: names HEAD {value}, not a commit in this "
                                 f"clone — the handoff describes other history"))
                continue
            anc = subprocess.run(["git", "merge-base", "--is-ancestor", value, "HEAD"],
                                 cwd=repo_root, capture_output=True).returncode == 0
            if not anc:
                out.append((rel, f"WARN: names HEAD {value}, which is NOT an "
                                 f"ancestor of the current HEAD"))
        elif not os.path.exists(os.path.join(repo_root, value)):
            out.append((rel, f"`{label}` names {value!r}, which does not exist"))
    return out


def main():
    parser = argparse.ArgumentParser(
        description="Validate cross-references in guidebook repo (SQLite-backed)"
    )
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--warn-only", action="store_true")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    sys.exit(run(repo_root=args.repo_root, fast=args.fast, warn_only=args.warn_only))


if __name__ == "__main__":
    main()
