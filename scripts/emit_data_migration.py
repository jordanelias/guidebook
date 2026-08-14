#!/usr/bin/env python3
"""
scripts/emit_data_migration.py — create a properly-named data-migration file.

Per GAP-290 resolution. The migration system (scripts/migrate_db.py) requires
data migrations to be named:

    scripts/migrations/data_{YYYYMMDDHHMMSS}_{session-slug}.sql

This script generates one for you. Two concurrent sessions will produce files
with different timestamps and can both land cleanly on `main`.

Usage:

    # Pipe SQL from stdin
    cat my_changes.sql | python3 scripts/emit_data_migration.py \\
        --session session_2026-05-11g-citation-mining.md \\
        --summary "add 14 evidence_sources from REF-00710 backward mining"

    # Read from a file
    python3 scripts/emit_data_migration.py \\
        --session session_2026-05-11g-citation-mining.md \\
        --summary "cleanup orphan source_slug_links rows" \\
        --input cleanup.sql

    # Output path printed to stdout; the file is committed by you afterward.

The SQL body is wrapped in a single transaction (BEGIN ... COMMIT) so partial
failure rolls back. A frontmatter header with metadata is prepended.

Validation:
  - Refuses if the resulting filename would already exist (timestamp collision —
    rare, sleep 1s and retry)
  - Refuses if the SQL is empty
  - Warns if the SQL contains DROP / TRUNCATE / DELETE without WHERE
"""

import argparse
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parent / "migrations"

RISKY_PATTERNS = [
    (re.compile(r"\bDROP\s+TABLE\b", re.I), "DROP TABLE"),
    (re.compile(r"\bTRUNCATE\b", re.I), "TRUNCATE"),
    (re.compile(r"\bDELETE\s+FROM\s+\w+\s*;", re.I), "DELETE without WHERE clause"),
    (re.compile(r"\bUPDATE\s+\w+\s+SET\s+[^;]+;", re.I), "UPDATE — check WHERE clause"),
]

# Closed vocabularies that are enforced by an AUDIT rather than by a table CHECK, so SQLite
# accepts a bad value silently and only test_db_integrity.py catches it — one integrity check
# down, discoverable solely by diffing against the pre-batch DB.
#
# WHY THIS EXISTS: the same wrong value ('NOT-APPLICABLE' in doi_resolution_outcome, whose
# vocabulary is RESOLVED/NO-MATCH/REVERTED) was written in two consecutive research batches on
# 2026-07-25. After the first, the lesson was recorded in prose — a session file, a PR body and
# an attestation deviation — and prose did not prevent the repeat a few hours later. The fix
# belongs at the point of writing, not in a document someone has to remember to re-read.
#
# This is a BLOCKING check, not a warning: warnings are what the repeat slipped past.
ENUM_GUARDS = [
    ("doi_resolution_outcome", {"RESOLVED", "NO-MATCH", "REVERTED"},
     "test_db_integrity.py [B03]"),
    ("url_resolution_outcome", {"MATCHED", "PARTIAL", "NO-MATCH", "DEAD-LINK", "DEAD-DNS",
                                "WAYBACK-MATCH", "WAYBACK-PARTIAL", "URL-NO-MATCH",
                                "RESOLVED", "DEAD", "RESOLVED-PARTIAL"},
     "test_db_integrity.py [B04]"),
]

# Closed *integer ranges* enforced by an AUDIT rather than a table CHECK —
# same gap as ENUM_GUARDS above, but ENUM_GUARDS structurally cannot cover
# them: it scans for `'QUOTED VALUE'` literals, and an out-of-range integer
# literal (e.g. `tier = 7`) is unquoted, so it never matches ENUM_GUARDS' regex
# at all. evidence_sources.tier is the T1-T6 (+ Co-1/Co-2 co-primary, mapped
# onto tier 1/2 — see schemas/evidence_source.py:129-131, NOT separate integer
# values) anchoring tier the whole evidence-strength doctrine
# (governance/tier-system.md) runs on, and had zero coverage of any kind before
# this guard: no CHECK constraint, no ENUM_GUARDS entry, no B-series vocabulary
# check. NULL is permitted (schemas/evidence_source.py:42); this guards values
# that are *present*, not presence itself. 1-6 is the already-ratified boundary
# (schemas/evidence_source.py:85) — this does not invent, extend, or
# reinterpret the tier vocabulary.
#
# Shape: (column, min, max, enforced_by). `column` is matched bare (like
# ENUM_GUARDS), not table-qualified: `case_study_outcomes.tier` is a distinct
# column with its own, stricter DB-level CHECK (1-3, see
# scripts/migrations/057_baseline_2026-08-12.sql:918) that this guard's wider
# 1-6 band cannot false-positive against, since 1-3 is a strict subset of 1-6.
#
# BLOCKING, same as ENUM_GUARDS — not a warning.
RANGE_GUARDS = [
    ("tier", 1, 6, "test_db_integrity.py [B10/B11]"),
]


def check_enum_guards(sql: str) -> list:
    """Return violations of the audit-enforced closed vocabularies.

    Scans for `'VALUE'` literals appearing near a guarded column name — both the
    `SET col='X'` form and the positional-INSERT form where the column appears in a column
    list. Deliberately conservative: it reports a value only when that value is not in the
    vocabulary AND is not obviously a placeholder (NULL / bind parameter).
    """
    violations = []
    for col, allowed, enforced_by in ENUM_GUARDS:
        if col not in sql:
            continue
        # Form 1: explicit assignment — col = 'VALUE'
        for m in re.finditer(rf"{col}\s*=\s*'([^']*)'", sql, re.I):
            if m.group(1) not in allowed:
                violations.append((col, m.group(1), allowed, enforced_by))
        # Form 2: the column is named in an INSERT column list. We cannot map positions
        # reliably, so flag any literal in the statement that looks like a member of a
        # RESOLUTION vocabulary but is not in this one — catches NOT-APPLICABLE, N/A, etc.
        if re.search(rf"\b{col}\b", sql, re.I):
            suspicious = {"NOT-APPLICABLE", "NOT APPLICABLE", "N/A", "NA", "NONE",
                          "UNKNOWN", "PENDING", "NOT-CHECKED", "UNRESOLVED"}
            for m in re.finditer(r"'([A-Z][A-Z /-]{2,24})'", sql):
                v = m.group(1).strip()
                if v in suspicious and v not in allowed:
                    violations.append((col, v, allowed, enforced_by))
    # de-duplicate while preserving order
    seen, out = set(), []
    for v in violations:
        if v[:2] not in seen:
            seen.add(v[:2])
            out.append(v)
    return out


def _split_sql_values(tuple_body: str) -> list:
    """Split a `VALUES (a, b, c)` tuple body on top-level commas.

    A plain `.split(',')` breaks on a comma inside a quoted string field
    (e.g. an authors field `'Smith, J.'`). This is a small state machine that
    tracks single-quoted-string state, including the doubled `''` escape, so
    such a comma is not mistaken for a field separator. It assumes no nested
    parentheses inside a field, which holds for the plain literal VALUES
    tuples this repo's migrations write.
    """
    fields = []
    buf = []
    in_str = False
    i = 0
    while i < len(tuple_body):
        c = tuple_body[i]
        if in_str:
            if c == "'":
                if i + 1 < len(tuple_body) and tuple_body[i + 1] == "'":
                    buf.append("''")
                    i += 2
                    continue
                in_str = False
            buf.append(c)
        else:
            if c == "'":
                in_str = True
                buf.append(c)
            elif c == ",":
                fields.append("".join(buf))
                buf = []
            else:
                buf.append(c)
        i += 1
    fields.append("".join(buf))
    return fields


def check_range_guards(sql: str) -> list:
    """Return violations of the audit-enforced closed integer ranges.

    Two forms, mirroring check_enum_guards:

    Form 1 — direct assignment (`UPDATE ... SET col = N`, or any bare
    `col = N`): a simple regex on the literal integer.

    Form 2 — positional INSERT (`INSERT INTO t (a, col, b) VALUES (1, N, 2)`):
    unlike check_enum_guards' Form 2, this maps the guarded column's actual
    position in the declared column list to the same position in each VALUES
    tuple, rather than scanning the whole statement for suspicious literals —
    an integer column list nearly always contains *other* unrelated integers
    (years, attempt counts, ids), so a same-statement heuristic would
    false-positive constantly. Positional mapping avoids that.

    NULL is always permitted at either form — these ranges bound values that
    are *present*, not presence itself.
    """
    violations = []
    for col, lo, hi, enforced_by in RANGE_GUARDS:
        if col not in sql:
            continue

        # Form 1: direct assignment.
        for m in re.finditer(rf"\b{col}\b\s*=\s*(-?\d+)\b", sql, re.I):
            val = int(m.group(1))
            if val < lo or val > hi:
                violations.append((col, val, lo, hi, enforced_by))

        # Form 2: positional INSERT.
        for insert_m in re.finditer(
                r"INSERT\s+INTO\s+\w+\s*\(([^)]*)\)\s*VALUES\s*(.+?);",
                sql, re.I | re.S):
            collist = [c.strip().strip('"').strip("`")
                       for c in insert_m.group(1).split(",")]
            collist_lower = [c.lower() for c in collist]
            if col.lower() not in collist_lower:
                continue
            idx = collist_lower.index(col.lower())
            for tuple_m in re.finditer(r"\(([^()]*)\)", insert_m.group(2)):
                fields = _split_sql_values(tuple_m.group(1))
                if idx >= len(fields):
                    continue
                field = fields[idx].strip()
                if field.upper() == "NULL" or field == "":
                    continue
                if re.fullmatch(r"-?\d+", field):
                    val = int(field)
                    if val < lo or val > hi:
                        violations.append((col, val, lo, hi, enforced_by))

    # de-duplicate while preserving order
    seen, out = set(), []
    for v in violations:
        if v[:2] not in seen:
            seen.add(v[:2])
            out.append(v)
    return out


def slugify_session(session: str) -> str:
    """Convert 'session_2026-05-11g-citation-mining.md' → '2026-05-11g-citation-mining'."""
    s = session
    if s.endswith(".md"):
        s = s[:-3]
    if s.startswith("session_"):
        s = s[len("session_"):]
    # Lowercase, alphanumeric and dash only
    s = re.sub(r"[^a-z0-9-]", "-", s.lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument("--session", required=True, help="Session filename, e.g. session_2026-05-11g-citation-mining.md")
    p.add_argument("--summary", required=True, help="One-line description for the frontmatter header")
    p.add_argument("--input", help="Read SQL from this path (default: stdin)")
    p.add_argument("--output-dir", default=str(MIGRATIONS_DIR))
    p.add_argument("--no-transaction", action="store_true",
                   help="Skip wrapping body in BEGIN/COMMIT (use only if the SQL contains its own transactions)")
    p.add_argument("--force-timestamp", help="Override timestamp (advanced; for tests only)")
    args = p.parse_args()

    if args.input:
        with open(args.input) as f:
            sql = f.read()
    else:
        sql = sys.stdin.read()

    sql = sql.strip()
    if not sql:
        print("ERROR: empty SQL body", file=sys.stderr)
        sys.exit(1)

    # Risky-pattern warnings
    warnings = []
    for pat, label in RISKY_PATTERNS:
        if pat.search(sql):
            warnings.append(label)
    if warnings:
        for w in warnings:
            print(f"  WARNING: detected risky pattern — {w}", file=sys.stderr)

    # Audit-enforced enum vocabularies — BLOCKING (see ENUM_GUARDS rationale).
    enum_violations = check_enum_guards(sql)
    if enum_violations:
        print("  ERROR: value outside an audit-enforced vocabulary — migration NOT emitted.",
              file=sys.stderr)
        for col, val, allowed, enforced_by in enum_violations:
            print(f"    {col}: '{val}' is not permitted. Allowed: "
                  f"{', '.join(sorted(allowed))}", file=sys.stderr)
            print(f"      Enforced by {enforced_by}. SQLite has no CHECK on this column, so a "
                  f"bad value applies silently and only shows up as a lost integrity check.",
                  file=sys.stderr)
            print(f"      If the value is genuinely inapplicable (e.g. a source with no DOI), "
                  f"use NULL — not a sentinel string.", file=sys.stderr)
        sys.exit(1)

    # Audit-enforced integer ranges — BLOCKING (see RANGE_GUARDS rationale).
    range_violations = check_range_guards(sql)
    if range_violations:
        print("  ERROR: value outside an audit-enforced range — migration NOT emitted.",
              file=sys.stderr)
        for col, val, lo, hi, enforced_by in range_violations:
            print(f"    {col}: {val} is not permitted. Allowed range: {lo}-{hi} inclusive.",
                  file=sys.stderr)
            print(f"      Enforced by {enforced_by}. SQLite has no CHECK on this column, so a "
                  f"bad value applies silently and only shows up as a lost integrity check.",
                  file=sys.stderr)
            print(f"      If the value is genuinely unknown, use NULL — not a placeholder "
                  f"integer.", file=sys.stderr)
        sys.exit(1)

    if args.force_timestamp:
        ts = args.force_timestamp
    else:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    slug = slugify_session(args.session)
    filename = f"data_{ts}_{slug}.sql"
    out_path = Path(args.output_dir) / filename

    # Retry on collision (extremely rare — same session emitting two migrations in same second)
    retries = 0
    while out_path.exists() and retries < 5:
        time.sleep(1)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        filename = f"data_{ts}_{slug}.sql"
        out_path = Path(args.output_dir) / filename
        retries += 1
    if out_path.exists():
        print(f"ERROR: filename collision unresolvable after {retries} retries: {out_path}", file=sys.stderr)
        sys.exit(1)

    iso = datetime.now(timezone.utc).isoformat(timespec='seconds')
    header = f"""-- {filename}
-- Data migration generated by scripts/emit_data_migration.py
-- Session:    {args.session}
-- Generated:  {iso}
-- Summary:    {args.summary}
--
-- This file is forward-only and immutable once committed. If a correction is
-- needed, emit a NEW data migration that compensates — do not edit this file.

"""
    body = sql if args.no_transaction else f"BEGIN TRANSACTION;\n\n{sql}\n\nCOMMIT;\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(header + body)
    print(str(out_path))


if __name__ == "__main__":
    main()
