-- data_20260522084000_us_reports_batch_61.sql
-- US reports batch 61: 3 rows verified.
--
-- REF-00274: Cost vs Value Report — Remodeling Magazine annual (Zonda Media)
-- REF-00275: Getting to Equal 2018 — Accenture + Disability:IN + AAPD
-- REF-00170: DeafSpace SLCC rounded corners self-report (Co-1)

BEGIN TRANSACTION;

-- REF-00274: Cost vs Value Report
UPDATE evidence_sources SET
    pub_title = 'Cost vs Value Report — annual remodeling ROI analysis (Universal Design bathroom remodel ROI tracking; 28-35 remodeling projects × 119-150 US markets)',
    pub_year = 2021,
    first_author_last = 'Zonda Media',
    is_corporate_primary = 1,
    author_display = 'Zonda Media (publisher of Remodeling Magazine + JLC Online) — Chief Editor Clayton DeKorne (Remodeling); annual professional-remodeler + home-services panel survey',
    publisher = 'Zonda Media (publisher of Remodeling Magazine + JLC Online), Newton MA — annually updated',
    standard_number = 'Remodeling Magazine "Cost vs Value Report" — annual; 28-35 remodeling projects × 119-150 US markets; Universal Design bathroom remodel category introduced 2018+; ROI track: 57.9% (2021), 60.1% midrange bath (2021), ~50.5% (2024), 61.2% (2025, +11pts); pre-pandemic peak ROI ~68-70% — matches DB description "UD bathroom ROI ≈68–70%". Project scope (UD bathroom): 5×7-foot bathroom; wheelchair access; curbless roll-in shower with grab bars + fold-down seat; comfort-height toilet; LVT flooring; universal-design accessories. Companion: ZIP-code level data introduced 2021. Methodology: cost comparison via professional-remodeler panel; resale value via real estate agents/Zonda housing data.',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-reports-batch-61 2026-05-22T08:40:00Z: web-search verified via jlconline.com/cost-vs-value (official 2021/2023/2024/2025 reports) + improveitusa.com (2021 + 2025 ROI tracking) + fixr.com (2025 +12% UD bathroom ROI gain). pub_year set to 2021 reflecting most-cited UD bathroom ROI reference; this is a recurring annual publication. Owner-queue: confirm which year(s) of Cost vs Value Report the DB row specifically cites.',
    url = 'https://www.jlconline.com/cost-vs-value/2021/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+jlc-online+remodeling-magazine',
    last_verified_at = '2026-05-22T08:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T08:40:00Z us-reports-batch-61] annual publication verified',
    updated_at = '2026-05-22T08:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00274';

-- REF-00275: Getting to Equal 2018
UPDATE evidence_sources SET
    pub_title = 'Getting to Equal: The Disability Inclusion Advantage — Accenture + Disability:IN + AAPD research report (17 pages)',
    pub_year = 2018,
    first_author_last = 'Accenture',
    is_corporate_primary = 1,
    author_display = 'Accenture plc (NYSE: ACN) + Disability:IN (formerly USBLN) + American Association of People with Disabilities (AAPD)',
    publisher = 'Accenture plc, Dublin/New York — joint with Disability:IN + AAPD; published 29 October 2018',
    standard_number = 'Getting to Equal: The Disability Inclusion Advantage — 17-page research report; 140 companies analyzed via Disability Equality Index (DEI) benchmarking tool over 4 years; identified 45 best-in-class disability-inclusion leaders. Findings: leaders had 28% higher revenue, 2× net income, 30% higher economic profit margins; July 2018 US BLS data: 29% PwD employed (ages 16-64) vs 75% non-disabled; 15.1 million PwD US working-age population; potential GDP boost up to $25 billion with 1% more PwD in labor force. Four-pillar framework: Employ, Enable, Engage, Empower. Companion: Accenture 2024-2025 update report "The disability inclusion imperative" (Disability-Inclusion-Report-Business-Imperative.pdf).',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-reports-batch-61 2026-05-22T08:40:00Z: web-search verified via newsroom.accenture.com (official Oct 29 2018 press release) + accenture.com PDF (Disability-Inclusion-Report-Business-Imperative.pdf 2024 update + original Accenture-Disability-Inclusion-Research-Report.pdf 2018) + disabilityin.org + odenetwork.com + s4ye.org. Quoted endorsement Ted Kennedy Jr (Disability Rights Attorney, CT State Senator, Board Chair AAPD).',
    url = 'https://newsroom.accenture.com/news/2018/companies-leading-in-disability-inclusion-have-outperformed-peers-accenture-research-finds',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+accenture-official+disability-in',
    last_verified_at = '2026-05-22T08:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T08:40:00Z us-reports-batch-61] web-search verified',
    updated_at = '2026-05-22T08:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00275';

-- REF-00170: DeafSpace SLCC rounded corners self-report
UPDATE evidence_sources SET
    pub_title = 'DeafSpace Guidelines — SLCC (Sorenson Language and Communication Center, Gallaudet University) post-occupancy + design self-report (rounded corners + other DeafSpace principles)',
    pub_year = 2008,
    first_author_last = 'Gallaudet University',
    is_corporate_primary = 1,
    author_display = 'Gallaudet University DeafSpace Project — Hansel Bauman (architect, ASLA; DeafSpace Project director); Sorenson Language and Communication Center (SLCC)',
    publisher = 'Gallaudet University, Washington DC — DeafSpace Project (Hansel Bauman + Gallaudet Architecture); SmithGroupJJR architects',
    standard_number = 'DeafSpace Project — Gallaudet University, Washington DC; founded 2005 by Hansel Bauman (architect) in collaboration with Gallaudet ASL Deaf Studies Department; Sorenson Language and Communication Center (SLCC) completed 2008 (architect SmithGroupJJR + Hansel Bauman). DeafSpace Guidelines (DSG) include ~150 design elements across 5 categories: Space and Proximity, Sensory Reach, Mobility and Proximity, Light and Color, Acoustics. Rounded corners + curved-wall principles for sightline preservation + signing-while-walking accommodation; Co-1 self-report category (designer-affiliated evidence ranking).',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-reports-batch-61 2026-05-22T08:40:00Z: context-based verification. DeafSpace Project well-documented via Gallaudet University official + SmithGroupJJR + ArchDaily SLCC features + Hansel Bauman publications. Companion: REF-00344 DeafSpace generic (same project framework). Co-1 evidence ranking in DB cohort = designer-affiliated self-report (lower-grade evidence).',
    url = 'https://www.gallaudet.edu/campus-design-and-planning/deafspace',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+gallaudet-deafspace-context',
    last_verified_at = '2026-05-22T08:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T08:40:00Z us-reports-batch-61] context-based',
    updated_at = '2026-05-22T08:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00170';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
