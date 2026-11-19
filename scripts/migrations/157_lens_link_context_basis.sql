-- 157_lens_link_context_basis.sql
-- SCHEMA migration (T-126). No data rows. A code value's lens is judged by the session that records it, from the
-- clause and its context, with its warrant (OD-65, "use contextual judgment"; the sixteenth set of 2026-11-14,
-- "at the moment of recording the row is when you will have best idea of context"; "yes lens in judgment"; as
-- corrected 2026-11-15: the recording session judges and writes the identity link, the maps only propose):
--   grep -n -F "Correction and registration 2026-11-15" references/project-standards.md
--
--   1. `basis` admits one more value, `context`: the clause's context (what it is for, where it applies: a mounting
--      height, a clearance, the building type or use, the group or need its section serves, its applicability)
--      warrants the link, by the recording session's judgment. The writer (db._require_lens_warrant) admits it only
--      on a source of tier 4 or above (the regulatory stratum): the owner moved the assignment for code values only.
--   2. One new cell, `basis_reason`: the session's judgment in its own words ("typically concerns wheelchair users"),
--      present exactly when the basis is `context` and never blank. `basis_text` keeps its meaning, the words the
--      source holds (for a context link, the words that state the context: "mounting height"), so the owner's warrant
--      "mounting height; typically concerns wheelchair users" is two cells, each in the cell that names it.
--   3. v_live_lens_links gains `basis_reason` after `basis_text`.
--
-- SQLite cannot alter a CHECK in place, so the table is rebuilt: the view that reads it comes down first, a new table
-- is built under a temporary name from the live DDL with only the two changes above, every row is copied by column name
-- (basis_reason NULL on every row), the old table is dropped, the new one renamed, its five indexes recreated from their
-- stored text, the AUTOINCREMENT floor restored (migration 076: an identifier is never reissued) and the view recreated.
-- No table holds a foreign key into extraction_lens_links, and no other view or trigger names it or its view (derive:
--   select name from sqlite_master where sql like '%extraction_lens_links%' or sql like '%v_live_lens_links%').
--
-- ORDER: migration 131's AFTER_DATA marker already places every schema migration numbered after it, this one included,
-- after the committed data migrations that write lens columns, so this rebuild copies every carried link; no marker of
-- its own is needed. `carried` stays in the CHECK while live rows hold it (T-127 and T-115 judge them).

CREATE TEMP TABLE _157_seq AS SELECT name, seq FROM sqlite_sequence WHERE name = 'extraction_lens_links';

DROP VIEW "v_live_lens_links";

CREATE TABLE "_157_new_extraction_lens_links" (
    link_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    extraction_id       INTEGER NOT NULL REFERENCES source_value_extractions(extraction_id),
    -- THE THREE LENSES, typed, one per row (2026-08-28 shape; "never two lenses in one row").
    identity_code       TEXT REFERENCES base_taxonomy_identity(identity_code),
    icf_code            TEXT REFERENCES base_icf(icf_code),
    needs_code          TEXT REFERENCES access_needs(need_code),
    -- THE WARRANT (rule 8: a judgment records its answer and its evidence in named columns).
    --   named_in_text       the figure's own words name the users / function / need (D-2)
    --   heading             the provision names no one; its heading names the group (OD-31)
    --   study_participants  a study's own participants are this group (2026-08-25 grade rule)
    --   context             a code value (tier 4 to 6) whose clause names no group: its context warrants the link, by
    --                       the recording session's judgment (OD-65; sixteenth set, as corrected 2026-11-15)
    --   carried             moved by migration 131 from the retired column; no judged warrant yet
    basis               TEXT NOT NULL CHECK (basis IN
                            ('named_in_text', 'heading', 'study_participants', 'context', 'carried')),
    basis_text          TEXT,          -- the exact words that warrant the link (for `context`: the words stating the context)
    basis_reason        TEXT,          -- `context` only: the recording session's judgment, in its own words
    retired_at          TEXT,
    retired_by_session  TEXT,
    retirement_reason   TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    CHECK ((identity_code IS NOT NULL) + (icf_code IS NOT NULL)
         + (needs_code IS NOT NULL) = 1),
    CHECK ((basis = 'carried') = (basis_text IS NULL)),
    CHECK (basis_text IS NULL OR length(trim(basis_text)) > 0),
    CHECK ((basis = 'context') = (basis_reason IS NOT NULL)),
    CHECK (basis_reason IS NULL OR length(trim(basis_reason)) > 0),
    CHECK ((retired_at IS NULL) = (retired_by_session IS NULL)
       AND (retired_at IS NULL) = (retirement_reason IS NULL))
);

INSERT INTO "_157_new_extraction_lens_links" ("link_id", "extraction_id", "identity_code", "icf_code", "needs_code", "basis", "basis_text", "retired_at", "retired_by_session", "retirement_reason", "created_at", "created_by_session", "updated_at", "updated_by_session") SELECT "link_id", "extraction_id", "identity_code", "icf_code", "needs_code", "basis", "basis_text", "retired_at", "retired_by_session", "retirement_reason", "created_at", "created_by_session", "updated_at", "updated_by_session" FROM "extraction_lens_links";
DROP TABLE "extraction_lens_links";
ALTER TABLE "_157_new_extraction_lens_links" RENAME TO "extraction_lens_links";
CREATE UNIQUE INDEX ux_extraction_lens_live ON extraction_lens_links
    (extraction_id, COALESCE(identity_code, ''), COALESCE(icf_code, ''),
     COALESCE(needs_code, ''))
    WHERE retired_at IS NULL;
CREATE INDEX ix_ell_extraction ON extraction_lens_links(extraction_id);
CREATE INDEX ix_ell_identity   ON extraction_lens_links(identity_code) WHERE retired_at IS NULL;
CREATE INDEX ix_ell_icf        ON extraction_lens_links(icf_code)      WHERE retired_at IS NULL;
CREATE INDEX ix_ell_needs      ON extraction_lens_links(needs_code)    WHERE retired_at IS NULL;

DELETE FROM sqlite_sequence WHERE name = 'extraction_lens_links';
INSERT INTO sqlite_sequence (name, seq) SELECT name, seq FROM _157_seq;
DROP TABLE _157_seq;

CREATE VIEW v_live_lens_links AS
SELECT link_id, extraction_id, identity_code, icf_code, needs_code,
       basis, basis_text, basis_reason, created_at, created_by_session
  FROM extraction_lens_links
 WHERE retired_at IS NULL;

PRAGMA user_version = 157;
