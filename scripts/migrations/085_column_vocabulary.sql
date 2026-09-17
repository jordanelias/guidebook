-- 085_column_vocabulary.sql
--
-- ONE ROLE, ONE COLUMN NAME.
--
-- WHAT WENT WRONG THAT MADE THIS WORTH DOING. `tools/pipeline_walk.py` shipped a
-- session-attribution helper matching two column names, `created_by_session` and
-- `session`. The corpus spells that ONE role eight ways, so the tool reported
-- fifteen tables -- including `source_locators`, 893 rows, the largest table it
-- places -- as "not attributable to a session". The defect was not in the tool.
-- It was here, in the schema, and nothing named it, so every new reader
-- rediscovers it by being wrong first. `scripts/audit/column_vocabulary_audit.py`
-- is the check that now names it; this migration is what makes that check pass.
--
-- WHAT IS RENAMED AND WHAT IS NOT. A role may legitimately appear under several
-- names when the columns record DIFFERENT events: `raised_by_session` and
-- `resolved_by_session` on `determination_gates` are two moments in one row's
-- life, not two spellings of one moment, and they are untouched. Renamed here are
-- only columns holding exactly what the majority spelling holds -- a domain verb
-- decorating the one fact "which session made this row, and when".
--
-- THE ORDERING MARKER IS LOAD-BEARING, NOT DECORATION. `session` appears in the
-- explicit column lists of twelve committed data migrations and `executed_at` in
-- nine. Migrations are append-only and immutable (CLAUDE.md rule 3), so those
-- INSERT statements can never be edited to the new names -- and
-- `migrate_db.py --rebuild` replays them. Without the marker below, a rebuild
-- would apply this rename first and then fail on twenty-one old INSERTs forever.
-- AFTER_DATA says: this migration, and every one numbered after it, applies only
-- once the data migrations up to that timestamp have replayed. That is the real
-- chronology, which the numbered/timestamped split cannot otherwise express.
-- The timestamp is the newest data migration on disk at the time of writing.
--
-- AFTER_DATA: 20260916233024
--
-- WHAT IS DELIBERATELY EXEMPT, with the reason, so the audit's exemption is not
-- mistaken for an oversight:
--
--   `data_migrations.applied_at` and `.applied_by_session` are drift by the same
--   definition and are NOT renamed, because renaming them is unrunnable.
--   `migrate_db.py` writes `INSERT INTO data_migrations (migration_id,
--   applied_at, content_sha, ...)` at three call sites DURING the run that would
--   apply this migration. Rename the column and the run that renames it cannot
--   record itself; update the writer first and it breaks before this migration
--   exists to be applied. That is a genuine bootstrap, not a preference, and the
--   audit records it as an exemption rather than a pending item.
--
-- THREE DROPS, NOT RENAMES. Three tables carry BOTH spellings of one fact, which
-- is rule 5 literally -- two homes for one value. A rename would collide, so the
-- redundant column goes. All three tables hold ZERO rows (verified immediately
-- before writing this), none of the three columns is named by any index or view,
-- and no row's provenance is destroyed. The owner ruling of 2026-09-16 ("retire
-- in place, never hard-delete") governs DATA ROWS AND IDENTIFIERS and says so in
-- its own text; an empty duplicate column is apparatus, which CLAUDE.md §8 is
-- removal-friendly about.

-- ---------------------------------------------------------------------------
-- Role: which session created this row  ->  created_by_session
-- ---------------------------------------------------------------------------
ALTER TABLE gap_mining              RENAME COLUMN attempted_by_session TO created_by_session;
ALTER TABLE supersession_check      RENAME COLUMN checked_by_session   TO created_by_session;
ALTER TABLE pipeline_runs           RENAME COLUMN run_by_session       TO created_by_session;
ALTER TABLE url_verification_runs   RENAME COLUMN run_by_session       TO created_by_session;
ALTER TABLE search_candidates       RENAME COLUMN session              TO created_by_session;
ALTER TABLE search_executions       RENAME COLUMN session              TO created_by_session;
ALTER TABLE reasoning_doc_citations RENAME COLUMN verified_by_session  TO created_by_session;
ALTER TABLE source_locators         RENAME COLUMN worked_by_session    TO created_by_session;

-- ---------------------------------------------------------------------------
-- Role: when this row was created  ->  created_at
-- `gap_mining.attempt_at` was not even past tense beside its own row's
-- `attempted_by_session`, which is how little held this vocabulary together.
-- ---------------------------------------------------------------------------
ALTER TABLE gap_mining              RENAME COLUMN attempt_at  TO created_at;
ALTER TABLE supersession_check      RENAME COLUMN checked_at  TO created_at;
ALTER TABLE search_executions       RENAME COLUMN executed_at TO created_at;
ALTER TABLE source_locators         RENAME COLUMN worked_at   TO created_at;

-- ---------------------------------------------------------------------------
-- Role: free text about the row  ->  notes
-- A singular/plural split across 41 tables with no rule behind it: 33 said
-- `notes`, 8 said `note`.
-- ---------------------------------------------------------------------------
ALTER TABLE access_need_axis_map        RENAME COLUMN note TO notes;
ALTER TABLE access_need_icf             RENAME COLUMN note TO notes;
ALTER TABLE citation_population_links   RENAME COLUMN note TO notes;
ALTER TABLE extraction_population_links RENAME COLUMN note TO notes;
ALTER TABLE icf_medical_map             RENAME COLUMN note TO notes;
ALTER TABLE identity_medical_map        RENAME COLUMN note TO notes;
ALTER TABLE population_axis_map         RENAME COLUMN note TO notes;
ALTER TABLE probe_population_links      RENAME COLUMN note TO notes;

-- ---------------------------------------------------------------------------
-- Two homes for one fact, in one table, on an empty table: drop the duplicate.
-- ---------------------------------------------------------------------------
ALTER TABLE item_audit_runs DROP COLUMN session;         -- beside created_by_session
ALTER TABLE connections     DROP COLUMN session_applied; -- beside created_by_session
ALTER TABLE bpc_metadata    DROP COLUMN last_updated;    -- beside updated_at

PRAGMA user_version = 85;
