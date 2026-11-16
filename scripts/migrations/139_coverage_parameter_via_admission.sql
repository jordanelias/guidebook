-- v_coverage_parameter_via_admission: one row per ACTIVE parameter and per pair the research scope owes
-- (v_research_scope), saying how searches in that pair reached the parameter. Owner, OR-8 (2026-10-29):
-- exhaustion is judged per parameter and per bucket member, a jurisdiction with its associated language.
-- A pair with nothing is a row of zeros, never a missing row. No threshold and no "exhausted" flag: the
-- reader judges from the counts (rule 8). Stages: research (search_executions, search_admissions) and
-- judgment (source_value_extractions), joined on ref_id; base for the scope and the parameters.
-- A search's jurisdiction rolls up to its country (OD-04; base_jurisdictions.parent_code, migration 129).
-- Only a search that ran counts (deferred_reason IS NULL, as v_coverage_priority since migration 137).
-- Readers: skills/run-pipeline_SKILL.md (Scope paragraph), skills/research-log-manager_SKILL.md (coverage).
CREATE VIEW v_coverage_parameter_via_admission AS
WITH searched AS (
  SELECT se.exec_id, se.parameter_id, UPPER(se.language) AS language,
         COALESCE(b.parent_code, se.jurisdiction) AS jurisdiction
    FROM search_executions se
    LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction
   WHERE se.deferred_reason IS NULL),
reached AS (
  SELECT DISTINCT s.exec_id, s.language, s.jurisdiction, x.parameter_id, sa.ref_id
    FROM searched s
    JOIN search_admissions sa ON sa.exec_id = s.exec_id
    JOIN source_value_extractions x ON x.ref_id = sa.ref_id)
SELECT p.parameter_id, v.language, v.jurisdiction, v.role,
       (SELECT COUNT(*) FROM searched s WHERE s.parameter_id = p.parameter_id
           AND s.language = v.language AND s.jurisdiction = v.jurisdiction) AS searches_naming_parameter,
       (SELECT COUNT(DISTINCT r.exec_id) FROM reached r WHERE r.parameter_id = p.parameter_id
           AND r.language = v.language AND r.jurisdiction = v.jurisdiction) AS searches_reaching_parameter,
       (SELECT COUNT(DISTINCT r.ref_id) FROM reached r WHERE r.parameter_id = p.parameter_id
           AND r.language = v.language AND r.jurisdiction = v.jurisdiction) AS sources_admitted
  FROM base_parameters p CROSS JOIN v_research_scope v
 WHERE p.status = 'active';

PRAGMA user_version = 139;
