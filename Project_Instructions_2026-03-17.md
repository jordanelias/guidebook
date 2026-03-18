# Project Instructions — Technical Guidebook Review System
**Last revised:** 2026-03-17 17:00
**Supersedes:** 2026-03-17 (earlier version this session)

---

## Overview

This project produces, audits, and critiques **technical guidebooks** for occupational therapy (OT) practitioners, architects, and policy makers. The primary lens is occupational therapy evidence.

**Current instance:** Guidebook for Accessible Design
**Active version:** V8.8 2026-03-12 14:00
**Primary file:** `Guidebook for Accessible Design 8.8 2026-03-12-14-00.md` (~17,900 lines)

**Architecture:** Skills live in Project Files (`/mnt/project/`). Persistent state lives on GitHub. See §GitHub API and §State Files.

---

## GitHub API

**Repo:** `jordanelias/guidebook` · branch `main`
**PAT:** Required at every session start. Prompt user if not provided. Never proceed without it.

### Read
```
GET https://api.github.com/repos/jordanelias/guidebook/contents/{path}
Authorization: token {PAT}
```
`content` field is base64-encoded. Decode before parsing. Capture `sha` for any write.

### Write
```
PUT https://api.github.com/repos/jordanelias/guidebook/contents/{path}
Authorization: token {PAT}
Body: {"message": "{commit message}", "content": "{base64-encoded}", "sha": "{current sha}"}
```
Always GET before PUT to obtain current SHA. On 409 conflict: re-GET and retry once.
On failure after retry: output content to chat as fenced code block with manual paste instructions. Never silently drop state.

### Commit message convention
`{skill-name}: {action} [{YYYY-MM-DD HH:MM}]`

---

## State Files (GitHub — persistent across sessions)

| File | Purpose | Writer |
|---|---|---|
| `session_log.md` | Rolling session YAML blocks | session-consolidator |
| `gap_register.md` | Typed gap register — append-only | workplan-orchestrator + contributing skills |
| `references/project-standards.md` | Canonical rules — append-only | session-consolidator |
| `references/search-log.md` | Per-topic search coverage index | research-log-manager |
| `references/best-practices-compendium.md` | Synthesised BPC entries per slug | research-log-manager |

---

## Session Start (mandatory — every new conversation)

`workplan-orchestrator` runs this protocol before any task. Do not skip.

1. **GET `session_log.md`** — find most recent `session_close` YAML. Report to user; confirm before resuming. If empty: "Starting fresh."
2. **GET `gap_register.md`** — surface OPEN P1 items if any.
3. **GET `references/project-standards.md`** — load rules into context.
4. **Confirm PAT** — prompt if not yet provided.

**Skip condition:** "fast-track" or "go" skips user confirmation at Task Intake only. Protocol still runs.

---

## Session Length
Once 95% of usage is spent: cease tasks <90% finished. Invoke `session-consolidator`. Write session-close YAML to GitHub. Produce bullet-point handoff summary for next session.

---

## Population Codes (canonical — never collapse sub-codes)

| Code | Label |
|---|---|
| MOB | Mobility & Strength (MOB/AMB, MOB/UPL) |
| VIS/vis | Visual impairment |
| VIS/DEAF | Deaf / hard of hearing / hearing device users |
| NEU | Neurological / ABI (NEU/PCS) |
| DEM | Dementia |
| NDV | Neurodivergence (NDV/AUT, NDV/ADHD, NDV/SENS) |
| NDV/MH | Mental health / PTSD / trauma |
| PAIN | Chronic pain / fibromyalgia |
| DBL | DeafBlind |
| OFS | Orthostatic & fatigue spectrum (OFS/ME, OFS/POTS, OFS/MCAS) |
| ALL | All disability categories |

**BAR relocated** — large body size provisions are in Supplementary Volume §IV. BAR is a cross-reference code only; not a disability taxonomy code; never appears in Volume 2. Any BAR-coded item in Volume 2 is an error.

**Supplementary volume codes** (not main taxonomy): CHD (CHD/INF, CHD/PRE, CHD/ESA, CHD/MCA, CHD/ADO) · LPA (LPA/ACH, LPA/PSS, LPA/MOB, LPA/JT) · EXH (EXH/ACR, EXH/GIG, EXH/TAL, EXH/MOB)

**VIS/vis ≠ VIS/DEAF ≠ DBL** — three populations, minimal technical overlap. Never conflate.

---

## Three-Tier Design Hierarchy

DAR (Design for Adaptable Readiness) mandatory at every tier.

| Tier | Standard | Context | Specification form |
|---|---|---|---|
| **Tier 0** | Universal Design — Improvable Floor | No predominant disability population. UD is the floor. | Above code minimum; designed to allow future tailoring. |
| **Tier 1** | Population-Informed Inclusive Design | Identified disability population(s). This guidebook's primary domain. | Ranges. Median is the population-informed default. |
| **Tier 2** | Person-Specific Co-Design | Identified individual. OT establishes functional capacity. | Co-designed. Resolves a specific value within the Tier 1 range. |

**Specification Range Doctrine:** Ranges are not uncertainty — they are the mechanism bridging Tier 1 and Tier 2. At Tier 1: use median. At Tier 2: resolve through co-design.

---

## Standing Rules

### 1. Pre-Flight Check
`workplan-orchestrator` issues Pre-Flight before any multi-step task. Stop and wait for confirmation.
**Skip conditions** (all must be met): valid YAML resumption block, OR task is single-step, OR user includes "fast-track" or "go".

### 2. Document Processing
Never process any document >500 lines as a single input. Run `haiku-chunker` first. Primary document is ~17,900 lines — always chunk before analysis. Section maps saved to `references/section-map_[DOC-ID].md`; reuse until version changes.

### 3. Model Selection

| Task type | Model |
|---|---|
| Structural extraction, pattern matching, section mapping, code extraction, heading correction | Haiku 4.5 |
| Judgment, synthesis, writing, clinical assessment, framing, evidence stratification | Sonnet 4.6 |

### 4. Output Formats

| Output type | Format |
|---|---|
| Inter-agent state, session handoffs | YAML |
| Human-readable final outputs | Markdown (.md) |
| Word documents | .docx — only if explicitly requested |
| Intermediate working documents | Lightweight, minimal formatting |

**All timestamps: `YYYY-MM-DD HH:MM`. No date-only timestamps anywhere.**

### 5. Source Verification
- All sources confirmed real before inclusion. "I don't know" preferred over invention.
- Unverified claims → `[UNVERIFIED — DOI/URL required before publication]`
- Do not silently remove unverified claims — flag them.
- `citation-verifier` defaults to PROVISIONAL mode.

### 6. Session Continuity
- `workplan-orchestrator` Session Start Protocol runs on every new conversation (§Session Start above).
- Never re-run a completed stage. Consume existing outputs.
- Context limit approaching → complete current stage, invoke `session-consolidator`, instruct user to start new chat.
- Stage checkpoints: 1–2 lines only.

### 7. Connector Activation
Activate PubMed, Consensus, Scholar Gateway only when a task explicitly requires research or citation verification. Not for planning, pre-flight, or structural analysis.

### 8. Token Efficiency
- Analyse size/breadth/depth before beginning. Break into staged workplan.
- L2 and L4 agents run in parallel — do not chain within a level.
- Reuse existing outputs. Never regenerate a completed stage.
- Upstream inputs to `critique-report-writer`: summarise to key findings if >2,000 words.
- `multilingual-research`: call `research-log-manager CHECK` before / `LOG` after. Skipping either is an error.
- Checkpoints: 1–2 lines. No prose narration of intermediate steps.
- Intermediate outputs: YAML or compact tables.

### 9. Risk Escalation
After each analysis level: tally escalation signals (→ `references/project-standards.md`). ≥2 signals → append REVIEW item to `gap_register.md` on GitHub.

### 10. Skill Selection
Before any repetitive operation, survey existing skills. If no relevant skill exists and task would recur, prompt user to build one first.

### 11. Prose Register
- **Voice:** soft imperative subjunctive — "to be", "not to exceed", "to provide"
- **Headings:** descriptive only — no values, ranges, or thresholds
- **Sequencing:** Ideal → Best Practice → Acceptable → Minimum
- **Concision:** ≤25 words per specification sentence; one claim per sentence
- **Evidentiary:** every prescriptive claim carries a citation or evidence tier marker, or is flagged `[UNSUPPORTED — citation required]`

Run `prose-style-checker` after `framing-checker`, before `critique-report-writer` and `item-specification-writer` packaging.

### 12. Research Log (mandatory)
Before any `multilingual-research` run: call `research-log-manager CHECK`. After: call `research-log-manager LOG`. Staleness threshold: 90 days.

---

## Skill Design Principles

1. No file names in skill body. File references belong in session-log YAML or workplan.
2. No completed-task references. Past decisions belong in `project-standards.md` or `gap_register.md`.
3. No version-locked language. Use structural roles.
4. One skill, one process. Audit and correction are separate skills.
5. BAR is not a main-taxonomy code. No skill routes BAR items to Volume 2.
6. All timestamps: `YYYY-MM-DD HH:MM`.

---

## Self-Critique Rules
- Standard content: 2 passes. High-stakes content (framing, evidence, citations): 3 passes. Maximum: 5 passes.
- External tool grounding required after Pass 1.
- HIGH-confidence claims → assess twice with different framing. Divergence → `UNCERTAIN_REVIEW`.

---

## Unresolved Blockers

| Blocker | Status | Action |
|---|---|---|
| Full bibliography | NOT AVAILABLE | citation-verifier in provisional mode |
| Application volume full text | NOT AVAILABLE | volii-validator in provisional mode |
| Levine et al. (2023) incomplete | OPEN — P1-06 | Replaced with Levine et al. (2024) KITE/UHN — verify DOI |
| Appendix A Emergency Evacuation | OPEN — P1-01 | Author must supply before publication |
| EXH population — no OT built environment literature | OPEN — GAP-029 P2 | See gap register |

---

## Deferred Production Items
- 82× "Chapter C" → "Part VIII §8.4" (deferred — find-and-replace, manual review per instance)
- 12× "Part VIII (case studies)" → "Part IX" (deferred — find-and-replace)

---

## Skill Registry

**Architecture:** Skills are defined in Project Files (`/mnt/project/`). GitHub holds copies for version history only. Upload amended Project Files to replace old versions — do not rely on GitHub copies for execution.

`research-log-manager` is defined in the Skill Definitions section of this document; no separate Project File exists.

### Orchestration
| Skill | Model | Primary trigger |
|---|---|---|
| `workplan-orchestrator` | — | Any multi-step task; session start; planning |
| `session-consolidator` | Sonnet 4.6 | Session end; save progress; update project knowledge |

### Document Processing
| Skill | Model | Primary trigger |
|---|---|---|
| `haiku-chunker` | Haiku 4.5 | Full document >500 lines |
| `structure-auditor` | Haiku 4.5 | Heading hierarchy; nesting; section numbering |
| `markdown-formatter` | Haiku 4.5 | Fix heading levels; markdown consistency |
| `chunk-assembler` | Haiku/Sonnet | Combine chunks into master document |
| `find-and-replace` | Haiku/Sonnet | Bulk text substitution with classification and validation |
| `table-formatter` | Haiku 4.5 | Table repair; format standardisation |

### Content Analysis
| Skill | Model | Primary trigger |
|---|---|---|
| `guidebook-auditor` | Haiku (A/C/E) · Sonnet (B/D) | Format/consistency/structure checks |
| `content-gap-analyzer` | Sonnet 4.6 | Gap analysis; population coverage |
| `framing-checker` | Sonnet 4.6 | Language/framing; social model; CRPD alignment |
| `evidence-auditor` | Sonnet 4.6 | Evidence stratification; overclaiming check |
| `item-consolidation-analyzer` | Sonnet 4.6 | Merge/split items; item count rationalisation |
| `version-diff` | Sonnet 4.6 | Compare document versions; semantic changes |

### Writing and Specification
| Skill | Model | Primary trigger |
|---|---|---|
| `prose-style-checker` | Sonnet 4.6 | Style audit; register check; voice; concision |
| `item-specification-writer` | Sonnet 4.6 | Item drafting; specification writing; revision |
| `practice-note-generator` | Sonnet 4.6 | Practitioner field tools; OT reference material |

### Research and Verification
| Skill | Model | Primary trigger |
|---|---|---|
| `citation-verifier` | Sonnet 4.6 | Citation audit; hallucination screen |
| `multilingual-research` | Sonnet 4.6 + web | 14-language search; always CHECK before / LOG after |
| `research-log-manager` | Sonnet 4.6 | Search coverage log; BPC; CHECK before / LOG after every `multilingual-research` run. **Defined in this document only.** |
| `literature-review-planner` | Sonnet 4.6 + web | Systematic review protocol; PRISMA alignment |
| `economics-researcher` | Sonnet 4.6 + web | Cost data; grant programmes; ROI evidence |
| `jurisdiction-tracker` | Sonnet 4.6 + web | Standards currency; jurisdiction-specific updates |

### Reference Management
| Skill | Model | Primary trigger |
|---|---|---|
| `cross-reference-resolver` | Haiku/Sonnet | Broken/stale internal cross-references |
| `volii-validator` | Haiku/Sonnet | Item code validation against application volume |
| `supplemental-integrator` | Haiku/Sonnet | Integrate new supplementary population volumes |

### Reporting
| Skill | Model | Primary trigger |
|---|---|---|
| `critique-report-writer` | Sonnet 4.6 | Formal critique output; review reports |

**Retired:** `vol1-corrections-writer` · `vol2-revision`

---

## Workflow Reference

| Workflow | Skill sequence |
|---|---|
| **Full Section Review** | haiku-chunker → [structure-auditor · markdown-formatter · guidebook-auditor · content-gap-analyzer · framing-checker · evidence-auditor] → [research-log-manager CHECK · multilingual-research · citation-verifier · research-log-manager LOG] → [guidebook-auditor C · volii-validator · cross-reference-resolver] → prose-style-checker → critique-report-writer |
| **Item Specification** | item-consolidation-analyzer → item-specification-writer → [framing-checker · evidence-auditor] → prose-style-checker → volii-validator |
| **Structural Change** | structure-auditor → markdown-formatter → cross-reference-resolver → find-and-replace → guidebook-auditor A |
| **Bulk Text Change** | find-and-replace (all stages) |
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

L2 and L4 skills in Full Section Review run in parallel. No skill takes another L2/L4 skill's output as input within the same level.

---

## Session-Close YAML Schema

```yaml
session_close: YYYY-MM-DD HH:MM
document: "[DOC-ID]"
skills_run: []
gaps_added: []
gaps_resolved: []
escalations_triggered: 0
patterns_noted: []
rules_added: []
blockers: []
research_log_updated: true|false
next_action:
  skill: name
  input_file: filename
  parameters: {}
```

---

## Persistent Storage Schema

**GitHub files:** see §State Files above.
**Key format (legacy reference):** `guidebook:{type}:{id}`
Types: `gaps` · `citations` · `volii` · `standards` · `sections` · `search-log` · `bpc`

---

---

# Skill Definitions
## Canonical versions — govern where they conflict with /mnt/project/ file versions

---

## multilingual-research

**Intake:** Focused query required. Ambiguous scope → ask one clarifying question before proceeding.
**Model:** Sonnet 4.6 with web search.
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API
**Every source confirmed real before inclusion. Flag grey literature. Flag thin base (<3 studies). "I don't know" → gap list.**

### Pre-Flight: Search Log Check
Before beginning any search, call `research-log-manager CHECK`:
1. Normalise query to slug: lowercase, spaces→hyphens, `|<population-code>`.
2. If COMPLETE and <90 days → load sources → skip to Synthesize.
3. If PARTIAL → search missing languages only → update log.
4. If STALE → re-run full search.
5. NOT FOUND → proceed to Step 1.

### Step 1 — Query Generation
Generate English query + native-language queries for all 14 languages. Identify relevant source types per language matrix.

### Step 2 — Academic Databases (English only)
Search PubMed (clinical/OT), Consensus (cross-discipline), Scholar Gateway (built environment). Tag `[DB: PubMed|Consensus|SG][LANG: EN]`.

### Step 3 — Web Search by Language

**Core languages — all 9 must be searched before early-close gate:**

| Language | Primary sources |
|---|---|
| English | ADA, Australian Standards, ISO, WHO, NICE, AOTA, CAOT |
| Swedish | BFS/BBR, Boverket, Scandinavian J Occupational Therapy |
| Norwegian | TEK17, Statsbygg, SINTEF, Ergoterapeutene |
| Danish | DS/SBi, Bygningsreglementet (BR18), Servicestyrelsen |
| Finnish | Accessibility Decree 241/2017, THL, STAKES, Valteri |
| French | CEREMA, ANPIHM, OPHQ (Quebec), Ergothérapie France |
| German | DIN 18040, BMAS, Bundesfachstelle Barrierefreiheit |
| Chinese | GB 50763, JGJ 50, MCA China, HK BD Code of Practice |
| Japanese | MLIT barrier-free law, DINF Japan, National Institute on Disability |

**Early-close gate:** After all 9 core languages searched — if ≥8 confirmed Tier 1–2 sources: close run. Record extended languages as `NOT-RUN`. If <8: proceed to extended languages.

**Extended languages (only if early-close gate does not trigger):**

| Language | Primary sources |
|---|---|
| Dutch | NEN, BNA, Ergotherapie Nederland |
| Spanish | ONCE, CONADIS (MX/AR/CO), IMSERSO |
| Portuguese | NBR 9050 (BR), DL 163/2006 (PT) |
| Korean | Welfare Facilities Standard, KODDI |
| Italian | DM 236/89, Linee guida CNAPPC |

### Step 4 — Translation and Tagging
Translate non-English findings. Tag `[LANG: XX][TRANSLATED]`. Flag untranslatable concepts with parenthetical explanation.

### Step 5 — Cross-Language Evaluation
Cluster semantically equivalent findings. Flag divergent conclusions (κ ≈ 0.30 — surface all divergence, suppress nothing).

### Step 6 — Synthesize

**Consensus findings** (≥2 independent sources, cross-language consistent): `Finding | Sources | Tier`
**Language-divergent findings:** `Topic | Lang A finding | Lang B finding`
**Emerging/single-source:** `Finding | Source | Lang` (flag as preliminary)
**Evidence gaps:** `Gap | Languages searched | Search terms`
**Source list:** `# | Authors | Year | Title | Journal | Lang | Tier | DOI`

### Post-Run: Log Updates (mandatory)
Call `research-log-manager LOG`. Skipping is an error.

### Evidence Hierarchy

| Tier | Type |
|---|---|
| 1 | Systematic review or meta-analysis |
| 2 | RCT or controlled study |
| 3 | Cohort, cross-sectional, or case-control study |
| 4 | Expert consensus, clinical guideline, professional standard |
| 5 | Grey literature, regulatory document, single case report |

Lived experience evidence is co-primary at Tier 3–4 where no clinical trial is feasible.

### Token Efficiency
- Batch web searches by language family (Nordic · Romance · Asian).
- Return ≤20 sources total; prioritise by tier then cross-language diversity.
- NO-DATA or THIN after one genuine attempt: log and move on.

---

## research-log-manager
**Defined in this document only. No /mnt/project/ file. Call by name; execute inline.**
**Model:** Sonnet 4.6
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API
**Files managed:** `references/search-log.md` · `references/best-practices-compendium.md`

### Actions

**CHECK**
1. Normalise slug: lowercase, spaces→hyphens, `|<population-code>`.
2. GET `references/search-log.md`. Parse. Find matching slug.
3. Return: **COMPLETE** (all 9 core languages SEARCHED, <90 days → provide source IDs + BPC slug; call RETRIEVE inline) · **PARTIAL** (list NOT-SEARCHED languages) · **STALE** (>90 days) · **NOT FOUND**.
4. If PARTIAL/STALE/NOT FOUND: proceed to `multilingual-research`.

**LOG**
Triggered after every `multilingual-research` run. Do not skip.
1. Normalise slug.
2. GET `references/search-log.md` + SHA. Locate or append slug entry. Write entry per schema. PUT back.
3. GET `references/best-practices-compendium.md` + SHA. Locate or append `## {slug}`. Write entry per schema. PUT back.
4. Confirm: `✓ Logged: {slug}`

**RETRIEVE**
1. Normalise slug.
2. GET `references/best-practices-compendium.md`. Locate `## {slug}`. Return inline.
3. If not found: `NOT FOUND — run multilingual-research for this slug.`

### Search Log Entry Schema

```yaml
slug: grab-bar-height|MOB
query: "grab bar height mobility impairment accessibility"
last_searched: YYYY-MM-DD HH:MM
early_close_triggered: false
languages:
  EN: {status: SEARCHED, results: 12, db: [PubMed, Consensus, SG, web]}
  SV: {status: SEARCHED, results: 6, db: [web]}
  NO: {status: SEARCHED, results: 3, db: [web]}
  DA: {status: SEARCHED, results: 3, db: [web]}
  FI: {status: SEARCHED, results: 2, db: [web]}
  FR: {status: SEARCHED, results: 4, db: [web]}
  DE: {status: SEARCHED, results: 5, db: [web]}
  ZH: {status: THIN, results: 1, db: [web], note: "GB 50763 only"}
  JA: {status: SEARCHED, results: 4, db: [web]}
  NL: {status: NOT-RUN, results: 0, db: [], note: "early-close gate triggered"}
  ES: {status: NOT-RUN, results: 0, db: [], note: "early-close gate triggered"}
  PT: {status: NOT-RUN, results: 0, db: [], note: "early-close gate triggered"}
  KO: {status: NOT-RUN, results: 0, db: [], note: "early-close gate triggered"}
  IT: {status: NOT-RUN, results: 0, db: [], note: "early-close gate triggered"}
top_sources: [REF-042, REF-088, REF-091, REF-107]
bpc_ref: "grab-bar-height|MOB"
thin_flags: [ZH]
no_data_flags: []
```

**Status values:** `SEARCHED` · `THIN` · `NO-DATA` · `NOT-RUN` (early-close gate) · `NOT-SEARCHED` (PARTIAL returns only)

### BPC Entry Schema

```markdown
## grab-bar-height|MOB
**Updated:** YYYY-MM-DD HH:MM  **Evidence tier:** 1–2
**Consensus finding:** [one sentence]
**Range:** [values] (Tier 1 median: [value])
**Jurisdictions confirmed:** [list]
**Early-close:** yes/no  **Thin/No-data:** [list with reason]
**Key sources:** [REF-IDs]
**Divergent findings:** [jurisdiction · standard · value, or —]
```

### Staleness Rule
Entries >90 days → STALE on CHECK. Re-run `multilingual-research` for any STALE entry in an active section.

### Scope Gate Inference
3+ independent searches returning `NO-DATA` for the same language across different topics → append P3 item to `gap_register.md`:
`SCOPE-GATE-CANDIDATE | Lang: XX | Evidence: N/N NO-DATA | Recommend: move to extended set`
Never permanently exclude a language.

---

## workplan-orchestrator

**On session start:** run Session Start Protocol (§Session Start in Project Instructions).

### Task Intake
1. Session Start Protocol complete → proceed.
2. New task: identify scope + goal → select workflow → confirm in ≤3 lines → execute.
3. Resumed task: confirm next action from YAML → execute from that stage.

### Workflows → Workflow Reference table in Project Instructions

### Gap Register — Write Protocol
When any skill produces a gap item:
1. GET `gap_register.md` + SHA.
2. Append: `GAP-XXX | P{1|2|3} | OPEN | {skill} | {section} | {description} | {YYYY-MM-DD HH:MM}`
3. PUT back. Commit: `workplan-orchestrator: append GAP-XXX [{YYYY-MM-DD HH:MM}]`
Never overwrite CLOSED items.

### Risk Escalation
After each analysis level: tally escalation signals. ≥2 → append REVIEW item to `gap_register.md`.

### Token Rules
Never re-run a completed stage. Checkpoint per stage: 1–2 lines. Context limit approaching → complete stage, invoke `session-consolidator`, instruct new chat. All timestamps: `YYYY-MM-DD HH:MM`.

---

## session-consolidator

**Model:** Sonnet 4.6
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API
**All timestamps: `YYYY-MM-DD HH:MM`**

### Steps

1. **Review session:** skills run · GAP-XXX items added/resolved · escalations · blockers · skill anomalies · research-log-manager LOG calls completed or missed.

2. **Extract patterns:** failing sources · recurring framing flags · skill failure modes · cross-section evidence gaps · languages consistently NO-DATA/THIN.

3. **Write rules to GitHub:** for each specific, actionable, recurring pattern:
   - GET `references/project-standards.md` + SHA.
   - Append: `RULE: {description}  CONDITION: {when}  ACTION: {what}  DATE: YYYY-MM-DD HH:MM`
   - PUT back. Commit: `session-consolidator: append rule [{YYYY-MM-DD HH:MM}]`

4. **Research log hygiene:** if `multilingual-research` ran and LOG was not called → flag as BLOCKER in YAML.

5. **Write session close to GitHub:**
   - GET `session_log.md` + SHA.
   - Append YAML block (never overwrite existing entries):
   ```yaml
   ---
   session_close: YYYY-MM-DD HH:MM
   document: "[DOC-ID]"
   skills_run: []
   gaps_added: []
   gaps_resolved: []
   escalations_triggered: 0
   patterns_noted: []
   rules_added: []
   blockers: []
   research_log_updated: true|false
   next_action:
     skill: name
     input_file: filename
     parameters: {}
   ```
   - PUT back. Commit: `session-consolidator: append session close [{YYYY-MM-DD HH:MM}]`

6. **Report to user (≤5 lines):** accomplishments · gaps added/resolved · next action · rules added · GitHub write status (✓ / ⚠ fallback).

**Fallback:** if PUT fails after one retry — output YAML block and rules text as fenced code blocks. Instruct user to paste manually. Never silently drop state.
