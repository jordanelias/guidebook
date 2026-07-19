# Equity dashboard — before/after, 2026-07-19 non-English research recovery

*Sessions: `session_2026-07-19-non-english-research-recovery` (batch 1),
`session_2026-07-19-non-english-research-recovery-batch2` (batch 2), and
`session_2026-07-19-non-english-research-recovery-batch3` (batch 3, a small follow-on fix). Full detail
in `non-english-coverage-matrix.json`; the recovery pipeline and discipline are in
`research-handoff-non-english.md`. Migrations:
`scripts/migrations/data_20260719034512_2026-07-19-non-english-research-recovery.sql` (batch 1),
`scripts/migrations/data_20260719052009_2026-07-19-non-english-research-recovery-batch2.sql` (batch 2),
`scripts/migrations/data_20260719053052_2026-07-19-non-english-research-recovery-batch3.sql` (batch 3).*

## Headline numbers (cumulative, all five batches)

| metric | pre-session baseline | after batch 1 | after batch 2 | after batch 3 | after batch 4 | after batch 5 | cumulative delta |
|---|---|---|---|---|---|---|---|
| `evidence_sources` total | 640 | 650 | 661 | 662 | 670 | 670 | +30 (new ingests; batch 5 corrected existing rows, added none) |
| non-English (`lang_detected` != en/eng) | 87 | 136 | 147 | 150 | 158 | **157** | **+70** (batch 5 reverted 1 over-correction, REF-00310) |
| `lang_detected` rows corrected (mislabel fix) | — | 59 | 59 | 61 | 61 | 61 (net; +1 correction, -1 reversion) | 59 (batch 1) + 2 (batch 3) − 1 reverted (batch 5) + 1 honesty-fixed (batch 5, value unchanged) |
| `jurisdiction` = INTL (seam, should be INT) | 5 | 0 | 0 | 0 | 0 | 0 | fixed |
| `verification_status` = VERIFIED-2 (search-corroborated, primary fetch blocked) | 0 | 10 | 21 | 22 | 30 | 30 | new category, honestly disclosed |
| `data_migrations` ledger rows | 199 | 200 | 201 | 202 | 203 | **204** | 5 migrations this session |

### Batch 5 — adversarial review, run at the user's request

A genuinely independent review (4 parallel agents, blind to the ingesting agent's own reasoning, tasked
with trying to REFUTE rather than confirm) checked: (a) DB integrity + migration SQL logic, (b) a sample of
8 new ingests via fresh WebSearch re-verification, (c) every quantitative claim in this documentation
re-derived directly from the live DB. **Structural integrity was clean throughout** (FK/PRAGMA checks, no
duplicate local_ref_ids) and 7 of 8 sampled sources were confirmed accurate on re-verification. Real issues
found and corrected via a compensating migration (this repo's migrations are forward-only/immutable —
corrections land as new migrations, never edits):

1. **One factual error**: `REF-00751` (Japan's MHLW dementia group-home ordinance) claimed "max 2
   units/18 residents" — the current standard (post-2021 revision) actually allows up to 3 units/27
   residents. Corrected; the "strictest small-scale mandate" superlative that partly rested on the wrong
   figure is withdrawn.
2. **Six tier/`evidence_type` doctrine violations** against `governance/tier-system.md`: `REF-00744`
   (GB/T, non-mandatory) was wrongly tiered T6 (statutory) — corrected to T5. Three formal national
   clinical-guideline-catalogue documents (`REF-00743`, `REF-00749`, `REF-00754`) used `evidence_type=
   clinical` (reserved for primary research) instead of `standard_eb` — corrected. `REF-00745` (a housing
   design guide, not a clinical document at all) and `REF-00221` (its own notes already said it wasn't a
   design standard) were both wrongly at T2/clinical, granting undeserved best-practice-anchoring status
   — corrected to T5/national_fw and T3/grey respectively. `REF-00765` (the Metote Lab Co-1 addition) was
   miscoded T3/grey instead of this DB's established Co-1 convention (T1/`co1`) — **this one silently
   defeated the batch's own stated purpose**, since nothing querying by `evidence_type='co1'` would have
   found it. Corrected.
3. **One likely `lang_detected` over-correction reverted**: `REF-00310` (a Lund University PhD
   dissertation) was flipped `en`→`sv` in batch 1, but Lund's own publications catalogue lists an English
   title for it. Reverted to `en` — this was exactly the kind of ambiguous case batch 1 correctly left
   alone for 5 *other* rows on the same reasoning; it should have been left alone here too.
4. **One verification_note honesty fix (data value unchanged)**: `REF-00299`'s stated justification
   ("verified from native-language text") was false — both title fields are entirely English; the real
   basis was jurisdiction-inference. The *value* (`no`) was independently re-confirmed correct; only the
   audit-trail's stated reasoning was corrected.
5. **Two documentation undercounts** (found by the doc-accuracy check, corrected below): this document
   previously claimed sensory-room-user-control at 2 non-English links (actual: 3 — missed that a batch-3
   `lang_detected` fix on an already-linked row also raised this slug's count) and deaf-spatial-design at 4
   (actual: 5 — undercounted 2 pre-existing non-EN relinks that predated this session's fresh-research
   additions). Both fixed below.

**One soft, non-fabrication issue left as a flagged note, not a fix**: a `luminance-contrast-and-pattern`
relink (`REF-00462`, GB 50763) cites a stair/tactile-contrast provision that lives in a different section
of the standard than this row's own excerpt (accessible entrances) — same real standard, imprecise section
targeting. Annotated in `source_slug_links.relevance_note`, not corrected further (would need a
section-specific GB 50763 row that may not exist in the DB yet).

**Batch 4:** see `slug-language-tracking-matrix.md` for full detail. Closed `luminance-contrast-and-pattern`
(a slug with rich search notes but **zero** `source_slug_links` at all, discovered this session) to
**100% non-English coverage (13/13)** — mostly relinks of already-verified rows, plus 2 new contrast-
specific standards (DIN 32975 Germany, NS 11001 Norway). Also discovered that 4 "Tier-2" slugs
(`mental-health-built-environment`, `deaf-spatial-design`, `cognitive-wayfinding-design`,
`accessible-circulation-geometry`) have **PRE-REMEDIATION stub search notes with zero named
instruments** — a different, harder problem than the other slugs, since there's nothing to extract-and-
verify. Did genuine fresh primary research (not notes-extraction) for 2 of the 4, 2 jurisdictions each,
finding real citable sources for both — including one **Co-1** addition (a Deaf-led Japanese research
project), a track this corpus has documented as thin and US/UK-skewed.

**Batch 3 (small follow-on):** widening batch 1's `lang_detected` fix beyond `standard_number`-bearing
rows found 2 more mislabeled rows — including **`REF-00572`, the ORIGINAL motivating example the handoff
itself cited** ("Guide acoustique pour personnes malentendantes," tagged `en`), which batch 1 missed
because it lacks a `standard_number` and so fell outside that batch's narrower filter. Also added one new
sensory-room-user-control source (Chile's Ley N° 21.545), ingested with an **honest scope correction**:
verification found the law creates a general procedural duty, not an explicit "sensory room" mandate as
the search notes implied — the stricter infrastructure requirement is a still-pending amendment bill, not
cited. A companion Brazilian bill (PL 3098/24) was investigated and found to be a **pending bill, not
enacted law** — deliberately NOT ingested (citing an unpassed bill as a "standard" would be an overclaim).

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

## Language distribution, before → after batch 1 → after batch 2

| lang | before (per handoff §1) | after batch 1 | after batch 2 |
|---|---|---|---|
| en/eng | ~553 | 514 | 514 |
| de | 11 | 25 | 26 |
| ja | 19 | 19 | 20 |
| no | 7 | 16 | 16 |
| fr | 11 | 14 | 15 |
| sv | 7 | 13 | 14 |
| nl | 9 | 11 | 13 |
| zh | — (not itemized; folded into "other") | 8 | 8 |
| pt | 7 | 7 | 7 |
| ko | 6 | 6 | 7 |
| it | 4 | 6 | 7 |
| fi | 2 | 6 | 6 |
| da | 2 | 3 | 5 |
| es | — | 2 | 3 |

(Before-column reproduces the handoff's §1 per-language ingested counts where itemized; some pre-session
per-language figures were not separately reported and are marked "—".)

## Tier-1 slug-level coverage (the concrete equity fix)

Three slugs were checked for non-English coverage at the `source_slug_links` level — the level that
actually determines what a reader sees on a rendered page. **All three had ZERO non-English sources linked
despite the multilingual search having named specific instruments for 11-14 languages each:**

| slug | non-EN search hits (per `search_languages`) | links before | non-EN before | links after batch 1 | non-EN after batch 1 | links after batch 2 | non-EN after batch 2 |
|---|---|---|---|---|---|---|---|
| deaf-classroom-reverberation-time | 79 | 3 | **0** | 12 | **9** | 12 | 9 (untouched in batch 2) |
| stair-ramp-threshold-biomechanics-accessibility | 102 | 15 | **0** | 24 | **9** | 26 | **11** (+1 new NL ingest, +1 ES citation correction/relink) |
| wayfinding-dementia-spatial-design | 108 | 9 | **0** | 12 | **3** (partial) | 22 | **13** (batch 2 completed the pass — 59% non-EN) |

Of the 22 batch-1 new/relinked sources across the three Tier-1 slugs: **13 were relinks of ALREADY-VERIFIED
rows** (zero new fabrication surface — the standard was already in the DB, correctly cited elsewhere, just
never connected to the slug the original search actually named it for), and **10 were genuinely new
ingests**. Batch 2 added **11 more items** to wayfinding-dementia-spatial-design and stair-ramp (10 new
ingests + 1 corrected relink), all real-retrieval verified this session (see `verification_status =
VERIFIED-2` disclosure below).

### Batch 2 — completing wayfinding-dementia-spatial-design, filling the NL/ES ramp gaps

wayfinding-dementia-spatial-design (108 non-EN search hits, the corpus's single richest non-English-search
slug) went from a batch-1 partial pass (3/~15 named instruments) to **10 of the remaining instruments
actioned**, taking it to **13 non-English sources / 22 total links (59% non-English)** — the highest
non-English share of any slug touched so far. Portugal was independently re-checked with 5 additional
search queries and the genuine-absence finding **held** (no formal Portuguese dementia-design regulation
found); one unconfirmed lead (IGAS 2023 ERPI Referencial de Boas Práticas) is flagged for a future pass,
not ingested.

Two sources were ingested at **deliberately reduced, honestly-scoped citations** rather than overclaimed:
- **DE — Wegweiser Demenz**: verified to be primarily a directory/referral portal, not a technical design
  standard. Ingested at tier 3 (grey), cited only for its confirmed content (a home-safety checklist and
  institutional resident-group-size norms), not the more granular corridor-geometry/mirror-avoidance claims
  in the original search notes, which could not be confirmed as native to this source.
- **ES — Guía de Práctica Clínica sobre Alzheimer**: verified to address environmental modification only at
  a general level; the granular color-therapy/signage content originally attributed to it actually belongs
  to a different Spanish publication (Fundación Pilares/AFAD). Ingested for the confirmed general content
  only.

**A second anti-fabrication catch, this time on a ramp-gradient table.** Verifying the CTE DB SUA (Spain)
ramp-gradient table for stair-ramp-threshold-biomechanics-accessibility found the search-notes-claimed
table (12%/8%/6%/4%, attributed to "SUA 9") was **wrong** — it conflated two different documents: the real
new-construction table (DB-SUA §SUA-1 4.3, Tabla 4.1: 10%/8%/6% + 2% cross-fall) with a separate
existing-building tolerance table (DA DB-SUA/2: 12%/10%/8%/6%). The existing DB row (`REF-00464`) was
relinked to the slug with the **corrected** figures and section citation, not the original wrong one.
Separately, the Netherlands' Bbl Article 4.30 (a height-tiered ramp table, unique in structure among the 14
jurisdictions searched) was verified and newly ingested, closing that gap.

## The VERIFIED-2 disclosure

All 21 new ingests (10 batch 1 + 11 batch 2) carry `verification_status = 'VERIFIED-2'`, not the
corpus-standard `VERIFIED`. This records honestly that verification rested on **convergent WebSearch
retrieval across multiple independent pages**, not a first-hand primary-document render — direct
`WebFetch` was blocked on nearly every primary source domain attempted across both batches. Batch 2
diagnosed this more precisely than batch 1's "shared proxy issue" framing: multiple independent
investigating agents ran **control-URL tests** (`example.com`, `en.wikipedia.org`, `anthropic.com`) and
found those also returned HTTP 403 — confirming a **session-wide `WebFetch` tooling outage**, not
target-site blocking or a proxy-domain-allowlist issue. This mirrors an existing DB convention
(`REF-00462`'s `DEFERRED-V2-FLIP-VERIFIED` pattern) rather than inventing a new one.

**Anti-fabrication gate held, twice.** Batch 1: one candidate (NF S31-080:2006, France) was dropped after
verification showed it doesn't actually cover classrooms (its real scope is offices/tertiary spaces) — the
search-notes framing was wrong, and rather than ingest a mis-scoped citation, it was replaced with the
correct one (arrêté du 25 avril 2003). Batch 2: the CTE DB SUA (Spain) ramp-gradient table named in the
search notes was verified to be a conflation of two different documents — corrected rather than ingested
as claimed (see the batch 2 section above).

## What this pass does NOT claim

- **Not comprehensive, even after 2 batches.** Tier-0 (the registry backlog), the 2 richest Tier-1 slugs,
  and wayfinding-dementia-spatial-design (now complete for its clearly-named instruments; Portugal is a
  confirmed genuine absence) are done. The remaining Tier-1/2 slugs (luminance-contrast-and-pattern 74
  hits, sensory-room-user-control 42, and four ~20-hit slugs) and the full 14-language × 24-jurisdiction
  sweep are untouched.
- **Jurisdiction ≠ language.** REF-00139 (Singapore) adds jurisdictional/Global-South diversity, not
  language diversity — its source document is in English. Recorded honestly, not folded into the
  non-English count.
- **The Global-South zero-result languages are diagnosed, not fixed — attempted twice, both times
  blocked by tooling, not by the sources' non-existence.** See `global-south-finding.md`. A second
  independent attempt this session to directly read the 9 flagged candidate sources (Indonesian, Hindi,
  Bangladeshi, Arabic-region) again failed to achieve a genuine primary-document read — this time
  precisely diagnosed as a session-wide `WebFetch` outage (control-URL tests against `example.com` also
  403'd). None of the 9 are ingested; they remain flagged leads for a session with working `WebFetch`.

## Next batch (not done this session)

1. Tier-2: luminance-contrast-and-pattern (74), sensory-room-user-control (42), and the four ~20-hit slugs
   (cognitive-wayfinding-design, deaf-spatial-design, mental-health-built-environment,
   accessible-circulation-geometry).
2. The 9 Global-South recoveries flagged in `non-english-coverage-matrix.json`
   (`global_south_zero_result_investigation.*.recovered_not_ingested`) — Indonesian SNI 03-1735-2000 /
   Kepmen PU 468/1998 / Permen PUPR 14/2017, the Hindi translation of India's Harmonised Guidelines,
   Bangladesh's BUAG site / 2013 disability act / BNBC Appendix D, and the Saudi SBC 201 / Dubai Universal
   Design Code / Egyptian Code 601 — need a session with functional `WebFetch` before any can be upgraded
   past search-snippet corroboration. **Do not retry this with WebSearch-only verification again** — two
   independent attempts have already hit the same ceiling; the blocker is tooling, not more searching.
3. Two unconfirmed leads surfaced during batch 2, not yet chased down: the Italian "Linee guida del
   Ministero della Sanità n. 1" companion to DPCM 22/12/1989 (exact date uncertain — 31 gennaio vs 31
   marzo 1994 across sources) and Portugal's IGAS 2023 "ERPI Referencial de Boas Práticas" (content
   unread, may or may not contain dementia-specific design provisions).
4. A corpus-wide audit of whether the *original* 81×19 multilingual sweep's zero-results (beyond the 5
   flagged Global-South languages) are partly a WebFetch-domain-blocking artifact — every investigating
   agent across both batches hit the same blocking pattern independently across unrelated domains/
   languages/sessions, which is now a 2-for-2 pattern worth a dedicated look.
