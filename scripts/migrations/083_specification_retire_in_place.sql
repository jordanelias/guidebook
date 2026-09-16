-- 083_specification_retire_in_place.sql
--
-- EXECUTES THE OWNER RULING OF 2026-09-16: "retire in place then".
--
-- `specifications` was the one table the ruling most needs and the one with none of the
-- mechanism. `evidence_sources` has `superseded_by_ref_id`, `base_parameters.status`
-- admits 'retired', `source_locators.status` admits 'RETIRED' -- and migration 076's own
-- comment names all three as the half-built proof of concept while conspicuously omitting
-- the determination table. Its `state` CHECK is
-- ('stated','provisional','pending','not_applicable') with no lifecycle value at all, and
-- `idx_spec_row_identity` is UNIQUE over the whole table, so a determined cell can never
-- be determined again by any route.
--
-- WHY NOT ADD 'retired' TO `state`. `state` is the determination's EPISTEMIC state -- how
-- well the evidence supports it. Retirement is a LIFECYCLE fact. Putting them in one
-- column would destroy the record of what a retired row had concluded, which is the whole
-- value of keeping it, and would force every reader that switches on `state` to learn a
-- value that answers a different question. Rule 5 in miniature: two facts, two homes.
--
-- WHY ALTER TABLE AND A TRIGGER RATHER THAN A REBUILD. The structural-constraint argument
-- says a rebuild, so the "a retired row states why" rule lives in a CHECK the way
-- migration 082 put SCREENED-OUT's reason in one. But `specifications` carries 35 columns,
-- most NOT NULL or CHECK-constrained, and hand-transcribing them into a new table is
-- exactly the drift CLAUDE.md warns about -- a rebuild that silently loses one CHECK is a
-- worse outcome than the constraint living in a trigger. A BEFORE UPDATE trigger is just
-- as structural: it holds for ANY writer, including hand SQL, which is the property that
-- mattered.
--
-- THE PARTIAL INDEX IS THE ACTUAL SUPERSEDE MECHANISM. Restricting uniqueness to live rows
-- means one live determination per cell and any number of retired ones, which is exactly
-- the history a supersede design is for. `assess_cell.validate_cell_undetermined()` is
-- re-keyed in the same commit to ask "is there a LIVE determination" rather than "does a
-- row exist" -- migration 076 predicted this in so many words: "assess_cell's
-- re-determination refusal could key on NOT RETIRED rather than NOT EXISTS".
--
-- WHAT THIS MIGRATION DELIBERATELY DOES NOT DO: retire anything. The ruling's ACTION item 2
-- is that no row is retired until every reader that could surface it filters. Seven views
-- read this table (v_pending, v_divergence, v_best_practice, v_code_floor_only,
-- v_source_reach_all, v_item_provenance, v_determination_provenance) and they are swept in
-- the same PR. Adding the columns surfaces nothing while no row is retired.

ALTER TABLE specifications ADD COLUMN retired_at TEXT;
ALTER TABLE specifications ADD COLUMN retired_by_session TEXT;
ALTER TABLE specifications ADD COLUMN retirement_reason TEXT;
ALTER TABLE specifications ADD COLUMN superseded_by_specification_id INTEGER
    REFERENCES specifications(specification_id);

-- One LIVE determination per cell; retired rows are unconstrained history.
DROP INDEX IF EXISTS idx_spec_row_identity;
CREATE UNIQUE INDEX idx_spec_row_identity ON specifications(
    parameter_id,
    COALESCE(identity_code, ''), COALESCE(icf_code, ''),
    COALESCE(needs_code, ''),    COALESCE(medical_code, '')
) WHERE retired_at IS NULL;

-- Finding retired rows, and finding the live one, are both common reads.
CREATE INDEX idx_spec_retired ON specifications(retired_at);

-- A RETIRED DETERMINATION STATES WHY. Structural, not a convention a writer may forget:
-- this fires for hand SQL as readily as for db.py. Mirrors migration 082's CHECK on
-- source_locators.screened_reason; a trigger rather than a CHECK only because adding a
-- CHECK to this table would require rebuilding 35 constrained columns.
CREATE TRIGGER trg_spec_retire_needs_reason
BEFORE UPDATE OF retired_at ON specifications
WHEN NEW.retired_at IS NOT NULL
 AND (NEW.retirement_reason IS NULL OR TRIM(NEW.retirement_reason) = '')
BEGIN
    SELECT RAISE(ABORT, 'a retired specification must carry a retirement_reason -- retiring a determination without recording why discards the judgement it cost');
END;

PRAGMA user_version = 83;
