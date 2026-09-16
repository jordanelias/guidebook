#!/usr/bin/env python3
"""What did this batch actually record, in EVERY table?

Owner request, 2026-09-16: "for every batch of work, I want to see what has been
recorded in every table."

THE TABLE SET IS DERIVED FROM THE SCHEMA, NEVER LISTED HERE (CLAUDE.md rule 8).
`dbcore.WRITABLE_TABLES` was a curated list of the tables a session may write and it
went blind EIGHT times; a curated list of the tables a session may REPORT would go
blind the same way and would do it silently, because the missing table looks like a
table with nothing in it. Every table in `sqlite_master` is examined, and the ones a
session's writes cannot be attributed to are NAMED rather than omitted -- an absent
row and an unattributable row are different facts and this report never conflates them.

ATTRIBUTION IS ALSO DERIVED. A table is reached one of three ways:
  DIRECT   it carries a session column (any column whose name contains 'session'),
           found by PRAGMA table_info, not by a hardcoded column name -- the corpus
           uses `session`, `created_by_session` and `recorded_by_session` already.
  FK       it has no session column but a foreign key into a table that does, so its
           rows inherit attribution through the pointer. This is CLAUDE.md rule 5's
           "point, do not copy" read backwards: because the child never copies the
           session, the only honest way to attribute it is to follow the pointer.
  NONE     neither, at any depth. These are the provenance holes. A row written here
           by a batch CANNOT be attributed to it by any mechanism, which is worth
           seeing on every run rather than discovering after a corpus clear.
"""
import argparse
import os
import sqlite3
import sys

DEFAULT_DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
MAX_HOPS = 4  # FK chains deeper than this exist (extraction -> spec links) but are rare


def _tables(con):
    return [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name")]


def _session_cols(con, table):
    return [c[1] for c in con.execute('PRAGMA table_info("%s")' % table)
            if "session" in c[1].lower()]


def _fks(con, table):
    return [(f[2], f[3], f[4]) for f in con.execute('PRAGMA foreign_key_list("%s")' % table)]


def _resolve(con, table, direct, seen=None, depth=0):
    """Return (kind, sql_predicate, path) for attributing `table` to a session."""
    if table in direct:
        col = direct[table][0]
        return "DIRECT", '"%s" = ?' % col, [table + "." + col]
    if depth >= MAX_HOPS:
        return "NONE", None, []
    seen = (seen or set()) | {table}
    for parent, from_col, to_col in _fks(con, table):
        if parent in seen:
            continue
        kind, pred, path = _resolve(con, parent, direct, seen, depth + 1)
        if kind == "NONE":
            continue
        to = to_col or "rowid"
        return ("FK",
                '"%s" IN (SELECT "%s" FROM "%s" WHERE %s)' % (from_col, to, parent, pred),
                [table + "." + from_col + " -> " + parent] + path)
    return "NONE", None, []


def report(session, db_path=DEFAULT_DB, show_empty=False):
    con = sqlite3.connect("file:%s?mode=ro" % db_path, uri=True)
    con.row_factory = sqlite3.Row
    tables = _tables(con)
    direct = {t: cols for t in tables if (cols := _session_cols(con, t))}

    rows, holes, examined = [], [], 0
    for t in tables:
        kind, pred, path = _resolve(con, t, direct)
        total = con.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
        examined += 1
        if kind == "NONE":
            holes.append((t, total))
            rows.append((t, "NONE", None, total, ""))
            continue
        # A session id is stored bare in DB columns and with .md in pointers (CLAUDE.md
        # §7). Matching both forms is deliberate: the wrong form scopes a gate to nothing
        # and it passes green, which is the exact failure this report exists to expose.
        stem = session[:-3] if session.endswith(".md") else session
        n = con.execute('SELECT COUNT(*) FROM "%s" WHERE %s' % (t, pred.replace("= ?", "IN (?,?)")),
                        (stem, stem + ".md")).fetchone()[0] if kind == "DIRECT" else \
            con.execute('SELECT COUNT(*) FROM "%s" WHERE %s' % (t, pred), (stem,)).fetchone()[0]
        rows.append((t, kind, n, total, " <- ".join(path)))

    written = [r for r in rows if r[1] != "NONE" and r[2]]
    silent = [r for r in rows if r[1] != "NONE" and not r[2]]

    print("BATCH CAPTURE REPORT — session %s" % session)
    print("DB: %s" % db_path)
    print("=" * 78)
    print("\nRECORDED BY THIS BATCH (%d table(s)):" % len(written))
    if not written:
        print("  (nothing — this session wrote no attributable row in any table)")
    for t, kind, n, total, path in sorted(written, key=lambda r: -r[2]):
        print("  %-34s %6d row(s)   [%s of %d]%s" % (t, n, kind, total,
              "  via " + path if kind == "FK" else ""))

    print("\nUNATTRIBUTABLE TABLES (%d) — no session column and no FK path to one." % len(holes))
    print("  A batch's writes here cannot be traced to it by any mechanism.")
    for t, total in holes:
        print("  %-34s %6d row(s) total" % (t, total))

    if show_empty:
        print("\nREACHABLE BUT UNTOUCHED BY THIS BATCH (%d):" % len(silent))
        for t, kind, n, total, path in silent:
            print("  %-34s %6d row(s) total   [%s]" % (t, total, kind))

    print("\n" + "=" * 78)
    print("EXAMINED: %d table(s) — every table in the schema, derived, none listed by hand."
          % examined)
    print("  attributable: %d   unattributable: %d   written by this batch: %d"
          % (examined - len(holes), len(holes), len(written)))
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--session", required=True, help="session id (bare stem or .md form)")
    p.add_argument("--db", default=DEFAULT_DB)
    p.add_argument("--show-empty", action="store_true",
                   help="also list reachable tables this batch did not write")
    a = p.parse_args()
    sys.exit(report(a.session, a.db, a.show_empty))
