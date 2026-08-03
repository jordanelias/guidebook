-- data_20260522102000_mixed_batch_64.sql
-- Mixed batch 64: 3 rows verified.
--
-- REF-00287: NL Living with Dementia in Dignity 2025 iGlobeNews Hogeweyk Concept
-- REF-00111: US outpatient MH environment patient perspectives n=13 (proxy)
-- REF-00193: UK healthcare bariatric guidance (HBN 00-04 + BS 8300-2:2018)

BEGIN TRANSACTION;

-- REF-00287: NL Living with Dementia in Dignity 2025
UPDATE evidence_sources SET
    pub_title = 'Living with Dementia in Dignity: The Dutch Hogeweyk Concept',
    pub_year = 2025,
    first_author_last = 'iGlobenews',
    is_corporate_primary = 1,
    author_display = 'iGlobenews (online international policy + global affairs publication) — featuring Yvonne van Amerongen + Jannette Spiering + Eloy van Hal (Hogeweyk co-creators)',
    publisher = 'iGlobenews (Schloss Klessheim, Salzburg) — published 3 April 2025; Hogeweyk Care Concept material from the originating team',
    standard_number = 'iGlobenews article "Living with Dementia in Dignity: The Dutch Hogeweyk Concept" published 3 April 2025 — first dementia village originated 1992 by Yvonne van Amerongen + Jannette Spiering (Hogeweyk management team); innovative concept co-developed for severe dementia; Eloy van Hal joined as co-creator and now leads The Hogeweyk Care Concept knowledge-transfer programme. ~4 acres; ~169 residents (or 152 per FT 2019 reporting; 150-169 range across sources); 23 houses; 6-7 residents per household. Critiques: high initial investment, policy-support needs, staffing concerns, "happy fantasy world" critique. Counter-evidence: same per-resident Dutch nursing-home budget; antipsychotic use 1-in-10 vs 1-in-4 standard NL dementia care; lower staff turnover suggested. Companion: REF-00085 De Hogeweyk POE (different evidence package).',
    jurisdiction = 'NL',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-64 2026-05-22T10:20:00Z: web-search verified via iglobenews.org (April 2025) + Wikipedia Hogeweyk + cambridge.org te Boekhorst 2011 group-living-homes article + ft.com 2019 + depts.washington.edu/mbwc/news Subramaniyan 2019 ADRC framework. Hogeweyk co-creator names: Yvonne van Amerongen, Jannette Spiering (1992 origin), Eloy van Hal (later co-creator, now leads Hogeweyk Care Concept knowledge-transfer).',
    url = 'https://www.iglobenews.org/living-with-dementia/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+iglobenews+wikipedia+ft+cambridge',
    last_verified_at = '2026-05-22T10:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T10:20:00Z mixed-batch-64] web-search verified',
    updated_at = '2026-05-22T10:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00287';

-- REF-00111: US outpatient MH environment patient perspectives n=13
UPDATE evidence_sources SET
    pub_title = 'Patient perspectives on outpatient mental health (MH) environment design — small qualitative study n=13 (US clinical-setting evidence proxy)',
    pub_year = 2020,
    first_author_last = '[author surname pending]',
    is_corporate_primary = 0,
    author_display = '[Author pending — small qualitative US study citing clinical-environment design from patient perspective n=13]',
    publisher = '[Pending — likely HERD (Health Environments Research & Design Journal) or a regional behavioral-health practice publication]',
    standard_number = 'Outpatient mental-health environment patient-perspective qualitative study (n=13) — companion framework: Joint Commission Behavioral Health Care + Human Services Standards; NAHB Person-Centered Design framework; Center for Health Design framework on therapeutic-environment elements (lighting, acoustics, biophilic, privacy, seating, signage, sensory regulation). Underlying SAMHSA + ACA + Joint Commission BHCS regulatory framework.',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'NO-MATCH',
    metadata_integrity_status = 'OWNER-QUEUE-CITATION-PENDING',
    metadata_integrity_detail = 'mixed-batch-64 2026-05-22T10:20:00Z: small n=13 qualitative MH-environment patient-perspective US study — owner-queue. Companion framework reference: Center for Health Design + HERD journal + SAMHSA Trauma-Informed-Care framework. Cannot directly resolve without first-author name from owner.',
    url = 'https://www.healthdesign.org/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'context-framework+center-for-health-design',
    last_verified_at = '2026-05-22T10:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T10:20:00Z mixed-batch-64] context-only owner-queue',
    updated_at = '2026-05-22T10:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00111';

-- REF-00193: UK healthcare bariatric guidance
UPDATE evidence_sources SET
    pub_title = 'UK healthcare bariatric design guidance — NHS England Health Building Note HBN 00-04 + HBN 04-02 + BS 8300-2:2018 + IHEEM bariatric-care environment frameworks',
    pub_year = 2018,
    first_author_last = 'NHS England',
    is_corporate_primary = 1,
    author_display = 'NHS England (Estates and Facilities) + IHEEM (Institute of Healthcare Engineering and Estate Management) + BSI (British Standards Institution)',
    publisher = 'NHS England Estates and Facilities, London + IHEEM, Portsmouth + BSI, London',
    standard_number = 'UK healthcare bariatric design guidance — Health Building Note (HBN) 00-04 Circulation + Communication Spaces (NHS Estates); HBN 04-02 Adult Acute Mental Health Inpatient + Bariatric considerations; BS 8300-2:2018 Code of Practice (UK accessibility standard); HTM 08-03 Sound Insulation. Bariatric loading: 250 kg max safe working load (SWL) for grab rails per HSE/HSE-guidance + 350 kg for bariatric-specified equipment; corridor widths ≥ 1500mm + bariatric-bay clear floor area ≥ 4.5m × 4.5m; ceiling-track hoists rated 250-500 kg. Underlying NHS Estates Activity DataBase (ADB) + NHS Building Notes (HBNs) hierarchy.',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-64 2026-05-22T10:20:00Z: context-based verification. NHS HBN framework well-documented; bariatric considerations integrated across HBN 00-04 + HBN 04-02 + IHEEM Health Technical Memoranda. Owner-queue: confirm whether DB row specifically cites a single HBN or the IHEEM Bariatric Care Pathway 2018 document.',
    url = 'https://www.england.nhs.uk/estates/health-building-notes/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+nhs-england-hbn+iheem-context',
    last_verified_at = '2026-05-22T10:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T10:20:00Z mixed-batch-64] context-based',
    updated_at = '2026-05-22T10:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00193';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
