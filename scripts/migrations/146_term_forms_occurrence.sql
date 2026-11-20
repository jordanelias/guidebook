-- 146_term_forms_occurrence.sql
-- SCHEMA migration -- a concept is its id; its names are forms, one row per occurrence; `canonical_en` is our label.
-- Tooling (IMP-21, workplan T-028; design workplan/2026-11-12-bidirectional-pipeline/tasks/T-028-design.md, revised
-- 2026-11-13; delegated resolution of OD-03; OD-38 answered by the owner 2026-11-12, "First recorded, until a named
-- judge picks; the pick is recorded with its reason"). No research rows.
--
-- AFTER_DATA: 20261106053823
-- (Why the marker: `migrate_db.py --rebuild` runs schema migrations before the data migrations that follow the last
-- marker, and data migrations may insert term_aliases rows; without it a data migration landed after 130 would replay
-- after this reshape and the rebuild would diverge. Value: the newest data migration at the time of writing, derived by
-- `ls scripts/migrations/data_*.sql | sed -E 's/.*data_([0-9]{14})_.*/\1/' | sort | tail -1`.)
--
-- WHAT CHANGES (design sections 3, 7 and 10):
--  1. term_aliases is rebuilt to ONE ROW PER OCCURRENCE: a surrogate key `form_id` (assigned here, once, from each row's
--     rowid; the rebuild reproduces it and nothing stored points by rowid), a unique occurrence index in place of the
--     primary key (term_id, alias, language), and a nullable `usage_type` (NULL = not yet typed, the truth for every
--     existing row; typed by judgment when the row is next touched, never guessed here). The column definitions T-026
--     added are copied from sqlite_master, so `attestation` keeps its DEFAULT 'unrecorded'. Legacy alias_type values
--     are not rewritten.
--  2. T-026's junction search_execution_forms is remapped BY KEY to form_id before the old table is dropped: at the
--     occurrence grain the old key is no longer unique, and a foreign key on it would answer `foreign key mismatch`.
--     Until now one row per key, so the join is exact and the junction's row count does not change.
--  3. term_label_picks: the one home of the judge, the reason and the former label of a label set by judgment (OD-38).
--     The route is derived from which pointer is set; the new label is terms.canonical_en, never copied here.
--  4. v_term_names: the name shown (E1) and whether our label is also an attested form, derived; no label-kind column
--     and no display pointer is stored.
-- No VACUUM: it may renumber the implicit rowids of every table without an INTEGER PRIMARY KEY.

CREATE TABLE _146_term_aliases (
    form_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    alias               TEXT NOT NULL,
    language            TEXT NOT NULL DEFAULT 'EN',
    alias_type          TEXT NOT NULL
                        CHECK(alias_type IN (
                            'SYNONYM','TRANSLATION','NARROWER',
                            'BROADER','DEPRECATED','DOMAIN'
                        )),
    jurisdiction        TEXT,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    observation_id      INTEGER REFERENCES observed_terms(observation_id),
    attestation         TEXT NOT NULL DEFAULT 'unrecorded'
    CHECK (attestation IN ('instrument','other_source','owner_supplied','model_seed','unrecorded')),
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
    CHECK (
        (source_clause IS NULL OR TRIM(source_clause, char(32,9,10,13)) <> '') AND
        -- an attested occurrence says where
        (attestation NOT IN ('instrument','other_source')
         OR observation_id IS NOT NULL
         OR (source_url IS NOT NULL AND (source_page IS NOT NULL OR source_clause IS NOT NULL)))
        -- a seed or an unrecorded form says nowhere
        AND (attestation IN ('instrument','other_source')
         OR (source_url IS NULL AND source_page IS NULL AND source_line IS NULL
             AND source_clause IS NULL))
    ),
    -- the sixth statement of 2026-11-06's usage types, in this column's own CHECK (read by dbcore.check_values)
    usage_type          TEXT
    CHECK (usage_type IS NULL OR usage_type IN
        ('code_term','colloquial','regional_variant','outdated_or_disfavoured','product_name'))
);

INSERT INTO _146_term_aliases (form_id, term_id, alias, language, alias_type, jurisdiction, notes, created_at,
                               created_by_session, updated_at, updated_by_session, observation_id, attestation,
                               source_url, source_page, source_line, source_clause, usage_type)
SELECT rowid, term_id, alias, language, alias_type, jurisdiction, notes, created_at,
       created_by_session, updated_at, updated_by_session, observation_id, attestation,
       source_url, source_page, source_line, source_clause, NULL
  FROM term_aliases;

CREATE TABLE _146_search_execution_forms (
    exec_id            INTEGER NOT NULL REFERENCES search_executions(exec_id),
    form_id            INTEGER NOT NULL REFERENCES term_aliases(form_id),
    created_at         TEXT NOT NULL,
    created_by_session TEXT NOT NULL,
    PRIMARY KEY (exec_id, form_id)
);

INSERT INTO _146_search_execution_forms (exec_id, form_id, created_at, created_by_session)
SELECT j.exec_id, a.form_id, j.created_at, j.created_by_session
  FROM search_execution_forms j JOIN _146_term_aliases a USING (term_id, alias, language);

DROP TABLE search_execution_forms;
DROP TABLE term_aliases;
ALTER TABLE _146_term_aliases RENAME TO term_aliases;
ALTER TABLE _146_search_execution_forms RENAME TO search_execution_forms;

-- One row per OCCURRENCE: the same form in two sources, jurisdictions or locators is two rows.
CREATE UNIQUE INDEX ux_term_aliases_occurrence ON term_aliases
    (term_id, alias, language, COALESCE(jurisdiction, ''), COALESCE(observation_id, 0),
     COALESCE(source_url, ''), COALESCE(source_clause, ''), COALESCE(source_page, ''),
     COALESCE(source_line, 0));
CREATE INDEX idx_ta_alias    ON term_aliases(alias);
CREATE INDEX idx_ta_language ON term_aliases(language);

CREATE TABLE term_label_picks (
    pick_id             INTEGER PRIMARY KEY,
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    former_label        TEXT,                                               -- NULL only for a mint by add-term --first-form
    form_id             INTEGER REFERENCES term_aliases(form_id),          -- rename-term --from-form, or a mint's first form
    observation_id      INTEGER REFERENCES observed_terms(observation_id), -- rename-term --from-observation
    ruling_quote        TEXT,                                               -- rename-term --ruling-quote
    judge               TEXT NOT NULL,                                      -- who picked
    reason              TEXT NOT NULL,                                      -- why (add-term --first-form: its --rationale)
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    CHECK ((form_id IS NOT NULL) + (observation_id IS NOT NULL) + (ruling_quote IS NOT NULL) = 1),
    CHECK (former_label IS NOT NULL OR form_id IS NOT NULL)
);

-- The only reader of "what is this concept called" (design section 7). Rules, in order: our label equals an English
-- form an instrument of an owed English-language jurisdiction uses; else the first recorded such form (OD-38); else the
-- origin instrument's phrase in its own language (E1); else our label, which a page marks as ours. "Owed" is read from
-- v_research_scope, the one home of scope; seeds are never vocabulary (E4).
CREATE VIEW v_term_names AS
WITH attested AS (
    SELECT form_id, term_id, alias, upper(language) AS language, jurisdiction, attestation
      FROM term_aliases
     WHERE alias_type NOT IN ('NARROWER','BROADER')
       AND attestation IN ('instrument','other_source')),
en_instrument AS (
    SELECT a.* FROM attested a
     WHERE a.attestation = 'instrument' AND a.language = 'EN'
       AND EXISTS (SELECT 1 FROM v_research_scope r
                    WHERE upper(r.language) = 'EN' AND r.jurisdiction = a.jurisdiction)),
pick AS (
    SELECT t.term_id, t.canonical_en,
           (SELECT form_id FROM en_instrument e WHERE e.term_id = t.term_id
              AND lower(e.alias) = lower(t.canonical_en) ORDER BY form_id LIMIT 1) AS en_label_form,
           (SELECT MIN(form_id) FROM en_instrument e WHERE e.term_id = t.term_id) AS en_first_form,
           (SELECT MIN(form_id) FROM attested o WHERE o.term_id = t.term_id
              AND o.attestation = 'instrument') AS origin_form
      FROM terms t)
SELECT p.term_id,
       p.canonical_en AS label,
       EXISTS (SELECT 1 FROM attested a WHERE a.term_id = p.term_id
                 AND lower(a.alias) = lower(p.canonical_en)) AS label_is_attested_form,
       CASE WHEN p.en_label_form IS NOT NULL THEN 'english_instrument_label'
            WHEN p.en_first_form IS NOT NULL THEN 'english_instrument_form'
            WHEN p.origin_form   IS NOT NULL THEN 'origin_instrument_form'
            ELSE 'label_ours' END AS display_basis,
       COALESCE(p.en_label_form, p.en_first_form, p.origin_form) AS display_form_id,
       COALESCE((SELECT alias FROM term_aliases f
                  WHERE f.form_id = COALESCE(p.en_label_form, p.en_first_form, p.origin_form)),
                p.canonical_en) AS display_name,
       COALESCE((SELECT upper(language) FROM term_aliases f
                  WHERE f.form_id = COALESCE(p.en_label_form, p.en_first_form, p.origin_form)),
                'EN') AS display_language,
       p.origin_form AS origin_form_id
  FROM pick p;

PRAGMA user_version = 146;
