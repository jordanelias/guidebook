# Best Practices Compendium — VIS
<!-- Managed by research-log-manager. Do not edit manually. -->
<!-- Population partition: VIS -->

---

## detectable-gradient-protocol-sensory-zones
**Updated:** 2026-03-18 22:30  **Evidence tier:** 3–4 (synthesized across 5+ sources)
**Consensus finding:** Multi-sensory zone boundaries — simultaneous visual, acoustic, spatial, and luminance signals at zone transitions — are well-supported by PAS 6463:2022, ISO 21542:2021, Mostafa ASPECTSS 2.0, and Williams et al. (2024). The "Detectable Gradient Protocol" specifies minimum perceptually detectable thresholds at each zone boundary.
**Evidence base:**
  - Multi-sensory redundancy at hazardous transitions: ISO 21542:2021 §9 (tactile + visual, verified)
  - Graduated sensory zone transitions reduce AUT arousal in post-occupancy evaluations: Mostafa (2021) ASPECTSS 2.0, Tier 2 (DOI: 10.3389/fpsyt.2021.727353)
  - Graduated sensory environments with multi-modal zone boundaries: PAS 6463:2022 §6.4, Tier 4
  - Sensory adaptive environments (multi-modal cues) show positive outcomes for autistic children: Williams et al. (2024) scoping review, Tier 1
  - ART "being away" component requires detectable environmental transition: Kaplan & Kaplan (1989)
**Protocol specification (minimum perceptually detectable thresholds):**
  - Visual: ≥30 LRV contrast change at zone boundary surface
  - Acoustic: ≥0.2 s RT60 change between zones (well above just-noticeable difference of ~5% at RT60 <1.0 s per Beranek 2004)
  - Luminance: ≥50 lux reduction between zones (conservative; JND for illuminance is ~15–20%; 50 lux at 300 lux background = 17%, borderline; at 200 lux background = 25%, clearly detectable)
  - Spatial: ceiling height change and/or corridor width change at zone boundary
**Important correction:** RT60 change (reverberation time) and NC change (steady-state noise level) are independent acoustic parameters — do not substitute one for the other. Zone boundaries may involve either a detectable RT60 change OR a background noise level change, not stated as equivalent.
**Zone model (three zones):**
  - Zone 1 — High activation: entry, reception, communal spaces; higher stimulation baseline
  - Zone 2 — Moderate activation: living rooms, corridors, shared circulation; transitional
  - Zone 3 — Low activation: bedrooms, bathrooms, quiet rooms; minimum stimulation retreat
  - Each zone transition uses a buffer zone ≥1.5 m with multi-sensory signals
**Jurisdictions confirmed:** PAS 6463:2022 (UK, guidance only); ASPECTSS 2.0 cross-jurisdictional; no mandatory standard operationalises the Detectable Gradient Protocol
**Early-close:** Yes  **Thin/No-data:** None (synthesized protocol, not language-searched)
**Key sources:** ISO21542-2021-s9 · PAS6463-2022-s6.4 · Mostafa-ASPECTSS2021 · Williams2024 · Beranek2004 · KaplanKaplan1989
**Divergent findings:** —
**Notes:** Numeric thresholds (0.2 s RT60, 50 lux, 30 LRV) are working specifications derived from perception science — label as "minimum perceptually detectable" not empirically validated clinical thresholds. Apply at all population types where sensory environment is a primary design driver: NDV, DEM, NEU/ABI, NDV/MH, OFS.

## luminance-contrast-lrv-evidence-base
**Updated:** 2026-03-18 23:30  **Evidence tier:** 3–4
**Consensus finding:** The 30% LRV (Light Reflectance Value) contrast threshold adopted by six national standards (UK BS 8300, DIN 18040-2, CEREMA France, Swedish BFS, Norwegian TEK17, Japanese MLIT) derives from UK Disability Discrimination Act final-stage regulatory guidance, not from peer-reviewed empirical evidence of sufficiency for people with low vision. It is a regulatory floor, not an evidence-derived optimum.
**Key evidence:**
  - Regulatory origin confirmed: 30% threshold adopted from UK DDA guidance; directly carried into AS 1428.1:2009 and AS 1428.1:2021 without independent empirical validation (GAP-007 research, 2026)
  - Functional benefit of contrast enhancement: real-world camera study found combined step-face and edge contrast enhancement reduced fall-related events vs. control stairway (OR = 2.87, p = .023) — supports enhancement but does not validate 30% as a threshold (Harper et al. 2022, Tier 3, Journal of Ergonomics DOI: 10.35248/2165-7556-22.12.303)
  - High-contrast nosing significantly reduced descending gait speed (coeff. −0.07, p = .010), consistent with improved hazard perception (Brown et al. 2023, Tier 3, Ergonomics DOI: 10.1080/00140139.2022.2141347)
  - Computational modelling: low-contrast nosings become invisible at moderate visual impairment levels even at 30% LRV under certain lighting conditions (Thompson 2017/2022, PMC PMC8993136)
  - For people with severe visual impairment: approximately 65% Michelson contrast (equivalent to ~75% LRV difference) is needed for reliable surface boundary detection — approximately 2.5× the current 30% standard (Dain et al., cited in Manandhar et al. 2022)
  - CNIB (2024): explicitly states 30% LRV as a minimum regulatory floor, not a functional optimum; recommends maximum achievable contrast
  - DSDC EADDAT validation (Marquardt 2011): uses contrast as binary variable (present/absent) — does not validate specific threshold
**Practical guidance specification (replacing the 30% floor as design target):**
  - Code compliance minimum: ≥30% LRV difference (all jurisdictions)
  - Guidebook best practice target: ≥50% LRV difference (NIHR-funded review recommendation; consistent with US Access Board 2-inch contrast band guidance)
  - Severe vision impairment: aim for ≥65% Michelson contrast at all critical junctions (stair nosings, platform edges, kerb lines)
  - Width of contrast strip: ≥50 mm (UK NIHR review); ≥51 mm (US Access Board) — narrower strips (<38 mm) fail to show gait benefit
  - Active research gap flag: no peer-reviewed study has established 30% as sufficient, and emerging evidence suggests it is substantially insufficient for the most severely impaired users. All C-items must carry: "Note: The 30% LRV minimum is a regulatory floor with unknown empirical basis. This guidebook recommends achieving the highest practicable contrast at all critical junctions."
**Standards confirmed:** BS 8300 · AS 1428.1:2021 · DIN 18040-2 · TEK17 · BFS 2024:12 · MLIT Japan — all adopt ≥30% LRV without citing an original empirical study
**Jurisdictions confirmed:** UK · Australia/NZ · Germany · Norway · Sweden · Japan · France (CEREMA)
**Early-close:** Yes  **Thin/No-data:** None (confirmed absence of evidence for threshold is itself the finding)
**Key sources:** Harper2022 · Brown2023 · Thompson2022 · Dain-cited-Manandhar2022 · CNIB2024 · AS1428.1:2021 · BS8300:2018
**Divergent findings:** —
**Notes:** Decision D-03 confirmed: all C-items must carry the regulatory-floor caveat. This is one of the most significant evidence-standards gaps in the entire guidebook. DO NOT cite 30% as an evidence-based optimum. Cite it as a regulatory minimum and recommend highest achievable contrast as design intent.

## visual-impairment-built-environment
**Updated:** 2026-03-19 19:18  **Evidence tier range:** 4–6

### Concept boundary notes
| Language | Native alias | Map | Warning |
|---|---|---|---|
| ZH | 盲道 | ⚠ PARTIAL | 盲道 used generically; search by specific provision type (tactile, contrast, lighting) separately |
| All others | See search-log | ✓ CLEAN | — |

### Best-practice synthesis
**Most inclusive provision:** Continuous tactile walking surface indicator (TWSI) system throughout all primary interior and exterior circulation routes, conforming to ISO 23599:2019: directional (ribbed) indicators throughout unobstructed routes; attention (domed) indicators at all decision points, hazard alerts, and facility entries. TWSI raised profile ≥4–5 mm; colour contrast to adjacent surface ≥70% LRV differential. Audio wayfinding at all primary entry points and lift call buttons.

**Most targeted provision:** For low vision users (who are the majority of VIS population and are often overlooked in tactile-only design): luminance contrast ≥30 LRV points at all critical junctions (stair nosings, door frames, counter edges, floor level changes); consistent lighting levels ≥300 lux in circulation areas without glare; no sudden illuminance transitions exceeding 5:1 ratio between adjacent zones. TWSI detectable by both cane and foot sensation.

**Conflict resolution:** TWSI colour (yellow/mid-yellow is the consensus standard) may conflict with dementia design requirements for plain, low-pattern flooring. Resolution: use detectable profile rather than relying on colour alone; yellow TWSI is acceptable where dementia colour provisions apply if profiling is the primary detection mechanism.

**Highest-ambition actionable specification:** Continuous ISO 23599:2019 TWSI (ribbed directional + domed attention) on all primary routes. ≥4 mm raised profile. Minimum ≥70% LRV contrast to adjacent surface. Audio beaconing at building entries. Luminance contrast ≥30 LRV points at all level changes and critical junctions. Consistent ≥300 lux circulation lighting without glare. Braille and tactile text on all fixed signage at 1400–1600 mm AFF. Contrasting door frames and hardware at all circulation entries.

### Consensus findings
| Finding | Languages confirming | Tier |
|---|---|---|
| TWSI (tactile walking surface indicators) mandatory on primary routes | EN, SV, NO, DA, FI, FR, DE, ZH, JA, NL, ES, PT, KO, IT | 4–6 (ISO 23599 + all jurisdictions) |
| Directional (ribbed) + attention (domed) TWSI types required | EN, ZH, JA, KO, PT | 4–6 |
| TWSI raised profile ≥4 mm | ZH (GB 50763), JA (JIS T 9251) | 6 |
| TWSI colour contrast to adjacent surface (yellow/mid-yellow standard) | ZH (GB 50763), SV, JA | 6 |
| Luminance contrast at critical junctions | EN, SV, DE, NO, DA | 5–6 (DIN 32975, BS 8300, NS 11001) |
| TWSI continuity — must not be obstructed | ZH, JA, KO, EN | 6 (mandatory / strongly worded) |
| Audio signals at pedestrian crossings | ZH, JA, KO, EN | 6 |
| Braille and tactile signage at lift buttons, stairs, building entries | EN, SV, DE, ZH, JA, KO | 5–6 |
| Consistent lighting levels without sudden transitions | EN, SV, DE | 5 (beyond-code guidance) |

### Divergent findings
| Topic | Lang A | Lang B | Cause |
|---|---|---|---|
| TWSI width | JA: standardised per JIS T 9251 | ZH: 250–500 mm range | Regulatory — different standards |
| Colour specification | ZH: medium yellow specifically | Others: general "contrasting colour" | Regulatory — ZH more prescriptive |

### NO-DATA / THIN
| Language | Reason | Predicted by boundary warning? |
|---|---|---|
| IT | DM 236/89 provisions exist but full tactile indicator specification thin | No |

### Citation mining
| Source | Direction | New sources added |
|---|---|---|
| ISO 23599:2019 | Forward | Not yet mined — deferred |

### Key sources
1. ISO 23599:2019 — Assistive products for persons with vision impairment: tactile walking surface indicators. [International · Tier 4]
2. GB 50763-2012 §3.2 — 盲道 specifications. [ZH · Tier 6]
3. MLIT BF Law + JIS T 9251:2006 — 点字ブロック. [JA · Tier 4/6]
4. DIN 32984:2011-10 — Bodenindikatoren im öffentlichen Raum. [DE · Tier 5/6]
5. ABNT NBR 16537:2024 — Acessibilidade — Sinalização tátil no piso. [PT · Tier 6]
6. 편의증진법 시행규칙 별표1 §3 — 시각장애인 유도 블록. [KO · Tier 6]
7. 한국시각장애인연합회 publications — tactile route advocacy. [KO · Tier 2]


8. RNIB (2023). *Building Sight: Design principles and practical recommendations for accessible buildings and environments*. London: RNIB. [EN, Tier 2, UK — primary community-developed VIS built environment guide]
---

## visual-alerting-and-wayfinding-light|VIS,DEAF,DBL
**Updated:** 2026-03-19 13:30  **Evidence tier:** 4–6 (international standards consensus)
**Consensus finding:** Visual alarm devices (VADs) on independent circuits are required in all occupied spaces where deaf, hard-of-hearing, or DBL users may be present; sleeping areas require additional vibrotactile supplementation; IEC 60118-4 hearing loop is the international floor for communication access.
**Flash rate range:** 0.5–2 Hz (EN 54-23 / EU) or 1–3 Hz (ADA/NFPA 72 / US) — both exclude rates associated with photosensitive epilepsy risk
**Jurisdictions confirmed:** UK, EU, US, NO, FR, DE, ZH (GB 50763), JA (FDMA 2016 guideline)
**Divergent findings:** JA: 光警報装置 recommended not mandatory; KO: no dedicated VAD standard confirmed
**Early-close:** no  **Thin/No-data:** FI (EN 54-23 applies but no FI-specific provision); KO (no VAD-specific standard)
**Citation mining:** Standards domain — not applicable
**Key sources:** BS EN 54-23:2010; NFPA 72; IEC 60118-4:2014+AMD1; FDMA JP 2016; GB 50763-2012 §8; Décret 2009-1272 (FR); Bufdir.no (NO)

## luminance-contrast-and-pattern|VIS,DEM,NDV
**Updated:** 2026-03-19 13:30  **Evidence tier:** 1–2 (Lukman et al. 2020); Tier 3–6 (standards and reviews)
**Consensus finding:** LRV ≥30 difference (UK/AU) / Michelson K ≥0.4 (DE) at all critical junctions is the internationally confirmed minimum for VIS navigation; patterned and high-contrast floor transitions are contraindicated in DEM environments; colour contrast alone cannot substitute for luminance contrast.
**DEM inverse rule:** ≤10 LRV differential between adjacent floor material zones to prevent step-misperception (DSDC evidence; supported by Alzheimer's Society perceptual mechanism documentation)
**Jurisdictions confirmed:** UK (BS 8300, Part M), AU (AS 1428.1), DE (DIN 32975, DIN 18040-1), FR (CEREMA), EU (EN 17210), ZH (GB 50763 tactile indicator contrast), JA (JIS T 9251)
**Divergent findings:** DE specifies tiered contrast (K≥0.4 for orientation vs K≥0.7 for signage) — more granular than UK flat ≥30 LRV; formula differs (Michelson vs LRV difference) but thresholds broadly equivalent
**Early-close:** no  **Thin/No-data:** ZH, JA, KO (dementia-specific floor pattern guidance not found)
**Citation mining:** PubMed 8716494 floor patterns wandering Alzheimer's added from DSDC literature
**Key sources:** REF-20 (Lukman et al. 2020 HERD OT study); REF-21 (Arditi PMC 2017 LRV evidence base analysis); REF-22 (DIN 32975); REF-24 (BS 8300/Part M); REF-25 (DSDC dementia flooring); REF-26 (PubMed 8716494); REF-28 (DBSV Fachbroschüre DE)

# BPC Entries — Append to references/best-practices-compendium.md
# Produced: 2026-03-19 11:00

---
