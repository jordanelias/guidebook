# Connections — communication-and-alerts
<!-- CO-0006 Phase 0B-1 migration 2026-04-08 — from connection-register-active.md -->

### CON-0015

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** F-04, F-02
**Target population(s):** NDV, OFS, PAIN, MH
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Air quality / fragrance-free specifications carry OFS, NDV, NEU, PAIN. MH absent despite TID framework emphasis on environmental predictability and trigger avoidance. Chemical stimuli can trigger PTSD hyperarousal.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Steinemann 2018 | 3 | General | MH |
| TID framework | 2–3 | MH | MH (chemical triggers) |

**Action required:** Add MH as co-population for F-02/F-04.

**Disposition notes:** - [ ] MODERATE → P2 gap item

---

### CON-0043

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** All C-items, D-02, D-06, F-01 zone boundaries
**Target population(s):** VIS, DEM, NDV/AUT, IntD, DBL
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** The `luminance-contrast-lrv-evidence-base` BPC documents that the universal 30% LRV threshold has no empirical basis — it is a regulatory floor adopted from UK DDA guidance without validation. Severe VI needs ≥65% Michelson contrast (2.5× the standard). The guidebook recommends ≥50% LRV as best practice for C-items.

The inconsistency: the `detectable-gradient-protocol-sensory-zones` BPC specifies ≥30 LRV change at zone boundaries — inheriting the unvalidated threshold. Cognitive wayfinding items depend on contrast-based landmarks for DEM, IntD, NDV. The guidebook's own ≥50% best-practice target is not propagated to zone boundaries or wayfinding items.

**Evidence basis:**
| Source | Tier | Currently cited for | Gap |
|---|---|---|---|
| Harper et al. 2022 (Ergonomics) | 3 | Stair contrast enhancement | Supports enhancement; doesn't validate 30% |
| Brown et al. 2023 (Ergonomics) | 3 | VIS nosing contrast | Confirms benefit; no threshold validation |
| Dain et al. (cited in Manandhar 2022) | 3 | Severe VI | ≥65% Michelson needed; 2.5× current standard |
| CNIB 2024 | Co-1 | VIS | 30% is minimum regulatory floor, not functional optimum |

**Action required:** Apply ≥50% LRV best-practice target consistently to all contrast-dependent provisions — C-items, zone boundaries, wayfinding items. At critical junctions (platform edges, stair nosings, kerb lines): ≥65% Michelson. The 30% value remains as code-compliance minimum only. Internal consistency correction — the guidebook already established the right position in the LRV BPC.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing for all C-items + F-01 zone boundaries

---

### CON-0063

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** F-02, F-04
**Target population(s):** NDV, OFS, PAIN, MH
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Fragrance-free policy + MERV 13+ filtration (F-02, F-04) specified for OFS/MCAS and NDV chemical sensitivity serves MH/PTSD populations via identical mechanism — chemical stimuli as trauma triggers. Trauma-informed design framework (mental-health-built-environment BPC) emphasises environmental predictability but does not cross-reference air quality specifications.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| air-quality-voc-chemical-sensitivity-built-environment BPC | 3 | OFS, NDV | MH |
| mental-health-built-environment BPC | 2 | MH | F-02, F-04 cross-ref |

**Action required:** Add MH as co-population for F-02/F-04 air quality items. Mechanism: chemical stimuli reduction serves OFS/NDV physiological + MH trauma-trigger avoidance.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0101

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** F-07, F-08, A-01, A-02, A-08
**Target population(s):** NEU/MS, OFS, PAIN, NDV/AUT, DEAF
**Evidence tier:** —
**Filed:** 2026-04-03
**Applied:** —

**Connection:** F-07 (Thermal Zoning) and F-08 (Thermal Transition) specify HVAC system requirements including forced air prohibition in NEU/OFS spaces and high-performance envelope. The ms-thermal BPC states "no forced air heating as sole source in NEU/OFS spaces (acoustic + airborne trigger concern)." This acoustic rationale is not cross-referenced in Category A acoustic items.

Conversely, A-08 specifies NC-25 background noise. HVAC system type is the primary determinant of achievable NC level. F-07/F-08 HVAC zoning strategy directly constrains which heating systems can meet A-08 NC-25. This bidirectional dependency is not documented.

Additionally, F-08 thermal mass specification (≤3°C diurnal swing) vi…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| ms-thermal BPC (forced air prohibition) | 4 | NEU/MS, OFS | A-01, A-02 acoustic cross-ref |
| room-acoustic-performance BPC | 3–4 | DEAF, NDV | F-07/F-08 HVAC cross-ref |
| CIBSE Guide A (HVAC noise) | 5 | General | F-07 acoustic constraint |

**Action required:** Add cross-reference in F-07 and F-08: "HVAC system selection must achieve NC-25 per A-08; forced air systems are contraindicated for NEU/OFS spaces per ms-thermal BPC." Add reciprocal note in A-08: "Background noise target constrains HVAC system type — coordinate with F-07 thermal zoning strategy." Add note in A-02: "Where F-08 specifies exposed thermal mass (concrete ceiling), additional acoustic…

**Disposition notes:** - [x] HIGH → APPLIED 2026-04-03: cross-refs added to A-08 (HVAC type constraint, NC-25/forced-air coordination, exposed thermal mass note) and F-07 (CON-0101 coordination note). F-08 thermal mass note included in F-07 addition. A-02 note added via CON-0101 cross-ref in A-08.

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

### CON-0108

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** F-08, E-01, E-06, E-13, E-14
**Target population(s):** OFS, NEU/MS, MOB, VIS, DEM
**Evidence tier:** —
**Filed:** 2026-04-03
**Applied:** —

**Connection:** F-08 specifies an entry vestibule (thermal buffer ≥2 m depth) at primary accessible entrances. E-01 (Entrance Door), E-06 (Level Entry), E-13 (PIR Entrance Lighting), and E-14 (Entrance Rest Seating) all specify provisions at the same spatial location — the building entrance.

The vestibule adds a second door transition (outer + inner) which:
1. Doubles the E-01 door specification scope — both vestibule doors must meet E-01 accessible door specification.
2. Creates a transition zone where E-13 lighting must maintain illuminance continuity (no dark zone between outer and inner doors).
3. Places E-14 entrance rest seating within or immediately after the thermal buffer zone — the seating benefi…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| CON-0068 (thermal transition) | Internal | OFS, NEU | E-series coordination |
| pain-ofs-built-environment-design BPC | 3 | OFS | Vestibule spatial requirements |

**Action required:** Add note to F-08 vestibule specification: "Both vestibule doors to meet E-01 specification. Level entry (E-06) at both thresholds. Lighting (E-13) continuous through vestibule — no dark transition zone. Where E-14 entrance rest seating is specified, locate within or immediately after vestibule." Add reciprocal note in E-01: "Where F-08 thermal vestibule is specified, accessible door specification …

**Disposition notes:** - [x] MEDIUM → APPLIED 2026-04-03: F-08 Retrofit section updated with E-series coordination note (both vestibule doors E-01; level entry E-06 both thresholds; E-13 lighting continuity; E-14 seating within vestibule). E-01 cross-ref updated with F-08 vestibule reciprocal note. E-06/E-13/E-14 coordination embedded in F-08 note — separate item edits deferred to Phase 5 cross-reference-resolver pass.

---
