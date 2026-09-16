-- 082_locator_screened_out.sql
--
-- THE CLUE STORE IS A WORK QUEUE, AND IT HAD NO WAY TO SAY "WORKED AND REJECTED".
--
-- Owner, 2026-09-16: "source_locators is supposed to be used for research: the research
-- agent will systematically go through the DOI in that table, gather evidence, and if
-- acceptable, mark that DOI off as searched in source_locators. Then the research agent
-- has to adjudicate the categorization of the DOI entry."
--
-- The status vocabulary was REFERENCE-ONLY | PROMOTED | RETIRED. Those cover "nobody has
-- looked at this", "this became evidence" and "this identifier is dead" -- and nothing
-- covers "a session worked this lead and judged it unacceptable". Measured before this
-- migration: 880 REFERENCE-ONLY, 13 RETIRED, and **0 PROMOTED** -- not one lead has ever
-- been marked off by any route.
--
-- Two consequences, both of which this migration exists to end:
--   * A rejected lead is indistinguishable from an unexamined one, so the next batch
--     re-works it and the re-work is invisible. "Systematically go through" is not even
--     measurable: there is no expression for how much of the queue is done.
--   * The rejection REASON has nowhere to live, so the judgement that cost the work is
--     the one thing not kept. CLAUDE.md 5(a) in the clue store: a lead dismissed with no
--     record of why is indistinguishable from a lead nobody examined.
--
-- WHY A REASON COLUMN AND NOT A NOTE. `notes` already exists and would have held the
-- string. It is unconstrained free text with no relationship to status, so nothing could
-- enforce that a SCREENED-OUT row HAS a reason -- and an unenforceable convention is the
-- shape this project keeps paying for (CLAUDE.md rule 8). The CHECK below makes the
-- refusal structural: SQLite rejects a SCREENED-OUT row with no reason, whatever writer
-- is used and whether or not it remembered to ask.
--
-- ATTRIBUTION IS PART OF THE SAME FIX, NOT A RIDER. `scripts/audit/batch_capture_report.py`
-- (written the same day, on the same owner request) reports every table a batch wrote;
-- on its first run it found `source_locators` UNATTRIBUTABLE -- 893 rows, no session
-- column, no foreign key path to one -- so no write to the clue store could be traced to
-- the batch that made it. `db.py update_locator` has ALWAYS taken a `session` argument
-- and never stored it. `worked_by_session` / `worked_at` close that: they record which
-- session moved a lead to a terminal state, for PROMOTED and SCREENED-OUT alike.
--
-- NOT BACKFILLED, DELIBERATELY. The 893 existing rows predate any attribution and there
-- is no truthful value to give them; inventing one would be exactly the fabrication shape
-- CLAUDE.md 5(c) records. They stay NULL, which reads as "unknown" and is true.
--
-- RETIRED IS UNTOUCHED AND MUST STAY A SEPARATE VALUE. It means "this identifier is dead,
-- never reissue it" -- the tombstone meaning migration 076 built it for, and the exact
-- distinction `research_batch_dod.py` R9a and `db.py add-source` were both fixed to
-- respect earlier today. SCREENED-OUT says something about the EVIDENCE; RETIRED says
-- something about the IDENTIFIER. Merging them would re-break what 076 and that fix hold.

PRAGMA foreign_keys=OFF;

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
                            CHECK (status IN ('REFERENCE-ONLY','PROMOTED',
                                              'SCREENED-OUT','RETIRED')),
    screened_reason         TEXT,
    worked_by_session       TEXT,
    worked_at               TEXT,
    notes                   TEXT,
    CHECK (doi IS NOT NULL OR url IS NOT NULL OR pmid IS NOT NULL
        OR pmcid IS NOT NULL OR isbn IS NOT NULL OR issn IS NOT NULL
        OR standard_number IS NOT NULL OR title IS NOT NULL),
    -- A screened-out lead states WHY. Structural, not a convention a writer may forget.
    CHECK (status <> 'SCREENED-OUT'
           OR (screened_reason IS NOT NULL AND TRIM(screened_reason) <> ''))
);

INSERT INTO source_locators_new (
    ref_id, doi, url, pmid, pmcid, isbn, issn, standard_number,
    doi_resolution_outcome, url_resolution_outcome, url_last_fetched,
    recovered_from, authors, pub_year, title, tier_claimed, jurisdiction,
    used_in_bpcs, status, notes)
SELECT
    ref_id, doi, url, pmid, pmcid, isbn, issn, standard_number,
    doi_resolution_outcome, url_resolution_outcome, url_last_fetched,
    recovered_from, authors, pub_year, title, tier_claimed, jurisdiction,
    used_in_bpcs, status, notes
FROM source_locators;

DROP TABLE source_locators;
ALTER TABLE source_locators_new RENAME TO source_locators;

CREATE INDEX idx_source_locators_status ON source_locators(status);
-- The queue's working set, which is what "systematically go through" reads.
CREATE INDEX idx_source_locators_queue ON source_locators(status, doi);

PRAGMA foreign_keys=ON;

PRAGMA user_version = 82;
