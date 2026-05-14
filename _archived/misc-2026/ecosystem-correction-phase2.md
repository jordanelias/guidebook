# Ecosystem Correction Workplan — Phase 2
**Date:** 2026-03-29
**Basis:** S1–S3 execution + github-io rebuild + pipeline audit + deep cross-referential audit + final assessment (this session)
**Supersedes:** correction-workplan-final.md §S7 (housekeeping absorbed here)
**Does NOT supersede:** S4–S6 (Opus review sessions — separate, unchanged)

---

## Scope

Everything identified in this session that remains unimplemented. Organized by dependency, not by discovery order. Every item traces to a specific conversation finding.

**Out of scope:** S4–S6 Opus review sessions (unchanged). New skill creation (index, glossary, figure numbering, format conversion, accessibility checker — logged as gaps, not scheduled).

---

## Phase A: File Cleanup (no dependencies — pure deletions, moves, headers)

All operations in one atomic GraphQL `createCommitOnBranch` commit.

### A1. Delete dead files (7 files)

| File | Reason |
|---|---|
| `skills/bibliography-compiler-spec.md` | Planning document. Content absorbed into bibliography-compiler_SKILL.md. |
| `references/ref-patterns.md` | Empty stub, never populated. cross-reference-resolver doesn't use it. |
| `references/terminology.md` | Empty stub, never populated. |
| `references/section-map.md` | Empty stub, never populated. haiku-chunker generates inline. |
| `references/economics-sources.md` | Empty stub, never populated. |
| `references/volii-registry.md` | 970b stub. volii-validator uses PROVISIONAL mode, not this file. |
| `references/critique-standards-section.md` | Boilerplate. Content to be merged into critique-report-writer before deletion (see B5). |

### A2. Move stale files to `_archived/` (9 files)

| File | Reason |
|---|---|
| `references/hierarchy-correction-v10.md` | Absorbed into toc.md + CO-0001. |
| `misc/best-practices-compendium_2026-03-20.md` | 265 KB historical BPC dump. |
| `misc/gap_register_2026-03-20.md` | Old gap register snapshot. |
| `misc/correction-workplan-2026-03-28.md` | Executed. |
| `misc/endnote-downstream-amendments-2026-03-27.md` | All amendments applied to skills. |
| `misc/ecosystem-audit-2026-03-28.md` | Findings executed. |
| `misc/ecosystem-update-plan-2026-03-29.md` | Superseded by correction workplan. |
| `misc/work-triage-plan-2026-03-29.md` | Absorbed into correction workplan. |
| `workplan/v10-4-integrated.md` | Superseded by v10-5. S7 says deprecate. |

**Method:** GraphQL `createCommitOnBranch` with deletions for originals + additions at `_archived/{filename}`.

### A3. Add FROZEN headers to 28 flat files (14 BPC + 14 SL)

Header text:
```
<!-- FROZEN — Do not read or write. Per-slug files at references/{bpc|search-log}/{topic}/{slug}.md are canonical. This file is a historical archive only. Any skill reading this file is in error. -->
```

Files: `references/bpc/{ALL-ENV,ALL-FW,ALL-ROOMS,DBL,DEAF,DEM,IntD,MOB,NDV-MH,NDV,NEU,OFS,PAIN,VIS}.md` and same 14 under `references/search-log/`.

**Method:** GraphQL batch_read all 28 files → prepend header → single atomic commit.

### A4. Strip `<!-- GOVERNED BY PROJECT INSTRUCTIONS -->` headers (4 files)

Files: bibliography-compiler, item-specification-writer, research-log-manager, connection-scout.

**Batch with A3 commit if practical, else separate commit.**

### A5. Rename legacy session file

`sessions/session_084.md` → identify its date from content, rename to `sessions/session_YYYY-MM-DD-HHMM.md` format.

---

## Phase B: Data Architecture (depends on A — clean state)

### B1. Fix Part number references in 4 skills

| Skill | Change |
|---|---|
| chunk-assembler | "Part 7" → "Part 4" (2 refs). "part-07" → "part-04". "cat-A.md through cat-K.md" unchanged (item codes are Part-independent). |
| item-specification-writer | "Part 7" → "Part 4". "Part 8 §8.4" → "Part 5 §5.2". |
| cross-reference-resolver | "Part 7" → "Part 4" (5 refs). "part-07" → "part-04". |
| workplan-orchestrator | "Part 8 development" → "Part 5 development" in Sensory QA workflow. |

**Single atomic commit.**

### B2. Remove all `Preceded by` / `Feeds into` from individual skills (8 files)

Skills affected: chunk-assembler, bibliography-compiler, citation-miner, evidence-marker, item-specification-writer (both sets — lines 200-201 AND 230-231), vol2-item-formatter, structure-auditor, cross-reference-resolver.

**Rationale:** The Workflow table in workplan-orchestrator is the sole authority on pipeline sequencing. Individual skills declare I/O contracts (Input/Output) only. Dual-source pipeline declarations have already drifted (ISW has two contradictory sets, v2f lists wrong predecessor, xr is incomplete).

**Replace with standardized I/O block:**
```markdown
**Input:** [what this skill consumes — file types, formats, preconditions]
**Output:** [what this skill produces — file types, formats, state changes]
```

Pipeline position, predecessors, and successors are defined exclusively in the workflow table.

**Single atomic commit for all 8 files.**

### B3. Fix stale file references in skills (2 files)

| Skill | Line | Change |
|---|---|---|
| cross-reference-resolver | 166 | `references/best-practices-compendium.md` → `references/bpc/{topic}/{slug}.md` (per-slug architecture) |
| item-specification-writer | 200-201 | Delete stale first declaration (duplicate of lines 230-231, already resolved by B2) |

**Batch with B2 commit.**

### B4. Compact Skill Registry (workplan-orchestrator)

Replace 85-line table with compact grouped list (~15 lines):

```markdown
## Skill Index

All skills Sonnet 4.6 unless noted. GET `skills/{name}_SKILL.md` before execution.

**Orchestration:** workplan-orchestrator · session-consolidator · github-io
**Document Processing:** haiku-chunker · structure-auditor · markdown-formatter · chunk-assembler · find-and-replace · fix-linebreaks · table-formatter · toc-editor · file-splitter · bulk-renumber
**Content Analysis:** guidebook-auditor · content-gap-analyzer · framing-checker · evidence-auditor · evidence-marker · item-consolidation-analyzer · version-diff · sensory-coherence-checker
**Writing:** prose-style-checker · item-specification-writer · vol2-item-formatter · bibliography-compiler · practice-note-generator
**Research:** citation-verifier · multilingual-research (Opus 4.6 for synthesis) · research-log-manager · literature-review-planner · economics-researcher · jurisdiction-tracker · citation-miner · functional-deficit-researcher (Opus 4.6 for synthesis) · connection-scout (Opus 4.6)
**Reference:** cross-reference-resolver · volii-validator · supplemental-integrator · cross-population-conflict-mapper (Opus 4.6 for synthesis)
**Reporting:** critique-report-writer

**Retired:** vol1-corrections-writer · vol2-revision · plain-language-synthesizer · neufert-image-analyzer · keyword-lookup
**To build (P2):** poe-assessor · intersectionality-checker · index-generator · glossary-manager · figure-numbering · docx-exporter · accessibility-checker
```

### B5. Merge standalone reference files into skills (2 merges)

| Source | Destination | Then |
|---|---|---|
| `references/format-rules.md` (7.9 KB) | Append to `guidebook-auditor_SKILL.md` as §Format Rules | Delete source |
| `references/critique-standards-section.md` (1.9 KB) | Append to `critique-report-writer_SKILL.md` as §Standards Boilerplate | Delete source (per A1) |

### B6. Compact project-standards.md further (212 → <100 lines)

**Remove** (item-specific, belongs in BPC/item specs):
- Specification Upgrades section (E-08, C-04, ramp, turning circle, E-10, H-04) — 18 lines
- Citation facts (G-03 Levine, AOTA 2014) — 6 lines
- Item structural decisions (B-10 strobe, de-escalation rooms, IntD egress, Part V/VI authored) — 14 lines
- Disclosure templates (PAIN/OFS, DBL/IntD) — 6 lines

**Tag as TRANSITIONAL** (remove after CO-0004 propagation pass):
- CO-0003/CO-0004 rules (~40 lines) — add `<!-- TRANSITIONAL — remove after propagation -->` comment

**Target:** ~100 lines of universal process rules.

### B7. Update workflow table (workplan-orchestrator)

| Workflow | Change | Reason |
|---|---|---|
| **Document Assembly** | `chunk-assembler → [bibliography-compiler · table-formatter] → cross-reference-resolver → guidebook-auditor A` | table-formatter is independent of bibliography-compiler; parallelizable. (C4 from pipeline audit) |
| **Structural Change** | `[structure-auditor · markdown-formatter] → cross-reference-resolver → find-and-replace → guidebook-auditor A` | Independent skills; parallelizable. (P2 from pipeline audit) |
| **New Chapter** | Delete as standalone workflow. Note: "Compose: Evidence Gap → Item Specification." | Redundant composition of two existing workflows. evidence-marker removed (R1: redundant for ISW-drafted items). (R2 from pipeline audit) |
| **Evidence Marker Pass** | Add note: "Audit mode only — runs on assembled volumes post-chunk-assembler. Not used inline with item-specification-writer." | Clarifies evidence-marker's role. (C5 from pipeline audit) |

---

## Phase C: Protocol and Model Updates (depends on B — accurate skill files)

### C1. Update session start protocol (workplan-orchestrator)

Replace current 5-step REST protocol with:

```markdown
### 1a — Load core state (GraphQL batch_read — call 1)

Fetch in one call via github-io batch_read:
- `sessions/LATEST`
- `references/project-standards.md`
- `skills/workplan-orchestrator_SKILL.md`

Parse LATEST to get session filename.

### 1b — Load session file (GraphQL batch_read — call 2)

Fetch the session file identified in LATEST.
Report: session_close, next_action, blockers. Confirm before resuming.

### 2 — Load gap register (filtered bash)
Extract OPEN P1 items only. Do not load full file.

### 3 — Confirm PAT
If not in PI: prompt.

### 4 — Task Intake
Select workflow → load required skills via batch_read (see §Workflow-Gated Loading).
```

**Total startup:** 2 GraphQL calls + 1 filtered bash read. ~8K tokens (workplan-orchestrator 3K + project-standards 2.5K + session file 1–2K + gap register filtered 0.5K).

**Removes:** REST calls (was 4+). Stale-file-filing step (periodic activity, not every session).
**Adds:** Workflow-gated loading. workplan-orchestrator mandatory at startup (contains workflow table, Population Codes, CO-0004 map).

### C2. Implement workflow-gated skill loading

Add section to workplan-orchestrator:

```markdown
## Workflow-Gated Loading

When a workflow is selected, load ONLY the skills listed in that workflow.

1. Resolve skill list from Workflows table.
2. GraphQL batch_read all skill files in one call.
3. Execute in workflow sequence. Each skill's output feeds next.
4. No skill outside the workflow list may execute without explicit user approval.

**Fork handling:** If a workflow step has a conditional branch (e.g., rlm CHECK → COMPLETE vs PARTIAL), load additional skills for the taken branch on demand via a second batch_read.

**Pipeline safety:** Workflow table is a DAG. Skills execute in topological order. The orchestrator is the sole caller — no skill calls another skill directly.
```

### C3. Update model declarations for 4 Opus-split skills

| Skill | Current | New |
|---|---|---|
| multilingual-research | `Sonnet 4.6 + web` | `Sonnet 4.6 (search, extraction, Steps 1–4) · Opus 4.6 (best_practice_synthesis). Opus routing: Sonnet completes search → checkpoints to GitHub → flags synthesis for Opus session. Sonnet NEVER writes best_practice_synthesis.` |
| evidence-auditor | `Sonnet 4.6` | `Sonnet 4.6 (extraction, marker counting) · Opus 4.6 (overclaiming judgment, evidence sufficiency). Opus routing: Sonnet extracts markers and evidence tiers → Opus determines whether evidence supports claims.` |
| content-gap-analyzer | `Sonnet 4.6` | `Sonnet 4.6 (inventory, coverage mapping) · Opus 4.6 (gap significance judgment). Opus routing: Sonnet produces coverage inventory → Opus determines which gaps are consequential.` |
| functional-deficit-researcher | `Sonnet 4.6` | `Sonnet 4.6 (search, scenario execution) · Opus 4.6 (synthesis, NOVEL/REFINES classification). Opus routing: Sonnet runs scenarios → Opus synthesizes findings into BPC.` |

**Practical constraint:** No programmatic Opus path from claude.ai artifact proxy. Opus requires model picker set to Opus. These skills run search/extraction in Sonnet sessions, checkpoint state, then synthesis steps execute in dedicated Opus sessions (S4–S6 pattern).

### C4. Add `Opus synthesis: YES/NO` gate to research-log-manager and item-specification-writer

**research-log-manager LOG:** Add field `opus_synthesis: true|false` to BPC entry. Default `false` on write. Set to `true` only when best_practice_synthesis is written or reviewed in an Opus session.

**item-specification-writer:** Pre-step check: if BPC entry has `opus_synthesis: false`, emit warning: `[BPC NOT OPUS-REVIEWED — synthesis may be incomplete. Proceed with Sonnet-level synthesis at reduced confidence.]` Do not block — but the warning propagates to all downstream outputs.

---

## Phase D: Publication Pipeline Gaps (identified, not scheduled)

These are skills needed for final publication that do not exist. Logged in workplan for future scheduling.

| Skill | Purpose | Priority |
|---|---|---|
| `index-generator` | Generate book index from marked terms across assembled volumes | P2 |
| `glossary-manager` | Add/update/cross-reference glossary entries; validate all glossary terms appear in body | P2 |
| `figure-numbering` | Sequential figure and table numbering across assembled volume | P2 |
| `docx-exporter` | Convert assembled .md to styled DOCX with ToC, headers, page numbers | P3 |
| `accessibility-checker` | Verify output document is itself accessible (heading structure, alt text, reading order) | P3 |

---

## Execution Plan

| Step | Phase | Method | Files touched | Commits |
|---|---|---|---|---|
| 1 | A1+A2 | GraphQL: additions (moved files at `_archived/` paths) + deletions (originals + dead stubs) | 16 deletions, 9 additions | 1 |
| 2 | A3+A4 | GraphQL batch_read 32 files → prepend FROZEN/strip headers → single commit | 32 modifications | 1 |
| 3 | A5 | GraphQL: rename session_084.md | 1 delete, 1 add | 1 |
| 4 | B1+B2+B3 | GraphQL batch_read 12 skills → fix Part numbers + remove pipeline declarations + fix stale refs → single commit | 12 modifications | 1 |
| 5 | B4+B5+B7 | GraphQL batch_read workplan-orch + guidebook-auditor + critique-report-writer → compact registry + merge reference files + update workflows → single commit + 2 deletions | 3 modifications, 2 deletions | 1 |
| 6 | B6 | GraphQL: update project-standards.md | 1 modification | 1 |
| 7 | C1+C2 | GraphQL: update workplan-orchestrator (session start + workflow-gated loading) | 1 modification | 1 |
| 8 | C3+C4 | GraphQL batch_read 6 skills → update model declarations + opus gate → single commit | 6 modifications | 1 |

**Total: 8 commits (down from 30+ if done the old way). All atomic via GraphQL.**

---

## Dependency Map

```
Phase A (cleanup) ─── no dependencies
  │
  ▼
Phase B (data architecture) ─── depends on A (clean state)
  │
  ▼
Phase C (protocols + models) ─── depends on B (accurate files)
  │
  ▼
Phase D (publication gaps) ─── future sessions, depends on C
```

S4–S6 (Opus review sessions from original workplan) run independently. They depend on S2 (pipeline verified ✓) but not on Phases A–C here. They CAN run in parallel with Phases A–C.

---

## Audit Checklist

| Check | Status |
|---|---|
| Every finding from pipeline audit addressed? | ✓ C1–C5, R1–R3, P1–P2, 10 missing declarations |
| Every finding from deep audit addressed? | ✓ A1–A13, B1–B2, C1–C6 |
| Every finding from final assessment addressed? | ✓ Dead files, missing skills, Opus splits, FROZEN headers |
| No circular dependencies in execution plan? | ✓ A→B→C→D linear |
| No contradiction with S4–S6 Opus sessions? | ✓ Independent, can parallel |
| PI text still valid after all changes? | ✓ PI references workplan-orchestrator; WO is updated, PI unchanged |
| Commit convention followed? | ✓ All messages follow `{skill}: {action} [{timestamp}]` |
| GraphQL used for all batch operations? | ✓ 8 commits, all atomic |
| Workflow-gated loading prevents out-of-sequence execution? | ✓ Orchestrator sole caller, DAG enforced |
| FROZEN headers prevent stale file access? | ✓ 28 files get headers with explicit "reading this is an error" instruction |
| Opus routing clearly defined? | ✓ 4 skills have split declarations, practical constraint documented |
| No item-specific content in session-loaded files? | ✓ After B6, project-standards contains only universal rules |
| Session start token budget? | ✓ ~8K tok (project-standards 2.5K + session file 1–2K + workplan-orchestrator 3K + gap register filtered 0.5K) |

---

## User Actions Required

1. **Replace PI** in Project custom instructions with text from workplan §1.1 (includes actual PAT). — Carried forward from S1, still pending.
2. **Delete `opus-passthrough.html`** from Project Files. — Carried forward from S1, still pending.
3. **PAT rotation** — deferred to post-S7, unchanged.

---

## What This Workplan Does NOT Cover

- S4–S6 Opus review sessions (grab bar, toilet, acoustics, sensory, NDV/AUT, case studies) — separate, unchanged
- CO-0004 Part renumbering propagation through guidebook body — separate find-and-replace pass
- Phase D skill creation — future sessions
- Body ↔ bibliography cross-reference audit — post Phase 3 assembly
- Research resumption — workplan v10-5

---

*End of workplan*
