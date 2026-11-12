# 25 — Stage `specification`

_Generated 2026-11-12 02:01 UTC at commit e73b588, schema user_version 125. Every figure here is computed by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_dossier.py`; re-run it, do not trust this text (CLAUDE.md rule 7a)._


**Contract anchor:** the determination — "therefore 1200 mm, marked ●". conceptual-model.md:90 ("BPC synthesis produces specifications"), restored by D-0167

**Contract entry condition(s):** a synthesis with a resolved value, ready for determination

## Tables (4)

| table | rows | columns |
|---|---|---|
| determination_gates | 1 | gate_id, parameter_id, identity_code, verdict, trigger_ref_id, trigger_tier, trigger_evidence_type, detail, raised_at, raised_by_session, resolved_at, resolved_by_session, resolution_rationale |
| specification_extraction_links | 151 | specification_id, extraction_id, role, exclusion_reason, created_at, created_by_session |
| specification_source_links | 38 | specification_id, ref_id, role, created_at, created_by_session |
| specifications | 8 | specification_id, parameter_id, identity_code, icf_code, needs_code, medical_code, state, design_scale, convergence_id, confidence_dimensions_present, confidence_dimensions_absent, confidence_synthesis_basis, gap_register_id, not_applicable_rationale, tier_basis, governing_refs, rule_version, derivation_sha, code_floor_only, value_min, value_max, value_unit, falsification_condition, has_unverified_sources, all_sources_disqualified, regulatory_stratum_only, created_at, created_by_session, updated_at, updated_by_session, value_note, functional_basis, derivation_rationale, cultural_claim_anchor, derivation_paths, retired_at, retired_by_session, retirement_reason, superseded_by_specification_id, rests_on_proxy_inference, value_notations, marker |

## Views touching this stage (8)

| view | all stages spanned |
|---|---|
| v_best_practice | specification |
| v_code_floor_only | base, specification |
| v_determination_provenance | base, evidence, judgment, specification |
| v_divergence | specification, synthesis |
| v_item_provenance | base, evidence, specification |
| v_open_determination_gates | specification |
| v_pending | specification, synthesis |
| v_source_reach_all | base, evidence, specification |

## Contract criteria

| id | kind | check | criterion (first 200 chars) |
|---|---|---|---|
| governing-refs-nonempty | integrity | scripts/validate_evidence_state.py | No `stated` or `provisional` determination without at least one `specification_source_links` row with role `governing` (anti-hallucination); `specifications.governing_refs` is frozen history the write |
| no-regulatory-stratum-stated | integrity | scripts/validate_evidence_state.py | A cell flagged code_floor_only or regulatory_stratum_only is never `stated` (convergence-not-evidence; DR-2026-07-21 §2.2 — such cells stay `provisional` and render as weak-band best practice only, pe |
| tier3-alone-threshold | integrity | scripts/validate_evidence_state.py | A single-axis cell whose clinical sources are all Tier 3 is `provisional`, not `stated`. |
| no-diagnosis-only-determination | integrity | scripts/audit/medical_lens_integrity.py | No determination is keyed on medical_code alone. A medical lens always accompanies at least one of identity, ICF or access-need on the cell. |
| derivation-handshake | integrity | scripts/audit/derivation_handshake_integrity.py | Determinations record derivation_paths (dual/population_only/function_only); a single-path assertion carries a named-path rationale; advisory CONTRADICTS/UNLINKED checks force `provisional` (never `st |

## `db.py` verbs that WRITE this stage's tables (3)

| verb | writes | reads | help |
|---|---|---|---|
| raise-determination-gate | determination_gates | base_parameters, base_taxonomy_identity, evidence_sources | Raise an H4 gate: cap a cell at provisional until it is resolved |
| resolve-determination-gate | determination_gates |  | Close an H4 gate by the named path, with the rationale the schema requires |
| retire-specification | specifications |  | Retire a determination in place so its cell can be determined again |

## `db.py` verbs that only READ this stage's tables (4)

`add-medical`, `add-parameter`, `merge-parameter`, `retire-parameter`

## Other code that WRITES this stage's tables (2)

| file | lines | writes | purpose (docstring) |
|---|---|---|---|
| scripts/validate_verification_consistency.py | 155 | specification_source_links, specifications | validate_verification_consistency.py — the has_unverified_sources truthfulness gate. Mechanizes a lesson from the 2026-07-24 Phase-B session: a determination cell can claim its sources are content-verified (has_unverified_sources=0) while t |
| scripts/assess/assess_cell.py | 2470 | specification_extraction_links, specification_source_links, specifications | scripts/assess/assess_cell.py — the determination engine (rule_version: `RULE_VERSION` below). THE STATE IS COMPUTED. Owner ruling 2026-09-09 (references/project-standards.md): *"you have to compute it. I can't handle this load manually."*  |

## Code that READS this stage's tables, writing none of them (14)

| file | lines | reads | purpose (docstring) |
|---|---|---|---|
| scripts/dbcore.py | 1385 | specification_extraction_links, specification_source_links, specifications | scripts/dbcore.py — the one place this repository opens, stamps and keys the database. WHY THIS EXISTS. Measured 2026-08-25: 104 raw `sqlite3.connect(` call sites across 55 live files, 48 independent resolutions of GUIDEBOOK_DB_PATH, and 37 |
| scripts/validate_evidence_state.py | 554 | specification_source_links, specifications | scripts/validate_evidence_state.py — Validate evidence state records. Per governance/evidence-methodology.md (A6), §2 (cell states), §3 (convergence), and §1.4/§1.6/§1.7 (scale + directness); decision D-D. Stage 2.4 wires this to the real D |
| scripts/validate_parameters.py | 140 | specifications | scripts/validate_parameters.py — CI validator for the design-parameter registry (`base_parameters` pointing at `terms`). WHAT WRONG THING REACHES THE GUIDEBOOK IF THIS DOES NOT EXIST (CLAUDE.md §8): a parameter whose name states its own ans |
| scripts/validate_schema.py | 344 | specifications | scripts/validate_schema.py — Validate entity YAML files against Pydantic schemas. Walks data/ directories and validates each YAML file against the appropriate schema model. Used by CI (schema job) and session start (--quick mode). Usage: py |
| scripts/audit/adjudication_integrity.py | 185 | specifications | adjudication_integrity.py — audit the evidence-adjudication substrate. Adds the one mechanical adjudication check that is specified-but-unbuilt — the Stage-2.5 tier-derivation consistency sweep that schemas/tier_derivation.py's own docstrin |
| scripts/audit/column_vocabulary_audit.py | 214 | determination_gates | Do the tables agree on what to call the same thing? WHY THIS EXISTS. A pipeline-walk tool (since deleted) shipped a session-attribution helper matching two column names, `created_by_session` and `session`. The corpus spells that one role EI |
| scripts/audit/derivation_handshake_integrity.py | 272 | determination_gates, specification_source_links, specifications | scripts/audit/derivation_handshake_integrity.py — the handshake, checked on the rows. WHAT WRONG THING REACHES THE *GUIDEBOOK* IF THIS DOES NOT EXIST (CLAUDE.md §8's bar, which is about the book and not the apparatus): 1. A `stated` determi |
| scripts/audit/extraction_follow_up_audit.py | 113 | specification_extraction_links, specifications | scripts/audit/extraction_follow_up_audit.py — open follow-ups, and live values resting on one or on a skimmed figure. WHY THIS EXISTS (tooling T1, 2026-10-09). The owner's answer to D1: "D1: yes figure from source filed by another slug allo |
| scripts/audit/extraction_relations_integrity.py | 216 | specifications | scripts/audit/extraction_relations_integrity.py — figure_role / extraction_relations integrity gate (migration 075, 2026-09-13). WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS (CLAUDE.md section 5(c) / section 1). `figure_role` is what |
| scripts/audit/identifier_floor_audit.py | 158 | specifications | scripts/audit/identifier_floor_audit.py — an identifier is never reissued. WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS (CLAUDE.md section 1's burden of proof). A source's `ref_id` is how every record outside the database names it: r |
| scripts/audit/medical_lens_integrity.py | 119 | specifications | scripts/audit/medical_lens_integrity.py — the fourth lens cannot become the frame. WHAT WRONG THING REACHES THE *GUIDEBOOK* IF THIS DOES NOT EXIST (CLAUDE.md §8's bar for adding a check, which is about the book and not the apparatus): 1. A  |
| scripts/audit/graph/extract_db.py | 157 | specifications | scripts/audit/graph/extract_db.py — DB introspection layer (Tier 0, data). Reads data/guidebook.db READ-ONLY and materialises it into the audit graph: - one db_table node per table (with row_count), - one entity node per row of each primary |
| scripts/audit/graph/topology.py | 259 | specifications | scripts/audit/graph/topology.py — Tier 1 graph-topology checks (stdlib only). Each check appends rows to the findings table. Severity is raw here; known-debt suppression and the pass/fail decision live in scripts/audit/graph_audit.py. Check |
| scripts/generate/context_map.py | 351 | specifications | scripts/generate/context_map.py — emit governance/context-map.yaml. WHAT THIS IS. A machine-readable orientation index: where everything is, what it is, who writes it, who reads it, and whether it is canonical or derived. It exists so a fre |

## Tests naming this stage's tables (8)
`scripts/tests/_baseline_ddl.py`, `scripts/tests/test_assess_cell_pilot.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_db_integrity.py`, `scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_run_pipeline_refusals.py`, `scripts/tests/test_scan_contract.py`, `scripts/tests/test_validate_evidence_state_2_4.py`

## Registry checks whose PRIMARY stage (by tables read) is `specification` (5)

| check id | battery | level | basis |
|---|---|---|---|
| validate_verification_consistency | schema | blocking | unattributed |
| column_vocabulary_audit | schema | blocking | base/base-schema-validates |
| context_map_fresh | render | advisory | hygiene |
| identifier_floor_audit | db_integrity | blocking | base/base-identifier-never-reissued |
| derivation_handshake_integrity | schema | advisory | specification/derivation-handshake |

## Skills naming this stage's tables (5)
`connection-discovery`, `cross-population-conflict-mapper`, `cross-reference-resolver`, `functional-deficit-researcher`, `run-pipeline`

## Prose homes for this stage
- `governance/evidence-architecture.md`
- `governance/conceptual-model.md`