-- 074_medical_lens_crossings.sql
-- SCHEMA migration — the fourth lens gets the structure the other three already have.
-- No new doctrine. D-0170 adopted the medical lens on 2026-08-27 and it has had a table
-- with no columns to point with and no writer to fill it ever since.
--
-- THE RULING THIS EXECUTES, and the correction that changes HOW.
--
--   D-0170 (decisions/DR-2026-08-27-four-taxonomies-are-browsing-lenses.md), RATIFIED ON
--   CONTACT. The owner: "yes we include the medical model too. we give our users the
--   choice of what model they want to use to browse the site." Its structural clause read
--   "lens-switching runs through the crossing maps, so a medical taxonomy needs the same
--   crossings into the other three or the lens cannot switch."
--
--   THAT CLAUSE IS SUPERSEDED, and a session obeying it literally would build the wrong
--   thing while correctly citing a ratified DR. D-0184
--   (DR-2026-09-01-the-lens-is-a-column-not-a-traversal.md) measured that traversal
--   manufactures inference and made the lens a COLUMN: render is `WHERE medical_code = ?`.
--   So the crossings below are NOT the render path. They are (a) the authoring aid that
--   lets a row state its other lens codes without inferring them, and (b) the only way to
--   measure medical-lens coverage at all. Both are real; neither is traversal.
--
--   D-0182's own evidence named this gap by the numbers: "11 tables can express identity,
--   3 icf, 2 needs, 0 medical." This migration moves the last figure off zero.
--
-- ⚠ THE CONTENT HALF IS BLOCKED, AND THE EMPTY TABLE AFTER THIS MIGRATION IS NOT AN
-- UNEXECUTED RULING. See scratchpad/pr-134-repository-orientation/MEDICAL-LENS-LICENSING-STOP.md.
-- Licensing is DG-NON item 7 (governance/decision-protocol.md:81) and the owner delegation
-- D-0188 enumerated the vocabulary's CONTENT, never its licensing. The guidebook publishes
-- under CC BY-SA 4.0 (governance/legal-regulatory.md:130), share-alike; ICD-11 is WHO
-- copyright under WHO's own terms. Whether those terms are compatible is UNVERIFIED and is
-- to be settled by reading WHO's current Terms of Use, never from a model's recollection --
-- that is the same rule that governs a bibliographic field (CLAUDE.md §5(c)), applied to a
-- vocabulary. Until it is settled: structure yes, WHO-derived prose no.
--
-- WHAT IS DELIBERATELY ABSENT, so silence is not read as oversight:
--
--   NO medical<->needs MAP. There is no identity<->needs map either. Needs are reached
--   through the `axes` hub (access_need_axis_map), and the medical lens takes the same
--   route. Building a fourth pairwise map that duplicates a two-hop path already available
--   would be apparatus whose absence costs the book nothing (CLAUDE.md §8), and a second
--   route to one fact is rule 5's dual home in map form.
--
--   NO 'ALIAS' IN icf_medical_map.role, though population_axis_map.role carries it. ALIAS
--   there means the population IS the axis under another name. A diagnosis is never an
--   alias of a functional demand -- that conflation is the medical model as frame, which
--   D-0170's rationale exists to refuse. Three roles, not four, and the divergence from
--   the parallel table is intentional.
--
--   mapping_confidence IS NOT access_need_icf.confidence. That column is ('confirmed',
--   'proposed') and records whether a mapping is RATIFIED. This one records how strongly
--   the diagnosis predicts the functional demand, on the four-value scale ratified
--   2026-07-21 in governance/functional-taxonomy.md §3.2 -- a scale that has never had a
--   table to live in. Two different questions; two different columns; neither renamed to
--   look like the other.

CREATE TABLE identity_medical_map (
  identity_code      TEXT NOT NULL REFERENCES populations(population_code),
  medical_code       TEXT NOT NULL REFERENCES base_taxonomy_medical(medical_code),
  -- 'names'          -- same subject under a clinical name
  -- 'member_of'      -- the identity row is a ratified umbrella containing this diagnosis
  -- 'identity_first' -- the community does not describe itself by this diagnosis; the
  --                     crossing is navigation ONLY, and populations.display_name is what
  --                     renders. functional-taxonomy §3.3: identity profiles carry no ICD
  --                     anchor -- still true, because the anchor lives on the medical row.
  relationship       TEXT NOT NULL CHECK (relationship IN ('names','member_of','identity_first')),
  note               TEXT,
  created_at         TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (identity_code, medical_code)
);

CREATE TABLE icf_medical_map (
  icf_code           TEXT NOT NULL REFERENCES axes(axis_code),
  medical_code       TEXT NOT NULL REFERENCES base_taxonomy_medical(medical_code),
  role               TEXT NOT NULL CHECK (role IN ('PRIMARY','SECONDARY','SITUATIONAL')),
  mapping_confidence TEXT NOT NULL
                       CHECK (mapping_confidence IN ('high_predictive','moderate','low','minimal')),
  note               TEXT,
  created_at         TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (icf_code, medical_code)
);

-- THE ANCHOR IS A POINTER, AND THAT IS THE POINT. A bare classification code is a fact;
-- the describing prose is ours. This is rule 5 ("point, do not copy") and the licensing
-- constraint above arriving at the same design independently, which is the strongest
-- agreement available. Comma-separated, mirroring axes.icf_b_anchors rather than inventing
-- a shape.
ALTER TABLE base_taxonomy_medical ADD COLUMN icd11_anchors TEXT;

-- NULL MEANS "NOT VERIFIED", AND IT IS MEANT TO BE READABLE AS THAT. Set only from a
-- payload persisted under retrieval-log/ that contains the code -- the same artefact
-- discipline retrieval_log.py enforces for a citation. Measured 2026-09-11 from this
-- container: no WHO credentials present, id.who.int/icd/release/11/mms -> 401, the token
-- endpoint -> 400. So every anchor written here today lands NULL, and the integrity check
-- reports the count rather than letting the absence pass as verification.
ALTER TABLE base_taxonomy_medical ADD COLUMN icd11_verified_at TEXT;

PRAGMA user_version = 74;
