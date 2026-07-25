<!-- Created 2026-07-25 from references/bpc/_template.md (CO-0006). -->
<!-- First-touch materialisation: the DB recorded a bpc_path for this slug but no file existed. -->

## energy-conservation-rest-points-seating

**Updated:** 2026-07-25  **Evidence tier range:** Co-1, 3–5  **Opus synthesis:** NO

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
jurisdiction_count: 4      # UK, US, FI, NO
language_count: 1          # EN
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

- The **need** for rest points along pedestrian routes is evidenced at **● full band**: absence
  of resting places is associated with reduced quality of life (REF-00945, n=589) and with unmet
  physical-activity need — most strongly among people with walking difficulty (REF-00946,
  n=643) — and is named spontaneously as a barrier by assistive-device users themselves
  (REF-00947, REF-00950).
- The **interval value** is evidenced at **○ weak band only**. See conflict note 1.
- **Seat usability** determines whether a rest point functions at all; a rest point at an
  unusable height is not a rest point. See conflict note 2.

**Opus note:** the need/value split above is the substantive finding and should govern any
later synthesis. Do not let ● on the need migrate onto the interval figure.

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

**2. Seat height variety versus a single band — an unresolved, real conflict.**
T5 specifies 470–480 mm for the majority of seats. Co-1 specifies **three** heights
(380 / 480 / 580 mm) plus perch at 700 mm, on the ground that a single height excludes people at
both ends. These are not reconcilable by picking a midpoint: the Co-1 position is that *variety
itself* is the provision. Per the role-appropriate-authority gate (`tier-system.md` §11), a
functional-need claim of this kind requires Co-1 or Co-2 — which is exactly what REF-00950 is.

**3. [UNVERIFIED-QUANT] — the ASLA 20 m figure.**
REF-00951's 20 m/65 ft interval and its "mobility-disabled people" attribution are both
unsupported by REF-00952, its sole cited source, which contains no spacing figure and studied
community-dwelling Norwegians aged 67+ with no disabled cohort. Flagged, not propagated.
