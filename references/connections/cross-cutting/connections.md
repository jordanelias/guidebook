# Connections — cross-cutting
<!-- CO-0006 Phase 0B-1 migration 2026-04-08 — from connection-register-active.md -->

### CON-0017

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** H-02 (Individual Environmental Control), A-16, B-06, B-07
**Target population(s):** NDV/AUT, NDV/MH, OFS, DEM, NEU, DEAF, VIS
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** "User control over environment" is documented as the single highest-impact provision across NDV subtypes (NDV BPC), the primary design requirement for sensory rooms (sensory-room-user-control BPC), a core requirement for NDV/MH retreat rooms, and essential for OFS temperature/lighting management. DEM benefits from consistent but adjustable environments. DEAF users benefit from lighting control for sign language visibility. The pattern repeats in 5+ population BPCs but is never synthesized into a cross-population design principle. No specification currently states that occupant environmental control is a Tier 0 universal provision. It is siloed as population-specific within each category. Thi…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| NDV BPC — "single highest-impact provision" | Co-1, Tier 4 | NDV/AUT, NDV/ADHD, NDV/SENS | ALL — Tier 0 candidate |
| Sensory room user control BPC — H-02 PRIMARY | Co-1 | NDV/AUT | ALL |
| OFS BPC — adjustable seating/temperature/lighting | Co-1/Tier 3 | OFS | ALL |
| NDV/MH BPC — user-adjustable lighting/acoustics | Tier 2–4 | NDV/MH | ALL |
| PAS 6463:2022 | Tier 5 | NDV, DEM | ALL |
| DeafSpace — lighting control for signing | Co-1/Tier 2 | DEAF | ALL |

**Action required:** Elevate H-02 (Individual Environmental Control) to Tier 0 universal design. Specification: all primary occupied spaces to provide occupant-adjustable lighting (level and CCT), acoustic management (operable panels or zones), and local thermal control. Population-specific overlays at Tier 1 define parameter ranges. This does not increase cost significantly — dimmer switches and local thermostats are…

**Disposition notes:** - [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED

---

### CON-0040

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-02, A-08, A-13, B-01, B-06, F-01, D-05, A-16
**Target population(s):** NDV/AUT, NDV/ADHD, NDV/SENS, DEM, NEU, DEAF, OFS, PAIN, VIS
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Four unreferenced BPC slugs describe four facets of a single sensory environment design system with no internal cross-references:

1. **`sensory-processing-model-design-application`** — Dunn's four sensory profiles → design requirement matrix
2. **`detectable-gradient-protocol-sensory-zones`** — Three spatial zones → boundary thresholds (≥0.2 s RT60 change, ≥50 lux, ≥30 LRV)
3. **`room-acoustic-performance`** — RT60/NC targets per population
4. **`therapeutic-lighting-design`** — Melanopic EDI/CCT targets per time of day

The unmade synthesis is the within-zone parameter assignment:

| Parameter | Zone 1 (High activation) | Zone 2 (Moderate) | Zone 3 (Low activation) |
|---|---|---|---|
| RT…

**Evidence basis:**
| Source | Tier | Slug | Proposed extension to |
|---|---|---|---|
| Dunn 1997 sensory model | Foundational | sensory-processing-model | Zone assignment framework |
| PAS 6463:2022 §6.4 | 5 | detectable-gradient-protocol | Zone boundary thresholds |
| Mostafa ASPECTSS 2.0 (2021) | 2 | detectable-gradient-protocol | Zone transition design |
| Iglehart 2020 / Murgia 2023 | 1 | room-acoustic-performance | Zone 3 RT60 target |
| Brown et al. 2022 / WELL v2 | 3/5 | therapeutic-lighting-design | Zone 1–3 CCT/EML targets |

**Action required:** Create unified sensory environment specification matrix linking Dunn's profiles to spatial zones to quantified parameters. Mark as ○ (expert synthesis) — zone boundaries empirically grounded, within-zone targets synthesised from population-specific evidence. No single study validates the complete matrix.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing for F-01, A-16, B-01, B-06, all Category A

---

### CON-0046

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-16, F-01, D-05, CON-0019 items
**Target population(s):** NDV/AUT, NDV/MH
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** CS-17 (NHS CAMHS inpatient review, NDTi/NHS England 2022) documents systematic harm: NHS inpatient mental health wards designed for NDV/MH are actively harmful to co-occurring NDV/AUT patients. Sensory environments "present sometimes extreme challenges" and "at best hinder wellbeing, at worst exacerbate mental health problems; instigate cycle of progression to more restrictive settings."

This is the only case study documenting design-caused escalation of disability — not failure to accommodate, but active worsening. The absence of sensory zoning (CON-0040 three-zone model) and environmental refuge (CON-0019) is the proximate cause. The sensory zoning system is not an optional enhancement — …

**Evidence basis:**
| Source | Tier | Finding |
|---|---|---|
| NDTi / NHS England 2022 (Tandfonline DOI 10.1080/13575279.2022.2126437) | 1 (Co-1 autistic-led, peer-reviewed) | Systematic sensory design failure for NDV/AUT in NDV/MH wards |
| PAS 6463:2022 | 5 | Sensory zoning as design principle — not implemented in NHS wards |
| CON-0019 (environmental refuge) | Internal | Refuge provision would mitigate harm |
| CON-0040 (sensory zone system) | Internal | Three-zone model prevents one-size-fits-all ward design |

**Action required:** Part 7/8: document as mandatory provision — Zone 3 + environmental refuge specified as required (not recommended) in healthcare, education, and any building type where NDV/AUT + NDV/MH co-occurrence is foreseeable. Shifts zone provision from best practice to harm prevention mandate. Reference NHS CAMHS as paradigm failure case in Part 13.

**Disposition notes:** - [ ] HIGH → Part 7/8 mandatory zoning + Part 13 failure case

---

### CON-0080

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** All room matrices
**Target population(s):** DBL, IntD
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** DBL and IntD populations absent from 15/16 room matrices (GAP-S4 series) despite documented requirements in respective BPCs. Both populations require provisions not currently specified: DBL tactile navigation consistency, IntD cognitive load reduction. Room matrix gap items document systematic omission across residential and non-residential typologies.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| deafblind-built-environment-design BPC | 4-5 | DBL | all room matrices |
| intellectual-disability-built-environment-design BPC | 4-5 | IntD | all room matrices |
| GAP-S4-series | — | DBL, IntD | room specifications |

**Action required:** Systematically add DBL and IntD provisions to all room matrices. DBL: tactile consistency, haptic communication space. IntD: visual simplicity, intuitive layout, pictogram signage.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0104

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** H-05, K-04, B-10, H-04
**Target population(s):** DBL, DEAF, MOB, DEM, OFS, PAIN
**Evidence tier:** —
**Filed:** 2026-04-03
**Applied:** —

**Connection:** H-05 (Nurse Call) specifies multi-modal alerting (audio, visual, tactile) but does not explicitly reference K-04 (Vibrotactile Alert) as the DBL-accessible modality. The deafblind BPC specifies vibrotactile alerting for all alarm/communication systems. H-05's "tactile feedback" specification refers to button confirmation — not to vibrotactile alerting of incoming calls to DBL occupants.

For a DBL occupant in a care environment: the nurse call system is their only emergency communication channel. Without vibrotactile integration, a DBL occupant cannot detect incoming nurse visits, call confirmations, or emergency notifications.

H-05 already cross-references B-10 (fire alarm integration) and…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| deafblind-built-environment-design BPC | 4–5 | DBL | H-05 K-04 integration |
| DbI best practice guidelines | Tier 2 | DBL | H-05 vibrotactile channel |
| visual-fire-alarm-seizure-safety BPC | 3–4 | NEU | Multi-channel alerting |

**Action required:** Add to H-05 cross-reference: "K-04 (Vibrotactile Alert — in DBL-designated care environments, nurse call activation must trigger vibrotactile alerting device (wearable pager or bed shaker) for DBL occupants; audio and visual channels alone are insufficient for this population)." Add DBL to H-05 Applicable Groups. Add reciprocal note in K-04: "K-04 vibrotactile devices must integrate with H-05 nurs…

**Disposition notes:** - [x] HIGH → APPLIED 2026-04-03: DBL added to H-05 Applicable Groups. H-05 cross-ref updated with K-04 vibrotactile integration note (life-safety specification for DBL). K-04 cross-ref updated with H-05 reciprocal note.

---

### CON-0137

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** mental-health-built-environment
**Target item(s):** Part 7 NR-HLT (healthcare matrices)
**Target population(s):** NDV/MH
**Evidence tier:** Tier 1 (Weltens 2023)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** The MH BPC documents that exceeding bed capacity in psychiatric wards produces OR 5.36 for aggression (Weltens 2023, experience sampling method). This is a built-environment capacity specification: the number of beds per ward is a design parameter with a direct, large, quantified effect on safety outcomes. The OR is among the largest in the MH BPC evidence base — comparable to the absence of private space (van der Schaaf 2013).

No Part 7 NR-HLT specification currently addresses maximum bed count per ward as an accessibility parameter. Ward capacity is treated as a programming decision, not a design specification. The evidence says otherwise: over-capacity is an environmental barrier with measurable harm.

Additionally, the MH BPC identifies that ward-level environmental factors (capacity, private space, sensory modulation availability) govern coercive measure use MORE than patient-level factors or staffing. This inverts the typical clinical assumption that patient behaviour drives restraint use.

**Evidence basis:** MH BPC: Weltens 2023 (ESM, OR 5.36 for aggression when capacity exceeded). van der Schaaf 2013 (n=23,868 — ward design variables > staffing variables for coercion). Husum 2010 (n=1,016 — ward-level variation in coercion not explained by patient characteristics).

**Action required:** Part 7 NR-HLT: add maximum bed capacity specification for psychiatric wards as an environmental design parameter. Bed count is not merely a planning metric — it is a safety specification with OR 5.36 evidence. Cross-reference: private space per patient (van der Schaaf 2013), sensory modulation room (Faerden 2022 d=2.0). These three provisions (capacity limit, private space, sensory modulation) are the MH environmental intervention triad.

**Disposition notes:** — Novel specification type: occupancy capacity as environmental design parameter. May face pushback from facility managers; evidence is strong.

---

---

### CON-0139

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** methodology-evidence-hierarchy-mapping (Phase 1A), mental-health-built-environment
**Target item(s):** Part 1 §1.5
**Target population(s):** ALL
**Evidence tier:** Tier 1
**Filed:** 2026-04-09

**Connection:** Phase 1A §7.4 states the ● / ○ system does not further stratify within ●. But the MH BPC contains Faerden 2022 (d=2.0), CAPABLE (RCT, hospitalisation halved), and Clemson Cochrane (38% fall reduction) — all ●, but the effect sizes differ by an order of magnitude. Part 1 should cite the d=2.0 as the upper anchor of ● evidence, demonstrating the range within the marker. This strengthens the methodology transparency commitment (Phase 1A §10.2) without changing the ● / ○ system.

**Action required:** Part 1 §1.5.3: add "effect size exemplars" footnote — d=2.0 (MH user control), 38% fall reduction (grab bars), OR 9.50 (wheelchair turning space) as concrete illustrations of what ● encompasses.

---

---

### CON-0147

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** true
**Source BPC slug(s):** intellectual-disability-built-environment-design, pain-ofs-built-environment-design
**Target item(s):** Part 7 NR-EDU, NR-HLT
**Target population(s):** IntD, OFS

**Connection:** IntD BPC: "reception/assistance point within sight of entrance" (CSA B651 §4.7). OFS BPC: "rest seating within 25–30m." In a healthcare or education building serving both populations, the entrance sequence must provide BOTH: visible assistance AND immediate rest. These are complementary, not competing: a reception desk with adjacent seated waiting serves both requirements simultaneously. But no specification links them.

**Action required:** Part 7 NR-HLT/NR-EDU entrance sequence: reception/assistance visible from entry (IntD) WITH adjacent seated waiting ≤3m from entrance (OFS/PAIN). Single spatial provision serves both. Low-cost coordination.

---

### CON-0102

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** F-07, F-08, F-04, F-06
**Target population(s):** OFS/MCAS, NDV (chemical sensitivity), PAIN
**Evidence tier:** —
**Filed:** 2026-04-03
**Applied:** —

**Connection:** F-07 (Thermal Zoning) specifies individual supplemental radiant heating. F-04 (Air Quality) specifies MERV 13+ filtration and no recirculated air without HEPA for OFS/MCAS spaces. F-06 (Fragrance-Free Policy) prohibits fragrance diffusers including HVAC-integrated systems.

These three F-category items are interdependent but specified independently:
1. F-07's radiant heating recommendation avoids forced air — but does not cross-reference F-04's reason (airborne chemical triggers for MCAS) or F-06's prohibition (no HVAC-integrated fragrance systems).
2. F-04 specifies fresh air supply ≥15 L/s per person in OFS/MCAS spaces — but does not reference F-07's ambient ≤18°C constraint (which affects…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| air-quality-voc BPC | 4–5 | OFS/MCAS | F-07 HVAC type constraint |
| ms-thermal BPC | 2–4 | NEU/MS | F-04 ventilation heat recovery |
| pain-ofs-built-environment-design BPC | 3 | OFS | F-category coordination note |

**Action required:** Create F-category coherence note in Part 4 preamble to Category F: "F-04 (Air Quality), F-06 (Fragrance-Free Policy), F-07 (Thermal Zoning), and F-08 (Thermal Transition) are interdependent specifications governing the same building system. For OFS/MCAS populations, HVAC design must simultaneously satisfy: (a) ambient ≤18°C (F-07); (b) MERV 13+ filtration, ≥15 L/s fresh air, no recirculated air wi…

**Disposition notes:** - [ ] HIGH → Category F preamble + item-specification-writer briefing for F-04, F-06, F-07, F-08 [DEFERRED — Category F preamble requires separate Part 4 category-level edit; individual item notes for F-04, F-07 applied via FDR-OFS-03 and CON-0101 passes. Full preamble to be written in Phase 5 assembly pass.]

---

---

### CON-0157

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** FDR-CMP-07
**Target item(s):** B-10, H-03, D-08, E-08
**Target population(s):** DEAF, DEM
**Evidence tier:** Opus synthesis
**Filed:** 2026-04-09
**Applied:** ---

**Connection:** DEAF+DEM compound resolves at Tier 1 (0 antagonistic). Two-layer information design: simple pictogram for DEM + detailed text for DEAF. Alarm comprehension gap is procedural (Part 9 staffing), not environmental.

**Action required:** Part 3 3.10 compound guidance. Two-layer information design principle.

---
