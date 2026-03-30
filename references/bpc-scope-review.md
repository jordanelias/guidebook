# BPC Evidence Scope Review: Professional Domain Classification

**Date:** 2026-03-29
**Source material:** All active BPC slug files (58 slugs), conflict matrices (3 domains + synthesis), cross-population conflict resolutions, connection register synthesis. Flat population files excluded per project-standards (frozen archives).
**Purpose:** Classify evidence-supported specifications by which professional domain holds specification authority: (a) engineers, (b) OTs + specialty consultants, (c) building policies/operations.

---

## Method

Each BPC best_practice_synthesis was reviewed for specifications that contain:
- Measurable physical performance values requiring engineering design → **(a)**
- Population-specific or person-specific calibration requiring clinical assessment → **(b)**
- Operational, management, or maintenance requirements that cannot be built → **(c)**

Items are classified by where the evidence itself places specification authority — not by where the current guidebook assigns them.

---

## (a) Specifications Where Engineering Holds Primary Authority

The BPC evidence consistently produces measurable performance targets. These targets originate in population-need evidence (OT/clinical research), but their *delivery* depends on engineering design. The guidebook should state the population need and the target value; the engineering consultant designs the system to achieve it.

### Acoustic performance values

| BPC slug | Specification | Value from evidence | Engineering discipline | Evidence tier |
|---|---|---|---|---|
| acoustics-speech-intelligibility | RT60 hearing-impaired populations | ≤0.3 s (500–2000 Hz) | AC | Tier 1 (Murgia 2023, Iglehart 2020) |
| acoustics-speech-intelligibility | RT60 general population (failure boundary) | ≤0.6 s | AC | Tier 4–6 |
| acoustics-speech-intelligibility | Background noise | ≤35 dBA unoccupied | AC + ME | Tier 4 (ANSI/ASA S12.60) |
| acoustics-speech-intelligibility | STI hearing loop users | ≥0.5 at furthest listener | AC + EE | Tier 4 (IEC 60118-4) |
| room-acoustic-performance | STI general | ≥0.60 | AC | Tier 5–6 |
| room-acoustic-performance | STI hearing-impaired/CI | ≥0.75 | AC | Tier 1 |
| room-acoustic-performance | NRC ceiling panels | ≥0.85 (means, not criterion) | AC | Tier 5–6 |
| sensory-relief-space-design | Sensory room STC | ≥50 partition | AC | Tier 5 (PAS 6463) |
| sensory-relief-space-design | Sensory room RT60 | ≤0.3 s | AC | Tier 5 |
| sensory-relief-space-design | Sensory room NC | ≤25 HVAC | AC + ME | Tier 5 |

**Opus synthesis note (room-acoustic-performance):** "NRC compliance alone does not guarantee adequate listening conditions. STI is the performance criterion, NRC is means." This directly supports engineering holding the design authority — the guidebook states the STI target, the acoustic engineer selects the means.

### Hearing loop and assistive listening

| BPC slug | Specification | Value | Discipline | Tier |
|---|---|---|---|---|
| assistive-listening-systems | Counter loop field strength | 100 mA/m ±3 dB per IEC 60118-4 | AC + EE | Tier 4 |
| assistive-listening-systems | Room loop field strength | IEC 60118-4 throughout | AC + EE | Tier 4 |
| assistive-listening-systems | Auracast DAR | 25 mm conduit + power provision | EE | Tier 5 (emerging) |

### Lighting performance values

| BPC slug | Specification | Value | Discipline | Tier |
|---|---|---|---|---|
| circadian-lighting-melanopic-edi | Daytime melanopic EDI | ≥250 lux at eye level | EE | Tier 3 (Brown 2022) |
| circadian-lighting-melanopic-edi | Evening melanopic EDI | ≤10 lux | EE | Tier 3 |
| circadian-lighting-melanopic-edi | Sleep melanopic EDI | <1 lux | EE | Tier 3 |
| therapeutic-lighting-design | Flicker-free LED | IEEE 1789-2015 compliant | EE | Tier 4 |
| visual-fire-alarm-seizure-safety | VAD flash rate | 0.5–1 Hz (synchronised) | EE + fire | Tier 3–4 |
| visual-fire-alarm-seizure-safety | Supplementary channels | Voice alarm + vibrotactile | EE + fire | Tier 3 |
| dementia-built-environment | Corridor illuminance | ≥300 lux | EE | Tier 3–5 (DSDC) |
| dementia-built-environment | Task illuminance | ≥500 lux | EE | Tier 3–5 |

### Air quality and thermal

| BPC slug | Specification | Value | Discipline | Tier |
|---|---|---|---|---|
| air-quality-voc | Filtration | MERV 13 minimum; HEPA for OFS/MCAS primary | ME | Tier 4–5 |
| air-quality-voc | Fresh air supply | ≥10 L/s general; ≥15 L/s OFS primary | ME | Tier 4–5 |
| air-quality-voc | VOC | TVOC ≤0.5 mg/m³ at 28 days (EN ISO 16000-9) | ME (commissioning) | Tier 4 |
| air-quality-voc | CO₂ monitoring | Alert at 800 ppm | ME (BMS) | Tier 5 (WELL v2) |
| air-quality-voc | Thermal stability | Ambient variation ≤1°C/hr; ≤2°C across primary route | ME | Expert consensus |
| thermal-comfort-older-adults | Older adult neutral temperature | 24.9°C (comfort zone 18.3–26.3°C) | ME | Tier 3 (Baquero 2023) |
| thermal-comfort-older-adults | Inter-room differential | ≤5–7°C | ME | Tier 5 (Japan CAA) |
| ms-thermal-temperature | MS/OFS ambient | ≤18–21°C | ME | Tier 3–4 |
| pain-ofs-built-environment-design | Individually controllable thermal zone | 18–23°C range | ME + EE (BMS) | Co-1/Tier 3 |

### Structural

| BPC slug | Specification | Value | Discipline | Tier |
|---|---|---|---|---|
| fold-down-grab-bar | Grab bar load rating (standard) | ≥200 kg SWL | SE | Tier 4–5 (elevated from KITE 1.3 kN) |
| fold-down-grab-bar | Grab bar load rating (bariatric) | ≥300 kg SWL | SE | Tier 5 |
| fold-down-grab-bar | Continuous structural blocking | Full toilet wall length, both sides | SE | Tier 4–5 |
| accessible-bathroom-and-grab-bar | Zero-threshold drainage | Linear drain within 1200 mm; floor slope ≤1:80 | ME + SE | Tier 5–6 |
| floor-vibration-wheelchair-disability | Floor vibration limit | Context-dependent; engineering analysis required | SE | Tier 3 |

### Summary finding (a)

The BPC evidence produces approximately **40 discrete measurable performance values** that are engineering deliverables. The evidence establishes the *why* (population need) and the *what* (target value). Engineering establishes the *how* (system design to achieve the target). The guidebook should present the target values with their population rationale and evidence tier, then cross-reference the engineering brief where the design solution is specified.

**Critical distinction from room-acoustic-performance Opus note:** "The 0.6 s value in most building codes is not an evidence-based target for inclusive design — it is the threshold at which even normal-hearing listeners begin to lose speech intelligibility." The guidebook's role is to state evidence-derived targets (which often exceed code) alongside the population rationale. Engineering's role is to deliver those targets. The guidebook should not specify the engineering means (duct velocity, NRC selection, plant room configuration).

---

## (b) Specifications Where OTs + Specialty Consultants Hold Primary Authority

These are specifications where the BPC evidence explicitly states that person-specific or population-specific clinical assessment is required to resolve the value. The guidebook provides Tier 1 population medians; the clinician resolves to the individual.

### OT-resolved specifications (Tier 2)

| BPC slug | Specification | Tier 1 median | Why OT resolves | Evidence |
|---|---|---|---|---|
| accessible-bathroom-and-grab-bar | Grab bar height | 700 mm (range 650–900 mm) | Transfer method determines optimal height: "280 mm above seat surface per OT assessment" — seat-relative formulation is the Tier 2 standard | Tier 1 (Levine 2025, Kennedy 2015, Nakamura 2009) |
| accessible-bathroom-and-grab-bar | WC turning circle | ø1500 mm standard / ≥1800 mm powered WC | Manual vs power wheelchair determines which value applies; Tier 2 = individual wheelchair measurement | Tier 5 (BS 8300-2 Annex G) |
| accessible-bathroom-and-grab-bar | Hemiplegic vertical bar positioning | 5 cm from WC edge, paralysis side | Paralysis side, grip capacity, trunk stability — all OT-assessed | Tier 1 (Nakamura 2009) |
| upper-limb-impairment | Toilet centreline distance | 760 mm (30 in.) from nearest wall | Transfer method (stand-pivot vs lateral) determines optimal distance; 90% use stand-pivot (Sanford 2013) but OT confirms for individual | Tier 3 |
| upper-limb-impairment | Grab bar configuration | Two vertical bars primary; continuous rail 600–1200 mm AFF | Individual grip capacity, COP deviation, fall-recovery strategy — OT-assessed | Tier 1 (Kennedy 2015) |
| residential-kitchen-and-task-surfaces | Worktop height | 800 mm fixed / 650–900 mm adjustable | Standing vs seated vs LPA — electric adjustment is universal resolution, but Tier 2 resolves to individual anthropometry | Tier 5 (NL WMO) |
| pain-ofs-built-environment-design | Seating interval | 25–30 m (OFS) / 50 m (MOB) | Orthostatic intolerance onset timing varies by individual; OT/physician determines | Co-1/Tier 3 |
| accessible-bathroom-and-grab-bar | Dressing area clear floor space | ≥1500×1500 mm (turning) / ≥760×1200 mm (transfer) | Full dressing turning vs transfer-only depends on individual mobility + dressing method | Tier Co-2 (CAOT 2024) |
| accessible-bathroom-and-grab-bar | Closet rod height | ≤1050 mm (forward reach, trunk-unstable) / ≤1200 mm (general seated) | Forward reach vs lateral reach vs standing — OT-assessed trunk stability determines | Tier Co-2 (RCOT 2019, AOTA 2023) |

### Specialty consultant-resolved specifications (Tier 1)

| BPC slug | Specification | Why specialist resolves | Which specialist | Evidence |
|---|---|---|---|---|
| dementia-built-environment | Floor plan topology (loop vs linear) | "Loop-plan is the evidence-based provision for residential DEM care. For non-residential, the evidence supports legible circulation with identifiable decision points." Stage-awareness needed. | Dementia design specialist | Tier 3 (Marquardt 2009, Bowes 2019) |
| dementia-built-environment | Toilet visibility from bedroom | Sightline geometry + cognitive staging determines optimal arrangement | Dementia design specialist | Tier 3 |
| deafblind-built-environment-design | Protactile spatial requirements | ≤600 mm face-to-face, ≥1500 mm per communication pair — "genuinely novel provision not found in any building standard worldwide" | DeafBlind specialist **[GAP — no Part 9 section]** | Co-1 (Clark/Nuccio) |
| deafblind-built-environment-design | JA close-range signing (接近手話) | 500–1000 mm interpreter positioning zone — "distinct from ASL/BSL spatial requirements and from Protactile" | DeafBlind specialist | Co-1 |
| deafblind-built-environment-design | Intervenor clear floor zone | ≥1500 mm adjacency at service counters — "no jurisdiction specifies this" | DeafBlind specialist | Tier 2 (DbI) |
| sensory-relief-space-design | Sensory room content calibration | "Individual occupant control is the primary design variable — more predictive of self-regulation outcomes than any static environmental parameter" | Sensory design consultant / OT | Tier 3 (Unwin 2022, 2023) |
| deaf-spatial-design | Sightline geometry for signed language | Distance, angle, lighting on interpreter — population-specific proxemics | DeafSpace consultant | Tier 5 (Gallaudet DeafSpace) |
| room-acoustic-performance | NDV/AUT acoustic calibration | "No internationally agreed quantified RT60 target specific to autistic users" — individual sensory profile determines | Sensory design consultant / OT | Tier 1 (Bettarello 2021, Caniato 2024) — threshold = unquantified |

### Conflict resolution requiring OT/specialist

The conflict-matrices SYNTHESIS explicitly identifies specifications that cannot be resolved architecturally:

| Domain | Finding | Why OT/specialist required |
|---|---|---|
| LIGHT-INT | "Intra-individual conflicts (NEU/MH/OFS) are not resolvable by architectural design alone" | Same person has conflicting lighting needs across conditions; OT assesses priority |
| SPATIAL-OPEN | "DEAF+NDV/AUT intra-individual: requires OT assessment at Tier 2" | Same person needs open sightlines (DEAF) and enclosed retreat (NDV); OT determines spatial arrangement |
| All divergent domains | "'Adjustable' fails for DEM late stage, IntD without support, and shared ambient parameters" | Guidebook must "specify operability per population for every 'adjustable' specification" — OT determines who can self-adjust |
| cross-population-conflict | "Where no population is disadvantaged by the lower [value]" → convergent = Tier 0 | But where divergent → "flag as Tier 2 — OT assessment required for individual resolution" |

### Summary finding (b)

The evidence consistently identifies a **Tier 1 → Tier 2 handoff point**: the BPC provides population medians; the OT/specialist resolves to the individual. This handoff is most critical for:

1. **Grab bar and bathroom layout** — transfer method, grip, trunk stability
2. **Workspace heights** — anthropometry, seated/standing, reach envelope
3. **Sensory environment calibration** — individual sensory profile determines thresholds
4. **DEM spatial topology** — cognitive stage determines optimal arrangement
5. **DBL spatial provisions** — communication method determines spatial requirements
6. **Intra-individual conflict resolution** — where one person has co-occurring conditions with opposing environmental needs

**GAP confirmed:** Part 9 has no DeafBlind specialist consultant section. The DBL evidence (13 KB, three merged entries) contains five novel spatial specifications that no building standard worldwide addresses. These are Co-1/Tier 2 evidence requiring specialist input that has no routing path in the current guidebook.

---

## (c) Specifications That Are Building Policies / Operations

These are requirements identified in the BPC evidence that cannot be delivered through construction specifications. They require ongoing operational enforcement.

### Explicitly identified as policy in BPC evidence

| BPC slug | Specification | Exact BPC language | Recommended home |
|---|---|---|---|
| air-quality-voc | Fragrance-free zone enforcement | "Not a design item — an operational policy that must be embedded in FM brief and lease/occupancy agreements" | FM brief / operational annex |
| air-quality-voc | Cleaning product restriction | "Low-fragrance, low-VOC in maintenance specification; no aerosol sprays during occupied hours" | FM brief |
| air-quality-voc | Biophilic planting species control | "Low-VOC, low-pollen species only in OFS-occupied spaces; no strongly scented flowering plants" | FM brief / landscape maintenance spec |
| deafblind-built-environment-design | Furniture rearrangement prohibition | "Furniture rearrangement protocols are to prohibit changes to primary tactile wayfinding routes without advance notification to DBL occupants" | FM protocol |
| deafblind-built-environment-design | Tactile map update cycle | "Updated every 3 years minimum" | FM/maintenance schedule |
| ofs-built-environment | Queue management systems | "Queue management systems eliminating prolonged enforced standing" | Operational policy |
| sensory-room-user-control | Staffing model | "1:1 adult-child interaction with child in control of all sensory equipment" | Staffing policy |
| dementia-built-environment | DSDC EADDAT as monitoring instrument | "OT assessment of cognitive staging and specific disorientation type informs environmental modification priority" — ongoing assessment, not one-time design | POE / operational protocol |

### Partially policy, partially construction

| BPC slug | Specification | Construction component | Policy component |
|---|---|---|---|
| air-quality-voc | Fragrance-free zones | Dedicated ventilation (ME — F-02) | Prohibition of fragranced products |
| pain-ofs-built-environment-design | Seated service provision | Seated counter design (architectural) | Requirement that staff permit seated interaction |
| thermal-comfort-older-adults | Inter-room temperature differential | HVAC zoning (ME) | Ongoing monitoring; seasonal adjustment |
| accessible-bathroom-and-grab-bar | Bed-exit sensor night lighting | Sensor + low-level lighting circuit (EE) | Response protocol when sensor triggers |
| accessible-bathroom-and-grab-bar | Emergency pull cord | Hardware (EE) | Response protocol — "response within 3 s" is staffing |
| accessible-bathroom-and-grab-bar | Bedside medication storage | Lockable cabinet at specified height (architectural) | Medication management protocol |

### Summary finding (c)

The BPC evidence identifies approximately **8 specifications that are purely operational** and **6 that are split** between a construction component and an operational component. The current guidebook does not have a dedicated operational annex. These specifications need a home that is:
- Linked to the relevant item specification (so the construction and policy components are cross-referenced)
- Clearly distinguished from construction specifications (so that architects do not misread policy as something they can "build in")
- Directed to facility managers, building operators, and care providers — not to the design team

---

## Structural Recommendations

### 1. Engineering performance values: state target, not means

The BPC evidence supports approximately 40 engineering performance targets. For each, the guidebook should:
- State the population need (from BPC best_practice_synthesis)
- State the target value with evidence tier
- Cross-reference the engineering brief where the design solution is specified
- Not prescribe the engineering means (e.g., "NRC ≥0.85 ceiling panels" becomes "RT60 ≤0.3 s in speech-critical rooms — acoustic engineer to specify absorption treatment")

### 2. Tier 2 handoff flags on all OT-resolvable specifications

Every specification where the BPC provides a range rather than a point value — and where the range reflects individual variation rather than jurisdictional difference — should carry:

> **Tier 1 default: [median value]. Tier 2: OT assessment resolves position within range based on [specific functional assessment parameter].**

The BPC evidence already supplies the functional assessment parameter in most cases (transfer method, trunk stability, sensory profile, cognitive stage, communication method).

### 3. New Part 9 section: DeafBlind Specialist Consultant

The DBL BPC contains five novel spatial specifications with no parallel in any building standard worldwide. All are Co-1/Tier 2 evidence. The guidebook currently has no routing path for DBL specialist input. Part 9 needs a §9.X DeafBlind Specialist Consultant section covering:
- Protactile spatial requirements
- Close-range signing positioning zones (接近手話, tactile BSL)
- Intervenor/guide-interpreter clear floor zone
- Tactile map and wayfinding continuity
- Appointment trigger: DBL as primary or secondary population code

### 4. Operational annex for policy specifications

Create Part [X] or an annex containing all specifications that require ongoing operational enforcement. Each entry should:
- Reference the parent item specification
- State the operational requirement
- Name the responsible party (FM, care provider, building owner)
- State the review cycle

### 5. Split specifications: tag both components

For the 6 split specifications (construction + policy), the item specification should tag both:

> **Construction: [specification]. Operations: [policy requirement — see Operational Annex §X.X].**

This prevents the policy component from being invisible once the design team hands over.

### 6. "Adjustable" audit

The conflict-matrices SYNTHESIS identifies that "adjustable" specifications fail for DEM late stage, IntD without support, and shared ambient parameters. Every specification currently written as "adjustable" or "individual control" needs a population operability note:

> **Operability: [list populations who can self-adjust]. Populations requiring carer/staff operation: [list]. Default setting when no individual present: [value, with harm-asymmetry rationale].**

---

## Appendix: Unsupported values flagged in BPC evidence

These values appear in current or proposed specifications but have no evidence derivation. They should not carry evidence-tier markers.

| Value | BPC source | Status |
|---|---|---|
| 20 m restorative interval distance (A-04) | cross-population-conflict-resolutions | [UNSUPPORTED — concept evidence-based, threshold not evidence-derived] |
| 5 m lighting transition zone (B-05) | cross-population-conflict-resolutions | [UNSUPPORTED — PCS photophobia mechanism solid; distance not derived] |
| 0.1 m/s RMS vibration isolation (A-09) | cross-population-conflict-resolutions | [THIN BASE — engineering convention; no disability-specific validation] |
| 500 m² threshold for retreat room | pain-ofs-built-environment-design | Tier 0 CANDIDATE — Co-1/Co-2 derived; pending higher-tier validation |
| 5 m entrance seating distance | pain-ofs-built-environment-design | Co-1/Co-2 derived; pending higher-tier validation |

---

## Correction: Architectural vs Engineering Authority (2026-03-30 03:55)

### Error in original classification

Section (a) incorrectly classified ~40 performance targets as "engineering holds primary specification authority." This conflated *execution dependency* with *specification authority*.

**Corrected principle:** Anything that is distinctly spatial in provision is architectural. Engineers support the execution of those spaces. Grab bars are a design intervention that happens to need structure. Sensory relief spaces are a design intervention that happens to involve acoustics and lighting. The architect specifies the performance target (RT60 ≤0.3 s, melanopic EDI ≥250, STC ≥50, NC-25, grab bar at 700 mm bilateral). The engineer designs the system to deliver it.

### What is genuinely engineering-determined

Only items where the engineer determines the *how* — not the *what*:
- Duct routing, velocity, lining selection (to achieve architect-specified NC-25)
- Plant room configuration, vibration isolation system design (to achieve architect-specified <0.1 m/s RMS)
- Hearing loop layout geometry, driver specification (to achieve architect-specified IEC 60118-4 field strength)
- Structural load path for grab bar blocking (to achieve architect-specified ≥200 kg SWL)
- Drainage fall calculations, channel design (to achieve architect-specified zero-threshold)
- Luminaire selection, driver specification (to achieve architect-specified melanopic EDI, flicker %, CCT)
- Filtration system selection (to achieve architect-specified MERV 13 / TVOC target)

These are means, not ends. The architect specifies the end; the engineer specifies the means.

### Corrected GAP-SCOPE-01

**Original:** "Part 4/Part 8 engineering value duplication — ~40 measurable performance targets duplicated between item specs and engineering briefs."

**Corrected:** Part 4 is the single specification source for all performance targets. Part 8 is a coordination register identifying which engineering briefs must carry the architect's specification for delivery. The deduplication direction is: Part 4 holds the value; Part 8 cross-references it with the discipline, stage, and commissioning test. Where Part 8 currently restates a Part 4 value, replace with a cross-reference. Where Part 4 and Part 8 values contradict (e.g., A-03 STC ≥35 in Part 4 vs STC ≥50 in Part 8), Part 4 governs; Part 8 is corrected to match.

### Items removed from engineering column

All grab bar specifications, sensory room specifications, bathroom layout specifications, lighting performance targets, acoustic performance targets, air quality targets, thermal targets — these are architectural specifications. They remain in Part 4 as the architect's specification. Part 8 maps them to engineering briefs for delivery coordination.

### What remains in section (a) — correctly scoped

Only genuine engineering *system design* decisions that the architect cannot specify:
- Loop field geometry (AC + EE determine layout to achieve IEC 60118-4)
- HVAC system configuration (ME determines ductwork, plant, dampers to achieve NC/VOC/thermal targets)
- Structural detailing (SE determines blocking method, connection type, reinforcement for grab bar/hoist loads)
- Fire alarm circuit design (EE determines circuit topology for independent VAD activation)
- BMS programming (EE determines control logic for automated CCT shift, zone control)

These are Part 8 scope — the engineer's design decisions in response to the architect's performance specification.
