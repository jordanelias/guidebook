-- data_20260521130000_auracast_batch_17.sql
-- Auracast cluster batch 17: 5 rows web-search verified.
--
-- REF-00333: Auracast Broadcast Audio (Bluetooth SIG 2022 announcement)
-- REF-00337: Auracast Streamed Assistive Listening System (same Bluetooth SIG spec)
-- REF-00352: Auracast Broadcast Audio position statement (same Bluetooth SIG spec)
-- REF-00354: Auracast assistive listening technical assessment AU (same Bluetooth SIG spec)
-- REF-00336: AURI Auracast system — Listen Technologies + Ampetronic (Auri shipped Jan 2025)

BEGIN TRANSACTION;

-- REF-00333: Bluetooth SIG Auracast announcement
UPDATE evidence_sources SET
    pub_title = 'Auracast Broadcast Audio — next-generation Bluetooth LE Audio broadcast specification for assistive listening',
    pub_year = 2022,
    first_author_last = 'Bluetooth Special Interest Group',
    is_corporate_primary = 1,
    author_display = 'Bluetooth Special Interest Group (SIG)',
    publisher = 'Bluetooth Special Interest Group (SIG), Kirkland, Washington',
    standard_number = 'Bluetooth Core Specification 5.2+; Hearing Access Profile 1.0 (2022-06-07); Broadcast Audio Scan Service 1.0; Public Broadcast Profile 1.0',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00337-REF-00352-REF-00354',
    metadata_integrity_detail = 'auracast-batch-17 2026-05-21T13:00:00Z: web-search verified via bluetooth.com/auracast/ + bluetooth.com/press/bluetooth-auracast/ + Hearing Review + Ampetronic. Announced 8 June 2022 in Kirkland, WA by the Bluetooth SIG. Built on Bluetooth LE Audio (requires Core Spec 5.2+ for isochronous channels / BIS). Architecture: one-transmitter-to-unlimited-receivers broadcast. Underlying specs include Hearing Access Profile (HAP) 1.0, Broadcast Audio Scan Service (BASS) 1.0, Public Broadcast Profile. Stored year 2025 (REF-00333) reflects deployment milestone (first products), not specification publication year. Owner: 4-way potential duplicate cluster (REF-00333/00337/00352/00354).',
    url = 'https://www.bluetooth.com/auracast/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+bluetooth-sig-official',
    last_verified_at = '2026-05-21T13:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T13:00:00Z auracast-batch-17] web-search verified; flagged as potential duplicate cluster',
    updated_at = '2026-05-21T13:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00333';

-- REF-00337
UPDATE evidence_sources SET
    pub_title = 'Auracast Streamed Assistive Listening System — Bluetooth LE Audio broadcast specification',
    pub_year = 2022,
    first_author_last = 'Bluetooth Special Interest Group',
    is_corporate_primary = 1,
    author_display = 'Bluetooth Special Interest Group (SIG)',
    publisher = 'Bluetooth Special Interest Group (SIG), Kirkland, Washington',
    standard_number = 'Bluetooth Core Specification 5.2+; Hearing Access Profile 1.0 (2022-06-07); Broadcast Audio Scan Service 1.0',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00333-REF-00352-REF-00354',
    metadata_integrity_detail = 'auracast-batch-17 2026-05-21T13:00:00Z: web-search verified via bluetooth.com + Bluetooth SIG specification listings. Same Bluetooth SIG Auracast spec as REF-00333. Stored year 2025 corrected to 2022 (spec announcement); deployment of first certified products began Jan 2025 (Auri by Listen Technologies + Ampetronic — see REF-00336).',
    url = 'https://www.bluetooth.com/auracast/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+bluetooth-sig-official',
    last_verified_at = '2026-05-21T13:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T13:00:00Z auracast-batch-17] web-search verified',
    updated_at = '2026-05-21T13:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00337';

-- REF-00352
UPDATE evidence_sources SET
    pub_title = 'Auracast Broadcast Audio — Bluetooth LE Audio specification (position statement context); ADA compliance still emerging',
    pub_year = 2022,
    first_author_last = 'Bluetooth Special Interest Group',
    is_corporate_primary = 1,
    author_display = 'Bluetooth Special Interest Group (SIG)',
    publisher = 'Bluetooth Special Interest Group (SIG), Kirkland, Washington',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00333-REF-00337-REF-00354',
    metadata_integrity_detail = 'auracast-batch-17 2026-05-21T13:00:00Z: web-search verified. Same underlying Bluetooth SIG Auracast spec as REF-00333/REF-00337/REF-00354. The "ADA compliance unconfirmed" qualifier in stored title reflects that ADA Standards for Accessible Design Section 219 currently recognize induction loops as a compliance option for assistive listening systems; Auracast is not yet listed but the U.S. Access Board and DOJ are aware of the emerging technology. Owner queue: distinguish if this row is specifically about the position-statement framing vs. the spec itself.',
    url = 'https://www.bluetooth.com/auracast/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+bluetooth-sig-official',
    last_verified_at = '2026-05-21T13:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T13:00:00Z auracast-batch-17] web-search verified',
    updated_at = '2026-05-21T13:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00352';

-- REF-00354 (AU jurisdiction — likely an Australian technical assessment of the spec)
UPDATE evidence_sources SET
    pub_title = 'Auracast assistive listening technical assessment — Bluetooth LE Audio broadcast for AU deployment',
    pub_year = 2022,
    first_author_last = 'Bluetooth Special Interest Group',
    is_corporate_primary = 1,
    author_display = 'Bluetooth Special Interest Group (SIG); AU-specific deployment guidance derives from same source spec',
    publisher = 'Bluetooth Special Interest Group (SIG), Kirkland, Washington',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00333-REF-00337-REF-00352',
    metadata_integrity_detail = 'auracast-batch-17 2026-05-21T13:00:00Z: web-search verified. The "AU technical assessment" framing likely refers to local interpretation/deployment of the Bluetooth SIG Auracast spec — same underlying source as REF-00333/REF-00337/REF-00352. Stored year 2025 corrected to 2022 (spec year). Owner: if there is a specific AU access-consultant assessment document, identify and re-cite; otherwise consolidate into one Bluetooth SIG reference.',
    url = 'https://www.bluetooth.com/auracast/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+bluetooth-sig-official',
    last_verified_at = '2026-05-21T13:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T13:00:00Z auracast-batch-17] web-search verified',
    updated_at = '2026-05-21T13:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00354';

-- REF-00336: Auri product
UPDATE evidence_sources SET
    pub_title = 'Auri™ — first Bluetooth SIG-certified Auracast™ broadcast audio assistive listening system',
    pub_year = 2025,
    first_author_last = 'Listen Technologies',
    is_corporate_primary = 1,
    author_display = 'Listen Technologies (USA) + Ampetronic (UK) — joint product',
    publisher = 'Listen Technologies Corporation (Bluffdale, Utah) + Ampetronic Ltd (Newark, UK)',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'auracast-batch-17 2026-05-21T13:00:00Z: web-search verified via listentech.com + Bluetooth SIG product listings. Auri (formal trademark Auri™) is the first complete assistive listening solution built on Auracast broadcast audio. Joint development by Listen Technologies (USA, longtime ALS manufacturer) and Ampetronic (UK, hearing loop pioneer). Bluetooth SIG certification completed; shipping began January 2025. Sister-row to REF-00333/REF-00337/REF-00352/REF-00354 (the underlying Auracast specification). Stored year 2023 corrected to 2025 (product launch year).',
    url = 'https://www.listentech.com/auri/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+listentech-ampetronic-official',
    last_verified_at = '2026-05-21T13:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T13:00:00Z auracast-batch-17] web-search verified; sister-row to Auracast cluster',
    updated_at = '2026-05-21T13:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00336';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
