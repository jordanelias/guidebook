-- 166_identity_need_icf_owner_review.sql
-- SCHEMA migration -- compensating migration for 165 (T-145), made after the adversarial pass on it. 165 is committed,
-- so it is not edited (rule 3); the table it made is EMPTY on every database (no triple has been written: derive
-- `select count(*) from identity_need_icf`), so it is dropped and recreated rather than altered. Tooling, no rows.
--
-- WHAT THE PASS FOUND, and what this changes:
--  1. "Only the owner's review makes a row stated" was held by nothing: `reviewed_by` was free text, and the session
--     that ran the review was recorded nowhere. A review is now BOUND to the owner's words, as retire-identity and
--     add-jurisdiction already bind theirs: `review_ref` is the heading of a dated ledger entry that begins "Owner" and
--     names the triple as the token TRIPLE-<id>. `reviewed_by` is gone (the entry says who); `reviewed_session` records
--     the session that ran the verb.
--  2. A reject discarded who authorised it. `retirement_ref` holds the owner entry that rejected the row.
--  3. "Never revived" was a sentence. The trigger below makes the schema refuse an edit of a retired row, of a row's
--     three keys, warrant or origin, and of a review once recorded (a data migration rendered by emit_batch_sql can
--     carry an UPDATE).
--  4. Unchanged, and now read: `review_note` and the retirement cells appear on `lens-crosswalk` (the view carries the
--     caveat and the owner entry; `--retired` lists the rejected rows with their reasons).
--
-- WRITERS: db.py propose-identity-need-icf, review-identity-need-icf. READERS: v_lens_crosswalk, read by db.py
-- lens-crosswalk (--retired reads the table). No AFTER_DATA marker: the table is new to every data migration.

DROP VIEW IF EXISTS v_lens_crosswalk;
DROP TABLE identity_need_icf;

CREATE TABLE identity_need_icf (
    triple_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    identity_code       TEXT NOT NULL REFERENCES base_taxonomy_identity(identity_code),
    need_code           TEXT NOT NULL REFERENCES access_needs(need_code),
    icf_code            TEXT NOT NULL REFERENCES base_icf(icf_code),
    state               TEXT NOT NULL
                        CHECK (state IN ('stated', 'provisional', 'pending', 'not_applicable')),
    warrant             TEXT NOT NULL CHECK (length(trim(warrant)) > 0),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    -- THE OWNER'S REVIEW: the heading of the ledger entry that records it, the time, and the session that ran the verb.
    review_ref          TEXT CHECK (review_ref IS NULL OR review_ref LIKE 'Owner%'),
    reviewed_at         TEXT,
    reviewed_session    TEXT,
    review_note         TEXT CHECK (review_note IS NULL OR length(trim(review_note)) > 0),
    retired_at          TEXT,
    retired_by_session  TEXT,
    retirement_reason   TEXT,
    retirement_ref      TEXT CHECK (retirement_ref IS NULL OR retirement_ref LIKE 'Owner%'),
    CHECK ((review_ref IS NULL) = (reviewed_at IS NULL) AND (review_ref IS NULL) = (reviewed_session IS NULL)),
    CHECK (state NOT IN ('stated', 'provisional') OR reviewed_at IS NOT NULL),
    CHECK (state <> 'pending' OR reviewed_at IS NULL),
    CHECK ((state = 'provisional') = (review_note IS NOT NULL)),
    CHECK ((retired_at IS NULL AND retired_by_session IS NULL AND retirement_reason IS NULL AND retirement_ref IS NULL)
        OR (retired_at IS NOT NULL AND retired_by_session IS NOT NULL AND length(trim(retirement_reason)) > 0
            AND retirement_ref IS NOT NULL))
);

CREATE UNIQUE INDEX ux_identity_need_icf_live
    ON identity_need_icf (identity_code, need_code, icf_code)
 WHERE retired_at IS NULL;

CREATE TRIGGER identity_need_icf_no_edit BEFORE UPDATE ON identity_need_icf
WHEN OLD.retired_at IS NOT NULL
  OR NEW.identity_code IS NOT OLD.identity_code OR NEW.need_code IS NOT OLD.need_code
  OR NEW.icf_code IS NOT OLD.icf_code OR NEW.warrant IS NOT OLD.warrant
  OR NEW.created_at IS NOT OLD.created_at OR NEW.created_by_session IS NOT OLD.created_by_session
  OR (OLD.reviewed_at IS NOT NULL AND (NEW.state IS NOT OLD.state OR NEW.review_ref IS NOT OLD.review_ref
      OR NEW.reviewed_at IS NOT OLD.reviewed_at OR NEW.reviewed_session IS NOT OLD.reviewed_session
      OR NEW.review_note IS NOT OLD.review_note))
BEGIN
    SELECT RAISE(ABORT, 'identity_need_icf: a retired row, a triple''s keys and warrant, and a recorded review are never edited; retire the row and propose a new one');
END;

CREATE VIEW v_lens_crosswalk AS
SELECT t.triple_id, t.identity_code, i.display_name AS identity_name,
       t.need_code, n.design_obligation AS need_obligation,
       t.icf_code, c.title AS icf_title,
       t.state, t.warrant, t.review_note, t.review_ref, t.reviewed_at, t.created_by_session
  FROM identity_need_icf t
  JOIN base_taxonomy_identity i ON i.identity_code = t.identity_code
  JOIN access_needs n           ON n.need_code     = t.need_code
  JOIN base_icf c               ON c.icf_code      = t.icf_code
 WHERE t.retired_at IS NULL;

PRAGMA user_version = 166;
