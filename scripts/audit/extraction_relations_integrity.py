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

GRADING IS UNCONDITIONAL. An earlier cut of this check carried a grandfather clause for
the eight rows that predated migration 075 -- first as a boundary computed from
MAX(data_migrations.applied_at), which floated forward and could un-fail the defects it
existed to catch, then as a frozen id list. The backfill graded those eight and the 2026-09-13
corpus clear deleted them, so the clause guarded nothing and its "on" position had become
actively wrong: extraction_id is AUTOINCREMENT and the sequence was not reset, so re-enabling
it would have excused the first eight rows of the NEXT corpus. Both are gone. Every
figure_role-NULL row fails, whenever it was written.
"""
import os
import sqlite3
import sys

DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
TABLE = "source_value_extractions"
RELATIONS = "extraction_relations"
VIEW = "v_derived_figure_check"



def main() -> int:
    if not os.path.exists(DB):
        print(f"FAIL: no database at {DB}")
        return 2
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row

    present = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
    for needed in (TABLE, RELATIONS, VIEW):
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

    # --- 1. figure_role IS NULL is a failure, unconditionally ---------------
    #
    # THE GRANDFATHER CLAUSE IS GONE, AND DELETING IT WAS NOT MERELY TIDYING. It was a
    # module-level `PRE_075_GRANDFATHER` flag plus a frozen id list {1..8} naming the
    # extraction rows that predated migration 075. The backfill graded all eight and
    # flipped the flag off the same day; the 2026-09-13 corpus clear then deleted the
    # rows themselves, and `source_value_extractions.extraction_id` is AUTOINCREMENT,
    # so the next batch re-mints from 1 into a table whose sequence was not reset.
    # Turning the flag back on would therefore have excused the FIRST EIGHT ROWS OF THE
    # NEW CORPUS -- rows it never meant, under the name of rows that no longer exist.
    #
    # A switch whose off position is correct and whose on position has become actively
    # wrong is not a switch. The rule it guarded survives as the general one below, and
    # git history is the archive for the mechanism (CLAUDE.md section 8).
    #
    # THE TRANSFERABLE LESSON, recorded here because it cost two corrections: a
    # grandfather clause is a FROZEN ENUMERATION or it is not a grandfather clause. This
    # check originally computed its boundary as MAX(data_migrations.applied_at), which
    # floated forward with every later migration and would eventually have excused the
    # very rows it existed to catch -- demonstrated un-firing itself, then replaced by
    # the frozen list, which has now outlived the rows it froze.
    unheeded = [r["extraction_id"] for r in sve_rows if r["figure_role"] is None]
    if unheeded:
        failures.append(
            f"{len(unheeded)} {TABLE} row(s) carry figure_role IS NULL, so nothing says "
            f"whether they assert a value, report a finding about someone else's, or "
            f"state a measurement condition: {unheeded[:10]}"
            + (" …" if len(unheeded) > 10 else ""))

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
    #
    # TOLERANCE MATCHES THE WRITER'S, AND MUST. `db.py derive_extraction` accepts a
    # supplied --claimed-value within 1e-9 of base+delta (db.py: `abs(cn - (bn + dn))
    # > 1e-9`). This check compared with SQL `<>`, i.e. exactly. Binary floating point
    # makes those two rules disagree on ordinary decimals: 0.1 + 0.2 = 0.30000000000000004,
    # so a row the sanctioned writer had just accepted turned this BLOCKING gate red
    # with `stored=0.3, recomputed=0.30000000000000004`. A gate that fails what its own
    # project's writer legitimately produces teaches its reader to route around it.
    # The comparison is done in Python rather than SQL because SQLite has no ABS-based
    # epsilon idiom that stays readable, and the row count here is bounded by the number
    # of derived figures, which is small by construction.
    EPSILON = 1e-9
    view_rows_full = con.execute(
        f"SELECT derived_id, stored, recomputed FROM {VIEW} "
        f"WHERE recomputed IS NOT NULL").fetchall()
    mismatches = [m for m in view_rows_full
                  if abs(float(m["recomputed"]) - float(m["stored"])) > EPSILON]
    if mismatches:
        failures.append(
            f"{len(mismatches)} {VIEW} row(s) disagree with their own base+delta inputs "
            f"by more than {EPSILON}: "
            + ", ".join(f"extraction_id {m['derived_id']} (stored={m['stored']}, "
                        f"recomputed={m['recomputed']})" for m in mismatches))

    # --- 3b. derived rows the VIEW CANNOT SEE -------------------------------
    #
    # CLAUDE.md 5(a) applied to this check's own subject. `v_derived_figure_check`
    # (migration 075) narrows itself with `d.claimed_unit = b.claimed_unit AND
    # d.claimed_unit = e.claimed_unit` and with GLOB tests for plain numerals. Every
    # other derived row is silently ABSENT from the view, so check 3 above reported
    # CLEAN over it having examined nothing -- and the excluded set is exactly the
    # unit-converted rows, which `derive-extraction --claimed-unit --conversion-note`
    # writes deliberately and which are the derived figures MOST likely to be wrong.
    # Demonstrated by an adversarial pass 2026-09-13: a derived row stored as 999 cm
    # against a 0.3 m base+delta produced `VERDICT: CLEAN`.
    #
    # The view is committed in migration 075 and migrations are immutable, so this is
    # the fix-forward: the check derives the full derived set itself and reports the
    # remainder as UNCHECKED rather than passing over it in silence. It is NOT a
    # failure -- a converted figure is legitimate and this check cannot arithmetically
    # verify one without a unit-conversion table the project does not have. Naming the
    # count is what stops a silent CLEAN from reading as a verified one.
    derived_ids = {r["extraction_id"] for r in sve_rows if r["figure_role"] == "derived"}
    covered = {r["derived_id"] for r in con.execute(f"SELECT derived_id FROM {VIEW}")}
    unchecked = sorted(derived_ids - covered)

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

    print(f"UNCHECKED: {len(unchecked)} of {len(derived_ids)} derived row(s) are outside "
          f"{VIEW} (unit-converted, or a value the view's numeric GLOB rejects) and "
          f"CANNOT be arithmetically re-verified here"
          + (f": extraction_id {unchecked}" if unchecked else ""))

    print("VERDICT: " + ("FAIL" if failures else "CLEAN"))
    for f in failures:
        print(f"  * {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
