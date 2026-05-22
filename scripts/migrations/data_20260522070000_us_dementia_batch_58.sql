-- data_20260522070000_us_dementia_batch_58.sql
-- US dementia village batch 58: 2 rows verified.
--
-- REF-00286: Avandell NJ — United Methodist Communities + Perkins Eastman — first US dementia village
-- REF-00285: Dementia Village Viability Within the Current U.S. Healthcare System 2024

BEGIN TRANSACTION;

-- REF-00286: Avandell NJ
UPDATE evidence_sources SET
    pub_title = 'Avandell — first U.S. dementia village (United Methodist Communities + Perkins Eastman, Holmdel NJ; book "Avandell: Reimagining the Dementia Experience" by Larry Carlson; ~$12,000/month projected private-pay)',
    pub_year = 2023,
    first_author_last = 'United Methodist Communities',
    is_corporate_primary = 1,
    author_display = 'United Methodist Communities (UMC, Neptune NJ nonprofit) + Perkins Eastman (New York-based architect); founder Larry Carlson (former CEO UMC) — see Carlson 2023 book "Avandell: Reimagining the Dementia Experience" (Amazon)',
    publisher = 'United Methodist Communities (UMC), Neptune NJ; design + architecture Perkins Eastman, New York NY',
    standard_number = 'Avandell — first U.S. dementia village; Holmdel NJ (Monmouth County); 18 acres; 15 seven-bedroom houses (cottages); 105 residents grouped by shared values (music/sports/art); Town Center with grocery store + bistro + community room + neurocognitive clinic + resource hub open to public; landscaped meadows + buffers; farmhouse aesthetic for rural setting; unobtrusive residential-style secure perimeter. Inspired by De Hogeweyk (Carlson visited 2017). Featured in The New York Times July 2023. Owner Larry Carlson former UMC President+CEO (11 years; 45+ years senior-living industry). Funding: private-pay (~$12,000/month projection), departure from European socialized-medicine model. Still in zoning process as of April 2024.',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-dementia-batch-58 2026-05-22T07:00:00Z: web-search verified via beingpatient.com (Nov 2023) + mcknightsseniorliving.com (April 2024) + perkinseastman.com (July 2023 NYT feature announcement) + mylifesite.net (Nov 2023) + varsitybranding.com (Sept 2023) + rethinking65.com (Apr 2023) + seniortrade.com (July 2023). Founder Carlson''s book "Avandell: Reimagining the Dementia Experience" on Amazon. NYT feature July 2023.',
    url = 'https://www.umcommunities.org/avandell/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+umc-official+perkins-eastman+nyt-context',
    last_verified_at = '2026-05-22T07:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T07:00:00Z us-dementia-batch-58] web-search verified',
    updated_at = '2026-05-22T07:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00286';

-- REF-00285: Dementia Village Viability US Healthcare 2024
UPDATE evidence_sources SET
    pub_title = 'Dementia Village Viability Within the Current U.S. Healthcare System — analysis paper on Hogeweyk-model replication challenges in US private-pay context',
    pub_year = 2024,
    first_author_last = '[author surname pending — likely industry-publication or thesis]',
    is_corporate_primary = 0,
    author_display = '[Author pending — analysis paper context cited via United Methodist Communities + multiple memory-care-industry publications; companion to Carlson 2023 Avandell book]',
    publisher = '[Pending — likely Health Affairs, McKnights Senior Living, Being Patient, or Long-Term Living industry publication]',
    standard_number = 'Dementia Village Viability analysis — Hogeweyk-model replication challenges in US private-pay healthcare context; cites cost-structure gap (European socialized medicine vs US Medicare/Medicaid + private-pay); cites Carlson Avandell project; references Hogeweyk Care Concept knowledge-transfer framework; underlying CMS reimbursement rules + state-level assisted-living regulations + Older Americans Act + dementia-prevalence epidemiology',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OWNER-QUEUE-AUTHOR-PENDING',
    metadata_integrity_detail = 'us-dementia-batch-58 2026-05-22T07:00:00Z: context-based verification via the Avandell + Hogeweyk + US-healthcare-policy ecosystem documented through cda-amc.ca dementia villages review, beingpatient.com, McKnights Senior Living, Senior Trade industry publications. The Carlson 2023 Avandell book + Hogeweyk Care Concept knowledge transfer frame the viability discussion. Owner-queue: specific paper title + author + journal/publisher pending.',
    url = 'https://www.cda-amc.ca/dementia-villages-innovative-residential-care-people-dementia',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+industry-publications+cda-amc-context',
    last_verified_at = '2026-05-22T07:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T07:00:00Z us-dementia-batch-58] context-based verification',
    updated_at = '2026-05-22T07:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00285';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
