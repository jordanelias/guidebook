# Session — re-derivation of the 5 remaining RETRACTED-PRE-REHAB empty slices
**Date:** 2026-07-20
**Branch:** `claude/multilingual-multi-jurisdictional-research-0ilfpm`

## Task
"Continue all five [remaining RETRACTED-PRE-REHAB slices] until complete carefully." Following the
`bathroom-typology-global-south` re-derivation (PR #34, merged), this session re-derives the other five
WS2 RETRACTED-PRE-REHAB empties, each with `source_slug_links=0` and `evidence_state=RETRACTED-PRE-REHAB`.

## Method — the enabling finding
Dedup against the live corpus showed that **nearly every source these five retracted syntheses named
already exists as a verified `evidence_sources` row** — ingested for other slugs, but never re-linked after
the DR-2026-05-23 rehab cleared these slices. So the lowest-fabrication-risk re-derivation is to **re-link
the already-verified rows** (45 of 47 links), and ingest only the two named leads genuinely absent from the
corpus (both re-retrieved via a real tool call). No source was linked below `verification_status` VERIFIED
except REF-00737, linked with an explicit UNVERIFIED-1 disclosure.

## Result (migration `data_20260720054037_...sql`)
`source_slug_links` 0 → **47** across the five slices; all five `evidence_state` RETRACTED-PRE-REHAB → **PARTIAL**.

| slug | links | audit grade | note |
|---|---|---|---|
| `bariatric-turning-radius-built-environment` | 8 | F → **D** (45.0) | Anglophone-concentrated, honestly — no non-English bariatric turning standard exists |
| `fold-down-grab-bar-specification` | 8 | F → **C** (55.3) | Novak 2024 (REF-00368) deliberately NOT linked, honouring the slice's standing do-not-cite flag |
| `jurisdiction-matrix-accessibility-standards` | 14 | F → **D‡** (46.6) | ‡ = code-floor/convergence-only — the honest character of a jurisdiction matrix (T4×4, T6×10), not a defect |
| `multilingual-evidence-convergence-non-english` | 8 | F → **B** (75.7) | strongest of the five; a methodology entry that is itself *about* non-English evidence |
| `neurodivergent-built-environment` | 9 | F → **C** (58.3) | strong anchor mix T1×2, T2×4 (PAS 6463, ASPECTSS, RCOT+NAS, Latiff Co-1) |

**Two net-new sources ingested:**
- **REF-00882** — Stroupe J & Sarbaugh S (2008), "Bariatrics defined," *Health Facilities Management* 21(4):27–32.
  T5 grey (trade/ASHE). 72-in (1830 mm) bariatric turning circle. WebSearch-verified.
- **REF-00883** — WHO (2021), Assistive Product Specification APS15, "Handrails and grab bars." T4. 110 kg × 3
  directions. WebFetch-verified against the who.int APS15 PDF (year corrected 2022→2021 in the adversarial pass).

## Adversarial review + self-caught correction
A fresh-context refuter re-retrieved the two net-new sources and spot-checked three cross-slug relevance links
(ICC A117.1-2017 / PAS 6463:2022 / Ielegems & Vanrie 2024). **Self-caught before commit:** REF-00882 was first
recorded with a fabricated first name ("John M. Stroupe" / "Sarbaugh D") — the sources give initials only
(Stroupe J, Sarbaugh S). Corrected via a forward-only compensating migration (`data_2026072005..._...sql`):
first name → unknown, `author_display` → "Stroupe J, Sarbaugh S", volume/issue/pages 21(4):27–32 added.
[Adversarial verdicts + any further corrections recorded in the compensating migration header.]

## Verification
`PRAGMA foreign_key_check` + `integrity_check` clean after both migrations; no duplicate DOIs/standard-numbers
(WHO APS15 unique). `tools/evidentiary_audit.py`: corpus F-count **11 → 6** (the five re-derived slices left F);
917 sources / 76 topics. `tools/regenerate_vetting_surface.py`: **0 orphans**.

## Not done / honest limits
- **All five keep `best_practice_synthesis` BLOCKED** — the retracted Opus syntheses are not rewritten (Opus
  capability floor; this was a re-linking/search pass). `search_complete` left 0.
- `jurisdiction-matrix` remains code-floor-only by nature; `bariatric` remains Anglophone-concentrated by the
  genuine absence of non-English bariatric turning standards — both stated, not hidden.
- The 8 empty *un-started* slices from the plan's WS2 (data-desync / MERGED-stale) are a separate data-hygiene
  batch; not in scope here. With these five, **all six RETRACTED-PRE-REHAB slices are now re-derived.**
