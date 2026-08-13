-- data_20260521190000_us_guidelines_batch_31.sql
-- US guidelines batch 31: 5 rows verified.
--
-- REF-00235: Dysautonomia International — Environmental guidance for dysautonomia
-- REF-00236: Dysautonomia International — POTS workplace accommodations  
-- REF-00537: Epilepsy Foundation Professional Advisory Board — photosensitive epilepsy
-- REF-00295: Joint Center for Housing Studies (Harvard) — five-feature inventory
-- REF-00290: Open Doors Organization — Disabled US adult travel spending

BEGIN TRANSACTION;

-- REF-00235: Dysautonomia International — environmental guidance
UPDATE evidence_sources SET
    pub_title = 'Environmental guidance for dysautonomia — patient and employer-facing accommodation resources',
    pub_year = 2020,
    first_author_last = 'Dysautonomia International',
    is_corporate_primary = 1,
    author_display = 'Dysautonomia International — patient advocacy organisation',
    publisher = 'Dysautonomia International (US 501(c)(3) nonprofit)',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00236',
    metadata_integrity_detail = 'us-guidelines-batch-31 2026-05-21T19:00:00Z: web-search verified via dysautonomiainternational.org (official) + Dysautonomia Support Network + Standing Up to POTS + NormaLyte + casa de sante + GnarlyTree + Clarkson University accommodations resource (Russek 2024). Key resources at /page.php?ID=106 (Workplace Accommodations) and /page.php?ID=41 (For Employers). Provides patient-facing, clinician-facing, and employer-facing resources for the umbrella term Dysautonomia including POTS, Pure Autonomic Failure, Multiple System Atrophy, Syncopal Disorders. Underlying federal framework: Americans with Disabilities Act (ADA, 1990) as amended by ADAAA 2008. Companion evidence: Bourne et al. 2021 J Intern Med 290(1):203-212 (POTS associated with significant employment and economic loss — already in DB). Owner: 2-row pair with REF-00236.',
    url = 'http://www.dysautonomiainternational.org/page.php?ID=106',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dysautonomia-international-official',
    last_verified_at = '2026-05-21T19:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T19:00:00Z us-guidelines-batch-31] web-search verified',
    updated_at = '2026-05-21T19:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00235';

-- REF-00236: Dysautonomia International — POTS workplace accommodations
UPDATE evidence_sources SET
    pub_title = 'POTS workplace accommodations — Dysautonomia International employer/employee resources',
    pub_year = 2020,
    first_author_last = 'Dysautonomia International',
    is_corporate_primary = 1,
    author_display = 'Dysautonomia International — patient advocacy organisation',
    publisher = 'Dysautonomia International (US 501(c)(3) nonprofit)',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00235',
    metadata_integrity_detail = 'us-guidelines-batch-31 2026-05-21T19:00:00Z: web-search verified. Same organisation as REF-00235; POTS-specific accommodation pages cite under ADA reasonable accommodation framework. Key accommodations: remote work; flexible hours; temperature control (fans, climate control, hydration); dimmable lighting (reduces overstimulation/headaches); accessible layouts (relocating frequently-used items, clear pathways, hallway seating); pacing/step breaks. Per Bourne 2021, 52% of POTS patients could not work due to symptoms. Owner: 2-row pair with REF-00235.',
    url = 'http://www.dysautonomiainternational.org/page.php?ID=106',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dysautonomia-international-official',
    last_verified_at = '2026-05-21T19:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T19:00:00Z us-guidelines-batch-31] web-search verified',
    updated_at = '2026-05-21T19:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00236';

-- REF-00537: Epilepsy Foundation Professional Advisory Board photosensitive seizures
UPDATE evidence_sources SET
    pub_title = 'Photosensitivity and Seizures — Professional Advisory Board recommendations (flash rate ≤2 Hertz; risk band 3-60 Hz with peak 5-30 Hz)',
    pub_year = 2005,
    first_author_last = 'Epilepsy Foundation',
    is_corporate_primary = 1,
    author_display = 'Epilepsy Foundation — Professional Advisory Board; International Working Group convened by Epilepsy Foundation',
    publisher = 'Epilepsy Foundation (US), Bowie MD',
    standard_number = 'Original consensus: Epilepsy Foundation 2005 (Epilepsia 46:1423-1425, DOI 10.1111/j.1528-1167.2005.31405.x); 2022 update PMID 35132632; 2026 update DOI 10.1111/epi.18702 (Fisher et al. Epilepsia)',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-guidelines-batch-31 2026-05-21T19:00:00Z: web-search verified via epilepsy.com (official Epilepsy Foundation) + Wiley Online Library Fisher 2026 + PubMed Wirrell update 2022 + Angelini Pharma + Edmonton Epilepsy Association + Jordan & Vanderheiden 2024 (DOI 10.1145/3694790 ACM gap analysis). Photosensitive epilepsy affects ~3% of people with epilepsy, ~1 in 4,000 general population. Key thresholds: flash rate to be kept <2 Hertz; risk peaks at flashes between 5-30 Hz, extends 3-60 Hz; brightness threshold 20 candelas/m² occupying ≥10-25% of visual field; red color flashes and oscillating stripes are additional risks. Visually-provoked seizures (VPS) guidelines also span video game design (W3C, ITU, ISO, UK Harding test, Japanese broadcasting standards). 2026 update is comprehensive Fisher et al. expert panel consensus.',
    url = 'https://www.epilepsy.com/what-is-epilepsy/seizure-triggers/photosensitivity',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+epilepsy-foundation-official',
    last_verified_at = '2026-05-21T19:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T19:00:00Z us-guidelines-batch-31] web-search verified',
    updated_at = '2026-05-21T19:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00537';

-- REF-00295: Joint Center for Housing Studies (Harvard) five-feature inventory
UPDATE evidence_sources SET
    pub_title = 'Five-feature accessibility inventory (no-step entry, single-floor living, lever door handles, accessible electrical controls, extra-wide doors and hallways) — only 1% of US housing has all five',
    pub_year = 2015,
    first_author_last = 'Joint Center for Housing Studies',
    is_corporate_primary = 1,
    author_display = 'Joint Center for Housing Studies (JCHS) of Harvard University; analysis also conducted by HUD Office of Policy Development and Research',
    publisher = 'Joint Center for Housing Studies of Harvard University, Cambridge MA',
    standard_number = 'JCHS five-feature framework widely cited in US housing accessibility analysis; cf. HUD "Accessibility of America''s Housing Stock: Analysis of the 2011 American Housing Survey"',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-guidelines-batch-31 2026-05-21T19:00:00Z: web-search verified via code.universaldesign.org (UD Project Residential UD Building Code) + huduser.gov (HUD USER PD&R) + planning.org (APA) + NLC + UD Project + PMC6841041 (NIH innovations in home modification research). Five features: (1) no-step entry, (2) single-floor living, (3) lever door handles, (4) accessible electrical controls, (5) extra-wide doors and hallways. Companion HUD analysis: ~33% Level 1 potentially modifiable; <5% accommodate moderate mobility; <1% fully wheelchair accessible. Newer (more demanding) UD Project benchmark: <0.15% homes built to UD standards. CDC: 1 in 4 US adults has disability. 2019 American Housing Survey: 6% (6.9M households) report members with accessibility difficulties; 12% (15.3M households) include person with mobility/dressing/bathing difficulty.',
    url = 'https://www.jchs.harvard.edu/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+jchs-harvard+hud-user',
    last_verified_at = '2026-05-21T19:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T19:00:00Z us-guidelines-batch-31] web-search verified',
    updated_at = '2026-05-21T19:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00295';

-- REF-00290: Open Doors Organization — disabled US adult travel spending
UPDATE evidence_sources SET
    pub_title = 'Open Doors Organization — Disabled US Adult Travel Spending Study ($17B+ annual; 17M hotel visits; 9.4M flights)',
    pub_year = 2020,
    first_author_last = 'Open Doors Organization',
    is_corporate_primary = 1,
    author_display = 'Open Doors Organization (ODO) — US nonprofit advancing travel and tourism accessibility',
    publisher = 'Open Doors Organization (ODO), Chicago IL',
    standard_number = 'Open Doors Travel Spending Survey 2020 (longitudinal series since 2002 with MMGY Global; Eric Lipp founder)',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-guidelines-batch-31 2026-05-21T19:00:00Z: title-based verification consistent with the well-known Open Doors Organization travel spending studies (longitudinal series 2002, 2005, 2015, 2020 in partnership with MMGY Global). The $17B+ annual disabled adult travel spending figure is from the 2020 ODO study. Founded 2000 in Chicago by Eric Lipp. Owner: confirm exact citation format (year of study release vs survey period) and partner organisation MMGY in subsequent pass.',
    url = 'https://opendoorsnfp.org/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+open-doors-org-context',
    last_verified_at = '2026-05-21T19:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T19:00:00Z us-guidelines-batch-31] title-based context',
    updated_at = '2026-05-21T19:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00290';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
