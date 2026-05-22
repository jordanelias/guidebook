-- data_20260522000000_doi_uplift_batch_43.sql
-- DOI uplift batch 43: 3 rows resolved.
--
-- REF-00175: Turvey 1996 Am Psychologist — DOI 10.1037/0003-066x.51.11.1134 — year-correct 1995->1996
-- REF-00385: Waters & Mulroy 1988 J Orthop Res — DOI 10.1002/jor.1100060208 — year-correct 1985->1988
-- REF-00383: Templer 1992 MIT Press "The Staircase" — book, COMPLETE via ISBN with doi_resolution_outcome=NO-MATCH

BEGIN TRANSACTION;

-- REF-00175: Turvey 1996 Am Psychologist
UPDATE evidence_sources SET
    pub_title = 'Dynamic touch',
    pub_year = 1996,
    first_author_last = 'Turvey',
    first_author_first = 'MT',
    is_corporate_primary = 0,
    author_display = 'Turvey MT',
    publisher = 'American Psychological Association; American Psychologist',
    journal_name = 'American Psychologist',
    journal_abbrev = 'Am Psychol',
    doi = '10.1037/0003-066x.51.11.1134',
    issn = '0003-066X',
    volume = '51',
    issue = '11',
    pages_start = '1134',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'YEAR-CORRECTED-1995-TO-1996',
    metadata_integrity_detail = 'doi-uplift-batch-43 2026-05-22T00:00:00Z: Crossref-confirmed. Foundational paper on haptic perception via dynamic (effortful) touch by Michael T. Turvey (Univ Connecticut + Haskins Labs). DB pub_year was 1995; actual American Psychologist 51(11):1134 published 1996. The "Academic Press" container in original DB title may refer to a related chapter/excerpt or be transcription confusion.',
    url = 'https://doi.org/10.1037/0003-066x.51.11.1134',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-22T00:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T00:00:00Z doi-uplift-batch-43] DOI resolved + year corrected',
    updated_at = '2026-05-22T00:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00175';

-- REF-00385: Waters & Mulroy 1988 J Orthop Res
UPDATE evidence_sources SET
    pub_title = 'Energy-speed relationship of walking: Standard tables',
    pub_year = 1988,
    first_author_last = 'Waters',
    first_author_first = 'RL',
    is_corporate_primary = 0,
    author_display = 'Waters RL, Mulroy S',
    publisher = 'Wiley/Orthopaedic Research Society; Journal of Orthopaedic Research',
    journal_name = 'Journal of Orthopaedic Research',
    journal_abbrev = 'J Orthop Res',
    doi = '10.1002/jor.1100060208',
    issn = '0736-0266',
    volume = '6',
    issue = '2',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'YEAR-CORRECTED-1985-TO-1988',
    metadata_integrity_detail = 'doi-uplift-batch-43 2026-05-22T00:00:00Z: Crossref-confirmed. Foundational standard-tables paper for gait energy economics by Robert L. Waters (Rancho Los Amigos Medical Center) and Sara Mulroy. J Orthop Res 6(2). DB pub_year was 1985 — likely confusion with the related 1985 J Bone Joint Surg paper "Energy cost of paraplegic locomotion" DOI 10.2106/00004623-198567080-00016 (which is a Waters research-program parallel paper). Owner: title in DB matches J Orthop Res 1988 standard tables paper exactly.',
    url = 'https://doi.org/10.1002/jor.1100060208',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+crossref',
    last_verified_at = '2026-05-22T00:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T00:00:00Z doi-uplift-batch-43] DOI resolved + year corrected',
    updated_at = '2026-05-22T00:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00385';

-- REF-00383: Templer 1992 MIT Press "The Staircase"
UPDATE evidence_sources SET
    pub_title = 'The Staircase: Studies of Hazards, Falls, and Safer Design',
    pub_year = 1992,
    first_author_last = 'Templer',
    first_author_first = 'J',
    is_corporate_primary = 0,
    author_display = 'Templer J (John Templer)',
    publisher = 'MIT Press, Cambridge MA',
    isbn = '978-0-262-20088-2',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'NO-MATCH',
    metadata_integrity_status = 'BOOK-ISBN-CANONICAL',
    metadata_integrity_detail = 'doi-uplift-batch-43 2026-05-22T00:00:00Z: book by John Templer (Georgia Institute of Technology), 2-volume work. Volume 1 "History and Theories" + Volume 2 "Studies of Hazards, Falls, and Safer Design". MIT Press 1992. ISBN 0-262-20088-0 (paperback Vol 1) / 978-0-262-20088-2. Companion 1994 Technology and Culture book review of Templer "The Staircase" at DOI 10.2307/3106526 (not the book itself). doi_resolution_outcome=NO-MATCH per books-as-canonical convention.',
    url = 'https://mitpress.mit.edu/9780262200882/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+mit-press-catalog',
    last_verified_at = '2026-05-22T00:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T00:00:00Z doi-uplift-batch-43] book ISBN-canonical',
    updated_at = '2026-05-22T00:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00383';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
