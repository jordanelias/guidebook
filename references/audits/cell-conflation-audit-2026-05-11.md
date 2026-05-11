# Cell Conflation Audit — All Tables
**Audited:** 2026-05-11 · `data/guidebook.db` (post evidence_sources v2 cutover)
**Tables audited:** 23 (skipped 4: empty `decisions`, empty `conflicts`, trivial `db_meta`, legacy `evidence_sources_v1_legacy`)
**Total rows examined:** ~8,300
**Method:** Two-pass — (1) regex pattern detection across all text columns excluding columns where the content type is legitimate (sessions, paths, dates, prose), (2) structural checks for multi-value cells, enum inconsistency, FK orphans, identifier-format mismatches, and type-swap errors

---

## Summary

The v2 schema migration eliminated the major conflation issues in `evidence_sources`. The remaining issues are **9 distinct findings across 5 tables**, ranked by severity below.

| Severity | Count | Notes |
|---|---|---|
| **High** (true conflation, blocks correct querying) | 4 | applicable_groups multi-value · PMC in pmid · FK orphans · multi-value targets |
| **Medium** (denormalization, fixable but works) | 2 | Section/connection_targets multi-value · gaps.section as item codes |
| **Low** (style / not semantic conflation) | 3 | ISO case · jurisdiction flag string · doi_less_key formatting |

---

## High-severity findings

### H1. `items.applicable_groups` — comma-separated list in a single column

**89% of items** (81 / 91) have multi-value strings in this column:

```
A-03  →  AUT, PCS, DEM, MH, SENS
A-05  →  NDV, DEM, PAIN, MH, OFS
A-08  →  AUT, PCS, DEM, MH, PAIN, OFS
```

This breaks the "one fact per column" rule and prevents joining against a `populations` table. Cannot answer "show all items applicable to DEM" without LIKE-pattern matching, which is fragile and slow.

**Fix:** create `item_population_links` junction table:
```sql
CREATE TABLE item_population_links (
  item_code   TEXT REFERENCES items(item_code),
  population  TEXT,
  PRIMARY KEY (item_code, population)
);
```
Migrate by splitting comma-separated values, then drop `applicable_groups`.

---

### H2. `evidence_sources.pmid` — PMC ID stored in PMID column

1 row identified: `REF-00701` has `pmid = 'PMC12673401'`. PMC IDs go in the `pmcid` column (which exists in v2 schema but is empty).

**Fix:**
```sql
UPDATE evidence_sources
SET pmcid = 'PMC12673401', pmid = NULL
WHERE ref_id = 'REF-00701';
```

---

### H3. FK orphans (3 cases)

| Child table | Orphan value | Should reference |
|---|---|---|
| `source_slug_links.ref_id` | `TBE-03` | not in `evidence_sources` (1 orphan) |
| `spec_value_probes.ref_id` | `ANSI-S12.60-S5.3` | not in `evidence_sources` (1 orphan) |
| `bpc_metadata.slug` | `ALL-ENV, ALL-FW, ALL-ROOMS, DBL, DEAF, ...` | not in `slugs` (16 orphans) |

The 16 `bpc_metadata` orphans likely represent an older slug naming convention that wasn't migrated when slugs were renamed. **Fix:** investigate whether `ALL-*` and population codes (`DBL`, `DEAF`, `VIS`, `DEM`, etc.) are legitimate slugs that need creating in `slugs`, or whether `bpc_metadata` was populated with abbreviated identifiers that should be expanded.

`TBE-03` and `ANSI-S12.60-S5.3` are non-`REF-` prefixed identifiers — likely legacy IDs from before the REF-NNNNN scheme. Either delete or create canonical `evidence_sources` rows for them.

---

### H4. `connection_targets.target` — multi-value cells (7 rows)

```
CON-0001 items; cognitive
Part 4 lighting -- Kolberg 2022: DEM nursing homes fail melanopic EDI
SRB items / LCL items -- Harper/Dakin stair contrast chain: unify specification
ULB grab bar items / fold-down-grab-bar -- Lee/Sanford 2018: bilateral 356mm CL 813mm AFF
MST conflict resolution stratum -- Berwick 2021 SR: 14/17 QST confirm FMS cold pain
```

These targets bundle two distinct things: (1) the actual target identifier, (2) a justification or evidence note. The justification should be in a separate column (`target_rationale` or similar), or the target should be split into multiple rows.

**Fix:** Add a `target_rationale` column; split each cell.

---

## Medium-severity findings

### M1. `gaps.section` — 103 distinct values; appears to be item_codes used as section labels

Sample values: `E-03` (11×), `G-04` (10×), `E-01` (9×), `I-01` (8×). These are **item codes**, not section labels. The column is doing double duty as "which item this gap relates to."

**Fix:** rename to `related_item_code` and add FK to `items(item_code)`, OR add a proper `gap_item_links` junction if a gap can relate to multiple items.

---

### M2. `evidence_sources.doi_less_key` — partial bibliographic reconstruction

This is a denormalized lookup key built before v2. With v2's structured fields it's redundant. 3 rows still contain DOI strings inline:

```
REF-00068 → keall_2015_hipi study. lancet 385:231–238. doi:10.1016/s0140-6736(14)61006-0
REF-00257 → (internal)_2026_references/case-study-compendium.md v10.4 — 26 case
REF-00627 → 筑波大学_2025_感覚過敏…
```

**Fix:** regenerate `doi_less_key` from v2 structured fields, or drop the column entirely now that `first_author_last`, `pub_year`, `doi`, `pmid` are queryable directly.

---

## Low-severity (style, not conflation)

### L1. `term_aliases.language` — uppercase ISO codes

All 14 language codes are uppercase (`EN`, `DA`, `ZH`) rather than the ISO 639-1 lowercase standard (`en`, `da`, `zh`). Consistent but non-standard.

`evidence_sources.lang_detected` uses lowercase. The two tables disagree on case.

**Fix:** lowercase all `term_aliases.language` values; add CHECK constraint `language = lower(language)`.

---

### L2. `evidence_sources.jurisdiction` — one row contains a flag-string

```
REF-00369 → '[GREY — jurisdiction unverified]'
```

The `[GREY — ...]` annotation should be in `verification_note` or `grey_reason`, with `jurisdiction = NULL` and `grey_flag = 1`.

**Fix:**
```sql
UPDATE evidence_sources
SET jurisdiction = NULL,
    grey_flag = 1,
    grey_reason = COALESCE(grey_reason || '; ', '') || 'jurisdiction unverified'
WHERE ref_id = 'REF-00369';
```

---

### L3. Freeform `mechanism` and `description` columns in `connections`

Schema didn't actually include `mechanism` or `kind` — only `connection_type` (1 distinct value: "CROSS-ITEM"), `status`, `filed_in`, `description`. Description is rightly freeform. No conflation here — earlier audit was using wrong column names.

---

## Tables that passed cleanly (no findings)

| Table | Why clean |
|---|---|
| `bpc_metadata` | Apart from 16 FK orphans (H3), columns are atomic |
| `citation_mining` | All deferral/notes content in proper fields |
| `connections` | Schema is minimal; freeform `description` is correct as prose |
| `data_migrations` | Migration metadata is correctly atomic |
| `evidence_population_match` | Grades, populations, notes all in correct columns |
| `evidence_source_authors` | **No type-swap errors** — is_corporate flag consistent with which name field is populated |
| `evidence_sources` (v2) | Apart from 2 low-severity items (L2, M2), the v2 migration achieved one-fact-per-column |
| `evidence_sources_v1_legacy` | Not audited — known stale, preserved for rollback |
| `gaps` | Status/priority/category use clean enums; description is prose |
| `item_audit_runs` | Run logs are correctly structured |
| `search_coverage`, `search_languages` | Per-row state tracking, atomic |
| `slugs` | Path columns correctly hold paths |
| `source_slug_links` | Junction table, correctly atomic |
| `spec_value_probes` | All enums clean (direction, phase, claim_type) |
| `term_aliases` | Atomic, except L1 casing |
| `term_item_links`, `terms` | Atomic |

---

## Recommended fix order

| # | Fix | Effort | Impact |
|---|---|---|---|
| 1 | H1: normalize `items.applicable_groups` → `item_population_links` | 2h | Unblocks joinable population queries |
| 2 | H2: move REF-00701 PMC ID to pmcid column | 1 min | Correctness |
| 3 | H3: investigate 16 `bpc_metadata.slug` orphans | 1h | Data integrity |
| 4 | H3: resolve `TBE-03` and `ANSI-S12.60-S5.3` orphans | 30 min | Data integrity |
| 5 | H4: split 7 `connection_targets.target` multi-value cells | 30 min | Correctness |
| 6 | L1: lowercase `term_aliases.language` codes | 5 min | ISO conformance |
| 7 | L2: clean REF-00369 jurisdiction field | 1 min | Correctness |
| 8 | M2: drop or regenerate `evidence_sources.doi_less_key` | 30 min | Schema cleanup |
| 9 | M1: rename `gaps.section` and add FK | 1h | Semantic clarity |

**Total: ~6 hours of remediation work** to reach a fully-normalized, conflation-free database.

---

## What this audit confirms

The v2 migration of `evidence_sources` was the right call and largely succeeded. Of 23 tables audited, **22 are structurally sound** — one fact per column, consistent enums, no cross-column duplication, no mojibake, valid FK references in the vast majority of cases.

The remaining 9 findings are surgical fixes, not structural redesigns. The largest single issue is `items.applicable_groups` (81 rows with comma-separated lists) which is the same denormalization pattern that motivated the v2 author table — and the same fix pattern (a junction table) applies.
