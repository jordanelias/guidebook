-- 045_render_manifest.sql
-- SCHEMA migration — give hop 10 (cell/item → rendered page) an edge object.
--
-- THE PROBLEM THIS SOLVES
-- The walk from a research topic to a rendered page has nine hops recorded in
-- tables and a tenth recorded nowhere. Nothing in the database knows that
-- site/specs/e-08.html exists, which item it came from, which DB state it was
-- built against, or which cells and sources it consumed. A page is therefore
-- not a node: you can walk topic → source → cell, and then the trail stops one
-- step short of the only surface a reader ever sees.
--
-- WHAT ALREADY EXISTED, AND WHY IT IS NOT ENOUGH
-- This is not a wholly new idea in this repo, and the earlier version deserves
-- credit rather than replacement-by-default. scripts/generate_parts.py:83 and
-- :134 already compute a DB fingerprint and write a manifest for parts/, with
-- an explicit idempotence contract ("identical fingerprint ⇒ identical
-- output"). Two things stop that pattern from carrying the walk:
--
--   1. It covers parts/ only; site/ has no equivalent, and no build driver.
--   2. It is prose in a markdown file. You cannot join it. "Which sources
--      justify this page?" and "which pages does REF-00338 reach?" are the
--      questions hop 10 exists to answer, and a manifest you cannot query
--      answers neither.
--
-- So: the same idea, in rows. db_fingerprint below deliberately uses the same
-- shape as generate_parts.py's so the two surfaces agree on what "the DB state"
-- means.
--
-- A KNOWN WEAKNESS, STATED RATHER THAN INHERITED SILENTLY
-- That fingerprint hashes table COUNTS plus user_version. It therefore cannot
-- see an UPDATE — the identical blindness that makes the blocking
-- migration_reproducibility gate pass while 845 enrichment cells diverge. It is
-- retained for continuity with parts/, but it is NOT the provenance record.
-- inputs_json is: it names the exact cell_ids and ref_ids the page consumed, so
-- a claim on a page can be traced to the rows that justified it even when the
-- fingerprint is unchanged.
--
-- WHY THIS MATTERS MORE IF THE SITE IS NOT STORED
-- Per the owner directive of 2026-08-04 ("do not rely on artifacts for
-- rendering the site"), the rendered output may not live in an expiring CI
-- artifact. Whether it is committed or regenerated on demand is still an open
-- decision — but under either answer, this table is what lets anyone establish
-- that a given render corresponds to a given database state. If the bytes are
-- not kept, the attestation that they were produced from these inputs is the
-- only durable record.
--
-- TIMESTAMPS
-- rendered_at carries NO `DEFAULT (datetime('now'))`. That default is why a
-- rebuilt database can never be byte-compared against the committed one; the
-- driver passes an explicit value. Same discipline as migration 044.
--
-- Forward-only; user_version -> 45.

CREATE TABLE IF NOT EXISTS render_manifest (
  page_path           TEXT PRIMARY KEY,
  item_code           TEXT REFERENCES items(item_code),
  population_code     TEXT REFERENCES populations(population_code),
  generator           TEXT NOT NULL,
  generator_version   TEXT NOT NULL,
  db_fingerprint      TEXT NOT NULL,
  db_user_version     INTEGER NOT NULL,
  inputs_json         TEXT NOT NULL DEFAULT '{}',
  output_sha256       TEXT,
  output_bytes        INTEGER,
  rendered_at         TEXT NOT NULL,
  rendered_by_session TEXT
);

-- The reverse walk: "which pages did this item produce?" A spec item today
-- yields one page, but populations and rooms will yield many, and the manifest
-- should not assume otherwise.
CREATE INDEX IF NOT EXISTS idx_render_manifest_item ON render_manifest(item_code);

-- Freshness queries filter on DB state before they filter on anything else.
CREATE INDEX IF NOT EXISTS idx_render_manifest_fingerprint
  ON render_manifest(db_fingerprint);
