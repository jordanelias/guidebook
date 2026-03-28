# Connection Register

**Created:** 2026-03-26 18:10  
**Last updated:** 2026-03-28 21:45

**Disposition lifecycle (per project-standards Rule 2026-03-27):**

| Status | Meaning |
|---|---|
| PENDING | Identified; not yet consumed by any skill |
| CONSUMED | Incorporated into item specification (session ref recorded) |
| DEFERRED | Valid but deferred to future phase (reason recorded) |
| SUPERSEDED | Overtaken by subsequent research or decision |
| CLOSED | No action required |

All existing entries: **PENDING** (disposition tracking added 2026-03-27).

**CO-0003 terminology (2026-03-28 21:30):** "Cross-population" is retired. Each connection entry describes one of:
- **[INTRA-INDIVIDUAL]** — co-occurring disabilities in one person (e.g., DEM+MOB+PAIN). Resolution: Tier 2 OT assessment within Tier 1 ranges.
- **[INTER-GROUP]** — different people with different primary conditions in the same space. Resolution: Tier 0/1 architectural (zoning, individual controls, spatial separation).
- **[BOTH]** — provision serves both cases.

Tagging of existing entries (CON-0001–0038) is scheduled for Phase 2C Session 9 (GAP-CO03-09). New entries use the tagging from creation.

---

## CON-0001 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** HIGH
**Type:** INTER-GROUP  
**Populations involved:** DEM, VIS, DBL, IntD, NDV/AUT  
**Items involved:** D-02, D-06, D-08, D-09, C-04  
**Gap register items:** GAP-S4-R03, GAP-S4-R04, GAP-S4-R05, GAP-S4-R07, GAP-S4-N01, GAP-S4-N02, GAP-S4-N04, GAP-S4-N06, GAP-NEW-05  

### Connection description
Five populations converge on consistent, legible, loop-based circulation with no dead-ends — from independent clinical rationales currently siloed in separate BPC entries:

- **DEM:** Cognitive mapping failure; loop circulation reduces disorientation (Marquardt 2011; DSDC EADDAT; 10+ jurisdictions). Floor plan is the most influential environmental factor (Bowes et al. 2019).
- **VIS:** Tactile landmark consistency enables spatial memory; unpredictable layout changes are high-risk (ISO 23599; TWSI systems).
- **DBL:** Consistent spatial layout is a core safety requirement; unfamiliar changes are high-risk (DbI guidelines, Tier 2). Tactile memory navigation relies on furniture permanence.
- **IntD:** One-way legible routes with ≤3 decision points per segment; colour-zone wayfinding; pictogram + single-word signage (expert consensus, no quantified standard).
- **NDV/AUT:** Sequential/one-directional circulation preferred; compartmentalised zones; transition alcoves at zone boundaries (Mostafa 2023; Black et al. 2022).

Convergence is strong enough — five populations, 10+ jurisdictions, Tier 2–5 evidence — to warrant a Tier 0 universal specification.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Marquardt 2011 | 3 | DEM | ALL (Tier 0 universal) |
| DSDC EADDAT 2022 | 5 | DEM | ALL |
| ISO 23599:2019 | 4 | VIS, DBL | ALL |
| DbI World Access guidelines | 2 | DBL | ALL |
| Mostafa 2023 (ASPECTSS) | 3 | NDV/AUT | ALL |
| Bowes, Dawson, Greasley-Adams 2019 | 3 | DEM | ALL |
| Black, Sharma & Roberts 2022 | 3 | NDV/AUT | ALL |

### Proposed synthesis direction
Create Tier 0 universal circulation legibility specification: all buildings to provide consistent, predictable circulation geometry (loop or single-path, no dead-ends); consistent furniture arrangement within room types (no mirror-image pairs); 3D object landmarks at every decision point. Population-specific overlays at Tier 1. Resolves root cause of 8+ gap items.

### Disposition
- [x] HIGH → item-specification-writer briefing

---

## CON-0002 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** HIGH
**Type:** BOTH  
**Populations involved:** NDV, MH, OFS, PAIN  
**Items involved:** A-16, H-02  
**Gap register items:** GAP-SRS-01, GAP-B4-07, GAP-NEW-11  

### Connection description
sensory-relief-space-design BPC (NDV primary) and mental-health-built-environment BPC (MH primary) specify substantially overlapping rooms — both require user-controlled lighting (2700–6500 K), acoustic treatment (RT60 ≤0.3 s), safe retreat, ≥8–9 m². OFS BPC requires reclined posture rest spaces. PAIN BPC requires seated/recumbent provision. Amaze/Architecture & Access (2025) explicitly extends A-16 to ADHD/OFS/PAIN comorbidities and trauma.

Currently A-16 is NDV-only. MH "de-escalation room" described as distinct. Evidence does not support two separate room types — supports single multi-population sensory relief / safe retreat spec with population-specific configuration notes.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Unwin, Powell & Jones 2022/2023 | 3 | NDV/AUT | NDV, MH, OFS, PAIN |
| Architecture & Access / Amaze 2025 | 3/5 | NDV (extends to OFS/PAIN) | NDV, MH, OFS, PAIN |
| PAS 6463:2022 | 5 | NDV | NDV, MH |
| CDC ME/CFS guidelines | Co-1 | OFS | OFS, PAIN |

### Proposed synthesis direction
Expand A-16 to carry NDV, MH, OFS, PAIN as co-primary populations. Retire separate MH "de-escalation room" concept. Add OFS reclined seating and PAIN cushioned seating within A-16. Elevate H-02 to primary cross-reference (per GAP-SRS-01). Collapses three separate specs into one.

### Disposition
- [x] HIGH → item-specification-writer briefing

---

## CON-0003 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** HIGH
**Type:** BOTH  
**Populations involved:** MOB, PAIN, OFS, DEM, NEU  
**Items involved:** G-03, G-04, G-05  
**Gap register items:** GAP-B4-05, GAP-B4-07  

### Connection description
Grab bar provisions (G-03/G-04) coded MOB primary. Three other populations have clinical rationale documented in BPC but not connected to grab bar items:

- **PAIN:** Pain on gripping/joint loading during transfers. Grab bars serve stable support during posture transitions.
- **OFS:** Orthostatic intolerance requires support during sit-to-stand. CDC ME/CFS and Newcastle POTS 2018 identify postural support need.
- **DEM:** Fall prevention; spatial anchoring. Clemson et al. 2023 Cochrane (22 RCTs, 8463 participants, 38% fall reduction).
- **NEU:** Balance impairment; ABI/stroke require bilateral support.

650–900mm height range already serves all five populations. Populations simply not listed.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Clemson et al. 2023 Cochrane CD013258 | 3 | MOB (fall prevention) | DEM, NEU |
| CDC ME/CFS guidelines | Co-1 | OFS | OFS (grab bar use) |
| Newcastle POTS 2018 | 4 | OFS | OFS (postural support) |
| Staud 2011 | 3 | PAIN | PAIN (grip support) |

### Proposed synthesis direction
Add PAIN, OFS, DEM, NEU as co-populations for G-03/G-04. No specification change — range already accommodates all. Population-specific rationale notes only.

### Disposition
- [x] HIGH → item-specification-writer briefing

---

## CON-0004 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** HIGH
**Type:** BOTH  
**Populations involved:** OFS, PAIN, MOB  
**Items involved:** F-05, G-05, NEW (reclining seating)  
**Gap register items:** GAP-B4-03, GAP-B4-07, GAP-B4-08, GAP-NEW-11  

### Connection description
Four OPEN gap items share root cause: seated/reclined work and rest provision for fatigue/pain populations not systematically addressed. Evidence distributed across three BPC entries (OFS, PAIN, MOB) but not unified. A single new item — adjustable posture seating provision — resolves all four gaps.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| CDC ME/CFS guidelines | Co-1 | OFS | OFS, PAIN, MOB |
| Kos et al. 2015 AJOT (energy conservation RCT) | 1 | OFS | OFS, PAIN |
| BS 8300:2018 (seating at intervals) | 5 | ALL | OFS, PAIN primary |

### Proposed synthesis direction
Create single new item: Adjustable Posture Seating Provision. Spec: ≥1 reclined/tilt seat per primary zone (≥120° recline with footrest); all reception counters with adjacent seated waiting ≤3m; all shared work surfaces with ≥1 seated-height station. Collapses GAP-B4-03, B4-07, B4-08, NEW-11.

### Disposition
- [x] HIGH → item-specification-writer briefing

---

## CON-0005 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** MODERATE
**Type:** BOTH  
**Populations involved:** MOB, PAIN, OFS  
**Items involved:** A-09, G-08 (proposed)  
**Gap register items:** GAP-B4-09, GAP-IMPL-02  

### Connection description
Floor-vibration BPC: resilient flooring is primary intervention for MOB wheelchair WBV. GAP-B4-09: cushioned flooring for PAIN joint impact (expert consensus, THIN). MOB evidence base for resilient flooring (Garcia-Mendez 2013; Larivière et al.) substantially stronger than PAIN evidence. Design solution identical — extending MOB spec to carry PAIN co-population requires only clinical rationale link.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Garcia-Mendez 2013 | 3 | MOB (WBV) | MOB, PAIN |
| Staud 2011 | 3 | PAIN | PAIN (flooring rationale) |

### Proposed synthesis direction
Add PAIN as co-population for A-09 resilient flooring. THIN flag for PAIN-specific evidence; strong for MOB. Resolves GAP-B4-09 without requiring independent PAIN flooring evidence.

### Disposition
- [ ] MODERATE → P2 gap item

---

## CON-0006 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** MODERATE
**Type:** BOTH  
**Populations involved:** DEM, NEU, NDV, MH, OFS  
**Items involved:** B-01 (circadian lighting)  
**Gap register items:** GAP-034  

### Connection description
Circadian lighting (≥250 melanopic EDI daytime) specified for DEM/NEU. MH BPC and OFS BPC do not mention circadian lighting despite clear clinical relevance: MH/PTSD sleep disruption and OFS fatigue cycle disruption both benefit from circadian entrainment. Population coding update only — no specification change.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Brown et al. 2022 | 3 | ALL (general) | MH, OFS explicit |
| CDC ME/CFS (sleep disruption) | Co-1 | OFS | OFS circadian |

### Proposed synthesis direction
Add MH and OFS as explicit co-populations for B-01.

### Disposition
- [ ] MODERATE → P2 gap item

---

## CON-0007 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** HIGH
**Type:** INTER-GROUP  
**Populations involved:** DEAF, DBL, MH, DEM  
**Items involved:** E-01, E-06, E-08  
**Gap register items:** GAP-STEP6-03, GAP-S4-R07  

### Connection description
Three populations require circulation wide enough for two people side-by-side (one providing communication or support) from independent rationales:

- **DEAF:** 2440mm for signed conversation (ASL proxemics).
- **DBL:** ≥1500mm for intervenor accompaniment (Nordic ledsagarservice statutory right).
- **MH:** Support person/companion accompaniment (PTSD, agoraphobia). Not currently specified.
- **DEM:** Carer accompaniment on all routes; escort width implicit, not specified.

2440mm DEAF specification accommodates all. Currently coded DEAF-only.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Deaf-spatial-design BPC (ASL proxemics) | Co-1 | DEAF | DEAF, DBL, MH, DEM |
| Nordic ledsagarservice statutes | 5 | DBL | DBL |
| DbI World Access guidelines | 2 | DBL | DBL, DEM |

### Proposed synthesis direction
Create Tier 0 companion-width specification: primary routes ≥1500mm clear (best practice 2440mm where DEAF primary). Unifies siloed specifications; resolves GAP-STEP6-03.

### Disposition
- [x] HIGH → item-specification-writer briefing

---

## CON-0008 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** MODERATE
**Type:** BOTH  
**Populations involved:** PAIN, OFS, NEU  
**Items involved:** A-02, A-08, A-13  
**Gap register items:** GAP-RAP-01  

### Connection description
Room acoustic items coded for DEAF, DEM, NDV populations. OFS BPC identifies acoustic sensitivity ("no forced air as sole source — acoustic trigger concern"). PAIN BPC: Geisser et al. 2021 identifies hyperacusis as fibromyalgia symptom. Neither population coded on acoustic items.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Geisser et al. 2021 | 3 | PAIN | PAIN acoustic |
| CDC ME/CFS (sensory sensitivity) | Co-1 | OFS | OFS acoustic |
| PAS 6463:2022 | 5 | NDV | NDV, OFS, PAIN |

### Proposed synthesis direction
Add PAIN and OFS as co-populations for A-02/A-08/A-13 with THIN-POPULATION-SPEC disclosure.

### Disposition
- [ ] MODERATE → P2 gap item

---

## CON-0009 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** MODERATE
**Type:** BOTH  
**Populations involved:** MOB, OFS, PAIN  
**Items involved:** Threshold items (residential-entry-and-threshold)  
**Gap register items:** NONE  

### Connection description
Entry/threshold BPC specifies level access for MOB/wheelchair. OFS (energy conservation — steps trigger PEM) and PAIN (joint loading on steps) benefit but are not listed. Specification values unchanged; population coding update only.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Kos et al. 2015 AJOT | 1 | OFS (behavioural) | OFS (architectural) |
| CDC ME/CFS (PEM from exertion) | Co-1 | OFS | OFS |

### Proposed synthesis direction
Add OFS and PAIN as co-populations for entry/threshold items.

### Disposition
- [ ] MODERATE → P2 gap item

---

## CON-0010 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** HIGH
**Type:** INTER-GROUP  
**Populations involved:** DEM, OFS, NDV, MH  
**Items involved:** BIO-01–BIO-05, A-16  
**Gap register items:** NONE  

### Connection description
Three BPC entries independently identify outdoor/nature spaces as therapeutic without cross-reference: biophilic-design (nature exposure reduces stress/pain — Al Khatib 2024 SR); dementia (outdoor loop routes reduce agitation — Danish evidence); OFS (rest spaces at ≤50m — no nature connection despite restorative potential); sensory-relief (transition zone — no outdoor decompression link). Convergence: outdoor therapeutic spaces serve DEM + OFS + NDV + MH through single spatial solution.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Latiff et al. 2024 (NDV outdoor decompression) | Co-1 | NDV | NDV, MH |
| Al Khatib et al. 2024 (biophilic SR, 61 sources) | 3 | ALL (healthcare) | DEM, OFS, MH |
| Danish DEM loop garden evidence | Co-1 | DEM | DEM, OFS |

### Proposed synthesis direction
Cross-reference biophilic outdoor items with DEM garden loop, OFS rest provision, NDV decompression, MH nature exposure. Consider unified "therapeutic outdoor space" specification.

### Disposition
- [x] HIGH → item-specification-writer briefing

---

## CON-0011 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** HIGH
**Type:** INTER-GROUP  
**Populations involved:** DBL, IntD  
**Items involved:** All room matrix items  
**Gap register items:** GAP-S4-R01 through GAP-S4-N07, REVIEW-S4-01  

### Connection description
15 OPEN gap items share single root cause: DBL and IntD not in population framework when room matrices were written. Both populations' requirements now documented in BPC. Single systematic insertion pass resolves all 15 gaps. Shared requirement (consistent layout) overlaps with CON-0001, strengthening Tier 0 case.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| DbI World Access guidelines | 2 | DBL | DBL (all rooms) |
| ISO 23599:2019 | 4 | DBL (circulation) | DBL (all rooms) |
| IntD BPC | 4–5 | IntD | IntD (all rooms) |
| NICE NG93 | 5 | IntD (healthcare) | IntD (all rooms) |

### Proposed synthesis direction
Single systematic item-specification-writer pass inserting DBL and IntD into all 16 room matrices using CON-0001 Tier 0 anchor. Resolves all 15 gaps in one operation.

### Disposition
- [x] HIGH → item-specification-writer briefing

---

## CON-0012 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** MODERATE
**Type:** INTER-GROUP  
**Populations involved:** ALL  
**Items involved:** DAR items  
**Gap register items:** NONE  

### Connection description
IT DM 236/89 adattabilità concept (walls reinforced for future grab bars, bidet removable, bath-to-shower convertibility at design stage) is a direct statutory parallel to DAR. Possibly the only national-level statutory implementation of the DAR principle. Not cross-referenced in residential-dar-provisions-priority-register BPC.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| IT DM 236/89 | 6 | MOB (statutory) | ALL (DAR cross-reference) |

### Proposed synthesis direction
Add Italian adattabilità as statutory precedent in DAR specification. Cross-reference in Part 1 DAR doctrine.

### Disposition
- [ ] MODERATE → P2 gap item

---

## CON-0013 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** MODERATE
**Type:** BOTH  
**Populations involved:** MOB, OFS, PAIN, LPA  
**Items involved:** Kitchen items  
**Gap register items:** GAP-B4-07, GAP-076  

### Connection description
Kitchen height-adjustable worktop (650–900mm) specified for MOB. OFS and PAIN not listed despite requiring seated work provision (energy conservation; joint-loading reduction).

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| ADA / NL WMO-keuken | 5–6 | MOB | MOB, OFS, PAIN |
| Kos et al. 2015 | 1 | OFS (behavioural) | OFS (architectural) |

### Proposed synthesis direction
Add OFS and PAIN as co-populations for kitchen adjustable worktop. Partially resolves GAP-B4-07.

### Disposition
- [ ] MODERATE → P2 gap item

---

## CON-0014 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** HIGH
**Type:** INTER-GROUP  
**Populations involved:** DEAF, DBL, NEU, NDV  
**Items involved:** B-10, visual-fire-alarm items  
**Gap register items:** GAP-035  

### Connection description
Visual-fire-alarm conflict resolution (DEAF/DBL need strobes; NEU/NDV at seizure risk from same) relies on vibrotactile as alternative channel for photosensitive populations. GAP-035: no jurisdiction specifies vibrotactile device type, intensity, latency, or coverage. Conflict resolution is principled but unimplementable without vibrotactile specification.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| RNID / HLAA / Bufdir recommendations | Co-1/2 | DEAF (vibrotactile) | DEAF, DBL, NEU |

### Proposed synthesis direction
New item: Vibrotactile Alerting Device (sleeping areas) — minimum vibration intensity, latency ≤3 s, coverage all sleeping rooms where DEAF/DBL/photosensitive populations primary. Completes visual-fire-alarm conflict resolution chain; resolves GAP-035.

### Disposition
- [x] HIGH → item-specification-writer briefing

---

## CON-0015 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** MODERATE
**Type:** BOTH  
**Populations involved:** NDV, OFS, PAIN, MH  
**Items involved:** F-04, F-02  
**Gap register items:** NONE  

### Connection description
Air quality / fragrance-free specifications carry OFS, NDV, NEU, PAIN. MH absent despite TID framework emphasis on environmental predictability and trigger avoidance. Chemical stimuli can trigger PTSD hyperarousal.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Steinemann 2018 | 3 | General | MH |
| TID framework | 2–3 | MH | MH (chemical triggers) |

### Proposed synthesis direction
Add MH as co-population for F-02/F-04.

### Disposition
- [ ] MODERATE → P2 gap item

---

## CON-0016 [2026-03-26 18:10]

**Mode:** Internal  
**Confidence:** SPECULATIVE
**Type:** INTER-GROUP  
**Populations involved:** DEM, VIS, NDV/AUT  
**Items involved:** C-04, D-02  
**Gap register items:** GAP-032, GAP-033  

### Connection description
Luminance contrast (VIS), floor pattern contraindication (DEM), and TWSI placement (VIS/DBL) interact in same physical space. DEM ≤10 LRV floor adjacency and VIS ≥30% TWSI contrast are complementary on plain floors but conflict on patterned flooring. Coordination note needed; not a new specification.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Lukman et al. 2020 | 3 | VIS | VIS, DEM interaction |
| DSDC (dark mats = holes) | Co-1 | DEM | DEM floor treatment |

### Proposed synthesis direction
Cross-reference note in C-04: DEM floor treatment and VIS TWSI contrast are complementary when coordinated; patterned flooring conflicts with both.

### Disposition
- [ ] SPECULATIVE → P3 gap item


---

## CON-0017 [2026-03-26 18:30]

**Mode:** Internal
**Confidence:** HIGH
**Type:** BOTH
**Populations involved:** NDV/AUT, NDV/MH, OFS, DEM, NEU, DEAF, VIS
**Items involved:** H-02 (Individual Environmental Control), A-16, B-06, B-07
**Gap register items:** NONE (new Tier 0 candidate)

### Connection description
"User control over environment" is documented as the single highest-impact provision across NDV subtypes (NDV BPC), the primary design requirement for sensory rooms (sensory-room-user-control BPC), a core requirement for NDV/MH retreat rooms, and essential for OFS temperature/lighting management. DEM benefits from consistent but adjustable environments. DEAF users benefit from lighting control for sign language visibility. The pattern repeats in 5+ population BPCs but is never synthesized into a cross-population design principle. No specification currently states that occupant environmental control is a Tier 0 universal provision. It is siloed as population-specific within each category. This is arguably the strongest Tier 0 candidate in the guidebook — evidenced across more populations than any other single provision.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| NDV BPC — "single highest-impact provision" | Co-1, Tier 4 | NDV/AUT, NDV/ADHD, NDV/SENS | ALL — Tier 0 candidate |
| Sensory room user control BPC — H-02 PRIMARY | Co-1 | NDV/AUT | ALL |
| OFS BPC — adjustable seating/temperature/lighting | Co-1/Tier 3 | OFS | ALL |
| NDV/MH BPC — user-adjustable lighting/acoustics | Tier 2–4 | NDV/MH | ALL |
| PAS 6463:2022 | Tier 5 | NDV, DEM | ALL |
| DeafSpace — lighting control for signing | Co-1/Tier 2 | DEAF | ALL |

### Proposed synthesis direction
Elevate H-02 (Individual Environmental Control) to Tier 0 universal design. Specification: all primary occupied spaces to provide occupant-adjustable lighting (level and CCT), acoustic management (operable panels or zones), and local thermal control. Population-specific overlays at Tier 1 define parameter ranges. This does not increase cost significantly — dimmer switches and local thermostats are standard building components. The specification change is from "optional upgrade" to "baseline provision."

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

## CON-0018 [2026-03-26 18:30]

**Mode:** Internal
**Confidence:** HIGH
**Type:** BOTH
**Populations involved:** DEM, NEU, NDV/AUT, OFS
**Items involved:** Cognitive wayfinding BPC, DEM BPC, NEU BPC
**Gap register items:** NONE (new Tier 0 candidate)

### Connection description
"Toilet visible from primary occupied space" is independently evidenced for DEM (Marquardt 2011 — reduces distress and incontinence; Davis & Weisbeck 2016), confirmed in cognitive wayfinding BPC for DEM and NDV, and functionally relevant for NEU (landmark-based navigation is the most effective compensatory strategy — Claessen & van der Ham 2017). OFS benefits from reduced navigation distance when symptomatic. The principle generalises: "essential facility visibility from primary occupation point" is a spatial planning principle serving DEM, NEU, NDV, and OFS simultaneously. It is currently documented only as a DEM-specific wayfinding provision in care settings. In residential settings, it would mean every dwelling's primary living area has direct sightline to the bathroom door — a provision that constitutes good spatial design for all occupants.

Note: CON-0001 covers loop circulation and legible layout; this connection is specifically about sightline to essential facilities, which is a distinct spatial planning principle.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Marquardt 2011 | Tier 3 | DEM | NEU, NDV/AUT, OFS |
| Davis & Weisbeck 2016 | Tier 3 | DEM | NEU |
| Claessen & van der Ham 2017 | Tier 1 | NEU | DEM confirmation |
| DSDC EADDAT 2022 | Tier 5 | DEM | Cross-population |
| Cognitive wayfinding BPC | Synthesis | DEM, NDV | NEU, OFS |

### Proposed synthesis direction
Elevate "essential facility sightline" to a Tier 0 residential design principle: WC/bathroom door visible from main living area without navigational decision points. In care settings, this is already standard for DEM; in residential design, it is not specified. The evidence supports it as a universal benefit.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

## CON-0019 [2026-03-26 18:30]

**Mode:** Internal
**Confidence:** HIGH
**Type:** BOTH
**Populations involved:** NDV/AUT, NDV/MH, OFS, PAIN
**Items involved:** A-16 (Sensory Room), NDV/MH retreat room, OFS rest space
**Gap register items:** GAP-NEW-11, GAP-B4-08

### Connection description
Extends CON-0002 (sensory/MH overlap) and CON-0004 (seated/reclined provision). Four populations independently require a low-stimulation refuge space: NDV/AUT (sensory quiet room A-16), NDV/MH (de-escalation/safe retreat ≥9 m²), OFS (low-stimulation rest space), PAIN (energy conservation rest point). These share overlapping functional requirements: low acoustic load (RT60 ≤0.4 s), user-controlled lighting, no through-traffic, accessible location. Currently specified as four distinct room types across four BPC entries. The synthesis: a single "environmental refuge" at Tier 0 — every occupied floor plate includes one refuge room — with population-specific overlays at Tier 1 (NDV/AUT: sensory equipment + blackout; NDV/MH: de-escalation furnishing; OFS: reclined seating + semi-recumbent positioning; PAIN: cushioned seating + thermal control). This resolves GAP-NEW-11 and GAP-B4-08 simultaneously within a unified spatial provision.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| PAS 6463:2022 | Tier 5 | NDV/AUT, DEM | OFS, PAIN, NDV/MH |
| OFS BPC rest space provision | Co-1/Tier 3 | OFS | NDV/AUT, NDV/MH, PAIN |
| NDV/MH BPC retreat room | Tier 2–4 | NDV/MH | OFS, PAIN |
| Sensory room user control BPC | Co-1 | NDV/AUT | All four |
| ASPECTSS escape space (Mostafa 2014) | Tier 1 | NDV/AUT | Cross-population |

### Proposed synthesis direction
Specify "environmental refuge space" as Tier 0 universal provision: one per occupied floor plate; user-controlled lighting (2700–5000 K dimmable); RT60 ≤0.4 s; no through-traffic; accessible without passing through high-stimulation zones. Population overlays added at Tier 1 per OT assessment.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

## CON-0020 [2026-03-26 18:30]

**Mode:** Internal
**Confidence:** SPECULATIVE
**Type:** INTER-GROUP
**Populations involved:** DEAF, VIS, DEM, NDV/AUT
**Items involved:** DEAF corridor glazing (DeafSpace), DEM glare provisions, VIS glare control, NDV visual noise
**Gap register items:** NONE (new conflict identification)

### Connection description
DEAF BPC specifies glazed corridor junctions for visual advance warning — a DeafSpace principle replacing opaque corners with transparent ones. DEM BPC identifies reflective/high-gloss surfaces as problematic (perceived as wet/holes). VIS BPC identifies glare as a barrier. NDV/AUT BPC requires reduced visual noise. Glazed junctions serve DEAF but may create: glare for VIS users; reflective confusion for DEM users; visual complexity for NDV/AUT users. This is a potential four-way conflict not documented in any BPC or in the conflict resolution BPC. The DeafSpace literature documents the curved-corner collision problem (Gallaudet) but the glazing solution's interaction with VIS/DEM/NDV is unassessed.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| DeafSpace Guidelines 2010 | Co-1 | DEAF | Conflict assessment needed |
| DSDC glare guidance | Tier 3–5 | DEM | Conflict with DEAF glazing |
| PAS 6463 visual noise | Tier 5 | NDV | Conflict with DEAF glazing |
| BS 8300 / DIN 32975 glare guidance | Tier 5 | VIS | Conflict with DEAF glazing |

### Proposed synthesis direction
Document as a conflict requiring resolution. Possible mitigations: anti-reflective coating on glazing; etched/frosted lower band maintaining upper sightline for signing; matte floor adjacent to glazed junction to eliminate floor reflections. Flag for §IV.2 conflict resolution or Opus 4 cross-synthesis if standard resolution fails.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [x] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED


---

## CON-0021 [2026-03-26 19:00]

**Mode:** External
**Confidence:** HIGH
**Type:** INTER-GROUP
**Populations involved:** ALL
**Items involved:** Part III (design hierarchy), Tier 0 doctrine
**Gap register items:** NONE (new theoretical framework connection)

### Connection description
UD2024 (Oslo, November 2024) proposed "Reduction of Fear" as an 8th Universal Design principle, arguing that Ron Mace's Principle 5 ("Tolerance for Error") places blame on the user ("error") rather than the environment. The paper documents fear of falling (DEM, MOB, NEU), fear of not finding a toilet (DEM, OFS), fear of forgetting procedures (DEM, NEU), and fear of being made to feel incapable (NDV/MH, all populations) as design-relevant concerns that current UD principles do not address. This maps directly onto the guidebook's Tier 0 provisions: the environmental refuge (CON-0019), essential facility sightline (CON-0018), and rest seating intervals (CON-0014) all reduce fear as their primary mechanism of action, but the guidebook does not frame them this way. Naming "fear reduction" as a design principle would unify multiple Tier 0 provisions under a single theoretical justification from environmental psychology.

### Evidence basis
| Source | Tier | Field | Not yet in guidebook? |
|---|---|---|---|
| UD2024 Proceedings (IOS Press 2024) — "Reduction of Fear" paper (Ireland cross-disciplinary group) | Tier 5 (conference proceedings, peer-reviewed) | Universal design theory | YES — not cited |
| Norway Declaration on UD 2024 | Policy | Universal design | YES — not cited |
| NDA Ireland research on fall detection technologies | Tier 5 | Gerontology/UD | YES — not cited |

### Proposed synthesis direction
Cite the "Reduction of Fear" proposal in Part III as theoretical support for the guidebook's Tier 0 provisions. Frame environmental refuge, facility sightline, rest seating, and consistent spatial layout as fear-reduction provisions, not merely functional accommodations. This shifts the framing from "compensating for deficit" to "designing environments that do not generate fear" — which aligns with the social model.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

## CON-0022 [2026-03-26 19:00]

**Mode:** External
**Confidence:** HIGH
**Type:** BOTH
**Populations involved:** NDV/MH, DEM, NEU, NDV/AUT
**Items involved:** NDV/MH BPC (TID), environmental refuge (CON-0019)
**Gap register items:** NONE (new evidence connection)

### Connection description
Trauma-informed design (TID) has emerged as a distinct field with its own evidence base, primarily targeting housing for people experiencing homelessness and domestic violence. A scoping review through the lens of neuroscience (Vickery et al. 2022, PMC9658651) identifies three design domains: safety/security, control, and enriched environments. These map directly onto the guidebook's provisions but from a completely different research tradition. "Safety/security" = consistent layout + no dead ends + sightlines (DEM/NEU/NDV provisions). "Control" = user environmental control H-02 (CON-0017). "Enriched environments" = biophilic elements + nature connection (CON-0010/CON-0015). The NDV/MH BPC mentions TID but does not cite the neuroscience evidence (amygdala hyperactivation, cortisol response to environmental unpredictability) that provides biological mechanism for why these provisions work. The convergence is significant: TID research independently validates the same spatial principles the guidebook derives from disability-specific evidence.

Additionally, Shopworks Architecture published "Designing for Dignity: Elements of Practice" (2025) with 22 elements of dignified design — and a 2025 empirical study (MDPI Soc. Sci. 14(7):417) provides quasi-experimental evidence from 5 permanent supportive housing sites, finding that TID features improved relationships and self-awareness but showed complex patterns for safety, suggesting design alone is insufficient without programmatic support.

### Evidence basis
| Source | Tier | Field | Not yet in guidebook? |
|---|---|---|---|
| Vickery et al. 2022 (PMC9658651) — TID scoping review with neuroscience lens | Tier 3 | Architecture + neuroscience | YES — not cited |
| Shopworks "Designing for Dignity" (2025) — 22 elements | Tier 2/5 | Architecture practice | YES — not cited |
| MDPI Soc. Sci. 2025 — quasi-experimental TID PSH study | Tier 1 (quasi-experimental) | Housing/social work | YES — not cited |
| Perkins&Will TID healthcare guidelines (2024) | Tier 5 | Healthcare design | YES — not cited |

### Proposed synthesis direction
Cross-reference TID neuroscience evidence as mechanistic support for the guidebook's spatial provisions. The amygdala-mediated stress response to environmental unpredictability explains WHY consistent layout works for DEM/NEU/NDV — it is not just cognitive convenience but biological stress reduction. Add TID sources to NDV/MH BPC and to the environmental refuge specification (CON-0019). Note the 2025 empirical finding that design alone is insufficient — supports the guidebook's Tier 2 co-design doctrine.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

## CON-0023 [2026-03-26 19:00]

**Mode:** External
**Confidence:** HIGH
**Type:** INTRA-INDIVIDUAL
**Populations involved:** NDV/AUT, NDV/ADHD, NDV/SENS
**Items involved:** A-16 (Sensory Room), NDV BPC
**Gap register items:** NONE (new evidence)

### Connection description
Al-Harasis, Jabi & Sharmin (2025, Building Research & Information) published a taxonomy of 83 sensory-informed architectural design qualities for autism, based on review of 76 sources. Critical finding: current autism design frameworks (including ASPECTSS) rely on "intuition sensory zoning as the main driver for spatial topology without quantifying the sensory drivers" and emphasise "interior design elements over spatial configuration." This is a direct critique of how the guidebook specifies A-16 and NDV provisions — qualitative parameters without quantified sensory driver hierarchy. The taxonomy provides a structured classification that could inform the guidebook's item specification approach for NDV spaces. Additionally, the taxonomy identifies 83 distinct design qualities — significantly more granular than the guidebook's current NDV coverage.

### Evidence basis
| Source | Tier | Field | Not yet in guidebook? |
|---|---|---|---|
| Al-Harasis et al. 2025 (Building Research & Information 53(4):532-551) | Tier 3 | Architecture + sensory science | YES — published Feb 2025 |
| Caniato et al. 2022a/b (Energy Reports) — sensitivity drivers for ASD indoor comfort | Tier 3 | Indoor environment | YES — not cited |
| SENSHOME/BeSENSHome project (Austria/Italy) — smart home for autism | Tier 3 | Assistive technology + architecture | YES — not cited |

### Proposed synthesis direction
Use the Al-Harasis taxonomy to audit the guidebook's NDV item specifications for coverage gaps against the 83 identified design qualities. Prioritise the taxonomy's finding that spatial configuration (layout topology, not just finish materials) is under-specified. This would feed into a future item-specification-writer run for NDV items. Add to NDV BPC as a structural reference.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

## CON-0024 [2026-03-26 19:00]

**Mode:** External
**Confidence:** HIGH
**Type:** INTER-GROUP
**Populations involved:** ALL
**Items involved:** Environmental refuge (CON-0019), biophilic outdoor (CON-0015), NDV/MH retreat
**Gap register items:** NONE (new theoretical connection)

### Connection description
Prospect-refuge theory (Appleton 1975; Hildebrand 1991) — the human need for environments providing both clear outward views (prospect) and sheltered protected spaces (refuge) — provides theoretical grounding from environmental psychology for several of the guidebook's cross-population provisions. The "environmental refuge" room (CON-0019) is literally a refuge space. The facility sightline principle (CON-0018) is a prospect provision. The biophilic outdoor space with looped path and seating (CON-0015) combines prospect (garden views) and refuge (sheltered seating). The guidebook currently derives these provisions from disability-specific clinical evidence but does not cite the environmental psychology framework that explains why they work for ALL populations — including non-disabled occupants. Connecting to prospect-refuge theory strengthens the Tier 0 argument: these are not disability accommodations but fundamental human spatial needs that disability populations make visible.

### Evidence basis
| Source | Tier | Field | Not yet in guidebook? |
|---|---|---|---|
| Appleton 1975 "The Experience of Landscape" | Foundational theory | Environmental psychology | YES — not cited |
| Dosen & Ostwald 2016 — meta-analysis of 34 prospect-refuge studies | Tier 3 | Architecture + psychology | YES — not cited |
| UD2024 Carpe Diem dementia village presentation (Bærum, Norway) — prospect-refuge in dementia care | Tier 5 / Co-1 | Architecture + dementia care | YES — not cited |
| Frontiers in Psychology 2025 — healing landscape prospect-refuge balance | Tier 3 | Environmental psychology | YES — not cited |

### Proposed synthesis direction
Cite prospect-refuge theory in Part III (design hierarchy) as theoretical support for the guidebook's Tier 0 provisions. The theory provides a non-disability-specific explanation for why environmental refuge, facility sightline, and biophilic outdoor spaces are universal human needs — not disability-specific accommodations. This strengthens the social model framing: disability populations do not need "special" spaces; they need spaces that fulfil fundamental human needs which conventional design has neglected.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

## CON-0025 [2026-03-26 19:00]

**Mode:** External
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Populations involved:** NDV/AUT, NDV/ADHD, NDV/SENS, VIS
**Items involved:** Outdoor provisions, biophilic BPC
**Gap register items:** NONE (new evidence domain)

### Connection description
Finnigan 2024 (Land 13(5):636) introduces the Sensory Responsive Environments Framework (SREF) based on 31 interviews with people with autism, ADHD, and dyslexia about their experiences in outdoor built environments. Key finding: outdoor landscape design for neurodivergent users is almost entirely unaddressed — existing frameworks (ASPECTSS, PAS 6463) focus on indoor environments. The guidebook's outdoor provisions (biophilic outdoor space, secure garden for DEM) do not address sensory-responsive outdoor design for NDV populations. SREF identifies: ambient environmental factors (wind, temperature, sun exposure), materiality (surface textures, visual complexity of materials), spatial design (openness vs enclosure gradient), and navigation (predictability of outdoor routes) as design domains. Additionally, a 2024 ScienceDirect study on park environments for visually impaired individuals in Guangzhou documents the sensory compensation mechanism — VIS users amplify auditory and tactile channels in outdoor environments, requiring different landscape design than sighted users.

### Evidence basis
| Source | Tier | Field | Not yet in guidebook? |
|---|---|---|---|
| Finnigan 2024 (Land 13(5):636) — SREF framework | Tier 3 (Co-1 qualitative) | Landscape architecture + NDV | YES |
| Guangzhou VIS park study 2024 (Landscape and Urban Planning) | Tier 3 | Environmental psychology + VIS | YES |
| Mostafa 2023 Venice Biennale — "sensory decolonization" concept | Co-1 | Architecture + NDV | YES |

### Proposed synthesis direction
Extend the guidebook's outdoor design provisions beyond biophilic and DEM secure garden to include sensory-responsive outdoor landscape design for NDV and VIS populations. The SREF framework provides a structured approach. Mostafa's "sensory decolonization" concept reframes outdoor sensory provision from accommodation to equity — sensory overstimulation in public space is as disabling as a flight of stairs.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

## CON-0026 [2026-03-26 19:00]

**Mode:** External
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Populations involved:** ALL
**Items involved:** Part III (evidence hierarchy), methodology
**Gap register items:** NONE (methodological connection)

### Connection description
Van Doorn et al. 2024 (Research in Autism Spectrum Disorders 113:102350) — scoping review of sensory adaptive environments (SAEs) for autistic children — finds "mixed evidence" and a critical methodological gap: "sensory adaptive environments are not tailored to the sensory needs of each child." This finding independently validates the guidebook's three-tier hierarchy: Tier 0/1 specifications are population-informed defaults that must be resolved through Tier 2 co-design for individual users. The SAE review confirms that generic sensory rooms (equivalent to Tier 1) have limited evidence; individualised sensory environments (equivalent to Tier 2) are more effective but under-researched. Piller et al. 2025 (Frontiers in Pediatrics 13:1720179) systematic review of sensory-based interventions confirms: "targeting a variety of sensory systems is more effective than targeting only one system" — supporting the guidebook's multi-sensory approach. Both reviews note "a lack of evidence on the impact of sensory environmental modifications" — confirming the guidebook's THIN-BASE flags on sensory room specifications are appropriate.

### Evidence basis
| Source | Tier | Field | Not yet in guidebook? |
|---|---|---|---|
| Van Doorn et al. 2024 (RASD 113:102350) — SAE scoping review | Tier 3 | OT + autism research | YES |
| Piller et al. 2025 (Frontiers in Pediatrics 13:1720179) — SBI systematic review | Tier 3 | OT + paediatrics | YES |

### Proposed synthesis direction
Cite both reviews in the sensory room (A-16) evidence base as methodological support for the three-tier approach. The evidence confirms that generic sensory environments have mixed evidence (supporting Tier 1 as a starting point only) while individualised approaches show more promise (supporting Tier 2 as the resolution). Add to the NDV BPC evidence-auditor notes.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

## CON-0027 [2026-03-26 20:20]

**Mode:** External
**Confidence:** HIGH
**Type:** INTER-GROUP
**Populations involved:** ALL
**Items involved:** Part 1 (theoretical framework), Part 3 (economics)
**Gap register items:** NONE

### Connection description
The Housing Enabler instrument (Iwarsson & Slaug, Lund University CASE) is the most widely validated OT research tool for quantifying person-environment fit in housing. It operationalises Lawton's competence-press model through a two-component assessment: personal (functional limitations) and environmental (physical barriers), combined to produce an accessibility problem score. The Housing Experiment 2021 (Slaug, Granbom & Iwarsson 2024, citizen science, N=large Swedish housing stock sample) found that environmental barriers remain prevalent despite 30 years of public health evidence, and that P-E fit predicts falls better than environmental hazards alone (cf. Iwarsson et al. 2009). Parkinson's-specific Housing Enabler research (Nilsson & Iwarsson 2021) demonstrates population-specific barrier ranking.

The guidebook references the competence-press model but does not name the Housing Enabler as a Tier 2 assessment instrument. This is a gap: the HE is the direct OT operationalisation of the theoretical framework the guidebook already uses. Explicitly citing it as the recommended person-environment fit assessment method for Tier 2 co-design would give practitioners a concrete, validated tool for resolving individual specifications within Tier 1 ranges.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Iwarsson & Slaug 2001/2010 Housing Enabler | 1 | Older adults (gerontology) | ALL (Tier 2 assessment) |
| Slaug, Granbom & Iwarsson 2024 (Housing Experiment 2021) | 1 | Older adults (Swedish housing stock) | ALL (P-E fit validation) |
| Nilsson & Iwarsson 2021 (Parkinson's HE) | 1 | NEU (Parkinson's) | NEU, MOB |
| Heller et al. 2024 SR (housing characteristics + health) | 3 | Older adults | ALL |

### Proposed synthesis direction
Part 1 theoretical framework: cite Housing Enabler as the recommended Tier 2 assessment instrument for operationalising competence-press / DAR. Part 4 OT practice guidance: reference HE methodology for resolving person-specific values within Tier 1 ranges. Practice note potential: HE-based Tier 2 assessment checklist for OT practitioners.

### Disposition
- [x] HIGH → item-specification-writer briefing

---

## CON-0028 [2026-03-26 20:20]

**Mode:** External
**Confidence:** HIGH
**Type:** INTER-GROUP
**Populations involved:** ALL
**Items involved:** Part 1 (theoretical framework — three-tier hierarchy)
**Gap register items:** NONE

### Connection description
Lawton (1989, 1990) distinguished environmental docility from environmental proactivity. Docility: declining personal competence → behaviour increasingly dictated by environment. Proactivity: higher competence → person actively shapes environment to match needs. A 2024 P-E fit scoping review (Journal of Asian Architecture and Building Engineering, 10.1080/13467581.2024.2373824) confirms these concepts remain foundational but identifies a knowledge gap: the lack of proactive and dynamic views in current P-E fit research.

The guidebook's three-tier hierarchy maps directly onto this continuum but does not name it:
- Tier 0 = reducing environmental press universally (docility mitigation — ensures environment does not overwhelm any user's competence)
- Tier 1 = population-informed press calibration (intermediate — reduces press for identified population groups)
- Tier 2 = person-specific co-design (proactivity — individual actively shapes environment with OT support)

This mapping is not stated in the guidebook. Making it explicit provides non-disability-specific theoretical grounding from the gerontology tradition — strengthening the argument that the three-tier approach is not a disability accommodation framework but a universal human-environment optimisation model.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Lawton 1989/1990 (environmental proactivity) | Foundational theory | Older adults | ALL (three-tier grounding) |
| P-E fit scoping review 2024 | 3 | Built environment (general) | ALL |
| Struckmeyer & Rice 2025 (Routledge chapter: EP-CM in OT) | Co-2 | OT practice | ALL |

### Proposed synthesis direction
Part 1 theoretical framework: add explicit mapping of three-tier hierarchy to Lawton's docility-proactivity continuum. Frame: Tier 0 = anti-docility floor; Tier 1 = population-calibrated press reduction; Tier 2 = proactive P-E optimisation through co-design. This reframes the entire hierarchy from accessibility levels to universal person-environment fit optimisation — non-disability-specific.

### Disposition
- [x] HIGH → item-specification-writer briefing

---

## CON-0029 [2026-03-26 20:20]

**Mode:** External
**Confidence:** HIGH
**Type:** INTER-GROUP
**Populations involved:** ALL
**Items involved:** NONE (new specification area: RFO-stage POE)
**Gap register items:** NONE

### Connection description
Two independent research programmes have developed inclusive-design-specific POE tools that the guidebook does not reference:

1. IDEA Audit (Zallio & Clarkson, Cambridge, Building and Environment 217:109058, 2022; case study in Buildings 14(9):3018, 2024): Four-component framework — physical accessibility (17%), sensory enhancement (15%), neurodivergent comfort, people-space engagement. Mixed-method occupant feedback. Survey validated with 114 building industry experts. 2024 case study showed before/after inclusive design implementation at corporate HQ using IDEA findings to inform redesign.

2. A.U.D.I.T. (Mosca & Capolongo, Acta Biomedica 94(S3):e2023124, 2023): Assessment Universal Design & Inclusion Tool for healthcare facilities — evaluates physical, sensory-cognitive, and social quality dimensions.

Zallio & Clarkson (2023, Architectural Science Review 67:268-279) found that only 10.6% of architectural practitioners reported clients seeking sensory and cognitive inclusion beyond physical accessibility, and that POE tools for inclusive design are almost nonexistent in practice. The guidebook covers design stages up to RFO but has no specification for post-occupancy evaluation. This is a gap: without POE, there is no feedback loop between design intent (Tier 0/1 specifications) and actual occupant experience.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Zallio & Clarkson 2022 (IDEA Audit) | 3 | ALL (built environment POE) | ALL (RFO-stage specification) |
| Zallio & Clarkson 2024 (case study) | 3 | ALL (workplace) | ALL |
| Mosca & Capolongo 2023 (A.U.D.I.T.) | 3 | ALL (healthcare) | ALL |
| Zallio & Clarkson 2023 (practitioner survey, n=114) | 3 | Building industry professionals | ALL |

### Proposed synthesis direction
Add RFO-stage POE specification to Part 5 (or equivalent practice guidance): recommend IDEA Audit framework (or adaptation) as post-occupancy feedback instrument. Components: physical accessibility audit, sensory environment assessment, neurodivergent comfort evaluation, people-space engagement survey. Link POE findings back to Tier 0/1 specifications for iterative improvement. This closes the design-occupy-evaluate loop currently missing from the guidebook.

### Disposition
- [x] HIGH → item-specification-writer briefing

---

## CON-0030 [2026-03-26 20:20]

**Mode:** External
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Populations involved:** DEM, IntD, NDV/AUT, VIS, NEU
**Items involved:** CON-0001 items (circulation legibility); cognitive wayfinding items
**Gap register items:** NONE

### Connection description
Cognitive ergonomics research on wayfinding quantifies the decision-point mechanism that the guidebook specifies qualitatively (CON-0001: three or fewer decision points per segment for IntD):

1. Wayfinding uncertainty model (bioRxiv 2023, validated Study 1 n=28, Study 2 n=11): Wayfinding uncertainty correlates with time elapsed since last helpful sign. The model predicts human-reported uncertainty levels under different signage conditions (ROC-AUC 0.70). Implication: signage spacing is a quantifiable parameter — the guidebook could specify maximum distance between wayfinding cues.

2. Intersection-based decision points (Bruyne et al. 2018, Cognitive Research: Principles and Implications 3:13): Intersections are the primary driver of navigation difficulty. Route complexity is contingent upon intersection count (Lupien et al. 1998). Spatial decisions are made before entering an intersection, not within it. Implication: validates the decision-point rule and suggests that advance warning of approaching decision points (sightlines, gradual opening of corridor junctions) reduces cognitive load.

3. Hospital wayfinding MCDM (Morag et al., Applied Ergonomics 2024): Multi-criteria decision-making approach rates route difficulty by impairment type — separate ease-of-use scores for mobility, vision, and cognitive impairment.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| bioRxiv 2023 wayfinding uncertainty model | 3 | General (neuroscience) | DEM, IntD, NDV/AUT |
| Bruyne et al. 2018 (intersection decision dynamics) | 3 | General (cognitive science) | DEM, IntD, VIS |
| Morag et al. 2024 (hospital wayfinding MCDM) | 3 | MOB, VIS, cognitive impairment | ALL |
| Lupien et al. 1998 (route complexity = decision point count) | 3 | General (neuroscience) | DEM, IntD |

### Proposed synthesis direction
Strengthen CON-0001 circulation legibility specification with quantified parameters from cognitive ergonomics: (a) maximum distance between wayfinding cues (derivable from uncertainty-decay model); (b) advance visual warning before decision points (glazed junctions per CON-0020 + sightline per CON-0018); (c) route complexity rating by population code. MODERATE confidence because the bioRxiv model is a preprint and sample sizes are small.

### Disposition
- [ ] MODERATE → P2 gap item

---

## CON-0031 [2026-03-26 20:20]

**Mode:** External
**Confidence:** HIGH
**Type:** INTER-GROUP
**Populations involved:** ALL
**Items involved:** Part 3 (economics)
**Gap register items:** NONE

### Connection description
Three recent meta-level sources converge on OT home modification cost-effectiveness — stronger than evidence currently cited in the guidebook's economics section:

1. Clemson et al. 2023 Cochrane SR (CD013258, 22 RCTs, 8,463 participants): Environmental interventions reduce fall rate by 38% among older community-dwelling adults. OT-delivered home modifications are the most effective single intervention type. Already cited in CON-0003 for grab bars; the economics implication is not drawn.

2. 2023 quasi-experimental (cited in OT practice literature, 2025): Mean home modification cost $10,397 versus annual healthcare costs of $22,763 to $154,478 for unmodified homes. Cost ratio: 1:2.2 to 1:14.9.

3. An et al. 2025 SR (fall prevention interventions): Exercise + home modification combined reduces fall rates by 30-40%. Two-visit OT home modification model demonstrates statistically significant improvement in occupational performance and satisfaction.

4. Lektip et al. 2023 meta-analysis (PeerJ 11:e15699, 10 RCTs, n=1,960): Home modification shows clinically meaningful 7% reduction in falls (RR=0.93). Long-term models project cost savings within 10-year horizon.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Clemson et al. 2023 Cochrane | 3 | MOB (fall prevention) | ALL (economics case) |
| 2023 quasi-experimental (cost comparison) | 3 | Older adults | ALL (economics) |
| An et al. 2025 SR | 3 | Older adults | ALL (economics) |
| Lektip et al. 2023 meta-analysis | 3 | Older adults | ALL (economics) |

### Proposed synthesis direction
Part 3 economics section: update cost-effectiveness evidence with 2023-2025 meta-level sources. Key framing: every dollar spent on OT-informed home modification saves $2.20 to $14.90 in healthcare costs. Clemson 2023 Cochrane provides the strongest single evidence statement for environmental intervention effectiveness. This strengthens the guidebook's business case for specification compliance.

### Disposition
- [x] HIGH → item-specification-writer briefing

---

## CON-0032 [2026-03-26 20:20]

**Mode:** External
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Populations involved:** ALL
**Items involved:** Part 1 (structure validation)
**Gap register items:** NONE

### Connection description
A 2025 scoping review in Humanities and Social Sciences Communications (Nature, accepted July 2025) analysed 64 empirical studies (2005-2024) on interior design and older adult health. Identified seven key interior design principles affecting physical, physiological, and mental health: (1) lighting, (2) thermal environment and air quality, (3) spatial layout, (4) barrier-free design, (5) space size, (6) furniture, (7) relaxation design.

These seven principles map directly onto the guidebook's existing item categories: (1) circadian lighting; (2) air quality/thermal items; (3) circulation/layout items; (4) threshold/grab bar items; (5) room dimension items; (6) furniture/workstation items; (7) sensory relief/rest items. The alignment is close but not exact — the review identifies relaxation design as a distinct category whereas the guidebook distributes relaxation across sensory relief (A-16), biophilic (BIO-xx), and rest seating (CON-0004). The review also notes a shift from institutional to home-based research focus post-2020, aligning with the guidebook's residential emphasis.

This is external validation of the guidebook's structural organisation from an independent gerontology evidence synthesis — not a novel connection per se, but confirmation that the category structure is evidence-aligned.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Interior design scoping review 2025 (64 studies) | 3 | Older adults (interior design) | ALL (structural validation) |

### Proposed synthesis direction
Note as structural validation in Part 1 methodology section. No specification change required. The relaxation design category consolidation question should be tracked — consider whether CON-0002 (sensory relief unification), CON-0004 (adjustable posture seating), and CON-0010 (therapeutic outdoor) should be formally grouped under a restorative environment umbrella category.

### Disposition
- [ ] MODERATE → P2 gap item

---

## CON-0033: CAPABLE multicomponent model → OT assessment specification
**Status:** PENDING
**Discovered:** 2026-03-27 (residential-accessible-home-case-studies Opus synthesis)
**Confidence:** HIGH
**Type:** INTER-GROUP
**Mode:** Internal (BPC → Part 5/7 specification)

### Connection
The CAPABLE programme (Liu 2020 Tier 1 RCT; Washington 2023 Tier 1 implementation; Sheffield 2013 Tier 1 RCT) establishes that OT-led structured assessment + home modification + nursing/handyman produces superior ADL outcomes. This multicomponent model should govern the OT assessment specification in Part 5 (residential process) and Part 7 (item specifications for assessment protocols). Three independent Tier 1 studies confirm standardised protocol > informal practice.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Liu/CAPABLE 2020 (PMID 32951215) | 1 RCT | MOB/ALL (older adults) | Part 5 residential assessment protocol |
| Washington/CAPABLE 2023 (PMID 36748717) | 1 implementation | MOB/ALL | Part 5 real-world delivery model |
| Sheffield 2013 (PMID 23213082) | 1 RCT | MOB/ALL | Part 7 OT assessment item |
| Malmgren Fänge 2019 (PMID 31684916) | 1 quasi-experimental | MOB/ALL | Part 5/7 — OR 9.50 wheelchair mobility anchors specification |

### Proposed synthesis direction
Write Part 5 residential assessment specification using CAPABLE as governing model. Malmgren Fänge OR 9.50 anchors wheelchair-specific provisions. Sheffield 39% personal care hour reduction provides economic justification.

### Disposition
- [ ] HIGH → item-specification-writer briefing for Part 5 + Part 7 assessment items

---

## CON-0034: Malmgren Fänge OR 9.50 → wheelchair home mobility specification
**Status:** PENDING
**Discovered:** 2026-03-27 (residential-accessible-home-case-studies Opus synthesis)
**Confidence:** HIGH
**Type:** INTER-GROUP
**Mode:** Internal (BPC → Part 7 MOB specification)

### Connection
Malmgren Fänge 2019 (SE/NO, Tier 1 quasi-experimental, PMID 31684916) found OR 9.50 for wheelchair use at home when standardised OT assessment protocol was used vs ordinary practice. This is the strongest single-outcome effect size in the residential evidence dataset. It should anchor wheelchair-accessible home layout and dimensional specifications in Part 7 MOB items.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Malmgren Fänge 2019 (PMID 31684916) | 1 quasi-experimental | MOB/ALL (older adults, SE/NO) | Part 7 MOB wheelchair home items — dimensional provisions |

### Proposed synthesis direction
Cross-reference to bathroom-design, kitchen-design, entrance-and-threshold, and corridor/circulation MOB items. Effect size justifies above-code spatial provisions for wheelchair users.

### Disposition
- [ ] HIGH → item-specification-writer briefing for MOB wheelchair items

---

## CON-0035: Douglas 2024 support > environment → Part 5 support framework specification
**Status:** PENDING
**Discovered:** 2026-03-27 (residential-accessible-home-case-studies Opus synthesis)
**Confidence:** HIGH
**Type:** INTER-GROUP
**Mode:** Internal (BPC → Part 5 specification)

### Connection
Douglas et al. 2024 (AU, Tier 1 qualitative, BMJ Open) found that support quality is a greater determinant of tenant QoL than the built environment in SDA housing. Converges with ILMI 2021 (IE, Co-1) and Carey et al. 2025 (AU, Co-1). The guidebook must specify transition planning and ongoing support frameworks alongside built environment provisions. Built environment is necessary but not sufficient.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Douglas et al. 2024 (BMJ Open) | 1 qualitative | NEU/MOB/ALL (SDA tenants) | Part 5 support framework specification |
| Carey et al. 2025 (PMID 41175339) | Co-1 | NEU/MOB families | Part 5 transition planning specification |
| ILMI 2021 | Co-1 | ALL (IE advocacy) | Part 5 support alongside housing |
| Ainsworth 2022 (PMID 36394257) | 1 qualitative | MOB/ALL (AU home mod) | Part 5 OT process quality specification |

### Proposed synthesis direction
Part 5 residential matrices must include support framework items — not just built environment specification. Transition planning, family/carer support, and ongoing support quality are co-primary with physical design. This is the most significant cross-cutting finding from the residential case studies synthesis.

### Disposition
- [ ] HIGH → item-specification-writer briefing for Part 5 support framework items

## CON-0036 [2026-03-28 17:00]
**Mode:** Internal
**Confidence:** MODERATE
**Type:** BOTH
**Disposition:** CONSUMED
**Populations involved:** OFS, PAIN, NDV/AUT, NDV/SENS, NEU, DEM, NDV/MH, DEAF
**Items involved:** D-05
**Gap register items:** GAP-FDR-T0-03

### Connection description
Retreat/reset room overlaps substantively with D-05 (Enclosed Low-Stimulation Spaces) but proposes universal requirement for public buildings >500 m². Sound attenuation specification creates emergency egress and communication isolation risk for DEAF population. Universal (Tier 0) adoption rejected; retreat/reset provisions remain Tier 1.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| PAIN/OFS FDR session 2026-03-26 | THIN (expert consensus) | OFS, PAIN, NDV/AUT, NDV/SENS, NEU, DEM, NDV/MH | REJECTED for Tier 0 due to DEAF conflict |

### Proposed synthesis direction
Maintain D-05 as Tier 1. Annotate: where retreat/reset spaces serve DEAF population, specify visual emergency alerts, transparent sidelights, or communication pass-through to mitigate isolation risk. Do not elevate to Tier 0.

### Disposition
- [x] Annotate D-05 with DEAF accommodation requirement for sound-attenuated spaces — DONE 2026-03-28 18:00
- [x] Reject GAP-FDR-T0-03 for Tier 0 status — DONE 2026-03-28 17:00

---

## CON-0037 [2026-03-28 17:00]
**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** CONSUMED (E-14 drafted 2026-03-28)
**Populations involved:** OFS, PAIN, MOB/AMB, DEM
**Items involved:** E-05, E-10
**Gap register items:** GAP-FDR-T0-04

### Connection description
Entrance recline seating within 5 m of all accessible entrances serves OFS, PAIN, MOB/AMB, and DEM with no identified conflicts. More stringent than existing E-10 (≤25 m interval) and complements E-05 (weather protection). PARTIAL Tier 0 status confirmed for entrance-specific application; neutral for VIS, DEAF, NEU, NDV.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| PAIN/OFS FDR 2026-03-26 | THIN (expert consensus) | OFS, PAIN | MOB/AMB, DEM |
| RCOT HAwD 2019 + Roxburgh 2024 BJOT | Co-2 / Tier 1 | MOB, OFS, PAIN | Entrance-specific recline requirement |

### Proposed synthesis direction
Create new Tier 0 item **E-14 Entrance Rest Seating** — reclinable or tilt-capable seating within 5 m of threshold, seat height ≥480 mm AFF, arms both sides, alcove ≥900 mm wide, ≥200 mm recess from circulation path. Cross-reference E-05 and E-10. Evidence tier: THIN pending empirical validation.

### Disposition
- [x] Draft E-14 as new Tier 0 item — parts/v10/e14-entrance-rest-seating.md
- [x] Cross-reference E-05 and E-10
- [x] Update GAP-FDR-T0-04 → CONSUMED (gap_register.md updated 2026-03-28)

---

## CON-0038 [2026-03-28 17:00]
**Mode:** Internal
**Confidence:** MODERATE
**Type:** BOTH
**Disposition:** CONSUMED
**Populations involved:** MOB, NEU, PAIN
**Items involved:** G-08
**Gap register items:** GAP-FDR-T0-05

### Connection description
Storage layout as incidental bracing surface (U-shape or L-shape, shelf edges at waist height) serves MOB, NEU, and PAIN in residential bedrooms with no identified conflicts. Passive provision (no energy/maintenance cost), enables future tailoring. Tier 0 status confirmed; neutral for VIS, DEAF, DEM.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| AOTA Home Modification Guidelines 2023 | Co-2 (single source) | MOB, NEU, PAIN | Tier 0 universal specification for residential bedrooms |

### Proposed synthesis direction
Elevate the U/L-shape shelf configuration bullet in G-08 from population-tagged to Tier 0 specification. Add explicit Tier 0 label within G-08. Flag for empirical validation (single Co-2 source). No separate item required — G-08 already covers the provision.

### Disposition
- [x] Elevate G-08 U/L-shape storage bullet to Tier 0 scope — DONE 2026-03-28 17:05
- [x] GAP-FDR-T0-05 CLOSED 2026-03-28 17:00


---

## CON-0039 [2026-03-28 21:45]
**Mode:** Internal
**Confidence:** HIGH
**Disposition:** PENDING
**Type:** [BOTH] — intra-individual (one person benefits from RT60 ≤0.3 s for multiple co-occurring conditions) and inter-group (building serves DEAF + NDV/AUT + DEM occupants)
**Populations involved:** DEAF, NDV/AUT, DEM, NEU/PCS
**Items involved:** A-02, A-08, A-13, all Category A items
**Gap register items:** NONE (new Tier 0 candidate)

### Connection description
Four independent evidence streams converge on RT60 ≤0.3 s as the specification ceiling for speech-critical rooms:

- **DEAF/hearing device users:** Iglehart 2020 (Tier 1 AJA), ANSI/ASA S12.60 Footnote e — 0.3 s for classrooms ≤283 m³. Speech perception scores significantly better at 0.3 s than 0.6 s for hearing aid/CI users.
- **NDV/AUT:** Bettarello 2021, Caniato 2024 (Tier 1) — existing standards calibrated to neurotypical populations are insufficient; sub-0.3 s indicated. Autistic users significantly more affected by modest background noise increases (52→55 dBA).
- **DEM:** Devos 2019 POE (Belgian nursing homes); Lyngby-Taarbæk case study (40% agitation reduction from acoustic ceiling installation). Acoustic calm as primary therapeutic intervention.
- **NEU/PCS:** Clinical guidance for low-background-noise environments; no contradicting evidence at 0.3 s.

The 0.3 s ceiling is a strict subset of the 0.6 s general-population ceiling — no population is disadvantaged. The Opus synthesis on `acoustics-speech-intelligibility-disability` established that 0.6 s is a failure boundary, not a compliant specification — a framing error repeated across ADA, BS 8300, and NCC.

**Additional conflict:** Sound masking (A-13) is contraindicated for NDV/AUT (PAS 6463, Bettarello evidence) but potentially useful in open-plan DEAF/hearing-loop settings. Genuine inter-group conflict requiring documentation in §8.6 (unresolvable without spatial zoning).

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Iglehart 2020 (AJA) | 1 | DEAF (hearing device users) | ALL — Tier 0 acoustic ceiling |
| ANSI/ASA S12.60-2010 Footnote e | 4 | DEAF | ALL |
| Bettarello et al. 2021 (Applied Sciences) | 1 | NDV/AUT | ALL |
| Caniato et al. 2024 | 1 | NDV/AUT | ALL |
| Devos et al. 2019 (PMC) | 2 | DEM | ALL |
| Murgia et al. 2023 (systematic review) | 1 | DEAF | ALL |

### Proposed synthesis direction
Elevate RT60 ≤0.3 s (mid-frequency average 500–2000 Hz) to Tier 0 universal specification for all speech-critical rooms. Frame 0.6 s explicitly as outer failure boundary, not compliant specification. Background noise ≤35 dBA; STI ≥0.5 at furthest listener position. Sound masking conflict with NDV/AUT documented separately in Part 7 §7.3.

### Disposition
- [ ] HIGH → item-specification-writer briefing for all Category A items

---

## CON-0040 [2026-03-28 21:45]
**Mode:** Internal
**Confidence:** HIGH
**Disposition:** PENDING
**Type:** [BOTH] — serves individuals with co-occurring sensory conditions and buildings with multiple disability populations
**Populations involved:** NDV/AUT, NDV/ADHD, NDV/SENS, DEM, NEU, DEAF, OFS, PAIN, VIS
**Items involved:** A-02, A-08, A-13, B-01, B-06, F-01, D-05, A-16
**Gap register items:** NONE (structural synthesis)

### Connection description
Four unreferenced BPC slugs describe four facets of a single sensory environment design system with no internal cross-references:

1. **`sensory-processing-model-design-application`** — Dunn's four sensory profiles → design requirement matrix
2. **`detectable-gradient-protocol-sensory-zones`** — Three spatial zones → boundary thresholds (≥0.2 s RT60 change, ≥50 lux, ≥30 LRV)
3. **`room-acoustic-performance`** — RT60/NC targets per population
4. **`therapeutic-lighting-design`** — Melanopic EDI/CCT targets per time of day

The unmade synthesis is the within-zone parameter assignment:

| Parameter | Zone 1 (High activation) | Zone 2 (Moderate) | Zone 3 (Low activation) |
|---|---|---|---|
| RT60 | ≤0.6 s | ≤0.4 s | ≤0.3 s |
| Background noise | ≤40 dBA | ≤35 dBA | ≤30 dBA |
| Daytime illuminance | ≥300 lux / ≥200 EML | 150–300 lux | User-controlled 0–150 lux |
| CCT daytime | ≥4000 K | 3000–4000 K | ≤3000 K dimmable |
| Evening CCT (all) | ≤2700 K / ≤10 EML | ≤2700 K | ≤2700 K |

Zone 3 RT60 ≤0.3 s aligns with CON-0039. Individual user control (CON-0017/H-02) is the resolution mechanism across all zones.

### Evidence basis
| Source | Tier | Slug | Proposed extension to |
|---|---|---|---|
| Dunn 1997 sensory model | Foundational | sensory-processing-model | Zone assignment framework |
| PAS 6463:2022 §6.4 | 5 | detectable-gradient-protocol | Zone boundary thresholds |
| Mostafa ASPECTSS 2.0 (2021) | 2 | detectable-gradient-protocol | Zone transition design |
| Iglehart 2020 / Murgia 2023 | 1 | room-acoustic-performance | Zone 3 RT60 target |
| Brown et al. 2022 / WELL v2 | 3/5 | therapeutic-lighting-design | Zone 1–3 CCT/EML targets |

### Proposed synthesis direction
Create unified sensory environment specification matrix linking Dunn's profiles to spatial zones to quantified parameters. Mark as ○ (expert synthesis) — zone boundaries empirically grounded, within-zone targets synthesised from population-specific evidence. No single study validates the complete matrix.

### Disposition
- [ ] HIGH → item-specification-writer briefing for F-01, A-16, B-01, B-06, all Category A

---

## CON-0041 [2026-03-28 21:45]
**Mode:** Internal
**Confidence:** HIGH
**Disposition:** PENDING
**Type:** [INTRA-INDIVIDUAL] — a person with DEM+MOB+PAIN in a residential setting experiences the thermal differential as a single hazard
**Populations involved:** DEM, MOB (older adults), NEU/MS, PAIN, OFS
**Items involved:** TC-01, TC-02, TC-03, TC-05, H-04, all residential bathroom matrix entries
**Gap register items:** NONE (safety-critical propagation)

### Connection description
Japan heat shock data (6,073 bathtub drowning deaths/year, MHLW 2023) is the most consequential mortality statistic in the BPC corpus. Root cause: 5–15°C differential between unheated bathrooms and heated living areas. Resolution: inter-room differential ≤5–7°C (Nakayama 1981).

This finding is siloed in `thermal-comfort-older-adults-care-settings` and not propagated to:
- Part 5 residential bathroom matrices (where it is a P1 safety specification)
- TC-01/TC-02/TC-03 items (which specify envelope performance but not inter-room differential)
- The `ms-thermal-temperature-conflict-resolution` BPC (which addresses population thermal preference conflicts but not the mortality mechanism)
- CON-0019 environmental refuge (which does not specify thermal zone assignment)

The thermal conflict resolution (ambient ≤18–21°C + individual supplemental heating) also affects refuge rooms: OFS populations need individual heating controls in refuge spaces; NDV/sensory-avoiding need cool baseline. Both require individual control — compatible but unstated.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| MHLW Japan 2023 (6,073 deaths) | 3 | DEM/older adults (JP) | ALL residential bathroom specification |
| Nakayama 1981 (≤5–7°C differential) | 3 | DEM/older adults (JP) | ALL residential inter-room thermal spec |
| Baquero et al. 2023 (n=1,065) | 3 | DEM/older adults | Thermal comfort targets |
| ms-thermal BPC (Uhthoff/PAIN/OFS conflict) | 2–4 | NEU/MS, PAIN, OFS | Resolution methodology |
| TC-05 (heated bathroom floor) | 5 | ALL | Direct prevention of heat shock mechanism |

### Proposed synthesis direction
Propagate inter-room thermal differential ≤5°C to all residential bathroom matrix entries as P1 safety specification. Cross-reference TC-05 (heated bathroom floor) as the primary prevention mechanism. Link to ms-thermal conflict resolution for multi-condition thermal management. Specify refuge room thermal zone assignment (individual control required).

### Disposition
- [ ] HIGH → item-specification-writer briefing for Part 5 bathroom matrices + TC items

---

## CON-0042 [2026-03-28 21:45]
**Mode:** Internal
**Confidence:** HIGH
**Disposition:** PENDING
**Type:** [INTER-GROUP] — different occupants need different alerting channels; also [INTRA-INDIVIDUAL] for DEAF+NEU co-occurrence
**Populations involved:** DEAF, DBL, NEU (seizure), NDV/AUT (photosensitive)
**Items involved:** B-10, visual alerting items, H-04, CON-0014 items
**Gap register items:** GAP-035

### Connection description
CON-0014 proposes vibrotactile alerting for sleeping areas where DEAF/DBL and photosensitive populations co-occur. The `visual-fire-alarm-seizure-safety` BPC specifies synchronised VADs at 0.5–1 Hz + voice alarm + vibrotactile. The `visual-alerting-and-wayfinding-light` BPC covers non-emergency alerting (doorbells, call systems).

The unmade synthesis: the alerting system is a single integrated domain. A person who needs vibrotactile fire alerts also needs vibrotactile doorbell, telephone, and intruder alerts. Specifying vibrotactile for fire only leaves the same person without notification for all other alert types.

The seizure/photosensitivity conflict applies to all visual alerting, not just fire — doorbell VADs at a photosensitive user's desk carry the same seizure risk. CON-0014's vibrotactile resolution must extend to non-emergency alerting.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Jordan & Vanderheiden 2024 (ACM TACCESS) | 3 | NEU (photosensitive epilepsy) | All visual alerting items |
| BS EN 54-23:2010 | 5 | DEAF (fire VAD) | Multi-channel specification |
| NFPA 72-2022 | 5 | DEAF | Multi-channel specification |
| RNID / HLAA / Bufdir | Co-1/2 | DEAF (vibrotactile) | All alerting channels |

### Proposed synthesis direction
Specify unified multi-channel alerting: every alert event (fire, intrusion, doorbell, telephone, intercom) available through all three channels (visual + auditory + vibrotactile) simultaneously. Consistent channel specifications across alert types to enable pattern recognition. Extends CON-0014 from sleeping-area fire alarm to all alerting.

### Disposition
- [ ] HIGH → item-specification-writer briefing for B-10 + all alerting items

---

## CON-0043 [2026-03-28 21:45]
**Mode:** Internal
**Confidence:** HIGH
**Disposition:** PENDING
**Type:** [BOTH] — serves individuals with VIS+DEM co-occurrence and buildings with VIS/DEM/NDV populations
**Populations involved:** VIS, DEM, NDV/AUT, IntD, DBL
**Items involved:** All C-items, D-02, D-06, F-01 zone boundaries
**Gap register items:** NONE (internal consistency correction)

### Connection description
The `luminance-contrast-lrv-evidence-base` BPC documents that the universal 30% LRV threshold has no empirical basis — it is a regulatory floor adopted from UK DDA guidance without validation. Severe VI needs ≥65% Michelson contrast (2.5× the standard). The guidebook recommends ≥50% LRV as best practice for C-items.

The inconsistency: the `detectable-gradient-protocol-sensory-zones` BPC specifies ≥30 LRV change at zone boundaries — inheriting the unvalidated threshold. Cognitive wayfinding items depend on contrast-based landmarks for DEM, IntD, NDV. The guidebook's own ≥50% best-practice target is not propagated to zone boundaries or wayfinding items.

### Evidence basis
| Source | Tier | Currently cited for | Gap |
|---|---|---|---|
| Harper et al. 2022 (Ergonomics) | 3 | Stair contrast enhancement | Supports enhancement; doesn't validate 30% |
| Brown et al. 2023 (Ergonomics) | 3 | VIS nosing contrast | Confirms benefit; no threshold validation |
| Dain et al. (cited in Manandhar 2022) | 3 | Severe VI | ≥65% Michelson needed; 2.5× current standard |
| CNIB 2024 | Co-1 | VIS | 30% is minimum regulatory floor, not functional optimum |

### Proposed synthesis direction
Apply ≥50% LRV best-practice target consistently to all contrast-dependent provisions — C-items, zone boundaries, wayfinding items. At critical junctions (platform edges, stair nosings, kerb lines): ≥65% Michelson. The 30% value remains as code-compliance minimum only. Internal consistency correction — the guidebook already established the right position in the LRV BPC.

### Disposition
- [ ] HIGH → item-specification-writer briefing for all C-items + F-01 zone boundaries

---

## CON-0044 [2026-03-28 21:45]
**Mode:** Internal
**Confidence:** MODERATE (theoretical) / HIGH (haptic continuity)
**Disposition:** PENDING
**Type:** [INTRA-INDIVIDUAL] — a person with VIS+MOB co-occurrence relies on haptic pathway for both navigation and postural support
**Populations involved:** ALL (theoretical); VIS, DBL, MOB (haptic continuity)
**Items involved:** Part 1 (§1.4 theoretical framework), all G-items, C-04
**Gap register items:** NONE

### Connection description
The `ecological-psychology-haptic-affordances-built-environment` BPC provides the most fundamental theoretical basis for the guidebook's specification logic: specifications are affordance thresholds — the point at which the environment switches from enabling to disabling action. This BPC is unreferenced in the connection register despite providing the meta-framework that unifies prospect-refuge (CON-0024), Lawton docility-proactivity (CON-0028), and Housing Enabler (CON-0027).

Two specific actionable findings:

1. **Misaffordance concept:** Environments signalling an action that doesn't exist. High-gloss floor appearing wet to DEM user = misaffordance. Glazed junction (CON-0020) creating reflection = misaffordance for DEM. Names the mechanism behind several existing conflicts.

2. **Haptic pathway continuity:** Handrail/grab bar interruptions at doorways break the tactile route for VIS and DBL users. Continuous handrail = continuous haptic pathway. Not connected to CON-0003 (grab bars) or CON-0001 (circulation legibility). Actionable: specify continuous haptic pathway as Tier 0 circulation requirement.

### Evidence basis
| Source | Tier | Framework | Application |
|---|---|---|---|
| Gibson 1979 (affordances) | Foundational | Affordance theory | Specification = affordance threshold |
| Heft 2001 (nested hierarchies) | Foundational | Environmental psychology | Wayfinding = affordance assemblage |
| Turvey & Carello 1995 (haptic) | Foundational | Haptic psychology | Handrail = haptic navigation structure |

### Proposed synthesis direction
Part 1 §1.4: cite ecological affordance framework as theoretical foundation. Specification = threshold at which affordance becomes available/unavailable. Misaffordance = actively harmful design (not just absence of accessibility). Haptic continuity: specify continuous handrail as Tier 0 on primary circulation routes — interruption at doors, corners, or landings is a haptic pathway break.

### Disposition
- [ ] MODERATE → P2 gap item for theoretical framing
- [ ] HIGH → item-specification-writer briefing for G-item haptic continuity

---

## CON-0045 [2026-03-28 21:45]
**Mode:** Internal (case study evidence)
**Confidence:** HIGH
**Disposition:** PENDING
**Type:** N/A — methodological finding, not a specification connection
**Populations involved:** VIS, PAIN, OFS (absence); DEM, NDV/AUT, MOB (presence)
**Items involved:** Part 1 (evidence methodology), Part 13 (case studies)
**Gap register items:** NONE

### Connection description
The case study corpus reveals a stark evidence asymmetry: VIS, PAIN/OFS, and DEAF (beyond Gallaudet) have zero purpose-built or home-modified environment case studies with outcome data globally. Confirmed not-found after full multilingual research pass.

DEM has 5 outcome studies; NDV/AUT has 3; MOB has the entire OT home modification corpus (CAPABLE, Sheffield, Malmgren Fänge, BATH-OUT, Petersson, DFG). Every PAIN/OFS and VIS item specification rests on clinical evidence transferred from non-built-environment settings — zero POE validation confirms these specifications work in situ.

The guidebook's evidence hierarchy does not weight "never tested in a built environment" differently from "tested and confirmed." It should. This connects to CON-0029 (POE tools): without POE tools applied to VIS/PAIN/OFS populations, the specification-to-outcome feedback loop is broken for these populations.

### Evidence basis
| Source | Status | Note |
|---|---|---|
| Cross-population case studies BPC Opus synthesis | COMPLETE | "CONFIRMED NOT FOUND globally" for VIS, PAIN/OFS case studies |
| Residential case studies BPC Opus synthesis | COMPLETE | Same finding confirmed for residential contexts |
| Case study compendium (26 entries) | COMPLETE | Zero VIS or PAIN/OFS entries with outcome data |

### Proposed synthesis direction
Part 1 evidence methodology: add evidence confidence weighting — provisions validated by built environment POE carry higher confidence than provisions derived from clinical transfer only. Part 13 §13.0 methodology note: explicit disclosure of VIS/PAIN/OFS evidence gap. Gap register: commission VIS and PAIN/OFS POE studies as v11 research priority.

### Disposition
- [ ] HIGH → Part 1 methodology note + Part 13 evidence gap disclosure

---

## CON-0046 [2026-03-28 21:45]
**Mode:** Internal (case study evidence)
**Confidence:** HIGH
**Disposition:** PENDING
**Type:** [INTER-GROUP] — NDV/AUT and NDV/MH are different diagnostic groups co-occupying the same inpatient ward
**Populations involved:** NDV/AUT, NDV/MH
**Items involved:** A-16, F-01, D-05, CON-0019 items
**Gap register items:** NONE

### Connection description
CS-17 (NHS CAMHS inpatient review, NDTi/NHS England 2022) documents systematic harm: NHS inpatient mental health wards designed for NDV/MH are actively harmful to co-occurring NDV/AUT patients. Sensory environments "present sometimes extreme challenges" and "at best hinder wellbeing, at worst exacerbate mental health problems; instigate cycle of progression to more restrictive settings."

This is the only case study documenting design-caused escalation of disability — not failure to accommodate, but active worsening. The absence of sensory zoning (CON-0040 three-zone model) and environmental refuge (CON-0019) is the proximate cause. The sensory zoning system is not an optional enhancement — it is the minimum provision required to prevent documented harm in any setting where NDV/AUT and NDV/MH co-occur.

This is a more consequential conflict than CON-0020 (DEAF glazed junctions) because it produces documented patient harm at scale in an existing building class.

### Evidence basis
| Source | Tier | Finding |
|---|---|---|
| NDTi / NHS England 2022 (Tandfonline DOI 10.1080/13575279.2022.2126437) | 1 (Co-1 autistic-led, peer-reviewed) | Systematic sensory design failure for NDV/AUT in NDV/MH wards |
| PAS 6463:2022 | 5 | Sensory zoning as design principle — not implemented in NHS wards |
| CON-0019 (environmental refuge) | Internal | Refuge provision would mitigate harm |
| CON-0040 (sensory zone system) | Internal | Three-zone model prevents one-size-fits-all ward design |

### Proposed synthesis direction
Part 7/8: document as mandatory provision — Zone 3 + environmental refuge specified as required (not recommended) in healthcare, education, and any building type where NDV/AUT + NDV/MH co-occurrence is foreseeable. Shifts zone provision from best practice to harm prevention mandate. Reference NHS CAMHS as paradigm failure case in Part 13.

### Disposition
- [ ] HIGH → Part 7/8 mandatory zoning + Part 13 failure case

---

## CON-0047 [2026-03-28 21:45]
**Mode:** Internal (case study evidence)
**Confidence:** HIGH
**Disposition:** PENDING
**Type:** N/A — methodological limitation
**Populations involved:** ALL
**Items involved:** Part 7/8 methodology (§7.1 / §8.2)
**Gap register items:** NONE

### Connection description
The cross-population case study Opus synthesis confirms: "Cross-population with outcomes for both populations: CONFIRMED NOT FOUND globally." No built environment study exists where a multi-population conflict resolution was implemented and both populations' outcomes were measured.

The closest cases document failures and corrections (DeafSpace rounded corners, Tenji blocks, NHS CAMHS), not pre-planned resolutions with dual-population outcomes. Part 7/8 conflict resolutions are principled syntheses from single-population evidence, not empirically validated multi-population outcomes.

Every resolution entry should carry a disclosure: "No built environment study has confirmed this resolution produces positive outcomes for both populations simultaneously." The IDEA Audit (CON-0029) could provide this validation — recommend dual-population POE as priority research agenda.

### Evidence basis
| Source | Status | Finding |
|---|---|---|
| Cross-population case studies BPC | COMPLETE Opus synthesis | Dual-population outcome studies: CONFIRMED NOT FOUND |
| Harrison et al. 2022 Cochrane (CS-22) | Tier 3 | 20 studies, 77,265 participants — very low certainty across all environmental design outcomes |
| DeafSpace SLCC (CS-08) | Co-1 | Documents failure + correction, not validated resolution |
| Kapsalis et al. 2024 (tenji blocks) | Tier 3 | Documents conflict, not resolution with dual outcome data |

### Proposed synthesis direction
Part 7/8 §7.1/§8.2 methodology note: explicit epistemic disclosure that conflict resolutions are evidence-informed syntheses, not empirically validated. Recommend dual-population POE as v11 research priority. Does not weaken Part 7/8 — strengthens it through honest epistemic framing.

### Disposition
- [ ] HIGH → Part 7/8 methodology note

---

## CON-0048 [2026-03-28 21:45]
**Mode:** Internal (case study evidence)
**Confidence:** HIGH
**Disposition:** PENDING
**Type:** [INTRA-INDIVIDUAL] — a person with MOB+DEM+PAIN benefits from home modification programme addressing all conditions
**Populations involved:** MOB, DEM, PAIN, OFS, ALL
**Items involved:** Part 12 (Economics)
**Gap register items:** NONE

### Connection description
Four evidence sources form a single economic argument at different scales:

- **CAPABLE** (CS-22, Tier 1 RCT, 6 trials, 1,087 participants): Programme cost ~$2,825 (including ~$700–$1,400 modifications). Hospitalisation 0.43→0.23/year (p=0.03). Modelled ROI: $10,000–$22,000 savings per participant.
- **LSE/Habinteg** (CS-23, Tier 2): M4(3) wheelchair standard costs ~£22,000 additional; produces ~£94,000 benefit over 10 years (4:1 ratio). Local authority savings £4,800–£9,200/year per household.
- **Sheffield** (Tier 1 RCT): 39% reduction in personal care hours from OT+modification.
- **Clemson Cochrane** (CON-0031/0032, Tier 3): 38% fall rate reduction; cost ratio 1:2.2 to 1:14.9.

These are not separate data points — they are a single economic continuum. $1,400 (single-room) → $2,825 (whole-home OT programme) → £22,000 (new-build wheelchair standard) all produce positive ROI. No source contradicts this. The economics section should present them as a unified case, not scattered citations.

### Evidence basis
| Source | Tier | Scale | ROI |
|---|---|---|---|
| CAPABLE RCT (Szanton 2019, PMID 30615024) | 1 | Single home (~$2,825) | $10,000–$22,000 modelled savings |
| LSE/Habinteg CASEreport 147 (2023) | 2 | New build (~£22,000 premium) | £94,000 benefit / 10 years |
| Sheffield RCT (2013, PMID 23213082) | 1 | Single home | 39% personal care hour reduction |
| Clemson Cochrane (2023, CD013258) | 3 | Environmental intervention | 38% fall rate reduction; 1:2.2–1:14.9 cost ratio |

### Proposed synthesis direction
Part 12: present as unified economic continuum — intervention at any scale is cost-effective. Anchor figures: CAPABLE ($2,825 → $10–22K savings), Habinteg (£22K → £94K benefit, 4:1), Sheffield (39% care hour reduction), Clemson (38% fall reduction, up to 1:14.9). Strongest economic argument in the guidebook — stronger than any single specification's clinical evidence.

### Disposition
- [ ] HIGH → Part 12 economics anchor evidence

---

## CON-0049 [2026-03-28 21:45]
**Mode:** Internal (case study evidence)
**Confidence:** HIGH
**Disposition:** PENDING
**Type:** [INTRA-INDIVIDUAL] — a person with co-occurring disabilities needs both environment AND support/assessment framework
**Populations involved:** ALL (MOB, NEU, DEM, OFS, PAIN primary evidence populations)
**Items involved:** Part 5 (residential process specification), Part 7/8 items
**Gap register items:** NONE (scope expansion)

### Connection description
Two Tier 1 studies converge on the most consequential finding for the guidebook's scope:

- **Douglas et al. 2024** (BMJ Open, Tier 1 qualitative): Support quality is a greater determinant of tenant QoL than the built environment in SDA housing.
- **Ainsworth et al. 2022** (Disabil Rehabil, Tier 1 qualitative): Outcomes are co-produced by environment AND OT process quality — therapists must understand clients' experience of home as initial step.

The broader implication: the guidebook specifies built environment provisions but does not specify the support, transition, and assessment framework that governs whether those provisions produce outcomes. The evidence says the framework matters more.

Connections: CON-0033 (CAPABLE) provides the specific validated framework (OT + nurse + handyman). CON-0027 (Housing Enabler) provides the Tier 2 assessment instrument. CON-0028 (Lawton docility-proactivity) provides theoretical grounding: Tier 2 is the proactivity stage — person actively shaping environment with professional support.

Together: the guidebook must expand scope from "what to build" to "what to build + how to assess + how to support + how to transition." Part 5 requires a process specification section co-primary with room matrices.

### Evidence basis
| Source | Tier | Key finding |
|---|---|---|
| Douglas et al. 2024 (BMJ Open) | 1 qualitative | Support quality > built environment for QoL |
| Ainsworth et al. 2022 (Disabil Rehabil, PMID 36394257) | 1 qualitative | Outcomes co-produced by environment + OT process quality |
| CAPABLE (Liu 2020, PMID 32951215) | 1 RCT | OT+nurse+handyman model: validated multicomponent framework |
| Carey et al. 2025 (PMID 41175339) | Co-1 | Family/carer transition support essential |
| Malmgren Fänge 2019 (PMID 31684916) | 1 quasi-experimental | Standardised OT assessment: OR 9.50 wheelchair mobility |

### Proposed synthesis direction
Part 5: add process specification section — structured OT assessment as prerequisite, multicomponent intervention model (CAPABLE), transition planning, ongoing support frameworks. Co-primary with room matrices. This is the single most important scope decision outstanding for the guidebook.

### Disposition
- [ ] HIGH → Part 5 structural expansion — process specification co-primary with room matrices

---

## CON-0050 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** BAR, MOB, MOB/UPL
**Items involved:** K-01, fold-down-grab-bar-specification
**Gap register items:** NONE

### Connection description
Fold-down grab bar load specification (200 kg SWL minimum per fold-down-grab-bar-specification BPC) conflicts with bariatric requirement documented in body-sizes-supplementary-populations BPC (300 kg user weight, WC + user). Bariatric WC users require ≥300 kg rated fold-down bars; standard MOB specification is structurally insufficient. Not currently cross-referenced in guidebook.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| fold-down-grab-bar-specification BPC | 3 | MOB | BAR load requirement |
| body-sizes-supplementary-populations BPC | 3 | BAR | grab bar loading |

### Proposed synthesis direction
Specify bariatric-rated fold-down grab bars (≥300 kg SWL) where BAR provision required; flag standard 200 kg bars as inadequate for BAR populations. Cross-reference K-01 with BAR body-sizes profile.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0051 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** DEAF, VIS, DBL, DEM, IntD
**Items involved:** D-05, wayfinding-dementia-spatial-design, cognitive-wayfinding-design
**Gap register items:** GAP-CON-02

### Connection description
Loop/linear circulation with no dead-ends serves five populations from independent clinical rationales: DEAF (visual field scan), VIS (tactile route memorisation), DBL (tactile navigation without choice points), DEM (prevents disorientation), IntD (reduces cognitive load). All five BPCs specify this geometry; currently siloed. This is a Tier 0 universal candidate.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| deaf-spatial-design BPC | 2 | DEAF | Tier 0 universal |
| visual-impairment-built-environment BPC | 2 | VIS | Tier 0 universal |
| wayfinding-dementia-spatial-design BPC | 2 | DEM | Tier 0 universal |
| deafblind-built-environment-design BPC | 4-5 | DBL | Tier 0 universal |
| intellectual-disability-built-environment-design BPC | 4-5 | IntD | Tier 0 universal |

### Proposed synthesis direction
Elevate loop/linear circulation to Tier 0 universal provision (D-02 revision). Mechanism: reduces wayfinding cognitive load for all users; essential for DEAF/VIS/DBL/DEM/IntD; neutral for others.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0052 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** DEAF, DBL
**Items involved:** A-10, A-11, assistive-listening-systems, deafblind-built-environment-design
**Gap register items:** GAP-CON-03, GAP-ALS-01

### Connection description
Hearing loop systems (IEC 60118-4) specified for DEAF populations serve DBL residual hearing users identically — not currently noted in DBL item specifications. DBL-specific guidance omits this provision despite documented DBL residual hearing prevalence (Edwards & Brentari 2020 per deafblind-built-environment-design BPC).

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| assistive-listening-systems BPC (IEC 60118-4) | 4 | DEAF | DBL residual hearing |
| deafblind-built-environment-design BPC (Edwards & Brentari 2020) | 2 | DBL | hearing loop applicability |

### Proposed synthesis direction
Add DBL as co-population for A-10/A-11 hearing loop items. Mechanism: residual hearing common in DBL; loop provision serves both DEAF and DBL without modification.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0053 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** VIS, DEAF, DBL, DEM, IntD
**Items involved:** D-09, residential-entry-and-threshold, cognitive-wayfinding-design
**Gap register items:** GAP-S4-R03, GAP-S4-R04, GAP-S4-R05, GAP-S4-R06

### Connection description
Consistent furniture layout (D-09) specified for DEM spatial memory serves VIS/DBL tactile navigation and IntD cognitive load reduction through identical mechanism — spatial predictability. Currently coded DEM-primary only; VIS/DBL/IntD applications documented in respective BPCs but not cross-referenced.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| dementia-built-environment BPC | 2 | DEM | VIS/DBL/IntD |
| deafblind-built-environment-design BPC | 4-5 | DBL | D-09 cross-ref |
| intellectual-disability-built-environment-design BPC | 4-5 | IntD | D-09 cross-ref |
| visual-impairment-built-environment BPC | 2 | VIS | D-09 cross-ref |

### Proposed synthesis direction
Recode D-09 as multi-population provision (DEM, VIS, DBL, IntD). Mechanism: spatial predictability reduces orientation barriers across four populations.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0054 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** OFS, PAIN, MOB/AMB, DEM
**Items involved:** E-14
**Gap register items:** GAP-FDR-T0-04

### Connection description
Entrance recline seating within 5 m of all accessible entrances (GAP-FDR-T0-04) serves four populations: OFS (orthostatic recovery), PAIN (joint relief), MOB/AMB (rest before walking), DEM (orientation pause point). Documented as Tier 0 candidate in gap register; not yet in guidebook item specifications.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| pain-ofs-built-environment-design BPC | 2 | OFS, PAIN | Tier 0 universal |
| mobility-built-environment BPC | 2 | MOB/AMB | entrance seating |
| dementia-built-environment BPC | 2 | DEM | entrance seating |

### Proposed synthesis direction
Create new item: entrance recline seating ≤5 m from accessible entrance (E-14). Specify as Tier 0 universal provision — essential for OFS/PAIN/MOB/AMB/DEM; beneficial for all.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0055 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** NEU, PAIN, OFS, MOB
**Items involved:** A-09
**Gap register items:** GAP-FDR-04

### Connection description
Cushioned/resilient flooring serves three populations via different mechanisms: MOB (WBV reduction per floor-vibration-wheelchair-disability BPC), PAIN (joint impact reduction per GAP-B4-09), NEU (fall impact mitigation per neurological-built-environment BPC). Currently only MOB provision documented in guidebook; PAIN and NEU applications thin-evidenced but mechanistically supported.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| floor-vibration-wheelchair-disability BPC (Misch 2022) | 2 | MOB | cross-population mechanism |
| GAP-B4-09 (expert consensus) | 5 | PAIN | thin evidence flag |
| neurological-built-environment BPC | 3-4 | NEU | fall impact |

### Proposed synthesis direction
Extend A-09 resilient flooring to PAIN and NEU as co-populations. Flag PAIN application as thin-evidenced (expert consensus only); NEU fall-impact application supported by fall injury literature.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0056 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** OFS, PAIN, MOB
**Items involved:** threshold-and-level-access, residential-entry-and-threshold
**Gap register items:** NONE

### Connection description
Zero-threshold entry (13-15 mm max) specified for MOB wheelchair caster wheels serves OFS and PAIN populations via step-elimination mechanism — steps trigger post-exertional malaise (PEM) in OFS and joint loading pain in PAIN. Currently coded MOB-only; OFS/PAIN clinical rationale documented in respective BPCs but not cross-referenced to threshold items.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| threshold-and-level-access BPC | 4 | MOB | OFS, PAIN |
| pain-ofs-built-environment-design BPC | 3 | OFS, PAIN | threshold items |

### Proposed synthesis direction
Add OFS and PAIN as co-populations for all threshold items (E-12, E-13). Mechanism: step elimination prevents PEM/pain triggers; same physical provision serves three populations.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0057 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** DEM, NEU, OFS, PAIN
**Items involved:** I-03
**Gap register items:** GAP-FDR-01-b

### Connection description
Thermostatic shower valve ≤37°C specified for OFS heat intolerance (pain-ofs-built-environment-design BPC) also prevents scalding risk for DEM and NEU populations documented in thermal-comfort-older-adults-care-settings BPC. Single specification serves four populations through two mechanisms: therapeutic temperature control (OFS) and safety (DEM/NEU).

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| pain-ofs-built-environment-design BPC | 3 | OFS | DEM, NEU safety |
| thermal-comfort-older-adults-care-settings BPC | 2 | DEM, older adults | thermostatic valve cross-ref |

### Proposed synthesis direction
Add DEM and NEU as co-populations for thermostatic shower valve specification. Dual mechanism: OFS therapeutic + DEM/NEU/PAIN safety.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0058 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** OFS, PAIN, MOB/AMB
**Items involved:** NONE
**Gap register items:** GAP-FDR-02

### Connection description
Bedroom-bathroom adjacency ≤5 m for OFS energy conservation (per pain-ofs-built-environment-design BPC) serves PAIN and MOB/AMB populations identically — reduces walking distance for populations with mobility/energy constraints. No standard currently specifies maximum bedroom-bathroom distance; OT energy conservation principle documented but not quantified in built environment codes.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| pain-ofs-built-environment-design BPC | 3 | OFS | PAIN, MOB/AMB |
| residential-accessible-home-case-studies BPC | 2 | MOB | bedroom-bathroom adjacency |

### Proposed synthesis direction
Create new DAR item: bedroom-bathroom adjacency ≤5 m for OFS, PAIN, MOB/AMB populations. Evidence: OT energy conservation + residential case study practice.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0059 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** BOTH
**Disposition:** PENDING
**Populations involved:** DEM, NEU, MH, OFS
**Items involved:** B-06, B-07
**Gap register items:** GAP-CON-06-b, GAP-034-b

### Connection description
Circadian lighting (≥250 melanopic EDI daytime) specified for DEM/NEU sleep-wake regulation serves MH and OFS populations via identical mechanism — circadian entrainment improves sleep outcomes across all four populations. MH and OFS BPCs document sleep disruption as core symptom but do not cross-reference circadian lighting specification.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| circadian-lighting-melanopic-edi BPC (Brown 2020) | 1 | DEM, NEU | MH, OFS |
| mental-health-built-environment BPC | 2 | MH | circadian lighting |
| pain-ofs-built-environment-design BPC | 3 | OFS | circadian lighting |

### Proposed synthesis direction
Add MH and OFS as co-populations for B-06/B-07 circadian lighting items. Mechanism: sleep-wake disruption common across DEM/NEU/MH/OFS; circadian lighting serves all four.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0060 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** VIS, DBL, DEM
**Items involved:** C-04, D-02
**Gap register items:** GAP-CON-01

### Connection description
Tactile walking surface indicators (TWSI, ISO 23599:2019) specified for VIS/DBL navigation serve DEM spatial orientation via identical physical mechanism — continuous tactile guide reduces disorientation. DEM application not currently cross-referenced despite wayfinding-dementia-spatial-design BPC documenting tactile landmark effectiveness.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| visual-impairment-built-environment BPC (ISO 23599:2019) | 4 | VIS, DBL | DEM |
| wayfinding-dementia-spatial-design BPC | 2 | DEM | TWSI cross-ref |

### Proposed synthesis direction
Add DEM as co-population for TWSI items. Mechanism: continuous tactile route serves VIS/DBL navigation + DEM orientation memory support.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0061 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** DEAF, VIS, DBL, DEM, IntD
**Items involved:** E-08, accessible-circulation-geometry
**Gap register items:** GAP-CO03-07

### Connection description
Corridor width ≥1500 mm for two-person side-by-side walking specified for DEAF signing conversation (deaf-spatial-design BPC) also accommodates VIS sighted guide, DBL intervenor, DEM support person, and IntD care companion — all requiring side-by-side width. Five populations, single dimensional requirement, currently siloed.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| deaf-spatial-design BPC (Gallaudet 2010) | 2 | DEAF | VIS, DBL, DEM, IntD |
| accessible-circulation-geometry BPC | 4 | MOB | DEAF, VIS, DBL, DEM, IntD |
| deafblind-built-environment-design BPC | 4-5 | DBL | corridor width |

### Proposed synthesis direction
Consolidate 1500+ mm corridor width as multi-population provision (DEAF, VIS, DBL, DEM, IntD, MOB). Mechanism: side-by-side communication/support width universal across populations.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0062 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** LPA, MOB, OFS, PAIN, VIS
**Items involved:** I-02, residential-kitchen-and-task-surfaces
**Gap register items:** NONE

### Connection description
Height-adjustable kitchen worktop (685-900 mm, per residential-kitchen-and-task-surfaces BPC) specified for MOB wheelchair users also serves LPA (lower reach range), OFS/PAIN (seated work), and VIS (tactile work surface at consistent height). Currently coded MOB-primary; other populations documented in respective BPCs but not cross-referenced.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| residential-kitchen-and-task-surfaces BPC | 2 | MOB | LPA, OFS, PAIN, VIS |
| reach-range-and-accessible-controls BPC | 4 | MOB, LPA | kitchen items |
| body-sizes-supplementary-populations BPC | 3 | LPA | kitchen worktop |

### Proposed synthesis direction
Add LPA, OFS, PAIN, VIS as co-populations for height-adjustable kitchen worktop specification. Mechanism: adjustability serves five populations via different reach/work-position requirements.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0063 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** NDV, OFS, PAIN, MH
**Items involved:** F-02, F-04
**Gap register items:** GAP-CON-15

### Connection description
Fragrance-free policy + MERV 13+ filtration (F-02, F-04) specified for OFS/MCAS and NDV chemical sensitivity serves MH/PTSD populations via identical mechanism — chemical stimuli as trauma triggers. Trauma-informed design framework (mental-health-built-environment BPC) emphasises environmental predictability but does not cross-reference air quality specifications.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| air-quality-voc-chemical-sensitivity-built-environment BPC | 3 | OFS, NDV | MH |
| mental-health-built-environment BPC | 2 | MH | F-02, F-04 cross-ref |

### Proposed synthesis direction
Add MH as co-population for F-02/F-04 air quality items. Mechanism: chemical stimuli reduction serves OFS/NDV physiological + MH trauma-trigger avoidance.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0064 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** OFS, PAIN, MOB/AMB
**Items involved:** G-06
**Gap register items:** GAP-FDR-03

### Connection description
Seated service counter option for OFS orthostatic intolerance (pain-ofs-built-environment-design BPC) also serves PAIN (reduces standing load) and MOB/AMB (eliminates standing barrier). No standard currently requires seated service counter provision; OT practice documents need but not quantified specification.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| pain-ofs-built-environment-design BPC | 3 | OFS | PAIN, MOB/AMB |
| mobility-built-environment BPC | 2 | MOB | seated service counter |

### Proposed synthesis direction
Create new item: seated service counter option (≥1 per facility) for OFS, PAIN, MOB/AMB. Specification: counter height 760-850 mm, knee clearance per reach-range standards.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0065 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** OFS, PAIN, NEU
**Items involved:** NONE
**Gap register items:** GAP-FDR-05

### Connection description
Mandatory shade on outdoor circulation routes for OFS heat intolerance (pain-ofs-built-environment-design BPC) also serves PAIN (reduces inflammatory triggers) and NEU (prevents heat-exacerbated symptoms). No standard currently specifies outdoor shade provision; OT practice documents need but not architectural specification.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| pain-ofs-built-environment-design BPC | 3 | OFS | PAIN, NEU |
| ms-thermal-temperature-conflict-resolution BPC | 2 | NEU | outdoor shade |

### Proposed synthesis direction
Create new item: continuous shade on primary outdoor routes (natural or built) for OFS, PAIN, NEU thermal management. Evidence: heat intolerance documented across three populations.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0066 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** OFS, PAIN
**Items involved:** NONE
**Gap register items:** GAP-FDR-06

### Connection description
Adjustable bed head elevation for OFS head-up tilt sleeping (pain-ofs-built-environment-design BPC) also serves PAIN populations requiring positional pain management. No residential standard specifies bed adjustability; OT assistive technology practice documents need but not as built environment specification.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| pain-ofs-built-environment-design BPC | 3 | OFS | PAIN |

### Proposed synthesis direction
Create DAR item: bedroom electrical provision for adjustable bed (future provision). Not mandatory bed installation; enables future adaptation for OFS/PAIN populations.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0067 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** DEM, IntD, NEU, NDV/AUT
**Items involved:** D-02, cognitive-wayfinding-design
**Gap register items:** GAP-CON-0030

### Connection description
Cognitive wayfinding research (Brunyé 2018 per GAP-CON-0030) quantifies decision-point mechanism: uncertainty peaks at 3+ route choices. DEM, IntD, NEU, and NDV/AUT populations share identical cognitive load threshold — ≤2 choices per decision point reduces disorientation. Currently qualitative in guidebook; quantitative threshold available.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| cognitive-wayfinding-design BPC (Marquardt 2011) | 2 | DEM | IntD, NEU, NDV |
| wayfinding-cognitive-science-spatial-design BPC | 2 | DEM | quantified threshold |
| GAP-CON-0030 (Brunyé 2018) | 2 | DEM | ≤2-choice specification |

### Proposed synthesis direction
Specify ≤2 route choices per decision point for DEM, IntD, NEU, NDV/AUT populations. Mechanism: reduces cognitive load at wayfinding decision nodes across four populations.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0068 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** DEM, NEU, NDV/AUT, OFS
**Items involved:** NONE
**Gap register items:** NONE

### Connection description
"Toilet visible from primary occupied space" specified for DEM (Marquardt 2011, reduces incontinence) also serves NEU/NDV/AUT (reduces anxiety/overload from searching) and OFS (reduces energy expenditure). Four populations, single design principle, currently siloed in DEM BPC only.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| dementia-built-environment BPC (Marquardt 2011) | 2 | DEM | NEU, NDV, OFS |
| neurodivergent-built-environment BPC | 2 | NDV | toilet visibility |
| pain-ofs-built-environment-design BPC | 3 | OFS | toilet proximity |

### Proposed synthesis direction
Elevate toilet visibility to multi-population provision (DEM, NEU, NDV/AUT, OFS). Mechanism: eliminates search burden for four populations via different clinical rationales.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0069 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** BAR, MOB
**Items involved:** bariatric-turning-radius-built-environment, accessible-circulation-geometry
**Gap register items:** NONE

### Connection description
Bariatric turning radius (≥1900 mm per bariatric-turning-radius-built-environment BPC) exceeds standard MOB turning space (1500-1525 mm per accessible-circulation-geometry BPC) by 375-400 mm. Single BAR user population requires larger dimension than all MOB specifications accommodate; currently documented as separate provision.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| bariatric-turning-radius-built-environment BPC (Steinfeld 2006) | 2 | BAR | MOB turning space revision |
| accessible-circulation-geometry BPC | 4 | MOB | BAR inadequacy |

### Proposed synthesis direction
Flag standard MOB turning space (1500-1525 mm) as inadequate for BAR populations. Specify 1900 mm where BAR provision required; 1800 mm minimum adaptation threshold.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0070 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** CHD, LPA, MOB
**Items involved:** H-01, reach-range-and-accessible-controls
**Gap register items:** NONE

### Connection description
Children's reach range (lower than adult wheelchair users per body-sizes-supplementary-populations BPC) overlaps with LPA and seated adult reach zones. Controls at 400-600 mm serve CHD standing + LPA/MOB seated; single height band serves three populations. Not currently cross-referenced.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| body-sizes-supplementary-populations BPC | 3 | CHD, LPA | MOB reach overlap |
| reach-range-and-accessible-controls BPC | 4 | MOB, LPA | CHD cross-ref |

### Proposed synthesis direction
Note 400-600 mm control zone serves CHD, LPA, and seated MOB populations. Mechanism: lower reach range common across three populations for different anthropometric reasons.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0071 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** NDV, MH, DEM, NEU
**Items involved:** BIO-series
**Gap register items:** GAP-CON-04

### Connection description
Biophilic outdoor/nature spaces documented independently in three BPCs: biophilic-design (NDV, reduces stress), mental-health-built-environment (MH trauma recovery), dementia-built-environment (DEM reduces agitation). All three cite nature exposure as therapeutic without cross-reference. Extends CON-0010 with NEU addition.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| biophilic-design-healthcare-workplace BPC (Ulrich 1984) | 1 | all | NDV, MH, DEM, NEU |
| mental-health-built-environment BPC | 2 | MH | biophilic cross-ref |
| dementia-built-environment BPC | 2 | DEM | biophilic cross-ref |

### Proposed synthesis direction
Consolidate biophilic/nature provisions as multi-population (NDV, MH, DEM, NEU). Create unified BIO-series items with population-specific mechanisms documented.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0072 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** OFS, PAIN
**Items involved:** NONE
**Gap register items:** GAP-FDR-07

### Connection description
Workplace lie-down/supine recovery space for OFS PEM management (pain-ofs-built-environment-design BPC) also serves PAIN populations requiring horizontal rest for pain relief. No workplace standard specifies supine rest provision; OT occupational health practice documents need but not architectural specification.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| pain-ofs-built-environment-design BPC | 3 | OFS | PAIN |
| ofs-built-environment BPC | 3 | OFS, PAIN | workplace supine rest |

### Proposed synthesis direction
Create new workplace item: supine rest space (quiet room with reclining surface) for OFS/PAIN populations. Evidence: horizontal rest documented for both populations.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0073 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** OFS, NEU
**Items involved:** NONE
**Gap register items:** GAP-FDR-08

### Connection description
Thermal transition zone (vestibule cooling) at entrance for OFS heat intolerance (pain-ofs-built-environment-design BPC) also serves NEU/MS populations with Uhthoff's phenomenon (heat-exacerbated symptoms per ms-thermal-temperature-conflict-resolution BPC). No standard specifies entrance thermal transition; climate adaptation practice emerging.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| pain-ofs-built-environment-design BPC | 3 | OFS | NEU thermal transition |
| ms-thermal-temperature-conflict-resolution BPC | 2 | NEU | entrance vestibule |

### Proposed synthesis direction
Create new item: entrance thermal transition zone (vestibule with cooling) for OFS/NEU populations. Evidence: heat intolerance documented for both populations.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0074 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** DEAF, VIS, DEM, NDV/AUT
**Items involved:** deaf-spatial-design
**Gap register items:** GAP-CON-0020

### Connection description
DEAF glazed corridor junctions (DeafSpace visual advance warning per deaf-spatial-design BPC) potentially conflict with VIS glare, DEM reflective surface confusion, and NDV visual noise. Spatial conflict documented in GAP-CON-0020 but resolution not specified. Requires matte glazing + strategic placement to serve DEAF without compromising other populations.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| deaf-spatial-design BPC (Gallaudet 2010) | 2 | DEAF | conflict resolution |
| dementia-built-environment BPC | 2 | DEM | glazing confusion |
| sensory-processing-model-design-application BPC | 3 | NDV | visual noise |

### Proposed synthesis direction
Specify matte/low-reflectance glazing at DEAF corridor junctions; position to avoid VIS glare paths. Zone-specific application where populations identified.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0075 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** NDV/AUT, VIS
**Items involved:** NONE
**Gap register items:** GAP-CON-0025

### Connection description
Sensory-responsive outdoor landscape (Finnigan 2024 SREF per GAP-CON-0025) for NDV populations overlaps with VIS tactile/auditory navigation landscape design. Outdoor spaces serve both populations through different sensory mechanisms — NDV sensory modulation + VIS non-visual wayfinding. Not currently cross-referenced.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| GAP-CON-0025 (Finnigan 2024) | 2 | NDV | VIS |
| visual-impairment-built-environment BPC | 2 | VIS | outdoor landscape |

### Proposed synthesis direction
Create outdoor landscape design guidance integrating NDV sensory-responsive elements + VIS tactile/auditory wayfinding. Evidence: both populations benefit from sensory-rich outdoor design.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0076 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** NDV/AUT, NEU, DEM
**Items involved:** A-16, sensory-room-user-control
**Gap register items:** GAP-CON-0026

### Connection description
Van Doorn et al. 2024 scoping review (GAP-CON-0026) finds mixed evidence for static sensory adaptive environments (SAEs) — individual control more important than fixed parameters. This principle extends from NDV/AUT to NEU/DEM populations: user-controlled sensory environment outperforms standardised design across all three populations.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| GAP-CON-0026 (Van Doorn 2024) | 2 | NDV/AUT | NEU, DEM |
| sensory-room-user-control BPC | 3 | NDV | NEU, DEM cross-ref |

### Proposed synthesis direction
Elevate user control principle to cross-population doctrine (NDV, NEU, DEM). Mechanism: individual sensory preferences vary within populations; control > fixed environment.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0077 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** ALL
**Items involved:** Part 4 POE
**Gap register items:** NONE

### Connection description
Two independent POE tool development programmes (IDEA Audit, Zallio & Langford per CON-0029) have created inclusive-design-specific post-occupancy evaluation instruments. Guidebook does not reference either; no POE methodology currently specified for accessibility compliance verification at ready-for-occupancy stage.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| CON-0029 (IDEA Audit, Zallio) | 2 | all | Part 4 POE specification |
| residential-accessible-home-case-studies BPC | 2 | all | POE requirement |

### Proposed synthesis direction
Specify IDEA Audit or equivalent as POE tool for accessibility verification. Evidence: validated instruments exist; guidebook lacks POE methodology.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0078 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** ALL
**Items involved:** Part 1 structure
**Gap register items:** GAP-CON-0032

### Connection description
2025 scoping review (64 studies, Nature HSSC per CON-0032) identifies seven interior design principles for older adult health. These align with guidebook item categories; validates current structure but identifies sensory environment as under-addressed.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| CON-0032 (Nature HSSC 2025) | 2 | all | Part 1 structure validation |
| design-framework-evidence-audit BPC | 3 | all | item category alignment |

### Proposed synthesis direction
Note 2025 scoping review validation of guidebook item category structure. Flag sensory environment (acoustics, air quality, thermal) as under-addressed relative to evidence base.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0079 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** MOB, OFS, PAIN
**Items involved:** R-LAU
**Gap register items:** GAP-LAU-01, GAP-LAU-02

### Connection description
Front-loading appliances on risers (380-430 mm drum centre per accessible-laundry-room-design BPC) specified for MOB seated reach also serve OFS/PAIN populations avoiding floor-level bending. Single specification serves three populations through different clinical mechanisms — MOB reach range + OFS/PAIN exertion reduction.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| accessible-laundry-room-design BPC | 2 | MOB | OFS, PAIN |
| GAP-LAU-01 | — | MOB | multi-population |

### Proposed synthesis direction
Add OFS and PAIN as co-populations for laundry appliance riser specification. Mechanism: raised drum height serves MOB reach + OFS/PAIN bending avoidance.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0080 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** DBL, IntD
**Items involved:** All room matrices
**Gap register items:** GAP-S4-R01 through GAP-S4-N07

### Connection description
DBL and IntD populations absent from 15/16 room matrices (GAP-S4 series) despite documented requirements in respective BPCs. Both populations require provisions not currently specified: DBL tactile navigation consistency, IntD cognitive load reduction. Room matrix gap items document systematic omission across residential and non-residential typologies.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| deafblind-built-environment-design BPC | 4-5 | DBL | all room matrices |
| intellectual-disability-built-environment-design BPC | 4-5 | IntD | all room matrices |
| GAP-S4-series | — | DBL, IntD | room specifications |

### Proposed synthesis direction
Systematically add DBL and IntD provisions to all room matrices. DBL: tactile consistency, haptic communication space. IntD: visual simplicity, intuitive layout, pictogram signage.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0081 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** VIS, DEAF, DBL
**Items involved:** B-10, visual-alerting-and-wayfinding-light
**Gap register items:** NONE

### Connection description
Visual alerting systems serve DEAF/VIS/DBL through different mechanisms: DEAF strobes for visual alert, VIS high-contrast wayfinding light, DBL vibrotactile + residual vision. Three populations require coordinated visual alerting strategy; currently specified separately without integration.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| visual-alerting-and-wayfinding-light BPC | 2 | VIS, DEAF, DBL | integrated strategy |
| assistive-listening-systems BPC | 4 | DEAF | DBL cross-ref |

### Proposed synthesis direction
Create integrated visual alerting specification serving DEAF/VIS/DBL. Coordinate VAD placement, contrast requirements, and vibrotactile supplementation.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0082 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** HIGH
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** ALL
**Items involved:** DAR items, residential-dar-provisions-priority-register
**Gap register items:** GAP-CON-12, GAP-NEW-12

### Connection description
Italian DM 236/89 adattabilità (design for adaptable readiness) + visitability (three core requirements) represent two models for minimum residential accessibility. Both require DAR provisions physically embedded in construction drawings; both prevent future adaptation cost multipliers. Not currently cross-referenced as complementary strategies.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| residential-dar-provisions-priority-register BPC | 4 | all | adattabilità comparison |
| visitability-residential-accessibility-minimum-standards BPC | 2 | MOB | DAR integration |

### Proposed synthesis direction
Present adattabilità and visitability as complementary DAR models: adattabilità = structural readiness, visitability = basic access. Both prevent retrofit cost multipliers.

### Disposition
- [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0083 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** MODERATE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** DEAF, VIS, DBL, NDV
**Items involved:** A-02, A-08, A-13
**Gap register items:** NONE

### Connection description
Non-English language evidence (DE DIN 18041, ZH, FR CEREMA per multilingual-evidence-convergence-non-english BPC) provides stronger acoustic specification for disability populations than English-language sources. Seven provisions have stronger empirical evidence in non-English literature; this language-based evidence gap affects DEAF, NDV acoustic items.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| multilingual-evidence-convergence-non-english BPC | 4 | all | acoustic items |

### Proposed synthesis direction
Flag English-language evidence limitation in acoustic items. Note stronger evidence base exists in DE/ZH/FR for DEAF/NDV provisions.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

## CON-0084 [2026-03-28 22:15]

**Mode:** Internal
**Confidence:** SPECULATIVE
**Type:** INTER-GROUP
**Disposition:** PENDING
**Populations involved:** ALL
**Items involved:** Part 8
**Gap register items:** GAP-054

### Connection description
Cross-population conflict resolution has no peer-reviewed methodological framework in any language (GAP-054). Guidebook resolves nine documented conflicts (cross-population-conflict-resolutions BPC) but lacks systematic methodology. Prospect-refuge theory (CON-0024) + sensory processing model may provide theoretical framework, but research gap remains.

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| cross-population-conflict-resolutions BPC | 3 | all | methodology framework |
| GAP-054 | — | all | research gap |
| CON-0024 (prospect-refuge) | 2 | all | potential framework |

### Proposed synthesis direction
Flag cross-population conflict resolution as under-researched domain. Note guidebook provides nine case-based resolutions but lacks theoretical framework.

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [x] SPECULATIVE → P3 gap item