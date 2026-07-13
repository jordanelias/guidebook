# Pre-Decision: Person-Profile Armature — Query Architecture for a Research-Grounded Built-Environment Design Reference

**Status:** PRE-DECISION DRAFT — captured intent for Stage A formalization. NOT decision-quality. Sonnet-drafted; flagged for Opus synthesis at A7 / A12.
**Date:** 2026-04-28 07:16
**Version:** v4. Replaces v3 (2026-04-27 20:20). Full lineage: v1 (`governance/pre-decision-multimodal-access-armature.md`, 2026-04-26 20:24, commit 9c2ee87) → v2 (2026-04-26 22:38) → v3 (2026-04-27 20:20) → v4.
**Scope:** Query architecture for the guidebook website — how practitioners and disabled people find relevant specifications. Data model implications for Stage A phases A3, A7, A8, A11, A12.
**Out of scope:** Visual design, interaction patterns, website implementation, post-launch features (testimony, community contributions, API).

---

## 1. What this project is

A research-grounded, multijurisdictional, multilingual built-environment design reference. It fills an international gap by surfacing codes, standards, research evidence, and design practices that relate to inclusive built environments across jurisdictions and populations, organized so practitioners worldwide can find what they need.

The project's tools are design interventions and architectural solutions. Its authority derives from its research base — the intensive evidence synthesis underpinning every specification. It is an advocacy project in orientation (per Core Doctrine) but a design reference in function.

What this document does: specifies the query architecture (the armature) that lets users navigate from "who am I designing for" to "what does the evidence say about this built environment element for this person, in this jurisdiction."

What this document does not do: specify the final axis set, the population taxonomy source, the output schema, the naming convention, the validation authority, or any visual/interaction design. All are flagged as decisions for named Stage A phases.

---

## 2. Definitions

**Armature.** The query architecture. The logical structure through which users navigate the guidebook's content. Named from sculpture: the internal supporting framework around which form is built. The axes and scope filters are the armature; population content and specifications are what is built onto it. Naming is an open question for A7 — the metaphor may not translate across languages.

**Functional axis.** A dimension of person-environment interaction along which built-environment specifications vary. Aggregations of ICF body function and activity codes, reframed where possible as interaction variables rather than person-deficit descriptors (e.g., "grip interaction requirement" rather than "grip impairment"). Designed for navigational utility in a design reference, not for clinical assessment.

**Population category.** A grouping recognized in the research literature, clinical practice, code frameworks, or disability communities, around which evidence is organized. Diagnoses, identity descriptors, and community-recognized population groupings. Each carries its own content — research synthesis, design considerations, code references — authored from the published corpus. Population categories exist because the research base is organized by population, not because they are convenient labels for axis configurations.

**Person profile.** The set of axis values describing who the design is for. A query-time construct — not a persisted data entity. It indexes into Specification entities via their axis attributes. Built via population-category entry (with axis pre-filling where the population-to-axis mapping is confident) or via direct axis entry, or both.

**Specification.** An evidence-graded, jurisdiction-mapped, tier-assigned built-environment design parameter. The primary content the armature retrieves.

**Evidence marker.** ● (filled circle) = specification supported by direct evidence (tiers 1–6 in the project hierarchy). ○ (empty circle) = specification inferred from clinical reasoning, adjacent evidence, or expert consensus — evidence gap disclosed. Every specification carries one.

**Synthesis method indicator.** How a specification was derived from its evidence base: direct (specification drawn from source evidence), inferred (specification derived from adjacent evidence by documented reasoning), or consensus (specification reflects expert or clinical consensus without direct empirical support). Complements the evidence marker by disclosing the derivation pathway, not just the evidence quality.

**Mapping confidence.** The degree to which a population category predicts a functional-axis profile, derived from clinical evidence on diagnosis-function relationships. Ranges from high-predictive (complete SCI at a named level) to minimal-predictive (IntD spectrum). A property of each population, not an architectural setting.

**Design hierarchy.** Universal Mode (Universal Design / Code Compliance — baseline, all profiles). Tier 1 (Population-Informed Inclusive Design — surfaced by axis match, evidence-graded ranges). Tier 2 (Individual Assessment — the system identifies the functional parameter requiring OT/specialist assessment and the range within which resolution occurs, but does not resolve).

**PWLE.** Person With Lived Experience (of disability).
**BPC.** Best Practice Compendium — population-organized evidence synthesis files.
**KFA.** Key Functional Attribute — structured specification entity.
**DAR.** Design for Ageing and Resilience — cross-cutting, mandatory at all tiers and design stages.

---

## 3. The gap this architecture addresses

The guidebook contains multijurisdictional, multilingual, evidence-graded specifications for built environments serving disabled people. Without a query architecture, this content is a linear document that cannot serve practitioners who need filtered, population-specific, jurisdiction-relevant, design-stage-appropriate specifications.

The query architecture must handle:

- Different populations require different specifications. The current population taxonomy (MOB, VIS, DEAF, NEU, DEM, NDV, etc.) is too coarse to drive specification selection at the granularity the evidence supports. Sub-population distinctions that change specifications (manual vs power wheelchair, low vision vs no functional vision, reduced grip vs absent grip) are not captured by population code alone.
- The research literature is organized by population, not by functional axis. Retrieving specifications requires both: axes for granular matching, population categories for accessing the population-organized evidence base.
- Different jurisdictions have different codes, standards, and practices. The same specification may be code-mandated in one jurisdiction, best practice in another, and unaddressed in a third.
- Different design stages require different levels of detail.
- Different users (designer, OT, policymaker, disabled person, carer) need the same specifications presented differently.

---

## 4. Architecture

### 4.1 Person profile — who the design is for

The person profile is the set of functional-axis values describing the person for whom the environment is being designed. It is the primary query input for specification retrieval.

The profile is a query-time construct. It is not a 7th entity type in the A3 data model. It is a session-level parameter set that indexes into Specification entities.

### 4.2 Two content layers

The data substrate has two content layers. Neither reduces to the other. Both are first-class.

**Layer 1 — Functional axes.** The dimensions along which built-environment specifications vary. These are what the data model queries against. A specification for transfer space varies by ambulatory capacity, postural control, transfer independence, and upper-limb function. The axes capture the person-environment interaction variables that differentiate specifications.

**Layer 2 — Population identity.** Groupings recognized in research, clinical practice, codes, and disability communities. Each population category carries its own content: research synthesis, design considerations specific to that population, code references, sub-classification scaffolds where applicable, and characteristic axis profiles where the evidence supports them. This content is authored from the published corpus. It exists because the research base is organized by population and because populations carry clinical, community, and identity significance that axes do not capture.

**The relationship between layers is explicit, empirically grounded, and variable.** The mapping confidence between a population category and a functional-axis profile is a property of the clinical evidence for that population:

| Mapping confidence | Characteristic | Examples | Interface behavior |
|---|---|---|---|
| High-predictive | Diagnosis reliably predicts functional profile | Complete T6 SCI; bilateral BKA with prosthetics; total bilateral hearing loss | Confident axis pre-fill; narrow defaults |
| Moderate-predictive | Stage or sub-classification needed | Retinitis pigmentosa (stage-dependent); Parkinson's (stage-dependent); rheumatoid arthritis | Sub-classification prompt using validated clinical scaffolds (where available); stage-dependent pre-fill |
| Low-predictive | High individual variation within diagnosis | MS; CP; ABI; EDS | Explicit "high variation" disclosure; sub-classification scaffold offered (EDSS, GMFCS/MACS); axes left for user to specify |
| Minimal-predictive | Diagnosis does not usefully predict functional profile | IntD (spectrum width exceeds predictive utility); "multiple conditions"; "aging-related decline" | No axis pre-fill; population-level content provided; user builds profile directly via axes |

The mapping confidence level for each population is itself a claim requiring documentation. Source evidence for each assignment should be traceable to published clinical literature on diagnosis-function relationships.

### 4.3 Entry paths

Two parallel paths. Both retrieve from the same substrate. Neither is primary. Neither is fallback.

**Via population identity.** Practitioner or disabled person selects a population category. System delivers population-specific content (research synthesis, design considerations, code references) and — with confidence appropriate to that population's mapping level — offers an axis profile as a starting point for specification retrieval. The user can adjust any axis value. The population identity is the organizing frame; axes are available as a refinement tool.

**Via functional description.** Practitioner or disabled person builds a functional profile directly from axes. System retrieves axis-matched specifications. System surfaces relevant population categories where the axis profile is common ("this profile is described in MS, EDS, fibromyalgia research — see those pages for population-specific design considerations"). The functional description is the organizing frame; population identity is available as context.

**Combining paths.** The natural workflow for many users is population entry followed by axis refinement: select a population, review the characteristic axis profile, adjust to match the specific individual. Where adjustments diverge from the population's characteristic profile, the system surfaces the divergence transparently. This is not a separate "mode" — it is normal use of the two-layer system.

**Reverse retrieval.** The research base (BPC entries) is organized by population code. When a user enters via axes only, the system must map from axis values to relevant population codes to retrieve applicable BPC entries. This reverse-mapping algorithm is architecturally significant — it determines whether axis-only entry can deliver the same evidence depth as population entry. The algorithm is a joint A3/A7 decision.

### 4.4 Scope — what the user wants to know

Five orthogonal sub-dimensions:

| Sub-dimension | Content | Notes |
|---|---|---|
| Categorical | Item categories per A3 entity model (A–K) | Primary organizational structure |
| Topic | Wayfinding, lighting, acoustics, thermal, flooring, controls, etc. | Cross-cuts categories |
| Spatial | Room type, building type, indoor/outdoor | Includes residential, workplace, educational, healthcare, cultural/recreational, transport, public realm |
| Temporal | Design stage: brief, schematic, DD, construction, RFO, POE | DAR is cross-cutting and mandatory at all stages — not a filter option |
| Jurisdictional | Country/region, code framework, standard | Enables multijurisdictional comparison |

User selects any combination. Empty filters surface everything in that sub-dimension.

### 4.5 Role — presentation layer

Role determines how query results are presented. Same specifications, different emphasis and register.

| Role | Emphasis | Register |
|---|---|---|
| Designer / architect | Specifications, conflict notes, code references, Universal-/Population-Mode values, detail-level guidance | Technical |
| OT / healthcare professional | Functional ranges, Person-Mode resolution parameters, assessment frameworks | Clinical |
| Policymaker / regulator | Code compliance mapping, jurisdiction comparison, evidence grading, economic evidence | Policy |
| Disabled person / advocate | Plain-language specifications, rights framework, what to ask for, evidence strength disclosure; the advocacy-brief use-pattern (audience-priority.md, G5) carries the code-vs-evidence delta | Plain-language |
| Carer / family / support worker | Plain-language, care-context framing, what environmental changes help, how to support environmental decisions | Plain-language (care-context) |

**Carer as distinct role.** The carer is not a proxy for the disabled person. A carer navigating environmental decisions (home modifications for a parent with dementia, bedroom design for an autistic child, workplace adjustments for a partner with EDS) has their own information needs and decision context. See §8 item 14.

**Role does not change the underlying data.** It changes what is emphasized, what language register is used, and what contextual framing accompanies specifications.

### 4.6 Output

The armature returns evidence-graded specifications. Each specification surfaced carries:

**Visible in the specification matrix:**
- Design mode (Universal / Population / Person)
- Evidence marker (● / ○)
- Specification value or range
- Jurisdiction scope (which code frameworks address this element)
- Conflict flag (where axis interactions produce competing requirements)

**Available on drill-down:**
- Synthesis method indicator (direct / inferred / consensus)
- Inference basis (for ○-marked and inferred specifications: derived from what, by what reasoning)
- Evidence provenance summary (sources, search strategy, inclusion criteria, date range)
- Assessment basis for tier assignment (traceable to documented quality assessment)
- BPC entry linkage
- Population-specific considerations (linked from Layer 2)
- Version and last-review date
- Authorship and validation provenance

**Cross-specification features:**
- Compound functioning flag (§3.8 Step 0) where multiple non-baseline axes interact non-additively
- Variable conflation check applied before surfacing apparent conflicts
- Person-Mode handoff with the functional parameter driving assessment named and the resolution range specified
- "Adjustable" provisions carrying population operability notes per project-standards rule

**Export:** specification matrix exportable as PDF, plain text, and accessible HTML. Shareable query URLs preserving query state.

### 4.7 Worked example

**Input:** Role = Designer. Person profile via population entry = "Cerebral palsy" → system flags low-predictive mapping confidence, prompts for GMFCS/MACS sub-classification → user selects GMFCS III (walks with assistive mobility devices) / MACS II (handles most objects but with reduced quality/speed) → axis profile pre-filled: ambulatory [aided — walker/crutches], postural control [reduced], transfer [assisted], grip [reduced precision], sensory regulation [typical unless adjusted]. User adjusts sensory regulation to [hyper-responsive]. Scope = Spatial[bathroom], Temporal[DD], Jurisdictional[Australia — NCC/AS 1428].

**Designer output:** filtered specification matrix, DD-relevant bathroom elements:

Each entry shows the specification value/range, design tier, evidence marker, and Australian code reference where applicable. Conflict notes surface where reduced postural control interacts with transfer space geometry (grab rail position for walker-to-WC transfer differs from wheelchair-to-WC transfer — specification clarifies which pattern applies at GMFCS III). Sensory-regulation adjustment surfaces lighting-level specification with dimming requirement. Tier 2 flags appear where individual variation within GMFCS III requires OT assessment (e.g., specific grab rail force tolerance — the functional parameter "maximum sustainable grip force during weight-bearing transfer" is named, the assessment range is specified).

Drill-down on any specification shows: evidence sources, synthesis method, BPC entry, last-review date. Link to CP population page for CP-specific design considerations (fatigue management in bathroom design, fall-risk considerations specific to CP gait patterns).

**Same profile, disabled-person output:** same specifications, plain-language register. "For a bathroom designed for someone who walks with crutches or a walker and has reduced hand control: the door needs to be wide enough to walk through with your mobility aid, the toilet needs grab rails positioned for how you transfer, taps need to work without gripping, and lighting should be adjustable if you're sensitive to bright light." Evidence markers translated: "This recommendation is supported by direct research evidence" (●) or "This recommendation is based on clinical reasoning — research evidence is not yet available for this specific point" (○). Specifications as ranges with context rather than bare values. "Questions to raise with your architect" and "questions to raise with your OT" lists generated from Person-Mode handoff flags.

---

## 5. Impairment axes — candidate set for A7

The candidate set below makes the architectural concept testable. It is not a recommendation. A7 (Opus synthesis) decides the final set, ICF cross-mapping, representation format, and validation criteria. This set carries reduced-confidence warning per Sonnet/Opus boundary.

The candidate set has 20 axes in 6 clusters. A7 may consolidate, expand, or restructure.

Axes are framed as person-environment interaction dimensions where possible. Where framing remains person-deficit (e.g., "cognitive processing"), A7 should evaluate whether interaction framing is achievable without losing navigational utility.

External classification systems referenced (GMFCS, MACS, EDSS) are validated for specific clinical purposes. Their repurposing as navigational sub-classification scaffolds in a design reference is a methodological choice requiring documentation — these instruments were designed for clinical communication, not for built-environment specification retrieval. A7 to evaluate fitness for this purpose and document the assessment.

### Mobility & posture
- **Ambulatory capacity** — full / aided (cane/crutch) / walker / manual wheelchair / power wheelchair / bed-based. Ambiguity for A7: does "full" include prosthetic users? Prosthetic gait differs functionally from intact-limb gait (joint range, fatigue, terrain response).
- **Postural control** — full / reduced seated balance / minimal. Independent of ambulatory capacity.
- **Transfer capacity** — independent / assisted / dependent.
- **Vestibular function** — typical / motion-affected / severely affected. Distinct from postural control; affects uneven surfaces, stairs, dynamic environments.

### Limb presence & upper limb function
- **Limb presence** — modifier: bilateral present / unilateral upper absence / bilateral upper absence / unilateral lower absence / bilateral lower absence / multiple. Applied alongside reach, grip, and ambulatory axes.
- **Reach envelope** — full / reduced overhead / reduced forward / minimal.
- **Grip & manipulation** — full / reduced force / reduced precision / minimal/absent.

### Sensory
- **Visual acuity** — full / low vision / no functional vision.
- **Visual processing** — typical / CVI or processing-affected.
- **Visual field** — full / restricted (peripheral or central loss).
- **Light tolerance** — normal / photophobic.
- **Auditory acuity** — full / hard of hearing / no functional hearing.
- **Auditory processing** — typical / APD / hearing-aid+loop dependent / CI dependent.
- **Sensory regulation** — typical / hyper-responsive / hypo-responsive / mixed.

**Deaf cultural/linguistic identity — open question for A7.** Auditory axes are medically framed. For Deaf signing communities, the relevant design consideration is linguistic (sign-language-first communication, visual-alert systems as primary not compensatory, video-relay infrastructure) rather than auditory. A7 should evaluate whether Deaf cultural/linguistic identity requires a distinct population category entry path or a distinct axis, rather than placement within the auditory cluster. This is an identity-recognition question, not just a clinical-framing question.

### Cognitive & communication
- **Cognitive processing** — A7 must resolve granularity. Three-point ordinal (intact / reduced / severe) is too coarse for a dimension where the project distinguishes DEM (memory-predominant), NEU (executive/processing speed), NDV (abstract reasoning/flexibility), and IntD (global/specific learning). Candidate sub-axes: memory / executive function / processing speed / abstract reasoning. Whether these are separate axes or a structured sub-classification within a single axis is an A7 decision.
- **Communication & speech** — typical / dysarthria / AAC user / non-verbal.

### Physiological
- **Pain & fatigue envelope** — unrestricted / limited (pacing required) / severely limited.
- **Thermoregulation** — intact / heat-sensitive / cold-sensitive / both. Drives confirmed co-occurrence conflicts with documented harm-asymmetry resolutions (FMS cold pain hypersensitivity vs MS/SCI cooling requirement).
- **Continence & toileting independence** — independent / assistance with timing / assistance with mechanics / fully dependent.
- **Respiratory / oxygen dependency** — independent / supplemental O2 (portable) / ventilator-dependent. Affects corridor width, bathroom space, air quality, elevator priority, emergency egress.

### 5.1 IntD mapping

IntD (Intellectual Disability) has no standalone population code — provisions proxied through DEM and NDV per project-standards. All IntD specifications carry THIN-BASE disclosure.

IntD maps to minimal-predictive confidence level. The diagnostic label does not usefully predict a functional-axis profile because the spectrum (mild independent-living adult to severe-profound with 24/7 support) spans nearly the full range of multiple axes simultaneously. Bottom-up axis entry is a more honest and more useful path for retrieving IntD-relevant specifications than diagnosis-to-profile mapping.

IntD exists as a population category (Layer 2) with its own content: design considerations from the published corpus, THIN-BASE disclosed where evidence is thin, with axis entry as the specification retrieval mechanism.

**Tool-user scope.** The armature is designed for users with the capacity to navigate population taxonomies and functional-axis frameworks. Built-environment specifications relevant to IntD populations are fully queryable by designers, OTs, carers, and policymakers. A separate cognitively accessible interface may be appropriate post-launch; it is out of scope for this architecture. This is a scope decision, not a value judgment about IntD populations. It is revisitable.

### 5.2 Diagnosis-to-profile mapping

Mappings are navigation hypotheses, not prescriptions. Consistent with Core Doctrine: "Disability populations are not uniform."

Mappings require validation. Pre-launch validation basis: alignment with published clinical literature on diagnosis-function relationships and validated clinical sub-classification scaffolds. Direct PWLE/DPO consultation has not occurred; this is a structural limitation, disclosed. Post-launch validation through consultation infrastructure is a project commitment, not an aspiration.

Each mapping should be documented with: source evidence for the axis-profile assignment, assessment process, mapping confidence classification and its basis, date of last review, and identified gaps. This documentation is the mapping's provenance record, analogous to the evidence provenance carried by specifications.

### 5.3 Population code relationship

The existing project taxonomy uses 11 population codes (MOB, VIS, DEAF, NEU, DEM, NDV, NDV/MH, PAIN, DBL, OFS, IntD) plus supplementary codes (CHD, LPA, EXH, BAR). Population codes are embedded throughout the data model — all 6 A3 entity types reference them.

Under the two-layer architecture, population codes become one type of population category in Layer 2. They coexist with diagnosis-level categories (which may be finer-grained than population codes) and identity-level categories (e.g., Deaf signing community). The data model retains population codes as an organizational structure for the existing BPC corpus while gaining the finer-grained population categories that the armature requires. The coexistence model is an A7 decision.

### 5.4 Supplementary Volume intersection

BAR is not a main taxonomy code. Large body size provisions belong in Supplementary Volume only. Body size affects spatial specifications the armature queries. Mechanism for integrating Supplementary Volume data without creating a BAR axis in the main taxonomy is an A7 decision.

### 5.5 Population entry usability

Population entry requires searching or selecting from a potentially large list. The interface must accommodate: search-as-you-type, plain-language synonyms, grouped/categorized presentation, and the ability to describe function rather than name a condition (redirecting to axis entry). Website-build requirement flagged here.

---

## 6. Methodological transparency

The guidebook is a secondary synthesis — it aggregates primary research, clinical evidence, codes, and practice guidance into a navigable reference. Its academic obligation is transparency about how evidence was selected, evaluated, weighted, and synthesized.

### 6.1 Transparency obligations

**Search and selection.** For each BPC entry and each specification: what sources were searched, what terms and databases were used, what date range was covered, what inclusion/exclusion criteria were applied. EvidenceSource entities carry this provenance.

**Evidence assessment.** For each specification's evidence marker (●/○) and tier assignment: what assessment criteria were applied, by whom (currently: solo author), with what result. The 7-tier hierarchy defines tiers; the assessment process for assigning sources to tiers must be documented per-specification, not just defined globally.

**Synthesis methodology.** How multiple sources were combined into a single specification or range. When sources disagreed, how disagreement was resolved. When evidence was absent, what inference method was used. The synthesis method indicator (direct / inferred / consensus) captures the derivation type; the inference basis captures the reasoning for each ○-marked specification.

**Independence and authorship.** Solo authorship with no external funding, no commercial interest, no institutional affiliation. All CRediT roles held by one person. Validation role unfilled by an independent party pre-launch. Disclosed.

**Gaps.** For each population, topic area, and jurisdiction: what is covered, what is not, and why. Gap entities carry this internally; the armature surfaces gaps to users via ○ markers, THIN-BASE disclosures, and population-level coverage statements.

### 6.2 Surfacing through the armature

The specification matrix is the user-facing output. Transparency metadata surfaces in two tiers:

**Specification matrix (visible):** tier, evidence marker, specification value/range, jurisdiction scope, conflict flag.

**Drill-down (available on request):** synthesis method indicator, inference basis, evidence provenance summary, assessment basis, BPC linkage, version and last-review date, authorship and validation provenance.

This two-tier surfacing respects the user's attention while making full provenance accessible. No specification is presented without its evidence marker. No ○-marked specification is presented without inference basis being available on drill-down.

### 6.3 Implications for A3 entity model

Extended metadata on existing entities:

- **EvidenceSource:** search strategy metadata, inclusion criteria, date range, database list
- **BPCMetadata:** synthesis method indicator, date of last review, quality-assessment summary
- **Specification:** synthesis method indicator, inference basis (where applicable), version history, jurisdiction scope array, last-review date
- **Gap:** user-facing surfacing flag, population-level gap aggregation

These are metadata extensions to existing entity types, not new entities.

---

## 7. Reconciliation with project framework

### 7.1 Core Doctrine

**"Disability populations are not uniform."** The two-layer architecture respects this: population categories organize the research base, functional axes capture individual variation within populations.

**"The guidebook is a starting framework for professional judgment, not a substitute for it."** The armature surfaces specifications and evidence; Mode S handoff flags where individual assessment is required. The tool does not replace OT assessment, designer judgment, or co-design.

**"The purpose of this guidebook is to get people to ask the right questions."** The armature surfaces the questions (via Mode S handoff flags, conflict notes, and gap disclosures), not just the answers. Each Tier 2 flag names the functional parameter that drives the assessment and the range within which resolution occurs.

**"The guidebook is an advocacy project, not an authority."** Specification language throughout is tier-appropriate: "Tier 1 evidence supports..." not "the specification is..." The armature presents evidence and surfaces questions — it does not prescribe.

### 7.2 Four-framework integration

- **ICF** maps to **functional axes**: axes are ICF-derived aggregations reframed for navigational utility in a design reference. The social-model tension is acknowledged: axes describe person-environment interactions but remain partially impairment-focused in vocabulary. This is a pragmatic limitation of using ICF-derived categories for a social-model-oriented project. Named, not pretended to be resolved.
- **PEO/PEOP** maps to the **query structure**: person (Layer 1 + Layer 2) × environment (scope: spatial) × occupation (scope: topic/categorical).
- **Capability Approach** intersects at the level of what specifications enable. The armature delivers specifications, not capability assessments. The distance between "transfer space ≥ 1500mm" and "this person can independently use the bathroom" is the distance between specification and capability. The armature does not bridge this gap. A12 to evaluate whether capability-level framing is achievable or whether it is an honest limitation of a specification-focused reference.
- **Kawa** intersects at the cultural layer: spatial models and design paradigms carry cultural assumptions. PAS 6463 sensory-room private retreat model is culturally specific. Specification language should not claim universality where cultural context governs applicability. Mechanism deferred to A12.

### 7.3 Design hierarchy and CRPD mapping

Design hierarchy is what the armature returns:
- **Universal Mode** (UD/Code Compliance) → CRPD Art 9 universal accessibility floor
- **Tier 1** (Population-Informed Inclusive Design) → CRPD Art 9 group-level accessibility
- **Tier 2** (Individual Assessment) → CRPD Art 5 reasonable accommodation

At Tier 2, the armature surfaces: the functional parameter driving assessment, the resolution range, and the OT appointment threshold per Part 9 §9.10. Conflict resolution at Tier 2 is the domain of the OT and the individual through co-design.

Evidence hierarchy is separate (7 tiers). Each specification carries both design tier and evidence marker. They are not collapsed.

In the plain-language role variant, ○-marked specifications are accompanied by: "This recommendation is based on clinical reasoning rather than direct research evidence."

### 7.4 Co-occurring disability and §3.8 Step 0

Project terminology: "co-occurring disability" (intra-individual), per CO-0003 terminology rule.

Compound functioning is supra-additive: per project-standards compound functioning rule, MWI ~16% additional disability per additional condition; Clarke 4.52x environment-impairment interaction. Pairwise resolution is insufficient; §3.8 Step 0 protocol applies.

When the person profile has multiple non-baseline axes, the system applies §3.8 Step 0 check. If non-additive interaction is identified, the system surfaces it explicitly and routes to Tier 2 with documented interaction mechanism. The armature does not "average" or "combine" specifications across axes silently. UI surfacing mechanism TBD at A12 / website build.

### 7.5 Variable conflation watch

Per project-standards: three apparent compound conflicts (CORRIDOR-W, COLOUR-CONT, PREDICT) dissolved when variable conflation was checked — opposing needs operated on different physical variables. The armature includes variable conflation check before surfacing apparent specification conflicts. Step 0 in §3.8 decision tree: verify that opposing needs operate on the same physical variable. Algorithm specification at A12.

### 7.6 "Adjustable is not universal conflict resolution"

Per project-standards. Every specification using "adjustable," "individual control," or "user-operated" must include a population operability note identifying: (1) populations who can self-adjust, (2) populations requiring carer/staff operation, (3) default setting when no individual present with harm-asymmetry rationale.

### 7.7 A3 entity model relationship

A3 signed off with 6 entity types: Specification, EvidenceSource, BPCMetadata, Connection, Slug, Gap. Cross-cutting axes scaffolded as Specification attributes.

The two-layer architecture implies a 7th entity type: **PopulationCategory**. This is a content-bearing entity with: category name (multilingual), category type (diagnosis / identity / situation), characteristic axis profile (where mapping confidence supports it), mapping confidence classification with source documentation, population-specific content (research synthesis, design considerations, code references), sub-classification scaffolds (where applicable), THIN-BASE flag, related categories, and validation provenance.

Whether PopulationCategory is a new entity type or an extension of existing BPCMetadata is an A3 decision. The content requirements exceed what BPCMetadata currently carries — A3 amendment is likely needed.

Whether Specification entities gain axis-level attributes (enabling direct axis-to-specification queries) or whether axes resolve to population codes before querying the entity model is an A7 decision with A3 implications.

---

## 8. Open questions — by phase

### A3 (Conceptual model)
1. Output schema — what does the armature return? Value, range, KFA spec entity, BPC entry, composed view?
2. PopulationCategory entity type — new entity or BPCMetadata extension?
3. Axis-level attributes on Specification entities — direct query or population-code resolution?
4. Reverse-mapping algorithm (axis-only entry → population-code-organized BPC retrieval)
5. Entity metadata extensions for methodological transparency (§6.3)

### A7 (Population taxonomy)
6. Naming — "armature" / "person-profile" / other
7. Final axis set with ICF cross-mapping and interaction-framing evaluation
8. Cognitive processing axis granularity (single axis vs sub-axes)
9. Deaf cultural/linguistic identity — axis, population category, or both?
10. Population code ↔ population category coexistence model
11. Diagnosis taxonomy source(s) — ICD-11 / DSM-5 / SNOMED CT / plain-language / mixed
12. Mapping confidence classification and documentation for each population
13. Validation criteria and method for population-to-axis mappings (constrained by solo authorship; minimum: alignment with published clinical literature and validated sub-classification scaffolds)
14. Clinical sub-classification scaffold fitness assessment (GMFCS, MACS, EDSS — validated for clinical use; fitness for navigational use in a design reference requires documented evaluation)
15. Supplementary Volume (body size) intersection mechanism
16. Respiratory/oxygen dependency axis evaluation
17. IntD axis mapping and THIN-BASE handling
18. Easy Read — axis value, role-layer content flag, or both?
19. Intersectional identity (gender per CRPD Art 6, age per Art 7) — separate dimension, axis extension, or scope modifier?

### A8 (Jurisdiction)
20. Jurisdictional scope dimension implementation — how jurisdiction data maps to specifications
21. Spatial scope coverage against CRPD Art 30 (cultural/recreational/sport venues), Art 24 (education), Art 27 (work)

### A11 (Evidence model)
22. Evidence assessment process documentation — per-specification or per-BPC-entry?
23. Synthesis method indicator implementation in the evidence hierarchy
24. Evidence handling for population-level content (distinct from specification-level evidence grading)

### A12 (Decision protocol)
25. Role-based delivery mechanism — filter vs content variant vs both
26. Carer role specification — distinct role, not proxy
27. Variable conflation check algorithm
28. §3.8 Step 0 UI surfacing
29. Cultural variation accommodation (Kawa framework)
30. Capability Approach integration depth — specification-only or capability-level framing?
31. Plain-language register specification

### Website build (post-Stage A)
32. Tool accessibility — WCAG 2.2 AA minimum; screen reader, switch input, keyboard-only, voice input compatibility; tested by disabled people across served populations; accessibility statement published
33. Population entry usability — search, synonyms, grouped presentation
34. Shareable query URLs
35. Export formats (PDF, plain text, accessible HTML)
36. Evidence marker accessible equivalents (text alternatives for ●/○)
37. Mobile-responsive design

---

## 9. Authority and validation

### 9.1 Pre-launch state

The project is a solo-author synthesis. No DPO partnerships, no Co-1 collaborator panels, no recruitment infrastructure exist. All architectural decisions, population categorizations, axis definitions, mapping confidence assignments, and content are authored by one person.

This is a structural limitation. Under CRPD Art 4.3, provisions affecting disabled people require close consultation with disabled people through their representative organizations. The project does not yet meet this standard.

Pre-launch validation basis: alignment with published clinical literature, validated clinical sub-classification scaffolds, established code frameworks, and published DPO position papers. This is the available validation — the Co-1 evidence commitment via the published corpus.

### 9.2 What this means for users

Every specification, population category, axis mapping, and content element in the guidebook should be understood as: authored by a solo researcher; validated against published sources; not yet validated through direct consultation with the populations described.

This disclosure is structural, not a caveat. It appears in the tool's methodology statement, not buried in documentation.

### 9.3 Post-launch commitment

The project commits to seeking PWLE/DPO consultation as operational capacity develops. Consultation is framed as an opportunity for structural revision, not validation of existing decisions. Elements most likely to require revision through consultation: population category selection and naming, axis naming and framing, mapping confidence levels, content framing for the disabled-person tool-user role, and the carer role definition.

This commitment is documented in the architecture because the architecture is the categorization. The categorization is what requires consultation.

---

## 10. The tool's own accessibility

A design reference for inclusive built environments should itself be accessible. Commitments:

- WCAG 2.2 AA minimum, with AAA where achievable
- Screen reader compatibility — full functionality, not degraded
- Switch input compatibility
- Keyboard-only navigation — full functionality
- No time limits on form completion
- Plain-language register available independent of role selection
- Evidence markers with text equivalents (not symbol-only)
- Axis-only entry operable without diagnosis literacy; population entry operable without axis-language literacy
- Anonymous use without account creation or data submission
- Tested by disabled people across served populations pre-launch
- Accessibility statement published with conformance level, known issues, and alternative-format request mechanism

These are preconditions for the project's coherence, not aspirations.

---

## 11. Sonnet / Opus boundary

This document is Sonnet-drafted. Per project rule: "Sonnet never determines best practice."

Structural architecture (Sections 3, 4, 6, 7) is structural specification — appropriate for Sonnet drafting.

The following require Opus synthesis at A7 / A12:
- Final axis set, count, granularity, ICF mapping, interaction framing
- Population category selection, naming, and content scoping
- Mapping confidence classification for each population
- Clinical sub-classification scaffold fitness assessment
- Evidence assessment process design
- Capability Approach integration decision
- Cultural variation accommodation design

This document is decision-quality only for the architectural concept and methodological transparency framework. Specific proposals carry reduced-confidence warnings until Opus synthesis occurs.

---

## 12. Recommended next action

A7 session, Opus selected, consuming this document plus `references/project-standards.md` plus existing population taxonomy plus A3 entity schemas. A7 produces:

- Naming decision
- Final axis set with ICF cross-mapping and interaction-framing evaluation
- Cognitive processing axis granularity decision
- Deaf cultural/linguistic identity handling
- Population code ↔ population category coexistence model
- Mapping confidence classification for each population (with source documentation)
- Clinical sub-classification scaffold fitness assessment
- Diagnosis taxonomy source decision
- Population-to-axis mappings (initial set, with validation provenance documented per §6)
- IntD mapping with THIN-BASE handling
- Supplementary Volume intersection mechanism
- Respiratory axis evaluation
- Easy Read classification
- Intersectional identity handling recommendation

A3 amendment likely follows A7 (PopulationCategory entity, axis-level Specification attributes, metadata extensions). Sequencing is a workplan-orchestrator decision.
