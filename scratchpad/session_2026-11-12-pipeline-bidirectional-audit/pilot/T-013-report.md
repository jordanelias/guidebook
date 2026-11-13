# T-013 pilot report (typed gaps)

PILOT (not real execution): no `/session-open`, no `scratchpad/CURRENT`, stayed on branch `pilot-T-013`, stopped after section 7 (local commit in the clone, `6e4a655`).

**Base commit:** `d095227` (tip of `origin/claude/peaceful-noether-kvf3sf` in the clone). I overrode the task file's own `BASE=` line (it chooses `origin/ccr-408aaa9b-z3e4s0` or `origin/main`) with `BASE=origin/claude/peaceful-noether-kvf3sf`, as the brief orders, because the workplan PR is unmerged.

**Canonical database** `/home/user/guidebook/data/guidebook.db` sha256 before and after: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d` (equal). Only the clone's copy was migrated.

## What was done
- `scripts/migrations/126_typed_gap_subject_and_search_cause.sql` (number derived: highest was 125). `ALTER TABLE ... ADD COLUMN` x8 (all nullable, FK clauses on a NULL default are legal), `PRAGMA user_version = 126`. Applied with `python3 scripts/migrate_db.py`. No table rebuild was needed (see defect 4).
- `scripts/assess/assess_cell.py`: the pending-cell gap INSERT now carries `parameter_id` and the four lens columns.
- `scripts/db.py`: `add-gap` accepts `--parameter --identity --icf --needs --medical --jurisdiction --language`, validated in `insert_gap` (FKs via `dbcore.fk_declared`, jurisdiction via `dbcore.check_jurisdiction`, language against `lang_jur_map` as `log-search` does); `log-search` accepts `--gap-id` (FK-checked).
- `scripts/tests/test_run_pipeline_refusals.py`: cases `T013-01`..`T013-06` (prefix confirmed free: `grep -c '"T013-'` gave 0).
- `governance/context-map.yaml` regenerated (`context_map_fresh` was fresh on the base and stale after the migration; a generated caller).
- Not changed: skills and prose that mention `add-gap`/`log-search` stay true (mentions). `architecture/sqlite-data-layer.md` section 4.3 DDL is already a stale historic snapshot (lacks columns added long before), left alone.

## The five questions
1. **Followed only CLAUDE.md and the task file:** yes (plus the brief and the baseline file).
2. **Evidence command printed what the file says:** yes. `gaps` columns: gap_id, category, priority, status, skill, section, description, created_at, created_by_session, updated_at, updated_by_session, falsification_condition, confidence_interval, shift_conditions, named_dissenter, mining_addressability (no parameter_id, lens, jurisdiction, language); second query `[(0,)]`. Caveat: the file's wording implies the lens/jurisdiction/language columns are a gap-level gap only; `search_executions` ALREADY has `jurisdiction`, `language`, the four lens columns and `parameter_id` (only `gap_id` is missing), which the file does say implicitly but never states (defect 3).
3. **Red before, green after:** yes.
   - Section 6 step 2 command: on the migrated copy with the unchanged engine, `select gap_id, parameter_id, identity_code` returned `('GAP-103', None, None)` (red); with the change it returned `('GAP-103', 7, 'ALL', None)` (green; the file's query `select parameter_id, identity_code ... order by rowid desc limit 1` gives `(7, 'ALL')`). `log-search --gap-id GAP-103` stored it (exec 204); `--gap-id GAP-999` refused by name.
   - New tests: with `db.py` and `assess_cell.py` stashed to the base (database migrated): T013-01..06 all FAILED (`EXAMINED: 181 cases, FAILED: 6`). With the change: `PASS: all 181 cases`.
   - Two of my own test-writing mistakes were caught by running (a cell E01 had already determined on the copy; a "highest gap id" that was non-numeric text). The file's guidance on fixtures does not warn of either (defect 7).
4. **Gate ran once; `EXAMINED:` lines read:** yes. `scripts/preflight.sh --base "$BASE" --explain`: `SELFTEST: PASS`, `RESULT: PASS — 60 check(s) green, 4 nothing-in-scope, 11 advisory failure(s)`, `PREFLIGHT: PASS`. NOTHING-IN-SCOPE: extraction_follow_up_audit, citation_mining_session, adversarial_pass_recorded, medical_lens_integrity (none touches this change). The 11 advisory FAILs are all not mine: test_scan_contract (G01/G02), validate_schema_cross_check, skill_vocabulary_audit, retired_vocabulary, research_dod (R12) are in the R2 baseline; scan_debt, verified_scan_integrity, metadata_integrity_audit, research_protocol_audit (CHECK 8) are corpus-state reds on rows I did not touch and not in the baseline file; search_log_completeness is the session's unlogged WebSearch ledger; research_tooling_separation is a false red (defect 1). The per-check `EXAMINED:` lines (before / after) are in the table.
5. **Patch and report saved:** yes, `T-013.patch` (one commit, `git format-patch -1`) and this file.

## Check-by-check, before and after (section 6 loop, as the registry runs them)
| check | before | after |
|---|---|---|
| test_run_pipeline_refusals | rc 0, EXAMINED: 175 cases | rc 0, EXAMINED: 181 cases (+6, mine) |
| test_db_amend_writers | rc 0, EXAMINED: 161 | rc 0, EXAMINED: 161 |
| test_scan_contract | rc 1, EXAMINED: 119, FAILED 2 (G01, G02, baseline) | identical |
| test_author_presence | rc 0, EXAMINED: 13 (final line) | identical |
| test_search_log_completeness | rc 0, EXAMINED: 23 | identical |
| test_assess_cell_pilot | rc 0, **no EXAMINED line** (examined nothing, by that measure) | identical |
| test_validate_evidence_state_2_4 | rc 0, **no EXAMINED line** (prints `ALL PASS (0 failed)`) | identical |
| migration_reproducibility | rc 0, EXAMINED: 57, PASS | rc 0, EXAMINED: 57, PASS; `--deep` PASS (EXAMINED: 56 tables) |
| schema_reference_audit | rc 0, EXAMINED: 1125 refs / 188 files | EXAMINED: 1135 (+10, my SQL) |
| test_db_integrity | rc 0, 56/56, EXAMINED 3659 | 56/56, EXAMINED 3673 (more rows to inspect: the new gap rows come from no fixture; the DB is the migrated clone copy) |
| column_vocabulary_audit | rc 0, 56 tables / 818 columns | 56 tables / 826 columns (+8), CLEAN |
| (extra) test_evidence_cell_state_2_3 | not run before | ALL PASS after |
| joined_cells_census | EXAMINED: 457 text column(s) with data; 66 candidate(s) | identical (no new candidate) |
| context_map_fresh | fresh on base | STALE after migration, regenerated, fresh |
| build_graph.py --check | 109 failure(s), 5 warning(s) | identical set (one WARN line order differs); baseline red, not mine |

No failing case appeared that was not failing before.

## Sweep result
Ran the section 5 commands for all six names. Hits equal the file's list (code, sqlite_master, registry, prose). Callers judged:
- `scripts/assess/assess_cell.py` (INSERT INTO gaps): changed. `machines.yaml` needle `INSERT INTO gaps` still present in that file.
- `scripts/db.py` `add-gap`/`log-search`/`insert_gap`/`log_search`: changed.
- `gap_register_id` hits (`schemas/evidence_state.py`, `validate_evidence_state.py`, tests, `v_pending`): unchanged, still true; `v_pending` names its columns (no recreate).
- `test_evidence_cell_state_2_3.py`, `test_validate_evidence_state_2_4.py`, `test_db_integrity.py`, `test_search_log_completeness.py`, `test_db_amend_writers.py`: run, green.
- `governance/context-map.yaml`: a generated caller, regenerated.
- `research_batch_dod.py` INSERT INTO search_executions with named columns: unaffected.
- Skills and `.claude/commands/batch-done.md` that mention `add-gap`/`log-search`: mentions, still true. Prose in `architecture/sqlite-data-layer.md`, `governance/stage-map.yaml`, `machines.yaml`: mentions.
- `build_graph.py --check`: 109 failures identical before and after; reported, not mine.
- Views/indexes: `v_pending` (gaps) and the `v_coverage_*`/`v_source_admission` views (search_executions) are untouched by ADD COLUMN.
- Side effect to know: `jurisdiction_db_vocabulary` audit reads "every table with a `jurisdiction` column", so `gaps` is now in its scope (all NULL; it passed in the gate).

## Code size
`git diff --cached --shortstat $(git merge-base HEAD $BASE) -- scripts schemas .github skills ':!scripts/migrations'`: 3 files changed, 97 insertions(+), 6 deletions(-) (of which 41+/6- is non-test: `db.py` and `assess_cell.py`; 56+ is the test). What reads the additions: the engine (writes), `db.py gaps` (SELECT *), `coverage`, T-034. Replaces/makes deletable: nothing.

## Task-file defects
1. **Gate base mismatch (cost: the largest time sink, and a false red).** `preflight.sh --base "$BASE"` is given the branch tip, but `research_tooling_separation` diffs against `origin/main` regardless (`Changeset vs origin/main: 737 path(s)`, 12 research data paths, `VERDICT: FAIL`). Run with `--base $BASE` the same check says `6 path(s) ... PASS`. The file says to read blocking FAILs only and treats advisory reds as pre-existing; this one is red on the wrong diff, not on the base. The file should say that, on an unmerged workplan base, `research_tooling_separation` is a false red (or the registry cmd should take `--base`).
2. **Section 6 `CHECKS` list omits a test that section 5 says to run.** Section 5: "Every test file in that list is run before and after"; the list contains `scripts/tests/test_evidence_cell_state_2_3.py` (INTO gaps, gap_register_id) but the section 6 loop does not. I ran it only after (green); no before-run exists. Also `test_db_integrity` and `test_validate_evidence_state_2_4` are in it, fine.
3. **Section 4 item 1 does not say `search_executions` already has `jurisdiction`, `language`, the four lenses and `parameter_id`.** The prose "add to `search_executions` a nullable `gap_id`" is right, but section 3's "Expected output" says nothing about search_executions beyond gap_id, and an executor might add duplicates. A one-line statement would remove the doubt (I verified with `select sql from sqlite_master where name='search_executions'`).
4. **"SQLite cannot add a NOT NULL foreign key ... use create, copy, drop, rename ... and list every view and index" is boilerplate that does not apply here.** All eight columns are nullable, so `ALTER TABLE ADD COLUMN ... REFERENCES` works (precedent: migrations 100, 125). The file should say "if every added column is nullable, ADD COLUMN, no rebuild; list views only for a rebuild". Following the boilerplate would have been a 50-line rebuild of two big tables (`search_executions` is STRICT with 40+ columns) for nothing. It does say to list the views; I did (`v_pending`, v_coverage_*).
5. **Section 6 step 2 is not a runnable test, and its command's expected result is slightly off.** It is one run-on sentence ("Before: the evidence shows no columns. After: cp ... then `select parameter_id, identity_code ...` returns `(7, 'ALL')`"). It also hard-types `7` and `ALL`, contradicting the next paragraph's rule "never type into a test an id the database can derive" (it is a probe, but the rule is about tests, so the executor has to decide). The engine writes `GAP-103` here (the newest by rowid), which the file does not state; "order by rowid desc limit 1" works only because the engine's gap is the last inserted. No `--gap-id <that id>` value is derivable from the command: the executor must read the id from the select, add a column to it.
6. **Where to put the T013 test cases is not stated.** The file names ~11 registered test files but not which gets new cases; I chose `test_run_pipeline_refusals.py` because it already covers `add-gap`, `log-search` and the engine. A one-line pointer would save a survey.
7. **No warning of two fixture traps in that test file:** (a) E01 has already determined the (P_NODIR, IDENT, ICF) cell on the shared copy, so a fixture using the helper's default lens is refused "already determined" (T013-01's first run failed on that; fixed by adding the needs lens, derived by query); (b) `far()` assumes numeric ids, and the highest `gap_id` by string order is non-numeric text (`GAP-TITLES`-style), so deriving a free gap id needs the numeric ordering `db.next_gap_id` uses. Both cost a test iteration each.
8. **"Fixing a caller the sweep finds is in scope" does not list generated artefacts as callers.** `governance/context-map.yaml` went stale (`context_map_fresh` is advisory and fires only on the gate); the file never mentions regenerating it. It was found only because I ran `context_map.py --check` after reading the sweep's `gap_register_id` prose hit. Add `python3 scripts/generate/context_map.py` to any schema-migration task.
9. **Section 6's grep for `EXAMINED|RESULTS|FAILED|VERDICT` does not show the subject of two checks** (`test_assess_cell_pilot`, `test_validate_evidence_state_2_4` print none), and `test_author_presence` matches assertion labels. The file's own rule ("no EXAMINED line = examined nothing: say so") then applies to two tests that plainly ran dozens of assertions. Say which of the eleven are known not to print one.
10. **Section 2 BASE line and the `git switch -c` in the set-up are not usable in a pilot** (brief overrides this; the file notes it). The `export SCRATCH` line resolves to `/tmp/guidebook-t-013` here (TMPDIR unset), not under the pilot scratchpad: fine, but two pilots with the same task id would share it.
11. **The gate's run time (about 4 minutes) exceeds the harness's 120 s foreground limit**, so the file's one-line gate command is moved to the background and its `rc=` and `grep` output come back only in a task output file. The file should say to run it in the background.
12. **Pilot-status paragraph (section "Pilot status") is stale for this brief:** it says "not piloted". Harmless; recorded.
13. **Minor:** section 3 evidence command "run after the set-up block so that `$SCRATCH` exists" but does not use `$SCRATCH`.

Count: 13 (three worst: 1 gate false red from the base mismatch; 4 the table-rebuild boilerplate that does not apply; 5 step 2 is a run-on, hard-types ids and gives no derivable gap id).
