# DR-2026-07-12: Evidence-architecture unification — proposed resolution

- Status: **PROPOSED — pending owner ratification**
- Date: 2026-07-12
- Prepared by: Claude, at the owner's request to resolve the recurring evidence-hierarchy × design-mode × audience question with maximum effort. **Not owner-ratified.** Every item below is a recommendation for owner review; items are separately ratifiable.
- Creates: `governance/evidence-architecture.md` (PROPOSED → CANONICAL on ratification)
- Affects (if ratified): `governance/mission-and-epistemics.md`, `governance/evidence-methodology.md`, `governance/audience-priority.md`, `governance/armature_v4.md`, `schemas/directness.py`, `scripts/migrations/026_reconcile_evidence_cell_state.sql` (follow-on migration for `regulatory_stratum_only`), `scripts/validate_evidence_state.py`, `references/methodology-evidence-hierarchy-mapping.md`
- Related: `decisions/DR-2026-05-29-evidence-hierarchy-reconciliation.md` (PROPOSED), `decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md` (PROPOSED), `decisions/DR-2026-07-12-tier3-stated-threshold.md` (PROPOSED), `decisions/RATIFICATION-PACKAGE-2026-07-12.md`

## Context

The owner has repeatedly encountered, and once shelved the project over, one question: how can an evidence hierarchy dynamically weight evidence by design mode (universal / population / person) and present per user type (disabled person, designer, policymaker, advocate) without compromising intellectual integrity?

Maximum-effort review (this session) found the question ~80% answered by existing doctrine — decision D-D (`evidence-methodology.md` §§1.4–1.7), the role layer (`armature_v4.md` §4.5), the audience structure (`audience-priority.md`), and the weighting-profile design (`workplan/best-practices-assessment-system.md` §5) — but the answer was (a) scattered across six-plus documents with no unifying statement, (b) obscured by a vocabulary collision in which "Tier 1/Tier 2" name design modes in `mission-and-epistemics.md` commitment 4 and evidence tiers everywhere else, plus a third "Mode P/Mode S" vocabulary, (c) un-ratified (four keystone DRs PROPOSED), and (d) unbuilt (`evidence_cell_state` = 0 rows). Adversarial review then found six genuine gaps at the edges of the existing resolution, two of them verified bugs in `schemas/directness.py` and one a latent doctrine–code contradiction.

## Proposed decision

Adopt `governance/evidence-architecture.md` as the CANONICAL single entry point to the evidence architecture (an index-and-synthesis: existing doctrine restated once with citations; new doctrine only in the flagged items below). Ratify the following items — **each separately answerable**:

### Item G1 — Close the convergence-laundering channel (deepest integrity risk)

**Problem.** `evidence-methodology.md` §2.3 allows a cell to reach `provisional` on T4–6 convergence alone, and §3.4 supplies rendering language for it, while `tier-system.md` §3 and `schemas/directness.py` (NON-ANCHORING) forbid exactly that stratum from anchoring best-practice claims. The `code_floor_only` flag (migration 026) covers only the T6-only case, so a T4/T5-only cell passes `v_best_practice`; the policymaker weighting profile up-weights exactly this stratum. This is the mechanism by which a policymaker rendering could launder code-convergence into best practice.

**Recommendation.** (a) **Scale-tagging:** every determination is tagged with the design scale its claim speaks to; T4–6-only determinations are Universal-Mode regulatory determinations, never rendered as best practice in any register. (b) **Flag extension:** `regulatory_stratum_only` (T4–6-only) supersedes/extends `code_floor_only` (T6-only); `v_best_practice` excludes it. (c) **Re-graining rule:** a T4/T5 source escapes GRAIN_CODE (→ GRAIN_AGGREGATE) only when its own evidence basis is documented traceable to T1/T2, provenance recorded — operationalizing the "if the standard itself rests on T1/T2 evidence" clause already in `tier-system.md` §1.

**Alternatives considered.** Leave §2.3 as-is and rely on the confidence flag (rejected: editorial discouragement, not mechanical prevention — the failure mode tier-system.md names would remain reachable); forbid T4–6-only `provisional` entirely (rejected: the regulatory-floor claim is legitimate and useful; the fix is labeling it as what it is, not deleting it).

**Consequences.** Follow-on migration adding `regulatory_stratum_only`; `validate_evidence_state.py` check extended from T6-only to T4–6-only; `evidence-methodology.md` §§2.3/3.4 prose amended post-ratification (execution section below); policymaker register map row carries the anti-laundering language.

### Item G2 — Distinguish NOT_ASSESSED from not-applicable in directness consolidation

**Problem (verified bug).** `schemas/directness.py` `consolidate()` line 225: `pop_full = population_directness in (POP_EXACT, None)` — a never-assessed population dimension grades as fully direct. Only 27/640 sources have `evidence_population_match` rows; at backfill scale ~96% of sources would silently condition as DIRECT on an unassessed dimension.

**Recommendation.** The engine distinguishes NOT_ASSESSED (dimension applies, no assessment exists) from not-applicable (genuinely inapplicable). NOT_ASSESSED caps consolidation at DOWN-WEIGHTED and flags the source. Implemented additively (new engine-side path under `rule_version="pilot-1"`; `consolidate()` signature untouched pre-ratification).

**Alternatives considered.** Treat None as blocking (rejected: breaks legitimate not-applicable cases §1.7 intends); backfill all 640 assessments first (rejected: months of work gating a structural fix; the cap is honest in the interim).

### Item G3 — Co-1 grain follows `co1_source_type`

**Problem (verified).** `GRAIN_FROM_EVIDENCE_TYPE` maps `co1 → GRAIN_SPECIFIC` wholesale. A DPO position paper would grade DIRECT at Person Mode — contradicting `co1-operational.md` (population Co-1 does not override individual assessment) — and DOWN-WEIGHTED at Population Mode, which is backwards for community-consensus evidence.

**Recommendation.** Grain derives from `co1_source_type`: `dpo_research`/`advocacy_position` → aggregate; `academic_narrative` → specific; `peer_reviewed_literature`/`validated_tool` → per the study's own design, recorded per source. Ethically load-bearing: population-grain speech never stands in for an individual, and individual narratives are not inflated into community consensus.

### Item G4 — State the asymmetry principle (declarative; no behavior change)

**Recommendation.** Adopt the positive formulation unifying D-D + `co1-operational.md`'s Person-scale rule: *at each design scale, the anchoring authority is the entity whose grain is that scale — the code at Universal, the aggregate evidence ladder at Population, the person themselves (in OT-supported co-design) at Person.* Codifies what is already ratified, scattered; `evidence-architecture.md` §3 is its home.

### Item G5 — Advocacy-brief as a use-pattern, not a fifth audience

**Problem.** "Advocate" (named in the owner's framing of the recurring question) is not an audience in canonical governance; `armature_v4.md` merges disabled person / advocate.

**Recommendation.** Ratify advocacy-brief as a use-pattern within the disabled-person primary audience (extendable to carers, DPO staff): emphasis = code-vs-best-practice delta + rights framing + citable evidence strength. Amends `audience-priority.md` (use-pattern table) post-ratification; no change to the four-audience structure or priority rules.

**Alternative considered.** Fifth audience (rejected: content needs are the policymaker-rationale pattern with reversed valence; a fifth audience would force re-litigating every conflict-resolution rule for marginal gain, and the advocate's priority claim is stronger as a member of a primary audience than as a new secondary one).

### Item G6 — Grain derives from (evidence_type × tier), not evidence_type alone

**Problem (verified latent contradiction).** `standard_eb` spans T2 named-organisation evidence-based standards and T4 international standards. The type-only default (`standard_eb → GRAIN_CODE`) makes T2 DPO/professional-body standards NON-ANCHORING at Population Mode, contradicting `evidence-methodology.md` §1.6 which lists Tier 2 among the anchoring strata.

**Recommendation.** `standard_eb` at T2 → GRAIN_AGGREGATE; at T4/T5 → GRAIN_CODE (unless re-grained per G1). Grain assignment becomes a function of the (type, tier) pair; implemented additively in the engine.

### Item V — Vocabulary normalization

**Recommendation.** Universal Mode / Population Mode / Person Mode become the sole canonical design-scale names ("Tier N" reserved for the evidence ladder; "Mode P/Mode S" deprecated). The collision is the mechanical reason the architecture kept reading as self-contradictory. Execution section lists the file-by-file edits; applied only post-ratification.

### Item R — Claim-strength register map + integrity invariants I1–I5

**Recommendation.** Adopt the register map (claim-strength language per determination tuple per register, a finite versioned lookup) and invariants I1–I5 (`evidence-architecture.md` §6) as the testable form of armature v4's "role does not change the underlying data," enforced by `scripts/audit/register_integrity_check.py` under mutation-test discipline.

## Impact analysis — project shape in all directions

A full-repo impact sweep (code / database / book / site / skills / governance) was run this session; the complete map is `decisions/DR-2026-07-12-evidence-architecture-unification-impact-appendix.md`. Summary of directions: **code** — `schemas/directness.py` gains additive per-`rule_version` paths (G1/G2/G3/G6); `validate_evidence_state.py` check extended (G1b); generators consume the register map when audience rendering ships. **Database** — one follow-on migration (`regulatory_stratum_only`; `weighting_profile` seeding); no change to applied history. **Book (`parts/v10/`)** — vocabulary-normalization edits (Item V execution list); any prose stating T4–6 convergence as best practice is a defect on current doctrine already, listed in the appendix. **Site** — population/spec page generators unaffected until they render determinations; then bound by I1–I5. **Skills** — hierarchy-teaching skills (e.g., `guidebook-auditor_SKILL.md`) amended in lock-step per the tier-system.md §6 precedent. **Governance** — four prose amendments listed below; no ratified doctrine is contradicted, three PROPOSED DRs are extended compatibly.

## Execution section — post-ratification edits (none performed pre-ratification)

1. `governance/mission-and-epistemics.md` commitment 4 table: rename design-mode rows to Universal/Population/Person Mode; commitment 7 prose likewise.
2. `governance/evidence-methodology.md`: §2.3 add scale-tagging + `regulatory_stratum_only` language (G1); §3.4 voice line gains the mandatory regulatory-stratum disclaimer; §4 "Mode P/Mode S" renamed.
3. `governance/audience-priority.md`: add advocacy-brief use-pattern row under disabled people (G5); "Tier 1 range" → "Population-Mode range" in OT rows.
4. `governance/armature_v4.md` §4.5/§4.6: "Disabled person / advocate" row annotated with the advocacy-brief use-pattern; "Universal Mode / 1 / 2" and "Mode S handoff" renamed.
5. `schemas/directness.py`: promote the pilot's G1/G2/G3/G6 paths from engine-side (`rule_version="pilot-1"`) to module defaults under a new `rule_version`; update GRAIN_FROM_EVIDENCE_TYPE to the (type × tier) function.
6. Follow-on migration 027: `regulatory_stratum_only` column + `v_best_practice` exclusion + `weighting_profile` seed rows for the four audience use-patterns + advocacy-brief.
7. `scripts/validate_evidence_state.py`: extend the code-floor check to `regulatory_stratum_only`.
8. Skills sweep per impact appendix — priority order: `cell-curator` (still states the superseded T3-alone⇒stated threshold), `voice-style` (register map lands here), `item-specification-writer` ("● = Tier 1–6" conflicts with the ●/◐/○ split), `guidebook-auditor`, `literature-review-planner` + `supersession-audit` (OLD ladder).
9. `references/project-standards.md` — the standing-rules register still states the superseded ladder as RULEs (L17/L26/L35) + 16 Mode P/S uses; **highest-risk single file** (feeds `doctrine_recheck.py` and every agent session).
10. `schemas/evidence_state.py` L108 docstring (OLD stated threshold) + `governance/pre-stage-a-decisions.md` L49/L81 (same); `architecture/schema-spec.md` L78–98 (wrong `co1_source_type` enum, phantom `co1-collaborator` type — G3 hard conflict); `references/global-reference-registry.md` hybrid "Co-1/N" labels.
11. Item V's one data-level migration: `conflicts.status` CHECK includes `MODE-S-ONLY` — SQLite CHECK requires a coordinated table rebuild + `schemas/conflict.py` + `scripts/validate_conflict{,s}.py` + `cross-population-conflict-mapper_SKILL.md` in the same change. Legacy replay paths (`scripts/convert/*`, `scripts/db/*`, `scripts/migrations/session_*`) are NOT edited — marked deprecated.
12. Same-change hygiene: update doctrine SHA 3da73bd pins (`schemas/directness.py`, `schemas/tier_derivation.py`, `schemas/evidence_state.py`, `skills/multilingual-research_SKILL.md`, `workplan/phase-e-execution-plan-v1.md`), `doctrine_recheck.py` snapshots, and `tools/regenerate_vetting_surface.py` per-tier blurbs — otherwise drift checks fail or stale doctrine auto-republishes.
13. Reconcile `schemas/enums.PopulationCode` with the live `populations` table (pilot-surfaced drift: SCI/UPL/AUT/ADHD etc. FK-valid but absent from the enum).

## Verification performed this session

- Matrix–code consistency: `scale_directness()` swept over all grain × scale combinations; output matches `evidence-architecture.md` §3/§10 exactly (including the generalizes-beyond-measured branch).
- G2/G3/G6 verified by direct code read (`schemas/directness.py` lines 76–85, 225) and cross-read against `evidence-methodology.md` §1.6, `co1-operational.md`, `tier-system.md` §§1–2.
- Pilot demonstration (working-copy DB only; canonical DB untouched): see `working/pilot/PILOT-MANIFEST.md` — determinations for cells covering every doctrinal branch, rendered in all registers, invariants I1–I5 mechanically checked under mutation-test discipline.

## What would make this ACCEPTED

Owner review with per-item answers (a one-line reply per item suffices; format in `decisions/RATIFICATION-PACKAGE-2026-07-12.md`). Items are independent except: G1(c) presupposes G6 (re-graining is expressed over the type × tier function); Item R presupposes G1 (row 3 of the map names `regulatory_stratum_only`).

## Revision history

- v1: drafted after two-sweep exploration + independent max-effort design review; G1–G6 verified against code and doctrine as cited above.
- v1.1 (same day): (a) full-repo impact sweep completed → `…-impact-appendix.md`; execution section extended with items 8–13 (project-standards.md, stated-threshold triangle, MODE-S-ONLY migration, SHA-pin hygiene, PopulationCode drift). (b) Pilot executed end-to-end on the working-copy DB: 7 cells, deterministic (byte-identical double run), validator clean, 6/6 validator mutations + 4/4 register-invariant mutations fired. (c) **Self-caught defect via I3's strictness:** the first register-map draft used "best practice" inside negations on regulatory-stratum rows; the checker flagged it; wording corrected in renderer + `evidence-architecture.md` §6 — I3 is deliberately a total phrase ban. Adversarial review of the full deliverable set (Phase 4) will append findings as v2 if any survive.
