# Ecosystem Audit — SQLite Integrity, Pipelines, Coverage
**Date:** 2026-05-10
**DB schema_version:** 5
**Tables:** 19 | **Total rows:** ~6,400

---

## Critical Findings (require fix)

### C1. source_slug_links FK collision — 648 broken rows

`source_slug_links.ref_id` has a FK to `evidence_sources.ref_id`. But 648 of 1,290 distinct ref_ids in the link table contain BPC-local reference IDs (like "MOB-01", "ACG-01") instead of global evidence_sources IDs (like "REF-00001"). The `ref_id` and `local_ref_id` columns hold the same value for these rows — the migration script used `local_ref_id` as `ref_id` when no global mapping existed.

**Impact:** 648/1,401 source-slug links are broken. Any query joining `source_slug_links` to `evidence_sources` silently drops ~46% of the citation graph. BPC coverage statistics, citation mining, and evidence tracing are all affected.

**Fix options:**
- (a) Build a mapping table from local ref_ids (MOB-01 etc.) to global ref_ids (REF-00001 etc.) using BPC file content as the bridge, then UPDATE source_slug_links.ref_id to the global ID.
- (b) If no global ID exists for a local ref, INSERT the source into evidence_sources first (populate from BPC key-sources tables), then update the link.
- (c) If the intent is that local_ref_id IS the link key, drop the FK to evidence_sources and make local_ref_id + slug the composite key. This would be a schema change.

**Recommended:** Option (a) + (b). The FK design is correct — sources should live in evidence_sources with global IDs. The migration just didn't populate them.

### C2. bpc_metadata orphans — 16 rows without slugs

16 bpc_metadata entries have no matching slugs row: 14 population-level summary files (ALL-ENV, DEAF, DEM, IntD, MOB, NDV, NDV-MH, NEU, OFS, PAIN, VIS, DBL, ALL-FW, ALL-ROOMS) plus 2 utility files (_template, index).

**Impact:** These rows fail FK checks. They represent population taxonomy files and file-system artifacts, not BPC research slugs.

**Fix:** Either (a) add corresponding entries to `slugs` with a special status like "POPULATION" or "UTILITY", or (b) delete these 16 rows from bpc_metadata since they don't represent research-tracked BPCs. Option (b) is cleaner — these files have no search_coverage, no search_languages, no source_slug_links. They're metadata without a pipeline.

### C3. items.bpc_source_slug — 91/91 NULL

Every item in the database has `bpc_source_slug = NULL`. The C0 bulk migration created 91 items but never linked them to their source BPCs.

**Impact:** The items→BPC relationship is completely unpopulated. Any query attempting to trace an item's evidence basis through its BPC gets nothing.

**Fix:** Populate bpc_source_slug from the BPC key-sources tables or from the Part 4 specification text that references each BPC. This is a workplan item, not a quick fix — needs the item audit pipeline (CO-0009) to map each item_code to its governing BPC slug.

---

## Structural Findings (design issues)

### S1. Jurisdiction code inconsistency — 30 codes in evidence_sources not in search_coverage

evidence_sources contains 30 jurisdiction codes not represented in the 23-code search_coverage vocabulary. These include:
- **Compound codes:** CA/INT, US/AU/INT, US/NL/INT, AU/NZ, EU/UK, TH/AU, INT/ZA
- **Language codes used as jurisdictions:** DA, FI, JA, ZH (these are ISO 639 language codes, not jurisdiction codes)
- **Regional groups:** Nordic, ASEAN, EU, LAC, INTL
- **Individual countries not in coverage:** BE, CL, GH, HK, MY, NG, PT, UAE
- **Unverified:** [GREY — jurisdiction unverified]

**Impact:** Evidence sources can't be traced to their jurisdictional coverage. Cross-referencing evidence_sources.jurisdiction with search_coverage.jurisdiction misses these 30 codes.

**Fix:** Normalize jurisdiction codes to the 23-code vocabulary used by search_coverage. Compound codes should be split into multiple rows or stored in a junction table. Language codes should not appear in jurisdiction fields.

### S2. connections.filed_in — 13 values not in slugs

`connections.filed_in` stores topic directory names (like "entrances-and-circulation", "wayfinding-and-signage") rather than BPC slugs. These are directory-level classifications, not individual BPC references.

**Impact:** Minor — filed_in is a classification field, not a FK. But it creates a loose coupling that can't be validated automatically.

### S3. Three empty tables

| Table | Status | Expected |
|---|---|---|
| citation_mining | 0 rows | Pipeline not yet started (citation_mining_complete=0 for all slugs) |
| conflicts | 0 rows | Schema populated, data not migrated from cross-population BPC |
| decisions | 0 rows | Decision records not yet migrated to DB |

---

## Coverage Assessment

### Jurisdictional coverage
- 23 jurisdictions tracked across 81 slugs
- All 81 non-MERGED slugs have ≥10 jurisdictions searched
- Zero slugs with 0 jurisdictions
- Coverage appears complete for the current 23-jurisdiction vocabulary
- **Gap:** 30 additional jurisdictions appear in evidence_sources but are untracked (see S1)

### Multilingual coverage
- 14 languages tracked across 81 slugs
- All 81 slugs have ≥5 languages searched
- EN dominates (230 results); DA is thinnest (18 results)
- No languages at zero coverage
- **Observation:** ES (23 results) and FI (20 results) are relatively thin given the number of Spanish-speaking and Finnish jurisdictions with accessibility standards

### Evidence tier distribution
| Tier | Count | % |
|---|---|---|
| 1 (primary research) | 101 | 15.4% |
| 2 (DPO/Co-1) | 60 | 9.2% |
| 3 (systematic review) | 218 | 33.3% |
| 4 (standards/guidelines) | 64 | 9.8% |
| 5 (code/regulation) | 121 | 18.5% |
| 6 (code floor) | 89 | 13.6% |
| NULL | 1 | 0.2% |

Tier 1+2+3 = 379 (57.9%) — majority of evidence base is primary research or systematic review. Healthy distribution for an evidence-based guidebook.

### Pipeline completeness
- Full pipeline (coverage + languages + sources): 67/81 slugs (83%)
- Partial pipeline: 14/81 slugs (17%)
- bpc_complete=1: 61 slugs (75%)
- search_complete=1: 48 slugs (59%)
- citation_mining_complete=1: 0 slugs (0%)

### Adversarial protocol coverage
- 244/250 CLOSED gaps missing adversarial protocol fields (confidence_interval, shift_conditions, named_dissenter, falsification_condition)
- Expected: standing rule #7 was added in PI v10.6 (2026-05-10); most gaps predate it

### Connections pipeline
- 245 connections total
- 201 CONSUMED (82%)
- 42 CONSUMED-DEFERRED (17%)
- 1 PENDING, 1 CLOSED
- 3 connections with zero targets (minor cleanup)

---

## Recommended Fix Priority

| Priority | Finding | Effort | Impact |
|---|---|---|---|
| P1 | C1: source_slug_links FK — build local→global ref_id mapping | ~2 sessions | Restores 46% of citation graph |
| P1 | C2: bpc_metadata orphans — delete 16 non-BPC rows | 10 min | Clears 16 of 717 FK violations |
| P2 | S1: Jurisdiction code normalization | ~1 session | Enables cross-referencing evidence↔coverage |
| P2 | C3: items.bpc_source_slug population | CO-0009 pipeline | Enables item→evidence tracing |
| P3 | S3: Populate conflicts table from cross-pop BPC | ~1 session | Structured conflict data |
| P3 | S2: connections.filed_in normalization | ~30 min | Minor consistency |
| Deferred | Adversarial protocol backfill | Ongoing | Apply to new closures; don't backfill 244 |

---

**End audit.**
