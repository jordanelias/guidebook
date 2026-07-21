# DR-2026-07-21 — Two-layer functional taxonomy: axes × profiles

- Status: **ACCEPTED — owner ratification "Ratify all", 2026-07-21.** Doctrine operative (functional-taxonomy.md v1.2 incl. §0.5); DB execution staged and gated per §9 — see `decisions/RATIFICATION-RECORD-2026-07-21.md` and `workplan/ratification-execution-register-2026-07-21.md`. Originally stated and did not execute
  (posture per `DR-2026-07-21-product-posture-thinking-tool-not-authority.md`).
- Version: **1.2 (2026-07-21)** — v1.1 amended after (a) an adversarial pass from a
  lived-experience standpoint, (b) an intensified pass from person-first and global
  non-English standpoints, and (c) reconciliation with canon this DR's v1.0 failed
  to read: `governance/armature_v4.md` (whose §§4.2–4.3/§5 two-layer architecture
  this taxonomy executes), `governance/population-taxonomy.md` (CANONICAL),
  `governance/mission-and-epistemics.md`, DR-2026-06-11-remove-colonial-role. The
  convergent re-derivation is evidence for the architecture; the failure to read
  first is recorded in the attestation. **v1.2 adds the irreducibility principle
  (§0.5)** — a governing preamble binding the whole taxonomy: every function is a
  spectrum along a spectrum, axes describe *specification-variation* not persons
  (armature §4.2), `population_axis_map` is a retrieval index not a portrait, measured
  function is inseparable from selfhood (ICF capacity/performance, Kawa, Capability
  conversion factors), and the person is the ground truth the specification serves.
  It operationalizes `held-tensions.md` T9.
- Doctrine: `governance/functional-taxonomy.md` v1.2 (irreducibility principle §0.5;
  dispositions, curation rules, gates). Staged schema:
  `working/taxonomy/staged_schema_functional_axes.sql`
  (outside the migration glob). Governed by `governance/held-tensions.md`
  (PROPOSED) — amendments annotated [T1]–[T8] therein.
- Affects (if ratified): population-layer semantics (via population-taxonomy §5's
  own change process); slug workflow (`serves_axes`); FDA skill §§1–2
  (regenerated); `evidence_population_match`; `db.py validate`; the questions-led
  entry surface's seed content (situations).

## Context

The population layer exists in three diverged representations (canonical 11+sub
codes; DB 22 flat codes; and the research-operations reality those feed). The
2026-07-21 audit verified operational failures the divergence produces: functions
named in canon (vestibular, in armature §5 and NEU/PCS prose) with zero curation
machinery — no b-codes, no slugs, no searches in 19 languages; evidence attached by
etiology rather than mechanism (MS under NEU); an axis living as a starved
population code (SENS, 1 item link); a skill vocabulary (ABI/ASD/LOW-VISION/
PCS-as-post-COVID) absent from the canonical table. Two adversarial passes then
established that v1.0's fix imported its own defects: deficit framing, Anglophone
gap-detection, diagnosis-keyed profiles, solo-user axes, dehumanizing record
vocabulary, and asymmetric burdens on newly visible categories.

## Decision (proposed)

Adopt the two-layer model as specified in `functional-taxonomy.md` v1.1:

1. **17 person-environment interaction axes** (Layer 1), ICF-anchored for
   findability, never as person-description; falsification conditions on *all*
   axes symmetrically; floor-level living, grid intermittency, and multi-script
   information demands named in the axis register.
2. **Profiles** (Layer 2) on the armature's mapping-confidence model
   (high/moderate/low/minimal-predictive), with: the emergence guarantee (profile
   and Co-1 content never reduced to axes; Co-1 = tier 1 = ● -eligible);
   diagnosis-optional membership as doctrine; the ICD-11 negative commitment;
   community- and language-deferential naming; dispositions realigned to canonical
   sub-codes (OFS/ME, NDV/AUT, NEU/PCS…); the PCS→PCS-TBI/LCOV split; `OAD`
   (older adults), `VES`, `LCOV`, CHD/LPA/EXH/BAR admissions; DBL retained
   first-class as a compound profile with canon's DBL ≠ VIS+DEAF rule preserved.
3. **Curation rules** with five attachment points — axes, profiles, items,
   **situations** (first-person, language-carrying episodes; the native Co-1
   home), and **operational access** (the maintenance/POE failure mode) — plus
   assisted/collective use-modes and a defined non-DOI intake path.
4. **Two standing gates before freeze:** a Co-1 review gate (provisional pending
   lived-experience review, in the form mission §Operational reality permits) and
   a non-English concept-validation gate (axes checked against native-alias
   machinery and already-searched non-English strata).

## Alternatives rejected

Status quo (operational invisibility persists); ICD-organized (encodes
disability=disease; cannot host identity profiles); flat function-only (destroys
non-decomposable corpora; subordinates Co-1 structurally); e-code item anchoring
(granularity far below item grain — retracted in-session); ignoring canon and
proposing a parallel taxonomy (v1.0's de facto position — corrected in v1.1 by
amending-by-proposal through population-taxonomy §5's process).

## Consequences if ratified

Curation acquires a selection principle and five attachment points; six previously
uncuratable functional domains (balance, information access, expressive
communication, arousal-safety, toileting-proximity, airborne exposure) gain
machinery; IntD information access stops being proxied (GAP-277); MH gains its
axis; the FDA↔DB↔canon vocabulary converges; the undiagnosed and the
never-certified are served by axis entry as a peer path; testimony and operational
reality become curatable as themselves. Costs: one staged migration + seeds; FDA
skill regeneration; 79-slug backfill; brief-harvest; the two gates' work. New
research queues behind the language debt per §8, whose equity cost is now stated
rather than elided.

## Explicitly not decided here

Public-realm scope · conflict precedence (parity stands) · Part 2 prose
restructure · armature amendment (integration notes live in `grounds.md` §R) ·
lived-experience review *structure* (mission §Operational reality governs) ·
`lang_jur_map` criteria (owner-defined per DR-2026-06-11).

## Ratification checklist (owner)

0. Ratify **the irreducibility principle (§0.5)** as the governing preamble — the
   axes are a retrieval index over specification-variation, never a portrait of a
   person; the person is the ground truth the taxonomy serves. (Listed first because
   it conditions how every item below is read.)
1. Ratify the 17-axis register — or amend membership/granularity.
2. Ratify dispositions incl. flagged judgment calls: DEAF dual disposition
   (armature's open question, answered as axis-infrastructure + identity-profile
   custody of d340/DeafSpace); EPI→AX-SPR situational; DBL structural placement.
3. Confirm the PCS split (PCS-TBI / LCOV) and canonical-sub-code realignment.
4. Confirm admissions: OAD, VES, LCOV, CHD/LPA/EXH/BAR.
5. Confirm the two gates (Co-1 review; non-English validation) as blocking
   pre-freeze, and the situations + operational-access attachment points.
6. **R6:** transfer capacity — folded into AX-WHM, or split per armature §5?
7. **R7:** cognitive granularity — two axes (COG-O/COG-L) or armature's four
   sub-dimensions?
8. **R8:** respiratory/oxygen — decomposed (v1.0 position) or a standalone axis
   (armature position)? Both cases are recorded in §2.3.
9. Queue order: does new-axis research remain behind the language debt (§8), or
   reorder?
10. On ratification: promote staged SQL; execute §9 steps 3–8.
