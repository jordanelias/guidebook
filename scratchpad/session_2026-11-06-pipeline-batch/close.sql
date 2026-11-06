-- Research batch delta, captured by scripts/research/emit_batch_sql.py
-- Captured:  2026-11-06T03:09:18+00:00
-- Scratch:   scratchpad/session_2026-11-06-pipeline-batch/walk.db
-- Canonical: data/guidebook.db (schema version 116)
-- Totals:    0 insert(s), 1 update(s), 0 delete(s), 0 restore(s)
--
-- No transaction wrapper: the migration runner owns the boundary (F5).
-- Feed this to: python3 scripts/emit_data_migration.py --input <this file>

-- adversarial_passes: 0 insert(s), 1 update(s)
UPDATE "adversarial_passes" SET "closed_at" = '2026-11-06 03:09' WHERE "pass_id" = 8;
