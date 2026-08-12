---
name: specification-curator
description: >
  Populate evidence state per (item × population) pair. Each specification records
  whether a given item has evidence for a given population, classified as:
  stated (direct evidence), provisional (inferred from adjacent evidence),
  pending (gap identified, no evidence), or not_applicable. ALWAYS use when:
  populating specification records, assessing evidence state for population pages, or
  auditing coverage across the item × population matrix. Trigger on: "specification state",
  "evidence state", "population coverage", "item coverage matrix", "specification curation".
---

<!-- Renamed from `cell-curator` on 2026-08-12 by owner instruction, following the
     schema rename of `evidence_cell_state` to `specifications`. Two committed
     attestations cite the identifier `cell-curator`; they are NOT rewritten, and
     `cell-curator` is registered in adherence_log_audit.py's EXTRA_RULE_IDS so
     they still resolve. See DR-2026-08-12-specification-curator-rename. -->

**Model:** Opus-class (evidence state classification requires judgment)
**SQLite:** `data/guidebook.db`
> **Schema note (corrected 2026-08-02):** `specification`, `specification_population`, and
> `population` — all SINGULAR — **do not exist**
> (note the plural `specifications` below: the singular is a different, legacy name and
> `scripts/generate/room_page.py:51` still reads it) in `data/guidebook.db` — verified against
> `sqlite_master`. The canonical tables are **`items`** (93, all `status='active'`),
> **`populations`** (23), and **`specifications`** (the per-(item × population) specification this
> skill exists to populate — 0 rows today, of a 93 × 23 grid; renamed from
> `evidence_cell_state` at schema version 055 on 2026-08-12). Queries below are repointed.
>
> Do **not** run `scripts/db/migrate_all.py`; it targets a legacy path that does not exist.
> All specification writes ship as migrations (`emit_data_migration.py` → `migrate_db.py`).


---

## 1. Evidence State Machine (per A6 §2)

| State | Meaning | Criteria |
|---|---|---|
| `stated` | Direct evidence exists | ≥1 Tier 1–3 source addresses this spec for this population |
| `provisional` | Inferred from adjacent evidence | No direct evidence, but related spec or related population has Tier 1–3 evidence that reasonably transfers |
| `pending` | Gap identified | No evidence found; gap register entry exists or should be created |
| `not_applicable` | Spec doesn't apply to population | Population's functional profile excludes this spec (e.g., acoustic specs for non-hearing populations) |

---

## 2. Workflow

### Per-spec curation
For a given spec, assess evidence state across all 11+ populations:

1. Query existing evidence links:
   ```sql
   SELECT ipl.population_code, es.tier, es.first_author_last, es.pub_year
   FROM item_population_links ipl
   JOIN items i ON ipl.item_code = i.item_code
   LEFT JOIN source_slug_links ssl ON i.bpc_source_slug = ssl.slug
   LEFT JOIN evidence_sources es ON ssl.ref_id = es.ref_id
   WHERE i.item_code = '{item_code}'
   ```

2. For each population: classify evidence state based on what's available
3. Write specification records to **`specifications`** — one row per (`item_code`,
   `population_code`), `state` ∈ `stated` / `provisional` / `pending` / `not_applicable`.
   `stated` and `provisional` require non-empty `governing_refs`. Ships as a migration.

### Batch curation
1. Query uncurated specifications:
   ```sql
   SELECT i.item_code, p.population_code
   FROM items i
   CROSS JOIN populations p
   WHERE i.status = 'active'
   AND NOT EXISTS (
     SELECT 1 FROM specifications ecs
     WHERE ecs.item_code = i.item_code AND ecs.population_code = p.population_code
   )
   ```
2. For each uncurated pair: assess and classify

---

## 3. Quality gate

Per C10: all active spec × population pairs must have an evidence state assigned.
```sql
SELECT COUNT(*) as uncurated
FROM items i
CROSS JOIN populations p
WHERE i.status = 'active'
AND NOT EXISTS (
  SELECT 1 FROM specifications ecs
  WHERE ecs.item_code = i.item_code AND ecs.population_code = p.population_code
)
```
