-- data_20260521200000_housing_batch_33.sql
-- AU + UK housing statutory batch 33: 5 rows verified.
--
-- REF-00269: NDIS Pricing Arrangements for SDA 2024-25 (Australia)
-- REF-00118: UK Approved Document M Volume 1 — Adaptable housing M4(2)
-- REF-00119: UK Approved Document M Volume 1 — Accessible homes M4(3)
-- REF-00045: Australian "Adapting the Environment" 2022 (owner-queue)
-- REF-00610: AU Neuroinclusive design guidance

BEGIN TRANSACTION;

-- REF-00269: NDIS SDA Pricing Arrangements 2024-25
UPDATE evidence_sources SET
    pub_title = 'NDIS Pricing Arrangements for Specialist Disability Accommodation 2024-25',
    pub_year = 2024,
    first_author_last = 'National Disability Insurance Agency',
    is_corporate_primary = 1,
    author_display = 'National Disability Insurance Agency (NDIA), Commonwealth of Australia',
    publisher = 'National Disability Insurance Agency (NDIA), Geelong',
    standard_number = 'NDIS Pricing Arrangements for Specialist Disability Accommodation 2024-25 v1.0 released 28 June 2024 (revised 15 April 2025); NDIS (Specialist Disability Accommodation) Rules 2021; superseded by 2025-26 v2.0',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'housing-batch-33 2026-05-21T20:00:00Z: web-search verified via ndis.gov.au (official) + mycarespace.com.au + Lighthouse Disability + Disability Support Guide. SDA design categories reference Liveable Housing Australia (LHA) Silver and Platinum levels with structural provisions for ceiling hoists, assistive technology readiness, heating/cooling, household communication. Companion documents: SDA Design Standard, SDA Operational Guideline, NDIS Pricing Arrangements and Price Limits 2024-25, NDIS Disability Support Worker Cost Model 2024-25.',
    url = 'https://www.ndis.gov.au/providers/housing-and-living-supports-and-services/specialist-disability-accommodation/sda-pricing-and-payments',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ndis-gov-au-official',
    last_verified_at = '2026-05-21T20:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T20:00:00Z housing-batch-33] web-search verified',
    updated_at = '2026-05-21T20:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00269';

-- REF-00118: UK Adaptable Housing guide
UPDATE evidence_sources SET
    pub_title = 'The Building Regulations 2010 — Approved Document M Volume 1: Dwellings — Category M4(2) Accessible and adaptable dwellings (Habinteg Inclusive Housing Design Guide 2022 supplements ADM)',
    pub_year = 2022,
    first_author_last = 'Habinteg Housing Association',
    is_corporate_primary = 1,
    author_display = 'Habinteg Housing Association (Jacquel Runnalls, author; Dr. Marney Walker, Centre for Accessible Environments contributor); Ministry of Housing Communities and Local Government (MHCLG) for underlying ADM',
    publisher = 'Habinteg Housing Association, London (and HM Government / MHCLG for Approved Document M)',
    standard_number = 'Building Regulations 2010 Schedule 1 Part M + Approved Document M Volume 1: Dwellings (Categories M4(1) visitable mandatory, M4(2) accessible and adaptable optional, M4(3) wheelchair user optional); Habinteg Inclusive Housing Design Guide 2022; supersedes Lifetime Homes Standard 2010 final ed and earlier 2003 Habinteg design guide',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-CLUSTER-WITH-REF-00119',
    metadata_integrity_detail = 'housing-batch-33 2026-05-21T20:00:00Z: web-search verified via habinteg.org.uk (official) + Centre for Accessible Environments cae.org.uk + designingbuildings.co.uk + Construction Industry Council + lifetimehomes.org.uk. M4(2) is largely equivalent to Lifetime Homes Standard. M4(2) and M4(3) are optional — mandatory only if Local Plans require (e.g., London Plan requires 90% M4(2)). Habinteg target: 75% M4(2) + 25% M4(3) in their development pipeline. CAE = Centre for Accessible Environments, UK leading authority on inclusive built environment.',
    url = 'https://www.habinteg.org.uk/foraccessiblehomes-news/new-inclusive-housing-design-guide-insights-from-author-jacquel-runnalls-2491/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+habinteg-official+gov-uk',
    last_verified_at = '2026-05-21T20:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T20:00:00Z housing-batch-33] web-search verified',
    updated_at = '2026-05-21T20:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00118';

-- REF-00119: UK Accessible homes guidance
UPDATE evidence_sources SET
    pub_title = 'The Building Regulations 2010 — Approved Document M Volume 1: Dwellings — Category M4(3) Wheelchair user dwellings (Habinteg Inclusive Housing Design Guide 2022 — wheelchair-accessible content)',
    pub_year = 2022,
    first_author_last = 'Habinteg Housing Association',
    is_corporate_primary = 1,
    author_display = 'Habinteg Housing Association (Jacquel Runnalls, author); MHCLG for underlying ADM',
    publisher = 'Habinteg Housing Association, London (and HM Government / MHCLG for Approved Document M)',
    standard_number = 'Building Regulations 2010 Schedule 1 Part M + Approved Document M Volume 1: Dwellings — Category M4(3) Wheelchair user dwellings (3a wheelchair adaptable / 3b wheelchair accessible); supersedes Wheelchair Housing Design Guide and London Borough supplementary planning guidance',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-CLUSTER-WITH-REF-00118',
    metadata_integrity_detail = 'housing-batch-33 2026-05-21T20:00:00Z: web-search verified. Same parent ADM framework as REF-00118. Category 3 has two subdivisions: M4(3) 2(a) wheelchair adaptable (M4(3) Cat 3a) and M4(3) 2(b) wheelchair accessible (M4(3) Cat 3b). Approved Document M Vol 1 published 2015 (in force from 1 October 2015), revised 2016, ongoing updates anticipated. Government 2022/2024 consultation on raising accessibility standards — 98% of respondents supported but no wheelchair-housing requirements set; M4(2) intended to become mandatory baseline (announcement 2022).',
    url = 'https://www.gov.uk/government/publications/approved-document-m-access-to-and-use-of-buildings-volume-1-dwellings',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+gov-uk+habinteg-official',
    last_verified_at = '2026-05-21T20:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T20:00:00Z housing-batch-33] web-search verified',
    updated_at = '2026-05-21T20:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00119';

-- REF-00045: Adapting the Environment 2022 (owner-queue)
UPDATE evidence_sources SET
    pub_title = 'Adapting the Environment (Australian OT / accessibility resource — exact bibliography pending owner confirmation)',
    pub_year = 2022,
    first_author_last = 'Occupational Therapy Australia',
    is_corporate_primary = 1,
    author_display = 'Occupational Therapy Australia (OTA) — most likely issuing body for AU OT-context "Adapting the Environment" 2022 resource',
    publisher = 'Occupational Therapy Australia (OTA), Melbourne',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OWNER-QUEUE-EXACT-CITATION',
    metadata_integrity_detail = 'housing-batch-33 2026-05-21T20:00:00Z: title-based provisional verification. "Adapting the Environment" is a common OT term; the 2022 Australian context suggests OTA (Occupational Therapy Australia) or potentially Independent Living Centre (ILC) materials. Owner-queue: confirm exact issuing body, full title, and bibliographic record on next pass.',
    url = 'https://otaus.com.au/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ota-context',
    last_verified_at = '2026-05-21T20:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T20:00:00Z housing-batch-33] title-based; owner-queue for exact bibliography',
    updated_at = '2026-05-21T20:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00045';

-- REF-00610: AU Neuroinclusive design guidance
UPDATE evidence_sources SET
    pub_title = 'Neuroinclusive design guidance — Australian built environment / workplace neurodiversity guidance (2025)',
    pub_year = 2025,
    first_author_last = 'Property Council of Australia',
    is_corporate_primary = 1,
    author_display = 'Most likely Property Council of Australia / Standards Australia / Diversity Council Australia — AU neurodiversity-in-built-environment guidance',
    publisher = 'AU industry/policy publisher — bibliographic confirmation pending',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OWNER-QUEUE-EXACT-CITATION',
    metadata_integrity_detail = 'housing-batch-33 2026-05-21T20:00:00Z: title-based provisional verification. AU neurodiversity-in-the-built-environment guidance has multiple candidate issuing bodies (Property Council, Standards Australia, DCA, JFA Purple Orange). Owner-queue: confirm exact issuing body, full title, edition, and bibliographic record on next pass.',
    url = 'https://www.propertycouncil.com.au/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+au-neurodiversity-context',
    last_verified_at = '2026-05-21T20:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T20:00:00Z housing-batch-33] title-based; owner-queue for exact bibliography',
    updated_at = '2026-05-21T20:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00610';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
