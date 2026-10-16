-- 112_search_execution_lens.sql
-- SCHEMA migration -- a logged search can say which lens it covered (plan Phase 3 research;
-- RULINGS R18, COMPARISON P2). The 2026-08-24 ruling is that every research slug is searched against
-- every population, access need and ICF code; before this file the log could not show it, because
-- search_executions had a slug and a free-text terms_used and no lens column (conflict C-033).
--
-- FOUR NULLABLE COLUMNS, each pointing at the registry of the lens it names. The key column of
-- access_needs is need_code; needs_code is the referencing column's name, as on
-- source_value_extractions and specifications. No CHECK (an optional lens is not "at least one"),
-- no DEFAULT, no backfill: the rows already logged keep NULL in all four, because saying which lens a
-- past search covered would be a research act (CLAUDE.md rule 10), and terms_used is kept.
--
--   identity_code -> populations(population_code)
--   icf_code      -> base_icf(icf_code)
--   needs_code    -> access_needs(need_code)
--   medical_code  -> base_taxonomy_medical(medical_code)     (holds no row until Phase 5 fills it)
--
-- NO AFTER_DATA MARKER: nothing is backfilled, and no committed data migration INSERTs into
-- search_executions without naming its columns, so a replay that reaches them before or after the
-- ALTER works. Re-derive:
--   grep -hE "INSERT (OR [A-Z]+ )?INTO \"?search_executions\"?\s*(VALUES|SELECT)" scripts/migrations/*.sql | wc -l
--
-- ONE VIEW over the logged cells, named for the v_coverage_* family and counting as they do: a
-- deferral is not a search. It lists cells that were logged; a never-searched cell is not derivable
-- from it, which needs a cross join against the registries (as v_coverage_priority does for
-- jurisdiction x language) and is not built here.

ALTER TABLE search_executions ADD COLUMN identity_code TEXT REFERENCES populations(population_code);
ALTER TABLE search_executions ADD COLUMN icf_code TEXT REFERENCES base_icf(icf_code);
ALTER TABLE search_executions ADD COLUMN needs_code TEXT REFERENCES access_needs(need_code);
ALTER TABLE search_executions ADD COLUMN medical_code TEXT REFERENCES base_taxonomy_medical(medical_code);

CREATE VIEW v_coverage_lens AS
SELECT slug, jurisdiction, language, identity_code, icf_code, needs_code, medical_code,
       SUM(deferred_reason IS NULL) AS searches, SUM(deferred_reason IS NOT NULL) AS deferred
FROM search_executions GROUP BY 1, 2, 3, 4, 5, 6, 7;

PRAGMA user_version = 112;
