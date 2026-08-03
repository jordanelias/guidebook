-- data_20260523001500_excise_40_retired.sql
-- Per owner directive 2026-05-22: excise the 40 UNVERIFIED-CLOSED rows entirely.
--
-- Impact:
--   evidence_sources: -40 rows (678 -> 638)
--   source_slug_links: -40 rows (one slug citation per retired ref)
--   evidence_source_authors: -25 rows (author rosters populated before retirement decision)
--   Total child rows cascade-deleted: 65
--
-- After excision: 638 rows, all eligible (100% eligibility rate in remaining corpus).
--
-- BPC reasoning doc markdown still contains the textual citation references for these
-- retired ref-ids; those references will become dangling pointers in the doc layer.
-- That cleanup is separate work — this migration only operates on the data layer.

BEGIN TRANSACTION;

-- Child-table deletes first (FKs declared NO ACTION, but defensive ordering for safety)
DELETE FROM evidence_source_authors WHERE ref_id IN (
    'REF-00001','REF-00024','REF-00031','REF-00052','REF-00093','REF-00106','REF-00133',
    'REF-00139','REF-00181','REF-00182','REF-00183','REF-00184','REF-00185','REF-00186',
    'REF-00218','REF-00221','REF-00232','REF-00243','REF-00253','REF-00257','REF-00273',
    'REF-00369','REF-00370','REF-00372','REF-00382','REF-00483','REF-00504','REF-00513',
    'REF-00514','REF-00521','REF-00529','REF-00543','REF-00594','REF-00595','REF-00596',
    'REF-00625','REF-00629','REF-00634','REF-00635','REF-00733'
);

DELETE FROM source_slug_links WHERE ref_id IN (
    'REF-00001','REF-00024','REF-00031','REF-00052','REF-00093','REF-00106','REF-00133',
    'REF-00139','REF-00181','REF-00182','REF-00183','REF-00184','REF-00185','REF-00186',
    'REF-00218','REF-00221','REF-00232','REF-00243','REF-00253','REF-00257','REF-00273',
    'REF-00369','REF-00370','REF-00372','REF-00382','REF-00483','REF-00504','REF-00513',
    'REF-00514','REF-00521','REF-00529','REF-00543','REF-00594','REF-00595','REF-00596',
    'REF-00625','REF-00629','REF-00634','REF-00635','REF-00733'
);

-- Parent-table delete
DELETE FROM evidence_sources WHERE ref_id IN (
    'REF-00001','REF-00024','REF-00031','REF-00052','REF-00093','REF-00106','REF-00133',
    'REF-00139','REF-00181','REF-00182','REF-00183','REF-00184','REF-00185','REF-00186',
    'REF-00218','REF-00221','REF-00232','REF-00243','REF-00253','REF-00257','REF-00273',
    'REF-00369','REF-00370','REF-00372','REF-00382','REF-00483','REF-00504','REF-00513',
    'REF-00514','REF-00521','REF-00529','REF-00543','REF-00594','REF-00595','REF-00596',
    'REF-00625','REF-00629','REF-00634','REF-00635','REF-00733'
);

COMMIT;
