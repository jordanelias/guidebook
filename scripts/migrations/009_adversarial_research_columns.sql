-- 009_adversarial_research_columns.sql
-- Captures column additions to evidence_sources and gaps that were applied
-- ad-hoc during the adversarial-research protocol rollout (DR-2026-05-09)
-- but never represented in a schema migration. Adding them here so that
-- rebuilding the DB from migrations produces the same schema as production.
--
-- Per GAP-290 resolution: closes the schema-drift gap that prevented the
-- migration-reproducibility CI check from passing.
--
-- schema_version → 9
--
-- Note: ALTER TABLE ADD COLUMN is idempotent-safe via the "IF NOT EXISTS"
-- pattern in SQLite 3.35+. We use a check pattern to avoid errors if the
-- column already exists (e.g., when running against a production DB that
-- already had the ad-hoc adds applied).

-- evidence_sources additions (per adversarial-research protocol)
ALTER TABLE evidence_sources ADD COLUMN derivation_chain TEXT;
ALTER TABLE evidence_sources ADD COLUMN prior_expectation TEXT;
ALTER TABLE evidence_sources ADD COLUMN search_queries_used TEXT;

-- gaps additions (per adversarial-research protocol, standing rule #7)
ALTER TABLE gaps ADD COLUMN confidence_interval TEXT;
ALTER TABLE gaps ADD COLUMN shift_conditions TEXT;
ALTER TABLE gaps ADD COLUMN named_dissenter TEXT;
ALTER TABLE gaps ADD COLUMN falsification_condition TEXT;
