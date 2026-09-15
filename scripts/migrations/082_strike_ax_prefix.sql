-- 082_strike_ax_prefix.sql
--
-- `AX-` IS STRUCK FROM EVERY CODE.
--
-- OWNER RULING 2026-09-15, quoted verbatim: "we should NEVER have AX- as part of a code
-- because axis is a term used to describe information", followed by "I have ruled this
-- before" and "I thought all instances of AX- had been struck". Both of those are
-- correct, and the second is the finding this migration exists to end.
--
-- THE RULING IS AT LEAST THE FOURTH ON THIS POINT:
--   2026-08-18  the owner ruled `axes` a bad coined term, marked "do not relitigate".
--               CLAUDE.md rule 0 carries this as its own worked proof, because the very
--               next day a research batch framed four of five searches on bare
--               `axis_code`.
--   2026-08-24  DR-2026-08-24 section R8 item 1: "axis" is descriptive vocabulary, never
--               a domain identifier. That DR's own table, row 1, records an implementer
--               abandoning the ruling on the grounds that it "would have overturned
--               DR-2026-07-22-work-from-axes, an ADOPTED owner directive" -- treating
--               paperwork as outranking the owner. That entry is where rule 0 comes from.
--   2026-08-25  owner ruling renaming the layer to `icf_demands` / `demand_code`. Its
--               ACTION item 3 declared the rename "scoped and owner-gated, and must not
--               be attempted piecemeal".
--   2026-09-13  "'AX-' for ICF should never ever exist anywhere", executed by migration
--               081 -- which re-pointed the ICF lens at real ICF codes but left the
--               demand registry's own 17 codes carrying the prefix.
--
-- WHY IT SURVIVED ALL FOUR, stated plainly because the mechanism will otherwise do it
-- again. The 2026-08-25 ruling made the execution owner-gated and no session ever
-- scheduled it, so the gate stopped being a safeguard and became the reason for
-- inaction: every session that met `AX-` found a ratified record saying the fix was
-- owner-gated, and stopped. Rule 0 answers this directly -- a live owner statement
-- supersedes the record it touches, ON CONTACT -- and the owner has now had to make that
-- statement four times. This migration is what "struck" means.
--
-- ============================================================================
-- THE RE-MINT
-- ============================================================================
--
-- `DM-` IS DERIVED, NOT CHOSEN. The 2026-08-25 owner ruling names the successor column
-- `icf_demands.demand_code`; `DM-` is that word's prefix. Picking a new letter pair here
-- would be inventing an identifier scheme beside a ratified one.
--
-- THE SUFFIXES ARE UNTOUCHED, and that is deliberate. `AMB`, `WHM`, `COG-L` carry the
-- meaning; the prefix carried the retired metaphor. Rewriting the suffixes as well would
-- break every frozen record's ability to be read against the live set, for no gain.
--
-- THE TRANSFORMATION IS COMPUTED FROM THE CODE, never a 17-row hand list (rule 8). A
-- hand list is a second home for the mapping and drifts from the table it describes.

UPDATE axes
   SET axis_code = 'DM-' || substr(axis_code, 4)
 WHERE axis_code GLOB 'AX-*';

-- The two maps that point at it. Their FK is to `axes(axis_code)`, and `migrate_db.py`
-- hoists `PRAGMA foreign_keys = OFF` into autocommit around the whole file, so the parent
-- and children are re-pointed inside one transaction and the end state is consistent.
-- `PRAGMA foreign_key_check` is run against the rehearsal to prove it, and the blocking
-- `validate_axes` check re-proves it on every battery run: it resolves every map code
-- against the registry, so a half-done re-mint cannot pass.

UPDATE population_axis_map
   SET axis_code = 'DM-' || substr(axis_code, 4)
 WHERE axis_code GLOB 'AX-*';

UPDATE access_need_axis_map
   SET axis_code = 'DM-' || substr(axis_code, 4)
 WHERE axis_code GLOB 'AX-*';

-- ============================================================================
-- THE LIVE PROSE THAT NAMES THE CODES
-- ============================================================================
--
-- Seven columns carry `AX-` inside sentences that INSTRUCT rather than record: a
-- falsification condition telling the next session what would merge two demands, a scope
-- note telling it which demand a term is linked to, a JSON array a renderer reads. A code
-- that no longer exists, sitting in a sentence that tells someone to use it, is the
-- "readable and wrong" failure `governance/retired-vocabulary.yaml` was built for.
--
-- REPLACE is safe on exactly these columns because `AX-` occurs in them only as the code
-- prefix -- verified against the live rows before this migration was written, not assumed.

UPDATE axes SET falsification_condition = REPLACE(falsification_condition, 'AX-', 'DM-')
 WHERE falsification_condition GLOB '*AX-*';
UPDATE axes SET notes = REPLACE(notes, 'AX-', 'DM-')
 WHERE notes GLOB '*AX-*';
UPDATE access_needs SET notes = REPLACE(notes, 'AX-', 'DM-')
 WHERE notes GLOB '*AX-*';
UPDATE access_need_axis_map SET note = REPLACE(note, 'AX-', 'DM-')
 WHERE note GLOB '*AX-*';
UPDATE access_need_icf SET note = REPLACE(note, 'AX-', 'DM-')
 WHERE note GLOB '*AX-*';
UPDATE terms SET scope_note = REPLACE(scope_note, 'AX-', 'DM-')
 WHERE scope_note GLOB '*AX-*';
UPDATE slugs SET serves_axes = REPLACE(serves_axes, 'AX-', 'DM-')
 WHERE serves_axes GLOB '*AX-*';

-- ============================================================================
-- WHAT IS DELIBERATELY LEFT CARRYING `AX-`
-- ============================================================================
--
-- FIVE VALUES IN TWO TABLES, and leaving them is the rule rather than an oversight.
--
--   `decisions.rationale` and `decisions.notes` (1 each) record what a decision SAID at
--   the time. Rewriting a decision's stated reasoning is rewriting history, and the
--   decision register is additionally a shadow store -- `test_db_integrity` L01 compares
--   it column-for-column against `data/decisions/decision_register.yaml`, so an UPDATE
--   here silently breaks a blocking parity check.
--
--   `search_executions.query_text`, `.deferred_reason` and `.findings_note` (1 each)
--   record what was actually searched and what was deliberately not. The research
--   contract's R8 is explicit: "KEEP EMPTIES … Never delete or backfill them." A search
--   log that has been edited to look correct is no longer evidence of anything.
--
-- The committed migrations under `scripts/migrations/` keep every `AX-` they have ever
-- held, for the same reason and by rule 3: they are append-only and immutable.
--
-- So `AX-` does not reach zero in this database, and it should not. What reaches zero is
-- `AX-` AS A LIVE CODE, which is what was ruled. Derive the residue rather than trusting
-- this paragraph:
--
--   select 'decisions' t union all select 'search_executions';
--
-- ============================================================================
-- AND IT CANNOT COME BACK
-- ============================================================================
--
-- FOUR RULINGS WERE NOT ENOUGH, so this stops being a thing anyone has to remember. The
-- registry gets a CHECK refusing the prefix outright -- the enforcement level CLAUDE.md
-- section 2 calls for when prose has already failed, which here it has, four times.
--
-- The CHECK is written as NOT GLOB 'AX-*' rather than as a positive 'DM-*' shape on
-- purpose: it mechanises exactly what was ruled and nothing more. A positive shape would
-- quietly also rule that every future demand code must begin `DM-`, which nobody has
-- said, and would have to be relitigated the day the layer is renamed again.
--
-- SQLite cannot ALTER a CHECK in, so the table is rebuilt. `axes` has no dependent views
-- and no AUTOINCREMENT sequence, which is why this is short -- and the recipe is still
-- migration 076's (build under a temporary name, copy, drop, rename) rather than
-- rename-aside. Migration 081's first cut used rename-aside and SQLite silently
-- re-pointed four CHILD tables' foreign keys at the temporary table it then dropped;
-- `PRAGMA foreign_key_check` called that clean, because the children held zero rows and a
-- foreign key resolves at INSERT time. `population_axis_map` and `access_need_axis_map`
-- hold 53 and 21 rows and would have been corrupted visibly rather than silently, which
-- is luck, not a reason to use the hazardous recipe.

CREATE TABLE _082_new_axes (
  axis_code        TEXT PRIMARY KEY
                   -- Owner ruling 2026-09-15, mechanised: "we should NEVER have AX- as
                   -- part of a code because axis is a term used to describe information".
                   CHECK (axis_code NOT GLOB 'AX-*'),
  name             TEXT NOT NULL,                  -- interaction-framed
  icf_b_anchors    TEXT,
  icf_d_anchors    TEXT,
  mechanism        TEXT NOT NULL,                  -- demand the environment places
  design_domains   TEXT,
  coverage_status  TEXT NOT NULL CHECK (coverage_status IN ('ESTABLISHED','PARTIAL','STUB')),
  falsification_condition TEXT NOT NULL,           -- symmetric: every demand carries one
  notes            TEXT,
  created_at       TEXT DEFAULT (datetime('now')),
  created_by_session TEXT
);

INSERT INTO _082_new_axes (axis_code, name, icf_b_anchors, icf_d_anchors, mechanism,
                           design_domains, coverage_status, falsification_condition,
                           notes, created_at, created_by_session)
     SELECT axis_code, name, icf_b_anchors, icf_d_anchors, mechanism,
            design_domains, coverage_status, falsification_condition,
            notes, created_at, created_by_session
       FROM axes;

DROP TABLE axes;

ALTER TABLE _082_new_axes RENAME TO axes;

PRAGMA user_version = 82;
