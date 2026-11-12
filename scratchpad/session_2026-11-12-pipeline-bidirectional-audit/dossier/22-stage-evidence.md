# 22 — Stage `evidence`

_Generated 2026-11-12 02:01 UTC at commit e73b588, schema user_version 125. Every figure here is computed by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_dossier.py`; re-run it, do not trust this text (CLAUDE.md rule 7a)._


**Contract anchor:** EvidenceSource corpus (ENT-02); PI rule #2 (Sonnet evidence inventories)

**Contract entry condition(s):** sources discovered for the topic/slug under research

## Tables (8)

| table | rows | columns |
|---|---|---|
| case_studies | 0 | case_study_id, slug, title, building_type, location, architect, year, setting, population_description, evidence_quality_tier, cost_data, cost_data_quality, part_section, limitations, harm_finding, status, notes, created_at, created_by_session, updated_at, updated_by_session, design_intent, populations_served_note, outcome_data, conflict_documented, failure_notes, construction_cost, accessible_design_premium, funding_sources, operational_cost_change, remediation_cost, roi_data, financial_evidence_tier, financial_data_quality, evidence_contribution, part13_status, sources |
| economics_entries | 1 | entry_id, pillar, entry_type, source, ref_id, jurisdiction, finding, study_design, sample, value_numeric, value_unit, currency, bcr, evidence_tier, confidence, source_section, quant_status, year, journal, status, notes, created_at, created_by_session, updated_at, updated_by_session |
| evidence_source_authors | 142 | id, ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session, corporate_name_note |
| evidence_sources | 59 | ref_id, source_type, author_count, author_count_is_complete, first_author_last, first_author_first, is_corporate_primary, author_display, pub_year, pub_year_note, pub_title, pub_subtitle, chapter_title, original_title, lang_detected, lang_detection_method, pub_title_en, pub_subtitle_en, chapter_title_en, journal_name_en, translation_method, translation_reviewed, journal_name, journal_abbrev, volume, issue, pages_start, pages_end, article_number, publisher, publisher_location, edition, book_title, series, series_number, report_number, institution, standard_number, doi, pmid, pmcid, isbn, issn, url, url_accessed, handle, local_id, tier, evidence_type, jurisdiction, co1_provenance, co1_source_type, synthesis_attribution_required, metadata_quality, verification_status, doi_resolution_outcome, bpc_shorthand, bpc_note, grey_flag, grey_reason, verification_note, prior_expectation, search_queries_used, derivation_chain, notes, created_at, created_by_session, updated_at, updated_by_session, verified_by_tool, last_verified_at, verification_attempt_count, superseded_by_ref_id, pages, pub_month, language, subtype, citation_count, url_resolution_outcome, url_last_fetched, url_match_similarity, metadata_integrity_status, metadata_integrity_detail, code_currency_status, code_currency_verified_at, code_currency_verified_by_session, code_currency_notes, scope, data_capture_status, citation_mining_status, processing_blocked_reason, standard_number_note, author_display_note, publisher_note, verification_disposition, verification_method, verification_closure_reason |
| external_root_registry | 0 | root_id, description, root_type, provenance, root_population_note, notes, created_at, created_by_session |
| observed_terms | 96 | observation_id, ref_id, surface_form, language, locator, context_quote, notes, created_at, created_by_session, updated_at, updated_by_session |
| source_scans | 18 | scan_id, ref_id, mode, catalogue_version, target_parameter_id, text_scope, pages_read, pages_total, file_sha256, open_pass_done, method, notes, created_at, created_by_session, updated_at, updated_by_session |
| source_slug_links | 71 | ref_id, slug, local_ref_id, created_at, created_by_session, updated_at, updated_by_session, relevance_note |

## Views touching this stage (10)

| view | all stages spanned |
|---|---|
| v_convergence_sources | evidence, synthesis |
| v_determination_provenance | base, evidence, judgment, specification |
| v_evidence_authors | evidence |
| v_item_provenance | base, evidence, specification |
| v_registry_duplicate_descriptions | evidence |
| v_scan_ledger | base, evidence, judgment |
| v_source_admission | evidence, research |
| v_source_reach_all | base, evidence, specification |
| v_unregistered_roots | base, evidence, judgment |
| v_value_independence | base, evidence, judgment |

## Contract criteria

| id | kind | check | criterion (first 200 chars) |
|---|---|---|---|
| evidence-verification-gate | integrity | scripts/audit/metadata_integrity_audit.py | No BPC synthesis claim cites a source with metadata_quality=AUTHOR-TITLE-ONLY or verification_status NULL (rule #10 existence gate). |
| discovery-provenance | completeness | scripts/audit/provenance_artefact_audit.py | Each candidate is checked against the bytes of the payload(s) its search actually returned, not merely against a typed exec_id that a batch can point anywhere (RC1, DR-2026-09-26-recurring-defect-shap |

## `db.py` verbs that WRITE this stage's tables (10)

| verb | writes | reads | help |
|---|---|---|---|
| add-case-study | case_studies | evidence_sources, slugs | Record a Part-12 case study |
| add-economics-entry | economics_entries | evidence_sources | Record a Part-13 economics finding |
| add-source | evidence_source_authors, evidence_sources, source_slug_links | base_parameters, citation_mining, observed_terms, slugs, source_locators, term_adjudications, terms, v_evidence_authors, v_scan_ledger | Insert an evidence source |
| amend-source | evidence_sources |  | Correct a JUDGEMENT field on an evidence row, recording what was replaced |
| correct-source | evidence_source_authors, evidence_sources |  | Rewrite bibliographic fields FROM THE LOGGED PAYLOAD |
| link-source-slug | source_slug_links | evidence_sources, slugs | Cross-file an ADMITTED source to an ADDITIONAL slug (R9 |
| log-mining | citation_mining, evidence_sources | connections, search_candidates, search_executions, source_locators, source_slug_links | Log citation mining |
| observe-term | observed_terms | evidence_sources | Record that a source USES a phrase (evidence stage, D-0173 |
| record-scan | source_scans | base_parameters, evidence_sources, v_scan_ledger | Record one READING of a source against the parameter list (source_scans); |
| supersede-source | evidence_sources | v_convergence_sources, v_determination_provenance, v_evidence_authors, v_item_provenance, v_source_admission, v_source_reach_all | Mark an admitted source SUPERSEDED BY another (a mirror, a DOI-less |

## `db.py` verbs that only READ this stage's tables (18)

`add-alias`, `add-extraction`, `add-locator`, `add-population-match`, `add-term`, `adjudicate-term`, `amend-extraction`, `amend-search`, `derive-extraction`, `is-mined`, `link-admission`, `log-search`, `raise-determination-gate`, `rename-term`, `resolve-candidate`, `set-parameter-direction`, `unmined`, `update-locator`

## Other code that WRITES this stage's tables (5)

| file | lines | writes | purpose (docstring) |
|---|---|---|---|
| scripts/dbcore.py | 1385 | evidence_sources | scripts/dbcore.py — the one place this repository opens, stamps and keys the database. WHY THIS EXISTS. Measured 2026-08-25: 104 raw `sqlite3.connect(` call sites across 55 live files, 48 independent resolutions of GUIDEBOOK_DB_PATH, and 37 |
| scripts/emit_data_migration.py | 783 | evidence_sources | scripts/emit_data_migration.py — create a properly-named data-migration file. Per GAP-290 resolution. The migration system (scripts/migrate_db.py) requires data migrations to be named: scripts/migrations/data_{YYYYMMDDHHMMSS}_{session-slug} |
| scripts/validate_verification_consistency.py | 155 | evidence_sources | validate_verification_consistency.py — the has_unverified_sources truthfulness gate. Mechanizes a lesson from the 2026-07-24 Phase-B session: a determination cell can claim its sources are content-verified (has_unverified_sources=0) while t |
| scripts/audit/research_batch_dod.py | 1795 | evidence_sources, observed_terms, source_scans | scripts/audit/research_batch_dod.py — RESEARCH BATCH DEFINITION-OF-DONE gate. **** RESEARCH IS INVALID IF IT IS NOT COMPLIANT WITH THIS PROJECT'S GOVERNANCE, **** **** VERIFICATION TOOLS, RULES AND ETHOS. (owner directive, 2026-07-24) ****  |
| scripts/research/emit_batch_sql.py | 455 | evidence_sources, source_slug_links | scripts/research/emit_batch_sql.py — capture a research batch out of a scratch DB. DR-2026-08-19 §12.0 (F3). The research write path is a session-scoped scratch copy of the database: `db.py` writes to it under GUIDEBOOK_DB_PATH, so every wr |

## Code that READS this stage's tables, writing none of them (24)

| file | lines | reads | purpose (docstring) |
|---|---|---|---|
| scripts/audit_evidence_metadata.py | 441 | evidence_source_authors, evidence_sources, source_slug_links | Audit evidence metadata against PI v10.8 standing rule #10. Standing rule #10 (evidence verification gate): No BPC synthesis claim may cite a source with metadata_quality = AUTHOR-TITLE-ONLY or verification_status = NULL. Required minimum:  |
| scripts/run_checks.py | 1013 | evidence_sources | scripts/run_checks.py — the single entry point for every ecosystem check. Reads governance/check-registry.yaml, works out which checks the current change actually warrants, runs them, and reports. CI and scripts/preflight.sh both call this, |
| scripts/validate_evidence_state.py | 554 | evidence_sources | scripts/validate_evidence_state.py — Validate evidence state records. Per governance/evidence-methodology.md (A6), §2 (cell states), §3 (convergence), and §1.4/§1.6/§1.7 (scale + directness); decision D-D. Stage 2.4 wires this to the real D |
| scripts/audit/adjudication_integrity.py | 185 | evidence_sources | adjudication_integrity.py — audit the evidence-adjudication substrate. Adds the one mechanical adjudication check that is specified-but-unbuilt — the Stage-2.5 tier-derivation consistency sweep that schemas/tier_derivation.py's own docstrin |
| scripts/audit/citation_mining_completeness.py | 376 | evidence_source_authors, evidence_sources, source_slug_links | scripts/audit/citation_mining_completeness.py Audit citation_mining completeness. Surfaces the GAP-283 protocol-violation pattern: research sessions adding Tier 1-2 evidence_sources rows without corresponding citation_mining rows (per stand |
| scripts/audit/derivation_handshake_integrity.py | 272 | evidence_sources | scripts/audit/derivation_handshake_integrity.py — the handshake, checked on the rows. WHAT WRONG THING REACHES THE *GUIDEBOOK* IF THIS DOES NOT EXIST (CLAUDE.md §8's bar, which is about the book and not the apparatus): 1. A `stated` determi |
| scripts/audit/gap_mining_audit.py | 261 | evidence_sources | Audit query for gap-driven mining protocol compliance (DR-2026-05-26). Flags: 1. Closed gaps lacking gap_mining row when description signals mining-addressability (an OPEN-ADDRESSABLE gap moved to CLOSED-FIXED with no gap_mining attempt rec |
| scripts/audit/graph_audit.py | 483 | evidence_sources, source_slug_links | graph_audit.py — vectorized structural audit (stdlib graph spine, data layer). Builds a derived, read-only audit graph from data/guidebook.db and runs Tier-1 topology checks over it, unifying orphan / dangling-reference / empty-table / stat |
| scripts/audit/judgment_handoff_shape.py | 90 | evidence_sources | Pin the evidence -> judgment hand-off shape ruled 2026-08-27. WHAT WRONG THING REACHES THE GUIDEBOOK IF THIS DOES NOT EXIST (CLAUDE.md §1). The owner ruled evidence -> judgment is 1:N, with a worked example: "one evidence source may provide |
| scripts/audit/metadata_integrity_audit.py | 118 | evidence_sources | metadata_integrity_audit.py — Level 2 audit for DR-2026-05-20 protocol. Three checks: 1. Inconsistency: COMPLETE / COMPLETE-STATUTORY rows must not carry an open MISMATCH-* or DOI-* integrity status. If a row is upgraded to COMPLETE but the |
| scripts/audit/migration_reproducibility.py | 618 | evidence_source_authors, evidence_sources, source_slug_links | scripts/audit/migration_reproducibility.py — GAP-290 enforcement. Rebuilds a fresh DB from the migration history alone and compares core invariants against the committed data/guidebook.db. A divergence means someone wrote directly to the DB |
| scripts/audit/observation_verbatim_audit.py | 118 | observed_terms | scripts/audit/observation_verbatim_audit.py — is each observation's quote in its source? WHY THIS EXISTS (tooling T1, 2026-10-09; catalogue-plan-v2 section 8.2, critique F7). An observation records that a source USES a phrase, with the sent |
| scripts/audit/research_protocol_audit.py | 322 | evidence_sources | Audit query for adversarial research protocol compliance. Flags: 1. Closed gaps lacking required protocol fields 2. Verified citations without population match records 3. Population match grade distribution suspicious (>70% EXACT) 4. Confid |
| scripts/audit/scan_debt.py | 117 | source_scans | scripts/audit/scan_debt.py — which (source, parameter) pairs nobody has read in full? WHY THIS EXISTS (tooling T1, 2026-10-09; catalogue-plan-v2 sections 3.8 and 8.2). The owner's requirement: "Ensure that we can add and expand parameter ca |
| scripts/audit/skill_vocabulary_audit.py | 215 | source_slug_links | scripts/audit/skill_vocabulary_audit.py — every value a skill names must have a home. WHY THIS EXISTS (CLAUDE.md rule 8; owner 2026-11-06: "ensure all terminologies and vocabularies are correct"). A skill is a prose caller: it tells an oper |
| scripts/audit/source_slug_links_duplicates.py | 158 | evidence_source_authors, evidence_sources, source_slug_links | scripts/audit/source_slug_links_duplicates.py Audit source_slug_links for duplicate (slug, local_ref_id) pairs. Per GAP-285, source_slug_links lacks a UNIQUE(slug, local_ref_id) constraint, and duplicates have accumulated: - accessibility-f |
| scripts/audit/verified_scan_integrity.py | 108 | evidence_sources, source_scans | scripts/audit/verified_scan_integrity.py — does every live extraction rest on a verified source and a reading? WHY THIS EXISTS (CLAUDE.md section 8: what wrong thing reaches the guidebook). OR-11a (owner, 2026-10-29): `extraction_status = ' |
| scripts/audit/graph/extract_db.py | 157 | evidence_sources | scripts/audit/graph/extract_db.py — DB introspection layer (Tier 0, data). Reads data/guidebook.db READ-ONLY and materialises it into the audit graph: - one db_table node per table (with row_count), - one entity node per row of each primary |
| scripts/audit/graph/topology.py | 259 | evidence_sources, source_slug_links | scripts/audit/graph/topology.py — Tier 1 graph-topology checks (stdlib only). Each check appends rows to the findings table. Severity is raw here; known-debt suppression and the pass/fail decision live in scripts/audit/graph_audit.py. Check |
| scripts/research/full_text.py | 201 | evidence_sources | Derive the WHOLE text of a source's held PDF or web page, registered under its ref_id. WHY THIS EXISTS (catalogue-plan-v2 section 3.3 step 1; tooling T1, owner approval D8, 2026-10-09). The scan contract reads every admitted source against  |
| scripts/research/page_image.py | 162 | evidence_sources | Render a page of a persisted PDF to an image, so a session can LOOK at the scan. WHY THIS EXISTS, AND IT IS A DEFECT REPORT ON BATCH 19 RATHER THAN A FEATURE NOTE. Batch 19 mined REF-01005's bibliography out of a scanned 1979 microfiche. Th |
| scripts/research/retrieval_log.py | 2261 | evidence_source_authors, evidence_sources | scripts/research/retrieval_log.py — persist what was actually retrieved. WHY --- On 2026-08-19 the first research batch after the restart wrote FABRICATED author lists onto all five of its admissions, and stamped them `verification_status=' |
| scripts/generate/owner_browser_build.py | 135 | evidence_sources | scripts/generate/owner_browser_build.py -- build the owner's browser page. WHAT THIS IS. One HTML file that opens the guidebook database inside the viewer (sql.js, WebAssembly), so the owner can read every table, follow every pointer and se |
| scripts/assess/assess_cell.py | 2470 | evidence_sources, source_slug_links | scripts/assess/assess_cell.py — the determination engine (rule_version: `RULE_VERSION` below). THE STATE IS COMPUTED. Owner ruling 2026-09-09 (references/project-standards.md): *"you have to compute it. I can't handle this load manually."*  |

## Tests naming this stage's tables (6)
`scripts/tests/test_assess_cell_pilot.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_db_integrity.py`, `scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_scan_contract.py`

## Registry checks whose PRIMARY stage (by tables read) is `evidence` (10)

| check id | battery | level | basis |
|---|---|---|---|
| migration_reproducibility | data | blocking | cross_stage/reproducibility-invariant |
| migration_reproducibility_deep | data | advisory | cross_stage/reproducibility-invariant |
| source_slug_links_duplicates | data | blocking | unattributed |
| observation_verbatim_audit | data | advisory | unattributed |
| verified_scan_integrity | db_integrity | advisory | judgment/verified-reading |
| citation_mining_session | data | advisory | unattributed |
| citation_mining_backlog_t2 | data | informational | unattributed |
| audit_evidence_metadata | schema | advisory | unattributed |
| metadata_integrity_audit | research | advisory | evidence/evidence-verification-gate |
| judgment_handoff_shape | schema | blocking | judgment/handoff-fanout-preserved |

## Skills naming this stage's tables (11)
`bibliography-compiler`, `citation-miner`, `connection-discovery`, `economics-researcher`, `functional-deficit-researcher`, `gap-driven-mining`, `multilingual-research`, `research-log-manager`, `run-pipeline`, `session-consolidator`, `supersession-audit`

## Prose homes for this stage
- `governance/evidence-architecture.md`
- `governance/tier-system.md`
- `governance/co1-operational.md`
- `governance/evidence-methodology.md`