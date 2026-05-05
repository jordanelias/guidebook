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
> **C2 overhaul 2026-05-05:** Session-start queries use SQLite. Saves ~7-8K tokens/session.


<!-- Updated: 2026-05-03 — Workplan v4 (Amendment 8), roadmap display on bootstrap, Stage B2 NEXT -->
<!-- Prior: CO-0008 2026-04-26 — Stage A workflows, Python-backed skill classification, Phase 2B dormant -->

**Model:** Opus 4.6 (primary for all work per CO-0008 PI update)
**GitHub backend:** `jordanelias/guidebook` · `main` · All GitHub operations use `github-io` patterns.

---

## Session Start Protocol (mandatory — every new conversation)

### 1a — Load core state (GraphQL batch_read — call 1)

Fetch in one call via github-io batch_read:
- `sessions/LATEST`
- `references/project-standards.md`
- `skills/workplan-orchestrator_SKILL.md`

Parse LATEST to get session filename.

> **Connection register (CO-0006 2026-04-08):** The monolithic `connection-register-active.md` is archived. Do NOT load it. Connection state is now in `references/connections/_index.md` (master index) + per-topic `connections.md` files. At session start, load `_index.md` only. Load per-topic files only when the session task touches that topic.

### 1b — Load session file (GraphQL batch_read — call 2)

Fetch the session file identified in LATEST AND `references/connections/_index.md` in the same call.
Report: session_close, next_action, blockers. Confirm with user before resuming. Do not auto-resume.

From `_index.md`: note count of PENDING HIGH-confidence connections — these are the highest-priority integration targets for any ISW session.

### 1c — Workplan roadmap (on any workplan-related bootstrap)

When the user's opening message mentions "workplan", "bootstrap", "roadmap", "where are we", "what's left", or similar — display this compact roadmap after reporting session state. Read `workplan/workplan-co0007-v4.md` §Budget arithmetic table and render:

```
ROADMAP — Accessible Built Environments Guidebook
══════════════════════════════════════════════════
Stage 0  Verification + decision freeze     ████████████████████ COMPLETE  (9 sessions)
Stage A  Foundations (A1-A13)                ████████████████████ COMPLETE  (24 sessions)
B1       Schema design                      ████████████████████ COMPLETE  (9 sessions)
─────────────────────────────────────────────────────────────────
B2       Schema impl + audit remediation    ░░░░░░░░░░░░░░░░░░░░ NEXT     (0/6-8)
B3       Navigation + website entities      ░░░░░░░░░░░░░░░░░░░░          (0/4-5)
B4       Pilot construction                 ░░░░░░░░░░░░░░░░░░░░          (0/6-10)
B5       Rendering layer                    ░░░░░░░░░░░░░░░░░░░░          (0/3-4)
B6       Pilot validation                   ░░░░░░░░░░░░░░░░░░░░          (0/3-4)
B7       Architecture lock                  ░░░░░░░░░░░░░░░░░░░░          (0/2)
─────────────────────────────────────────────────────────────────
C0-C11   Content migration + population     ░░░░░░░░░░░░░░░░░░░░          (0/121-177)
═════════════════════════════════════════════════════════════════
CONSUMED: 42 sessions  |  REMAINING: 146-211  |  TOTAL: 188-253
```

**Update rules for this roadmap:**
- As sessions complete within a sub-stage, update consumed count and fill bars proportionally
- When a sub-stage completes, mark it COMPLETE and fill the bar
- The roadmap is a rendering of the workplan budget table — it does not store independent state
- If the workplan is amended, the roadmap auto-reflects the new budget table
- For Stage C, show sub-stage breakdown only when C-stage work begins; until then, show as single line

### 2 — Load gap register (filtered bash)

Extract OPEN P1 items only from `SQLite gaps table`. Do not load full file.

### 2b — Data health check (conditional)

If `data/` directory exists:
```
pip install pydantic pyyaml --break-system-packages -q
python3 scripts/validate_schema.py --quick
```
Container does not persist pip packages between conversations — install before every Python tool call. Validates a random sample of entity YAML against Pydantic schemas. Catches data corruption between sessions. Skip if `data/` directory does not exist yet.

### 3 — Confirm PAT

If PAT not present in Project Instructions: prompt user.

### 4 — Task Intake

Select workflow → load required skills via batch_read (see §Workflow-Gated Loading below).
No skill outside the workflow list may execute without explicit user approval.

**Total startup:** 2 GraphQL calls + 1 filtered bash read + 1 optional validation. ~8K tokens.

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
| Apps | Appendices A, B, D, E, Bibliography, Glossary | — (follows Vol II) |
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

---

## Task Intake
New task: identify scope + goal → select workflow → confirm in ≤3 lines → execute.
Resumed task: confirm next action from YAML → execute from that stage.

---

## Skill Execution Patterns (CO-0008)

Every skill follows one of three execution patterns:

### Python Tool
Mechanical processing with defined I/O schemas. Claude calls the script via bash_tool; the script enforces constraints. Claude does not interpret the rules — the code does.
```
python3 scripts/{skill_name}.py --input <path> --output <path>
```

### Hybrid
Claude does the thinking (synthesis, writing, research judgment); the output is mechanically validated.
```
1. Claude reads skills/{name}_SKILL.md for guidance
2. Claude produces output (YAML with prose sections)
3. Claude calls: python3 skills/{name}_validate.py --check output.yaml
4. Validator reports pass/fail with field-level errors
5. Claude fixes errors before committing
```

### Prose Only
Guidance for Claude's judgment where output is not mechanically validatable. Voice, style, framing.

---

## Workflows

### Active Workflows (Stage A)

| Workflow | Skill sequence |
|---|---|
| **Governance + Code** | [read prior governance docs] → [draft governance document] → [write Pydantic schema in schemas/] → [write validator in scripts/] → [run conversion on sample data] → [fix edge cases] → [commit all: governance + schema + validator + converter] |
| **Infrastructure Build** | [throughline analysis] → [schema scaffolding] → [validator runner] → [proof-of-concept conversion] → [CI expansion] → [commit] |
| **Session Wrap** | session-consolidator |

### Dormant Workflows (Phase 2B — reactivate at Stage C)

These workflows are structurally sound but depend on skills that will be rebuilt as Python-backed tools during Stage A and C. Do not run until their constituent skills have been converted.

| Workflow | Skill sequence | Reactivation gate |
|---|---|---|
| **DOCX Conversion Prep** | fix-linebreaks → haiku-chunker → [analysis skills] | C-stage |
| **Full Section Review** | haiku-chunker → [structure-auditor · markdown-formatter · guidebook-auditor · content-gap-analyzer · framing-checker · evidence-auditor] → [research-log-manager CHECK · multilingual-research · citation-verifier · research-log-manager LOG] → [guidebook-auditor C · volii-validator · cross-reference-resolver] → prose-style-checker → critique-report-writer | C-stage: all analysis skills Python-backed |
| **Item Specification** | item-consolidation-analyzer → research-log-manager RETRIEVE → item-specification-writer (REF-IDs + sources-cited) → vol2-item-formatter (REF-ID validation) → [framing-checker · evidence-auditor] → prose-style-checker → volii-validator | A6 (evidence methodology): ISW output validator built |
| **Structural Change** | [structure-auditor · markdown-formatter (parallel)] → cross-reference-resolver → find-and-replace → guidebook-auditor A | C-stage |
| **Structural Nomenclature Change** | toc-editor → find-and-replace (per Change Order) → cross-reference-resolver → guidebook-auditor A | C-stage |
| **Bulk Text Change** | find-and-replace (all stages) | C-stage |
| **Citation Audit** | citation-verifier → critique-report-writer §7 | C-stage |
| **Evidence Gap** | content-gap-analyzer → research-log-manager CHECK → multilingual-research → research-log-manager LOG → gap list | A6 |
| **Format Check** | structure-auditor → markdown-formatter → guidebook-auditor A+B | C-stage |
| **Framing + Style** | framing-checker → prose-style-checker | Available (prose-only) |
| **New Chapter** | Compose: Evidence Gap → Item Specification workflows. | A6 |
| **Research Retrieval** | research-log-manager CHECK → if COMPLETE: RETRIEVE BPC · if PARTIAL/STALE/NOT FOUND: multilingual-research → research-log-manager LOG | Available (prose skills) |
| **Multilingual Research (full)** | research-log-manager CHECK → [view Keyword Compendium Part 3 + view Protocol v4 Networks] → multilingual-research (Step 1–4) → citation-miner → pre-LOG completeness check → research-log-manager LOG | Available (prose skills) |
| **Citation Mining** | citation-miner (backward) → citation-miner (forward) → research-log-manager LOG | Available (prose skills) |
| **Version Comparison** | version-diff on two aligned chunks | C-stage |
| **Supplementary Volume** | supplemental-integrator → [find-and-replace · volii-validator · cross-reference-resolver] → guidebook-auditor A | C-stage |
| **Document Assembly** | chunk-assembler → [bibliography-compiler · table-formatter (parallel)] → cross-reference-resolver → guidebook-auditor A | C-stage |
| **Renumbering** | bulk-renumber (from Change Order map) → cross-reference-resolver → structure-auditor | C-stage |
| **File Decomposition** | file-splitter → manifest verification | C-stage |
| **Evidence Marker Pass** | evidence-marker (classification) → evidence-auditor (marker verification). Audit mode only — runs on assembled volumes post-chunk-assembler. | C-stage |
| **Sensory QA** | sensory-coherence-checker → gap register updates → Part 5 development | C-stage |

**Note:** "Available" workflows use prose-only skills that remain functional. "C-stage" workflows depend on skills being rebuilt. Framing + Style and Research workflows can run now.

**Parallel rule:** L2 and L4 agents in Full Section Review run independently. No L2/L4 agent takes another's output as input within the same level.

---

## Gap Register — Write Protocol
When any skill produces a gap item:
1. GET `SQLite gaps table` + SHA via github-io.
2. Append: `GAP-XXX | P{1|2|3} | OPEN | {skill} | {section} | {description} | {YYYY-MM-DD HH:MM}`
3. PUT back via github-io. Commit: `workplan-orchestrator: append GAP-XXX [{YYYY-MM-DD HH:MM}]`

Never overwrite CLOSED items.

---

## Skill Index (CO-0008 classification)

### Python Tool (11)
Called via bash_tool. Script enforces constraints mechanically.

| Skill | Status |
|---|---|
| evidence-auditor | Hybrid (proof-of-concept validator built CO-0008) |
| evidence-marker | To convert (C-stage) |
| structure-auditor | To convert (C-stage) |
| volii-validator | To convert (C-stage) |
| cross-reference-resolver | To convert (A3 rewrite) |
| guidebook-auditor (validation checks) | To convert (C-stage) |
| content-gap-analyzer | To convert (C-stage) |
| bibliography-compiler | To convert (C-stage) |
| bulk-renumber | To convert (C-stage) |
| sensory-coherence-checker | To convert (C-stage) |
| validate_schema.py | Built (CO-0008) |

### Hybrid (15)
Claude reads SKILL.md for judgment; output validated by _validate.py.

| Skill | Validator status | Model |
|---|---|---|
| item-specification-writer | To build (A6) | Sonnet 4.6 |
| multilingual-research | To build (A6) | Opus 4.6 (synthesis) |
| citation-miner | To build (C-stage) | Sonnet 4.6 |
| citation-verifier | To build (C-stage) | Sonnet 4.6 |
| functional-deficit-researcher | To build (C-stage) | Opus 4.6 (synthesis) |
| connection-discovery | To build (B2) | Opus 4.6 |
| connection-auditor | To build (B2) | Sonnet 4.6 |
| cross-population-conflict-mapper | To build (C-stage) | Opus 4.6 (synthesis) |
| economics-researcher | To build (C-stage) | Sonnet 4.6 |
| jurisdiction-tracker | To build (A8) | Sonnet 4.6 |
| literature-review-planner | To build (C-stage) | Sonnet 4.6 |
| item-consolidation-analyzer | To build (C-stage) | Sonnet 4.6 |
| research-log-manager | To build (C-stage) | Sonnet 4.6 |
| practice-note-generator | To build (C-stage) | Sonnet 4.6 |
| critique-report-writer | To build (C-stage) | Sonnet 4.6 |

### Prose Only (4)
Guidance for Claude's judgment. No mechanical validation.

| Skill | Model |
|---|---|
| voice-style | Sonnet 4.6 |
| prose-style-checker | Sonnet 4.6 |
| workplan-orchestrator | Opus 4.6 |
| session-consolidator | Opus 4.6 |

### Infrastructure (2)
Unchanged.

| Skill |
|---|
| github-io |
| github-filing |

### Deprecated (10)
Replaced by Python tools or absorbed into other skills.

chunk-assembler · file-splitter · find-and-replace · fix-linebreaks · markdown-formatter · table-formatter · haiku-chunker · toc-editor · supplemental-integrator · vol2-item-formatter

### To build (Phase B/C)
poe-assessor · intersectionality-checker · index-generator · glossary-manager · figure-numbering · docx-exporter · accessibility-checker

---

## Stage A Skill Build Schedule

| Phase | Python tools co-produced | Hybrid validators co-produced |
|---|---|---|
| Infrastructure (CO-0008) | validate_schema.py, convert_spec_db.py | evidence_auditor_validate.py (proof of concept) |
| A3 (Conceptual model) | validate_entities.py, validate_cross_refs.py (rewrite), convert_bpc_metadata.py, convert_connections.py | — |
| A6 (Evidence methodology) | validate_evidence_state.py, convert_sources.py | multilingual-research output validator |
| A7 (Population taxonomy) | validate_population.py | — |
| A8 (Jurisdiction philosophy) | validate_jurisdiction.py, convert_jurisdictions.py | jurisdiction-tracker output validator |
| A9 (Time model) | validate_temporal.py, version_retrofit.py | — |
| A10 (Adversarial-use review) | audit_adversarial_use.py | — |
| A12 (Decision protocol) | decision_capture.py | — |
| A13 (Doctrine recheck) | doctrine_recheck.py, contamination_sampler.py | — |

---

## Risk Escalation
After each analysis level: tally escalation signals (→ `references/project-standards.md`). ≥2 signals → append REVIEW item to `SQLite gaps table` via github-io.

## Token Rules
Never re-run a completed stage. Consume existing outputs. Checkpoint per stage: 1–2 lines. Context limit approaching → complete stage, invoke `session-consolidator`, instruct user to start new chat. All timestamps: `YYYY-MM-DD HH:MM`.
