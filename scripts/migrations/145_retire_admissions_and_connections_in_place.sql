-- 145_retire_admissions_and_connections_in_place.sql
-- SCHEMA migration (T-050; OD-29, resolved under delegation: a connection and a search-to-source admission edge are
-- data rows under the owner's ruling of 2026-09-16, "RETIRE IN PLACE, NEVER HARD-DELETE"; a genuine deletion of either
-- is an exception only the owner rules on). No data rows.
--
-- `search_admissions` and `connections` each gain the retirement shape `specifications` and `extraction_lens_links`
-- already use: `retired_at`, `retired_by_session` and `retirement_reason`, nullable, set together or not at all. The
-- CHECK sits on the last of the three, because SQLite adds a column by ALTER and a column constraint may name its
-- siblings. `connection_targets` gains nothing: a target of a retired connection is retired through its pointer.
--
-- THE RULING'S EXECUTION CONDITION: "No row is retired in place until every reader that could surface it filters on
-- status." The two views that read `search_admissions` filter below; every other reader of either table is a script and
-- is fixed in the same pull request (db.py, research_batch_dod.py, test_db_integrity.py, graph/extract_db.py).
--  * v_source_admission, from its current text in sqlite_master (migration 070 set it), gains `AND sa.retired_at IS NULL`:
--    a withdrawn attribution is not "the search that admitted this source".
--  * v_coverage_parameter_via_admission, from its current text (migration 140 set it), gains the same predicate in the
--    `reached` CTE: a search does not reach a parameter through an admission it has withdrawn. No view reads
--    `connections` or `connection_targets`.
-- The retired edge stays a row: it is the record that the claim was made, when, by whom and why it was withdrawn, and it
-- is never un-retired in place (db.py link-admission refuses it and names log-search).
-- WRITERS: db.py unlink-admission and delete-connection (each now sets the three columns instead of deleting).
-- READERS: the two views above, db.py get_connections, db.py's parameter reach, research_batch_dod R17,
-- test_db_integrity S01 and the graph extractor.

ALTER TABLE search_admissions ADD COLUMN retired_at TEXT;
ALTER TABLE search_admissions ADD COLUMN retired_by_session TEXT;
ALTER TABLE search_admissions ADD COLUMN retirement_reason TEXT
  CHECK ((retired_at IS NULL) = (retired_by_session IS NULL) AND (retired_at IS NULL) = (retirement_reason IS NULL));

ALTER TABLE connections ADD COLUMN retired_at TEXT;
ALTER TABLE connections ADD COLUMN retired_by_session TEXT;
ALTER TABLE connections ADD COLUMN retirement_reason TEXT
  CHECK ((retired_at IS NULL) = (retired_by_session IS NULL) AND (retired_at IS NULL) = (retirement_reason IS NULL));

DROP VIEW v_source_admission;
CREATE VIEW v_source_admission AS
SELECT
    es.ref_id,
    es.pub_title,
    es.tier                     AS source_tier,
    es.evidence_type,
    es.verification_status,
    es.verification_disposition,
    se.exec_id,
    se.slug                     AS admitted_under_slug,
    se.query_text,
    se.engine,
    se.language,
    se.jurisdiction             AS search_jurisdiction,
    se.depth_method,
    se.mining_direction,
    se.target_tier,
    se.backfill                 AS search_was_backfilled,
    se.created_by_session                  AS admitting_session,
    se.created_at              AS admitted_at,
    -- The research-stage prior, reached by pointer rather than copied onto the
    -- evidence row. This is what makes CHECK 7 answerable.
    se.prior_expectation
FROM evidence_sources es
JOIN search_admissions sa ON sa.ref_id  = es.ref_id AND sa.retired_at IS NULL
JOIN search_executions se ON se.exec_id = sa.exec_id;

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
    JOIN search_admissions sa ON sa.exec_id = s.exec_id AND sa.retired_at IS NULL
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

PRAGMA user_version = 145;
