-- 060_restore_superseded_status.sql
-- SCHEMA migration — put SUPERSEDED back into the ratified status vocabulary.
--
-- Owner ruling 2026-08-15: "yes we keep superseded".
--
-- WHY THIS MIGRATION EXISTS. Migration 058 retired SUPERSEDED on MY reading, not
-- on an instruction. The owner's 2026-08-14 list did not name the word; I flagged
-- that before implementing and implemented it in the same turn on two grounds:
-- that zero rows used the status, and that decisions.supersedes already carried
-- the relation.
--
-- The second ground was FALSE, and a re-derivation the owner asked for found it:
-- supersedes is '[]' on all 162 rows and has never been written to. The check
-- that produced the claim tested `supersedes != ''` — and '[]' is a non-empty
-- STRING. So the retirement rested on a column I had reported as populated and
-- which is empty everywhere. What IS populated is the inverse, predecessors, on
-- 51 rows.
--
-- The owner has now overturned the retirement. That is the correct outcome
-- independent of my error: a lifecycle word whose replacement pointer has never
-- been written is a word doing work nothing else does.
--
-- THE VOCABULARY IS NOW NINE WORDS, on both tables:
--   ACTIVE · PROPOSED · DEFERRED · RESOLVED-EVIDENCE · RESOLVED-CONSENSUS ·
--   UNRESOLVED · CLOSED · RETIRED · SUPERSEDED
--
-- SUPERSEDED and RETIRED are not synonyms and the distinction is the reason to
-- keep both: SUPERSEDED means replaced by a NAMED successor; RETIRED means
-- removed with no successor. Collapsing them would have made "was it replaced,
-- and by what?" unanswerable from the status alone — which is exactly what the
-- empty supersedes column already fails to answer.
--
-- NO DATA CHANGE. Widening a CHECK cannot invalidate an existing row, and zero
-- rows carry SUPERSEDED today. Unlike 058 there is no inline remap, and the
-- table copy is a straight SELECT *.
--
-- Same rebuild shape as 058, and for the same verified reasons: no view
-- references either table (v_root_id_conflicts reads source_value_extractions
-- and merely has "conflicts" in its name), and no foreign key points at either,
-- so the views need no drop-and-recreate. Re-verified against the live schema
-- rather than inherited from 058's header.

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
                            'RESOLVED-CONSENSUS','UNRESOLVED','CLOSED','RETIRED',
                            'SUPERSEDED'
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

INSERT INTO _new_decisions SELECT * FROM decisions;

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
                            'RESOLVED-CONSENSUS','UNRESOLVED','CLOSED','RETIRED',
                            'SUPERSEDED'
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

INSERT INTO _new_conflicts SELECT * FROM conflicts;

DROP TABLE conflicts;
ALTER TABLE _new_conflicts RENAME TO conflicts;

CREATE UNIQUE INDEX idx_conflicts_dedup  ON conflicts(item_code, domain, pop_a, pop_b);
CREATE INDEX        idx_conflicts_status ON conflicts(status);
CREATE INDEX        idx_conflicts_item   ON conflicts(item_code);

PRAGMA foreign_keys = ON;

PRAGMA user_version = 60;
