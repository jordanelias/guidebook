-- data_20260520200000_ato_doi_rehab_batch_1.sql
--
-- AUTHOR-TITLE-ONLY × VERIFIED × has-DOI rehabilitation, batch 1 of 1 for
-- the DOI-bearing cohort (n=59).
--
-- Verdicts (matches /tmp/full_outcomes.json from probe_ato_verified_doi.py):
--   35 → COMPLETE (Crossref MATCH + PARTIAL + 1 diacritic-fp reclass)
--   18 → AUTHOR-TITLE-ONLY held with metadata_integrity_status=MISMATCH-*
--    6 → AUTHOR-TITLE-ONLY held with metadata_integrity_status=DOI-{TRUNCATED|404}
--
-- Schema dependency: migration 014 (metadata_integrity_status, metadata_integrity_detail).
--
BEGIN TRANSACTION;

-- REF-00002: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Journal of Applied Research in Intellectual Disabilities',
  journal_abbrev='Research Intellect Disabil',
  volume='38',
  issue='6',
  article_number='e70142',
  publisher='Wiley',
  issn='1360-2322',
  author_count_is_complete=1,
  pub_month=11,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00002';

-- REF-00008: HOLD-CROSSREF-MISMATCH → MISMATCH-AUTHOR
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-AUTHOR',
  metadata_integrity_detail='author:cr=''van der Kuil'' vs db=''van der Ham''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-AUTHOR',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00008';

-- REF-00009: ATO->COMPLETE-CROSSREF-PARTIAL
UPDATE evidence_sources SET
  journal_name='Disability Studies Quarterly',
  journal_abbrev='DSQ',
  volume='24',
  issue='3',
  publisher='The Ohio State University Libraries',
  issn='2159-8371',
  author_count_is_complete=1,
  pub_month=6,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00009';

-- REF-00012: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='HERD: Health Environments Research &amp; Design Journal',
  journal_abbrev='HERD',
  volume='16',
  issue='4',
  pages_start='172',
  pages_end='186',
  publisher='SAGE Publications',
  issn='1937-5867',
  author_count=5,
  author_count_is_complete=1,
  first_author_last='Elf',
  first_author_first='Marie',
  pub_month=6,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00012';

-- REF-00027: HOLD-CROSSREF-404 → DOI-TRUNCATED
UPDATE evidence_sources SET
  metadata_integrity_status='DOI-TRUNCATED',
  metadata_integrity_detail='stored DOI ''10.1080/10400435'' lacks article identifier suffix',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] DOI-TRUNCATED',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00027';

-- REF-00028: HOLD-CROSSREF-MISMATCH → MISMATCH-MULTI
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-MULTI',
  metadata_integrity_detail='title:cr=''Grab Bar Use Influences Fall Hazard During Bathtub Exit '' vs db=''Grab bar placement varies with body height (r=0.67). Human F'' ; year:cr=2021 vs db=2023',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-MULTI',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00028';

-- REF-00029: HOLD-CROSSREF-MISMATCH → MISMATCH-TITLE
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-TITLE',
  metadata_integrity_detail='title:cr=''Grab Bar Grasp Location During Bathtub Exit and Sit-to-Stand'' vs db=''Grab bar adjustability evidence. JMIR ''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-TITLE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00029';

-- REF-00041: HOLD-CROSSREF-MISMATCH → MISMATCH-AUTHOR
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-AUTHOR',
  metadata_integrity_detail='author:cr=''Hu'' vs db=''Clark''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-AUTHOR',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00041';

-- REF-00054: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  publisher='RIBA Publishing',
  first_author_last='Habinteg Housing Association',
  pub_month=9,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=monograph',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00054';

-- REF-00056: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  publisher='AOTA Press',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=book-set',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00056';

-- REF-00060: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Assistive Technology',
  volume='22',
  issue='1',
  pages_start='51',
  pages_end='67',
  publisher='Informa UK Limited',
  issn='1040-0435',
  author_count_is_complete=1,
  pub_month=3,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00060';

-- REF-00063: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  first_author_last='Habinteg Housing Association',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=monograph',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00063';

-- REF-00068: HOLD-CROSSREF-MISMATCH → MISMATCH-TITLE
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-TITLE',
  metadata_integrity_detail='title:cr=''Home modifications to reduce injuries from falls in the Home'' vs db=''HIPI study. Lancet 385:231–238. 61006-0 ''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-TITLE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00068';

-- REF-00069: HOLD-CROSSREF-MISMATCH → MISMATCH-MULTI
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-MULTI',
  metadata_integrity_detail='title:cr=''Design features that reduce the use of seclusion and restrai'' vs db=''MHIPI study. Lancet Public Health 6:e631–e640 '' ; author:cr=''Oostermeijer'' vs db=''Keall''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-MULTI',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00069';

-- REF-00091: HOLD-CROSSREF-MISMATCH → MISMATCH-TITLE
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-TITLE',
  metadata_integrity_detail='title:cr=''Applying Trauma-Informed Design Principles to Therapeutic Re'' vs db=''TID youth. PMC10689333 ''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-TITLE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00091';

-- REF-00096: HOLD-CROSSREF-MISMATCH → MISMATCH-MULTI
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-MULTI',
  metadata_integrity_detail='author:cr=''van Oel'' vs db=''Faerden'' ; year:cr=2020 vs db=2022',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-MULTI',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00096';

-- REF-00101: HOLD-CROSSREF-MISMATCH → MISMATCH-TITLE
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-TITLE',
  metadata_integrity_detail='title:cr=''Open Doors by Fair Means: a quasi-experimental controlled st'' vs db=''BMC Health Services Research — psychiatric architecture ''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-TITLE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00101';

-- REF-00102: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='BMJ Open',
  volume='13',
  issue='2',
  pages_start='e067943',
  publisher='BMJ',
  issn='2044-6055',
  author_count_is_complete=1,
  pub_month=2,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00102';

-- REF-00103: HOLD-CROSSREF-MISMATCH → MISMATCH-TITLE
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-TITLE',
  metadata_integrity_detail='title:cr=''A cross-sectional prospective study of seclusion, restraint '' vs db=''BMC Health Services Research — Norwegian acute psychiatry ''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-TITLE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00103';

-- REF-00107: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  publisher='Consortium Erudit',
  issn='0383-6320',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00107';

-- REF-00127: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Science',
  volume='224',
  issue='4647',
  pages_start='420',
  pages_end='421',
  publisher='American Association for the Advancement of Science (AAAS)',
  issn='0036-8075',
  pub_month=4,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00127';

-- REF-00136: HOLD-CROSSREF-MISMATCH → MISMATCH-TITLE
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-TITLE',
  metadata_integrity_detail='title:cr=''Inclusion, diversity, equity and accessibility in the built '' vs db=''Inclusive design failures. Build Environ ''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-TITLE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00136';

-- REF-00151: HOLD-CROSSREF-MISMATCH → MISMATCH-TITLE
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-TITLE',
  metadata_integrity_detail='title:cr=''Home modifications to reduce injuries from falls in the Home'' vs db=''HIPI study — 26% fall reduction. Lancet 385:231. 61006-0 ''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-TITLE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00151';

-- REF-00172: HOLD-CROSSREF-MISMATCH → MISMATCH-AUTHOR
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-AUTHOR',
  metadata_integrity_detail='author:cr=''Haber'' vs db=''Gibson''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-AUTHOR',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00172';

-- REF-00173: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  publisher='Psychology Press',
  pub_month=7,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=book',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00173';

-- REF-00176: HOLD-CROSSREF-MISMATCH → MISMATCH-AUTHOR
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-AUTHOR',
  metadata_integrity_detail='author:cr=''Weick'' vs db=''Barker''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-AUTHOR',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00176';

-- REF-00180: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='The Kawa Model',
  pages_start='109',
  pages_end='136',
  publisher='Elsevier',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=book-chapter',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00180';

-- REF-00246: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=book',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00246';

-- REF-00250: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='The American Journal of Occupational Therapy',
  volume='69',
  issue='5',
  pages_start='6905290020p1',
  pages_end='6905290020p11',
  publisher='AOTA Press',
  issn='0272-9490',
  author_count_is_complete=1,
  pub_month=9,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00250';

-- REF-00261: HOLD-CROSSREF-MISMATCH → MISMATCH-YEAR
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-YEAR',
  metadata_integrity_detail='year:cr=2021 vs db=2023',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-YEAR',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00261';

-- REF-00265: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Journal of Risk and Financial Management',
  pages_start='375',
  author_count_is_complete=1,
  first_author_last='Bailey',
  first_author_first='Jason R.',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00265';

-- REF-00266: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Journal of Risk and Financial Management',
  pages_start='146',
  author_count_is_complete=1,
  first_author_last='Bailey',
  first_author_first='Jason R.',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00266';

-- REF-00302: HOLD-CROSSREF-MISMATCH → MISMATCH-MULTI
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-MULTI',
  metadata_integrity_detail='author:cr=''Mauldin'' vs db=''Tibble'' ; year:cr=2022 vs db=2005',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-MULTI',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00302';

-- REF-00303: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  publisher='The Conversation',
  pub_month=7,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=posted-content',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00303';

-- REF-00332: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Hearing Research',
  pages_start='122',
  pages_end='132',
  publisher='Elsevier BV',
  issn='0378-5955',
  author_count=3,
  author_count_is_complete=1,
  first_author_last='Eurich',
  first_author_first='Bernhard',
  pub_month=6,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00332';

-- REF-00345: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  pub_subtitle='An Ethnographic Study in a Village in Ghana',
  pub_month=4,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=monograph',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00345';

-- REF-00398: ATO->COMPLETE-CROSSREF-MATCH-DIACRITIC
UPDATE evidence_sources SET
  journal_name='Vibration',
  volume='4',
  issue='2',
  pages_start='444',
  pages_end='481',
  publisher='MDPI AG',
  issn='2571-631X',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00398';

-- REF-00399: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Journal of Rehabilitation and Assistive Technologies Engineering',
  volume='9',
  article_number='20556683221092322',
  publisher='SAGE Publications',
  issn='2055-6683',
  pub_month=4,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00399';

-- REF-00478: HOLD-CROSSREF-MISMATCH → MISMATCH-AUTHOR
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-AUTHOR',
  metadata_integrity_detail='author:cr=''Lynch'' vs db=''Passini''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-AUTHOR',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00478';

-- REF-00482: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Advances in Child Development and Behavior',
  pages_start='9',
  pages_end='55',
  publisher='Elsevier',
  issn='0065-2407',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=book-chapter',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00482';

-- REF-00485: HOLD-CROSSREF-MISMATCH → MISMATCH-MULTI
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-MULTI',
  metadata_integrity_detail='author:cr=''Dillman-Hasso'' vs db=''Kaplan'' ; year:cr=2020 vs db=1989',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] MISMATCH-MULTI',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00485';

-- REF-00505: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Iconarp International J. of Architecture and Planning',
  journal_abbrev='ICONARP',
  article_number='1',
  publisher='Iconarp International Journal of Architecture and Planning',
  issn='2147-9380',
  author_count_is_complete=1,
  pub_month=6,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00505';

-- REF-00518: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Research in Autism Spectrum Disorders',
  volume='114',
  pages_start='102362',
  article_number='102362',
  publisher='Elsevier BV',
  issn='1750-9467',
  author_count_is_complete=1,
  pub_month=6,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00518';

-- REF-00519: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Concert Halls and Opera Houses',
  pages_start='37',
  pages_end='489',
  publisher='Springer New York',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=book-chapter',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00519';

-- REF-00525: ATO->COMPLETE-CROSSREF-PARTIAL
UPDATE evidence_sources SET
  journal_name='Australasian Journal on Ageing',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00525';

-- REF-00527: HOLD-CROSSREF-404 → DOI-TRUNCATED
UPDATE evidence_sources SET
  metadata_integrity_status='DOI-TRUNCATED',
  metadata_integrity_detail='stored DOI ''10.35248/2165-7556-22'' lacks article identifier suffix',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] DOI-TRUNCATED',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00527';

-- REF-00528: HOLD-CROSSREF-404 → DOI-TRUNCATED
UPDATE evidence_sources SET
  metadata_integrity_status='DOI-TRUNCATED',
  metadata_integrity_detail='stored DOI ''10.1080/00140139'' lacks article identifier suffix',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] DOI-TRUNCATED',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00528';

-- REF-00534: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Interactive Journal of Medical Research',
  pages_start='e60622',
  issn='1929-073X',
  pub_month=1,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00534';

-- REF-00543: HOLD-CROSSREF-404 → DOI-TRUNCATED
UPDATE evidence_sources SET
  metadata_integrity_status='DOI-TRUNCATED',
  metadata_integrity_detail='stored DOI ''10.1080/09613218'' lacks article identifier suffix',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] DOI-TRUNCATED',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00543';

-- REF-00544: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  pub_subtitle='',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=standard',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00544';

-- REF-00550: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='HERD: Health Environments Research &amp; Design Journal',
  journal_abbrev='HERD',
  volume='18',
  issue='4',
  pages_start='137',
  pages_end='149',
  publisher='SAGE Publications',
  issn='1937-5867',
  author_count_is_complete=1,
  pub_month=7,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00550';

-- REF-00602: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='PLOS ONE',
  journal_abbrev='PLoS ONE',
  volume='20',
  issue='1',
  pages_start='e0317266',
  publisher='Public Library of Science (PLoS)',
  issn='1932-6203',
  author_count=5,
  author_count_is_complete=1,
  first_author_last='Kates',
  first_author_first='James M.',
  pub_month=1,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00602';

-- REF-00605: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=dissertation',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00605';

-- REF-00609: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Autism',
  volume='28',
  issue='3',
  pages_start='644',
  pages_end='655',
  publisher='SAGE Publications',
  issn='1362-3613',
  author_count_is_complete=1,
  pub_month=7,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00609';

-- REF-00630: HOLD-CROSSREF-404 → DOI-TRUNCATED
UPDATE evidence_sources SET
  metadata_integrity_status='DOI-TRUNCATED',
  metadata_integrity_detail='stored DOI ''10.21834/jabs'' lacks article identifier suffix',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] DOI-TRUNCATED',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00630';

-- REF-00637: HOLD-CROSSREF-404 → DOI-TRUNCATED
UPDATE evidence_sources SET
  metadata_integrity_status='DOI-TRUNCATED',
  metadata_integrity_detail='stored DOI ''10.3389/fbuil'' lacks article identifier suffix',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] DOI-TRUNCATED',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00637';

-- REF-00638: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='International Journal of Environmental Research and Public Health',
  journal_abbrev='IJERPH',
  volume='20',
  issue='21',
  pages_start='6986',
  publisher='MDPI AG',
  issn='1660-4601',
  pub_month=10,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00638';

-- REF-00639: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='HERD: Health Environments Research &amp; Design Journal',
  journal_abbrev='HERD',
  volume='16',
  issue='1',
  pages_start='233',
  pages_end='250',
  publisher='SAGE Publications',
  issn='1937-5867',
  pub_month=8,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00639';

-- REF-00640: ATO->COMPLETE-CROSSREF-MATCH
UPDATE evidence_sources SET
  journal_name='Sustainability',
  volume='16',
  issue='9',
  pages_start='3639',
  publisher='MDPI AG',
  issn='2071-1050',
  pub_month=4,
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='crossref-resolved 2026-05-20T20:05:00Z; type=journal-article',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-DOI-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T20:05:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00640';

-- Record this migration's application
INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes)
VALUES (
  'data_20260520200000_ato_doi_rehab_batch_1',
  '2026-05-20T20:05:00Z',
  'computed-at-apply-time',
  'session_2026-05-20-ato-rehab',
  'AUTHOR-TITLE-ONLY × VERIFIED × DOI rehab batch 1: 35 upgrades to COMPLETE, 24 held with metadata_integrity_status flags'
);

COMMIT;

-- Summary: 35 upgrades, 24 integrity holds, total 59 rows touched.
