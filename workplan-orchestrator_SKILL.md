---
name: workplan-orchestrator
description: >
  Orchestrate multi-skill workflows for the Accessible Built Environments Guidebook project.
  ALWAYS use this skill at the start of any complex guidebook task, to decompose it into the
  correct skill sequence, manage inter-skill handoffs, track the gap register, and ensure outputs
  feed forward correctly. Trigger on: "start a review", "audit the guidebook", "begin work on",
  "what's the plan", "how should we approach", "run a full review", "where did we leave off",
  any multi-step guidebook task, or resuming work after a session gap.
---

**Model:** Sonnet 4.6
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API

---

## Session Start Protocol (mandatory — every new conversation)

### 1 — Load session state
GET `session_log.md`. Find most recent `session_close` YAML block.
- **Found:** Report last session datetime, last skill run, next action, open P1 gap count, blockers. Confirm with user before resuming. Do not auto-resume.
- **Empty/not found:** "No prior session. Starting fresh."

### 2 — Load gap register
GET `gap_register.md`. Extract OPEN P1 items. Surface to user if any; otherwise proceed silently.

### 3 — Load project standards
GET `references/project-standards.md`. Load rules into active context.

### 4 — Confirm PAT
If PAT not yet provided: prompt user. Do not proceed without it.

**Skip condition:** "fast-track" or "go" skips user confirmation at Task Intake only. Protocol still runs.

---

## Task Intake
New task: identify scope + goal → select workflow → confirm in ≤3 lines → execute.
Resumed task: confirm next action from YAML → execute from that stage.

---

## Workflows

| Workflow | Skill sequence |
|---|---|
| **Full Section Review** | haiku-chunker → [structure-auditor · markdown-formatter · guidebook-auditor A+B+C · content-gap-analyzer · framing-checker · evidence-auditor] → [research-log-manager CHECK · multilingual-research · citation-verifier · research-log-manager LOG] → [guidebook-auditor C · volii-validator · cross-reference-resolver] → prose-style-checker → critique-report-writer |
| **Item Specification** | item-consolidation-analyzer → item-specification-writer → [framing-checker · evidence-auditor] → prose-style-checker → volii-validator |
| **Structural Change** | structure-auditor → markdown-formatter → cross-reference-resolver → find-and-replace → guidebook-auditor A |
| **Bulk Text Change** | find-and-replace (all six stages — classification before execution) |
| **Citation Audit** | citation-verifier → critique-report-writer §7 |
| **Evidence Gap** | content-gap-analyzer → research-log-manager CHECK → multilingual-research → research-log-manager LOG → gap list |
| **Format Check** | structure-auditor → markdown-formatter → guidebook-auditor A+B |
| **Framing + Style** | framing-checker → prose-style-checker |
| **New Chapter** | content-gap-analyzer → research-log-manager CHECK → multilingual-research → research-log-manager LOG → citation-verifier → item-specification-writer → evidence brief |
| **Research Retrieval** | research-log-manager CHECK → if COMPLETE: retrieve BPC · if PARTIAL/STALE/NOT FOUND: multilingual-research → research-log-manager LOG |
| **Version Comparison** | version-diff on two aligned chunks |
| **Supplementary Volume** | supplemental-integrator → [find-and-replace · volii-validator · cross-reference-resolver] → guidebook-auditor A |
| **Document Assembly** | chunk-assembler → cross-reference-resolver → guidebook-auditor A |
| **Session Wrap** | session-consolidator |

**Parallel rule:** L2 and L4 agents in Full Section Review run independently. No L2/L4 agent takes another's output as input within the same level.

---

## Gap Register — Write Protocol
When any skill produces a gap item:
1. GET `gap_register.md` + SHA.
2. Append: `GAP-XXX | P{1|2|3} | OPEN | {skill} | {section} | {description} | {YYYY-MM-DD HH:MM}`
3. PUT back. Commit: `workplan-orchestrator: append GAP-XXX [{YYYY-MM-DD HH:MM}]`

Never overwrite CLOSED items.

---

## Skill Registry

### Orchestration
| Skill | Model | Role |
|---|---|---|
| `workplan-orchestrator` | — | This skill |
| `session-consolidator` | Sonnet 4.6 | Session end; YAML handoff to GitHub |

### Document Processing
| Skill | Model | Role |
|---|---|---|
| `haiku-chunker` | Haiku 4.5 | Chunk docs >500 lines; build section map |
| `structure-auditor` | Haiku 4.5 | Heading hierarchy; structural violations |
| `markdown-formatter` | Haiku 4.5 | Heading levels; markdown consistency |
| `chunk-assembler` | Haiku/Sonnet | Reassemble chunks in section-map order |
| `find-and-replace` | Haiku/Sonnet | Bulk text substitution with classification |
| `fix-linebreaks` | Haiku 4.5 | Join hard-wrapped prose lines from DOCX conversion |
| `table-formatter` | Haiku 4.5 | Table repair and standardisation |

### Content Analysis
| Skill | Model | Role |
|---|---|---|
| `guidebook-auditor` | Haiku (A/C/E) · Sonnet (B/D) | Format, consistency, structure |
| `content-gap-analyzer` | Sonnet 4.6 | Population and topic coverage gaps |
| `framing-checker` | Sonnet 4.6 | Social model framing; CRPD alignment |
| `evidence-auditor` | Sonnet 4.6 | Evidence stratification; overclaiming |
| `item-consolidation-analyzer` | Sonnet 4.6 | Merge/split/scope items |
| `version-diff` | Sonnet 4.6 | Semantic diff between versions |

### Writing and Specification
| Skill | Model | Role |
|---|---|---|
| `prose-style-checker` | Sonnet 4.6 | Register; concision; voice |
| `item-specification-writer` | Sonnet 4.6 | Draft and revise specifications |
| `vol2-item-formatter` | Haiku/Sonnet | Format and validate Vol 2 item blocks |
| `practice-note-generator` | Sonnet 4.6 | OT practitioner field tools |

### Research and Verification
| Skill | Model | Role |
|---|---|---|
| `citation-verifier` | Sonnet 4.6 | Citation audit; hallucination screen |
| `multilingual-research` | Sonnet 4.6 + web | 14-language search; CHECK before / LOG after |
| `research-log-manager` | Sonnet 4.6 | GitHub-backed search log and BPC |
| `literature-review-planner` | Sonnet 4.6 + web | Systematic review protocol; PRISMA |
| `economics-researcher` | Sonnet 4.6 + web | Economics evidence; funding programmes |
| `jurisdiction-tracker` | Sonnet 4.6 + web | Standards currency by jurisdiction |

### Reference Management
| Skill | Model | Role |
|---|---|---|
| `cross-reference-resolver` | Haiku/Sonnet | Audit and repair internal cross-references |
| `volii-validator` | Haiku/Sonnet | Item code validation |
| `supplemental-integrator` | Haiku/Sonnet | Integrate supplementary volumes |

### Reporting
| Skill | Model | Role |
|---|---|---|
| `critique-report-writer` | Sonnet 4.6 | Formal critique and review reports |

---

## Risk Escalation
After each analysis level: tally escalation signals (→ `references/project-standards.md`). ≥2 signals → append REVIEW item to `gap_register.md` on GitHub.

## Token Rules
Never re-run a completed stage. Consume existing outputs. Checkpoint per stage: 1–2 lines. Context limit approaching → complete stage, invoke `session-consolidator`, instruct user to start new chat. All timestamps: `YYYY-MM-DD HH:MM`.
