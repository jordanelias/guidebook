-- 147_term_relations.sql
-- SCHEMA migration -- typed pointers from one term to another, each with its warrant (T-029, IMP-29; amended
-- 2026-11-17 by the propagation and consolidation adjudication, gaps G1 and G2; OD-56 answered by the owner 2026-11-14,
-- "b"; OD-29 resolved under delegation, "both retire in place"). Tooling, no research rows. Without it a ramp's
-- gradient and run length, or "this concept is broader than that one", are held as shared alias strings and prose, so
-- parameters that belong together cannot be shown together and an element page has nothing to derive from.
--
-- No AFTER_DATA marker: the table is new, so no committed data migration can INSERT into it.
--
-- THE THREE PLACES THAT RECORD A LIKENESS, one sentence each (a fact lives in one of them, rule 5):
--  * term_aliases relates a PHRASE to a term, by its alias_type (the values are that column's own CHECK:
--    dbcore.check_values(conn, 'term_aliases', 'alias_type')).
--  * term_relations (this table) relates a TERM to another term, by its kind (the values are `kind`'s own CHECK:
--    dbcore.check_values(conn, 'term_relations', 'kind')).
--  * T-032's relation rows relate a PROVISION to a provision at synthesis, judged at the Opus floor (OD-25 names their
--    kinds).
--
-- THE KINDS. A row reads "<from term> <kind> <to term>".
--  broader                 from is the broader concept and to the narrower one (a concept and what it includes).
--  part of                 from is a part of to.
--  element has parameter   from is a building element and to is a term one of its dimensions or quantities is
--                          measured by; to is normally the term of a parameter (base_parameters.term_id), which
--                          the reader looks up, not copies.
--  element has provision   from is a building element and to is a provision whose question is whether it is present
--                          (a hearing loop, a visual alarm, a tactile walking surface indicator); such a provision is
--                          not a parameter and no value is computed for it (OD-56). The row is the one home of "element
--                          E should carry provision P, per source S": the element-level determination (T-060) points
--                          at it and holds neither the provision term nor the warrant again.
--  adjacent                the two terms name things that meet or sit next to each other.
--  distinct                two terms a judge recorded as two concepts although their names are near or shared (a
--                          homonym, or a near name for another thing); written by add-term --distinct-from (T-129)
--                          and the consolidation pass (T-131), and read by T-130's proposer so that a judged pair is
--                          not proposed again until the base grows under it. Stored with the lower term id first.
-- `equivalent` is NOT a kind: two terms that name one concept are a dual home, and the act is a merge (T-129's
-- merge-term), never a standing pointer; until it merges them they are left as they are and listed. No reader needs a
-- "counterpart, not identical" kind, so none was added.
--
-- ONE LIVE ROW PER UNORDERED PAIR PER KIND. The unique index below is on the pair's lower and higher term id, so it
-- also refuses the converse of a directed row ("A broader B" while "B broader A" is live): a judge changes a relation
-- by retiring it with a reason and writing the new one, never by an UPDATE (OD-29, retire in place).
--
-- THE WARRANT is exactly one pointer, to the row that says it: an observation (observed_terms), an extraction
-- (source_value_extractions) or an adjudication (term_adjudications; the warrant of a `distinct` row written with its
-- term). `reason` is the judge's reason in words. Who judged it and when are created_by_session and created_at.
--
-- WRITERS: db.py add-term-relation, retire-term-relation. READERS: db.py element-parameters (an element's parameters
-- and provisions; T-033 and render read it); every later reader keeps `retired_at IS NULL`.

CREATE TABLE term_relations (
    relation_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    from_term_id        TEXT NOT NULL REFERENCES terms(term_id),
    kind                TEXT NOT NULL
                        CHECK (kind IN ('broader', 'part of', 'element has parameter', 'element has provision',
                                        'adjacent', 'distinct')),
    to_term_id          TEXT NOT NULL REFERENCES terms(term_id),
    reason              TEXT NOT NULL CHECK (length(trim(reason)) > 0),
    observation_id      INTEGER REFERENCES observed_terms(observation_id),
    extraction_id       INTEGER REFERENCES source_value_extractions(extraction_id),
    adjudication_id     INTEGER REFERENCES term_adjudications(adjudication_id),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    retired_at          TEXT,
    retired_by_session  TEXT,
    retirement_reason   TEXT,
    CHECK (from_term_id <> to_term_id),
    CHECK ((observation_id IS NOT NULL) + (extraction_id IS NOT NULL) + (adjudication_id IS NOT NULL) = 1),
    CHECK (kind <> 'distinct' OR from_term_id < to_term_id),
    CHECK ((retired_at IS NULL AND retired_by_session IS NULL AND retirement_reason IS NULL)
        OR (retired_at IS NOT NULL AND retired_by_session IS NOT NULL AND length(trim(retirement_reason)) > 0))
);

CREATE UNIQUE INDEX ux_term_relations_live_pair
    ON term_relations (kind, min(from_term_id, to_term_id), max(from_term_id, to_term_id))
 WHERE retired_at IS NULL;

PRAGMA user_version = 147;
