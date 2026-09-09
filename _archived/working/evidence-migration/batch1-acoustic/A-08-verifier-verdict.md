# A-08 — separate verifier verdict: **CONFIRMED (with refinements folded in)** · 2026-07-19

An independent guilty-until-proven verifier re-checked the A-08 derivation against `data/guidebook.db`
(24 tool calls) and the web. The ◐ code-floor grade is **CONFIRMED**; two refinements were surfaced and
written into the cell. Nothing fabricated.

| # | claim | verdict | key evidence retrieved |
|---|---|---|---|
| C1 | PMP walk converges NC-25, code-anchored, no strict-pass evidence ref | CONFIRMED | 3 rows, NC-20/24 fail, final NC-25 gap=0; no `passes_strict=1`, all `ref_id=None` |
| C2 | No T1/T2 sets an NC/dBA threshold | CONFIRMED | 17 Tier≤2 links all RT60/speech/effort *outcomes*; `source_value_extractions` 100% RT60, 0 NC/dBA hits; **strongest refutation path** (T1 autism-noise REF-00726/00727) = noise-as-stressor (~55 dBA), not a design ceiling |
| **C3** | **metric mapping honest** | **CONFIRMED (+ refinements)** | **ANSI/ASA S12.60 = ≤35 dB(A) (~NC-30), NOT NC-25**; "NC-25" is an **ASHRAE** HVAC-component convention via dBA→NC extrapolation. Derivation flagged this correctly; label owed |
| C4 | ◐ `regulatory_stratum_only` correct (● = laundering) | CONFIRMED | doctrine (evidence-architecture §6/§8.3, DR-2026-07-12 G1, mapping L163); consistent with the only precedents — E-06 (9005) + A-02 (9012) |
| C5 | one universal cell, not six | CONFIRMED | value identical across all 6 populations; ANSI even excludes special-ed rooms → no population-specific NC evidence; six cells would fabricate differentiation |
| C6 | held (no A-08 cell); DAR high-penalty | CONFIRMED | 0 A-08 rows pre-write; HVAC remedies (silencers, plant isolation, low-velocity duct) web-confirmed as design-stage, high deferral penalty |

## Refinements written into the cell (the verifier improved it)

1. **Anchor corrected.** The migrated code ref REF-00563 (ANSI) anchors the **≤35 dBA room-total floor
   (~NC-30, laxer)**, not NC-25. NC-25 is an **ASHRAE HVAC-component** figure, and **no ASHRAE acoustic
   ref is migrated** (REF-00620 is ASHRAE *filtration*/MERV) → the NC-25 anchor is **owed**. The cell
   records `governing_refs=['REF-00563']` with the ASHRAE/NC-25 provenance and the owed-ref stated.
2. **Metric labelled.** NC-25 carries `extrapolated-from(dBA→NC)` in the cell's provenance; the falsehood
   in the underlying PMP walk row ("matches ANSI S12.60 exactly, gap=0") is flagged for a walk-note
   correction (hygiene track) — it does not affect the ◐ grade.

**Verdict: ◐ code-floor CORRECT and doctrinally consistent.** Written to `evidence_cell_state` as cell 9013
(state=provisional, regulatory_stratum_only=1, NC-25, governing REF-00563) + convergence 9013 — migration
`data_20260719023539`. Verified: FK-check clean · 35/35 integrity · rebuild-parity PASS. Grading throat
**8 → 9 of 93 items**.

*Same slug↔item seam as A-02 noted (walk rows under `school-environment-autism`, item_code correctly A-08)
— Stage-0 triage track.*
