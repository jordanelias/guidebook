-- 102_observation_per_sighting.sql
-- SCHEMA migration — an observation is ONE SIGHTING: a phrase AT A PLACE in a source.
-- Tooling T1, approved by the owner 2026-10-09 ("D8 approve tooling"); catalogue-plan-v2
-- section 3.5 and critique finding F3 (scratchpad/session_2026-10-09-research-batch-24-
-- parameter-pilot/).
--
-- THE DEFECT. Migration 068 keyed `observed_terms` UNIQUE (ref_id, surface_form,
-- language), on the reasoning that "a second sighting of the same phrase in the same
-- source is the same fact", and `db.py observe-term` returned the earlier row with
-- `created: False` for any repeat. That holds for a phrase that names one thing. It is
-- false for a phrase a source uses for two quantities: the held ADA 2010 text says
-- "clear width" at a door clause and at a route clause (53 times across elements,
-- counted in the persisted HTML for the plan). The second sighting was folded into the
-- first, its locator and context quote were dropped, and the second sense was never
-- judged -- so the owner's requirement, "I expect harvesting across multiple terms if a
-- source discusses multiple terms" (2026-10-09), could not be met by the schema. Batch
-- 23's scanner had to invent an `also_at` field to carry the second place.
--
-- THE FIX. The sighting key gains the locator: UNIQUE (ref_id, surface_form, language,
-- COALESCE(locator, '')). Each sighting is judged on its own, so one sighting can name a
-- door width and another a corridor width. A deliberate second JUDGEMENT of one sighting
-- is unchanged: it is a second term_adjudications row, a contest (068's own design).
-- COALESCE because a NULL locator compares unequal to every other NULL, so without it
-- the legacy rows that carry no locator would stop deduplicating at all; with it they
-- keep exactly the old key. `observe-term` now refuses a NEW observation with no
-- locator, so the '' bucket holds only rows written before this migration.
--
-- A COPYING REBUILD, because SQLite cannot drop an inline table constraint. Same route
-- as 071 and 076: build, copy every row with its observation_id, drop, rename. The
-- inbound reference `term_adjudications.observation_id REFERENCES observed_terms` is
-- resolved by NAME at statement time, so it survives the rename; migrate_db.py hoists
-- `PRAGMA foreign_keys = OFF` around the file and restores it after. No view or trigger
-- reads this table (checked against sqlite_master before writing this), so nothing has
-- to be dropped and recreated around the rebuild.
--
-- NO ROW CHANGES. Every observation_id, every column value and the child FK are carried
-- over; the old key is strictly narrower than the new one, so no existing row can
-- collide under it. Rows written before this migration are untouched; the verbatim check
-- applies to new observations only (db.py observe-term), and
-- scripts/audit/observation_verbatim_audit.py reports the old ones against a baseline.
--
-- KNOWN PROSE CALLER, left as it is: the DDL comment inside `source_value_extractions`
-- (migration 073) describes observed_terms as "keyed UNIQUE (ref_id, surface_form,
-- language)". A table's comment can only change with a rebuild of that table, and a
-- rebuild of the extraction table for a comment is not worth its risk; this header is
-- the correction.

CREATE TABLE observed_terms_new (
    observation_id      INTEGER PRIMARY KEY,
    -- POINTER, not a copy. The source's bibliography stays in evidence_sources.
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    -- The phrase EXACTLY as the source writes it. Not normalised, not translated,
    -- not mapped. R11 forbids back-translation and this is where that starts.
    surface_form        TEXT NOT NULL,
    -- The language the phrase APPEARS IN, which need not be the source's language.
    language            TEXT NOT NULL DEFAULT 'EN',
    -- R3's locator discipline: where in the source it appears. Part of the sighting's
    -- key since migration 102 (ux_observed_terms_sighting below).
    locator             TEXT,
    -- Enough surrounding text that judgment can adjudicate without re-retrieving.
    context_quote       TEXT,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT
);

INSERT INTO observed_terms_new
    (observation_id, ref_id, surface_form, language, locator, context_quote, notes,
     created_at, created_by_session, updated_at, updated_by_session)
SELECT observation_id, ref_id, surface_form, language, locator, context_quote, notes,
       created_at, created_by_session, updated_at, updated_by_session
  FROM observed_terms;
DROP TABLE observed_terms;
ALTER TABLE observed_terms_new RENAME TO observed_terms;

-- Recreated: the rebuild dropped it with the old table.
CREATE INDEX idx_observed_terms_ref ON observed_terms(ref_id);

-- ONE SIGHTING: a phrase, in a language, at a place, in a source.
CREATE UNIQUE INDEX ux_observed_terms_sighting
    ON observed_terms(ref_id, surface_form, language, COALESCE(locator, ''));

PRAGMA user_version = 102;
