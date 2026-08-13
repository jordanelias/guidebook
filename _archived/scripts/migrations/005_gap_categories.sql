-- 005_gap_categories.sql
-- CO-0009 Phase 1 Session 1c
-- Adds CONF and AUDT to gaps CHECK constraint (recreation pattern per migration 002)
-- Adds deferred_reason column to citation_mining
-- Decision: D-0144, D-0145
-- schema_version → 5

-- ============================================================
-- gaps: add CONF and AUDT categories
-- Full set after expansion:
-- RP, SW, CR, ST, MX, CD, EC, EG, CI, DEC, CONF, AUDT
-- ============================================================

CREATE TABLE gaps_new (
    gap_id              TEXT PRIMARY KEY,
    category            TEXT NOT NULL
                        CHECK(category IN (
                            'RP','SW','CR','ST','MX','CD','EC','EG',
                            'CI','DEC','CONF','AUDT'
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

-- ============================================================
-- citation_mining: add deferred_reason column
-- NULL  = source was mined (or not yet processed)
-- TEXT  = source was deferred; value is reason string
--         e.g. "not-relevant-to-I-01"
-- ============================================================

ALTER TABLE citation_mining ADD COLUMN deferred_reason TEXT;

-- ============================================================
-- schema_version
-- ============================================================

UPDATE db_meta SET value = '5' WHERE key = 'schema_version';
