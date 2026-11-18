-- 155_quantity_kind_ground_in_base.sql
-- SCHEMA migration, compensating 143 (T-083; owner statements 2026-11-18, OD-71: "the base grounds itself except for
-- when evidence that allows for new terms/aliases/parameters to be found is pointed to as justification; but this
-- justification should then be absorbed by base and grounded as if it were always there", and "ref_id as provenance?
-- sure. but it's ONLY for provenance"). No data rows.
--
-- 143 gave base_parameters (a base table) `quantity_kind_observation_id REFERENCES observed_terms`, a foreign key into
-- the evidence stage, as the warrant of a parameter's quantity kind. It is dropped. The warrant is now the base's own
-- cells, the pattern 151 gave term_relations:
--  * WHERE A SOURCE STATES A VALUE OF THE QUANTITY: quantity_kind_source_url, _page, _line and _clause, spelled and
--    checked as term_aliases spells source_url, source_page, source_line and source_clause (one fact, one spelling),
--    prefixed because base_parameters holds a second warranted fact (the direction) and each fact keeps its own cells.
--    A locator is a URL plus a page or a clause; a locator part without the URL says nowhere. A row with a kind
--    carries a locator. Only the locator is absorbed, not the source's quoted words (OD-71 does not say they are).
--  * quantity_kind_ref_id is PROVENANCE ONLY: nullable, no foreign key, validated against nothing, read by no decision.
-- No row moves: no parameter carried a kind when this was written
-- (`select count(*) from base_parameters where quantity_kind is not null`), and a row with a kind and no locator would
-- fail the CHECK below rather than be copied without its warrant. Not touched: direction_ref_id (the ruling of
-- 2026-10-30 names a dependency there; whether OD-71 reaches it is the owner's).

ALTER TABLE base_parameters DROP COLUMN quantity_kind_observation_id;

ALTER TABLE base_parameters ADD COLUMN quantity_kind_source_url TEXT
    CHECK (quantity_kind_source_url IS NULL OR (
        (quantity_kind_source_url GLOB 'http://[^/' || char(32,9,10,13) || ']*'
         OR quantity_kind_source_url GLOB 'https://[^/' || char(32,9,10,13) || ']*')
        AND quantity_kind_source_url NOT GLOB '*[' || char(32,9,10,13) || ']*'));

ALTER TABLE base_parameters ADD COLUMN quantity_kind_source_page TEXT
    CHECK (quantity_kind_source_page IS NULL OR TRIM(quantity_kind_source_page, char(32,9,10,13)) <> '');

ALTER TABLE base_parameters ADD COLUMN quantity_kind_source_line INTEGER
    CHECK (quantity_kind_source_line IS NULL
           OR (typeof(quantity_kind_source_line) = 'integer' AND quantity_kind_source_line > 0));

ALTER TABLE base_parameters ADD COLUMN quantity_kind_source_clause TEXT
    CHECK (
        (quantity_kind_source_clause IS NULL OR TRIM(quantity_kind_source_clause, char(32,9,10,13)) <> '')
        -- a locator part says nowhere without the URL
        AND (quantity_kind_source_url IS NOT NULL
             OR (quantity_kind_source_page IS NULL AND quantity_kind_source_line IS NULL
                 AND quantity_kind_source_clause IS NULL))
        -- a kind is a judgment and carries where a source states a value of the quantity
        AND (quantity_kind IS NULL
             OR (quantity_kind_source_url IS NOT NULL
                 AND (quantity_kind_source_page IS NOT NULL OR quantity_kind_source_clause IS NOT NULL)))
    );

ALTER TABLE base_parameters ADD COLUMN quantity_kind_ref_id TEXT;   -- provenance only (OD-71): no foreign key

PRAGMA user_version = 155;
