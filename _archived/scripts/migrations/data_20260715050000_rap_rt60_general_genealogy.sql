-- data_20260715050000_rap_rt60_general_genealogy.sql
--
-- Phase E.1 pilot (room-acoustic-performance) — Checkpoint 1, next block: the
-- GENERAL RT60 genealogy, under the owner-approved rule (a)
-- (committee_assertion-unless-traceable) + PAYWALL posture (b).
--
-- CORRECTED after independent adversarial review (2026-07-15, verdict DO-NOT-APPLY
-- on the prior draft). The prior draft made the self-serving error: it typed all 5
-- jurisdiction codes as measurement_primary ECHOES of a manufactured STI external
-- root, yielding v_value_independence(RT60, ALL) = 1. That violated rule (a):
--   * Rule (a)'s DEFAULT is committee_assertion; measurement_primary must be EARNED
--     by traceability. The draft itself admitted the measurement root is "not
--     traceable at this pass (paywalled)" — so the rule yields committee_assertion.
--   * Reasoning-doc step-7 ("independent rather than copy-derived — different
--     working groups landed in the same band from different epistemic frames")
--     describes independent COMMITTEE DELIBERATION, not independent MEASUREMENT.
--     Independent committees converging on a value is the textbook committee_assertion
--     case; it does NOT grant measurement independence.
--   * "1" laundered one independence unit out of pure consensus — the exact thing
--     the header claimed not to do; and contested=1 is cosmetic to the discriminator.
--   * measurement_primary planted a 1->5 inflation bomb (a later "split" of the 5
--     rows -> independence 5); committee_assertion is inflation-proof (stays absent).
--
-- CORRECT CLASSIFICATION: all 5 jurisdiction code values are committee_assertion.
-- The v_value_independence allow-list excludes committee_assertion, so RT60/ALL is
-- ABSENT from the view = 0 independent roots = "consensus, not evidence" — rule-(a)-
-- faithful and inflation-proof. No STI external-root stub is needed (committee
-- assertions carry no measurement root). The rows still back the step-3 table cells
-- ("no cell without a backing extraction row") and document what the codes state.
--
-- If the owner later wants to credit the speech-intelligibility science as one real
-- root behind the guidebook's CHOSEN general value, the honest expression is a single
-- measurement_primary row rooted to a SPECIFIC primary (Bradley & Sato) attached to
-- the chosen value in cell-state (Checkpoint 4) — not 5 paywalled codes rooted to a
-- vague 100-year lineage. Deferred to cell-state.
--
-- PAYWALL (posture b): US/DE/IT/AU-NZ standards were NOT re-opened at section this
-- pass (skim; values copied from the pilot step-3 table, itself "verification
-- PENDING") -> extraction_status = preliminary. UK values ARE rule-#10 verified
-- (RDC-RAP-RT60-UK-001 = 0.6 primary; UK-002 = 0.8 secondary) -> reviewed; the 0.4
-- floor is the specially-resourced (HI/DEAF) value (UK-003), NOT general, so the UK
-- general value is recorded as 0.6-0.8.
--
-- LOGGED (not fixed, per freeze): population_code='ALL' means "applies universally"
-- but a general/typical value does NOT apply universally (DEAF 0.3 / AUT 0.4 / DEM
-- 0.5 differ). There is no dedicated 'general' population code; 'ALL' is the existing
-- convention (the 7 UK reasoning_doc_citations already use it for general values), so
-- it is used here for consistency and the taxonomy gap is flagged for the owner. Also:
-- US cites REF-00563 (Part-1 Schools, slug-linked); the doc/PMP chain uses REF-00335;
-- four duplicate ANSI-2010 records (REF-00326/335/563/604) remain flagged for dedup.
--
-- STAGED then applied by me under the owner's standing authorization
-- ("you don't need my permission, just do it", 2026-07-14) after this corrected pass.
-- Held behind the pilot's PROVISIONAL banner; source-stated values only.

BEGIN;

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
   'skim', 'preliminary', '2026-07-15T05:00:00Z', '2026-07-15T05:00:00Z',
   'session_2026-07-15-pilot-rt60-general-genealogy',
   NULL, 'committee_assertion', NULL,
   'Standards-committee value (ASA S12 working group); no independent measurement root traceable to corpus at this pass.',
   'stated_unmeasured', 'not_device_scoped',
   'typical-hearing occupants, learning spaces <= 283 m3',
   'references/bpc-reasoning/room-acoustic-performance.md#step-3 (US) + step-7 + REF-00563',
   'committee_assertion per rule (a): no traceable measurement root (PAYWALL, not re-opened). Excluded from v_value_independence -> RT60/ALL absent = consensus, not evidence. contested=1: a paywall-cleared read could trace an independent measurement root, which would then need registration to score.',
   1),

  ('REF-00562', 'room-acoustic-performance', 'RT60', 'RT60', 'ALL', 'UK',
   'range', '0.6-0.8', 's',
   'BB93 (2015) Table 6: general teaching spaces Tmf (500/1k/2k Hz avg) 0.6 s (primary) to 0.8 s (secondary).',
   'Table 6, p.33 (general new-build rooms)',
   're-read', 'reviewed', '2026-07-15T05:00:00Z', '2026-07-15T05:00:00Z',
   'session_2026-07-15-pilot-rt60-general-genealogy',
   NULL, 'committee_assertion', NULL,
   'Standards-committee value; independent committee deliberation, not independent measurement.',
   'stated_unmeasured', 'not_device_scoped',
   'general school occupants',
   'references/bpc-reasoning/room-acoustic-performance.md#step-3 (UK) + REF-00562 Table 6',
   'committee_assertion per rule (a). Value rule-#10 verified: RDC-RAP-RT60-UK-001 (0.6, primary) + UK-002 (0.8, secondary), EXACT — so status reviewed. NOTE: the 0.4 floor in step-3 is the specially-resourced (HI/DEAF) value (UK-003), NOT general, so general is recorded as 0.6-0.8. Metric is Tmf, not strictly RT60 (same value, per UK rdc notes).',
   1),

  ('REF-00329', 'room-acoustic-performance', 'RT60', 'RT60', 'ALL', 'DE',
   'range', '0.4-0.8', 's',
   'DIN 18041:2016 volume-dependent target curve yields RT60 typically 0.4-0.8 s for small-to-medium rooms by use type.',
   'Volume-dependent target curve (Hoersamkeit), by room use type',
   'skim', 'preliminary', '2026-07-15T05:00:00Z', '2026-07-15T05:00:00Z',
   'session_2026-07-15-pilot-rt60-general-genealogy',
   NULL, 'committee_assertion', NULL,
   'Standards-committee value (formula-based comparator); no independent measurement root traceable to corpus at this pass.',
   'stated_unmeasured', 'not_device_scoped',
   'general occupants, small-to-medium rooms',
   'references/bpc-reasoning/room-acoustic-performance.md#step-3 (DE) + REF-00329',
   'committee_assertion per rule (a): no traceable measurement root (PAYWALL, DIN 18041 not re-opened; value from pilot step-3). Excluded from independence. contested=1.',
   1),

  ('REF-00564', 'room-acoustic-performance', 'RT60', 'RT60', 'ALL', 'IT',
   'numerical', '0.5', 's',
   'UNI 11532-2:2020 room-class A4 (high-criticality educational) general RT60 target approximately 0.5 s.',
   'Room-class A4 reverberation target',
   'skim', 'preliminary', '2026-07-15T05:00:00Z', '2026-07-15T05:00:00Z',
   'session_2026-07-15-pilot-rt60-general-genealogy',
   NULL, 'committee_assertion', NULL,
   'Standards-committee value (room-class comparator); no independent measurement root traceable to corpus at this pass.',
   'stated_unmeasured', 'not_device_scoped',
   'general occupants, class A4 educational spaces',
   'references/bpc-reasoning/room-acoustic-performance.md#step-3 (IT) + REF-00564',
   'committee_assertion per rule (a): no traceable measurement root (PAYWALL, UNI 11532-2 not re-opened; value from pilot step-3). Excluded from independence. contested=1.',
   1),

  ('REF-00574', 'room-acoustic-performance', 'RT60', 'RT60', 'ALL', 'AU/NZ',
   'range', '0.4-0.6', 's',
   'AS/NZS 2107:2016 recommended RT60 for typical classroom space types approximately 0.4-0.6 s.',
   'Recommended reverberation times table, classroom space types',
   'skim', 'preliminary', '2026-07-15T05:00:00Z', '2026-07-15T05:00:00Z',
   'session_2026-07-15-pilot-rt60-general-genealogy',
   NULL, 'committee_assertion', NULL,
   'Standards-committee value (space-type table); no independent measurement root traceable to corpus at this pass.',
   'stated_unmeasured', 'not_device_scoped',
   'general occupants, classroom space types',
   'references/bpc-reasoning/room-acoustic-performance.md#step-3 (AU/NZ) + REF-00574',
   'committee_assertion per rule (a): no traceable measurement root (PAYWALL, AS/NZS 2107 not re-opened; value from pilot step-3). Excluded from independence. contested=1.',
   1);

COMMIT;
