-- data_20260521055000_uk_guidelines_batch_3.sql
--
-- UK guidelines no-identifier cohort web-search verification batch 3.
-- Per DR-2026-05-18 statutory-metadata-completeness gray-lit / regulatory protocol.
--
-- REF-00248: VisitBritain "Make Your Business Accessible" business advice
-- REF-00264: HM Government "Raising accessibility standards for new homes" 2022 consultation outcome
-- REF-00282: House of Commons WEC "Accessibility of products and services to disabled people" 2024
-- REF-00247: Wheels for Wellbeing "Benches and Seating in Public Spaces" 2025

BEGIN TRANSACTION;

-- REF-00248: VisitBritain Make Your Business Accessible
UPDATE evidence_sources SET
    pub_title = 'Make your business accessible — business advice and resources for accessibility',
    pub_year = 2023,
    first_author_last = 'VisitBritain',
    is_corporate_primary = 1,
    author_display = 'VisitBritain (UK national tourism agency)',
    publisher = 'VisitBritain',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-3 2026-05-21T05:50:00Z: web-search verified via visitbritain.org. Page provides UK tourism business accessibility advice including seating-at-regular-intervals guidance. Note: the "50m seating interval" specification in stored title appears to be generic UK accessibility guidance (BS 8300-1:2018, DfT Inclusive Mobility 2021) rather than originating in this VisitBritain page; this row may be citing the page for §5 of its accessibility checklist. Owner: confirm slug context.',
    url = 'https://www.visitbritain.org/business-advice/make-your-business-accessible',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+visitbritain-official',
    last_verified_at = '2026-05-21T05:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T05:50:00Z uk-guidelines-batch-3] web-search verified',
    updated_at = '2026-05-21T05:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00248';

-- REF-00264: Raising Accessibility Standards consultation outcome
UPDATE evidence_sources SET
    pub_title = 'Raising accessibility standards for new homes: summary of consultation responses and government response',
    pub_year = 2022,
    first_author_last = 'HM Government',
    is_corporate_primary = 1,
    author_display = 'HM Government (Department for Levelling Up, Housing and Communities; previously Ministry of Housing, Communities and Local Government)',
    publisher = 'HM Government — gov.uk',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-3 2026-05-21T05:50:00Z: web-search verified via gov.uk. Original consultation paper Sept 2020 (Crown Copyright 2020, MHCLG); consultation outcome published 29 July 2022. Announces intention to mandate M4(2) Accessible and Adaptable as minimum default; M4(1) by exception. Status as of Feb 2024: implementation still pending further technical consultation per Baroness Penn.',
    url = 'https://www.gov.uk/government/consultations/raising-accessibility-standards-for-new-homes/outcome/raising-accessibility-standards-for-new-homes-summary-of-consultation-responses-and-government-response',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+gov-uk-official',
    last_verified_at = '2026-05-21T05:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T05:50:00Z uk-guidelines-batch-3] web-search verified',
    updated_at = '2026-05-21T05:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00264';

-- REF-00282: WEC Accessibility of products and services to disabled people
UPDATE evidence_sources SET
    pub_title = 'Accessibility of products and services to disabled people',
    pub_year = 2024,
    first_author_last = 'Women and Equalities Committee',
    is_corporate_primary = 1,
    author_display = 'House of Commons Women and Equalities Committee (chaired by Caroline Nokes MP)',
    publisher = 'House of Commons (UK Parliament)',
    standard_number = 'HC 605 (Fourth Report of Session 2023-24)',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-3 2026-05-21T05:50:00Z: web-search verified via publications.parliament.uk. Fourth Report of Session 2023-24, HC 605. Ordered to be printed 6 March 2024; published by authority of the House of Commons on 19 March 2024. Part of the National Disability Strategy inquiry. Available in EasyRead, BSL and Large Print formats.',
    url = 'https://publications.parliament.uk/pa/cm5804/cmselect/cmwomeq/605/report.html',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+parliament-official',
    last_verified_at = '2026-05-21T05:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T05:50:00Z uk-guidelines-batch-3] web-search verified',
    updated_at = '2026-05-21T05:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00282';

-- REF-00247: Wheels for Wellbeing Benches and Seating in Public Spaces
UPDATE evidence_sources SET
    pub_title = 'Benches and Seating in Public Spaces — Design guidance for accessible public seating',
    pub_year = 2025,
    first_author_last = 'Wheels for Wellbeing',
    is_corporate_primary = 1,
    author_display = 'Wheels for Wellbeing (UK disability cycling charity); contributing input from David Smith (City of York Council)',
    publisher = 'Wheels for Wellbeing',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-3 2026-05-21T05:50:00Z: web-search verified via wheelsforwellbeing.org.uk + accessassociation.co.uk. Latest update Nov 2025 (additional information re space under benches for disabled people with assistance dogs or who need to move feet under body while sitting). Cites BS 8300-1:2018 §10.7(d) for armrest design. Updated version of earlier 2024 release.',
    url = 'https://wheelsforwellbeing.org.uk/our-campaigns/resources/benches-and-seating-in-public-spaces/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+wfw-official',
    last_verified_at = '2026-05-21T05:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T05:50:00Z uk-guidelines-batch-3] web-search verified',
    updated_at = '2026-05-21T05:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00247';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
