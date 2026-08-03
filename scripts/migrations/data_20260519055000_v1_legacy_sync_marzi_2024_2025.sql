-- data_20260519055000_v1_legacy_sync_marzi_2024_2025.sql
--
-- v1_legacy synchronization for the two post-cutover rows added 2026-05-17 in
-- session_2026-05-17-pilot-pass-2-sub-1 (Marzi 2024 and Marzi 2025 — REF-00726
-- and REF-00727, both clinical/INT/tier-1 sources for the indoor-comfort BPC).
--
-- Per precedent data_20260515210000 (compensating sync after the 2026-05-15
-- dedup migration), evidence_sources_v1_legacy is treated as a synced shadow
-- of evidence_sources (v1-schema view of the same logical set), not an
-- archaeological freeze. CI checks db_integrity.C05 and db_integrity.D02
-- enforce this. When REF-00726 and REF-00727 were inserted into
-- evidence_sources on 2026-05-17 without parallel inserts into v1_legacy,
-- C05/D02 began failing silently — masked by an unrelated B01 failure
-- introduced 2026-05-19.
--
-- This migration restores parity by inserting the same two rows into
-- v1_legacy under the v1 schema. Column mapping uses the same author/title/
-- doi/tier/jurisdiction/metadata-quality/verification-status pattern as the
-- canonical v1_legacy rows. Fields not in the v1 schema (author_display,
-- journal_name, volume, etc.) are dropped during the projection.
--
-- Forward-only and immutable once committed. If a correction is needed,
-- emit a NEW data migration that compensates.

BEGIN;

INSERT INTO evidence_sources_v1_legacy (
    ref_id, authors, year, title, doi, doi_less_key, pmid,
    tier, evidence_type, jurisdiction, metadata_quality, verification_status,
    co1_provenance, co1_source_type, synthesis_attribution_required, notes,
    created_at, created_by_session, updated_at, updated_by_session,
    derivation_chain, prior_expectation, search_queries_used, doi_resolution_outcome
) VALUES
('REF-00726',
 'Marzi, A.; Caniato, M.; Gasparella, A.',
 '2024',
 'Inclusive indoor comfort of neurodivergent individuals diagnosed before adulthood: A comprehensive study on thermal, acoustic, visual and air quality domains',
 '10.1016/j.buildenv.2024.112254',
 'marzi_2024_inclusive indoor comfort of neurodivergent',
 NULL,
 1, 'clinical', 'INT', 'COMPLETE', 'VERIFIED',
 NULL, NULL, NULL,
 'v1_legacy sync per data_20260519055000; original row created 2026-05-17 in session_2026-05-17-pilot-pass-2-sub-1',
 '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1',
 '2026-05-19 19:30', 'session_2026-05-19-deployment-state-reconciliation',
 NULL, NULL, NULL, 'RESOLVED'),

('REF-00727',
 'Marzi, A.; Caniato, M.; Gasparella, A.',
 '2025',
 'The influence of indoor temperature and noise on autistic individuals',
 '10.1038/s41598-025-02358-4',
 'marzi_2025_the influence of indoor temperature and noise',
 '40442157',
 1, 'clinical', 'INT', 'COMPLETE', 'VERIFIED',
 NULL, NULL, NULL,
 'v1_legacy sync per data_20260519055000; original row created 2026-05-17 in session_2026-05-17-pilot-pass-2-sub-1',
 '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1',
 '2026-05-19 19:30', 'session_2026-05-19-deployment-state-reconciliation',
 NULL, NULL, NULL, 'RESOLVED');

COMMIT;
