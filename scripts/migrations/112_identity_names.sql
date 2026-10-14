-- 112_identity_names.sql
-- SCHEMA migration -- the identity registry and its ICF map take the names of the lens vocabulary
-- (plan Phase 3 base; RULINGS R14 as narrowed, the LED-127 confirmation recorded in R49 (c)).
--
--   populations                         -> base_taxonomy_identity      (population_code -> identity_code)
--   population_icf_links                -> identity_icf_map            (population_code -> identity_code)
--
-- SQLite rewrites every REFERENCES clause, index and sqlite_sequence row that names them, so the five
-- foreign keys into populations(population_code) and the self-reference follow. The index names
-- idx_picf_icf and the autoindexes keep their abbreviations: SQLite has no RENAME INDEX.
--
-- NOT RENAMED, deliberately: evidence_population_match and its target_population and study_population
-- columns. LED-127 names served_group and study_group for them and keeps them out of the lens
-- vocabulary; that is the owner's choice of name, and four committed data migrations dated after
-- migration 095's marker INSERT into the table, which would need the marker and a re-emission.
--
-- NO AFTER_DATA MARKER, because no data migration dated after 095's marker names the three identifiers
-- renamed here. Re-derive before trusting this sentence:
--   grep -lwE 'populations|population_icf_links|population_code' scripts/migrations/data_*.sql \
--     | xargs -n1 basename | cut -d_ -f2 | awk '$1>"20260920060857"'
-- prints nothing, and the same command with evidence_population_match in place of the three prints
-- timestamps (so the command can match). A rebuild replays this file in its numeric place.
--
-- FUTURE DATA MIGRATIONS must use the new names. One emitted under the old names and unmerged when this
-- lands has to be re-emitted: emit_batch_sql captures the live table names, and refuses a scratch whose
-- user_version differs from the canonical database.

ALTER TABLE populations RENAME TO base_taxonomy_identity;
ALTER TABLE base_taxonomy_identity RENAME COLUMN population_code TO identity_code;
ALTER TABLE population_icf_links RENAME TO identity_icf_map;
ALTER TABLE identity_icf_map RENAME COLUMN population_code TO identity_code;

PRAGMA user_version = 112;
