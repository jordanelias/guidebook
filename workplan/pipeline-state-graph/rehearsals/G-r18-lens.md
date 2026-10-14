# G2-lens rehearsal report: slug-by-lens coverage (R18, COMPARISON P2, plan Phase 3 "research" row)

Clone: `$S/rehearsals/G2-lens` (base `31142552`, 8 wip commits, detached). Patch: `$S/rehearsals/G2-lens.patch` (598 lines, text only, `git apply --check` clean on a fresh worktree of the base). All figures below are results of commands run in the clone; re-run before quoting (rule 7a). `$S` = `/tmp/claude-0/-home-user-guidebook/db856d85-2082-5d35-9529-aa996506261b/scratchpad`.

## Verdict: EXECUTABLE WITH CHANGES

It executes, every gate is at or better than baseline, and `P-M` and C1.8 turn PASS. The changes to the wording are small and listed in section 8: key column of `access_needs`, the view's name and counting rule, the size of the writer change (now measured), the side effects on three freshness checks if it runs before step 1.1, the instrument edits R9 requires, and the R3 exception, which has no code to name because the step replaces none.

## 1. Migration `scripts/migrations/102_search_execution_lens.sql` (16 lines: 5 comment, 2 blank, 9 statement)

- Four `ALTER TABLE search_executions ADD COLUMN ... TEXT REFERENCES ...`, nullable, no CHECK, no DEFAULT, no backfill:
  `identity_code` -> `populations(population_code)`, `icf_code` -> `base_icf(icf_code)`, `needs_code` -> `access_needs(need_code)`, `medical_code` -> `base_taxonomy_medical(medical_code)`.
- **The key column of `access_needs` is `need_code`, not `needs_code`** (`needs_code` is the name of the referencing column, as on `source_value_extractions` and `specifications`; `PRAGMA foreign_key_list` on both confirms the same four targets).
- Applies to a copy of the live database (sqlite 3.45.1, STRICT table): 191 rows before and after, `PRAGMA foreign_key_check` 0 rows before and after, `integrity_check` ok; applied again through `migrate_db.py` in the clone with the same result (`Done. Schema at version 102; 0 data migration(s) applied.`). The earlier passes' claim holds.
- No `AFTER_DATA` marker is needed: it backfills nothing, and all 30 committed data migrations that INSERT into `search_executions` name their columns (`grep -hE "INSERT (OR [A-Z]+ )?INTO \"?search_executions\"?\s*(VALUES|SELECT)" scripts/migrations/*.sql | wc -l` -> 0), so a replay that reaches them before or after the ALTER works. `--rebuild` proves it (section 6).
- **Number collision:** T1 carries migrations 102 to 105 (`git diff 3077b99 origin/claude/t1-scan-contract-tooling --stat -- scripts/migrations`). At stack time this file renumbers (T1 first per step 0.2, so 106). Renumbering is a three-token edit in one file (file name, header line, `PRAGMA user_version`); I removed every "migration 102" mention from db.py, the test, and the mirror so nothing else cites the number. T1 does not touch `log_search`, `search_executions` or `schemas/search_execution.py` (no match in its committed diff or its uncommitted `db.py` diff), so no textual conflict is expected.
- **Order against R14's rename** (Phase 3 base: `populations` -> `base_taxonomy_identity`, `population_code` -> `identity_code`): either order works. Tested on a copy: after `ALTER TABLE populations RENAME TO base_taxonomy_identity` and `RENAME COLUMN population_code TO identity_code`, SQLite rewrote the new column's clause to `REFERENCES "base_taxonomy_identity"(identity_code)`, 191 rows, 0 foreign-key violations, view still reads. If the rename is stacked first, the migration must be written with the new names, because the replay runs it after the rename.

### The coverage view: `v_coverage_lens`

```sql
CREATE VIEW v_coverage_lens AS
SELECT slug, jurisdiction, language, identity_code, icf_code, needs_code, medical_code,
       SUM(deferred_reason IS NULL) AS searches, SUM(deferred_reason IS NOT NULL) AS deferred
FROM search_executions GROUP BY 1, 2, 3, 4, 5, 6, 7;
```

- **The repo already has four `v_coverage_*` views** (`_jurisdiction`, `_language`, `_branch`, `_priority`); the ideal's name `v_coverage` would break that family and the plan did not say so. I named it `v_coverage_lens`.
- **Counting rule differs from the ideal's** (`COUNT(*) AS searches` counts deferrals as searches). The three existing views count only `deferred_reason IS NULL` as a search, so `searches` here does the same and `deferred` is reported beside it. On the live table: 39 groups, `SUM(searches)` 190 + `SUM(deferred)` 1 = 191 rows.
- Grain is the ideal's (slug x jurisdiction x language x four codes) because a coarser view cannot be refined and a finer one rolls up by `SUM`. It is 4 lines. Today every one of its 39 groups has all four codes NULL (no pre-existing row says which lens it covered, and inventing that would be a research act).
- **What it cannot show:** a cell that was never searched. It lists logged cells only. The complement (every slug x every lens code, minus logged) needs a cross join against the registries, as `v_coverage_priority` does for jurisdiction x language; that is not built, and `P-M` passing means the record exists, not that R4 can be demonstrated. Scale for the owner: `select count(*) from slugs where status in ('ACTIVE','STUB')` (103) times the registry rows (`populations` 23, `base_icf` 72, `access_needs` 17, `base_taxonomy_medical` 0) is the "every code is a cell" reading; whether a cell is a code or a family is not ruled (re-derive; this is a reading, not a ruling).
- Reader (rule: nothing is added without naming what reads it): `skills/research-log-manager_SKILL.md` (the skill that tells sessions to log searches and read coverage from the views); like its three siblings it has no code reader. R4's enforcer in `scripts/audit/research_batch_dod.py` still reads `evidence_population_match`, and its own comment says text cannot prove a crossing; the lens columns are the structural evidence it asks for. Re-pointing it is not part of R18 and is not done or sized here.
- Stage-map: **no entry is needed.** `governance/stage-map.yaml` lists tables only (its header says views are "STILL OWED"); `build_graph.py`'s `view_info` derives the view's stage: reads `search_executions` only, stage `research`, crosses nothing. No table is added, so `build_graph.py --check` needs no stage-map edit.
- Rule 4 sweep of `sqlite_master`: the only views over `search_executions` are `v_coverage_{jurisdiction,language,branch,priority}` and `v_source_admission`, all with explicit column lists (none is `SELECT *`); the only trigger in the database is on `specifications`. Nothing breaks.

## 2. The writer: `scripts/db.py log_search`, +17 lines, 0 deleted

Flags (all optional, named as `add-extraction` names them):

```
log-search ... [--identity POPULATION_CODE] [--icf ICF_CODE] [--needs NEED_CODE] [--medical MEDICAL_CODE]
```

- `log_search(..., identity_code=None, icf_code=None, needs_code=None, medical_code=None, dry_run=False)`: new keyword parameters sit before `dry_run`; no caller passes `dry_run` positionally (all Python callers use keywords; `grep -n "log_search(" scripts`).
- Validation is one loop inside the existing `with connect(...)` block: `for col in _LENS_COLUMNS: dbcore.fk_declared(conn, "search_executions", col, row[col], f"log-search {col}")`. `dbcore.fk_declared` already existed (used by `amend-term`, `amend-source`, the extraction amender) and **reads `PRAGMA foreign_key_list`**, so the registry table and key are derived from the column's own foreign key, with no `choices=` list and no vocabulary restated. `_LENS_COLUMNS` is the existing names-only constant used by `add-extraction`; nothing new is listed. `grep -c 'choices=' scripts/db.py` is 55 at the base and 55 after (0 added).
- Refusals observed (exit 1, nothing written, row count unchanged): `--identity NOPE` / `--icf b999` / `--needs A-NOPE` / `--medical MED-1` -> `REFUSING: log-search <col>: search_executions.<col>='<v>' has no matching row in <registry>.<key>. A reference must point at something this project actually holds. Nothing was written.` A blank value (`--identity ""`) is refused the same way (it is not silently dropped, as `add-extraction` does; one fewer line, and a blank is not an absence).
- Not wired, by choice: no `choices=` on the flags (72 ICF codes would flood `--help`, `base_taxonomy_medical` is empty); no "at least one lens" rule (R18 and the brief make them optional; "at least one" is `add-extraction`'s D-0182 and would break every existing invocation); no bucket refusal (waits on LED-193); no `amend-search --set-lens` (the columns are write-once, like `jurisdiction` and the prior; a wrong lens costs a compensating migration; the 191 pre-existing rows stay NULL).
- **`--medical` refuses every code until `base_taxonomy_medical` has a row** (it has 0 today; Phase 5 fills it through `add-medical`). The refusal says "has no matching row in base_taxonomy_medical.medical_code", which is accurate but less pointed than `add-extraction`'s "the registry holds no rows". So the medical column of `v_coverage_lens` is NULL for every row until Phase 5. Not fixed (4 more lines for a nicer message).
- Existing invocations: the legacy shape (no lens flag) wrote exec 192 with four NULLs; `test_search_log_completeness` (CLI `log-search` with no lens flag) and the J05 case (positional call) pass; the INSERT fixtures in `research_batch_dod.py` name their columns.
- **Hazard that no gate covers:** a scratch database copied before this migration lands, used with the new `db.py`, fails every `log-search` with `no column named identity_code` (the row dict now always carries the four keys). `emit_batch_sql` already refuses a scratch whose `user_version` differs from the canonical's, so the failure is loud and the remedy is to re-copy. A session that spans the merge meets it once.

## 3. Capture (`dbcore.writable_tables`, `emit_batch_sql.py`, `emit_data_migration.py`): 0 lines to edit

- `writable_tables` is table-level and already holds `search_executions` (its `_INSERT_RE` finds `INSERT INTO search_executions` at one place in `db.py`).
- Columns come from `PRAGMA table_info` in `emit_batch_sql.emit` (`cols = columns(ca, table)`), not from a list, so the new columns are captured the moment they exist. `emit_data_migration.py` passes the SQL through (no column list; its guards are `RANGE_GUARDS` for `evidence_sources.tier` and risky-pattern warnings).
- End-to-end run in the clone (inline `GUIDEBOOK_DB_PATH` on every call): scratch copy of the post-102 database -> `db.py log-search` twice (one legacy shape, one with `--identity ADHD --icf b114 --needs A-AT`) -> `emit_batch_sql.py` wrote `2 insert(s), 0 update(s), 0 delete(s)` and its INSERT column list ends `"updated_at", "updated_by_session", "identity_code", "icf_code", "needs_code", "medical_code"` with values `'ADHD', 'b114', 'A-AT', NULL` -> `emit_data_migration.py` -> `migrate_db.py` (`1 data migration(s) applied`, 193 rows, 0 FK violations, `v_coverage_lens` showed the lens row beside the NULL row) -> `migrate_db.py --rebuild` (`user_version 102`, same table and view sets, `search_executions` identical to the canonical in all 33 columns and 193 rows). Evidence kept: `$S/rehearsals/G2-lens_delta.sql`, `G2-lens_capture_data_migration.sql.txt`.
- The rehearsal data migration was then deleted and the database blob restored (rule 10: research rows never ship with tooling): the final database hashes to the committed post-102 blob (`sha256 1340e93c...`); I issued no write against `/home/user/guidebook`; the clone's starting blob hash equals `git show 31142552:data/guidebook.db | sha256sum`.

## 4. Tests: `scripts/tests/test_db_amend_writers.py` Section M, +32 lines (3 assertions: 120 -> 123)

- M01 refusal: each of the four flags with `NOT-A-CODE` exits 1, names "has no matching row in", and writes nothing (row count unchanged).
- M02 storage: live codes (read from the copy, none hard-coded) land in their columns, with the medical column NULL.
- M03 capture: `emit_batch_sql.emit` renders that INSERT ending `'<pop>', '<icf>', '<need>', NULL);`.
- Through argparse (`run_cli`), not the function, because an unwired flag is invisible to a function call.
- Fault injection (each restored afterwards; `git status` clean): validation loop replaced by `pass` -> M01 red (the row dies as a bare `sqlite3.IntegrityError: FOREIGN KEY constraint failed`, the old behaviour); dispatch wiring removed -> M01, M02, M03 red (120/123); only `medical_code=args.medical` removed from the dispatch -> M01 red; row-dict entries removed -> `KeyError: 'identity_code'` in `log_search`, the suite exits 1 at the first fixture (red). Green after restoration: 123/123.
- Existing writer tests: the full suite is `test_db_amend_writers` (123/123), `test_search_log_completeness`, `test_db_integrity` (blocking), all green inside `run_checks --all`.

## 5. Instrument (R4, R9): P-M and C1.8 turn PASS

`python3 workplan/pipeline-state-graph/build_graph.py` (no `--compare`), before -> after:

| item | before | after |
|---|---|---|
| `P-M` | FAIL `{"lens_columns_on_search_executions": [], "tables": []}` | PASS `{"lens_columns_on_search_executions": ["identity_code","icf_code","needs_code","medical_code"], "tables": ["search_executions"]}` |
| C1.8 | FAIL (P-M = FAIL) | PASS (P-M = PASS) |
| C-033 | open, `P-M -> FAIL` | entry deleted from `conflicts.yaml` (-13 lines), R9 |
| capabilities.yaml "Search log" note | "has no lens column, so R4's slug x lens coverage cannot be shown (C1.8)" | one line rewritten: the claim was false after this step (a prose caller no gate covers) |
| `v_coverage_lens` in STATE-GRAPH §views | absent | stage `research`, crosses nothing |
| `build_graph.py --check` / `--selftest` | 0 failures, 5 warnings / 15 mutation tests | 0 failures, 5 warnings / 15 mutation tests |

The LED-029 -> SUPERSEDED status correction stays in `conflicts.yaml` `status_corrections` (step 2.2), so deleting C-033 loses no tracked item. Regeneration also pulls in unrelated live drift (`pipeline_runs` 5 -> 6 rows, infrastructure 743 -> 744) and rewrites the `Generated ... from git HEAD ...` and `Source tree:` lines, so every PR that regenerates the instrument conflicts with every other that does; regenerate last.

## 6. Gates (baseline first)

Baseline method: the clone's `origin/main` is a stale local `main` (`3077b99`, T1's base), which puts batch 24's research migration into every changeset and turns `research_tooling_separation` red the moment tooling is added (plan §5a records this). I set the clone-local ref `refs/remotes/origin/main` to the pinned base `31142552` (simulating a main that already contains the merge), then measured a same-ref baseline in a detached worktree of the base. The first, stale-ref baseline (67 green / 7 nothing / 11 red) is also saved.

| gate | baseline (same ref) | after | note |
|---|---|---|---|
| `run_checks.py --all` | 63 green, 11 nothing-in-scope, 11 advisory red, exit 0 | 65 green, 10 nothing, 10 advisory red, exit 0 | per-check diff: only `context_map_fresh` FAIL -> PASS (regenerated) and `research_tooling_separation` NONE -> PASS (it now has a subject). Red set otherwise identical; detail text identical except `schema_walkability_fresh` EXAMINED (21 -> 22 views, 115 -> 119 edges) and a memory address in `validate_pydantic_schemas`. |
| `run_checks.py --changed-from origin/main --explain` | n/a | exit 0: 65 green, 10 nothing, 9 advisory red; 15 changed files; kinds data, governance, render, schema, tooling | |
| `--selftest` | PASS | PASS | not skipped |
| `schema_reference_audit.py` | PASS | PASS | |
| `build_graph.py --check` | 0 failures | 0 failures | |
| `migrate_db.py --rebuild` + compare | `user_version` 101; same 82 tables; same views; `pipeline_runs` 6 vs 0 (exempt) | `user_version` 102; same 82 tables; same views (22); `pipeline_runs` 6 vs 0 only; DDL of `search_executions` and `v_coverage_lens` identical; `search_executions` rows identical | rebuild also run with the rehearsal data migration present (section 3) |

Two checks went red from this step and are cured in the same PR **only because it runs before step 1.1**:
- `pipeline_completeness_fresh` (**blocking**) and `pipeline_walk_fresh` (advisory) embed `user_version` and the view/table facts of the database, so any schema bump makes them stale. Cure: `python3 tools/pipeline_completeness.py` and `python3 tools/pipeline_walk.py` (3 changed lines each of HTML, `user_version 101` -> `102`). `schema_walkability_fresh` was already red at baseline and is left alone. After 1.1 these checks no longer exist, so the plan's ordering (Phase 1 before Phase 3) removes the cost; the v4 text should say so, because this step is also the first schema migration to land after any freshness check survives.
- `context_map_fresh` (advisory, red at baseline) is regenerated (`python3 scripts/generate/context_map.py`, +13/-4) and goes green. About half of that diff is not this step's (the plan file listing, `pipeline_runs` 5 -> 6).

## 7. Measured diff

`git diff --shortstat 31142552..HEAD -- . ':!data/guidebook.db'`: 14 files changed, 163 insertions(+), 60 deletions(-). **The step ADDS more than it removes.**

| area | files | added | removed |
|---|---:|---:|---:|
| `scripts/db.py` (writer) | 1 | 17 | 0 |
| `scripts/tests/test_db_amend_writers.py` | 1 | 32 | 0 |
| `schemas/search_execution.py` (mirror) | 1 | 7 | 1 |
| `skills/research-log-manager_SKILL.md` | 1 | 3 | 1 |
| `tools/*.html` regenerated | 2 | 3 | 3 |
| R3 areas (`scripts schemas tools .github skills`, migrations excluded) | 6 | **62** | **5** |
| `scripts/migrations/102_...sql` | 1 | 16 (9 statements) | 0 |
| `conflicts.yaml` (C-033) | 1 | 0 | 13 |
| `capabilities.yaml` | 1 | 1 | 1 |
| generated: `governance/context-map.yaml` | 1 | 13 | 4 |
| generated: `STATE-GRAPH.md`, `CONFLICTS.md`, `CAPABILITIES.md`, `graph.json` | 4 | 71 | 37 |

Budget metric (plan §1 command): `scripts/` py+sh 46,510 -> 46,559 (+49, i.e. db.py +17 and the test +32). `db.py` 9,355 -> 9,372. Hand-written lines: +76 / -16. The plan's COMPARISON estimate of "10 migration lines" was for the four ALTERs; with the view, header and PRAGMA it is 16 lines, 9 of them statements.

**The R3 exception this is:** plan Phase 3 "research" row (the only one the plan allows). R3 asks the exception to name "the code it replaces". **There is none**: nothing in `scripts/` is deleted or shrunk, `terms_used` and `--terms-used` stay, no check reads either. The plan's phrase "replacing the free-text `terms_used` as the evidence of coverage" is about the evidence, not code. The v4 text should state "replaces no code" and carry the measured figure. Offsets available, none taken: `schemas/search_execution.py` (77 lines before this step) is imported by nothing and absent from `validate_pydantic_schemas`' curated map (the archived 2026-08-04 findings already record `SearchExecution` unmapped), so under RULINGS R5 it would be deleted outright and my +7/-1 mirror edit is wasted; under the plan's "keep the requirement for now" CLAUDE.md §4 requires the edit. v4 should say which.

Files edited (14): `scripts/db.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/migrations/102_search_execution_lens.sql` (new), `schemas/search_execution.py`, `skills/research-log-manager_SKILL.md`, `governance/context-map.yaml`, `tools/pipeline-completeness-dashboard.html`, `tools/pipeline-walk.html`, `workplan/pipeline-state-graph/{conflicts.yaml, capabilities.yaml, STATE-GRAPH.md, CONFLICTS.md, CAPABILITIES.md, graph.json}`. Non-obvious: the skill (the only thing that tells a session to pass the flags; without it the columns stay NULL), the stale capabilities note, the two dashboards.

## 8. Defects and changes to the plan's wording

1. `access_needs` key column is `need_code`; the plan and R18 name only the tables. v4 should give the four `table(key)` pairs.
2. R18 says "under the R14 names" and the plan and brief say "under the live registry names". The two are not the same text after R14's rename, and the migration must use the names in force at its position in the stack. The rename and this migration commute (tested), so the order is free; the wording must not fix the names.
3. The plan's "one coverage view" collides with the existing `v_coverage_*` family and with the ideal's counting rule (deferrals counted as searches). Section 1 gives the form.
4. The `log-search` change is sized (+17 db.py, +32 test, +3 skill, 0 in `dbcore`/`emit_*`), not "unsized".
5. The step breaks `pipeline_completeness_fresh` (blocking), `pipeline_walk_fresh` and `context_map_fresh` if it runs before 1.1; the plan names none of them. Phase order makes it moot for the first two.
6. R9 requires the step to delete C-033 and the instrument carried a false prose claim (`capabilities.yaml` note). Neither is in the plan's row. Plan §4's slug-by-lens sheet row ("gates: C-033, 3 research"), §6's research row (conflicts column) and §7's two slug-by-lens rows still cite C-033 and should drop it.
7. R3 exception has no replaced code (section 7).
8. `P-M` passing is weaker than C-033's title suggests: the record exists, but absence of a searched cell is not derivable (section 1), and the medical column cannot be filled until Phase 5.

## 9. Residual risk and what I did not verify

- The 191 existing rows are NULL in all four lens columns by design; coverage by lens starts from the first logged search after this lands. If the owner wants history classified, that is research content (rule 10) and cannot ship with the tooling.
- Lens columns are write-once (no amend verb); a mistyped but valid code is permanent.
- [UNVERIFIED] Behaviour on a SQLite older than 3.45.1 (the repository's rebuild uses the system library; ADD COLUMN with REFERENCES and a NULL default is long supported, STRICT tables need 3.37).
- [UNVERIFIED] CI on GitHub (`ci.yml`), the `check_commit_msg.py` format on push, and attestation/rule-2 paths (this diff touches none of `references/bpc-reasoning/`, `references/connection-reasoning/`, `decisions/`, `sessions/`).
- [UNVERIFIED] Whether `view_info`'s derived stage and the unregistered view survive T1's merge; T1's `v_scan_ledger` is a different object.
- Not done, not sized: re-pointing R4's batch-DoD enforcer at the lens columns; a verb to print the complement (never-searched cells); a message for `--medical` against the empty registry.
- Not run: step 2.2's `LED-029` status correction; the antagonist pass (R7); the Pydantic ruling.

## 10. Wording for the v4 plan row (Phase 3, research)

> **research** | **Slug-by-lens coverage (R18).** One schema migration adds four nullable columns to `search_executions`: `identity_code` -> `populations(population_code)`, `icf_code` -> `base_icf(icf_code)`, `needs_code` -> `access_needs(need_code)`, `medical_code` -> `base_taxonomy_medical(medical_code)` (the names in force at its position in the stack: written with `base_taxonomy_identity(identity_code)` if R14's rename is stacked first; the two commute), no CHECK, no backfill, `terms_used` kept; and one view, `v_coverage_lens` (slug x jurisdiction x language x the four codes -> `searches` = `deferred_reason IS NULL`, `deferred`), named for the existing `v_coverage_*` family. `db.py log-search` gains `--identity --icf --needs --medical` (optional; each refused by `dbcore.fk_declared` unless it names a row of its registry, so no list is restated); `--medical` refuses everything until Phase 5 fills `base_taxonomy_medical`. Same-PR edits: `test_db_amend_writers.py` Section M (refusal, storage, capture; fault-injected); `skills/research-log-manager_SKILL.md` (the flags and the view); `schemas/search_execution.py` only if the Pydantic ruling keeps mirrors (otherwise delete the file, which nothing imports); regenerate `governance/context-map.yaml` and the instrument (`build_graph.py`, last); delete C-033 from `conflicts.yaml` and rewrite the "Search log" note in `capabilities.yaml`; and, if 1.1 has not landed, regenerate `tools/pipeline-completeness-dashboard.html` and `tools/pipeline-walk.html` (the migration stales `pipeline_completeness_fresh`, blocking). `dbcore.py`, `emit_batch_sql.py`, `emit_data_migration.py`, `stage-map.yaml` need no edit. Measured at base `31142552`: R3 areas +62/-5, migration +16 (9 statements), generated +84/-41 (context map +13/-4, instrument outputs +71/-37); the step adds code and replaces none, which is the one R3 exception. The bucket refusal waits for LED-193. | `P-M`, C1.8 (both PASS in the rehearsal); C-033 leaves the register

Pointers: renumber the migration at stack time (three tokens in one file); regenerate the instrument after the stack, not before.
