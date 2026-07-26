<!-- Created 2026-07-25 from references/bpc/_template.md (CO-0006). -->
<!-- First-touch materialisation: the DB recorded a bpc_path for this slug but no file existed. -->

## energy-conservation-rest-points-seating

**Updated:** 2026-07-25 (batch 2)  **Evidence tier range:** Co-1, 3–5  **Opus synthesis:** NO

### Metadata
```yaml
slug: energy-conservation-rest-points-seating
populations: []            # derived through the axis layer, not asserted here
serves_axes: [AX-STA, AX-PAI, AX-AMB, AX-BAL]
opus_synthesis: false
opus_session: null
status: STUB
last_updated: 2026-07-25
evidence_tier_range: "Co-1, Tier 3–5"
jurisdiction_count: 10     # UK, GB-SCT, US, FI, NO, AU, CA, CZ, FR, HK — ALL Anglophone-published
language_count: 1          # EN — non-EN deferred 3 batches running; now GAP-311
batches_run: 3
co1_source_count: 1        # the slug's thinnest point, unchanged since batch 1
```

**Scope (worked from axes — `DR-2026-07-22-work-from-axes`).** This slug serves the
**sustained-exertion demand** (`AX-STA`; ICF b455, b130 · d230, d450): the environment-side
question of *how far a route requires a person to travel before a usable rest is available, and
whether that rest is usable once reached*. No population umbrella is coined. Provisions are
tracked as separable parameters — **interval**, **seat height**, **armrest**, **setback**,
**transfer space** — because a single "seating" provision serves opposed demands unevenly.

### Concept boundary notes
| Language | Native alias | Map | Warning |
|---|---|---|---|
| EN | rest point / resting place / seating interval | DIRECT | UK "seating" in code text means the *furniture*; "rest point" in the research literature means the *opportunity*. Not interchangeable. |
| — | — | — | Non-EN vocabulary NOT YET BUILT for this slug — deferred, not absent. |

### Best-practice synthesis
**`opus_synthesis: false` — this section carries REDUCED CONFIDENCE. No synthesis is authored
here. Batch 1 established the evidence position only; the doc is queued at the synthesis
boundary.**

**Provisional evidence position (not a synthesis):**

- The **need** for rest points is evidenced at **● full band and is now independently
  replicated**. Batch 1 rested on two Finnish cohorts plus one US qualitative study, which was a
  single-group dependency (GAP-306). Batch 2 closed that gap: five further groups in six
  countries reach the same association by five different methods — GPS-measured routes
  (REF-00955, CA), population survey (REF-00956, CZ), spatial accessibility model (REF-00957, FR),
  qualitative interviews (REF-00958, HK), and a validated audit instrument at n=3,677
  (REF-00959, US). None share authors with the Jyväskylä cluster.
- The **interval value** is evidenced at **○ weak band only**. Batch 2 *sharpened* rather than
  closed this — but its wording was an overclaim, corrected by the 2026-07-26 adversarial pass.
  **What was actually established:** of the six sources batch 2 cited here, only REF-00953 was
  read in full text and REF-00954 fetched; **REF-00955–00959 were abstract-only**, and an
  abstract omitting a spacing figure does not establish the paper contains none. So the honest
  statement is that **no spacing figure has been found in any source read so far**, not that none
  exists in them. See conflict note 1 and GAP-313.
- **Seat usability** determines whether a rest point functions at all. Batch 2 moved this from
  Co-1-versus-standard to **primary-evidence-backed**: REF-00953 demonstrates a single seat
  height cannot serve the population. See conflict note 2 and GAP-307.
- **Anticipatability** is a newly surfaced parameter with no specification anywhere: a rest point
  that cannot be seen or signposted in advance does not support the decision to attempt the
  journey (REF-00954). See GAP-308.
- **Exhaustion is documented as an outcome, in disabled people's own words** (REF-00960, n=26 UK
  interviews): *"a recurrent impact of participants feeling exhausted due to the streetscape
  barriers… participation in society was draining."* This evidences the **demand** (`AX-STA`) that
  the slug exists to serve. It does **not** evidence any provision — see conflict note 6.
- **The dimensional figures are attributed, not primary-verified** (batch 3). The chain behind
  them is now located (REF-00961–00964) but unread. See GAP-310.

**Opus note:** the need/value split remains the governing distinction — do not let ● on the need
migrate onto the interval figure. Batch 2 makes the split sharper, not softer: the need is now
*better* evidenced while the interval is now *demonstrably* unmeasured by anyone.

### Consensus findings
| Finding | Languages with evidence | Jurisdictions confirming | Tier |
|---|---|---|---|
| Lack of resting places associated with reduced QoL / unmet activity need | 1 (EN) | FI | T3 clinical |
| Resting-place availability named as a barrier by disabled people themselves | 1 (EN) | US, UK | T3 clinical, Co-1 |
| Seat height, armrest and setback govern usability of a provided rest | 1 (EN) | UK | T5, Co-1 |

### Divergent findings
| Topic | Position A | Position B | Cause |
|---|---|---|---|
| Rest-point interval | 50 m (DfT *Inclusive Mobility* §4.5, p.31 — urban) | 100 m (same doc, p.124 — countryside) | **Boundary** — context-dependent, single authority |
| Rest-point interval | 50 m (UK, T5) | 20 m / 65 ft (ASLA, US, T3-grey) | **Empirical — unresolved.** Position B unsupported by its own cited source |
| Seat height | 470–480 mm single band (T5) | 380 / 480 / 580 mm plural (Co-1) | **Empirical** — standard assumes one height serves; Co-1 says variety is required |

### NO-DATA / THIN
| Jurisdiction | Language | Reason | Co-1 attempted? | Tier 5 attempted? |
|---|---|---|---|---|
| All except UK/US/FI/NO | non-EN | Batch 1 deliberately EN-only; deferred with reason, not searched-and-empty | No | No |

### Citation mining
| Source | Direction | New sources added |
|---|---|---|
| REF-00951 (ASLA) | backward | 1 (REF-00952) — and established the mis-citation |
| REF-00950 (WfW) | backward | 0 admitted; 5 staged as candidates |
| REF-00945 / REF-00946 | backward/forward | Deferred to batch 2 — single-group cluster, needs adversarial construction |

### Bottom-up findings (functional deficit pass)
*Not yet run — schedule functional deficit pass.*

### Key sources

| REF-ID | Short-key | Authors | Year | Title | Journal/Publisher | DOI/URL | Tier | Lang | Jurisdictions |
|---|---|---|---|---|---|---|---|---|---|
| REF-00945 | rantakokko-qol | Rantakokko M, Iwarsson S, Kauppinen M, Leinonen R, Heikkinen E, Rantanen T | 2010 | Quality of life and barriers in the urban outdoor environment in old age | J Am Geriatr Soc 58(11):2154-9 | 10.1111/j.1532-5415.2010.03143.x | Tier 3 | EN | FI |
| REF-00946 | rantakokko-unmet | Rantakokko M, Iwarsson S, Hirvensalo M, Leinonen R, Heikkinen E, Rantanen T | 2010 | Unmet physical activity need in old age | J Am Geriatr Soc 58(4):707-12 | 10.1111/j.1532-5415.2010.02792.x | Tier 3 | EN | FI |
| REF-00947 | rosenberg-outdoor | Rosenberg DE, Huang DL, Simonovich SD, Belza B | 2012 | Outdoor built environment barriers and facilitators to activity among midlife and older adults with mobility disabilities | The Gerontologist 53(2):268-79 | 10.1093/geront/gns119 | Tier 3 | EN | US |
| REF-00948 | portegijs-barriers | Portegijs E, Rantakokko M, Edgren J, Salpakoski A, Heinonen A, Arkela M, Kallinen M, Rantanen T, Sipilä S | 2013 | Effects of a rehabilitation program on perceived environmental barriers in older patients recovering from hip fracture | BioMed Res Int 2013:769645 | 10.1155/2013/769645 | Tier 3 | EN | FI |
| REF-00949 | dft-inclusive-mobility | Department for Transport | 2021 | Inclusive Mobility: A Guide to Best Practice on Access to Pedestrian and Transport Infrastructure | DfT (Crown copyright) | https://assets.publishing.service.gov.uk/media/61d32bb7d3bf7f1f72b5ffd2/ | Tier 5 | EN | UK |
| REF-00950 | wfw-benches | Wheels for Wellbeing | 2025 | Benches and Seating in Public Spaces | Wheels for Wellbeing (charity no. 1120905) | https://wheelsforwellbeing.org.uk/our-campaigns/resources/benches-and-seating-in-public-spaces/ | Co-1 | EN | UK |
| REF-00951 | asla-streets | American Society of Landscape Architects | n.d. | Universal Design Guide — Streets | ASLA | https://www.asla.org/focus-areas/diversity,-equity,-inclusion/universal-design-guide/universal-design-guide-streets | Tier 3 (grey) | EN | US |
| REF-00952 | norway-walking | (see search log) | 2016 | Improving walking conditions for older adults. A three-step method investigation | European Journal of Ageing | 10.1007/s10433-015-0340-5 | Tier 3 | EN | NO |
| REF-00953 | blackler-seating | Blackler A, Brophy C, O'Reilly M, Chamorro-Koc M | 2018 | Seating in aged care: Physical fit, independence and comfort | SAGE Open Medicine 6:2050312117744925 | 10.1177/2050312117744925 | Tier 3 | EN | AU |
| REF-00954 | tscot-appendix-c | Transport Scotland | n.d. | Inclusive Design in Town Centres and Busy Street Areas — Appendix C: Perspectives of disabled street users | Transport Scotland | (see search log) | Tier 5 | EN | GB-SCT |
| REF-00955 | nouri-gps | Nouri M, Chaudhury H | 2025 | Individual and Neighborhood Characteristics of Walking Activity in People Living With Dementia | J Aging Phys Act 33(5):481-496 | 10.1123/japa.2024-0121 | Tier 3 | EN | CA |
| REF-00956 | maresova-rural | Maresova P, Komarkova L, Horak J, et al. | 2023 | Unveiling Seniors' Perception of Mobility: Urbanization, Region, and Physical Activity | Patient Prefer Adherence 17:3015-3031 | 10.2147/PPA.S426789 | Tier 3 | EN | CZ |
| REF-00957 | amaya-model | Amaya V, Moulaert T, Gwiazdzinski L, Vuillerme N | 2022 | Assessing and Qualifying Neighborhood Walkability for Older Adults | Int J Environ Res Public Health 19(3):1808 | 10.3390/ijerph19031808 | Tier 3 | EN | FR |
| REF-00958 | leung-perceptions | Leung KM, Ou KL, Chung PK, Thøgersen-Ntoumani C | 2021 | Older Adults' Perceptions toward Walking: A Qualitative Study Using a Social-Ecological Model | Int J Environ Res Public Health 18(14):7686 | 10.3390/ijerph18147686 | Tier 3 | EN | HK |
| REF-00959 | sallis-maps-mini | Sallis JF, Cain KL, Conway TL, et al. | 2015 | Is Your Neighborhood Designed to Support Physical Activity? A Brief Streetscape Audit Tool | Prev Chronic Dis 12:E141 | 10.5888/pcd12.150098 | Tier 3 | EN | US |

| REF-00960 | ulahannan-streetscapes | Ulahannan A, Birrell S, Herriotts P | 2025 | Inclusive streetscapes: Embedding disabled people's lived experience into street accessibility | Wellbeing, Space and Society 8:100261 | 10.1016/j.wss.2025.100261 | Tier 3 | EN | GB |
| REF-00961 | holden-fernie-1989 | Holden JM, Fernie GR | 1989 | Specifications for a mass producible static lounge chair for the elderly | Applied Ergonomics 20(1) | 10.1016/0003-6870(89)90007-0 | Tier 3 | EN | CA |
| REF-00962 | holden-fernie-1988 | Holden JM, Fernie GR, Lunau K | 1988 | Chairs for the elderly — design considerations | Applied Ergonomics 19(4) | 10.1016/0003-6870(88)90075-0 | Tier 3 | EN | CA |
| REF-00963 | kothiyal-2001 | Kothiyal K, Tettey S | 2001 | Anthropometry for Design for the Elderly | Int J Occup Saf Ergon 7(1) | 10.1080/10803548.2001.11076474 | Tier 3 | EN | AU |
| REF-00964 | kothiyal-2000 | Kothiyal K, Tettey S | 2000 | Anthropometric data of elderly people in Australia | Applied Ergonomics 31(3) | 10.1016/s0003-6870(99)00052-6 | Tier 3 | EN | AU |

*REF-IDs are stable once emitted. Do not renumber.*

### Conflict notes

**1. The interval figure is weak-band, and the corpus must not double-count it.**
Wheels for Wellbeing (Co-1) states "no more than 50 m" — but its reference list cites DfT
*Inclusive Mobility (2021)*. It is the same figure restated, not independent lived-experience
corroboration. The interval's entire basis is therefore **T5 plus a Co-1 restatement of that
T5**; no primary study in this batch measures the distance at which rest becomes necessary.
Under `tier-system.md` §8 + `DR-2026-07-21` Option A the interval anchors **only at ○**, rendered
as *"best practice as currently known"* with the convergence-not-evidence flag. Rendering it at
● or ◐, or unflagged, is in error.

**2. Seat height variety versus a single band — RESOLVED IN FAVOUR OF VARIETY (batch 2).**
T5 specifies 470–480 mm for the majority of seats. Co-1 (REF-00950) specifies **three** heights
(380 / 480 / 580 mm) plus perch at 700 mm. Batch 1 could only present this as Co-1 asserting
against a standard. **Batch 2 supplies the primary evidence, and it is independent** — REF-00953
is Australian aged-care research that never cites the UK guidance, yet reaches the same
conclusion from measurement:

- Audited seat heights 410–505 mm (facilities) and 423–510 mm (suppliers). **None** would fit a
  5th-percentile older Australian female (popliteal height 330 mm; population mean 379 mm).
- The paper names the mechanism the standard misses: *"The disparity between seat height required
  for STS and seat height required for comfort while seated."* One number cannot satisfy both.
- Its recommendation is variety, not a compromise value: *"Variable height chairs, a range of
  chairs of different heights in each space and footrests"*; Christenson (cited within)
  recommends a **380–457 mm** range — close to the Co-1 380/480/580 mm position.

**Contrast this with conflict note 1, deliberately.** There, a Co-1 source agreeing with a
standard was *not* corroboration, because it cited that standard. Here, a Co-1 source agreeing
with primary research *is* corroboration, because the two are independent and reached the
position by different routes. The independence check must run in both directions or it is just
scepticism pointed at conclusions we dislike.

**Armrests — the standard is too permissive.** REF-00949 says armrests *"are helpful for some."*
REF-00953 observed them *"used 100% of the time regardless of the resident's level of mobility"*
and *"identified as vital by all participants"*, with 90% of observed sit-to-stand transfers
needing more than one attempt. REF-00954 converges independently (push-up bars/handles). On the
evidence, armrests are not an option for some users; they are load-bearing infrastructure for the
transfer. Note also two live dimensional disputes: research cited in REF-00953 puts armrests
~250 mm above the seat for best sit-to-stand support (REF-00949 says ~200 mm), and participants
found *slimmer* armrests easier to grip, contradicting the 120 mm width in the literature.

**3. [UNVERIFIED-QUANT] — the ASLA 20 m figure.**
REF-00951's 20 m/65 ft interval and its "mobility-disabled people" attribution are both
unsupported by REF-00952, its sole cited source, which contains no spacing figure and studied
community-dwelling Norwegians aged 67+ with no disabled cohort. Flagged, not propagated.

**4. Single-height seating is an equity harm, and it is gendered (batch 2, GAP-307).**
The consequence of the note-2 conflict is not discomfort alone. REF-00953: *"shorter residents
are being disadvantaged compared with taller ones, suffering discomfort and possible
musculoskeletal damage while sitting and being put at risk of deep venous thrombosis (DVT) due to
the seating design."* Because women are 69% of permanent aged care in Australia and are likelier
to be shorter, a single-height specification distributes harm by sex. The UK 470–480 mm band sits
inside the range REF-00953 found excludes short users. This is the strongest argument in the slug
for specifying a range rather than a value, and it should be carried into any synthesis.

**5. Provision is not enough — rest points must be anticipatable (batch 2, GAP-308).**
REF-00954 records disabled street users requiring that seating *"be positioned so that it is
possible to see from a distance i.e. to allow journey planning"* and be *"clearly signposted …
to allow them to know when to anticipate potential for breaks in their journey."* Neither
REF-00949 nor REF-00950 specifies visibility, sightline or signage — both specify provision and
setback only. A bench that cannot be seen in advance does not inform the decision of whether the
journey is attemptable at all, which is the decision the sustained-exertion demand actually
turns on. No parameter for this exists anywhere in the corpus.

**6. Ulahannan 2025 evidences the demand, not the provision — recorded to stop a future misread.**
REF-00960 was staged across two batches as probable support for rest-point provision. On reading,
it contains **no seating finding at all**: "benches" appears twice, both as an example of street
furniture in definitional text. It is admitted for its *"feeling exhausted"* theme — one of its
four key impacts — which is lived-experience evidence for the `AX-STA` demand. Its population
match is **EXACT** (26 disabled people, recruited as such) while its topical contribution to
seating is **nil**. Population fit and topical fit are separate axes; conflating them is how a
paper about streetscapes becomes a citation for benches.

**7. The seat and armrest dimensions rest on unread primaries (GAP-310).**
Batch 3 traced REF-00953's figures to REF-00961–00964 and admitted them, but obtained only
Crossref metadata — no full text. So the corpus knows precisely *where* the numbers come from
without having read them at source. Two attributions are additionally **split across companion
papers**: "Holden and Fernie" could be the 1988 paper, the 1989 paper, or both; likewise
Kothiyal & Tettey (2000 dataset vs 2001 design paper). Until read:

- armrest 730 mm from floor / 250 mm above seat / 120 mm width / 120 mm protrusion — **attributed**
- seat depth 376 mm — **attributed**

These must not be cited as primary-sourced. Given batch 1 already caught a professional body
misreporting its own citation (conflict note 3), the reading should actively look for a
discrepancy rather than assume confirmation.

**8. Every jurisdiction reached so far is Anglophone-published (GAP-311).**
Ten jurisdictions sounds broad; all ten were reached through English-language publication. Non-EN
vocabulary has been deferred for three consecutive batches — correctly, since inventing terms
would be back-translation (R11) — but three deferrals is a structural hole, not a scheduling
accident. Public-realm seating traditions in Nordic, German and Japanese practice are likely to
differ substantively, so this is a probable **content** gap, not merely a coverage metric.

**9. Adversarial pass, 2026-07-26 — errors found in this slug's own record.**
Prompted by the owner. The four primaries batch 3 admitted unread were read; every finding below
is a defect in *my* work, not in the sources.

- **The 376 mm seat depth is circular.** REF-00953 writes that "Jean" has a buttock-popliteal
  length of 376 mm and that "Kothiyal and Tettey recommend 376 mm… exactly right for Jean." Both
  halves trace to the **same 171-person Sydney dataset**. It is one number appearing twice, so
  "exactly right" is a tautology, not an independent match. Same double-count class as the 50 m
  interval caught in batch 1 — committed by me this time.
- **REF-00963 and REF-00964 are one study, not two.** Both are Kothiyal & Tettey, n=171, aged
  65+, metropolitan Sydney — a 4-page data note (*Appl Ergon* 2000) and a 20-page treatment
  (*IJOSE* 2001). Batch 3 admitted them as two rows, inflating the apparent source count.
- **The two Holden & Fernie papers are different species.** The 1989 paper is an iterative
  rig-based experiment on elderly inpatients across four chair shapes — a genuine **T1 candidate**,
  deliberately *not* re-tiered upward here because promoting on an abstract is the inflation risk
  this pass exists to check. The 1988 paper is a **discussion piece with no participants** and is
  now **grey-flagged**, so it anchors at the weak band only. Batch 3 filed both identically at T3,
  having read neither.
- **GAP-312:** the GAP-307 equity harm generalises from those 171 Sydney residents, measured a
  quarter-century ago, and its DVT/musculoskeletal consequence is REF-00953's own inference rather
  than a measured outcome. The claim may well hold; the scope was simply never stated.
- **GAP-313:** the structural version of the overclaim above — prose asserted what had been read
  while the row metadata stayed honest. No automated check compares a claim about source *content*
  against the retrieval depth recorded on the rows it cites.
