---
name: cell-curator
description: >
  Populate evidence state per (specification × population) pair. Each cell represents
  whether a specific spec has evidence for a specific population, classified as:
  stated (direct evidence), provisional (inferred from adjacent evidence),
  pending (gap identified, no evidence), or not_applicable. ALWAYS use when:
  populating cell records, assessing evidence state for population pages, or
  auditing coverage across the spec×population matrix. Trigger on: "cell state",
  "evidence state", "population coverage", "spec coverage matrix", "cell curation".
---

**Model:** Opus 4.6 (evidence state classification requires judgment)
**SQLite:** `data/guidebook.db`

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
   SELECT sp.population_code, es.evidence_tier, es.surname, es.year
   FROM specification_population sp
   JOIN specification s ON sp.spec_id = s.spec_id
   LEFT JOIN source_slug_links ssl ON s.bpc_source_slug = ssl.slug
   LEFT JOIN evidence_sources es ON ssl.ref_id = es.ref_id
   WHERE s.item_code = '{item_code}'
   ```

2. For each population: classify evidence state based on what's available
3. Write cell records to specification_population or a dedicated cell table

### Batch curation
1. Query uncurated cells:
   ```sql
   SELECT s.item_code, p.population_code
   FROM specification s
   CROSS JOIN population p
   WHERE s.status = 'active'
   AND NOT EXISTS (
     SELECT 1 FROM specification_population sp
     WHERE sp.spec_id = s.spec_id AND sp.population_code = p.population_code
   )
   ```
2. For each uncurated pair: assess and classify

---

## 3. Quality gate

Per C10: all active spec × population pairs must have an evidence state assigned.
```sql
SELECT COUNT(*) as uncurated
FROM specification s
CROSS JOIN population p
WHERE s.status = 'active'
AND NOT EXISTS (
  SELECT 1 FROM specification_population sp
  WHERE sp.spec_id = s.spec_id AND sp.population_code = p.population_code
)
```
