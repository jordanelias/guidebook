-- data_20260521193000_int_guidelines_batch_32.sql
-- INT guidelines batch 32: 5 rows verified.
--
-- REF-00226: WELL v2 Thermal Comfort feature
-- REF-00555: WELL v2/v6 Feature L07 (Light)
-- REF-00598: WELL v2 Feature 54
-- REF-00618: WELL v2 Air Quality feature
-- REF-00039: Deafblind International Guidelines on Best Practice

BEGIN TRANSACTION;

-- REF-00226: WELL v2 Thermal Comfort
UPDATE evidence_sources SET
    pub_title = 'WELL Building Standard v2 — Thermal Comfort concept (T features T01-T07: Thermal Performance, Enhanced Thermal Performance, Thermal Zoning, Individual Thermal Control, Radiant Thermal Comfort, Thermal Comfort Monitoring, Humidity Control)',
    pub_year = 2024,
    first_author_last = 'International WELL Building Institute',
    is_corporate_primary = 1,
    author_display = 'International WELL Building Institute (IWBI), New York; administered by Green Business Certification Inc. (GBCI)',
    publisher = 'International WELL Building Institute (IWBI), New York',
    standard_number = 'WELL Building Standard v2 (originally launched 2018; continuously updated; v1 launched 2014); 10 concepts: Air, Water, Nourishment, Light, Movement, Thermal Comfort, Sound, Materials, Mind, Community; certification valid 3 years with annual reporting',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-CLUSTER-WITH-REF-00555-00598-00618',
    metadata_integrity_detail = 'int-guidelines-batch-32 2026-05-21T19:30:00Z: web-search verified via wellcertified.com / IWBI official + atmocube.com (Atmotube blog) + envira.global + bluescopebuildings.com + aircare.it + aethair.io + cim.io + envigilance.com + LinkedIn. As of mid-2025: 6B+ sqft real estate across 100,000 locations in 137 countries engaged with WELL. Maximum 110 points; Bronze ≥40, Silver ≥50, Gold ≥60, Platinum ≥80. Performance-based verification by approved WELL Performance Testing Agents. Thermal Comfort concept: T01 Thermal Performance (precondition); T02-T05 Enhanced/Zoning/Individual/Radiant optimizations; T06 Thermal Comfort Monitoring; T07 Humidity Control.',
    url = 'https://standard.wellcertified.com/thermal-comfort',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+iwbi-official',
    last_verified_at = '2026-05-21T19:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T19:30:00Z int-guidelines-batch-32] web-search verified',
    updated_at = '2026-05-21T19:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00226';

-- REF-00555: WELL v2/v6 Feature L07
UPDATE evidence_sources SET
    pub_title = 'WELL Building Standard v2 + v6 — Light concept Feature L07 (Visual Acuity for Focus / Right-to-Light enhancements)',
    pub_year = 2024,
    first_author_last = 'International WELL Building Institute',
    is_corporate_primary = 1,
    author_display = 'International WELL Building Institute (IWBI), New York',
    publisher = 'International WELL Building Institute (IWBI), New York',
    standard_number = 'WELL v2/v6 Light concept (L01-L08+): L01 Light Exposure & Education, L02 Visual Lighting Design, L03 Circadian Lighting Design, L04 Electric Light Quality, L05 Daylight Design Strategies, L06 Daylight Simulation, L07 Visual Acuity, L08 Occupant Control of Lighting',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-CLUSTER-WITH-REF-00226-00598-00618',
    metadata_integrity_detail = 'int-guidelines-batch-32 2026-05-21T19:30:00Z: web-search verified via wellcertified.com / IWBI official + bluescopebuildings.com (Features L01-05, L07, L08) + atmotube + Aethair. Light concept includes circadian lighting requirements (melanopic ratio thresholds), daylight simulation (sDA, ASE), visual acuity thresholds, glare control.',
    url = 'https://standard.wellcertified.com/light',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+iwbi-official',
    last_verified_at = '2026-05-21T19:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T19:30:00Z int-guidelines-batch-32] web-search verified',
    updated_at = '2026-05-21T19:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00555';

-- REF-00598: WELL v2 Feature 54 (legacy numbering)
UPDATE evidence_sources SET
    pub_title = 'WELL Building Standard v1/v2 — Feature 54 (Circadian Lighting Design; v1 legacy numbering maps to v2 L03 Circadian Lighting Design)',
    pub_year = 2024,
    first_author_last = 'International WELL Building Institute',
    is_corporate_primary = 1,
    author_display = 'International WELL Building Institute (IWBI), New York',
    publisher = 'International WELL Building Institute (IWBI), New York',
    standard_number = 'WELL v1 Feature 54 = WELL v2 L03 Circadian Lighting Design; equivalent UL DG 24480 / WELL melanopic lux requirements (~200 EML at desktop)',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-CLUSTER-WITH-REF-00226-00555-00618',
    metadata_integrity_detail = 'int-guidelines-batch-32 2026-05-21T19:30:00Z: web-search verified. v1 used numerical features (Feature 54 = Circadian Lighting Design); v2 reorganised into Concept+Feature codes (L03). Stored title "Feature 54" reflects v1 framing — confirmed equivalent to v2 L03.',
    url = 'https://standard.wellcertified.com/light',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+iwbi-official',
    last_verified_at = '2026-05-21T19:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T19:30:00Z int-guidelines-batch-32] web-search verified',
    updated_at = '2026-05-21T19:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00598';

-- REF-00618: WELL v2 Air Quality
UPDATE evidence_sources SET
    pub_title = 'WELL Building Standard v2 — Air concept (A features A01-A14: A01 Air Quality, A02 Smoke-Free Environment, A03 Ventilation Effectiveness, A04 Construction Pollution Management preconditions; A05-A14 optimizations including A08 Air Quality Monitoring & Awareness)',
    pub_year = 2024,
    first_author_last = 'International WELL Building Institute',
    is_corporate_primary = 1,
    author_display = 'International WELL Building Institute (IWBI), New York',
    publisher = 'International WELL Building Institute (IWBI), New York',
    standard_number = 'WELL v2 Air concept: A01-A04 preconditions, A05-A14 optimizations; PM2.5 and PM10 thresholds; A08 IAQ continuous monitoring & awareness',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-CLUSTER-WITH-REF-00226-00555-00598',
    metadata_integrity_detail = 'int-guidelines-batch-32 2026-05-21T19:30:00Z: web-search verified via aethair.io + atmotube.com + envira.global. Air concept: 4 preconditions (A01-A04) and 10 optimizations (A05-A14). Strict PM2.5/PM10 thresholds; A08 Air Quality Monitoring & Awareness specifically requires continuous IAQ tracking. Performance-based, on-site testing by approved Performance Testing Agents at certification time and annual reporting.',
    url = 'https://standard.wellcertified.com/air',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+iwbi-official',
    last_verified_at = '2026-05-21T19:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T19:30:00Z int-guidelines-batch-32] web-search verified',
    updated_at = '2026-05-21T19:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00618';

-- REF-00039: Deafblind International Best Practice Service Provision
UPDATE evidence_sources SET
    pub_title = 'Guidelines on Best Practice for Service Provision to Deafblind People',
    pub_year = 2020,
    first_author_last = 'Deafblind International',
    is_corporate_primary = 1,
    author_display = 'Deafblind International (DbI) — global network on services for people with deafblindness',
    publisher = 'Deafblind International (DbI)',
    standard_number = 'DbI Best Practice Guidelines; companion CBM 2022 guidelines developed with WFDB, DbI, Perkins International, Sense International, Royal Dutch Visio',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'int-guidelines-batch-32 2026-05-21T19:30:00Z: web-search verified via deafblindinternational.org (official) + cbm.org/dam (Best Practice Guidelines on Working with People Living with Deafblindness) + sense.org.uk + senseinternational.org.uk + Special Needs Jungle. Environmental modification recommendations: good lighting + reduced background noise (residual senses), contrasting colours, tactile floor information, clear/tactile signage, induction loops in receptions/public meeting rooms. Notes barriers in public buildings: glass, mirrored, chrome surfaces, marble — hard to perceive. Key partners: World Federation of the Deafblind (WFDB), Sense (UK national), Sense International, Perkins International, Royal Dutch Visio.',
    url = 'https://www.deafblindinternational.org/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dbi-official+cbm',
    last_verified_at = '2026-05-21T19:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T19:30:00Z int-guidelines-batch-32] web-search verified',
    updated_at = '2026-05-21T19:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00039';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
