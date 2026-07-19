# Equity dashboard — before/after, 2026-07-19 non-English research recovery

*Session: `session_2026-07-19-non-english-research-recovery`. Full detail in
`non-english-coverage-matrix.json`; the recovery pipeline and discipline are in
`research-handoff-non-english.md`. Migration:
`scripts/migrations/data_20260719034512_2026-07-19-non-english-research-recovery.sql`.*

## Headline numbers

| metric | before | after | delta |
|---|---|---|---|
| `evidence_sources` total | 640 | 650 | +10 (new ingests) |
| non-English (`lang_detected` != en/eng) | 87 | **136** | **+49** |
| `lang_detected` rows corrected (mislabel fix) | — | 59 | new finding this session |
| `jurisdiction` = INTL (seam, should be INT) | 5 | 0 | fixed |
| `verification_status` = VERIFIED-2 (search-corroborated, primary fetch blocked) | 0 | 10 | new category, honestly disclosed |

The **+49 non-English delta is not just 10 new sources** — it is mostly a **data-hygiene correction**,
not new gathering. A systematic audit (triggered while investigating the handoff's single cited example,
REF-00572) found the same bug recurring across **59 rows**: national standards/regulations whose
`lang_detected` was set from English-gloss metadata or cross-contaminated between languages, rather than
the source document's actual home language. Examples caught: NS 8175 (Norway) tagged `en`; GB 50118-2010
(China) tagged `en`; five GB 50763 (China) rows tagged `ja` (Han-script confusion); DIN 18040 (Germany)
rows scattered across `en`/`no`/`nl`. **5 borderline cases were deliberately left uncorrected** rather than
guessed (see `non-english-coverage-matrix.json` → `lang_detected_hygiene_fix.deliberately_not_corrected`).

**Why this matters more than the raw count:** the corpus's actual non-English content didn't grow by 59 —
the *visibility* of it did. Any downstream equity metric reading `lang_detected` (coverage matrices, the
per-language distribution table in `HANDOFF.md` §2/§5) was undercounting non-English coverage before this
fix, in some cases significantly (e.g., every national-code jurisdiction's language axis was silently wrong
for a subset of its own rows).

## Language distribution, before → after

| lang | before (per handoff §1) | after |
|---|---|---|
| en/eng | ~553 | 514 |
| de | 11 | 25 |
| ja | 19 | 19 |
| no | 7 | 16 |
| fr | 11 | 14 |
| sv | 7 | 13 |
| nl | 9 | 11 |
| zh | — (not itemized; folded into "other") | 8 |
| pt | 7 | 7 |
| ko | 6 | 6 |
| it | 4 | 6 |
| fi | 2 | 6 |
| da | 2 | 3 |
| es | — | 2 |

(Before-column reproduces the handoff's §1 per-language ingested counts where itemized; some pre-session
per-language figures were not separately reported and are marked "—".)

## Tier-1 slug-level coverage (the concrete equity fix)

Three slugs were checked for non-English coverage at the `source_slug_links` level — the level that
actually determines what a reader sees on a rendered page. **All three had ZERO non-English sources linked
despite the multilingual search having named specific instruments for 11-14 languages each:**

| slug | non-EN search hits (per `search_languages`) | links before | non-EN links before | links after | non-EN links after |
|---|---|---|---|---|---|
| deaf-classroom-reverberation-time | 79 | 3 | **0** | 12 | **9** |
| stair-ramp-threshold-biomechanics-accessibility | 102 | 15 | **0** | 24 | **9** |
| wayfinding-dementia-spatial-design | 108 | 9 | **0** | 12 | **3** (partial pass — highest-yield slug, only 3 of ~15 named instruments actioned) |

Of the 22 new/relinked sources across these three slugs: **13 were relinks of ALREADY-VERIFIED rows**
(zero new fabrication surface — the standard was already in the DB, correctly cited elsewhere, just never
connected to the slug the original search actually named it for), and **10 were genuinely new ingests**,
each real-retrieval verified this session (see `verification_status = VERIFIED-2` disclosure below).

## The VERIFIED-2 disclosure

All 10 new ingests carry `verification_status = 'VERIFIED-2'`, not the corpus-standard `VERIFIED`. This
records honestly that verification rested on **convergent WebSearch retrieval across multiple independent
pages**, not a first-hand primary-document render — direct `WebFetch` was blocked (HTTP 403) on nearly
every primary source domain attempted this session (government/standards-body sites in Japan, Singapore,
Finland, France, Italy, Sweden, Netherlands, Norway, China), confirmed via the environment's proxy-status
endpoint as a **shared infrastructure issue this session** (many unrelated hosts affected simultaneously),
not evidence the sources don't exist. This mirrors an existing DB convention (`REF-00462`'s
`DEFERRED-V2-FLIP-VERIFIED` pattern) rather than inventing a new one. **Anti-fabrication gate held**: one
candidate (NF S31-080:2006, France) was dropped after verification showed it doesn't actually cover
classrooms (its real scope is offices/tertiary spaces) — the search-notes framing was wrong, and rather
than ingest a mis-scoped citation, it was replaced with the correct one (arrêté du 25 avril 2003).

## What this pass does NOT claim

- **Not comprehensive.** This is a first pass over Tier-0 (the registry backlog) + the two richest Tier-1
  slugs by non-EN yield + a partial pass on a third. wayfinding-dementia-spatial-design alone had 108
  non-EN hits across 14 languages; only 3 instruments (NO, CN, FI) were actioned. The remaining Tier-1
  slugs (luminance-contrast-and-pattern, sensory-room-user-control, and four ~20-hit slugs) and the full
  14-language × 24-jurisdiction sweep are untouched.
- **Jurisdiction ≠ language.** REF-00139 (Singapore) adds jurisdictional/Global-South diversity, not
  language diversity — its source document is in English. Recorded honestly, not folded into the
  non-English count.
- **The Global-South zero-result languages are diagnosed, not fixed.** See `global-south-finding.md`.
  Several real candidate sources were found during that investigation but are **not yet ingested** —
  flagged for a follow-up verify-and-ingest batch, consistent with the "recover, don't fabricate"
  discipline (a diagnosis is not itself a citation).

## Next batch (not done this session)

1. wayfinding-dementia-spatial-design's remaining ~12 named instruments (DE, IT, DA, ES, FR, JA, KO, NL,
   PT, SV clusters).
2. Tier-2: luminance-contrast-and-pattern (74), sensory-room-user-control (42), and the four ~20-hit slugs.
3. The 4 Global-South recoveries flagged in `non-english-coverage-matrix.json`
   (`global_south_zero_result_investigation.*.recovered_not_ingested`) — Indonesian SNI 03-1735-2000, the
   Hindi translation of India's Harmonised Guidelines, Bangladesh's BUAG site + 2013 disability act, and
   the Saudi/Dubai/Egyptian Arabic-region codes — each needs an independent direct-read verification pass
   before ingest (this session only got WebSearch corroboration, not a primary-document render, on any of
   them).
4. NL (Bouwbesluit/Bbl ramp provisions) and ES (CTE DB SUA ramp table) for
   stair-ramp-threshold-biomechanics-accessibility — named in search notes, not yet matched to a DB row.
5. A corpus-wide audit of whether the *original* 81×19 multilingual sweep's zero-results (beyond the 5
   flagged Global-South languages) are partly a WebFetch-domain-blocking artifact — every investigating
   agent this session hit the same blocking pattern independently across unrelated domains/languages.
