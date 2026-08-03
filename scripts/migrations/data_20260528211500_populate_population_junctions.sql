-- data_20260528211500_populate_population_junctions.sql
--
-- Back-fills the three population junction tables (migration 021) from the
-- current scalar population values, splitting compound (comma-separated)
-- values into one junction row per canonical code. Per owner directive
-- 2026-05-28 ("improve schema so that sqlite can accommodate everything
-- flagged properly").
--
-- Source state (canonical codes, post population/setting split):
--   reasoning_doc_citations:
--     RDC-RAP-RT60-UK-001  ALL
--     RDC-RAP-RT60-UK-002  ALL
--     RDC-RAP-RT60-UK-003  DEAF
--     RDC-RAP-RT60-UK-004  NDV,AUT
--     RDC-RAP-PAS-UK-001   NDV,AUT
--   spec_value_probes (per-probe-row):
--     population = 'ALL'
--     population = 'DEAF'
--     population = 'AUT, PCS, DEM, MH, PAIN, OFS'
--   source_value_extractions: 0 rows (nothing to migrate)
--
-- Idempotency: re-running fails on the composite PK (rows already present),
-- which is the correct signal that the migration is applied.
--
-- INSERT...SELECT keyed on the scalar value, so it is robust to row identity
-- and auditable: each statement maps exactly one scalar value to one code.

BEGIN;

-- ============================================================
-- citation_population_links  (from reasoning_doc_citations.population)
-- ============================================================
INSERT INTO citation_population_links (citation_id, population_code, created_at, created_by_session)
SELECT citation_id, 'ALL', '2026-05-28 21:15', 'session_2026-05-28-vetting-surface-and-extraction-layer'
  FROM reasoning_doc_citations WHERE population = 'ALL';

INSERT INTO citation_population_links (citation_id, population_code, created_at, created_by_session)
SELECT citation_id, 'DEAF', '2026-05-28 21:15', 'session_2026-05-28-vetting-surface-and-extraction-layer'
  FROM reasoning_doc_citations WHERE population = 'DEAF';

-- compound NDV,AUT -> two rows per citation
INSERT INTO citation_population_links (citation_id, population_code, created_at, created_by_session)
SELECT citation_id, 'NDV', '2026-05-28 21:15', 'session_2026-05-28-vetting-surface-and-extraction-layer'
  FROM reasoning_doc_citations WHERE population = 'NDV,AUT';
INSERT INTO citation_population_links (citation_id, population_code, created_at, created_by_session)
SELECT citation_id, 'AUT', '2026-05-28 21:15', 'session_2026-05-28-vetting-surface-and-extraction-layer'
  FROM reasoning_doc_citations WHERE population = 'NDV,AUT';

-- ============================================================
-- probe_population_links  (from spec_value_probes.population)
-- ============================================================
INSERT INTO probe_population_links (probe_id, population_code, created_at, created_by_session)
SELECT probe_id, 'ALL', '2026-05-28 21:15', 'session_2026-05-28-vetting-surface-and-extraction-layer'
  FROM spec_value_probes WHERE population = 'ALL';

INSERT INTO probe_population_links (probe_id, population_code, created_at, created_by_session)
SELECT probe_id, 'DEAF', '2026-05-28 21:15', 'session_2026-05-28-vetting-surface-and-extraction-layer'
  FROM spec_value_probes WHERE population = 'DEAF';

-- compound 'AUT, PCS, DEM, MH, PAIN, OFS' -> six rows per probe
INSERT INTO probe_population_links (probe_id, population_code, created_at, created_by_session)
SELECT probe_id, 'AUT', '2026-05-28 21:15', 'session_2026-05-28-vetting-surface-and-extraction-layer'
  FROM spec_value_probes WHERE population = 'AUT, PCS, DEM, MH, PAIN, OFS';
INSERT INTO probe_population_links (probe_id, population_code, created_at, created_by_session)
SELECT probe_id, 'PCS', '2026-05-28 21:15', 'session_2026-05-28-vetting-surface-and-extraction-layer'
  FROM spec_value_probes WHERE population = 'AUT, PCS, DEM, MH, PAIN, OFS';
INSERT INTO probe_population_links (probe_id, population_code, created_at, created_by_session)
SELECT probe_id, 'DEM', '2026-05-28 21:15', 'session_2026-05-28-vetting-surface-and-extraction-layer'
  FROM spec_value_probes WHERE population = 'AUT, PCS, DEM, MH, PAIN, OFS';
INSERT INTO probe_population_links (probe_id, population_code, created_at, created_by_session)
SELECT probe_id, 'MH', '2026-05-28 21:15', 'session_2026-05-28-vetting-surface-and-extraction-layer'
  FROM spec_value_probes WHERE population = 'AUT, PCS, DEM, MH, PAIN, OFS';
INSERT INTO probe_population_links (probe_id, population_code, created_at, created_by_session)
SELECT probe_id, 'PAIN', '2026-05-28 21:15', 'session_2026-05-28-vetting-surface-and-extraction-layer'
  FROM spec_value_probes WHERE population = 'AUT, PCS, DEM, MH, PAIN, OFS';
INSERT INTO probe_population_links (probe_id, population_code, created_at, created_by_session)
SELECT probe_id, 'OFS', '2026-05-28 21:15', 'session_2026-05-28-vetting-surface-and-extraction-layer'
  FROM spec_value_probes WHERE population = 'AUT, PCS, DEM, MH, PAIN, OFS';

-- source_value_extractions: 0 rows; extraction_population_links starts empty.

COMMIT;
