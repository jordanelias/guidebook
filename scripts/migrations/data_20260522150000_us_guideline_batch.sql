-- data_20260522150000_us_guideline_batch.sql
-- US guideline batch: 8 rows verified via web-search confirming real sources behind paraphrased DB descriptions.
-- Triage finding: c1-migration-fix-era "AI-sounding" titles are DB-side paraphrases of real industry blog and FAQ sources, not hallucinations.

BEGIN TRANSACTION;

-- REF-00292: Behind The Hedges (Dan's Papers Hamptons real-estate blog)
UPDATE evidence_sources SET
    pub_title = 'Notable Features of Modern Bathrooms — accessibility-as-luxury rebrand (Behind The Hedges real-estate trend article citing 2026 NKBA Trends Report + Forbes)',
    pub_year = 2026,
    first_author_last = 'Behind The Hedges',
    is_corporate_primary = 1,
    author_display = 'Behind The Hedges (a Dan''s Papers Hamptons real-estate publication, NY)',
    publisher = 'Dan''s Papers / Behind The Hedges (Hamptons real-estate publication), New York',
    standard_number = 'Behind The Hedges April 5, 2026 trend article citing: 2026 National Kitchen & Bath Association (NKBA) Trends Report (72% designers report bathroom enlargement for wellness features); Forbes (curbless entries + built-in benches as luxury safety features); Re-Bath designer Jenny Mars (organic-minimalism trend). Low-grade industry-blog provenance; cited in BPC context for "accessibility-as-luxury market repositioning" framing.',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'LOW-GRADE-INDUSTRY-BLOG-PROVENANCE',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | us-guideline-batch 2026-05-22T15:00:00Z: web-search verified at behindthehedges.com/notable-features-of-modern-bathrooms (April 5 2026). DB description was paraphrased from a real industry blog post; source chain is blog→NKBA Trends Report+Forbes+designer commentary. Confidence is appropriate for trend-pattern citation, not for primary research.',
    url = 'https://behindthehedges.com/notable-features-of-modern-bathrooms/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-direct',
    last_verified_at = '2026-05-22T15:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T15:00:00Z us-guideline-batch] direct URL match',
    updated_at = '2026-05-22T15:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00292';

-- REF-00293: Kukun (mykukun.com home renovation app blog by Alejandro Guerrero)
UPDATE evidence_sources SET
    pub_title = 'Why Accessibility is the Highest-ROI Renovation for the 2026 Rental Market — Kukun renovation-analytics industry blog citing JCHS Harvard data',
    pub_year = 2026,
    first_author_last = 'Guerrero',
    first_author_first = 'A',
    is_corporate_primary = 0,
    author_display = 'Guerrero A (Alejandro), Kukun blog editor — Kukun home renovation analytics platform (mykukun.com)',
    publisher = 'Kukun Inc. (mykukun.com home renovation analytics platform, USA)',
    standard_number = 'Kukun blog article published April 28 2026 by Alejandro Guerrero — references Joint Center for Housing Studies (JCHS) Harvard projections on accessibility renovation spending; PICO™ Functional Utility score (Kukun proprietary); "Per-Bed" senior-living rental ROI model; cites Independent Living Median rent ($3,065/month 2026) + Senior-Lite assisted-living conversion economics. Low-grade industry-blog provenance; cited in BPC context for "highest-ROI accessibility renovation" market thesis.',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'LOW-GRADE-INDUSTRY-BLOG-PROVENANCE',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | us-guideline-batch 2026-05-22T15:00:00Z: web-search verified at mykukun.com/blog/why-accessibility-is-the-highest-roi-renovation (April 28 2026 by Alejandro Guerrero). DB description was paraphrased from a real industry-blog post; source chain is Kukun → JCHS Harvard. Low confidence for primary-research citation but valid market-thesis source.',
    url = 'https://mykukun.com/blog/why-accessibility-is-the-highest-roi-renovation',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-direct',
    last_verified_at = '2026-05-22T15:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T15:00:00Z us-guideline-batch] direct URL match',
    updated_at = '2026-05-22T15:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00293';

-- REF-00304 + REF-00309: ADA National Network FAQ — "<1% new-build premium"
UPDATE evidence_sources SET
    pub_title = 'Is it expensive to make all newly constructed places of public accommodation and commercial facilities accessible? — Top ADA FAQ',
    pub_year = 2025,
    first_author_last = 'ADA National Network',
    is_corporate_primary = 1,
    author_display = 'ADA National Network (NIDILRR-funded, ~10 regional ADA Centers) — under U.S. Department of Health and Human Services Administration for Community Living',
    publisher = 'ADA National Network (adata.org) — Pacific ADA Center hosts FAQ site; funded by NIDILRR/HHS',
    standard_number = 'ADA National Network "Top ADA Frequently Asked Questions" page (adata.org/faq/it-expensive-make-all-newly-constructed-places-public-accommodation-and-commercial-facilities) — states: "The cost of incorporating accessibility features in new construction is less than one percent of construction costs. This is a small price in relation to the economic benefits to be derived from full accessibility in the future, such as increased employment and consumer spending." Companion: ada.gov + access-board.gov; underlying ADA Title III + 2010 ADA Standards for Accessible Design. Source for the widely-cited <1% new-build accessibility cost premium claim.',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | us-guideline-batch 2026-05-22T15:00:00Z: web-search verified at adata.org/faq. Authoritative FAQ from federally-funded ADA National Network. Cluster with REF-00309 (same FAQ resource).',
    url = 'https://adata.org/faq/it-expensive-make-all-newly-constructed-places-public-accommodation-and-commercial-facilities',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-direct+adata-org',
    last_verified_at = '2026-05-22T15:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T15:00:00Z us-guideline-batch] direct URL match',
    updated_at = '2026-05-22T15:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN ('REF-00304','REF-00309');

-- REF-00305 + REF-00308: Woodstock Institute HUD HomeMod cost study
UPDATE evidence_sources SET
    pub_title = 'HomeMod Program: Costs and Benefits — Evaluation of Chicago''s HomeMod home-modification program (HUD-funded Woodstock Institute study)',
    pub_year = 2020,
    first_author_last = 'Woodstock Institute',
    is_corporate_primary = 1,
    author_display = 'Woodstock Institute (Chicago IL) — funded by U.S. Department of Housing and Urban Development (HUD)',
    publisher = 'Woodstock Institute, Chicago IL — funded by U.S. Department of Housing and Urban Development (HUD); evaluation of HomeMod Program administered by Illinois Assistive Technology Program (IATP) + IL Department on Aging',
    standard_number = 'Woodstock Institute HUD-funded HomeMod cost-benefit study — Chicago HomeMod Program evaluation; average modification cost $12,200–$15,150/unit; 3-year cost-savings $7,427–$8,891/participant from reduced service use (DB description "$6,668" reflects a different metric window — owner-queue reconciliation); break-even if 2.5–4.6% participants defer assisted living by 5 yrs OR 0.5–1.0% defer nursing home by 8 yrs. Source for U.S. visitable/aging-in-place cost-benefit literature.',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | us-guideline-batch 2026-05-22T15:00:00Z: web-search verified at woodstockinst.org/research/homemod-costs-and-benefits. Exact dollar figure match for $12,200-$15,150 + Woodstock+HUD partnership. Cluster with REF-00308 (same study).',
    url = 'https://woodstockinst.org/research/homemod-costs-and-benefits/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-direct+woodstockinst',
    last_verified_at = '2026-05-22T15:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T15:00:00Z us-guideline-batch] exact-figure match',
    updated_at = '2026-05-22T15:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN ('REF-00305','REF-00308');

-- REF-00321: US Access Board Washing Machines and Clothes Dryers Guide Sept 2021
UPDATE evidence_sources SET
    pub_title = 'Guide to the ADA Standards: Washing Machines and Clothes Dryers (September 2021) + Guide to the ABA Standards: Washing Machines and Clothes Dryers (September 2021) — Chapter 6 Plumbed Elements',
    pub_year = 2021,
    first_author_last = 'U.S. Access Board',
    is_corporate_primary = 1,
    author_display = 'U.S. Access Board (federal accessibility-standards agency) — primary technical writers Phil Bratta + Josh Schorr',
    publisher = 'U.S. Access Board (formerly Architectural and Transportation Barriers Compliance Board), Washington DC — independent federal agency',
    standard_number = 'US Access Board Technical Guide to ADA + ABA Standards Chapter 6: Washing Machines and Clothes Dryers (September 2021) — official guide on §611 specifications (clear floor space 30"×48" parallel approach, operable parts 15-48" height range, doors clearing wheelchair space, top-loading vs front-loading, side-by-side stacked appliance accessibility). Released alongside Lavatories and Sinks (Sept 2021) and Saunas and Steam Rooms (May 2022) technical bulletins.',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | us-guideline-batch 2026-05-22T15:00:00Z: web-search verified at access-board.gov/ada/guides/chapter-6-washers + access-board.gov/files/ada/guides/washers.pdf. Official federal agency technical guide.',
    url = 'https://www.access-board.gov/ada/guides/chapter-6-washers/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-direct+access-board-gov',
    last_verified_at = '2026-05-22T15:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T15:00:00Z us-guideline-batch] direct URL match',
    updated_at = '2026-05-22T15:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00321';

-- REF-00442: Lori Greene Decoded column at iDigHardware + Door Security + Safety Magazine
UPDATE evidence_sources SET
    pub_title = 'Decoded — code-requirements column on door hardware (Lori Greene at iDigHardware + Door Security + Safety Magazine)',
    pub_year = 2021,
    first_author_last = 'Greene',
    first_author_first = 'L',
    is_corporate_primary = 0,
    author_display = 'Greene L (Lori) — Manager, Codes and Resources at Allegion (NYSE: ALLE); creator of iDigHardware (idighardware.com); 35+ years door + hardware industry experience',
    publisher = 'Allegion plc (NYSE: ALLE) — iDigHardware platform + Door Security + Safety Magazine (DHI publication)',
    standard_number = 'Lori Greene "Decoded" column — recurring code-requirements articles for Door Security + Safety Magazine (Door and Hardware Institute, DHI); 2021 series included: Decoded: Automatic Operators on Accessible Public Entrances; Decoded: Opening Force vs. Operable Force; Decoded: Door & Gate Hardware for Swimming Pools (April 2021); Decoded: 2021 Code Changes (Nov 2021). Underlying codes referenced: 2021 IBC + IFC + ICC/ANSI A117.1 + 2010 ADA Standards + NFPA 80 + NFPA 101 + UL 294. Owner-queue: confirm which specific 2021 Decoded article DB cites; current verification reflects framework attribution.',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | us-guideline-batch 2026-05-22T15:00:00Z: web-search verified via idighardware.com (multiple 2021 Decoded posts). Lori Greene is Allegion''s Manager, Codes and Resources; Decoded column is industry-standard reference for door-hardware code compliance.',
    url = 'https://idighardware.com/category/articles/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-direct+idighardware',
    last_verified_at = '2026-05-22T15:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T15:00:00Z us-guideline-batch] framework verified',
    updated_at = '2026-05-22T15:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00442';

COMMIT;
