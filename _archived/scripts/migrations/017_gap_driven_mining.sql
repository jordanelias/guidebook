-- 017_gap_driven_mining.sql
-- Schema migration: adds structural support for gap-driven citation mining.
--
-- Per DR-2026-05-26-gap-driven-mining-protocol. The existing citation-miner
-- skill is anchor-source-keyed: it starts from a confirmed Tier 1-3 source
-- and traces backward + forward citations, depth-1 limit. It cannot address
-- gaps that exist BECAUSE no anchor source was found — THIN-BASE flags,
-- "0/N Co-1 jurisdictions", "no indexed evidence for parameter X". Those
-- gaps need search starting from the parameter × population × outcome
-- shortfall, not from a source. This migration adds the two structural
-- pieces the gap-driven protocol requires.
--
-- Closes GAP-283 (citation-miner skill never invoked inline; structural
-- pivot to gap-driven mining per owner direction 2026-05-23).
--
-- Two structural additions:
--
--   1. gaps.mining_addressability — classifies each gap's resolution path.
--      Enum: ADDRESSABLE (mining is the right resolution), NOT-ADDRESSABLE
--      (some other path applies — content authorship, structural fix,
--      database correction, etc.), TRIAGE-NEEDED (classification deferred).
--      NULL is permitted for backward-compat with pre-migration rows; a
--      one-time triage data migration (separate session) backfills explicit
--      values for every OPEN gap; subsequent gap-raising skills set the
--      value at intake.
--
--   2. gap_mining table — per-attempt record of a gap-driven mining attempt.
--      Mirrors the supersession_check design (DR-2026-05-24). One row per
--      attempt, append-only, allowing semiannual-sweep semantics: a gap
--      mined once with null_result is re-eligible after a tunable horizon.
--      The operative outcome for a gap is MAX(attempt_at).
--
-- Interlocks with existing rules (see DR §Interlocks):
--   - rule #7 (adversarial research): closure_evidence_found outcome
--     requires populating gaps.{falsification_condition, confidence_interval,
--     shift_conditions, named_dissenter} BEFORE gap status moves to CLOSED-*.
--   - rule #8 (PMP): numerical-spec gaps route through progressive-measurement
--     AFTER candidate discovery, BEFORE gap closure.
--   - rule #10 sub-rules 2/3: discoveries that land in BPC reasoning docs
--     route through reasoning-doc-citations.
--   - DR-2026-05-24 (supersession protocol): discoveries that supersede
--     existing anchors create both a gap_mining row AND a supersession_check
--     row; they describe orthogonal relationships (gap_mining = "what
--     evidence closed this gap"; supersession_check = "does the new evidence
--     replace what an anchor was supporting").
--
-- schema_version: 16 -> 17

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- gaps.mining_addressability: classifies resolution path.
-- ----------------------------------------------------------------------------
-- Default class proposed by triage migration (override allowed at intake):
--   skill = functional-deficit-auditor      -> ADDRESSABLE
--   skill = content-gap-analyzer            -> ADDRESSABLE
--   skill = research-log-manager            -> ADDRESSABLE
--   skill = bpc-auditor / guidebook-auditor -> NOT-ADDRESSABLE
--   skill = citation-verifier               -> NOT-ADDRESSABLE
--   skill = supersession-audit              -> NOT-ADDRESSABLE
--                                              (supersession protocol owns
--                                              its own resolution path)
--   skill = citation-miner / NULL / '-'     -> TRIAGE-NEEDED
ALTER TABLE gaps ADD COLUMN mining_addressability TEXT
    CHECK(mining_addressability IS NULL OR mining_addressability IN (
        'ADDRESSABLE',
        'NOT-ADDRESSABLE',
        'TRIAGE-NEEDED'
    ));

CREATE INDEX idx_gaps_mining_addressability ON gaps(mining_addressability);

-- ----------------------------------------------------------------------------
-- gap_mining: per-attempt record of a gap-driven mining attempt.
-- ----------------------------------------------------------------------------
-- One row per attempt; append-only. The most recent row for each gap_id is
-- the operative outcome; older rows are retained for audit history. This
-- mirrors supersession_check (migration 015) — gap-driven mining and
-- supersession audits are the two protocols that ship as append-only
-- per-attempt records rather than one-row-per-subject mutations.
CREATE TABLE gap_mining (
    gap_mining_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    gap_id               TEXT NOT NULL REFERENCES gaps(gap_id),

    -- Provenance
    attempt_at           TEXT NOT NULL,
    attempted_by_session TEXT NOT NULL,

    -- Search strategy record (replayable). JSON:
    --   {"strategies": [{"tool":"pubmed","query":"...","date_filter":"...",
    --                    "tier_filter":"...","connectors_used":["pubmed",...],
    --                    "candidates_returned":N}, ...]}
    search_strategy_record TEXT NOT NULL,
    candidates_returned    INTEGER NOT NULL DEFAULT 0,
    candidates_reviewed    INTEGER NOT NULL DEFAULT 0,

    -- Outcome enum
    outcome              TEXT NOT NULL CHECK(outcome IN (
        'closure_evidence_found',  -- enough to close the gap (rule #7 must fire)
        'partial_evidence_found',  -- some discoveries; gap stays OPEN with annotation
        'null_result',             -- searches ran clean, no relevant discoveries
        'gap_recategorized',       -- gap not mining-addressable after all
        'deferred'                 -- connectors unavailable / other blocker
    )),

    -- Discoveries: JSON array of evidence_sources.ref_id values written to
    -- evidence_sources + source_slug_links as part of THIS attempt.
    -- NULL or '[]' permitted for null_result / deferred / gap_recategorized.
    discoveries_logged   TEXT,

    -- Rule #10 gate: candidates returned but not yet verified are recorded
    -- as DOIs only, NOT INSERTed to evidence_sources. The next session may
    -- verify and promote them. Mirrors supersession_check.superseding_dois.
    candidate_dois       TEXT,  -- JSON array

    -- Method used. Composite is the cluster-search pattern (skills/
    -- supersession-audit_SKILL.md §3) — 3-6 queries per gap, evaluated
    -- as a single attempt rather than per-query.
    check_method         TEXT NOT NULL CHECK(check_method IN (
        'pubmed_cluster',
        'scholar_gateway_lived_experience',
        'cochrane_direct',
        'standards_body_direct',
        'multilingual_research',
        'composite'
    )),

    notes                TEXT,

    -- Integrity: closure_evidence_found must have at least one discovery
    CHECK (
        outcome != 'closure_evidence_found'
        OR (discoveries_logged IS NOT NULL AND discoveries_logged != '[]')
    ),

    -- Integrity: gap_recategorized must document why (>=20 chars)
    CHECK (
        outcome != 'gap_recategorized'
        OR (notes IS NOT NULL AND length(notes) >= 20)
    ),

    -- Integrity: deferred must document the blocker (>=10 chars)
    CHECK (
        outcome != 'deferred'
        OR (notes IS NOT NULL AND length(notes) >= 10)
    )
);

CREATE INDEX idx_gap_mining_gap ON gap_mining(gap_id);
CREATE INDEX idx_gap_mining_outcome ON gap_mining(outcome);
CREATE INDEX idx_gap_mining_attempt_at ON gap_mining(attempt_at);

-- Schema-version bump
PRAGMA user_version = 17;
