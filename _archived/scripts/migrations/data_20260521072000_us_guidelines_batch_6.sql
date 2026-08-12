-- data_20260521072000_us_guidelines_batch_6.sql
--
-- US guidelines batch 6: 4 rows web-search verified to COMPLETE-STATUTORY.
--
-- REF-00267: Maisel J.L., Smith E., Steinfeld E. (2008) "Increasing Home Access: Designing for
--            Visitability" AARP Public Policy Institute
-- REF-00213: ADA National Network "Opening Doors to Everyone" factsheet (2017)
-- REF-00206: Greene L. (2014) "Understanding the New Accessibility Requirements for Doors"
--            Construction Specifier / Allegion
-- REF-00112: Hunt J.M., Sine D.M., McMurray K.N. (2024) "Design Guide for the Built Environment
--            of Behavioral Health Facilities" 26th revision; Behavioral Health Facility Consulting

BEGIN TRANSACTION;

-- REF-00267: AARP Visitability paper
UPDATE evidence_sources SET
    pub_title = 'Increasing Home Access: Designing for Visitability',
    pub_year = 2008,
    first_author_last = 'Maisel',
    first_author_first = 'Jordana',
    is_corporate_primary = 0,
    author_display = 'Maisel, J. L. (RERC-UD/IDEA Center, University at Buffalo); Smith, E. (Concrete Change); Steinfeld, E. (IDEA Center, University at Buffalo)',
    author_count = 3,
    author_count_is_complete = 1,
    publisher = 'AARP Public Policy Institute',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-guidelines-batch-6 2026-05-21T07:20:00Z: web-search verified via aarp.org + ncil.org + idea.ap.buffalo.edu + Harvard JCHS. Published August 2008 by AARP Public Policy Institute, Washington DC. 117pp policy report examining visitability initiatives in US housing, evaluating their potential for aging-in-place independence. Co-authored by Maisel (Research Associate RERC-UD), Smith (founder Concrete Change), Steinfeld (Director IDEA Center, co-author Principles of Universal Design).',
    url = 'https://ncil.org/wp-content/uploads/2016/10/AARP-Increasing-Home-Access.pdf',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+aarp-public-policy',
    last_verified_at = '2026-05-21T07:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T07:20:00Z us-guidelines-batch-6] web-search verified',
    updated_at = '2026-05-21T07:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00267';

-- REF-00213: ADA Network Opening Doors to Everyone factsheet
UPDATE evidence_sources SET
    pub_title = 'Opening Doors To Everyone — ADA accessibility factsheet on door requirements',
    pub_year = 2017,
    first_author_last = 'ADA National Network',
    is_corporate_primary = 1,
    author_display = 'ADA National Network (adata.org)',
    publisher = 'ADA National Network',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-guidelines-batch-6 2026-05-21T07:20:00Z: web-search verified via adata.org. ADA Network is a federally-funded program (NIDILRR Office of Special Education and Rehabilitative Services). Factsheet provides guidance on accessible doors per Americans with Disabilities Act (ADA) — 32-inch clear width minimum, 5-lb max force, lever/pull handle requirements, 60% accessible entrance requirement.',
    url = 'https://adata.org/factsheet/opening-doors-everyone',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ada-network-official',
    last_verified_at = '2026-05-21T07:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T07:20:00Z us-guidelines-batch-6] web-search verified',
    updated_at = '2026-05-21T07:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00213';

-- REF-00206: Greene 2014 Construction Specifier
UPDATE evidence_sources SET
    pub_title = 'Understanding the New Accessibility Requirements for Doors',
    pub_year = 2014,
    first_author_last = 'Greene',
    first_author_first = 'Lori',
    is_corporate_primary = 0,
    author_display = 'Greene, L. (Manager of Codes and Resources, Allegion)',
    author_count = 1,
    author_count_is_complete = 1,
    journal_name = 'Construction Specifier',
    publisher = 'Construction Specifier (CSI / Kenilworth Media)',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-guidelines-batch-6 2026-05-21T07:20:00Z: web-search verified via constructionspecifier.com + idighardware.com + allegion.com. Published June 2014. Interpretation of 2010 ADA Standards door-hardware requirements: 5-lb force limit, 32-in clear width, BHMA A156.10 (power-operated) and A156.19 (low-energy/power-assist) standards. Industry-practice guidance article.',
    url = 'https://www.constructionspecifier.com/understanding-new-accessibility-requirements-for-doors/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+construction-specifier',
    last_verified_at = '2026-05-21T07:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T07:20:00Z us-guidelines-batch-6] web-search verified',
    updated_at = '2026-05-21T07:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00206';

-- REF-00112: Behavioral Health Design Guide (26th revision)
UPDATE evidence_sources SET
    pub_title = 'Design Guide for the Built Environment of Behavioral Health Facilities — 8.4 / 26th Revision',
    pub_year = 2024,
    first_author_last = 'Hunt',
    first_author_first = 'James M.',
    is_corporate_primary = 0,
    author_display = 'Hunt, J. M. (AIA, NCARB); Sine, D. M. (DrBE, ARM, CSP, CPHRM); McMurray, K. N. (AIA, EDAC, MBA)',
    author_count = 3,
    author_count_is_complete = 1,
    publisher = 'Behavioral Health Facility Consulting (BHFC) — formerly published by Facility Guidelines Institute (FGI); originally NAPHS (National Association of Psychiatric Health Systems)',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-guidelines-batch-6 2026-05-21T07:20:00Z: web-search verified via bhfcllc.com + fgiguidelines.org. Stored "Behavioral Health Facility Compendium Design Guide" corrected to canonical title "Design Guide for the Built Environment of Behavioral Health Facilities". 2024 edition is 26th revision (matches stored). Originally posted 2003. Classifies facility areas Level 1-5 by risk. Companion to FGI Guidelines for Design and Construction of Hospitals + Outpatient Facilities.',
    url = 'https://www.bhfcllc.com/design-guide',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+bhfc-official',
    last_verified_at = '2026-05-21T07:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T07:20:00Z us-guidelines-batch-6] web-search verified',
    updated_at = '2026-05-21T07:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00112';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
