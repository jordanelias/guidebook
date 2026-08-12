-- 051_admission_provenance_view.sql
-- SCHEMA migration — give `search_admissions` its reader, and correct two
-- claims migration 050 made yesterday-hour that the DB does not support.
--
-- ── PART 1: THE VIEW 050 SHOULD HAVE SHIPPED ───────────────────────────────
-- 050's header states the reverse walk twice as "the point" — "which search
-- found REF-00891?" — and builds an index for it. It then shipped no query
-- path that performs it. Nothing in the repo SELECTs `search_admissions`; the
-- only reader is the parity check that guards it. By migration 047's own
-- standard ("these views are what turn that edge into an answerable
-- question"), the edge was inert on arrival.
--
-- `v_source_admission` is that path. It is the missing half of 047:
-- `v_source_reach` walks a source FORWARD to the pages it justifies;
-- this walks the same source BACKWARD to the logged search that admitted it,
-- with the verbatim query text. Together they answer, for one ref_id, "where
-- did this come from and what does it hold up?" — which is the whole fork
-- goal stated as a single query.
--
-- `admitted_under_slugs` in `v_source_reach` answers a weaker version of the
-- backward question from `source_slug_links`: it names the TOPIC the source
-- belongs to, not the SEARCH that found it. That is hop 3; this is finer.
--
-- ── PART 2: TWO CORRECTIONS TO 050'S HEADER ────────────────────────────────
-- Migration 046 recorded 045's mistake in its own header rather than editing
-- 045 to look prescient. Same discipline here — 050 is committed and stays as
-- written. Both claims were caught by an adversarial review and re-derived
-- against the live DB before being recorded here.
--
-- C1. 050:19-21 — "every edge on the walk from a research question to a
-- rendered specification is a row with a foreign key." FALSE, and contradicted
-- by the ladder in the same commit. Hop 6 (BPC → reasoning doc) is still a
-- filename convention. Hop 4 (`source_value_extractions` → item) has no item
-- edge at all. Hop 7 runs on the legacy scalar `items.bpc_source_slug` with
-- `item_bpc_links` populated at 3%. Three edge objects short of the claim.
--
-- C2. 050:20-21 — "the last JSON-array-as-edge in that path." FALSE.
-- `citation_mining.connections_produced` is still one, and citation mining is
-- a discovery channel exactly like a logged search.
--
-- But it is NOT the same shape, and normalising it is NOT the same one-line
-- json_each. Measured across its 183 rows:
--   * 25 rows carry a non-empty value; 13 of those hold a BARE INTEGER
--     (`1`, `0`, `5`) — a COUNT, in a column whose other rows hold a LIST.
--   * of the 81 array entries: 15 are global `REF-#####` ids, 50 are
--     slug-scoped `local_ref_id` values resolvable only via
--     `source_slug_links(slug, local_ref_id)`, and 3 resolve to nothing
--     (CCD-12 for `accessible-design-economics-cost-premium`; MHB-35 and
--     MHB-36 for `sensory-space-global-south`).
-- Three vocabularies and two cardinalities in one column. It cannot be
-- foreign-keyed until a decision says what the column means, and the three
-- unresolvable ids are a data finding in their own right. Recorded here so the
-- next person meets the real problem instead of the easy one.
--
-- No view is added for it. That is 043's lesson: an edge object over a column
-- whose vocabulary is undecided would harden the ambiguity into a schema.
--
-- Forward-only; user_version -> 51. Views only — no table, no data.

-- ── Backward: which logged search admitted this source? ────────────────────
-- One row per (source, admitting search). A source with no row here was
-- admitted before the search-execution substrate (DR-2026-07-24) and its
-- provenance was never logged — 824 of 863 today. That absence is a fact
-- about the record, not about the source, and this view represents it by
-- omission rather than by a NULL-filled row that would read as a search.
CREATE VIEW IF NOT EXISTS v_source_admission AS
SELECT
    es.ref_id,
    es.pub_title,
    es.tier                     AS source_tier,
    es.evidence_type,
    es.verification_status,
    es.verification_disposition,
    se.exec_id,
    se.slug                     AS admitted_under_slug,
    se.query_text,
    se.engine,
    se.language,
    se.jurisdiction             AS search_jurisdiction,
    se.depth_method,
    se.mining_direction,
    se.target_tier,
    se.backfill                 AS search_was_backfilled,
    se.session                  AS admitting_session,
    se.executed_at              AS admitted_at
FROM evidence_sources es
JOIN search_admissions sa ON sa.ref_id  = es.ref_id
JOIN search_executions se ON se.exec_id = sa.exec_id;
