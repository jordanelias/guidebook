-- DATA migration — empty the five author copies on evidence_sources.
--
-- Pairs with schema migration 063, which created v_evidence_authors. The copies are
-- writer-retired: after the code sweep of 2026-08-24 nothing in the repository writes
-- them, and every reader goes to the view. What remains is to stop them holding values
-- that will now silently age.
--
-- WHY NULL AND NOT DROP. Committed data migrations INSERT these columns, and migrations
-- are append-only and replay from the baseline (CLAUDE.md §0.3). Dropping a column an
-- earlier migration writes breaks the rebuild that CI compares against. They stay as
-- tombstones.
--
-- WHY NULL AT ALL, RATHER THAN LEAVING THEM. A stale value is worse than an absent one:
-- it reads as an answer. These five were LAST correct on 2026-08-19 and cannot be kept
-- correct — `resolve_dois.py` replaces every author row on enrichment and, until today,
-- refreshed none of these. Left populated, the next reader to reach for the familiar
-- column name gets a confident wrong byline; emptied, they get nothing and go to the view.
--
-- NOT RETIRED, AND DELIBERATELY UNTOUCHED:
--   author_count_is_complete — a curation assertion (was the WHOLE list obtained?).
--                              The rows cannot answer it; counting them only says how
--                              many were stored, not whether any are missing.
--   author_display_note      — prose standing in where no name exists, e.g. the
--                              2026-08-19 fabrication corrections. Not derivable, and
--                              the vetting surface renders it when there is no name.
--
-- VERIFIED BEFORE WRITING: v_evidence_authors reproduces all five columns EXACTLY on all
-- 10 live sources — author_display byte for byte, including its first-initial-only form.
-- Nothing is lost by emptying them.

UPDATE evidence_sources
   SET author_display       = NULL,
       first_author_last    = NULL,
       first_author_first   = NULL,
       author_count         = NULL,
       is_corporate_primary = NULL
 WHERE author_display       IS NOT NULL
    OR first_author_last    IS NOT NULL
    OR first_author_first   IS NOT NULL
    OR author_count         IS NOT NULL
    OR is_corporate_primary IS NOT NULL;
