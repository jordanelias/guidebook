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

**Sprawl warning.** The current `references/` directory contains 90+ files, many of which are one-off audit reports (e.g., `bibliography-citation-audit-2026-04-09.md`, `co1-verification-report-2026-04-23.md`). These should be migrated to `_archived/` once their findings have been actioned, to keep the namespace navigable. See `<open_items>`.
</reference_files_pattern>

<skill_registry_pattern>
PI declares skill *assignments* as one-line entries (which skills the PI itself invokes). Detail (location, status, purpose, triggers, dependencies, classification) lives in `references/skill-registry.md`.

Skill files use flat form: `skills/<name>_SKILL.md` (not directory form).

Deprecated skills live in `skills/deprecated/` and are not loaded on trigger.

**Pruning rule:** any skill that stays at `planned` for >90 days without invocation gets demoted from PI assignments. Avoid carrying ghost skills.

**Placeholder convention.** When PI references a skill that does not yet have a file, the PI must explicitly state "skill placeholder" or "no skill file exists" inline. This avoids confusion between "missing skill" (a bug) and "named informational hook for future work" (deliberate). PI v10.9 follows this convention for `reasoning-doc-citations`, `bpc-curator`, `gap-register`, `bpc-writer`, and `opus-synthesis`.

**Drift between PI references and actual `skills/` content** is reconciled in `skill-registry.md`'s "Reconciliation drift" section, not in PI itself.
</skill_registry_pattern>

<enforcement_spectrum>
Rules can live at any of five levels. Higher levels are more reliable but more expensive to author and maintain.

| Level | Mechanism | Where | Reliability |
|---|---|---|---|
| 1 | Text rule | PI standing rules, DRs, skill descriptions | Low |
| 2 | Audit script | `scripts/audit/*.py` (CLI, manual or scheduled) | Medium |
| 3 | CI workflow, non-blocking | `.github/workflows/*.yml` with `continue-on-error: true` | High |
| 4 | CI workflow, blocking | `.github/workflows/*.yml` with `continue-on-error: false` | Highest |
| 5 | Pre-commit hook (local) | `.git/hooks/` (not yet installed in this project) | Highest (local) |

**Current state (2026-05-13):**

*Level 1 (text only):*
- Standing rules #1 (source discipline), #2 (synthesis routing), #5 (connector posture) — judgment calls, stay text
- Most of the rest of the PI's standing rules have level 2-4 enforcement supplementing them

*Level 2 (audit scripts, manual run):*
- `scripts/audit/pmp_audit.py` — rule #8 + rule #10 sub-rule 1 enforcement (added 2026-05-13)
- `scripts/audit/reasoning_doc_citations_audit.py` — rule #10 sub-rules 2/3 enforcement (added 2026-05-13)
- `scripts/audit/research_protocol_audit.py` — rule #7 enforcement
- `scripts/audit_evidence_metadata.py` — rule #10 existence-gate enforcement (top-level scripts/)
- `scripts/audit_adversarial_use.py`, `scripts/decision_capture.py`, `scripts/doctrine_recheck.py` — promoted to level 4 via `ci.yml` governance job

*Level 3-4 (CI workflows, currently 15+ blocking checks):*
- `.github/workflows/ci.yml`:
  - **syntax** — UTF-8 / JSON / YAML validity (blocking)
  - **structure** — `validate_bpc.py --all`, `validate_cross_refs.py`, `check_thresholds.py` (blocking)
  - **commit-msg** — commit message format per PI convention (blocking)
  - **schema** — `validate_schema.py`, `validate_evidence_state.py`, `validate_population.py`, `validate_jurisdiction.py`, `validate_temporal.py` (blocking; some `continue-on-error: true`)
  - **db_integrity** — `test_db_integrity.py` (35 checks; blocking)
  - **governance** — A10 adversarial-use catalogue, A12 decision register, A13 doctrine recheck (blocking)
- `.github/workflows/audit.yml`:
  - **source_slug_links duplicates** — blocking (per GAP-287)
  - **citation-mining completeness (current session)** — blocking
  - **migration reproducibility** — blocking (per GAP-290); rebuilds DB from migration history and compares invariants
  - Two informational citation-mining checks at T1-2 and T1-3 (continue-on-error: true)
- `.github/workflows/verify-urls.yml`, `.github/workflows/resolve-dois.yml` — scheduled jobs (not on push)

*Level 5 (pre-commit hooks, local):*
- None installed. Pre-commit hooks would catch issues before push (faster feedback) but require per-developer setup. Given the project has a single primary author and CI catches everything, deferred indefinitely.

**Promotion path.** New rules start at level 1 in PI standing rules. If the rule is mechanically checkable AND drift is observably costly, promote to level 2 by writing an audit script. If the rule must NEVER drift in `main`, promote to level 4 by adding the audit script as a blocking job in CI.

**Demotion path.** Audit scripts that haven't found an issue in 6 months may be downgraded to scheduled (weekly cron via GitHub Actions) rather than per-push, to reduce CI cost.

**Audit script style** (per existing examples in `scripts/audit/`):
- Module docstring lists checks numerically with rule provenance
- Single `audit()` function with each check as a numbered SQL query or comparison
- Reports formatted with "=" separators
- Exit code 0 = pass, 1 = any issues found
- Reads `data/guidebook.db` via `REPO = Path(__file__).resolve().parent.parent.parent` resolution
</enforcement_spectrum>

<conflict_resolution_examples>
| # | Situation | Resolution |
|---|---|---|
| 1 | Preference says X, PI silent | Preference applies |
| 2 | PI explicitly overrides a preference with named clause | PI applies |
| 3 | PI rule and skill content conflict on procedure | Skill wins on mechanics; PI wins on whether the skill runs |
| 4 | Text rule and CI workflow disagree on the same check | CI wins; flag drift as `[ASSUMPTION]` in the next session record |
| 5 | Audit script (level 2) and CI workflow (level 4) check the same thing | CI is authoritative; the level-2 script remains for local debugging |
| 6 | Two skills overlap on the same trigger | `[GAP]` — disambiguate explicitly in `skill-registry.md` |
| 7 | Architecture spec and PI conflict | Architecture wins on architectural rules (layer ownership, enforcement spectrum, where things belong); PI wins on project specifics (skill assignments, terminology, identity) |
| 8 | Bootstrap procedure in PI > 100 lines or runtime > 30s | Refactor: extract SQLite/state-query block to a `bootstrap-status` skill, leave thin caller in PI |
| 9 | A PI-referenced skill file doesn't exist | If labeled "placeholder" → OK (future hook); otherwise `[GAP]` — author the skill or remove the reference |
</conflict_resolution_examples>

<migration_and_growth>
**Adding a new feature to PI:**
1. Classify: preference-level (already covered by v6.1, don't restate) · project-specific (add to PI) · procedural (extract to skill) · architectural (add here).
2. Decide enforcement level. If level 2+, write the audit script as part of the change.
3. Update PI changelog.
4. If the change is workplan-level (affects multiple BPCs or rewrites a phase), write a DR in `decisions/` and reference it from the PI.

**Bootstrap or PI grows past target size:**
- Bootstrap >100 lines or runtime >30s → extract to skill
- PI >200 lines (current target; was 150 in v2.1) → audit for state content that should move to DRs, audit scripts, or the DB. PI should describe rules, not record state. Specific anti-patterns: "current state as of YYYY-MM-DD: N/M records...", banners for transient conditions, session-specific commentary.

**Shipping a new audit script:**
- Place at `scripts/audit/<name>.py` following the style in `<enforcement_spectrum>` above.
- Update `<enforcement_spectrum>` in this file with the new script entry.
- Reference from the corresponding PI standing rule.
- If blocking-in-CI: add job to `.github/workflows/ci.yml` or `.github/workflows/audit.yml`.

**Adopting a new DR:**
- File at `decisions/DR-YYYY-MM-DD-<slug>.md` following the style of existing DRs.
- If the DR sharpens or adds a standing rule: draft the corresponding PI bump in `governance/project-instructions-v10_X.md` and queue via `decisions/PI-update-needed.md`.
- The PI bump goes live only when the owner manually pastes the new content into claude.ai project settings — this layer is not API-writable.
</migration_and_growth>

<open_items>
- `[GAP: references/project-instructions.md still bears deprecation banner referencing "v10.4" (now v10.9). Stale banner should be updated, or file moved to _archived/.]`
- `[GAP: effort-guide.md is dated 2026-04-07 and contains skills from another project (Valoria cross-contamination: valoria-mechanic-audit, valoria-canon-guard, valoria-simulator, valoria-orchestrator, valoria-chunker). It also lacks adversarial-research, progressive-measurement, reasoning-doc-citations. Major refresh needed.]`
- `[GAP: skill-registry.md is from 2026-05-08 and references "Architecture v2.2"; needs refresh to v2.3 and to reconcile the "missing from repo / unclassified" lists against current state. toc-editor specifically should be removed from "deprecated" classification — it's actively maintained per PI rule #3.]`
- `[GAP: hook-workplan-guidebook.md referenced by PI v10.9 `<hooks_status>` does not exist. The concept ("Phase 1 hooks targeting 5 rules") was superseded by the CI workflows that actually shipped. Update PI to reference `.github/workflows/ci.yml` + `audit.yml` directly instead, or author a brief hook-workplan that documents the current state.]`
- `[GAP: ~80 of the 90+ files in references/ are one-off audit reports. Recommend a sweep to migrate dated audit reports to _archived/ to keep references/ navigable. Candidates: anything named *-audit-YYYY-MM-DD.md, *-report-YYYY-MM-DD.md, or with a "_2026-04-XX" suffix.]`
- `[ASSUMPTION: Guidebook continues to target only claude.ai chat with Code Interpreter — basis: no requirement has surfaced for API, Claude Code, or other surfaces. Revisit if scope changes.]`
- `[ASSUMPTION: Pre-commit hooks (level 5) remain deferred. Basis: single primary author + CI catches everything. Revisit when contributor count > 1.]`
</open_items>

<changelog>
- **V2.3 (2026-05-13)** — Major refresh after audit. Replaces stale v2.1 description of enforcement state ("all rules are level 1") with current reality: 15+ blocking CI checks across `ci.yml` and `audit.yml`. Enforcement spectrum expanded to five levels with concrete examples per level. Added cross-cutting `<layer_ownership>` description of audit scripts and CI workflows. `<reference_files_pattern>` updated for Phase A directories (`bpc-reasoning/`, `connection-reasoning/`, `keyword-compendiums/`) and notes the `references/` sprawl problem. `<bootstrap_exception>` acknowledges current ~70-line bootstrap as deliberate. `<skill_registry_pattern>` adds the placeholder convention (PI v10.9 uses this for 5 named-but-not-built skills). PI growth target raised from 150 → 200 lines. New examples #4–5, #8–9 in `<conflict_resolution_examples>`. `<open_items>` refreshed with current gaps and decisions log.
- **V2.2 (prepared but never committed)** — Referenced by `references/skill-registry.md` (2026-05-08) but no file was committed to repo. Content believed lost; v2.3 supersedes.
- **V2.1 (2026-05-07)** — Removed cross-references to other projects in ecosystem. Project-isolated.
- **V2.0 (2026-05-07)** — Split from generic spec into project-specific governance. XML tag wrapping. Identity at top, current state at bottom per Anthropic attention guidance.
- **V1.x** — Generic ecosystem-wide spec. Superseded.
</changelog>
