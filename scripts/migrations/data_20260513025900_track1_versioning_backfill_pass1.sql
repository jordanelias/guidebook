-- data_20260513025900_track1_versioning_backfill_pass1.sql
-- Track 1 first pass per DR-2026-05-13: populate `edition` on records
-- with `verified_by_tool = 'publisher-catalog-fetch'` by extracting year/date
-- suffix from `standard_number` (falls back to `pub_year` when no suffix present).
--
-- Idempotent via WHERE edition IS NULL guard.
-- `superseded_by_ref_id` deferred per standing rule #1 (source discipline).

UPDATE evidence_sources SET edition = '2019', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00015' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2011-10', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00018' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2022', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00050' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2022', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00130' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2010', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00142' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2011', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00144' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2019', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00199' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2011', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00207' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2018', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00209' AND edition IS NULL;
UPDATE evidence_sources SET edition = '1992', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00211' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2018', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00249' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2010', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00320' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2011', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00323' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2016', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00329' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2018', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00330' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2016', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00351' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2018', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00358' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2021', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00361' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2018', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00406' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2010', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00409' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2011', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00412' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2021', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00417' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2021', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00420' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2010', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00422' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2010', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00429' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2018', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00430' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2011', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00431' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2021', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00436' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2021', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00441' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2010', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00443' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2018', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00444' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2010', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00445' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2021', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00446' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2021', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00453' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2019', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00506' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2021', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00515' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2022', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00516' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2021', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00532' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2018', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00533' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2016', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00540' AND edition IS NULL;
UPDATE evidence_sources SET edition = '2022', updated_at = '2026-05-13T03:00:00Z', updated_by_session = 'session_2026-05-13b-evidence-verification-methodology' WHERE ref_id = 'REF-00568' AND edition IS NULL;
