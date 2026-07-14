-- data_20260714210000_rap_rt60_extraction_substrate.sql
--
-- Phase E.1 pilot (room-acoustic-performance) — Checkpoint 1: the first
-- source_value_extractions rows, authored WITH H1 genealogy from row one
-- (migration 028). Scope: the DEAF RT60 evidence base + the NDV/AUT Tier-3
-- source-stated range. This is the "no step-3 table cell without a backing
-- extraction row" substrate (Phase-E plan v1 §4 Pass-1 step 4) for the pilot's
-- best-evidenced parameter/population.
--
-- STAGED, not applied to canonical — presented for owner review per the
-- 2026-07-14 posture (adversarial review before application). Held behind the
-- pilot's PROVISIONAL banner; writes NO chosen values (those are cell-state,
-- Checkpoint 4) — only what the SOURCES state.
--
-- GENEALOGY DEMONSTRATION (the reason this is Checkpoint 1). The DEAF 0.3 s value
-- appears in TWO sources: Iglehart 2020 (REF-00325, the peer-reviewed measurement
-- that validated 0.3 s, PMP-A18-001 strict-termination PASS) and ANSI/ASA
-- S12.60-2010/Part 1 (REF-00563, whose Footnote e ADOPTED 0.3 s from the same
-- Iglehart working-group line). The code is an ECHO of the measurement, not an
-- independent root. Both rows therefore carry root_ref_id = REF-00325, so
-- v_value_independence(RT60, DEAF) = 1 independent root — NOT 2. This exercises
-- the migration-028 fix (Finding C) against real pilot evidence: two sources,
-- one root, correctly not inflated.
--
-- Blocker note: the pilot's May-era "REF-00335 AUTHOR-TITLE-ONLY" flag is RESOLVED
-- — both ANSI entries (REF-00335, REF-00563) are now COMPLETE-STATUTORY/VERIFIED;
-- the slug cites REF-00563.

INSERT INTO source_value_extractions
  (ref_id, slug, parameter, parameter_canonical, population_code, jurisdiction,
   claim_type, claimed_value, claimed_unit, claim_text, source_section,
   extraction_method, extraction_status, created_at, updated_at, created_by_session,
   root_id, root_type, root_ref_id, echo_of, measurement_paradigm, device_class,
   root_population_note, file_anchor, root_classification_basis, contested)
VALUES
  -- Row 1 — the ROOT: Iglehart 2020 peer-reviewed measurement of 0.3 s.
  ('REF-00325', 'room-acoustic-performance', 'RT60', 'RT60', 'DEAF', 'US',
   'numerical', '0.3', 's',
   'Iglehart 2020 validated speech perception for children with hearing impairment using hearing aids in RT60 = 0.3 s learning spaces <= 283 m3; results support the 0.3 s acoustic standard for this population.',
   'Results / abstract conclusion (N=10 pediatric HA users, four RT conditions)',
   're-read', 'verified', '2026-07-14T21:00:00Z', '2026-07-14T21:00:00Z',
   'session_2026-07-14-pilot-rt60-extraction-substrate',
   'root-rt60-deaf-iglehart', 'measurement_primary', 'REF-00325', NULL,
   'instrumented_physical_measurement', 'not_device_scoped',
   'N=10 pediatric hearing-aid users, classroom listening, learning spaces <= 283 m3 (Iglehart 2020)',
   'references/bpc-reasoning/room-acoustic-performance.md#step-5-tier-evidence (DEAF Tier 1) + REF-00325',
   'Peer-reviewed primary validation; PMP-A18-001 strict-termination PASS at 0.3 s (spec_value_probes probe 21, gap_signed 0.00). This is the in-corpus anchor for the Iglehart HA/CI classroom-RT measurement line.',
   0),

  -- Row 2 — an ECHO: ANSI/ASA S12.60 code value, rooted in Iglehart (same root_ref_id).
  ('REF-00563', 'room-acoustic-performance', 'RT60', 'RT60', 'DEAF', 'US',
   'numerical', '0.3', 's',
   'ANSI/ASA S12.60-2010/Part 1 Footnote e: RT60 <= 0.3 s for children with hearing impairment in core learning spaces <= 283 m3.',
   'Section 5.3 Footnote e + Annex Commentary 5.3.1',
   're-read', 'reviewed', '2026-07-14T21:00:00Z', '2026-07-14T21:00:00Z',
   'session_2026-07-14-pilot-rt60-extraction-substrate',
   'root-rt60-deaf-iglehart', 'measurement_primary', 'REF-00325',
   'ANSI/ASA S12.60-2010 Footnote e adopts 0.3 s from the Iglehart working-group research (2007-2008 proceedings), peer-review-validated by Iglehart 2020 (REF-00325). The code value is a standards echo, not an independent root.',
   'instrumented_physical_measurement', 'not_device_scoped',
   'Same root population as Iglehart 2020 (pediatric HA/CI, learning spaces <= 283 m3)',
   'references/bpc-reasoning/room-acoustic-performance.md#step-4-lowest-barrier-code (DEAF) + REF-00563 S5.3',
   'Standards echo of the Iglehart measurement; recorded as echo_of, root_ref_id points to the measurement root REF-00325 so it does not inflate independence.',
   0),

  -- Row 3 — the NDV/AUT source-stated RANGE (Tier-3 single-site measurement root).
  ('REF-00561', 'room-acoustic-performance', 'RT60', 'RT60', 'AUT', 'IT',
   'range', '0.4-0.7', 's',
   'Bettarello 2021 proposes an aspirational RT60 range of 0.4-0.7 s from acoustic optimization of one Italian daily-care facility (n=7 rooms) for autistic occupants. A design recommendation, not a Tier-1 threshold.',
   'Acoustic optimization results (n=7 rooms, single facility)',
   'full-read', 'reviewed', '2026-07-14T21:00:00Z', '2026-07-14T21:00:00Z',
   'session_2026-07-14-pilot-rt60-extraction-substrate',
   'root-rt60-aut-bettarello', 'measurement_primary', 'REF-00561', NULL,
   'instrumented_physical_measurement', 'not_device_scoped',
   'Single Italian daily-care facility, n=7 rooms, autistic occupants (Bettarello 2021)',
   'references/bpc-reasoning/room-acoustic-performance.md#step-5-tier-evidence (NDV/AUT Tier 3) + REF-00561',
   'Tier-3 single-site instrumented measurement (weak but a measurement root, not a committee assertion). The pilot chosen value 0.4 s is a conjecture at this range floor and lives in cell-state, not here.',
   0);
