# Item-Jurisdiction Divergence Matrix
**Generated:** 2026-04-23
**Source:** jurisdiction_summary fields from 69 search-log files
**Purpose:** Feed Part 4 Evidence Basis table enrichment (Phase 3B)

---

## How to Use This Matrix

For each Part 4 item, this matrix identifies:
- Which jurisdictions specify values for this parameter
- Where values diverge across jurisdictions
- Recommended guidebook target based on cross-jurisdictional analysis

Items marked **HIGH DIVERGENCE** have ≥3 jurisdictions with different values — these are priority targets for Phase 3B enrichment and Phase 3C Opus synthesis.

---

## Category A — Acoustics (A-01 to A-17)

### A-01 to A-09: Acoustic Environment Items
**Source slugs:** acoustics-speech-intelligibility-disability, room-acoustic-performance, deaf-acoustic-built-environment

| Parameter | US | UK | DE | NO | AU | ISO | Guidebook Target |
|---|---|---|---|---|---|---|---|
| Classroom RT (general) | ≤0.6s (ANSI S12.60) | Per BB93 by room type | DIN 18041 by room type | NS 8175 classification | AS/NZS 2107 | ISO 3382 measurement | ≤0.6s |
| Classroom RT (HI children) | **≤0.3s** (ANSI S12.60-2010) | BB93 lower target | — | — | — | — | **≤0.3s** |
| Background noise (classroom) | ≤35 dBA | BB93 targets | DIN 18041 | NS 8175 | AS/NZS 2107 | — | ≤35 dBA |
| HVAC noise (sensitive) | NC-25 (FGI healthcare) | — | — | — | — | — | NC-25 |

**HIGH DIVERGENCE:** Classroom RT for hearing-impaired — only US specifies separate target (0.3s). UK BB93 is most prescriptive mandatory standard. DE DIN 18041 most comprehensive room acoustic standard. NO SINTEF provides largest empirical dataset (87 schools).

### A-10, A-11: Assistive Listening
**Source slug:** assistive-listening-systems

| Parameter | US | UK | EU | ISO | Guidebook Target |
|---|---|---|---|---|---|
| Assembly area trigger | ≥50 occupants (ADA §219) | All meeting/counter (BS 8300) | EN 17210 recommends | IEC 60118-4 performance | All assembly + counter |
| Hearing-aid compatible | 25% of receivers | Induction loop specifically | — | — | Induction loop (telecoil) |
| Performance standard | IEC 60118-4 via A117.1 | BS EN 60118-4 | EN 60118-4 | IEC 60118-4:2018 | IEC 60118-4 |

### A-16: Sensory Room
**Source slug:** sensory-room-user-control

No building code mandates sensory rooms. UK PAS 6463:2022 is closest reference. Snoezelen concept (NL origin 1970s). Clinical evidence only.

---

## Category B — Lighting (B-01 to B-11)

### B-01: Circadian Lighting
**Source slug:** circadian-lighting-melanopic-edi

| Parameter | DE | INT (WELL) | INT (CIE) | Guidebook Target |
|---|---|---|---|---|
| Daytime melanopic EDI | ≥250 MEDI (DIN/TS 67600) | ≥150 EML / ≥250 m-EDI (WELL v2/v6) | CIE S 026 metric | ≥250 MEDI daytime |
| Evening melanopic EDI | — | ≤50 EML | — | ≤10 MEDI |
| Sleep melanopic EDI | — | — | — | <1 MEDI |

NO national building code mandates melanopic EDI. DE DIN/TS 67600:2022 is Tier 5 only.

### B-10: Visual Fire Alarm
**Source slug:** visual-fire-alarm-seizure-safety

| Parameter | US | UK/EU | Guidebook Target |
|---|---|---|---|
| Flash rate | ≤2 Hz (NFPA 72) | EN 54-23 categories | ≤2 Hz |
| Coverage | ADA §702 | EN 54-23 W/C/O categories | Per EN 54-23 |

DEAF vs NEU/NDV conflict resolved via ≤2 Hz frequency limitation.

---

## Category C — Colour & Contrast (C-01 to C-06)

### C-04: LRV Contrast
**Source slug:** luminance-contrast-and-pattern, luminance-contrast-lrv-evidence-base

| Parameter | US | UK | AU | DE | Guidebook Target |
|---|---|---|---|---|---|
| Minimum LRV contrast | No numeric (ADA) | ≥30 points (BS 8300) | ≥30% (AS 1428.1) | DIN 32975 | ≥30 minimum |
| Critical LRV contrast | — | ≥70 points | — | — | ≥50 best practice |

**HIGH DIVERGENCE:** US has NO numeric LRV requirement — significant gap. UK BS 8300 most developed methodology.

---

## Category D — Wayfinding (D-01 to D-11)

### D-08: Signage / D-04: Landmarks
**Source slug:** cognitive-wayfinding-design

UK PAS 6463 is the ONLY standard addressing cognitive wayfinding. Most codes address physical signage only.

### TWSIs (E-09 related)
**Source slug:** detectable-gradient-protocol-sensory-zones

| Jurisdiction | Standard | Notes |
|---|---|---|
| JP | JIS T 9251 | Originated TWSIs (1965) |
| ISO | ISO 23599:2019 | International harmonisation |
| DE | DIN 32984:2020 | Most comprehensive system |
| US | ADA §705 | Limited to specific locations |
| AU | AS 1428.4.1:2009 | Comprehensive TWSI system |
| UK | BS 8300 + DfT guidance | Tactile paving guidance |

**HIGH DIVERGENCE:** TWSI systems vary significantly between jurisdictions.

---

## Category E — Entrances & Circulation (E-01 to E-15)

### E-01 to E-02: Lifts
**Source slug:** accessible-circulation-geometry

| Parameter | US | UK | DE | AU | ISO | Guidebook Target |
|---|---|---|---|---|---|---|
| Turning space | 1524mm (ADA) / 1702mm (A117.1 powered) | 1500mm (BS 8300) | 1500mm (DIN 18040) | 2070mm (powered, AS 1428.1) | 1524mm (ISO 21542) | By device type |

**HIGH DIVERGENCE:** AU 2070mm for powered chairs vs ISO 1524mm — 36% larger.

### E-03: Ramp Gradient
**Source slug:** stair-ramp-threshold-biomechanics-accessibility

| Parameter | US | UK | DE | AU | FR | NO | ISO | Guidebook Target |
|---|---|---|---|---|---|---|---|---|
| Max gradient | 8.3% (1:12) | 8.3% max, 5% preferred | 6% (1:16.7) | 7.1% (1:14) | 5% preferred | 5% (1:20 outdoor) | 5% preferred | 5-6.7% best practice |

**HIGH DIVERGENCE:** US/UK 8.3% max vs FR/NO 5% preferred vs DE 6%. Guidebook targets European range.

### E-06: Level Entry / Threshold
**Source slugs:** threshold-and-level-access, residential-entry-and-threshold

| Parameter | US | UK | DE | AU | FR | Guidebook Target |
|---|---|---|---|---|---|---|
| Max threshold | ≤13mm | Level preferred | ≤20mm (→10mm draft) | **≤5mm** | ≤20mm | **≤5mm** |

**HIGH DIVERGENCE:** AU ≤5mm is 4× stricter than US ≤13mm. DE revision to 10mm is key pending change.

### E-08: Corridor Width
**Source slug:** accessible-circulation-geometry

| Parameter | US | UK | DE | AU | Guidebook Target |
|---|---|---|---|---|---|
| Min clear width | 915mm (ADA) | 1200mm (BS 8300) | 1500mm (DIN 18040) | 1000mm (AS 1428.1) | ≥1200mm |
| Passing width | 1524mm | 1800mm | 1800mm | 1800mm | ≥1800mm |

### E-11: Door Hardware
**Source slug:** threshold-door-hardware

| Parameter | US | UK | DE | AU | ISO | Guidebook Target |
|---|---|---|---|---|---|---|
| Opening force (interior) | ≤22N | ≤30N (BS) / ≤20N (BP) | Not specified | **≤20N** | ≤25N | **≤20N** |

---

## Category F — Sensory & Thermal (F-01 to F-08)

### F-04: Air Quality
**Source slug:** air-quality-voc-chemical-sensitivity-built-environment

Governed by ASHRAE 62.1 (US), EN 16798 (EU), AD F (UK). NO code addresses chemical sensitivity (MCS/MCAS) as accessibility. WELL Air closest.

### F-07, F-08: Thermal
**Source slug:** thermoregulation-built-environment

Governed by ASHRAE 55 (US), EN 16798-1 (EU), ISO 7730 (INT). NO code addresses disability-specific thermoregulation. MS heat sensitivity vs DEM cold sensitivity conflict unresolved by any standard.

---

## Category G — Bathrooms (G-01 to G-08)

**Source slug:** accessible-bathroom-and-grab-bar

Bathroom specifications vary significantly by jurisdiction. Key parameters: grab bar height, WC centre-line offset, turning space, shower dimensions. Detailed divergence data in BPC.

---

## Category H — Controls (H-01 to H-04)

**Source slug:** reach-range-and-accessible-controls

| Parameter | US | UK | DE | AU | ISO | Guidebook Target |
|---|---|---|---|---|---|---|
| Reach range (high) | 1220mm (ADA) | 1200mm (BS 8300) | 1050mm (DIN 18040) | 1100mm (AS 1428.1) | 1100mm (ISO 21542) | **1100mm** |
| Reach range (low) | 380mm (ADA) | 750mm (BS 8300) | 850mm (DIN 18040) | 900mm (AS 1428.1) | 800mm (ISO 21542) | **900mm** |

**HIGH DIVERGENCE:** Low reach — US 380mm vs DE 850mm vs AU 900mm. High reach — US 1220mm vs DE 1050mm. Guidebook targets DE/AU/ISO overlap: **900-1100mm**.

---

## Category H (Kitchen)

**Source slug:** residential-kitchen-and-task-surfaces

**HIGH DIVERGENCE:** DE DIN 18040-2 requires height-adjustable worktops (820-870mm). US/UK do not require adjustable.

---

## Summary of HIGH DIVERGENCE Items (Priority for Phase 3B)

| Item | Parameter | Jurisdictions Diverging | Spread |
|---|---|---|---|
| E-03 | Ramp gradient | US 8.3% vs DE 6% vs FR 5% | 3.3pp |
| E-06 | Threshold height | AU 5mm vs US 13mm vs DE 20mm | 15mm |
| E-08 | Corridor width | US 915mm vs DE 1500mm | 585mm |
| H-01 | Reach range | US 380-1220mm vs DE 850-1050mm | Full overlap: 900-1050mm |
| C-04 | LRV contrast | US none vs UK ≥30/≥70 | Binary gap |
| E-01 | Turning space | ISO 1524mm vs AU 2070mm | 546mm |
| A-04 | Classroom RT (HI) | US 0.3s vs general 0.6s | 0.3s |
| TWSIs | System design | JP/ISO/DE/AU/US all differ | System-level |
| Kitchen | Worktop adjustability | DE mandatory vs US/UK not | Binary gap |
