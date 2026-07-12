#!/usr/bin/env python3
"""
schema_reference_drift_audit.py — Level 2 audit for table-reference drift.

Per architecture/project-architecture-guidebook-v2.3.md <data_layer_pattern>:
"The SQLite database... is the single source of truth. Markdown files and
JSON exports may derive from it but never compete with it." A specific
recurring failure of that principle already caught once (website-generator
scripts referencing tables removed/renamed in the live schema, reconciled
2026-07-12) is: source code that queries a table name no longer (or never)
present in the actual database. This script re-checks for that specific
failure mode going forward.

Two checks:
  1. Table-reference drift: scans the *currently-live* script surface —
     scripts/generate/ (the site/page generators; this is exactly where the
     one already-caught phantom-table bug lived), scripts/audit/,
     scripts/ci_helpers/, scripts/convert/, and loose scripts/*.py files —
     for SQL keywords FROM/JOIN/INTO/UPDATE followed by an identifier, and
     flags any referenced table name absent from the live database. FAIL.
     Deliberately excludes scripts/migrations/ (defines tables, doesn't
     reference them), scripts/db/, scripts/migrate/, scripts/probes/ (one-time
     historical migration/seed scripts that legitimately reference an older
     schema shape the live DB no longer has — see
     audits/project-inventory-and-state-2026-07-12.md finding 3 on DB
     non-reproducibility from migration history). scripts/tests/ (plural)
     is EXCLUDED FOR A DIFFERENT REASON than the docstring originally
     (wrongly) claimed: it is NOT dead/fixture-only code —
     .github/workflows/ci.yml runs scripts/tests/test_db_integrity.py as a
     blocking check on every push. It is excluded because that file
     references a known-legacy table (evidence_sources_v1_legacy) behind an
     explicit existence guard this lexical scanner cannot see, which would
     otherwise be a guaranteed false positive; scripts/test/ (singular) is
     excluded as an actual one-time/legacy directory, same rationale as
     scripts/db/migrate/probes/.
  2. Unreferenced tables: tables that exist in the live database but are
     never referenced by any scanned (live-surface) script. Not a failure —
     some tables are legitimately populated only by migrations or read only
     via ad hoc/legacy tooling excluded from check 1 — surfaced as INFO for
     the owner to sanity-check. Tables only ever referenced through dynamic
     (f-string-interpolated) table names are reported separately (see check 3)
     rather than folded into this INFO list, since this scanner cannot
     resolve an interpolated variable to a table name and would otherwise
     misreport those tables as fully unreferenced.
  3. Dynamic references: FROM/JOIN/etc. followed by an f-string
     `{variable}` instead of a literal identifier. These cannot be resolved
     to a table name by a lexical scan, so they are listed as INFO
     (file + line count) rather than silently dropped or silently folded
     into check 2's "unreferenced" count — an earlier version of this
     script did the latter, which produced an incorrect INFO list (tables
     actually referenced via scripts/audit/population_integrity_audit.py's
     `f"...FROM {jt}"` pattern showed up as "unreferenced").

Known limitations (stated explicitly rather than silently over-claimed):
  - Only matches UPPERCASE SQL keywords (FROM/JOIN/INTO/UPDATE), matching
    this codebase's embedded-SQL style. This deliberately avoids matching
    Python's lowercase `from x import y` syntax, at the cost of missing any
    embedded SQL written in lowercase.
  - A pure lexical scan cannot distinguish a real table from a CTE alias
    introduced by a `WITH alias AS (...)` clause in the same query — such
    aliases can surface as false-positive "missing table" hits and need a
    human read of the flagged line, not blind trust in the FAIL count.
  - Excluding scripts/db/, scripts/migrate/, scripts/probes/, scripts/test/
    trades recall for precision: if one of those directories starts holding
    live, routinely-run code rather than one-time historical scripts, it
    should move out of EXCLUDE_DIRS. This exclusion is directory-based, not
    semantic — a one-time/legacy script sitting as a loose file directly in
    scripts/ (e.g. scripts/migrate_evidence_sources_v2.py) is NOT excluded
    just because its purpose matches the excluded directories', and can
    still surface as a real (if low-priority) check-1 hit.
  - Does not parse schemas/*.py Pydantic models against column definitions;
    Pydantic models here are hand-structured (nested objects, computed
    fields) and do not map 1:1 to SQL columns, so a field-level diff would
    produce more noise than signal. This script checks table-name
    reachability only, not column-level parity.

Usage:
    python3 scripts/audit/schema_reference_drift_audit.py
    GUIDEBOOK_DB_PATH=/path/to/db python3 scripts/audit/schema_reference_drift_audit.py

Exit codes: 0 = pass (check 1 clean), 1 = check 1 found a missing-table reference.
"""
import os
import re
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.environ.get(
    "GUIDEBOOK_DB_PATH",
    str(REPO_ROOT / "data" / "guidebook.db"),
))

SCRIPTS_DIR = REPO_ROOT / "scripts"
EXCLUDE_DIRS = {"migrations", "db", "migrate", "probes", "test", "tests"}
THIS_FILE = Path(__file__).resolve()

TABLE_REF_RE = re.compile(r'\b(?:FROM|JOIN|INTO|UPDATE)\s+["\'`]?([A-Za-z_][A-Za-z0-9_]*)')
DYNAMIC_REF_RE = re.compile(r'\b(?:FROM|JOIN|INTO|UPDATE)\s+\{(\w+)\}')

SQLITE_INTERNAL_PREFIXES = ("sqlite_",)


def live_tables(conn):
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    return {r[0] for r in rows if not r[0].startswith(SQLITE_INTERNAL_PREFIXES)}


def scan_references():
    """Return (refs, dynamic_refs).

    refs: {table_name: set of relative file paths that reference it via a
    literal identifier}.
    dynamic_refs: {relative file path: count of FROM/JOIN/etc. followed by
    an f-string {variable} this scanner cannot resolve to a table name}.
    """
    refs = {}
    dynamic_refs = {}
    for path in SCRIPTS_DIR.rglob("*.py"):
        if path.resolve() == THIS_FILE:
            continue
        if any(part in EXCLUDE_DIRS for part in path.relative_to(SCRIPTS_DIR).parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = str(path.relative_to(REPO_ROOT))
        for m in TABLE_REF_RE.finditer(text):
            table = m.group(1)
            refs.setdefault(table, set()).add(rel)
        n_dynamic = len(DYNAMIC_REF_RE.findall(text))
        if n_dynamic:
            dynamic_refs[rel] = n_dynamic
    return refs, dynamic_refs


def audit():
    if not DB_PATH.exists():
        print(f"ERROR: DB not found at {DB_PATH}", file=sys.stderr)
        return 1

    try:
        conn = sqlite3.connect(DB_PATH)
        tables = live_tables(conn)
    except sqlite3.DatabaseError as e:
        print(f"ERROR: {DB_PATH} is not a readable SQLite database: {e}", file=sys.stderr)
        return 1

    refs, dynamic_refs = scan_references()

    print("=" * 70)
    print("schema_reference_drift_audit.py")
    print("=" * 70)
    print()

    exit_code = 0

    # Check 1: referenced-but-missing tables (sqlite internals, e.g.
    # sqlite_master, are never "missing" — they're not project tables).
    missing = {
        t: files for t, files in refs.items()
        if t not in tables and not t.startswith(SQLITE_INTERNAL_PREFIXES)
    }
    if missing:
        print(f"[1] FAIL: {len(missing)} referenced table name(s) not found in live DB")
        for t in sorted(missing):
            files = sorted(missing[t])
            print(f"    {t}")
            for f in files[:5]:
                print(f"      referenced in: {f}")
            if len(files) > 5:
                print(f"      ... ({len(files) - 5} more files)")
        exit_code = 1
    else:
        print("[1] PASS: every table referenced in scripts/ exists in the live DB")

    # Check 2: tables never referenced (informational only).
    print()
    referenced_tables = set(refs) & tables
    unreferenced = sorted(tables - referenced_tables)
    print(f"[2] INFO: {len(unreferenced)} / {len(tables)} live tables not referenced by any scanned script")
    if unreferenced:
        print("    (not a failure — some tables are populated by migrations only, or read via")
        print("     tooling this scanner doesn't cover; listed for owner sanity-check)")
        for t in unreferenced[:20]:
            print(f"      {t}")
        if len(unreferenced) > 20:
            print(f"      ... ({len(unreferenced) - 20} more)")

    # Check 3: dynamic (f-string) table references this scanner can't resolve.
    print()
    if dynamic_refs:
        total_dynamic = sum(dynamic_refs.values())
        print(f"[3] INFO: {total_dynamic} dynamic (f-string-interpolated) table reference(s) "
              f"in {len(dynamic_refs)} file(s) — not resolvable to a table name")
        print("    (a table only reached this way may appear in check [2]'s 'unreferenced'")
        print("     list even though it IS referenced — verify manually)")
        for f, n in sorted(dynamic_refs.items()):
            print(f"      {f}: {n}")
    else:
        print("[3] INFO: no dynamic (f-string) table references found")

    print()
    print("=" * 70)
    print(f"VERDICT: {'PASS' if exit_code == 0 else 'FAIL'}")
    print("=" * 70)
    return exit_code


if __name__ == "__main__":
    sys.exit(audit())
