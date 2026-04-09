# Connection Scout — Opus BPC Cross-Reference Scan (Batch 3)
**Date:** 2026-04-09
**Model:** Opus 4.6
**BPCs read (this batch):** air-quality-voc, room-acoustic-performance, deaf-acoustic, therapeutic-lighting, neurodivergent, mental-health, reach-range-and-accessible-controls

---

## New Connections

### CON-0131

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** mental-health-built-environment (Opus synthesis 2026-03-30)
**Target item(s):** A-16, CON-0002
**Target population(s):** NDV/MH, NDV/AUT
**Evidence tier:** Tier 1 (Faerden 2022, van der Schaaf 2013, Wilson 2023 Co-1)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** **CON-0002 correction required.** CON-0002 (CONSUMED) proposes collapsing the MH de-escalation room into A-16, retiring the separate MH room concept. The MH BPC Opus synthesis (completed 2026-03-30, AFTER CON-0002 was applied) explicitly contradicts this: "These serve different clinical functions and cannot be combined. A single 'quiet room' fails MH users (who need exit sightline and staff-accessible de-escalation) and NDV users (who need acoustic isolation without staff presence)."

The MH BPC provides a detailed functional comparison:

| Parameter | MH de-escalation | A-16 sensory quiet |
|---|---|---|
| Clinical function | Crisis de-escalation; voluntary retreat | Sensory regulation; overstimulation recovery |
| Exit sightline | Required FROM inside TO exit (PTSD anti-entrapment) | Not specified |
| Staff access | Discrete monitoring required | Not required |
| Visual privacy | Required — no observation from common areas | Preferred, not required |
| Minimum area | ≥9 m² | ≥8 m² |

Wilson 2023 (Co-1) documents the failure mode: sensory rooms repurposed as de-escalation spaces are "clinically useless." Faerden 2022 (Cohen's d = 2.0 for user control in MH) — the largest single effect size in the entire BPC corpus — depends on the MH room meeting MH-specific requirements that A-16 does not.

**Evidence basis:** MH BPC Opus synthesis 2026-03-30. Wilson 2023 Co-1 (failure documentation). Faerden 2022 (Tier 1, effect size). van der Schaaf 2013 (n=23,868 across 199 wards — private space as primary variable).

**Action required:** (1) Flag CON-0002 as PARTIALLY INCORRECT — the multi-population expansion of A-16 (adding OFS, PAIN) is correct; the retirement of the separate MH room is incorrect per subsequent Opus synthesis. (2) Re-establish MH de-escalation room as a distinct item from A-16 — either as a separate item code or as a population-specific variant within A-16 that carries additional MH requirements (exit sightline, staff access, visual privacy). (3) Part 7 NR-HLT: both A-16 AND MH de-escalation room required in healthcare/psychiatric settings — they are not substitutes.

**Disposition notes:** — Evidence post-dates CON-0002 application. This is the most significant evidence-register inconsistency found during this scan.

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

### CON-0133

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** dementia-built-environment, neurodivergent-built-environment, intellectual-disability-built-environment-design, reach-range-and-accessible-controls
**Target item(s):** H-01, H-02, E-01 (door hardware)
**Target population(s):** DEM, NDV, IntD
**Evidence tier:** Tier 3-5 (DEM, NDV, IntD BPCs) + Tier 1-6 (controls BPC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** H-01/H-02 specify controls for MOB/UPL: reach range (400-1100mm), activation force (≤22.2N), lever hardware, no pinch/grip/twist. The controls BPC is entirely physical-access focused. Three populations have cognitive operability requirements undocumented in the controls specification:

**DEM:** Consistent placement (same switch position in every room); lever not rotary (rotary operation requires procedural memory); no multi-step sequences (each additional step loses ~30% of DEM users — inferred from CDM cognitive levels); colour contrast between control and wall (≥30% LRV per C-04).

**NDV:** Predictable, consistent response (no variable-speed dimmer behaviour); no ambiguous feedback states (a switch is either on or off — never "transitioning"); tactile confirmation of state; no audible click sounds >45 dBA (acoustic trigger).

**IntD:** Pictogram labels on all controls (light symbol, fan symbol, temperature symbol); single-action operation only; no combined controls (a switch that controls multiple circuits is cognitively inaccessible); placement at same height and same position in every room.

These are interface design requirements that the physical-access specification does not address. A DEM user who can reach a switch at 1000mm but cannot remember which switch does what, or an IntD user who can operate a lever but not interpret a three-way toggle, is functionally excluded by a specification that meets H-01.

**Evidence basis:** DEM BPC: consistent environment reduces confusion. NDV BPC: predictable, non-ambiguous interfaces. IntD BPC: pictogram + single-word signage; simplified interaction. Controls BPC: physical reach only; status PROVISIONAL; 16 jurisdictions NOT-RUN.

**Action required:** Add cognitive operability layer to H-01/H-02: (a) consistent placement across rooms (DEM, IntD); (b) single-action operation, no multi-step (DEM, IntD); (c) pictogram labelling (IntD); (d) unambiguous binary state (NDV); (e) colour contrast to wall ≥30% LRV (DEM, VIS). This is the highest-priority expansion for the controls-and-hardware topic — currently the thinnest in the coverage matrix (1 BPC, MOB only).

**Disposition notes:** — Fills the largest single topic gap in the coverage matrix.

---

### CON-0134

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** mental-health-built-environment
**Target item(s):** H-02, Part 7 NR-HLT
**Target population(s):** NDV/MH
**Evidence tier:** Tier 1 (Faerden 2022; van der Schaaf 2013)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Faerden 2022 reports Cohen's d = 2.0 for patient support and d = 1.7 for staff support when sensory modulation rooms are available in psychiatric inpatient settings. This is the largest single effect size for any built-environment intervention in the entire BPC corpus — larger than Clemson 2023 (fall prevention, 38% reduction), larger than CAPABLE (hospitalisation 0.43→0.23/year), larger than Sheffield (39% care hour reduction).

H-02 is already Tier 0 (CON-0017) but the MH evidence provides the strongest quantified justification for user environmental control of any population. The MH-specific additions not in H-02's current specification: (a) exit sightline from every occupied space — user must see the exit route at all times (anti-entrapment); (b) no locked-in perception — door latches must be user-operable from inside even in secure settings; (c) user control of door to own space (can close, can lock from inside).

van der Schaaf 2013 (n=23,868 across 199 wards) confirms private space per patient as the largest-effect design variable for reducing coercive measures — larger than staffing ratio, larger than therapeutic programme type.

**Evidence basis:** MH BPC: Faerden 2022 (Tier 1, d=2.0); van der Schaaf 2013 (Tier 1, n=23,868); Husum 2010 (Tier 1, n=1,016).

**Action required:** (1) Add MH-specific user control provisions to H-02 population overlay: exit sightline, no entrapment perception, user-operable locks from inside. (2) Part 7 NR-HLT: cite Faerden d=2.0 as governing evidence for sensory modulation room specification; cite van der Schaaf n=23,868 for private space per patient. (3) Part 1: reference d=2.0 as the strongest single effect size for environmental intervention — strengthens the case for built environment as primary intervention, not amenity.

**Disposition notes:** — The d=2.0 figure should be prominent in Part 1 evidence section and Part 11 economics.

---

### CON-0135

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** deaf-acoustic-built-environment, room-acoustic-performance
**Target item(s):** A-01, A-02, A-08, A-10
**Target population(s):** DEAF, ALL
**Evidence tier:** Tier 4-5 (IEC 60118-4, DIN 18041, deaf-acoustic BPC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** The deaf-acoustic BPC specifies Auracast (Bluetooth LE Audio) infrastructure as a DAR provision in all new assembly spaces, alongside IEC 60118-4 hearing loop systems. IEC 60118-17 (Auracast standard) is expected late 2027. During the transition period, dual provision (loop + Auracast-ready infrastructure) is best practice.

This is a DAR item not currently connected to Part 10 (DAR) or H-04 (digital infrastructure). The infrastructure requirement is physical: BLE access points at ceiling level in all assembly/reception spaces; conduit from AV distribution to BLE AP positions; power at each AP location. The cost at construction stage is trivial (conduit + outlet); the retrofit cost is significant (ceiling access in occupied assembly spaces).

Additionally, Auracast serves not only DEAF but also NDV (personal audio stream selection in multi-source environments), VIS (audio description channel), and DBL (residual hearing via personal receiver). It is a multi-population DAR provision.

**Evidence basis:** deaf-acoustic BPC: Auracast infrastructure provision (IEC 60118-17 expected 2027). DAR principle: construction-stage provisions preserve future capacity at negligible cost.

**Action required:** (1) Create DAR provision for Auracast-ready infrastructure in Part 10: BLE AP positions at ceiling level in all assembly, reception, and service counter spaces; conduit from AV distribution; power at AP locations. (2) Add to A-10 (assistive listening) as DAR supplement: "Auracast infrastructure provided alongside IEC 60118-4 hearing loop during technology transition period." (3) Cross-reference H-04 (digital infrastructure). (4) Add NDV, VIS, DBL as co-populations for personal audio stream provision.

**Disposition notes:** — Time-sensitive: IEC 60118-17 publication will trigger a specification update. DAR now preserves the option.

---

### CON-0136

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** reach-range-and-accessible-controls, pain-ofs-built-environment-design, ofs-built-environment
**Target item(s):** E-01, H-01
**Target population(s):** OFS, PAIN
**Evidence tier:** Tier 1 (AAATE 2016 door force study) + Tier 5 (PAIN/OFS BPCs)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Door force specification (≤30N preferred, ≤38N maximum) is coded for MOB (wheelchair user arm strength). OFS and PAIN are not coded despite clear clinical rationale: OFS energy conservation — every door push depletes the post-exertional malaise budget; cumulative door-opening through a building visit can trigger PEM. PAIN — joint loading on hands, wrists, and shoulders during manual door operation aggravates arthritic and fibromyalgia pain.

The AAATE 2016 study (Tier 1, 94.7% WC user acceptance at ≤30N) provides the force threshold. The clinical extension: for OFS, the threshold applies not because of arm strength limitation but because of cumulative energy expenditure. For PAIN, because of joint-loading pain. The specification value (≤30N) remains unchanged; the population coding expands.

Additionally: automatic door openers (specified as "best practice" for entrance doors) should be elevated to MANDATORY for all doors on primary circulation routes where OFS/PAIN populations are primary users. The clinical rationale: eliminating door-opening exertion entirely is the energy conservation specification, not merely reducing force.

**Evidence basis:** Controls BPC: ≤30N door force (AAATE 2016 Tier 1). OFS BPC: energy conservation at all interaction points. PAIN BPC: joint loading reduction. The force threshold is already correct; the population rationale extends it.

**Action required:** (1) Add OFS and PAIN as co-populations for door force specification (E-01, H-01). (2) Elevate automatic door openers from "best practice" to "mandatory on primary circulation routes" where OFS/PAIN are primary users. (3) Mechanism note: OFS door force is energy-budget, not strength; PAIN door force is joint-loading, not strength. Same specification value, different clinical rationale.

**Disposition notes:** — Zero-cost connection (population tag expansion). Automatic door elevation has cost implications.

---

### CON-0137

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** mental-health-built-environment
**Target item(s):** Part 7 NR-HLT (healthcare matrices)
**Target population(s):** NDV/MH
**Evidence tier:** Tier 1 (Weltens 2023)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** The MH BPC documents that exceeding bed capacity in psychiatric wards produces OR 5.36 for aggression (Weltens 2023, experience sampling method). This is a built-environment capacity specification: the number of beds per ward is a design parameter with a direct, large, quantified effect on safety outcomes. The OR is among the largest in the MH BPC evidence base — comparable to the absence of private space (van der Schaaf 2013).

No Part 7 NR-HLT specification currently addresses maximum bed count per ward as an accessibility parameter. Ward capacity is treated as a programming decision, not a design specification. The evidence says otherwise: over-capacity is an environmental barrier with measurable harm.

Additionally, the MH BPC identifies that ward-level environmental factors (capacity, private space, sensory modulation availability) govern coercive measure use MORE than patient-level factors or staffing. This inverts the typical clinical assumption that patient behaviour drives restraint use.

**Evidence basis:** MH BPC: Weltens 2023 (ESM, OR 5.36 for aggression when capacity exceeded). van der Schaaf 2013 (n=23,868 — ward design variables > staffing variables for coercion). Husum 2010 (n=1,016 — ward-level variation in coercion not explained by patient characteristics).

**Action required:** Part 7 NR-HLT: add maximum bed capacity specification for psychiatric wards as an environmental design parameter. Bed count is not merely a planning metric — it is a safety specification with OR 5.36 evidence. Cross-reference: private space per patient (van der Schaaf 2013), sensory modulation room (Faerden 2022 d=2.0). These three provisions (capacity limit, private space, sensory modulation) are the MH environmental intervention triad.

**Disposition notes:** — Novel specification type: occupancy capacity as environmental design parameter. May face pushback from facility managers; evidence is strong.

---

### CON-0138

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** true
**Source BPC slug(s):** room-acoustic-performance, neurodivergent-built-environment
**Target item(s):** A-01, A-02, A-08
**Target population(s):** NDV/AUT
**Evidence tier:** Tier 1 (Bettarello 2021, Caniato 2024) + Tier 3 (room-acoustic BPC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** CON-0039 proposes RT60 ≤0.3 s as Tier 0 universal for speech-critical rooms, based on DEAF evidence (Iglehart 2020). The room-acoustic-performance BPC documents that NDV/AUT evidence (Bettarello 2021, Caniato 2024) indicates existing standards (calibrated to neurotypical populations) are insufficient and that autistic users are "significantly more affected by modest background noise increases (52→55 dBA)." The BPC suggests sub-0.3s RT60 may be needed for NDV/AUT but no quantified target exists.

This creates a population-within-specification hierarchy for acoustic items:
- General population: 0.6 s (code compliance, Tier 6)
- DEAF/hearing devices: 0.3 s (Tier 0 per CON-0039)
- NDV/AUT primary spaces: <0.3 s (Tier 1 — specific value unquantified; ○ marker)

The practical implication: in NDV-primary spaces (autism schools, sensory rooms, A-16), the DEAF Tier 0 of 0.3 s is a floor, not a ceiling. Additional acoustic treatment beyond what satisfies DEAF requirements may be needed. Background noise threshold for NDV/AUT is also more stringent: the 3 dBA increase (52→55) that is perceptually negligible for neurotypical and minimally impactful for DEAF is functionally significant for NDV/AUT.

**Evidence basis:** room-acoustic-performance BPC: Bettarello 2021 (Tier 1), Caniato 2024 (Tier 1) — autistic populations significantly more affected by modest noise increases. NDV BPC Opus synthesis: "no internationally agreed quantified RT60 target specific to autistic users."

**Action required:** Add NDV/AUT acoustic annotation to A-01/A-02: "In NDV/AUT-primary spaces, RT60 ≤0.3 s (Tier 0) is a floor. Additional acoustic treatment to achieve lowest practicable RT60 and background noise level is recommended (○ — no quantified NDV/AUT-specific target; gap flagged for v11 research)." Cross-reference CON-0039.

**Disposition notes:** — MODERATE because no quantified NDV/AUT-specific target exists. The direction is clear; the value is not.
