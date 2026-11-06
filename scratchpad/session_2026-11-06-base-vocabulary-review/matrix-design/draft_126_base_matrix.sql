-- DRAFT ONLY, 2026-11-06. NOT a migration: not in scripts/migrations/, not applied, approves nothing.
-- 126_base_matrix.sql -- SCHEMA migration: the base is the matrix and grounds itself
-- (references/project-standards.md, "Owner statements 2026-11-06 (seventh)").
-- Design: scratchpad/session_2026-11-06-base-vocabulary-review/matrix-design/base-matrix-design.md
-- Three tables, four columns on terms, one dropped column, three views. Vocabularies live in the CHECKs
-- below and are read by dbcore.check_values(); no list in code. Every value its own cell (CLAUDE.md §4).

-- 1. WHERE A FORM WAS FOUND. One row per source, so its URL has one home (rule 5): today the URL is
--    repeated inside a joined `source` cell on every equivalents row.
CREATE TABLE base_sources (
    source_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    url                 TEXT NOT NULL UNIQUE CHECK (url GLOB 'http*://*'),   -- where it was retrieved from
    archive_url         TEXT CHECK (archive_url IS NULL OR archive_url GLOB 'http*://*'),
    title_as_written    TEXT NOT NULL CHECK (length(trim(title_as_written)) > 0),
    issuing_body        TEXT,
    edition_in_force    TEXT,
    language            TEXT NOT NULL,             -- the source's own language, in lang_jur_map's code
    jurisdiction        TEXT NOT NULL,             -- the matrix column's jurisdiction (FR, DE, CN ...)
    subdivision         TEXT CHECK (subdivision IS NULL OR subdivision GLOB '[A-Z][A-Z]-?*'),  -- DE-BY, ES-CT, CN-BJ
    source_class        TEXT NOT NULL CHECK (source_class IN
                            ('instrument', 'other statute', 'signage manual', 'public-body guidance',
                             'disabled people''s organisation', 'trade or product catalogue')),
    retrieved_at        TEXT,
    retrieved_sha256    TEXT CHECK (retrieved_sha256 IS NULL OR length(retrieved_sha256) = 64),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    FOREIGN KEY (language, jurisdiction) REFERENCES lang_jur_map(language, jurisdiction)
);

-- 2. THE MATRIX CELL'S MEMBERS. One row per OCCURRENCE (sixth entry, item 5: equivalence is judged per
--    occurrence). The cell (term x language x jurisdiction) is a GROUP BY, never stored.
CREATE TABLE term_forms (
    form_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    form                TEXT NOT NULL CHECK (length(trim(form)) > 0),     -- verbatim
    language            TEXT NOT NULL,             -- lang_jur_map code (NO, ZH ...)
    variety             TEXT,                      -- BCP 47 subtag as written: nb, nn, Hans, Hant
    usage_type          TEXT NOT NULL CHECK (usage_type IN
                            ('code term', 'colloquial', 'regional variant', 'outdated or disfavoured',
                             'product name', 'qualifier')),
    source_id           INTEGER REFERENCES base_sources(source_id),
    page                TEXT,                      -- as printed
    line                INTEGER CHECK (line IS NULL OR line > 0),
    clause              TEXT,                      -- article / clause / section as written
    quote               TEXT,                      -- verbatim, short; contains `form`
    seed_origin         TEXT CHECK (seed_origin IS NULL OR seed_origin IN ('owner-supplied', 'model')),
    scope_note          TEXT,
    conflation_note     TEXT,
    conflates_term_id   TEXT REFERENCES terms(term_id),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    -- OR-17/E4: no source means a flagged seed, and a seed carries no locator or quote.
    CHECK ((source_id IS NULL) = (seed_origin IS NOT NULL)),
    CHECK (source_id IS NULL OR page IS NOT NULL OR clause IS NOT NULL),
    CHECK (source_id IS NOT NULL OR (page IS NULL AND line IS NULL AND clause IS NULL AND quote IS NULL)),
    CHECK (quote IS NULL OR instr(quote, form) > 0),
    CHECK (conflates_term_id IS NULL OR conflation_note IS NOT NULL)
);
CREATE UNIQUE INDEX ux_term_forms_occurrence ON term_forms
    (term_id, form, language, COALESCE(variety, ''), COALESCE(source_id, 0),
     COALESCE(clause, ''), COALESCE(page, ''), COALESCE(line, 0));
CREATE INDEX ix_term_forms_form ON term_forms(form);

-- 3. WHERE A CONCEPT WAS LOOKED FOR. Only this makes SEARCHED-NONE-FOUND distinguishable from
--    NOT-SEARCHED. "Found" is not stored: it is the existence of a term_forms row from that source.
CREATE TABLE base_form_searches (
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    source_id           INTEGER NOT NULL REFERENCES base_sources(source_id),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    PRIMARY KEY (term_id, source_id)
);

-- 4. THE CONCEPT SIDE (E1). canonical_en stays NOT NULL (six data migrations INSERT it) and holds the
--    name; name_language says what language that name is in. Existing rows default to EN, which is
--    what the column has always held.
ALTER TABLE terms ADD COLUMN name_language TEXT NOT NULL DEFAULT 'EN';
ALTER TABLE terms ADD COLUMN kind TEXT CHECK (kind IS NULL OR kind IN
    ('quantity', 'element', 'setting', 'technique', 'performance criterion', 'trigger rule',
     'outcome level', 'drafting layer'));
ALTER TABLE terms ADD COLUMN split_of_term_id TEXT REFERENCES terms(term_id);
ALTER TABLE terms ADD COLUMN discriminating_test TEXT
    CHECK ((split_of_term_id IS NULL) = (discriminating_test IS NULL));

-- 5. THE INVERTED POINTER GOES (seventh entry, item 2). 0 rows carry it; no data_* migration writes it.
--    Re-derive before applying: SELECT COUNT(observation_id) FROM term_aliases;
--    grep -l observation_id scripts/migrations/data_* | xargs grep -l 'INSERT INTO term_aliases'
ALTER TABLE term_aliases DROP COLUMN observation_id;

-- 6. COVERAGE: derived from the base itself. Columns = lang_jur_map; owed = v_research_scope.
CREATE VIEW v_base_matrix AS
WITH found AS (
    SELECT f.term_id, f.language, s.jurisdiction,
           COUNT(*) AS n_occurrences, COUNT(DISTINCT f.form) AS n_forms
      FROM term_forms f JOIN base_sources s ON s.source_id = f.source_id
     GROUP BY f.term_id, f.language, s.jurisdiction),
searched AS (
    SELECT q.term_id, s.language, s.jurisdiction, COUNT(*) AS n_sources_read
      FROM base_form_searches q JOIN base_sources s ON s.source_id = q.source_id
     GROUP BY q.term_id, s.language, s.jurisdiction)
SELECT t.term_id, t.kind, m.language, m.jurisdiction,
       COALESCE(fd.n_forms, 0) AS n_forms,
       COALESCE(sr.n_sources_read, 0) AS n_sources_read,
       CASE WHEN fd.term_id IS NOT NULL THEN 'HAS-FORM'
            WHEN r.language IS NULL      THEN 'OUT-OF-SCOPE'
            WHEN sr.term_id IS NOT NULL  THEN 'SEARCHED-NONE-FOUND'
            ELSE 'NOT-SEARCHED' END AS cell_state
  FROM terms t
  CROSS JOIN lang_jur_map m
  LEFT JOIN v_research_scope r ON r.language = m.language AND r.jurisdiction = m.jurisdiction
  LEFT JOIN found fd    ON fd.term_id = t.term_id AND fd.language = m.language AND fd.jurisdiction = m.jurisdiction
  LEFT JOIN searched sr ON sr.term_id = t.term_id AND sr.language = m.language AND sr.jurisdiction = m.jurisdiction;

-- A form whose (language, source jurisdiction) is not a lang_jur_map column: it would fall out of the
-- matrix silently. Must be empty, or the pair declared (a lang_jur_map row).
CREATE VIEW v_base_forms_unmapped AS
SELECT f.form_id, f.term_id, f.form, f.language, s.jurisdiction
  FROM term_forms f JOIN base_sources s ON s.source_id = f.source_id
 WHERE NOT EXISTS (SELECT 1 FROM lang_jur_map m
                    WHERE m.language = f.language AND m.jurisdiction = s.jurisdiction);

-- What research looks a phrase up in: attested forms, seeds, and the legacy aliases, each flagged.
-- One view, no copy; term_aliases keeps its 2382 rows untouched.
CREATE VIEW v_base_lookup AS
SELECT f.term_id, f.form, f.language, s.jurisdiction, f.usage_type, NULL AS alias_type,
       CASE WHEN f.source_id IS NULL THEN 'seed' ELSE 'attested' END AS standing,
       f.seed_origin, s.url, f.page, f.line, f.clause
  FROM term_forms f LEFT JOIN base_sources s ON s.source_id = f.source_id
UNION ALL
SELECT a.term_id, a.alias, upper(a.language), a.jurisdiction, NULL, a.alias_type, 'legacy alias',
       NULL, NULL, NULL, NULL, NULL
  FROM term_aliases a;

PRAGMA user_version = 126;
