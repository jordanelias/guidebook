-- data_20260515210000_2026-05-15-v1-legacy-dedup-sync.sql
-- Compensating data migration to data_20260515200000_2026-05-15-duplicate-doi-dedup.sql.
--
-- This file is forward-only and immutable once committed.
--
-- ============================================================================
-- BACKGROUND
-- ============================================================================
--
-- The preceding dedup migration (timestamp 20260515200000) deleted 6 duplicate
-- non-canonical rows from evidence_sources but left evidence_sources_v1_legacy
-- untouched, on the basis that v1_legacy is a historical snapshot.
--
-- CI check `db_integrity.C05` and `db_integrity.D02` rejected this:
--   C05: evidence_sources row count matches v1_legacy
--   D02: evidence_sources and v1_legacy have matching ref_id sets
--
-- The CI checks are authoritative on the project's actual treatment of v1_legacy
-- as a synced shadow (v1-schema view of the same logical set), not an
-- archaeological freeze. This migration synchronizes v1_legacy by deleting the
-- same 6 non-canonical ref_ids that 20260515200000 removed from evidence_sources.
--
-- The retained canonical ref_ids in v1_legacy preserve the v1-schema row for
-- the deduplicated DOI's authoritative representative.
--
-- ============================================================================

BEGIN;

DELETE FROM evidence_sources_v1_legacy
WHERE ref_id IN (
    'REF-00046',  -- DOI 10.3390/ijerph18063203, dedup'd to canonical REF-00710
    'REF-00490',  -- DOI 10.3390/ijerph18063203, dedup'd to canonical REF-00710
    'REF-00546',  -- DOI 10.3390/ijerph18063203, dedup'd to canonical REF-00710
    'REF-00154',  -- DOI 10.1371/journal.pone.0291228, dedup'd to canonical REF-00006
    'REF-00455',  -- DOI 10.3233/978-1-61499-684-2-612, dedup'd to canonical REF-00204
    'REF-00023'   -- DOI 10.1080/10400430903520280, dedup'd to canonical REF-00060
);

COMMIT;
