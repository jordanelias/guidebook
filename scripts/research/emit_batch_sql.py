#!/usr/bin/env python3
"""
scripts/research/emit_batch_sql.py — capture a research batch out of a scratch DB.

DR-2026-08-19 §12.0 (F3). The research write path is a session-scoped scratch
copy of the database: `db.py` writes to it under GUIDEBOOK_DB_PATH, so every
write-time refusal stays live (R9 duplicate-DOI lookups, H05/H07, CHECK
constraints, real exec_id allocation) instead of being reimplemented against a
renderer. This tool then extracts the delta as SQL, which feeds the ordinary
`emit_data_migration.py --input` and its ENUM/RANGE guards.

    python3 scripts/research/emit_batch_sql.py --scratch batch01.db --out batch01.sql

Both databases are opened read-only. This tool never writes to either one; the
only canonical write in a research session remains `migrate_db.py`.

The walk is additive by design. A row present in canonical but absent from the
scratch is REFUSED rather than rendered as a DELETE: a research batch adds
evidence, and a missing row means the scratch drifted from the canonical base
(usually a stale copy), which is a mistake to surface, not to replay.

ONE NARROW EXCEPTION, opt-in (2026-09-26). Some db.py writers delete on purpose --
`unlink-admission` removes a wrong search_admissions edge -- and an additive-only
capture made that sanctioned write impossible to ship. `--allow-delete TABLE` renders
the missing rows of TABLE as DELETEs, and only when a writer in scripts/ actually
deletes from TABLE (dbcore.deletable_tables, derived from the writers the way the
capture set is). Every other missing row is still refused, so a stale copy is still
caught, and a deletion never happens unless the operator names the table.
"""

import argparse
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

# The canonical DB honours GUIDEBOOK_DB_PATH like every other live script
# (scripts/audit/db_path_env_audit.py enforces this). The runbook invokes this
# tool without the variable set -- the scratch is named explicitly by --scratch --
# so the default resolves to data/guidebook.db in normal use.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dbcore                                                      # noqa: E402

DEFAULT_CANONICAL = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")

# FK order: a parent is always emitted before anything that references it, so
# the migration applies cleanly even with foreign_keys enforcement on.
# TABLES MOVED TO scripts/dbcore.py 2026-08-25 and is imported below.
#
# WHY: this list and db.py's write coverage were two separate homes of one fact --
# "which tables a session may write" -- and that is exactly how a table became
# writable-but-invisible to capture. A rescue wrote 8 source_locators rows and this
# tool emitted 32 statements instead of 40, losing them with NO ERROR RAISED.
#
# THAT FIX WAS THE WRONG SHAPE, corrected 2026-09-13. One constant with two importers
# stopped the CLI and this tool disagreeing WITH EACH OTHER; it did nothing about the
# constant disagreeing with db.py's actual write surface, which is where all eight
# blindnesses lived — four of them already present when the comment claiming "a table
# can never again be known to one and not the other" was written. The set is now
# DERIVED from the writers by dbcore.writable_tables(conn), so a table is captured the
# moment something can write it. Ordering comes from the live FK graph, which also
# retired a real defect: the hand list placed evidence_population_match ahead of gaps,
# which it references.


def ro(path):
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


def lit(v):
    """Render one value as a SQL literal."""
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, (bytes, bytearray)):
        return "X'" + v.hex() + "'"
    return "'" + str(v).replace("'", "''") + "'"


def columns(con, table):
    return [r[1] for r in con.execute('PRAGMA table_info("%s")' % table)]


def pk_columns(con, table):
    info = list(con.execute('PRAGMA table_info("%s")' % table))
    return [r[1] for r in sorted((r for r in info if r[5]), key=lambda r: r[5])]


def load(con, table, cols, pk):
    """Return {pk_tuple: {col: value}} for one table, ordered by primary key."""
    collist = ", ".join('"%s"' % c for c in cols)
    order = ", ".join('"%s"' % c for c in pk)
    rows = {}
    for r in con.execute('SELECT %s FROM "%s" ORDER BY %s' % (collist, table, order)):
        d = dict(zip(cols, r))
        rows[tuple(d[c] for c in pk)] = d
    return rows


def where(pk, row):
    return " AND ".join('"%s" = %s' % (c, lit(row[c])) for c in pk)


def emit(scratch_path, canonical_path, out_path, allow_delete=()):
    if scratch_path == canonical_path:
        sys.exit("ERROR: --scratch and --canonical are the same file. The scratch "
                 "must be a copy; the canonical DB is never written outside migrate_db.py.")
    sc, ca = ro(scratch_path), ro(canonical_path)

    sv = sc.execute("PRAGMA user_version").fetchone()[0]
    cv = ca.execute("PRAGMA user_version").fetchone()[0]
    if sv != cv:
        sys.exit(f"ERROR: schema version mismatch — scratch is {sv}, canonical is {cv}. "
                 "Re-copy the scratch from the current canonical DB.")

    # Derived per run from the live schema and the writers; never a module constant,
    # because a constant is what drifted eight times.
    tables = dbcore.writable_tables(ca)
    allow_delete = set(allow_delete or ())
    if allow_delete:
        not_deletable = sorted(allow_delete - dbcore.deletable_tables(ca))
        if not_deletable:
            sys.exit(f"ERROR: --allow-delete {not_deletable}: no sanctioned writer deletes from "
                     f"{'that table' if len(not_deletable) == 1 else 'those tables'} "
                     f"(dbcore.deletable_tables). A row missing there is drift, not a "
                     f"deletion to replay.")
    lines, n_ins, n_upd, missing = [], 0, 0, []
    deletes = {}
    for table in tables:
        cols = columns(ca, table)
        if not cols:
            sys.exit(f"ERROR: table {table} does not exist in the canonical DB.")
        if columns(sc, table) != cols:
            sys.exit(f"ERROR: column set for {table} differs between scratch and canonical. "
                     "Re-copy the scratch; do not hand-edit its schema.")
        pk = pk_columns(ca, table)
        if not pk:
            sys.exit(f"ERROR: {table} has no declared primary key; refusing to diff it "
                     "on implicit rowids, which are not stable across a rebuild.")

        s_rows = load(sc, table, cols, pk)
        c_rows = load(ca, table, cols, pk)
        gone = [k for k in c_rows if k not in s_rows]
        if table in allow_delete:
            if gone:
                deletes[table] = ['DELETE FROM "%s" WHERE %s;' % (table, where(pk, c_rows[k]))
                                  for k in gone]
        else:
            missing += [(table, k) for k in gone]

        inserts, updates = [], []
        for key, row in s_rows.items():                     # already PK-ordered
            if key not in c_rows:
                inserts.append('INSERT INTO "%s" (%s) VALUES (%s);' % (
                    table,
                    ", ".join('"%s"' % c for c in cols),
                    ", ".join(lit(row[c]) for c in cols)))
                continue
            changed = [c for c in cols if row[c] != c_rows[key][c]]
            if changed:
                updates.append('UPDATE "%s" SET %s WHERE %s;' % (
                    table,
                    ", ".join('"%s" = %s' % (c, lit(row[c])) for c in changed),
                    where(pk, row)))
        if inserts or updates:
            lines.append("-- %s: %d insert(s), %d update(s)" % (table, len(inserts), len(updates)))
            lines += inserts + updates
            lines.append("")
        n_ins += len(inserts)
        n_upd += len(updates)

    if missing:
        for table, key in missing[:10]:
            print(f"  {table}: {key}", file=sys.stderr)
        sys.exit(f"ERROR: {len(missing)} row(s) exist in the canonical DB but not in the "
                 "scratch. The batch path is additive — this means the scratch was copied "
                 "from a different base, or rows were deleted. Refusing to emit. If a "
                 "sanctioned writer deleted them on purpose (unlink-admission), name the "
                 "table with --allow-delete.")

    # Deletions first, children before parents (the reverse of the replay order), so a
    # DELETE never runs against a row a later statement in the same file still needs.
    n_del = 0
    del_lines = []
    for table in reversed(tables):
        if table in deletes:
            del_lines.append("-- %s: %d delete(s)" % (table, len(deletes[table])))
            del_lines += deletes[table] + [""]
            n_del += len(deletes[table])
    lines = del_lines + lines

    if not lines:
        sys.exit("ERROR: no delta — the scratch is identical to the canonical DB across "
                 "all %d writable tables. Nothing to emit.\n"
                 "         If you believe you wrote rows, check they went to a table a "
                 "writer can reach: this compares exactly the tables scripts/db.py and "
                 "assess_cell.py INSERT into, minus %s." % (len(tables), sorted(dbcore.NOT_CAPTURED)))

    header = [
        "-- Research batch delta, captured by scripts/research/emit_batch_sql.py",
        "-- Captured:  %s" % datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "-- Scratch:   %s" % scratch_path,
        "-- Canonical: %s (schema version %d)" % (canonical_path, cv),
        "-- Totals:    %d insert(s), %d update(s), %d delete(s)" % (n_ins, n_upd, n_del),
        "--",
        "-- No transaction wrapper: the migration runner owns the boundary (F5).",
        "-- Feed this to: python3 scripts/emit_data_migration.py --input <this file>",
        "",
    ]
    text = "\n".join(header + lines).rstrip() + "\n"
    if out_path == "-":
        sys.stdout.write(text)
    else:
        with open(out_path, "w") as fh:
            fh.write(text)
        print("Wrote %s — %d insert(s), %d update(s), %d delete(s)"
              % (out_path, n_ins, n_upd, n_del))
    return 0


def selftest():
    """Prove the emitter round-trips, rather than asserting it."""
    import tempfile, os, shutil
    results, failures = [], 0

    def check(name, cond, detail=""):
        nonlocal failures
        results.append((name, bool(cond), detail))
        if not cond:
            failures += 1

    with tempfile.TemporaryDirectory() as tmp:
        canon = os.path.join(tmp, "canon.db")
        con = sqlite3.connect(canon)
        con.execute('CREATE TABLE evidence_sources (ref_id TEXT PRIMARY KEY, title TEXT, year INT)')
        con.execute('CREATE TABLE source_slug_links (ref_id TEXT, slug TEXT, note TEXT, '
                    'PRIMARY KEY (ref_id, slug))')
        con.execute("INSERT INTO evidence_sources VALUES ('REF-1','existing',2020)")
        con.commit(); con.close()

        scratch = os.path.join(tmp, "scratch.db")
        shutil.copy(canon, scratch)
        con = sqlite3.connect(scratch)
        con.execute("INSERT INTO evidence_sources VALUES ('REF-2','O''Brien; a title',2021)")
        con.execute("INSERT INTO source_slug_links VALUES ('REF-2','room-acoustic-performance',NULL)")
        con.execute("UPDATE evidence_sources SET year=2022 WHERE ref_id='REF-1'")
        con.commit(); con.close()

        out = os.path.join(tmp, "batch.sql")
        # Narrow the walk to the fixture's two tables, and RESTORE it afterwards --
        # a module-global mutated by a test and left changed is a trap for any
        # caller that imports this module and runs selftest() before emit().
        _real_writable = dbcore.writable_tables
        dbcore.writable_tables = lambda _conn: ["evidence_sources", "source_slug_links"]
        emit(scratch, canon, out)
        sql = open(out).read()
        check("insert emitted", "INSERT INTO \"evidence_sources\"" in sql)
        check("update emitted, changed column only",
              'UPDATE "evidence_sources" SET "year" = 2022' in sql, sql)
        check("quote escaped", "'O''Brien; a title'" in sql)
        check("no transaction wrapper", "BEGIN" not in sql.upper().replace("BEGINNING", ""))
        check("parent table precedes child",
              sql.index("evidence_sources") < sql.index("source_slug_links"))

        # applying the delta to a copy of canonical must reproduce the scratch
        replay = os.path.join(tmp, "replay.db")
        shutil.copy(canon, replay)
        con = sqlite3.connect(replay, isolation_level=None)
        # Strip comment LINES before splitting. Filtering whole chunks that start
        # with "--" would silently drop the statement following a comment header,
        # which is exactly the class of bug the runner's _code_of() exists to avoid.
        code = "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--"))
        for stmt in [s for s in code.split(";\n") if s.strip()]:
            con.execute(stmt)
        got = con.execute("SELECT * FROM evidence_sources ORDER BY ref_id").fetchall()
        got_l = con.execute("SELECT * FROM source_slug_links").fetchall()
        con.close()
        con = sqlite3.connect(scratch)
        want = con.execute("SELECT * FROM evidence_sources ORDER BY ref_id").fetchall()
        want_l = con.execute("SELECT * FROM source_slug_links").fetchall()
        con.close()
        check("replay reproduces the scratch exactly", got == want and got_l == want_l,
              f"{got} vs {want}")

        # determinism: two runs byte-identical apart from the timestamp header
        out2 = os.path.join(tmp, "batch2.sql")
        emit(scratch, canon, out2)
        strip = lambda t: "\n".join(l for l in t.splitlines() if not l.startswith("-- Captured:"))
        check("output is deterministic", strip(sql) == strip(open(out2).read()))

        # a row missing from the scratch must be refused, not rendered as a DELETE
        con = sqlite3.connect(scratch)
        con.execute("DELETE FROM evidence_sources WHERE ref_id='REF-1'"); con.commit(); con.close()
        rc = 0
        try:
            emit(scratch, canon, os.path.join(tmp, "x.sql"))
        except SystemExit as e:
            rc = 1
            check("deletion refused with a reason", "additive" in str(e), str(e))
        check("deletion refused", rc == 1)

        # ...unless the operator names the table AND a writer deletes from it
        _real_deletable = dbcore.deletable_tables
        dbcore.deletable_tables = lambda _conn: {"evidence_sources"}
        out3 = os.path.join(tmp, "batch3.sql")
        emit(scratch, canon, out3, allow_delete=["evidence_sources"])
        sql3 = open(out3).read()
        check("an allowed deletion is rendered as a keyed DELETE",
              """DELETE FROM "evidence_sources" WHERE "ref_id" = 'REF-1';""" in sql3, sql3)
        check("deletions precede inserts",
              sql3.index("DELETE FROM") < sql3.index("INSERT INTO"))
        replay3 = os.path.join(tmp, "replay3.db")
        shutil.copy(canon, replay3)
        con = sqlite3.connect(replay3, isolation_level=None)
        code3 = "\n".join(l for l in sql3.splitlines() if not l.strip().startswith("--"))
        for stmt in [s for s in code3.split(";\n") if s.strip()]:
            con.execute(stmt)
        got3 = con.execute("SELECT * FROM evidence_sources ORDER BY ref_id").fetchall()
        con.close()
        con = sqlite3.connect(scratch)
        want3 = con.execute("SELECT * FROM evidence_sources ORDER BY ref_id").fetchall()
        con.close()
        check("replay with the deletion reproduces the scratch exactly", got3 == want3,
              f"{got3} vs {want3}")
        dbcore.deletable_tables = lambda _conn: set()
        rc = 0
        try:
            emit(scratch, canon, os.path.join(tmp, "y.sql"), allow_delete=["evidence_sources"])
        except SystemExit as e:
            rc = 1
            check("--allow-delete on a table no writer deletes from is refused",
                  "no sanctioned writer" in str(e), str(e))
        check("--allow-delete without a deleting writer refused", rc == 1)
        dbcore.deletable_tables = _real_deletable

    dbcore.writable_tables = _real_writable
    print("\n--- emit_batch_sql selftest ---")
    for name, ok, detail in results:
        print("  %s: %s%s" % ("PASS" if ok else "**FAIL**", name,
                              ("  [%s]" % detail) if not ok else ""))
    print("\nRESULTS: %d/%d selftest cases pass" % (len(results) - failures, len(results)))
    print("SELFTEST: %s" % ("FAIL" if failures else "PASS"))
    return 1 if failures else 0


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--scratch", help="Session scratch DB written by db.py under GUIDEBOOK_DB_PATH")
    p.add_argument("--canonical", default=DEFAULT_CANONICAL,
                   help="Canonical DB to diff against (default: $GUIDEBOOK_DB_PATH "
                        "or data/guidebook.db)")
    p.add_argument("--out", default="-", help="Write SQL here ('-' for stdout)")
    p.add_argument("--allow-delete", action="append", default=[], metavar="TABLE",
                   help="Render rows missing from the scratch in TABLE as DELETEs. Only for a "
                        "table a sanctioned writer deletes from (e.g. search_admissions, "
                        "unlink-admission); repeatable. Everything else stays additive.")
    p.add_argument("--selftest", action="store_true", help="Run the round-trip tests and exit")
    args = p.parse_args()
    if args.selftest:
        sys.exit(selftest())
    if not args.scratch:
        p.error("--scratch is required (or use --selftest)")
    sys.exit(emit(args.scratch, args.canonical, args.out, allow_delete=args.allow_delete))


if __name__ == "__main__":
    main()
