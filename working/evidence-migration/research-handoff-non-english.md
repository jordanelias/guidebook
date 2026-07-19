# Research handoff — recover the non-English evidence the search already surfaced

*Self-contained brief for a fresh session/researcher. Grounded in `data/guidebook.db`, 2026-07-19. This is
the **lowest-fabrication-risk, highest-equity-leverage** gathering move: we are not researching the world
from zero — we are recovering non-English sources a prior search already **found and named** but never
ingested.*

---

## 1. The premise (why this, why now)

The full-chain audit found the corpus's English skew is **manufactured in ingestion, not search**:

- The multilingual search ran **19 languages × 81 slugs** (`search_languages`, 1,539 rows).
- **14 languages returned results** — DE 109 · NO 82 · JA 82 · NL 76 · FR 75 · ZH 74 · IT 65 · ES 58 ·
  SV 56 · KO 54 · PT 52 · DA 52 · FI 50 — ≈ **885 non-English search-hits recorded** (these double-count a
  source found for several slugs, so unique instruments are fewer).
- Yet **only 87 non-English sources are ingested** into `evidence_sources` (ja 19 · fr 11 · de 11 · nl 9 ·
  sv 7 · pt 7 · no 7 · ko 6 · it 4 · fi 2 · da 2 · ca 1 · af 1).

**The enabling finding — the evidence is recoverable, not lost.** Of the 404 non-English search rows that
returned hits, **all 404 name their key instruments in `search_languages.notes`** (0 are count-only). Real,
specific sources are already written down, e.g.:
- **DE** — `DIN 18041:2016-03 "Hörsamkeit in Räumen"` (deaf-classroom-reverberation)
- **NO** — `NS 8175 "Lydforhold i bygninger"`; `Helsedirektoratet Nasjonal faglig retningslinje for demens`
- **ZH** — `GB 50763-2012《无障碍设计规范》` (Accessibility Design Code, MOHURD)
- **FR** — `Loi n° 2005-102`, `Arrêté du 1er août 2006`, `Arrêté du 8 décembre 2014`

So the task is **extract → verify → ingest**, not open-ended research.

## 2. The recovery pipeline (per non-English search row)

Run for each `search_languages` row where `language ∉ {EN}` and `results_count > 0`:

1. **Extract** the named instrument(s) from `notes` (they are there — 404/404).
2. **Verify each resolves** — a *real* tool call (WebSearch/WebFetch for the standard/law/guideline; PubMed
   / Scholar Gateway for articles). A source that does not re-retrieve is **dropped**, never ingested
   (the anti-fabrication gate; this is the rule the verifier already caught me breaking once).
3. **Dedup** against `evidence_sources` — some named instruments are already ingested (e.g., DIN 18041 is
   `REF-00329`; GB 50763 may be the registered-but-un-migrated `REF-00382`). Don't create duplicates.
4. **Tag** on ingest: `lang_detected` = the **true source language** (not the English metadata — see §5),
   `jurisdiction`, `tier` (most are T4–6 regulatory stratum; a few are T2 named-org standards), `evidence_type`,
   `standard_number`, `verification_status`.
5. **Ingest** via a migration (`scripts/emit_data_migration.py` → `migrate_db.py`; never ad-hoc UPDATE) and
   **link to the slug** in `source_slug_links`.
6. **Record the coverage matrix** row `{language, jurisdiction, slug, searched:Y, found:n, ingested:n,
   best_tier, note}` — **empties included** (a searched-and-found-nothing cell is a finding, per S6).

**A separate guilty-until-proven verifier re-retrieves a sample of the ingested sources** and rejects any
that don't resolve — same discipline as every graded item this session.

## 3. Targets, prioritized (start here)

**Tier 0 — already-registered, un-migrated non-English refs** (from `registry-reconciliation.md`; lowest
risk — a registry entry already exists, just verify + ingest):
`REF-00221` (JP, 盲ろう者 deafblind communication) · `REF-00382` (CN, GB 50763《无障碍出入口》) · `REF-00372`
(FR, Arrêté 2017 + CEREMA) · `REF-00243` (FI, Decree 241/2017) · `REF-00218` (DE, DIN 18041 — **verify vs
REF-00329 before ingesting; likely a duplicate/renumber**) · `REF-00139` (Asian wayfinding code).

**Tier 1 — richest slugs by non-English yield** (the instruments are named in `notes`):

| slug | non-EN hits | likely instrument cluster |
|---|---|---|
| wayfinding-dementia-spatial-design | 108 | NO Helsedirektoratet dementia guideline; DE/ZH dementia-design codes |
| stair-ramp-threshold-biomechanics-accessibility | 102 | FR Loi 2005-102 + Arrêtés; ZH GB 50763; DE DIN 18040 |
| deaf-classroom-reverberation-time | 79 | DE DIN 18041; NO NS 8175; (dovetails with the A-18/acoustic grading) |
| luminance-contrast-and-pattern | 74 | UK/EU luminance codes; JA/KO contrast standards |
| sensory-room-user-control | 42 | non-EN sensory/autism design guidance |
| cognitive-wayfinding-design · deaf-spatial-design · mental-health-built-environment · accessible-circulation-geometry | 19–23 each | mixed national standards |

**Tier 2 — the rest of the 14 productive languages**, slug by slug, until the coverage matrix is filled.

## 4. The Global-South zero-result investigation (a distinct sub-task — do NOT skip)

**Five languages returned zero across all 81 searches: SW (Swahili) · ID (Indonesian) · HI (Hindi) ·
BN (Bengali) · AR (Arabic).** This is the sharpest equity signal in the corpus. It is **not** a curation
choice — the search ran and found nothing. Determine *which* of three causes, because each has a different
remedy, and **state the finding honestly** (S3/S6 — absence demonstrated, not assumed):
- (a) **Tooling reachability** — the search engine/indexes don't cover those languages/regions → try
  region-specific sources (e.g., national standards bodies BIS/India, SNI/Indonesia, regional CRPD Art. 9
  concluding observations via IDA compilations, doctrine L336).
- (b) **Query construction** — English-transliterated queries that don't match native-script indexes → re-run
  with native-script terms.
- (c) **Genuine absence** — little formal accessibility-standards literature exists in those languages → then
  the honest move is Co-1 / lived-experience and CRPD treaty-body evidence, and the coverage matrix records
  the absence as a stated gap, not a failure to hide.

Whatever the answer, it is a **finding to publish**, not an embarrassment to bury.

## 5. Data-hygiene to fix during ingest (the runs surfaced these)

- **`lang_detected` mislabels.** Non-English standards were tagged `en` because `langdetect` ran on the
  English catalogue metadata (e.g., the French "Guide acoustique pour personnes malentendantes" REF-00572
  is tagged `en`). On ingest/re-tag, set `lang_detected` from the **home-language source text**, so the
  coverage matrix counts truthfully. (Jurisdiction is currently the more reliable equity axis; this fixes
  the language axis.)
- **Jurisdiction seam** — normalize `INT`/`INTL`/`EU` and backfill the 19 null jurisdictions
  (`db/migrations/0001-jurisdiction-hygiene.sql`, proposed) so the matrix is countable.
- **Home-language value verification** — where an English-metadata standard already carries an extracted
  value (`source_value_extractions`, `echo_of`), confirm the number against the **original-language** text
  (the A-08 run showed a metric can drift — ANSI "35 dBA" ≠ "NC-25").

## 6. Discipline (non-negotiable — the equity mandate's own worst failure mode is fabrication)

- **Every ingested source re-retrievable** via a real tool call; no exceptions. Non-English fabrications are
  *harder* to catch, so this gate is the loudest rule.
- **No back-translation** — never relabel an English source as another language to pad the matrix (a seeded
  plant the verifier already catches).
- **No quota parity** — equity = equal *search effort* + transparent yield, not equal counts. Weighting a
  thin non-English source up to hit a number is a rigour violation.
- **Empties kept** — a searched-and-empty language/jurisdiction cell is recorded, not dropped.

## 7. Success criteria · deliverables · honest limit

**Done (first pass) =** the named non-English instruments from Tier-0 + Tier-1 slugs verified and ingested
(deduped, correctly language/jurisdiction-tagged), the coverage matrix filled for those slugs, and the
Global-South zero-result cause identified and stated.
**Deliverables:** the ingest migrations (`db/migrations/`), a `non-english-coverage-matrix.json`, a
before/after `equity-dashboard.md` (non-EN ingested: 87 → N; per-language distribution), and the
`global-south-finding.md`.
**Verify:** verifier re-retrieves a sample; `PRAGMA foreign_key_check`; re-run the language-distribution
query to confirm the shift; no new duplicate DOIs/standard-numbers (dedup held).
**Honest limit (S3):** recovery from *named* notes is high-confidence and near-complete; a full
14-language × 24-jurisdiction sweep beyond what search already named is a larger program, reported as a
running fraction — not claimed as "all."

## 8. Key files & tables

- `data/guidebook.db`: `search_languages` (the source of the named instruments), `evidence_sources`,
  `source_slug_links`, `jurisdictional_values`, `source_value_extractions`.
- `working/evidence-migration/`: `registry-reconciliation.md` (the Tier-0 refs), `pipeline-audit.md` (the
  bias-funnel finding), `pilot-A18-rt60/coverage-matrix.md` (the language-tag-unreliability finding).
- Plan: `/root/.claude/plans/delegated-pondering-pine.md` Part IV (equity machinery), Part V (tools:
  PubMed / Consensus / Scholar Gateway / bioRxiv / WebSearch).
- Doctrine: `references/project-standards.md` (Co-1 co-primary L35; 24-juris/14-lang L121/L127; IDA
  compilations L336; Kawa L405). Render: `architecture/page-templates.md` facet 7 (jurisdictions side-by-side).
