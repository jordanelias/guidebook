-- 126_extraction_value_as_written.sql
-- SCHEMA migration -- an extraction records the source's own WORDING of a figure it had to translate.
--
-- `claimed_value` is a reading of the source's wording, not a copy of a numeral in it: the Dutch
-- "vijf procent" is 5 and %, the Finnish "viisi prosenttia" is 5 and %, "1,200" is 1200 or 1.2. Until
-- now a figure written in words had no route: it was stored as words (which the determination engine
-- cannot read) or passed the number-in-the-quote guard by accident. This column holds the span of
-- `claim_text` that the numeral and unit translate (owner, 2026-11-12: "just translate these into
-- numbers/units"); the numeral stays in `claimed_value` and the unit in `claimed_unit`. NULL means the
-- quote states the claimed numbers as unambiguous numerals.
--
-- ONE NULLABLE COLUMN, ALTER TABLE ... ADD COLUMN, with a one-column CHECK. The rules that read two
-- columns (the wording is required exactly when a claimed number is not stated as a numeral; it must
-- occur in `claim_text` and must not state a different figure) live in `db._require_stated_numbers`,
-- which `add-extraction` and `amend-extraction` reach. Nothing is backfilled: whether a stored row
-- needs a wording is a judgment about its source, made by a later task through `amend-extraction`.
-- No view, trigger or index names a column that changes; the views that name the table
-- (`select name from sqlite_master where type='view' and sql like '%source_value_extractions%'`) are
-- untouched by a new nullable column. The determination engine does not read the column.

ALTER TABLE source_value_extractions ADD COLUMN value_as_written TEXT CHECK (value_as_written IS NULL OR length(trim(value_as_written)) > 0);

PRAGMA user_version = 126;
