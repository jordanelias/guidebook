-- 142_deferred_acts_standing_by_cell.sql
-- SCHEMA migration (T-079 critic repairs; no data). A deferral STANDS iff the thing it defers is, now, still undone,
-- and "undone" has ONE definition per kind. Migration 141 (committed, not edited) gave v_deferred_acts three standing
-- rules that did not match the writer's, the ledger's or the owner's signal; this replaces the view and adds the one
-- view the reading arm and `db.py defer-reading` now both read.
--
-- WHAT WAS WRONG IN 141 (each reproduced on a scratch copy before this repair; cases T079-11, 12, 13, 21..25, 31)
--   mining   the arm required evidence_sources.citation_mining_status = 'deferred'. That status is ONE flag for every
--            slug and both directions, so a pass logged under ANOTHER slug set it to 'mined' and the row under the
--            first slug, still holding its deferred_reason, vanished from the age list. The typed fact lives in the
--            row: a mining deferral stands while ITS OWN deferred_reason is set, and `db.py log-mining
--            --discharge-deferral` (which clears exactly that) is what ends it.
--   reading  the arm dropped a deferral only when a full reading dated at or after it covered it, and the whole-source
--            test demanded mode = 'catalogue'. So (a) a whole-source deferral followed by targeted full readings of
--            every parameter listed forever while the verb said no reading was owed; (b) a full catalogue reading, a
--            parameter minted, and a whole-source deferral in the same minute was accepted and never listed; (c)
--            merge-parameter re-pointed an older full targeted reading onto the survivor and the deferral became
--            immortal. A deferral can only be created while no full reading covers its cell, so the date is no rule:
--            a deferral stands iff its cell is, now, owed.
--   reading  a deferral on a MERGED parameter or a SUPERSEDED source dropped out and the replacement pair lost the
--            deferral's age. The deferral of a merged parameter is its merged_into parameter's, and the deferral of a
--            superseded source is its successor's (one hop each), with the date the obligation was first recorded.
--
-- v_reading_owed is the ONE statement of "a reading is owed": a (source in scope) x (active parameter) pair of
-- v_scan_ledger that no FULL reading covers and that is not BLOCKED. Covered by a full reading is the ledger's own
-- definition (its text_scope column names the strongest covering reading, full first; a catalogue reading covers a
-- parameter that existed when it was made, a targeted one its target); BLOCKED is the ledger's "the full text could
-- not be obtained or read", which is not reading debt (scan_debt.py counts only NOT-READ and READ-PARTIAL for the
-- same reason). EXTRACTED and STATED-ABSENT pairs with no full reading are NOT excluded here: the repair keeps the
-- 141 behaviour, so they may be deferred; whether a pair accounted for by an extraction owes a full reading is an
-- owner question this migration does not decide. v_deferred_acts and db.py defer-reading read this view and neither
-- restates the predicate. What reads it: those two. What wrong thing reaches the guidebook without it: a deferral the
-- writer refuses to repeat that the age list keeps forever, or one the list hides that the ledger still owes.
--
-- STAGES v_deferred_acts spans (CLAUDE.md section 3; governance/stage-map.yaml is the home of each table's stage):
-- research (search_executions, citation_mining), evidence (evidence_sources, source_scans, reading_deferrals,
-- observed_terms), judgment (term_adjudications), base (base_parameters). 141's header called observed_terms a
-- judgment-stage table; the stage map puts it in evidence, and it is a record of what a source says, so evidence.
-- A deferral that is a pointer onto a source and a parameter crosses evidence and base only through the ledger.

DROP VIEW v_deferred_acts;

CREATE VIEW v_reading_owed AS
-- v_reading_owed: the (source, parameter) pairs whose reading is owed. One row per pair of v_scan_ledger that no FULL
-- reading covers (text_scope is the strongest covering reading's; NULL when none covers) and that the ledger does not
-- read BLOCKED. A partial, fragment or abstract reading covers nothing here, as in the ledger. Written once: the verb
-- `db.py defer-reading` asks it whether a deferral is allowed and v_deferred_acts asks it whether one still stands.
SELECT ref_id, parameter_id
  FROM v_scan_ledger
 WHERE COALESCE(text_scope, '') <> 'full'
   AND status <> 'BLOCKED';

CREATE VIEW v_deferred_acts AS
-- v_deferred_acts: every deferral that still STANDS, one row each, with the date it was first recorded.
--   kind                subject
--   search              the exec id, with its slug when it has one
--   mining              the mined ref_id and the slug
--   reading             the ref_id and the parameter (or the whole source)
--   adjudication        the observation id, its ref_id and its surface form
-- ref_id and parameter_id are the same facts as columns, so a writer asks "is this pair already deferred?" of this
-- view and cannot disagree with it (db.py defer-reading does). They are NULL where the kind has none. For a reading
-- they are the EFFECTIVE pair (see below), which is the pair the ledger owes.
-- deferred_at is the date the obligation was FIRST recorded (created_at), never the date a row was last written: a
-- re-deferral that reset the clock would hide an old obligation. An older search row carries only a date; every other
-- row, and any search logged now, a minute.
--
-- WHAT STANDS, per kind (a standing deferral is one nothing has since discharged):
--   search        EVERY deferred search. A search later run is a new row that names nothing it discharges, so a
--                 deferred search whose cell a later search covered still lists. Not derivable today.
--   mining        every citation_mining row whose OWN deferred_reason is set. The source's citation_mining_status is
--                 not read: it is one flag for every slug and both directions, so a pass for another slug sets it to
--                 'mined' while this row's deferral stands. `db.py log-mining --discharge-deferral` clears the row's
--                 deferred_reason, which is what ends it. A ref that resolves to no evidence_sources row (a lead
--                 anchor) is listed like any other. created_at is the ROW's.
--   reading       a deferral whose EFFECTIVE pair is still owed (v_reading_owed, the one definition). The effective
--                 source is the deferral's own, or its successor when the source is superseded (one hop); the
--                 effective parameter is the deferral's own, or the one it was merged into (one hop). A pair deferral
--                 stands iff its effective pair is owed; a whole-source deferral (NULL parameter) stands iff SOME
--                 active parameter of the effective source is owed. A retired parameter or a superseded successor
--                 leaves no ledger row, so it drops out. No date is read: a deferral can only be created while its
--                 cell is owed, and it stands for exactly as long as the cell is.
--   adjudication  an observation whose LATEST adjudication (highest adjudication_id, the rule alias and rename writers
--                 use) is DEFERRED: a later judgment of any other outcome discharges it.
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
 WHERE cm.deferred_reason IS NOT NULL
UNION ALL
SELECT 'reading',
       d.eff_ref || ' ' || COALESCE('parameter ' || d.eff_param, 'whole source')
         || CASE WHEN d.eff_ref <> d.ref_id OR d.eff_param IS NOT d.parameter_id
                 THEN ' (recorded for ' || d.ref_id || COALESCE(' parameter ' || d.parameter_id, ' whole source') || ')'
                 ELSE '' END,
       d.eff_ref,
       d.eff_param,
       d.reason,
       d.created_at,
       d.created_by_session
  FROM (SELECT r.*,
               COALESCE(e.superseded_by_ref_id, r.ref_id) AS eff_ref,
               CASE WHEN p.status = 'merged' THEN p.merged_into ELSE r.parameter_id END AS eff_param
          FROM reading_deferrals r
          JOIN evidence_sources e ON e.ref_id = r.ref_id
          LEFT JOIN base_parameters p ON p.parameter_id = r.parameter_id) d
 WHERE EXISTS (SELECT 1 FROM v_reading_owed o
                WHERE o.ref_id = d.eff_ref AND (d.parameter_id IS NULL OR o.parameter_id = d.eff_param))
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

PRAGMA user_version = 142;
