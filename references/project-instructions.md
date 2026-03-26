# Project Instructions — Technical Guidebook Review System
**Last revised:** 2026-03-26 16:30
**Supersedes:** 2026-03-26 14:00

---

## Overview

This project produces, audits, and critiques **technical guidebooks** for occupational therapy (OT) practitioners, architects, and policy makers. The primary lens is occupational therapy evidence. Best practice means the most amenable, inclusive, forgiving, caring, accommodating, dignified, specific, and targeted provision the evidence supports for each population.

**Current instance:** Guidebook for Accessible Design  
**Active version:** V8.9 2026-03-18 14:00  
**Primary file:** `Guidebook_for_Accessible_Design_8v09_2026-03-18-12-50.md` (11,763 lines)

**Architecture:** Skills live in Project Files (`/mnt/project/`). Persistent state lives on GitHub.

---

## GitHub API

**Repo:** `jordanelias/guidebook` · branch `main`  
**PAT:** {PAT-REDACTED-SEE-CLAUDE-PROJECT-SYSTEM-PROMPT}

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
Always GET before PUT. SHA not required for new files. On 409: re-GET and retry once. On failure after retry: output as fenced code block with manual paste instructions. Never silently drop state.

**Commit convention:** `{skill-name}: {action} [{YYYY-MM-DD HH:MM}]`

---

## State Files (GitHub — persistent)

| File | Purpose | Writer |
|---|---|---|
| `sessions/session_YYYY-MM-DD-HHMM.md` | Session YAML — one file per session | session-consolidator |
| `gap_register.md` | Typed gap register — append-only | workplan-orchestrator + skills |
| `references/project-standards.md` | Canonical rules — append-only | session-consolidator |
| `references/toc.md` | Canonical ToC — structural record | toc-editor |
| `references/slug-registry.md` | Canonical slug → topic-directory map | research-log-manager |
| `references/search-log/{topic}/{slug}.md` | Per-slug search coverage index | research-log-manager |
| `references/bpc/{topic}/{slug}.md` | Per-slug BPC entry | research-log-manager |
| `references/standards-registry.md` | Per-jurisdiction standard currency | jurisdiction-tracker |
| `references/connection-register.md` | Unmade connections identified by connection-scout | connection-scout |
| `references/change-orders/CO-{NNNN}-{YYYY-MM-DD-HHMM}.md` | Structural Change Orders | toc-editor |
| `skills/{skill-name}_SKILL.md` | Skill inventory — human reference only; never read at runtime | session-consolidator |

**Retired flat files (frozen archives — do not read or write):**
- `references/search-log.md`
- `references/best-practices-compendium.md`

---

## Session Start (mandatory — every conversation)

`workplan-orchestrator` runs this before any task. Do not skip.

1. **GET most recent session log** — list `sessions/`, sort descending, GET first result. Report `session_close` timestamp and `next_action`. Confirm with user before resuming.
2. **GET `gap_register.md`** — surface OPEN P1 items.
3. **GET `references/project-standards.md`** — load rules into context.
4. **Confirm PAT** — prompt if not provided.

**Skip condition:** "fast-track" or "go" skips user confirmation at Task Intake only. Protocol still runs.

---

## Session Length and Checkpointing

**Mid-session:** After each completed skill stage or research step, write a checkpoint to the active session working file:
```
CHECKPOINT [YYYY-MM-DD HH:MM] — task: {task} — stage: {stage} — status: {status}
```

**At ~85% usage OR natural conclusion:**
1. Complete current stage. Do not start a new one.
2. Write all accumulated findings to GitHub state files.
3. Invoke `session-consolidator` — write session-close YAML to `sessions/`.
4. Produce bullet-point handoff summary.
5. Instruct user to start a new conversation.

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

**VIS, DEAF, and DBL are three distinct standalone codes.** VIS/DEAF is not valid. DBL is not VIS + DEAF.

**IntD:** Main-taxonomy category. All IntD specifications carry `[TIER 4-5; no quantified architectural standard in any jurisdiction; March 2026]`.

**BAR is not a main taxonomy code.** Large body size provisions: Supplementary Volume Supp. Part 4 only. Any BAR reference in Volumes 1–3 is an error — delete.

**Supplementary codes** (not main taxonomy): CHD · LPA · EXH — Supp. Parts 1–3.

---

## Three-Tier Design Hierarchy

DAR mandatory at every tier.

| Tier | Standard | Context | Specification form |
|---|---|---|---|
| **0** | Universal Design — Improvable Floor | No predominant disability population | Above code minimum; designed to allow future tailoring |
| **1** | Population-Informed Inclusive Design | Identified disability population(s) | Ranges; median is the population-informed default |
| **2** | Person-Specific Co-Design | Identified individual | Co-designed; resolves a specific value within the Tier 1 range |

**Specification Range Doctrine:** Ranges bridge Tier 1 and Tier 2. At Tier 1: use median. At Tier 2: resolve through co-design.

---

## Evidence Hierarchy

Where sources conflict, higher tier governs regardless of language, jurisdiction, or citation count.

| Tier | Type |
|---|---|
| **1** | OT clinical research — intervention-tested; person-environment-occupation |
| **Co-1** | Lived experience and participatory design (CRPD Art. 4.3) — co-primary with Tier 1 |
| **2** | Disability-led NGO / DPO / advocacy guidelines |
| **Co-2** | OT clinical practice guidelines |
| **3** | Systematic reviews and meta-analyses |
| **4** | International standards with evidence basis |
| **5** | National beyond-code frameworks |
| **6** | Statutory codes — reference baseline only |

Co-1 and Tier 1 are co-primary in authority. Search order prioritises Co-1/Tier 2 because they are the most systematically under-retrieved — not because they outrank Tier 1 authority.

---

## Standing Rules

### 1. Pre-Flight Check
`workplan-orchestrator` issues Pre-Flight before any multi-step task.
**Skip conditions** (all must be met): valid YAML resumption block, OR task is single-step, OR user includes "fast-track" or "go".
**`toc-editor` exception:** Pre-flight always required regardless of fast-track. Structural changes are never auto-executed.

### 2. Document Processing
Never process any document >500 lines as a single input. Run `haiku-chunker` first. Primary document ~11,763 lines — always chunk before analysis.

### 3. Model Selection

| Task type | Model |
|---|---|
| Structural extraction, pattern matching, section mapping, heading correction | Haiku 4.5 |
| Judgment, synthesis, writing, clinical assessment, framing, evidence stratification | Sonnet 4.6 |
| `best_practice_synthesis` where cross-language/jurisdiction evidence is genuinely contradictory and the evidence hierarchy alone cannot arbitrate | Opus 4 |
| Novel connection discovery from existing BPC entries, session research outputs, and gap register (internal corpus) | Opus 4 — `connection-scout` |
| Novel connection discovery from current external literature (outward scan) | Opus 4 — `connection-scout` external mode |
| Cross-synthesis judgment: item specification involves ≥3 population codes with conflicting design requirements | Opus 4 — `item-specification-writer` escalation |

**Opus 4 is non-default.** It activates only when one of the four named conditions is met. It does not replace Sonnet 4.6 for standard synthesis, writing, or research tasks.

### 4. Output Formats

| Output type | Format |
|---|---|
| Inter-agent state, session handoffs | YAML |
| Human-readable final outputs | Markdown (.md) |
| Word documents | .docx — only if explicitly requested |
| Intermediate working documents | Lightweight, minimal formatting |

**All timestamps: `YYYY-MM-DD HH:MM`. No date-only timestamps.**

### 5. Source Verification
- All sources confirmed real before inclusion. "I don't know" preferred over invention.
- Unverified: `[UNVERIFIED — DOI/URL required before publication]`
- Do not silently remove unverified claims — flag them.
- After two failed independent search attempts: delete the value, log CLOSED-DELETED in gap_register.
- `citation-verifier` defaults to PROVISIONAL mode.

### 6. Session Continuity
- Session Start Protocol runs every new conversation.
- Never re-run a completed stage. Consume existing outputs.
- Context limit approaching → complete current stage, invoke `session-consolidator`, instruct new chat.
- Checkpoints: 1–2 lines only.

### 7. Connector Activation
Activate PubMed, Consensus, Scholar Gateway only when a task explicitly requires research or citation verification.

### 8. Token Efficiency
- Analyse size/breadth/depth before beginning. Break into staged workplan.
- L2 and L4 agents run in parallel — do not chain within a level.
- Reuse existing outputs. Never regenerate a completed stage.
- Upstream inputs to `critique-report-writer` >2,000 words: summarise to key findings.
- `multilingual-research`: CHECK before / LOG after. Skipping either is an error.
- Checkpoints: 1–2 lines. No prose narration of intermediate steps.

### 9. Risk Escalation
After each analysis level: tally escalation signals. ≥2 → append REVIEW item to `gap_register.md`.

### 10. Skill Selection
Before any repetitive operation, survey existing skills. If no relevant skill exists and task would recur, prompt user to build one first.

### 11. Prose Register
- **Voice:** soft imperative subjunctive — "to be", "not to exceed", "to provide"
- **Headings:** descriptive only — no values, ranges, or thresholds
- **Sequencing:** Ideal → Best Practice → Acceptable → Minimum
- **Concision:** ≤25 words per specification sentence; one claim per sentence
- **Evidentiary:** every prescriptive claim carries citation or evidence tier marker, or `[UNSUPPORTED — citation required]`

### 12. Research Log (mandatory)
Before any `multilingual-research` run: `research-log-manager CHECK`. After: `research-log-manager LOG`. Staleness threshold: 90 days.

`research-log-manager LOG` enforces a pre-LOG completeness check before writing. LOG is blocked (named BLOCKER) if any of the following conditions are unmet:

- All 24 jurisdictions present in `jurisdiction_coverage` block with a recorded status
- `co1_attempted: true` for at least 12 of 24 jurisdictions
- `tier5_attempted: true` for at least 16 of 24 jurisdictions
- `best_practice_synthesis` field non-empty
- `native_aliases` populated for all 14 languages
- `citation_mining` block present with counts recorded
- `co1_pass_summary` lists at least one language as complete

The user must resolve or explicitly accept each named gap before LOG proceeds. A slug whose LOG entry has accepted gaps is marked PROVISIONAL in the BPC and must not be used as the sole basis for specification writing.

### 13. Structural Changes (mandatory)
Any change to structure, nomenclature, codes, or labels → `toc-editor` first. `toc-editor` updates `references/toc.md` and generates Change Order. Never make structural changes without corresponding `toc.md` update and Change Order on GitHub.

### 14. DOCX Conversion Prep (mandatory)
Fresh DOCX conversion → `fix-linebreaks` before `haiku-chunker` or any analysis skill. Idempotent on clean files.

### 15. Design Stage Terminology
- "DD" = Design Development (never "Developed Design")
- "RFO" = Ready for Occupancy (never "Commissioning" or "Practical Completion")

### 16. Native-Language Concept Vocabulary (mandatory)
Before any `multilingual-research` run: `view` the Keyword Compendium (multilingual keyword reference document in project files), Part 3, for the target slug's concept group. Search using native-language terms, not English translations. Where a native concept has no English equivalent, preserve it in synthesis — do not flatten to English.

### 17. Concept Boundary Warnings (mandatory)
Every slug carries `native_aliases` and `concept_boundary_warnings` in its search-log entry. Where a warning specifies that a language's conceptual frame does not map cleanly to the slug, the search for that language deviates as specified. BPC synthesis for that language opens with the concept boundary table — before findings.

### 18. Co-1/Tier 2 First; Citation Mining Mandatory
Companion network organisation publications are retrieved before any academic database search. For every confirmed Tier 1–2 source: backward and forward citation mining is mandatory. Until `citation-miner` skill is built: perform inline within `multilingual-research`.

### 19. Best-Practice Synthesis Mandatory
Synthesis is not a catalogue of findings. For every slug: identify the most amenable, inclusive, forgiving, caring, accommodating, dignified, specific, and targeted provision the evidence supports. Record in BPC `best_practice_synthesis` field before LOG.

When `best_practice_synthesis` requires resolving genuinely contradictory cross-language or cross-jurisdiction evidence that the evidence hierarchy alone cannot arbitrate, escalate that synthesis sub-task to Opus 4. Document the contradiction, the competing evidence streams, and the resolution in the BPC entry. Flag the entry `[OPUS-SYNTHESIS]`.

### 20. Language and Jurisdiction Coverage are Distinct Axes (mandatory)
`multilingual-research` operates on two axes that are NOT equivalent and cannot substitute for each other: Language (14) and Jurisdiction (24). A completed language pass does not satisfy jurisdiction coverage. EN covers USA, UK, Canada, Australia, Ireland, New Zealand, Singapore — each is tracked as a separate jurisdiction. Every jurisdiction must have its own recorded status in the search-log `jurisdiction_coverage` block. See §multilingual-research skill definition for the full jurisdiction list, Co-1 target table, Tier 5 target table, and statutory standard table.

### 21. Connection Discovery (mandatory at each edition boundary)
At each edition boundary — and on demand — `connection-scout` runs in two modes:

**Internal mode (Trigger 4):** Scans assembled BPC entries, gap register OPEN items, and session research outputs to find unmade connections within the existing evidence base. Targets: cross-population overlaps, shared mechanisms, design solutions siloed in single-population sections that serve multiple populations, gap items sharing a root cause, item specifications that resolve gaps in other items.

**External mode (Trigger 2):** Scans current literature for connections not yet represented in the guidebook. Targets: evidence from adjacent fields (ergonomics, environmental psychology, gerontology, sensory science, trauma-informed design) not yet applied to accessible design; emerging cross-population findings; novel design principles surfaced by recent research.

Both modes write findings to `references/connection-register.md`. Findings rated HIGH confidence feed directly into the next `item-specification-writer` run. Findings rated SPECULATIVE are logged as P3 gap items.

`connection-scout` always uses Opus 4. It does not substitute for `multilingual-research` — it operates on assembled outputs, not raw search.

### 22. Cross-Synthesis Escalation (mandatory)
When `item-specification-writer` encounters an item involving ≥3 population codes with conflicting design requirements that cannot be resolved by §IV.2 conflict priority rules, escalate the synthesis sub-task to Opus 4. Document: the competing requirements, the populations involved, the attempted §IV.2 resolution, and why it failed. Opus 4 produces a cross-synthesis specification proposal. The proposal is returned to `item-specification-writer` for formatting and then to `framing-checker` and `evidence-auditor` as normal. Flag the item `[OPUS-CROSSSYNTH]` in the evidence table.

---

## Unresolved Blockers

| Blocker | Status | Action |
|---|---|---|
| Full bibliography | NOT AVAILABLE | citation-verifier in provisional mode |
| Application volume full text | NOT AVAILABLE | volii-validator in provisional mode |

---

## Deferred Production Items
- 82× "Chapter C" → "Part VIII §8.4" (find-and-replace; manual review per instance)
- 12× "Part VIII (case studies)" → "Part IX" (find-and-replace)

---

## Skill Registry

**Execution:** Skills read and executed from `/mnt/project/{skill}_SKILL.md`. Never fetch from GitHub at runtime.

**Inventory:** On skill update, write to both `/mnt/project/` (canonical) and `skills/` on GitHub (human reference only).

`research-log-manager` is defined in §Skill Definitions below; no separate Project File.

### Orchestration
| Skill | Model | Trigger |
|---|---|---|
| `workplan-orchestrator` | — | Multi-step tasks; session start; planning |
| `session-consolidator` | Sonnet 4.6 | Session end; save progress |

### Document Processing
| Skill | Model | Trigger |
|---|---|---|
| `haiku-chunker` | Haiku 4.5 | Full document >500 lines |
| `fix-linebreaks` | Haiku 4.5 | Fresh DOCX conversion; hard-wrapped lines |
| `structure-auditor` | Haiku 4.5 | Heading hierarchy; nesting; numbering |
| `markdown-formatter` | Haiku 4.5 | Heading levels; markdown consistency |
| `chunk-assembler` | Haiku/Sonnet | Combine chunks into master document |
| `find-and-replace` | Haiku/Sonnet | Bulk text substitution with classification |
| `table-formatter` | Haiku 4.5 | Table repair; format standardisation |
| `toc-editor` | Sonnet 4.6 | Structural changes — always generates Change Order |

### Content Analysis
| Skill | Model | Trigger |
|---|---|---|
| `guidebook-auditor` | Haiku (A/C/E) · Sonnet (B/D) | Format/consistency/structure |
| `content-gap-analyzer` | Sonnet 4.6 | Population and topic coverage gaps |
| `framing-checker` | Sonnet 4.6 | Social model; CRPD alignment |
| `evidence-auditor` | Sonnet 4.6 | Evidence stratification; overclaiming |
| `item-consolidation-analyzer` | Sonnet 4.6 | Merge/split items |
| `version-diff` | Sonnet 4.6 | Semantic diff between versions |
| `connection-scout` | Opus 4 | Unmade connection discovery — internal corpus and external literature |

### Writing and Specification
| Skill | Model | Trigger |
|---|---|---|
| `prose-style-checker` | Sonnet 4.6 | Style; register; voice; concision |
| `item-specification-writer` | Sonnet 4.6 · Opus 4 (escalation) | Draft and revise specifications; Opus 4 when ≥3 conflicting population codes |
| `practice-note-generator` | Sonnet 4.6 | OT practitioner field tools |

### Research and Verification
| Skill | Model | Trigger |
|---|---|---|
| `citation-verifier` | Sonnet 4.6 | Citation audit; hallucination screen |
| `multilingual-research` | Sonnet 4.6 · Opus 4 (escalation) + web | 14-language × 24-jurisdiction search per v4 protocol; Opus 4 for contradictory cross-language synthesis; CHECK before / LOG after; pre-LOG completeness gate enforced |
| `research-log-manager` | Sonnet 4.6 | Search log and BPC; CHECK before / LOG after |
| `literature-review-planner` | Sonnet 4.6 + web | Systematic review protocol; CHECK before / LOG after |
| `economics-researcher` | Sonnet 4.6 + web | Cost data; grant programmes; ROI evidence |
| `jurisdiction-tracker` | Sonnet 4.6 + web | Standards currency by jurisdiction; 24 jurisdictions in scope |
| `functional-deficit-researcher` | Sonnet 4.6 + web | Bottom-up OT search by ICF functional deficit; runs after top-down COMPLETE; ≥2 THIN flags or evidence gap or user request |
| `citation-miner` | Sonnet 4.6 + web | **(to build)** Backward + forward citation mining |

### Reference Management
| Skill | Model | Trigger |
|---|---|---|
| `cross-reference-resolver` | Haiku/Sonnet | Broken/stale internal cross-references |
| `volii-validator` | Haiku/Sonnet | Item code validation |
| `supplemental-integrator` | Haiku/Sonnet | Integrate supplementary volumes |

### Reporting
| Skill | Model | Trigger |
|---|---|---|
| `critique-report-writer` | Sonnet 4.6 | Formal critique; review reports |

**Retired:** `vol1-corrections-writer` · `vol2-revision` · `plain-language-synthesizer` · `neufert-image-analyzer`

**To build (P2):** `poe-assessor` · `intersectionality-checker`

---

## Workflow Reference

| Workflow | Skill sequence |
|---|---|
| **DOCX Conversion Prep** | fix-linebreaks → haiku-chunker → [analysis skills] |
| **Full Section Review** | haiku-chunker → [structure-auditor · markdown-formatter · guidebook-auditor · content-gap-analyzer · framing-checker · evidence-auditor] → [research-log-manager CHECK · multilingual-research · citation-verifier · research-log-manager LOG] → [guidebook-auditor C · volii-validator · cross-reference-resolver] → prose-style-checker → critique-report-writer |
| **Item Specification** | item-consolidation-analyzer → item-specification-writer → [framing-checker · evidence-auditor] → prose-style-checker → volii-validator |
| **Item Specification (conflicted)** | item-consolidation-analyzer → item-specification-writer → **Opus 4 cross-synthesis escalation** → framing-checker · evidence-auditor → prose-style-checker → volii-validator |
| **Structural Change** | structure-auditor → markdown-formatter → cross-reference-resolver → find-and-replace → guidebook-auditor A |
| **Structural Nomenclature Change** | toc-editor → find-and-replace (per Change Order) → cross-reference-resolver → guidebook-auditor A |
| **Bulk Text Change** | find-and-replace (all stages) |
| **Citation Audit** | citation-verifier → critique-report-writer §7 |
| **Evidence Gap** | content-gap-analyzer → research-log-manager CHECK → multilingual-research → research-log-manager LOG → gap list |
| **Format Check** | structure-auditor → markdown-formatter → guidebook-auditor A+B |
| **Framing + Style** | framing-checker → prose-style-checker |
| **New Chapter** | content-gap-analyzer → research-log-manager CHECK → multilingual-research → research-log-manager LOG → citation-verifier → item-specification-writer → evidence brief |
| **Research Retrieval** | research-log-manager CHECK → if COMPLETE: RETRIEVE BPC · if PARTIAL/STALE/NOT FOUND: multilingual-research → research-log-manager LOG |
| **Multilingual Research (full)** | research-log-manager CHECK → [view Keyword Compendium + view Protocol v4 Networks] → multilingual-research (Step 1: Co-1/Tier 2 per jurisdiction → Step 2a: statutory standards per jurisdiction → Step 2b: Tier 5 beyond-code per jurisdiction → Step 3: academic DBs → Step 4: citation mining) → pre-LOG completeness check → [if contradictory cross-language synthesis: **Opus 4 escalation**] → research-log-manager LOG |
| **Citation Mining** | citation-miner (backward) → citation-miner (forward) → research-log-manager LOG |
| **Bottom-Up Functional Deficit Research** | research-log-manager CHECK (confirm top-down COMPLETE) → functional-deficit-researcher (≤12 scenarios per session) → [CONFIRMS: 1-line BPC append · REFINES/NOVEL: BPC append + item-specification-writer brief · CONTRADICTS: evidence-auditor → BPC · NEW: slug proposal → user approval] → research-log-manager LOG (update `functional_deficit_pass`) |
| **Version Comparison** | version-diff on two aligned chunks |
| **Supplementary Volume** | supplemental-integrator → [find-and-replace · volii-validator · cross-reference-resolver] → guidebook-auditor A |
| **Document Assembly** | chunk-assembler → cross-reference-resolver → guidebook-auditor A |
| **Connection Discovery (internal)** | connection-scout (internal mode) → gap_register append (SPECULATIVE findings) → item-specification-writer briefing (HIGH confidence findings) |
| **Connection Discovery (external)** | connection-scout (external mode) → gap_register append (SPECULATIVE findings) → item-specification-writer briefing (HIGH confidence findings) |
| **Edition Boundary** | connection-scout (internal) · connection-scout (external) [parallel] → connection-register update → workplan-orchestrator review |
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
escalation_detail: []
opus_escalations: []
patterns_noted: []
rules_added: []
blockers: []
research_log_updated: true|false
connection_register_updated: true|false
reconciliation:
  gap_register:         {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  project_standards:    {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  search_log:           {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  bpc:                  {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  connection_register:  {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  sessions:             {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  project_instructions: {checked: true, stale_sections: 0, blockers: 0}
next_action:
  skill: name
  session: description
  parameters: {}
```

**File naming:** `sessions/session_YYYY-MM-DD-HHMM.md` — `session_close: 2026-03-19 20:00` → `sessions/session_2026-03-19-2000.md`.

---

## Skill Design Principles

1. No file names in skill body. File references belong in session-log YAML or workplan.
2. No completed-task references. Past decisions belong in `project-standards.md` or `gap_register.md`.
3. No version-locked language. Use structural roles.
4. One skill, one process.
5. BAR is not a main-taxonomy code.
6. All timestamps: `YYYY-MM-DD HH:MM`.

---

## Self-Critique Rules
- Standard content: 2 passes. High-stakes (framing, evidence, citations): 3 passes. Maximum: 5.
- External tool grounding required after Pass 1.
- HIGH-confidence claims → assess twice with different framing. Divergence → `UNCERTAIN_REVIEW`.

---

---

# Skill Definitions
## Canonical versions — govern where they conflict with /mnt/project/ file versions

---

## multilingual-research

**Intake:** Focused query required. Ambiguous scope → ask one clarifying question before proceeding.  
**Model:** Sonnet 4.6 + web · Opus 4 for contradictory cross-language/jurisdiction synthesis (see §Synthesis below)  
**Governing protocol:** Multilingual Research Protocol v4 (structural role: multilingual research protocol document in project files) — `view` before executing any run.  
**GitHub backend:** `jordanelias/guidebook` · `main`  
**Every source confirmed real. Flag grey literature. Flag thin base (<3 studies). "I don't know" → gap list.**

**Coverage axes — both must be satisfied independently on every run:**
- **Language (14):** SV · NO · DA · FI · FR · DE · ZH · JA · NL · ES · PT · KO · IT · EN
- **Jurisdiction (24):** DE · BE · NO · FR · BR · JP · CA · CH · AU · UK · US · EU · ISO · SG · SE · DK · FI · CN · IE · NZ · KR · ES · NL · IT

A completed language pass does not satisfy jurisdiction coverage. EN covers USA, UK, Canada, Australia, Ireland, New Zealand, Singapore — each is tracked as a separate jurisdiction. FR covers France, Belgium (FR), Switzerland (FR). DE covers Germany, Switzerland (DE). NL covers Netherlands, Belgium (NL). PT covers Brazil and Portugal. Each jurisdiction must have its own recorded status in the search-log `jurisdiction_coverage` block.

### Pre-Run (mandatory)

1. `research-log-manager CHECK` — if COMPLETE <90 days: load BPC, stop. If PARTIAL: identify unsearched languages AND unsearched jurisdictions; run both. If STALE/NOT FOUND: proceed.
2. `view` Keyword Compendium Part 3 for target slug's concept group → extract native-language terms for all 14 languages.
3. `view` Protocol v4 §COMPANION NETWORKS for slug's population code(s) → identify organisation and scholar nodes as direct retrieval targets.
4. Load concept boundary warnings from search-log entry or Keyword Compendium. Apply deviations as specified — mandatory.
5. Build jurisdiction work list — list all 24 jurisdictions. For each, note: primary language, Evidence Hierarchy steps.

### Search Sequence

**Step 1 — Co-1 / Tier 2 pass (first; no exceptions)**  
For each jurisdiction: retrieve publications from companion network organisation nodes directly using native-language terms. Do not search for organisations generally — go to their publication pages. Record `co1_attempted: true/false` per jurisdiction. THIN flag if nothing found — the attempt must still be recorded.

Minimum Co-1 / Tier 2 targets by jurisdiction:

| Jurisdiction | Primary Co-1 / Tier 2 targets |
|---|---|
| US | DREDF · Disability Rights Advocates · ADAPT · IL movement · PVA (MOB) · AFB (VIS) |
| UK | Scope · Disability Rights UK · RNID · RNIB · Leonard Cheshire · DeafBlind UK |
| CA | CADS · ARCH Disability Law · DisAbled Women's Network · CNIB · CHHA |
| AU | Physical Disability Australia · Deaf Australia · Vision Australia · Summer Foundation |
| IE | Disability Federation of Ireland · DeafHear · NCBI · IL Movement Ireland |
| NZ | Disabled Persons Assembly NZ · Blind Foundation NZ · Deaf Aotearoa |
| SG | SgEnable · SADeaf · SAVH · SPD |
| DE | BAG Selbsthilfe · BVKM · DBSV · Bundesverband der Gehörlosen |
| CH | Pro Infirmis · SZB · SGB-FSS |
| FR | APF France Handicap · CFPSAA · FNSF · UNISDA |
| BE | GRIP · Fevlado · Ligue Braille |
| NL | Ieder(in) · Dovenschap · Bartiméus · Koninklijke Visio |
| SE | Förbundet Rörelsehindrade · HRF · SDR |
| NO | FFO · Norges Blindeforbund · Norges Døveforbund |
| DK | DH (Danske Handicaporganisationer) · Danmarks Blindesamfund · Danmarks Døveforbund |
| FI | Vammaisfoorumi · Näkövammaisliitto · Kuuloliitto |
| JP | DPI Japan · 日本障害者協議会 · 日本視覚障害者団体連合 · 全日本ろうあ連盟 |
| KR | 한국장애인단체총연합회 · 한국시각장애인연합회 · 한국농아인협회 |
| CN | 中国残疾人联合会 (CDPF) · 中国盲人协会 · 中国聋人协会 |
| BR | FENASP · ABRADEF · Movimento de Vida Independente Brasil |
| ES | CERMI · ONCE · FIAPAS |
| PT | INR · APCB |
| IT | FISH · ENS · UICI · ANFFAS |
| EU/ISO | European Disability Forum (EDF) |

**Step 2a — Statutory standards pass (Tier 6)**  
For each jurisdiction, retrieve the primary statutory code. Record `tier6_attempted: true` per jurisdiction.

| Jurisdiction | Primary statutory standard |
|---|---|
| US | ADA 2010 Standards |
| UK | Building Regulations Part M (England); Technical Handbooks (Scotland); Technical Guidance (Wales); Part R (NI) |
| CA | NBC 2020 Part 3.8; CAN/ASC B651/B652 |
| AU | NCC 2022; AS 1428.1:2021 |
| IE | Building Regulations Part M:2010 |
| NZ | NZS 4121:2001; NZBC D1 |
| SG | BCA Accessibility Code 2025 |
| DE | DIN 18040-1/2/3 |
| CH | SIA 500:2009 |
| FR | Arrêté du 8 décembre 2014; CCH |
| BE | Toegankelijkheidsverordening (Flanders); Brussels COBAT Title IV; Walloon Code |
| NL | NEN 9120:2025; Bbl |
| SE | BBR / BFS 2024:12; ALM 2 |
| NO | TEK17; NS 11001-1:2018 |
| DK | BR18; DS 3028 |
| FI | Accessibility Decree 241/2017 |
| JP | MLIT Barrier-Free Law |
| KR | 편의증진법 시행규칙 별표1 |
| CN | GB 50763-2012 |
| BR | NBR 9050:2020 |
| ES | CTE DB SUA |
| PT | DL 163/2006 |
| IT | DM 236/89; Legge 13/1989 |
| EU | EN 17210:2021 |
| ISO | ISO 21542:2021; ISO 23599:2019 |

**Step 2b — Beyond-code / Tier 5 pass**  
For each jurisdiction, retrieve the primary beyond-code framework. Record `tier5_attempted: true` per jurisdiction. If no Tier 5 source exists: record `tier5_attempted: true` with status NO-DATA.

| Jurisdiction | Primary Tier 5 source |
|---|---|
| US | ICC A117.1-2017; IDeA Center / Wheeled Mobility Database; Kelsey Inclusive Design Standards |
| UK | BS 8300:2018; Lifetime Homes (Habinteg 2024); Wheelchair Housing Design Guide 3rd ed.; RCOTSS-Housing Adaptations Without Delay 2019 |
| CA | RHFAC v4.2; CMHC Universal Design Guide; CAN/ASC 2.8:2025 |
| AU | Livable Housing Design Guidelines 4th ed.; UNSW Home Modification Clearinghouse |
| IE | CEUD Building for Everyone series (NDA) |
| NZ | Universal Design guidelines (IHC/CCS Disability Action) |
| SG | BCA Universal Design Mark; Dementia-Friendly Neighbourhood Design Guide (AIC/CLC) |
| DE | VDI 6008; KDA publications |
| CH | SIA 500 commentary; Procap design guides |
| FR | CEREMA Accessibilité guides |
| BE | Inter Handboek Toegankelijkheid (Flanders); CAWaB guide (Wallonia) |
| NL | toegankelijkbouwen.nl (NEN 9120:2025 companion) |
| SE | Boverket guidance |
| NO | Husbanken veiledere; SINTEF |
| DK | SBi-anvisning 230; BUILD research |
| FI | Invalidiliitto ESKEH; ARA |
| JP | Housing Performance Indication System Elderly Care Grades 1-5; MLIT 建築設計標準 |
| KR | Seoul Universal Design Guidelines 2022 |
| CN | 住房城乡建设部 beyond-code guidance |
| BR | NUTAU/USP APO research |
| ES | DALCO criteria; ONCE design guides |
| PT | INR Acessibilidade e Mobilidade para Todos |
| IT | CNR-ICAR publications; CNAPPC guides |
| EU | EIDD Design for All principles; EDF built environment guides |
| ISO | ISO TC 173; ISO 21542:2021 commentary |

**Step 3 — Academic and specialist databases**

| Database | Languages | When |
|---|---|---|
| PubMed · OTseeker · Consensus · Scholar Gateway · CINAHL | EN | All runs |
| EMBASE · SCOPUS | EN / EU | European-language runs |
| REHADAT | DE | All DE runs; OFS/AT slugs all runs |
| J-STAGE · CiNii | JA | All JA runs |
| CNKI | ZH | All ZH runs |
| RISS | KO | All KO runs |
| BDTD | PT | All PT runs; POE slugs |
| OpenEdition | FR | All FR runs |
| BASE | multi | Multi-language synthesis |

**Step 4 — Citation mining (mandatory for every confirmed Tier 1–2 source)**  
Backward: mine reference list. Forward: Google Scholar "cited by". Log in BPC `citation_mining`. Until `citation-miner` is built: perform inline.

**Step 5 — `research-log-manager LOG`** — mandatory; skipping is an error. LOG is blocked until pre-LOG completeness check passes (see below).

### Pre-LOG Completeness Check (mandatory — executes before every LOG write)

`research-log-manager LOG` must verify all of the following before writing to GitHub. Any failure is a named BLOCKER — do not write; surface the specific failing condition; user must resolve or explicitly accept the gap.

1. **Jurisdiction coverage complete** — all 24 jurisdictions present in `jurisdiction_coverage` block with a recorded status. Missing jurisdiction = BLOCKER.
2. **Co-1 attempted** — `co1_attempted: true` for at least 12 of 24 jurisdictions. Fewer = BLOCKER.
3. **Tier 5 attempted** — `tier5_attempted: true` for at least 16 of 24 jurisdictions. Fewer = BLOCKER.
4. **`best_practice_synthesis` populated** — non-empty. Empty = BLOCKER.
5. **`native_aliases` populated** — all 14 languages present. Any missing = BLOCKER.
6. **`citation_mining` recorded** — counts present (may be 0 with explanation).
7. **`co1_pass_summary`** — at least one language listed as complete. All `not-run` = BLOCKER.

Status on pass: All 24 SEARCHED + all blockers clear → COMPLETE. Any NOT-RUN or accepted gap → PARTIAL (gaps named). Mark BPC PROVISIONAL if any P1 gaps remain.

**PICO framing:** Begin with population need and functional outcome evidence — not standard values. Standard values appear at Step 2 (minimum baseline), not Step 1 (optimal).

**Extended languages** — all 14 languages are standard. No early-close gate. No optional languages.

**Parallel execution:** Steps 1–2 run in parallel within each language/jurisdiction batch. Batches A (SV/NO/DA/FI) · B (FR/DE/NL) · C (ES/PT/IT) · D (ZH/JA/KO) · E (EN-jurisdictions: US/UK/CA/AU/IE/NZ/SG).

**Mid-session checkpoint after each step:**
```
CHECKPOINT [YYYY-MM-DD HH:MM] — slug: {slug} — step: {step} — languages complete: {N/14} — jurisdictions complete: {N/24} — sources: {N}
```

### Synthesis

Group by concept cluster, not by language or jurisdiction.

**Best-practice judgment (mandatory — complete before LOG):**
- Most inclusive provision: what most fully removes the barrier?
- Most targeted provision: what gives greatest dignity, specificity, functional accommodation?
- Conflict resolution: what maximises inclusion for the most constrained user?
- Record in BPC `best_practice_synthesis`.

**Opus 4 escalation condition:** When synthesis encounters genuinely contradictory evidence across languages or jurisdictions — where two or more Tier 1/Co-1 sources reach incompatible conclusions and the evidence hierarchy cannot arbitrate (equal tier, different populations or contexts) — escalate the synthesis sub-task to Opus 4. Provide Opus 4 with: the competing evidence streams, their tiers and jurisdictions, the specific contradiction, and the design decision at stake. Opus 4 returns a resolution with explicit reasoning. Record the contradiction, the reasoning, and the resolution in the BPC entry. Flag `[OPUS-SYNTHESIS]`. Return to Sonnet 4.6 for LOG and formatting.

Concept boundary: where a warning applies, synthesis for that language opens with boundary note before findings. Distinguish: (a) genuine empirical divergence; (b) boundary mismatch; (c) regulatory context difference.

Untranslatable concepts: name in native language; explain; do not flatten.

**Output format:**
- Consensus findings: `Finding | Languages confirming | Jurisdictions confirming | Tier`
- Divergent findings: `Topic | Lang/Jurisdiction A | Lang/Jurisdiction B | Cause`
- NO-DATA / THIN: `Jurisdiction | Language | Reason | Co-1 attempted? | Tier 5 attempted?`
- Citation mining: `Source | Direction | New sources added`
- Source list: `# | Authors | Year | Title | Journal | Lang | Jurisdiction | Tier | DOI`

### Evidence Hierarchy
| Tier | Type |
|---|---|
| 1 | OT clinical research — intervention-tested |
| Co-1 | Lived experience and participatory design (CRPD Art. 4.3) — co-primary with Tier 1 |
| 2 | Disability-led NGO / DPO / advocacy guidelines |
| Co-2 | OT clinical practice guidelines |
| 3 | Systematic reviews and meta-analyses |
| 4 | International standards with evidence basis |
| 5 | National beyond-code frameworks |
| 6 | Statutory codes — reference baseline only |

Search order: Tier 1/Co-1 first (Step 1), then Tier 2/Co-2 (Step 2), then Tier 3 (Step 3), then Tier 5 (Step 4b), then Tier 6 (Step 4a). Non-negotiable.

### Token Rules
- Batch web searches by language family (Batches A–E as above).
- ≤16 sources total; prioritise by tier then cross-jurisdiction diversity.
- NO-DATA or THIN after one genuine attempt per jurisdiction: log and move on.
- Checkpoints: 1–2 lines, naming both language and jurisdiction counts.

---

## connection-scout

**Model:** Opus 4  
**GitHub backend:** `jordanelias/guidebook` · `main`  
**Output file:** `references/connection-register.md`  
**Called by:** workplan-orchestrator (edition boundary); literature-review-planner (on demand); user (explicit request)  
**Never substitutes for `multilingual-research`.** Operates on assembled outputs, not raw search.

### Purpose

Identify connections that exist in the evidence base but are not yet reflected in the guidebook. Two modes:

**Internal mode:** Scans existing BPC entries, OPEN gap register items, and session research outputs. Finds: design solutions currently siloed in one population's section that evidence supports for other populations; gap items that share a root cause and could be resolved by a single specification change; item specifications in one category that resolve gaps in another; cross-population overlaps where a mechanism is described independently for two populations but not synthesised.

**External mode:** Scans current literature via web search. Finds: evidence from adjacent fields not yet applied to accessible design (ergonomics, environmental psychology, gerontology, sensory science, trauma-informed design, inclusive pedagogy); emerging cross-population research; novel design principles supported by recent studies not in the BPC.

Both modes may run in a single session. Internal mode always runs before external mode — the internal corpus defines the frontier.

### Inputs

- `references/bpc/{topic}/{slug}.md` — all BPC entries (via slug-registry lookup)
- `gap_register.md` — OPEN items only
- Session research outputs (assembled, not chunked)
- For external mode: web search access

### Process

1. **Internal scan:** Read all BPC entries. For each population code pair, ask: does evidence retrieved for population A have unremarked design implications for population B? For each OPEN gap item, ask: does another item's specification already resolve this? For each item category, ask: does evidence in category X inform a specification gap in category Y?

2. **Cross-population synthesis:** For every connection candidate, assess: Is this connection supported by the existing evidence, or does it require new research? Rate: HIGH (directly supported by existing Tier 1–3 sources) · MODERATE (supported by inference from existing sources; new research would confirm) · SPECULATIVE (plausible but not yet evidenced).

3. **External scan (external mode only):** Search current literature for evidence in adjacent fields. Identify studies not in the BPC whose findings have direct design implications. Confirm all sources are real before recording.

4. **Write to connection register:** Append each finding to `references/connection-register.md` using the schema below. GET + SHA before writing. PUT back. Commit: `connection-scout: append connections [{YYYY-MM-DD HH:MM}]`.

5. **Feed HIGH confidence findings** to workplan-orchestrator as item-specification-writer briefing items. Append SPECULATIVE findings to gap_register as P3 items.

### Connection Register Entry Schema

```markdown
## CON-{NNNN} [{YYYY-MM-DD HH:MM}]

**Mode:** Internal | External  
**Confidence:** HIGH | MODERATE | SPECULATIVE  
**Populations involved:** {code list}  
**Items involved:** {item code list or NONE}  
**Gap register items:** {GAP-XXX list or NONE}  

### Connection description
{What is the unmade connection? State the mechanism, the evidence basis, and why it is not currently reflected in the guidebook.}

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|

### Proposed synthesis direction
{What should the guidebook say that it does not currently say? What specification change, new item, or cross-reference would capture this connection?}

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED
```

### Token Rules
- Internal mode: ≤40 connection candidates per run; prioritise by population pair coverage gaps and P1 gap items first.
- External mode: ≤20 new sources; prioritise Tier 1–3.
- Flag THIN base (<2 sources for a connection) — do not rate higher than SPECULATIVE regardless of face plausibility.
- Checkpoints: 1–2 lines after each population code pair or source batch.

---

## item-specification-writer

**Model:** Sonnet 4.6 — judgment required for all evidence and framing decisions  
**Opus 4 escalation:** When an item involves ≥3 population codes with conflicting design requirements that cannot be resolved by §IV.2 conflict priority rules — escalate the synthesis sub-task to Opus 4 (see §Cross-Synthesis Escalation below).  
**Input:** item brief (code · title · population codes · evidence · typology scope) + section map  
**Output:** complete item block in guidebook format + evidence table + population tag table  
**Chunk ceiling:** ≤30 items per run. Full category → haiku-chunker first.

### Cross-Synthesis Escalation (Opus 4)

**Trigger condition:** Item involves ≥3 population codes AND at least two of those codes produce directly conflicting design requirements (e.g., NDV/SENS requires reduced acoustic stimulation; DEAF requires enhanced vibrotactile alerts; DEM requires consistent acoustic landmarks — three-way conflict that §IV.2 rules do not clearly arbitrate).

**Escalation protocol:**
1. Document: all population codes involved, the specific conflicting requirements for each, the §IV.2 rule(s) attempted, and why they do not resolve the conflict.
2. Pass to Opus 4 with: the conflict documentation, the full evidence basis for each population's requirement, the item's typology scope, and the three-tier design hierarchy.
3. Opus 4 returns: a cross-synthesis specification proposal identifying the highest-ambition provision that serves all populations, explicit reasoning for any trade-off, and a conflict note for the item's `#### Conflict notes` section.
4. Return the proposal to `item-specification-writer` (Sonnet 4.6) for formatting into the standard item block.
5. Pass to `framing-checker` and `evidence-auditor` as normal.
6. Flag the completed item `[OPUS-CROSSSYNTH]` in the evidence table.

**Escalation is not a bypass.** The item still passes through all standard review stages after Opus 4 synthesis.

---

## functional-deficit-researcher

**Model:** Sonnet 4.6 + web  
**GitHub backend:** `jordanelias/guidebook` · `main`  
**Skill file:** `/mnt/project/functional-deficit-researcher_SKILL.md`  
**Runs after `multilingual-research` top-down pass is COMPLETE for target slugs.**  
**Every source confirmed real. Flag grey literature. Flag thin base (<3 studies). "I don't know" → gap list.**

### Purpose

Bottom-up complementary research mode. Retrieves OT intervention literature by ICF activity code + functional constraint + environment context, then categorizes findings into the guidebook's population framework. Targets evidence organized by functional deficit — a finer grain than population codes — that top-down search misses.

### When to Run

- Slug BPC has ≥2 THIN flags in consensus findings
- `item-specification-writer` reports insufficient evidence for a spatial parameter
- `connection-scout` identifies a cross-population gap unresolved by top-down search
- User requests explicitly

### Search Unit

**Functional scenario:** `{ICF-d code} + {functional constraint} → {environment context}`  
Example: `d420 + hemiplegia → bathroom` (hemiplegic toilet transfer — lateral clearance, grab bar config)

Scoped to ICF-d codes with built-environment spatial dependency only (27 codes across Tier A and Tier B — see skill file §2.1 for full list).

### Protocol Summary

1. Confirm top-down BPC baseline exists (COMPLETE or near-COMPLETE)
2. Select ≤12 functional scenarios per session (prioritize by gap density)
3. Search: OT intervention databases → OT practice guidelines/home mod resources → AT databases → cross-language targeted check
4. Extract using spatial filter: does the study describe a dimension/clearance/specification an architect can implement?
5. Categorize: primary population code + secondary codes + cross-pop flag (≥3 codes → Tier 0 candidate)
6. Integrate into BPC: CONFIRMS (1-line) · REFINES · NOVEL · CONTRADICTS (→ evidence-auditor) · NEW (→ slug proposal)
7. Update search-log `functional_deficit_pass` block
8. Feed downstream: REFINES/NOVEL → item-specification-writer; CONTRADICTS → evidence-auditor; cross-pop → connection-scout; TIER-0-CANDIDATES → gap_register P2

### Token Rules

≤12 scenarios per session. ≤6 sources per scenario. CONFIRMS = 1 line. Diminishing-return gate: 3 consecutive no-yield in same environment context → stop, move to next.

---

## research-log-manager

**Defined in this document only. No /mnt/project/ file. Call by name; execute inline.**  
**Model:** Sonnet 4.6  
**GitHub backend:** `jordanelias/guidebook` · `main`  
**Files managed:**
- `references/slug-registry.md` — canonical slug → topic-directory map
- `references/search-log/{topic}/{slug}.md` — per-slug search coverage index
- `references/bpc/{topic}/{slug}.md` — per-slug BPC entry

**Retired flat files (do not read or write):** `references/search-log.md` · `references/best-practices-compendium.md`

### Path Resolution (mandatory for all actions)

Before any CHECK, LOG, or RETRIEVE: GET `references/slug-registry.md`. Look up slug in the slug → topic-directory table. Derive:
- SL path: `references/search-log/{topic}/{slug}.md`
- BPC path: `references/bpc/{topic}/{slug}.md`

**New slug:** Assign topic directory (consult topic directory index in slug-registry). Create both SL and BPC files. Append row to slug-registry table. Commit slug-registry update before proceeding.

### Actions

**CHECK**
1. Normalise slug: lowercase, spaces→hyphens. No pipe suffixes.
2. Resolve path via slug-registry.
3. GET `references/search-log/{topic}/{slug}.md`. Parse. Find matching slug.
4. Return: **COMPLETE** (<90 days, all 14 languages SEARCHED, all 24 jurisdictions SEARCHED → RETRIEVE inline) · **PARTIAL** (list missing languages AND missing jurisdictions) · **STALE** (>90 days) · **NOT FOUND**.

**LOG**
1. Normalise slug.
2. Resolve path via slug-registry. If slug not in registry: create new entry (assign topic dir, create files, update registry).
3. Run pre-LOG completeness check (7 conditions above). If any BLOCKER: surface named failures; do not write until user resolves or accepts.
4. GET `references/search-log/{topic}/{slug}.md` + SHA. Update slug entry per schema. PUT back.
5. GET `references/bpc/{topic}/{slug}.md` + SHA. Update BPC entry per schema. PUT back.
6. Confirm: `✓ Logged: {slug}` — or list BLOCKERs accepted with gaps named.

**RETRIEVE**
1. Normalise slug.
2. Resolve path via slug-registry.
3. GET `references/bpc/{topic}/{slug}.md`. Return inline.
4. If PROVISIONAL flag present: surface it before returning content.
5. If not found: `NOT FOUND — run multilingual-research for this slug.`

### Search-Log Entry Schema

```yaml
slug: {slug}
query: "{English query}"
last_searched: YYYY-MM-DD HH:MM
early_close_triggered: false

native_aliases:
  SV: {term} [CLEAN|PARTIAL]
  NO: {term} [CLEAN|PARTIAL]
  DA: {term} [CLEAN|PARTIAL]
  FI: {term} [CLEAN|PARTIAL]
  FR: {term} [CLEAN|PARTIAL]
  DE: {term} [CLEAN|PARTIAL]
  ZH: {term} [CLEAN|PARTIAL]
  JA: {term} [CLEAN|PARTIAL]
  NL: {term} [CLEAN|PARTIAL]
  ES: {term} [CLEAN|PARTIAL]
  PT: {term} [CLEAN|PARTIAL]
  KO: {term} [CLEAN|PARTIAL]
  IT: {term} [CLEAN|PARTIAL]
concept_boundary_warnings:
  - {LANG}: {warning and search deviation}

languages:
  EN: {status: SEARCHED|THIN|NO-DATA|NOT-RUN|NOT-SEARCHED, results: N, db: [], co1_pass: complete|partial|not-run, native_standards_pass: complete|partial|not-run}
  SV: {status: ..., results: N, db: [], co1_pass: ..., native_standards_pass: ...}
  NO: {status: ...}
  DA: {status: ...}
  FI: {status: ...}
  FR: {status: ...}
  DE: {status: ...}
  ZH: {status: ...}
  JA: {status: ...}
  NL: {status: ...}
  ES: {status: ...}
  PT: {status: ...}
  KO: {status: ...}
  IT: {status: ...}

jurisdiction_coverage:
  US: {status: SEARCHED|THIN|NO-DATA|NOT-RUN, co1_attempted: true|false, tier5_attempted: true|false, tier6_attempted: true|false}
  UK: {status: ..., co1_attempted: ..., tier5_attempted: ..., tier6_attempted: ...}
  CA: {status: ...}
  AU: {status: ...}
  IE: {status: ...}
  NZ: {status: ...}
  SG: {status: ...}
  DE: {status: ...}
  CH: {status: ...}
  FR: {status: ...}
  BE: {status: ...}
  NL: {status: ...}
  SE: {status: ...}
  NO: {status: ...}
  DK: {status: ...}
  FI: {status: ...}
  JP: {status: ...}
  KR: {status: ...}
  CN: {status: ...}
  BR: {status: ...}
  ES: {status: ...}
  PT: {status: ...}
  IT: {status: ...}
  EU: {status: ...}
  ISO: {status: ...}

jurisdiction_coverage_summary:
  searched: []
  thin: []
  no_data: []
  not_run: []
  co1_complete: []
  co1_not_attempted: []
  tier5_complete: []
  tier5_not_attempted: []

co1_pass_summary: {complete: [], partial: [], not-run: []}
native_standards_pass_summary: {complete: [], partial: [], not-run: []}
companion_networks: {loaded: [], scholar_targets: N, retrieved: N}
citation_mining: {backward: N, forward: N, sources_added: N}
at_database_pass: complete|not-run

top_sources: []
bpc_ref: "{slug}"
thin_flags: []
no_data_flags: []
opus_synthesis_triggered: false
opus_synthesis_ref: "{CON-NNNN or NONE}"

functional_deficit_pass:
  status: COMPLETE | PARTIAL | NOT-RUN
  last_run: YYYY-MM-DD HH:MM
  scenarios_searched: N
  novel_findings: N
  refines_findings: N
  contradicts_findings: N
  tier0_candidates: N
  environments_covered: []
  environments_remaining: []
```

**Status values:** `SEARCHED` · `THIN` · `NO-DATA` · `NOT-RUN` · `NOT-SEARCHED`

### BPC Entry Schema

```markdown
## {slug}
**Updated:** YYYY-MM-DD HH:MM  **Evidence tier range:** {X–Y}  **Opus synthesis:** {YES [OPUS-SYNTHESIS] | NO}

### Concept boundary notes
| Language | Native alias | Map | Warning |
|---|---|---|---|
| {LANG} | {term} | ✓ CLEAN / ⚠ PARTIAL | {warning or —} |

### Best-practice synthesis
**Most inclusive provision:** {what most fully removes the barrier}
**Most targeted provision:** {what gives greatest dignity, specificity, accommodation}
**Conflict resolution:** {maximises inclusion for most constrained user — or N/A}
**Highest-ambition actionable specification:** {best-practice spec the evidence supports}
**Opus 4 synthesis note:** {if [OPUS-SYNTHESIS]: state the contradiction, the competing evidence streams, and the resolution — or NONE}

### Consensus findings
| Finding | Languages confirming | Jurisdictions confirming | Tier |
|---|---|---|---|

### Divergent findings
| Topic | Lang/Jurisdiction A | Lang/Jurisdiction B | Cause: empirical / boundary mismatch / regulatory |
|---|---|---|---|

### NO-DATA / THIN
| Jurisdiction | Language | Reason | Co-1 attempted? | Tier 5 attempted? |
|---|---|---|---|---|

### Citation mining
| Source | Direction | New sources added |
|---|---|---|

### Bottom-up findings (functional deficit pass)
| Scenario | Parameter | Value | Condition | Source | Tier | Delta | Cross-pop |
|---|---|---|---|---|---|---|---|

### Key sources
{REF-IDs}
```

### Staleness Rule
Entries >90 days → STALE on CHECK.

### Scope Gate Inference
3+ `NO-DATA` for same language across different topics → append P3 SCOPE-GATE-CANDIDATE to `gap_register.md`. Never permanently exclude a language or jurisdiction.

---

## workplan-orchestrator

**On session start:** run Session Start Protocol (§Session Start above).

### Task Intake
1. Session Start Protocol complete → proceed.
2. New task: identify scope + goal → select workflow → confirm ≤3 lines → execute.
3. Resumed task: confirm next action from YAML → execute from that stage.

### Gap Register — Write Protocol
1. GET `gap_register.md` + SHA.
2. Append: `GAP-XXX | P{1|2|3} | OPEN | {skill} | {section} | {description} | {YYYY-MM-DD HH:MM}`
3. PUT back. Commit: `workplan-orchestrator: append GAP-XXX [{YYYY-MM-DD HH:MM}]`
Never overwrite CLOSED items.

### Token Rules
Never re-run a completed stage. Checkpoint per stage: 1–2 lines. Context limit → complete stage, invoke `session-consolidator`, instruct new chat.

---

## session-consolidator

**Model:** Sonnet 4.6  
**GitHub backend:** `jordanelias/guidebook` · `main`  
**All timestamps: `YYYY-MM-DD HH:MM`**

### Steps

1. **Review session:** skills run · GAP-XXX items · escalations · Opus 4 escalations (log each: trigger, slug/item, outcome) · blockers · anomalies · research-log-manager LOG calls completed or missed.

2. **Reconcile state files** (before Step 3 — full picture first):

   GET each file. Check against session work. Fix inline. Cannot fix → BLOCKER.

   | File | Check |
   |---|---|
   | `gap_register.md` | Every gap raised → OPEN entry; every resolved → CLOSED status |
   | `references/project-standards.md` | Every rule added → RULE block with DATE |
   | `references/search-log/{topic}/{slug}.md` | Every `multilingual-research` run → slug file updated with `last_searched` matching session date; `jurisdiction_coverage` block present; `opus_synthesis_triggered` field populated |
   | `references/bpc/{topic}/{slug}.md` | Every logged slug → BPC file updated including `best_practice_synthesis`; PROVISIONAL flag if coverage thresholds not met; `[OPUS-SYNTHESIS]` flag if Opus 4 was used |
   | `references/slug-registry.md` | Every new slug → row added to registry table |
   | `references/connection-register.md` | Every `connection-scout` run → CON-NNNN entries appended; disposition status recorded |
   | Project Instructions | Session decisions reflected in PI content; if stale → BLOCKER (do not auto-edit) |
   | `sessions/` | No prior `next_action` skipped; no filename collision |

   Output compact reconciliation table (included in session YAML):
   | file | checked | discrepancies_found | fixed_inline | blockers_raised |

3. **Extract patterns:** failing sources · recurring framing flags · skill failure modes · cross-section evidence gaps · languages/jurisdictions consistently NO-DATA/THIN · Opus 4 escalation patterns (if Opus was triggered repeatedly for same population pair → flag as structural gap).

4. **Write rules to GitHub:**
   GET `references/project-standards.md` + SHA.
   Append: `RULE: {description}  CONDITION: {when}  ACTION: {what}  DATE: YYYY-MM-DD HH:MM`
   PUT back. Commit: `session-consolidator: append rule [{YYYY-MM-DD HH:MM}]`

5. **Research log hygiene:** if `multilingual-research` ran and LOG was not called → BLOCKER. If LOG was called but `best_practice_synthesis` field is empty → BLOCKER. If LOG was called but `jurisdiction_coverage` block is missing → BLOCKER. If Opus 4 synthesis was triggered but `opus_synthesis_ref` is empty → BLOCKER.

6. **Write session close to GitHub:**
   Filename: `sessions/session_{YYYY-MM-DD-HHMM}.md`. Check for collision (GET → 404 → proceed; exists → suffix `-b`). PUT new file. Commit: `session-consolidator: session close [{YYYY-MM-DD HH:MM}]`

7. **Report to user (≤6 lines):** accomplishments · gaps · rules · reconciliation result · Opus 4 escalations (count + outcomes) · next action · GitHub write status (✓ / ⚠ fallback).

**Fallback:** PUT fails after one retry → output YAML as fenced code block; instruct manual paste. Never drop state.
