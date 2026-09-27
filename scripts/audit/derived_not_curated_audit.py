#!/usr/bin/env python3
"""
scripts/audit/derived_not_curated_audit.py — CLAUDE.md rule 8, mechanised.

THE RULE: derive it, or name who judged it. Never curate a fact the machine can compute.

WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS. A curated list and the thing it
describes drift, and only the list is ever read. Every instance found on 2026-09-13 failed
in the SAFE-LOOKING direction, which is why none was noticed:

  * `dbcore.WRITABLE_TABLES` — a hand list of the tables a session may write. Blind eight
    times. A `gap_mining` row written through the sanctioned CLI was captured as nothing
    and the session was told "no delta — nothing to emit".
  * `db.py --verification-method` — an argparse `choices=` list missing `direct-render`
    for as long as that value had existed, so the CLI REFUSED a value the schema admits.
  * `PRE_075_UNGRADED_IDS` — a frozen id list that outlived the rows it froze.
  * `governance/check-registry.yaml`'s "N today" counts — every one measured stale.

None of those made a wrong claim reach the book directly. Each made a TRUE thing
unreachable, or a checkable thing uncheckable, which is how a corpus quietly stops being
verifiable.

WHAT THIS CHECKS, and why only this class for now. Rule 8 is general and most of it is
judgement, which a script cannot police. ONE class of violation is mechanically decidable:
an argparse `choices=` literal whose values are exactly a live column's CHECK vocabulary.
That is a second home with a first home sitting next to it, and the fix is always the same
(`dbcore.schema_choices(table, column)`). The other known violations named in rule 8 —
`--ref-id` and `--tier` asking for derivable values, the curated `MODEL_TABLE_MAP`, the
registry's counts — need judgement about what the single home should BE, so they are
listed in the rule for a reader rather than asserted here.

A SECOND MECHANICALLY DECIDABLE CLASS, added 2026-09-17: A WRITER THAT NAMES A COLUMN
THE LIVE SCHEMA DOES NOT HAVE. A row dict spelling its own audit columns as string
literals is the same defect as a curated vocabulary -- a second home for the column's
name, with the first home (the schema) sitting right there.

  Migration 085 renamed `search_executions.session` -> `created_by_session` and
  `.executed_at` -> `created_at`. Its caller sweep was EMPIRICAL: it ran the whole check
  battery against a rebuilt DB, which is a better sweep than grep and still could not see
  this, because NO CHECK WRITES A SEARCH EXECUTION. The battery stayed green, the selftest
  stayed green, and `db.py log-search` -- the FIRST command of every research batch, and
  the only way R8 ("log EVERY query verbatim before screening") can be met -- raised
  `table search_executions has no column named session` on its next call. The wrong thing
  that reaches the BOOK is a batch whose searches cannot be recorded: research that is
  invalid by the research contract's own terms, discovered only after the retrieval work
  is spent. Every writer that reached for `dbcore.stamp_for` instead survived the rename
  untouched, because stamp_for reads the live schema.

WHAT THIS SECOND CLASS DOES NOT CATCH, stated so a green result is not over-read. It sees
a row built as a DICT LITERAL inside the same function as its INSERT. It does NOT see a
row built by `dict(data)` and then amended by subscript (`row["session"] = session`), nor
one assembled in one function and inserted in another. Both shapes existed in this same
rename: `insert_search_candidate` broke by the first and `add-audit-run` by the second,
and neither would have been flagged here. They were found by RUNNING the writers against
a scratch DB, which remains the only complete sweep. Treat this class as a tripwire for
the commonest shape, never as proof the callers are swept.

A CHECK THAT GREPS ITS OWN REPOSITORY, deliberately. The alternative is importing db.py
and inspecting the parser, which would run module-level code and couple this gate to the
writer it polices — the thing dbcore's own docstring says a gate must not do.

THREE MORE CLASSES, added 2026-09-27 (RC2, DR-2026-09-26-recurring-defect-shapes-remediation.md
section 3). The first pass above sees only a bracketed `choices=[...]` literal; the
detector was blind to every OTHER shape the same shortcut takes. `grep -c 'choices='
scripts/db.py` against `grep -c 'choices=dbcore\.\(schema_choices\|check_values\)'
scripts/db.py` (CLAUDE.md rule 8) names the gap this closes.

  * CLASS 3 — a module-level string collection (frozenset/set/list/tuple literal) in a
    writer module that EQUALS a live CHECK IN-list. FAILS. A collection that is a proper
    SUBSET of a live vocabulary is printed as SUBSET and never fails — three exist today
    on purpose (`_VALID_DIRECTIONS`, `_ROW_ONLY_RELATIONS`,
    `assess_cell.VALUE_SUPPLYING_ROLES`), each a deliberate restriction, not a drifted
    copy. Neither list is quoted here as a count; the class computes both live, each run.
  * CLASS 4 — a numeric `choices=` (a `range(...)` or an integer literal list) that
    mirrors a `BETWEEN` CHECK, read through `dbcore.check_expression` rather than
    `check_values` (which cannot parse a range expression). `--target-tier
    choices=range(1, 7)` mirroring `target_tier BETWEEN 1 AND 6` is the specimen.
  * CLASS 5 — a DDL comment enumerating three or more pipe-separated values on a column
    with NO CHECK at all. REPORTED, never failed — the remedy is a judgement call (does
    this column get a CHECK, and is its vocabulary doctrinal), not a mechanical rewrite.
    `search_executions.engine` is the specimen: its vocabulary lives only in a comment,
    and live rows already hold values outside it.

EXAMINED counts `choices=` literals, module-level collections, and DDL-comment
enumerations inspected — not files read.
"""
import ast
import os
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = os.environ.get("GUIDEBOOK_DB_PATH", str(ROOT / "data" / "guidebook.db"))

sys.path.insert(0, str(ROOT / "scripts"))
import dbcore                                                        # noqa: E402

#: Files whose argparse parsers are in scope. The writers; a report script that offers a
#: fixed menu of its own output formats is not restating a schema vocabulary.
SCANNED = ("scripts/db.py",)

#: Class 3's scan set — the three writer modules the DR names (section 3.1). Wider than
#: SCANNED because a module-level collection, unlike an argparse choices= literal, can
#: live in any of them.
MODULE_SCAN = ("scripts/db.py", "scripts/dbcore.py", "scripts/assess/assess_cell.py")

_RANGE_CALL = re.compile(r"choices=range\((-?\d+),\s*(-?\d+)\)")
_INT_LIST = re.compile(r"choices=\[([^\]]*)\]")
#: Class 5: a column definition line ending in a comment holding >=3 pipe-separated
#: tokens. The column name is the first identifier on the line (quoted or bare).
_COMMENT_ENUM_LINE = re.compile(
    r'^\s*"?(\w+)"?\s+\w+.*--\s*([^\s|][^|]*(?:\|[^|]+){2,})\s*$')

#: Trees scanned for the column-name class. Wider than SCANNED because any writer can
#: hard-code a column name, and AST parsing is cheap. Derived by walk, never listed.
WRITER_ROOTS = ("scripts", "tools")

_INSERT_TARGET = re.compile(
    r'(?:INSERT|REPLACE)\s+(?:OR\s+\w+\s+)?INTO\s+"?(\w+)"?|UPDATE\s+"?(\w+)"?\s+SET',
    re.I)

_CHOICES = re.compile(r"choices=\[([^\]]*)\]")
_LITERAL = re.compile(r'"([^"]*)"|\'([^\']*)\'')


def check_vocabularies(con):
    """Every column CHECK vocabulary in the live schema, keyed by its value set."""
    out = {}
    for (table,) in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"):
        for col in con.execute('PRAGMA table_info("%s")' % table):
            vals = dbcore.check_values(con, table, col[1])
            if vals:
                out.setdefault(frozenset(vals), []).append((table, col[1]))
    return out


def _row_vars(fn):
    """Variables this function actually feeds to an INSERT, by dataflow, not by shape.

    The idiom every writer here uses is `conn.execute(f"INSERT INTO t ({cols}) ...",
    list(row.values()))`. The second argument NAMES the row variable, which is the only
    reliable way to tell a row from a result payload: an `_emit({...})` dict echoing the
    row shares most of its keys with the table and is not a row. A first cut of this check
    judged any dict matching the table on a majority of keys and produced fifteen findings,
    every one of them a result dict and not one a real defect -- a check red by
    construction, which CLAUDE.md rule 6 says teaches its reader to ignore it.
    """
    for node in ast.walk(fn):
        if not isinstance(node, ast.Call):
            continue
        for arg in node.args:
            inner = arg
            if (isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name)
                    and arg.func.id == "list" and arg.args):
                inner = arg.args[0]
            if (isinstance(inner, ast.Call) and isinstance(inner.func, ast.Attribute)
                    and inner.func.attr == "values"
                    and isinstance(inner.func.value, ast.Name)):
                yield inner.func.value.id


def _keys_of(fn, var):
    """Every string key given to `var`: dict-literal keys and subscript stores alike.

    Both shapes broke in the migration-085 rename -- `log_search` by a dict literal and
    `insert_search_candidate` by `row["session"] = session` -- so reading only one of them
    would have caught only one of them.
    """
    keys, lineno = set(), None
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if (isinstance(t, ast.Name) and t.id == var
                        and isinstance(node.value, ast.Dict)):
                    for k in node.value.keys:
                        if isinstance(k, ast.Constant) and isinstance(k.value, str):
                            keys.add(k.value)
                            lineno = lineno or node.lineno
                if (isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name)
                        and t.value.id == var
                        and isinstance(t.slice, ast.Constant)
                        and isinstance(t.slice.value, str)):
                    keys.add(t.slice.value)
                    lineno = lineno or node.lineno
    return keys, lineno


def scan_writer_columns(con):
    """Flag a writer naming a column the table it INSERTs into does not have.

    Scoped to the function, so the table is READ from the INSERT rather than guessed, and
    scoped to the variable the INSERT is actually given, so a result dict is never judged
    as a row.
    """
    cols = {}
    for (table,) in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"):
        cols[table] = {c[1] for c in con.execute('PRAGMA table_info("%s")' % table)}

    examined, violations = 0, []
    for root in WRITER_ROOTS:
        for path in sorted((ROOT / root).rglob("*.py")):
            rel = path.relative_to(ROOT).as_posix()
            if "migrations" in rel or "_archived" in rel:
                continue
            src = path.read_text(encoding="utf-8", errors="replace")
            try:
                tree = ast.parse(src)
            except SyntaxError:
                continue
            for fn in ast.walk(tree):
                if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                seg = ast.get_source_segment(src, fn) or ""
                targets = {a or b for a, b in _INSERT_TARGET.findall(seg)}
                targets = {t for t in targets if t in cols}
                if not targets:
                    continue
                known = set().union(*(cols[t] for t in targets))
                for var in set(_row_vars(fn)):
                    keys, lineno = _keys_of(fn, var)
                    if not keys:
                        continue
                    examined += 1
                    stray = sorted(k for k in keys if k not in known)
                    if stray:
                        best = max(targets,
                                   key=lambda t: len(keys & cols[t]))
                        violations.append(
                            "%s:%d builds the row `%s` with column(s) %s that %s does "
                            "not have — the schema is the one home of a column's name "
                            "(rule 8); derive the audit columns with "
                            "dbcore.stamp_for(conn, %r, session)"
                            % (rel, lineno or fn.lineno, var, ", ".join(stray),
                               best, best))
    return examined, violations


def _literal_collection(node):
    """The set of string constants in a module-level collection literal, or None.

    Handles `frozenset({...})` / `frozenset((...))` / `frozenset([...])` calls and bare
    Set/List/Tuple literals — the shapes `_VALID_DIRECTIONS` (frozenset), the retired
    `_ROW_ONLY_RELATIONS` (tuple) and `assess_cell.VALUE_SUPPLYING_ROLES` (tuple) all use.
    Returns None for anything that is not entirely string constants (so an int range or a
    mixed list is never mistaken for a vocabulary mirror — that is Class 4's job).
    """
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "frozenset" and node.args
            and isinstance(node.args[0], (ast.Set, ast.List, ast.Tuple))):
        node = node.args[0]
    if not isinstance(node, (ast.Set, ast.List, ast.Tuple)):
        return None
    out = set()
    for elt in node.elts:
        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
            out.add(elt.value)
        else:
            return None
    return out if out else None


def scan_module_collections(con, vocab):
    """Class 3: a module-level string collection that equals or is a subset of a live
    CHECK vocabulary. Equality FAILs; a proper subset is reported as SUBSET only."""
    examined, violations, subsets = 0, [], []
    for rel in MODULE_SCAN:
        path = ROOT / rel
        if not path.exists():
            continue
        src = path.read_text(encoding="utf-8", errors="replace")
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        for node in tree.body:          # module level only — a local variable is scoped
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, ast.Name):
                continue
            lits = _literal_collection(node.value)
            if lits is None:
                continue
            examined += 1
            frozen = frozenset(lits)
            owner = vocab.get(frozen)
            if owner:
                table, column = owner[0]
                violations.append(
                    "%s:%d `%s` EQUALS the CHECK on %s.%s — replace with "
                    "dbcore.check_values(conn, %r, %r) or dbcore.schema_choices(%r, %r)"
                    % (rel, node.lineno, target.id, table, column,
                       table, column, table, column))
                continue
            for live, owners in vocab.items():
                if lits and lits < live:          # proper subset
                    t, c = owners[0]
                    subsets.append(
                        "%s:%d `%s` is a SUBSET of the CHECK on %s.%s (%d of %d values) "
                        "— reported only; a deliberate restriction is not a violation"
                        % (rel, node.lineno, target.id, t, c, len(lits), len(live)))
                    break
    return examined, violations, subsets


_FLAG_NAME = re.compile(r'"(--[\w-]+)"')


def _flag_on_line(src: str, pos: int):
    """The first `"--flag-name"` on the physical line containing `pos`, or None.

    Required to accept a Class 4 match: `add-supersession-check --tier
    choices=[1,2,3,4,5,6]` numerically coincides with `search_executions.target_tier`'s
    BETWEEN 1 AND 6, and the two are UNRELATED — the flag writes
    `supersession_check.anchor_evidence_type`, which declares no CHECK at all, and the
    code's own comment explains at length why borrowing a foreign column's CHECK there
    would be silently wrong. Class 1's string-vocabulary match has the same ambiguity and
    resolves it with a caveat rather than a name check because an exact string-set
    coincidence is rare; a 1..6 or 1..N integer span is not, so Class 4 requires the flag
    name to equal the mirrored column's name before it reports anything.
    """
    line_start = src.rfind("\n", 0, pos) + 1
    line_end = src.find("\n", pos)
    line = src[line_start:(line_end if line_end != -1 else len(src))]
    m = _FLAG_NAME.search(line)
    return m.group(1)[2:].replace("-", "_") if m else None


def _report_numeric_mirror(rel, src, m, span, display, between):
    """One Class-4 violation string, or None — shared by both the range() and int-list
    finditer loops below, which differ only in how `span`/`display` are derived."""
    owner = next((o for o in between.get(span, [])
                 if o[1] == _flag_on_line(src, m.start())), None)
    if not owner:
        return None
    line = src[:m.start()].count("\n") + 1
    table, column = owner
    return ("%s:%d choices=%s mirrors %s.%s's BETWEEN %d AND %d — read it with "
           "dbcore.schema_range(%r, %r) instead"
           % (rel, line, display, table, column, span[0], span[1], table, column))


def scan_numeric_mirrors(con):
    """Class 4: a numeric choices= (range(...) or an int literal list) that mirrors a
    BETWEEN CHECK, read through dbcore.schema_range (check_values cannot parse a range
    expression). Only reported when the flag's own name equals the mirrored column's
    name — see `_flag_on_line`."""
    between = {}    # (lo, hi) -> [(table, column), ...], derived from every live CHECK
    for (table,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        for col in con.execute('PRAGMA table_info("%s")' % table):
            span = dbcore.schema_range(table, col[1])
            if span:
                between.setdefault((span.start, span.stop - 1), []).append((table, col[1]))

    examined, violations = 0, []
    for rel in SCANNED:
        path = ROOT / rel
        if not path.exists():
            continue
        src = path.read_text(encoding="utf-8", errors="replace")
        for m in _RANGE_CALL.finditer(src):
            lo, hi_exclusive = int(m.group(1)), int(m.group(2))
            span = (lo, hi_exclusive - 1)     # range(a, b) is a..b-1 inclusive
            examined += 1
            v = _report_numeric_mirror(rel, src, m, span, "range(%d, %d)" % (lo, hi_exclusive),
                                       between)
            if v:
                violations.append(v)
        for m in _INT_LIST.finditer(src):
            lits = _LITERAL.findall(m.group(1))
            if lits:
                continue    # a string list, already Class 1's subject
            try:
                nums = sorted(int(x.strip()) for x in m.group(1).split(",") if x.strip())
            except ValueError:
                continue
            if not nums or nums != list(range(nums[0], nums[-1] + 1)):
                continue    # not contiguous — not a range mirror
            examined += 1
            v = _report_numeric_mirror(rel, src, m, (nums[0], nums[-1]), str(nums), between)
            if v:
                violations.append(v)
    return examined, violations


def scan_comment_vocabularies(con):
    """Class 5: a DDL comment enumerating >=3 pipe-separated values on a column with no
    CHECK at all. Reported, never failed — the remedy needs judgement."""
    examined, reported = 0, []
    for (table, sql) in con.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL"):
        for line in sql.splitlines():
            m = _COMMENT_ENUM_LINE.match(line)
            if not m:
                continue
            column, tokens = m.group(1), m.group(2)
            examined += 1
            if dbcore.check_values(con, table, column):
                continue    # already has a real, parseable CHECK
            reported.append(
                "%s.%s: comment enumerates %d value(s) (%s) with NO CHECK on the column "
                "— a judgement call, not asserted here"
                % (table, column, len(tokens.split("|")), tokens.strip()))
    return examined, reported


def main():
    if not Path(DB).exists():
        print("FAIL: no database at %s" % DB)
        return 2
    con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    vocab = check_vocabularies(con)

    examined, violations = 0, []
    for rel in SCANNED:
        path = ROOT / rel
        if not path.exists():
            continue
        src = path.read_text(encoding="utf-8", errors="replace")
        for m in _CHOICES.finditer(src):
            lits = {a or b for a, b in _LITERAL.findall(m.group(1))}
            if not lits:
                continue          # a non-literal list: derived already, or numeric
            examined += 1
            owner = vocab.get(frozenset(lits))
            if owner:
                line = src[:m.start()].count("\n") + 1
                table, column = owner[0]
                violations.append(
                    "%s:%d restates the CHECK on %s.%s — replace with "
                    "dbcore.schema_choices(%r, %r)%s"
                    % (rel, line, table, column, table, column,
                       "" if len(owner) == 1 else
                       " (several columns share this vocabulary: %s — pick the one the "
                       "flag WRITES, not whichever is found first)" % owner))

    col_examined, col_violations = scan_writer_columns(con)
    violations += col_violations

    mod_examined, mod_violations, mod_subsets = scan_module_collections(con, vocab)
    violations += mod_violations

    num_examined, num_violations = scan_numeric_mirrors(con)
    violations += num_violations

    cmt_examined, cmt_reported = scan_comment_vocabularies(con)

    print("EXAMINED: %d argparse choices= literal(s) across %d writer file(s), against "
          "%d live CHECK vocabular(ies); %d row dict(s) against the columns of the "
          "table their own function writes; %d module-level collection(s) across %d "
          "module(s); %d numeric choices=; %d DDL-comment enumeration(s)"
          % (examined, len(SCANNED), len(vocab), col_examined, mod_examined,
             len(MODULE_SCAN), num_examined, cmt_examined))
    print("VERDICT: " + ("FAIL" if violations else "CLEAN"))
    for v in violations:
        print("  * " + v)
    if mod_subsets:
        print("SUBSET (not a violation — a deliberate restriction, reported so it stays "
              "legible as one):")
        for s in mod_subsets:
            print("  * " + s)
    if cmt_reported:
        print("REPORTED (not blocking — a judgement call, class 5):")
        for r in cmt_reported:
            print("  * " + r)
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
