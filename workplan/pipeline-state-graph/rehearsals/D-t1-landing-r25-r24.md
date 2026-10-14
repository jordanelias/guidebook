# Rehearsal D-t1-r24-r25: land T1 (step 0.2), fold R25, add the root pointer (R24)

**Date:** 2026-10-13. **Clone:** `scratchpad/rehearsals/D-t1-r24-r25` (built from `/home/user/guidebook-t1`, never pushed). **Main tip used:** `31142552` (= `origin/main` `f54d09fd` plus the plan's workplan files; the conflict set is the same against either).

| part | verdict |
|---|---|
| (i) step 0.2, land T1 on current main | **EXECUTABLE WITH CHANGES.** The mechanics work as worded (main's blob + `migrate_db.py` applies 102–105 cleanly; `--rebuild` identical), but the step under-names its own conflict set and its same-PR edits: the baseline needs a hand merge (not `--write-baseline`), all five derived files must be regenerated (taking main's leaves five of six `--check`s stale), and R4's own probe `build_graph.py --check` goes red with three failures until the instrument is edited. T1's `scan_debt` lands red (468 pairs), which the done-when does not say. |
| (ii) R25, `term_catalogue_origins` → three columns on `terms` | **EXECUTABLE WITH CHANGES.** Done in migration 104 and its callers, every gate unchanged, net −49 hand-edited lines. Two consequences the ruling does not name: the per-term `rationale` has no column, and the approval check weakens from "these words occur once in the ledger" to "this entry heading occurs once". |
| (iii) R24, `root_id REFERENCES external_root_registry(root_id)` | **EXECUTABLE WITH CHANGES.** The rebuild preserves every dependent (22/22 views select with identical counts, view SQL verbatim, rows and `sqlite_sequence` identical, `--rebuild` identical, gates unchanged, walkability 21 → 19 failing). But the FK narrows a ratified field: DR-2026-07-13 H1 and `evidence-architecture.md` (a) let a `root_id` resolve through `root_ref_id`; under the FK it must be a registry row. No row or migration has ever written a `root_id`, so nothing is lost in data, but the ruling is not "agent" authority as written: it needs an owner-merged sentence, a ledger supersession line and an instrument atom edit in the same PR. |

---

## Baselines

All runs from the clone root; outputs under `scratchpad/rehearsals/D-t1-r24-r25_*`.

- **main @ 31142552** (separate clone `D-t1-r24-r25_mainbase`, whose `origin/main` is the stale local `main` = `3077b99`): `--all` 67 green / 7 examined nothing / 11 advisory red; `--selftest` PASS; `schema_reference_audit` PASS; `build_graph.py --check` 0 failures, 5 warnings; walkability 21 of 82 fail.
- **T1 tip + uncommitted refactor** (`03afa521`, the patch baseline): `--all` 70 / 10 / 9; `--selftest` PASS; `schema_reference_audit` PASS; `--rebuild` identical (85 tables, 22 views; `pipeline_runs` 5 → 0 exempt). `build_graph.py` does not exist on T1.

In the rehearsal clone I pointed `refs/remotes/origin/main` at `31142552` (local ref only) so the changeset-scoped checks see the PR's real diff. That is why the attestation gates read NOTHING-IN-SCOPE after the merge and PASS at the main baseline: T1 touches no synthesis path. It is not a regression.

---

## (i) Step 0.2: land T1

### What I did (exact commands)

```
S=/tmp/claude-0/-home-user-guidebook/db856d85-2082-5d35-9529-aa996506261b/scratchpad; ID=D-t1-r24-r25
git clone -q --shared /home/user/guidebook-t1 "$S/rehearsals/$ID" && cd "$S/rehearsals/$ID"
git checkout -q claude/t1-scan-contract-tooling                      # 4085c7d8
git -C /home/user/guidebook-t1 diff --binary > "$S/rehearsals/${ID}_t1-uncommitted.diff"
git apply --index "$S/rehearsals/${ID}_t1-uncommitted.diff"          # 12 files +386/-328
git commit -m "... T1 uncommitted refactor ..."                      # 03afa521 (patch baseline)
git fetch -q /home/user/guidebook 31142552e15d01f272a0734b9fb13a4a79a01756   # abbreviated SHA cannot be fetched
git merge --no-edit FETCH_HEAD                                       # 7 conflicts
git checkout --theirs -- data/guidebook.db && python3 scripts/migrate_db.py   # applies 102-105, 0 data migrations, user_version 105
git show :2:governance/research-contract-baseline.json | sed 's/"R16": 9,/"R16": 8,/' > governance/research-contract-baseline.json
bash scripts/regenerate_derived.sh && python3 scripts/generate/context_map.py
git add <the seven> && git commit                                     # dea3a84c
# R4's probe then fails 3 times; instrument edits, then:
python3 workplan/pipeline-state-graph/build_graph.py && python3 workplan/pipeline-state-graph/build_graph.py --check   # b9e1e14f
```

### The conflict set (measured)

`git diff --name-only 3077b99 FETCH_HEAD` ∩ `git diff --name-only 3077b99 HEAD` gave seven files, all of which conflicted:

| file | resolution | why |
|---|---|---|
| `data/guidebook.db` | main's blob, then `python3 scripts/migrate_db.py` | as the plan says; applies 102–105 with 0 data migrations; `--rebuild` identical |
| `governance/research-contract-baseline.json` | **hand merge**: main's `"R16": 8` plus T1's four new keys `R16-scan` 52, `R17` 2, `observation-quote-missing` 17, `observation-quote-unscoped` 37 | the hunk is not one line: T1 added four keys beside it. The four values were re-derived on the merged DB (`research_batch_dod.py`, `observation_verbatim_audit.py`) and came out unchanged. **`research_batch_dod.py --write-baseline` is not a substitute:** run on main's file it wrote `R16-scan` and `R17` but not the two observation-quote keys, which belong to `observation_verbatim_audit.py` (no writer); that check then fails "no baseline entry". `--check-baseline` against `31142552`: PASS, 4 NEW, 0 raised |
| `governance/context-map.yaml` | regenerate | taking main's: `context_map.py --check` exit 1 |
| `tools/data-atlas.html`, `tools/pipeline-completeness-dashboard.html`, `tools/pipeline-walk.html`, `tools/schema-walkability.html` | regenerate (`regenerate_derived.sh`) | taking main's: `--check` exit 1 for four of the five tools (`evidentiary_audit` was current). Regeneration also rewrites a fifth, non-conflicted file, `tools/spec-curation-vetting-surface.html` |

So "regenerate or take main's" is wrong for the derived files: only regeneration works. The step should also say to commit the refactor **before** the merge, not after. The plan has it after; merging into a dirty tree worked here only because none of the 12 refactor files is touched by main.

### R4's probe goes red when T1 lands (not in the plan)

`build_graph.py --check` after the merge: **3 failures**.
- `RES-17`, `RES-18`: quotes found in `governance/research-contract.yaml` but not near cited lines 321/322; T1's contract edit moved them to 352/353.
- `M03.t5`: needle `DELIBERATELY ABSENT: an un-decline verb` not found in `decline_parameter`, because T1 adds `revoke-declination`.

Same-PR edits I made (`b9e1e14f`, 6 files, +364/−82, of which `graph.json`, `STATE-GRAPH.md`, `CAPABILITIES.md` and `ATOMS.tsv` are regenerated):
- `atoms/atoms-contracts.jsonl`: RES-17 → `:352`, RES-18 → `:353`; RES-16's enforcement text drops "(+ T1 R16-scan, unmerged)".
- `machines.yaml`: M03.t5 `TERM → DECLINED` (no longer "terminal"; needles `REVERSING ONE is \`revoke-declination\`` and `is already declined, by`); new M03.t5r `DECLINED → TERM` via `revoke-declination`; M03.t6 now names `retire-parameter` and `merge-parameter`. Its old claim "merged and retired have NO writer on main" became false while its needle still passed: a green probe over stale prose (rule 7a).

After the edits: 0 failures, 5 warnings (the same as main).

### Probes the step names

From regenerated `graph.json`: `P-V` NOT-BUILT → PASS, `P-W` FAIL → PASS, `P-PARAM-LIFECYCLE` FAIL → PASS; `C1.3` FAIL → PASS, `C1.5` NOT-BUILT → PASS, `C2.5` FAIL → PASS, `C2.6` NOT-BUILT → PASS. No other probe or predicate changed.

### Gates

| check | main@31142552 | T1 tip+refactor | 0.2 merged | R25 | R24 |
|---|---|---|---|---|---|
| totals (`--all`) | 67 / 7 / 11 red | 70 / 10 / 9 | 68 / 11 / 10 | 68 / 11 / 10 | 68 / 11 / 10 |
| `scan_debt` (T1, advisory) | absent | PASS | **FAIL** | FAIL | FAIL |
| `context_map_fresh` | FAIL | PASS | PASS | PASS | PASS |
| `schema_walkability_fresh` | FAIL | PASS | PASS | PASS | PASS |
| `test_scan_contract`, `observation_verbatim_audit` | absent | PASS | PASS | PASS | PASS |
| `extraction_follow_up_audit` | absent | NONE | NONE | NONE | NONE |
| `attestation_presence`, `attestation_schema` (blocking) | PASS* | NONE | NONE | NONE | NONE |
| `adversarial_pass_recorded` | NONE | PASS | NONE | NONE | NONE |
| `--selftest` | PASS | PASS | PASS | PASS | PASS |
| `schema_reference_audit` | PASS | PASS | PASS | PASS | PASS |
| `build_graph.py --check` | 0 fail | n/a | **3 fail** → 0 after edits | 0 | 0 |
| `--rebuild` | n/a | identical | identical | identical | identical |
| walkability (IDEAL-GRAPH §6) | 21 of 82 | — | 21 of 85 | 21 of 84 | **19 of 84** |

\* The attestation and adversarial differences come from which ref the changeset is scoped against (stale `origin/main` in the main clone), not from the code.

All other checks have the same status in every column. Blocking checks are green throughout: `test_db_integrity`, `migration_reproducibility`, `identifier_floor_audit`, `judgment_handoff_shape`, `extraction_relations_integrity`, `research_contract_baseline_ratchet`, `research_contract_sync`. The diff-scoped gate on the final head (`run_checks.py --changed-from origin/main`, the substance of `preflight.sh`): PASS, 68 / 11 / 9; `research_tooling_separation` PASS (schema-only DB change).

**`scan_debt` goes red on landing.** It reports 468 (source, parameter) pairs NOT-READ: 52 sources × the 9 parameters batch 24 minted on main after T1 branched. T1's DB held 1 parameter; main holds 10. It is advisory and it is research debt (Phase 5), not a tooling defect, but it is a check red from the day it lands. The PR must say so, or the debt must be baselined.

### Measured

- T1 against main (`git diff --shortstat 31142552 dea3a84c -- . ':!data/guidebook.db'`): 35 files, +4,127 / −147. Of that, code (`scripts schemas tools .github skills`, excluding migrations and `tools/*.html`) is 19 files, +3,517 / −124. Migrations are 4 files, +364. The plan's figures re-derive exactly: committed 23 files +3,426/−94 (18 files +3,419/−87 without `tools/*.html`); uncommitted 12 files +386/−328.
- Merge resolution: baseline +5/−1; `context-map.yaml` +73/−4; five html files ±1–2 each.
- **The step ADDS lines**, as the plan says: it is the one sanctioned addition.

### Residual risk

- The `--write-baseline` trap above. A future rebase of the baseline file by script drops the observation-quote keys silently, and only `observation_verbatim_audit` notices.
- Every later schema migration in this plan collides with T1's numbers: COMMON's "start at 102" is wrong once T1 lands. The next free number is 106.
- [UNVERIFIED] "the rehearsal in #171's body" (the PR body was not read); T1's GitHub state (the branch is local only and must be pushed before a PR exists).

---

## (ii) R25: `term_catalogue_origins` → three columns on `terms`

### Callers swept

`git grep term_catalogue_origins`, outside `transcripts/`, `scratchpad/` and the plan's own `workplan/` files, plus `sqlite_master` (views and triggers: none; no FK into it; 0 rows; no data migration writes it). The callers:
- `scripts/migrations/104_vocabulary_lifecycle.sql`
- `scripts/db.py` (parser `choices`, `_resolve_catalogue_entry` docstring, `mint_term_from_catalogue`)
- `scripts/validate_parameters.py` (P2)
- `scripts/tests/test_scan_contract.py` (M05, M07, M10, M11, C01, C02, C03, CLI1)
- `schemas/base_parameter.py` (`TermCatalogueOrigin`) and `scripts/audit/validate_pydantic_schemas.py` (`MODEL_TABLE_MAP`)
- `governance/stage-map.yaml` (entry and comment)
- `governance/check-registry.yaml` (the `validate_parameters` note)
- generated: `governance/context-map.yaml`, `tools/*.html`, `workplan/pipeline-state-graph/{graph.json,STATE-GRAPH.md}`

Nothing else reads it.

### What I did (`a356e673`)

- **Migration 104**: the `CREATE TABLE term_catalogue_origins` and its comment are replaced by `ALTER TABLE terms ADD COLUMN catalogue TEXT CHECK (catalogue IN (<the same five paths>))`, `catalogue_entry_ref TEXT`, and `catalogue_approval_ref TEXT CHECK (<all three NULL> OR (catalogue IS NOT NULL AND length(trim(catalogue_entry_ref))>0 AND length(trim(catalogue_approval_ref))>0))`. The CHECK sits on the last column, which is the 078 pattern T1 already uses for `revoked_*`. `dbcore.schema_choices("terms","catalogue")` reads the five values from the ALTERed DDL.
- **`db.py mint-term-from-catalogue`**: one `INSERT INTO terms` carrying the three columns (the second INSERT is gone). `--approval-quote` becomes `--approval-ref`: the dated `## ` heading of the approving ledger entry, refused unless it occurs exactly once and carries a `YYYY-MM-DD`. `--rationale` is removed. `choices` and `check_declared` now point at `terms`.
- **`dbcore.ledger_heading_count()`** (+8): the one home of the lookup, used by the writer and by P2.
- **P2** reads `terms WHERE catalogue IS NOT NULL` and fails on a pointer that matches anything other than exactly one heading.
- `TermCatalogueOrigin` (33 lines) and its map entry are deleted. `terms` has no Pydantic mirror at all, so there is nothing to extend.
- The stage-map entry and comment clause, and the registry prose, are edited as text.
- Tests: M05 (an unknown pointer is refused), M07 (the row carries the three values), M10/M11 (P2 passes, then fails on an injected UPDATE and is restored), C01/C02/C03 (capture now looks for `"catalogue_approval_ref"` and replays `terms`), CLI1.
- The DB was rebuilt from main's blob with the edited 104 (`git show 31142552:data/guidebook.db > data/guidebook.db && python3 scripts/migrate_db.py`).

### Measured

| area | files | + | − | net |
|---|---:|---:|---:|---:|
| code (`scripts`, `schemas`, excl. migrations) | 6 | 77 | 111 | −34 |
| migration 104 | 1 | 22 | 34 | −12 |
| governance YAML | 2 | 5 | 8 | −3 |
| **hand-edited total** | **9** | **104** | **153** | **−49** |

Generated files (context map, html, graph) are extra. **Net negative.** One table, one Pydantic model, one map entry, one stage-map entry and one INSERT are gone.

### Gates

`test_scan_contract`: 103/103. `validate_parameters`: PASS (P2 examined 0 catalogue-minted terms). `--all`: identical to the merged state, check by check. `--selftest`, `schema_reference_audit` and `build_graph.py --check`: PASS. `--rebuild`: identical. Walkability: 21 of 84 (the dropped table was `ok`).

### Defects and deviations

1. **Rationale loss.** T1's table required `rationale`, and R25's three columns have no home for it. I dropped `--rationale`. The owner's accept-or-strike (SES-063) should see this. `created_at` and `created_by_session` were copies of the term row's own stamps, so they go without loss.
2. **The approval check weakens.** T1 proved the approving *words* occur once. The pointer proves an *entry* exists once, not that it approves this term. That is what "a pointer, not a quote copy" buys. The form ("date/anchor") was undetermined in the ruling. I chose the heading text because the ledger's entries are `## Owner … YYYY-MM-DD — …` headings and need no slug code.
3. **CLI change**: `--approval-quote`/`--rationale` become `--approval-ref`. No skill or runbook names the old flags (`git grep approval-quote`: db.py and tests only).

---

## (iii) R24: the root pointer

### Dependents enumerated (from `sqlite_master` and `PRAGMA foreign_key_list` on the merged database)

- **Views reading the table**, as a transitive closure: `v_root_id_conflicts`, `v_derived_figure_check`, `v_determination_provenance`, `v_unregistered_roots`, `v_scan_ledger` (T1, 103), `v_value_independence` (re-created by T1's 104). No view reads any of those six.
- **Indexes**: `idx_sve_ref`, `idx_sve_status`, `ix_sve_locator`, `idx_sve_slug_param`, `idx_sve_param_ref`. **Triggers**: none.
- **Inbound FKs**: `extraction_relations` (from and to), `specification_extraction_links`, `extraction_population_links`, `extraction_follow_ups` (T1, 105).
- **Outbound FKs**: 9. **AUTOINCREMENT**: `sqlite_sequence` 114 = max id. The two table CHECKs (claim/value and the lens `COALESCE`) and seven column CHECKs; `figure_role` and `comparator` were added by ALTER.
- **Rows**: 101; `count(root_id)` = 0. `external_root_registry`: 0 rows, no writer (`dbcore.writable_tables` excludes it).
- **Data migrations**: 25 INSERT into the table (111 statements, every one with an explicit column list; latest `20261001034401`); 12 UPDATE it (latest `20260925061025`). No committed migration has ever written a non-NULL `root_id`: the only "root_id" hits in UPDATEs are `root_ref_id`.

### What I did (`758b3a46`)

`scripts/migrations/106_root_pointer.sql` (366 lines), generated from the live `sqlite_master` and then frozen:
1. `CREATE TEMP TABLE _106_seq AS SELECT name, seq FROM sqlite_sequence`
2. drop the six views
3. `CREATE TABLE "_106_new_source_value_extractions"`: the live DDL verbatim, with only the `root_id` line changed to `root_id TEXT REFERENCES external_root_registry(root_id)` plus a two-line comment
4. `INSERT … SELECT` all 51 columns by name
5. `DROP`, then `ALTER … RENAME`
6. the five indexes, verbatim
7. restore the sequence
8. the six views, verbatim
9. `PRAGMA user_version = 106`

Marker: `-- AFTER_DATA: 20261010002423`, the latest data migration (`ls scripts/migrations/data_*.sql | sed -E 's/.*data_([0-9]{14})_.*/\1/' | sort | tail -1`).

In `db.py insert_extraction` (+9), an unregistered `--root-id` is refused in words before the INSERT. `amend-extraction` cannot write `root_id` (`_AMENDABLE_SVE_FIELDS`), so this is the only write path.

### Verification

- **Schema diff, live before vs after**: only the table's SQL changed. All other 204 named objects in `sqlite_master` are byte-identical, including the six recreated views. The table has 10 FKs (was 9). Row hash, column list, index set, `sqlite_sequence` (all tables) and the four children's FKs are all identical. `foreign_key_check` is empty; `integrity_check` is ok.
- **Views**: `select count(*)` from each of the 22 views, before and after, gives identical results: `v_best_practice` 0, `v_code_floor_only` 0, `v_convergence_sources` 69, `v_coverage_branch` 84, `v_coverage_jurisdiction` 27, `v_coverage_language` 20, `v_coverage_priority` 7190, `v_derived_figure_check` 0, `v_determination_provenance` 0, `v_divergence` 0, `v_evidence_authors` 53, `v_item_provenance` 0, `v_open_determination_gates` 1, `v_pending` 0, `v_pmp_latest_walk` 0, `v_registry_duplicate_descriptions` 0, `v_root_id_conflicts` 0, `v_scan_ledger` 520, `v_source_admission` 55, `v_source_reach_all` 83, `v_unregistered_roots` 0, `v_value_independence` 1. Every view's column list is identical too. Four of the six rebuilt views return 0 rows, so their verbatim SQL, not their counts, is the proof (rule 4).
- **FK behaviour on a scratch copy** with `foreign_keys=ON`: an unregistered `root_id` → `FOREIGN KEY constraint failed`; a registered one is accepted; deleting a referenced registry row is refused. The `db.py` dry-run refuses `ROOT-FIXTURE` in a sentence and writes with `root_id` NULL.
- **`--rebuild`**: identical, including the table's rows and `sqlite_sequence` (114). The only rebuild differences anywhere are the pre-existing bot divergence in `evidence_sources`, `evidence_source_authors` and their sequence, which is also present for main's live DB against its rebuild (CLAUDE.md rule 3).
- **Gates**: identical to R25 check by check (68 / 11 / 10); blocking all green.
- **Walkability script, before and after**: 21 → 19 of 84 failing. `external_root_registry` goes from `up down orphan` to `ok`, and `source_value_extractions` from `unFK:root_id` to `ok`. Still failing: `access_duration access_stakes lang_jur_map life_stage_modifiers situations url_verification_runs bpc_metadata data_migrations pipeline_runs weighting_profile citation_mining reference_stubs research_code_leads search_coverage search_languages source_locators conflicts connection_targets connections`.

### Two experiments (not committed)

- **Without the marker**, `--rebuild` is also identical. The marker is what R6 requires for a table that committed data migrations write, and it is harmless (it moves only 106 and later-numbered migrations after all data). But it is **not load-bearing on today's data**: no committed migration writes a non-NULL `root_id`, and every INSERT names its columns. The plan should not claim the rebuild fails without it.
- **A `PRAGMA writable_schema` variant** (`UPDATE sqlite_master SET sql = replace(...)` on the one line): 8 lines instead of 366, `integrity_check` ok, `--rebuild` identical to its own live state. SQLite documents that route for *removing* constraints, not adding them, so I do not recommend it without the owner's acceptance. It is recorded because the owner asked for the least code.

### Defects in the ruling, and residuals

1. **The FK narrows a ratified field.** DR-2026-07-13 H1 defines `root_id` as the "shared identifier for one evidentiary root", with `root_ref_id` the FK "when the root document is in corpus". `governance/evidence-architecture.md:106` (a) says "a `root_id` must resolve either to a `root_ref_id` in `evidence_sources` or to a registered external-root stub". `v_unregistered_roots` flags an unregistered `root_id` only when `root_ref_id IS NULL`, and `v_root_id_conflicts` exists for rows carrying both. Under the FK, every non-NULL `root_id` must be a row of the *external* registry, even for an in-corpus root, and the `'unregistered'` branch of `v_unregistered_roots` becomes structurally empty. The data cost is zero (no row and no migration has ever set `root_id`), and `COALESCE(root_ref_id, root_id)` still counts in-corpus roots through `root_ref_id`. But R24's premises omit H1 and (a), and its authority ("agent") is too low. The same PR needs: a ledger line recording the supersession (rule 0), the (a) sentence amended (owner merge), and atom `EVI-162` updated. When I amended (a) in the clone, `build_graph.py --check` failed on EVI-162, so I reverted the amendment and left it for the owner.
2. **The DB file grows 240 KB** (5,128,192 → 5,373,952 bytes): the dropped table's pages are free and nothing VACUUMs. This is harmless and the rebuild reproduces it.
3. **Combine rebuilds.** R37 NULL-forwards `source_value_extractions.slug`, which is `NOT NULL REFERENCES slugs(slug)`. Dropping a NOT NULL also needs a rebuild of this table. If R37 is taken, do it in the same migration, so the table is rebuilt once.
4. **The marker must be re-derived when the plan's migrations are stacked**, and the migration renumbered (106 assumes T1 is 102–105).

### The missing writer: GAP shape only (not built; rule 10)

`external_root_registry` columns:
- `root_id` TEXT PK
- `description` NOT NULL
- `root_type` CHECK, the same five values as `source_value_extractions.root_type`
- `provenance`, `root_population_note`, `notes`
- `created_at`, `created_by_session`

Readers: `v_value_independence` (K23), `v_unregistered_roots`, `v_registry_duplicate_descriptions`, and now the FK.

What the verb needs, in a tooling-only PR:
- one verb (for example `add-root`), whose `root_id` is minted by a derived next-id rule and never typed (rule 8);
- `--description`, non-blank, refusing a normalised duplicate of an existing description. That is the condition `v_registry_duplicate_descriptions` reports after the fact, and the anti-gaming purpose in (a): "so two extractors cannot mint two ids for one root".
- `--root-type` from the column's CHECK (`dbcore.schema_choices`);
- `--provenance` as a pointer to a persisted payload or citation (CLAUDE.md 5(c)), never written from memory;
- a refusal when the root is an admitted source (that root belongs in `--root-ref-id`);
- `dbcore.stamp_for` stamps.

Until it ships, `--root-id` is refused in words. That costs nothing today because no row uses it.

---

## What the v4 plan must say

**Step 0.2** (replace the cell):

> **0.2 Land T1** (owner-approved, LED-206; R25 folded in first). In the T1 worktree (`/home/user/guidebook-t1`, `claude/t1-scan-contract-tooling`, base `3077b99`, local only):
> 1. Commit the stress-tested refactor (12 files, +386/−328, `git diff --shortstat`).
> 2. Apply R25 to migration 104 and its callers (below). T1 is unmerged, so 104 may still be edited.
> 3. Run `git merge origin/main`. Seven files conflict (measured 2026-10-13): `data/guidebook.db`, `governance/research-contract-baseline.json`, `governance/context-map.yaml`, `tools/data-atlas.html`, `tools/pipeline-completeness-dashboard.html`, `tools/pipeline-walk.html`, `tools/schema-walkability.html`. Resolve them as follows:
>    - The database: `git checkout --theirs -- data/guidebook.db && python3 scripts/migrate_db.py` (applies 102–105 and 0 data migrations; `user_version` 105).
>    - The baseline, by hand: main's `"R16"` plus T1's four new keys (`R16-scan`, `R17`, `observation-quote-missing`, `observation-quote-unscoped`), each re-derived on the merged database with `research_batch_dod.py --all` and `observation_verbatim_audit.py`. Do not use `--write-baseline`: it does not write the two observation-quote keys.
>    - The other five, by regeneration only: `bash scripts/regenerate_derived.sh && python3 scripts/generate/context_map.py`. Taking main's copies leaves them stale.
> 4. Same-PR instrument edits, or R4's probe fails (3 failures measured):
>    - `atoms/atoms-contracts.jsonl`: RES-17 and RES-18 cite `governance/research-contract.yaml:352` and `:353`.
>    - `machines.yaml`: M03.t5 loses "NO un-decline verb" and its needle; a `DECLINED → TERM` transition via `revoke-declination` is added; M03.t6 names `retire-parameter` and `merge-parameter`.
>    - Then run `build_graph.py`.
> 5. Gate, then open the PR. Expect `--all` at 68 green / 11 examined nothing / 10 advisory red. The one new red is T1's own advisory `scan_debt`: 468 pairs, because batch 24 minted nine parameters on main after T1 branched. That is Phase 5 research debt, and the PR says so. `--rebuild` is identical.
>
> Migrations 102–105 take the next four numbers, so every later schema migration in this plan starts at 106. **Done when** `P-V`, `P-W`, `P-PARAM-LIFECYCLE`, C1.3, C1.5, C2.5 and C2.6 pass (all measured PASS) and `build_graph.py --check` reports 0 failures.

**R25, inside 0.2:**

> In migration 104, replace `CREATE TABLE term_catalogue_origins` with three nullable columns on `terms`: `catalogue` (the five-path CHECK), `catalogue_entry_ref` and `catalogue_approval_ref`, with the all-or-none CHECK on the last.
>
> `mint-term-from-catalogue` writes the three columns in its single `INSERT INTO terms`. It takes `--approval-ref`, the dated `## ` heading of the approving ledger entry, which must occur exactly once (`dbcore.ledger_heading_count`). It no longer takes `--approval-quote` or `--rationale`.
>
> Same-PR edits:
> - `validate_parameters.py` P2 reads `terms WHERE catalogue IS NOT NULL`.
> - Delete `TermCatalogueOrigin` and its `MODEL_TABLE_MAP` entry.
> - Delete the stage-map entry and its comment clause.
> - Edit the `validate_parameters` registry note.
> - In `test_scan_contract.py`, update M05, M07, M10–M11, C01–C03 and CLI1.
>
> No view, trigger, FK or data migration reads the table. Measured: 9 hand-edited files, +104/−153. The owner's accept-or-strike covers two losses: the per-term rationale, and the approval check, which now proves an entry exists, not that it names these words.

**The root-pointer step** (new, Phase 3 judgment, after T1):

> **Root pointer (R24).** One schema migration, numbered after T1's, rebuilds `source_value_extractions` with `root_id TEXT REFERENCES external_root_registry(root_id)`, nullable, by the 081 procedure:
> 1. Save `sqlite_sequence` to a temp table.
> 2. Drop the views that read the table, re-derived at execution as the transitive closure over `sqlite_master` (six on 2026-10-13: `v_root_id_conflicts`, `v_derived_figure_check`, `v_determination_provenance`, `v_unregistered_roots`, `v_scan_ledger`, `v_value_independence`).
> 3. Create the new table from the live DDL, changing only the `root_id` line, and `INSERT … SELECT` every column by name.
> 4. Drop the old table and rename the new one.
> 5. Recreate the five indexes and the views verbatim from their stored SQL.
> 6. Restore the sequence.
>
> The four child tables need no edit. Declare `-- AFTER_DATA: <latest data migration>` (re-derive it: `ls scripts/migrations/data_*.sql | sed -E 's/.*data_([0-9]{14})_.*/\1/' | sort | tail -1`). Twenty-five data migrations INSERT into this table and twelve UPDATE it. The marker is R6-compliant but not load-bearing today, because no committed migration writes a `root_id`.
>
> `insert_extraction` refuses an unregistered `--root-id` in words (+9 lines). If R37 is taken, drop `slug`'s NOT NULL in the same rebuild.
>
> **Owner merge, same PR:** the FK makes `root_id` registry-only, against DR-2026-07-13 H1 ("shared identifier") and `evidence-architecture.md` §(a) ("resolve either to a `root_ref_id` … or to a registered external-root stub"). Record the supersession in the ledger, amend (a), and update atom EVI-162, or `build_graph.py --check` fails.
>
> File the registry's writer as a GAP: a minted id, a non-blank description that refuses a normalised duplicate, `root_type` from the CHECK, provenance as a pointer, and a refusal for in-corpus roots.
>
> **Done when:** every view selects with unchanged counts and verbatim SQL; `--rebuild` is identical (including `sqlite_sequence`); gates are unchanged; the walkability script drops `external_root_registry` and `source_value_extractions`.
>
> Measured: migration 366 lines (an 8-line `writable_schema` variant exists and is not recommended), code +9.

---

## Files

- Patches (all exclude `data/guidebook.db` and the regenerated `tools/*.html`):
  - `D-t1-r24-r25.patch`: `03afa521..HEAD`, the brief's baseline. It also excludes `transcripts/` and `scratchpad/`, and it includes main's own changes since `3077b99`.
  - `D-t1-r24-r25-vs-main.patch`: `31142552..HEAD`, which is what stacks on main.
  - per-step patches: `-step0.2-instrument.patch`, `-R25.patch`, `-R24.patch`.
- Gate outputs: `D-t1-r24-r25_gates_{merged,r25,r24}/` (`all.txt`, `summ.tsv`, `selftest.txt`, `sra.txt`, `bg.txt`, `cmp.txt`, `views.tsv`, `walk.tsv`); baselines `D-t1-r24-r25_{mainbase,t1base}_*`; R24 snapshots `D-t1-r24-r25_sve_{before,after}.txt`, `_views_{before,after}_r24.tsv`, `_walk_{before,after}_r24.tsv`.
- Helpers: `D-t1-r24-r25_tools/` (`gates.sh`, `cmp_rebuild.py`, `summ.py`, `viewcounts.py`, `svesnap.py`, `walk.py` = IDEAL-GRAPH §6 lines 606–633).

## Not verified

- PR #171's body; T1's remote state.
- Whether the owner accepts R24 or R25 (SES-063).
- The `writable_schema` variant's safety beyond `integrity_check` and `--rebuild`.
- An antagonist pass was not run (R7).
- `migration_reproducibility_deep` (advisory, red throughout) was not investigated; its divergence predates this work.
