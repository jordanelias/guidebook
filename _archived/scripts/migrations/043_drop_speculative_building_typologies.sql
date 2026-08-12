-- 043_drop_speculative_building_typologies.sql
-- SCHEMA migration — remove a table added yesterday on speculation.
--
-- building_typologies was created by migration 042 with 0 rows and, as an
-- adversarial pass established, zero references anywhere in the repo outside
-- 042 itself. Its stated justification pointed at case_studies.building_type —
-- a free-text column in a table that also has 0 rows.
--
-- 042's own comment sets the standard it failed: "Add either when there is data
-- that cannot be expressed without it." That test was applied to two other
-- tables in the same migration and not to this one.
--
-- A pre-existing typology vocabulary already exists in scripts/convert/
-- convert_rooms.py (NR-* codes: Education, Healthcare, Workplace, Retail,
-- Cultural, Hospitality, Transport). If a typology table is ever wanted, it
-- should be seeded from that rather than invented again.
--
-- Forward-only; user_version -> 43.

DROP TABLE IF EXISTS building_typologies;
