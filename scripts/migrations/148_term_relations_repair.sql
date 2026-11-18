-- 148_term_relations_repair.sql
-- SCHEMA migration -- a compensating migration for 147_term_relations (T-029; 147 is committed and is not edited).
-- Tooling, no research rows. The table holds no rows when this runs, and the copy below carries any it holds.
-- Rebuilt by create, copy, drop, rename, because SQLite cannot change a CHECK in place.
--
-- WHAT CHANGES, each the repair of a defect the adversarial pass found in 147:
--  1. THE RETIREMENT CHECK. 147's form `length(trim(retirement_reason)) > 0` is NULL when the reason is NULL, and a
--     CHECK that evaluates to NULL passes, so a row retired with a session and no reason was accepted. The three cells
--     now follow the siblings' form (search_admissions, connections: `(a IS NULL) = (b IS NULL)`), and a non-blank guard
--     that cannot be NULL-passed (the equalities make the other two cells non-NULL whenever retired_at is).
--  2. `element has provision` takes no adjudication warrant. OD-56 names the source statements that say an element
--     should carry a provision: observation rows and extraction rows. T-029's file names the same two.
--  3. `reason` is nullable (its blank is still refused). T-029's file names a warrant and no reason cell; T-129's design
--     (section A6) sets a `distinct` row's reason to the rationale text, which its warrant adjudication already holds.
--     Whether the cell survives is a design question recorded in the commit; until it is answered the cell may be empty.
--  4. `distinct` is stored with the lower term id first, compared by the number after the id's hyphen (TERM-999 is below
--     TERM-1000), the text only breaking a tie. The writer derives the same key from the id's own form.
-- Everything else is 147's, unchanged: the kinds, the warrant (exactly one pointer), and the one live row per unordered
-- pair per kind.

CREATE TABLE _148_term_relations (
    relation_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    from_term_id        TEXT NOT NULL REFERENCES terms(term_id),
    kind                TEXT NOT NULL
                        CHECK (kind IN ('broader', 'part of', 'element has parameter', 'element has provision',
                                        'adjacent', 'distinct')),
    to_term_id          TEXT NOT NULL REFERENCES terms(term_id),
    reason              TEXT CHECK (reason IS NULL OR length(trim(reason)) > 0),
    observation_id      INTEGER REFERENCES observed_terms(observation_id),
    extraction_id       INTEGER REFERENCES source_value_extractions(extraction_id),
    adjudication_id     INTEGER REFERENCES term_adjudications(adjudication_id),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    retired_at          TEXT,
    retired_by_session  TEXT,
    retirement_reason   TEXT,
    CHECK (from_term_id <> to_term_id),
    CHECK ((observation_id IS NOT NULL) + (extraction_id IS NOT NULL) + (adjudication_id IS NOT NULL) = 1),
    CHECK (kind <> 'element has provision' OR adjudication_id IS NULL),
    CHECK (kind <> 'distinct'
           OR CAST(substr(from_term_id, instr(from_term_id, '-') + 1) AS INTEGER)
              < CAST(substr(to_term_id, instr(to_term_id, '-') + 1) AS INTEGER)
           OR (CAST(substr(from_term_id, instr(from_term_id, '-') + 1) AS INTEGER)
               = CAST(substr(to_term_id, instr(to_term_id, '-') + 1) AS INTEGER)
               AND from_term_id < to_term_id)),
    CHECK ((retired_at IS NULL) = (retired_by_session IS NULL) AND (retired_at IS NULL) = (retirement_reason IS NULL)),
    CHECK (retired_at IS NULL OR (length(trim(retired_at)) > 0 AND length(trim(retired_by_session)) > 0
                                  AND length(trim(retirement_reason)) > 0))
);

INSERT INTO _148_term_relations (relation_id, from_term_id, kind, to_term_id, reason, observation_id, extraction_id,
                                 adjudication_id, created_at, created_by_session, retired_at, retired_by_session,
                                 retirement_reason)
SELECT relation_id, from_term_id, kind, to_term_id, reason, observation_id, extraction_id, adjudication_id,
       created_at, created_by_session, retired_at, retired_by_session, retirement_reason
  FROM term_relations;

DROP TABLE term_relations;
ALTER TABLE _148_term_relations RENAME TO term_relations;

CREATE UNIQUE INDEX ux_term_relations_live_pair
    ON term_relations (kind, min(from_term_id, to_term_id), max(from_term_id, to_term_id))
 WHERE retired_at IS NULL;

PRAGMA user_version = 148;
