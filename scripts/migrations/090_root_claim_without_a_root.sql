-- 090_root_claim_without_a_root.sql
--
-- A ROW THAT CLAIMS A PRIMARY MEASUREMENT AND NAMES NO ROOT IS THE ONE CASE THE ROOT
-- VIEW COULD NOT SEE.
--
-- WHAT WENT WRONG, MEASURED ON THE BATCH THAT WROTE THIS. Batch 19 wrote extraction 57
-- with root_type='measurement_primary', root_ref_id NULL and root_id NULL: a value
-- REF-01005 did not measure (it tested 1:12, 1:16 and 1:20 only), attributed to a 1957
-- dissertation this corpus does not hold. The prose in root_classification_basis said so
-- honestly. THE TYPED COLUMNS SAID "a primary measurement whose root is nothing", and no
-- gate could contradict them.
--
-- `v_unregistered_roots` exists for exactly this -- a root held outside the corpus -- and
-- its WHERE opened `sve.root_id IS NOT NULL`. So it examines rows that NAME an external
-- root and are missing its registry entry, and it is blind to the strictly worse case:
-- a row that names no root at all. `v_value_independence` drops the same rows from
-- independent_root_count silently. The blind spot was named in db.py's own comment when
-- root_type was made amendable, and making the repair path is not the same as closing it:
-- the next `add-extraction --root-type measurement_primary` with both columns null is
-- still invisible.
--
-- WHAT THIS CHANGES. The view keeps its existing subject and gains the missing one, with
-- a `defect` column saying which case each row is, because they are not the same problem
-- and a reader fixing them needs to know:
--
--   'unregistered'  -- names an external root_id with no external_root_registry entry.
--                      The original subject, unchanged.
--   'rootless'      -- claims a rooted root_type and names NO root at all, by either
--                      column. Nothing to register and nothing to point at.
--
-- 'untraced' is deliberately NOT a defect. It is the vocabulary's own word for "the root
-- is not known", so a row that says untraced and names nothing is consistent, which is
-- exactly what extraction 57 was corrected TO. The rooted types are the three that assert
-- a provenance a reader could in principle follow.
--
-- NO DATA CHANGES. This is a view definition only; the one row that provoked it was
-- already corrected to 'untraced' by data_20260920041301. The view is expected to render
-- 0 rows immediately after this migration, and that is a real 0 rather than a vacuous
-- one -- CLAUDE.md rule 4's "treat a 0-row object as unproven, not clean" applies, so the
-- falsifier is stated here: write an extraction with root_type='measurement_primary' and
-- no root and it must appear.
--
-- AFTER_DATA: 20260920041301

DROP VIEW IF EXISTS v_unregistered_roots;

CREATE VIEW v_unregistered_roots AS
    SELECT sve.extraction_id,
           sve.slug,
           sve.parameter_id,
           t.canonical_en AS parameter_label,
           sve.root_id,
           'unregistered' AS defect
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_id IS NOT NULL
      AND sve.root_ref_id IS NULL
      AND NOT EXISTS (
          SELECT 1 FROM external_root_registry err
          WHERE err.root_id = sve.root_id)

    UNION ALL

    SELECT sve.extraction_id,
           sve.slug,
           sve.parameter_id,
           t.canonical_en AS parameter_label,
           sve.root_id,
           'rootless' AS defect
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_id IS NULL
      AND sve.root_ref_id IS NULL
      AND sve.root_type IN ('measurement_primary', 'participatory_finding',
                            'committee_assertion');

PRAGMA user_version = 90;
