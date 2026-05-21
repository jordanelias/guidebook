-- data_20260521122000_us_reports_batch_16.sql
-- US reports batch 16: 2 rows verified.
-- REF-00276: Accenture+Disability:IN+AAPD (2023) "The Disability Inclusion Imperative"
-- REF-00731: Szanton et al (2016) Health Affairs CAPABLE home-based care DOI 10.1377/hlthaff.2016.0140
--   (stored year 2019 corrected to 2016 — $2,825/participant figure)

BEGIN TRANSACTION;

-- REF-00276: Accenture Disability Inclusion Imperative
UPDATE evidence_sources SET
    pub_title = 'The Disability Inclusion Imperative — How leading companies are advancing disability inclusion at work',
    pub_year = 2023,
    first_author_last = 'Accenture',
    is_corporate_primary = 1,
    author_display = 'Accenture — in partnership with Disability:IN and the American Association of People with Disabilities (AAPD)',
    publisher = 'Accenture',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-reports-batch-16 2026-05-21T12:20:00Z: web-search verified via accenture.com newsroom + disabilityin.org + Annual Reviews Org Psych cited reference + Fortune cite + Together We Rock + financial wire. Published 27 Nov 2023. Follow-up to 2018 landmark Accenture/Disability:IN report on disability inclusion at work. Sample: 346 unique respondents to the Disability Equality Index (DEI) 2015-2022. Three measures: profitability (revenues + net income), productivity (revenue per employee), value creation (economic profit). Key finding: disability inclusion leaders generated 1.6x revenue, 2.6x net income, 2x economic profit, and 25% higher productivity vs. peers.',
    url = 'https://www.accenture.com/content/dam/accenture/final/accenture-com/document-2/Disability-Inclusion-Report-Business-Imperative.pdf',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+accenture-official',
    last_verified_at = '2026-05-21T12:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T12:20:00Z us-reports-batch-16] web-search verified',
    updated_at = '2026-05-21T12:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00276';

-- REF-00731: Szanton et al 2016 Health Affairs CAPABLE
-- Stored year 2019 corrected to 2016 (year of original Health Affairs publication of the $2,825 cost figure)
UPDATE evidence_sources SET
    doi = '10.1377/hlthaff.2016.0140',
    pub_title = 'Home-Based Care Program Reduces Disability And Promotes Aging In Place',
    pub_year = 2016,
    first_author_last = 'Szanton',
    first_author_first = 'Sarah L.',
    is_corporate_primary = 0,
    author_display = 'Szanton, S. L.; Leff, B.; Wolff, J. L.; Roberts, L.; Gitlin, L. N. (Johns Hopkins School of Nursing)',
    author_count = 5,
    author_count_is_complete = 1,
    journal_name = 'Health Affairs',
    volume = '35',
    issue = '9',
    pages_start = '1558',
    pages_end = '1563',
    publisher = 'Project HOPE — The People-to-People Health Foundation',
    issn = '0278-2715',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-reports-batch-16 2026-05-21T12:20:00Z: web-search + Crossref verified. Stored year 2019 corrected to 2016. The $2,825/participant home modification figure traces to this Szanton et al. 2016 Health Affairs paper on CAPABLE (Community Aging in Place, Advancing Better Living for Elders). Funded by CMS Innovation Center. Szanton subsequently received the 2019 Heinz Award for CAPABLE; the stored year 2019 may reflect that recognition rather than the publication.',
    url = 'https://doi.org/10.1377/hlthaff.2016.0140',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref-confirm',
    last_verified_at = '2026-05-21T12:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T12:20:00Z us-reports-batch-16] DOI confirmed; stored year 2019 -> 2016',
    updated_at = '2026-05-21T12:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00731';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
