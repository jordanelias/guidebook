-- data_20260521120000_us_reports_batch_15.sql
--
-- US reports batch 15: 7 rows verified incl. 4-way duplicate cluster.
--
-- REF-00161: VA SAH/SHA FY 2026 (FedReg doc 2025-20047)
-- REF-00338: Bauman 2010 DeafSpace Design Guidelines — dup-of REF-00339
-- REF-00231/REF-00234/REF-00245/REF-00223: Bateman et al. 2021 ME/CFS Essentials —
--   4-way duplicate cluster, all citing same Mayo Clin Proc paper DOI 10.1016/j.mayocp.2021.07.004
-- REF-00042: Clark 2021 "Against Access" McSweeney's Quarterly Concern 64

BEGIN TRANSACTION;

-- REF-00161: VA SAH/SHA FY 2026
UPDATE evidence_sources SET
    pub_title = 'Loan Guaranty: Assistance to Eligible Individuals in Acquiring Specially Adapted Housing; Cost-of-Construction Index for Fiscal Year 2026 (SAH $126,526; SHA $25,350; TRA-SAH $50,961; TRA-SHA $9,100)',
    pub_year = 2025,
    first_author_last = 'U.S. Department of Veterans Affairs',
    is_corporate_primary = 1,
    author_display = 'U.S. Department of Veterans Affairs (VA), Loan Guaranty Service, Veterans Benefits Administration',
    publisher = 'Federal Register (U.S. Government Publishing Office)',
    standard_number = 'Federal Register Vol. 90, Doc 2025-20047 (Nov 18, 2025); 38 U.S.C. 2102(e); 38 CFR 36.4411',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-reports-batch-15 2026-05-21T12:00:00Z: web-search verified via federalregister.gov + justia + military.net. Published 18 Nov 2025; effective 1 Oct 2025. 3.87% increase per Turner Building Cost Index Q2 2025 vs Q2 2024. Authority: 38 U.S.C. 2102(e), 2102A(b)(2), 2102B(b)(2); 38 CFR 36.4411. Contact: Jason Latona, Assistant Director for Specially Adapted Housing Policy and Native American Direct Loans, Loan Guaranty Service, Veterans Benefits Administration. Sister-row to REF-00316 (FY 2024 amounts).',
    url = 'https://www.federalregister.gov/documents/2025/11/18/2025-20047/loan-guaranty-assistance-to-eligible-individuals-in-acquiring-specially-adapted-housing',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+fed-register-official',
    last_verified_at = '2026-05-21T12:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T12:00:00Z us-reports-batch-15] web-search verified',
    updated_at = '2026-05-21T12:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00161';

-- REF-00338: Bauman 2010 DeafSpace Design Guidelines (dup-of REF-00339)
UPDATE evidence_sources SET
    pub_title = 'DeafSpace Design Guidelines (working draft, 85pp)',
    pub_year = 2010,
    first_author_last = 'Bauman',
    first_author_first = 'Hansel',
    is_corporate_primary = 0,
    author_display = 'Bauman, H. (architect, hbhm; Director of Campus Planning and Design, Gallaudet); with Bahan B., Bauman H.D., Sirvage R. (ASL/Deaf Studies, Gallaudet); Mitnick H. (color/material); Dangermond S., Keane C. (Dangermond Keane Architecture); Dunlop B. (lighting)',
    publisher = 'Gallaudet University, Washington DC — DeafSpace Project',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00339',
    metadata_integrity_detail = 'us-reports-batch-15 2026-05-21T12:00:00Z: web-search verified via Scribd + RIT InfoGuides + SMU LibGuides + Wikipedia + StudioTwentySeven Architecture + Institute for Human Centered Design + Pinelands Alliance hosting. DeafSpace Project ran 2005-2010 at Gallaudet. The "DeafSpace Design Guidelines" 85-page document is cited as unpublished working draft (REF-00338 framing) but is also the published Volume 1 (REF-00339 framing) — same artifact. Five touch points: Space and Proximity, Sensory Reach, Mobility and Proximity, Light and Color, Acoustics and EMI. >150 design principles. Owner: consolidate REF-00338 + REF-00339.',
    url = 'https://humancentereddesign.org/inclusive-design/library/gallaudet-university-deafspace-design-guidelines',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+gallaudet-ihcd',
    last_verified_at = '2026-05-21T12:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T12:00:00Z us-reports-batch-15] web-search verified; flagged as potential duplicate of REF-00339',
    updated_at = '2026-05-21T12:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00338';

-- ME/CFS cluster: REF-00231/00234/00245/00223 all cite same Bateman 2021 paper
-- REF-00223
UPDATE evidence_sources SET
    doi = '10.1016/j.mayocp.2021.07.004',
    pub_title = 'Myalgic Encephalomyelitis/Chronic Fatigue Syndrome: Essentials of Diagnosis and Management',
    pub_year = 2021,
    first_author_last = 'Bateman',
    first_author_first = 'Lucinda',
    is_corporate_primary = 0,
    author_display = 'Bateman, L.; Bested, A. C.; Bonilla, H. F.; Chheda, B. V.; Chu, L.; Curtin, J. M.; Dempsey, T.; Dimmock, M. E.; Dowell, T. G.; Felsenstein, D.; Kaufman, D. L.; Klimas, N. G.; Komaroff, A. L.; Lapp, C. W.; Levine, S. M.; Montoya, J. G.; Natelson, B. H.; Peterson, D. L.; Podell, R. N.; Ruhoy, I. S.; Vera-Nunez, M. A.; Yellman, B. P. (on behalf of the U.S. ME/CFS Clinician Coalition)',
    author_count = 23,
    author_count_is_complete = 1,
    journal_name = 'Mayo Clinic Proceedings',
    volume = '96',
    issue = '11',
    pages_start = '2861',
    pages_end = '2878',
    publisher = 'Elsevier / Mayo Foundation for Medical Education and Research',
    issn = '0025-6196',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00234-REF-00245-REF-00231',
    metadata_integrity_detail = 'us-reports-batch-15 2026-05-21T12:00:00Z: web-search + Crossref verified. DOI 10.1016/j.mayocp.2021.07.004. Open Access CC BY-NC-ND 4.0. Published online 25 Aug 2021, print Nov 2021. Lead by 23-member U.S. ME/CFS Clinician Coalition (formed 2018); chaired by Bateman of Bateman Horne Center. The cool/low-sensory-environment requirement stored in REF-00223 corresponds to the recommendations in Table 4 of this paper. Stored year 2024 corrected to 2021. Owner: 4-way duplicate cluster (REF-00231/00234/00245/00223) — consolidate.',
    url = 'https://doi.org/10.1016/j.mayocp.2021.07.004',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref-confirm',
    last_verified_at = '2026-05-21T12:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T12:00:00Z us-reports-batch-15] DOI + cluster verified',
    updated_at = '2026-05-21T12:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00223';

-- REF-00234
UPDATE evidence_sources SET
    doi = '10.1016/j.mayocp.2021.07.004',
    pub_title = 'Myalgic Encephalomyelitis/Chronic Fatigue Syndrome: Essentials of Diagnosis and Management',
    pub_year = 2021,
    first_author_last = 'Bateman',
    first_author_first = 'Lucinda',
    is_corporate_primary = 0,
    author_display = 'Bateman, L. et al. (23 authors of the U.S. ME/CFS Clinician Coalition)',
    author_count = 23,
    author_count_is_complete = 1,
    journal_name = 'Mayo Clinic Proceedings',
    volume = '96',
    issue = '11',
    pages_start = '2861',
    pages_end = '2878',
    publisher = 'Elsevier / Mayo Foundation for Medical Education and Research',
    issn = '0025-6196',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00223-REF-00245-REF-00231',
    metadata_integrity_detail = 'us-reports-batch-15 2026-05-21T12:00:00Z: web-search + Crossref verified. Same paper as REF-00223/REF-00245/REF-00231. Stored year 2024 corrected to 2021.',
    url = 'https://doi.org/10.1016/j.mayocp.2021.07.004',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref-confirm',
    last_verified_at = '2026-05-21T12:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T12:00:00Z us-reports-batch-15] DOI + cluster verified',
    updated_at = '2026-05-21T12:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00234';

-- REF-00231
UPDATE evidence_sources SET
    doi = '10.1016/j.mayocp.2021.07.004',
    pub_title = 'Myalgic Encephalomyelitis/Chronic Fatigue Syndrome: Essentials of Diagnosis and Management',
    pub_year = 2021,
    first_author_last = 'Bateman',
    first_author_first = 'Lucinda',
    is_corporate_primary = 0,
    author_display = 'Bateman, L. et al. (23 authors of the U.S. ME/CFS Clinician Coalition)',
    author_count = 23,
    author_count_is_complete = 1,
    journal_name = 'Mayo Clinic Proceedings',
    volume = '96',
    issue = '11',
    pages_start = '2861',
    pages_end = '2878',
    publisher = 'Elsevier / Mayo Foundation for Medical Education and Research',
    issn = '0025-6196',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00223-REF-00234-REF-00245',
    metadata_integrity_detail = 'us-reports-batch-15 2026-05-21T12:00:00Z: web-search + Crossref verified. Same paper as REF-00223/REF-00234/REF-00245. Stored year 2025 corrected to 2021.',
    url = 'https://doi.org/10.1016/j.mayocp.2021.07.004',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref-confirm',
    last_verified_at = '2026-05-21T12:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T12:00:00Z us-reports-batch-15] DOI + cluster verified',
    updated_at = '2026-05-21T12:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00231';

-- REF-00245
UPDATE evidence_sources SET
    doi = '10.1016/j.mayocp.2021.07.004',
    pub_title = 'Myalgic Encephalomyelitis/Chronic Fatigue Syndrome: Essentials of Diagnosis and Management',
    pub_year = 2021,
    first_author_last = 'Bateman',
    first_author_first = 'Lucinda',
    is_corporate_primary = 0,
    author_display = 'Bateman, L. et al. (23 authors of the U.S. ME/CFS Clinician Coalition)',
    author_count = 23,
    author_count_is_complete = 1,
    journal_name = 'Mayo Clinic Proceedings',
    volume = '96',
    issue = '11',
    pages_start = '2861',
    pages_end = '2878',
    publisher = 'Elsevier / Mayo Foundation for Medical Education and Research',
    issn = '0025-6196',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00223-REF-00234-REF-00231',
    metadata_integrity_detail = 'us-reports-batch-15 2026-05-21T12:00:00Z: web-search + Crossref verified. Same paper as REF-00223/REF-00234/REF-00231. Stored year 2025 corrected to 2021.',
    url = 'https://doi.org/10.1016/j.mayocp.2021.07.004',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+crossref-confirm',
    last_verified_at = '2026-05-21T12:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T12:00:00Z us-reports-batch-15] DOI + cluster verified',
    updated_at = '2026-05-21T12:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00245';

-- REF-00042: Clark 2021 Against Access McSweeney's
UPDATE evidence_sources SET
    pub_title = 'Against Access',
    pub_year = 2021,
    first_author_last = 'Clark',
    first_author_first = 'John Lee',
    is_corporate_primary = 0,
    author_display = 'Clark, J. L. (DeafBlind poet/essayist; 2020-21 Disability Futures Fellow; National Magazine Award winner)',
    author_count = 1,
    author_count_is_complete = 1,
    journal_name = 'McSweeney''s Quarterly Concern',
    volume = '64',
    publisher = 'McSweeney''s, San Francisco',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-reports-batch-15 2026-05-21T12:00:00Z: web-search verified via johnleeclark.com + Univ. of Iowa Krause Essay Prize page + jimcromwellinterpreting.com + ddbeck.com + MetaFilter. Essay published in McSweeney''s Quarterly Concern Issue 64 (August 2021). Critique of accessibility framing from DeafBlind perspective; advocates for Protactile movement and Co-Navigation. Won the 2022 Krause Essay Prize (Univ. of Iowa Nonfiction Writing Program). McSweeney''s does not assign DOIs.',
    url = 'https://store.mcsweeneys.net/products/mcsweeneys-issue-64-mcsweeneys-quarterly-concern',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+mcsweeneys-author-confirm',
    last_verified_at = '2026-05-21T12:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T12:00:00Z us-reports-batch-15] web-search verified',
    updated_at = '2026-05-21T12:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00042';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
