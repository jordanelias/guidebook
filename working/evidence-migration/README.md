# Evidence Migration & Rehabilitation

**Status:** pilot in progress · **Branch:** `claude/project-status-next-steps-wgatjq` (restarted off `main` @ fcc366e) · **Started:** 2026-07-18

This directory is the working deliverable for finishing the evidence migration — taking each provision
from a retracted stub to a rehabilitated, multimodally-sourced, equity-searched, ethically-screened,
honestly-graded provision. The full plan (constraints S1–S8, the per-slug pipeline, the equity/multimodal/
ethics gates) lives at `/root/.claude/plans/delegated-pondering-pine.md`.

## What the migration debt is (verified against `data/guidebook.db`, 2026-07-18)

The **source records** migrated (640 rows, 635 VERIFIED). The **layers on top of them mostly did not**:

| layer | signal | state |
|---|---|---|
| Synthesis | `bpc_metadata.evidence_state` | **68/82 RETRACTED-PRE-REHAB**, 13 null, 1 methodology |
| Rehab flags | pico / co1 / juris / citation-mine / supersession | **0 / 0 / 0 / 6 / 6** of 82 |
| Grading | `evidence_cell_state` | **11 cells / 7 of 93 items**; **person-scale = 0** |
| Equity | `lang_detected`, jurisdiction | ~6× English by tag (but see the pilot — the tag is unreliable) |
| Multimodal | `co1_pass_count`, co1 sources | 0/82 passed; 29 co1 sources linked but **26/29 English, 21/29 US+UK** |

## Transparency model (per the project ethos, reaffirmed by the owner)

We **make available all jurisdictions / international standards / precedents** searched; we **admit when we
are extrapolating** evidence to venture a suggestion (labeled `extrapolated-from(X)`, basis shown); and we
**admit when our evidence base is thin** (`inadequate`) or **absent** (searched, not found). We do **not**
present fabrications as an exhibit — the anti-fabrication gate rejects non-resolving citations internally as
quality control. Every value carries its genealogy and a **provenance-strength** tag: `direct` /
`inadequate` / `extrapolated-from(X)` / `absent`.

## Contents

- `registry-reconciliation.md` — L0: the 46 well-formed registry/audit-only refs classified (un-migrated
  evidence vs cruft), the REF-00181 live hole, jurisdiction hygiene.
- `pilot-A18-rt60/` — the first pilot cell (A-18, RT60) walked through the pipeline with a **separate
  adversarial verifier**. Demonstrates value-derivation across three modes, *converge ≠ evidence*, the
  coverage matrix, and the ethics screen — on real canonical data.
- `checkpoints/` — per-slug stage checkpoints (suspension-resilient resume).
- `db/migrations/` — proposed canonical writes (migration-based, reviewable; nothing promoted to `stated`
  without verifier confirmation).

## The headline finding so far (corrected after adversarial verification)

**The substrate is deeper than the flags admit; the debt is flags, Co-1, and flagged errors.** A-18's
`bpc_metadata` flags read "barely started" (`RETRACTED-PRE-REHAB`, co1/pico/juris = 0), but underneath, the
July 2026 sessions built a rigorous rehabilitation substrate: 4 population-coded evidence-graded cell-states,
8 jurisdiction-tagged code-threshold extractions with `echo_of` provenance (converge≠evidence handled
*correctly* — incl. ANSI Footnote-e 0.3 s for HI children marked as an echo of the evidence), 13 PMP
derivation walks, and convergence assessments. So the migration debt is **not** the value or the code-floor
— it is (1) recording flags that don't reflect the substrate, (2) **Co-1 lived experience genuinely absent**
(all cells single-axis clinical), and (3) real DB-flagged data errors (a Devos-2019/REF-00571 mislink; four
duplicate ANSI records).

An independent verifier refuted three claims in the first draft of this pilot (code values "un-migrated",
`population_code` "null", a "2× ANSI floor / V-01 instance"); all are corrected in `pilot-A18-rt60/` and
recorded in `verifier-verdict.md`. **The correction is the point** — it is why the pipeline runs a separate
guilty-until-proven verifier, and why the plan now opens with a substrate inventory (below).
