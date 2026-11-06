-- 119_typed_harm_and_absence.sql
-- SCHEMA migration -- two states that were prose become typed columns (pipeline-operations.md section 5:
-- "a state is a coded value ... in a constrained column so it can be counted, joined and checked").
--
-- (1) source_value_extractions.harm_finding. R7: failure, harm and inadequacy are first-class evidence. The
-- research stage already types it (search_executions.harm_finding, search_candidates.harm_finding); the
-- judgment stage, where a figure becomes a row a determination and a page read, had no such column, so a
-- harm finding (a T2 report that code-compliant ramps cause incidents) was indistinguishable from any other
-- `finding` row. Only a `finding` row can carry it: the CHECK names figure_role, the same sibling-column
-- pattern as migration 116. READERS: the render contract's "why it matters" element (RENDER-CONTRACT-
-- parameters-3-and-12.md, E6) and the adversarial lens S1-harm-reached-row, whose subject is exactly "a flagged
-- harm finding reached the row it should".
--
-- (2) search_executions.absence_class. R14: a zero-yield search is evidence of ABSENCE only if the query was
-- well-formed, and the record must say query-shape failure vs wrong index vs genuine absence. That classification
-- lived in findings_note prose, which no gate or page can count. It is NULL until a human judges it, and only a
-- search that found nothing can carry one. READERS: lens L8-query-shape (its whole subject), the render Gaps
-- section (a gap stated as "searched, genuine absence" differs from "searched, query-shape failure"), and
-- `db.py coverage`.
--
-- ADD COLUMN, NOT A REBUILD, as in 116: SQLite checks an added CHECK against the existing rows, and every
-- existing row satisfies both (harm_finding defaults to 0; absence_class defaults to NULL).

ALTER TABLE source_value_extractions ADD COLUMN harm_finding INTEGER NOT NULL DEFAULT 0
  CHECK (harm_finding IN (0, 1))
  CHECK (harm_finding = 0 OR figure_role = 'finding');

ALTER TABLE search_executions ADD COLUMN absence_class TEXT
  CHECK (absence_class IS NULL OR absence_class IN ('query_shape_failure', 'wrong_index', 'genuine_absence'))
  CHECK (absence_class IS NULL OR results_found = 0);

PRAGMA user_version = 119;
