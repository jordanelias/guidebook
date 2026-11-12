# 10 — The pipeline itself

_Generated 2026-11-12 02:01 UTC at commit e73b588, schema user_version 125. Every figure here is computed by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_dossier.py`; re-run it, do not trust this text (CLAUDE.md rule 7a)._


## 10.1 Spine and contract

```
base -> research -> evidence -> judgment -> synthesis -> specification -> render
```

Contract status: `PROPOSED`, ratified: `False`. Stages: base, research, evidence, judgment, synthesis, specification, render.

Cross-stage criteria:

| id | check | criterion (first 200) |
|---|---|---|
| adherence-log | scripts/audit/adherence_log_audit.py | Each stage boundary emits `[ADHERENCE-LOG — stage N: <name>]` with per-rule FIRED/NOT-FIRED/SKIPPED, a bias_direction, and an independent_reviewer_counterclaim. |
| attestation-doctrine-binding | scripts/audit/adherence_log_audit.py | Commits touching synthesis paths carry a schema-valid attestations/<slug>.json. (The [DOCTRINE:<7-sha>] token half was abolished 2026-08-19 by OD-10 item 4.) |
| definition-of-done | scripts/audit/claims_docket.py | No ratification request / 'done' / ready-for-review PR while the integrity-protocol Mode-3 mechanical battery is unrun OR an independent adversarial pass is unrun/unapplied. |
| reproducibility-invariant | scripts/audit/migration_reproducibility.py | The committed DB reproduces the 7 core invariants from migration history, and no table is exempt. |
| doctrine-recheck | scripts/doctrine_recheck.py | A doctrine recheck fires at every stage transition and every 25 sessions; work-product must not contradict canonical doctrine. |
| doctrine-currency | scripts/audit/supersession_backpointer_audit.py | A ruling that supersedes binding text elsewhere carries a SUPERSEDES/BY back-pointer at the superseded text itself, anchored on quotes occurring exactly once at both ends -- never a currency index, wh |
| research-tooling-separation | scripts/audit/research_tooling_separation.py | Research data (rows, or a data migration) and tooling (schema, scripts, checks, governance prose) ship in separate changesets -- never both in one, so a writer gap found mid-batch cannot be patched wi |


**Contract criteria with `check: null` (unenforced): 5** — base/base-direction-from-source, judgment/convergence-independence, judgment/comparator-recorded, synthesis/opus-routing, render/register-invariants

## 10.2 Pipeline-level code

- `scripts/db.py` (10821 lines) — scripts/db.py — SQLite interface for guidebook data layer. Environment: GUIDEBOOK_DB_PATH Path to database file (default: data/guidebook.db) CLI usage: python3 scripts/db.py init python3 scripts/db.py migrate python3 scripts/db.py gaps [--p
- `scripts/dbcore.py` (1385 lines) — scripts/dbcore.py — the one place this repository opens, stamps and keys the database. WHY THIS EXISTS. Measured 2026-08-25: 104 raw `sqlite3.connect(` call sites across 55 live files, 48 independent resolutions of GUIDEBOOK_DB_PATH, and 37
- `scripts/run_checks.py` (1013 lines) — scripts/run_checks.py — the single entry point for every ecosystem check. Reads governance/check-registry.yaml, works out which checks the current change actually warrants, runs them, and reports. CI and scripts/preflight.sh both call this,
- `scripts/migrate_db.py` (626 lines) — scripts/migrate_db.py — Run pending migrations against guidebook.db. Spec: architecture/sqlite-data-layer.md §7 (schema) + governance/concurrent-write-architecture-proposal-2026-05-11.md (data). Handles BOTH migration types: 1. Schema migra
- `scripts/emit_data_migration.py` (783 lines) — scripts/emit_data_migration.py — create a properly-named data-migration file. Per GAP-290 resolution. The migration system (scripts/migrate_db.py) requires data migrations to be named: scripts/migrations/data_{YYYYMMDDHHMMSS}_{session-slug}
- `scripts/research/emit_batch_sql.py` (455 lines) — scripts/research/emit_batch_sql.py — capture a research batch out of a scratch DB. DR-2026-08-19 §12.0 (F3). The research write path is a session-scoped scratch copy of the database: `db.py` writes to it under GUIDEBOOK_DB_PATH, so every wr
- `scripts/research/retrieval_log.py` (2261 lines) — scripts/research/retrieval_log.py — persist what was actually retrieved. WHY --- On 2026-08-19 the first research batch after the restart wrote FABRICATED author lists onto all five of its admissions, and stamped them `verification_status='
- `scripts/assess/assess_cell.py` (2470 lines) — scripts/assess/assess_cell.py — the determination engine (rule_version: `RULE_VERSION` below). THE STATE IS COMPUTED. Owner ruling 2026-09-09 (references/project-standards.md): *"you have to compute it. I can't handle this load manually."* 
- `scripts/preflight.sh` (106 lines)

## 10.3 Migrations

226 files in `scripts/migrations/` (157 `data_*`). Schema migrations (first 3 and last 3 by name): `057_baseline_2026-08-12.sql`, `058_status_vocabulary_ratification.sql`, `059_tier1_retirements.sql`, `123_research_scope_and_ledger_precedence.sql`, `124_ledger_blocked_precedence.sql`, `125_alias_observation_pointer.sql`

## 10.4 Check registry

75 checks. By battery: {'syntax': 3, 'structure': 1, 'db_integrity': 4, 'data': 12, 'research': 14, 'governance': 11, 'schema': 13, 'attestation': 4, 'tests': 12, 'render': 1}. By level: {'blocking': 30, 'advisory': 43, 'informational': 2}.

| id | battery | level | kinds | primary stage by tables | basis |
|---|---|---|---|---|---|
| check_utf8_md | syntax | blocking | always | — | hygiene |
| check_json | syntax | blocking | always | — | hygiene |
| check_yaml | syntax | blocking | always | — | hygiene |
| validate_cross_refs | structure | blocking | always | base | hygiene |
| test_db_integrity | db_integrity | blocking | data,schema | research | unattributed |
| migration_reproducibility | data | blocking | data,schema | evidence | cross_stage/reproducibility-invariant |
| migration_reproducibility_deep | data | advisory | data,schema | evidence | cross_stage/reproducibility-invariant |
| source_slug_links_duplicates | data | blocking | data | evidence | unattributed |
| validate_parameters | data | advisory | data,schema | base | base/base-parameter-vocabulary |
| readonly_db_open_audit | data | advisory | data,tooling | — | unattributed |
| db_path_env_audit | data | blocking | data,tooling | — | unattributed |
| alias_provenance_audit | data | blocking | data | base | unattributed |
| observation_verbatim_audit | data | advisory | data | evidence | unattributed |
| scan_debt | data | advisory | data | base | unattributed |
| verified_scan_integrity | db_integrity | advisory | data,schema | evidence | judgment/verified-reading |
| extraction_follow_up_audit | data | advisory | data | judgment | unattributed |
| citation_mining_session | data | advisory | data,synthesis | evidence | unattributed |
| citation_mining_backlog_t2 | data | informational | data | evidence | unattributed |
| provenance_artefact_audit | research | blocking | data | research | evidence/discovery-provenance |
| provenance_attribution_audit | research | advisory | data | research | evidence/discovery-provenance |
| claude_skills_loadable | governance | advisory | governance,docs | — | hygiene |
| claude_md_spine | governance | blocking | governance,docs | — | base/base-names-resolve |
| schema_reference_audit | schema | blocking | schema,code,governance | — | base/base-names-resolve |
| validate_schema_cross_check | schema | advisory | schema,data | synthesis | base/base-schema-validates |
| validate_evidence_state | schema | blocking | schema,data,synthesis | synthesis | ['specification/governing-refs-nonempty', 'specification/no-regulatory-stratum-stated', 'specification/tier3-alone-threshold'] |
| jurisdiction_db_vocabulary | schema | blocking | schema,data | base | base/base-jurisdiction-vocabulary |
| validate_jurisdiction | schema | blocking | schema,data | — | base/base-jurisdiction-vocabulary |
| validate_verification_consistency | schema | blocking | schema,data | specification | unattributed |
| audit_evidence_metadata | schema | advisory | data,synthesis | evidence | unattributed |
| audit_adversarial_use | governance | blocking | governance,data | — | unattributed |
| author_fidelity | research | advisory | data,synthesis | research | DR-2026-08-19 §7 adversarial pass, lens L1 (2026-08-19) |
| doctrine_recheck | governance | blocking | governance,synthesis | — | cross_stage/doctrine-recheck |
| skill_vocabulary_audit | governance | advisory | governance,docs | base | base/base-derived-not-curated |
| retired_vocabulary | governance | advisory | always | — | base/base-retired-vocabulary-not-taught |
| matrix_consistency | governance | advisory | governance,schema | — | render/mode-stratum-matrix-consistency |
| pipeline_contract_audit | governance | advisory | governance,tooling | synthesis | unattributed |
| claims_docket | governance | advisory | governance,synthesis | — | cross_stage/definition-of-done |
| attestation_presence | attestation | blocking | synthesis,governance | base | cross_stage/adherence-log |
| attestation_schema | attestation | blocking | synthesis,governance | base | cross_stage/adherence-log |
| attestation_evidence | attestation | advisory | synthesis,governance | base | cross_stage/adherence-log |
| attestation_verdict | attestation | informational | synthesis,governance | base | cross_stage/adherence-log |
| research_contract_baseline_ratchet | research | blocking | always | research | hygiene |
| research_contract_sync | research | blocking | governance,tooling | — | hygiene |
| research_dod_selftest | research | blocking | always | research | unattributed |
| research_dod | research | advisory | data,synthesis | research | unattributed |
| research_dod_session | research | blocking | data,synthesis | research | unattributed |
| adversarial_pass_recorded | research | advisory | data,synthesis | base | cross_stage/definition-of-done |
| search_log_completeness | research | advisory | data,synthesis | research | evidence/discovery-provenance |
| test_search_log_completeness | tests | advisory | tooling | research | hygiene |
| research_tooling_separation | governance | advisory | data | — | cross_stage/research-tooling-separation |
| supersession_backpointer_audit | governance | advisory | governance,synthesis | — | cross_stage/doctrine-currency |
| research_protocol_audit | research | advisory | data,synthesis | research | research/adversarial-fields-complete |
| metadata_integrity_audit | research | advisory | data,synthesis | evidence | evidence/evidence-verification-gate |
| gap_mining_audit | research | advisory | data,synthesis | synthesis | unattributed |
| graph_audit | research | advisory | data,synthesis | synthesis | unattributed |
| test_graph_audit | tests | advisory | tooling | — | hygiene |
| test_pipeline_contract | tests | advisory | tooling,governance | — | hygiene |
| test_record_command_session | tests | advisory | tooling | — | hygiene |
| test_db_amend_writers | tests | advisory | tooling | base | hygiene |
| test_run_pipeline_refusals | tests | advisory | tooling,schema | research | hygiene |
| test_scan_contract | tests | advisory | tooling,schema | base | hygiene |
| test_author_presence | tests | advisory | tooling | — | hygiene |
| test_assess_cell_pilot | tests | advisory | tooling,data | judgment | hygiene |
| test_evidence_cell_state_2_3 | tests | advisory | tooling,data,schema | base | hygiene |
| test_validate_evidence_state_2_4 | tests | advisory | tooling,data,schema | base | hygiene |
| test_directness_2_2 | tests | advisory | tooling,data | judgment | hygiene |
| column_vocabulary_audit | schema | blocking | schema,data | specification | base/base-schema-validates |
| context_map_fresh | render | advisory | data,schema,tooling,governance | specification | hygiene |
| judgment_handoff_shape | schema | blocking | schema,data,governance | evidence | judgment/handoff-fanout-preserved |
| extraction_relations_integrity | db_integrity | blocking | data,schema,governance | judgment | judgment/figure-role-stated |
| derived_not_curated_audit | schema | blocking | schema,governance | research | base/base-derived-not-curated |
| identifier_floor_audit | db_integrity | blocking | data,schema,governance | specification | base/base-identifier-never-reissued |
| derivation_handshake_integrity | schema | advisory | schema,data,governance | specification | specification/derivation-handshake |
| adjudication_integrity | schema | blocking | data,schema | synthesis | unattributed |
| medical_lens_integrity | schema | advisory | schema,data,governance | base | base/base-medical-lens-offered-not-adopted |

## 10.5 Skills and project agents/commands

Project skills (`.claude/skills/`): `bibliography-compiler`, `citation-miner`, `citation-verifier`, `connection-discovery`, `content-gap-analyzer`, `cross-population-conflict-mapper`, `cross-reference-resolver`, `doctrine-recheck`, `economics-researcher`, `evidence-auditor`, `find-and-replace`, `functional-deficit-researcher`, `gap-driven-mining`, `github-io`, `jurisdiction-tracker`, `multilingual-research`, `prose-style-checker`, `research-log-manager`, `run-pipeline`, `session-consolidator`, `supersession-audit`, `toc-editor`

Agents: `antagonist`, `db-census`, `repo-sweep`. Commands: `/adversarial`, `/batch-done`, `/orient`, `/session-open`

## 10.6 Operations (verbatim `governance/pipeline-operations.md` §1)

See that file. Stage-orchestration entry point: `.claude/skills/run-pipeline/SKILL.md` (verbatim copy appended in `11-run-pipeline-skill.md`).
