# Metadata Reconciliation + DOI Resolution Report — 2026-05-11

**Session:** session_2026-05-11-metadata-reconciliation
**Scope:** (1) Consolidate metadata from 5 parallel stores into canonical DB; (2) Run CrossRef DOI resolution; (3) Fix infrastructure bug in GitHub Action
**PI version:** v10.8
**Workplan phase:** Pre-Phase-B foundational data consolidation

---

## 1. Problem: five parallel metadata stores, never reconciled

| Source | Format | Entries | DOIs | PMIDs | Verification |
|---|---|---|---|---|---|
| `data/guidebook.db` (canonical) | SQLite `evidence_sources` | 675 | 30 | 5 | 32 VERIFIED |
| `data/db/guidebook.db` (Action) | SQLite `evidence_source` | 532 | 56 | — | — |
| `bibliography-v11-draft.md` | Markdown | ~446 | 74 | 48 | — |
| `global-reference-registry.json` | JSON | 531 | 56 | 41 | metadata_quality |
| `tier*-verified-sources.json` (×6) | JSON | 551 | 108 | 59 | 498 VERIFIED |

**Infrastructure bug:** The GitHub Action `resolve-dois.yml` wrote to `data/db/guidebook.db` (table `evidence_source`, singular). The canonical DB is `data/guidebook.db` (table `evidence_sources`, plural). Different schemas, non-matching ref_ids. Action results from 2026-05-07 never reached the canonical DB.

---

## 2. What was done

### Step 1: Flat-file reconciliation (451 updates)

Content-based matching (first-author + year, falling back to first-author + title prefix) across all 5 sources. Only NULL/empty fields populated; no overwrites.

- **92 DOIs** imported (8 later removed as junk → net 84)
- **62 PMIDs** imported
- **49 metadata_quality** upgrades (AUTHOR-TITLE-ONLY → COMPLETE)
- **248 verification_status** upgrades (NULL → VERIFIED)

DOI quality fixes: 3 truncated DOIs nulled (`10.1016/j`), 4 GREY notes removed from DOI field, 1 Korea Science ID moved to notes, 3 unclosed parens fixed.

### Step 2: CrossRef DOI resolution (76 verified DOIs)

Ran fixed `resolve_dois.py` against the reconciled DB (MAX_RESOLVE=300).

- **Phase 1 (PMID→DOI via NCBI):** 0 resolved (NCBI blocked by egress proxy — 403)
- **Phase 2 (CrossRef title search):** 100 candidates resolved
- **Audit:** 25 false positives identified and reverted (duplicate DOIs assigned to wrong refs, author-TBC entries, no-year entries)
- **Net retained:** 76 verified DOIs

### Step 3: Infrastructure fix

- `scripts/resolve_dois.py` — changed table `evidence_source` → `evidence_sources`, default DB path `data/db/guidebook.db` → `data/guidebook.db`, added `pmid` column check for Phase 1, added `updated_at`/`updated_by_session` tracking
- `.github/workflows/resolve-dois.yml` — changed `GUIDEBOOK_DB_PATH` env var, changed `git add` target

---

## 3. Final state

| Metric | Before | After | Change |
|---|---|---|---|
| DOI populated | 30 (4%) | 190 (28%) | +160 |
| PMID populated | 5 (1%) | 67 (10%) | +62 |
| metadata_quality = COMPLETE | 18 (3%) | 67 (10%) | +49 |
| metadata_quality = AUTHOR-TITLE-ONLY | 567 (84%) | 518 (77%) | −49 |
| verification_status = VERIFIED | 32 (5%) | 280 (41%) | +248 |
| verification_status = NULL | 642 (95%) | 394 (58%) | −248 |
| Synthesis-eligible (rule #10) | ~14 (2%) | 47 (7%) | +33 |

5 duplicate DOIs remain — these are genuine DB duplicates (same paper under different ref_ids), flagged for Phase B deduplication.

---

## 4. Phase B workplan impact

| Sub-task | Original scope | After this session | Saved |
|---|---|---|---|
| B.2 (AUTHOR-TITLE-ONLY resolve) | 567 × 15 min = 140h | 518 remaining | ~12h |
| B.7 (verification_status) | 642 × 10 min = 110h | 394 remaining | ~41h |
| **Combined** | **~250h** | | **~54h** |

**Key structural insight:** 213 sources are VERIFIED but not COMPLETE. They need DOI/journal resolution but NOT existence verification. Phase B.2 and B.7 can be decoupled for this subset.

---

## 5. Remaining action items

1. **Re-run Action in GitHub UI** — the fixed workflow can now be dispatched with `max_resolve: 500` to resolve more DOIs. NCBI Phase 1 will work from GitHub (not blocked by egress proxy).
2. **Deprecate `data/db/guidebook.db`** — no longer needed. Archive or delete.
3. **Flag 5 duplicate ref_ids** for Phase B deduplication.
4. **28 PMID-bearing sources still lack DOIs** — NCBI resolution blocked in container; will resolve when Action runs from GitHub.

---

## 6. Commits

| SHA | File | Message |
|---|---|---|
| c0f8bb2fe9ab | `data/guidebook.db` | First reconciliation pass (451 updates) |
| 4ec50bf39995 | `data/guidebook.db` | + CrossRef resolution (76 DOIs) + audit cleanup |
| 1bb96b69b209 | `scripts/resolve_dois.py` | Fix table name + DB path |
| c2fc557fc358 | `.github/workflows/resolve-dois.yml` | Fix DB path |
| bccb09435f52 | `references/audits/metadata-reconciliation-report-2026-05-11.md` | Initial report |
| 1cb41479bf2a | `references/audits/reconciliation-manifest-2026-05-11.json` | Audit trail |
