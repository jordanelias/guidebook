# Ecosystem Audit — Resolution Summary
**Date:** 2026-05-10
**Commits:** `768ecb78` (audit + C2), `353101c8` (C1 + S1 + minor)

## Resolved This Session

| Finding | Action | Result |
|---|---|---|
| C1: 701 FK violations (source_slug_links) | Identified as duplicate rows (local_ref_id inserted as ref_id alongside valid global ref_id). Deleted 701 duplicates. | **0 FK violations** |
| C2: 16 bpc_metadata orphans | Deleted 16 population/utility rows without slug entries | Clean |
| S1: 30 non-standard jurisdiction codes | Normalized compound codes, fixed language-as-jurisdiction errors, mapped regional groups to INT | 33 clean jurisdiction codes |
| Minor: 3 targetless connections | Deleted CON-0033/0034/0035 | Clean |

## Known Remaining

| Finding | Status | Action needed |
|---|---|---|
| C3: 91/91 items.bpc_source_slug NULL | Deferred to CO-0009 | Requires domain-specific item→slug mapping |
| S3: 3 empty tables (citation_mining, conflicts, decisions) | Schema present, data not migrated | citation_mining is a pipeline not yet started; conflicts could be populated from cross-pop BPC; decisions are governance records |
| 1 NULL-tier evidence source (REF-00257) | Internal reference (case-study-compendium) | Leave as-is — not a peer-reviewed source |
| 12 unlinked evidence_sources (REF-VERIFIED-*) | Added during verification passes, not yet slug-linked | Link when relevant slugs are identified |
| 11/30 terms with no item_links | Terms exist but not mapped to items | Part of CO-0009 |
| 1 lost source link (TBE-03) | Deleted with orphans — no global ref existed | Re-add when thermoregulation BPC is next updated |

## Post-Fix DB State

- **0 FK violations** (was 717)
- **19 tables, ~6,100 rows** (was ~6,400 — removed duplicates)
- **33 jurisdiction codes** (was 53 including non-standard)
- **14 languages, all producing results**
- **654 evidence sources, 379 at Tier 1-3 (58%)**

---
