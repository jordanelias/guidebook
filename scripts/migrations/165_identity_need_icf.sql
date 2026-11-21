-- 165_identity_need_icf.sql
-- SCHEMA migration -- the judged identity, access-need and ICF matrix (T-145). Tooling, no research rows: the triples
-- that fill it are a later research pull request the owner reviews.
--
-- WHY. Owner, 2026-11-20: readers will navigate the repository first by a disability identity, and "you basically need
-- to have a big 3D matrix of ICF codes * access needs * disability identities" ("yes, correct" to a table of judged
-- triples). Today an identity cannot say which access needs it has, and 11 of the 23 identities name no ICF code
-- (derive: task T-145 section 3). access_needs.absorbs holds identities as a delimited cell, which one value per cell
-- (2026-11-06) does not allow to stay the only home. Ledger: `grep -n -F "Owner statements 2026-11-20 (fifth)"
-- references/project-standards.md`.
--
-- ALL THREE KEYS, EACH NOT NULL (owner, 2026-11-20: "should be all three"). A cell of the cube has three coordinates.
-- What is known of only two is a `gaps` row (gaps carries identity_code, icf_code and needs_code), not a stored row.
-- D-0182 (at least one lens) governs a determination and is not touched.
--
-- STORED SPARSELY. A cell with no row reads as not yet judged. A `not_applicable` row reads as judged and not
-- applying. Both carry the same warrant (a quiet "does not apply" is the failure the cell states exist to prevent).
--
-- THE STATES. A session proposes a triple as `pending` (judged to apply) or `not_applicable` (judged not to). Only the
-- review verb, run on the owner's review of a batch, sets `stated` (or `provisional`, accepted with a caveat held in
-- review_note); the CHECKs below refuse a stated or provisional row with no reviewer, and a pending row with one.
-- A row the owner rejects is retired in place with the reason; a retired row is never revived (write a new one).
--
-- NOT CHANGED. identity_icf_map (61 rows), access_need_icf (43) and access_needs.absorbs stay as the maps a session
-- reads when it proposes (T-126). They propose; this table judges. `absorbs` is retired by a later schema migration
-- once triples cover every need, placed after every data migration that INSERTs it (rule 5).
--
-- No AFTER_DATA marker: the table is new, so no committed data migration can INSERT into it.
--
-- WRITERS: db.py propose-identity-need-icf, review-identity-need-icf. READERS: the view v_lens_crosswalk, read by
-- db.py lens-crosswalk (from an identity, a need or an ICF code; --uncovered lists identities and needs with no live
-- triple, which are the gaps ACTION 3 of the ledger entry says to close). All three keys are base tables, so the view
-- crosses no stage (CLAUDE.md section 3).

CREATE TABLE identity_need_icf (
    triple_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    identity_code       TEXT NOT NULL REFERENCES base_taxonomy_identity(identity_code),
    need_code           TEXT NOT NULL REFERENCES access_needs(need_code),
    icf_code            TEXT NOT NULL REFERENCES base_icf(icf_code),
    state               TEXT NOT NULL
                        CHECK (state IN ('stated', 'provisional', 'pending', 'not_applicable')),
    -- THE WARRANT, in this row's own cell: why this identity, this need and this code belong together (or why they do
    -- not, for not_applicable), in the judge's words. A source it rests on is named here; the base holds its own
    -- justification (OD-71), so there is no foreign key into evidence.
    warrant             TEXT NOT NULL CHECK (length(trim(warrant)) > 0),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    reviewed_at         TEXT,
    reviewed_by         TEXT CHECK (reviewed_by IS NULL OR length(trim(reviewed_by)) > 0),
    -- The caveat of a `provisional` row, in the reviewer's words; empty for every other state.
    review_note         TEXT CHECK (review_note IS NULL OR length(trim(review_note)) > 0),
    retired_at          TEXT,
    retired_by_session  TEXT,
    retirement_reason   TEXT,
    CHECK ((reviewed_at IS NULL) = (reviewed_by IS NULL)),
    CHECK (state NOT IN ('stated', 'provisional') OR reviewed_at IS NOT NULL),
    CHECK (state <> 'pending' OR reviewed_at IS NULL),
    CHECK ((state = 'provisional') = (review_note IS NOT NULL)),
    CHECK ((retired_at IS NULL AND retired_by_session IS NULL AND retirement_reason IS NULL)
        OR (retired_at IS NOT NULL AND retired_by_session IS NOT NULL AND length(trim(retirement_reason)) > 0))
);

CREATE UNIQUE INDEX ux_identity_need_icf_live
    ON identity_need_icf (identity_code, need_code, icf_code)
 WHERE retired_at IS NULL;

CREATE VIEW v_lens_crosswalk AS
SELECT t.triple_id, t.identity_code, i.display_name AS identity_name,
       t.need_code, n.design_obligation AS need_obligation,
       t.icf_code, c.title AS icf_title,
       t.state, t.warrant, t.reviewed_at, t.reviewed_by, t.created_by_session
  FROM identity_need_icf t
  JOIN base_taxonomy_identity i ON i.identity_code = t.identity_code
  JOIN access_needs n           ON n.need_code     = t.need_code
  JOIN base_icf c               ON c.icf_code      = t.icf_code
 WHERE t.retired_at IS NULL;

PRAGMA user_version = 165;
