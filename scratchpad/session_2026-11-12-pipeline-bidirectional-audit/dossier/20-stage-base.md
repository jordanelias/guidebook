# 20 — Stage `base`

_Generated 2026-11-12 02:01 UTC at commit e73b588, schema user_version 125. Every figure here is computed by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_dossier.py`; re-run it, do not trust this text (CLAUDE.md rule 7a)._


**Contract anchor:** the vocabulary and registry layer every stage points into (D-0167, owner ruling 2026-08-27: "it supplies the base information upon which research can perform its task... it's the first layer of information")

**Contract entry condition(s):** a vocabulary, registry or crossing map the downstream stages resolve codes against

## Tables (18)

| table | rows | columns |
|---|---|---|
| access_duration | 3 | code, definition, created_at, created_by_session |
| access_need_icf | 43 | need_code, icf_code, icf_type, confidence, notes, created_at, created_by_session |
| access_needs | 17 | need_code, family, design_obligation, absorbs, typical_stakes, source_version, notes, created_at, created_by_session |
| access_stakes | 3 | code, definition, created_at, created_by_session |
| base_icf | 72 | icf_code, component, is_range, title, title_source, notes, created_at, created_by_session |
| base_parameters | 10 | parameter_id, term_id, status, merged_into, notes, created_at, created_by_session, updated_at, updated_by_session, direction_rationale, accessibility_direction, direction_ref_id |
| base_taxonomy_identity | 23 | identity_code, display_name, category, description, parent_code, is_compound, status, created_at, updated_at |
| base_taxonomy_medical | 0 | medical_code, display_name, description, status, notes, created_at, created_by_session, icd11_anchors, icd11_verified_at |
| icf_medical_map | 0 | icf_code, medical_code, role, mapping_confidence, notes, created_at, created_by_session |
| identity_icf_map | 61 | link_id, identity_code, icf_code, mechanism, mapping_confidence, provenance, notes, created_at, created_by_session |
| identity_medical_map | 0 | identity_code, medical_code, relationship, notes, created_at, created_by_session |
| lang_jur_map | 70 | language, jurisdiction, role, notes, created_at, created_by_session, scope_status |
| life_stage_modifiers | 2 | code, label, definition, created_at, created_by_session |
| parameter_declinations | 1 | term_id, reason, created_at, created_by_session, revoked_at, revoked_by_session, revocation_reason |
| rooms | 17 | room_code, name, category, description, status, notes, created_at, created_by_session, updated_at, updated_by_session |
| slugs | 106 | slug, topic_directory, sl_path, bpc_path, status, merged_into, created_at, created_by_session, updated_at, updated_by_session |
| term_aliases | 2382 | term_id, alias, language, alias_type, jurisdiction, notes, created_at, created_by_session, updated_at, updated_by_session, observation_id |
| terms | 94 | term_id, canonical_en, definition, domain, scope_note, created_at, created_by_session, updated_at, updated_by_session, catalogue, catalogue_entry_ref, catalogue_approval_ref |

## Views touching this stage (9)

| view | all stages spanned |
|---|---|
| v_code_floor_only | base, specification |
| v_coverage_priority | base, research |
| v_determination_provenance | base, evidence, judgment, specification |
| v_item_provenance | base, evidence, specification |
| v_research_scope | base |
| v_scan_ledger | base, evidence, judgment |
| v_source_reach_all | base, evidence, specification |
| v_unregistered_roots | base, evidence, judgment |
| v_value_independence | base, evidence, judgment |

## Contract criteria

| id | kind | check | criterion (first 200 chars) |
|---|---|---|---|
| base-schema-validates | integrity | scripts/validate_schema.py | Every base vocabulary validates against its declared schema and its own CHECK constraints. |
| base-names-resolve | integrity | scripts/audit/schema_reference_audit.py | Every table and view named by an executable or instructional caller -- scripts, tools, schemas, governance YAML, skills -- exists in the live schema. |
| base-medical-lens-offered-not-adopted | integrity | scripts/audit/medical_lens_integrity.py | Every medical-lens row carries an MD- code with no digit, states no determination in its own display_name or description, and is crossed to at least one other lens. A row nothing crosses to is a dead  |
| base-jurisdiction-vocabulary | integrity | scripts/validate_jurisdiction.py | Every jurisdiction value resolves to the declared vocabulary. |
| base-parameter-vocabulary | completeness | scripts/validate_parameters.py | No base_parameters row points at a terms.canonical_en that itself states a determination (a digit, a comparator, or a min/max word). |
| base-derived-not-curated | integrity | scripts/audit/derived_not_curated_audit.py | A vocabulary, an ordering, an identifier or a set that the schema or the code can compute is never also maintained as a list beside it. The list and the thing drift, and only the list is read. Mechani |
| base-identifier-never-reissued | integrity | scripts/audit/identifier_floor_audit.py | An identifier the permanent record has already used is spent, whatever the live tables say. ref_id is computed as MAX+1 over the live tables (dbcore.ref_id_high_water) and parameter_id/specification_i |
| base-retired-vocabulary-not-taught | integrity | scripts/audit/retired_vocabulary_audit.py | No retired base token survives in live prose, skills or code outside the exempt paths. |
| base-direction-from-source | integrity | **NONE (unenforced)** | A parameter's accessibility direction is recorded from an admitted source that holds an extraction for the parameter (base_parameters.direction_ref_id, migration 122), never hand-set. Held by the writ |

## `db.py` verbs that WRITE this stage's tables (16)

| verb | writes | reads | help |
|---|---|---|---|
| add-alias | term_aliases | evidence_sources, observed_terms, term_adjudications, terms | Record a SOURCE-ATTESTED alias from an adjudicated |
| add-icf-code | base_icf |  | Mint one ICF code into base_icf — the registry the ICF lens points at |
| add-medical | base_taxonomy_medical, icf_medical_map, identity_medical_map | base_icf, base_taxonomy_identity, specifications, terms | Mint a medical-lens row and at least one crossing |
| add-parameter | base_parameters | parameter_declinations, specifications, term_adjudications, terms | Promote an adjudicated term into base_parameters |
| add-population-icf-link | identity_icf_map | base_icf, base_taxonomy_identity | Map a population to an ICF activity it has a functional deficit in (H3 |
| add-term | term_adjudications, terms | observed_terms, term_aliases | Mint a term for a NEW concept and adjudicate it NAMES-NEW |
| amend-term | terms | term_aliases | Replace a term's definition or scope_note, recording the |
| annotate-parameter | base_parameters | terms | Append a dated, attributed line to a parameter's notes |
| decline-parameter | parameter_declinations | base_parameters, terms | Record that a term is NOT a design parameter, and why |
| merge-parameter | base_parameters | determination_gates, specifications, terms | Fold one parameter into another: status merged, |
| mint-term-from-catalogue | terms | term_aliases | Mint a term from a PERMITTED catalogue, pointing at the |
| rename-term | term_aliases, terms | observed_terms, term_adjudications | Correct a term's canonical name from an observation or an |
| retire-parameter | base_parameters | determination_gates, source_value_extractions, specifications, terms, v_scan_ledger, v_value_independence | Retire a parameter IN PLACE (status retired; reason |
| revoke-declination | parameter_declinations | decisions | Revoke a parameter declination (recorded on the row, |
| set-icf-title | base_icf |  | Name a seeded ICF code (GAP-ICF-TITLES); refuses to overwrite a title |
| set-parameter-direction | base_parameters | evidence_sources, source_value_extractions, terms | Record which way is better for a disabled person on this parameter |

## `db.py` verbs that only READ this stage's tables (18)

`add-candidate`, `add-case-study`, `add-conflict`, `add-connection`, `add-extraction`, `add-population-match`, `add-source`, `adjudicate-term`, `coverage`, `derive-extraction`, `link-source-slug`, `log-search`, `next-id`, `raise-determination-gate`, `reattribute-candidate`, `record-scan`, `resolve-candidate`, `unmined`

## Other code that WRITES this stage's tables (4)

| file | lines | writes | purpose (docstring) |
|---|---|---|---|
| scripts/audit/graph_audit.py | 483 | base_taxonomy_identity | graph_audit.py — vectorized structural audit (stdlib graph spine, data layer). Builds a derived, read-only audit graph from data/guidebook.db and runs Tier-1 topology checks over it, unifying orphan / dangling-reference / empty-table / stat |
| scripts/audit/migration_reproducibility.py | 618 | slugs | scripts/audit/migration_reproducibility.py — GAP-290 enforcement. Rebuilds a fresh DB from the migration history alone and compares core invariants against the committed data/guidebook.db. A divergence means someone wrote directly to the DB |
| scripts/audit/research_batch_dod.py | 1795 | base_parameters, parameter_declinations, term_aliases, terms | scripts/audit/research_batch_dod.py — RESEARCH BATCH DEFINITION-OF-DONE gate. **** RESEARCH IS INVALID IF IT IS NOT COMPLIANT WITH THIS PROJECT'S GOVERNANCE, **** **** VERIFICATION TOOLS, RULES AND ETHOS. (owner directive, 2026-07-24) ****  |
| scripts/assess/assess_cell.py | 2470 | slugs | scripts/assess/assess_cell.py — the determination engine (rule_version: `RULE_VERSION` below). THE STATE IS COMPUTED. Owner ruling 2026-09-09 (references/project-standards.md): *"you have to compute it. I can't handle this load manually."*  |

## Code that READS this stage's tables, writing none of them (20)

| file | lines | reads | purpose (docstring) |
|---|---|---|---|
| scripts/audit_evidence_metadata.py | 441 | slugs | Audit evidence metadata against PI v10.8 standing rule #10. Standing rule #10 (evidence verification gate): No BPC synthesis claim may cite a source with metadata_quality = AUTHOR-TITLE-ONLY or verification_status = NULL. Required minimum:  |
| scripts/dbcore.py | 1385 | base_parameters, base_taxonomy_medical, lang_jur_map, terms | scripts/dbcore.py — the one place this repository opens, stamps and keys the database. WHY THIS EXISTS. Measured 2026-08-25: 104 raw `sqlite3.connect(` call sites across 55 live files, 48 independent resolutions of GUIDEBOOK_DB_PATH, and 37 |
| scripts/validate_cross_refs.py | 354 | slugs | validate_cross_refs.py — Cross-reference integrity validator. Checks: 1. Slug references resolve via SQLite slugs table (was: slug-registry.md) 2. CON-IDs (CON-NNNN) resolve via SQLite connections table (was: _index.md) 3. Part section refe |
| scripts/validate_parameters.py | 140 | base_parameters, terms | scripts/validate_parameters.py — CI validator for the design-parameter registry (`base_parameters` pointing at `terms`). WHAT WRONG THING REACHES THE GUIDEBOOK IF THIS DOES NOT EXIST (CLAUDE.md §8): a parameter whose name states its own ans |
| scripts/validate_schema.py | 344 | slugs | scripts/validate_schema.py — Validate entity YAML files against Pydantic schemas. Walks data/ directories and validates each YAML file against the appropriate schema model. Used by CI (schema job) and session start (--quick mode). Usage: py |
| scripts/audit/adherence_log_audit.py | 628 | slugs | adherence_log_audit.py — Level 2 audit for attestation files. Checks performed (per PI v10.12 rule #11): 0. Attestation presence. For every synthesis-path file in the changeset, verify a corresponding `attestations/<slug>.json` is either al |
| scripts/audit/adversarial_pass_audit.py | 172 | slugs | scripts/audit/adversarial_pass_audit.py — the pass exists for what this session wrote. WHY THIS EXISTS. Three canonical statements already require an adversarial pass on every research/synthesis diff (the 2026-08-19 RULE; DR-2026-09-11 clau |
| scripts/audit/alias_provenance_audit.py | 171 | lang_jur_map, term_aliases, terms | scripts/audit/alias_provenance_audit.py — provenance + verification surface for the controlled vocabulary (terms / term_aliases). Why this exists. `term_aliases` drives multilingual retrieval via the (now deleted) query generator, but nothi |
| scripts/audit/citation_mining_completeness.py | 376 | slugs | scripts/audit/citation_mining_completeness.py Audit citation_mining completeness. Surfaces the GAP-283 protocol-violation pattern: research sessions adding Tier 1-2 evidence_sources rows without corresponding citation_mining rows (per stand |
| scripts/audit/derivation_handshake_integrity.py | 272 | identity_icf_map | scripts/audit/derivation_handshake_integrity.py — the handshake, checked on the rows. WHAT WRONG THING REACHES THE *GUIDEBOOK* IF THIS DOES NOT EXIST (CLAUDE.md §8's bar, which is about the book and not the apparatus): 1. A `stated` determi |
| scripts/audit/derived_not_curated_audit.py | 475 | terms | scripts/audit/derived_not_curated_audit.py — CLAUDE.md rule 8, mechanised. THE RULE: derive it, or name who judged it. Never curate a fact the machine can compute. WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS. A curated list and the  |
| scripts/audit/identifier_floor_audit.py | 158 | base_parameters | scripts/audit/identifier_floor_audit.py — an identifier is never reissued. WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS (CLAUDE.md section 1's burden of proof). A source's `ref_id` is how every record outside the database names it: r |
| scripts/audit/jurisdiction_db_vocabulary.py | 146 | lang_jur_map, term_aliases | scripts/audit/jurisdiction_db_vocabulary.py — jurisdiction codes IN THE DATABASE. WHY THIS EXISTS. `governance/jurisdiction-philosophy.md` states the UK/GB rule at ERROR level -- "GB appearing as a jurisdiction code is rejected; must be UK" |
| scripts/audit/medical_lens_integrity.py | 119 | base_taxonomy_medical, icf_medical_map, identity_medical_map | scripts/audit/medical_lens_integrity.py — the fourth lens cannot become the frame. WHAT WRONG THING REACHES THE *GUIDEBOOK* IF THIS DOES NOT EXIST (CLAUDE.md §8's bar for adding a check, which is about the book and not the apparatus): 1. A  |
| scripts/audit/scan_debt.py | 117 | base_parameters, terms | scripts/audit/scan_debt.py — which (source, parameter) pairs nobody has read in full? WHY THIS EXISTS (tooling T1, 2026-10-09; catalogue-plan-v2 sections 3.8 and 8.2). The owner's requirement: "Ensure that we can add and expand parameter ca |
| scripts/audit/skill_vocabulary_audit.py | 215 | access_needs, base_icf, base_taxonomy_identity, slugs, terms | scripts/audit/skill_vocabulary_audit.py — every value a skill names must have a home. WHY THIS EXISTS (CLAUDE.md rule 8; owner 2026-11-06: "ensure all terminologies and vocabularies are correct"). A skill is a prose caller: it tells an oper |
| scripts/audit/verified_scan_integrity.py | 108 | base_parameters | scripts/audit/verified_scan_integrity.py — does every live extraction rest on a verified source and a reading? WHY THIS EXISTS (CLAUDE.md section 8: what wrong thing reaches the guidebook). OR-11a (owner, 2026-10-29): `extraction_status = ' |
| scripts/audit/graph/extract_db.py | 157 | base_taxonomy_identity, slugs, term_aliases, terms | scripts/audit/graph/extract_db.py — DB introspection layer (Tier 0, data). Reads data/guidebook.db READ-ONLY and materialises it into the audit graph: - one db_table node per table (with row_count), - one entity node per row of each primary |
| scripts/audit/graph/topology.py | 259 | base_taxonomy_identity, lang_jur_map, slugs | scripts/audit/graph/topology.py — Tier 1 graph-topology checks (stdlib only). Each check appends rows to the findings table. Severity is raw here; known-debt suppression and the pass/fail decision live in scripts/audit/graph_audit.py. Check |
| scripts/research/mining_screen.py | 258 | terms | Derive a citation-mining yield from a persisted payload and a NAMED screen. CLAUDE.md rule 7a: a number is written as the command that computes it. A mining yield is a number, and until 2026-09-18 it was produced by a regex typed into a she |

## Tests naming this stage's tables (8)
`scripts/tests/test_assess_cell_pilot.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_db_integrity.py`, `scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_scan_contract.py`, `scripts/tests/test_search_log_completeness.py`, `scripts/tests/test_validate_evidence_state_2_4.py`

## Registry checks whose PRIMARY stage (by tables read) is `base` (16)

| check id | battery | level | basis |
|---|---|---|---|
| validate_cross_refs | structure | blocking | hygiene |
| validate_parameters | data | advisory | base/base-parameter-vocabulary |
| alias_provenance_audit | data | blocking | unattributed |
| scan_debt | data | advisory | unattributed |
| jurisdiction_db_vocabulary | schema | blocking | base/base-jurisdiction-vocabulary |
| skill_vocabulary_audit | governance | advisory | base/base-derived-not-curated |
| attestation_presence | attestation | blocking | cross_stage/adherence-log |
| attestation_schema | attestation | blocking | cross_stage/adherence-log |
| attestation_evidence | attestation | advisory | cross_stage/adherence-log |
| attestation_verdict | attestation | informational | cross_stage/adherence-log |
| adversarial_pass_recorded | research | advisory | cross_stage/definition-of-done |
| test_db_amend_writers | tests | advisory | hygiene |
| test_scan_contract | tests | advisory | hygiene |
| test_evidence_cell_state_2_3 | tests | advisory | hygiene |
| test_validate_evidence_state_2_4 | tests | advisory | hygiene |
| medical_lens_integrity | schema | advisory | base/base-medical-lens-offered-not-adopted |

## Skills naming this stage's tables (14)
`bibliography-compiler`, `citation-miner`, `citation-verifier`, `connection-discovery`, `content-gap-analyzer`, `cross-population-conflict-mapper`, `economics-researcher`, `functional-deficit-researcher`, `gap-driven-mining`, `multilingual-research`, `prose-style-checker`, `research-log-manager`, `run-pipeline`, `supersession-audit`

## Prose homes for this stage
- `governance/population-taxonomy.md`
- `governance/functional-taxonomy.md`
- `governance/jurisdiction-philosophy.md`
- `governance/retired-vocabulary.yaml`
- `governance/grounds.md`