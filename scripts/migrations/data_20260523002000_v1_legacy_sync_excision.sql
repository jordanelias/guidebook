-- data_20260523002000_v1_legacy_sync_excision.sql
-- Mirror the 40-row excision in evidence_sources_v1_legacy to restore C05/D02 parity.
-- Follows the established v1_legacy-sync pattern from prior migrations.

BEGIN TRANSACTION;

DELETE FROM evidence_sources_v1_legacy WHERE ref_id IN (
    'REF-00001','REF-00024','REF-00031','REF-00052','REF-00093','REF-00106','REF-00133',
    'REF-00139','REF-00181','REF-00182','REF-00183','REF-00184','REF-00185','REF-00186',
    'REF-00218','REF-00221','REF-00232','REF-00243','REF-00253','REF-00257','REF-00273',
    'REF-00369','REF-00370','REF-00372','REF-00382','REF-00483','REF-00504','REF-00513',
    'REF-00514','REF-00521','REF-00529','REF-00543','REF-00594','REF-00595','REF-00596',
    'REF-00625','REF-00629','REF-00634','REF-00635','REF-00733'
);

COMMIT;
