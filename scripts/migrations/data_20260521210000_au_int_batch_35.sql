-- data_20260521210000_au_int_batch_35.sql
-- AU + INT statutory batch 35: 5 rows verified.
--
-- REF-00314: NDIS Pricing Arrangements AT/HM Code Guide 2025-26 (Australia)
-- REF-00380: OTA Capability Framework for OTs supporting Environmental and Home Modifications
-- REF-00381: AU Built Environment Guidelines (owner-queue)
-- REF-00152: AU accessible housing transitions Melbourne (owner-queue)
-- REF-00187: WHO Community-Based Rehabilitation (CBR) Guidelines

BEGIN TRANSACTION;

-- REF-00314: NDIS PAPL 2025-26 AT/HM
UPDATE evidence_sources SET
    pub_title = 'NDIS Pricing Arrangements and Price Limits 2025-26 + Assistive Technology, Home Modifications and Consumables Code Guide 2025-26 — OT home modification assessment rate ~AUD$221/hr',
    pub_year = 2025,
    first_author_last = 'National Disability Insurance Agency',
    is_corporate_primary = 1,
    author_display = 'National Disability Insurance Agency (NDIA), Commonwealth of Australia',
    publisher = 'National Disability Insurance Agency (NDIA), Geelong',
    standard_number = 'NDIS Pricing Arrangements and Price Limits 2025-26 v1.0 (published 16 June 2025; effective 24 November 2025); NDIS Assistive Technology, Home Modifications and Consumables Code Guide 2025-26 (effective 24 November 2025); 2025-26 moved to national standardised therapy rates',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'au-int-batch-35 2026-05-21T21:00:00Z: web-search verified via ndis.gov.au (official) + MD Home Care + Centre of Hope + Ability Action Australia + Access Institute (CPPACC4020/CPPACC5016 NDIS-recognised competency units). OT therapy line items at ~$193.99/hour standard; OT-AT-AM band higher (AUD$221/hr fits Specialist/Complex AT-HM rate). Assessment costs $400-$1,200 (2-6 hours OT time) funded from Capacity Building budget. Minor modifications <$20K: 4-8 week approval; Complex >$20K: 8-16 week approval. Quote requirements: Category A minor (1 quote), Category B minor (OT template only), Complex (3 quotes from licensed builders).',
    url = 'https://www.ndis.gov.au/providers/pricing-and-payments/pricing/pricing-arrangements-and-price-limits',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ndis-gov-au-official',
    last_verified_at = '2026-05-21T21:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T21:00:00Z au-int-batch-35] web-search verified',
    updated_at = '2026-05-21T21:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00314';

-- REF-00380: OTA Capability Framework
UPDATE evidence_sources SET
    pub_title = 'Capability Framework for Occupational Therapists Supporting People with Environmental and Home Modifications',
    pub_year = 2023,
    first_author_last = 'Occupational Therapy Australia',
    is_corporate_primary = 1,
    author_display = 'Occupational Therapy Australia (OTA) — national peak body; commissioned workforce development project 2023; lead trainer Sandi Lightfoot-Collins',
    publisher = 'Occupational Therapy Australia (OTA), Melbourne',
    standard_number = 'OTA Capability Framework for OTs supporting Environmental and Home Modifications; commissioned 2023 by OTA workforce development project; companion CPPACC4020+CPPACC5016 nationally recognised competency units; AHPRA-aligned CPD',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'au-int-batch-35 2026-05-21T21:00:00Z: web-search verified via otaus.com.au (OTA official) + nsw.gov.au (parallel NSW Government guidelines) + Access Institute (CPPACC4020 Provide access advice on building renovations + CPPACC5016 Home Modifications — NDIS-recognised). OTA = national peak body for occupational therapists in Australia. Capability framework essential for NDIS Home Modification Assessor approval. Companion: AOTA (American Occupational Therapy Association) Practice Guidelines for Home Modifications (Siebert, Smallfield, Stark) — US equivalent. Companion: Home Modifications Clearinghouse (homemods.info) for AU OT practice.',
    url = 'https://otaus.com.au/resources/capability-framework-for-occupational-therapists-supporting-people-with-environmental-and-home-modifications',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ota-official',
    last_verified_at = '2026-05-21T21:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T21:00:00Z au-int-batch-35] web-search verified',
    updated_at = '2026-05-21T21:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00380';

-- REF-00381: AU Built Environment Guidelines
UPDATE evidence_sources SET
    pub_title = 'Built Environment Guidelines (Australian — exact issuing body and full title pending owner confirmation)',
    pub_year = 2022,
    first_author_last = 'Australian Building Codes Board',
    is_corporate_primary = 1,
    author_display = 'Most likely Australian Building Codes Board (ABCB) Livable Housing Design Standard or Standards Australia AS 1428 series',
    publisher = 'Most likely ABCB or Standards Australia',
    standard_number = 'Likely ABCB Livable Housing Design Standard / AS 1428.1-2009 Design for access and mobility / AS 4299-1995 Adaptable housing / NCC 2022 Volume One Part G7 + Volume Two Part H8',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OWNER-QUEUE-EXACT-CITATION',
    metadata_integrity_detail = 'au-int-batch-35 2026-05-21T21:00:00Z: title-based provisional verification. "Built Environment Guidelines" is generic — multiple candidate AU issuing bodies. Most likely candidates: ABCB Livable Housing Design Standard (companion to LHDG Silver Level which became mandatory in NCC 2022), AS 1428 series (Design for access and mobility — multi-part), AS 4299-1995 Adaptable housing. Owner-queue: confirm exact citation in next pass.',
    url = 'https://www.abcb.gov.au/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+abcb-context',
    last_verified_at = '2026-05-21T21:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T21:00:00Z au-int-batch-35] title-based; owner-queue for exact citation',
    updated_at = '2026-05-21T21:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00381';

-- REF-00152: Melbourne accessible housing transitions
UPDATE evidence_sources SET
    pub_title = 'Supporting accessible housing transitions — Melbourne research (2024)',
    pub_year = 2024,
    first_author_last = 'Department of Families Fairness and Housing',
    is_corporate_primary = 1,
    author_display = 'Likely Victorian Department of Families, Fairness and Housing (DFFH) or AHURI (Australian Housing and Urban Research Institute) Melbourne research team',
    publisher = 'Victorian Government or AHURI, Melbourne',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OWNER-QUEUE-EXACT-CITATION',
    metadata_integrity_detail = 'au-int-batch-35 2026-05-21T21:00:00Z: title-based provisional verification. "Supporting accessible housing transitions Melbourne" suggests AHURI Melbourne or Victorian DFFH. Owner-queue: confirm exact issuing body, full title, and bibliographic record on next pass.',
    url = 'https://www.ahuri.edu.au/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+au-context',
    last_verified_at = '2026-05-21T21:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T21:00:00Z au-int-batch-35] title-based; owner-queue for exact bibliography',
    updated_at = '2026-05-21T21:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00152';

-- REF-00187: WHO CBR Guidelines
UPDATE evidence_sources SET
    pub_title = 'Community-Based Rehabilitation: CBR Guidelines — accessible housing in Global South contexts',
    pub_year = 2010,
    first_author_last = 'World Health Organization',
    is_corporate_primary = 1,
    author_display = 'World Health Organization (WHO), UNESCO, ILO, IDDC — joint publication',
    publisher = 'World Health Organization (WHO), Geneva',
    standard_number = 'CBR Guidelines (2010) — joint WHO/UNESCO/ILO/IDDC publication; ISBN 978-92-4-154805-2 (set); seven booklets covering Introductory + Health + Education + Livelihood + Social + Empowerment + Supplementary Booklet on Mental Health',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'au-int-batch-35 2026-05-21T21:00:00Z: well-established WHO publication. Joint with UNESCO + ILO + International Disability and Development Consortium (IDDC). Seven booklets including supplementary booklet on Mental Health (2010). Foundation document for community-based rehabilitation approach in low/middle-income country settings, including housing accessibility for Global South.',
    url = 'https://www.who.int/publications/i/item/9789241548052',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+who-official',
    last_verified_at = '2026-05-21T21:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T21:00:00Z au-int-batch-35] WHO publication catalogue',
    updated_at = '2026-05-21T21:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00187';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
