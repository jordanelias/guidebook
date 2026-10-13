# The stack: every rehearsed slice applied in the plan's order

**Date:** 2026-10-13. **Base:** `31142552` (`origin/main` `f54d09fd` plus this branch's workplan files). **Method:** a fresh clone, `refs/remotes/origin/main` pointed at the base (the changeset-scoped checks otherwise read other people's data migrations as the stack's own), the slices applied as commits in the order below, each conflict resolved by hand, each schema migration renumbered to the next free number, the database blob always taken from the previous layer and migrated by `scripts/migrate_db.py` (never merged), derived outputs regenerated last. Gates were run on a snapshot clone of the layer (`run_checks.py --all`, `--selftest`, `schema_reference_audit.py`, `build_graph.py --check`, `migrate_db.py --rebuild` compared table by table and row by row). The stack clone lives in the session scratchpad and is not kept; this file is the record. Migration numbers are the stack's own and renumber at merge (plan R6).

## Order and what each layer cost

| layer | source slice | conflicts met | resolution |
|---|---|---|---|
| 1 | `D-t1-landing-r25-r24` (T1, R25, R24; migrations 102–106) | none against main (the slice patch was made against it) | regenerate the derived files (html, context map, instrument) after migrating |
| 2 | Phase 1 (`A-phase1-deletions`: 1.1 to 1.9 and A2's three fixes; migrations 107–111) | five html files modify/delete; `stage-map.yaml` header comment; `atoms-contracts.jsonl` (T1 re-cited RES-16–18, Phase 1 re-cited PIP atoms); `validate_pydantic_schemas.py` (T1's two map entries beside the `bpc_metadata` entry 1.9 removes); `check-registry.yaml` for 1.8 | `git rm` the html; keep both stage-map comments; a three-way merge by atom id (`merge_jsonl.py`) then re-anchor line cites; keep T1's map entries; **re-run the prose-deletion tool on the stacked registry instead of merging its 837-line diff** (58 fields, 882 lines on this stack) |
| 3 | R5 (`F-r5-r22-r30`) | seven: `CLAUDE.md` (generated-output bullet reworded by 1.1), `check-registry.yaml`, three modify/delete (`base_parameter.py`, `slug.py` edited by T1/1.4; `validate_pydantic_schemas.py` edited by 1.9), `assess_cell.py` docstring, `atoms-claude.jsonl` (CLM-033, CLM-051 edited by both) | delete the files; keep the 1.1 wording and drop the drift bullet; remove the registry entry as text; apply F's CLM-033 re-quote and strike CLM-051 over the re-cited versions |
| 4 | R22 | 21 paths (most are files that 1.1, 1.6 or 1.9 had already deleted and F edited) | every modify/delete resolved by deletion; `bpc_metadata` migration **dropped** (1.9 has dropped the table); **the slice shrinks from 38 files, +140/−1,313 to 17 files, +61/−65** |
| 5 | R30 | registry entry `decision_capture`; one deleted `tools/pipeline_completeness.py` | delete the entry as text; `git rm` |
| 6 | R29 data migration (`E-r29-divergence`) | the database blob | take the layer's blob, apply the migration with its session; the deep check passes |
| 7 | R29 tooling | `CLAUDE.md` (paragraph already deleted by 1.5), registry, contract criterion, `migration_reproducibility.py` | take the 1.5 versions, then **empty `EXEMPT_TABLES`** and guard the print of the exempt list; both reproducibility checks pass |
| 8 | R18 (`G-r18-lens`; migration 112) | none (`git apply --3way`, excluding generated files and the mirror R5 deleted) | renumber; the migration's own header said "pre-102": reword |
| 9 | band and marker (`C-r7-tier-marker`; migration 113) | the database blob; `adjudication_integrity.py` (1.6 had already added `EXAMINED` and the NULL-tier test) | `-- AFTER_DATA` **re-derived** (`20261013212204`, the R29 migration); take C's version of `adjudication_integrity.py` and delete the leftover `skipped` lines 1.6 had written, **which raise `NameError` and which only running the script showed** |
| 10 | R14 narrowed (M4; migration 114) | the slice's patch was made against a stand-in; seven rejects | applied by hand to the stack; regenerate `.claude/settings.json` with `research_contract_hook.py --write`; **T1's `test_scan_contract.py` read `populations`: `schema_reference_audit` (blocking) failed until it was edited** — the sweep must run after T1 lands |
| 11 | R32 (stage-map; not a rehearsed slice) | none | move `source_value_extractions` and `extraction_relations` to judgment, delete the three `disputed:` entries (R32, R42), correct CLAUDE.md §3's two rows; `P-STAGE-SVE` turns PASS |
| — | regenerate | | `context_map.py`, `build_graph.py` last (`context_map_fresh` PASS) |

**Not in the stack:** R37 (the writer guard and the `slug` NULL-forward rebuild; `P-V2` still FAIL), 3.R, Phase 2, steps 0.3 to 0.6, Phase 4, Phase 5; R25's owner accept-or-strike; the R24 registry writer (a GAP). The stack is 29 commits on the base, of which layers 2 to 11 are 28; the five migrations of Phase 1 became 107–111 and R18, the marker and M4 became 112–114.

## Gates

| | base (`31142552`) | after T1 + Phase 1 | final |
|---|---|---|---|
| `run_checks.py --all` | 85 registered; 63 green / 11 nothing in scope / 11 advisory red | 74 registered; 58 / 8 / 8 | 72 registered; **57 / 8 / 7**; `RESULT: PASS` |
| advisory red | `migration_reproducibility_deep`, `validate_schema_cross_check`, `validate_pydantic_schemas`, `retired_vocabulary`, `research_protocol_audit`, `metadata_integrity_audit`, `validate_reasoning`, `schema_walkability_fresh`, `context_map_fresh`, `site_pages_fresh`, `source_locators_integrity` | the first six, `scan_debt`, `context_map_fresh` | `scan_debt` (T1's 468 pairs), `validate_schema_cross_check`, `retired_vocabulary`, `research_tooling_separation` (the combined changeset holds tooling and the R29 data migration; they ship as separate PRs), `research_protocol_audit`, `metadata_integrity_audit`, `context_map_fresh` (PASS after the last regeneration) |
| `--selftest` | PASS | PASS | PASS |
| `schema_reference_audit` | PASS | PASS | PASS (after the `test_scan_contract` edit) |
| `build_graph.py --check` / `--selftest` | 0 failures / 15 | 0 / 15 | 0 / 15 |
| `migrate_db.py --rebuild` | identical but `pipeline_runs` (6 vs 0) | identical (56 tables, 21 views) | identical, `user_version 114`, 56 tables, 22 views, every row count and all DDL |
| `migration_reproducibility_deep` | FAIL | FAIL | **PASS, with no exempt table** |

No blocking check is worse than baseline at any layer. `scan_debt` and `research_tooling_separation` are the only reds the stack introduces.

## Measures (the plan's own commands, run on the base and on the stack)

| area | base | stack | change |
|---|---:|---:|---:|
| `scripts/` (py + sh) | 46,510 | 41,017 | −5,493 |
| of which `scripts/audit/` | 12,575 | 11,078 | −1,497 |
| of which `db.py` + `dbcore.py` | 10,618 | 11,478 | +860 (T1) |
| of which `scripts/tests/` | 6,398 | 6,351 | −47 |
| of which `scripts/generate/` | 2,438 (with `generate_parts.py`) | 553 | −1,885 |
| `tools/*.py` | 5,053 | 0 | −5,053 |
| `schemas/*.py` | 5,698 | 2,799 | −2,899 |
| `governance/check-registry.yaml` | 2,525 | 1,264 | −1,261 |
| active skills | 9,871 | 6,393 | −3,478 |
| `.github/workflows/` | 714 | 275 | −439 |
| migrations | 184 files, 20,061 lines | 198 files, 21,187 lines | +14 files, +1,126 lines (T1's four migrations +364, R24's, eight more schema migrations, one data migration) |
| budget metric (scripts + tools + schemas + workflows + skills) | 67,846 | 50,484 | **−17,362 (−25.6%)**, T1's +3,517 included |
| `git diff --shortstat` excluding the database | | 256 files | +6,235 / −37,676 |
| tables / views / foreign keys | 82 / 21 / 115 | 56 / 22 / 78 | |
| registered checks | 85 | 72 | |
| `IDEAL-GRAPH.md` §6 script: tables failing | 21 of 82 | 15 of 56 | |

## Defects the stack found that no slice found alone

1. R22 and Phase 1 overlap: 1.6 deletes the BPC validators and 1.9 drops `bpc_metadata`, so R22 is a 17-file residue and its migration is redundant. The plan's R22 step is rewritten as the residue.
2. Both 1.6 and the band slice edit `adjudication_integrity.py`; a hand merge left a reference to a variable (`skipped`) that no longer existed, so the script raised `NameError` on every run. Run each script you merged by hand before committing.
3. Atom line cites move with every layer that edits `CLAUDE.md`, the contract or `tier-system.md`: 31, 37 and 11 anchors were re-cited at three layers. Re-anchor after every layer.
4. Phase 1 wrote a migration number into `CLAUDE.md` ("migration 102"), which goes stale on renumbering; the stack names it by slug.
5. T1's tests are callers of the tables R14 renames; the order T1 → R14 is forced, and the sweep must be re-run after T1 lands.
6. `EXEMPT_TABLES` goes through three states (`pipeline_runs` and the authors table; the authors table; none) across 1.5 and R29.
