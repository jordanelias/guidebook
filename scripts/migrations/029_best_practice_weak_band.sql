-- 029_best_practice_weak_band.sql
-- ENGINE-LAG follow-up. Per DR-2026-07-21-evidence-architecture-option-a-execution §5 item 1,
-- and under DR-2026-07-21-product-posture-thinking-tool-not-authority (RATIFIED): the machinery
-- adjudicates the evidence and surfaces the best-supported figure at a stated strength; a weak-band
-- figure is a figure for thought, flagged, never suppressed and never promoted.
--
-- Option A (§1.1): a determination whose entire evidence basis is the regulatory stratum
-- (T4-T6, regulatory_stratum_only) IS a best-practice determination at the WEAK band (circle) —
-- rendered flagged, in every register, never at anchoring strength. The engine contradicted this:
-- migration 027's v_best_practice EXCLUDED those rows outright. This migration reconciles the engine
-- with the ratified doctrine (removes the [ENGINE-LAG] contradiction for the view layer).
--
-- CHANGE:
--   1. Drop the two regulatory_stratum_only guards (the column predicate AND the tier_basis marker
--      guard) added by migration 027, so weak-band rows surface.
--   2. Add a `strength_band` column so surfaced weak rows are DISTINCT and never silently mixed with
--      anchored rows (the DR's explicit requirement). Computed from the authoritative flag columns,
--      not by parsing tier_basis.
--
-- DELIBERATELY NOT CHANGED (flagged for owner, not decided unilaterally):
--   - The `code_floor_only = 0` guard (T6-only, migration 026) is RETAINED. code_floor_only is a
--     subset of the regulatory stratum and under a strict reading of Option A ("T4-T6") would also
--     surface at the weak band; but DR §5.1 scopes this execution item to regulatory_stratum_only,
--     and there are currently 0 code_floor_only cells, so the choice is moot for present data.
--     Extending to code_floor_only is a one-line follow-up once the owner confirms intent. Retaining
--     it avoids a semantic asymmetry (T4-6 surfacing while pure-T6 does not) being decided here.
--
-- REMAINING §5 HARDENING NOT IN THIS MIGRATION (tracked, not restamped here):
--   - re-derive the 3 affected cells (E-06/MOB, A-02/ALL, A-08/ALL) under a bumped RULE_VERSION with
--     fresh derivation_sha; rework scripts/audit/register_integrity_check.py I3 lexicon to the amended
--     (unflagged / above-band) form; renderer register-map row 3. This migration lands view behavior
--     only; it does not restamp derivations or touch tier assignments.

DROP VIEW IF EXISTS v_best_practice;
CREATE VIEW v_best_practice AS
    SELECT *,
           CASE
               WHEN regulatory_stratum_only = 1 THEN 'weak'
               ELSE 'anchored'
           END AS strength_band
    FROM evidence_cell_state
    WHERE state IN ('stated', 'provisional')
      AND code_floor_only = 0;
