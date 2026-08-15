-- 058_status_vocabulary_ratification.sql
-- SCHEMA migration — ratify one status vocabulary across decisions and conflicts.
--
-- Owner ruling 2026-08-14, given in three parts:
--
--   1. "ADOPT RETIRED, DROP WITHDRAWN"
--   2. "PROPOSED = PROVISIONAL FOR ME IN THIS PROJECT"
--   3. "RESOLVED-EVIDENCE AND RESOLVED-CONSENSUS ARE ONLY TO BE USED FOR DIRECT
--       EVIDENCE OR CLAIMS DIRECTLY DERIVED FROM THEM. OTHERWISE 'CLOSED' FOR
--       ITEMS LIKE FINISHED INFRASTRUCTURE ITEMS"
--   4. "DEFERRED IS DIFFERENT THAN OPEN BECAUSE IT ALLOWS US TO TELL (AND
--       POSSIBLY WITH A COUNTER) HOW MANY TIMES WE HAVE CHOSEN TO NOT ADDRESS IT"
--   5. "THEN REPLACE 'OPEN' WITH 'ACTIVE'. ONLY ONE SURVIVES"
--
-- THE RATIFIED WORDS
--   ACTIVE              live; not yet closed or resolved (replaces OPEN)
--   PROPOSED            put forward, not yet in force (absorbs PROVISIONAL)
--   DEFERRED            deliberately not addressed this pass — countable
--   RESOLVED-EVIDENCE   resolved by direct evidence
--   RESOLVED-CONSENSUS  resolved by claims directly derived from direct evidence
--   UNRESOLVED          worked and could not be resolved at this scale
--   CLOSED              finished without an evidence resolution (e.g. infrastructure)
--   RETIRED             removed from force without a successor (replaces WITHDRAWN)
--
-- WHAT THIS FIXES. The two layers policing these fields disagreed. The database
-- accepted WITHDRAWN and rejected RETIRED; schemas/enums.py did the reverse, so
-- which word was legal depended on whether the write went through Python or SQL.
-- On conflicts the sets shared 2 words of 5. Zero rows used any contested value,
-- which is why nothing had failed yet and why this costs one migration today.
--
-- ONE SHARED LIST ON BOTH TABLES, not per-field subsets. The ruling names a flat
-- set of words for the project rather than two lists, and a superset is the
-- reversible direction: narrowing later is a forward migration, while a too-narrow
-- CHECK refuses a legitimate write the moment someone makes one.
--
-- RETIRED SPELLINGS, and why each one goes:
--   WITHDRAWN            -> RETIRED             owner ruling 1; 0 rows
--   PROVISIONAL          -> PROPOSED            owner ruling 2; 1 row (D-0139)
--   OPEN                 -> ACTIVE              owner ruling 5; file layer only
--   SUPERSEDED           -> CLOSED              0 rows. Not named in the ratified
--                                               list. The relation it encoded is
--                                               already carried by decisions.supersedes,
--                                               which every row populates, so the
--                                               status word was a second spelling
--                                               of a fact the table already held.
--   RESOLUTION-PROPOSED  -> PROPOSED            direct synonym; no meaning change
--   MODE-S-ONLY          -> UNRESOLVED          "Mode S" was retired as vocabulary
--   UNRESOLVABLE-MODE-S  -> UNRESOLVED          on 2026-07-21 in favour of "Person
--                                               Mode" (governance/evidence-architecture.md
--                                               §7 normalization table). The database
--                                               CHECK was still enforcing the retired
--                                               spelling. The Person-Mode handoff that
--                                               MODE-S-ONLY carried is not lost: it
--                                               lives in mode_s_trigger /
--                                               unresolvable_residual, which is where
--                                               the handoff belongs. The status says
--                                               "not resolvable at population scale";
--                                               the handoff field says what the OT
--                                               assesses.
--
-- REPLAY ORDERING. migrate_db.py applies ALL schema migrations, then ALL data
-- migrations (see 055's header and 025's, which both hit this). D-0139's
-- PROVISIONAL value arrives in the schema phase — it is an INSERT inside the 057
-- baseline — so it is already present when this file runs and is remapped inline
-- below. It cannot be fixed by a paired data migration: that would replay after
-- this CHECK exists and the rebuild would already have failed.
--
-- The remap is deliberately narrow. WITHDRAWN and SUPERSEDED were verified at 0
-- rows before authoring, so no CASE arm is written for them: if either ever
-- appears in replay the copy fails loudly, which is the correct outcome for a
-- value nobody ratified.
--
-- No view references either table (v_root_id_conflicts reads
-- source_value_extractions and merely has "conflicts" in its name), and no
-- foreign key points at either, so the 039 drop-and-recreate-views dance is not
-- needed here. Verified against the live schema rather than assumed.

PRAGMA foreign_keys = OFF;

-- ---------- decisions ----------

CREATE TABLE _new_decisions (
    decision_id         TEXT PRIMARY KEY,
    category            TEXT NOT NULL
                        CHECK(category IN (
                            'D-DOCT','D-METH','D-SCHEMA','D-OP','D-PRES'
                        )),
    delegation          TEXT NOT NULL
                        CHECK(delegation IN ('DG-NON','DG-REVIEW','DG-AUTO')),
    delegation_rationale TEXT,
    summary             TEXT NOT NULL,
    outcome             TEXT NOT NULL,
    rationale           TEXT NOT NULL,
    decision_date       TEXT NOT NULL,
    decided_by          TEXT NOT NULL,
    model_routing       TEXT NOT NULL,
    effort_level        INTEGER NOT NULL,
    status              TEXT NOT NULL DEFAULT 'ACTIVE'
                        CHECK(status IN (
                            'ACTIVE','PROPOSED','DEFERRED','RESOLVED-EVIDENCE',
                            'RESOLVED-CONSENSUS','UNRESOLVED','CLOSED','RETIRED'
                        )),
    review_status       TEXT NOT NULL,
    supersedes          TEXT NOT NULL DEFAULT '[]',
    predecessors        TEXT NOT NULL DEFAULT '[]',
    decision_artifacts  TEXT NOT NULL DEFAULT '[]',
    alternatives_considered TEXT NOT NULL DEFAULT '[]',
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

INSERT INTO _new_decisions
SELECT decision_id, category, delegation, delegation_rationale, summary,
       outcome, rationale, decision_date, decided_by, model_routing,
       effort_level,
       CASE status WHEN 'PROVISIONAL' THEN 'PROPOSED' ELSE status END,
       review_status, supersedes, predecessors, decision_artifacts,
       alternatives_considered, notes, created_at, created_by_session,
       updated_at, updated_by_session
FROM decisions;

DROP TABLE decisions;
ALTER TABLE _new_decisions RENAME TO decisions;

CREATE INDEX idx_decision_status   ON decisions(status);
CREATE INDEX idx_decision_category ON decisions(category);

-- ---------- conflicts ----------

CREATE TABLE _new_conflicts (
    conflict_id         TEXT PRIMARY KEY,
    item_code           TEXT REFERENCES items(item_code),
    domain              TEXT NOT NULL,
    pop_a               TEXT NOT NULL,
    pop_b               TEXT NOT NULL,
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'ACTIVE','PROPOSED','DEFERRED','RESOLVED-EVIDENCE',
                            'RESOLVED-CONSENSUS','UNRESOLVED','CLOSED','RETIRED'
                        )),
    resolution          TEXT,
    evidence            TEXT,
    gap_id              TEXT,
    source_skill        TEXT NOT NULL DEFAULT 'cross-population-conflict-mapper',
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

INSERT INTO _new_conflicts
SELECT conflict_id, item_code, domain, pop_a, pop_b,
       CASE status
            WHEN 'RESOLUTION-PROPOSED' THEN 'PROPOSED'
            WHEN 'MODE-S-ONLY'         THEN 'UNRESOLVED'
            ELSE status
       END,
       resolution, evidence, gap_id, source_skill, created_at,
       created_by_session, updated_at, updated_by_session
FROM conflicts;

DROP TABLE conflicts;
ALTER TABLE _new_conflicts RENAME TO conflicts;

CREATE UNIQUE INDEX idx_conflicts_dedup  ON conflicts(item_code, domain, pop_a, pop_b);
CREATE INDEX        idx_conflicts_status ON conflicts(status);
CREATE INDEX        idx_conflicts_item   ON conflicts(item_code);

PRAGMA foreign_keys = ON;

PRAGMA user_version = 58;
