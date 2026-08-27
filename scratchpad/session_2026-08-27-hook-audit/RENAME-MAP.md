# The rename — reconciling three stage maps, then executing

**Owner instruction 2026-08-27:** *"I really need us to rename all our tables with the revised
nomenclature."* This document reconciles what "revised" now means, because three maps disagree, and
the stage prefix **is** the table name — so renaming against the wrong map means renaming twice.

## 1. What already exists (read in full, per owner instruction, from #120 and #121)

| document | date | what it settles |
|---|---|---|
| `REPAIR-PLAN.md` §1 | 08-25/26 | **The ordering graph. `P0.1` is "safety: nothing else runs first."** |
| `REPAIR-PLAN.md` P0.6 | 08-26 | §R8 rename `axes`→demand layer, **owner-gated, whole, rename BEFORE register entry** |
| `REPAIR-PLAN.md` P1.0 | 08-25/26 | `specifications` re-key: **drop `item_code` AND `population_code`**; key on `parameter_canonical` |
| `STAGE-TABLE-MAP.md` | 08-25 | All 66 tables derived to stage — **under FIVE stages** |
| `NOMENCLATURE.md` Part E | 08-27 am | All 66 renamed — **under SIX stages, `res_/evi_/jud_/syn_/spe_/ren_`** |
| the architecture note | 08-27 pm | **`base.` / `research.` / `evidence` / `judgment`** — full-word namespaces |

**Migration numbers are already spoken for**: `065` (P1.1), `066` (P2.2), `067` (P2.5). The rename
must take a free number, not 065.

## 2. The three maps disagree on where four tables live

Rule 0 makes the architecture note the latest statement, and it **re-homes tables the earlier two
placed elsewhere**:

| table | STAGE-TABLE-MAP (08-25) | NOMENCLATURE Part E (08-27 am) | **architecture note (08-27 pm)** |
|---|---|---|---|
| `source_locators` | research | `res_items` — research hand-off | **`base.clues` — SUBSTRATE** |
| `source_value_extractions` | evidence collection | `evi_items` — evidence hand-off | **judgment** *(the deep read "derives value")* |
| `evidence_sources` | evidence collection | `evi_sources` — a satellite | **the evidence object itself** |
| `items` | substrate | retired outright | **`base.building` — substrate** |

**This is not a naming disagreement. It is a stage disagreement**, and under the grammar the stage is
the prefix. `source_locators` becomes `research_items` under one map and `base_clues` under another.

**CORRECTED 2026-08-27 — the premise stated here was false.** This section originally read *"The
note wins on rule 0"* for all four rows. It does not. The owner adopted **items #1 and #2 only**, and
explicitly did **not** adopt item #3: *"`base.clues` is not moved to substrate."* The note is *"not
complete, and not definitive — just a thought document."*

| table | disposition |
|---|---|
| `source_value_extractions` → **judgment** | **RULED** (item #2 adopted). Stands. |
| `evidence_sources` → **the evidence object** | **RULED** (item #2 adopted). Stands. |
| `source_locators` → `base.clues` | **NOT ADOPTED.** It stays in **research**. |
| `items` → `base.building` | **NOT REACHED by the note.** Owner ruled separately: `base_building` is three levels and `items` is none of them, so the 2026-08-26 render-rollup ruling stands. |

**What executing the original premise would have done:** moved the 875-row clue store into substrate,
reversing the ratified `DR-2026-08-06` wall — *"nothing joins it, no determination may cite it"* —
with no recorded supersession. The R1 audit also measured the physical fact that settles it
independently: `source_locators` has **0 inbound and 0 outbound foreign-key edges**, and a substrate
table nothing may join is a contradiction in terms.

## 3. Three genuine conflicts that need one word each

**C-1 · `items`.** #120 ruled *"`items` is demoted to the Part-4 render rollup, derived from
specifications"*. The note puts building elements in **`base.building`** — substrate. Those are
different stages. **Which?** *(My read: the note is later and `base.building` is where a reader would
look. But #120's ruling is explicit and load-bearing for P1.0.)*

**C-2 · the ICF layer's name.** §R8 ruled `axes` → **`icf_demands`** (2026-08-25, confirmed 08-26,
with a register entry). The note calls the same thing **`base.taxonomy_icf`**. **Under the namespace
grammar: `base_icf_demands`?** — keeping the ruled noun, adding the ruled namespace.

**C-3 · separator and prefix form.** The note writes `base.models`. **SQLite has no schemas**, and a
dot in an identifier collides with `schema.table` syntax — it would need quoting everywhere forever.
**Proposal: underscore** — `base_models`, `research_logs`, `evidence_items`, `judgment_items`. This
also retires B1's collision finding against 3-char `stage_id[:3]` prefixes, since full words don't
collide.

## 4. What is NOT blocked, and should go first regardless of C-1..C-3

`REPAIR-PLAN` P0.1 is explicit: **"safety: nothing else runs first."**

`dbcore.is_canonical()` exists solely to refuse writes to the committed database, and **its only
callers are its own selftest** (`dbcore.py:438-439`). `connect()` never calls it, and `db_path()`
**defaults to canonical** when `GUIDEBOOK_DB_PATH` is unset.

> **A rename is the largest write this project has ever attempted, and the guard that stops it
> landing on the canonical database is unwired.** P0.1 is not bureaucracy ahead of the rename — it is
> the specific protection against the specific accident this specific change can cause.

P0.1 ships with P0.2 (four skill lines instructing `GUIDEBOOK_DB_PATH=data/guidebook.db` on **write**
commands — `connection-auditor_SKILL.md:185,192,199`, `connection-discovery_SKILL.md:219`), because
wiring the guard alone turns those skills into runtime failures.

**Already done this session:** the `ref_id` allocator precondition — `_REF_ID_HOMES` was hardcoded to
two tables and swallowed `OperationalError`, so post-rename `next_ref_id` would have minted
`REF-00001` onto live data **silently**. Now derived from the schema; 12 tables carry `ref_id`.

## 5. The order

```
P0.1 + P0.2   canonical-write guard        ← unblocked, and gates everything
      │
   [C-1..C-3 answered]
      │
  RE-DERIVE the map under the architecture note   ← STAGE-TABLE-MAP is 5-stage; Part E is pre-note
      │
  landmine sweep: migration_reproducibility CORE_INVARIANTS (6 names, `items` ×14)
                  build_site FP_TABLES (6 of 7 renamed)
      │
  ONE migration, AFTER_DATA marked, + caller sweep + --selftest
```

**Not 065.** And the sweep list is the one A3-F6/A4-B10 measured, not Part G's: 3 views, 16 Python
files, 22 skills, 4 governance YAMLs, plus the generators.
