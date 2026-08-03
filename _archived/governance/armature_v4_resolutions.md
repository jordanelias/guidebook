# Armature v4 — Open Question Resolution

**Date:** 2026-04-28 07:25
**Author:** Opus 4.6
**Status:** Authoritative resolution for architectural and best-practice synthesis questions. Population-specific content decisions (naming, specific axis values, specific mappings) remain subject to revision through PWLE/DPO consultation per §9 of armature v4.
**Scope:** Design reference repository — research-grounded, multijurisdictional, multilingual built-environment specification reference.

---

## A3 — Conceptual Model

### Q1. Output schema — what does the armature return?

**Resolution: Filtered specification set.**

The armature returns a set of structured specification records, filtered by person profile, scope, and jurisdiction, presented according to role. Not a single value, not a narrative, not a composed view. A filterable, sortable, exportable set.

Each specification record carries:

- **Identity:** slug, element name, category (A–K), topic, spatial context
- **Value:** single value, range, or conditional (with the condition stated). Unit. Design stage applicability.
- **Design tier:** 0 / 1 / 2. Tier 2 records include: the functional parameter driving assessment, the resolution range, and the referral threshold.
- **Evidence:** marker (●/○), synthesis method (direct/inferred/consensus), inference basis (for non-direct), evidence provenance link, BPC entry link.
- **Jurisdiction:** array of {jurisdiction, code reference, compliance status (mandated/recommended/unaddressed)}.
- **Conflicts:** array of {conflicting axis, conflict type, resolution reference, variable-conflation-check result}.
- **Adjustability metadata:** where applicable — populations who can self-adjust, populations requiring carer/staff operation, default setting with harm-asymmetry rationale.
- **Axes:** which axis values this specification applies to (the query-match metadata).
- **Provenance:** version, last-review date, authorship.

The role layer transforms presentation of this set (register, emphasis, contextual framing) without changing the underlying records. The export function outputs the set in the user's chosen format (PDF, plain text, accessible HTML).

Tier 2 specifications are included in the set, not omitted. They are the system's way of saying "here is the question you need to ask and the range within which the answer falls." Omitting them would leave users unaware that an individual-assessment question exists.

**A3 implication:** the Specification entity schema must carry all fields above. Most are extensions of the existing schema. The `jurisdiction_scope` array and `adjustability` metadata are new structured fields.

---

### Q2. PopulationCategory — new entity or BPCMetadata extension?

**Resolution: New entity type.**

PopulationCategory exceeds what BPCMetadata can carry. BPCMetadata is a metadata wrapper for an evidence synthesis document. PopulationCategory is a content-bearing entity with:

- Category name (multilingual, with terminology variants per locale — "disabled people" UK / "people with disabilities" US / "persons with disabilities" CRPD)
- Category type: `diagnosis` | `identity` | `situation` | `population_code`
- Description: authored plain-language description of the population
- Characteristic axis profile: array of {axis, typical_value_or_range, confidence_note}
- Mapping confidence: `high` | `moderate` | `low` | `minimal` with source documentation
- Sub-classification scaffolds: array of {scaffold_name, scaffold_source, fitness_assessment}
- Population-specific design considerations: authored content from published corpus — what designers need to know about this population beyond what axes capture
- Related categories: links to other PopulationCategory entities (e.g., CP → MOB, NEU; MS → MOB, VIS, NEU, PAIN)
- Related BPC entries: links to BPCMetadata entities for this population
- THIN-BASE flag: boolean + explanation
- Validation provenance: {basis, date, assessor, method}
- Version history

This is a 7th entity type. A3 schema requires amendment.

**Rationale:** population categories carry content the research base is organized around. They are not metadata about evidence synthesis documents — they are the organizational structure of the evidence base itself. Forcing them into BPCMetadata conflates the evidence container with the population it describes.

---

### Q3. Axis-level attributes on Specification entities?

**Resolution: Yes — direct axis-level attributes on Specifications.**

Specifications gain an `axes_applicable` array: each entry is {axis_id, value_or_range} describing which axis values the specification applies to. This enables direct axis-to-specification queries without resolving through population codes first.

Population codes remain on Specifications as a parallel attribute — they are the existing organizational structure and continue to serve BPC retrieval. The two coexist. Axis attributes enable fine-grained querying; population codes enable corpus-organized retrieval.

**Rationale:** resolving axes to population codes before querying forces every axis-only query through a lossy mapping step (axis combination → nearest population code → specifications for that code). Direct axis attributes eliminate the lossy step for the primary query path while preserving population-code retrieval for the BPC corpus path.

**A3 implication:** Specification schema gains `axes_applicable` array. Existing `population` field retained. Both are queryable. Validators updated.

---

### Q4. Reverse-mapping algorithm (axis-only → BPC retrieval)

**Resolution: Axis-overlap scoring with population-relevance threshold.**

When a user enters via axes only, the system needs to surface relevant BPC entries (which are population-code-organized). Algorithm:

1. For each population code, compare the user's axis profile against the population's characteristic axis profile (stored on PopulationCategory).
2. Score overlap: count of axes where the user's value falls within the population's typical range, weighted by axes that are definitional for that population (e.g., ambulatory capacity is definitional for MOB; auditory acuity is definitional for DEAF).
3. Threshold: surface BPC entries for populations scoring above a defined relevance threshold. The threshold is calibrated so that: a manual wheelchair user with no other non-baseline axes surfaces MOB BPC entries; a manual wheelchair user with reduced vision surfaces both MOB and VIS BPC entries.
4. Surfaced BPC entries are presented as "relevant population research" — not as identity assignment. The system says "research for [population] is relevant to this profile" — not "you are [population]."

**Rationale:** this is the minimal algorithm that bridges axis-only entry to population-organized evidence. It's a relevance-scoring mechanism, not a classification mechanism. The distinction matters: the system is surfacing relevant research, not assigning identity.

**Calibration:** the overlap-scoring weights and relevance threshold require testing against representative profiles. Initial weights: definitional axes at 3×, secondary axes at 1×. Threshold: ≥0.5 of maximum possible score for a population. These are starting values subject to empirical adjustment.

---

### Q5. Entity metadata extensions for methodological transparency

**Resolution: Implement as specified in armature v4 §6.3, with the following specifics.**

**EvidenceSource gains:**
- `search_strategy`: {databases: [string], search_terms: [string], date_range: {start, end}, inclusion_criteria: string, exclusion_criteria: string}
- `screening_counts`: {identified, screened, eligible, included} — PRISMA flow numbers
- `quality_assessment`: {method: string, result: string} — how the source was assessed

**BPCMetadata gains:**
- `synthesis_method`: `narrative` | `quantitative` | `mixed`
- `last_review_date`: date
- `review_cycle`: string (e.g., "annual" or "triggered by new evidence")
- `quality_summary`: string — GRADE-like overall assessment of the evidence body

**Specification gains:**
- `synthesis_method_indicator`: `direct` | `inferred` | `consensus`
- `inference_basis`: string | null — populated when indicator ≠ direct
- `last_review_date`: date
- `jurisdiction_scope`: [{jurisdiction: string, code_ref: string, status: `mandated` | `recommended` | `unaddressed`}]
- `version_history`: [{version, date, change_summary}]

**Gap gains:**
- `user_facing`: boolean — whether this gap is surfaced through the armature
- `population_level`: boolean — whether this is a population-level gap vs specification-level
- `surfacing_method`: `evidence_marker` | `thin_base` | `coverage_statement`

These are field additions to existing entities. No new entity types beyond PopulationCategory (Q2).

---

## A7 — Population Taxonomy

### Q6. Naming

**Resolution: "Person Profile" for the query construct. No special name for the architecture itself.**

"Armature" is an internal project term useful for development. It should not appear in the user-facing tool. Users don't need to know the architecture has a name. They need to know what they're doing: building a person profile and querying specifications.

The user-facing vocabulary:
- "Person profile" — the set of functional descriptions driving the query
- "Population" or "condition" — the Layer 2 category entry point
- "Specifications" — what the tool returns

No metaphor needed. No novel terminology. Users understand "tell us about the person, we'll show you the specifications."

---

### Q7. Final axis set

**Resolution: 18 axes in 6 clusters. Reduce from 20.**

Changes from v4 candidate set:

**Merge visual processing into visual acuity as a sub-qualifier.** Visual processing differences (CVI) affect specification selection, but the number of specifications that vary by visual processing independently of visual acuity is small. Visual acuity becomes: `full` | `low vision` | `low vision + processing affected` | `no functional vision` | `no functional vision + processing affected`. This preserves the distinction without a separate axis.

**Merge light tolerance into sensory regulation.** Photophobia is a sensory regulation phenomenon. Its built-environment implications (lighting control, glare reduction) overlap with sensory hyper-responsiveness provisions. Sensory regulation becomes: `typical` | `hyper-responsive` | `hypo-responsive` | `mixed` with a sub-qualifier for `photophobic` that triggers lighting-specific specifications. This reduces axis count without losing specification granularity.

**Retain all others as proposed.** Each remaining axis independently drives specification differences that cannot be captured by other axes.

Final 18:

**Mobility & posture (4):** ambulatory capacity, postural control, transfer capacity, vestibular function.

**Limb & upper limb (3):** limb presence (modifier), reach envelope, grip & manipulation.

**Sensory (4):** visual acuity (with processing sub-qualifier), visual field, auditory acuity, auditory processing, sensory regulation (with photophobia sub-qualifier).

**Cognitive & communication (2):** cognitive processing, communication & speech.

**Physiological (4):** pain & fatigue envelope, thermoregulation, continence & toileting independence, respiratory/oxygen dependency.

That's 17 by my count. Let me recount: 4 + 3 + 5 + 2 + 4 = 18. No — sensory is visual acuity, visual field, auditory acuity, auditory processing, sensory regulation = 5. Total = 4+3+5+2+4 = 18. Correct.

**ICF cross-mapping:** each axis maps to one or more ICF b-codes (body function) and d-codes (activity). The mapping is documented per-axis as a traceability record, not as a claim that the axes are ICF codes. They are navigational aggregations derived from ICF, reframed for built-environment design query utility.

**Interaction framing evaluation:** of the 18 axes, the following can be reframed from person-deficit to person-environment interaction without losing navigational utility:

| Axis | Current (deficit) framing | Interaction framing | Feasible? |
|---|---|---|---|
| Ambulatory capacity | How the person moves | Mobility-environment interface | Yes — "how this person moves through space" |
| Grip & manipulation | What the person can grip | Manipulation-interface requirement | Yes — "what grip demand the environment can place" |
| Visual acuity | What the person can see | Visual-environment interface | Partially — "visual information the environment must provide" works for specifications but is clumsy for profile entry |
| Cognitive processing | What the person can process | Cognitive-environment interface | No — too abstract; users need to describe the person, not the environment, at entry time |

**Determination:** reframe axis *descriptions and help text* toward interaction language where natural. Retain person-descriptive axis *names* for entry usability. The profile entry UI says "how does this person move?" (person-descriptive) while the specification output says "mobility-environment interface requirements" (interaction-framed). The reframing happens at the output layer, not the input layer. This is honest: users describe people; the system translates to environment requirements.

---

### Q8. Cognitive processing granularity

**Resolution: Structured sub-classification within a single axis, not separate axes.**

The axis is "cognitive processing" with a required sub-qualifier when the value is not `typical`:

```
cognitive_processing: typical | reduced | severe
  sub_profile (when reduced or severe): {
    memory: intact | affected
    executive_function: intact | affected
    processing_speed: intact | affected
    abstract_reasoning: intact | affected
  }
```

**Rationale:** built-environment specifications vary by cognitive sub-profile in ways that matter. A wayfinding specification for someone with memory-predominant cognitive impairment (DEM) differs from one for someone with executive-function impairment (ABI) — the first needs recognition cues, the second needs decision-reduction. These are different design interventions. A single three-point ordinal collapses them.

But: four separate top-level axes would make cognitive processing disproportionately represented in the axis set (4 of 18+4 = 22 axes would be cognitive). The sub-classification structure keeps the axis count manageable while preserving the specification-relevant distinctions.

**Interface implication:** when a user sets cognitive processing to `reduced` or `severe`, the system prompts for the sub-profile. This prompt must be in plain language: "Which aspects of thinking are most affected? Memory (remembering routes, names, sequences), planning and organizing (making decisions, following multi-step tasks), processing speed (needing more time), or abstract thinking (understanding symbols, maps, complex instructions)." Multiple selections allowed.

**Mapping from populations:** DEM typically maps to memory-affected + processing-speed-affected. NEU with executive dysfunction maps to executive-function-affected. NDV may map to abstract-reasoning-affected and/or executive-function-affected depending on the specific condition. IntD maps variably across all four. These mappings are stored on PopulationCategory entities.

---

### Q9. Deaf cultural/linguistic identity

**Resolution: Both — a distinct population category AND retention within the auditory axis cluster.**

The auditory axes (acuity + processing) remain as functional axes because they drive built-environment specifications at the physical level: hearing loop coverage, visual alarm systems, acoustic treatment, vibrotactile alert systems. These specifications vary by auditory function regardless of cultural identity.

Deaf cultural/linguistic identity becomes a population category in Layer 2 with its own content:

- Category type: `identity`
- Description: Deaf people who use sign language as a primary or preferred language and identify with Deaf culture
- Design considerations beyond auditory axes: sign-language-visible sight lines in meeting rooms and reception areas, video relay infrastructure, lighting positioned for sign-language visibility (not just "adequate illumination"), visual communication systems as primary (not "alternative"), Deaf space design principles (open sight lines, circular seating, visual connectedness)
- Related axes: auditory acuity [no functional hearing], auditory processing [not applicable], communication [sign language user — this requires adding "sign language user" to the communication axis values]

**Communication axis update:** add `sign language user` as a value. Current values (typical / dysarthria / AAC user / non-verbal) do not capture sign language use. A Deaf signing person is not "non-verbal" — they use a language; the modality is visual-gestural. The axis value `sign language user` triggers specifications for sign-language-visible environments, interpreter space, and video communication infrastructure.

**Rationale:** this honors the Deaf community's consistent position that deafness is a linguistic and cultural identity, not (only) a hearing deficit. The auditory axes remain because built-environment physics (sound, vibration, visual alerting) are real. The population category carries what the axes cannot: the design implications of a language community, not just a hearing status.

---

### Q10. Population code ↔ population category coexistence

**Resolution: Population codes become one subtype of PopulationCategory.**

The existing 11 codes (MOB, VIS, DEAF, NEU, DEM, NDV, NDV/MH, PAIN, DBL, OFS, IntD) and supplementary codes (CHD, LPA, EXH, BAR) are migrated into PopulationCategory entities with `category_type: population_code`. They retain their existing function: organizing the BPC corpus, structuring the gap register, anchoring specification population attributes.

Additional PopulationCategory entities are created at finer grain:
- Diagnosis-level categories (e.g., "Multiple Sclerosis," "Cerebral Palsy," "Ehlers-Danlos Syndrome") with `category_type: diagnosis`
- Identity-level categories (e.g., "Deaf signing community," "wheelchair user") with `category_type: identity`
- Situation-level categories (e.g., "aging in place," "multiple conditions") with `category_type: situation`

Each finer-grained category links to one or more population codes via `related_categories`. This preserves BPC retrieval: a query entering via "Multiple Sclerosis" resolves to PopulationCategory[MS] which links to population codes [MOB, VIS, NEU, PAIN] and through those to the relevant BPC entries.

**Data model:** PopulationCategory has a self-referential `related_categories` array. Population codes are the coarser grouping; diagnosis/identity/situation categories are finer. The hierarchy is: population code → one or more diagnosis/identity/situation categories. The reverse: each diagnosis/identity/situation category → one or more population codes.

**Migration:** existing data model references to population codes (on Specification, BPCMetadata, Connection, Slug, Gap) are retained. PopulationCategory entities for population codes carry the same code string as their identifier. No existing references break.

---

### Q11. Diagnosis taxonomy source

**Resolution: No single source. Plain-language controlled vocabulary with clinical cross-references.**

The user-facing entry vocabulary is plain language: "Multiple Sclerosis," "Cerebral Palsy," "Ehlers-Danlos Syndrome," "Parkinson's Disease." Not ICD-11 codes, not SNOMED CT identifiers, not DSM-5 categories. Users — including disabled people and carers — think and speak in plain-language diagnosis names.

Each PopulationCategory entity of type `diagnosis` carries:
- `display_name`: plain-language name (multilingual)
- `synonyms`: array of alternative names, abbreviations, colloquial terms (e.g., "CP" for cerebral palsy, "MS" for multiple sclerosis, "hypermobile EDS" / "hEDS" for hypermobile Ehlers-Danlos syndrome)
- `clinical_references`: array of {system: `ICD-11` | `DSM-5` | `SNOMED-CT` | `OMIM`, code: string} — for traceability and interoperability, not for user-facing display
- `terminology_note`: where terminology is contested or varies by community (e.g., identity-first vs person-first, UK vs US usage), the note documents the choice and alternatives

**Rationale:** a single taxonomy source forces a single framing. ICD-11 is medical-model. DSM-5 is psychiatric. SNOMED CT is clinical-system interoperability. None of these is the user's mental model. Plain language with clinical cross-references serves user entry while preserving academic traceability.

**Inclusion criteria for diagnosis-level categories:** a diagnosis becomes a PopulationCategory when: (a) it has built-environment specification implications that are not fully captured by existing population codes or other diagnosis categories, AND (b) the evidence base (including THIN-BASE evidence) supports at least one specification or design consideration specific to that population. This prevents unbounded proliferation while ensuring coverage follows evidence.

---

### Q12. Mapping confidence classification

**Resolution: Classify all current populations. Classification is a documented assessment, not a label.**

Each PopulationCategory of type `diagnosis` or `population_code` carries a mapping confidence record:

```
mapping_confidence: {
  level: high | moderate | low | minimal
  basis: string  // summary of evidence supporting this classification
  sources: [string]  // references to clinical literature
  assessed_date: date
  assessor: string  // currently "solo author" — updated when consultation occurs
  notes: string  // caveats, known limitations
}
```

**Classifications for existing population codes:**

| Population | Confidence | Basis |
|---|---|---|
| MOB (manual wheelchair, full-time) | High | Wheelchair-environment interaction well-characterized; specifications tightly coupled to wheelchair dimensions and user anthropometrics |
| MOB (power wheelchair, full-time) | High | As above; power wheelchair dimensions and turning radii are specific and well-documented |
| MOB (ambulatory, aided) | Moderate | Aid type (cane/crutch/walker) and bilateral vs unilateral substantially change profile; sub-classification by aid type needed |
| VIS (no functional vision) | High | Built-environment implications (tactile wayfinding, auditory information, hazard protection) are well-characterized |
| VIS (low vision) | Moderate | Variation by condition (macular degeneration vs glaucoma vs diabetic retinopathy produces different visual field and acuity profiles); sub-classification by condition or visual field pattern useful |
| DEAF (profound, signing) | High for physical specifications; identity-level content adds considerations not capturable by axes alone |
| DEAF (hard of hearing) | Moderate | Variation by type (conductive vs sensorineural), hearing aid use, and CI use changes specifications; sub-classification useful |
| NEU (general) | Low | NEU spans stroke, ABI, MS, Parkinson's, motor neuron disease — each has fundamentally different trajectory, axis profile, and specification implications |
| DEM | Moderate | Dementia type (Alzheimer's vs vascular vs frontotemporal vs Lewy body) changes cognitive sub-profile and therefore specification emphasis; stage is a strong modifier; sub-classification by stage useful |
| NDV (Autism) | Low | Autistic individuals' built-environment needs vary enormously by sensory profile, communication profile, and cognitive profile; axis entry likely more useful than diagnosis defaults |
| NDV (ADHD) | Low | Built-environment implications are primarily executive-function and sensory-regulation related; axis entry captures this without diagnosis-level defaults |
| NDV/MH | Minimal | Mental health conditions' built-environment implications are highly individual and variable; axis entry is the appropriate path |
| PAIN (chronic pain generally) | Low | Pain conditions vary too much; specific diagnoses (fibromyalgia, CRPS, chronic back pain) have different environmental needs |
| PAIN (Fibromyalgia specifically) | Moderate | Characteristic profile (pain, fatigue, cold sensitivity, cognitive fog) is consistent enough for useful defaults with caveats |
| DBL (Deafblind) | Moderate-High | Combined sensory loss produces specific interaction requirements (tactile communication, guide-based navigation, specific spatial organization) that are well-characterized; variation by whether residual vision/hearing exists |
| OFS (general) | Low | OFS spans conditions with vastly different profiles; diagnosis-level entry is more useful |
| IntD | Minimal | Spectrum width exceeds predictive utility; axis entry only |

**Diagnosis-level classifications (illustrative — not exhaustive):**

| Diagnosis | Confidence | Basis |
|---|---|---|
| Complete SCI T6 | High | Level-specific functional profile well-documented in rehabilitation literature |
| Complete SCI C5 | High | As above; different level = different profile |
| Bilateral BKA with prosthetics | High | Functional profile reasonably predictable |
| Cerebral Palsy | Low | GMFCS level is strong predictor but within-level variation remains; MACS adds upper limb; both needed |
| Multiple Sclerosis | Low | Type (RRMS/SPMS/PPMS), stage, and individual variation make diagnosis-level defaults unreliable; EDSS sub-classification helps but doesn't fully resolve |
| Parkinson's Disease | Moderate | Hoehn & Yahr staging provides useful sub-classification; medication state (on/off) is a strong modifier |
| Retinitis pigmentosa | Moderate | Progressive but characteristic pattern (peripheral field loss → tunnel vision); stage matters |
| Ehlers-Danlos Syndrome (hEDS) | Low | Pain, fatigue, joint instability, autonomic dysfunction vary enormously between individuals |
| Stroke (completed, chronic) | Low | Affected side, severity, cognitive involvement, communication involvement all vary; axis entry usually more useful |
| Spina bifida | Moderate | Level-dependent like SCI but with additional considerations (hydrocephalus, latex allergy, cognitive profile) |
| Down syndrome | Moderate | More consistent cognitive and physical profile than IntD generally; sub-classification by independence level useful |
| ME/CFS | Low | Severity (mild/moderate/severe/very severe) is the key variable; axis entry for fatigue + cognitive + autonomic more useful than diagnosis defaults |

---

### Q13. Validation criteria for population-to-axis mappings

**Resolution: Three-tier validation framework.**

**Tier A validation (available pre-launch):** mapping aligns with published clinical literature on diagnosis-function relationships and with validated clinical sub-classification scaffolds. Systematic search documented per §6 transparency requirements. Assessment conducted by solo author.

**Tier B validation (target post-launch, Phase 1):** mapping reviewed by at least one clinical specialist (OT, rehabilitation physician, or relevant clinical specialist) with expertise in the population. Review documented with reviewer credentials, date, and outcome (confirmed / revised / contested).

**Tier C validation (target post-launch, Phase 2):** mapping reviewed by PWLE and/or DPO representatives for the population. Review documented with reviewer identity (or anonymized with consent), organization affiliation, date, and outcome. This is the CRPD Art 4.3 alignment step.

Each PopulationCategory carries its current validation tier. Pre-launch, all mappings are Tier A. Users can see the validation tier on drill-down. The tool's methodology statement explains the three tiers.

**Rationale:** this is honest about where the project is while committing to where it needs to go. Tier A is the minimum for publication — unsupported mappings don't publish. Tier B and C are sequential improvements that the project commits to pursuing as capacity develops.

---

### Q14. Clinical sub-classification scaffold fitness assessment

**Resolution: Fitness is conditional. Each scaffold assessed individually.**

Clinical sub-classification scaffolds (GMFCS, MACS, EDSS, Hoehn & Yahr, etc.) were validated for clinical purposes — prognostication, treatment planning, clinical communication. Using them as navigational sub-prompts in a design reference is a different purpose. The question is: does the scaffold's classification predict built-environment specification differences?

**GMFCS (Gross Motor Function Classification System, for CP):** Fit for navigational use. GMFCS levels predict mobility-environment interaction (Level I walks without restrictions → Level V transported in manual wheelchair). Built-environment specifications differ meaningfully between levels. The five levels map to meaningfully different axis profiles. **Assessment: suitable.**

**MACS (Manual Ability Classification System, for CP):** Fit for navigational use. MACS levels predict upper-limb-environment interaction (Level I handles objects easily → Level V does not handle objects). Built-environment specifications for controls, handles, and interfaces differ between levels. **Assessment: suitable.**

**EDSS (Expanded Disability Status Scale, for MS):** Partially fit. EDSS is heavily weighted toward ambulation (EDSS 1–4.5 are ambulatory; 5–6.5 are walking distance limited; 7+ are wheelchair). It under-represents cognitive, visual, and fatigue dimensions of MS that affect built-environment specifications. EDSS is useful for mobility-axis sub-classification but insufficient as a complete navigational scaffold for MS. **Assessment: suitable for mobility sub-classification; insufficient as sole scaffold; supplement with descriptive sub-classification for cognitive, visual, fatigue, thermoregulation axes.**

**Hoehn & Yahr (for Parkinson's):** Moderately fit. Five stages predict motor progression but don't capture non-motor symptoms (cognitive, autonomic, sleep) that affect built-environment specifications. **Assessment: suitable for motor sub-classification; supplement with descriptive sub-classification for non-motor axes.**

**No validated scaffold exists for:** EDS, fibromyalgia, ME/CFS, ABI, autism, ADHD, most mental health conditions. For these populations, descriptive sub-classification (plain-language prompts for functional profile) is the appropriate navigational mechanism. The armature should not invent scaffolds where validated ones don't exist — it should use plain-language prompts that help users describe the relevant functional profile.

**Documentation:** each scaffold used in the armature carries a fitness-assessment record: {scaffold_name, source, validated_purpose, navigational_fitness: suitable | partial | unsuitable, limitations, supplementary_mechanism}.

---

### Q15. Supplementary Volume (body size) intersection

**Resolution: Body size as a scope modifier, not an axis.**

Body size is not a disability. BAR is not a main taxonomy code. Large body size provisions belong in Supplementary Volume only. But body size affects spatial specifications that the armature queries — turning circles, corridor widths, seating dimensions, bathroom clearances, doorway widths.

**Mechanism:** a scope toggle (not an axis) labeled "include body size considerations" that, when active, applies Supplementary Volume dimensional adjustments to retrieved specifications. This surfaces larger spatial requirements where they apply without creating a body-size axis that implies large body size is an impairment.

**Implementation:** Supplementary Volume specifications are stored with a `scope_modifier: body_size` flag. When the toggle is active, the specification set includes these alongside the axis-matched specifications. They appear as additive dimensional notes: "If designing for larger body sizes, this dimension increases to [value]."

**Interface language:** the toggle should use neutral, non-stigmatizing language. "Include specifications for larger body sizes" or "adjust for body size range." Not "bariatric" in the user-facing interface (retain BAR as internal code for BPC retrieval).

---

### Q16. Respiratory/oxygen dependency axis

**Resolution: Include. Axis confirmed.**

Respiratory/oxygen dependency independently drives built-environment specifications that no other axis captures:

- Corridor width increases for O2 cart/concentrator turning radius
- Bathroom space increases for O2 equipment storage and maneuvering
- Electrical outlet placement and capacity for concentrators/ventilators
- Air quality specifications (filtration, ventilation rates) for respiratory-compromised users
- Elevator priority and sizing for O2-dependent users with equipment
- Emergency egress planning for ventilator-dependent individuals (power-dependent, cannot use stairs without power backup)
- Bedroom specifications for CPAP/BiPAP/ventilator positioning

These are not captured by ambulatory capacity, fatigue, or any other axis. The axis stays.

Values: `independent` | `supplemental O2 (portable)` | `CPAP/BiPAP (nocturnal)` | `ventilator-dependent`. Adding CPAP/BiPAP as a value — it's common, affects bedroom and bathroom specifications, and is distinct from portable O2 and from ventilator dependency.

---

### Q17. IntD axis mapping and THIN-BASE handling

**Resolution: Consistent with armature v4 §5.1. IntD is a population category with minimal mapping confidence. Axis entry is the specification retrieval mechanism. All IntD-derived specifications carry THIN-BASE disclosure.**

IntD as PopulationCategory:
- `category_type: population_code`
- `mapping_confidence: minimal`
- Content: authored from published corpus, covering wayfinding simplicity, sensory regulation, predictable layouts, Easy Read signage considerations, safe environments. All THIN-BASE disclosed.
- Related population codes: DEM (shared wayfinding/cognitive provisions), NDV (shared sensory/communication provisions)
- Axis entry: no pre-fill. User builds profile from cognitive sub-profile, communication, sensory regulation, and any co-occurring motor/sensory axes.

Sub-categories for IntD (e.g., "Down syndrome," "intellectual disability — independent living") may be created as `category_type: diagnosis` or `category_type: situation` entities with their own characteristic profiles where the evidence supports them. Down syndrome has a more consistent profile than IntD generally and warrants its own category at moderate mapping confidence.

---

### Q18. Easy Read

**Resolution: Role-layer content flag, not an axis value.**

Easy Read is a content format (short sentences, everyday words, images supporting text), not a functional impairment. It describes how content is presented, not who the person is or how they interact with the environment.

Easy Read is triggered by role selection (disabled person / carer role variants) combined with a content-format preference. The interface offers a content-format selector: "standard plain language" | "Easy Read format" | "technical." This is a presentation control, not a person-profile input.

Easy Read formatted content is a distinct content variant requiring specific authoring (not auto-generated from technical register). Where Easy Read content has been authored, it's served. Where it hasn't, the system serves standard plain language with a disclosure: "Easy Read version not yet available for this content."

**Rationale:** making Easy Read an axis value would imply that needing Easy Read is a personal impairment. It isn't — it's a communication preference appropriate for many populations (IntD, some DEM, low literacy, non-native-language readers, children). It belongs in the presentation layer.

---

### Q19. Intersectional identity

**Resolution: Age as a scope modifier. Gender as a scope modifier for specific building types. Other intersectional dimensions as contextual metadata on jurisdiction content, not as axes or scope dimensions.**

**Age:** a scope modifier (not an axis) with three values: `child (0–17)` | `adult (18–64)` | `older adult (65+)`. Age modifies specifications in ways the axis system cannot capture: child-height controls, child-scaled grab rails, playground-specific specifications, age-appropriate wayfinding. Older adult provisions overlap substantially with DEM and MOB axis-derived specifications but include age-specific considerations (falls prevention literature, age-related sensory decline patterns). The modifier adjusts the specification set — it doesn't replace axis-driven retrieval but adds age-specific specifications where they exist.

CRPD Art 7 alignment: children with disabilities have specific rights. The age modifier surfaces child-specific provisions. Art 7.3 (evolving capacity of children) is addressed in Mode S handoff notes for pediatric specifications.

**Gender:** a scope modifier for building types where gendered specifications exist: bathroom design (menstrual hygiene facilities, gender-neutral bathroom design, changing places), breastfeeding/lactation spaces in non-residential buildings, domestic violence refuge design. Not a universal modifier — for most specifications, gender is irrelevant. Active only when `spatial_context` includes building types where gendered specifications apply.

CRPD Art 6 alignment: women and girls with disabilities face multiple discrimination. The gender modifier surfaces gender-specific provisions where they exist in the built environment literature.

**Race, class, immigration status, incarceration status, housing tenure:** these affect access to environments and to advocacy, not the physical specifications of environments. A bathroom specification doesn't change by the user's race. However:

- **Housing tenure** affects jurisdiction content (what rights apply, what funding mechanisms exist, what modification permissions apply) and is already handled by the jurisdictional scope dimension.
- **Incarceration status** affects building type (custodial environments have specific design constraints — detained persons cannot freely leave, choice is restricted, accessible design in carceral settings intersects with security requirements). This is handled by spatial scope: if a building type for custodial/detention environments is included, its specifications carry the relevant constraints. Whether to include custodial-environment specifications is a content-coverage question, not an architecture question.
- **Race and class** do not affect physical specifications. They affect health outcomes, disability prevalence, access to diagnosis, access to advocacy, and experience of the built environment. These are real and important. They are not within scope of a design reference that specifies physical parameters of environments. The project's methodology statement can acknowledge that structural inequality affects who has access to well-designed environments — but the specifications themselves don't vary by race or class.

**Rationale:** the architectural principle is that scope modifiers exist where physical built-environment specifications vary by the modifier's value. Age and gender meet this test for specific building types. Race and class do not. This is not a claim that race and class don't matter — it's a scope determination for a design reference.

---

## A8 — Jurisdiction

### Q20. Jurisdictional scope implementation

**Resolution: Jurisdiction as a structured attribute on specifications, not a separate data layer.**

Each Specification entity carries `jurisdiction_scope`: an array of jurisdiction records. Each record:

```
{
  jurisdiction: string  // ISO 3166-1 country code + optional region
  code_framework: string  // e.g., "NCC Volume 1", "BS 8300-2:2018", "ADA Standards"
  code_reference: string  // specific section/clause
  compliance_status: mandated | recommended | best_practice | unaddressed
  effective_date: date | null
  notes: string | null  // jurisdiction-specific caveats
}
```

The jurisdictional scope dimension in the armature filters the specification set by jurisdiction. When a user selects a jurisdiction, the system:
1. Surfaces specifications that have a record for that jurisdiction, with the compliance status shown
2. Also surfaces specifications that have no record for that jurisdiction but are relevant by axis match, marked as "no jurisdiction-specific code reference available — best practice based on international evidence"

This serves the multijurisdictional mission: practitioners see what their jurisdiction mandates alongside what international evidence supports, even where their jurisdiction is silent.

**Jurisdiction comparison:** when a user selects multiple jurisdictions, the system shows specifications side by side with compliance status per jurisdiction. This is the "multijurisdictional comparison" feature that fills the international gap.

---

### Q21. Spatial scope coverage against CRPD

**Resolution: Spatial scope category list must cover all CRPD-relevant building types.**

Minimum spatial scope categories, mapped against CRPD articles:

- **Residential:** house, apartment, supported living, aged care facility (Art 19 — independent living; Art 28 — adequate standard of living)
- **Workplace:** office, industrial, retail, hospitality (Art 27 — work and employment)
- **Educational:** school, university, vocational (Art 24 — education)
- **Healthcare:** hospital, clinic, rehabilitation, dental, mental health facility (Art 25 — health)
- **Cultural/recreational:** theatre, cinema, museum, gallery, library, place of worship (Art 30 — cultural life)
- **Sport/leisure:** gym, pool, sports facility, park, playground (Art 30 — recreation and sport)
- **Transport:** station, airport, bus terminal, taxi rank (Art 20 — personal mobility)
- **Public realm:** streetscape, pedestrian crossing, public square, market (Art 9 — accessibility)
- **Commercial:** shop, restaurant, hotel, bank (Art 9 — accessibility of services)
- **Civic/government:** courthouse, government office, polling station, embassy (Art 29 — political participation)

This is a minimum set. Each category may have sub-categories. The spatial scope is extensible — new categories can be added without architectural change.

**Art 19 (independent living / deinstitutionalization):** residential categories should distinguish community-based settings from institutional settings. Specifications for institutional settings (e.g., aged care facility) should carry a note referencing Art 19's deinstitutionalization mandate and surfacing design features that promote autonomy, choice, and personal space — cross-cutting, not filtered out.

---

## A11 — Evidence Model

### Q22. Evidence assessment documentation — per-specification or per-BPC-entry?

**Resolution: Per-BPC-entry for the systematic review methodology; per-specification for the tier assignment and synthesis method.**

Two levels of documentation:

**BPC-entry level:** the systematic review methodology — search strategy, databases, date ranges, inclusion/exclusion criteria, screening counts, quality assessment of the evidence body. This is documented once per BPC entry because the evidence synthesis is conducted at population-topic level, not at individual-specification level. A BPC entry on "bathroom design for manual wheelchair users" has one search strategy that produces many specifications.

**Specification level:** the evidence marker (●/○), the tier assignment (which tier of the 7-tier hierarchy the strongest supporting evidence falls in), and the synthesis method indicator (direct/inferred/consensus). This is documented per specification because each specification may draw on different evidence within the same BPC entry — one specification may be directly supported by an RCT while another in the same BPC entry is inferred from clinical reasoning.

For ○-marked specifications, the inference basis is documented per specification: "Inferred from [source specification/principle] by [reasoning]. Evidence gap: [what evidence would resolve this]."

---

### Q23. Synthesis method indicator implementation

**Resolution: Three values, defined precisely.**

**Direct:** the specification value or range is drawn from one or more sources that directly measured or specified this parameter for this population in this built-environment context. Example: a study measured optimal grab rail height for manual wheelchair users transferring to WC; the specification cites this study.

**Inferred:** the specification value or range is derived from adjacent evidence by documented reasoning. The inference chain is explicit. Example: transfer space width for a specific wheelchair model is inferred from the wheelchair's turning radius (measured) plus clearance requirements (from ergonomic principles) plus user reach envelope (from rehabilitation literature). Each link in the chain is cited. The inference basis field documents the chain.

**Consensus:** the specification value or range reflects clinical or expert consensus without direct empirical support. Example: a specification for sensory room size in autistic-friendly design is based on expert consensus from practice guidelines, not from empirical measurement of optimal dimensions. The consensus source is cited.

**Implementation:** the indicator is a required field on every Specification entity. No specification publishes without it. This is a transparency obligation, not a quality judgment — consensus-based specifications are not inherently inferior to direct-evidence specifications. They are different kinds of knowledge, disclosed honestly.

---

### Q24. Evidence handling for population-level content

**Resolution: Population-level content on PopulationCategory entities uses a simplified evidence framework distinct from specification-level evidence grading.**

Population-specific design considerations (the authored content on PopulationCategory entities — e.g., "MS and heat sensitivity: implications for built-environment thermal design") are not individual specifications with single evidence markers. They are narrative evidence syntheses drawing on multiple sources.

Each piece of population-level content carries:
- `evidence_basis`: `literature_review` | `code_derived` | `clinical_guidance` | `dpo_position`
- `source_references`: array of citations
- `confidence`: `established` | `emerging` | `limited`
- `thin_base`: boolean

This is simpler than the 7-tier specification-level hierarchy because population-level content is contextual and integrative rather than parametric. The user needs to know "is this well-established or is the evidence thin?" — not the detailed tier assignment appropriate for a dimensional specification.

---

## A12 — Decision Protocol

### Q25. Role-based delivery mechanism

**Resolution: Content variant for the disabled-person and carer roles. Filter + emphasis adjustment for designer, OT, and policymaker roles.**

**Designer / OT / policymaker** roles view the same specification set with different emphasis:
- Designer sees: all specifications, full technical detail, conflict notes prominent, code references prominent
- OT sees: all specifications, Mode S handoff parameters prominent, assessment frameworks linked, clinical reasoning visible
- Policymaker sees: all specifications, compliance status prominent, jurisdiction comparison available, evidence grading prominent

These are filter + emphasis adjustments on the same specification records. No separate content authoring required per role.

**Disabled person / carer** roles receive a content variant: the specification data is the same, but the presentation includes authored plain-language framing that is not auto-generated from technical register. Each specification set, when presented in the disabled-person or carer role, is accompanied by:
- A plain-language summary of what the specifications mean in practice
- "Questions to ask your architect/designer" generated from Tier 1 specifications
- "Questions to ask your OT" generated from Mode S handoff parameters
- Evidence strength disclosure in plain language
- Rights framework reference (jurisdiction-dependent)

The plain-language summaries are a content artifact that requires authoring. They can be authored at the category level (e.g., "bathroom specifications for wheelchair users, plain language") rather than per-specification, which is manageable.

**Rationale:** auto-generating plain language from technical register produces stilted, unhelpful output. The disabled-person and carer roles deserve authored content, not machine-translated content. This is where "dignified and kind" becomes concrete.

---

### Q26. Carer role

**Resolution: Distinct role. Not proxy. Not supported-decision-making frame.**

The carer role is a person making or supporting environmental decisions in a care context. They have their own information needs:

- What environmental changes help for this person's condition?
- What should I prioritize given budget and practical constraints?
- What should I discuss with the disabled person vs decide independently vs defer to a clinician?
- What are the care-context considerations (night-time safety, supervision sight lines, equipment storage, respite space)?

The carer role presentation includes:
- All specifications (same data as other roles)
- Care-context framing (authored content, not auto-generated)
- Decision-support notes where specifications involve tradeoffs between autonomy and safety (e.g., stair access — mobility independence vs fall risk)
- Clear guidance on when the disabled person should be central to the decision (always, where capacity permits) and what that looks like in practice

The language is: "what to discuss with [person]" and "how to support [person] in making this decision" — not "what to decide on behalf of [person]."

For situations where the disabled person cannot participate in decisions (severe dementia, profound IntD with high support needs, some acute brain injury): the carer role content acknowledges this reality without defaulting to substituted-decision-making framing. The language shifts to "what [person's] comfort and dignity require" and "what the evidence says about environments that support [person's] wellbeing."

---

### Q27. Variable conflation check algorithm

**Resolution: Three-step check applied before surfacing any specification conflict.**

When the specification set contains apparent conflicts (two specifications for the same element with different values driven by different axes), the system applies:

**Step 1 — Variable identification.** Are the conflicting specifications operating on the same physical variable? Example: "wide corridor for wheelchair turning" and "narrow corridor for wall-trailing wayfinding" appear to conflict on corridor width. But wall-trailing operates on the *wall surface* (tactile continuity, handrail provision), not on the *corridor width*. The physical variables are different. No conflict. (This is CORRIDOR-W from project-standards.)

**Step 2 — If same variable, assess whether resolution is possible within the specification range.** Some apparent conflicts dissolve when ranges overlap. If Spec A says 1500–1800mm and Spec B says 1200–1600mm, the overlap zone (1500–1600mm) satisfies both. No conflict — surface the overlap zone.

**Step 3 — If same variable and no overlap, surface the conflict explicitly.** The conflict is real. The system surfaces:
- Both specifications with their axis basis and evidence
- The conflict type (dimensional, sensory, operational)
- The harm asymmetry if documented (which population is harmed more by the other's specification prevailing)
- The resolution pathway (Mode S handoff to OT/specialist with the specific conflict named)

**Implementation:** Steps 1 and 2 require structured metadata on specifications: `physical_variable` (what the specification acts on — corridor width, wall surface, lighting level, temperature, etc.) and `value` as a range rather than a point. Step 3 requires conflict-resolution metadata (harm asymmetry records, resolution pathways) stored on Connection entities or a dedicated conflict-resolution data structure.

**When compound functioning applies (§3.8 Step 0):** the three-step check runs first. If Step 3 identifies a real conflict AND the person profile has multiple non-baseline axes contributing to the conflict, the system additionally applies the compound functioning assessment: is the interaction non-additive? If so, the system surfaces the compound interaction mechanism and routes to Tier 2 with the interaction documented.

---

### Q28. §3.8 Step 0 UI surfacing

**Resolution: Inline annotation on affected specifications, plus a summary banner when compound interactions are detected.**

**Inline annotation:** each specification affected by a compound interaction carries a visible marker (distinct from the ● / ○ evidence marker). Suggested: a link icon or interaction icon with hover/tap text: "This specification interacts with [other specification] for profiles with [axis combination]. The interaction is [description]. Tier 2 assessment recommended for: [specific question]."

**Summary banner:** when the specification set contains one or more compound interactions, a banner appears above the specification matrix: "[N] specification interactions detected for this profile. These interactions may change the specifications listed. See details on affected items, or consult an OT for individual assessment."

**Plain-language role variant:** "Some of these recommendations interact with each other in ways that may change what's best for you specifically. Items marked with [icon] need individual assessment. Questions to raise with your OT: [generated list of specific interaction questions]."

**Not a modal/popup.** Not a warning that blocks access. Not an error state. It is information that supplements the specification set, surfaced proportionally — inline for details, banner for summary.

---

### Q29. Cultural variation accommodation

**Resolution: Jurisdiction-linked cultural context notes, not a separate cultural dimension.**

Built-environment design paradigms carry cultural assumptions. PAS 6463's sensory room model (private retreat) is culturally specific — in some cultural contexts, retreat is isolation and distress, not regulation and comfort. Bathroom design assumptions (seated vs squat toilet, bidet use, modesty requirements) are culturally variable. Residential space assumptions (open-plan vs compartmented, shared vs private sleeping, family vs individual orientation) are culturally variable.

**Mechanism:** cultural context notes are stored as metadata on specifications, linked to jurisdiction or cultural-region identifier:

```
cultural_context: [{
  region: string  // cultural region identifier, often but not always aligned with jurisdiction
  note: string  // how this specification may need adaptation for cultural context
  evidence_basis: string
  source: string
}]
```

These surface on drill-down. They do not override specifications — they contextualize them. The note says "in [cultural context], this specification may require adaptation because [reason]." The practitioner makes the judgment.

**Rationale:** a separate "cultural dimension" in the armature would imply that culture is a query parameter like ambulatory capacity. It isn't — it's a contextual lens that affects how specifications are applied. Jurisdiction-linked notes are the right mechanism for a design reference.

---

### Q30. Capability Approach integration depth

**Resolution: Specification-only for now. Capability-level framing is an honest limitation, acknowledged.**

The armature delivers specifications, not capability assessments. The distance between "transfer space ≥ 1500mm" and "this person can independently use the bathroom" is real. Bridging it would require the data model to encode what each specification enables or restricts for each axis profile — essentially a capability-inference engine on top of the specification database.

This is not achievable in the current project scope without:
- Empirical data on specification-capability relationships (which specifications actually enable which capabilities for which profiles — this is a research program, not a data model extension)
- A validated capability taxonomy for built-environment contexts (what capabilities are being assessed — mobility within the home? independent toileting? unsupervised cooking? social participation in the workplace? — each is a different capability with different specification dependencies)

**What the project can do now:** the plain-language role variant already performs partial capability translation: "with these specifications, you can expect [practical outcome]." This is authored content, not systematic capability inference. It's useful but not the same as genuine CA integration.

**Acknowledgment for the methodology statement:** "This reference delivers evidence-graded specifications for built environments. It does not deliver capability assessments — it does not systematically evaluate what capabilities a given built environment configuration enables or restricts for a given person profile. The distance between specifications and capabilities is a limitation of the current scope. Practitioners should evaluate capability implications through professional judgment and co-design with the disabled person."

**Post-launch possibility:** if the project develops capability-specification relationship data (possibly through post-occupancy evaluation research or through PWLE consultation on "does this specification actually enable independent use?"), capability-level framing could be added. The data model does not foreclose this — specification entities can gain capability metadata without schema restructuring.

---

### Q31. Plain-language register specification

**Resolution: Authored per category-topic combination, governed by plain-language standards, tested with target audience.**

Plain-language content for the disabled-person and carer roles is:

**Authored, not auto-generated.** Technical-to-plain-language translation by algorithm produces stilted, patronizing, or inaccurate output. Plain-language content is written by a person who understands both the technical content and the target audience.

**Governed by a stated plain-language standard.** The project adopts the International Plain Language Standard (ISO 24495-1:2023) as its reference framework. Key requirements: purpose clearly stated, content organized for the audience, sentences are short and direct, words are common and well-known, design supports comprehension.

**Scoped to category-topic combinations, not per-specification.** A plain-language summary for "bathroom specifications for manual wheelchair users" covers the specification set for that combination. This is manageable at the authoring level — the number of category × topic × population combinations that need plain-language content is finite and can be prioritized by usage frequency.

**Tested with target audience where possible.** Pre-launch: tested with available readers (which may be limited by solo authorship). Post-launch: feedback from disabled-person tool users drives revision. Testing methodology: readability scoring (Flesch-Kincaid or equivalent) as a floor, not a ceiling — readability scores don't capture whether content is actually useful to the reader.

**Easy Read is distinct from plain language.** Easy Read (short sentences + supporting images, formal accessibility format per Mencap/CHANGE guidelines) is a separate content format. It is not the default plain-language register — it's an additional format available where authored. See Q18.

---

## Website Build

### Q32. Tool accessibility

**Resolution: Specific commitments, not just WCAG conformance level.**

| Commitment | Standard | Rationale |
|---|---|---|
| WCAG 2.2 AA conformance | W3C | Minimum for public-sector digital services in most jurisdictions |
| Keyboard-only full functionality | WCAG 2.1.1, 2.1.2 | Serves motor-impaired users, switch users, and users without pointer devices |
| Screen reader full functionality | WCAG 4.1.2, 1.3.1 | Serves blind and low-vision users — a primary population for this tool |
| Target size minimum 24×24px, aim 44×44px | WCAG 2.5.8 (AA), 2.5.5 (AAA) | Axis selection controls must be operable with reduced precision |
| No time limits | WCAG 2.2.1 | Profile construction and specification review cannot be time-limited |
| Redundant entry prevention | WCAG 3.3.7 | User shouldn't re-enter axis values when adjusting scope |
| Focus not obscured | WCAG 2.4.11 | Faceted query interface with overlapping panels must not obscure focus |
| Dragging alternatives | WCAG 2.5.7 | Any slider-based axis selection must have non-drag alternative |
| Consistent help location | WCAG 3.2.6 | Help, glossary, and definitions in consistent locations |
| No cognitive function test for authentication | WCAG 3.3.8 | If accounts introduced, no CAPTCHA or puzzle |
| Color not sole information carrier | WCAG 1.4.1 | Evidence markers, tier indicators, conflict flags not color-only |
| Text alternatives for all non-text content | WCAG 1.1.1 | Evidence marker symbols, icons, diagrams |
| Responsive to 320px width | WCAG 1.4.10 | Mobile accessibility |

**Beyond WCAG:**
- Anonymous use without account creation
- No data submission required for basic queries
- Accessibility statement published (conformance level, known issues, contact for complaints, alternative-format requests)
- Tested by disabled people across served populations before launch

---

### Q33. Population entry usability

**Resolution: Search-first with categorized browse as fallback.**

**Primary mechanism:** search-as-you-type with fuzzy matching. User types "MS" or "multiple sclerosis" or "walking difficulties" and gets matched results. Search indexes: PopulationCategory display_name, synonyms, and plain-language descriptions. Fuzzy matching catches misspellings and partial matches.

**Fallback mechanism:** categorized browse. Population categories organized by cluster (mobility, sensory, cognitive, pain/fatigue, etc.) with expandable groups. Each group shows its constituent categories.

**Redirect mechanism:** when search terms match functional descriptions rather than population names ("I have trouble gripping things"), the system offers: "You can describe your functional profile directly" with a link to axis entry, plus any population categories whose descriptions mention the search term.

**Recently-viewed:** if the user has used the tool before (via localStorage or session), recently-viewed populations appear as quick-access options. Privacy-respecting: no server-side tracking; local-only; clearable.

---

### Q34. Shareable query URLs

**Resolution: URL-encoded query state, human-readable where possible.**

Every query state (person profile + scope + role) generates a stable, shareable URL. Format:

```
/query?population=cerebral-palsy&gmfcs=3&macs=2
  &axes=ambulatory:aided,grip:reduced-precision,sensory-reg:hyper
  &scope=spatial:bathroom,stage:dd,jurisdiction:au-ncc
  &role=designer
```

Parameters are human-readable slug values, not opaque IDs. This means URLs are partially self-documenting — a practitioner can read the URL and understand roughly what query it represents.

**Privacy consideration:** the URL contains disability-related information. When sharing a query URL, the system displays a note: "This link contains information about the person profile you've described. Share only with people who need this information." This is a privacy reminder, not a gate — the URL is shareable by design.

**Persistence:** URLs are stateless — they encode the query, not server-stored data. They work without an account. They work indefinitely (as long as the referenced population categories and axes exist in the system).

---

### Q35. Export formats

**Resolution: Three formats, all accessible.**

**PDF:** specification matrix formatted for print and filing. Includes: full specification set, evidence markers with text equivalents, jurisdiction references, Mode S handoff notes. Accessible PDF (tagged, reading-order correct, alt text on visual elements). Generated server-side.

**Plain text / Markdown:** specification set as structured text. Suitable for pasting into documents, emails, reports. No visual formatting dependencies.

**Accessible HTML:** specification set as a standalone HTML page. WCAG-compliant. Self-contained (no external dependencies). Suitable for: local saving, integration into other documents, sharing via email as attachment.

**Not included pre-launch:** BIM/IFC integration, JSON/API export, CSV. These are post-launch considerations.

Each export carries: the query parameters that generated it, the date of generation, the methodology statement link, and the validation provenance disclosure.

---

### Q36. Evidence marker accessible equivalents

**Resolution: Dual-encoded — symbol plus text.**

●-marked specifications: the symbol ● is accompanied by a `title` attribute and a screen-reader-accessible label: "Evidence-based." In the specification matrix, a column header reads "Evidence" and each cell contains either "Evidence-based" or "Inferred" with the symbol as a visual shorthand.

○-marked specifications: the symbol ○ is accompanied by: "Inferred — evidence gap disclosed" as accessible text. On drill-down, the inference basis is available.

Color is never the sole differentiator. The symbols differ by fill (filled vs unfilled), not by color. Text equivalents are always present.

In the plain-language role variant, symbols are replaced entirely by text: "This recommendation is supported by direct research evidence" (●) or "This recommendation is based on clinical reasoning — direct research evidence is not yet available for this specific point" (○).

---

### Q37. Mobile-responsive design

**Resolution: Responsive down to 320px, with progressive disclosure of complexity.**

The specification matrix is the most complex visual element. On mobile:

- Specification list view replaces matrix view (one specification per card, swipeable/scrollable)
- Each card shows: element name, value, tier, evidence marker
- Expand for: jurisdiction, conflict notes, provenance
- Filters (axes, scope) collapse into a filter panel accessible via button
- Person profile summary visible at top, tappable to edit

The profile-construction interface on mobile:
- Cluster-based navigation (6 clusters, not 18 axes simultaneously)
- Each cluster expands to show its axes
- Each axis is a single selection control (dropdown or radio, not slider)
- "Skip / unknown" available on every axis
- Progress indicator showing clusters completed

Population entry on mobile:
- Search-first (search bar prominent)
- Categorized browse as scrollable list
- Population page as single-column layout

**Touch targets:** 44×44px minimum for all interactive elements. This exceeds WCAG AA (24×24px) and meets AAA (44×44px). Non-negotiable for a tool serving users with motor impairments using mobile devices.

---

## Summary of entity model changes

The resolutions above produce the following A3 amendment requirements:

**New entity type:**
- PopulationCategory (Q2, Q10, Q11, Q12, Q13, Q17)

**Extended existing entities:**

Specification:
- `axes_applicable` array (Q3)
- `jurisdiction_scope` structured array (Q1, Q20)
- `synthesis_method_indicator` + `inference_basis` (Q5, Q23)
- `physical_variable` identifier (Q27)
- `adjustability_metadata` structure (Q1)
- `tier2_handoff` structure (Q1)
- `cultural_context` array (Q29)
- `version_history` array (Q5)
- `last_review_date` (Q5)

EvidenceSource:
- `search_strategy` structure (Q5)
- `screening_counts` structure (Q5)
- `quality_assessment` structure (Q5)

BPCMetadata:
- `synthesis_method` (Q5)
- `last_review_date` + `review_cycle` (Q5)
- `quality_summary` (Q5)

Gap:
- `user_facing` boolean (Q5)
- `population_level` boolean (Q5)
- `surfacing_method` enum (Q5)

**Scope modifiers (query-layer, not entity-level):**
- Body size toggle (Q15)
- Age modifier (Q19)
- Gender modifier (Q19)

**Axis set:** 18 axes in 6 clusters (Q7), with cognitive processing carrying a structured sub-classification (Q8). Communication axis gains `sign language user` value (Q9). Respiratory axis confirmed with expanded values (Q16).

---

## Resolved vs remaining

**Fully resolved (30):** Q1, Q2, Q3, Q4, Q5, Q6, Q8, Q9, Q10, Q11, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32, Q33, Q34, Q35, Q36, Q37.

**Resolved with caveat (5):**
- Q7 (axis set): resolved at 18 axes, but final validation requires PWLE/DPO consultation per §9. Axis framing (interaction vs deficit) resolved as input-layer person-descriptive / output-layer interaction-framed — but specific axis names and help text require authoring and testing.
- Q12 (mapping confidence): all current populations classified, but classifications are Tier A validation only (solo author against published literature). Tier B/C validation per Q13 framework is a post-launch commitment.
- Q25 (role-based delivery): mechanism resolved, but plain-language content requires authoring work that is substantial and not yet scoped.
- Q26 (carer role): role defined, but carer-context content requires authoring.
- Q29 (cultural variation): mechanism resolved, but cultural context notes require authoring and validation by culturally competent reviewers.

**Remaining (2):**
- Q7 sub-question: the specific interaction-framed axis names and help text are authoring tasks, not architectural decisions. They require writing and testing.
- Q31 sub-question: prioritization of which category-topic combinations get plain-language content first is a content-planning decision, not an architectural one. Recommend prioritizing by: (a) population size, (b) specification set size, (c) likelihood of disabled-person tool-user queries. MOB-bathroom, MOB-bedroom, VIS-wayfinding, DEAF-communication-systems are likely first priorities.
