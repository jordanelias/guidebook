-- 047_provenance_views.sql
-- SCHEMA migration — make the walk queryable in both directions.
--
-- The project's stated goal is that any published best practice can be walked
-- back to the sources, populations and doctrine behind it, and that any source
-- can be followed forward to everything it touches. Until migration 044 the
-- cell→source edge was an unindexed JSON array and neither direction was a
-- join. It is now an edge object, and these views are what turn that edge into
-- an answerable question.
--
-- Measured before writing: of the 13 views already in this database, NOT ONE
-- touches evidence_sources or cell_source_links. Nothing here duplicates
-- existing work; the walk has simply never been expressible in SQL.
--
-- WHY ITEM-CENTRIC AND NOT PAGE-CENTRIC
-- An earlier design keyed the forward view on rendered page paths, joined
-- through a render_manifest table. That table is gone (migration 046) because
-- the target architecture is dynamic rendering, under which a "page" is a
-- route resolved at request time rather than a file that was built. Keying
-- provenance to item_code instead makes these views correct under both the
-- current static stopgap and the dynamic destination: the render layer maps an
-- item to a URL however it likes, and the provenance answer does not move.
--
-- WHY VIEWS AND NOT TABLES
-- The chain is a fixed shallow DAG -- at most six joins over 93 items, 15
-- cells and 863 sources. There is nothing here to materialise for
-- performance, and a materialised copy would be a second thing to keep in
-- sync. The canonical edge (cell_source_links) is a table because it records a
-- human synthesis judgement and must be FK-checkable; the composition of that
-- edge is derivable, so it is schema rather than data. That split also keeps
-- the reproducibility contract clean: edges rebuild from migrations, views
-- rebuild from this file.
--
-- These views read cell_source_links, never evidence_cell_state.governing_refs.
-- The JSON column still exists and is still written, but it is the legacy
-- copy; anything new that reads it re-creates the problem 044 solved.
--
-- Forward-only; user_version -> 47.

-- ── Forward: what justifies this specification? ─────────────────────────────
-- item → cell → governing source, with everything a reader needs to judge the
-- claim: the cell's state and tier basis, the source's tier and verification
-- standing. One row per (item, population, source).
CREATE VIEW IF NOT EXISTS v_item_provenance AS
SELECT
    i.item_code,
    i.name                      AS item_name,
    i.category                  AS item_category,
    ecs.cell_id,
    ecs.population_code,
    ecs.state                   AS cell_state,
    ecs.tier_basis,
    ecs.regulatory_stratum_only,
    csl.role                    AS source_role,
    es.ref_id,
    es.pub_title,
    es.author_display,
    es.pub_year,
    es.tier                     AS source_tier,
    es.evidence_type,
    es.verification_status,
    es.jurisdiction
FROM items i
JOIN evidence_cell_state ecs ON ecs.item_code = i.item_code
JOIN cell_source_links   csl ON csl.cell_id   = ecs.cell_id
JOIN evidence_sources    es  ON es.ref_id     = csl.ref_id;

-- ── Reverse: what does this source reach? ───────────────────────────────────
-- source → cell → item, plus the research topics the source was admitted
-- under. Answers "if this source turns out to be wrong, what has to be
-- revisited?" -- which is the question the DISPUTED sweep of 2026-07-20 had to
-- answer by hand.
CREATE VIEW IF NOT EXISTS v_source_reach AS
SELECT
    es.ref_id,
    es.pub_title,
    es.tier                     AS source_tier,
    es.verification_status,
    ecs.cell_id,
    ecs.item_code,
    i.name                      AS item_name,
    ecs.population_code,
    ecs.state                   AS cell_state,
    (SELECT GROUP_CONCAT(ssl.slug, '; ')
       FROM source_slug_links ssl
      WHERE ssl.ref_id = es.ref_id)  AS admitted_under_slugs
FROM evidence_sources es
JOIN cell_source_links   csl ON csl.ref_id  = es.ref_id
JOIN evidence_cell_state ecs ON ecs.cell_id = csl.cell_id
JOIN items i                 ON i.item_code = ecs.item_code;

-- ── Population ancestry: NOT added, deliberately ───────────────────────────
-- A recursive-CTE view over populations.parent_code was drafted here and
-- removed before this migration was committed. The column exists and the model
-- documents the relationship, but measured against the live data: 23
-- populations, ZERO with a non-null parent_code. The view was correct and
-- returned nothing.
--
-- Migration 046, written the same hour, drops a table added ahead of a decided
-- need. Shipping a view over an unpopulated relationship in the next migration
-- would be the same mistake wearing a cheaper costume -- and "it costs nothing
-- and might be useful later" is precisely the reasoning 043 and 046 exist to
-- refuse. It is one statement to add on the day a population acquires a parent.
