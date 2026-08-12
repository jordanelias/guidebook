-- data_20260524200000_gap_293_db_py_codeorder_fix.sql
-- Materialize GAP-293 (db.py code-ordering bug fix surfaced during B.11 batch 2 closure).
-- Inserted via db.py add-gap → needs paired migration for reproducibility.

BEGIN TRANSACTION;

INSERT OR REPLACE INTO gaps (
    gap_id, category, priority, status, skill, section, description,
    created_at, created_by_session, updated_at, updated_by_session,
    falsification_condition, confidence_interval, shift_conditions, named_dissenter
) VALUES (
    'GAP-293',
    'CD',
    'P3',
    'OPEN',
    NULL,
    NULL,
    'scripts/db.py had a code-ordering bug: `if __name__ == "__main__": main()` block was placed at line 1099, BEFORE the definitions of update_bpc_metadata, insert_evidence_source, insert_source_slug_link, and get_unmined_for_all_slugs (all defined at lines 1107-1183). update-bpc invocation hit NameError because main() reached the dispatch case before those functions were loaded. Fixed in this session by relocating the __main__ block to the actual end of file. Surfaced when B.11 batch 2 closure tried to set citation_mining_complete=1 for room-acoustic-performance.',
    '2026-05-24 19:47',
    'session_2026-05-23-bpc-rewrite-phase-b-closure',
    '2026-05-24 19:47',
    'session_2026-05-23-bpc-rewrite-phase-b-closure',
    NULL, NULL, NULL, NULL
);

COMMIT;
