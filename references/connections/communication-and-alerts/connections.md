# Connections — communication-and-alerts
<!-- CO-0006 Phase 0B-1 migration 2026-04-08 — from connection-register-active.md -->

### CON-0063

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** F-02, F-04
**Target population(s):** NDV, OFS, PAIN, MH
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Fragrance-free policy + MERV 13+ filtration (F-02, F-04) specified for OFS/MCAS and NDV chemical sensitivity serves MH/PTSD populations via identical mechanism — chemical stimuli as trauma triggers. Trauma-informed design framework (mental-health-built-environment BPC) emphasises environmental predictability but does not cross-reference air quality specifications.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| air-quality-voc-chemical-sensitivity-built-environment BPC | 3 | OFS, NDV | MH |
| mental-health-built-environment BPC | 2 | MH | F-02, F-04 cross-ref |

**Action required:** Add MH as co-population for F-02/F-04 air quality items. Mechanism: chemical stimuli reduction serves OFS/NDV physiological + MH trauma-trigger avoidance.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0101

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** F-07, F-08, A-01, A-02, A-08
**Target population(s):** NEU/MS, OFS, PAIN, NDV/AUT, DEAF
**Evidence tier:** —
**Filed:** 2026-04-03
**Applied:** —

**Connection:** F-07 (Thermal Zoning) and F-08 (Thermal Transition) specify HVAC system requirements including forced air prohibition in NEU/OFS spaces and high-performance envelope. The ms-thermal BPC states "no forced air heating as sole source in NEU/OFS spaces (acoustic + airborne trigger concern)." This acoustic rationale is not cross-referenced in Category A acoustic items.

Conversely, A-08 specifies NC-25 background noise. HVAC system type is the primary determinant of achievable NC level. F-07/F-08 HVAC zoning strategy directly constrains which heating systems can meet A-08 NC-25. This bidirectional dependency is not documented.

Additionally, F-08 thermal mass specification (≤3°C diurnal swing) vi…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| ms-thermal BPC (forced air prohibition) | 4 | NEU/MS, OFS | A-01, A-02 acoustic cross-ref |
| room-acoustic-performance BPC | 3–4 | DEAF, NDV | F-07/F-08 HVAC cross-ref |
| CIBSE Guide A (HVAC noise) | 5 | General | F-07 acoustic constraint |

**Action required:** Add cross-reference in F-07 and F-08: "HVAC system selection must achieve NC-25 per A-08; forced air systems are contraindicated for NEU/OFS spaces per ms-thermal BPC." Add reciprocal note in A-08: "Background noise target constrains HVAC system type — coordinate with F-07 thermal zoning strategy." Add note in A-02: "Where F-08 specifies exposed thermal mass (concrete ceiling), additional acoustic…

**Disposition notes:** - [x] HIGH → APPLIED 2026-04-03: cross-refs added to A-08 (HVAC type constraint, NC-25/forced-air coordination, exposed thermal mass note) and F-07 (CON-0101 coordination note). F-08 thermal mass note included in F-07 addition. A-02 note added via CON-0101 cross-ref in A-08.

---

### CON-0108

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** F-08, E-01, E-06, E-13, E-14
**Target population(s):** OFS, NEU/MS, MOB, VIS, DEM
**Evidence tier:** —
**Filed:** 2026-04-03
**Applied:** —

**Connection:** F-08 specifies an entry vestibule (thermal buffer ≥2 m depth) at primary accessible entrances. E-01 (Entrance Door), E-06 (Level Entry), E-13 (PIR Entrance Lighting), and E-14 (Entrance Rest Seating) all specify provisions at the same spatial location — the building entrance.

The vestibule adds a second door transition (outer + inner) which:
1. Doubles the E-01 door specification scope — both vestibule doors must meet E-01 accessible door specification.
2. Creates a transition zone where E-13 lighting must maintain illuminance continuity (no dark zone between outer and inner doors).
3. Places E-14 entrance rest seating within or immediately after the thermal buffer zone — the seating benefi…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| CON-0068 (thermal transition) | Internal | OFS, NEU | E-series coordination |
| pain-ofs-built-environment-design BPC | 3 | OFS | Vestibule spatial requirements |

**Action required:** Add note to F-08 vestibule specification: "Both vestibule doors to meet E-01 specification. Level entry (E-06) at both thresholds. Lighting (E-13) continuous through vestibule — no dark transition zone. Where E-14 entrance rest seating is specified, locate within or immediately after vestibule." Add reciprocal note in E-01: "Where F-08 thermal vestibule is specified, accessible door specification …

**Disposition notes:** - [x] MEDIUM → APPLIED 2026-04-03: F-08 Retrofit section updated with E-series coordination note (both vestibule doors E-01; level entry E-06 both thresholds; E-13 lighting continuity; E-14 seating within vestibule). E-01 cross-ref updated with F-08 vestibule reciprocal note. E-06/E-13/E-14 coordination embedded in F-08 note — separate item edits deferred to Phase 5 cross-reference-resolver pass.

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

### CON-0132

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** air-quality-voc-chemical-sensitivity-built-environment, biophilic-design-healthcare-workplace
**Target item(s):** BIO-01 through BIO-05, F-04
**Target population(s):** OFS/MCAS, DEM, NDV/MH
**Evidence tier:** Tier 4-5 (air quality BPC) + Tier 3 (biophilic BPC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Biophilic design provisions (BIO-series: indoor planting, nature views, natural materials) are therapeutic for DEM (reduced agitation — Al Khatib 2024 SR), NDV/MH (stress reduction — Ulrich), and NEU (ART/SRT restorative benefit). The air quality BPC specifies for OFS/MCAS spaces: "low-VOC, low-pollen species only; no strongly scented flowering plants." Additionally, F-06 (Fragrance-Free Policy) prohibits fragrance diffusers including any HVAC-integrated scent system.

Conflict: biophilic planting that serves DEM/NDV/MH may trigger OFS/MCAS symptoms. Flowering plants, aromatic herbs (lavender, rosemary — commonly recommended in DEM garden design), and high-pollen species are documented MCAS triggers.

Resolution: species-restricted planting list for shared OFS+DEM/NDV spaces. Permitted: foliage-only plants (ferns, pothos, snake plant), low-pollen succulents, sealed terrarium plantings. Prohibited: flowering plants, aromatic herbs, high-pollen grasses, plants with latex sap. Nature views through glazing (visual biophilia) serve all populations without air quality risk.

**Evidence basis:** air-quality BPC: OFS/MCAS fragrance/VOC/pollen triggers. biophilic BPC (Al Khatib 2024 SR, 61 sources): nature exposure therapeutic for DEM/NDV. Project-standards: DEM olfactory wayfinding is NOT an evidence-based specification; fragrance-free is the universal built environment specification.

**Action required:** Add species-restriction note to BIO-01/BIO-02 (indoor planting items): "Where OFS/MCAS populations co-occur, planting shall comply with F-04 air quality specification (low-VOC, low-pollen, no scented flowering species). Visual biophilia through glazing is the conflict-free alternative." Cross-reference BIO ↔ F-04.

**Disposition notes:** — Resolves a real specification conflict. Species restriction is the architectural equivalent of harm-asymmetry: MCAS reaction (physiological) > therapeutic planting benefit (psychological).

---

### CON-0142

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** thermoregulation-built-environment, air-quality-voc-chemical-sensitivity-built-environment
**Target item(s):** F-07, F-04
**Target population(s):** NEU/MS, OFS/MCAS
**Evidence tier:** Project-standards rule (2026-04-07)

**Connection:** Project-standards specifies 18–22°C working target for thermoregulation-impaired populations, with mechanical cooling as medically necessary in hot-humid tropical contexts. F-04 air quality specifies ≥15 L/s fresh air per person for OFS/MCAS spaces with no recirculated air without HEPA. In tropical contexts, these two specifications interact adversely: high fresh-air supply rates at 32°C+ ambient increase cooling load dramatically. The HVAC system must simultaneously cool to ≤22°C AND supply ≥15 L/s fresh air AND filter to MERV 13+ — this is an engineering coordination constraint that neither F-04 nor F-07 documents.

**Action required:** Part 8 (Engineering): add HVAC coordination note for tropical jurisdictions — cooling, ventilation, and filtration constraints from F-04 + F-07 are simultaneously binding. Engineering brief must specify all three. Cross-reference CON-0101 (HVAC type constraint).

---

### CON-0042

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** B-10, visual alerting items, H-04, CON-0014 items
**Target population(s):** DEAF, DBL, NEU (seizure), NDV/AUT (photosensitive)
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** CON-0014 proposes vibrotactile alerting for sleeping areas where DEAF/DBL and photosensitive populations co-occur. The `visual-fire-alarm-seizure-safety` BPC specifies synchronised VADs at 0.5–1 Hz + voice alarm + vibrotactile. The `visual-alerting-and-wayfinding-light` BPC covers non-emergency alerting (doorbells, call systems).

The unmade synthesis: the alerting system is a single integrated domain. A person who needs vibrotactile fire alerts also needs vibrotactile doorbell, telephone, and intruder alerts. Specifying vibrotactile for fire only leaves the same person without notification for all other alert types.

The seizure/photosensitivity conflict applies to all visual alerting, not …

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Jordan & Vanderheiden 2024 (ACM TACCESS) | 3 | NEU (photosensitive epilepsy) | All visual alerting items |
| BS EN 54-23:2010 | 5 | DEAF (fire VAD) | Multi-channel specification |
| NFPA 72-2022 | 5 | DEAF | Multi-channel specification |
| RNID / HLAA / Bufdir | Co-1/2 | DEAF (vibrotactile) | All alerting channels |

**Action required:** Specify unified multi-channel alerting: every alert event (fire, intrusion, doorbell, telephone, intercom) available through all three channels (visual + auditory + vibrotactile) simultaneously. Consistent channel specifications across alert types to enable pattern recognition. Extends CON-0014 from sleeping-area fire alarm to all alerting.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing for B-10 + all alerting items

---

---

## Connections CON-0131+ (Write-back from Opus batches, 2026-04-09)

### CON-0132

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** air-quality-voc-chemical-sensitivity-built-environment, biophilic-design-healthcare-workplace
**Target item(s):** BIO-01 through BIO-05, F-04
**Target population(s):** OFS/MCAS, DEM, NDV/MH
**Evidence tier:** Tier 4-5 (air quality BPC) + Tier 3 (biophilic BPC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Biophilic design provisions (BIO-series: indoor planting, nature views, natural materials) are therapeutic for DEM (reduced agitation — Al Khatib 2024 SR), NDV/MH (stress reduction — Ulrich), and NEU (ART/SRT restorative benefit). The air quality BPC specifies for OFS/MCAS spaces: "low-VOC, low-pollen species only; no strongly scented flowering plants." Additionally, F-06 (Fragrance-Free Policy) prohibits fragrance diffusers including any HVAC-integrated scent system.

Conflict: biophilic planting that serves DEM/NDV/MH may trigger OFS/MCAS symptoms. Flowering plants, aromatic herbs (lavender, rosemary — commonly recommended in DEM garden design), and high-pollen species are documented MCAS triggers.

Resolution: species-restricted planting list for shared OFS+DEM/NDV spaces. Permitted: foliage-only plants (ferns, pothos, snake plant), low-pollen succulents, sealed terrarium plantings. Prohibited: flowering plants, aromatic herbs, high-pollen grasses, plants with latex sap. Nature views through glazing (visual biophilia) serve all populations without air quality risk.

**Evidence basis:** air-quality BPC: OFS/MCAS fragrance/VOC/pollen triggers. biophilic BPC (Al Khatib 2024 SR, 61 sources): nature exposure therapeutic for DEM/NDV. Project-standards: DEM olfactory wayfinding is NOT an evidence-based specification; fragrance-free is the universal built environment specification.

**Action required:** Add species-restriction note to BIO-01/BIO-02 (indoor planting items): "Where OFS/MCAS populations co-occur, planting shall comply with F-04 air quality specification (low-VOC, low-pollen, no scented flowering species). Visual biophilia through glazing is the conflict-free alternative." Cross-reference BIO ↔ F-04.

**Disposition notes:** — Resolves a real specification conflict. Species restriction is the architectural equivalent of harm-asymmetry: MCAS reaction (physiological) > therapeutic planting benefit (psychological).

### CON-0142

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** thermoregulation-built-environment, air-quality-voc-chemical-sensitivity-built-environment
**Target item(s):** F-07, F-04
**Target population(s):** NEU/MS, OFS/MCAS
**Evidence tier:** Project-standards rule (2026-04-07)

**Connection:** Project-standards specifies 18–22°C working target for thermoregulation-impaired populations, with mechanical cooling as medically necessary in hot-humid tropical contexts. F-04 air quality specifies ≥15 L/s fresh air per person for OFS/MCAS spaces with no recirculated air without HEPA. In tropical contexts, these two specifications interact adversely: high fresh-air supply rates at 32°C+ ambient increase cooling load dramatically. The HVAC system must simultaneously cool to ≤22°C AND supply ≥15 L/s fresh air AND filter to MERV 13+ — this is an engineering coordination constraint that neither F-04 nor F-07 documents.

**Action required:** Part 8 (Engineering): add HVAC coordination note for tropical jurisdictions — cooling, ventilation, and filtration constraints from F-04 + F-07 are simultaneously binding. Engineering brief must specify all three. Cross-reference CON-0101 (HVAC type constraint).

