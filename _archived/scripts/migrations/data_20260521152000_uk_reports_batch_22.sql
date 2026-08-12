-- data_20260521152000_uk_reports_batch_22.sql
-- UK reports batch 22: 2 rows verified.
--
-- REF-00734: Tibble (2005) DWP Working Paper 21 — Review of existing research on the extra costs of disability
-- REF-00268: Provan et al. (2023) LSE CASEreport 147 — The Social and Economic Value of Wheelchair User Homes

BEGIN TRANSACTION;

-- REF-00734: Tibble 2005
UPDATE evidence_sources SET
    pub_title = 'Review of existing research on the extra costs of disability',
    pub_year = 2005,
    first_author_last = 'Tibble',
    first_author_first = 'Matthew',
    is_corporate_primary = 0,
    author_display = 'Tibble, M.',
    author_count = 1,
    author_count_is_complete = 1,
    publisher = 'Department for Work and Pensions (DWP), London',
    standard_number = 'DWP Working Paper No. 21',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-reports-batch-22 2026-05-21T15:20:00Z: web-search verified via multiple secondary citations (IRISS, Wiley Health Economics Cullinan 2011, Cambridge Ageing & Society, MDPI Social Sciences, UN cost-of-disability report). Frequently cited as Tibble M. 2005. "Review of existing research on the extra costs of disability." DWP Working Paper No. 21, London. Foundational UK government working paper on disability cost research methodology.',
    url = 'https://webarchive.nationalarchives.gov.uk/ukgwa/+/http://www.dwp.gov.uk/asd/asd5/working_papers.asp',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dwp-uk',
    last_verified_at = '2026-05-21T15:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T15:20:00Z uk-reports-batch-22] web-search verified',
    updated_at = '2026-05-21T15:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00734';

-- REF-00268: Provan et al. LSE CASEreport 147
UPDATE evidence_sources SET
    pub_title = 'The Social and Economic Value of Wheelchair User Homes (technical report) / Living Not Existing: The Economic & Social Value of Wheelchair User Homes (Habinteg summary)',
    pub_year = 2023,
    first_author_last = 'Provan',
    first_author_first = 'James Albert',
    is_corporate_primary = 0,
    author_display = 'Provan, J. A.; Lane, L.; Horne Rowan, J. (LSE Housing and Communities / Centre for Analysis of Social Exclusion)',
    author_count = 3,
    author_count_is_complete = 1,
    publisher = 'London School of Economics — Centre for Analysis of Social Exclusion (CASE), CASEreport 147; commissioned by Habinteg Housing Association',
    standard_number = 'CASEreport 147; COI: 20.500.12592/m83dqr',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-reports-batch-22 2026-05-21T15:20:00Z: web-search verified via eprints.lse.ac.uk/121508 + sticerd.lse.ac.uk + habinteg.org.uk + Housing LIN + Parliament committee evidence + Policy Commons. Published 4 Sept 2023, Accessible Homes Week. Cost-benefit analysis: working-age wheelchair user benefit £94,000 / 10 years vs build cost £22,000 (4x ROI); later-life (65+) wheelchair user benefit £101,000 / 10 years vs £18,000 build cost (5.6x ROI). Local authority saving: ~£5,000/yr working-age, ~£9,000/yr later-life.',
    url = 'https://eprints.lse.ac.uk/121508/1/casereport147.pdf',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+lse-eprints',
    last_verified_at = '2026-05-21T15:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T15:20:00Z uk-reports-batch-22] web-search verified',
    updated_at = '2026-05-21T15:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00268';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
