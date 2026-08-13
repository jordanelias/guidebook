-- data_20260519060000_dedup_bettarello_2021_app11093942.sql
--
-- Genuine duplicate-DOI group: 10.3390/app11093942 (Bettarello, F. et al.
-- "Indoor Acoustic Requirements for Autism-Friendly Spaces." Applied Sciences,
-- 2021).
--
-- Two ref_ids share this DOI:
--   - REF-00047: legacy ghost. Title field reads "Acoustic thresholds in ASD
--                daily-care facility" (a partial/wrong title) but DOI resolves
--                to the canonical paper. source_type='standard' is also a
--                misclassification (should be 'journal_article'). Created
--                2026-05-08 in session_2026-05-08-c1-migration-fix; backfill
--                paired the wrong title to the correct DOI. verification_note
--                acknowledges the title-DOI pairing on 2026-05-12.
--   - REF-00561: canonical. Full title matches DOI. source_type correct.
--                Manually web-verified 2026-05-16 against MDPI catalog (per
--                verification_note). Used as the "Bettarello precedent" in
--                DR-2026-05-13 §4 demonstrating that even VERIFIED+COMPLETE
--                academic metadata can be wrong (this DOI mismatch was caught
--                by rule #10 sub-rule 2 content-verification).
--
-- Canonical: REF-00561. Repoint REF-00047's downstream rows to REF-00561,
-- then delete REF-00047 from evidence_sources and evidence_sources_v1_legacy
-- (the latter per the v1_legacy-synced-shadow precedent set by
-- data_20260515210000).
--
-- Pattern follows data_20260515200000 verbatim.
--
-- ============================================================================
-- FK PRE-CHECK (verified pre-authoring, 2026-05-19):
--   source_slug_links:        1 row to REPOINT (slug
--                             ndv-aut-built-environment-quantified-thresholds;
--                             no collision — REF-00561 cites a different slug
--                             room-acoustic-performance, so the union is two
--                             slugs, not a duplicate slug-ref_id link)
--   evidence_source_authors:  4 rows to DELETE (canonical REF-00561 retains
--                             its own author rows)
--   evidence_population_match: 0 rows
--   citation_mining:          0 rows
--   reasoning_doc_citations:  0 rows
--   evidence_sources.superseded_by_ref_id: 0 rows point at REF-00047
--   spec_value_probes:        0 rows
--   evidence_sources_v1_legacy: 1 row to DELETE (parallel)
--
-- Net effect:
--   evidence_sources:           671 -> 670 (-1)
--   evidence_sources_v1_legacy: 671 -> 670 (-1)
--   evidence_source_authors:    -4 rows
--   source_slug_links:          repointed (count unchanged)
-- ============================================================================

BEGIN;

-- Repoint downstream rows
UPDATE source_slug_links SET ref_id = 'REF-00561' WHERE ref_id = 'REF-00047';

-- Delete author rows for the non-canonical
DELETE FROM evidence_source_authors WHERE ref_id = 'REF-00047';

-- Delete the non-canonical evidence_sources row
DELETE FROM evidence_sources WHERE ref_id = 'REF-00047';

-- Delete the parallel v1_legacy row per the synced-shadow precedent
-- (data_20260515210000)
DELETE FROM evidence_sources_v1_legacy WHERE ref_id = 'REF-00047';

COMMIT;
