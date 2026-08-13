-- 048_source_reach_includes_the_unreached.sql
-- SCHEMA migration — fix a view that answered its own question with silence.
--
-- `v_source_reach` (migration 047, one migration ago) inner-joins
-- evidence_sources through cell_source_links. Its header claims it answers
-- "if this source turns out to be wrong, what has to be revisited?" -- the
-- question the DR-2026-07-20 correctness sweep had to answer by hand.
--
-- Measured against the live corpus: 57 of 863 sources appear. **806 are
-- invisible by construction**, and among the invisible are **all 7 DISPUTED
-- sources** -- the precise population the sweep was about. Asked what a
-- disputed source reaches, the view returns no rows, which is
-- indistinguishable from "that ref_id is not in the corpus". A provenance tool
-- that cannot distinguish "reaches nothing" from "does not exist" is worse
-- than no tool, because it looks like an answer.
--
-- This is the inner-join blindness that adversarial review is for. The
-- original view is retained unchanged -- it is correct for the traversal it
-- performs, and callers wanting only reached sources should not pay for the
-- outer join -- and a companion is added that is honest about the empty case.
--
-- `v_source_reach_all` keeps one row per source that reaches nothing, with
-- NULL item/cell columns and an explicit `reaches` flag, so the difference
-- between "no rows" (unknown ref) and "one row, reaches=0" (known, reaches
-- nothing) is legible without the caller knowing the corpus.
--
-- Forward-only; user_version -> 48.

CREATE VIEW IF NOT EXISTS v_source_reach_all AS
SELECT
    es.ref_id,
    es.pub_title,
    es.tier                     AS source_tier,
    es.verification_status,
    CASE WHEN ecs.cell_id IS NULL THEN 0 ELSE 1 END AS reaches,
    ecs.cell_id,
    ecs.item_code,
    i.name                      AS item_name,
    ecs.population_code,
    ecs.state                   AS cell_state,
    (SELECT GROUP_CONCAT(ssl.slug, '; ')
       FROM source_slug_links ssl
      WHERE ssl.ref_id = es.ref_id)  AS admitted_under_slugs
FROM evidence_sources es
LEFT JOIN cell_source_links   csl ON csl.ref_id  = es.ref_id
LEFT JOIN evidence_cell_state ecs ON ecs.cell_id = csl.cell_id
LEFT JOIN items i                 ON i.item_code = ecs.item_code;
