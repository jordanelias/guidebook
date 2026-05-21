-- data_20260520231500_v1_legacy_sync_for_attribution_correction.sql
-- Companion to data_20260520230000_wrong_attribution_correction.sql.
-- Syncs evidence_sources_v1_legacy to include the 3 new rows (REF-00728/729/730)
-- created by the wrong-attribution correction migration. Restores C05/D02 db_integrity.

BEGIN TRANSACTION;

INSERT INTO evidence_sources_v1_legacy (
    ref_id, authors, year, title, doi, doi_less_key, pmid,
    tier, evidence_type, jurisdiction, metadata_quality, verification_status,
    notes, created_at, created_by_session, updated_at, updated_by_session
) VALUES
('REF-00728', 'Keall, M. et al.', '2021',
 'MHIPI study. Lancet Public Health 6:e631–e640',
 NULL, 'keall_2021_mhipi study. lancet public health', NULL,
 3, 'clinical', 'NZ', 'AUTHOR-TITLE-ONLY', NULL,
 'Displaced from REF-00069 by wrong-attribution-correction 2026-05-20',
 '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab',
 '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00729', 'Faerden, A.', '2022',
 'Single rooms and patient control in inpatient mental health',
 NULL, 'faerden_2022_single rooms and patient control in inpatient', NULL,
 3, 'clinical', 'NO', 'AUTHOR-TITLE-ONLY', NULL,
 'Displaced from REF-00096 by wrong-attribution-correction 2026-05-20',
 '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab',
 '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00730', 'Harper, S.A.', '2022',
 'Stairway Visual Contrast Enhancement to Reduce Fall-Related Injuries',
 NULL, 'harper_2022_stairway visual contrast enhancement to reduce', NULL,
 3, 'clinical', 'US', 'AUTHOR-TITLE-ONLY', NULL,
 'Displaced from REF-00527 by wrong-attribution-correction 2026-05-20',
 '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab',
 '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab');

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
