# Verification Pipeline — Architecture Proposal

**Author:** session 2026-05-12-verification-pipeline-design
**Status:** PROPOSAL (not yet approved or built)
**Scope:** End-to-end design for verifying every source in `evidence_sources` against an authoritative external referent, replacing the current ad-hoc, Channel-1-only state with a tiered, idempotent pipeline.

---

## 1. Current state review

### What works

| Piece | Role | Coverage |
|---|---|---|
| `scripts/resolve_dois.py` (weekly Action) | Channel 1 verifier — academic | Handles 91/675 sources (13% of corpus). Strict matching prevents false positives. |
| `evidence_sources` v2 schema | Storage substrate | All structured fields present: `verification_status`, `metadata_quality`, `doi_resolution_outcome`, `co1_provenance`, `derivation_chain`, `verification_note`. |
| `audit_evidence_metadata.py` | Reads verification state for Phase E gating | Reports per-BPC eligibility. Reactive — doesn't drive new verification. |
| `validate_evidence_state.py` (A6) | Validates evidence-state YAML records | Enforces stated/provisional/pending/not_applicable contract; applies §2.8 downgrade. |
| `validate_reasoning.py` (A.9) | Validates reasoning docs against template | Catches missing 9-step parameter blocks, missing adversarial fields. |
| `audit_adversarial_use.py` (A10) | Pre-release review gate | Confirms human adversarial review has occurred per version. |

### Where the gaps are

| Gap | Affects |
|---|---|
| **No Channel-2 verifier** for standards, regulations, NGO/CPG, government reports | 583/675 sources (86%) — the majority of the corpus has no automated path to verification |
| **Corporate-authored academic items** skipped by Channel 1 | ~30-40 journal articles with org authors fall through CrossRef |
| **Title-paraphrase rows** correctly rejected by Channel 1 but not surfaced for human triage | ~150 sources where the `pub_title` field is BPC summary text |
| **PMC IDs hiding in title field** never extracted | At least 3 known; sampling suggests 10-20 total |
| **No Co-1 attestation registry** | Co-1 lived-experience sources need a different framework — not verifiable against an external catalog |
| **No verification provenance** beyond `updated_by_session` | Can't tell which tool verified a given row; can't bulk-revoke if a verifier was buggy |
| **No reverification cadence** | Once verified, never re-checked — but URLs rot, standards get superseded |

### The structural mismatch

Channel 1 (CrossRef + NCBI) is 14% of the verification need by source count. Channel 2 (standards/NGO/government catalogs) is 86%. The current pipeline is built for the smaller channel. Reversing this priority is the central design move of this proposal.

---

## 2. Design principles

1. **Two-channel architecture matches the corpus shape.** Don't try to extend CrossRef to do what it can't. Build a separate Channel 2 pipeline that knows about standards catalogs, government legislation portals, and NGO/CPG publication archives.

2. **Verification ≠ claim support.** This pipeline confirms a source *exists at the cited identifier*. It does not confirm that the source supports any specific synthesis claim made about it — that's the adversarial protocol's job (rule #7). The pipeline is a *necessary but not sufficient* gate for synthesis.

3. **Per-body resolvers, not a monolithic verifier.** Each standards body, government catalog, and large NGO has its own URL conventions and metadata shape. Trying to abstract these into a generic resolver loses too much information. Better: one small resolver per body, dispatched by a thin orchestrator.

4. **Idempotent and incremental.** Each verifier can be added independently. Re-running the pipeline doesn't re-verify confirmed sources. New verifiers don't break existing data.

5. **Honest about uncertainty.** When a verifier can't confidently confirm, mark `NEEDS-HUMAN-REVIEW` rather than guessing. The skip logic from `resolve_dois.py` is the model: NO-MATCH retries after 30 days, REVERTED never retries.

6. **Polite to upstream APIs.** Rate-limited, identified user-agent with contact email, retry-with-backoff on transient errors. Already implemented in `resolve_dois.py`; extend to all verifiers.

7. **Auditable provenance.** Every verification leaves a trail: which tool, which session, when, what response was received, what decision was made. The `verification_note` and `derivation_chain` fields exist for this — add a `verified_by_tool` column.

8. **No new schema unless necessary.** Reuse existing columns wherever the semantic fit is clean.

---

## 3. Pipeline architecture

```
                          ┌─────────────────────────────────────┐
                          │     scripts/verify_dispatch.py      │
                          │   (new — replaces resolve_dois)     │
                          │                                     │
                          │  selects rows, routes by source_type│
                          └────────────────┬────────────────────┘
                                           │
              ┌────────────────────────────┼────────────────────────────┐
              │                            │                            │
              ▼                            ▼                            ▼
  ┌──────────────────────┐    ┌──────────────────────┐    ┌─────────────────────────┐
  │  CHANNEL 1           │    │  CHANNEL 2           │    │  CHANNEL 3              │
  │  Academic            │    │  Standards / Gov     │    │  Co-1 attestation       │
  │                      │    │  / NGO / Reports     │    │                         │
  │  • CrossRef          │    │  • ISO catalog       │    │  • Manual sign-off      │
  │  • NCBI/PMC          │    │  • DIN catalog       │    │    registry             │
  │  • OpenAlex (fall-   │    │  • BSI / ANSI / CSA  │    │  • six required fields  │
  │    back, future)     │    │  • JIS / ABNT / GB   │    │    per co1-operational  │
  │  • Semantic Scholar  │    │  • légifrance, gov.uk│    │  • Co-1 contributor IDs │
  │    (fallback, future)│    │    riksdagen, etc.   │    │                         │
  │                      │    │  • RCOT / AOTA /     │    │                         │
  │                      │    │    CAOT publications │    │                         │
  └──────────┬───────────┘    │  • web_fetch + parse │    └─────────────┬───────────┘
             │                └──────────┬───────────┘                  │
             │                           │                              │
             └───────────────────────────┼──────────────────────────────┘
                                         │
                                         ▼
                          ┌──────────────────────────────┐
                          │  verification_outcome state  │
                          │  written back to             │
                          │  evidence_sources            │
                          └──────────────┬───────────────┘
                                         │
                                         ▼
                          ┌──────────────────────────────┐
                          │  audit_evidence_metadata.py  │
                          │  reads new state, re-scores  │
                          │  Phase E readiness           │
                          └──────────────────────────────┘
```

### Verification outcome state machine

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
        │              │              │                │
        ▼              ▼              ▼                ▼
  written to     marked, will     surfaced in     no state write
  evidence_      retry             dashboard
  sources                                          
        │
        ▼
   [REVERIFIED]  (periodic — annual cadence; URLs rot)
        │
        ▼
   [SUPERSEDED]  (standard withdrawn / replaced)
        │
        ▼
   [REVERTED]   (verification later found to be wrong; never retry)
```

Maps to existing `verification_status` enum plus new values: `NEEDS-HUMAN`, `SUPERSEDED`, `TRANSIENT-RETRY-PENDING`.

---

## 4. Per-channel verifier specifications

### Channel 1 — Academic (CrossRef + NCBI)

**Status:** Already shipped (`scripts/resolve_dois.py`).

**Improvements proposed:**
- Add OpenAlex fallback for CrossRef misses (free, no auth, broader coverage of preprints and non-DOI journal articles).
- Add Semantic Scholar fallback for cases where title contains BPC paraphrase (S2's title-similarity search is more tolerant than CrossRef's exact-match).
- Add PMC-ID-in-title-field extractor: regex scan for `PMC\d+` in pub_title, send to NCBI converter, write back DOI + PMCID separately.
- For corporate-authored journal articles: skip CrossRef author query (it fails), use bibliographic search via `query.bibliographic` with the corporate name + title + year.

### Channel 2 — Standards bodies

One small resolver module per body, dispatched by (corporate_name, standard_number) pattern match.

| Body | Catalog URL pattern | Verification method | Sources affected |
|---|---|---|---|
| ISO | iso.org/standard/{number}.html (where number is the numeric portion of ISO XXXXX:YYYY) | `web_fetch` the catalog page; confirm title contains expected keywords; extract publication year | ~25 ISO standards |
| DIN | din.de search API; resolve `DIN 18040-1:2010` → catalog entry | Search-then-confirm pattern | ~15 DIN standards |
| BSI | shop.bsigroup.com/SearchResults/ for `BS 8300-2:2018` | Search confirm | ~10 BS standards |
| CSA | csagroup.org/store/product/{number} | Direct URL | ~8 CSA standards |
| ANSI | webstore.ansi.org | Search | ~6 ANSI standards |
| JIS | jisc.go.jp database | Search; multilingual | ~5 JIS standards |
| GB (China) | std.samr.gov.cn or openstd.samr.gov.cn | Search; ZH-language results | ~12 GB standards |
| ABNT (Brazil) | abntcatalogo.com.br | Search | ~3 ABNT standards |
| AS/NZS | standards.org.au | Search | ~4 AS/NZS standards |
| EN | cen.eu / cenelec.eu | Search | ~8 EN standards |

Total: ~10-12 resolver modules covering ~100 sources.

### Channel 2 — Government legislation portals

| Country | Portal | URL pattern |
|---|---|---|
| UK | legislation.gov.uk | `legislation.gov.uk/{type}/{year}/{number}` |
| FR | legifrance.gouv.fr | search-then-confirm |
| DE | gesetze-im-internet.de | direct URL by short title |
| SE | riksdagen.se | search |
| ES | boe.es | direct by reference |
| IT | normattiva.it | search by D.M. / D.Lgs. ref |
| PT | dre.pt | direct by decreto-lei reference |
| NL | wetten.overheid.nl | search |
| CN | gov.cn / mohurd.gov.cn | search; multilingual |
| KR | law.go.kr | search |
| JP | e-gov.go.jp | search |
| US | (federal) federalregister.gov; (state) varies | varies |
| CA | laws-lois.justice.gc.ca; provincial varies | direct |
| AU | legislation.gov.au; state varies | direct |

Total: ~12-14 country modules covering ~80 government documents.

### Channel 2 — Professional / NGO bodies

| Org | Verification method | Notes |
|---|---|---|
| RCOT | rcot.co.uk publication archive | Has stable URL patterns |
| AOTA | aota.org practice guidelines | Members-only for some; verify URL exists, not content |
| CAOT | caot.ca | Direct URLs |
| RNIB | rnib.org.uk publications | Direct URLs |
| Dementia Australia | dementia.org.au | Direct URLs |
| WHO | who.int/publications | Has DOIs for most modern reports |
| World Bank | documents.worldbank.org | Direct URLs |
| UN | un.org / unescap.org / unesco.org | Mixed; many have DOIs now |
| IWA Ireland | iwa.ie | Direct URLs |
| CEUD / NDA Ireland | universaldesign.ie | Direct URLs |
| UNSW Home Modification Clearinghouse | homemods.info | Direct URLs |
| Inter-Fédération (BE) | inter.be | Direct URLs |

Total: ~12-15 NGO modules covering ~100 sources.

### Channel 3 — Co-1 attestation

**Different shape entirely.** Co-1 lived-experience sources are not findable in an external catalog. They are testimony, advocacy publications, or direct contributor statements. Per `governance/co1-operational.md`, each Co-1 source requires six fields:
- contributor identity (or anonymized identifier)
- contributor consent record
- date of attestation
- jurisdiction context
- population context
- attestation type (testimony, advocacy publication, lived-experience report, etc.)

A Co-1 attestation registry is needed: a separate table linking Co-1 sources to their attestation records, with an attestation sign-off process distinct from external verification.

**Proposed schema:**

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

## 5. Schema additions

Minimal new state on `evidence_sources`:

```sql
ALTER TABLE evidence_sources ADD COLUMN verified_by_tool TEXT;
ALTER TABLE evidence_sources ADD COLUMN last_verified_at TEXT;
ALTER TABLE evidence_sources ADD COLUMN verification_attempt_count INTEGER DEFAULT 0;
ALTER TABLE evidence_sources ADD COLUMN superseded_by_ref_id TEXT REFERENCES evidence_sources(ref_id);
```

- `verified_by_tool`: short identifier like `crossref-v2`, `iso-catalog`, `legifrance`, `manual-2026-05-12`. Lets us bulk-revoke if a verifier turns out to have been buggy.
- `last_verified_at`: ISO timestamp. Drives reverification cadence.
- `verification_attempt_count`: increments on each attempt, regardless of outcome. Surfaces stuck rows.
- `superseded_by_ref_id`: when a standard is withdrawn and replaced, link to the replacement.

New table:
- `co1_attestations` (above)

---

## 6. Dispatcher

A single orchestrator chooses which verifier to invoke per row:

```python
def route(row):
    """Return list of verifiers to try, in priority order."""
    if row.doi:
        return ['already-resolved']  # skip
    
    # Channel 1 — academic
    if row.source_type in ('journal_article','book','book_chapter','thesis','conference_paper'):
        if row.pmid:
            return ['ncbi', 'crossref-structured', 'openalex', 'semantic-scholar']
        if row.first_author_last and row.pub_title and row.pub_year:
            return ['crossref-structured', 'openalex', 'semantic-scholar']
        if row.is_corporate_primary and row.pub_title and row.pub_year:
            return ['crossref-bibliographic']
        return ['needs-human-channel-1']
    
    # Channel 2 — standards
    if row.source_type == 'standard':
        body = identify_standards_body(row)  # ISO/DIN/BSI/CSA/etc.
        if body:
            return [f'standards-{body}']
        return ['needs-human-channel-2']
    
    # Channel 2 — government regulation
    if row.source_type in ('guideline','report') and row.jurisdiction and row.is_governmental:
        return [f'government-{row.jurisdiction.lower()}']
    
    # Channel 2 — NGO/CPG
    if row.source_type in ('guideline','report'):
        org = identify_org(row.corporate_name)  # RCOT/AOTA/WHO/etc.
        if org:
            return [f'ngo-{org}']
        return ['needs-human-channel-2']
    
    # Channel 3 — Co-1
    if row.source_type == 'grey' and row.co1_provenance:
        return ['co1-attestation-queue']
    
    return ['needs-human-classification']
```

The dispatcher itself does no fetching. It hands the row to the first verifier in the priority list; on `NO-MATCH` it tries the next; on `TRANSIENT` it stops and queues for retry.

---

## 7. Phased rollout

### V1 — Minimum viable (1-2 sessions of work)

Just two additions to the existing Channel 1:

1. PMC-ID-in-title extractor → existing NCBI converter
2. CrossRef bibliographic-search fallback for corporate-authored academic items

Expected unblock: 10-20 additional sources verified per Action run; ~30-50 over a quarter.

**Effort: ~3 hours. Pure addition to `resolve_dois.py`. No new tables.**

### V2 — Channel 2 standards + government (3-5 sessions)

Build resolver modules for the top-5 standards bodies and top-3 government portals by source count:
- ISO, DIN, BSI, CSA, EN (covers ~70% of standards)
- légifrance, gov.uk, MOHURD/openstd (covers ~50% of government regs)
- Verification dispatcher in `scripts/verify_dispatch.py`
- New columns: `verified_by_tool`, `last_verified_at`

Expected unblock: 80-120 additional sources verified over a quarter; brings overall eligibility from 7% to ~30%.

**Effort: ~20-25 hours. New code, new schema columns, but contained.**

### V3 — Full Channel 2 + Channel 3 (10-15 sessions)

- Remaining standards bodies (JIS, GB, ABNT, AS/NZS, ANSI)
- Remaining government portals (DE, SE, ES, IT, PT, NL, KR, JP, US, CA, AU)
- NGO/CPG verifiers (RCOT, AOTA, CAOT, WHO, RNIB, Dementia Australia, etc.)
- Co-1 attestation registry table + sign-off workflow
- Reverification cadence scheduler (annual recheck of URL-based verifications)
- Verification frontier dashboard

Expected unblock: ~80-90% of corpus verified; all Co-1 sources have attestation records; Phase E unblocked across most BPCs.

**Effort: ~80-120 hours spread across multiple sessions. The bulk of long-term work.**

---

## 8. Integration with existing validators

The pipeline writes verification state that the existing validators already read. No retrofitting needed for:

- `audit_evidence_metadata.py` — reads `metadata_quality` + `verification_status` to score Phase E readiness; will benefit automatically.
- `validate_evidence_state.py` (A6) — reads `verification_status` for §2.8 downgrade; will benefit automatically.
- `validate_reasoning.py` — checks reasoning docs cite eligible sources; will benefit automatically as more sources become eligible.

What benefits from minor extension:

- `audit_adversarial_use.py` could be extended to require an "evidence verification has been performed" precondition before adversarial review, ensuring claims are reviewed against confirmed-real sources only.

---

## 9. What this pipeline does NOT do

Stating limits explicitly so they don't get hidden:

1. **Does not validate claim support.** Confirming a paper exists is not confirming it supports a specific synthesis claim. The adversarial protocol (rule #7) is a separate gate that must be applied independently.

2. **Does not assess source quality.** Tier assignment, methodological rigor, and inclusion/exclusion are editorial decisions, not automatable.

3. **Does not handle paywalls.** For paywalled content, verification stops at "confirmed to exist at this DOI/URL"; the project's editorial process must arrange separate access for full-text reading.

4. **Does not detect retractions.** A separate periodic pass against CrossRef's retraction watch API would handle this — out of scope for V1-V3 but trivially addable.

5. **Does not arbitrate jurisdictional precedence.** If two standards conflict, the pipeline confirms both exist; the synthesis pass decides which governs.

---

## 10. Recommended next step

If this proposal is approved, the cleanest first move is **V1 only**:

- 30-line PMC-ID extractor added to `resolve_dois.py`
- ~50-line CrossRef bibliographic-search fallback for corporate authors
- No new schema, no new tables, no dispatcher yet
- Test that V1 unblocks at least 10 additional sources on the next Action run

That validates the pipeline shape with the lowest possible commitment. If V1 works, V2 follows; if V2 works, V3 becomes the long-running compounding work.

The full architecture above is the *target state*. V1 is the *first step toward it*. Don't build V3 in one session — it would be over-engineered for what's needed today and would lock in design choices before they're proven.

---

## Appendix — Cost-benefit summary

| Phase | Effort (hours) | Sources verified incremental | Sources verified cumulative | Phase E unblock |
|---|---|---|---|---|
| Current state | — | — | 47/675 (7%) | 1 BPC ready |
| V1 (PMC + bib-search) | 3 | +30-50 | 80-100 (12-15%) | ~3-5 BPCs ready |
| V2 (top standards + top govt) | 25 | +80-120 | 160-220 (24-33%) | ~15-25 BPCs ready |
| V3 (full coverage) | 80-120 | +400-450 | 560-670 (83-99%) | ~60-75 BPCs ready |

Comparison to current Phase B grind without this pipeline: ~800-1,600h of manual verification at maybe 5-10 sources/hour by a human. The pipeline is a 100-150h investment that replaces 600-1,400h of that grind. Net saving: ~500-1,250h.

---

## Decision needed

This proposal is at design stage. To proceed, the project owner should decide:

1. **Is the two-channel framing accepted?** (Channel 1 academic + Channel 2 standards/gov/NGO + Channel 3 Co-1 attestation)
2. **Is the phased rollout (V1 → V2 → V3) the right shape?**
3. **Are the proposed schema additions (`verified_by_tool`, `last_verified_at`, `verification_attempt_count`, `superseded_by_ref_id`, `co1_attestations` table) acceptable?**
4. **Should V1 be built now?**

Awaiting direction before any code is written.
