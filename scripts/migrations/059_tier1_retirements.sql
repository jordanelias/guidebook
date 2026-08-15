-- 059_tier1_retirements.sql
-- SCHEMA migration — drop the three database objects in the Tier-1 retirement
-- batch. Owner approval 2026-08-14 ("APPROVE WHOLE TIER-1 BATCH"), scoped by
-- workplan/2026-08-14-remediation-workplan.md §6.
--
-- The file half of the batch (scripts/convert/**, scripts/db/**, eight of ten
-- scripts/migrate/**, init_db.py, validate_db.py, migrate_evidence_sources_v2.py,
-- test_generate_parts_4_2.py, two superseded probe logs) is archived in the same
-- commit under _archived/, mirroring origin paths. Nothing is deleted.
--
-- WHAT GOES, AND ON WHAT AUTHORITY
--
--   db_meta (2 rows)
--     A second schema-version marker that never tracked migrations and sat
--     forty-one versions stale. Retired as an authority on 2026-08-06 in favour
--     of PRAGMA user_version, which CLAUDE.md §4 names as the only marker. The
--     two surviving rows are `created_at` and `project` — a creation stamp and a
--     repo name, both recoverable from git. Nothing reads this table: verified
--     with git grep across scripts/, schemas/, tools/, governance/ and .github/.
--
--   population_reclass (29 rows)
--     Held-031 scaffolding for the population-taxonomy replacement.
--     DR-2026-07-23-population-schema-replace lists it under follow-ups in its
--     own words: "population_reclass (held-031 scaffolding) — now obsolete;
--     retire in a follow-up." This is that follow-up.
--     THE CROSSWALK IS NOT LOST. Its 29 rows are the old-code -> canonical-code
--     rename map, and they survive in three places: the INSERT statements inside
--     the 057 baseline, which is immutable and replayed on every rebuild; the
--     deferred entry in governance/retired-vocabulary.yaml, which spells the
--     mapping out (VIS->BLIND, UPL->LMB, DBL->DEAFBLIND, and the rest); and
--     DR-2026-07-22-population-representation-reconciliation, which cites the
--     column by name. A reader who needs the map has three routes to it.
--     Its one live mention is an EXCLUDED_TABLES entry in validate_population.py
--     — an exclusion, not a read. Removed in the same commit, since excluding a
--     table that does not exist is dead reasoning that reads as live.
--
--   v_source_reach (view)
--     Superseded by v_source_reach_all, which answers the same question honestly:
--     v_source_reach INNER JOINs through specification_source_links, so a source
--     that reaches nothing simply vanishes from the result and the view cannot
--     distinguish "no such source" from "source reaches no specification".
--     v_source_reach_all LEFT JOINs and carries an explicit `reaches` flag.
--     Checked before dropping rather than assumed: v_source_reach_all does NOT
--     reference v_source_reach — the two are independent SELECTs over the base
--     tables, so this drop cannot orphan the survivor.
--
-- Forward-only, like every migration here. Re-adding any of the three when a
-- renderer or a reader appears is a small migration; carrying them costs census
-- confusion at every audit cycle, which is what the 2026-08-14 audit spent its
-- retirement pass measuring.

DROP VIEW IF EXISTS v_source_reach;

DROP TABLE IF EXISTS db_meta;
DROP TABLE IF EXISTS population_reclass;

PRAGMA user_version = 59;
