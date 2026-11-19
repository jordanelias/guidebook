-- 158_figure_retire_in_place.sql
-- SCHEMA migration (T-078; AT-18, REQ-018). No data rows. A figure retires in place under the owner's ruling of
-- 2026-09-16, "retire in place then" (grep -n -F 'retire in place then' references/project-standards.md): a wrong
-- figure (misread, superseded by a correction, filed against the wrong parameter) stays a row, with when, by whom and
-- why it was withdrawn, instead of being hard-deleted as data_20260913040739_2026-09-13-clear-circulation-corpus.sql did.
--
-- 1. `source_value_extractions` gains `retired_at`, `retired_by_session` and `retirement_reason`, nullable, in the shape
--    T-050 gave `search_admissions` and `connections` (migration 145) and `term_relations` carries: the three set
--    together or not at all, and none blank once set. The CHECK sits on the last column, because SQLite adds a column
--    by ALTER and a column constraint may name its siblings. Retirement is not a value of `extraction_status` (that
--    cell says how far a figure has been reviewed; one cell holds one fact, owner 2026-11-06).
-- 2. One trigger refuses changing `retired_at` once it is set (no un-retiring in place: a wrong retirement is answered
--    by a new figure). The CHECK cannot hold that, since clearing all three cells satisfies it.
-- 3. THE RULING'S EXECUTION CONDITION: "No row is retired in place until every reader that could surface it filters on
--    status." The views that read figures, from their current text in sqlite_master, decided one by one:
--      v_live_lens_links          FILTERS: a link of a retired figure is not live. Every reader of the view inherits
--                                 it (the engine's _lens_clause, count_extractions and gathers, cell-status, the lens
--                                 audits, batch-done); the link rows themselves stay, unretired (rule 5: the figure's
--                                 withdrawal is held once, on the figure).
--      v_scan_ledger              FILTERS: EXTRACTED and STATED-ABSENT are earned by live figures only, so a pair whose
--                                 only figure is retired goes back to its reading status.
--      v_value_independence       FILTERS: independent roots are counted over live figures.
--      v_unregistered_roots       FILTERS: a withdrawn figure's root is not a defect to repair.
--      v_root_id_conflicts        FILTERS: a withdrawn figure's root attribution is not a live conflict.
--      v_coverage_parameter_via_admission  FILTERS (the `reached` CTE): a search reaches a parameter through a figure
--                                 a source states, and a retired figure is not stated.
--      v_determination_provenance KEEPS HISTORY, unchanged: it lists what each live determination was built from, and
--                                 db.py retire-extraction refuses a figure a live determination links, so a retired
--                                 figure appears there only under a determination that was itself retired first.
--      v_derived_figure_check     KEEPS HISTORY, unchanged: it re-verifies the arithmetic of every derived row ever
--                                 written (extraction_relations_integrity's subject is every edge); a retired row's
--                                 arithmetic stays checkable.
--    No trigger reads figures (derive: select name from sqlite_master where type='trigger').
-- WRITER: db.py retire-extraction. READERS fixed in the same change: db.py (cell-status, add-extraction's copy check,
-- set-parameter-direction), scripts/assess/assess_cell.py (gather_extraction_links, the out-of-lens count,
-- gather_confirmers), verified_scan_integrity, research_batch_dod R3, adjudication_integrity, test_db_integrity K02 and
-- T018-05. ORDER: migration 131's AFTER_DATA marker places this after every committed data migration.

ALTER TABLE source_value_extractions ADD COLUMN retired_at TEXT;
ALTER TABLE source_value_extractions ADD COLUMN retired_by_session TEXT;
ALTER TABLE source_value_extractions ADD COLUMN retirement_reason TEXT
  CHECK ((retired_at IS NULL) = (retired_by_session IS NULL) AND (retired_at IS NULL) = (retirement_reason IS NULL)
         AND (retired_at IS NULL OR (length(trim(retired_at)) > 0 AND length(trim(retired_by_session)) > 0
                                     AND length(trim(retirement_reason)) > 0)));

CREATE TRIGGER trg_sve_retirement_is_final
BEFORE UPDATE OF retired_at ON source_value_extractions
WHEN OLD.retired_at IS NOT NULL AND NEW.retired_at IS NOT OLD.retired_at
BEGIN
    SELECT RAISE(ABORT, 'a retired figure stays retired -- a wrong retirement is answered by a new figure (db.py add-extraction), never by clearing retired_at');
END;

DROP VIEW v_live_lens_links;
CREATE VIEW v_live_lens_links AS
SELECT k.link_id, k.extraction_id, k.identity_code, k.icf_code, k.needs_code,
       k.basis, k.basis_text, k.basis_reason, k.created_at, k.created_by_session
  FROM extraction_lens_links k
  JOIN source_value_extractions x ON x.extraction_id = k.extraction_id AND x.retired_at IS NULL
 WHERE k.retired_at IS NULL;

DROP VIEW v_scan_ledger;
CREATE VIEW v_scan_ledger AS
-- v_scan_ledger: one row per (source in scope) x (active parameter).
--
--   source in scope   evidence_sources with superseded_by_ref_id IS NULL. A tombstone is
--                     never read again; its replacement is.
--   active parameter  base_parameters.status = 'active'. Retired and merged parameters
--                     leave the ledger (their extractions stay, as history).
--
-- STATUS PRECEDENCE, first match wins:
--   1 EXTRACTED          a live (not retired, migration 158) non-absent extraction exists for the pair
--                        (any figure_role).
--   2 STATED-ABSENT      only live claim_type 'absent' extractions exist: the source addresses
--                        the quantity and sets nothing -- a positive statement.
--   3 READ-NOTHING-FOUND a FULL-scope reading covers the pair and found no row.
--   4 BLOCKED            no full reading covers the pair AND the source carries an obstacle
--                        processing_blocked_reason (below): the full text could not be
--                        obtained or read, so the pair is not reading debt until a full
--                        reading is recorded. Any partial / fragment / abstract reading of
--                        the pair is still named in scan_id / text_scope / method.
--   5 READ-PARTIAL       only partial / fragment / abstract readings cover it, and no
--                        obstacle stands: the full text is obtainable and unread -- debt.
--   6 NOT-READ           no reading covers it.
-- WHY THIS ORDER (it is derived from what each fact proves; 122 ranked BLOCKED above every
-- reading and 123 below every reading, both guesses): a FULL reading proves the obstacle
-- gone, since the whole text was read, so 3 outranks 4. A partial, fragment or abstract
-- reading proves nothing about the full text, so under a standing obstacle 4 outranks 5.
-- A reading COVERS a pair when it is catalogue-mode with catalogue_version >= parameter_id
-- (the parameter existed when the reading was made), or targeted at that parameter. Rows 1
-- and 2 win over readings because a row written is stronger evidence than a reading
-- recorded; 3 wins over the rest because a full reading supersedes a partial one.
--
-- THE BLOCKED CASE BELOW IS THE ONE HOME of "the text could not be obtained or read", and
-- this header is the ONE HOME of the classification of every processing_blocked_reason
-- value (evidence_sources CHECK, migration 091); each value appears here as a bare token
-- under exactly one head, and a test derives the CHECK and fails on a value this header
-- does not name. The writers and gates read this view's status, never the column. NOTHING
-- CLEARS THE COLUMN: it is the retrieval record and stays as history; the ledger alone says
-- whether a pair is still blocked.
--   obstacle to the text (BLOCKED, above):  no-full-text, paywalled, language.
--   copy of a typed fact (not an obstacle; the writers refuse it by pointer -- the judgement
--     lives in db.py _BLOCK_REASON_COPIES): no-quantified-claims -> a recorded full reading;
--     superseded -> superseded_by_ref_id.
--   pending owner question 8 of the round-3 adjudication, treated as NULL (the source owes
--     its reading): out-of-scope, tier-not-required (they say no text was unobtainable);
--     no-doi, not-indexed (migration 091's comments describe discovery -- "no resolvable
--     identifier for automated paths", "absent from the indexes the pipeline queries" --
--     not an obstacle to a text in hand, and a URL-only report admitted without a DOI can
--     be read).
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
                         AND x.claim_type <> 'absent' AND x.retired_at IS NULL) THEN 'EXTRACTED'
         WHEN EXISTS (SELECT 1 FROM source_value_extractions x
                       WHERE x.ref_id = b.ref_id AND x.parameter_id = b.parameter_id
                         AND x.claim_type = 'absent' AND x.retired_at IS NULL) THEN 'STATED-ABSENT'
         WHEN s.text_scope = 'full' THEN 'READ-NOTHING-FOUND'
         WHEN b.processing_blocked_reason IN
              ('no-full-text', 'paywalled', 'language') THEN 'BLOCKED'
         WHEN s.scan_id IS NOT NULL THEN 'READ-PARTIAL'
         ELSE 'NOT-READ'
       END AS status,
       b.scan_id,
       s.text_scope,
       s.method
  FROM best b
  LEFT JOIN source_scans s ON s.scan_id = b.scan_id;

DROP VIEW v_value_independence;
CREATE VIEW v_value_independence AS
    SELECT sve.parameter_id,
           t.canonical_en AS parameter_label,
           COUNT(DISTINCT COALESCE(sve.root_ref_id, sve.root_id)) AS independent_root_count
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_type IN ('measurement_primary', 'participatory_finding',
                            'derived_calculation')
      AND (sve.root_ref_id IS NOT NULL
           OR sve.root_id IN (SELECT root_id FROM external_root_registry))
      -- 104: active parameters only; a retired parameter's extractions are history.
      AND p.status = 'active'
      -- 158: live figures only; a retired figure is history.
      AND sve.retired_at IS NULL
    GROUP BY sve.parameter_id, t.canonical_en;

DROP VIEW v_unregistered_roots;
CREATE VIEW v_unregistered_roots AS
    SELECT sve.extraction_id,
           sve.slug,
           sve.parameter_id,
           t.canonical_en AS parameter_label,
           sve.root_id,
           'unregistered' AS defect
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
                           AND p.status = 'active'
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_id IS NOT NULL
      AND sve.root_ref_id IS NULL
      AND sve.retired_at IS NULL
      AND NOT EXISTS (
          SELECT 1 FROM external_root_registry err
          WHERE err.root_id = sve.root_id)

    UNION ALL

    SELECT sve.extraction_id,
           sve.slug,
           sve.parameter_id,
           t.canonical_en AS parameter_label,
           sve.root_id,
           'rootless' AS defect
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
                           AND p.status = 'active'
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_id IS NULL
      AND sve.root_ref_id IS NULL
      AND sve.retired_at IS NULL
      AND sve.root_type IS NOT NULL
      AND sve.root_type NOT IN ('untraced', 'derived_calculation');

DROP VIEW v_root_id_conflicts;
CREATE VIEW v_root_id_conflicts AS
    SELECT 'ref_id_has_multiple_root_ids' AS conflict_type,
           root_ref_id AS conflict_key,
           COUNT(DISTINCT root_id) AS distinct_count
    FROM source_value_extractions
    WHERE root_ref_id IS NOT NULL AND root_id IS NOT NULL AND retired_at IS NULL
    GROUP BY root_ref_id HAVING COUNT(DISTINCT root_id) > 1
    UNION ALL
    SELECT 'root_id_spans_multiple_ref_ids' AS conflict_type,
           root_id AS conflict_key,
           COUNT(DISTINCT root_ref_id) AS distinct_count
    FROM source_value_extractions
    WHERE root_ref_id IS NOT NULL AND root_id IS NOT NULL AND retired_at IS NULL
    GROUP BY root_id HAVING COUNT(DISTINCT root_ref_id) > 1;

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
   WHERE x.claim_type <> 'absent' AND COALESCE(x.extraction_method, '') <> 'skim' AND x.retired_at IS NULL)
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

PRAGMA user_version = 158;
