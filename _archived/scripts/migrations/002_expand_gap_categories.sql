-- 002_expand_gap_categories.sql
-- Adds CI (CI/CD infrastructure) and DEC (decision record) categories
-- to the gaps table CHECK constraint, matching actual gap_register.md data.

-- SQLite requires table recreation to modify CHECK constraints.

CREATE TABLE gaps_new (
    gap_id              TEXT PRIMARY KEY,
    category            TEXT NOT NULL
                        CHECK(category IN (
                            'RP','SW','CR','ST','MX','CD','EC','EG','CI','DEC'
                        )),
    priority            TEXT NOT NULL CHECK(priority IN ('P1','P2','P3')),
    status              TEXT NOT NULL
                        CHECK(status LIKE 'OPEN%' OR status LIKE 'CLOSED%'),
    skill               TEXT,
    section             TEXT,
    description         TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

INSERT INTO gaps_new SELECT * FROM gaps;

DROP TABLE gaps;

ALTER TABLE gaps_new RENAME TO gaps;

CREATE INDEX idx_gap_priority_status ON gaps(priority, status);

UPDATE db_meta SET value = '2' WHERE key = 'schema_version';
