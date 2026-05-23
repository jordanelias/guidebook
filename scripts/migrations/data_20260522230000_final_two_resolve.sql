-- data_20260522230000_final_two_resolve.sql
-- Final 2 open rows resolved per owner directive (retire if not verifiable; both verifiable).

BEGIN TRANSACTION;

-- REF-00191: McDowell US paediatric anthropometrics
-- DB description matches the McDowell-tradition NHANES anthropometric reference series.
-- Original McDowell-led editions: 1988-1994 (Vital Health Stat 11(249), 2009); 1999-2002 (Adv Data 361, 2005); 2003-2006 (Natl Health Stat 10, 2008).
-- Most recent (DB year 2021 matches): Fryar CD, Carroll MD, Gu Q, Afful J, Ogden CL (2021) Vital Health Stat 3(46):1-44 PMID 33541517 — series continues McDowell tradition.
UPDATE evidence_sources SET
    source_type = 'government_report',
    pub_title = 'Anthropometric Reference Data for Children and Adults: United States, 2015–2018',
    pub_year = 2021,
    first_author_last = 'Fryar',
    first_author_first = 'CD',
    is_corporate_primary = 0,
    author_display = 'Fryar CD, Carroll MD, Gu Q, Afful J, Ogden CL — National Center for Health Statistics (NCHS), CDC; continues McDowell-led NHANES anthropometric series (McDowell MA et al. 1988-1994 / 1999-2002 / 2003-2006)',
    publisher = 'U.S. Department of Health and Human Services, Centers for Disease Control and Prevention, National Center for Health Statistics (NCHS), Hyattsville MD',
    journal_name = 'Vital and Health Statistics, Series 3: Analytical and Epidemiological Studies',
    journal_abbrev = 'Vital Health Stat 3',
    pmid = '33541517',
    volume = '3',
    issue = '46',
    pages_start = '1',
    pages_end = '44',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'MCDOWELL-TRADITION-NHANES-SERIES',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | final-two 2026-05-22T23:00:00Z: web-search verified at cdc.gov/nchs/data/series/sr_03 + pubmed.ncbi.nlm.nih.gov/33541517. DB "McDowell M.A. 2021" reflects the McDowell-tradition NHANES series; canonical 2021 update is Fryar CD et al. continuing the series McDowell originally led (1988-1994 + 1999-2002 + 2003-2006 editions). 2025 successor edition (NCHS Series 3 No. 50, August 2021-August 2023 data) exists but DB year 2021 maps to the 2015-2018 data edition published 2021.',
    url = 'https://www.cdc.gov/nchs/data/series/sr_03/sr03-046-508.pdf',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search+pubmed+cdc-nchs',
    last_verified_at = '2026-05-22T23:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T23:00:00Z final-two] McDowell-tradition resolved',
    updated_at = '2026-05-22T23:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00191';

-- REF-00224: Newcastle POTS clinic
-- Match: Strassheim V, Welford J, Ballantine R, Newton JL (2018) "Managing fatigue in postural tachycardia syndrome (PoTS): The Newcastle approach"
UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Managing fatigue in postural tachycardia syndrome (PoTS): The Newcastle approach',
    pub_year = 2018,
    first_author_last = 'Strassheim',
    first_author_first = 'V',
    is_corporate_primary = 0,
    author_display = 'Strassheim V, Welford J, Ballantine R, Newton JL — Newcastle Hospitals NHS Foundation Trust + Newcastle University Cardiovascular Autonomic Disorders Service',
    publisher = 'Elsevier BV',
    journal_name = 'Autonomic Neuroscience: Basic and Clinical',
    journal_abbrev = 'Auton Neurosci',
    doi = '10.1016/j.autneu.2018.02.003',
    issn = '1566-0702',
    volume = '215',
    pages_start = '56',
    pages_end = '61',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'NEWCASTLE-POTS-APPROACH-PUBLISHED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | final-two 2026-05-22T23:00:00Z: Crossref + web-search confirmed. Covers thermal/weather management (warm-weather vasodilation, compression stockings, environmental-demand management) — direct match for DB "POTS thermal triggers — clinical guidance" framing. Julia Newton is senior author (4th position); first author Victoria Strassheim. DB "Newcastle POTS clinic" attribution is correct.',
    url = 'https://www.autonomicneuroscience.com/article/S1566-0702(17)30328-4/fulltext',
    url_accessed = '2026-05-22',
    verified_by_tool = 'crossref-api+web-search',
    last_verified_at = '2026-05-22T23:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T23:00:00Z final-two] Newcastle PoTS approach resolved',
    updated_at = '2026-05-22T23:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00224';

COMMIT;
