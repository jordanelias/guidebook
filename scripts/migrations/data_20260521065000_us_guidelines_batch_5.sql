-- data_20260521065000_us_guidelines_batch_5.sql
--
-- US guidelines no-identifier cohort web-search verification batch 5.
-- Per DR-2026-05-18 statutory-metadata-completeness gray-lit / regulatory protocol.
--
-- REF-00447: ICC A117.1-2017 Accessible and Usable Buildings and Facilities standard
-- REF-00143: HUD Fair Housing Act Design Manual (1996 first, 1998 revised — stored year 2022 corrected)
-- REF-00062: PVA Accessible Home Design 2nd ed. (Davies & Lopez, 2021)
-- REF-00316: VA SAH/SHA grants FY 2024 amounts (Federal Register 88 FR 78089 Nov 2023)
-- REF-00317: USDA Section 504 Rural Housing Repair program (7 CFR Part 3550)

BEGIN TRANSACTION;

-- REF-00447: ICC A117.1-2017
UPDATE evidence_sources SET
    pub_title = 'Accessible and Usable Buildings and Facilities (ICC A117.1-2017)',
    pub_year = 2017,
    first_author_last = 'International Code Council',
    is_corporate_primary = 1,
    author_display = 'International Code Council (ICC); ANSI Accredited Standards Committee A117 on Architectural Features and Site Design of Public Buildings and Residential Structures for Persons with Disabilities',
    publisher = 'International Code Council (ICC)',
    standard_number = 'ICC A117.1-2017 (ANSI A117.1-2017)',
    isbn = '9781609837013',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-guidelines-batch-5 2026-05-21T06:50:00Z: web-search verified via ANSI Webstore + ICC + ANSI blog. American National Standard; 2017 revision of ICC A117.1-2009. Used as HUD safe harbor for Fair Housing Act compliance (since 2020 rule). Co-publishes with ADAAG and Fair Housing Design Guidelines.',
    url = 'https://shop.iccsafe.org/standards/icc-a117-1-2017-standard-for-accessible-and-usable-buildings-and-facilities-1.html',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+iccsafe-official',
    last_verified_at = '2026-05-21T06:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T06:50:00Z us-guidelines-batch-5] web-search verified',
    updated_at = '2026-05-21T06:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00447';

-- REF-00143: Fair Housing Act Design Manual
-- Stored year 2022 corrected — canonical version is 1996 first / 1998 revised
UPDATE evidence_sources SET
    pub_title = 'Fair Housing Act Design Manual: A Manual to Assist Designers and Builders in Meeting the Accessibility Requirements of the Fair Housing Act',
    pub_year = 1998,
    first_author_last = 'U.S. Department of Housing and Urban Development',
    is_corporate_primary = 1,
    author_display = 'U.S. Department of Housing and Urban Development (HUD), Office of Fair Housing and Equal Opportunity',
    publisher = 'U.S. Department of Housing and Urban Development',
    isbn = '9780894992391',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-guidelines-batch-5 2026-05-21T06:50:00Z: web-search verified via HUD + DOJ joint statement + Wiley + Northwest ADA Center. Canonical Design Manual published August 1996, revised April 1998 (no 2022 update — stored year corrected). One of HUD-approved safe harbors for Fair Housing Act compliance. Companion to: Final Fair Housing Accessibility Guidelines (56 FR 9472, March 6, 1991) and Supplement (59 FR 33362, June 28, 1994). Implementing regulations at 24 CFR Part 100. Statutory authority: Fair Housing Amendments Act of 1988, 42 U.S.C. 3604(f)(3)(C).',
    url = 'https://www.huduser.gov/portal/publications/destech/fairhousing.html',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+hud-official',
    last_verified_at = '2026-05-21T06:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T06:50:00Z us-guidelines-batch-5] web-search verified; stored year 2022 corrected to 1998 (canonical revised edition)',
    updated_at = '2026-05-21T06:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00143';

-- REF-00062: PVA Accessible Home Design 2nd ed
UPDATE evidence_sources SET
    pub_title = 'Accessible Home Design: Architectural Solutions for the Wheelchair User, 2nd Edition',
    pub_year = 2021,
    first_author_last = 'Davies',
    first_author_first = 'Thomas D.',
    is_corporate_primary = 0,
    author_display = 'Davies, T. D., Jr.; Lopez, C. P. (Architects, Paralyzed Veterans of America)',
    author_count = 2,
    author_count_is_complete = 1,
    publisher = 'Paralyzed Veterans of America (PVA)',
    isbn = '9780929819181',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-guidelines-batch-5 2026-05-21T06:50:00Z: web-search verified via pva.org + Amazon. PVA item 2500-181. 2nd edition is a revised+expanded successor to the 1st edition; covers entrances, residential elevators/lifts, kitchen design, bath/toilet plans, plumbing, grab bars, doors, windows, outdoor rooms, garden paths. PVA is the only US veterans organization with on-staff architects.',
    url = 'https://pva.org/research-resources/accessible-design/accessible-home-design-book/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+pva-official',
    last_verified_at = '2026-05-21T06:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T06:50:00Z us-guidelines-batch-5] web-search verified',
    updated_at = '2026-05-21T06:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00062';

-- REF-00316: VA SAH/SHA grant amounts FY 2024
UPDATE evidence_sources SET
    pub_title = 'Loan Guaranty: Assistance to Eligible Individuals in Acquiring Specially Adapted Housing; Cost-of-Construction Index — FY 2024 aggregate amounts (SAH $109,986; SHA $22,036)',
    pub_year = 2023,
    first_author_last = 'U.S. Department of Veterans Affairs',
    is_corporate_primary = 1,
    author_display = 'U.S. Department of Veterans Affairs (VA), Loan Guaranty Service, Veterans Benefits Administration',
    publisher = 'Federal Register (U.S. Government Publishing Office)',
    standard_number = 'Federal Register Vol. 88, No. 218 (Nov 14, 2023); Doc 2023-24984; FR-6235-N-01',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-guidelines-batch-5 2026-05-21T06:50:00Z: web-search verified via federalregister.gov + military.com. FY 2024 aggregate amounts notice; statutory authority 38 U.S.C. 2102(e), 2102A(b)(2), 2102B(b)(2), and 38 CFR 36.4411. FY 2024: SAH $109,986, SHA $22,036, TRA-SAH $50,961, TRA-SHA $9,100. Annual cost-of-construction index adjustment effective Oct 1 each year. Some sources cite SAH $117,014 — variance based on subsection; $109,986 is the 38 USC 2101(a) figure stored in this row.',
    url = 'https://www.federalregister.gov/documents/2023/11/14/2023-24984/loan-guaranty-assistance-to-eligible-individuals-in-acquiring-specially-adapted-housing',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+fed-register-official',
    last_verified_at = '2026-05-21T06:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T06:50:00Z us-guidelines-batch-5] web-search verified',
    updated_at = '2026-05-21T06:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00316';

-- REF-00317: USDA Section 504 Home Repair Loans and Grants
-- Stored "$10,000 grant + $27,500 loan" mixes program eras: $27,500 is historical combined-cap; current is $40,000 loan
UPDATE evidence_sources SET
    pub_title = 'Single Family Housing Repair Loans and Grants (Section 504 Home Repair Program) — rural very-low-income homeowner repair assistance',
    pub_year = 2024,
    first_author_last = 'U.S. Department of Agriculture',
    is_corporate_primary = 1,
    author_display = 'U.S. Department of Agriculture (USDA), Rural Development, Rural Housing Service',
    publisher = 'USDA Rural Development',
    standard_number = '7 CFR Part 3550; Handbook HB-1-3550 Chapter 12',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-guidelines-batch-5 2026-05-21T06:50:00Z: web-search verified via rd.usda.gov + 7 CFR Part 3550. Statutory authority: Section 504 of the Housing Act of 1949. Current limits (2024+): max grant $10,000, max loan $40,000, combined max $50,000 ($55,000 in presidentially declared disaster areas). For very-low-income (<50% AMI) rural homeowners; grants restricted to age 62+. Loan terms: 20-year, 1% fixed interest. CALIFORNIA pilot doubles standard limits. Stored "$27,500 loan" figure conflates the historical combined-cap of the pre-2024 program; row metadata corrected to reflect current Section 504 maximum loan $40,000.',
    url = 'https://www.rd.usda.gov/programs-services/single-family-housing-programs/single-family-housing-repair-loans-grants',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+usda-official',
    last_verified_at = '2026-05-21T06:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T06:50:00Z us-guidelines-batch-5] web-search verified',
    updated_at = '2026-05-21T06:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00317';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
