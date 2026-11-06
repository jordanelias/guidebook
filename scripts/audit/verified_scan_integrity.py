#!/usr/bin/env python3
"""
scripts/audit/verified_scan_integrity.py — does a `verified` extraction rest on a full reading?

WHY THIS EXISTS (CLAUDE.md section 8: what wrong thing reaches the guidebook). OR-11a
(owner, 2026-10-29): `extraction_status = 'verified'` requires a recorded FULL-scope
`source_scans` reading that covers the row's parameter. The render contract (C5) prints
each row's status as stored and reports the verified rows that lack such a reading, so a
page would otherwise print "verified" over a figure nobody read in full. `db.py
add-extraction` and `amend-extraction` refuse the state at write time since 2026-11-06;
this is the corpus-wide reader for rows written before that, and for any other path.

EXAMINED is the number of live `verified` rows (sources not superseded, parameters
active). A row FAILS when no source_scans row with text_scope='full' covers its
(ref_id, parameter_id) -- catalogue mode with catalogue_version >= parameter_id, or
targeted at the parameter -- the same rule v_scan_ledger and db.py state.

ADVISORY, and red on main while the legacy rows stand (derive: run it). Re-grading them is
a data change: `db.py amend-extraction --field extraction_status --value reviewed` on each,
or a full reading recorded with `record-scan`; never a hand UPDATE.

Usage: python3 scripts/audit/verified_scan_integrity.py
Exit 0 every verified row covered; 1 otherwise; 2 cannot run.
"""
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))


def main():
    if not DB_PATH.exists():
        print(f"verified_scan_integrity: no database at {DB_PATH}", file=sys.stderr)
        return 2
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        if not conn.execute("SELECT 1 FROM sqlite_master WHERE name='source_scans'").fetchone():
            print("verified_scan_integrity: source_scans is absent (pre-103 schema)",
                  file=sys.stderr)
            return 2
        rows = conn.execute(
            "SELECT x.extraction_id, x.ref_id, x.parameter_id, "
            "  EXISTS (SELECT 1 FROM source_scans s WHERE s.ref_id = x.ref_id "
            "          AND s.text_scope = 'full' "
            "          AND ((s.mode = 'catalogue' AND s.catalogue_version >= x.parameter_id) "
            "            OR (s.mode = 'targeted' AND s.target_parameter_id = x.parameter_id))) "
            "FROM source_value_extractions x "
            "JOIN evidence_sources e ON e.ref_id = x.ref_id "
            "JOIN base_parameters p ON p.parameter_id = x.parameter_id "
            "WHERE x.extraction_status = 'verified' AND e.superseded_by_ref_id IS NULL "
            "  AND p.status = 'active' ORDER BY x.ref_id, x.parameter_id, x.extraction_id"
        ).fetchall()
    finally:
        conn.close()
    bad = [r for r in rows if not r[3]]
    print("verified_scan_integrity — every `verified` extraction rests on a full-scope reading (OR-11a)")
    print(f"EXAMINED: {len(rows)}")
    if not rows:
        print("NOTHING-IN-SCOPE: no live verified extraction")
        return 0
    if not bad:
        print("PASS: every verified row has a full-scope covering reading")
        return 0
    by_src = {}
    for eid, ref, pid, _ in bad:
        by_src.setdefault(ref, []).append((pid, eid))
    for ref, items in by_src.items():
        print(f"  {ref}: {len(items)} verified row(s) with no full-scope reading covering them "
              f"(parameter, extraction): {items[:8]}{' ...' if len(items) > 8 else ''}")
    print(f"FAIL: {len(bad)} of {len(rows)} verified row(s) rest on no full-scope reading. Record "
          f"the reading (scripts/research/full_text.py, then db.py record-scan --text-scope full) "
          f"or re-grade the row (db.py amend-extraction --field extraction_status).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
