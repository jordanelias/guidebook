# PR body notes, step 1.3 (splinter and case-study children) -- branch stack/1.3-splinter-children (stacked on 1.2)
Migration drop_splinter_and_case_study_children (re-pin the number at PR open) drops case_study_populations, citation_population_links,
economics_entry_populations, extraction_population_links, case_study_outcomes, case_study_strategies: all 0 rows, no inbound FK, no view or trigger, no data migration.
Callers: schemas/population_links.py deleted, validate_pydantic_schemas map (2), assess_cell docstring, stage-map (6), known_debt.yaml entry,
topology.MISSION_CRITICAL entry, emit_data_migration RANGE_GUARDS comment. population_integrity_audit already deleted in 1.2.
Gates: preflight PASS (same 8 advisory); selftest PASS; schema_reference_audit PASS; graph_audit PASS; rebuild parity (except 4 bot tables); FK/integrity clean.
Net-negative: scripts/schemas/.github/skills excluding migrations: 6 files +3 / -74.
Not done by design: schemas/case_study.py CaseStudyOutcome (output shape per validate_pydantic_schemas header; R5 owns mirrors).
Merge note: stack/1.2 repair c52f6be merged in (schemas/population_links.py modify/delete resolved by deletion).
