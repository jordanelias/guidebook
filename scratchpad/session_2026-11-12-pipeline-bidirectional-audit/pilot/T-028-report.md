# T-028 pilot report (A concept that is not an English string)

Pilot, not real execution. Opus-class executor. Clone: `/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/pilot/t-028`, branch `pilot-t-028`, two local commits: T-026's (`8f516dd`, applied from `T-026.patch`) and mine (`af01290`). Nothing pushed. `T-028.patch` holds only my commit (`git format-patch -1 --binary`).

**Base commit:** `b331dc6` (tip of `origin/claude/peaceful-noether-kvf3sf`). I overrode the file's own BASE line, as the brief says: that line would pick `origin/ccr-408aaa9b-z3e4s0` or `origin/main`, both stale in a clone.

**Stack route:** plain `git am "$OUT/T-026.patch"` worked, binary DB blob included. No `--3way`, no `git apply --exclude`. `python3 scripts/migrate_db.py` afterwards printed `Schema at version 126; 0 data migration(s) applied`, so the blob already carried T-026's schema. T-026 took 126. My migration's number came from the file's rule: highest was 126, so mine is 127.

**Outcome: PILOTED.** I got a green result. On the way I had to make four decisions that the file and the design leave open. Each is listed under Task-file defects (defects 3, 4, 5 and 6). None was guessing a vocabulary value. Each was choosing where a fact lives, or whether to keep a check. A real execution should have them settled first.

Canonical `data/guidebook.db` sha256 was `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d` before and after (equal). The clone's own copy moved to schema 127 through `migrate_db.py` only.

## Did it hold

1. **Only CLAUDE.md and the task file:** yes. I also read `T-028-design.md` (permitted), the T-026 pilot report and patch (needed to compare with the stack), and the code and tests the design names.
2. **The evidence command printed what the file says:** `[(0,)]`, as expected. The gate in section 2 printed `OD-03 OPEN (delegated; not required)` and `OD-38 OPEN (owner)`. `OD-38 STATUS: ANSWERED BY THE OWNER`, and ledger line 6072 carries the quoted ruling.
3. **Red before, green after:** yes. On the unchanged code these were red: T028-01 (an argparse usage error, because `--first-form` is unknown), T028-02 (`TypeError: insert_term() got an unexpected keyword argument 'attestation'`), T028-03 (the second jurisdiction was refused: `already holds 'quillonage rampe' (ar) as SYNONYM, instrument`), T028-04 and T028-07 (`rename_term() got an unexpected keyword argument 'from_form'`), T028-05 and T028-06 (`_name_holder()` and `_near_terms()` take 2 positional arguments). T028-03b is a guard case: it passes on both sides. After the change all eight pass. Each case's red was observed in the run, not assumed.
4. **Gate ran once; every named check's `EXAMINED:` read:** yes. The gate printed `RESULT: PASS — 60 check(s) green, 4 nothing-in-scope, 11 advisory failure(s)` and `PREFLIGHT: PASS`. The four nothing-in-scope checks were `extraction_follow_up_audit`, `citation_mining_session`, `adversarial_pass_recorded` and `medical_lens_integrity`; none reads this change. The 11 advisory failures are the same 11 the T-026 pilot reported, by name. `research_tooling_separation` FAILs in the gate. Run by hand with `--base origin/claude/peaceful-noether-kvf3sf` it gives EXAMINED 14 and PASS, so that FAIL is not mine.
5. **Patch and report saved:** yes.

## Check by check, before and after

Each check was run from its registry `cmd`, using the file's loop. The "before" state is the T-026 commit; the "after" state is my change.

| Check | Before | After | Failing set |
|---|---|---|---|
| migration_reproducibility | rc 0, EXAMINED 58, PASS | rc 0, EXAMINED 59, PASS | same |
| schema_reference_audit | rc 0, EXAMINED 1146 / 81 objects | rc 0, EXAMINED 1162 / 83 | same (none) |
| test_db_integrity | 56/56, EXAMINED 3669, same 10 passed-having-examined-nothing | 56/56, EXAMINED 3682, same 10 | same |
| column_vocabulary_audit | rc 0, EXAMINED 57 tables / 827 columns | rc 0, 58 / 837 | same |
| test_scan_contract | rc 1, EXAMINED 133, G01 and G02 fail | rc 1, EXAMINED 141 (+8 T028 cases), G01 and G02 fail | same as baseline file |
| test_db_amend_writers | rc 0, EXAMINED 161 | rc 0, 161 | same |
| test_evidence_cell_state_2_3 | rc 0, **no EXAMINED line** (`ALL PASS (0 failed)`) | same | same |
| test_run_pipeline_refusals | rc 0, EXAMINED 175 | rc 0, 175 | same |
| alias_provenance_audit | rc 0, EXAMINED 2382 | rc 0, 2382 | same |
| validate_parameters | rc 0, EXAMINED 10 | rc 0, 10 | same |
| jurisdiction_db_vocabulary | rc 0, EXAMINED 114 | rc 0, 114 | same |
| research_dod_selftest | rc 0, **no EXAMINED line** (`SELFTEST: PASS`) | same | same |
| scan_debt | rc 1, EXAMINED 580 | rc 1, 580 | same (red before) |

Other proofs:

- `migrate_db.py --rebuild` printed `Rebuilt ... successfully`.
- `migration_reproducibility.py --deep` printed `PASS`, so every form_id in the rebuilt database equals the applied one.
- `joined_cells_census.py` gave `EXAMINED: 458 ...; 66 candidate(s)` before and after, with no diff. The new `usage_type` is all NULL, so the census cannot judge it yet.
- `build_graph.py --check` gave 109 failures on the T-026 commit (run in a worktree) and 109 after. In between, my first after-run gave 110: the extra failure was `tables in the schema but not in stage-map: ['term_label_picks']`. Registering the table in `stage-map.yaml` cleared it.
- `v_term_names` on the clone: 94 terms, all `label_ours`, all `label_is_instrument_term = 0`, which is what design section 6 predicts.
- The DB blob grew from 5206016 to 5836800 bytes. The rebuild leaves free pages, and there is no VACUUM.

## Sweep

I swept the five names the file lists (`canonical_en`, `term_aliases`, `_name_holder`, `_near_terms`, `alias_type`) with the file's four commands. For the writers I also used the verb needles (`insert_term`, `rename_term`, `add-term`, `rename-term`, `mint_term_from_catalogue`), because of defect 9 below. These are the callers I found and repaired:

- **`scripts/db.py`**
  - `_near_terms`, now `(conn, name, language)`.
  - `_name_holder`, now `(conn, name, language, *, exclude_term)`; it returns `{clashes, seed_matches}`, plus a new helper `_label_clash`.
  - `insert_term`: both routes, writes the first member row, and `--attestation` is required.
  - `rename_term`: no alias row; `--from-form` and `--judge`.
  - `mint_term_from_catalogue`: label screen only.
  - `add_alias`, `_alias_direct`, `_alias_write`: occurrence grain, a `form_id` key on updates, a DOMAIN refusal, `--usage-type`, and `_conflations`.
  - `log_search`: validates `form_id`, not `rowid`.
  - The three parsers and their dispatch.
- **Tests**
  - `test_scan_contract.py`: N07 rewritten (no alias row; the former label is in `scope_note`); T201 and T202 gain `attestation`; T026-02 and T026-07 call `_near_terms(..., "EN")`; T028-01 to T028-07 and T028-03b added.
  - `test_run_pipeline_refusals.py`: T01 and T02 gain `attestation`.
  - `test_db_amend_writers.py`: the `fixture_term` helper gains `attestation`.
- **Skills**
  - `skills/run-pipeline_SKILL.md`: the add-term paragraph now covers the first form, `--first-form`, the label as ours, the per-language screens and `--from-form --judge`.
  - `skills/research-log-manager_SKILL.md`: `--form-id` is now a form_id, and the sentence "a search uses the forms of its language, never the label" is added.
- **`workplan/pipeline-state-graph/machines.yaml`** M03.t3: the guard "a term can only be minted FROM an observation" was made false by the base route, so I rewrote it.
- **Governance:** `stage-map.yaml` and `owner-browser.yaml` gained `term_label_picks`; the `owner-browser` sentences for `term_aliases` and `terms` were rewritten as "forms / occurrence" and "our English label". I regenerated `context-map.yaml`.

These hits are mentions, left unchanged:

- `research_batch_dod.py`: its selftest INSERT has no `attestation` and still works through T-026's DEFAULT.
- `scan_debt.py`, `validate_parameters.py`: they read `canonical_en` as a label.
- `extract_db.py`, `jurisdiction_db_vocabulary.py`.
- `alias_provenance_audit.py`: it already counts per row, which is per form_id. Design section 13's "counts per form_id, not per key" needs no change.
- `pipeline-contract.yaml:53`, `functional-taxonomy.md:249/426`, `held-tensions.md:99`, `check-registry.yaml:329` ("2382 today", still true).
- `skills/multilingual-research_SKILL.md`: named by the design, but it mentions neither table nor verb.

`architecture/sqlite-data-layer.md` §4.9 is a stale design document dated 2026-05-05. It shows the old PRIMARY KEY, `term_item_links` and item codes, and was already false before T-026. I left it and report it here.

## Code size

`git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`) measures T-026 and T-028 together: `7 files changed, 712 insertions(+), 203 deletions(-)`. Mine alone (against `HEAD~1`): `6 files changed, 479 insertions(+), 213 deletions(-)`. On top of that there is a 141-line migration, `127_term_forms_occurrence.sql`.

What reads each addition:

- `v_term_names`: render (T-037, not built yet) and the tests. No writer reads it today.
- `term_label_picks`: nothing reads it yet. It is the record OD-38 demands, and the tests read it.
- `usage_type`: `add-alias` and `add-term` write it; nothing reads it yet (T-107, render).

What the change makes deletable: nothing. `rename_term`'s DEPRECATED-alias branch is deleted (about 20 lines).

## Where T-028's design and T-026's pilot patch disagree

1. **The junction FK.** The T-026 patch made `search_execution_forms.form_id` with no FK. Its comment reads "no FK is possible on a rowid", and migration 126 says "T-028 adds the key when term_aliases has one". The T-028 task file never says to rebuild the junction. Design section 10, step 4, says "T-026's junction will name it by FK: recreate as it stands", which is false: there is no FK. The junction appears in the file's `sqlite_master ... like '%term_aliases%'` probe only because its SQL **comment** contains the word. I rebuilt it with `REFERENCES term_aliases(form_id)` (a STRICT table, rows copied), as migration 126 promises.
2. **DEFAULT on `attestation`.** The design's section 3 sketch has `attestation TEXT NOT NULL` with no DEFAULT. T-026 had to add `DEFAULT 'unrecorded'` (ADD COLUMN NOT NULL needs one). Design section 10, step 2, says to copy the column definitions from `sqlite_master`, which keeps the DEFAULT. I kept it, because `research_batch_dod.py`'s selftest INSERT relies on it. The sketch and the stack disagree, and the file does not say which wins.
3. **`_near_terms`.** T-026 narrowed it to `canonical_en` plus attested EN aliases of any `alias_type`, NARROWER and BROADER included. The design wants members only, per language, with labels only for EN. I took the design's version.
4. **`add-alias` base route.** T-026 added `--alias`, `--language` and `--jurisdiction`, and its own lang_jur_map pair rule. Design section 4 names none of these, and T-028 builds on them without saying so. The no-downgrade and held-attested refusals T-026 added (keyed on `(term, alias, language)`) are replaced by the occurrence rule. A second observation of an attested form is now a new row, not a refusal.
5. **`log-search --form-id`.** T-026 validates by `rowid` and documents it ("SELECT rowid, alias ...") in `db.py` and in the research-log-manager skill. I moved both to `form_id`. Neither file lists this caller.
6. **`alias_provenance_audit`.** T-026 keeps a notes fallback for `unrecorded` rows. The design's section 13 says only "reads `attestation`". No conflict in behaviour, but the design does not record the fallback.
7. **The "rowid until T-028" window.** T-026's junction rows point at rowids that are stable only if no VACUUM or rebuild runs before 127. The 127 rebuild copies `rowid` into `form_id`, so the pointers survived (deep reproducibility PASS). There were 0 junction rows on the clone, so this was proven on an empty table only, which by CLAUDE.md rule 4 is unproven.

## Task-file defects

The count is 17. The three worst are 1, 3 and 5.

1. **The junction FK is missing from the file, and the design states it wrongly.** See disagreement 1. The file's section 4 and the design's section 10 never say to rebuild `search_execution_forms`. The design says the junction "will name it by FK", but it cannot and does not. The probe that "lists every view and index that names the table" finds the junction through a SQL comment, which is a false positive that happens to point at a real job. The probe command was `python3 -I -c "...select type,name from sqlite_master where sql like '%term_aliases%' and name<>'term_aliases'"`, and it printed the two indexes and `('table','search_execution_forms')`. A corrected file needs: "rebuild `search_execution_forms` with `form_id REFERENCES term_aliases(form_id)`, as migration 126's header promises."
2. **Section 8 contradicts section 4 on the OD-38 home.** Section 4, item 2, says the home of the judge and the reason "is the executor's to name". Section 8 says "Do not add a table, column ... that section 4 does not name". I added a table, `term_label_picks(pick_id, term_id, form_id FK, former_label, judge, reason, created_*)`. I chose a table over columns on `terms` because columns would be overwritten by a later rename and would describe a stale pick. The design's alternative D forbids a display pointer on `terms`; this table is not read by `v_term_names`. The file should name the home outright.
3. **The design's routes for the former label are inconsistent.** Design section 6 says "the former label stays recorded once, in the `scope_note` trailer". Section 8, as corrected for OD-38, says a trailer appended to a note is forbidden by the 2026-11-06 schema-shape statement. I applied the correction to `--from-form` only: the former label goes to `term_label_picks.former_label` and no trailer is written. `--from-observation` and `--ruling-quote` still write the `AMENDED` trailer, which is the same defect the correction names. A corrected file should say whether the other two routes also move to a typed home (and which one), or that the trailer is knowingly kept for them.
4. **The base route's `--rationale` has no home.** The design specifies `add-term --first-form ... --rationale "..."`. But the base route writes no adjudication (`term_adjudications.observation_id` is NOT NULL), and `terms` has no rationale column. I stored it in the first member row's `term_aliases.notes`, the row that founds the concept. That is a judgment about the concept sitting in a cell about one form. The file or the design must name its home: a column on `terms`, or a base-route adjudication table.
5. **The design weakens refusals that section 8 forbids weakening.** Design section 8 makes `rename-term` and `mint-term-from-catalogue` "label screen only". Before, both refused a name that was any alias of another term. A new label that equals another concept's attested form is now accepted. `_near_terms` no longer compares a non-English name with English labels. These narrowings are E4 and the eighth statement working as intended. But the task file's section 8 ("Do not weaken a refusal") forbids them as written, and section 9 makes that a stop. I followed the design, because the file says the design governs. The file should say that these narrowings are licensed.
6. **The observation route writes an attestation with less proof than `add-alias` demands.** `add-term --from-observation` now writes an attested member row (`observation_id` set, `attestation` instrument or other_source). Unlike `add-alias`'s observation route, it does not check that the observation's quote is in a file saved for its source. So the same attestation is written to two standards. The design is silent. I did not add the check: it would break fixtures in three test files and section 8 forbids unnamed additions. A corrected file should decide this.
7. **The design's expected-red texts are not what a test that can turn green observes.** T028-01's expected red is "the following arguments are required: --from-observation". It is an argparse usage error, but which argument it names depends on argv order. T028-02's expected red is "refused: not inside the observed phrase". A test that passes the now-required `attestation` gets `TypeError: unexpected keyword argument 'attestation'` on the old code instead. A test that omits `attestation` would refuse on the new code. The design should state the red loosely ("refused, or the argument is unknown").
8. **"The refusal text must say" there are no tokens, but no refusal fires.** Design section 8 says a non-Latin name "yields no tokens and no near match, which the refusal text must say". With no tokens, no near-match refusal occurs at all. I put an informational `near_screen` key in `add-term`'s output instead. The design should say "the writer's output must say".
9. **The sweep's needles miss callers of the changed writers.** The five names do not include `insert_term`, `rename_term`, `add-term` or `rename-term`. That misses:
   - `workplan/pipeline-state-graph/machines.yaml` M03.t3, whose guard became false;
   - `test_run_pipeline_refusals.py` T01 and T02, and `test_db_amend_writers.py`'s `fixture_term`. All three break once `--attestation` is required, and were found only because those files happen to contain `canonical_en`;
   - `skills/run-pipeline_SKILL.md:67`;
   - the T-026 rowid wording in `log_search` and `research-log-manager_SKILL.md`, which `term_aliases` finds but which neither file lists.

   The file should add the verb and function names as needles.
10. **A new table's registrations are not named.** The file says to regenerate `context-map.yaml`, but not to add the table to `governance/stage-map.yaml` and `owner-browser.yaml`. `build_graph.py --check` went from 109 to 110 failures (`tables in the schema but not in stage-map: ['term_label_picks']`) until I added it. This is the same gap as T-026's defect 15. The stage I chose (`base`) is a judgment the file should make.
11. **The DOMAIN refusal and `--usage-type` have no test case.** Design section 14's six cases do not cover them. I checked them by CLI only: `add-alias ... --alias-type DOMAIN` printed `REFUSING: add-alias: DOMAIN joins a relation with a usage ... --usage-type code_term|colloquial|...`. There is no registered test.
12. **`label_is_instrument_term` is misnamed.** In the design's view sketch it is computed over attested forms of both kinds (`instrument` or `other_source`), not over instruments. The name says "instrument". Either rename it or restrict it to instruments. I kept the sketch.
13. **The AFTER_DATA marker is redundant on this stack.** T-026's migration 126 already carries `AFTER_DATA: 20261106053823`, the same cutoff the design's step 1 derives, so 127's marker opens no new segment. It is harmless, but the file states it as necessary without saying it depends on whether data migrations arrive between T-026 and T-028.
14. **Section 6's before-run list omits the tests section 5 says to run.** I added the registered test files plus `alias_provenance_audit`, `validate_parameters`, `jurisdiction_db_vocabulary`, `research_dod_selftest` and `scan_debt`. `test_evidence_cell_state_2_3` and `research_dod_selftest` print no `EXAMINED:` line.
15. **The set-up BASE line is stale for a pilot** (overridden, as the brief says). Also, `$TMPDIR` was unset, so `SCRATCH` became `/tmp/guidebook-t-028`, a fixed path shared across runs of this task.
16. **The precondition "T-026 merged" cannot be checked as written in a stacked pilot.** The file's grep needs "<that task's commit subject>", which the file does not give. I found it by `git log | grep -F "type alias attestation"`. The file should give the subject.
17. **Minor.** The DB blob grows by about 600 KB from the rebuild's free pages, and nothing VACUUMs it; the file could say whether that is acceptable. And `architecture/sqlite-data-layer.md` §4.9, a caller of all three names, is stale beyond this task. The design lists it as a prose caller to fix, but fixing it means rewriting a historical design document.

### What a corrected file would need

- Name the junction FK rebuild.
- Name the OD-38 home (or license `term_label_picks`), and say whether the `AMENDED` trailer stays for the other two rename routes.
- Give the base route's rationale a home.
- License the refusal narrowings that E4 and the eighth statement require.
- Decide whether `add-term --from-observation` must verify the quote, as `add-alias` does.
- Add `insert_term`, `rename_term`, `add-term`, `rename-term` and `rowid` as sweep needles, and name `machines.yaml` M03.t3.
- Add the stage-map and owner-browser registration of the new table.
- Add DOMAIN and usage-type test cases.
- Restate the expected reds loosely.
- Give T-026's commit subject for the precondition.
