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
> **Phase 1-C update 2026-05-04:** Steps 1b and 2 now use `db.py` CLI instead of markdown registers.


<!-- Updated: 2026-05-04 — Phase 1-C: session-start SQLite migration (1b connections, 2 gaps) -->
<!-- Prior: CO-0008 2026-04-26 — Stage A workflows, Python-backed skill classification, Phase 2B dormant -->

**Model:** Opus-class (primary for all work per CO-0008 PI update)
**GitHub backend:** `jordanelias/guidebook` · `main` · All GitHub operations use `github-io` patterns.

---

## Session Start Protocol (mandatory — every new conversation)

### 1a — Load core state (GraphQL batch_read — call 1)

Load:
- `references/project-standards.md` — the append-only operative rule ledger
- the **newest** dated file(s) in `workplan/` that match your task

> **[CORRECTED 2026-08-04] There is no single canonical plan.** This step used to
> name `workplan/workplan-co0007-v4.md` as "canonical operative plan (always
> load)". **That file does not exist.** Several dated workplans
> coexist by design (consolidation, coverage-completion, remediation, fork-cut, …);
> sort `workplan/` by date and read the newest that matches the task at hand. Do
> not treat any one of them as authority over the others, and do not trust a date
> written inside one — derive current state from the DB and `git log`.

> **`sessions/LATEST` is NOT a reliable session pointer** (CLAUDE.md §7, "Two session
> pointers" — pointer corrected 2026-08-22, was §10). It is
> being asked to mean both "most recent session" and "most recent *research*
> session", and it currently names a session that logged zero `evidence_sources`
> rows. Splitting it is W4.1 of `workplan/2026-08-02-architecture-decision-and-execution-plan.md`
> and is owner-gated. Find the current handoff via the newest `workplan/` file instead.

> **Connection register (Phase 1 SQLite — 2026-05-05):** All connection state is in `data/guidebook.db`. Do NOT load `references/connections/_index.md` (archived). Query connections via `python3 scripts/db.py connections`. Per-topic `connections.md` files are archived — do not read or write.

> ~~**Workplan authority (2026-05-08):** `workplan-co0007-v4.md` is the only operative plan. All other workplan files are either deprecated (with explicit banners) or tactical references subordinate to v4. Do not load or follow any other workplan for session planning.~~ **[SUPERSEDED 2026-08-04 — the named file does not exist and the single-plan model was abandoned; see the correction above; CLAUDE.md §8's table now answers "what to do now" with the
> operative DR, not with a workplan file. Pointer corrected 2026-08-22, was §9.]** `workplan/workplan-reconciliation-2026-05-08.md` remains readable as the historical supersession map.

### 1b — Load session file + connection summary (GraphQL + bash — call 2)

Fetch the session file identified in LATEST via GraphQL.
Report: session_close, next_action, blockers. Confirm with user before resuming. Do not auto-resume.

Query PENDING HIGH-confidence connections via SQLite (saves ~4K tokens vs loading `_index.md`):
```bash
python3 scripts/db.py connections --status PENDING --confidence HIGH
```
Note count — these are the highest-priority integration targets for any ISW session.

### 1c — Workplan roadmap (display)

When the user asks "where are we", "what's left" or similar, **derive the answer
from the live repo** — the newest `workplan/` file, recent `git log`, and the DB —
not from the block below.

> **[SUPERSEDED 2026-08-04] The roadmap below is a May-2026 snapshot and its
> instruction to "render from v4" points at a file that does not exist.** It shows
> C1 as ACTIVE and every C-stage at zero; since then the project has run Phase B/E
> rehabilitation, the SQLite substrate, D-0157, and the fork-cut work — none of
> which this ladder can express. It is retained only as a record of how the work
> was originally staged. **Do not report it to a user as current status.**

```
ROADMAP — Accessible Built Environments Guidebook (May 2026 snapshot — SUPERSEDED)
══════════════════════════════════════════════════
Stage 0  Verification + decision freeze     ████████████████████ COMPLETE  (9 sessions)
Stage A  Foundations (A1-A13)                ████████████████████ COMPLETE  (24 sessions)
B1       Schema design                      ████████████████████ COMPLETE  (9 sessions)
B2-B4.1  Schema impl + pilot                ████████████████████ COMPLETE  (1 session)
C0       Bulk migration                     ████████████████████ COMPLETE  (same session)
─────────────────────────────────────────────────────────────────
C1       Migration tooling                  ░░░░░░░░░░░░░░░░░░░░ ACTIVE   (0/3-5)
C2       Skill set rebuild                  ░░░░░░░░░░░░░░░░░░░░          (0/10-14)
C3       Specification pages                ░░░░░░░░░░░░░░░░░░░░          (0/25-35)
C4       Population pages                   ░░░░░░░░░░░░░░░░░░░░          (0/12-18)
C5       Room pages                         ░░░░░░░░░░░░░░░░░░░░          (0/15-22)
C6       Conflict pages                     ░░░░░░░░░░░░░░░░░░░░          (0/10-15)
C7       Evidence + bibliography            ░░░░░░░░░░░░░░░░░░░░          (0/12-17)
C8       Jurisdiction content               ░░░░░░░░░░░░░░░░░░░░          (0/6-10)
C9       Cross-cutting prose (Opus)         ░░░░░░░░░░░░░░░░░░░░          (0/18-25)
C10      Quality gates                      ░░░░░░░░░░░░░░░░░░░░          (0/5-8)
C11      Maintenance lifecycle              ░░░░░░░░░░░░░░░░░░░░          (0/3-5)
─────────────────────────────────────────────────────────────────
B4.2-B7  Deferred (post-content)            ░░░░░░░░░░░░░░░░░░░░          (0/14-20)
═════════════════════════════════════════════════════════════════
CONSUMED: ~43 sessions  |  REMAINING: ~145-210  |  TOTAL: 188-253
```

**Do not update this block.** It is a superseded snapshot, not a live tracker;
editing it would recreate the false impression that it reflects current state.

### 2 — Load gap register (SQLite query)

Extract OPEN P1 items only:
```bash
python3 scripts/db.py gaps --status OPEN --priority P1
```
Do not load `gap_register.md` (archived).

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

#### 4a — Block gate check (mandatory before any Phase A content workflow)

Run before selecting any workflow. Uses only files already on disk from steps 1–3 — no additional downloads.

```bash
# PAT sourced from Project Instructions (see bootstrap §<project_identity>)
REPO="jordanelias/guidebook"
AUTH="Authorization: Bearer $PAT"

# HEAD-only checks — no file download
_exists() { curl -so /dev/null -w "%{http_code}" -H "$AUTH" \
  "https://api.github.com/repos/$REPO/contents/$1"; }

# Gate checks
B0=$([ "$(_exists scripts/validate_bpc.py)" = "200" ] && \
     [ "$(_exists .github/workflows/ci.yml)" = "200" ] && echo PASS || echo FAIL)

B1=$([ "$B0" = "PASS" ] && \
     [ "$(_exists gap_register_archive.md)" = "200" ] && \
     [ "$(_exists references/parser-source-readiness.md)" = "200" ] && echo PASS || echo FAIL)

B3=$([ "$B1" = "PASS" ] && \
     [ "$(_exists references/part04-item-index.md)" = "200" ] && \
     [ "$(_exists references/spec-db-part4-reconciliation.md)" = "200" ] && echo PASS || echo FAIL)

PENDING=$(python3 -c "import sqlite3; \
  print(sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True) \
  .execute(\"SELECT COUNT(*) FROM connections WHERE status='PENDING'\") \
  .fetchone()[0])" 2>/dev/null || echo "?")

B4=$([ "$B3" = "PASS" ] && [ "$PENDING" = "0" ] && echo PASS || echo FAIL)

# Dependency-graph output (B2 unlocks with B0 only, parallel to B3)
echo "=== BLOCK GATE ==="
echo "  B0 enforcement infra  : $B0"
echo "  B1 cleanup + audit    : $B1  $([ "$B0" != "PASS" ] && echo '[locked: B0]')"
echo "  B2 citation migration : $([ "$B0" = "PASS" ] && echo "UNLOCKED (dep:B0)" || echo "LOCKED [dep:B0]")"
echo "  B3 spec completeness  : $([ "$B3" = "PASS" ] && echo "PASS" || echo "LOCKED [dep:B1]")  $([ "$B1" != "PASS" ] && echo '→ complete B1 first')"
echo "  B4 connection consump : $([ "$B4" = "PASS" ] && echo "UNLOCKED" || echo "LOCKED")  $([ "$B3" != "PASS" ] && echo '[dep:B3]')$([ "$PENDING" != "0" ] && echo "[PENDING=$PENDING — must be 0]")"
echo "  B5 readiness audit    : $([ "$B4" = "PASS" ] && echo "UNLOCKED" || echo "LOCKED [dep:B4]")"
```

**Gate enforcement rule** — apply to every incoming task before workflow selection. Map user requests to v4 C-stages:

| If the user wants to do… | v4 stage | Gate action |
|---|---|---|
| BPC CO-0006 migration, citation enrichment | C1 (migration tooling) + C7 (evidence base) | Proceed — B0 PASS is sufficient |
| Part 4 spec completion, ISW, annotations | C3 (specification pages) | Check: part04-item-index exists |
| Connection consumption, ISW cross-refs | C3 (36 CON-HIGH entries) | Check: PENDING=0 required |
| Prose edits to Parts 1, 10, 11, 12 | C9 (cross-cutting prose — **Opus required**) | Check: C3 substantially complete first; confirm Opus model |
| Hallucination audit, GRADE ratings | C7 / C3 | Proceed with appropriate checks |
| Schema work, migration scripts, validators | C1 / C2 | Proceed — governance/infra always allowed |
| Final readiness audit | C10 | Check: C3-C9 substantially complete |
| Governance, infra, session wrap | Any | Never blocked |

If a content workflow is BLOCKED, respond with:
```
BLOCK GATE: [task] maps to v4 [C-stage] which requires [prerequisite].
Gate failures: [specific check results]
Permitted work this session: [list unlocked C-stages]
To unblock: [specific action needed]
```
Do not proceed with the blocked workflow. Do not substitute adjacent work.

#### 4b — Workflow selection

Select workflow → load required skills via batch_read (see §Workflow-Gated Loading below).
No skill outside the workflow list may execute without explicit user approval.

**Total startup:** 2 GraphQL calls + 1 filtered bash read + 1 optional validation + 5 HEAD requests (gate). ~8K tokens.

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

## Population Codes

**Do not read a population list out of a skill file — query the table.**

```bash
python3 -c "import sqlite3; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); \
  [print(f'{r[0]:<12}{r[1]}') for r in c.execute('SELECT population_code, display_name FROM populations ORDER BY 1')]"
```

The set is **23 flat codes**, ratified by `DR-2026-07-23` and mirrored exactly by
`schemas/enums.py:PopulationCode`. Curate *from the functional axes* — never coin
umbrella codes (`governance/functional-taxonomy.md` §3.3, RULE 2026-07-22,
`DR-2026-07-22-work-from-axes`).

> **[CORRECTED 2026-08-04] The table that stood here was wrong on roughly half its
> rows and was labelled "canonical".** It listed `VIS`, `NEU`, `DBL`, `OFS`,
> `IntD` and `NDV/MH` — **none of which exist** in `populations`. The
> 2026-07-21/22 reclassification replaced them (`VIS`→`BLIND`, `DBL`→`DEAFBLIND`,
> the orthostatic/fatigue group→`COM`, `IntD`→`ID`, and so on) and added `LMB`,
> `MOVE`, `BRAIN`, `LPA`, `TALL`, `VES`, `EPI`, `MS`, `SCI`.
>
> Two of its rules were not merely stale but **inverted**:
> - *"VIS/DEAF is invalid"* — correct in outcome, but `table-formatter_SKILL.md`
>   simultaneously mandates a `VIS/DEAF` matrix column as "canonical, never
>   reorder". Neither code exists; the pair contradicted each other on a code that
>   is simply gone.
> - *"BAR is NOT main taxonomy … BAR in Volumes I–II = error"* — **`BAR` is an
>   active population** in the live table (fat people; people in larger bodies).
>   It carries one `item_population_links` row today, so it is thinly populated,
>   not illegitimate. Flagging it as an error was doctrine-inverting.

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

> **Block gate governs workflow selection.** Run §4a before selecting any Phase A content workflow. See §4a for the dependency graph, gate check commands, and enforcement rules. The table below lists which block each workflow belongs to — if that block is LOCKED, the workflow is BLOCKED.

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
Gaps live in the `gaps` table (313 rows), not in a file. Write one with:

```bash
python3 scripts/db.py add-gap --priority P1 --category AUDT \
  --description "..." --session "$SESSION"
```

> **[CORRECTED 2026-08-04]** These steps read *"GET `SQLite gaps table` + SHA via
> github-io … PUT back"* — a literal placeholder string left by a find-and-replace
> that swept `gap_register.md` out of the skills, producing an instruction to
> fetch and commit a **file named "SQLite gaps table"**. `gap_register.md` was
> archived; the register is a table. The same placeholder appears elsewhere in
> this file and in three other skills.

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
| item-specification-writer | To build (A6) | Sonnet-class |
| multilingual-research | To build (A6) | Opus-class or above (synthesis) |
| citation-miner | To build (C-stage) | Sonnet-class |
| citation-verifier | To build (C-stage) | Sonnet-class |
| functional-deficit-researcher | To build (C-stage) | Opus-class or above (synthesis) |
| connection-discovery | To build (B2) | Opus-class |
| connection-auditor | To build (B2) | Sonnet-class |
| cross-population-conflict-mapper | To build (C-stage) | Opus-class or above (synthesis) |
| economics-researcher | To build (C-stage) | Sonnet-class |
| jurisdiction-tracker | To build (A8) | Sonnet-class |
| literature-review-planner | To build (C-stage) | Sonnet-class |
| item-consolidation-analyzer | To build (C-stage) | Sonnet-class |
| research-log-manager | To build (C-stage) | Sonnet-class |
| practice-note-generator | To build (C-stage) | Sonnet-class |
| critique-report-writer | To build (C-stage) | Sonnet-class |

### Prose Only (4)
Guidance for Claude's judgment. No mechanical validation.

| Skill | Model |
|---|---|
| voice-style | Sonnet-class |
| prose-style-checker | Sonnet-class |
| workplan-orchestrator | Opus-class |
| session-consolidator | Opus-class |

### Infrastructure (2)
Unchanged.

| Skill |
|---|
| github-io |
| github-filing |

### Deprecated (5)
Replaced by Python tools or absorbed into other skills. These are the files that
actually live in `skills/deprecated/`:

chunk-assembler · file-splitter · fix-linebreaks · haiku-chunker · vol2-item-formatter

> **[CORRECTED 2026-08-04]** This list named **ten**, five of which are live skills
> in `skills/`: `find-and-replace`, `markdown-formatter`, `table-formatter`,
> `toc-editor`, `supplemental-integrator`. An agent trusting this roster would
> refuse to use five available skills. Verified against the filesystem, not the
> registry — `references/skill-registry.md` is itself incomplete (it omits
> `integrity-protocol` and `supersession-audit`, both live).
>
> The full deprecated set in `skills/deprecated/` is larger than five (it also
> holds `bibliography-updater`, `bulk-renumber`, `connection-scout`,
> `evidence-marker`, `keyword-lookup`, `neufert-image-analyzer`); the five above
> are only the ones this list previously got right. **Check the directory, not
> this table.**

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
| A9 (Time model) | ~~validate_temporal.py~~ (DELETED 2026-08-20 — quarantined 2026-08-04 as passing on zero records, `data/temporal/` never existed), version_retrofit.py (its generator, never run) | — |
| A10 (Adversarial-use review) | audit_adversarial_use.py | — |
| A12 (Decision protocol) | decision_capture.py | — |
| A13 (Doctrine recheck) | doctrine_recheck.py (~~contamination_sampler.py~~ DELETED 2026-08-20) | — |

---

## Risk Escalation
After each analysis level: tally escalation signals (→ `references/project-standards.md`). ≥2 signals → record a REVIEW gap with `python3 scripts/db.py add-gap` (see the Gap Register write protocol above; the `SQLite gaps table` placeholder that stood here was a find-and-replace artifact).

## Token Rules
Never re-run a completed stage. Consume existing outputs. Checkpoint per stage: 1–2 lines. Context limit approaching → complete stage, invoke `session-consolidator`, instruct user to start new chat. All timestamps: `YYYY-MM-DD HH:MM`.
