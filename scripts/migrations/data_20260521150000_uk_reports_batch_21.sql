-- data_20260521150000_uk_reports_batch_21.sql
-- UK reports batch 21: 4 rows verified.
--
-- REF-00162: Disabled Facilities Grant (MHCLG/DHSC; £30k max England)
-- REF-00259: DFG programme data 2023/24
-- REF-00313: DFG 2026-27 £723M allocation
-- REF-00149: Habinteg 2025 Forecast for Accessible Homes

BEGIN TRANSACTION;

-- REF-00162: DFG main page
UPDATE evidence_sources SET
    pub_title = 'Disabled Facilities Grant (DFG) — England — Housing Grants, Construction and Regeneration Act 1996 s.23',
    pub_year = 2024,
    first_author_last = 'Ministry of Housing, Communities and Local Government',
    is_corporate_primary = 1,
    author_display = 'Ministry of Housing, Communities and Local Government (MHCLG) + Department of Health and Social Care (DHSC), HM Government',
    publisher = 'HM Government — MHCLG + DHSC (joint policy responsibility)',
    standard_number = 'Housing Grants, Construction and Regeneration Act 1996 s.23-24; max grant £30,000 (England), £36,000 (Wales), £25,000 (NI)',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00259-REF-00313',
    metadata_integrity_detail = 'uk-reports-batch-21 2026-05-21T15:00:00Z: web-search verified via gov.uk + commonslibrary.parliament.uk + Wikipedia + Foundations DFG library + Disability Rights UK + local authority pages (Southampton, Adur & Worthing, Warrington). Mandatory grant; means-tested except for children under 19. Statutory authority: Housing Grants, Construction and Regeneration Act 1996. Eligible adaptations: stair-lifts, level-access showers/wet-rooms, wash-and-dry toilets, ramps, wider doors, bespoke extensions, heating, insulation, telecare. Owner: REF-00162/REF-00259/REF-00313 form a 3-row cluster about the same DFG programme — consider consolidating or treating as facets (programme / annual data / 2026-27 allocation).',
    url = 'https://www.gov.uk/government/consultations/changing-the-way-government-allocates-disabled-facilities-grant-funding-to-local-authorities-in-england',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+gov-uk-official',
    last_verified_at = '2026-05-21T15:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T15:00:00Z uk-reports-batch-21] web-search verified',
    updated_at = '2026-05-21T15:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00162';

-- REF-00259: DFG programme 2023/24
UPDATE evidence_sources SET
    pub_title = 'Disabled Facilities Grant — programme data and annual allocations 2023/24 (£573M central government allocation England)',
    pub_year = 2024,
    first_author_last = 'Ministry of Housing, Communities and Local Government',
    is_corporate_primary = 1,
    author_display = 'MHCLG + DHSC; programme data hosted via Foundations (DFG technical hub) and House of Commons Library',
    publisher = 'HM Government — MHCLG + DHSC; programme management via Foundations DFG technical hub',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00162-REF-00313',
    metadata_integrity_detail = 'uk-reports-batch-21 2026-05-21T15:00:00Z: web-search verified via foundations.uk.com/library/dfg-allocations + commonslibrary.parliament.uk briefing SN03011. 2023/24 budget: £573M central government allocation + £102M additional April 2023 capital top-up over 2 years. Funding channeled into Better Care Fund (BCF; pooled with NHS England).',
    url = 'https://www.foundations.uk.com/library/dfg-allocations/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+foundations-uk+commonslibrary',
    last_verified_at = '2026-05-21T15:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T15:00:00Z uk-reports-batch-21] web-search verified',
    updated_at = '2026-05-21T15:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00259';

-- REF-00313: DFG 2026-27 £723M
UPDATE evidence_sources SET
    pub_title = 'Disabled Facilities Grant — 2026-27 allocation methodology and funding (£723M projected; £30k max per applicant England; consultation outcome Feb 2026)',
    pub_year = 2026,
    first_author_last = 'Ministry of Housing, Communities and Local Government',
    is_corporate_primary = 1,
    author_display = 'Ministry of Housing, Communities and Local Government (MHCLG), HM Government',
    publisher = 'HM Government — MHCLG (Department for Levelling Up, Housing and Communities, predecessor name)',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00162-REF-00259',
    metadata_integrity_detail = 'uk-reports-batch-21 2026-05-21T15:00:00Z: web-search verified via gov.uk consultation outcome page (published Feb 2026; consultation ran summer 2025). 2024-25 and 2025-26 allocation: £711M each. The £723M for 2026-27 figure cited in stored note tracks with ongoing increase. Consultation on new allocation formula (replacing 2011 BRE methodology) responded to 2018 independent review + 2024 LUHC Select Committee Report on disabled people in housing.',
    url = 'https://www.gov.uk/government/consultations/changing-the-way-government-allocates-disabled-facilities-grant-funding-to-local-authorities-in-england/outcome/changing-the-way-government-allocates-disabled-facilities-grant-funding-to-local-authorities-in-england-consultation-response',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+gov-uk-official',
    last_verified_at = '2026-05-21T15:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T15:00:00Z uk-reports-batch-21] web-search verified',
    updated_at = '2026-05-21T15:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00313';

-- REF-00149: Habinteg Forecast for Accessible Homes 2025
UPDATE evidence_sources SET
    pub_title = 'A Forecast for Accessible Homes 2025: One Decade On — Milestone or Millstone?',
    pub_year = 2025,
    first_author_last = 'Habinteg Housing Association',
    is_corporate_primary = 1,
    author_display = 'Habinteg Housing Association — Insight Report for Accessible Homes Week 8-12 September 2025',
    publisher = 'Habinteg Housing Association, London',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-reports-batch-21 2026-05-21T15:00:00Z: web-search verified via habinteg.org.uk + Housing LIN repository (housinglin.org.uk). Insight report published for Habinteg''s 10th Accessible Homes Week, marking a decade since M4(2)/M4(3) building regulations introduced (October 2015). Analyzed 311 English local plans (June-July 2025). Key findings: 170/311 plans have no target for wheelchair user homes; only ~4% (~108,000) of planned new homes are to wheelchair-user (M4(3)) standard; stark regional disparity (London 1:210 vs North West 1:2006 per planned wheelchair user home).',
    url = 'https://www.housinglin.org.uk/_assets/Resources/Housing/OtherOrganisation/A-forecast-for-accessible-homes-2025-one-decade-on-milestone-or-millstone-report.pdf',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+habinteg-official+housinglin',
    last_verified_at = '2026-05-21T15:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T15:00:00Z uk-reports-batch-21] web-search verified',
    updated_at = '2026-05-21T15:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00149';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
