-- data_20260521014500_remaining_statutory_individuals.sql
--
-- Three remaining individual statutory rows after Parts A/B/C bulk cleanup.
--
-- REF-00054 & REF-00148 are DUPLICATES — same DOI 10.4324/9781003564164 resolves
-- to "The Inclusive Housing Design Guide" 2024 RIBA Publishing, Habinteg
-- Housing Association corporate author. REF-00054 has correct corporate author;
-- REF-00148's "Runnalls" author is wrong-attribution.
--
-- REF-00054: field-fix (already COMPLETE; populate empty fields from canonical)
-- REF-00148: mark as duplicate of REF-00054; clear wrong author
-- REF-00261: field-fix with note-as-title caveat (DOI resolves to book chapter
--            about SF/DC mixed-income housing in general; stored title is a
--            specific Kelsey Civic Center note); populate empty fields, log
--            disagreement, keep AUTHOR-TITLE-ONLY

BEGIN TRANSACTION;

-- REF-00054: field-fix Inclusive Housing Design Guide
UPDATE evidence_sources SET
  pub_title = COALESCE(NULLIF(pub_title, ''), 'The Inclusive Housing Design Guide'),
  publisher = COALESCE(NULLIF(publisher, ''), 'RIBA Publishing'),
  pub_year = COALESCE(pub_year, 2024),
  isbn = COALESCE(NULLIF(isbn, ''), '9781003564164'),
  is_corporate_primary = 1,
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:45:00Z: field-fix from canonical (DOI 10.4324/9781003564164 → Habinteg Housing Association 2024 RIBA Publishing monograph). Note: REF-00148 is likely duplicate (same DOI).',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:45:00Z statutory-cohort-cleanup] field-fix; potential duplicate REF-00148',
  updated_at = '2026-05-21T01:45:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00054';

-- REF-00148: mark as potential duplicate of REF-00054; flag wrong author
UPDATE evidence_sources SET
  metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00054',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:45:00Z: same DOI 10.4324/9781003564164 as REF-00054 (Inclusive Housing Design Guide 2024 RIBA Publishing). Stored first_author_last "Runnalls" is wrong-attribution (canonical author is Habinteg Housing Association corporate). Owner: merge with REF-00054 or remove.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:45:00Z statutory-cohort-cleanup] duplicate-flag + wrong-author-attribution',
  updated_at = '2026-05-21T01:45:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00148';

-- REF-00261: field-fix with note-as-title caveat (Kelsey Civic Center)
UPDATE evidence_sources SET
  publisher = COALESCE(NULLIF(publisher, ''), 'Routledge'),
  first_author_last = COALESCE(NULLIF(first_author_last, ''), 'Hirsch'),
  first_author_first = COALESCE(NULLIF(first_author_first, ''), 'Joni'),
  author_display = COALESCE(NULLIF(author_display, ''), 'Hirsch, J.; Joseph, M.L.; Khare, A.T.'),
  author_count = COALESCE(author_count, 3),
  author_count_is_complete = COALESCE(author_count_is_complete, 1),
  pub_year = 2021,
  metadata_integrity_status = 'NOTE-AS-TITLE-OWNER-REVIEW',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:45:00Z: DOI 10.4324/9781003172949-10 resolves to Hirsch/Joseph/Khare 2021 Routledge book-chapter "Mixed-Income Public Housing Transformation in San Francisco and Washington, D.C." in "Cities and Affordable Housing". Stored title "The Kelsey Civic Center, San Francisco - 112-unit mixed-income disability-forward housing" is a specific case-study note that may be referenced within the chapter. Pub_year corrected 2023->2021 (canonical). Owner: confirm whether the row should describe (a) the chapter generally, or (b) a specific Kelsey case-study which may not be the chapter''s focus.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:45:00Z statutory-cohort-cleanup] field-fix; note-as-title flagged',
  updated_at = '2026-05-21T01:45:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00261';

-- Insert canonical author rows for REF-00261
INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES
('REF-00261', 1, 'Hirsch', 'Joni', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T01:45:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00261', 2, 'Joseph', 'Mark L.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T01:45:00Z', 'session_2026-05-20-ato-rehab'),
('REF-00261', 3, 'Khare', 'Amy T.', NULL, NULL, 0, NULL, NULL, 'author', '2026-05-21T01:45:00Z', 'session_2026-05-20-ato-rehab');

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
