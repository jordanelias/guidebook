#!/usr/bin/env python3
"""
Migration 011: reasoning_doc_citations table (Track 3 of DR-2026-05-13)
========================================================================
Date: 2026-05-13
Session: session_2026-05-13b-evidence-verification-methodology
Adopted via: DR-2026-05-13 §4 Track 3

Scope
-----
Create the `reasoning_doc_citations` table that records per-cell content
verification of claims in BPC reasoning documents. Supports the sharpened
standing rule #10 sub-rules 2 (jurisdiction-comparison cells) and 3
(qualitative/definitional claims). PMP (rule #8) continues to handle
numerical-spec claims via `spec_value_probes`.

Design
------
Single table with `claim_type` enum covering all four claim categories.
CHECK constraint enforces that the appropriate value/match fields are
populated per claim type. Forward-compatible with future split if needed
(per DR-2026-05-13 §12.1 adoption answer).

`paywall_purchase_candidate` flag (default 0) supports periodic owner
review for high-leverage paywalled-source purchase decisions, per
DR-2026-05-13 §12.2 adoption answer.

Verification
------------
- BEFORE: table does not exist.
- AFTER: table exists, four indexes exist, CHECK constraints work.
- AFTER: insert/reject tests confirm constraints fire correctly.
- AFTER: user_version advances from 10 to 11.

Reversibility
-------------
DROP TABLE removes the table cleanly. New table is empty at end of migration.
"""
import sqlite3
import sys


DB_PATH = sys.argv[1] if len(sys.argv) > 1 else "/tmp/guidebook.db"


REASONING_DOC_CITATIONS = """
CREATE TABLE reasoning_doc_citations (
    citation_id          TEXT PRIMARY KEY,
    reasoning_doc_slug   TEXT NOT NULL,
    parameter            TEXT NOT NULL,
    jurisdiction         TEXT,
    population           TEXT,
    claim_type           TEXT NOT NULL CHECK(claim_type IN (
        'numerical_spec','jurisdiction_value','qualitative','definitional'
    )),
    claimed_value        TEXT,
    claimed_unit         TEXT,
    claim_text           TEXT,
    source_ref_id        TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    source_section       TEXT,
    value_match          TEXT CHECK(value_match IN (
        'EXACT','WITHIN-TOLERANCE','DIFFERENT','NOT-FOUND','PAYWALL','SUPERSEDED'
    )),
    claim_match          TEXT CHECK(claim_match IN (
        'SUPPORTED','PARTIAL','NOT-FOUND','PAYWALL','CONTRADICTED'
    )),
    verified_at          TEXT NOT NULL,
    verified_by_session  TEXT NOT NULL,
    paywall_purchase_candidate INTEGER NOT NULL DEFAULT 0 CHECK(paywall_purchase_candidate IN (0,1)),
    notes                TEXT,
    CHECK (
      (claim_type IN ('numerical_spec','jurisdiction_value') AND claimed_value IS NOT NULL AND value_match IS NOT NULL) OR
      (claim_type IN ('qualitative','definitional') AND claim_text IS NOT NULL AND claim_match IS NOT NULL)
    )
)
"""

INDEXES = [
    "CREATE INDEX idx_rdc_slug_param  ON reasoning_doc_citations(reasoning_doc_slug, parameter)",
    "CREATE INDEX idx_rdc_ref         ON reasoning_doc_citations(source_ref_id)",
    "CREATE INDEX idx_rdc_claim_type  ON reasoning_doc_citations(claim_type)",
    "CREATE INDEX idx_rdc_paywall     ON reasoning_doc_citations(paywall_purchase_candidate) WHERE paywall_purchase_candidate = 1",
]


def main() -> int:
    db = sqlite3.connect(DB_PATH)
    db.isolation_level = None

    print(f"Migration 011 against: {DB_PATH}")
    print("=" * 60)

    pre_uv = db.execute("PRAGMA user_version").fetchone()[0]
    print(f"Pre user_version: {pre_uv}")
    if pre_uv != 10:
        print(f"  HALT: expected user_version=10 (run migration 007 first), found {pre_uv}")
        return 1

    exists = db.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='reasoning_doc_citations'").fetchone()[0]
    if exists:
        print("  HALT: reasoning_doc_citations table already exists")
        return 1

    db.execute("PRAGMA foreign_keys = ON")
    db.execute("BEGIN")
    try:
        db.execute(REASONING_DOC_CITATIONS)
        for idx in INDEXES:
            db.execute(idx)
        db.execute("""INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes)
                      VALUES ('011_reasoning_doc_citations_2026-05-13',
                              datetime('now'),
                              'create_reasoning_doc_citations_table_4_indexes_track3_dr_2026-05-13',
                              'session_2026-05-13b-evidence-verification-methodology',
                              'Track 3 of DR-2026-05-13: create reasoning_doc_citations table with claim_type enum covering numerical, jurisdictional, qualitative, definitional claims. 4 indexes. Backs the sharpened rule #10 sub-rules 2 and 3.')""")
        db.execute("COMMIT")
    except Exception as e:
        db.execute("ROLLBACK")
        print(f"  HALT: exception, rolled back: {e}")
        return 1

    db.execute("PRAGMA user_version = 11")

    # Verify
    post_uv = db.execute("PRAGMA user_version").fetchone()[0]
    print(f"Post user_version: {post_uv}")
    if post_uv != 11:
        return 1

    cols = [c[1] for c in db.execute("PRAGMA table_info(reasoning_doc_citations)")]
    expected_cols = {"citation_id", "reasoning_doc_slug", "parameter", "jurisdiction", "population",
                     "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_ref_id",
                     "source_section", "value_match", "claim_match", "verified_at",
                     "verified_by_session", "paywall_purchase_candidate", "notes"}
    print(f"Columns: {sorted(cols)}")
    missing = expected_cols - set(cols)
    if missing:
        print(f"  HALT: missing columns: {missing}")
        return 1

    idx_count = db.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name='reasoning_doc_citations'").fetchone()[0]
    print(f"Indexes on reasoning_doc_citations: {idx_count} (expected ≥4)")
    if idx_count < 4:
        return 1

    # Test CHECK constraints: insert a valid numerical_spec row, then a valid qualitative row,
    # then prove the cross-constraint fires by attempting an invalid one.
    test_es = db.execute("SELECT ref_id FROM evidence_sources LIMIT 1").fetchone()[0]
    print(f"Constraint tests using source_ref_id={test_es}")

    db.execute("BEGIN")
    try:
        db.execute("""INSERT INTO reasoning_doc_citations
                        (citation_id, reasoning_doc_slug, parameter, jurisdiction, population,
                         claim_type, claimed_value, claimed_unit, source_ref_id, source_section,
                         value_match, verified_at, verified_by_session)
                      VALUES ('TEST-NUM', 'test-slug', 'corridor_width', 'AU', 'wheelchair-user',
                              'jurisdiction_value', '1200', 'mm', ?, '§7.2',
                              'EXACT', datetime('now'), 'session_2026-05-13b-evidence-verification-methodology')""",
                   (test_es,))

        db.execute("""INSERT INTO reasoning_doc_citations
                        (citation_id, reasoning_doc_slug, parameter, population,
                         claim_type, claim_text, source_ref_id, source_section,
                         claim_match, verified_at, verified_by_session)
                      VALUES ('TEST-QUAL', 'test-slug', 'visual_markers', 'low-vision',
                              'qualitative', 'high-contrast visual markers improve wayfinding for low-vision users',
                              ?, '§3.4',
                              'SUPPORTED', datetime('now'), 'session_2026-05-13b-evidence-verification-methodology')""",
                   (test_es,))

        # This should fail: jurisdiction_value but missing claimed_value
        try:
            db.execute("""INSERT INTO reasoning_doc_citations
                            (citation_id, reasoning_doc_slug, parameter, claim_type, source_ref_id,
                             verified_at, verified_by_session)
                          VALUES ('TEST-BAD', 'test-slug', 'corridor_width', 'jurisdiction_value', ?,
                                  datetime('now'), 'session_2026-05-13b-evidence-verification-methodology')""",
                       (test_es,))
            print("  HALT: CHECK constraint did not fire for missing claimed_value")
            db.execute("ROLLBACK")
            return 1
        except sqlite3.IntegrityError:
            print("  CHECK constraint correctly rejected bad row")

        # Roll back the test inserts so the table starts empty for real use
        db.execute("ROLLBACK")
    except Exception as e:
        db.execute("ROLLBACK")
        print(f"  HALT: constraint test failed: {e}")
        return 1

    post_count = db.execute("SELECT COUNT(*) FROM reasoning_doc_citations").fetchone()[0]
    print(f"Final row count: {post_count} (expected 0)")
    if post_count != 0:
        return 1

    print("=" * 60)
    print("Migration 011 SUCCESS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
