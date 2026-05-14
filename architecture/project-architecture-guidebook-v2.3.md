# Project Architecture — Guidebook
**V2.3 · 2026-05-13**
Project-specific architecture governance. Lives in `architecture/` of `jordanelias/guidebook`.
Companions: `userPreferences-v6.1.md` (account-wide), `governance/project-instructions-v10_9.md` (this project's PI).

<governs>
This document governs the Accessible Built Environments Guidebook project. It defines what belongs in the user preferences, the PI, the skills, the audit scripts, and the CI workflows — and how those layers interact.
</governs>

<three_layer_model>
```
┌──────────────────────────────────────┐
│  USER PREFERENCES (account-wide)     │  ← v6.1
│  In claude.ai Settings → Profile     │
└──────────────────────────────────────┘
            ↓ outer wins by default
┌──────────────────────────────────────┐
│  GUIDEBOOK PI (this project)         │  ← v10.9
│  In claude.ai Project Instructions   │
└──────────────────────────────────────┘
            ↓ outer wins by default
┌──────────────────────────────────────┐
│  GUIDEBOOK SKILLS (executable)       │
│  In jordanelias/guidebook/skills/    │
└──────────────────────────────────────┘
            ↓ cross-cutting enforcement
┌──────────────────────────────────────┐
│  AUDIT SCRIPTS + CI WORKFLOWS        │
│  scripts/audit/ + .github/workflows/ │
└──────────────────────────────────────┘
```

Conflict resolution:
1. Outer layer wins by default.
2. PI may override a preference only with an explicit clause naming the rule and scope. Implicit overrides are ignored.
3. Skills override PI only on execution mechanics; PI governs trigger conditions and assignments.
4. CI workflows and audit scripts (the cross-cutting layer) trump text rules for the matching check, regardless of where the text rule lives.
</three_layer_model>

<layer_ownership>
**User preferences** own: tone · output format · logging conventions · effort calibration · web/MCP defaults · token reporting · accuracy and uncertainty tags · persistence mitigation · model identity policy · model routing for artifact-side calls · extended thinking guidance · execution permissions.

Preferences exclude: anything project-specific.

**Guidebook PI** owns: project identity (repo, branch, PAT) · bootstrap (the documented exception) · project terminology (DD, RFO, BPC, PMP) · project-specific standing rules · skill assignments · reference file declarations · commit convention · session close protocol · override clauses · the architecture/PI/skills/CI pointer.

PI excludes: re-statements of preference-level rules · procedural detail (lives in skills) · transient state (lives in DB, sessions, or DRs) · anything not project-specific.

**Guidebook skills** own: the actual procedures (how to run a research check, how to consolidate a session, how to write an item specification, etc.) · templates · skill metadata · per-skill model assignment.

Skills exclude: project identity · user preferences · trigger-condition policy (that's PI's job).

**Audit scripts and CI workflows** own: mechanical compliance checks · regression tests · referential integrity · format validation.

The cross-cutting layer exists because text rules degrade over time without mechanical enforcement. Rules that the project cannot afford to drift on get promoted from text (level 1) → audit script (level 2) → CI (level 3/4).
</layer_ownership>

<bootstrap_exception>
PI may contain bootstrap procedure inline. This is the only procedural exception.

**Why:** skills load on trigger, but bootstrap must run *before* skills can load. A skill cannot bootstrap itself.

**Constraints:**
- minimal · executable (actual bash, not abstract description) · idempotent (safe to re-run) · self-reporting (outputs a status block)
- portable backend: gh CLI if available, curl otherwise (PI v10.3 added this)
- read-only: bootstrap never writes
- runtime under ~30 seconds when network responsive

**Current size note.** PI v10.9's bootstrap is ~70 lines (vs v2.1's stated 30-line target). The growth comes from the SQLite query block (rule #8 PMP metrics, rule #10 evidence-gate metrics, v10.9's Track 1 / Track 3 progress counters) added across v10.7-v10.9. Reading the DB on bootstrap is high-value (state visibility before every session) and outweighs the size discipline. If bootstrap grows past ~100 lines or runtime exceeds 30 seconds, extract the SQLite block to a `bootstrap-status` skill and leave a thin caller in PI.
</bootstrap_exception>

<surface>
**Guidebook targets claude.ai chat with Code Interpreter.**

Bootstrap requires code execution. Without Code Interpreter, the PI's bash + curl calls cannot run and the project fails to load. If a session is opened without Code Interpreter, the PI's bootstrap-exempt clause applies: limit work to review/conversation that doesn't touch repo state.

Skills are repo-resident files in `jordanelias/guidebook/skills/`, fetched into context on demand. They are not claude.ai Settings → Capabilities skills (which are global to the account).

The Code Interpreter container is ephemeral. Files at `/tmp/*` and `/home/claude/*` reset between turns; all durable work must be committed to the repo via the GitHub Contents API.
</surface>

<reference_files_pattern>
Guidebook maintains a `references/` directory in the repo. The PI declares which files are loaded on bootstrap; everything else is read on demand.

**Required (loaded on bootstrap):**
- `project-standards.md` — domain conventions, citation style, voice rules, structural rules
- `skill-registry.md` — index of all skills with status/classification/triggers. Source of truth for skill assignments per `<skill_registry_pattern>` below.

**Required (read on demand):**
- `effort-guide.md` — per-skill effort overrides. Default `medium` if not listed.

**Phase A directories** (per BPC rewrite workplan `audits/bpc-rewrite-workplan-2026-05-11.md`):
- `bpc-reasoning/<slug>.md` — per-BPC reasoning documents (Phase E.1 target: 95 docs)
- `connection-reasoning/<con-id>.md` — per-connection reasoning documents (Phase D target: 245 docs)
- `keyword-compendiums/<lang>.md` — per-language native-vocabulary compendiums (Phase A.11; required for AR/HI/ID/SW/BN before they exit `[UNVERIFIED-TERMS]` status)

**Removed:**
- `canonical-sources.md` — removed in v10.3 per PI changelog

**Reference files are project context, not skills.** Treat them as production documents — version them, audit them, keep them tight.

**Sprawl warning.** The current `references/` directory contains 90+ files, many of which are one-off audit reports (e.g., `bibliography-citation-audit-2026-04-09.md`, `co1-verification-report-2026-04-23.md`). These should be migrated to `_archived/` once their findings have been actioned, to keep the namespace navigable. See `<open_items>
**Resolved in session_2026-05-13b (this session, after audit):**
- ✓ `architecture/project-architecture-guidebook-v2.3.md` — was phantom across PI v10.3–v10.9; authored this session
- ✓ `references/project-instructions.md` — deprecated v9 PI shell archived to `_archived/references/project-instructions-v9-deprecated.md`
- ✓ `references/effort-guide.md` — full refresh; Valoria cross-project contamination removed; 4 missing skills added
- ✓ `references/skill-registry.md` — 368 → 109 lines; reconciled with current `skills/` state; architecture pointer corrected v2.2 → v2.3
- ✓ Phantom `hook-workplan-guidebook.md` — PI v10.10 `<hooks_status>` rewritten to reference actual `.github/workflows/ci.yml` + `audit.yml`
- ✓ `references/` sprawl — 21 dated audit reports moved to `audits/_archived/`; references/ now at 48 files (was 70+)
- ✓ Root-level clutter — 4 files relocated (`gap_register*.md` → `_archived/`; `tag_*_claims.py` → `scripts/`)
- ✓ Superseded `co0007-*` workplans — 17 files moved to `workplan/_superseded/`
- ✓ `working/` dated work product — 10 files moved to `_archived/working-2026/`
- ✓ Critical data-layer fix — `scripts/generate/{spec,room,population}_page.py` had `DB_PATH = data/db/guidebook.db` (non-existent); corrected to `data/guidebook.db`. Vestigial `data/db/` directory removed.

**Still open:**
- `[GAP: skills/workplan-orchestrator_SKILL.md embedded skill-index taxonomy is stale — still classifies toc-editor as deprecated despite PI rule #3 invoking it; missing 11 newer skills. Refresh queued for future session.]`
- `[GAP: skills/reasoning-doc-citations_SKILL.md placeholder named in PI v10.10 rule #10; skill file to be authored in Phase A parallel-track.]`
- `[GAP: ~14 working-doc files remain in references/ (theory-gap-analysis.md, throughline-*.md, methodology-*.md, parser-source-readiness.md, etc.) — looked stale during reorg but not unambiguously archivable without owner input. Triage queued.]`
- `[GAP: effort-guide.md uses numerical levels (50/75/100/125/150) while user preferences use qualitative (low/medium/high/max). Both coexist functionally; harmonization decision deferred.]`
- `[ASSUMPTION: Guidebook continues to target only claude.ai chat with Code Interpreter — basis: no requirement has surfaced for API, Claude Code, or other surfaces. Revisit if scope changes.]`
- `[ASSUMPTION: Pre-commit hooks (level 5) remain deferred. Basis: single primary author + CI catches everything. Revisit when contributor count > 1.]`
</open_items>

<changelog>
- **V2.3 (2026-05-13)** — Major refresh after audit. Replaces stale v2.1 description of enforcement state ("all rules are level 1") with current reality: 15+ blocking CI checks across `ci.yml` and `audit.yml`. Enforcement spectrum expanded to five levels with concrete examples per level. Added cross-cutting `<layer_ownership>` description of audit scripts and CI workflows. `<reference_files_pattern>` updated for Phase A directories (`bpc-reasoning/`, `connection-reasoning/`, `keyword-compendiums/`) and notes the `references/` sprawl problem. `<bootstrap_exception>` acknowledges current ~70-line bootstrap as deliberate. `<skill_registry_pattern>` adds the placeholder convention (PI v10.9 uses this for 5 named-but-not-built skills). PI growth target raised from 150 → 200 lines. New examples #4–5, #8–9 in `<conflict_resolution_examples>`. `<open_items>` refreshed with current gaps and decisions log.
- **V2.2 (never committed)** — Referenced by `references/skill-registry.md` (2026-05-08) but no file existed. v2.3 supersedes.
- **V2.1 (2026-05-07)** — Removed cross-references to other projects in ecosystem. Project-isolated.
- **V2.0 (2026-05-07)** — Split from generic spec into project-specific governance. XML tag wrapping. Identity at top, current state at bottom per Anthropic attention guidance.
- **V1.x** — Generic ecosystem-wide spec. Superseded.
</changelog>
