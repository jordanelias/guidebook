# Session — bathroom-typology-global-south re-derivation (multilingual/multi-jurisdictional)
**Date:** 2026-07-20
**Branch:** `claude/multilingual-multi-jurisdictional-research-0ilfpm`

## Task
"Continue multilingual multi-jurisdictional research." Scoped against the live project state, not
started from zero. The prior same-mandate session (`session_2026-07-20-poe-global-multilingual-research`)
filled WS2's one genuinely-empty *un-started* slice (`post-occupancy-evaluation-global`). This session
picked the next WS2 target from `workplan/evidentiary-base-research-plan-2026-07-19.md`: the
**RETRACTED-PRE-REHAB** empty slices — prior work cleared, awaiting re-derivation via the loop.

## Target selection (checked live DB, not the plan snapshot)
Of the 13 WS2 empties, POE-global is now done. Of the 6 RETRACTED-PRE-REHAB slices, chose
**`bathroom-typology-global-south`** — the best fit for a *multilingual multi-jurisdictional* mandate:
its retracted synthesis spans Indonesia (Sejong semi-squat toilet), Japan (多目的トイレ split facility),
India (RESNA), Brazil/LAC, MENA, Sub-Saharan Africa. Live state before this session:
`source_slug_links = 0`, `bpc_metadata.evidence_state = RETRACTED-PRE-REHAB`, `jurisdictions_searched = 0`,
all 19 `search_languages` rows `results_count = 0`. Genuinely empty in the DB (the retracted Opus
synthesis text existed on disk but carried zero linked evidence).

## What was done — the recovery loop (handoff §2)
Native-language WebSearch (Indonesian, Japanese, Portuguese-Brazil) + EN academic databases, every
ingested source re-retrieved via a real tool call before ingestion, then an adversarial refutation pass.

**Ingested (5 new, `REF-00877`–`REF-00881`) via `data_20260720051528_...sql`:**
- **REF-00877** — Sprouse et al. 2024, "Shared sanitation in informal settlements: a systematic review
  and meta-analysis," *Int J Hyg Environ Health* 260:114392. **T2 sr_meta, INT.** PubMed-confirmed
  (PMID 38788338, get_article_metadata). *This is the genuine record behind the retracted synthesis's
  garbled "ScienceDirect 2025, 93 studies, 22 countries" citation — ingested with correct metadata.*
- **REF-00878** — Daniel et al. 2023, inclusive-sanitation access for PWDs in Indonesia, *Sci Rep*
  13(1):4310. **T3 clinical, ID** (Indonesian-authored: UGM/ITB/Udayana). PubMed-confirmed (PMID 36922602).
- **REF-00879** — Sokhibi et al. 2025, universal-design accessible toilet + Javanese culture, *ETASR*
  15(6):28550–28559. **T3 clinical, ID** (Universitas Sebelas Maret). Verified via WebFetch of the DOI
  record (10.48084/etasr.12975).
- **REF-00880** — WHO/UNICEF JMP 2023, "Progress on household drinking water, sanitation and hygiene
  2000-2022." **T4 standard_eb, INT.** WebSearch-confirmed (3.5bn without safely managed sanitation, 2022).
- **REF-00881** — the Sejong / *Setengah Jongkok* (semi-squat) accessible toilet, Plan International
  Indonesia + Universitas Nusa Cendana + an OPD (Water for Women Fund). **Co-1 grey, ID.**
  WebSearch-confirmed (WebFetch of the funder page 503'd; identity established via snippet cross-read).

**Deduped + linked (3 existing corpus standards — no new rows created):**
- **REF-00077** — ABNT NBR 9050:2020 (Brazil, `pt`, T6 code) — Cluster 1 accessible-bathroom dims.
- **REF-00770** — Permen PUPR 14/PRT/M/2017 (Indonesia, `id`, T6 code) — Cluster 1/2 statutory requirements.
- **REF-00065** — MLIT 建築設計標準 (Japan, `ja`, T6 code) — Cluster 3 multipurpose/split-facility toilet.

`source_slug_links` **0 → 8**. Jurisdictions: **ID ×4, BR, JP, INT ×2** (4 distinct + 2 multi-country
syntheses). Languages: **id, ja, pt** (3 genuinely non-English standards) + en (4 Indonesian-authored /
international academic sources) — directly diluting the corpus's Anglophone concentration per WS3.

## Adversarial review (same session, fresh-context refuter)
Briefed to refute; re-retrieved all 5 new sources + 3 dedup-link identities from scratch. **All 8 held.**
Two field corrections, applied via a forward-only compensating migration (`data_20260720051847_...sql`):
- **REF-00881** — pub_year **2022 → 2020** (the Water for Women page dates the design *process* to 2020;
  2022 was publication/article timing).
- **REF-00077 BTG-6 link note** — WC-rim height tightened from loose "43–46 cm" to strict-norm "43–45 cm".
No drops. The reviewer independently confirmed the PP 16/2021 (Cipta Kerja) supersession *concern* for
Permen PUPR 14/2017 is legitimate — recorded as a code-currency flag on the BTG-7 link, not asserted current.

## Result / verification
- `PRAGMA foreign_key_check` + `integrity_check`: **clean** after both migrations. No duplicate DOIs;
  dedup held (standard_number `14/PRT/M/2017` stays 1 row, `NBR 9050:2020` stays 5).
- `tools/evidentiary_audit.py`: slice moved **grade F (rank 73, 0.0) → grade B (rank 24, 68.3)**;
  tier spread T1×1 (co1), T2×1, T3×2, T4×1, T6×3; 4 jurisdictions / 4 languages. Corpus: 82 slices /
  **870 instances** (was 862). Audit byte-stable after the correction migration (year/note only).
- `tools/regenerate_vetting_surface.py`: **0 orphans**, 870 sources.
- `bpc_metadata.evidence_state` RETRACTED-PRE-REHAB → **PARTIAL**; BPC file + search-log updated.

## Not done / honest limits
- **`best_practice_synthesis` remains BLOCKED** — the retracted Opus synthesis is *not* rewritten (Opus
  capability floor; this was a Sonnet search pass). `search_complete=0`.
- **The squat-toilet dimensional-specification gap is real and open** — the Sejong toilet is the only
  documented accessible semi-squat innovation and publishes no dimensions/load ratings; the guidebook
  must not reverse-engineer specs from the project description (retains the retracted synthesis's honest
  treatment). No Co-1 field pass beyond that exemplar.
- **Dropped, not padded:** the "Solano LAC review" named in the retracted synthesis did not re-retrieve
  under any search — dropped per the anti-fabrication gate. The MLIT 多機能トイレ basic-information report
  (mlit.go.jp/common/000209201.pdf) resolved but WebFetch returned unparseable binary — recorded as a
  follow-up lead, not ingested.
- **Not fixed (out of scope):** `scripts/validate_db.py` fails on a pre-existing `doi_less_key` column
  drift (confirmed identical failure against the committed HEAD DB) — a tooling issue independent of this
  batch, left for a data-hygiene session.
- The other 5 RETRACTED-PRE-REHAB slices (`bariatric-turning-radius-…`, `fold-down-grab-bar-…`,
  `jurisdiction-matrix-…`, `multilingual-evidence-convergence-non-english`, `neurodivergent-…`) remain
  the natural next WS2 targets.
