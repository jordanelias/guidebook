# CLAUDE.md — Guidebook working guide for Claude Code

This file orients a fresh Claude Code session to this repository: what it is, how it is
governed, what will block your commits, and how to do work here without breaking the
apparatus. **Read it fully before your first edit.**

> **This file is a derived map, not a source of truth.** The authoritative sources are
> `references/project-standards.md`, the governance docs under `governance/`, and the
> Decision Records under `decisions/`. Where this file disagrees with them, *they win* —
> and this file should be corrected. The single canonical data source is the SQLite
> database `data/guidebook.db`; every count, value, or list in prose (including here) may
> be stale. When a number matters, query the DB.

---

## 0. TL;DR — the non-negotiables (CI blocks these)

Two GitHub Actions workflows gate `main` (`.github/workflows/ci.yml`, `audit.yml`). Before
you commit or push, know these five rules. Details in §7–§8.

1. **Commit message format.** `{skill-name}: {action} [YYYY-MM-DD HH:MM]` — the timestamp
   must be the **last** bracket on the line. Get it with `date -u '+%Y-%m-%d %H:%M'`.
   For work with no specific project skill, use `governance` as the skill-name.
2. **Doctrine token.** Any commit touching a *synthesis path* — `references/bpc-reasoning/`,
   `references/connection-reasoning/`, `decisions/`, or `sessions/` — must add
   `[DOCTRINE: <7-hex>]` **before** the timestamp, matching the current doctrine SHA:
   `git rev-parse HEAD:governance/mission-and-epistemics.md | cut -c1-7`.
   Canonical form: `{skill}: {action} [DOCTRINE: <sha>] [YYYY-MM-DD HH:MM]`.
3. **Attestation.** The same synthesis-path commits must add/update
   `attestations/<artifact-slug>.json`, valid against `schemas/attestation.schema.json`
   (backfill-on-touch: the first edit of a grandfathered artifact creates its attestation).
4. **Never write `data/guidebook.db` directly.** All DB changes ship as migrations via
   `scripts/emit_data_migration.py`; CI rebuilds the DB from migration history and fails on
   any divergence (§6). Direct writes (including ad-hoc `scripts/db.py` writes to the
   committed DB) break the reproducibility gate.
5. **Structural renames/removals aren't done until the caller sweep is done.** Renaming or
   deleting any identifier, path, tag, heading, schema column, table, or skill name requires
   searching all non-archived callers and fixing every one (per
   `architecture/project-architecture-guidebook-v2.3.md` `<migration_and_growth>`).

**You are Claude Code operating on a local clone.** The repo's Project Instructions and
`scripts/bootstrap.sh` target a *different* surface (claude.ai chat + Code Interpreter) and
are **PAT-gated / fetch from the remote** — do **not** run the bootstrap. Orient locally
instead: read the current plan (§9), query the DB, run the validators (§7).

---

## 1. What this project is

The **Accessible Built Environments Guidebook** — a reference on architecture, accessibility,
and built-environment standards centred on **disabled people**. Its stance is fixed doctrine:
it is a **thinking tool and advocacy project, not an authority** — "the purpose of this
guidebook is to get people to ask the right questions." It is not a prescription manual, not
a legal authority, and not a substitute for professional judgment. ("Inclusive / accessible /
universal" in this repo always means *inclusion of persons with disabilities* — no
design-for-everyone framing.)

- **Maturity:** pre-launch, single primary author (`@jordanelias`). The governance, schema,
  and tooling are elaborate and real; **the synthesized content is ~1% populated.** Today
  `bpc_metadata` shows **0 of 82** BPCs `COMPLETE` and 62 `RETRACTED-PRE-REHAB`. The project
  is parked mid-rehabilitation (Phase B / pilot Phase E — see §9). Treat it as scaffolding
  under active construction, not a finished book.
- **Repo:** `jordanelias/guidebook`, default branch `main` (protected by CI).
- **Two product front-ends exist and are different things:** the hand-authored mockup
  (`index.html` + `assets/guidebook.css`, showing the *intended* end-state — every provision
  link is dead except the `specs/e-08.html` exemplar) versus the actually-generated static
  site under `site/` (thin, real, full of honest "not yet computed" banners). Don't confuse
  the mockup for output.

## 2. Mental model: the layers

From `architecture/project-architecture-guidebook-v2.3.md`. Outer layer wins unless an inner
layer names an explicit override; code-enforced checks trump text rules for the matching
invariant.

| Layer | Where | Scope |
|---|---|---|
| User preferences | `userPreferences-v*.md` (not in repo; lives in claude.ai) | cross-project |
| Project Instructions (PI) | `governance/project-instructions-v*.md` | this project |
| Skills + hooks + CI | `skills/`, `.github/workflows/`, `scripts/audit/` | execution mechanics |
| **Data layer (beneath all)** | `data/guidebook.db` + `schemas/` + `scripts/migrations/` | source of truth |

**The DB is authoritative.** Markdown "parts", the HTML site, JSON/YAML registries, and
reasoning docs *derive from or feed* the DB; they never outrank it. When two stores disagree,
the DB is canonical and the other is the thing to reconcile/retire.

Rules live on a 5-level **enforcement spectrum**: (1) text rule → (2) audit script → (3) CI
non-blocking → (4) CI blocking → (5) pre-commit hook (none installed; single author). Promote
a rule up the spectrum only when it's mechanically checkable and drift is costly.

## 3. Repository map

| Path | Contents |
|---|---|
| `governance/` | Doctrine + protocols. `mission-and-epistemics.md` (**the doctrine**, SHA-tracked), `evidence-architecture.md`, `tier-system.md`, `conceptual-model.md`, `decision-protocol.md`, `doctrine-recheck.md`, `pipeline-contract.yaml`, `project-instructions-v10_14.md` (latest PI). CODEOWNERS-protected. |
| `references/` | Working corpus (~440 files). `project-standards.md` + `skill-registry.md` are the two most-loaded files. Also `bpc/`, `bpc-reasoning/`, `connection-reasoning/`, `fdr/`, `search-log/`, `audit-briefs/`, `conflict-matrices/`, registries. |
| `decisions/` | Decision Records `DR-YYYY-MM-DD-slug.md` — the governance changelog. Read the recent ones (§9). |
| `attestations/` | `*.json` adherence-log attestations (see §8). |
| `schemas/` | Pydantic v2 models mirroring the SQLite layout + `attestation.schema.json`. CODEOWNERS-protected. |
| `scripts/` | Tooling. `migrations/` (canonical schema+data SQL), `audit/` (enforcers), `validate_*.py`, `db.py`, `generate/`. Both protected subdirs. |
| `data/` | `guidebook.db` (canonical) + entity YAML subdirs (`decisions/`, `adversarial_use/`, `doctrine_recheck/`, `jurisdictional_values/`). |
| `parts/` | The guidebook as chaptered markdown (`parts/v10/part00–13`), machine-generated stubs — do not hand-edit. |
| `site/` | Generated static site (`specs/`, `populations/`, `rooms/`). Generated — do not hand-edit. |
| `audits/`, `workplan/`, `sessions/` | Dated audit reports; active + superseded workplans; per-session records. |
| `_archived/` | Retired-but-preserved content (mirrors origin paths). Retire *here*, don't delete. |
| `.github/workflows/` | CI (see §7). CODEOWNERS-protected. |

## 4. The data layer (how to change data safely)

`data/guidebook.db` — SQLite, ~5.3 MB, committed as a binary blob (`.gitattributes`, **not**
Git-LFS). **`PRAGMA user_version = 28`** is the authoritative schema version. (The
`db_meta.schema_version` row says `21` — that's a stale 2026-05-08 artifact; ignore it.)
There is **no `sqlite3` CLI** in this environment — use Python, read-only:

```python
import sqlite3
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
```

**Backbone (42 tables, 9 views).** Two axes — `items` (design parameters, `item_code`
`A-01…K-NN`, 93 rows) × `populations` (disability population codes, self-referencing
`parent_code`, 22 rows) — meet in **`evidence_cell_state`**, the per-(item×population)
synthesis cell (`state` ∈ `stated`/`provisional`/`pending`/`not_applicable`). Evidence lives
in **`evidence_sources`** (`ref_id` `REF-NNNNN`, 804 rows; `tier` 1–6 and `evidence_type` are
orthogonal) and attaches through `source_slug_links` → `slugs` (research units, 82) and
directly via `evidence_population_match`, `reasoning_doc_citations`, `spec_value_probes`,
`source_value_extractions`, `jurisdictional_values`. `gaps` (299; 37 open) is the gap register.
`decisions` in the DB is **empty scaffolding** — canonical decisions live in
`data/decisions/decision_register.yaml`.

**Changing the data model:**

- **Schema change** → new `scripts/migrations/NNN_slug.sql` (forward-only, bump
  `user_version`) **and** mirror it in the matching `schemas/*.py` Pydantic model (drift is a
  CI-caught bug). Enum changes are a schema **Decision** (D-SCHEMA) — Change-Order gated.
- **Data change** → generate a migration, never hand-edit the DB or an existing `data_*.sql`:
  ```
  python3 scripts/emit_data_migration.py --session <session-id> --summary "<what>" --input changes.sql
  python3 scripts/migrate_db.py            # apply pending
  ```
  Data migrations are **append-only and immutable once committed** — fix forward with a new
  compensating migration. They're tracked in the `data_migrations` table; schema migrations by
  `user_version`. `012_baseline_2026-05-15.sql` is a baseline that supersedes 001–011.
- **Verify reproducibility** before pushing DB changes:
  `python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db` (this is what CI does).
- **Exempt tables** (written by scheduled jobs outside migrations, per DR-2026-05-28):
  `evidence_source_authors`, `pipeline_runs`. Don't add to that list without a DR.

`scripts/db.py` is the read/query workhorse (library + ~30-subcommand CLI). Use it to *read*
freely; route any *write* to the committed DB through a migration.

## 5. Governance & doctrine (the crux of this repo)

Every substantive change is a governed act. The pieces:

- **Doctrine:** `governance/mission-and-epistemics.md` — CANONICAL, amended in place (its SHA
  is what commit tokens and attestations bind to). `references/project-standards.md` is the
  **append-only operative rule ledger** (managed by the `session-consolidator` skill) and is
  usually *ahead of* the PI on doctrine — prefer it and the recent DRs over older PI text.
- **Decision Records:** `decisions/DR-*.md`, protocol in `governance/decision-protocol.md`.
  Categories D-DOCT / D-METH / D-SCHEMA / D-OP / D-PRES; delegation DG-NON / DG-REVIEW /
  DG-AUTO. **DG-NON (owner-only, you propose — you do not decide):** mission/audience/CRPD
  posture, population taxonomy, evidence-tier definitions, jurisdiction and work-product
  inclusion/exclusion, Co-1 corpus, licensing, trajectory. Validator: `scripts/decision_capture.py`.
- **Attestations:** `attestations/*.json` (§8).
- **Doctrine recheck:** `governance/doctrine-recheck.md` — fires every 25 working sessions, at
  stage transitions, and on any doctrinal-rule revision. `scripts/doctrine_recheck.py`.
- **Owner-gating:** file moves/retirements and all DG-NON decisions need owner sign-off.
  "When you know better, you do better" — but for irreversible or structural moves, **propose;
  don't unilaterally execute.**

## 6. Evidence & content model (brief — read the governance docs for depth)

- **Evidence hierarchy** (`governance/tier-system.md`, OPERATIVE): **T1** primary controlled
  research · **Co-1** lived experience/participatory design (co-primary with T1, CRPD Art. 4.3)
  · **T2** synthesis (systematic reviews/meta-analyses + named-org evidence-based standards) ·
  **Co-2** OT professional-body CPGs (co-primary with T2) · **T3** lower-control/grey primary
  (supporting; T3-alone never reaches `stated`) · **T4** international standards · **T5**
  national frameworks · **T6** statutory codes. **T4–T6 are the "regulatory stratum," walled
  off from best-practice anchoring** — *convergence across codes is not evidence*. Per the
  weighted-strength model (2026-07-20) + "Option A" (2026-07-21), a code-consensus best-practice
  claim is a **weak-band (○)** claim, always flagged code-derived; rendered unflagged or above
  the weak band it is *in error*.
- **Evidence markers** (tier-system §5): **●** confirmed evidence base · **◐** policy/standards
  basis only (T4/T5) · **○** grey/expert-consensus/thin/T6. Every spec sentence carries one;
  unmarked = error. (Note: `mission-and-epistemics.md` still describes a two-marker ●/○ scheme —
  a known reconciliation drift; `tier-system.md` is operative.)
- **Design Modes:** Universal (code compliance, fixed values) / Population (ranges, median
  default) / Person (OT co-design; population informs but does not bound the individual). DAR
  (Design for Adaptable Readiness) is mandatory at all modes.
- **Evidence-state machine** (per cell): `stated` / `provisional` / `pending`
  (`[BEST-PRACTICE-PENDING]` + gap link) / `not_applicable`. `stated`/`provisional` require
  non-empty `governing_refs`.
- **Item codes** `A-01…K-NN` (category J deliberately struck) are **distinct** from entity-type
  codes `ENT-01…ENT-20` in `governance/conceptual-model.md` — those were renamed from `E-##` on
  2026-07-21 precisely to end the collision (`ENT-08` = the *Item* entity type; `E-08` = the
  *Corridor Clear Width* parameter). Don't conflate them.
- **BPC** = Best Practice Compendium. Per-slug synthesis at `references/bpc/<topic>/<slug>.md`;
  the audit-trail/reasoning behind it at `references/bpc-reasoning/<slug>.md` (the workplan's
  primary deliverable — currently ~1% written); connection reasoning at
  `references/connection-reasoning/<con-id>.md`.
- **Synthesis routing (hard floor, PI rule #2 + DR-2026-06-10):** only **Opus-class** models
  write `best_practice_synthesis`. Lower-tier models do inventories, verification, multilingual
  search, and 9-step comparison tables, then queue the doc for an Opus session. If you're not
  Opus-class and asked to author synthesis, say so and stop at the queue boundary.
- **Citation discipline:** sources confirmed real ("I don't know" > invention); two failed
  searches → `CLOSED-DELETED`; quantified claims need DOI + page/table (or direct URL) else
  `[UNVERIFIED-QUANT]`.

**Pipeline** (`governance/pipeline-contract.yaml`, PROPOSED/advisory): research → collection →
judgment → synthesis → render, over the spine EvidenceSource → BPC entry → Specification → Item
→ render. The content workplan (`audits/bpc-rewrite-workplan-2026-05-11.md`) runs phases **A–G**
with a **strict "B before E"** gate: no BPC is rewritten (Phase E) until its linked sources pass
Phase B verification.

## 7. Running things (setup, validators, tests)

**Environment setup (do this first).** `PyYAML` is present but **`pydantic` and `jsonschema`
are not** — the schema/governance validators import `schemas/*.py` and will `ModuleNotFoundError`
until you install deps (CI installs them per-job):

```
pip install -r requirements.txt      # pydantic==2.13.3, PyYAML==6.0.3
pip install jsonschema                # only needed for attestation audits
```

Every DB-aware script honours `GUIDEBOOK_DB_PATH` (default `data/guidebook.db`). There's no
"run all" wrapper; CI runs discrete steps. The ones you'll actually use:

| Command | Purpose | Deps |
|---|---|---|
| `python3 scripts/validate_bpc.py --all --verbose` | BPC file structure | stdlib |
| `python3 scripts/validate_cross_refs.py --repo-root .` | cross-reference integrity | stdlib |
| `python3 scripts/tests/test_db_integrity.py` | 35 DB checks (FK/enum/consistency) | stdlib |
| `python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db` | rebuild DB from migrations (repro check) | stdlib |
| `python3 scripts/validate_schema.py --verbose` (`--cross-check`) | entity YAML vs Pydantic | pydantic |
| `python3 scripts/validate_evidence_state.py` | cell-state machine + Co-1 fields | pydantic |
| `python3 scripts/audit_evidence_metadata.py` | rule-#10 evidence-eligibility gate | pydantic |
| `python3 scripts/decision_capture.py` · `doctrine_recheck.py --cross-ref` | governance audits | pydantic |

Tests are **standalone scripts, not pytest** (`python3 scripts/tests/<name>.py`, each prints
`RESULTS: X/Y` and exits 0/1). Only `test_db_integrity.py` is wired into CI.

**CI workflows** (both trigger on push to `main` and PRs to `main`):
`ci.yml` — 6 jobs: syntax, structure, commit-msg (push-only), schema, `db_integrity` (blocking),
governance. `audit.yml` — `source_slug_links` duplicates, citation-mining completeness (reads
`sessions/LATEST`), **migration reproducibility** (blocking; 7 invariants), and attestation
schema/presence (blocking). Several jobs are path-gated: a PR that touches only docs (like this
file) runs just `syntax` + `structure` + the `audit.yml` jobs.

> **CI is currently RED on `main` — this predates you; don't assume your change caused it.**
> On the latest `main` run, three jobs fail: **commit-msg** (the merge-commit subject can't
> match the `{skill}: {action} [ts]` format — every PR merge trips this), **`db_integrity`**
> (`test_db_integrity.py` fails ~26/35 against the committed DB: a mix of *stale hardcoded enum
> allowlists in the test* — the DB legitimately contains newer `verification_status` /
> `metadata_quality` / `source_type` / `gaps.status` values — and *real data-invariant debt*),
> and the **schema** job's `validate_evidence_state.py` step. Fixing these is unscoped
> owner-gated work (it touches CODEOWNERS-protected `scripts/` and DB data); don't fold it into
> an unrelated change. Also note `scripts/validate_db.py` is outright broken against the current
> schema (`no such column: doi_less_key`) — prefer `test_db_integrity.py` for DB health.

## 8. The commit + attestation workflow (walkthrough)

For a routine, non-synthesis change (docs, tooling, a script):

```
{skill-name}: {action} [YYYY-MM-DD HH:MM]
# e.g.  governance: add CLAUDE.md onboarding guide [2026-07-21 18:40]
```

The format check (`scripts/ci_helpers/check_commit_msg.py`) requires:
`^[a-z][a-z0-9_-]+:\s+.+\s+\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\]$` — lowercase-hyphenated prefix,
timestamp as the **final** bracket.

For a **synthesis-path** change (`references/bpc-reasoning/`, `references/connection-reasoning/`,
`decisions/`, `sessions/`) you additionally must:

1. **Add the doctrine token before the timestamp:**
   `SHA=$(git rev-parse HEAD:governance/mission-and-epistemics.md | cut -c1-7)` →
   `{skill}: {action} [DOCTRINE: $SHA] [YYYY-MM-DD HH:MM]`.
   Exempt when the commit itself modifies `governance/mission-and-epistemics.md` (then
   re-attest affected downstream artifacts within `RE_ATTESTATION_WINDOW` = 5 commits or by
   next session close). Bots and merge commits are exempt.
2. **Add/update `attestations/<artifact-slug>.json`** against `schemas/attestation.schema.json`.
   Required fields: `schema_version`, `session`, `artifact`, `doctrine_sha`, `rules_in_scope`
   (stable rule identifiers from `references/skill-registry.md`, not numbers), `per_rule_status`
   (each `FIRED` needs an `evidence_path`; each `SKIPPED` needs a `reason`), `deviations`,
   `bias_direction` (≥30 chars), `independent_reviewer_counterclaim` (≥30 chars), `verdict`
   (`CLEAN`/`DEVIATION-LOGGED`/`NON-COMPLIANT`/`REVERT`). The optional `reattestation[]` log is
   forward-only — never rewrite a prior entry.

**Push protocol:** develop on your assigned branch, `git push -u origin <branch>`, then open a
PR against `main` (ready for review). Never commit secrets — a redacted PAT lives in the PI's
repo-side copy and GitHub push-protection is on.

## 9. Current state, active work & guardrails

The live plan is **`workplan/consolidation-execution-plan-2026-07-21.md`** — a consolidation
push (execute already-ratified archival; retire md/yaml/json shadows in favour of the DB;
finish the re-attestation mechanism; de-duplicate doctrine statements). Recent doctrine motion
is in the 2026-07 DRs: entity-code rename, evidence-architecture "Option A" (weak-band code
consensus), weighted-strength anchor model, product-posture ("thinking tool, not authority"),
and re-attestation materiality. Read those DRs before touching evidence/tier/attestation logic.

**Guardrails carried from that plan (they encode failure modes already hit):**

1. **Re-verify every "divergence" claim against *current* files before acting.** Older audits
   describe a moving repo; a prior doc's stale anchor caused a real error.
2. **Redirect-stub, never delete, anything still referenced** (e.g. `mission-PROVISIONAL.md`,
   connection registers). Retire to `_archived/`, mirroring the origin path.
3. **Don't spin up a new register/sweep** — extend the existing 2026-07-12 apparatus.
4. **Owner-gate file moves and retirements.**
5. **Prefer the DB.** When two stores disagree, the DB is canonical; reconcile then retire the
   shadow (treat disagreements as findings, not silent overwrites).

## 10. Gotchas / trip-hazards

- **Prose counts are stale everywhere** (`index.html`, `parts/*/manifest.md`, older audits
  disagree with each other and with the DB). Query the DB; never trust a hardcoded number.
- **Stale pointers:** `sessions/LATEST` and `sessions/handoff-next-session.md` both point at
  old sessions. The current handoff is the consolidation plan above. (`audit.yml` reads
  `sessions/LATEST` for its citation-mining check — a known wrinkle, not something to "fix" ad hoc.)
- **PI versioning is intentional:** `project-instructions-v10_7…v10_13` are historical snapshots;
  `v10_14` (2026-05-20) is the deployed one. The PI is not API-writable — the owner pastes it
  into claude.ai — so the repo PI legitimately lags current doctrine. Don't "fix" the multiple
  versions; don't treat PI text as more current than `project-standards.md` + recent DRs.
- **`schemas/*.py` ↔ SQLite drift is a bug, not a convention** — keep them in sync when you
  change either.
- **Don't hand-edit generated output** (`parts/`, `site/`) — edit the DB / reasoning docs and
  regenerate (`scripts/generate_parts.py`, `scripts/generate/*.py`).
- **`skills/*_SKILL.md` are project-domain skills** (authoring protocols keyed by
  `references/skill-registry.md`), *not* Claude Code harness skills. Renaming one is a governed
  event (attestations reference the stable identifiers).
- **Don't run `scripts/bootstrap.sh`** (PAT-gated, remote-fetching; for the claude.ai surface).
- **Don't run `scripts/init_db.py`** expecting a working DB (it applies only migration 001) —
  use `migrate_db.py --rebuild`.

## 11. Where to read for depth

| Question | Read |
|---|---|
| The whole architecture / where things belong | `architecture/project-architecture-guidebook-v2.3.md` |
| The doctrine (mission, epistemics, evidence commitments) | `governance/mission-and-epistemics.md` |
| Current operative rules (append-only ledger) | `references/project-standards.md` |
| Evidence tiers, markers, weighted strength | `governance/tier-system.md`, `governance/evidence-architecture.md` |
| Entity model / ENT-## codes | `governance/conceptual-model.md` |
| Decision process | `governance/decision-protocol.md`; recent `decisions/DR-2026-07-*.md` |
| Attestation / re-attestation | `schemas/attestation.schema.json`; `governance/doctrine-recheck.md`; `governance/doctrine-deltas.json` |
| Data-model / schema reconciliation | `architecture/schema-spec.md`, `architecture/schema-reconciliation.md`, `architecture/sqlite-data-layer.md` |
| Content pipeline / phases A–G | `audits/bpc-rewrite-workplan-2026-05-11.md`; `governance/pipeline-contract.yaml` |
| Skill roster | `references/skill-registry.md` |
| What to do next | `workplan/consolidation-execution-plan-2026-07-21.md` |

*This guide reflects the repository as of 2026-07-21. Verify volatile facts (doctrine SHA, DB
counts, CI status, the active plan) against the live repo — the commands to do so are above.*
