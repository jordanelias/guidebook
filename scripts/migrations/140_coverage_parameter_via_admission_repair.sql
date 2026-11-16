-- 140_coverage_parameter_via_admission_repair.sql
-- SCHEMA migration, view only (a compensating migration: 139 is committed and is not edited). Repairs what the
-- read-only critic of T-067 found in v_coverage_parameter_via_admission:
--  * A SUPERSEDED SOURCE IS NOT A SECOND SOURCE (LED-171, migration 106): `reached` now joins evidence_sources and
--    keeps only sources with no superseded_by_ref_id. Live, (3, KO, KR) counted REF-01019 and its successor REF-01031,
--    one Korean annex, as two sources.
--  * A SEARCH REACHES A PARAMETER THROUGH A FIGURE A SOURCE STATES, not through a record that the source does NOT hold
--    it (claim_type 'absent') and not through a skimmed row (extraction_method 'skim'; dbcore.NOT_PUBLISHABLE_METHODS,
--    owner 2026-10-09, which a test pins against this literal). Two of parameter 8's three non-zero live pairs were
--    reached only by absence rows.
--  * A ROW OF ZEROS IS NOT "UNSEARCHED": a search that ran under a slug and admitted nothing credits no parameter.
--    searches_ran_in_pair counts every search that ran in the pair, whatever it was for, so "searched, nothing found"
--    and "not looked for" are told apart (research-log-manager: the thing the pipeline exists to preserve).
--  * jurisdiction_registered says whether the pair's jurisdiction is a declared code (a search cannot be logged in
--    one that is not), so a structural zero is not read as an unsearched pair.
-- Unchanged on purpose: a source admitted for one parameter reaches every parameter it holds a figure for (that is
-- what "through admissions" means); an UNVERIFIED source still reaches (a lead is a reach; whether it should is the
-- owner's reading of OR-8, recorded in the pull request); T-050 adds the retired_at filter to `reached`.
DROP VIEW v_coverage_parameter_via_admission;
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
    JOIN evidence_sources e ON e.ref_id = sa.ref_id AND e.superseded_by_ref_id IS NULL
    JOIN source_value_extractions x ON x.ref_id = sa.ref_id
   WHERE x.claim_type <> 'absent' AND COALESCE(x.extraction_method, '') <> 'skim')
SELECT p.parameter_id, v.language, v.jurisdiction, v.role,
       (SELECT COUNT(*) FROM searched s WHERE s.language = v.language AND s.jurisdiction = v.jurisdiction)
           AS searches_ran_in_pair,
       (SELECT COUNT(*) FROM searched s WHERE s.parameter_id = p.parameter_id
           AND s.language = v.language AND s.jurisdiction = v.jurisdiction) AS searches_naming_parameter,
       (SELECT COUNT(DISTINCT r.exec_id) FROM reached r WHERE r.parameter_id = p.parameter_id
           AND r.language = v.language AND r.jurisdiction = v.jurisdiction) AS searches_reaching_parameter,
       (SELECT COUNT(DISTINCT r.ref_id) FROM reached r WHERE r.parameter_id = p.parameter_id
           AND r.language = v.language AND r.jurisdiction = v.jurisdiction) AS sources_admitted,
       EXISTS (SELECT 1 FROM base_jurisdictions j WHERE j.jurisdiction_code = v.jurisdiction) AS jurisdiction_registered
  FROM base_parameters p CROSS JOIN v_research_scope v
 WHERE p.status = 'active';

PRAGMA user_version = 140;
