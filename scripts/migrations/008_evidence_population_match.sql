-- 008_evidence_population_match.sql
-- Captures the evidence_population_match table that exists in production but
-- is not represented in any prior schema migration (likely added via ad-hoc
-- ALTER during the adversarial-research protocol rollout, DR-2026-05-09).
--
-- Adding it here so that:
--   (a) rebuilding the DB from migrations produces the same schema as production
--   (b) future fresh installs get the table automatically
--   (c) the CI reproducibility check (GAP-290) passes
--
-- schema_version → 8
--
-- Note: the table was created with a trailing column add (ref_id) — the CREATE
-- below matches the final shape including that column.

CREATE TABLE IF NOT EXISTS evidence_population_match (
    match_id TEXT PRIMARY KEY,
    source_ref TEXT NOT NULL,
    target_population TEXT NOT NULL,
    study_population TEXT,
    sample_size INTEGER,
    match_grade TEXT NOT NULL CHECK(match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH')),
    mismatch_note TEXT,
    created_at TEXT NOT NULL,
    created_by_session TEXT NOT NULL,
    ref_id TEXT REFERENCES evidence_sources(ref_id)
);
