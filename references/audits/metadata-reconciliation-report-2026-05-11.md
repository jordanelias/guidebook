# Metadata Reconciliation Report — 2026-05-11

**Session:** session_2026-05-11-metadata-reconciliation
**Scope:** Consolidate DOI, PMID, verification_status, and metadata_quality from 5 flat-file sources into `data/guidebook.db`
**PI version:** v10.8 (live as of this session)
**Workplan phase:** Pre-Phase-B — foundational data consolidation

---

## 1. Problem discovered

The project has accumulated five parallel stores of bibliographic metadata that were never reconciled into the canonical database (`data/guidebook.db`):

| Source | Format | Entries | DOIs | PMIDs | Verification data |
|---|---|---|---|---|---|
| `data/guidebook.db` (canonical) | SQLite, `evidence_sources` table | 675 | 30 | 5 | 32 VERIFIED |
| `data/db/guidebook.db` (Action target) | SQLite, `evidence_source` table | 532 | 56 | — | — |
| `references/bibliography-v11-draft.md` | Markdown | ~446 | 74 | 48 | — |
| `references/global-reference-registry.json` | JSON | 531 | 56 | 41 | metadata_quality |
| `references/tier*-verified-sources.json` (×6) | JSON | 551 | 108 | 59 | 498 VERIFIED |

The BPC rewrite workplan (Phase B) was scoped against `data/guidebook.db` alone. It estimated 140 hours for DOI resolution and 110 hours for verification — work partly already done in the flat files.

### Critical infrastructure bug

The GitHub Action `resolve-dois.yml` writes to `data/db/guidebook.db` using table `evidence_source` (singular). The canonical DB is `data/guidebook.db` using table `evidence_sources` (plural). The Action ran successfully twice (2026-05-07) but its results never reached the canonical DB. **These are two completely separate databases with different schemas and non-matching ref_ids.**

---

## 2. Reconciliation method

1. **Content-based matching** — ref_ids do NOT correspond across sources. Matching used first-author surname + year (exact), falling back to first-author + title prefix (5 words). Match types: `AY-UNIQUE` (74%), `AYT` (18%), `DOI` (existing match), `AT-UNIQUE` (remainder).

2. **Update rules** — only populate NULL/empty fields. Never overwrite existing values. verification_status only upgraded TO `VERIFIED`, never downgraded.

3. **DOI quality check** — 11 problematic DOIs found and fixed:
   - 3 truncated to `10.1016/j` → nulled (junk from DB2 CrossRef matching)
   - 4 GREY notes stored in DOI field → moved to `notes`, DOI nulled
   - 1 Korea Science ID (`JAKO...`) → not a DOI; nulled, ID preserved in title
   - 3 unclosed parens (`10.1044/...`) → closing paren appended

---

## 3. Results

| Metric | Before | After | Change |
|---|---|---|---|
| DOI populated | 30 (4%) | 114 (17%) | +84 |
| PMID populated | 5 (1%) | 67 (10%) | +62 |
| metadata_quality = COMPLETE | 18 (3%) | 67 (10%) | +49 |
| metadata_quality = AUTHOR-TITLE-ONLY | 567 (84%) | 518 (77%) | −49 |
| verification_status = VERIFIED | 32 (5%) | 280 (41%) | +248 |
| verification_status = NULL | 642 (95%) | 394 (58%) | −248 |
| Synthesis-eligible (rule #10) | ~14 (2%) | 47 (7%) | +33 |

451 individual field updates across 273 rows. Zero errors. All updates tagged with `updated_by_session = 'session_2026-05-11-metadata-reconciliation'`.

---

## 4. Phase B workplan impact

| Phase B sub-task | Original scope | After reconciliation | Hours saved |
|---|---|---|---|
| B.2 (AUTHOR-TITLE-ONLY → resolve) | 567 sources × 15 min = 140h | 518 remaining | ~12h |
| B.7 (verification_status) | 642 sources × 10 min = 110h | 394 remaining | ~41h |
| **Combined** | | | **~54h** |

**Key structural insight:** 213 sources are now VERIFIED but not COMPLETE. These need DOI/journal resolution (Phase B.2–B.5) but do NOT need existence verification (Phase B.7). The two phases can be decoupled and parallelized for these 213.

---

## 5. Remaining issues requiring action

### 5.1 Fix GitHub Action target (infrastructure bug)

`scripts/resolve_dois.py` + `.github/workflows/resolve-dois.yml`:
- **Current:** writes to `data/db/guidebook.db`, table `evidence_source` (singular)
- **Required:** write to `data/guidebook.db`, table `evidence_sources` (plural)
- **Action:** update `GUIDEBOOK_DB_PATH` default in script + workflow env var; update all SQL to use `evidence_sources`; deprecate `data/db/guidebook.db`

### 5.2 Re-run Action against reconciled DB

After fixing 5.1, re-run `resolve-dois.yml` with `max_resolve: 500`. The 518 remaining AUTHOR-TITLE-ONLY entries could yield ~100–200 more DOIs via CrossRef title search, further reducing Phase B.2 scope.

### 5.3 Consolidate or deprecate parallel stores

| File | Recommendation |
|---|---|
| `data/db/guidebook.db` | Deprecate after fixing Action target. Archive or delete. |
| `references/global-reference-registry.json` | Keep as read-only export. Generate from DB, not maintained independently. |
| `references/bibliography-v11-draft.md` | Keep as human-readable bibliography. Generate from DB for future versions. |
| `references/tier*-verified-sources.json` (×6) | Keep as audit trail. Do not add new data here — add to DB directly. |

### 5.4 evidence_type still 95% empty

None of the flat files carry `evidence_type` data. This remains fully Phase B.6 work (~55 hours). The tier classification from the JSON filenames (tier1 = clinical, tier3 = SR/meta) provides a signal but doesn't map cleanly to the 9-value `evidence_type` enum.

---

## 6. Provenance trail

All 451 updates carry:
- `updated_at = '2026-05-11 reconciliation'`
- `updated_by_session = 'session_2026-05-11-metadata-reconciliation'`

Full manifest: saved as `reconciliation_manifest.json` (451 entries with ref_id, field, new_value, source, match_type).
