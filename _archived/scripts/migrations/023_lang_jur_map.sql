-- 023_lang_jur_map.sql
-- Schema migration (Phase A.3): create the language<->jurisdiction mapping table.
--
-- Per the operative workplan (audits/bpc-rewrite-workplan-2026-05-11.md, A.3) and
-- PI standing rule #9, the multilingual coverage axis needs a table mapping each
-- of the 19 research languages to the 46 jurisdictions with a role assignment, so
-- that Phase E can cross-check coverage (e.g. flag when EN is SEARCHED but a
-- US-specific source for a US claim was not logged).
--
-- Schema: lang_jur_map(language, jurisdiction, role), role in
-- {PRIMARY, SECONDARY, COLONIAL}. language / jurisdiction are free TEXT to match
-- the loose-coupling convention of search_languages.language and
-- search_coverage.jurisdiction (neither is FK-bound to an enum in this DB).
--
-- POPULATION IS DEFERRED, NOT DONE HERE. The role taxonomy is underspecified by
-- the project: A.3 gives three illustrative rows ((EN,US,PRIMARY), (EN,IN,SECONDARY),
-- (EN,ZA,SECONDARY)) but no definitions and no COLONIAL example, and many of the 46
-- jurisdictions' official languages fall outside the 19-language set (Thai, Amharic,
-- Tagalog, ...), which makes most role cells interpretive. Assigning ~60-100
-- PRIMARY/SECONDARY/COLONIAL rows without the project's role definitions would be
-- fabrication. The table is created empty; a companion data migration populates it
-- once the role taxonomy is defined (owner / spec input).
--
-- Schema-only, additive. The runner sets PRAGMA user_version to 23 after applying.

BEGIN;

CREATE TABLE lang_jur_map (
    language            TEXT NOT NULL,
    jurisdiction        TEXT NOT NULL,
    role                TEXT NOT NULL
                        CHECK (role IN ('PRIMARY', 'SECONDARY', 'COLONIAL')),
    notes               TEXT,
    created_at          TEXT,
    created_by_session  TEXT,
    PRIMARY KEY (language, jurisdiction)
);

COMMIT;
