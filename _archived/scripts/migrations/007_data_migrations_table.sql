-- 007_data_migrations_table.sql
-- GAP-290 P1 — concurrent-write architecture, Option B (migration-based data writes)
-- Decision record: governance/concurrent-write-architecture-proposal-2026-05-11.md
-- Adopted: 2026-05-11 in session_2026-05-11g-citation-mining.md
-- schema_version → 7

-- ============================================================
-- data_migrations
--
-- Tracks which data-migration files have been applied to this DB.
-- Schema migrations (numbered 001..NNN_*.sql) are tracked via PRAGMA user_version.
-- Data migrations (named data_{YYYYMMDDHHMMSS}_{session}.sql) are tracked here
-- because there's no monotonic ordering between two sessions producing concurrent
-- data migrations — both must be applied, and the order is determined by the
-- timestamp embedded in the filename rather than by a global counter.
--
-- A migration is applied iff its migration_id is present here. The runner
-- skips already-applied migrations. content_sha lets a future tool detect if
-- a migration file was modified after being applied (a forbidden operation —
-- migrations are forward-only and immutable once committed).
-- ============================================================

CREATE TABLE data_migrations (
    migration_id        TEXT PRIMARY KEY,        -- e.g. "data_20260511053900_2026-05-11g-citation-mining"
    applied_at          TEXT NOT NULL,           -- ISO 8601 UTC
    content_sha         TEXT NOT NULL,           -- SHA-256 hex of the migration file body when applied
    applied_by_session  TEXT,                    -- which session ran the runner; NULL for batch reconstructions
    notes               TEXT
);

CREATE INDEX idx_data_migrations_applied_at ON data_migrations(applied_at);
