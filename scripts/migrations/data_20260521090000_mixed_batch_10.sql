-- data_20260521090000_mixed_batch_10.sql
-- Mixed batch 10: 1 academic journal article DOI-verified.
-- REF-00030: Kim et al. 2014 IJIE ramp slope wheelchair

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    doi = '10.1016/j.ergon.2014.07.001',
    pub_title = 'Effects of ramp slope, ramp height and users'' pushing force on performance, muscular activity and subjective ratings during wheelchair driving on a ramp',
    pub_year = 2014,
    first_author_last = 'Kim',
    first_author_first = 'Chung Sik',
    is_corporate_primary = 0,
    author_display = 'Kim, C. S.; Lee, D.; Kwon, S.; Chung, M. K.',
    author_count = 4,
    author_count_is_complete = 1,
    journal_name = 'International Journal of Industrial Ergonomics',
    volume = '44',
    issue = '5',
    pages_start = '636',
    pages_end = '646',
    publisher = 'Elsevier',
    issn = '0169-8141',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-10 2026-05-21T09:00:00Z: web-search identified candidate paper via Crossref author+title search; canonical metadata confirmed (DOI 10.1016/j.ergon.2014.07.001, IJIE 44(5):636-646, 2014). Author = Kim, Chung Sik (Korean, Inha University). Paper directly matches stored claim "Ramp gradient >6% increases propulsion effort" — examines ramp slope vs. muscular activity and pushing force.',
    url = 'https://doi.org/10.1016/j.ergon.2014.07.001',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref-confirm',
    last_verified_at = '2026-05-21T09:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T09:00:00Z mixed-batch-10] Crossref confirmed',
    updated_at = '2026-05-21T09:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00030';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
