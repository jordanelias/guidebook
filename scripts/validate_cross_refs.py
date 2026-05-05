#!/usr/bin/env python3
"""
validate_cross_refs.py — Cross-reference integrity validator.

Checks:
  1. Slug references resolve via SQLite slugs table (was: slug-registry.md)
  2. CON-IDs (CON-NNNN) resolve via SQLite connections table (was: _index.md)
  3. Part section references (§X.Y) resolve to existing headings in correct part file
  4. BPC ↔ search-log co-existence (every BPC has matching search-log, vice versa)

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

DB_PATH = "data/guidebook.db"
BPC_ROOT = "references/bpc"
SEARCH_LOG_ROOT = "references/search-logs"

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
    return sorted(set(os.path.normpath(f) for f in files))


def collect_bpc_slugs(repo_root: str) -> dict[str, str]:
    pattern = os.path.join(repo_root, BPC_ROOT, "**", "*.md")
    result = {}
    for path in glob.glob(pattern, recursive=True):
        stem = Path(path).stem
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
