-- 151_term_relations_ground_in_base.sql
-- SCHEMA migration, compensating 147 and 148 (T-029 repair; owner statements 2026-11-18, OD-71: "the base grounds itself
-- except for when evidence that allows for new terms/aliases/parameters to be found is pointed to as justification; but
-- this justification should then be absorbed by base and grounded as if it were always there", and "ref_id as
-- provenance? sure. but it's ONLY for provenance"). No data rows.
--
-- term_relations (a base table) carried three foreign keys out of the base: observation_id to observed_terms (evidence),
-- extraction_id to source_value_extractions and adjudication_id to term_adjudications (judgment). It is rebuilt without
-- them. A relation's justification is now the base's own cells:
--  * WHERE IT WAS FOUND: source_url, source_page, source_line and source_clause, spelled and checked as term_aliases
--    spells them (one fact, one spelling). A locator is a URL plus a page or a clause; a locator part without the URL
--    says nowhere. Only the locator is absorbed, not the source's quoted words (the ruling does not say they are).
--  * WHY: `reason`, the judge's reason in words. A `distinct` relation is a judgment between two concepts the base
--    already holds, so it rests on its reason alone (its rationale, absorbed: the base does not wait on, or point into,
--    the judgment stage); every other kind rests on the located statement that says so. An `element has provision` row
--    is therefore never justified by a reason alone (OD-56: it rests on the source statement that says the element
--    should carry the provision).
--  * ref_id is PROVENANCE ONLY: nullable, no foreign key, validated against nothing, read by no base decision.
-- Rows are copied as they stand; a row without a locator that is not `distinct` cannot be copied and the CHECK aborts the
-- migration rather than drop it (none existed when this was written: `select count(*) from term_relations`).
-- Everything else is 147's and 148's, unchanged: the kinds, the retirement cells, the order of a `distinct` row, and
-- the one live row per unordered pair per kind.

CREATE TABLE _151_term_relations (
    relation_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    from_term_id        TEXT NOT NULL REFERENCES terms(term_id),
    kind                TEXT NOT NULL
                        CHECK (kind IN ('broader', 'part of', 'element has parameter', 'element has provision',
                                        'adjacent', 'distinct')),
    to_term_id          TEXT NOT NULL REFERENCES terms(term_id),
    reason              TEXT CHECK (reason IS NULL OR length(trim(reason)) > 0),
    source_url          TEXT
    CHECK (source_url IS NULL OR (
        (source_url GLOB 'http://[^/' || char(32,9,10,13) || ']*'
         OR source_url GLOB 'https://[^/' || char(32,9,10,13) || ']*')
        AND source_url NOT GLOB '*[' || char(32,9,10,13) || ']*')),
    source_page         TEXT
    CHECK (source_page IS NULL OR TRIM(source_page, char(32,9,10,13)) <> ''),
    source_line         INTEGER
    CHECK (source_line IS NULL OR (typeof(source_line) = 'integer' AND source_line > 0)),
    source_clause       TEXT
    CHECK (source_clause IS NULL OR TRIM(source_clause, char(32,9,10,13)) <> ''),
    ref_id              TEXT,                                               -- provenance only (OD-71): no foreign key
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    retired_at          TEXT,
    retired_by_session  TEXT,
    retirement_reason   TEXT,
    CHECK (from_term_id <> to_term_id),
    CHECK (source_url IS NOT NULL
           OR (source_page IS NULL AND source_line IS NULL AND source_clause IS NULL)),
    CHECK (kind = 'distinct' OR (source_url IS NOT NULL AND (source_page IS NOT NULL OR source_clause IS NOT NULL))),
    CHECK (kind <> 'distinct' OR reason IS NOT NULL),
    CHECK (kind <> 'distinct'
           OR CAST(substr(from_term_id, instr(from_term_id, '-') + 1) AS INTEGER)
              < CAST(substr(to_term_id, instr(to_term_id, '-') + 1) AS INTEGER)
           OR (CAST(substr(from_term_id, instr(from_term_id, '-') + 1) AS INTEGER)
               = CAST(substr(to_term_id, instr(to_term_id, '-') + 1) AS INTEGER)
               AND from_term_id < to_term_id)),
    CHECK ((retired_at IS NULL) = (retired_by_session IS NULL) AND (retired_at IS NULL) = (retirement_reason IS NULL)),
    CHECK (retired_at IS NULL OR (length(trim(retired_at)) > 0 AND length(trim(retired_by_session)) > 0
                                  AND length(trim(retirement_reason)) > 0))
);

INSERT INTO _151_term_relations (relation_id, from_term_id, kind, to_term_id, reason, source_url, source_page,
                                 source_line, source_clause, ref_id, created_at, created_by_session, retired_at,
                                 retired_by_session, retirement_reason)
SELECT relation_id, from_term_id, kind, to_term_id, reason, NULL, NULL, NULL, NULL, NULL, created_at,
       created_by_session, retired_at, retired_by_session, retirement_reason
  FROM term_relations;

DROP TABLE term_relations;
ALTER TABLE _151_term_relations RENAME TO term_relations;

CREATE UNIQUE INDEX ux_term_relations_live_pair
    ON term_relations (kind, min(from_term_id, to_term_id), max(from_term_id, to_term_id))
 WHERE retired_at IS NULL;

PRAGMA user_version = 151;
