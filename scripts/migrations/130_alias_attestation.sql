-- 130_alias_attestation.sql
-- SCHEMA migration -- a form says how it is attested, and a search says which forms it used.
-- Tooling (IMP-22, workplan T-026, forms home per workplan/2026-11-12-bidirectional-pipeline/
-- tasks/T-028-design.md section 2, delegated resolution of OD-03); no research rows.
--
-- AFTER_DATA: 20261106053823
-- (Why the marker: `migrate_db.py --rebuild` runs schema migrations before the data migrations that
-- follow the last marker, and committed data migrations write term_aliases. Without it the rebuild
-- fills `attestation` before those rows exist and `migration_reproducibility.py --deep` diverges.
-- Value: the newest data migration at the time of writing.)
--
-- WHY. Nothing typed separated a term found in a national instrument from one a model generated:
-- provenance lived in `notes` (substring markers) and, since migration 125, in an observation
-- pointer. A search run on an invented word returned nothing, and the empty result was recorded as
-- an absent literature. Now a form carries its attestation in a cell that names it, with the
-- locator that warrants it, and a search records which forms it fired.
--
-- term_aliases is the one forms home (design section 2): columns are ADDED; its key is NOT changed
-- (the occurrence grain is T-028's rebuild). `attestation` is NOT NULL with DEFAULT 'unrecorded'
-- (SQLite refuses a NOT NULL ADD COLUMN with no default), so a writer that omits it writes
-- `unrecorded`, which is true of it. The two cross-column CHECKs ride on the LAST column added
-- (ADD COLUMN may carry a CHECK naming other columns), so the writer is not the only guard.

ALTER TABLE term_aliases ADD COLUMN attestation TEXT NOT NULL DEFAULT 'unrecorded'
    CHECK (attestation IN ('instrument','other_source','owner_supplied','model_seed','unrecorded'));
ALTER TABLE term_aliases ADD COLUMN source_url TEXT
    CHECK (source_url IS NULL OR source_url GLOB 'http*://*');
ALTER TABLE term_aliases ADD COLUMN source_page TEXT;
ALTER TABLE term_aliases ADD COLUMN source_line INTEGER
    CHECK (source_line IS NULL OR source_line > 0);
ALTER TABLE term_aliases ADD COLUMN source_clause TEXT
    CHECK (
        -- an attested occurrence says where
        (attestation NOT IN ('instrument','other_source')
         OR observation_id IS NOT NULL
         OR (source_url IS NOT NULL AND (source_page IS NOT NULL OR source_clause IS NOT NULL)))
        -- a seed or an unrecorded form says nowhere
        AND (attestation IN ('instrument','other_source')
         OR (source_url IS NULL AND source_page IS NULL AND source_line IS NULL
             AND source_clause IS NULL))
    );

-- FILL, from what each row already says, in alias_provenance_audit.classify()'s precedence. INSTR,
-- not LIKE: LIKE is case-insensitive and classify() is a case-sensitive `in`. Never `instrument`
-- by inference. The VERIFIED-* rows carry no observation and no locator, so the first CHECK would
-- refuse `other_source` for them: they are `unrecorded` until T-107 re-attests them with a locator.
UPDATE term_aliases SET attestation = CASE
    WHEN INSTR(COALESCE(notes,''), 'VERIFIED-GLOSSARY') > 0 THEN 'unrecorded'
    WHEN INSTR(COALESCE(notes,''), 'VERIFIED-CROSS')    > 0 THEN 'unrecorded'
    WHEN INSTR(COALESCE(notes,''), 'VERIFIED-NATIVE')   > 0 THEN 'unrecorded'
    WHEN observation_id IS NOT NULL                          THEN 'other_source'
    WHEN INSTR(COALESCE(notes,''), 'model-generated')   > 0 THEN 'model_seed'
    ELSE 'unrecorded' END;

-- THE JUNCTION: which forms a search fired. It points at a form by term_aliases' PRESENT KEY with a
-- real foreign key, not by rowid: SQLite cannot declare a foreign key on a rowid, and the capture
-- path (scripts/research/emit_batch_sql.py) diffs a table by its declared key and does not carry
-- implicit rowids, so a rowid taken on a scratch copy could name another row in the canonical
-- database. T-028's rebuild remaps this table by that key to a surrogate form_id.
CREATE TABLE search_execution_forms (
    exec_id            INTEGER NOT NULL REFERENCES search_executions(exec_id),
    term_id            TEXT NOT NULL,
    alias              TEXT NOT NULL,
    language           TEXT NOT NULL,
    created_at         TEXT NOT NULL,
    created_by_session TEXT NOT NULL,
    PRIMARY KEY (exec_id, term_id, alias, language),
    FOREIGN KEY (term_id, alias, language) REFERENCES term_aliases(term_id, alias, language)
);

PRAGMA user_version = 130;
