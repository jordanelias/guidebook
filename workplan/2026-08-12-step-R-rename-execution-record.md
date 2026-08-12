# Step R — execution record: `cell` → `specification`

**Owner ruling, 2026-08-12:** the (item × population) determination is a **specification**, not a
"cell". Executed here. This record exists because a rename is not done when the DB is renamed — it
is done when every caller is fixed and every deliberate non-sweep is named
(`CLAUDE.md` §0 rule 5; architecture v2.3 `<migration_and_growth>`).

---

## 1. What was renamed

| Old | New |
|---|---|
| `evidence_cell_state` | `specifications` |
| `cell_source_links` | `specification_source_links` |
| `evidence_cell_state.cell_id` | `specifications.specification_id` |
| `cell_source_links.cell_id` | `specification_source_links.specification_id` |
| `idx_cell_state_item` / `_pop` / `_state` | `idx_specifications_item` / `_pop` / `_state` |
| `idx_cell_source_links_ref` | `idx_spec_source_links_ref` |

Both tables held **0 rows** at rename time (2026-08-06 clean-room reset plus this session's
evidence-stage clearance), so no row was moved and none could be lost.

Seven dependent views (`v_pending`, `v_divergence`, `v_code_floor_only`, `v_best_practice`,
`v_item_provenance`, `v_source_reach`, `v_source_reach_all`) were rewritten automatically by
SQLite 3.45.1 under `legacy_alter_table=0`; 18/18 views still execute and
`PRAGMA foreign_key_check` returns 0.

---

## 2. The ordering defect this uncovered — and why the DDL is in a data migration

The first draft shipped the ALTER statements in `scripts/migrations/055_rename_cell_to_specification.sql`
and asserted in its own comment that "replay is chronological, so [the old-name migrations] run first
and this renames after."

**That was false, and `migrate_db.py --rebuild` proved it:**

```
sqlite3.OperationalError: no such table: evidence_cell_state
```

`migrate_db.py` applies **all** numbered schema migrations first, then **all** data migrations in
timestamp order. It does not interleave them by date. **19 committed, immutable data migrations
write to the old names** — from `data_20260712150000_jurisdictional-values-backfill.sql` through
`data_20260806222208_2026-08-03-clean-room-reset.sql` — so a rename in the schema phase runs *before*
them and breaks replay.

The repository has hit this collision before, from the opposite side. `scripts/migrations/025_drop_colonial_role.sql`
records it verbatim: *"The CHECK cannot be tightened while that migration's COLONIAL inserts remain
in replay (CI rebuilds schema-before-data), hence the withdrawal."* Migration 025 resolved it by
withdrawing a single same-day data migration. **Withdrawal is not available across 19 migrations
spanning two months.**

**Resolution.** The change is split:

- `scripts/migrations/055_rename_cell_to_specification.sql` — **version marker only**. Keeps
  `PRAGMA user_version` honest as the authoritative schema-version marker and reserves 055 so a
  future 056 is not silently skipped by the runner's version-based pending detection.
- `scripts/migrations/data_20260812075349_2026-08-12-rename-cell-to-specification.sql` — the DDL,
  timestamped after all 19, so it renames only once they have replayed.

DDL inside a data migration has precedent: `data_20260525013000_supersession_v1_stamp_correction.sql`
runs `ALTER TABLE ... ADD/DROP/RENAME COLUMN` for the same class of reason (a schema constraint
blocking a data correction).

**Verified after the split:** rebuild succeeds; committed DB and rebuilt DB agree on
`PRAGMA user_version` (55), on every `sqlite_master` object *including its SQL text* (0 differences
either direction), and on row counts across every shared table (0 divergences).

---

## 3. Callers swept

**23 live `.py` files, 221 token replacements** across `schemas/`, `scripts/`, `tools/`. All parse.

**Configuration and prose (live surfaces):**

| File | Change |
|---|---|
| `scripts/audit/graph/known_debt.yaml` | `table:` and `lift_when_sql:` repointed — these are **executed**, and a stale `lift_when_sql` degrades to a `known_debt.unsound` WARN rather than an error. Entry `id` deliberately kept stable so its paper trail survives; the rename is noted in-file |
| `governance/check-registry.yaml` | one prose mention in a check `note:` |
| `governance/context-map.yaml` | regenerated (`scripts/generate/context_map.py`) |
| `governance/pipeline-operations.md`, `governance/research-contract.yaml` | table references |
| `references/tooling-register.md`, `references/methodology-evidence-hierarchy-mapping.md`, `references/methodology/intra-category-cross-test-methodology.md` | table references |
| `skills/cell-curator_SKILL.md`, `skills/item-specification-writer_SKILL.md` | table references and the surrounding "cell" prose |
| `CLAUDE.md` | §1 and §4, with the old name retained once as a pointer |

**Generated output, regenerated rather than edited:** `parts/v10/*` (`generate_parts.py`),
`site/specs/*` (`generate/build_site.py`), six of eleven `site/populations/*`
(`generate/population_page.py`), `tools/pipeline-completeness-dashboard.html`
(`tools/pipeline_completeness.py`), `governance/context-map.yaml`.

---

## 4. The near-miss: a blind sweep changed a selector, not a reference

`scripts/tests/test_validate_evidence_state_2_4.py` discovers its fixture DDL by scanning the
numbered migration files for a **literal table name**. The token sweep rewrote that selector to
`"specifications"` — a string that appears in **no** numbered migration, because migrations are
immutable and still say `evidence_cell_state`. The selector then matched only on
`convergence_assessment`, silently collected a *different* file set, and the test died with
`table "gaps" already exists`.

**This is W6.6's defect class** (a regex classification treated as a finding) reaching the sweep
itself: a string that must match *historical, immutable* text is not a reference to be renamed.

It was caught only by baselining the check suite at `df64417` in a worktree and diffing the failure
sets — the test **passes at baseline and failed with the change**. Running the suite once and
observing "the same things fail" would have missed it, because the failure list is long.

**Fixed** by restoring the selector to the historical name and replaying the rename onto the fixture
(`_apply_055()`), applied only to objects the collected DDL actually created, so it stays correct if
the file set changes. `scripts/tests/test_evidence_cell_state_2_3.py` got the same treatment against
migration 024.

### 4b. Two latent fixture defects the rename surfaced

Neither is caused by the rename; both were invisible until a rename forced SQLite to re-parse views.

1. **`test_validate_evidence_state_2_4`'s stub `gaps` table was `gap_id` only**, while `v_pending`
   selects `g.description`, `g.category`, `g.priority`. Stubbed out properly.
2. **The fixture's partial schema cannot compile several shipped views** (`v_item_provenance` needs
   `evidence_sources`, which the fixture never creates). They had been carried as dead definitions;
   a rename turns them into hard errors. They are now dropped before the rename, with the reason
   recorded in the file.

---

## 5. Deliberately not swept

| Path | Reason |
|---|---|
| `scripts/migrations/*.sql` (28 files) | **Immutable.** They correctly describe the schema on their date |
| `_archived/`, `audits/`, `sessions/`, `workplan/_superseded/`, `decisions/`, `attestations/`, `working/` | Frozen records; true on their date. Rewriting them would forge the paper trail (guardrail 2, and the `.ignore` rationale in `DR-2026-08-06-cold-storage-search-scope.md`) |
| `architecture/schema-spec.md` | Describes an **aspirational** `cell` table with a `TEXT` `cell_id` of the form `CELL-{spec_id}-{population_code}` — a design that never shipped. Renaming there would assert a correspondence that does not exist. Belongs to `architecture/schema-reconciliation.md`, not to this rename |
| `architecture/consolidation-remediation-roadmap-2026-07-12.md` | Dated roadmap; one historical mention |
| `scripts/migrate/init_database.py` | Legacy one-time code, already out of scope for the `GUIDEBOOK_DB_PATH` contract (`scripts/{db,migrate,probes,test}/**`) |
| `scripts/tests/test_evidence_cell_state_2_3.py` (filename) and check id `test_evidence_cell_state_2_3` | The file tests migration 024 by name. Renaming it is registry churn with no gain; the check id is the more stable identifier |
| `skills/cell-curator_SKILL.md` (skill name) | **Owner-gated.** Skill identifiers are cited by two committed attestations; renaming one is a governed event |
| `site/populations/{dbl,neu,ofs,upl,vis}.html` | See §6 |

---

## 6. Finding: five orphaned population pages

`site/populations/` holds eleven pages. **Five name population codes that no longer exist** — `DBL`,
`NEU`, `OFS`, `UPL`, `VIS` — retired by the 2026-07-23 population-schema replacement. Their
generator refuses them (`ERROR: Population 'VIS' not found.`), so they cannot be regenerated and
still carry the pre-rename table name.

This predates the rename. `build_site.py` states its own scope honestly — it drives `site/specs/`
only — so nothing has been regenerating these. **Deleting them is a retirement and therefore
owner-gated** (guardrail 4). Recorded here rather than executed.

---

## 7. Verification

| Gate | Result |
|---|---|
| `migrate_db.py --rebuild` | succeeds (44 schema + 292 data migrations) |
| committed vs rebuilt | `user_version` 55 = 55 · 0 `sqlite_master` object differences either direction · 0 row-count divergences |
| `scripts/tests/test_db_integrity.py` | **70/70** |
| `scripts/tests/test_evidence_cell_state_2_3.py` | ALL PASS (0 failed) |
| `scripts/tests/test_validate_evidence_state_2_4.py` | ALL PASS (0 failed) — **passes at baseline, so this had to be fixed, not excused** |
| `scripts/tests/probe_pipeline.py` | 1136 records · surface **481/481** (FK=ON, re-probed FK=OFF) · NULL-path 18/18 · SILENT-PASS 106 · ORPHAN 6 · ERROR 6 · BLOCKED 12 — **identical to the pre-rename run** |
| `run_checks.py --all` | **PASS** — 57 green, **0 blocking failures**, 8 advisory |

**Baseline comparison, run in a worktree at `df64417`:** baseline was 10 advisory + **1 blocking**
failure. After this change: **8 advisory, 0 blocking** — a strict subset. `context_map_fresh`,
`site_pages_fresh` and the blocking `pipeline_completeness_fresh` were red at baseline on staleness
and are now green. Two of the eight were checked line-by-line against baseline to confirm the
failure is the same one and not a new failure wearing the same name:
`validate_pydantic_schemas` 246 → 246 drift findings; `retired_vocabulary` 70 → **69** occurrences.

**No check that passed at baseline fails now.**

---

## 8. What this unblocks

Part I's constraints, Part I §I.3/§I.5/§I.6/§I.7 and the `specification_extraction_links` junction
(M4′) can now be written against the final names. The plan's own sequencing rule — *"sequence this
before Part I's rebuilds, or every constraint is written against a name about to change"* — is
discharged.
