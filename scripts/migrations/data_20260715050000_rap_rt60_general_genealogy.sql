-- data_20260715050000_rap_rt60_general_genealogy.sql
--
-- Phase E.1 pilot (room-acoustic-performance) — Checkpoint 1, next block: the
-- GENERAL RT60 genealogy. This is where the committee_assertion-unless-traceable
-- rule (owner-approved 2026-07-14, rule "a") does its real work — the "many
-- jurisdictions agree on ~0.6 s" case.
--
-- THE RULE-(a) DEMONSTRATION. ~15 national codes state a general classroom RT60
-- target in the 0.4-0.8 s band (US ANSI, UK BB93, DE DIN 18041, IT UNI 11532-2,
-- AU/NZ AS/NZS 2107, Nordic, NL, BE, ES, ...). Naively that reads as overwhelming
-- independent evidence. But per the pilot's own step-7 rationale, they all descend
-- from ONE research lineage: Sabine absorption (early 1900s) -> the Speech
-- Transmission Index (Houtgast & Steeneken, 1970s) -> Bradley & Sato classroom
-- studies (1990s-2000s), converging on ~0.4-0.8 s for typical-hearing speech
-- understanding. So the codes are ECHOES of one out-of-corpus measurement root,
-- not N independent roots. This migration registers that root once and roots the
-- code values to it, so v_value_independence(RT60, ALL) = 1 -- consensus, not
-- evidence. Jurisdictional agreement is still recorded (as convergence, in the
-- reasoning doc), never laundered into an independence count.
--
-- CONTESTED (per DR §H1 discipline c). The pilot's step-7 calls the convergence
-- "independent rather than copy-derived -- different working groups landed in the
-- same band from different epistemic frames." That is a genuine tension: shared
-- underlying science (echo of one root, this migration's read) vs genuinely
-- independent per-jurisdiction measurement programs (which would be multiple
-- roots). Because I cannot open most of these statutory standards to trace whether
-- each ran its own measurements (they are PAYWALL -- posture "b"), the honest,
-- conservative call under rule (a) is: root them to the shared STI lineage and set
-- contested=1, so the root-vs-echo judgment is recordably disputable, not asserted.
-- A reviewer or a later paywall-cleared read can split any row into its own root.
--
-- PAYWALL (posture "b"). The VALUES here are from the pilot's step-3 table (Pass 1,
-- "citation-grade verification PENDING"); extraction_method reflects what was
-- actually done (UK/BB93 was rule-#10 verified -> re-read; the paywalled statutory
-- standards -> skim, not re-opened at section this pass). The rule-#10
-- reasoning_doc_citations for the paywalled cells are flagged NOT-FOUND/paywall in
-- the citations pass, not fabricated.
--
-- STAGED then applied by me under the owner's standing authorization
-- ("you don't need my permission, just do it", 2026-07-14) AFTER an independent
-- adversarial review. Held behind the pilot's PROVISIONAL banner; source-stated
-- values only (the chosen 0.6 s general value is cell-state, not here). DEM 0.5 s
-- is deliberately ABSENT: no source states a dementia-specific RT60 (the pilot's
-- thinnest base), so its chosen value is a synthesis that lives in cell-state, and
-- authoring an extraction row would fabricate a source claim that does not exist.

BEGIN;

-- The one out-of-corpus measurement root the general classroom target descends from.
INSERT OR IGNORE INTO external_root_registry
  (root_id, description, root_type, provenance, root_population_note, notes, created_at, created_by_session)
VALUES
  ('root-rt60-general-sti',
   'Speech-intelligibility science lineage: Sabine absorption (early 1900s) -> Speech Transmission Index (Houtgast & Steeneken, 1970s) -> Bradley & Sato classroom acoustics studies (1990s-2000s), converging on RT60 ~0.4-0.8 s for typical-hearing speech understanding at conversational distance under controlled background noise.',
   'measurement_primary',
   'Out-of-corpus research lineage named in references/bpc-reasoning/room-acoustic-performance.md step-7 (general rationale). Individual primaries (Sabine; Houtgast/Steeneken; Bradley/Sato) are not separately in the evidence corpus; registered here as one external root per DR-2026-07-13 §H1 discipline (a).',
   'typical-hearing occupants, general-use indoor / classroom spaces',
   'General classroom RT60 target root. Jurisdiction code values in the 0.4-0.8 s band echo this lineage (contested; see rows).',
   '2026-07-15T05:00:00Z', 'session_2026-07-15-pilot-rt60-general-genealogy');

-- General RT60 code values, each an echo of the STI root (contested root-vs-echo call).
INSERT INTO source_value_extractions
  (ref_id, slug, parameter, parameter_canonical, population_code, jurisdiction,
   claim_type, claimed_value, claimed_unit, claim_text, source_section,
   extraction_method, extraction_status, created_at, updated_at, created_by_session,
   root_id, root_type, root_ref_id, echo_of, measurement_paradigm, device_class,
   root_population_note, file_anchor, root_classification_basis, contested)
VALUES
  ('REF-00563', 'room-acoustic-performance', 'RT60', 'RT60', 'ALL', 'US',
   'numerical', '0.6', 's',
   'ANSI/ASA S12.60-2010/Part 1: general classroom RT60 <= 0.6 s in core learning spaces <= 283 m3.',
   'Main reverberation-time requirement, core learning spaces <= 283 m3',
   'skim', 'reviewed', '2026-07-15T05:00:00Z', '2026-07-15T05:00:00Z',
   'session_2026-07-15-pilot-rt60-general-genealogy',
   'root-rt60-general-sti', 'measurement_primary', NULL,
   'ANSI/ASA S12.60 adopts the general classroom target from the speech-intelligibility science; the ASA S12 working group draws on the Bradley/Sato/STI line (step-7).',
   'instrumented_physical_measurement', 'not_device_scoped',
   'typical-hearing occupants, learning spaces <= 283 m3',
   'references/bpc-reasoning/room-acoustic-performance.md#step-3 (US row) + step-7 (general) + REF-00563',
   'Echo of the STI lineage (root-rt60-general-sti). CONTESTED: step-7 frames cross-jurisdiction convergence as "independent rather than copy-derived"; whether ANSI ran independent measurements vs adopted the shared science is not traceable at this pass (paywalled). Rooted to the shared lineage conservatively; splittable on a cleared read.',
   1),

  ('REF-00562', 'room-acoustic-performance', 'RT60', 'RT60', 'ALL', 'UK',
   'range', '0.4-0.8', 's',
   'BB93 (2015) Table 6: general teaching space Tmf (500/1k/2k Hz avg) 0.4-0.8 s by room type.',
   'Table 6, p.33 (general/new-build rooms)',
   're-read', 'reviewed', '2026-07-15T05:00:00Z', '2026-07-15T05:00:00Z',
   'session_2026-07-15-pilot-rt60-general-genealogy',
   'root-rt60-general-sti', 'measurement_primary', NULL,
   'BB93 room-type Tmf targets descend from the same speech-intelligibility science (step-7).',
   'instrumented_physical_measurement', 'not_device_scoped',
   'general school occupants',
   'references/bpc-reasoning/room-acoustic-performance.md#step-3 (UK) + REF-00562 Table 6; value rule-#10 verified in RDC-RAP-RT60-UK-001/002',
   'Echo of the STI lineage. CONTESTED as above. Value itself is rule-#10 verified (RDC-RAP-RT60-UK-001/002, EXACT) but that verifies the number, not root independence. Metric is Tmf (500/1k/2k Hz), not strictly RT60 -- same value, per the UK rdc notes.',
   1),

  ('REF-00329', 'room-acoustic-performance', 'RT60', 'RT60', 'ALL', 'DE',
   'range', '0.4-0.8', 's',
   'DIN 18041:2016 volume-dependent target curve yields RT60 typically 0.4-0.8 s for small-to-medium rooms by use type.',
   'Volume-dependent target curve (Hoersamkeit), by room use type',
   'skim', 'reviewed', '2026-07-15T05:00:00Z', '2026-07-15T05:00:00Z',
   'session_2026-07-15-pilot-rt60-general-genealogy',
   'root-rt60-general-sti', 'measurement_primary', NULL,
   'DIN 18041 target curve descends from the same speech-intelligibility science (step-7); formula-based comparator.',
   'instrumented_physical_measurement', 'not_device_scoped',
   'general occupants, small-to-medium rooms',
   'references/bpc-reasoning/room-acoustic-performance.md#step-3 (DE) + REF-00329',
   'Echo of the STI lineage. CONTESTED as above; PAYWALL -- DIN 18041 not re-opened at section this pass, value from pilot step-3.',
   1),

  ('REF-00564', 'room-acoustic-performance', 'RT60', 'RT60', 'ALL', 'IT',
   'numerical', '0.5', 's',
   'UNI 11532-2:2020 room-class A4 (high-criticality educational) general RT60 target approximately 0.5 s.',
   'Room-class A4 reverberation target',
   'skim', 'reviewed', '2026-07-15T05:00:00Z', '2026-07-15T05:00:00Z',
   'session_2026-07-15-pilot-rt60-general-genealogy',
   'root-rt60-general-sti', 'measurement_primary', NULL,
   'UNI 11532-2 room-class targets descend from the same speech-intelligibility science (step-7); room-class comparator.',
   'instrumented_physical_measurement', 'not_device_scoped',
   'general occupants, class A4 educational spaces',
   'references/bpc-reasoning/room-acoustic-performance.md#step-3 (IT) + REF-00564',
   'Echo of the STI lineage. CONTESTED as above; PAYWALL -- UNI 11532-2 not re-opened at section this pass, value from pilot step-3.',
   1),

  ('REF-00574', 'room-acoustic-performance', 'RT60', 'RT60', 'ALL', 'AU/NZ',
   'range', '0.4-0.6', 's',
   'AS/NZS 2107:2016 recommended RT60 for typical classroom space types approximately 0.4-0.6 s.',
   'Recommended reverberation times table, classroom space types',
   'skim', 'reviewed', '2026-07-15T05:00:00Z', '2026-07-15T05:00:00Z',
   'session_2026-07-15-pilot-rt60-general-genealogy',
   'root-rt60-general-sti', 'measurement_primary', NULL,
   'AS/NZS 2107 space-type table descends from the same speech-intelligibility science (step-7).',
   'instrumented_physical_measurement', 'not_device_scoped',
   'general occupants, classroom space types',
   'references/bpc-reasoning/room-acoustic-performance.md#step-3 (AU/NZ) + REF-00574',
   'Echo of the STI lineage. CONTESTED as above; PAYWALL -- AS/NZS 2107 not re-opened at section this pass, value from pilot step-3.',
   1);

COMMIT;
