-- 117_best_practice_view_shows_code_floor.sql
-- SCHEMA migration -- a determination resting only on the regulatory stratum is shown in the best-practice
-- view, flagged, instead of being filtered out of it.
--
-- RULING. Owner OR-7 (references/project-standards.md, "Owner rulings 2026-10-29 (second)"): "Yes, show it
-- flagged -- Empty circle." Its reading item 5 says the view stops filtering `code_floor_only = 0`; and
-- "Owner rulings 2026-10-30 (second)" ratifies that a determination resting on T4 to T6 alone keeps the
-- weak band and flag ("Yes, keep the ○ band and flag").
--
-- WHICH ROWS THIS ADMITS, stated exactly. The dropped filter was on code_floor_only (set when the threshold is
-- T6-only). Two kinds of row had it set: (a) regulatory_stratum_only = 1, resting on the regulatory stratum
-- alone, which migration 116's CHECK pins to the empty circle; and (b) the proxy branch of assess_cell, where a
-- T6 threshold is paired with anchoring-tier direction findings (rests_on_proxy_inference = 1,
-- regulatory_stratum_only = 0), which takes the band its mixed evidence earns and states that it rests on proxy
-- inference. (b) is not "a determination resting on T4 to T6 alone", so showing it with its flags is within the
-- ruling; it also appears in v_code_floor_only, as a code-floor row. Both flags stay on the row.
--
-- WHAT THE FILTER WAS FOR, AND WHY DROPPING IT IS SAFE. It was the convergence-laundering guard of
-- migrations 027/029: it kept a code floor from reading as a best-practice claim. The marker CHECK of 116
-- and validate_evidence_state (a code-floor row is never `stated`) now carry that guard on the row itself.
--
-- READERS. sqlite_master names no other view over v_best_practice; the code readers are the migrations and
-- audit comments (re-derive: git grep -nI v_best_practice -- scripts governance skills references). The live table
-- holds no live determination when this is written, so no query result changes today.

DROP VIEW v_best_practice;
CREATE VIEW v_best_practice AS
    SELECT *
    FROM "specifications"
    WHERE state IN ('stated', 'provisional')
      AND retired_at IS NULL;

PRAGMA user_version = 117;
