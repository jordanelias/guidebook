# Effort Level Guide

Per-skill effort overrides for the `/effort` parameter. `/effort` sets Claude's extended-thinking token budget — more reasoning steps before responding. It does not change the model. Model assignment is separate (per skill frontmatter).

**Default if a skill is not listed: 100.** User preference `<effort_levels>` qualitative default `max` applies when the user has not overridden.

---

## Decision rule

| Numerical | Use when |
|---|---|
| **150** | Opus-assigned skill; best-practice synthesis across competing sources/jurisdictions |
| **125** | Maximum Sonnet reasoning demand; multi-source judgment without Opus routing |
| **100** | Structured protocol with meaningful cross-referential judgment |
| **75** | Single-pass pattern recognition; tool-dependent or limited judgment |
| **50** | Mechanical; extraction, assembly, format correction, or I/O |

---

## Syntax

```
/effort 150  Synthesise best-practice guidance for tactile wayfinding across AU, UK, and EU jurisdictions.
/effort 125  Write item specification A-04 for acoustic zoning.
/effort 100  Run content-gap-analyzer on Section 4.3.
/effort 75   Check citations in the ramp section.
/effort 50   Fix linebreaks in vol2a after DOCX conversion.
```

---

## Skill table

### 150 — Opus-assigned; best-practice synthesis; cross-jurisdictional arbitration

| Skill | Rationale |
|---|---|
| multilingual-research | Cross-jurisdictional synthesis, 19 languages × 46 jurisdictions per skill protocol |
| evidence-auditor | Stratum determination; SelfCheck with divergent framing; contested-claim arbitration |
| functional-deficit-researcher | Opus-assigned for synthesis/NOVEL/REFINES classification; ICF → spatial requirement reasoning |
| cross-population-conflict-mapper | Opus-assigned for resolution synthesis and best-practice determination |
| adversarial-research | Confidence intervals, dissenter search, falsification conditions; Opus required for genuine adversarial framing |

### 125 — Heavy multi-source judgment; maximum Sonnet reasoning demand

| Skill | Rationale |
|---|---|
| item-specification-writer | Evidence and framing decisions; three-tier hierarchy; BPC synthesis gate check |
| sensory-coherence-checker | Cross-domain judgment across acoustic, visual, thermal, olfactory specs |
| literature-review-planner | PRISMA protocol construction; evidence hierarchy mapping |
| economics-researcher | Cost claim verification; cross-jurisdictional economic evidence |
| progressive-measurement | Iterative spec-value probing with strict termination criteria; heavy reasoning per step |
| economics-auditor | Cost-data verification across jurisdictions and contexts |
| functional-deficit-auditor | Audit pass over functional-deficit research output |

### 100 — Structured protocol with meaningful cross-referential judgment

| Skill | Rationale |
|---|---|
| content-gap-analyzer | Systematic coverage mapping; evidence type assessment across taxonomy |
| critique-report-writer | Editorial synthesis across upstream outputs |
| item-consolidation-analyzer | Redundancy/overload judgment; typology scope assignment |
| supplemental-integrator | Cross-volume taxonomy coordination; code relocation decisions |
| citation-miner | Forward/backward citation network traversal; tier classification |
| citation-verifier | Tool-dependent lookup and classify; tier-1 sources require judgment |
| gap-driven-mining | Gap-keyed search-matrix execution with outcome judgment; depth-1 constraint; rule #7/#8/#10 interlocks (DR-2026-05-26) |
| guidebook-auditor | Multi-mode audit; Modes B and D require Sonnet judgment |
| workplan-orchestrator | Multi-skill workflow coordination; risk escalation decisions |
| structure-auditor | Structural integrity judgment; orphan detection |
| audit-consolidator | Cross-audit synthesis; finding deduplication |
| item-audit-pipeline | Multi-stage audit pipeline coordination |
| cell-curator | Per-cell evidence curation in jurisdiction comparison tables |
| reasoning-doc-citations | Per-cell verification recording for synthesis claims (skill placeholder) |
| connection-discovery | Identify candidate cross-BPC connections |
| connection-auditor | Audit existing connections for validity and currency |
| cross-reference-resolver | Audit and classify broken refs; mechanical repair handoff |
| doctrine-recheck | A13 doctrine snapshot + cross-reference recheck |
| relational-integrity-checker | DB referential integrity validation |

### 75 — Single-pass pattern recognition; limited judgment; tool-dependent

| Skill | Rationale |
|---|---|
| practice-note-generator | Drafting from confirmed upstream evidence; limited new judgment |
| prose-style-checker | Register pattern recognition; single-pass rewrite |
| voice-style | Style conformance; single-pass framing check |
| jurisdiction-tracker | Web search + CURRENT/UPDATED/SUPERSEDED classification |
| session-consolidator | Pattern extraction from bounded session context; YAML write |
| question-author | Generate per-spec question framings from prepared evidence |
| bibliography-compiler | Deduplication and sequential numbering |
| version-diff | Semantic comparison with improvement/regression assessment |

### 50 — Mechanical; extraction, assembly, format correction, I/O

| Skill | Rationale |
|---|---|
| table-formatter | Format detection and conversion |
| find-and-replace | Mechanical string substitution |
| markdown-formatter | Heading hierarchy correction |
| github-io | Pure I/O; no judgment |
| github-filing | File move operations |
| toc-editor | Structural change recording; Change Order generation (frontmatter and codes only) |
| research-log-manager | Log read/write; BPC retrieval |

---

## Notes

- When a skill is not listed here, sessions invoking it default to 100. Numerical and qualitative levels coexist: qualitative levels (low/medium/high/max) apply when the user invokes `/effort low|medium|high|max`; numerical values document the skill's expected reasoning depth for routing decisions.
- **Deprecated skills** (`skills/deprecated/`) are not assigned an effort level. If a deprecated skill must be invoked, default to 50.
