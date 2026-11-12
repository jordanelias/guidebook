# 21 — Stage `research`

_Generated 2026-11-12 02:01 UTC at commit e73b588, schema user_version 125. Every figure here is computed by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_dossier.py`; re-run it, do not trust this text (CLAUDE.md rule 7a)._


**Contract anchor:** PI rule #7 (adversarial-research); rule #8 (PMP); workplan phase B

**Contract entry condition(s):** an OPEN gap or an item/parameter lacking sufficient evidence

## Tables (8)

| table | rows | columns |
|---|---|---|
| citation_mining | 38 | slug, local_ref_id, global_ref_id, doi, backward, forward, connections_produced, notes, created_at, created_by_session, updated_at, updated_by_session, deferred_reason |
| gap_mining | 0 | gap_mining_id, gap_id, created_at, created_by_session, search_strategy_record, candidates_returned, candidates_reviewed, outcome, discoveries_logged, candidate_dois, check_method, notes |
| research_code_leads | 96 | lead_id, jurisdiction, standard_name, clause, status, recovered_from, notes, created_at, created_by_session, updated_at, updated_by_session |
| search_admissions | 61 | exec_id, ref_id, created_at, created_by_session |
| search_candidates | 155 | candidate_id, exec_id, found_under_slug, suggested_slug, disposition, title, locator, locator_status, tier_guess, harm_finding, why_not_admitted, notes, created_by_session, created_at, resolved_ref_id, surfaced_in, surfaced_quote, updated_at, updated_by_session |
| search_execution_artefacts | 117 | exec_id, artefact, created_by_session, created_at |
| search_executions | 203 | exec_id, slug, parameter_id, jurisdiction, language, target_tier, target_evidence_type, target_scope, query_text, terms_used, engine, depth_method, mining_direction, results_found, results_screened, results_admitted, saturation_signal, admitted_ref_ids, deferred_reason, backfill, created_by_session, created_at, findings_note, harm_finding, prior_expectation, origin, mined_ref_id, origin_pass_id, updated_at, updated_by_session, identity_code, icf_code, needs_code, medical_code, absence_class |
| source_locators | 893 | ref_id, doi, url, pmid, pmcid, isbn, issn, standard_number, doi_resolution_outcome, url_resolution_outcome, url_last_fetched, recovered_from, authors, pub_year, title, tier_claimed, jurisdiction, used_in_bpcs, status, screened_reason, created_by_session, created_at, notes |

## Views touching this stage (6)

| view | all stages spanned |
|---|---|
| v_coverage_branch | research |
| v_coverage_jurisdiction | research |
| v_coverage_language | research |
| v_coverage_lens | research |
| v_coverage_priority | base, research |
| v_source_admission | evidence, research |

## Contract criteria

| id | kind | check | criterion (first 200 chars) |
|---|---|---|---|
| adversarial-fields-complete | integrity | scripts/audit/research_protocol_audit.py | Every research gap-closure carries the mandatory falsifiable fields (falsification_condition, confidence_interval, shift_conditions, named_dissenter) before status CLOSED. |

## `db.py` verbs that WRITE this stage's tables (13)

| verb | writes | reads | help |
|---|---|---|---|
| add-candidate | search_candidates | search_executions, slugs | Stage a screened candidate (search_candidates |
| add-code-lead | research_code_leads | source_locators | Record a code/standard lead (research_code_leads |
| add-gap-mining | gap_mining |  | Record a gap-driven mining attempt (DR-2026-05-26 |
| add-locator | source_locators | evidence_sources | Write a lead into the clue store |
| amend-search | search_execution_artefacts, search_executions | adversarial_passes, evidence_sources, v_coverage_branch | APPEND a dated correction to a logged search's findings_note |
| link-admission | search_admissions, search_executions | evidence_sources, search_candidates, v_coverage_language | Record that an EXISTING search admitted a source -- only |
| log-mining | citation_mining, evidence_sources | connections, search_candidates, search_executions, source_locators, source_slug_links | Log citation mining |
| log-search | search_admissions, search_execution_artefacts, search_executions | adversarial_passes, base_parameters, evidence_sources, lang_jur_map, slugs, v_coverage_branch, v_research_scope | Append one row to search_executions |
| reattribute-candidate | search_candidates | search_executions, terms | Repoint a candidate at the search that surfaced it |
| resolve-candidate | search_candidates | evidence_sources, slugs | Close a staged candidate, re-describing it from the source (R15 |
| unlink-admission | search_admissions, search_executions | search_candidates, v_coverage_language | Remove a WRONG admission edge (the corrective half of |
| update-code-lead | research_code_leads |  | Move a code lead's status or clause, APPENDING a dated note |
| update-locator | source_locators | evidence_sources | Move a lead's status in the clue store |

## `db.py` verbs that only READ this stage's tables (5)

`add-source`, `coverage`, `is-mined`, `unmined`, `unmined-gaps`

## Other code that WRITES this stage's tables (2)

| file | lines | writes | purpose (docstring) |
|---|---|---|---|
| scripts/dbcore.py | 1385 | source_locators | scripts/dbcore.py — the one place this repository opens, stamps and keys the database. WHY THIS EXISTS. Measured 2026-08-25: 104 raw `sqlite3.connect(` call sites across 55 live files, 48 independent resolutions of GUIDEBOOK_DB_PATH, and 37 |
| scripts/audit/research_batch_dod.py | 1795 | search_admissions, search_candidates, search_executions, source_locators | scripts/audit/research_batch_dod.py — RESEARCH BATCH DEFINITION-OF-DONE gate. **** RESEARCH IS INVALID IF IT IS NOT COMPLIANT WITH THIS PROJECT'S GOVERNANCE, **** **** VERIFICATION TOOLS, RULES AND ETHOS. (owner directive, 2026-07-24) ****  |

## Code that READS this stage's tables, writing none of them (16)

| file | lines | reads | purpose (docstring) |
|---|---|---|---|
| scripts/validate_schema.py | 344 | research_code_leads | scripts/validate_schema.py — Validate entity YAML files against Pydantic schemas. Walks data/ directories and validates each YAML file against the appropriate schema model. Used by CI (schema job) and session start (--quick mode). Usage: py |
| scripts/audit/citation_mining_completeness.py | 376 | citation_mining | scripts/audit/citation_mining_completeness.py Audit citation_mining completeness. Surfaces the GAP-283 protocol-violation pattern: research sessions adding Tier 1-2 evidence_sources rows without corresponding citation_mining rows (per stand |
| scripts/audit/column_vocabulary_audit.py | 214 | source_locators | Do the tables agree on what to call the same thing? WHY THIS EXISTS. A pipeline-walk tool (since deleted) shipped a session-attribution helper matching two column names, `created_by_session` and `session`. The corpus spells that one role EI |
| scripts/audit/derived_not_curated_audit.py | 475 | gap_mining, search_executions | scripts/audit/derived_not_curated_audit.py — CLAUDE.md rule 8, mechanised. THE RULE: derive it, or name who judged it. Never curate a fact the machine can compute. WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS. A curated list and the  |
| scripts/audit/gap_mining_audit.py | 261 | gap_mining | Audit query for gap-driven mining protocol compliance (DR-2026-05-26). Flags: 1. Closed gaps lacking gap_mining row when description signals mining-addressability (an OPEN-ADDRESSABLE gap moved to CLOSED-FIXED with no gap_mining attempt rec |
| scripts/audit/graph_audit.py | 483 | gap_mining | graph_audit.py — vectorized structural audit (stdlib graph spine, data layer). Builds a derived, read-only audit graph from data/guidebook.db and runs Tier-1 topology checks over it, unifying orphan / dangling-reference / empty-table / stat |
| scripts/audit/identifier_floor_audit.py | 158 | source_locators | scripts/audit/identifier_floor_audit.py — an identifier is never reissued. WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS (CLAUDE.md section 1's burden of proof). A source's `ref_id` is how every record outside the database names it: r |
| scripts/audit/jurisdiction_db_vocabulary.py | 146 | source_locators | scripts/audit/jurisdiction_db_vocabulary.py — jurisdiction codes IN THE DATABASE. WHY THIS EXISTS. `governance/jurisdiction-philosophy.md` states the UK/GB rule at ERROR level -- "GB appearing as a jurisdiction code is rejected; must be UK" |
| scripts/audit/migration_reproducibility.py | 618 | citation_mining | scripts/audit/migration_reproducibility.py — GAP-290 enforcement. Rebuilds a fresh DB from the migration history alone and compares core invariants against the committed data/guidebook.db. A divergence means someone wrote directly to the DB |
| scripts/audit/provenance_artefact_audit.py | 153 | search_candidates, search_execution_artefacts | scripts/audit/provenance_artefact_audit.py — a candidate checked against the bytes its search actually returned (RC1, DR-2026-09-26-recurring-defect-shapes-remediation.md section 2). Two registrations, one script -- the precedent is `citati |
| scripts/audit/research_protocol_audit.py | 322 | research_code_leads, search_admissions, search_executions | Audit query for adversarial research protocol compliance. Flags: 1. Closed gaps lacking required protocol fields 2. Verified citations without population match records 3. Population match grade distribution suspicious (>70% EXACT) 4. Confid |
| scripts/audit/search_log_completeness.py | 306 | search_executions | scripts/audit/search_log_completeness.py — every WebSearch the session RAN is a search it LOGGED. WHY THIS EXISTS (I5, process-gap plan WP14). `search_executions` is the one event home of a discovery step (pipeline contract evidence/discove |
| scripts/audit/skill_vocabulary_audit.py | 215 | citation_mining, source_locators | scripts/audit/skill_vocabulary_audit.py — every value a skill names must have a home. WHY THIS EXISTS (CLAUDE.md rule 8; owner 2026-11-06: "ensure all terminologies and vocabularies are correct"). A skill is a prose caller: it tells an oper |
| scripts/audit/graph/topology.py | 259 | gap_mining | scripts/audit/graph/topology.py — Tier 1 graph-topology checks (stdlib only). Each check appends rows to the findings table. Severity is raw here; known-debt suppression and the pass/fail decision live in scripts/audit/graph_audit.py. Check |
| scripts/research/emit_batch_sql.py | 455 | search_admissions, source_locators | scripts/research/emit_batch_sql.py — capture a research batch out of a scratch DB. DR-2026-08-19 §12.0 (F3). The research write path is a session-scoped scratch copy of the database: `db.py` writes to it under GUIDEBOOK_DB_PATH, so every wr |
| scripts/research/retrieval_log.py | 2261 | search_candidates, search_execution_artefacts, source_locators | scripts/research/retrieval_log.py — persist what was actually retrieved. WHY --- On 2026-08-19 the first research batch after the restart wrote FABRICATED author lists onto all five of its admissions, and stamped them `verification_status=' |

## Tests naming this stage's tables (5)
`scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_db_integrity.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_scan_contract.py`, `scripts/tests/test_search_log_completeness.py`

## Registry checks whose PRIMARY stage (by tables read) is `research` (13)

| check id | battery | level | basis |
|---|---|---|---|
| test_db_integrity | db_integrity | blocking | unattributed |
| provenance_artefact_audit | research | blocking | evidence/discovery-provenance |
| provenance_attribution_audit | research | advisory | evidence/discovery-provenance |
| author_fidelity | research | advisory | DR-2026-08-19 §7 adversarial pass, lens L1 (2026-08-19) |
| research_contract_baseline_ratchet | research | blocking | hygiene |
| research_dod_selftest | research | blocking | unattributed |
| research_dod | research | advisory | unattributed |
| research_dod_session | research | blocking | unattributed |
| search_log_completeness | research | advisory | evidence/discovery-provenance |
| test_search_log_completeness | tests | advisory | hygiene |
| research_protocol_audit | research | advisory | research/adversarial-fields-complete |
| test_run_pipeline_refusals | tests | advisory | hygiene |
| derived_not_curated_audit | schema | blocking | base/base-derived-not-curated |

## Skills naming this stage's tables (8)
`bibliography-compiler`, `citation-miner`, `economics-researcher`, `functional-deficit-researcher`, `gap-driven-mining`, `multilingual-research`, `research-log-manager`, `run-pipeline`

## Prose homes for this stage
- `governance/pipeline-operations.md`
- `governance/research-contract.yaml`
- `governance/mining-screens.yaml`
- `governance/evidence-methodology.md`