# Adversarial critique of migration 065 and its verification

**2026-08-28. Every claim below is measured against a scratch database with 065 applied
and a git worktree with the sweep applied.** Where this contradicts what I said earlier,
this document is right and the earlier statement was wrong.

## A. The completeness proof I gave is CIRCULAR

I claimed: *"`schema_reference_audit.py` passes against the migrated schema with the sweep
applied, and fails with 382 references to 44 names against the current one. That pair is
the proof the sweep is complete."*

**`sweep_065.py` imports its region detector from `schema_reference_audit.py`.** They share
`SQL_REGION`, `SQL_VERB` and `CTX`. The gate therefore cannot, by construction, report
anything the sweeper failed to rewrite: both are blind in exactly the same places. The
"matched pair" proves the sweeper is self-consistent, not that it is complete.

**Measured empirically instead** — swept worktree, migrated database, full battery:

```
BLOCKING failures (9): test_db_integrity, migration_reproducibility, validate_schema,
  validate_axes, validate_verification_consistency, research_dod_selftest,
  pipeline_completeness_fresh, evidentiary_audit_fresh, judgment_handoff_shape
NON-BLOCKING failures (17)
```

Four of the nine (`*_fresh`, `migration_reproducibility`) are expected artefacts of not
having regenerated derived output or applied to canonical. **Five are real breakage.**

## B. Three blind spots, each independent

**B1 — a bare table-name string outside any SQL region.** The sweeper only rewrites inside
string literals that themselves contain an uppercase SQL verb. It never sees
`dbcore.exists(conn, "evidence_sources", "ref_id", ref)`.

> **185 sites in 31 files.** `db.py` 44 · `generate_parts.py` 25 · `test_db_integrity.py`
> 17 · `dbcore.py` 16. Most-referenced: `items` 23, `evidence_sources` 18, `populations`
> 16, `specifications` 12.

Demonstrated: `db.py add-population-match` dies on
`sqlite3.OperationalError: no such table: evidence_sources`.

**B2 — SQL split across adjacent string literals.** `validate_verification_consistency.py:55`
is `"has_unverified_sources FROM specifications "`. The `SELECT` is in the *previous*
literal, so this chunk has no verb of its own, fails `SQL_VERB`, and is skipped. The check
dies on `no such table: specifications`.

**B3 — columns were never swept at all.** The sweeper rewrites table names and *reports*
columns. Thirteen columns cease to exist under 065 — `population_code`, `axis_code`,
`need_code`, `target_population`, `population_label`, `study_population`, `serves_axes`,
`attaches_axes`, `population`, `population_description`, `populations_served_note`,
`root_population_note`, `rationale_ref`.

> **540 sites in 60 files** name one. `population_code` 153, `axis_code` 19,
> `target_population` 15.

Demonstrated: `validate_axes.py` → `no such column: axis_code`;
`test_db_integrity.py` → `no such column: p.population_code`.

## C. The sweep BREAKS a check that works today

`scripts/validate_schema.py`'s `ENTITY_REGISTRY` maps `"jurisdictional_values"` to the
**directory** `data/jurisdictional_values/`. It is in the sweeper's `QUOTED_TARGETS`, so the
sweep rewrote it to `"research_code_leads"`. No such directory exists, and the check goes
from green to a blocking failure reading *"ENTITY_REGISTRY names no directory that exists
under data/. This is a configuration fault, not a pass."*

I had already caught this exact class once — `OUTPUT_DIR = REPO_ROOT / "site" / "rooms"` —
and fixed only the instance I could see rather than the rule that produced it.

## D. The rename does NOT create the spine

CLAUDE.md: *"not one foreign key in the schema lands on any stage's hand-off object … The
rename creates the spine."* It does not. Measured on the migrated schema:

| hand-off | rows | inbound FKs | points at the previous hand-off? |
|---|---|---|---|
| `research_items` | 875 | 0 | — |
| `evidence_items` | 10 | 13 | **NO** (no FK to `research_items`) |
| `judgment_items` | 0 | 1 | YES — and it pre-existed as `source_value_extractions.ref_id` |
| `synthesis_items` | 0 | 0 | **NO** |
| `specification_items` | 0 | 1 | **NO** |
| `render_provisions` | 93 | 13 | **NO** |

**One of five links exists, and the rename did not create it.** A rename cannot create a
foreign key. Building the spine is a separate migration that adds columns and keys, and
nothing in 065 does it.

## E. Connectivity is not improved where it is worst

Fifteen tables sit outside the main connected component (undirected, so joins count in
either direction):

```
research_items 875 rows   base_decisions 174   base_data_migrations 353
base_lang_jur_map 70      base_weighting_profile 5   base_access_duration 3
base_access_stakes 3      base_life_stage_modifiers 2   base_pipeline_runs 1
base_situations 0         evidence_roots 0     evidence_url_verification_runs 0
research_stubs 0          synthesis_connections 0 + synthesis_connection_links 0
```

`research_items` — the 875-row clue store, the research stage's hand-off object — has
**zero foreign keys in either direction**, exactly as before. The connection layer
(`synthesis_connections` + `synthesis_connection_links`) is a severed two-table island.

## F. "80 → 125 foreign keys" overstates the gain by 14

Fourteen of the 45 new keys are `medical_code` columns pointing at
`base_taxonomy_medical`, which holds **0 rows and has no crossing map to the other three
taxonomies**. D-0170 says explicitly that lens-switching runs through the crossing maps, so
the fourth lens cannot be written (FK fails) and could not be switched to if it could.
Verified: `INSERT ... medical_code` → `FOREIGN KEY constraint failed`.

The honest figure is **80 → 111 usable pointers**, plus 14 declared-but-unresolvable.

## G. A ratified DR contradicts CLAUDE.md, and I followed the DR silently

`CLAUDE.md:66`: *"`judgment_items` is a NEW table, not a rename."*
`D-0168` rationale: *"judgment_items is not a new table needing a designed column set; it
inherits the extraction table."*

065 renames `source_value_extractions` → `judgment_items`, which follows the DR. That is
almost certainly correct — the DR is ratified and specific — but I made the choice without
recording the conflict, and CLAUDE.md still says the opposite.

## H. `sweep_065.py` edits the wrong repository

It resolves the tree from `schema_reference_audit.py`'s own location, ignoring the working
directory. Running it from inside a git worktree swept **the main checkout instead**, which
is what happened during this critique. A one-shot rewriter that can silently edit a
different tree than the one you are standing in is dangerous; it needs a `--root`.

## I. What actually held up under attack

Not everything failed, and the parts that held are the parts I tested hardest:

- Applies clean; `foreign_key_check` clean; `integrity ok`; DDL byte-identical between
  rebuild-from-history and direct-apply across all 66 tables and 18 views.
- Every original CHECK and named index preserved; `dbcore.check_values()` reads the folded
  table's `applicability` vocabulary correctly through the CLI.
- The lens refusals fire exactly as designed: two lenses → CHECK fails; zero lenses → CHECK
  fails; duplicate `(item, code, subtype)` → UNIQUE fails; a legitimate single-lens write
  succeeds.
- `dbcore.ref_id_homes()` finds all 12 ref_id tables under their new names;
  `next_ref_id` → `REF-00971`, correct above the 970 high-water mark.
- Every `db.py` read subcommand works against the migrated schema.
- The owner's citation walk — `render_provisions` ↔ `evidence_items` — **is reachable**.

## J. A modelling error I made during this critique

My first reachability pass followed foreign keys in the outbound direction only and
reported that no render table can reach `evidence_items`. That is wrong: a join traverses a
key in either direction, so read-walkability is undirected. Corrected in §E and §I. The
isolated-table finding is unaffected — those tables have no edges in either direction.

## What I would do before landing

1. **Stop claiming the gate proves the sweep.** Give the gate its own detector, or drop the
   claim and rely on the battery.
2. **Sweep columns**, or accept that 540 sites break. This is the largest single item and it
   was never in scope.
3. **Revert `validate_schema.py`** in the sweep; audit the other seven `QUOTED_TARGETS` for
   non-table strings.
4. **Handle split SQL literals** — join adjacent literals before region detection.
5. **Handle bare table-name arguments** — a name that exactly equals a live table, in a call
   position, in a file that opens the database.
6. Decide whether the **spine** lands in 065 or a successor, and stop saying the rename
   creates it.
7. Either seed `base_taxonomy_medical` **and its crossings**, or drop the 14 `medical_code`
   columns until there is a vocabulary — an FK that can never resolve is apparatus.
