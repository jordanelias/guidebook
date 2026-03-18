---
name: literature-review-planner
description: >
  Converts research outputs and gap registers into a structured literature review plan
  for the Accessible Built Environments Guidebook. Produces: systematic search strategy,
  PRISMA-aligned protocol, evidence hierarchy mapping, synthesis framework, and prioritised
  research agenda. Use when: planning a formal literature review, structuring evidence for
  publication, preparing a research brief for an academic partner, or building a systematic
  review protocol from existing research session outputs.
  Trigger on: "literature review plan", "research plan", "systematic review protocol",
  "search strategy", "PRISMA", "evidence synthesis", "research agenda", "next research phase".
---

**Model:** Sonnet 4.6 with web search (for database and search term verification)
**Framing:** Social model throughout. CRPD Article 9 as governing framework.
**Output audience:** Design professionals AND academic reviewers (dual audience — must satisfy both)
**Research log:** Call `research-log-manager CHECK` before any search run. Call `research-log-manager LOG` after. Skipping either is an error.

---

## Plan Structure

Every literature review plan produced by this skill contains the following sections:

### Section 1 — Review Scope and Questions
Define:
- Primary research question (one sentence, PICO-adjacent format for built environment research)
- Secondary questions (maximum 5)
- Population codes in scope (MOB/AMB · MOB/UPL · VIS/vis · VIS/DEAF · NEU · NEU/PCS · DEM · NDV · NDV/AUT · NDV/ADHD · NDV/SENS · NDV/MH · PAIN · OFS · OFS/ME · OFS/POTS · OFS/MCAS · DBL · CHD · LPA · EXH; large body size provisions: Supplementary Volume — use → `references/project-standards.md` as authoritative code list)
- Building typologies in scope
- Date range rationale
- Exclusion criteria (explicit)

### Section 2 — Search Strategy
For each topic cluster:

**2a. Database list:** use the database + language matrix defined in `multilingual-research` (PubMed · Consensus · Scholar Gateway for English; jurisdiction-specific sources per language). Do not duplicate the list here.

**2b. Search term clusters** (per topic — Boolean strings):
Format:
```
Cluster name: [term A OR term B OR term C] AND [term D OR term E] AND [exclusion NOT term F]
```

**2c. Grey literature sources** (per topic):
List organisations, reports, and practice sources relevant to topic.

**2d. Multilingual search terms** (flag languages requiring specialist search):
Format: `Topic | English terms | German | French | Norwegian | Japanese | Portuguese | Dutch`

### Section 3 — PRISMA-aligned Protocol
- Identification: databases + grey literature + forward/backward citation
- Screening: title/abstract criteria
- Eligibility: full-text criteria (study design, population, outcome, date)
- Inclusion: final inclusion criteria with justification
- Data extraction form fields (minimum): Author-Year · Study design · Population · N · Setting · Outcome · Jurisdiction · Evidence tier
- Evidence quality appraisal tool (suggest per study design): RCT → PEDro; Observational → NOS; Systematic review → AMSTAR-2; Standards/guidelines → AGREE-II

### Section 4 — Evidence Hierarchy (project-specific)
Adapted from the guidebook's evidence tier system:
| Tier | Type | Weight |
|---|---|---|
| 1 | Systematic review / meta-analysis (peer-reviewed) | Highest |
| 2 | RCT or controlled quasi-experimental study | High |
| 3 | Cohort / longitudinal study | Moderate-high |
| 4 | Cross-sectional study / survey | Moderate |
| 5 | Case study / qualitative study | Moderate-low |
| 6 | Expert consensus / Delphi | Low-moderate |
| 7 | International standard (ISO, EN, CRPD) | Authority |
| 8 | National standard / code | Authority (jurisdiction-specific) |
| 9 | Practice guideline / grey literature | Supplementary |
| 10 | Single opinion / anecdote | Flag only |

**Rule:** Tiers 7–10 are cited as authority sources, not as evidence of effect. Tiers 1–6 provide empirical evidence of effect. Both types are needed; they must not be conflated.

### Section 5 — Priority Research Agenda
Organise all identified gaps into a priority matrix:

**Priority 1 — Blocking (must resolve before Volume can be finalised):**
Gaps where a Volume 2 item has no evidence above Tier 8 for its primary claim.

**Priority 2 — Strengthening (should resolve before publication):**
Gaps where evidence exists but is dated (>10 years), from a single jurisdiction, or a single study type.

**Priority 3 — Horizon (desirable for next edition):**
Emerging areas where evidence is beginning to accumulate but not yet sufficient for firm specification.

Format:
```
GAP-XXX | V2 Item(s) affected | Population code | Gap description | Priority | Recommended search | Languages | Estimated search volume
```

### Section 6 — Synthesis Framework
How findings will be synthesised into the guidebook:

**Quantitative synthesis:** Where ≥3 studies report a common outcome (e.g. reverberation time, contrast ratio, turning radius) — produce a specification table with source-by-source data comparison and recommended design value.

**Narrative synthesis:** Where studies are too heterogeneous for quantitative pooling — produce a structured narrative with explicit framing of convergence and divergence.

**Standards gap analysis:** Where empirical evidence and current standards diverge (e.g. luminance contrast 30% standard vs Manandhar et al. 2022 finding of inadequacy) — produce an explicit gap statement flagging the discrepancy and recommended interim specification.

**Cross-jurisdictional comparison:** Where standards differ significantly across jurisdictions (e.g. turning radius: ISO 1524 mm vs ANSI 1702 mm) — produce a comparison table and recommend which figure to adopt and why.

### Section 7 — Timeline and Resource Estimate
| Phase | Task | Estimated searches | Skill(s) required | Priority |
|---|---|---|---|---|
| Phase 1 | Priority 1 gaps — blocking | X searches | multilingual-research, economics-researcher | Immediate |
| Phase 2 | Priority 2 gaps — strengthening | X searches | multilingual-research | Next revision |
| Phase 3 | POE and longitudinal evidence | X searches | multilingual-research | Ongoing |
| Phase 4 | Emerging areas | X searches | multilingual-research | Next edition |

---

## Gap Classification Rules (for Section 5)
- Absent entirely: no source of any tier found → Priority 1
- Single source, no replication: one study, no cross-jurisdiction confirmation → Priority 2
- Outdated: all sources >10 years old → Priority 2 if foundational, Priority 3 if supplementary
- Subscription-blocked: source exists but not accessed → Priority 1 if critical data, Priority 2 if confirmatory
- Language gap: evidence exists but only in non-English and not yet retrieved → Priority 2
- POE gap: design recommendation without post-occupancy validation → Priority 3 (systematic)

---

## Token Rules
- One research plan per run (scope: up to 5 topic clusters per plan)
- Section 2 search strings: maximum 3 Boolean strings per cluster
- Priority matrix: maximum 30 gap entries per run
- Timeline estimates: ranges only (do not false-precision)
