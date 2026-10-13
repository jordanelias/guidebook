# Rehearsal B-rename: ruling R14 (population names to identity names)

Clone: `scratchpad/rehearsals/B-rename`, based on `31142552`. Branches there: `r14-full` (R14 as worded, the deliverable), `m4-variant` (the recommended narrower act). Patches: `B-rename.patch` (31142552..r14-full, text only), `B-rename_M4-variant.patch` (post-Phase-1 stand-in to m4-variant), `B-rename_C2_phase1-deleted-files.patch` (counterfactual edits, committed then reverted). Gate outputs: `B-rename_gates_<stage>/` (all.txt, selftest.txt, sra.txt, bg.txt, rebuild.txt, rebuild_cmp.txt, SUMMARY.txt). SQLite 3.45.1.

## Verdict

**R14 as worded: EXECUTABLE WITH CHANGES, and not worth doing in that form.** The mechanics hold. SQLite rewrites every REFERENCES clause, index, autoindex and `sqlite_sequence` row. `--rebuild` matches the live database, and the gates return to the post-Phase-1 baseline. Three problems stop it being executable as written:

1. **Rebuild.** It needs `-- AFTER_DATA: <latest data_ timestamp>`. Without the marker, `--rebuild` exits 1 at `data_20260925050333` with "no such table: evidence_population_match".
2. **Sweep.** The sweep cannot rely on the gates. `schema_reference_audit` reported 10 sites. About 50 runtime sites exist in surviving code, plus about 20 in tests. At least two of the misses are **silent**: the engine computes a wrong answer and its test stays green.
3. **Done-when.** Its done-when probe, `P-C`, still fails afterwards. Seven columns carrying "population" survive Phase 1, and R14 does not rename them.

It also contradicts the ledger entry it rests on:

- LED-127 renames `target_population`/`study_population` to `served_group`/`study_group`. R14 omits this.
- LED-127 keeps those columns "out of the lens vocabulary", but R14 names their table `evidence_identity_match`.
- LED-127 says to register the retired tokens after the rename. That register step floods `retired_vocabulary` with 719 occurrences, and the English word `population` fails the register's admission test 4.

**Recommended:** run nothing until the owner records the LED-127 confirmation. If the owner nods, run **M4**: `populations` → `base_taxonomy_identity`, `population_icf_links` → `identity_icf_map`, and `population_code` → `identity_code` in both tables. Leave `evidence_population_match` and its two columns for the owner, as named below. Measured cost of M4:

- 21 files, +90/−91.
- A 10-line migration with **no AFTER_DATA marker**; `--rebuild` is green.
- Gates identical to full R14.
- Walkability identical.

M4 drops a third of R14's churn and the only replay hazard.

## Step 0: baseline (clone at 31142552, before any edit)

| gate | result |
|---|---|
| `run_checks.py --all` | PASS: 67 green, 7 examined nothing, 11 advisory red. The red set is the documented 10 plus `schema_walkability_fresh`. |
| `--selftest` | PASS |
| `schema_reference_audit.py` | PASS |
| `build_graph.py --check` | 0 failures, 5 warnings |
| `--rebuild` vs live | 82 tables, 21 views, 95 indexes and 1 trigger identical. Only `pipeline_runs` differs (6 vs 0, exempt). |

## Step 1: the post-Phase-1 stand-in (not R14's cost)

**What I did.** I wrote migrations 102, 103 and 104 as plain drops of the seven population-named tables:

- 1.2: `probe_population_links`, `item_population_elaborations`
- 1.3: `case_study_populations`, `citation_population_links`, `economics_entry_populations`, `extraction_population_links`
- 1.4: `population_axis_map`

Steps 1.5 and 1.9 contain no population-named table. No data migration INSERTs any of the seven. `population_axis_map`'s 53 rows come from `057_baseline` only. `--rebuild` stays green: 75 tables are identical, and no marker is needed.

**Reds that belong to Phase 1** (named, not fixed):

- `test_db_integrity` (blocking) crashes at A08 (`item_population_elaborations`).
- `schema_reference_audit` (blocking) flags `tools/regenerate_vetting_surface.py:94,97,100`, `known_debt.yaml:47` and `test_db_integrity.py:173,176`.
- `pipeline_completeness_fresh` (blocking) and `pipeline_walk_fresh` are owned by step 1.1.
- `population_integrity_audit` is deleted by 1.6(a).
- `test_db_amend_writers` fails as collateral of the crash.
- `build_graph --check` fails on stage-map entries for dropped tables.
- `research_tooling_separation` is red because the clone's `origin/main` is stale at 3077b99. This is an artefact of the rehearsal, as in §5a.

**Phase-1 shim (commit 69e3ea6, 4 files, −21 lines).** These are edits the plan already assigns to steps 1.2, 1.3 and 1.4. I made them only so that the crash would stop masking the rename:

- removed `test_db_integrity` A08;
- removed seven `stage-map.yaml` keys;
- removed the `known_debt.yaml` entry for `extraction_population_links`;
- removed `topology.py` `MISSION_CRITICAL["extraction_population_links"]`.

**Post-Phase-1 baseline (postshim):** 63 green, 6 examined nothing, 16 red. The blocking reds are `schema_reference_audit` (tools/ only) and `pipeline_completeness_fresh`, both owned by step 1.1. The rename is measured against this baseline.

## Step 2: enumeration (at 31142552; `git grep -lw`, frozen directories excluded)

The four names (`populations`, `population_icf_links`, `evidence_population_match`, `population_code`) appear in 351 text files and 1,803 lines. `populations` is also an English word. The second pair of columns below counts only identifier-shaped hits: the three unambiguous names, plus `populations` where it appears in backticks, SQL context, `populations.`, `populations(`, or as a quoted string.

| bucket | files | lines | identifier files | identifier lines |
|---|---:|---:|---:|---:|
| prose (governance/references/architecture) | 171 | 770 | 55 | 186 |
| workplan | 88 | 581 | 62 | 376 |
| scripts (py, non-test) | 23 | 160 | 23 | 139 |
| skills | 14 | 65 | 6 | 21 |
| governance yaml | 5 | 54 | 5 | 41 (context-map 30 of them, generated) |
| tools (py + html) | 8 | 38 | 6 | 26 |
| schemas | 11 | 37 | 7 | 19 |
| tests | 6 | 32 | 6 | 30 |
| generated/render (parts, site, specs, assets) | 5 | 15 | 1 | 1 |
| retrieval-log payloads (immutable) | 12 | 13 | 1 | 2 |
| CLAUDE.md | 1 | 3 | 1 | 3 |
| .claude | 1 | 1 | 0 | 0 (English, inside the injected R4 hook) |
| .github | 1 | 1 | 0 | 0 (a CI job name) |
| other (data/ YAML, working/) | 5 | 33 | 4 | 4 |

**Schema objects, derived from `sqlite_master` and PRAGMA after the stand-in drops:**

- Tables `populations`, `population_icf_links` and `evidence_population_match`.
- Columns `populations.population_code` (PK) and `population_icf_links.population_code`.
- Six FKs into `populations(population_code)`: `determination_gates`, `identity_medical_map`, `item_taxonomy_links`, `source_value_extractions` and `specifications`, all on columns already named `identity_code`, plus `populations.parent_code`.
- Indexes `idx_picf_icf`, `idx_epm_gap` and `idx_epm_ref`. Their names are abbreviations; SQLite has no `RENAME INDEX`. Their DDL is rewritten.
- No view or trigger names any of them.
- Seven more columns carry the word and are outside R14:
  - `evidence_population_match.target_population` and `.study_population`
  - `source_value_extractions.root_population_note` (16 rows)
  - `external_root_registry.root_population_note`
  - `reasoning_doc_citations.population`
  - `case_studies.population_description` and `.populations_served_note`
  - plus `bpc_metadata.population`, `spec_value_probes.population` and `term_item_links.population`, which steps 1.2 and 1.9 drop.

## Step 3: the rename migration and replay order

`105_identity_names.sql`, 15 lines: five `ALTER TABLE` statements (three `RENAME TO`, two `RENAME COLUMN`) and `-- AFTER_DATA: 20261010002423`.

**Committed data migrations that name the old identifiers:**

| name | data migrations naming it | INSERTing | after 095's cutoff (20260920060857) |
|---|---:|---:|---:|
| `evidence_population_match` | 33 | 23 | **4 INSERT** (20260925050333, 20260928074257, 20260928210349, 20261001034401) |
| `population_icf_links` | 2 | 2 | 0 |
| `populations` | 11 (comments or other tables' text) | 0 | 0 |
| `population_code` | 3 | 0 (as column list of `population_icf_links` INSERTs) | 0 |

**Without the marker,** 105 replays in the schema segment that follows 095, ahead of the four post-cutoff data migrations. The rebuild then fails, as measured: exit 1 at `data_20260925050333`, "no such table: evidence_population_match".

**With the marker,** `build_plan` puts 105 at index 187 of 188, after every data migration. 102, 103 and 104 stay before the post-cutoff data, at indexes 159–161 against 162. The rebuild exits 0 and matches live: 75 tables, 21 views, 91 indexes and 1 trigger, every row count equal except `pipeline_runs`.

**Variants that leave `evidence_population_match` alone need no marker.** Both the M4 set and `populations` alone rebuilt green without one.

**Future data migrations.**

- `emit_batch_sql.py` captures what `dbcore.writable_tables(conn)` returns. That is the set of literal `INSERT INTO <name>` strings in `db.py` and `assess_cell.py`, intersected with live tables. The capture therefore follows the writer edit with no list to maintain.
- I drove `add-population-match` and `add-population-icf-link` on a scratch copy and emitted the result through `emit_data_migration.py`. The emitted file read `INSERT INTO "evidence_identity_match"` and `INSERT INTO "identity_icf_map" (… "identity_code" …)`, and `--rebuild` replayed it after 105 (54→55 and 61→62 rows).
- `emit_data_migration.py` names no tables.
- `emit_batch_sql` refuses a scratch whose `user_version` differs from the canonical database, so a scratch copied before the rename cannot be captured.

**What every future data migration must say,** and what the v4 plan must state:

- New names only.
- Any data migration emitted under the old names but unmerged when the rename lands must be re-emitted. I measured this: a copy with old names dated after the marker fails `--rebuild` with "no such table".
- The marker's timestamp must be re-pinned at merge to the latest `data_*` on main.
- At stack time T1 brings 102–105, so the rename is renumbered.
- The marker also makes every later-numbered schema migration replay after those data migrations. That is the real chronology and harmless, but it is a property the plan should name.

## Step 4: the caller sweep (commits 53d4387, 8abb8a2, 6db87fd, 3e4d97b on `r14-full`)

**Breakage with no caller edits** (postrename_noedits): 53 green, 6 examined nothing, 26 red.

- New blocking reds: `test_db_integrity`, `validate_axes`, `research_dod_selftest`, `research_dod_session`.
- New advisory reds: `validate_population`, `research_dod`, `test_graph_audit`, `test_db_amend_writers`, `test_evidence_cell_state_2_3`, `test_directness_2_2`.
- `build_graph --check` fails on three stage-map keys.
- `schema_reference_audit` lists 10 sites.

**Edits that survive Phase 1** (the real cost), 26 files, 133 changed lines (+132/−133):

| bucket | files | lines changed | files |
|---|---:|---:|---|
| scripts (py) | 10 | 81 | `db.py` 31; `validate_population.py` 9; `assess_cell.py` 9; `graph_audit.py` 7; `graph/extract_db.py` 5; `research_batch_dod.py` 5; `derivation_handshake_integrity.py` 4; `research_protocol_audit.py` 4; `validate_pydantic_schemas.py` 4 (`MODEL_TABLE_MAP`, `FIELD_ALIASES`); `graph/topology.py` 3 |
| tests | 6 | 29 (2 of them in `test_db_integrity` A03, which step 1.2 deletes) | `test_assess_cell_pilot` 10, `test_db_amend_writers` 5, `test_db_integrity` 5, `test_validate_evidence_state_2_4` 4, `test_evidence_cell_state_2_3` 3, `test_directness_2_2` 2 |
| schemas | 3 | 7 | `directness.py`, `evidence_state.py`, `source_value_extraction.py` (comments and docstrings only) |
| skills | 3 | 7 | `adversarial-research`, `gap-driven-mining`, `workplan-orchestrator` (an SQL example) |
| governance yaml | 1 | 4 | `stage-map.yaml`: three keys and one `disputed:` sentence |
| **owner merge** | 3 | 5 | `research-contract.yaml` R4 hook sentence and R13 anchor; `.claude/settings.json` regenerated by `research_contract_hook.py --write`, one line; CLAUDE.md §6, one sentence |
| derived | 1 | +30/−120 | `context-map.yaml` regenerated. About 43 lines are the rename's own; the rest are Phase-1 drops and pre-existing staleness. |
| migration | 1 | +15 | `105_identity_names.sql` |

**Net code lines: 0.** The edits are line-for-line. Migrations add +15 and CLAUDE.md −1. The step does not add code under the plan's budget metric, but it touches 133 lines.

**Not edited, and kept on purpose:**

- Historical comments that name a past defect under its then-name (`dbcore.py`, `emit_batch_sql.py`, `db.py:6004,8813`, `assess_cell.py:1483`).
- English uses of "populations".
- Registry `note:` prose (`check-registry.yaml` 795, 1517, 2352, 2382). Step 1.8 deletes most of it.
- `retired-vocabulary.yaml:924`.
- Verb and flag names (`add-population-icf-link`, `add-population-match`, `--population`, `--target-population`, `--study-population`), the Python names `insert_population_match`, `PopulationCode` and `Population`, and the graph-audit node kind `population`. R14 does not rule on these. Renaming the verbs would also touch skills and every session command log.

**Gates after the sweep** (`final`): 63 green, 6 examined nothing, 16 red, a count identical to postshim.

| check | baseline | postshim (post-Phase-1) | rename, no edits | final (R14) | m4 |
|---|---|---|---|---|---|
| `test_db_integrity` (blocking) | PASS | PASS | **FAIL** | PASS | PASS |
| `research_dod_selftest`, `research_dod_session` (blocking) | PASS | PASS | **FAIL** | PASS | PASS |
| `validate_axes` (blocking) | PASS | PASS | **FAIL** | FAIL, Phase-1-dependent (1.4 deletes it; counterfactual fix is 3 lines) | FAIL, same |
| `schema_reference_audit` (blocking) | PASS | FAIL (tools/, 1.1) | FAIL (+7 sites) | FAIL (tools/ only, 1.1) | same |
| `pipeline_completeness_fresh` (blocking) | PASS | FAIL (1.1) | FAIL | FAIL (1.1) | FAIL (1.1) |
| `validate_population`, `research_dod`, `test_graph_audit`, `test_db_amend_writers`, `test_evidence_cell_state_2_3`, `test_directness_2_2` | PASS | PASS | **FAIL** | PASS | PASS |
| `context_map_fresh` | FAIL | FAIL | FAIL | PASS (regenerated) | PASS |
| `derivation_handshake_integrity` | PASS (56 pairs) | PASS (56) | **PASS with 0 pairs (silent)** | PASS (56) | PASS (56) |
| `validate_pydantic_schemas` drift findings | 213 | 216 | — | 216 | — |
| `--selftest` | PASS | PASS | PASS | PASS | PASS |
| `build_graph --check` | 0 fail | 0 fail | 2 fail (stage-map) | 0 fail | 0 fail |
| `--rebuild` parity | OK | OK | OK | OK (marker) | OK (no marker) |

Every other check is unchanged from postshim. The four Phase-1-owned advisory reds (`population_integrity_audit`, `pipeline_walk_fresh`, `schema_walkability_fresh`, `site_pages_fresh`) stay as they were. So does the stale-origin artefact, `research_tooling_separation`.

**Counterfactual, running the rename before Phase 1:** 9 more files, 23 lines.

- `tools/pipeline_completeness.py`, `tools/regenerate_vetting_surface.py`
- `scripts/generate/{spec_page,build_site}.py`, `scripts/generate_parts.py`
- `validate_axes.py`, `population_integrity_audit.py`
- the `functional-deficit-auditor` and `progressive-measurement` skills

After those edits the gates equal postshim exactly. It would also owe renames of seven more `population_code` columns in seven population-named tables. R14 is right to order the rename after Phase 1.

**Runtime behaviour verified directly:**

- Both renamed writers work on a scratch copy.
- `add-population-icf-link` refuses an unknown code with the live list.
- `insert_population_icf_link` has **no test**; I drove it by hand.
- `validate_population` must change `CODE_COLUMNS`. After the rename no `population_code` column exists anywhere. I replaced it with `identity_code`, which also scans four more FK-enforced tables: EXAMINED went from 61 to 171. This is a behaviour change the plan must name.

## Step 5: prose (counted, not edited)

| area | files with any match | lines | files with identifier-shaped hits | lines |
|---|---:|---:|---:|---:|
| `references/` | 145 | 619 | 37 | 97 |
| `governance/*.md` | 17 | 77 | 10 | 26 |
| `architecture/` | 9 | 74 | 8 | 64 (56 of them `population_code` in older specs) |
| **total** | 171 | 770 | **55** | **187** |

The `governance/*.md` files are `conceptual-model`, `evidence-architecture`, `functional-taxonomy`, `pipeline-operations`, `population-taxonomy` and five more. `references/project-standards.md` is the append-only ledger and is not edited.

**Does leaving them stale violate anything?**

- Rule 4 says prose callers are not swept by any gate.
- Rule 7a's "third shape" and §5(b) ("prose that contradicts the database") make leaving them stale a violation that only a human catches. The operative `governance/*.md` lines (10 files, 26 lines) are the minimum to fix. `functional-taxonomy` and `conceptual-model` are taxonomy texts, so editing them is an owner merge.
- LED-127's ACTION says: "Add `population` and `population_code` to `retired-vocabulary.yaml` when the rename lands." I measured this by temporarily registering `population_icf_links`, `evidence_population_match` and `population_code`. Occurrences on the live surface went from 86 to 805: +45, +234 and +440 respectively.
- `population` cannot be registered at all: it is an English word, so it fails the register's admission test 4 ("matched mechanically without a judgment call").
- The register step is therefore not executable as written. The workable form is to register the two table names only, with category-A exemptions for history, and triage the remaining hits.

## Step 6: walkability (the IDEAL-GRAPH §6 script)

| state | tables | failing |
|---|---:|---:|
| 31142552 | 82 | 21 |
| after the seven stand-in drops | 75 | 21 |
| R14 | 75 | 21 |
| M4 | 75 | 21 |

The failing set is identical in every state. The renamed tables pass before and after, with the same hop counts.

The only structural change is latent: the identity key now has one name in its PK and in all six FK columns. Before the rename the PK was `population_code` and the FKs were `identity_code`. A name-based derivation such as the script's `unFK` test now covers the identity lens. It flags nothing today because every `identity_code` column already has an FK.

## Defects found in the plan and the rulings

1. **R14 omits the replay requirement.** The plan's R6 covers backfills and table drops, not renames. A rename of a table that post-095 data migrations INSERT into needs `AFTER_DATA`, as `migrate_db.py`'s `build_plan` docstring already says. Only `evidence_population_match` triggers it.
2. **R14's done-when cannot pass.** Plan §5 Phase 3 base lists `P-C` "per the sheet". After R14, `P-C` still reports seven population-bearing columns once Phase 1 has run (ten in this clone). Passing it needs those columns renamed too. That costs an estimated 40 more code lines (`target_population` 19, `study_population` 6, `root_population_note` 8, `population_description` 4, `populations_served_note` 2, plus `reasoning_doc_citations.population`) [estimate, not rehearsed], under the same marker: 4–5 post-cutoff data migrations name them.
3. **R14 against LED-127.** It omits `served_group`/`study_group`, which LED-127 names. Its `evidence_identity_match` puts the lens word on a table whose columns LED-127 keeps "out of the lens vocabulary". (Separately, LED-127's description of `target_population` as non-lens is itself contradicted: the writer validates it against identity codes.) And LED-127's register step floods the advisory check (Step 5).
4. **R14 against LED-121.** The owner's words are "base_taxonomy_icf, base_taxonomy_medical etc", and the ledger's own table maps `access_needs` → `base_taxonomy_needs`. R14 renames one of the three non-parallel registries. R18 accepts `base_icf` and `access_needs` as they stand. The ledger itself labels `base_taxonomy_identity` "derived" (D1, `references/project-standards.md`), with confirmation pending. R14's premise that "the family name and the lens name are both owner words" overstates this.
5. **`schema_reference_audit` (blocking; the enforcer rule 4 names) under-reports renames:**
   - Its "defined nearby" filter is scoped by directory and includes subpackages. Test fixtures in `scripts/tests/` and `validate_axes.py`'s selftest `CREATE TABLE` the old names, which masks every reference in `scripts/*.py`. For `db.py` it reported 0 of about 22 breaking lines.
   - It misses SQL split across implicitly concatenated string literals. At `assess_cell.py:655` the `FROM` is in a string without the verb.
   - It ignores existence-guarded reads: `_table_exists(conn, "x")`, `sqlite_master WHERE name='x'`, `"x" in tables`.
6. **Silent casualties.** Re-run against the renamed database, the unedited code fails without an error:
   - `assess_cell.derivation_handshake` returns no functional basis, so the engine silently drops the function path. `test_assess_cell_pilot`, which builds its own fixture with the old name, stays green.
   - `derivation_handshake_integrity` reports CLEAN over 0 (identity, ICF) pairs instead of 56, and EXAMINED stays 1.
   - The guarded reads in `research_batch_dod.py:396` and `graph/extract_db.py:160` would likewise skip silently [inferred from the code; not run in isolation].
7. **T1 adds a caller.** `scripts/tests/test_scan_contract.py` in T1, 2 lines. The sweep must run after T1 lands.
8. **`validate_population`.** Plan 1.6(b) makes its deletion conditional. The rename forces the decision on `CODE_COLUMNS`.

## Deviations from the brief

- I made four Phase-1 shim edits (commit 69e3ea6) that the plan assigns to steps 1.2, 1.3 and 1.4. Without them the `test_db_integrity` crash masks the rename.
- I edited `test_db_integrity` A03 even though 1.2 deletes it; it is counted separately above.
- I made the counterfactual edits to files Phase 1 deletes, then reverted them, to show that the gates return exactly to postshim.

## What the v4 plan text must say (replacement for the Phase 3 base row's "population" clause)

> **Identity names (R14, narrowed; owner confirmation of LED-127 recorded first).** One schema migration after Phase 1 and T1:
> `ALTER TABLE populations RENAME TO base_taxonomy_identity; ALTER TABLE base_taxonomy_identity RENAME COLUMN population_code TO identity_code; ALTER TABLE population_icf_links RENAME TO identity_icf_map; ALTER TABLE identity_icf_map RENAME COLUMN population_code TO identity_code;`
>
> No `AFTER_DATA` marker. Prove it at execution: `grep -lwE 'populations|population_icf_links|population_code' scripts/migrations/data_*.sql | xargs -n1 basename | cut -d_ -f2 | awk '$1>"20260920060857"'` must print nothing.
>
> **Same-PR edits.** Re-derive them with `git grep -nwE 'populations|population_icf_links|population_code' -- scripts schemas skills .claude 'governance/*.yaml' CLAUDE.md ':!scripts/migrations'` and read every hit. `schema_reference_audit` does not see most of them. They are:
> - `scripts/db.py`: every `--identity`/`target_population` existence check, `_LENS_COLUMNS`, `insert_population_icf_link` and its `schema_choices`, and help texts;
> - `scripts/assess/assess_cell.py`: `LENS_COLUMNS`, plus the `_table_exists` guard and the query in `derivation_handshake`. A miss there is silent, and its test stays green.
> - `scripts/audit/derivation_handshake_integrity.py` (a miss is silent: CLEAN over 0 pairs);
> - `scripts/audit/graph/extract_db.py`, `graph/topology.py`, and the `graph_audit.py` selftest;
> - `scripts/audit/validate_pydantic_schemas.py` (`MODEL_TABLE_MAP`, `FIELD_ALIASES`);
> - `scripts/validate_population.py`: `EXCLUDED_TABLES`, the query, and `CODE_COLUMNS` `population_code` → `identity_code`, which widens P2 to every `identity_code` column;
> - tests `test_assess_cell_pilot`, `test_db_amend_writers`, `test_evidence_cell_state_2_3`, `test_validate_evidence_state_2_4`, and T1's `test_scan_contract`;
> - skills `adversarial-research` and `workplan-orchestrator`;
> - `governance/stage-map.yaml` (two keys);
> - regenerate `governance/context-map.yaml`.
>
> **Owner merge:** the R4 hook sentence in `governance/research-contract.yaml`, then `python3 scripts/generate/research_contract_hook.py --write`; the CLAUDE.md §6 sentence "`populations` IS the identity lens"; and the operative prose in `governance/*.md` (10 files; the taxonomy texts are owner merge).
>
> **Done when:**
> - `--rebuild` gives table, view and row parity;
> - `derivation_handshake_integrity` prints the same (identity, ICF) pair count as before;
> - `validate_population` EXAMINED is at or above its pre-rename figure;
> - the grep above prints only historical comments.
>
> **Not in this step:** `evidence_population_match` and its `target_population`/`study_population` columns. LED-127 names `served_group`/`study_group` and keeps them out of the lens vocabulary, so the table's new name is the owner's. Its rename needs `-- AFTER_DATA: <latest data_ timestamp at merge>` and re-emission of any unmerged data migration. `P-C` stays NOT-BUILT after this step; it is not this step's done-when. LED-127's register step registers only the two renamed table names, with exemptions for history; `population` fails admission test 4.

## Residual risk and what I could not verify

- The breaking-site count (about 49 in surviving code plus about 20 in tests) is a classification I made by reading the diff, not a tool output [estimate].
- The silent skips in `research_batch_dod.py:396` and `extract_db.py:160` are inferred from the code. Only `assess_cell` and `derivation_handshake_integrity` were run old against new.
- The cost of making `P-C` pass (about 40 lines) was counted, not rehearsed.
- T1's uncommitted refactor was grepped for the old names (none found), not merged.
- The rename's interaction with R18's four lens columns on `search_executions` was not rehearsed. `RENAME TABLE` would rewrite their FK automatically. Ordering base before research, as the plan does, avoids any double edit.
- The owner's nod on LED-127 is not in the repository; its STATUS still reads "Confirmation pending".
