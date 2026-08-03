-- data_20260521080000_books_batch_8.sql
--
-- Books batch 8: 3 classic academic books — wrong-DOI-cleared rows now ISBN-verified.
-- Per DR-2026-05-18: for academic books, ISBN + publisher + edition serves as the
-- audit-trail identifier (equivalent role to DOI for journal articles).
--
-- REF-00176: Barker R.G. (1968) Ecological Psychology, Stanford University Press
-- REF-00478: Passini R. (1984) Wayfinding in Architecture, Van Nostrand Reinhold
-- REF-00485: Kaplan R. & Kaplan S. (1989) The Experience of Nature, Cambridge University Press

BEGIN TRANSACTION;

-- REF-00176: Barker 1968
UPDATE evidence_sources SET
    pub_title = 'Ecological Psychology: Concepts and Methods for Studying the Environment of Human Behavior',
    pub_year = 1968,
    first_author_last = 'Barker',
    first_author_first = 'Roger G.',
    is_corporate_primary = 0,
    author_display = 'Barker, R. G.',
    author_count = 1,
    author_count_is_complete = 1,
    publisher = 'Stanford University Press',
    isbn = '9780804706582',
    pages_start = 'x',
    pages_end = '242',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'books-batch-8 2026-05-21T08:00:00Z: web-search verified via Stanford University Press + Amazon + Open Library + Wikipedia citation. Hardcover, October 1968. ISBN-13 9780804706582, ISBN-10 0804706581. 242 pages. Foundational text on behavior-setting theory and ecological psychology. Revised/extended 1989 by Phil Schoggen under different title "Behavior Settings" (ISBN 9780804715430). Stored row was WRONG-DOI-CLEARED earlier this session; DOI not applicable to 1968 book — ISBN is the canonical identifier.',
    url = 'https://www.sup.org/books/cite/?id=2200',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+sup-amazon-openlibrary',
    last_verified_at = '2026-05-21T08:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T08:00:00Z books-batch-8] web-search + ISBN verified',
    updated_at = '2026-05-21T08:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00176';

-- REF-00478: Passini 1984
UPDATE evidence_sources SET
    pub_title = 'Wayfinding in Architecture',
    pub_year = 1984,
    first_author_last = 'Passini',
    first_author_first = 'Romedi',
    is_corporate_primary = 0,
    author_display = 'Passini, R.',
    author_count = 1,
    author_count_is_complete = 1,
    publisher = 'Van Nostrand Reinhold Company, New York',
    isbn = '9780442275907',
    pages_start = 'x',
    pages_end = '229',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'books-batch-8 2026-05-21T08:00:00Z: web-search verified via WorldCat (OCLC 10324959) + Abebooks + Biblio + multiple citation references. 1st edition 1984; Environmental Design Series Vol. 4. ISBN-13 9780442275907 (hardcover); paperback 9780442010959 (1992 reprint). x + 229 pages. Foundational wayfinding text; led to author''s 1992 collaboration with Paul Arthur on "Wayfinding: People, Signs and Architecture". Stored row was WRONG-DOI-CLEARED; DOI not applicable — ISBN is the canonical identifier.',
    url = 'https://search.worldcat.org/title/Wayfinding-in-architecture/oclc/10324959',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+worldcat-abebooks',
    last_verified_at = '2026-05-21T08:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T08:00:00Z books-batch-8] web-search + ISBN verified',
    updated_at = '2026-05-21T08:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00478';

-- REF-00485: Kaplan & Kaplan 1989
UPDATE evidence_sources SET
    pub_title = 'The Experience of Nature: A Psychological Perspective',
    pub_year = 1989,
    first_author_last = 'Kaplan',
    first_author_first = 'Rachel',
    is_corporate_primary = 0,
    author_display = 'Kaplan, R.; Kaplan, S. (both University of Michigan)',
    author_count = 2,
    author_count_is_complete = 1,
    publisher = 'Cambridge University Press, Cambridge & New York',
    isbn = '9780521341394',
    pages_start = 'xii',
    pages_end = '340',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'books-batch-8 2026-05-21T08:00:00Z: web-search verified via WorldCat (OCLC 18814094) + Internet Archive + Cambridge University Press + Amazon. 1st edition published 28 July 1989. ISBN-13 9780521341394 (hardcover) / 9780521349390 (paperback). xii + 340 pages (some sources cite 352). LCCN 88031575. Foundational work on Attention Restoration Theory and biophilic design. Stored row was WRONG-DOI-CLEARED; DOI not applicable to 1989 book — ISBN is the canonical identifier.',
    url = 'https://archive.org/details/experienceofnatu00kapl',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+worldcat-archive-org',
    last_verified_at = '2026-05-21T08:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T08:00:00Z books-batch-8] web-search + ISBN verified',
    updated_at = '2026-05-21T08:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00485';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
