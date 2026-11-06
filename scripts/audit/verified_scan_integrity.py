#!/usr/bin/env python3
"""
scripts/audit/verified_scan_integrity.py — does every live extraction rest on a verified source and a reading?

WHY THIS EXISTS (CLAUDE.md section 8: what wrong thing reaches the guidebook). OR-11a
(owner, 2026-10-29): `extraction_status = 'verified'` requires a recorded FULL-scope
`source_scans` reading that covers the row's parameter; the write-time rules add that no
extraction exists for a source that is not VERIFIED, or for a (source, parameter) no reading
covers (contract criterion `verified-reading`). A figure stated over an unverified source, or
one nobody read, reaches a determination looking like any other. `db.py add-extraction` and
`amend-extraction` refuse each state at write time since 2026-11-06; this is the corpus-wide
reader for rows written before that and for any other path. Its readers: the re-reading
worklist (catalogue plan section 7, P3) and the adversarial pass.

EXAMINED is the number of live extraction rows (source not superseded, parameter active).
Three classes, each printed with its sources and its remedy:
  VERIFIED-WITHOUT-FULL-READING  the row is `verified` and no FULL-scope reading covers its
                                 (ref_id, parameter_id): record the reading (record-scan
                                 --text-scope full) or re-grade the row (amend-extraction)
  SOURCE-NOT-VERIFIED            the source's verification_status is not VERIFIED (NULL
                                 included): verify it (correct-source, or amend-source
                                 --field verification_status) or retire the row through the
                                 extraction writers
  NO-COVERING-READING            no source_scans row at ANY scope covers the pair (catalogue
                                 mode with catalogue_version >= parameter_id, or targeted at
                                 the parameter -- the rule v_scan_ledger states): record-scan
A row can sit in more than one class. FAIL when any class is non-empty.

ADVISORY, and red on main while the legacy rows stand (derive: run it). Re-grading them is
a data change, never a hand UPDATE.

Usage: python3 scripts/audit/verified_scan_integrity.py
Exit 0 every class empty; 1 otherwise; 2 cannot run.
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
        cover = ("EXISTS (SELECT 1 FROM source_scans s WHERE s.ref_id = x.ref_id{full} "
                 "AND ((s.mode = 'catalogue' AND s.catalogue_version >= x.parameter_id) "
                 "  OR (s.mode = 'targeted' AND s.target_parameter_id = x.parameter_id)))")
        rows = conn.execute(
            "SELECT x.extraction_id, x.ref_id, x.parameter_id, "
            "  x.extraction_status = 'verified' AND NOT " + cover.format(full=" AND s.text_scope = 'full'") + ", "
            "  COALESCE(e.verification_status, '') <> 'VERIFIED', "
            "  NOT " + cover.format(full="") + " "
            "FROM source_value_extractions x "
            "JOIN evidence_sources e ON e.ref_id = x.ref_id "
            "JOIN base_parameters p ON p.parameter_id = x.parameter_id "
            "WHERE e.superseded_by_ref_id IS NULL AND p.status = 'active' "
            "ORDER BY x.ref_id, x.parameter_id, x.extraction_id"
        ).fetchall()
    finally:
        conn.close()
    classes = (
        ("VERIFIED-WITHOUT-FULL-READING", 3,
         "record the full reading (scripts/research/full_text.py, then db.py record-scan "
         "--text-scope full) or re-grade the row (db.py amend-extraction --field extraction_status)"),
        ("SOURCE-NOT-VERIFIED", 4,
         "verify the source (db.py correct-source, or amend-source --field verification_status) "
         "or retire the row through the extraction writers"),
        ("NO-COVERING-READING", 5,
         "record the reading (db.py record-scan)"),
    )
    print("verified_scan_integrity — every live extraction rests on a VERIFIED source and a reading (OR-11a)")
    print(f"EXAMINED: {len(rows)}")
    if not rows:
        print("NOTHING-IN-SCOPE: no live extraction")
        return 0
    failed = 0
    for name, col, remedy in classes:
        bad = [r for r in rows if r[col]]
        print(f"  {name}: {len(bad)} row(s)")
        by_src = {}
        for r in bad:
            by_src.setdefault(r[1], []).append((r[2], r[0]))
        for ref, items in by_src.items():
            print(f"    {ref}: {len(items)} row(s) (parameter, extraction): "
                  f"{items[:8]}{' ...' if len(items) > 8 else ''}")
        if bad:
            failed += len(bad)
            print(f"    remedy: {remedy}")
    if not failed:
        print("PASS: every live extraction has a VERIFIED source and a covering reading")
        return 0
    print(f"FAIL: {failed} (row, class) pair(s) across {len(rows)} live extraction(s); "
          f"each class above names its remedy.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
