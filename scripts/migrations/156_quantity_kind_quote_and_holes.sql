-- 156_quantity_kind_quote_and_holes.sql
-- SCHEMA migration, compensating 155 (committed, not edited): T-083 repair after the adversarial pass. No data rows.
--
-- 1. THE QUOTED WORDS. 155 absorbed only the locator of a quantity kind's warrant (OD-71, 2026-11-18), so T-020's
--    refusal of a warrant whose words state no value had nothing left to read, and a kind could be written on any
--    URL and page. quantity_kind_quote holds the source's words where it states a value of the quantity: a base cell,
--    the justification absorbed into the base's own columns; no foreign key, nothing read from the evidence stage.
--    The writer (db._kind_refusal) refuses a quote that holds no digit (any script's digits, so the CHECK below does
--    not repeat that test with an ASCII class). WHETHER THE BASE SHOULD REPEAT A SOURCE'S QUOTED WORDS IS STILL THE
--    OWNER'S QUESTION: OD-71's "What it does not decide" leaves it open; the coordinator chose to keep the words so
--    the refusal T-020 built is not lost, and the owner may reverse that.
-- 2. ALL OR NONE. A kind, its quote, its URL and a page or a clause are present together or absent together; a
--    locator part, a line, a ref_id or a quote with no kind is refused.
-- 3. HOLES CLOSED, as 154 closed them on source_clauses: a cell holding only whitespace is blank by 154's character set
--    (no-break space and the Unicode spaces included) plus the zero-width characters U+200B, U+200C, U+200D, U+2060
--    and U+FEFF (dbcore.ZERO_WIDTH holds the same five; a test compares the two); a zero-width character anywhere in a
--    URL, page, clause or ref_id is refused, and a URL holds no whitespace of that set; every text cell must be TEXT
--    (no BLOB, no number).
-- 4. quantity_kind_ref_id stays PROVENANCE ONLY: no foreign key, validated against nothing but its shape.
--
-- Rebuilt by dropping 155's five cells (the clause cell first: its CHECK names the others) and adding them again with
-- the new CHECKs. That is correct only while no parameter carries a kind (none did when this was written:
-- `select count(*) from base_parameters where quantity_kind is not null`); the guard below aborts the migration rather
-- than drop a warrant if one does.

CREATE TEMP TABLE _156_guard (kinded INTEGER CHECK (kinded = 0));
INSERT INTO _156_guard SELECT COUNT(*) FROM base_parameters WHERE quantity_kind IS NOT NULL;
DROP TABLE _156_guard;

ALTER TABLE base_parameters DROP COLUMN quantity_kind_source_clause;
ALTER TABLE base_parameters DROP COLUMN quantity_kind_source_line;
ALTER TABLE base_parameters DROP COLUMN quantity_kind_source_page;
ALTER TABLE base_parameters DROP COLUMN quantity_kind_source_url;
ALTER TABLE base_parameters DROP COLUMN quantity_kind_ref_id;

ALTER TABLE base_parameters ADD COLUMN quantity_kind_source_url TEXT
    CHECK (quantity_kind_source_url IS NULL OR (typeof(quantity_kind_source_url) = 'text'
        AND (quantity_kind_source_url GLOB 'http://[^/' || char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288) || char(8203,8204,8205,8288,65279) || ']*'
             OR quantity_kind_source_url GLOB 'https://[^/' || char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288) || char(8203,8204,8205,8288,65279) || ']*')
        AND quantity_kind_source_url NOT GLOB '*[' || char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288) || char(8203,8204,8205,8288,65279) || ']*'));

ALTER TABLE base_parameters ADD COLUMN quantity_kind_source_page TEXT
    CHECK (quantity_kind_source_page IS NULL OR (typeof(quantity_kind_source_page) = 'text'
        AND trim(quantity_kind_source_page, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288) || char(8203,8204,8205,8288,65279)) <> ''
        AND quantity_kind_source_page NOT GLOB '*[' || char(8203,8204,8205,8288,65279) || ']*'));

ALTER TABLE base_parameters ADD COLUMN quantity_kind_source_line INTEGER
    CHECK (quantity_kind_source_line IS NULL
           OR (typeof(quantity_kind_source_line) = 'integer' AND quantity_kind_source_line > 0));

ALTER TABLE base_parameters ADD COLUMN quantity_kind_source_clause TEXT
    CHECK (quantity_kind_source_clause IS NULL OR (typeof(quantity_kind_source_clause) = 'text'
        AND trim(quantity_kind_source_clause, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288) || char(8203,8204,8205,8288,65279)) <> ''
        AND quantity_kind_source_clause NOT GLOB '*[' || char(8203,8204,8205,8288,65279) || ']*'));

ALTER TABLE base_parameters ADD COLUMN quantity_kind_ref_id TEXT                -- provenance only (OD-71): no foreign key
    CHECK (quantity_kind_ref_id IS NULL OR (typeof(quantity_kind_ref_id) = 'text'
        AND trim(quantity_kind_ref_id, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288) || char(8203,8204,8205,8288,65279)) <> ''
        AND quantity_kind_ref_id NOT GLOB '*[' || char(8203,8204,8205,8288,65279) || ']*'));

ALTER TABLE base_parameters ADD COLUMN quantity_kind_quote TEXT
    CHECK (
        (quantity_kind_quote IS NULL OR (typeof(quantity_kind_quote) = 'text'
            AND trim(quantity_kind_quote, char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288) || char(8203,8204,8205,8288,65279)) <> ''))
        -- a kind, its quote, its URL and a page or a clause: all present, or all absent
        AND ((quantity_kind IS NULL AND quantity_kind_quote IS NULL AND quantity_kind_source_url IS NULL
              AND quantity_kind_source_page IS NULL AND quantity_kind_source_line IS NULL
              AND quantity_kind_source_clause IS NULL AND quantity_kind_ref_id IS NULL)
          OR (quantity_kind IS NOT NULL AND quantity_kind_quote IS NOT NULL AND quantity_kind_source_url IS NOT NULL
              AND (quantity_kind_source_page IS NOT NULL OR quantity_kind_source_clause IS NOT NULL)))
    );

PRAGMA user_version = 156;
