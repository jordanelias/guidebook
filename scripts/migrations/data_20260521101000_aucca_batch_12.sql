-- data_20260521101000_aucca_batch_12.sql
--
-- AU + CA cross-jurisdiction batch 12: 4 rows web-search verified.
--
-- REF-00271: Livable Housing Design Guidelines, 4th Edition (LHA 2017) — full guidelines
-- REF-00471: LHA 4th ed cited for doors specifically — flagged as dup-of REF-00271
-- REF-00141: CMHC Universal Design Guide for New Multi-Unit Residential Buildings (2023)
-- REF-00288: Rick Hansen Foundation Accessibility Certification v4.0 (2024)

BEGIN TRANSACTION;

-- REF-00271: LHA Livable Housing Design Guidelines 4th ed
UPDATE evidence_sources SET
    pub_title = 'Livable Housing Design Guidelines, Fourth Edition',
    pub_year = 2017,
    first_author_last = 'Livable Housing Australia',
    is_corporate_primary = 1,
    author_display = 'Livable Housing Australia (LHA) — partnership between community/consumer groups, government, and industry',
    publisher = 'Livable Housing Australia, Sydney',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'au-ca-batch-12 2026-05-21T10:10:00Z: web-search verified via livablehousingaustralia.org.au + universaldesignaustralia.net.au + accessaustralia.com.au + yourhome.gov.au. 4th edition published 2017 (updates: June 2017). Defines 15 livable design elements with Silver/Gold/Platinum performance levels. Arose from the Kirribilli Dialogue on Universal Housing Design. Silver level was adopted as the basis for the ABCB Standard for Livable Housing Design 2022, referenced in National Construction Code 2022 (NCC Vol 1 Part G7 for Class 2; Vol 2 Part H8 for Class 1a). As of 1 July 2025, Access Institute took over LHA Assessor registration.',
    url = 'https://livablehousingaustralia.org.au/wp-content/uploads/2021/02/SLLHA_GuidelinesJuly2017FINAL4.pdf',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+lha-official',
    last_verified_at = '2026-05-21T10:10:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T10:10:00Z au-ca-batch-12] web-search verified',
    updated_at = '2026-05-21T10:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00271';

-- REF-00471: LHA cited for doors — dup-of REF-00271
UPDATE evidence_sources SET
    pub_title = 'Livable Housing Design Guidelines, Fourth Edition — doors',
    pub_year = 2017,
    first_author_last = 'Livable Housing Australia',
    is_corporate_primary = 1,
    author_display = 'Livable Housing Australia (LHA)',
    publisher = 'Livable Housing Australia, Sydney',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00271',
    metadata_integrity_detail = 'au-ca-batch-12 2026-05-21T10:10:00Z: web-search verified. Cites the LHA Livable Housing Design Guidelines 4th ed (2017) for the door-element provisions specifically. Stored year 2022 corrected to 2017 (canonical publication year). Owner: this may be redundant with REF-00271 which cites whole guidelines — consider consolidating, or keep separate if the BPC context calls out doors specifically.',
    url = 'https://livablehousingaustralia.org.au/wp-content/uploads/2021/02/SLLHA_GuidelinesJuly2017FINAL4.pdf',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+lha-official',
    last_verified_at = '2026-05-21T10:10:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T10:10:00Z au-ca-batch-12] web-search verified; flagged as potential duplicate of REF-00271',
    updated_at = '2026-05-21T10:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00471';

-- REF-00141: CMHC Universal Design Guide
UPDATE evidence_sources SET
    pub_title = 'Universal Design Guide for New Multi-Unit Residential Buildings',
    pub_year = 2023,
    first_author_last = 'Canada Mortgage and Housing Corporation',
    is_corporate_primary = 1,
    author_display = 'Canada Mortgage and Housing Corporation (CMHC) / Société canadienne d''hypothèques et de logement (SCHL)',
    publisher = 'Canada Mortgage and Housing Corporation (CMHC)',
    jurisdiction = 'CA',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'au-ca-batch-12 2026-05-21T10:10:00Z: web-search verified via cmhc-schl.gc.ca + universaldesign.ca + CHRC Commission references. CMHC''s practical non-technical introduction to Universal Design for multi-unit residential building designers, builders and developers. Supports CMHC''s 2026-2028 Accessibility Plan and the federal Housing Design Catalogue. Companion to CSA/ASC B652-23 Accessible dwellings standard (2023) and CAN/ASC-2.8:2025 Accessible-Ready Housing standard.',
    url = 'https://www.cmhc-schl.gc.ca/professionals/industry-innovation-and-leadership/industry-expertise/accessible-adaptable-housing/universal-design-new-multi-unit-residential-buildings/universal-design-guide',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+cmhc-official',
    last_verified_at = '2026-05-21T10:10:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T10:10:00Z au-ca-batch-12] web-search verified',
    updated_at = '2026-05-21T10:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00141';

-- REF-00288: Rick Hansen Foundation Accessibility Certification v4.0
UPDATE evidence_sources SET
    pub_title = 'Rick Hansen Foundation Accessibility Certification (RHFAC) — Rating Survey v4.0 and Guide to RHF Accessibility Certification v4.2',
    pub_year = 2024,
    first_author_last = 'Rick Hansen Foundation',
    is_corporate_primary = 1,
    author_display = 'Rick Hansen Foundation (RHF)',
    publisher = 'Rick Hansen Foundation, Richmond, BC',
    jurisdiction = 'CA',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'au-ca-batch-12 2026-05-21T10:10:00Z: web-search verified via rickhansen.com + CSA Group. RHFAC v4.0 effective 15 January 2024; v3.0 remained available until 30 June 2024. Guide to RHFAC v4.2 June 2024. Voluntary rating system measuring meaningful access across mobility, vision, hearing and neurological experiences. Two-tier recognition: RHF Accessibility Certified / RHF Accessibility Certified Gold. Founded by Canadian Paralympian Rick Hansen.',
    url = 'https://www.rickhansen.com/become-accessible/rating-certification/rhfac-v40',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+rhf-official',
    last_verified_at = '2026-05-21T10:10:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T10:10:00Z au-ca-batch-12] web-search verified',
    updated_at = '2026-05-21T10:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00288';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
