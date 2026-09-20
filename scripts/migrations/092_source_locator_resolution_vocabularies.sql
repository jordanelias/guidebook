-- 092_source_locator_resolution_vocabularies.sql
--
-- THE SAME TWO VOCABULARIES ON THE OTHER TABLE, AND THE ONE ROW THAT PROVES WHY IT MATTERS.
--
-- 091 moved `doi_resolution_outcome` and `url_resolution_outcome` into their columns' own
-- CHECK on `evidence_sources`, and its header records the reasoning in full. It did not
-- touch `source_locators`, which carries the SAME TWO COLUMN NAMES over 893 rows -- more
-- than thirty times the 27 rows `evidence_sources` holds. The clue store is where the
-- resolution outcomes are actually written in bulk: 415 rows carry a doi outcome and 71
-- carry a url outcome here, against 20 and 0 there.
--
-- AND HERE THE PRECONDITION 091 RELIED ON DOES NOT HOLD. 091 could say "every live value is
-- already inside its set ... so nothing on disk is invalidated". On this table one row is
-- outside it:
--
--     REF-00023  doi_resolution_outcome = 'UNVERIFIED'
--
-- 'UNVERIFIED' is not in the declared vocabulary and never was. `ENUM_GUARDS` in
-- scripts/emit_data_migration.py has named that vocabulary RESOLVED / NO-MATCH / REVERTED
-- since it was written, and its own comment explains that it exists because the same class
-- of wrong value ('NOT-APPLICABLE') was written in two consecutive research batches on
-- 2026-07-25 -- the second a few hours after the lesson had been recorded in prose. Its
-- closing line is "The fix belongs at the point of writing, not in a document someone has
-- to remember to re-read." That guard scans migration SQL for quoted literals; this row
-- landed through data_20260823223155_2026-08-23-execute-master-plan-repairs.sql and has sat
-- in the table ever since, with every gate green. A CHECK would have refused it at INSERT.
-- This migration is that closing line applied to the table the guard could not protect.
--
-- WHAT HAPPENS TO THE ROW, AND WHY NULL RATHER THAN A WIDER CHECK. The honest reading of
-- 'UNVERIFIED' here is "resolution was never attempted", and the vocabulary has no token for
-- that because NULL already is it -- 478 of the 893 rows say exactly that by being NULL.
-- 'NO-MATCH' would be a stronger and FALSER claim: it means the R10 ladder ran and returned
-- nothing. Widening the CHECK to admit 'UNVERIFIED' was the other option and is rejected:
-- it would ratify on this table a value 091 excluded on its sibling hours earlier, and leave
-- two spellings of one state in one schema (rule 5).
--
-- The row is a pre-reset bibliographic record migrated from the markdown registry
-- (recovered_from = global-reference-registry.json, status REFERENCE-ONLY). Its stored DOI is
-- TRUNCATED -- '10.1016/S0140-6736(14' breaks at the opening parenthesis -- so it could not
-- have resolved whatever was attempted. That truncation is NOT repaired here: completing a
-- DOI from memory is the 2026-08-19 fabrication shape (CLAUDE.md §5(c)), and the only correct
-- repair is a re-retrieval that persists a payload. Recorded so the next reader inherits the
-- finding rather than rediscovering it.
--
-- NO VIEW DEPENDS ON THIS TABLE, verified against sqlite_master before writing, so the
-- drop-and-restore dance 089 and 091 both needed is not required. The two indexes are
-- recreated explicitly.
--
-- AFTER_DATA: 20260920060857

-- The compensating correction, first: the CHECK below cannot be declared over a row that
-- violates it. Fix-forward per CLAUDE.md rule 3 -- the 2026-08-23 migration that wrote this
-- value is committed and immutable, and is not edited.
UPDATE source_locators
   SET doi_resolution_outcome = NULL,
       notes = COALESCE(notes || ' ', '')
               || '|| 2026-09-20 doi_resolution_outcome CORRECTED from ''UNVERIFIED'' to NULL '
               || '(migration 092). ''UNVERIFIED'' is not in this column''s declared vocabulary '
               || '(RESOLVED/NO-MATCH/REVERTED, ENUM_GUARDS in emit_data_migration.py) and NULL '
               || 'is how this table already states "resolution not attempted" in 478 other rows. '
               || 'NO-MATCH was not used because it asserts the R10 ladder ran and returned '
               || 'nothing, which is not known here. The stored DOI is truncated at the opening '
               || 'parenthesis and is left exactly as it stands: completing it from memory is the '
               || 'fabrication shape CLAUDE.md 5(c) forbids, and only a re-retrieval that persists '
               || 'a payload can repair it.'
 WHERE doi_resolution_outcome = 'UNVERIFIED';

CREATE TABLE source_locators__092 (
    ref_id                  TEXT PRIMARY KEY,
    doi                     TEXT,
    url                     TEXT,
    pmid                    TEXT,
    pmcid                   TEXT,
    isbn                    TEXT,
    issn                    TEXT,
    standard_number         TEXT,
    -- Mirrors evidence_sources.doi_resolution_outcome as migration 091 declared it. The two
    -- columns are one vocabulary and must not drift apart; dbcore.check_values() reads this
    -- CHECK, so db.py's argparse, --help and amend-source all arm themselves from here.
    doi_resolution_outcome  TEXT
                            CHECK (doi_resolution_outcome IS NULL
                                   OR doi_resolution_outcome IN
                                      ('RESOLVED', 'NO-MATCH', 'REVERTED')),
    url_resolution_outcome  TEXT
                            CHECK (url_resolution_outcome IS NULL
                                   OR url_resolution_outcome IN
                                      ('MATCHED', 'PARTIAL', 'NO-MATCH', 'DEAD-LINK', 'DEAD-DNS',
                                       'WAYBACK-MATCH', 'WAYBACK-PARTIAL', 'URL-NO-MATCH',
                                       'RESOLVED', 'DEAD', 'RESOLVED-PARTIAL')),
    url_last_fetched        TEXT,
    recovered_from          TEXT NOT NULL DEFAULT 'corpus-pre-reset-2026-08-06',
    authors                 TEXT,
    pub_year                TEXT,
    title                   TEXT,
    tier_claimed            TEXT,
    jurisdiction            TEXT,
    used_in_bpcs            TEXT,
    status                  TEXT NOT NULL DEFAULT 'REFERENCE-ONLY'
                            CHECK (status IN ('REFERENCE-ONLY','PROMOTED',
                                              'SCREENED-OUT','RETIRED')),
    screened_reason         TEXT,
    created_by_session       TEXT,
    created_at               TEXT,
    notes                   TEXT,
    CHECK (doi IS NOT NULL OR url IS NOT NULL OR pmid IS NOT NULL
        OR pmcid IS NOT NULL OR isbn IS NOT NULL OR issn IS NOT NULL
        OR standard_number IS NOT NULL OR title IS NOT NULL),
    -- A screened-out lead states WHY. Structural, not a convention a writer may forget.
    CHECK (status <> 'SCREENED-OUT'
           OR (screened_reason IS NOT NULL AND TRIM(screened_reason) <> ''))
);

INSERT INTO source_locators__092
SELECT ref_id, doi, url, pmid, pmcid, isbn, issn, standard_number,
       doi_resolution_outcome, url_resolution_outcome, url_last_fetched,
       recovered_from, authors, pub_year, title, tier_claimed, jurisdiction,
       used_in_bpcs, status, screened_reason, created_by_session, created_at, notes
  FROM source_locators;

DROP TABLE source_locators;
ALTER TABLE source_locators__092 RENAME TO source_locators;

CREATE INDEX idx_source_locators_status ON source_locators(status);
CREATE INDEX idx_source_locators_queue  ON source_locators(status, doi);

PRAGMA user_version = 92;
