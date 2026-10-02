-- 101_parameter_declinations.sql
-- SCHEMA migration — GAP-061 prerequisite (process-gap remediation plan, T1 / WP1).
--
-- THE GAP. A term that judgment has named (a NAMES-NEW or NAMES-EXISTING adjudication)
-- has had exactly one recordable fate: promotion to `base_parameters` through
-- `db.py add-parameter`. A term that names something other than a quantity under
-- determination -- a population lens term such as 'wheelchair user', an element such as
-- 'ramp' whose quantities are separate terms, a method -- had no disposition at all. So
-- "not yet looked at" and "looked at and judged not a parameter" read identically, and a
-- contract rule requiring every adjudicated term on a batch's admissions to be disposed
-- of could never go green on such a term. This table records the second answer.
--
-- A SEPARATE TABLE, NOT A `base_parameters.status` VALUE. A declined term must never hold
-- a `parameter_id`: an extraction (`source_value_extractions.parameter_id`) or a
-- determination (`specifications.parameter_id`) could then point at a concept judged not
-- to be a parameter, with only a status column saying so. Here there is no parameter_id
-- to point at.
--
-- STAGE: base -- the negative space of the parameter registry. Its reader is base's own
-- writer: `insert_parameter` (db.py add-parameter) refuses a declined term. One row per
-- term (the PRIMARY KEY), and `db.py decline-parameter` refuses a second declination by
-- naming the standing one. There is no un-decline verb: reversing a declination is a
-- recorded decision plus a compensating migration, and nothing reads an un-decline yet
-- (CLAUDE.md section 8).
--
-- `reason` IS CHECKED IN THE SCHEMA as well as by the writer (`dbcore.require_reason`):
-- a declination that cannot say why cannot be contested, and an invariant worth a
-- writer refusal is worth holding for every future writer and every data migration --
-- the precedent migration 097 set for its own CHECKs.
--
-- SCHEMA ONLY, NO ROWS, NO BACKFILL. Which terms to decline is a judgement, made per term
-- with its reason, and this migration ships in a tooling PR (CLAUDE.md rule 10). Rows
-- arrive through the ordinary capture path: `dbcore.writable_tables()` derives this table
-- from the writer's own INSERT literal, so no capture list is edited.

CREATE TABLE parameter_declinations (
    term_id            TEXT PRIMARY KEY REFERENCES terms(term_id),
    reason             TEXT NOT NULL CHECK (length(trim(reason)) > 0),
    created_at         TEXT NOT NULL,
    created_by_session TEXT NOT NULL
);

PRAGMA user_version = 101;
