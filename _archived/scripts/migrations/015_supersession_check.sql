-- 015_supersession_check.sql
-- Adds the `supersession_check` table and the `supersession_check_complete` +
-- `closure_definition_version` columns on `bpc_metadata`.
--
-- Per DR-2026-05-24-best-practice-supersession-protocol. Establishes the
-- per-anchor-source supersession-check record as a precondition for slug closure
-- under the v2 closure definition (citation_mining_complete=1 AND
-- supersession_check_complete=1).
--
-- Supports doctrinal commitments 2, 3, 5 from governance/mission-and-epistemics.md.
--
-- schema_version: 14 -> 15

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- supersession_check: per-anchor-source supersession outcome record.
-- One row per (slug, ref_id, checked_at).
-- The most recent row for each (slug, ref_id) is the operative outcome; older
-- rows are retained for audit history.
-- ----------------------------------------------------------------------------
CREATE TABLE supersession_check (
    check_id            TEXT PRIMARY KEY,
    slug                TEXT NOT NULL,
    local_ref_id        TEXT NOT NULL,
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    anchor_tier         INTEGER NOT NULL CHECK(anchor_tier BETWEEN 1 AND 6),
    anchor_evidence_type TEXT NOT NULL,  -- co1, co2, clinical, sr_meta, standard_eb, national_fw, code, grey

    -- The outcome of the supersession search
    outcome             TEXT NOT NULL CHECK(outcome IN (
        'current_best',
        'superseded_by',
        'refined_by',
        'divergent_no_supersession',
        'co1_addition_logged',
        'pending'  -- check started but not yet completed; should not appear on closed slug
    )),

    -- Outcome details
    superseding_ref_ids  TEXT,  -- JSON array of ref_ids for superseded_by / refined_by / divergent
    superseding_dois     TEXT,  -- JSON array of DOIs for not-yet-INSERTed candidates (rule #10 gate)
    refinement_dimension TEXT,  -- For refined_by: which parameter/population/outcome dimension was refined
    divergence_notes     TEXT,  -- For divergent_no_supersession: prose summary of the divergence

    -- Search strategy record (so the check is replayable)
    search_strategy_record TEXT NOT NULL,  -- JSON: {tool, query, date_filter, tier_filter, candidates_returned, candidates_reviewed}
    candidates_returned  INTEGER NOT NULL DEFAULT 0,
    candidates_reviewed  INTEGER NOT NULL DEFAULT 0,

    -- Audit fields
    checked_at           TEXT NOT NULL,
    checked_by_session   TEXT NOT NULL,
    check_method         TEXT NOT NULL CHECK(check_method IN (
        'pubmed_search', 'scholar_gateway', 'cochrane_direct',
        'standards_body_direct', 'multilingual_research',
        'composite'
    )),
    notes                TEXT,

    -- Integrity constraints
    CHECK (
        -- superseded_by / refined_by / divergent_no_supersession require superseding refs
        (outcome IN ('superseded_by','refined_by','divergent_no_supersession')
         AND (superseding_ref_ids IS NOT NULL OR superseding_dois IS NOT NULL))
        OR
        outcome IN ('current_best','co1_addition_logged','pending')
    ),
    CHECK (
        -- refined_by must name the refinement dimension
        outcome != 'refined_by' OR refinement_dimension IS NOT NULL
    ),
    CHECK (
        -- divergent_no_supersession must include divergence notes
        outcome != 'divergent_no_supersession' OR divergence_notes IS NOT NULL
    ),
    CHECK (
        -- co1_addition_logged only valid for Co-1 sources
        outcome != 'co1_addition_logged' OR anchor_evidence_type = 'co1'
    )
);

CREATE INDEX idx_supersession_check_slug ON supersession_check(slug);
CREATE INDEX idx_supersession_check_ref ON supersession_check(ref_id);
CREATE INDEX idx_supersession_check_outcome ON supersession_check(outcome);
CREATE INDEX idx_supersession_check_checked_at ON supersession_check(checked_at);

-- ----------------------------------------------------------------------------
-- bpc_metadata additions
-- ----------------------------------------------------------------------------

-- supersession_check_complete: set to 1 when every cited anchor source in the slug
-- has a supersession_check row with a terminal outcome (not 'pending').
-- Required (alongside citation_mining_complete=1) for v2 slug closure.
ALTER TABLE bpc_metadata ADD COLUMN supersession_check_complete INTEGER NOT NULL DEFAULT 0
    CHECK(supersession_check_complete IN (0, 1));

-- closure_definition_version: tracks which closure bar a slug was closed under.
-- 'v1' = citation_mining_complete=1 only (pre-DR-2026-05-24)
-- 'v2' = citation_mining_complete=1 AND supersession_check_complete=1 (this DR)
-- Default v1 for backward compat; new closures stamp v2 explicitly.
ALTER TABLE bpc_metadata ADD COLUMN closure_definition_version TEXT NOT NULL DEFAULT 'v1'
    CHECK(closure_definition_version IN ('v1', 'v2'));

-- Bump schema version
PRAGMA user_version = 15;
