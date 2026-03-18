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
**Skill registry:** Full registry below.
**Rules:** `references/project-standards.md` (read from GitHub at session start)

---

## GitHub Backend

All persistent project state lives in `jordanelias/guidebook` on branch `main`.

**PAT:** Required at session start. If not present in context, prompt user before proceeding:
> "Please provide your GitHub PAT to continue."

**Read a file:**
```
GET https://api.github.com/repos/jordanelias/guidebook/contents/{path}
Authorization: token {PAT}
```
Response `content` field is base64-encoded. Decode before parsing. Capture `sha` for any subsequent write.

**Write a file:**
```
PUT https://api.github.com/repos/jordanelias/guidebook/contents/{path}
Authorization: token {PAT}
Body: { "message": "{commit message}", "content": "{base64-encoded}", "sha": "{current sha}" }
```
Always GET before PUT to obtain current SHA. On 409 conflict: re-GET and retry once.

**Commit message convention:**
```
workplan-orchestrator: {ACTION} [{YYYY-MM-DD HH:MM}]
```

---

## Session Start Protocol (mandatory — every new conversation)

Run this protocol before any task intake. Do not skip.

### Step 1 — Read session_log.md from GitHub
GET `session_log.md`. Decode. Find the most recent `session_close` YAML block.

- **YAML block found:** Report to user:
  ```
  Last session: {session_close datetime}
  Document: {document}
  Last stage completed: {last entry in skills_run}
  Next action: {next_action.skill} on {next_action.input_file}
  Open P1 gaps: {count from gaps_added minus gaps_resolved}
  Blockers: {blockers list or "none"}
  ```
  Confirm with user before resuming. Do not auto-resume.

- **No YAML block / file empty:** Report: "No prior session found. Starting fresh." Proceed to task intake.

### Step 2 — Read gap_register.md from GitHub
GET `gap_register.md`. Decode. Extract all OPEN P1 items.

- If P1 items exist: surface them to user before proceeding.
- If none: proceed silently.

### Step 3 — Read project-standards.md from GitHub
GET `references/project-standards.md`. Decode. Load rules into active context for this session.

### Step 4 — Confirm PAT is available
If PAT was not provided at session open: prompt now. Do not proceed to task intake without it.

---

## Task Intake

1. Session Start Protocol complete → proceed.
2. New task: identify scope + goal → select workflow → confirm with user in ≤3 lines → execute.
3. Resumed task: confirm next action from YAML block → execute from that stage.

**Skip condition:** user includes "fast-track" or "go" → skip user confirmation step only. Session Start Protocol still runs.

---

## Workflows

**Full Section Review**
L1 (Haiku): `haiku-chunker` A+B → section map + chunks
L2 (parallel): `structure-auditor` · `markdown-formatter` · `guidebook-auditor` A+B+C · `content-gap-analyzer` · `framing-checker` · `evidence-auditor`
L3: `research-log-manager` CHECK → `multilingual-research` (from L2 gaps) · `citation-verifier` (all claims) → `research-log-manager` LOG
L4 (Haiku ok): `guidebook-auditor` C · `volii-validator` provisional · `cross-reference-resolver`
→ aggregate → `prose-style-checker` → `critique-report-writer`

**Item Specification**
`item-consolidation-analyzer` → `item-specification-writer` → [`framing-checker` · `evidence-auditor`] → `prose-style-checker` → `volii-validator`

**Structural Change Package**
`structure-auditor` → `markdown-formatter` → `cross-reference-resolver` → `find-and-replace` → `guidebook-auditor` A

**Bulk Text Change**
`find-and-replace` (all six stages required — classification before execution)

**Citation Audit**
`citation-verifier` → `critique-report-writer` §7

**Evidence Gap**
`content-gap-analyzer` → `research-log-manager` CHECK → `multilingual-research` → `research-log-manager` LOG → gap list

**Format Check**
`structure-auditor` → `markdown-formatter` → `guidebook-auditor` A+B

**Framing + Style**
`framing-checker` → `prose-style-checker`

**New Chapter**
`content-gap-analyzer` → `research-log-manager` CHECK → `multilingual-research` → `research-log-manager` LOG → `citation-verifier` → `item-specification-writer` → evidence brief

**Research Retrieval**
`research-log-manager` CHECK → if COMPLETE: retrieve from BPC → pass to `item-specification-writer` · if PARTIAL/STALE/NOT FOUND: `multilingual-research` → `research-log-manager` LOG

**Version Comparison**
`version-diff` on two aligned chunks

**Supplementary Volume Integration**
`supplemental-integrator` → [`find-and-replace` · `volii-validator` · `cross-reference-resolver`] → `guidebook-auditor` A

**Document Assembly**
`chunk-assembler` (requires current section map) → `cross-reference-resolver` → `guidebook-auditor` A

**Session Wrap**
`session-consolidator`

**Parallel rule:** L2 and L4 agents in Full Section Review run independently. No agent takes another L2/L4 agent's output as input within the same level.

---

## Gap Register — Write Protocol

When any skill produces a gap item, write it to GitHub:

1. GET `gap_register.md` — capture content + SHA.
2. Append new OPEN item in this format:
   ```
   GAP-XXX | P{1|2|3} | OPEN | {skill} | {section} | {description} | {YYYY-MM-DD HH:MM}
   ```
3. PUT updated file back with SHA.
4. Commit message: `workplan-orchestrator: append GAP-XXX to gap_register [{YYYY-MM-DD HH:MM}]`

Never overwrite CLOSED items. Append only.

---

## Skill Registry

### Orchestration
| Skill | Model | Role |
|---|---|---|
| `workplan-orchestrator` | — | This skill |
| `session-consolidator` | Sonnet 4.6 | Session end; gap register; YAML handoff |

### Document Processing
| Skill | Model | Role |
|---|---|---|
| `haiku-chunker` | Haiku 4.5 | Chunk docs >500 lines; build section map |
| `structure-auditor` | Haiku 4.5 | Heading hierarchy audit; structural violations |
| `markdown-formatter` | Haiku 4.5 | Correct heading levels and markdown consistency |
| `chunk-assembler` | Haiku/Sonnet | Reassemble chunks; section-map-derived order |
| `find-and-replace` | Haiku/Sonnet | Bulk text substitution with classification and validation |
| `table-formatter` | Haiku 4.5 | Repair and standardise tables |

### Content Analysis
| Skill | Model | Role |
|---|---|---|
| `guidebook-auditor` | Haiku (A/C/E) · Sonnet (B/D) | Format, consistency, structure audit |
| `content-gap-analyzer` | Sonnet 4.6 | Population and topic coverage gap detection |
| `framing-checker` | Sonnet 4.6 | Social model framing; CRPD alignment |
| `evidence-auditor` | Sonnet 4.6 | Evidence stratification; overclaiming detection |
| `item-consolidation-analyzer` | Sonnet 4.6 | Merge/split/scope items within a category |
| `version-diff` | Sonnet 4.6 | Semantic diff between document versions |

### Writing and Specification
| Skill | Model | Role |
|---|---|---|
| `prose-style-checker` | Sonnet 4.6 | Project prose register; concision; voice |
| `item-specification-writer` | Sonnet 4.6 | Draft and revise item-level specifications |
| `practice-note-generator` | Sonnet 4.6 | OT practitioner field tools |

### Research and Verification
| Skill | Model | Role |
|---|---|---|
| `citation-verifier` | Sonnet 4.6 | Citation audit; hallucination screen |
| `multilingual-research` | Sonnet 4.6 + web | 14-language literature search; always preceded by research-log-manager CHECK and followed by LOG |
| `research-log-manager` | Sonnet 4.6 | GitHub-backed search log and best-practices compendium |
| `literature-review-planner` | Sonnet 4.6 + web | Systematic review protocol; PRISMA alignment |
| `economics-researcher` | Sonnet 4.6 + web | Economics evidence; funding programme research |
| `jurisdiction-tracker` | Sonnet 4.6 + web | Standards currency by jurisdiction |

### Reference Management
| Skill | Model | Role |
|---|---|---|
| `cross-reference-resolver` | Haiku/Sonnet | Audit and repair internal narrative cross-references |
| `volii-validator` | Haiku/Sonnet | Item code validation against application volume library |
| `supplemental-integrator` | Haiku/Sonnet | Integrate supplementary population volumes |

### Reporting
| Skill | Model | Role |
|---|---|---|
| `critique-report-writer` | Sonnet 4.6 | Formal critique and review reports |

---

## Risk Escalation
After each analysis level: tally escalation signals (→ `references/project-standards.md`). ≥2 signals → append REVIEW item to `gap_register.md` on GitHub with signals, section, and triggering skill.

---

## Token Rules
Never re-run a completed stage. Consume existing outputs. Checkpoint per stage: 1–2 lines only. Context limit approaching → complete stage, invoke `session-consolidator`, instruct user to start new chat.

All timestamps: `YYYY-MM-DD HH:MM`.
