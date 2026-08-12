-- data_20260521050000_uk_guidelines_batch_2.sql
--
-- UK guidelines no-identifier cohort web-search verification batch 2.
-- Per DR-2026-05-18 statutory-metadata-completeness gray-lit / regulatory protocol.
--
-- REF-00084: EADDAT (DSDC University of Stirling, 2022)
-- REF-00201: EADDAT 2024 (same source as REF-00084; flagged duplicate)
-- REF-00281: Click-Away Pound Report 2019 (Williams & Brownlow, Freeney Williams, Feb 2020)
-- REF-00280: Purple Pound 2020 (DWP / We Are Purple)
-- REF-00022: Building Sight (RNIB, 2023 update by Lewis & Thomas)

BEGIN TRANSACTION;

-- REF-00084: EADDAT 2022
UPDATE evidence_sources SET
    pub_title = 'Environments for Ageing and Dementia Design Assessment Tool (EADDAT)',
    pub_year = 2022,
    first_author_last = 'Palmer',
    first_author_first = 'Lesley',
    is_corporate_primary = 0,
    author_display = 'Palmer, L. (Chief Architect, Dementia Services Development Centre, University of Stirling); DSDC team',
    publisher = 'Dementia Services Development Centre (DSDC), University of Stirling',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-2 2026-05-21T05:00:00Z: web-search verified via dementia.stir.ac.uk + Inside Ageing + Care Management Matters. EADDAT replaces DSDC 2008 Dementia Design Audit Tool. Trialed by Transport for London and Kirklees Council 2022. Three tiers: Tier 1 Aware (foundations), Tier 2 Supportive (7 sub-resources R1-R7), Tier 3.',
    url = 'https://shop.dementia.stir.ac.uk/collections/eaddat',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dsdc-official',
    last_verified_at = '2026-05-21T05:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T05:00:00Z uk-guidelines-batch-2] web-search verified',
    updated_at = '2026-05-21T05:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00084';

-- REF-00201: EADDAT 2024 — same source as REF-00084, possibly Tier 2 specific
UPDATE evidence_sources SET
    pub_title = 'Environments for Ageing and Dementia Design Assessment Tool (EADDAT)',
    pub_year = 2022,
    first_author_last = 'Palmer',
    first_author_first = 'Lesley',
    is_corporate_primary = 0,
    author_display = 'Palmer, L. (Chief Architect, Dementia Services Development Centre, University of Stirling); DSDC team',
    publisher = 'Dementia Services Development Centre (DSDC), University of Stirling',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00084',
    metadata_integrity_detail = 'uk-guidelines-batch-2 2026-05-21T05:00:00Z: same source as REF-00084 (EADDAT, DSDC University of Stirling). Stored year 2024 corrected to 2022 (canonical release year per DSDC announcement Sept 2022). Owner: merge into REF-00084 or keep if citing specific Tier 2 / R2-R7 component.',
    url = 'https://shop.dementia.stir.ac.uk/collections/eaddat',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dsdc-official',
    last_verified_at = '2026-05-21T05:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T05:00:00Z uk-guidelines-batch-2] web-search verified; potential duplicate of REF-00084',
    updated_at = '2026-05-21T05:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00201';

-- REF-00281: Click-Away Pound Report 2019
-- Note: stored £11.75B figure is from 2016 survey; 2019 report figure was £17.1B.
-- Year 2019 refers to survey period; publication date Feb 2020.
UPDATE evidence_sources SET
    pub_title = 'The Click-Away Pound Report 2019: Revisiting the online shopping experience of customers with disabilities, and the cost to business of ignoring them',
    pub_year = 2019,
    first_author_last = 'Williams',
    first_author_first = 'Rick',
    is_corporate_primary = 0,
    author_display = 'Williams, R.; Brownlow, S.',
    author_count = 2,
    author_count_is_complete = 1,
    publisher = 'Freeney Williams Ltd (disability and diversity consultancy)',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-2 2026-05-21T05:00:00Z: web-search verified via clickawaypound.com + parliamentary report + Recite Me. Survey 2019, report published Feb 2020. Stored "£11.75B" figure is from the prior 2016 survey iteration; the 2019 click-away total was £17.1B per Williams & Brownlow.',
    url = 'https://www.clickawaypound.com/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+clickawaypound-official',
    last_verified_at = '2026-05-21T05:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T05:00:00Z uk-guidelines-batch-2] web-search verified',
    updated_at = '2026-05-21T05:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00281';

-- REF-00280: Purple Pound 2020 (£274B figure)
UPDATE evidence_sources SET
    pub_title = 'The Purple Pound — spending power of disabled people and their households (UK 2020 estimate £274 billion)',
    pub_year = 2020,
    first_author_last = 'Purple',
    is_corporate_primary = 1,
    author_display = 'Purple (We Are Purple charity); underlying research by Department for Work and Pensions (DWP)',
    publisher = 'Purple / We Are Purple',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-2 2026-05-21T05:00:00Z: aggregator infographic citing DWP Family Resources Survey + Disability Benefits Consortium data. £274B figure widely cited across UK accessibility literature 2020 onwards. Underlying primary source is DWP statistical release, not Purple itself.',
    url = 'https://wearepurple.org.uk/the-purple-pound-infographic/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+purple-official',
    last_verified_at = '2026-05-21T05:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T05:00:00Z uk-guidelines-batch-2] web-search verified',
    updated_at = '2026-05-21T05:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00280';

-- REF-00022: Building Sight (RNIB, 2023 update)
UPDATE evidence_sources SET
    pub_title = 'Building Sight: Design principles and practical recommendations',
    pub_year = 2023,
    first_author_last = 'Lewis',
    first_author_first = 'Caroline',
    is_corporate_primary = 0,
    author_display = 'Lewis, C.; Thomas, C. (Access Design Solutions UK) — 2023 update of Barker, P.; Barrick, J.; Wilson, R. 1995 original',
    publisher = 'Royal National Institute of Blind People (RNIB) — original HMSO 1995',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-2 2026-05-21T05:00:00Z: web-search verified via media.rnib.org.uk + N. Somerset Access Officer archive. First published 1995 by Peter Barker, Jon Barrick, Rod Wilson (HMSO/RNIB). Updated 2023 by Caroline Lewis and Carol Thomas (Access Design Solutions UK).',
    url = 'https://media.rnib.org.uk/documents/Building_Sight_2023.pdf',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+rnib-official',
    last_verified_at = '2026-05-21T05:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T05:00:00Z uk-guidelines-batch-2] web-search verified',
    updated_at = '2026-05-21T05:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00022';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
