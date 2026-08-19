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
"""

import argparse
import os
import sqlite3
import sys
from datetime import datetime, timezone

# The canonical DB honours GUIDEBOOK_DB_PATH like every other live script
# (scripts/audit/db_path_env_audit.py enforces this). The runbook invokes this
# tool without the variable set -- the scratch is named explicitly by --scratch --
# so the default resolves to data/guidebook.db in normal use.
DEFAULT_CANONICAL = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")

# FK order: a parent is always emitted before anything that references it, so
# the migration applies cleanly even with foreign_keys enforcement on.
TABLES = [
    "evidence_sources",
    "source_slug_links",
    "search_executions",
    "search_admissions",
    "search_candidates",
    "evidence_population_match",
    "citation_mining",
    "jurisdictional_values",
    "economics_entries",
    "case_studies",
    "gaps",
]


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


def emit(scratch_path, canonical_path, out_path):
    if scratch_path == canonical_path:
        sys.exit("ERROR: --scratch and --canonical are the same file. The scratch "
                 "must be a copy; the canonical DB is never written outside migrate_db.py.")
    sc, ca = ro(scratch_path), ro(canonical_path)

    sv = sc.execute("PRAGMA user_version").fetchone()[0]
    cv = ca.execute("PRAGMA user_version").fetchone()[0]
    if sv != cv:
        sys.exit(f"ERROR: schema version mismatch — scratch is {sv}, canonical is {cv}. "
                 "Re-copy the scratch from the current canonical DB.")

    lines, n_ins, n_upd, missing = [], 0, 0, []
    for table in TABLES:
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
        missing += [(table, k) for k in c_rows if k not in s_rows]

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
                 "from a different base, or rows were deleted. Refusing to emit.")

    if not lines:
        sys.exit("ERROR: no delta — the scratch is identical to the canonical DB across "
                 "all %d tables. Nothing to emit." % len(TABLES))

    header = [
        "-- Research batch delta, captured by scripts/research/emit_batch_sql.py",
        "-- Captured:  %s" % datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "-- Scratch:   %s" % scratch_path,
        "-- Canonical: %s (schema version %d)" % (canonical_path, cv),
        "-- Totals:    %d insert(s), %d update(s)" % (n_ins, n_upd),
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
        print("Wrote %s — %d insert(s), %d update(s)" % (out_path, n_ins, n_upd))
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
        global TABLES
        _real_tables = TABLES
        TABLES = ["evidence_sources", "source_slug_links"]
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

    TABLES = _real_tables
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
    p.add_argument("--selftest", action="store_true", help="Run the round-trip tests and exit")
    args = p.parse_args()
    if args.selftest:
        sys.exit(selftest())
    if not args.scratch:
        p.error("--scratch is required (or use --selftest)")
    sys.exit(emit(args.scratch, args.canonical, args.out))


if __name__ == "__main__":
    main()
