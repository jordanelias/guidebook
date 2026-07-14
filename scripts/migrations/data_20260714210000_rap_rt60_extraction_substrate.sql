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
-- that validated 0.3 s, PMP-A18-001-F strict-termination PASS) and ANSI/ASA
-- S12.60-2010/Part 1 (REF-00563, whose Footnote e ADOPTED 0.3 s from the same
-- Iglehart working-group line). The code is an ECHO of the measurement, not an
-- independent root. Both rows carry root_ref_id = REF-00325, so
-- v_value_independence(RT60, DEAF) = 1 independent root — NOT 2. Verified robust
-- by counterfactual (independent adversarial review 2026-07-14): the count stays
-- 1 even if ANSI is classed committee_assertion; only misclassifying it as an
-- independent measurement inflates to 2. This exercises migration 028's Finding-C
-- fix against real pilot evidence.
--
-- ADVERSARIAL-REVIEW FIXES (2026-07-14, independent pass) applied below:
--   * ANSI root is temporally the 2007-2008 Iglehart proceedings (out-of-corpus,
--     unregistered), NOT the 2020 paper. Rather than mint a separate external
--     root (which would wrongly split the single Iglehart line into 2 roots),
--     REF-00325 is recorded as the IN-CORPUS PROXY ANCHOR for that one research
--     line (2007-2008 origin -> 2020 validation), stated in root_classification_basis.
--   * Bettarello 0.4-0.7 s: the in-source location is UNCONFIRMED (the corpus
--     trail attributes the figure via a Caniato self-citation; no value_match rdc
--     row exists yet). extraction_method downgraded full-read -> skim; status held
--     at 'reviewed'; a value_match citation is required before 'verified'.
--   * probe reference uses the stable probe_id PMP-A18-001-F (not a rowid).
--
-- LOGGED FINDINGS (surfaced, not fixed here — governance freeze; not pilot-blocking):
--   * ANSI/ASA S12.60-2010 has FOUR unsuperseded corpus records (REF-00326,
--     REF-00335, REF-00563, REF-00604). This row cites REF-00563 (the Part-1
--     "Schools" record the slug links); the reasoning-doc/PMP chain cites
--     REF-00335. One physical standard under four ref_ids is a latent cross-ref
--     inflation vector (a value rooted to REF-00335 vs REF-00563 would count as 2)
--     — flag for a later dedup/supersession pass. This row dodges it by rooting to
--     REF-00325, not to any ANSI ref.
--   * DISCRIMINATOR CAVEAT: v_value_independence counts roots, not tiers. Row 3
--     makes (RT60, AUT) = 1 identical to (RT60, DEAF) = 1, but the AUT root is a
--     single-site n=7 Tier-3 recommendation and the DEAF root is Tier-1. The count
--     must be read ALONGSIDE tier, never as a standalone quality measure.

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
   'Peer-reviewed primary validation; PMP-A18-001-F strict-termination PASS at 0.3 s (gap_signed 0.00, REF-00325 anchor). REF-00325 is the in-corpus proxy anchor for the single Iglehart HA/CI classroom-RT research line (2007-2008 proceedings origin -> 2020 peer-reviewed validation); both DEAF rows root here so the line counts once.',
   0),

  -- Row 2 — an ECHO: ANSI/ASA S12.60 code value, rooted in the Iglehart line (same root).
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
   'Standards echo of the Iglehart measurement line; root_ref_id points to the in-corpus proxy anchor REF-00325 (the true root is the 2007-2008 Iglehart proceedings, out-of-corpus) so it does not inflate independence. NOTE: cites REF-00563 (Part-1 Schools, the slug-linked ANSI record); the reasoning-doc/PMP chain uses REF-00335 — one of four duplicate ANSI-2010 records flagged for dedup.',
   0),

  -- Row 3 — the NDV/AUT source-stated RANGE (Tier-3 single-site; provenance hedged).
  ('REF-00561', 'room-acoustic-performance', 'RT60', 'RT60', 'AUT', 'IT',
   'range', '0.4-0.7', 's',
   'Bettarello 2021 is attributed an aspirational RT60 range of 0.4-0.7 s for autistic occupants from acoustic optimization of one Italian daily-care facility (n=7 rooms). A design recommendation, not a Tier-1 threshold.',
   'Acoustic optimization results (n=7 rooms, single facility) — in-source location UNCONFIRMED',
   'skim', 'reviewed', '2026-07-14T21:00:00Z', '2026-07-14T21:00:00Z',
   'session_2026-07-14-pilot-rt60-extraction-substrate',
   'root-rt60-aut-bettarello', 'measurement_primary', 'REF-00561', NULL,
   'instrumented_physical_measurement', 'not_device_scoped',
   'Single Italian daily-care facility, n=7 rooms, autistic occupants (Bettarello 2021)',
   'references/bpc-reasoning/room-acoustic-performance.md#step-5-tier-evidence (NDV/AUT Tier 3) + REF-00561',
   'Tier-3 single-site instrumented measurement (a weak measurement root, not a committee assertion). PROVENANCE HEDGE: the 0.4-0.7 s figure is relayed from the reasoning doc; the corpus trail attributes it via a Caniato self-citation and the value is NOT yet confirmed at its in-source location — a value_match reasoning_doc_citations row against Bettarello body text is required before promoting past reviewed. jurisdiction=IT is the study site (evidence_sources classes REF-00561 as INT); population=AUT is the FK-valid precise code (the 7 existing rdc rows use the non-FK string NDV,AUT — reconcile at cell-state join). The pilot chosen value 0.4 s is a conjecture at this range floor and lives in cell-state, not here.',
   0);
