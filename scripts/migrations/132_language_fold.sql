-- 132_language_fold.sql
-- SCHEMA migration -- the two coverage views that report a language fold it to the map's letter case. No table,
-- column or row changes; no stored row is updated (the workplan declines it: K-9, K-10). Tooling (workplan
-- T-015 / the pipeline-resolution workplan's T-6a); no research rows.
--
-- WHY. The same language is stored as `EN` and `en` (search_executions holds both), so v_coverage_language counted
-- one language as two and v_coverage_lens reported it on two rows, and coverage asked for, or skipped, research on a
-- spelling. `db.py coverage`, v_coverage_priority and the pair anti-join already compare UPPER(language) (the
-- letter case lang_jur_map holds); these two views were the readers that did not, and they are made to.
--
-- WHAT. v_coverage_language groups by UPPER(language) and v_coverage_lens selects and groups by UPPER(language).
-- Everything else in each definition is the text of its last definition.
DROP VIEW IF EXISTS v_coverage_language;
CREATE VIEW v_coverage_language AS
SELECT slug, UPPER(language) AS language, COUNT(*) AS searches, SUM(results_admitted) AS admitted
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY slug, UPPER(language);

DROP VIEW IF EXISTS v_coverage_lens;
CREATE VIEW v_coverage_lens AS
SELECT slug, parameter_id, COALESCE(b.parent_code, se.jurisdiction) AS jurisdiction, UPPER(language) AS language,
       identity_code, icf_code, needs_code, medical_code,
       SUM(deferred_reason IS NULL) AS searches, SUM(deferred_reason IS NOT NULL) AS deferred
FROM search_executions se
LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8;

PRAGMA user_version = 132;
