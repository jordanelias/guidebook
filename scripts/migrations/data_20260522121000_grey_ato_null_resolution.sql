-- data_20260522121000_grey_ato_null_resolution.sql
-- GREY×NULL + ATO×NULL Crossref-resolution batch: 7 rows verified.
-- Author + year + journal hints in DB used to title-search Crossref/PubMed; canonical metadata populated.
--
-- REF-00104: Askew, Fisher, Beazley 2020 J Psychiatr Ment Health Nurs 27(3):272-280 DOI 10.1111/jpm.12576
-- REF-00132: Iwarsson, Nygren, Slaug 2005 Scand J Occup Ther 12(1):29-39 DOI 10.1080/11038120510027144
-- REF-00135: Russell, Ormerod, Newton 2018 J Aging Res 2018:4904379 DOI 10.1155/2018/4904379
-- REF-00138: Zallio, Chivaran, Capece, Clarkson, Buono 2023 Strategic Des Res J 15(3):262-276 DOI 10.4013/sdrj.2022.153.04
-- REF-00219: Chaseling, Batlett, Capon, Crandall, Fiatarone Singh, Bi 2022 FASEB J 36(S1):R3555 DOI 10.1096/fasebj.2022.36.s1.r3555
-- REF-00407 + REF-00454: Putthinoi, Lersilp, Chakpitak 2017 J Aging Res 2017:2865960 DOI 10.1155/2017/2865960 PMID 28656108 PMC5471586

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Being in a Seclusion Room: The Forensic Psychiatric Inpatients'' Perspective',
    pub_year = 2020,
    first_author_last = 'Askew',
    first_author_first = 'L',
    is_corporate_primary = 0,
    author_display = 'Askew L, Fisher P, Beazley P',
    publisher = 'Wiley',
    journal_name = 'Journal of Psychiatric and Mental Health Nursing',
    journal_abbrev = 'J Psychiatr Ment Health Nurs',
    doi = '10.1111/jpm.12576',
    issn = '1351-0126',
    volume = '27',
    issue = '3',
    pages_start = '272',
    pages_end = '280',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-CROSSREF',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-resolution 2026-05-22T12:10:00Z: Crossref-resolved via author+year+journal hint; year corrected 2019→2020 (DB hint 2019 was pre-print year).',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T12:10:00Z',
    updated_at = '2026-05-22T12:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00104';

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Cross-national and multi-professional inter-rater reliability of the Housing Enabler',
    pub_year = 2005,
    first_author_last = 'Iwarsson',
    first_author_first = 'S',
    is_corporate_primary = 0,
    author_display = 'Iwarsson S, Nygren C, Slaug B',
    publisher = 'Informa UK Limited (Taylor & Francis)',
    journal_name = 'Scandinavian Journal of Occupational Therapy',
    journal_abbrev = 'Scand J Occup Ther',
    doi = '10.1080/11038120510027144',
    issn = '1103-8128',
    volume = '12',
    issue = '1',
    pages_start = '29',
    pages_end = '39',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-CROSSREF',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-resolution 2026-05-22T12:10:00Z: Crossref-resolved Housing Enabler validation study Iwarsson + Nygren + Slaug; Lund University Sweden.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T12:10:00Z',
    updated_at = '2026-05-22T12:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00132';

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'The Development of a Design and Construction Process Protocol to Support the Home Modification Process Carried Out by Older People',
    pub_year = 2018,
    first_author_last = 'Russell',
    first_author_first = 'R',
    is_corporate_primary = 0,
    author_display = 'Russell R, Ormerod M, Newton R',
    publisher = 'Hindawi (Wiley)',
    journal_name = 'Journal of Aging Research',
    journal_abbrev = 'J Aging Res',
    doi = '10.1155/2018/4904379',
    issn = '2090-2204',
    volume = '2018',
    article_number = '4904379',
    pages_start = '1',
    pages_end = '13',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-CROSSREF',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-resolution 2026-05-22T12:10:00Z: Crossref-resolved 4-phase 9-subphase OT-design protocol; Russell + Ormerod + Newton; University of Salford SURFACE Inclusive Design Research Centre.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T12:10:00Z',
    updated_at = '2026-05-22T12:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00135';

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Inclusive spatial learning experience',
    pub_year = 2023,
    first_author_last = 'Zallio',
    first_author_first = 'M',
    is_corporate_primary = 0,
    author_display = 'Zallio M, Chivaran C, Capece S, Clarkson PJ, Buono M',
    publisher = 'UNISINOS',
    journal_name = 'Strategic Design Research Journal',
    journal_abbrev = 'Strateg Des Res J',
    doi = '10.4013/sdrj.2022.153.04',
    issn = '1984-2988',
    volume = '15',
    issue = '3',
    pages_start = '262',
    pages_end = '276',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-CROSSREF',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-resolution 2026-05-22T12:10:00Z: Crossref-resolved Zallio + Chivaran + Capece + Clarkson + Buono 2023 IDEA framework spatial learning context Cambridge Engineering Design Centre.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T12:10:00Z',
    updated_at = '2026-05-22T12:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00138';

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Effects of Beta-Blockers on Thermal and Cardiovascular Strain of Adults With Coronary Artery Disease During Heat Exposure (conference abstract)',
    pub_year = 2022,
    first_author_last = 'Chaseling',
    first_author_first = 'G',
    is_corporate_primary = 0,
    author_display = 'Chaseling G, Batlett A-A, Capon A, Crandall C, Fiatarone Singh M, Bi P',
    publisher = 'Federation of American Societies for Experimental Biology (FASEB)',
    journal_name = 'The FASEB Journal',
    journal_abbrev = 'FASEB J',
    doi = '10.1096/fasebj.2022.36.s1.r3555',
    issn = '0892-6638',
    volume = '36',
    issue = 'S1',
    article_number = 'R3555',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-CROSSREF',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-resolution 2026-05-22T12:10:00Z: Crossref-resolved FASEB conference abstract; Chaseling et al. patient thermal resilience strategies. Companion 2024 full study Eur J Appl Physiol cold-water swilling.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T12:10:00Z',
    updated_at = '2026-05-22T12:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00219';

-- REF-00407 + REF-00454: Putthinoi 2017 J Aging Res cluster
UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Home Features and Assistive Technology for the Home-Bound Elderly in a Thai Suburban Community by Applying the International Classification of Functioning, Disability, and Health',
    pub_year = 2017,
    first_author_last = 'Putthinoi',
    first_author_first = 'S',
    is_corporate_primary = 0,
    author_display = 'Putthinoi S, Lersilp S, Chakpitak N',
    publisher = 'Hindawi (Wiley)',
    journal_name = 'Journal of Aging Research',
    journal_abbrev = 'J Aging Res',
    doi = '10.1155/2017/2865960',
    pmid = '28656108',
    pmcid = 'PMC5471586',
    issn = '2090-2204',
    volume = '2017',
    article_number = '2865960',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-PUBMED-CLUSTER',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-resolution 2026-05-22T12:10:00Z: PubMed-resolved PMID 28656108 + DOI 10.1155/2017/2865960 + PMC5471586 + 3-author Thai team (Chiang Mai University). Cluster member with REF-00454 (same PMID).',
    verified_by_tool = 'pubmed-eutils-resolution',
    last_verified_at = '2026-05-22T12:10:00Z',
    updated_at = '2026-05-22T12:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN ('REF-00407','REF-00454');

COMMIT;
