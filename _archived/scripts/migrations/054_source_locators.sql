-- 054_source_locators.sql
-- Reference-only registry of document locators recovered from the pre-reset
-- corpus (owner ruling 2026-08-12: keep DOIs and URLs).
-- NOT an evidence table: no tier, no evidence_type, no claim, no bibliographic
-- content. Pointers only. Admitting a source remains the pipeline's job and
-- populates evidence_sources; this table only prevents duplicate lookups and
-- names documents worth sourcing.
CREATE TABLE source_locators (
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
    CHECK (doi IS NOT NULL OR url IS NOT NULL OR pmid IS NOT NULL
        OR pmcid IS NOT NULL OR isbn IS NOT NULL OR issn IS NOT NULL
        OR standard_number IS NOT NULL)
);
CREATE INDEX ix_source_locators_doi ON source_locators (doi);
CREATE INDEX ix_source_locators_url ON source_locators (url);
PRAGMA user_version = 54;
