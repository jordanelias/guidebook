# T-055 pilot report (mobility family tooling: the `device_class` values and the parent gather)

Pilot, stacked. Written 2026-11-13. Base: `origin/claude/peaceful-noether-kvf3sf` at `f2772f1`. I overrode the task file's own BASE line (it would pick `origin/main` or the workplan branch `origin/ccr-408aaa9b-z3e4s0`, both stale for this pilot) with the branch tip, as the brief orders.

Stack applied in order with plain `git am`, no `--3way`, no fallback needed: `T-008-repilot.patch`, `T-016.patch`, `T-017.patch`, `T-018.patch`, `T-019.patch` (five commits on top of the base). `python3 scripts/migrate_db.py` afterwards reported "Schema at version 127", so the stack's migration is 127 (`127_extraction_lens_links.sql`); my migration is 128 (derived: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` plus one). No migration number collided.

Result: PILOTED. Outcome green, with 16 task-file defects (number 16 withdrawn) below.

## Brief checks (1) to (5)

1. Followed only CLAUDE.md and the task file, plus `T-102-design.md` (permitted) and `T-018-design.md`, which the task file names ("the recursive `family` CTE of `T-018-design.md` section 4") and which is not on the permitted list. Reading it was necessary: the task file is not self-contained here (defect 8).
2. Evidence command printed what the file says: the `device_class` CHECK with the chair and walker values (`manual_self_propelled, manual_attendant, power_chair, scooter, bariatric_manual, bariatric_power, walker_rollator, mixed, not_device_scoped`), then `0` for `grep -c parent_code scripts/assess/assess_cell.py`. One cosmetic difference: the regex stops before the closing `))`, so the CHECK prints with one `)` missing (defect 15).
3. Red before, green after. Details below.
4. Gate ran once (`scripts/preflight.sh --base "$BASE" --explain`). `RESULT: PASS — 59 check(s) green, 4 nothing-in-scope, 12 advisory failure(s)`; `PREFLIGHT: PASS`; `SELFTEST: PASS`. No blocking FAIL. EXAMINED lines of every named check are in the table.
5. Patch `T-055.patch` (one commit, `format-patch -1 --binary`) and this report are saved.

Canonical database sha256 before and after: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d` (unchanged; every write went to the clone's own copy).

## What was built (one commit)

- `scripts/migrations/128_device_class_mobility_values.sql`: rebuild of `source_value_extractions` (create, copy by column name, drop, rename, recreate four indexes, restore the AUTOINCREMENT floor, recreate the six views verbatim), generated from `sqlite_master` with one substitution: `crutches`, `cane`, `lower_limb_prosthesis` added to the `device_class` CHECK. T-018's all-NULL lens CHECK is carried verbatim. No `AFTER_DATA` marker of its own (see defect 6: the file is right).
- `scripts/db.py`: `device_class` added to `_AMENDABLE_SVE_FIELDS`, plus two help strings that said "ONLY these two" / "figure_role or comparator" (already false before this task). The `--reason` requirement and the CHECK vocabulary are the existing generic gates (`dbcore.check_declared`); no new code.
- `scripts/assess/assess_cell.py`: `_lens_clause` now builds the identity lens as `k.identity_code IN (<recursive family subquery>)` inside the per-figure `EXISTS`. Every gather path (sources, findings, confirmers, extraction links, `count_extractions`) goes through that one function, so one edit covers all. The exclusion reason text was corrected to mention the `parent_code` chain.
- `skills/run-pipeline_SKILL.md`: the sentence stating the gather rule corrected (caller).
- `governance/context-map.yaml`: regenerated (`scripts/generate/context_map.py`); the migration bumped `schema_version` and the engine now reads `base_taxonomy_identity` (defect 9).
- Tests: `scripts/tests/test_assess_cell_pilot.py` (T055-01 to T055-07, fixture `base_taxonomy_identity` added to `synth_db`, live cases T019-13 and T019-14 made family-aware); `scripts/tests/test_db_amend_writers.py` (T055-01 to T055-07).

## Red before, green after

Evidence command: before, the CHECK has no prosthesis, crutches or cane value and `grep -c parent_code` prints `0`. After: the CHECK holds all three and the engine reads the family.

Tests written first, run on the unchanged code (red), then after the change (green):

| Case (file) | Before | After |
|---|---|---|
| T055-01 (assess): parent cell gathers own plus descendants, grandchild included | FAIL (`['REF-T55-MOB']`) | PASS |
| T055-02 (assess): child cell gathers child and its descendants only | FAIL | PASS |
| T055-03 (assess): no family declared, a code is a root | PASS (guard) | PASS |
| T055-04 (assess, OI-13): figure linked to two children gathered once; governing count equals distinct extraction ids | FAIL | PASS |
| T055-05 (assess): parent with no figure of its own still has a cell (OD-08) | FAIL (refused "has no row") | PASS |
| T055-06 (assess): descendant's retired link carries nothing | PASS (guard) | PASS |
| T055-07 (assess): copy of the live database, two live codes put in parent and child relation on the copy | FAIL | PASS |
| T055-01 to -03 (amend): add-extraction accepts each new value | FAIL x3 | PASS x3 |
| T055-04 (amend): unknown value refused, nothing written | PASS (guard, argparse choices) | PASS |
| T055-05 (amend): amend-extraction `--field device_class` records the device with the reason ledgered | FAIL | PASS |
| T055-06 (amend): unknown value and blank reason refused | FAIL (setup row absent) | PASS |
| T055-07 (amend): vocabulary read by `dbcore.check_values` holds the new and the old values | FAIL | PASS |

T055-04 (assess) "must be able to fail": I seeded a defect (the family predicate written as a join on the links, in `count_extractions`) and it went red: `4 governing, 4 distinct, n_extractions=6, n_sources=2`; the seeded code was removed (file restored from a saved copy; the final diff contains none of it). The "T055-03/-06/amend-04 pass before" rows are regression guards, not red tests, and are marked so.

The stress harness of T-014 (section 6 step 2 says it "shows no other change") was not run: it is not in the stack and the file does not say where it is (defect 11).

## Check-by-check, before and after (as the registry runs them)

| Check | Before | After | Failing lines diff |
|---|---|---|---|
| `schema_reference_audit` | rc 0; `EXAMINED: 1189 SQL identifier references in 188 files against 82 live tables and views` | rc 0; `EXAMINED: 1206 ...` (+17 are my new SQL strings); first attempt was RED (defect 7), fixed, see below | none |
| `migration_reproducibility` | rc 0; `EXAMINED: 58`, `VERDICT: PASS` | rc 0; `EXAMINED: 58`, `VERDICT: PASS` | none |
| `migration_reproducibility.py --deep` (after only) | n/a | `EXAMINED: 57` (57 tables identical), `VERDICT: PASS` | n/a |
| `test_db_integrity` | rc 0; `RESULTS: 57/57`; `EXAMINED: 3894 subject-inspections across 47 instrumented check(s) of 57`; "PASSED HAVING EXAMINED NOTHING (10): B04, I3, I3b, B09, C10, C05, D02, G03, K01, K02" | identical | none |
| `test_assess_cell_pilot` | rc 0; 168 PASS lines | rc 0; 175 PASS lines (+7 mine) | none |
| `test_db_amend_writers` | rc 0; `EXAMINED: 169 assertion(s)` 169/169 | rc 0; `EXAMINED: 176` 176/176 (+7 mine) | none |
| `test_run_pipeline_refusals` | rc 0; 233 cases | rc 0; 233 cases | none |
| `test_scan_contract` | rc 1; 2 failed (G01, G02: the R2 baseline) | rc 1; the same 2 | none |
| `python3 workplan/pipeline-state-graph/build_graph.py --check` | rc 1; `109 failure(s), 5 warning(s)` | rc 1; `109 failure(s), 5 warning(s)` (only the order of 2 WARN lines differs) | no change |
| `research_tooling_separation.py --base "$BASE"` | n/a | `EXAMINED: 23`, `VERDICT: PASS` | n/a |
| `context_map_fresh` (`context_map.py --check`) | red after the migration, before regeneration | `EXAMINED: 1 context map (1763 lines) — fresh` after regeneration. Only this one check was re-run after I regenerated the file; the gate itself was not repeated. | n/a |

Ten checks in `test_db_integrity` examine nothing (K01 and K02 among them): that is the same in the before-run, so it says nothing of this change, but note that K01 (the derivation sha) is among the ones that examined nothing, so no registered check proves the family gather does not disturb a stored determination. The T019-13/14 live cases in `test_assess_cell_pilot` are the closest thing, and they were green.

Gate output, the three things the brief says to read:
- `RESULT: PASS — 59 check(s) green, 4 nothing-in-scope, 12 advisory failure(s)`.
- NOTHING-IN-SCOPE (4): `extraction_follow_up_audit`, `citation_mining_session`, `adversarial_pass_recorded`, `medical_lens_integrity`. Not passed, examined nothing; none reads what this task changes.
- Blocking FAIL: none. The 12 advisory FAILs: `scan_debt`, `verified_scan_integrity`, `validate_schema_cross_check`, `skill_vocabulary_audit`, `retired_vocabulary`, `research_dod`, `search_log_completeness`, `research_tooling_separation`, `research_protocol_audit`, `metadata_integrity_audit`, `test_scan_contract`, `context_map_fresh`. Of these, `validate_schema_cross_check`, `skill_vocabulary_audit`, `retired_vocabulary`, `research_dod`, `test_scan_contract` are in the R2 baseline. `research_tooling_separation` reads `origin/main` and fails on paths I did not touch; with `--base` it passes (as the file says it will). `context_map_fresh` was MINE (regenerated, green). `scan_debt`, `verified_scan_integrity`, `search_log_completeness`, `research_protocol_audit`, `metadata_integrity_audit` are corpus content and ledger failures (REF-xxxx scan debt, WebSearch ledger lines of another session, 24 CORRECTED metadata rows). They are not in `baseline-red-on-main.txt`, and I did not run them on the unchanged stack to prove they are red there; the migration copies every row unchanged (rows identical, below) and the diff touches no scan or source data, so I judge them not mine, but that is inference, not measurement.

## Rebuild proof

- Verified the migration copies rows unchanged: all 214 `source_value_extractions` rows and 216 `extraction_lens_links` rows identical before and after (every column compared), `sqlite_sequence` floor 227 kept, the object set (tables, indexes, views) identical, view SQL byte-identical, `PRAGMA foreign_key_check` empty, `PRAGMA integrity_check` ok.
- `migrate_db.py --rebuild` rebuilt the database; `migration_reproducibility.py --deep` PASS, `EXAMINED: 57`.
- The rebuild printed `('item_taxonomy_links', 495, 'base_icf', 4)` style foreign-key notices: pre-existing, not from 128.

## Sweep result

Names: `device_class`, `parent_code`, "the identity predicate of the engine".

- `device_class` in code: `scripts/db.py` (argparse `choices=dbcore.schema_choices(...)`, already derived, so the new values reached `add-extraction --help` with no edit; `_SVE_VOCAB_COLUMNS`; the insert column list) and two skills that only list it (`connection-discovery_SKILL.md`, `run-pipeline_SKILL.md` line about vocabularies): mentions, left. Views, triggers, indexes: only the table itself. Registry: no check names it. Prose: `governance/evidence-architecture.md`, `references/methodology/value-genealogy-worked-example-corridor-width.md`, `architecture/schema-spec.md`, `governance/context-map.yaml`: the context map was a caller (regenerated); the others are mentions.
- `parent_code`: only `scripts/audit/graph/*` and `graph_audit.py`, which read it for a cycle check: mentions.
- The identity predicate: no needle in the file is greppable (defect 5). By reading: one function, `_lens_clause`, used by `gather_sources`, `gather_findings`, `gather_confirmers`, `gather_extraction_links`, `count_extractions`. Callers that were affected and fixed: (a) `test_assess_cell_pilot.synth_db` had no `base_taxonomy_identity`, so every synthetic determination would have crashed on the family subquery; (b) T019-13 and T019-14 (live) compare the cell's reach with the figures linked to the cell's own code only, and would go red the day T-102 mints the first child; (c) the exclusion reason text; (d) the sentence in `run-pipeline_SKILL.md`; (e) the context map. Not touched: `population_match` matches a cell's identity code against `evidence_population_match.target_population`, so a parent's cell does not inherit a child's grade. That is the design's "grades are never fanned out" and I left it, but the file does not say it (defect 14).
- `RULE_VERSION` ("pilot-6") was not bumped, because the file says "nothing else in the engine changes" and no stored determination changes today (the registry holds no child under any parent: `select ... where parent_code is not null` prints `[]`). T-019 bumped it for its own change. Whether this change needs a bump is not decided by the file (defect 13).

Code size, as the file prescribes (`git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'`): measured against the base this reads `14 files changed, 1479 insertions(+), 377 deletions(-)` before my commit, because the stack's five commits sit between the merge-base and the base-tip clone. My commit alone: `5 files changed, 183 insertions(+), 21 deletions(-)` (`git diff --shortstat HEAD~1 HEAD -- scripts schemas .github skills ':!scripts/migrations'`), plus a 395-line generated migration. What reads what was added: `device_class` values are read by `add-extraction` and `amend-extraction`, and by T-102 (rows) and T-110; the family subquery is read by every gather in the engine; the `base_taxonomy_identity` fixture table is read by `_lens_clause`.

## Disagreements between the task file, `T-102-design.md`, and the stack (T-018, T-019)

Names that agree: `extraction_lens_links` (the link table), `v_live_lens_links`, `parent_code` on `base_taxonomy_identity`, `retire-lens-link`, `add-lens-link`, `amend-extraction`, the three new values (`lower_limb_prosthesis`, `crutches`, `cane`), `WHEEL`/`LLD`/`WALKAID` under `MOB`, `SCI` retired to `WHEEL`, `LMB` becoming `UPL`, "the design keeps no upper-limb prosthesis value", the stale-vocabulary alternative F (CHECK, not table). The T-055 task file's section 4 item 2 parenthesis (ninth set: `PROSTH` replaced by `LLD`; `lower_limb_prosthesis` stays a `device_class` value) agrees with the design's section 0 and section 4.

Disagreements (each is a defect below): flag names `--basis` / `--basis-text` in `T-102-design.md` sections 6a and 9 against `--lens-basis` / `--lens-basis-text` in the stack (T-018 task file, real code, `add-lens-link --help`); `T-102-design.md` section 7 item 4 and section 9 say T-018's verb takes `--identity C --basis ...` (same issue); T-102-design section 11 still carries a `PROSTH` mention list that is read as `LLD` (it says so); sections 10 and 12 keep `PROSTH` as record (they say so).

## Task-file defects

1. **Task file section 4 item 2 prescribes a CTE form that fails a blocking check.** It tells the executor to use "the recursive `family` CTE of `T-018-design.md` section 4", i.e. `WITH RECURSIVE family(code) AS (...)`. `schema_reference_audit` (blocking in the gate's list; here `rc=1`) reads that as a reference to a table called `family`: `MISSING: family (1 site(s))  scripts/assess/assess_cell.py:242`, `RESULT: FAIL — 1 reference(s) to 1 name(s) the schema does not have`. The audit's CTE detector is `\bWITH\s+(?:RECURSIVE\s+)?(\w+)\s+AS`, which does not match a CTE with a column list. The working form is `WITH RECURSIVE family AS (SELECT ? AS code UNION ...)`. This cost a failed before/after comparison and a re-run; the file (and `T-018-design.md` section 4) should state the column-listless form.
2. **The family CTE cannot be used as T-018-design section 4 sketches it.** The sketch has a top-level `WITH RECURSIVE ... ` and `k.identity_code IN (SELECT code FROM family)`. The engine builds its WHERE as a fragment spliced into five different SELECTs, so the CTE has to be a parenthesised subquery inside the `IN`. The file does not say that; the executor has to work it out.
3. **Task file section 4 item 2 says "Nothing else in the engine changes", but the engine's own fixtures break.** `test_assess_cell_pilot.synth_db` builds an in-memory schema with no `base_taxonomy_identity`; the first determination after the change would raise "no such table". The file's own sweep rule makes fixing it in scope, but the file does not predict it, and the file's section 8 ("Do not add a table, column ... that section 4 does not name") could be read as forbidding the fixture table. I added a fixture table and a `family=` keyword and said so; a corrected file should name it.
4. **A latent red the file does not warn about.** The live-database cases T019-13 and T019-14 assert that a cell reaches only figures carrying the cell's own identity code. They are green today (the registry holds no child), and go red the day T-102 mints one. I made them family-aware. The file's "Tests that must be red (or green) before you start" and its sweep do not list them.
5. **The sweep needle "the identity predicate of the engine" is not a greppable string.** Section 5's `N='<name>'` loop cannot run on it (it finds nothing). The needles should be the symbol `_lens_clause` (and optionally `v_live_lens_links` for the engine's reads).
6. **AFTER_DATA: the file is right, and says why in half a sentence only.** I checked it: `scripts/migrate_db.py` `build_plan` makes "this migration, and every migration numbered after it" wait for the data it names, so 128 needs no marker. A short pointer to `build_plan` would spare the executor a check; the file's wording ("T-018's marker already orders it after the data T-018 reshaped") is correct but gives no way to confirm.
7. **Section 6 step 1 omits `context_map_fresh`.** Its list of checks "that read what this task touches" is `schema_reference_audit migration_reproducibility test_db_integrity`. A schema migration bumps `schema_version`, and the context map is stale: the gate printed `STALE: governance/context-map.yaml differs from a fresh generation. Run: python3 scripts/generate/context_map.py`. Neither the file's steps nor its commit section mention regenerating it. (T-019's patch also edited `governance/context-map.yaml`.)
8. **The file claims to be self-contained ("beyond it this file is self-contained") but depends on `T-018-design.md` section 4 and `T-102-design.md` section 4.** The brief let me read the second; the first is named only by reference. The family CTE (the heart of item 2) is not in the file.
9. **The generated migration needs a recipe the file does not give.** Section 4 item 1 says "create, copy, drop, rename, and recreate every view and index naming the table" but names no template. `114_extraction_slug_and_root.sql` / `127_extraction_lens_links.sql` are the models; `T-018-design.md` section 5 names 114. The file should name the generation approach (read `sqlite_master`, one substitution, copy by column name), the six views to drop in dependency order, the four indexes, and the sqlite_sequence floor. I generated it from the live DDL (the migration header says so); a hand-typed copy of a 150-line table would have invited an error.
10. **Section 3's "Expected output today" is an approximation.** It says "the chair and walker values only; `0`". The command prints the CHECK with one `)` missing and the file treats that as a match; harmless but the executor must decide whether the printed text "differs".
11. **Section 6 step 2 requires the "stress harness of T-014" and the stack does not contain it.** `git ls-files | grep -i stress` finds only the October scratchpad session files; the T-014 task file (`tasks/T-014-stress-harness-and-probes.md`) is not applied by the stack, and T-014 is not in section 2's preconditions. I could not run it; the sentence is a no-op.
12. **Section 6 step 2 asks for a test that "a determination at the parent gathers the child's figure and one at the child does not gather the parent's" and also "seeded by the test on its own scratch copy (never in the canonical database)", but gives no way to seed.** In a synthetic fixture the registry does not exist (defect 3); on a copy of the live database there are no children and no figure for a seeded child. I used both: synthetic fixtures with a `family` keyword, and a live copy where two codes already linked on one parameter are put in a parent and child relation by an UPDATE of `parent_code` on the copy. A corrected file should say that this is the intended shape.
13. **No decision on `RULE_VERSION`.** The gather rule changes, and T-019 (a gather change of the same kind) bumped `RULE_VERSION` to `pilot-6` and changed the K01 payload. The file does not say whether to bump, or why not. I did not bump (no stored determination changes today, and the payload is unchanged). `stale_determinations` and K01 read the label, so a later bump would mark every live determination of the previous label.
14. **Grades interplay is unstated.** `population_match` matches a cell's identity word against `evidence_population_match.target_population`. A parent determination that gathers a child's figure will therefore not find a grade (it stays DOWN-WEIGHTED). That is consistent with the design ("grades never fanned out") but the task file never says it, and a reader testing a `MOB` determination may think the engine is broken.
15. **The T-102 design uses the wrong flag names for T-018's verbs.** `T-102-design.md` section 9: `add-lens-link --extraction-id N --identity C --basis {named_in_text,heading,study_participants} --basis-text "<words>"` and section 6a step 1 `--basis named_in_text`. The stack's verbs take `--lens-basis` and `--lens-basis-text` (`add-lens-link --help`; T-018 task file line "writers accept ... `--lens-basis` and `--lens-basis-text`"). The column names are `basis` and `basis_text`. The T-055 task file uses neither flag, so it is not affected, but T-102's executor will copy a flag that does not exist.
16. (withdrawn: I checked the `grep -n '_AMENDABLE_SVE_FIELDS =' -A3 scripts/db.py` pointer in `T-102-design.md` section 9 and it prints the whole set; it is correct.)
17. **`help` strings in `db.py` for `amend-extraction` were already false** ("figure_role or comparator", "ONLY these two") and the file does not tell the executor to fix them; the sweep rule makes them in scope, so I fixed them (see "What was built").

The three worst: defect 1 (the prescribed CTE form fails a blocking audit), defect 3 (the "nothing else changes" claim is false for the engine's fixtures, and the live T019 cases), and defect 7 (the context map is stale after any schema migration and the file never says to regenerate it).

Pilot effects of the provisional stack, as asked: T-018's task file and T-019's were revised after their patches. None of that affected my result beyond naming: the stack's real flags (`--lens-basis`, `--lens-basis-text`) are the ones the T-102 design gets wrong (defect 15), the stack's migration number is 127 (the real execution derives its own), and T-019's `OD-08` refusal ("has no row") is why T055-05 is red before the change and why the parent-with-only-children case needed no extra engine work. If the real T-019 merges with a different refusal text, T055-05's detail string is unaffected (it matches only that the result is the governing list).

Scratch copies deleted: `/tmp/guidebook-t-055` and the pilot clone.
