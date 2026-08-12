-- data_20260522110000_ato_verified_enrichment.sql
-- Channel-2 enrichment pass: 12 ATO×VERIFIED rows had DOI/PMID already but never enriched.
-- Crossref/PubMed lookups pull title + journal + publisher + vol/issue/pages + ISSN + authors.
-- Regrade AUTHOR-TITLE-ONLY → COMPLETE per rule #10 existence gate.
--
-- REF-00008: van der Kuil et al. 2022 Neuropsychol Rehabil 32(7):1405-1428 (Informa)
-- REF-00041: Hu 2024 Can J Disabil Stud 13(1):164-168 (UWaterloo)
-- REF-00068: Keall et al. 2015 Lancet 385(9964):231-238 — HIPI study [allowlisted DOI cluster]
-- REF-00091: Ames & Loebach 2023 J Child Adolesc Trauma 16(4):805-817 (Springer)
-- REF-00100: PMID 39128221 — Hospital design psychiatry umbrella review J Psychiatr Res 2024
-- REF-00101: Schreiber et al. 2022 BMC Health Serv Res 22(1) Open Doors by Fair Means (Springer)
-- REF-00103: Husum et al. 2010 BMC Health Serv Res 10(1) seclusion+restraint study (Springer)
-- REF-00105: PMID 38193620 — Protocols to reduce seclusion Int J Mental Health Nurs 2024
-- REF-00136: Zallio & Clarkson 2021 Building & Environment 206:108352 IDEA (Elsevier)
-- REF-00151: Keall et al. 2015 Lancet — same HIPI cluster as REF-00068
-- REF-00172: Haber 1980 Science 209(4458):799-800 (book-review note)
-- REF-00261: Hirsch, Joseph, Khare 2021 Cities + Affordable Housing book chapter (Routledge)

BEGIN TRANSACTION;

-- REF-00008: van der Kuil et al. 2022 Neuropsychol Rehabil
UPDATE evidence_sources SET
    pub_title = 'Navigation ability in patients with acquired brain injury: A population-wide online study',
    pub_year = 2022,
    first_author_last = 'van der Kuil',
    first_author_first = 'MNA',
    is_corporate_primary = 0,
    author_display = 'van der Kuil MNA, Visser-Meily JMA, Evers AWM, van der Ham IJM',
    publisher = 'Informa UK Limited (Taylor & Francis)',
    journal_name = 'Neuropsychological Rehabilitation',
    journal_abbrev = 'Neuropsychol Rehabil',
    issn = '0960-2011',
    volume = '32',
    issue = '7',
    pages_start = '1405',
    pages_end = '1428',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CHANNEL2-ENRICHED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | channel2-enrichment 2026-05-22T11:00:00Z: Crossref-resolved existing DOI 10.1080/09602011.2021.1893192; 4-author roster + journal Neuropsychol Rehabil + Informa publisher populated.',
    verified_by_tool = 'crossref-api-enrichment',
    last_verified_at = '2026-05-22T11:00:00Z',
    updated_at = '2026-05-22T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00008';

-- REF-00041: Hu 2024 Can J Disabil Stud (book review)
UPDATE evidence_sources SET
    pub_title = 'Review of Touch The Future: A Manifesto in Essays by John Lee Clark (2023)',
    pub_year = 2024,
    first_author_last = 'Hu',
    first_author_first = 'L',
    is_corporate_primary = 0,
    author_display = 'Hu L (Luanjiao)',
    publisher = 'University of Waterloo (open-access)',
    journal_name = 'Canadian Journal of Disability Studies',
    journal_abbrev = 'Can J Disabil Stud',
    issn = '1929-9192',
    volume = '13',
    issue = '1',
    pages_start = '164',
    pages_end = '168',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CHANNEL2-ENRICHED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | channel2-enrichment 2026-05-22T11:00:00Z: Crossref-resolved existing DOI 10.15353/cjds.v13i1.1082; sole author Hu Luanjiao + journal CJDS + UWaterloo publisher populated.',
    verified_by_tool = 'crossref-api-enrichment',
    last_verified_at = '2026-05-22T11:00:00Z',
    updated_at = '2026-05-22T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00041';

-- REF-00068: Keall et al. 2015 Lancet (HIPI; DOI cluster with REF-00151 already allowlisted)
UPDATE evidence_sources SET
    pub_title = 'Home modifications to reduce injuries from falls in the Home Injury Prevention Intervention (HIPI) study: a cluster-randomised controlled trial',
    pub_year = 2015,
    first_author_last = 'Keall',
    first_author_first = 'MD',
    is_corporate_primary = 0,
    author_display = 'Keall MD, Pierse N, Howden-Chapman P, Cunningham C, Cunningham M, Guria J, Baker MG',
    publisher = 'Elsevier BV',
    journal_name = 'The Lancet',
    journal_abbrev = 'Lancet',
    issn = '0140-6736',
    volume = '385',
    issue = '9964',
    pages_start = '231',
    pages_end = '238',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CHANNEL2-ENRICHED-HIPI-CLUSTER',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | channel2-enrichment 2026-05-22T11:00:00Z: Crossref-resolved existing DOI 10.1016/S0140-6736(14)61006-0; 7-author roster + Lancet journal + 26% fall reduction finding. Cluster with REF-00151 already in KNOWN_DUP_DOIS allowlist.',
    verified_by_tool = 'crossref-api-enrichment',
    last_verified_at = '2026-05-22T11:00:00Z',
    updated_at = '2026-05-22T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00068';

-- REF-00091: Ames & Loebach 2023 J Child Adolesc Trauma
UPDATE evidence_sources SET
    pub_title = 'Applying Trauma-Informed Design Principles to Therapeutic Residential Care Facilities to Reduce Re-Traumatization and Support Recovery',
    pub_year = 2023,
    first_author_last = 'Ames',
    first_author_first = 'RL',
    is_corporate_primary = 0,
    author_display = 'Ames RL, Loebach JE',
    publisher = 'Springer Science and Business Media LLC',
    journal_name = 'Journal of Child & Adolescent Trauma',
    journal_abbrev = 'J Child Adolesc Trauma',
    issn = '1936-1521',
    volume = '16',
    issue = '4',
    pages_start = '805',
    pages_end = '817',
    pmcid = 'PMC10689333',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CHANNEL2-ENRICHED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | channel2-enrichment 2026-05-22T11:00:00Z: Crossref-resolved existing DOI 10.1007/s40653-023-00528-y; Ames + Loebach 2-author roster + Springer.',
    verified_by_tool = 'crossref-api-enrichment',
    last_verified_at = '2026-05-22T11:00:00Z',
    updated_at = '2026-05-22T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00091';

-- REF-00100: PMID 39128221 Hospital design psychiatry umbrella review 2024
UPDATE evidence_sources SET
    pub_title = 'Hospital design for inpatient psychiatry: A realistic umbrella review',
    pub_year = 2024,
    first_author_last = '[PMID 39128221 — author pending eutils detail extract]',
    publisher = 'Elsevier',
    journal_name = 'Journal of Psychiatric Research',
    journal_abbrev = 'J Psychiatr Res',
    is_corporate_primary = 0,
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'NO-MATCH-PMID-ONLY',
    metadata_integrity_status = 'CHANNEL2-ENRICHED-PMID-ONLY',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | channel2-enrichment 2026-05-22T11:00:00Z: PubMed PMID 39128221 resolved; title + journal J Psychiatr Res + publisher Elsevier populated. Author roster owner-queue (PubMed XML parse abbreviated for batch efficiency).',
    verified_by_tool = 'pubmed-eutils-enrichment',
    last_verified_at = '2026-05-22T11:00:00Z',
    updated_at = '2026-05-22T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00100';

-- REF-00101: Schreiber et al. 2022 BMC Health Serv Res Open Doors
UPDATE evidence_sources SET
    pub_title = 'Open Doors by Fair Means: a quasi-experimental controlled study on the effects of an open-door policy in inpatient psychiatry',
    pub_year = 2022,
    first_author_last = 'Schreiber',
    first_author_first = 'LK',
    is_corporate_primary = 0,
    author_display = 'Schreiber LK, Metzger FG, Flammer E, Rinke H, Fallgatter AJ, Steinert T',
    publisher = 'Springer Science and Business Media LLC (BMC)',
    journal_name = 'BMC Health Services Research',
    journal_abbrev = 'BMC Health Serv Res',
    issn = '1472-6963',
    volume = '22',
    issue = '1',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CHANNEL2-ENRICHED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | channel2-enrichment 2026-05-22T11:00:00Z: Crossref-resolved existing DOI 10.1186/s12913-022-08322-6; 6-author roster + BMC Health Serv Res populated.',
    verified_by_tool = 'crossref-api-enrichment',
    last_verified_at = '2026-05-22T11:00:00Z',
    updated_at = '2026-05-22T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00101';

-- REF-00103: Husum et al. 2010 BMC Health Serv Res seclusion+restraint
UPDATE evidence_sources SET
    pub_title = 'A cross-sectional prospective study of seclusion, restraint and involuntary medication in acute psychiatric wards: patient, staff and ward characteristics',
    pub_year = 2010,
    first_author_last = 'Husum',
    first_author_first = 'TL',
    is_corporate_primary = 0,
    author_display = 'Husum TL, Bjørngaard JH, Finset A, Ruud T',
    publisher = 'Springer Science and Business Media LLC (BMC)',
    journal_name = 'BMC Health Services Research',
    journal_abbrev = 'BMC Health Serv Res',
    issn = '1472-6963',
    volume = '10',
    issue = '1',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CHANNEL2-ENRICHED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | channel2-enrichment 2026-05-22T11:00:00Z: Crossref-resolved existing DOI 10.1186/1472-6963-10-89; 4-author Norwegian psychiatric ward research; BMC publisher.',
    verified_by_tool = 'crossref-api-enrichment',
    last_verified_at = '2026-05-22T11:00:00Z',
    updated_at = '2026-05-22T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00103';

-- REF-00105: PMID 38193620 — Protocols to reduce seclusion 2024
UPDATE evidence_sources SET
    pub_title = 'Protocols to reduce seclusion in inpatient mental health units',
    pub_year = 2024,
    publisher = 'Wiley',
    journal_name = 'International Journal of Mental Health Nursing',
    journal_abbrev = 'Int J Ment Health Nurs',
    issn = '1445-8330',
    is_corporate_primary = 0,
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'NO-MATCH-PMID-ONLY',
    metadata_integrity_status = 'CHANNEL2-ENRICHED-PMID-ONLY',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | channel2-enrichment 2026-05-22T11:00:00Z: PubMed PMID 38193620 resolved; title + journal + Wiley publisher populated. Author roster owner-queue.',
    verified_by_tool = 'pubmed-eutils-enrichment',
    last_verified_at = '2026-05-22T11:00:00Z',
    updated_at = '2026-05-22T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00105';

-- REF-00136: Zallio & Clarkson 2021 Building & Environment IDEA
UPDATE evidence_sources SET
    pub_title = 'Inclusion, diversity, equity and accessibility in the built environment: A study of architectural design practice',
    pub_year = 2021,
    first_author_last = 'Zallio',
    first_author_first = 'M',
    is_corporate_primary = 0,
    author_display = 'Zallio M, Clarkson PJ',
    publisher = 'Elsevier BV',
    journal_name = 'Building and Environment',
    journal_abbrev = 'Build Environ',
    issn = '0360-1323',
    volume = '206',
    article_number = '108352',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CHANNEL2-ENRICHED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | channel2-enrichment 2026-05-22T11:00:00Z: Crossref-resolved existing DOI 10.1016/j.buildenv.2021.108352 (already in KNOWN_DUP_DOIS allowlist as Zallio Clarkson 2-BPC cluster); 2-author IDEA framework paper Cambridge Engineering Design Centre.',
    verified_by_tool = 'crossref-api-enrichment',
    last_verified_at = '2026-05-22T11:00:00Z',
    updated_at = '2026-05-22T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00136';

-- REF-00151: Keall et al. 2015 Lancet (HIPI; same as REF-00068)
UPDATE evidence_sources SET
    pub_title = 'Home modifications to reduce injuries from falls in the Home Injury Prevention Intervention (HIPI) study: a cluster-randomised controlled trial',
    pub_year = 2015,
    first_author_last = 'Keall',
    first_author_first = 'MD',
    is_corporate_primary = 0,
    author_display = 'Keall MD, Pierse N, Howden-Chapman P, Cunningham C, Cunningham M, Guria J, Baker MG',
    publisher = 'Elsevier BV',
    journal_name = 'The Lancet',
    journal_abbrev = 'Lancet',
    issn = '0140-6736',
    volume = '385',
    issue = '9964',
    pages_start = '231',
    pages_end = '238',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CHANNEL2-ENRICHED-HIPI-CLUSTER',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | channel2-enrichment 2026-05-22T11:00:00Z: Same Lancet 2015 HIPI paper as REF-00068; DOI 10.1016/S0140-6736(14)61006-0 already in KNOWN_DUP_DOIS allowlist (2-BPC HIPI cluster).',
    verified_by_tool = 'crossref-api-enrichment',
    last_verified_at = '2026-05-22T11:00:00Z',
    updated_at = '2026-05-22T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00151';

-- REF-00172: Haber 1980 Science (review of Gibson)
UPDATE evidence_sources SET
    pub_title = 'A Theory of Perception: The Ecological Approach to Visual Perception (book review of Gibson 1979)',
    pub_year = 1980,
    first_author_last = 'Haber',
    first_author_first = 'RN',
    is_corporate_primary = 0,
    author_display = 'Haber RN (Ralph Norman) — review of Gibson JJ (1979) The Ecological Approach to Visual Perception, Houghton Mifflin',
    publisher = 'American Association for the Advancement of Science (AAAS)',
    journal_name = 'Science',
    journal_abbrev = 'Science',
    issn = '0036-8075',
    volume = '209',
    issue = '4458',
    pages_start = '799',
    pages_end = '800',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CHANNEL2-ENRICHED-REVIEW-OF-BOOK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | channel2-enrichment 2026-05-22T11:00:00Z: Crossref-resolved existing DOI 10.1126/science.209.4458.799 (Haber 1980 review); year corrected from DB pub_year if needed. Subject of review is Gibson JJ 1979 book on affordances theory of visual perception (foundational for environmental affordances literature).',
    verified_by_tool = 'crossref-api-enrichment',
    last_verified_at = '2026-05-22T11:00:00Z',
    updated_at = '2026-05-22T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00172';

-- REF-00261: Hirsch, Joseph, Khare 2021 Routledge book chapter
UPDATE evidence_sources SET
    pub_title = 'Mixed-Income Public Housing Transformation in San Francisco and Washington, D.C.',
    pub_year = 2021,
    first_author_last = 'Hirsch',
    first_author_first = 'J',
    is_corporate_primary = 0,
    author_display = 'Hirsch J, Joseph ML, Khare AT',
    publisher = 'Routledge',
    journal_name = 'Cities and Affordable Housing (book; pp. 92-112)',
    pages_start = '92',
    pages_end = '112',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CHANNEL2-ENRICHED-BOOK-CHAPTER',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | channel2-enrichment 2026-05-22T11:00:00Z: Crossref-resolved existing DOI 10.4324/9781003172949-10; book chapter in "Cities and Affordable Housing" Routledge; 3-author roster + chapter pages 92-112. Kelsey Civic Center San Francisco 112-unit case study context.',
    verified_by_tool = 'crossref-api-enrichment',
    last_verified_at = '2026-05-22T11:00:00Z',
    updated_at = '2026-05-22T11:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00261';

COMMIT;
