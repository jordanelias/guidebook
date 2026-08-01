#!/usr/bin/env python3
"""
scripts/audit/migration_reproducibility.py — GAP-290 enforcement.

Rebuilds a fresh DB from the migration history alone and compares core invariants
against the committed data/guidebook.db. A divergence means someone wrote directly
to the DB and bypassed the migration system, so the committed blob no longer
reproduces from its own history.

WHY THIS IS A SCRIPT
--------------------
It used to exist twice — as an inline heredoc in .github/workflows/audit.yml and
a second, separately-maintained heredoc in scripts/preflight.sh. Two copies of an
invariant list is one copy too many: adding a table to one does not add it to the
other, and nothing would have told you. This is now the single definition, wired
through governance/check-registry.yaml.

SCOPE (DR-2026-05-28 / D-4.3-H option 3a, ratified 2026-06-11)
--------------------------------------------------------------
The gate enforces the CORE INVARIANTS below. They cover all synthesis-bearing
content and must reproduce from migration history.

The job-owned tables `evidence_source_authors` and `pipeline_runs` are
DELIBERATELY EXEMPT: the source-verification scheduled job (resolve-dois.yml /
verify-urls.yml) is their authoritative writer and writes them outside the
migration framework by design. Do NOT add them to the invariant list.
**Adding any new exempt table requires a new DR.**

Checks:
  C1  the migration history rebuilds without error
  C2  PRAGMA user_version matches
  C3  each core table's row count matches

Usage:
    python3 scripts/audit/migration_reproducibility.py
    python3 scripts/audit/migration_reproducibility.py --rebuilt-to /tmp/rebuilt.db
    python3 scripts/audit/migration_reproducibility.py --selftest

Exit codes: 0 = reproducible, 1 = divergence or rebuild failure, 2 = cannot run.

Honours GUIDEBOOK_DB_PATH (default data/guidebook.db).
"""

import argparse
import os
import sqlite3
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# The 7 core invariants. Keep this list and the DR in sync; it is the contract.
CORE_INVARIANTS = [
    ("PRAGMA user_version", "schema_version"),
    ("SELECT COUNT(*) FROM evidence_sources", "evidence_sources count"),
    ("SELECT COUNT(*) FROM citation_mining", "citation_mining count"),
    ("SELECT COUNT(*) FROM source_slug_links", "source_slug_links count"),
    ("SELECT COUNT(*) FROM gaps", "gaps count"),
    ("SELECT COUNT(*) FROM connections", "connections count"),
    ("SELECT COUNT(*) FROM items", "items count"),
]

EXEMPT_TABLES = ("evidence_source_authors", "pipeline_runs")

# Columns whose divergence is bookkeeping rather than substance. Kept separate so
# --deep can say "277 rows differ, all of them only in updated_at" instead of
# reporting that as content drift and being ignored for crying wolf.
VOLATILE_COLUMNS = frozenset({
    "created_at", "updated_at", "last_updated",
    "created_by_session", "updated_by_session",
})

# data_migrations is the ledger *of* the rebuild, so comparing its application
# provenance compares the run to itself: applied_at is when this run applied each
# migration, and the runner stamps notes='rebuilt by runner'. What must match is
# which migrations exist and what their content hashed to. Handled by name rather
# than by adding "notes"/"applied_at" to VOLATILE_COLUMNS, which would blind the
# comparison to genuine drift in any other table carrying a column so named.
LEDGER_TABLE = "data_migrations"
LEDGER_COLUMNS = ("migration_id", "content_sha")


def db_path():
    return os.environ.get("GUIDEBOOK_DB_PATH", os.path.join(REPO_ROOT, "data", "guidebook.db"))


def rebuild(target):
    """C1 — rebuild from migration history alone."""
    proc = subprocess.run(
        [sys.executable, "scripts/migrate_db.py", "--rebuild", target],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


def compare(committed_path, rebuilt_path):
    """C2/C3 — compare the core invariants. Returns (rows, mismatches)."""
    committed = sqlite3.connect(f"file:{committed_path}?mode=ro", uri=True)
    rebuilt = sqlite3.connect(f"file:{rebuilt_path}?mode=ro", uri=True)
    rows, mismatches = [], []
    for sql, label in CORE_INVARIANTS:
        try:
            c = committed.execute(sql).fetchone()[0]
            r = rebuilt.execute(sql).fetchone()[0]
        except sqlite3.OperationalError as exc:
            # A table may legitimately not exist in an older schema version.
            rows.append((label, None, None, f"skip ({exc})"))
            continue
        status = "OK" if c == r else "MISMATCH"
        rows.append((label, c, r, status))
        if c != r:
            mismatches.append((label, c, r))
    committed.close()
    rebuilt.close()
    return rows, mismatches


def user_tables(conn):
    return {n for (n,) in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}


def deep_compare(committed_path, rebuilt_path):
    """Every table, every row — not just seven scalars.

    WHY THIS EXISTS. The core invariants are `PRAGMA user_version` plus COUNT(*)
    on six tables. An UPDATE changes no count, so the entire class of "someone
    edited values in the committed DB" is invisible to them, and so is any change
    to the 56 tables not on the list. CLAUDE.md rule 4 nonetheless says CI "fails
    on any divergence", which was never what the comparator did.

    Returns (report_rows, substantive, volatile_only), where each report row is
    (table, verdict, detail).
    """
    committed = sqlite3.connect(f"file:{committed_path}?mode=ro", uri=True)
    rebuilt = sqlite3.connect(f"file:{rebuilt_path}?mode=ro", uri=True)
    rows, substantive, volatile_only = [], [], []

    tc, tr = user_tables(committed), user_tables(rebuilt)
    for missing in sorted(tc - tr):
        rows.append((missing, "MISSING-IN-REBUILD", "table absent from migration history"))
        substantive.append(missing)
    for extra in sorted(tr - tc):
        rows.append((extra, "EXTRA-IN-REBUILD", "migration history builds a table the DB lacks"))
        substantive.append(extra)

    for table in sorted(tc & tr):
        if table in EXEMPT_TABLES:
            rows.append((table, "EXEMPT", "job-owned per DR-2026-05-28"))
            continue
        cols = [r[1] for r in committed.execute(f"PRAGMA table_info({table})")]
        rcols = [r[1] for r in rebuilt.execute(f"PRAGMA table_info({table})")]
        if cols != rcols:
            rows.append((table, "SCHEMA-DIFF", f"columns differ: {set(cols) ^ set(rcols)}"))
            substantive.append(table)
            continue
        if table == LEDGER_TABLE:
            cols = [c for c in cols if c in LEDGER_COLUMNS]
        order = ", ".join(f'"{c}"' for c in cols)
        # Explicit column list, not SELECT * — the ledger case narrows `cols`, and
        # * would return the excluded columns anyway and compare them.
        sql = f'SELECT {order} FROM "{table}" ORDER BY {order}'
        cr = committed.execute(sql).fetchall()
        rr = rebuilt.execute(sql).fetchall()
        if len(cr) != len(rr):
            rows.append((table, "COUNT", f"committed={len(cr)} rebuilt={len(rr)}"))
            substantive.append(table)
            continue
        differing_cols, n_rows = {}, 0
        for a, b in zip(cr, rr):
            if a == b:
                continue
            n_rows += 1
            for i, name in enumerate(cols):
                if a[i] != b[i]:
                    differing_cols[name] = differing_cols.get(name, 0) + 1
        if not differing_cols:
            rows.append((table, "OK", ""))
            continue
        real = {c: n for c, n in differing_cols.items() if c not in VOLATILE_COLUMNS}
        summary = ", ".join(f"{c}({n})" for c, n in
                            sorted(differing_cols.items(), key=lambda x: -x[1])[:5])
        if real:
            rows.append((table, "CONTENT", f"{n_rows} rows; {summary}"))
            substantive.append(table)
        else:
            rows.append((table, "TIMESTAMPS", f"{n_rows} rows; {summary}"))
            volatile_only.append(table)

    committed.close()
    rebuilt.close()
    return rows, substantive, volatile_only


def audit(rebuilt_to=None, deep=False):
    committed_path = db_path()
    if not os.path.exists(committed_path):
        print(f"ERROR: committed DB not found at {committed_path}")
        return 2

    print("=" * 70)
    print("Migration reproducibility (GAP-290)")
    print("=" * 70)
    print(f"  committed: {committed_path}")

    tmp = rebuilt_to
    cleanup = False
    if tmp is None:
        handle, tmp = tempfile.mkstemp(suffix=".db", prefix="reproducibility_")
        os.close(handle)
        os.unlink(tmp)          # migrate_db.py wants to create it itself
        cleanup = True
    print(f"  rebuilt:   {tmp}")
    print()

    ok, log = rebuild(tmp)
    if not ok:
        print("  C1 rebuild from migration history: FAIL")
        for line in log.splitlines()[-15:]:
            print(f"      {line}")
        return 1
    print("  C1 rebuild from migration history: OK")
    print()

    rows, mismatches = compare(committed_path, tmp)
    for label, c, r, status in rows:
        if c is None:
            print(f"  {label:30} {status}")
        else:
            print(f"  {label:30} committed={c:>8}  rebuilt={r:>8}  {status}")

    deep_substantive = deep_volatile = None
    if deep:
        print()
        print("  --- deep comparison: every table, every row ---")
        deep_rows, deep_substantive, deep_volatile = deep_compare(committed_path, tmp)
        for table, verdict, detail in deep_rows:
            if verdict == "OK":
                continue
            print(f"  {table:32} {verdict:20} {detail}")
        n_ok = sum(1 for _, v, _ in deep_rows if v == "OK")
        print(f"  ({n_ok} tables identical, not listed)")

    if cleanup:
        try:
            os.unlink(tmp)
        except OSError:
            pass

    print()
    print(f"  Exempt (job-owned, DR-2026-05-28): {', '.join(EXEMPT_TABLES)}")
    print("=" * 70)
    if mismatches:
        print(f"  ERROR: {len(mismatches)} invariant(s) diverge between the committed DB")
        print("  and what the migration history produces. Someone wrote to")
        print("  data/guidebook.db without emitting a data migration.")
        print("  Per GAP-290, all DB writes go through scripts/emit_data_migration.py.")
        print("VERDICT: FAIL")
        return 1
    if deep and deep_substantive:
        print(f"  ERROR: {len(deep_substantive)} table(s) diverge in content that the")
        print("  seven core invariants cannot see, because an UPDATE changes no COUNT:")
        print(f"    {', '.join(sorted(deep_substantive))}")
        if deep_volatile:
            print(f"  ({len(deep_volatile)} more differ only in timestamp/session columns:")
            print(f"    {', '.join(sorted(deep_volatile))})")
        print("  Either those writes owe a data migration, or the table is job-owned")
        print("  and DR-2026-05-28's exemption list needs widening. Both are owner")
        print("  calls; this check reports the divergence rather than choosing.")
        print("VERDICT: FAIL (deep)")
        return 1
    if deep and deep_volatile:
        print(f"  NOTE: {len(deep_volatile)} table(s) differ only in timestamp/session")
        print(f"  columns: {', '.join(sorted(deep_volatile))}")
    print("  PASS: the committed DB matches what the migration history produces.")
    print("VERDICT: PASS")
    return 0


def selftest():
    """Prove the comparator actually fires. Builds two DBs that differ by one row
    and asserts a mismatch is reported — the repo's "a gate nobody has watched
    fire is not a gate" norm."""
    print("=" * 70)
    print("migration_reproducibility --selftest")
    print("=" * 70)
    failures = []

    def check(label, condition, detail=""):
        if condition:
            print(f"  [PASS] {label}")
        else:
            print(f"  [FAIL] {label}{': ' + detail if detail else ''}")
            failures.append(label)

    with tempfile.TemporaryDirectory() as tmpdir:
        a = os.path.join(tmpdir, "a.db")
        b = os.path.join(tmpdir, "b.db")
        for path, extra in ((a, 0), (b, 1)):
            con = sqlite3.connect(path)
            con.execute("PRAGMA user_version = 42")
            for table in ("evidence_sources", "citation_mining", "source_slug_links",
                          "gaps", "connections", "items"):
                con.execute(f"CREATE TABLE {table} (id INTEGER PRIMARY KEY)")
                con.execute(f"INSERT INTO {table} (id) VALUES (1)")
            for i in range(extra):
                con.execute("INSERT INTO items (id) VALUES (?)", (100 + i,))
            con.commit()
            con.close()

        _, same = compare(a, a)
        check("identical DBs report no mismatch", not same, str(same))

        _, differ = compare(a, b)
        check("a one-row divergence in `items` IS reported",
              any(label == "items count" for label, _, _ in differ), str(differ))

        # A missing table must be skipped, not crash the comparator.
        c = os.path.join(tmpdir, "c.db")
        con = sqlite3.connect(c)
        con.execute("PRAGMA user_version = 42")
        con.commit()
        con.close()
        rows, _ = compare(c, c)
        check("missing tables are skipped, not fatal",
              any(r[3].startswith("skip") for r in rows))

        # --- deep comparison -------------------------------------------------
        # The point of --deep is the case the core invariants are blind to: an
        # UPDATE, which changes values while leaving every COUNT identical. These
        # two assertions are a matched pair — the second is only meaningful
        # because the first shows the core comparator says PASS on the same DBs.
        d = os.path.join(tmpdir, "d.db")
        e = os.path.join(tmpdir, "e.db")
        for path, title, stamp in ((d, "original", "2026-01-01"), (e, "TAMPERED", "2026-01-01")):
            con = sqlite3.connect(path)
            con.execute("PRAGMA user_version = 42")
            for table in ("evidence_sources", "citation_mining", "source_slug_links",
                          "gaps", "connections", "items"):
                con.execute(f"CREATE TABLE {table} (id INTEGER PRIMARY KEY)")
                con.execute(f"INSERT INTO {table} (id) VALUES (1)")
            con.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, title TEXT, updated_at TEXT)")
            con.execute("INSERT INTO t VALUES (1, ?, ?)", (title, stamp))
            con.commit()
            con.close()

        _, core_mismatches = compare(d, e)
        check("core invariants are BLIND to a value-only edit (the gap --deep closes)",
              not core_mismatches, str(core_mismatches))

        _, substantive, _ = deep_compare(d, e)
        check("--deep reports the value-only edit the counts missed",
              "t" in substantive, str(substantive))

        # A timestamp-only difference must be separated from real content, or the
        # check cries wolf on every rebuild and stops being read.
        f = os.path.join(tmpdir, "f.db")
        con = sqlite3.connect(f)
        con.execute("PRAGMA user_version = 42")
        for table in ("evidence_sources", "citation_mining", "source_slug_links",
                      "gaps", "connections", "items"):
            con.execute(f"CREATE TABLE {table} (id INTEGER PRIMARY KEY)")
            con.execute(f"INSERT INTO {table} (id) VALUES (1)")
        con.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, title TEXT, updated_at TEXT)")
        con.execute("INSERT INTO t VALUES (1, 'original', '2026-09-09')")
        con.commit()
        con.close()

        _, subst2, volatile2 = deep_compare(d, f)
        check("a timestamp-only difference is classed volatile, not content",
              "t" in volatile2 and "t" not in subst2, f"subst={subst2} volatile={volatile2}")

    print("=" * 70)
    if failures:
        print(f"SELFTEST: FAIL — {', '.join(failures)}")
        return 1
    print("SELFTEST: PASS — the comparator fires on divergence.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rebuilt-to", metavar="PATH",
                    help="keep the rebuilt DB at PATH instead of a temp file")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--deep", action="store_true",
                    help="compare every table and every row, not just the 7 core "
                         "invariants (which are counts, and so cannot see an UPDATE)")
    args = ap.parse_args()
    return selftest() if args.selftest else audit(args.rebuilt_to, deep=args.deep)


if __name__ == "__main__":
    sys.exit(main())
