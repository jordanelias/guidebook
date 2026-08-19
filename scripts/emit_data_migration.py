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
    tracks single-quoted-string state, including the doubled `''` escape, and
    ALSO tracks parenthesis depth, so a comma inside a nested function call
    in a field (e.g. `datetime('now')`, or a hypothetical `f(1, 2)`) is not
    mistaken for a field separator either.

    Deliberately hand-rolled rather than `csv.reader(..., quotechar="'",
    doublequote=True)`: csv's quote-aware splitting alone would handle the
    `'Smith, J.'` case, but it has no concept of parenthesis nesting, so it
    cannot correctly split a field containing `datetime('now')` — that case
    is in this module's own false-negative test list (see selftest), so
    csv is not a drop-in replacement here. Kept as-is.
    """
    fields = []
    buf = []
    in_str = False
    depth = 0
    i = 0
    n = len(tuple_body)
    while i < n:
        c = tuple_body[i]
        if in_str:
            if c == "'":
                if i + 1 < n and tuple_body[i + 1] == "'":
                    buf.append("''")
                    i += 2
                    continue
                in_str = False
            buf.append(c)
        else:
            if c == "'":
                in_str = True
                buf.append(c)
            elif c == "(":
                depth += 1
                buf.append(c)
            elif c == ")":
                depth = max(0, depth - 1)
                buf.append(c)
            elif c == "," and depth == 0:
                fields.append("".join(buf))
                buf = []
            else:
                buf.append(c)
        i += 1
    fields.append("".join(buf))
    return fields


def _strip_sql_comments(sql: str) -> str:
    """Blank out `--` line comments and `/* ... */` block comments.

    Comment markers found *inside* a single-quoted string are just text, not
    comments (honoured via `in_str`). Replacement is same-length-ish
    whitespace (newlines preserved) rather than deletion, so character
    offsets into the returned string still line up with the statement
    structure for the callers that scan it afterward.

    This exists because `check_range_guards`'s old Form 1 scanned raw file
    text: a documentation comment like `-- an earlier batch wrote tier = 9`
    was indistinguishable from a real assignment and refused a legitimate
    migration (L1 false positive).
    """
    out = []
    in_str = False
    in_line_comment = False
    in_block_comment = False
    i = 0
    n = len(sql)
    while i < n:
        c = sql[i]
        if in_line_comment:
            if c == "\n":
                in_line_comment = False
                out.append(c)
            else:
                out.append(" ")
            i += 1
            continue
        if in_block_comment:
            if c == "*" and i + 1 < n and sql[i + 1] == "/":
                in_block_comment = False
                out.append("  ")
                i += 2
                continue
            out.append("\n" if c == "\n" else " ")
            i += 1
            continue
        if in_str:
            out.append(c)
            if c == "'":
                if i + 1 < n and sql[i + 1] == "'":
                    out.append(sql[i + 1])
                    i += 2
                    continue
                in_str = False
            i += 1
            continue
        if c == "'":
            in_str = True
            out.append(c)
            i += 1
            continue
        if c == "-" and i + 1 < n and sql[i + 1] == "-":
            in_line_comment = True
            out.append("  ")
            i += 2
            continue
        if c == "/" and i + 1 < n and sql[i + 1] == "*":
            in_block_comment = True
            out.append("  ")
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _mask_non_numeric_strings(text: str) -> str:
    """Blank the *contents* of single-quoted string literals in `text`,
    except when the content is itself a bare integer (`'9'`) — SQLite's
    INTEGER-affinity coercion means a quoted digit is a real integer value
    at the storage layer (L2), so it must stay visible to the range regex;
    a narrative string like `'reviewer said tier = 9 is wrong'` must not, or
    its prose gets misread as an assignment (L1 false positive).

    Used only to prepare an UPDATE statement's SET-clause text for the
    direct-assignment regex — never for the positional-INSERT path, which
    never text-searches string contents in the first place.
    """
    out = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c != "'":
            out.append(c)
            i += 1
            continue
        j = i + 1
        content = []
        while j < n:
            if text[j] == "'":
                if j + 1 < n and text[j + 1] == "'":
                    content.append("'")
                    j += 2
                    continue
                break
            content.append(text[j])
            j += 1
        raw = "".join(content)
        if re.fullmatch(r"-?\d+", raw):
            out.append("'" + raw + "'")
        else:
            out.append("'" + ("#" * len(raw)) + "'")
        i = j + 1 if j < n else j
    return "".join(out)


_UPDATE_SET_RE = re.compile(
    r'\bUPDATE\s+(?:"[^"]+"|`[^`]+`|\[[^\]]+\]|\w+)'
    r'(?:\.(?:"[^"]+"|`[^`]+`|\[[^\]]+\]|\w+))?\s+SET\s+',
    re.I,
)


def _iter_update_set_clauses(clean_sql: str):
    """Yield the SET-clause text of each UPDATE statement in `clean_sql`
    (already comment-stripped) — the substring between `SET` and that
    statement's top-level `WHERE` / trailing `;` / end of string.

    "Top-level" skips a `WHERE` or `;` that is inside a nested parenthesised
    expression (e.g. a scalar subquery) or a quoted string. This is the
    fix for the other half of the L1 false-positive class: a comparison in
    a WHERE clause (`... WHERE tier = 0`) is structurally never part of the
    yielded text, so it can never be mistaken for an assignment — no matter
    how the assignment-matching regex is written downstream.
    """
    for m in _UPDATE_SET_RE.finditer(clean_sql):
        i = start = m.end()
        n = len(clean_sql)
        depth = 0
        in_str = False
        while i < n:
            c = clean_sql[i]
            if in_str:
                if c == "'":
                    if i + 1 < n and clean_sql[i + 1] == "'":
                        i += 2
                        continue
                    in_str = False
                i += 1
                continue
            if c == "'":
                in_str = True
                i += 1
                continue
            if c == "(":
                depth += 1
                i += 1
                continue
            if c == ")":
                depth = max(0, depth - 1)
                i += 1
                continue
            if depth == 0 and c == ";":
                break
            if (depth == 0 and clean_sql[i:i + 5].upper() == "WHERE"
                    and (i == 0 or not (clean_sql[i - 1].isalnum() or clean_sql[i - 1] == "_"))
                    and (i + 5 >= n or not (clean_sql[i + 5].isalnum() or clean_sql[i + 5] == "_"))):
                break
            i += 1
        yield clean_sql[start:i]


_INSERT_RE = re.compile(
    r'\bINSERT\s+(?:OR\s+(?:REPLACE|IGNORE|ABORT|FAIL|ROLLBACK)\s+)?INTO\s+'
    r'(?:"[^"]+"|`[^`]+`|\[[^\]]+\]|\w+)'
    r'(?:\.(?:"[^"]+"|`[^`]+`|\[[^\]]+\]|\w+))?'
    r'\s*(?:\(([^()]*)\))?\s*VALUES\s*',
    re.I,
)


def _find_statement_end(sql: str, start: int) -> int:
    """Index of the next top-level (not-inside-a-string) `;` at or after
    `start`, or len(sql) if the statement has none — i.e. it's the last
    statement in the file and was never given a trailing semicolon
    (L2 case: "statement with no trailing `;`")."""
    in_str = False
    i = start
    n = len(sql)
    while i < n:
        c = sql[i]
        if in_str:
            if c == "'":
                if i + 1 < n and sql[i + 1] == "'":
                    i += 2
                    continue
                in_str = False
            i += 1
            continue
        if c == "'":
            in_str = True
            i += 1
            continue
        if c == ";":
            return i
        i += 1
    return n


def _extract_top_level_tuples(text: str) -> list:
    """Find each top-level parenthesised `(...)` tuple in `text` (the
    material after `VALUES`), returning each tuple's inner content with the
    outer parens stripped.

    Quote state is checked BEFORE paren-depth bookkeeping on every
    character, so:
      - a `)` or `(` inside a quoted field (e.g. a source title
        `'ISO 21542 (2021)'`) never perturbs depth — this is what the old
        `re.finditer(r"\\(([^()]*)\\)", ...)` got wrong: it was paren-aware
        but not quote-aware, so it closed the tuple early at the first `)`
        inside the title, truncating it before the `tier` field.
      - a NESTED (non-string) paren, e.g. a function call
        `datetime('now')` inside a tuple, is correctly treated as part of
        the same top-level tuple rather than closing it early.
    """
    tuples = []
    buf = []
    depth = 0
    in_str = False
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if in_str:
            if depth > 0:
                buf.append(c)
            if c == "'":
                if i + 1 < n and text[i + 1] == "'":
                    if depth > 0:
                        buf.append("'")
                    i += 2
                    continue
                in_str = False
            i += 1
            continue
        if c == "'":
            in_str = True
            if depth > 0:
                buf.append(c)
            i += 1
            continue
        if c == "(":
            depth += 1
            if depth > 1:
                buf.append(c)
            i += 1
            continue
        if c == ")":
            depth -= 1
            if depth > 0:
                buf.append(c)
            elif depth == 0:
                tuples.append("".join(buf))
                buf = []
            i += 1
            continue
        if depth > 0:
            buf.append(c)
        i += 1
    return tuples


_NUMERIC_EXPR_RE = re.compile(r"^-?\d+(?:\s*[+\-*/]\s*\d+)*$")


def _eval_int_expr(expr: str):
    """Evaluate a bare arithmetic literal expression (`6+3`, `9`, `10 - 1`)
    to an int, or return None if it isn't one. `expr` is validated against
    `_NUMERIC_EXPR_RE` first — digits, whitespace, and `+-*/` only — before
    it ever reaches `eval`, so this cannot execute arbitrary input (L2 case:
    `tier = 6+3` stores 9 in SQLite, same as a literal `9` would)."""
    expr = expr.strip()
    if not _NUMERIC_EXPR_RE.match(expr):
        return None
    try:
        val = eval(expr, {"__builtins__": {}}, {})  # noqa: S307 — input pre-validated above
    except Exception:
        return None
    if isinstance(val, float) and val.is_integer():
        val = int(val)
    return val if isinstance(val, int) else None


def _coerce_int_field(field: str):
    """Return the SQLite-affinity integer value of one INSERT VALUES field,
    or None if it isn't representable as a plain integer. Handles a bare
    integer literal (`9`) and a quoted integer literal (`'9'`) — SQLite's
    INTEGER column affinity coerces a well-formed integer TEXT literal to an
    integer at storage time (L2 case: `tier='9'`), so both are equivalent
    subjects for this range guard."""
    field = field.strip()
    if re.fullmatch(r"-?\d+", field):
        return int(field)
    m = re.fullmatch(r"'(-?\d+)'", field)
    if m:
        return int(m.group(1))
    return None


def check_range_guards(sql: str) -> list:
    """Return violations of the audit-enforced closed integer ranges.

    Two forms, mirroring check_enum_guards:

    Form 1 — direct assignment, `UPDATE ... SET col = N`. Scoped to the
    SET-clause text of each UPDATE statement (never a WHERE/ON/HAVING
    comparison — see `_iter_update_set_clauses`), over comment-stripped SQL
    (`_strip_sql_comments`) with non-numeric string contents masked out
    (`_mask_non_numeric_strings`). `N` may be a bare integer, a quoted
    integer (`'9'`), or a bare arithmetic literal (`6+3`) — all three are
    genuine SQLite storage values for an INTEGER-affinity column.

    Form 2 — positional INSERT (`INSERT INTO t (a, col, b) VALUES (1, N,
    2)`, `INSERT OR REPLACE`, quoted/schema-qualified table names, multi-row
    VALUES, statements with or without a trailing `;`): unlike
    check_enum_guards' Form 2, this maps the guarded column's actual
    position in the declared column list to the same position in each
    VALUES tuple, rather than scanning the whole statement for suspicious
    literals — an integer column list nearly always contains *other*
    unrelated integers (years, attempt counts, ids), so a same-statement
    heuristic would false-positive constantly. Positional mapping avoids
    that. Tuple boundaries are found quote-aware-then-paren-aware
    (`_extract_top_level_tuples`), so a paren inside a quoted field (a
    source title like `'ISO 21542 (2021)'`) or a nested function call
    (`datetime('now')`) cannot desynchronise field positions.

    KNOWN LIMITATION (not fixed — see module selftest / emit_data_migration
    audit report): an `INSERT INTO t VALUES (...)` with NO column list has
    no positional mapping this script can resolve without a schema/column-
    order reference it doesn't have, so such statements are not scanned by
    Form 2 at all. Not a regression — the pre-fix code had the same gap.

    NULL is always permitted at either form — these ranges bound values that
    are *present*, not presence itself.
    """
    violations = []
    clean = _strip_sql_comments(sql)

    for col, lo, hi, enforced_by in RANGE_GUARDS:
        if col not in clean:
            continue

        # Form 1: direct assignment, scoped to SET clauses only.
        assign_re = re.compile(
            rf"\b{col}\b\s*=\s*(?:'(-?\d+)'|(-?\d+(?:\s*[+\-*/]\s*\d+)*))", re.I)
        for set_clause in _iter_update_set_clauses(clean):
            masked = _mask_non_numeric_strings(set_clause)
            for m in assign_re.finditer(masked):
                if m.group(1) is not None:
                    val = int(m.group(1))
                else:
                    val = _eval_int_expr(m.group(2))
                if val is None:
                    continue
                if val < lo or val > hi:
                    violations.append((col, val, lo, hi, enforced_by))

        # Form 2: positional INSERT.
        for insert_m in _INSERT_RE.finditer(clean):
            collist_raw = insert_m.group(1)
            if collist_raw is None:
                continue  # no column list — see KNOWN LIMITATION above
            collist = [c.strip().strip('"').strip("`").strip("[").strip("]")
                       for c in collist_raw.split(",")]
            collist_lower = [c.lower() for c in collist]
            if col.lower() not in collist_lower:
                continue
            idx = collist_lower.index(col.lower())
            stmt_end = _find_statement_end(clean, insert_m.end())
            values_text = clean[insert_m.end():stmt_end]
            for tuple_body in _extract_top_level_tuples(values_text):
                fields = _split_sql_values(tuple_body)
                if idx >= len(fields):
                    continue
                field = fields[idx].strip()
                if field.upper() == "NULL" or field == "":
                    continue
                val = _coerce_int_field(field)
                if val is None:
                    continue
                if val < lo or val > hi:
                    violations.append((col, val, lo, hi, enforced_by))

    # de-duplicate while preserving order
    seen, out = set(), []
    for v in violations:
        if v[:2] not in seen:
            seen.add(v[:2])
            out.append(v)
    return out


def selftest():
    """Mutation tests for check_range_guards. A guard with no selftest stops
    guarding on its next refactor — this file had none before this fix.

    Cases are grouped: L1 false positives (legitimate SQL that must now be
    ACCEPTED — zero violations), L2 false negatives (bad data that must now
    be REFUSED — at least one violation), and control cases (genuine valid
    writes that must stay accepted, so the fix isn't overcorrected)."""
    accept_cases = [
        # --- L1 false positives: must be accepted (no violations) ---
        ("comment merely documenting a bad historical value",
         "-- Compensating migration: an earlier batch wrote tier = 9 in error.\n"
         "DELETE FROM evidence_sources WHERE tier = 0;"),
        ("WHERE-clause comparison is not an assignment",
         "DELETE FROM evidence_sources WHERE tier = 0;"),
        ("tier=9 text inside an unrelated string literal value",
         "UPDATE gaps SET note = 'reviewer said tier = 9 is wrong' WHERE id=1;"),
        ("SET on a differently-named column plus a WHERE comparison on the guarded one",
         "UPDATE weighting_profile SET tier_weights = '{}' WHERE tier = 0;"),
        # --- controls: genuine valid writes must still be accepted ---
        ("genuine in-range assignment",
         "UPDATE evidence_sources SET tier = 3 WHERE id=1;"),
        ("genuine NULL assignment",
         "UPDATE evidence_sources SET tier = NULL WHERE id=1;"),
        ("in-range positional INSERT with a parenthesised year in an unrelated field",
         "INSERT INTO evidence_sources (ref_id, title, tier) "
         "VALUES ('REF-1', 'ISO 21542 (2021)', 3);"),
        ("known limitation: no column list has no positional mapping to check",
         "INSERT INTO evidence_sources VALUES ('R', 9);"),
    ]
    refuse_cases = [
        # --- L2 false negatives: must be refused (at least one violation) ---
        ("quoted-digit assignment bypasses affinity coercion",
         "UPDATE evidence_sources SET tier='9' WHERE id=1;"),
        ("bare arithmetic literal evaluates out of range",
         "UPDATE evidence_sources SET tier = 6+3 WHERE id=1;"),
        ("INSERT OR REPLACE was not matched by the old INSERT\\s+INTO regex",
         "INSERT OR REPLACE INTO evidence_sources (title, tier) VALUES ('R', 9);"),
        ("semicolon inside a string literal ends the tuple regex early",
         "INSERT INTO evidence_sources (title, tier) VALUES ('a;b', 9);"),
        ("nested function-call parens in a VALUES tuple confuse naive paren matching",
         "INSERT INTO evidence_sources (ref_id, tier, created_at) "
         "VALUES ('R', 9, datetime('now'));"),
        ("double-quoted table name was not matched by \\w+",
         "INSERT INTO \"evidence_sources\" (title, tier) VALUES ('R', 9);"),
        ("schema-qualified table name was not matched by \\w+",
         "INSERT INTO main.evidence_sources (title, tier) VALUES ('R', 9);"),
        ("statement with no trailing semicolon (end of file)",
         "INSERT INTO evidence_sources (title, tier) VALUES ('R', 9)"),
        ("paren inside a quoted field closes the tuple regex before the tier field "
         "(coordinator-reported: parenthesised years/editions are the NORMAL case "
         "for evidence_sources titles, not an edge case)",
         "INSERT INTO evidence_sources (ref_id, title, tier) "
         "VALUES ('REF-1', 'ISO 21542 (2021)', 7);"),
    ]

    fails = []
    for name, sql in accept_cases:
        got = check_range_guards(sql)
        if got:
            fails.append(f"[accept] {name}: expected no violations, got {got}")
    for name, sql in refuse_cases:
        got = check_range_guards(sql)
        if not got:
            fails.append(f"[refuse] {name}: expected a violation, got none")

    n = len(accept_cases) + len(refuse_cases)
    if fails:
        print("emit_data_migration selftest FAILURES:", file=sys.stderr)
        for f in fails:
            print("  -", f, file=sys.stderr)
        print(f"\nRESULTS: {n - len(fails)}/{n}", file=sys.stderr)
        return 1
    print(f"RESULTS: {n}/{n} selftest cases pass "
          f"({len(accept_cases)} accept cases incl. L1 false-positive regressions, "
          f"{len(refuse_cases)} refuse cases incl. L2 false-negative fixes)")
    return 0


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
    p.add_argument("--session", help="Session filename, e.g. session_2026-05-11g-citation-mining.md")
    p.add_argument("--summary", help="One-line description for the frontmatter header")
    p.add_argument("--input", help="Read SQL from this path (default: stdin)")
    p.add_argument("--output-dir", default=str(MIGRATIONS_DIR))
    p.add_argument("--no-transaction", action="store_true",
                   help="Accepted no-op. Bodies are never wrapped: the migration "
                        "runner owns the transaction boundary (DR-2026-08-19 F5)")
    p.add_argument("--force-timestamp", help="Override timestamp (advanced; for tests only)")
    p.add_argument("--selftest", action="store_true",
                   help="Run the range-guard mutation tests and exit (no --session/--summary needed)")
    args = p.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if not args.session or not args.summary:
        p.error("the following arguments are required: --session, --summary")

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
    # The runner owns the transaction boundary (DR-2026-08-19 §12.0, F5). A
    # wrapper here made executescript commit the body from inside the file, so
    # the body and its data_migrations ledger row committed separately and a
    # "rolled back" failure discarded only the ledger row. --no-transaction is
    # kept as an accepted no-op so existing invocations do not break.
    body = sql
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(header + body)
    print(str(out_path))


if __name__ == "__main__":
    main()
