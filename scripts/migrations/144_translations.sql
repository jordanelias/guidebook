-- 144_translations.sql
-- SCHEMA migration (T-049; owner statements 2026-11-12, "everything non-English be translated ... probably at
-- synthesis or whatever we need"). No data rows. A typed home for translations, attached by POINTER.
--
-- THE POINTER. A translation names the cell it translates by (source_table, source_column, source_row_key) and never
-- replaces or copies it. `source_row_key` is the value, as text, of the pointed table's single-column declared primary
-- key; a table whose key has more than one column cannot be pointed at (db.py refuses it). SQLite cannot hold a foreign
-- key to "any cell", so `source_sha256` (the hash of the cell's text when it was translated; a hash is not a copy) lets a
-- later change to the original be SEEN: scripts/audit/translation_pointer_audit.py reads it. There is no column that says
-- "this is a translation": the table is the mark.
--
-- THE LIFECYCLE. requested -> translated -> reviewed | rejected. `translated_text` is NULL exactly while requested; the
-- translator (kind and name) is NULL while requested and set after; the reviewer (kind, name, time) is set exactly when
-- reviewed or rejected, and is never the translator (OD-30, resolved under delegation: a translation shown to a reader
-- is reviewed by an Opus-class instance other than its translator; the database records the reviewer's name and cannot
-- verify its class). `review_reason` is the one cell for why: required when rejected, optional when reviewed, NULL
-- otherwise. A corrected translation is a new row; the old one is retired in place (`superseded_by_translation_id`).
-- `requested_at_stage` is the stage that asked; `due_stage` NULL means the translation rule of
-- governance/pipeline-contract.yaml decides, computed when read and never stored; a value is an explicit override for
-- this row. Neither stage column is a CHECK: the stage ids live in the contract and the writers validate against it. The
-- target language is validated by the writers against lang_jur_map, which holds it as a value, not as a key.
--
-- NOT the aliases typed TRANSLATION in term_aliases: those are generated search forms and stay where they are.
-- STAGE: cross-stage (governance/stage-map.yaml). WRITERS: db.py request-translation, record-translation,
-- review-translation. READERS: v_translations_current (the only read surface), db.py translations --due-at, and
-- translation_pointer_audit. Nothing is backfilled and no data migration accompanies this one.

CREATE TABLE translations (
    translation_id               INTEGER PRIMARY KEY AUTOINCREMENT,
    source_table                 TEXT NOT NULL CHECK (length(trim(source_table)) > 0),
    source_column                TEXT NOT NULL CHECK (length(trim(source_column)) > 0),
    source_row_key               TEXT NOT NULL CHECK (length(trim(source_row_key)) > 0),
    source_sha256                TEXT NOT NULL CHECK (length(source_sha256) = 64),
    target_language              TEXT NOT NULL CHECK (length(trim(target_language)) > 0),
    translated_text              TEXT CHECK (translated_text IS NULL OR length(trim(translated_text)) > 0),
    status                       TEXT NOT NULL DEFAULT 'requested'
                                 CHECK (status IN ('requested', 'translated', 'reviewed', 'rejected')),
    translator_kind              TEXT CHECK (translator_kind IS NULL OR translator_kind IN ('model', 'tool', 'person')),
    translator_name              TEXT CHECK (translator_name IS NULL OR length(trim(translator_name)) > 0),
    requested_at_stage           TEXT NOT NULL CHECK (length(trim(requested_at_stage)) > 0),
    due_stage                    TEXT CHECK (due_stage IS NULL OR length(trim(due_stage)) > 0),
    reviewed_by_kind             TEXT CHECK (reviewed_by_kind IS NULL OR reviewed_by_kind IN ('model', 'tool', 'person')),
    reviewed_by_name             TEXT CHECK (reviewed_by_name IS NULL OR length(trim(reviewed_by_name)) > 0),
    reviewed_at                  TEXT,
    review_reason                TEXT CHECK (review_reason IS NULL OR length(trim(review_reason)) > 0),
    superseded_by_translation_id INTEGER REFERENCES translations(translation_id),
    created_at                   TEXT NOT NULL,
    created_by_session           TEXT NOT NULL,
    updated_at                   TEXT NOT NULL,
    updated_by_session           TEXT NOT NULL,
    -- text exists exactly once the request has been answered
    CHECK ((status = 'requested') = (translated_text IS NULL)),
    -- who translated it: none while requested, both once past it
    CHECK ((status = 'requested' AND translator_kind IS NULL AND translator_name IS NULL)
        OR (status <> 'requested' AND translator_kind IS NOT NULL AND translator_name IS NOT NULL)),
    -- who reviewed it: all three exactly when reviewed or rejected, and never the translator (OD-30)
    CHECK ((status IN ('reviewed', 'rejected')
            AND reviewed_by_kind IS NOT NULL AND reviewed_by_name IS NOT NULL AND reviewed_at IS NOT NULL)
        OR (status NOT IN ('reviewed', 'rejected')
            AND reviewed_by_kind IS NULL AND reviewed_by_name IS NULL AND reviewed_at IS NULL)),
    CHECK (reviewed_by_name IS NULL OR reviewed_by_name <> translator_name),
    -- a rejection says why; a row that was not reviewed holds no reason
    CHECK (status <> 'rejected' OR review_reason IS NOT NULL),
    CHECK (status IN ('reviewed', 'rejected') OR review_reason IS NULL),
    CHECK (superseded_by_translation_id IS NULL OR superseded_by_translation_id <> translation_id)
);

CREATE VIEW v_translations_current AS
SELECT translation_id, source_table, source_column, source_row_key, source_sha256, target_language,
       translated_text, status, translator_kind, translator_name, requested_at_stage, due_stage,
       reviewed_by_kind, reviewed_by_name, reviewed_at
FROM translations
WHERE status IN ('translated', 'reviewed') AND superseded_by_translation_id IS NULL;

PRAGMA user_version = 144;
