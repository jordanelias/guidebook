#!/usr/bin/env python3
"""
scripts/audit/extraction_relations_integrity.py — figure_role / extraction_relations
integrity gate (migration 075, 2026-09-13).

WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS (CLAUDE.md section 5(c) / section 1).
`figure_role` is what tells a downstream reader whether a stored number is the source's
own headline claim, an incidental finding, a qualifier that means nothing on its own, or
a value this project computed rather than read off a source. Nothing else on the row says
this. Once a writer exists that lets a session grade these columns (one is being built in
parallel — this check assumes it will land), a row that is EVER created without a stated
figure_role is a row a determination can silently treat as an asserted value — a tested
rig setting, or a finding that a code is inadequate, governing a cell as though it were a
plain claim. That is exactly the class of error migration 075's own header describes:
every field involved is populated and none of them is individually false; the falsity is
in what the figure IS, relative to what the row lets a reader assume. Separately, a row
graded 'derived' with no linked base input is a number with no declared arithmetic behind
it, and a stored 'derived' value that no longer matches what its own linked base+delta
inputs recompute to is a determination silently drifting away from the evidence it claims
to be computed from — the same "stored figure trusted on faith" failure derivation_sha and
test_db_integrity's K01 already exist to close for specifications, now open on this table
too because v_derived_figure_check (migration 075) is not wired to anything until this
check reads it. A 'condition' row that qualifies nothing (not the target of any edge, and
the source of no condition_on edge) is a qualifier attached to nothing — the same shape as
the ramp-slope-with-no-run-limit problem 075 exists to fix, reintroduced one row at a time
if nobody checks that every condition actually conditions something.

WHAT IT CHECKS
  1. UNGRADED / FAILED figure_role. Every live row predates migration 075 and is NULL —
     that is expected and reported as UNGRADED, not failed, per the guard below. A row
     created AFTER the migration-075 boundary with figure_role IS NULL has no such excuse
     and fails.
  2. Every figure_role='derived' row carries an outgoing extraction_relations edge with
     relation='derived_from' AND input_role='base'. No base input, no legible derivation.
  3. Every row of v_derived_figure_check where recomputed disagrees with the row's own
     stored value fails — a derived figure that no longer matches its own inputs.
  4. Every figure_role='condition' row is either the target of some edge or the source of
     a condition_on edge. Neither: it is a condition on nothing, an orphan.

HOW THE MIGRATION-075 BOUNDARY IS DERIVED (CLAUDE.md rule 7 — no hand-written dates).
`scripts/migrate_db.py` was read end to end to answer this (see discover_schema_migrations,
_apply_atomically, and the `data_migrations` ledger it builds). A SCHEMA migration — 075 is
one — is applied by bumping `PRAGMA user_version` atomically with its own DDL and nothing
else; unlike a DATA migration, it gets no row anywhere recording WHEN. There is no
"schema_migrations" table in this schema (confirmed against sqlite_master) and no other
timestamped record of a schema migration's application exists in the database.

Git history of the migration file DOES record it (migration 075 landed in one isolated
commit, 2026-09-13T02:15:07+00:00, touching nothing but the DB blob and its own
apparatus) — but this check's own registration (battery db_integrity) runs in a CI job
whose `actions/checkout` step takes the default `fetch-depth: 1` (.github/workflows/ci.yml,
`db-integrity:` job), a SHALLOW clone with no history to walk. A check that depends on git
log here would pass locally and lie in exactly the CI job that matters. So this reads the
one thing migrate_db.py DOES ledger with a timestamp: `data_migrations.applied_at`. Because
migrate_db.py always finishes every pending SCHEMA step before any pending DATA step in the
same run (build_plan()'s documented default order), MAX(data_migrations.applied_at) as of
today is a real fact recorded by the runner and a SAFE (never-too-early) lower bound on when
075 applied, given 075 has already reached this database (figure_role/comparator exist —
checked below) and every data migration on disk has already applied (checked separately;
not assumed here). The bound is conservative in one direction only: a future data migration
applied after today would push it later, which only widens the grandfather window a little
further — never turns a genuinely-pre-075 row into a failure, and stops mattering entirely
the moment the PRE_075_GRANDFATHER guard below is flipped off. It is deliberately not
pinned to a literal date.

THE GUARD — flip this OFF in the backfill commit; say so in the check-registry.yaml note too.
"""
import os
import sqlite3
import sys
from datetime import datetime, timezone

DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
TABLE = "source_value_extractions"
RELATIONS = "extraction_relations"
VIEW = "v_derived_figure_check"
LEDGER = "data_migrations"

# ---------------------------------------------------------------------------
# BACKFILL GUARD (single line, per the orchestrator's own instruction: flip
# this to False in the commit that backfills figure_role on the pre-075 rows,
# and nowhere else). While True: a figure_role-NULL row created at-or-before
# the migration-075 boundary computed below is reported as UNGRADED and does
# NOT fail this check. Once False: every figure_role-NULL row fails, full
# stop, and the boundary is never consulted.
# ---------------------------------------------------------------------------
PRE_075_GRANDFATHER = False  # flipped 2026-09-13: the backfill landed, all rows graded

# THE GRANDFATHERED SET IS A FROZEN LIST OF ROW IDS, NOT A TIME RANGE.
#
# Corrected 2026-09-13 by the orchestrator, before this check was ever committed.
# The first implementation grandfathered any figure_role-NULL row created at or
# before MAX(data_migrations.applied_at). That boundary FLOATS FORWARD with every
# new data migration, and the consequence was demonstrated rather than argued:
#
#   an ungraded row created 02:45, boundary 01:10  -> VERDICT: FAIL, exit 1
#   one unrelated data migration lands at 03:00    -> VERDICT: CLEAN, exit 0
#
# The same defect, un-failed by an event that had nothing to do with it. And it
# is worse than intermittent: a row is written to a scratch DB and the migration
# carrying it is applied afterwards, so EVERY row written through the sanctioned
# path has created_at earlier than the applied_at of its own migration. A
# floating boundary can therefore never catch the case this check exists for,
# while being a BLOCKING gate that reports CLEAN -- CLAUDE.md 5(a), a gate that
# passes having examined nothing, inside the check written to enforce 075.
#
# The grandfathered set is not a period of time. It is eight specific rows that
# existed when 075 landed, and it is enumerable, so it is enumerated. Anything
# not on this list must be graded, whenever it was written. The list only ever
# shrinks: the backfill grades these rows and the guard above goes False.
PRE_075_UNGRADED_IDS = frozenset({1, 2, 3, 4, 5, 6, 7, 8})


def _parse_ts(raw):
    """Parse either timestamp form this database actually uses into an aware
    UTC datetime, or None if it parses as neither.

      - data_migrations.applied_at: ISO-8601 with a UTC offset, e.g.
        '2026-09-13T01:10:06+00:00' (migrate_db.py: datetime.now(timezone.utc)
        .isoformat(timespec='seconds')).
      - source_value_extractions.created_at: naive, minute precision, always
        UTC, e.g. '2026-09-13 01:07' (scripts/dbcore.py: now() ->
        strftime("%Y-%m-%d %H:%M")).

    datetime.fromisoformat handles both directly (Python's isoformat parser
    accepts the space-separated form as well as 'T'); a naive result is
    stamped UTC rather than left ambiguous, because every writer of either
    column in this codebase is UTC-only.
    """
    if raw is None:
        return None
    raw = raw.strip()
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def main() -> int:
    if not os.path.exists(DB):
        print(f"FAIL: no database at {DB}")
        return 2
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row

    present = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
    for needed in (TABLE, RELATIONS, VIEW, LEDGER):
        if needed not in present:
            print(f"FAIL: {needed} does not exist. If it was renamed, this check is a "
                  f"caller and must be swept (CLAUDE.md rule 4).")
            return 2

    cols = {r[1] for r in con.execute(f"PRAGMA table_info({TABLE})")}
    if "figure_role" not in cols or "comparator" not in cols:
        print(f"FAIL: {TABLE} lacks figure_role/comparator — migration 075 is not applied "
              f"to this database.")
        return 2

    sve_rows = con.execute(
        f"SELECT extraction_id, figure_role, comparator, created_at FROM {TABLE}"
    ).fetchall()
    rel_rows = con.execute(f"SELECT * FROM {RELATIONS}").fetchall()
    view_rows = con.execute(f"SELECT derived_id FROM {VIEW}").fetchall()

    examined = len(sve_rows) + len(rel_rows) + len(view_rows)
    print(f"EXAMINED: {examined}  ({len(sve_rows)} {TABLE} row(s), "
          f"{len(rel_rows)} {RELATIONS} edge(s), {len(view_rows)} {VIEW} row(s))")

    if examined == 0:
        print("VERDICT: NOTHING-IN-SCOPE — no extraction, relation or derived-figure row "
              "exists yet.")
        return 0

    failures = []

    # --- 1. figure_role IS NULL: ungraded (excused) vs unheeded (not) -------
    ungraded, unheeded = [], []
    for r in sve_rows:
        if r["figure_role"] is not None:
            continue
        eid = r["extraction_id"]
        if PRE_075_GRANDFATHER and eid in PRE_075_UNGRADED_IDS:
            ungraded.append(eid)
        else:
            unheeded.append(eid)

    if unheeded:
        if PRE_075_GRANDFATHER:
            reason = ("and is not one of the eight rows that predate migration 075, so no "
                      "writer excuse is left")
        else:
            reason = "and PRE_075_GRANDFATHER is off, so every NULL row must be graded now"
        failures.append(
            f"{len(unheeded)} {TABLE} row(s) carry figure_role IS NULL, {reason}: "
            f"{unheeded[:10]}" + (" …" if len(unheeded) > 10 else ""))

    if PRE_075_GRANDFATHER:
        still = sorted(PRE_075_UNGRADED_IDS - {r["extraction_id"] for r in sve_rows
                                               if r["figure_role"] is not None})
        print(f"UNGRADED: {len(ungraded)}  (figure_role NULL on rows predating migration "
              f"075 — grandfathered by the frozen id list, not failed. Still ungraded: "
              f"{still}. Flip PRE_075_GRANDFATHER off once the backfill lands.)")
    else:
        print("UNGRADED: 0  (PRE_075_GRANDFATHER is off — every figure_role-NULL row is "
              "required to be graded, unconditionally)")

    # --- 2. figure_role='derived' must carry a derived_from/base edge -------
    derived_ids = {r["extraction_id"] for r in sve_rows if r["figure_role"] == "derived"}
    base_edge_sources = {
        r["from_extraction_id"] for r in rel_rows
        if r["relation"] == "derived_from" and r["input_role"] == "base"
    }
    orphan_derived = sorted(derived_ids - base_edge_sources)
    if orphan_derived:
        failures.append(
            f"{len(orphan_derived)} figure_role='derived' row(s) carry no "
            f"derived_from edge with input_role='base', so nothing says what they are "
            f"computed from: extraction_id {orphan_derived}")

    # --- 3. v_derived_figure_check: a derived value that disagrees with its --
    #        own recomputed inputs.
    mismatches = con.execute(
        f"SELECT derived_id, stored, recomputed FROM {VIEW} "
        f"WHERE recomputed IS NOT NULL AND recomputed <> CAST(stored AS REAL)"
    ).fetchall()
    if mismatches:
        failures.append(
            f"{len(mismatches)} {VIEW} row(s) disagree with their own base+delta inputs: "
            + ", ".join(f"extraction_id {m['derived_id']} (stored={m['stored']}, "
                        f"recomputed={m['recomputed']})" for m in mismatches))

    # --- 4. orphan figure_role='condition' rows ------------------------------
    condition_ids = {r["extraction_id"] for r in sve_rows if r["figure_role"] == "condition"}
    targeted = {r["to_extraction_id"] for r in rel_rows if r["to_extraction_id"] is not None}
    condition_on_sources = {
        r["from_extraction_id"] for r in rel_rows if r["relation"] == "condition_on"
    }
    orphan_conditions = sorted(
        c for c in condition_ids if c not in targeted and c not in condition_on_sources
    )
    if orphan_conditions:
        failures.append(
            f"{len(orphan_conditions)} figure_role='condition' row(s) qualify nothing — "
            f"neither the target of any edge nor the source of a condition_on edge: "
            f"extraction_id {orphan_conditions}")

    print("VERDICT: " + ("FAIL" if failures else "CLEAN"))
    for f in failures:
        print(f"  * {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
