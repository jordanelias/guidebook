-- 110_drop_scheduled_run_tables.sql
-- SCHEMA migration -- the run-record tables of the two scheduled DB-writing workflows are dropped
-- (plan step 1.5; RULINGS R2 and R49(b)). The same commit deletes the workflows, their scripts and
-- their tests, so nothing writes these tables any more and nothing reads them.
--
-- WHY. The scheduled `source-verification` workflow committed straight into the database blob, which
-- breaks CLAUDE.md rule 3 (migrations only) on a timer and hands every open pull request that
-- touches the blob a binary conflict whenever it fires. R2 deletes the workflows.
--
-- R3 MARKER (LED-169 ACTION (4)). `pipeline_runs` holds six rows, written by the workflow and by no
-- migration (it is in migration_reproducibility's EXEMPT_TABLES), so a rebuild does not reproduce
-- them and they survive only in the git history of the blob. Measured 2026-10-14 before the migration
-- (re-run rather than trust):
--     select run_id, total_resolved, created_by_session from pipeline_runs order by run_id;
--       2026-08-24 06:33 | 0 | 32697832238        2026-09-28 06:06 | 0 | 36384796860
--       2026-09-07 10:57 | 0 | 34114064926        2026-10-05 06:10 | 0 | 37271064510
--       2026-09-21 11:20 | 0 | 35593474934        2026-10-12 06:09 | 0 | 38211139899
--   Four of them (2026-09-21 onward) were written by bot commits on main under the subject prefix
--   "source-verification:"; the 2026-08-24 and 2026-09-07 rows first appear in the blob at root commit 55ae5c1
--   (`git log -S<run created_by_session> -- data/guidebook.db`), under no such commit. No run
--   resolved a DOI (total_resolved is 0 in all six); four runs enriched `evidence_sources` rows in
--   phase 4 (phase_4_enriched 0, 0, 1, 1, 2, 1 in date order); those rewrites are the divergence that
--   plan steps 1.5b and 1.5c deal with, and dropping this table does not undo them.
--   `url_verification_runs` holds 0 rows.
--
-- DEPENDENCIES (derived from sqlite_master and pragma foreign_key_list): no foreign key points at
-- either table, no view or trigger names them, and no data migration writes them:
--     grep -nE "(INSERT( OR [A-Z]+)? INTO|UPDATE|DELETE FROM) \"?(pipeline_runs|url_verification_runs)\"?[ (]" scripts/migrations/data_*.sql
--   finds nothing, so no AFTER_DATA marker is needed. The two auto-indexes go with their tables.
--
-- WHAT THIS DOES NOT CLEAR. The standing divergence of `evidence_sources` and
-- `evidence_source_authors` between the blob and the chain is a separate act (plan steps 1.5a to 1.5c).

DROP TABLE pipeline_runs;
DROP TABLE url_verification_runs;

PRAGMA user_version = 110;
