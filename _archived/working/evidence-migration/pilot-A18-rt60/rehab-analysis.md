# Pilot — A-18 (RT60 in Occupied Learning and Listening Spaces)

*Slug: `room-acoustic-performance` · `evidence_state`: RETRACTED-PRE-REHAB · citation-mining ✓ ·
supersession ✓ · co1 ✗ · pico ✗ · jurisdictions-searched ✗.*

> **This artifact was corrected after an independent adversarial verifier refuted parts of the first
> draft** (see `verifier-verdict.md`). The corrections *strengthened* the finding — the DB is more
> rehabilitated, and more correct, than the first pass claimed. Every figure below is read from
> `data/guidebook.db` (grounded) or retrieved with a cited URL.

---

## The headline (corrected): the substrate is deep — the debt is flags, Co-1, and flagged errors

A-18's `bpc_metadata` flags say `RETRACTED-PRE-REHAB`, co1 0, pico 0, jurisdictions-searched 0 — which reads
like "barely started." **That is misleading.** Underneath, the July 2026 pilot sessions built a deep,
rigorous rehabilitation substrate:

- **4 population-coded, evidence-graded cell-states** (`evidence_cell_state`): DEAF 0.3 s (stated, T1),
  ALL 0.55–0.57 s (stated, T1), DEM 0.5 s (provisional, T2), AUT 0.4 s (provisional, T3) — all
  `code_floor_only=0` (● evidence-derived).
- **8 jurisdiction-tagged code-threshold extractions** (`source_value_extractions`) with echo-provenance:
  ANSI 0.6 s (ALL) / **0.3 s (DEAF, Footnote e)**, BB93 0.6–0.8 s (UK), DIN 0.4–0.8 s (DE), UNI 0.5 s (IT),
  AS/NZS 0.4–0.6 s (AU/NZ) — each marked `echo_of` a committee/evidence root, **not** counted as
  independent evidence.
- **13 PMP derivation walks** (`spec_value_probes`) with strict-termination logic, per population, recording
  exactly where a value passes (DEAF 0.3 s, ALL 0.55 s) and where it fails by design (DEM, AUT conjectures).
- **Convergence assessments** per cell (`convergence_assessment`), all correctly `single_axis` (clinical).

So the migration debt for A-18 is **not the value derivation** — that is rigorous and, importantly, already
handles *convergence ≠ evidence* correctly (next section). The genuine remaining debt is narrower:

| real gap | evidence |
|---|---|
| **Recording flags don't reflect the substrate** | `co1/pico/jurisdictions_searched = 0`, `evidence_state=RETRACTED-PRE-REHAB` despite extensive extraction/PMP/cell-state work — surface/flag debt |
| **Co-1 lived experience genuinely absent** | all 4 `convergence_assessment` rows `single_axis`, `co1_sources=[]`; `co1_pass_count=0` |
| **DB-flagged data errors** — ✅ **RESOLVED** (migration `data_20260718071505`) | elab_id=6 mis-cited Devos 2019 as **REF-00571** (*Kotloski 2020, a genetics paper*) → re-pointed to real Devos **REF-00735**. **Four ANSI-2010 records** REF-00326/335/**563**/604 → consolidated onto canonical **REF-00563** (FKs re-pointed, dups marked `DUPLICATE-OF`, reversible) |
| **Person/OT cell + DAR layer** | no `person`-scale cell (though `items.pmp_delta_min=0.05 down` encodes the person adjustment); no DAR provisioning recorded |

## Convergence ≠ evidence — the DB does this correctly (my first draft did not)

The first draft claimed: *"the ANSI 0.6 s code-floor is ~2× laxer than the 0.3 s T1 evidence for
hearing-impaired children — build to code and you fail them (V-01)."* **The verifier refuted this, and it
is wrong**, because:

- **ANSI/ASA S12.60 Footnote e itself specifies RT60 ≤ 0.3 s for children with hearing impairment** (≤283 m³).
  The DB records this (`source_value_extractions` REF-00563, pop=DEAF, 0.3 s) with `echo_of` = *"ANSI Footnote
  e adopts 0.3 s from the Iglehart working-group research … a standards echo, not an independent root."*
  So for HI children the code **converges with** the evidence — it does not floor them at 0.6 s.
- The 0.6 s figure is ANSI's **general (typical-hearing) minimum**, and it is **unoccupied/furnished**; A-18
  is an **occupied** target, and the DB's general value (0.55 s, Prodi 2022 occupied dose-response) is
  already on the correct basis.

**The correct, grounded reading:** the DB keeps the strata separate exactly as doctrine requires — the
committee/code values are tagged `echo_of` and never counted as independent evidence; the ● best-practice
values rest on the T1 studies. The residual *ethics* point is a **susceptibility, not an instance** (see
`ethics-screen.md`): if a designer applied the code's **general** 0.6 s minimum to an HI space while ignoring
ANSI's own Footnote-e 0.3 s provision, that would be minimum-compliance misuse — but the code's own
population provision already guards against it.

## Value derivation — three modes, both directions, DAR (S8), as it actually stands

- **Universal (top-down floor):** RT60 ≤ **0.55–0.57 s**, typical-hearing, ● T1 (Prodi 2022, Neuman 2010).
  Provenance-strength: `direct`.
- **Population (evidence range):** DEAF ≤ **0.3 s** ● T1 (`direct`, strict-termination PASS on Iglehart);
  DEM ≤ 0.5 s ◑ T2 and AUT ≤ 0.4 s ◑ T3 — both **`inadequate`/conjecture** (PMP strict-termination FAIL,
  recorded as designed; no Tier-1 dementia dose-response, no autism-distinct quantified target).
- **Person (bottom-up, OT within range):** `items.pmp_delta_min=0.05 (down)` — OT tightens the population
  value by up to 0.05 s for greater individual need. `extrapolated-from(population range + PMP delta)`; not
  yet a `person`-scale cell — a determination is owed.
- **DAR:** acoustic absorption is highly retrofittable; provision ceiling grid + wall blocking now. Not
  recorded — venture as an approach.
- **Code-floor (◐, walled off):** ANSI 0.6 s / DIN 0.4–0.8 s / BB93 0.6–0.8 s / UNI 0.5 s / AS-NZS 0.4–0.6 s
  — present in `source_value_extractions`, correctly `echo_of`, shown as a floor beside the evidence, never
  as the anchor. (Note: the range reaches 0.8 s, so "codes converge on 0.4–0.6 s" would understate — the
  DB's own phrasing is "agree near 0.6 s.")

**TECHNIQUE layer:** porous absorption (ceiling NRC ≥0.85 A-02; fabric panels NRC ≥0.70 A-06), avoid
parallel hard surfaces (A-07) — graded under their own items.
