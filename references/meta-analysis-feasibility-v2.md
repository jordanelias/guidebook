# Evidence Synthesis Feasibility Assessment v2
**Date:** 2026-04-09
**Scope:** Guidebook for Accessible Design V9.0 — entire project
**Basis:** 12 canonical BPC topic-directory files read in full; coverage-matrix.md; evidence-base-audit-2026-04-06.md; economics-gap-analysis-2026-04-09.md; FDR slug registry v2; connection register (170 entries); literature-review-planner skill
**Model:** Opus 4.6 (assessment and judgment); Sonnet 4.6 (data compilation)
**Supersedes:** meta-analysis-feasibility.md v1 (withdrawn — see self-review-v1.md for documented flaws)

---

## 0. What This Assessment Is and Is Not

**Is:** A decision tool for allocating finite research resources. It answers: where should the project invest in formal evidence synthesis, what type of synthesis is appropriate for each domain, and what should the project explicitly disclose as evidence gaps?

**Is not:** A systematic review, a meta-analysis, or a substitute for either. Executing the reviews identified here is a separate work programme.

**Relationship to existing project assets:**
- `evidence-base-audit-2026-04-06.md` (39K chars) provides the most detailed per-category evidence assessment in the project. This document builds on it, not replaces it.
- `coverage-matrix.md` provides the canonical population × topic slug count matrix. This document uses those counts directly rather than re-estimating.
- `economics-gap-analysis-2026-04-09.md` (17K chars) provides the Part 11 gap analysis. This document references it rather than duplicating.

---

## 1. Project-Level Assessment

### 1.1 The project's evidentiary character

The guidebook is not a clinical practice guideline and should not be assessed as one. It is a design specification framework that translates clinical and normative evidence into architectural specifications. Its evidence base is therefore inherently multi-type:

| Evidence function | What it does in the guidebook | Primary tiers |
|---|---|---|
| **Specifies** — provides dimensional values | "Grab bar height 650–900mm" | Tier 1 (biomechanics), Tier 4-6 (standards) |
| **Justifies** — explains why a specification matters | "Reverberation >0.6s prevents 100% speech perception" | Tier 1-3 (research) |
| **Legitimates** — establishes authority | "24 jurisdictions confirm..." | Tier 4-6 (standards), CRPD |
| **Centres** — ensures lived experience governs | "Co-1 validates/contradicts..." | Co-1 (lived experience) |
| **Resolves** — determines precedence in conflicts | "Harm asymmetry: neurological deterioration > pain" | Tier 1 (clinical), expert consensus |

A meta-analysis pools effect sizes to answer "what is the mean effect?" This is useful for **Specifies** and **Justifies** functions only, and only where quantitative outcomes exist. The majority of the project's evidence serves **Legitimates**, **Centres**, and **Resolves** functions, which require different synthesis methods.

### 1.2 Appropriate synthesis methods for this project

| Method | What it pools | When appropriate | Project applicability |
|---|---|---|---|
| **Quantitative meta-analysis** | Effect sizes from comparable studies | ≥3 studies with common outcome measure | ~8 specification domains (see §3) |
| **Qualitative meta-synthesis** (meta-ethnography, thematic synthesis) | Themes/concepts from qualitative studies | Co-1 lived experience research; DPO reports | HIGH — Co-1 is co-primary; ~50+ qualitative sources across populations |
| **Realist review** (Pawson & Tilley) | Context-mechanism-outcome configurations | "What works, for whom, in what circumstances" | HIGH — this IS the guidebook's central question |
| **Umbrella review** | Findings from existing systematic reviews | Where Tier 3 SRs already exist | MODERATE — ~15 existing SRs cited in BPC |
| **Standards comparison** (jurisdictional analysis) | Specification values across jurisdictions | Where Tier 4-6 standards diverge | ALREADY DONE — 24 jurisdictions mapped |
| **Scoping review** (Arksey & O'Malley) | Evidence landscape mapping | Where research volume/type is unknown | PARTIALLY DONE — BPC coverage matrix |
| **Evidence gap map** | Visual display of evidence/absence | Strategic research prioritisation | THIS DOCUMENT provides it |
| **Narrative synthesis** | Heterogeneous evidence integrated textually | Complex, multi-type evidence | DEFAULT — most guidebook sections |

### 1.3 Claim-to-evidence ratio

Based on BPC file inspection, the project has three tiers of evidential grounding:

**Well-grounded (Tier 1-3 evidence directly supports specification values):**
- Acoustics: RT60, STI thresholds — Murgia 2023, Iglehart 2020 (Tier 1 SR)
- Bathroom grab bars: height, angle, bilateral — Levine 2025, Kennedy 2015, Nakamura 2009 (Tier 1)
- LRV contrast: ≥30 threshold — Harper 2022, Brown 2023 (Tier 3); ≥65% Michelson for severe VI — Dain (Tier 3)
- Thermoregulation: 18-22°C — Griggs 2019, Hayashi 2022, Davis 2010, Burini 2018 (Tier 1-3)
- Reach range: 400-1100mm — AAATE 2016 (Tier 1 for door force); ADA/CSA (Tier 6 for height)
- Economics new-build premium: 0.94-3.92% — Ielegems & Vanrie 2024 (Tier 3)

**Normatively grounded (Tier 4-6 standards converge, but no primary research validates the specific values):**
- Most E-category items (corridor width, ramp gradient, turning circles)
- Most H-category items (control heights, operable force)
- Wayfinding signage dimensions (Tier 4-6 convergence across jurisdictions)
- Laundry specifications (ADA S611 sole source — Tier 6)

**Thinly grounded or ungrounded (specifications extrapolated from adjacent evidence or expert consensus):**
- All OFS built-environment specifications — "Tier 5 all provisions — extrapolated" (BPC status line)
- All PAIN built-environment specifications — BPC file is 320 chars, status MERGED
- All DBL built-environment specifications — "Zero Tier 1-2 evidence" (BPC consensus finding)
- IntD — proxied through DEM/NDV; THIN-BASE disclosure mandatory
- Sensory room dimensional specifications — "No Tier 1 RCTs exist" (BPC evidence note)
- All compound functioning specifications — zero primary built-environment studies
- All non-residential room types except education (classroom acoustics) and healthcare (POEs)
- Living room, garage, laundry, hallway — zero or near-zero dedicated research

### 1.4 Project-level verdict

The project is **methodologically rigorous in its evidence collection** (76 BPC slugs, 24 jurisdictions, 14 languages, 170 connections, Opus synthesis). It is **honest about its gaps** (THIN-BASE disclosures, ● / ○ markers, evidence-base-audit). 

The gap is not in evidence collection but in **formal evidence synthesis.** The BPC files contain expert narrative synthesis (Opus-quality). What is absent is:
1. Transparent, reproducible search protocols (PRISMA)
2. Quality appraisal of included studies (RoB, AMSTAR-2, NOS)
3. Quantitative pooling where feasible
4. Qualitative meta-synthesis of Co-1 evidence
5. Structured confidence-of-recommendation grading (GRADE or equivalent)

These five absences separate the guidebook from a formally publishable evidence-based guideline. They do not invalidate the guidebook's utility as a design framework, but they limit its citation authority.

---

## 2. Scoping Review: What Evidence Exists

### 2.1 Quantitative evidence (primary studies reporting numerical outcomes)

Grounded in BPC file inspection. Each row confirmed by reading the relevant BPC.

| Domain | Confirmed studies (from BPC) | Outcome measure(s) | Poolable? |
|---|---|---|---|
| **RT60/STI for hearing-impaired** | Murgia 2023 (SR), PLOS ONE 2025, ANSI/ASA S12.60 | Speech recognition %; RT60 s; STI | YES — common outcome |
| **Grab bar biomechanics** | Levine 2025, Kennedy 2015, Nakamura 2009 | COP deviation mm; FIM score; fall rate | YES — COP/biomechanics poolable |
| **LRV contrast detection** | Harper 2022, Brown 2023, Thompson 2017, Dain et al. | Fall rate; gait speed; detection % | PARTIAL — different outcome measures |
| **Thermoregulation thresholds** | Griggs 2019, Hayashi 2022, Burini 2018, Davis 2010, Flensner 2011, Chaseling 2022 | Tcore °C; sweat capacity %; symptom onset temp | YES — temperature threshold poolable by condition |
| **Door opening force** | AAATE 2016 | % wheelchair users succeeding at given force | YES but single study (N insufficient for MA) |
| **Construction cost premium** | Ielegems & Vanrie 2024, TERRAGON/DStGB 2017, Fuglerud 2015 | % cost premium by building type | MARGINAL — different cost bases |
| **Dementia wayfinding** | Marquardt 2011, De Hogeweyk POE | Wayfinding success %; incontinence events | PARTIAL — heterogeneous settings |
| **Sensory room outcomes** | Unwin 2022, 2023; Rashid 2025 | Self-regulation measures | NO — heterogeneous; emerging |

**Total confirmed primary study clusters suitable for quantitative meta-analysis: 3-4** (RT60/STI, grab bar biomechanics, thermoregulation thresholds, possibly LRV). All others have either too few studies, heterogeneous outcomes, or both.

### 2.2 Qualitative evidence (Co-1, DPO reports, lived experience)

The project's Co-1 evidence is extensive but uncatalogued as a synthesisable corpus. From BPC inspection:

| Population | Co-1 evidence character | Meta-synthesis feasible? |
|---|---|---|
| MOB | Housing adaptation experiences; wheelchair user testimonies; DPO surveys | YES — sufficient volume |
| VIS | Wayfinding experiences; LRV perceptual reports | PARTIAL |
| DEAF | DeafSpace design narratives; Gallaudet documentation | YES — rich corpus |
| DEM | Carer narratives; POE qualitative components | YES — substantial |
| NDV | Sensory environment experiences; Amaze/NAS surveys | YES — growing corpus |
| NDV/MH | De-escalation space experiences; trauma-informed design | PARTIAL |
| OFS | Very limited — clinical not experiential | NO |
| PAIN | Very limited | NO |
| DBL | Protactile movement documentation (Co-1 strong); built-env thin | PARTIAL — strong on communication, thin on built-env |

**Qualitative meta-synthesis is feasible for 4-5 populations** (MOB, DEAF, DEM, NDV, possibly VIS). This is a higher-value investment than quantitative MA for most guidebook purposes, because Co-1 is co-primary in the project's evidence hierarchy.

### 2.3 Normative evidence (Tier 4-6 standards)

Already comprehensively mapped: 24 jurisdictions, 14 languages. The existing jurisdictional comparison in BPC files IS a form of standards scoping review. What is absent is:
- Formal AGREE-II quality appraisal of standards as evidence sources
- Explicit tracking of which standards are evidence-based vs consensus-based vs historically inherited
- The LRV BPC demonstrates this gap perfectly: "30% LRV threshold derives from UK DDA guidance, not from peer-reviewed empirical evidence of sufficiency"

### 2.4 Existing systematic reviews cited (Tier 3)

From BPC files inspected, confirmed Tier 3 SRs include:
- Murgia 2023 (classroom acoustics — Tier 1 SR)
- MS housing rapid review 2025 (thermoregulation)
- Bertone 2021 (ASPECTSS, 5/21 studies — Tier 3)
- Multiple Cochrane/Campbell reviews cited in population BPCs (not individually inspected)

An **umbrella review** of existing SRs would establish: which specifications are already supported by published SRs, which SRs are current, and where SR gaps exist.

---

## 3. Prioritised Deep-Dives

### Selection criteria
1. Sufficient primary studies for formal synthesis (≥5 for narrative SR; ≥3 with common outcome for MA)
2. Direct specification impact (the synthesis would change or confirm a guidebook value)
3. Not already synthesised at SR level (no existing Tier 3 SR is adequate and current)

### Deep-Dive 1: Realist Review of Co-1 Evidence Across Populations
- **Method:** Realist synthesis (Pawson & Tilley)
- **Question:** What built-environment features work, for which disability populations, in which contexts, and through what mechanisms?
- **Why this matters most:** The project's central innovation is its population-specific, context-sensitive specification framework. A realist review would provide the theoretical spine that connects all specifications. No existing review does this.
- **Inputs:** All Co-1 sources across all population BPCs; case study evidence (Part 12); DPO publications
- **Estimated scope:** 50-100 sources; 3-6 months researcher time
- **Classification:** Beyond project scope — requires external research programme. But the framework could be DESIGNED within the project using the literature-review-planner skill.

### Deep-Dive 2: Quantitative MA — Acoustic Thresholds for Hearing-Impaired Populations
- **Method:** Quantitative meta-analysis (PRISMA; Cochrane methodology)
- **Question:** What RT60 and background noise thresholds produce clinically significant speech intelligibility improvement for hearing-impaired populations in built environments?
- **Why:** RT60 ≤0.3s is the project's most consequential acoustic specification. It is already supported by Murgia 2023 (Tier 1 SR). A focused MA could confirm the effect size and subgroup by device type.
- **Confirmed studies from BPC:** Murgia 2023, PLOS ONE 2025, Iglehart 2020, ANSI/ASA S12.60 evidence base
- **Feasibility:** HIGH — common outcome measure (speech recognition %), well-defined population, sufficient study count [UNVERIFIED — actual count requires database search]
- **Classification:** Executable within project using PubMed connector + literature-review-planner. 1-2 sessions.

### Deep-Dive 3: Quantitative MA — Grab Bar Biomechanics and Fall Prevention
- **Method:** Quantitative meta-analysis
- **Question:** What grab bar configurations (height, diameter, angle, bilateral vs unilateral) produce the greatest stability benefit during toilet transfer?
- **Why:** G-03 and G-04 are safety-critical specifications. The project cites Levine 2025, Kennedy 2015, and Nakamura 2009 as Tier 1 but has not pooled their effect sizes.
- **Confirmed studies from BPC:** Levine 2023/2025, Kennedy 2015, Nakamura 2009 (COP deviation data)
- **Feasibility:** MODERATE — common biomechanical measures exist but sample sizes may be small; need database search to confirm total study count [UNVERIFIED]
- **Classification:** Executable within project. 1-2 sessions.

### Deep-Dive 4: Qualitative Meta-Synthesis — NDV Sensory Environment Experiences
- **Method:** Thematic synthesis (Thomas & Harden)
- **Question:** What sensory environment features do neurodivergent people identify as enabling or disabling, and how do these relate to the project's A-16 and F-category specifications?
- **Why:** NDV/sensory has the richest qualitative evidence (9 BPC slugs in sensory-environment; Opus synthesis complete). The sensory-relief-space-design BPC explicitly notes "No Tier 1 RCTs exist." Qualitative synthesis would provide the strongest available evidence base for these specifications.
- **Confirmed sources:** Unwin 2022/2023, Rashid 2025, PAS 6463, Amaze/Architecture & Access 2025, Mostafa ASPECTSS studies
- **Feasibility:** HIGH — substantial Co-1 corpus; well-defined population
- **Classification:** Executable within project. 2-3 sessions.

### Deep-Dive 5: Thermoregulation Threshold Review — Multi-Condition
- **Method:** Scoping review with quantitative synthesis where poolable
- **Question:** What ambient temperature ranges produce symptom exacerbation for SCI, MS, and FMS populations, and what is the specification-level implication for the 18-22°C working target?
- **Why:** The thermoregulation BPC (12,195 chars) is the most detailed single-topic BPC in the project. The 18-22°C target is derived from clinical evidence synthesis but has not been formalised as a review. The FMS vs MS/SCI conflict is a key Part 5 resolution.
- **Confirmed studies:** 6+ primary studies with temperature data (Griggs, Hayashi, Burini, Davis, Flensner, Chaseling)
- **Feasibility:** HIGH — clinical studies with quantitative temperature outcomes
- **Classification:** Executable within project. 1-2 sessions.

---

## 4. Evidence Gap Map (Grounded)

### 4.1 Population × Topic — Using Canonical Coverage Matrix Data

Source: `coverage-matrix.md` (76 slugs, direct BPC file analysis). Values are **slug counts** (Opus-synthesised count in parentheses). Zero = no BPC coverage.

| Topic | MOB | VIS | DEAF | DEM | NDV | MH | OFS | PAIN | NEU | DBL |
|---|---|---|---|---|---|---|---|---|---|---|
| bathrooms-and-wet-areas | 2 (2) | 0 | 0 | 1 (1) | 1 (1) | 0 | 1 (1) | 1 (1) | 1 (1) | 0 |
| communication-and-alerts | 0 | 0 | 4 (4) | 1 (1) | 2 (2) | 0 | 0 | 0 | 0 | 0 |
| controls-and-hardware | 1 (1) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| entrances-and-circulation | 3 (3) | 3 (3) | 0 | 2 (2) | 1 (1) | 0 | 2 (2) | 1 (1) | 2 (2) | 0 |
| health-and-symptom-mgmt | 2 (2) | 0 | 0 | 4 (4) | 3 (3) | 1 (1) | 5 (5) | 3 (3) | 4 (4) | 0 |
| kitchens-and-workspaces | 1 (1) | 0 | 0 | 1 (1) | 0 | 0 | 1 (1) | 1 (1) | 1 (1) | 0 |
| room-types | 1 (1) | 0 | 0 | 0 | 0 | 0 | 1 (1) | 0 | 1 (1) | 0 |
| sensory-environment | 0 | 2 (2) | 3 (3) | 3 (3) | 9 (9) | 4 (4) | 3 (3) | 2 (2) | 5 (5) | 1 (1) |
| wayfinding-and-signage | 0 | 4 (4) | 2 (2) | 4 (4) | 2 (2) | 1 (1) | 1 (1) | 0 | 2 (2) | 1 (1) |

**Observations grounded in data:**

1. **NDV-sensory is the densest cell** (9 slugs, all Opus). This is the strongest candidate for qualitative meta-synthesis.
2. **OFS-health and NEU-sensory are surprisingly dense** (5 slugs each). But the OFS BPC itself notes "Tier 5 all provisions — extrapolated." Slug count ≠ evidence quality. OFS has high research VOLUME but low evidence TIER — the research is clinical, not built-environment.
3. **DBL, PAIN, MH have structural gaps.** DBL has 2 slugs total (sensory + wayfinding). PAIN's standalone BPC was merged (320 chars). MH has coverage only in sensory + wayfinding + health.
4. **Controls-and-hardware is the thinnest topic** (1 slug, MOB only). Despite reach-range having PROVISIONAL status (16 jurisdictions NOT-RUN), it serves as sole BPC for all H-category items.
5. **Room-types has 1 slug** (laundry only). All other room-type specifications are derived from topic-level BPCs, not room-level research.

### 4.2 Evidence TIER Map (grounded in BPC file inspection)

This replaces the fabricated ■/▓/░/· matrix from v1. Ratings are based ONLY on BPC files I have directly read. Unread cells are marked [NOT INSPECTED].

| BPC file read | Reported tier range | Opus synthesis? | Tier 1 present? | Co-1 present? | THIN-BASE? |
|---|---|---|---|---|---|
| accessible-bathroom-and-grab-bar | 1-6 | YES | YES (Levine, Kennedy, Nakamura) | YES (25/24 jurisdictions) | NO |
| acoustics-speech-intelligibility | 1-3 | YES | YES (Murgia 2023 SR) | Not reported | NO |
| luminance-contrast-lrv | 3-4 | YES | NO (Tier 3 lowest) | Not reported | YES (30% LRV has no empirical basis) |
| reach-range-and-controls | 1-6 | YES (PROVISIONAL) | YES (AAATE 2016 for door force) | 0/24 jurisdictions | YES (PROVISIONAL) |
| thermoregulation | 1-3 | YES | YES (6+ clinical studies) | Not reported | NO |
| cross-population-conflicts | 1-4 | YES | YES (embedded from pop BPCs) | Not reported | NO (for resolved conflicts) |
| deafblind-built-environment | 4-5 | YES | NO — zero Tier 1-2 | YES (Protactile) | YES |
| accessible-laundry-room | 4-5 | YES (PARTIAL) | NO | 0/4 jurisdictions | YES (PARTIAL — 4 juris only) |
| sensory-relief-space-design | 2-3-5 | YES | NO ("No Tier 1 RCTs exist") | YES (NAS, Amaze) | EMERGING |
| economics-cost-premium | 1-3 | YES | YES (Ielegems 2024) | N/A | NO |
| case-study-economics | 2-5 | NO (pending) | NO | N/A | YES (5 verified / 26 total) |
| OT-cpg-built-environment | Co-2 | YES | N/A (Co-2 inventory) | N/A | NO (4 confirmed OT bodies with built-env CPGs) |

### 4.3 Co-occurrence evidence (grounded)

v1 claimed "zero evidence for all pairings." This is wrong. The `cross-population-conflict-resolutions` BPC documents **9 resolved conflicts** with evidence from Tier 1-4. Additionally, 12 conflict domain matrices with Opus synthesis exist. The project's co-occurrence evidence is not in primary built-environment studies — it is in the structured resolution of clinically grounded conflicts.

| Evidence type | Count | Status |
|---|---|---|
| Resolved cross-population conflicts (BPC) | 9 | Opus synthesised |
| Conflict domain matrices | 12 + SYNTHESIS | Opus synthesised (2026-03-30) |
| Connection register entries (co-occurrence type) | ~20 of 170 [UNVERIFIED — estimated] | 80 consumed, 37 pending, 53 unwritten |
| FDR compound scenarios | 8 designed | ALL NOT-RUN |
| FDR occupation scenarios | 6 designed | ALL NOT-RUN |
| Primary built-environment studies on compound effects | 0 confirmed | TRUE ABSENCE |

**Corrected assessment:** The project has substantial SYNTHESIS evidence for co-occurrence (resolutions, matrices, connections) but zero PRIMARY evidence. The FDR compound scenarios are designed to generate structured clinical-reasoning-based specifications for co-occurring conditions. A formal systematic review of co-occurrence would confirm what the project already knows: the evidence is absent. The higher-value action is executing the FDR compound scenarios.

### 4.4 Economics evidence (grounded — per economics-gap-analysis)

The economics-gap-analysis (17K chars) provides a comprehensive assessment. Key findings from that document:

- 4 intervention categories missing from cost tables (kitchen, bedroom, emergency, controls)
- 5 VERIFIED financial entries out of 26 case studies
- Per-item cost estimates are largely [UNVERIFIED — estimated] from industry knowledge, not from published cost data
- Cost premium data is from 3 jurisdictions with published studies (BE, DE, NO)

### 4.5 Critical Evidence Absences (confirmed)

These are TRUE ABSENCES confirmed by BPC inspection, not inferred from file counts:

1. **Compound functioning in built environments** — zero primary studies (confirmed by FDR registry: all 8 compound scenarios NOT-RUN; no primary literature identified)
2. **DBL built-environment Tier 1-2** — "Zero Tier 1-2 evidence" (BPC consensus finding, direct quote from file)
3. **OFS built-environment Tier 1-2** — "Tier 5 all provisions — extrapolated" (BPC status line)
4. **PAIN built-environment** — BPC file merged into pain-ofs; no standalone evidence base
5. **30% LRV empirical validation** — "derives from UK DDA guidance, not from peer-reviewed empirical evidence" (BPC consensus finding)
6. **Sensory room RCTs** — "No Tier 1 RCTs exist for dedicated sensory room architectural design" (BPC evidence note)
7. **Non-residential room-specific evidence** — room-types has 1 slug (laundry); all other NR rooms derive from topic-level BPCs
8. **Collectivist-context sensory space model** — "PAS 6463 private retreat model does not transfer" (project standard); FDR-ENV-05 NOT-RUN
9. **OT CPG thermal gap** — "No OT CPG addresses thermal environment as a home modification domain" (project standard)
10. **Per-item construction cost data** — no cross-jurisdictional poolable data exists (economics-gap-analysis finding)

---

## 5. Decision Matrix: Where to Invest

### 5.1 Formal synthesis investments (ranked by value-per-effort)

| Rank | Action | Type | Effort | Value | Sessions | Executable? |
|---|---|---|---|---|---|---|
| 1 | Qualitative meta-synthesis: NDV sensory experiences | Thematic synthesis | Medium | HIGH — grounds A-16, F-01–F-04 in Co-1 | 2-3 | YES (within project) |
| 2 | Acoustic RT60/STI threshold MA | Quantitative MA | Medium | HIGH — confirms/refines A-01–A-14 | 1-2 | YES (PubMed + LRP) |
| 3 | Thermoregulation threshold review | Scoping + quantitative | Medium | HIGH — grounds TC-01, F-04, conflict resolution | 1-2 | YES (within project) |
| 4 | Grab bar biomechanics MA | Quantitative MA | Medium | MODERATE — confirms G-03/G-04 (already Tier 1) | 1-2 | YES (PubMed + LRP) |
| 5 | FDR compound scenarios (P1 set) | Clinical reasoning synthesis | High | HIGH — fills largest gap | 4-6 | YES (Opus FDR skill) |
| 6 | LRV contrast empirical review | Scoping review | Low | MODERATE — current spec may be insufficient | 1 | YES (within project) |
| 7 | Umbrella review of existing Tier 3 SRs | Umbrella review | Medium | MODERATE — validates evidence base | 2-3 | YES (within project) |
| 8 | Realist review: population-specific built-env | Realist synthesis | Very high | VERY HIGH — provides theoretical spine | 3-6 months | NO (external research) |
| 9 | Co-1 meta-synthesis: MOB/DEAF/DEM | Qualitative MA | High | HIGH | 4-6 | PARTIAL (within project for design; external for execution) |

### 5.2 Disclosure investments (no research required)

| Action | Effort | Impact |
|---|---|---|
| Add GRADE-equivalent confidence rating to all Part 4 specifications | High (125+ items) | HIGH — transforms guidebook from design framework to evidence-based guideline |
| Complete ● / ○ evidence marker pass on all specifications | Medium | HIGH — already designed, partially implemented |
| Add "Evidence density statement" to each Part opening | Low | MODERATE — per §4.2 tier map data |
| Flag all specifications with PROVISIONAL BPC status | Low | MODERATE — reach-range, laundry currently PROVISIONAL |
| Formal statement of evidence absence for OFS, PAIN, DBL | Low | HIGH — honesty principle; already informally disclosed |

### 5.3 Do NOT invest (diminishing returns)

| Action | Why not |
|---|---|
| Meta-analysis of cross-jurisdictional standards convergence | Already done in BPC synthesis; formalising it adds citation authority but no new knowledge |
| Systematic review of co-occurrence built-environment literature | The literature doesn't exist; the FDR compound scenarios are the correct investment |
| Per-item construction cost meta-analysis | Heterogeneous cost bases across jurisdictions make pooling meaningless; the economics-gap-analysis already identifies this |
| Formal SR for every population × topic cell | 110 cells × ~2 sessions each = ~220 sessions. The BPC coverage matrix already provides the scoping function |

---

## 6. Methodological Framework for Executing Reviews

Per `literature-review-planner` skill (§3):

**PRISMA-aligned protocol minimum:**
- Identification: databases + grey literature + forward/backward citation mining
- Screening: title/abstract criteria
- Eligibility: full-text criteria (study design, population, outcome, date)
- Data extraction: Author-Year · Study design · Population · N · Setting · Outcome · Jurisdiction · Evidence tier
- Quality appraisal: RCT → PEDro; Observational → NOS; SR → AMSTAR-2; Standards → AGREE-II

**Project-specific evidence hierarchy (§4):**
Co-1 = Tier 1 in authority. Both precede Tier 2 → Co-2 → Tier 3 → Tier 4 → Tier 5 → Tier 6. Tiers 5-6 are authority sources, not evidence of effect.

**Synthesis framework (§6):**
- ≥3 studies with common outcome → specification table with source comparison
- Heterogeneous → structured narrative with convergence/divergence framing
- Standards vs evidence divergence → explicit gap statement with interim specification

---

## 7. Honest Limitations of This Assessment

1. **I read 12 of 76 canonical BPC files.** The remaining 64 are characterised by file size and the coverage-matrix slug counts, not by direct inspection. Tier assessments for unread files are [NOT INSPECTED].
2. **Study counts in §3 deep-dives are from BPC citations, not from database searches.** The "confirmed studies" are what the project cites, not the total literature. Actual meta-analysis would require de novo search.
3. **The qualitative meta-synthesis feasibility assessment (§2.2) is based on BPC descriptions of Co-1, not on reading the primary Co-1 sources.** The assessment that "sufficient volume" exists is inferred, not confirmed.
4. **Connection register co-occurrence count (~20) is estimated.** I read the _index.md but did not count connection types. The actual distribution requires reading per-topic connection files.
5. **The "sessions" estimates in §5.1 assume Sonnet execution for most tasks and Opus for compound FDR.** Actual session counts depend on search yield and evidence complexity.

---

## 8. Confidence Calibration

| Claim | Confidence | Basis |
|---|---|---|
| Quantitative MA is feasible for RT60/STI | HIGH | Murgia 2023 is a published SR; BPC confirms common outcome measures |
| Quantitative MA is feasible for grab bars | MODERATE | 3 Tier 1 studies confirmed; need database search for total count |
| Qualitative meta-synthesis is the highest-value investment | HIGH | Co-1 is co-primary; NDV-sensory has 9 Opus-synthesised BPC slugs |
| Compound functioning literature is absent | HIGH | FDR registry confirms; BPC confirms; project standards confirm |
| PAIN/OFS/DBL have near-zero built-env evidence | HIGH | Direct BPC file inspection confirms |
| 30% LRV lacks empirical basis | HIGH | BPC file explicitly documents this |
| Realist review would be highest value but is external scope | MODERATE | Judgment call; no BPC data directly supports this claim |
| Total meta-analysable domains = 3-4 | MODERATE | Based on BPC citations; database search may reveal more |
