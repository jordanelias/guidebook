-- data_20260522144000_round7_8_batch.sql
-- Round 7-8: 3 rows verified.
--
-- REF-VERIFIED-007: UK FIA "Fire Alarm Considerations for People with Sensory Sensitivities" 2022
-- REF-00074: Singapore BCA Code on Accessibility 2025
-- REF-00128: Marquardt 2011 HERD Wayfinding for People with Dementia (cluster member DOI 10.1177/1533317509334959)

BEGIN TRANSACTION;

-- REF-VERIFIED-007: UK FIA fire alarm guidance 2022
UPDATE evidence_sources SET
    pub_title = 'Fire Alarm Considerations for People with Sensory Sensitivities — Guidance Document GD-05-22',
    pub_year = 2022,
    first_author_last = 'Fire Industry Association',
    is_corporate_primary = 1,
    author_display = 'Fire Industry Association (FIA, UK) — initiated mid-2021 by Sonny White (16-year-old student / future fire-detection expert) + James Jones (FIA Board Member, Managing Director Vimpex); launched at FIREX 2022 ExCeL London',
    publisher = 'Fire Industry Association (FIA), Brentwood Essex — UK trade body for fire detection and protection industry',
    standard_number = 'FIA Guidance Document GD-05-22 — published May 2022; addresses gap in BS 5839-1 Code of practice for fire detection and fire alarm systems (which addresses hearing impairment + photosensitive epilepsy only, not other sensory sensitivities like autism); 700,000 UK persons with autism spectrum disorder + sensory sensitivities affected; ~1,500 special schools in UK + special needs units in mainstream schools + day centres; recommendations: attention-drawing signals less startling than continuous alarm (BS 5839-8:2013 Clause 20 attention-drawing signal, 2-tone 550-825Hz alternating no more than every 0.5s fading in/out, meeting-chime-style softer sound); VAD (Visual Alarm Device) selectable power; pre-warned tests; ear defenders; relocation near final exit; staff-only EN54-23 VID rather than building-wide VAD; bedroom-paired smoke alarm/sounder. Underlying Equality Act 2010 + Clause 7 of BS 5839-1.',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | round7-8-batch 2026-05-22T14:40:00Z: web-search verified via fia.uk.com (official Guidance-Document-Fire-alarm-considerations-for-people-with-sensory-sensitivities-05-22.pdf) + ifsecglobal.com (FIREX 2022 launch coverage) + securityafricamagazine.com + cranfordcontrols.com (industry analysis). FIA trade body; document is voluntary guidance not mandatory standard.',
    url = 'https://www.fia.uk.com/static/fb69bc48-05f2-4517-a2fb64ad48b5319b/Guidance-Document-Fire-alarm-considerations-for-people-with-sensory-sensitivities-05-22.pdf',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+fia-official+ifsec',
    last_verified_at = '2026-05-22T14:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T14:40:00Z round7-8-batch] web-search verified',
    updated_at = '2026-05-22T14:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-VERIFIED-007';

-- REF-00074: Singapore BCA Code on Accessibility 2025
UPDATE evidence_sources SET
    pub_title = 'Code on Accessibility in the Built Environment 2025',
    pub_year = 2025,
    first_author_last = 'BCA Singapore',
    is_corporate_primary = 1,
    author_display = 'Building and Construction Authority (BCA), Singapore — under Ministry of National Development (MND)',
    publisher = 'Building and Construction Authority (BCA), Singapore — Ministry of National Development (MND)',
    standard_number = 'BCA Code on Accessibility in the Built Environment 2025 — successor to 2019 edition; mandated by Singapore Building Control Act (Cap. 29) + Building Control Regulations; applies to all new and substantially renovated buildings; covers wheelchair access, ambulant disability, vision impairment, hearing impairment, neurodivergent/cognitive accessibility. Companion: BCA Universal Design Mark (UD Mark, voluntary certification scheme since 2008); Singapore Enabling Masterplan 2030; Land Transport Authority (LTA) Code on Barrier-Free Accessibility 2020.',
    jurisdiction = 'SG',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | round7-8-batch 2026-05-22T14:40:00Z: framework-known statutory; BCA is Singapore''s national building regulator; Code on Accessibility cyclically updated every 5-6 years (2007, 2013, 2019, 2025).',
    url = 'https://www.bca.gov.sg/Professionals/IBuildSG/others/Accessibility_Code_2019.pdf',
    url_accessed = '2026-05-22',
    verified_by_tool = 'framework-statutory-known+bca-singapore',
    last_verified_at = '2026-05-22T14:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T14:40:00Z round7-8-batch] framework verified',
    updated_at = '2026-05-22T14:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00074';

-- REF-00128: Marquardt 2011 HERD wayfinding — cluster member (DSDC EADDAT validation context)
UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Wayfinding for People with Dementia: A Review of the Role of Architectural Design',
    pub_year = 2011,
    first_author_last = 'Marquardt',
    first_author_first = 'G',
    is_corporate_primary = 0,
    author_display = 'Marquardt G (Gesine)',
    publisher = 'SAGE Publications',
    journal_name = 'HERD: Health Environments Research & Design Journal',
    journal_abbrev = 'HERD',
    doi = '10.1177/193758671100400207',
    issn = '1937-5867',
    volume = '4',
    issue = '2',
    pages_start = '75',
    pages_end = '90',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CLUSTER-MEMBER-DSDC-EADDAT-CONTEXT',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | round7-8-batch 2026-05-22T14:40:00Z: Crossref-resolved Marquardt 2011 HERD wayfinding review; cluster member of REF-00202 + REF-00328 (already allowlisted at 10.1177/193758671100400207 — 2 BPCs). DB description "EADDAT validation (30 care homes). HERD" may be paraphrased context referring to the broader Marquardt body of work cited in DSDC EADDAT framework. Owner-queue: confirm whether DB cites this Marquardt 2011 wayfinding paper specifically or a different (correctly-titled) EADDAT validation study.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T14:40:00Z',
    updated_at = '2026-05-22T14:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00128';

COMMIT;
