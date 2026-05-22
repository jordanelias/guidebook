-- data_20260522104000_grey_regrade_pass2.sql
-- SQL-regrade pass 2: 5 GREY rows with valid DOIs.
-- Each row already had a DOI in DB but was misclassified at GREY with placeholder title.
-- Pull canonical metadata from Crossref + regrade GREY→COMPLETE.
--
-- REF-00356: Stark S, Keglovits M, Arbesman M, Lieberman D (2017) AJOT 71(2):7102290010
-- REF-00363: Gitlin LN, Winter L, Dennis MP, Corcoran M, Schinfeld S, Hauck WW (2006) JAGS 54(5):809-816
-- REF-00368: Greene R, Levine IC, Guay M, Novak AC (2024) Can J Occup Ther 91(2):183-193
-- REF-00371: Guay M et al. (2020) JMIR 22(8):e16175
-- REF-00242: Hersche R, Weise A (2022) Occup Ther Int 2022:4590154

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    pub_title = 'Effect of Home Modification Interventions on the Participation of Community-Dwelling Adults With Health Conditions: A Systematic Review',
    first_author_last = 'Stark',
    first_author_first = 'S',
    is_corporate_primary = 0,
    author_display = 'Stark S, Keglovits M, Arbesman M, Lieberman D',
    publisher = 'AOTA Press',
    journal_name = 'The American Journal of Occupational Therapy',
    journal_abbrev = 'Am J Occup Ther',
    issn = '0272-9490',
    volume = '71',
    issue = '2',
    article_number = '7102290010',
    pages_start = '7102290010p1',
    pages_end = '7102290010p11',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'REGRADE-FROM-GREY-PASS2',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-regrade-pass2 2026-05-22T10:40:00Z: Crossref-resolved DOI 10.5014/ajot.2017.018887; title + journal + publisher + 4-author roster populated; regraded GREY→COMPLETE per rule #10 existence gate.',
    verified_by_tool = 'crossref-api-resolve+grey-regrade-pass2',
    last_verified_at = '2026-05-22T10:40:00Z',
    updated_at = '2026-05-22T10:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00356';

UPDATE evidence_sources SET
    pub_title = 'A Randomized Trial of a Multicomponent Home Intervention to Reduce Functional Difficulties in Older Adults',
    first_author_last = 'Gitlin',
    first_author_first = 'LN',
    is_corporate_primary = 0,
    author_display = 'Gitlin LN, Winter L, Dennis MP, Corcoran M, Schinfeld S, Hauck WW',
    publisher = 'Wiley',
    journal_name = 'Journal of the American Geriatrics Society',
    journal_abbrev = 'J Am Geriatr Soc',
    issn = '0002-8614',
    volume = '54',
    issue = '5',
    pages_start = '809',
    pages_end = '816',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'REGRADE-FROM-GREY-PASS2',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-regrade-pass2 2026-05-22T10:40:00Z: Crossref-resolved DOI 10.1111/j.1532-5415.2006.00703.x; title + journal JAGS + publisher Wiley + 6-author roster populated; regraded GREY→COMPLETE.',
    verified_by_tool = 'crossref-api-resolve+grey-regrade-pass2',
    last_verified_at = '2026-05-22T10:40:00Z',
    updated_at = '2026-05-22T10:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00363';

UPDATE evidence_sources SET
    pub_title = 'Biomechanical Demands and User Preference Associated with Wall-Mounted and Rim-Mounted Grab Bars',
    first_author_last = 'Greene',
    first_author_first = 'R',
    is_corporate_primary = 0,
    author_display = 'Greene R, Levine IC, Guay M, Novak AC',
    publisher = 'SAGE Publications',
    journal_name = 'Canadian Journal of Occupational Therapy',
    journal_abbrev = 'Can J Occup Ther',
    issn = '0008-4174',
    volume = '91',
    issue = '2',
    pages_start = '183',
    pages_end = '193',
    pub_year = 2024,
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'REGRADE-FROM-GREY-PASS2',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-regrade-pass2 2026-05-22T10:40:00Z: Crossref-resolved DOI 10.1177/00084174231186066; title + journal CJOT + publisher SAGE + 4-author roster populated; regraded GREY→COMPLETE.',
    verified_by_tool = 'crossref-api-resolve+grey-regrade-pass2',
    last_verified_at = '2026-05-22T10:40:00Z',
    updated_at = '2026-05-22T10:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00368';

UPDATE evidence_sources SET
    pub_title = 'Self-Selection of Bathroom-Assistive Technology: Development of an Electronic Decision Support System (Hygiene 2.0)',
    first_author_last = 'Guay',
    first_author_first = 'M',
    is_corporate_primary = 0,
    author_display = 'Guay M, Latulippe K, Auger C, Giroux D, Séguin-Tremblay N, Gauthier J, Genest C, Morales E, Vincent C',
    publisher = 'JMIR Publications Inc.',
    journal_name = 'Journal of Medical Internet Research',
    journal_abbrev = 'J Med Internet Res',
    issn = '1438-8871',
    volume = '22',
    issue = '8',
    article_number = 'e16175',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'REGRADE-FROM-GREY-PASS2',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-regrade-pass2 2026-05-22T10:40:00Z: Crossref-resolved DOI 10.2196/16175; title + journal JMIR + publisher + 9-author roster populated; regraded GREY→COMPLETE.',
    verified_by_tool = 'crossref-api-resolve+grey-regrade-pass2',
    last_verified_at = '2026-05-22T10:40:00Z',
    updated_at = '2026-05-22T10:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00371';

UPDATE evidence_sources SET
    pub_title = 'Occupational Therapy-Based Energy Management Education in People with Post-COVID-19 Condition-Related Fatigue: Results from a Focus Group Discussion',
    first_author_last = 'Hersche',
    first_author_first = 'R',
    is_corporate_primary = 0,
    author_display = 'Hersche R, Weise A',
    publisher = 'Wiley',
    journal_name = 'Occupational Therapy International',
    journal_abbrev = 'Occup Ther Int',
    issn = '0966-7903',
    volume = '2022',
    article_number = '4590154',
    pages_start = '1',
    pages_end = '9',
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'REGRADE-FROM-GREY-PASS2',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | grey-regrade-pass2 2026-05-22T10:40:00Z: Crossref-resolved DOI 10.1155/2022/4590154; title + journal Occup Ther Int + publisher Wiley + 2-author roster populated; regraded GREY→COMPLETE.',
    verified_by_tool = 'crossref-api-resolve+grey-regrade-pass2',
    last_verified_at = '2026-05-22T10:40:00Z',
    updated_at = '2026-05-22T10:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00242';

COMMIT;
