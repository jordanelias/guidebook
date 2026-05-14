# Project Architecture — Guidebook

This file describes how the Guidebook project is structured, where things belong, and how the layers interact. It governs and frames. It does not log specific issues, decisions, or session activity — that content lives in `decisions/`, `audits/`, `sessions/`, and git history.

---

<identity>
**Project:** Accessible Built Environments Guidebook — a reference document on architecture, accessibility, and built environment standards.
**Surface:** claude.ai chat with Code Interpreter.
**Repository convention:** single primary author; main branch protected by CI; data layer is authoritative.
</identity>

<layer_model>
Three runtime layers govern Claude's behavior. Outer wins by default; layers override only with explicit named clauses.

| Layer | Source | Scope |
|---|---|---|
| User preferences | `userPreferences-v*.md` | Cross-project |
| Project instructions (PI) | `governance/project-instructions-v*.md` | This project only |
| Skills + hooks + CI | `skills/`, `.github/workflows/`, `scripts/audit/` | Execution mechanics |

PI overrides preferences only via explicit clause naming the rule and scope. Skills override PI on mechanics; PI governs whether a skill runs and under what conditions. Code-enforced checks (hooks, CI) trump text rules for the matching invariant.

A cross-cutting **data layer** sits beneath all three: `data/guidebook.db` (canonical SQLite), schemas in `schemas/`, migrations in `scripts/migrations/`. The website and all derived artifacts read from this layer. Direct writes that bypass migrations are prohibited; CI enforces reproducibility.
</layer_model>

<reference_files_pattern>
The PI declares which reference files it expects. Each file has a single defined purpose. Reference files contain **rules, taxonomies, and structured registries** — not session activity, dated reports, or transient state.

Conventional locations:

| Directory | Contents |
|---|---|
| `references/` | Production reference material consumed by ongoing work |
| `audits/` | Audit reports (dated); `audits/_archived/` for resolved findings |
| `decisions/` | Decision records (DR-YYYY-MM-DD-slug.md) and transient deployment queues |
| `sessions/` | Per-session records and `sessions/LATEST` pointer |
| `workplan/` | Active workplans; `workplan/_superseded/` for retired plans |
| `_archived/` | Files removed from active circulation but preserved for git history |

When a reference file accumulates session-specific notes, dated commentary, or resolved-item logs, that content is extracted to the appropriate directory above. Reference files should read the same six months from now as they do today.
</reference_files_pattern>

<skill_registry_pattern>
PI declares skill *assignments* — one-line entries naming which skills the PI itself invokes. Detail (location, status, purpose, triggers, dependencies) lives in `references/skill-registry.md`.

Skill files are flat: `skills/<name>_SKILL.md`. Deprecated skills live in `skills/deprecated/` and are not loaded on trigger.

**Universality requirement.** A skill file describes a protocol Claude executes when invoked. The protocol is generic over inputs: it cites no specific session IDs, no specific dates, no commit SHAs, no specific gaps, no embedded changelog. Project-specific state that the skill operates on lives in the database or in DRs the skill references by stable identifier. If a skill cannot be authored without specific project state, the state belongs in the PI rule that invokes the skill, not in the skill itself.

**Placeholder convention.** When PI references a skill that does not yet have a file, the PI states "skill placeholder" or "no skill file exists" inline so the absence is intentional rather than a bug.

**Drift between PI references and `skills/` content** is reconciled in `references/skill-registry.md`, not in PI itself.
</skill_registry_pattern>

<enforcement_spectrum>
Rules live at one of five enforcement levels. Higher levels are more reliable but more expensive to author and maintain.

| Level | Mechanism | Where | Reliability |
|---|---|---|---|
| 1 | Text rule | PI standing rules, DRs, skill descriptions | Low |
| 2 | Audit script | `scripts/audit/*.py` (CLI, manual or scheduled) | Medium |
| 3 | CI workflow, non-blocking | `.github/workflows/*.yml` with `continue-on-error: true` | High |
| 4 | CI workflow, blocking | `.github/workflows/*.yml` with `continue-on-error: false` | Highest |
| 5 | Pre-commit hook (local) | `.git/hooks/` | Highest (local) |

**Promotion path.** New rules start at level 1 in PI standing rules. If the rule is mechanically checkable AND drift is observably costly, promote to level 2 by writing an audit script. If the rule must never drift in `main`, promote to level 4 by adding the audit script as a blocking job in CI. Pre-commit hooks (level 5) are deferred until contributor count exceeds one.

**Demotion path.** Audit scripts that haven't found an issue in 6 months may be downgraded to scheduled execution (e.g., weekly cron via GitHub Actions) rather than per-push, to reduce CI cost.

**Audit script style.** Module docstring lists checks numerically with rule provenance. Single `audit()` function with each check as a numbered SQL query or comparison. Reports formatted with `=` separators. Exit code 0 = pass, 1 = any issues found. Repository root resolved relative to `__file__` (no hardcoded absolute paths). DB path defaults to `data/guidebook.db` relative to repo root, overridable via `GUIDEBOOK_DB_PATH` environment variable to mirror `scripts/migrate_db.py`.
</enforcement_spectrum>

<data_layer_pattern>
The SQLite database at `data/guidebook.db` is the single source of truth for project content. Markdown files and JSON exports may derive from it but never compete with it.

**Schema discipline.**
- Schema changes ship as numbered SQL migrations: `scripts/migrations/NNN_<slug>.sql`. Forward-only. Tracked via `PRAGMA user_version`.
- Data changes ship as timestamped SQL migrations: `scripts/migrations/data_<YYYYMMDDHHMMSS>_<slug>.sql`. Forward-only, append-only. Tracked via the `data_migrations` table.
- The runner is `scripts/migrate_db.py`. It applies pending migrations on push and supports `--rebuild` for CI reproducibility verification.

**Reproducibility invariant.** The committed `data/guidebook.db` must be reproducible from its migration history. CI rebuilds a fresh DB by replaying all migrations and compares key invariants against the committed file. Any direct DB write that bypasses the migration framework fails this check.

**Schema documentation.** Pydantic schemas in `schemas/` mirror the SQLite layout. Drift between Pydantic and SQLite is a CI-detectable bug.

**FK integrity.** `PRAGMA foreign_keys = ON` at session start; `PRAGMA foreign_key_check` returns empty on a healthy DB. Migrations that bulk-load may toggle FK enforcement off within their script body and back on at exit, but must leave the DB in a referentially-consistent state.
</data_layer_pattern>

<bootstrap_pattern>
Each session loads project context via a bootstrap block at the start of the PI. The bootstrap pulls files from GitHub, queries `data/guidebook.db` for current state, and prints a status summary.

**Constraints.**
- Halt on critical fetch failure; log `[GAP: <filename> — not present]` on non-critical failure.
- Total runtime budget: under 30 seconds. Total line count: under 100 lines.
- Use `gh` CLI when available; fall back to `curl` with PAT.

When bootstrap grows past these budgets, extract the heaviest portion (typically SQLite state queries) to a `bootstrap-status` skill and leave a thin caller in PI.

**Bootstrap-exempt operations.** Pure governance work on PI / preferences / architecture themselves; tooling questions not touching repo state; workflow conversations that do not touch repo content.
</bootstrap_pattern>

<conflict_resolution>
| # | Situation | Resolution |
|---|---|---|
| 1 | Preference says X, PI silent | Preference applies |
| 2 | PI explicitly overrides a preference with named clause | PI applies |
| 3 | PI rule and skill content conflict on procedure | Skill wins on mechanics; PI wins on whether the skill runs |
| 4 | Text rule and CI workflow disagree on the same check | CI wins; record drift as `[ASSUMPTION]` in the next session record |
| 5 | Audit script (level 2) and CI workflow (level 4) check the same thing | CI is authoritative; the level-2 script remains for local debugging |
| 6 | Two skills overlap on the same trigger | `[GAP]` in `skill-registry.md` — disambiguate explicitly |
| 7 | Architecture spec and PI conflict | Architecture wins on architectural rules (layer ownership, enforcement spectrum, where things belong); PI wins on project specifics (skill assignments, terminology, identity) |
| 8 | Bootstrap procedure exceeds 100 lines or 30s runtime | Refactor: extract SQLite/state-query block to a `bootstrap-status` skill, leave thin caller in PI |
| 9 | A PI-referenced skill file doesn't exist | If labeled "placeholder" → OK (future hook); otherwise `[GAP]` — author the skill or remove the reference |
</conflict_resolution>

<migration_and_growth>
**Adding a feature to PI.** Classify: preference-level (covered by user preferences, don't restate) · project-specific (add to PI) · procedural (extract to skill) · architectural (add here). Decide enforcement level. If level 2+, write the audit script as part of the change. If the change is workplan-level (affects multiple BPCs or rewrites a phase), write a DR in `decisions/` and reference it from the PI.

**PI growth.** PI standing rules describe rules, not state. State content — "current AUTHOR-TITLE-ONLY counts," retraction banners, session-specific commentary — belongs in DRs, audit scripts, or the DB. When PI exceeds its size budget, audit for state content that should move out. The budget is set in the PI itself, not here.

**Bootstrap growth.** When bootstrap exceeds its budgets in `<bootstrap_pattern>`, extract to a skill.

**Shipping a new audit script.** Place at `scripts/audit/<name>.py` following the style in `<enforcement_spectrum>`. Reference from the corresponding PI standing rule. If blocking-in-CI, add a job to the appropriate workflow.

**Adopting a new DR.** File at `decisions/DR-YYYY-MM-DD-<slug>.md`. If the DR sharpens or adds a standing rule, draft the corresponding PI bump in `governance/project-instructions-v<next>.md` and queue via `decisions/PI-update-needed.md`. The PI bump goes live only when the owner manually pastes the new content into claude.ai project settings — this layer is not API-writable.

**Retiring content.** Move to `_archived/` rather than delete. Preserves git history while reducing namespace noise. Subdirectories under `_archived/` mirror the origin location.
</migration_and_growth>

<scope_assumptions>
The architecture currently assumes a single primary author, single deployment surface (claude.ai chat), and no concurrent contributors. Pre-commit hooks (level 5 enforcement), multi-surface PI specialization, and contributor-coordination mechanics are out of scope until those assumptions change.
</scope_assumptions>
