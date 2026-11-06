-- 117_best_practice_view_shows_code_floor.sql
-- SCHEMA migration -- a determination resting only on the regulatory stratum is shown in the best-practice
-- view, flagged, instead of being filtered out of it.
--
-- RULING. Owner OR-7 (references/project-standards.md, "Owner rulings 2026-10-29 (second)"): "Yes, show it
-- flagged -- Empty circle." Its reading item 5 says the view stops filtering `code_floor_only = 0`; and
-- "Owner rulings 2026-10-30 (second)" ratifies that a determination resting on T4 to T6 alone keeps the
-- weak band and flag ("Yes, keep the ○ band and flag"). Migration 116 already guarantees the glyph: a row
-- with regulatory_stratum_only = 1 can carry only the empty circle, so the rows this admits cannot be
-- mistaken for full-strength anchoring. The flag stays on the row (code_floor_only, regulatory_stratum_only).
--
-- WHAT THE FILTER WAS FOR, AND WHY DROPPING IT IS SAFE. It was the convergence-laundering guard of
-- migrations 027/029: it kept a code floor from reading as a best-practice claim. The marker CHECK of 116
-- and validate_evidence_state (a code-floor row is never `stated`) now carry that guard on the row itself.
--
-- READERS. sqlite_master names no other view over v_best_practice; the code readers are the migrations and
-- audit comments (re-derive: git grep -nI v_best_practice -- scripts governance skills). The live table
-- holds no live determination when this is written, so no query result changes today.

DROP VIEW v_best_practice;
CREATE VIEW v_best_practice AS
    SELECT *
    FROM "specifications"
    WHERE state IN ('stated', 'provisional')
      AND retired_at IS NULL;

PRAGMA user_version = 117;
