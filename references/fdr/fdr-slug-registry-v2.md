# FDR Research Slug Registry — Comprehensive v2
<!-- Supersedes §9 Priority Targets in functional-deficit-researcher_SKILL.md -->
<!-- Generated: 2026-04-09 04:25 -->
<!-- Informed by: framework-compound-functioning-review.md, existing FDR file audit, item category coverage, population code coverage -->

## Design Principles

1. **Functional scenario = search unit** — `{ICF-d code} + {functional constraint} → {environment context}` (unchanged from FDR skill §2).
2. **Compound scenarios added** — per framework review §4.4, new slug type: `{ICF-d code} + {constraint-A} + {constraint-B} → {environment}` where the functional interaction is non-additive. These are flagged `[COMPOUND]`.
3. **Occupation-level scenarios added** — per PEO/PEOP framework, new slug type: `{occupation} + {constraint cluster} → {environment}` where the search target is the whole-occupation performance, not a single activity code. These are flagged `[OCCUPATION]`.
4. **Environment-led scenarios added** — some spatial parameters are best searched by environment type, not by ICF code. These are flagged `[ENVIRONMENT]`.
5. **Each slug maps to exactly one FDR file** in `references/fdr/`.
6. **Priority:** P1 = immediate (next 3 sessions); P2 = soon (within 10 sessions); P3 = backlog.

---

## Status Key

| Status | Meaning |
|---|---|
| COMPLETE | All planned scenarios run; findings committed |
| PARTIAL | Some scenarios run; remaining listed |
| NOT-RUN | No scenarios executed yet |

---

## A. Existing FDR Files — Completion Status

| File slug | Status | Remaining scenarios |
|---|---|---|
| accessible-bathroom-and-grab-bar | COMPLETE | — |
| accessible-circulation-geometry | COMPLETE | — |
| accessible-laundry-room-design | PARTIAL | Fatigue-specific adjacency (OFS/PAIN) |
| bariatric-turning-radius-built-environment | COMPLETE | — |
| cognitive-wayfinding-design | COMPLETE | — |
| deaf-spatial-design | PARTIAL | Acoustic management for HA/CI users in reverberant spaces |
| deafblind-built-environment-design | PARTIAL | Emergency alerting (tactile-only evacuation) |
| dementia-built-environment | PARTIAL | Outdoor/return-home wayfinding; kitchen safety |
| fold-down-grab-bar-specification | COMPLETE | — |
| intellectual-disability-built-environment-design | COMPLETE | — |
| luminance-contrast-lrv-evidence-base | COMPLETE | — |
| mental-health-built-environment | COMPLETE | — |
| mobility-built-environment | COMPLETE | — |
| ms-thermal-temperature-conflict-resolution | COMPLETE | — |
| ndv-aut-built-environment-quantified-thresholds | COMPLETE | — |
| neurodivergent-built-environment | COMPLETE | — |
| neurological-built-environment | COMPLETE | — |
| ofs-built-environment | COMPLETE | — |
| pain-ofs-built-environment-design | COMPLETE | — |
| reach-range-and-accessible-controls | COMPLETE | — |
| residential-entry-and-threshold | COMPLETE | — |
| residential-kitchen-and-task-surfaces | COMPLETE | — |
| sensory-relief-space-design | PARTIAL | Hyposensitivity stimulation space; collectivist-context retreat |
| stair-ramp-threshold-biomechanics-accessibility | COMPLETE | — |
| threshold-door-hardware | COMPLETE | — |
| upper-limb-impairment-built-environment | COMPLETE | — |
| visual-fire-alarm-seizure-safety | COMPLETE | — |
| visual-impairment-built-environment | PARTIAL | Orientation/wayfinding interior spaces |
| wayfinding-dementia-spatial-design | COMPLETE | — |
| framework-compound-functioning-review | COMPLETE | (Framework review, not scenario-based) |

**PARTIAL files remaining work: 6 files, ~10 scenarios.**

---

## B. New Slugs — Granular Functional Scenarios (ICF-based)

### B.1 Bathroom / Wet Area Gaps

| ID | Scenario | ICF | Constraint | Environment | Target item codes | Priority | Rationale |
|---|---|---|---|---|---|---|---|
| FDR-NEW-01 | d510 + dementia → bath/shower recognition and sequence | d510 | cognitive sequencing deficit | bathroom | G-03, G-04, C-04 | P2 | DEM bathroom safety beyond contrast — task sequencing (soap/rinse order, temperature recognition) |
| FDR-NEW-02 | d530 + OFS/POTS → toileting with orthostatic intolerance | d530 | orthostatic hypotension | bathroom | G-05, G-06, I-03 | P1 | OFS toileting: positional blood pressure drop during sit-to-stand from low WC; grab bar + WC height interaction |
| FDR-NEW-03 | d510 + chronic pain → shower posture and duration | d510 | pain-limited standing tolerance | bathroom | G-03, G-04, I-03 | P2 | PAIN: shower seat specification driven by pain-limited standing; fatigue vs MOB rationale distinct |

### B.2 Kitchen Gaps

| ID | Scenario | ICF | Constraint | Environment | Target item codes | Priority | Rationale |
|---|---|---|---|---|---|---|---|
| FDR-NEW-04 | d630 + visual impairment → meal prep safety | d630 | absent/reduced vision | kitchen | H-01, H-02, C-04 | P1 | VIS kitchen: tactile differentiation of controls, hob safety (induction-only rationale), knife storage, hot surface indication |
| FDR-NEW-05 | d630 + dementia → kitchen safety and task completion | d630 | cognitive decline | kitchen | H-01, H-02, E-01 | P1 | DEM kitchen: gas vs induction, automatic shut-off, simplified controls, visible contents (glass-front cabinets) |
| FDR-NEW-06 | d550 + dysphagia/UPL → eating environment | d550 | swallowing + upper limb | dining | I-02, G-07 | P3 | Compound: table height for adaptive equipment, lighting for food visibility, non-slip surface |

### B.3 Bedroom Gaps

| ID | Scenario | ICF | Constraint | Environment | Target item codes | Priority | Rationale |
|---|---|---|---|---|---|---|---|
| FDR-NEW-07 | d540 + bilateral UPL → dressing (closet/storage) | d540 | bilateral upper limb | bedroom | G-07, H-01 | P2 | Closet geometry for bilateral UPL: pull-down rails, front-access drawers, motorised wardrobe systems; extends FDR-BAB-05 |
| FDR-NEW-08 | d570 + epilepsy → bedroom night safety | d570 | seizure risk | bedroom | B-10, F-04, G-07 | P2 | NEU/epilepsy: mattress at floor level option, padded furniture edges, seizure detection sensor placement, emergency alert |
| FDR-NEW-09 | d410 + OFS/ME → bed rising and positional management | d410 | post-exertional malaise, orthostatic | bedroom | G-07, I-03, H-02 | P1 | OFS: adjustable bed head elevation (manages POTS), staged rising protocol, bedside controls within supine reach |

### B.4 Entry / Circulation Gaps

| ID | Scenario | ICF | Constraint | Environment | Target item codes | Priority | Rationale |
|---|---|---|---|---|---|---|---|
| FDR-NEW-10 | d475 + wheelchair → vehicle-to-dwelling transition | d475 | wheelchair user | entrance/parking | E-01, E-05, D-09 | P2 | Transfer from vehicle to WC to entrance: covered transfer zone, level surface, charging point for power WC at entry |
| FDR-NEW-11 | d460 + deafblind → emergency evacuation route | d460 | combined VI + HI | circulation | F-04, D-06, E-08 | P1 | DBL evacuation: tactile evacuation signage, vibrotactile alarm, guidance rail continuity to exit — life safety gap |
| FDR-NEW-12 | d450 + ambulant with walking frame → door approach and manoeuvre | d450 | walking frame geometry | entrance/corridor | E-01, E-06, E-08 | P2 | Walking frame (rollator/Zimmer): approach clearance distinct from WC; door opening force while frame-dependent; threshold catch on frame wheels |

### B.5 Communication and Alerting Gaps

| ID | Scenario | ICF | Constraint | Environment | Target item codes | Priority | Rationale |
|---|---|---|---|---|---|---|---|
| FDR-NEW-13 | d310 + DEAF + dementia → communication in shared space | d310 | hearing loss + cognitive | common room | A-10, A-11, F-02 | P2 | Compound: hearing loop in space where DEM occupant cannot operate personal hearing device; fixed environmental provision required |
| FDR-NEW-14 | d310 + speech impairment (NEU) → intercom/entry communication | d310 | dysarthria/aphasia | entrance | F-02, H-05 | P2 | NEU: voice-based intercom inaccessible for dysarthric users; video + text alternative; AAC device compatibility |

### B.6 Controls and Technology Gaps

| ID | Scenario | ICF | Constraint | Environment | Target item codes | Priority | Rationale |
|---|---|---|---|---|---|---|---|
| FDR-NEW-15 | d440 + tremor (PD/MS/essential) → fine control operation | d440 | action tremor | all rooms | E-14, H-01, H-02 | P1 | Tremor: touchscreen inaccessible (mis-registration); toggle/rocker preferred; environmental control interface design |
| FDR-NEW-16 | d440 + tetraplegia (C4-C5) → environmental control unit interface | d440 | no hand function | all rooms | H-02, H-04, H-05 | P1 | ECU: sip-and-puff, eye-gaze, voice — spatial requirements (mounting, cable routing, backup power, switch access point at bed/WC/chair) |

### B.7 Sensory Environment Gaps

| ID | Scenario | ICF | Constraint | Environment | Target item codes | Priority | Rationale |
|---|---|---|---|---|---|---|---|
| FDR-NEW-17 | d710 + NDV/MH + PTSD → retreat space in non-residential | d710 | hypervigilance, sensory overwhelm | workplace/public | A-16, F-01, F-06 | P2 | Non-residential sensory retreat: different from residential (time-limited, shared, must allow return to activity); airport/hospital/office quiet room specification |
| FDR-NEW-18 | d230 + NDV/ADHD → routine management through spatial cues | d230 | executive function deficit | residential | D-05, C-04, B-01 | P3 | ADHD spatial cueing: visual task stations, colour-coded zones, clock/timer placement, reduced visual distraction in work zones |

---

## C. New Slugs — Compound Functioning Scenarios [COMPOUND]

These address the framework review finding that co-occurring conditions produce supra-additive functional impacts.

| ID | Scenario | Constraints | Environment | Priority | Rationale |
|---|---|---|---|---|---|
| FDR-CMP-01 | d420 + hemiplegia + chronic pain → transfer with pain avoidance | MOB + PAIN | bathroom/bedroom | P1 | Transfer technique modified by pain: avoidance of weight-bearing on affected side changes grab bar requirements; pain alters transfer sequencing |
| FDR-CMP-02 | d450 + visual impairment + fatigue → circulation with compound barrier | VIS + OFS | corridor/general | P1 | VIS navigation requires cognitive load (scanning, counting); fatigue reduces cognitive reserve; rest point specification must account for both simultaneously |
| FDR-CMP-03 | d630 + seated wheelchair + cognitive impairment → meal prep compound | MOB + DEM | kitchen | P2 | Seated wheelchair position + cognitive decline: reduced visibility of hob + reduced hazard awareness; spatial arrangement must compensate for both concurrently |
| FDR-CMP-04 | d460 + dementia + visual impairment → wayfinding with dual sensory-cognitive loss | DEM + VIS | circulation | P1 | Dual loss: tactile wayfinding (VIS) requires learning and memory that DEM impairs; DEM colour-coding (visual) inaccessible to VIS. What works when both fail? |
| FDR-CMP-05 | d540 + hemiplegia + shoulder pain → dressing with compound UL limitation | MOB + PAIN | bedroom | P2 | Hemiplegic dressing techniques require the unaffected arm to compensate; shoulder pain on the "good" side eliminates the compensatory mechanism. Closet/bench geometry must accommodate both |
| FDR-CMP-06 | d410 + lower limb spasticity + orthostatic intolerance → sit-to-stand compound | NEU + OFS | all rooms | P1 | Spasticity requires slow controlled rise (avoid stretch reflex); OFS requires staged positional change. Same direction but different mechanisms — surface height and support specifications interact |
| FDR-CMP-07 | d310 + hearing loss + cognitive impairment → communication in noise | DEAF + DEM/NEU | common/dining | P2 | Hearing loop requires device operation that DEM/NEU may not manage; background noise reduction benefits both but through different mechanisms; simplified fixed environmental provision |
| FDR-CMP-08 | d450 + ambulant + tremor + visual impairment → stair negotiation | MOB + NEU + VIS | stair/level change | P2 | Triple compound: handrail grip compromised by tremor; nosing visibility compromised by VIS; balance compromised by all three. Stair specification must address all simultaneously |

---

## D. New Slugs — Occupation-Level Scenarios [OCCUPATION]

Per PEO/PEOP framework: whole-occupation performance, not decomposed ICF codes.

| ID | Occupation | Constraint cluster | Environment | Priority | Rationale |
|---|---|---|---|---|---|
| FDR-OCC-01 | Morning ADL routine (wake → toilet → wash → dress → eat) | Any compound profile | residential | P1 | The occupation is the routine, not any single activity. Spatial sequencing of bedroom → bathroom → kitchen must support the flow. PEO congruence: room adjacency, door-free transitions, consistent grab bar availability along the path |
| FDR-OCC-02 | Hosting/receiving visitors | MOB + DEAF or DEM | residential entry + living | P2 | Multi-step occupation: hear/see doorbell → identify visitor → navigate to door → open → welcome → seat guest. Each step has a different functional requirement; the occupation fails if any step fails |
| FDR-OCC-03 | Home-based work/study | NDV/ADHD or OFS/ME | home office/bedroom | P2 | Sustained cognitive work with fatigue or executive function constraints: desk height/posture, lighting for screen + document, acoustic isolation, break space adjacency, postural change provisions |
| FDR-OCC-04 | Carer-assisted personal care | Any high-support need (C4-C5, advanced DEM) | bathroom/bedroom | P1 | The occupation includes two people: the occupant + the carer. Spatial specification must accommodate both bodies, both movement patterns, and the interaction (hoist, transfer board, sling). PEO with two persons |
| FDR-OCC-05 | Night-time toileting | DEM or OFS or MOB-elder | bedroom → bathroom | P1 | High-risk occupation: fall risk peaks at night; lighting must guide without fully waking (circadian disruption); route must be obstacle-free, grab-bar continuous, and orientation-preserving for DEM |
| FDR-OCC-06 | Leaving and returning home | MOB + VIS or DEM | entry → public realm | P3 | Door sequence → threshold → path → gate/street. Outbound and return require different orientations. DEM may not recognise own door on return. VIS needs consistent tactile sequence |

---

## E. New Slugs — Environment-Led Scenarios [ENVIRONMENT]

Where the environment type defines the research target, not the functional deficit.

| ID | Environment | Research question | Target populations | Priority | Rationale |
|---|---|---|---|---|---|
| FDR-ENV-01 | Balcony/terrace/outdoor living | What spatial parameters enable safe, independent outdoor access for wheelchair users, fall-risk populations, and DEM? | MOB, DEM, OFS, VIS | P2 | Outdoor residential space: threshold, drainage, railing height, shade/thermal, fall-from-height protection, DEM wandering containment |
| FDR-ENV-02 | Utility/storage room | What clearances, reach ranges, and fixture heights enable independent use? | MOB, UPL, VIS | P3 | Often omitted from accessible design; critical for independent living (boiler, fuse box, water stop, storage) |
| FDR-ENV-03 | Hallway/corridor as living space | In small dwellings, corridors serve as circulation AND storage AND social space. What width enables multi-function use? | MOB, walking frame users, bariatric | P3 | Small-dwelling reality: the corridor is not just circulation; it must accommodate coat storage, wheelchair charging, passing two people |
| FDR-ENV-04 | Shared/multi-occupant bathroom | What specifications resolve conflicts when two or more occupants with different needs share one bathroom? | All co-occurring | P2 | Residential reality: most dwellings have one bathroom. Part 5 co-occurrence at room level, not building level |
| FDR-ENV-05 | Non-residential quiet/sensory room (Kawa-informed) | What specification works for collectivist-context sensory relief — shared rather than private retreat? | NDV, NDV/MH, DEM | P1 | Direct response to framework review: PAS 6463 private retreat model fails in collectivist cultures; need shared-calm-space specification |

---

## F. Priority Summary

### P1 — Immediate (next 3 sessions, ~30 scenarios)

**Granular:** FDR-NEW-02, -04, -05, -09, -11, -15, -16
**Compound:** FDR-CMP-01, -02, -04, -06
**Occupation:** FDR-OCC-01, -04, -05
**Environment:** FDR-ENV-05
**Existing PARTIAL completions:** laundry (1), deaf (1), deafblind (1), dementia (2), sensory (2), visual (1) = 8

**Total P1: ~22 scenarios**

### P2 — Soon (within 10 sessions)

**Granular:** FDR-NEW-01, -03, -07, -08, -10, -12, -13, -14, -17
**Compound:** FDR-CMP-03, -05, -07, -08
**Occupation:** FDR-OCC-02, -03
**Environment:** FDR-ENV-01, -04

**Total P2: ~18 scenarios**

### P3 — Backlog

**Granular:** FDR-NEW-06, -18
**Occupation:** FDR-OCC-06
**Environment:** FDR-ENV-02, -03

**Total P3: ~5 scenarios**

---

## G. Token Budget Guidance

- Limit of 12 granular scenarios per session (existing rule).
- Compound scenarios count as 2 granular (they require searching each constraint independently then synthesising the interaction).
- Occupation scenarios count as 3 granular (they require searching multiple ICF codes in sequence then synthesising the flow).
- Environment scenarios count as 2 granular.
- **Recommended session mix:** 4 granular + 2 compound + 1 occupation = ~12 equivalent. Or: 6 granular + 1 environment + 1 compound = ~11 equivalent.
- Compound and occupation synthesis: **Opus required** per framework review §5.

---

## H. Methodology Notes

### H.1 Compound Scenario Search Protocol
1. Search each constituent constraint independently (standard FDR §4).
2. Search for the compound profile explicitly: `"{constraint-A} AND {constraint-B}" AND {environment}`.
3. If no compound-specific literature: document the interaction as clinical reasoning (Co-2), citing the individual constraint findings and the non-additivity principle (MWI, Clarke 4.52x).
4. Classification: COMPOUND-NOVEL (no prior BPC entry addresses the interaction), COMPOUND-REFINES (existing spec is adequate for compound but rationale unstated), COMPOUND-CONFLICTS (individual specs give contradictory guidance for compound profile).

### H.2 Occupation Scenario Search Protocol
1. Map the occupation to its constituent ICF codes (typically 3-6).
2. Search the occupation name directly in OT home modification literature (e.g., "morning routine home modification").
3. Search the PEO literature for the occupation-environment fit.
4. Extract spatial parameters that emerge only at the occupation level (e.g., room adjacency, transition zones) that no individual ICF code search would surface.

### H.3 Environment Scenario Search Protocol
1. Search the environment type + "accessible design" + "home modification".
2. Search population-specific guidance for that environment (e.g., "dementia balcony safety").
3. Extract parameters unique to the environment type that cross-cut populations.
