-- 100_search_execution_candidate_update_stamps.sql
-- SCHEMA migration — GAP-053, folded into DR-2026-09-26 phase 2b per the owner ruling
-- of 2026-09-27 ("The fix folds into phase 2b's tooling PR (DR-2026-09-26 §7) when
-- that lands.", references/project-standards.md).
--
-- THE DEFECT. `adversarial_pass_audit.py` scopes a session's subject rows by matching
-- every column ending `_by_session` (CLAUDE.md rule 8: derived, not a curated list) on
-- the 2026-08-19 RULE's eleven named tables. `search_executions` and `search_candidates`
-- carry only `created_by_session` — no `updated_by_session` — so a diff that runs
-- `amend-search`/`reattribute-candidate` (41 UPDATEs in the phase-2-data migration
-- alone: 24 to search_executions, 17 to search_candidates) is invisible to that scope
-- and reports EXAMINED: 0 / NOTHING-IN-SCOPE — CLAUDE.md's own named failure mode 5(a),
-- inside the very mechanism ratified 2026-09-27 to end it. The other 9 of the RULE's 11
-- tables already carry the pair (verified: `evidence_sources`, `source_slug_links`,
-- `source_value_extractions`, `specifications`, `convergence_assessment`,
-- `jurisdictional_values`, `case_studies`, `economics_entries` all have both
-- `updated_at` and `updated_by_session`; `evidence_population_match` has neither and is
-- append-only by convention, outside this migration's scope). This is a two-column
-- convention hole, not a design question.
--
-- BOTH COLUMNS, MATCHING THE LIVE CONVENTION. GAP-053's own fix names only
-- `updated_by_session` (the column the audit's suffix-match actually needs), but every
-- other stamped table in this schema carries `updated_at` alongside it, never one
-- without the other. Adding `updated_by_session` alone here would mint a new,
-- narrower one-off shape where a consistent one already exists across nine tables
-- (rule 8: derive the convention, do not invent a partial one).
--
-- BOTH NULLABLE, NO BACKFILL, NO DATA MIGRATION. Unlike a fresh-created table whose
-- rows are always stamped at INSERT, these two tables have existed since before this
-- column did, and NULL is the honest value for a row that has never been touched by
-- `amend-search`/`reattribute-candidate` — which is the literal truth for most of the
-- 100 `search_executions` and 130 `search_candidates` rows alive today. Filling a
-- retrospective value would be inventing history, not recording it, and would also
-- make this a research-data change under `research_tooling_separation` (RC6) rather
-- than the tooling-only migration it is. `log-search` and `add-candidate` (the INSERT
-- paths) are UNCHANGED: a freshly-inserted row's "last touched" fact is already
-- `created_at`/`created_by_session`; the new columns start recording only from the
-- first UPDATE a session actually makes.
--
-- No rebuild needed: both are plain nullable ADD COLUMNs, following migration 098's
-- own precedent for these same two tables.

ALTER TABLE search_executions ADD COLUMN updated_at TEXT;
ALTER TABLE search_executions ADD COLUMN updated_by_session TEXT;
ALTER TABLE search_candidates ADD COLUMN updated_at TEXT;
ALTER TABLE search_candidates ADD COLUMN updated_by_session TEXT;

PRAGMA user_version = 100;
