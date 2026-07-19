# Batch 1 · A-02 — Acoustic Ceiling Panels (NRC ≥ …) — agonist derivation

*Slug `room-acoustic-performance`. Grounded in `data/guidebook.db` (7 PMP walks, linked sources). Pending
the separate verifier (`A-02-verifier-verdict.md`). Nothing written to canonical `evidence_cell_state`
until the verifier confirms.*

## The honest headline: A-02's number is **code-derived (◐), not evidence-derived (●)**

The item is a **TECHNIQUE-layer** provision (S5): A-18's `RT60 ≤ 0.3–0.55 s` is the performance **TARGET**;
acoustic ceiling panels at a given NRC are a **TECHNIQUE** to achieve it. The strict-termination PMP walk
(population **ALL** only) converged on **NRC ≥ 0.90** (empirical ceiling ≈ 0.935; STOP at δ_min = 0.005) —
**and the only reference that passed strict-termination is `REF-00563` = ANSI/ASA S12.60 S5.3 ("ceiling
minimum NRC 0.90"), a Tier-4 code.** No Tier-1/2 study in the corpus establishes an NRC panel threshold;
the T1 acoustic evidence (Iglehart, Neuman, Wroblewski, Prodi…) establishes RT60 / speech-perception
**outcomes**, which anchor A-18 — not the NRC number here.

**Therefore, per doctrine (T4–6 walled off; converge ≠ evidence), the NRC value grades ◐ (policy/code-floor),
not ●.** Many national standards specifying an NRC minimum is *code convergence*, not evidence. A naive
grader, seeing "NRC ≥ 0.90 in ANSI + a dozen linked T1 acoustic studies," would stamp this ● — that would be
convergence-laundering. It is not.

## Derivation by mode (S8)

| mode | value | grade | basis / provenance-strength |
|---|---|---|---|
| **Universal** (top-down floor) | **NRC ≥ 0.90**, empirical ceiling ≈ 0.935 | **◐** code-floor | ANSI S12.60 S5.3 (REF-00563, T4). `direct` from the code; **`absent`** at the evidence layer — no T1 NRC threshold exists |
| **Population** | — | — | **only ALL was walked**; no population-specific NRC evidence. Population-mode NRC = `absent` (stated, not invented) |
| **Person** (OT within range) | use ≥ 0.90 tiles; marginal individuation | n/a | NRC is a fixed material spec; `items.pmp_delta_min` is NULL (direction 'up') → no meaningful person delta |

**Flag — item spec vs floor:** the item name reads "NRC ≥ 0.85", which is **below** the ANSI 0.90 code floor.
That discrepancy is surfaced, not silently corrected — the render should show ≥ 0.90 (floor) with the 0.85
origin noted for review.

## Contested technique (S5 — a technique can backfire)

**REF-00580 (Amlani 2016, Tier-1): "Negative effect of acoustic panels on listening effort."** Adding
absorption is **not** monotonically better — over-damping can raise listening effort in some conditions. So
A-02 is a technique with a **documented backfire mode**, and best-practice voice must carry that caveat
rather than "more NRC = better." This is a ● Tier-1 signal — but it *complicates* the technique, it does not
set the NRC number.

## DAR (Design for Adaptable Readiness)

Ceiling treatment is highly retrofittable: specify a **demountable ceiling grid that accepts higher-NRC
tiles later** (low deferral penalty). Provision now; do not defer the acoustic function behind it (V-07).

## Ethics screen (A10) — brief

- **V-06 evidence-tier laundering** — the live risk here: presenting the NRC code convergence as the evidence
  basis. Foreclosed by grading the number ◐ and keeping the ● evidence at the RT60-outcome layer.
- **V-01 minimum-compliance** — "we met NRC 0.90" used to stop there; mitigated by surfacing the empirical
  ceiling (0.935) and the RT60 outcome the panels serve.
- No V-03/V-05/V-09 surface (physical material spec; no per-person data; population not proxied).

## Proposed cell-state (HELD — verifier must confirm before write)

```
item_code=A-02, population_code=ALL, design_scale=universal, state=provisional,
tier_basis='T4-6-only(code-floor)', value_min=0.90, value_max=0.935, value_unit='NRC',
code_floor_only=1, regulatory_stratum_only=1, governing_refs=['REF-00563'],
falsification_condition='A Tier-1/2 study establishing an NRC panel threshold (which would move this
  off code-floor-only and permit a ● grade), or evidence that NRC ≥0.90 raises listening effort net-negative
  (Amlani direction) in occupied learning spaces.'
```
Note: `state=provisional` and `code_floor_only=1` — this cell is **honestly a code floor**, not a graded
best-practice value. That is the correct, non-inflated outcome.
