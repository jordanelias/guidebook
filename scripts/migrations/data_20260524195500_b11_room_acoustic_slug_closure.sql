-- data_20260524195500_b11_room_acoustic_slug_closure.sql
-- B.11 slug closure: set bpc_metadata.citation_mining_complete = 1 for room-acoustic-performance.
-- Per citation-miner skill §1 BATCH mode step 3: this is the flag flipped when all
-- in-scope T1-3 sources in a slug have either:
--   (a) backward=1 AND forward=1 (fully mined), OR
--   (b) backward=0 AND forward=0 (or partial) with a deferred_reason explaining why.
-- Final state for room-acoustic-performance: 19 fully mined / 2 deferred (RAP-10 no-DOI, RAP-27
--   CrossRef-404 backward) / 1 excluded (RAP-13, GAP-292 misclassification). All 21 rows have
--   either positive mining or a deferred_reason — protocol-complete.
-- Forward-only; idempotent.

BEGIN TRANSACTION;

UPDATE bpc_metadata
   SET citation_mining_complete = 1,
       updated_at = datetime('now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE slug = 'room-acoustic-performance'
   AND COALESCE(citation_mining_complete, 0) = 0;

COMMIT;
