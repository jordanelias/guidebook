# Workplan v2.2 against the ideal state graph: comparison and adjudications

**Status:** PROPOSED · **Date:** 2026-10-12 · **Compares:** `workplan/2026-10-12-simplification-workplan.md` (v2.2) and `workplan/pipeline-state-graph/IDEAL-GRAPH.md` (the Opus design, after a fourth antagonist pass). **Adjudications** are made on the owner's instruction of 2026-10-12 ("wherever there is a conflict, adjudicate to ensure 100% accuracy, code compliance and logic for ensuring walkability in pipeline as well as dynamic information collection") and are open to the owner's override. Doctrine text (mission, tier definitions) stays an owner merge. Facts marked *(checked)* I re-ran; facts marked *(pass)* come from the antagonist's report and I did not re-run them. Every figure has its command in the plan's §9, the ideal's §9, or the line beside it.

## 1. Verdict

Neither document is adopted as it stands. **The ideal is the better shape and an unreachable destination as written:** the antagonist built its DDL against the live data and found 28 of 53 admitted sources, 30 of 88 observations and 25 to 101 of 101 extractions would not load *(pass)*; its derivations of admissions, slug links and the follow-up tag are false on live rows *(P3, P13 below)*; it drops a live guard (identifier reissue) without replacing it. **The plan is reachable and deletes first, but it leaves the owner's walkability requirement unmet:** after its Phase 1, 21 of the remaining 58 tables still fail the ideal's walkability check, and no step makes the judgment-to-synthesis or the bytes handshake exist. The adjudicated course below keeps v2.2's order, rehearsal evidence and ruling discipline, and adds only those elements of the ideal that (a) load the live rows without stranding any, (b) replace more than they add, and (c) cite a failing handshake.

## 2. Measures

| measure | live | after v2.2 Phase 1 | ideal |
|---|---|---|---|
| tables | 82 | 58 (53 with step 1.9) | 33 |
| views | 21 | 20 | 5 |
| `db.py` verbs | 72 | at least 65 (1.2 removes 7) | 28 |
| registered checks | 85 | at least 69 (1.1 to 1.6 remove 16) | 12 |
| tables failing the walkability script | 21 of 82 | 21 of 58 (16 of 53 with 1.9) | 7 of 33 (5 are infrastructure, 2 named residuals) |
| lines deleted, gross | — | 17,635 named (plan §5) | about 40,000 *(pass; estimate)* |
| lines added | — | T1 +3,426; a renderer at most 300 (estimate) | 5,000 to 14,000 *(pass; estimate, not sized by the design)* |
| order | — | net negative from the first PR | net positive for several PRs, net negative only after the last deletion *(pass)* |

Commands: tables and views, `python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select type,count(*) from sqlite_master where type in ('table','view') and name not like 'sqlite_%' group by 1\").fetchall())"` (the 58 and 20 are the same query on the rehearsal database at version 105); the walkability script is `IDEAL-GRAPH.md` §6, run on each database *(checked)*; ideal counts, `IDEAL-GRAPH.md` §9. The tables still failing after Phase 1 are `access_duration`, `access_stakes`, `life_stage_modifiers`, `rooms`, `lang_jur_map`, `case_studies`, `external_root_registry`, `bpc_metadata`, `citation_mining`, `reference_stubs`, `research_code_leads`, `search_coverage`, `search_languages`, `source_locators`, `conflicts`, `connections`, `connection_targets`, `source_value_extractions` (`root_id` has no FK) and the infrastructure residuals `data_migrations`, `decisions`, `weighting_profile`. Rows: `rooms` 17, `lang_jur_map` 70, `citation_mining` 33, `research_code_leads` 96, `source_locators` 893, `access_duration` 3, `access_stakes` 3, `life_stage_modifiers` 2; the other nine are empty *(checked)*.

## 3. What each has that the other lacks

| the ideal adds | v2.2 lacks |
|---|---|
| a pointer from every row that depends on bytes to the retrieved file (K16, K17, K37) | any handshake work; the bytes are reachable only by manifest and `file_anchor` (18 of 101 extractions) *(checked)* |
| a judgment-to-synthesis pointer, so a synthesis names what it weighed | the handshake is empty today; no synthesis table names a judgment row *(pass, re-ran its stage-pair script)* |
| one walk over the live foreign keys and one derived check in place of four walkers | the walkers remain; `graph_audit` and its `graph/` modules survive Phase 1 |
| `tier_ladder` as data, ending `TIER_MAP` in code | the hard-coded map |
| a hard-coded inventory (157 import-time path bindings, 69 files reading `GUIDEBOOK_DB_PATH`, 58 `REPO_ROOT` definitions) *(pass)* | no step centralizes them |

| v2.2 has | the ideal lacks |
|---|---|
| an order that deletes first and rehearsed what each step breaks | any account of reaching it from live data; no row-level migration was tried until the antagonist did |
| the same-PR edit lists and the owner-ruling sheet | tests: the 11 `test_*` registry entries and `scripts/tests/` (6,398 lines) go with it, including the engine's tests *(pass)* |
| retire-in-place and rule 3 and 5 discipline | five of the 12 kept gates read objects the ideal deletes, so they are unsized rewrites *(pass)* |

## 4. Where they agree

Delete the render apparatus, the scheduled workflows, the item layer, the splinter tables, the axes; merge the lens-registry naming only on the owner's word; retire stale registry prose; take slugs off extractions (LED-196); build one small renderer over one view; do not rebuild the migrations; prune in place by forward migrations. Plan steps 0.1, 0.4, 1.1, 1.4, 1.5, 1.7, 1.8 and 3.R agree with the ideal and are unchanged.

## 5. Adjudications

Tests: **(a)** accuracy, **(b)** code compliance, **(c)** walkability, **(d)** dynamic collection regardless of slug. Tie-breaks in order: the later live owner statement (rule 0); the specific over the general; the option with less code and one home per fact. ✓ holds, ✗ fails, — not engaged.

| # | point | v2.2 | ideal | what the live data and the rules show | tests | adjudication |
|---|---|---|---|---|---|---|
| P1 | cross-parameter synthesis and the eight synthesis tables | do not build | merge eight tables and `determination_gates` into `syntheses` + `synthesis_inputs` | the handshake is empty today. The merge cannot take the live rows: 110 per-source rows map to 64 key collisions and 46 role refusals; three pending specifications carry 23 extraction links and no synthesis; `GAP-010` is closed with the four closure fields NULL *(pass)*. LED-169 forbids hard-deleting rows | v2.2 ✗c; ideal ✗a | **Add the pointer, defer the merge.** One additive pointer table from the existing convergence table to extractions makes the handshake walkable both ways; no table is dropped or merged until a row-level migration rehearsal for that table passes and, for row-bearing tables, the owner rules case by case. Cross-parameter synthesis stays unbuilt until a second parameter has data; the pointer means nothing blocks it |
| P2 | slug by lens coverage | logged query text; delete `P-M` | four nullable lens FKs on `search_executions`; `v_coverage` | `terms_used` is free text, so `P-M` fails. Four nullable `ALTER TABLE … ADD COLUMN … REFERENCES` statements (to `populations`, `base_icf`, `access_needs`, `base_taxonomy_medical`) apply to a copy of the live database with all 191 rows intact and no foreign-key violation *(checked)*. The ideal's other CHECKs on that table refuse 50 rows, but the lens columns are not among them *(pass)* | v2.2 ✗a; ideal ✓ | **Adopt the four lens FKs under the live registry names, and `v_coverage`; keep `P-M` and predicate C1.8; take none of the ideal's new CHECKs on `search_executions`.** The bucket refusal at `log-search` (A31) waits: `v_coverage` counts searches, and LED-193's exhaustion is SEARCHED, THIN or NO-DATA per slug, which the ideal deletes |
| P3 | T1 follow-up tag | land T1 as built | derive `v_follow_up`; strike T1's `extraction_follow_ups` | the derived view reads `search_candidates.resolved_ref_id` only, empty for 44 of 51 admitted sources, so it tags 46 of 54 preliminary extractions wrongly on day one *(pass; the 54 checked)* | ideal ✗a | **Keep T1's explicit follow-up record.** `term_catalogue_origins` into three `terms` columns is the owner's accept-or-strike (SES-063); folding it is cheaper before T1 lands than after |
| P4 | `conflicts` in step 1.2 | rebuild without the `items` FK | merge into `syntheses` | follows P1: the table is empty and its merge is deferred | — | **v2.2 stands** |
| P5 | `case_studies`, `economics_entries` | keep (R12) | fold into sources plus extractions | RES-12 is ratified ("go to their structured tables"); no later owner statement *(pass)*; the ideal rated it medium confidence | ideal ✗b | **v2.2 stands.** The fold is a doctrine question for the owner |
| P6 | tier storage | derive `--tier` at `add-source`; keep the column | `tier_ladder` + `source_grades`; no stored tier | all 53 live grades resolve through the ladder and the Co-1 CHECK holds *(pass)*. A stored tier is a copy of a derivable fact (rule 5); the column cannot be dropped, 23 data migrations INSERT it *(plan §5)*. `assess_cell.py` reads `e.tier` and `co1_source_type` | ideal ✓; v2.2 keeps a copy | **Adopt the ladder as data and the grade table, staged:** add `tier_ladder`, `source_grades`, `v_source_tier`; writer-retire the stored tier; re-point readers (sweep first); NULL-forward by compensating migration. Phase 3, after Phase 1 has shrunk the surface. Replaces the plan's Phase 3 evidence "derive at add-source" row |
| P7 | `medical_lens_integrity` | keep | a CHECK replaces it | the CHECK covers one of the gate's four subjects *(pass)* | ideal ✗a | **Keep the gate** until a constraint holds all four |
| P8 | gates and tests | keep a check that examined something and guards the book | 12 gates; delete the rest and all tests | the antagonist found at least nine deleted gates whose invariant nothing else holds, including `identifier_floor_audit`, `derived_not_curated_audit`, `adversarial_pass_recorded`, `column_vocabulary_audit`, `author_fidelity`, `alias_provenance_audit` and `extraction_relations_integrity` *(pass)* | ideal ✗a, ✗b | **v2.2's test stands.** A gate is deleted when a CHECK, FK or writer refusal holds the same invariant (named in the commit) or its subject is deleted; a test is deleted with its subject. The 12-gate target is a direction |
| P9 | identifier reissue (PIP-17) | silent | drops `AUTOINCREMENT` on four tables and the floor audit | nine live tables carry `AUTOINCREMENT`, the ideal's DDL none *(checked)* | ideal ✗a, ✗b | **Keep `AUTOINCREMENT` and `identifier_floor_audit`.** Rejected |
| P10 | `extraction_relations` | silent | drops `input_role`, `to_kind`, three-valued `stated` | `to_kind` is set on 25 live rows and `stated` holds three values *(checked)*; the integrity check and LED-162's band arithmetic read them | ideal ✗a | **Keep the live columns.** Rejected |
| P11 | bytes | manifests and `file_anchor` | `retrievals` with NOT NULL pointers | 404 of 433 manifest lines load; 11 of 53 sources appear in no manifest and 15 have no strict payload *(pass)*; `source_type` is NULL on 25 of 53 *(checked)*. "Re-read, not migrated" strands admitted rows (LED-169, LED-170) and makes the path a research act (rule 10) | v2.2 ✗c; ideal ✗a | **Adopt a `retrievals` table by widening `search_execution_artefacts` (110 rows, all map to manifest paths), with the pointers nullable on legacy-bearing tables.** The writer refuses a new row without one; a derived query lists the rows still without bytes as the R10 backlog. The manifest stays the write-ahead log the table is rebuilt from, so it is a recorded rule-5 tension, not a second reader. Backfill from manifests is a tooling migration; re-retrieving the unlinked sources is Phase 5. **End state is the ideal's constraint:** the legacy rows are defective against R10 and CLAUDE.md 5(c), so the nullable pointer is a transition; when the backlog query returns nothing, a final migration makes it NOT NULL |
| P12 | scans | land T1's scan contract | `scan_id` NOT NULL with a composite FK on extractions | `main` has no scans; every live extraction fails the constraint as written *(pass)* | ideal ✗a | **T1's contract governs;** legacy extractions keep a NULL scan, refused for new rows by the writer, until their sources have bytes (P11) and a scan can be recorded honestly; then the pointer is made NOT NULL as in P11 |
| P13 | admissions and slug links | silent | derive `search_admissions`, `results_admitted`, `source_slug_links` | 7 of 55 admission edges are derivable from candidates; 65 admissions are recorded; 14 slug links (6 sources, four of them twice) have no derivation and cannot load into a UNIQUE `ref_id` *(checked)* | ideal ✗a | **Keep the three.** Rejected |
| P14 | dropped columns | silent | "columns not shown are retired" | 82 `evidence_sources` columns are dropped, 43 with data (`pages` 42, `verification_method` 48, `metadata_quality` 53); `source_value_extractions` loses the value-genealogy columns that `v_value_independence` counts *(pass)* | ideal ✗a | **No column is retired without naming its reader and following rule 5's order.** K17 and K23 substrates stay |
| P15 | registry and map names | silent | `lens_crossings`, `lens_matches`, `base_taxonomy_identity`, `base_taxonomy_needs` | the ledger records the companion names as reopened and "confirmation pending" (`references/project-standards.md:2166–2178`, `:2480–2481`) *(pass)* | ideal ✗b | **Not adopted;** live names stay until the owner confirms |
| P16 | LED-202, preliminary figures | silent | adopts a side | the atom is OPEN *(pass)* | ideal ✗a | **Left open;** nothing is built on either answer |
| P17 | `v_render` lifecycle | n/a | claims every view filters lifecycle | `v_render` still shows a superseded source's reference *(pass)* | ideal ✗a | **Fix when 3.R builds the view:** filter on `superseded_by_ref_id IS NULL` in its subqueries |
| P18 | the determination's marker | 3.R: a view that "already carries" it | `marker` column, CHECKed | no view carries it; the logic is in `pilot_renderings.py`; all 8 live rows are retired *(checked)*; five provisional legacy rows cannot take a computed marker *(pass)* | v2.2 ✗a; ideal ✗a | **Add a nullable `marker` the engine computes from `tier_ladder.band`; the CHECK applies to live (unretired) rows only.** 3.R builds the view |
| P19 | Pydantic mirrors | defer to the owner's ruling | generate the mirrors | a requirement the owner ratified (OD-7); a generated mirror cannot drift (rule 8) | — | **v2.2 stands.** If the requirement stays, generate |
| P20 | walkers | `tools/` walkers go in 1.1 | one `walk` and one `walkability` check replace four walkers (2,635 lines) | the script reproduces 21 of 82 *(checked)*; `graph_audit` and `graph/` remain after 1.1 | v2.2 ✗c | **Adopt in Phase 4:** the derived check replaces the `graph_audit` stack |
| P21 | hard-coded paths, clocks, connection | silent | `dbcore.connect`, `REPO_ROOT`, `now`, injected | 157 bindings, 69 and 58 files *(pass)* | v2.2 ✗(rule 8) | **Adopt in Phase 4, file by file, behaviour-preserving,** each binding deleted where replaced |
| P22 | verbs | delete verbs used three times or fewer that nothing needs | 28 verbs | the figure turns on counting (29 or 12 of 72 at ten or more; plan §1) | — | **v2.2 stands;** the ideal's merges (`decline-parameter` into `add-parameter`, and so on) are done where a stage repair touches them |
| P23 | orphan tables | silent | delete or merge | nine tables are empty and orphaned; eight hold rows (counts in §2) | v2.2 ✗c | **New step 1.9: drop the five empty, unreferenced ones** (`external_root_registry`, `bpc_metadata`, `reference_stubs`, `search_coverage`, `search_languages`; rehearsed: readers in `db.py`, `test_db_integrity` and `research_protocol_audit`). Row-bearing orphans go to the owner case by case (LED-169); `conflicts`, `connections`, `connection_targets`, `case_studies` follow P1 and P5 |
| P24 | reaching the target | tooling PRs, then one research PR | "tooling PRs ordered along the spine" | the ideal's path includes re-retrieving 11 to 15 sources, supplying `source_type` for 25, `title` for 343 locators, a marker for five determinations, and the ledger entries *(pass)* | ideal ✗b (rule 10) | **Split:** structure in tooling PRs; content acts in Phase 5 or the ledger |

## 6. What changes in the plan

- §4 gains the owner questions below; step 1.4 is gated on the `serves_axes` value.
- New step 1.9 (P23).
- Phase 3 is rewritten per stage from P1, P2, P6, P11, P12, P17, P18, with each addition naming what it replaces and the handshake it makes walkable.
- Phase 4 gains 4.4 (the walkability check replaces the `graph_audit` stack, P20) and 4.5 (centralize bindings, P21).
- Phase 5 gains the legacy backfill and re-retrieval (P11, P24).
- The ideal's own file carries a banner: its DDL is a target shape, not a migration, and §5 of this file supersedes its adjudications where they differ.

## 7. Owner questions that remain

1. `slugs.serves_axes` value `["AX-BAL"]` may be destroyed (LED-169; step 1.4).
2. T1 extras: strike or keep `term_catalogue_origins` (SES-063).
3. `case_studies` and `economics_entries`: fold into sources and extractions (RES-12)?
4. The registry and map names (P15).
5. LED-202: may a preliminary full-read figure set a published value?
6. T3-grey alone: `pending` or `provisional` at ○ (C-004; the ideal recommends the latter, matching Option A for a T6-only cell).
7. Re-baseline the migrations (both documents say no).
8. Retire the Pydantic mirror requirement, or generate the mirrors.
9. The `migration_reproducibility_deep` divergence from the bot's `evidence_sources` updates: compensating migration, or widen the exemption.
10. Doctrine text owed (mission wording, markers, tier wording, jurisdiction §2.3; the plan's §4 sheet).

## 8. Limits

[CONFIDENCE: medium — the antagonist's reachability table (28 of 53 sources and the rest) is its measurement; I re-ran the counts behind P3, P9, P10, P13 and the walkability script, not the row-by-row load.]
[GAP: the size of everything this file adds is not measured; every addition above is stated as replacing something, and none is sized.]
[GAP: P1's pointer table is named, not designed; its row-level rehearsal is the first deliverable of the synthesis step.]
[ASSUMPTION: the owner's instruction to adjudicate covers choosing which record governs and the course of action, and not rewriting doctrine text.]
[NULL: no adjudication here changes a research row or a ratified document.]
