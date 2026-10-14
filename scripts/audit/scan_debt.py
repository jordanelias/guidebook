#!/usr/bin/env python3
"""
scripts/audit/scan_debt.py — which (source, parameter) pairs nobody has read in full?

WHY THIS EXISTS (tooling T1, 2026-10-09; catalogue-plan-v2 sections 3.8 and 8.2). The
owner's requirement: "Ensure that we can add and expand parameter catalogue as required
based on new information we come across." A parameter promoted in month three is owed a
look in month one's sources, and nothing showed that debt: the catalogue could imply "no
code sets a requirement" where nobody read the code for that quantity, while every gate
read green -- how GAP-061's figures were lost. `v_scan_ledger` (migration 103) derives a
status for every unsuperseded source x active parameter from the extractions and the
reading record (source_scans); this counts the pairs still owed.

DEBT = NOT-READ + READ-PARTIAL pairs. EXTRACTED, STATED-ABSENT and READ-NOTHING-FOUND are
accounted for. READ-PARTIAL is debt because a partial, fragment or abstract reading cannot
say a quantity is absent from the pages it did not see.

NO DEBT BASELINE, deliberately (the "no floor" this check was asked for). Debt RISES
legitimately -- every parameter promoted and every source admitted adds pairs -- so a
ratchet-down baseline would turn red on correct work. It is advisory and red whenever
debt > 0: the honest state of a catalogue that has not been read. Its readers: the next
cohort's worklist (the pairs printed below), the catalogue's evidence-state line, and the
Release 0 acceptance test (plan section 12, Q12), which will scope it to that source set.

EXAMINED is the number of ledger pairs. Zero pairs means no unsuperseded source or no
active parameter -- a corpus clear, which this project has done once (2026-09-13) -- and
the registry floor (min_items: 1) makes that visible rather than a silent pass.

Usage:
    python3 scripts/audit/scan_debt.py [--limit N]
Exit 0 no debt; 1 debt; 2 cannot run (no database, or a pre-103 schema).
"""
import argparse
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))
DEBT = ("NOT-READ", "READ-PARTIAL")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--limit", type=int, default=20,
                    help="how many owed pairs to list per parameter (default 20)")
    args = ap.parse_args()
    if not DB_PATH.exists():
        print(f"scan_debt: no database at {DB_PATH}", file=sys.stderr)
        return 2
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        if not conn.execute("SELECT 1 FROM sqlite_master WHERE name='v_scan_ledger'"
                            ).fetchone():
            print("scan_debt: v_scan_ledger is absent (pre-103 schema)", file=sys.stderr)
            return 2
        status = dict(conn.execute("SELECT status, COUNT(*) FROM v_scan_ledger "
                                   "GROUP BY status").fetchall())
        per_param = conn.execute(
            "SELECT l.parameter_id, t.canonical_en, "
            "SUM(l.status = 'NOT-READ'), SUM(l.status = 'READ-PARTIAL') "
            "FROM v_scan_ledger l JOIN base_parameters p USING (parameter_id) "
            "JOIN terms t ON t.term_id = p.term_id "
            "GROUP BY l.parameter_id ORDER BY l.parameter_id").fetchall()
        owed = conn.execute(
            "SELECT parameter_id, ref_id, status FROM v_scan_ledger WHERE status IN (?, ?) "
            "ORDER BY parameter_id, ref_id", DEBT).fetchall()
    finally:
        conn.close()

    total = sum(status.values())
    debt = sum(status.get(s, 0) for s in DEBT)
    print("scan_debt — (source x active parameter) pairs not yet read in full")
    print(f"EXAMINED: {total}")
    for s in ("EXTRACTED", "STATED-ABSENT", "READ-NOTHING-FOUND", "READ-PARTIAL",
              "NOT-READ"):
        print(f"  {s:<19} {status.get(s, 0)}")
    if not debt:
        print("PASS: every pair is extracted, stated absent, or read in full")
        return 0
    for pid, name, not_read, partial in per_param:
        if not_read or partial:
            refs = [r for p, r, _s in owed if p == pid]
            print(f"  parameter {pid} ({name}): {not_read} not read, {partial} read only "
                  f"partially -- {', '.join(refs[:args.limit])}"
                  + (" ..." if len(refs) > args.limit else ""))
    print(f"DEBT: {debt} pair(s). Read each source against the whole list and record it "
          f"(db.py record-scan; scripts/research/full_text.py derives a held PDF's text), or "
          f"a targeted reading for one new parameter (record-scan --mode targeted).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
