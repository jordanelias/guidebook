-- data_20260521110000_books_batch_14.sql
-- Books batch 14: 1 OT textbook ISBN-verified.
-- REF-00177: Townsend E.A. & Polatajko H.J. (2007) Enabling Occupation II, CAOT, Ottawa.

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    pub_title = 'Enabling Occupation II: Advancing an Occupational Therapy Vision for Health, Well-being, & Justice through Occupation',
    pub_year = 2007,
    first_author_last = 'Townsend',
    first_author_first = 'Elizabeth A.',
    is_corporate_primary = 0,
    author_display = 'Townsend, E. A.; Polatajko, H. J.',
    author_count = 2,
    author_count_is_complete = 1,
    publisher = 'CAOT Publications ACE (Canadian Association of Occupational Therapists), Ottawa, Ontario',
    isbn = '9781895437768',
    pages_start = 'xxiii',
    pages_end = '418',
    jurisdiction = 'CA',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'NO-MATCH',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'ca-batch-14 2026-05-21T11:00:00Z: web-search verified via Amazon + Internet Archive + CAOT + WorldCat (OCLC 988818041). 1st edition published 2007 (ISBN 9781895437768). 2nd edition 2013 (ISBN 9781895437898). The 9th Canadian Occupational Therapy Guidelines. Introduces CMOP-E (Canadian Model of Occupational Performance and Engagement), CMCE (Canadian Model of Client-Centred Enablement), and CPPF (Canadian Practice Process Framework).',
    url = 'https://archive.org/details/enablingoccupati0000town',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+worldcat-isbn',
    last_verified_at = '2026-05-21T11:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T11:00:00Z ca-batch-14] web-search + ISBN verified',
    updated_at = '2026-05-21T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00177';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
