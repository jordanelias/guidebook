---
name: literature-review-planner
description: >
  Converts research outputs and gap registers into a structured literature review plan for the
  Accessible Built Environments Guidebook. Produces: systematic search strategy, PRISMA-aligned
  protocol, evidence hierarchy mapping, synthesis framework, and prioritised research agenda.
  Use when: planning a formal literature review, structuring evidence for publication, preparing
  a research brief, or building a systematic review protocol from existing session outputs.
  Trigger on: "literature review plan", "research plan", "systematic review protocol",
  "search strategy", "PRISMA", "evidence synthesis", "research agenda", "next research phase".
---

**Model:** Sonnet 4.6 + web  
**Framing:** Social model throughout. CRPD Article 9 as governing framework.  
**Output audience:** Design professionals AND academic reviewers.  
**Research log:** `research-log-manager CHECK` before any search run. `research-log-manager LOG` after. Skipping either is an error.

**PICO sequence (mandatory):** Begin with population need and functional outcome (optimal first) — not standard values. Standards appear at Step 2 as minimum baseline only.

---

## Plan Structure

### Section 1 — Scope and Questions
- Primary research question (one sentence, PICO-adjacent)
- Secondary questions (≤5)
- Population codes in scope (canonical list → `references/project-standards.md`)
- Building typologies in scope
- Date range rationale
- Exclusion criteria (explicit)

### Section 2 — Search Strategy

**2a. Databases:** use the database + language matrix defined in `multilingual-research`. Do not duplicate here.

**2b. Search term clusters** (per topic — Boolean strings):
```
Cluster name: [term A OR term B] AND [term C OR term D] NOT [term E]
```

**2c. Grey literature** (per topic): organisations, reports, practice sources.

**2d. Multilingual terms** (flag languages requiring specialist search):
`Topic | English | DE | FR | NO | JA | PT | NL`

### Section 3 — PRISMA-Aligned Protocol
- Identification: databases + grey literature + forward/backward citation mining
- Screening: title/abstract criteria
- Eligibility: full-text criteria (study design, population, outcome, date)
- Inclusion: final criteria with justification
- Data extraction fields (minimum): Author-Year · Study design · Population · N · Setting · Outcome · Jurisdiction · Evidence tier
- Quality appraisal tools: RCT → PEDro; Observational → NOS; Systematic review → AMSTAR-2; Standards → AGREE-II

### Section 4 — Evidence Hierarchy (project-specific)
Per guidebook §1.5. Co-1 (lived experience) = Tier 1 (OT clinical) in authority. Both precede Tier 2 (NGO/advocacy) → Co-2 (OT CPGs — CAOT, AOTA, RCOT, COTEC, WFOT, national equivalents) → Tier 3 (systematic reviews / meta-analyses) → Tier 4 (international standards with evidence basis) → Tier 5 (national beyond-code frameworks) → Tier 6 (statutory codes).

Tiers 5–6 are authority sources, not evidence of effect. Tiers 1–4, Co-1, and Co-2 provide empirical evidence of effect. Both types are needed; they must not be conflated.

### Section 5 — Priority Research Agenda

**P1 — Blocking:** Volume item has no evidence above Tier 6 for its primary claim.  
**P2 — Strengthening:** Evidence exists but is dated (>10 years), single-jurisdiction, or single study type.  
**P3 — Horizon:** Emerging evidence; insufficient for firm specification.

Format:
```
GAP-XXX | V2 Item(s) | Population | Gap description | Priority | Search slug | Languages | Est. search volume
```

### Section 6 — Synthesis Framework

**Quantitative:** ≥3 studies report common outcome → specification table with source comparison and recommended design value.  
**Narrative:** Heterogeneous studies → structured narrative with explicit convergence/divergence framing.  
**Standards gap:** Empirical evidence and current standards diverge → explicit gap statement with interim specification.  
**Cross-jurisdictional:** Standards differ across jurisdictions → comparison table with recommended adoption rationale.

**Best-practice synthesis:** For each finding cluster, identify the most amenable, inclusive, forgiving, caring, accommodating, dignified, specific, and targeted provision the evidence supports. This is the synthesis output — not a catalogue.

### Section 7 — Timeline and Resource Estimate
| Phase | Task | Est. searches | Skill(s) | Priority |
|---|---|---|---|---|
| 1 | P1 gaps | X | multilingual-research, economics-researcher | Immediate |
| 2 | P2 gaps | X | multilingual-research | Next revision |
| 3 | POE and longitudinal | X | multilingual-research | Ongoing |
| 4 | Emerging areas | X | multilingual-research | Next edition |

---

## Gap Classification Rules
- Absent entirely → P1
- Single source, no replication → P2
- All sources >10 years old → P2 (foundational) or P3 (supplementary)
- Subscription-blocked → P1 (critical) or P2 (confirmatory)
- Language gap: evidence exists in non-English, not yet retrieved → P2
- POE gap: no post-occupancy validation → P3

---

## Token Rules
- ≤5 topic clusters per plan
- ≤3 Boolean strings per cluster
- ≤30 gap entries per run
- Timeline: ranges only
