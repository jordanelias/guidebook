# Slug × language tracking matrix — non-English research recovery

*Live tracking document, updated as work proceeds across sessions/batches. Legend below. This is the
single place to check "have we touched X language for Y slug yet" before spending more research effort.*

**Batch 5 note (adversarial review, run at the user's request):** an independent review found and
corrected 1 factual error, 6 tier/`evidence_type` doctrine violations, 1 `lang_detected`
over-correction (reverted), and 1 misleading audit-trail note (data value unchanged) — via migration
`data_20260719060557_..._batch5.sql`. It also caught 2 undercounts in this document's own non-English
totals (sensory-room-user-control 2→3, deaf-spatial-design 4→5, both already corrected below). Full
detail in `equity-dashboard.md`'s "Batch 5" section and `non-english-coverage-matrix.json` →
`batch5_adversarial_review`. Structural DB integrity was clean throughout; 7 of 8 independently
re-verified sources were confirmed accurate.

**Batch 7 note (closing out the Global-South leads + 2 small loose ends):** Permen PUPR 14/2017
(Indonesia) ingested as REF-00770 — the last unresolved Global-South lead, now all 9 original leads
resolved. Kepmen PU 468/1998 confirmed superseded (revoked by Permen PU 30/PRT/M/2006), correctly not
ingested. The Italian companion "Linee guida n. 1" date on REF-00746 was corrected/confirmed to 31 marzo
1994 (not 31 gennaio), with the Legge 724/1994 art. 3 cross-reference now confirmed rather than
suspected. Portugal's IGAS 2023 ERPI referencial was checked for dementia-specific design content and
found to contain none (clinical/organizational care guidance only) — this **corroborates**, not
overturns, Portugal's existing genuine-absence finding for wayfinding-dementia-spatial-design. No DB
change needed for the Portugal item. Full detail in `equity-dashboard.md`'s "Batch 7" section.

**Batch 8-9 note (the 2 final Tier-2 stub-notes slugs + a citation-mining scoping pass):**
`cognitive-wayfinding-design` and `accessible-circulation-geometry` — the last 2 "not started" slugs from
the substrate-quality finding below — were closed out via 4 pure relinks of already-verified DB rows (zero
new fabrication surface): Sweden + Denmark for cognitive-wayfinding-design (both matching its own
documented small-group-residential-scale finding), Netherlands + Japan for accessible-circulation-geometry
(both general national accessibility standards analogous to the DIN 18040-1 citation already there). While
researching, found and fixed 3 more instances of the unicode_block Chinese-hanzi-misread-as-Japanese bug
(REF-00195, REF-00196, REF-00502) plus 1 jurisdiction-code typo (REF-00198, `JA`→`JP`). Separately, a
citation-mining scoping pass (batch 9) tested real network reachability to CrossRef/OpenAlex/Semantic
Scholar and confirmed all 3 are blocked this session — the same root-cause egress policy as the `WebFetch`
outage, not a per-source problem. Full detail in `citation-mining-non-english-finding.md`.

## Legend

- ✅**R** = relinked an already-verified DB row (zero new fabrication surface)
- ✅**N** = new source ingested, real-retrieval verified this session
- ✅**N(rs)** = new source ingested at a deliberately **r**educed/**s**coped citation (verification found the search notes overclaimed it)
- 🚫**A** = genuine absence confirmed (searched, real effort, nothing formal exists) — a finding, not a gap
- 🔎**F** = found via fresh research but **not yet ingested** (flagged lead — needs a verify-and-ingest pass, or is a pending bill/non-binding guidance not fit to cite as a standard)
- ⛔**B** = blocked — investigated but rejected (e.g., confirmed to be a pending bill, or a wrong/mis-scoped citation caught and corrected elsewhere)
- ⬜ = not yet touched this recovery effort
- `stub` = the `search_languages.notes` for this slug/language are PRE-REMEDIATION placeholder rows ("Extracted from BPC REF-ID table") with **zero named instruments** — nothing to recover without fresh primary research

## Tier-0 (registry backlog, resolved batch 1)

| ref | jurisdiction | disposition |
|---|---|---|
| REF-00221 | JP | ✅N — deafblind communication guide |
| REF-00139 | SG | ✅N — BCA wayfinding code 2025 (EN language, jurisdictional diversity only) |
| REF-00218 | DE | ⛔B — stale registry dup of REF-00329 |
| REF-00243 | FI | ⛔B — stale registry dup of REF-00424/459 |
| REF-00372 | FR | ⛔B — stale registry dup of REF-00350 |
| REF-00382 | CN | ⛔B — stale registry dup of REF-00462 |

## Per-slug matrix

| slug | DE | FR | IT | ES | NL | SV | NO | DA | FI | PT | JA | KO | ZH | CL/other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **deaf-classroom-reverberation-time** | ✅R (DIN18041) | ✅N (Arrêté 2003, corrected) | ✅R+✅N (UNI11532 + Circolare 3150/1967) | ⬜ | ✅N (PvE Frisse Scholen) | ✅N (SS25268) | ✅R (NS8175) | 🚫A (no clean single std) | ✅N (SFS5907) | ⬜ (not searched by orig. sweep) | 🚫A (no binding std) | ⬜ (not searched by orig. sweep) | ✅R (GB50118) | — |
| **stair-ramp-threshold-biomechanics-accessibility** | ✅R (DIN18040-1) | ✅R (Arrêté 2014) | ✅R (DM236/DPR503) | ✅R+B (CTE-DB-SUA, citation corrected) | ✅N (Bbl Art.4.30) | ✅R (BFS/BBR) | ✅R (TEK17 §12-16) | ✅R (BR18) | ✅R (Decree241/2017) | ✅R (DL163/2006) | ⬜ | ⬜ (not cross-checked) | ✅R (GB50763) | — |
| **wayfinding-dementia-spatial-design** | ✅N(rs) (Wegweiser Demenz) | ✅N (Décret 2016-1164 UHR/PASA) | ✅N (DPCM 22/12/1989) | ✅N(rs) (GuíaSalud GPC484) | ✅N (Toolkit Dementievr. Woongebouw) | ✅N (Socialstyrelsen 2017-12-2) | ✅N (Helsedirektoratet) | ✅N×2 (Mærkningsordning + SBi-259) | ✅N (Ympäristöopas 2018) | 🚫A (re-confirmed 2×, 5+ queries) | ✅N (MHLW Ord. 34) | ✅N (Seoul Cog. Health Design Manual) | ✅N (GB/T 46401-2025) | — |
| **sensory-room-user-control** | 🚫A (no DIN std, already recorded) | pre-existing non-EN (REF-00700, "Les espaces Snoezelen" — corrected en→fr in batch 3, a cross-effect on this slug's count not originally noticed) | 🚫A | 🚫A | 🚫A | 🚫A | 🚫A | 🚫A | ⬜ | 🚫A | 🚫A | ⬜ (existing SI-clinical link REF-00702 ko, not std) | 🚫A | ✅N Chile Ley 21.545 (rs); ⛔B Brazil PL3098/24 (pending bill, not ingested) — total non-EN 3/13 (corrected 2026-07-19 batch5, see note at top) |
| **luminance-contrast-and-pattern** | ✅N (DIN 32975) | ✅R (Arrêté 2014, LCP-03) | ✅R (DM236/DPR503, LCP-04) | ✅R (CTE-DB-SUA §SUA1 4.3, LCP-05) | ✅R (NEN9120 REF-00071, LCP-06) | ✅R (BFS/BBR, LCP-07) | ✅N (NS11001-1/2) | ✅R (BR18, LCP-08) | ✅R (Decree241/2017, LCP-09) | ✅R (DL163/2006, LCP-10) | ✅R (バリアフリー法, general only — specific Road Mobility Guideline unconfirmed, LCP-11) | ✅R (편의증진법 REF-00511, LCP-12) | ✅R (GB50763, LCP-13) | — **100% non-EN (13/13) — 0/0 → 13/13** |
| **mental-health-built-environment** | ✅N ×2 (EPH Planungshandbuch Psychiatrie; DGUV Info 207-027) | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ✅N (Werkboek HIC); ⛔B (College bouw zorginstellingen — historical/defunct, not ingested) | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | — | ⬜ `stub` | — | ⬜ `stub` | 🔎F Niedersachsen Planungshilfe (state- not federal-level, not ingested) |
| **deaf-spatial-design** | ✅N (DAB DeafSpace article); 🔎F TU Darmstadt research group + Elbschule Hamburg (context only, not separately ingested) | ⬜ `stub` | pre-existing non-EN (REF-00347, LIS decree — predates this session, not counted as a batch-4 addition) | ⬜ `stub` | ⬜ `stub` | pre-existing non-EN (REF-00346, Stockholm accessibility — predates this session, not counted as a batch-4 addition) | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ✅N ×2 (Tsukuba Univ. of Technology campus — grey/national; Metote Lab — **Co-1**, Deaf-led, Tokyo-regional); 🔎F Nikken Sekkei (corporate research, not ingested) | ⬜ `stub` | ⬜ `stub` | — total non-EN 5/13 (2 pre-existing + 3 new; corrected 2026-07-19 batch5, see note at top) |
| **cognitive-wayfinding-design** | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ✅R (REF-00754, Nationella riktlinjer — small-scale-housing scope) | ⬜ `stub` | ✅R (REF-00747, DK dementia-home labelling — small-scale-housing scope) | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ✅N (lang-fix: REF-00502 corrected ja→zh, unicode_block bug) | — batch 8: 22→24 links, 8→10 non-EN (2 relinks: SE, DK) |
| **accessible-circulation-geometry** | ⬜ `stub` (already has 2 relinked refs from batch-1 lang-fix, not a fresh recovery pass) | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ✅R (REF-00071, NEN 9120 — reduced/scoped, content specifics unconfirmed) | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ⬜ `stub` | ✅R (REF-00065, Japan MLIT accessible-building design standard — reduced/scoped) | ⬜ `stub` | ⬜ `stub` | — batch 8: 12→14 links, 3→5 non-EN (2 relinks: NL, JP) |

## Global-South language investigation (cross-slug, not per-slug — see `global-south-finding.md`)

| language | verdict | resolution (batch 6) |
|---|---|---|
| Swahili (SW) | 🚫A genuine absence (underlying KE/TZ law is real but English-only) | n/a — nothing to ingest |
| Indonesian (ID) | 🔎F — query-construction failure, NOT absence; 3 candidates found | ⛔B SNI 03-1735-2000 confirmed OUT OF SCOPE (fire-safety egress standard, not accessibility — full title resolved batch 6). ✅N Permen PUPR 14/2017 ingested batch 7 (REF-00770, "Berlaku"/in force, first Indonesian jurisdiction in corpus). ⛔B Kepmen PU 468/1998 confirmed genuinely accessibility-scoped but formally revoked by Permen PU 30/PRT/M/2006 (explicit repeal language on the JDIH BPK RI record) — not ingested. |
| Hindi (HI) | 🔎F — query-construction failure, NOT absence; 1 candidate found | ⛔B could not re-locate the file via WebSearch batch 6 (4 queries, empty); relationship to REF-00509 (already-ingested India HGS-2021) undetermined — not ingested to avoid double-count risk. |
| Bengali (BN) | 🔎F — query-construction failure (subtler), NOT absence; 2 candidates found | ✅N Bangladesh 2013 Disability Rights Act ingested (REF-00769, honest enforcement-weakness caveat). ⛔B BUAG confirmed a secondary BNBC explainer, not a primary standard, publisher still unconfirmed — not ingested. |
| Arabic (AR) | 🔎F — query-construction failure, NOT absence; 4 candidates found | ✅N×3 Saudi SBC 201 (REF-00766), Egyptian Code 601 (REF-00767), Dubai Universal Design Code (REF-00768) all ingested, all confirmed mandatory/enforceable. |

**All 9 original leads now resolved (batches 6-7)** — 5 ingested, 4 correctly excluded — via careful
WebSearch-only re-verification. `WebFetch` failed its control-URL test for a 4th consecutive session in
batch 7, so the batch-5-validated verification standard was applied again rather than waiting for the tool.
The final 2 leads (the Indonesian Kepmen/Permen pair) were resolved batch 7: Permen PUPR 14/2017 ingested
(REF-00770, in force), Kepmen 468/1998 confirmed superseded and excluded.

## `lang_detected` hygiene fix (cross-cutting, not slug-specific)

64 rows corrected total (59 batch 1 + 2 batch 3 + 3 batch 8), spanning DE(13+1=14), CH(2), CN(7+3=10),
SE(6), NO(11), DK(3), NL(5), FR(2+1=3), FI(2), IT(2), ES(2), JP(4) jurisdictions. The 3 batch-8 corrections
(REF-00195, REF-00196, REF-00502) are the same `unicode_block` Chinese-hanzi-misread-as-Japanese pattern as
the earlier CN fixes, found incidentally while researching cognitive-wayfinding-design/
accessible-circulation-geometry — not from a dedicated sweep. Plus 1 jurisdiction-code typo fixed
(REF-00198, `JA`→`JP`, unrelated to language). Full list in `non-english-coverage-matrix.json` →
`lang_detected_hygiene_fix`. **Known incomplete**: batch 3's widened sweep (beyond `standard_number`-bearing
rows) checked only 28 candidate rows across 8 jurisdictions and found 2 more, and batch 8's 3 finds were
incidental, not from a dedicated audit — a full audit of all non-`standard_number` rows (journal articles,
reports, grey lit) across all non-English jurisdictions is still owed (see `equity-dashboard.md` next-batch
list).

## Substrate-quality finding (important, cross-cutting)

Not every "non-EN hit count" in the original handoff is equally recoverable. Two distinct data qualities
exist in `search_languages.notes`:
1. **TIER2 NATIVE SEARCH** (2026-05-11) — rich, real, named instruments. Covers: deaf-classroom-
   reverberation-time, stair-ramp-threshold-biomechanics-accessibility, wayfinding-dementia-spatial-design,
   luminance-contrast-and-pattern (confirmed this session), and presumably others not yet checked.
2. **PROTOCOL: PRE-REMEDIATION stub** — placeholder rows, zero named instruments, literally "Extracted
   from BPC REF-ID table" (a language-mention COUNT from a prior English-language extraction, not a real
   native-language search result). Confirmed for: mental-health-built-environment, deaf-spatial-design,
   cognitive-wayfinding-design, accessible-circulation-geometry. **These 4 slugs cannot be processed via
   the "extract-and-verify" recovery pipeline** — there's nothing named to extract; they need genuine fresh
   primary research instead, a different and higher-effort activity than "recovery." Batch 4 did this for 2
   of the 4 (mental-health-built-environment, deaf-spatial-design), 2 jurisdictions each, real sources
   found and ingested for both (see table above). **cognitive-wayfinding-design and
   accessible-circulation-geometry have NOT had this fresh-research treatment** — both are lower priority
   since they already carry meaningful non-EN coverage from relinks (8/22 and 3/12 respectively), unlike
   mental-health/deaf-spatial which started at 1/22 and 0/10.

## What's genuinely done vs. still open, after 4 batches

**Done to a real, if not exhaustive, standard:** deaf-classroom-reverberation-time (9/12, 75%),
stair-ramp-threshold-biomechanics-accessibility (11/26, 42%), wayfinding-dementia-spatial-design (13/22,
59% — all clearly-named instruments actioned, Portugal's absence independently re-confirmed twice),
luminance-contrast-and-pattern (13/13, **100%** — every named instrument in the rich search notes now
relinked or ingested).

**Started, intentionally not finished (2 jurisdictions each, by design):** sensory-room-user-control (1
new + 1 investigated-and-rejected pending bill; most jurisdictions are genuine absence, already so
recorded), mental-health-built-environment (3 new, DE+NL only, `stub`-notes slug), deaf-spatial-design (3
new, DE+JA only, `stub`-notes slug, includes 1 Co-1 addition).

**Closed out via relink (batch 8), not fresh primary research:** cognitive-wayfinding-design (24 links,
10/24 non-EN — added SE, DK), accessible-circulation-geometry (14 links, 5/14 non-EN — added NL, JP). Both
were `stub`-notes slugs where the notes-extraction pipeline doesn't apply; rather than risk new
WebSearch-only fabrication surface for a low-priority slug, both were closed via pure relinks of
already-verified DB rows with honestly reduced/scoped relevance notes. This is a real jurisdictional
addition, not exhaustive coverage — neither slug has been searched fresh in all 14 languages.

**Not started:** the full 14×24 sweep beyond the slugs touched across batches 1-8. The Global-South 9
leads are fully resolved (batch 7); citation mining for non-English sources has a documented scoping
finding (batch 9, `citation-mining-non-english-finding.md`) rather than full coverage, since most
non-English sources (140/161) are structurally ineligible (no DOI) and the DOI-bearing remainder is
network-blocked this session.
