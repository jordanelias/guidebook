-- 062_locators_carry_bibliography.sql
-- SCHEMA migration — let the clue store hold a clue that has no identifier, so that the
-- duplication migration 061 created can be undone by the data migration that follows.
--
-- OWNER, 2026-08-23, shown the count: "that's stupid. we need to deduplicate."
--
-- WHAT 061 GOT WRONG. The directive was that citation data stored in .md be recorded in a
-- table. I created a NEW table, reference_stubs, keyed on ref_id — the key source_locators
-- already used. That produced three homes, not one:
--     499 records in BOTH source_locators and reference_stubs
--      32 records in BOTH reference_stubs and search_candidates
--     344 records in source_locators alone
-- A 1:1 split on a shared primary key with no foreign key is not normalisation. It is
-- fragmentation, and it broke the "one fact, one home" rule recorded that same morning.
--
-- WHY 061 REACHED FOR A SECOND TABLE, which is the defect this migration actually fixes:
-- the old CHECK on source_locators required at least one IDENTIFIER, so the 32 title-only
-- records were illegal here and had to go somewhere else. The constraint, not the data,
-- forced the sprawl. The new CHECK requires an identifier OR a title — a title-only clue
-- is the ordinary shape of a standards reference or grey literature — while a wholly empty
-- row stays illegal.
--
-- WHY THE MERGE IS NOT IN THIS FILE. Rebuild replays every SCHEMA migration before any
-- DATA migration. reference_stubs is populated by a committed data migration
-- (data_20260823223839), so any schema-time read of it sees an empty table on rebuild and
-- a full one live — and the reproducibility gate compares those two. A first attempt did
-- the merge and the DROP here and failed exactly that way: "ERROR applying
-- data_20260823223839: no such table: reference_stubs". Migrations are append-only, so
-- the fix is forward: this file only widens the schema, and the merge runs as a DATA
-- migration timestamped after the one that fills the table.
--
-- reference_stubs is therefore NOT dropped. It survives as an EMPTY tombstone, because a
-- committed data migration writes to it and replay must keep working. That is a scar from
-- 061 and it is left visible rather than tidied away.
--
-- WHAT THIS MATERIAL IS. Clues, in the owner's words: "not stored as usable for any case
-- unless it is being read by a researcher." Nothing joins it, no determination may cite
-- it. DR-2026-08-06 demoted it and ruled that resuming research does not restore it;
-- `status` defaults to REFERENCE-ONLY and admission runs the full R1-R15 path into
-- evidence_sources. The one machine use that survives is duplicate detection (R9a/R9b),
-- which asks a question ABOUT the stash rather than making a claim FROM it.

PRAGMA foreign_keys = OFF;

CREATE TABLE source_locators_new (
    ref_id                  TEXT PRIMARY KEY,
    doi                     TEXT,
    url                     TEXT,
    pmid                    TEXT,
    pmcid                   TEXT,
    isbn                    TEXT,
    issn                    TEXT,
    standard_number         TEXT,
    doi_resolution_outcome  TEXT,
    url_resolution_outcome  TEXT,
    url_last_fetched        TEXT,
    recovered_from          TEXT NOT NULL DEFAULT 'corpus-pre-reset-2026-08-06',
    authors                 TEXT,
    pub_year                TEXT,
    title                   TEXT,
    tier_claimed            TEXT,
    jurisdiction            TEXT,
    used_in_bpcs            TEXT,
    status                  TEXT NOT NULL DEFAULT 'REFERENCE-ONLY'
                            CHECK (status IN ('REFERENCE-ONLY','PROMOTED','RETIRED')),
    notes                   TEXT,
    CHECK (doi IS NOT NULL OR url IS NOT NULL OR pmid IS NOT NULL
        OR pmcid IS NOT NULL OR isbn IS NOT NULL OR issn IS NOT NULL
        OR standard_number IS NOT NULL OR title IS NOT NULL)
);

INSERT INTO source_locators_new (ref_id, doi, url, pmid, pmcid, isbn, issn,
    standard_number, doi_resolution_outcome, url_resolution_outcome, url_last_fetched,
    recovered_from)
SELECT ref_id, doi, url, pmid, pmcid, isbn, issn, standard_number,
       doi_resolution_outcome, url_resolution_outcome, url_last_fetched, recovered_from
FROM source_locators;

DROP TABLE source_locators;
ALTER TABLE source_locators_new RENAME TO source_locators;

CREATE INDEX idx_source_locators_status ON source_locators(status);

PRAGMA foreign_keys = ON;

PRAGMA user_version = 62;
