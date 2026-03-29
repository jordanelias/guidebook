## Multi-Population Conflict Matrix — LIGHT-INT (Illuminance Level)
**Date:** 2026-03-29 00:50
**Domain:** LIGHT-INT — Daytime illuminance (lux / melanopic EDI)
**Populations served:** DEM, NEU, NDV/AUT, NDV/SENS, NDV/MH, PAIN, OFS, VIS, DEAF
**Classification:** [BOTH] — inter-group AND intra-individual
**Overall status:** UNRESOLVED at Tier 0 · RESOLUTION-PROPOSED at Tier 1 (zoning + individual control) · TIER-2-ONLY for intra-individual co-occurrence

### Active Conflicts

| Domain | Pop A | Pop B | A spec | B spec | Resolution | Status | Evidence |
|---|---|---|---|---|---|---|---|
| LIGHT-INT (daytime) | DEM, VIS, DEAF | NDV/AUT, NDV/SENS, NEU(migraine), PAIN(fibro), OFS/MCAS | ≥300 lux / ≥250 melanopic EDI / ≥4000 K | ≤200 lux ambient preferred; user-controlled to 0 lux; ≤3000 K; no fluorescent | Zoning + individual control + temporal dosing | RESOLUTION-PROPOSED (Tier 1) | ◐ |
| LIGHT-INT (evening) | DEM | NDV/AUT, NEU, PAIN, OFS | ≤2700 K / ≤10 melanopic EDI | ≤2700 K / dim | Non-conflicting — parameters aligned | RESOLVED-CONSENSUS | ● |
| LIGHT-INT (intra-individual) | NEU/MH/OFS circadian need | NEU/MH/OFS photosensitivity | ≥250 melanopic EDI for sleep-wake | Blue-enriched spectrum (480nm) triggers pain via shared ipRGC pathway | Temporal dosing; Tier 2 OT assessment | TIER-2-ONLY | ◐ |

### Mechanistic Finding

The ipRGC/melanopsin pathway (peak ~480nm) mediates BOTH circadian entrainment AND migraine/fibromyalgia photosensitivity. This is a single retinal pathway serving opposing clinical objectives. Circadian-effective lighting requires blue-enriched spectrum; migraine/fibro photosensitivity is worst at blue wavelengths. These cannot be separated by luminaire design alone (indirect/diffuse delivery does not change the melanopic dose at the eye).

### Resolution Evidence Register

**Resolution 1 — Spatial zoning (three-zone model)**
- Source: CON-0016; detectable-gradient-protocol BPC; PAS 6463:2022; Brown et al. 2022
- Mechanism: Zone 1 (social/circadian): ≥300 lux / ≥200 EML, ≥4000 K · Zone 2 (transition): 150–300 lux, 3000–4000 K · Zone 3 (quiet/refuge): user-controlled 0–150 lux, ≤3000 K · Evening all zones: ≤2700 K / ≤10 EML
- Outcome data: None for integrated three-zone system. Individual zone parameters from separate evidence bases.
- Guidebook implication: Tier 1 specification. Zone 1 explicitly stated as DEM/VIS/DEAF-serving; will cause discomfort for photosensitive populations. Zone 2/3 must provide equivalent functional access (workspaces, dining, social — not only refuge rooms). DAR required for post-occupancy zone boundary adjustment.
- Status: **RESOLVED-CONSENSUS** · Confidence: **MEDIUM**

**Resolution 2 — Individual dimming control (H-02)**
- Source: circadian-lighting-melanopic-edi BPC; NDV BPC; CON-0005; PAS 6463:2022; Unwin et al. 2022/2023
- Mechanism: Occupant-controlled dimming 0–100%, CCT 2700–5000 K, at individual position within ambient environment.
- Outcome data: Unwin et al. 2022/2023 (Tier 3, n=41): user control is primary design variable for self-regulation. Convergent evidence across NDV, DEM, DEAF, OFS populations.
- Guidebook implication: Tier 0 mandatory infrastructure. No fluorescent/stroboscopic sources anywhere in building. Individual control does not resolve shared ambient parameters (corridors, dining rooms, open-plan spaces).
- Operability limitation: DEM late stage cannot operate. IntD without support cannot operate. Adjustment requiring disability disclosure is exclusionary.
- Status: **RESOLVED-CONSENSUS** (infrastructure) · Confidence: **HIGH** for principle; **MEDIUM** for shared-ambient limitation

**Resolution 3 — Indirect/diffuse delivery**
- Source: circadian-lighting-melanopic-edi BPC
- Mechanism: Circadian dose via diffuse/indirect luminaires (B-07); reduces perceived glare/point-source discomfort.
- Outcome data: None comparing migraine response to indirect vs direct at equivalent melanopic EDI.
- Assessment: Reduces perceptual glare but does NOT resolve melanopic pathway conflict. 250 melanopic EDI from a diffuse ceiling activates the same ipRGC→thalamic trigeminovascular pathway as 250 melanopic EDI from a direct downlight. Migraine pain mechanism is melanopic dose, not luminaire geometry.
- Status: **PARTIAL** — addresses comfort, not mechanism · Confidence: **MEDIUM-LOW**

**Resolution 4 — Temporal separation (evening)**
- Source: Brown et al. 2022 (PLOS Biology)
- Mechanism: Evening ≤2700 K / ≤10 melanopic EDI serves both DEM circadian protocol and NDV/AUT/NEU low-stimulation preference.
- Outcome data: Brown et al. 2022 consensus (Tier 3).
- Assessment: Evening parameters non-conflicting. Daytime conflict remains.
- Status: **RESOLVED-CONSENSUS** (evening only) · Confidence: **HIGH**

**Resolution 5 — Temporal dosing (morning circadian window)**
- Source: therapeutic-lighting-design BPC; clinical circadian protocol literature
- Mechanism: Morning circadian dose (≥250 melanopic EDI, ≥4000 K) for defined 30–60 min window when therapeutic benefit highest and interictal photosensitivity may be lower. Remainder of day at lower, controllable levels.
- Outcome data: No RCT for built-environment implementation of timed dosing in photosensitive populations.
- Guidebook implication: Tier 2 — OT assessment determines individual tolerance and dosing window. Guidebook provides range and protocol framework; clinician resolves individual.
- Status: **RESOLUTION-PROPOSED** · Confidence: **LOW** — clinical plausibility without built-environment evidence

**Resolution 6 — Spectral separation (narrow-band green, 520nm)**
- Source: Noseda et al. 2016 (Brain, DOI:10.1093/brain/aww119, n=69); Lipton et al. 2023 (Frontiers Neurology, DOI:10.3389/fneur.2023.1282236, open-label)
- Mechanism: NbGL (520±10nm) at low intensity produces smallest retinal/cortical signals; reduced migraine pain ~20%. At high office-level intensity (~500 lux), ~80% migraine patients reported intensification in all colours except green.
- Assessment: Addresses photosensitivity but does NOT drive melanopic/circadian response (ipRGCs peak 480nm, not 520nm). Technology currently expensive and not commercially available at building scale.
- Guidebook implication: Specification note under B-06/B-07 as emerging evidence (○). Not a specification value. May be considered for task lighting in photosensitivity-designated zones pending further evidence and commercial availability.
- Status: **EMERGING** · Confidence: **LOW** — Tier 3, pre-commercial, single-pathway

**Resolution 7 — Tier escalation**
- The conflict is irreconcilable at Tier 0 for shared ambient spaces. At Tier 1, architect zones based on identified populations. At Tier 2, OT assessment resolves individual placement.
- For intra-individual co-occurrence (NEU/MH/OFS): circadian lighting and photosensitivity management are competing clinical objectives. The guidebook states the trade-off explicitly; neither takes priority without individual assessment.
- Status: **TIER-2-ONLY** for intra-individual · Confidence: **HIGH** — this is the honest answer

### Tier 0 Default Specification

Tier 0 cannot specify a single lux value for shared spaces. Tier 0 specifies:

1. Individual lighting control (H-02) mandatory in all primary occupied spaces — dimmable 0–100%, CCT 2700–5000 K, zero fluorescent/stroboscopic sources building-wide
2. Zoning infrastructure — electrical and spatial capacity for ≥2 distinct illuminance zones per floor plate, with DAR for post-occupancy zone boundary adjustment
3. No fixed high-brightness ambient (≥300 lux / ≥4000 K) without adjacent low-stimulation alternative of equivalent function (not only refuge — workspaces, dining, social)
4. Default ambient: ≤300 lux photopic, ≤3500 K. Circadian-dose spaces (≥250 melanopic EDI, ≥4000 K) available but not universal.

**Harm asymmetry:** Bright ambient causes measurable pain in 70–90% of migraine/fibro populations; dim ambient reduces circadian benefit for DEM but does not inflict pain. The asymmetry favours the lower default.

**Exception:** DEM-designated facilities (Tier 1): default to bright circadian (≥300 lux / ≥250 melanopic EDI daytime). Photosensitive staff/visitors use zoned alternatives.

### Unresolved Conflicts → Gap Register

| Gap ID | Populations | Specification implication | Research needed |
|---|---|---|---|
| GAP-CONF-LIGHT-01 | NEU(migraine), PAIN(fibro), NDV/SENS | Resolution 3 validity: indirect vs direct at equivalent melanopic EDI | Study comparing migraine response by luminaire type at controlled melanopic dose |
| GAP-CONF-LIGHT-02 | ALL multi-population facilities | Three-zone integrated system untested | POE of facility implementing zoned lighting across DEM/NDV/NEU populations |
| GAP-CONF-LIGHT-03 | NEU/MH/OFS (intra-individual) | Temporal dosing protocol feasibility | RCT: timed morning circadian dose in photosensitive populations, built environment |
| GAP-CONF-LIGHT-04 | DEM late-stage + photosensitivity | Intra-individual conflict when user cannot self-adjust or relocate | No evidence pathway identified — clinical management, not architectural resolution |

### Sources

| Source | Tier | Role in matrix |
|---|---|---|
| Brown et al. 2022, PLOS Biology, DOI:10.1371/journal.pbio.3001571 | 3 | Melanopic EDI thresholds; evening consensus |
| Noseda et al. 2016, Brain, DOI:10.1093/brain/aww119 | 3 | Green light / ipRGC mechanism; spectral conflict |
| Lipton et al. 2023, Frontiers Neurology, DOI:10.3389/fneur.2023.1282236 | 3 | NbGL clinical confirmation |
| Heinricher et al. 2016, PMC4794405 | 3 | Fibromyalgia photosensitivity quantification |
| ScienceDirect 2025, VPDT study | 3 | Fibromyalgia as strongest VPDT predictor |
| Unwin et al. 2022, Autism 26(6), DOI:10.1177/13623613211050176 | 3 | User control as primary variable |
| DSDC Stirling | 3–5 | DEM lighting thresholds |
| DIN/TS 67600:2022 | 5 | Circadian design guideline |
| PAS 6463:2022 | 5 | NDV/DEM sensory zoning |
| DeafSpace Guidelines (Gallaudet 2010) | Co-1 | DEAF signing visibility |
| WELL v2/v6 Feature L07 | 5 | Circadian lighting standard |
| CDC ME/CFS clinical guidance | Co-1 | OFS photosensitivity |
| AMF (American Migraine Foundation) | 2 | Migraine photosensitivity prevalence |

---
*Opus synthesis 2026-03-29. First execution of cross-population-conflict-mapper skill.*
