# Effort Level Guide
**Last updated:** 2026-04-07 00:50
**Active version:** V9.0 2026-03-20

---

## How Effort Works

The `/effort` parameter sets Claude's extended thinking token budget — more reasoning steps before responding. It does not change the model. Model assignment is separate (Project Instructions §Architecture).

**Valid levels:** 150 · 125 · 100 · 75 · 50

---

## Decision Rule

> **150** — Opus-assigned skill, or best-practice synthesis across competing sources/jurisdictions.
> **125** — Maximum Sonnet reasoning demand; multi-source judgment without Opus routing.
> **100** — Structured protocol with meaningful cross-referential judgment.
> **75** — Single-pass pattern recognition; tool-dependent or limited judgment.
> **50** — Mechanical; extraction, assembly, format correction, or I/O.

When in doubt: match to the skill table below. If the skill is not listed, default to 100.

---

## Syntax

Prepend the flag to your instruction:

```
/effort 150  Synthesise best-practice guidance for tactile wayfinding across AU, UK, and EU jurisdictions.

/effort 125  Write item specification A-04 for acoustic zoning — NEU and NDV populations.

/effort 100  Run content-gap-analyzer on Section 4.3.

/effort 75   Check citations in the ramp section.

/effort 50   Fix linebreaks in vol2a after DOCX conversion.
```

---

## Skill Table

### 150 — Opus-assigned; best-practice synthesis; cross-jurisdictional arbitration

| Skill | Rationale |
|---|---|
| multilingual-research | Cross-jurisdictional synthesis, 14 languages, κ ≈ 0.30 divergence expected |
| evidence-auditor | Stratum determination; SelfCheck with divergent framing; contested-claim arbitration |
| connection-scout | Opus-assigned; cross-population synthesis across assembled evidence base |
| functional-deficit-researcher | Opus-assigned for synthesis/NOVEL/REFINES classification; ICF → spatial requirement reasoning |
| cross-population-conflict-mapper | Opus-assigned for resolution synthesis and best-practice determination |

### 125 — Heavy multi-source judgment; maximum Sonnet reasoning demand

| Skill | Rationale |
|---|---|
| item-specification-writer | Evidence and framing decisions; three-tier hierarchy; BPC Opus-synthesis check gate |
| sensory-coherence-checker | Cross-domain judgment across acoustic, visual, thermal, and olfactory specs |
| framing-checker | Two-pass CRPD-grounded protocol; flag categorisation on contested cases |
| literature-review-planner | PRISMA protocol construction; evidence hierarchy mapping |
| economics-researcher | Cost claim verification; cross-jurisdictional economic evidence |
| valoria-mechanic-audit | Complex interacting system cross-referencing; formula validation |

### 100 — Structured protocol with meaningful cross-referential judgment

| Skill | Rationale |
|---|---|
| content-gap-analyzer | Systematic coverage mapping; evidence type assessment across taxonomy |
| critique-report-writer | Editorial synthesis across upstream outputs |
| version-diff | Semantic comparison with improvement/regression assessment |
| evidence-marker | Evidence classification (●/○); tier assignment judgment |
| item-consolidation-analyzer | Redundancy/overload judgment; typology scope assignment |
| supplemental-integrator | Cross-volume taxonomy coordination; code relocation decisions |
| citation-miner | Forward/backward citation network traversal; tier classification |
| guidebook-auditor | Multi-mode audit; Modes B and D require Sonnet judgment |
| workplan-orchestrator | Multi-skill workflow coordination; risk escalation decisions |
| structure-auditor | Structural integrity judgment; orphan detection |
| valoria-canon-guard | Constraint checking against P-01–P-14 |
| valoria-simulator | Multi-step mechanical state tracking; probability analysis |
| valoria-orchestrator | Workflow routing; editorial gate enforcement |

### 75 — Single-pass pattern recognition; limited judgment; tool-dependent

| Skill | Rationale |
|---|---|
| practice-note-generator | Drafting from confirmed upstream evidence; limited new judgment |
| prose-style-checker | Register pattern recognition; single-pass rewrite |
| voice-style | Style conformance; single-pass framing check |
| jurisdiction-tracker | Web search + CURRENT/UPDATED/SUPERSEDED classification |
| citation-verifier | Tool-dependent lookup and classify; bottleneck is retrieval not reasoning |
| volii-validator | Code matching; binary status determination |
| session-consolidator | Pattern extraction from bounded session context; YAML write |

### Mechanical; does not require effort; extraction, assembly, format correction, I/O

| Skill | Rationale |
|---|---|
| haiku-chunker | Structural extraction only; no content judgment |
| valoria-chunker | Structural extraction only; no content judgment |
| table-formatter | Format detection and conversion |
| find-and-replace | Mechanical string substitution |
| fix-linebreaks | Paragraph join; no judgment |
| markdown-formatter | Heading hierarchy correction; mechanical |
| bulk-renumber | Numbering map application; mechanical |
| bibliography-compiler | Deduplication and sequential numbering |
| chunk-assembler | File assembly; no content judgment |
| file-splitter | Structural decomposition; no content judgment |
| vol2-item-formatter | Format validation and rendering |
| cross-reference-resolver | Audit and classify broken refs; mechanical repair handoff |
| github-io | Pure I/O; no judgment |
| github-filing | File move operations |
| toc-editor | Structural change recording; Change Order generation |
| research-log-manager | Log read/write; BPC retrieval |
