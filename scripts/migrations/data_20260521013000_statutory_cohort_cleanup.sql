-- data_20260521013000_statutory_cohort_cleanup.sql
--
-- Three-part statutory-cohort cleanup from full-DB verification audit.
--
-- A) DIN/EN/IEC promotion to COMPLETE-STATUTORY (14 rows). Per DR-2026-05-18.
--    Standards are real, documented, stored metadata matches reality (verified
--    via web search of DIN 18040 series, EN 17210:2021, IEC 60118-4:2014+AMD1).
--    Simultaneously fixes Drift 3: the 10 overlapping rows had been promoted to
--    COMPLETE-STATUTORY by migration 20260518050000 in history, but the committed
--    DB never received the promotion (a non-runner write demoted them sideways to
--    plain COMPLETE).
--
-- B) ASD-tagged academic recategorization (8 rows). standard_number='ASD' is a
--    topic tag, not a standards identifier. source_type='standard' incorrectly
--    routes them to the statutory verification track. Fix: source_type='report',
--    clear standard_number, populate metadata_integrity_detail explaining.
--
-- C) Wrong-DOI Mostafa-ASPECTSS cleanup (4 rows). Four rows share DOI
--    10.3389/fpsyt.2021.727353 which returns 404 at Crossref. Mostafa 2021 reference
--    is to the DCU 'Autism Friendly University Design Guide' (issuu) — NOT a
--    Frontiers Psychiatry paper. Wrong-DOI attachment; clear DOIs, flag as
--    potential-multi-citation-duplicates for owner merge decision.
--
BEGIN TRANSACTION;

-- =============================================================
-- Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY (fixes Drift 3)
-- =============================================================

-- REF-00018: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: DIN 32984:2011-10 — Bodenindikatoren im öffentlichen Raum (tactile ground indicators), confirmed via DIN catalog entries. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00018';

-- REF-00121: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: EN 17210:2021 — European standard ''Accessibility and usability of the built environment'', confirmed via BIH (Bundesarbeitsgemeinschaft der Integrationsämter). Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00121';

-- REF-00144: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: DIN 18040-2:2011-09 — Barrierefreies Bauen Teil 2: Wohnungen (dwellings), confirmed via baunormenlexikon.de + nullbarriere.de. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00144';

-- REF-00200: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: IEC 60118-4:2014+AMD1:2017 — Electroacoustics - Hearing aids - Part 4: Induction-loop systems for hearing aid purposes - System performance requirements (well-documented IEC standard). Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00200';

-- REF-00207: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: DIN 18040-2:2011 §5 Bedienungshöhen (operating heights) — section reference within confirmed standard. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00207';

-- REF-00323: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: DIN 18040-2:2011-09 — Barrierefreies Bauen Wohnungen, confirmed. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00323';

-- REF-00328: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: IEC 60118-4:2014+AMD1:2017 — Induction-loop systems performance requirements, confirmed. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00328';

-- REF-00329: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: DIN 18041:2016-03 — Hörsamkeit in Räumen (acoustic quality in rooms), well-known German acoustics standard, confirmed. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00329';

-- REF-00348: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: IEC 60118-4:2014+AMD1:2017 — Hearing aids Part 4, confirmed. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00348';

-- REF-00351: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: DIN 18040-1:2010 §5.2.2 — Induktionsschleife / Zwei-Sinne-Prinzip (two-senses principle) section reference within confirmed standard. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00351';

-- REF-00412: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: DIN 18040-2:2011 + Draft E DIN 18040-2:2023 — confirmed series; draft 2023 in progress. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00412';

-- REF-00422: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: DIN 18040-1:2010 — Barrierefreies Bauen Teil 1: Öffentlich zugängliche Gebäude, confirmed via BIH. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00422';

-- REF-00431: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: DIN 18040-2:2011 Nullschwelle doctrine — section reference within confirmed standard. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00431';

-- REF-00445: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)
UPDATE evidence_sources SET
  metadata_quality = 'COMPLETE-STATUTORY',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part A: DIN 18040-1/-2 Türen (doors) — section reference within confirmed standards. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00445';

-- =============================================================
-- Part B: ASD-tagged academic recategorization (8 rows)
-- =============================================================

-- REF-00049: recategorize source_type standard->report, clear ASD tag
UPDATE evidence_sources SET
  source_type = 'report',
  standard_number = NULL,
  metadata_integrity_status = COALESCE(metadata_integrity_status, 'OK'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part B: Caniato 2024 Institute of Acoustics — academic paper, not a standard. source_type recategorized standard->report; standard_number cleared (ASD is topic tag, not standards identifier).',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part B: ASD-tag recategorization',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00049';

-- REF-00547: recategorize source_type standard->report, clear ASD tag
UPDATE evidence_sources SET
  source_type = 'report',
  standard_number = NULL,
  metadata_integrity_status = COALESCE(metadata_integrity_status, 'OK'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part B: Black 2022 SAGE/Autism — scoping review, not a standard. source_type recategorized standard->report; standard_number cleared (ASD is topic tag, not standards identifier).',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part B: ASD-tag recategorization',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00547';

-- REF-00602: recategorize source_type standard->report, clear ASD tag
UPDATE evidence_sources SET
  source_type = 'report',
  standard_number = NULL,
  metadata_integrity_status = COALESCE(metadata_integrity_status, 'OK'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part B: Kates 2025 PLOS — binaural study, not a standard. source_type recategorized standard->report; standard_number cleared (ASD is topic tag, not standards identifier).',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part B: ASD-tag recategorization',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00602';

-- REF-00611: recategorize source_type standard->report, clear ASD tag
UPDATE evidence_sources SET
  source_type = 'report',
  standard_number = NULL,
  metadata_integrity_status = COALESCE(metadata_integrity_status, 'OK'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part B: Leonardi 2025 SAGE/Autism — multisensory environments review, not a standard. source_type recategorized standard->report; standard_number cleared (ASD is topic tag, not standards identifier).',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part B: ASD-tag recategorization',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00611';

-- REF-00612: recategorize source_type standard->report, clear ASD tag
UPDATE evidence_sources SET
  source_type = 'report',
  standard_number = NULL,
  metadata_integrity_status = COALESCE(metadata_integrity_status, 'OK'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part B: De Domenico 2024 MDPI/JCM — multi-sensory environment study, not a standard. source_type recategorized standard->report; standard_number cleared (ASD is topic tag, not standards identifier).',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part B: ASD-tag recategorization',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00612';

-- REF-00613: recategorize source_type standard->report, clear ASD tag
UPDATE evidence_sources SET
  source_type = 'report',
  standard_number = NULL,
  metadata_integrity_status = COALESCE(metadata_integrity_status, 'OK'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part B: Kim 2022 SAGE/HERD — multisensory environment evaluation, not a standard. source_type recategorized standard->report; standard_number cleared (ASD is topic tag, not standards identifier).',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part B: ASD-tag recategorization',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00613';

-- REF-00702: recategorize source_type standard->report, clear ASD tag
UPDATE evidence_sources SET
  source_type = 'report',
  standard_number = NULL,
  metadata_integrity_status = COALESCE(metadata_integrity_status, 'OK'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part B: Korean Academy of Sensory Integration 2022 — systematic review, not a standard. source_type recategorized standard->report; standard_number cleared (ASD is topic tag, not standards identifier).',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part B: ASD-tag recategorization',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00702';

-- REF-00710: recategorize source_type standard->report, clear ASD tag
UPDATE evidence_sources SET
  source_type = 'report',
  standard_number = NULL,
  metadata_integrity_status = COALESCE(metadata_integrity_status, 'OK'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | statutory-cohort-cleanup 2026-05-21T01:30:00Z Part B: Tola 2021 MDPI/IJERPH — built environment review, not a standard. source_type recategorized standard->report; standard_number cleared (ASD is topic tag, not standards identifier).',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part B: ASD-tag recategorization',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00710';

-- =============================================================
-- Part C: Mostafa-ASPECTSS wrong-DOI cleanup (4 rows)
-- =============================================================

-- REF-00051: clear wrong DOI (Frontiers Psychiatry 10.3389/fpsyt.2021.727353 → 404)
UPDATE evidence_sources SET
  doi = NULL,
  verification_status = NULL,
  doi_resolution_outcome = NULL,
  metadata_quality = CASE WHEN metadata_quality IN ('COMPLETE', 'COMPLETE-STATUTORY') THEN 'AUTHOR-TITLE-ONLY' ELSE metadata_quality END,
  metadata_integrity_status = 'WRONG-DOI-CLEARED-POTENTIAL-DUPLICATE',
  metadata_integrity_detail = 'statutory-cohort-cleanup 2026-05-21T01:30:00Z Part C: DOI 10.3389/fpsyt.2021.727353 CLEARED — returns 404 at Crossref. Mostafa 2021 reference is to DCU "Autism Friendly University Design Guide" (issuu.com/magdamostafa/docs/the_autism_friendly_design_guide), NOT a Frontiers Psychiatry paper. All four rows (REF-00051, REF-00129, REF-00517, REF-00592) share this wrong-DOI; they are likely multi-citation references to the same Mostafa source. Owner: decide whether to merge into single row or keep separated by aspect.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part C: CLEAR-DOI wrong-attribution + potential-duplicate flag',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00051';

-- REF-00129: clear wrong DOI (Frontiers Psychiatry 10.3389/fpsyt.2021.727353 → 404)
UPDATE evidence_sources SET
  doi = NULL,
  verification_status = NULL,
  doi_resolution_outcome = NULL,
  metadata_quality = CASE WHEN metadata_quality IN ('COMPLETE', 'COMPLETE-STATUTORY') THEN 'AUTHOR-TITLE-ONLY' ELSE metadata_quality END,
  metadata_integrity_status = 'WRONG-DOI-CLEARED-POTENTIAL-DUPLICATE',
  metadata_integrity_detail = 'statutory-cohort-cleanup 2026-05-21T01:30:00Z Part C: DOI 10.3389/fpsyt.2021.727353 CLEARED — returns 404 at Crossref. Mostafa 2021 reference is to DCU "Autism Friendly University Design Guide" (issuu.com/magdamostafa/docs/the_autism_friendly_design_guide), NOT a Frontiers Psychiatry paper. All four rows (REF-00051, REF-00129, REF-00517, REF-00592) share this wrong-DOI; they are likely multi-citation references to the same Mostafa source. Owner: decide whether to merge into single row or keep separated by aspect.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part C: CLEAR-DOI wrong-attribution + potential-duplicate flag',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00129';

-- REF-00517: clear wrong DOI (Frontiers Psychiatry 10.3389/fpsyt.2021.727353 → 404)
UPDATE evidence_sources SET
  doi = NULL,
  verification_status = NULL,
  doi_resolution_outcome = NULL,
  metadata_quality = CASE WHEN metadata_quality IN ('COMPLETE', 'COMPLETE-STATUTORY') THEN 'AUTHOR-TITLE-ONLY' ELSE metadata_quality END,
  metadata_integrity_status = 'WRONG-DOI-CLEARED-POTENTIAL-DUPLICATE',
  metadata_integrity_detail = 'statutory-cohort-cleanup 2026-05-21T01:30:00Z Part C: DOI 10.3389/fpsyt.2021.727353 CLEARED — returns 404 at Crossref. Mostafa 2021 reference is to DCU "Autism Friendly University Design Guide" (issuu.com/magdamostafa/docs/the_autism_friendly_design_guide), NOT a Frontiers Psychiatry paper. All four rows (REF-00051, REF-00129, REF-00517, REF-00592) share this wrong-DOI; they are likely multi-citation references to the same Mostafa source. Owner: decide whether to merge into single row or keep separated by aspect.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part C: CLEAR-DOI wrong-attribution + potential-duplicate flag',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00517';

-- REF-00592: clear wrong DOI (Frontiers Psychiatry 10.3389/fpsyt.2021.727353 → 404)
UPDATE evidence_sources SET
  doi = NULL,
  verification_status = NULL,
  doi_resolution_outcome = NULL,
  metadata_quality = CASE WHEN metadata_quality IN ('COMPLETE', 'COMPLETE-STATUTORY') THEN 'AUTHOR-TITLE-ONLY' ELSE metadata_quality END,
  metadata_integrity_status = 'WRONG-DOI-CLEARED-POTENTIAL-DUPLICATE',
  metadata_integrity_detail = 'statutory-cohort-cleanup 2026-05-21T01:30:00Z Part C: DOI 10.3389/fpsyt.2021.727353 CLEARED — returns 404 at Crossref. Mostafa 2021 reference is to DCU "Autism Friendly University Design Guide" (issuu.com/magdamostafa/docs/the_autism_friendly_design_guide), NOT a Frontiers Psychiatry paper. All four rows (REF-00051, REF-00129, REF-00517, REF-00592) share this wrong-DOI; they are likely multi-citation references to the same Mostafa source. Owner: decide whether to merge into single row or keep separated by aspect.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-21T01:30:00Z statutory-cohort-cleanup] Part C: CLEAR-DOI wrong-attribution + potential-duplicate flag',
  updated_at = '2026-05-21T01:30:00Z', updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00592';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
