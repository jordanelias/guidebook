# Connections — entrances-and-circulation
<!-- CO-0006 Phase 0B-1 migration 2026-04-08 — from connection-register-active.md -->

### CON-0006

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** B-01 (circadian lighting)
**Target population(s):** DEM, NEU, NDV, MH, OFS
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Circadian lighting (≥250 melanopic EDI daytime) specified for DEM/NEU. MH BPC and OFS BPC do not mention circadian lighting despite clear clinical relevance: MH/PTSD sleep disruption and OFS fatigue cycle disruption both benefit from circadian entrainment. Population coding update only — no specification change.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Brown et al. 2022 | 3 | ALL (general) | MH, OFS explicit |
| CDC ME/CFS (sleep disruption) | Co-1 | OFS | OFS circadian |

**Action required:** Add MH and OFS as explicit co-populations for B-01.

**Disposition notes:** - [ ] MODERATE → P2 gap item

---

### CON-0008

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-02, A-08, A-13
**Target population(s):** PAIN, OFS, NEU
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Room acoustic items coded for DEAF, DEM, NDV populations. OFS BPC identifies acoustic sensitivity ("no forced air as sole source — acoustic trigger concern"). PAIN BPC: Geisser et al. 2021 identifies hyperacusis as fibromyalgia symptom. Neither population coded on acoustic items.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Geisser et al. 2021 | 3 | PAIN | PAIN acoustic |
| CDC ME/CFS (sensory sensitivity) | Co-1 | OFS | OFS acoustic |
| PAS 6463:2022 | 5 | NDV | NDV, OFS, PAIN |

**Action required:** Add PAIN and OFS as co-populations for A-02/A-08/A-13 with THIN-POPULATION-SPEC disclosure.

**Disposition notes:** - [ ] MODERATE → P2 gap item

---

### CON-0009

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** Threshold items (residential-entry-and-threshold)
**Target population(s):** MOB, OFS, PAIN
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Entry/threshold BPC specifies level access for MOB/wheelchair. OFS (energy conservation — steps trigger PEM) and PAIN (joint loading on steps) benefit but are not listed. Specification values unchanged; population coding update only.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Kos et al. 2015 AJOT | 1 | OFS (behavioural) | OFS (architectural) |
| CDC ME/CFS (PEM from exertion) | Co-1 | OFS | OFS |

**Action required:** Add OFS and PAIN as co-populations for entry/threshold items.

**Disposition notes:** - [ ] MODERATE → P2 gap item

---

### CON-0010

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** BIO-01–BIO-05, A-16
**Target population(s):** DEM, OFS, NDV, MH
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Three BPC entries independently identify outdoor/nature spaces as therapeutic without cross-reference: biophilic-design (nature exposure reduces stress/pain — Al Khatib 2024 SR); dementia (outdoor loop routes reduce agitation — Danish evidence); OFS (rest spaces at ≤50m — no nature connection despite restorative potential); sensory-relief (transition zone — no outdoor decompression link). Convergence: outdoor therapeutic spaces serve DEM + OFS + NDV + MH through single spatial solution.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Latiff et al. 2024 (NDV outdoor decompression) | Co-1 | NDV | NDV, MH |
| Al Khatib et al. 2024 (biophilic SR, 61 sources) | 3 | ALL (healthcare) | DEM, OFS, MH |
| Danish DEM loop garden evidence | Co-1 | DEM | DEM, OFS |

**Action required:** Cross-reference biophilic outdoor items with DEM garden loop, OFS rest provision, NDV decompression, MH nature exposure. Consider unified "therapeutic outdoor space" specification.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing

---

### CON-0014

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** B-10, visual-fire-alarm items
**Target population(s):** DEAF, DBL, NEU, NDV
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Visual-fire-alarm conflict resolution (DEAF/DBL need strobes; NEU/NDV at seizure risk from same) relies on vibrotactile as alternative channel for photosensitive populations. GAP-035: no jurisdiction specifies vibrotactile device type, intensity, latency, or coverage. Conflict resolution is principled but unimplementable without vibrotactile specification.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| RNID / HLAA / Bufdir recommendations | Co-1/2 | DEAF (vibrotactile) | DEAF, DBL, NEU |

**Action required:** New item: Vibrotactile Alerting Device (sleeping areas) — minimum vibration intensity, latency ≤3 s, coverage all sleeping rooms where DEAF/DBL/photosensitive populations primary. Completes visual-fire-alarm conflict resolution chain; resolves GAP-035.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing

---

### CON-0019

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-16 (Sensory Room), NDV/MH retreat room, OFS rest space
**Target population(s):** NDV/AUT, NDV/MH, OFS, PAIN
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Extends CON-0002 (sensory/MH overlap) and CON-0004 (seated/reclined provision). Four populations independently require a low-stimulation refuge space: NDV/AUT (sensory quiet room A-16), NDV/MH (de-escalation/safe retreat ≥9 m²), OFS (low-stimulation rest space), PAIN (energy conservation rest point). These share overlapping functional requirements: low acoustic load (RT60 ≤0.4 s), user-controlled lighting, no through-traffic, accessible location. Currently specified as four distinct room types across four BPC entries. The synthesis: a single "environmental refuge" at Universal Mode — every occupied floor plate includes one refuge room — with population-specific overlays at Tier 1 (NDV/AUT: sensory e…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| PAS 6463:2022 | Tier 5 | NDV/AUT, DEM | OFS, PAIN, NDV/MH |
| OFS BPC rest space provision | Co-1/Tier 3 | OFS | NDV/AUT, NDV/MH, PAIN |
| NDV/MH BPC retreat room | Tier 2–4 | NDV/MH | OFS, PAIN |
| Sensory room user control BPC | Co-1 | NDV/AUT | All four |
| ASPECTSS escape space (Mostafa 2014) | Tier 1 | NDV/AUT | Cross-population |

**Action required:** Specify "environmental refuge space" as Universal Mode universal provision: one per occupied floor plate; user-controlled lighting (2700–5000 K dimmable); RT60 ≤0.4 s; no through-traffic; accessible without passing through high-stimulation zones. Population overlays added at Tier 1 per OT assessment.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

### CON-0020

**Status:** CONSUMED
**Confidence:** SPECULATIVE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** DEAF corridor glazing (DeafSpace), DEM glare provisions, VIS glare control, NDV visual noise
**Target population(s):** DEAF, VIS, DEM, NDV/AUT
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** DEAF BPC specifies glazed corridor junctions for visual advance warning — a DeafSpace principle replacing opaque corners with transparent ones. DEM BPC identifies reflective/high-gloss surfaces as problematic (perceived as wet/holes). VIS BPC identifies glare as a barrier. NDV/AUT BPC requires reduced visual noise. Glazed junctions serve DEAF but may create: glare for VIS users; reflective confusion for DEM users; visual complexity for NDV/AUT users. This is a potential four-way conflict not documented in any BPC or in the conflict resolution BPC. The DeafSpace literature documents the curved-corner collision problem (Gallaudet) but the glazing solution's interaction with VIS/DEM/NDV is unas…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| DeafSpace Guidelines 2010 | Co-1 | DEAF | Conflict assessment needed |
| DSDC glare guidance | Tier 3–5 | DEM | Conflict with DEAF glazing |
| PAS 6463 visual noise | Tier 5 | NDV | Conflict with DEAF glazing |
| BS 8300 / DIN 32975 glare guidance | Tier 5 | VIS | Conflict with DEAF glazing |

**Action required:** Document as a conflict requiring resolution. Possible mitigations: anti-reflective coating on glazing; etched/frosted lower band maintaining upper sightline for signing; matte floor adjacent to glazed junction to eliminate floor reflections. Flag for §IV.2 conflict resolution or Opus 4 cross-synthesis if standard resolution fails.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [x] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

### CON-0023

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-16 (Sensory Room), NDV BPC
**Target population(s):** NDV/AUT, NDV/ADHD, NDV/SENS
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Al-Harasis, Jabi & Sharmin (2025, Building Research & Information) published a taxonomy of 83 sensory-informed architectural design qualities for autism, based on review of 76 sources. Critical finding: current autism design frameworks (including ASPECTSS) rely on "intuition sensory zoning as the main driver for spatial topology without quantifying the sensory drivers" and emphasise "interior design elements over spatial configuration." This is a direct critique of how the guidebook specifies A-16 and NDV provisions — qualitative parameters without quantified sensory driver hierarchy. The taxonomy provides a structured classification that could inform the guidebook's item specification appro…

**Evidence basis:**
| Source | Tier | Field | Not yet in guidebook? |
|---|---|---|---|
| Al-Harasis et al. 2025 (Building Research & Information 53(4):532-551) | Tier 3 | Architecture + sensory science | YES — published Feb 2025 |
| Caniato et al. 2022a/b (Energy Reports) — sensitivity drivers for ASD indoor comfort | Tier 3 | Indoor environment | YES — not cited |
| SENSHOME/BeSENSHome project (Austria/Italy) — smart home for autism | Tier 3 | Assistive technology + architecture | YES — not cited |

**Action required:** Use the Al-Harasis taxonomy to audit the guidebook's NDV item specifications for coverage gaps against the 83 identified design qualities. Prioritise the taxonomy's finding that spatial configuration (layout topology, not just finish materials) is under-specified. This would feed into a future item-specification-writer run for NDV items. Add to NDV BPC as a structural reference.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

### CON-0024

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** Environmental refuge (CON-0019), biophilic outdoor (CON-0015), NDV/MH retreat
**Target population(s):** ALL
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Prospect-refuge theory (Appleton 1975; Hildebrand 1991) — the human need for environments providing both clear outward views (prospect) and sheltered protected spaces (refuge) — provides theoretical grounding from environmental psychology for several of the guidebook's cross-population provisions. The "environmental refuge" room (CON-0019) is literally a refuge space. The facility sightline principle (CON-0018) is a prospect provision. The biophilic outdoor space with looped path and seating (CON-0015) combines prospect (garden views) and refuge (sheltered seating). The guidebook currently derives these provisions from disability-specific clinical evidence but does not cite the environmental…

**Evidence basis:**
| Source | Tier | Field | Not yet in guidebook? |
|---|---|---|---|
| Appleton 1975 "The Experience of Landscape" | Foundational theory | Environmental psychology | YES — not cited |
| Dosen & Ostwald 2016 — meta-analysis of 34 prospect-refuge studies | Tier 3 | Architecture + psychology | YES — not cited |
| UD2024 Carpe Diem dementia village presentation (Bærum, Norway) — prospect-refuge in dementia care | Tier 5 / Co-1 | Architecture + dementia care | YES — not cited |
| Frontiers in Psychology 2025 — healing landscape prospect-refuge balance | Tier 3 | Environmental psychology | YES — not …

**Action required:** Cite prospect-refuge theory in Part III (design hierarchy) as theoretical support for the guidebook's Universal Mode provisions. The theory provides a non-disability-specific explanation for why environmental refuge, facility sightline, and biophilic outdoor spaces are universal human needs — not disability-specific accommodations. This strengthens the social model framing: disability populations do not n…

**Disposition notes:** - [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

### CON-0025

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** Outdoor provisions, biophilic BPC
**Target population(s):** NDV/AUT, NDV/ADHD, NDV/SENS, VIS
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Finnigan 2024 (Land 13(5):636) introduces the Sensory Responsive Environments Framework (SREF) based on 31 interviews with people with autism, ADHD, and dyslexia about their experiences in outdoor built environments. Key finding: outdoor landscape design for neurodivergent users is almost entirely unaddressed — existing frameworks (ASPECTSS, PAS 6463) focus on indoor environments. The guidebook's outdoor provisions (biophilic outdoor space, secure garden for DEM) do not address sensory-responsive outdoor design for NDV populations. SREF identifies: ambient environmental factors (wind, temperature, sun exposure), materiality (surface textures, visual complexity of materials), spatial design (…

**Evidence basis:**
| Source | Tier | Field | Not yet in guidebook? |
|---|---|---|---|
| Finnigan 2024 (Land 13(5):636) — SREF framework | Tier 3 (Co-1 qualitative) | Landscape architecture + NDV | YES |
| Guangzhou VIS park study 2024 (Landscape and Urban Planning) | Tier 3 | Environmental psychology + VIS | YES |
| Mostafa 2023 Venice Biennale — "sensory decolonization" concept | Co-1 | Architecture + NDV | YES |

**Action required:** Extend the guidebook's outdoor design provisions beyond biophilic and DEM secure garden to include sensory-responsive outdoor landscape design for NDV and VIS populations. The SREF framework provides a structured approach. Mostafa's "sensory decolonization" concept reframes outdoor sensory provision from accommodation to equity — sensory overstimulation in public space is as disabling as a flight …

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

### CON-0026

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** Part III (evidence hierarchy), methodology
**Target population(s):** ALL
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Van Doorn et al. 2024 (Research in Autism Spectrum Disorders 113:102350) — scoping review of sensory adaptive environments (SAEs) for autistic children — finds "mixed evidence" and a critical methodological gap: "sensory adaptive environments are not tailored to the sensory needs of each child." This finding independently validates the guidebook's three-tier hierarchy: Universal Mode/1 specifications are population-informed defaults that must be resolved through Tier 2 co-design for individual users. The SAE review confirms that generic sensory rooms (equivalent to Tier 1) have limited evidence; individualised sensory environments (equivalent to Tier 2) are more effective but under-researched. Pille…

**Evidence basis:**
| Source | Tier | Field | Not yet in guidebook? |
|---|---|---|---|
| Van Doorn et al. 2024 (RASD 113:102350) — SAE scoping review | Tier 3 | OT + autism research | YES |
| Piller et al. 2025 (Frontiers in Pediatrics 13:1720179) — SBI systematic review | Tier 3 | OT + paediatrics | YES |

**Action required:** Cite both reviews in the sensory room (A-16) evidence base as methodological support for the three-tier approach. The evidence confirms that generic sensory environments have mixed evidence (supporting Tier 1 as a starting point only) while individualised approaches show more promise (supporting Tier 2 as the resolution). Add to the NDV BPC evidence-auditor notes.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

### CON-0030

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** CON-0001 items (circulation legibility); cognitive wayfinding items
**Target population(s):** DEM, IntD, NDV/AUT, VIS, NEU
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Cognitive ergonomics research on wayfinding quantifies the decision-point mechanism that the guidebook specifies qualitatively (CON-0001: three or fewer decision points per segment for IntD):

1. Wayfinding uncertainty model (bioRxiv 2023, validated Study 1 n=28, Study 2 n=11): Wayfinding uncertainty correlates with time elapsed since last helpful sign. The model predicts human-reported uncertainty levels under different signage conditions (ROC-AUC 0.70). Implication: signage spacing is a quantifiable parameter — the guidebook could specify maximum distance between wayfinding cues.

2. Intersection-based decision points (Bruyne et al. 2018, Cognitive Research: Principles and Implications 3:1…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| bioRxiv 2023 wayfinding uncertainty model | 3 | General (neuroscience) | DEM, IntD, NDV/AUT |
| Bruyne et al. 2018 (intersection decision dynamics) | 3 | General (cognitive science) | DEM, IntD, VIS |
| Morag et al. 2024 (hospital wayfinding MCDM) | 3 | MOB, VIS, cognitive impairment | ALL |
| Lupien et al. 1998 (route complexity = decision point count) | 3 | General (neuroscience) | DEM, IntD |

**Action required:** Strengthen CON-0001 circulation legibility specification with quantified parameters from cognitive ergonomics: (a) maximum distance between wayfinding cues (derivable from uncertainty-decay model); (b) advance visual warning before decision points (glazed junctions per CON-0020 + sightline per CON-0018); (c) route complexity rating by population code. MODERATE confidence because the bioRxiv model …

**Disposition notes:** - [ ] MODERATE → P2 gap item

---

### CON-0039

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-02, A-08, A-13, all Category A items
**Target population(s):** DEAF, NDV/AUT, DEM, NEU/PCS
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Four independent evidence streams converge on RT60 ≤0.3 s as the specification ceiling for speech-critical rooms:

- **DEAF/hearing device users:** Iglehart 2020 (Tier 1 AJA), ANSI/ASA S12.60 Footnote e — 0.3 s for classrooms ≤283 m³. Speech perception scores significantly better at 0.3 s than 0.6 s for hearing aid/CI users.
- **NDV/AUT:** Bettarello 2021, Caniato 2024 (Tier 1) — existing standards calibrated to neurotypical populations are insufficient; sub-0.3 s indicated. Autistic users significantly more affected by modest background noise increases (52→55 dBA).
- **DEM:** Devos 2019 POE (Belgian nursing homes); Lyngby-Taarbæk case study (40% agitation reduction from acoustic ceiling ins…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Iglehart 2020 (AJA) | 1 | DEAF (hearing device users) | ALL — Universal Mode acoustic ceiling |
| ANSI/ASA S12.60-2010 Footnote e | 4 | DEAF | ALL |
| Bettarello et al. 2021 (Applied Sciences) | 1 | NDV/AUT | ALL |
| Caniato et al. 2024 | 1 | NDV/AUT | ALL |
| Devos et al. 2019 (PMC) | 2 | DEM | ALL |
| Murgia et al. 2023 (systematic review) | 1 | DEAF | ALL |

**Action required:** Elevate RT60 ≤0.3 s (mid-frequency average 500–2000 Hz) to Universal Mode universal specification for all speech-critical rooms. Frame 0.6 s explicitly as outer failure boundary, not compliant specification. Background noise ≤35 dBA; STI ≥0.60 at furthest listener position (BPC minimum; ≥0.75 for DEAF/CI per Iglehart 2020). Sound masking conflict with NDV/AUT documented separately in Part 7 §7.3.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing for all Category A items

---

### CON-0044

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** Part 1 (§1.4 theoretical framework), all G-items, C-04
**Target population(s):** ALL (theoretical); VIS, DBL, MOB (haptic continuity)
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** The `ecological-psychology-haptic-affordances-built-environment` BPC provides the most fundamental theoretical basis for the guidebook's specification logic: specifications are affordance thresholds — the point at which the environment switches from enabling to disabling action. This BPC is unreferenced in the connection register despite providing the meta-framework that unifies prospect-refuge (CON-0024), Lawton docility-proactivity (CON-0028), and Housing Enabler (CON-0027).

Two specific actionable findings:

1. **Misaffordance concept:** Environments signalling an action that doesn't exist. High-gloss floor appearing wet to DEM user = misaffordance. Glazed junction (CON-0020) creating re…

**Evidence basis:**
| Source | Tier | Framework | Application |
|---|---|---|---|
| Gibson 1979 (affordances) | Foundational | Affordance theory | Specification = affordance threshold |
| Heft 2001 (nested hierarchies) | Foundational | Environmental psychology | Wayfinding = affordance assemblage |
| Turvey & Carello 1995 (haptic) | Foundational | Haptic psychology | Handrail = haptic navigation structure |

**Action required:** Part 1 §1.4: cite ecological affordance framework as theoretical foundation. Specification = threshold at which affordance becomes available/unavailable. Misaffordance = actively harmful design (not just absence of accessibility). Haptic continuity: specify continuous handrail as Universal Mode on primary circulation routes — interruption at doors, corners, or landings is a haptic pathway break.

**Disposition notes:** - [ ] MODERATE → P2 gap item for theoretical framing
- [ ] HIGH → item-specification-writer briefing for G-item haptic continuity

---

### CON-0052

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-10, A-11, assistive-listening-systems, deafblind-built-environment-design
**Target population(s):** DEAF, DBL
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Hearing loop systems (IEC 60118-4) specified for DEAF populations serve DBL residual hearing users identically — not currently noted in DBL item specifications. DBL-specific guidance omits this provision despite documented DBL residual hearing prevalence (Edwards & Brentari 2020 per deafblind-built-environment-design BPC).

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| assistive-listening-systems BPC (IEC 60118-4) | 4 | DEAF | DBL residual hearing |
| deafblind-built-environment-design BPC (Edwards & Brentari 2020) | 2 | DBL | hearing loop applicability |

**Action required:** Add DBL as co-population for A-10/A-11 hearing loop items. Mechanism: residual hearing common in DBL; loop provision serves both DEAF and DBL without modification.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0055

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-09
**Target population(s):** NEU, PAIN, OFS, MOB
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Cushioned/resilient flooring serves three populations via different mechanisms: MOB (WBV reduction per floor-vibration-wheelchair-disability BPC), PAIN (joint impact reduction per GAP-B4-09), NEU (fall impact mitigation per neurological-built-environment BPC). Currently only MOB provision documented in guidebook; PAIN and NEU applications thin-evidenced but mechanistically supported.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| floor-vibration-wheelchair-disability BPC (Misch 2022) | 2 | MOB | cross-population mechanism |
| GAP-B4-09 (expert consensus) | 5 | PAIN | thin evidence flag |
| neurological-built-environment BPC | 3-4 | NEU | fall impact |

**Action required:** Extend A-09 resilient flooring to PAIN and NEU as co-populations. Flag PAIN application as thin-evidenced (expert consensus only); NEU fall-impact application supported by fall injury literature.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0056

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** threshold-and-level-access, residential-entry-and-threshold
**Target population(s):** OFS, PAIN, MOB
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Zero-threshold entry (13-15 mm max) specified for MOB wheelchair caster wheels serves OFS and PAIN populations via step-elimination mechanism — steps trigger post-exertional malaise (PEM) in OFS and joint loading pain in PAIN. Currently coded MOB-only; OFS/PAIN clinical rationale documented in respective BPCs but not cross-referenced to threshold items.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| threshold-and-level-access BPC | 4 | MOB | OFS, PAIN |
| pain-ofs-built-environment-design BPC | 3 | OFS, PAIN | threshold items |

**Action required:** Add OFS and PAIN as co-populations for all threshold items (E-12, E-13). Mechanism: step elimination prevents PEM/pain triggers; same physical provision serves three populations.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0059

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** B-06, B-07
**Target population(s):** DEM, NEU, MH, OFS
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Circadian lighting (≥250 melanopic EDI daytime) specified for DEM/NEU sleep-wake regulation serves MH and OFS populations via identical mechanism — circadian entrainment improves sleep outcomes across all four populations. MH and OFS BPCs document sleep disruption as core symptom but do not cross-reference circadian lighting specification.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| circadian-lighting-melanopic-edi BPC (Brown 2020) | 1 | DEM, NEU | MH, OFS |
| mental-health-built-environment BPC | 2 | MH | circadian lighting |
| pain-ofs-built-environment-design BPC | 3 | OFS | circadian lighting |

**Action required:** Add MH and OFS as co-populations for B-06/B-07 circadian lighting items. Mechanism: sleep-wake disruption common across DEM/NEU/MH/OFS; circadian lighting serves all four.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0065

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** NONE
**Target population(s):** OFS, PAIN, NEU
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Mandatory shade on outdoor circulation routes for OFS heat intolerance (pain-ofs-built-environment-design BPC) also serves PAIN (reduces inflammatory triggers) and NEU (prevents heat-exacerbated symptoms). No standard currently specifies outdoor shade provision; OT practice documents need but not architectural specification.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| pain-ofs-built-environment-design BPC | 3 | OFS | PAIN, NEU |
| ms-thermal-temperature-conflict-resolution BPC | 2 | NEU | outdoor shade |

**Action required:** Create new item: continuous shade on primary outdoor routes (natural or built) for OFS, PAIN, NEU thermal management. Evidence: heat intolerance documented across three populations.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0069

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** bariatric-turning-radius-built-environment, accessible-circulation-geometry
**Target population(s):** BAR, MOB
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Bariatric turning radius (≥1900 mm per bariatric-turning-radius-built-environment BPC) exceeds standard MOB turning space (1500-1525 mm per accessible-circulation-geometry BPC) by 375-400 mm. Single BAR user population requires larger dimension than all MOB specifications accommodate; currently documented as separate provision.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| bariatric-turning-radius-built-environment BPC (Steinfeld 2006) | 2 | BAR | MOB turning space revision |
| accessible-circulation-geometry BPC | 4 | MOB | BAR inadequacy |

**Action required:** Flag standard MOB turning space (1500-1525 mm) as inadequate for BAR populations. Specify 1900 mm where BAR provision required; 1800 mm minimum adaptation threshold.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0071

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** BIO-series
**Target population(s):** NDV, MH, DEM, NEU
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Biophilic outdoor/nature spaces documented independently in three BPCs: biophilic-design (NDV, reduces stress), mental-health-built-environment (MH trauma recovery), dementia-built-environment (DEM reduces agitation). All three cite nature exposure as therapeutic without cross-reference. Extends CON-0010 with NEU addition.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| biophilic-design-healthcare-workplace BPC (Ulrich 1984) | 1 | all | NDV, MH, DEM, NEU |
| mental-health-built-environment BPC | 2 | MH | biophilic cross-ref |
| dementia-built-environment BPC | 2 | DEM | biophilic cross-ref |

**Action required:** Consolidate biophilic/nature provisions as multi-population (NDV, MH, DEM, NEU). Create unified BIO-series items with population-specific mechanisms documented.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0073

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** NONE
**Target population(s):** OFS, NEU
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Thermal transition zone (vestibule cooling) at entrance for OFS heat intolerance (pain-ofs-built-environment-design BPC) also serves NEU/MS populations with Uhthoff's phenomenon (heat-exacerbated symptoms per ms-thermal-temperature-conflict-resolution BPC). No standard specifies entrance thermal transition; climate adaptation practice emerging.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| pain-ofs-built-environment-design BPC | 3 | OFS | NEU thermal transition |
| ms-thermal-temperature-conflict-resolution BPC | 2 | NEU | entrance vestibule |

**Action required:** Create new item: entrance thermal transition zone (vestibule with cooling) for OFS/NEU populations. Evidence: heat intolerance documented for both populations.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0074

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** deaf-spatial-design
**Target population(s):** DEAF, VIS, DEM, NDV/AUT
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** DEAF glazed corridor junctions (DeafSpace visual advance warning per deaf-spatial-design BPC) potentially conflict with VIS glare, DEM reflective surface confusion, and NDV visual noise. Spatial conflict documented in GAP-CON-0020 but resolution not specified. Requires matte glazing + strategic placement to serve DEAF without compromising other populations.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| deaf-spatial-design BPC (Gallaudet 2010) | 2 | DEAF | conflict resolution |
| dementia-built-environment BPC | 2 | DEM | glazing confusion |
| sensory-processing-model-design-application BPC | 3 | NDV | visual noise |

**Action required:** Specify matte/low-reflectance glazing at DEAF corridor junctions; position to avoid VIS glare paths. Zone-specific application where populations identified.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0075

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** NONE
**Target population(s):** NDV/AUT, VIS
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Sensory-responsive outdoor landscape (Finnigan 2024 SREF per GAP-CON-0025) for NDV populations overlaps with VIS tactile/auditory navigation landscape design. Outdoor spaces serve both populations through different sensory mechanisms — NDV sensory modulation + VIS non-visual wayfinding. Not currently cross-referenced.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| GAP-CON-0025 (Finnigan 2024) | 2 | NDV | VIS |
| visual-impairment-built-environment BPC | 2 | VIS | outdoor landscape |

**Action required:** Create outdoor landscape design guidance integrating NDV sensory-responsive elements + VIS tactile/auditory wayfinding. Evidence: both populations benefit from sensory-rich outdoor design.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0076

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-16, sensory-room-user-control
**Target population(s):** NDV/AUT, NEU, DEM
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Van Doorn et al. 2024 scoping review (GAP-CON-0026) finds mixed evidence for static sensory adaptive environments (SAEs) — individual control more important than fixed parameters. This principle extends from NDV/AUT to NEU/DEM populations: user-controlled sensory environment outperforms standardised design across all three populations.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| GAP-CON-0026 (Van Doorn 2024) | 2 | NDV/AUT | NEU, DEM |
| sensory-room-user-control BPC | 3 | NDV | NEU, DEM cross-ref |

**Action required:** Elevate user control principle to cross-population doctrine (NDV, NEU, DEM). Mechanism: individual sensory preferences vary within populations; control > fixed environment.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0081

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** B-10, visual-alerting-and-wayfinding-light
**Target population(s):** VIS, DEAF, DBL
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Visual alerting systems serve DEAF/VIS/DBL through different mechanisms: DEAF strobes for visual alert, VIS high-contrast wayfinding light, DBL vibrotactile + residual vision. Three populations require coordinated visual alerting strategy; currently specified separately without integration.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| visual-alerting-and-wayfinding-light BPC | 2 | VIS, DEAF, DBL | integrated strategy |
| assistive-listening-systems BPC | 4 | DEAF | DBL cross-ref |

**Action required:** Create integrated visual alerting specification serving DEAF/VIS/DBL. Coordinate VAD placement, contrast requirements, and vibrotactile supplementation.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0083

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-02, A-08, A-13
**Target population(s):** DEAF, VIS, DBL, NDV
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Non-English language evidence (DE DIN 18041, ZH, FR CEREMA per multilingual-evidence-convergence-non-english BPC) provides stronger acoustic specification for disability populations than English-language sources. Seven provisions have stronger empirical evidence in non-English literature; this language-based evidence gap affects DEAF, NDV acoustic items.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| multilingual-evidence-convergence-non-english BPC | 4 | all | acoustic items |

**Action required:** Flag English-language evidence limitation in acoustic items. Note stronger evidence base exists in DE/ZH/FR for DEAF/NDV provisions.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0086

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-16, Part 5 residential
**Target population(s):** NDV/MH, MH
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** First quasi-experimental TID study (Holtzinger et al. 2025, Social Sciences MDPI, 5 PSH sites, Colorado) found mixed results: TID sites improved relationship quality and self-awareness but decreased psychological safety scores; conflict and aggression increased over study period. Cautions against assuming TID features automatically improve outcomes without programme-level support. Relevant to guidebook MH provisions and A-16 sensory relief room specification.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Holtzinger et al. 2025 (Social Sciences, MDPI) | 1 | NDV/MH (homelessness) | MH item caveats |
| Owen & Crane 2022 (IJERPH scoping review) | 3 | NDV/MH | TID neuroscience lens |

**Action required:** Add TID evidence caveat to MH provisions: design features alone are necessary but insufficient; programme-level trauma-informed care must accompany physical design. First empirical evidence for this caution.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0087

**Status:** CONSUMED
**Confidence:** SPECULATIVE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-02, A-08, A-16
**Target population(s):** NDV/ADHD, NDV/SENS
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** First architectural design paper targeting misophonia (MDPI Architecture 2025) proposes spatial design as therapeutic approach for ADHD and misophonia. Identifies architectural spatial triggers (acoustic, visual) and proposes minimal design + VR/AR overlay as intervention. Misophonia not currently in guidebook population taxonomy; overlaps NDV/SENS and acoustic items. Evidence base extremely thin (conceptual paper, no empirical validation).

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| MDPI Architecture 2025 (misophonia/ADHD) | 5 | NDV/ADHD, NDV/SENS | acoustic items |

**Action required:** Flag misophonia as emerging NDV/SENS subpopulation for acoustic specification. Monitor for empirical evidence before adding to population taxonomy.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [x] SPECULATIVE → P3 gap item

---

### CON-0093

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** Ramp items (E-series)
**Target population(s):** MOB, PAIN
**Evidence tier:** —
**Filed:** 2026-04-02
**Applied:** —

**Connection:** The stair-ramp-threshold-biomechanics-accessibility BPC documents that ramp gradients above 1:12 force a high-force two-arm propulsion technique that increases long-term shoulder injury risk for manual wheelchair users (Waters et al. 1985, Tier 3; Kim et al. 2014). This is a pathway through which an inadequate ramp specification causes PAIN as a secondary condition in MOB populations.

The guidebook specifies ramps as MOB provisions. PAIN is currently not listed as a co-population for ramp items, despite the documented mechanism: repeated shoulder overload at grades >1:12 → rotator cuff injury → chronic shoulder PAIN. The 1:20 recommended gradient is not only about propulsion effort — it is …

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Waters et al. 1985 (shoulder injury, ramp gradient) | 3 | MOB | MOB, PAIN (shoulder PAIN prevention) |
| Kim et al. 2014 (ramp propulsion effort) | 3 | MOB | MOB, PAIN |
| stair-ramp-threshold-biomechanics-accessibility BPC | 2–4 | MOB | MOB, PAIN |

**Action required:** Add PAIN as co-population for ramp specifications. Frame 1:20 gradient as both ergonomic preference (MOB) and PAIN prevention (MOB users who develop shoulder pathology at inadequate gradients). Cross-reference pain-ofs-built-environment-design BPC.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing for ramp items

---

### CON-0094

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** Stair items, handrail items (G-series)
**Target population(s):** MOB, NEU, DEM, PAIN, VIS
**Evidence tier:** —
**Filed:** 2026-04-02
**Applied:** —

**Connection:** The stair-ramp-threshold-biomechanics-accessibility BPC documents that stair descent fall risk is 3× stair ascent risk (Simoneau et al. 1991, Tier 3), and that each 6 mm riser irregularity increases misstep probability by ~18% (Templer 1992, Tier 4).

These findings apply across MOB, NEU, DEM, PAIN, and VIS populations — each with different mechanisms, all resulting in elevated stair descent risk. Guidebook stair items are currently coded primarily for MOB and VIS. DEM, NEU, and PAIN are not systematically listed as co-populations despite documented fall risk.

The riser irregularity finding (6 mm = 18% misstep) is particularly relevant to DEM (spatial perception), NEU (proprioception), and …

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Simoneau et al. 1991 (3× descent vs ascent risk) | 3 | MOB | MOB, NEU, DEM, PAIN, VIS |
| Templer 1992 (6 mm irregularity = 18% misstep) | 4 | MOB | MOB, NEU, DEM, VIS |
| stair-ramp-threshold-biomechanics-accessibility BPC | 2–4 | MOB | ALL five populations |

**Action required:** Add NEU, DEM, PAIN, VIS as co-populations for stair descent and riser consistency specifications. Stair handrails (G-series): add same five populations. The 3× descent risk justification strengthens the case for handrail continuity on descent side.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing for stair and handrail items

---

### CON-0097

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** DAR items, visitability items, E-series (threshold), I-series (bathroom/shower)
**Target population(s):** MOB, OFS, PAIN (primary DAR populations)
**Evidence tier:** —
**Filed:** 2026-04-02
**Applied:** —

**Connection:** The ot-built-environment-interface BPC documents Wellecke et al. 2022 (Tier 1, n=144 Australian OTs): the three highest-priority OT-specified built environment features are (1) step-free external access, (2) zero-threshold shower, (3) ground-floor bedroom/bathroom.

These three exactly match the visitability/DAR minimum specification hierarchy documented in CON-0082 (adattabilità + visitability) and the residential-dar-provisions-priority-register BPC. CON-0082 derives the three priorities from regulatory precedent and universal design theory. Wellecke 2022 provides independent empirical confirmation from 144 OT practitioners — Tier 1 evidence for the priority ordering.

This is a significan…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Wellecke et al. 2022 (n=144 AU OTs, Tier 1) | 1 | MOB/ALL (AU residential) | CON-0082 visitability hierarchy |
| residential-dar-provisions-priority-register BPC | 4–5 | MOB/ALL | Confirmed priority order |
| ot-built-environment-interface BPC | 1–3 | OT practice | Visitability evidence anchor |

**Action required:** Add Wellecke 2022 as Tier 1 OT empirical evidence for visitability priority ordering in CON-0082 and DAR items. Reframe three visitability minimums as OT-empirically confirmed, not merely regulatory-derived. This strengthens the case for mandatory visitability provisions beyond code minimums.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing for DAR and visitability items

---

### CON-0100

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** Stair items, corridor/seating height items
**Target population(s):** MOB, NEU, DEM, PAIN, VIS, OFS
**Evidence tier:** —
**Filed:** 2026-04-02
**Applied:** —

**Connection:** The stair-ramp-threshold-biomechanics-accessibility BPC provides the biomechanical basis for seating height specification: 450–500 mm seat height reduces hip extensor moment by 40% compared to 380 mm (Rodosky et al. 1989, Tier 3). Reduced sit-to-stand capacity predicts falls in older adults (Lord et al. 1993). The 2 cm threshold defeats 45.8% of wheelchair users on first attempt (Al Lawati et al. 2017). Contrast sensitivity at 6 cycles/degree is reduced ~50% at age 70+ compared to young adults (Owsley et al. 2001).

Taken together, these biomechanical findings from a single BPC span MOB, NEU, DEM, PAIN, VIS, and OFS populations but were synthesised primarily for the MOB clinical context. Eac…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Rodosky et al. 1989 (seating height, hip moment) | 3 | MOB (older adults) | PAIN, OFS, DEM, NEU |
| Al Lawati et al. 2017 (2 cm threshold, 45.8% defeat) | 3 | MOB | MOB, PAIN, OFS, NEU |
| Owsley et al. 2001 (contrast sensitivity age 70+) | 3 | VIS | VIS, DEM, NEU |
| Lord et al. 1993 (sit-to-stand predicts falls) | 3 | MOB (older adults) | DEM, NEU, PAIN, OFS |
| stair-ramp-threshold-biomechanics-accessibility BPC | 2–4 | MOB | ALL affected populations |

**Action required:** Part 1 methodology: add explicit statement that dimensional specifications are biomechanically derived, not arbitrary — cite stair-ramp-threshold BPC as the primary evidence source for threshold (≤4–6 mm), ramp gradient (1:20), riser (≤175 mm), and seating height (450–500 mm) values. Each value corresponds to a documented functional threshold at which the environment switches from enabling to disa…

**Disposition notes:** - [x] HIGH → Part 1 methodology note + item-specification-writer briefing

---

### CON-0106

**Status:** CONSUMED
**Confidence:** MEDIUM
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** Part 5 §5.2, Part 3 §3.8/§3.9, all items referenced in conflict resolution table
**Target population(s):** ALL
**Evidence tier:** —
**Filed:** 2026-04-03
**Applied:** —

**Connection:** Part 5 §5.2 contains an 11-entry conflict resolution table. Each entry identifies a conflict domain, a resolution strategy, and a governing provision. Part 3 §3.8 provides the decision tree for selecting resolution strategies. Part 3 §3.9 provides the strategies menu (IEC/SZ/TS/DAR/SRW/PP/T0/OT-REF).

These two Parts were written by Sonnet independently. The CON register does not contain structural connections documenting:
1. That Part 5 §5.2 entries must be derivable from Part 3 §3.8 decision tree — applying §3.8 to each conflict should produce the resolution shown in §5.2.
2. That Part 3 §3.9 strategies must be exhaustive — every strategy code used in §5.2 must appear in §3.9.
3. That Part…

**Evidence basis:**
Internal structural consistency — no external evidence.

**Action required:** OP-G (Part 3 §3.8/3.9 methodology review) addresses this. No item specification change required. This CON entry documents the dependency for future maintenance: any change to Part 3 §3.8/3.9 must be verified against Part 5 §5.2, and vice versa.

**Disposition notes:** - [x] MEDIUM → RESOLVED via OP-G (Part 3 §3.8/3.9 methodology review, complete 2026-04-03). No item-specification-writer action required. Dependency documented for future maintenance.

---

### CON-0133

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** dementia-built-environment, neurodivergent-built-environment, intellectual-disability-built-environment-design, reach-range-and-accessible-controls
**Target item(s):** H-01, H-02, E-01 (door hardware)
**Target population(s):** DEM, NDV, IntD
**Evidence tier:** Tier 3-5 (DEM, NDV, IntD BPCs) + Tier 1-6 (controls BPC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** H-01/H-02 specify controls for MOB/UPL: reach range (400-1100mm), activation force (≤22.2N), lever hardware, no pinch/grip/twist. The controls BPC is entirely physical-access focused. Three populations have cognitive operability requirements undocumented in the controls specification:

**DEM:** Consistent placement (same switch position in every room); lever not rotary (rotary operation requires procedural memory); no multi-step sequences (each additional step loses ~30% of DEM users — inferred from CDM cognitive levels); colour contrast between control and wall (≥30% LRV per C-04).

**NDV:** Predictable, consistent response (no variable-speed dimmer behaviour); no ambiguous feedback states (a switch is either on or off — never "transitioning"); tactile confirmation of state; no audible click sounds >45 dBA (acoustic trigger).

**IntD:** Pictogram labels on all controls (light symbol, fan symbol, temperature symbol); single-action operation only; no combined controls (a switch that controls multiple circuits is cognitively inaccessible); placement at same height and same position in every room.

These are interface design requirements that the physical-access specification does not address. A DEM user who can reach a switch at 1000mm but cannot remember which switch does what, or an IntD user who can operate a lever but not interpret a three-way toggle, is functionally excluded by a specification that meets H-01.

**Evidence basis:** DEM BPC: consistent environment reduces confusion. NDV BPC: predictable, non-ambiguous interfaces. IntD BPC: pictogram + single-word signage; simplified interaction. Controls BPC: physical reach only; status PROVISIONAL; 16 jurisdictions NOT-RUN.

**Action required:** Add cognitive operability layer to H-01/H-02: (a) consistent placement across rooms (DEM, IntD); (b) single-action operation, no multi-step (DEM, IntD); (c) pictogram labelling (IntD); (d) unambiguous binary state (NDV); (e) colour contrast to wall ≥30% LRV (DEM, VIS). This is the highest-priority expansion for the controls-and-hardware topic — currently the thinnest in the coverage matrix (1 BPC, MOB only).

**Disposition notes:** — Fills the largest single topic gap in the coverage matrix.

---

---

### CON-0136

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** reach-range-and-accessible-controls, pain-ofs-built-environment-design, ofs-built-environment
**Target item(s):** E-01, H-01
**Target population(s):** OFS, PAIN
**Evidence tier:** Tier 1 (AAATE 2016 door force study) + Tier 5 (PAIN/OFS BPCs)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Door force specification (≤30N preferred, ≤38N maximum) is coded for MOB (wheelchair user arm strength). OFS and PAIN are not coded despite clear clinical rationale: OFS energy conservation — every door push depletes the post-exertional malaise budget; cumulative door-opening through a building visit can trigger PEM. PAIN — joint loading on hands, wrists, and shoulders during manual door operation aggravates arthritic and fibromyalgia pain.

The AAATE 2016 study (Tier 1, 94.7% WC user acceptance at ≤30N) provides the force threshold. The clinical extension: for OFS, the threshold applies not because of arm strength limitation but because of cumulative energy expenditure. For PAIN, because of joint-loading pain. The specification value (≤30N) remains unchanged; the population coding expands.

Additionally: automatic door openers (specified as "best practice" for entrance doors) should be elevated to MANDATORY for all doors on primary circulation routes where OFS/PAIN populations are primary users. The clinical rationale: eliminating door-opening exertion entirely is the energy conservation specification, not merely reducing force.

**Evidence basis:** Controls BPC: ≤30N door force (AAATE 2016 Tier 1). OFS BPC: energy conservation at all interaction points. PAIN BPC: joint loading reduction. The force threshold is already correct; the population rationale extends it.

**Action required:** (1) Add OFS and PAIN as co-populations for door force specification (E-01, H-01). (2) Elevate automatic door openers from "best practice" to "mandatory on primary circulation routes" where OFS/PAIN are primary users. (3) Mechanism note: OFS door force is energy-budget, not strength; PAIN door force is joint-loading, not strength. Same specification value, different clinical rationale.

**Disposition notes:** — Zero-cost connection (population tag expansion). Automatic door elevation has cost implications.

---

---

### CON-0156

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** FDR-CMP-08 compound interaction audit
**Target item(s):** E-03 (handrail), C-04 (nosing contrast), E-09 (TWSI), B-04 (stair lighting)
**Target population(s):** MOB, NEU (tremor), VIS
**Evidence tier:** Opus synthesis (FDR-NEW-15 + FDR-VI-02 + MOB stair evidence)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Triple compound MOB+NEU/tremor+VIS resolves at Tier 1 with zero antagonistic parameters. The 40–45mm handrail diameter range serves both tremor grip stability AND VIS tactile character readability. All stair provisions (continuous handrail, nosing contrast, TWSI, 300+ lux lighting, step regularity) are independently specifiable and convergent across all three populations. Critical finding: cumulative fall probability is MULTIPLICATIVE across the three risk factors — removing any single provision disproportionately increases compound fall risk. This reinforces Part 11 §11.5.2 value engineering argument for stair accessibility as an integrated system.

**Evidence basis:** FDR-CMP-08 audit (3 convergent, 2 independent, 1 conditional, 0 antagonistic). CAN/ASC 2.2 (handrail tactile characters). Parkinson's Foundation (tremor grip). BS 8300 stair provisions.

**Action required:** Add MOB+NEU+VIS stair compound note to Part 3 §3.10. Note multiplicative fall probability. Cross-ref Part 11 §11.5.2 (VE protection). Confirm 40–45mm handrail for triple compound.

**Disposition notes:** - [x] HIGH → Part 3 §3.10 compound convergence

---

---

## Connections CON-0131+ (Write-back from Opus batches, 2026-04-09)

### CON-0133

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** dementia-built-environment, neurodivergent-built-environment, intellectual-disability-built-environment-design, reach-range-and-accessible-controls
**Target item(s):** H-01, H-02, E-01 (door hardware)
**Target population(s):** DEM, NDV, IntD
**Evidence tier:** Tier 3-5 (DEM, NDV, IntD BPCs) + Tier 1-6 (controls BPC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** H-01/H-02 specify controls for MOB/UPL: reach range (400-1100mm), activation force (≤22.2N), lever hardware, no pinch/grip/twist. The controls BPC is entirely physical-access focused. Three populations have cognitive operability requirements undocumented in the controls specification:

**DEM:** Consistent placement (same switch position in every room); lever not rotary (rotary operation requires procedural memory); no multi-step sequences (each additional step loses ~30% of DEM users — inferred from CDM cognitive levels); colour contrast between control and wall (≥30% LRV per C-04).

**NDV:** Predictable, consistent response (no variable-speed dimmer behaviour); no ambiguous feedback states (a switch is either on or off — never "transitioning"); tactile confirmation of state; no audible click sounds >45 dBA (acoustic trigger).

**IntD:** Pictogram labels on all controls (light symbol, fan symbol, temperature symbol); single-action operation only; no combined controls (a switch that controls multiple circuits is cognitively inaccessible); placement at same height and same position in every room.

These are interface design requirements that the physical-access specification does not address. A DEM user who can reach a switch at 1000mm but cannot remember which switch does what, or an IntD user who can operate a lever but not interpret a three-way toggle, is functionally excluded by a specification that meets H-01.

**Evidence basis:** DEM BPC: consistent environment reduces confusion. NDV BPC: predictable, non-ambiguous interfaces. IntD BPC: pictogram + single-word signage; simplified interaction. Controls BPC: physical reach only; status PROVISIONAL; 16 jurisdictions NOT-RUN.

**Action required:** Add cognitive operability layer to H-01/H-02: (a) consistent placement across rooms (DEM, IntD); (b) single-action operation, no multi-step (DEM, IntD); (c) pictogram labelling (IntD); (d) unambiguous binary state (NDV); (e) colour contrast to wall ≥30% LRV (DEM, VIS). This is the highest-priority expansion for the controls-and-hardware topic — currently the thinnest in the coverage matrix (1 BPC, MOB only).

**Disposition notes:** — Fills the largest single topic gap in the coverage matrix.

### CON-0136

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** reach-range-and-accessible-controls, pain-ofs-built-environment-design, ofs-built-environment
**Target item(s):** E-01, H-01
**Target population(s):** OFS, PAIN
**Evidence tier:** Tier 1 (AAATE 2016 door force study) + Tier 5 (PAIN/OFS BPCs)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Door force specification (≤30N preferred, ≤38N maximum) is coded for MOB (wheelchair user arm strength). OFS and PAIN are not coded despite clear clinical rationale: OFS energy conservation — every door push depletes the post-exertional malaise budget; cumulative door-opening through a building visit can trigger PEM. PAIN — joint loading on hands, wrists, and shoulders during manual door operation aggravates arthritic and fibromyalgia pain.

The AAATE 2016 study (Tier 1, 94.7% WC user acceptance at ≤30N) provides the force threshold. The clinical extension: for OFS, the threshold applies not because of arm strength limitation but because of cumulative energy expenditure. For PAIN, because of joint-loading pain. The specification value (≤30N) remains unchanged; the population coding expands.

Additionally: automatic door openers (specified as "best practice" for entrance doors) should be elevated to MANDATORY for all doors on primary circulation routes where OFS/PAIN populations are primary users. The clinical rationale: eliminating door-opening exertion entirely is the energy conservation specification, not merely reducing force.

**Evidence basis:** Controls BPC: ≤30N door force (AAATE 2016 Tier 1). OFS BPC: energy conservation at all interaction points. PAIN BPC: joint loading reduction. The force threshold is already correct; the population rationale extends it.

**Action required:** (1) Add OFS and PAIN as co-populations for door force specification (E-01, H-01). (2) Elevate automatic door openers from "best practice" to "mandatory on primary circulation routes" where OFS/PAIN are primary users. (3) Mechanism note: OFS door force is energy-budget, not strength; PAIN door force is joint-loading, not strength. Same specification value, different clinical rationale.

**Disposition notes:** — Zero-cost connection (population tag expansion). Automatic door elevation has cost implications.

### CON-0152

**Status:** PENDING
**Target:** D-05, I-03
**Connection:** [DESCRIPTION PENDING]

### CON-0156

**Status:** PENDING
**Target:** E-03, C-04, E-09, B-04
**Connection:** [DESCRIPTION PENDING]

### CON-0165
*[formerly CON-0154]*

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** true
**Source BPC slug(s):** floor-vibration-wheelchair-disability, residential-kitchen-and-task-surfaces
**Target item(s):** A-09, kitchen/laundry flooring
**Target population(s):** MOB (wheelchair), VIS
**Evidence tier:** Tier 3 (Larivière 2024)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Floor type is the single largest WBV determinant for wheelchair users (Larivière 2024). Hard tile in kitchens/laundries transmits maximum WBV. Water-resistant resilient flooring (sheet vinyl with foam backing, sealed rubber) satisfies both water resistance AND WBV reduction. VIS: plain colour, low pattern.

**Action required:** Kitchen/laundry flooring specification: water-resistant resilient flooring in wheelchair-primary spaces. Hard tile contraindicated. Cross-reference A-09.


### CON-0181

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** floor-vibration-wheelchair-disability, chronic-pain-built-environment, ofs-built-environment
**Target item(s):** A-09 (floor surface spec)
**Target population(s):** MOB, PAIN, NEU, OFS
**Evidence tier:** 3
**Filed:** 2026-04-24
**Applied:** —

**Connection type:** CROSS-POPULATION
**Connection:** WBV evidence (Garcia-Mendez 2013, Koontz 2012, Chénier 2014 — all confirmed by citation-verifier) demonstrates wheelchair users exceed ISO 2631-1 health caution zones on common surfaces. Floor type is the single largest WBV determinant. This evidence is currently siloed in MOB/wheelchair BPC entries but applies directly to: PAIN (WBV increases spinal disorder risk in populations with pre-existing sensitised pain processing), NEU (tremor amplification from surface vibration), and OFS (vibration-induced fatigue compounds reduced activity tolerance in ME/CFS).

**Evidence basis:** Garcia-Mendez et al. 2013 (PMID:23820152); Koontz et al. 2012 (DOI:10.1123/jab.28.4.412); Chénier & Aissaoui 2014 (PMID:25276802). All verified T3.

**Action required:** Extend floor surface specification to include PAIN, NEU, OFS population tags. Add WBV risk note to chronic-pain and fatigue-spectrum slugs.

**Disposition notes:** —

---

## CON-0194

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** visual-impairment-built-environment, pain-ofs-built-environment-design
**Target item(s):** I-03, D-02, E-08
**Target population(s):** VIS, OFS
**Evidence tier:** 2-3
**Filed:** 2026-05-04
**Applied:** —

**Connection type:** COMPOUND-INTERACTION
**Connection:** VIS+OFS circulation compound (FDR-CMP-02): VIS navigation requires continuous cognitive processing. OFS fatigue reduces cognitive reserve with distance. Compound: cognitive resource for VIS navigation decreases as OFS fatigue accumulates. Rest seating for VIS+OFS must be tactile-indicated (cane-detectable) and recline-capable (venous pooling). Interval ≤20m (50% of OFS standalone, accounting for dual cognitive load).

**Evidence basis:** VIS BPC FDR; OFS BPC FDR; compound interaction audit methodology.

**Action required:** I-03: add VIS+OFS compound specification. D-02: note wayfinding cognitive load compounds with OFS fatigue. E-08: tactile-indicated rest alcove.

**Disposition notes:** —

---

## CON-0197

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** mobility-built-environment, neurological-built-environment
**Target item(s):** C-04, E-09
**Target population(s):** NEU/PD, VIS/DBL
**Evidence tier:** 2-3
**Filed:** 2026-05-04
**Applied:** —

**Connection type:** CROSS-ITEM
**Connection:** PD floor visual cue strips (FDR-MOB-01: 450mm, high-contrast, stride-length intervals) and TWSI directional guidance strips (ISO 23599: elongated bars) are both linear floor-mounted contrast elements on shared corridors. VIS cane user could confuse PD strips with TWSI. Differentiation: TWSI uses ISO 23599 raised profile ≥4mm; PD strips must be FLAT contrast bands (no raised profile) — visually effective for PD while cane-distinguishable from TWSI.

**Evidence basis:** FDR-MOB-01; ISO 23599:2012; VIS BPC TWSI specification.

**Action required:** C-04/E-09: add differentiation protocol. Part 5: corridor floor element coordination.

**Disposition notes:** —

---

## CON-0200

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** mobility-built-environment, pain-ofs-built-environment-design, deaf-spatial-design, neurological-built-environment
**Target item(s):** A-09, E-07, C-04, E-08
**Target population(s):** NEU/spasticity, PAIN, DEAF
**Evidence tier:** 2-3
**Filed:** 2026-05-04
**Applied:** —

**Connection type:** CROSS-POPULATION
**Connection:** Corridor floor is the most specification-overloaded element: 9+ simultaneous requirements, 3+ direct conflicts. NEU/spasticity FIRM non-compliant. PAIN CUSHIONED resilient. DEAF HARD for vibration. Plus PTV ≥36, plain (DEM), TWSI (VIS), PD strips, LRV contrast. Resolution: SPATIAL DIFFERENTIATION — primary path firm/non-compliant/PTV ≥36/plain; TWSI lane within; cushioned mat at rest points only; acoustic via ceiling+wall not floor. New 13th conflict domain: FLOOR-SPECIFICATION-SYSTEM.

**Evidence basis:** FDR-MOB-03; pain-ofs BPC; FDR-DEAF-02; compound audit; corridor analysis.

**Action required:** Part 3 §3.8: corridor floor as PRIMARY CONFLICT DOMAIN. A-09: zoned floor system. Part 5: 13th conflict domain.

**Disposition notes:** —

---

## CON-0205

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** visual-impairment-built-environment, dementia-built-environment, neurodivergent-built-environment
**Target item(s):** E-08, A-02
**Target population(s):** VIS, DEM, NDV
**Evidence tier:** 3
**Filed:** 2026-05-04
**Applied:** —

**Connection type:** CROSS-POPULATION
**Connection:** Long-cane detection gap: objects 300-2000mm AFF projecting into circulation are undetectable by cane sweep. No element should project above 300mm AFF without detectable base at ≤300mm AFF. Cross-population: DEM cognitive inattention + NDV inattentional blindness during hyperfocus also fail to detect overhead hazards. Base-detectability serves VIS + DEM + NDV without conflict.

**Evidence basis:** FDR-VI-01; AS 1428.1; DEM BPC; NDV BPC.

**Action required:** E-08: add overhead obstacle base-detectability specification. A-02: cross-reference for wall-mounted elements.

**Disposition notes:** —

---

## CON-0229

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** mobility-built-environment
**Target item(s):** A-02, A-07, A-09, E-07
**Target population(s):** MOB
**Evidence tier:** 1
**Filed:** 2026-05-04
**Applied:** —

**Connection type:** CROSS-ITEM
**Connection:** Sawatzky et al. 2015 (Tier 1, AJPMR): upper limb overuse is the PRIMARY health risk for manual wheelchair users. Environment must reduce propulsion effort. Existing connections cover ramp gradient and door force. But propulsion-reduction is BUILDING-WIDE: A-09 corridor surface friction (carpet vs hard — rolling resistance), A-02 corridor distance (shorter routes reduce cumulative shoulder load), A-07 cross-slope (any deviation increases unilateral shoulder load), E-07 threshold transitions (each bump is bilateral force spike). Currently specified for wheelchair ACCESS not INJURY PREVENTION. The specification framing changes: A-02 minimum corridor width is not 'can a wheelchair fit?' but 'does the corridor minimise propulsion effort over repeated daily use?' MOB BPC explicitly flagged Sawatzky as 'Not yet mined — deferred citation-miner.'

**Evidence basis:** Sawatzky et al. 2015 AJPMR (Tier 1); MOB BPC deferred flag.

**Action required:** A-02/A-07/A-09/E-07: reframe specifications from access to injury prevention. Add propulsion effort as specification rationale alongside dimensional access. Part 3: add wheelchair propulsion effort as building-level specification principle.

**Disposition notes:** —

---

## CON-0237

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** mobility-built-environment
**Target item(s):** A-02, A-07
**Target population(s):** MOB
**Evidence tier:** 3
**Filed:** 2026-05-04
**Applied:** —

**Connection type:** CROSS-ITEM
**Connection:** Koontz et al. 2012 (DOI:10.1123/jab.28.4.412): below 900mm corridor width, metabolic cost for manual wheelchair users increases 30-45% due to trunk lean and restricted stroke length. At 1200mm, metabolic cost normalises to open corridor conditions. This provides a quantified THRESHOLD for the propulsion-effort principle (CON-0229). Current A-02 specifications set minimum widths for ACCESS (can a wheelchair pass?) but not for METABOLIC EFFICIENCY (can a wheelchair propel without cumulative injury?). The 1200mm normalisation threshold should be the MINIMUM corridor width for primary wheelchair circulation routes — not 900mm (which is a passing-only dimension with 30-45% metabolic penalty). Distinct from existing Koontz citation in register (floor vibration WBV context) — this is the metabolic corridor width finding.

**Evidence basis:** Koontz et al. 2012 (DOI:10.1123/jab.28.4.412); MOB BPC corridor width section.

**Action required:** A-02: set 1200mm as minimum for primary wheelchair circulation (metabolic normalisation point). 900mm only for secondary/passing corridors with metabolic penalty note. A-07: cross-reference for cross-slope metabolic interaction.

**Disposition notes:** —
