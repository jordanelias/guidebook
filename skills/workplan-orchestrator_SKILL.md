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
**GitHub backend:** `jordanelias/guidebook` · `main` · All GitHub operations use `github-io` patterns.

---

## Session Start Protocol (mandatory — every new conversation)

### 1 — Load session state
Session logs are stored at `sessions/session_YYYY-MM-DD-HHMM.md` (one file per session).
1. GET `sessions/` directory listing via github-io.
2. Sort by filename descending. GET the most recent file.
3. Find the `session_close` YAML block within it.
- **Found:** Report last session datetime, last skill run, next action, open P1 gap count, blockers. Confirm with user before resuming. Do not auto-resume.
- **Empty/not found:** "No prior session. Starting fresh."

### 2 — Load gap register (filtered)
Extract OPEN P1 items from `gap_register.md` via filtered fetch — do not load the full file:

```bash
curl -sL -H "Authorization: token ${PAT}" \
  "https://api.github.com/repos/jordanelias/guidebook/contents/gap_register.md" \
  | python3 -c "import sys,json,base64; d=json.load(sys.stdin); c=base64.b64decode(d['content']).decode(); [print(l) for l in c.split('\n') if '| OPEN |' in l or '| P1 |' in l]"
```

Surface OPEN P1 items to user if any; otherwise proceed silently.

### 3 — Load project standards
GET `references/project-standards.md`. Load rules into active context.

### 4 — File stale versioned files
For each watched directory (`workplan/`, `versions/current/`):
- GET directory listing.
- Count non-directory files not already in a `deprecated/` subdirectory.
- **Count = 1:** proceed silently.
- **Count > 1:** invoke `github-filing` on that directory before continuing. Do not prompt user — file automatically and report result inline.

### 5 — Confirm PAT
If PAT not yet provided: prompt user. Do not proceed without it.

**Skip condition:** "fast-track" or "go" skips user confirmation at Task Intake only. Protocol still runs.

---

## CO-0004 Part Numbering Map (canonical — supersedes v10.1)

**CO-0004 date:** 2026-03-29. 13 Parts → 12 Parts. 3 Volumes → 2 Volumes.

| Part | Title | Volume |
|---|---|---|
| 1 | Foundations of Accessible Design | I |
| 2 | Disability Categories | I |
| 3 | Synthesis, Sequencing and the Co-Occurrence Framework | I |
| 4 | Item Specification Library (Categories A–K) | I |
| 5 | Building-Level Co-Occurrence Resolution | I |
| 6 | Residential Application Matrices | I |
| 7 | Non-Residential Application Matrices | I |
| 8 | Engineering and Coordination | I |
| 9 | Working with Specialist Consultants | I |
| 10 | Design for Adaptable Readiness — DAR | II |
| 11 | The Economics of Accessible Construction | II |
| 12 | Case Studies — Documented Accessible Built Environments | II |
| Apps | Appendices A, B, D, E, Bibliography, Glossary | II |
| Supp | Supplementary Volume: Body Sizes | — |

Section numbering follows Part number: Part N uses §N.x. Item codes in Part 4 use letter-prefix: A-01 through K-NN. **Bare codes only — no volume-part prefix.**

Full old→new mapping: `workplan/P1-D2-D3-co0004-remapping.md`.

---
## Population Codes (canonical)

| Code | Label |
|---|---|
| MOB | Mobility & Strength (MOB/AMB, MOB/UPL) |
| VIS | Visual impairment |
| DEAF | Deaf / hard of hearing / hearing device users |
| NEU | Neurological / ABI (NEU/PCS) |
| DEM | Dementia |
| NDV | Neurodivergence (NDV/AUT, NDV/ADHD, NDV/SENS) |
| NDV/MH | Mental health / PTSD / trauma |
| PAIN | Chronic pain / fibromyalgia |
| DBL | DeafBlind |
| OFS | Orthostatic & fatigue spectrum (OFS/ME, OFS/POTS, OFS/MCAS) |
| IntD | Intellectual disability |
| ALL | All disability categories |

VIS, DEAF, DBL: three distinct codes. VIS/DEAF is invalid. DBL ≠ VIS + DEAF.
BAR is NOT main taxonomy. Large body size → Supp. Part 4 only. BAR in Volumes I–II = error.
Supplementary only (not main taxonomy): CHD · LPA · EXH · BAR.


## Task Intake
New task: identify scope + goal → select workflow → confirm in ≤3 lines → execute.
Resumed task: confirm next action from YAML → execute from that stage.

---

## Workflows

| Workflow | Skill sequence |
|---|---|
| **DOCX Conversion Prep** | fix-linebreaks → haiku-chunker → [analysis skills] |
| **Full Section Review** | haiku-chunker → [structure-auditor · markdown-formatter · guidebook-auditor · content-gap-analyzer · framing-checker · evidence-auditor] → [research-log-manager CHECK · multilingual-research · citation-verifier · research-log-manager LOG] → [guidebook-auditor C · volii-validator · cross-reference-resolver] → prose-style-checker → critique-report-writer |
| **Item Specification** | item-consolidation-analyzer → item-specification-writer → [framing-checker · evidence-auditor] → evidence-marker → prose-style-checker → vol2-item-formatter → volii-validator |
| **Structural Change** | structure-auditor → markdown-formatter → cross-reference-resolver → find-and-replace → guidebook-auditor A |
| **Structural Nomenclature Change** | toc-editor → find-and-replace (per Change Order) → cross-reference-resolver → guidebook-auditor A |
| **Bulk Text Change** | find-and-replace (all stages) |
| **Citation Audit** | citation-verifier → critique-report-writer §7 |
| **Evidence Gap** | content-gap-analyzer → research-log-manager CHECK → multilingual-research → research-log-manager LOG → gap list |
| **Format Check** | structure-auditor → markdown-formatter → guidebook-auditor A+B |
| **Framing + Style** | framing-checker → prose-style-checker |
| **New Chapter** | content-gap-analyzer → research-log-manager CHECK → multilingual-research → research-log-manager LOG → citation-verifier → item-specification-writer → evidence-marker → evidence brief |
| **Research Retrieval** | research-log-manager CHECK → if COMPLETE: RETRIEVE BPC · if PARTIAL/STALE/NOT FOUND: multilingual-research → research-log-manager LOG |
| **Multilingual Research (full)** | research-log-manager CHECK → [view Keyword Compendium + view Protocol v4 Networks] → multilingual-research (Step 1–4) → citation-miner → pre-LOG completeness check → research-log-manager LOG |
| **Citation Mining** | citation-miner (backward) → citation-miner (forward) → research-log-manager LOG |
| **Version Comparison** | version-diff on two aligned chunks |
| **Supplementary Volume** | supplemental-integrator → [find-and-replace · volii-validator · cross-reference-resolver] → guidebook-auditor A |
| **Document Assembly** | chunk-assembler (manifest mode) → cross-reference-resolver → guidebook-auditor A |
| **Renumbering** | bulk-renumber (from Change Order map) → cross-reference-resolver → structure-auditor |
| **File Decomposition** | file-splitter → manifest verification |
| **Evidence Marker Pass** | evidence-marker (classification) → evidence-auditor (marker verification) |
| **Sensory QA** | sensory-coherence-checker → gap register updates → Part 8 development |
| **Session Wrap** | session-consolidator |

**Parallel rule:** L2 and L4 agents in Full Section Review run independently. No L2/L4 agent takes another's output as input within the same level.

---

## Gap Register — Write Protocol
When any skill produces a gap item:
1. GET `gap_register.md` + SHA via github-io.
2. Append: `GAP-XXX | P{1|2|3} | OPEN | {skill} | {section} | {description} | {YYYY-MM-DD HH:MM}`
3. PUT back via github-io. Commit: `workplan-orchestrator: append GAP-XXX [{YYYY-MM-DD HH:MM}]`

Never overwrite CLOSED items.

---

## Skill Registry

### Orchestration
| Skill | Model | Role |
|---|---|---|
| `workplan-orchestrator` | — | This skill |
| `session-consolidator` | Sonnet 4.6 | Session end; YAML handoff to GitHub |

### Infrastructure
| Skill | Model | Role |
|---|---|---|
| `github-io` | Any | Standardised GitHub read/write/list; all skills use this |

### Document Processing
| Skill | Model | Role |
|---|---|---|
| `haiku-chunker` | Haiku 4.5 | Chunk docs >500 lines; build section map |
| `structure-auditor` | Haiku 4.5 | Heading hierarchy; structural violations; v10.1 numbering |
| `markdown-formatter` | Haiku 4.5 | Heading levels; markdown consistency |
| `chunk-assembler` | Haiku/Sonnet | Reassemble from manifest (v10.1) or section map |
| `find-and-replace` | Haiku/Sonnet | Bulk text substitution with classification |
| `fix-linebreaks` | Haiku 4.5 | Join hard-wrapped prose lines from DOCX conversion |
| `table-formatter` | Haiku 4.5 | Table repair and standardisation |
| `toc-editor` | Sonnet 4.6 | Structural changes; Change Orders; always requires pre-flight |
| `file-splitter` | Haiku 4.5 | Decompose master to per-Part files (Phase 4) |
| `bulk-renumber` | Haiku/Sonnet | Context-aware §-reference rewriting (Phase 4) |

### Content Analysis
| Skill | Model | Role |
|---|---|---|
| `guidebook-auditor` | Haiku (A/C/E) · Sonnet (B/D) | Format, consistency, structure |
| `content-gap-analyzer` | Sonnet 4.6 | Population and topic coverage gaps |
| `framing-checker` | Sonnet 4.6 | Social model; CRPD; BAR-in-Vol-I; marker framing |
| `evidence-auditor` | Sonnet 4.6 | Evidence stratification; overclaiming; ●/○ verification |
| `evidence-marker` | Sonnet 4.6 | ●/○ classification, audit, and upgrade |
| `item-consolidation-analyzer` | Sonnet 4.6 | Merge/split/scope items |
| `version-diff` | Sonnet 4.6 | Semantic diff between versions |
| `sensory-coherence-checker` | Sonnet 4.6 | Sensory consistency across room matrices (Phase 5) |

### Writing and Specification
| Skill | Model | Role |
|---|---|---|
| `prose-style-checker` | Sonnet 4.6 | Register; concision; voice |
| `item-specification-writer` | Sonnet 4.6 | Draft/revise specs; ●/○ template; K-category; illustration note |
| `vol2-item-formatter` | Haiku/Sonnet | Format and validate item blocks; ●/○ system |
| `practice-note-generator` | Sonnet 4.6 | OT practitioner field tools |

### Research and Verification
| Skill | Model | Role |
|---|---|---|
| `citation-verifier` | Sonnet 4.6 | Citation audit; hallucination screen; HARVEST mode |
| `multilingual-research` | Sonnet 4.6 + web | 14-language × 24-jurisdiction search per v4 protocol |
| `research-log-manager` | Sonnet 4.6 | GitHub-backed search log and BPC |
| `literature-review-planner` | Sonnet 4.6 + web | Systematic review protocol |
| `economics-researcher` | Sonnet 4.6 + web | Economics evidence; funding programmes |
| `jurisdiction-tracker` | Sonnet 4.6 + web | Standards currency by jurisdiction |
| `citation-miner` | Sonnet 4.6 + web | Backward + forward citation mining |

### Reference Management
| Skill | Model | Role |
|---|---|---|
| `cross-reference-resolver` | Haiku/Sonnet | Audit/repair refs; BPC↔Item traceability; per-Part file aware |
| `volii-validator` | Haiku/Sonnet | Item code validation |
| `supplemental-integrator` | Haiku/Sonnet | Integrate supplementary volumes |

### Reporting
| Skill | Model | Role |
|---|---|---|
| `critique-report-writer` | Sonnet 4.6 | Formal critique and review reports |

**Retired:** `vol1-corrections-writer` · `vol2-revision` · `plain-language-synthesizer` · `neufert-image-analyzer` · `keyword-lookup`

**To build (P2):** `poe-assessor` · `intersectionality-checker`

---

## Risk Escalation
After each analysis level: tally escalation signals (→ `references/project-standards.md`). ≥2 signals → append REVIEW item to `gap_register.md` via github-io.

## Token Rules
Never re-run a completed stage. Consume existing outputs. Checkpoint per stage: 1–2 lines. Context limit approaching → complete stage, invoke `session-consolidator`, instruct user to start new chat. All timestamps: `YYYY-MM-DD HH:MM`.
