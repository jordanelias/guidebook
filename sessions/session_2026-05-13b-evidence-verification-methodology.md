---
session: session_2026-05-13b-evidence-verification-methodology
date: 2026-05-13
session_close: 2026-05-13 — DR-2026-05-13 adopted; migrations 010+011 applied; Track 1 first pass; architecture v2.3 authored; PI v10.10 drafted; repo reorganized (113 file ops across 6 batches); audit findings actioned
next_action: owner deploys PI v10.10 to live project settings; next-session work — Track 1 second pass, Phase E.1 single-BPC pilot under reasoning_doc_citations workflow, author skills/reasoning-doc-citations_SKILL.md
blockers: PI v10.10 deployment requires manual owner paste (Anthropic's project-knowledge layer not API-writable); pilot BPC for Track 3 not yet selected
---

# Session 2026-05-13b — Evidence verification methodology + repo reorganization

## Mandate

Three owner directives:
1. Research best practices for parallel situations, then decide methodology for the existence-vs-content verification gap
2. Clean PI v10.9 for conciseness; create architecture file (provided v2.1 as input); audit all directions
3. Organize repository per data-management best practices (multi-lens website needs SQLite integrity for academic rigor)

All under owner directive "do whatever is in best interest of project long-term."

## Decision (DR-2026-05-13)

**Option C** — three-track hybrid. Not the handoff's A or B.

- **Track 1**: versioning backfill from already-fetched catalog pages. 41 records done; ~600 remaining.
- **Track 2**: PMP promoted to actual gate via rule #10 sharpening.
- **Track 3**: new `reasoning_doc_citations` table for per-cell verification during Phase E.1.

Research grounding: Cochrane mandatory dual independent extraction; GRADE 10% pilot calibration; empirical 17-25% quotation-error base rate across three meta-analyses (~44,000 quotations in peer-reviewed medical lit; no improvement over time per Cobey et al. 2025).

`[CONFIDENCE: medium — base rate not domain-matched to building codes]`

## Architecture v2.3 (was phantom)

Authored from v2.1 starting point. Major refresh:

- `<enforcement_spectrum>` rewritten to reflect actual state: 15+ blocking CI checks across `ci.yml` and `audit.yml` (was "all rules are level 1" in v2.1)
- `<reference_files_pattern>` updated for Phase A directories
- `<bootstrap_exception>` acknowledges current ~70-line bootstrap
- `<skill_registry_pattern>` adds placeholder convention
- `<open_items>` refreshed with actionable gaps

226 lines. Committed to `architecture/project-architecture-guidebook-v2.3.md`.

## PI v10.10

307 lines (v10.9) → 259 lines (v10.10). State content moved out of standing rules to DRs/DB. `<hooks_status>` rewritten to reference actual CI workflows instead of phantom hook-workplan. Architecture pointer correct (file now exists).

## Repo reorganization (6 batched commits, 113 file ops)

| Batch | Action | Files |
|---|---|---|
| A | Root cleanup → archived/scripts | 4 files |
| B | Stale dated audit reports → `audits/_archived/` | 21 files |
| C | Deprecated reference docs → `_archived/references/` | 2 files |
| D | Superseded workplans → `workplan/_superseded/` | 17 files |
| E | `working/` dated work → `_archived/working-2026/` | 10 files |
| F | Data-layer fixes | 3 generate scripts repointed at `data/guidebook.db`; `data/db/` removed |
| G | Refresh `effort-guide.md` + `skill-registry.md` | 2 files (Valoria removed; new skills added; registry 368→109 lines) |

`scripts/generate/` had been pointing at `data/db/guidebook.db` (didn't exist); fixed to `data/guidebook.db` (the actual canonical path used by migrations, CI, and audit scripts).

## DB state changes (session total)

- user_version 9 → 11
- schema_version 6 → 11
- Migration 010 (FK integrity): 4 tables / 782 rows repointed; 1 invalid FK fixed; 5 epm NULLs backfilled; `gap_id` column added
- Migration 011 (reasoning_doc_citations): table + 4 indexes + CHECK constraints
- Track 1 data migration: 41 records' `edition` populated
- New audit scripts shipped: `pmp_audit.py`, `reasoning_doc_citations_audit.py`

## Files now durable in repo

Architecture v2.3, PI v10.10, DR-2026-05-13, migrations 010/011/track1, two new audit scripts, updated DB, refreshed effort-guide and skill-registry, session record. Plus 54 archived files across `_archived/`, `audits/_archived/`, `workplan/_superseded/`, `_archived/working-2026/`.

## Audit findings (architecture/PI/skills/hooks)

11 drift items identified during audit. Actions taken:
- HIGH-1: Architecture spec phantom → **AUTHORED v2.3**
- HIGH-2: Stale `references/project-instructions.md` v9 banner → **archived to `_archived/references/`**
- HIGH-3: Phantom `hook-workplan-guidebook.md` → **PI v10.10 references actual CI workflows instead**
- MED-1: `skill-registry.md` referenced "Architecture v2.2" → **rewritten, references v2.3**
- MED-2: `toc-editor` registry status vs PI conflict → **note added to registry**
- MED-3: `effort-guide.md` Valoria contamination + missing skills → **full refresh**
- MED-4: 5 PI-named skill placeholders → **placeholder convention added to architecture v2.3 + PI v10.10**
- LOW-1: 90+ files in `references/` → **23 archived to `audits/_archived/` and `_archived/references/`**
- LOW-2: `working/` dir of dated work product → **all 10 files + subdir moved to `_archived/working-2026/`**
- LOW-3: Root-level clutter → **4 files relocated**
- LOW-4: Superseded co0007 workplans still in `workplan/` → **17 files moved to `workplan/_superseded/`**

## Token usage estimate

~500k of 1M context window (~50%). Substantial headroom for further work.

## Logging tags applied

- `[SELF-AUTHORED — bias risk]` on the DR (reviewing prior session handoff)
- `[CONFIDENCE: medium — base rate not domain-matched]` on the 17-25% quotation-error prior

## Caveats

- Track 3 pilot BPC not yet selected (owner directive needed)
- Cochrane gold-standard dual independent extraction structurally unavailable (single-reviewer project); pilot mandate is partial mitigation
- The orchestrator's skill-index taxonomy embedded in `skills/workplan-orchestrator_SKILL.md` is itself stale (still classifies `toc-editor` deprecated; missing 11 newer skills). Refresh queued for future session.
- Effort-guide uses numerical levels (50/75/100/125/150) while user preferences use qualitative (low/medium/high/max). Both coexist; possible future consolidation.
