-- 075_extraction_relations.sql
-- SCHEMA migration -- ADDITIVE ONLY. Two nullable columns on source_value_extractions
-- plus one new junction table, one view, no DROP, no rebuild.
--
-- WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS (CLAUDE.md rule 1).
--
-- Measured against the live corpus: the four ramp-gradient extractions on parameter_id 1
-- read "1:20, 1:16, 1:12, 1:8" (extraction_id 1) and "1:8 to 1:20" (extraction_id 3) --
-- bare rise:run RATIOS. Half of them carry no run-length limit and no landing rule
-- alongside the ratio, because this table has never had a column for "this figure is
-- conditioned on a second fact" -- there is nowhere to write "and a landing is required
-- every 9 m of run" next to the slope it qualifies. Print "1:12" from that row today and
-- the book states a slope with no ceiling on how far it may run, which several ratified
-- codes (ADA 405.6, NBC 3.8) do not permit as a standalone figure. That is wrong content
-- in the rendered guidebook, not merely a thin row in the database.
--
-- Separately: extraction_id 6 (REF-00971) reads "no tested scooter completed all five
-- configurations ... within the space EXISTING STANDARDS allow" -- a T1 finding measured
-- AGAINST a code's own number, not an independent measurement establishing one. Nothing
-- on the row today distinguishes that from extraction_id 7 (REF-00976), which states an
-- enlargement OVER a surveyed baseline -- a delta, not an absolute width either. A render
-- pipeline that cannot tell "this source measured a value" from "this source tested a
-- code's number and found it wanting" can promote the CODE's own figure to a
-- ●-anchored T1 best-practice value on the strength of a study that never measured
-- an independent value at all -- exactly the class of error CLAUDE.md section 5(c) warns
-- a green gate will not catch, because every field involved is populated and none of
-- them is false; the falsity is in what the figure is stated RELATIVE TO, which no column
-- anywhere on this table has ever recorded.
--
-- THE SHAPE OF THE FIX. A comparator is either a ROW this project already holds (another
-- extraction, so the two can be joined and reasoned about together) or a LABEL naming
-- something the project has not captured as a row (a code clause, a study's own baseline
-- sample, a source that names no standard at all). `extraction_relations` records which,
-- and the four lens columns on `specifications` (owner 2026-08-28) are the precedent for
-- doing this as a typed, checked, real structure rather than a free-text afterthought.
--
-- WHY ADDITIVE ONLY, NOT A REKEY LIKE 073. Nothing about the evidence->judgment hand-off
-- changes -- `source_value_extractions.ref_id` stays NOT NULL into `evidence_sources`,
-- and NO UNIQUE index is added anywhere on that table. `scripts/audit/judgment_handoff_shape.py`
-- (BLOCKING) polices exactly this shape and this migration gives it nothing to fail on.
-- SQLite's ALTER TABLE ADD COLUMN accepts a column-level CHECK and a column-level
-- REFERENCES; it refuses ADD COLUMN NOT NULL without a DEFAULT once a table holds rows
-- (verified against a scratch copy of this table's own row count before writing this
-- file), which is why both new columns below are nullable. It also refuses a table-level
-- ADD CONSTRAINT outright ("near CONSTRAINT: syntax error", verified the same way), which
-- is why every new rule on `extraction_relations` is written into that table's own
-- CREATE TABLE rather than bolted on afterward.

-- ---------------------------------------------------------------------------
-- 1. Two columns on the judgment item. Both start NULL on every existing row; NULL
--    means "not yet graded", the same posture `db.py add-extraction` already takes for
--    `claim_text` -- required at the CLI, not at the schema, because the schema cannot
--    demand a value of eight rows that already exist without one. Grading these two is a
--    later writer's job and a later integrity check's job, not this migration's.
-- ---------------------------------------------------------------------------

-- figure_role -- WHAT KIND OF NUMBER THIS ROW IS, separate from whether it is TRUE.
--   claim     -- the source's own headline assertion for this parameter; what most rows
--               written before this migration would be graded, once graded.
--   finding   -- a result the source reports incidentally while investigating something
--               else -- REF-00971's "no scooter completed all five configurations" is a
--               finding about existing standards, not a claim about corridor width.
--   condition -- a qualifier that only means something attached to another row: a run
--               length, a landing rule, a duration, a population subset. Never printed
--               alone.
--   derived    -- computed from other rows this project holds, never read off the source
--               directly. `v_derived_figure_check` below is what re-derives it.
ALTER TABLE source_value_extractions ADD COLUMN figure_role TEXT
  CHECK (figure_role IS NULL OR figure_role IN ('claim', 'finding', 'condition', 'derived'));

-- comparator -- THE ARITHMETIC RELATION BETWEEN THE STORED VALUE AND WHAT IT IS STATED
-- AGAINST, when the row has one. A bare number carries none: comparator is NULL, not '='.
--   =        -- the source states the value holds exactly, with nothing above or below.
--   <        -- the source states an upper bound the value must stay under.
--   <=       -- the same bound, stated as inclusive.
--   >        -- the source states a lower bound the value must clear.
--   >=       -- the same bound, stated as inclusive.
--   between  -- the source states a range; claimed_value carries both ends, as the range
--             rows on this table already do today (e.g. extraction_id 1's "1:20, 1:16,
--             1:12, 1:8").
--   approx   -- the source hedges the value itself ("approximately", "around") rather
--             than bounding it.
ALTER TABLE source_value_extractions ADD COLUMN comparator TEXT
  CHECK (comparator IS NULL OR comparator IN ('=', '<', '<=', '>', '>=', 'between', 'approx'));

-- ---------------------------------------------------------------------------
-- 2. extraction_relations -- the junction that records what a figure is stated relative
--    to. One row per comparator edge; an extraction with no comparator gets no row here,
--    which is the correct representation of "this figure needed nothing else."
-- ---------------------------------------------------------------------------
CREATE TABLE extraction_relations (
  relation_id         INTEGER PRIMARY KEY AUTOINCREMENT,

  -- THE FIGURE THIS EDGE QUALIFIES. NOT NULL and a real FK -- an edge naming no source
  -- row describes nothing. No UNIQUE index touches this column alone: one extraction may
  -- carry several comparator edges (a ramp slope is both condition_on a run-length limit
  -- AND audited_against a code's stated maximum), and collapsing that to one row per
  -- extraction would force a choice this table exists to avoid forcing.
  from_extraction_id  INTEGER NOT NULL REFERENCES source_value_extractions(extraction_id),

  -- WHAT KIND OF COMPARISON THIS EDGE IS. Eight values; the CHECK is the vocabulary
  -- (CLAUDE.md section 4) and this is only its meaning, one line each.
  --   tested_at        -- the source physically measured its subjects at/against this
  --                      referent -- REF-00973's four ramp slopes were each tested_at a
  --                      named gradient.
  --   audited_against  -- the source measured whether subjects could perform WITHIN a
  --                      referent's own stated limit, rather than measuring an
  --                      independent value -- REF-00971's "existing standards".
  --   confirms         -- an independent measurement agrees with the referent's value.
  --   insufficient     -- the source asserts the referent's value is NOT ENOUGH for the
  --                      population or task in question -- REF-00784's 10-100% figure.
  --   exceeds          -- the source asserts the referent's value is more than needed.
  --   delta_over       -- the source states an increment relative to a baseline rather
  --                      than an absolute figure -- REF-00976's "more than thirty
  --                      centimetres of enlargement over the surveyed stock".
  --   condition_on     -- this figure only holds given a second figure this project also
  --                      holds as a row -- a slope given its run-length limit.
  --   derived_from     -- this figure is computed from the referent, never read off a
  --                      source -- always paired with input_role below and always a row
  --                      referent, never a label; see the CHECK immediately following.
  relation            TEXT NOT NULL CHECK (relation IN (
                        'tested_at', 'audited_against', 'confirms', 'insufficient',
                        'exceeds', 'delta_over', 'condition_on', 'derived_from')),

  -- THE REFERENT, HALF A: a row this project already holds. Nullable -- see to_label.
  -- Self-joins to the same table this column sits on, which is why the identity CHECK
  -- below refuses an edge from a row to itself.
  to_extraction_id    INTEGER REFERENCES source_value_extractions(extraction_id),

  -- THE REFERENT, HALF B: prose naming what to_extraction_id would otherwise point at,
  -- for a referent this project has not captured as its own row -- a code clause never
  -- extracted on its own parameter, a source's private baseline sample, or a referent the
  -- source itself never names. Exactly one of this column and to_extraction_id is set on
  -- every row; the CHECK enforcing that sits with the rest below, not here, because it
  -- names both columns together.
  to_label            TEXT,

  -- WHAT SORT OF THING to_label NAMES, when it is set. Meaningless and left NULL when
  -- the referent is a row instead -- a row already carries this information in its own
  -- data.
  --   standard      -- a code, guideline or published standard's own stated figure.
  --   own_sample    -- the source's own baseline measurement of its own subjects or
  --                   stock, as in REF-00976's surveyed housing.
  --   prior_source  -- an earlier study or publication, distinct from a code and from the
  --                   citing source's own sample.
  --   unnamed       -- the source itself does not say what the referent is. See the
  --                   `stated` column: this value and 'unnamed' there always travel
  --                   together, by CHECK.
  to_kind             TEXT CHECK (to_kind IS NULL OR to_kind IN (
                        'standard', 'own_sample', 'prior_source', 'unnamed')),

  -- HOW EXPLICITLY THE SOURCE ITSELF NAMES THE REFERENT -- independent of whether this
  -- project could resolve it to a row. NOT NULL: every edge takes a position on this.
  --   named     -- the source identifies the referent by name (a code number, an author,
  --              a described sample).
  --   unnamed   -- the source gestures at a referent ("existing standards") without
  --              naming which one. Never a row referent -- see the CHECK below; naming
  --              nothing is not the same claim as naming a specific row.
  --   inferred  -- the source names no referent at all and this project supplied one from
  --              context (a code the jurisdiction and date make unambiguous). The
  --              weakest of the three and the one most likely to need revisiting.
  stated              TEXT NOT NULL CHECK (stated IN ('named', 'unnamed', 'inferred')),

  -- WHICH SIDE OF A DERIVATION this edge supplies. Meaningful only for relation =
  -- 'derived_from', enforced by CHECK -- every other relation leaves it NULL.
  --   base    -- the starting figure the derived value is computed from.
  --   delta   -- the increment added to (or subtracted from) the base.
  --   factor  -- a multiplier applied to the base, for a derivation `v_derived_figure_check`
  --            does not itself recompute -- that view covers base+delta only; a
  --            factor-based derivation is a known residual, not a silent gap, recorded
  --            here rather than built speculatively (CLAUDE.md section 8).
  input_role          TEXT CHECK (input_role IS NULL OR input_role IN ('base', 'delta', 'factor')),

  -- THE SOURCE'S OWN WORDS FOR THE COMPARISON, NOT NULL. Mirrors the verbatim discipline
  -- `observed_terms.context_quote` and `db.py add-extraction`'s required `--claim-text`
  -- already carry on this project's other judgment-stage rows: a comparator asserted with
  -- nothing of the source's own phrasing behind it is not a comparator this project has
  -- actually read.
  quote               TEXT NOT NULL,

  notes               TEXT,

  created_at          TEXT NOT NULL,
  created_by_session  TEXT NOT NULL,

  -- An edge cannot compare a figure to itself.
  CHECK (to_extraction_id IS NULL OR to_extraction_id <> from_extraction_id),

  -- The referent is named as a row or as a label; never as both at once and never as
  -- neither, or the edge would point at two things or at nothing.
  CHECK ((to_extraction_id IS NULL) <> (to_label IS NULL)),

  -- You cannot be conditioned by, or computed from, a figure that does not exist as a
  -- row: condition_on and derived_from both require a resolvable to_extraction_id.
  CHECK (relation NOT IN ('condition_on', 'derived_from') OR to_extraction_id IS NOT NULL),

  -- input_role names which side of a derivation this edge is, so it is meaningless
  -- outside relation = 'derived_from' and mandatory inside it.
  CHECK (
    (relation = 'derived_from' AND input_role IS NOT NULL)
    OR (relation <> 'derived_from' AND input_role IS NULL)
  ),

  -- An unnamed referent cannot simultaneously be one specific known row: if the source
  -- does not say what it is, this project cannot have resolved it to a row either.
  CHECK (stated <> 'unnamed' OR to_extraction_id IS NULL),

  -- Calling the referent's kind 'unnamed' is a claim about how the source stated it, so
  -- it must agree with the stated column rather than disagree with it.
  CHECK (to_kind IS NULL OR to_kind <> 'unnamed' OR stated = 'unnamed')
);

-- One edge is one fact; writing the identical edge twice is a duplicate, not a second
-- fact, and the COALESCE pair is what lets two NULL-referent rows still collide instead
-- of comparing unequal the way raw NULLs would under a plain UNIQUE index.
CREATE UNIQUE INDEX idx_xr_identity ON extraction_relations(
  from_extraction_id, relation, COALESCE(to_extraction_id, -1), COALESCE(to_label, ''));

-- Reader: anything asking "what points AT this figure" -- v_derived_figure_check below,
-- and any future audit walking the graph from a referent back to what cites it.
CREATE INDEX idx_xr_to ON extraction_relations(to_extraction_id);

-- ---------------------------------------------------------------------------
-- 3. v_derived_figure_check -- a stored derived value is an ATTESTATION a check
--    recomputes, never a number trusted on faith. Same posture as `derivation_sha` and
--    K01 (scripts/tests/test_db_integrity.py): those re-verify a determination against
--    the evidence that produced it; this re-verifies a derived figure against the base
--    and delta figures named as its own inputs.
--
--    ARITHMETIC MODELLED: recomputed = base + delta. That is what input_role names
--    'base' and 'delta' mean together, and it covers every derived_from edge pair this
--    migration's own examples need. A factor-based derivation (input_role = 'factor')
--    is NOT recomputed here -- stated as a known residual above, not silently dropped.
--
--    "PARSES AS REAL": a GLOB filter, not a full numeric parser -- it accepts a value
--    containing only digits, a decimal point, e/E or +/- (and at least one digit), which
--    is what CAST(... AS REAL) needs to have parsed something real rather than quietly
--    returning 0.0 for text like "1:12" or "12mm". Known residual: a malformed value
--    like "3.4.5" passes the filter and CAST silently reads only its "3.4" prefix, the
--    same quiet truncation SQLite's own CAST always does. No custom SQL function is
--    registered to do better -- this project's readers are plain `sqlite3.connect()`
--    calls (CLAUDE.md section 4), and a view that requires a registered function is a
--    view most callers cannot open.
--
--    UNITS: the derived row's own claimed_unit must equal both inputs' claimed_unit
--    exactly. No conversion is attempted -- mm compared against inches is a unit-mapping
--    problem, not this view's job.
--
--    Two joins onto extraction_relations, once per input_role, both filtered to
--    relation = 'derived_from' and to figure_role = 'derived' on the row being checked
--    -- a row that is not graded 'derived' has nothing here to recompute.
CREATE VIEW v_derived_figure_check AS
SELECT
    d.extraction_id                                              AS derived_id,
    CAST(d.claimed_value AS REAL)                                 AS stored,
    CAST(b.claimed_value AS REAL)                                 AS base_value,
    CAST(e.claimed_value AS REAL)                                 AS delta_value,
    CAST(b.claimed_value AS REAL) + CAST(e.claimed_value AS REAL) AS recomputed
FROM source_value_extractions d
JOIN extraction_relations rb
  ON rb.from_extraction_id = d.extraction_id
 AND rb.relation = 'derived_from'
 AND rb.input_role = 'base'
JOIN source_value_extractions b ON b.extraction_id = rb.to_extraction_id
JOIN extraction_relations rd
  ON rd.from_extraction_id = d.extraction_id
 AND rd.relation = 'derived_from'
 AND rd.input_role = 'delta'
JOIN source_value_extractions e ON e.extraction_id = rd.to_extraction_id
WHERE d.figure_role = 'derived'
  AND d.claimed_value GLOB '*[0-9]*' AND d.claimed_value NOT GLOB '*[^0-9.eE+-]*'
  AND b.claimed_value GLOB '*[0-9]*' AND b.claimed_value NOT GLOB '*[^0-9.eE+-]*'
  AND e.claimed_value GLOB '*[0-9]*' AND e.claimed_value NOT GLOB '*[^0-9.eE+-]*'
  AND d.claimed_unit = b.claimed_unit
  AND d.claimed_unit = e.claimed_unit;

PRAGMA user_version = 75;
