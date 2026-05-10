-- 006_spec_value_probes.sql
-- DR-2026-05-10-progressive-measurement-protocol
-- Adds spec_value_probes table and pmp_* columns on items, plus latest-walk view.
-- Workplan: workplan/progressive-measurement-protocol.md
-- schema_version → 6

-- ============================================================
-- spec_value_probes
--
-- Append-only log of progressive-measurement walks. One walk_id groups all
-- step rows of a single walk; re-running a walk creates a new walk_id and
-- preserves prior rows for audit. The 'final' row carries the empirical
-- ceiling/floor and signed gap from V₀ for that walk.
-- ============================================================

CREATE TABLE spec_value_probes (
    probe_id            TEXT PRIMARY KEY,
    walk_id             TEXT NOT NULL,
    slug                TEXT NOT NULL,
    item_code           TEXT NOT NULL REFERENCES items(item_code),
    spec_value_origin   REAL NOT NULL,
    spec_unit           TEXT NOT NULL,
    direction           TEXT NOT NULL CHECK (direction IN ('up','down')),
    population          TEXT NOT NULL,
    claim_type          TEXT NOT NULL
                        CHECK (claim_type IN (
                            'minimum','maximum','target','range_low','range_high'
                        )),
    step_index          INTEGER NOT NULL,
    phase               TEXT NOT NULL
                        CHECK (phase IN (
                            'outer-pass-1st','outer-pass-2nd','outer-stop',
                            'refinement-pass-1st','refinement-pass-2nd','refinement-stop',
                            'final'
                        )),
    step_value          REAL NOT NULL,
    step_value_unit     TEXT NOT NULL,
    search_query        TEXT,
    search_query_alt    TEXT,
    passes_strict       INTEGER CHECK (passes_strict IN (0,1)),
    ref_id              TEXT REFERENCES evidence_sources(ref_id),
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL
);

CREATE INDEX idx_svp_slug_item  ON spec_value_probes(slug, item_code);
CREATE INDEX idx_svp_walk       ON spec_value_probes(walk_id, step_index);
CREATE INDEX idx_svp_item_phase ON spec_value_probes(item_code, phase);
CREATE INDEX idx_svp_ref        ON spec_value_probes(ref_id);

-- ============================================================
-- items: add pmp_* columns
--
-- Single-row item-level summary of latest walk. Detail lives in
-- spec_value_probes. These columns are convenience for queries
-- and audits; spec_value_probes is the source of truth.
-- ============================================================

ALTER TABLE items ADD COLUMN pmp_delta_min          REAL;
ALTER TABLE items ADD COLUMN pmp_direction          TEXT;
ALTER TABLE items ADD COLUMN pmp_last_walk_at       TEXT;
ALTER TABLE items ADD COLUMN pmp_empirical_ceiling  REAL;
ALTER TABLE items ADD COLUMN pmp_gap_signed         REAL;

-- ============================================================
-- v_pmp_latest_walk: convenience view
-- ============================================================

CREATE VIEW v_pmp_latest_walk AS
SELECT
    item_code,
    slug,
    walk_id,
    MAX(created_at) AS walk_completed_at,
    SUM(CASE WHEN phase IN (
            'outer-pass-1st','outer-pass-2nd',
            'refinement-pass-1st','refinement-pass-2nd'
        ) THEN 1 ELSE 0 END) AS supported_steps,
    SUM(CASE WHEN phase IN (
            'outer-stop','refinement-stop'
        ) THEN 1 ELSE 0 END) AS terminator_steps
FROM spec_value_probes
GROUP BY item_code, slug, walk_id;

-- ============================================================
-- schema_version
-- ============================================================

UPDATE db_meta SET value = '6' WHERE key = 'schema_version';
