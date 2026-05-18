-- data_20260518010000_pmp_walk_a18_deaf_rt60.sql
--
-- PMP walk per standing rule #8 for A-18 DEAF population, claim RT60 <= 0.3 s.
-- Phase E.1 pilot Pass 2 sub-task 2 (chain order: rule #7 -> rule #8 -> rule #9 steps 4-9 -> rule #10).
--
-- Setup:
--   V0 = 0.3 s, U = s, D = down, claim_type = maximum
--   pop = "Pediatric hearing-aid or cochlear-implant users in classroom listening"
--   delta_min = 0.05 s (decisecond granularity is standard in DEAF acoustic specs;
--   sub-decisecond resolution is below measurement noise floor of ISO 3382 method)
--
-- Walk:
--   Step 1 (outer-stop): V_test = 0.24 s (V0 * 0.80). Primary + alt-phrasing
--          searches both fail. No peer-reviewed source specifies RT60 <= 0.24 s
--          for the target population. V_outer_floor = 0.30, V_outer_fail = 0.24.
--   Step 2 (refinement-stop): V_test = 0.27 s (midpoint, distance 0.06 > delta_min).
--          Both searches fail. New distance = 0.03 <= delta_min -> terminate.
--   Step 3 (final): V_empirical_ceiling = 0.30 s. gap_signed = 0.0.
--          Strict termination PASSED at V0: Iglehart 2020 (REF-00325, Tier 1,
--          COMPLETE/VERIFIED) is the peer-reviewed source. Its abstract conclusion:
--          "These results support the acoustic standard of 0.3-s RT for children
--          with hearing impairment in learning spaces <= 283 m^3."
--
-- Strict-termination detection-question check ("does evidence specifically validate
-- the value, or does it just speak to the topic?"): Iglehart 2020 specifically tested
-- 0.3 s as a discrete experimental condition with CHH using hearing aids and concluded
-- the standard is supported. Claim-level, not topic-level.
--
-- Topic-vs-claim guard (PI standing rule #7 anti-pattern): noted explicitly. Steps 1
-- and 2 returned topic-related results (e.g., DGUV 0.45 s; AES-3788 listening-room
-- formula; Iglehart 2020 itself uses 0.24 s as a CALIBRATION test signal, not a
-- specification value). None of these specifically validates RT60 <= 0.24 or <= 0.27
-- for the target population. passes_strict = 0 enforced.
--
-- REF-00335 (ANSI S12.60:2010) co-supports 0.3 s but is AUTHOR-TITLE-ONLY in
-- metadata_quality -> rule #10 ineligible. Not cited as PMP final-row ref_id.
-- Logged in notes for traceability; would become eligible after citation-miner pass.
--
-- Writes:
--   1. Three spec_value_probes rows (steps 1, 2, 3-final)
--   2. evidence_population_match row for REF-00325 keyed to this walk's slug + pop
--   3. UPDATE items.pmp_* columns on A-18
--   4. data_migrations row

-- Walk identifier
-- walk_id = 'PMP-A18-001'

-- 1a. Step 1: outer-stop at V_test = 0.24 s
INSERT INTO spec_value_probes (probe_id, walk_id, slug, item_code, spec_value_origin, spec_unit, direction, population, claim_type, step_index, phase, step_value, step_value_unit, search_query, search_query_alt, passes_strict, ref_id, notes, created_at, created_by_session)
VALUES ('PMP-A18-001-1', 'PMP-A18-001', 'room-acoustic-performance', 'A-18', 0.3, 's', 'down', 'DEAF (pediatric hearing-aid / cochlear-implant users in classroom listening)', 'maximum', 1, 'outer-stop', 0.24, 's',
  'classroom reverberation time RT60 0.24 seconds hearing impaired children standard specification',
  '"0.24 s" OR "240 ms" reverberation cochlear implant pediatric audiology specification',
  0, NULL,
  'V_test = V0 * 0.80 = 0.24 s. Primary search returned Iglehart 2020 PMC, where 0.24 s appears as a CALIBRATION test signal for measurement equipment, not as a specification value (topic-vs-claim guard: speaks to the topic). Alt-phrasing search returned cochlear-implant audiology results unrelated to room-acoustic specifications. No peer-reviewed source specifies RT60 <= 0.24 s for the target population. V_outer_floor = 0.30, V_outer_fail = 0.24.',
  '2026-05-18 01:00', 'session_2026-05-17-pilot-pass-2-sub-2');

-- 1b. Step 2: refinement-stop at V_test = 0.27 s
INSERT INTO spec_value_probes (probe_id, walk_id, slug, item_code, spec_value_origin, spec_unit, direction, population, claim_type, step_index, phase, step_value, step_value_unit, search_query, search_query_alt, passes_strict, ref_id, notes, created_at, created_by_session)
VALUES ('PMP-A18-001-2', 'PMP-A18-001', 'room-acoustic-performance', 'A-18', 0.3, 's', 'down', 'DEAF (pediatric hearing-aid / cochlear-implant users in classroom listening)', 'maximum', 2, 'refinement-stop', 0.27, 's',
  'classroom acoustic standard reverberation time 0.27 seconds hearing impaired hearing aid specification',
  '"270 ms" OR "0.27" RT60 hearing loss listening room acoustic requirement specification',
  0, NULL,
  'V_test = (0.30 + 0.24) / 2 = 0.27 s. Distance from V_outer_floor was 0.06 > delta_min = 0.05, so refinement step warranted. Primary search returned Iglehart 2020 again (still validating 0.3 s specifically; not 0.27 s), DGUV inclusive-classrooms guidance at <= 0.45 s, and other classroom-acoustic standards anchored to 0.6 s / 0.3 s decisecond marks. Alt-phrasing search returned AES-3788 listening-room formula (typically 200-400 ms range) and home-theater calculators — none specify 0.27 s for the target population. Topic-vs-claim guard: no source claim-validates 0.27 s. New distance = 0.03 <= delta_min = 0.05 -> terminate refinement.',
  '2026-05-18 01:00', 'session_2026-05-17-pilot-pass-2-sub-2');

-- 1c. Step 3: final row at V_empirical_ceiling = 0.30 s
INSERT INTO spec_value_probes (probe_id, walk_id, slug, item_code, spec_value_origin, spec_unit, direction, population, claim_type, step_index, phase, step_value, step_value_unit, passes_strict, ref_id, notes, created_at, created_by_session)
VALUES ('PMP-A18-001-F', 'PMP-A18-001', 'room-acoustic-performance', 'A-18', 0.3, 's', 'down', 'DEAF (pediatric hearing-aid / cochlear-implant users in classroom listening)', 'maximum', 3, 'final', 0.30, 's',
  1, 'REF-00325',
  'V_empirical_ceiling = 0.30 s. gap_signed = 0.00 (BPC value matches evidence floor exactly). Strict termination PASSED at V0: Iglehart 2020 (REF-00325, Tier 1, COMPLETE/VERIFIED) is the peer-reviewed anchor. Quote (paraphrased): "Results support the acoustic standard of 0.3-s RT for children with hearing impairment in learning spaces <= 283 m^3, as specified in ANSI/ASA S12.60-2010/Part 1." Detection-question check passes: study specifically tested 0.3 s as an experimental condition with CHH using hearing aids; this is claim-level validation, not topic-level. Co-supporting standard ANSI/ASA S12.60-2010 Part 1 S5.3 + Commentary 5.3.1 (REF-00335) is AUTHOR-TITLE-ONLY in metadata_quality -> rule #10 ineligible until citation-miner pass; not cited as ref_id here, but corroborates 0.3 s independently of Iglehart. Note for PMP audit C4: this walk has multiple outer/refinement steps (not just 1), so C4 shallow-probe flag does not apply.',
  '2026-05-18 01:00', 'session_2026-05-17-pilot-pass-2-sub-2');

-- 2. evidence_population_match for REF-00325 specifically keyed to this PMP walk
INSERT INTO evidence_population_match (match_id, source_ref, target_population, study_population, sample_size, match_grade, mismatch_note, created_at, created_by_session, ref_id, gap_id)
VALUES ('EPM-PMP-A18-001', 'REF-00325', 'DEAF (pediatric hearing-aid users, classroom listening, room volume <= 283 m^3)', 'Children with hearing loss wearing hearing aids; speech perception tested across multiple reverberation-time conditions including 0.3 s', 10, 'EXACT',
  'Iglehart 2020 directly tested 0.3 s as an experimental RT condition with N=10 CHH using hearing aids and concluded the value supports the ANSI/ASA S12.60-2010 standard for this population. Same condition (hearing-impaired pediatric), same setting (classroom), same value (0.3 s), same claim type (maximum). N=10 is small but is the published peer-reviewed evidence available; preliminary support from conference proceedings noted in the paper. PMP final-row anchor.',
  '2026-05-18 01:00', 'session_2026-05-17-pilot-pass-2-sub-2', 'REF-00325', NULL);

-- 3. Update items.pmp_* on A-18
UPDATE items
SET pmp_delta_min        = 0.05,
    pmp_direction        = 'down',
    pmp_last_walk_at     = '2026-05-18 01:00',
    pmp_empirical_ceiling = 0.30,
    pmp_gap_signed       = 0.00,
    updated_at           = '2026-05-18 01:00',
    updated_by_session   = 'session_2026-05-17-pilot-pass-2-sub-2'
WHERE item_code = 'A-18';

-- 4. Track migration
INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes)
VALUES (
    'pmp_walk_a18_deaf_rt60_2026-05-18',
    '2026-05-18 01:00',
    'pmp_walk_PMP_A18_001_3_probe_rows_1_epm_row_update_items_A18',
    'session_2026-05-17-pilot-pass-2-sub-2',
    'PMP walk PMP-A18-001 for A-18 DEAF RT60 maximum 0.3 s. Strict termination PASSED at V0 with REF-00325 (Iglehart 2020) as Tier-1 peer-reviewed anchor. V_empirical_ceiling = 0.30, gap_signed = 0.00. Walk has outer-stop + refinement-stop + final phases (3 rows). Phase E.1 pilot Pass 2 sub-task 2 complete; sub-task 3 (rule #9 steps 4-9 authoring) is next.'
);
