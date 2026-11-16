-- 137: a deferred search is not a searched pair.
-- T-080 (OD-45, resolved under delegation) tells a session to log a request that returned no result list with
-- --deferred-reason, as a search NOT RUN. v_coverage_priority's anti-join named a pair searched on any logged row,
-- deferred or not, so that search took its cell off the owed list and `db.py coverage --slug` counted it searched
-- (the T-080 critic, 2026-11-15). The anti-join now reads only rows that ran, as the view's own slug_searches column
-- and v_coverage_lens.searches already do. A deferred row stays visible in v_coverage_lens.deferred.
-- Only the view changes; no table is touched.

DROP VIEW v_coverage_priority;
CREATE VIEW v_coverage_priority AS
SELECT
    s.slug,
    ljm.jurisdiction,
    ljm.language,
    ljm.role,
    ( (CASE ljm.role WHEN 'PRIMARY' THEN 3 ELSE 1 END)
      + (CASE WHEN (SELECT COUNT(*) FROM search_executions se2
                    WHERE se2.slug = s.slug AND se2.deferred_reason IS NULL) = 0
              THEN 2 ELSE 0 END)
    ) AS priority_score,
    (SELECT COUNT(*) FROM search_executions se3
     WHERE se3.slug = s.slug AND se3.deferred_reason IS NULL) AS slug_searches
FROM slugs s
JOIN v_research_scope ljm        -- CROSS JOIN: every in-scope slug x every owed (lang,jur)
WHERE s.status IN ('ACTIVE', 'STUB')
  AND NOT EXISTS (
      SELECT 1 FROM search_executions se
      LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction
      WHERE se.slug = s.slug
        AND se.deferred_reason IS NULL
        AND COALESCE(b.parent_code, se.jurisdiction) = ljm.jurisdiction
        AND UPPER(se.language) = ljm.language
  );

PRAGMA user_version = 137;
