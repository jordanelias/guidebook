# 26 — Stage `render`

_Generated 2026-11-12 02:01 UTC at commit e73b588, schema user_version 125. Every figure here is computed by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_dossier.py`; re-run it, do not trust this text (CLAUDE.md rule 7a)._


**Contract anchor:** renderers + the claim-strength register map (evidence-architecture.md §6)

**Contract entry condition(s):** determinations tagged with design_scale, ready to present per audience

## Tables (1)

| table | rows | columns |
|---|---|---|
| weighting_profile | 5 | audience, use_pattern, tier_weights, notes |

## Views touching this stage (0)

None.

## Contract criteria

| id | kind | check | criterion (first 200 chars) |
|---|---|---|---|
| register-invariants | integrity | **NONE (unenforced)** | Every rendering of a cell carries the identical determination tuple across registers; no unflagged and no above-weak-band best-practice language on regulatory-stratum cells under any weighting profile |
| mode-stratum-matrix-consistency | integrity | scripts/audit/matrix_consistency.py | The grain x design-scale directness matrix regenerated from schemas/directness.py matches evidence-architecture.md §3. |

## `db.py` verbs that WRITE this stage's tables (0)

None.

## `db.py` verbs that only READ this stage's tables (0)

None.

## Other code that WRITES this stage's tables (1)

| file | lines | writes | purpose (docstring) |
|---|---|---|---|
| scripts/emit_data_migration.py | 783 | weighting_profile | scripts/emit_data_migration.py — create a properly-named data-migration file. Per GAP-290 resolution. The migration system (scripts/migrate_db.py) requires data migrations to be named: scripts/migrations/data_{YYYYMMDDHHMMSS}_{session-slug} |

## Code that READS this stage's tables, writing none of them (0)

None.

## Tests naming this stage's tables (0)
None.

## Registry checks whose PRIMARY stage (by tables read) is `render` (0)

None.

## Skills naming this stage's tables (0)
None.

## Prose homes for this stage
- `architecture/page-templates.md`
- `architecture/navigation-modes.md`
- `governance/evidence-architecture.md`
- `governance/audience-priority.md`