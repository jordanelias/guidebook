# Connection Scout — Opus Mechanism-Clustering Scan
**Date:** 2026-04-09
**Model:** Opus 4.6
**Method:** Mechanism-clustering cross-referential analysis
**Inputs:** 113 existing CON entries (full text), coverage matrix, connection network graph, 76 BPC presence data

---

## Method Description

Previous connection-scout scans identified connections by reading BPC entries sequentially and noting cross-population overlaps. This scan uses a different approach: extracting underlying *environmental mechanisms* that mediate person-environment interaction, then tracing which items serve each mechanism and which populations benefit from that mechanism but are not coded on the item.

This is analogous to embedding-based similarity search in that it matches by latent functional relationship rather than surface-level keyword co-occurrence. The "embedding space" is the set of environmental mechanisms; items that share a mechanism are "close" regardless of their item category or population tag.

### Mechanisms Extracted

| Mechanism | Populations served | Items involved | Existing CON coverage |
|---|---|---|---|
| Energy conservation | OFS, PAIN, MOB, DEM | Thresholds, rest seating, adjacency, adjustable surfaces | Moderate (CON-0009, 0056, 0058) |
| Spatial predictability | DEM, VIS, DBL, IntD, NDV/AUT, NEU | Loop circulation, furniture consistency, TWSI | Good (CON-0001, 0051, 0053) |
| Sensory modulation | NDV, MH, DEAF, NEU, OFS, PAIN | A-16, zone system, user control | Good (CON-0019, 0040, 0046) |
| Thermal regulation | NEU/MS, OFS, PAIN/FMS, DEM | F-07, F-08, vestibule | Good (CON-0041, 0101, 0102) |
| Visual contrast/legibility | VIS, DEM, DBL, IntD | C-04, TWSI, wayfinding | Moderate (CON-0043, 0060) |
| Postural support | MOB, OFS, PAIN, NEU | Grab bars, seating, reclining | Moderate (CON-0003, 0004) |
| Multi-channel alerting | DEAF, DBL, NEU (seizure) | B-10, K-04, H-05 | Good (CON-0042, 0104) |
| Fear/stress reduction | DEM, NEU, NDV/MH, OFS | Sightlines, refuge, consistent layout | Good (CON-0021, 0022, 0024) |
| **Haptic navigation** | **DBL, VIS, DEM** | **Grab bars, handrails, TWSI, door hardware** | **THIN — major gap** |
| **Emergency communication during transfer** | **DBL, MOB (high SCI), DEM** | **I-04, H-05, K-04** | **ZERO — safety-critical gap** |
| **Door as wayfinding element** | **DEM, VIS, IntD, NDV** | **E-01, D-02** | **ZERO** |
| **Rest provision scaling** | **OFS, PAIN, NDV, MH** | **I-03, D-05, A-16** | **Partial (items connected; scaling hierarchy unmade)** |
| **Zoning coordination** | **NDV, OFS, PAIN, NEU** | **F-01, F-07, B-01, B-06** | **ZERO (lighting and thermal zones specified independently)** |

---

## New Connections

### CON-0114

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** deafblind-built-environment-design, upper-limb-impairment-built-environment
**Target item(s):** I-04, H-05, K-04
**Target population(s):** DBL, MOB (C4+ SCI), DEM
**Evidence tier:** Tier 2 (DbI guidelines) + clinical reasoning
**Filed:** 2026-04-09
**Applied:** —

**Connection:** A person suspended in a ceiling hoist (I-04) cannot reach a wall-mounted nurse call button (H-05). For DBL users, auditory call confirmation is also inaccessible. For high-level SCI users (C4+), hand-operated call buttons are inaccessible during the transfer itself. The hoist-to-bed/chair transfer is the highest-risk moment for falls and injury — and the moment when emergency communication is least available. No current specification addresses emergency communication during hoist operation.

**Evidence basis:** deafblind BPC documents that all communication systems must be accessible through non-visual, non-auditory channels for DBL. upper-limb-impairment BPC documents reach/grip limitations for C4+ SCI. CON-0104 connects H-05 to K-04 for DBL in care environments but does not address the hoist-use scenario. CON-0103 connects I-04 to G-03/G-04 but not to alerting items.

**Action required:** Add hoist-operation emergency communication specification to I-04: pendant or wearable nurse call device (K-04 vibrotactile + voice) that remains accessible during hoist suspension. This is a life-safety specification — the gap between I-04 and H-05/K-04 is a zero-communication window during the highest-risk activity.

**Disposition notes:** — Safety-critical. Recommend Batch 1 priority.

---

### CON-0115

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** deafblind-built-environment-design, dementia-built-environment
**Target item(s):** D-09, D-02
**Target population(s):** DBL, DEM
**Evidence tier:** Tier 2 (DbI guidelines) + Tier 3 (Marquardt 2011)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** DBL and DEM rely on identical environmental mechanism — spatial predictability — through different sensory channels. DBL navigates by tactile memory of fixed spatial relationships; any furniture rearrangement breaks the tactile map. DEM navigates by cognitive spatial mapping; any layout change breaks the memory trace. The specification (D-09: consistent furniture arrangement) already serves both, and CON-0053 extends D-09 to VIS/DBL/IntD. But the *convergence mechanism* between DBL and DEM is undocumented: both populations are catastrophically (not merely inconvenienced) affected by spatial change. This elevates D-09 from "helpful consistency" to "safety-critical spatial stability" for the DBL+DEM co-occurrence — which occurs in aged-care settings where DEM prevalence is high and DBL (acquired) is co-occurring.

**Evidence basis:** deafblind BPC: tactile memory navigation relies on furniture permanence; unfamiliar changes are high-risk (DbI guidelines, Tier 2). dementia BPC: Marquardt 2011 identifies floor plan as the most influential environmental factor; Bowes et al. 2019 confirms spatial change as disorientation trigger.

**Action required:** Strengthen D-09 with DBL+DEM co-occurrence note: in settings where both populations are present (aged care, residential care), spatial arrangement changes must follow a documented change protocol — advance notification through accessible channels (tactile map update for DBL, gradual phased change for DEM). Specification goes beyond "don't rearrange" to "manage change."

**Disposition notes:** — Extends CON-0053. Aged-care-specific.

---

### CON-0116

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** wayfinding-dementia-spatial-design, cognitive-wayfinding-design, visual-impairment-built-environment
**Target item(s):** E-01, D-02
**Target population(s):** DEM, VIS, IntD, NDV/AUT
**Evidence tier:** Tier 3 (Marquardt 2011) + Tier 2 (DSDC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Doors are the primary decision points in wayfinding. E-01 specifies door hardware (handle type, clear width, closing force) but not door-as-wayfinding-element. D-02 specifies wayfinding systems (signage, TWSI, landmarks) but not door-level cues. The gap: a person navigating a corridor encounters doors as the most salient spatial feature, but no specification links the door to the wayfinding system. DEM users identify rooms by door colour/position (Marquardt 2011). VIS users identify doors by contrast and tactile cue. IntD users need pictogram + door-colour coding. NDV/AUT users need consistent door-colour-to-function mapping (e.g., all toilet doors same colour). Currently, door appearance is an interior design decision with no specification guidance.

**Evidence basis:** wayfinding-dementia-spatial-design BPC: door colour and position are the most used wayfinding cues for DEM users; toilet door colour is the single strongest predictor of independent toileting (Marquardt 2011). cognitive-wayfinding-design BPC: decision-point identification reduces cognitive load.

**Action required:** Add door-as-wayfinding-element specification: (a) consistent door colour coding by function (all bathroom doors = one colour; all exit doors = another); (b) LRV contrast between door and frame ≥30% (code minimum) / ≥50% (guidebook target per CON-0043); (c) tactile room-number plate at consistent height (1400mm AFF) on latch side. Cross-reference E-01 ↔ D-02.

**Disposition notes:** — Bridges two item categories that share a spatial location but have no connection.

---

### CON-0117

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** sensory-relief-space-design, pain-ofs-built-environment-design, PAS 6463:2022
**Target item(s):** I-03, D-05, A-16
**Target population(s):** OFS, PAIN, NDV/AUT, NDV/MH
**Evidence tier:** Tier 5 (PAS 6463) + Tier 3 (OFS/PAIN BPCs) + CON-0019
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Rest provision scales through three tiers — seated rest (I-03, every 50m on primary routes), enclosed low-stimulation space (D-05, one per floor), full sensory room (A-16, one per building) — but the scaling relationship is not specified. A practitioner does not know: (a) at what building occupancy does each tier become mandatory? (b) what is the distance/time threshold between tiers? (c) can D-05 substitute for A-16 in smaller buildings? These three items are specified independently. The scaling hierarchy is implicit in the BPC evidence (PAS 6463 recommends quiet spaces at building scale; OFS BPC specifies rest points at 50m intervals) but never codified.

**Evidence basis:** PAS 6463:2022 §6.4 (quiet space provision by building type). pain-ofs BPC (rest point intervals). CON-0019 (environmental refuge as Universal Mode — one per floor). sensory-relief-space-design BPC (A-16 specification).

**Action required:** Create rest provision scaling table in Part 4 preamble or Part 3 §3.x: I-03 (≤50m intervals, all buildings) → D-05 (per floor, buildings >500m² GFA or >2 storeys) → A-16 (per building, buildings >2000m² GFA or where NDV/MH populations primary). Tier thresholds: I-03 = Universal Mode; D-05 = Universal Mode (>500m²) / Tier 1 (<500m²); A-16 = Tier 1 for most buildings / mandatory for healthcare + education per CON-0046.

**Disposition notes:** — Codifies implicit hierarchy. High practitioner value.

---

### CON-0118

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** deafblind-built-environment-design, reach-range-and-accessible-controls
**Target item(s):** H-01, H-02
**Target population(s):** DBL
**Evidence tier:** Tier 2 (DbI guidelines)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** H-01 (reach range) and H-02 (individual environmental control) specify controls for MOB, VIS, DEAF — but not DBL. DBL users cannot use: visual displays (temperature readouts, lighting level indicators), auditory feedback (beeps, click sounds), touchscreen interfaces, or any control that requires simultaneous visual + auditory confirmation. DBL needs: tactile-only operable controls with distinct raised profiles per function, haptic confirmation of state change (vibration pattern), Braille labels at consistent positions, and controls that remain legible when hands are wet (bathroom/kitchen context).

**Evidence basis:** deafblind BPC: all environmental controls must provide non-visual non-auditory feedback (DbI best practice guidelines). Controls-and-hardware BPC: H-01 documents reach range but not interface modality requirements by population.

**Action required:** Add DBL as co-population for H-01/H-02. Specify: (a) all environmental controls to provide tactile state feedback (not just visual/auditory); (b) distinct raised button profiles per function (temperature ≠ lighting ≠ ventilation); (c) Braille labels at 1200mm AFF on latch side of control panel; (d) haptic confirmation of activation (vibration pulse).

**Disposition notes:** — Controls-and-hardware has only 1 BPC covering only MOB (coverage matrix). DBL is the most under-represented population in this topic.

---

### CON-0119

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** true
**Source BPC slug(s):** sensory-processing-model-design-application, thermoregulation-built-environment, circadian-lighting-melanopic-edi
**Target item(s):** F-01, F-07, B-01, B-06
**Target population(s):** NDV/AUT, OFS, PAIN, NEU/MS
**Evidence tier:** Tier 5 (PAS 6463) + Tier 3 (Dunn model, thermoregulation BPC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** CON-0040 specifies a three-zone sensory environment system (Zone 1 high activation → Zone 3 low activation) with lighting parameters per zone. F-07 specifies thermal zones (18–22°C range by population). These two zoning systems operate on the same building but are specified independently. The unmade coordination: Zone 3 (low activation) should be both dimmer/warmer CCT AND cooler temperature (for NEU/MS/OFS). Zone 1 (high activation) should be brighter/cooler CCT AND can tolerate wider thermal range. If lighting zones and thermal zones are designed by different consultants (typical), they may produce contradictory sensory environments — a Zone 3 space with high-activation lighting, or a Zone 1 space with low-activation thermal setpoint.

**Evidence basis:** sensory-processing-model BPC: Dunn's profiles map to both lighting and thermal preferences. thermoregulation BPC: harm-asymmetry analysis shows NEU/MS populations need cool ambient in low-activation spaces. circadian-lighting BPC: daytime CCT targets (4000K+) apply to Zone 1/2 but may be inappropriate for Zone 3 refuge spaces.

**Action required:** Create sensory zone coordination table: for each zone level, specify coordinated lighting (lux, CCT, melanopic EDI) AND thermal (ambient °C, radiant supplement) AND acoustic (RT60, NC) targets. Single table replaces three independent specifications. Mark as ○ (expert synthesis) — no single study validates multi-parameter zone coordination.

**Disposition notes:** — Prevents contradictory consultant specifications. Requires cross-category coordination.

---

### CON-0120

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** accessible-bathroom-and-grab-bar, deafblind-built-environment-design, ecological-psychology-haptic-affordances-built-environment
**Target item(s):** G-03, G-04
**Target population(s):** DBL
**Evidence tier:** Tier 2 (DbI guidelines) + foundational (Gibson 1979 haptic affordances)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Grab bars serve DBL through a dual mechanism not captured in the current specification: (1) postural support (same as MOB/PAIN/OFS — CON-0003), and (2) haptic spatial landmark. For a deafblind person in a bathroom, the grab bar layout communicates the room's topology — horizontal bar = wall alongside; L-shaped bar = corner; vertical bar = doorway/transfer point. This haptic wayfinding function means grab bar placement for DBL populations carries additional spatial-orientation requirements beyond the biomechanical positioning optimised for MOB. A grab bar placed at the biomechanically optimal height for sit-to-stand (CON-0003) may not be at the haptic-scan height for a standing DBL user.

**Evidence basis:** deafblind BPC: tactile cues provide spatial orientation in unfamiliar wet environments. ecological-psychology-haptic BPC (CON-0044): handrail as haptic navigation structure; Gibson affordance theory applies to grab bars as affordance communicators. DbI guidelines: tactile consistency in all frequently used spaces.

**Action required:** Add DBL as co-population for G-03/G-04. Add haptic wayfinding note: grab bar layout in DBL-designated bathrooms should provide a continuous tactile route from door to each fixture (toilet, basin, shower). Supplementary vertical orientation bars at fixture positions serve as haptic landmarks. This is a population-specific overlay (Tier 1) on the existing MOB biomechanical specification.

**Disposition notes:** — bathrooms-and-wet-areas has ZERO DBL coverage (coverage matrix). This fills the most safety-critical gap.

---

### CON-0121

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** true
**Source BPC slug(s):** circadian-lighting-melanopic-edi, visual-impairment-built-environment
**Target item(s):** B-06, B-07
**Target population(s):** VIS
**Evidence tier:** Tier 1 (Brown 2022 circadian) + Tier 2 (VIS BPC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** CON-0006/CON-0059 identify circadian lighting (≥250 melanopic EDI daytime, 4000K+ CCT) as multi-population provision for DEM/NEU/MH/OFS. VIS is absent from the population coding despite two interactions: (1) Synergy — higher illuminance improves both circadian entrainment and visual acuity; many VIS conditions benefit from increased light levels that circadian targets independently require. (2) Potential conflict — some VIS conditions (photophobia in albinism, certain macular conditions) are aggravated by high-intensity light; circadian targets may exceed comfortable levels for these sub-populations. The interaction is bidirectional and undocumented.

**Evidence basis:** circadian-lighting BPC (Brown 2022): melanopic EDI targets require ≥250 lux equivalent at eye level. visual-impairment BPC: VIS population has wide variation in light-level requirements — from maximum illumination (low vision) to minimum (photophobia). Neither BPC cross-references the other.

**Action required:** Add VIS as co-population for B-06/B-07 with bidirectional note: circadian illuminance targets benefit most VIS users (higher illuminance improves function) but contraindicate photophobic sub-populations. User control hierarchy (§1.4.4, H-02) resolves: individual dimming must be available in all spaces with circadian lighting. This is a synergy with a conflict edge case.

**Disposition notes:** — Fills sensory-environment × VIS coverage gap (currently 2 slugs but no lighting-VIS connection).
