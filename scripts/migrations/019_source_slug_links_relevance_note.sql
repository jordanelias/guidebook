-- 019_source_slug_links_relevance_note.sql
-- Schema migration: adds a per-link relevance note column.
--
-- The source_slug_links table records "this source is relevant to this
-- topic" but stores no statement of HOW the source is relevant. The
-- vetting surface's Evidence Spread needs a column distinguishing, for
-- each linked source, the role it plays for the topic (e.g.
-- "primary mechanistic evidence on RT60 for hearing-impaired children",
-- "international standard cited as code-baseline", "qualitative study
-- on classroom acoustic perception").
--
-- Schema-only change: adds a single nullable column. Existing rows
-- remain unchanged. Population is mining work, not a migration.
--
-- No companion DR — this is the minimal armature change the vetting
-- surface needs to surface relevance per source. The mining session
-- that populates it should produce a sister table or skill if a more
-- structured relevance taxonomy proves necessary.

BEGIN;

ALTER TABLE source_slug_links ADD COLUMN relevance_note TEXT;

COMMIT;
