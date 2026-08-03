-- 003_expand_decision_status.sql
-- Adds PROVISIONAL to decisions status CHECK, matching actual data.

CREATE TABLE decisions_new (
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
                            'ACTIVE','SUPERSEDED','WITHDRAWN','PROPOSED','PROVISIONAL'
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

INSERT INTO decisions_new SELECT * FROM decisions;

DROP TABLE decisions;

ALTER TABLE decisions_new RENAME TO decisions;

CREATE INDEX idx_decision_status   ON decisions(status);
CREATE INDEX idx_decision_category ON decisions(category);

UPDATE db_meta SET value = '3' WHERE key = 'schema_version';
