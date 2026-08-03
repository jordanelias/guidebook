-- data_20260522125000_grey_targeted_round2.sql
-- GREY targeted resolution round 2: 3 rows verified.
--
-- REF-00251: van Hoof J, Kort HSM, Hensen JLM, Duijnstee MSH, Rutten PGS (2010) Building & Environment 45(2):358-370 DOI 10.1016/j.buildenv.2009.06.013
-- REF-00393: Manandhar S, Lukman A, Dain SJ, Bridge CE, Relf M, Boon MY (2022) Work 73(4):1265-1278 DOI 10.3233/wor-210997
-- REF-00631: de Leeuw A, Happé F, Hoekstra RA (2020) Autism Research 13(7):1029-1050 DOI 10.1002/aur.2276

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Thermal comfort and the integrated design of homes for older people with dementia',
    pub_year = 2010,
    first_author_last = 'van Hoof',
    first_author_first = 'J',
    is_corporate_primary = 0,
    author_display = 'van Hoof J, Kort HSM, Hensen JLM, Duijnstee MSH, Rutten PGS',
    publisher = 'Elsevier BV',
    journal_name = 'Building and Environment',
    journal_abbrev = 'Build Environ',
    doi = '10.1016/j.buildenv.2009.06.013',
    issn = '0360-1323',
    volume = '45',
    issue = '2',
    pages_start = '358',
    pages_end = '370',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-ROUND2',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-round2 2026-05-22T12:50:00Z: Crossref-resolved canonical van Hoof Build Environ 2010 dementia thermal comfort paper; 5-author Eindhoven/Utrecht team; PMV/PPD discussion ground.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T12:50:00Z',
    updated_at = '2026-05-22T12:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00251';

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Luminance contrast preferences of people with a vision impairment for elements in the built environment',
    pub_year = 2022,
    first_author_last = 'Manandhar',
    first_author_first = 'S',
    is_corporate_primary = 0,
    author_display = 'Manandhar S, Lukman A, Dain SJ, Bridge CE, Relf M, Boon MY',
    publisher = 'IOS Press',
    journal_name = 'Work',
    journal_abbrev = 'Work',
    doi = '10.3233/wor-210997',
    issn = '1051-9815',
    volume = '73',
    issue = '4',
    pages_start = '1265',
    pages_end = '1278',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-ROUND2',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-round2 2026-05-22T12:50:00Z: Crossref-resolved LRV/luminance-contrast preferences VI population paper; 6-author UNSW Sydney team. Companion REF-00531 Canada LRV multi-jurisdictional cluster.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T12:50:00Z',
    updated_at = '2026-05-22T12:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00393';

UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'A Conceptual Framework for Understanding the Cultural and Contextual Factors on Autism Across the Globe',
    pub_year = 2020,
    first_author_last = 'de Leeuw',
    first_author_first = 'A',
    is_corporate_primary = 0,
    author_display = 'de Leeuw A, Happé F, Hoekstra RA',
    publisher = 'Wiley (INSAR)',
    journal_name = 'Autism Research',
    journal_abbrev = 'Autism Res',
    doi = '10.1002/aur.2276',
    issn = '1939-3792',
    volume = '13',
    issue = '7',
    pages_start = '1029',
    pages_end = '1050',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GREY-RESOLUTION-ROUND2',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-round2 2026-05-22T12:50:00Z: Crossref-resolved de Leeuw + Happé + Hoekstra 2020 Autism Research cross-cultural autism framework; King''s College London + IoPPN.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T12:50:00Z',
    updated_at = '2026-05-22T12:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00631';

COMMIT;
