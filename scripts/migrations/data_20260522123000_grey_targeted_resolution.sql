-- data_20260522123000_grey_targeted_resolution.sql
-- GREY×NULL targeted resolution: 4 rows with strong Crossref hits.
--
-- REF-00099: van der Schaaf PS, Dusseldorp E, Keuning FM, Janssen WA, Noorthoorn EO (2013) BJP 202(2):142-149
-- REF-00098: Price E (2024) Sage Encyclopedia LGBTQ+ Studies — Dementia entry — OWNER-QUEUE topic mismatch with DB "EDITION study"
-- REF-00189: Hoover-Fong JE et al. (2022) Yearbook of Paediatric Endocrinology — achondroplasia growth
-- REF-00573: Bettarello F, Di Prisco M, Scavuzzo G, Caniato M (2025) Forum Acusticum proceedings — neurodivergent acoustic design

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Impact of the physical environment of psychiatric wards on the use of seclusion',
    pub_year = 2013,
    first_author_last = 'van der Schaaf',
    first_author_first = 'PS',
    is_corporate_primary = 0,
    author_display = 'van der Schaaf PS, Dusseldorp E, Keuning FM, Janssen WA, Noorthoorn EO',
    publisher = 'Cambridge University Press (Royal College of Psychiatrists)',
    journal_name = 'The British Journal of Psychiatry',
    journal_abbrev = 'Br J Psychiatry',
    doi = '10.1192/bjp.bp.112.118422',
    issn = '0007-1250',
    volume = '202',
    issue = '2',
    pages_start = '142',
    pages_end = '149',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-CROSSREF',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-targeted-resolution 2026-05-22T12:30:00Z: Crossref-resolved Dutch psychiatric-ward physical-environment seclusion study; 5-author roster populated.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T12:30:00Z',
    updated_at = '2026-05-22T12:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00099';

UPDATE evidence_sources SET
    pub_title = 'Dementia (encyclopedia entry)',
    pub_year = 2024,
    first_author_last = 'Price',
    first_author_first = 'E',
    is_corporate_primary = 0,
    author_display = 'Price E (Elizabeth)',
    publisher = 'SAGE Publications, Inc.',
    journal_name = 'The Sage Encyclopedia of LGBTQ+ Studies (book chapter; n126)',
    doi = '10.4135/9781071891414.n126',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OWNER-QUEUE-DB-DESCRIPTION-MISMATCH',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-targeted-resolution 2026-05-22T12:30:00Z: Crossref-resolved Sage Encyclopedia entry by Elizabeth Price (Brighton dementia researcher). DB description "EDITION study" does NOT match this entry — owner-queue: confirm whether REF-00098 cites this Sage entry or a different Price publication on EDITION trial.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T12:30:00Z',
    updated_at = '2026-05-22T12:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00098';

UPDATE evidence_sources SET
    pub_title = 'Growth in achondroplasia including stature, weight, weight-for-height and head circumference from CLARITY: Clinical and statistical insights from a multinational cohort',
    pub_year = 2022,
    first_author_last = 'Hoover-Fong',
    first_author_first = 'JE',
    is_corporate_primary = 0,
    author_display = 'Hoover-Fong JE, Schulze KJ, Alade AY, Bober MB, Gough E, Hashmi SS, Hecht JT, Legare JM',
    publisher = 'Bioscientifica Ltd (European Society for Paediatric Endocrinology)',
    journal_name = 'Yearbook of Paediatric Endocrinology (commentary/abstract)',
    journal_abbrev = 'Yearb Paediatr Endocrinol',
    doi = '10.1530/ey.19.5.8',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-CROSSREF',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-targeted-resolution 2026-05-22T12:30:00Z: Crossref-resolved Yearbook commentary on Hoover-Fong achondroplasia anthropometrics (n=1,374 CLARITY cohort); 8-author roster. Original primary research is Hoover-Fong et al. 2021 Genet Med — this Yearbook entry is commentary version. DB n=1,374 figure matches CLARITY cohort.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T12:30:00Z',
    updated_at = '2026-05-22T12:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00189';

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Acoustic Design Case Studies Of Educational Spaces For Neurodivergent Individuals',
    pub_year = 2025,
    first_author_last = 'Bettarello',
    first_author_first = 'F',
    is_corporate_primary = 0,
    author_display = 'Bettarello F, Di Prisco M, Scavuzzo G, Caniato M',
    publisher = 'European Acoustics Association (EAA) Forum Acusticum 2025',
    journal_name = 'Proceedings of the 11th Convention of the European Acoustics Association Forum Acusticum / EuroNoise 2025',
    doi = '10.61782/fa.2025.0068',
    pages_start = '6075',
    pages_end = '6079',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-CROSSREF',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-targeted-resolution 2026-05-22T12:30:00Z: Crossref-resolved Forum Acusticum / EuroNoise 2025 conference proceedings paper; Caniato M is co-author position #4 (DB first_author_last hint was salient-author indication, not Crossref position 1). 4-author roster Italian acoustic research team.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T12:30:00Z',
    updated_at = '2026-05-22T12:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00573';

COMMIT;
