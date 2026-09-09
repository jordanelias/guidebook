# The Global-South zero-result finding — Swahili, Indonesian, Hindi, Bengali, Arabic

*Sessions: `session_2026-07-19-non-english-research-recovery` (batch 1, the diagnosis below) and
`session_2026-07-19-non-english-research-recovery-batch2` (batch 2, a re-attempted direct-read
verification — see "Batch 2 update" at the end). Companion to `equity-dashboard.md` and
`non-english-coverage-matrix.json`. Per `research-handoff-non-english.md` §4, this is "the sharpest equity
signal in the corpus" — five of nineteen searched languages returned **zero hits across all 81 slugs**, and
the handoff required determining *which* of three causes explains it, honestly, per-language, not assumed.*

## Method

For each language, an independent agent ran real `WebSearch`/`WebFetch` calls: (a) a general native-script
query for the topic domain, to test whether the tooling can reach that language at all; (b) a
naive/romanized/English-transliterated query alongside a properly-localized native query on the same
narrow topic, to isolate query construction as a variable; (c) a targeted check for whether the country/
region in question has *any* formal accessibility-standards literature, in *any* language, to separate
"nothing exists" from "something exists but wasn't found."

## Verdicts

| language | verdict | (a) reachable? | (c) literature exists? |
|---|---|---|---|
| **Swahili (SW)** | mixed — primarily **(c) genuine absence**, secondary (b) | yes (Swahili content is reachable for other topics) | **only in English** — Tanzania's Persons with Disabilities Act 2010 and Kenya's Persons with Disabilities Act + National Building Code 2024 (referencing KS ISO 21542:2011) are real and current, but no Swahili-original or Swahili-translated accessibility building standard was found |
| **Indonesian (ID)** | **(a)/(b) tooling/query construction** — (c) firmly ruled out | yes | yes, extensively — SNI 03-1735-2000 (national standard since 2000), Kepmen PU 468/KPTS/1998, Permen PUPR 14/2017, plus academic literature including a wayfinding paper for a school for visually-disabled students in Surabaya that matches a corpus slug almost verbatim |
| **Hindi (HI)** | **(b) query construction** — (a) ruled out | yes | yes — India's Harmonised Guidelines and Space Standards for Barrier-Free Built Environment (MoHUA), reportedly with an official Hindi translation |
| **Bengali (BN)** | mixed, leaning **(b) query construction** (a subtler failure — wrong terminology, not just wrong script) | yes, once correct terminology used | yes — BNBC 2020 Part 3 Appendix D (Universal Accessibility), the 2013 Rights and Protection of Persons with Disabilities Act, and a dedicated Bengali-language guideline site (BUAG) |
| **Arabic (AR)** | **(b) query construction** — (c) firmly ruled out | yes | yes, substantially — Saudi Arabia's SBC 201/901, Dubai's Universal Design Code, Egypt's Code 601 (under Law 10/2018), plus an IDA compilation of CRPD Article 9 concluding observations |

**Bottom line: 4 of 5 languages (ID, HI, BN, AR) are query-construction failures, not absence — the
literature is there and reachable once the query is right.** Only Swahili shows a genuine content gap, and
even that gap is narrower than "nothing exists": the *legal instruments* exist, they simply were never
written in Swahili.

## Why this matters, stated plainly

The original 81×19 sweep almost certainly built its non-English queries by some form of English-term
translation or transliteration rather than domain-appropriate native terminology. The clearest
demonstration is Arabic: a naive/garbled query on "wayfinding" returned nothing useful, while a properly
phrased Modern Standard Arabic query on the *identical* topic ("نظام الإرشاد والتوجيه المكاني للمكفوفين
داخل المباني") returned a Qatar-based accessibility center's article specifically on indoor navigation for
visually disabled people. Bengali shows an even subtler version of the same failure: the *first* native-
script attempt used a plausible-sounding phrase ("প্রবেশযোগ্য ভবন নকশা," accessible building design) and
got weak results; switching to the term Bangladeshi accessibility documents actually use
("সার্বজনীনগম্য," universal-accessibility) unlocked real content. **Neither of these is a Global-South
absence problem — they are a query-engineering problem that happens to have concentrated its damage on
non-Latin-script, low-cognate-overlap languages.**

## A corpus-wide caveat this investigation surfaced (not previously flagged)

Every one of the five investigating agents independently reported that direct `WebFetch` returned HTTP 403
on a broad set of government/standards-body/NGO domains, spanning unrelated countries and languages
(India, Bangladesh, China, Finland, Norway, Italy, Sweden, Saudi Arabia, UAE, Egypt, Indonesia...) within
the same session window. Cross-checked against the environment's proxy-status endpoint, this reads as a
**shared infrastructure condition this session**, not source-specific unavailability — but it means every
finding in this document (and in the parallel Tier-0/Tier-1 verification work) rests on `WebSearch`
cross-corroboration, not a first-hand primary-document render (disclosed per-source as
`verification_status = VERIFIED-2` where ingested). It also raises a real question for whoever runs the
*next* full-scale sweep: if the original 81×19 multilingual search also depended on `WebFetch` for a
similar domain set, some fraction of the *other* 14 languages' "zero results" for specific slugs — not just
these 5 fully-zero languages — could carry the same artifact. Worth a dedicated audit before the next
scaling pass.

## Recovered but NOT yet ingested

The investigation surfaced real, specific candidate sources for 4 of the 5 languages. None are in
`evidence_sources` yet — each was found via `WebSearch` corroboration only (primary documents 403'd to
direct fetch), so per the anti-fabrication discipline they are recorded here as **leads for a follow-up
verify-and-ingest pass**, not citations:

- **Indonesian:** SNI 03-1735-2000 (national accessibility standard, since 2000); Kepmen PU 468/KPTS/1998;
  Permen PUPR 14/2017.
- **Hindi:** the Ministry of Housing and Urban Affairs' Hindi translation of the Harmonised Guidelines
  (`mohua.gov.in/.../92 Hindi_Corrected.pdf` — title/filename only, not opened).
- **Bengali:** BUAG (`buag.info/accessible-building`, a dedicated Bengali-language accessibility-guideline
  site); Bangladesh's Rights and Protection of Persons with Disabilities Act, 2013 (accessibility clause,
  ~Section 34).
- **Arabic:** Saudi Building Code SBC 201/SBC 901; Dubai Universal Design Code; Egyptian Code for
  Accessibility (Code 601, under Law 10/2018); the IDA compilation of CRPD Article 9 concluding
  observations.
- **Swahili:** none — see verdict above; the honest finding is that no Swahili-language accessibility-
  standard document was found because none appears to exist (the underlying English-language Kenyan/
  Tanzanian instruments are already indirectly reachable via their English citations, which is a separate,
  already-tracked gap, not a Swahili-specific one).

Full URLs and per-source status are in `non-english-coverage-matrix.json` →
`global_south_zero_result_investigation`.

## Batch 2 update — a second attempt, still blocked, now precisely diagnosed

Batch 2 dispatched two independent agents to make a **fresh, second attempt** at directly opening and
reading (not just WebSearch-corroborating) all 9 recovered-not-ingested candidates above. **Result: 0/9
achieved a genuine direct read** — the same outcome as batch 1, but this time the cause was pinned down
precisely. Both agents ran **control-URL tests** — fetching `https://example.com`,
`https://en.wikipedia.org`, `https://www.anthropic.com` — and found these trivial, unrelated targets
*also* returned HTTP 403, with `curl`'s CONNECT tunnel rejected for nearly every host attempted. This
confirms a **session-wide `WebFetch` tooling outage**, not target-site blocking, not a domain-allowlist
policy, and — importantly — **not evidence about whether the underlying sources are real**. `WebSearch`
(a different retrieval path) continued to work throughout and remains the sole basis for every finding in
this document.

One genuinely new thing surfaced during the re-attempt: the Indonesian-search agent found search snippets
suggesting SNI 03-1735-2000's actual title may include a fire-hazard-prevention qualifier
("...untuk Pencegahan Bahaya Kebakaran Pada Bangunan Gedung") not present in the original candidate
description — which would mean its primary scope is fire-egress access, not general disability
accessibility. This needs a direct read to resolve one way or the other; it is **not** assumed to be either
scope on the strength of a search snippet.

**Recommendation for whoever picks this up next: do not attempt a third `WebSearch`-only verification
pass.** Two independent attempts have already hit the same ceiling for the same reason — the blocker is
tooling, not insufficient searching. Retry only from a session with confirmed-functional `WebFetch`
(verify against a trivial control URL first, before spending effort on the actual targets).

## Batch 6 update — resolved, not by waiting for WebFetch, but by upgrading the standard of care

`WebFetch` failed the same control-URL test a **3rd consecutive session** (batches 1-2, batch 4, batch 6
all independently confirmed `example.com` returning 403). At that point, continuing to wait for the tool
to start working was no longer a defensible plan — batch 5's adversarial review had already validated
that the `WebSearch`-corroboration + `VERIFIED-2` pattern used throughout this whole effort is reliable
(7 of 8 sampled sources confirmed accurate by an independent, refutation-seeking reviewer). Batch 6
applied that same standard, deliberately more rigorously than the first pass — and it changed the outcome
for 7 of the 9 leads:

- **Ingested (4):** Saudi Arabia's SBC 201, Egypt's Code 601, UAE/Dubai's Universal Design Code, and
  Bangladesh's 2013 Disability Rights Act (the last with an explicit, load-bearing caveat about weak
  real-world enforcement — see `equity-dashboard.md`'s batch 6 section). Four genuinely new jurisdictions
  for this corpus.
- **Correctly excluded on closer inspection (2):** Indonesia's SNI 03-1735-2000 turned out, once its
  *complete* official title was retrieved rather than a truncated snippet, to be a **fire-safety egress
  standard** — nothing to do with disability accessibility. It was never actually a Global-South-equity
  finding at all; it was a scope-matching error in the original lead, caught by insisting on the full
  title before ingesting anything. BUAG (Bangladesh) was confirmed to be a secondary Bengali-language
  explainer of BNBC 2020, not an independent primary standard citable on its own — and its publisher
  remains unconfirmed after two separate investigation rounds.
- **Correctly left alone, not chased further (1):** the Hindi MoHUA PDF lead could not even be re-located
  via `WebSearch` this time (four distinct queries, including the exact filename, all came up empty), and
  its relationship to the DB's already-present `REF-00509` (India's 2021 Harmonised Guidelines) is
  genuinely undetermined — ingesting it now would risk either double-counting an existing document or
  citing a file that may not be independently retrievable at all. Not ingested.
- **Not re-investigated in batch 6 (2):** Indonesia's Kepmen PU 468/1998 and Permen PUPR 14/2017 — these
  two were simply not revisited that batch (effort went to the higher-confidence Arabic-region and
  Bangladesh leads); resolved in batch 7 (below).

The honest lesson here is not "WebSearch-only verification is fine, ignore the earlier warning" — it's
that **the standard of care matters more than the tool**. The earlier "do not retry with WebSearch-only
verification" warning was really about not repeating the *same shallow pass* expecting a different
result. Batch 6 didn't repeat the pass — it insisted on complete titles, explicit enforceability findings,
and honest "could not confirm" outcomes where the evidence ran out, and that additional rigor is what
actually moved 7 of 9 leads to a resolved state.

## Batch 7 update — the final 2 leads resolved; all 9 original leads now closed

`WebFetch` failed its control-URL test a **4th consecutive session**. Batch 7 applied the same
batch-5/batch-6-validated WebSearch-only standard to the two Indonesian leads batch 6 left untouched,
explicitly re-applying the SNI 03-1735-2000 lesson (get the COMPLETE official title before concluding
scope):

- **Kepmen PU No. 468/KPTS/1998** — complete official title confirmed genuinely disability-accessibility
  ("Persyaratan Teknis Aksesibilitas pada Bangunan Umum dan Lingkungan," no hidden qualifier like the SNI
  fire-safety trap). However, its legal status resolved to **superseded**: the JDIH BPK RI record for its
  successor, Permen PU No. 30/PRT/M/2006, explicitly states "[Kepmen 468/KPTS/1998] dicabut dan dinyatakan
  tidak berlaku" (revoked and declared no longer in effect), effective 1 December 2006. Per this project's
  code-currency discipline, a revoked regulation is not ingested as an active citation. **Not ingested.**
- **Permen PUPR No. 14/PRT/M/2017** — complete official title confirmed genuinely disability-accessibility
  ("Persyaratan Kemudahan Bangunan Gedung"), publisher and scope confirmed across 3 independent official/
  government sources (Kementerian PUPR Cipta Karya, peraturan.go.id, JDIH BPK RI). Legal status: "Berlaku"
  (in force) per the JDIH BPK RI status field (confirmed via WebSearch snippet, not a direct page read —
  disclosed as a medium-confidence caveat on this specific point). No source found PP 16/2021 (the later
  Cipta Kerja-era implementing regulation) explicitly revoking it; it appears to remain the operative
  ministerial technical regulation. **Ingested as REF-00770**, tier 6 / `code` (statutory, legally
  enforceable, matching `governance/tier-system.md`'s T6 definition) — Indonesia's first jurisdiction in
  this corpus.

**All 9 original Global-South leads are now resolved: 5 ingested (Saudi Arabia, Egypt, UAE, Bangladesh,
Indonesia), 4 correctly excluded** (Indonesia's SNI 03-1735-2000 — wrong scope; Bangladesh's BUAG —
secondary source, unconfirmed publisher; India's Hindi MoHUA PDF — could not be re-located, relationship
to existing REF-00509 undetermined; Indonesia's Kepmen 468/1998 — superseded). Swahili's genuine-absence
finding stands unchanged (no Swahili-language accessibility standard exists to ingest).

### A small companion loose end resolved the same batch (not a Global-South item)

Two unrelated small items were resolved alongside the Indonesian leads, using the same WebSearch-only
standard: the exact date of Italy's companion "Linee guida del Ministero della Sanità n. 1" document
(REF-00746's `notes` previously recorded this as uncertain, "31 gennaio vs 31 marzo 1994") was confirmed
via multiple convergent independent sources to be **31 marzo 1994** — the "31 gennaio" variant appears to
be a corruption; a separate, genuine **31 maggio 1994** date is when the guidelines were transmitted to
the Regions, which likely fed the original date confusion. The Legge 23 dicembre 1994, n. 724 art. 3
cross-reference is now confirmed (not just suspected). Separately, Portugal's IGAS 2023 ERPI referencial
was checked for dementia-specific built-environment content and found to contain none — it is
clinical/organizational health-care guidance (co-produced with Portugal's medical/nursing/pharmacy
professional orders, no architectural body involved), with the physical/spatial specifications that
surfaced in early searches actually tracing to a *different* document (Portaria n.º 349/2023, the ERPI
licensing regulation) and an ArchDaily neuroarchitecture article, neither of which is dementia-specific
building-design regulation either. This **corroborates, not overturns**, Portugal's existing
genuine-absence finding for `wayfinding-dementia-spatial-design` — a valid, honest research result, not a
gap needing a fix. No DB change was needed for this item.
