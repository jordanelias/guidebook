#!/usr/bin/env python3
"""
scripts/audit/extraction_follow_up_audit.py — open follow-ups, and live values resting on
one or on a skimmed figure.

WHY THIS EXISTS (tooling T1, 2026-10-09). The owner's answer to D1: "D1: yes figure from
source filed by another slug allowed. skimmed values are not publishable", read with the
earlier "should be yes, but we still tag it for follow up later" (ledger, "Owner
statements 2026-10-09"). So a figure read outside its source's admitting purpose MAY set a
published value while tagged (`db.py raise-follow-up`, extraction_follow_ups), and a
skimmed figure may NOT (assess_cell.NOT_PUBLISHABLE_METHODS). This is the reader of both
answers.

WHAT IT DOES:
  * LISTS every open follow-up (extraction, source, parameter, reason, warrant).
  * FAILS a LIVE determination that has a GOVERNING link to an extraction with an open
    follow-up -- allowed by D1, but the reader must be told, and nothing renders that yet
    (catalogue-plan-v2 section 8.2, "follow-up governing"), so until the render states it
    this is the place it is said.
  * FAILS a live determination governed by a SKIMMED extraction -- the engine refuses to
    produce one, so this is the backstop for rows written by another route. K02 holds the
    same for a row re-marked skim after its determination was stamped.

VACUOUS TODAY, AND SAYS SO. No live determination exists and no follow-up has been raised
(both are counted below on every run), so it examines nothing until research raises the
first follow-up or the engine writes the first live determination. Registered with a
no_floor reason that asserts the subject is empty, so the run that finds a subject flags
that reason as stale -- the registry's own signal to ratchet the floor to min_items: 1.

Usage:
    python3 scripts/audit/extraction_follow_up_audit.py
Exit 0 nothing rests on an open follow-up or a skimmed figure; 1 something does;
2 cannot run.
"""
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))


def main():
    if not DB_PATH.exists():
        print(f"extraction_follow_up_audit: no database at {DB_PATH}", file=sys.stderr)
        return 2
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        if not conn.execute("SELECT 1 FROM sqlite_master WHERE name='extraction_follow_ups'"
                            ).fetchone():
            print("extraction_follow_up_audit: extraction_follow_ups is absent "
                  "(pre-105 schema)", file=sys.stderr)
            return 2
        n_all = conn.execute("SELECT COUNT(*) FROM extraction_follow_ups").fetchone()[0]
        open_rows = conn.execute(
            "SELECT f.follow_up_id, f.extraction_id, x.ref_id, x.parameter_id, f.reason, "
            "f.warrant, f.raised_by_session FROM extraction_follow_ups f "
            "JOIN source_value_extractions x ON x.extraction_id = f.extraction_id "
            "WHERE f.resolved_at IS NULL ORDER BY f.follow_up_id").fetchall()
        n_live = conn.execute("SELECT COUNT(*) FROM specifications "
                              "WHERE retired_at IS NULL").fetchone()[0]
        on_follow_up = conn.execute(
            "SELECT DISTINCT s.specification_id, l.extraction_id, f.follow_up_id "
            "FROM specifications s "
            "JOIN specification_extraction_links l ON l.specification_id = s.specification_id "
            "JOIN extraction_follow_ups f ON f.extraction_id = l.extraction_id "
            "WHERE s.retired_at IS NULL AND l.role = 'governing' AND f.resolved_at IS NULL "
            "ORDER BY 1, 2").fetchall()
        on_skim = conn.execute(
            "SELECT DISTINCT s.specification_id, l.extraction_id "
            "FROM specifications s "
            "JOIN specification_extraction_links l ON l.specification_id = s.specification_id "
            "JOIN source_value_extractions x ON x.extraction_id = l.extraction_id "
            "WHERE s.retired_at IS NULL AND l.role = 'governing' "
            "AND x.extraction_method = 'skim' ORDER BY 1, 2").fetchall()
    finally:
        conn.close()

    print("extraction_follow_up_audit — open follow-ups; live values resting on one")
    print(f"EXAMINED: {n_all + n_live}")
    print(f"  follow-ups: {n_all} raised, {len(open_rows)} open")
    for fid, eid, ref, pid, reason, warrant, by in open_rows[:50]:
        print(f"    follow-up {fid}: extraction {eid} ({ref}, parameter {pid}) {reason} -- "
              f"{warrant[:120]} [raised by {by}]")
    print(f"  live determinations: {n_live}"
          + ("" if n_live else " -- none exists, so the second half examines nothing"))
    bad = False
    for sid, eid, fid in on_follow_up:
        bad = True
        print(f"  FAIL: live determination {sid} is governed by extraction {eid}, which "
              f"has open follow-up {fid}. Allowed (owner D1, 2026-10-09), but the reader "
              f"must be told: state it on the render, or resolve the follow-up "
              f"(db.py resolve-follow-up).")
    for sid, eid in on_skim:
        bad = True
        print(f"  FAIL: live determination {sid} is governed by SKIMMED extraction {eid}. "
              f"Skimmed values are not publishable (owner 2026-10-09); re-run the engine "
              f"(scripts/assess/assess_cell.py) after retiring it.")
    if bad:
        return 1
    print("PASS: no live determination rests on an open follow-up or a skimmed figure")
    return 0


if __name__ == "__main__":
    sys.exit(main())
