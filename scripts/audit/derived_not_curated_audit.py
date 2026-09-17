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

EXAMINED counts `choices=` literals inspected, not files read.
"""
import ast
import os
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = os.environ.get("GUIDEBOOK_DB_PATH", str(ROOT / "data" / "guidebook.db"))

#: Files whose argparse parsers are in scope. The writers; a report script that offers a
#: fixed menu of its own output formats is not restating a schema vocabulary.
SCANNED = ("scripts/db.py",)

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
    sys.path.insert(0, str(ROOT / "scripts"))
    import dbcore                                                    # noqa: E402
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

    print("EXAMINED: %d argparse choices= literal(s) across %d writer file(s), against "
          "%d live CHECK vocabular(ies); and %d row dict(s) against the columns of the "
          "table their own function writes" % (examined, len(SCANNED), len(vocab),
                                               col_examined))
    print("VERDICT: " + ("FAIL" if violations else "CLEAN"))
    for v in violations:
        print("  * " + v)
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
