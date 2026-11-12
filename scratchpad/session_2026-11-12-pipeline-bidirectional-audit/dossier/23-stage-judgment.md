# 23 — Stage `judgment`

_Generated 2026-11-12 02:01 UTC at commit e73b588, schema user_version 125. Every figure here is computed by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_dossier.py`; re-run it, do not trust this text (CLAUDE.md rule 7a)._


**Contract anchor:** the 4-state determination machine + convergence + directness (evidence-architecture.md §5)

**Contract entry condition(s):** an admitted evidence source, ready for value extraction and a tier verdict

## Tables (5)

| table | rows | columns |
|---|---|---|
| evidence_population_match | 61 | match_id, source_ref, target_population, study_population, sample_size, match_grade, mismatch_note, created_at, created_by_session, ref_id, gap_id |
| extraction_follow_ups | 0 | follow_up_id, extraction_id, reason, warrant, raised_at, raised_by_session, resolved_at, resolved_by_session, resolution |
| extraction_relations | 57 | relation_id, from_extraction_id, relation, to_extraction_id, to_label, to_kind, stated, input_role, quote, notes, created_at, created_by_session |
| source_value_extractions | 214 | extraction_id, ref_id, slug, parameter_id, identity_code, icf_code, needs_code, medical_code, jurisdiction, setting, claim_type, claimed_value, claimed_unit, claim_text, source_section, root_id, root_type, root_ref_id, echo_of, measurement_paradigm, device_class, root_population_note, root_classification_basis, contested, file_anchor, locator_scheme, loc_division, loc_part, loc_section, loc_subsection, loc_paragraph, loc_clause, loc_subclause, loc_division_end, loc_part_end, loc_section_end, loc_subsection_end, loc_paragraph_end, loc_clause_end, loc_subclause_end, loc_note, extraction_method, extraction_status, promoted_to_rdc_id, notes, created_at, created_by_session, updated_at, updated_by_session, figure_role, comparator, harm_finding |
| term_adjudications | 90 | adjudication_id, observation_id, outcome, term_id, rationale, created_at, created_by_session, updated_at, updated_by_session |

## Views touching this stage (6)

| view | all stages spanned |
|---|---|
| v_derived_figure_check | judgment |
| v_determination_provenance | base, evidence, judgment, specification |
| v_root_id_conflicts | judgment |
| v_scan_ledger | base, evidence, judgment |
| v_unregistered_roots | base, evidence, judgment |
| v_value_independence | base, evidence, judgment |

## Contract criteria

| id | kind | check | criterion (first 200 chars) |
|---|---|---|---|
| handoff-fanout-preserved | integrity | scripts/audit/judgment_handoff_shape.py | The evidence->judgment hand-off is 1:N: source_value_extractions.ref_id is NOT NULL and references evidence_sources(ref_id), and NO UNIQUE index exists on that table. One evidence source may provide m |
| convergence-independence | completeness | **NONE (unenforced)** | Convergence counts INDEPENDENT evidence axes (and, once genealogy lands, independent roots excluding committee_assertion), never document/citation count. The root-count substrate exists (root_id / roo |
| comparator-recorded | completeness | **NONE (unenforced)** | A figure stated relative to something else carries that relation as a row in extraction_relations (migration 075, 2026-09-13), not only as a number. A ramp slope given as a bare ratio with no linked r |
| figure-role-stated | integrity | scripts/audit/extraction_relations_integrity.py | Every source_value_extractions row created after migration 075 applied states what kind of number it is (figure_role IS NOT NULL) once a grading writer exists; the eight rows that predate the migratio |
| verified-reading | integrity | scripts/audit/verified_scan_integrity.py | An extraction marked verified rests on a recorded FULL-scope source_scans reading that covers its parameter (catalogue mode at a catalogue_version >= the parameter, or targeted at it), and no extracti |

## `db.py` verbs that WRITE this stage's tables (10)

| verb | writes | reads | help |
|---|---|---|---|
| add-extraction | extraction_relations, source_value_extractions | base_parameters, base_taxonomy_medical, evidence_sources, external_root_registry, source_scans, source_slug_links, v_derived_figure_check, v_scan_ledger | Record what one source asserts for one parameter |
| add-population-match | evidence_population_match | base_taxonomy_identity, evidence_sources | Grade population-of-study vs population-served (R13 |
| add-term | term_adjudications, terms | observed_terms, term_aliases | Mint a term for a NEW concept and adjudicate it NAMES-NEW |
| adjudicate-term | term_adjudications | evidence_population_match, observed_terms, terms | Decide whether an observed phrase names our concept |
| amend-extraction | source_value_extractions | evidence_sources, extraction_relations, source_scans, v_scan_ledger | Change figure_role or comparator on an existing |
| amend-population-match | evidence_population_match |  | Re-grade an R13 match in place (a ruling, not a dissent -- |
| derive-extraction | extraction_relations, source_value_extractions | base_parameters, base_taxonomy_medical, evidence_sources, external_root_registry, source_scans, source_slug_links, v_derived_figure_check, v_scan_ledger | Write a computed (base+delta) extraction and the |
| raise-follow-up | extraction_follow_ups | source_value_extractions | Tag an extraction for a reviewer to re-check |
| relate-extraction | extraction_relations | source_value_extractions | Add a comparator edge to an existing extraction row, |
| resolve-follow-up | extraction_follow_ups |  | Close an open extraction follow-up with what the re-check |

## `db.py` verbs that only READ this stage's tables (6)

`add-alias`, `add-parameter`, `add-source`, `rename-term`, `retire-parameter`, `set-parameter-direction`

## Other code that WRITES this stage's tables (1)

| file | lines | writes | purpose (docstring) |
|---|---|---|---|
| scripts/audit/research_batch_dod.py | 1795 | source_value_extractions, term_adjudications | scripts/audit/research_batch_dod.py — RESEARCH BATCH DEFINITION-OF-DONE gate. **** RESEARCH IS INVALID IF IT IS NOT COMPLIANT WITH THIS PROJECT'S GOVERNANCE, **** **** VERIFICATION TOOLS, RULES AND ETHOS. (owner directive, 2026-07-24) ****  |

## Code that READS this stage's tables, writing none of them (11)

| file | lines | reads | purpose (docstring) |
|---|---|---|---|
| scripts/dbcore.py | 1385 | evidence_population_match, extraction_relations, source_value_extractions, term_adjudications | scripts/dbcore.py — the one place this repository opens, stamps and keys the database. WHY THIS EXISTS. Measured 2026-08-25: 104 raw `sqlite3.connect(` call sites across 55 live files, 48 independent resolutions of GUIDEBOOK_DB_PATH, and 37 |
| scripts/audit/adjudication_integrity.py | 185 | source_value_extractions | adjudication_integrity.py — audit the evidence-adjudication substrate. Adds the one mechanical adjudication check that is specified-but-unbuilt — the Stage-2.5 tier-derivation consistency sweep that schemas/tier_derivation.py's own docstrin |
| scripts/audit/extraction_follow_up_audit.py | 113 | extraction_follow_ups, source_value_extractions | scripts/audit/extraction_follow_up_audit.py — open follow-ups, and live values resting on one or on a skimmed figure. WHY THIS EXISTS (tooling T1, 2026-10-09). The owner's answer to D1: "D1: yes figure from source filed by another slug allo |
| scripts/audit/extraction_relations_integrity.py | 216 | extraction_relations, source_value_extractions | scripts/audit/extraction_relations_integrity.py — figure_role / extraction_relations integrity gate (migration 075, 2026-09-13). WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS (CLAUDE.md section 5(c) / section 1). `figure_role` is what |
| scripts/audit/judgment_handoff_shape.py | 90 | source_value_extractions | Pin the evidence -> judgment hand-off shape ruled 2026-08-27. WHAT WRONG THING REACHES THE GUIDEBOOK IF THIS DOES NOT EXIST (CLAUDE.md §1). The owner ruled evidence -> judgment is 1:N, with a worked example: "one evidence source may provide |
| scripts/audit/research_protocol_audit.py | 322 | evidence_population_match | Audit query for adversarial research protocol compliance. Flags: 1. Closed gaps lacking required protocol fields 2. Verified citations without population match records 3. Population match grade distribution suspicious (>70% EXACT) 4. Confid |
| scripts/audit/verified_scan_integrity.py | 108 | source_value_extractions | scripts/audit/verified_scan_integrity.py — does every live extraction rest on a verified source and a reading? WHY THIS EXISTS (CLAUDE.md section 8: what wrong thing reaches the guidebook). OR-11a (owner, 2026-10-29): `extraction_status = ' |
| scripts/audit/graph/topology.py | 259 | source_value_extractions | scripts/audit/graph/topology.py — Tier 1 graph-topology checks (stdlib only). Each check appends rows to the findings table. Severity is raw here; known-debt suppression and the pass/fail decision live in scripts/audit/graph_audit.py. Check |
| scripts/research/emit_batch_sql.py | 455 | evidence_population_match | scripts/research/emit_batch_sql.py — capture a research batch out of a scratch DB. DR-2026-08-19 §12.0 (F3). The research write path is a session-scoped scratch copy of the database: `db.py` writes to it under GUIDEBOOK_DB_PATH, so every wr |
| scripts/research/retrieval_log.py | 2261 | extraction_relations | scripts/research/retrieval_log.py — persist what was actually retrieved. WHY --- On 2026-08-19 the first research batch after the restart wrote FABRICATED author lists onto all five of its admissions, and stamped them `verification_status=' |
| scripts/assess/assess_cell.py | 2470 | evidence_population_match, extraction_relations, source_value_extractions | scripts/assess/assess_cell.py — the determination engine (rule_version: `RULE_VERSION` below). THE STATE IS COMPUTED. Owner ruling 2026-09-09 (references/project-standards.md): *"you have to compute it. I can't handle this load manually."*  |

## Tests naming this stage's tables (6)
`scripts/tests/test_assess_cell_pilot.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_db_integrity.py`, `scripts/tests/test_directness_2_2.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_scan_contract.py`

## Registry checks whose PRIMARY stage (by tables read) is `judgment` (4)

| check id | battery | level | basis |
|---|---|---|---|
| extraction_follow_up_audit | data | advisory | unattributed |
| test_assess_cell_pilot | tests | advisory | hygiene |
| test_directness_2_2 | tests | advisory | hygiene |
| extraction_relations_integrity | db_integrity | blocking | judgment/figure-role-stated |

## Skills naming this stage's tables (4)
`connection-discovery`, `cross-population-conflict-mapper`, `gap-driven-mining`, `run-pipeline`

## Prose homes for this stage
- `governance/evidence-architecture.md`
- `governance/time-model.md`
- `governance/held-tensions.md`