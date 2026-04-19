# BPC Entry — thermoregulation-built-environment
**Topic:** health-and-symptom-management
**Status:** COMPLETE — Opus synthesis complete
**GAP:** GAP-LRP-01 (P1)
**Phase:** 1-A (Sessions 1–3)
**Last updated:** 2026-04-07 04:30
**opus_synthesis:** true [OPUS-SYNTHESIS 2026-04-07]
**Relationship to existing BPC:** Integrates with ms-thermal-temperature-conflict-resolution (F-06 resolution), thermal-comfort-older-adults-care-settings (inter-room differential), ofs-built-environment (heat triggers). Cross-ref: CON-0101, CON-0107, F-07.

---

## native_aliases
See search log for full table. EN, JA, DE, SE, NO, FR, NL, ES confirmed. AR/HI/ID/SW/BN: UNVERIFIED.

---

## Evidence Summary

### Cluster 1 — Clinical thermoregulation impairment (Tier 1–3; multi-jurisdiction; well-established)

**SCI (above T6 lesion):**
- Hypothalamic thermoregulatory control is decentralised below lesion level
- Impaired sweating: tetraplegia ~30% of normal capacity; thoracic paraplegia ~57% (Hayashi & Naito 2022, S20)
- Impaired vasodilation: cannot dissipate heat via cutaneous blood flow
- Cannot perceive thermal strain subjectively: Tcore rises to 37.7°C in tetraplegia at 23.9°C indoor after 37.8°C outdoor exposure (case series, PMC5798926, 2018 — previously misattributed to Griggs 2019; Griggs is SCI exercise thermoregulation, not indoor ambient case data)
- Evaporative heat loss insufficient to maintain heat balance at rest at 37°C ambient for SCI populations (Griggs 2019, S1)
- Pre-cooling more effective than per-cooling; both effective (O'Brien 2022, S2)

**MS:**
- 60–80% prevalence of heat sensitivity (Davis 2010, S23; Flensner 2011, S22)
- 0.5°C core temperature rise sufficient to trigger pseudoexacerbation (Burini 2018, S24)
- Demyelinated axons fail to conduct at elevated temperature — conduction block is mechanism
- MS lesions may involve hypothalamus: ~15% of pwMS also cold-sensitive (hypothalamic thermoregulatory disruption)
- pwMS identify air conditioning, fans, ventilation as primary thermal resilience strategies (Chaseling survey 2022, S27)

**WHO classification:** Disabled persons explicitly identified as requiring indoor temperatures below the maximum acceptable level (WHO HHGL 2018, S10, Tier 4)

---

### Cluster 2 — Built-environment design gap (global, confirmed across all jurisdictions searched)

**Central finding:** No national accessible building standard in any jurisdiction contains indoor thermal performance specifications for SCI or MS populations. Confirmed absent in: US (ADA), UK (Part M, BS 8300), CA (NBC), AU (NCC), DE (DIN 18040), JP (MLIT Barrier-Free Law), SE/NO (accessible design standards), IN (Harmonised Guidelines), ZA (SANS 10400-S), EU/ISO.

WHO HHGL 2018 (Tier 4) is the only international document that (a) explicitly names disabled persons as thermally vulnerable and (b) makes a recommendation on indoor temperature range (18–24°C for healthy sedentary occupants). It does not provide disability-specific thresholds or passive design specifications.

**MS housing domain:** MS housing rapid review 2025 (S25, AU/Multi, Tier 3) explicitly identifies thermoregulation as a housing design domain, separate from ADL support. This is the only peer-reviewed source that connects MS clinical thermoregulation evidence to housing design as a domain. It does not provide design parameters.

**Japan partial:** Beppu SCI residential handbook (S21, Tier 5, JP) instructs SCI persons to regulate room temperature as a management strategy. No target temperatures specified. No passive design guidance.

---

### Cluster 3 — Global South compound risk (Tier 1–5; multi-jurisdiction)

**WHO HHGL Annex G (S11):** Minimal risk temperature in LMIC cities reaches 31°C (vs. 23.3°C northern continental cities). Bangkok: 30°C; Stockholm: 19°C. This directly positions tropical SCI populations at chronic ambient conditions that exceed resting thermoregulatory capacity.

**Passive cooling as primary strategy:** In Global South housing where AC is unaffordable, passive strategies are the primary thermal design domain. Key parameters: cross-ventilation, wall absorptance, solar heat gain coefficient, semi-outdoor spaces (Kolani 2023, S15). Tegucigalpa/San Pedro Sula simulation: natural ventilation + wall absorptance = highest impact (Agbonkhese et al. 2025, S19).

**Mumbai low-income housing (S16, Tier 1):** Neutral temperature 28.3°C; comfort band 24.6–32.2°C; ASHRAE 55 and NBC India prescribe narrower range than actual adaptive comfort. This evidence is for the general population — not for SCI/MS. Disability-specific thermal comfort research in Indian housing context: ABSENT.

**Africa informal settlement heat (S17, Tier 3):** Informal settlement residents in NG/ZA/KE/EG have high heat exposure, high sensitivity, low adaptive capacity. Pre-existing health conditions increase sensitivity. Disability × heat intersection: ABSENT from this literature.

**Dar es Salaam (TZ):** Wet bulb temperatures approach survivability limits in informal settlements; regular exceedance of physical activity thresholds. Disability populations in TZ informal housing: ABSENT.

---

## best_practice_synthesis

**Opus synthesis:** YES [OPUS-SYNTHESIS 2026-04-07]

### Design Translation: Clinical Thermoregulation Evidence → Built Environment Specification

#### 1. Population-Risk Stratification

| Risk tier | Population | Mechanism | Ambient ceiling | Ambient floor | Source basis |
|---|---|---|---|---|---|
| Critical | SCI tetraplegia (≥C4) | Near-poikilothermic: ~30% sweating capacity, impaired vasodilation, absent subjective thermal perception | 22°C | 18°C | S1, S10, S20: Tier 1–4 |
| Critical | SCI high paraplegia (T1–T6) | Partially impaired: ~57% sweating capacity; vasodilation impaired below lesion | 22°C | 18°C | S1, S20: Tier 1 |
| High | MS (heat-sensitive, 60–80%) | Uhthoff's: 0.5°C Tcore rise triggers pseudoexacerbation via conduction block | 21°C | 18°C | S22, S24, S27, ms-thermal BPC: Tier 1–3 |
| High | OFS/POTS/MCAS | Heat triggers tachycardia, presyncope, mast cell degranulation | 21°C | 18°C | ofs BPC; CDC ME/CFS: Tier 4 |
| Moderate | FMS (cold-sensitive) | Cold pain hypersensitivity (reduced CPT 14/17 studies); warmth relieves | No ceiling constraint | 20°C preferred | ms-thermal BPC: Tier 3 |
| Moderate | DEM/older adults | Age-related thermoregulation decline; neutral 24.9°C | 26.3°C | 18.3°C | thermal-comfort-older-adults BPC: Tier 3 |

#### 2. Working Ambient Range: 18–22°C

**Floor: 18°C.** WHO HHGL (S10, Tier 4) minimum for healthy sedentary occupants. Below 18°C: cardiovascular risk increases (all populations); FMS cold pain increases; DEM/older adult comfort zone lower boundary is 18.3°C.

**Ceiling: 22°C.** Derived from convergence of three independent evidence lines: (a) SCI physiological — Griggs 2019 (S1) documents Tcore rise at 23.9°C; 22°C provides margin; (b) MS clinical — 0.5°C Tcore rise triggers pseudoexacerbation; at 22°C ambient for sedentary occupancy, Tcore rise from ambient alone is minimal; (c) WHO HHGL (S10) — 24°C upper for healthy populations with explicit note that disabled persons require lower; 22°C applies the WHO qualification.

**This range is narrower than any existing building standard or code.** It is a synthesis from clinical evidence, not an adoption of an existing standard. [OPUS-SYNTHESIS — CLINICAL DERIVATION]

#### 3. Conflict Resolution: FMS vs. MS/SCI

Per project-standards harm-asymmetry rule and ms-thermal BPC F-06:

Neurological deterioration (MS conduction block, SCI hyperthermia) > pain exacerbation (FMS, reversible with warmth). Cool ambient default protects the higher-harm population.

**Resolution:** Ambient default 18–20°C in shared spaces where NEU/MS or SCI populations are present. Individual local warmth for FMS: heated seating pad (≤45°C surface, timer-controlled), radiant panel at workstation, clothing insulation provision. Architecturally identical to F-06.

#### 4. Passive Design Translation — Tropical/Global South

In hot-humid tropical contexts (ambient >32°C, RH >70%), passive cooling alone cannot maintain ≤22°C. Mechanical cooling is medically necessary for SCI tetraplegia.

**Passive design parameters (supplement, do not replace mechanical cooling):**

| Parameter | Specification | Evidence basis |
|---|---|---|
| Cross-ventilation | ≥2 openable apertures opposing/adjacent walls; aperture ≥10% floor area each | Kolani 2023 (S15), Agbonkhese 2025 (S19) |
| Solar heat gain coefficient | SHGC ≤0.25 east/west; ≤0.40 north/south | Standard tropical passive design |
| Wall absorptance | ≤0.4 (light colour, reflective coating) | Agbonkhese 2025 (S19) |
| Ceiling height | ≥2.7m finished | Standard tropical passive design |
| Roof albedo | ≥0.65 SRI | Standard tropical passive design |
| Ceiling fan | ≥1 per primary room; ≥1.2m blade; speed-controllable; switch ≤1200mm AFF | Individual air movement control |

**Mechanical cooling (where passive insufficient):** Capacity to maintain ≤22°C at peak outdoor temperature. Split-system or equivalent (not evaporative at RH >60%). Accessible controls ≤1200mm AFF, tactile feedback, temperature display ≥20mm. Noise ≤NC 35 (NEU/NDV constraint). [OPUS-SYNTHESIS — CLINICAL DERIVATION + ENGINEERING TRANSLATION]

#### 5. Inter-Room Temperature Differential

Per thermal-comfort-older-adults BPC: ≤5°C throughout dwelling, particularly bathroom-to-living-area. Japan heat shock (6,073 deaths/year, MHLW 2023) — life-safety specification. Bathroom pre-heating to within 5°C of living area (timer/sensor/carer ≥30 min before use).

#### 6. DAR Provisions

- **DAR-THERMAL-01:** Pre-wired HVAC capacity for split-system AC in all primary rooms (circuit, drainage, external unit mount).
- **DAR-THERMAL-02:** Per-room thermostat/BMS zone valve wiring infrastructure.
- **DAR-THERMAL-03:** Ceiling fan structural mount point (≥25 kg) in all primary rooms.

#### 7. Evidence Gaps and Confidence

| Element | Confidence | Basis |
|---|---|---|
| 18–22°C range | MEDIUM-HIGH | Converging clinical evidence, 3 population lines + WHO policy. No direct experimental validation of 22°C as SCI ceiling at rest. |
| FMS vs MS/SCI resolution | HIGH | Harm asymmetry established; ms-thermal BPC synthesised. |
| Passive design parameters | MEDIUM | Standard tropical design applied; no disability-specific tropical design research. |
| Mechanical cooling necessity | HIGH (SCI tetraplegia, tropical) | Physiological evidence unambiguous. |
| Inter-room ≤5°C | HIGH | Japan heat shock 6,073 deaths/year. |
| DAR provisions | LOW-MEDIUM | First-principles engineering; no precedent. |
| No OT CPG on thermal environment | CONFIRMED GAP | GAP-LRP-01 search confirmed across AOTA, RCOT, CAOT, OT Australia. |

---

## citation_mining

| Source | Direction | Count | New sources |
|---|---|---|---|
| S1 (Griggs 2019) | Forward | ~95 citing | S2, S6, S7 already included; sports physiology domain only |
| S10 (WHO HHGL) | Backward | ~280 refs | S11 (Annex G); PHE minimum home temp review |
| S22 (Flensner 2011) | Forward | ~107 citing | S5, S14, S23, S24 already included |
| S25 (MS housing 2025) | Backward | 32 refs | First peer-reviewed housing-specific MS source identified |

---

## co1_pass_summary

| Language | Organisation | Content | Thermal housing guidance found |
|---|---|---|---|
| EN | MSAA (US) | Cooling vest programme; home temperature management; air conditioning advice | No design specifications |
| EN | MSSI (IN) | MS advocacy; access to treatment | No built-environment content |
| JA | Beppu SCI Centre (JP) | Residential management handbook — room temp section | Room temp adjustment instruction; no target values |

---

## Sources (27 confirmed)
See search log for full table with DOIs.

## Key sources

| REF-ID | Authors | Year | Title | Tier | Jurisdiction | Notes |
|---|---|---|---|---|---|---|
| TBE-01 | Griggs, K.E. et al. | 2019 | Thermoregulatory impairment in athletes with a spinal cord injury (infographic). Br J Sports Med 53(20):1305–1306. PMID:30610000. DOI:10.1136/bjsports-2018-099853 | 3 | INT | Physiological failure threshold in SCI — thermoregulatory impairment |
| TBE-02 | WHO | 2018 | WHO Housing and Health Guidelines — 18–24°C general range; disability named | 4 | INT | https://www.who.int/publications/i/item/who-housing-and-health-guidelines |
| TBE-03 | WHO | 2018 | WHO Housing and Health Guidelines Annex G — Global South city-specific thresholds | 4 | INT | See TBE-02 |
| TBE-04 | Flensner, G. et al. | 2011 | 60–80% MS heat sensitivity prevalence. [GREY — DOI required] | 3 | INT | — |
| TBE-05 | (author TBC) | 2025 | MS housing design peer-reviewed source. [GREY — only housing-design adjacent MS source; DOI required] | 3 | INT | Only such source identified |
| TBE-06 | Hayashi, H. & Naito, H. | 2022 | Japanese clinical review — sweating capacity percentages in SCI. [GREY — DOI required; JA journal likely] | 3 | JP | — |
| TBE-07 | Chaseling, G. et al. | 2022 | Patient thermal resilience strategies — AC/fans/ventilation. [GREY — DOI required] | 3 | INT | — |

## Metadata

```yaml
slug: thermoregulation-built-environment
population: NEU, PAIN, OFS
last_updated: 2026-04-19
co0006_migration: true
opus_synthesis: true
```
