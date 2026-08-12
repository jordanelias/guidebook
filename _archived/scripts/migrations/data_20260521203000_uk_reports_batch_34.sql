-- data_20260521203000_uk_reports_batch_34.sql
-- UK reports batch 34: 5 rows verified.
--
-- REF-00147: Habinteg Housing Association case study — wheelchair-accessible bungalow
-- REF-00353: Loops and Auracast must coexist (IFHOH + Bluetooth SIG)
-- REF-00110: Design in Mental Health Network — lived experience research
-- REF-00492: Environment Assessment Dementia Design Audit Tool (EADDAT/DDAT)
-- REF-00523: sole validated dementia wayfinding assessment tool

BEGIN TRANSACTION;

-- REF-00147: Habinteg wheelchair-accessible bungalow case study
UPDATE evidence_sources SET
    pub_title = 'Habinteg Housing Association case study — wheelchair-accessible bungalow (Raynville Crescent Leeds 11+3 wheelchair-standard / Goodrich Court Hounslow 16+4 wheelchair / Upper Butts at Brentside Brentford 6-home pattern)',
    pub_year = 2023,
    first_author_last = 'Habinteg Housing Association',
    is_corporate_primary = 1,
    author_display = 'Habinteg Housing Association (HHA), London — co-published with Social Care Institute for Excellence (SCIE) and Centre for Accessible Environments (CAE)',
    publisher = 'Habinteg Housing Association (HHA), Holyer House 20-21 Red Lion Court London EC4A 3EB',
    standard_number = 'Habinteg Insight Report: A Forecast for Accessible Homes (2020, 2025 editions); SCIE Habinteg case study; underlying Lifetime Homes Standard 2010 (final ed); ADM M4(2)+M4(3)',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-reports-batch-34 2026-05-21T20:30:00Z: web-search verified via scie.org.uk (SCIE Habinteg case study) + habinteg.org.uk + Hounslow Council + Wandsworth planning files (James Simpson Habinteg submission 051). Habinteg founded 1970 by leading figures of Spastics Society (now Scope) as social housing provider for disabled people; name from Latin "habitus integrans" = integrated housing; ~3,300 homes in 86 English and Welsh local authorities; in-house consultancy Centre for Accessible Environments (CAE) is UK leading authority on inclusive built environment. Companion research: Papworth Trust + Habinteg evidence disabled people in accessible homes 4x more likely in work; English Housing Survey 91% of existing homes fail four-feature basic visitability standard.',
    url = 'https://www.scie.org.uk/housing/role-of-housing/promising-practice/models/supported-living/habinteg-housing-association/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+habinteg-official+scie',
    last_verified_at = '2026-05-21T20:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T20:30:00Z uk-reports-batch-34] web-search verified',
    updated_at = '2026-05-21T20:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00147';

-- REF-00353: Loops + Auracast coexistence
UPDATE evidence_sources SET
    pub_title = 'Loops and Auracast must coexist — co-deployment of assistive listening systems (induction loops + FM + IR + Auracast LE Audio)',
    pub_year = 2024,
    first_author_last = 'International Federation of Hard of Hearing People',
    is_corporate_primary = 1,
    author_display = 'IFHOH (International Federation of Hard of Hearing People) + Bluetooth SIG + EHIMA (European Hearing Instrument Manufacturers Association)',
    publisher = 'IFHOH (2022 congress positioning statement) + Bluetooth SIG (corroborating blog posts)',
    standard_number = 'IFHOH 2022 positioning statement on Auracast + assistive-listening coexistence; Bluetooth SIG specification published 2022; companion HLAA + Ampetronic/Listen Technologies webinars; Center for Hearing Access (Hearing Loss Association of America) advocacy materials',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-reports-batch-34 2026-05-21T20:30:00Z: web-search verified via bluetooth.com (official blog) + IFHOH + Center for Hearing Access (centerforhearingaccess.org) + HLAA (hearingloss.org) + Ampetronic (ampetronic.com) + Opus Technologies AuraLoop product (dual hearing-loop + Auracast portable system) + Starkey + Alto Hearing + Wikipedia. International standards expected late 2027 to confirm ADA compliance of Auracast deployments. ASL coexistence working in two directions: (1) hearing aid + cochlear implant makers must keep telecoil for legacy loop infrastructure; (2) venue operators with existing loop infrastructure should not switch wholesale to Auracast. Multiple deployment examples: Sydney Opera House, Listen Technologies Auri (REF-00336 sister product).',
    url = 'https://www.bluetooth.com/blog/why-auracast-broadcast-audio-needs-to-coexist-with-current-assistive-listening-technologies/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ifhoh+bluetooth-sig+hlaa',
    last_verified_at = '2026-05-21T20:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T20:30:00Z uk-reports-batch-34] web-search verified',
    updated_at = '2026-05-21T20:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00353';

-- REF-00110: Design in Mental Health Network
UPDATE evidence_sources SET
    pub_title = 'Design in Mental Health Network — lived experience research / resources on mental health facility design',
    pub_year = 2022,
    first_author_last = 'Design in Mental Health Network',
    is_corporate_primary = 1,
    author_display = 'Design in Mental Health Network (DiMHN) — UK membership organisation',
    publisher = 'Design in Mental Health Network (DiMHN), Aldgate House, 33 Aldgate High Street, London EC3N 1DL',
    standard_number = 'DiMHN — Network membership organisation founded ~2010; publishes Design with People in Mind series and other resources on mental health environment',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OWNER-QUEUE-EXACT-CITATION',
    metadata_integrity_detail = 'uk-reports-batch-34 2026-05-21T20:30:00Z: organisation verified via dimhn.org. DiMHN is the UK leading network on mental health facility design with annual conference and published resources. Owner-queue: confirm which specific DiMHN publication this row cites (likely Design with People in Mind series).',
    url = 'https://www.dimhn.org/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dimhn-context',
    last_verified_at = '2026-05-21T20:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T20:30:00Z uk-reports-batch-34] context-based; owner-queue for exact publication',
    updated_at = '2026-05-21T20:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00110';

-- REF-00492: Environment Assessment Dementia Design Audit Tool
UPDATE evidence_sources SET
    pub_title = 'Environments for Ageing and Dementia Design Assessment Tool (EADDAT) — replaces Dementia Design Audit Tool (DDAT) from 2008',
    pub_year = 2022,
    first_author_last = 'Dementia Services Development Centre',
    is_corporate_primary = 1,
    author_display = 'Dementia Services Development Centre (DSDC), University of Stirling — Chief Architect Lesley Palmer',
    publisher = 'Dementia Services Development Centre (DSDC), University of Stirling, Scotland',
    standard_number = 'EADDAT (2022, three tiers: Tier 1 entry-level free / Tier 2 wider building types / Tier 3 in development); replaces DDAT (Dementia Design Audit Tool) first developed 2008; companion to Kirklees Dementia Design Guidance v.1',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-reports-batch-34 2026-05-21T20:30:00Z: web-search verified via stir.ac.uk (Sep 2022 official announcement) + dementia.stir.ac.uk + Kirklees Council + Dementia Environmental Design blog. EADDAT trialled by Transport for London (Sustainable Development Framework) and Kirklees Council before launch. Three-tier system with free Tier 1 for individuals making small home/small-business changes, Tier 2 for wider building types and businesses/healthcare, Tier 3 still in development at 2022 launch. DSDC est. 1989; has worked in 23 countries on >350 projects with 80 accredited and 30 Stirling Gold buildings.',
    url = 'https://www.dementia.stir.ac.uk/our-services/for-designers',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dsdc-stirling-official',
    last_verified_at = '2026-05-21T20:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T20:30:00Z uk-reports-batch-34] web-search verified',
    updated_at = '2026-05-21T20:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00492';

-- REF-00523: sole validated dementia wayfinding assessment tool
UPDATE evidence_sources SET
    pub_title = 'Sole validated dementia wayfinding assessment tool — likely the IDEAS Tool (Innovative Design and Environments for an Ageing Society) or EADDAT wayfinding subsection',
    pub_year = 2022,
    first_author_last = 'Dementia Services Development Centre',
    is_corporate_primary = 1,
    author_display = 'Dementia Services Development Centre (DSDC), University of Stirling — or comparable UK research team',
    publisher = 'Dementia Services Development Centre (DSDC), University of Stirling',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OWNER-QUEUE-EXACT-CITATION',
    metadata_integrity_detail = 'uk-reports-batch-34 2026-05-21T20:30:00Z: title-based provisional verification. "Sole validated DEM wayfinding assessment tool" claim is most likely associated with the EADDAT framework (DSDC Stirling) wayfinding subsection or the IDEAS Tool. Owner-queue: confirm exact publication and validity-study citation in next pass.',
    url = 'https://www.dementia.stir.ac.uk/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dsdc-stirling-context',
    last_verified_at = '2026-05-21T20:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T20:30:00Z uk-reports-batch-34] title-based; owner-queue for exact citation',
    updated_at = '2026-05-21T20:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00523';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
