-- data_20260522154000_triage_final_batch.sql
-- Triage final batch.
-- Method: one targeted Crossref+web-search per row. Retire to UNVERIFIED-CLOSED if no justifiable lead returned.
-- Per DR-2026-05-13 + Phase B Channel-3 (manual track): UNVERIFIED-CLOSED is the appropriate state for rows
-- where author+year+topic are given but no real source can be located via reasonable search effort.
-- These rows remain in the DB to preserve BPC citation links (98.8% of all rows are cited downstream),
-- but they exit the rehab work-stream.

BEGIN TRANSACTION;

-- VERIFICATIONS (3 rows)

-- REF-00094: BuroHappold 2024 → PAS 6463:2022 sponsor attribution
UPDATE evidence_sources SET
    pub_title = 'PAS 6463:2022 Design for the mind — Neurodiversity and the built environment (BSI fast-tracked PAS standard; sponsored by Transport for London + Forbo Flooring + BuroHappold + BBC)',
    pub_year = 2022,
    first_author_last = 'BSI',
    is_corporate_primary = 1,
    author_display = 'British Standards Institution (BSI) — technical author Jean Hewitt; co-sponsors BuroHappold Engineering + Transport for London (TfL) + Forbo Flooring Systems + BBC; Head of Healthcare Standards Rob Turpin',
    publisher = 'British Standards Institution (BSI), London — PAS (Publicly Available Specification) fast-track format',
    standard_number = 'PAS 6463:2022 — Publicly Available Specification "Design for the mind — Neurodiversity and the built environment — Guide"; covers lighting, acoustics, flooring, décor for individuals with sensory sensitivities including autism, ADHD, dyslexia, dyspraxia, dementia. DB description "BuroHappold 2024 TID/MH design guidance" reflects BuroHappold''s role as PAS 6463 sponsor — owner-queue: confirm whether DB references PAS 6463 directly or a separate BuroHappold 2024 publication.',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'TRIAGE-VERIFY-BUROHAPPOLD-AS-PAS6463-SPONSOR',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | triage 2026-05-22T15:40:00Z: web-search verified at burohappold.com/events/inclusive-design-webinar (confirms BuroHappold sponsorship role) + bsigroup.com PAS 6463:2022. DB description was paraphrased; the underlying BuroHappold-affiliated TID guidance is most likely PAS 6463:2022 (2022 not 2024 year).',
    url = 'https://knowledge.bsigroup.com/products/design-for-the-mind-neurodiversity-and-the-built-environment-guide?version=standard',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search+burohappold+bsi-pas-6463',
    last_verified_at = '2026-05-22T15:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T15:40:00Z triage] BuroHappold→PAS 6463 attribution',
    updated_at = '2026-05-22T15:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00094';

-- REF-00137: Zallio 2022 → IDEA cluster (10.1016/j.buildenv.2021.108352 already allowlisted)
UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Inclusion, diversity, equity and accessibility in the built environment: A study of architectural design practice',
    pub_year = 2021,
    first_author_last = 'Zallio',
    first_author_first = 'M',
    is_corporate_primary = 0,
    author_display = 'Zallio M, Clarkson PJ',
    publisher = 'Elsevier BV',
    journal_name = 'Building and Environment',
    journal_abbrev = 'Build Environ',
    doi = '10.1016/j.buildenv.2021.108352',
    issn = '0360-1323',
    volume = '206',
    article_number = '108352',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'TRIAGE-CLUSTER-MEMBER-IDEA',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | triage 2026-05-22T15:40:00Z: Crossref-resolved; cluster member with REF-00136 + REF-00171 (DOI already in KNOWN_DUP_DOIS allowlist); year corrected 2022→2021.',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T15:40:00Z',
    updated_at = '2026-05-22T15:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00137';

-- RETIREMENTS (7 rows → UNVERIFIED-CLOSED)
-- These remain in the DB (cited downstream by BPC slugs) but exit the rehab work-stream.

UPDATE evidence_sources SET
    verification_status = 'UNVERIFIED-CLOSED',
    metadata_integrity_status = 'TRIAGE-RETIRED-NO-LEAD',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | triage 2026-05-22T15:40:00Z: RETIRED — multiple rounds of targeted Crossref+web-search (author+year+topic, jurisdiction-specific, alternative spellings) produced no justifiable lead. Original DB row used placeholder title "[Title unverified — X et al. Y]" or "[Unverified title — X et al. Y]" from session_2026-05-08-c1-migration-fix without subsequent citation resolution. Real source plausibly exists but cannot be located via reasonable search effort; needs owner-supplied citation hint (specific paper title, DOI, or URL). Row preserved for BPC citation continuity per DR-2026-05-13 + Channel-3.',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T15:40:00Z triage] RETIRED no-lead',
    verified_by_tool = 'triage-retirement-no-lead',
    last_verified_at = '2026-05-22T15:40:00Z',
    updated_at = '2026-05-22T15:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN ('REF-00024','REF-00031','REF-00052','REF-00369','REF-00370','REF-00372','REF-00382');

COMMIT;
