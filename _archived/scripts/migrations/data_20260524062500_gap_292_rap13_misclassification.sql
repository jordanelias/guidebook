-- data_20260524062500_gap_292_rap13_misclassification.sql
-- Materialize GAP-292 (logged during B.11 batch 1 backward mining via db.py add-gap)
-- as a data migration so the migration-reproducibility check (GAP-290 enforcement) passes.
-- Lesson: `db.py add-gap` writes directly to DB; for replayability the gap must also exist
-- as a migration file. Future B.11 sessions should prefer writing gap-creation SQL directly
-- in the same batch migration rather than splitting CLI writes from migration files.
-- Forward-only; idempotent via INSERT OR REPLACE on the primary key.

BEGIN TRANSACTION;

INSERT OR REPLACE INTO gaps (
    gap_id, category, priority, status, skill, section, description,
    created_at, created_by_session, updated_at, updated_by_session,
    falsification_condition, confidence_interval, shift_conditions, named_dissenter
) VALUES (
    'GAP-292',
    'CD',
    'P2',
    'OPEN',
    NULL,
    NULL,
    'REF-00571 (Kotloski 2020, ''Genetic Background Influences Acute Response to TBI in Kindling-Susceptible, Kindling-Resistant, and Outbred Rats'', DOI 10.3389/fneur.2019.01286) is linked to slug ''room-acoustic-performance'' as RAP-13 but is a rat-kindling TBI/seizure-genetics paper unrelated to acoustic performance. Probable misclassification at ingest. Surfaced during B.11 backward-mining batch 1, session 2026-05-23. Owner action: reclassify slug link (likely belongs under epilepsy/seizure-safety) or retire the source_slug_links row.',
    '2026-05-24 06:25',
    'session_2026-05-23-bpc-rewrite-phase-b-closure',
    '2026-05-24 06:25',
    'session_2026-05-23-bpc-rewrite-phase-b-closure',
    NULL, NULL, NULL, NULL
);

COMMIT;
