## Part 8: Engineering and Coordination

<!-- evidence_density: Moderate -->
> **Evidence density: ▓ Moderate** — Engineering performance targets (RT60, STI, NC-25, STC, melanopic EDI ≥250, MERV 13+) are derived from Part 4 specifications and their underlying BPC evidence. Part 8 is a coordination register and engineering brief framework, not an independent evidence source. Engineering coordination protocol and stage-gating are procedural (expert consensus + professional practice standards). VE Protection Register items are supported by verified retrofit cost multipliers (TERRAGON/DStGB 2017 Tier 3; RHF 2023).


<!-- v10.0 scaffold — CO-0004: was Part 9. Section numbering renumbered §9.x → §8.x (B2.2 2026-05-03).
     PENDING:
     - §8.1.4: Write TC-02+TC-03 combined item (Thermal Envelope and Mass — Passive Thermal Performance)
       Cross-reference F-07 and F-08. Source: ms-thermal-temperature-conflict-resolution BPC.
     - All §8.x internal references updated to §8.x
     - Part 8 cross-references → Part 8 -->


---

## 8.0 Overview and Operating Principle

### 8.0.1 Purpose

Part 8 provides the coordination interface between the architect and the engineering consultancy team for accessibility provisions in the design library. It performs two functions:

1. **Engineering Coordination Register** — a cross-reference identifying every design library item whose delivery depends on input from at least one engineering discipline, with the discipline, delivery stage, and document home.
2. **Consultant Brief Templates** — minimum specification language for insertion into each engineering consultant's scope of services, structured by discipline and design stage.

**Scope boundary.** Part 8 covers four engineering disciplines — Acoustic (AC), Mechanical (ME), Electrical (EE), and Structural (SE). Plumbing is addressed within the ME scope. Items that are purely spatial, material, or product-selection decisions — delivered solely through the architect's construction specification or finishes schedule — are excluded from this Part. Their absence does not reduce their importance; it means the architect holds sole responsibility for their delivery without engineering coordination.

Part 8 is not a substitute for engineering design. It is the architect's instrument for ensuring that accessibility requirements are activated within each consultant's scope at the right stage. An accessibility provision that appears only in the architect's specification but is absent from the relevant consultant's brief is not specified — it is a wish.

### 8.0.2 Engineering Coordination Doctrine

**This guidebook treats parallel specification as mandatory.** Every engineering-dependent accessibility item must appear in two documents simultaneously: the architect's construction specification or room data sheet, and the relevant consultant's brief at the appropriate design stage. Failure at either location is a coordination failure.

**Stage sequencing is non-negotiable.** Several items are irreversible once past schematic design. These are flagged NOT-RETROFITTABLE in the tables below. No value engineering, scope reduction, or programme pressure justifies deferring these items past their declared stage gate.

**Ready for Occupancy is specification.** A specification without a commissioning test is aspirational. Every engineering item with a measurable performance target carries a commissioning requirement, to be included in the commissioning schedule issued at technical design stage.

### 8.0.3 Engineering Disciplines in This Part

| Code | Discipline | Scope in this Part |
|---|---|---|
| **AC** | Acoustic Engineer | Noise criteria, RT60, STI, partition STC, hearing loop layout and performance |
| **EE** | Electrical Engineer | Lighting circuits, fire alarm, hearing loop wiring, power for controls and assistive technology, BMS |
| **ME** | Mechanical Engineer | HVAC, ventilation, vibration isolation, thermal zone control, TMV, underfloor heating, plumbing drainage infrastructure |
| **SE** | Structural Engineer | Lift shaft, grab bar blocking, hoist track, floating plant room, floor recess, refuge enclosure — §8.5 |

---

## 8.1 Engineering Coordination Register

### 8.1.1 How to Read This Register

The register identifies design library items (Part 7, Categories A–J) that require a brief instruction to at least one engineering consultant. Items with no such dependency are excluded.

**An item is engineering-dependent only if its performance cannot be achieved without a brief instruction to at least one engineering consultant.** Spatial, material, and product-selection items remain the architect's sole responsibility and are excluded even if they carry structural or cost implications.

**Column definitions:**

- **Item** — Part 7 item code and short title
- **Discipline(s)** — consultants requiring a brief instruction; multiple entries mean the item must appear in multiple briefs
- **Earliest Brief Stage** — when this item must enter the consultant's brief; later issue means the provision is lost or retrofit cost multiplies
- **NOT-RETROFITTABLE** — item cannot be incorporated after this stage without major engineering works
- **Ready for Occupancy Test** — measurable performance test required post-installation
- **Architect Document Home** — primary architect document specifying this item (in addition to the consultant brief)

**Stage abbreviations:** SD = Schematic Design · DD = Design Development · CD = Construction Documents · RFO = Ready for Occupancy

---

### 8.1.2 Acoustic Engineering Items

| Item | Title | Discipline(s) | Earliest Brief Stage | NOT-RETROFITTABLE | Ready for Occupancy Test | Architect Doc Home |
|---|---|---|---|---|---|---|
| A-01 | Acoustic Buffer Zones at Noisy Adjacencies | AC | SD | ⚠ YES — NC-25 target must be confirmed achievable before SD closes; adjacency cannot be resolved at later stages without room relocation | NC-25 in sensitive spaces post-completion | Room adjacency plan; acoustic strategy |
| A-02 | Acoustic Ceiling Panels (NRC ≥0.85) | AC | DD | No | RT60 at 500 Hz in occupied condition | Finishes specification |
| A-03 | Sound Transmission Class (STC ≥50) at Sensitive Partitions | AC | DD | Partial — partition type must be confirmed at DD | STC measurement at sensitive boundaries pre-completion | Partition schedule |
| A-05 | Acoustic Wall Panels and Bass Trapping | AC | DD | No | RT60 post-installation | Finishes specification |
| A-06 | Acoustic Wall Panels — Mid-Frequency Treatment | AC | DD | No | RT60 at 500 Hz | Finishes specification |
| A-08 | HVAC Noise Control (NC-25 in Sensitive Spaces) | AC, ME | SD | ⚠ YES — plant room location and duct routing are schematic decisions; cannot be resolved by ductwork modification at later stages | NC-25 at all air terminals in sensitive spaces; NC-30 in general occupied spaces | Acoustic strategy; ME brief |
| A-09 | HVAC Vibration Isolation (Floating Plant Room) | AC, ME, SE | SD | ⚠ YES — floating slab and isolation specification are schematic decisions. SE scope: §8.5. | Vibration at sensitive space floors <0.1 m/s RMS | Acoustic strategy; ME brief |
| A-10 | Counter Hearing Loop | AC, EE | DD | No | IEC 60118-4 field strength throughout counter loop area | EE brief; loop layout drawing |
| A-11 | Room Hearing Loop | AC, EE | DD | No | IEC 60118-4 field strength across full room area | EE brief; loop layout drawing |
| A-12 | Sound Field System (Classroom / Assembly) | AC, EE | DD | No | STI ≥0.7; coverage uniformity | EE brief; AV schedule |
| A-13 | Reverberation Time Control (RT60 ≤0.4 s) | AC | DD | No | RT60 at 500 Hz in occupied condition | Acoustic strategy |
| A-14 | Speech Privacy (STC ≥50 at Clinical Partitions) | AC | DD | Partial — partition type confirmed at DD | Privacy index measurement | Partition schedule |
| A-16 | Sensory Room (Multi-Sensory Environment) | AC, ME, EE | SD | ⚠ YES — room location and adjacency are schematic decisions; NC-25 requires HVAC to be coordinated from SD | NC-25; RT60 ≤0.4 s; lighting commissioning | Room data sheet |
| A-17 | Background Noise Control (Open-Plan Office, NC-30) | AC, ME | DD | No | NC-30 at workstations | Acoustic strategy; ME brief |

*Items A-07 (flutter echo — geometry/material) and A-15 (tactile warning surfaces — product specification) have no engineering dependency and are excluded.*

**Coordination note — A-08/A-09:** Both items must enter the ME and AC briefs simultaneously at schematic design. HVAC plant room location determines vibration transmission path. Both are irreversible once the structural slab is poured.

---

### 8.1.3 Electrical Engineering Items

| Item | Title | Discipline(s) | Earliest Brief Stage | NOT-RETROFITTABLE | Ready for Occupancy Test | Architect Doc Home |
|---|---|---|---|---|---|---|
| A-04 | Acoustic Paging System (DEM) | EE | DD | No | STI ≥0.5 | EE brief; electrical schedule |
| B-01 | Circadian Lighting Strategy (Variable CCT 2700–5500 K) | EE | DD | No | CCT and EML at eye level across 24-hour cycle; EML ≥200 at 09:00; CCT ≤2700 K at 19:00 | Lighting specification; BMS brief |
| B-02 | High-CRI Luminaires (CRI ≥90, R9 ≥50) | EE | DD | No | CRI at all task surfaces | Lighting specification |
| B-03 | Elimination of Fluorescent Lighting | EE | DD | No | IEEE 1789-2015 compliance certificate for all luminaires at handover | Lighting specification |
| B-04 | Flicker-Free LED (IEEE 1789-2015 Compliant) | EE | DD | No | Flicker % <5% at all dimming levels including 20% output | Lighting specification |
| B-05 | Gradual Lighting Transition Zones (≥3–5 m) | EE | DD | No | No illuminance step change >10:1 over <1 m across transition zone | Lighting specification; circuit zoning diagram |
| B-06 | Individual Dimming Control (≥300 Lux Range) | EE | DD | No | 10 lux minimum to full output; response time <1 s | Electrical schedule; BMS brief |
| B-07 | Indirect/Uplighting (Glare Control, UGR <19) | EE | DD | No | UGR measurement per CIE 117 | Lighting specification |
| B-08 | Task Lighting (≥500 Lux at Task Surfaces) | EE | DD | No | Illuminance at task plane | Lighting specification |
| B-09 | Maximisation of Natural Light — Supplementary Electric in Transition Zones | EE | DD | No | ≥150 lux in transition zone under overcast reference condition | Lighting strategy |
| B-10 | Visual Fire Alarm (Strobe VAD, BS EN 54-23 Category W) | EE | DD | No | Full EN 54-23 coverage; flash rate 1–3 Hz; intensity ≥75 cd; independent activation from audio circuit | EE brief; fire alarm schedule |
| B-11 | Warm Colour Temperature for Evening (≤2700 K after 19:00) | EE | DD | No | Automated CCT shift at 19:00 confirmed; manual override function | BMS brief; lighting specification |
| D-09 | Multi-Modal Wayfinding — Audio Beacon Power Provision | EE | DD | No | Power at each declared beacon node | EE brief; signage schedule |
| D-11 | Secured Outdoor Loop Path — Gate Operation and Lighting | EE | SD | No | Gate operation; external lighting ≥50 lux on path | Site plan; EE brief |
| E-01 | Accessible Lift — Power, Controls, Announcement System | EE | SD | ⚠ YES — shaft location is schematic. SE scope: §8.5. | Load test; door force ≤22 N; travel time; floor announcement audible and visible | EE brief |
| E-04 | Accessible Parking — External Lighting | EE | SD | No | Illuminance ≥50 lux at bay surface | Site plan; EE brief |
| E-11 | Automatic Door (Low-Energy Operator, ≤22 N) | EE | DD | No | Door force ≤22 N; activation zone function test | EE brief; door schedule |
| E-12 | Emergency Evacuation — Evacuation Lift Power, Intercom, UPS | EE | SD | ⚠ YES — refuge locations are schematic decisions. SE scope: §8.5. | UPS 2-hour endurance test; refuge intercom function | EE brief |
| G-04 | Height-Adjustable Worksurface *(electric models only)* | EE | DD | No | Full adjustment range; power at each unit confirmed | Furniture schedule; EE brief |
| G-05 | Height-Adjustable Seating and Desks *(electric models only)* | EE | DD | No | Adjustment range; power confirmed | Furniture schedule; EE brief |
| H-01 | Accessible Controls (400–1100 mm AFF, All Operated Surfaces) | EE | CD | No | Height measurement at all electrical devices | EE brief; electrical schedule |
| H-02 | Individual Environmental Control (Lighting, HVAC, Blinds) | EE, ME | DD | No | Full function from accessible control position; response <1 s | EE brief; ME brief; BMS brief |
| H-03 | Visual Paging and CART Captioning | EE | DD | No | Visual coverage; CART accuracy ≥98% for prepared speech | EE brief; AV schedule |
| H-04 | Accessible Intercom and Video Door Entry | EE | DD | No | Full intercom function; BMS remote door release confirmed | EE brief; door schedule |
| H-05 | Nurse Call / Emergency Pull Cord | EE | DD | No | Response within 3 s from all cord positions; audible and visual confirmation | EE brief; electrical schedule |
| H-06 | Assistive Technology Infrastructure (Conduit + Power Provision) | EE | DD | No | Continuity on all conduit runs; power at each provision point | EE brief; DAR register |
| I-05 | Hoist and Ceiling Track — Motor Power | EE | CD | ⚠ YES — structural track provision: ×20–40 retrofit. SE scope: §8.5. | Power at each track point; motor function | EE brief |
| I-06 | Kitchen for UPL Users — Power at Accessible Height *(assisted living / residential care)* | EE | DD | No | Power at accessible height; knee clearance under hob confirmed | EE brief; room data sheet |

*Note on B-09:* Structural openings for clerestories and rooflights are SE items — §8.5. The EE scope here is limited to supplementary electric lighting in daylit transition zones.

*Note on B-10:* Visual fire alarms must be on an independent circuit from the audio alarm system. State this explicitly in the EE brief. The common failure mode is a single circuit that defaults to audio-only when the VAD is isolated.

*Note on G-04/G-05:* Manual height-adjustable furniture requires no EE coordination. Power provision applies to electric models only.

---

### 8.1.4 Mechanical Engineering Items

| Item | Title | Discipline(s) | Earliest Brief Stage | NOT-RETROFITTABLE | Ready for Occupancy Test | Architect Doc Home |
|---|---|---|---|---|---|---|
| A-08 | HVAC Noise Control (NC-25 in Sensitive Spaces) | ME, AC | SD | ⚠ YES — see §8.1.2 | NC-25 at all air terminals; NC-30 general | Acoustic strategy; ME brief |
| A-09 | HVAC Vibration Isolation (Floating Plant Room) | ME, AC, SE | SD | ⚠ YES — see §8.1.2 | Vibration <0.1 m/s RMS at sensitive space floors | ME brief |
| A-16 | Sensory Room — HVAC Supply | ME, AC, EE | SD | ⚠ YES — see §8.1.2 | NC-25 in sensory room | Room data sheet |
| A-17 | Background Noise Control (Open-Plan Office, NC-30) | ME, AC | DD | No | NC-30 at workstations | ME brief |
| E-06 | Level Entry (Zero Step Threshold) — Threshold Drainage | ME | SD | ⚠ YES — floor levels and drainage route are schematic decisions. SE structural threshold detail: §8.5. | No ponding at threshold under 50 mm/hr rainfall simulation | ME brief |
| E-12 | Emergency Evacuation — Stairwell Pressurisation | ME | SD | ⚠ YES — see §8.1.3 | Pressure differential per fire engineer's brief | ME brief |
| F-01 | Sensory Gradient Strategy — Zone Ventilation | ME, AC | SD | ⚠ YES — zone locations must be confirmed at SD; ventilation design follows from zone arrangement | NC-25 in low-stimulation zones | Room adjacency plan; ME brief |
| F-02 | Fragrance-Free Zone — Dedicated Ventilation | ME | DD | No | VOC <0.1 mg/m³; no shared recirculation confirmed | ME brief; FM brief |
| F-03 | Sensory Retreat — Mechanical Supply | ME, AC, EE | SD | ⚠ YES — location is schematic | NC-25; RT60 ≤0.4 s; lighting 50–200 lux achievable | Room data sheet |
| F-04 | Sensory Activity Zone — Independent Ventilation | ME, AC | SD | ⚠ YES — adjacency is schematic | STC ≥50 at perimeter partitions; independent ventilation confirmed | Room adjacency plan |
| F-05 | Olfactory / VOC Control — Mechanical Ventilation | ME | DD | No | CO₂ <800 ppm; VOC <0.1 mg/m³ at supply | ME brief; FM brief |
| F-07 | Acoustic Zone Separation — HVAC Duct Cross-Talk | ME, AC | DD | No | NC-25 maintained in sensitive zone; no duct cross-talk between zones | ME brief; acoustic strategy |
| H-02 | Individual Environmental Control — HVAC Zone | ME, EE | DD | No | 18–22°C range independently achievable per zone; accessible control confirmed | ME brief |
| I-03 | TMV (Thermostatic Mixing Valve, ≤38°C at Outlet) | ME | DD | No | ≤38°C at all outlets under all flow conditions; annual service in FM brief | ME brief |
| I-04 | Accessible Bathroom — Drainage Channel and Floor Drain | ME | SD | ⚠ YES — drainage route and slab recess are schematic. SE floor recess: §8.5. | No pooling at threshold; drainage test | ME brief |

*Items F-06 (tactile flooring zoning — product specification) and the spatial aspects of F-01/F-03/F-04 are architect-specified; only the mechanical ventilation and acoustic requirements are addressed here.*

---

## 8.2 Engineering Brief Templates

*Quick-reference: use when drafting or reviewing each consultant's brief.*

### 8.2.1 Acoustic Engineer

The acoustic brief must be issued before ME ductwork design and EE ceiling/lighting design are finalised. Both affect acoustic outcomes and cannot be adjusted once committed.

| Item | Core Requirement | Stage | Performance Target | Ready for Occupancy |
|---|---|---|---|---|
| A-01 | Confirm that proposed room adjacency achieves NC-25 in sensitive spaces; identify any adjacency that cannot achieve target and propose resolution before SD sign-off | SD | NC-25 achievable confirmed | NC post-completion |
| A-02 | Confirm NRC ≥0.85 achievable with architect's ceiling system; coverage ≥80% of ceiling area | DD | NRC ≥0.85; RT60 achievable | RT60 at 500 Hz |
| A-03/A-14 | Confirm STC ≥50 achievable with specified partition types at all sensitive boundaries; issue STC-rated partition schedule | DD | STC ≥50 at sensitive boundaries | STC measurement pre-completion |
| A-05/A-06 | Confirm wall treatment achieves target RT60 in combination with ceiling and floor specification | DD | RT60 per brief (clinical ≤0.4 s; general per project brief) | RT60 post-installation |
| A-08 | Issue NC-25 limit to ME as a primary plant selection constraint before ME commences ductwork design; confirm ME's plant and ductwork meets target before DD closes | SD | NC-25 in ME design confirmed | NC at all air terminals |
| A-09 | Confirm vibration isolation specification with ME achieves <0.1 m/s RMS at sensitive space floors | SD | <0.1 m/s RMS | Vibration measurement |
| A-10/A-11 | Provide loop layout for all room and counter hearing loops; confirm no architectural or structural interference with loop field; confirm no loop-to-loop interference between adjacent rooms | DD | IEC 60118-4 field strength throughout | IEC 60118-4 measurement at commissioning |
| A-12/A-13 | Confirm RT60 ≤0.4 s and STI ≥0.7 achievable with proposed ceiling and wall treatment; confirm sound field system layout with EE | DD | RT60 ≤0.4 s; STI ≥0.7 | RT60 and STI post-installation |
| A-16 | Confirm sensory room achieves NC-25 and RT60 ≤0.4 s with specified finishes and HVAC supply; no vibration from adjacent plant | SD | NC-25; RT60 ≤0.4 s | NC and RT60 |
| A-17 | Confirm NC-30 achievable with HVAC design and ceiling specification; confirm speech privacy index ≥0.5 between adjacent workstations | DD | NC-30; privacy index ≥0.5 | NC and privacy index |
| F-01/F-07 | Confirm acoustic targets per sensory zone are achievable; identify any HVAC duct path transmitting noise between zones | SD/DD | NC-25 in low-stimulation zones | NC measurement per zone |

**AC brief standard clause:**
> *The acoustic performance targets in this brief are primary design constraints, not post-design adjustments. NC-25 in sensitive spaces and NC-30 in general occupied spaces are plant selection and ductwork design constraints to be issued to the mechanical engineer before plant selection commences. RT60 targets are ceiling and wall treatment design constraints to be confirmed before the finishes specification is issued. All performance targets are commissioning requirements.*

---

### 8.2.2 Electrical Engineer

#### Lighting

| Item | Core Requirement | Stage | Performance Target | Ready for Occupancy |
|---|---|---|---|---|
| B-01 | Tunable white luminaires (2700–5500 K) in all primary spaces where DEM, NDV/MH, NEU, or OFS users are primary occupants; BMS-automated schedule with manual override | DD | EML ≥200 at 09:00; CCT ≤2700 K at 19:00 | CCT and EML at eye level over 24-hour cycle |
| B-02 | All luminaires CRI ≥90, R9 ≥50 throughout building | DD | CRI ≥90 at all task surfaces | CRI measurement |
| B-03 | Zero fluorescent luminaires; IEEE 1789-2015 compliance confirmed for all drivers | DD | No fluorescent luminaire installed; IEEE 1789 certificates at handover | Certificate audit |
| B-04 | All LED drivers IEEE 1789-2015 low-risk compliant; flicker % <5% at all dimming levels including 20% output | DD | Flicker % <5% at 20% and 100% output | Flicker measurement |
| B-05 | Dedicated lighting circuits at all illuminance transition zones; ramp gradient across ≥3 m | DD | No step change >10:1 over <1 m | Gradient measurement at each transition |
| B-06 | Occupant dimmer in all spaces where NDV, DEM, PCS, PAIN, or OFS users are primary occupants: 10 lux minimum to full output; 900–1100 mm AFF; response <1 s | DD | 10 lux minimum achievable | Range and response test |
| B-07 | Indirect or uplighting as primary luminaire type in sensitive spaces; UGR <19; no bare lamp visible at normal viewing angle | DD | UGR <19 | UGR measurement per CIE 117 |
| B-08 | Task lighting ≥500 lux at work surfaces; independently switched from ambient | DD | ≥500 lux at task plane | Illuminance measurement |
| B-09 | Supplementary electric lighting in daylit transition zones: ≥150 lux under overcast conditions | DD | ≥150 lux at overcast reference | Illuminance at overcast condition |
| B-10 | VAD on independent circuit from audio alarm; BS EN 54-23 Category W; all occupied spaces including sleeping areas, bathrooms, meeting rooms, and public assembly areas; 75 cd minimum; 1–3 Hz | DD | Full EN 54-23 coverage; independent activation confirmed | Coverage test; independent activation test |
| B-11 | BMS-automated CCT shift ≤2700 K at 19:00 in DEM, NEU, and NDV/MH spaces; manual override available | DD | Automated shift at 19:00 confirmed | Automated shift test; override test |

#### Controls, BMS, and Assistive Technology

| Item | Core Requirement | Stage | Performance Target | Ready for Occupancy |
|---|---|---|---|---|
| H-01 | All electrical devices 400–1100 mm AFF; forward reach clear of obstruction within 600 mm; confirm heights with architect's partition layout before CD | CD | All devices within 400–1100 mm AFF | Height measurement at each device |
| H-02 | BMS: occupant control of lighting level, CCT, HVAC zone, and motorised blinds from 900–1100 mm AFF; response <1 s | DD | Full function from accessible control position | Function test per room |
| H-03 | Visual paging coverage throughout building; CART display units at all assembly and meeting spaces | DD | Full visual coverage; CART accuracy ≥98% for prepared speech | Coverage and CART accuracy test |
| H-04 | Video intercom: display ≥100 mm; tactile feedback on button press; button ≥30 mm; 900–1100 mm AFF; BMS remote door release from primary habitable room | DD | Full function; BMS remote release confirmed | Full function test |
| H-05 | Nurse call / pull cord: 900–1000 mm AFF with lower cord at 100 mm AFF; audible and visual response at call point and remote station within 3 s | DD | Response within 3 s | Pull test all positions; response time |
| H-06 | DAR conduit: 32 mm conduit from consumer unit to accessible height chase in each primary room; power provision point 900–1100 mm AFF for future assistive technology | DD | Continuity on all runs; power at each provision point | Continuity and power test |
| D-09 | Low-voltage power supply at each declared BLE beacon wayfinding node | DD | Power at each node | Power confirmation |
| G-04/G-05 | Power provision at each electrically adjustable furniture location | DD | Power confirmed at each location | Power confirmation |
| I-05 | Power to hoist motor at each ceiling track provision point | CD | Power confirmed at each point | Power and function test |
| I-06 | Power outlets at accessible height; knee clearance confirmed under accessible hob | DD | Power at accessible height | Height and clearance measurement |

#### Fire and Life Safety

| Item | Core Requirement | Stage | Performance Target | Ready for Occupancy |
|---|---|---|---|---|
| B-10 | VAD independent circuit — see lighting table | DD | Independent activation | Independent activation test |
| E-01 | Lift power supply; controls; audible and visual floor announcement system | SD | Full lift function; announcement audible and visible | Load and function test |
| E-12 | Evacuation lift: independent power circuit; UPS ≥2-hour operation; two-way voice intercom between lift and fire command point | SD | UPS endurance 2 hours; intercom function confirmed | UPS test; intercom test |
| A-10/A-11 | Hearing loop circuit: dedicated circuit from distribution board; IEC 60118-4 field strength −3 to +3 dBPa across loop area; driver accessible for commissioning test | DD | IEC 60118-4 throughout loop area | Field strength measurement |

**EE brief standard clause:**
> *Electrical systems in this project are to be designed with accessibility as a primary performance requirement across four sub-systems: lighting quality, controls and BMS, fire and life safety, and assistive technology infrastructure. The following items are on the VE protection register and cannot be substituted without written design team approval: IEEE 1789-2015 lighting specification; IEC 60118-4 hearing loop specification; visual fire alarm independent circuit. Substitution requests must include performance equivalence evidence against the declared target.*

---

### 8.2.3 Mechanical Engineer

| Item | Core Requirement | Stage | Performance Target | Ready for Occupancy |
|---|---|---|---|---|
| A-08 | HVAC to achieve NC-25 in sensitive spaces; NC-30 in all other occupied spaces. Duct velocity ≤3 m/s at primary distribution. Acoustic lining to supply ducts ≥10 m from AHU | SD/DD | NC-25 sensitive; NC-30 general | NC at all air terminals post-commissioning |
| A-09 | Rotating plant on vibration isolation pads ≥20 dB insertion loss at 16–250 Hz. Floating plant room where adjacent to sensitive spaces (SE co-ordination per §8.5). Flexible connections at all pipe and duct connections to mechanical plant | SD | <0.1 m/s RMS at sensitive space floors | Vibration measurement |
| A-16 | HVAC supply to sensory room to achieve NC-25; no shared return air with noisy adjacencies | SD | NC-25 | NC measurement |
| A-17 | HVAC to achieve NC-30 in open-plan office spaces | DD | NC-30 | NC measurement |
| E-06 | Drainage at level threshold: channel design to prevent ponding; coordinate with structural slab recess (§8.5) | SD | Zero ponding at threshold | Water test |
| E-12 | Stairwell pressurisation at evacuation lift lobbies and refuge enclosures per fire engineer's strategy | SD | Pressure differential per fire strategy | Pressurisation test |
| F-01 | Sensory zone ventilation: NC-25 in low-stimulation zones; independently controllable ventilation per zone | SD | NC-25 in low-stimulation zones | NC measurement per zone |
| F-02 | Dedicated ventilation supply to fragrance-free zones; no shared recirculation with zones where scented products are used | DD | VOC <0.1 mg/m³; ACH confirmed | Air sampling |
| F-04 | Independent ventilation circuit for sensory activity zone; dampers at zone boundaries | SD | No cross-contamination to adjacent zones | Duct isolation confirmed |
| F-05 | CO₂ <800 ppm in all occupied spaces; VOC <0.1 mg/m³ at supply air | DD | CO₂ and VOC targets | Air quality post-commissioning |
| F-07 | No HVAC duct cross-talk between sensory zones; dampers at zone boundaries | DD | NC-25 maintained in sensitive zones | NC measurement |
| H-02 | Individual HVAC zone control accessible from 900–1100 mm AFF; each zone independently operable | DD | 18–22°C range per zone | Temperature test per zone |
| I-03 | TMV at all patient/resident bathrooms and WCs: ≤38°C at outlet. ≤35°C where NEU users are primary occupants. Annual service to be in FM brief | DD | ≤38°C at all outlets under all flow conditions | Temperature test at all outlets |
| I-04 | Floor drain and drainage channel for zero-threshold shower; slab recess coordination with SE (§8.5) | SD | No pooling at threshold | Drainage test |

**ME brief standard clause:**
> *Mechanical systems in this project are to be designed with the following accessibility constraints as primary performance requirements. HVAC acoustic targets — NC-25 in sensitive spaces, NC-30 in general occupied spaces — are plant selection and ductwork design constraints, not commissioning adjustment targets. These criteria must be met by design. Vibration isolation to sensitive spaces is to be resolved jointly with the structural engineer at schematic design stage before the structural slab is finalised.*

---

## 8.3 Stage-Gated Coordination Protocol

### 8.3.1 Schematic Design Gate

The following items must be confirmed — in writing and on named drawings — before schematic design is signed off. Items not confirmed at SD are to be recorded in the project risk register with the retrofit cost multiplier stated.

| Item | Confirmation Required at SD | Discipline | If Missed |
|---|---|---|---|
| E-01 | Lift power supply strategy confirmed; shaft location fixed | EE (power); SE (shaft — §8.5) | ×50+ |
| E-06 | Threshold drainage design initiated; slab level confirmed | ME; SE (§8.5) | Not retrofittable |
| E-12 | Evacuation lift power and pressurisation strategy confirmed | EE; ME | Significant structural/engineering intervention |
| A-08 | Plant room location confirmed; NC-25 path modelled by AC | ME; AC | ×5–10 ductwork retrofit |
| A-09 | Vibration isolation specification issued to SE | ME; AC | Not retrofittable |
| A-16 | Sensory room HVAC and acoustic feasibility confirmed | ME; AC; EE | ×3–6 room relocation |
| F-01 | Sensory zone ventilation strategy confirmed | ME; AC | ×3–6 zone relocation |
| F-03 | Sensory retreat mechanical and electrical feasibility confirmed | ME; AC; EE | ×3–6 |
| F-04 | High-stimulation zone containment strategy confirmed | AC; ME | ×3–6 |
| I-04 | Floor drainage channel route confirmed; slab recess initiated with SE | ME | ×20–40 |

### 8.3.2 Technical Design Gate — Brief Issue

At technical design commencement, the architect is to issue updated consultant briefs incorporating all items from §8.2. The gate is not complete until:

- AC brief issued covering: A-01 through A-17 as applicable, F-01, F-04, F-07
- ME brief issued covering: A-08, A-09, A-16, A-17, E-06, E-12, F-01 through F-05, F-07, H-02, I-03, I-04
- EE brief issued covering: all B-category items, D-09, D-11, E-01, E-04, E-11, E-12, G-04/G-05, all H-category items, I-05, I-06
- SE brief issued covering: all items in §8.5

### 8.3.3 VE Protection Register

The following specifications are not to be value-engineered without written agreement of the lead architect. Issue to the contractor at Stage 3.

| Item | Protected Specification |
|---|---|
| A-08/A-09 | HVAC NC-25/NC-30 targets; vibration isolation <0.1 m/s RMS |
| A-10/A-11 | Hearing loop IEC 60118-4 compliance; commissioning field strength certificate |
| B-03/B-04 | IEEE 1789-2015 LED specification — no non-compliant driver or luminaire substitution |
| B-10 | Visual fire alarm independent circuit — no consolidation with audio alarm circuit |
| I-03 | TMV specification ≤38°C — no substitution with standard mixer tap |
| I-04 | Zero-threshold floor drainage — no substitution with raised threshold |
| I-05 | Ceiling hoist structural power provision — no deletion |

---

## 8.4 O&M Manual — Engineering Accessibility Systems

Include the following in the Operations and Maintenance manual in addition to standard engineering maintenance schedules.

| System | FM Requirement | Frequency |
|---|---|---|
| HVAC (A-08) | NC measurement in sensitive spaces | Annual |
| Vibration isolation (A-09) | Anti-vibration mount condition check | Annual |
| Hearing loops (A-10/A-11) | IEC 60118-4 performance test | Annual; after any electrical works in loop area |
| Visual fire alarms (B-10) | Flash rate and intensity verification | Monthly |
| Luminaires (B-03/B-04) | IEEE 1789 compliance confirmed at any lamp or driver replacement | At each replacement event |
| TMV (I-03) | Temperature test at outlet; valve servicing per manufacturer | Annual minimum |
| Hoist power and track (I-05) | Load test; track and power continuity | Annual |
| BLE beacons (D-09) | Battery level; signal test | Quarterly |
| Fragrance-free protocol (F-02/F-05) | Cleaning product audit; ventilation ACH confirmed | Annual |
| Grab bar blocking (G-03) | Load-bearing condition check at all installed grab bars | Annual; after any wall repair in grab bar zone |

---

## 8.5 Structural Engineer Coordination

Structural engineering operates under a distinct scope from acoustic, mechanical, and electrical engineering. The items below are collected separately because structural accessibility provisions are among the highest-cost items to retrofit, are frequently missing from SE briefs, and must be confirmed on structural drawings — not only in the specification text. Structural drawings are the confirmation document; a specification entry without a corresponding structural drawing is not a structural commitment.

| Item | SE Requirement | Stage | Drawing Confirmation | If Missed |
|---|---|---|---|---|
| E-01 | Lift shaft: minimum internal clear dimensions per EN 81-70; designed to accommodate future full-passenger upgrade where platform lift is the interim measure | SD | Floor plans; structural drawings ⚠ | ×50+ |
| E-06 | Threshold structural detail: level threshold achievable at all principal entries; drainage slab recess coordinated with ME | SD | Section drawing ⚠ | Not retrofittable |
| E-12 | Refuge enclosure: fire-rated partition structural requirements at each stair core; evacuation lift shaft structural co-location | SD | Structural drawings ⚠ | Major structural intervention |
| A-09 | Floating plant room: floating concrete slab on spring isolators; structural separation from occupied floors; slab mass and isolator specification per ME requirements | SD | Structural drawings ⚠ | Not retrofittable |
| B-09 | Structural openings for clerestory, rooflight, or light well: lintel sizing, weatherproofing interface | SD | Structural drawings ⚠ | ×10 per opening |
| G-03 | Grab bar blocking: all bathrooms, shower rooms, WCs, and any space where future grab bar installation is anticipated. Rated load ≥1.5 kN point load per ISO 11199. Blocking extends 300 mm beyond anticipated grab bar positions on all four sides. Photographic record required before wall lining is applied. | CD | Structural/blocking drawings ⚠ | ×75 |
| I-04 | Zero-threshold shower floor recess: structural slab recess for drainage channel; recess depth coordinated with ME drainage design | SD | Structural/section drawings ⚠ | ×20–40 |
| I-05 | Ceiling hoist tracking: structural blocking or dedicated track support in all designated bedrooms and bathrooms; track layout confirmed with architect; minimum 800 kg dynamic load rating | CD | Structural drawings ⚠ | ×20–40 |

**SE brief standard clause:**
> *All structural provisions for accessibility are primary structural design requirements, not secondary modifications. DAR (Design for Adaptable Readiness) provisions are to be incorporated at the earliest stage. Published retrofit cost multipliers for structural accessibility provisions: grab bar blocking ×75; ceiling hoist tracking ×20–40; lift shaft ×50+ (Rick Hansen Foundation 2023; TERRAGON/DStGB 2017). These figures are to be cited in any value engineering discussion where structural accessibility provisions are challenged. No structural accessibility provision is to be removed from the design without the written agreement of the lead architect.*


---

## 8.6 DeafBlind (DBL) Specialist Consultant

### 8.6.1 When DBL Specialist Input Is Required

DeafBlind design provisions cannot be derived by combining DEAF specifications with VIS specifications. The compound impairment produces distinct spatial, navigational, and communication requirements — among them tactile communication protocols (Protactile, hand-under-hand, close-range signing) with specific spatial clearance demands that appear in neither the DEAF nor the VIS literature. A building intended to serve DBL occupants without DBL specialist input will produce environments calibrated to two single-category populations rather than to the compound DBL condition.

Engage a DBL specialist consultant when:

- The building serves a known DBL occupant in a residential or supported living context.
- The building is a DBL-serving institution (deafblind school, deafblind resource centre, combined-sensory loss unit within a healthcare setting).
- The building includes K-category items (K-01 through K-04) where DBL occupancy is a primary or secondary condition.
- Any specification for the building references Protactile design, tactile map provision, intervenor corridor width, or vibrotactile alerting for a non-fire-alarm purpose.

Where DBL occupancy is incidental (a DBL visitor to a general-purpose building), K-category items are specified from the item library without specialist input and represent population-informed best practice, not co-designed provision.

---

### 8.6.2 DBL Specialist Coordination Register

The following K-category items require DBL specialist input for their specification and delivery. The specialist's scope at each stage is noted.

| Item | Title | Specialist Stage | DBL Specialist Scope | If Specialist Absent |
|---|---|---|---|---|
| K-01 | DBL Intervenor Adjacency Zone | SD | Confirm intervenor zone position relative to primary occupant's habitual sitting and sleeping positions; confirm ≥1500 mm clear zone dimensions and furniture-free enforcement | Intervenor zone placed by architect without user-specific knowledge; likely undersized or obstructed |
| K-02 | Tactile Building Map Station | DD | Review map content for accuracy against building layout; confirm braille accuracy; review haptic symbology against DBL user's navigational vocabulary (not standardised internationally) | Map produced without DBL navigation review; likely contains inaccuracies that make it misleading rather than helpful |
| K-03 | Haptic Communication Clear Zone | SD | Identify all primary DBL occupant positions (classroom seat, dining position, workplace desk, therapy space); confirm clear floor zone dimensions (≥1200 × 1200 mm minimum; 1500 × 1500 mm preferred) are reflected in furniture plan | Zone dimensions unverified; DBL occupant cannot communicate via close-range tactile methods in their primary occupation positions |
| K-04 | Vibrotactile Alert Infrastructure | DD | Confirm alert event types and vibrotactile device locations relative to primary occupation positions; review BMS relay logic for DBL-specific alerting (doorbell, intercom, telephone, fire — four separate alert signatures); confirm device placement is within tactile reach of sleeping and primary occupation positions | Alert system covers fire only or covers all events with identical vibrotactile signatures (prevents pattern recognition) |

---

### 8.6.3 Novel Spatial Specifications Requiring DBL Specialist Verification

Five spatial specifications in the DBL evidence base have no equivalent in DEAF or VIS single-category guidance. Each requires DBL specialist verification before appearing in construction documents.

**Protactile communication clearance (≤600 mm face-to-face):** Protactile and hand-on-body communication requires participants to be within ≤600 mm of each other — a distance significantly closer than standard interpersonal interaction norms. Furniture layout, workstation spacing, and seating configurations in DBL primary spaces must accommodate ≤600 mm face-to-face positioning without obstruction. Standard open-plan workplace layouts (900–1200 mm desk centres) do not accommodate this. DBL specialist verifies: furniture plan permits ≤600 mm positioning at all primary DBL occupant workstations and communication positions.

**Close-range sign language clearance (接近手話: 500–1000 mm):** Japanese close-proximity signing (接近手話) and equivalent close-range tactile signing in other traditions requires 500–1000 mm lateral clearance at head and shoulder height, with no furniture or structural element obstructing the visual-tactile communication field at this range. DBL specialist verifies: no obstruction exists within the 500–1000 mm lateral field at sitting and standing head height for DBL occupants at primary communication positions.

**Intervenor accompaniment corridor width (≥1500 mm):** Nordic ledsagarservice (intervenor accompaniment) is a statutory support right for DBL persons in SE, NO, DK, and FI. The intervenor accompanies the DBL person in physical contact along all circulation routes. The minimum corridor width for single-file DBL + intervenor travel is 1500 mm clear. The 2400 mm DEAF signing-pair corridor width (E-08 best practice) accommodates this; the 1200 mm MOB minimum does not. DBL specialist verifies: all primary circulation routes on the DBL occupant's access path are ≥1500 mm clear with no pinch points below this width.

**Tactile building map accuracy:** K-02 tactile map content must accurately represent the building layout at a scale navigable by a person with no visual reference. Map accuracy errors — transposed room positions, omitted corridors, incorrect scale — produce navigational hazards rather than orientation aids. DBL specialist verifies: map content against confirmed floor plan before fabrication.

**Consistent spatial layout (no reconfiguration):** Spatial memory is the primary DBL navigational strategy in familiar environments. Any reconfiguration of furniture, equipment, or room function in a DBL primary space requires advance notification to the DBL occupant and, ideally, a tactile walkthrough with intervenor before the reconfiguration is occupied. This is an FM and operational requirement, not a construction requirement. DBL specialist provides: written FM protocol for spatial changes, including advance notice period (minimum five working days) and tactile walkthrough procedure.

---

### 8.6.4 DBL Specialist Brief Template

The following minimum scope language is to be inserted in the DBL specialist consultant's appointment letter and terms of reference:

> *The consultant is appointed to provide DeafBlind design advisory services for [project name]. The appointment covers: (1) review of K-category item specifications (K-01 through K-04) for compatibility with the DBL occupant's communication methods, navigational strategies, and spatial requirements; (2) verification of five novel spatial specifications as listed in Part 8 §8.6.3 of the Guidebook for Accessible Design; (3) attendance at design review meetings at schematic design and design development stages; (4) provision of a written design verification note at each stage confirming compliance or identifying required amendments; and (5) provision of an FM protocol document for spatial change management. The consultant's scope is advisory, not supervisory. Construction compliance remains with the architect and design team. The consultant's verification notes are project documents and are to be retained in the project record.*

---

### 8.6.5 DBL Specialist Stage Coordination

| Stage | DBL Specialist Action | Output |
|---|---|---|
| SD | Review floor plan for K-01 and K-03 zone dimensions; confirm intervenor corridor widths on primary circulation routes; flag any spatial configuration incompatible with ≤600 mm Protactile clearance | Written stage review note |
| DD | Review K-02 tactile map content against confirmed floor plan; review K-04 BMS relay brief for alert-event type coverage and device locations; review furniture plan for Protactile and close-range signing clearances | Written DD verification note |
| CD | Confirm tactile map fabrication specification; confirm K-04 device model and placement in electrical drawings | Signature on K-04 electrical specification |
| RFO (Ready for Occupancy) | Conduct tactile walkthrough of building with DBL occupant and intervenor; confirm K-02 map accuracy against built state; confirm K-04 alert-event coverage by system test | Signed RFO verification note |
| Post-occupancy | Provide FM spatial change protocol; advise on any DBL-specific issues identified in first 12 months of occupancy | FM protocol document |

---

*Evidence basis (DBL specialist section):* DbI World Access guidelines (Tier 2, international); Nordic ledsagarservice statutes (SE, NO, DK, FI — Tier 6 statutory); Protactile Movement literature (Clark; Nuccio & Granda — Co-1); ISO 23599:2019 applied to DBL context (Tier 4); Japanese 接近手話 practice (Tier 5). THIN-BASE disclosure: no Tier 1 OT clinical research on DBL-specific built environment spatial provisions has been identified in any language reviewed. All specifications derive from Tier 2–6 sources. See GAP-DBL-BE-01 for research gap disclosure.


### §8.1.4 Thermal Envelope and Mass — Passive Thermal Performance

<!-- CO-0004/CO-0003: TC-02 + TC-03 combined item. Previously in Appendix C (retired). Now in Part 8 Engineering and Coordination as an engineering coordination item. Cross-references: F-07 (Thermal Zoning — design brief); F-08 (Thermal Transition — system response). -->

**Engineering coordination item — Mechanical and Structural Engineers.**

Passive thermal performance of the building envelope and thermal mass determines the baseline ambient temperature stability that HVAC systems must maintain. For buildings serving NEU/MS (Uhthoff's), OFS, or PAIN populations, envelope performance directly affects patient and user safety.

**Coordination requirement.** The mechanical engineer's HVAC brief (§8.2.3) must state the thermal envelope performance targets required to achieve the F-07 ambient temperature specification (≤18°C primary activity spaces where NEU/MS is primary). The structural engineer must confirm thermal mass specification is compatible with the HVAC zoning strategy.

**Thermal Envelope (from TC-02):**
**Applicable Groups:** OFS, NEU, ALL **Specification:** U-value ≤0.15 W/m²K for external wall; windows triple-glazed (Uw ≤0.8 W/m²K); thermal bridges eliminated at structural connections. Internal surface temperature variation ≤2°C between floor and 1800 mm AFF in occupied spaces. **Clinical basis:** Temperature fluctuation triggers exertional response in OFS/MCAS and fatigue escalation in NEU. Thermal stability reduces physiological demand of building occupation. *Co-benefit: sustainability synergy — reduced heating/cooling load. See Part 11I §8.5.1.*

**Thermal Mass (from TC-03):**
**Applicable Groups:** OFS, NEU, ALL **Specification:** Exposed thermal mass (concrete, masonry, earth) in primary occupied spaces to moderate temperature swing. Target: ≤3°C diurnal internal temperature variation without active HVAC. **Clinical basis:** Passive thermal stability via thermal mass reduces dependency on active HVAC systems (which introduce acoustic noise: see A-08) while achieving thermal stability for NEU and OFS users. *Cross-reference: A-08 (HVAC noise — reduced dependency); TC-02 (envelope)*

**Cross-population coordination note:** High-performance envelope eliminates cold bridging that creates localised cold surfaces — a PAIN allodynia trigger. Thermal mass dampens daily temperature swing (target ≤3°C per F-08). Both provisions serve NEU/MS, OFS, PAIN, and DEM populations simultaneously with no specification conflict. See Part 5 §5.2 TEMP-RANGE for conflict resolution where PAIN and NEU/MS occupy the same space.

**Cross-references:** F-07 (Thermal Zoning); F-08 (Thermal Transition); Part 9 §9.1.4 (Mechanical Engineer brief); ms-thermal-temperature-conflict-resolution BPC.
