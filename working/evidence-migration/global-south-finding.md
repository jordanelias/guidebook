# The Global-South zero-result finding — Swahili, Indonesian, Hindi, Bengali, Arabic

*Session: `session_2026-07-19-non-english-research-recovery`. Companion to `equity-dashboard.md` and
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
