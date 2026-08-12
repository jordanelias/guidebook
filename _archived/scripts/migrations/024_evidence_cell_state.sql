-- 024_evidence_cell_state.sql
-- Schema migration (Stage 2.3): build the four-state cell machine + convergence
-- assessment the doctrine makes binding. Closes R2 (these tables were specified
-- but unbuilt). Built DIRECTNESS-AWARE per decision D-D and
-- governance/evidence-methodology.md §2 (cell states), §3 (convergence), and
-- §1.4/§1.6/§1.7 (scale-conditioned weighting + directness conditioning layer);
-- doctrine SHA 3da73bd. Applies the model in schemas/directness.py (Stage 2.2).
--
-- CELL IDENTITY. The doctrine's "(parameter × population)" cell is keyed on the
-- canonical live parameter `items.item_code` (e.g. A-02), NOT the spec-layer
-- SPEC-NNNN: no `specification` table exists in the migration-built DB (it is
-- defined only in the legacy scripts/migrate/init_database.py, which is not the
-- canonical scripts/migrate_db.py path). When/if the specification layer is built
-- canonically, the cell can be refined to spec_id × population; for now item_code
-- is the FK-valid parameter key. schemas/evidence_state.py is revised to match.
--
-- DIRECTNESS-AWARENESS.
--   * evidence_cell_state.design_scale — the §1.4/§1.6 design-scale axis
--     (universal/population/person). It is the conditioning input from which each
--     source's directness is computed (schemas/directness.scale_directness).
--   * convergence_assessment.down_weighted_sources / .discounted_sources — the
--     §1.7 directness conditioning recorded at the convergence level: sources
--     grain-mismatched for this cell's scale are DOWN-WEIGHTED (count less) or
--     DISCOUNTED / NON-ANCHORING (cannot anchor). The anchoring set is
--     (clinical_sources ∪ co1_sources ∪ co2_sources) minus discounted.
--
-- State-dependent required-field rules (pending⇒gap_register_id,
-- provisional⇒confidence flag, not_applicable⇒rationale, stated/provisional⇒
-- convergence) are conditional across columns and are enforced in the revised
-- Pydantic model, not in SQLite CHECK. The table carries the columns + the
-- enum/boolean CHECKs that SQLite can express.
--
-- Schema-only, additive. The runner sets PRAGMA user_version to 24 after applying.

BEGIN;

-- Convergence assessment — one row per assessed cell (§3.2), directness-aware.
CREATE TABLE convergence_assessment (
    convergence_id          INTEGER PRIMARY KEY,
    status                  TEXT NOT NULL
                            CHECK (status IN ('convergent', 'divergent',
                                              'single_axis', 'pending_assessment')),
    clinical_sources        TEXT,   -- JSON array of REF-IDs (Tier 1-3)
    co1_sources             TEXT,   -- JSON array of REF-IDs (Co-1)
    co2_sources             TEXT,   -- JSON array of REF-IDs (Co-2)
    down_weighted_sources   TEXT,   -- JSON array — directness DOWN-WEIGHTED (§1.7)
    discounted_sources      TEXT,   -- JSON array — directness DISCOUNTED/NON-ANCHORING
    rationale               TEXT,   -- required for divergent + single_axis (model)
    synthesis_approach      TEXT,   -- required for divergent (model)
    created_at              TEXT,
    created_by_session      TEXT,
    updated_at              TEXT,
    updated_by_session      TEXT
);

-- Evidence cell state — one row per (item_code × population) cell (§2).
CREATE TABLE evidence_cell_state (
    cell_id                 INTEGER PRIMARY KEY,
    item_code               TEXT NOT NULL REFERENCES items(item_code),
    population_code         TEXT NOT NULL REFERENCES populations(population_code),
    state                   TEXT NOT NULL
                            CHECK (state IN ('stated', 'provisional',
                                             'pending', 'not_applicable')),
    design_scale            TEXT
                            CHECK (design_scale IN ('universal', 'population', 'person')),
    convergence_id          INTEGER REFERENCES convergence_assessment(convergence_id),
    -- provisional confidence flag (§2.3)
    confidence_dimensions_present   TEXT,   -- JSON array
    confidence_dimensions_absent    TEXT,   -- JSON array
    confidence_synthesis_basis      TEXT,
    -- pending gap link (§2.4)
    gap_register_id         TEXT REFERENCES gaps(gap_id),
    -- not_applicable rationale (§2.5)
    not_applicable_rationale TEXT,
    -- source-quality flags
    has_unverified_sources   INTEGER NOT NULL DEFAULT 0
                             CHECK (has_unverified_sources IN (0, 1)),
    all_sources_disqualified INTEGER NOT NULL DEFAULT 0
                             CHECK (all_sources_disqualified IN (0, 1)),
    created_at              TEXT,
    created_by_session      TEXT,
    updated_at              TEXT,
    updated_by_session      TEXT,
    UNIQUE (item_code, population_code)
);

CREATE INDEX idx_cell_state_item  ON evidence_cell_state(item_code);
CREATE INDEX idx_cell_state_pop   ON evidence_cell_state(population_code);
CREATE INDEX idx_cell_state_state ON evidence_cell_state(state);

COMMIT;
