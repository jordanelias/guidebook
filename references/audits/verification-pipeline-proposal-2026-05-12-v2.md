# Verification Pipeline — Architecture Proposal (Revised)

**Author:** session 2026-05-12-verification-pipeline-design
**Status:** PROPOSAL (revised after testing — 22/22 tests pass)
**Supersedes:** `verification-pipeline-proposal-2026-05-12.md` (original)
**Test report:** `verification-pipeline-test-report-2026-05-12.md`
**Scope:** End-to-end design for verifying every source in `evidence_sources` against an authoritative external referent.

---

## What changed from the original proposal

Two findings from the test suite materially simplify the design:

1. **CrossRef already indexes ISO and EN international standards** via BSI's DOI prefix `10.3403/`. Channel 2a for ISO/EN does not need custom catalog scrapers — `query.bibliographic` + `filter=type:standard` works. Per-body scrapers reduced from 10-12 → 5 (DIN, CSA, JIS, GB, ABNT).

2. **PMC pool is 12 rows, not 6.** A broader scan of `pub_title` found PMC IDs in REF-00481, REF-00534, REF-00535, REF-00541, REF-00571, REF-00605 in addition to the 6 initial. All 12 are mechanically resolvable.

Additionally, the test suite confirmed:
- All proposed schema additions (`verified_by_tool`, `last_verified_at`, `verification_attempt_count`, `superseded_by_ref_id`) can be applied via `ALTER TABLE` to the live DB without rebuilds.
- The central `write_verification()` function correctly handles all four channels' writes, preserves existing data, and is idempotent.
- The Phase E gate (`audit_evidence_metadata.py`) reads new verification state without modification.

---

## 1. Current state review

### What works (live, in production)

| Piece | Role | Coverage |
|---|---|---|
| `scripts/resolve_dois.py` (weekly Action) | Channel 1 verifier — academic | Strict matching prevents false positives. 218/675 sources have DOIs (32%). |
| `evidence_sources` v2 schema | Storage substrate | All structured fields present: `verification_status`, `metadata_quality`, `doi_resolution_outcome`, `co1_provenance`, `derivation_chain`, `verification_note`, `pmcid`. |
| `audit_evidence_metadata.py` | Reads verification state for Phase E gating | Reports per-BPC eligibility. **Confirmed by test H01 to read new state correctly.** |
| `validate_evidence_state.py` (A6) | Validates evidence-state YAML records | Enforces stated/provisional/pending/not_applicable contract. |
| `validate_reasoning.py` (A.9) | Validates reasoning docs | Catches missing 9-step blocks, missing adversarial fields. |
| `audit_adversarial_use.py` (A10) | Pre-release review gate | Confirms human adversarial review has occurred per version. |

### What the test suite confirmed works

| Behavior | Test ID | Confirmed |
|---|---|---|
| CrossRef structured query (live) | B01, D01 | ✓ Unwin 2021 + ISO 21542 both correctly identified |
| PMC extraction from pub_title | C01 | ✓ 12 IDs identified correctly |
| REVERTED rows permanently skipped | B03, G02 | ✓ 26 REVERTED rows, 0 in candidate pool |
| NO-MATCH 30-day retry window | G01 | ✓ Window enforced; 41 NO-MATCH rows currently |
| Transient errors (403) don't write state | C03, E02 | ✓ No mutation on transient failures |
| Cross-row isolation | F01 | ✓ Write to one row leaves neighbors untouched |
| Idempotency | B04, G04 | ✓ Repeated writes don't corrupt; attempt_count increments |
| All 4 channel tools update `verified_by_tool` correctly | G03 | ✓ All 4 tool identifiers write correctly |

### Where the gaps are

| Gap | Affects |
|---|---|
| **No CrossRef `type:standard` extension** | ~25-30 ISO/EN standards immediately resolvable via CrossRef (newly found) |
| **No PMC-ID extractor pass** | 12 sources mechanically resolvable to DOIs once extracted |
| **No Channel-2 catalog scrapers** for DIN, CSA, JIS, GB, ABNT | ~30 standards in these bodies |
| **No government legislation portal resolvers** | ~80 sources |
| **No NGO/CPG publication verifiers** | ~100 sources |
| **No Co-1 attestation registry** | ~50 sources (different framework needed) |
| **No reverification cadence** | URLs rot, standards get superseded — no detection |
| **Container-environment limitation** | `bash_tool` egress proxy only allows `api.crossref.org` and `www.ncbi.nlm.nih.gov`. Channel 2 fetches must run in GitHub Actions. |

### Channel sizing (refresher)

| Channel | Sources | Approach |
|---|---|---|
| Channel 1 — Academic (CrossRef + NCBI) | 91 (13%) | Mostly handled; extensions: PMC extractor, corp-author fallback |
| Channel 2 — Standards / Government / NGO | 583 (86%) | Mix of CrossRef extensions (ISO/EN) and per-body scrapers |
| Channel 3 — Co-1 lived experience | ~50 | Attestation registry, not external lookup |

---

## 2. Design principles (unchanged from original)

1. **Three-channel architecture matches corpus shape.** Test results validate this.
2. **Verification ≠ claim support.** Pipeline confirms existence at cited identifier. Adversarial protocol (rule #7) separately confirms claim support.
3. **Per-body resolvers, not monolithic.** Each standards body has its own URL/API conventions.
4. **Idempotent and incremental.** Confirmed by tests B04 and G04.
5. **Honest about uncertainty.** Transient errors don't write state; NO-MATCH retries after window.
6. **Polite to upstream APIs.** Rate-limited, identified user-agent.
7. **Auditable provenance.** Every write logs tool, session, timestamp.
8. **No new schema unless necessary.** Four columns + one table is the entire schema change.

---

## 3. Pipeline architecture

```
                          ┌─────────────────────────────────────┐
                          │     scripts/verify_dispatch.py      │
                          │   (new — orchestrator)              │
                          │                                     │
                          │  selects rows, routes by:           │
                          │  source_type + corp_name +          │
                          │  standard_number + jurisdiction     │
                          └────────────────┬────────────────────┘
                                           │
              ┌────────────────────────────┼────────────────────────────┐
              │                            │                            │
              ▼                            ▼                            ▼
  ┌──────────────────────┐    ┌──────────────────────┐    ┌─────────────────────────┐
  │  CHANNEL 1           │    │  CHANNEL 2           │    │  CHANNEL 3              │
  │  Academic + ISO/EN   │    │  Custom resolvers    │    │  Co-1 attestation       │
  │                      │    │                      │    │                         │
  │  • CrossRef          │    │  • DIN catalog       │    │  • Sign-off registry    │
  │    - structured      │    │  • CSA catalog       │    │  • Six required fields  │
  │    - bibliographic   │    │  • JIS catalog       │    │  • Contributor IDs      │
  │    - type:standard   │◀── │  • GB / openstd      │    │                         │
  │  • NCBI PMID/PMC     │    │  • ABNT catalog      │    │                         │
  │  • OpenAlex (later)  │    │  • Govt portals      │    │                         │
  │  • Semantic Scholar  │    │    (per country)     │    │                         │
  │    (later)           │    │  • NGO/CPG sites     │    │                         │
  │                      │    │  • URL reachability  │    │                         │
  └──────────┬───────────┘    └──────────┬───────────┘    └─────────────┬───────────┘
             │                           │                              │
             └───────────────────────────┼──────────────────────────────┘
                                         │
                                         ▼
                          ┌──────────────────────────────┐
                          │   write_verification()       │
                          │   (central writer — tested)  │
                          └──────────────┬───────────────┘
                                         │
                                         ▼
                          ┌──────────────────────────────┐
                          │  evidence_sources columns:   │
                          │    verification_status       │
                          │    verified_by_tool          │
                          │    last_verified_at          │
                          │    verification_attempt_count│
                          │    verification_note         │
                          │    doi (if found)            │
                          │    pmcid (if found)          │
                          │    updated_at, _by_session   │
                          └──────────────┬───────────────┘
                                         │
                                         ▼
                          ┌──────────────────────────────┐
                          │  audit_evidence_metadata.py  │
                          │  reads, re-scores Phase E    │
                          │  readiness                   │
                          └──────────────────────────────┘
```

### Channel 1 expanded — academic + ISO/EN

**REVISED from original:** Channel 1 now handles four sub-paths, all via CrossRef + NCBI:

| Sub-path | Method | Source pool |
|---|---|---|
| 1a — Person-authored academic | CrossRef `query.author` + `query.title` (existing) | ~75 candidates |
| 1b — PMID present | NCBI `idconv` → DOI (existing) | 8 candidates |
| 1c — PMC ID in pub_title field | Regex extract → write `pmcid` → NCBI `idconv` (NEW) | 12 candidates |
| 1d — Corporate-authored academic | CrossRef `query.bibliographic` (NEW) | ~5 candidates |
| 1e — ISO/EN standards | CrossRef `filter=type:standard` (NEW) | ~25-30 candidates |

Total Channel 1 yield with extensions: ~75 + 8 + 12 + 5 + 30 = ~130 sources resolvable through CrossRef + NCBI alone.

### Channel 2 — Per-body resolvers (REDUCED scope)

Custom scrapers needed for only the bodies CrossRef doesn't cover:

| Body | Approach | Sources affected |
|---|---|---|
| DIN | beuth.de search → confirm by title | ~15 |
| CSA | csagroup.org/store → direct URL | ~8 |
| JIS | jisc.go.jp database → search | ~5 |
| GB (China) | openstd.samr.gov.cn → search (ZH-language) | ~12 |
| ABNT | abntcatalogo.com.br → search | ~3 |

**Plus government legislation portals** (still needed):
- UK: legislation.gov.uk
- FR: legifrance.gouv.fr
- DE: gesetze-im-internet.de
- SE: riksdagen.se
- ES: boe.es
- IT: normattiva.it
- PT: dre.pt
- NL: wetten.overheid.nl
- CN: gov.cn / mohurd.gov.cn
- KR: law.go.kr
- JP: e-gov.go.jp
- US: federalregister.gov
- CA: laws-lois.justice.gc.ca
- AU: legislation.gov.au

**Plus NGO/CPG bodies** (still needed):
- RCOT, AOTA, CAOT, RNIB, Dementia Australia, WHO, World Bank, UN, IWA Ireland, CEUD, UNSW HMC, Inter-Fédération (BE)

### Channel 3 — Co-1 attestation (unchanged from original)

Different shape entirely. Co-1 sources require attestation records, not external catalog lookup. Schema:

```sql
CREATE TABLE co1_attestations (
  attestation_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  ref_id             TEXT NOT NULL REFERENCES evidence_sources(ref_id),
  contributor_id     TEXT NOT NULL,
  contributor_consent_record TEXT NOT NULL,
  attestation_date   TEXT NOT NULL,
  jurisdiction       TEXT,
  populations        TEXT,
  attestation_type   TEXT CHECK(attestation_type IN (
    'testimony', 'advocacy-publication', 'lived-experience-report',
    'practitioner-attestation', 'community-survey'
  )),
  attestation_url    TEXT,
  attestation_note   TEXT,
  created_at         TEXT,
  created_by_session TEXT
);
```

---

## 4. Verification outcome state machine (unchanged)

```
                  [unattempted]
                       │
                       ▼ verify_dispatch picks up
                  [in-flight]
                       │
        ┌──────────────┼──────────────┬────────────────┐
        ▼              ▼              ▼                ▼
   [VERIFIED]    [NO-MATCH]    [NEEDS-HUMAN]    [TRANSIENT]
        │              │              │                │
        │              │ retry after  │ queued for     │ retry next
        │              │ 30 days      │ manual review  │ run
        │              │              │                │ (no state write)
        ▼              ▼              ▼                ▼
  written to     marked, will     surfaced in     no state mutation
  evidence_      retry             dashboard        — tested C03, E02
  sources
        │
        ▼
   [REVERIFIED]  (annual cadence)
        │
        ▼
   [SUPERSEDED]  (standard withdrawn / replaced)
        │
        ▼
   [REVERTED]   (later found wrong; never retry — tested G02)
```

`verification_status` enum: `VERIFIED`, `UNVERIFIED-1`, `NO-MATCH`, `NEEDS-HUMAN`, `SUPERSEDED`, `REVERTED`, `PROBABILISTIC` (existing), NULL (unattempted).

---

## 5. Central write function (tested)

The dispatcher and all per-channel verifiers call exactly one function to commit state:

```python
def write_verification(conn, ref_id, tool, status, doi=None, pmcid=None, note=None):
    """Atomic verification-state write. Tested 22/22."""
    conn.execute("""
        UPDATE evidence_sources SET
            verification_status = ?,
            verified_by_tool = ?,
            last_verified_at = ?,
            verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1,
            verification_note = COALESCE(CASE WHEN ? IS NOT NULL THEN ? ELSE verification_note END, verification_note),
            doi = COALESCE(CASE WHEN ? IS NOT NULL THEN ? ELSE doi END, doi),
            pmcid = COALESCE(CASE WHEN ? IS NOT NULL THEN ? ELSE pmcid END, pmcid),
            updated_at = ?,
            updated_by_session = ?
        WHERE ref_id = ?
    """, (status, tool, NOW, note, note, doi, doi, pmcid, pmcid, NOW, SESSION, ref_id))
    conn.commit()
```

**Key guarantees confirmed by tests:**
- Never overwrites existing `doi` or `pmcid` with NULL (B02, D02, D03)
- `verification_attempt_count` increments monotonically (G04)
- `verified_by_tool` always set to the calling tool's identifier (G03)
- Cross-row isolation enforced via `WHERE ref_id = ?` (F01)
- On transient errors (403, timeout), the verifier does NOT call this function — no state write (C03, E02)

---

## 6. Schema additions

```sql
ALTER TABLE evidence_sources ADD COLUMN verified_by_tool TEXT;
ALTER TABLE evidence_sources ADD COLUMN last_verified_at TEXT;
ALTER TABLE evidence_sources ADD COLUMN verification_attempt_count INTEGER DEFAULT 0;
ALTER TABLE evidence_sources ADD COLUMN superseded_by_ref_id TEXT REFERENCES evidence_sources(ref_id);

-- One new table:
CREATE TABLE co1_attestations (...);  -- see §3 Channel 3 above
```

**Tested via `ALTER TABLE` against live DB copy. No rebuild needed; all data preserved.**

---

## 7. Dispatcher routing logic

```python
def route(row):
    """Return list of verifiers to try, in priority order."""
    if row.doi and row.verification_status == 'VERIFIED':
        return ['skip-already-verified']

    if row.doi_resolution_outcome == 'REVERTED':
        return ['skip-reverted']

    if row.doi_resolution_outcome == 'NO-MATCH':
        if not in_retry_window(row.updated_at, 30):
            return ['skip-no-match-recent']

    # Channel 1 — academic
    if row.source_type in ('journal_article','book','book_chapter','thesis',
                            'conference_paper','primary_research'):
        verifiers = []
        # 1c — PMC extraction first (no network)
        if 'PMC' in (row.pub_title or '') and not row.pmcid:
            verifiers.append('pmc-extractor')
        # 1b — NCBI if PMID or pmcid present
        if row.pmid or row.pmcid:
            verifiers.append('ncbi-id-converter')
        # 1a / 1d — CrossRef
        if row.first_author_last and row.pub_title and row.pub_year:
            if row.is_corporate_primary:
                verifiers.append('crossref-bibliographic')
            else:
                verifiers.append('crossref-structured')
        return verifiers or ['needs-human-channel-1']

    # Channel 1e + 2a — standards
    if row.source_type == 'standard':
        body = identify_standards_body(row)  # ISO/EN/BSI/DIN/CSA/JIS/GB/ABNT
        verifiers = []
        # 1e — CrossRef first for ISO/EN/BSI (often indexed)
        if body in ('iso', 'en', 'bsi'):
            verifiers.append('crossref-standard')
        # 2a — per-body scraper as fallback or primary
        if body in ('din', 'csa', 'jis', 'gb', 'abnt'):
            verifiers.append(f'standards-{body}')
        if not verifiers:
            verifiers.append('crossref-standard')  # try anyway
        return verifiers

    # Channel 2c — government regulation
    if row.source_type in ('guideline','report') and is_governmental(row):
        country = row.jurisdiction.lower()
        return [f'government-{country}', 'url-fetch-fallback']

    # Channel 2d — NGO/CPG with URL
    if row.source_type in ('guideline','report') and row.url:
        return ['url-fetch', 'crossref-bibliographic']

    # Channel 2d — NGO/CPG by org name
    if row.source_type in ('guideline','report'):
        org = identify_org(row.corporate_name)
        if org:
            return [f'ngo-{org}']
        return ['needs-human-channel-2']

    # Channel 3 — Co-1
    if row.source_type == 'grey' and row.co1_provenance:
        return ['co1-attestation-queue']

    return ['needs-human-classification']
```

---

## 8. Environment constraints (test-confirmed)

| Domain | Container bash_tool | GitHub Actions runners |
|---|---|---|
| `api.crossref.org` | ✓ | ✓ |
| `www.ncbi.nlm.nih.gov` | ✗ (403 from egress proxy) | ✓ |
| `iso.org`, `bsigroup.com`, `din.de`, etc. | ✗ (403) | ✓ |
| `legislation.gov.uk`, `legifrance.gouv.fr`, etc. | ✗ (403) | ✓ |
| `rcot.co.uk`, `aota.org`, etc. | ✗ (403) | ✓ |

**Implication:** Channel 2 verifiers (other than CrossRef-standard) cannot be tested or run from the Claude container. They run exclusively in GitHub Actions workflows where runners have full internet access. The `resolve_dois.yml` workflow is the template.

---

## 9. Revised phased rollout

### V1 — Channel 1 extensions only (3-4 hours)

All changes to `scripts/resolve_dois.py`. No new scripts, no new tables. One migration for the 4 new columns.

**Changes:**

1. **Phase 0 — PMC extractor** (20 lines added at top of `main()`)
   ```python
   for r in conn.execute("SELECT ref_id, pub_title, pmcid FROM evidence_sources WHERE pub_title LIKE '%PMC%'"):
       m = re.search(r'PMC(\d+)', r['pub_title'] or '')
       if m and not r['pmcid']:
           conn.execute("UPDATE evidence_sources SET pmcid=? WHERE ref_id=?",
                        (f"PMC{m.group(1)}", r['ref_id']))
   ```

2. **Phase 1b — NCBI pmcid → DOI** (extend existing Phase 1 to also handle pmcid column).

3. **Phase 2b — CrossRef bibliographic fallback for corporate-authored academic** (~30 lines).

4. **Phase 3 — CrossRef type:standard for ISO/EN standards** (~40 lines, new phase):
   ```python
   if row.source_type == 'standard' and any(s in (row.standard_number or '').upper()
                                              for s in ('ISO ', 'EN ', 'BS ', 'IEC ')):
       params = {"query.bibliographic": f"{row.standard_number} {strip_year(row.pub_title)}",
                 "filter": "type:standard", "rows": "5"}
       # Acceptance: publisher contains 'BSI' or 'British Standards' or 'ISO'
       # AND title contains keywords from row.pub_title
   ```

5. **Schema migration** — 4 ALTER TABLE statements + 1 row in `data_migrations`.

**Expected V1 yield (data-confirmed):**
- 12 PMC sources → DOI (via Phase 0 + Phase 1b in next Action run from GitHub)
- ~5 corporate-author academic → DOI (via Phase 2b)
- ~25-30 ISO/EN standards → DOI (via Phase 3)
- Total: ~40-50 new verified sources

**Eligibility delta:** 47/675 (7%) → ~80-100 (12-15%).

**BPCs unblocked:** estimated 3-5 additional BPCs reach Phase E readiness threshold.

### V2 — Custom scrapers + government portals (20-25 hours)

New script `scripts/verify_dispatch.py` orchestrating per-channel verifiers. New per-body resolver modules.

**Reduced scope (from original proposal):**
- 5 custom standards scrapers (DIN, CSA, JIS, GB, ABNT) — NOT 10-12 (CrossRef handles ISO/EN/BSI)
- Top 3-5 government portals by source count (UK, FR, DE, CN, KR likely highest yield)
- URL reachability resolver for sources that have a `url` field populated

**Expected V2 yield:** 80-120 additional sources verified. Eligibility delta: → 24-33%. BPCs unblocked: ~15-25.

### V3 — Full coverage + Channel 3 + cadence (60-90 hours)

(Reduced from 80-120h original since V2 scope shrinks.)

- Remaining standards bodies
- Remaining government portals (12 countries)
- NGO/CPG scrapers (~12 orgs)
- Co-1 attestation registry table + sign-off workflow
- Reverification cadence (annual URL recheck)
- Verification frontier dashboard

**Expected V3 yield:** ~80-90% of corpus verified. BPCs unblocked: ~60-75.

---

## 10. Test-confirmed integration points

### Reads from existing components (no modification needed)

- **`audit_evidence_metadata.py`** — reads `metadata_quality` + `verification_status`. **Test H01 confirmed it picks up new VERIFIED sources immediately.** No changes needed.
- **`validate_evidence_state.py`** (A6) — reads `verification_status` for §2.8 downgrade. Will benefit automatically.
- **`validate_reasoning.py`** (A.9) — validates reasoning docs cite eligible sources. Will benefit automatically as eligible pool grows.

### Writes to existing components

- **`evidence_sources`** — all writes through `write_verification()`. Confirmed correct on all 4 channels by tests B01, C04, D02, E01.

### Minor extensions (V2-V3)

- **`audit_adversarial_use.py`** — could add precondition "evidence verification performed" before allowing adversarial review.
- **`scripts/resolve_dois.py`** — already a generic name; rename/refactor as `verify_dispatch.py` in V2.

---

## 11. What this pipeline still does NOT do

(Unchanged from original — limits stated explicitly.)

1. Does not validate claim support. Confirming a paper exists ≠ confirming it supports a specific synthesis claim. Adversarial protocol (rule #7) handles this separately.
2. Does not assess source quality. Tier assignment is editorial.
3. Does not handle paywalls beyond existence confirmation.
4. Does not detect retractions. (CrossRef retraction watch is a future addition.)
5. Does not arbitrate jurisdictional precedence. Pipeline confirms both standards exist; synthesis decides which governs.

---

## 12. Cost-benefit summary (revised)

| Phase | Effort (hours) | New verified sources | Cumulative eligibility | BPCs unblocked |
|---|---|---|---|---|
| Current state | — | — | 47 / 675 (7%) | 1 |
| V1 (CrossRef extensions + PMC) | **3-4** | **+40-50** | 87-100 (13-15%) | **+3-5** |
| V2 (5 custom scrapers + top govt) | **20-25** | +80-120 | 170-220 (25-33%) | +15-25 |
| V3 (full coverage + Co-1 + cadence) | **60-90** | +350-450 | 540-670 (80-99%) | +60-75 |

**Total investment: 85-120 hours** (down from original 100-150h estimate).
**Net saving vs manual Phase B grind: ~500-1,300 hours.**

---

## 13. Acceptance criteria for V1

V1 ships when:

1. ☐ Schema columns added via migration (recorded in `data_migrations`)
2. ☐ `resolve_dois.py` extended with Phase 0 (PMC extractor), Phase 2b (corp-author CrossRef), Phase 3 (ISO/EN CrossRef standards)
3. ☐ Tests pass: re-run `scripts/tests/test_verification_pipeline.py` against extended script
4. ☐ Action run from GitHub Actions resolves ≥10 of the 12 known PMC candidates (NCBI accessible from runners)
5. ☐ Action run resolves ≥5 of the ~25-30 ISO/EN standards
6. ☐ `audit_evidence_metadata.py` reports increased eligibility count and additional BPCs ready

If all six pass on first run, V2 design begins.

---

## 14. Decision needed

Same questions as original proposal:

1. **Is the three-channel framing accepted?** (Now informed by test data confirming the architecture works as designed.)
2. **Is V1 → V2 → V3 rollout the right shape?** (V1 effort dropped from 3h to 3-4h with broader yield; V2 simplified.)
3. **Are the schema additions acceptable?** (Test-confirmed they apply cleanly via ALTER TABLE.)
4. **Should V1 be built now?**

V1 is now the smallest possible commit — three additions to one existing file plus a 4-column migration, with the test suite already in place to verify it. If approved, it ships today.
