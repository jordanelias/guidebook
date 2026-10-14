# PR body notes, step 1.6 (checks diet) -- branch stack/1.6-checks-diet (stacked on 1.5)
Eight checks deleted (code_currency_audit, pre_rehab_banner_audit, register_integrity_check, reasoning_doc_citations_audit, source_locators_integrity, validate_reasoning,
validate_bpc, validate_population); THREE criteria deleted (base-population-vocabulary, locator-title-matches-identifier, nine-step-synthesis). [CORRECTION: the commit title says four.]
adjudication_integrity promoted to blocking (EXAMINED, NULL tier/evidence_type fail; planted-NULL run exits 1). R44: PopulationCode enum retired.
Residual risk: validate_population P2 also covered reasoning_doc_citations.population and bpc_metadata.population (unconstrained, 0 rows each).
Owner-gated text: tier-system.md, evidence-architecture.md, population-taxonomy.md §5, conceptual-model.md (1 row), retired-vocabulary.yaml (1 sentence), pipeline-contract.yaml.
Owner items: bpc-reasoning/connection-reasoning _template.md still cite validate_reasoning.py (attestation needed); population-taxonomy §4.1 specifies a deleted check.
Instrument: P-QUARANTINE reworked (FAILs honestly for the render half until 3.R); C-028 reworded; 12 atoms deleted; C-018 edited; 20 re-anchored.

## After the adversarial pass (5ecc64f)
Commit-message corrections: title says four criteria (three deleted); "20 re-anchored" was 18. F1: R44 now carries a SUPERSEDES line for the 2026-07-24 ledger RULE ACTION (3) naming PopulationCode.
F2 OWNER ITEM: code_currency_audit never printed EXAMINED; its 17 flagged T4-T6 sources (code_currency_status NULL, pub_year 2006-2017) underlie retired specifications 4-8; R4's "surfaced by the 3.R view" is false until 3.R exists; whether R4's overturn clause is met is the owner's call (script in git history at 1bc5d5b^).
F3 every atom re-anchored (tool: scratchpad/tools/reanchor_all.py); seven atoms quoting the deleted validator spec deleted. F4 A14 added for evidence_population_match.target_population (the only populated population-valued column with no FK).
F6 population-taxonomy §4 (validator spec) deleted, banner and clauses fixed.
