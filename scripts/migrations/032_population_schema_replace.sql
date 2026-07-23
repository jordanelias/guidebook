-- 032_population_schema_replace.sql
-- SCHEMA migration — structural half of the population retire/replace (DR-2026-07-23).
-- Only DDL here (creates the life-stage modifier table). The DATA transformation — the
-- population code re-key (rename/merge/repoint/delete) — is a DATA migration
-- (data_2026..._population-schema-replace.sql) so it runs in the data phase AFTER all
-- data is loaded. A schema migration runs before the data phase and would operate on
-- half-loaded tables, so the re-key MUST NOT live here.
-- Forward-only; user_version -> 32.

BEGIN TRANSACTION;

-- Life-stage modifiers (orthogonal; NOT populations — a child/older adult can hold any profile)
CREATE TABLE IF NOT EXISTS life_stage_modifiers (
  code TEXT PRIMARY KEY CHECK (code IN ('SEN','CHD')),
  label TEXT NOT NULL,
  definition TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now')), created_by_session TEXT
);
INSERT INTO life_stage_modifiers(code,label,definition) VALUES
 ('SEN','older adults; older disabled people','Life-stage modifier, orthogonal to all populations and needs. Many members reject "disabled" as a self-description while having substantial access needs.'),
 ('CHD','disabled children; children with disabilities','Life-stage modifier, orthogonal. Convention rests on parent-led/professional organizations more than children''s own stated preference — weaker evidence than elsewhere.');

-- Determinism for the rebuild gate
UPDATE life_stage_modifiers SET created_at='2026-07-23T00:00:00Z', created_by_session='session_2026-07-23-population-schema-replace';

COMMIT;
