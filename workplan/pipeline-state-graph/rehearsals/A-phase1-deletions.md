# A2 rehearsal report: Phase 1 (steps 1.1 to 1.9), finished and re-verified by A2b-finish

Clone: `/tmp/claude-0/-home-user-guidebook/db856d85-2082-5d35-9529-aa996506261b/scratchpad/rehearsals/A2-phase1`
Base: `31142552`. A2-phase1's nine commits: `cba0d24` 1.1, `dde0ff4` 1.2, `7faa1b4` 1.3, `ecc8fd3` 1.4, `bd26594` 1.5, `ef2a655` 1.6, `c9f9c2b` 1.7, `0b1d88c` 1.8, `9cef95e` 1.9.
A2b-finish added three small fix commits on top (section 7): `b8ca6b8`, `87185b1`, `323a746` (HEAD).
Patch: `A2-phase1.patch` (`git diff 31142552..HEAD -- . ':!data/guidebook.db'`, 177 files, +492 / -31,267; checked with `git apply --check` against a base worktree).
Everything below marked "re-verified" was run by A2b at HEAD `323a746`. Per-step gate tables for the intermediate commits are copied from A2-phase1's logs (`A2-phase1_s1N_*.txt`) and are claims, except where A2b's own checks cover the same facts (stated).

---

## 0. Verdicts

Verdict first: Phase 1 is executable and every gate at HEAD is no worse than baseline, but the plan's same-PR lists (section 5a) are incomplete for six of nine steps, and two of the instrument's fifteen mutation tests (`build_graph.py --selftest`, which no gate runs) were broken by the deletions (fixed here).

| step | verdict | one-line reason |
|---|---|---|
| 1.1 render apparatus | EXECUTABLE WITH CHANGES | green, but the 5a list omits the `context_map_fresh` basis re-point (selftest C7 fails without it), instrument edits (2 atoms, 1 probe, 1 predicate, 1 conflict, line re-anchors), `retired-vocabulary.yaml` exemptions, the CLAUDE.md section 3 `render` row, and four unlisted deleted files |
| 1.2 item-layer cluster | EXECUTABLE WITH CHANGES | `schemas/item.py`, `bootstrap.sh`, `migration_reproducibility.py` (blocking `schema_reference_audit` fails without it) are not in the list; three edits are wasted because 1.3/1.4 delete the files |
| 1.3 splinter and case-study children | EXECUTABLE WITH CHANGES | `population_integrity_audit` has to be deleted here, not in 1.6(a); otherwise as written |
| 1.4 axes as one act | EXECUTABLE AS WRITTEN | list complete apart from the generic atom re-anchoring (rule in section 8); `AFTER_DATA` marker is mandated by R3, not by the plan text |
| 1.5 scheduled workflows | EXECUTABLE AS WRITTEN | list complete apart from generic re-anchoring; `pipeline_runs` held 6 rows, not 5 |
| 1.6 checks diet | EXECUTABLE WITH CHANGES | plan's "delete `validate_population` only if confirmed enforced" is not satisfied for its P1 (enum drift); owner-gated doc edits (tier-system, evidence-architecture) and eight deleted atoms are unlisted; R4 and R22 clauses left unexecuted |
| 1.7 skills diet | EXECUTABLE WITH CHANGES | the "nothing broke" note in 5a is wrong in latent form: 23 committed attestations name rule ids that only the deleted skills supplied |
| 1.8 registry prose | EXECUTABLE AS WRITTEN | 54 fields / 837 lines removed (plan estimate 900 to 940 net, 1,044 gross) |
| 1.9 empty orphan tables | EXECUTABLE WITH CHANGES | two skills call `update-bpc` / query `bpc_metadata` (unlisted); the frozen coverage verbs in `db.py` still name the dropped grids; one prose line cannot be edited without deleting an instrument atom |

---

## 1. Re-verification at HEAD (A2b ran these)

Baseline used: `A2-phase1_baseline2_all.txt` (second baseline, same tree 31142552; 85 registered, 5 quarantined, 63 green / 11 nothing-in-scope / 11 advisory red). The first baseline (`A2-phase1_baseline_all.txt`: 67 / 7 / 11) differs only in changeset-scoped checks (`research_tooling_separation`, `attestation_presence`, `attestation_schema`, `attestation_verdict`) that read PASS or NONE depending on the diff in scope.

`research_tooling_separation`: PASS at HEAD (examined 176). The clone's `origin/main` is `31142552`, the base, so it is not stale; no rerun against the base was needed.

| gate | baseline (31142552) | HEAD 323a746 |
|---|---|---|
| `run_checks.py --all` | 85 registered; 63 green, 11 NONE, 11 advisory red | 70 registered (1 quarantined); 56 green, 7 NONE, 7 advisory red |
| red set | migration_reproducibility_deep, validate_schema_cross_check, validate_pydantic_schemas, retired_vocabulary, research_protocol_audit, metadata_integrity_audit, validate_reasoning, schema_walkability_fresh, context_map_fresh, site_pages_fresh, source_locators_integrity | the first six and `context_map_fresh` only; the other four were deleted with their entries. No check changed from PASS or NONE to FAIL. |
| registry delta | | 16 entries removed (evidentiary_audit_fresh, pipeline_completeness_fresh, pipeline_walk_fresh, pmp_audit, population_integrity_audit, reasoning_doc_citations_audit, render_audit_browser, schema_walkability_fresh, site_pages_fresh, source_locators_integrity, test_url_verifier, test_verification_pipeline, validate_axes, validate_bpc, validate_population, validate_reasoning); 1 added (`adjudication_integrity`, promoted from quarantine); `context_map_fresh` basis changed; all other loaded entries identical (YAML-level comparison) |
| red-check detail | retired_vocabulary 86 occurrences; validate_pydantic_schemas 213 findings plus a `bpc_metadata` import error | 73 occurrences, 0 dead exemptions; 192 findings, no import error; research_protocol_audit 18 issues and metadata_integrity_audit 19 rows unchanged; migration_reproducibility_deep fails on `evidence_sources` only, as before |
| `run_checks.py --selftest` | PASS | PASS (`contract criteria with no check claiming them: 6 of 30`, was 6 of 36) |
| `schema_reference_audit.py` | PASS | PASS (811 references, 201 files, 75 live tables and views) |
| `build_graph.py --check` | 0 failures, 5 warnings | 0 failures, 5 warnings (54 tables placed) |
| `build_graph.py --selftest` | 15/15 PASS | **2 FAIL at A2-phase1's HEAD (first red at 1.2 and 1.3; no gate runs it)**; 15/15 PASS after A2b fix `b8ca6b8` |
| `run_checks.py --changed-from origin/main --explain` | n/a | PASS, 56 / 7 / 7, same red set |
| `migrate_db.py --rebuild` | 83 tables incl. sqlite_sequence, 21 views, 164 indexes, row-count diff `pipeline_runs (6 vs 0)` only | user_version 106; 55 tables incl. sqlite_sequence, 20 views, 1 trigger, 110 indexes; table, view, trigger, index sets identical; **every row count identical**; DDL text identical |

Rebuild comparison detail (script `A2b_work/cmp.py`): full-row hash differs in `data_migrations`, `evidence_sources`, `evidence_source_authors` and `sqlite_sequence` only. The same four differ between base `data/guidebook.db` and its own rebuild, so this is the standing bot divergence (CLAUDE.md rule 3, `migration_reproducibility_deep`), not a Phase 1 effect. Separately, applying migrations 102 to 106 with `migrate_db.py` to a copy of the base blob produced a database identical, row for row, to the committed `data/guidebook.db` at HEAD (so the committed blob is exactly base plus the five migrations). `--rebuild` replays 50 schema and 139 data migrations (base: 45 and 139); the pre-existing advisory "158 FK violations after 081_icf_registry.sql" is unchanged.

Other things A2b checked at HEAD: all views compile (`select * from v limit 0`); `PRAGMA foreign_key_check` empty; no foreign key anywhere points at a dropped table (base scan of `PRAGMA foreign_key_list`: one hit, `conflicts.item_code -> items`, handled by 102); the only view or trigger in `sqlite_master` that named a dropped table at base was `v_pmp_latest_walk` (dropped in 102); `trg_spec_retire_needs_reason` is intact; every remaining `schemas/` module imports; `py_compile` passes on `scripts/`; `db.py add-item` is now "invalid choice", `coverage --slug` works, and `add-conflict` writes a row into the rebuilt `conflicts` table (scratch copy only; the committed blob sha is unchanged).

---

## 2. Measurements, per step

Lines are `git diff --numstat` of each commit, `data/guidebook.db` excluded. "Budget metric" is the plan's section 1 definition (scripts py/sh, tools py, schemas, workflows, skills; migrations excluded; `render_audit.js` and `tools/README.md` are outside it and listed under "other").

| step | files | + / - total | budget metric removed / added / net | migrations added | registry +/- | governance yaml +/- | instrument +/- | generated html - | other +/- |
|---|---:|---:|---|---:|---|---|---|---:|---|
| 1.1 | 64 | 38 / 18,509 | 7,144 / 15 / -7,129 (tools 5,053, scripts 1,937, workflows 154) | 0 | 1 / 169 | 6 / 38 | 11 / 34 | 6,429 | 5 / 4,309 (audits 4,284, `.ignore` 16, CLAUDE.md 9) |
| 1.2 | 45 (+DB) | 168 / 2,917 | 2,831 / 58 / -2,773 (skills 1,617, scripts 1,014, schemas 200) | 81 | 0 / 19 | 1 / 32 | 23 / 23 | 0 | 5 / 7 |
| 1.3 | 9 (+DB) | 32 / 273 | 243 / 1 / -242 | 31 | 0 / 17 | 0 / 6 | 0 / 0 | 0 | 0 / 0 |
| 1.4 | 8 (+DB) | 59 / 187 | 142 / 1 / -141 | 38 | 0 / 16 | 0 / 9 | 20 / 20 | 0 | 0 / 0 |
| 1.5 | 19 (+DB) | 85 / 2,960 | 2,867 / 15 / -2,852 (scripts 2,582, workflows 285) | 28 | 0 / 26 | 2 / 4 | 40 / 55 | 0 | 0 / 8 |
| 1.6 | 19 | 101 / 2,350 | 2,033 / 24 / -2,009 | 0 | 14 / 211 | 5 / 35 | 55 / 63 | 0 | 3 / 8 |
| 1.7 | 43 | 8 / 3,045 | 2,990 / 0 / -2,990 | 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 | 8 / 40 (skill-registry) |
| 1.8 | 1 | 1 / 837 | 0 | 0 | 1 / 837 | 0 / 0 | 0 / 0 | 0 | 0 |
| 1.9 | 11 (+DB) | 43 / 240 | 235 / 9 / -226 | 33 | 0 / 0 | 0 / 4 | 0 / 0 | 0 | 1 / 1 |
| A2b fixes | 4 | 17 / 9 | 2 / 4 / +2 (selftest fixtures) | 0 | 0 | 0 | 11 / 5 | 0 | 2 / 2 |
| **sum of 1.1 to 1.9** | 175 distinct (219 file-edits) | 535 / 31,318 | **18,485 / 123 / -18,362** | 211 | 16 / 1,295 | 14 / 128 | 149 / 195 | 6,429 | 22 / 4,373 |
| cumulative diff, 1.1 to 1.9 | 175 | 477 / 31,260 | | | | | | | |
| cumulative diff incl. A2b fixes (the patch) | 177 | 492 / 31,267 | | | | | | | |

Columns do not cover: `render_audit.js` 303 and `tools/README.md` 83 (1.1), `known_debt.yaml` 7 (1.3), and the 20 `.claude/skills` link lines (5 in 1.2, 15 in 1.7), which `areas.py` counts under skills but the budget metric does not. The sum of steps exceeds the cumulative diff because some lines (atom anchors, `stage-map.yaml`, `check-registry.yaml`) are edited in more than one step.

Does any step add more than it removes? No. Every step is net negative in total lines and in the budget metric. Steps 1.2 to 1.6 and 1.9 add lines in categories that are not the budget metric: 211 migration lines (additive history, five files), instrument anchor rewrites (143 anchor edits on 90 atoms, net zero lines), and 123 lines added to scripts and skills (replacement fixtures, docstring rewrites). The three A2b fixes add 17 lines and remove 9 (self-test fixtures and prose).

Plan section 1 table at HEAD (plan commands, run at base and HEAD; base column reproduces the plan's figures exactly):

| area | base | HEAD | change |
|---|---:|---:|---:|
| scripts (py + sh) | 46,510 | 38,614 | -7,896 |
| of which scripts/audit | 12,575 | 10,947 | -1,628 |
| of which db.py + dbcore.py | 10,618 | 10,230 | -388 |
| of which scripts/tests | 6,398 | 5,435 | -963 |
| of which generate + generate_parts | 2,438 | 553 | -1,885 |
| tools py | 5,053 | 0 | -5,053 |
| schemas | 5,698 | 5,356 | -342 |
| check-registry.yaml | 2,525 | 1,246 | -1,279 |
| active skills (`skills/*_SKILL.md`) | 9,871 | 6,399 | -3,472 |
| workflows | 714 | 275 | -439 |
| migrations | 184 files, 20,061 lines | 189 files, 20,272 lines | +5 files, +211 |

Other whole-tree figures: tracked files 3,601 to 3,489; tables 82 to 54; views 21 to 20; `db.py` verbs 72 to 64 (removed: add-item, items, add-audit-run, update-audit-run, audit-runs, add-jurisdictional-value, synonyms, update-bpc); registered checks 85 to 70; quarantined 5 to 1; contract criteria 36 to 30; `.claude/skills` links 41 to 21.

---

## 3. The plan's measured deletion figures, re-derived

Re-derived with `wc -l` / `git show 31142552:<path>` on the named files, then compared with what the commits removed.

| step | plan | re-derived from base tree | what the commit(s) actually removed |
|---|---:|---|---|
| 1.1 | 7,423 | 5,053 (6 tools py) + 183 (154 yml + 29 sh) + 1,884 (233 + 362 + 282 + 535 + 472) + 303 = **7,423 exact** | 18,509 total: the 7,423 plus 6,429 generated HTML (tools/*.html 3,738; site css 2,170; parts/v10 521), 4,284 audits/evidentiary-base-audit* and 83 tools/README (not in the plan), 169 registry lines, 100-odd lines of edits |
| 1.2 | 2,071 | 297 + 187 scripts = 484; skills 330 + 244 + 414 + 251 + 123 + 225 = 1,587; **2,071 exact** | 2,917: adds `schemas` 200, `db.py` about 293 lines changed, `test_db_integrity` 48, `extract_db` 43, `gap_mining_audit` 35, `graph_audit` 33, and the other edited scripts and skills |
| 1.3 | tables only | n/a | -273 / +32: `population_integrity_audit.py` -189 (moved forward from 1.6(a)), `schemas/population_links.py` -50, registry -17, others small |
| 1.4 | 158 | `validate_axes.py` is 158 lines at base **exact** | 137 in this commit (21 lines were already edited out in 1.2); total -187 / +59 |
| 1.5 | 2,775 | 1,092 + 554 + 480 + 364 + 149 + 136 = **2,775 exact** | 2,960: adds `test_db_integrity` 53, registry 26, `research_batch_dod` about 36 lines changed, small edits |
| 1.6(a) | 1,174 | 234 + 123 + 455 + 191 + 171 = **1,174 exact** | 983 in this commit; `population_integrity_audit` (189 after a 2-line edit in 1.2) went in 1.3. Also deleted but outside the 1,174: `validate_population` 251, `source_locators_integrity` 116, `validate_reasoning` 336, `validate_bpc` 311 = 1,014 |
| 1.7 | 1,834 + 1,156 = 2,990 | 15 skills 1,834 and `skills/deprecated/` 12 files 1,156 = **2,990 exact** | 3,005 skill lines (2,990 + 15 `.claude/skills` link lines) |
| 1.8 | 1,044 gross; about 900 net of earlier steps | base registry: note 854 + floor_basis 106 + reason 75 + prior_note 9 = 1,044 (72 fields) **exact** | 837 lines, 54 fields (note 42 / 722 lines, floor_basis 11 / 106, reason 1 / 9); 207 prose lines had already gone with entries deleted in 1.1 to 1.6, so the plan's net estimates (902 and 939) were 65 to 100 lines high |
| total | 17,635 | 7,423 + 2,071 + 158 + 2,775 + 1,174 + 2,990 + 1,044 | the named items realise 16,591 (code) + 837 = 17,428; the budget metric actually removed 18,485 lines of py/sh/yml/skills (plus `render_audit.js` 303 outside it), because the unmeasured tables, verbs, tests and mirrors (about 2,200 lines) came out as well |

Plan's "5 pipeline_runs rows" is stale: the table held 6 at base (a sixth bot run, 2026-10-12 06:09). Also stale: the plan's phase_4 figures "1, 1, 2" (rows show 0, 0, 1, 1, 2, 1).

---

## 4. Step by step

Each step below lists what was done, the non-obvious edited files, defects, deviations from the wording, residual risk, and the exact text the v4 plan needs. Gate results for intermediate commits are from A2-phase1's logs; the pattern is: registered 79, 78, 77, 76, 74, 70, 70, 70, 70 after steps 1.1 to 1.9; green 60, 60, 60, 59, 57, 56, 56, 56, 56; NONE 10, 9, 8, 8, 8, 7, 7, 7, 7; advisory red 9, 9, 9, 9, 9, 7, 7, 7, 7; `schema_reference_audit` PASS, `--selftest` PASS and `--rebuild` table, view, row-count and DDL identical at every step (with `pipeline_runs (6 vs 0)` until 1.5); `build_graph --check` 0 failures at every step except 1.9 as first run (see 1.9), 0 at HEAD.

### 1.1 Render apparatus (`cba0d24`): EXECUTABLE WITH CHANGES

Done: deleted `tools/` entirely (6 py, 7 html, README), the five renderers, `regenerate-derived.yml`, `regenerate_derived.sh`, `render_audit.js`, `parts/v10` (15), `site/assets/guidebook.css`, `audits/evidentiary-base-audit*` (4); `specs/e-08-brief.html` moved to `_archived/specs/` (rename). 64 files (42 D, 21 M, 1 R). Registry: removed the five entries and `render_audit_browser` as text edits (YAML re-loaded and compared: identical apart from the deletions). `--rebuild` unaffected (no schema change).

Non-obvious files: `governance/check-registry.yaml` (`context_map_fresh` basis `render/render-freshness` to `hygiene`), `governance/retired-vocabulary.yaml` (13 exempt_path lines removed across 8 entries), `workplan/pipeline-state-graph/{atoms/atoms-claude.jsonl, atoms/atoms-contracts.jsonl, build_graph.py, capabilities.yaml, conflicts.yaml}`, `CLAUDE.md`, `scripts/run_checks.py`.

Deviation: deletes four files the plan does not name (`tools/README.md`; `audits/evidentiary-base-audit.csv`, `.json`, `.md`, `-items.csv`, 4,284 lines, outputs of the deleted generator, hidden from searches by `.ignore`).

Defects found: none in the commit. A2b found two `.claude` prose callers (`.claude/agents/repo-sweep.md:19`, `.claude/commands/orient.md:29`) still telling readers `.ignore` hides `tools/*.html`; fixed in `87185b1`.

Residual risk: `governance/check-registry.yaml` `kinds.render.paths` (parts/**, site/**, specs/**, tools/*.html, audits/evidentiary-base-audit*) and the path fixtures at `scripts/run_checks.py:714-724` still name deleted paths (string classification only, no gate); `parts/{88_to_90,_archived,deprecated}/_MOVED.md` and `assets/guidebook.css` remain; prose callers remain in `architecture/`, `references/tooling-register.md`, `governance/` and frozen `workplan/` records.

v4 text, same-PR edits for 1.1 (replace the 5a row):
- Registry (text edit): remove `pipeline_completeness_fresh`, `evidentiary_audit_fresh`, `schema_walkability_fresh`, `pipeline_walk_fresh`, `site_pages_fresh`, `render_audit_browser` (and the `# DELETED 2026-09-10 (P7)` comment block above it); change `context_map_fresh` `basis: render/render-freshness` to `basis: hygiene` (selftest C7 fails otherwise: tested).
- `governance/schema-reference-exemptions.yaml`: remove keys `room`, `room_item_population`, `room_dar_provision`, `room_conflict`, and clause (3) of the `specification` key (blocking `schema_reference_audit` fails on a stale key: tested).
- Contract (owner merge): remove criterion `render-freshness`.
- `governance/retired-vocabulary.yaml`: remove the `.github/workflows/regenerate-derived.yml` exempt_path from RV-005, RV-006, RV-007 and the `scripts/generate/spec_page.py` and `tools/regenerate_vetting_surface.py` exempt_paths from the five entries that list them (advisory: 3 dead exemptions if left).
- Instrument (required by `build_graph.py --check`): delete atoms CLM-050 and PIP-07; delete probe P-I (`build_graph.py`), predicate C4.7 (`capabilities.yaml`), conflict C-027 and PIP-07 from the item-layer conflict's atom list (`conflicts.yaml`); re-anchor the `source` line of every atom whose cited line moved by more than three (rule in section 8).
- `CLAUDE.md` (owner merge): section 3 table `render` row, the "Don't hand-edit generated output" bullet, the "`tools/*.html` are hidden" bullet.
- Delete also: `tools/README.md`, `audits/evidentiary-base-audit*`.
- Text only, no gate: `.ignore` block, `scripts/preflight.sh` (2 hunks), comments in `dbcore.py`, `db.py`, `audit_evidence_metadata.py`, `generate/context_map.py`, `generate/research_contract_hook.py`, `audit/column_vocabulary_audit.py`, `audit/migration_reproducibility.py`, `stage-map.yaml` header, `.claude/agents/repo-sweep.md`, `.claude/commands/orient.md`; `run_checks.py` selftest C5 assertion about `render_audit_browser` (vacuous after deletion, optional).

### 1.2 Item-layer cluster (`dde0ff4`, migration 102): EXECUTABLE WITH CHANGES

Done: migration 102 drops 12 tables (items, item_audit_runs, item_bpc_links, item_taxonomy_links, item_population_elaborations, term_item_links, room_items, case_study_specs, economics_entry_specs, spec_value_probes, probe_population_links, jurisdictional_values) and view `v_pmp_latest_walk`, and rebuilds `conflicts` without the `items` FK (DDL compared with base: same columns, CHECK, indexes; a row can be written through `db.py add-conflict`). Children dropped before parents; `PRAGMA user_version = 102`; no `AFTER_DATA` marker. Verified: every data migration that writes a dropped table (`jurisdictional_values` 20260821185244 and 20260821185514, `item_taxonomy_links` 20260901183203, and the deletes of `item_taxonomy_links`, `items`, `jurisdictional_values` and `term_item_links` in 20260901205639) is dated before 095's marker 20260920060857, and `--rebuild` is identical. 45 files (+ DB; 15 D, 29 M, 1 A). Verbs removed: add-item, items, add-audit-run, update-audit-run, audit-runs, add-jurisdictional-value, synonyms. Skills deleted: 6 (and 5 `.claude/skills` links).

Defects: none gating. Wasted edits (ordering): edits to `scripts/validate_axes.py` (-21), `scripts/audit/population_integrity_audit.py` (-6), `schemas/population_links.py` (-9, `ProbePopulationLink`) were deleted outright by 1.4 and 1.3. The `pipeline_contract_audit.py` fixtures were derived from the live registry with `next(...)`; that raises `StopIteration` when the quarantine holds no existing path (reproduced by simulation); fixed in `323a746`.

Residual risk: `scripts/validate_schema.py:33` comment says `schemas/jurisdictional_value.py` still exists; 23 attestations (see 1.7) cite `audit-consolidator`; `skills/gap-driven-mining_SKILL.md:167` ("No PMP required") and `scripts/audit/adherence_log_audit.py:94,108` keep PMP rule ids; the retirement of `pmp-strict-termination` plus the removal of the PMP clauses in `gap-driven-mining` and `gap_mining_audit` CHECK 3 retires the PI rule #8 interlock in effect (the plan lists the criterion; it does not say the skill and audit clauses go with it).

v4 text, same-PR edits for 1.2 (replace the 5a row):
- `test_db_integrity.py`: sub-checks A02, A03, A03b, A03c, A03d, A04 (spec_value_probes), A08 (item_population_elaborations), and the `spec_value_probes` term in the `CAPTURED` predicate. Locate by name.
- `governance/stage-map.yaml`: entries for all 12 tables (and `conflicts` stays).
- Registry: `pmp_audit` entry. Contract (owner merge): `pmp-strict-termination` criterion; `research.anchor` text "rule #8 (PMP)" (cosmetic).
- `schemas/item.py` (81 lines; the plan names only `jurisdictional_value.py` and `population_links.py`), `schemas/jurisdictional_value.py`, and the `item.Item` and `jurisdictional_value.JurisdictionalValueRecord` entries of `validate_pydantic_schemas.MODEL_TABLE_MAP`.
- `scripts/audit/migration_reproducibility.py`: the sentinel table name `items` to `slugs` in `_usable_cache` and in six selftest fixtures (reverting breaks that script's `--selftest` and gives `schema_reference_audit` two MISSING refs: tested).
- `scripts/audit/graph_audit.py` (selftest fixtures and docstring), `audit/graph/extract_db.py`, `audit/graph/topology.py` (`STATE_DIST["items"]`), `audit/adherence_log_audit.py` (check 5), `audit/gap_mining_audit.py` (CHECK 3), `scripts/bootstrap.sh` (PMP backlog query on `items`), `db.py` (verbs, docstring), `test_db_amend_writers.py` J10, `pipeline_contract_audit.py` fixtures (derive from a synthetic registry, not from the live quarantine list).
- `governance/schema-reference-exemptions.yaml`: key `specification`.
- Skills: delete the six; edit `connection-discovery`, `gap-driven-mining`, `evidence-metadata-rehabilitation`, `reasoning-doc-citations`, `workplan-orchestrator` (listed) and `content-gap-analyzer`, `cross-population-conflict-mapper` (unlisted: they name deleted skills).
- `CLAUDE.md` (owner merge): the "`item_taxonomy_links` is unwritable ... D-0184's own object" sentence in section 4; the item-layer bullet in section 7 ("`items` holds 0 rows" to "table is dropped (migration N)"; delete "`db.py add-item` refuses for this reason").
- Do not edit `validate_axes.py` or `population_integrity_audit.py` in this step; delete them in 1.4 and 1.3.
- Instrument: re-anchor 23 atoms (5 citing CLAUDE.md, 18 citing the contract).

### 1.3 Splinter and case-study children (`7faa1b4`, migration 103): EXECUTABLE WITH CHANGES

Done: migration 103 drops `case_study_populations`, `citation_population_links`, `economics_entry_populations`, `extraction_population_links`, `case_study_outcomes`, `case_study_strategies` (0 rows; no inbound FK; no data migration touches them: grep clean). No marker needed. Deleted `schemas/population_links.py`, `population_integrity_audit.py` and its registry entry. 9 files (+ DB).

Deviation: `population_integrity_audit` is deleted here (moved forward from 1.6(a)) because its only subjects are the dropped junctions; a deleted-table audit that stays returns "Junction tables missing" and exit 1.

Residual: `build_graph.py` probe P-A (the five splinter tables are gone) now PASSes; its self-test fixture used it as the FAIL case (fixed `b8ca6b8`).

v4 text, same-PR edits for 1.3: stage-map entries (6); `known_debt.yaml` entry `extraction-population-links-empty` and `topology.MISSION_CRITICAL["extraction_population_links"]` (graph_audit stays PASS with one WARN if left: tested; edit for tidiness only); `schemas/population_links.py` delete, with its `MODEL_TABLE_MAP` entries (2); delete `population_integrity_audit.py` and its registry entry; `scripts/assess/assess_cell.py` docstring (names `schemas.population_links`).

### 1.4 Axes retired as one act (`ecc8fd3`, migration 104): EXECUTABLE AS WRITTEN

Done: migration 104 drops `population_axis_map`, `access_need_axis_map`, `axes`, `situations` and `ALTER TABLE slugs DROP COLUMN serves_axes`. Rows destroyed: axes 17, access_need_axis_map 21, population_axis_map 53, situations 0, and the one stored value `["AX-BAL"]` on `vestibular-balance-built-environment` (SQLite 3.45.1 here; replay verified). The `-- AFTER_DATA: 20260920060857` marker is redundant for the build (095's marker already opens that segment; no data migration writes these) but RULINGS R3 requires a marker later than `data_20260902220357`; keep it. `validate_axes.py` and its registry entry deleted; criterion `base-demand-vocabulary` removed (its check read `axes`, not `base_icf`; ICF codes downstream are held by foreign keys to `base_icf`: not re-derived by A2b). 8 files (+ DB).

Residual: `db.py` help text for `add-medical --icf` was `axes.axis_code` (now `base_icf.icf_code`); `build_graph.py` probe P-AXIS now PASSes.

v4 text, same-PR edits for 1.4: registry entry `validate_axes`; contract (owner merge) `base-demand-vocabulary`; stage-map (4 entries); `schemas/slug.py` `serves_axes`; `db.py` help text; migration header must state the R3 marker.

### 1.5 Scheduled DB-writing workflows (`bd26594`, migration 105): EXECUTABLE AS WRITTEN

Done: deleted `resolve-dois.yml`, `verify-urls.yml`, `resolve_dois.py`, `verify_urls.py`, `test_url_verifier.py`, `test_verification_pipeline.py` and their two registry entries; migration 105 drops `pipeline_runs` (6 rows, quoted in the commit message with dates) and `url_verification_runs` (0). `EXEMPT_TABLES` shrinks to `evidence_source_authors`; `reproducibility-invariant` criterion text and the CLAUDE.md rule-3 "breaks this rule on a timer" paragraph edited; `test_db_integrity` E02, E03, F01 to F04 removed; `machines.yaml` M02.t2 and conflict C-029 edited and removed. 19 files (+ DB).

Note for ordering: the next scheduled fires are Monday 06:00 UTC (`resolve-dois`) and the 1st and 15th at 06:00 UTC (`verify-urls`); any bot commit before merge produces a binary DB conflict (rule 3). Merge this step early.

Unnecessary for green (tested): the `EXEMPT_TABLES` shrink (check PASSes either way) and `dbcore.NOT_CAPTURED["pipeline_runs"]` (tests and schema batteries stay green with the stale key); both are still right to make. R10b in `research_batch_dod.py` still fires but its stated reason (the cron) is gone; it is a rule without a rationale and a candidate for deletion.

v4 text, same-PR edits for 1.5: registry entries (2); `test_db_integrity` E02, E03 and the F-group; stage-map (2); `machines.yaml` M02.t2 (`via` and two evidence needles); `migration_reproducibility.py` exempt tuple and docstring; contract `reproducibility-invariant` text (owner merge); `dbcore.NOT_CAPTURED["pipeline_runs"]`; `research_batch_dod.py` docstring, three comments and the R10b message; `run_checks.py` comment; delete conflict C-029 (R9); `CLAUDE.md` rule 3 paragraph (owner merge); re-anchor 38 atoms (all citing CLAUDE.md, moved by the rule-3 paragraph deletion).

### 1.6 Checks diet (`ef2a655`): EXECUTABLE WITH CHANGES

Done: deleted `code_currency_audit`, `pre_rehab_banner_audit`, `register_integrity_check`, `reasoning_doc_citations_audit` (with registry entries); per R21 and R22 `source_locators_integrity`, `validate_reasoning`, `validate_bpc`; `validate_population`. Promoted `adjudication_integrity` from quarantine to blocking (registry entry; script prints `EXAMINED:` and fails on a NULL tier; its selftest updated). Contract criteria removed: `base-population-vocabulary`, `locator-title-matches-identifier`, `nine-step-synthesis`; `register-invariants` prose edited. 19 files (8 D, 11 M).

Defects:
1. `validate_population`'s check P1 (`schemas/enums.py` `PopulationCode` agrees with the `populations` table in both directions) is held by no other gate. The plan said delete only if the identity-lens table's own CHECK and FKs already enforce it, "confirm first"; A2-phase1's own message says P2 to P5 are, P1 is not. The enum and the table agree today (23 and 23, no difference, checked by A2b), and `PopulationCode` still has readers (`schemas/population.py`, `schemas/failure_demand_recovery.py` validate against it), so drift between enum and table can now arise unseen. The v4 plan has to say either "keep a ten-line enum-versus-table check (for example inside `validate_pydantic_schemas`)" or "retire the enum and read the table". Owner decision (population taxonomy is doctrine).
2. Owner-gated documents edited without a plan line: `governance/tier-system.md` (the code-currency enforcement paragraph, including its 7-year and 5-year thresholds, replaced by one sentence; RULINGS R4 names the sentence, plan 5a does not), `governance/evidence-architecture.md` (two sentences), `governance/retired-vocabulary.yaml` (one sentence).
3. Eight instrument atoms had to be deleted because their quotes left the documents (EVI-040, 041, 042, 043, 234, 252, PIP-15, PIP-21) and 52 re-anchored (33 citing `tier-system.md`, 19 citing the contract); conflict C-018 loses PIP-15.
4. R4's text says delete the retired `validate_db` quarantine entry too; it was kept (one-line reason; its longer reason also held the "31 connections with zero targets" finding, which survives in `DR-2026-08-14-tier-1-retirement-batch.md` and `data/decisions/decision_register.yaml:5285`). R22's other clauses are not executed anywhere: `references/bpc-reasoning/` to `_archived/`, shrinking CLAUDE.md rule 2's path list, NULL-forwarding `promoted_to_rdc_id`.
5. The step's "(a) 1,174" figure is spread over 1.3 and 1.6, and the (b) and (c) triage deletes a further 1,014 script lines.

v4 text, same-PR edits for 1.6: registry entries (`validate_bpc`, `validate_population`, `validate_reasoning`, `reasoning_doc_citations_audit`, `source_locators_integrity`; quarantine entries `register_integrity_check`, `code_currency_audit`, `pre_rehab_banner_audit`; move `adjudication_integrity` to `checks:`); contract (owner merge) `base-population-vocabulary`, `locator-title-matches-identifier`, `nine-step-synthesis`, `register-invariants` prose and references; `tier-system.md` and `evidence-architecture.md` sentences (owner merge); `retired-vocabulary.yaml` deferred-entry sentence; `assess_cell.py` comment; `adjudication_integrity.py` (EXAMINED, NULL tier, selftest); `skills/reasoning-doc-citations_SKILL.md` (frontmatter `enforcement:` and the "Audit query" section); instrument: delete the eight atoms above, re-anchor 52, edit C-018.

### 1.7 Skills diet (`c9f9c2b`): EXECUTABLE WITH CHANGES

Done: the 15 skills the section 9 command printed after 1.2 and 1.5 (1,834 lines), `skills/deprecated/` (12 files, 1,156 lines) and the 15 `.claude/skills` links deleted; the `references/skill-registry.md` "All active skills" block regenerated from `skills/` (26 names; the six skills deleted in 1.2 were still listed until here) and the "Deprecated skills" section removed. `claude_skills_loadable` PASS; no dangling links. 43 files.

Defect (latent, no gate): `scripts/audit/adherence_log_audit.py` `_load_skill_ids()` takes the valid rule identifiers from that same registry block. 151 attestations are committed; 8 already cited unknown ids at base, 31 do at HEAD, so **23 attestations newly fail CHECK 3 the next time any PR puts them in its changeset**: `structure-auditor` (21 files), `guidebook-auditor` (13), `audit-consolidator` (12), `connection-auditor` (1), `relational-integrity-checker` (1). Derive with the script in `A2b_work` (or: ids in `rules_in_scope`, `per_rule_status` keys and `deviations[].rule` that are not in the registry block). The plan's "1.7, 1.8: nothing broke" is false for the PR after this one.

v4 text, same-PR edits for 1.7: `references/skill-registry.md` block and "Deprecated skills" section as done; and a stated choice for the 23 attestations: keep the five retired names where `_load_skill_ids()` still reads them (for example a second block headed "Retired rule identifiers"), or accept an id edit whenever those attestations are re-touched.

### 1.8 Registry prose (`0b1d88c`): EXECUTABLE AS WRITTEN

Done: text-level deletion of 54 scalars over 300 characters (`note` 42, `floor_basis` 11, `reason` 1), 837 lines, one line added (the `validate_db` one-line reason). Verified by A2b: loading the registry before and after gives identical `checks` and `quarantine` apart from the deleted keys; the 11 remaining over-300 strings are all `no_floor` (C8/C9 need them); the file ends with a newline. `--all` and `--selftest` unchanged. Rule 7a note: the plan's "72 fields / 1,044" is true of the base tree; after 1.1 to 1.7 it is 54 / 837.

### 1.9 Empty orphan tables (`9cef95e`, migration 106): EXECUTABLE WITH CHANGES

Done: migration 106 drops `reference_stubs`, `search_coverage`, `search_languages`, `bpc_metadata` (0 rows; no view, trigger or FK reaches them). Data migrations 20260823223839 (531 inserts into `reference_stubs`) and 20260823225142 (delete) predate 095's marker, so `--rebuild` replays and then drops them: verified. `external_root_registry` kept. `update-bpc` and `update_bpc_metadata` deleted; `schemas/bpc_metadata.py` deleted (it did not even import: a Pydantic decorator error, so `validate_pydantic_schemas` loses an import error); `test_db_integrity` A06 and D03; `research_protocol_audit` CHECK 9; `legacy_grid` in `get_coverage_completeness`. 11 files (+ DB).

Defects:
1. First run of the gates at this step had `build_graph --check` red (ENT-044 quotes `governance/conceptual-model.md:215`, "Citation records now live in the `reference_stubs` table (531 rows, migration 061)"). A2-phase1 left that sentence alone and edited only line 107, so a stale statement about a dropped table survives at `conceptual-model.md:215`; fixing it means deleting or re-quoting atom ENT-044.
2. Two live skills call the deleted verb or table: `skills/citation-miner_SKILL.md` (`update-bpc` step) and `skills/research-log-manager_SKILL.md` (a `bpc_metadata` query). Not in the plan; edited here.
3. `db.py` still carries the frozen coverage machinery that names the dropped grids: `_COVERAGE_COLS` and `_LANGUAGE_COLS` (lines 88 to 91), `class FrozenGridError` (536 to 549), the `LEGACY COVERAGE GRIDS ARE FROZEN` comment and `_FROZEN_MSG` (550 to 612), `upsert_search_coverage` and `upsert_search_language` (615 to 625, no caller), the `upsert-coverage` and `upsert-language` parsers (2088 to 2105) and branch (2556 to 2562). A comment says the verbs were kept deliberately so old callers get a redirect, so this is a judgment, not a defect; the plan's "`search_coverage` in `db.py`" is not finished by the commit. About 110 lines.

v4 text, same-PR edits for 1.9: `db.py` (`update-bpc`, `update_bpc_metadata`, `_BPC_META_COLS`, docstring line, `legacy_grid` reads; decide the frozen verbs above); `schemas/bpc_metadata.py` with its `MODEL_TABLE_MAP` entry; `test_db_integrity` A06 and D03; `research_protocol_audit` CHECK 9, the `search_languages` row count in `EXAMINED`, and the docstring list; stage-map (4); `governance/conceptual-model.md:107` (and :215 with atom ENT-044); `scripts/assess/assess_cell.py` docstring; `skills/citation-miner_SKILL.md`, `skills/research-log-manager_SKILL.md`.

---

## 5. Owner-merge edits (listed separately; these edit ratified or owner-gated text)

Pipeline contract (`governance/pipeline-contract.yaml`; note its header says `status: PROPOSED`, `ratified: false`, and RULINGS R21 says the contract is not ratified, so the plan's "owner merge" label for it is a conservative choice, not a fact; v4 should say which):
- criteria removed (6): `render-freshness` (1.1), `pmp-strict-termination` (1.2), `base-demand-vocabulary` (1.4), `base-population-vocabulary`, `locator-title-matches-identifier`, `nine-step-synthesis` (1.6);
- text edited (3): `research.anchor` (1.2, cosmetic), `reproducibility-invariant` criterion (1.5), `register-invariants` criterion and references (1.6).

`CLAUDE.md`:
- 1.1: section 3 `render` row; "Don't hand-edit generated output" bullet; the `tools/*.html` bullet.
- 1.2: section 4 sentence on `item_taxonomy_links` and D-0184; section 7 item-layer bullet (two edits).
- 1.5: rule 3 "breaks this rule on a timer" paragraph (deleted, 8 lines).
- Not done and named by the rulings: R22's shrink of rule 2's path list.

Other owner-gated or doctrine text: `governance/tier-system.md` (code-currency enforcement paragraph), `governance/evidence-architecture.md` (two sentences), `governance/retired-vocabulary.yaml` (13 exempt_path lines across 8 RV entries in 1.1; one deferred-entry sentence in 1.6), `governance/conceptual-model.md:107` (1.9), `references/skill-registry.md` (1.7), `.ignore` (1.1), `.claude/agents/repo-sweep.md` and `.claude/commands/orient.md` (A2b fix).

Rows destroyed from the blob (LED-169 action 4, owner entry assumed in the commits): `axes` 17, `access_need_axis_map` 21, `population_axis_map` 53, `pipeline_runs` 6 (reconstructible from the migration chain except `pipeline_runs`, which no migration ever wrote), and the `["AX-BAL"]` value. Rulings cited in migrations and commits as R2, R3, R4, R21, R22 are PROPOSED rulings in `RULINGS.md`, not ledger entries; each cite needs the owner's ledger id before merge.

---

## 6. Edits against the plan's lists

### 6a. Made by the commits and not named in 5a or the step text (exact file and what)

1.1: `check-registry.yaml` `context_map_fresh` basis; `retired-vocabulary.yaml` exempt_paths; `atoms-claude.jsonl` (CLM-050), `atoms-contracts.jsonl` (PIP-07) and line re-anchors; `build_graph.py` (P-I); `capabilities.yaml` (C4.7); `conflicts.yaml` (C-027, PIP-07 reference); `CLAUDE.md` section 3 `render` row; `scripts/run_checks.py` (selftest C5 assertion); `stage-map.yaml` header; `audit_evidence_metadata.py` comment; deleted `tools/README.md` and `audits/evidentiary-base-audit{,-items}.csv|json|md`.
1.2: `schemas/item.py`; `scripts/audit/migration_reproducibility.py` (`items` to `slugs`, 7 places); `scripts/bootstrap.sh`; `scripts/validate_axes.py`, `scripts/audit/population_integrity_audit.py`, `schemas/population_links.py` (wasted); `skills/content-gap-analyzer_SKILL.md`; `skills/cross-population-conflict-mapper_SKILL.md`; `pipeline-contract.yaml` `research.anchor`; `CLAUDE.md` two passages; `scripts/db.py` docstring; atoms re-anchors.
1.3: deletion of `population_integrity_audit.py` and registry entry (moved from 1.6(a)); `scripts/assess/assess_cell.py` docstring.
1.4: `scripts/db.py:1789` help text; atoms re-anchors (40 lines).
1.5: `scripts/run_checks.py:295` comment; `research_batch_dod.py` docstring and three comment blocks; `migration_reproducibility.py` docstring; conflict C-029 deleted; atoms-claude re-anchors (76 lines).
1.6: `tier-system.md`, `evidence-architecture.md`, `retired-vocabulary.yaml`, `assess_cell.py` comment, `skills/reasoning-doc-citations_SKILL.md`; atoms-evi (6 deleted, 33 re-anchored), atoms-contracts (PIP-15, PIP-21 deleted, 19 re-anchored; 52 re-anchored in all), `conflicts.yaml` C-018; four further scripts deleted (1,014 lines).
1.7: six 1.2-era entries and the "Deprecated skills" section in `skill-registry.md`; PI-placeholder line.
1.9: `skills/citation-miner_SKILL.md`, `skills/research-log-manager_SKILL.md`, `assess_cell.py` docstring, `db.py` docstring and `_BPC_META_COLS`.

### 6b. Named by the plan and unnecessary for a green gate (tested by temporary revert unless marked)

- `known_debt.yaml` `extraction-population-links-empty` and `MISSION_CRITICAL["extraction_population_links"]` (1.3): `graph_audit` still PASS, one extra WARN.
- `migration_reproducibility.EXEMPT_TABLES` shrink (1.5): PASS either way.
- `dbcore.NOT_CAPTURED["pipeline_runs"]` (1.5): tests and schema batteries stay green with it present.
- `retired-vocabulary` exempt_path removals (1.1): advisory only (3 dead exemptions reported if restored).
- 1.1's text-only items (`preflight.sh`, `.ignore`, comments) and the R10b message (1.5): no gate reads them [not individually reverted].
- Necessary, for the record (reverting fails a gate): stale `room*` and `specification` exemption keys (blocking `schema_reference_audit`), `context_map_fresh` basis (selftest C7), `migration_reproducibility.py` `items` references.

### 6c. Named by the plan or rulings and not done

Frozen coverage verbs in `db.py` (1.9); `conceptual-model.md:215` (1.9); `validate_db` quarantine entry (R4); R22's `references/bpc-reasoning/` move, rule 2 path list and `promoted_to_rdc_id`; regenerating `governance/context-map.yaml` (0.6; A2b ran the generator: it works after Phase 1 and shrinks the file from 1,938 to 1,566 lines, 12 added and 384 removed; not committed; `context_map_fresh` is red at baseline and stays red); the instrument's generated outputs (`STATE-GRAPH.md`, `CAPABILITIES.md`, `graph.json`, `ATOMS.tsv`) still describe the deleted scripts [UNVERIFIED whether the plan expects them regenerated per step].

---

## 7. Defects found in the commits, and what A2b did

Fixed by A2b (each a small additional commit, say so in any hand-off):
1. `b8ca6b8` `build_graph.py --selftest`: two of 15 mutation tests failed after Phase 1 and no gate runs them (`build_graph.py` is not in the registry; R4 names only `--check`). "The `writable` predicate can say PASS and can say FAIL" named `item_taxonomy_links` (dropped in 1.2; first red at `dde0ff4`); "a capability can come out CAN and can come out BLOCKED" used probe P-A, which passes once 1.3 drops the splinter tables (first red at `7faa1b4`). After 1.2 the live `unwritable_set()` holds three entries, all same-verb pairs, so no live table can demonstrate FAIL; the fixtures are now synthetic stubs. 15/15 at HEAD; `--check` unchanged. Verified red at the two named commits in throwaway worktrees (removed).
2. `323a746` `pipeline_contract_audit.py --selftest`: the "quarantined check" fixture used `next(...)` over the live quarantine and would raise `StopIteration` once R4's literal "delete `validate_db`" is applied (reproduced by simulation). Now synthetic; 8/8 as before.
3. `87185b1` two `.claude` files still said `.ignore` hides `tools/*.html`.

Not fixed (decisions or out of scope): the five items under "Defects" in 1.6, 1.7, 1.9 (P1 enum drift check; 23 attestations; frozen verbs; `conceptual-model.md:215`; R22 and R4 leftovers). R10b's missing rationale (1.5). `scripts/validate_schema.py:33` stale comment.

---

## 8. Defects in the plan and the rulings (what the v4 text must contain)

1. **R4 needs a clause about the instrument's own checks.** `build_graph.py --check` verifies every atom quote verbatim and within three lines of its cited line (`verify_atoms`). Any step that edits `CLAUDE.md`, `pipeline-contract.yaml`, `tier-system.md` or `conceptual-model.md` shifts lines or removes quotes. Over Phase 1: 10 atoms deleted (CLM-050, PIP-07, PIP-15, PIP-21, EVI-040/041/042/043/234/252), 143 `source` anchor edits on 90 distinct atoms (38 citing CLAUDE.md, 33 tier-system.md, 19 pipeline-contract.yaml), 1 probe, 1 predicate and 2 conflicts deleted. 5a says `--check` fails after 1.1 to 1.5 "on stage-map entries and machines.yaml M02.t2"; that is incomplete. Proposed wording: "After editing any file an atom cites, run `build_graph.py --check`; delete atoms whose quote left the document (and everything that cites them), and re-anchor the rest."
2. **`build_graph.py --selftest` is outside every gate**; add it to R4's list ("`build_graph.py --check` and `--selftest`") or register it.
3. **Section 4 / 5a counts that are stale**: `pipeline_runs` 6 rows, not 5; registry prose after 1.1 to 1.7 is 54 fields / 837 lines; the 5a note "1.7, 1.8: nothing" is wrong (23 attestations).
4. **Step 1.6 (b)**: "delete `validate_population` only if the identity-lens table's own CHECK and FKs already enforce it" is not satisfied (P1). Say what happens to `PopulationCode`.
5. **Step order**: do 1.3's `population_integrity_audit` deletion and 1.4's `validate_axes` deletion before or with 1.2 (or say "do not edit, delete") to avoid editing files that the next two steps delete; or accept the wasted edits.
6. **The contract's own header says PROPOSED / unratified** (R21 says so), while 1.x commits label criterion edits "owner merge". Pick one.
7. **R22 is larger than 1.6 and 1.9**: it also moves `references/bpc-reasoning/` to `_archived/` (two attestations name those paths), shrinks rule 2's path list and NULL-forwards `promoted_to_rdc_id`; assign those to a step.
8. **Migration numbers**: the five migrations here are 102 to 106; T1 (step 0.2) brings 102 to 105, so these renumber to 106 to 110 at stack time. Prose that names the numbers: `CLAUDE.md:429`, `governance/conceptual-model.md:107`, `scripts/db.py:975`, and the headers of the five new migration files (file names, first comment line, one cross-reference in 103).
9. **Ruling ids in migrations and commits** (R2, R3, R4, R21, R22) are proposals until the owner enters them in the ledger (step 2.1); the migrations are append-only, so the comment text must be right the first time.
10. **Bot timing**: `resolve-dois` fires Mondays 06:00 UTC and `verify-urls` on the 1st and 15th; each fire commits the blob and conflicts with any open DB PR. Stack 1.5 first among the schema steps.

---

## 9. What A2b did not verify

- Intermediate-step gate tables (after 1.1 to 1.8) are A2-phase1's logs, not re-run; HEAD and the committed blob (equal to base plus migrations 102 to 106) were re-verified.
- Necessity of the prose-only edits (comments, docstrings, skill text, `.ignore`, `preflight.sh`) was not individually reverted. Reverted and tested: `migration_reproducibility.py` items references, `context_map_fresh` basis, the `room*` and `specification` exemption keys, `EXEMPT_TABLES`, `NOT_CAPTURED["pipeline_runs"]`, `known_debt` plus `MISSION_CRITICAL`, `retired-vocabulary` exempt_paths.
- `scripts/preflight.sh` and GitHub CI were not run; `.github/workflows/ci.yml` is unchanged and references no deleted path.
- Stacking on T1 (renumbering to 106 to 110, the binary DB merge) was not rehearsed.
- No antagonist pass (R7) was run on the diff.
- Whether `ICF codes resolve in base_icf` (the intent of the deleted `base-demand-vocabulary` criterion) is fully held by foreign keys was not re-derived.
- Prose callers of deleted names in `architecture/`, `references/`, `governance/*.md` and frozen `workplan/` records were located (examples above) but not edited or counted exhaustively.
