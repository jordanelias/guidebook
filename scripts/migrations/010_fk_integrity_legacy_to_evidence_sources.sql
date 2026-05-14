-- 010_fk_integrity_legacy_to_evidence_sources.sql
-- FK integrity fix: repoint foreign keys from `evidence_sources_v1_legacy` to
-- `evidence_sources` on four tables (782 rows total) using SQLite's
-- table-rebuild pattern. Includes two data fixes and one schema addition.
--
-- Per DR-2026-05-13 §9 step 1 (session_2026-05-13b).
-- Origin: handoff-2026-05-13b §3.
--
-- schema_version → 10

-- Tables affected:
--   source_slug_links           721 rows  ref_id          NOT NULL
--   evidence_population_match    22 rows  ref_id          NULL OK
--   spec_value_probes            18 rows  ref_id          NULL OK
--   citation_mining              21 rows  global_ref_id   NULL OK
--
-- Data fixes:
--   - PMP-A02-001-S2.ref_id: 'ANSI-S12.60-S5.3' (invalid) → 'REF-00335' (ANSI S12.60:2010)
--   - 5 evidence_population_match.ref_id NULLs backfilled from source_ref:
--       EPM-S3-001 → REF-00642, EPM-S3-002 → REF-00710, EPM-S3-003 → REF-00711,
--       EPM-C4-001 → REF-00551, EPM-C4-002 → REF-00557
--
-- Schema addition:
--   - evidence_population_match.gap_id (nullable, FK → gaps.gap_id)
--     supports standing rule #7 audit trail (which gap generated each match).
--
-- NOT in scope:
--   - search_query / search_query_alt NOT NULL on spec_value_probes (6 legitimate NULLs)
--   - Dropping evidence_sources_v1_legacy (defer; other sessions may reference it)
--   - Resolving evidence_population_match source_ref/ref_id duplicate-column anomaly

PRAGMA foreign_keys = OFF;

-- 1. Drop dependent view (will be recreated below)
DROP VIEW IF EXISTS v_pmp_latest_walk;

-- 2. Rebuild source_slug_links
CREATE TABLE _new_source_slug_links (
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id        TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (ref_id, slug)
);
INSERT INTO _new_source_slug_links
SELECT ref_id, slug, local_ref_id, created_at, created_by_session, updated_at, updated_by_session
FROM source_slug_links;
DROP TABLE source_slug_links;
ALTER TABLE _new_source_slug_links RENAME TO source_slug_links;
CREATE INDEX idx_ssl_slug ON source_slug_links(slug);
CREATE INDEX idx_ssl_ref  ON source_slug_links(ref_id);

-- 3. Rebuild evidence_population_match (adds gap_id column)
CREATE TABLE _new_evidence_population_match (
    match_id            TEXT PRIMARY KEY,
    source_ref          TEXT NOT NULL,
    target_population   TEXT NOT NULL,
    study_population    TEXT,
    sample_size         INTEGER,
    match_grade         TEXT NOT NULL CHECK(match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH')),
    mismatch_note       TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    ref_id              TEXT REFERENCES evidence_sources(ref_id),
    gap_id              TEXT REFERENCES gaps(gap_id)
);
INSERT INTO _new_evidence_population_match
    (match_id, source_ref, target_population, study_population, sample_size,
     match_grade, mismatch_note, created_at, created_by_session, ref_id)
SELECT match_id, source_ref, target_population, study_population, sample_size,
       match_grade, mismatch_note, created_at, created_by_session, ref_id
FROM evidence_population_match;
DROP TABLE evidence_population_match;
ALTER TABLE _new_evidence_population_match RENAME TO evidence_population_match;
CREATE INDEX idx_epm_ref ON evidence_population_match(ref_id);
CREATE INDEX idx_epm_gap ON evidence_population_match(gap_id);

-- 4. Rebuild spec_value_probes (also fixes PMP-A02-001-S2 ref_id inline)
CREATE TABLE _new_spec_value_probes (
    probe_id            TEXT PRIMARY KEY,
    walk_id             TEXT NOT NULL,
    slug                TEXT NOT NULL,
    item_code           TEXT NOT NULL REFERENCES items(item_code),
    spec_value_origin   REAL NOT NULL,
    spec_unit           TEXT NOT NULL,
    direction           TEXT NOT NULL CHECK (direction IN ('up','down')),
    population          TEXT NOT NULL,
    claim_type          TEXT NOT NULL CHECK (claim_type IN ('minimum','maximum','target','range_low','range_high')),
    step_index          INTEGER NOT NULL,
    phase               TEXT NOT NULL CHECK (phase IN ('outer-pass-1st','outer-pass-2nd','outer-stop','refinement-pass-1st','refinement-pass-2nd','refinement-stop','final')),
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
INSERT INTO _new_spec_value_probes
SELECT probe_id, walk_id, slug, item_code, spec_value_origin, spec_unit,
       direction, population, claim_type, step_index, phase,
       step_value, step_value_unit, search_query, search_query_alt,
       passes_strict,
       CASE WHEN probe_id='PMP-A02-001-S2' THEN 'REF-00335' ELSE ref_id END,
       notes, created_at, created_by_session
FROM spec_value_probes;
DROP TABLE spec_value_probes;
ALTER TABLE _new_spec_value_probes RENAME TO spec_value_probes;
CREATE INDEX idx_svp_slug_item  ON spec_value_probes(slug, item_code);
CREATE INDEX idx_svp_walk       ON spec_value_probes(walk_id, step_index);
CREATE INDEX idx_svp_item_phase ON spec_value_probes(item_code, phase);
CREATE INDEX idx_svp_ref        ON spec_value_probes(ref_id);

-- 5. Rebuild citation_mining
CREATE TABLE _new_citation_mining (
    slug                 TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id         TEXT NOT NULL,
    global_ref_id        TEXT REFERENCES evidence_sources(ref_id),
    doi                  TEXT,
    backward             INTEGER NOT NULL DEFAULT 0 CHECK(backward IN (0,1)),
    forward              INTEGER NOT NULL DEFAULT 0 CHECK(forward IN (0,1)),
    connections_produced TEXT NOT NULL DEFAULT '[]',
    notes                TEXT,
    created_at           TEXT NOT NULL,
    created_by_session   TEXT NOT NULL,
    updated_at           TEXT NOT NULL,
    updated_by_session   TEXT NOT NULL,
    deferred_reason      TEXT,
    PRIMARY KEY (slug, local_ref_id)
);
INSERT INTO _new_citation_mining
SELECT slug, local_ref_id, global_ref_id, doi, backward, forward,
       connections_produced, notes, created_at, created_by_session,
       updated_at, updated_by_session, deferred_reason
FROM citation_mining;
DROP TABLE citation_mining;
ALTER TABLE _new_citation_mining RENAME TO citation_mining;
CREATE INDEX idx_cm_unmined ON citation_mining(slug, backward, forward);

-- 6. Recreate v_pmp_latest_walk view
CREATE VIEW v_pmp_latest_walk AS
SELECT
    item_code,
    slug,
    walk_id,
    MAX(created_at) AS walk_completed_at,
    SUM(CASE WHEN phase IN ('outer-pass-1st','outer-pass-2nd','refinement-pass-1st','refinement-pass-2nd') THEN 1 ELSE 0 END) AS supported_steps,
    SUM(CASE WHEN phase IN ('outer-stop','refinement-stop') THEN 1 ELSE 0 END) AS terminator_steps
FROM spec_value_probes
GROUP BY item_code, slug, walk_id;

-- 7. Backfill 5 evidence_population_match.ref_id NULLs from source_ref
UPDATE evidence_population_match SET ref_id='REF-00642' WHERE match_id='EPM-S3-001' AND ref_id IS NULL;
UPDATE evidence_population_match SET ref_id='REF-00710' WHERE match_id='EPM-S3-002' AND ref_id IS NULL;
UPDATE evidence_population_match SET ref_id='REF-00711' WHERE match_id='EPM-S3-003' AND ref_id IS NULL;
UPDATE evidence_population_match SET ref_id='REF-00551' WHERE match_id='EPM-C4-001' AND ref_id IS NULL;
UPDATE evidence_population_match SET ref_id='REF-00557' WHERE match_id='EPM-C4-002' AND ref_id IS NULL;

PRAGMA foreign_keys = ON;
