#!/usr/bin/env python3
"""
metadata_integrity_audit.py — Level 2 audit for DR-2026-05-20 protocol.

Three checks:
  1. Inconsistency: COMPLETE / COMPLETE-STATUTORY rows must not carry an open
     MISMATCH-* or DOI-* integrity status. If a row is upgraded to COMPLETE
     but the integrity column says MISMATCH, one of the two writes was wrong.
  2. Coverage: rule #10 eligible rows (COMPLETE+VERIFIED, COMPLETE-STATUTORY+
     VERIFIED/UNVERIFIED-1) without metadata_integrity_status populated are
     legacy rows that pre-date DR-2026-05-20. Surfaced as 'NEEDS-CROSS-CHECK'.
  3. Owner queue surface: rows with metadata_integrity_status NOT IN
     ('OK','RESOLVED', NULL) are the owner-review queue. Counted and bucketed.

Exit code 0 = clean. Exit code 1 = check 1 inconsistency found (data corruption).
Check 2 and 3 surface counts but do not fail (they describe rather than enforce).

Usage:
    python3 scripts/audit/metadata_integrity_audit.py
    GUIDEBOOK_DB_PATH=/path/to/db python3 scripts/audit/metadata_integrity_audit.py
"""
import os
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(os.environ.get(
    "GUIDEBOOK_DB_PATH",
    str(Path(__file__).resolve().parents[2] / "data" / "guidebook.db"),
))


def audit():
    if not DB_PATH.exists():
        print(f"ERROR: DB not found at {DB_PATH}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("=" * 70)
    print("metadata_integrity_audit.py (per DR-2026-05-20)")
    print("=" * 70)
    print()

    exit_code = 0

    # Check 1: inconsistency — COMPLETE rows with open MISMATCH/DOI integrity status.
    rows = c.execute("""
        SELECT ref_id, metadata_quality, verification_status,
               metadata_integrity_status, metadata_integrity_detail
        FROM evidence_sources
        WHERE metadata_quality IN ('COMPLETE', 'COMPLETE-STATUTORY')
          AND metadata_integrity_status IS NOT NULL
          AND metadata_integrity_status NOT IN ('OK', 'RESOLVED')
        ORDER BY ref_id
    """).fetchall()
    if rows:
        print(f"[1] FAIL: {len(rows)} COMPLETE/COMPLETE-STATUTORY rows with open integrity flag")
        for r in rows[:10]:
            print(f"    {r[0]}  mq={r[1]:18s} vs={str(r[2]):10s} mis={r[3]}")
            print(f"      detail: {(r[4] or '')[:100]}")
        if len(rows) > 10:
            print(f"    ... ({len(rows) - 10} more)")
        exit_code = 1
    else:
        print("[1] PASS: No COMPLETE rows with open integrity flags")

    # Check 2: coverage — rule #10 eligible rows without integrity probe recorded.
    legacy = c.execute("""
        SELECT COUNT(*)
        FROM evidence_sources
        WHERE metadata_quality IN ('COMPLETE', 'COMPLETE-STATUTORY')
          AND verification_status IN ('VERIFIED', 'UNVERIFIED-1')
          AND metadata_integrity_status IS NULL
    """).fetchone()[0]
    eligible_total = c.execute("""
        SELECT COUNT(*)
        FROM evidence_sources
        WHERE metadata_quality IN ('COMPLETE', 'COMPLETE-STATUTORY')
          AND verification_status IN ('VERIFIED', 'UNVERIFIED-1')
    """).fetchone()[0]
    pct = 100 * legacy / eligible_total if eligible_total else 0
    print(f"[2] INFO: {legacy} / {eligible_total} eligible rows lack a cross-check record "
          f"({pct:.1f}% — pre-DR-2026-05-20 legacy)")
    if legacy:
        print("    These rows cleared rule #10's existence gate but predate the cross-check")
        print("    protocol. Future synthesis claims on these rows should run cross-check first.")

    # Check 3: owner-review queue surface.
    print()
    print("[3] INFO: Owner-review queue (metadata_integrity_status NOT IN ('OK','RESOLVED',NULL))")
    queue = c.execute("""
        SELECT metadata_integrity_status, COUNT(*)
        FROM evidence_sources
        WHERE metadata_integrity_status IS NOT NULL
          AND metadata_integrity_status NOT IN ('OK', 'RESOLVED')
        GROUP BY metadata_integrity_status
        ORDER BY COUNT(*) DESC
    """).fetchall()
    queue_total = sum(r[1] for r in queue)
    print(f"    Total: {queue_total} rows")
    for status, n in queue:
        print(f"      {status:25s} {n}")

    print()
    print("=" * 70)
    print(f"VERDICT: {'PASS' if exit_code == 0 else 'FAIL'}")
    print("=" * 70)
    return exit_code


if __name__ == "__main__":
    sys.exit(audit())
