# Correction Workplan — Final
**Date:** 2026-03-28
**Basis:** Ecosystem audit (this session) + Ecosystem Update Plan (2026-03-29 rev.) + Work Triage Plan
**Absorbs and supersedes:** Ecosystem Update Plan FIX-01 through FIX-14 (all items resequenced)
**Goal:** Resolve all ecosystem issues in minimum sessions with correct dependency ordering

---

## Principles

1. **PI shrink first.** Every subsequent session benefits. Highest-ROI change in the project.
2. **Single source of truth.** Each piece of information lives in one place. Duplicates deleted.
3. **Fix infrastructure before content.** Pipeline integrity before Phase 3 writing.
4. **User actions batched.** All manual changes in one block.
5. **Minimize sessions.** Batch compatible steps. Separate only what must be separated (file size, model requirement).

---

## Session Plan Overview

| Session | Model | Content | Depends on |
|---|---|---|---|
| **S1** | Sonnet | PI rebuild + state file compaction + connection register split | — |
| **S2** | Sonnet | Pipeline integrity (endnote amendments, workflow resolution, dry run) | S1 (PI live) |
| **S3** | Sonnet | Skill file cleanup (frontmatter, model assignments, multilingual-research fix, session-consolidator update) | — |
| **S4** | Opus | Safety-critical synthesis review (grab bar, toilet centreline, conflict resolutions) | S2 (pipeline verified) |
| **S5** | Opus | Consequential judgments (acoustics, sensory relief, NDV/AUT, T0-03, E-14) | S4 |
| **S6** | Opus | Framework synthesis (case studies, pre-passthrough escalations) | — |
| **S7** | Sonnet | Housekeeping (file deprecated workplan, freeze flat files, commit final plan, PAT rotation) | S1–S6 |

**S2 and S3 are parallelizable** — they touch different files. Run in whichever order is convenient.
**S6 has no dependencies** — can run any time after S1.
**Total: 4 Sonnet + 3 Opus = 7 sessions.** With parallelization: 5 sequential sessions minimum.

User actions (PI paste, Project Files cleanup, PAT rotation) happen between S1 and S2.

---

## S1: PI Rebuild + State File Compaction (Sonnet)

### 1.1 Write the new PI

The new PI contains ONLY (~1,200 tokens):

```markdown
# Project Instructions — Accessible Built Environments Guidebook
**Revised:** [date]

## Identity
**Repo:** `jordanelias/guidebook` · branch `main`
**PAT:** [token]
**Commit convention:** `{skill-name}: {action} [{YYYY-MM-DD HH:MM}]`
**Active version:** V9.0 2026-03-20

## Architecture
- Conversation model: Sonnet 4.6. All assembly, drafting, research, coordination.
- Opus 4.6: best-practice synthesis, evidence arbitration, cross-referential judgment. Requires Opus selected in model picker — no programmatic escalation path.
- Artifact proxy: routes all model strings to Sonnet 4.5. Not a sub-model routing mechanism. Use only for user-facing interactive deliverables. Serial calls only (concurrent → 429). `show_widget` has no proxy access.
- PI text governs where PI and skill file conflict. Where a GitHub skill file has been updated more recently than the PI, the GitHub file governs for execution details; PI governs for model assignment and trigger conditions.

## Session Protocol
**Start (every conversation):**
1. GET `sessions/LATEST` → GET that session file. Report `session_close`, `next_action`, blockers.
2. GET `gap_register.md` — extract OPEN P1 items only (filtered, not full load).
3. GET `references/project-standards.md`.
4. GET `skills/workplan-orchestrator_SKILL.md`. Present workplan for user approval.
Other skills: GET from GitHub only when identified in workplan AND user approves.

**Close (~85% context or natural conclusion):**
Complete current stage. Commit all work. Invoke `session-consolidator`. Bullet-point handoff.

## Standing Rules
1. Never process >500 lines as single input.
2. All timestamps: `YYYY-MM-DD HH:MM` via `date -u`.
3. Default output: `.md`. DOCX only if requested.
4. `research-log-manager CHECK` before research; `LOG` after. Skipping = error.
5. Sources confirmed real. "I don't know" > invention.
6. Sonnet never determines best practice. Flag for Opus session.
7. Structural changes → `toc-editor` first. Change Order required.
8. Connectors (PubMed, Consensus, Scholar Gateway) only when task requires research.
9. DD = Design Development. RFO = Ready for Occupancy.
```

**What moved and where:**

| Removed from PI | Now lives in |
|---|---|
| Skill Registry (41 entries) | `workplan-orchestrator` §Skill Registry |
| Workflow Reference | `workplan-orchestrator` §Workflows |
| Evidence Hierarchy | `multilingual-research` + guidebook §1.5 |
| Population Codes + BAR rule | `workplan-orchestrator` (new §Population Codes) |
| Three-Tier Design Hierarchy | `item-specification-writer` |
| Endnote System | `bibliography-compiler` + `item-specification-writer` |
| Session-Close YAML schema | `session-consolidator` |
| Prose Register | `prose-style-checker` |
| Versioning rules | `workplan-orchestrator` |
| Unresolved Blockers | Session YAML `blockers:` field |
| GitHub API operations | `github-io` |
| Skill Design Principles | Deleted (recreatable) |

### 1.2 Add Population Codes section to workplan-orchestrator

GET `skills/workplan-orchestrator_SKILL.md`. Add section after §CO-0004 Part Numbering Map:

```markdown
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
```

Commit: `workplan-orchestrator: add Population Codes section [date]`

### 1.3 Commit PI text to GitHub

PUT new PI to `references/project-instructions.md` for version control.

### 1.4 Compact project-standards.md

GET `references/project-standards.md` (790 lines). Process:

1. Delete all explicitly SUPERSEDED rules (4 identified).
2. Delete contradictory skill-source rules (Rules 37, 48, 49, 90). Replace with single rule: "All skills: GitHub `skills/{name}_SKILL.md`. GET before execution."
3. Fix Rule ~51 (stale evidence hierarchy — says Tier 5 = "jurisdiction-specific regulatory documents" but canonical hierarchy says Tier 5 = "National beyond-code frameworks"). Correct or delete.
4. Delete one-time structural decisions absorbed into guidebook structure (e.g., "Part V is not a stub").
5. Merge duplicate rules (multiple timestamp rules, multiple skill-source rules).
6. Delete deprecated-skill rules (keyword-lookup deprecation notice — functionality already in multilingual-research).

Target: <200 lines.

Commit: `workplan-orchestrator: compact project-standards.md [date]`

### 1.5 Filter gap register loading

Update `workplan-orchestrator` session start protocol to extract OPEN items from gap_register.md via inline bash filter instead of loading the full 72 KB file. Pattern:

```bash
# In session start, replace full GET with filtered extract
curl -sL -H "Authorization: token ${PAT}" \
  "https://api.github.com/repos/jordanelias/guidebook/contents/gap_register.md" \
  | python3 -c "import sys,json,base64; d=json.load(sys.stdin); c=base64.b64decode(d['content']).decode(); [print(l) for l in c.split('\n') if '| OPEN |' in l or '| P1 |' in l]"
```

Commit with the workplan-orchestrator update from 1.2.

### 1.6 Split connection-register.md

GET `references/connection-register.md`. This file is 150 KB — may need chunked processing.

Split into:
- `references/connection-register-active.md` — PENDING entries only + header
- `references/connection-register-archive.md` — all other statuses

Commit both. Delete or redirect the original.

### 1.7 User actions (batched — do between S1 and S2)

1. **Replace PI** in Project custom instructions with the text from §1.1.
2. **Delete** `opus-passthrough.html` from Project Files.
3. After S7: **Rotate PAT** (see §S7).

**Checkpoint S1:** PI reduced to ~1,200 tokens. project-standards.md compacted. Gap register filtered at load. Connection register split. Session start cost: ~20,000 tokens (down from ~52,000).

---

## S2: Pipeline Integrity (Sonnet)

### 2.1 Amend chunk-assembler

GET `skills/chunk-assembler_SKILL.md`. Apply endnote-downstream-amendments §3:
- Add `bibliography-compiler` to `Feeds into:`
- Add REF-ID marker recognition (do NOT flag `[REF:...]` as broken refs pre-bibliography-compiler)
- Update back-matter assembly order to include endnotes

Commit: `chunk-assembler: endnote pipeline integration [date]`

### 2.2 Amend cross-reference-resolver

GET `skills/cross-reference-resolver_SKILL.md`. Apply endnote-downstream-amendments §4:
- Add endnote superscript pattern to Reference Pattern Inventory
- Add pre-run bibliography-compiler detection
- Add superscript ↔ endnote entry validation

Commit: `cross-reference-resolver: endnote pipeline integration [date]`

### 2.3 Resolve workflow conflicts + registry cleanup

GET `skills/workplan-orchestrator_SKILL.md`. Establish single canonical sequences:

**Item Specification:**
```
item-consolidation-analyzer
  → research-log-manager RETRIEVE
  → item-specification-writer (REF-IDs + sources-cited)
  → vol2-item-formatter (REF-ID validation)
  → [framing-checker · evidence-auditor]
  → prose-style-checker
  → volii-validator
```

**Document Assembly:**
```
chunk-assembler → bibliography-compiler → cross-reference-resolver → guidebook-auditor A
```

Also in this commit:
- Remove `neufert-image-analyzer` from Skill Registry (deprecated)
- Remove `keyword-lookup` from multilingual-research references (deprecated; replaced by "view Keyword Compendium Part 3")
- Verify `bibliography-compiler` and `vol2-item-formatter` are in Skill Registry with correct model assignments (Sonnet, not Haiku — since Haiku is not invocable)

Commit: `workplan-orchestrator: canonical workflows + registry cleanup [date]`

### 2.4 Endnote pipeline dry run

Execute full pipeline on ONE item (select an item with confirmed BPC Key sources):

1. `research-log-manager RETRIEVE` — confirm BPC has Key sources with REF-ID-ready entries
2. `item-specification-writer` — emit one item with `[REF:{slug}:{NN}]` markers + `#### Sources cited` table
3. `vol2-item-formatter` — validate REF-ID ↔ sources-cited integrity
4. `bibliography-compiler` — extract, deduplicate, number, replace markers with superscripts, generate endnote list
5. `cross-reference-resolver` — validate superscripts against endnote list

Pass criteria: no ORPHAN-REF errors, superscripts resolve correctly, endnote list is well-formed.

Commit results: `misc/bibliography-assembly-dryrun-[date].md`

**Checkpoint S2:** Endnote pipeline verified end-to-end. Phase 3 unblocked for non-REDO items.

---

## S3: Skill File Cleanup (Sonnet)

**This session can run in parallel with S2 — no shared file dependencies.**

### 3.1 Fix multilingual-research

GET `skills/multilingual-research_SKILL.md`. Process:
- Strip all `\\*\\*`, `\\---`, `&#x20;` escaped markdown artifacts
- Add YAML frontmatter (name + description <1024 chars)
- If >500 lines after cleanup: extract jurisdiction tables (Steps 2a/2b/Tier 5) into `skills/multilingual-research-jurisdictions.md` reference file; add `view` instruction in SKILL.md
- Remove keyword-lookup reference from pre-run steps

Commit: `multilingual-research: fix escaped markdown + YAML frontmatter [date]`

### 3.2 Add YAML frontmatter to 4 skills

GET and PUT each:
- `bibliography-compiler_SKILL.md`
- `connection-scout_SKILL.md`
- `item-specification-writer_SKILL.md`
- `research-log-manager_SKILL.md`

Commit one per skill.

### 3.3 Fix VIS/DEAF in item-specification-writer

While item-specification-writer is open: remove `VIS/DEAF` from the canonical codes list. Replace with correct separate VIS and DEAF entries.

Combine with 3.2 commit for this file.

### 3.4 Update model assignments

Batch across all affected skills. For each:
- **14 "Haiku" skills:** Change to "Model: Sonnet 4.6". Remove constraints predicated on Haiku limitations ("no content judgment") where Sonnet judgment would improve quality. Retain constraints that are desirable regardless of model.
- **4 "Opus" skills** (cross-population-conflict-mapper, research-log-manager synthesis, evidence-auditor judgment, content-gap-analyzer judgment): Change to "Model: Sonnet 4.6 — route synthesis/judgment to Opus session."
- **1 Opus skill** (connection-scout): Change "Opus 4" to "Opus 4.6". Retain Opus designation.

Affected skills (19 total): haiku-chunker, structure-auditor, markdown-formatter, fix-linebreaks, table-formatter, github-filing, file-splitter, bulk-renumber, find-and-replace, evidence-marker, guidebook-auditor, citation-verifier, chunk-assembler, cross-reference-resolver, vol2-item-formatter, volii-validator, supplemental-integrator, jurisdiction-tracker, connection-scout.

Execute as sequential GET → edit model line → PUT. Commit: `{skill}: update model assignment [date]`

### 3.5 Update session-consolidator

GET `skills/session-consolidator_SKILL.md`. Apply:

1. Formalize `date -u +"%Y-%m-%d %H:%M"` as canonical timestamp source. Remove any reference to system prompt date or bash clock.
2. Add YAML pre-commit blocker validation: GET prior session YAML, diff `blockers:` against gap register OPEN items, close any now-CLOSED. Blockers without corresponding gap IDs → create gap entry or remove blocker.
3. Update reconciliation: check `connection-register-active.md` instead of full register.
4. Reconciliation scope: session-local change log (skills run, gaps added/resolved, rules added), not full-file re-read of all state files. Full reconciliation becomes a periodic dedicated activity.

Commit: `session-consolidator: timestamp + blocker validation + lightweight reconciliation [date]`

**Checkpoint S3:** All skill files have YAML frontmatter. Model assignments reflect reality. No escaped markdown. No deprecated references. Reconciliation protocol is lightweight.

---

## S4–S6: Opus Review Sessions

Per Work Triage Plan. Run in Opus conversation sessions (model picker set to Opus).

### S4: Safety-Critical (blocks grab bar, toilet, A-04/B-05/A-09 items)

**Prerequisite:** S2 complete (pipeline verified).

Load BPCs: `fold-down-grab-bar-specification`, `upper-limb-impairment-built-environment`, `cross-population-conflict-resolutions`.

Tasks:
1. Verify 1.3 kN biomechanics → confirm or revise 200 kg load rating recommendation
2. Confirm or revise ADA 18-inch toilet centreline conflict assessment
3. Determine which A-04/B-05/A-09 values are defensible vs. [UNSUPPORTED]
4. (Parallel) Review CON-0050–0084 MODERATE connections — elevate or downgrade each

Output: Amended `best_practice_synthesis` sections. Updated GAP-OPS-01/02. Connection verdicts.

### S5: Consequential Judgments

**Prerequisite:** S4 complete.

Load BPCs: `acoustics-speech-intelligibility-disability`, `sensory-relief-space-design`, `ndv-aut-built-environment-quantified-thresholds`. Load E-14 draft. Load T0-03 rejection record.

Tasks:
1. Confirm 0.6 s as failure boundary (not compliance spec) for acoustic items
2. Confirm toilet adjacency mandatory status for sensory relief space
3. Confirm process-based design as highest-ambition spec for NDV/AUT thresholds
4. Review T0-03 retreat room rejection — can it achieve T0 with modified provision?
5. Confirm E-14 specification logic + verify remaining citations

Output: Amended syntheses. T0-03 verdict. E-14 marked Phase 3-ready or revised.

### S6: Framework Synthesis (no prerequisite — run any time after S1)

Load BPC: `residential-accessible-home-case-studies`. Load pre-passthrough escalation records.

Tasks:
1. Review 8 governing principles for Part 12 case study structure
2. Review pre-passthrough escalation determinations (grab bar type, turning circle, seizure, DEAF RT60)

Output: Confirmed or amended framework. Escalation determinations validated.

**Checkpoint S4–S6:** All REDO items resolved. All FLAG items reviewed. Phase 3 writing fully unblocked.

---

## S7: Housekeeping (Sonnet)

### 7.1 File stale workplan

Move `workplan/v10-4-integrated.md` to `workplan/deprecated/` via `github-filing`.

### 7.2 Freeze flat BPC/SL files

Add `<!-- FROZEN — new entries use per-slug files at references/bpc/{topic}/{slug}.md -->` header to each of 14 flat population-level BPC files and 14 flat SL files. Batch operation: GET each, prepend header, PUT back.

### 7.3 Update ecosystem plan on GitHub

Replace `misc/ecosystem-update-plan-2026-03-29.md` with final version reflecting all completed actions and remaining status.

### 7.4 PAT rotation (user action)

User creates new scoped PAT: `contents:read` + `contents:write` on `jordanelias/guidebook` only. No admin. Update PI. Revoke old PAT.

**Checkpoint S7:** All ecosystem corrections complete. Clean infrastructure for Phase 2B/3.

---

## Coverage Verification

Every finding from the ecosystem audit, every FIX from the ecosystem update plan, and every issue raised in the session conversation is addressed:

| Category | Items | All covered? |
|---|---|---|
| Ecosystem Update Plan FIX-01–FIX-14 | 14 | ✓ (FIX-02 and FIX-07 already done) |
| Audit §1 Architecture issues | 3 | ✓ |
| Audit §2 Skill-by-skill issues | 8 | ✓ |
| Audit §3 Pipeline integrity | 4 | ✓ |
| Audit §4 Data architecture | 4 | ✓ |
| Audit §5 Token efficiency | 5 optimizations | ✓ |
| Audit §6 Process integrity | 3 | ✓ |
| Audit §7 Accuracy issues | 3 | ✓ |
| Session conversation issues | 5 | ✓ |
| **Total** | **43 findings** | **All addressed** |

---

## What This Workplan Does NOT Cover

These are explicitly out of scope and tracked elsewhere:

- Phase 2B research resumption → workplan v10-5
- CO-0004 numbering propagation through skills → deferred until author approval
- Native Agent Skills upload → concluded as not suitable (audit §8)
- New skills (poe-assessor, intersectionality-checker) → P2 backlog
- Body ↔ bibliography cross-reference audit → post Phase 3 assembly

---

## Token Impact Summary

| Metric | Before | After S1 | After S1–S3 |
|---|---|---|---|
| PI system prompt | ~5,500 tok | ~1,200 tok | ~1,200 tok |
| project-standards.md load | ~18,000 tok | ~5,000 tok | ~5,000 tok |
| gap_register.md load | ~18,000 tok | ~2,000 tok | ~2,000 tok |
| connection-register.md | ~37,000 tok (unloadable) | ~5,000 tok (active only) | ~5,000 tok |
| Session start total | ~52,000 tok | ~20,000 tok | ~20,000 tok |
| Usable context (200K) | ~148,000 tok | ~180,000 tok | ~180,000 tok |
| **Efficiency gain** | — | **+22%** | **+22%** |
| Per-turn PI savings (×20 turns) | — | **86,000 tok/session** | — |

---

*End of workplan*
