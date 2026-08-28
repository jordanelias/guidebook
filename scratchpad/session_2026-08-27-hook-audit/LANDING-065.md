# Landing migration 065 — state, proof, and the one blocked step

**Written 2026-08-28.** Everything below is measured, not recalled. The migration is
written and proven; the only thing outstanding is a permission.

## The blocked step

`python3 scripts/migrate_db.py` is refused by this session's permission classifier.
Canonical is untouched: `user_version 64`, sha256
`8507c4cf0a48e1568ca16e24de5e4a7dd3ac856c9acfba27f7975fda09acacec`.

`065` therefore waits at `065_seven_stage_names_and_four_lenses.sql.pending` in this
directory rather than in `scripts/migrations/`. That is not a workaround: that
directory's contract is *"forward-only and immutable once committed"*, and a
migration sitting there unapplied IS the divergence `migration_reproducibility`
exists to report. The gate was right; the file was in the wrong place.

## Resume sequence

```
git mv scratchpad/session_2026-08-27-hook-audit/065_*.sql.pending \
       scripts/migrations/065_seven_stage_names_and_four_lenses.sql
python3 scripts/migrate_db.py --session session_2026-08-27-hook-audit.md
python3 scratchpad/session_2026-08-27-hook-audit/build_065.py --declarations /tmp/decl
python3 scratchpad/session_2026-08-27-hook-audit/sweep_065.py --apply
bash scripts/regenerate_derived.sh
python3 scripts/run_checks.py --changed-from origin/main
python3 scripts/run_checks.py --selftest
```

Migration and sweep land in ONE commit. The sweep is only correct against the
migrated schema: applied on a version-64 database it turns 14 blocking checks red.

## What is proven

| | result |
|---|---|
| applies to a copy of canonical | clean · `foreign_key_check` clean · `integrity ok` · `user_version 65` |
| views | all 18 selectable |
| foreign keys | 80 → 125 |
| retired vocabulary | none left in any table or column name |
| `judgment_match_grades` | 25 of 25 carry `identity_code` |
| `base_item_taxonomy_links` | 530 rows, 372 identity + 158 icf, 0 null coalesce |
| `rename_insurance.py` | PASS, one waiver carrying its reason |
| rebuild-from-history vs direct-apply | table sets identical · **DDL byte-identical**, all 66 tables and 18 views · row differences: `base_pipeline_runs` only, already declared EXEMPT |
| rebuild WITH 065 vs WITHOUT, under the rename map | `base_taxonomy_medical` (the new empty table). Nothing else. |

## Why the caller sweep is believed complete

Not by reading. By a matched pair, run against two databases:

- `schema_reference_audit.py` **PASSES** against the migrated schema with the sweep applied.
- The same check **FAILS with 382 references to 44 names** against the current schema.

Neither result alone means anything. Together they say the callers name exactly the
post-rename schema and nothing else.

**The functional surface, enumerated and each part accounted for:**

| surface | how it is handled | verified |
|---|---|---|
| SQL regions in scripts, tools, skills, workflows | swept, 908 sites in 75 files | by the gate above |
| eight files holding a table-name list or map | swept by exact target list | diff read by hand |
| `MODEL_TABLE_MAP` in `validate_pydantic_schemas.py` | swept | 18 of 18 mapped tables covered |
| `governance/check-registry.yaml` | **no functional reference** — all 52 hits are prose in `note:`/`basis:` | measured 2026-08-28 |
| `governance/pipeline-map.yaml` | **nothing reads it** — the file says so itself, `readers_today: 0` | its own field |
| generated output (`site/`, `parts/`, `audits/`, `tools/*.html`) | regenerated, never swept | `regenerate_derived.sh` |
| prose, frozen records, `_archived/` | not callers | — |

## Things found on the way that are NOT this rename's, and are not fixed

1. **`scripts/generate/room_page.py`** queries four tables that have never existed
   (`room`, `room_item_population`, `room_dar_provision`, `room_conflict`; the live
   ones are `rooms` and `room_items`). Recorded 2026-08-02 as disposal flag 3 awaiting
   owner decision 8 on the room stratum — **still open 26 days later**. Exempted with
   that evidence, not fixed: fixing it decides what the room stratum IS (DG-NON).
2. **`skills/question-author_SKILL.md`** teaches
   `UPDATE specification SET question_heading WHERE spec_id`. Measured: the table does
   not exist, `spec_id` and `title` are not columns of `specifications`, and
   `question_heading` exists in **no table in the schema**. That skill's write path has
   never been runnable.
3. **`schemas/population.py` / `schemas/population_links.py`** carry retired vocabulary
   in their MODULE names, and under the four-lens change `population_links` no longer
   describes anything. Renaming Python modules means sweeping imports; queued, not done.
4. **`governance/pipeline-map.yaml`** — 900 lines, 196 table references, and by its own
   statement nothing reads it. CLAUDE.md §1 makes an unread artefact a deletion
   candidate, but it is reader-facing CONTENT, so `_archived/` and owner sign-off, not a
   cull. Queued.
5. **`record-command.py`** files Bash logs under `sessions/LATEST`, which names the
   PREVIOUS session for the whole life of the current one (§7 trap). Queued.

## Two gates were repaired because this rename found them blind

- `migration_reproducibility.py` hardcoded six table names and turned a missing table
  into a silent `skip`. Against the rename ALL SIX skipped while it printed
  `EXAMINED: 7`. Now derived: schema version plus `COUNT(*)` on every table either
  database has, absence is a MISMATCH. `EXAMINED` 7 → 65. Mutation-tested four ways.
- `rename_insurance.py` accepted the 60 new lens foreign keys without checking any of
  them — a build that made them plain TEXT would have passed green. Now declared edge
  by edge. Caught by mutation, not by reading.
