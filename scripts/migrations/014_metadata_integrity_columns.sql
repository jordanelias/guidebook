-- 014_metadata_integrity_columns.sql
-- Schema migration: add explicit metadata-integrity tracking to evidence_sources.
--
-- Surfaced during the AUTHOR-TITLE-ONLY × VERIFIED × has-DOI rehabilitation
-- probe (session 2026-05-20-ato-rehab): 32% of DOI-bearing rows had a
-- discrepancy between the DB's recorded title/author/year and what the DOI
-- actually resolves to at Crossref. Patterns: pub_title used as citation
-- shorthand ("note-as-title"), truncated DOIs (publisher+journal prefix only),
-- and a smaller cohort of likely-misattribution. These need owner review at
-- the source level, not silent overwrite.
--
-- The verification_note column is already in use for V2-manual probe logging;
-- mixing integrity findings into that field makes triage queries painful.
-- Two new columns separate the integrity dimension from the verification
-- dimension cleanly.
--
-- metadata_integrity_status enum:
--   NULL                — no integrity probe run on this row
--   OK                  — probe ran, all cross-checks passed
--   MISMATCH-TITLE      — db pub_title disagrees with canonical title at DOI
--   MISMATCH-AUTHOR     — db first_author_last disagrees with canonical author
--   MISMATCH-YEAR       — db pub_year disagrees with canonical year (>1 yr)
--   MISMATCH-MULTI      — multiple-field disagreement (likely wrong DOI)
--   DOI-TRUNCATED       — DOI is a prefix fragment, not a full DOI
--   DOI-404             — DOI well-formed but not found at registrar
--   RESOLVED            — owner reviewed and resolved; detail field carries
--                         the resolution (prefix '[RESOLVED: ...]')
--
-- metadata_integrity_detail: human-readable detail. For MISMATCH-* values,
-- format 'cr={canonical} vs db={recorded}'. For DOI-* values, the DOI string.
-- For RESOLVED, prefix '[RESOLVED: ...]' followed by what was decided.

ALTER TABLE evidence_sources ADD COLUMN metadata_integrity_status TEXT;
ALTER TABLE evidence_sources ADD COLUMN metadata_integrity_detail TEXT;

-- Bump schema version.
PRAGMA user_version = 14;
