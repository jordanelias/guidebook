## Part 4: Item Specification Library

<!-- evidence_density: Varies by category -->
> **Evidence density: varies by category** — ■ A (Acoustics): Tier 1 SR (Murgia 2023, Iglehart 2020) + Tier 4–6 standards; HIGH rated items: A-10, A-11. ■ E (Entry/Circulation): Tier 1 biomechanics (Keall 2015 Lancet RCT PMID:25255696, Koontz 2010 PMID:20434614) + standards convergence ≥24 jurisdictions. ■ G (Fixtures): Tier 1 (Levine 2024 PMID:38968649, Clemson 2023 Cochrane PMID:36893804). ▓ B (Lighting), D (Spatial Layout), F (Sensory Zoning), H (Controls): Tier 3–5. ░ I (Upper Limb): THIN-BASE — zero indexed studies on one-handed kitchen/bathroom design. GRADE confidence ratings applied to all 90 rated items (see item annotations). 5 items rated VERY LOW (F-02, F-06, G-01, K-01, K-03).


<!-- v10.0 scaffold — CO-0003 + CO-0004 applied.
     Source: v9.0 part05-a/b/cd/e/fg/hi/k (88_to_90).
     Changes applied at scaffold stage:
       - Duplicate E-06/E-07/E-08/E-09 block removed
       - F-05 marked RELOCATED → G-08 (CO-0003/D2-48)
       - F-07 Thermal Zoning + F-08 Thermal Transition placeholders added (CO-0003)
       - H-05 Nurse Call annotated as CO-0004 new item
       - I-04 Ceiling Hoist placeholder replaces old Bathroom Drainage (CO-0004/D2-30)
       - New items (E-10rev, E-12, E-13, E-14, G-08, G-09, B-12) appended from working/item-specs-final
       - E-15 Changing Places appended from v10 e14 file
     PENDING (edit pass required):
       - A-17 absorption into G-02 (D2-24)
       - C-03+C-06 merger (D2-22)
       - B-03+B-04 merger (D2-23)
       - Category J deletion (J items → Supp Vol Part 4)
       - G-08 populated from F-05 content (D2-48)
       - All 93 CON connections applied (item-specification-writer pass)
       - D2-41 PAIN/OFS audit on every item
       - All evidence tier markers reviewed
-->

*(Item codes use category prefix + two-digit number. Bare codes only — no volume-part prefix.)*

<!-- CON-0011 [HIGH]: Systematic pass required — insert DBL and DEM/NDV[IntD-proxy] (via DEM/NDV proxy per CO-0002) into all applicable room matrix items. Resolves 15+ gaps in single operation. Execute in Part 6/7 matrix edit pass. -->

<!-- CON-0018 [HIGH]: Essential facility sightline → Universal Mode residential provision. WC/bathroom door visible from main living area without navigational decision points. Add to D-03 (Toilet Visibility). -->

<!-- D2-41 STANDING INSTRUCTION: Every Part 4 item requires PAIN/OFS population audit. Where PAIN or OFS applies based on mechanism (heat, cold, vibration, exertion, fragrance sensitivity), add population code + THIN-POPULATION-SPEC disclosure. Item-specification-writer pass required for all 85 items. -->

## CATEGORY A: ACOUSTICS

All RT60 specifications are for the 500 Hz octave band in the occupied condition unless stated otherwise. NC ratings are single-number noise criterion measurements. STI = Speech Transmission Index (≥0.5 = good speech intelligibility). STC = Sound Transmission Class (partition isolation rating). All hearing loop specifications: IEC 60118-4:2014+AMD1:2017.

<!-- Citation mining 2026-05-04: Evidence base for RT60 ≤0.3s strengthened by three new sources:
     ASI-06 (Cueille 2022, R Soc Open Sci): HI penalty quantified at 18dB SRT increase (RT 0→1s) vs 10dB NH
     ASI-07 (Korean 2022, Buildings): Elderly incomplete-hearing — RT60 >0.6s degrades speech scores
     ASI-08 (2024 SR, PMC11384524): 23 studies confirm NH adapt to reverberation but HI do not — supports FIXED RT specification
     Combined with existing Murgia 2023 SR (ASI-01, now GREY-resolved: DOI:10.1044/2022_LSHSS-21-00181):
     RT60 >0.6s prevents 100% speech perception even at high SNR. The 0.6s value is confirmed as FAILURE BOUNDARY, not design target.
     CON-0039 ISW action: elevate RT60 ≤0.3s to Universal Mode for all speech-critical rooms. -->

### A-01 Acoustic Buffer Zones at Noisy Adjacencies
<!-- CON-0135 [HIGH]: A-01/A-02/A-08/A-10 acoustic cluster: adjacency + panels + HVAC NC-25 + hearing loop IEC 60118-4 -->
<!-- CON-0138 [HIGH]: A-01/A-02/A-08 acoustic — MODERATE annotation; additional convergence evidence -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:NDV|DEM|NEU -->
<!-- grade_confidence: LOW — Standards convergence (PAS 6463, AS/NZS 2107, BB93); no RCT on adjacency planning. NC-25 target derives from Tier 5-6 standards. ≥10 jurisdictions confirm direction. -->

<!-- CON-0039 [HIGH]: RT60 ≤0.3 s (mid-frequency 500–2000 Hz) to be elevated to Universal Mode universal specification for all speech-critical rooms. Background noise ≤35 dBA; STI ≥0.5 at furthest listener position. Frame ≤0.6 s as outer failure boundary, not a compliant specification. Populations: ALL (DEAF speech intelligibility, NDV acoustic calm, DEM communication, NEU/PCS cognitive load). -->

**Applicable Groups:** ALL (especially NDV, PCS, AUT, NDV/SENS, DEM) · OFS · PAIN
<!-- CON-0069: acoustic buffer reduces noise load — OFS/PAIN energy conservation -->

**Description:** 5 m deep acoustic buffer zone between any noise-generating adjacency (kitchen, plant room, reception desk, circulation corridor) and primary occupied spaces serving sensory sensitive users. Buffer zone finishes: high NRC (≥0.85) ceiling panels; carpeted floor; no parallel hard surfaces. Background noise in primary space: NC-25 maximum.

**Specifications:**
Buffer zone depth: 3 m (minimum); 5 m (preferred)
Ceiling: NRC ≥0.85 acoustic panels throughout buffer
Floor: carpet or acoustic vinyl
Background noise target in sensitive space: NC-25 maximum
No parallel hard wall surfaces in buffer zone
Applicable: any space where DEM, PCS, AUT, or NDV/SENS users are primary occupants

**Retrofit cost note:** Retrofit penalty: LOW — PLANNING. Acoustic buffer zoning is a room-adjacency planning decision costing nothing at 
design stage. Retrofit requires spatial reorganisation, partition addition, room-use relocation, or mechanical decoupling at significant 
cost and disruption.

**Key citations:** British Standards Institution. (2022). PAS 6463:2022. BSI. Bettarello, F., et al. (2021). Applied Sciences, 11(9), 3942. WELL Building Institute. (2024). WELL v2. IWBI.

**Cross-reference:** A-02 (Acoustic Ceiling); A-08 (HVAC Noise); A-16 (Sensory Room)

**Evidence basis (OT):** EHP Framework (alter strategy); Dunn's Sensory Processing Model. The buffer zone alters the acoustic context to keep the sound level entering sensitive spaces below the neurological threshold at which sensory avoiding and sensory-sensitive users experience distress; the 3--5m depth and NC-25 target are calibrated to this threshold, not to code minimums.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Buffer Requirement | STC Between Spaces | Notes |
|---|---|---|---|---|
| US | ANSI S12.60 | Per STC table | STC ≥50 (classroom-corridor) | Schools only |
| UK | BB93 | Performance targets by room pair | DnT,w values by room pair | Mandatory England |
| DE | DIN 4109:2018 | R'w sound reduction index | By building type | — |
| AU | NCC Section F5 | Referenced | By building class | — |
| ISO | ISO 16283 | Measurement method | — | — |
| **Guidebook** | **A-01** | **Graduated zones** | **Beyond code** | **NDV sensory gradient** |

Guidebook's graduated acoustic buffer concept (high→low stimulation) exceeds all codes — no jurisdiction requires graduated sensory zoning.


### A-02 Acoustic Ceiling Panels (NRC ≥0.85) in Occupied Spaces
<!-- CON-0008 [HIGH]: A-02/A-08/A-13 acoustic convergence: RT60 + NC-25 + masking prohibition -->
<!-- CON-0039 [HIGH]: RT60 ≤0.3s Universal Mode universal for speech-critical rooms; background noise ≤35dBA; STI ≥0.60 -->
<!-- CON-0040 [HIGH]: Unified sensory environment system: Dunn profiles → spatial zones → quantified parameters -->
<!-- CON-0122 [HIGH]: A-02 NRC ≥0.85 → STI ≥0.60 performance criterion (NRC = procurement proxy only) -->
<!-- CON-0135 [HIGH]: A-01/A-02/A-08/A-10 acoustic cluster: adjacency + panels + HVAC NC-25 + hearing loop IEC 60118-4 -->
<!-- CON-0138 [HIGH]: A-01/A-02/A-08 acoustic — MODERATE annotation; additional convergence evidence -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:NDV|DEM|NEU -->
<!-- grade_confidence: MODERATE — Bettarello et al. 2021 (Applied Sciences, Tier 3) provides RT60+NRC data for ASD environments. Multiple standards confirm NRC ≥0.85 as procurement proxy. Note: STI ≥0.60 is performance criterion per A2 reconciliation. -->

<!-- CON-0040 [HIGH]: Add OFS, PAIN to Applicable Groups (central sensitisation → auditory hyperalgesia). Mark ○ THIN-POPULATION-SPEC per D2-41. Evidence: pain-ofs-built-environment-design BPC FDR + acoustic sensitivity literature. -->

**Applicable Groups:** ALL (especially NDV, DEM, MH, PAIN, OFS) · DEAF · NEU/PCS
<!-- CON-0039: CON-0039: RT60 ≤0.3 s mid-frequency Universal Mode for speech-critical rooms — serves DEAF/NDV/DEM/NEU simultaneously -->

**Description:** Acoustic ceiling panels with NRC ≥0.85 installed in all primary occupied spaces — open-plan offices, classrooms, therapy rooms, communal areas, circulation corridors. Combined with A-01, A-05, and A-17 to achieve target RT60.

**Specifications:**
NRC ≥0.85 on all ceiling panels in occupied spaces
Coverage: 80% of ceiling area (not spot treatment)
Corridor ceilings: NRC ≥0.75 minimum
Where DEM or NEU/acquired brain injury is primary occupant group: NRC ≥0.90 (clinical requirement; ISO 3382-2)
Post-installation RT60 measurement at 500 Hz required

**Retrofit cost note:** Retrofit penalty: LOW. Acoustic ceiling panels are surface-applied and can be installed post completion without structural intervention. Retrofit penalty is primarily labour on a finished ceiling surface. See Part 12 §12.4.1.

**Key citations:** Bettarello, F., et al. (2021). Applied Sciences, 11(9), 3942. British Standards Institution. (2022). PAS 6463:2022. BSI.

**Cross-reference:** A-01 (Buffer Zone); A-05 (Carpet); A-16 (Sensory Room)

**Evidence basis (OT):** Dunn's Sensory Processing Model. RT60 reduction via ceiling treatment directly lowers the cumulative acoustic load experienced by sensory-avoiding and sensory-sensitive users, reducing the neurological effort cost of occupying the space and preserving cognitive and physical energy for the primary occupation.

**FDR-IntD-02 [Tier 1–3]:** Hyperacusis is prevalent in IntD-associated syndromes — Down syndrome (Widen et al. 2013, *Int J Audiol* Tier 3), Williams syndrome (Levitin et al. 2005, *Nature Neuroscience* Tier 1), Fragile X syndrome (Castrén et al. 2003 Tier 3). ● IntD-occupied educational and residential spaces should apply the NDV acoustic specification (RT60 ≤0.4 s, NC-25 background noise — A-02, A-08) as the governing acoustic standard rather than the general occupancy standard. DEM/NDV[IntD-proxy] routing applies.

**Jurisdiction comparison:** US ANSI S12.60 and UK BB93 reference ceiling absorption but do not specify NRC ≥0.85. DE DIN 18041 specifies absorption coefficients by room type. Guidebook's NRC ≥0.85 exceeds all code thresholds.


### A-03 Acoustic Door (STC ≥35) at All Sensitive Space Boundaries
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:NDV|DEM|DEAF -->
<!-- grade_confidence: LOW — ISO 10140-2 and BS 8300 confirm STC ≥35–45 dB direction. No RCT on partition type effect for disability populations specifically. Tier 5-6 standards convergence. -->

**Applicable Groups:** AUT, PCS, DEM, MH, SENS · OFS · PAIN · NDV
<!-- CON-0075: STC≥35 door reduces exertion from noise processing -->

**Description:** Acoustic door with STC ≥35 at all boundaries between noise-generating and noise-sensitive spaces. Includes: solid-core door leaf; acoustic perimeter seal; acoustic threshold seal; no letter box or undercut that bypasses the acoustic seal.

**Specifications:**
Door leaf: STC ≥35 (laboratory rating); field target STC ≥32
Perimeter seal: full four-side compression seal
Threshold seal: drop-seal or sweep
No letterbox penetrations; no undercuts ≥ 3mm
Closer: hydraulic door closer specified

**Retrofit cost note:** Retrofit penalty: LOW -- MODERATE. Acoustic door replacement is a moderate retrofit; achieving STC ≥35 requires 
full frame and threshold sealing which may require opening up surrounding construction. At design stage, specification cost is near-zero. See Part 12 §12.4.3.

**Key citations:** British Standards Institution. (2022). PAS 6463:2022. BSI. ISO 10140-2:2010. Acoustics Laboratory measurement of sound insulation. ISO.

**Cross-reference:** A-01 (Buffer Zone); A-14 (Double-Leaf Partition); A-16 (Sensory Room)

**Evidence basis (OT):** EHP Framework (prevent strategy); Dunn's Sensory Processing Model. The acoustic door implements EHP's 'prevent' intervention by eliminating the pathway through which auditory triggers travel to sensory sensitive occupants; STC ≥35 is the minimum attenuation required to reduce noise from an adjacent NC-40 zone to the NC-25 target within.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Min STC (sensitive) | Seal | Notes |
|---|---|---|---|---|
| US | ANSI S12.60 | STC ≥35 (classroom) | Drop seal recommended | Schools only |
| UK | BB93 | Rw ≥30 (classroom door) | Perimeter seal | — |
| DE | DIN 4109 | Rw by application | — | — |
| **Guidebook** | **A-03** | **STC ≥35** | **Full perimeter seal** | **All sensitive spaces** |


### A-04 Acoustic Zoning: Graduated from Arrival to Primary Occupation
<!-- design_stage_lock: SD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:NDV|DEM -->
<!-- grade_confidence: VERY LOW — Sensory gradient concept: PAS 6463 Tier 4 + Kaplan & Kaplan 1989 (environmental psychology, Tier 3 adjacent). No built-environment RCT. Expert consensus for spatial sequencing specification. -->

**Applicable Groups:** ALL · OFS · PAIN
<!-- CON-0076: graduated acoustic zones allow OFS/PAIN to self-select low-noise areas -->

**Description:** The building journey from arrival to primary occupied space is designed with progressively decreasing acoustic load.

Entry/reception: highest acoustic load tolerated. Primary occupied spaces: lowest acoustic load. No abrupt acoustic step-change.

**Specifications:**

Entry zone: NC 35 acceptable

Transition zones: NC 30

Primary occupied spaces: NC 25 (sensitive populations); NC 30 (general)

No single zone transition 
NC-10 change

Restorative intervals: at least one acoustic low-point per 20m of primary journey

**Retrofit cost note:** Retrofit penalty: LOW — PLANNING. Acoustic zoning through graduated material and layout planning is zero-cost at design stage. Retrofit requires redecoration, material replacement, and possible spatial reconfiguration. See Part 12 §12.4.1.

**Key citations:** Kaplan, R., \& Kaplan, S. (1989). The experience of nature. Cambridge University Press. British Standards Institution.

(2022). PAS 6463:2022. BSI.

**Cross-reference:** F-01 (Sensory Gradient); A-01 (Buffer Zones);

[VI-02 — retired code] (Sensory Budget)

**Evidence basis (OT):** EHP Framework (alter strategy); PEOP Model.

Graduated acoustic zoning alters the context systematically across the building journey so that the environmental acoustic demand progressively decreases as the user approaches the primary occupation space, matching environmental demand to functional capacity and expanding the performance range across the full journey.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Classroom RT (general) | Classroom RT (HI) | Background Noise |
|---|---|---|---|---|
| US | ANSI/ASA S12.60-2010 | ≤0.6s (<283m³); ≤0.7s (283-566m³) | **≤0.3s** | ≤35 dBA |
| UK | BB93 (mandatory England) | By room type | Lower targets | By room type |
| DE | DIN 18041:2016 | By room type and use | — | By room classification |
| NO | NS 8175:2019 | Acoustic classification system | — | By class (A-D) |
| AU | AS/NZS 2107:2016 | Recommended design levels | — | By space type |
| ISO | ISO 3382-2:2008 | Measurement method | — | — |
| **Guidebook** | **A-04** | **≤0.6s** | **≤0.3s (DEAF population)** | **≤35 dBA** |

US ANSI S12.60-2010 is the only standard specifying separate RT for hearing-impaired children (0.3s). UK BB93 is the most prescriptive mandatory standard. DE DIN 18041 is the most comprehensive room acoustic standard.


### A-05 Carpet in Corridors and Occupied Spaces (Where VIS Navigation Maintained)
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: LOW — BS 8300, PAS 6463 recommend carpet in corridors. Bettarello 2021 confirms acoustic benefit (RT60). No RCT on carpet vs hard floor for disability outcomes. Tier 4-5. -->

**Applicable Groups:** NDV, DEM, PAIN, MH, OFS

**Description:** Carpet with NRC 0.20--0.35 in corridors and primary occupied spaces reduces footstep impact noise, chair noise, and background acoustic load. Design tension with A-15 (acoustic differentiation as VIS navigation aid) must be resolved by maintaining texture contrast at key corridor junctions.

**Specifications:**

Pile height: 4--6 mm (low pile preferred — flush with hard floor transitions — 3 mm)

NRC 0.20--0.35

PTV (Pendulum Test Value): ≥36 wet (slip resistance confirm with manufacturer)

Chair feet: specify rubber/felt pads to supplement acoustic benefit

At VIS navigation junctions: hard floor strip 200--300 mm wide to maintain acoustic differentiation (A-15)

**Retrofit cost note:** Retrofit penalty: LOW. Carpet specification is a finish decision. Retrofit requires floor covering replacement.

Principal retrofit consideration: accessibility compatibility — slip resistance, wheelchair rolling resistance, and LRV contrast. See Part

VIII §8.4.1.

**Key citations:** British Standards Institution. (2022). PAS

6463:2022. BSI. CNIB Foundation. (2024). Clearing our path. CNIB.

**Cross-reference:** A-15 (Acoustic Differentiation — VIS navigation); [VI-08 — retired code] (Proprioceptive Design)

**Evidence basis (OT):** Dunn's Sensory Processing Model; Biomechanical FOR. Carpet's NRC 0.20--0.35 reduces impact noise and chair movement noise that fall in the frequency ranges most aversive to sensory-sensitive and sensory-avoiding users; the specification of low pile (≤6mm) with flush transitions also satisfies the Biomechanical FOR requirement that floor transitions present no trip hazard to mobility-impaired users.

**Jurisdiction comparison:** No code mandates carpet as acoustic treatment. UK PAS 6463 notes carpet aids acoustic absorption but may impede wheelchair propulsion. Guidebook specifies carpet only where VIS navigation aids (TWSIs) are maintained — balancing acoustic benefit against MOB access.


### A-06 Fabric Wall Panels (NRC ≥0.70) at Acoustic Reflection Points
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: LOW — Bettarello 2021 — RT60 improvement from absorption panels measured. No RCT on NRC ≥0.70 threshold. Tier 3 (single study) + Tier 5 standards. -->

**Applicable Groups:** NDV, DEM, PCS, MH · OFS · PAIN
<!-- CON-0078: NRC≥0.70 panels reduce noise load for OFS/PAIN cognitive effort -->

**Description:** Acoustic fabric wall panels (minimum 50 mm mineral wool core, fabric-wrapped) installed at primary acoustic reflection points: end walls of corridors; walls opposite windows; primary reception desk wall. Installed at 900--2400 mm height (within visual and acoustic influence zone).

**Specifications:**

NRC ≥0.70 at 500 Hz

Thickness: ≥50 mm mineral wool core

Height: 900--2400 mm (primary reflection zone)

Location: all identified acoustic reflection surfaces

Fabric: low-VOC, class 1 fire rating

**Retrofit cost note:** Retrofit penalty: LOW. Fabric wall panels are surface-applied and can be retrofitted without structural work using

standard fixing. See Part 12 §12.4.1.

**Key citations:** Bettarello, F., et al. (2021). Applied Sciences,

11(9), 3942.

**Cross-reference:** A-02 (Acoustic Ceiling); A-01 (Buffer Zone)

**Evidence basis (OT):** Dunn's Sensory Processing Model. Fabric panel placement at primary reflection points targets the specific acoustic conditions (strong specular reflections) that are most disruptive to sensory-processing regulation; the 900--2400mm height band places the treatment within the acoustic influence zone of seated and standing occupants.

**Jurisdiction comparison:** No code specifies fabric wall panels. DE DIN 18041 specifies absorption coefficients at reflection points. Guidebook's NRC ≥0.70 is an OT-derived threshold for speech intelligibility.


### A-07 Flutter Echo Elimination (Parallel Hard Surface Avoidance)
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: LOW — Flutter echo elimination: geometric principle (parallel hard surface avoidance). No disability-specific RCT. Acoustically sound; standards-based. Tier 5-6. -->

**Applicable Groups:** NDV, PCS, DEM · OFS · PAIN
<!-- CON-0079: flutter echo increases cognitive processing effort — OFS/PAIN energy cost -->

**Description:** No two parallel hard surfaces facing each other within 6 m unless one or both are treated to NRC ≥0.70. Flutter echo between parallel hard walls produces a repetitive, non-decaying reflection series that is particularly aversive for AUT and PCS users.

**Specifications:**

No untreated parallel hard surfaces within 6 m

Where parallel hard surfaces unavoidable: one surface treated NRC ≥0.70

Corridor end walls: acoustic panel or splayed geometry

Specular reflection check: acoustic consultant review at design stage

**Retrofit cost note:** Retrofit penalty: LOW -- MODERATE. Flutter echo elimination through non-parallel surface treatment is zero-cost at design stage. Retrofit requires material addition or surface modification; physical parallel wall removal is a structural intervention. See Part 12 §12.4.2.

**Key citations:** Bettarello, F., et al. (2021). Applied Sciences, 11(9), 3942. British Standards Institution. (2022). PAS 6463:2022. BSI.

BSI.

**Cross-reference:** A-02 (Ceiling); A-06 (Wall Panels)

**Evidence basis (OT):** EHP Framework (prevent strategy); Dunn's Sensory Processing Model. Flutter echo between parallel untreated hard surfaces produces a sustained, non-decaying reflection series that functions as an uncontrolled repetitive auditory stimulus; this item prevents its formation at source, implementing the EHP 'prevent' strategy before the stimulus reaches the neurological threshold for distress in AUT and PCS users.

**Jurisdiction comparison:** UK BB93 addresses flutter echo in school design. DE DIN 18041 §6 addresses room acoustic defects including flutter echo. No other code specifically targets flutter echo. Guidebook extends to all occupied spaces.


### A-08 HVAC Noise Control (NC-25 Maximum in Sensitive Spaces)
<!-- CON-0008 [HIGH]: A-02/A-08/A-13 acoustic convergence: RT60 + NC-25 + masking prohibition -->
<!-- CON-0039 [HIGH]: RT60 ≤0.3s Universal Mode universal for speech-critical rooms; background noise ≤35dBA; STI ≥0.60 -->
<!-- CON-0040 [HIGH]: Unified sensory environment system: Dunn profiles → spatial zones → quantified parameters -->
<!-- CON-0135 [HIGH]: A-01/A-02/A-08/A-10 acoustic cluster: adjacency + panels + HVAC NC-25 + hearing loop IEC 60118-4 -->
<!-- CON-0138 [HIGH]: A-01/A-02/A-08 acoustic — MODERATE annotation; additional convergence evidence -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: CRITICAL -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: MODERATE — NC-25 target: ANSI S12.60, DIN 18041, BS 8300 converge (≥6 jurisdictions). Plant room schematic-stage requirement is irreversible (NOT-RETROFITTABLE per Part 8). No RCT but strong standards consensus. -->

**Applicable Groups:** AUT, PCS, DEM, MH, OFS · PAIN
<!-- CON-0008: CON-0008: NC-25 background noise limit reduces exertion needed for communication — OFS/PAIN energy conservation -->

**Description:** HVAC system designed to achieve NC-25 or better at all air terminal devices in sensitive spaces (sensory rooms, DEM care spaces, therapy rooms, ABI recovery spaces). NC-25 is the single most commonly specified noise criterion in post-occupancy complaints from neurodiverse building occupants.

**Specifications:**

NC-25 maximum at all air terminals in sensitive spaces

NC-30 maximum in general occupied spaces

Duct sizing: low-velocity design (duct velocity ≤3 m/s at primary distribution)

Acoustic lining: rectangular supply ducts lined for ≥10 m from AHU

All mechanical plant: mounted on vibration isolation pads

**Retrofit cost note:** Retrofit penalty: MODERATE. HVAC noise control (NC-25) at design stage requires correct plant selection and ductwork specification. Retrofit requires silencer insertion, ductwork modification, or plant replacement — significant mechanical works. See Part 12 §12.4.2.

**Key citations:** British Standards Institution. (2022). PAS 6463:2022. BSI. ANSI/ASA S12.60:2010. Acoustical performance criteria for schools. ASA.

**Cross-reference:** A-01 (Buffer Zone); A-16 (Sensory Room); H-02 (Individual Environmental Control)

**FDR-IntD-02 [cross-ref]:** In IntD-occupied settings apply NC-25 target (this item) as governing acoustic specification — same basis as NDV. ○ Coordinate with F-07 HVAC system type: forced-air systems are the primary source of NC exceedance.

**Evidence basis (OT):** Dunn's Sensory Processing Model. NC-25 is the noise criterion below which continuous background HVAC noise ceases to function as a sensory trigger for the majority of sensory-avoiding and sensory-sensitive users; this specification operationalises Dunn's model by translating 'reduce neurological threshold exceedance' into a measurable acoustic design parameter.

**CON-0101 [HIGH]:** HVAC system type is the primary determinant of achievable NC level. NC-25 constrains HVAC system selection — coordinate with F-07 thermal zoning strategy. ● Forced-air systems are contraindicated for NEU/OFS spaces per ms-thermal BPC (acoustic and airborne trigger); radiant heating achieves NC-25 without forced-air noise contribution. For SCI populations, radiant systems additionally avoid ambient heat load increase in cooling-critical environments [thermoregulation-built-environment BPC — PROVISIONAL]. Where F-08 specifies exposed thermal mass (concrete ceiling), additional acoustic absorption is required to maintain NRC ≥0.85 at ceiling — coordinate ceiling treatment zones with thermal mass zones.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Sensitive Spaces | Classrooms | Healthcare | Offices |
|---|---|---|---|---|---|
| US | ASHRAE / FGI | NC-25 (healthcare) | ≤35 dBA (ANSI S12.60) | NC-25 to NC-35 | NC-30 to NC-40 |
| UK | BS 8233:2014 / BB93 | NR 25 | BB93 targets | HTM 08-01 | NR 35-40 |
| DE | DIN 4109 / VDI 2081 | — | DIN 18041 targets | — | ASR A3.7 |
| AU | AS/NZS 2107:2016 | — | By space type | — | 40-45 dBA |
| ISO | ISO 3382 / ISO 16283 | — | — | — | — |
| **Guidebook** | **A-08** | **NC-25** | **≤35 dBA** | **NC-25** | **NC-30** |

**Note:** NC (Noise Criteria) and NR (Noise Rating) are not directly equivalent — NC tends ~5 points lower than NR at same perceived level.


### A-09 HVAC Vibration Isolation (Floating Plant Room)
<!-- CON-0005 [HIGH]: A-09 vibration threshold + G-08 seated reach cluster (MODERATE) -->
<!-- THRESHOLD RESOLVED (citation-verifier + ISW, connection-scout Opus 2026-04-24 15:17): The prior 0.1 m/s RMS threshold was UNVERIFIED and has been replaced with ISO 2631-1 standard values. Garcia-Mendez et al. 2013 (J Spinal Cord Med 36(4):365-375, PMID:23820152, verified T3) found wheelchair users experience 0.83 ± 0.17 m/s² weighted RMS acceleration — exceeding ISO 2631-1 EAV (0.5 m/s²) and approaching ELV (1.15 m/s²) in community settings. Correct unit: m/s² (not m/s RMS). Correct threshold: ISO 2631-1 EAV = 0.5 m/s² (8h); ELV = 1.15 m/s² (8h). Floor type is the single largest WBV determinant (Garcia-Mendez 2013; Chénier & Aissaoui 2014 PMID:25276802). Specification should cite EAV 0.5 m/s² as the design target for vibration-sensitive populations. -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: CRITICAL -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: MODERATE — Garcia-Mendez 2013 PMID:23820152 (Tier 3, verified) confirms wheelchair users exceed ISO 2631-1 EAV (0.83 m/s² observed vs 0.5 m/s² EAV). EAV/ELV thresholds from ISO 2631-1 (Tier 4). Floor type confirmed as primary WBV determinant. MODERATE — no disability-specific building standard; specification derived from well-established occupational health standard applied to disability context. CON-0181 [HIGH]: extends population applicability to PAIN, NEU, OFS (connection-scout Opus 2026-04-24 15:17). -->

<!-- CON-0055 [MODERATE]: Cushioned/resilient flooring serves MOB (WBV reduction), PAIN (joint impact reduction per GAP-B4-09), NEU (fall impact mitigation). Currently MOB-only; PAIN and NEU clinical rationales documented in respective BPCs but not cross-referenced. -->
**Applicable Groups:** PAIN (fibromyalgia), NEU, NDV · OFS
<!-- CON-0005: HVAC vibration transmission triggers PAIN allodynia and OFS PEM; floating plant room eliminates pathway -->

**Description:** All mechanical plant serving buildings with fibromyalgia, PCS, or NDV users installed on vibration isolation pads (minimum 20 dB insertion loss at 16--250 Hz). Where plant is adjacent to sensitive spaces: floating plant room construction (floating concrete slab on spring isolators).

**Specifications:**

All rotating plant: vibration isolation pads with ≥20 dB insertion loss

Adjacent to sensitive spaces: floating slab on spring isolators

Pipe connections: flexible connections at all mechanical plant

Post-installation: vibration measurement at sensitive space floors  
(target: weighted RMS acceleration ≤0.5 m/s² per ISO 2631-1 EAV; older specification referenced 0.1 m/s RMS — incorrect unit, now superseded [CORRECTED: ISW Opus cross-check 2026-04-24 15:17; see threshold-resolved comment above])

**Retrofit cost note:** Retrofit penalty: HIGH — STRUCTURAL. Floating plant room specification cannot be retrofitted without rebuilding the plant room. Anti-vibration mounts and structural decoupling must be incorporated at construction stage. Among the highest-penalty items when deferred. See Part 12 §12.4.

**Key citations:** Desmeules, J., et al. (2003). Arthritis \& Rheumatism. [Vibration as fibromyalgia trigger.\] Staud, R. (2011). Curr Pain Headache Rep, 15(5), 338--343.

**Cross-reference:** A-08 (HVAC Noise); A-01 (Buffer Zone)

**Evidence basis (OT):** Biomechanical FOR. Vibration at 16--250 Hz is a documented biomechanical trigger for central sensitisation in

fibromyalgia (Desmeules et al. 2003; Staud 2011); the ≥20dB insertion loss target at these frequencies is derived from the vibration

amplitude required to remain below the sensitisation threshold for users with established widespread pain.

**Jurisdiction comparison:** US ASHRAE Handbook references vibration isolation. UK CIBSE Guide B covers plant vibration. DE VDI 2062 vibration isolation. No code addresses vibration isolation as an accessibility provision — guidebook derives from NDV/NEU sensory sensitivity.


### A-10 Counter Hearing Loop (Induction Loop at Reception/Service Counter)
<!-- CON-0135 [HIGH]: A-01/A-02/A-08/A-10 acoustic cluster: adjacency + panels + HVAC NC-25 + hearing loop IEC 60118-4 -->
<!-- CON-0145 [HIGH]: A-10 hearing loop + H-04 video intercom — DEAF communication cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:DEAF|DBL -->
<!-- grade_confidence: HIGH — IEC 60118-4 field strength target universally adopted. Hearing loop efficacy: multiple Tier 1-2 RCT/cohort studies for DEAF populations. ≥10 jurisdictions mandate. Counter loop geometry: BS 8300 + BCA SG. HIGH confidence. -->

<!-- CON-0052 [HIGH]: Add Auracast DAR provision cross-reference to A-10 and A-11. IEC 60118-17 (Auracast) expected late 2027; dual provision (loop + Auracast-ready conduit) is best practice. See A-12 (Auracast Infrastructure Readiness). -->

**Applicable Groups:** DEAF, DBL

**Description:** Counter loop installed at all service counters, reception desks, ticket offices, and triage points where one-to-one communication occurs. Counter loop provides T-coil compatible audio direct to hearing aid without microphone interference.

**Specifications:**

Loop: concealed under counter surface

Field strength: 100 mA/m ±3 dB (IEC 60118-4:2014+AMD1:2017)

Frequency response: ±3 dB from 100--5000 Hz

Signage: IFHOH T symbol at counter

All staffed service points: counter loop required

**Retrofit cost note:** Retrofit penalty: LOW. Counter hearing loop is a low-cost surface or under-counter cable installation. Retrofit

penalty is minimal; power supply proximity is the principal constraint. See Part 12 §12.4.

**Key citations:** International Electrotechnical Commission. (2017). IEC 60118-4:2014+AMD1:2017 [BS EN IEC 60118-4:2015+A1:2018 for UK/EU\]. IEC. Hearing Loss Association of America. (2023). Hearing loop technology. HLAA.

**DBL evidence note:** [THIN BASE — Tier 2+4 only; no Tier 1 OT clinical research on DeafBlind built environments in any jurisdiction; March 2026]

**Cross-reference:** A-11 (Room Perimeter Loop); B-02 (Face Illumination for Lip Reading)

**Evidence basis (OT):** Compensatory FOR. The counter loop is an environmental compensation enabling the occupation of independent service interaction for users dependent on hearing devices; without this compensation the environment disables the occupation. The IEC 60118-4:2014+AMD1:2017 field strength specification ensures functional effectiveness, not symbolic compliance.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Requirement | Performance Standard |
|---|---|---|---|
| US | ADA 2010 §219 | Assistive listening in assembly ≥50 occ. | IEC 60118-4 via A117.1 |
| UK | BS 8300-2:2018 | Hearing loop at ALL counters/help points | BS EN 60118-4 |
| AU | NCC / AS 60118.4 | Hearing augmentation in assembly | AS 60118.4 |
| DE | DIN 18040-1 | Two-Senses: visual + auditory redundancy | DIN EN 60118-4 |
| EU | EN 17210:2021 | Hearing enhancement recommended | EN 60118-4 |
| ISO | IEC 60118-4:2018 | Universal performance standard | — |
| **Guidebook** | **A-10** | **All counters/service points** | **IEC 60118-4** |

UK BS 8300-2 is most prescriptive — requires hearing loop specifically at counters (not just "assistive listening"). US ADA allows choice of technology (loop, IR, FM).


### A-10b RT60 for Hydrotherapy and Pool Environments

**Applicable Groups:** MOB, PAIN, NDV, DEM

**Description:** RT60 ≤2.0 seconds in hydrotherapy pools and wet therapy environments. Acoustic absorption products must be moisture-resistant (Class E or better water exposure rating).

**Specifications:**

RT60 ≤2.0 s at 500 Hz and 1000 Hz in occupied condition

All absorption products: moisture resistant rating confirmed

Post-installation: RT60 measurement at commissioning

**Retrofit cost note:** Retrofit penalty: MODERATE -- HIGH. Pool/hydrotherapy acoustic treatment involves wet environment panels and surface specification. Retrofit without facility closure requires a full tile/substrate replacement programme. At design stage, specification is the only cost. See Part 12 §12.4.2.

**Key citations:** ISO 3382-2:2008. Measurement of room acoustic parameters. ISO. Bettarello, F., et al. (2021). Applied Sciences, 11(9), 3942.

**Cross-reference:** A-02 (Acoustic Ceiling); A-16 (Sensory Room)

**Evidence basis (OT):** Dunn's Sensory Processing Model. Hydrotherapy pool environments present an unusually high baseline acoustic energy load from hard reflective surfaces and water sounds; RT60 ≤2.0s limits the reverberation that amplifies this load for sensory-sensitive users, preserving the therapeutic occupation value of the hydrotherapy environment.

**Jurisdiction comparison:** No code specifies RT60 for hydrotherapy pools specifically. UK BB93 covers school pool halls. UK HTM 08-01 covers healthcare acoustic environments. ISO 3382 provides measurement methodology. Hydrotherapy RT60 targets are guidebook-specific — derived from DEAF/HI communication needs in high-reverberation wet environments.


### A-11 Room Perimeter Hearing Loop (Assembly and Meeting Spaces)
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:DEAF|DBL -->
<!-- grade_confidence: HIGH — As A-10: IEC 60118-4 universally adopted. Room loop geometry: BS 8300, EN 17210, multiple jurisdictions. Tier 1-2 evidence on hearing loop benefit. HIGH confidence. -->

**Applicable Groups:** DEAF, DBL

**Description:** Room perimeter induction loop installed in all assembly spaces (≥25 capacity) and all consultation/interview rooms.

Compliant with IEC 60118-4:2014+AMD1:2017.

**Specifications:**

Cable: 1.5--2.5 mm² copper, installed in floor screed (new) or under flooring (retrofit)

Field strength: 100 mA/m ±3 dB throughout coverage area

Spill: ≤10 dB at 1 m outside boundary

Provision trigger: all assembly spaces ≥25 capacity; all consultation/interview rooms

French CEREMA standard (CEREMA, 2021): loops required at all counters AND all spaces ≥50 seats — more comprehensive than the UK-derived ≥25 capacity threshold above. In France, the higher CEREMA standard applies.

Certificate of Conformity: required post-commissioning from qualified loop engineer

Signage: IFHOH symbol at all entrances to looped space

Required: all assembly spaces ≥25 capacity; all consultation/interview rooms

**Retrofit cost note:** Retrofit penalty: LOW -- MODERATE. Room perimeter hearing loop requires a cable run in floor or wall chase. In a finished building, chase-cutting and reinstatement adds moderate cost. Design stage conduit provision eliminates this entirely. See Part 11 for DAR conduit provisions; Part 12 §12.4.

**Key citations:** International Electrotechnical Commission. (2017). IEC 60118-4:2014+AMD1:2017 [BS EN IEC 60118-4:2015+A1:2018 for UK/EU\]. IEC. Hearing Loss Association of America. (2023). Hearing loop technology and Auracast. HLAA. HLF. (2023). Teleslynge i alle offentlige bygg [Norwegian\]. HLF.

**DBL evidence note:** [THIN BASE — Tier 2+4 only; no Tier 1 OT clinical research on DeafBlind built environments in any jurisdiction; March 2026]

**Cross-reference:** A-10 (Counter Loop); A-12 (Auracast Infrastructure); B-02 (Lip Reading Illumination)

**Evidence basis (OT):** Compensatory FOR. The room perimeter loop compensates for hearing impairment by delivering a direct audio signal to the hearing device, enabling participation in assembly and communal occupations that would otherwise be inaccessible; the commissioning certificate requirement ensures the compensation meets the functional standard, not merely the installation standard.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Assembly Trigger | Technology Specified | Performance |
|---|---|---|---|---|
| US | ADA 2010 §219 | ≥50 fixed seats or amplification | "Assistive listening" (choice) | IEC 60118-4 via A117.1 |
| UK | BS 8300-2:2018 | All meeting/lecture/performance rooms | Induction loop, IR, or radio | BS EN 60118-4 |
| AU | NCC | Assembly and meeting spaces | Hearing augmentation | AS 60118.4 |
| DE | DIN 18040-1 | Assembly spaces | Two-Senses principle | DIN EN 60118-4 |
| FR | Arrêté 2017 | ≥50 seats | Hearing enhancement | NF EN 60118-4 |
| EU | EN 17210:2021 | Recommended | Hearing enhancement | EN 60118-4 |
| **Guidebook** | **A-11** | **All assembly/meeting spaces** | **Perimeter induction loop** | **IEC 60118-4** |

Guidebook specifies perimeter induction loop (not just "assistive listening") because telecoil-compatible hearing aids are the most common technology worldwide. Cross-reference A-12 (Auracast readiness) for emerging Bluetooth LE Audio alternative.


### A-12 Auracast Infrastructure Readiness
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:DEAF -->
<!-- grade_confidence: MODERATE — Auracast readiness: technology is Bluetooth LE Audio standard (confirmed 2023). No built-environment RCT yet — standard very new. Tier 2 (BT SIG). MODERATE given forward-compatibility rationale. -->

**Applicable Groups:** DEAF, DBL · OFS
<!-- CON-0081: personal receiver system reduces OFS exertion from following speech in noisy environments -->

**Description:** In new construction: conduit and power provision for future Auracast (Bluetooth LE Audio) transmitter at ceiling/high-wall positions in all assembly spaces ≥25 capacity. Future-readiness provision, not a current installation requirement. Does not replace A-11.

**Specifications:**

Conduit: 25 mm diameter from electrical distribution to ceiling/high-wall position

Power: 13A fused spur at transmitter position

Data: Cat6 network drop at same position

Loop installation (A-11) remains required; Auracast does not substitute

**Retrofit cost note:** Retrofit penalty: LOW. Auracast infrastructure readiness requires conduit provision and power access points — a

design-stage specification only. Retrofit requires surface-run conduit or chase cutting. See Part 11; Part 12 §12.4.

**Key citations:** Hearing Loss Association of America. (2023).

Hearing loop technology and Auracast. HLAA. IFHOH. (2023).

International hearing access committee. IFHOH.

**DBL evidence note:** [THIN BASE — Tier 2+4 only; no Tier 1 OT clinical research on DeafBlind built environments in any jurisdiction; March 2026]

**Cross-reference:** A-10; A-11.

**Evidence basis (OT):** Compensatory FOR; EHP Framework (adapt strategy). Auracast conduit and power pre-provision implements both the Compensatory FOR principle (environment as future-ready compensation tool) and the EHP 'adapt' strategy: the context is partially modified at construction to enable full modification later without structural intervention, directly aligning with the DAR principle (§1.6).

**Jurisdiction comparison:** No jurisdiction mandates Auracast (Bluetooth LE Audio). Technology is pre-regulatory — Bluetooth SIG published LC3 codec specification. UK RNID and US HLAA are monitoring. IEC 60118-4 (induction loop) remains the only mandated assistive listening technology. Guidebook specifies infrastructure readiness (conduit, power, network) for future adoption.


### A-13 No Sound Masking in Neurological Population Environments
<!-- CON-0008 [HIGH]: A-02/A-08/A-13 acoustic convergence: RT60 + NC-25 + masking prohibition -->
<!-- CON-0039 [HIGH]: RT60 ≤0.3s Universal Mode universal for speech-critical rooms; background noise ≤35dBA; STI ≥0.60 -->
<!-- CON-0040 [HIGH]: Unified sensory environment system: Dunn profiles → spatial zones → quantified parameters -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DEAF|NDV -->
<!-- grade_confidence: LOW — No sound masking in NEU/NDV spaces: PAS 6463 guidance. Physiological rationale (hyperacusis) is Tier 1 mechanism (Garfinkel 2016 interoception). No built-env RCT. Tier 4. -->

<!-- CON-0040 [HIGH]: Add OFS, PAIN to Applicable Groups (same mechanism as A-02). ○ THIN-POPULATION-SPEC. -->
<!-- CON-0039 [HIGH]: Strict NDV/AUT acoustic target (RT60 ≤0.3 s) is a sub-target of the general DEAF/DEM target. No sound masking in any space where NDV is primary — already specified but ensure cross-reference to NDV/DEAF conflict resolution in Part 5 §5.2. -->

**Applicable Groups:** AUT, PCS, NEU, DEM, NDV · OFS · PAIN
<!-- CON-0008: CON-0008: sound masking increases cognitive load; energy cost for OFS/PAIN populations -->

**Description:** Electronic sound masking systems explicitly excluded from spaces serving neurological populations, PCS patients, and dementia residents. Sound masking adds continuous broadband noise (45--48 dBA) that is clinically contraindicated for PCS and AUT users.

**Specifications:**

No electronic sound masking systems in: sensory rooms, ABI/PCS recovery spaces, DEM environments, AUT-specific spaces

Privacy alternative: acoustic partitions (STC ≥35 per A-03) instead of masking

Open offices: acoustic zoning (A-04), focus rooms (D-05)

**Key evidence (non-English):** De Hogeweyk post-occupancy evaluation (BuroKade/Vivium, Dutch-language reports, 2012--2019): 94% of residents with moderate dementia navigated independently to the village square and back within 6 months of admission, compared to 34% in conventional dementia units — the strongest empirical wayfinding evidence available for consistent environment provisions (D-09) in combination with loop plan (D-01).

**Retrofit cost note:** Retrofit penalty: ZERO — NET SAVING. This item is a specification exclusion. Omitting sound masking systems costs less than installing them. Retrofit action is removal of existing masking systems at minor cost. See Part 12 §12.4.1.

**Key citations:** Canadian Association of Occupational Therapists. (2018). Practice guidelines for acquired brain injury. CAOT.

**Cross-reference:** A-08 (HVAC Noise); A-16 (Sensory Room); D-05 (Focus Rooms)

**Evidence basis (OT):** EHP Framework (prevent strategy); Dunn's Sensory Processing Model. Electronic sound masking adds a continuous broadband signal (45--48dBA) that constitutes an uncontrolled, non-adjustable sensory input; for AUT and PCS users in the sensory-avoiding and sensory-sensitive quadrants (Dunn's model), this input exceeds neurological thresholds and actively restricts the performance range. This item implements a categorical EHP 'prevent' intervention.

**Jurisdiction comparison:** No code restricts sound masking systems. US ASHRAE and sound masking industry promote it for open offices. Guidebook PROHIBITS sound masking in neurological population environments — derived from NEU/NDV/AUT evidence that artificial noise exacerbates cognitive load and sensory distress.


### A-14 Double-Leaf Partition (STC ≥50) for Sensitive Adjacencies
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:NDV|MH -->
<!-- grade_confidence: MODERATE — STC ≥50 at clinical partitions: speech privacy standard well-established (ANSI, BS 8300, ISO). Mental health built environment BPC (Faerden 2022 PMID:36567605 — single rooms, patient control). ≥6 jurisdictions. -->

**Applicable Groups:** AUT, PCS, DEM, MH · OFS · NDV
<!-- D2-41: D2-41: acoustic separation reduces cognitive load; OFS energy conservation -->

**Description:** Double-leaf partition with 50 mm air gap (unfilled) between two independent leaves, each with 70 mm steel stud, 2×15 mm acoustic plasterboard, 50 kg/m³ mineral wool quilt. Resilient bars on one leaf. No mechanical connections between leaves.

**Specifications:**

Construction: double leaf, 50 mm cavity minimum (unfilled)

Each leaf: 70 mm stud; 2×15 mm acoustic plasterboard; 50 kg/m³ quilt

One leaf: resilient bars

No through-connections between leaves (no sockets penetrating both)

Flanking: sealed at all ceiling/floor junctions

Target: STC ≥50 laboratory; Field STC ≥45

**Retrofit cost note:** Retrofit penalty: HIGH. Double-leaf STC ≥50 partitions require structural provision at wall head and floor --- major interventions in an existing building. At design stage, the specification premium over a standard partition is modest. See Part 12 §12.4.2.

**Key citations:** British Standards Institution. (2022). PAS

6463:2022. BSI. Bettarello, F., et al. (2021). Applied Sciences,

11(9), 3942.

**Cross-reference:** A-03 (Acoustic Door); A-16 (Sensory Room)

**Evidence basis (OT):** EHP Framework (create strategy); Dunn's Sensory Processing Model. The double-leaf partition at STC ≥50 creates a new acoustic context enabling occupations (therapy, recovery, focused work) that require protection from auditory intrusion above what any single-leaf construction can provide.

**Jurisdiction comparison:** US ANSI S12.60 specifies STC ≥50 for classroom-corridor partitions. UK BB93 specifies DnT,w values by room pair. DE DIN 4109 specifies R'w by building type. Guidebook specifies STC ≥50 double-leaf for ALL sensitive adjacencies — exceeds codes that limit to educational settings.


### A-15 Acoustic Differentiation Between Spaces (Navigation Aid for VIS)
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:VIS|DBL -->
<!-- grade_confidence: LOW — Acoustic differentiation for VIS/DBL wayfinding: Tier 4 (ISO 23599 adjacent). No disability-specific RCT on acoustic landmark design. Expert consensus + standards. -->

**Applicable Groups:** VIS (blind, severely visually impaired) · NEU · OFS
<!-- D2-41: D2-41: acoustic landmarks reduce navigation effort for OFS/NEU -->

**Description:** Deliberately maintain distinct acoustic character between spaces rather than uniform RT60 treatment. Hard surfaces in circulation give a live acoustic signature distinct from soft-finished rooms, providing orientation cues for blind users.

**Specifications:**

Circulation routes: maintain distinct acoustic character from rooms (harder surfaces, slightly higher RT60)

Entry atria/landmarks: allow RT60 0.8--1.2s (recognisable as distinct from corridors)

Do not apply full acoustic treatment to primary circulation if it removes all acoustic differentiation

Resolve tension with A-05: carpet reduces acoustic cues — provide hard floor strips at key junctions

**Retrofit cost note:** Retrofit penalty: LOW -- MODERATE. Acoustic differentiation between spaces is a material and finish specification at zero cost at design stage. Retrofit requires finish replacement and potentially structural element modification at room junctions. See Part 12 §12.4.1.

**Key citations:** CNIB Foundation. (2024). Clearing our path. CNIB.

Norges Blindeforbund. (2023). Kontrast i bygde omgivelser

[Norwegian\].

**Cross-reference:** A-05 (Carpet tension); D-04 (Landmarks); BIO-03 (Tactile Variety)

**Evidence basis (OT):** Compensatory FOR. Acoustic differentiation preserves the environmental cues that compensate for the absence of visual information during navigation; deliberate maintenance of a distinct acoustic signature between corridor and room surfaces is an environmental compensation strategy that enables independent wayfinding as an occupation.

**Jurisdiction comparison:** No code addresses acoustic differentiation as a VIS navigation aid. This is a guidebook-specific provision — different acoustic signatures (floor material, ceiling height, reverberation character) help VIS users identify space transitions without visual cues.


### A-16 Sensory Room / Quiet Room Provision
<!-- CON-0040 [HIGH]: Unified sensory environment system: Dunn profiles → spatial zones → quantified parameters -->
<!-- CON-0046 [HIGH]: NHS CAMHS: sensory refuge mandatory (not optional) where NDV/AUT + NDV/MH co-occurrence foreseeable -->
<!-- CON-0117 [HIGH]: I-03 TMV ≤38°C + D-05 low-stimulation + A-16 sensory room — OFS/NDV/MH cluster -->
<!-- CON-0141 [HIGH]: A-16 sensory room — Part 7 NR-EDU education matrix cross-reference -->
<!-- CON-0144 [HIGH]: A-16 sensory room — additional evidence; RHFAC v4.0 + Wilson 2023 PMID -->
<!-- CON-0148 [HIGH]: A-16 sensory room — additional clinical evidence annotation -->
<!-- CON-0150 [HIGH]: A-16 sensory room door specification — acoustic door seal requirement STC ≥35 -->
<!-- CON-0163 [HIGH]: A-16 sensory room — Part 9 §9.2.2 OT appointment trigger cross-reference -->
<!-- CON-0164 [HIGH]: B-10 visual alarm + A-16 sensory room + K-04 vibrotactile — alert cluster -->
<!-- CON-0166 [HIGH]: B-01/B-06/B-07/A-16 — circadian + dimming + indirect + sensory room — lighting cluster -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:NDV|DEM|NEU|OFS|NDV/MH -->
<!-- grade_confidence: LOW — Sensory room ≥8m²: PAS 6463 §14.1 (Tier 4). No RCT on room size for NDV outcomes. Wilson 2023 PMID (Co-1) documents failure modes. Caldwell 2025 qualitative. No validated threshold. -->

<!-- CON-0046 [HIGH]: CS-17 (NHS CAMHS, NDTi 2022) documents NDV/MH ward environments actively harmful to NDV/AUT co-occupants. Sensory rooms in MH settings must be distinct from MH de-escalation rooms — different clinical purpose, different specification. -->
<!-- CON-0002 [HIGH]: Expand Applicable Groups to NDV, NDV/MH, OFS, PAIN (in addition to NDV/AUT). Add recline-capable seating option (OFS/PAIN — Tier 2 clinical basis, THIN-POPULATION-SPEC). Collapse MH de-escalation room into A-16 with population-specific configuration notes (see §2.8 distinction table). Cross-reference H-02 as co-primary. CON-0019: specify as Universal Mode universal — one per occupied floor plate. -->
<!-- CON-0023 [HIGH]: Audit against Al-Harasis taxonomy — spatial configuration (layout topology) is underspecified relative to finish materials. Add note on approach route (no high-stimulation zones on path to A-16). --> (≥8 m², one per floor or per 500 m² GFA)

**Applicable Groups:** AUT, ADHD, PCS, DEM, MH, OFS · NDV/MH · PAIN · NEU/PCS
<!-- CON-0066: CON-0066: sensory room serves NEU/PCS alongside NDV — fatigue and overstimulation recovery -->
<!-- CON-0002: CON-0002/CON-0019: A-16 is multi-population: NDV/AUT sensory regulation + NDV/MH de-escalation (separate rooms) + OFS reclined rest + PAIN cushioned seating. H-02 cross-ref mandatory. -->

**Description:** Dedicated enclosed room, minimum 8 m², with acoustic specification STC ≥50 partition and RT60 ≤0.3s, individual HVAC at NC-25, full dimming (100% to 0 lux), no external windows or blackout blinds, and comfortable seating. Located adjacent to primary circulation.

> **Cross-population convergence (CON-0186):** A-16 is specified as a universal provision because four independent clinical evidence bases arrive at identical room requirements via separate mechanisms: (1) NDV/AUT — sensory overload recovery (PAS 6463:2022); (2) MH — de-escalation and safety regulation in psychiatric and supported-living environments (Oostermeijer et al. 2021, PMID:34233981; Weber et al. 2022, PMID:35046849); (3) DEM — calm retreat and wandering management (DSDC EADDAT 2022); (4) OFS/ME — mandatory rest space during post-exertional malaise episodes (BPC fatigue-spectrum, CDC ME/CFS Tier Co-1). The shared physical specification — quiet, low-stimulation, user-controlled, within 25 m — is not a compromise; it is a genuine convergence. Provision of one A-16 per floor plate resolves accessibility gaps for all four populations simultaneously.

**Specifications:**
Area: 8 m² (minimum); 12 m² preferred
Partition: STC ≥50 (A-14); Door: STC ≥35 (A-03)
RT60: ≤0.3 s (NRC ≥0.90 surfaces throughout)
Lighting: 100%--0 lux dimming; warm amber 2700 K; no fluorescent
HVAC: NC-25 maximum; individual control
Blackout: 100% blackout blinds or no windows
Location: adjacent to primary circulation; not via another occupied space

**Retrofit cost note:** Retrofit penalty: HIGH. Sensory room provision requires dedicated floor area — a planning decision at design stage. Retrofit requires spatial reorganisation within a finished building. Minimum 8 m² cannot be created from circulation space. See Part 12 §12.4.2.

**Key citations:** British Standards Institution. (2022). PAS 6463:2022. BSI. Rick Hansen Foundation. (2024). RHFAC v4.0, Category 11. RHF. National Autistic Society. (2023). Creating autism-friendly environments. NAS.

**Cross-reference:** A-01; A-03; A-14; F-03 (Graduated Stimulation Re-entry)

**Evidence basis (OT):** EHP Framework (create strategy). The sensory room implements EHP's 'create' strategy: an entirely new environmental context is constructed within which the occupation of sensory self-regulation becomes possible. The 8 m² minimum, STC ≥50 partition, and RT60 ≤0.3s specifications are the minimum context parameters required for this occupation to occur.

**FDR-MST-01 [Tier 3 — Leavitt 2014; Davis 2010]:** Uhthoff's phenomenon recovery time 30–60 minutes post heat exposure (Leavitt & Feinstein 2014, Davis 2010). NEU/MS users require a cooling-capacity retreat distinct from NDV sensory regulation — ambient ≤16°C preferred (vs NDV typical ≤20°C). ○ In facilities serving NEU/MS as a primary or significant secondary population: where A-16 serves both NDV and NEU/MS, specify individual HVAC control enabling ≤16°C setpoint. Alternatively, a separate cooling station (≤12 m², individually temperature-controlled to ≤16°C, adjacent to MS clinic or specialist facility area) may be provided as a dedicated NEU/MS provision. Extended occupancy capacity required (30–60 min recovery duration vs 10–15 min NDV reset). [THIN — architectural implication only; no design standard specifies]

**Jurisdiction comparison:** No code mandates sensory rooms. UK PAS 6463:2022 references sensory environments. NL Snoezelen concept (1970s) is historical origin. ISO 25552 (dementia) references calming environments. Guidebook specifies provision in all settings serving NDV/AUT/DEM populations — user-controllable lighting, sound, texture.


### A-17 Upholstered Seating [ABSORBED INTO G-02 per CO-0003/D2-24]
<!-- design_stage_lock: SD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- CO-0003: A-17 specification content absorbed into G-02 Variety of Seating Types. G-02 now includes: upholstered seating throughout occupied spaces as population-serving provision for OFS/PAIN acoustic absorption benefits. -->

**Applicable Groups:** AUT, PCS, DEM, NDV

**Description:** Upholstered seating (fabric, not hard plastic or metal) at all seating locations. Contributes acoustic absorption (NRC

0.15--0.30 per person) and reduces impact noise from chair movement.

**Specifications:**
All seating: upholstered seat and back minimum; padded armrests preferred
Chair feet: rubber or felt pads on all chairs
Fixed seating: upholstered cushion minimum
Hygiene contexts: wipe clean upholstery (vinyl, antimicrobial fabric) is acoustically equivalent

**Retrofit cost note:** Retrofit penalty: LOW. Upholstered seating is a procurement specification with no structural or services

implications. Retrofit is furniture replacement, phaseable without building disruption. See Part 12 §12.4.1.

**Key citations:** Bettarello, F., et al. (2021). Applied Sciences, 11(9), 3942. British Standards Institution. (2022). PAS 6463:2022. BSI.

**Cross-reference:** A-02 (Acoustic Ceiling); G-02 (Variety of Seating Types)

**Evidence basis (OT):** Dunn's Sensory Processing Model; Biomechanical FOR. Upholstered seating reduces impact noise transmission (Dunn's: acoustic load reduction) and eliminates hard surface contact that constitutes an allodynia trigger for users with fibromyalgia or tactile sensitisation (Biomechanical FOR: contact force and vibration transmission to body tissues).


## CATEGORY B: LIGHTING

All EML (Equivalent Melanopic Lux) targets are at seated eye level (1200 mm AFF). CCT = Correlated Colour Temperature. EML measured per WELL v2 Feature L07. UGR = Unified Glare Rating (EN 12464-1). Lux values: horizontal illuminance at 850 mm AFF unless stated. Vertical illuminance at 1500 mm AFF (face level).

**Jurisdiction comparison:** MERGED — see G-02 (Variety of Seating Types).


### B-01 Circadian Lighting (≥250 Melanopic EDI at Eye Level in Daytime Spaces)
<!-- CON-0006 [HIGH]: B-01 circadian lighting melanopic EDI — updated per A2 P1 (B-01 title + metric note) -->
<!-- CON-0040 [HIGH]: Unified sensory environment system: Dunn profiles → spatial zones → quantified parameters -->
<!-- CON-0166 [HIGH]: B-01/B-06/B-07/A-16 — circadian + dimming + indirect + sensory room — lighting cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:DEM|NEU|NDV -->
<!-- grade_confidence: MODERATE — Melanopic EDI ≥250: Brown et al. 2022 PLOS Biology (Tier 1) + CIE S026:2018. WELL v2 sets lower threshold (≥181 melanopic EDI). DIN/TS 67600:2022 adopts melanopic EDI metric. ≥5 jurisdictions moving toward circadian metrics. Tier 1 photobiology evidence; limited built-env RCT. -->
<!-- METRIC NOTE: This item uses melanopic EDI (≥250) as the daytime threshold per Brown et al. 2022 PLOS Biology. Prior versions cited EML (≥150–200 EML). Conversion: melanopic EDI ≈ EML / 1.104. Use melanopic EDI ≥250 as the unified design target. See BPC circadian-lighting-melanopic-edi and spec-db-part4-reconciliation Section C1. -->

**Applicable Groups:** ALL (especially DEM, MH, PAIN, NEU) · OFS · NDV/AUT
<!-- CON-0182 [HIGH]: NDV/AUT photosensitivity at high melanopic EDI creates compound interaction with DEM/MH circadian needs — added to Applicable Groups with compound-interaction note below. ISW: connection-scout Opus [2026-04-24 15:17] -->
<!-- CON-0006: CON-0006: circadian lighting supports OFS energy regulation and NEU sleep-wake cycle recovery alongside DEM -->

**Description:** Lighting delivering ≥250 lux melanopic EDI at seated eye level (1200 mm AFF) during daytime occupied hours (08:00–18:00). Evening (after 19:00): ≤50 lux melanopic EDI with shift to warm 2700 K CCT for sleep preparation. (Legacy EML values — ≥150 daytime, ≤10 evening — are superseded; see METRIC NOTE in item header.)

> **Cross-population compound interaction (CON-0182):** The melanopic EDI ≥250 lux daytime target that serves DEM circadian entrainment and MH therapeutic lighting is contraindicated for NDV/AUT (photosensitivity — high lux triggers sensory overload) and OFS/ME (light-triggered symptom exacerbation in photosensitive ME/CFS). Resolution: circadian-optimised communal lighting applies at full specification; a mandatory low-lux opt-out (A-16 sensory room, ≤50 lux) must be accessible within 25 m of any primary occupancy space. Do not compromise the daytime threshold — spatial zoning is the only solution.

**Specifications:**

Melanopic EDI: ≥250 lux at eye level (1200 mm AFF) during daytime hours (08:00–18:00) — per Brown et al. 2022, CIE S 026:2018, DIN/TS 67600:2022. (Equivalent to ≥276 EML via conversion factor 1.104 — older EML values of ≥150 EML are insufficient and have been superseded by the melanopic EDI metric. See METRIC NOTE in item header.)  
[CORRECTED: ISW Opus cross-check 2026-04-24 15:17 — Specifications block previously retained legacy EML ≥150 while item heading and jurisdiction comparison table cited ≥250 MEDI; internal inconsistency now resolved.]

CCT: ≥4000 K for electric light during daytime

Evening (after 19:00): ≤50 lux melanopic EDI; 2700 K CCT; reduced intensity (legacy EML equivalent: ≤10 EML — superseded)

Natural light maximised; not substituted by electric light where achievable

DEM environments: circadian lighting is a clinical requirement, not a comfort enhancement

**Retrofit cost note:** Retrofit penalty: MODERATE. Circadian lighting requires tuneable-white luminaires with control wiring. At design stage the cost premium over standard LED is modest. Retrofit requires luminaire replacement and control circuit rewiring or smart system overlay. See Part 12 §12.4.2.

**Key citations:** WELL Building Institute. (2024). WELL v2. IWBI. Alzheimer's Disease International. (2020). World Alzheimer Report 2020. ADI.

**Cross-reference:** B-09 (Natural Light); B-11 (Warm CCT Evening); B-06 (Individual Dimming)

**Evidence basis (OT):** Dunn's Sensory Processing Model; PEOP Model. Circadian-appropriate lighting (≥250 MEDI daytime, ≤50 MEDI evening) supports the occupation of time-structured daily activity by calibrating the environmental light signal to the neurological systems that regulate alertness and sleep; for DEM and NEU users this is a clinical requirement, not an enhancement.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Daytime Melanopic EDI | Evening | Care Homes | Mandatory |
|---|---|---|---|---|---|
| DE | DIN/TS 67600:2022 | ≥250 MEDI at eye (1.2m) | Reduced | Explicitly covered | No (Tier 5) |
| INT | WELL v2/v6 L03/L07 | ≥150 EML / ≥250 m-EDI | ≤50 EML | — | No (voluntary) |
| INT | CIE S 026/E:2018 | Metric definition | — | — | No (metric only) |
| US | UL 24480 | CS ≥0.3 (different model) | — | — | No (voluntary) |
| All others | — | **No requirement** | — | — | — |
| **Guidebook** | **B-01** | **≥250 MEDI daytime** | **≤50 MEDI evening** | **Adjusted for age** | **Recommended** |

No national building code mandates circadian metrics. US UL 24480 uses Circadian Stimulus (CS) model — NOT equivalent to melanopic EDI.


### B-02 Diffuse Lighting for Lip Reading and Sign Language (Shadow-Free Face Illumination)
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DEAF|DBL -->
<!-- grade_confidence: MODERATE — Diffuse shadow-free lighting for lip reading/BSL: DeafSpace guidelines (Gallaudet, Tier 2 co-design) + BS 8300 §8.3. Photometric principle is sound (lighting science). No RCT on diffuse lighting vs directional for Deaf communication outcomes. ≥4 jurisdictions reference. -->

**Applicable Groups:** DEAF, DBL

**Description:** In all spaces where Deaf users communicate: diffuse, shadow-free illumination of face and upper body from multiple directions. No strong directional downlight creating facial shadows. No backlit windows behind speakers.

**Specifications:**

Horizontal illuminance: ≥500 lux at table/work surface

Vertical illuminance at face (1500 mm AFF, omnidirectional): ≥300 lux

No backlit window positions for primary speaker/signer positions

Multiple ceiling luminaire positions (no single high-intensity downlight)

Preferred: indirect or semi-indirect luminaires supplemented by wall-wash

**Retrofit cost note:** Retrofit penalty: MODERATE. Diffuse face illumination requires careful luminaire positioning at design stage

— negligible cost premium. Retrofit requires repositioning existing luminaire points, which may involve ceiling works and circuit

modification. See Part 12 §12.4.2.

**Key citations:** DeafSpace Project, Gallaudet University. (2010).

DeafSpace design guidelines. Gallaudet. British Standards Institution.

(2018). BS 8300:2018. BSI.

**DBL evidence note:** [THIN BASE — Tier 2+4 only; no Tier 1 OT clinical research on DeafBlind built environments in any jurisdiction; March 2026]

**Cross-reference:** A-11 (Hearing Loop); B-06 (Dimming Control); D-10 (Transparent Panels)

**Evidence basis (OT):** Biomechanical FOR. The ≥300 lux vertical illuminance at face level (1500mm AFF) and shadow-free specification are derived from the minimum illuminance required for lip-reading at normal conversational distance (0.5--1.5m) given the visual acuity range of hard-of-hearing users who rely on lip reading as a primary communication supplement.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Face Illuminance | Shadow Control | Vertical Illuminance | Notes |
|---|---|---|---|---|---|
| US | ADA | Not specified | — | — | — |
| UK | BS 8300-2:2018 §12 | Face adequately lit | — | — | General provision |
| DE | DIN 18041 / DIN 18040 | Acoustic + visual | — | — | — |
| ISO | ISO 21542:2021 | Referenced | — | — | — |
| **Guidebook** | **B-02** | **≥300 lux vertical** | **Shadow-free face zone** | **Specified** | **DEAF lip-reading evidence** |

No building code specifies vertical illuminance for lip reading. Guidebook's ≥300 lux at face height is derived from DEAF communication research. Significant gap in all codes.


### B-03 Elimination of Fluorescent Overhead Lighting
<!-- design_stage_lock: DD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:NDV|NEU -->
<!-- grade_confidence: HIGH — No fluorescent/non-IEEE-1789-compliant LEDs: IEEE 1789-2015 (Tier 4 engineering standard) defines flicker-free threshold. NDV/NEU seizure and photosensitivity evidence: Harding et al. 2005 Epilepsia (Tier 3 SR). ≥10 jurisdictions moving to LED — mandatory IEEE compliance is VE-protected per Part 8. HIGH on fluorescent elimination; MODERATE on IEEE 1789 threshold specifically. -->

**Applicable Groups:** PCS, AUT, PAIN, NDV · OFS · NEU
<!-- CON-0071: fluorescent flicker is OFS/NEU/PAIN trigger -->

**Description:** No fluorescent luminaires (T8, T5, compact fluorescent) installed anywhere in the building. Replaced with flicker-free LED throughout (B-04). Applies to all spaces.

**Specifications:**

Zero fluorescent luminaires anywhere in the building

All luminaires: LED driver with high frequency switching (not mains-frequency ripple)

Verified per B-04: IEEE 1789-2015 compliance required

Heritage buildings: LED retrofit of T8 tubes may not achieve IEEE 1789 compliance; specify new luminaires

**Retrofit cost note:** Retrofit penalty: LOW -- MODERATE. Fluorescent elimination is a luminaire swap. In retrofit, ballast removal and fixture replacement across a building carries moderate labour cost but no structural implications. At design stage, LED specification is standard. See Part 12 §12.4.1.

**Key citations:** Canadian Association of Occupational Therapists. (2018). Practice guidelines for acquired brain injury. CAOT. AOTA. (2023). OT practice guidelines for adults with TBI. AJOT, 77(4).

**Cross-reference:** B-04 (Flicker-Free LED); B-07 (Indirect Lighting)

**Evidence basis (OT):** EHP Framework (prevent strategy); Dunn's Sensory Processing Model. Fluorescent luminaires (magnetic ballast 100Hz flicker; electronic 20--50kHz flicker at visible amplitudes) are documented triggers for migraine, photosensitive epilepsy, and PCS symptom exacerbation; this item implements a categorical prevent intervention by removing the trigger source entirely rather than attempting to mitigate it.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Flicker Limit | Fluorescent Restriction | Notes |
|---|---|---|---|---|
| US | IEEE 1789-2015 | Modulation <10% above 90Hz | Recommended | Not mandatory |
| UK | PAS 6463:2022 | Avoid fluorescent | Recommended | NDV provision |
| EU | EN 12464-1 | No visible flicker | — | General provision |
| **Guidebook** | **B-03** | **LED only; SVM ≤0.4** | **No fluorescent** | **NDV/NEU/migraine** |

No code bans fluorescent lighting. IEEE 1789 and PAS 6463 are closest. SVM (Stroboscopic Visibility Measure) ≤0.4 is guidebook-specific.


### B-04 Flicker-Free LED Luminaires [MERGED INTO B-03 per CO-0003/D2-23]
<!-- CON-0156 [HIGH]: E-03 ramp + C-04 contrast + E-09 TWSI + B-04 flicker — circulation safety cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:NDV|NEU -->
<!-- grade_confidence: HIGH — IEEE 1789-2015 flicker-free spec: same evidence as B-03. MERGED into B-03 per CO-0003. Rating inherited. VE-protected per Part 8 §8.3.3. -->
<!-- CO-0003: B-04 content absorbed into B-03. B-03 now covers: elimination of fluorescent + flicker-free LED specification (IEEE 1789-2015 / IEC TR 61547-1). Applicable Groups: NDV · NEU/PCS · OFS · DEM · VIS · ALL. -->

**Applicable Groups:** PCS, AUT, PAIN, DEM · OFS · NEU
<!-- CON-0072: already merged into B-03; note added -->

**Description:** All LED luminaires specified to IEEE 1789-2015 at low flicker risk. Flicker percentage <5% at all dimming levels. Flicker index <0.1 at full output. Minimum flicker frequency ≥1000 Hz.

**Specifications:**

Flicker percentage: <5% at all dimming levels (IEEE 1789-2015 low-risk threshold)

Flicker index: <0.1 at full output

Minimum flicker frequency: ≥1000 Hz if ripple present

At all dimming levels including 20% output: within low-risk range

Product specification: IEEE 1789 compliance certificate required before installation

**Retrofit cost note:** Retrofit penalty: LOW. Flicker-free IEEE 1789-compliant LEDs are a standard specification item. Retrofit is simple luminaire replacement. See Part 12 §12.4.1.

**Key citations:** IEEE. (2015). IEEE 1789-2015: Recommended practices for modulating current in high-brightness LEDs. IEEE. CAOT. (2018). Practice guidelines for acquired brain injury. CAOT.

**Cross-reference:** B-03 (No Fluorescent); B-06 (Dimming Control)

**Evidence basis (OT):** EHP Framework (prevent strategy); Dunn's Sensory Processing Model. IEEE 1789-2015 compliant LED luminaires eliminate the flicker frequencies that cause neurological distress in photosensitive users; the standard defines the safe modulation depth and frequency relationship that prevent flicker from entering the visual pathways as a trigger.

**Jurisdiction comparison:** MERGED — see B-03 (Elimination of Fluorescent Overhead Lighting).


### B-05 Gradual Lighting Transition Zones (≥5 m at All Major Illuminance Changes)
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:VIS|DEM -->
<!-- grade_confidence: MODERATE — Gradual lighting transition ≥5m: VIS/DEM populations — BS 8300, DSDC EADDAT, CNIB guidance. Physiological rationale (pupil adaptation, ~5s at high contrast) is Tier 3 (vision science). No built-env RCT. ≥6 jurisdictions reference transition zones. -->

**Applicable Groups:** PCS, AUT, VIS, DEM · PAIN · OFS
<!-- D2-41: D2-41: photosensitivity in OFS/PCS; gradual transitions prevent pain flare from sudden light exposure -->

**Description:** Transitional lighting zone 3--5 m deep at all entries and all transitions where illuminance changes >10:1. Illuminance

ramps gradually from brighter to dimmer space.

**Specifications:**

Zone depth: 3 m minimum; 5 m preferred

Illuminance gradient: ramp across zone depth (no step change)

Applies where illuminance differential >10:1

Entry: supplementary electric lighting in vestibule in dull weather

**Retrofit cost note:** Retrofit penalty: MODERATE. Gradual lighting transition zones require zone circuit design at design stage. Retrofit

requires circuit separation, dimmer installation, and possible luminaire addition in transition areas. See Part 12 §12.4.2.

**Key citations:** CAOT. (2018). Practice guidelines for acquired brain injury. CAOT. Invalidiliitto. (2022). Esteettömyysopas [Finnish\]. Invalidiliitto. CNIB Foundation. (2024). Clearing our path. CNIB.

**Cross-reference:** B-06 (Dimming); B-09 (Natural Light); E-06 (Level Entry)

**Evidence basis (OT):** EHP Framework (prevent strategy); Dunn's Sensory Processing Model. Glare sources in the UGR >19 range constitute a visual trigger that activates threat-detection responses in sensory sensitive users and impairs visual contrast detection in low-vision users; this item prevents the trigger at luminaire-selection stage.

**Jurisdiction comparison:** No code specifies ≥5m lighting transition zones. UK CIBSE SLL Lighting Guide references adaptation. DE DIN EN 12464-1 §5 references illuminance uniformity. Guidebook's 5m transition zone is derived from VIS dark adaptation research (≥3 minutes for rod-cone transition).


### B-06 Individual Dimming Control (≥300 Lux Range)
<!-- CON-0040 [HIGH]: Unified sensory environment system: Dunn profiles → spatial zones → quantified parameters -->
<!-- CON-0127 [HIGH]: C-04 wall colour LRV + B-06 lighting CCT — visual contrast + circadian joint specification -->
<!-- CON-0146 [HIGH]: B-06 individual dimming + B-07 indirect lighting — lighting quality convergence -->
<!-- CON-0166 [HIGH]: B-01/B-06/B-07/A-16 — circadian + dimming + indirect + sensory room — lighting cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:NDV|DEM|NEU|OFS -->
<!-- grade_confidence: MODERATE — Individual dimming ≥300 lux range: BS 8300 + WELL v2 + PAS 6463. Circadian and NDV evidence supports individual control (Tier 3-4). No RCT on dimmer range for disability outcomes. Cross-population benefit (DEM/NDV/NEU/OFS). ≥8 jurisdictions reference occupant lighting control. -->

<!-- CON-0017 [HIGH]: B-06 individual dimming is the highest-impact single lighting provision for DEM/VIS vs NDV/OFS illuminance conflict. Cross-reference H-02 (individual environmental control hierarchy). Ensure B-06 specifies CCT adjustability as well as level — CCT adjustment resolves DEM circadian vs NDV predictability conflict (see Part 5 §5.2 LIGHT-INT). --> (≥300 Lux Range)

**Applicable Groups:** AUT, PCS, DEM, MH, PAIN, OFS

**Description:** Occupant-controlled dimmer in all spaces where neurological or sensory populations spend significant time. Dimming range: 100% down to 10 lux minimum — not merely 30--300 lux. 10 lux is the clinically relevant minimum for PCS users in acute symptom periods.

**Specifications:**

Dimming range: 100% to 10 lux minimum

Dimmer: trailing-edge electronic dimmer compatible with flicker-free

LED (B-04)

Control: accessible switch 800--1200 mm AFF; lever or rocker (UPL compatible)

Sensory/consulting rooms: scene controller with preset 'minimum' (10 lux) scene

Where residential occupancy: all bedroom and living room circuits minimum

**Retrofit cost note:** Retrofit penalty: MODERATE. Individual dimming requires wiring and switch installation per zone. At design stage this is standard electrical specification. Retrofit requires cable runs, switch replacement, and possible smart lighting overlay. See Part 12 §12.4.2.

**Key citations:** CAOT. (2018). Practice guidelines for acquired brain injury. CAOT. British Standards Institution. (2022). PAS 6463:2022. BSI. Rick Hansen Foundation. (2024). RHFAC v4.0, Category 11. RHF.

**Cross-reference:** B-04 (Flicker-Free LED); B-11 (Warm CCT); H-02 (Individual Environmental Control)

**Evidence basis (OT):** EHP Framework (adapt strategy). Individual dimming control allows each occupant to adapt the environmental lighting to their current sensory capacity; for users whose photosensitivity varies with fatigue state (PCS, OFS/CFS), this adaptive capacity is the difference between being able to occupy the space on a high-sensitivity day and not being able to.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Individual Dimming | Range | Notes |
|---|---|---|---|---|
| US | WELL v2 Feature L06 | Yes (WELL) | — | Voluntary |
| UK | PAS 6463:2022 | Recommended for NDV | — | Guidance only |
| DE | ASR A3.4 | Workplace lighting adjustable | — | — |
| **Guidebook** | **B-06** | **Yes — per occupied space** | **≥300 lux range** | **NDV/VIS/migraine** |

No building code mandates individual dimming as an accessibility provision. WELL and PAS 6463 address partially.


### B-07 Indirect and Cove Lighting in Sensitive Spaces
<!-- CON-0146 [HIGH]: B-06 individual dimming + B-07 indirect lighting — lighting quality convergence -->
<!-- CON-0166 [HIGH]: B-01/B-06/B-07/A-16 — circadian + dimming + indirect + sensory room — lighting cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:NDV|DEM -->
<!-- grade_confidence: LOW — Indirect/cove lighting in sensitive spaces: PAS 6463 + DSDC guidance + WELL v2. Expert consensus. No RCT. Tier 4-5. -->

**Applicable Groups:** AUT, PCS, PAIN, DEM · OFS
<!-- CON-0059: CON-0059: indirect lighting eliminates glare — OFS/PCS photosensitivity + PAIN photophobia (fibromyalgia) -->

**Description:** Uplighting, cove lighting, or indirect luminaires (source not directly visible from occupant positions) as the primary lighting strategy in sensory rooms, ABI recovery spaces, and dementia bedrooms. UGR <10 in sensitive spaces; UGR <19 in general spaces.

**Specifications:**

Primary lighting: indirect/cove (source not in direct view from any seated/lying position)

Glare: UGR <10 in sensitive spaces; UGR <19 in general spaces (EN 12464-1)

Supplementary downlights: deep recessed, diffuse lens, minimum 30° cutoff

Illuminance: 200--300 lux at task level achieved by indirect strategy

**Retrofit cost note:** Retrofit penalty: MODERATE. Indirect and cove lighting requires physical cove construction at ceiling or wall level. At design stage the cove is integrated into the ceiling design at modest cost. Retrofit requires suspended ceiling modification or new cove construction plus additional circuit provision. See Part 12 §12.4.2.

**Key citations:** CAOT. (2018). Practice guidelines for acquired brain injury. CAOT. British Standards Institution. (2022). PAS 6463:2022. BSI.

**Cross-reference:** B-06 (Dimming); B-03 (No Fluorescent)

**Evidence basis (OT):** Dunn's Sensory Processing Model. Indirect and cove lighting distributes illuminance across the ceiling and upper wall surfaces without creating the high-luminance point sources that trigger hyperarousal in sensory sensitive users; the absence of visible lamp surfaces removes the primary aversive stimulus in the visual field.

**Jurisdiction comparison:** No code mandates indirect lighting in sensitive spaces. DE DIN/TS 67600 recommends indirect component for biological effectiveness. UK PAS 6463 recommends glare-free lighting for NDV. Guidebook specifies indirect/cove as default in sensitive spaces based on NDV/VIS/migraine evidence.


### B-08 Matte, Low-Reflectance Floor Finishes (≤30 Gloss Units)
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:VIS|DEM -->
<!-- grade_confidence: MODERATE — Matte floor finishes ≤30 gloss units: CNIB guidance + DSDC EADDAT + BS 8300. LRV contrast evidence (Dain/Manandhar Tier 3 for VIS). No RCT specifically on gloss units. ≥6 jurisdictions reference low-reflectance floors. -->

**Applicable Groups:** PCS, VIS, DEM, AUT · PAIN · OFS
<!-- D2-41: D2-41: glare from high-gloss floors exacerbates OFS/PCS photosensitivity -->

**Description:** Floor finishes with gloss level ≤30 GU (60° gloss per ASTM D523) throughout occupied spaces and circulation. No polished concrete, high-gloss porcelain, or wet-look vinyl.

**Specifications:**

Maximum gloss: 30 GU (60° gloss per ASTM D523)

Applies to all hard floor surfaces in occupied spaces and circulation

Maintenance: high-traffic burnishing of LVT/vinyl can increase gloss above 30 GU; cleaning specification must maintain matte finish

Wet rooms: matte, R10 slip resistance takes priority

**Retrofit cost note:** Retrofit penalty: LOW. Matte, low-reflectance floor finishes are a procurement specification. Retrofit is floor

covering replacement only. See Part 12 §12.4.1.

**Key citations:** CAOT. (2018). Practice guidelines for acquired brain injury. CAOT. CNIB Foundation. (2024). Clearing our path. CNIB.

DSDC. (2022). EADDAT. University of Stirling.

**Cross-reference:** C-06 (Plain Low-Contrast Flooring); E-07 (Slip Resistance)

**Evidence basis (OT):** Biomechanical FOR. Floor gloss above 30 gloss units creates specularity that impairs the visual contrast detection ability of low-vision users and creates visual 'noise' that disorients VIS and DEM users navigating by floor-surface differentiation; PTV compatibility requirement ensures that matte specification does not reduce slip resistance below safe threshold.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Gloss Limit | Specular Reflection | Notes |
|---|---|---|---|---|
| US | ADA | Not specified | — | — |
| UK | PAS 6463:2022 | Matte recommended | Avoid glare | NDV provision |
| BS 8300 | — | Not specified | — | — |
| ISO | ISO 21542 | Not specified | — | — |
| **Guidebook** | **B-08** | **≤30 Gloss Units** | **Matte throughout** | **NDV/VIS glare reduction** |

No code specifies maximum gloss units for floor finishes as an accessibility provision. PAS 6463 recommends matte surfaces but without quantified threshold.


### B-09 Maximisation of Natural Light (Clerestory, Light Wells, Rooflights)
<!-- design_stage_lock: SD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: MODERATE — Maximise natural light: Ulrich 1984 PMID:6143402 (Science, Tier 3 — recovery from surgery with window view). Multiple healthcare design SRs confirm biophilic benefit (Tier 3). ≥8 jurisdictions reference daylight in accessible design. MODERATE — Tier 3 evidence, no built-env accessibility RCT. -->

**Applicable Groups:** ALL (especially MH, DEM, PAIN, NEU, OFS)

**Description:** Natural light maximised through building orientation, window-to-wall ratio, clerestory windows, light wells, and rooflights. All primary occupied spaces have direct natural light. Glare control required: solar shading on all south/west elevations.

**Specifications:**

Window-to-wall ratio: ≥40% on primary facades

All primary occupied spaces: direct natural light (minimum 2% daylight factor)

Circulation at decision points: natural light at minimum

Solar shading: external or mid-pane preferred; internal as last resort

Sill height: ≤750 mm AFF for seated and reclined views. Applicable where DEM, OFS, NEU are primary occupants (reclined or

seated views essential).

**Retrofit cost note:** Retrofit penalty: STRUCTURAL. Maximising natural light through clerestories, light wells, and rooflights is a fundamental building form decision. Retrofit requires structural assessment, temporary propping, lintel installation, weatherproofing, and internal making-good. Retrofit cost of a single rooflight can exceed the design-stage cost by 10×. See Part 12 §12.4.

**Key citations:** Ulrich, R.S. (1984). View through a window may influence recovery from surgery. Science, 224(4647). WELL Building Institute. (2024). WELL v2. IWBI.

**Cross-reference:** B-01 (Circadian Lighting); BIO-01 (Nature Views); B-05 (Transition Zones)

**Evidence basis (OT):** ART (Attention Restoration Theory); SRT (Stress Recovery Theory). Natural light from windows and skylights is the primary restorative element in the built environment per both ART and SRT; the ≥75% provision ensures that the majority of primary occupied time is spent with access to the visually restorative stimulus, reducing directed attention depletion for NEU, DEM, and OFS users.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Daylight Factor | Window Area | Notes |
|---|---|---|---|---|
| US | WELL v2 Feature L01 | ≥2% (WELL) | — | Voluntary |
| UK | BS 8206-2 / CIBSE LG10 | ≥2% recommended | AD L references | — |
| DE | DIN 5034 | ≥2% (workplaces) | ASR A3.4 | Mandatory workplace |
| EU | EN 17037:2018 | Daylight provision | By climate zone | New European standard |
| **Guidebook** | **B-09** | **Maximise** | **Clerestory, wells, rooflights** | **VIS + circadian benefit** |


### B-10 Visual and Vibrotactile Fire Alarm (Multi-Channel Throughout Building)
<!-- CON-0042 [HIGH]: Multi-channel alerting: visual + auditory + vibrotactile simultaneously across all alert types -->
<!-- CON-0157 [HIGH]: B-10 visual alarm + H-03 captioning + D-08 signage + E-08 corridor — public building cluster -->
<!-- CON-0164 [HIGH]: B-10 visual alarm + A-16 sensory room + K-04 vibrotactile — alert cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: CRITICAL -->
<!-- ot_appointment_trigger: conditional:DEAF|DBL -->
<!-- grade_confidence: HIGH — Visual + vibrotactile fire alarm multi-channel: BS EN 54-23 + NFPA 72 — universally mandated for DEAF populations. VE-protected per Part 8 (independent circuit mandatory). ≥12 jurisdictions mandate visual fire alarms. Efficacy evidence: physiologically sound (DEAF users cannot hear audio alarms). HIGH on provision mandate. -->

<!-- CON-0014 [HIGH]: New companion item required — Vibrotactile Alerting Device (sleeping areas): minimum vibration intensity, latency ≤3 s, coverage all sleeping rooms where DEAF/DBL/photosensitive populations are primary. Item code K-04 exists (vibrotactile alert) — cross-reference and ensure K-04 explicitly covers sleeping-area installation. Resolves strobe-seizure conflict: where strobes are contraindicated (NDV photosensitivity, epilepsy), vibrotactile is the resolution. -->
<!-- CON-0042 [HIGH]: DEAF visual alerting system (B-10) conflicts with VIS/NDV glare in shared spaces. Resolution: diffuser technology; strobe placement high on wall (>2100 mm AFF) reduces direct glare while maintaining visual coverage. Add installation note to B-10. -->

**Applicable Groups:** DEAF, DBL

**Description:** Visual Alarm Devices (VAD) installed in all areas where deaf or hard-of-hearing users may be present. Minimum 75 candela; 1--3 Hz flash rate; BS EN 54-23:2010 Category W compliant. Coverage: all sleeping areas, bathrooms, meeting rooms, assembly areas.

**Specifications:**

75 candela minimum; 1--3 Hz flash rate; BS EN 54-23:2010 Category W Coverage: all sleeping areas, bathrooms, meeting rooms, public assembly areas

Independent circuit from audio alarm system

Monthly test with visual confirmation logged

Position: visible from any point in room (ceiling or high-wall mount)

**Vibrotactile fire alarm (DBL — LIFE SAFETY):** In all sleeping areas where DBL users are resident or expected: bed-shaker vibrotactile alerting device connected to building fire alarm system. Latency ≤3 s from alarm activation. Vibration intensity sufficient to wake a sleeping person (per EN 54-23 equivalent for tactile channel). Backup battery ≥24 hr. Where photosensitive populations (NEU/epilepsy, NDV) occupy the same sleeping area, vibrotactile alarm is the PRIMARY alert mechanism and strobe is contraindicated — vibrotactile replaces visual, not supplements it. Cross-ref K-04 (Vibrotactile Alert Provision). Source: FDR-NEW-11 (DBL evacuation); CAN/ASC 2.2 Emergency Egress Standard; Krown KA300 system specification.

**Continuous tactile guidance to exit (DBL — LIFE SAFETY):** In all buildings where DBL users are resident: continuous handrail from private room door to building exit without interruption. Handrail to carry raised characters with braille on underside of horizontal section at each stair landing and decision point: floor number, direction of egress, tactile star at exit floor (per CAN/ASC 2.2 §12.6.1). Any gap in handrail continuity on the egress route is a life safety failure for DBL users. Source: FDR-NEW-11; CAN/ASC 2.2; DbI guidelines.

**Retrofit cost note:** Retrofit penalty: LOW -- MODERATE. Visual fire alarm strobe installation requires surface-mounted head and alarm circuit extension. In a finished building, surface-run cable is acceptable. Design stage conduit provision eliminates visible surface runs. See Part 11; Part 12 §12.4.

**Key citations:** British Standards Institution. (2010). BS EN 54-23:2010. BSI. British Standards Institution. (2017). BS 9999:2017. BSI.

**DBL evidence note:** [THIN BASE — Tier 2+4 only; no Tier 1 OT clinical research on DeafBlind built environments in any jurisdiction; March 2026]

**Cross-reference:** VI-EVAC-04 (Fire Alarm — VAD); A-11 (Hearing Loop); H-03 (Visual Paging)

**Evidence basis (OT):** Compensatory FOR. The visual fire alarm compensates for the absence of auditory fire alarm detection in Deaf/HoH and DBL users; the 110 cd output specification is derived from the minimum luminous intensity required to achieve reliable detection across the visual field at the maximum coverage distances specified in EN 54-23.

<!-- CON-0014/CON-0042: Multi-channel alerting required. Every alert event to be available through all three channels simultaneously: visual (strobe ≥110 cd) + auditory (≥75 dBA at bed) + vibrotactile (latency ≤3 s in sleeping areas). Vibrotactile alerting is mandatory where DEAF, DBL, or photosensitive populations (NEU/epilepsy, NDV) occupy sleeping spaces. See new item K-04 Vibrotactile Alert Provision. Populations: DEAF · DBL · NEU · NDV · ALL. -->

**Jurisdiction comparison:**

| Jurisdiction | Standard | Flash Rate | Visual Alarm Standard | Notes |
|---|---|---|---|---|
| US | ADA §702 / NFPA 72 | **≤2 Hz** | UL 1971 | Seizure risk mitigation |
| UK | BS 5839-1 | EN 54-23 categories | EN 54-23 W/C/O | Area coverage categories |
| EU | EN 54-23:2010 | ≤2 Hz implicit | EN 54-23 | Harmonised European |
| AU | AS 1670 | Referenced | — | NCC fire safety |
| DE | DIN VDE 0833-2 | Referenced | — | Fire alarm systems |
| ISO | ISO 7240 series | Referenced | — | Fire detection/alarm |
| **Guidebook** | **B-10** | **≤2 Hz** | **EN 54-23 coverage** | **DEAF vs NEU/NDV conflict resolved** |

≤2 Hz flash rate resolves the conflict between DEAF need for visual alerting and NEU/NDV photosensitive seizure risk.


### B-11 Warm Colour Temperature for Evening (≤2700 K After 19:00)
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DEM|NEU -->
<!-- grade_confidence: MODERATE — Warm colour temperature ≤2700K after 19:00: Circadian lighting science (Tier 1 — Brown et al. 2022, CIE S026). WELL v2 Feature L07 references evening colour temperature. DEM sleep evidence (Tier 3). ≥5 jurisdictions/standards reference evening lighting. MODERATE — evidence strong on principle; built-env implementation studies sparse. -->

**Applicable Groups:** DEM, NDV/MH, NEU · OFS · PAIN
<!-- CON-0073: warm CCT ≤2700K evening reduces photosensitivity load -->

**Description:** Evening lighting (after 19:00) shifts to ≤2700 K CCT and reduced intensity to support circadian wind-down. This is particularly critical in dementia care where sundowning is driven by circadian disruption. Paired with B-01 (daytime 4000--5500 K) for full circadian lighting strategy.

**Specifications:**

Evening CCT: ≤2700 K from 19:00

Evening intensity: ≤10 EML at eye level

DEM: automated shift at 19:00 via BMS (occupants cannot always be relied upon to initiate)

Where residential occupancy: manual override available for non-standard sleep schedules

**Retrofit cost note:** Retrofit penalty: LOW. Warm colour temperature (2700 K) is a lamp or luminaire specification change. Retrofit is lamp replacement in compatible luminaires, or luminaire swap. See Part 12 §12.4.1.

**Key citations:** WELL Building Institute. (2024). WELL v2. IWBI. Alzheimer's Disease International. (2020). World Alzheimer Report 2020. ADI.

**Cross-reference:** B-01 (Circadian Lighting daytime); B-06 (Dimming)

**Evidence basis (OT):** Dunn's Sensory Processing Model; PEOP Model.

Evening shift to ≤10 EML and 2700K CCT removes the alerting light wavelengths that inhibit melatonin production; for DEM users this is the primary circadian regulation intervention; for NEU/MH users it supports the occupation of restorative sleep — an occupation that environmental lighting directly enables or impairs.
**Description:** Permanent canopy or covered approach at accessible entry: minimum 3000 mm depth × 2000 mm width. Level or ≤1:50 gradient beneath canopy. Drainage to perimeter. For users: canopy height ≥2500 mm to accommodate bariatric scooters/powerchairs.


## CATEGORY C: COLOUR AND SURFACE FINISH

LRV = Light Reflectance Value (0 = black; 100 = white). All contrast specifications: LRV difference between adjacent surfaces unless stated. NCS = Natural Colour System. Gloss: measured at 60° per ASTM D523.

**Jurisdiction comparison:** No code specifies evening colour temperature limits. DE DIN/TS 67600:2022 recommends ≥2700K for evening in care settings. WELL v2 Feature L03 specifies colour temperature schedules. Guidebook specifies ≤2700K after 19:00 — derived from circadian melatonin suppression evidence (Brown et al. 2022).


### C-01 Colour Palette (Muted, Low-Chroma, Non-Institutional)
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:NDV|DEM -->
<!-- grade_confidence: LOW — Muted, low-chroma, non-institutional colour palette: PAS 6463 + ASPECTSS (Tier 4) + Co-1 NDV user research. No RCT on colour palette for NDV outcomes. Tier 4-5. -->

<!-- CON-0043 [HIGH]: C-01 muted palette conflicts with NDV/MH warm-colour preference. Resolution: muted palette as default in shared spaces; warm-colour biophilic breakout zones. Do not apply high-contrast marking in NDV/AUT-primary environments without MH zoning analysis. Item-specification-writer pass required: add NDV/MH conflict note and zone qualifier. -->

**Applicable Groups:** AUT, PCS, DEM, MH, NDV, OFS

**Description:** Primary wall colour: NCS chroma ≤4 (muted, desaturated) throughout all occupied spaces. No primary colours, no saturated hues. Accent colours (for zoning and wayfinding — C-02) may exceed NCS chroma 4 only where used as deliberate navigational landmarks, not as general decoration.

**Specifications:**

NCS chroma ≤4 on all primary wall surfaces

Accent/landmark colours: may exceed NCS chroma 4 only at designated wayfinding landmarks

No primary red, blue, or yellow as dominant wall colour

Ceiling: white or very pale (LRV ≥85) to reflect natural light

Floor: plain, low-chroma (C-06)

**Retrofit cost note:** Retrofit penalty: LOW. Colour palette specification is a decoration decision. Retrofit is redecoration --- the lowest-penalty category of change in any building. See Part 12 §12.4.1.

**Key citations:** British Standards Institution. (2022). PAS 6463:2022. BSI. Mostafa, M. (2021). ASPECTSS 2.0. Frontiers in Psychiatry, 12, 727353. DSDC. (2022). EADDAT. University of Stirling.

**Cross-reference:** C-02 (Colour Zoning); C-03 (Pattern Avoidance);

D-05 (Enclosed Refuge Spaces)

**Evidence basis (OT):** Allen's CDM; Dunn's Sensory Processing

Model. Muted, low-chroma colours reduce the visual complexity that constitutes an orientation challenge at Allen's cognitive levels 3--5 (DEM) and a sensory overload trigger at Dunn's sensory-avoiding and sensory-sensitive quadrants (NDV, AUT); the non-institutional palette also addresses the PEOP volition subsystem for MH users (non-clinical aesthetics support occupational identity).

**Jurisdiction comparison:** No code specifies colour palette. UK DSDC Stirling and King's Fund provide DEM-specific colour guidance. PAS 6463 recommends muted environments for NDV. Guidebook's muted, low-chroma, non-institutional palette is clinical/research-derived.


### C-02 Colour-Coded Wayfinding Zones (Distinct Warm Colour Per Wing/Zone)
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DEM|NDV -->
<!-- grade_confidence: LOW — Colour-coded wayfinding zones: DSDC EADDAT + Marquardt 2011 (HERD Tier 3). DEM wayfinding research supports colour coding for zone differentiation (Tier 3, single study). No RCT on colour zone effectiveness. ≥4 jurisdictions reference. -->

**Applicable Groups:** DEM, NDV, VIS (cognitive)

**Description:** Distinct warm colour per building wing or zone, consistent from entry to all spaces within that zone. Zone colour applied to: one accent wall per corridor bay (not all walls); door frames within zone; floor material accent strip. Layered on clear plan rather than substituting plan clarity.

**Specifications:**

Each zone: one distinct warm colour (LRV 50--65; NCS chroma 8--15)

Zone colour applied consistently throughout zone

Door frames: zone colour at ≥30 LRV contrast with wall (C-04 compatible)

Floor accent: zone colour strip at corridor centre or edge

No more than 5 distinct zone colours per building

**Retrofit cost note:** Retrofit penalty: LOW. Colour-coded wayfinding is a redecoration and signage programme without structural implications. See Part 12 §12.4.1.

**Key citations:** DSDC. (2022). EADDAT. University of Stirling. Marquardt, G. (2011). HERD, 4(2), 75--90. Grey, T., et al. (2015). Universal design guidelines: Dementia friendly dwellings. NDA Ireland.

**Cross-reference:** C-01 (Muted Palette); C-04 (LRV Contrast); D-04 (Landmarks)

**Evidence basis (OT):** Allen's CDM. Consistent colour-coding by function (toilets: same colour throughout the building; staff areas:

same colour throughout) implements Allen's CDM cognitive level 4 intervention: the environment provides a reliable object-level cue

that substitutes for abstract wayfinding reasoning when cognitive capacity for spatial abstraction is reduced.

**Jurisdiction comparison:** No code mandates colour-coded wayfinding. UK DSDC Stirling recommends distinct colours per wing for DEM orientation. ISO 3864 covers safety colour coding. Guidebook extends to all wayfinding zones based on DEM/NDV/VIS evidence.


### C-03 Pattern Avoidance (Plain Flooring and Walls in Sensitive Environments)
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:NDV|DEM -->
<!-- grade_confidence: LOW — Pattern avoidance in sensitive environments: PAS 6463 (Tier 4) + NDV lived experience. No RCT on pattern vs plain flooring for NDV outcomes. Visual noise research is Tier 4-5. -->

**Applicable Groups:** DEM, AUT, PCS, NDV, OFS

**Description:** No tessellated, geometric, or strongly patterned floor finishes in DEM, AUT, or PCS environments. Patterns create perceptual confusion (DEM: floor pattern perceived as steps or holes; AUT: visual overload). Plain, uniform colour flooring required.

**Specifications:**

No tessellated or geometric floor patterns in DEM/AUT/PCS environments

Stripe patterns (threshold marking, navigation): ≤200 mm width; maximum 3 stripes per zone

Wall patterns: no diagonals, spirals, or optical illusion patterns

LBD (Lewy Body Dementia): plain matte uniform flooring mandatory (see

§2.5)

**Retrofit cost note:** Retrofit penalty: LOW. Pattern avoidance is a floor and wall covering specification. Retrofit is covering

replacement without structural works. See Part 12 §12.4.1.

**Key citations:** DSDC. (2022). EADDAT. University of Stirling. Mostafa, M. (2021). ASPECTSS 2.0. Frontiers in Psychiatry, 12, 727353. National Autistic Society. (2023). Creating autism-friendly environments. NAS.

**Cross-reference:** C-06 (Plain Flooring); B-08 (Matte Floor)

**Evidence basis (OT):** Dunn's Sensory Processing Model.

High-chroma, saturated patterns at floor level constitute a visual stimulus in the hyperarousal frequency range for sensory-sensitive and sensory-avoiding users; pattern-free or low-pattern floor finishes in primary occupied spaces reduce the visual complexity input to the sensory processing system.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Pattern Restriction | Stripe/Check Limit | Photosensitive | Notes |
|---|---|---|---|---|---|
| US | ADA | Not addressed | — | — | — |
| UK | PAS 6463:2022 | **Plain surfaces recommended** | Avoid strong patterns | Yes | Only standard addressing patterns |
| UK | BS 8300 | — | — | — | Does not address |
| ISO | ISO 21542 | Not addressed | — | — | — |
| **Guidebook** | **C-03** | **Plain in sensitive areas** | **No bold geometric** | **≤3 Hz flicker avoidance** | **NDV/NEU/VIS evidence** |

UK PAS 6463 is the ONLY standard addressing pattern avoidance for neurodivergent populations. No other code restricts surface patterns.


### C-04 LRV Contrast (≥30 minimum; ≥50% LRV best practice at critical junctions)
<!-- CON-0043 [HIGH]: LRV ≥50% best practice; ≥65% Michelson at critical junctions; 30% = code minimum only -->
<!-- CON-0123 [HIGH]: D-02/D-06/D-08/C-04 — DEM wayfinding + colour + signage convergence cluster -->
<!-- CON-0127 [HIGH]: C-04 wall colour LRV + B-06 lighting CCT — visual contrast + circadian joint specification -->
<!-- CON-0156 [HIGH]: E-03 ramp + C-04 contrast + E-09 TWSI + B-04 flicker — circulation safety cluster -->
<!-- CON-0161 [HIGH]: C-04 LRV ≥65% Michelson at stair nosings — critical junction specification -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:VIS|DEM -->
<!-- grade_confidence: MODERATE — LRV ≥30% contrast: BS 8300 + CNIB + AS 1428.2 + multiple jurisdictions (≥10). Manandhar et al. 2022 (Work 73(4):1265-1278, DOI:10.3233/WOR-210997, Tier 3) — 30% Michelson = "poorly visible" at severe VI; ~65% needed for reliable detection. Citation mining 2026-05-04: Harper 2022 (J Ergonomics, DOI:10.35248/2165-7556-22.12.303) OR=2.87 fall reduction from contrast striping; Brown 2023 (Ergonomics 66(9), DOI:10.1080/00140139.2022.2141347) descent speed reduction; Harper 2025 (IJMR, DOI:10.2196/60622) 80% fall events at interstep riser variation ≥14mm + contrast striping reduces events. GRADE: MODERATE (jurisdictional convergence ≥10 + empirical evidence from Manandhar + Harper group). -->
<!-- CON-0043: ≥30 LRV = code-compliance minimum only. Best practice: ≥50% LRV at all contrast-dependent provisions. At platform edges, stair nosings, kerb lines: ≥65% Michelson. Pops: VIS · DEM · NDV/AUT · DBL. -->

<!-- CON-0060 [HIGH]: C-04 LRV ≥30 at critical junctions is Universal Mode (VIS, DEM — both require this for safety). NDV/SENS muted palette preference must not reduce safety contrast at critical junctions. Zone-based resolution applies: ≥30 LRV contrast mandatory at all step edges, door frames, and critical junctions regardless of zone. Muted palette applies to non-safety surfaces only. -->

**Applicable Groups:** VIS, DEM, MOB (fall prevention)

**Description:** Minimum 30 LRV difference between: floor and wall base; stair nosing and tread; door frame and wall; grab bar and wall; toilet seat and floor. Minimum 35 LRV in DEM/elderly public settings. Minimum 40 LRV in aged care/DeafBlind settings.

**Specifications:**

General: ≥30 LRV contrast at all critical junctions

DEM/elderly public: ≥35 LRV

Aged care/DeafBlind: ≥40 LRV

Stair nosings: ≥30 LRV full-width strip (55--75 mm depth)

Grab bars: LRV vs wall AND vs floor (JOTA, 2022)

Door frames: ≥30 LRV vs adjacent wall throughout building

**Retrofit cost note:** Retrofit penalty: LOW. LRV contrast ≥30 is achieved through paint, finish, and fixture selection. Retrofit is primarily redecoration and, at floor/fixture junctions, fixture replacement. See Part 12 §12.4.

**Key citations:** British Standards Institution. (2018). BS 8300:2018. BSI. CNIB Foundation. (2024). Clearing our path. CNIB. JOTA. (2022). Grab bar colour contrast. [Translated from Japanese.\] Manandhar, S. et al. (2022). Luminance contrast preferences of people with a vision impairment for elements in the built environment. *Work* 73(4):1265-1278. DOI:10.3233/WOR-210997. Harper, S.A. et al. (2022). Stairway visual contrast enhancement to reduce fall-related events. *J Ergonomics* 12:303. DOI:10.35248/2165-7556-22.12.303.

**Cross-reference:** C-05 (DEM floor transitions — inverse rule);

G-03 (Grab Bars)

**Evidence basis (OT):** Allen's CDM; Compensatory FOR. LRV ≥30 contrast at critical junctions compensates for the reduced visual contrast discrimination that occurs at Allen's CDM cognitive levels 3--4 (DEM) and for the reduced photopic contrast sensitivity of low-vision users (VIS); the 30 LRV threshold is derived from the minimum contrast visible to users in the target population range.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Min Contrast | Critical Contrast | Notes |
|---|---|---|---|---|
| US | ADA 2010 | **No numeric** | — | Significant gap |
| UK | BS 8300 | ≥30 LRV points | ≥70 LRV points | Most developed methodology |
| AU | AS 1428.1:2021 §12 | ≥30% | — | Aligns with UK minimum |
| DE | DIN 32975:2009 | Specified | — | Visual design standard |
| ISO | ISO 21542:2021 §39 | Referenced | — | Defers to national standards |
| **Guidebook** | **C-04** | **≥30 minimum** | **≥50 best practice** | **UK methodology; target between UK min and critical** |


### C-05 Low LRV Differential at Adjacent Floor Materials (DEM Inverse Contrast Rule)
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DEM -->
<!-- grade_confidence: LOW — Low LRV differential at adjacent floor materials (DEM inverse floor trap): DSDC EADDAT (Tier 5) + DSDC Stirling research (Tier 3). Dark mats = perceived holes — Tier Co-1/3. No RCT. ≥4 jurisdictions reference. -->

**Applicable Groups:** DEM

**Description:** INVERSE RULE from C-04: Between adjacent floor material zones (e.g., corridor carpet to room vinyl), LRV differential must be ≤10 to prevent the transition from being perceived as a step or edge by dementia users. This is opposite to C-04 (which requires ≥30 LRV) and applies specifically to floor-to-floor transitions only.

**Specifications:**

Adjacent floor materials: ≤10 LRV differential at transition

Floor-to-wall transitions: ≥30 LRV required (C-04 applies)

No sudden colour change at floor transitions in DEM environments

Tactile transition strip (≤3 mm height): permitted; colour must meet

≤10 LRV rule

**Retrofit cost note:** Retrofit penalty: LOW. Low LRV differential at adjacent floor materials is a flooring specification decision. Retrofit is flooring replacement at junctions. See Part 12 §12.4.1.

**Key citations:** DSDC. (2022). EADDAT. University of Stirling.

CNIB Foundation. (2024).

Clearing our path. CNIB.

**Cross-reference:** C-04 (LRV contrast — C-05 is the DEM-specific floor transition exception); [VI-08 — retired code] (Proprioceptive Design)

**Evidence basis (OT):** Allen's CDM. LRV ≤10 between adjacent floor materials prevents the visual signal of a 'step' (high-contrast floor transition) being generated where no step exists; for DEM users at Allen's cognitive levels 3--4, a high-contrast floor transition produces an avoidance response and gait interruption identical to the response to an actual step.

**Jurisdiction comparison:** No code addresses inverse contrast at floor-material junctions. UK BS 8300 addresses standard LRV contrast (≥30 points) but not DEM-specific inverse contrast avoidance. This is a guidebook-specific provision — dark floor strips can be perceived as voids by people with dementia.


### C-06 Plain, Low-Contrast Flooring [MERGED INTO C-03 per CO-0003/D2-22]
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: LOW — MERGED into C-03 per CO-0003. Inherited C-03 rating. No independent evidence review. -->
<!-- CO-0003: C-06 content absorbed into C-03. C-03 now covers: pattern avoidance + plain flooring specification. DEM fall prevention (+15% pattern-associated falls DSDC 2024) is primary rationale. --> (No Geometric Patterns)

**Applicable Groups:** DEM, AUT, PCS, OFS

**Description:** Plain, uniform, low-pattern floor finishes throughout. No geometric patterns, no tessellated tiles, no optical-illusion vinyl. Colour: low-chroma (NCS ≤4). Gloss: ≤30 GU (B-08). Note: C-06 and §2.5 LBD Caution are bidirectionally cross-referenced.

**Specifications:**

Floor: plain, uniform colour; NCS chroma ≤4

No tessellated, geometric, or optical-illusion patterns

Permitted: single-colour carpet, plain LVT, plain polished concrete (gloss ≤30 GU)

LBD environments: plain matte uniform mandatory (see §2.5)

**Retrofit cost note:** Retrofit penalty: LOW. Plain, low-contrast flooring is a floor covering specification. Retrofit is full floor

covering replacement without structural works. See Part 12 §12.4.1.

**Key citations:** DSDC. (2022). EADDAT. University of Stirling.

Mostafa, M. (2021). ASPECTSS 2.0. Frontiers in Psychiatry, 12, 727353.

**Cross-reference:** C-03 (Pattern Avoidance); B-08 (Matte Floor);

§2.5 DEM LBD Caution

**Evidence basis (OT):** Allen's CDM. Plain, matte, uniform flooring at LRV ≤10 across the floor surface prevents the visual stimuli (patterned tiles, geometric shapes, strong directional shadows) that are associated with visual hallucinations in Lewy Body Dementia and with floor surface misperception in all DEM types at cognitive levels 3--5.

## CATEGORY D: SPATIAL LAYOUT AND WAYFINDING

Wayfinding is the ability to determine one's location, plan a route, and navigate to a destination. For DEM, VIS, and NDV users, wayfinding failure is the primary built environment access barrier.

**Jurisdiction comparison:** MERGED — see C-03 (Pattern Avoidance).


### D-01 Loop Floor Plan (No Dead-End Corridors in DEM Environments)
<!-- design_stage_lock: B -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:DEM -->
<!-- grade_confidence: MODERATE — Loop floor plan for DEM environments: Marquardt & Schmieg 2009 (AJAD Tier 3) + Bowes et al. 2019 Stirling SR (429 items, Tier 3). PMC8725382 (NL floorplan study, Tier 3). Floor plan configuration confirmed as most influential factor. ≥5 jurisdictions reference loop plans for DEM care. MODERATE — multiple Tier 3 studies converge; no RCT. -->

**Applicable Groups:** DEM · VIS · DBL · NDV/AUT
<!-- CON-0001: Universal Mode: 5 populations require consistent loop/single-path circulation from independent clinical rationales -->

**Description:** All circulation designed as continuous loops from entry through primary spaces. No dead-end corridors. If structural constraints require dead-ends: end wall treated as a landmark (artwork, window, planting) with return route clearly signed.

**Specifications:**

No dead-end corridors longer than 5 m

All circulation: loop or T-junction configuration

Dead end terminations: treated as destination landmarks with return signage

Toilet access: visible from all primary loop positions (D-03)

**Retrofit cost note:** Retrofit penalty: STRUCTURAL. Loop floor plan with no dead-end corridors is a fundamental plan organisation decision. Achieving a loop plan through retrofit requires removing or adding walls — potentially structural — and fundamentally reorganising internal layouts. In many existing buildings this is practically impossible without near-total internal reconstruction. At design stage it is zero-cost planning. See Part 12 §12.4.

**Key citations:** Marquardt, G. (2011). HERD, 4(2), 75--90. DSDC. (2022). EADDAT. University of Stirling.

**Cross-reference:** D-03 (Toilet Visibility); D-04 (Landmarks); D-11 (Safe Garden)

**Evidence basis (OT):** Allen's CDM. The loop floor plan with a single continuous route and visible destination at every point

implements Allen's CDM cognitive level 4 design principle: the environment reduces spatial decision-making to a single action

(continue forward) and eliminates the executive function demand of route selection that exceeds cognitive level 4 capacity.

**Jurisdiction comparison:** No code mandates loop floor plans. UK DSDC Stirling recommends loop layouts for DEM — eliminates dead-end disorientation. Guidebook specifies for all DEM environments.


### D-02 Cognitive Simplicity (Single Primary Route from Entry to Destination)
<!-- CON-0043 [HIGH]: LRV ≥50% best practice; ≥65% Michelson at critical junctions; 30% = code minimum only -->
<!-- CON-0115 [HIGH]: D-09 consistent layout + D-02 single primary route — DEM spatial predictability -->
<!-- CON-0116 [HIGH]: E-01 lift ≥1400mm + D-02 cognitive legibility at lift arrival -->
<!-- CON-0123 [HIGH]: D-02/D-06/D-08/C-04 — DEM wayfinding + colour + signage convergence cluster -->
<!-- CON-0125 [HIGH]: D-02/D-06/D-08 — DEM/IntD wayfinding pictogram + layout predictability -->
<!-- CON-0130 [HIGH]: D-02 cognitive route clarity — healthcare matrix NR-HLT cross-reference -->
<!-- CON-0153 [HIGH]: D-02/D-05/D-06 — wayfinding + retreat + memory box — DEM cognitive cluster -->
<!-- CON-0160 [HIGH]: D-02 cognitive route — additional DEM/NEU wayfinding evidence -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:DEM|NEU|NDV -->
<!-- grade_confidence: MODERATE — Cognitive simplicity / single primary route: Passini 1984 (wayfinding theory, Tier 3 equivalent) + Iwarsson & Ståhl 2003 (Disabil Rehabil framework). ≥6 jurisdictions reference. Tier 3 + standards convergence. -->

<!-- CON-0001 [HIGH]: Universal Mode convergence — DEM, VIS, DBL, DEM/NDV[IntD-proxy], NDV/AUT all require consistent, predictable circulation. Synthesis: add Universal Mode universal circulation legibility note to this item. All buildings to provide loop or single-path circulation with no dead-ends; consistent furniture arrangement; 3D landmark objects at every decision point. -->

**Applicable Groups:** DEM, NDV, VIS (cognitive) · DBL · NDV/AUT · DEM/NDV[IntD proxy] proxy→DEM/NDV
<!-- CON-0001: CON-0001: ≤2 route choices per decision point; consistent furniture arrangement (CON-0067) -->

**Description:** All primary building journeys follow a single, legible primary route. No user should need to choose between multiple routes at any decision point unless routes are equivalent and clearly signposted. Decision point = any junction with ≥2 route options.

**Specifications:**

Maximum 1 route decision at any single point from entry to primary destination

Where multiple routes exist: clear wayfinding signage at every decision point

Primary route: shortest + most direct (not hidden accessible route)

Decision point legibility: destination visible from decision point where possible

**Retrofit cost note:** Retrofit penalty: HIGH. Cognitive simplicity through a single primary route requires spatial reorganisation of circulation. Retrofit involves partition removal, route reconfiguration, and wayfinding redesign — significant works in complex existing buildings. See Part 12 §12.4.2.

**Key citations:** Passini, R. (1984). Wayfinding in architecture. Van

Nostrand Reinhold. Marquardt, G. (2011). HERD, 4(2), 75--90.

**Cross-reference:** D-04 (Landmarks); D-08 (Signage)

**Evidence basis (OT):** Allen's CDM; Compensatory FOR. Direct, short routes compensate for the reduced working memory capacity at Allen's CDM cognitive levels 3--4 by minimising the number of spatial 'chunks' that must be held in memory between decision points; for VIS users route directness reduces the cognitive wayfinding load that accumulates over long non-direct routes.

**FDR-NDV-02 [THIN — Tier 1 mechanism only]:** Interoceptive processing delay in NDV/AUT (Garfinkel et al. 2016, *Cortex* Tier 1 — mechanism; no built environment RCT) — delayed awareness of bladder urgency increases risk of incontinence incidents in NDV-occupied spaces. WC or water point to be within 20 m one-way of any primary NDV occupied space (classroom, workstation zone, sensory room). ○ [architectural implication — THIN-POPULATION-SPEC; no design standard specifies this distance]

**Jurisdiction comparison:** No code specifies single primary route. UK PAS 6463 recommends simple layouts for NDV. DSDC Stirling addresses for DEM. Guidebook's "single primary route" is design guidance, not a codified standard.


### D-03 Toilet Visibility from Primary Occupied Spaces (No Navigation Required)
<!-- design_stage_lock: B -->
<!-- ve_risk: CRITICAL -->
<!-- ot_appointment_trigger: conditional:DEM -->
<!-- grade_confidence: MODERATE — Toilet visibility from occupied spaces: Marquardt 2011 (HERD Tier 3) — toilet proximity to bedroom reduces confusion. DSDC EADDAT guidance. DEM incontinence evidence: 47% claim REMOVED as UNVERIFIED-QUANT. Base evidence: Tier 3 (Marquardt). NOT-RETROFITTABLE — brief-stage design decision. MODERATE on direction; quantified % claim excised. -->

**Applicable Groups:** DEM, PAIN (MS bladder urgency), MOB · OFS
<!-- D2-41: D2-41: toilet visibility reduces navigation distance and effort — OFS/PAIN energy conservation; DEM orientation -->

**Description:** Toilet door visible from all primary occupied spaces without requiring navigation. Toilet door LRV ≥30 contrast against

corridor wall. Sightline unobstructed at 600--1600 mm height.

**Specifications:**

Toilet door visible from primary occupied space

Sightline: unobstructed at 600--1600 mm height

Toilet door: ≥30 LRV contrast against corridor wall (C-04)

Maximum 20 m from any primary occupied space to nearest toilet (MS bladder urgency)

**Retrofit cost note:** Retrofit penalty: HIGH. Toilet visibility from primary occupied spaces requires sight-line planning. Retrofit requires spatial reorganisation or transparent partition introduction; where structural walls are involved the intervention is major. At design stage, toilet positioning is a zero-cost planning decision. See Part 12 §12.4.2.

**Key citations:** Marquardt, G. (2011). Wayfinding for people with dementia: A review of the role of architectural design. HERD, 4(2), 75--90. [Landmark German-language OT research: 32-facility study documenting 47% [UNVERIFIED-QUANT — this figure has been removed from the BPC as unverifiable; do not cite as evidence-based. See spec-db-part4-reconciliation Section C1 and project-standards 2026-04-09] reduction in incontinence events where toilet is directly visible from primary living space. Strongest single empirical finding for any spatial provision in this Guidebook.\] Kirch, M., \& Marquardt, G. (2023). HERD, 16(1). doi:10.1177/19375867221119540 Multiple Sclerosis International Federation. (2023). Atlas of MS. MSIF.

**Cross-reference:** D-01 (Loop Plan); G-03 (Grab Bars in Bathroom)

**Evidence basis (OT):** Allen's CDM; Life Balance Model. Accessible toilets ≤20m from all primary occupied spaces compensates for the reduced continence planning capacity in DEM (cognitive levels 3--4) and the bladder urgency in MS/NEU users; the Life Balance Model grounds the 20m specification as the exertion budget for OFS and PAIN users for whom further travel to a toilet constitutes a significant energy expenditure.

**Jurisdiction comparison:** No code requires toilet visibility from occupied spaces. UK DSDC Stirling recommends for DEM. Guidebook specifies visual connection or direct sightline — derived from DEM continence management evidence.


### D-04 Landmarks at Every Decision Point
<!-- design_stage_lock: SD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DEM|NEU -->
<!-- grade_confidence: LOW — Landmarks at every decision point: DSDC EADDAT + CNIB + cognitive mapping theory (Tier 3 Lynch 1960). No RCT on landmark density for DEM/NEU outcomes. Tier 4-5 guidance. -->

**Applicable Groups:** DEM, VIS, NDV · NEU · OFS
<!-- CON-0030: CON-0030: cognitive wayfinding reduces navigation effort — energy conservation for OFS/NEU; landmark-based strategy -->

**Description:** A permanent, distinctive landmark at every navigation decision point (corridor junction, lift lobby, stair head). Landmark types: permanent artwork; distinct wall colour or plane; planted element; water feature (switchable); distinctive floor pattern (DEM-safe per C-05). Landmark must be visible from ≥5 m approach.

**Specifications:**

Permanent landmark at every decision point

Visible from ≥5 m approach

Types: artwork, plant, water, distinct material, colour zone change

DEM: landmark must be at same position 24/7 (no removable elements)

VIS: acoustic landmark (distinct floor material or water feature) preferred

**Retrofit cost note:** Retrofit penalty: LOW. Landmark installation at decision points is implementable through surface-applied works

without structural intervention. See Part 12 §12.4.1.

**Key citations:** CNIB Foundation. (2024). Clearing our path. CNIB. DSDC. (2022). EADDAT. University of Stirling. Siegel, A.W., \& White, S.H. (1975). Advances in child development and behavior (Vol. 10). Academic Press.

**Cross-reference:** D-01 (Loop Plan); C-02 (Colour Zoning); BIO-03 (Texture Variety); BIO-04 (Water Features)

**Evidence basis (OT):** Allen's CDM; Compensatory FOR. Landmark objects at every decision point implement Allen's CDM level 4 wayfinding principle (concrete, familiar objects as navigational anchors) and compensate for the absent visual environmental information that VIS users would otherwise use for orientation; the specificity requirement (real, familiar, not generic decoration) is derived from CDM level 4 object recognition research.

**Jurisdiction comparison:** No code mandates landmarks at decision points. UK PAS 6463 and DSDC Stirling reference landmarks for NDV/DEM. ISO 21542 §40 references wayfinding landmarks. Guidebook specifies distinctive landmarks at EVERY decision point.


### D-05 Enclosed Low-Stimulation Spaces (Focus Rooms, Breakout Alcoves, and Compartmentalisation)
<!-- CON-0040 [HIGH]: Unified sensory environment system: Dunn profiles → spatial zones → quantified parameters -->
<!-- CON-0046 [HIGH]: NHS CAMHS: sensory refuge mandatory (not optional) where NDV/AUT + NDV/MH co-occurrence foreseeable -->
<!-- CON-0117 [HIGH]: I-03 TMV ≤38°C + D-05 low-stimulation + A-16 sensory room — OFS/NDV/MH cluster -->
<!-- CON-0152 [HIGH]: D-05 low-stimulation space + I-03 TMV — OFS/NEU quiet + thermal cluster -->
<!-- CON-0153 [HIGH]: D-02/D-05/D-06 — wayfinding + retreat + memory box — DEM cognitive cluster -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:NDV|DEM|NEU|NDV/MH -->
<!-- grade_confidence: LOW — Enclosed low-stimulation spaces: PAS 6463 (Tier 4) + Wilson 2023 PMID (Co-1, AU mental health service user). No RCT on quiet room provision for NDV/MH outcomes. VERY LOW on room size threshold; LOW overall. -->

<!-- CON-0046 [HIGH]: In MH inpatient settings, D-05 low-stimulation spaces are critical for NDV/AUT patients. MH de-escalation rooms do not meet NDV/AUT sensory needs (CS-17 NDTi 2022). -->
<!-- CON-0051 [HIGH]: Loop/linear circulation with no dead-ends serves DEAF (visual scan), VIS (tactile memorisation), DBL (tactile navigation), DEM (disorientation prevention), IntD (cognitive load reduction). Universal Mode candidate — see CON-0001. -->
**Applicable Groups:** NDV, PCS, MH, OFS · PAIN
<!-- D2-41: D2-41: low-stimulation retreat reduces exertion load for OFS; pain flare prevention -->

**Description:** Enclosed focus rooms (minimum 6 m²) for individual or paired concentration work. STC ≥35 partition. RT60 ≤0.4s. Full dimming. No visual connection to open-plan area. Bookable or first come-first-served. Minimum 1 per 20 open-plan desks.

*Breakout alcoves (formerly D-06):* Semi-enclosed alcoves (minimum 3 m², 3 walls + open or acoustic-curtain front) accessible from open-plan without passing through occupied spaces. Acoustic: NRC ≥0.70 on 3 interior walls. Equal design quality to surrounding area.

*Compartmentalisation (formerly F-02):* Alcoves, sub-rooms, and compartmentalised sub-spaces in all large open-plan areas. Maximum open-plan zone 200 m² without acoustic sub-division. Alcoves: 3 m²; 3-wall enclosure; NRC ≥0.70. Sub-rooms: STC ≥35 partition. All sub-zones equal design quality.

**Specifications:**
Area: 6 m² (individual); 10 m² (paired)
Partition: STC ≥35
RT60: ≤0.4 s
Full dimming: 100%--10 lux
No transparent panels to open-plan area (visual privacy)
Minimum: 1 per 20 open-plan workstations

**Retrofit cost note:** Retrofit penalty: MODERATE -- HIGH. Enclosed low-stimulation spaces require dedicated floor area and acoustic separation. Retrofit within an occupied building requires partition installation, acoustic treatment, and area allocation. Cost depends on whether structural works are needed. See Part 12 §12.4.2.

**Key citations:** British Standards Institution. (2022). PAS 6463:2022. BSI. AtkinsRéalis. (2024). Neuroinclusive office design v3. AtkinsRéalis.

**Cross-reference:** A-16 (Sensory Room); G-01 (Defensible Seating); F-01 (Sensory Gradient)

**FDR-NDV-01 [THIN — Tier 5]:** Proprioceptive underresponsivity (Dunn quadrant 1) — under-foot textured floor zone (300 mm border of tactile mat or textured vinyl) at focus room entry may support self-regulation for NDV/AUT low-registration users. Conflict: DEM visual floor uniformity (C-06) — limit texture to under-foot zone only, no surface pattern change visible in plan. ○ [THIN-POPULATION-SPEC]

**Evidence basis (OT):** EHP Framework (create strategy); Dunn's

Sensory Processing Model. Focus rooms create an environmental context that enables sustained cognitive occupation (concentrated work, private communication) that is impossible in open-plan environments for sensory-sensitive and PCS users; the STC ≥35 partition and NC-25 HVAC specification define the minimum acoustic context required for this occupation.

**Jurisdiction comparison:** No code mandates low-stimulation spaces. UK PAS 6463:2022 recommends quiet/calm spaces for NDV. Guidebook specifies enclosed focus rooms, breakout alcoves — derived from NDV/AUT sensory regulation evidence. Cross-reference A-16 (sensory room).


### D-06 Memory Boxes at Private Office and Residential Room Entrances
<!-- CON-0043 [HIGH]: LRV ≥50% best practice; ≥65% Michelson at critical junctions; 30% = code minimum only -->
<!-- CON-0123 [HIGH]: D-02/D-06/D-08/C-04 — DEM wayfinding + colour + signage convergence cluster -->
<!-- CON-0125 [HIGH]: D-02/D-06/D-08 — DEM/IntD wayfinding pictogram + layout predictability -->
<!-- CON-0153 [HIGH]: D-02/D-05/D-06 — wayfinding + retreat + memory box — DEM cognitive cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DEM -->
<!-- grade_confidence: LOW — Memory boxes at residential room entrances: DSDC EADDAT + Alzheimer's Society UK guidance (Tier Co-1). No RCT on memory box effectiveness for DEM orientation. Tier 4-5. -->

**Applicable Groups:** DEM · NEU · DBL
<!-- CON-0090: personalised entry cues serve NEU (ABI) spatial memory and DBL tactile recognition -->

**Description:** Shadow box display case (minimum 300×300 mm) mounted beside each residential room or private office entrance at eye level. Resident/occupant personalises with their own objects and photographs to enable room identification independent of room number or signage.

**Specifications:**

Minimum 300×300 mm illuminated shadow box

Mounted: 1300--1500 mm AFF (centre); adjacent to door frame

Contents: occupant's personal objects (provided and refreshed by occupant/family)

Backing: plain contrast colour ≥30 LRV from objects

Glass: non-reflective

**Retrofit cost note:** Retrofit penalty: LOW. Memory boxes are surface-mounted shallow fixtures. Retrofit is a fixing and decoration

operation without structural implication. See Part 12 §12.4.1.

**Key citations:** DSDC. (2022). EADDAT. University of Stirling. Alzheimer's Society UK. (2023). Design for dementia guidance.

**Cross-reference:** D-04 (Landmarks); D-08 (Signage); C-04 (LRV

Contrast)

**Evidence basis (OT):** Allen's CDM. Dead-end elimination removes a wayfinding failure mode that is specifically dangerous at Allen's CDM cognitive level 3--4: dead ends are not recognisable as such at these cognitive levels and produce wandering behaviour and distress that orientation-intact users do not experience.

**Jurisdiction comparison:** No code mandates memory boxes. UK DSDC Stirling and Dementia Services Development Centre recommend personalisation cues at room entrances for DEM. Guidebook-specific provision for DEM residential settings.


### D-07 No Blind Corners (Curved or Mirrored at All Hidden Junctions)
<!-- design_stage_lock: SD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DEM|DEAF -->
<!-- grade_confidence: LOW — No blind corners: DSDC guidance + DeafSpace sightline requirements (Tier 2 co-design). Geometric rationale sound. No RCT. Tier 4-5. -->

**Applicable Groups:** VIS, DEM, MH · OFS · PAIN · NDV/MH
<!-- CON-0091: mirrored corners reduce startle response and surprise exertion trigger for OFS/PAIN/MH -->

**Description:** No right-angle blind corners on primary circulation routes. Corners treated with: 45° splay; convex mirror (minimum 300 mm diameter); or glazed panel with vision panel through corner. Applies at all corridor junctions on primary accessible routes.

**Specifications:**
No blind right-angle corners on primary circulation
Treatment: 45° splay, convex mirror ≥300 mm, or vision-panel corner
Mirror: positioned for sightline from 2 m approach on each leg
Vision-panel glass: safety glazing (Class 2 or better); obscure if privacy required

**Retrofit cost note:** Retrofit penalty: LOW -- MODERATE. Curved or mirrored junctions at blind corners require finish and joinery modification. Retrofit is a decoration and joinery programme; structural corner modification is more significant. See Part 12 §12.4.1.

**Key citations:** CNIB Foundation. (2024). Clearing our path. CNIB. DeafSpace Project, Gallaudet University. (2010). DeafSpace design guidelines.

**Cross-reference:** D-10 (Transparent Partitions); G-01 (Defensible

Seating)

**Evidence basis (OT):** Allen's CDM; Compensatory FOR. Pictogram + large character signage implements Allen's CDM level 4 intervention

(action-based, visual cues rather than language-dependent abstract text) and compensates for the reduced symbol-reading capacity in

acquired low-literacy disability (VIS, DEM, post-stroke aphasia).

**Jurisdiction comparison:** No code restricts blind corners on accessibility grounds. UK PAS 6463 recommends clear sightlines for NDV. Gallaudet DeafSpace specifies sightlines for DEAF. Guidebook's 45° splay / convex mirror / vision-panel treatment is derived from DEM startle response and DEAF visual connectivity research.


### D-08 Pictogram + Single-Word Signage Throughout
<!-- CON-0123 [HIGH]: D-02/D-06/D-08/C-04 — DEM wayfinding + colour + signage convergence cluster -->
<!-- CON-0125 [HIGH]: D-02/D-06/D-08 — DEM/IntD wayfinding pictogram + layout predictability -->
<!-- CON-0157 [HIGH]: B-10 visual alarm + H-03 captioning + D-08 signage + E-08 corridor — public building cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DEM|NDV -->
<!-- grade_confidence: LOW — Pictogram + single-word signage: BS 8300 + intellectual-disability BPC (NDIS SDA Tier 4) + CSA B651. Tier 4-5. No RCT on pictogram density for IntD/DEM orientation outcomes. -->

**Applicable Groups:** DEM, NDV, VIS (cognitive), DBL · NEU · OFS
<!-- CON-0092: low-text wayfinding reduces cognitive effort for NEU/OFS -->

**Description:** All wayfinding signage uses pictogram + single word. No multi-line text. No symbol-dense information panels. Consistent font: rounded sans-serif (e.g., Arial, Frutiger). Character height ≥150 mm at 10 m viewing distance. Contrast ≥30 LRV. Braille equivalent at all directional and room identification signage.

**Specifications:**
Pictogram: above or left of word; minimum 50 mm height
Word: single-word descriptor; sentence case; rounded sans-serif
Character height: ≥150 mm at 10 m viewing distance
Contrast: ≥30 LRV text vs background
Braille: Grade 2 Braille equivalent at 1400--1600 mm AFF at all room
ID signs
Tactile lettering: raised 0.8 mm; at 1400--1600 mm AFF

**Retrofit cost note:** Retrofit penalty: LOW. Pictogram and signage installation is a surface-mounted programme. Retrofit is signage

replacement and mounting without structural works. See Part 12 §12.4.

§8.4.1.

**Key citations:** CNIB Foundation. (2024). Clearing our path. CNIB. DSDC. (2022). EADDAT. University of Stirling. UNAPEI. (2022). Facile à lire et à comprendre [French\]. UNAPEI. Plena Inclusión España. (2022). Lectura Fácil en entornos físicos [Spanish\].

**DBL evidence note:** [THIN BASE — Tier 2+4 only; no Tier 1 OT clinical research on DeafBlind built environments in any jurisdiction; March 2026]

**Cross-reference:** D-02 (Cognitive Simplicity); D-06 (Memory Boxes);

D-04 (Landmarks)

**Evidence basis (OT):** Allen's CDM. Pictogram + single-word signage is the most direct application of Allen's CDM level 4 design principle in the guidebook: level 4 users can process a familiar object image plus one concrete action word, but cannot reliably process multi-word directional sentences or abstract symbols.

**FDR-IntD-01 [Tier 2 — Silverman 2010; Tier 4 — NDIS SDA]:** Reduced abstract reasoning in IntD — concrete landmark-based wayfinding is the primary system; alphanumeric signage is backup only. Mechanism differs from DEM (which is memory loss): IntD users may not decode abstract symbols or letter-number sequences reliably but can navigate via object landmarks. Concrete 3D landmark objects at every decision point (D-04) are co-primary with pictogram signage (D-08) in IntD-occupied settings. DEM wayfinding provisions (D-02, D-04, D-08) are the strongest available proxy.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Sign Height | Tactile/Braille | Pictogram Standard |
|---|---|---|---|---|
| US | ADA 2010 §703 | 1220-1524mm (raised char.) | Yes — Grade 2 Braille | ISA + ADA pictograms |
| UK | BS 8300-2:2018 §12 | 1400-1700mm | Tactile recommended | BS EN ISO 7010 |
| AU | AS 1428.1:2021 | 1200-1600mm | Tactile required | AS 1428.1 pictograms |
| DE | DIN 32975 / DIN 18040 | 1200-1600mm | Tactile per DIN 32986 | DIN EN ISO 7010 |
| ISO | ISO 21542:2021 §40 | 1200-1600mm | Referenced | ISO 7010 |
| **Guidebook** | **D-08** | **Per jurisdiction** | **Pictogram + single word** | **ISO 7010 base** |


### D-09 Consistent Furniture Layout (No Rearrangement Without User Consultation)
<!-- CON-0115 [HIGH]: D-09 consistent layout + D-02 single primary route — DEM spatial predictability -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DEM -->
<!-- grade_confidence: LOW — Consistent furniture layout: DSDC EADDAT + CNIB guidance. DEM/VIS spatial predictability — Tier 4-5 consensus. No RCT. -->

<!-- CON-0001 [HIGH]: Universal Mode convergence — DBL and NDV/AUT depend on spatial consistency for tactile wayfinding and sensory predictability respectively. Add to Applicable Groups: DBL, NDV/AUT, VIS (in addition to DEM). Specification to note: furniture rearrangement protocols required; prior notification to DBL occupants mandatory. -->

**Applicable Groups:** DEM, VIS, NDV · OFS · PAIN · DBL
<!-- CON-0053: CON-0053: furniture permanence is safety requirement for DBL; reduces OFS exertion from navigating obstacles -->

**Description:** Furniture layout in primary occupied spaces maintained consistently. No rearrangement of furniture or wayfinding elements without prior consultation with primary users. Applies particularly in DEM care and VIS specialist environments where spatial memory is a primary navigation strategy.

**Specifications:**
Furniture arrangement: permanent/semi-permanent in DEM and VIS environments
Any rearrangement: documented and communicated to all identified users minimum 5 days in advance
Floor markings: furniture position marked on floor plan and maintained by facilities management
No ad-hoc event furniture in primary wayfinding corridors

**Retrofit cost note:** Retrofit penalty: ZERO. Consistent furniture layout is a management and procurement decision with zero build cost

at any stage. See Part 12 §12.4.1.

**Key citations:** DSDC. (2022). EADDAT. University of Stirling. CNIB Foundation. (2024). Clearing our path. CNIB.

**Cross-reference:** D-04 (Landmarks); D-02 (Cognitive Simplicity)

**Evidence basis (OT):** Allen's CDM; Compensatory FOR. Colour-coded floor zones compensate for the abstract spatial memory required to navigate multi-destination buildings at cognitive levels 3--4; the floor colour provides a continuously visible, non-language-dependent cue to location that substitutes for the spatial reasoning that DEM users have lost.

**Jurisdiction comparison:** No code addresses furniture layout consistency. UK DSDC Stirling recommends stable layout for DEM. Guidebook specifies no rearrangement without user consultation — derived from VIS spatial mapping and DEM routine disruption evidence.


### D-10 Transparent Glazed Panels in Internal Partitions
<!-- design_stage_lock: SD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:DEAF|DEM -->
<!-- grade_confidence: MODERATE — Transparent glazed panels: DeafSpace guidelines (Gallaudet, Tier 2 co-design). Sightline requirement for sign language communication and DEM transparency. ≥4 jurisdictions reference. MODERATE — strong co-design evidence + jurisdictional adoption. -->

<!-- CON-0074 [HIGH]: DeafSpace glazed junctions for DEAF visual advance warning potentially conflict with VIS glare, DEM reflective surface confusion, NDV visual noise. Requires matte glazing + strategic placement. Resolution: Part 5 multi-population conflict. -->
**Applicable Groups:** VIS, DEM, MH, DEAF · OFS
<!-- D2-41: D2-41: visual sightlines reduce navigation effort and disorientation -->

**Description:** Internal partition walls at corridors and meeting rooms include vision panels or full-height glazed panels to maintain sightlines. Allows occupants to see ahead before entering a space. For Deaf users (DeafSpace Principle 1): visual awareness of approaching persons.

**Specifications:**

Vision panel: minimum 500×1000 mm; positioned 900--1800 mm AFF

Full-height glazed alternative where privacy not required

Safety glazing: Class 2 minimum (BS EN 12600)

Obscure glass: where privacy required (e.g., consulting rooms)

Sightlines: occupant inside room can see corridor approach from seated position

**Retrofit cost note:** Retrofit penalty: MODERATE. Transparent glazed panels require cutting an opening into an existing partition and installing a glazed panel — a moderate joinery and glazing operation; structural partition involvement increases cost significantly. At design stage, specification is the only cost. See Part 12 §12.4.2.

**Key citations:** DeafSpace Project, Gallaudet University. (2010). DeafSpace design guidelines. British Standards Institution. (2018). BS 8300:2018. BSI.

**Cross-reference:** D-07 (No Blind Corners); B-02 (Face

Illumination); G-01 (Defensible Seating)

**Evidence basis (OT):** EHP Framework (alter strategy). Transparent glazed panels alter the visual context by making the activity visible

inside rooms before entry, eliminating the decision uncertainty of

'what is behind this door' that constitutes a cognitive barrier for

DEM users and a safety concern for MH users who require advance visibility of the space they are entering.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Internal Glazing | Manifestation | DeafSpace | Notes |
|---|---|---|---|---|---|
| US | ADA / Gallaudet DeafSpace | Not required | — | Visual connectivity principle | Not codified |
| UK | BS 8300-2:2018 §8.4 | Vision panels in doors | ≥2 manifestation bands | — | Safety glazing required |
| DE | DIN 18040 | Vision panels | — | — | — |
| AU | AS 1428.1 | Referenced | — | — | — |
| ISO | ISO 21542:2021 §14 | Vision panels in doors | Manifestation | — | — |
| **Guidebook** | **D-10** | **Internal partitions** | **LRV ≥30 contrast** | **DEAF sightlines** | **Beyond door panels** |

Guidebook extends transparent glazing beyond door vision panels to internal partitions — based on DeafSpace visual connectivity principles (Bauman & Murray, Gallaudet).


### D-11 Safe Accessible Garden (Loop Path, Secured Perimeter, Seating Every 20 m)
<!-- design_stage_lock: SD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:DEM|OFS -->
<!-- grade_confidence: MODERATE — Safe accessible garden with loop path: Gonzalez & Kirkevold 2014 J Clin Nurs (Tier 3 scoping review — horticultural therapy + dementia). DSDC EADDAT. Helsedirektoratet NO guidelines. ≥5 jurisdictions reference. MODERATE — Tier 3 scoping + multiple jurisdictions. -->

**Applicable Groups:** DEM, MOB, MH, OFS · PAIN
<!-- D2-41: D2-41: garden loop with seating ≤20m serves OFS rest intervals; DEM wandering freedom; PAIN cushioned seating -->

**Description:** Accessible outdoor garden with: secured perimeter (no open exit to unsupervised road); loop path (no dead ends — DEM principle from D-01 applied outdoors); seating every 20 m; hard surface throughout (PTV ≥36 wet). Natural planting within reach of path.

**Specifications:**
Secured perimeter: no unsupervised exit to road or open public area
Loop path: continuous; no dead-ends
Hard surface throughout: PTV ≥36 wet
Seating: every 20 m; 450 mm seat height; armrests; covered option
Planting: within reach of path; non-toxic species (DEM); no thorns
Accessible entry: level or ramp ≤1:20

**Retrofit cost note:** Retrofit penalty: HIGH — STRUCTURAL. Safe accessible garden with loop path and secured perimeter requires new hard landscaping, path construction, perimeter enclosure, planting, and drainage — significant external works in an existing outdoor space. At design stage it is a landscape brief decision. See Part 12 §12.4.2.

**Key evidence (non-English):** Nationalt Videnscenter for Demens / Danish landscape architecture research: empirical data showing that sensory garden loop paths with seating at ≤20 m intervals reduce agitation episodes in dementia care settings. Danish care village research from the 1990s (Midgaard, Fredericia; Dagmarsminde, Frederikssund) established the normalised outdoor environment concept that underpins both D-09 and D-11.

**Key citations:** DSDC. (2022). EADDAT. University of Stirling.

Dignified Design. (2024). 22 design elements for permanent supportive housing. Rick Hansen Foundation. (2024). RHFAC v4.0. RHF.

**Cross-reference:** D-01 (Loop Plan); BIO-01 (Nature Views); BIO-02 (Interior Planting)

**Evidence basis (OT):** EHP Framework (create strategy); Life Balance Model. The safe enclosed garden creates an outdoor environmental context that is otherwise unavailable to DEM, MOB, and MH users in institutional or high-security settings; the Life Balance Model grounds the provision as a participation right — access to outdoor occupation — not an optional amenity.


## CATEGORY E: ENTRY AND CIRCULATION

All entry and circulation provisions address the complete journey from arrival at site boundary to primary occupied space. 'Entry' means the principal entrance — not a secondary 'accessible entrance'.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Garden Provision | Loop Path | Seating Interval | Notes |
|---|---|---|---|---|---|
| US | ADA §228 | Accessible route through gardens | — | — | — |
| UK | BS 8300-1:2018 §10 | Accessible outdoor spaces | — | ≤50m external | — |
| UK | DSDC Stirling | **Dementia garden design** | Loop recommended | Seating throughout | DEM-specific |
| **Guidebook** | **D-11** | **All residential settings** | **Yes** | **≤20m** | **Secured perimeter for DEM** |

UK DSDC Stirling is the primary source for dementia-specific garden design. No code mandates loop paths or secured perimeters.


### E-01 Accessible Lift (1400×1100 mm Car, All Floors Served)
<!-- CON-0116 [HIGH]: E-01 lift ≥1400mm + D-02 cognitive legibility at lift arrival -->
<!-- CON-0136 [HIGH]: E-01 lift + H-01 controls — mobility access convergence -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: CRITICAL -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: HIGH — Lift accessibility: EN 81-70:2021 + multiple Tier 6 standards (ADA, BCA, AS 1428, BS 8300, DIN 18040, TEK17). ≥12 jurisdictions mandate. 1400×1100mm car dimension confirmed by wheelchair anthropometry (Steinfeld 2010, ambiguous PMID but Tier 1 study). HIGH — universally mandated and supported. -->

**Applicable Groups:** MOB, VIS, DEM · OFS · PAIN
<!-- CON-0083: lift eliminates stair exertion — primary OFS/PAIN provision -->

**Description:** Passenger lift serving all occupied floors. Minimum car 1400 mm deep × 1100 mm wide. Door clear width ≥900 mm. Controls: 800--1200 mm AFF; Braille and tactile numerals; audible floor announcements. For bariatric-accessible routes: see .

**Specifications:**

Car: ≥1400 mm deep × 1100 mm wide

Door: ≥900 mm clear width

Door open time: minimum 5 seconds; adjustable 5--15 seconds (temporal accessibility)

Controls: 800--1200 mm AFF; ≥50 mm push-pad; Braille numerals

Audible floor announcements; visual floor display

Floor indicator: visual external to lift on all floors

**Retrofit cost note:** Retrofit penalty: STRUCTURAL. Accessible lift provision requires a lift shaft. In an existing building without a shaft, provision requires a major structural intervention: forming the shaft, structural openings at each floor, and machine configuration. Cost multipliers of 20× versus design-stage provision are well documented. See Part 12 §12.4; Part 11 for DAR shaft provisions.

**Key citations:** Building and Construction Authority. (2025). BCA Code on Accessibility 2025. BCA. British Standards Institution. (2018). BS 8300:2018. BSI. CSA Group. (2023). CSA B651:2023. CSA.

**Cross-reference:** E-02 (Platform Lift); E-06 (Level Entry); [VI-03 — retired code] (Temporal Accessibility); F-08 (Thermal Vestibule — CON-0108: where F-08 thermal vestibule is specified, accessible door specification (E-01) applies to both inner and outer vestibule doors)

**Evidence basis (OT):** Compensatory FOR; Biomechanical FOR. The lift is the primary environmental compensation for vertical mobility

impairment; the 1400×1100mm car dimensions are derived from wheelchair biomechanics ensuring that the compensation is functionally effective.

The 5--15 second adjustable door open time addresses the temporal performance range of users with variable motor speed.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Min Car (W×D mm) | Turning Space | Notes |
|---|---|---|---|---|
| US | ADA 2010 / A117.1-2017 | 1730×1370 | 1702mm (powered) | Largest for powered chairs |
| UK | BS 8300-2:2018 / EN 81-70 | 1100×1400 | 1500mm | Matches guidebook |
| DE | DIN 18040-1 / EN 81-70 | 1100×1400 | 1500mm | DIN aligns with EN |
| AU | AS 1735 / NCC | 1400×1600 | 2070mm (powered) | Largest turning space globally |
| NO | TEK17 / NS 11001 | 1100×1400 | 1500mm | EN 81-70 adopted |
| ISO | ISO 21542:2021 | 1100×1400 | 1524mm | Reference dimension |
| EU | EN 81-70:2021+A1:2022 | 1100×1400 (Type 2) | 1500mm | Harmonised European |
| **Guidebook** | **E-01** | **1400×1100** | **By device type** | **ISO baseline; note AU/US for powered** |

KEY DIVERGENCE: AU 2070mm turning for powered chairs is 36% larger than ISO 1524mm. US A117.1 1702mm is intermediate.


### E-02 Platform Lift (Where Full Passenger Lift Not Achievable)
<!-- design_stage_lock: SD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: MODERATE — Platform lift: ISO 9386-1:2000 + BS 8300 + multiple standards. Acceptable interim where E-01 unachievable. No RCT on platform vs full lift for disability outcomes. Tier 5-6 standards convergence. -->

**Applicable Groups:** MOB · OFS · PAIN
<!-- CON-0012: CON-0012: platform lift reduces exertion on stairs — OFS/PAIN primary benefit alongside MOB -->

**Description:** Where a full passenger lift cannot be provided (listed building, structural constraint): platform lift with car minimum 900×1400 mm; maximum travel 2 m; maximum speed 0.15 m/s; safety enclosure. Not preferred over E-01; see .

**Specifications:**

Car: ≥900×1400 mm (minimum)

Maximum travel: 2 m

Maximum speed: 0.15 m/s

Safety enclosure: required

Usage: retrofit/heritage only where E-01 is not achievable

**Retrofit cost note:** Retrofit penalty: HIGH — STRUCTURAL. Platform lift requires a structural pit or above-floor enclosure, structural fixing, and electrical supply. In a finished building, forming the pit requires opening up the floor structure. At design stage, pit provision is a minor structural item. See Part 12 §12.4.

**Key citations:** British Standards Institution. (2018). BS 8300:2018. BSI. ISO 9386-1:2000. Power-operated lifting platforms. ISO.

**Cross-reference:** E-01 (Passenger Lift)

**Evidence basis (OT):** Compensatory FOR. The platform lift is a compensatory fallback provision where the preferred compensation

(E-01) cannot be delivered; its specifications (900×1400mm minimum, 2m maximum travel) represent the minimum context modification that

constitutes an effective compensation, 

**Jurisdiction comparison:**

| Jurisdiction | Standard | Max Travel | Min Platform | Enclosure | Notes |
|---|---|---|---|---|---|
| US | ADA / ASME A18.1 | Various | 915×1220mm | Per ASME | — |
| UK | BS 6440:2011 | ≤2m (unenclosed) | 1100×1400mm | Required >2m | — |
| EU | EN 81-41:2010 | ≤3m | 900×1400mm | Per EN 81-41 | — |
| DE | DIN 18040-1 | Per EN 81-41 | 1100×1400mm | — | Preferred: full lift |
| AU | AS 1735.14 | Per AS | 1100×1400mm | — | — |
| **Guidebook** | **E-02** | **Per EN 81-41** | **1100×1400mm** | **As code requires** | **Full lift preferred (E-01)** |


### E-03 Ramp Gradient (≤1:20 — MS Fatigue and Temporal Accessibility)
<!-- CON-0009 [HIGH]: Threshold items: zero-step + ≤20mm bevelled max confirmed ≥12 jurisdictions -->
<!-- CON-0156 [HIGH]: E-03 ramp + C-04 contrast + E-09 TWSI + B-04 flicker — circulation safety cluster -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:MOB|OFS|NEU -->
<!-- grade_confidence: MODERATE — Ramp ≤1:20 (5%): DIN 18040 (6% = 1:16.7), TEK17, SIA 500 (max 6%), BS 8300. Koontz et al. 2010 PMID:20434614 (Tier 1) — upper extremity load vs ramp gradient. ≥8 jurisdictions. MODERATE — Tier 1 biomechanical study + standards convergence. -->

**Applicable Groups:** MOB, PAIN, OFS

**Description:** Maximum ramp gradient 1:20 on all accessible routes. 1:12 (code minimum in many jurisdictions) requires 3× the energy expenditure of 1:20 per metre of rise. For MS and CFS/ME users: 1:12 ramps cause metabolic expenditure that can trigger exacerbation.

**Specifications:**

Maximum gradient: 1:20 on all accessible routes

Maximum continuous run without rest platform: 9 m

Rest platform at each 9 m: minimum 1500×1500 mm level

Handrail both sides: continuous; 865--1000 mm AFF; 300 mm horizontal extension each end

Surface: PTV ≥36 wet; non-slip aggregate or profiled surface

**Retrofit cost note:** Retrofit penalty: HIGH — STRUCTURAL. Ramp provision at ≤1:20 requires both horizontal run and vertical rise to be correct. In an existing building with a stepped approach, achieving ≤1:20 requires significant groundworks, structural underpinning at entry thresholds, and drainage modification. Internal ramping in a finished building may be structurally impractical. See Part 12 §12.4.

**Key citations:** Multiple Sclerosis International Federation. (2023). Atlas of MS. MSIF. Koontz, A.M., et al. (2012). Wheelchair propulsion and ramp gradients. [Tier 3.] Waters, R.L., et al. (1985). Energy cost of wheelchair propulsion and shoulder injury risk on grades above 1:12. Arch Phys Med Rehabil 66(7):465–469. [Tier 3.] Kim, J., et al. (2014). Effect of ramp slope on propulsion force and fall risk for manual wheelchair users. J Biomech Eng 136(4). [Tier 3.] Building and Construction Authority. (2025). BCA Code 2025. BCA.

**Cross-reference:** E-01 (Lift); [VI-03 — retired code] (Temporal Accessibility --- fold-down seating at ramp head)

**Evidence basis (OT):** Biomechanical FOR. The 1:20 gradient is the primary Biomechanical FOR-derived specification in this guidebook:

Koontz et al. (2012) demonstrated that reducing gradient from 1:12 (code minimum) to 1:20 decreases shoulder propulsive force by approximately 35%, placing self-propelled ramp ascent within the functional capacity range of manual wheelchair users with reduced upper limb endurance. Waters et al. (1985) established the cumulative injury pathway: repeated propulsion at gradients above 1:12 generates shoulder loading that accumulates as rotator cuff pathology over years of daily ramp use. Ramp gradient is therefore a PAIN prevention specification as well as a fatigue management specification — inadequate gradient is a mechanism by which the built environment creates chronic shoulder PAIN as a secondary condition in manual wheelchair users (CON-0093).

**Jurisdiction comparison:**

| Jurisdiction | Standard | Max Gradient | Notes |
|---|---|---|---|
| US | ADA 2010 §405 | 1:12 (8.3%) | Code minimum; rise ≤760mm per run |
| UK | BS 8300-1:2018 §9 | 1:12 max; 1:20 preferred | Best practice aligns with guidebook |
| DE | DIN 18040-1 §4.3.8 | 1:16.7 (6%) | Stricter than US/UK |
| AU | AS 1428.1:2021 §10; NCC | 1:14 (7.1%) | Between US and DE |
| NO | TEK17 §12-18 | 1:20 outdoor; 1:12 short indoor | Most restrictive outdoor |
| FR | Arrêté 2017 | 5% preferred; 8% max short | Aligns with DE |
| CH | SIA 500 | 6% max | Same as DE |
| ISO | ISO 21542:2021 §10 | 1:20 preferred; 1:12 max | Matches guidebook best practice |
| **Guidebook** | **E-03** | **1:20 (5%)** | **Aligns with NO/ISO preferred; DE/FR range** |


### E-04 Accessible Parking (3600 mm Width, Covered, Closest to Entry)
<!-- design_stage_lock: SD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: LOW — Accessible parking 3600mm width: BS 8300, ADA, AS 1428, BCA SG. No RCT on parking bay width for disability outcomes. Tier 5-6 standards only. -->

**Applicable Groups:** MOB, VIS, PAIN, OFS · DEM
<!-- CON-0084: covered parking close to entry reduces wayfinding load for DEM -->

**Description:** Accessible parking bays: 3600 mm width (standard accessible) minimum; 4500 mm width. Located closest to accessible entry. Covered where possible. Surface: level (≤1:50 cross-fall); PTV ≥36 wet. Marked: International Symbol of Access + Braille equivalent tactile indicator at bay boundary.

**Specifications:**

Standard accessible bay: 3600 mm width



Location: closest accessible bay to entry; ≤50 m to entry

Surface: ≤1:50 cross-fall; PTV ≥36 wet

Cover: weather protection preferred

Quantity: minimum 5% of total parking, or per local code where greater

**Retrofit cost note:** Retrofit penalty: MODERATE -- HIGH. Covered accessible parking at 3600 mm width requires planning and layout decisions at design stage. Retrofit may require resurfacing, line-marking, canopy installation, drainage, and legal agreement. See Part 12 §12.4.2.

**Key citations:** British Standards Institution. (2018). BS

8300:2018. BSI. Building and Construction Authority. (2025). BCA Code

2025. BCA. CSA Group. (2023). CSA B651:2023. CSA.

**Cross-reference:** E-06 (Level Entry route from parking);

Parking)

**Evidence basis (OT):** PEOP Model; Life Balance Model. Accessible parking directly addresses the person-environment transaction at the

point of building approach; inadequate parking or excessive distance forces exertion expenditure before the primary occupation begins. The

≤50m distance specification reflects the exertion budget for OFS users.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Space Width | Aisle Width | Total Width | Covered | Proximity |
|---|---|---|---|---|---|---|
| US | ADA 2010 §502 | 2440mm | 1524mm | 3964mm | Not required | Closest route |
| UK | BS 8300-1:2018 §5 | 2400mm | 1200mm shared | 3600mm | Not required | ≤50m from entrance |
| DE | DIN 18040-1 §4.1 | 3500mm (total) | — | 3500mm | Not required | Near entrance |
| AU | AS 2890.6 / NCC | 2400mm | Shared access | 3200mm min | Not required | — |
| **Guidebook** | **E-04** | **3600mm total** | **Integrated** | **3600mm** | **Covered** | **Closest to entry** |


### E-05 Weather Protection at Entry (Covered Canopy Minimum 3000×2000 mm)
<!-- design_stage_lock: SD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:OFS -->
<!-- grade_confidence: LOW — Weather protection 3000×2000mm canopy: BS 8300 + expert consensus. No RCT. OFS rationale (thermal triggers) is Tier 2-3 clinical but no built-env study. -->

**Applicable Groups:** MOB, PAIN, OFS, VIS · DEM · DBL
<!-- CON-0085: covered canopy provides wayfinding landmark and sensory orientation point -->

**Specifications:**

Canopy depth: ≥3000 mm; width: ≥2000 mm

Gradient: ≤1:50 beneath canopy

Drainage: to perimeter (no central drain creating trip hazard)

Canopy height: ≥2500 mm

Lighting: ≥100 lux at entry surface level; night-activated

**Retrofit cost note:** Retrofit penalty: MODERATE. Weather protection canopy installation requires structural fixing to the building fabric. In a finished building, canopy fixing requires structural assessment and making-good. At design stage, the canopy is a simple structural specification. See Part 12 §12.4.2.

**Key citations:** British Standards Institution. (2018). BS 8300:2018. BSI. CAN/ASC 2.8:2025. Accessible-Ready Housing. ASC.

**Cross-reference:** E-06 (Level Entry)

**Evidence basis (OT):** Compensatory FOR; Life Balance Model. The canopy compensates for the environmental condition (rain, sun, wind) that disproportionately elevates the physical and thermoregulatory cost of entry for MOB, PAIN, and OFS users; the 3000mm depth specification ensures sufficient shelter to pause and manage equipment.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Canopy Required | Min Size | Notes |
|---|---|---|---|---|
| US | ADA | Not required | — | — |
| UK | BS 8300-1:2018 §8 | Covered approach recommended | — | — |
| DE | DIN 18040-1 | Weather protection at entry | 1500×1500mm | Movement area protected |
| NO | TEK17 | Weather protection | — | Climate-driven |
| **Guidebook** | **E-05** | **Yes** | **3000×2000mm** | **Wheelchair transfer + companion** |

Guidebook specifies significantly larger canopy (3000×2000mm) than any code to accommodate wheelchair transfer with weather protection.


### E-06 Level Entry (Zero Step at All Accessible Entrances)
<!-- CON-0009 [HIGH]: Threshold items: zero-step + ≤20mm bevelled max confirmed ≥12 jurisdictions -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: CRITICAL -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: HIGH — Zero step at accessible entrances: ADA, DIN 18040, TEK17, BS 8300, NCC 2022, BCA SG, NBR 9050, NZS 4121, AS 1428 — universally mandated (≥12 jurisdictions). Al Lawati 2017 (Tier 3, n=214): 2cm defeats 45.8% WC users on first attempt. Keall 2015 PMID:25255696 (Tier 1 RCT Lancet): home modifications reduce falls. HIGH — cross-jurisdictional mandate + Tier 1 RCT evidence. -->

<!-- CON-0056 [HIGH]: Zero-threshold (13-15 mm max) specified for MOB caster wheels also serves OFS (step-elimination prevents PEM) and PAIN (reduces joint loading). Add OFS, PAIN to Applicable Groups. -->
**Applicable Groups:** MOB, VIS, DEM, OFS · DEAF · DBL · NDV/MH · PAIN
<!-- CON-0009: Zero threshold eliminates exertion barrier and PAIN vibration trigger at each entry -->
<!-- CON-0007: CON-0007: Universal Mode companion-width at entries: primary routes ≥1500mm clear. Level entry + wide path = universal. -->

**Description:** Zero step (≤4 mm threshold) at all accessible entrances. Where site topography requires raised threshold: ramped approach ≤1:20 (E-03). No stepped entry at any accessible entrance.

Single level entry flush with finish floor level.

**Specifications:**

Threshold: ≤4 mm at accessible entry (preferred); ≤10 mm permitted where drainage constraints make zero threshold impractical (DIN 18040-2 reduced-barrier variant — imperceptible to most wheelchair users in daily use per Bundesfachstelle Barrierefreiheit, 2022)

Ramped approach where required: ≤1:20 (E-03)

Door mat: flush with floor level; recessed mat well preferred

Level surface maintained for 1500 × 1500 mm clear inside entry

DAR: all new residential — design for future level approach even if not constructed initially (CAN/ASC 2.8:2025)

**Retrofit cost note:** Retrofit penalty: HIGH — STRUCTURAL. Level entry (zero step) is a site-level and threshold decision. Retrofit of a stepped entry requires ramp construction, threshold lowering, drainage provision, and potentially structural work at the door opening. Threshold lowering in masonry construction requires structural assessment. See Part 12 §12.4.

**Key citations:** CSA Group. (2023). CSA B651:2023. CSA. Standard Norge. (2018). NS 11001-1:2018 [Norwegian\]. Standard Norge. CAN/ASC 2.8:2025. ASC. Wellecke, C., et al. (2022). Occupational therapists' perspectives on priority features of accessible housing. Australian Occupational Therapy Journal 69(4):459–470. [Tier 1, n=144 Australian OTs.] Finding: step-free external access, zero-threshold shower, and ground-floor bedroom/bathroom are the three highest-priority features specified by OTs — confirming the visitability hierarchy (CON-0097).

**Cross-reference:** E-03 (Ramp Gradient); E-05 (Canopy); E-07 (Slip Resistance)

**Evidence basis (OT):** EHP Framework (alter strategy). Level entry is the canonical 'alter' intervention: the environmental context is

changed (threshold eliminated) to directly expand the performance range, enabling the occupation of independent building entry for any

user whose mobility impairment or energy limitation makes threshold negotiation a barrier.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Max Threshold | Notes |
|---|---|---|---|
| US | ADA 2010 §404.2.5 | ≤13mm | Beveled if >6mm |
| UK | AD M Vol 1 | Level preferred | M4(2) level threshold |
| DE | DIN 18040-2 §4.3.3 | ≤20mm | Draft revision: ≤10mm |
| AU | AS 1428.1:2021 | **≤5mm** | Strictest globally |
| NO | TEK17 §12-4 | Step-free mandatory | For qualifying dwellings |
| FR | Arrêté 2014 | ≤20mm | Same as current DE |
| ISO | ISO 21542:2021 §14 | Level preferred | Aligns with guidebook |
| **Guidebook** | **E-06** | **≤5mm** | **AU standard — weather-sealed level detail** |


### E-07 Slip Resistance (PTV ≥36 Wet Throughout All Circulation and Entry)
<!-- CON-0009 [HIGH]: Threshold items: zero-step + ≤20mm bevelled max confirmed ≥12 jurisdictions -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: MODERATE — PTV ≥36 wet: HSE guidance + BS 8300. Slip resistance science is Tier 3-4 (HSL studies). No RCT on PTV threshold for disability-specific fall outcomes. ≥8 jurisdictions reference anti-slip requirements. -->

**Applicable Groups:** MOB, DEM, VIS (fall prevention) · PAIN · OFS · NEU
<!-- CON-0086: fall prevention applies equally to NEU/DEM alongside MOB/PAIN -->
<!-- D2-41: D2-41: fall fear and instability are pain/fatigue amplifiers; slip resistance reduces exertion effort -->

**Description:** All floor surfaces on accessible routes achieve PTV (Pendulum Test Value) ≥36 in wet condition. External approaches, entry vestibules, bathrooms, and kitchens: PTV ≥36 wet (HSE guidance).

Dry-only internal circulation: PTV ≥36 dry.

**Specifications:**

PTV ≥36 wet: external approaches, entry vestibules, bathrooms, kitchens, ramps (temperate climates)

PTV ≥40 wet: all wet surfaces in high-rainfall, tropical, or monsoon climates; all bathroom and shower surfaces regardless of climate (JIS T 9251; Tier 4 — governs over HSE Tier 5 ≥36 value)

PTV ≥36 dry: all internal circulation

Test: BS 7976-2 pendulum test

Maintenance: cleaning regime must not reduce PTV below threshold; specify in cleaning contract

Post-occupancy: re-test at 12 months if floor condition changes

**Retrofit cost note:** Retrofit penalty: LOW. Slip resistance PTV ≥36 wet is a floor finish specification. Retrofit is floor covering

replacement or surface treatment application. Anti-slip coating can be applied to existing surfaces at modest cost. See Part 12 §12.4.1.

**Key citations:** HSE. (2014). Slips and trips: Guidance for the catering industry. [PTV ≥36 reference.\] British Standards Institution. (2018). BS 8300:2018. BSI.

**Cross-reference:** B-08 (Matte Floor — gloss and PTV compatibility); G-04 (Wet Room); E-06 (Level Entry)

**Evidence basis (OT):** Biomechanical FOR. PTV ≥36 wet is derived from biomechanical research on the coefficient of friction required to

prevent slip initiation under ambulant and mobility-device loads on wet surfaces; below PTV 36 wet, the risk of slip-initiated fall

exceeds clinically acceptable thresholds for populations with reduced balance and reaction time.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Test Method | Wet Threshold | Ramp Threshold | Notes |
|---|---|---|---|---|---|
| US | ADA / ASTM | DCOF (ANSI A326.3) | ≥0.42 DCOF | — | Dynamic Coefficient of Friction |
| UK | BS 7976-2 / HSE | Pendulum PTV | **PTV ≥36 wet** | PTV ≥36+ for ramps | Most prescriptive; PTV is reference |
| AU | AS 4586:2013 | Pendulum + Ramp | P3-P5 (wet pendulum) | R9-R13 (ramp) | Dual-method system |
| DE | DIN 51130 | Ramp test (R-value) | — | R9-R13 by application | R-value system |
| ISO | ISO 10545-17 | Referenced | — | — | Ceramic tiles specific |
| **Guidebook** | **E-07** | **Pendulum PTV** | **PTV ≥36 wet** | **PTV ≥36** | **UK methodology** |

**HIGH DIVERGENCE:** Test methods differ fundamentally — US uses DCOF (friction coefficient), UK uses PTV (pendulum), DE uses R-value (ramp angle), AU uses both. Values are NOT directly comparable across methods.


### E-08 Corridor Clear Width (≥1200 mm Minimum on All Primary Routes)
<!-- CON-0157 [HIGH]: B-10 visual alarm + H-03 captioning + D-08 signage + E-08 corridor — public building cluster -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:MOB -->
<!-- grade_confidence: MODERATE — Corridor ≥1200mm: BS 8300, ADA, DIN 18040, TEK17, NCC 2022, NBR 9050, AS 1428. Koontz 2010 PMID:20434614 (Tier 1): corridor width affects propulsion biomechanics. ≥10 jurisdictions confirm 1200mm minimum. MODERATE — Tier 1 biomechanical + strong standards convergence. -->

<!-- CON-0007 [HIGH]: Create Universal Mode companion-width specification. Primary routes ≥1500 mm clear (best practice); ≥2440 mm where DEAF is primary population (DeafSpace signed-conversation standard, Co-1 ASL-derived). Resolves siloed MOB/DEAF specifications into unified tier-ladder: 1200 mm minimum / 1500 mm best practice / 2440 mm DEAF-primary. --> (≥1200 mm Minimum on All Primary Routes)

**Applicable Groups:** MOB, VIS, DEM · DEAF · DBL
<!-- CON-0061: CON-0061: ≥1500 mm is multi-population (DEAF signing pairs, VIS cane sweep, DBL intervenor, DEM wandering freedom, MOB turning). Best practice 1800 mm on all primary routes. -->

**Description:** All primary accessible routes: 1200 mm clear width minimum (code minimum 1000 mm in most jurisdictions — E-08 exceeds code). Where 1200 mm continuous not achievable: passing bay ≥1500×1500 mm at maximum 10 m intervals. routes: 1500 mm clear width ().

**Specifications:**

Primary routes: 1200 mm clear width minimum 

Where <1200 mm continuous: passing bay ≥1500×1500 mm at ≤10 m intervals

No furniture, equipment, or signage projecting into corridor

Skirting/kickplate at 200--300 mm AFF on wheelchair routes (impact protection)

**Retrofit cost note:** Retrofit penalty: HIGH — STRUCTURAL. Corridor clear width of 1200 mm minimum is a plan dimension. In an existing building with narrower corridors, achieving 1200 mm requires partition removal — structural in many cases — or the corridor cannot comply. This is among the most expensive accessibility retrofits; where structural walls form the corridor, compliance may be impossible without major reconstruction. See Part 12 §12.4.

**Key citations:** British Standards Institution. (2018). BS 8300:2018. BSI. Koontz, A.M., et al. (2012). Wheelchair propulsion. [Tier 3.\]

**Cross-reference:** E-01 (Lift Car Width)

**Evidence basis (OT):** Biomechanical FOR. The 1200mm clear width (exceeding 1000mm code minimum) is grounded in wheelchair propulsion

biomechanics: corridors narrower than 1200mm force compensatory manoeuvres that increase shoulder joint loading and reduce propulsion

efficiency, directly restricting the performance range of manual wheelchair users.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Min Width | Passing Width | Notes |
|---|---|---|---|---|
| US | ADA 2010 §403 | 915mm | 1524mm | Narrowest minimum |
| UK | BS 8300-2:2018 §7 | 1200mm | 1800mm | Guidebook aligns |
| DE | DIN 18040-1 §4.3 | 1500mm | 1800mm | Widest minimum |
| AU | AS 1428.1:2021 §7 | 1000mm | 1800mm | Between US and UK |
| NO | TEK17 §12-6 | 1500mm | — | Same as DE |
| ISO | ISO 21542:2021 | 1200mm | 1800mm | Matches UK/guidebook |
| **Guidebook** | **E-08** | **≥1200mm** | **≥1800mm** | **UK/ISO standard** |


### E-09 Tactile Walking Surface Indicators (ISO 23599:2019)
<!-- CON-0156 [HIGH]: E-03 ramp + C-04 contrast + E-09 TWSI + B-04 flicker — circulation safety cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:VIS|DBL -->
<!-- grade_confidence: MODERATE — ISO 23599:2019 TWSI: derived from JIS T 9251 (Japan — extensive field deployment since 1967). Multiple jurisdictions adopt. No RCT on TWSI efficacy vs no TWSI for VIS outcomes (would be unethical). Standards + established practice evidence. -->

**Applicable Groups:** VIS, DBL, NEU, DEM, PAIN

**Description:** TWSI (Tactile Walking Surface Indicators) installed at all hazard points and on primary accessible routes for VIS users. At stair heads and platform edges, domed TWSI serve as a hazard-warning surface for all populations with elevated stair descent fall risk — not only VIS/DBL navigation users.

Domed (warning) profiles at hazards; bar (directional) profiles for guidance routes. Per ISO 23599:2019.

**Specifications:**

Domed profile: at stair heads, platform edges, road crossings, escalator heads

**Stair descent fall risk (CON-0094):** Domed TWSI at stair heads also serves NEU, DEM, and PAIN populations — stair descent fall risk is 3× ascent risk (Simoneau et al. 1991, Tier 3). Each 6 mm of riser irregularity increases misstep probability by ~18% (Templer 1992, Tier 4). Domed TWSI at stair head provides a tactile hazard cue that reduces misstep risk for all populations with proprioceptive, cognitive, or pain-related vulnerability to stair descent. Handrail specification (G-05) applies at all staired routes where NEU/DEM/PAIN are primary populations.

Bar profile: directional guidance on primary accessible routes only

Colour: maximum tonal contrast with adjacent surface; minimum 30 LRV

Profile height: 5 mm ±1 mm (ISO 23599:2019)

Material: durable, slip-resistant; confirmed for climate zone

DEM environments: domed TWSI maximum 3 mm profile; same-colour as adjacent floor (B.4.6 conflict resolution)

**Retrofit cost note:** Retrofit penalty: LOW. Tactile walking surface indicators are surface-applied or recessed tiles. Retrofit is a floor

works operation — tile removal, TWSI installation, and reinstatement. No structural implications. See Part 12 §12.4.1.

**Key citations:** ISO. (2019). ISO 23599:2019 — Assistive products — Tactile walking surface indicators. ISO. CNIB Foundation. (2024). Clearing our path. CNIB. Japan Blind People's Association. (2022). [Japanese.] JBPA. Simoneau, G.G., et al. (1991). Etiology of age-related gait changes and stair descent falls. J Appl Physiol 70(3):1290–1295. [Tier 3.] Templer, J. (1992). The staircase: studies of hazards, falls and safer design. MIT Press. [Tier 4.]

**DBL evidence note:** [THIN BASE — Tier 2+4 only; no Tier 1 OT clinical research on DeafBlind built environments in any jurisdiction; March 2026]

**Cross-reference:** Part 5 §5.2 (COLOUR-CONT conflict — TWSI vs DEM: resolved; see resolution entry); CON-0094 (stair descent multi-population fall risk)

**Evidence basis (OT):** Compensatory FOR. TWSI are environmental compensation devices that substitute tactile (proprioceptive/plantar) information for absent visual information during navigation; the ISO 23599:2019 profile specifications are derived from the sensory detection thresholds required for the compensation to be reliably perceptible under normal ambulant conditions.
**Specifications:**

Canopy depth: ≥3000 mm; width: ≥2000 mm

Gradient: ≤1:50 beneath canopy

Drainage: to perimeter (no central drain creating trip hazard)

Canopy height: ≥2500 mm

Lighting: ≥100 lux at entry surface level; night-activated

**Retrofit cost note:** Retrofit penalty: MODERATE. Weather protection canopy installation requires structural fixing to the building fabric. In a finished building, canopy fixing requires structural assessment and making-good. At design stage, the canopy is a simple structural specification. See Part 12 §12.4.2.

**Key citations:** British Standards Institution. (2018). BS 8300:2018. BSI. CAN/ASC 2.8:2025. Accessible-Ready Housing. ASC.

**Cross-reference:** E-06 (Level Entry)

**Evidence basis (OT):** Compensatory FOR; Life Balance Model. The canopy compensates for the environmental condition (rain, sun, wind) that disproportionately elevates the physical and thermoregulatory cost of entry for MOB, PAIN, and OFS users; the 3000mm depth specification ensures sufficient shelter to pause and manage equipment.

**Jurisdiction comparison:**

| Jurisdiction | Standard | System | Notes |
|---|---|---|---|
| JP | JIS T 9251 | Originated TWSIs (1965) | Most extensive deployment |
| ISO | ISO 23599:2019 | International harmonisation | Reference standard |
| DE | DIN 32984:2020 | Most comprehensive system | Detailed indicator types |
| AU | AS 1428.4.1:2009 | Comprehensive TWSI | Widely deployed |
| UK | BS 8300 + DfT guidance | Tactile paving | Colour differentiation |
| US | ADA §705 | Detectable warnings only | Limited to specific locations |
| **Guidebook** | **E-09** | **ISO 23599:2019** | **International reference** |


### E-10 Rest Seating on Circulation Routes (≤20m Interval)
<!-- design_stage_lock: SD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:OFS|MOB|PAIN -->
<!-- grade_confidence: LOW — Rest seating interval 25m: Roxburgh et al. 2024 (BJ Occup Ther, Tier 1) — OT home modification for ME/CFS. OFS clinical pacing guidance (CDC, IOM/NAM Tier 1 clinical). BS 8300: 100m general. No built-env RCT on seating interval vs OFS outcomes. LOW — clinical rationale strong but no architectural study. -->

<!-- DUPLICATE RESOLVED 2026-04-19 (A4). This entry superseded by the revised E-10 specification below (L3205+). Canonical specification: see E-10 at end of Category E section. The 20 m interval in this entry has been revised to 25 m per Tier 1 evidence (Roxburgh et al. 2024); alcove geometry and OFS seat height added. Do not use this entry for specification writing. -->

*[See E-10 canonical specification below — resolved per workplan Block 3 A4 2026-04-19]*
**Jurisdiction comparison:**

| Jurisdiction | Standard | Max Interval | Seat Height | Armrests | Notes |
|---|---|---|---|---|---|
| US | ADA 2010 | Not specified (no interval) | — | — | Significant gap |
| UK | BS 8300-1:2018 §10 | ≤50m (external) | 450-475mm | Both sides recommended | — |
| DE | DIN 18040-1 | — | — | — | — |
| AU | AS 1428.2 | Referenced | — | — | — |
| NO | TEK17 | — | — | — | — |
| ISO | ISO 21542:2021 §12 | Referenced | — | — | — |
| **Guidebook** | **E-10** | **≤20m** | **450mm** | **Both sides** | **2.5× stricter than UK** |

**HIGH DIVERGENCE:** US ADA has NO rest seating interval requirement. UK BS 8300 specifies ≤50m. Guidebook specifies ≤20m based on OFS/PAIN fatigue data — 2.5× stricter than UK, infinitely stricter than US.


### E-11 Automatic Sliding Entry and Internal Doors
<!-- design_stage_lock: SD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:MOB|OFS -->
<!-- grade_confidence: MODERATE — Automatic sliding doors: BS 8300, DIN 18040, ADA, TEK17, multiple jurisdictions. No RCT but engineering standard + disability population surveys confirm door force as primary barrier. ≥8 jurisdictions. -->

**Applicable Groups:** MOB, UPL, OFS · PAIN
<!-- D2-41: D2-41: zero door force eliminates push/pull effort — OFS PEM prevention -->

**Description:** Automatic sliding or swing doors (not heavy manually-operated) on all primary accessible routes. Maximum opening force: 20 N (AU AS 1428.1:2021; NO TEK17 — best practice; ISO 21542 specifies 22 N but AU/NO Tier 5 governs as more inclusive). Door hold-open time: adjustable 5--15 seconds from accessible control.

**Specifications:**
Automatic operation on all primary route doors
Maximum opening force: 20 N (manual operation if automatic not installed)
Hold-open time: adjustable 5--15 seconds (temporal accessibility)
Slow-open profile: 0--100% over 2--3 seconds (not <1 second — Part 8 §8.4.8)
Presence detection: both sides of door

**Retrofit cost note:** Retrofit penalty: MODERATE. Automatic sliding door installation requires door leaf replacement, overhead track/motor

installation, and sensor provision. In a finished building, the door opening is typically already present; the retrofit is primarily

mechanical and electrical. See Part 12 §12.4.2.

**Key citations:** ISO. (2021). ISO 21542:2021. ISO. British Standards

Institution. (2018). BS 8300:2018. BSI.

**Cross-reference:** E-06 (Level Entry); H-01 (Controls)

**Evidence basis (OT):** EHP Framework (adapt strategy); Compensatory FOR. Automatic doors adapt the entry context to eliminate the manual force and coordination demands of door operation; for MOB, UPL, and OFS users the elimination of door-opening force is both a direct compensation (no action required) and a performance range expansion (users who cannot open manual doors can now enter independently).

**Coverage gap note (v9.0):** Visual intercom and visual doorbell provisions for DEAF users are not yet fully specified in this category. NDV users require predictable, low-stimulus entry sequences; this is partially addressed in F-01 (sensory gradient) and D-01 (wayfinding). Full specifications deferred to v9.0.


---

**Jurisdiction comparison:**

| Jurisdiction | Standard | Opening Force (manual) | Automatic Door Trigger | Notes |
|---|---|---|---|---|
| US | ADA 2010 §404.2.9 | ≤22N (interior); ≤38N (exterior) | Proximity sensor or push plate | — |
| UK | BS 8300-2:2018 §8 | ≤30N (BS); ≤20N (best practice) | Automatic preferred at main entry | — |
| AU | AS 1428.1:2021 §13 | **≤20N** | Automatic preferred | Strictest force |
| DE | DIN 18040-1 §4.3.3 | Not specified in DIN | — | ASR A1.7 for workplaces |
| NO | TEK17 §12-15 | — | — | — |
| ISO | ISO 21542:2021 §14.5 | ≤25N preferred | — | — |
| **Guidebook** | **E-11** | **≤20N** | **Automatic sliding at main entry** | **AU standard** |


### E-15 Changing Places Facility (Height-Adjustable Bench, Overhead Hoist, Peninsular WC)
<!-- design_stage_lock: B -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:MOB -->
<!-- grade_confidence: MODERATE — Changing Places: Changing Places Consortium UK evidence (Tier 2 Co-1). MHCLG mandate in England (Tier 6). BCA SG 2025 adopts. No RCT. ≥5 jurisdictions now mandate. MODERATE — strong advocacy evidence + increasing mandates. -->

**Applicable Groups:** MOB, DEM/NDV[IntD proxy], NEU
**Typology:** Non-Residential (public, institutional, transport hubs, entertainment venues, retail ≥1000 m²); Residential (supported living, residential care)
**Design Stage:** SD — spatial footprint and hoist track structure are irreversible after slab pour

#### Specification

● Minimum net floor area: 12 m² (Changing Places Consortium standard); preferred 15 m² where hoist track extends to all four transfer positions

● Ceiling height: ≥2700 mm throughout the full hoist track area to accommodate overhead mobile hoist travel with occupant in sling

● Height-adjustable changing bench: 1800 × 800 mm clear surface; height-adjustable 450–1000 mm; rated ≥250 kg; wall-mounted fold-flat or fixed (depending on hoist track configuration); anti-slip surface; wipe-clean material

● Overhead hoist and ceiling track: continuous H-track (or XY gantry) covering bench, WC transfer position, and door entry/exit arc; minimum rated load 250 kg; commissioning load test before occupation; SE coordination required for ceiling reinforcement (see §8.5)

● Peninsular WC: minimum 600 mm clear on each side; 700 mm preferred; WC height 450–500 mm; bilateral grab bars (G-03)

● Clear floor zone at bench: minimum 2200 × 1400 mm manoeuvring zone adjacent to bench; must be outside hoist track footprint when hoist is parked

● Carer circulation: ≥900 mm clear circulation route encircling all three positions (bench + WC + door); two carers must circulate simultaneously without crossing

● Wash basin: lever-operated; height 750–850 mm; knee clearance per I-02; accessible from hoist-user position without docking/undocking hoist

● Slip-resistant floor: PTV ≥36 wet (consistent with E-07 throughout); non-porous surface for clinical hygiene

● Alarm: emergency pull cord (H-05) at floor level (accessible to fallen occupant) and standard height; vibrotactile alert integration (K-04) where DBL occupants

● Location: within the accessible travel circuit; not routed through a gendered-access facility; not requiring lift access where level-access alternative exists

#### Evidence basis

The Changing Places Consortium (UK, 2006–present; now BS 8300:2018 Annex G) estimates 250,000+ people in the UK require a Changing Places facility rather than a standard accessible WC — they cannot use a standard accessible WC unassisted or safely. The specifications above derive from BS 8300:2018 Annex G (Tier 5), the Changing Places Consortium Technical Brief (Tier 5), and the Motability Foundation (2023) audit of Changing Places facilities post-installation. No Tier 1 OT clinical RCTs on Changing Places facility dimensions exist; specifications are consensus-derived from OT assessment practice and user-led advocacy evidence.

**Evidence markers:** ● BS 8300:2018 Annex G (Tier 5 — national standard); ◐ Changing Places Consortium Technical Brief (Tier 5 — industry consensus); ○ dimensional specifications beyond minimum standard (expert consensus from OT assessment practice).

#### Key citations

British Standards Institution. (2018). BS 8300:2018 — Design of an accessible and inclusive built environment: Buildings — Code of practice. BSI. Changing Places Consortium. (2024). Changing Places — Technical standards. Changing Places Consortium. Motability Foundation. (2023). Changing Places: Audit of installations 2022–2023. Motability Foundation.

#### Retrofit note

**Retrofit: VERY HIGH penalty.** Changing Places requires 12 m² of dedicated floor area with ceiling hoist reinforcement. In existing buildings, retrofitting requires either identifying and repurposing 12 m² of accessible ground-floor space with structural ceiling capacity, or major alteration. Cost multiplier: ×20–50 relative to new-build provision. Structural engineer review mandatory for ceiling track installation in existing buildings.

#### Cross-references

G-03 (Grab Bars — bilateral at peninsular WC); G-04 (Wet Room Configuration — floor gradient and drainage apply); H-05 (Nurse Call/Emergency Pull Cord — floor-level cord required); K-04 (Vibrotactile Alert — where DBL occupants); §8.5 (Structural Engineer — ceiling hoist track)

---


## CATEGORY F: SENSORY ZONING

Sensory zoning is the deliberate organisation of a building's sensory environment so that stimulation level varies predictably, decreasing from public/entry zones to primary occupied/private zones.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Mandatory | Key Features |
|---|---|---|---|
| UK | BS 8300-2:2018 / Building Regs 2021 | **YES** (since Sept 2021) | Height-adjustable bench, ceiling hoist, peninsular WC, ≥12m² |
| AU | NCC / AS 1428.1 | Partial | "Accessible adult change facility" in some building classes |
| US | ADA / A117.1-2017 | Adult changing stations (Supplement 1) | Added 2024 IBC; not yet universal |
| DE | DIN 18040-1 | Not mandated | "Toilette für alle" voluntary initiative |
| ISO | ISO 21542:2021 | Referenced | Not mandated |
| **Guidebook** | **E-15** | **Recommended** | **UK BS 8300-2 specification** |

UK is the ONLY jurisdiction where Changing Places are mandatory (since September 2021 via Building Regulations amendment).

<!-- CON-0102 APPLIED 2026-05-04: F-category coherence note -->
**F-Category Interdependence Note:** F-04 (Air Quality), F-06 (Fragrance-Free Policy), F-07 (Thermal Zoning), and F-08 (Thermal Transition) are interdependent specifications governing the same building system. For OFS/MCAS populations, HVAC design must simultaneously satisfy: MERV 13+ filtration with no recirculated air without HEPA (F-04); zero fragrance diffusers including HVAC-integrated systems (F-06); individual supplemental radiant heating that does not recirculate air (F-07); and thermal vestibule air handling coordinated with both F-06 fragrance-free and F-04 filtration requirements (F-08). These four items must be specified as a coordinated HVAC system, not independently. Failure to coordinate produces intra-individual co-triggering: the same OFS/MCAS user experiences thermal and chemical triggers from the same air handling system. Citation mining 2026-05-04 confirmed: Steinemann 2019 (AQV-10) documents MCS-autism co-prevalence at ~3x general population, reinforcing the OFS/NDV overlap that makes F-category coordination critical.


### F-01 Sensory Gradient (High to Low Stimulation from Entry to Occupation)
<!-- CON-0040 [HIGH]: Unified sensory environment system: Dunn profiles → spatial zones → quantified parameters -->
<!-- CON-0043 [HIGH]: LRV ≥50% best practice; ≥65% Michelson at critical junctions; 30% = code minimum only -->
<!-- CON-0046 [HIGH]: NHS CAMHS: sensory refuge mandatory (not optional) where NDV/AUT + NDV/MH co-occurrence foreseeable -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:NDV|DEM|NEU|OFS|NDV/MH -->
<!-- grade_confidence: LOW — Sensory gradient high-to-low: Kaplan & Kaplan 1989 (attention restoration theory, Tier 3). PAS 6463 (Tier 4) + detectable-gradient-protocol BPC. No RCT on sensory gradient spatial design for NDV outcomes. Tier 3-4. -->

<!-- CON-0046 [HIGH]: Sensory gradient critical for NDV/AUT in MH inpatient settings — CS-17 documents MH ward sensory environments as actively harmful to AUT co-occupants. -->
**Applicable Groups:** NDV, PCS, AUT, MH, DEM, OFS

**Description:** The complete building journey from arrival to primary occupied space is organised so that sensory load decreases progressively. Entry/reception: highest acceptable load. Transition zones: intermediate. Primary occupied spaces: lowest load. No abrupt step-change in either direction.

**Specifications:**

Entry zone: NC 35; muted palette (NCS chroma ≤6); 300--500 lux

Transition: NC 30; NCS chroma ≤4; 200--300 lux

Primary occupied spaces: NC 25; NCS chroma ≤3; 100--200 lux

No single transition >NC-10 acoustic change

Restorative element at each transition (BIO-01, BIO-02)

**Retrofit cost note:** Retrofit penalty: LOW — PLANNING. Sensory gradient from entry to occupation is a room arrangement and

material-specification decision at zero additional cost at design stage. Retrofit requires redecoration, material replacement, and

possibly layout modification. See Part 12 §12.4.1.

**Key citations:** Kaplan, R., \& Kaplan, S. (1989). The experience of nature. Cambridge University Press. British Standards Institution.

(2022). PAS 6463:2022. BSI. AtkinsRéalis. (2024). Neuroinclusive office design v3.

**Cross-reference:** A-04 (Acoustic Zoning); B-05 (Lighting Transitions)

**Evidence basis (OT):** EHP Framework (alter strategy); Dunn's Sensory Processing Model. Sensory gradient from high-stimulation entry to low-stimulation primary occupied space alters the context progressively to keep cumulative sensory load within the processing capacity of sensory-sensitive users; abrupt transitions from high-load to low-load zones constitute shock stimuli that are themselves a trigger.

---

#### Unified Sensory Environment Specification Matrix (CON-0040)

*This matrix links Dunn's Sensory Processing Model profiles to spatial zones and quantified design parameters. It provides the cross-category coordination framework for Category A (Acoustics), B (Lighting), C (Colour/Surface), and F (Environmental Quality) specifications. Source: CON-0040; sensory-processing-model-design-application BPC (Opus synthesis); sensory-relief-space-design BPC (Opus synthesis).*

**Applicable Groups:** NDV/AUT · NDV/ADHD · NDV/SENS · DEM · OFS · PAIN · NEU/PCS · ALL

| Dunn Profile | Spatial Zone | Acoustic | Illuminance | CCT | Colour | Notes |
|---|---|---|---|---|---|---|
| **Sensory avoiding** | Zone 3 — sensory retreat (A-16, F-01) | RT60 ≤0.3 s; NC-25; no masking (A-13) | 0–50 lux (user-controlled); full blackout available | ≤2700 K warm amber | NCS chroma ≤2; no high-contrast pattern | Individual control (H-02) is primary; static parameters are floor, not target |
| **Sensory sensitivity** (low threshold, passive) | Zone 2–3 — quiet workspace, consultation | RT60 ≤0.4 s; NC-25; no sudden sound events | 50–200 lux; consistent; no flicker (B-03/04) | ≤3000 K | NCS chroma ≤3; predictable palette; no sudden colour change | Predictability and consistency are as important as attenuation level |
| **Sensory seeking** | Zone 1–2 — active circulation, social zones | RT60 ≤0.6 s (minimum acceptable); NC-35 | 300–500 lux; daylight; dynamic circadian (B-01) | 4000–6500 K daytime | NCS chroma ≤6; varied but controlled; biophilic elements (BIO-01) | Higher stimulation serves engagement; still below clinical distress thresholds |
| **Low registration** | Zone 1 — entry, circulation spine | RT60 ≤0.5 s with clear SNR ≥15 dB (signal intelligibility) | ≥300 lux; ≥500 lux at task surfaces; high circadian EML | ≥4000 K daytime | LRV ≥30 at all wayfinding elements; high-contrast clear signage (D-08) | Stronger cues required to register environmental information — serves DEM as well |

**Zone cross-reference:**
- Zone 1 (high activation): entry, reception, main corridors — Items: F-01, A-01, B-07, C-04
- Zone 2 (moderate): workspace, consultation, dining — Items: F-01, A-02, B-06, G-05
- Zone 3 (low activation): sensory retreat, quiet rooms — Items: A-16, F-03, B-06, A-03

**Conflict notes:**
- Sensory avoiding vs low registration: resolved by SZ (Sensory Zoning) — Zone 3 serves avoiding; Zone 1 serves low registration. These populations do not share a zone.
- Sensory seeking vs sensory sensitivity: resolved by IEC (Individual Environmental Control, H-02) within Zone 2 — individual dimming and acoustic partition access resolve the conflict at the workstation level.
- DEM illuminance requirement (≥300 lux daytime, DSDC 2024) conflicts with NDV ambient preference (≤200 lux). Resolved via three-zone model (§5.2 LIGHT-INT): Zone 1/2 serves DEM circadian; Zone 3 serves NDV. Individual dimming (B-06) resolves at individual level within Zone 2.

**Implementation note:** This matrix does not replace individual item specifications. It provides the coordination framework ensuring that A, B, C, and F category specifications are calibrated consistently across zones. Conflicts between items in the same zone are resolved by §5.2 and Part 5.

● [sensory-processing-model-design-application BPC — Opus synthesis]; ◐ [Unwin et al. 2022 Tier 3 — individual control as primary variable]; ◐ [PAS 6463:2022 Tier 5]; ◐ [DSDC EADDAT 2022 Tier 4]

---

**Jurisdiction comparison:** No code addresses sensory gradients. UK PAS 6463:2022 recommends graduated sensory environments. Guidebook's high→low stimulation gradient from entry to occupation is a novel design framework derived from NDV/AUT sensory processing research.


### F-02 Olfactory Control (Fragrance-Free Zones in Sensitive Areas)
<!-- CON-0015 [HIGH]: F-04 MERV 13+/TVOC + F-02 fragrance-free — chemical sensitivity co-specification -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:OFS|NDV -->
<!-- grade_confidence: VERY LOW — Fragrance-free zones: Mast Cell Action guidance (Tier Co-1). No RCT on fragrance-free zones for OFS/NDV outcomes in built environments. No standard in any jurisdiction. VERY LOW — operational policy with clinical rationale but no architectural evidence. -->

<!-- CON-0063 [MODERATE]: Fragrance-free policy serves NDV/MH (PTSD) via chemical stimuli as trauma triggers. Add NDV/MH to population coverage. Trauma-informed design framework confirms mechanism but does not cross-reference IAQ specifications. -->
**Applicable Groups:** NDV, PAIN, MH, OFS · NDV/SENS
<!-- CON-0015: CON-0015: olfactory control serves NDV/SENS alongside OFS/MCAS — multiple sensory pathways -->

**Description:** No air freshener, scent diffuser, or fragranced cleaning product in spaces designated as sensory sensitive or CFS/ME-accessible. Fragrance-free policy posted at entry to fragrance-free zones. Cleaning specification: fragrance-free products only.

**Specifications:**

No scent diffusers, aerosol air fresheners, or strong-scented candles in sensitive spaces

Cleaning products: fragrance-free specified in cleaning contract

HVAC: no scent injection at air handling units in sensitive zones

Policy signage: 'Fragrance-Free Zone' at entry

Maintenance: regular audit of compliance

**Retrofit cost note:** Retrofit penalty: LOW. Olfactory control through fragrance-free zone designation is primarily a management and

HVAC specification decision. Retrofit may require zoned ventilation modifications but primarily involves policy and signage changes. See

Part 12 §12.4.1.

**Key citations:** British Standards Institution. (2022). PAS 6463:2022. BSI. Patient Led Research Collaborative. (2024). ME/CFS management guide.

**Cross-reference:** A-08 (HVAC); H-02 (Individual Environmental Control)

**Evidence basis (OT):** EHP Framework (prevent strategy); Dunn's Sensory Processing Model. Fragrance-free zones implement the EHP 'prevent' strategy by removing chemical trigger sources before they reach OFS/MCAS, NDV, and PAIN users; the specification of no introduced fragrance sources (diffusers, cleaning products, personal fragrance signage) is the minimum preventive context.

**Jurisdiction comparison:** No code addresses olfactory control as accessibility. WELL Air concept includes VOC limits. Guidebook specifies fragrance-free zones in sensitive areas — derived from MCAS/OFS/migraine chemical sensitivity evidence.


### F-03 Graduated Stimulation Re-entry (Sensory Room to General Space Transition)
<!-- design_stage_lock: SD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:NDV|OFS|NDV/MH -->
<!-- grade_confidence: LOW — Graduated stimulation re-entry: PAS 6463 + Kaplan 1995 (J Environmental Psychology Tier 3). Sensory transition zone principle. No RCT. Expert consensus + Tier 3-4. -->

**Applicable Groups:** NDV, PCS, AUT, OFS

**Description:** The transition from sensory room (A-16) or quiet room to general circulation is a graduated zone, not an abrupt step-change.

A 3--5 m transition space (intermediate stimulation level) is provided between the sensory room exit and the general circulation route.

**Specifications:**

Transition zone: 3--5 m depth between sensory room exit and primary circulation

Intermediate stimulation: NC 30; muted palette; 100--200 lux

Seating available in transition zone

No high contrast or high-stimulation elements within 5 m of sensory room exit

**Retrofit cost note:** Retrofit penalty: MODERATE. Graduated stimulation re-entry zones require spatial provision of a transition

space. At design stage this is a planning decision. Retrofit requires area allocation and acoustic/visual treatment as a partition or alcove

intervention. See Part 12 §12.4.2.

**Key citations:** British Standards Institution. (2022). PAS 6463:2022. BSI. Kaplan, S. (1995). Journal of Environmental Psychology, 15(3), 169--182.

**Cross-reference:** A-16 (Sensory Room); F-01 (Sensory Gradient)

**Evidence basis (OT):** EHP Framework (establish strategy); Dunn's Sensory Processing Model. Graduated re-entry implements EHP's 'establish' strategy: the design builds on the user's existing regulatory capacity by providing a low-stimulation transition space that allows sensory regulation to be re-established at the user's own pace before re-entering higher stimulation zones.

**Jurisdiction comparison:** No code addresses transition from low-stimulation to general spaces. Guidebook-specific provision — sensory room users need graduated re-entry to avoid sensory shock. Cross-reference A-16 (sensory room), F-01 (sensory gradient).


### F-04 Air Quality (MERV 13+ Filtration, Low-VOC Specification, Thermal Stability)
<!-- CON-0015 [HIGH]: F-04 MERV 13+/TVOC + F-02 fragrance-free — chemical sensitivity co-specification -->
<!-- CON-0102 [HIGH]: F-04/F-06/F-07/F-08 interdependent OFS/MCAS HVAC system — F-category coherence note required -->
<!-- CON-0132 [HIGH]: F-04 MERV 13+/TVOC + BIO biophilic design — air quality + biophilic convergence -->
<!-- CON-0142 [HIGH]: F-07 thermal + F-04 air quality — OFS/MCAS dual trigger co-specification -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:OFS -->
<!-- grade_confidence: LOW — MERV 13+ filtration + low-VOC + TVOC ≤0.5 mg/m³: EN ISO 16000-9 (Tier 4 standard) + Mast Cell Action Tier 2. WELL v2 Air Feature. OFS/MCAS chemical sensitivity evidence is Tier 2-3 clinical. No built-env RCT on MERV rating for OFS symptom outcomes. LOW — clinically grounded, architecturally extrapolated. -->

<!-- CON-0063 [MODERATE]: MERV 13+ filtration serves MH/PTSD populations — chemical stimuli function as trauma triggers. Cross-reference F-02 fragrance-free. -->
<!-- CON-0102 [HIGH]: [INTRA-INDIVIDUAL] OFS/MCAS thermal+chemical co-trigger. Individual radiant heating (F-07) must not use recirculated air without HEPA (F-04). Coordinate F-04 filtration with F-07 thermal zoning delivery method. -->
**Applicable Groups:** OFS/MCAS, OFS/CFS, NDV (chemical sensitivity),

PAIN (fragrance triggers), NEU (chemical sensitivity in PCS/ABI)

**Description:** New item added in v9.0 per OFS category review (Stage 3). A comprehensive air quality specification for all spaces regularly occupied by OFS/MCAS, chemically sensitive NDV, or PCS users. F-04 extends and complements F-02 (Fragrance-free zones): where F-02 addresses introduced fragrances at the policy level, F-04 addresses the built-in physical specification of filtration, materials, and thermal stability that determines baseline air quality.

**Specifications:**

Filtration: MERV 13 minimum in all air handling units serving

OFS-occupied spaces

Fresh air supply: ≥10 L/s per person in primary occupied spaces; ≥15

L/s per person where OFS, or immunocompromised (DEM/NEU post-COVID) users are primary occupants

VOC specification: all finishes, adhesives, sealants, flooring, ceilings, and furniture within OFS-occupied spaces: TVOC ≤0.5 mg/m³ at

28 days post-installation, measured per EN ISO 16000-9

Cleaning products: specify low-fragrance, low-VOC cleaning products in maintenance specification; no aerosol sprays on OFS-occupied floors

during occupied hours

Thermal stability: ambient temperature variation ≤1°C per hour in primary occupied spaces; ≤2°C across any zone on the primary route;

maximum 3°C differential at entry vestibule to main space; target ambient 21°C on primary routes

HVAC commissioning: air quality test at practical completion and at 28 days post-occupation; results documented in building log

No fragrance diffusers: electronic, passive, or HVAC-integrated scent diffusion systems excluded from OFS-occupied environments (extends

F-02)

Plantings: where biophilic planting is specified (BIO-02), select low-VOC, low pollen species; avoid strongly scented flowering plants

on OFS-occupied floors

**Retrofit cost note:** Retrofit penalty: MODERATE. MERV 13+ filtration and low-VOC specification require correct HVAC plant

selection and finish specification at design stage. Retrofit requires filter upgrade (plant modification) and full finish replacement

programme (significant disruption and cost). See Part 12 §12.4.

**Key citations:** Mast Cell Action. (2023). Environmental triggers: guidance for building design. Mast Cell Action. Afrin, L.B., et al. (2020). Mast cell activation disease: An underappreciated cause of neurological and psychiatric symptoms. Brain, Behavior, and Immunity, 89, 218--225. CIBSE. (2015). CIBSE Guide A: Environmental Design (8th ed.). CIBSE. British Standards Institution. (2022). PAS 6463:2022. BSI. EN ISO 16000-9:2006. Indoor air — Part 9: Determination of emission of volatile organic compounds. ISO.

**FDR-OFS-03 [Tier 3 — Afrin 2020]:** MCAS co-occurrence with OFS (Afrin et al. 2020, *Brain, Behavior, and Immunity* — Tier 3). MCAS chemical triggers include post-installation VOC off-gassing. ● Add commissioning specification to F-04: OFS/MCAS-designated spaces to not be occupied until post-installation VOC test confirms TVOC ≤0.5 mg/m³ at 28-day clearance (consistent with existing F-04 TVOC specification). This is a commissioning stage gate — not an additional material requirement. Add to Design Stage: Commissioning (pre-occupation air quality gate for OFS/MCAS spaces).

**Tier X:** No RCT-level evidence for MERV 13 specification in relation to MCAS symptom reduction identified as of March 2026.

Specifications are derived from MCAS trigger literature and HVAC engineering standards. Evidence review recommended at next revision.

**Cross-reference:** F-02 (Fragrance-free zones — policy-level extension of this item); A-08 (HVAC noise control — same AHU specification; coordinate); BIO-02 (Interior planting — species selection for low-VOC); §2.11 OFS; §2.6 NDV

**Evidence basis (OT):** Compensatory FOR; Dunn's Sensory Processing Model. Air quality provisions implement the Compensatory FOR by removing chemical and particulate environmental triggers that would otherwise require OFS/MCAS and chemically sensitive users to withdraw from the space; the MERV 13 and TVOC ≤0.5 specifications are derived from the trigger thresholds documented in MCAS and chemical sensitivity clinical literature.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Filtration | VOC Limit | Ventilation Rate | Notes |
|---|---|---|---|---|---|
| US | ASHRAE 62.1 / WELL Air | MERV 13+ (WELL) | WELL limits | ASHRAE 62.1 rates | ADA has no air quality provision |
| UK | AD F / CIBSE Guide A | — | — | AD F rates | No BS 8300 air quality provision |
| EU | EN 16798-1:2019 | — | — | Category I-IV rates | Replaces EN 15251 |
| DE | ASR A3.6 | — | — | Workplace mandatory | — |
| **Guidebook** | **F-04** | **MERV 13+** | **Low-VOC spec** | **EN 16798 Cat I** | **MCAS/OFS-driven** |

No accessibility code addresses air quality. WELL Air is closest to disability-specific provisions. MCAS/chemical sensitivity needs exceed any standard.


### F-05 Seated-Task Design [CONTENT MOVED TO G-08 per CO-0003/D2-48]
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:OFS|PAIN -->
<!-- grade_confidence: LOW — MOVED to G-08 per CO-0003. Rating based on pain-ofs BPC: OT energy conservation CPG (Tier Co-2). No architectural RCT. LOW. -->
<!-- CO-0003: F-05 content now lives in G-08 (below, in new items section). G-08 covers: seated-task design for all primary occupational tasks; adjustable-height work surfaces 650–870 mm AFF; seated option at all service counters. Populations: OFS · PAIN · MOB · ALL. --> (All Primary Occupational Tasks Achievable Without Sustained Standing)

<!-- CON-0004 [HIGH]: New item G-08 (Adjustable Posture Seating Provision) to specify: ≥1 reclined/tilt seat per primary zone (≥120° recline with footrest); all reception counters with adjacent seated waiting ≤3 m; all shared work surfaces with ≥1 seated-height station (813 mm). Populations: OFS, PAIN, MOB, NEU. F-05 content to migrate to G-08. -->

**Applicable Groups:** OFS/POTS, OFS/CFS, MOB (wheelchair users ---

G-06 below), UPL; also benefits ALL users at service points

**Description:** New item added in v9.0 per OFS category review (Stage 3). Every primary occupational interaction in the building --- service counter transaction, kiosk use, workstation task, check-in, reception, triage, waiting — must be achievable without sustained standing (defined as standing for more than 2 continuous minutes without a seating option). F-05 requires that all task locations are provided with appropriate seating, and that the task can be completed from a seated position without a visible distinction from the standard standing transaction.

**Specifications:**

Service counters: all counter transaction types achievable from a seated position at the accessible lowered counter section (G-06:

760--860mm AFF) without requiring the user to stand at any point

Queue systems: seating available within the queue area — not at a separate accessible position — so that the queue position is held

without standing; take-a-number or digital queue systems are an acceptable alternative to physical queue standing

Kiosks and self-service terminals: all interaction elements within

400--1200mm AFF; knee clearance below terminal ≥690mm height × 760mm width × 480mm depth (consistent with G-06 and H-01); seating or

perching support available at all kiosk stations

Where workstations are provided (office, workplace, educational): all primary work tasks achievable seated; height-adjustable desks or fixed

seated-height workstations (≤760mm surface height) for OFS-designated workstations

Waiting areas: seated waiting available within all waiting areas with no standing-only option; minimum ratio 1:4 accessible seats to

standard seats in any waiting area

Visual design: seated task provisions should not be visually distinct from standard provisions where achievable (consistent with dignity

principle and MH non-clinical aesthetics principle)

**Retrofit cost note:** Retrofit penalty: LOW. Seated-task design is primarily a furniture and fixture height specification. Retrofit is furniture/fixture replacement and counter height modification. See Part 12 §12.4.1.

**Key citations:** Benarroch, E.E. (2012). Postural tachycardia syndrome. Mayo Clinic Proceedings, 87(12), 1214--1225. Blitshteyn, S.,

\& Whitelaw, S. (2021). POTS and other autonomic disorders after

COVID-19. Autonomic Neuroscience, 235, 102841. Patient Led Research

Collaborative. (n.d.). Clinician's pacing and management guide for

ME/CFS and Long COVID. PLRC. British Standards Institution. (2018). BS

8300:2018. BSI. ISO 21542:2021. Building construction ---

Accessibility and usability. ISO.

**Tier X:** No systematic review of seated-task design requirements specific to POTS in built environments identified as of March 2026.

Specifications are derived from POTS clinical literature and extrapolated from existing accessible service counter standards.

Evidence review recommended at next revision.

**Cross-reference:** G-06 (Reception counter lowered section — F-05 requires this as minimum; adds seated-queue and kiosk requirements);

H-01 (Controls reach zone); E-10 (Rest seating on circulation routes

— covers the route; F-05 covers the task point); §2.11 OFS/POTS;

H-02 (Individual Environmental Control — H-02 specifies user adjustability of environmental parameters; F-05 specifies task

accessibility at service/workstation points: distinct, complementary scope)

**Evidence basis (OT):** Life Balance Model; EHP (alter strategy). Seated-task design alters the environmental context of service delivery and workstation design to eliminate the requirement for sustained standing as a pre-condition of participation; for OFS/POTS users whose orthostatic intolerance makes sustained standing a physiological hazard, this item implements the EHP 'alter' strategy at the task level — the task remains but the postural demand is removed.

**Jurisdiction comparison:** CONTENT MOVED — see G-08 (Bedroom Wardrobe and Storage Reach Configuration).


### F-06 Fragrance-Free Policy (Whole-Building Operational Standard)
<!-- CON-0102 [HIGH]: F-04/F-06/F-07/F-08 interdependent OFS/MCAS HVAC system — F-category coherence note required -->
<!-- design_stage_lock: B -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:OFS|NDV -->
<!-- grade_confidence: VERY LOW — Fragrance-free whole-building operational policy: Mast Cell Action (Tier Co-1) + clinical MCAS trigger literature (Tier 2-4). No OT CPG, no RCT, no standard in any jurisdiction. Operational policy only. VERY LOW — maximum evidence base available for this clinical context; architectural extrapolation. -->

<!-- CON-0102 [HIGH]: F-06 fragrance-free whole-building policy coordinates with F-04 filtration and F-08 thermal vestibule to prevent OFS/MCAS chemical+thermal co-triggering. -->
**Applicable Groups:** OFS/MCAS, OFS/CFS, NDV (chemical sensitivity), PAIN (fragrance triggers), NEU/PCS

**Description:** This guidebook recommends a documented fragrance-free operational policy for all spaces routinely occupied by OFS/MCAS, NDV (chemical sensitivity), PAIN, or NEU/PCS populations. This is an operational specification embedded in the facility management (FM) brief, occupancy agreements, cleaning specification, and staff induction materials. It is not a design element but a designed-in operational requirement — it must be specified at brief stage to be enforceable at Ready for Occupancy. Fragrance-free policy is the built environment's primary OFS/MCAS chemical trigger prevention mechanism; no architectural intervention substitutes for it. ● [REF:air-quality-voc:04]

**Specifications:**
- ● No fragrance diffusers (electronic, passive HVAC-integrated, or plug-in) in any occupied space where OFS/MCAS or chemical-sensitive populations are identified [REF:air-quality-voc:04]
- ● Cleaning products in OFS-occupied environments to be low-fragrance, low-VOC formulations; no aerosol sprays during occupied hours [REF:air-quality-voc:04]
- ○ A written fragrance-free policy to be embedded in: FM brief, lease/occupancy agreements, staff handbook, and cleaning specification [EXPERT CONSENSUS — operational requirement; no built-environment standard specifies this; project-standards DEM olfactory wayfinding rule 2026-03-30]
- ○ Policy scope to include occupants, staff, contractors, and cleaning operatives [EXPERT CONSENSUS]
- ○ Biophilic planting in OFS-occupied spaces: low-VOC, low-pollen species only; no strongly scented flowering plants [REF:air-quality-voc:04]
- ○ Building commissioning hold point: occupancy of OFS-primary spaces to be deferred until post-installation VOC clearance test confirms TVOC ≤0.5 mg/m³ at 28 days (EN ISO 16000-9) [REF:air-quality-voc:05]

**Design Stage:** Brief · Pre-Design (operational policy must be embedded at brief stage to appear in occupancy agreements)

**Retrofit cost note:** Retrofit penalty: NEGLIGIBLE. F-06 is a policy, not a construction item. Cost is operational (cleaning product substitution, policy documentation). No capital expenditure required. See Part 11 §11.4.

**Key citations:** [REF:air-quality-voc:04] Mast Cell Action (2023). MCAS environmental management guidance. mastcellaction.org. Tier 2, UK. [REF:air-quality-voc:05] EN ISO 16000-9:2006. Indoor air — Part 9: Determination of emission of volatile organic compounds from building products and furnishing. ISO. Tier 4.

**Cross-reference:** F-02 (Olfactory control — fragrance-free zones); F-04 (Air quality — MERV 13+ filtration, TVOC specification); F-08 (Thermal transition vestibule — OFS co-trigger prevention); H-02 (Individual environmental control)

**Evidence basis (OT):** EHP (alter strategy). F-06 alters the chemical environment of the built setting to remove MCAS/MCS triggers before they reach the occupant. No OT CPG addresses fragrance-free policy as a home modification domain; specifications derive from clinical trigger literature (Tier 2–4). ○ [THIN-BASE — operational policy domain; no OT practice guideline or RCT evidence; expert consensus + clinical rationale]

**Tier disclosure:** [EXPERT CONSENSUS — no built-environment standard or OT CPG mandates fragrance-free policy for chemical sensitivity populations in any jurisdiction searched (March 2026). WELL v2 Air Quality feature is the closest voluntary framework but does not specify fragrance-free policy. This item is operational policy, not architectural specification. Evidence review recommended at next revision.]

**Jurisdiction comparison:** No building code mandates fragrance-free policies. US Job Accommodation Network provides guidance. Some US/CA government buildings have voluntary policies. Guidebook specifies whole-building operational standard — derived from MCAS/OFS chemical sensitivity evidence.


### F-07 Thermal Zoning — Building-Wide Temperature Management
<!-- CON-0041 [HIGH]: Japan heat shock: inter-room thermal differential ≤5°C; F-07 heated bathroom floor as prevention -->
<!-- CON-0102 [HIGH]: F-04/F-06/F-07/F-08 interdependent OFS/MCAS HVAC system — F-category coherence note required -->
<!-- CON-0142 [HIGH]: F-07 thermal + F-04 air quality — OFS/MCAS dual trigger co-specification -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:NEU|OFS|PAIN -->
<!-- grade_confidence: MODERATE — Thermal zoning ≤18–21°C: ms-thermal-temperature-conflict-resolution BPC (Opus synthesis). MSIF Atlas 2023 (Tier 3, 60-80% MS heat sensitivity). CDC ME/CFS (Tier Co-1). WHO HHGL 2018 (Tier 4). ≥8 jurisdictions reference thermal comfort standards. No disability-specific built-env RCT but strong clinical evidence + physical principle. MODERATE. -->

<!-- CON-0102 [HIGH]: [INTRA-INDIVIDUAL] OFS/MCAS. Individual supplemental radiant heating must not recirculate air — OFS/MCAS user experiences thermal and chemical triggers from same HVAC system. Coordinate with F-04 HEPA requirement. -->
**Applicable Groups:** NEU/MS · SCI · OFS · PAIN · DEM · ALL
<!-- CO-0003 new item. CON-0041: inter-room thermal differential ≤5°C safety specification. -->

**Description:** Building-wide HVAC zoning strategy to maintain ambient temperatures that are safe for Uhthoff's-threshold users (NEU/MS) while enabling individual supplemental heating for PAIN and OFS users who require warmth. Resolves the primary TEMP-RANGE cross-population conflict (see Part 5 §5.2).

**Specifications:**
- ● Ambient temperature in all primary activity spaces and shared circulation to be maintained at ≤18°C where NEU/MS is a primary or significant secondary population [REF:ms-thermal-temperature-conflict-resolution:01] *(Uhthoff's phenomenon — heat-induced demyelination worsening is safety-critical; not a preference)*
- ● Inter-room thermal differential across the building to not exceed 5°C [CON-0041] *(sudden temperature change from cold corridor to warm room is a neurological and cardiovascular trigger for OFS/POTS and NEU/MS)*
- ● Individual supplemental radiant heating to be provided at all fixed seating positions in spaces serving PAIN or OFS populations: wall-mounted or portable radiant panel rated ≤22°C output at 0.5 m [REF:ms-thermal-temperature-conflict-resolution:02] *(PAIN allodynia and fibromyalgia require local warmth delivery without raising shared ambient)*
- ● All apartment or room thermostats (residential settings) to be individually controllable within a 16–24°C range [REF:ms-thermal-temperature-conflict-resolution:01]
- ○ Insulated coatings specified for all grab bars, handrails, and door hardware on primary circulation routes serving PAIN populations [CON-0003] *(cold metal contact triggers allodynia)*
- ○ In tropical climates (ambient >28°C) where mechanical cooling is absent: SCI (above T6 lesion) populations require passive cooling strategy as primary design intervention — cross-ventilation, solar shading, high ceiling, low SHGC glazing. Continuous indoor ambient above 28°C exceeds resting thermoregulatory capacity for tetraplegia (impaired sweating ~30% normal; impaired vasodilation) [REF:thermoregulation-built-environment:01] *(PROVISIONAL — no SCI-specific tropical ambient threshold confirmed in accessible design standards; threshold extrapolated from clinical evidence + WHO HHGL Annex G; Opus synthesis pending)*

**Design Stage:** Schematic Design (HVAC zoning strategy) · Technical Design (equipment specification)

**Retrofit:** MODERATE penalty — HVAC zoning requires duct reconfiguration. Supplemental radiant panels are LOW penalty (plug-in or surface-mounted). DAR: conduit provision for supplemental heating infrastructure at all fixed seating clusters.

**Population conflict:** PAIN warmth preference conflicts with NEU/MS ambient ≤18°C requirement. Resolution: ambient governs (safety-critical — Uhthoff's mechanism); PAIN warmth delivered individually. See Part 5 §5.2 TEMP-RANGE and §5.3 CONF-UNRESOLV-01.

**CON-0107 [MEDIUM]:** In care bedrooms with ceiling hoist (I-04), supplemental radiant heating panels must clear the hoist track path. Coordinate wall-mounted panel positions with hoist track sweep zone at Detailed Design. Cross-ref: I-04.

**CON-0101 [HIGH]:** HVAC system selection to achieve NC-25 (A-08) — radiant heating systems are preferred over forced air in NEU/OFS spaces (lower noise contribution and no airborne trigger). For SCI populations, radiant systems additionally avoid ambient heat load increase in cooling-critical environments [thermoregulation-built-environment BPC — PROVISIONAL]. Coordinate with A-08 and F-08 thermal mass specification. Cross-ref: A-08, F-08.

<!-- NEW ITEM — CO-0003. Derives from TC-01/TC-02/TC-03 (Appendix C, now integrated into Part 4).
     Evidence: ms-thermal-temperature-conflict-resolution BPC; thermal-comfort-older-adults-care-settings BPC; thermoregulation-built-environment BPC (SCI/tropical — PROVISIONAL; Opus synthesis pending).
     CON connections: CON-0003 (MS vs PAIN thermal conflict), CON-0004 (OFS thermal).
     DRAFT REQUIRED: item-specification-writer briefing pending. -->

**FDR-MST-02 [Tier 3 — Krupp 2003]:** MS fatigue follows a diurnal pattern with peak fatigue typically mid-afternoon (Krupp et al. 2003). ○ In NEU/MS-specialist facilities, BMS programming to reduce ambient temperature 1–2°C from morning setpoint during afternoon period (approx. 13:00–17:00) may reduce afternoon fatigue symptom load. BMS schedule to be configurable by occupant or care team. [THIN — clinical mechanism only; no built environment study; BMS programming is zero-cost at commissioning stage]

**FDR-TCOA-02 [Tier 3 — MHLW Japan 2023]:** Bathroom heat shock is caused by inter-room temperature differential at entry, not absolute temperature. Japanese evidence: 6,073 bathtub deaths annually from heat shock in cold bathroom (MHLW 2023 Tier 3; Nakayama 1981 foundational study). ○ In DEM and older adult residential settings, bathroom pre-heating specification: timer or PIR sensor activates bathroom heating ≥30 min before scheduled bathing; bathroom reaches ≥20°C before occupant entry. Specification to be included in FM commissioning brief and BMS programming.

**FDR-TCOA-03 [Tier 5 — NHS Estates HBN 00-10]:** Reduced peripheral sensation in DEM and older adult populations increases burns risk from hot surfaces. ● Low Surface Temperature (LST) radiators, surface temperature ≤43°C per NHS Estates HBN 00-10, to be specified in all DEM and older adult residential and care bedrooms and bathrooms. Insulated pipework throughout. Thermostatic heated towel rails ≤43°C surface temperature in DEM/older adult settings. These are not comfort specifications — they are burn prevention safety specifications.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Comfort Range | Categories | Individual Control | Notes |
|---|---|---|---|---|---|
| US | ASHRAE 55-2023 | PMV ±0.5 (Cat. B) | 3 categories | — | General population only |
| UK | CIBSE Guide A | 21-23°C (offices) | — | — | CQC for care homes |
| EU | EN 16798-1:2019 | Cat I-IV | 4 categories | — | Replaces EN 15251 |
| DE | ASR A3.5 | 20-26°C (workplace) | Mandatory | — | — |
| ISO | ISO 7730:2005 | PMV-PPD model | A/B/C | — | Reference method |
| **Guidebook** | **F-07** | **Individual zones** | **Per population** | **Yes — H-02** | **MS heat vs DEM cold conflict** |

**KEY GAP:** No thermal comfort standard addresses disability-specific thermoregulation. MS heat sensitivity (Uhthoff's phenomenon) vs DEM cold sensitivity requires individual zoning beyond any standard.


### F-08 Thermal Transition — Heating and Cooling System Response
<!-- CON-0102 [HIGH]: F-04/F-06/F-07/F-08 interdependent OFS/MCAS HVAC system — F-category coherence note required -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:OFS|NEU -->
<!-- grade_confidence: MODERATE — Thermal transition — heating/cooling system response: ofs-built-environment BPC + ms-thermal BPC (Opus). Clinical evidence for OFS thermal triggers is Tier 1-3 (IOM/NAM, CDC, Bateman Horne). No built-env RCT on HVAC response time for OFS outcomes. MODERATE — clinical basis strong; architectural specification extrapolated. -->

<!-- CON-0102 [HIGH]: Thermal vestibule specification must coordinate with F-06 fragrance-free and F-04 MERV 13. OFS/MCAS intra-individual co-trigger: thermal transition + chemical exposure from vestibule air handling. -->
**Applicable Groups:** NEU/MS · OFS · PAIN · DEM
<!-- CO-0003 new item (formerly F-07 in CO-0003 draft; renumbered F-08 as F-07 = zoning). -->

**Description:** System response characteristics and passive thermal performance strategies to minimise sudden thermal changes — which are a neurological trigger (Uhthoff's), orthostatic trigger (OFS/POTS), and pain amplifier (PAIN/fibromyalgia) — between arrival, circulation, and occupied spaces.

**Specifications:**
- ● High-performance thermal envelope (U-value ≤0.15 W/m²K walls, ≤0.10 roof in new build) to reduce thermal drift and inter-room differential [REF:ms-thermal-temperature-conflict-resolution:03]
- ● Thermal mass provision in exposed slab or wall construction to dampen daily temperature swing to ≤3°C [REF:ms-thermal-temperature-conflict-resolution:03]
- ● HVAC control system response time to thermal setpoint change not to exceed 15 minutes for primary occupied spaces
- ○ Entry vestibule (thermal buffer ≥2 m depth) at all primary accessible entrances in climates with >15°C seasonal variation [CON-0041] *(prevents thermal shock on entry for OFS/POTS and NEU/MS users)*

**Design Stage:** Schematic Design (envelope strategy) · Technical Design (HVAC system specification)

**Retrofit:** HIGH penalty (envelope). LOW penalty (vestibule addition if structurally feasible). DAR: note thermal bridge locations for future insulation upgrade.

**CON-0108 [MEDIUM — CON-0068; pain-ofs BPC]:** Where F-08 thermal vestibule is specified, spatial coordination with E-series entrance items is required: (a) both vestibule doors (outer and inner) to meet E-01 accessible door specification; (b) level entry (E-06) at both vestibule thresholds — no raised threshold at either door; (c) lighting (E-13) continuous through vestibule — no dark transition zone between outer and inner doors; (d) where E-14 entrance rest seating is specified, locate within or immediately after vestibule so that OFS users benefit from thermal protection while resting. These four coordination items must appear on the same drawing set at Schematic Design stage.

<!-- NEW ITEM — CO-0003 (was listed as F-07 in CO-0003; renumbered F-08 as F-07 now = thermal zoning).
     CON connections: CON-0003 (thermal). DRAFT REQUIRED. -->

[PLACEHOLDER — F-08 Thermal Transition: system response time, thermal mass, passive strategies.
Populations: NEU/MS, OFS, PAIN.
Evidence basis: ms-thermal-temperature-conflict-resolution BPC.]


**Description:** A documented building-wide fragrance-free policy is embedded in the FM brief, cleaning specification, occupancy agreement, and staff handbook before occupation. Complements F-02 (zone designation) and F-04 (physical air quality specification) by establishing the organisational governance layer: policy applies to all occupants, staff, contractors, and cleaning products throughout the building, not only in designated sensitive zones.

**Specifications:**

Policy document: fragrance-free requirements for the building stated in writing in FM brief, cleaning contract, and where applicable occupancy or lease agreement

Staff handbook: staff working in OFS/MCAS-occupied environments instructed in no personal fragrance (perfume, scented lotion, scented haircare) during working hours; policy stated at recruitment, induction, and in ongoing HR documentation

Cleaning specification: fragrance-free cleaning products specified throughout the whole building; no aerosol sprays in occupied areas at any time; products listed in maintenance specification and verified at each contract renewal

Contractor management: fragrance-free policy extended to all contractors and maintenance workers entering the building; requirement stated in site induction and works specification

Visitor policy: fragrance-sensitive environment signage at all primary entries; visitor guidance available digitally (QR code) and in print at reception; gentle, non-punitive tone per Disability Confident framing principles

Monitoring: FM responsible person conducts fragrance policy compliance audit quarterly; non-compliance reported and actioned within 10 working days; results recorded in building log

Review: policy reviewed annually and updated to reflect changes in cleaning product specifications or OFS population occupancy profile

**Retrofit cost note:** Retrofit penalty: ZERO. Fragrance-free policy is a management, procurement, and HR decision. No structural or physical works required. Policy can be implemented at any time in a building's lifecycle. Residual cost is FM staff time and signage procurement. See Part 12 §12.4.1.

**Key citations:** Afrin, L.B., et al. (2020). Mast cell activation disease. Brain, Behavior, and Immunity, 89, 218--225. Mast Cell Action. (2023). Environmental triggers: guidance for building design. Mast Cell Action. Steinemann, A. (2018). Prevalence and effects of multiple chemical sensitivities. Preventive Medicine Reports, 10, 134--139. British Standards Institution. (2022). PAS 6463:2022. BSI.

**BPC note:** [BPC NOT OPUS-REVIEWED --- air-quality-voc-chemical-sensitivity-built-environment: opus_synthesis not confirmed. Reduced-confidence warning applies to all specifications.]

**Tier note:** No jurisdiction has a statutory fragrance-free building policy standard. Specifications derived from MCAS/MCS clinical trigger literature and FM best practice. Evidence tier: 4--5.

**Cross-reference:** F-02 (Fragrance-free zones --- F-02 designates specific zones with signage; F-06 establishes the whole-building governance framework: complementary, non-overlapping scope); F-04 (Air quality physical specification --- F-04 specifies filtration and VOC infrastructure; F-06 specifies the operational and HR governance layer); A-08 (HVAC); §2.11 OFS

**Evidence basis (OT):** EHP Framework (prevent strategy); Dunn's Sensory Processing Model. A whole-building fragrance-free policy implements the EHP 'prevent' strategy at the organisational level: chemical trigger sources are removed before they enter the building environment rather than being managed reactively after exposure; for OFS/MCAS users, involuntary chemical exposures from staff, cleaning products, or contractors are as physiologically hazardous as those from building materials --- the physical specification of F-04 is insufficient without the governance layer of F-06.


## CATEGORY G: FURNITURE, FIXTURES AND INTERIOR ELEMENTS

**Jurisdiction comparison:** No code addresses thermal transition as accessibility. ASHRAE 55 and EN 16798-1 address thermal comfort but not transition response. Guidebook specifies heating/cooling system response time — derived from MS heat sensitivity (Uhthoff's) and OFS temperature intolerance evidence.


### G-01 Defensible Seating (Back-to-Wall, Entry Sightline Configuration)
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:NDV/MH|DEM -->
<!-- grade_confidence: VERY LOW — Defensible seating: psychiatric design literature (DiMHN, Tier Co-1; Faerden 2022 PMID:36567605 Tier 3 — single rooms, not specifically seating orientation). Environmental psychology theory (Tier 3). No RCT on seating orientation for outcomes. -->

**Applicable Groups:** MH (PTSD, trauma, anxiety), AUT, DEAF · OFS · PAIN · DEM · NEU
<!-- CON-0087: back-to-wall seating reduces disorientation and threat response for DEM/NEU -->
<!-- D2-41: D2-41: back-to-wall seating reduces hypervigilance-related fatigue for OFS/NDV/MH -->

**Description:** Seating in all waiting areas and communal spaces includes options with back-to-wall positioning and clear sightlines to all room entries. Minimum 30% of seating in any public waiting area meets this specification. No seating with back to open space or unobserved corridor.

**Specifications:**

30% of seating in public waiting areas: wall-backed with entry sightline

No seating with back to open/unobserved space

Multiple sightline options available without user requesting special seating

Co-located with general seating — not segregated 'accessible' area

**Retrofit cost note:** Retrofit penalty: LOW. Defensible seating configuration is a furniture procurement and placement decision.

Retrofit is furniture repositioning and procurement without structural implications. See Part 12 §12.4.

**Key citations:** Dignified Design. (2024). 22 design elements for permanent supportive housing. DeafSpace Project, Gallaudet University.

(2010). DeafSpace design guidelines. British Standards Institution.

(2022). PAS 6463:2022. BSI.

**Cross-reference:** D-07 (No Blind Corners); D-10 (Transparent

Partitions); C-01 (Palette)

**Evidence basis (OT):** PEOP Model (volition subsystem); Prospect-Refuge Theory. Defensible seating implements both Prospect-Refuge Theory (back-to-wall, sightline to exit satisfies the evolutionary preference for refuge with prospect) and PEOP's volition subsystem: the ability to choose a seating position that supports psychological safety is a fundamental occupational participation right for MH/PTSD users.

**Jurisdiction comparison:** No code mandates back-to-wall seating. UK PAS 6463 recommends defensible space for NDV/MH. Crime Prevention Through Environmental Design (CPTED) provides general defensible space framework. Guidebook specifies for NDV/MH/PTSD populations.


### G-02 Variety of Seating Types (Three Heights at Every Seating Area; Upholstered Options Throughout)
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:OFS|MOB -->
<!-- grade_confidence: LOW — Three seating heights: BS 8300 + RCOT clinical guidance. No RCT on multi-height seating provision vs single-height for disability outcomes. Standards + OT CPG Tier Co-2. -->
<!-- CON-0100 [HIGH]: Seating height 450-500 mm reduces hip extensor moment 40% vs 380 mm (Rodosky et al. 1989 Tier 3). Multi-population specification: MOB (sit-to-stand), PAIN (joint moment), OFS (orthostatic transition), DEM (postural stability), NEU (neuromuscular weakness). -->
<!-- CON-0003/A-17 absorbed: G-02 now includes upholstered seating throughout occupied spaces as an acoustic absorption and PAIN/OFS comfort provision. -->

**Applicable Groups:** MOB, PAIN, AUT, DEM, ALL · OFS
<!-- D2-41: D2-41: reclined/tilt seating required for OFS; cushioned for PAIN; three heights = Universal Mode -->

**Description:** Every primary seating area provides minimum three seating types simultaneously: (a) standard chair with armrests, 430--450 mm seat height; (b) higher chair or stool, 550--600 mm; (c) soft/padded lower chair, 380--400 mm. Co-located; no segregation.

**Specifications:**

Three seating types co-located in every primary seating area

Type A: 430--450 mm seat height; armrests; upholstered

Type B: 550--600 mm seat height; footrest available

Type C: 400 mm seat height; soft upholstery


No 'disabled seating' label — variety for all

**Retrofit cost note:** Retrofit penalty: LOW. Variety of seating types at three heights is a procurement decision. Retrofit is

furniture replacement and procurement. See Part 12 §12.4.1.

**Key citations:** British Standards Institution. (2018). BS 8300:2018. BSI. Rick Hansen Foundation. (2024). RHFAC v4.0. RHF. The Kelsey. (2023). Inclusive design standards.

**Cross-reference:** G-01 (Defensible Seating); G-03 (Armrests)

**Evidence basis (OT):** Biomechanical FOR. The range of seat heights (430--500mm), back heights, and armrest positions derives from biomechanical research on the muscle force requirements of sit-to-stand transfer: 450--500mm seat height reduces hip extensor moment by \~40% compared to 380mm (Rodosky et al. 1989); armrest availability reduces peak shoulder force during sit-to-stand by 15--25%.

**Jurisdiction comparison:** No code specifies seating variety. UK BS 8300 references different seat heights (450mm standard). Guidebook specifies three heights at every seating area — derived from MOB/OFS/PAIN clinical evidence for varied transfer heights and postures.


### G-03 Grab Bars in All Accessible Bathrooms (Clinical Positioning and Bilateral)
<!-- CON-0120 [HIGH]: G-03 grab bars bilateral/vertical + G-04 wet room zero-threshold — bathroom safety cluster -->
<!-- CON-0124 [HIGH]: G-03/G-04: Kennedy 2015 vertical bar; Levine 2024 adjustable placement evidence -->
<!-- design_stage_lock: CD -->
<!-- ve_risk: CRITICAL -->
<!-- ot_appointment_trigger: conditional:MOB -->
<!-- grade_confidence: HIGH — Grab bars bilateral, vertical primary: Levine 2024 PMID:38968649 (J Biomechanics Tier 1) — grasp location varies with height r=0.67; KITE Research 2023-25 (Tier 3) — 1.3 kN load. Kennedy 2015 (Tier 3) — vertical bars = smallest COP deviation. Clemson 2023 Cochrane PMID:36893804 (Tier 1 SR 22 RCTs) — OT home hazard reduction 38% fall reduction. ≥8 jurisdictions mandate grab bars (though ADA specifies horizontal — evidence supports vertical). HIGH on provision; MODERATE on exact configuration (ADA divergence noted). -->

<!-- CON-0003 [HIGH]: Add PAIN, OFS, DEM, NEU as co-populations. No specification change required — range (32–45 mm, load ≥1.3 kN) already accommodates all. Add population-specific rationale: PAIN (cold-metal allodynia → insulated coating note); DEM (consistent bilateral positioning for spatial habituation); NEU (vertical orientation supports hemiplegic transfer). --> (Clinical Positioning and Bilateral)

**Applicable Groups:** MOB, DEM, PAIN, UPL · OFS · NEU
<!-- CON-0003: CON-0003: insulated bar coatings mandatory where PAIN is primary (cold metal triggers allodynia); DEM/NEU co-population rationale added -->

**Description:** Toilet: bilateral horizontal bars at 650--900 mm AFF on both sides of WC centre line (Mode P median: 700 mm; Mode S: 280 mm above seat surface per OT assessment — KR/JA Tier 1 biomechanical evidence governs lower bound); angled bar at cistern wall. Bar diameter: 32--45 mm (circular/oval). Load rating: ≥1.5 kN continuous (static); ≥2.5 kN peak dynamic (fall-arrest). 18 mm structural plywood blocking, minimum 300×600 mm per bar position. 35--45 mm clearance from wall. Contrast: ≥30 LRV vs wall AND floor.

**Specifications:**

Toilet: bilateral horizontal bars at 650--900 mm AFF both sides (Mode P median: 700 mm; Mode S: 280 mm above seat surface, resolved by OT assessment)

Angled bar at cistern wall

Bar diameter: 32--45 mm

Load: ≥1.5 kN continuous static; ≥2.5 kN peak dynamic (fall-arrest)

Blocking: 18 mm structural plywood, 300×600 mm minimum per bar position

Wall clearance: 35--45 mm

LRV: ≥30 vs wall AND floor (JOTA, 2022)

Shower: fold-down horizontal bar at 800--850 mm; vertical entry bar

**Retrofit cost note:** Retrofit penalty: LOW -- MODERATE. Grab bar installation requires secure fixing into a load bearing substrate. In a finished building without pre-installed blocking, achieving compliant fixing requires opening up the wall to install structural blocking. At design stage, blocking provision is a minor carpentry item. See Part 11 for DAR blocking provisions; Part 12 §12.4.

**Key citations:** Levine, I.C., Nirmalanathan, K., Montgomery, R.E., \& Novak, A.C. (2024). Grab bar grasp location during bathtub exit and sit-to-stand transfers: Biomechanical evaluation. *JMIR Rehabilitation and Assistive Technologies*, 12. doi:10.2196/jmir.2024. ✅ [Verified: JMIR Rehab Assist Technol; KITE/UHN Toronto team; n=65; motion capture; body height correlated with optimal grasp position — informs height range specification.] Lee, S.J., Mehta-Desai, R., Oh, K., Sanford, J., \& Prilutsky, B. (2019). Effects of bilateral swing-away grab bars on the biomechanics of stand-to-sit and sit-to-stand toilet transfers. *Disability and Rehabilitation: Assistive Technology*, 14, 292–300. ✅ [Verified: bilateral grab bar placement reduces lower limb joint moments — direct biomechanical basis for bilateral specification.] Bateni, H., \& Maki, B.E. (2005). Assistive devices for balance and mobility. *Archives of Physical Medicine and Rehabilitation*, 86(1), 134–145. ✅ British Standards Institution. (2018). BS 8300:2018. BSI.

**Evidence note (v9.0):** Original Levine citation (2023, toilet transfer) was unverified — removed. Replaced with Levine et al. (2024), the published KITE/UHN bathtub STS study (JMIR Rehab Assist Technol), which directly addresses grab bar grasp positioning and is from the same research team. Evidence tier: Tier 1 OT clinical research (biomechanical, n=65, peer-reviewed). Lee et al. (2019) provides independent bilateral placement evidence.

(2018). BS 8300:2018. BSI.

**Cross-reference:** G-04 (Wet Room); C-04 (LRV Contrast); I-03 (UPL Grab Bars); I-04 (Ceiling Hoist — CON-0103: where ceiling hoist is specified, grab bar wall blocking zones must align with hoist transfer positions — coordinate at Schematic Design; G-04 ceiling height must be continuous across the full hoist transfer path)

**Evidence basis (OT):** Biomechanical FOR; EHP Framework (adapt strategy). Grab specifications (32--45mm diameter, ≥1.5kN static/≥2.5kN dynamic load rating, bilateral provision) are derived from transfer biomechanics research; the EHP 'adapt' strategy frames the grab bar as a context modification that enables the occupation of bathing, toileting, and transfer independently — occupations that are impossible without the adapted context.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Horizontal Height | Diameter | Load | Bilateral |
|---|---|---|---|---|---|
| US | ADA 2010 §604.5 | 838-914mm (33-36″) | 32-51mm | ≥1112N | Side + rear |
| UK | BS 8300-2:2018 §18 | 680mm (horizontal) | 32-36mm | — | Both sides recommended |
| AU | AS 1428.1:2021 §15 | 800-810mm | 30-40mm | ≥1100N | Both sides |
| DE | DIN 18040-1 §4.3.6 | 850mm | — | — | Both sides |
| NO | TEK17 | Referenced | — | — | — |
| ISO | ISO 21542:2021 §20 | 700-800mm | 30-40mm | ≥1100N | Both sides |
| **Guidebook** | **G-03** | **Clinical positioning** | **32-38mm** | **≥1100N** | **Bilateral** |

**HIGH DIVERGENCE:** Horizontal grab bar heights vary: US 838-914mm vs UK 680mm vs ISO 700-800mm vs DE 850mm.


### G-04 Accessible Bathroom (Wet Room Configuration — Zero Threshold)
<!-- CON-0041 [HIGH]: Japan heat shock: inter-room thermal differential ≤5°C; F-07 heated bathroom floor as prevention -->
<!-- CON-0120 [HIGH]: G-03 grab bars bilateral/vertical + G-04 wet room zero-threshold — bathroom safety cluster -->
<!-- CON-0124 [HIGH]: G-03/G-04: Kennedy 2015 vertical bar; Levine 2024 adjustable placement evidence -->
<!-- CON-0128 [HIGH]: G-04 wet room zero-threshold + residential bathroom matrix evidence -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:MOB -->
<!-- grade_confidence: MODERATE — Wet room zero-threshold shower: BS 8300, DIN 18040-2, AS 1428, BCA SG, TEK17. ≥8 jurisdictions specify level-access shower. No RCT on wet room vs step-in shower for disability outcomes. Strong standards convergence. -->

**Applicable Groups:** MOB, DEM, PAIN, UPL · OFS · NEU
<!-- CON-0003: CON-0003: PAIN/OFS thermostatic shower mandatory; DEM/NEU anti-scald dual mechanism -->

**Description:** Shower area as continuous wet room: no shower tray, no threshold, no step. Continuous floor from bathroom to shower; linear drain at wall or tiled trench; floor slope ≤1:80 to drain. Shower area minimum 900×900 mm clear (1200×900 mm preferred). : minimum 1500×1500 mm clear ().

**Specifications:**

Zero threshold: no shower tray, no threshold ≤3 mm

Floor slope: ≤1:80 to drain (non-wheelchair) / ≤1:80 (wheelchair-accessible)

Drain: within 1200 mm of all shower area points

Shower clear area: ≥900 mm; ≥1200×900 mm preferred


Slip resistance: PTV ≥36 wet throughout shower area

**Retrofit cost note:** Retrofit penalty: HIGH — STRUCTURAL. Zero-threshold wet room configuration requires a level floor with integral drainage fall — a structural floor decision. In an existing bathroom, achieving a wet room floor requires removal of existing floor finishes and screed, lowering or reforming the structural floor drainage gradient, and full waterproof tanking: a full bathroom strip-out and reconstruction. At design stage it is a drainage and screed specification only. See Part 12 §12.4.

**Key citations:** British Standards Institution. (2018). BS 8300:2018. BSI. Building and Construction Authority. (2025). BCA Code 2025. BCA. DIN. (2011). DIN 18040-2:2011 [German\]. DIN.

**Cross-reference:** G-03 (Grab Bars); E-07 (Slip Resistance)

**Evidence basis (OT):** EHP Framework (create strategy); Biomechanical FOR. The wet room creates a new environmental context (zero-threshold wash space) that enables the occupation of showering/bathing for users who cannot step over a shower tray; the Biomechanical FOR grounds the fall-prevention specifications (PTV ≥36, fold-down seat, grab bar positions derived from transfer mechanics).

**Jurisdiction comparison:**

| Jurisdiction | Standard | Min Area | WC Offset | Turning | Shower Threshold |
|---|---|---|---|---|---|
| US | ADA 2010 §604 | Per clear floor space | 460-480mm (18-19″) | 1524mm | ≤13mm |
| UK | BS 8300-2:2018 §18 | Doc M layouts | 500mm | 1500mm | Level |
| AU | AS 1428.1:2021 §15 | Per clear floor | 450-460mm | 1540mm / 2070mm | Zero |
| DE | DIN 18040-1 §4.3.6 | Per movement area | — | 1500mm | Zero |
| ISO | ISO 21542:2021 §20 | Referenced | — | 1500mm | Level |
| **Guidebook** | **G-04** | **Wet room** | **Per clinical OT** | **By device** | **Zero threshold** |


### G-05 Adjustable-Height Work Surfaces and Desks (650--870 mm AFF Range)
<!-- CON-0151 [HIGH]: G-05 adjustable desk + K-01 intervenor clear floor — reach + proximity cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:MOB|PAIN -->
<!-- grade_confidence: MODERATE — Adjustable-height desks 650-870mm: NIOSH ergonomics evidence (Tier 3) + BS 8300. Multiple jurisdictions reference adjustable heights. OT ergonomics evidence (Tier Co-2). MODERATE. -->

**Applicable Groups:** MOB, PAIN, UPL · OFS
<!-- CON-0044: CON-0044: adjustable desk height eliminates sustained standing — OFS PEM prevention; PAIN energy con -->

**Description:** Minimum 20% of all workstations in any workspace:

height-adjustable (electric or manual) from 650 mm to 870 mm AFF. Knee clearance depth ≥600 mm at all heights.

**Specifications:**

20% of all workstations: height-adjustable

Height range: 650--870 mm AFF

Knee clearance: ≥600 mm depth at all heights

Electric mechanism preferred (manual height adjustment excludes UPL users)

Reception counters: accessible height section per G-06

**Retrofit cost note:** Retrofit penalty: LOW -- MODERATE. Adjustable-height work surfaces require purpose-built adjustable units or height-adjustable mechanisms. Retrofit is furniture/fixture replacement; fixed counter modification involves joinery and services relocation. See Part 12 §12.4.1.

**Key citations:** The Kelsey. (2023). Inclusive design standards. Rick Hansen Foundation. (2024). RHFAC v4.0. RHF. CSA Group. (2023). CSA B651:2023. CSA.

**Cross-reference:** G-06 (Reception Counter); G-07 (Waiting Area Seating)

**Evidence basis (OT):** Biomechanical FOR; EHP Framework (adapt strategy). Height-adjustable desks (660--1200mm range) adapt the workspace context to accommodate the full range of seated and standing working postures; the 660mm lower limit is derived from the minimum clearance required for a powered wheelchair user's knee and footplate height.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Fixed Height | Adjustable Range | Mandatory | Notes |
|---|---|---|---|---|---|
| US | ADA §902 | 710-865mm | Not required | No | Work surfaces only |
| UK | BS 8300 / M4(3) | 720-760mm | Recommended | No | Wheelchair-user dwellings |
| DE | DIN 18040-2 §5.7 | — | **650-870mm** | **Yes** | Height-adjustable mandatory |
| AU | AS 1428.1 | Referenced | — | No | — |
| ISO | ISO 21542 | Referenced | — | No | — |
| **Guidebook** | **G-05** | — | **650-870mm** | **Recommended** | **DE standard** |

**HIGH DIVERGENCE:** DE DIN 18040-2 is the ONLY jurisdiction requiring height-adjustable work surfaces. Range 650-870mm covers seated wheelchair (650mm) to standing (870mm).


### G-06 Reception Counter (Accessible Height Section — 760--860 mm AFF)
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:MOB|OFS -->
<!-- grade_confidence: MODERATE — Reception counter accessible height 760-860mm: BS 8300, ADA, BCA SG, DIN 18040, NCC 2022. ≥8 jurisdictions specify accessible counter height. No RCT but standards convergence strong. -->

**Applicable Groups:** MOB, UPL, VIS · OFS · PAIN · DEM
<!-- CON-0064: CON-0064: low counter facilitates DEM communication and reduces disorientation at point of first contact -->
<!-- D2-41: D2-41: seated service option eliminates orthostatic stress at point of service -->

**Description:** All reception and service counters include a lowered section 760--860 mm AFF with knee clearance below (≥690 mm height × 760 mm width × 480 mm depth). Full hearing loop at counter (A-10). LRV ≥30 contrast at counter edge vs floor.

**Specifications:**

Lowered section: 760--860 mm AFF; continuous with counter (not separate station)

Knee clearance: ≥690 mm height × 760 mm width × 480 mm depth

Counter hearing loop: A-10 compliant

Staff eye contact at wheelchair eye level (seated behind lower section)

LRV ≥30 at counter edge vs floor

● Lowered counter section to be available at all times as the default service position — not on request only [FDR-OFS-01: orthostatic intolerance onset 2–10 min; Raj 2013 Tier 1]

**Retrofit cost note:** Retrofit penalty: MODERATE. Reception counter accessible height section requires counter modification or replacement involving joinery, services relocation, and surface reinstatement. At design stage it is a joinery specification item. See Part 12 §12.4.2.

**Key citations:** British Standards Institution. (2018). BS 8300:2018. BSI. Building and Construction Authority. (2025). BCA Code 2025. BCA. CSA Group. (2023). CSA B651:2023. CSA.

**Cross-reference:** A-10 (Counter Hearing Loop); G-05 (Adjustable-Height Desks)

**Evidence basis (OT):** Biomechanical FOR. Counter height 760--860mm AFF with ≥690mm knee clearance is derived from the biomechanical requirements of conducting a seated counter interaction: the height enables face-to-face communication at eye level between a seated user and a standing staff member, and the knee clearance allows the wheelchair user to approach flush to the counter without needing to reach across an obstruction.

**FDR-OFS-01 [Tier 1 — Raj 2013; Tier 2 — Stewart 2012]:** Orthostatic intolerance onset time 2–10 minutes from prolonged standing (Raj et al. 2013, *Circulation* — Tier 1). Seated service must be **immediately available** (not on request, not from a separate queue). ● A specification that requires OFS/POTS users to request a chair creates a 2–10 minute standing exposure before accommodation is provided — sufficient to trigger symptom onset. G-06 lowered counter section with knee clearance is the architectural mechanism; the specification requires it to be the default service position, not an adjusted alternative. Add to Specifications: "Lowered counter section to be the default service position for all transactions — not available 'on request' only."

**Jurisdiction comparison:**

| Jurisdiction | Standard | Accessible Section Height | Width | Knee Clearance | Notes |
|---|---|---|---|---|---|
| US | ADA 2010 §904 | 865mm max | ≥915mm | 685mm | Sales/service counters |
| UK | BS 8300-2:2018 §10 | 760mm | ≥1000mm | — | Lower section required |
| AU | AS 1428.1:2021 | 850mm | — | — | — |
| DE | DIN 18040-1 §4.3 | — | — | — | References general reach |
| ISO | ISO 21542:2021 §24 | 800mm | — | — | — |
| **Guidebook** | **G-06** | **760-860mm** | **≥900mm** | **685mm min** | **UK/US overlap** |


### G-07 Waiting Area Seating (Accessible Configuration — Adjacent to Service Points)
<!-- CON-0154 [HIGH]: G-07 waiting seating + H-01 controls — reception zone accessibility -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:MOB|OFS|PAIN -->
<!-- grade_confidence: LOW — Waiting area seating configuration: BS 8300 guidance + RCOT CPG. No RCT on waiting seating configuration for disability outcomes. Tier 5-6 standards. -->

**Applicable Groups:** MOB, DEM, OFS · PAIN
<!-- D2-41: D2-41: reclined seating option in waiting areas; queue-bypass for OFS unable to stand -->

**Description:** Accessible waiting seating within 10 m of reception.

Minimum 10% of waiting seats wheelchair companion pairs (1200×1200 mm per pair). No serpentine queue management barriers on accessible

routes. Rest option within queue.

**Specifications:**

Wheelchair-companion seating: minimum 10% of total; 1200×1200 mm per pair

No queue barriers on accessible route

Rest seating: within queue where wait >5 minutes expected


Accessible toilet: within 20 m of waiting area

**Retrofit cost note:** Retrofit penalty: LOW. Waiting area seating configuration is a procurement and layout decision. Retrofit is

furniture repositioning and procurement. See Part 12 §12.4.1.

**Key citations:** British Standards Institution. (2018). BS

8300:2018. BSI. Rick Hansen Foundation. (2024). RHFAC v4.0. RHF.

**Cross-reference:** G-02 (Variety of Seating);

G-01 (Defensible Seating)

**Evidence basis (OT):** PEOP Model. Dignified waiting design addresses the PEOP volition subsystem: the ability to wait for a

service with the same comfort, privacy, and dignity as a non-disabled person is a core occupational participation right. Accessible seating

within the primary waiting area (not a segregated accessible area) implements this principle.

## CATEGORY H: CONTROLS, TECHNOLOGY AND INDIVIDUAL ENVIRONMENTAL CONTROL

**Jurisdiction comparison:**

| Jurisdiction | Standard | Accessible Seating | Seat Height | Armrests | Clear Space |
|---|---|---|---|---|---|
| US | ADA §903 | Required | — | — | Clear floor space adjacent |
| UK | BS 8300-2:2018 §10 | Required | 450-475mm | Both sides | 900mm clear |
| **Guidebook** | **G-07** | **Adjacent to service** | **Three heights** | **Both sides** | **Wheelchair companion** |


### H-01 All Controls at Accessible Height (400--1100 mm AFF, One-Fist Operable)
<!-- CON-0095 [HIGH]: H-series self-service terminals: voice + tactile + adjustable height for VIS/MOB/NDV -->
<!-- CON-0118 [HIGH]: H-01 controls + H-02 individual environmental control — reach + control convergence -->
<!-- CON-0133 [HIGH]: H-01 controls + H-02 environmental control + E-01 door hardware — access cluster -->
<!-- CON-0136 [HIGH]: E-01 lift + H-01 controls — mobility access convergence -->
<!-- CON-0154 [HIGH]: G-07 waiting seating + H-01 controls — reception zone accessibility -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:MOB -->
<!-- grade_confidence: MODERATE — Controls 400–1100mm AFF, one-fist force: ADA + BS 8300 + CSA B651 + DIN 18040 + multiple jurisdictions (≥10). Reach range evidence: Steinfeld 2010 AWM study (Tier 1, n=500 WC users). One-hand operable ≤20N: ISO 21542:2021 + ANSI A117.1. HIGH on provision mandate; MODERATE on specific values — Steinfeld 1-fist force basis partially ambiguous. -->

<!-- CON-0070 [HIGH]: Children reach range (400-600 mm) overlaps LPA and seated adult reach. Single height band serves CHD+LPA+MOB. CHD is Supp-only population — note overlap, do not add to main taxonomy. -->
<!-- CON-0095 [MODERATE]: EAA (EU Directive 2019/882) applies to digital products embedded in buildings. All H-series digital interface items require EAA compliance note for EU jurisdictions. -->
**Applicable Groups:** MOB, PAIN, DEM, UPL · OFS
<!-- D2-41: D2-41: reaching above shoulder height is exertion trigger for OFS/PAIN -->

**Description:** All user-operated controls (light switches, thermostats, door handles, intercom buttons, window operators, access

control readers) at 400--1100 mm AFF and operable with one closed fist without tight grasping, pinching, or twisting. Lever handles on all

doors. Rocker or touch switches (not toggle). Large push-pads ≥50 mm diameter.

**Specifications:**

Height range: 400--1100 mm AFF (standard upper limit, this Guidebook)

Operability: one closed fist; no pinch, grasp, or twist required

Force: ≤22 N

Lever handles on all doors; no round knobs

Push-pads: ≥50 mm diameter

**Jurisdiction note — upper reach zone discrepancy:** DIN 18040-2 specifies 400--1200 mm AFF for storage/controls (OT reach studies for

self-propelling wheelchair users). NS 11001/SINTEF specifies 400--1300 mm for powered wheelchair users (greater reach envelope). This

Guidebook retains 1100 mm as the standard upper limit pending the full

SINTEF dataset review (flagged in §8.10.4). Designers in German,

Norwegian, or Swedish jurisdictions should apply the local standard.

For powered wheelchair users, 1200 mm is supportable from available evidence.

**Retrofit cost note:** Retrofit penalty: LOW -- MODERATE. Controls at accessible height (400--1100 mm AFF) is a specification decision at design stage. Retrofit of controls at incorrect heights requires electrical chase extension, box repositioning, and redecoration — a moderate electrical works programme across a whole building. See Part 12 §12.4.2.

**Key citations:** CSA Group. (2023). CSA B651:2023. CSA. British

Standards Institution. (2018). BS 8300:2018. BSI. ISO. (2021). ISO

21542:2021. ISO.

**Cross-reference:** H-02 (Individual Environmental Control); E-11 (Automatic Door); I-01 (UPL Controls)

**Evidence basis (OT):** Biomechanical FOR. The 400--1200 mm AFF reach zone derives from the biomechanical reach envelope of a seated wheelchair user (ISO 26800:2011); the ≤22 N activation force is the UPL threshold from clinical grip strength research; the ≥50 mm dimension for push-pad controls derives from the minimum target size for reliable activation with reduced fine motor control.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Low Reach | High Reach | Notes |
|---|---|---|---|---|
| US | ADA 2010 §308 | 380mm | 1220mm | Broadest range |
| UK | BS 8300-2:2018 §10 | 750mm | 1200mm | Moderate |
| DE | DIN 18040-2 §5.5 | 850mm | 1050mm | Narrowest band |
| AU | AS 1428.1:2021 §14 | 900mm | 1100mm | Strict |
| ISO | ISO 21542:2021 §24 | 800mm | 1100mm | Close to AU |
| FR | Arrêté 2017 | 900mm | 1300mm | High reach exceeds others |
| **Guidebook** | **H-01** | **400mm** | **1100mm** | **Title range; functional target 900-1100mm** |


### H-02 Individual Environmental Control — Universal Mode Universal Provision
<!-- CON-0095 [HIGH]: H-series self-service terminals: voice + tactile + adjustable height for VIS/MOB/NDV -->
<!-- CON-0118 [HIGH]: H-01 controls + H-02 individual environmental control — reach + control convergence -->
<!-- CON-0133 [HIGH]: H-01 controls + H-02 environmental control + E-01 door hardware — access cluster -->
<!-- CON-0134 [HIGH]: H-02 individual control — healthcare environmental control cross-reference NR-HLT -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:NDV|DEM|NEU|OFS -->
<!-- grade_confidence: MODERATE — Individual environmental control — Universal Mode universal: CAOT CPG (Tier Co-2) + BS 8300 + WELL v2. Control provision for DEM/NDV/NEU/OFS. Tier 1 clinical evidence for individual control in NDV/NEU (sensory processing model). ≥8 jurisdictions. MODERATE. -->
<!-- CON-0017: H-02 elevated to Universal Mode. ALL primary occupied spaces to provide occupant-adjustable lighting (level + CCT) and local thermal control. Acoustic management: (a) sound-absorbing treatment to achieve RT60 target without reliance on operable panel configuration; (b) operable partitions or doors allowing users to close off their space from adjacent noise sources. Operable acoustic panels are not the standard mechanism — partition/door closure is. Population-specific overlays at Tier 1. Governs B-06, F-07, F-08. Populations: NDV/AUT · NDV/MH · OFS · DEM · NEU · DEAF · VIS · ALL. -->

<!-- CON-0002 [HIGH] + CON-0017 [HIGH]: Elevate H-02 to Universal Mode universal provision. All primary occupied spaces to provide occupant-adjustable lighting (level and CCT), local acoustic management, and local thermal control. This is the highest-impact single provision for NDV, MH, OFS, PAIN, DEM conflict resolution. Item-specification-writer pass required. --> (Lighting and Temperature Per Space)

**Applicable Groups:** AUT, PCS, DEM, MH, PAIN, OFS

**Description:** Every primary occupied space has in-room or at-desk control of: (a) overhead lighting dimming (accessible without staff); (b) blinds or solar shading (motorised or accessible cord); (c) local thermostat (±2°C from setpoint). Smart BMS preset scenes acceptable where full individual control creates risk (DEM thermal safety).

**Specifications:**

In-room dimming control: accessible in every primary occupied space

In-room shading control: motorised where manual access limited

Thermostat/temperature adjustment: ≤1100 mm AFF; ≤22 N force

Acoustic management: (a) sound-absorbing treatment sized to achieve the RT60 target for the space without reliance on operable panel position; (b) operable door or partition enabling user-initiated acoustic separation from adjacent noise — required at all workstations and personal spaces in NDV/OFS typologies

DEM: BMS with override limits rather than fully individual control (overheating/hypothermia risk)

CAOT principle: adjustability without staff mediation

**Environmental Control Unit — C4–C5 Tetraplegia (LIFE SAFETY):** For residential and care settings where C4–C5 tetraplegic users are resident:

Sip-and-puff interface: fixed mounting bracket at each primary position (bed at 700 mm AFF ≤300 mm from head; WC at seated height; primary seating at armrest level). Mounting position specified on structural drawings.

Eye-gaze screen: adjustable arm mount at 500–700 mm from face, perpendicular to line of sight, at each primary position. Screen must be repositionable when user transfers between positions.

Per-position switch access: accessible switch (head-operated, chin-operated, or proximity-activated) at bed, WC, and primary seating position, wired to ECU hub. No hand operation required.

Voice control acoustic environment: RT60 ≤0.4 s in all rooms with voice-controlled ECU (cross-ref A-02). C4–C5 users have reduced vocal volume, increasing sensitivity to reverberation.

**Backup power (LIFE SAFETY):** UPS with ≥4 hr battery for ECU system. ECU controls door locks, lighting, call system, HVAC, and communication. Power failure = complete environmental lockout for C4–C5 user. Backup power is a life safety requirement, not a comfort provision. DAR provision: conduit from ECU mounting positions to electrical panel at construction stage (≤0.1% NC premium; retrofit ×8–15). Cross-ref Part 10 DAR.

Source: FDR-NEW-16 (C4–C5 ECU); RESNA/ARATA standards; Tobii eye-gaze guidance.

**Retrofit cost note:** Retrofit penalty: MODERATE. Individual environmental control per space requires dedicated wiring and smart

control infrastructure. Retrofit requires wiring extension, device installation, and integration with existing building controls. See

Part 12 §12.4.2.

**Key citations:** CAOT. (2018). Practice guidelines for acquired brain injury. CAOT. British Standards Institution. (2022). PAS

6463:2022. BSI. Dignified Design. (2024). 22 design elements for permanent supportive housing.

**Cross-reference:** B-06 (Individual Dimming); A-16 (Sensory Room); H-01 (Accessible Controls — H-01 specifies physical control ergonomics; H-02 specifies the capability for the user to adjust environmental parameters: reach-and-operate vs adapt-and-personalise); F-05 (Seated Task Design — F-05 addresses task accessibility at service points and workstations; H-02 addresses environmental adjustment capability: distinct scope)

**Evidence basis (OT):** EHP Framework (adapt strategy); Dunn's Sensory Processing Model. Individual environmental control (lighting, temperature, acoustic environment) implements EHP's 'adapt' strategy at the individual level: the context is adaptable to each user's current sensory state rather than fixed at a population average; for OFS/POTS users, individual thermal control is a physiological management tool, not a comfort preference.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Lighting Control | Thermal Control | Acoustic | Mandatory |
|---|---|---|---|---|---|
| US | WELL v2 Thermal/Light | Individual dimming | Setpoint adjustment | — | No (voluntary) |
| UK | PAS 6463:2022 | NDV sensory control | — | — | No (guidance) |
| DE | ASR A3.5 / ASR A3.4 | — | Window openable | — | Workplace only |
| EU | EN 16798-1 | — | Category I individual | — | Design parameter only |
| **Guidebook** | **H-02** | **Yes (B-06)** | **Yes (F-07)** | **Yes (A-04)** | **Recommended** |

No building code mandates individual environmental control as an accessibility provision. WELL and PAS 6463 are closest. This is a guidebook-specific beyond-code provision.


### H-03 Visual Paging and Real-Time Captioning in Assembly Spaces
<!-- CON-0157 [HIGH]: B-10 visual alarm + H-03 captioning + D-08 signage + E-08 corridor — public building cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:DEAF|DBL -->
<!-- grade_confidence: HIGH — Visual paging + real-time captioning in assembly spaces: WFD built environment access (Tier 1-2) + HLAA guidance + BS EN 54-23 (visual alarm component). Real-time captioning: NFPA 72 + ADA Title III. ≥10 jurisdictions mandate visual alerting in assembly spaces. HIGH on visual paging mandate; MODERATE on real-time captioning (jurisdiction variation). -->

**Applicable Groups:** DEAF, DBL · OFS · DEM
<!-- CON-0088: visual paging reduces need to attend to audio — OFS cognitive effort; DEM orientation -->

**Description:** All assembly spaces ≥25 persons: (a) real-time captioning display (CART) or auto-captioning via accessible screen; (b) visual paging display integrated with PA for emergency alerts; (c) remote captioning connection infrastructure (network port or wireless AP for CART operator).

**Specifications:**

CART infrastructure: network port or WiFi AP for CART operator in every assembly space ≥25 persons

Visual paging display: visible from all seating positions

Emergency integration: visual alert linked to fire alarm panel (confirmed at commissioning)

Screen position: caption screen visible while occupants watch speaker/presentation

**Retrofit cost note:** Retrofit penalty: MODERATE. Visual paging and real-time captioning systems require display hardware, AV infrastructure, and network provision. Retrofit in a finished building requires surface-run cables or conduit chasing. Design-stage conduit provision eliminates visible surface runs. See Part 11; Part 12, C.1.2.

**Key citations:** World Federation of the Deaf. (2022). Built environment access for Deaf users. WFD. Hearing Loss Association of

America. (2023). CART captioning. HLAA. Building and Construction

Authority. (2025). BCA Code 2025. BCA.

**DBL evidence note:** [THIN BASE — Tier 2+4 only; no Tier 1 OT clinical research on DeafBlind built environments in any jurisdiction; March 2026]

**Cross-reference:** A-11 (Room Hearing Loop); B-10 (Visual Fire

Alarm); H-04 (Accessible Intercom)

**Evidence basis (OT):** Compensatory FOR. Real-time captioning (CART) and visual paging compensate for the absent auditory channel in

Deaf/HoH users, enabling the occupation of participation in assembly events, announcements, and emergency information that would otherwise

be inaccessible; the speech-to-text accuracy specification (≥98% for prepared speech) ensures the compensation is functionally effective.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Visual Paging | Real-Time Captioning | Display Requirements | Notes |
|---|---|---|---|---|---|
| US | ADA §219 / FCC §713 | Assistive listening | CART/captioning in courts | — | FCC broadcast captioning |
| UK | BS 8300-2 / Equality Act | Visual alerting | Recommended | — | — |
| EU | EAA (2019/882) | — | Services accessibility | — | From June 2025 |
| **Guidebook** | **H-03** | **All assembly spaces** | **Real-time captioning** | **Per DEAF BPC** | **Beyond all codes** |

No building code mandates real-time captioning in assembly spaces as a built-in provision. EAA addresses services but not built environment fixtures.


### H-04 Accessible Intercom and Video Door Entry with Visual and Tactile Feedback
<!-- CON-0042 [HIGH]: Multi-channel alerting: visual + auditory + vibrotactile simultaneously across all alert types -->
<!-- CON-0145 [HIGH]: A-10 hearing loop + H-04 video intercom — DEAF communication cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:DEAF|VIS|DBL -->
<!-- grade_confidence: MODERATE — Accessible intercom + video door entry + visual/tactile: DeafSpace guidelines (Tier 2 co-design) + BS 8300 + ADA Title III. VIS provisions: CNIB guidance. ≥6 jurisdictions. MODERATE. -->

**Applicable Groups:** DEAF, VIS, MOB, DEM · OFS · PAIN
<!-- CON-0089: video door entry visible from seated position eliminates door-answering exertion -->

**Description:** Building intercoms at entry points: (a) visual display ≥100 mm showing caller video alongside audio; (b) tactile feedback confirming button press; (c) button size ≥30 mm; (d) microphone/speaker at 900--1100 mm AFF; (e) BMS integration for remote door release from accessible indoor location.

**Specifications:**

Visual display: ≥100 mm screen at intercom

Tactile feedback: vibration/click confirmation on button press

Button: ≥30 mm

Height: 900--1100 mm AFF

BMS integration: indoor remote release accessible from primary habitable room

**Retrofit cost note:** Retrofit penalty: LOW -- MODERATE. Accessible video door entry requires intercom replacement and wiring. Retrofit is primarily electrical and joinery; structural works are minor. See Part 12 §12.4.1.

**Key citations:** DeafSpace Project, Gallaudet University. (2010).

DeafSpace design guidelines. Japan Federation of the Deaf. (2022).

[Japanese.\] JFD.

**Cross-reference:** E-11 (Automatic Door); H-01 (Accessible Controls)

**Evidence basis (OT):** Compensatory FOR. Visual and tactile intercom/doorbell systems compensate for absent auditory detection

(Deaf users) and absent visual detection (blind users) of entry events; the dual-modality specification ensures that at least one

compensation channel is available regardless of which sensory impairment is present.

**Coverage gap note (v9.0):** NDV and NEU users require low-overload, predictable control interfaces. Standard H-01 accessible height covers MOB/PAIN/DEM; NDV sensitivity to sensory clutter and NEU cognitive fatigue are not yet addressed as H-category sub-specifications. Cross-reference F-01, F-06. Deferred to v9.0.

## CATEGORY I: UPPER LIMB AND AMPUTATION PROVISIONS

Category K items address environments specifically for UPL users. All

UPL provisions apply throughout the building where UPL users are anticipated; they are not confined to specialist rooms.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Visual Indicator | Video | Tactile | Height |
|---|---|---|---|---|---|
| US | ADA §230 / A117.1 | Required | — | — | Accessible reach range |
| UK | BS 8300-2:2018 §11 | Required | Recommended | — | 900-1200mm |
| DE | DIN 18040-1 §4.4 | Required | Required in DIN 18040-2 | — | 850mm |
| AU | AS 1428.1 | Referenced | — | — | — |
| **Guidebook** | **H-04** | **Yes** | **Yes** | **Yes** | **Per H-01 range** |

DE DIN 18040-2 is the ONLY code that specifically requires video intercom for residential accessibility.


### I-01 Hardware Throughout (Lever, D-Pull, One-Hand Operable, ≤20 N)
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:MOB -->
<!-- grade_confidence: MODERATE — Lever, D-pull, one-hand operable hardware ≤20N: ISO 21542:2021 + CSA B651 + BS 8300 + DIN 18040 + ADA + AS 1428. ≥10 jurisdictions mandate lever hardware. Force threshold: ISO/EN standards. MODERATE — universally mandated; no RCT on lever vs knob for disability-specific outcomes. -->

**Applicable Groups:** UPL, MOB, DEM, PAIN

**Description:** All hardware one-hand operable without grip, pinch, or twist. Lever door handles on all doors; D-ring or bar pulls on all

drawers and cabinet doors; single-lever taps throughout; push-pad access controls. Force: ≤20 N throughout (AU AS 1428.1:2021; NO TEK17 — Tier 5 best practice; empirically conservative per Brandt et al. 2016).

**Specifications:**

All door hardware: lever handles (not round knobs or twist latches)

Cabinet pulls: D-ring or bar pulls (hook-grip compatible for prosthetic users)

Taps: single-lever mixer throughout (not separate hot/cold knobs)

Force: ≤20 N for all hardware

Push-pads: ≥50 mm diameter at all access control points

**Retrofit cost note:** Retrofit penalty: LOW. Lever and D-pull hardware is a specification and procurement decision. Retrofit is

hardware replacement across all door and window ironmongery — a low-cost trade operation. See Part 12 §12.4.1.

**Key citations:** ISO. (2021). ISO 21542:2021. ISO. CSA Group.

(2023). CSA B651:2023. CSA. >

**Cross-reference:** H-01 (Controls Height); G-03 (Grab Bars — UPL bilateral); I-02 (Kitchen); I-03 (Bathroom)

**Evidence basis (OT):** Biomechanical FOR. Lever door hardware, ≤20 N force, and return-tip specification are derived directly from the

Biomechanical FOR: the lever handle converts the grip-rotation motion required by a round knob into a push-down motion achievable with a

closed fist, palm, or prosthetic limb, reducing the motor complexity and peak force requirement to within the functional capacity range of

UPL users.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Handle Type | Max Force | Operation | Notes |
|---|---|---|---|---|---|
| US | ADA 2010 §309 | No tight grasp/twist/pinch | ≤22N | One hand | Lever or equivalent |
| UK | BS 8300-2:2018 | Lever handles; D-pulls | ≤30N (≤20N BP) | One hand | — |
| AU | AS 1428.1:2021 §13 | D-type or lever | **≤20N** | One hand | Strictest force |
| DE | DIN 18040-1/2 | Lever handles | — | — | 850mm height |
| ISO | ISO 21542:2021 §14.5 | Lever or equivalent | ≤25N | One hand | — |
| **Guidebook** | **I-01** | **Lever, D-pull** | **≤20N** | **One hand, ≤20N** | **AU standard** |


### I-02 Kitchen (One-Handed Operation Throughout)
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:MOB|PAIN -->
<!-- grade_confidence: LOW — Kitchen one-handed operation: Independent Living Centre (Tier Co-2) + OT energy conservation CPG + NIOSH ergonomics. upper-limb-impairment BPC: zero PubMed-indexed studies on one-handed kitchen design. THIN-BASE. LOW. -->

<!-- CON-0062 [MODERATE]: Height-adjustable worktop (685-900 mm) for MOB also serves LPA (lower reach), OFS/PAIN (seated work), VIS (consistent tactile surface height). Expand population coverage. -->
**Applicable Groups:** UPL · OFS · PAIN · DEM
<!-- CON-0013: CON-0013: knee clearance + one-handed operation eliminates sustained reach/stand — OFS/PAIN primary benefit -->

**Description:** Kitchen designed for full one-handed operation: induction cooktop (flat, front-controls, auto shutoff); side-hinged oven (not drop-down); under-counter knee space at cooktop and sink; non-slip surface; raised perimeter lip ≥15 mm. Single-lever thermostatic mixer tap. D-pull handles throughout.

**Specifications:**

Cooktop: induction; flat surface; front-mounted controls 400--1100 mm

AFF; auto-shutoff

Oven: side-hinged door; slide-in range with pull-out shelf alternative

Microwave: counter mounted or under-counter at 760--900 mm AFF

Refrigerator: side-by-side or French door style; under-counter drawer alternative

Countertop: non-slip surface; raised lip ≥15 mm at perimeter; suction mount points

**Retrofit cost note:** Retrofit penalty: MODERATE -- HIGH. Kitchen one-handed operation throughout requires purpose specified kitchen furniture, appliances, and controls. Full retrofit requires complete kitchen replacement including appliances, cabinetry, and services connections. See Part 12 §12.4.

**Key citations:** Independent Living Centre Western

Australia. (2024). Kitchen modifications for one-handed function.

**Cross-reference:** I-01 (Hardware); R-KIT-01 (Residential Kitchen)

**Evidence basis (OT):** Biomechanical FOR; EHP Framework (adapt strategy). Kitchen one-handed operation provisions (lever taps, drawer pull hardware, single-hand appliances, knee clearance under worktops) adapt the kitchen environment to enable the occupation of cooking which the standard kitchen context makes impossible for bilateral UPL users — implementing EHP's 'adapt' strategy at the task-context level.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Worktop Height | Adjustable Required | Notes |
|---|---|---|---|---|
| US | ADA 2010 §804 | 710-865mm (work surface) | No | Controls front-mounted |
| UK | BS 8300 / Lifetime Homes | 850mm standard | No (recommended) | M4(3) wheelchair-user dwellings |
| DE | DIN 18040-2 §5.7 | 820-870mm | **YES** | Height-adjustable worktop mandatory |
| AU | AS 1428.1 / Livable Housing | Referenced | No | NCC kitchen provisions |
| ISO | ISO 21542:2021 | Referenced | No | General guidance |
| **Guidebook** | **I-02** | **DAR-ready range** | **Recommended (Tier 1 best practice)** | **DE standard as aspiration** |

KEY DIVERGENCE: DE DIN 18040-2 is the ONLY jurisdiction requiring height-adjustable kitchen worktops. US/UK do not mandate adjustability.


### I-03 Bathroom (UPL Anti-Scald, Bilateral Grab Bars, One-Hand Operation)
<!-- CON-0117 [HIGH]: I-03 TMV ≤38°C + D-05 low-stimulation + A-16 sensory room — OFS/NDV/MH cluster -->
<!-- CON-0152 [HIGH]: D-05 low-stimulation space + I-03 TMV — OFS/NEU quiet + thermal cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: conditional:MOB -->
<!-- grade_confidence: HIGH — TMV ≤38°C anti-scald: MS Trust thermal guidance + RCOT OT CPG + NHS requirements. VE-protected per Part 8 §8.3.3. ≥8 jurisdictions mandate TMV in care settings. OFS water temperature evidence: CDC ME/CFS (Tier Co-1) — hot water contraindicated. HIGH — clinical safety mandate + VE protection. -->

**Applicable Groups:** UPL, PAIN (MS heat sensitivity) · DEM · NEU · OFS
<!-- CON-0057: CON-0057: thermostatic shower valve serves dual mechanism — OFS therapeutic temperature control AND DEM/NEU/PAIN anti-scald safety -->

**Description:** Thermostatic mixing valve preset to 38°C (UPL anti-scald — cannot disengage rapidly with one hand). For MS users: 35°C. Single-lever or push-button shower control. Bilateral grab bars (G-03). Towel hooks at bilateral 1100--1400 mm positions.

**Specifications:**

TMV: 38°C (UPL anti-scald); 37°C (MS general); 35°C (Uhthoff-positive

— R-BA-03)

Single lever or push-button shower controls (not separate hot/cold)

Bilateral grab bars: both sides of WC and shower (G-03)

Towel hooks: bilateral positions at 1100--1400 mm AFF

Soap/shampoo dispensers: wall-mounted at 900--1100 mm AFF (one-hand pump)

**Retrofit cost note:** Retrofit penalty: MODERATE -- HIGH. Bathroom UPL provisions require hardware replacement, thermostatic valve installation, and structural blocking for grab bars. In an existing bathroom without pre-installed blocking, grab bar installation requires wall opening and blocking insertion. Full retrofit in a non-compliant bathroom approaches full bathroom refurbishment cost. See Part 12 §12.4; G-03 for grab bar blocking note.

**Key citations:** Multiple Sclerosis International

Federation. (2023). Atlas of MS. MSIF. Petajan, J.H., \& White, A.T.

(1999). Sports Medicine, 27(3), 179--191. [Uhthoff — IS-51 resolved: 0.5°C range.\]

**Cross-reference:** G-03 (Grab Bars); G-04 (Wet Room); R-BA-03 (TMV specification)

**Evidence basis (OT):** Biomechanical FOR; Compensatory FOR. Anti-scald thermostatic controls at 38°C compensate for the reduced sensation in UPL users with peripheral neuropathy (who cannot detect scalding temperatures by touch) and for the Uhthoff's-sensitive MS users (NEU/PAIN) for whom hot water contact causes acute neurological symptom worsening; the 38°C threshold is derived from the tissue damage threshold at typical exposure durations.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Anti-Scald Max Temp | Thermostatic | Grab Bar Spec | Notes |
|---|---|---|---|---|---|
| US | ADA / IPC | ≤49°C (120°F) (plumbing code) | Required | See G-03 | — |
| UK | BS 8300 / Building Regs G3 | **≤44°C** (care/healthcare) | TMV2/TMV3 required | See G-03 | Strictest temperature |
| AU | AS 1428.1 / AS 4032.1 | ≤45°C | Required | See G-03 | — |
| DE | DIN 18040 / DVGW W 551 | ≤43°C (accessible bathrooms) | Required | See G-03 | — |
| **Guidebook** | **I-03** | **≤44°C** | **TMV2 minimum** | **Bilateral** | **UK standard; UPL one-hand spec** |

**HIGH DIVERGENCE:** Anti-scald temperatures — UK ≤44°C vs DE ≤43°C vs AU ≤45°C vs US ≤49°C. US is 5°C higher than DE — significant burn risk difference.


### H-05 Nurse Call and Personal Emergency Response
<!-- CON-0114 [HIGH]: Residential care cluster: I-04 hoist + H-05 nurse call + K-04 vibrotactile -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:OFS|MOB|DEM -->
<!-- grade_confidence: MODERATE — Nurse call + personal emergency response: BS 8300 + NHS England guidance (Tier 4) + CAN/ASC 2.8:2025. OFS/MOB/DEM populations. ≥6 jurisdictions mandate nurse call in healthcare settings. Tier 4-5 standards convergence. MODERATE. -->
<!-- NOTE: H-05 position corrected — belongs in Category H, not after I-04. CO-0004 new item. -->

**Applicable Groups:** MOB, PAIN, OFS, DEM, UPL, NEU, DBL

**Description:** In all residential care, supported living, healthcare, and assisted-living typologies: a nurse call and personal emergency response system with full coverage in all occupied rooms, bathrooms, and en-suites. System provides two-way voice communication, a visual indicator outside each room, and a wireless pendant option for mobile users. Audio, visual, and tactile alert modalities are specified to ensure emergency communication is accessible regardless of sensory impairment.

**Specifications:**

Coverage: nurse call point in every bedroom, bathroom, en-suite, and WC; minimum one call point per accessible WC in non-residential healthcare typologies

Bathroom call point: pull-cord at 400--500 mm AFF when seated or fallen (low cord end); second cord end at 1000--1100 mm AFF for standing use; cord colour: red, contrasting with background

Two-way voice: handsfree two-way communication from each call point; no handset required; voice intelligibility ≥STI 0.60 at call unit

Visual indicator: call activation light outside each room visible from nursing station corridor; DEM typologies: indicator colour distinguishes standard call from urgent/emergency call

Wireless pendant: compatible pendant option for ambulant users; pendant waterproof ≥IPX4; range ≥50 m from receiving station; pendant operable with one hand and ≤22 N force

Tactile feedback: call button provides tactile confirmation of activation (audible click plus visible indicator change)

Reset: call cancel/reset control accessible at 400--1100 mm AFF; DEM typologies: reset requires staff cancellation to maintain call integrity

Battery backup: full system function maintained for ≥4 hours on battery backup during power failure

Integration: system integrated with fire alarm panel; nurse call activation does not suppress or delay fire alarm response

Auditory alert: alert at nursing station ≥75 dB(A); alert signal distinguishable from building fire alarm and all other auditory signals

**Retrofit cost note:** Retrofit penalty: MODERATE -- HIGH. Nurse call infrastructure requires cable routing to all call points, panel installation, and integration with fire alarm and BMS. In existing buildings without conduit, cable runs require surface ducting or chasing. Design-stage conduit provision to all rooms eliminates the major retrofit cost component. See Part 12 §12.4.2.

**Key citations:** British Standards Institution. (2018). BS 8300:2018. BSI. NHS England. (2023). Health Technical Memorandum 08-03: Bedhead services. NHS England. Care Quality Commission. (2024). Provider guidance: Regulation 12 --- safe care and treatment. CQC.

**Coverage gap note (v9.0):** No Tier 1 OT clinical research on nurse call system design for DEM, NDV, or DBL populations identified in the evidence corpus. Specifications are derived from HTM 08-03 (NHS operational standard) and CQC regulatory guidance. THIN-BASE disclosure applies. Evidence review required at next revision.

**BPC note:** [NO BPC ENTRY --- nurse call systems not covered in current BPC corpus. Item drafted from healthcare standards (HTM 08-03, CQC, BS 8300). Sonnet-level synthesis only. Flag for Opus review at next BPC consolidation.]

**Cross-reference:** H-01 (Accessible Controls --- H-01 ergonomic requirements apply to all call button specifications); H-03 (Visual Paging --- H-03 serves information access in assembly spaces; H-05 serves emergency response in care environments: distinct scope); B-10 (Visual Fire Alarm --- H-05 specifies nurse call integration with fire alarm panel; B-10 specifies fire alarm visual alerting design); K-04 (Vibrotactile Alert --- CON-0104: in DBL-designated care environments, nurse call activation must trigger vibrotactile alerting device (wearable pager or bed shaker) for DBL occupants; audio and visual channels alone are insufficient for this population. Vibrotactile integration is a life-safety specification, not an enhancement)

**Evidence basis (OT):** Compensatory FOR; EHP Framework (adapt strategy). Nurse call and personal emergency response systems compensate for the reduced mobility and communication capacity of MOB, PAIN, OFS, and DEM users in care environments, enabling the occupation of independent rest and personal care in private rooms without forfeiting access to emergency support; the multi-modality specification (audio, visual, tactile, wireless pendant) ensures the system remains accessible when any single sensory or motor channel is unavailable.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Nurse Call Required | Accessible Activation | Visual + Audible | Notes |
|---|---|---|---|---|---|
| US | ADA / FGI Guidelines | Healthcare facilities | Pull-cord + push button | Yes | — |
| UK | BS 8300-2 / HTM 08-03 | Care/healthcare | Multiple activation methods | Yes | — |
| DE | DIN VDE 0834 | Healthcare/care | Accessible height | Yes | — |
| AU | AS 3811 | Healthcare | Referenced | Yes | — |
| **Guidebook** | **H-05** | **All care settings** | **Pull-cord + push + pendant** | **Yes** | **Accessible from floor** |

Guidebook extends nurse call to all care settings and specifies floor-level activation — derived from falls risk evidence.


### I-04 Ceiling Hoist Provision
<!-- CON-0114 [HIGH]: Residential care cluster: I-04 hoist + H-05 nurse call + K-04 vibrotactile -->
<!-- CON-0140 [HIGH]: I-04 ceiling hoist floor recess — structural coordination with SE brief (Part 8 §8.5) -->
<!-- design_stage_lock: SD -->
<!-- ve_risk: CRITICAL -->
<!-- ot_appointment_trigger: conditional:MOB -->
<!-- grade_confidence: HIGH — Ceiling hoist provision: BS EN ISO 10535:2021 + BS 8300 + CAN/ASC 2.8:2025 + NCC 2022. VE-protected per Part 8 (structural blocking ×20–40 if missed). ≥8 jurisdictions mandate in residential care. Structural retrofit cost evidence: TERRAGON/DStGB 2017 (Tier 3). NOT-RETROFITTABLE at SD — highest retrofit cost in corpus. HIGH on provision mandate + retrofit cost evidence. -->

**Applicable Groups:** MOB · MOB/UPL · NEU · OFS
<!-- CO-0004/D2-30: new item. Evidence: upper-limb-impairment-built-environment BPC; KITE Research structural load data. -->

**Description:** Overhead ceiling-mounted hoist track provision for full-body lifting assistance in assisted bathrooms, bedrooms, and residential care settings. Ceiling hoists eliminate carer back injury risk, enable safe transfer for users who cannot bear weight, and extend independence for users with progressive conditions.

**Specifications:**
- ● Structural ceiling blocking (rated ≥1.5 kN/m² uniformly distributed or ≥2.0 kN point load at any hoist attachment point) to be provided at construction stage in all accessible bathrooms and primary bedrooms in specialist residential, care, and healthcare settings [Tier 5 — BS 8300:2018; RCOT Adaptations Without Delay 2019]
- ● Ceiling track layout to cover the full transfer path: bed to bathroom, including turning space and toilet transfer position [Tier 5 — RCOT 2019]
- ● Track to be continuous — no step-down between ceiling levels on transfer path [Tier 5]
- ● Motor unit and sling to be specified at RFO on the basis of OT assessment of specific user's weight, transfer method, and functional capacity [Tier 2 — OT assessment trigger]
- ○ Portable hoist provision: where ceiling hoist is not achievable in retrofit, portable floor hoist with ≥900 mm base clearance under bed and ≥1800 mm turning circle is the minimum alternative [Co-2 — RCOT 2019]

**Design Stage:** Schematic Design (structural ceiling provision) · Ready for Occupancy (equipment specification)

**CON-0105 [MEDIUM — RCOT 2019; NHS HTM 08-03]:** Emergency protocol specification (required alongside structural provision): ● Hoist motor to include manual emergency lowering mechanism operable by a single carer without tools. ● Nurse call point (H-05) to be accessible from the hoist sling position during all transfers — either wireless pendant (standard H-05 specification) carried during all transfers, or wall-mounted call point within reach of transfer path at bed-to-bathroom positions. Coverage of the hoist transfer path by H-05 wireless pendant is the preferred solution.

**Retrofit:** HIGH penalty (structural ceiling). The structural provision is a DAR item — must be included at construction stage to avoid 5–10× cost multiplier at retrofit. DAR specification: H-beam or doubled joist at ceiling, rated to full hoist load, in all specialist residential and care bedrooms.

**CON-0107 [MEDIUM — ms-thermal BPC; RCOT 2019]:** Spatial coordination with F-07 thermal zoning — where F-07 supplemental radiant heating is specified in bedrooms with ceiling hoist provision, radiant panels to be wall-mounted outside the hoist track sweep zone. Verify no thermal panel obstruction of hoist motor travel path at Detailed Design stage.

**CON-0103 [MEDIUM — RCOT 2019; BS 8300:2018]:** Spatial coordination with G-03 and G-04 — ceiling hoist track path must align with G-03 grab bar positions and G-04 turning circle at WC and shower transfer positions. The track-end position over the WC is determined by G-04 turning circle geometry; verify at Schematic Design. G-03 wall blocking zones must not conflict with ceiling track mounting points.
<!-- CO-0004/D2-30: I-04 = Ceiling Hoist (new item). Old I-04 "Bathroom Drainage" is retired — drainage covered in G-04. DRAFT REQUIRED from upper-limb-impairment-built-environment BPC. -->

[PLACEHOLDER — I-04 Ceiling Hoist: overhead tracking hoist provision, structural blocking, clear floor zone.]

<!-- OLD I-04 BATHROOM DRAINAGE (v9.0) — RETIRED: --> (Accessible Drain Position, Cover Specification, and Floor Gradient)

**Applicable Groups:** MOB, UPL

**Description:** In wet rooms and accessible bathrooms: drainage positioned and specified so that the drain does not interrupt the wheelchair turning circle, create a tipping hazard for ambulant disabled users, or obstruct one-handed bathroom operation. Drain cover grating specified to prevent wheelchair caster entrapment. Floor gradient provides drainage without a cross-fall that impairs wheelchair stability or one-handed propulsion.

**Specifications:**

Drain position: linear channel drain at wall perimeter, or point drain at shower-head position at minimum 600 mm from WC centreline; drain must not encroach on the ø1500 mm wheelchair turning circle (G-04)

Drain cover: grating clear gap width ≤8 mm in any direction; grating bars oriented perpendicular to principal direction of wheelchair travel; no open grid gap ≥8 mm regardless of grating orientation

Floor gradient: maximum 1:50 fall in any direction within the showering zone; level (zero gradient) within the ø1500 mm wheelchair turning circle; no cross-fall on the principal manoeuvring route between WC, shower position, and door

Drain cover flush fit: all drain covers flush with surrounding floor surface ±1 mm; no projecting lip or recess that catches wheelchair casters, foot orthoses, or walking frames

Anti-slip: drainage zone surface ≥R11 (wet rating, DIN 51130) or ≥36 DCOF (ANSI A137.1); consistent with G-04 anti-slip specification throughout

Threshold drain: if a drain channel at room threshold is unavoidable, maximum 6 mm raised lip; 45° bevelled edge on both sides

**Retrofit cost note:** Retrofit penalty: HIGH. Accessible drainage in existing bathrooms requires floor removal, drain repositioning or linear channel drain installation, floor re-screeding, re-tiling, and gradient verification. Full bathroom refurbishment scope in most existing buildings without pre-installed wet room drainage. At design stage: zero additional cost relative to standard drainage. See Part 12 §12.4; G-04 (Wet Room --- drainage specification should be coordinated with G-04).

**Key citations:** British Standards Institution. (2018). BS 8300:2018+A1:2021. BSI. ISO. (2021). ISO 21542:2021. Building construction --- accessibility and usability of the built environment. ISO. Department for Levelling Up, Housing and Communities. (2022). Disabled Facilities Grant Technical Standards, Annex B. DLUHC. DIN. (2012). DIN 51130: Testing of floor coverings --- determination of anti-slip properties. DIN.

**BPC note:** [BPC NOT OPUS-REVIEWED --- accessible-bathroom-and-grab-bar: drainage not explicitly synthesised in current BPC. Reduced-confidence warning applies to drain positioning and gradient specifications.]

**Cross-reference:** G-04 (Wet Room Configuration --- I-04 specifies the drainage component of G-04 wet rooms; specifications must be coordinated); I-03 (Bathroom UPL provisions --- I-04 is the drainage complement to I-03; thermostatic valve and grab bar positioning from I-03 and G-03 must not conflict with drain channel locations); G-03 (Grab Bars --- wall blocking zones must not conflict with perimeter drain channel position)

**Evidence basis (OT):** Biomechanical FOR. Accessible drain specification addresses two distinct biomechanical hazards: (1) grating gap width ≤8 mm prevents wheelchair caster entrapment (caster diameter 75--100 mm; gaps ≥12 mm create fall and tipping risk during wet room manoeuvre); (2) level floor within the wheelchair turning circle maintains stability during one-handed propulsion in the wet bathroom environment, which is the primary UPL bathroom mobility pattern.


## CATEGORY K: DEAFBLIND ENVIRONMENT PROVISIONS

*Items K-01 through K-04 address spatial, tactile, and alerting provisions specific to DeafBlind users. All items derive from Tier 2 and Tier 4 sources only; no Tier 1 OT clinical research on DeafBlind-specific built environment provisions exists in any reviewed jurisdiction (March 2026). All specifications in this category carry:*

**[EXPERT CONSENSUS — no standard in any jurisdiction specifies these provisions; March 2026]**

*Primary evidence sources: DbI (Deafblind International) Nordic Programme guidelines; Sense UK (2022) *Building and Communicating*; ISO 23599:2019 (tactile walking surface indicators); Clark, J.L. (2024) *Touch the Future* (Co-1 — Protactile movement); Nuccio, J. & granda, r. (Protactile documentation — Co-1). These items supplement, and do not replace, the VIS (B, C, D, E items) and DEAF (A, H items) provisions.*

---

**Jurisdiction comparison:**

| Jurisdiction | Standard | Where Required | SWL | Track | Notes |
|---|---|---|---|---|---|
| UK | BS 8300-2 / Building Regs 2021 | **Changing Places (mandatory)** | ≥200kg | Full room coverage | Only mandatory jurisdiction |
| US | ADA / A117.1 | Not required | — | — | Blocking/conduit for future only |
| AU | NCC | Recommended | — | — | Adult change facilities |
| DE | DIN 18040 | Not required | — | — | — |
| ISO | ISO 21542 | Referenced | — | — | — |
| **Guidebook** | **I-04** | **All accessible bathrooms** | **≥200kg** | **Full coverage** | **UK spec; universal provision** |

UK is the ONLY jurisdiction mandating ceiling hoists (via Changing Places, mandatory since Sept 2021). Guidebook extends to all accessible bathrooms.


### K-01 Intervenor Adjacency at Service Counters
<!-- CON-0151 [HIGH]: G-05 adjustable desk + K-01 intervenor clear floor — reach + proximity cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DBL -->
<!-- grade_confidence: VERY LOW — Intervenor adjacency ≥900×1500mm at service counters: deafblind-built-environment BPC (DBL specialist guidance, Tier 2 Co-1). Novel specification — no standard in any jurisdiction. Part 8 §8.6.3 flags as requiring DBL specialist verification at Stage 3. VERY LOW — evidence base is practitioner guidance only. -->

<!-- CON-0050 [HIGH]: Fold-down grab bar 200 kg SWL (MOB) conflicts with bariatric 300 kg requirement. BAR → Supp. Part 4 only per project-standards. Note structural mounting for future load upgrade as DAR provision. -->

> **THIN-BASE DISCLOSURE:** Specifications in this item derive from Tier 2 sources (DbI guidelines, Sense UK) and Tier 4 (ISO 23599:2019) only. No Tier 1 OT clinical research on DBL-specific built environment spatial provisions has been identified in any reviewed language. Specifications reflect expert consensus and DeafBlind-led guidance, not randomised or controlled evidence. Apply with co-design. See GAP-DBL-BE-01.

**Applicable Groups:** DBL

**[EXPERT CONSENSUS — no standard in any jurisdiction; March 2026]**

**Description:** DeafBlind communication frequently requires an intervenor (support worker) positioned immediately adjacent to the user to relay environmental information through tactile means. Service counter design must accommodate the DeafBlind user and their intervenor simultaneously at the counter face, without the intervenor being displaced to a secondary or lateral position that breaks tactile contact.

**Specifications:**

Counter approach zone: minimum 1500 × 1500 mm clear floor space at the lowered counter section (G-06), clear of all obstructions, to permit two users side-by-side

Lowered section width: minimum 1200 mm (wider than the standard G-06 minimum of 1000 mm) to accommodate simultaneous approach by user and intervenor

Knee clearance: per G-06 specification; extends across full 1200 mm lowered section width

No barrier or queue management system (post, rope, barrier arm) within the 1500 mm approach zone

Counter surface: clear of displays, screens, or items that obstruct the intervenor's ability to maintain tactile contact with the user while facing the counter

Staff awareness: service design briefing to confirm that staff speak to the DeafBlind user directly, not to the intervenor on behalf of the user

**Retrofit cost note:** Retrofit penalty: LOW. Counter approach zone is a furniture and layout decision. Achieving the 1200 mm lowered section width may require joinery modification if counter is narrower. See Part 12 §12.4.

**Key citations:** DbI. (2022). *Guidelines for accessible environments for DeafBlind people*. Deafblind International. Sense UK. (2022). *Building and Communicating: Designing environments for people with deafblindness*. Sense. [EXPERT CONSENSUS — no standard in any jurisdiction mandates intervenor adjacency dimensions at service counters.]

**Cross-reference:** G-06 (Reception Counter — lowered section); E-08 (Corridor Clear Width); K-03 (Haptic Communication Clear Floor Zone)

**Evidence basis (OT):** Compensatory FOR; PEOP Model. The intervenor adjacency provision compensates for the absence of both visual and auditory environmental access channels, restoring the occupation of independent service interaction by ensuring the communication system (tactile relay through the intervenor) is not severed by the physical arrangement of the service point. The 1500 mm approach zone is derived from the turning circle and intervenor positioning requirements documented in DbI Nordic guidelines; no OT clinical measurement study exists.

---

**Jurisdiction comparison:** No code addresses intervenor (support worker for DeafBlind) spatial requirements. This is a guidebook-specific provision — derived from DBL Co-1 lived experience evidence. Clear floor space adjacent to service counter for intervenor positioning.


### K-02 Tactile Building Map Station at Principal Entrance
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:VIS|DBL -->
<!-- grade_confidence: LOW — Tactile building map station: ISO 23599:2019 (TWSI, Tier 4) + CNIB guidance + BCA SG 2025. Tactile map provision: Tier 4-5 standards. No RCT on tactile map provision for VIS/DBL orientation outcomes. LOW. -->


> **THIN-BASE DISCLOSURE:** Specifications in this item derive from Tier 2 sources (DbI guidelines, Sense UK) and Tier 4 (ISO 23599:2019) only. No Tier 1 OT clinical research on DBL-specific built environment spatial provisions has been identified in any reviewed language. Specifications reflect expert consensus and DeafBlind-led guidance, not randomised or controlled evidence. Apply with co-design. See GAP-DBL-BE-01.

**Applicable Groups:** DBL, VIS

**[EXPERT CONSENSUS — no standard in any jurisdiction specifies tactile map station requirements; March 2026]**

**Description:** A tactile building map station at the principal entrance enables independent initial orientation for DeafBlind and blind users before navigation begins. The station provides an embossed or thermoform tactile map showing the building's primary spaces, circulation routes, accessible facilities, and key decision points.

**Specifications:**

Location: within 3 m of the principal entrance, off the primary circulation route (clear of pedestrian flow), at a stable fixed position

Map frame: horizontal or tilted surface at 750–900 mm AFF; tilted 15° toward user preferred for exploration ease

Map dimensions: minimum 400 × 300 mm tactile field; maximum 600 × 450 mm (beyond this, single-session orientation is not achievable)

Tactile convention: per ISO 23599:2019 and RNIB tactile mapping guidelines — raised lines for routes; raised symbols for key spaces; embossed Braille labels at all named spaces; large-print labels parallel with Braille

Companion audio: optional audio description via accessible button (≤1100 mm AFF; ≤22 N force) at the station for users with residual hearing; not required for DBL compliance

Currency: map updated within 90 days of any change to the primary layout, circulation routes, or accessible facility locations

Durability: thermoform or stainless-steel embossed construction; UV-stable; non-toxic surface

Approach: TWSI directional bar route (E-09) from entrance to map station; tactile approach confirmed before other routes diverge

**Retrofit cost note:** Retrofit penalty: LOW. Tactile map station is a free-standing or wall-mounted fixture; no structural works required. Principal cost is production of map at correct specification and ongoing currency maintenance. See Part 12 §12.4.

**Key citations:** DbI. (2022). *Guidelines for accessible environments for DeafBlind people*. Deafblind International. ISO. (2019). *ISO 23599:2019 — Assistive products for persons with vision impairment: Tactile walking surface indicators*. ISO. RNIB. (2022). *Tactile maps and models: guidelines for design and production*. RNIB. [EXPERT CONSENSUS — no building standard in any jurisdiction mandates a tactile building map station.]

**Cross-reference:** E-09 (Tactile Walking Surface Indicators — approach route to station); D-08 (Pictogram + Signage — parallel provision for other populations); K-03 (Haptic Communication Clear Floor Zone)

**Evidence basis (OT):** Compensatory FOR; Ecology of Human Performance (EHP — alter strategy). The tactile building map station alters the information environment at building entry to make orientation accessible through the tactile channel; for DeafBlind users for whom both visual building plans and verbal instructions are inaccessible, the station implements the EHP 'alter' strategy: the context is modified so that independent spatial orientation becomes achievable. No controlled study on tactile map station effectiveness for DBL users in built environments has been conducted.

---

**Jurisdiction comparison:** No code mandates tactile building maps at entrances. US ADA §216 requires accessible signage but not tactile maps. Some US/UK transport facilities provide tactile maps voluntarily. Guidebook specifies raised-relief map station at principal entrance — derived from VIS/DBL wayfinding evidence.


### K-03 Haptic Communication Clear Floor Zone
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DBL -->
<!-- grade_confidence: VERY LOW — Haptic communication clear floor zone ≥900×1500mm: deafblind-built-environment BPC (Protactile/tactile sign requirements). Novel specification. No standard in any jurisdiction. DBL specialist verification required. VERY LOW. -->


> **THIN-BASE DISCLOSURE:** Specifications in this item derive from Tier 2 sources (DbI guidelines, Sense UK) and Tier 4 (ISO 23599:2019) only. No Tier 1 OT clinical research on DBL-specific built environment spatial provisions has been identified in any reviewed language. Specifications reflect expert consensus and DeafBlind-led guidance, not randomised or controlled evidence. Apply with co-design. See GAP-DBL-BE-01.

**Applicable Groups:** DBL

**[EXPERT CONSENSUS — no standard in any jurisdiction; March 2026. Specifications derived from Protactile movement documentation (Clark 2024; Nuccio & granda) and DbI practice guidelines — Co-1 evidence basis.]**

**Description:** Protactile communication — a tactile language system used by DeafBlind people — requires the communicating parties to maintain physical contact, typically through hand-to-hand or hand-to-body touch. This requires clear, stable floor space for both participants adjacent to any point where extended communication (orientation assistance, information transaction, instruction) occurs. All service points, waiting areas, and primary communication locations must provide a haptic communication clear floor zone.

**Specifications:**

Minimum clear floor zone: 1500 × 1500 mm at all service points (counters, reception, information desks) in addition to the standard wheelchair turning circle

At seating positions: 900 × 900 mm clear alongside each designated accessible seat for an intervenor seated position without obstructing the circulation route

At assembly and meeting spaces: row-end seats (aisle positions) designated for DBL users — minimum 1200 × 1200 mm clear zone per position (user + adjacent intervenor position); the clear zone is in addition to and does not substitute for the turning circle at wheelchair positions

Floor surface: firm, level, non-slip within haptic communication zones; no scatter rugs, gratings, or surface changes within the zone

Zone adjacency: haptic communication zones are within the primary circulation route, not in alcoves or recessed bays requiring additional navigation

**Retrofit cost note:** Retrofit penalty: LOW. Clear floor zone provision is a furniture layout and seating placement decision. In fixed-seating venues (auditoria, theatres), achieving the 1200 × 1200 mm aisle-end clear zone may require removal of one seat per row at aisle positions — a low-cost trade operation. See Part 12 §12.4.

**Key citations:** Clark, J.L. (2024). *Touch the Future: The Lives and Language of Protactile DeafBlind People*. University of Minnesota Press. [Co-1 evidence — lived experience of Protactile communication in built environments.] Nuccio, J., & granda, r. [Protactile documentation — Co-1 evidence.] DbI. (2022). *Guidelines for accessible environments for DeafBlind people*. Deafblind International. [EXPERT CONSENSUS — no building standard in any jurisdiction mandates haptic communication clear floor zone dimensions.]

**Cross-reference:** K-01 (Intervenor Adjacency at Service Counters); G-07 (Waiting Area Seating — companion accessible seating standard); E-08 (Corridor Clear Width)

**Evidence basis (OT):** PEOP Model (volition subsystem); Compensatory FOR. The haptic communication clear floor zone compensates for the absence of visual and auditory communication channels by ensuring that the physical space required for Protactile and other tactile communication is not obstructed. The PEOP volition subsystem grounds the provision: the ability to communicate with full agency and without spatial obstruction is a fundamental occupational participation right for DeafBlind users. The 1500 mm zone is derived from two-person tactile communication positioning described in Protactile practice; no architectural measurement study exists.

---

**Jurisdiction comparison:** No code addresses haptic (tactile sign language) communication zones. This is a guidebook-specific provision for DBL population — clear floor zone with adequate lighting for tactile signing. No jurisdiction equivalent exists.


### K-04 Vibrotactile Alert Provision
<!-- CON-0042 [HIGH]: Multi-channel alerting: visual + auditory + vibrotactile simultaneously across all alert types -->
<!-- CON-0114 [HIGH]: Residential care cluster: I-04 hoist + H-05 nurse call + K-04 vibrotactile -->
<!-- CON-0164 [HIGH]: B-10 visual alarm + A-16 sensory room + K-04 vibrotactile — alert cluster -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: MEDIUM -->
<!-- ot_appointment_trigger: conditional:DEAF|DBL -->
<!-- grade_confidence: MODERATE — Vibrotactile alert provision: BS EN 54-23 (Tier 4) + NFPA 72 + Assistive Listening Systems BPC. Vibrotactile alerting is mandated for DEAF in ≥6 jurisdictions. DeafBlind extension requires specialist input (Part 8 §8.6). MODERATE on DEAF mandate; VERY LOW on DBL-specific parameters. -->


> **THIN-BASE DISCLOSURE:** Specifications in this item derive from Tier 2 sources (DbI guidelines, Sense UK) and Tier 4 (ISO 23599:2019) only. No Tier 1 OT clinical research on DBL-specific built environment spatial provisions has been identified in any reviewed language. Specifications reflect expert consensus and DeafBlind-led guidance, not randomised or controlled evidence. Apply with co-design. See GAP-DBL-BE-01.

**Applicable Groups:** DBL

**[EXPERT CONSENSUS — no building standard in any jurisdiction mandates vibrotactile alerting in the built environment; March 2026]**

**Description:** Visual fire alarms (B-10) and standard audio alarms are both inaccessible to DeafBlind users. Vibrotactile alerting — through floor-mounted vibration panels, personal pagers with building integration, or wristband receiver systems — provides emergency and communication alerts through tactile sensation. Vibrotactile provision is the only reliable alert mechanism for building-wide emergencies for DeafBlind occupants.

**Specifications:**

Emergency alerting: vibrotactile floor panel or personal pager system integrated with the building fire alarm panel, activating simultaneously with the audio and visual alarm (B-10)

Floor panel specification (where fixed installation): vibration frequency 20–200 Hz; minimum perceptible amplitude 0.1 mm; panel area ≥300 × 300 mm; flush-mounted; slip-resistant surface; positioned at all primary rest positions and sleeping areas for DBL occupants

Personal pager system: where fixed floor panels are not provided, the building management infrastructure must support a personal pager system; this requires: (a) a fire alarm trigger output (dry contact or BMS relay) accessible for pager base-station integration; (b) BMS point for security/reception notification; (c) charging station at accessible height (400–1100 mm AFF) at the primary DBL user's home base within the building

Communication alerting: where a DBL user occupies a space without staff continuously present, a secondary vibrotactile call system (call button at accessible position ≤1100 mm AFF; vibrotactile response confirmation) supplements the building intercom (H-04)

In residential settings: vibrating wake-up alarm integrated with bedroom services (bedside control H-04) at any bedroom designated for a DBL occupant

**Retrofit cost note:** Retrofit penalty: LOW–MODERATE. Personal pager BMS integration (dry contact relay) is an electrical specification addition at low cost in new construction. Floor panel installation requires floor surface opening and connection — moderate retrofit. Charging station is a power outlet at accessible height. In all cases, the principal cost is the personal pager system hardware, not the building infrastructure. See Part 12 §12.4.

**Key citations:** DbI. (2022). *Guidelines for accessible environments for DeafBlind people*. Deafblind International. Sense UK. (2022). *Building and Communicating*. Sense. Bellman & Symfon. (2024). *Vibrotactile alerting systems for persons with combined hearing and vision loss*. [Tier 5 — manufacturer technical reference; no independent clinical study.] [EXPERT CONSENSUS — no building standard in any jurisdiction mandates vibrotactile alert provision in the built environment.]

**Cross-reference:** B-10 (Visual Fire Alarm — simultaneous activation required); H-04 (Accessible Intercom — personal pager integration); H-05 (Nurse Call / Emergency Pull Cord — CON-0104: K-04 vibrotactile devices must integrate with H-05 nurse call system in care environments; both directions of nurse call communication (outgoing alert from occupant; incoming staff notification) require vibrotactile confirmation for DBL occupants)

**Evidence basis (OT):** Compensatory FOR; EHP Framework (prevent strategy). Vibrotactile alerting compensates for the absence of both auditory and visual emergency notification by providing a tactile alert channel; for DeafBlind occupants this is not an enhancement but the sole reliable mechanism for life-safety alerting. The EHP 'prevent' strategy grounds the provision: the environment is modified to prevent the life-safety failure that results from no accessible alert channel. The 20–200 Hz vibration frequency range is derived from the perceptible vibrotactile frequency range for individuals with intact tactile sensitivity (Verrillo, 1993); no architectural standard specifies this range for built environment applications.


---

## New Items (v10.0 additions)

**Jurisdiction comparison:** No code mandates vibrotactile alerting as a building system. US ADA §702 specifies visual alarms. UK BS 5839 specifies visual alerting. Guidebook adds vibrotactile as a third alerting channel — derived from DBL evidence where neither auditory nor visual alerts are received.


### G-08 Bedroom Wardrobe and Storage Reach Configuration
<!-- CON-0005 [HIGH]: A-09 vibration threshold + G-08 seated reach cluster (MODERATE) -->
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:MOB|PAIN|OFS -->
<!-- grade_confidence: LOW — Wardrobe and storage reach configuration: NIOSH reach range (Tier 4) + OT energy conservation CPG (Tier Co-2). No RCT on reach zone specification for disability outcomes. -->

**Applicable Groups:** MOB, MOB/UPL, NEU, OFS, PAIN

**Description:** Wardrobe and storage design to provide independent access across the full reach envelope for seated and ambulant users with reduced reach or trunk instability. Hanging rods, shelves, and drawers to be positioned and dimensioned to eliminate the need for trunk forward-lean beyond the 30° fall-risk threshold. Wardrobe door type to preserve clear manoeuvre space within the dressing area.

**Specifications:**
- ● Hanging rods to be at no greater than 1050 mm AFF, permitting seated forward reach without trunk lean exceeding 30° [REF:accessible-bathroom-and-grab-bar:18]
- ● Where wardrobe depth permits, a dual-rod configuration to be provided — upper rod at 1000–1100 mm AFF, lower rod at 600 mm AFF [REF:accessible-bathroom-and-grab-bar:18]
- ● Fixed shelf depth not to exceed 380 mm [REF:accessible-bathroom-and-grab-bar:18] *(single Co-2 source)*
- ● Where deeper storage is required, full-extension pull-out drawers to be provided, drawer depth not to exceed 600 mm [REF:accessible-bathroom-and-grab-bar:18]
- ● Shelf units to be arranged in a U-shape or L-shape configuration where practicable [REF:accessible-bathroom-and-grab-bar:19] *(Universal Mode provision — CON-0038; serves MOB, NEU, PAIN; neutral for VIS, DEAF, DEM)*
- ● Fixed storage below 500 mm AFF to be provided with a pull-out mechanism only [REF:accessible-bathroom-and-grab-bar:18]
- ○ Wardrobe doors to be sliding or bi-fold; outward-swing doors to be used only where clear floor space ≥ door-width plus 600 mm is available adjacent to the door arc [REF:accessible-bathroom-and-grab-bar:18]
- ● A turning and manoeuvre space of no less than 1500 mm × 1500 mm to be maintained clear of fixed furniture throughout the dressing area [REF:accessible-bathroom-and-grab-bar:18]

**Design Stage:** Design Development · Technical Architecture

**Retrofit:** LOW penalty — no structural change required. Pull-out hardware and dual-rod installation are non-structural adaptations. DAR provision: blocking behind wardrobes for future bracket and rod-height adjustment to be specified at construction stage. See Part 11 §DAR.

#### Sources cited

| REF-ID | Authors | Year | Title | Journal/Publisher | Tier | Lang | Jurisdiction |
|---|---|---|---|---|---|---|---|
| REF:accessible-bathroom-and-grab-bar:18 | Russell, R., Walker, M., Copeman, I., & Porteus, J. | 2019 | Adaptations Without Delay | Royal College of Occupational Therapists / Housing LIN | Co-2 | EN | UK | https://www.rcot.co.uk/explore-resources/rcot-publications/adaptations-without-delay |
| REF:accessible-bathroom-and-grab-bar:18 | AOTA | 2023 | Home Modification Practice Guidelines | AOTA | Co-2 | EN | US |
| REF:accessible-bathroom-and-grab-bar:18 | CAOT | 2024 | Home Assessment and Modifications | CAOT | Co-2 | EN | CA |
| REF:accessible-bathroom-and-grab-bar:18 | UNSW Home Mod Clearinghouse | 2023 | OT Home Modification Guidelines | UNSW/HMC | Co-2 | EN | AU |
| REF:accessible-bathroom-and-grab-bar:19 | Siebert, C., Smallfield, S., & Stark, S. | 2014 | Occupational Therapy Practice Guidelines for Home Modifications | AOTA Press | Co-2 | EN | US | https://library.aota.org/OT_Practice_Guidelines_Home_Modification/ [YEAR MISMATCH: cited as 2023; confirmed edition is 2014. AOTA library updated — verify if 2023 edition exists] |


**Cross-reference:** G-04 (Accessible Bathroom — transfer clearance); G-05 (Adjustable-height work surfaces); Part 11 (DAR provisions)

**Illustration:** [Illustration: to be provided] — Plan view of dual-rod wardrobe with 380 mm shelf depth and 1500 mm dressing turning circle.

**FDR-TCOA-01 [Tier 3 — van Hoof 2010]:** Thermoregulatory unawareness in DEM — carer-managed dressing is a primary occupational need. In DEM-designated residential and care bedrooms, wardrobe to provide: full-width door opening (minimum 900 mm clear); adjustable hanging rail 1050–1200 mm AFF (suits carer-operated dressing from seated or standing position); shelf height 600–900 mm for carer-visible clothing display; visual display arrangement of clothing options (open shelving or glass front). ○ [THIN — Tier 3 clinical mechanism; no dedicated wardrobe design RCT]

---


**FDR-NDV-03 [THIN — Tier 1 mechanism; Co-2 OT practice]:** Executive function deficits in NDV/AUT and NDV/ADHD (Pennington & Ozonoff 1996 — Tier 1 mechanism) impair location memory for stored items. Visible, labelled storage reduces cognitive overhead of retrieval. ○ In NDV-occupied residential and workplace settings: open shelving or glass-front cabinet doors preferred over solid doors at all primary storage; shelf items to be visible at eye level or above from standing position. Complements D-05 provision.

**G-08 also covers: Seated-Task Design (relocated from F-05 per CO-0003/D2-48)**

**Applicable Groups (seated-task):** OFS · PAIN · MOB · ALL
<!-- CO-0003/D2-48: F-05 content relocated here. All primary occupational tasks to be achievable without sustained standing. -->

**Seated-task specifications:**
- ● All primary occupational task surfaces to be achievable from a seated position; standing-only task configurations not to be specified [Tier 5 — BS 8300:2018; JAN workplace accommodation guidance]
- ● Adjustable-height work surfaces: 650–870 mm AFF range (seated to standing); knee clearance ≥680 mm depth × ≥ 900 mm width under all adjustable surfaces [Co-2 — RCOT 2019; CAOT 2024]
- ● At least one seated-height service counter or work position per functional zone in non-residential settings [Tier 5 — BS 8300; CSA B651]
- ○ Reception and service counters: minimum 30% of counter length at 760–860 mm AFF with knee clearance beneath [Tier 6 — ADA; BS 8300]
- ● Rest seating with backrest and armrests accessible within 25 m of any primary task location [pain-ofs-built-environment-design BPC]

**Design Stage:** Design Development · Technical Architecture

**Retrofit:** LOW penalty — adjustable-height desk mechanisms are non-structural; DAR provision at construction stage: conduit for powered desk motors; knee-clearance maintained under all fixed worktops.

**Jurisdiction comparison:**

| Jurisdiction | Standard | Reach Range | Rail Height | Shelf Height | Notes |
|---|---|---|---|---|---|
| US | ADA §811 / A117.1 | Per §308 reach ranges | — | — | Storage elements |
| UK | M4(2) / M4(3) | — | — | — | Wheelchair-user dwellings |
| DE | DIN 18040-2 | 850-1050mm handles | — | — | General reach |
| **Guidebook** | **G-08** | **Per H-01 (900-1100mm)** | **Adjustable** | **Adjustable** | **UPL one-hand operation** |


### G-09 Bedroom Emergency Call Provision and Overnight Lighting
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:OFS|NEU|DEM -->
<!-- grade_confidence: LOW — Bedroom emergency call + overnight lighting: BS 8300 + DEN provisions. Tier 5-6. No RCT on emergency call provision for OFS/NEU overnight outcomes. -->

**Applicable Groups:** MOB, DEM, NEU, OFS, PAIN, NDV/MH, MOB/UPL

**Description:** Accessible bedrooms to be provided with dual emergency call positions, a pillow-proximity light control, bed-exit sensor-activated overnight lighting, and clear floor space for emergency responder access. Where medication is stored in the bedroom, lockable bedside storage to be within reach from the bed edge. Bedroom door to be identifiable by colour or texture in residential settings with multiple bedroom doors off a common route.

**Specifications:**
- ● Two emergency call positions to be provided: one with cord end at 100–150 mm AFF (floor-level fall recovery), one at no greater than 500 mm AFF from the bed head [REF:accessible-bathroom-and-grab-bar:18] *(single Co-2 source)*
- ● A luminaire control to be positioned within 900 mm of the pillow position, operable without sitting upright [REF:accessible-bathroom-and-grab-bar:18] *(single Co-2 source)*
- ● An automatic night-lighting system, activated by a bed-exit sensor, to be provided on the route between bed and bathroom [REF:accessible-bathroom-and-grab-bar:18] *(single Co-2 source)*; manual switch alone does not meet this requirement
- ● Continuous low-level pathway lighting to be installed at 300–400 mm AFF on the bed-to-bathroom route, providing a minimum of 5 lux at floor level [REF:accessible-bathroom-and-grab-bar:22]
- ● Colour temperature not to exceed 3000 K [REF:accessible-bathroom-and-grab-bar:22]
- ○ Bedroom doors to be distinguishable from other internal doors by colour contrast or texture; a name, number, or personalisation plate to be provided at 1200 mm AFF [REF:accessible-bathroom-and-grab-bar:22]
- ● Medication storage, where provided, to be lockable, at no greater than 1200 mm AFF, and within 500 mm horizontal reach of a seated bed-edge position [REF:accessible-bathroom-and-grab-bar:23] *(single Co-2 source)*
- ● Clear floor space of no less than 1000 mm to be maintained at the foot of the bed as an emergency responder access path [REF:accessible-bathroom-and-grab-bar:23] *(single Co-2 source)*

**Design Stage:** Design Development · Technical Architecture

**Retrofit:** MODERATE penalty — bed-exit sensor wiring and low-level pathway lighting require electrical work. DAR provision: conduit from bed-head to ceiling rose; floor-level lighting circuit rough-in to be specified at construction stage. See Part 11 §DAR.

#### Sources cited

| REF-ID | Authors | Year | Title | Journal/Publisher | Tier | Lang | Jurisdiction |
|---|---|---|---|---|---|---|---|
| REF:accessible-bathroom-and-grab-bar:18 | Russell, R., Walker, M., Copeman, I., & Porteus, J. | 2019 | Adaptations Without Delay | Royal College of Occupational Therapists / Housing LIN | Co-2 | EN | UK | https://www.rcot.co.uk/explore-resources/rcot-publications/adaptations-without-delay |
| REF:accessible-bathroom-and-grab-bar:22 | Dementia Australia | 2022 | Designing Dementia-Friendly Care Environments | Dementia Australia | 2 | EN | AU | https://www.dementia.org.au/professionals/designing-dementia-friendly-care-environments [TITLE MISMATCH: cited as Built Environment Guidelines; confirmed title is Designing Dementia-Friendly Care Environments. Year 2022 plausible but not confirmed exact — verify at dementia.org.au] |
| REF:accessible-bathroom-and-grab-bar:23 | American Occupational Therapy Association | 2023 | Fall Prevention in the Home | AOTA | Co-2 | EN | US | [UNVERIFIED — AOTA publishes fall prevention tip sheets and practice resources but specific standalone 'Fall Prevention in Bedroom 2023' not confirmed. May be from AOTA Practice Advisory or OT Practice article. Verify at aota.org] |

**Cross-reference:** B-11 (Warm colour temperature ≤2700 K after 19:00); B-12 (Sensor-activated overnight pathway lighting); H-01 (Controls at accessible height); D-06 (Memory boxes at residential room entrances)

**Illustration:** [Illustration: to be provided] — Bedroom plan showing dual cord positions, pillow-proximity switch zone, bed-exit sensor coverage arc, and 1000 mm foot clearance.

---

**Jurisdiction comparison:** UK HTM 08-03 covers healthcare call systems. DE DIN VDE 0834 covers nurse call. Guidebook specifies bedroom-specific emergency call with overnight low-level pathway lighting — integrated provision for falls prevention + alerting.


### B-12 Sensor-Activated Overnight Pathway Lighting
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DEM|OFS -->
<!-- grade_confidence: LOW — Sensor-activated overnight pathway lighting: BS 8300 + DSDC EADDAT + OT CPG. No RCT on sensor vs manual lighting for DEM/OFS overnight outcomes. Tier 5-6 standards + Co-2. -->

**Applicable Groups:** MOB, DEM, NEU, OFS, PAIN, VIS, NDV/MH, DBL

**Description:** Sensor-activated low-level lighting to be provided on all residential circulation routes between the bedroom and bathroom. Activation to be by bed-exit infrared sensor, without requiring manual switching. Luminaires to be positioned at floor level to illuminate the path without disturbing occupants in the adjacent bed. Colour temperature to remain within the warm spectrum to avoid circadian disruption.

**Specifications:**
- ● Sensor-activated low-level lighting to be provided on any residential circulation route between bedroom and bathroom [REF:accessible-bathroom-and-grab-bar:18] *(single Co-2 source)*
- ● Activation to be by infrared bed-exit sensor; manual switch operation alone does not meet this requirement [REF:accessible-bathroom-and-grab-bar:18]
- ● Luminaires to be positioned at 300–400 mm AFF, oriented to illuminate the floor surface [REF:accessible-bathroom-and-grab-bar:22]
- ● Floor illuminance to be no less than 5 lux throughout the route [REF:accessible-bathroom-and-grab-bar:22]
- ● Colour temperature not to exceed 3000 K [REF:accessible-bathroom-and-grab-bar:22] *(single Tier 2 source)*
- ○ Where the bed-to-bathroom route passes through a shared circulation area, low-level lighting to be maintained throughout; the pathway lighting system to be independent of the general room lighting circuit

**Design Stage:** Design Development · Technical Architecture · Post-Occupancy

**Retrofit:** MODERATE penalty — new circuit and sensor required. Floor-level conduit chase is moderate cost. Plug-in sensor-activated nightlights (≥5 lux) are an acceptable interim post-occupancy solution. See Part 11 §DAR.

#### Sources cited

| REF-ID | Authors | Year | Title | Journal/Publisher | Tier | Lang | Jurisdiction |
|---|---|---|---|---|---|---|---|
| REF:accessible-bathroom-and-grab-bar:18 | Russell, R., Walker, M., Copeman, I., & Porteus, J. | 2019 | Adaptations Without Delay | Royal College of Occupational Therapists / Housing LIN | Co-2 | EN | UK | https://www.rcot.co.uk/explore-resources/rcot-publications/adaptations-without-delay |
| REF:accessible-bathroom-and-grab-bar:22 | Dementia Australia | 2022 | Designing Dementia-Friendly Care Environments | Dementia Australia | 2 | EN | AU | https://www.dementia.org.au/professionals/designing-dementia-friendly-care-environments [TITLE MISMATCH: cited as Built Environment Guidelines; confirmed title is Designing Dementia-Friendly Care Environments. Year 2022 plausible but not confirmed exact — verify at dementia.org.au] |

**Cross-reference:** B-11 (Warm colour temperature ≤2700 K after 19:00); G-09 (Bedroom emergency call and overnight lighting)

**Illustration:** [Illustration: to be provided] — Section through bedroom showing 300–400 mm AFF luminaire position and sensor activation zone.

---

**Jurisdiction comparison:** No code specifies sensor-activated overnight pathway lighting. UK DSDC Stirling recommends nighttime lighting for DEM. Guidebook specifies PIR-activated low-level warm lighting (≤2700K, ≤10 lux) on bedroom-to-bathroom route — derived from DEM falls prevention and circadian protection evidence.


### E-12 Entrance Landing and Manoeuvring Space for Power Wheelchair Users
<!-- design_stage_lock: SD -->
<!-- ve_risk: HIGH -->
<!-- ot_appointment_trigger: not-triggered -->
<!-- grade_confidence: LOW — Evacuation lift + refuge: BS EN 81-70, BS 9999. No RCT on evacuation outcomes for disabled users. Tier 5-6 fire engineering standards. Fire safety context — precautionary principle applies. -->

**Applicable Groups:** MOB, MOB/UPL, OFS

**Description:** Entrance landings and manoeuvring clearances to be dimensioned for the larger footprint and deceleration geometry of electrically propelled wheelchairs. Level landing to be no less than 1800 mm × 1800 mm, superseding the 1500 mm × 1500 mm provision at E-06 for power wheelchair populations. Canopy to accommodate power wheelchair and companion simultaneously. Where threshold and landing cannot both meet requirements, threshold governs.

**Specifications:**
- ● A level landing of no less than 1800 mm × 1800 mm to be provided outside every accessible entrance door, clear of the door swing arc [REF:residential-entry-and-threshold:04] *(single Tier 5 source)*
- ● Clear manoeuvring space of no less than 500 mm to be provided on the latch side where a power wheelchair population is identified [REF:residential-entry-and-threshold:04] *(single Tier 6 source)*
- ● A canopy or weather protection to be provided at all accessible entrances, to a minimum depth of 1800 mm and a minimum width of 2000 mm [REF:residential-entry-and-threshold:04] *(single Tier 5 source)*
- ● Where threshold height and landing size cannot both meet requirements, threshold height to govern: zero threshold with adequate deceleration approach takes priority [REF:residential-entry-and-threshold:05]
- ● Threshold >6 mm combined with landing <1800 mm constitutes a design that excludes independent access by power wheelchair users [REF:residential-entry-and-threshold:05]

**Design Stage:** Schematic Design · Design Development

**Retrofit:** HIGH penalty — landing enlargement requires external works; canopy addition requires structural fixing. Both to be planned at initial design stage. See Part 11 §DAR.

#### Sources cited

| REF-ID | Authors | Year | Title | Journal/Publisher | Tier | Lang | Jurisdiction |
|---|---|---|---|---|---|---|---|
| REF:residential-entry-and-threshold:04 | BSI | 2018 | BS 8300-2:2018, Annex G | BSI | 5 | EN | UK |
| REF:residential-entry-and-threshold:04 | Standards Australia | 2021 | AS 1428.1:2021 | Standards Australia | 6 | EN | AU |
| REF:residential-entry-and-threshold:05 | Putthinoi et al. | 2017 | ICF-based home modification outcomes | American Journal of OT | 1 | EN | TH/AU |

**Cross-reference:** E-06 (Level Entry — Universal Mode floor); E-05 (Weather protection at entry — NR canopy spec); G-04 (Accessible Bathroom — turning space differential)

**Illustration:** [Illustration: to be provided] — Plan view showing 1800 × 1800 mm landing, 500 mm latch-side clearance, and canopy footprint.

---

**Jurisdiction comparison:**

| Jurisdiction | Standard | Landing Size | Clear of Door Swing | Notes |
|---|---|---|---|---|
| US | ADA 2010 §404.2.4 | 1524×1524mm | Yes | Maneuvering clearance by approach type |
| UK | BS 8300-2:2018 §8 | 1500×1500mm | Yes | — |
| DE | DIN 18040-1 §4.3.3 | 1500×1500mm | Yes | Movement area |
| AU | AS 1428.1:2021 | 1540×1540mm / 2070×2070mm | Yes | Powered chair dimensions |
| ISO | ISO 21542:2021 §14 | 1500×1500mm | Yes | — |
| **Guidebook** | **E-12** | **By device type** | **Yes** | **AU dimensions for powered chairs** |


### E-13 Entrance Cognitive Legibility Provisions
<!-- design_stage_lock: DD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:DEM|NDV -->
<!-- grade_confidence: LOW — Entrance cognitive legibility: cognitive wayfinding BPC (Tier 3-4). No RCT. Expert consensus for DEM/NDV entrance design. -->

**Applicable Groups:** DEM, NEU, NDV, VIS, DBL, NDV/MH

**Description:** Entrance door and approach to be legible and identifiable for users with cognitive impairment, including dementia, neurodivergence, and neurological conditions. Luminance contrast, colour direction, activation controls, automatic lighting, and address identification to be provided to a standard that supports independent wayfinding to and recognition of the entrance from the public footpath.

**Specifications:**
- ● Entrance door leaf luminance contrast to be no less than 0.4 against the adjacent wall surface, assessed at 3 m from the approach path [REF:residential-entry-and-threshold:06] *(single Co-2 source)*
- ● Where DEM is the identified population, warm-spectrum colour (red, amber, or yellow) to be preferred where consistent with the building's colour and surface finish strategy [REF:residential-entry-and-threshold:06]
- ● Entry activation controls to have a minimum button diameter of 50 mm, positioned at 900–1200 mm AFF, and visible from the approach path before the user reaches the door [REF:residential-entry-and-threshold:06] *(single Co-2 source)*
- ● A PIR sensor-activated luminaire providing no less than 150 lux at threshold level to be installed at all accessible entrances [REF:residential-entry-and-threshold:06] *(single Co-2 source)*; this does not remove the requirement for a manual luminaire control
- ● Address numerals to be provided at no less than 150 mm character height, high-contrast, backlit or retro-reflective, positioned at 1200–1600 mm AFF [REF:residential-entry-and-threshold:07] *(single Co-2 source)*
- ○ Where DEM is the identified population and the entrance is set back from the street boundary, the property boundary to be demarcated by a continuous visual feature distinctive in colour [REF:residential-entry-and-threshold:07]

**Design Stage:** Schematic Design · Design Development · Technical Architecture

**Retrofit:** LOW penalty — address signage, button replacement, and PIR luminaire are non-structural. Luminance contrast at door leaf requires repainting or cladding where existing finish does not meet the 0.4 threshold. See Part 11 §DAR.

#### Sources cited

| REF-ID | Authors | Year | Title | Journal/Publisher | Tier | Lang | Jurisdiction |
|---|---|---|---|---|---|---|---|
| REF:residential-entry-and-threshold:06 | RCOT | 2020 | Dementia Design Guidance | RCOT/Housing LIN | Co-2 | EN | UK |
| REF:residential-entry-and-threshold:07 | AOTA | 2023 | Cognitive Impairment Home Modification | AOTA | Co-2 | EN | US |
| REF:residential-entry-and-threshold:08 | Dementia Australia | 2022 | Built Environment Guidelines | Dementia Australia | 2 | EN | AU |

**Cross-reference:** C-01 (Colour and surface finish — luminance contrast); D-02 (Cognitive simplicity); D-04 (Landmarks at every decision point); B-01 (Circadian lighting)

**Illustration:** [Illustration: to be provided] — Elevation of entrance door showing luminance contrast zones, intercom position at 900–1200 mm AFF, and address numeral placement.

---

**Jurisdiction comparison:** No code specifies cognitive legibility at entrances. UK PAS 6463 recommends clear entrance identification for NDV. Guidebook specifies visible entrance, clear signage, consistent approach sequence — derived from DEM/NDV wayfinding evidence.


### E-10 Rest Seating on Circulation Routes
<!-- design_stage_lock: SD -->
<!-- ve_risk: LOW -->
<!-- ot_appointment_trigger: conditional:OFS|MOB|PAIN -->
<!-- grade_confidence: LOW — Rest seating interval 25m: Roxburgh et al. 2024 (BJ Occup Ther, Tier 1) — OT home modification for ME/CFS. OFS clinical pacing guidance (CDC, IOM/NAM Tier 1 clinical). BS 8300: 100m general. No built-env RCT on seating interval vs OFS outcomes. LOW — clinical rationale strong but no architectural study. -->

**Applicable Groups:** OFS, MOB/AMB, PAIN, DEM, NEU, NDV

*Revision note: Prior E-10 specified interval only (≤20 m). Interval revised to ≤25 m (Tier 1 evidence). Alcove geometry and OFS-specific seat height added. ≤20 m interval was an overclaim.*

**Description:** Rest seating to be provided at intervals not exceeding 25 m on all primary accessible circulation routes, recessed into alcoves that do not reduce clear circulation width. Seating to be dimensioned to serve the postural requirements of OFS/POTS users, ambulant disabled users, and others for whom sustained standing or walking without rest creates a barrier. Arms to be provided on all seats to enable lever-up from seated.

**Specifications:**
- ● Rest seating to be provided at intervals not exceeding 25 m on all primary accessible circulation routes [REF:accessible-circulation-geometry:09]
- ○ Where 25 m intervals cannot be achieved, a maximum interval of 30 m is acceptable on secondary routes only [REF:accessible-circulation-geometry:09]
- ● Rest seating to be recessed a minimum of 200 mm from the clear circulation path, in alcoves of no less than 900 mm width per seat and 450 mm seat depth [REF:accessible-circulation-geometry:12] *(single Co-2 source)*
- ● Seat height to be no less than 480 mm AFF; seat height below this threshold creates a postural barrier for OFS/POTS users [REF:accessible-circulation-geometry:12]
- ● Arms to be provided on both sides of each seat, extending at least 200 mm beyond the front seat edge [REF:accessible-circulation-geometry:02] *(single Tier 5 proxy)*
- ○ A minimum of one seating position per alcove to accommodate a tilt or recline angle of no less than 15° from vertical [REF:accessible-circulation-geometry:09]
- ○ Full horizontal capability to be provided at a rate of one per floor in buildings where OFS/ME is the identified population and full recline is required for symptom management

**Design Stage:** Schematic Design · Design Development

**Retrofit:** MODERATE penalty — alcove integration requires spatial planning at design stage. Individual seating units at 480 mm seat height with arms are LOW penalty retrofit where alcove provision has been made. See Part 11 §DAR.

#### Sources cited

| REF-ID | Authors | Year | Title | Journal/Publisher | Tier | Lang | Jurisdiction |
|---|---|---|---|---|---|---|---|
| REF:accessible-circulation-geometry:09 | Roxburgh, R., Hughes, J., & Milgate, W. | 2024 | Using time diaries to inform OT practice for people with ME/CFS | British Journal of Occupational Therapy | 1 | EN | UK |
| REF:accessible-circulation-geometry:12 | RCOT | 2019 | Housing Adaptations Without Delay | RCOT/Housing LIN | Co-2 | EN | UK |
| REF:accessible-circulation-geometry:02 | BSI | 2018 | BS 8300-2:2018 | BSI | 5 | EN | UK |

**Cross-reference:** D-11 (Safe accessible garden — seating every 20 m outdoors); G-02 (Variety of seating types); GAP-FDR-T0-09 (Universal Mode candidate — pending connection-scout)

**Illustration:** [Illustration: to be provided] — Plan of alcove showing 900 mm width, 200 mm recess from circulation path, and 450 mm seat depth. Section showing 480 mm AFF seat height and arm projection.


---

## E-14 Entrance Rest Seating

<!-- CON-0054 [HIGH]: Entrance rest seating serves OFS (orthostatic recovery), PAIN (joint relief), MOB/AMB (rest before walking), DEM (orientation pause). Universal Mode candidate per GAP-FDR-T0-04. Four populations, independent clinical rationales. -->
# E-14 — Entrance Rest Seating

**Category:** E — Entrances and Circulation  
**Item code:** E-14  
**Tier:** 0 (Universal Design)  
**Populations served:** ALL  
**Primary beneficiaries:** OFS · PAIN · MOB/AMB · DEM  
**Evidence status:** ○ Expert consensus overall; seat height and arm provision ● evidence-based per RCOT clinical guidance  
**Related items:** E-05 (Weather Protection) · E-10 (Circulation Route Rest Seating)  
**Evidence disclosure:** [EXPERT CONSENSUS — no built-environment spatial research specifically addresses entrance rest seating in any jurisdiction searched; March 2026. Clinical seating parameters derive from OT home modification practice evidence (Co-2/Tier 1). Spatial application parameters are expert consensus.]

[Illustration: to be provided]

---

## Purpose

○ Rest seating at accessible entrances removes the standing demand during threshold tasks: operating intercoms, security keypads, automatic door delays, and footwear removal.¹ ● The entrance transition zone concentrates multiple simultaneous demands — door operation, orientation, weather exposure, grade change — at the point of maximum physical load for fatigue, pain, and orthostatic populations.² ³

○ For users experiencing orthostatic intolerance, chronic pain, or fatigue-related disability, seating at the threshold prevents the forced choice between abandoning entrance tasks and triggering post-exertional malaise, orthostatic episodes, or pain escalation.² ³ ● Entrance seating provision is among the top five most frequently recommended OT home modifications for OFS and fatigue populations.³

○ For users with dementia, a consistent seating location at the entrance provides an orientation reference and reduces wayfinding demand during the disorienting threshold transition.⁴ This provision is neutral for VIS, DEAF, NEU, and NDV populations.

*E-14 is distinct from E-10 (Circulation Route Rest Seating). E-10 governs seating intervals on routes (25–30 m). E-14 governs entrance-zone provision regardless of route length.*

---

## Specification

### Ideal

○ Reclinable seating with bilateral fixed arms, seat height 450–460 mm AFF, within 3 m of accessible entrance threshold, in alcove ≥1200 mm wide recessed ≥300 mm from the main accessible route, under weather protection (E-05).⁵ ⁶

● Back support ≥450 mm high, seat depth 400–450 mm, bilateral fixed arms extending 200–250 mm forward of seat front edge, arm height 180–220 mm above compressed seat surface.¹

○ Recline mechanism: tilt-in-space or backrest recline to ≥120° from vertical, operable from seated position without grip strength demand (lever or push-button actuator).² ³

○ Seat and backrest: cushioned (minimum 40 mm compression foam or equivalent), non-slip surface when wet, drainage provision if exposed to weather.⁵

○ Alcove orientation: seating faces the entrance door to allow the user to observe approach, door operation, and visitor arrival without requiring head rotation.⁴

○ Clear floor space ≥900 mm × 1400 mm in front of seating, unobstructed and outside the main accessible route, for mobility device parking or companion standing.⁶

---

### Best Practice

● Seating with bilateral fixed arms, seat height 440–480 mm AFF, within 5 m of accessible entrance threshold, in alcove ≥1200 mm wide recessed ≥200 mm from the main accessible route, under weather protection (E-05).¹ ⁵ ⁶

○ Recline capability recommended at Universal Mode (tilt-in-space or backrest recline ≥110° from vertical preferred; fixed upright seating acceptable).² At Tier 1 where OFS or PAIN populations are identified, recline capability is mandatory.² ³

● Arms: both fixed, extending ≥200 mm forward of seat front edge, height 180–250 mm above compressed seat surface, minimum 40 mm graspable diameter or equivalent profile.¹

● Backrest: continuous support across full seat width; where recline mechanism is not provided, backrest angle 100–110° from horizontal.¹

○ Seat surface: firm (≤50 mm compression under load), non-slip when wet.⁵

○ Clear floor space ≥900 mm × 1200 mm in front of seating, outside the main accessible route.⁶

---

### Acceptable

○ Fixed upright seating with bilateral fixed arms, seat height 440–480 mm AFF, within 5 m of threshold, alcove ≥900 mm wide recessed ≥200 mm from the main accessible route, under weather protection.¹ ⁵ ⁶

● Back support ≥350 mm high, seat depth ≥380 mm.¹

● Arms extending ≥150 mm forward of seat front, height 180–250 mm above seat surface.¹

○ Seat material: non-cushioned acceptable if non-slip and not thermally conductive (metal and stone seat surfaces are not acceptable in cold climates or shade-exposed locations).⁵

---

### Minimum

○ Fixed bench seating, seat height 440–480 mm AFF, with back support (minimum 300 mm high) and at minimum one fixed arm, within 5 m of accessible entrance threshold, alcove ≥900 mm wide recessed ≥200 mm from the main accessible route, under weather protection.¹ ⁵ ⁶

○ Where weather protection (E-05) is not provided at the entrance, entrance rest seating is deferred to the first covered interior space within 5 m of threshold.

---

## Design Development and Ready for Occupancy notes

**DD:** Confirm seating alcove does not reduce accessible path clear width at E-08 or turning space at E-01/E-02. Confirm recline trajectory (where provided) does not project into circulation path. Confirm arm height clears door furniture and keypad mounting heights.

**RFO:** Verify seating is positioned within weather-protected zone (E-05 canopy/porch boundary). Verify clear floor space in front is unobstructed. Confirm recline mechanism is operational without grip force demand.

---

#### Sources cited

| REF-ID | Source | Tier |
|---|---|---|
| REF:seating-entrance:01 | RCOT Housing Adaptations Without Delay (2019). Royal College of Occupational Therapists, London. | Co-2 |
| REF:seating-entrance:02 | Roxburgh, E. & Mackay, L. (2024). Occupational therapy home modification outcomes for fatigue and orthostatic populations. British Journal of Occupational Therapy, 87(3). [YEAR AND VOLUME PROVISIONAL — confirm DOI before publication] | Tier 1 |
| REF:seating-entrance:03 | PAIN/OFS functional-deficit-researcher synthesis (2026-03-26). Internal evidence collation. Co-2/Tier 3 aggregate. | Co-2/Tier 3 |
| REF:seating-entrance:04 | CON-0037 connection-scout Opus synthesis (2026-03-28). Entrance zone demand analysis and DEM application. Expert consensus. | ○ |
| REF:seating-entrance:05 | E-05 Weather Protection item specification. Volume II Part 7, Category E. Internal cross-reference. | — |
| REF:seating-entrance:06 | Accessible-circulation-geometry BPC (references/bpc/entrances-and-circulation/accessible-circulation-geometry.md). Clear floor space and alcove geometry standards. | Tier 4–5 aggregate |

**Note on REF:seating-entrance:02:** Roxburgh & Mackay (2024) citation requires DOI verification before publication. If unverified after two search attempts: apply deletion rule (project-standards.md) and replace with [UNSUPPORTED — citation required] on the recline-mandatory-Tier-1 claim.

---

## Gap register update required

- GAP-FDR-T0-04-E14: update to CLOSED-CONSUMED on E-14 integration (this document)
- CON-0037: update disposition PENDING → CONSUMED (this document; session ref 2026-03-28)
