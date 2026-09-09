-- 071_parameter_at_base.sql
-- SCHEMA migration — the determination gets a subject, and it is the design parameter.
--
-- THREE RULINGS EXECUTED HERE, none of them new:
--
--   2026-08-26 (references/project-standards.md, `grep -n 'judgment object is the'`)
--     "The judgment object is the canonical parameter, and `items` is the render rollup
--     the entity model already calls it." Its ACTION (1): the P1.0 migration drops BOTH
--     item_code and population_code from specifications' identity and keys it on the
--     canonical parameter. ACTION (2): a canonical-parameter vocabulary lands in or
--     before that migration -- "the key may not be unconstrained free text. Its home is
--     the schema's own CHECK or a registry table, decided by the executing session and
--     recorded; not a list in code (rule 5)." This session chose the registry table.
--
--   2026-08-28, as relaxed by D-0182 (2026-09-01)
--     Any table attaching a determination to a group of disabled people takes four lens
--     columns, one CHECK, real typed FKs, and population_code is retired in favour of
--     the four. D-0182 relaxed "exactly one" to AT LEAST ONE -- COALESCE(...) IS NOT
--     NULL -- which is what migration 065 built and what item_taxonomy_links says in its
--     own comment.
--
--   2026-09-09, owner: "parameter at base"
--     Which is why this is base_parameters and not judgment_parameters. An adversarial
--     pass had proposed the latter, on the reasoning that a parameter is ADJUDICATED at
--     judgment. The owner ruled for base, and the contract already agreed: the criterion
--     `base-parameter-vocabulary` has been staged at `base` all along. Holding a
--     vocabulary and adjudicating into it are different acts; the registry is substrate,
--     and the adjudication that puts a row in it belongs to judgment and POINTS here.
--
-- ONE SUPERSESSION APPLIED RATHER THAN OBEYED. The 2026-08-26 ACTION (1) also says "the
-- three N:N cross-reference junctions (population, access need, ICF) land in the same
-- migration". The 2026-08-28 ruling is LATER and rules the opposite shape -- four lens
-- COLUMNS, and "Never a `population_*` link table". Rule 0: the later ruling supersedes
-- on contact. Columns, not junctions. Recorded here rather than silently resolved.
--
-- WHY specifications CAN BE DROPPED AND RECREATED. It holds 0 rows and NO committed
-- migration INSERTs into it -- verified 2026-09-09 with
-- `grep -lE 'INSERT INTO "?specifications"?' scripts/migrations/*.sql` (no matches), so
-- a replay reaches this point with the table empty and nothing downstream to strand.
-- Rule 5's "a column a committed data migration INSERTs can never be dropped" does not
-- bite, because nothing was ever inserted.
--
-- WHY item_taxonomy_links IS LEFT ALONE AND NOT RE-KEYED. It IS inserted into, by
-- migration 065 and by data_20260901183203, so a replay would apply those INSERTs; an
-- ALTER or DROP here would break it. Its rows were emptied when the owner deleted the
-- item layer on 2026-09-01, and its item_code FK into an emptied `items` makes it
-- unwritable today. Left dead rather than repaired: what replaces it, if anything, is
-- downstream of the first real determination and is not this migration's question.

-- ---------------------------------------------------------------------------
-- 1. The registry. BASE stage.
-- ---------------------------------------------------------------------------
-- The NAME lives in `terms` and is reached by pointer, never copied (rule 5). terms is
-- the vocabulary the owner ruled in use on 2026-09-09 ("use add-term for now"), and
-- `db.py add-term` is the only sanctioned route in: it mints the term and its NAMES-NEW
-- adjudication together, refuses a name carrying a digit, comparator or min/max word,
-- and requires an observed phrase to mint FROM. So a parameter cannot exist without an
-- observation behind it -- which is the whole difference from `items`, whose 93 rows
-- were authored months before any research and whose names stated their own answers.
CREATE TABLE base_parameters (
    parameter_id        INTEGER PRIMARY KEY,
    -- UNIQUE: one parameter per term. A second row for the same term is the dual home
    -- rule 5 forbids; `add-term` already refuses a duplicate canonical_en upstream.
    term_id             TEXT    NOT NULL UNIQUE REFERENCES terms(term_id),
    status              TEXT    NOT NULL DEFAULT 'active'
                                CHECK (status IN ('active', 'merged', 'retired')),
    merged_into         INTEGER REFERENCES base_parameters(parameter_id),
    notes               TEXT,
    created_at          TEXT    NOT NULL,
    created_by_session  TEXT    NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT,
    -- merged_into is meaningful only for a merged row, and required for one.
    CHECK ((status = 'merged' AND merged_into IS NOT NULL)
        OR (status <> 'merged' AND merged_into IS NULL))
);

-- ---------------------------------------------------------------------------
-- 2. The judgment hand-off gets a typed pointer at the registry.
-- ---------------------------------------------------------------------------
-- NULLABLE on purpose: an extraction is written when the value is read out of the
-- source, and the parameter is adjudicated afterwards. NULL means "not yet
-- adjudicated", which is a real state, not a defect. parameter_canonical stays for now
-- and is writer-retired rather than dropped -- committed data migrations reference the
-- column and rule 5 says NULL forward, never DROP.
ALTER TABLE source_value_extractions
    ADD COLUMN parameter_id INTEGER REFERENCES base_parameters(parameter_id);

-- ---------------------------------------------------------------------------
-- 3. specifications, re-keyed.
-- ---------------------------------------------------------------------------
DROP TABLE specifications;

CREATE TABLE specifications (
    specification_id                INTEGER PRIMARY KEY,
    -- THE SUBJECT (owner 2026-08-26). Was item_code NOT NULL into an emptied table,
    -- which is why no determination could be written at all.
    parameter_id                    INTEGER NOT NULL REFERENCES base_parameters(parameter_id),
    -- THE FOUR LENSES (owner 2026-08-28; CHECK relaxed by D-0182). population_code is
    -- retired in favour of these. NULL in a lens means "this determination is not
    -- stated in that lens", which is legitimate; stating several at once is the ideal.
    identity_code                   TEXT REFERENCES populations(population_code),
    icf_code                        TEXT REFERENCES axes(axis_code),
    needs_code                      TEXT REFERENCES access_needs(need_code),
    medical_code                    TEXT REFERENCES base_taxonomy_medical(medical_code),
    state                           TEXT NOT NULL
                                    CHECK (state IN ('stated', 'provisional',
                                                     'pending', 'not_applicable')),
    design_scale                    TEXT
                                    CHECK (design_scale IN ('universal', 'population', 'person')),
    convergence_id                  INTEGER REFERENCES convergence_assessment(convergence_id),
    confidence_dimensions_present   TEXT,   -- JSON array
    confidence_dimensions_absent    TEXT,   -- JSON array
    confidence_synthesis_basis      TEXT,
    gap_register_id                 TEXT REFERENCES gaps(gap_id),
    not_applicable_rationale        TEXT,
    tier_basis                      TEXT,
    governing_refs                  TEXT CHECK (governing_refs IS NULL OR json_valid(governing_refs)),
    rule_version                    TEXT,
    derivation_sha                  TEXT,
    code_floor_only                 INTEGER NOT NULL DEFAULT 0
                                    CHECK (code_floor_only IN (0, 1)),
    value_min                       REAL,
    value_max                       REAL,
    value_unit                      TEXT,
    falsification_condition         TEXT,
    has_unverified_sources          INTEGER NOT NULL DEFAULT 0
                                    CHECK (has_unverified_sources IN (0, 1)),
    all_sources_disqualified        INTEGER NOT NULL DEFAULT 0
                                    CHECK (all_sources_disqualified IN (0, 1)),
    regulatory_stratum_only         INTEGER NOT NULL DEFAULT 0
                                    CHECK (regulatory_stratum_only IN (0, 1)),
    created_at                      TEXT,
    created_by_session              TEXT,
    updated_at                      TEXT,
    updated_by_session              TEXT,
    -- D-0182, mechanised: absence in a lens is fine, absence in ALL of them is not.
    CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)
);

-- The row identity the old UNIQUE (item_code, population_code) used to state. COALESCE
-- to '' because SQLite treats NULLs as distinct in a UNIQUE index, so two rows both
-- naming only identity_code would otherwise never collide. Mirrors idx_itl_row_identity.
CREATE UNIQUE INDEX idx_spec_row_identity ON specifications(
    parameter_id,
    COALESCE(identity_code, ''), COALESCE(icf_code, ''),
    COALESCE(needs_code, ''),    COALESCE(medical_code, '')
);

-- ---------------------------------------------------------------------------
-- 4. v_value_independence re-derived. 2026-08-26 ACTION (4), verbatim:
--    "v_value_independence still groups by population_code; under this ruling population
--    is a cross-reference, so that view's grain is re-derived in the same change or an
--    independence count fragments across populations."
-- ---------------------------------------------------------------------------
-- Population leaves the grain. parameter_id joins it, and the text parameter remains as
-- the fallback label while extractions are still being adjudicated (parameter_id NULL).
-- Swept first: no executable caller SELECTs from this view -- only the baseline that
-- defines it, plus prose in evidence-architecture.md and the contract.
DROP VIEW IF EXISTS v_value_independence;
CREATE VIEW v_value_independence AS
    SELECT parameter_id,
           COALESCE(parameter_canonical, parameter) AS parameter_label,
           COUNT(DISTINCT COALESCE(root_ref_id, root_id)) AS independent_root_count
    FROM source_value_extractions
    WHERE root_type IN ('measurement_primary', 'participatory_finding',
                        'derived_calculation')
      AND (root_ref_id IS NOT NULL
           OR root_id IN (SELECT root_id FROM external_root_registry))
    GROUP BY parameter_id, COALESCE(parameter_canonical, parameter);

PRAGMA user_version = 71;
