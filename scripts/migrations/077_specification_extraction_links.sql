-- 077_specification_extraction_links.sql
--
-- THE DETERMINATION POINTS AT THE ROWS THAT PRODUCED IT, NOT MERELY AT THEIR SOURCES.
--
-- WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS. A determination records which
-- SOURCES governed it -- `specification_source_links.ref_id`, plus the `governing_refs`
-- JSON copy. A source carries many judgment rows: evidence to judgment is 1:N (D-0168),
-- and migration 075 made those rows materially different from one another. REF-00973
-- carried a `condition` (the slopes a treadmill was set to) AND a `finding` (that
-- musculoskeletal risk rises with inclination). Recording "REF-00973 governed" says
-- neither which of those produced the figure nor under what qualifiers.
--
-- So the backward walk breaks here, and only here. From a rendered figure you can reach
-- the source and its persisted bytes; you cannot reach the sentence. A reader asking
-- "why 1200 mm, and conditional on what?" gets a bibliography.
--
-- THREE MORE THINGS THIS CLOSES, which is why it is a junction and not a column.
--
--   1. THE ATTESTATION BLIND SPOT. `derivation_sha` hashed the governing REF set plus an
--      UNFILTERED `COUNT(*)` of the parameter's extractions. Since 075, `gather_sources`
--      admits only `figure_role IN ('claim','derived')` -- so `db.py amend-extraction
--      --field figure_role --value condition` flips a cell from `stated` to `pending`
--      (the engine's own headline example) while leaving the ref set, the count, and
--      therefore the sha UNCHANGED. K01 is BLOCKING and reported CLEAN over a
--      determination whose inputs had changed. The sha's own docstring says the count was
--      added to stop two materially different cells hashing identically; the 075 predicate
--      reopened that collision through a wider door. Once the governing set is stored it is
--      recomputable in one line, so the sha can hash the SET -- which the docstring wanted
--      and could not have, because nothing stored it.
--
--   2. "WHY IS THIS PENDING?" A `pending` cell is the honest answer when nothing states a
--      value, and today it is indistinguishable from a parameter nobody has read. The
--      `excluded` role with its mandatory reason records the rows that WERE examined and
--      did not govern -- exactly the distinction the sha docstring names as cases (a) and
--      (b), now visible to a reader rather than only to a hash.
--
--   3. THE CONDITIONS TRAVEL WITH THE FIGURE. A slope means nothing without its run
--      length; `figure_role='condition'` rows are recorded at judgment and then dropped at
--      determination. `conditioning` carries them onto the determination, so the render
--      stage can state the tuple the owner asked for -- slope AND max run AND landing --
--      instead of a bare number.
--
-- WHAT IT DELIBERATELY DOES NOT DO. It does not retire `specifications.governing_refs`,
-- though it makes that retirement possible for the first time: the JSON was load-bearing
-- because `derivation_sha` hashed it, and after this it is not. Retiring it means changing
-- test_db_integrity's H01/H02 (which assert JSON-to-junction parity) and sweeping every
-- reader, which is a separate change. Recorded here so the next session knows the blocker
-- is gone rather than rediscovering it.
--
-- ROLE VOCABULARY, and why exactly three:
--   governing     the row supplied a value -- figure_role IN ('claim','derived').
--   conditioning  the row qualifies a governing row -- figure_role='condition'.
--   excluded      the row exists for this parameter and did not govern. Carries a
--                 MANDATORY reason, because "excluded" without one is the same silence
--                 this table exists to break.
--
-- No `superseded` role: a determination is not edited in place (there is no
-- re-determination path -- `idx_spec_row_identity` is UNIQUE and the supersede design is
-- an open owner decision), so a link never changes meaning after it is written.

CREATE TABLE specification_extraction_links (
    specification_id    INTEGER NOT NULL
                        REFERENCES specifications(specification_id),
    extraction_id       INTEGER NOT NULL
                        REFERENCES source_value_extractions(extraction_id),
    role                TEXT NOT NULL
                        CHECK (role IN ('governing', 'conditioning', 'excluded')),
    -- Why this row did not govern. Free text by design: the reasons are the engine's
    -- own vocabulary (tier non-anchoring, figure_role, superseded source) and pinning
    -- them to a CHECK here would be a second home for rules that live in assess_cell.
    exclusion_reason    TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    PRIMARY KEY (specification_id, extraction_id),
    -- A reason is required for an exclusion and meaningless otherwise.
    CHECK ((role =  'excluded' AND exclusion_reason IS NOT NULL)
        OR (role <> 'excluded' AND exclusion_reason IS NULL))
);

-- The backward walk: given an extraction, which determinations rest on it. Without this
-- index that question is a table scan, and it is the question a retraction asks -- "this
-- source was withdrawn; what did it hold up?"
CREATE INDEX idx_sxl_extraction ON specification_extraction_links(extraction_id);

-- THE BACKWARD WALK, AS A VIEW, because CLAUDE.md section 3 says a cross-stage view IS the
-- pointer and is the most protected object in the schema. This one spans specification ->
-- judgment -> evidence in a single hop, so the question "what is this determination made
-- of" is one SELECT rather than a join a reader has to reconstruct correctly each time.
CREATE VIEW v_determination_provenance AS
SELECT s.specification_id,
       s.parameter_id,
       t.canonical_en                AS parameter_name,
       s.state,
       COALESCE(s.identity_code, s.icf_code, s.needs_code, s.medical_code) AS lens,
       l.role,
       l.exclusion_reason,
       x.extraction_id,
       x.figure_role,
       x.comparator,
       x.claimed_value,
       x.claimed_unit,
       x.claim_text,
       x.ref_id,
       e.tier,
       e.evidence_type,
       e.verification_status
  FROM specifications s
  JOIN specification_extraction_links l ON l.specification_id = s.specification_id
  JOIN source_value_extractions       x ON x.extraction_id    = l.extraction_id
  JOIN base_parameters                p ON p.parameter_id     = s.parameter_id
  JOIN terms                          t ON t.term_id          = p.term_id
  LEFT JOIN evidence_sources          e ON e.ref_id           = x.ref_id;

PRAGMA user_version = 77;
