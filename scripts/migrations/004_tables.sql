-- 004_tables.sql
-- CO-0009 Phase 1 Session 1a
-- Adds: items, item_audit_runs, conflicts tables
-- Decisions: D-0141, D-0142, D-0143
-- Does NOT expand gap categories or citation_mining — those are migration 005
-- schema_version → 4

-- ============================================================
-- items
-- Anchor table for per-item audit pipeline state.
-- item_code is the primary identifier (e.g. I-01, A-10b).
-- category uses IN constraint (not BETWEEN) to prevent multi-char values.
-- item_id (ITEM-NNNN) nullable: assigned during formal item registration,
--   which is out of CO-0009 scope.
-- bpc_source_slug FK to slugs: nullable for items without a BPC file.
-- status: draft → active → merged/retired lifecycle.
-- ============================================================

CREATE TABLE items (
    item_code           TEXT PRIMARY KEY,
    item_id             TEXT UNIQUE,
    category            TEXT NOT NULL
                        CHECK(category IN (
                            'A','B','C','D','E','F','G','H','I','J','K'
                        )),
    name                TEXT NOT NULL,
    applicable_groups   TEXT,
    bpc_source_slug     TEXT REFERENCES slugs(slug),
    status              TEXT NOT NULL DEFAULT 'draft'
                        CHECK(status IN ('draft','active','merged','retired')),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE INDEX idx_items_category ON items(category);
CREATE INDEX idx_items_slug     ON items(bpc_source_slug);

-- ============================================================
-- item_audit_runs
-- Tracks per-item pipeline audit state across sessions.
-- run_id = {item_code}_{session_filename} — unique per item per session.
-- steps_started: written before each step begins.
-- steps_complete: written after step commits its findings.
-- A step in steps_started but not steps_complete → mid-step failure → re-run.
-- spec_hash: MD5 of normalised item spec text at run start.
--   On resume: recompute and compare. Mismatch → warn + prompt.
-- brief_path: references/audit-briefs/{item_code}_brief.md
-- ============================================================

CREATE TABLE item_audit_runs (
    run_id              TEXT PRIMARY KEY,
    item_code           TEXT NOT NULL REFERENCES items(item_code),
    session             TEXT NOT NULL,
    steps_complete      TEXT NOT NULL DEFAULT '[]',
    steps_started       TEXT NOT NULL DEFAULT '[]',
    status              TEXT NOT NULL DEFAULT 'IN-PROGRESS'
                        CHECK(status IN ('IN-PROGRESS','COMPLETE','HANDED-OFF')),
    spec_hash           TEXT,
    brief_path          TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE INDEX idx_audit_runs_item   ON item_audit_runs(item_code);
CREATE INDEX idx_audit_runs_status ON item_audit_runs(status);

-- ============================================================
-- conflicts
-- Per-item audit findings from cross-population-conflict-mapper.
-- DISTINCT from data/db/guidebook.db conflict table (website DB,
-- canonical 12-domain content). Both use the same domain taxonomy
-- codes for cross-reference but are not FK-linked (cross-DB FK
-- impossible in SQLite).
-- conflict_id: CONF-NNNN sequential (tracking DB only).
-- item_code FK: nullable for historical conflicts lacking item association.
-- pop_a/pop_b: wrapper MUST normalise so pop_a < pop_b lexicographically
--   before INSERT. UNIQUE index deduplicates on the normalised pair.
--   Schema alone cannot enforce ordering (CHECK pop_a<pop_b would block
--   all inserts until normalised — wrapper is the right enforcement layer).
-- gap_id: no FK constraint (populated after gap in same transaction;
--   deferred FK would need explicit DEFERRABLE clause). Consolidator
--   validates gap_id references an OPEN gap and flags orphans.
-- ============================================================

CREATE TABLE conflicts (
    conflict_id         TEXT PRIMARY KEY,
    item_code           TEXT REFERENCES items(item_code),
    domain              TEXT NOT NULL,
    pop_a               TEXT NOT NULL,
    pop_b               TEXT NOT NULL,
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'RESOLVED-EVIDENCE',
                            'RESOLVED-CONSENSUS',
                            'RESOLUTION-PROPOSED',
                            'UNRESOLVED',
                            'MODE-S-ONLY'
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

-- Dedup on (item_code, domain, pop_a, pop_b) — wrapper ensures pop_a < pop_b.
CREATE UNIQUE INDEX idx_conflicts_dedup ON conflicts(item_code, domain, pop_a, pop_b);
CREATE INDEX        idx_conflicts_status ON conflicts(status);
CREATE INDEX        idx_conflicts_item   ON conflicts(item_code);

-- ============================================================
-- schema_version
-- ============================================================

UPDATE db_meta SET value = '4' WHERE key = 'schema_version';
