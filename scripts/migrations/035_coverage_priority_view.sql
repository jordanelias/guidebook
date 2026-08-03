-- 035_coverage_priority_view.sql
-- Schema migration: v_coverage_priority — the coverage-loop's priority queue.
-- Fixes the executability gap where the coverage-loop routine said "pop the highest-value
-- required cells from the priority queue" but no such artifact existed (adversarial review
-- 2026-07-24, finding C1). A "required" cell is one the lang_jur_map bridge marks in-scope
-- (a (language, jurisdiction) pair with a PRIMARY/SECONDARY role) crossed with an in-scope slug
-- (ACTIVE or STUB). A required cell is UNCOVERED when it has no search_executions row at all.
--
-- Score (minimal, faithful to coverage-completion-loop-methodology §4, not exhaustive):
--   role_weight (PRIMARY=3, SECONDARY=1) + slug_starvation_bonus (2 if the slug has zero
--   non-deferred logged searches). Open-gap and branch-thinness bonuses are omitted here
--   because gaps has no slug FK (linkage is free-text) — the loop applies those out-of-view.
-- Consumers order the queue: SELECT * FROM v_coverage_priority ORDER BY priority_score DESC,
--   slug_searches ASC LIMIT <batch>.
--
-- Read-only, additive. The runner sets PRAGMA user_version to 35.

BEGIN;

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
JOIN lang_jur_map ljm            -- CROSS JOIN: every in-scope slug x every required (lang,jur)
WHERE s.status IN ('ACTIVE', 'STUB')
  AND NOT EXISTS (
      SELECT 1 FROM search_executions se
      WHERE se.slug = s.slug
        AND se.jurisdiction = ljm.jurisdiction
        AND se.language = ljm.language
  );

COMMIT;
