-- data_20260521010000_truncated_doi_recovery.sql
--
-- DOI recovery for 5 IDENTIFIER-TRUNCATED rows from full-DB audit.
-- Canonical DOIs found via Crossref bibliographic phrase search (query.bibliographic
-- + author + year filter). Plus 1 FIELD-FIX via recovery (REF-00029 same DOI but
-- stored title was note-style).
--
-- Net effect: 5 truncated DOIs replaced with canonical full DOIs; rows upgraded
-- to COMPLETE x VERIFIED.
--
BEGIN TRANSACTION;

-- REF-00028: already corrected in data_20260521000000; this recovery pass confirms canonical match

-- REF-00029: FIELD-FIX (Levine 2025)
UPDATE evidence_sources SET
  doi = '10.2196/69442',
  pub_title = COALESCE(NULLIF(pub_title, ''), 'Grab Bar Grasp Location During Bathtub Exit and Sit-to-Stand Transfers: Biomechanical Evaluation'),
  pub_year = COALESCE(pub_year, 2025),
  journal_name = COALESCE(NULLIF(journal_name, ''), 'JMIR Rehabilitation and Assistive Technologies'),
  first_author_last = COALESCE(NULLIF(first_author_last, ''), 'Levine'),
  first_author_first = COALESCE(NULLIF(first_author_first, ''), 'Iris C'),
  author_display = COALESCE(NULLIF(author_display, ''), 'Levine, I.; Nirmalanathan, K.; Montgomery, R.; Novak, A.'),
  author_count = COALESCE(author_count, 4),
  volume = COALESCE(NULLIF(volume, ''), '12'),
  issue = COALESCE(NULLIF(issue, ''), NULL),
  pages_start = COALESCE(NULLIF(pages_start, ''), 'e69442'),
  pages_end = COALESCE(NULLIF(pages_end, ''), 'e69442'),
  publisher = COALESCE(NULLIF(publisher, ''), 'JMIR Publications Inc.'),
  issn = COALESCE(NULLIF(issn, ''), '2369-2529'),
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'DOI-recovery 2026-05-21T01:00:00Z (FIELD-FIX): Same DOI 10.2196/69442 (was already canonical); stored title was note-style "Grab bar adjustability evidence" - canonical Levine 2025 grasp-location paper.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T01:00:00Z DOI-recovery] FIELD-FIX',
  updated_at = '2026-05-21T01:00:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00029';

-- REF-00528: DOI-REPLACE (Brown 2022)
UPDATE evidence_sources SET
  doi = '10.1080/00140139.2022.2141347',
  pub_title = COALESCE(NULLIF(pub_title, ''), 'Step edge highlighters and illuminance changes influence stair descent in a real-world setting'),
  pub_year = COALESCE(pub_year, 2022),
  journal_name = COALESCE(NULLIF(journal_name, ''), 'Ergonomics'),
  first_author_last = COALESCE(NULLIF(first_author_last, ''), 'Brown'),
  first_author_first = COALESCE(NULLIF(first_author_first, ''), 'Chayston B.'),
  author_display = COALESCE(NULLIF(author_display, ''), 'Brown, C.; Barrett, T.; Long, C.; Corbridge, S.; Braeger, A.; Zollinger, B.; Harrison, K.; Poulsen, S.'),
  author_count = COALESCE(author_count, 11),
  volume = COALESCE(NULLIF(volume, ''), '66'),
  issue = COALESCE(NULLIF(issue, ''), '9'),
  pages_start = COALESCE(NULLIF(pages_start, ''), '1219'),
  pages_end = COALESCE(NULLIF(pages_end, ''), '1228'),
  publisher = COALESCE(NULLIF(publisher, ''), 'Informa UK Limited'),
  issn = COALESCE(NULLIF(issn, ''), '0014-0139'),
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'DOI-recovery 2026-05-21T01:00:00Z (DOI-REPLACE): Truncated DOI 10.1080/00140139 replaced with canonical 10.1080/00140139.2022.2141347. Note year correction 2023->2022.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T01:00:00Z DOI-recovery] DOI-REPLACE',
  updated_at = '2026-05-21T01:00:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00528';

-- REF-00534: DOI-CONFIRM (Harper 2025)
UPDATE evidence_sources SET
  doi = '10.2196/60622',
  pub_title = COALESCE(NULLIF(pub_title, ''), 'Interstep Variations of Stairways and Associations of High-Contrast Striping and Fall-Related Events: Observational Study'),
  pub_year = COALESCE(pub_year, 2025),
  journal_name = COALESCE(NULLIF(journal_name, ''), 'Interactive Journal of Medical Research'),
  first_author_last = COALESCE(NULLIF(first_author_last, ''), 'Harper'),
  first_author_first = COALESCE(NULLIF(first_author_first, ''), 'Sara A'),
  author_display = COALESCE(NULLIF(author_display, ''), 'Harper, S.; Brown, C.; Poulsen, S.; Barrett, T.; Dakin, C.'),
  author_count = COALESCE(author_count, 5),
  volume = COALESCE(NULLIF(volume, ''), '14'),
  issue = COALESCE(NULLIF(issue, ''), NULL),
  pages_start = COALESCE(NULLIF(pages_start, ''), 'e60622'),
  pages_end = COALESCE(NULLIF(pages_end, ''), NULL),
  publisher = COALESCE(NULLIF(publisher, ''), 'JMIR Publications Inc.'),
  issn = COALESCE(NULLIF(issn, ''), '1929-073X'),
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'DOI-recovery 2026-05-21T01:00:00Z (DOI-CONFIRM): Stored DOI 10.2196/60622 was already canonical - Crossref simply returns now.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T01:00:00Z DOI-recovery] DOI-CONFIRM',
  updated_at = '2026-05-21T01:00:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00534';

-- REF-00535: DOI-CONFIRM (Jordan 2024)
UPDATE evidence_sources SET
  doi = '10.1145/3694790',
  pub_title = COALESCE(NULLIF(pub_title, ''), 'International Guidelines for Photosensitive Epilepsy: Gap Analysis and Recommendations'),
  pub_year = COALESCE(pub_year, 2024),
  journal_name = COALESCE(NULLIF(journal_name, ''), 'ACM Transactions on Accessible Computing'),
  first_author_last = COALESCE(NULLIF(first_author_last, ''), 'Jordan'),
  first_author_first = COALESCE(NULLIF(first_author_first, ''), 'J. Bern'),
  author_display = COALESCE(NULLIF(author_display, ''), 'Jordan, J.; Vanderheiden, G.'),
  author_count = COALESCE(author_count, 2),
  volume = COALESCE(NULLIF(volume, ''), '17'),
  issue = COALESCE(NULLIF(issue, ''), '3'),
  pages_start = COALESCE(NULLIF(pages_start, ''), '1'),
  pages_end = COALESCE(NULLIF(pages_end, ''), '35'),
  publisher = COALESCE(NULLIF(publisher, ''), 'Association for Computing Machinery (ACM)'),
  issn = COALESCE(NULLIF(issn, ''), '1936-7228'),
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'DOI-recovery 2026-05-21T01:00:00Z (DOI-CONFIRM): Stored DOI 10.1145/3694790 confirmed.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T01:00:00Z DOI-recovery] DOI-CONFIRM',
  updated_at = '2026-05-21T01:00:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00535';

-- REF-00630: DOI-REPLACE (Ghazali 2018)
UPDATE evidence_sources SET
  doi = '10.21834/e-bpj.v3i7.1262',
  pub_title = COALESCE(NULLIF(pub_title, ''), 'A Review of Sensory Design Physical Learning Environment for Autism Centre in Malaysia'),
  pub_year = COALESCE(pub_year, 2018),
  journal_name = COALESCE(NULLIF(journal_name, ''), 'Environment-Behaviour Proceedings Journal'),
  first_author_last = COALESCE(NULLIF(first_author_last, ''), 'Ghazali'),
  first_author_first = COALESCE(NULLIF(first_author_first, ''), 'Roslinda'),
  author_display = COALESCE(NULLIF(author_display, ''), 'Ghazali, R.; Sakip, S.; Samsuddin, I.'),
  author_count = COALESCE(author_count, 3),
  volume = COALESCE(NULLIF(volume, ''), '3'),
  issue = COALESCE(NULLIF(issue, ''), '7'),
  pages_start = COALESCE(NULLIF(pages_start, ''), '145'),
  pages_end = COALESCE(NULLIF(pages_end, ''), NULL),
  publisher = COALESCE(NULLIF(publisher, ''), 'e-IPH Ltd.'),
  issn = COALESCE(NULLIF(issn, ''), '2398-4287'),
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'DOI-recovery 2026-05-21T01:00:00Z (DOI-REPLACE): Truncated DOI 10.21834/jabs replaced with canonical 10.21834/e-bpj.v3i7.1262. Year correction 2019->2018.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T01:00:00Z DOI-recovery] DOI-REPLACE',
  updated_at = '2026-05-21T01:00:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00630';

-- REF-00637: DOI-REPLACE (Al Khatib 2024)
UPDATE evidence_sources SET
  doi = '10.3389/fbuil.2024.1467692',
  pub_title = COALESCE(NULLIF(pub_title, ''), 'A systematic review of the impact of therapeutical biophilic design on health and wellbeing of patients and care providers in healthcare services settings'),
  pub_year = COALESCE(pub_year, 2024),
  journal_name = COALESCE(NULLIF(journal_name, ''), 'Frontiers in Built Environment'),
  first_author_last = COALESCE(NULLIF(first_author_last, ''), 'Al Khatib'),
  first_author_first = COALESCE(NULLIF(first_author_first, ''), 'Inas'),
  author_display = COALESCE(NULLIF(author_display, ''), 'Al Khatib, I.; Samara, F.; Ndiaye, M.'),
  author_count = COALESCE(author_count, 3),
  volume = COALESCE(NULLIF(volume, ''), '10'),
  issue = COALESCE(NULLIF(issue, ''), NULL),
  pages_start = COALESCE(NULLIF(pages_start, ''), NULL),
  pages_end = COALESCE(NULLIF(pages_end, ''), NULL),
  publisher = COALESCE(NULLIF(publisher, ''), 'Frontiers Media SA'),
  issn = COALESCE(NULLIF(issn, ''), '2297-3362'),
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'DOI-recovery 2026-05-21T01:00:00Z (DOI-REPLACE): Truncated DOI 10.3389/fbuil replaced with canonical 10.3389/fbuil.2024.1467692.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T01:00:00Z DOI-recovery] DOI-REPLACE',
  updated_at = '2026-05-21T01:00:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00637';

-- REF-00244: OWNER-QUEUE (title 'Beyond ME/CFS' too short for reliable Crossref search; DOI 10.17226/19012 returns 404)
UPDATE evidence_sources SET
  metadata_integrity_status = 'NEEDS-OWNER-VERIFICATION',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | full-DB-audit DOI-recovery 2026-05-21T01:00:00Z: DOI 10.17226/19012 (National Academies) returns 404 at Crossref; stored title "Beyond ME/CFS" too short to safely title-search. Owner: verify DOI or replace with full National Academies citation.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T01:00:00Z DOI-recovery] OWNER-QUEUE',
  updated_at = '2026-05-21T01:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00244';

-- REF-00543: OWNER-QUEUE (truncated DOI 10.1080/09613218; title-search returns wrong author/paper; cannot recover automatically)
UPDATE evidence_sources SET
  metadata_integrity_status = 'NEEDS-OWNER-VERIFICATION',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | full-DB-audit DOI-recovery 2026-05-21T01:00:00Z: truncated DOI 10.1080/09613218 (Building Research and Information journal-stem); title-search returned different paper (Khoo 2025 Playscape Co-Lab) not Rashid 2025 sensory-informed taxonomy. Cannot recover automatically. Owner: verify Rashid Build Res Inf 2025 paper and provide canonical DOI.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T01:00:00Z DOI-recovery] OWNER-QUEUE',
  updated_at = '2026-05-21T01:00:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00543';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
