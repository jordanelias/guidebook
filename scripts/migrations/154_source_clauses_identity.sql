-- 154_source_clauses_identity.sql
-- SCHEMA migration (T-031 repair after the adversarial pass; no data). Compensates migration 153 (committed, not
-- edited), which left source_clauses with no identity and CHECKs with blank holes, and said its text was "the clause as
-- the file read holds it", which was not true.
--
-- 1. WHAT clause_text HOLDS, corrected: the clause as the reader gave it, which `db.py record-scan` accepts only when its
--    letters and digits, in order, are those of a passage of the file the reading names (retrieval_log.normalise_quote:
--    case, markup, whitespace and punctuation are not compared). It is not a byte copy of the file.
-- 2. BLANKS. A locator cell or the text holding only whitespace (char(160) included) is refused; 153 tested NULL only.
-- 3. IDENTITY. One row per clause per reading: a unique index over the scan and every locator cell, NULL-safe (a NULL
--    level reads as ''). An `_end` level needs its start level.
-- 4. ONE HOME FOR THE FORMS OF A TERM. `v_attested_term_forms` is the attested set `v_term_names` reads (the CTE it held
--    inline, moved, unchanged); `scripts/audit/scan_debt.py` matches a parameter against a clause with the same set.
--
-- STAGE, READERS and NOT SHOWN: as 153 (dbcore.NOT_SHOWN names clause_text; the owner-browser page reads no column it
-- names).

CREATE TABLE _154_source_clauses (
    clause_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id             INTEGER NOT NULL REFERENCES source_scans(scan_id),
    locator_scheme      TEXT CHECK (locator_scheme IS NULL OR trim(locator_scheme, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_division        TEXT CHECK (loc_division IS NULL OR trim(loc_division, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_part            TEXT CHECK (loc_part IS NULL OR trim(loc_part, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_section         TEXT CHECK (loc_section IS NULL OR trim(loc_section, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_subsection      TEXT CHECK (loc_subsection IS NULL OR trim(loc_subsection, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_paragraph       TEXT CHECK (loc_paragraph IS NULL OR trim(loc_paragraph, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_clause          TEXT CHECK (loc_clause IS NULL OR trim(loc_clause, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_subclause       TEXT CHECK (loc_subclause IS NULL OR trim(loc_subclause, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_division_end    TEXT CHECK (loc_division_end IS NULL OR trim(loc_division_end, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_part_end        TEXT CHECK (loc_part_end IS NULL OR trim(loc_part_end, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_section_end     TEXT CHECK (loc_section_end IS NULL OR trim(loc_section_end, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_subsection_end  TEXT CHECK (loc_subsection_end IS NULL OR trim(loc_subsection_end, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_paragraph_end   TEXT CHECK (loc_paragraph_end IS NULL OR trim(loc_paragraph_end, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_clause_end      TEXT CHECK (loc_clause_end IS NULL OR trim(loc_clause_end, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_subclause_end   TEXT CHECK (loc_subclause_end IS NULL OR trim(loc_subclause_end, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    loc_note            TEXT CHECK (loc_note IS NULL OR trim(loc_note, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    -- the clause as the reader gave it; its letters and digits, in order, are a passage of the file read (see 1 above)
    clause_text         TEXT    NOT NULL CHECK (trim(clause_text, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288)) <> ''),
    created_at          TEXT    NOT NULL,
    created_by_session  TEXT    NOT NULL,
    CHECK (loc_division_end IS NULL OR loc_division IS NOT NULL),
    CHECK (loc_part_end IS NULL OR loc_part IS NOT NULL),
    CHECK (loc_section_end IS NULL OR loc_section IS NOT NULL),
    CHECK (loc_subsection_end IS NULL OR loc_subsection IS NOT NULL),
    CHECK (loc_paragraph_end IS NULL OR loc_paragraph IS NOT NULL),
    CHECK (loc_clause_end IS NULL OR loc_clause IS NOT NULL),
    CHECK (loc_subclause_end IS NULL OR loc_subclause IS NOT NULL),
    CHECK (COALESCE(loc_division, loc_part, loc_section, loc_subsection, loc_paragraph, loc_clause,
                    loc_subclause) IS NOT NULL)
);
INSERT INTO _154_source_clauses (clause_id, scan_id, locator_scheme, loc_division, loc_part, loc_section, loc_subsection, loc_paragraph, loc_clause, loc_subclause, loc_division_end, loc_part_end, loc_section_end, loc_subsection_end, loc_paragraph_end, loc_clause_end, loc_subclause_end, loc_note, clause_text, created_at, created_by_session) SELECT clause_id, scan_id, locator_scheme, loc_division, loc_part, loc_section, loc_subsection, loc_paragraph, loc_clause, loc_subclause, loc_division_end, loc_part_end, loc_section_end, loc_subsection_end, loc_paragraph_end, loc_clause_end, loc_subclause_end, loc_note, clause_text, created_at, created_by_session FROM source_clauses;
DROP TABLE source_clauses;
ALTER TABLE _154_source_clauses RENAME TO source_clauses;
CREATE INDEX idx_source_clauses_scan ON source_clauses(scan_id);
CREATE UNIQUE INDEX ux_source_clauses_place ON source_clauses(scan_id, COALESCE(locator_scheme, ''), COALESCE(loc_division, ''), COALESCE(loc_part, ''), COALESCE(loc_section, ''), COALESCE(loc_subsection, ''), COALESCE(loc_paragraph, ''), COALESCE(loc_clause, ''), COALESCE(loc_subclause, ''), COALESCE(loc_division_end, ''), COALESCE(loc_part_end, ''), COALESCE(loc_section_end, ''), COALESCE(loc_subsection_end, ''), COALESCE(loc_paragraph_end, ''), COALESCE(loc_clause_end, ''), COALESCE(loc_subclause_end, ''));

CREATE VIEW v_attested_term_forms AS
-- The forms of a term that name the concept itself and are attested (an instrument or another source): the set
-- v_term_names displays from and scan_debt.py matches a clause against. One home (migration 154).
SELECT form_id, term_id, alias, upper(language) AS language, jurisdiction, attestation
  FROM term_aliases
 WHERE alias_type NOT IN ('NARROWER','BROADER')
   AND attestation IN ('instrument','other_source');

DROP VIEW v_term_names;
CREATE VIEW v_term_names AS
WITH attested AS (SELECT * FROM v_attested_term_forms),
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

PRAGMA user_version = 154;
