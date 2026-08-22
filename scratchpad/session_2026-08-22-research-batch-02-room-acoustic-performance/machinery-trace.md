# Machinery trace — research batch 02

Generated from the DB schema, `governance/check-registry.yaml` and `governance/pipeline-map.yaml`.
**No grep, no regex** — per the rule ratified 2026-08-22, a hit count is not a finding.

Owner directive 2026-08-22: *"trace how it interacts with all of our machinery and conversely
see how much of our machinery isn't being used."*

## 1. Data surface — 65 tables

### Written by this batch (8)

| table | rows this batch | rows total |
|---|---:|---:|
| `citation_mining` | 2 | 7 |
| `evidence_population_match` | 13 | 25 |
| `evidence_source_authors` | 14 | 37 |
| `evidence_sources` | 5 | 10 |
| `search_admissions` | 5 | 10 |
| `search_candidates` | 14 | 44 |
| `search_executions` | 9 | 18 |
| `source_slug_links` | 5 | 10 |

### Populated but untouched by this batch (24)

These hold data and this batch neither read nor wrote them through a logged act.

`access_duration`(3), `access_need_axis_map`(21), `access_need_icf`(43), `access_needs`(17), `access_stakes`(3), `axes`(17), `data_migrations`(342), `decisions`(166), `gaps`(4), `item_axis_links`(158), `item_population_links`(372), `items`(93), `jurisdictional_values`(109), `lang_jur_map`(70), `life_stage_modifiers`(2), `population_axis_map`(53), `populations`(23), `rooms`(17), `slugs`(106), `source_locators`(835), `term_aliases`(2382), `term_item_links`(147), `terms`(88), `weighting_profile`(5)


### Empty — 33 of 65 tables carry no rows at all

This is the blunt measure of how much of the schema is unused.

`bpc_metadata`, `case_studies`, `case_study_outcomes`, `case_study_populations`, `case_study_specs`, `case_study_strategies`, `citation_population_links`, `conflicts`, `connection_targets`, `connections`, `convergence_assessment`, `economics_entries`, `economics_entry_populations`, `economics_entry_specs`, `external_root_registry`, `extraction_population_links`, `gap_mining`, `item_audit_runs`, `item_bpc_links`, `item_population_elaborations`, `pipeline_runs`, `probe_population_links`, `reasoning_doc_citations`, `room_items`, `search_coverage`, `search_languages`, `situations`, `source_value_extractions`, `spec_value_probes`, `specification_source_links`, `specifications`, `supersession_check`, `url_verification_runs`


## 2. Views — 17

`governance/pipeline-map.yaml` records, after a corrected fourth pass, that **zero of these
are queried by any code**. This batch queried none of them either.

`v_best_practice`(0), `v_code_floor_only`(0), `v_coverage_branch`(8), `v_coverage_jurisdiction`(3), `v_coverage_language`(3), `v_coverage_priority`(7208), `v_divergence`(0), `v_item_extractions`(0), `v_item_provenance`(0), `v_pending`(0), `v_pmp_latest_walk`(0), `v_registry_duplicate_descriptions`(0), `v_root_id_conflicts`(0), `v_source_admission`(10), `v_source_reach_all`(10), `v_unregistered_roots`(0), `v_value_independence`(0)


## 3. Check surface — 63 registered, 4 quarantined

Quarantined and therefore NEVER selected by `run_checks.py`: `validate_db`, `adjudication_integrity`, `code_currency_audit`, `pre_rehab_banner_audit`


Registered checks by declared kind:

| kinds | n | ids |
|---|---:|---|
| `data,schema` | 11 | `migration_reproducibility`, `migration_reproducibility_deep`, `population_integrity_audit`, `test_db_integrity`, `validate_axes`, `validate_items`, `validate_jurisdiction`, `validate_population`, `validate_pydantic_schemas`, `validate_schema_cross_check`, `validate_verification_consistency` |
| `data,synthesis` | 10 | `audit_evidence_metadata`, `author_fidelity`, `citation_mining_session`, `gap_mining_audit`, `graph_audit`, `metadata_integrity_audit`, `pmp_audit`, `reasoning_doc_citations_audit`, `research_dod`, `research_protocol_audit` |
| `always` | 8 | `check_json`, `check_utf8_md`, `check_yaml`, `research_contract_baseline_ratchet`, `research_dod_selftest`, `retired_vocabulary`, `validate_bpc`, `validate_cross_refs` |
| `governance,synthesis` | 6 | `attestation_evidence`, `attestation_presence`, `attestation_schema`, `attestation_verdict`, `claims_docket`, `doctrine_recheck` |
| `data,tooling` | 4 | `db_path_env_audit`, `readonly_db_open_audit`, `test_assess_cell_pilot`, `test_directness_2_2` |
| `data` | 3 | `alias_provenance_audit`, `citation_mining_backlog_t2`, `source_slug_links_duplicates` |
| `governance,tooling` | 3 | `pipeline_contract_audit`, `research_contract_sync`, `test_pipeline_contract` |
| `tooling` | 3 | `test_graph_audit`, `test_url_verifier`, `test_verification_pipeline` |
| `data,render` | 3 | `evidentiary_audit_fresh`, `pipeline_completeness_fresh`, `site_pages_fresh` |
| `data,governance,schema` | 2 | `decision_capture`, `validate_schema` |
| `data,schema,tooling` | 2 | `test_evidence_cell_state_2_3`, `test_validate_evidence_state_2_4` |
| `data,schema,synthesis` | 1 | `validate_evidence_state` |
| `data,governance` | 1 | `audit_adversarial_use` |
| `governance,schema` | 1 | `matrix_consistency` |
| `synthesis` | 1 | `validate_reasoning` |
| `data,governance,schema,tooling` | 1 | `context_map_fresh` |
| `data,render,synthesis` | 1 | `check_rendered_docs` |
| `data,render,tooling` | 1 | `register_integrity_check` |
| `render` | 1 | `render_audit_browser` |


## 4. What this changeset actually selects

Work kinds selected: **data, governance, render, schema, synthesis, tooling**

Paths in the changeset that select NO kind-scoped battery: **13**

`.ignore`, `CLAUDE.md`, `references/connection-register.md`, `references/synonym-chart.md`, `references/tooling-register.md`, `retrieval-log/session_2026-08-22-research-batch-02-room-acoustic-performance/`, `scratchpad/session_2026-08-20-provenance-walk/commands.jsonl`, `scratchpad/session_2026-08-22-record-correction-and-biblio-repair/commands.jsonl`, `scratchpad/session_2026-08-22-research-batch-02-room-acoustic-performance/`, `skills/question-author_SKILL.md`, `skills/workplan-orchestrator_SKILL.md`, `workplan/2026-08-22-agonist-antagonist-execution-plan.md`


Repo-wide for comparison: **1233 of 2183** tracked files select no kind-scoped battery.


## 5. What this measures, stated plainly

This is the first time the question could be answered with a real batch on one side of it. Every
prior utilisation claim in this repository was made against **zero** research, so "unused" and
"waiting for subjects" were indistinguishable. They are now distinguishable.

**The batch used 8 tables of 65.** It wrote `search_executions`, `search_admissions`,
`search_candidates`, `evidence_sources`, `evidence_source_authors`, `source_slug_links`,
`evidence_population_match`, `citation_mining`. That is the whole of the collection-and-grading
stratum, and it is the only stratum a batch **can** exercise.

**33 of 65 tables hold no rows at all** — and the emptiness divides into three kinds that should
never be conflated:

1. **Waiting on the owner, not on work.** `specifications`, `specification_source_links`,
   `convergence_assessment`, `source_value_extractions`, `spec_value_probes`. These are the
   determination stratum. They are empty because **D-0165 deferred the population-taxonomy
   question**, so no cell on the only slug with admitted evidence is authorable. A batch cannot
   fill them; a decision can.
2. **Waiting on a class of finding this batch did not produce.** `case_studies`, `economics_entries`
   and their junctions, `conflicts`, `gap_mining`. R12 routes findings here when they occur; none
   occurred, and the DoD gate confirmed that rather than assuming it (`economics_entries=0 for 0
   prose findings`).
3. **Structurally unreachable or superseded.** `item_bpc_links` (0 rows, the slug→item bridge the
   pilot engine's own gap description calls "1/92 populated" — it is now 0/93), `reasoning_doc_citations`
   (0, and FK-blocked by OD-5 per D-2's record), `search_coverage`/`search_languages` (frozen legacy),
   `pipeline_runs`/`url_verification_runs` (job-owned, no job has run against canonical),
   `external_root_registry`, `room_items`, `situations`.

**All 17 views were unused, again.** The map records that zero of them are queried by any code; this
batch adds that zero are queried by a *research act* either. `v_coverage_priority` holds **7,208
rows** — the largest derived object in the database — and nothing reads it. `v_best_practice`, which
carries the only semantic guard in the schema, holds 0 rows and will stay empty until §1 above moves.

**The check surface is 63 registered, 4 quarantined.** The quarantined four are never selected by
`run_checks.py` — which is how `adjudication_integrity` sat on a real 5-of-5 finding unseen until it
was run by hand on 2026-08-22.

**Selection is the sharpest finding.** This changeset selects **all six** work kinds, so it draws the
full battery. But **13 of its own paths select nothing**, and repo-wide **1,233 of 2,183 tracked
files (56%)** select no kind-scoped battery at all. Among this changeset's unselected paths are
`CLAUDE.md`, `.ignore`, two `skills/*_SKILL.md` files a session actually loads, and the entire
`retrieval-log/` — the fabrication-defence artefact store. A commit that touched only those would run
the 8 `always` checks and nothing else.

**The honest summary.** The machinery that acts on research is small, and this batch exercised nearly
all of it. The machinery that is idle is idle for three different reasons, and only one of them
("waiting for subjects") is the reason usually given. The determination stratum is blocked on a
decision; the routing stratum is correctly empty; and a third of the schema is structurally
unreachable, superseded, or read by nothing.
