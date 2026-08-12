# Archived migration history — frozen 2026-08-12

**355 files**: 56 numbered schema migrations (`001`–`056`), 297 data migrations
(`data_20260511000000_*` through `data_20260812083254_*`), and two replay artifacts from the
2026-05-11 concurrent-write incident (`session_2026_05_11g_data.json`,
`session_2026_05_11g_replay.py`). Plus three mining scripts archived earlier, on 2026-08-03.

They mirror their origin path (`scripts/migrations/`), per the retire-here-don't-delete rule. They
are **frozen**: not edited, not renamed, not swept. Every one of them was true when it ran.

## What replaced them

`scripts/migrations/057_baseline_2026-08-12.sql` — one file holding the complete schema **and**
data as of 2026-08-12: 67 tables, 18 views, 77 indexes, 5,072 rows. The runner's baseline
convention (`discover_schema_migrations`) skips every schema migration numbered below the highest
baseline, and `BASELINE_DATA_CUTOFF_TS` in `scripts/migrate_db.py` was moved past the last archived
data migration, so nothing here is looked for.

Owner instruction, 2026-08-12: *"freeze and archive existing change history then compress change
history for fresh start."*

## Why

Replaying this history was the only proof that the committed database had not been hand-edited.
That property is kept — the baseline is still replayed and compared. What was shed is the cost:

1. **Immutable data migrations pinned retired names forever.** Renaming `evidence_cell_state` to
   `specifications` collided with 19 of these files and required a new ordering mechanism
   (`AFTER_DATA`, schema 056) purely to work around replay. `DR-2026-08-12-specification-rename-and-replay-order`
   named a full baseline as the larger answer and deferred it to the owner; this is that decision
   taken.
2. **Most of what replayed no longer existed.** The 2026-08-06 clean-room reset and the 2026-08-12
   evidence-stage clearance emptied the evidence, source, gap, connection and specification tables.
   297 data migrations ran to insert rows that a later migration deleted.
3. **Test fixtures were reconstructing schema by scanning these files for literal table names.**
   That selector had to match immutable historical text, so a rename sweep rewrote it and the
   fixture silently built the wrong schema. Both fixtures now read the baseline
   (`scripts/tests/_baseline_ddl.py`) and the hand-copied rename replay is gone.

The corpus was at its smallest at the moment of the freeze — 5,072 rows, ~91% controlled vocabulary
(`term_aliases`, `source_locators`, `populations`, `items`, `axes`) — which is the cheapest this
operation will ever be.

## What was preserved rather than discarded

- **The 319-row `data_migrations` ledger is baked into the baseline**, so every historical
  `migration_id`, timestamp and content hash is still queryable from the database itself.
- **These files remain readable here**, at their origin-mirroring path.
- `db_meta`, the 158-row `decisions` table and every vocabulary table carry over intact.

## Reading this directory

`_archived/**` is hidden from ripgrep by the root `.ignore` (see
`DR-2026-08-06-cold-storage-search-scope`). `ls`, `Glob`, `git grep` and every Python tool in the
repo see it normally. To search it, name the path explicitly.

**Do not restore a file from here into `scripts/migrations/`.** Its effect is already contained in
the baseline; replaying it would apply that effect twice. `BASELINE_DATA_CUTOFF_TS` guards the data
migrations against exactly that mistake, but the numbered schema migrations have no such guard
beyond the baseline-supersedes rule.

## Provenance

- Prior baseline: `012_baseline_2026-05-15.sql` (superseded 001–011; itself archived here now).
- Decision: `decisions/DR-2026-08-12-migration-history-baseline.md`, register row **D-0159**.
- Reproducibility verified before the freeze: applied to an empty database the baseline yields, against
  the pre-baseline committed DB, **0** `sqlite_master` object differences either direction (name,
  type and SQL text), **0** row-count divergences across all 67 tables, **0** content divergences
  compared row-by-row including `rowid`, `PRAGMA foreign_key_check` empty, `PRAGMA integrity_check`
  ok, and all 18 views executing.
