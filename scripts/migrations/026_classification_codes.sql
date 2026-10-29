-- 026_classification_codes.sql
-- Schema migration: a coded classification layer so evidence can be filtered by
-- WHO-ICF code and access need, not only by population.
--
-- WHY. Pages must be filterable by population / ICF code / access need
-- (owner request 2026-10-29). Evidence sources had no structured population,
-- ICF or access-need coding: population lived in free text (evidence_population_match),
-- in per-BPC context, or nowhere. This adds the code vocabularies, the
-- population -> code maps, and per-source tags that record HOW each tag was
-- assigned (method, confidence, review status) so no automated tag is mistaken
-- for a verified one.
--
-- DESIGN NOTES.
--  * Three owner-defined design scales (universal / population / person) already
--    exist as evidence_cell_state.design_scale (migration 024). 'ALL' (populations)
--    is the universal scale, not a population.
--  * ICF = taxonomy only (decision of 2026-04-09): codes classify; ICF documents
--    are not evidence sources.
--  * STRICT tables + CHECKs (audit finding F-09: adopt SQLite enforcement).
--  * Vocabularies and maps are PROVISIONAL until the owner / functional-deficit
--    review marks them REVIEWED.
--  * Numbering: 026 was sketched in workplan/best-practices-assessment-system.md
--    for evidence_cell_state/weighting; this is a prerequisite for filterable
--    presentation, so that workplan's migration renumbers to 027+.
--
-- Schema-only, additive. The runner sets PRAGMA user_version to 26 after applying.

BEGIN;

CREATE TABLE icf_codes (
    icf_code            TEXT PRIMARY KEY
                        CHECK (icf_code GLOB '[bsde][0-9][0-9][0-9]*'),
    chapter             TEXT NOT NULL
                        CHECK (chapter IN ('b', 's', 'd', 'e')
                               AND chapter = substr(icf_code, 1, 1)),
    title               TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL
) STRICT;

CREATE TABLE access_needs (
    need_code           TEXT PRIMARY KEY CHECK (need_code GLOB 'AN-[0-9][0-9]'),
    label               TEXT NOT NULL,
    description         TEXT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'PROVISIONAL'
                        CHECK (status IN ('PROVISIONAL', 'ADOPTED')),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL
) STRICT;

CREATE TABLE population_icf_map (
    population_code     TEXT NOT NULL REFERENCES populations(population_code),
    icf_code            TEXT NOT NULL REFERENCES icf_codes(icf_code),
    relation            TEXT NOT NULL CHECK (relation IN ('primary', 'secondary')),
    basis               TEXT NOT NULL,
    review_status       TEXT NOT NULL DEFAULT 'PROVISIONAL'
                        CHECK (review_status IN ('PROVISIONAL', 'REVIEWED')),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    PRIMARY KEY (population_code, icf_code)
) STRICT;

CREATE TABLE population_access_need_map (
    population_code     TEXT NOT NULL REFERENCES populations(population_code),
    need_code           TEXT NOT NULL REFERENCES access_needs(need_code),
    basis               TEXT NOT NULL,
    review_status       TEXT NOT NULL DEFAULT 'PROVISIONAL'
                        CHECK (review_status IN ('PROVISIONAL', 'REVIEWED')),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    PRIMARY KEY (population_code, need_code)
) STRICT;

-- Per-source tags. role: 'subject' = the population the source is ABOUT / studied;
-- 'cited-for' = populations of the Guidebook items the source is cited to support.
CREATE TABLE source_population_tags (
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    population_code     TEXT NOT NULL REFERENCES populations(population_code),
    role                TEXT NOT NULL CHECK (role IN ('subject', 'cited-for')),
    method              TEXT NOT NULL
                        CHECK (method IN ('manual-read', 'population-match-record',
                                          'title-keyword', 'slug-item-link')),
    confidence          TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
    review_status       TEXT NOT NULL DEFAULT 'UNREVIEWED'
                        CHECK (review_status IN ('UNREVIEWED', 'REVIEWED')),
    basis               TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    PRIMARY KEY (ref_id, population_code, role, method)
) STRICT;

CREATE TABLE source_icf_tags (
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    icf_code            TEXT NOT NULL REFERENCES icf_codes(icf_code),
    method              TEXT NOT NULL
                        CHECK (method IN ('manual-read', 'derived-from-population-map')),
    confidence          TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
    review_status       TEXT NOT NULL DEFAULT 'UNREVIEWED'
                        CHECK (review_status IN ('UNREVIEWED', 'REVIEWED')),
    basis               TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    PRIMARY KEY (ref_id, icf_code, method)
) STRICT;

CREATE TABLE source_need_tags (
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    need_code           TEXT NOT NULL REFERENCES access_needs(need_code),
    method              TEXT NOT NULL
                        CHECK (method IN ('manual-read', 'derived-from-population-map')),
    confidence          TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
    review_status       TEXT NOT NULL DEFAULT 'UNREVIEWED'
                        CHECK (review_status IN ('UNREVIEWED', 'REVIEWED')),
    basis               TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    PRIMARY KEY (ref_id, need_code, method)
) STRICT;

CREATE INDEX idx_spt_pop  ON source_population_tags(population_code);
CREATE INDEX idx_sit_icf  ON source_icf_tags(icf_code);
CREATE INDEX idx_snt_need ON source_need_tags(need_code);

COMMIT;
