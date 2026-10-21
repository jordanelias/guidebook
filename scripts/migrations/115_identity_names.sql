-- 115_identity_names.sql
-- SCHEMA migration -- the identity lens registry and its ICF map take the lens's own name (plan Phase 3
-- base; RULINGS R14 narrowed to M4, confirmed in R49(c); LED-127, LED-121). `populations` is the
-- identity lens (owner, 2026-08-28), and its key was the one lens key still called population_code
-- while every referencing column already said identity_code.
--
--   populations                  -> base_taxonomy_identity   (population_code -> identity_code)
--   population_icf_links         -> identity_icf_map         (population_code -> identity_code)
--
-- NOT IN THIS FILE: evidence_population_match and its target_population / study_population columns.
-- LED-127 names them served_group / study_group and keeps them out of the lens vocabulary, which R14's
-- evidence_identity_match contradicts; the name is the owner's. Renaming the table needs an
-- AFTER_DATA marker, because data migrations dated after 095 INSERT into it.
--
-- NO AFTER_DATA MARKER for the two renames above. Two facts together make that safe, and the second
-- is the operative one: (1) no committed data migration dated after the 095 cutoff names the renamed
-- objects (must print nothing; the literal is 095's cutoff, not today's):
--   grep -lwE 'populations|population_icf_links|population_code' scripts/migrations/data_*.sql | xargs -n1 basename | cut -d_ -f2 | awk '$1>"20260920060857"'
-- and (2) migrations 113 and 114 carry AFTER_DATA markers at the latest data_ timestamp, so
-- migrate_db.build_plan replays 115 after every committed data migration whatever it names. If (2)
-- ever changes, (1) is the check that must still hold.
--
-- SQLite rewrites every REFERENCES clause, the UNIQUE autoindex and the sqlite_sequence row itself;
-- idx_picf_icf keeps its name (there is no RENAME INDEX) and its column list is rewritten. No view and
-- no trigger names either table.

ALTER TABLE populations RENAME TO base_taxonomy_identity;
ALTER TABLE base_taxonomy_identity RENAME COLUMN population_code TO identity_code;
ALTER TABLE population_icf_links RENAME TO identity_icf_map;
ALTER TABLE identity_icf_map RENAME COLUMN population_code TO identity_code;

PRAGMA user_version = 115;
