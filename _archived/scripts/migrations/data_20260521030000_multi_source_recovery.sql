-- data_20260521030000_multi_source_recovery.sql
--
-- Multi-source ATO recovery follow-up. OpenAlex + Semantic Scholar probe surfaced
-- 6 single-source candidates from 55 ATO×no-ID rows. 4 of 6 verified canonical via
-- independent Crossref query (REF-00260 Szanton, REF-00728 Keall, REF-00730 Harper,
-- REF-00731 Szanton-displaced); 2 were wrong-author-year-collision and stay in queue.
--
-- REF-00260 and REF-00731 share canonical DOI (both Szanton 2019 JAMA Internal
-- Medicine CAPABLE RCT) — REF-00731 marked as POTENTIAL-DUPLICATE-OF-REF-00260 for
-- owner merge decision.
--
BEGIN TRANSACTION;

-- REF-00728: multi-source confirmed canonical upgrade
UPDATE evidence_sources SET
  doi = '10.1016/s2468-2667(21)00135-3',
  pub_title = COALESCE(NULLIF(pub_title,''), 'Home modifications to prevent home fall injuries in houses with Māori occupants (MHIPI): a randomised controlled trial'),
  pub_year = COALESCE(pub_year, 2021),
  journal_name = COALESCE(NULLIF(journal_name,''), 'The Lancet Public Health'),
  first_author_last = COALESCE(NULLIF(first_author_last,''), 'Keall'),
  first_author_first = COALESCE(NULLIF(first_author_first,''), 'Michael D'),
  author_display = COALESCE(NULLIF(author_display,''), 'Keall, M.; Tupara, H.; Pierse, N.; Wilkie, M.; Baker, M.; Howden-Chapman, P.; Cunningham, C.'),
  author_count = COALESCE(author_count, 7),
  author_count_is_complete = COALESCE(author_count_is_complete, 1),
  volume = COALESCE(NULLIF(volume,''), '6'),
  issue = COALESCE(NULLIF(issue,''), '9'),
  pages_start = COALESCE(NULLIF(pages_start,''), 'e631'),
  pages_end = COALESCE(NULLIF(pages_end,''), 'e640'),
  publisher = COALESCE(NULLIF(publisher,''), 'Elsevier BV'),
  issn = COALESCE(NULLIF(issn,''), '2468-2667'),
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | multi-source-recovery 2026-05-21T03:00:00Z: OpenAlex + Crossref independent confirmation of canonical DOI 10.1016/s2468-2667(21)00135-3. REF-00728 carries Keall MHIPI metadata displaced from REF-00069 on 2026-05-20; now identified as the actual Keall 2021 Lancet Public Health MHIPI study.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T03:00:00Z multi-source-recovery] CONFIRMED canonical via OpenAlex + Crossref',
  updated_at = '2026-05-21T03:00:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00728';

-- REF-00730: multi-source confirmed canonical upgrade
UPDATE evidence_sources SET
  doi = '10.1101/2022.03.25.22271716',
  pub_title = COALESCE(NULLIF(pub_title,''), 'Stairway visual contrast enhancement to reduce fall-related events'),
  pub_year = COALESCE(pub_year, 2022),
  journal_name = COALESCE(NULLIF(journal_name,''), NULL),
  first_author_last = COALESCE(NULLIF(first_author_last,''), 'Harper'),
  first_author_first = COALESCE(NULLIF(first_author_first,''), 'Sara A.'),
  author_display = COALESCE(NULLIF(author_display,''), 'Harper, S.; Long, C.; Corbridge, S.; Barrett, T.; Braeger, A.; Zollinger, B.; Hale, A.; Brown, C.'),
  author_count = COALESCE(author_count, 12),
  author_count_is_complete = COALESCE(author_count_is_complete, 1),
  volume = COALESCE(NULLIF(volume,''), NULL),
  issue = COALESCE(NULLIF(issue,''), NULL),
  pages_start = COALESCE(NULLIF(pages_start,''), NULL),
  pages_end = COALESCE(NULLIF(pages_end,''), NULL),
  publisher = COALESCE(NULLIF(publisher,''), 'openRxiv'),
  issn = COALESCE(NULLIF(issn,''), NULL),
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | multi-source-recovery 2026-05-21T03:00:00Z: OpenAlex + Crossref independent confirmation of canonical DOI 10.1101/2022.03.25.22271716. REF-00730 carries Harper metadata displaced from REF-00527 on 2026-05-20; now identified as Harper 2022 bioRxiv preprint on stairway visual contrast.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T03:00:00Z multi-source-recovery] CONFIRMED canonical via OpenAlex + Crossref',
  updated_at = '2026-05-21T03:00:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00730';

-- REF-00260: multi-source confirmed canonical upgrade
UPDATE evidence_sources SET
  doi = '10.1001/jamainternmed.2018.6026',
  pub_title = COALESCE(NULLIF(pub_title,''), 'Effect of a Biobehavioral Environmental Approach on Disability Among Low-Income Older Adults'),
  pub_year = COALESCE(pub_year, 2019),
  journal_name = COALESCE(NULLIF(journal_name,''), 'JAMA Internal Medicine'),
  first_author_last = COALESCE(NULLIF(first_author_last,''), 'Szanton'),
  first_author_first = COALESCE(NULLIF(first_author_first,''), 'Sarah L.'),
  author_display = COALESCE(NULLIF(author_display,''), 'Szanton, S.; Xue, Q.; Leff, B.; Guralnik, J.; Wolff, J.; Tanner, E.; Boyd, C.; Thorpe, R.'),
  author_count = COALESCE(author_count, 10),
  author_count_is_complete = COALESCE(author_count_is_complete, 1),
  volume = COALESCE(NULLIF(volume,''), '179'),
  issue = COALESCE(NULLIF(issue,''), '2'),
  pages_start = COALESCE(NULLIF(pages_start,''), '204'),
  pages_end = COALESCE(NULLIF(pages_end,''), NULL),
  publisher = COALESCE(NULLIF(publisher,''), 'American Medical Association (AMA)'),
  issn = COALESCE(NULLIF(issn,''), '2168-6106'),
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | multi-source-recovery 2026-05-21T03:00:00Z: OpenAlex + Crossref independent confirmation of canonical DOI 10.1001/jamainternmed.2018.6026. Original CAPABLE costing reference; resolves to Szanton 2019 JAMA Internal Medicine CAPABLE RCT main outcomes paper.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T03:00:00Z multi-source-recovery] CONFIRMED canonical via OpenAlex + Crossref',
  updated_at = '2026-05-21T03:00:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00260';

-- REF-00731: same canonical DOI as REF-00260 (both Szanton 2019 JAMA Int Med CAPABLE);
-- upgrade to canonical AND flag potential duplicate for owner merge decision
-- REF-00731: multi-source confirmed canonical upgrade
UPDATE evidence_sources SET
  doi = '10.1001/jamainternmed.2018.6026',
  pub_title = COALESCE(NULLIF(pub_title,''), 'Effect of a Biobehavioral Environmental Approach on Disability Among Low-Income Older Adults'),
  pub_year = COALESCE(pub_year, 2019),
  journal_name = COALESCE(NULLIF(journal_name,''), 'JAMA Internal Medicine'),
  first_author_last = COALESCE(NULLIF(first_author_last,''), 'Szanton'),
  first_author_first = COALESCE(NULLIF(first_author_first,''), 'Sarah L.'),
  author_display = COALESCE(NULLIF(author_display,''), 'Szanton, S.; Xue, Q.; Leff, B.; Guralnik, J.; Wolff, J.; Tanner, E.; Boyd, C.; Thorpe, R.'),
  author_count = COALESCE(author_count, 10),
  author_count_is_complete = COALESCE(author_count_is_complete, 1),
  volume = COALESCE(NULLIF(volume,''), '179'),
  issue = COALESCE(NULLIF(issue,''), '2'),
  pages_start = COALESCE(NULLIF(pages_start,''), '204'),
  pages_end = COALESCE(NULLIF(pages_end,''), NULL),
  publisher = COALESCE(NULLIF(publisher,''), 'American Medical Association (AMA)'),
  issn = COALESCE(NULLIF(issn,''), '2168-6106'),
  metadata_quality = 'COMPLETE',
  verification_status = 'VERIFIED',
  doi_resolution_outcome = 'RESOLVED',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | multi-source-recovery 2026-05-21T03:00:00Z: OpenAlex + Crossref independent confirmation of canonical DOI 10.1001/jamainternmed.2018.6026. REF-00731 carries Szanton metadata displaced from REF-00150 on 2026-05-20; now identified as the same Szanton 2019 paper as REF-00260. POTENTIAL DUPLICATE OF REF-00260 — owner: decide whether to merge.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T03:00:00Z multi-source-recovery] CONFIRMED canonical via OpenAlex + Crossref',
  updated_at = '2026-05-21T03:00:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00731';

-- REF-00731: override metadata_integrity_status to flag duplicate-of-REF-00260
UPDATE evidence_sources SET
  metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00260',
  metadata_integrity_detail = metadata_integrity_detail || ' | DUPLICATE FLAG: REF-00731 and REF-00260 both resolve to canonical DOI 10.1001/jamainternmed.2018.6026 (Szanton 2019 JAMA Int Med CAPABLE). Owner: merge or remove.',
  updated_at = '2026-05-21T03:00:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00731';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
