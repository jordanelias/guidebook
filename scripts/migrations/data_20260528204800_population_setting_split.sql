-- data_20260528204800_population_setting_split.sql
--
-- Data correction: split conflated (population, setting) values into the
-- canonical population code(s) plus the new setting column added by
-- migration 020. Per owner directive 2026-05-28 ("populations have to
-- correspond to our disability populations, not things like secondary
-- classroom") and the disability-centric framing lock of 2026-05-11.
--
-- Scope: 7 rows in reasoning_doc_citations (room-acoustic-performance),
-- and 1 distinct value in spec_value_probes (item A-18 walk).
--
-- Mapping confirmed against canonical populations table (22 codes; ALL =
-- "applies universally to all populations"). Rows where population was
-- already NULL (the comparator-type / statutory-status qualitative rows)
-- are left untouched -- they are correctly NULL.
--
-- Append-only data migration; idempotent because each UPDATE keys on
-- the exact pre-migration string value, which is rewritten by the
-- statement itself.

BEGIN;

-- ============================================================
-- reasoning_doc_citations
-- ============================================================

-- "general (primary classroom)" -> ALL + primary classroom
UPDATE reasoning_doc_citations
   SET population = 'ALL',
       setting    = 'primary classroom'
 WHERE population = 'general (primary classroom)';

-- "general (secondary classroom)" -> ALL + secondary classroom
UPDATE reasoning_doc_citations
   SET population = 'ALL',
       setting    = 'secondary classroom'
 WHERE population = 'general (secondary classroom)';

-- "DEAF / hearing-impaired (specially-resourced provision)"
--   -> DEAF + specially-resourced provision
UPDATE reasoning_doc_citations
   SET population = 'DEAF',
       setting    = 'specially-resourced provision'
 WHERE population = 'DEAF / hearing-impaired (specially-resourced provision)';

-- "NDV/AUT (special hearing or communication needs - inclusive)"
--   -> NDV,AUT (compound) + setting
UPDATE reasoning_doc_citations
   SET population = 'NDV,AUT',
       setting    = 'special hearing or communication needs - inclusive'
 WHERE population = 'NDV/AUT (special hearing or communication needs - inclusive)';

-- "NDV/AUT" -> NDV,AUT (compound), no setting
UPDATE reasoning_doc_citations
   SET population = 'NDV,AUT'
 WHERE population = 'NDV/AUT';

-- ============================================================
-- spec_value_probes
-- ============================================================

-- "DEAF (pediatric hearing-aid / cochlear-implant users in classroom listening)"
--   -> DEAF + setting captures the qualifier
UPDATE spec_value_probes
   SET population = 'DEAF',
       setting    = 'pediatric hearing-aid / cochlear-implant users in classroom listening'
 WHERE population = 'DEAF (pediatric hearing-aid / cochlear-implant users in classroom listening)';

-- The 'ALL' and 'AUT, PCS, DEM, MH, PAIN, OFS' rows are left as-is.
-- 'ALL' is already a canonical population code. The comma-separated multi-
-- population value uses the same convention introduced for NDV,AUT above.

COMMIT;
