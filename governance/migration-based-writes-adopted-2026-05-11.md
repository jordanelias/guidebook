# Migration-based DB writes — adopted

**Filed:** 2026-05-11 (session_2026-05-11g-citation-mining.md)
**Resolves:** GAP-290 (P1, AUDT) — concurrent-write architecture
**Status:** Adopted

## Decision

The project moves to **Option B (migration-based schema)** from `governance/concurrent-write-architecture-proposal-2026-05-11.md`. Data writes to `data/guidebook.db` now flow through versioned, immutable migration files that git merges cleanly when concurrent sessions emit them.

## Why this option

- **Option A (lock file)** doesn't allow concurrent sessions, it serializes them. User asked for clean concurrency.
- **Option C (hosted DB)** would allow concurrency but requires infrastructure decisions (provider, credentials, billing, ops). Owner-scope, not session-scope.
- **Option B (migration-based)** is the answer that fits the request: two sessions writing independent data migrations both land cleanly on `main` via git's text-merge.

The project already had Option B infrastructure for **schema** migrations (`scripts/migrate_db.py` + `scripts/migrations/NNN_*.sql`, tracked via `PRAGMA user_version`). This session extends it to **data** migrations.

## What shipped

| Artifact | Path | Role |
|---|---|---|
| Schema migration | `scripts/migrations/007_data_migrations_table.sql` | Adds `data_migrations` tracking table |
| Schema migration | `scripts/migrations/008_evidence_population_match.sql` | Captures table from adversarial-research protocol that had no migration |
| Schema migration | `scripts/migrations/009_adversarial_research_columns.sql` | Captures 7 columns from adversarial-research protocol that had no migration |
| Bootstrap data migration | `scripts/migrations/data_20260511000000_2026-05-11g-citation-mining.sql` | Snapshots current production data state as baseline |
| Extended runner | `scripts/migrate_db.py` | Now applies both schema and data migrations; `--rebuild` recreates DB from scratch |
| Emit helper | `scripts/emit_data_migration.py` | Generates timestamped data-migration files from SQL or stdin |
| CI check | `.github/workflows/audit.yml` | Migration-reproducibility step rebuilds DB from history and diffs against committed binary |

## How sessions write to the DB now

### Old way (DEPRECATED, causes GAP-290 clobbers)

```bash
python3 scripts/db.py add-source --tier 2 --year 2021 ...
# This wrote directly to data/guidebook.db. Concurrent sessions clobbered each other.
```

### New way (concurrent-safe)

```bash
# Build SQL for what you want to do (any number of operations)
cat > /tmp/my_changes.sql <<'SQL'
INSERT INTO evidence_sources (ref_id, tier, ...) VALUES ('REF-00999', 2, ...);
INSERT INTO source_slug_links (slug, local_ref_id, ref_id, ...) VALUES (...);
SQL

# Emit the migration file (gets a unique timestamp)
python3 scripts/emit_data_migration.py \
    --session "session_2026-05-11h-my-work.md" \
    --summary "add REF-00999 from forward mining of REF-00710" \
    --input /tmp/my_changes.sql

# Output: scripts/migrations/data_20260511053900_2026-05-11h-my-work.sql

# Apply it to your local DB
python3 scripts/migrate_db.py --session "session_2026-05-11h-my-work.md"

# Commit BOTH the migration file AND the updated data/guidebook.db
git add scripts/migrations/data_20260511053900_*.sql data/guidebook.db
git commit -m "session-name: action [timestamp]"
```

Two sessions doing this in parallel get **different timestamps** in the migration filename and can both push to `main` without conflict. The git merge resolves cleanly because they're independent text files. When the next session pulls, it gets both migrations and applies any that aren't yet recorded in its local `data_migrations` table.

### Transition: existing `scripts/db.py` commands still work

The existing `db.py` helpers (`add-source`, `add-gap`, etc.) still write directly to the DB. They are unaffected by this change but expose the same clobber risk as before. **Sessions running in time windows where concurrent activity is possible should use the migration path instead.** Single-agent sessions on a quiet repo can continue using `db.py` if convenient — the CI reproducibility check (below) is forgiving for the bootstrap window.

A future cleanup pass should refactor `db.py` to emit migration files internally rather than writing to the DB directly, eliminating the legacy code path entirely.

## CI check explained

`.github/workflows/audit.yml` includes a **migration-reproducibility** step:

1. Apply every migration in order to build a fresh DB from scratch (`migrate_db.py --rebuild /tmp/rebuilt.db`)
2. Compare row counts and `user_version` against the committed `data/guidebook.db`
3. FAIL the build if they diverge

What this catches: a session that wrote to the DB directly (e.g., via `db.py add-source`) without also emitting a corresponding migration. The migration history would then no longer reproduce the committed DB. The check blocks the push and surfaces the diff.

What this doesn't catch: a session that emitted a migration but the migration content has a bug (e.g., the SQL references a non-existent slug). For those, the runner's FK-check pass at the end of each migration surfaces the problem when the migration is applied. Pre-existing FK drift in the production DB (~18 violations in the bootstrap snapshot, all from legacy `bpc_metadata` and `spec_value_probes` rows) is treated as warnings, not failures.

## Open follow-up

- Refactor `scripts/db.py` write-helpers to emit migrations rather than write the DB directly. Once that lands, the legacy clobber path is closed entirely and the CI check becomes hard-strict.
- Audit existing direct-DB writes for FK-drift fixes (the 18 violations in the bootstrap).
- Consider compaction strategy for the data_migrations directory once it grows large (e.g., periodic snapshots that consolidate prior history into a new bootstrap).

## Acceptance criteria — closing GAP-290

- ✓ Schema migration 007 ships the `data_migrations` table
- ✓ `scripts/migrate_db.py` applies both schema and data migrations
- ✓ `scripts/emit_data_migration.py` produces correctly-named, concurrency-safe migration files
- ✓ Bootstrap data migration captures current production state
- ✓ CI reproducibility check rebuilds DB from migrations and diffs against committed binary
- ✓ End-to-end test passes locally (rebuilt DB row-for-row matches production)
- ✓ Concurrent-emission test passes (two migrations with distinct timestamps both apply via one runner pass)

GAP-290 → CLOSED-FIXED.
