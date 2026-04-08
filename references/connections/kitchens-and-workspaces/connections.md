# Connections — kitchens-and-workspaces
<!-- CO-0006 Phase 0B-1 migration 2026-04-08 — from connection-register-active.md -->

### CON-0002

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** A-16, H-02
**Target population(s):** NDV, MH, OFS, PAIN
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** sensory-relief-space-design BPC (NDV primary) and mental-health-built-environment BPC (MH primary) specify substantially overlapping rooms — both require user-controlled lighting (2700–6500 K), acoustic treatment (RT60 ≤0.3 s), safe retreat, ≥8–9 m². OFS BPC requires reclined posture rest spaces. PAIN BPC requires seated/recumbent provision. Amaze/Architecture & Access (2025) explicitly extends A-16 to ADHD/OFS/PAIN comorbidities and trauma.

Currently A-16 is NDV-only. MH "de-escalation room" described as distinct. Evidence does not support two separate room types — supports single multi-population sensory relief / safe retreat spec with population-specific configuration notes.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Unwin, Powell & Jones 2022/2023 | 3 | NDV/AUT | NDV, MH, OFS, PAIN |
| Architecture & Access / Amaze 2025 | 3/5 | NDV (extends to OFS/PAIN) | NDV, MH, OFS, PAIN |
| PAS 6463:2022 | 5 | NDV | NDV, MH |
| CDC ME/CFS guidelines | Co-1 | OFS | OFS, PAIN |

**Action required:** Expand A-16 to carry NDV, MH, OFS, PAIN as co-primary populations. Retire separate MH "de-escalation room" concept. Add OFS reclined seating and PAIN cushioned seating within A-16. Elevate H-02 to primary cross-reference (per GAP-SRS-01). Collapses three separate specs into one.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing

---

### CON-0013

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** Kitchen items
**Target population(s):** MOB, OFS, PAIN, LPA
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Kitchen height-adjustable worktop (650–900mm) specified for MOB. OFS and PAIN not listed despite requiring seated work provision (energy conservation; joint-loading reduction).

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| ADA / NL WMO-keuken | 5–6 | MOB | MOB, OFS, PAIN |
| Kos et al. 2015 | 1 | OFS (behavioural) | OFS (architectural) |

**Action required:** Add OFS and PAIN as co-populations for kitchen adjustable worktop. Partially resolves GAP-B4-07.

**Disposition notes:** - [ ] MODERATE → P2 gap item

---

### CON-0041

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** F-06, Part 9 §9.1.4 (envelope+mass), F-07, H-04, all residential bathroom matrix entries
**Target population(s):** DEM, MOB (older adults), NEU/MS, PAIN, OFS
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Japan heat shock data (6,073 bathtub drowning deaths/year, MHLW 2023) is the most consequential mortality statistic in the BPC corpus. Root cause: 5–15°C differential between unheated bathrooms and heated living areas. Resolution: inter-room differential ≤5–7°C (Nakayama 1981).

This finding is siloed in `thermal-comfort-older-adults-care-settings` and not propagated to:
- Part 5 residential bathroom matrices (where it is a P1 safety specification)
- F-06/Part 9 §9.1.4 items (which specify envelope performance but not inter-room differential)
- The `ms-thermal-temperature-conflict-resolution` BPC (which addresses population thermal preference conflicts but not the mortality mechanism)
- CON-…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| MHLW Japan 2023 (6,073 deaths) | 3 | DEM/older adults (JP) | ALL residential bathroom specification |
| Nakayama 1981 (≤5–7°C differential) | 3 | DEM/older adults (JP) | ALL residential inter-room thermal spec |
| Baquero et al. 2023 (n=1,065) | 3 | DEM/older adults | Thermal comfort targets |
| ms-thermal BPC (Uhthoff/PAIN/OFS conflict) | 2–4 | NEU/MS, PAIN, OFS | Resolution methodology |
| F-07 (heated bathroom floor, formerly TC-05) | 5 | ALL | Direct prevention of heat shock mechanism |

**Action required:** Propagate inter-room thermal differential ≤5°C to all residential bathroom matrix entries as P1 safety specification. Cross-reference F-07 (heated bathroom floor, formerly TC-05) as the primary prevention mechanism. Link to ms-thermal conflict resolution for multi-condition thermal management. Specify refuge room thermal zone assignment (individual control required).

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing for Part 5 bathroom matrices + F-06/F-07 items

---

### CON-0042

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** B-10, visual alerting items, H-04, CON-0014 items
**Target population(s):** DEAF, DBL, NEU (seizure), NDV/AUT (photosensitive)
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** CON-0014 proposes vibrotactile alerting for sleeping areas where DEAF/DBL and photosensitive populations co-occur. The `visual-fire-alarm-seizure-safety` BPC specifies synchronised VADs at 0.5–1 Hz + voice alarm + vibrotactile. The `visual-alerting-and-wayfinding-light` BPC covers non-emergency alerting (doorbells, call systems).

The unmade synthesis: the alerting system is a single integrated domain. A person who needs vibrotactile fire alerts also needs vibrotactile doorbell, telephone, and intruder alerts. Specifying vibrotactile for fire only leaves the same person without notification for all other alert types.

The seizure/photosensitivity conflict applies to all visual alerting, not …

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Jordan & Vanderheiden 2024 (ACM TACCESS) | 3 | NEU (photosensitive epilepsy) | All visual alerting items |
| BS EN 54-23:2010 | 5 | DEAF (fire VAD) | Multi-channel specification |
| NFPA 72-2022 | 5 | DEAF | Multi-channel specification |
| RNID / HLAA / Bufdir | Co-1/2 | DEAF (vibrotactile) | All alerting channels |

**Action required:** Specify unified multi-channel alerting: every alert event (fire, intrusion, doorbell, telephone, intercom) available through all three channels (visual + auditory + vibrotactile) simultaneously. Consistent channel specifications across alert types to enable pattern recognition. Extends CON-0014 from sleeping-area fire alarm to all alerting.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing for B-10 + all alerting items

---

### CON-0070

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** H-01, reach-range-and-accessible-controls
**Target population(s):** CHD, LPA, MOB
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Children's reach range (lower than adult wheelchair users per body-sizes-supplementary-populations BPC) overlaps with LPA and seated adult reach zones. Controls at 400-600 mm serve CHD standing + LPA/MOB seated; single height band serves three populations. Not currently cross-referenced.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| body-sizes-supplementary-populations BPC | 3 | CHD, LPA | MOB reach overlap |
| reach-range-and-accessible-controls BPC | 4 | MOB, LPA | CHD cross-ref |

**Action required:** Note 400-600 mm control zone serves CHD, LPA, and seated MOB populations. Mechanism: lower reach range common across three populations for different anthropometric reasons.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0109

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** H-02, H-04, Part 10 DAR provisions
**Target population(s):** MOB, NEU, VIS, DEAF, DEM, OFS, PAIN, ALL
**Evidence tier:** —
**Filed:** 2026-04-08
**Applied:** —

**Connection:** Two 2025 OT studies demonstrate mainstream smart home technology (smart speakers, home automation) delivered through structured OT-led service delivery as formal assistive technology. Ding et al. (JMIR Rehabil Assist Technol 12:e70855, 2025) developed the ASSIST intervention: OT assessment → technology recommendation → installation → training. Significant functional independence gains (p<.001) at ~$5000 per client. Mun (AJOT 79(5):7905205190, 2025) confirmed OT-led smart home solutions improve occupational performance, quality of life, and psychosocial impact across physical disability populations. Lee et al. (Disability & Rehab AT, 2025) identified population-differentiated adoption barrier…

**Evidence basis:**
| Source | Tier | Current citation context | Proposed extension |
|---|---|---|---|
| Ding et al. 2025 (JMIR Rehabil Assist Technol 12:e70855) | 1 | Not cited | H-02, Part 10 DAR — OT-led MSHT intervention model |
| Mun 2025 (AJOT 79(5):7905205190) | 1 | Not cited | H-02, Part 10 DAR — smart home as formal AT |
| Lee et al. 2025 (Disability & Rehab AT) | 2 | Not cited | Part 9 §9.5 — population-differentiated technology prescription |

**Action required:** Create DAR provision for smart-home-ready infrastructure: (1) conduit from distribution board to all primary occupied rooms, (2) Wi-Fi AP position at ceiling level in circulation hub, (3) power outlet at smart speaker mounting height (1200 mm AFF) in kitchen, bedroom, living room, (4) structured cabling to entrance intercom position for future video door integration. Tier 1 evidence supports OT-le…

**Disposition notes:** - [x] HIGH → item-specification-writer briefing (H-02, Part 10 DAR)

---
