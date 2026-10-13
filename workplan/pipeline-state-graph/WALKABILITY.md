# WALKABILITY: the pipeline walked in every direction

**Status.** A measurement, 2026-10-13, not a ruling; nothing here is entered in the ledger. Instrument: `workplan/pipeline-state-graph/walkability.py` (read-only). It reads the schema, the stage-map and the spine in `governance/pipeline-contract.yaml`, counts non-NULL pointers, and asks of each view whether it returns a row; it reads no other row. Three states are measured: **live** (`data/guidebook.db`, `user_version 101`, 82 tables, 115 foreign keys, 21 views); **post-Phase-1 with R32**, the Phase 1 rehearsal clone (A2, commit `9cef95e`: 54 tables, 70 foreign keys, 20 views) with the stage-map edited so that `source_value_extractions` and `extraction_relations` sit in judgment, as `RULINGS.md` R32 rules; and the **stacked end-state**, the rehearsal stack of every slice in the plan's order (`rehearsals/STACK.md`: 56 tables, 78 foreign keys, 22 views, `user_version 114`; the stage-map there already carries R32). The stack is a rehearsal, not an execution (plan §5a).

**Verdict: no.** The chain from a determination back to the search that found its source has one broken link (synthesis does not point at judgment) and one reversed link (research holds the pointer to evidence, evidence holds none to research), and after Phase 1 nothing in any stage reaches render (today only the empty item cluster does). At the level of records, one parameter of ten and one slug of 106 reach an extraction. Phase 1 as rehearsed deletes 45 foreign keys and adds none; the four populated ones it removes are all in the two axis-map tables R3 retires, so no populated pointer on the spine is lost. **The whole stack then adds 8 declared pointers (T1's three, R24's one, R18's four lens keys) and populates none**: 78 foreign keys declared, 48 populated, the same count as after Phase 1 (the M4 rename swaps `population_icf_links`'s two columns for `identity_icf_map`'s). On the `IDEAL-GRAPH.md` §6 script 15 of 56 tables fail on the stack (21 of 82 live). What would repair the chain is already in the plan or the rulings (R32's map change, 3.R's view, data); one design question, whether a search may be recorded without a slug, is covered by no ruling (section 7, finding 4).

## 1. What is counted

For an ordered pair of stages (a before b in the spine), per the docstring of `walkability.py`:

- **up**: tables of b that reach a table of a by following foreign keys child → parent, through any stage. A single join chain; the cardinality at each step is many-to-one.
- **down**: tables of a that reach a table of b by following foreign keys parent → child. A reverse lookup, one-to-many; the same edges as *up*, counted from the other end because a sender needs the receiver's pointer to exist.
- **skip**: as *up*, never passing through a table of a stage between a and b.
- **recvFK / sendFK**: foreign keys whose child is in b and parent in a (the later stage holds the pointer back: the normal direction), and those whose child is in a and parent in b (the earlier stage holds a pointer forward: re-entrant).
- **zigzag**: the shortest undirected path between any table of a and any table of b over foreign keys and over "a view reads both" co-reads, never passing through a base, infrastructure or unmapped table (base connects everything and so walks nothing; the others are not spine stages). Equal-length ties go to fewer view hops, then alphabetical order. The path is an existence proof; the matrix is the measure.
- **lateral**: tables of one stage joined through a shared foreign-key parent or child, or by a foreign key between two tables of the stage. **Re-entrant**: foreign keys whose child stage precedes the parent stage. **Declared** means the foreign key exists; **populated** means some child row carries a non-NULL pointer.

A table is never a stage and the matrix is a function of the stage-map: a wrong map gives a wrong matrix (section 7, finding 7). Joins through a shared vocabulary value (the lens crossing, by `identity_code` and the others) are not counted as walks; they are the crossing, and a view reads both sides.

## 2. Structure: every ordered pair

`up / down / skip / recvFK / sendFK`; – means no intermediate stage to skip.

| pair | live | post-Phase-1 with R32 | stacked end-state |
|---|---|---|---|
| base → research | 7 / 1 / – / 6 / 0 | 5 / 1 / – / 4 / 0 | 5 / 5 / – / 8 / 0 |
| base → evidence | 11 / 7 / 11 / 10 / 0 | 2 / 1 / 2 / 2 / 0 | 3 / 3 / 3 / 3 / 0 |
| base → judgment | 4 / 7 / 4 / 4 / 0 | 3 / 7 / 3 / 7 / 0 | 4 / 7 / 4 / 7 / 0 |
| base → synthesis | 3 / 1 / 3 / 2 / 0 | 2 / 1 / 2 / 2 / 0 | 2 / 1 / 2 / 2 / 0 |
| base → specification | 5 / 7 / 5 / 8 / 0 | 4 / 7 / 4 / 7 / 0 | 4 / 7 / 4 / 7 / 0 |
| base → render | 5 / 6 / 5 / 8 / 1 | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 |
| research → evidence | 0 / 0 / – / 0 / 3 | 0 / 0 / – / 0 / 3 | 0 / 0 / – / 0 / 3 |
| research → judgment | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 |
| research → synthesis | 0 / 0 / 0 / 0 / 1 | 0 / 0 / 0 / 0 / 1 | 0 / 0 / 0 / 0 / 1 |
| research → specification | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 |
| research → render | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 |
| evidence → judgment | 5 / 3 / – / 3 / 0 | 4 / 2 / – / 4 / 0 | 5 / 3 / – / 5 / 0 |
| evidence → synthesis | 3 / 1 / 3 / 3 / 1 | 3 / 1 / 3 / 3 / 0 | 3 / 1 / 3 / 3 / 0 |
| evidence → specification | 4 / 2 / 4 / 4 / 0 | 3 / 1 / 2 / 2 / 0 | 3 / 2 / 2 / 2 / 0 |
| evidence → render | 1 / 1 / 1 / 1 / 3 | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 |
| judgment → synthesis | 0 / 0 / – / 0 / 2 | 0 / 0 / – / 0 / 2 | 0 / 0 / – / 0 / 2 |
| judgment → specification | 0 / 0 / 0 / 0 / 1 | 1 / 1 / 1 / 1 / 0 | 1 / 1 / 1 / 1 / 0 |
| judgment → render | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 |
| synthesis → specification | 3 / 3 / – / 2 / 0 | 3 / 3 / – / 2 / 0 | 3 / 3 / – / 2 / 0 |
| synthesis → render | 0 / 0 / 0 / 0 / 1 | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 |
| specification → render | 0 / 0 / – / 0 / 1 | 0 / 0 / – / 0 / 0 | 0 / 0 / – / 0 / 0 |

Reading it: research → evidence has `recvFK 0` and `sendFK 3` in both states: no evidence table points at a research table; `search_admissions.ref_id`, `search_executions.mined_ref_id` and `search_candidates.resolved_ref_id` point the other way. Judgment → synthesis is `0 / 0 / – / 0 / 2` in both: no synthesis table points at a judgment table, and the two forward keys hold no pointer (`evidence_population_match.gap_id`, and live `citation_population_links.citation_id`, post-R32 `source_value_extractions.promoted_to_rdc_id`). Every pair with render is 0 after Phase 1. Under the live map judgment is a leaf (no foreign key anywhere has a judgment table as parent); under R32 it is not (`specification_extraction_links.extraction_id` points at an extraction), which is why the second and third columns differ from the first. The stack differs from the second column by T1's tables (`source_scans` points at a parameter: `base → evidence` `recvFK` 2 → 3; `extraction_follow_ups` points at an extraction, a judgment-to-judgment edge, so it raises `up` for `base → judgment` 3 → 4 and `evidence → judgment` 4 → 5 and no `recvFK`), by R24 (the registry now has a child: `evidence → judgment` `recvFK` 4 → 5 and `down` 2 → 3, `evidence → specification` `down` 1 → 2) and by R18's four lens keys (`base → research` `recvFK` 4 → 8, `down` 1 → 5).

## 3. The practical walk: zigzag over populated pointers

| stages | live | stacked end-state |
|---|---|---|
| research ↔ evidence | search_admissions - evidence_sources | search_admissions - evidence_sources |
| research ↔ judgment | search_admissions - evidence_sources - evidence_population_match | search_admissions - evidence_sources - evidence_population_match |
| research ↔ synthesis | search_admissions - evidence_sources - convergence_sources | search_admissions - evidence_sources - convergence_sources |
| research ↔ specification | search_admissions - evidence_sources - determination_gates | search_admissions - evidence_sources - determination_gates |
| research ↔ render | NO PATH | NO PATH |
| evidence ↔ judgment | evidence_sources - evidence_population_match | evidence_sources - evidence_population_match |
| evidence ↔ synthesis | evidence_sources - convergence_sources | evidence_sources - convergence_sources |
| evidence ↔ specification | evidence_sources - determination_gates | evidence_sources - determination_gates |
| evidence ↔ render | NO PATH | NO PATH |
| judgment ↔ synthesis | evidence_population_match - evidence_sources - convergence_sources | evidence_population_match - evidence_sources - convergence_sources |
| judgment ↔ specification | evidence_population_match - evidence_sources - determination_gates | source_value_extractions - specification_extraction_links |
| judgment ↔ render | NO PATH | NO PATH |
| synthesis ↔ specification | convergence_assessment - specifications | convergence_assessment - specifications |
| synthesis ↔ render | NO PATH | NO PATH |
| specification ↔ render | NO PATH | NO PATH |

Both columns use only foreign keys with a non-NULL pointer and views that return a row. Every populated path that leaves research, and the path from judgment to synthesis, runs through `evidence_sources`: research reaches judgment, synthesis and specification only by first reaching a source. The declared graph offers an alternative route of the same length between research and judgment (`gap_mining` → `gaps` → `evidence_population_match`) that no row uses. Every populated path above is foreign keys only: the synthesis paths end in `convergence_sources` (69 rows, pointing at `evidence_sources`), and `judgment ↔ synthesis` runs `evidence_population_match` → `evidence_sources` ← `convergence_sources`, through a source and not through an extraction. The only direct judgment ↔ specification path after R32 is the 151-row `specification_extraction_links`.

## 4. Lateral, re-entrant, orphans

**Lateral** (components of same-stage tables joined through a shared parent or child):

| stage | live: tables / components / isolated | stacked end-state: tables / components / isolated |
|---|---|---|
| base | 23 / 7 / access_duration, access_stakes, lang_jur_map, life_stage_modifiers, situations | 18 / 6 / access_duration, access_stakes, lang_jur_map, life_stage_modifiers, rooms |
| research | 11 / 5 / gap_mining, reference_stubs, research_code_leads, source_locators | 8 / 4 / gap_mining, research_code_leads, source_locators |
| evidence | 17 / 3 / external_root_registry, url_verification_runs | 8 / 1 / none |
| judgment | 5 / 3 / evidence_population_match, term_adjudications | 5 / 2 / term_adjudications |
| synthesis | 8 / 3 / conflicts | 8 / 3 / conflicts |
| specification | 5 / 1 / none | 4 / 1 / none |
| render | 6 / 2 / weighting_profile | 1 / 1 / weighting_profile |
| infrastructure | 7 / 6 / bpc_metadata, data_migrations, decisions, item_audit_runs, pipeline_runs | 4 / 3 / data_migrations, decisions |

**Re-entrant foreign keys** (the earlier stage points forward):

| FK (child → parent) | live non-NULL rows | stacked end-state |
|---|---:|---|
| `search_admissions.ref_id` → `evidence_sources` | 55 | kept |
| `search_executions.mined_ref_id` → `evidence_sources` | 11 | kept |
| `search_candidates.resolved_ref_id` → `evidence_sources` | 7 | kept |
| `case_study_specs.item_code` → `items` | 0 | table dropped |
| `citation_population_links.citation_id` → `reasoning_doc_citations` | 0 | table dropped |
| `conflicts.item_code` → `items` | 0 | key dropped, table kept |
| `economics_entry_specs.item_code` → `items` | 0 | table dropped |
| `evidence_population_match.gap_id` → `gaps` | 0 | kept |
| `gap_mining.gap_id` → `gaps` | 0 | kept |
| `jurisdictional_values.item_code` → `items` | 0 | table dropped |
| `probe_population_links.probe_id` → `spec_value_probes` | 0 | table dropped |
| `room_items.item_code` → `items` | 0 | table dropped |
| `source_value_extractions.promoted_to_rdc_id` → `reasoning_doc_citations` | 0 | kept |
| `spec_value_probes.item_code` → `items` | 0 | table dropped |

The three populated edges are research recording what became evidence, the re-entry CLM-029 licenses. The other re-entrant keys are empty or all-NULL; `evidence_population_match.gap_id` is NULL on all 54 rows, and `gap_mining` is empty, so the gap-driven return from synthesis to research is declared and unused. Eight of the fourteen go with Phase 1 (six into `items`, two link tables; the stack keeps the other six). The probe's fourteen is between spine stages and counts six into `items`; `RULINGS.md` R42 first said fourteen but named seven into `items` (the seventh is `item_audit_runs`, infrastructure and outside the spine), so its list summed to fifteen; it is corrected to six in the same commit (its `[CORRECTION]` line), and the probe confirms the corrected enumeration.

**Orphans** (no foreign key in or out, no view reads): live, 11 (`access_duration`, `access_stakes`, `data_migrations`, `life_stage_modifiers`, `pipeline_runs`, `reference_stubs`, `research_code_leads`, `situations`, `source_locators`, `url_verification_runs`, `weighting_profile`); post-Phase-1 and on the stack, 10 (`access_duration`, `access_stakes`, `conflicts`, `data_migrations`, `decisions`, `life_stage_modifiers`, `research_code_leads`, `rooms`, `source_locators`, `weighting_profile`). **Id columns with no foreign key:** live and post-Phase-1, `source_value_extractions.root_id` and `conflicts.gap_id`, both with 0 non-NULL rows; on the stack R24 gives `root_id` its key (still 0 non-NULL), leaving `conflicts.gap_id`.

**Views spanning more than one stage:** 11 live and after Phase 1, 12 on the stack (T1's `v_scan_ledger` reads base, evidence and judgment), none reading render. After R32 `v_value_independence`, `v_unregistered_roots` and `v_determination_provenance` also read judgment.

## 5. Declared against populated

| state | foreign keys | with a non-NULL pointer | child table empty | child populated, every pointer NULL |
|---|---:|---:|---:|---:|
| live | 115 | 52 | 52 | 11 |
| post-Phase-1 | 70 | 48 | 11 | 11 |
| stacked end-state | 78 | 48 | 14 | 16 |

Phase 1 removes 45 foreign keys; 41 of them have no pointer. The 4 populated ones are the two keys each of `access_need_axis_map` (21 rows) and `population_axis_map` (53 rows), which R3 retires; the other row-bearing tables R3 drops, `axes` (17) and `pipeline_runs` (6), carry no populated key. The stack's 16 all-NULL keys are those 11 with `source_value_extractions.root_id` (101 rows) and R18's four lens keys on `search_executions` (191 rows each) added; its 14 empty-child keys add T1's `source_scans` and `extraction_follow_ups`. The 11 all-NULL keys of the first two states are the same 11: `evidence_population_match.gap_id` (54 rows), `populations.parent_code` (23), `search_executions.origin_pass_id` (191), `economics_entries.ref_id` (1), `base_parameters.merged_into` (10), `specifications` `icf_code`, `needs_code` and `medical_code` (8 each), and `source_value_extractions` `promoted_to_rdc_id`, `icf_code` and `medical_code` (101 each). Count after count, the declared graph is larger than the walked one.

## 6. Records: the funnel on the live database

Each row is a walk; the queries use `EXISTS`, not `NOT IN` (`search_candidates.exec_id` is nullable, and a `NOT IN` over it returned 0 on the first try: a vacuous zero, CLAUDE.md §5a).

| walk | start | reaches |
|---|---:|---:|
| extraction → its source | 101 | 101 |
| extraction → source → admission → execution (back to the search) | 101 | 98 |
| source → slug link / observed term / extraction | 53 | 53 / 53 / 53 |
| source → population match | 53 | 48 |
| source → convergence | 53 | 15 |
| source → specification link (`specification_source_links`; 20 sources through extraction links) | 53 | 8 |
| observed term → adjudication | 88 | 77 |
| extraction → specification | 101 | 33 |
| parameter → extraction / specification | 10 | 1 / 1 |
| slug → execution / source link / extraction | 106 | 2 / 5 / 1 |
| execution → admission row / candidate row | 191 | 48 / 59 |
| execution → neither (results found 85 of these) | 191 | 98 |
| candidate → its execution | 147 | 107 |

Further: 2 of 53 sources (`REF-00987`, `REF-01010`; both VERIFIED, tier 6, `code`) have no admission row, so 3 extractions cannot be walked back to a search. 7 executions state 10 admitted results (`results_admitted`) and have no `search_admissions` row: the counts sum to 65, the rows to 55. The seven are executions 1, 3, 6, 10, 13, 14 and 16 of batches 01 and 02 (2026-08-19 and 2026-08-22); no execution below 30 has an admission row and the first `search_admissions` row is execution 30 (2026-09-16), so these searches predate the rows. 40 of 147 candidates have a NULL `exec_id`. 73 of 76 `gaps` are pointed at by no foreign key (3 by `specifications.gap_register_id`). All 8 specifications are retired; the five convergence assessments are reachable from extractions only through them (`specifications.convergence_id` → `specification_extraction_links`). Lens columns on the 101 extractions: `identity_code` 101, `needs_code` 1, `icf_code` 0, `medical_code` 0; on the 8 specifications: `identity_code` 8, the others 0.

## 7. Findings, worst first

1. **Render is not in the graph.** Every pair with render is 0 after Phase 1; the stage is one orphan table (`weighting_profile`). The walk into render will be a view and a renderer that do not yet exist (3.R). The probe reads stages from tables only (`stage-map.yaml` lists tables), and a view's stages are those of the tables it reads, so a view that reads only specification tables is one-stage whatever it is for: a render pair becomes non-zero only when the view reads a table mapped to render. Until then a walk into render is unmeasurable by this instrument, not merely unmet.
2. **Synthesis does not point at judgment.** `convergence_sources` (69 rows) points at sources, not extractions; which figures converged is answerable only through the retired specifications. R17 builds nothing and carries the walk through the determination; that satisfies the declared walk and leaves the record-level walk answerable for nothing live.
3. **Research ↔ the later stages runs only through `evidence_sources`, and the sender holds the pointer.** A source records no search; the walk back is a reverse lookup on `search_admissions.ref_id` (51 of 53 sources, 98 of 101 extractions). The gap-driven return from synthesis to research has declared keys and no rows. 85 executions found results and left neither an admission nor a candidate (screened out by design or lost: the schema does not distinguish them [UNVERIFIED]); 7 early executions (ids 1 to 16, August 2026) claim admissions that predate the `search_admissions` rows (the first row is execution 30).
4. **Breadth is data, but one constraint is design.** One parameter of ten has extractions; two of 106 slugs have executions. `search_executions.slug` and `search_candidates.found_under_slug` are NOT NULL, so a search that targets a parameter or a lens and no slug cannot be recorded, which collides with the owner's "regardless of search slug". R18 adds four nullable lens keys to `search_executions` and leaves the slug as it is; no ruling decides it [GAP: no ruling covers nullable slug on searches]. `IDEAL-GRAPH.md` (lines 225 and 236) already drafts the shape — `slug` nullable beside a CHECK that one of `slug`, `synthesis_id`, `mined_ref_id` is set — and `COMPARISON.md` does not adopt it.
5. **The lens crossing is mostly empty.** Of four lens columns, one carries values (`identity_code`); `needs_code` has one row. There is nothing to walk across until the medical and ICF fill in Phase 5 (R16).
6. **Unpointed rows and keys:** 73 of 76 gaps; `conflicts.gap_id` and `root_id` without keys; ten orphan tables after Phase 1, nine of them row-bearing (only `conflicts` is empty), which are the owner's case by case (LED-169) or pointers to add.
7. **The matrix is only as right as the map.** Under the live map judgment is a leaf and the 101 extractions are evidence; moving two entries (R32) makes judgment a stage with a direct pointer from specification. Treat the stage-map as an input to every figure above, not an output of it.

## 8. What the plan's steps change, by direction

Measured on the Phase 1 clone, on the clone with the R32 map, or on the stack (plan §5a); "pending" marks a slice not yet in a measured state.

| step | down | up | lateral | skip | re-entrant |
|---|---|---|---|---|---|
| 1.1–1.3, 1.9 (render apparatus, item layer, splinter tables, empty orphans) | render drained to `weighting_profile`; every render pair 0 | evidence → render `up` 1 → 0 | research 11 → 8 tables, 5 → 4 components (`reference_stubs` out); evidence 17 → 9 tables, 3 → 2 components (7 tables once R32 moves two) | none lost | 14 → 6 edges; the 3 populated kept |
| 1.4–1.5 (axes, scheduled workflows) | 4 populated foreign keys lost, all in the axis maps | – | `situations`, `pipeline_runs`, `url_verification_runs` leave the orphans and isolated lists | – | – |
| 1.6–1.8 (checks, skills, registry prose) | – | – | – | – | – (no schema change) |
| R32 (map) | judgment → specification 0/0/0/0/0 → 1/1/1/1/0 (151 rows) | evidence → judgment `recvFK` 2 → 4 | judgment 2 → 4 tables, 2 components either way | – | `promoted_to_rdc_id` moves from evidence → synthesis to judgment → synthesis |
| 0.2 (T1) | `source_scans` → a parameter: `base → evidence` `recvFK` 2 → 3 (0 rows) | `extraction_follow_ups` → an extraction (judgment to judgment): `up` +1 for `base → judgment` and `evidence → judgment` (0 rows) | – | – | `v_scan_ledger` reads base, evidence and judgment |
| R24 (`root_id` key) | the registry gains a child: `evidence → judgment` `down` 2 → 3, `evidence → specification` `down` 1 → 2 | `source_value_extractions.root_id` → `external_root_registry`: `evidence → judgment` `recvFK` 4 → 5; 101 rows, all NULL; the registry and the extraction table pass `IDEAL-GRAPH.md` §6 (21 → 19 failing in the D rehearsal) | – | – | – (no writer for the registry, so the key stays unpopulated) |
| R18 (lens keys on `search_executions`) | `base → research` `recvFK` 4 → 8: four keys, NULL on all 191 rows | – | research ↔ base lens (a shared-vocabulary join, which the probe does not count; `v_coverage_lens` groups the lens columns of `search_executions` and reads no registry, so the never-searched complement is not derivable from it) | – | – |
| 3.R (view) | specification → render once the view is mapped to render | – | – | – | – (pending) |

Not in the plan; each is a proposal for the owner or Fable, not a ruling:
(a) Whether `search_executions.slug` and `search_candidates.found_under_slug` may be NULL when a search targets a parameter or a lens (finding 4).
(b) Whether the 2 unadmitted sources and the 7 executions whose counts the rows do not show belong to Phase 5's backlog or are recorded as exceptions; they are rows, so they ship with research, not tooling (CLAUDE.md rule 10).
(c) Whether the registered walk check (4.4) includes receiving and sending pointers and the lateral and re-entrant counts or stays the 40-line §6 script. This probe (`wc -l` counts it) is scaffolding that leaves with this folder in Phase 6 unless the owner keeps it; it replaces the plan's earlier statement that "the lateral, skip and re-entrant directions stay unmeasured". Net code added: this file.

## 9. Limits

- The stacked end-state is a rehearsal (plan §5a): R37, 3.R, Phase 2 and the Phase 4 steps are not in it, and its migrations are numbered 102 to 114 for the stack only.
- The post-Phase-1 state is the A2 clone at `9cef95e`; A2's three later fix commits change scripts, not the schema.
- [NULL: unmapped tables] None on either measured state; the probe prints an UNMAPPED stage if there are any.
- Re-derive any figure: `python3 workplan/pipeline-state-graph/walkability.py [DB [STAGE_MAP]]` (add `--json` for the raw structure). The funnel in section 6 is the queries named in its rows, run read-only through `sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)`.
