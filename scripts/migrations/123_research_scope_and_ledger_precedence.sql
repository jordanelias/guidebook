-- 123_research_scope_and_ledger_precedence.sql
-- SCHEMA migration -- two derived views corrected after the second operator walk-through of the run-pipeline skill,
-- 2026-11-06 (scratchpad run-pipeline-round2-adjudication.md, R2-1 and R2-3). No table, column or row changes.
--
-- 1. v_research_scope (new) -- the ONE home of "what is owed". Migration 122 added lang_jur_map.scope_status, NULL
--    meaning "not recorded". `db.py coverage` and v_coverage_priority then read the column in the wrong direction: on
--    2026-11-06 marking four languages `scoped-out` left every other row NULL, and `coverage` read required 0/0,
--    complete true. A NULL scope_status is OWED: an unrecorded scope never shrinks the requirement. The fill of the
--    column is a data migration after owner question 5 (the two jurisdiction homes), not this one.
--    Readers: v_coverage_priority, `db.py coverage`.
-- 2. v_coverage_priority -- reads v_research_scope instead of lang_jur_map, and compares the logged language folded
--    to upper case: live search_executions rows hold `en`, `fr`, `ja`, `nl` while the map holds `EN`, `FR`, ...
--    (derive: SELECT language, COUNT(*) FROM search_executions GROUP BY 1), so the anti-join never matched them.
-- 3. v_scan_ledger -- precedence corrected and BLOCKED narrowed. Migration 122 ranked BLOCKED above the readings, so
--    a reading of held bytes (which proves the block lifted) was masked by a stale reason. A recorded reading now
--    outranks a block, and only the reasons whose CHECK comment (migration 091) says the text could not be obtained or
--    read count as an obstacle. Readers: scan_debt.py, research_batch_dod R16-scan and R11-harvest,
--    verified_scan_integrity.py.

DROP VIEW v_coverage_priority;
DROP VIEW v_scan_ledger;

CREATE VIEW v_research_scope AS
-- v_research_scope: the (language, jurisdiction) pairs the research scope OWES a search for.
--
-- The ONE home of "what is owed": every lang_jur_map row not recorded `scoped-out`. A NULL scope_status is owed --
-- an unrecorded scope never shrinks the requirement (on 2026-11-06 marking four languages `scoped-out` left every
-- other row NULL, and `coverage` read required 0/0, complete true). The fill of scope_status is a data migration
-- after owner question 5; until then the requirement is the whole map, less what is recorded `scoped-out`.
-- Readers: v_coverage_priority, `db.py coverage`.
SELECT language, jurisdiction, role
  FROM lang_jur_map
 WHERE COALESCE(scope_status, 'in-scope') <> 'scoped-out';

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
      WHERE se.slug = s.slug
        AND se.jurisdiction = ljm.jurisdiction
        AND UPPER(se.language) = ljm.language
  );

CREATE VIEW v_scan_ledger AS
-- v_scan_ledger: one row per (source in scope) x (active parameter).
--
--   source in scope   evidence_sources with superseded_by_ref_id IS NULL. A tombstone is
--                     never read again; its replacement is.
--   active parameter  base_parameters.status = 'active'. Retired and merged parameters
--                     leave the ledger (their extractions stay, as history).
--
-- STATUS PRECEDENCE, first match wins:
--   1 EXTRACTED          a non-absent extraction exists for the pair (any figure_role).
--   2 STATED-ABSENT      only claim_type 'absent' extractions exist: the source addresses
--                        the quantity and sets nothing -- a positive statement.
--   3 READ-NOTHING-FOUND a FULL-scope reading covers the pair and found no row.
--   4 READ-PARTIAL       only partial / fragment / abstract readings cover it.
--   5 BLOCKED            no reading covers the pair AND the source carries a
--                        processing_blocked_reason that says its text could not be obtained
--                        or read: nothing of it can be read, so the pair is not reading
--                        debt until the block clears.
--   6 NOT-READ           no reading covers it.
-- A recorded reading ALWAYS outranks a block: a reading of held bytes proves the block
-- lifted (migration 122 ranked BLOCKED above the readings and masked them). A reading
-- COVERS a pair when it is catalogue-mode with catalogue_version >= parameter_id (the
-- parameter existed when the reading was made), or targeted at that parameter. Rows 1 and
-- 2 win over readings because a row written is stronger evidence than a reading recorded;
-- 3 wins over 4 because a full reading supersedes a partial one of the same source.
--
-- THE BLOCKED CASE BELOW IS THE ONE HOME of "the text could not be obtained or read": the
-- writers and gates read this view's status, never the column. It admits exactly the
-- processing_blocked_reason values whose CHECK comment (migration 091) names an obstacle to
-- the text: no-full-text, paywalled, no-doi, not-indexed, language. `no-quantified-claims`
-- and `superseded` are copies of typed facts (a recorded reading; superseded_by_ref_id) and
-- the writers refuse them by pointer. `out-of-scope` and `tier-not-required` say no text
-- was unobtainable, so they are treated as NULL (the source owes its reading) pending
-- owner question 8 of the round-2 adjudication.
--
-- scan_id / text_scope / method name the STRONGEST covering reading (full scope first,
-- then full-read before pre-screen, then the latest), so a READ-NOTHING-FOUND resting on
-- a pre-screen only is visible as such. NULL when no reading covers the pair.
WITH pairs AS (
    SELECT e.ref_id, p.parameter_id, e.processing_blocked_reason
      FROM evidence_sources e
     CROSS JOIN base_parameters p
     WHERE e.superseded_by_ref_id IS NULL
       AND p.status = 'active'
),
best AS (
    SELECT pr.ref_id, pr.parameter_id, pr.processing_blocked_reason,
           (SELECT s.scan_id FROM source_scans s
             WHERE s.ref_id = pr.ref_id
               AND ((s.mode = 'catalogue' AND s.catalogue_version >= pr.parameter_id)
                 OR (s.mode = 'targeted' AND s.target_parameter_id = pr.parameter_id))
             ORDER BY (s.text_scope = 'full') DESC, (s.method = 'full-read') DESC,
                      s.scan_id DESC
             LIMIT 1) AS scan_id
      FROM pairs pr
)
SELECT b.ref_id,
       b.parameter_id,
       CASE
         WHEN EXISTS (SELECT 1 FROM source_value_extractions x
                       WHERE x.ref_id = b.ref_id AND x.parameter_id = b.parameter_id
                         AND x.claim_type <> 'absent') THEN 'EXTRACTED'
         WHEN EXISTS (SELECT 1 FROM source_value_extractions x
                       WHERE x.ref_id = b.ref_id AND x.parameter_id = b.parameter_id
                         AND x.claim_type = 'absent') THEN 'STATED-ABSENT'
         WHEN s.text_scope = 'full' THEN 'READ-NOTHING-FOUND'
         WHEN s.scan_id IS NOT NULL THEN 'READ-PARTIAL'
         WHEN b.processing_blocked_reason IN
              ('no-full-text', 'paywalled', 'no-doi', 'not-indexed', 'language') THEN 'BLOCKED'
         ELSE 'NOT-READ'
       END AS status,
       b.scan_id,
       s.text_scope,
       s.method
  FROM best b
  LEFT JOIN source_scans s ON s.scan_id = b.scan_id;

PRAGMA user_version = 123;
