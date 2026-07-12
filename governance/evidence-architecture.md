# Evidence Architecture — the unified statement
**Status:** PROPOSED — pending owner ratification via `decisions/DR-2026-07-12-evidence-architecture-unification.md`. On ratification this document becomes CANONICAL as the single entry point to the evidence architecture; until then every already-decided element it restates remains governed by its cited source document.
**Created:** 2026-07-12
**Character:** Index-and-synthesis. This document states each already-decided element **once**, with a citation to its canonical home; it introduces new doctrine **only** in passages flagged `[NEW — DR-gated]`, each of which is a separately ratifiable item (G1–G6) in the unification DR. It is deliberately not a seventh scattered restatement: where this document and a cited source ever diverge, the cited source governs until the divergence is reconciled by DR.
**Doctrinal basis:** `governance/mission-and-epistemics.md` · `governance/tier-system.md` · `governance/evidence-methodology.md` · `governance/audience-priority.md` · `governance/armature_v4.md` §4.5 · `governance/co1-operational.md` · `decisions/DR-2026-05-29-evidence-hierarchy-reconciliation.md` · `decisions/DR-2026-07-12-*.md` · `schemas/directness.py` · `schemas/tier_derivation.py`

---

## 1. Why this document exists

The project has repeatedly re-encountered one question as if unresolved: *how can a single evidence hierarchy dynamically weight evidence by design mode (universal / population / person), and present differently per audience, without compromising intellectual integrity?*

The answer exists. It was decided incrementally — T-03/T-04 (Stage 0.5), A5/A6 (April 2026), the owner directive of 2026-05-25, decision D-D and DR-2026-05-29 (May 2026), the armature v4 role layer, and the Stage 2.2 directness build — but it was never stated in one place, and three colliding vocabularies made the fragments look inconsistent when they were not (§7). This document is the one place.

**The scatter map** — where each element canonically lives:

| Element | Canonical home |
|---|---|
| The 7-tier ladder + Co-1/Co-2 co-primacy | `governance/tier-system.md` §1; `governance/mission-and-epistemics.md` §Epistemic commitments |
| sr_meta at T2 (owner directive "t2>t3 this is enshrined") | `governance/tier-system.md` §2; `decisions/DR-2026-05-29-evidence-hierarchy-reconciliation.md` |
| Best-practice ≠ convergence (T4–6 walled off from best-practice anchoring) | `governance/tier-system.md` §3 |
| The three design modes | `governance/mission-and-epistemics.md` §Doctrinal commitment 4 |
| Orthogonal axes of coverage | `governance/mission-and-epistemics.md` §Two orthogonal axes; `governance/evidence-methodology.md` §1.4 |
| Scale-conditioned (mode-asymmetric) weighting — decision D-D | `governance/evidence-methodology.md` §1.6 |
| Directness as grain-matching conditioning layer | `governance/evidence-methodology.md` §1.7; `schemas/directness.py` |
| Four-state determination machine (`stated`/`provisional`/`pending`/`not_applicable`) | `governance/evidence-methodology.md` §2 |
| Cell identity + determination storage | `decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md`; `scripts/migrations/026_reconcile_evidence_cell_state.sql` |
| Audience priority (two primary, two secondary) | `governance/audience-priority.md` |
| Role presentation layer ("role does not change the underlying data") | `governance/armature_v4.md` §4.5 |
| Co-1 operational requirements | `governance/co1-operational.md` |
| Tier-3-alone `stated` threshold | `decisions/DR-2026-07-12-tier3-stated-threshold.md` |
| Academic-methodology correspondence (GRADE/JBI/SIGN) | `references/methodology-evidence-hierarchy-mapping.md` (v2) |

---

## 2. One ladder

There is exactly **one** evidence hierarchy: seven tiers with two co-primary community-knowledge tracks (`governance/tier-system.md` §1). Its governing principle: **tier reflects what kind of claim a source can anchor, not how good the source is.**

- **T1** — primary research with intervention-level or biomechanical control; OT-prioritized, not OT-exclusive (decision D-E).
- **Co-1** — disability-led lived-experience evidence (CRPD Art. 4.3), **co-primary with T1**: primary-research evidence and lived-experience evidence are non-substitutable on different claim types. T1 anchors claims that turn on mechanism; Co-1 anchors claims that turn on user-stated preference, dignity, autonomy, self-determined accommodation.
- **T2** — synthesis: (a) systematic reviews / meta-analyses; (b) named-organisation evidence-based standards. **Co-2** — OT professional-body CPGs, co-primary with T2.
- **T3** — lower-control primary clinical + grey-literature primary research; supporting, rarely sole basis (threshold for T3-alone `stated`: `decisions/DR-2026-07-12-tier3-stated-threshold.md`).
- **T4–T6** — the **regulatory stratum**: international standards, national beyond-code frameworks, statutory codes. Valid for code-baseline claims and jurisdiction tracking. **They do not anchor best-practice claims** (`tier-system.md` §3): convergence of codes is convergence-not-evidence — the jurisdictions could all be wrong together, or all be copying one unevidenced ancestor.

The ladder never re-ranks. Nothing in this architecture — no design mode, no audience, no weighting profile — reorders these tiers. What varies is *conditioning* (§4) and *emphasis* (§6), never rank.

## 3. Three modes, one asymmetry principle

The three design modes (`mission-and-epistemics.md` commitment 4, names normalized per §7):

| Mode | Function | Resolution |
|---|---|---|
| **Universal Mode** | Universal design / code compliance — the floor, not an aspiration | Population-agnostic; fixed values |
| **Population Mode** | Population-informed inclusive design | Ranges; median as default |
| **Person Mode** | Person-specific co-design | OT assessment resolves position within the Population-Mode range |

Evidence tier and design mode are **orthogonal axes of coverage** — both always consulted, neither determining the other (`evidence-methodology.md` §1.4). But orthogonality is *scale-conditioned* (decision D-D, §1.6): the ladder is consulted at every scale while its adjudicating force is asymmetric.

**The asymmetry principle** `[NEW — DR-gated: G4]` — the single sentence that unifies D-D:

> **At each design scale, the anchoring authority is the entity whose grain *is* that scale: at Universal Mode, the code (the only place code-grain evidence is direct); at Population Mode, the aggregate evidence ladder (the only place source-ranking does its substantive adjudication); at Person Mode, the person themselves — in OT-supported co-design, the in-situ analogue of Co-1 co-primacy — with published evidence conditioning the assessment *process*, never overriding the assessed answer.**

This is not new machinery; it is the already-ratified content of §1.6 plus `co1-operational.md`'s Person-scale rule, stated positively. Its corollaries, all already canonical: Universal Mode uses source-ranking only to justify exceeding the floor; the Population range is where the hierarchy adjudicates values; Person Mode asks a different evidence question (assessment and clinical-reasoning evidence), so the parameter-value ladder does not re-run there, and no population-level source — including population-grain Co-1 — overrides an individual's assessed position.

**The mode × evidence-stratum matrix.** Rows are evidence strata (tier × type × default grain); columns are the claim's design mode; cells show the anchoring role, with the mechanical `scale_directness` outcome from `schemas/directness.py` in parentheses. Grain assignments marked † change under G3/G6 (§4); the matrix shows the **post-G3/G6** state, which is the state the pilot engine implements.

| Evidence stratum (grain) | Universal Mode claim | Population Mode claim | Person Mode claim |
|---|---|---|---|
| T1 clinical (specific) | Supports raising the floor (ADJACENT) | **Anchors** (DIRECT; DOWN-WEIGHTED if it generalizes beyond what it measured) | Conditions assessment process (DIRECT as grain, but the claim type differs — §1.6) |
| Co-1, individual-grain: `academic_narrative`, individual-testimony corpus (specific†) | Supports raising the floor (ADJACENT) | **Anchors** preference/dignity/autonomy claims (DIRECT unless generalizing beyond source) | Honored as evidence; **never substitutes for this person's own voice** (DIRECT as grain; co-design governs) |
| Co-1, population-grain: `dpo_research`, `advocacy_position` (aggregate†) | Supports raising the floor (ADJACENT) | **Anchors** community-consensus claims (DIRECT) | Conditions, does not resolve (DOWN-WEIGHTED; `co1-operational.md`: population Co-1 does not override individual assessment) |
| T2 sr_meta (aggregate) | Supports raising the floor (ADJACENT) | **Anchors** (DIRECT) | Conditions, does not resolve (DOWN-WEIGHTED) |
| T2 standard_eb — named-org evidence-based standards (aggregate†) | Supports raising the floor (ADJACENT) | **Anchors** (DIRECT) | Conditions, does not resolve (DOWN-WEIGHTED) |
| Co-2 OT CPGs (aggregate) | Supports raising the floor (ADJACENT) | **Anchors** (DIRECT) | Governs the assessment *process* (DOWN-WEIGHTED as parameter-value evidence; primary as process evidence) |
| T3 clinical / grey (specific) | Supports (ADJACENT) | Supports; anchors alone only per tier3-threshold DR (DIRECT/DOWN-WEIGHTED) | Conditions assessment (DIRECT as grain) |
| T4–T5 standards/frameworks (code, unless re-grained per G1) | **Direct** — defines/raises the harmonised floor (DIRECT) | NON-ANCHORING (convergence-not-evidence) unless re-grained per G1 | NON-ANCHORING |
| T6 statutory code (code) | **Direct** — *is* the floor (DIRECT) | NON-ANCHORING | NON-ANCHORING |

The matrix is mechanically checkable: §10 includes the runnable sweep that regenerates the parenthesized outcomes from `schemas/directness.py` and diffs them against this table.

## 4. Directness — the conditioning layer

Directness conditions the weight a source carries for a given claim, as a categorical layer over the single ladder — never a separate hierarchy per scale, never a numeric confidence score (`evidence-methodology.md` §1.7; `schemas/directness.py`). Three dimensions: population-directness (EXACT/PARTIAL/PROXY/MISMATCH), value-directness (EXACT/WITHIN-TOLERANCE/NOT-FOUND/CONTRADICTED), scale-directness (DIRECT/ADJACENT/DOWN-WEIGHTED/NON-ANCHORING). They consolidate to one conditioning grade: DIRECT / DOWN-WEIGHTED / DISCOUNTED / NON-ANCHORING. The principle is **grain-matching, not specificity-ranking** — bidirectional per GRADE's directness (indirectness) domain: an aggregate systematic review is strongest for a population claim and down-weighted for a person-specific claim; a direct intervention study is the reverse.

Four refinements close gaps found by adversarial review (2026-07-12); each is a separately ratifiable DR item:

**G1 — Re-graining rule for T4/T5** `[NEW — DR-gated]`. `tier-system.md` §1 already says T4/T5 sources can support best-practice claims "if the standard itself rests on T1/T2 evidence." This document operationalizes that clause: a T4/T5 source is assigned `GRAIN_AGGREGATE` (and thereby escapes NON-ANCHORING at Population Mode) **only** when its evidence basis is documented as traceable to T1/T2 evidence, with that provenance recorded on the source record. Otherwise it keeps `GRAIN_CODE`. Untraceable standards convergence stays in the regulatory stratum where §2 put it.

**G2 — NOT_ASSESSED is not EXACT** `[NEW — DR-gated]`. `consolidate()` currently treats a `None` population-directness as "not applicable — does not block," which is correct for claims where the dimension genuinely does not apply, but only 27 of 640 sources carry any `evidence_population_match` row — so at backfill scale, "never assessed" would silently grade as fully direct. The engine distinguishes **NOT_ASSESSED** (dimension applies, no assessment exists) from **not-applicable** (dimension genuinely inapplicable). A NOT_ASSESSED dimension caps consolidation at DOWN-WEIGHTED and flags the source for assessment. Absence of assessment is never treated as evidence of directness — the Altman & Bland distinction (`evidence-methodology.md` §2.4) applied to the project's own metadata.

**G3 — Co-1 grain follows `co1_source_type`** `[NEW — DR-gated]`. Co-1 is not uniform in grain: `dpo_research` and `advocacy_position` are population-grain community knowledge (→ GRAIN_AGGREGATE); `academic_narrative` and individual-testimony corpora are individual-grain (→ GRAIN_SPECIFIC); `peer_reviewed_literature` and `validated_tool` default per the study's own design, recorded per source. This makes the matrix row-pair in §3 mechanical, and it encodes the ethical rule already in `co1-operational.md`: a DPO position paper is community consensus — it anchors Population-Mode claims *and does not override an individual at Person Mode*; an individual narrative is the reverse.

**G6 — Grain derives from (evidence_type × tier), not evidence_type alone** `[NEW — DR-gated]`. `standard_eb` spans two strata: T2 named-organisation evidence-based standards (synthesis-tier — the "same epistemic move as sr_meta, different machinery," `tier-system.md` §2) and T4 international standards (regulatory stratum). The current type-only default grains both as CODE, which would make T2 DPO/professional-body standards NON-ANCHORING at Population Mode — contradicting `evidence-methodology.md` §1.6, which lists Tier 2 among the anchoring strata. Resolution: `standard_eb` at T2 → GRAIN_AGGREGATE; `standard_eb` at T4/T5 → GRAIN_CODE (unless re-grained per G1). Grain assignment is a function of the (type, tier) pair.

## 5. Determinations — states, and what each state is *about*

Each (item × population) cell holds one of four states (`evidence-methodology.md` §2; storage: migration 026): `stated`, `provisional`, `pending`, `not_applicable`. The determination is written by a pure function — same evidence + same `rule_version` ⇒ same state and same `derivation_sha` (`workplan/best-practices-assessment-system.md` §3) — and no `stated` or `provisional` determination can exist without non-empty `governing_refs` (anti-hallucination, DR-2026-07-12 item 10; `pending`/`not_applicable` rows carry a gap link or rationale instead).

**Scale-tagging** `[NEW — DR-gated: G1b]`. Every determination is tagged with the design scale its claim speaks to, and the tag governs what the determination may be *called* in every rendering:

- A determination anchored in T1/Co-1/T2/Co-2 (with T3 per its threshold DR) is a **Population-Mode best-practice determination** — the only kind entitled to the phrase "best practice."
- A determination whose entire basis is the regulatory stratum (T4–6) is a **Universal-Mode regulatory determination**. It answers "what does the harmonised/statutory floor specify?" — a legitimate, useful claim — and is flagged `regulatory_stratum_only` (extending migration 026's `code_floor_only`, which covers only the T6-only case, to the full T4–6-only case). It is never rendered as best practice, in any register, for any audience. `v_best_practice` excludes it; the `provisional` confidence flag names the absent anchoring dimensions (§2.3's flag, now with teeth at T4/T5, not just T6).
- Person Mode produces no stored determinations at all: it is process-resolution within the Population range (§3). What the guidebook stores for Person Mode is the *handoff* — the functional parameter driving assessment and the resolution range (`armature_v4.md` §4.6 "Mode S handoff" — vocabulary normalized to "Person-Mode handoff" per §7).

This closes the one channel through which the convergence-not-evidence trap could re-enter: previously, `evidence-methodology.md` §2.3 let T4–6 convergence produce a `provisional` synthesis that §3.4's voice line could render as "[N] jurisdictions' standards converge on [value]" without a mandatory scale disclaimer, and the policymaker profile up-weights exactly that stratum. Scale-tagging makes the laundering path mechanically impossible rather than editorially discouraged.

Two further determinations-layer refinements surfaced by the operational pilot, each separately ratifiable:

**G7 — the `stated`-threshold wording admits what §1.6 anchors** `[NEW — DR-gated]`. §2.2's OR-clause names "Tier 1–3 **clinical** evidence… Co-1… Co-2" while §1.6 lists **Tier 2** (both streams — sr_meta *and* named-organisation evidence-based standards) among the anchoring strata. A cell anchored solely by a T2 evidence-based standard (e.g. a professional-advisory flash-rate recommendation) is `stated` under §1.6's reading and unreachable under §2.2's literal wording. Resolution: amend §2.2 to admit T2 anchors explicitly (both streams), keeping the G6 grain rule so T2-standard anchoring never leaks to T4/T5.

**G8 — `pending_assessment` cells may render, with mandatory disclosure** `[NEW — DR-gated]`. §3.4 says `pending_assessment` cells are "not rendered — flagged for assessment before publication," treating the status as transitional. With `source_value_extractions` empty, multi-axis cells are honestly `pending_assessment` for as long as value extraction lags — suppressing them would hide the corpus's strongest cells because of a metadata backlog. Resolution: a `pending_assessment` cell may render **only** with the value-level-convergence-pending disclosure in every register (the register map's `stated_multi_axis` rows carry it), and §3.4 is amended accordingly.

## 6. Audiences — same determination, different register, never different data

Audience structure (`governance/audience-priority.md`, CANONICAL): **primary** = designers and disabled people (production-use endpoints); **secondary** = occupational therapists and policymakers (intermediaries). Presentation (`armature_v4.md` §4.5): each role maps to an emphasis and a register — Designer/technical, OT/clinical, Policymaker/policy, Disabled person/plain-language, Carer/plain-language-care-context — under the hard rule: **role does not change the underlying data.**

**Advocacy-brief use-pattern** `[NEW — DR-gated: G5]`. "Advocate" is not currently a named audience anywhere in canonical governance; `armature_v4.md` merges "disabled person / advocate" into one role. Resolution: advocacy is ratified as a **use-pattern within the disabled-person primary audience** (available by extension to carers and DPO staff), not a fifth audience. Its content need is real and distinct: the code-vs-best-practice **delta** ("the law requires 1800mm; the evidence supports 2440mm"), rights framing (CRPD-linked), and citable evidence strength — the policymaker rationale pattern with reversed valence. It inherits primary-audience priority (it belongs to a primary audience), which `audience-priority.md`'s conflict rules already handle; no restructuring of the four-audience architecture is needed, and the delta it foregrounds is computable (`v_code_floor` join per DR-2026-07-12 item 9).

**The claim-strength register map** `[NEW — DR-gated: integrity mechanism]`. "Role changes register, never data" has until now been asserted, not testable. It becomes testable by making claim-strength language a **finite lookup, not free prose**: every rendering of a determination must draw its claim-strength language from a single map keyed by the determination tuple

`(state, tier_basis, convergence, conditioning summary, regulatory_stratum_only)`

with one language cell per register. Illustrative rows (the full map ships with the pilot and is versioned with `rule_version`):

| Determination tuple | Technical register | Policy register | Plain-language register |
|---|---|---|---|
| `stated`, T1+Co-1, converge | "Best practice: X [●]. Clinical and lived-experience evidence converge." | "Evidence-based best practice X (convergent clinical + lived-experience basis); its relation to the code floor is stated only where extracted values support it." | "Research and disabled people's own experience both support X." |
| `stated`, Co-2 only | "Best practice: X [●] (OT professional-body guidance)." | "Best practice X per OT clinical practice guidelines; no independent trial evidence yet." | "Occupational-therapy professional guidance supports X. Research trials haven't tested this point yet." |
| `provisional`, `regulatory_stratum_only` | "Regulatory-stratum value: X [◐]. Standards converge; **no anchoring evidence (T1/Co-1/T2/Co-2) exists for this cell.**" | "Standards converge on X. **Convergence is not evidence** — no T1/Co-1/T2/Co-2 anchor exists; treat X as floor, not target — the jurisdictions could all be wrong together." | "Building rules in several countries agree on X, but there's no research or lived-experience evidence yet showing X is what actually works best." |
| `pending` | "[BEST-PRACTICE-PENDING] — gap register →" | "[BEST-PRACTICE-PENDING] — evidence gap logged →" | "We don't know yet. This is an open gap we are tracking — not a settled answer." |

Note the third row: the policymaker register — the one most tempted by convergence — carries the *strongest* anti-laundering language, not the weakest. Emphasis re-ranking (the `weighting_profile` mechanism, `workplan/best-practices-assessment-system.md` §5) chooses **which cells and columns are foregrounded** per audience; it can never move a rendering to a different row of this map.

**The five integrity invariants** `[NEW — DR-gated: integrity mechanism]` — mechanically checked by `scripts/audit/register_integrity_check.py`, which must be demonstrated firing on injected violations before its passes count (§10):

- **I1 — Tuple identity.** Every rendering of a cell, in every register, carries the identical determination tuple. Different words, same facts.
- **I2 — Floor-anchor pairing.** Any rendering that shows a regulatory floor value alongside an evidence-anchored value must show both and label which is which; the policymaker register must always render the delta, never the floor alone.
- **I3 — No best-practice language on regulatory-stratum-only cells,** in any register, under any weighting profile.
- **I4 — Marker translations are drawn only from the register map.** Plain-language translations of ●/◐/○ (`tier-system.md` §5) come from the map, not ad-hoc prose.
- **I5 — No register may express claim strength exceeding its map row.** A register may say *less* than the maximum (brevity), never *more* (inflation).

## 7. One vocabulary

Three vocabularies currently name the design modes, and one of them collides catastrophically with the evidence tiers:

| Deprecated usage | Where it appears | Canonical replacement |
|---|---|---|
| "Tier 1" / "Tier 2" *as design modes* | `mission-and-epistemics.md` commitment 4 table; `armature_v4.md` §4.6 output matrix ("Universal Mode / 1 / 2"); scattered prose | **Population Mode** / **Person Mode** |
| "Mode P" / "Mode S" | `evidence-methodology.md` §4; `armature_v4.md` §4.6 ("Mode S handoff") | **Population Mode** / **Person Mode** ("Person-Mode handoff") |
| "Tier 1 range" (design sense) | OT use-pattern rows in `audience-priority.md` | "Population-Mode range" |

`[NEW — DR-gated: vocabulary normalization]` **Universal Mode / Population Mode / Person Mode** become the sole canonical names for the design scales (matching `schemas/directness.py` SCALE_* values, which already use universal/population/person). "Tier N" is reserved exclusively for the evidence ladder. The unification DR's execution section lists the exact file-by-file edits; canonical documents are edited only after ratification. This collision is not cosmetic: it is the mechanical reason the architecture kept reading as contradictory — "Tier 2" simultaneously meant *systematic reviews*, *person-specific co-design*, and *OT CPGs* depending on the document.

## 8. Worked examples — the architecture end-to-end

**8.1 Corridor width (the canonical case, `tier-system.md` §3).** T5/T6 codes converge on 1800mm two-wheelchair passing; Co-1/T2/T3 evidence (Bauman 2010 DeafSpace, Vaughn 2018, Cloete & Rout 2025) anchors 2440mm primary corridors. — *Universal Mode:* floor = 1800mm (code-grain DIRECT); the population evidence justifies specifying above the floor. *Population Mode:* best practice 2440mm; the 1800mm convergence is NON-ANCHORING (I3 forbids calling it best practice in every register). *Person Mode:* no re-adjudication; assessment resolves within the population range (e.g., a wheelchair user with a service animal, or two signing companions, may need the full 2440mm envelope). — *Designer:* "2440mm best practice [●]; 1800mm regulatory floor (AS 1428.1 et al.)." *Policymaker:* the delta, with the convergence-not-evidence warning. *Disabled person:* "Research and Deaf-community experience support corridors wide enough for two people to sign side-by-side or two wheelchairs to pass — wider than the legal minimum." *Advocacy-brief:* "The law requires 1800mm; the evidence supports 2440mm. Citable sources: …" Same tuple in all four (I1).

**8.2 Co-2-only cell (e.g., a home-modification parameter addressed by an RCOT/AOTA CPG, no trial evidence).** State `stated` per §2.2 condition 3; tuple (stated, Co-2, single). Every register discloses the basis honestly (map row 2): the claim is legitimate best practice *and* its evidence character is visible — rigour and usability are not traded off.

**8.3 T4/T5-only cell (the decisive G1 test).** ISO + BS convergence on a parameter, zero T1/Co-1/T2/Co-2. Pre-G1: `provisional`, rendered "standards converge on X," policymaker profile up-weights it — laundering. Post-G1: `provisional` + `regulatory_stratum_only`; excluded from `v_best_practice`; every register uses map row 3; the confidence flag names the absent anchoring dimensions; the cell appears in the gap register as needing anchoring evidence. If the standard's own evidence base is later documented as traceable to T1/T2, the G1 re-graining rule admits it as GRAIN_AGGREGATE — with provenance recorded, not assumed.

**8.4 Co-1/T1 divergence at Person Mode (entrance threshold, `evidence-methodology.md` §4).** Where clinical evidence and lived-experience evidence diverge on a parameter, the divergence is recorded and a synthesis approach is required and rendered (never hidden). At Person Mode the asymmetry principle governs: the person's own assessed need — not the population median, not the DPO position, not the CPG — resolves the value within the range. The OT register presents the functional parameter and resolution range; the plain-language register tells the person what is theirs to decide.

## 9. Academic rigour and ethics — the standing commitments

**Rigour.** The architecture's methodological anchors, and where each is argued in full: correspondence to GRADE/JBI/SIGN and why wholesale GRADE adoption is insufficient for built-environment claims (`references/methodology-evidence-hierarchy-mapping.md` v2 — the directness layer *is* GRADE's indirectness domain, applied bidirectionally; synthesis-above-primary follows GRADE; the co-primacy of lived experience is a declared, argued departure, not an oversight); categorical rather than numeric conditioning (no false-precision scores, `schemas/directness.py` BOUNDARY note); determinism and reproducibility (pure determination function, `rule_version` + `derivation_sha`); falsifiability (every `stated`/`provisional` cell records what evidence would overturn it, `workplan/best-practices-assessment-system.md` §3 item 6); absence-of-evidence ≠ evidence-of-absence (Altman & Bland 1995, applied to cells in §2.4 and — via G2 — to the project's own assessment metadata); and the anti-hallucination gate (no determination without resolvable `governing_refs`).

**Ethics.** The commitments are structural, not aspirational: CRPD Art. 4.3 grounds Co-1 co-primacy (Art. 9 ≈ Universal Mode floor; Art. 5 reasonable accommodation ≈ Person Mode; the full article-by-article critique is `governance/armature_v3_review.md`); epistemic justice is engineered — testimonial justice via Co-1's non-substitutable co-primacy and G3's refusal to let population-grain speech stand in for individuals, hermeneutical justice via the plain-language register receiving the *same* determination tuple as the technical one (I1: access to the same facts, not a simplified sub-truth); the carer is a distinct role, never a proxy for the disabled person (Art. 12 supported-not-substituted decision-making, `armature_v4.md` §4.5); representation-checking by disabled readers is an elevated-weight use-pattern whose failure overrides designer convenience (`audience-priority.md` §Within-primary); and the solo-authorship limit is declared on every Co-1-governed determination — pre-launch engagement with Co-1 is evidence-level, not participation-level, and CRPD Art. 4.3 is thereby honored in partial form only (`mission-and-epistemics.md` §Operational reality). Integrity here means the limits are rendered, not just recorded.

## 10. What would falsify this architecture, and how it is checked

**Mechanical checks (each must be shown firing on injected bad data before its pass counts):**
1. *Matrix–code consistency:* the sweep below regenerates §3's parenthesized outcomes from `schemas/directness.py` for all grain × scale combinations; any diff fails.
2. *Determinism:* the pilot engine run twice over the same evidence set yields byte-identical `derivation_sha` values.
3. *Invariants I1–I5:* `scripts/audit/register_integrity_check.py` over rendered output.
4. *State-machine integrity:* `scripts/validate_evidence_state.py` (governing_refs non-empty; `code_floor_only`/`regulatory_stratum_only` never `stated`; Tier-3-alone threshold).

```python
# Matrix–code consistency sweep (§3). Run from repo root: python -c "…" or scripts/audit/matrix_consistency.py
from schemas.directness import (ALL_GRAINS, ALL_SCALES, scale_directness)
for grain in sorted(ALL_GRAINS):
    for scale in sorted(ALL_SCALES):
        print(f"{grain:>10} × {scale:<11} -> {scale_directness(grain, scale)}")
# Expected (must match §3's parentheses): aggregate×population DIRECT; aggregate×person DOWN-WEIGHTED;
# aggregate×universal ADJACENT; code×universal DIRECT; code×population NON-ANCHORING; code×person NON-ANCHORING;
# specific×person DIRECT; specific×population DIRECT (DOWN-WEIGHTED if generalizes_beyond_measured); specific×universal ADJACENT.
```

**Falsification conditions (doctrinal):** this architecture is wrong if — a rendering pipeline honoring I1–I5 cannot serve a named audience's canonical use-pattern without breaching an invariant (audience needs and integrity actually conflict); or a real cell arises whose correct handling requires re-ranking the ladder per mode rather than conditioning it (D-D's core is false); or representation-checking by disabled readers returns systematic "this is wrong about my experience" verdicts on determinations the machinery marks sound (the machinery measures the wrong thing). Any of these routes to a DR, not a silent patch.

---

## Status

| Field | Value |
|---|---|
| Created | 2026-07-12 |
| Status | PROPOSED — pending owner ratification (`decisions/DR-2026-07-12-evidence-architecture-unification.md`) |
| New-doctrine items | G1 (re-graining + `regulatory_stratum_only` + scale-tagging), G2 (NOT_ASSESSED), G3 (Co-1 grain by source type), G4 (asymmetry principle, declarative), G5 (advocacy-brief use-pattern), G6 (grain from type × tier), G7 (`stated` threshold admits T2 anchors explicitly), G8 (`pending_assessment` renders with mandatory disclosure), register map + invariants I1–I5, vocabulary normalization |
| Everything else | Restatement with citation; source documents govern |
| Author | Claude, at owner request; adversarially reviewed pre-proposal (see DR revision history) |
