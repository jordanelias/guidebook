-- 061_reference_stubs.sql
-- SCHEMA migration — give the 531 pre-reset bibliographic records a table, so that
-- the last citation store living in markdown stops being a system of record.
--
-- OWNER DIRECTIVE 2026-08-23: "anything like citation which is stored in .md should be
-- recorded in a table." This executes it.
--
-- WHAT WAS WRONG. references/global-reference-registry.md opens by declaring itself
-- "Single source of truth for all references cited anywhere in the guidebook" — a
-- markdown file claiming the role the database holds. Its .json twin was deleted the
-- same day after its 531 identifiers were absorbed into source_locators, but the .md
-- carried something the DB did not: the citation TEXT. Authors, year, title, the tier
-- claimed for it, the jurisdiction, and which BPCs used it. None of that is an
-- identifier, so source_locators could not hold it — its CHECK requires one.
--
-- WHY THIS TABLE CARRIES NO DOI AND NO PMID, which is the whole design.
-- A DOI is an attribute of an IDENTIFIER, and identifiers live in source_locators
-- keyed by ref_id. On 2026-08-23 this project measured four tables independently
-- storing a DOI as a copied string with no foreign key, 17 DOIs duplicated across
-- them, and FOUR ALREADY DRIFTED (evidence_sources held 10.1044/2019_aja-19-0010
-- while three other tables held 10.1044/2019_AJA-19-0010 — one DOI to a human, two
-- to `=`). Adding a fifth copy here would reproduce the exact defect the same day it
-- was written up. Join to source_locators on ref_id instead.
--
-- WHAT THIS TABLE IS NOT. It is NOT a restoration of the corpus that
-- DR-2026-08-06 reset. That reset demoted these records to reference and ruled that
-- "research resuming does not restore the reset rows"; nothing here changes what the
-- guidebook may claim. These rows were already in the repository as tracked markdown
-- — this migration changes WHERE they live, not WHETHER they exist. They are not
-- evidence, they are not citable, and admission still runs the full R1–R15 path into
-- evidence_sources. The status column makes that refusal explicit rather than relying
-- on a reader knowing the history.
--
-- WHAT READS IT: nothing yet, and that is stated rather than hidden. It replaces a
-- file that nothing read either — its two live PROCEDURE callers were repointed on
-- 2026-08-23 when the .json went. The table exists so that the next reader of a
-- pre-reset REF-ID has one place to look, and so that a gate CAN see these records,
-- which no gate could while they were prose.

PRAGMA foreign_keys = OFF;

CREATE TABLE reference_stubs (
    ref_id            TEXT PRIMARY KEY,
    authors           TEXT,
    pub_year          TEXT,          -- TEXT: the source carries 'n.d.' and ranges
    title             TEXT NOT NULL,
    tier_claimed      TEXT,          -- as CLAIMED pre-reset; never a derived tier
    jurisdiction      TEXT,
    used_in_bpcs      TEXT,
    metadata_quality  TEXT,
    status            TEXT NOT NULL DEFAULT 'REFERENCE-ONLY'
                      CHECK (status IN ('REFERENCE-ONLY','PROMOTED','RETIRED')),
    recovered_from    TEXT NOT NULL,
    notes             TEXT
);

CREATE INDEX idx_reference_stubs_status ON reference_stubs(status);
CREATE INDEX idx_reference_stubs_year   ON reference_stubs(pub_year);

PRAGMA foreign_keys = ON;

PRAGMA user_version = 61;
