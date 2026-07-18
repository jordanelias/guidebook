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

## The headline finding so far

**Grading ≠ rehabilitation.** A-18's *value derivation* is already excellent (four evidence-graded
cell-state rows, ● Tier-1), yet its slug is still `RETRACTED-PRE-REHAB` because the **rehabilitation layers
are missing**: no Person/OT mode, no Co-1 lived experience, no walled-off code-floor, no DAR layer, null
`population_code`s, and no recorded jurisdiction/language coverage. The migration debt is concentrated in
*those* layers, not in the value itself. See `pilot-A18-rt60/`.
