-- data_20260521060000_mixed_batch_4.sql
--
-- Mixed batch 4: demonstrates DR-2026-05-18 protocol applies correctly across
-- BOTH source types. REF-00169 is an academic journal article that gets the
-- standard Crossref-confirmed COMPLETE treatment; REF-00339 is a US university
-- design guideline that gets the COMPLETE-STATUTORY treatment per DR-2026-05-18.
--
-- REF-00169: Williams G., Corbyn J., Hart A. (2022/2023) "Improving the Sensory
--            Environments of Mental Health in-patient Facilities for Autistic
--            Children and Young People" Child Care in Practice 29(1):35-53
--            DOI 10.1080/13575279.2022.2126437
-- REF-00339: Gallaudet University DeafSpace Design Guidelines Volume 1 (2010)
--            Hansel Bauman, hbhm architects + ASL/Deaf Studies Department

BEGIN TRANSACTION;

-- REF-00169: NDTi/Williams paper — ACADEMIC, not statutory
UPDATE evidence_sources SET
    doi = '10.1080/13575279.2022.2126437',
    pub_title = 'Improving the Sensory Environments of Mental Health in-patient Facilities for Autistic Children and Young People',
    pub_year = 2023,
    first_author_last = 'Williams',
    first_author_first = 'Gemma',
    is_corporate_primary = 0,
    author_display = 'Williams, G.; Corbyn, J.; Hart, A. (National Development Team for Inclusion, NDTi)',
    author_count = 3,
    author_count_is_complete = 1,
    journal_name = 'Child Care in Practice',
    volume = '29',
    issue = '1',
    pages_start = '35',
    pages_end = '53',
    publisher = 'Informa UK Limited (Taylor & Francis)',
    issn = '1357-5279',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-4 2026-05-21T06:00:00Z: web-search identified candidate paper via tandfonline + NHS England long-read; canonical metadata confirmed via Crossref query (DOI 10.1080/13575279.2022.2126437, Child Care in Practice 29(1):35-53, online ahead 2022, published 2023). Stored year 2022 corrected to 2023 (issue publication). This is an ACADEMIC journal article — DR-2026-05-18 COMPLETE-STATUTORY does not apply; standard COMPLETE protocol used.',
    url = 'https://www.tandfonline.com/doi/full/10.1080/13575279.2022.2126437',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref-confirm',
    last_verified_at = '2026-05-21T06:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T06:00:00Z mixed-batch-4] web-search + Crossref confirmed',
    updated_at = '2026-05-21T06:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00169';

-- REF-00339: DeafSpace Design Guidelines Volume 1
UPDATE evidence_sources SET
    pub_title = 'DeafSpace Design Guidelines, Volume 1',
    pub_year = 2010,
    first_author_last = 'Bauman',
    first_author_first = 'Hansel',
    is_corporate_primary = 0,
    author_display = 'Bauman, H. (Director of Campus Planning and Design, Gallaudet University; partner, hbhm architects); collaborators: Mitnick H. (hbhm — color and material guidelines), ASL/Deaf Studies Department (Bahan B., Bauman H.-D., Sirvage R.)',
    publisher = 'Gallaudet University (in collaboration with hbhm architects)',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-4 2026-05-21T06:00:00Z: web-search verified via Gallaudet University DeafSpace site, Studio Twenty Seven Architecture case study, Institute for Human Centered Design library, and DSDG document hosted at pinelandsalliance.org. Released 2010 (Volume 1); originated from 2005-2010 DeafSpace Project (Hansel Bauman + ASL/Deaf Studies Department). Companion to Gallaudet Campus Design Guide. Won International Association of Universal Design award. "DeafSpace" is a registered service mark of Gallaudet University.',
    url = 'https://gallaudet.edu/campus-design-facilities/campus-design-and-planning/deafspace/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+gallaudet-official',
    last_verified_at = '2026-05-21T06:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T06:00:00Z mixed-batch-4] web-search verified',
    updated_at = '2026-05-21T06:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00339';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
