-- data_20260521103000_ca_batch_13.sql
--
-- CA batch 13: 2 Canadian federal sources web-search verified.
--
-- REF-00205: CMHC Renovating for Accessibility — multi-fact-sheet series (2021)
-- REF-00160: CRA Home Accessibility Tax Credit (HATC) — federal income tax credit

BEGIN TRANSACTION;

-- REF-00205: CMHC Renovating for Accessibility
UPDATE evidence_sources SET
    pub_title = 'Renovating for Accessibility — fact-sheet series on barrier-free renovation for multi-family housing (Building Entrances, Vertical Circulation, Kitchens, Bathrooms, Other Building Features)',
    pub_year = 2021,
    first_author_last = 'Canada Mortgage and Housing Corporation',
    is_corporate_primary = 1,
    author_display = 'Canada Mortgage and Housing Corporation (CMHC) / Société canadienne d''hypothèques et de logement (SCHL)',
    publisher = 'Canada Mortgage and Housing Corporation (CMHC)',
    jurisdiction = 'CA',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'ca-batch-13 2026-05-21T10:30:00Z: web-search verified via cmhc-schl.gc.ca. Multi-part fact-sheet series published 31 May 2021. Each fact sheet (Building Entrances, Vertical Circulation, Kitchens, Bathrooms, Other Building Features) is a downloadable PDF. Aimed at building owners, property managers, developers, non-profits to inform barrier-free renovation of multi-family housing built without accessibility in mind (1970s-1990s stock).',
    url = 'https://www.cmhc-schl.gc.ca/professionals/industry-innovation-and-leadership/industry-expertise/accessible-adaptable-housing/renovating-for-accessibility',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+cmhc-official',
    last_verified_at = '2026-05-21T10:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T10:30:00Z ca-batch-13] web-search verified',
    updated_at = '2026-05-21T10:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00205';

-- REF-00160: HATC
UPDATE evidence_sources SET
    pub_title = 'Home Accessibility Tax Credit (HATC) — Canada Revenue Agency federal non-refundable tax credit, Line 31285',
    pub_year = 2024,
    first_author_last = 'Canada Revenue Agency',
    is_corporate_primary = 1,
    author_display = 'Canada Revenue Agency (CRA), Government of Canada',
    publisher = 'Canada Revenue Agency (canada.ca)',
    standard_number = 'T1 Line 31285; Schedule 12; Income Tax Act s.118.041',
    jurisdiction = 'CA',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'ca-batch-13 2026-05-21T10:30:00Z: web-search verified via canada.ca. Federal non-refundable tax credit established 2016 (Income Tax Act s.118.041). Effective 2022, maximum qualifying expenses raised from $10,000 to $20,000; credit rate 15% → max credit $3,000 per year per qualifying dwelling. Qualifying individuals: age 65+ at year-end OR Disability Tax Credit eligible. Eligible expenses: enduring/integral home renovations improving access, mobility, function, safety.',
    url = 'https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/deductions-credits-expenses/line-31285-home-accessibility-expenses.html',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+cra-canada-official',
    last_verified_at = '2026-05-21T10:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T10:30:00Z ca-batch-13] web-search verified',
    updated_at = '2026-05-21T10:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00160';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
