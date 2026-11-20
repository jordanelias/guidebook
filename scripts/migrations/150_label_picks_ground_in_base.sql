-- 150_label_picks_ground_in_base.sql
-- SCHEMA migration, compensating 146 (T-028 repair; owner statements 2026-11-18, OD-71: "the base grounds itself
-- except for when evidence that allows for new terms/aliases/parameters to be found is pointed to as justification;
-- but this justification should then be absorbed by base and grounded as if it were always there", and "ref_id as
-- provenance? sure. but it's ONLY for provenance"). No data rows.
--
-- term_label_picks (a base table) carried `observation_id REFERENCES observed_terms`, a foreign key into the evidence
-- stage. It is rebuilt without it. A pick's warrant is the base's own: the named judge, the reason, and either the
-- form it rests on (a term_aliases row; rename-term --from-observation now rests on this term's form holding the
-- observed phrase) or the owner's quoted words. `ref_id` is PROVENANCE ONLY: nullable, no foreign key, validated
-- against nothing and read by no base decision.
-- Rows are copied as they stand; a row whose only warrant was an observation cannot be copied without a form, and the
-- CHECK then aborts the migration rather than drop it (none existed when this was written: `select count(*) from
-- term_label_picks where observation_id is not null`).

CREATE TABLE _150_term_label_picks (
    pick_id             INTEGER PRIMARY KEY,
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    former_label        TEXT,                                               -- NULL only for a mint by add-term --first-form
    form_id             INTEGER REFERENCES term_aliases(form_id),          -- the form the pick rests on
    ruling_quote        TEXT,                                               -- rename-term --ruling-quote
    ref_id              TEXT,                                               -- provenance only (OD-71): no foreign key
    judge               TEXT NOT NULL,                                      -- who picked
    reason              TEXT NOT NULL,                                      -- why (add-term --first-form: its --rationale)
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    CHECK ((form_id IS NOT NULL) + (ruling_quote IS NOT NULL) = 1),
    CHECK (former_label IS NOT NULL OR form_id IS NOT NULL)
);

INSERT INTO _150_term_label_picks (pick_id, term_id, former_label, form_id, ruling_quote, ref_id, judge, reason,
                                   created_at, created_by_session)
SELECT pick_id, term_id, former_label, form_id, ruling_quote, NULL, judge, reason, created_at, created_by_session
  FROM term_label_picks;

DROP TABLE term_label_picks;
ALTER TABLE _150_term_label_picks RENAME TO term_label_picks;

PRAGMA user_version = 150;
