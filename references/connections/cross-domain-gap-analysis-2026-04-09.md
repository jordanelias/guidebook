# Cross-Domain Evidence Connection Analysis — Corrected
**Date:** 2026-04-09
**Model:** Sonnet 4.6 (reduced-confidence — Opus validation required per project-standards §opus_synthesis)
**Method:** Verified against 76 BPC files (read, not inferred from names), 34 FDR files, 155 connections (7 Opus scan batches read in full), Parts 5 and 8, per-topic connection files
**Replaces:** Initial version committed same date (contained false positives, fabricated specifics, and gaps already covered by existing BPCs/connections)

---

## 0. Self-Correction Log

The initial version of this analysis contained the following errors, each caused by inferring coverage from file names rather than reading the evidence:

| Claimed gap | Actual status | Error type |
|---|---|---|
| FS-04 strobe ↔ seizure | **COVERED** — visual-fire-alarm-seizure-safety BPC: 0.5–1 Hz, synchronisation, multi-channel resolution | False positive — BPC exists and was not read |
| Zone coordination | **COVERED** — CON-0119 (Opus mechanism scan): lighting + thermal + acoustic zone alignment | Rediscovery of existing finding |
| Rest provision scaling | **COVERED** — CON-0117 (Opus mechanism scan): I-03 → D-05 → A-16 scaling hierarchy | Rediscovery of existing finding |
| VE vulnerability | **COVERED** — CON-0166 (Opus Batch 7): integrated specification clusters | Rediscovery of existing finding |
| DAR maintenance | **PARTIALLY COVERED** — CON-0160: nail plates, conduit labels, O&M notation | Partial rediscovery |
| Post-occupancy regression | **COVERED** — design-failures BPC Failure Mode 5 | False positive — BPC read only after initial analysis |
| FM-01 TWSI "3–5 year degradation" | Number fabricated — no source | Invented specificity |
| IP-04 copper alloy tactile | No evidence basis for the claim | Speculation presented as finding |

**Lesson:** 6 of 10 claimed "zero-coverage" gaps were already covered. The method (directory-name scanning without reading content) produced a document that looked authoritative but was substantially wrong.

---

## 1. What the Evidence Base Already Covers (verified)

Before identifying gaps, here is the verified coverage map from reading Opus batches 1–7, the mechanism scan, and key BPCs:

**Environmental mechanisms with GOOD coverage (≥3 connections + BPC):**
Spatial predictability, sensory modulation, thermal regulation, multi-channel alerting, visual contrast/legibility, fear/stress reduction, energy conservation, postural support

**Mechanisms with THIN coverage (identified by Opus, connections written but not yet consumed):**
Haptic navigation (CON-0120 DBL grab bar as spatial landmark), emergency communication during transfer (CON-0114 hoist scenario), door as wayfinding element (CON-0116), rest provision scaling (CON-0117), zoning coordination (CON-0119)

**Cross-domain domains already scanned by Opus:**
OT practice, clinical rehabilitation, acoustics, lighting/circadian, wayfinding/cognitive science, sensory processing, biomechanics, building codes (24 jurisdictions), economics, disability rights/CRPD, Global South, mental health, ecological psychology

---

## 2. Confirmed Gaps — Verified Against Evidence Base

Each gap below has been checked against all BPC files, all 155 connections, Part 5, Part 8, and per-topic connection files. Status: NOT FOUND in any existing source.

### GAP-A: Fire Safety Engineering as Coordination Discipline

**What exists:** Part 8 lists four engineering disciplines: AC, EE, ME, SE. Fire alarm (B-10) appears under EE. Refuge enclosure appears under SE §8.5. E-12 (evacuation lift) references "per fire engineer's strategy."

**What's missing:** Fire safety engineering is NOT a briefed discipline. It appears only as a passive reference — the fire engineer's strategy is assumed to exist but the architect's brief to the fire engineer for accessibility provisions is absent. Every other discipline has a structured brief template (§9.1.2–9.1.5). Fire safety has none.

**Specific accessibility provisions requiring fire engineer coordination:**
- Refuge area size, location, and communication provisions (not just structural enclosure)
- Visual alarm placement and synchronisation strategy (currently EE, but fire-safety-strategy-dependent)
- Evacuation route wayfinding under degraded conditions
- Fire door hold-open device strategy and locations

**Confidence:** HIGH — verified structural absence in Part 8.
**Action:** Add FE (Fire Safety Engineer) as fifth discipline in Part 8 §8.0.3 and create §8.1.6 Fire Safety Engineering Items table.

---

### GAP-B: Fire Door ↔ Spatial Continuity Conflict

**What exists:** Part 5 §5.1 states fire evacuation provisions take safety-critical priority. Visual-fire-alarm-seizure BPC covers strobe ↔ seizure. No BPC, connection, or Part 5 entry addresses fire door separation vs spatial continuity.

**What's missing:** Fire doors held closed (fire code requirement) break spatial continuity for DEM users (Marquardt 2011: floor plan is the most influential environmental factor for orientation) and sightlines for DEAF users (DeafSpace: visual connectivity for signing and environmental awareness). Electromagnetic hold-open devices (release on alarm) resolve this — but are a fire engineering specification, not an accessibility specification. No item code, BPC, or connection addresses this conflict.

**Related evidence already in system:** CON-0116 (door as wayfinding element) addresses door appearance/colour but not fire separation function. DEM BPC documents spatial continuity as orientation mechanism. DEAF BPC (deaf-spatial-design) documents sightline requirements.

**Confidence:** HIGH — the two population needs (DEM spatial continuity, DEAF sightline) and the fire code requirement (closed doors) are all documented separately. The conflict is the gap.
**Action:** New connection + new E-series item for electromagnetic hold-open devices on circulation route fire doors. Cross-reference Part 5. Route to GAP-A fire engineering brief.

---

### GAP-C: Refuge Area Accessibility (Distinct from Environmental Refuge)

**What exists:** Part 8 SE §8.5 specifies refuge enclosure structure. E-12 specifies evacuation lift. CON-0019 specifies environmental refuge (sensory low-stimulation space) — this is a different concept entirely.

**What's missing:** Fire evacuation refuge areas (stairwell refuges for people who cannot use stairs) have no accessibility specification beyond structural enclosure. No specification addresses:
- Seating in refuge (OFS/PAIN/MOB users cannot stand for extended waits — common evacuation waiting time: 20–45 minutes in high-rise)
- Communication from refuge (CON-0114 identified the emergency communication gap for hoist use; the same gap applies to refuge areas — a DEAF user in a refuge cannot communicate via intercom; a DBL user cannot use either audio or visual communication)
- Wayfinding TO refuge (D-series items do not address refuge wayfinding signage under degraded conditions)

**Confidence:** HIGH — verified against Part 8, E-12, CON-0019, CON-0114.
**Action:** New item specification for accessible refuge areas. Cross-reference I-03 (seating), CON-0114 (emergency communication), D-series (wayfinding).

---

### GAP-D: Emergency Wayfinding Under Degraded Conditions

**What exists:** D-series items (D-02 wayfinding, D-05 spatial design, D-06 TWSI, D-08 signage, D-09 consistency) all assume normal operating conditions — full lighting, clear air, functioning power.

**What's missing:** Under fire conditions (smoke, emergency lighting only, power failure), most wayfinding mechanisms fail:
- LRV contrast (C-04): invisible in smoke
- TWSI (D-06): functional (floor-level, tactile) — the only mechanism that survives
- Colour-coded signage (D-08): invisible in smoke/emergency lighting
- Cognitive wayfinding (DEM): spatial memory and landmarks degraded by disorientation/panic
- Digital wayfinding (if installed): power-dependent

Photoluminescent path markings (ISO 16069) and low-level wayfinding lighting (emergency lighting standards) are fire-safety specifications that directly serve VIS and DEM populations under degraded conditions but are not referenced in any D-series item or BPC.

**Confidence:** MODERATE — the degraded-condition gap is logical and the relevant standards exist, but no BPC has investigated whether photoluminescent markings serve the accessibility populations specifically.
**Action:** Research query required before connection can be written. Check: do photoluminescent path markings benefit VIS users specifically? Does any accessibility standard reference ISO 16069?

---

### GAP-E: Infection Prevention / Touchless Interfaces ↔ Accessibility

**What exists:** Zero coverage. No BPC. No connection. Not mentioned in Part 8. Not mentioned in any per-topic connection file.

**What's missing:** Post-COVID touchless installations (sensor-activated doors, infrared taps, touchless flush, hand sanitiser stations) create specific accessibility conflicts:

1. **Sensor-activated doors ↔ VIS/DBL:** The tactile door-finding cue (sweeping hand to find handle) is eliminated. VIS users may not detect that a door exists until it auto-opens unexpectedly, or may not trigger the sensor if approaching from the wrong angle. DBL users lose both the tactile and visual detection mechanism.

2. **Infrared taps ↔ DEM/IntD:** No visible mechanism. Cognitively opaque — nothing to turn, push, or pull. DEM and IntD users in care settings (where touchless was most aggressively installed) cannot independently operate facilities designed for infection control.

3. **Hand sanitiser station placement ↔ VIS/MOB:** Wall-mounted dispensers protruding into path of travel are collision hazards for VIS users. Pump mechanisms may be inoperable for MOB/UPL users.

**Confidence:** HIGH for items 1 and 2 (the mechanism is straightforward and the populations' needs are documented in existing BPCs). MODERATE for item 3 (specific hazard geometry needs verification).
**Action:** New BPC: touchless-interface-accessibility. Research: which jurisdictions mandate touchless installations in care/institutional settings? Any DPO/Co-1 evidence on touchless barriers?

---

### GAP-F: BMS ↔ Individual Environmental Control Governance Hierarchy

**What exists:** Part 8 mentions BMS under EE for lighting (B-01, B-06). H-02 specifies individual environmental control. CON-0017 (CONSUMED) links H-02, A-16, and B-01.

**What's missing:** When BMS automation and H-02 individual control conflict, which governs? Part 8 does not specify the hierarchy. If a BMS schedules building-wide temperature at 24°C at 14:00 (typical energy-saving setpoint), and an OFS/MCAS user has H-02 zone control set to 20°C, does the BMS override H-02? For NEU/MS users, a BMS override above 22°C can trigger Uhthoff's phenomenon (neurological deterioration). For NDV users, a BMS override of personal lighting settings removes the sensory regulation mechanism.

**Confidence:** MODERATE — the conflict mechanism is clear from existing BPCs (thermoregulation, NDV sensory), but no evidence base documents BMS override as an accessibility barrier specifically. This may be a specification gap (resolvable by stating H-02 overrides BMS) or an evidence gap (needing research).
**Action:** Specify in Part 8 EE section: H-02 individual environmental control takes precedence over BMS automation for any space with identified Tier 1/2 population users. BMS provides the default; H-02 provides the override. No BMS schedule may prevent H-02 from reaching the population-specified range.

---

### GAP-G: Accessibility Feature Durability and Maintenance Specification

**What exists:** CON-0160 addresses DAR operational protection (nail plates, conduit labelling). Failure taxonomy Mode 5 (post-occupancy regression) documents the problem category. Part 8 I-03 TMV entry specifies "annual service in FM brief."

**What's missing:** Two specific durability gaps not addressed by CON-0160 or any BPC:

1. **TWSI material durability:** TWSI effectiveness depends on maintained height differential and contrast. High-traffic installations degrade. No specification addresses: minimum material hardness for TWSI in high-traffic areas, replacement trigger criteria (measurable height differential threshold), or inspection frequency. The TMV entry in Part 8 provides a model — "annual service in FM brief" — that could be extended to TWSI.

2. **Automatic door failure mode:** E-01 specifies door hardware including power-operated doors. No specification addresses failure-mode behaviour. Should a failed automatic door fail-open (fire risk, security risk, but maintains access) or fail-closed (maintains fire compartment, but creates a barrier for MOB/UPL who cannot manually open a heavy door)? The failure mode is a fire safety + accessibility intersection — another dimension of GAP-A.

**Confidence:** MODERATE — the degradation mechanism is real but no evidence base quantifies it. These are specification logic gaps, not evidence gaps.
**Action:** Add maintenance specification notes to TWSI (D-06) and automatic door (E-01) items. Cross-reference Part 8 FM brief requirements.

---

### GAP-H: Acoustic Privacy (Distinct from Speech Intelligibility)

**What exists:** Four acoustics BPCs (acoustics-speech-intelligibility, room-acoustic-performance, deaf-acoustic, deaf-classroom-RT). All focus on making speech audible and intelligible — STI, RT60, NC. CON-0119 addresses zone coordination including acoustic targets.

**What's missing:** Acoustic privacy — preventing speech from being heard outside a space — is the inverse specification. Relevant to:
- NDV/MH therapy rooms: conversation privacy is clinically essential (therapeutic alliance depends on confidentiality)
- DEAF relay/interpreter spaces: interpreter conversations are often louder than typical speech; acoustic containment prevents disclosure
- MH de-escalation rooms (CON-0131): crisis de-escalation may involve raised voices; acoustic isolation protects dignity

STC (Sound Transmission Class) for partition walls between these spaces is an acoustic specification distinct from STI within a space. No BPC addresses this. Part 8 AC items specify RT60 and STI but not STC for privacy-critical spaces.

**Confidence:** MODERATE — the need is clinically obvious for MH/NDV-MH contexts, but no BPC has investigated whether any accessibility standard specifies STC for these spaces.
**Action:** Research query: do any DPO guidelines, MH facility design standards, or OT CPGs specify acoustic privacy requirements for therapy/de-escalation rooms?

---

## 3. Summary: Genuine vs False Gaps

| Gap | Status | First analysis claim | Corrected status |
|---|---|---|---|
| Fire engineering discipline | **CONFIRMED** | Partially correct | Refined: structural absence in Part 8 |
| Fire door conflict | **CONFIRMED** | Correct | Unchanged |
| Refuge area accessibility | **CONFIRMED** | Correct | Distinguished from environmental refuge |
| Emergency wayfinding | **CONFIRMED** | Correct | Needs research before connection |
| Touchless interfaces | **CONFIRMED** | Correct but included fabricated IP-04 | IP-04 removed |
| BMS ↔ H-02 | **CONFIRMED** | Correct | Refined to governance hierarchy |
| TWSI durability | **CONFIRMED** | Correct principle, fabricated numbers removed | Numbers removed |
| Automatic door failure mode | **CONFIRMED** | Correct | Unchanged |
| Acoustic privacy | **CONFIRMED** | Correct | Unchanged |
| Strobe ↔ seizure (FS-04) | **FALSE** | Claimed as gap | Already in visual-fire-alarm-seizure BPC |
| Zone coordination | **FALSE** | Claimed as gap | Already CON-0119 |
| Rest provision scaling | **FALSE** | Claimed as gap | Already CON-0117 |
| VE vulnerability | **FALSE** | Claimed as gap | Already CON-0166 |
| Copper alloy tactile (IP-04) | **FALSE** | Speculative | No evidence basis |
| TWSI "3–5 year" figure | **FALSE** | Fabricated | No source |

**Confirmed genuine gaps: 9. False positives in first analysis: 6.**

---

## 4. Priority and Sequencing

### P1 — Safety-critical or actively creating barriers now

| Gap | Rationale | Estimated work |
|---|---|---|
| GAP-A: Fire engineering discipline | Structural gap in Part 8 — every other discipline briefed | 1 session: add FE discipline + §9.1.6 table |
| GAP-B: Fire door conflict | Undocumented conflict between fire code and DEM/DEAF needs | 1 connection + possible new E-series item |
| GAP-C: Refuge area accessibility | Safety-critical gap in evacuation provision | 1 connection + cross-references to I-03, CON-0114 |
| GAP-E: Touchless interfaces | Post-COVID installations are creating barriers in care settings now | New BPC required (research session) |

### P2 — Important specification logic gaps

| Gap | Rationale | Estimated work |
|---|---|---|
| GAP-D: Emergency wayfinding | Needs research before writing connection | 1 research query (ISO 16069 + accessibility) |
| GAP-F: BMS ↔ H-02 | Resolvable by specification statement in Part 8 EE | 1 Part 8 addition |
| GAP-G: Feature durability | Specification logic, not evidence gap | Add maintenance notes to D-06, E-01 |
| GAP-H: Acoustic privacy | Needs research before writing connection | 1 research query (STC for MH/therapy spaces) |

---

## 5. Meta-Observations (evidence-derived, not speculative)

1. **The evidence base is strong on person-environment fit and weak on building-as-system.** The Opus mechanism scan's five gap mechanisms (haptic navigation, emergency communication during transfer, door as wayfinding element, rest scaling, zone coordination) all involve inter-system relationships, not single-item specifications. The confirmed gaps in this analysis (fire engineering, BMS governance, failure modes) follow the same pattern. The guidebook specifies items well; it specifies system interactions less well.

2. **Fire safety is the largest genuinely unscanned domain.** It intersects accessibility at four distinct points (GAPs A, B, C, D) and is the only engineering discipline serving every building that has no Part 8 brief template.

3. **Touchless is the only confirmed gap actively creating new barriers.** All other gaps describe pre-existing specification holes. Touchless interfaces are being installed in care settings now, creating barriers for DEM, VIS, DBL, and IntD populations that did not exist before COVID.

4. **The analysis method matters more than the analysis scope.** My first attempt covered more domains (12 vs 8) but produced 6 false positives because it inferred from file names instead of reading content. The corrected version covers fewer domains but each gap is verified.

**[REDUCED-CONFIDENCE: Sonnet analysis. Connections should not be written to register until Opus validates GAP-B, GAP-C, GAP-D, and GAP-H, which involve cross-population synthesis judgment.]**
