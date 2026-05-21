-- data_20260521141000_batch_19_fixup.sql
-- Fixup for batch 19 D01/G02 audit failures:
--   D01: REF-00090's new DOI 10.3390/ijerph192114279 collides with REF-00527 (same paper)
--   G02: REF-00090 needs evidence_source_authors rows
--
-- Resolution: insert Owen + Crane as authors for REF-00090; flag REF-00090 + REF-00527
-- as a duplicate pair. NOTE: REF-00527 stores 'Crane, Jasmine' but the PMC9658651
-- source (verified live 2026-05-21) lists 'James Crane' as co-author. Owner-queue.

BEGIN TRANSACTION;

-- Insert author rows for REF-00090
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, is_corporate, role, created_at, created_by_session) VALUES
  ('REF-00090', 1, 'Owen', 'Ceridwen', 0, 'author', '2026-05-21T14:10:00Z', 'session_2026-05-20-ato-rehab'),
  ('REF-00090', 2, 'Crane', 'James', 0, 'author', '2026-05-21T14:10:00Z', 'session_2026-05-20-ato-rehab');

-- Flag REF-00090 + REF-00527 as potential duplicate pair
UPDATE evidence_sources SET
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00527',
    metadata_integrity_detail = 'batch-19-fixup 2026-05-21T14:10:00Z: REF-00090 shares DOI 10.3390/ijerph192114279 with REF-00527 (both cite Owen & Crane 2022 TID scoping review IJERPH 19(21):14279). Owner-queue: REF-00527 stored Crane first name as ''Jasmine''; PMC9658651 lists ''James Crane''. Verify and either correct REF-00527 or determine if REF-00527 references a different work. Both rows added to KNOWN_DUP_DOIS allowlist meanwhile.',
    updated_at = '2026-05-21T14:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00090';

UPDATE evidence_sources SET
    metadata_integrity_status = COALESCE(metadata_integrity_status, '') || ' | POTENTIAL-DUPLICATE-OF-REF-00090',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | batch-19-fixup 2026-05-21T14:10:00Z: shares DOI with REF-00090. Note: stored Crane first name ''Jasmine'' may be wrong — PMC9658651 source lists ''James Crane''. Owner-queue.',
    updated_at = '2026-05-21T14:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00527';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
