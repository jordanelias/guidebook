-- 064_item_provenance_reads_the_view.sql
-- SCHEMA migration — finish the M5 author sweep. `v_item_provenance` was missed.
--
-- THIS IS A SWEEP FAILURE, AND THE FOURTH OF THE DAY. Migration 063 writer-retired the
-- five author copies on `evidence_sources` and redirected eight Python readers and six
-- skills to `v_evidence_authors`. It did not redirect THIS VIEW, which selects
-- `es.author_display` — a column that now reads NULL on every row.
--
-- The read-only audit that scoped M5 named this view FIRST, in its own words:
--     "change `v_item_provenance` ... to derive `author_display` via GROUP_CONCAT over
--      evidence_source_authors ordered by position; sweep the four named readers"
-- I swept the readers and built a better derivation than the one suggested, and then
-- missed the object the instruction opened with. CLAUDE.md §0.4: a rename or removal is
-- not done until the callers are swept, and a sweep that stops at the filename is not a
-- sweep. A view is a caller.
--
-- WHY IT WAS INVISIBLE, which is the part worth carrying forward. My completeness proof
-- for 063 was that regenerating every derived output changed nothing but the schema-version
-- stamp. That proof was sound for what it covered and blind here: `specifications` holds
-- 0 rows, so `v_item_provenance` returns 0 rows, so it appears in no rendered output and
-- in no check's subject. AN EMPTY SCOPE HID A REAL DEFECT FROM A BYTE-EXACT RENDER DIFF.
-- The same day's instrumentation work found 26 checks passing over empty scopes; this is
-- the same shape one layer down, and the reason a grep for the retired column names is
-- not optional even when the rendered output is provably identical.
--
-- No data is read here. DROP VIEW / CREATE VIEW stores a query, not a result, so this
-- replays correctly ahead of every data migration.

DROP VIEW IF EXISTS v_item_provenance;

CREATE VIEW v_item_provenance AS
SELECT
    i.item_code,
    i.name                      AS item_name,
    i.category                  AS item_category,
    ecs.specification_id,
    ecs.population_code,
    ecs.state                   AS cell_state,
    ecs.tier_basis,
    ecs.regulatory_stratum_only,
    csl.role                    AS source_role,
    es.ref_id,
    es.pub_title,
    -- POINTER, NOT COPY (migration 063). Was `es.author_display`, a writer-retired
    -- tombstone reading NULL. The authors have one home, evidence_source_authors, and
    -- v_evidence_authors renders it.
    va.author_display,
    es.pub_year,
    es.tier                     AS source_tier,
    es.evidence_type,
    es.verification_status,
    es.jurisdiction
FROM items i
JOIN "specifications" ecs ON ecs.item_code = i.item_code
JOIN "specification_source_links"   csl ON csl.specification_id   = ecs.specification_id
JOIN evidence_sources    es  ON es.ref_id     = csl.ref_id
LEFT JOIN v_evidence_authors va ON va.ref_id = es.ref_id;

PRAGMA user_version = 64;
