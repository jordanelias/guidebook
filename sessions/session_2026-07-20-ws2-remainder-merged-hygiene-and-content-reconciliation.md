# Session — WS2 remainder: MERGED-stale hygiene + DB-sync-gap content reconciliation
**Date:** 2026-07-20
**Branch:** `claude/multilingual-multi-jurisdictional-research-0ilfpm`

## Task
"Do the remaining WS2 items thoroughly." After the six RETRACTED-PRE-REHAB slices (PRs #34, #35), the
plan's WS2 (Finding 4) still listed six "un-started" slugs — all ACTIVE with 0 `source_slug_links`. On
inspection they split cleanly into two groups, neither of which was a genuine from-zero research gap.

## Group A — MERGED-stale (data hygiene, not research)
Three slugs are **redirect-only** — their BPC files already declare a `MERGED — 2026-03-28` redirect, but
`slugs.status` was never flipped from ACTIVE, so the audit kept counting them as un-started empty slices:
- `chronic-pain-built-environment` → `pain-ofs-built-environment-design`
- `fatigue-spectrum-built-environment` → `pain-ofs-built-environment-design`
- `hearing-impairment-built-environment` → `deaf-acoustic-built-environment`

Verified both merge targets are ACTIVE and carry real evidence (12 and 10 links). Fixed by:
1. Migration: `slugs.status='MERGED'`, `merged_into=<target>` for the 3 (the DB now matches the BPC files).
2. `tools/evidentiary_audit.py`: added `WHERE status='ACTIVE'` to the slice query — a MERGED redirect must
   not be graded as an empty slice. Audit scope 82 → **79 ACTIVE slices**.

## Group B — DB-sync gap (real content, 0 links)
Three slugs carried substantial **cited markdown** but **0 `source_slug_links`** — documented, never (fully)
ingested. Reconciled each by matching the documented sources to the corpus (DOI/PMID/author-year), linking
what exists, and ingesting the PubMed-verifiable sources that were genuinely absent:

| slug | links | audit | what was done |
|---|---|---|---|
| `economics-sources` | 23 | F → **C (62.6)** | 18 net-new economics/home-mod sources ingested (`REF-00884`–`REF-00901`) + 5 in-corpus linked |
| `government-grant-programmes` | 4 | F → **D** | linked the PubMed-verified grant-economics anchors (Keall HAPPI, CAPABLE, Clemson SR) |
| `accessible-design-failures-poor-performance` | 4 | F → **E†** | linked the Zallio & Clarkson POE-deficit trio + Rodríguez-Labajos 2024 |

**The 18 net-new economics sources** (falls-prevention / home-modification cost-effectiveness RCTs + one
Cochrane SR) were each confirmed via a real **PubMed** call — `get_article_metadata` on the PMID documented
in `economics-sources.md`, with Szanton 2017 (PMID 29165789) and the Tsuchiya-Ito DOIs additionally resolved
via `convert_article_ids`. Canonical PubMed metadata was used verbatim (title/journal/vol/pages/first author).
Clemson 2023 (Cochrane SR) tiered **T2 sr_meta**; the rest **T3 clinical** (economic evaluations informing
cost-effectiveness, not a specific BE design parameter). Jurisdictions span NZ, AU, US, UK, SE, INT.

## Result / verification
- `PRAGMA foreign_key_check` + `integrity_check`: **clean**. No duplicate DOIs/PMIDs (18 new deduped against
  corpus by DOI+PMID+author-year; 2 candidates that were already in-corpus were linked, not re-ingested).
- `tools/evidentiary_audit.py`: **corpus F-count 6 → 0** — every ACTIVE slice is now graded E or better
  (A:8 B:18 C:24 D:18 E:11 across 79 slices). 948 sources.
- `tools/regenerate_vetting_surface.py`: **0 orphans**, 79 topics, 948 sources.

## Not done / honest limits
- **Documented economics backlog (real, verifiable, deferred — not yet in the DB):** Tsuchiya-Ito 2022/2023/2024
  (Japan LTC), Fänge & Iwarsson 2005 (Sweden), Carnemolla 2019/2020, Mackintosh 2020, Hutchinson 2025, González
  Alonso 2024, Chandola 2022, Ielegems 2019; and for accessible-design-failures: Mazumdar & Geis 2002 (JAPR),
  Slaug et al. 2025, Oslo Economics 2018/2023. These are named in the BPC banners; a dedicated economics ingest
  pass (with full metadata capture) is the right home for them, rather than rushing them in without canonical
  metadata this session.
- No `best_practice_synthesis` written (Opus floor); the content slices remain PARTIAL, not closed.
- `scripts/validate_db.py` still fails on the pre-existing `doi_less_key` column drift (unchanged, unrelated).

**WS2 status:** with this batch, every WS2 slug — the 13 originally flagged empty — is now either re-derived
(PARTIAL with a verified base), correctly MERGED, or carries a documented backlog. Corpus F-count is 0.
