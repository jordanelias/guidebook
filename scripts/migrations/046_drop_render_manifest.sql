-- 046_drop_render_manifest.sql
-- SCHEMA migration — remove a table added hours earlier on a premise that
-- turned out to be wrong.
--
-- Migration 045 created `render_manifest` to record per-page static build
-- events: which item produced which HTML file, against which DB state, from
-- which cells and sources. That design assumed the site's last hop is a
-- build step producing durable per-page artifacts.
--
-- The owner then stated the target architecture: "the entire pipeline is
-- dynamic rendering on site", and separately, "do not rely on artifacts for
-- rendering the site". Under dynamic rendering there is no per-page build
-- event to record. A manifest of build events is not a weaker version of the
-- right table; it is a record of something that will not happen.
--
-- The owner has chosen static build now, dynamic later — so per-page HTML
-- continues to be generated as a stopgap. That does not rescue this table:
-- `scripts/generate/build_site.py` answers "is this page stale?" by comparing
-- the file on disk against a fresh render, which needs no stored manifest and
-- keeps working unchanged when the static stopgap is retired.
--
-- THE PRECEDENT THIS FOLLOWS, AND THE ONE IT REPEATS
-- Migration 043 dropped `building_typologies`, created a day earlier by 042
-- with zero rows and zero references, and its header says why: a table added
-- on speculation about future need. 045 cited 043 as a lesson and then made
-- the same mistake within the day — schema written ahead of a decided
-- architecture, justified by a story about what would probably be needed.
-- Recorded here rather than quietly reverted, because the pattern is more
-- useful to a future session than the table would have been.
--
-- No data is lost: render_manifest was never populated. The build driver in
-- scripts/generate/build_site.py is retained — it is the missing build-all
-- driver, which was a real gap independent of the manifest.
--
-- Forward-only; user_version -> 46.

DROP INDEX IF EXISTS idx_render_manifest_item;
DROP INDEX IF EXISTS idx_render_manifest_fingerprint;
DROP TABLE IF EXISTS render_manifest;
