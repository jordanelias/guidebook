-- 093_convergence_sources_junction.sql
--
-- SIXTY-NINE POINTERS THAT WERE STRINGS, GIVEN A REAL HOME.
--
-- `convergence_assessment` records which sources converge on a determination, and it has
-- been recording them as five JSON arrays of ref_ids inside five TEXT columns:
-- clinical_sources, co1_sources, co2_sources, down_weighted_sources, discounted_sources.
-- A ref_id inside a JSON string is not a pointer. It has no foreign key, so the database
-- cannot refuse a ref that does not exist and cannot refuse one that is later retired; it
-- cannot be joined, so every reader re-parses JSON in Python; and `schema_reference_audit`
-- cannot see it at all, because there is no reference in the schema for it to check.
--
-- Measured 2026-09-20 across this table and `specifications.governing_refs`: 107 ref_ids
-- were held inside JSON strings, all 107 resolving today, none of them protected. The
-- 2026-09-13 circulation clear is the precedent that makes this urgent rather than tidy --
-- it moved the ref_id mark REF-00982 -> REF-00970 with every gate green, because the
-- database was internally consistent and the contradiction lived between the database and
-- the record of what it had held. That is exactly the failure a string cannot resist:
-- delete a source and the JSON keeps naming it, silently, forever.
--
-- WHY A JUNCTION AND NOT A WIDER COLUMN. CLAUDE.md rule 5: "It is better to have a table
-- cell point to another table cell than to rewrite." The role (clinical / co1 / co2 /
-- down_weighted / discounted) is a property of the PAIRING -- this source, in this
-- assessment, weighed this way -- not of the source and not of the assessment, so it is the
-- junction's own column. The vocabulary is declared in its CHECK, which is where a
-- vocabulary belongs (rule 8), rather than implied by which of five columns a string
-- happened to sit in.
--
-- THE JSON COLUMNS ARE NOT DROPPED, AND CANNOT BE. Seven committed data migrations INSERT
-- them, and a committed data migration is immutable (rule 3), so dropping the columns would
-- break a rebuild from history. Rule 5 names the sequence for exactly this case --
-- "writer-retire, reader-retire, NULL forward" -- and this migration is its first step:
--
--   1. (here)  create the junction and backfill every existing row from the JSON.
--   2. writer  assess_cell.py writes convergence_sources and stops writing the arrays.
--   3. reader  validate_evidence_state.py reads the junction.
--   4. forward new rows carry NULL in the five columns; the five rows written before today
--              keep their arrays, because that is what the immutable migrations say they
--              held, and the junction now says the same thing in a form that can be checked.
--
-- This is deliberately NOT a parity check between the two homes. CLAUDE.md is explicit that
-- "a parity check is not a fix -- it makes a dual home survivable, therefore permanent." The
-- junction becomes the only home a writer writes and the only home a reader reads; the
-- arrays are frozen history, not a second live copy.
--
-- AFTER_DATA: 20260920060857

CREATE TABLE convergence_sources (
    convergence_id  INTEGER NOT NULL
                    REFERENCES convergence_assessment(convergence_id),
    ref_id          TEXT    NOT NULL
                    REFERENCES evidence_sources(ref_id),
    -- The weighing is a property of the pairing, so it lives here. Vocabulary in the
    -- column's own CHECK, read by dbcore.check_values() rather than retyped by a caller.
    role            TEXT    NOT NULL
                    CHECK (role IN ('clinical', 'co1', 'co2',
                                    'down_weighted', 'discounted')),
    created_at          TEXT,
    created_by_session  TEXT,
    PRIMARY KEY (convergence_id, ref_id, role)
);

CREATE INDEX idx_convergence_sources_ref  ON convergence_sources(ref_id);
CREATE INDEX idx_convergence_sources_role ON convergence_sources(role);

-- Backfill, one INSERT per role, reading the arrays with json_each so the migration does
-- not re-list the ref_ids it is migrating. A ref_id in an array that no longer resolves to
-- evidence_sources would violate the new FK; none does today, and if one ever did the
-- migration failing loudly here is the correct outcome -- that is the whole point of the
-- constraint this table adds.
INSERT INTO convergence_sources (convergence_id, ref_id, role, created_at, created_by_session)
SELECT ca.convergence_id, je.value, 'clinical', ca.created_at, ca.created_by_session
  FROM convergence_assessment ca, json_each(ca.clinical_sources) je
 WHERE ca.clinical_sources IS NOT NULL;

INSERT INTO convergence_sources (convergence_id, ref_id, role, created_at, created_by_session)
SELECT ca.convergence_id, je.value, 'co1', ca.created_at, ca.created_by_session
  FROM convergence_assessment ca, json_each(ca.co1_sources) je
 WHERE ca.co1_sources IS NOT NULL;

INSERT INTO convergence_sources (convergence_id, ref_id, role, created_at, created_by_session)
SELECT ca.convergence_id, je.value, 'co2', ca.created_at, ca.created_by_session
  FROM convergence_assessment ca, json_each(ca.co2_sources) je
 WHERE ca.co2_sources IS NOT NULL;

INSERT INTO convergence_sources (convergence_id, ref_id, role, created_at, created_by_session)
SELECT ca.convergence_id, je.value, 'down_weighted', ca.created_at, ca.created_by_session
  FROM convergence_assessment ca, json_each(ca.down_weighted_sources) je
 WHERE ca.down_weighted_sources IS NOT NULL;

INSERT INTO convergence_sources (convergence_id, ref_id, role, created_at, created_by_session)
SELECT ca.convergence_id, je.value, 'discounted', ca.created_at, ca.created_by_session
  FROM convergence_assessment ca, json_each(ca.discounted_sources) je
 WHERE ca.discounted_sources IS NOT NULL;

-- A cross-stage pointer in view form: synthesis (convergence) reached from evidence
-- (the source and its tier), which is what "point, do not copy" looks like in SQL and is
-- the object CLAUDE.md §3 calls the most protected in the schema. It exists so a reader
-- asking "which sources, at which tiers, weighed into this assessment" has a join rather
-- than a JSON parse.
CREATE VIEW v_convergence_sources AS
SELECT cs.convergence_id,
       ca.status            AS convergence_status,
       cs.role,
       cs.ref_id,
       es.tier,
       es.evidence_type,
       es.verification_status
  FROM convergence_sources cs
  JOIN convergence_assessment ca ON ca.convergence_id = cs.convergence_id
  JOIN evidence_sources es       ON es.ref_id         = cs.ref_id;

PRAGMA user_version = 93;
