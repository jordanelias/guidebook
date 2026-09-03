-- 070_v_source_admission_carries_the_prior.sql
-- SCHEMA migration — the pointer must carry what its reader needs.
--
-- Migration 069 moved prior_expectation to search_executions, where the fact exists,
-- and repointed research_protocol_audit CHECK 7 to reach it the way CHECK 8 reaches
-- query_text: through v_source_admission, on the shared reference id.
--
-- But the view did not SELECT the column, so the repointed check could not see it. A
-- VIEW IS A CALLER (CLAUDE.md rule 4), and a rename or move is not done until the
-- callers are swept -- migration 064 exists because 063 swept eight Python readers and
-- six skills and missed v_item_provenance. This is the same sweep, caught before
-- shipping rather than after: CHECK 7 would have reported every verified source as
-- lacking a prior, because the pointer returned NULL for all of them.
--
-- Nothing else changes. Column order is preserved and prior_expectation is appended, so
-- any positional reader keeps working; there are none, but the cost of appending rather
-- than inserting is zero.

DROP VIEW IF EXISTS v_source_admission;

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
    se.session                  AS admitting_session,
    se.executed_at              AS admitted_at,
    -- The research-stage prior, reached by pointer rather than copied onto the
    -- evidence row. This is what makes CHECK 7 answerable.
    se.prior_expectation
FROM evidence_sources es
JOIN search_admissions sa ON sa.ref_id  = es.ref_id
JOIN search_executions se ON se.exec_id = sa.exec_id;

PRAGMA user_version = 70;
