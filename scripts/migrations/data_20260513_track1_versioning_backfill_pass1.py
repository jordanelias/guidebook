#!/usr/bin/env python3
"""
Track 1 versioning backfill (first pass)
=========================================
Date: 2026-05-13
Session: session_2026-05-13b-evidence-verification-methodology
Per: DR-2026-05-13 §4 Track 1

Scope (first pass)
------------------
For the 41 records with `verified_by_tool = 'publisher-catalog-fetch'`,
populate `edition` from the publication-date suffix in `standard_number`
(or fall back to `pub_year` as string if no suffix).

`superseded_by_ref_id` is NOT auto-populated in this first pass. Of the 12
records with supersession info in their verification_note:
- REF-00018 (DIN 32984:2011-10) — superseded by 2020-12 / 2023-04, neither in DB
- REF-00211 (AS 1428.2:1992) — likely superseded, successor not in DB
- BS 8300-2:2018 records — these ARE the new edition; predecessor BS 8300:2009 not in DB
- AS 1428.1:2021 records — these ARE the new edition; predecessor AS 1428.1:2009 not in DB

Per standing rule #1 (source discipline: "I don't know" > invention), no
inference is made beyond what is unambiguously supported by data in-DB.
Successor records not yet in the DB are an honest gap to be addressed
in a future Phase B subtask.

Yield
-----
- `edition` populated on up to 41 records (one per publisher-catalog-fetch record)
- `superseded_by_ref_id`: 0 records this pass
- Recorded in `data_migrations` as track-1-pass-1.

Reversibility
-------------
Each UPDATE only writes to `edition` where it is currently NULL. To revert,
SET edition=NULL on rows updated by this session. The pre-backfill DB
is at /tmp/guidebook.db.pre-mig008 (pre-007 is at .pre-mig007).
"""
import re
import sqlite3
import sys


DB_PATH = sys.argv[1] if len(sys.argv) > 1 else "/tmp/guidebook.db"
SESSION = "session_2026-05-13b-evidence-verification-methodology"


def extract_edition(standard_number: str | None, pub_year: int | None) -> str | None:
    """Extract an edition string from standard_number; fall back to pub_year."""
    if not standard_number:
        return str(pub_year) if pub_year else None
    # Patterns to match (order matters; most specific first):
    # 'DIN 32984:2011-10'  -> '2011-10'
    # 'ISO 23599:2019'     -> '2019'
    # 'AS 1428.1:2021'     -> '2021'
    # 'BS 8300-2:2018'     -> '2018'
    # 'DIN 18040-2:2023'   -> '2023'
    # 'ADA Standards 2010' -> '2010'    (no colon)
    # 'DIN 18040-2'        -> None      (no year suffix; use pub_year)
    m = re.search(r":(\d{4}(?:-\d{2})?)\b", standard_number)
    if m:
        return m.group(1)
    m = re.search(r"\b(\d{4})\b", standard_number)
    if m:
        return m.group(1)
    return str(pub_year) if pub_year else None


def main() -> int:
    db = sqlite3.connect(DB_PATH)
    db.isolation_level = None

    print(f"Track 1 versioning backfill against: {DB_PATH}")
    print("=" * 60)

    uv = db.execute("PRAGMA user_version").fetchone()[0]
    print(f"user_version: {uv}")
    if uv < 11:
        print(f"  HALT: expected user_version>=11, found {uv}. Run migrations 007 and 008 first.")
        return 1

    # Fetch candidate records
    rows = list(db.execute("""
        SELECT ref_id, standard_number, pub_year, edition
        FROM evidence_sources
        WHERE verified_by_tool = 'publisher-catalog-fetch'
        ORDER BY ref_id
    """))
    print(f"Candidate records (publisher-catalog-fetch): {len(rows)}")

    skipped_already_set = 0
    skipped_no_value = 0
    updated = []

    db.execute("PRAGMA foreign_keys = ON")
    db.execute("BEGIN")
    try:
        for ref_id, std, py, ed_current in rows:
            if ed_current:
                skipped_already_set += 1
                continue
            ed_new = extract_edition(std, py)
            if not ed_new:
                skipped_no_value += 1
                continue
            db.execute("""UPDATE evidence_sources
                          SET edition = ?, updated_at = datetime('now'), updated_by_session = ?
                          WHERE ref_id = ? AND edition IS NULL""",
                       (ed_new, SESSION, ref_id))
            updated.append((ref_id, std, ed_new))

        db.execute("""INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes)
                      VALUES ('track1_backfill_pass1_2026-05-13',
                              datetime('now'),
                              'edition_backfill_from_standard_number_publisher_catalog_fetch_41_records',
                              ?,
                              ?)""",
                   (SESSION,
                    f"Track 1 first pass per DR-2026-05-13: edition populated on {len(updated)} publisher-catalog-fetch records by extracting year/date from standard_number. superseded_by_ref_id NOT auto-populated in this pass; deferred to manual review per rule #1."))
        db.execute("COMMIT")
    except Exception as e:
        db.execute("ROLLBACK")
        print(f"  HALT: rolled back: {e}")
        return 1

    print(f"Updated: {len(updated)}")
    print(f"Skipped (edition already set): {skipped_already_set}")
    print(f"Skipped (no extractable value): {skipped_no_value}")
    print()
    print("=== First 15 updates ===")
    for r in updated[:15]:
        print(f"  {r[0]} | std='{r[1]}' | edition='{r[2]}'")
    if len(updated) > 15:
        print(f"  ... and {len(updated)-15} more")

    # Verify
    print()
    populated = db.execute("SELECT COUNT(*) FROM evidence_sources WHERE edition IS NOT NULL").fetchone()[0]
    print(f"Total evidence_sources with edition populated: {populated} (was 1 at v10.9 audit)")

    print("=" * 60)
    print("Track 1 first pass SUCCESS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
