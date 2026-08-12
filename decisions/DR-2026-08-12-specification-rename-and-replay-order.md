# DR-2026-08-12 — Rename the (item × population) determination to `specification`, and make migration replay order faithful

**Status:** OPERATIVE — 2026-08-12.
**Decision by:** Owner directive 2026-08-12 ("product cell as (item x population) is confusing
terminology. rename to specification").
**Category:** D-SCHEMA. **Delegation:** DG-NON — the naming is owner-directed and recorded here;
the mechanism is captured, not originated.
**Amends:** `data/guidebook.db` (schema version 055/056), `scripts/migrate_db.py`,
`governance/pipeline-operations.md`, `governance/retired-vocabulary.yaml`, and the live surfaces
that named the old tables.
**Closes:** the terminology collision between "cell" and the Specification layer that
`armature_v4_resolutions.md` already reserved by name.

---

## 1. The problem

The per-(item × population) synthesis record was called a **cell** — a matrix framing that
collided with the vocabulary the repository already used everywhere else: `spec_page.py`,
`spec_value_probes`, `case_study_specs`, `economics_entry_specs`, the `specs/` directory, and the
Specification layer named in `armature_v4_resolutions.md`. A reader meeting "cell" could not tell
whether it meant a determination, a table row, or a grid position.

## 2. The decision

| Old | New |
|---|---|
| `evidence_cell_state` | `specifications` |
| `cell_source_links` | `specification_source_links` |
| `cell_id` (both tables) | `specification_id` |
| `idx_cell_state_item` / `_pop` / `_state` | `idx_specifications_item` / `_pop` / `_state` |
| `idx_cell_source_links_ref` | `idx_spec_source_links_ref` |

Both tables held **0 rows** at rename time (the 2026-08-06 clean-room reset plus the 2026-08-12
evidence-stage clearance), so no row moved and none could be lost. Seven dependent views were
rewritten automatically by SQLite under `legacy_alter_table=0`.

## 3. The second decision this forced — replay order

The rename could not be executed as an ordinary numbered schema migration.
`scripts/migrate_db.py` applied **all** schema migrations before **any** data migration, and **19
committed, immutable data migrations still write to the old names**. A schema-phase rename runs
before them and `--rebuild` dies with `no such table: evidence_cell_state`.

`scripts/migrations/025_drop_colonial_role.sql` records the same collision from the other side —
*"the CHECK cannot be tightened while that migration's COLONIAL inserts remain in replay (CI
rebuilds schema-before-data)"* — and escaped it by **withdrawing** a single same-day data
migration. Withdrawal is not available across 19 migrations spanning two months.

**Decision:** the numbered/timestamped split cannot express the real chronology, so give it a way
to. A numbered schema migration may declare, on its own line:

```
-- AFTER_DATA: YYYYMMDDHHMMSS
```

meaning *this migration, and every migration numbered after it, applies only once the data
migrations up to that timestamp have replayed*. `migrate_db.py:build_plan()` produces one ordered
plan from that, and **both** the rebuild path and the apply-pending path walk it — so the two
cannot disagree, which would otherwise surface as a mystery in the reproducibility gate rather
than as this bug.

Executed as:

- `scripts/migrations/055_rename_cell_to_specification.sql` — version marker; DDL is in the
  paired data migration `data_20260812075349_2026-08-12-rename-cell-to-specification.sql`, dated
  after all 19.
- `scripts/migrations/056_schema_phase_rebased_after_rename.sql` — carries the `AFTER_DATA`
  marker, reopening the numbered schema phase on the post-rename names.

**From 057 onward, ordinary numbered schema migrations may reference `specifications` and
`specification_source_links` normally.** Part I's constraints and triggers need no special
handling.

## 4. Alternatives considered and refused

1. **Rename in the schema phase and accept the broken rebuild.** Refused: the reproducibility
   comparison is a blocking gate, and a permanently red gate is a disarmed gate.
2. **Withdraw or rewrite the 19 old-name data migrations.** Refused: data migrations are
   append-only and immutable once committed; forward-fixing is the contract.
3. **Leave the DDL permanently in the data phase, with the invariant merely documented.** Refused:
   it makes the project's two central tables unreachable from the numbered schema phase forever,
   which distorts every future constraint into a data migration, and a documented trap is what a
   defect looks like when it has been described instead of fixed (the same reasoning RV-017 gives).
4. **A compatibility shim — a view named `evidence_cell_state` with `INSTEAD OF` triggers, dropped
   at the end of replay.** Refused: the triggers must enumerate every column and every statement
   shape the 19 migrations use, so the shim's fidelity is unverifiable in the direction that
   matters, and it puts a dead name back into `sqlite_master` for the duration.
5. **A new schema + data baseline squashing the history.** Not refused — deferred. It is the
   larger, cleaner answer, it needs a runner change for data-migration supersession that does not
   exist today, and it is a separate owner decision. `AFTER_DATA` does not foreclose it.

## 5. Enforcement

`evidence_cell_state` and `cell_source_links` are registered in
`governance/retired-vocabulary.yaml` as **RV-020** and **RV-021** (severity `broken`), so the
remaining sweep is a standing mechanical check rather than a one-off grep. `cell_id` is recorded in
that file's `rejected:` section with its reasoning: it fails admission test 4 because
`architecture/schema-spec.md`'s aspirational `cell` table declares its own `cell_id` and no regex
separates the two.

`scripts/tests/test_validate_evidence_state_2_4.py` replays the rename onto its fixture and refuses
to run if that hand-copy drifts from the shipped migration — verified by tampering with it and
watching the guard fire, not by assuming it would.

## 6. Reversal

By a new dated Decision Record and a forward migration, never by rewriting this one or by editing
055, 056 or the data migration.
