-- data_20260521000000_full_db_metadata_corrections.sql
--
-- Comprehensive metadata corrections from full-DB verification audit.
-- Audit re-fetched canonical metadata for all 238 evidence_sources rows with any
-- identifier; 12 rows (5%) showed WRONG-ATTRIBUTION or IDENTIFIER-DISAGREE.
--
-- Action types:
--   FIELD-FIX (3 rows): REF-00028, REF-00262, REF-00284 — same paper; fix fields
--   DISPLACE (5 rows):  REF-00150/00233/00240/00302/00571 — wrong-attribution;
--                       overwrite with canonical, preserve displaced as 731-735
--   CLEAR-DOI (2 rows): REF-00176, REF-00478 — DOI was wrong; book metadata real
--   CLEAR-PMID (1 row): REF-00096 — PMID was wrong; DOI is correct
--   OWNER-QUEUE (1 row): REF-00363 — Gitlin DOI/PMID disagree, owner decides
--
BEGIN TRANSACTION;

-- REF-00028: FIELD-FIX
UPDATE evidence_sources SET
  pub_title = 'Grab Bar Use Influences Fall Hazard During Bathtub Exit',
  pub_year = 2021,
  journal_name = 'Human Factors: The Journal of the Human Factors and Ergonomics Society',
  first_author_last = 'Levine',
  first_author_first = 'Iris C.',
  author_display = 'Levine, I.; Montgomery, R.; Novak, A.',
  author_count = 3,
  author_count_is_complete = 1,
  volume = '65',
  issue = '8',
  pages_start = '1821',
  pages_end = '1829',
  publisher = 'SAGE Publications',
  issn = '0018-7208',
  metadata_quality = 'COMPLETE',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'field-fix 2026-05-21T00:00:00Z: same paper (Levine 2021 Human Factors: The Journal of the Human Factors and Ergonomics Society). Stored had paraphrased pub_title and wrong year 2023; canonical is Levine 2021.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:00:00Z full-DB-audit] FIELD-FIX from canonical',
  updated_at = '2026-05-21T00:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count,0)+1
WHERE ref_id = 'REF-00028';

-- REF-00262: FIELD-FIX
UPDATE evidence_sources SET
  pub_title = 'Universal Design: A Step toward Successful Aging',
  pub_year = 2013,
  journal_name = 'Journal of Aging Research',
  first_author_last = 'Carr',
  first_author_first = 'Kelly',
  author_display = 'Carr, K.; Weir, P.; Azar, D.; Azar, N.',
  author_count = 4,
  author_count_is_complete = 1,
  volume = '2013',
  issue = NULL,
  pages_start = '1',
  pages_end = '8',
  publisher = 'Wiley',
  issn = '2090-2204',
  metadata_quality = 'COMPLETE',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'field-fix 2026-05-21T00:00:00Z: same paper (Carr 2013 Journal of Aging Research). Stored first_author_last was ''Carr K'' (form drift); title shortened.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:00:00Z full-DB-audit] FIELD-FIX from canonical',
  updated_at = '2026-05-21T00:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count,0)+1
WHERE ref_id = 'REF-00262';

-- REF-00284: FIELD-FIX
UPDATE evidence_sources SET
  pub_title = 'CAPABLE ADAPTATIONS: MEETING THE NEEDS OF OLDER ADULTS ACROSS DIVERSE CONTEXTS TO SUPPORT FUNCTION',
  pub_year = 2024,
  journal_name = 'Innovation in Aging',
  first_author_last = 'Cudjoe',
  first_author_first = 'Thomas',
  author_display = 'Cudjoe, T.; Steinman, L.',
  author_count = 2,
  author_count_is_complete = 1,
  volume = '8',
  issue = 'Supplement_1',
  pages_start = '180',
  pages_end = '180',
  publisher = 'Oxford University Press (OUP)',
  issn = '2399-5300',
  metadata_quality = 'COMPLETE',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'field-fix 2026-05-21T00:00:00Z: same paper (Cudjoe 2024 Innovation in Aging). Stored author ''Cudjoe T'' form drift; title-case variation. Same paper.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:00:00Z full-DB-audit] FIELD-FIX from canonical',
  updated_at = '2026-05-21T00:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count,0)+1
WHERE ref_id = 'REF-00284';

-- REF-00096: CLEAR-PMID (DOI correct -> van Oel 2020; PMID 36567605 was wrong-attached)
UPDATE evidence_sources SET
  pmid = NULL,
  metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | full-DB-audit 2026-05-21T00:00:00Z: PMID 36567605 cleared - it resolves to Faerden 2023 different paper. DOI alone is correct identifier.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:00:00Z full-DB-audit] CLEAR-PMID 36567605 (wrong-attached)',
  updated_at = '2026-05-21T00:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count,0)+1
WHERE ref_id = 'REF-00096';

-- REF-00176: CLEAR-DOI
UPDATE evidence_sources SET
  doi = NULL,
  verification_status = NULL,
  doi_resolution_outcome = NULL,
  metadata_integrity_status = 'WRONG-DOI-CLEARED',
  metadata_integrity_detail = 'full-DB-audit 2026-05-21T00:00:00Z: DOI 10.1126/science.166.3907.856-a CLEARED - it resolves to Weick 1969 book review of Barker in Science. Stored citation IS Barker 1968 ''Ecological Psychology'' (Stanford UP) - real book predating DOI registration. verification_status reverted from VERIFIED (prior verification was based on wrong identifier).',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:00:00Z full-DB-audit] CLEAR-DOI (wrong-attribution)',
  updated_at = '2026-05-21T00:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count,0)+1
WHERE ref_id = 'REF-00176';

-- REF-00478: CLEAR-DOI
UPDATE evidence_sources SET
  doi = NULL,
  verification_status = NULL,
  doi_resolution_outcome = NULL,
  metadata_integrity_status = 'WRONG-DOI-CLEARED',
  metadata_integrity_detail = 'full-DB-audit 2026-05-21T00:00:00Z: DOI 10.1177/019263658506948224 CLEARED - resolves to Lynch 1985 book review in NASSP Bulletin, not Passini''s book. Stored citation IS Passini 1984 ''Wayfinding in Architecture'' (Van Nostrand Reinhold) - real book predating DOI registration. verification_status reverted from VERIFIED.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:00:00Z full-DB-audit] CLEAR-DOI (wrong-attribution)',
  updated_at = '2026-05-21T00:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count,0)+1
WHERE ref_id = 'REF-00478';

-- REF-00363: OWNER-QUEUE (DOI and PMID both Gitlin 2006 but different papers)
UPDATE evidence_sources SET
  metadata_integrity_status = 'IDENTIFIER-DISAGREE-OWNER-DECIDE',
  metadata_integrity_detail = 'full-DB-audit 2026-05-21T00:00:00Z: DOI 10.1111/j.1532-5415.2006.00703.x -> Gitlin 2006 Multicomponent Home Intervention (JAGS); PMID 17050754 -> Gitlin 2006 Enhancing quality of life of families who use adult day services (different paper). Owner must decide intent; clear the other identifier.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:00:00Z full-DB-audit] OWNER-DECIDE: DOI/PMID resolve to different Gitlin 2006 papers',
  updated_at = '2026-05-21T00:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count,0)+1
WHERE ref_id = 'REF-00363';

-- DISPLACE: REF-00150 -> REF-00731 (identifier resolves to Iker 2019)
-- Step A: insert displaced metadata
INSERT INTO evidence_sources (
  ref_id, source_type, author_count, author_count_is_complete,
  first_author_last, first_author_first, is_corporate_primary, author_display,
  pub_year, pub_title, lang_detected, lang_detection_method, translation_method,
  tier, evidence_type, jurisdiction,
  metadata_quality, verification_status, verification_attempt_count,
  metadata_integrity_status, metadata_integrity_detail,
  verification_note,
  created_at, created_by_session, updated_at, updated_by_session
) VALUES (
  'REF-00731', 'report', 1, 0,
  'Szanton', 'S.', 0, 'Szanton, S.',
  2019, '$2,825/participant home modification', 'en', 'langdetect', 'native_english',
  3, 'clinical', 'US',
  'AUTHOR-TITLE-ONLY', NULL, 0,
  'DISPLACED-FROM-REF-00150',
  'Displaced from REF-00150 by full-DB-audit 2026-05-21T00:00:00Z. REF-00150 carried identifier(s) that resolved to Iker 2019 (different paper). Identifier(s) stayed with REF-00150; this row preserves original Szanton metadata. Slug links not migrated; owner review required.',
  '[2026-05-21T00:00:00Z session_2026-05-20-ato-rehab] Created via full-DB-audit displacement from REF-00150.',
  '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab'
);

-- Step B: move evidence_source_authors REF-00150 -> REF-00731
UPDATE evidence_source_authors SET ref_id = 'REF-00731',
  created_by_session = COALESCE(created_by_session,'') || ' | moved 2026-05-21T00:00:00Z from REF-00150 (full-DB-audit displacement)'
WHERE ref_id = 'REF-00150';

-- Step C: overwrite REF-00150 with canonical Iker metadata
UPDATE evidence_sources SET
  first_author_last = 'Iker',
  first_author_first = 'E',
  author_display = 'Iker, E.; Mayfield, C.; Gould, D.; Patel, K.',
  author_count = 4,
  author_count_is_complete = 1,
  is_corporate_primary = 0,
  pub_year = 2019,
  pub_title = 'Characterizing Lower Extremity Lymphedema and Lipedema with Cutaneous Ultrasonography and an Objective Computer-Assisted Measurement of Dermal Echogenicity.',
  journal_name = 'Lymphatic research and biology',
  volume = '17',
  issue = '5',
  pages_start = '525',
  pages_end = '530',
  publisher = NULL,
  issn = '1539-6851',
  jurisdiction = NULL,
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'wrong-attribution-corrected 2026-05-21T00:00:00Z by full-DB-audit. Canonical metadata for identifier(s); displaced Szanton metadata preserved at REF-00731. jurisdiction reset to NULL (prior US belonged to displaced paper).',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:00:00Z full-DB-audit] WRONG-ATTRIBUTION corrected; displaced -> REF-00731',
  updated_at = '2026-05-21T00:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count,0)+1
WHERE ref_id = 'REF-00150';

-- Step D: insert canonical author rows for REF-00150
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00150', 1, 'Iker', 'E', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00150', 2, 'Mayfield', 'CK', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00150', 3, 'Gould', 'DJ', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00150', 4, 'Patel', 'KM', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');

-- DISPLACE: REF-00233 -> REF-00732 (identifier resolves to Richardson 2018)
-- Step A: insert displaced metadata
INSERT INTO evidence_sources (
  ref_id, source_type, author_count, author_count_is_complete,
  first_author_last, first_author_first, is_corporate_primary, author_display,
  pub_year, pub_title, lang_detected, lang_detection_method, translation_method,
  tier, evidence_type, jurisdiction,
  metadata_quality, verification_status, verification_attempt_count,
  metadata_integrity_status, metadata_integrity_detail,
  verification_note,
  created_at, created_by_session, updated_at, updated_by_session
) VALUES (
  'REF-00732', 'report', 1, 0,
  'Strassheim', NULL, 0, 'Strassheim',
  2018, 'OI in ME/CFS', 'en', 'langdetect', 'native_english',
  3, 'clinical', 'INT',
  'AUTHOR-TITLE-ONLY', NULL, 0,
  'DISPLACED-FROM-REF-00233',
  'Displaced from REF-00233 by full-DB-audit 2026-05-21T00:00:00Z. REF-00233 carried identifier(s) that resolved to Richardson 2018 (different paper). Identifier(s) stayed with REF-00233; this row preserves original Strassheim metadata. Slug links not migrated; owner review required.',
  '[2026-05-21T00:00:00Z session_2026-05-20-ato-rehab] Created via full-DB-audit displacement from REF-00233.',
  '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab'
);

-- Step B: move evidence_source_authors REF-00233 -> REF-00732
UPDATE evidence_source_authors SET ref_id = 'REF-00732',
  created_by_session = COALESCE(created_by_session,'') || ' | moved 2026-05-21T00:00:00Z from REF-00233 (full-DB-audit displacement)'
WHERE ref_id = 'REF-00233';

-- Step C: overwrite REF-00233 with canonical Richardson metadata
UPDATE evidence_sources SET
  first_author_last = 'Richardson',
  first_author_first = 'Alice M.',
  author_display = 'Richardson, A.; Lewis, D.; Kita, B.; Ludlow, H.; Groome, N.; Hedger, M.; de Kretser, D.; Lidbury, B.',
  author_count = 8,
  author_count_is_complete = 1,
  is_corporate_primary = 0,
  pub_year = 2018,
  pub_title = 'Weighting of orthostatic intolerance time measurements with standing difficulty score stratifies ME/CFS symptom severity and analyte detection',
  journal_name = 'Journal of Translational Medicine',
  volume = '16',
  issue = '1',
  pages_start = NULL,
  pages_end = NULL,
  publisher = 'Springer Science and Business Media LLC',
  issn = '1479-5876',
  jurisdiction = NULL,
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'wrong-attribution-corrected 2026-05-21T00:00:00Z by full-DB-audit. Canonical metadata for identifier(s); displaced Strassheim metadata preserved at REF-00732. jurisdiction reset to NULL (prior INT belonged to displaced paper).',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:00:00Z full-DB-audit] WRONG-ATTRIBUTION corrected; displaced -> REF-00732',
  updated_at = '2026-05-21T00:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count,0)+1
WHERE ref_id = 'REF-00233';

-- Step D: insert canonical author rows for REF-00233
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00233', 1, 'Richardson', 'Alice M.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00233', 2, 'Lewis', 'Don P.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00233', 3, 'Kita', 'Badia', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00233', 4, 'Ludlow', 'Helen', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00233', 5, 'Groome', 'Nigel P.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00233', 6, 'Hedger', 'Mark P.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00233', 7, 'de Kretser', 'David M.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00233', 8, 'Lidbury', 'Brett A.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');

-- DISPLACE: REF-00240 -> REF-00733 (identifier resolves to McVeigh 2008)
-- Step A: insert displaced metadata
INSERT INTO evidence_sources (
  ref_id, source_type, author_count, author_count_is_complete,
  first_author_last, first_author_first, is_corporate_primary, author_display,
  pub_year, pub_title, lang_detected, lang_detection_method, translation_method,
  tier, evidence_type, jurisdiction,
  metadata_quality, verification_status, verification_attempt_count,
  metadata_integrity_status, metadata_integrity_detail,
  verification_note,
  created_at, created_by_session, updated_at, updated_by_session
) VALUES (
  'REF-00733', 'report', 1, 0,
  'Ismail', NULL, 0, 'Ismail',
  2023, 'Fibromyalgia hydrotherapy SR. Tandfonline', 'en', 'langdetect', 'native_english',
  3, 'sr_meta', 'INT',
  'AUTHOR-TITLE-ONLY', NULL, 0,
  'DISPLACED-FROM-REF-00240',
  'Displaced from REF-00240 by full-DB-audit 2026-05-21T00:00:00Z. REF-00240 carried identifier(s) that resolved to McVeigh 2008 (different paper). Identifier(s) stayed with REF-00240; this row preserves original Ismail metadata. Slug links not migrated; owner review required.',
  '[2026-05-21T00:00:00Z session_2026-05-20-ato-rehab] Created via full-DB-audit displacement from REF-00240.',
  '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab'
);

-- Step B: move evidence_source_authors REF-00240 -> REF-00733
UPDATE evidence_source_authors SET ref_id = 'REF-00733',
  created_by_session = COALESCE(created_by_session,'') || ' | moved 2026-05-21T00:00:00Z from REF-00240 (full-DB-audit displacement)'
WHERE ref_id = 'REF-00240';

-- Step C: overwrite REF-00240 with canonical McVeigh metadata
UPDATE evidence_sources SET
  first_author_last = 'McVeigh',
  first_author_first = 'JG',
  author_display = 'McVeigh, J.; McGaughey, H.; Hall, M.; Kane, P.',
  author_count = 4,
  author_count_is_complete = 1,
  is_corporate_primary = 0,
  pub_year = 2008,
  pub_title = 'The effectiveness of hydrotherapy in the management of fibromyalgia syndrome: a systematic review.',
  journal_name = 'Rheumatology international',
  volume = '29',
  issue = '2',
  pages_start = '119',
  pages_end = '30',
  publisher = NULL,
  issn = '0172-8172',
  jurisdiction = NULL,
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'wrong-attribution-corrected 2026-05-21T00:00:00Z by full-DB-audit. Canonical metadata for identifier(s); displaced Ismail metadata preserved at REF-00733. jurisdiction reset to NULL (prior INT belonged to displaced paper).',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:00:00Z full-DB-audit] WRONG-ATTRIBUTION corrected; displaced -> REF-00733',
  updated_at = '2026-05-21T00:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count,0)+1
WHERE ref_id = 'REF-00240';

-- Step D: insert canonical author rows for REF-00240
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00240', 1, 'McVeigh', 'JG', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00240', 2, 'McGaughey', 'H', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00240', 3, 'Hall', 'M', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00240', 4, 'Kane', 'P', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');

-- DISPLACE: REF-00302 -> REF-00734 (identifier resolves to Mauldin 2022)
-- Step A: insert displaced metadata
INSERT INTO evidence_sources (
  ref_id, source_type, author_count, author_count_is_complete,
  first_author_last, first_author_first, is_corporate_primary, author_display,
  pub_year, pub_title, lang_detected, lang_detection_method, translation_method,
  tier, evidence_type, jurisdiction,
  metadata_quality, verification_status, verification_attempt_count,
  metadata_integrity_status, metadata_integrity_detail,
  verification_note,
  created_at, created_by_session, updated_at, updated_by_session
) VALUES (
  'REF-00734', 'report', 1, 0,
  'Tibble', NULL, 0, 'Tibble',
  2005, 'Review of extra costs facing disabled people', 'en', 'langdetect', 'native_english',
  5, 'co1', 'UK',
  'AUTHOR-TITLE-ONLY', NULL, 0,
  'DISPLACED-FROM-REF-00302',
  'Displaced from REF-00302 by full-DB-audit 2026-05-21T00:00:00Z. REF-00302 carried identifier(s) that resolved to Mauldin 2022 (different paper). Identifier(s) stayed with REF-00302; this row preserves original Tibble metadata. Slug links not migrated; owner review required.',
  '[2026-05-21T00:00:00Z session_2026-05-20-ato-rehab] Created via full-DB-audit displacement from REF-00302.',
  '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab'
);

-- Step B: move evidence_source_authors REF-00302 -> REF-00734
UPDATE evidence_source_authors SET ref_id = 'REF-00734',
  created_by_session = COALESCE(created_by_session,'') || ' | moved 2026-05-21T00:00:00Z from REF-00302 (full-DB-audit displacement)'
WHERE ref_id = 'REF-00302';

-- Step C: overwrite REF-00302 with canonical Mauldin metadata
UPDATE evidence_sources SET
  first_author_last = 'Mauldin',
  first_author_first = 'Laura',
  author_display = 'Mauldin, L.',
  author_count = 1,
  author_count_is_complete = 1,
  is_corporate_primary = 0,
  pub_year = 2022,
  pub_title = 'Long COVID leaves newly disabled people facing old barriers – a sociologist explains',
  journal_name = NULL,
  volume = NULL,
  issue = NULL,
  pages_start = NULL,
  pages_end = NULL,
  publisher = 'The Conversation',
  issn = NULL,
  jurisdiction = NULL,
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'wrong-attribution-corrected 2026-05-21T00:00:00Z by full-DB-audit. Canonical metadata for identifier(s); displaced Tibble metadata preserved at REF-00734. jurisdiction reset to NULL (prior UK belonged to displaced paper).',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:00:00Z full-DB-audit] WRONG-ATTRIBUTION corrected; displaced -> REF-00734',
  updated_at = '2026-05-21T00:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count,0)+1
WHERE ref_id = 'REF-00302';

-- Step D: insert canonical author rows for REF-00302
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00302', 1, 'Mauldin', 'Laura', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');

-- DISPLACE: REF-00571 -> REF-00735 (identifier resolves to Kotloski 2020)
-- Step A: insert displaced metadata
INSERT INTO evidence_sources (
  ref_id, source_type, author_count, author_count_is_complete,
  first_author_last, first_author_first, is_corporate_primary, author_display,
  pub_year, pub_title, lang_detected, lang_detection_method, translation_method,
  tier, evidence_type, jurisdiction,
  metadata_quality, verification_status, verification_attempt_count,
  metadata_integrity_status, metadata_integrity_detail,
  verification_note,
  created_at, created_by_session, updated_at, updated_by_session
) VALUES (
  'REF-00735', 'report', 1, 0,
  'Devos', NULL, 0, 'Devos',
  2019, 'Dementia soundscape. PMC6950055', 'en', 'langdetect', 'native_english',
  3, 'clinical', 'INT',
  'AUTHOR-TITLE-ONLY', NULL, 0,
  'DISPLACED-FROM-REF-00571',
  'Displaced from REF-00571 by full-DB-audit 2026-05-21T00:00:00Z. REF-00571 carried identifier(s) that resolved to Kotloski 2020 (different paper). Identifier(s) stayed with REF-00571; this row preserves original Devos metadata. Slug links not migrated; owner review required.',
  '[2026-05-21T00:00:00Z session_2026-05-20-ato-rehab] Created via full-DB-audit displacement from REF-00571.',
  '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab'
);

-- Step B: move evidence_source_authors REF-00571 -> REF-00735
UPDATE evidence_source_authors SET ref_id = 'REF-00735',
  created_by_session = COALESCE(created_by_session,'') || ' | moved 2026-05-21T00:00:00Z from REF-00571 (full-DB-audit displacement)'
WHERE ref_id = 'REF-00571';

-- Step C: overwrite REF-00571 with canonical Kotloski metadata
UPDATE evidence_sources SET
  first_author_last = 'Kotloski',
  first_author_first = 'Robert J.',
  author_display = 'Kotloski, R.; Rutecki, P.; Sutula, T.',
  author_count = 3,
  author_count_is_complete = 1,
  is_corporate_primary = 0,
  pub_year = 2020,
  pub_title = 'Genetic Background Influences Acute Response to TBI in Kindling-Susceptible, Kindling-Resistant, and Outbred Rats',
  journal_name = 'Frontiers in Neurology',
  volume = '10',
  issue = NULL,
  pages_start = NULL,
  pages_end = NULL,
  publisher = 'Frontiers Media SA',
  issn = '1664-2295',
  jurisdiction = NULL,
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'wrong-attribution-corrected 2026-05-21T00:00:00Z by full-DB-audit. Canonical metadata for identifier(s); displaced Devos metadata preserved at REF-00735. jurisdiction reset to NULL (prior INT belonged to displaced paper).',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:00:00Z full-DB-audit] WRONG-ATTRIBUTION corrected; displaced -> REF-00735',
  updated_at = '2026-05-21T00:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count,0)+1
WHERE ref_id = 'REF-00571';

-- Step D: insert canonical author rows for REF-00571
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00571', 1, 'Kotloski', 'Robert J.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00571', 2, 'Rutecki', 'Paul A.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('REF-00571', 3, 'Sutula', 'Thomas P.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab');

-- v1_legacy sync for new displaced rows
INSERT INTO evidence_sources_v1_legacy (
  ref_id, authors, year, title, doi, doi_less_key, pmid,
  tier, evidence_type, jurisdiction, metadata_quality, verification_status,
  notes, created_at, created_by_session, updated_at, updated_by_session
) VALUES (
  'REF-00731', 'Szanton, S.', '2019',
  '$2,825/participant home modification', NULL, 'szanton_2019_$2,825/participant_home_modifi', NULL,
  3, 'clinical', 'US', 'AUTHOR-TITLE-ONLY', NULL,
  'Displaced from REF-00150 by full-DB-audit 2026-05-21',
  '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab'
);
INSERT INTO evidence_sources_v1_legacy (
  ref_id, authors, year, title, doi, doi_less_key, pmid,
  tier, evidence_type, jurisdiction, metadata_quality, verification_status,
  notes, created_at, created_by_session, updated_at, updated_by_session
) VALUES (
  'REF-00732', 'Strassheim', '2018',
  'OI in ME/CFS', NULL, 'strassheim_2018_oi_in_me/cfs', NULL,
  3, 'clinical', 'INT', 'AUTHOR-TITLE-ONLY', NULL,
  'Displaced from REF-00233 by full-DB-audit 2026-05-21',
  '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab'
);
INSERT INTO evidence_sources_v1_legacy (
  ref_id, authors, year, title, doi, doi_less_key, pmid,
  tier, evidence_type, jurisdiction, metadata_quality, verification_status,
  notes, created_at, created_by_session, updated_at, updated_by_session
) VALUES (
  'REF-00733', 'Ismail', '2023',
  'Fibromyalgia hydrotherapy SR. Tandfonline', NULL, 'ismail_2023_fibromyalgia_hydrotherapy_sr._', NULL,
  3, 'sr_meta', 'INT', 'AUTHOR-TITLE-ONLY', NULL,
  'Displaced from REF-00240 by full-DB-audit 2026-05-21',
  '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab'
);
INSERT INTO evidence_sources_v1_legacy (
  ref_id, authors, year, title, doi, doi_less_key, pmid,
  tier, evidence_type, jurisdiction, metadata_quality, verification_status,
  notes, created_at, created_by_session, updated_at, updated_by_session
) VALUES (
  'REF-00734', 'Tibble', '2005',
  'Review of extra costs facing disabled people', NULL, 'tibble_2005_review_of_extra_costs_facing_d', NULL,
  5, 'co1', 'UK', 'AUTHOR-TITLE-ONLY', NULL,
  'Displaced from REF-00302 by full-DB-audit 2026-05-21',
  '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab'
);
INSERT INTO evidence_sources_v1_legacy (
  ref_id, authors, year, title, doi, doi_less_key, pmid,
  tier, evidence_type, jurisdiction, metadata_quality, verification_status,
  notes, created_at, created_by_session, updated_at, updated_by_session
) VALUES (
  'REF-00735', 'Devos', '2019',
  'Dementia soundscape. PMC6950055', NULL, 'devos_2019_dementia_soundscape._pmc695005', NULL,
  3, 'clinical', 'INT', 'AUTHOR-TITLE-ONLY', NULL,
  'Displaced from REF-00571 by full-DB-audit 2026-05-21',
  '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab', '2026-05-21T00:00:00Z', 'session_2026-05-20-ato-rehab'
);

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
