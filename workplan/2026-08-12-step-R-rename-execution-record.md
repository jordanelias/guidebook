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
- `scripts/migrations/056_schema_phase_rebased_after_rename.sql` — **added after the adversarial
  review**, because the split above fixed replay backwards and broke it forwards. See §4c.

DDL inside a data migration has precedent: `data_20260525013000_supersession_v1_stamp_correction.sql`
runs `ALTER TABLE ... ADD/DROP/RENAME COLUMN` for the same class of reason (a schema constraint
blocking a data correction).

### 2b. What `056` adds, and the invariant that now holds

Because the DDL is data-phase, **any future numbered schema migration touching these two tables
would run before the rename existed.** `056` carries a marker read by `migrate_db.py:build_plan()`:

```
-- AFTER_DATA: 20260812075349
```

meaning *this migration, and every migration numbered after it, applies only once the data
migrations up to that timestamp have replayed.* Replay becomes: schema 001–055 → all data through
the rename → schema 056+. That is the true chronology; the numbered/timestamped split simply had no
way to say it. Both the rebuild path and the apply-pending path walk **one** plan, so they cannot
disagree — a divergence there would surface in the blocking reproducibility gate as a mystery
rather than as this bug.

**From 057 onward, ordinary numbered schema migrations may reference `specifications` and
`specification_source_links` normally.** Part I's constraints and triggers need no special handling.
No committed file was edited to achieve this: 055 and the data migration are immutable and unchanged.

**Verified:** rebuild succeeds; committed DB and rebuilt DB agree on `PRAGMA user_version` (56), on
every `sqlite_master` object *including its SQL text* (0 differences either direction), and on row
counts across every shared table (0 divergences). The reviewer's own falsifier — a scratch `057`
running `ALTER TABLE specifications ADD COLUMN doctrine_sha TEXT`, a `CREATE INDEX` and a
`CREATE VIEW` on the renamed table — now rebuilds green at `user_version` 57.

---

## 3. Callers swept

**23 live `.py` files** across `schemas/`, `scripts/`, `tools/`. All parse. (An earlier draft
claimed "221 token replacements"; the figure came from a sed run count and is not reproducible by
any counting rule — 222 old-name occurrences existed across those files at `df64417`, of which a
number were deliberately retained. The file count is exact; the replacement count is withdrawn.)

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

## 4c. What the adversarial review found — and what changed because of it

Two antagonist reviews ran against `84cdac0`. **Ten findings survived**; the material ones are
below, with what was done. This section exists because a review whose findings are not enumerated
is indistinguishable from a review that found nothing.

### Fixed

| Finding | What was wrong | Fix |
|---|---|---|
| **Replay order broke forwards** | Moving the DDL to the data phase fixed replay backwards and broke it forwards: any *future* numbered schema migration touching these tables runs before the rename exists. The reviewer proved it by writing the exact next planned statement — W3.3's `ALTER TABLE ... ADD COLUMN doctrine_sha` — into a scratch migrations dir and watching `--rebuild` die. **`055`'s claim that the sequencing rule was "discharged" was false.** | `AFTER_DATA` marker in `migrate_db.py:build_plan()`, carried by `056`. Both the rebuild path and the apply-pending path walk one plan, so they cannot disagree. Verified with the reviewer's own probe: rebuilds green at `user_version` 57 with the column present and a dependent view compiling |
| **A frozen audit record was overwritten, with a forged as-of stamp** | The probe re-run overwrote `audits/2026-08-12-pipeline-probe-*` — **the very thing §5 below forbids** — and its header stamped `repo HEAD df64417`, where the table is `evidence_cell_state`, while the body says `specifications` 161 times. The subject was the uncommitted working tree | Originals restored from `7e8319b`. The probe now appends `+dirty` to the stamp and names the working tree as the subject, so the stamp cannot be true of a commit it did not read. The new run ships under its own dated name |
| **No Decision Record for a D-SCHEMA change** | Migrations 036/037/038 each have a register entry; a rename of the central synthesis table had neither a DR nor a register row. A `workplan/` execution record is not a decision record and `decision_capture` C9 will never see it | `decisions/DR-2026-08-12-specification-rename-and-replay-order.md`, register row **D-0158**, a mirroring row in the canonical `decisions` table, and an attestation. C9 orphans and total warnings are unchanged from baseline at 49 and 54 |
| **The retired-vocabulary register was not updated** | The repo's purpose-built mechanism for exactly this residue — a token that is readable and wrong — was untouched, so nothing would stop a future session reintroducing the old name | **RV-020** and **RV-021** at severity `broken`, with `exempt_paths` naming every legitimate carrier. `cell_id` recorded in `rejected:` with its reasoning (it fails admission test 4 against `schema-spec.md`'s own `cell_id`). The register found 43 live occurrences; they are now **1** — `specs/e-08.html`, under a separate owner instruction |
| **Live plans still carried old-name DDL** | `workplan/2026-08-12-resolution-plan.md` and the `execution-plan-2026-08-12/` set held copy-pasteable `BEFORE INSERT ON evidence_cell_state` and `SELECT ... FROM sqlite_master WHERE name='cell_source_links'` for work not yet done. The "frozen record" defence was unavailable — this commit had already edited one of those files | Swept. The undated `best-practices-assessment-system.md` and `phase-e-execution-plan-v1.md` swept too: the register's own rule is that undated workplans read as standing instructions |
| **The fixture replay was an unlinked hand-copy** | Nothing tied `_apply_055()` to the migration it replays, so a compensating migration would not propagate and the fixture would silently build a schema the DB no longer has | `_assert_rename_replay_matches_migration()` parses the shipped migration's `RENAME` lines and refuses to run if any is missing from the replay. **Verified by tampering with it and watching it fire**, not by assuming it would |
| **Prose the sweep made false or mixed-vintage** | `pipeline-operations.md`'s table was stamped "Measured 2026-08-02" but one row had been updated to 2026-08-12 — worse than uniformly stale. `intra-category-cross-test-methodology.md` claimed three items are "already live in `specifications`" against 0 rows. `CLAUDE.md` and the skill pointed readers at "migration 055", which carries no DDL. Four live gate strings still printed "cell" | All corrected. The `pipeline-operations.md` table is restored to one vintage, with the reset stated once above it |
| **`168/167` scripts in the probe log** | A hardcoded denominator | Derived from the file list |

### Recorded, not fixed

- **86% of `84cdac0` is not the rename.** Regenerating `parts/` and `site/` folded a large,
  product-visible content deletion into a commit titled "rename": `parts/v10/part05.md` goes from
  273 recorded connections to 0 and drops the whole pending-connection table;
  `site/specs/a-18.html` loses its four-population determination table and eight governing-source
  citations. **This is not data loss** — those tables were already 0 rows *at baseline*, so the
  generated files were simply stale and the regeneration made them honest. It is a scope failure:
  a reviewer of a rename would not look there, and reverting the rename now also reverts the
  content. Disclosed rather than rewritten, because the history is pushed and the content is
  correct; the lesson is that a regeneration belongs in its own commit.
- **`PRAGMA user_version` 55 does not by itself imply the renamed names**, since the DDL is
  data-phase. **56 does.** `--schema-only` now refuses to cross the gate and says so, rather than
  applying a later schema migration out of order and claiming a schema the DB does not have.
- **`scripts/generate/room_page.py:51` reads a table literally named `specification`** (singular),
  which does not exist. It was obviously phantom before the rename; now it looks like a typo for a
  real table. Called out in `skills/cell-curator_SKILL.md`'s disambiguation note.

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
(M4′) can now be written against the final names, **as ordinary numbered schema migrations from 057
onward** — which was true only after `056`; the first version of this section claimed it while the
schema phase could not see the renamed tables at all. The plan's own sequencing rule — *"sequence
this before Part I's rebuilds, or every constraint is written against a name about to change"* — is
discharged.

**Still open, and owner-gated:** the deferred alternative in D-0158 §4(5) — a schema *and data*
baseline squashing the migration history. It is the larger clean answer to replay order, it needs a
runner change for data-migration supersession that does not exist today, and the corpus is at its
smallest right now, which is the cheapest moment it will ever have. `AFTER_DATA` does not foreclose
it.
