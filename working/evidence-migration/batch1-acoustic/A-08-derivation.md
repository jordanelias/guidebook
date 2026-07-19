# Batch 1 · A-08 — HVAC Noise Control (NC-25 Max in Sensitive Spaces) — agonist derivation

*Slug `room-acoustic-performance`. Grounded in `data/guidebook.db` (3 PMP walks, linked sources). Pending
the separate verifier (`A-08-verifier-verdict.md`). Nothing written to `evidence_cell_state` until confirmed.*

## Headline (same shape as A-02): NC-25 is **code-anchored (◐), not evidence-derived (●)**

A-08 is a **TECHNIQUE-layer** provision (S5): HVAC noise control is a *technique* for the low-background-noise
environment that noise-sensitive populations need; the low-noise environment is what actually serves them
(and connects to A-18's RT60 target). The strict-termination PMP walk (populations **AUT · PCS · DEM · MH ·
PAIN · OFS**) converged on **NC-25** — outer-stop NC-20 fails ("no source specifies it for these
populations"), refinement NC-24 fails ("not in any standard"), and the final step records
`V_empirical_ceiling=25, gap_signed=0, "BPC value matches ANSI S12.60."`

**The anchor is a code (ANSI S12.60), not primary evidence.** As with A-02, the 17 linked Tier≤2 acoustic
sources are RT60 / speech-perception / listening-effort **outcomes** — none sets an HVAC background-noise
(NC/dBA) threshold. So under doctrine (T4–6 walled off; converge ≠ evidence) the value grades **◐
`regulatory_stratum_only`, state=provisional** — not ●.

## ⚠ Anti-fabrication flag for the verifier — metric mapping

ANSI/ASA S12.60 states its background-noise limit as a **dBA** figure (commonly **≤35 dBA** for core learning
spaces). The item and the walk state **NC-25**. NC and dBA are *different metrics*; NC-25 is a plausible
NC-curve equivalent of ~35 dBA, but **that mapping is an extrapolation, not a direct code citation.** The
walk asserts "matches ANSI S12.60" without recording the metric conversion. **The verifier must confirm
whether ANSI S12.60 specifies NC-25 directly or specifies dBA (and NC-25 is a derived equivalent).** If the
latter, the value carries an `extrapolated-from(dBA→NC)` label and the code-floor is honestly "≤35 dBA,
≈ NC-25."

## Modeling — one universal code-floor cell, not six

The NC-25 value is **uniform across all six sensitive populations** and code-anchored — it is not
population-differentiated. So (unlike A-18, which had genuinely different RT60 values per population) A-08 is
**one cell**, `design_scale=universal` (NC-25 is a population-agnostic code criterion), scoped to
**sensitive-occupancy spaces** via the note — not six redundant population cells. `items.pmp_delta_min` is
NULL (direction 'down'); no per-person delta.

## Ethics screen (A10) — brief

- **V-06 evidence-tier laundering** (live risk): presenting the ANSI/ASHRAE convergence as the evidence
  basis. Foreclosed by grading ◐ and keeping the ● evidence at the outcome (RT60/A-18) layer.
- **V-01 minimum-compliance**: "we met NC-25" used to stop, when the sensitive populations may need quieter
  (the walk *tested* NC-20/NC-24 and found no standard support — an honest ceiling, not a denied aspiration).
- No V-03/V-05/V-09 surface.

## DAR (Design for Adaptable Readiness)

HVAC noise control is **hard to retrofit** (duct silencers, plant isolation, oversized ductwork are
mechanical/structural) — **high deferral penalty**. Provision at design stage; do not defer behind "we'll
quiet it later" (V-07). This is the *opposite* of A-02/ceiling panels (easily retrofitted).

## Cell-state — ✅ verifier-CONFIRMED and WRITTEN (cell 9013, migration `data_20260719023539`)

The separate verifier confirmed the ◐ grade and **resolved the metric flag** (see `A-08-verifier-verdict.md`):
ANSI/ASA S12.60 specifies **≤35 dBA (~NC-30)**, not NC-25 — "NC-25" is an **ASHRAE HVAC-component**
convention via a dBA→NC extrapolation, and **no ASHRAE acoustic ref is migrated (owed)**. Refinements folded
in and written to canonical `evidence_cell_state`:

```
cell_id=9013, item_code=A-08, population_code=ALL, design_scale=universal, state=provisional,
tier_basis='T4-6-only(regulatory_stratum_only)', regulatory_stratum_only=1, code_floor_only=0,
value_min=25, value_max=25, value_unit='NC', governing_refs=['REF-00563'], convergence_id=9013,
falsification_condition='NC-25 = ASHRAE HVAC-component convention [extrapolated-from(dBA→NC)]; ANSI S12.60
  (REF-00563) floor is ≤35 dBA (~NC-30, laxer, room-total); ASHRAE NC-25 ref unmigrated (owed). Never ●
  by more codes agreeing; only a T1/T2 NC/dBA study (or Co-1/Co-2) can. NC-20/24 tested, unsupported.'
```
The PMP walk row's "matches ANSI S12.60 exactly (gap=0)" is **metrically false** (ANSI=35 dBA≈NC-30) — caught
by this derivation, flagged for a walk-note correction on the hygiene track. Honest, non-inflated: a code
floor at NC-25, `extrapolated-from(dBA→NC)`, state=provisional. Grading throat now **9/93 items**.
