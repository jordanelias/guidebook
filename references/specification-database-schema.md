# Specification Database — Schema Reference
**Created:** 2026-04-08 (Phase 2A — CO-0006)
**Format:** JSON array in `specification-database.json`
**Current batch:** batch1 (10 BPC files, 143 records)
**Total BPC files:** 76 — remaining batches to follow

## Field definitions

| Field | Type | Description |
|---|---|---|
| `spec_id` | string | SPEC-NNNN — stable identifier |
| `item_code` | string/null | Part 4 item code (A-01 etc.) — null until mapped at ISW |
| `bpc_source_slug` | string | Source BPC slug |
| `topic` | string | Topic directory |
| `parameter` | string | Parameter type (grab_bar_height, rt60, etc.) |
| `value_type` | string | `range` or `fixed` |
| `value_min` | number | Minimum value |
| `value_max` | number | Maximum value |
| `value_median` | number | Midpoint of range |
| `unit` | string | mm, %, dB, lux, s, m², K, etc. |
| `evidence_tier` | string/null | Tier of supporting evidence — null until curated |
| `populations` | array | Population codes this spec applies to — empty until curated |
| `jurisdictions_supporting` | array | Jurisdictions that specify this value |
| `jurisdictions_divergent` | array | Jurisdictions with different value |
| `opus_synthesized` | bool/null | Whether source BPC has Opus synthesis |
| `recommendation_strength` | string/null | Strong / Conditional / No recommendation (Phase 1A) |
| `percentile_basis` | string/null | Anthropometric basis for range endpoints, if known |
| `context_note` | string | Surrounding text context from BPC extraction |
| `extraction_batch` | string | Which extraction pass produced this record |
| `conditions` | array | Conditional values per CO-0006 §C3 (population-dependent) |

## Conditions sub-schema (CO-0006 amendment C3)
For parameters with population-dependent values:
```json
"conditions": [
  {"condition": "MOB single wheelchair user", "value_min": 1500, "value_max": 1500},
  {"condition": "MOB two wheelchair users passing", "value_min": 1800, "value_max": 1800}
]
```
When conditions is non-empty, top-level value_min/value_max represent the full range across all conditions.

## Curation status
Batch 1: Automated extraction only. Fields requiring manual curation: `item_code`, `evidence_tier`, `populations`, `jurisdictions_supporting`, `jurisdictions_divergent`, `recommendation_strength`, `percentile_basis`.

Curation occurs at ISW stage when each item is written.

## Extraction notes
- Extraction used regex pattern matching on consensus findings + best-practice synthesis sections
- Classifier assigns `parameter` type from context keywords — review `unclassified` records
- Some noise likely: verify records with unit `k`, `cm` (may be mixed-unit captures)
- Deduplication within slug by (parameter, value_min, value_max, unit)

## Batches
| Batch | BPC files | Records | Date |
|---|---|---|---|
| batch1 | 10 | 143 | 2026-04-08 |
| batch2 | — | — | pending |
| batch3 | — | — | pending |
| batch4 | — | — | pending |
