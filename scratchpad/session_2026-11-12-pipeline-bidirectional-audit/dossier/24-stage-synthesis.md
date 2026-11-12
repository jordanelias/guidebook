# 24 — Stage `synthesis`

_Generated 2026-11-12 02:01 UTC at commit e73b588, schema user_version 125. Every figure here is computed by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_dossier.py`; re-run it, do not trust this text (CLAUDE.md rule 7a)._


**Contract anchor:** best_practice_synthesis / ISW; PI rule #9 (9-step); Opus-only (rule #2)

**Contract entry condition(s):** a determination with a resolved value, ready for cross-jurisdictional synthesis

## Tables (8)

| table | rows | columns |
|---|---|---|
| conflicts | 0 | conflict_id, domain, pop_a, pop_b, status, resolution, evidence, gap_id, source_skill, created_at, created_by_session, updated_at, updated_by_session, parameter_id |
| connection_targets | 0 | target_id, con_id, parameter_id, slug, identity_code, extraction_id, methodology |
| connections | 0 | con_id, status, confidence, connection_type, filed_in, description, source_skill, opus_reviewed, created_at, created_by_session, updated_at, updated_by_session |
| convergence_assessment | 5 | convergence_id, status, clinical_sources, co1_sources, co2_sources, down_weighted_sources, discounted_sources, rationale, synthesis_approach, created_at, created_by_session, updated_at, updated_by_session |
| convergence_sources | 69 | convergence_id, ref_id, role, created_at, created_by_session |
| gaps | 110 | gap_id, category, priority, status, skill, section, description, created_at, created_by_session, updated_at, updated_by_session, falsification_condition, confidence_interval, shift_conditions, named_dissenter, mining_addressability |
| reasoning_doc_citations | 0 | citation_id, reasoning_doc_slug, parameter, jurisdiction, population, claim_type, claimed_value, claimed_unit, claim_text, source_ref_id, source_section, value_match, claim_match, verified_at, created_by_session, paywall_purchase_candidate, notes, setting, locator_scheme, loc_division, loc_part, loc_section, loc_subsection, loc_paragraph, loc_clause, loc_subclause, loc_division_end, loc_part_end, loc_section_end, loc_subsection_end, loc_paragraph_end, loc_clause_end, loc_subclause_end, loc_note |
| supersession_check | 0 | check_id, slug, local_ref_id, ref_id, anchor_tier, anchor_evidence_type, outcome, superseding_ref_ids, superseding_dois, refinement_dimension, divergence_notes, search_strategy_record, candidates_returned, candidates_reviewed, created_at, created_by_session, check_method, notes |

## Views touching this stage (3)

| view | all stages spanned |
|---|---|
| v_convergence_sources | evidence, synthesis |
| v_divergence | specification, synthesis |
| v_pending | specification, synthesis |

## Contract criteria

| id | kind | check | criterion (first 200 chars) |
|---|---|---|---|
| opus-routing | completeness | **NONE (unenforced)** | best_practice_synthesis is authored at the ratified capability floor (Opus-class), never by a lower tier (rule #2). |

## `db.py` verbs that WRITE this stage's tables (10)

| verb | writes | reads | help |
|---|---|---|---|
| add-conflict | conflicts | base_parameters, base_taxonomy_identity, decisions | Insert a conflict record |
| add-connection | connection_targets, connections | base_parameters | Insert a new connection record |
| add-gap | gaps |  | Insert a new gap record |
| add-supersession-check | supersession_check |  | Record a per-anchor-source supersession outcome (DR-2026-05-24 |
| amend-gap | gaps |  | APPEND a dated correction to a gap's description |
| close-gap | gaps |  | Close a gap record |
| delete-connection | connection_targets, connections |  | Hard-delete a connection by CON-ID (data corrections only |
| update-conflict | conflicts |  | Update a conflict record |
| update-connection | connections |  | Update connection status |
| update-gap-addressability | gaps |  | Set gaps.mining_addressability per DR-2026-05-26 |

## `db.py` verbs that only READ this stage's tables (6)

`conflicts`, `connections`, `gaps`, `log-mining`, `next-id`, `unmined-gaps`

## Other code that WRITES this stage's tables (3)

| file | lines | writes | purpose (docstring) |
|---|---|---|---|
| scripts/emit_data_migration.py | 783 | gaps | scripts/emit_data_migration.py — create a properly-named data-migration file. Per GAP-290 resolution. The migration system (scripts/migrate_db.py) requires data migrations to be named: scripts/migrations/data_{YYYYMMDDHHMMSS}_{session-slug} |
| scripts/audit/graph_audit.py | 483 | connection_targets, connections | graph_audit.py — vectorized structural audit (stdlib graph spine, data layer). Builds a derived, read-only audit graph from data/guidebook.db and runs Tier-1 topology checks over it, unifying orphan / dangling-reference / empty-table / stat |
| scripts/assess/assess_cell.py | 2470 | convergence_assessment, convergence_sources, gaps | scripts/assess/assess_cell.py — the determination engine (rule_version: `RULE_VERSION` below). THE STATE IS COMPUTED. Owner ruling 2026-09-09 (references/project-standards.md): *"you have to compute it. I can't handle this load manually."*  |

## Code that READS this stage's tables, writing none of them (18)

| file | lines | reads | purpose (docstring) |
|---|---|---|---|
| scripts/dbcore.py | 1385 | conflicts, connection_targets, connections, convergence_sources, gaps, supersession_check | scripts/dbcore.py — the one place this repository opens, stamps and keys the database. WHY THIS EXISTS. Measured 2026-08-25: 104 raw `sqlite3.connect(` call sites across 55 live files, 48 independent resolutions of GUIDEBOOK_DB_PATH, and 37 |
| scripts/validate_cross_refs.py | 354 | connections | validate_cross_refs.py — Cross-reference integrity validator. Checks: 1. Slug references resolve via SQLite slugs table (was: slug-registry.md) 2. CON-IDs (CON-NNNN) resolve via SQLite connections table (was: _index.md) 3. Part section refe |
| scripts/validate_evidence_state.py | 554 | convergence_assessment, convergence_sources, gaps | scripts/validate_evidence_state.py — Validate evidence state records. Per governance/evidence-methodology.md (A6), §2 (cell states), §3 (convergence), and §1.4/§1.6/§1.7 (scale + directness); decision D-D. Stage 2.4 wires this to the real D |
| scripts/validate_schema.py | 344 | connections, gaps | scripts/validate_schema.py — Validate entity YAML files against Pydantic schemas. Walks data/ directories and validates each YAML file against the appropriate schema model. Used by CI (schema job) and session start (--quick mode). Usage: py |
| scripts/audit/adherence_log_audit.py | 628 | reasoning_doc_citations | adherence_log_audit.py — Level 2 audit for attestation files. Checks performed (per PI v10.12 rule #11): 0. Attestation presence. For every synthesis-path file in the changeset, verify a corresponding `attestations/<slug>.json` is either al |
| scripts/audit/adjudication_integrity.py | 185 | convergence_assessment | adjudication_integrity.py — audit the evidence-adjudication substrate. Adds the one mechanical adjudication check that is specified-but-unbuilt — the Stage-2.5 tier-derivation consistency sweep that schemas/tier_derivation.py's own docstrin |
| scripts/audit/adversarial_pass_audit.py | 172 | connection_targets | scripts/audit/adversarial_pass_audit.py — the pass exists for what this session wrote. WHY THIS EXISTS. Three canonical statements already require an adversarial pass on every research/synthesis diff (the 2026-08-19 RULE; DR-2026-09-11 clau |
| scripts/audit/derived_not_curated_audit.py | 475 | supersession_check | scripts/audit/derived_not_curated_audit.py — CLAUDE.md rule 8, mechanised. THE RULE: derive it, or name who judged it. Never curate a fact the machine can compute. WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS. A curated list and the  |
| scripts/audit/gap_mining_audit.py | 261 | gaps, supersession_check | Audit query for gap-driven mining protocol compliance (DR-2026-05-26). Flags: 1. Closed gaps lacking gap_mining row when description signals mining-addressability (an OPEN-ADDRESSABLE gap moved to CLOSED-FIXED with no gap_mining attempt rec |
| scripts/audit/migration_reproducibility.py | 618 | connections, gaps | scripts/audit/migration_reproducibility.py — GAP-290 enforcement. Rebuilds a fresh DB from the migration history alone and compares core invariants against the committed data/guidebook.db. A divergence means someone wrote directly to the DB |
| scripts/audit/pipeline_contract_audit.py | 293 | gaps | pipeline_contract_audit.py — validate the governance pipeline contract. The pipeline contract (governance/pipeline-contract.yaml, PROPOSED per DR-2026-07-13-pipeline-contract) declares, per pipeline stage, the integrity + completeness crite |
| scripts/audit/research_batch_dod.py | 1795 | gaps | scripts/audit/research_batch_dod.py — RESEARCH BATCH DEFINITION-OF-DONE gate. **** RESEARCH IS INVALID IF IT IS NOT COMPLIANT WITH THIS PROJECT'S GOVERNANCE, **** **** VERIFICATION TOOLS, RULES AND ETHOS. (owner directive, 2026-07-24) ****  |
| scripts/audit/research_protocol_audit.py | 322 | gaps | Audit query for adversarial research protocol compliance. Flags: 1. Closed gaps lacking required protocol fields 2. Verified citations without population match records 3. Population match grade distribution suspicious (>70% EXACT) 4. Confid |
| scripts/audit/skill_vocabulary_audit.py | 215 | gaps | scripts/audit/skill_vocabulary_audit.py — every value a skill names must have a home. WHY THIS EXISTS (CLAUDE.md rule 8; owner 2026-11-06: "ensure all terminologies and vocabularies are correct"). A skill is a prose caller: it tells an oper |
| scripts/audit/graph/extract_db.py | 157 | conflicts, connection_targets, connections, convergence_assessment, gaps | scripts/audit/graph/extract_db.py — DB introspection layer (Tier 0, data). Reads data/guidebook.db READ-ONLY and materialises it into the audit graph: - one db_table node per table (with row_count), - one entity node per row of each primary |
| scripts/audit/graph/topology.py | 259 | conflicts, connections, convergence_assessment, gaps, reasoning_doc_citations | scripts/audit/graph/topology.py — Tier 1 graph-topology checks (stdlib only). Each check appends rows to the findings table. Severity is raw here; known-debt suppression and the pass/fail decision live in scripts/audit/graph_audit.py. Check |
| scripts/research/emit_batch_sql.py | 455 | gaps | scripts/research/emit_batch_sql.py — capture a research batch out of a scratch DB. DR-2026-08-19 §12.0 (F3). The research write path is a session-scoped scratch copy of the database: `db.py` writes to it under GUIDEBOOK_DB_PATH, so every wr |
| scripts/research/retrieval_log.py | 2261 | connections, gaps | scripts/research/retrieval_log.py — persist what was actually retrieved. WHY --- On 2026-08-19 the first research batch after the restart wrote FABRICATED author lists onto all five of its admissions, and stamped them `verification_status=' |

## Tests naming this stage's tables (5)
`scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_db_integrity.py`, `scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_validate_evidence_state_2_4.py`

## Registry checks whose PRIMARY stage (by tables read) is `synthesis` (6)

| check id | battery | level | basis |
|---|---|---|---|
| validate_schema_cross_check | schema | advisory | base/base-schema-validates |
| validate_evidence_state | schema | blocking | ['specification/governing-refs-nonempty', 'specification/no-regulatory-stratum-stated', 'specification/tier3-alone-threshold'] |
| pipeline_contract_audit | governance | advisory | unattributed |
| gap_mining_audit | research | advisory | unattributed |
| graph_audit | research | advisory | unattributed |
| adjudication_integrity | schema | blocking | unattributed |

## Skills naming this stage's tables (15)
`connection-discovery`, `content-gap-analyzer`, `cross-population-conflict-mapper`, `economics-researcher`, `evidence-auditor`, `find-and-replace`, `functional-deficit-researcher`, `gap-driven-mining`, `github-io`, `multilingual-research`, `research-log-manager`, `run-pipeline`, `session-consolidator`, `supersession-audit`, `toc-editor`

## Prose homes for this stage
- `governance/evidence-architecture.md`
- `governance/held-tensions.md`