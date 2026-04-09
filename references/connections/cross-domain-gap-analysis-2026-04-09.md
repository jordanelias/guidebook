# Cross-Domain Evidence Connection Analysis
**Date:** 2026-04-09
**Model:** Sonnet 4.6 (reduced-confidence — Opus validation required per project-standards §opus_synthesis)
**Method:** Disciplinary domain mapping against 76 BPC files, 34 FDR files, 155 connections, 7 Opus scan batches
**Purpose:** Identify disciplinary perspectives not yet systematically cross-referenced in the evidence base

---

## 1. Domain Coverage Matrix

### Domains with GOOD coverage (systematic BPC + Opus scan complete)

| Domain | BPC files | Opus batch | Key gaps already identified |
|---|---|---|---|
| OT practice / home modification | 3 (ot-built-environment-interface, ot-frameworks, ot-cpg) | Batch 6 | OT thermal gap (GAP-LRP-01) |
| Clinical rehabilitation / neurology | 7 (thermoregulation, MS-thermal, pain, OFS, fatigue, chronic-pain, thermal-comfort) | Batches 2, 4 | FMS vs MS/SCI thermal conflict resolved |
| Acoustics / speech intelligibility | 4 (acoustics-SI, room-acoustic, deaf-acoustic, deaf-classroom-RT) | Batch 3 | STI vs NRC criterion established |
| Lighting / circadian | 2 (therapeutic-lighting, circadian-melanopic) | Batch 3 | Circadian ↔ seizure conflict noted |
| Wayfinding / cognitive science | 4 (cognitive-wayfinding, wayfinding-cognitive-science, dementia-spatial, detectable-gradient) | Batch 5 | Decision-point + zone-boundary overload (CON-0148) |
| Sensory processing / NDV | 4 (sensory-relief, sensory-room-control, sensory-processing-model, NDV-quantified) | Batches 2, 5 | PAS 6463 cultural transfer problem |
| Biomechanics / anthropometrics | 4 (stair-ramp, grab-bar, circulation-geometry, reach-range) | Batch 5 | — |
| Building codes / jurisdiction | 2 (jurisdiction-matrix, EAA-scope) + 24-jurisdiction tracker | Batch 7 | Implementation gap vs specification gap |
| Economics / cost | 3 (economics-cost, case-study-financial, grant-programmes) | Batch 7 | Policy misallocation (CON-0162) |
| Disability rights / CRPD | 1 (crpd-implementation) + Phase 1-E research | Batch 6 | Treaty body = mandate, not specification |
| Global South / non-Western | 3 (co1-housing, bathroom-typology-GS, wayfinding-GS, sensory-space-GS) | Phase 1-E | Formal/informal city divide meta-barrier |
| Mental health / TID | 1 (mental-health-built-environment) | Batch 3 | MH room ≠ A-16 (CON-0131) |
| Ecological psychology / haptics | 1 (ecological-psychology-haptic-affordances) | Batch 5 | Haptic navigation THIN (mechanism scan) |
| Environmental controls / hardware | 1 (reach-range-and-accessible-controls) | Batch 3 | — |

### Domains with PARTIAL coverage (some BPC content, no dedicated cross-domain scan)

| Domain | What exists | What's missing |
|---|---|---|
| Air quality / chemical sensitivity | 1 BPC (air-quality-voc) | No cross-reference to ventilation ↔ acoustic isolation conflict; no connection to OFS/MCAS ↔ sealed building performance |
| Biophilic design | 1 BPC (biophilic-design-healthcare) | Appendix B only — no systematic cross-ref to DEM outdoor access, MH nature exposure, or PAIN distraction evidence |
| Floor vibration | 1 BPC (floor-vibration-wheelchair) | Only wheelchair perspective — not crossed with NEU (seizure trigger?), PAIN (vibration sensitivity), VIS (disorientation) |
| Post-occupancy evaluation | 1 BPC (STUB) | Phase 1-E identified as gap; no cross-domain scan of POE methods against population-specific outcomes |
| Interior materiality | LRV contrast BPCs only | No full material specification domain (slip resistance, thermal conductivity of surfaces, acoustic absorption of finishes) |
| Aging-in-place | DAR provisions register + visitability BPC | No cross-domain scan against gerontechnology, smart home, or progressive adaptation literature |

### Domains with ZERO coverage (no BPC, no scan, no connections)

| Domain | Relevance to guidebook | Estimated connection yield | Priority |
|---|---|---|---|
| **Fire safety / emergency egress** | Refuge areas, evacuation for MOB/VIS/DEM/DEAF; visual alarms (partial via K-04/B-10); wayfinding under smoke; door hold-open ↔ fire separation | HIGH (10–15 connections) | **P1 — safety-critical** |
| **Infection prevention / touchless design** | Post-COVID touchless interfaces ↔ VIS (no tactile feedback), DEM (unfamiliar tech), DBL (no visual confirmation), MOB/UPL (gesture requires dexterity) | HIGH (8–12 connections) | **P1 — conflicts with existing specs** |
| **Smart building / IoT / assistive technology** | Building automation ↔ individual control (H-02); indoor positioning ↔ wayfinding (D-series); voice control ↔ DEAF; app-based control ↔ DEM/IntD | MODERATE (6–10 connections) | P2 |
| **Facilities management / maintenance** | Degradation of accessibility features (TWSI worn smooth, automatic doors failing, grab bars loosening, contrast fading); maintenance access vs accessible layout | MODERATE (5–8 connections) | P2 |
| **Construction practice / tolerances** | How specs fail during construction — tolerance stack-up (1200mm clear opening → 1180mm after frame); value engineering removing "non-code" features; sequencing errors (grab bar backing not installed before tiling) | MODERATE (5–8 connections) | P2 |
| **Pediatric disability** | Different anthropometrics, developmental needs, school/education settings; not just scaled-down adult specs | MODERATE (4–6 connections) | P3 |
| **Landscape / outdoor transition** | Path of travel to building entry; garden/outdoor space accessibility; transition zone design (indoor→outdoor sensory shift for NDV); outdoor rest provision | MODERATE (4–6 connections) | P3 |
| **Acoustic privacy** | Distinct from speech intelligibility — privacy in MH settings (anti-eavesdropping), NDV/MH need for conversation privacy, DEAF relay/interpreter privacy | LOW-MODERATE (3–5 connections) | P3 |
| **Water / plumbing interaction** | Anti-scald (DEM, NEU — reduced sensation), accessible tap/valve operation, drainage in level-access bathrooms, water temperature ↔ thermal sensitivity | LOW (2–4 connections) | P3 |
| **Disaster resilience** | Accessible emergency shelter, post-disaster temporary housing, climate adaptation ↔ disability | LOW (2–3 connections) | P3 |

---

## 2. Cross-Domain Connection Candidates (ZERO-coverage domains)

### 2.1 Fire Safety / Emergency Egress — Candidate Connections

**FS-01: Refuge area ↔ rest provision (I-03)**
OFS/PAIN/MOB users who cannot use stairs need refuge areas. These are specified by fire codes but never cross-referenced to I-03 (rest seating) or accessibility specs. A refuge area without seating is inaccessible to OFS users who cannot stand for extended evacuation waits. Refuge area design is fire engineer territory — no population-specific specification exists.

**FS-02: Emergency wayfinding ↔ D-series items under degraded conditions**
VIS wayfinding relies on LRV contrast and TWSI. Under smoke: LRV contrast destroyed; TWSI still functions. DEM wayfinding relies on spatial memory and visual landmarks. Under smoke: both destroyed. DEAF wayfinding relies on visual alerts. Under strobe + smoke: reduced effectiveness. No D-series item addresses degraded-condition wayfinding. Low-level photoluminescent path markings (ISO 16069) are a fire-safety spec that benefits VIS/DEM under smoke but is not cross-referenced.

**FS-03: Fire door hold-open devices ↔ DEM wandering / DEAF sightline**
Fire doors are normally closed (fire code) OR held open by electromagnetic devices that release on alarm. DEM users are confused by closed fire doors (barrier to spatial continuity — Marquardt 2011). DEAF users lose sightline through closed fire doors (DeafSpace). The fire-safety vs accessibility conflict is a known issue (UK AD M vs AD B) but not documented in our conflict matrices.

**FS-04: Alarm system interaction ↔ NEU seizure / NDV sensory overload**
Visual fire alarms (strobe, B-10 / K-04) are DEAF-essential but are photosensitive seizure triggers for NEU (3–30 Hz range). CON-0042 and CON-0104 address multi-channel alerting but do not address the strobe-seizure conflict. Additionally, multi-modal alarms (auditory + visual + tactile simultaneously) may trigger NDV sensory overload at the moment requiring clearest cognition.

**FS-05: Evacuation chair / hoist ↔ MOB/SCI dignity + safety**
Evacuation chairs require a trained operator. For high-SCI users, transfer from wheelchair to evacuation chair is itself a risk. No specification addresses whether the hoist (I-04) can be used for emergency evacuation, or how emergency communication (CON-0114 gap) operates during evacuation.

### 2.2 Infection Prevention / Touchless Design — Candidate Connections

**IP-01: Touchless door activation ↔ VIS/DBL wayfinding**
Touchless doors (sensor-activated) eliminate the tactile door-finding cue that VIS and DBL users rely on. A VIS user sweeping a hand along a wall to find a door handle encounters nothing if the door auto-opens. The design solution (retain tactile indicator + touchless option) is straightforward but unspecified.

**IP-02: Touchless taps/flush ↔ DEM/IntD comprehension**
Infrared-sensor taps are cognitively opaque — no visible mechanism. DEM and IntD users may not understand how to activate them (no lever to turn, no button to press). The pandemic accelerated touchless installation in care settings serving precisely these populations. Dual-mode (sensor + manual lever) is the resolution.

**IP-03: Hand sanitiser stations ↔ VIS/MOB/OFS**
Wall-mounted hand sanitiser dispensers are a trip/collision hazard for VIS users if they protrude into the path of travel. For MOB/UPL users, pump mechanisms may be inoperable. For OFS/MCAS, alcohol-based sanitiser can trigger chemical sensitivity reactions. No item addresses sanitiser station placement or specification.

**IP-04: Antimicrobial surfaces ↔ NDV/AUT tactile sensitivity**
Antimicrobial coatings and copper-alloy surfaces change the tactile and thermal properties of grab bars, handrails, and door hardware. NDV/AUT users with tactile hypersensitivity may find copper alloy unacceptable (different thermal conductivity, texture). No specification addresses material selection for infection control ↔ sensory acceptability conflict.

### 2.3 Smart Building / IoT — Candidate Connections

**SB-01: Building automation defaults ↔ individual control (H-02)**
BMS (Building Management Systems) set default lighting, temperature, ventilation. H-02 specifies individual environmental control. The interaction: who governs — the BMS or the individual control? For NDV: BMS override of personal lighting settings removes the regulation mechanism. For OFS: BMS temperature override can trigger symptom cascade. No specification addresses BMS ↔ H-02 hierarchy.

**SB-02: Indoor positioning / Bluetooth beacons ↔ D-series wayfinding**
Digital wayfinding (smartphone-based) is rapidly supplementing physical signage. For VIS: audio wayfinding via phone is often more effective than TWSI alone. For DEM: phone-based wayfinding is inaccessible (cannot operate device). The physical wayfinding system must remain complete and independent — digital is supplementary, not substitutive. This principle is implicit but unspecified.

**SB-03: Voice control ↔ DEAF/DBL/speech impairment**
Smart home voice interfaces (lighting, temperature, doors) are inaccessible to DEAF, DBL, and users with speech impairment (NEU/ABI dysarthria). Every voice-controlled system needs an equivalent non-voice control path. This is an existing accessibility principle but not applied to building automation.

### 2.4 Facilities Management / Maintenance — Candidate Connections

**FM-01: TWSI degradation**
TWSI (Tactile Walking Surface Indicators) effectiveness depends on maintained height differential (5mm) and contrast. In high-traffic areas, TWSI wear flat within 3–5 years. No specification addresses material durability or replacement cycle. The specification becomes inaccessible through maintenance failure, not design failure.

**FM-02: Automatic door maintenance**
Automatic doors (E-01) are the most failure-prone accessibility feature. A failed automatic door becomes a barrier (heavy, no manual override for MOB/UPL). No specification addresses maintenance protocol, failure-mode behaviour (should a failed door fail-open or fail-closed?), or interim access during repair.

**FM-03: Contrast maintenance**
LRV contrast (C-04) degrades through cleaning chemical damage, UV fading, and surface wear. A 30-point LRV contrast specified at installation may be 15-point after 5 years. No specification addresses minimum maintained contrast or maintenance inspection protocol.

---

## 3. Existing Mechanism Gaps (from Opus Batch 4) — Cross-Domain Lens

The Opus mechanism scan identified 5 gap mechanisms. Applying cross-domain lenses reveals additional depth:

### Zoning coordination (ZERO coverage)
Lighting zones (B-01, B-06), thermal zones (F-07), acoustic zones (F-01), and sensory zones (detectable-gradient-protocol) are specified independently. In fire safety: zone boundaries often align with fire compartments. In HVAC engineering: zone boundaries are duct-routing decisions. In lighting design: zone boundaries are circuit-routing decisions. **The cross-domain insight: zone boundaries should align across all systems where possible, reducing the cognitive load of multiple simultaneous environmental transitions.** This is a building physics + sensory science + fire safety intersection with no current BPC.

### Rest provision scaling (PARTIAL)
I-03 specifies rest seating. The fire safety domain adds: rest provision along evacuation routes (not just circulation routes). The gerontology domain adds: progressive fatigue means rest interval distance should decrease with building height/complexity. The OFS domain adds: horizontal rest (lying down) required, not just seated. **Multiple domains converge on a rest-scaling specification that is more granular than I-03 currently provides.**

---

## 4. Recommended Actions

### Immediate (Opus session)

1. **Fire safety cross-domain scan (P1)** — FS-01 through FS-05 are safety-critical. Load UK AD B, AS 1428.1 fire provisions, ISO 21542 §Emergency, and NFPA 72 (visual alarm) against existing BPC corpus. Estimate: 10–15 new connections, 2–3 new items. **This is the highest-yield gap.**

2. **Validate this analysis (Opus)** — This document carries reduced-confidence. Opus review needed before any connections are written to the register.

### Short-term (next 2–3 sessions)

3. **Infection prevention / touchless scan (P1)** — IP-01 through IP-04 conflict with existing specifications. Post-COVID installations are creating accessibility barriers in care settings now.

4. **Zoning coordination BPC** — Synthesise lighting, thermal, acoustic, sensory zone specifications into a single zone-coordination methodology entry for Part 3 §3.8 or Part 8.

### Medium-term

5. **Smart building / IoT scan** — SB-01 through SB-03 as the built environment increasingly automates.

6. **Facilities management / maintenance BPC** — FM-01 through FM-03 address the operational dimension that no design guide covers.

7. **Acoustic privacy BPC** — Distinct from speech intelligibility; specific to MH, NDV/MH, DEAF relay contexts.

### Deferred

8. Pediatric disability — P3; requires separate anthropometric and developmental evidence base.
9. Landscape/outdoor — P3; partially addressed by biophilic BPC but outdoor accessibility is its own domain.
10. Disaster resilience — P3; out of specification scope (formal new construction) per project-standards but worth flagging in Part 1 §1.9.

---

## 5. Coverage Heatmap: Domain × Population

Blank cells = no cross-domain connection identified in current evidence base.

| Domain ↓ / Population → | MOB | VIS | DEAF | NEU | DEM | NDV | MH | PAIN | DBL | OFS | IntD |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Fire safety | FS-05 | FS-02 | FS-03 | FS-04 | FS-02,03 | FS-04 | — | — | — | FS-01 | — |
| Infection prev. | IP-03 | IP-01 | — | — | IP-02 | IP-04 | — | — | IP-01 | IP-03 | IP-02 |
| Smart building | — | SB-02 | SB-03 | SB-03 | SB-02 | SB-01 | — | — | SB-03 | SB-01 | — |
| Maintenance | FM-02 | FM-01,03 | — | — | FM-03 | — | — | — | FM-01 | — | — |
| Acoustic privacy | — | — | ✓ (relay) | — | — | ✓ | ✓ | — | — | — | — |
| Zone coordination | — | ✓ | — | ✓ | ✓ | ✓ | — | ✓ | — | ✓ | — |

---

## 6. Meta-Observation

The existing evidence base is strong on **person-environment fit** (how individual populations interact with specific building elements) and on **inter-population conflict** (how different populations' needs clash). The systematic gaps cluster in three meta-categories:

1. **Building operations** — what happens after handover (maintenance, FM, degradation)
2. **System interactions** — where building systems intersect (fire + accessibility, HVAC + acoustics, BMS + individual control)
3. **Technology transition** — where new technology changes the accessibility equation (touchless, IoT, digital wayfinding)

These are all domains where the evidence sits outside disability-specific literature — in fire engineering journals, FM research, building science, and HCI. The existing multilingual-research protocol searches disability + built environment literature. A supplementary protocol for adjacent-field literature is needed.

**[REDUCED-CONFIDENCE: Sonnet analysis. Opus validation required before writing connections to register.]**
