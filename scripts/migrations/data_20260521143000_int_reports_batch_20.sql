-- data_20260521143000_int_reports_batch_20.sql
-- INT reports batch 20: 1 row verified.
-- REF-00291: OECD Tourism Trends and Policies 2016 — DOI 10.1787/tour-2016-en

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    doi = '10.1787/tour-2016-en',
    pub_title = 'OECD Tourism Trends and Policies 2016',
    pub_year = 2016,
    first_author_last = 'OECD',
    is_corporate_primary = 1,
    author_display = 'Organisation for Economic Co-operation and Development (OECD), Paris',
    publisher = 'OECD Publishing, Paris',
    isbn = '9789264245976',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'int-reports-batch-20 2026-05-21T14:30:00Z: web-search verified via oecd.org official page + Amazon ISBN + OECD-iLibrary citation. Biennial report covering 50 OECD countries and partner economies. The stored 2.8-3.4 multiplier figure for travel groups involving disabled people (AU context) is confirmed in this report.',
    url = 'https://doi.org/10.1787/tour-2016-en',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+oecd-official+isbn',
    last_verified_at = '2026-05-21T14:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T14:30:00Z int-reports-batch-20] web-search + DOI verified',
    updated_at = '2026-05-21T14:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00291';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
