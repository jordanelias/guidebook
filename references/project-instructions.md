# Project Instructions — Technical Guidebook Review System
**Last revised:** 2026-03-27 17:30
**Supersedes:** 2026-03-27 16:30

---

## Overview

This project produces, audits, and critiques **technical guidebooks** for OT practitioners, architects, and policy makers. Primary lens: occupational therapy evidence. Best practice = most amenable, inclusive, forgiving, caring, accommodating, dignified, specific, and targeted provision the evidence supports.

**Active version:** V9.0 2026-03-20
**Primary file:** `Guidebook_for_Accessible_Design_v9-0_2026-03-20.md`

---

## GitHub API

**Repo:** `jordanelias/guidebook` · branch `main`
**PAT:** {PAT — provided at session start}

**Read:** `GET .../contents/{path}` — `content` is base64. Capture `sha` for writes.
**Write:** `PUT .../contents/{path}` with `{"message","content","sha"}`. GET before PUT. On 409: re-GET, retry once. Failure → fenced code block + manual paste instructions.
**Commit convention:** `{skill-name}: {action} [{YYYY-MM-DD HH:MM}]`

---

## State Files (GitHub)

| File | Purpose |
|---|---|
| `sessions/session_YYYY-MM-DD-HHMM.md` | Session YAML — one per session |
| `gap_register.md` | Typed gap register — append-only, unique IDs |
| `references/project-standards.md` | Canonical rules — append-only |
| `references/toc.md` | Canonical ToC |
| `references/slug-registry.md` | Slug → topic-directory map |
| `references/search-log/{topic}/{slug}.md` | Per-slug search coverage |
| `references/bpc/{topic}/{slug}.md` | Per-slug best-practice compendium |
| `references/standards-registry.md` | Per-jurisdiction standard currency |
| `references/connection-register.md` | Unmade connections (PENDING→CONSUMED→DEFERRED→SUPERSEDED→CLOSED) |
| `references/change-orders/CO-{NNNN}-{YYYY-MM-DD-HHMM}.md` | Structural Change Orders |
| `references/bibliography-v9.md` | Bibliography verification reference |

**Retired (frozen):** `references/search-log.md` · `references/best-practices-compendium.md` · 15 flat `references/bpc/{POPULATION}.md` · 15 flat `references/search-log/{POPULATION}.md`

---

## Skill Architecture

**All skills live on GitHub at `skills/{skill-name}_SKILL.md`.** No project files are used for skill storage. At runtime: GET the skill file from GitHub before execution.

**Session start loads only:** `workplan-orchestrator` · `session-consolidator` · `github-io`. All other skills are loaded only when (1) identified in the workplan AND (2) user approves proceeding.

**Skill updates:** All skill edits are committed directly to GitHub. Commit: `{skill-name}: {description} [{YYYY-MM-DD HH:MM}]`.

---

## Model Roles

| Role | Model | Scope |
|---|---|---|
| **Assembly, collation, writing, formatting, extraction, organisation** | Sonnet 4.6 | Collate data. Present findings. Write from curated plans/directions/evidence/instructions. Format. Organise. Pattern match. Structural extraction. |
| **Judgment, synthesis, best-practice determination, evidence arbitration** | Opus 4 | Determine what constitutes best practice. Analyse and synthesise evidence. Resolve conflicting evidence. Arbitrate between competing provisions. Evaluate what is most inclusive/dignified/targeted. All `best_practice_synthesis` content. |
| **Mechanical tasks** | Haiku 4.5 | Chunking, line-level extraction, renumbering, formatting checks |

**Sonnet never determines best practice.** Sonnet collates evidence and presents it to Opus for judgment. Opus returns the synthesis. Sonnet then writes the specification from Opus's determination.

**Workflow:** Sonnet retrieves → Sonnet collates → Opus judges → Sonnet writes from Opus output.

---

## Session Protocol

### Start (every conversation)

1. GET `github-io`, `workplan-orchestrator`, `session-consolidator` from GitHub skills/.
2. GET most recent `sessions/` file. Report `session_close` + `next_action`.
3. GET `gap_register.md` — surface OPEN P1 items.
4. GET `references/project-standards.md` — load rules.
5. Present workplan for user approval before proceeding.

### Checkpointing

After each skill stage: `CHECKPOINT [YYYY-MM-DD HH:MM] — task · stage · status` (1–2 lines).

### Close (~85% usage OR natural conclusion)

1. Complete current stage.
2. Write all findings to GitHub.
3. Invoke `session-consolidator`.
4. Bullet-point handoff. Instruct new conversation.

---

## Population Codes

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
| IntD | Intellectual disability — main taxonomy; specs carry `[TIER 4-5; no quantified standard; March 2026]` |
| ALL | All disability categories |

VIS, DEAF, DBL: three distinct codes. VIS/DEAF invalid. DBL ≠ VIS + DEAF.
BAR: NOT main taxonomy. Large body size → Supp. Part 4 only. BAR in Volumes 1–3 = error; delete.
Supplementary (not main): CHD · LPA · EXH · BAR → Supp. Parts 1–4.

---

## Three-Tier Design Hierarchy

DAR mandatory at every tier.

| Tier | Context | Specification |
|---|---|---|
| **0** | No predominant disability population | Above code minimum; designed for future tailoring |
| **1** | Identified population(s) | Ranges; median = population-informed default |
| **2** | Identified individual | Co-designed; resolves value within Tier 1 range |

Ranges bridge Tier 1↔2. The guidebook is a framework for professional judgment, not a substitute.

---

## Evidence Hierarchy

Higher tier governs on conflict.

| Tier | Type |
|---|---|
| **1** | OT clinical research — intervention-tested |
| **Co-1** | Lived experience / participatory design (CRPD Art. 4.3) — co-primary with Tier 1 |
| **2** | Disability-led NGO / DPO / advocacy guidelines |
| **Co-2** | OT clinical practice guidelines |
| **3** | Systematic reviews and meta-analyses |
| **4** | International standards with evidence basis |
| **5** | National beyond-code frameworks |
| **6** | Statutory codes — reference baseline only |

Co-1/Tier 2 searched first (most under-retrieved). Evidence markers: ● = evidence-based; ○ = expert consensus; ◐ = mixed.

---

## Endnote System

All citations in Parts and Categories use **numbered endnotes** (superscript ¹²³ in body text). Each volume ends with a full endnote list in sequential order, organised under headings matching the Part/Category structure.

**Production chain:**
1. `item-specification-writer` (Sonnet) emits `[REF:{slug}:{NN}]` markers inline.
2. `vol2-item-formatter` (Sonnet) validates marker ↔ sources-cited integrity.
3. `bibliography-compiler` (Haiku) replaces markers with sequential superscripts, generates per-volume `## Endnotes` section organised by Part/Category headings.
4. `cross-reference-resolver` validates superscripts against endnote entries.

BPC Key sources ordering is frozen once REF-IDs are emitted. New sources append only.

---

## Standing Rules

### Document Processing
1. Never process >500 lines as single input → `haiku-chunker`.
2. Fresh DOCX conversion → `fix-linebreaks` first.
3. All timestamps: `YYYY-MM-DD HH:MM`.
4. Default output: `.md`. DOCX only if requested.

### Research
5. `research-log-manager CHECK` before any research; `LOG` after. Skipping = error.
6. Pre-LOG completeness gate: 7 conditions in skill file. Blocked until pass or explicit acceptance.
7. View Keyword Compendium (`multilingual-research-protocol-v4-2026-03-18-1.md` Part 3) before research.
8. Co-1/Tier 2 first. Citation mining mandatory for Tier 1–2 sources via `citation-miner`.
9. Best-practice synthesis mandatory before LOG. **Opus determines best practice; Sonnet collates evidence for Opus.**
10. Language (14) and jurisdiction (24 + ISO) are distinct axes; both independently satisfied.
11. Pre-v4 slugs: triage CONSUME / SUPPLEMENT / RE-RUN before executing.
12. Flat BPC/SL files frozen. New research → per-slug directory entries.
13. Sources confirmed real. "I don't know" > invention. 2 failed searches → CLOSED-DELETED.

### Citation & Endnote
14. Every prescriptive claim carries `[REF:{slug}:{NN}]`. Pre-step: `research-log-manager RETRIEVE`.
15. `bibliography-compiler` generates per-volume endnote sections with sequential numbering under Part/Category headings.
16. Bibliography reconciliation at assembly: diff compiler output vs bibliography-v9.md.
17. Endnote pipeline dry run (1 item end-to-end) must pass before Phase 3.

### Structure
18. Structural changes → `toc-editor` first. Change Order required. Never skip.
19. Volumes: Roman numerals. Parts: sequential 1–13. Sections: §X.Y.
20. DD = Design Development. RFO = Ready for Occupancy.

### Session & Skills
21. Never re-run completed stages.
22. Gap register IDs unique. Collision → suffix -b, -c.
23. Working documents committed to GitHub before session close.
24. Connection register: update PENDING→CONSUMED on incorporation. Verify at close.
25. Connectors (PubMed, Consensus, Scholar Gateway) only when task requires research.
26. All skills on GitHub. GET before execution. No project file reads for skills.

### Prose Register
- Voice: soft imperative subjunctive
- Headings: descriptive only
- Sequencing: Ideal → Best Practice → Acceptable → Minimum
- ≤25 words/sentence; one claim per sentence
- Every claim carries citation or `[UNSUPPORTED — citation required]`

### Versioning
Major (X.0) = structural. Minor (X.Y) = content. Patch (X.Y.Z) = editorial.

### FDR CONTRADICTS
Do not delete original BPC claim. Append `[CONTRADICTED BY FDR]`. Route to evidence-auditor (Sonnet collates; Opus adjudicates).

---

## Skill Registry

All skills stored at `skills/{name}_SKILL.md` on GitHub. GET before execution.

### Orchestration
| Skill | Model | Trigger |
|---|---|---|
| `workplan-orchestrator` | — | Multi-step tasks; session start |
| `session-consolidator` | Sonnet | Session end |

### Document Processing
| Skill | Model | Trigger |
|---|---|---|
| `haiku-chunker` | Haiku | Document >500 lines |
| `fix-linebreaks` | Haiku | Fresh DOCX conversion |
| `structure-auditor` | Haiku | Heading hierarchy |
| `markdown-formatter` | Haiku | Markdown consistency |
| `chunk-assembler` | Sonnet | Combine chunks |
| `find-and-replace` | Sonnet | Bulk substitution |
| `table-formatter` | Haiku | Table repair |
| `toc-editor` | Sonnet | Structural changes + Change Order |
| `vol2-item-formatter` | Sonnet | Item format + REF-ID validation |
| `bibliography-compiler` | Haiku | Endnote compilation; per-volume endnote sections |
| `bulk-renumber` | Haiku | Sequential renumbering |

### Content Analysis
| Skill | Model | Trigger |
|---|---|---|
| `guidebook-auditor` | Haiku (A/C/E) · Sonnet (B/D) | Format/consistency |
| `content-gap-analyzer` | Sonnet (collation) · Opus (judgment) | Coverage gaps |
| `framing-checker` | Sonnet | Social model; CRPD alignment |
| `evidence-auditor` | Sonnet (collation) · Opus (judgment) | Evidence stratification |
| `item-consolidation-analyzer` | Sonnet | Merge/split items |
| `version-diff` | Sonnet | Semantic diff |
| `connection-scout` | Opus | Cross-population connection discovery |
| `sensory-coherence-checker` | Sonnet (collation) · Opus (judgment) | Sensory spec consistency |

### Writing and Specification
| Skill | Model | Trigger |
|---|---|---|
| `prose-style-checker` | Sonnet | Style; voice; concision |
| `item-specification-writer` | Sonnet (drafting from Opus synthesis) · Opus (best-practice determination) | Specs with REF-ID + sources-cited |
| `practice-note-generator` | Sonnet | OT practitioner field tools |

### Research and Verification
| Skill | Model | Trigger |
|---|---|---|
| `citation-verifier` | Sonnet | Citation audit (PROVISIONAL mode) |
| `multilingual-research` | Sonnet (retrieval/collation) · Opus (synthesis/best-practice) | 14-lang × 24+ISO jurisdiction |
| `research-log-manager` | Sonnet | CHECK / LOG / RETRIEVE |
| `literature-review-planner` | Sonnet | Systematic review protocol |
| `economics-researcher` | Sonnet | Cost data; grants; ROI |
| `jurisdiction-tracker` | Sonnet | Standards currency |
| `functional-deficit-researcher` | Sonnet (retrieval) · Opus (synthesis) | Bottom-up OT/ICF search |
| `citation-miner` | Sonnet | Backward + forward citation mining |

### Reference Management
| Skill | Model | Trigger |
|---|---|---|
| `cross-reference-resolver` | Sonnet | Cross-refs; endnote superscript validation |
| `volii-validator` | Sonnet | Item code validation (PROVISIONAL) |
| `supplemental-integrator` | Sonnet | Supplementary volumes |

### Reporting
| Skill | Model | Trigger |
|---|---|---|
| `critique-report-writer` | Sonnet (assembly) · Opus (judgment) | Critique reports |

### Utility
| Skill | Model | Trigger |
|---|---|---|
| `github-io` | — | GitHub API helper |
| `evidence-marker` | Haiku | Evidence-tier markers |
| `file-splitter` | Haiku | Split into per-Part chunks |

**To build (P2):** `poe-assessor` · `intersectionality-checker`

---

## Workflow Reference

| Workflow | Sequence |
|---|---|
| **Full Section Review** | haiku-chunker → [structure-auditor · guidebook-auditor · content-gap-analyzer · framing-checker · evidence-auditor] → [research-log-manager CHECK · multilingual-research · citation-verifier · research-log-manager LOG] → prose-style-checker → critique-report-writer |
| **Item Specification** | item-consolidation-analyzer → research-log-manager RETRIEVE → Opus best-practice synthesis → item-specification-writer (Sonnet writes from Opus output) → vol2-item-formatter → [framing-checker · evidence-auditor] → prose-style-checker → volii-validator |
| **Document Assembly** | chunk-assembler → bibliography-compiler (generates per-volume endnotes) → bibliography-reconciliation → cross-reference-resolver → guidebook-auditor A |
| **Multilingual Research** | research-log-manager CHECK → Sonnet retrieves (Co-1 → statutory → beyond-code → academic → citation mining) → Opus synthesises best practice → research-log-manager LOG |
| **Connection Discovery** | connection-scout (Opus: internal then external) → connection-register → HIGH→item-spec briefing · SPECULATIVE→gap_register |
| **Bottom-Up FDR** | research-log-manager CHECK → functional-deficit-researcher (Sonnet retrieves; Opus synthesises) → research-log-manager LOG |
| **Bibliography Reconciliation** | bibliography-compiler output → diff vs bibliography-v9.md → flag discrepancies |
| **Structural Change** | toc-editor → find-and-replace → cross-reference-resolver → guidebook-auditor A |
| **Session Wrap** | session-consolidator |

---

## Session-Close YAML Schema

```yaml
session_close: YYYY-MM-DD HH:MM
document: "[DOC-ID]"
skills_run: []
gaps_added: []
gaps_resolved: []
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
next_action:
  skill: name
  session: description
  parameters: {}
```

---

## Unresolved Blockers

| Blocker | Status |
|---|---|
| Application volume full text | NOT AVAILABLE — volii-validator provisional |
| Endnote pipeline integration test | NOT DONE — must pass before Phase 3 |
| Body ↔ bibliography cross-reference audit | NOT DONE |

---

## Skill Design Principles

1. No file names in skill body.
2. No completed-task references.
3. No version-locked language.
4. One skill, one process.
5. All timestamps: `YYYY-MM-DD HH:MM`.
6. Skills live on GitHub only. GET before execution.

---

*End of Project Instructions*
