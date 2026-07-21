# Functional Taxonomy — Two-Layer Model (Axes × Profiles)

**Status: PROPOSED — pending owner ratification.** Version 1.1 (2026-07-21) —
amended after two adversarial passes (general; lived-experience and global
non-English standpoints) and reconciliation with canon. Decision wrapper:
`decisions/DR-2026-07-21-two-layer-functional-taxonomy.md`. Staged schema:
`working/taxonomy/staged_schema_functional_axes.sql` (outside the migration glob).
**This document states doctrine; it executes nothing.**

**Architectural basis.** This taxonomy is the data-model execution of
`governance/armature_v4.md` §§4.2–4.3 and §5 — the two-layer architecture ("Layer 1
— Functional axes … Layer 2 — Population identity … Neither reduces to the other.
Both are first-class"; two entry paths, "Neither is primary. Neither is fallback")
and its impairment-axes candidate set. Version 1.0 of this document was drafted
without reading the armature and independently re-derived much of it; that
convergence is evidence for the architecture, and this version defers to the
armature's vocabulary and mechanisms wherever they are stronger (notably
mapping-confidence, §3.2). Amendments are annotated **[T1]–[T8]** to the tensions
they instantiate in `governance/held-tensions.md`, whose bindings govern this
document.

---

## §0 Why taxonomy is the curation gate

Every research entity downstream of this document — slugs, search-log entries, BPC
files, evidence rows, item links — inherits its selection and attachment rules from
the taxonomy. A source is only findable if some entity names what it is evidence
*about*; it is only curatable if an entity exists for it to attach *to*.

Axes are framed as **person-environment interaction dimensions** — where a person's
functioning meets an environmental demand — per armature §5 ("Axes are framed as
person-environment interaction dimensions where possible") and the mission's
biopsychosocial ground. The taxonomy names demands the *environment* places on
variable bodies, which is the part designers control; it does not define bodies by
deficit. **[T1][T2]** Where an ICF `b`-code anchor (a body-function code) appears,
it serves *findability* — reaching the clinical literatures indexed that way — and
never serves as a description of any person (population-taxonomy §1.1: codes are
"an organizing convenience, not a definition of people").

The 2026-07-21 audit found both curation failure modes live:

- **Findability failure:** balance/vestibular function was named in canon
  (armature §5 lists a vestibular axis; `population-taxonomy.md` NEU/PCS names
  "vestibular") yet is **operationally invisible**: zero ICF b-codes corpus-wide,
  zero slugs, zero searches in any of 19 tracked languages. Conceptual presence
  without curation machinery produced structural absence. **Caveat [T1]:** the
  absence checks were run with English search terms over an EN-heavy corpus; the
  non-English validation gate (§9.2) exists precisely because "missing" so far
  means "missing-in-English."
- **Attachment failure:** evidence about MS thermal intolerance attaches to a
  diagnosis shelved under "neurological" — an etiological placement — so sibling
  populations with the same functional demand (SCI poikilothermia, POTS, older
  adults) cannot reach it.

## §1 The representations being reconciled

Three representations of the population layer currently coexist and have drifted:

| Representation | Where | Shape |
|---|---|---|
| Canonical governance taxonomy | `governance/population-taxonomy.md` (CANONICAL, A7) | 11 top-level codes + sub-codes (MOB/AMB, MOB/UPL, NDV/AUT, NDV/ADHD, NDV/SENS, NEU/PCS, OFS/ME, OFS/POTS, OFS/MCAS); supplementary CHD/LPA/EXH/BAR; IntD proxied |
| Live database | `data/guidebook.db` `populations` | 22 flat codes (sub-codes flattened: AUT, ADHD, MS, EPI, SCI, CFS, POTS, MCAS, PCS…), archetypes absent |
| This proposal | this document + staged SQL | 17 axes (Layer 1) × profiles (Layer 2) |

This document **amends-by-proposal** the canonical taxonomy rather than silently
diverging from it **[T4]**: under ratification, `population-taxonomy.md` §5's own
change process applies (proposal → decision → enum → governance update). The
canonical codes are retained as Layer 2 identifiers; where the DB flattened a
canonical sub-code (e.g. `CFS` for `OFS/ME`, `AUT` for `NDV/AUT`, `PCS` for
`NEU/PCS`), §4 records the canonical alias and the migration plan re-aligns the DB
to canon. The defect being fixed is not the canonical codes — it is that the
canonical structure mixes three ontologies (functional clusters, diagnoses,
archetypes) in one namespace, which armature §4.2 already resolves into two layers.

## §2 Layer 1 — Functional axes

An **axis** is an architect-actionable person-environment interaction dimension:
an environmental demand that bodies meet variably, which design parameters can
lower, meet, or fail. Axes anchor mechanism and threshold evidence and
`item_axis_links`. An axis with zero linked slugs or items is a *visible,
queryable coverage hole* — by design.

### §2.1 The axis register (17)

| Axis | Name (interaction-framed) | ICF anchors (findability) | Demand the environment places | Status |
|---|---|---|---|---|
| `AX-AMB` | Ambulant movement | b770, b730 · d450, d455, d460 | Continuous walking, stairs, distance, gradients — incl. **floor-level living: floor-sitting, prostration, and floor-to-standing transitions** [T1] | ESTABLISHED |
| `AX-WHM` | Wheeled movement & transfer | b730, b710 · d465, d420, d410 | Turning, clearance, transfer geometry — independent **and assisted** (two-person, hoist) [T3][T5] | ESTABLISHED |
| `AX-REA` | Reach & manipulation | b730, b710 · d440, d445 | Reach envelopes, grip, operating force — at chair, counter, **and floor-level** heights | ESTABLISHED |
| `AX-BAL` | Balance & postural demand | b235, b240 · d415, d410 | (a) fall-risk under gait/transfer load; (b) **environments that precipitate dizziness**: repeating pattern, specular floors, glazed edges at height, escalators, large uniform visual fields | STUB |
| `AX-STA` | Sustained-exertion demand | b455, b130 · d230, d450 | Standing, queueing, distance without rest; **grid/lift failure converting routes into exertion cliffs** [T1] | ESTABLISHED |
| `AX-PAI` | Pain-load demand | b280 · d410, d450, d640 | Impact, vibration, pressure, cold. Mechanism spans **nociceptive and centrally-sensitized pain** — fibromyalgia-type pain is not nociception-dominant, and provisions must not assume load-avoidance alone suffices | ESTABLISHED |
| `AX-THR` | Thermal demand | b550 · d230 | Heat/cold exposure for impaired thermoregulation — via conditioning **and passive means (shading, mass, ventilation) where grids are intermittent** [T1] | PARTIAL |
| `AX-CHM` | Airborne-exposure demand | b435, b440 · d230 | VOCs, fragrance, particulates, smoke | PARTIAL |
| `AX-VIS-L` | Low-vision information demand | b210 · d460, d166 | Environments legible through residual vision: contrast, lighting, glare, size | ESTABLISHED |
| `AX-VIS-N` | Non-visual information demand | b210 · d460 | Environments legible without vision: tactile, acoustic, layout consistency | ESTABLISHED |
| `AX-AUD` | Auditory access & alerting demand | b230 · d310, d115 | Speech access, alert receipt, assistive listening infrastructure | ESTABLISHED |
| `AX-SPR` | Sensory-load demand | b156, b140 · d230, d160 | Stimulus intensity, unpredictability, trigger exposure (incl. photic) — ICF under-represents modulation; anchors are nearest-fit, recorded honestly | ESTABLISHED |
| `AX-COG-O` | Orientation demand | b114, b144 · d460, d175 | Legible-space demands: memory, sequencing, decision-point load | ESTABLISHED |
| `AX-COG-L` | Information-access demand | b117, b167 · d166, d310, d315 | Legible-information demands: comprehension load of signage and instructions — **across scripts and literacy levels, not only Easy-Read-genre English** [T1] | STUB |
| `AX-COM-E` | Expressive-communication demand | b320, b330 · d330, d335, d350 | Environments that require producing speech under time/acoustic pressure: counters, intercoms, service interactions; AAC-user dwell and device acoustics. **Signed languages are languages, not deficits: d340 (sign production) is held by the Deaf-community profile (§4), which this axis serves only for sightline/lighting infrastructure** [T2][T3] | STUB |
| `AX-ARO` | Arousal-safety demand | b152 · d240 | Threat-appraisal load: exposure, unpredictability, lack of retreat or exit legibility | STUB |
| `AX-CNT` | Toileting-proximity demand | b620, b525 · d530 | Urgency/frequency as plan-driver: distance, provision count, management space (ostomy/catheter; adult-changing provision as need-driven), **squat and sitting WC typologies both first-class** [T1] | STUB |

**Falsification symmetry [T4].** *Every* axis — established and new alike — carries
a dissolution condition in the staged schema (e.g., AX-AMB/AX-WHM re-merge if
evidence shows no parameter divergence; AX-BAL merges into AX-AMB if precipitant
guidance reduces to fall-prevention parameters). New categories do not audition for
existence under a burden established categories are spared.

### §2.2 New-axis specifications (abbreviated)

`AX-BAL`: both mechanisms currently homeless operationally (§0). Proposed slug
`vestibular-balance-built-environment`, queued per §8. `AX-COG-L`: un-proxies
intellectual disability for information access (GAP-277); armature §5.1 governs the
IntD treatment (population-level content + axis entry; minimal-predictive mapping).
`AX-COM-E`: built-environment residual only; the bulk of communication support is
human/service scope. `AX-ARO`: rescinds the FDA scope-out of b152/d240 for the
architecturally actionable subset; trauma-informed design evidence curates here.
`AX-CNT`: the physiological driver behind provision-count/proximity parameters.
`AX-CHM`: names the axis the air-quality slug already feeds; re-homes MCAS by
mechanism.

### §2.3 Reconciliation with armature §5 (20-axis candidate set)

The armature's candidate set maps onto this register as follows; granularity
deltas are ratification items, not silent decisions:

| Armature §5 candidate | This register | Note |
|---|---|---|
| Ambulatory capacity; Postural control; Transfer capacity | AX-AMB; AX-BAL (postural); AX-WHM (transfer) | Transfer folded into wheeled-movement; **checklist item R6**: keep folded or split per armature |
| Vestibular function | AX-BAL | Convergent — armature named it first |
| Limb presence; Reach envelope; Grip & manipulation | AX-REA (+ profile modifier for limb presence) | Limb presence as profile attribute, not axis |
| Visual acuity / field / processing; Light tolerance | AX-VIS-L, AX-VIS-N, AX-SPR (photic) | Coarser here; armature's finer grain available as axis sub-values at build |
| Auditory acuity / processing | AX-AUD | Processing sub-values at build |
| Sensory regulation | AX-SPR | Convergent |
| Cognitive processing (memory/executive/speed/abstract) | AX-COG-O, AX-COG-L | Armature flags granularity as an A7 decision — unresolved here too; **checklist item R7** |
| Communication & speech | AX-COM-E | With the d340 carve-out (§2.1) |
| Pain & fatigue envelope | AX-PAI + AX-STA | Split by mechanism (nociceptive/central vs exertional); both feed pain-ofs slug |
| Thermoregulation | AX-THR | Convergent |
| Continence & toileting independence | AX-CNT | Convergent; independence spectrum carried as axis values |
| **Respiratory / oxygen dependency** | **Divergence — checklist item R8** | v1.0 rejected a respiratory axis (decomposes to AX-STA + AX-CHM + egress thread); armature lists it with concrete spatial consequences (corridor width, bathroom space, lift priority, egress). Both positions are recorded; the owner adjudicates |

## §3 Layer 2 — Profiles

A **profile** is who evidence is about: population codes (canonical Layer 2
identifiers), diagnosis-level, identity-level, demographic, anthropometric,
compound, and umbrella groupings — each carrying weighted axis mappings *plus
authored emergent content that is never derived from, and never reduced to, the
axis layer*.

### §3.1 The emergence guarantee **[T3]**

Mature design corpora — DeafSpace, dementia-friendly design, ASPECTSS, age-friendly
design, DBL tactile-first practice — are authored at profile level and are not
reconstructable from axis sums. Profile-level and Co-1 evidence curate against
profiles and are never subordinated: Co-1 is encoded `tier: 1` (mission #3), so
lived-experience evidence anchors full-strength (●) claims. Conflicts between
profile guidance and axis-derived guidance display at parity (held-tensions T7);
no precedence rule exists.

### §3.2 Mapping confidence (adopted from armature §4.2) **[T2][T4]**

Diagnosis-to-axis mappings are *navigation hypotheses, not prescriptions*, graded:
**high-predictive** (confident pre-fill; e.g. complete T6 SCI), **moderate**
(sub-classification prompt; validated scaffolds), **low** (explicit high-variation
disclosure; e.g. MS, ABI), **minimal** (no pre-fill; population content + direct
axis entry; e.g. IntD). Each mapping's confidence is itself a documented claim with
provenance. This replaces v1.0's flat PRIMARY/SECONDARY roles as the honesty
mechanism; the staged schema carries both (role for query weighting, confidence for
disclosure).

### §3.3 Membership doctrine **[T2][T4]**

**Diagnosis-optional.** Profiles describe; they never gate. Axis entry retrieves
every specification with no population selection (armature §4.3 — the two paths are
peers), so no diagnosis, certification, or code is ever a condition of any
provision, any Co-1 attachment, or any reader's use. **ICD-11 negative
commitment:** ICD anchors on diagnostic profiles serve interoperability and
disambiguation only; they are never required for membership, never gate content,
and are never used to rank populations. Identity profiles (Deaf community;
identity-model neurodivergence) carry **no** ICD anchor by design.

**Naming.** Person-first vs identity-first conventions differ *between communities
and between languages*; the taxonomy defers to each community's stated preference
in English and to native-language conventions via `term_aliases` — display names
are presentation-layer, revisable without schema change **[T1][T5]**.

## §4 Disposition of the population layer

No rows change until ratification. Canonical sub-code aliases shown where the DB
flattened them. `ALL` is a scope qualifier, not a population
(population-taxonomy §1.3).

| Code (DB) | Canonical | Disposition | Maps to | Rationale / fixes |
|---|---|---|---|---|
| MOB | MOB (+MOB/AMB, MOB/UPL) | AXIS-ALIAS | AX-AMB + AX-WHM | Canonical sub-codes already split ambulant/upper-limb; axis layer completes it |
| UPL | MOB/UPL | AXIS-ALIAS | AX-REA | |
| VIS | VIS | AXIS-ALIAS | AX-VIS-L + AX-VIS-N | Armature's finer visual axes available at build |
| DEAF | DEAF | Dual: axis-alias AX-AUD **+ Deaf-community profile** (identity; no ICD) | AX-AUD | Armature §5 poses this exact open question ("identity-recognition question, not just clinical-framing"); this is the proposed answer. DeafSpace corpus and d340 sign-space provisions are held by the profile — signed language as language, with the axis serving infrastructure only |
| SENS | NDV/SENS | AXIS-ALIAS | AX-SPR | Sub-code was an axis in population clothing; explains its 1-item-link starvation |
| PAIN | PAIN | AXIS-ALIAS | AX-PAI | Mechanism spans nociceptive + central sensitization (§2.1) |
| OFS | OFS | AXIS-ALIAS | AX-STA (+AX-THR) | |
| DEM | DEM | PROFILE (diagnostic; low-predictive) | COG-O primary; ARO, VIS-L, AMB | Emergent corpus: dementia-friendly design |
| NDV | NDV | PROFILE (umbrella; identity-framed; no ICD) | SPR, ARO, COG-O | |
| AUT | NDV/AUT | PROFILE (diagnostic/identity dual; parent NDV) | SPR primary; ARO, COM-E | Distinct emergent corpus (ASPECTSS); ICD-11 6A02 |
| ADHD | NDV/ADHD | PROFILE (diagnostic; parent NDV) | SPR, COG-O | ICD-11 6A05 |
| MH | NDV/MH (top-level per canon §2.4) | PROFILE (umbrella) | **ARO primary**; SPR | Canon already holds MH top-level for distinct functional profile; ARO gives it the axis it lacked |
| NEU | NEU | PROFILE (umbrella; low-predictive) | COG-O, AMB, ARO, COM-E | FDA term `ABI` resolves here |
| EPI | (sub-code proposal: NEU/EPI) | PROFILE (diagnostic) | SPR (situational: photic trigger) | Documented judgment call — checklist item |
| MS | (sub-code proposal: NEU/MS) | PROFILE (diagnostic; **low-predictive** per armature) | **THR primary** (Uhthoff); STA, AMB, VIS-L, CNT | Re-homed by mechanism, not etiology |
| SCI | (sub-code proposal: MOB/SCI) | PROFILE (diagnostic; high-predictive at complete lesions, else moderate) | WHM, REA, THR, CNT, PAI | Autonomic demands made visible |
| POTS | OFS/POTS | PROFILE (diagnostic) | STA, THR, BAL (situational) | |
| CFS | **OFS/ME** | PROFILE (diagnostic) | STA primary | Canonical name is OFS/ME; display "ME/CFS" per community preference. **Post-exertional malaise is a first-class design constraint: environments must not assume exertion is recoverable by rest — distance, queueing, and standing demands are harm vectors, not inconveniences** [T3] |
| MCAS | OFS/MCAS | PROFILE (diagnostic) | **CHM primary** | Re-homed by mechanism (immune), not comorbidity. Contested-legitimacy history noted: thin Tier-1 evidence partly reflects historical dismissal; §5.6 intake path applies |
| PCS | NEU/PCS | **SPLIT**: `PCS-TBI` (post-concussion) | BAL, SPR, COG-O, STA | Canon's NEU/PCS description ("light sensitivity, cognitive fatigue, vestibular") matches PCS-TBI; the FDA skill's "PCS = post-COVID" resolves to LCOV below |
| — | (new) | `LCOV` PROFILE (post-COVID condition; ICD-11 RA02) | STA (PEM), THR, COG-O | |
| DBL | DBL | PROFILE (compound; first-class) | VIS-N × AUD at compound weight | Retains full first-class standing with its authored tactile-first corpus; canon §3.1 rule preserved verbatim: DBL ≠ VIS + DEAF. (v1.0's "de-privileged" phrasing is retracted — the change is structural placement, not standing) [T4] |
| ALL | ALL | QUALIFIER | — | |

**Admitted profiles:** `CHD`, `LPA`, `EXH`, `BAR` (anthropometric; Supplementary
Volume corpora; BAR containment rule preserved — validator scope extends to the
profile layer), **`OAD` older adults** (demographic; age-friendly corpus;
readmitted under the same emergent-corpus criterion that keeps DEM), `VES`
vestibular disorders (diagnostic; BAL primary; evidence-stub *record status* — the
status describes the record, never the people **[T4]**), `LCOV` (above).
**Deferred candidates:** migraine (SPR+BAL), aphasia/dysarthria (COM-E),
IBD/ostomy (CNT) — named so their absence is visible.

## §5 Curation rules — what gets curated, and how

1. **Selection principle.** A source is in-scope iff it bears on (a) an axis
   demand-mechanism or threshold, (b) a profile's mappings or emergent guidance,
   (c) an item parameter, **(d) a situation (§5.4), or (e) operational access
   (§5.5)**. Otherwise logged out-of-scope with reason.
2. **Attachment.** Mechanism/threshold evidence → axes. Population outcomes, Co-1,
   cultural design corpora → profiles. Spec values and jurisdictional floors →
   items. First-person accounts → situations. Maintenance/POE/operational evidence
   → operational-access records against items or buildings.
3. **Slug discipline.** Every slug declares `serves_axes` (≥1). Reconciliation
   with population-taxonomy §3.3 ("one slug, one population"): slugs serve *axes*;
   population linkage is *derived* through the axis layer, so the one-population
   rule is preserved where a slug is population-scoped and relaxed only at the
   axis layer — the canonical rule is not violated, it is layered. Search-log
   entries record axis codes; `evidence_population_match.target_population` is
   normalised to codes + free-text elaboration.
4. **Situations entity [T3][T1].** First-person, episode- or journey-level
   accounts (an induced-vertigo episode in an atrium; a day navigated around
   toilet access), curated *in the teller's language* with translation held
   alongside, attaching to items, axes, profiles, or buildings. Situations are
   never decomposed into axis fragments as their primary representation;
   decomposition may *reference* them. This is the native Co-1 attachment point
   and the seed content for questions-led navigation (mission #6).
5. **Assisted and collective use [T3][T5].** Every axis carries independent /
   assisted / collective use-mode values where applicable (armature: transfer
   "independent / assisted / dependent"; carer as distinct role §4.5). Evidence
   about two-person transfers, hoist clearances, multigenerational and communal
   use curates first-class — the solo-user default is a disclosed bias, not a
   frame. The four-framework layering already includes Kawa (project-standards
   §2026-04-09), whose collectivist ground this operationalizes.
6. **Intake path for non-DOI evidence [T1][T3].** Gray, oral-history-derived, and
   DPO-authored evidence without DOI resolvability enters via a defined route:
   archived copy (or transcript) + provenance record + translation note, tiered
   normally (Co-1/Tier 3/grey per content), flagged `non_doi_intake`. DOI
   verification machinery applies where DOIs exist; its absence does not bar
   intake. This closes the loop where the verification pipeline's strictness
   would otherwise filter out exactly the evidence Co-1 doctrine protects.
7. **Strength semantics unchanged.** Tiers, bands, weak-band code-consensus rule
   per mission #2 and DR-2026-07-20. Co-1 = tier 1 = eligible to anchor ● claims.
8. **Coverage semantics.** `axis with zero slugs` and `axis with zero item links`
   are standing gap queries (extend `db.py validate`).

## §6 Vocabulary reconciliation

| Term in use | Canonical resolution |
|---|---|
| `ABI` (FDA skill) | NEU umbrella profile |
| `ASD` (FDA skill) | NDV/AUT |
| `LOW-VISION` (FDA skill) | AX-VIS-L |
| `PCS` = post-COVID (FDA skill) | LCOV |
| `PCS` = post-concussion (DB) | PCS-TBI (canon NEU/PCS) |
| `CFS` (DB) | OFS/ME (display: ME/CFS) |
| `AUT`,`ADHD`,`SENS`,`POTS`,`MCAS` (DB flat) | canonical sub-codes NDV/AUT, NDV/ADHD, NDV/SENS, OFS/POTS, OFS/MCAS |
| MOB "balance" (FDA mechanism text) | AX-BAL |

Post-ratification the FDA skill §§1–2 regenerate from the axis register, ending
skill↔DB drift; the `PopulationCode` enum change follows population-taxonomy §5's
process.

## §7 Compatibility — what this document does NOT change

Item codes A–K (entities are `ENT-##` per the rename DR) · parity conflict display
and §3.9 menu · tier system, bands, Option A weak-band rule · posture ·
population-taxonomy validator rules (BAR containment, VIS/DEAF non-compound,
DBL ≠ VIS+DEAF, ALL exclusivity — all preserved and extended to the profile
layer) · `lang_jur_map` remains empty pending owner-defined PRIMARY/SECONDARY
criteria per DR-2026-06-11 (v1.0-adjacent session advice to populate it is
withdrawn) · the mission, audience-priority, armature, and canonical taxonomy
texts · all DB rows, item links, and skill files — until ratification.

## §8 Coverage holes, and the queue rule's honest cost

Ratification creates five STUB axes, one newly named PARTIAL axis (AX-CHM), and
two evidence-stub profile records (`VES`, `LCOV`) with zero evidence obligations
attached. Research execution queues behind the existing language/jurisdiction debt
(AR/HI/BN/SW at zero; ~82% of coverage cells NOT-RUN) unless the owner reorders.
**The equity cost of that queue is named, not elided [T1][T3]:** the populations
these axes serve — newly visible after being structurally invisible — wait longer
because of a debt they did not create. The queue order is an owner decision made
for anti-displacement reasons (a governance-capacity constraint), not a judgment
of priority between people; the checklist (§9) offers the reorder explicitly.

## §9 Migration plan and gates (post-ratification)

1. **Co-1 review gate [T3][T5].** This taxonomy is *provisional pending
   lived-experience review* in whatever form the mission's §Operational reality
   permits: pre-launch, adversarial standpoint passes (the 2026-07-21 pair stand
   as the form) plus published-Co-1 checks per disposition; post-launch, the
   consultation infrastructure decides *with* disabled people. Ratification by the
   owner does not discharge this gate; it schedules it.
2. **Non-English validation gate [T1].** Before the axis register is frozen: check
   the 17 axes against `term_aliases` / native-alias machinery and the already-
   searched JA/DE/ZH/KO/ES/FR strata — do non-English literatures carve the space
   differently? Divergences are ratification items.
3. Apply staged DDL + seeds (promoted into `scripts/migrations/` at apply time).
4. Backfill `slugs.serves_axes` (79 slugs); harvest `item_axis_links` from the 87
   FDA audit briefs; then re-derive population links.
5. Regenerate FDA skill §§1–2 from the axis register; follow population-taxonomy
   §5 for enum changes.
6. Normalise `evidence_population_match.target_population`.
7. Extend `db.py validate` with zero-coverage axis queries and profile-layer
   containment rules.
8. Close GAP-277 (IntD information-access — answered by AX-COG-L + armature §5.1
   treatment); open gap rows for STUB-axis evidence debts.
