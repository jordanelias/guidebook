# Synthesis Scan — Cross-Domain Specification Opportunities
**Date:** 2026-05-06 04:42
**Model:** Opus 4.6
**Method:** Granular scan of all BPC files (48), FDR files (30), Part 4 (78 items), Part 5 (11 conflicts + 4 UNRESOLV), Part 3 (synthesis framework), 251 connections, 32 OPEN P2 gaps. Cross-matched every quantified measurement, mechanism, framework, and finding against every other. Unmatched pairs identified by shared mechanism, shared measurement, or shared theoretical principle where the connection has not been explicitly made.

**Structure:** Matched pairs (Section A — previously identified) are listed for completeness; unmatched pairs (Section B — newly interpolated) are the primary deliverable; recombinations (Section C — multi-way interpolations producing novel synthesis) follow.

---

## A. MATCHED PAIRS (previously identified — included for register completeness)

These are synthesis opportunities already flagged by connections, ISW briefs, or prior session work. Included here as baseline.

| ID | Pair | Status | Target |
|---|---|---|---|
| A1 | 30° trunk lean → 380mm universal lower storage bound (FDR-BAB-05 × FDR-KIT-03 × reach-range) | ISW pending | Part 3 §3.4 universal rule |
| A2 | Power WC geometry package (FDR-BAB-04 × FDR-KIT-01 × FDR-ACG-02) | ISW pending | Part 4 preamble |
| A3 | OFS rest seating ≥480mm (FDR-ACG-01 Roxburgh Tier 1) vs standard 420mm | ISW pending | E-10, G-07 |
| A4 | Sensory relief space quantified physics (FDR-SRS-01) | ISW pending | A-16 |
| A5 | Cognitive wayfinding decision architecture (FDR-COGWAY-01/02) | ISW pending | D-04, D-08 |
| A6 | I-01 operability propagation (PENDING CON-0247–0252) | PENDING | All user-operated items |
| A7 | Proximal stabilisation surface for tremor (FDR-RRC-04) | ISW pending | H-01 |
| A8 | Hardware force/torque disaggregation (FDR-RRC-01) | ISW pending | I-01 |
| A9 | CMP-01 through CMP-06 compound interaction notes | ISW pending | G-03, E-10, G-08, Part 3 §3.10 |
| A10 | Kawa shared calm space Model B/C (FDR-ENV-05) | ISW pending | A-16 |
| A11 | Cross-room task surface unification (CON-0162) | CONSUMED-DEFERRED | Part 4 preamble |
| A12 | Unsupported values: A-04 20m, B-05 5m, A-09 0.1 m/s RMS | Flagged | Research or ○ marker |

---

## B. UNMATCHED PAIRS (newly interpolated)

### B-I. Shared mechanism, different populations — not yet linked

**B-I-01. Cognitive fatigue accumulation as universal compound rest interval modifier**
- Source A: CMP-02 (VIS + OFS) — cognitive fatigue from VIS tactile navigation accumulates faster than physical fatigue; rest intervals should be halved
- Source B: DEM wayfinding fatigue — DEM cognitive reserve depletes during navigation (PMC8725382); wayfinding in unfamiliar environments is cognitively effortful
- Source C: NEU/PCS — post-concussion cognitive fatigue follows same depletion pattern as OFS but via different mechanism (neurovascular uncoupling)
- **Interpolation:** Cognitive fatigue accumulation during navigation is a cross-population mechanism (VIS, OFS, DEM, NEU/PCS). The rest interval modifier isn't specific to VIS+OFS — it applies to ANY population with reduced cognitive reserve navigating via effortful strategy. The compound principle: whenever navigation is cognitively mediated (not automatic), rest intervals should be shorter than the physical-fatigue-only specification.
- **Specification target:** E-10 population note; Part 3 §3.10 synergy entry. Rest interval reduction factor for cognitive-load populations on unfamiliar routes.
- **Confidence:** MODERATE — mechanism is sound (cognitive fatigue is population-independent); specific halving factor from CMP-02 is extrapolated.

**B-I-02. Proximal stabilisation surface: tremor → extend to PAIN and NEU/PCS**
- Source A: FDR-RRC-04 — OT prescribes stable surface adjacent to controls for tremor users (forearm bracing)
- Source B: PAIN BPC — chronic pain populations brace against environmental surfaces during pain episodes; wall-mounted grab rails and counter edges provide incidental bracing
- Source C: NEU/PCS — post-concussion vertigo and ataxia; environmental bracing surfaces compensate for impaired postural control
- **Interpolation:** The "proximal stabilisation surface" principle extends beyond tremor. Three populations use the same environmental feature (horizontal surface at 900–1000mm AFF near controls and along corridors) for different clinical reasons. The specification should be population-agnostic: *horizontal bracing surface at 900–1000mm AFF within reach of all user-operated controls and at 6m intervals along primary circulation.*
- **Specification target:** New population note spanning H-01 (controls) and E-08 (corridor). Universal Mode candidate.
- **Confidence:** HIGH for mechanism; MODERATE for 6m interval (extrapolated from corridor rest seating data).

**B-I-03. Exit sightline as cross-population visual-access-to-destination principle**
- Source A: MH BPC — PTSD anti-entrapment: exit sightline FROM inside room TO exit (Faerden 2022; Wilson 2023)
- Source B: DEM BPC — toilet visibility from bedroom/occupied space (D-03: no navigation required to reach toilet)
- Source C: FDR-COGWAY-01 — visual confirmation of destination from ≥5m approach (cognitive wayfinding, PMC8725382 Tier 2)
- **Interpolation:** Three populations independently require the same spatial property — visual access to the next destination from the current position — for three different clinical reasons (PTSD fear of entrapment; DEM wayfinding failure; cognitive impairment route confirmation). This is a convergent design principle not yet named in Part 3: *destination visibility*. The principle: from any occupied position in the building, the next likely destination should be visible without requiring navigation decisions.
- **Specification target:** Part 3 §3.4 new synthesis principle; D-03 extension beyond toilets; MH de-escalation room specification.
- **Confidence:** HIGH — three independent Tier 1–3 evidence streams converge on the same spatial property.

**B-I-04. Velocity-sensitive hardware contraindication: spasticity → extend to tremor and PAIN**
- Source A: FDR UPL — spring-loaded levers that require rapid depression trigger extensor spasm in spastic UL (velocity-dependent mechanism)
- Source B: FDR-RRC-04 (tremor) — lever with return spring resets during sustained tremor hold, releasing prematurely
- Source C: PAIN — rapid-action hardware increases sharp pain response in hypersensitive hands (allodynia)
- **Interpolation:** Velocity-dependent hardware is contraindicated for three populations via three distinct mechanisms (spasm trigger, premature release, pain). The common specification: *all door and control hardware must be operable without velocity-dependent action (no spring-loaded mechanisms requiring rapid engagement)*. Magnetic latches and slow-return levers serve all three.
- **Specification target:** I-01 universal rule; cross-reference E-11 (automatic doors).
- **Confidence:** HIGH — all three mechanisms are clinically documented.

**B-I-05. Specular reflectance contraindication: DEM × VIS × NDV**
- Source A: FDR-LRV — polished/high-gloss floors create glare and puddle illusion for DEM; reflections misread as obstacles
- Source B: FDR-LRV — specular reflectance insufficient controlled by LRV alone; surface finish matters
- Source C: NDV — large glazed areas create uncontrolled light variation (Architizer); reflective floors create moving visual input
- Source D: Ecological psychology — reflective floors are misaffordances (signalling non-existent action possibilities — water, holes)
- **Interpolation:** Three populations (DEM, VIS, NDV) are harmed by the same physical property (specular/high-gloss surface finish) via different mechanisms (illusion, glare, visual overload). The ecological psychology framework explains WHY — specular surfaces are misaffordances. Current C-03 and B-08 address this partially but don't unify the cross-population rationale or invoke the misaffordance concept. The specification: *all floor and wall surfaces in occupied spaces must be matte (≤30 gloss units); specular finish is a misaffordance contraindicated across DEM, VIS, and NDV populations*.
- **Specification target:** B-08 refinement (add misaffordance rationale and multi-population justification); Part 3 misaffordance checklist.
- **Confidence:** HIGH — convergent evidence across three populations.

**B-I-06. Stair nosing dual-population rationale: VIS identification + PD gait cueing**
- Source A: FDR stair-ramp — stair nosings function as natural visual gait cues for PD (nosing line = transverse floor stripe); stairs are often SAFER than level corridors for PD
- Source B: VIS — nosing contrast ≥30 LRV (C-04) for step edge identification
- **Interpolation:** The same nosing contrast specification serves two populations via entirely different mechanisms (VIS: edge detection; PD: gait cueing). The PD rationale is currently absent from E-09 and C-04. Adding it strengthens the value-engineering resistance: nosing contrast isn't just a VIS safety feature — it's a PD gait-restoration feature. The compound reinforcement makes it harder to value-engineer out.
- **Specification target:** C-04 or E-09 population note adding PD cueing rationale.
- **Confidence:** HIGH — PD gait cueing from visual horizontal lines is Tier 2 evidence.

**B-I-07. Bilateral handrail as multi-mechanism provision**
- Source A: FDR stair-ramp — hemiplegia bilateral handrail mandatory (affected side unpredictable left/right; single-side rail serves 50%)
- Source B: FDR stair-ramp — OA bilateral handrail enables load-offloading (reduces knee joint load during descent)
- Source C: CMP-08 — triple compound (MOB+NEU/tremor+VIS) stair convergence confirms handrail continuity
- Source D: Ecological psychology — handrails as continuous haptic pathways (Turvey & Carello 1995)
- **Interpolation:** Bilateral continuous handrails serve FOUR different populations via FOUR different mechanisms: hemiplegia (laterality coverage), OA (load offloading), VIS/DBL (haptic navigation), tremor (proximal stabilisation). No single population's evidence alone justifies bilateral continuous handrails at all stairs — but the compound of all four makes it an overwhelming Universal Mode specification. This recombination should be documented in Part 3 §3.10 as a paradigm example of how single-population evidence compounds into Universal Mode specification.
- **Specification target:** Part 3 §3.10 new convergence example; reinforces existing E-03/stair provision.
- **Confidence:** HIGH — four independent evidence streams.

### B-II. Same measurement, different rooms — not yet unified

**B-II-01. RT60 ≤0.4s multi-population convergence**
- DEAF speech intelligibility (BS 8300, DIN 18041)
- NDV/AUT sensory relief (FDR-SRS-01)
- MH de-escalation room (MH BPC)
- A-16 sensory quiet room (PAS 6463)
- PAIN ambient acoustic comfort (pain-ofs BPC)
- **Interpolation:** RT60 ≤0.4s appears independently across five population evidence streams. This is the strongest acoustic specification convergence in the guidebook. Current state: each item specifies RT60 ≤0.4s independently. The unification: RT60 ≤0.4s is a cross-population acoustic constant for occupied spaces where sensitive populations are primary users. It should be stated once as a Part 4 Category A preamble universal acoustic target, with individual items cross-referencing rather than restating.
- **Specification target:** Category A preamble; reduces specification sprawl.

**B-II-02. ≤22.2N force as universal operability constant**
- ADA §309.4 (push-button actuator)
- FDR door hardware (one-hand pull/push threshold for UPL)
- FDR RRC-01 (control activation force)
- Fold-down grab bar deployment (≤10N preferred but ≤22.2N maximum)
- **Interpolation:** 22.2N (5 lbf) appears as the maximum acceptable force in four independent contexts. But FDR-RRC-01 documents three distinct force TYPES (rotational torque ≤3.16 N·m, linear push/pull ≤66.7N for panic hardware, activation force ≤22.2N). The 22.2N constant is the ACTIVATION force — the force for fine-motor contact operations. The unified specification: *all user-activated controls and mechanisms ≤22.2N activation force; panic/emergency hardware ≤66.7N linear force; rotational hardware ≤3.16 N·m torque*. Three-tier force specification replaces single generic limit.
- **Specification target:** I-01 disaggregated force specification.

**B-II-03. 380mm–1200mm AFF as universal accessible storage envelope**
- FDR-BAB-05 bedroom: lower bound 380mm (30° trunk lean threshold)
- FDR-KIT-03 laundry: lower bound 380mm (same mechanism)
- Reach-range BPC: upper bound 1220mm (ANSI A117.1)
- FDR-RRC-05: bilateral UPL upper bound = shoulder height of seated user (~1050–1200mm)
- PVA SCI CPG: NO overhead reach zone for bilateral UPL
- **Interpolation:** The accessible storage envelope is 380mm–1200mm AFF regardless of room type. Below 380mm = fall risk from trunk lean. Above 1200mm = forward reach limit exceeded. This envelope appears independently in bedroom, kitchen, laundry, and bathroom FDRs. Unified specification: *all user-accessed storage in accessible dwellings shall be within the 380–1200mm AFF envelope. Items below 380mm or above 1200mm AFF are not independently accessible to seated users with trunk instability. Mode S adjusts upper bound to individual shoulder height.*
- **Specification target:** Part 4 preamble or new G-category item (universal storage envelope).

### B-III. Theoretical framework → specification gap — not yet operationalised

**B-III-01. Misaffordance = DEM visual illusion = ecological psychology → unified audit tool**
- Ecological psychology BPC: misaffordances (signalling non-existent action possibilities) are actively harmful
- DEM BPC: dark mats perceived as holes; reflective floors perceived as wet; glass doors perceived as open
- NDV: visual complexity from reflective/patterned surfaces
- **Interpolation:** DEM visual illusions documented in the DEM BPC ARE misaffordances as defined by ecological psychology. The DEM literature describes them clinically; the ecological psychology framework explains them theoretically. Part 3 §3.13 (Sensory Coherence Audit Tool, currently GAP-CR-16) should incorporate a misaffordance checklist derived from both: *for each surface, does it signal an action possibility that does not exist? For each transition, does it signal a hazard that is not present?* This closes GAP-CR-16 by providing the theoretical content for the audit tool.
- **Specification target:** Part 3 §3.13 misaffordance audit protocol.
- **Confidence:** HIGH — theoretical framework (ecological psychology) + empirical evidence (DEM BPC) converge.

**B-III-02. Behaviour setting audit = sensory coherence audit → unified room validation protocol**
- Ecological psychology BPC: behaviour setting audit — confirm prescribed behaviour is achievable for all anticipated populations
- Part 3 §3.13: Sensory Coherence Audit Tool (GAP-CR-16) — verify sensory parameters are coherent across zones
- Kawa model: river channel audit — verify flow (well-being) is not obstructed by environmental barriers
- **Interpolation:** These are the same concept from three disciplinary traditions. The unified protocol: for each room, three questions — (1) can each anticipated population perform the prescribed activity? (behaviour setting); (2) are the sensory parameters (acoustic, lighting, thermal, olfactory) consistent with the population requirements? (sensory coherence); (3) are there environmental obstructions to well-being flow? (Kawa). This produces a single room-validation protocol applicable at DD and RFO stages.
- **Specification target:** Part 3 §3.13 — transforms from stub to full protocol.

**B-III-03. Competence-press model empirically validated by CMP audit results**
- Part 3 §3.2.2: competence-press model predicts that compound disability increases environmental press non-additively
- CMP-01 through CMP-08: compound interaction audits empirically test this prediction at item level
- **Interpolation:** The CMP results are the first empirical validation of the competence-press prediction within this guidebook. CMP-04 (DEM+VIS wayfinding, 3 antagonistic) confirms supra-additive press; CMP-06 (NEU+OFS sit-to-stand, 3 convergent) confirms that convergence is also possible. Part 3 §3.2.2 should cite the CMP audit results as internal validation. The CMP-04 SPECIFICATION-LIMIT flag is the strongest empirical evidence that the built environment has boundaries — precisely the competence-press prediction.
- **Specification target:** Part 3 §3.2.2 internal validation citation.

### B-IV. Population × room intersections not yet explored

**B-IV-01. NDV/MH + bedroom overnight: PTSD exit sightline × DEM overnight pathway convergence**
- MH BPC: PTSD exit sightline FROM inside room TO exit (anti-entrapment)
- FDR-BAB-07: DEM overnight wayfinding pathway lighting (continuous strip 300–400mm AFF, ≥5 lux, 2700–3000K)
- **Interpolation:** PTSD bedroom requires exit visibility; DEM bedroom requires illuminated pathway to exit. These converge: a lit pathway visible from the bed that leads to an exit satisfies both. The specification: *bed position in NDV/MH or DEM residential rooms must have unobstructed sightline to room exit door; continuous low-level pathway lighting (300–400mm AFF, ≥5 lux, 2700–3000K) from bed to exit door*. This is a compound convergence that produces a stronger specification than either population's requirement alone.
- **Specification target:** Part 6 residential matrix; G-09 overnight safety.
- **Confidence:** HIGH — both requirements are independently evidence-based.

**B-IV-02. OFS + PAIN intra-individual shower temperature conflict**
- OFS BPC: shower temperature ≤37°C (heat causes vasodilation, worsens orthostatic intolerance)
- PAIN/FMS BPC: warm bath ≥38°C (hydrotherapy Tier 1 evidence for pain management)
- **Interpolation:** OFS+PAIN co-occurrence creates an intra-individual shower temperature conflict analogous to UNRESOLV-04 (MS+FMS thermal). The built environment resolution: dual-zone wet room with thermostatic control allowing two temperature presets (≤37°C shower for OFS management; ≥38°C bath/seated shower for pain management). Both zones share the same wet room space but different water supply circuits. This should be flagged as UNRESOLV-05 or resolved via the dual-zone specification.
- **Specification target:** G-04 wet room OFS+PAIN compound note; Part 5 §5.3 potential UNRESOLV-05.
- **Confidence:** MODERATE — clinical mechanism is sound; dual-zone resolution is novel and untested.

**B-IV-03. DBL + bathroom wayfinding**
- FDR-DB-01: DBL tactile wayfinding requires continuous guidance TWSI from entry to all primary destinations with no gap
- DEM BPC: toilet visible from bedroom
- FDR-BAB-07: bedroom-bathroom overnight pathway
- **Interpolation:** DBL bathroom wayfinding is unspecified. The specification gap: continuous tactile guidance from bedroom to bathroom for DBL users. This requires TWSI guidance strip on bedroom-to-bathroom route (not just corridor routes), attention pattern at bathroom door threshold, and braille signage at bathroom entry. Currently no BPC or FDR addresses the bedroom-to-bathroom route as a tactile wayfinding segment for DBL.
- **Specification target:** K-02 extension (tactile map should include bedroom-bathroom route); Part 6 residential matrix DBL column.
- **Confidence:** MODERATE — extrapolated from FDR-DB-01 general principles to specific room pair.

**B-IV-04. PAIN + laundry: whole-body vibration from appliances**
- CON-0165: floor type is the single largest WBV determinant for wheelchair users (Larivière 2024); hard tile transmits maximum WBV
- PAIN/FMS BPC: vibration sensitivity; allodynia triggered by mechanical vibration
- FDR-KIT-03: laundry pedestal height (300–400mm) for seated access
- **Interpolation:** Laundry appliances on pedestal at 300–400mm transmit vibration through the floor to adjacent seated/wheelchair users. For PAIN/FMS populations, this vibration is a pain trigger. The specification gap: vibration isolation for laundry appliances in accessible dwellings. Anti-vibration pads beneath pedestal; resilient flooring in laundry zone; appliance location ≥1200mm from seated work position.
- **Specification target:** New laundry provision or F-category environmental quality item; Part 6 residential matrix.
- **Confidence:** MODERATE — mechanism is sound (PAIN vibration sensitivity + WBV research); specific distance threshold (1200mm) is extrapolated.

---

## C. RECOMBINATIONS (multi-way interpolations producing novel synthesis)

**C-01. Anti-token provision quality criteria for sensory spaces**
- Sources: Wilson 2023 MH (Co-1: sensory room repurposed from storeroom with no window, token equipment = clinically useless) + Kawa Model B (shared calm requires ≥12m², companion seating, natural light) + FDR-SRS-01 (minimum 4m², ≤35 dB(A), blackout, floor texture zoning, direct access) + NDV FDR (on-demand availability without prior request)
- **Recombination:** Four independent evidence streams converge on a quality standard for sensory/calm spaces that current A-16 does not specify. The anti-token provision: a sensory space that is (a) <4m², (b) has no natural light access, (c) lacks acoustic treatment, (d) requires advance booking, or (e) is repurposed from storage is NOT an A-16-compliant provision. This produces a minimum quality threshold checklist for A-16 that prevents the documented failure mode.
- **Specification target:** A-16 minimum quality checklist.

**C-02. DEM stage-specific wayfinding × VIS learned-route × ecological psychology affordance transition**
- Sources: DEM BPC Opus note (early dementia = diversity/landmarks; advanced dementia = predictability/regularity) + VIS BPC (learned-route wayfinding requires consistency) + ecological psychology (affordances are organism-specific — the same environment affords different things to different cognitive stages)
- **Recombination:** DEM early-stage and VIS wayfinding CONVERGE on distinctive landmarks at decision points. DEM advanced-stage and VIS CONVERGE on spatial predictability and consistency. The apparent DEM divergent finding (symmetry vs. diversity) resolves when stage is considered: the wayfinding strategy changes as dementia progresses, and each stage shares a convergence partner with a different population. This means Part 6 DEM residential matrices should specify BOTH landmark diversity AND spatial regularity, with a stage-transition note: early stage uses landmarks; advanced stage uses spatial regularity; VIS benefits from both simultaneously.
- **Specification target:** D-01, D-04 stage-specific notes; Part 3 §3.10 convergence entry.

**C-03. Capacity management × privacy × minimum floor area derivation**
- Sources: Weltens 2023 (OR 5.36 exceeding bed capacity → aggression) + van der Schaaf 2013 (private space per patient → reduced seclusion) + MH BPC (design occupancy = maximum occupancy)
- **Recombination:** Two Tier 1 findings (capacity and privacy) are currently stated as principles without a spatial parameter. The interpolation: if private space per patient reduces seclusion AND exceeding bed capacity increases aggression, then a minimum floor area per patient is derivable. The specification: *minimum bedroom floor area in MH inpatient settings = single occupancy room, ≥12m² (person + support worker + unobstructed exit path + personal environmental control zone)*. The 12m² derives from MH de-escalation room ≥9m² + single bed + bedside furniture. This converts two Tier 1 principles into a spatial specification.
- **Specification target:** Part 7 NR-HLT (healthcare) matrix; potential new G-category item for MH bedroom sizing.
- **Confidence:** MODERATE — principles are Tier 1; spatial derivation is inferential.

**C-04. Satin > peened wet grip (FDR fold-down grab bar) × G-03 finish specification × I-01 hardware finish**
- Sources: FDR fold-down grab bar — Bobrick Advisory TB-108: satin finish provides 10% more traction than peened finish under wet conditions (ASTM F2961 testing, Bureau Veritas) + G-03 current spec (no finish specified beyond "no knurled") + I-01 hardware (no surface finish spec)
- **Recombination:** The counterintuitive finding (smooth satin > textured peened in wet grip) contradicts practitioner assumption that textured = safer. This has specification implications beyond grab bars: all hardware in wet areas (door handles, controls, grab rails) should specify satin or brushed finish, NOT peened or heavily textured. The evidence is Tier 3 (manufacturer-commissioned independent test, ASTM protocol). If confirmed, this changes the finish specification for G-03, I-01 (bathroom hardware), and I-03 (bathroom UPL provisions).
- **Specification target:** G-03 finish note; I-01 wet-area hardware finish.
- **Confidence:** MODERATE — single test source (ASTM F2961); counterintuitive finding needs replication flagging.

**C-05. Thermal load from exertion during corridor traversal**
- Sources: F-07 (thermal zoning ≤18°C ambient for MS) + E-10 (rest seating on routes) + OFS BPC (heat intolerance, orthostatic worsening with exertion) + E-08 (corridor clear width) + FDR stair-ramp (ramp preference over stairs for OA on joint-load grounds)
- **Recombination:** Movement through a building generates metabolic heat. For thermoregulation-impaired populations (MS, SCI, OFS), corridor traversal is not thermally neutral — it raises core temperature. Current specifications treat thermal environment (F-07/F-08) and circulation (E-08/E-10) independently. The interpolation: rest seating on circulation routes should be coordinated with thermal zoning. Rest points should be in thermally cool zones (≤18°C or air-movement zones) so that the rest period also provides thermal recovery. The specification: *rest seating positions on primary routes to be located at or adjacent to thermal cool points (air movement outlet, window opening, or cool-zone boundary) where thermoregulation-impaired populations are anticipated occupants*.
- **Specification target:** E-10 × F-07 coordination note; Part 5 worked example.

**C-06. Fluorescent prohibition: three independent mechanisms converging**
- Sources: NDV FDR (visual flicker 50/60Hz trigger + audible hum — dual sensory trigger) + FDR visual-fire-alarm-seizure-safety (LED with low-frequency PWM dimming can introduce flicker in PSE provocative range 3–30Hz) + B-03/B-04 existing specification (flicker-free LED)
- **Recombination:** Fluorescent prohibition is currently framed as an NDV provision (B-03). The PSE FDR adds a second independent rationale: LED replacements with low-frequency PWM dimming can INTRODUCE flicker in the seizure-provocative range if not specified correctly. The specification gap: B-03 prohibits fluorescent but doesn't specify the LED replacement requirement — PWM frequency must be >3000Hz or DC-driven. Without this, B-03 compliance (LED replacement) can create a NEW hazard (PSE-range flicker). The unified specification: *no fluorescent or CFL luminaires; LED luminaires must be DC-driven or use PWM dimming frequency >3000Hz to avoid PSE-range flicker (3–70Hz)*. IEEE 1789 is the reference standard.
- **Specification target:** B-03 refinement (add PWM frequency requirement and PSE rationale).

**C-07. High-contrast architectural patterns as PSE environmental trigger × NDV visual complexity × DEM visual illusion**
- Sources: FDR visual-fire-alarm — high-contrast regular patterns (stripes >1 cycle/degree) trigger seizures in ~30% of PSE individuals (PMC5438467 Tier 2) + NDV BPC — visual complexity from patterned surfaces + DEM BPC — patterned floors associated with +15% falls (DSDC 2024)
- **Recombination:** Three populations are harmed by the same environmental feature (high-contrast regular patterns on large surfaces) via three different mechanisms (PSE seizure trigger, NDV sensory overload, DEM fall risk from visual illusion). Current C-03 addresses pattern avoidance for DEM and NDV but does NOT cite the PSE seizure mechanism. Adding PSE converts C-03 from a comfort specification to a SAFETY specification — pattern avoidance prevents seizures, not just sensory discomfort. This elevates the evidence tier and increases value-engineering resistance.
- **Specification target:** C-03 add PSE population with Tier 2 seizure evidence.

---

## D. SPECIFICATION-LIMIT FLAGS (where evidence says built environment cannot resolve)

| ID | Compound/scenario | Limit | Resolution pathway |
|---|---|---|---|
| D-01 | CMP-04 DEM+VIS wayfinding | 3 antagonistic; no environmental wayfinding system resolves | Human assistance is Tier 2; Part 1 §1.9 scope boundary |
| D-02 | UNRESOLV-04 MS+FMS intra-individual thermal | Built environment cannot resolve internal physiological contradiction | OT clinical management; Part 9 §9.2.4 |
| D-03 | FDR-RRC-02 laterality-specific control placement | Affected side varies per individual; not standardisable | Mode S only |
| D-04 | FDR-RRC-03 prosthesis reach envelope | Too device-variable for architectural specification | Mode S only; existing reach range is baseline |
| D-05 | B-IV-02 OFS+PAIN shower temperature | Intra-individual conflict on same parameter | Dual-zone wet room or Mode S |

---

## E. PRIORITY RANKING — all pairs ordered by specification impact

| Rank | ID | Rationale |
|---|---|---|
| 1 | B-I-03 | Destination visibility — cross-population convergence of 3 Tier 1–3 streams; names a new design principle for Part 3 |
| 2 | B-I-07 | Bilateral handrail multi-mechanism — paradigm convergence example; strengthens Universal Mode |
| 3 | C-07 | PSE + NDV + DEM pattern avoidance — elevates C-03 from comfort to safety specification |
| 4 | C-06 | Fluorescent + PWM — closes a safety gap (LED replacement can introduce PSE-range flicker) |
| 5 | B-II-03 | Universal storage envelope 380–1200mm — unifies 4 rooms into one cross-room constant |
| 6 | C-01 | Anti-token quality criteria for A-16 — prevents documented failure mode |
| 7 | B-I-05 | Specular reflectance as misaffordance — ecological psychology operationalised |
| 8 | B-III-01 | Misaffordance audit tool — closes GAP-CR-16 with theoretical content |
| 9 | B-I-01 | Cognitive fatigue accumulation — universal compound rest interval modifier |
| 10 | C-05 | Thermal + circulation coordination — E-10 × F-07 novel coordination |
| 11 | B-I-02 | Proximal stabilisation extended — tremor → PAIN/NEU/PCS |
| 12 | B-I-04 | Velocity-sensitive hardware contraindication — three-population Universal Mode |
| 13 | B-IV-01 | PTSD + DEM bedroom overnight convergence |
| 14 | C-02 | DEM stage-specific × VIS wayfinding resolution |
| 15 | B-I-06 | Stair nosing dual rationale (VIS + PD) |
| 16 | C-04 | Satin > peened wet grip — counterintuitive finish specification |
| 17 | B-II-01 | RT60 ≤0.4s multi-population unification |
| 18 | B-II-02 | Force disaggregation 22.2N / 66.7N / 3.16 N·m |
| 19 | C-03 | MH minimum bedroom floor area derivation |
| 20 | B-IV-03 | DBL bedroom-bathroom tactile wayfinding |
| 21 | B-IV-04 | PAIN + laundry vibration isolation |
| 22 | B-III-02 | Unified room validation protocol (behaviour setting + sensory coherence + Kawa) |
| 23 | B-III-03 | Competence-press empirical validation by CMP results |
| 24 | B-IV-02 | OFS+PAIN shower temperature dual-zone |

---

## F. NEXT STEPS

1. **Commit this document** to `references/synthesis-scan-2026-05-06.md`
2. **Generate connections** for each B and C item (24 new CON entries)
3. **ISW sessions** for priority 1–8 items (specification drafting)
4. **Part 3 §3.10 update** with convergence examples from B-I-03, B-I-07, C-02
5. **Part 3 §3.13** populated with B-III-01 and B-III-02 content (closes GAP-CR-16)
6. **C-03 and B-03 refinement** for PSE safety elevation (C-06, C-07)
