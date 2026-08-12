-- data_20260520230000_wrong_attribution_correction.sql
--
-- Corrects wrong-DOI-attachment corruption introduced by
-- session_2026-05-12j-phase-b-verification on 2026-05-12, where unrelated
-- DOIs and PMIDs were attached to AUTHOR-TITLE-ONLY rows and the rows were
-- marked VERIFIED. Identifiers and title/author/year point to different
-- papers in each case.
--
-- Per owner direction (option 2): overwrite the corrupted row with canonical
-- metadata from the identifier, AND preserve the displaced original metadata
-- as a new AUTHOR-TITLE-ONLY row so the original citation isn't lost.
--
-- Three rows corrected:
--   REF-00069 (NZ Keall MHIPI 2021) → became Oostermeijer 2021 BMJ Open AU;
--             displaced Keall metadata → new REF-00728.
--   REF-00096 (NO Faerden 2022) → became van Oel 2020 HERD NL;
--             displaced Faerden metadata → new REF-00729.
--   REF-00527 (US Harper 2022) → became Owen 2022 IJERPH AU (canonical DOI
--             replaces the truncated/wrong DOI 10.35248/2165-7556-22);
--             displaced Harper metadata → new REF-00730.
--
-- Slug links NOT touched — owner review needed (a slug pointing to any of
-- these three may have meant the original paper or the canonical paper;
-- only owner can disambiguate per BPC content).

BEGIN TRANSACTION;

-- ============================================================
-- Step 1: Insert displaced metadata as new rows
-- ============================================================

INSERT INTO evidence_sources (
    ref_id, source_type, author_count, author_count_is_complete,
    first_author_last, first_author_first, is_corporate_primary, author_display,
    pub_year, pub_title, lang_detected, lang_detection_method, translation_method,
    tier, evidence_type, jurisdiction,
    metadata_quality, verification_status, doi_resolution_outcome,
    verification_attempt_count,
    metadata_integrity_status, metadata_integrity_detail,
    verification_note,
    created_at, created_by_session, updated_at, updated_by_session
) VALUES (
    'REF-00728', 'report', 1, 0,
    'Keall', 'M.', 0, 'Keall, M.',
    2021, 'MHIPI study. Lancet Public Health 6:e631–e640',
    'en', 'langdetect', 'native_english',
    3, 'clinical', 'NZ',
    'AUTHOR-TITLE-ONLY', NULL, NULL,
    0,
    'DISPLACED-FROM-REF-00069',
    'Original metadata displaced from REF-00069 (wrong-DOI-attachment correction 2026-05-20T23:00:00Z). REF-00069 carried identifiers (DOI 10.1136/bmjopen-2020-046647, PMID 34233981) that resolve to Oostermeijer 2021 BMJ Open; the row originally stored Keall MHIPI 2021 Lancet Public Health metadata which belonged to a different paper. Identifiers stayed with REF-00069 (paper-identity is canonical); displaced Keall metadata preserved here. Slug links not migrated — owner must disambiguate per-BPC.',
    '[2026-05-20T23:00:00Z session_2026-05-20-ato-rehab] Created via wrong_attribution_correction migration to preserve displaced metadata from REF-00069.',
    '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab',
    '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'
);

INSERT INTO evidence_sources (
    ref_id, source_type, author_count, author_count_is_complete,
    first_author_last, first_author_first, is_corporate_primary, author_display,
    pub_year, pub_title, lang_detected, lang_detection_method, translation_method,
    tier, evidence_type, jurisdiction,
    metadata_quality, verification_status, doi_resolution_outcome,
    verification_attempt_count,
    metadata_integrity_status, metadata_integrity_detail,
    verification_note,
    created_at, created_by_session, updated_at, updated_by_session
) VALUES (
    'REF-00729', 'report', 1, 0,
    'Faerden', 'A.', 0, 'Faerden, A.',
    2022, 'Single rooms and patient control in inpatient mental health',
    'en', 'langdetect', 'native_english',
    3, 'clinical', 'NO',
    'AUTHOR-TITLE-ONLY', NULL, NULL,
    0,
    'DISPLACED-FROM-REF-00096',
    'Original metadata displaced from REF-00096 (wrong-DOI-attachment correction 2026-05-20T23:00:00Z). REF-00096 carried identifiers (DOI 10.1177/1937586720937995, PMID 36567605) that resolve to van Oel 2020 HERD; the row originally stored Faerden 2022 NO mental-health-architecture metadata which belonged to a different paper. Identifiers stayed with REF-00096; displaced Faerden metadata preserved here. Slug links not migrated.',
    '[2026-05-20T23:00:00Z session_2026-05-20-ato-rehab] Created via wrong_attribution_correction migration to preserve displaced metadata from REF-00096.',
    '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab',
    '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'
);

INSERT INTO evidence_sources (
    ref_id, source_type, author_count, author_count_is_complete,
    first_author_last, first_author_first, is_corporate_primary, author_display,
    pub_year, pub_title, lang_detected, lang_detection_method, translation_method,
    tier, evidence_type, jurisdiction,
    metadata_quality, verification_status, doi_resolution_outcome,
    verification_attempt_count,
    metadata_integrity_status, metadata_integrity_detail,
    verification_note,
    created_at, created_by_session, updated_at, updated_by_session
) VALUES (
    'REF-00730', 'report', 1, 0,
    'Harper', 'S.A.', 0, 'Harper, S.A.',
    2022, 'Stairway Visual Contrast Enhancement to Reduce Fall-Related Injuries',
    'en', 'langdetect', 'native_english',
    3, 'clinical', 'US',
    'AUTHOR-TITLE-ONLY', NULL, NULL,
    0,
    'DISPLACED-FROM-REF-00527',
    'Original metadata displaced from REF-00527 (wrong-DOI-attachment correction 2026-05-20T23:00:00Z). REF-00527 carried identifiers (DOI 10.35248/2165-7556-22 [truncated/wrong publisher prefix], PMID 36361166) that PMID resolves to Owen 2022 IJERPH; the row originally stored Harper 2022 US stairway-contrast metadata which belonged to a different paper. Canonical DOI 10.3390/ijerph192114279 replaces the truncated/wrong DOI on REF-00527; displaced Harper metadata preserved here. Slug links not migrated.',
    '[2026-05-20T23:00:00Z session_2026-05-20-ato-rehab] Created via wrong_attribution_correction migration to preserve displaced metadata from REF-00527.',
    '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab',
    '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'
);

-- ============================================================
-- Step 2: Move existing author rows to displaced refs
-- ============================================================

UPDATE evidence_source_authors SET ref_id = 'REF-00728',
    created_by_session = COALESCE(created_by_session, '') || ' | moved 2026-05-20T23:00:00Z from REF-00069 (wrong-attribution correction)'
WHERE ref_id = 'REF-00069';

UPDATE evidence_source_authors SET ref_id = 'REF-00729',
    created_by_session = COALESCE(created_by_session, '') || ' | moved 2026-05-20T23:00:00Z from REF-00096 (wrong-attribution correction)'
WHERE ref_id = 'REF-00096';

UPDATE evidence_source_authors SET ref_id = 'REF-00730',
    created_by_session = COALESCE(created_by_session, '') || ' | moved 2026-05-20T23:00:00Z from REF-00527 (wrong-attribution correction)'
WHERE ref_id = 'REF-00527';

-- ============================================================
-- Step 3: Overwrite REF-00069 with canonical Oostermeijer 2021 BMJ Open metadata
-- ============================================================

UPDATE evidence_sources SET
    first_author_last = 'Oostermeijer',
    first_author_first = 'Sanne',
    author_display = 'Oostermeijer, S.; Brasier, C.; Harvey, C.; Hamilton, B.; Roper, C.; Martel, A.; Fletcher, J.; Brophy, L.',
    author_count = 8,
    author_count_is_complete = 1,
    is_corporate_primary = 0,
    pub_year = 2021,
    pub_title = 'Design features that reduce the use of seclusion and restraint in mental health facilities: a rapid systematic review',
    journal_name = 'BMJ Open',
    volume = '11',
    issue = '7',
    pages_start = 'e046647',
    pages_end = NULL,
    publisher = 'BMJ',
    issn = '2044-6055',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'wrong-attribution-corrected 2026-05-20T23:00:00Z; canonical metadata from DOI 10.1136/bmjopen-2020-046647 (Crossref) + PMID 34233981 (PubMed) — identifiers internally consistent. Displaced Keall MHIPI metadata preserved at REF-00728. Phase B verification (session_2026-05-12j) attached correct identifiers but failed to update title/author/year — corruption surfaced by batch-1 and batch-2 cross-checks (both flagged MISMATCH-MULTI).',
    verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-20T23:00:00Z wrong-attribution-correction] title/author/year/journal overwritten with canonical metadata from identifiers; displaced metadata → REF-00728',
    updated_at = '2026-05-20T23:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00069';

-- ============================================================
-- Step 4: Overwrite REF-00096 with canonical van Oel 2020 HERD metadata
-- ============================================================

UPDATE evidence_sources SET
    first_author_last = 'van Oel',
    first_author_first = 'Clarine J.',
    author_display = 'van Oel, C.J.; Mlihi, M.; Freeke, A.',
    author_count = 3,
    author_count_is_complete = 1,
    is_corporate_primary = 0,
    pub_year = 2020,
    pub_title = 'Design Models for Single Patient Rooms Tested for Patient Preferences',
    journal_name = 'HERD: Health Environments Research & Design Journal',
    volume = '14',
    issue = '1',
    pages_start = '31',
    pages_end = '46',
    publisher = 'SAGE Publications',
    issn = '1937-5867',
    jurisdiction = 'NL',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'wrong-attribution-corrected 2026-05-20T23:00:00Z; canonical metadata from DOI 10.1177/1937586720937995 (Crossref) — note PMID 36567605 on this row needs separate verification (was attached by Phase B alongside the DOI). Displaced Faerden metadata preserved at REF-00729.',
    verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-20T23:00:00Z wrong-attribution-correction] title/author/year/journal overwritten with canonical metadata from DOI; displaced metadata → REF-00729',
    updated_at = '2026-05-20T23:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00096';

-- ============================================================
-- Step 5: Overwrite REF-00527 with canonical Owen 2022 IJERPH metadata
--         AND replace truncated/wrong DOI with canonical DOI
-- ============================================================

UPDATE evidence_sources SET
    first_author_last = 'Owen',
    first_author_first = 'Ceridwen',
    author_display = 'Owen, C.; Crane, J.',
    author_count = 2,
    author_count_is_complete = 1,
    is_corporate_primary = 0,
    pub_year = 2022,
    pub_title = 'Trauma-Informed Design of Supported Housing: A Scoping Review through the Lens of Neuroscience',
    journal_name = 'International Journal of Environmental Research and Public Health',
    volume = '19',
    issue = '21',
    pages_start = '14279',
    pages_end = NULL,
    publisher = 'MDPI AG',
    issn = '1660-4601',
    doi = '10.3390/ijerph192114279',
    pmcid = 'PMC9658651',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'wrong-attribution-corrected 2026-05-20T23:00:00Z; canonical metadata from PMID 36361166 (PubMed) including canonical DOI 10.3390/ijerph192114279 (replaces wrong stored 10.35248/2165-7556-22 — that prefix is the NLM Open publisher, not MDPI; was not a truncation but a genuinely wrong DOI). Displaced Harper metadata preserved at REF-00730.',
    verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-20T23:00:00Z wrong-attribution-correction] title/author/year/journal/DOI overwritten with canonical metadata from PMID; displaced metadata → REF-00730',
    updated_at = '2026-05-20T23:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00527';

-- ============================================================
-- Step 6: Insert new author rows for canonical papers
-- ============================================================

-- REF-00069 (Oostermeijer et al. 2021 BMJ Open)
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES
('REF-00069', 1, 'Oostermeijer', 'Sanne', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00069', 2, 'Brasier', 'Catherine', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00069', 3, 'Harvey', 'Carol', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00069', 4, 'Hamilton', 'Bridget', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00069', 5, 'Roper', 'Cath', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00069', 6, 'Martel', 'Andrew', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00069', 7, 'Fletcher', 'Justine', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00069', 8, 'Brophy', 'Lisa', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab');

-- REF-00096 (van Oel et al. 2020 HERD)
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES
('REF-00096', 1, 'van Oel', 'Clarine J.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00096', 2, 'Mlihi', 'Meloek', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00096', 3, 'Freeke', 'Arno', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab');

-- REF-00527 (Owen & Crane 2022 IJERPH)
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES
('REF-00527', 1, 'Owen', 'Ceridwen', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00527', 2, 'Crane', 'Jasmine', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-20T23:00:00Z', 'session_2026-05-20-ato-rehab');

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
