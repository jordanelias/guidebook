-- 141_reading_deferrals.sql
-- SCHEMA migration (T-079, AT-17; no data). A reading can be deferred on the record, and every deferred act lists with
-- its age from one view.
--
-- WHY. The owner (2026-09-18): a deferral is legitimate "so long as it runs eventually"; nothing in the repository
-- enforced or even measured it. A search not run and a source not mined each carried a deferral and a date; a source
-- not read had no deferred state, so "chosen not to read yet" could not be told from "nobody has looked", and no query
-- listed all of them with their age. What reaches the guidebook without it: a source whose full text is owed for a
-- parameter, deferred once, never read, and indistinguishable from one deferred last week.
--
-- reading_deferrals is a table of its own. Rejected: a source_scans row (its file_sha256 and text_scope describe a
-- reading that HAPPENED; a deferral is the opposite fact); evidence_sources.data_capture_status (one value per source,
-- no date, no reason, and a column a data migration INSERTs); a new v_scan_ledger status (the pair stays owed until it
-- is read, and every gate that reads the ledger's statuses would change meaning). A deferral is DISCHARGED BY
-- DERIVATION, never by a write: the view below drops it when a full reading covers it.
--
-- v_deferred_acts is a cross-stage pointer view (CLAUDE.md section 3): it reads research (search_executions,
-- citation_mining), evidence (evidence_sources, source_scans, reading_deferrals) and judgment (term_adjudications,
-- observed_terms), plus base (base_parameters). Nothing reads it as a gate: what age makes a standing deferral a defect
-- is the owner's to say, and no threshold is stored or typed anywhere. The age query is
--   SELECT * FROM v_deferred_acts WHERE deferred_at < datetime('now', '-<N> days') ORDER BY deferred_at;

CREATE TABLE reading_deferrals (
    deferral_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    ref_id              TEXT    NOT NULL REFERENCES evidence_sources(ref_id),
    -- NULL: the whole-source catalogue reading is what is deferred.
    parameter_id        INTEGER REFERENCES base_parameters(parameter_id),
    reason              TEXT    NOT NULL CHECK (trim(reason) <> ''),
    created_at          TEXT    NOT NULL,
    created_by_session  TEXT    NOT NULL
);

CREATE VIEW v_deferred_acts AS
-- v_deferred_acts: every deferral that still STANDS, one row each, with the date it was first recorded.
--   kind                subject
--   search              the exec id, with its slug when it has one
--   mining              the mined ref_id and the slug
--   reading             the ref_id and the parameter (or the whole source)
--   adjudication        the observation id, its ref_id and its surface form
-- ref_id and parameter_id are the same facts as columns, so a writer asks "is this pair already deferred?" of this
-- view and cannot disagree with it (db.py defer-reading does). They are NULL where the kind has none.
-- deferred_at is the date the obligation was FIRST recorded (created_at), never the date a row was last written: a
-- re-deferral that reset the clock would hide an old obligation. An older search row carries only a date; every other
-- row, and any search logged now, a minute.
--
-- WHAT EACH ARM DROPS, and why (a standing deferral is one nothing has since discharged):
--   search        NOTHING. A search later run is a new row that names nothing it discharges, so every deferred
--                 search lists, including one whose cell a later search has since covered. Not derivable today.
--   mining        a row whose source's citation_mining_status is no longer 'deferred' (the owner's execution signal,
--                 2026-09-18: db.py log-mining --discharge-deferral clears the row and the status together). A row whose
--                 ref resolves to no evidence_sources row (a lead anchor) has no status to read and lists while its own
--                 deferred_reason stands. created_at is the ROW's: a row first written by a pass that ran and deferred
--                 later is dated from the pass.
--   reading       a deferral whose source is now superseded (the replacement is what is owed) or whose parameter is no
--                 longer active (the ledger drops it), and one a FULL reading dated at or after the deferral covers:
--                 for a parameter, the strongest covering reading v_scan_ledger names is full-scope; for a NULL
--                 parameter, any full catalogue reading. Dates are minute-resolution, so "at or after".
--   adjudication  an observation whose LATEST adjudication (highest adjudication_id, the rule alias and rename writers
--                 use) is not DEFERRED: a later judgment of any other outcome discharges it.
SELECT 'search' AS kind,
       'exec ' || se.exec_id || COALESCE(' ' || se.slug, '') AS subject,
       se.mined_ref_id AS ref_id,
       se.parameter_id AS parameter_id,
       se.deferred_reason AS reason,
       se.created_at AS deferred_at,
       se.created_by_session AS created_by_session
  FROM search_executions se
 WHERE se.deferred_reason IS NOT NULL
UNION ALL
SELECT 'mining',
       COALESCE(cm.global_ref_id, cm.local_ref_id) || ' ' || cm.slug,
       COALESCE(cm.global_ref_id, cm.local_ref_id),
       NULL,
       cm.deferred_reason,
       cm.created_at,
       cm.created_by_session
  FROM citation_mining cm
  LEFT JOIN evidence_sources e ON e.ref_id = COALESCE(cm.global_ref_id, cm.local_ref_id)
 WHERE cm.deferred_reason IS NOT NULL
   AND (e.ref_id IS NULL OR e.citation_mining_status = 'deferred')
UNION ALL
SELECT 'reading',
       d.ref_id || ' ' || COALESCE('parameter ' || d.parameter_id, 'whole source'),
       d.ref_id,
       d.parameter_id,
       d.reason,
       d.created_at,
       d.created_by_session
  FROM reading_deferrals d
  JOIN evidence_sources e ON e.ref_id = d.ref_id AND e.superseded_by_ref_id IS NULL
 WHERE (d.parameter_id IS NULL
        OR EXISTS (SELECT 1 FROM base_parameters p
                    WHERE p.parameter_id = d.parameter_id AND p.status = 'active'))
   AND NOT EXISTS (
         SELECT 1
           FROM source_scans s
          WHERE s.ref_id = d.ref_id AND s.text_scope = 'full' AND s.created_at >= d.created_at
            AND CASE WHEN d.parameter_id IS NULL
                     THEN s.mode = 'catalogue'
                     ELSE s.scan_id = (SELECT l.scan_id FROM v_scan_ledger l
                                        WHERE l.ref_id = d.ref_id AND l.parameter_id = d.parameter_id
                                          AND l.text_scope = 'full') END)
UNION ALL
SELECT 'adjudication',
       'observation ' || o.observation_id || ' ' || o.ref_id || ' ' || o.surface_form,
       o.ref_id,
       NULL,
       a.rationale,
       a.created_at,
       a.created_by_session
  FROM term_adjudications a
  JOIN observed_terms o ON o.observation_id = a.observation_id
 WHERE a.outcome = 'DEFERRED'
   AND a.adjudication_id = (SELECT MAX(b.adjudication_id) FROM term_adjudications b
                             WHERE b.observation_id = a.observation_id);

PRAGMA user_version = 141;
