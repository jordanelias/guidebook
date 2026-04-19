## Part 5: Building-Level Co-Occurrence Resolution

<!-- evidence_density: Thin -->
> **Evidence density: ░ Thin** — Conflict resolution methodology is expert consensus informed by harm-asymmetry analysis. Nine resolved conflicts draw on Tier 1–4 sources from individual population evidence. No primary study validates the resolution framework itself. The variable-conflation correction (Step 0) is an original analytical contribution of this guidebook. **Critical gap:** Zero primary built-environment studies on compound functioning; all compound resolutions are inference from single-population evidence.


*Guidebook for Accessible Design v10.0*

---

### §5.1 Scope and Operating Principle

Every population-specific accessibility specification in this guidebook is calibrated to its population's OT evidence base. When a building serves two or more populations simultaneously — the rule rather than the exception in any institutional, commercial, or multi-resident building — some specifications conflict directly. The high-contrast visual environment that orients a VIS user creates overstimulation for an NDV user in the same corridor. The acoustic amplification that enables a DEAF user to follow speech is a sensory assault for a NEU/PCS user in the same meeting room. A plain floor that prevents falls for a DEM user removes the tactile differentiation that a VIS user relies on for orientation. These are not design failures or specification errors. They are the inevitable result of applying population-specific evidence to shared space.

Part 5 exists because conflict resolution requires a different method from specification writing. Specification writing asks: what does the evidence say for this population? Conflict resolution asks: when two evidence-based provisions contradict each other in the same space, which governs, and how does the design reconcile them? The answer is not to split the difference. It is to apply the resolution hierarchy, document the rationale, and identify — explicitly — the conflicts that cannot be resolved without individual co-design.

The resolution hierarchy for this guidebook is:

1. **Safety-critical provisions take priority.** A provision that prevents a fall, prevents scalding, or enables fire evacuation governs over a provision that optimises sensory comfort. Plain flooring (DEM fall prevention) governs over patterned flooring (VIS orientation) because a fall is an injury; a navigation challenge is a barrier. The Tier 1 OT clinical evidence for the safety outcome determines which provision takes precedence, not the frequency of the populations involved.

2. **Tier 1 OT clinical evidence governs where safety provisions are equivalent.** Where both conflicting provisions have safety rationales of equivalent weight, the provision supported by higher-tier OT evidence takes Tier 1 priority. Tier 2 and lower provisions are resolved to Tier 1 constraints with a residual gap noted.

3. **The most constrained user's provision governs where OT evidence is equal.** Where evidence quality is equivalent, the provision serving the population with the more severe functional consequence of non-compliance governs. Acoustic amplification is more critical to a DEAF user than quiet is to an NDV user with moderate sensory sensitivity; the NDV user has management strategies (ear protection, withdrawal) that a DEAF user without a hearing loop does not.

4. **Range specifications are preferred over point specifications.** Where a parameter is contested, a range that falls within the acceptable zone for both populations avoids the need to choose. The 32–45 mm grab bar diameter range is the product of this principle: 32 mm is the minimum that satisfies UPL grip evidence; 45 mm is the maximum before standard MOB grip evidence degrades. Both populations are served within the range.

5. **Zoning separates irreconcilable conflicts.** Where no single parameter value serves all populations, spatial separation — assigning zones with distinct parameter sets — is the resolution mechanism. The three-zone sensory gradient (F-01) is the primary zoning tool for illuminance, acoustic level, and olfactory provision.

6. **Irresolvable conflicts are documented, not hidden.** Where a conflict cannot be resolved at Tier 0 or Tier 1 for a shared ambient parameter, this section records it as a Tier 2 conflict — resolvable only through individual co-design. The absence of a Tier 0–1 resolution does not mean the space cannot be designed; it means the OT assessment is mandatory.

**Compound intra-individual profiles.** The resolution hierarchy above addresses inter-group conflicts — different people in the same space. For intra-individual compound profiles — a single person who is simultaneously MOB + PAIN + DEM, for example — pairwise resolution is necessary but insufficient. The compound functional impact of co-occurring conditions is supra-additive: the person's functional profile cannot be predicted from the sum of individual population specifications (BMC Geriatrics 2022, Multimorbidity-Weighted Index; Clarke et al., American Journal of Epidemiology, 4.52x environment-impairment interaction). For these occupants, Part 5's building-level resolution provides the environmental baseline, but the final specification is a Tier 2 domain. The OT co-design assessment addresses the interaction between conditions for the individual, using the compound evidence base where it exists and clinical reasoning where it does not. The guidebook equips the OT with the specification parameters (Part 4), the conflict identification (Part 5), and the co-design methodology (Part 9) — but does not prescribe the compound resolution.



---

### §5.2 Conflict Resolution Table

Eleven environmental parameters produce direct conflicts between population-specific specifications. For each conflict: the opposing specifications are stated, the governing resolution is identified, and the guidebook item cross-references are given. Conflicts are classified by resolution status using the definitions in §5.1

Resolution evidence quality is marked: ● = Tier 1–3 OT clinical or post-occupancy evidence; ◐ = Tier 3–5 consensus or standards; ○ = Tier 5–6 expert consensus with no outcome data.

Strategy codes (§3.9): **IEC** = Individual Environmental Control; **SZ** = Sensory Zoning; **TS** = Technical Specification; **DAR** = Design for Adaptable Readiness; **SRW** = Shared Route/Space with modifications; **PP** = Parallel Provision; **T0** = Tier 0 Safety-Critical Governs; **OT-REF** = OT Assessment Required; **RS** = Range Specification (serves both populations within a defined range).

| Domain | Pop A | Pop B (and others) | Pop A specification | Pop B specification | Resolution | Status | Evidence |
|---|---|---|---|---|---|---|---|
| **COLOUR-CONT — Luminance contrast (LRV)** | VIS, DEM | NDV/SENS, NDV/AUT | ≥30% LRV differential at all step edges, door frames, counter edges, platform edges (C-04); ≥50% at critical junctions (best practice) | Muted palette; ≤20 LRV differential in sensory retreat zones; no high-contrast pattern in quiet spaces | Zone-based: ≥30 LRV contrast on all primary accessible routes (Zone 1/2 — safety-critical; governs over NDV sensory comfort); ≤20 LRV in sensory retreat spaces (Zone 3 — NDV comfort served; VIS orientation via wall contrast and architectural landmarks rather than floor-level contrast). Plain floor (C-06) throughout primary routes satisfies both: DEM fall prevention + VIS orientation via perimeter contrast rather than surface pattern. | RESOLVED-EVIDENCE · **SZ + PP** | ● DSDC EADDAT 2022 (DEM plain floor; +15% pattern-associated falls); ◐ CNIB 2024 (VIS contrast minimum); ◐ PAS 6463:2022 (NDV muted palette). Cross-ref: C-04, C-06, F-01. |
| **ACOUSTIC-LVL — Amplification and background noise** | DEAF, CI users | NDV/SENS, NDV/AUT, NEU/PCS | Hearing loop (IEC 60118-4) in all assembly spaces, counters, and classrooms; STI ≥0.75 for DEAF/CI (Iglehart 2020) | No amplification or broadcast audio in sensory retreat and quiet zones; background noise ≤30 dBA (Zone 3); no sound masking (A-13) | Hearing loop amplifies direct speech pickup without requiring broadcast audio. Audio input to loop system is independently controlled from PA and background music circuits. Loop zone on IEC 60118-4 with dedicated direct-input microphone; PA and broadcast audio muted in Zone 3 areas. RT60 ≤0.3 s in NDV co-occurrence spaces (the stricter NDV target governs where both populations share space; acoustic calm serves NDV while exceeding DEAF speech clarity requirement). RT60 ≤0.4 s in DEAF-only spaces without NDV co-occurrence (DIN 18041 Nutzungsart A3/A4; BS 8300-2:2018 §11). No sound masking in any space where NDV is a primary population. | RESOLVED-CONSENSUS · **SZ + IEC** | ◐ IEC 60118-4:2022 (loop zones and field strength); ● Iglehart 2020 AJA (RT60 ≤0.3 s, CI/HA speech scores); ◐ PAS 6463:2022 (NDV no masking). Cross-ref: A-10, A-11, A-13. |
| **GRAB BAR DIAMETER — Grip profile** | MOB (standard grip) | UPL (upper limb pathology) | 32–38 mm preferred circular (ISO 21542; BS 8300); avoid knurled | 32–45 mm; oval permitted where equivalent grip perimeter; 45–50 mm where ≥250 kg static load rating required (BAR/structural — Supp Vol IV) | Range specification: 32–45 mm serves both populations. Circular cross-section preferred for both. Oval permitted where structural integration requires flat-wall mounting (equivalent perimeter calculation). Below 32 mm: inadequate for standard grip. Above 45 mm: UPL grip strength reduces; standard MOB population also degrades. | RESOLVED-EVIDENCE · **RS** | ● BS 8300:2018 (32–45 mm range); ◐ ISO 21542:2021 (circular preferred); ◐ Guay 2020 (Clinical Biomechanics, biomechanical load). Cross-ref: G-03. [OPG-05: RS = Range Specification — 32–45 mm is the designed-in bridge between MOB and UPL specifications.] |
| **TEMP-RANGE — Ambient temperature** | NEU/MS (Uhthoff's phenomenon) | PAIN (fibromyalgia, chronic pain) | ≤18°C in primary activity spaces (heat-induced demyelination worsening is safety-critical; Tier 3 clinical evidence — Uhthoff's mechanism, 60–80% MS prevalence, MSIF Atlas 2023) | 22–24°C preferred; cold contact with metal surfaces triggers PAIN allodynia | Ambient at ≤18°C governs (MS/NEU safety-critical — heat causes neurological worsening, not discomfort). Warmth delivered individually: radiant panel at each regular seat/workstation; heated grab bar coatings; personal thermal options at all workstations. OFS: ambient ≤18–20°C; individual supplemental heating provides PAIN population warmth without raising shared ambient. | RESOLVED-CONSENSUS · **T0 + IEC** | ● Uhthoff 1890/Davis 2010 Neurology (Uhthoff's mechanism); ◐ Staud 2011 (PAIN allodynia); ◐ ms-thermal-temperature-conflict-resolution BPC. Cross-ref: F-07, F-08. [T0: ambient <=18C is safety-critical — Uhthoff mechanism governs. IEC: individual supplemental radiant heating delivers PAIN warmth without raising shared ambient.] |
| **SURFACE-TEXT — Tactile floor indicators** | VIS, DBL | PAIN (vibration sensitivity), MOB/AMB (wheel and frame resistance) | Full ISO 23599:2019 truncated dome profile on primary accessible routes (detectable warning function — safety-critical for VIS route boundary marking) | Smooth surface preferred; textured indicators create vibration pain trigger (PAIN fibromyalgia); wheel and frame resistance (MOB ambulant) | Safety-critical: ISO 23599 truncated dome on primary accessible routes governs (VIS/DBL detectable warning is safety function). Partial resolution for secondary routes: high-contrast flush edging strip (colour + LRV ≥30) provides orientation cue without raised profile; accepted VIS Tier 3 compromise on secondary circulation. PAIN wheel/frame resistance: resolved by truncated dome sizing per JIS T9251 (dome height 5 mm, base diameter 25 mm, dome centre spacing 60 mm) — the only parameter with full empirical resolution evidence across both populations. Residual gap: no product currently meets both full ISO 23599 profile and vibration attenuation for PAIN. | PARTIAL · **T0** | ◐ ISO 23599:2019 (profile specification); ◐ JIS T9251 (dome sizing, conflict-resolved empirically in JP context); ○ PAIN vibration sensitivity (expert consensus, no comparative product study). Cross-ref: C-04, E-09. [T0: VIS/DBL safety-critical detectable warning governs on primary routes.] |
| **SPATIAL-OPEN — Visual transparency and spatial enclosure** | DEAF | NDV/AUT, NDV/SENS | Glazed corridor junctions (DeafSpace visual advance warning; matte/low-reflectance specification — see §5.3); open-plan layouts ≥2400 mm primary corridor width for signing pairs | Compartmentalised zones with predictable, enclosed approaches; ≤sensory complexity | Graduated spatial model: open circulation spine (≥1500 mm minimum accessible width; ≥2400 mm where signing is the primary communication mode — DeafSpace Guidelines 2010) transitions to enclosed sub-zones (sensory-reduced areas, quiet rooms). Glazed junctions: low-reflectance, matte glazing at corridor junctions for DEAF visual advance warning; etched or frosted lower band maintains signing sightline while reducing visual noise for NDV. Open/enclosed gradient follows F-01 sensory zone logic. Prospect-refuge balance (Appleton 1975; CON-0024): circulation spine provides prospect (open sightlines); alcoves and quiet rooms provide refuge (enclosure). | RESOLVED-CONSENSUS · **SZ** | ◐ DeafSpace Guidelines 2010 (glazed junctions); ◐ PAS 6463:2022 (NDV enclosure preference); ○ Prospect-refuge theory (Appleton 1975; Dosen & Ostwald 2016 meta-analysis). Cross-ref: E-08, F-01, D-05. [SZ: graduated spatial model — open spine/enclosed sub-zones resolves DEAF vs NDV spatial preference through zone differentiation.] |
| **LIGHT-INT — Illuminance (lux and EML)** | DEM, VIS | NDV/AUT, NDV/SENS, NEU/PCS, PAIN, OFS | DEM circadian: ≥300 lux at eye level daytime (DSDC 2024); ≥250 melanopic EDI (Brown 2022); ≥500 lux task surfaces (VIS task performance) | NDV: ≤200 lux ambient preferred; dimmable to ≤50 lux in sensory retreat; OFS/PCS: glare contraindicated; no cool-white CCT in sensory-sensitive zones | Three-zone illuminance model: Zone 1 (high activation — circulation, assembly): ≥300 lux ambient / ≥500 lux at task surfaces / ≥200 EML daytime; Zone 2 (moderate — workspace, consultation): 150–300 lux at workplane, ≥500 lux at task surfaces (user dimmable); Zone 3 (low activation — sensory retreat, quiet rooms): user-controlled 0–150 lux, ≤50 lux available. Individual dimming (B-06) at every primary work position is the single highest-impact conflict mitigation: it resolves the DEM/VIS vs NDV/OFS illuminance conflict for any user who can operate the control. CCT: ≥4000 K in DEM circadian areas during morning; ≤2700 K in all spaces from 19:00; user-controllable CCT where NDV/DEM co-occurrence is primary. | RESOLVED-CONSENSUS · **SZ + IEC** | ● Brown 2022 (melanopic EDI ≥250 consensus, 13 jurisdictions); ◐ DSDC EADDAT 2022 (DEM ≥300 lux); ◐ PAS 6463:2022 (NDV ≤200 lux ambient). Cross-ref: B-01, B-06, B-07, B-11, F-01. [SZ: three-zone illuminance model. IEC: individual dimming (B-06) is the highest-impact single conflict mitigation.] |
| **VIS-COMPLEX — Signage and visual information density** | DEM, DEM/NDV[IntD-proxy] | NDV/SENS | High-redundancy signage: pictogram + word + Braille + colour coding at all junctions (D-08, D-09); colour zone wayfinding | Minimal visual clutter; muted palette; ≤3 sign elements per decision point; no high-contrast pattern | Signage resolution: pictogram + word + Braille system (D-08) satisfies both — pictograms serve DEM/NDV[IntD-proxy] (simple symbol ≤3 elements); matte, non-reflective sign field serves NDV/SENS (no visual noise from glossy surfaces). Colour zone wayfinding: consistent, non-saturated colour differentiation by zone (DEM spatial orientation) — same system provides NDV predictability if zones are consistent and limited in number (≤5 zones per building). High-contrast pattern is the site of genuine tension: DEM benefits from colour contrast differentiation at junctions; NDV/SENS benefits from plain surfaces. Resolution: contrast at architectural elements (door frames, skirting, transition edges) rather than floor surface patterns. | RESOLVED-CONSENSUS · **PP** | ◐ DSDC EADDAT 2022 (DEM signage); ◐ PAS 6463:2022 (NDV visual clutter); ○ DEM/NDV[IntD-proxy] signage (NICE NG93; BILD expert consensus). Cross-ref: D-04, D-08, D-09. [PP: pictogram+word+Braille (D-08) independently satisfies DEM and NDV/SENS cognitive access needs.] |
| **MOVE-FREE — Circulation freedom vs supervised pathways** | DEM (wandering freedom) | MOB/fall risk (supervised paths) | Unobstructed loop floor plan (D-01); no dead ends; continuous supervised circulation for DEM; all routes passable independently | Contained pathways with support surfaces; no obstacles; consistent bilateral grab bar provision on extended routes | Outdoor: secure garden loop with bilateral handrails (G-05) at garden perimeter satisfies both — DEM freedom within supervised perimeter; MOB fall support throughout loop. Indoor: grab bars on extended corridor routes (G-05) provide MOB support; DEM wandering permitted on all carpeted grab-bar routes. Genuinely irreconcilable in public buildings where MOB fall supervision conflicts with DEM freedom: resolved as Tier 2 (OT assessment required for individual programme design). | RESOLVED-CONSENSUS (residential); TIER-2-ONLY (institutional) · **SRW** (residential) · **OT-REF** (institutional) | ◐ DSDC EADDAT 2022 (DEM loop; freedom of movement); ◐ Clemson 2023 Cochrane CD013258 (fall prevention, grab bars). Cross-ref: D-01, D-11, G-05. [SRW: shared route with bilateral grab bars. OT-REF: institutional non-zoned shared space requires OT assessment.] |
| **FRAGRANCE — Olfactory environment** | OFS/MCAS, NDV/SENS | DEM (olfactory orientation therapy) | Zero fragrance throughout: F-02 fragrance-free zones; F-06 whole-building policy | Scented environmental cues (familiar food smells, floral scents) for DEM spatial orientation and wellbeing | Genuine tension with no fully satisfactory population-level resolution. Mitigation: fragrance-free policy (F-06) as building-wide baseline; DEM olfactory cueing via food smells (kitchen adjacency, dining visibility) and natural scents (lavender planting ≥600 mm from circulation edge, per nature provision guidelines) rather than chemical fragrances or air fresheners. Natural food smells are not chemical triggers for OFS/MCAS; synthetic fragrances are. DEM orientation cues can be architectural-spatial (cooking smells from kitchen at corridor junction) rather than applied fragrance. Residual gap: some DEM dementia village programmes use synthetic lavender diffusers — contraindicated for OFS/MCAS populations and should not be specified in shared buildings. | PARTIAL · **PP** | ◐ Afrin 2020 (MCAS chemical triggers); ◐ DSDC EADDAT 2022 (DEM olfactory cues); ○ natural vs synthetic distinction (expert consensus). Cross-ref: F-02, F-03, F-06. [PP: architectural-spatial food/natural scent cues provide DEM olfactory orientation without chemical fragrance — parallel provision that does not trigger OFS/MCAS.] |
| **DOOR-OPERATION — Automatic vs manual door actuation** | MOB (force-free access) | NDV/MH (predictability; startle response) | Automatic doors: no push force; 10-second hold-open; power-assisted throughout | Predictable actuation; no unexpected movement; advance visual and auditory warning before door opens | Motion sensor at ≥3 m (visual warning zone before door activates); auditory chime (≤65 dBA at 1 m) on sensor trigger; glazed door leaf (NDV spatial preview before entry); ≥3 seconds opening travel (no sudden movement); high-contrast floor activation zone (C-04 ≥30 LRV). Combined: MOB receives force-free access; NDV/MH receives predictable, pre-announced door movement with visual advance notice. | RESOLVED-CONSENSUS · **TS** | ◐ PAS 6463:2022 (NDV door predictability); ◐ BS 8300:2018 (automatic door performance); ◐ DeafSpace 2010 (glazed leaf visual preview). Cross-ref: E-11, C-04. [TS: integrated door specification (sensor range + auditory chime + glazed leaf + travel speed) resolves both populations through a single technical solution.] |

---

### §5.3 Unresolvable Conflicts Register

Three conflict types remain unresolvable at Tier 0–1 for shared ambient environments. Each is recorded here with its Tier 2 requirement and the specific condition that triggers mandatory individual co-design.

**CONF-UNRESOLV-01 — Ambient temperature (OFS/NEU/MS vs PAIN/fibromyalgia in a non-zoned space)**

The thermal resolution in §5.2 (≤18°C ambient + individual supplemental heating) resolves the NEU/MS vs PAIN conflict for most building configurations. The residual unresolvable case is a non-zoned shared sleeping space — a hospital bay, a care home bedroom corridor, or a dormitory — where ambient temperature is truly shared and where individual supplemental heating is not operationally feasible. In this configuration, ≤18°C ambient governs (safety-critical: Uhthoff's mechanism), and the PAIN population's thermal need is carried by: (1) insulated coated grab bars (G-03 thermal provision); (2) warm bedding specification; and (3) individual heated throw or vest as an FM provision. The design cannot resolve this without individual assessment. OT assessment is mandatory where a building or space will simultaneously serve a person with MS-spectrum diagnosis and a person with fibromyalgia or cold-aggravated pain in a shared non-zoned sleeping space.

**CONF-UNRESOLV-02 — Acoustic amplification and NDV/AUT in a shared open-plan space**

Where a hearing loop or sound field system (A-11, A-12) serves DEAF and CI users in an open-plan space, and NDV/AUT users occupy the same open-plan space without physical separation, the ambient acoustic level produced by the loop system conflicts with the NDV/AUT noise sensitivity requirement. The NDV/AUT provision (A-13 no sound masking; ≤35 dBA ambient in NDV-primary zones) cannot be achieved in the same zone as a hearing loop operating at its prescribed output. Zoning resolves this in most institutional buildings (separate classrooms, consultation rooms). In open-plan co-working or retail environments where NDV and DEAF users occupy the same space simultaneously, individual wireless receiver technology (A-12 Auracast or equivalent personal receiver system) is the technical resolution — but its availability does not reduce the DEAF user's right to an accessible ambient environment if a personal receiver is not available or desired. Flag for OT assessment where building brief explicitly includes both NDV/AUT and DEAF populations in a shared open-plan space without physical zone separation.

**CONF-UNRESOLV-03 — Visual glazing (DEAF DeafSpace junctions vs DEM reflective surface confusion and NDV visual noise)**

Glazed corridor junctions (DEAF visual advance warning provision — §5.2 SPATIAL-OPEN) conflict with DEM reflective surface contraindication and NDV visual complexity. The matte/low-reflectance glazing specification in §5.2 partially mitigates both. The residual unresolvable case is a DEAF primary building (school for the Deaf; DEAF-majority workplace) where maximised glazing area is specified for signing visibility, and where DEM or NDV populations are secondary occupants. No single glazing specification fully satisfies: high-transmittance clear glass (DEAF signing) vs matte/etched glass (DEM reflection contraindication). Mitigation: clear glass upper band (>1400 mm AFF — signing sightline); frosted or etched lower band (≤1400 mm AFF — reduces floor-level reflections; lowers visual noise field). This is a dimensional compromise, not an evidence-based resolution. Where DEAF is the primary population, DEAF signing requirements govern; DEM/NDV mitigation is applied as far as possible within that constraint.

---

*§5.4 Worked Examples — Building-Level Co-Occurrence Resolution: to be drafted in Phase 3, Session 2. See part04_v9-0 worked examples (§3.11) for cross-population synthesis examples pending formal §5.4 extraction.*

---

**Cross-references to update:** Part 3 §3.4 references to "Part 8 §8.4" should be updated to "Part 5 §5.2" following this section's completion. See GAP-CONF-02 for tracking.


---

### §5.4 Application to Design Stages — Worked Examples

The conflict resolution table in §5.2 operates at design stage: conflicts must be identified before schematic design closes, resolutions built into the brief, and parameter choices propagated into each consultant's scope. The three examples below trace the §5.2 entries through actual design decisions for three common building types. They are not exhaustive; they demonstrate the method.

---

#### §5.41 Worked Example A: Dementia Care Home (DEM Primary; MOB Secondary; NDV/SENS Tertiary — Staff)

**Population brief.** 24 residents: DEM (all residents, by definition of facility type); MOB (20 of 24 — ambulant with walking aids or wheeled mobility); NDV/SENS (estimated 4 of 14 staff — UK CIPD 2023 prevalence data applied to care workforce).

**Active conflict domains at schematic:**

*COLOUR-CONT.* DEM requires high contrast at all threshold and step edges (DEM fall prevention — safety-critical). NDV/SENS staff require a muted palette in staff areas. Resolution: §5.2 zone-based — high-contrast provisions (C-04, ≥30 LRV) throughout resident circulation and all resident-occupied spaces. Staff workstation and staff rest room carry ≤20 LRV palette. The two populations occupy distinct spatial zones; the conflict is resolved spatially rather than by specification compromise.

*LIGHT-INT.* DEM circadian lighting (≥300 lux daytime, ≥250 melanopic EDI) governs in all resident-occupied spaces. NDV/SENS staff require dimmable lower-intensity ambient in staff areas. Resolution: §5.2 three-zone model — Zone 1 (resident common rooms): ≥300 lux circadian; Zone 2 (corridors): 150–300 lux dimmable; Zone 3 (staff office, sensory room): user-controlled 0–150 lux. Individual dimming (B-06) at all staff workstations resolves the residual illuminance conflict without reducing circadian provision for residents.

*MOVE-FREE.* DEM residents benefit from autonomous wandering within a legible loop. MOB residents require bilateral grab bars on all extended routes (G-05). Resolution: §5.2 — secure garden loop with continuous bilateral handrails satisfies both. Indoor loop circulation with grab bars on all corridors ≥15 m: DEM freedom maintained; MOB fall support provided throughout.

*FRAGRANCE.* DEM olfactory orientation (cooking smells as spatial cues) vs NDV/SENS staff chemical sensitivity. Resolution: §5.2 partial — food smells from kitchen at corridor junction provide DEM olfactory cue without synthetic fragrance triggers. F-06 fragrance-free policy governs cleaning products and staff personal fragrance; natural food smells are not OFS/MCAS triggers. NDV/SENS staff protected; DEM orientation cues preserved via architectural adjacency.

**Design stage actions generated:**
- SD: loop floor plan (D-01), zone boundary positions on schematic, kitchen adjacency to main corridor, secure garden with loop path
- DD: B-06 dimming circuits by zone; C-04 LRV schedule (≥30 in resident areas; ≤20 in staff areas); G-05 grab bars on all corridors ≥15 m; F-06 fragrance-free policy in FM brief
- CD: lighting control commissioning; TWSI at all stair heads (E-09)

---

#### §5.42 Worked Example B: Neurodivergent Co-Working Office (NDV Primary; DEAF Secondary; OFS Tertiary)

**Population brief.** 60-person co-working office; 25% NDV/AUT/ADHD (client disclosure); 2 DEAF staff (hearing aid users); 8% OFS (ME/CFS, POTS, MCS — self-disclosed).

**Active conflict domains at schematic:**

*ACOUSTIC-LVL.* DEAF staff require hearing loop (A-11) in all meeting rooms and the collaboration zone. NDV/AUT and NDV/ADHD staff require ≤35 dBA ambient in quiet zones; no sound masking (A-13). Resolution: §5.2 — hearing loop operates on direct microphone input, not broadcast audio; PA and background music muted in NDV-primary zones. RT60 ≤0.3 s universal (serves both DEAF speech clarity and NDV acoustic calm). Result: loop infrastructure throughout; audio input control at zone level; no masking anywhere.

*SPATIAL-OPEN.* DEAF staff benefit from open-plan layouts with sightlines for signing pairs. NDV/AUT staff benefit from enclosed sub-zones with predictable approaches. Resolution: §5.2 graduated model — open-plan collaboration spine (≥1500 mm, signing-compatible) transitions to enclosed acoustic pods (NDV quiet zones, RT60 ≤0.3 s, NC ≤20). DEAF staff primary workstations on open-plan spine; NDV/AUT staff primary workstations in or adjacent to enclosed pods with open-plan access.

*LIGHT-INT.* NDV/ADHD staff: individual dimming (≤200 lux ambient preferred in quiet zones). OFS/PCS staff: glare contraindicated; cool-white CCT triggers photophobia symptoms. Resolution: §5.2 — B-06 individual dimming at every desk; B-07 UGR <19 universal (eliminates glare for OFS without reducing task light for DEAF); B-04 flicker-free LED throughout (NDV and OFS both benefit); CCT ≥4000 K in collaboration zone (circadian and visual acuity); ≤3000 K in quiet zones and at OFS-designated workstations.

*FRAGRANCE.* OFS/MCAS: fragrance-free building policy (F-06). NDV/SENS: same requirement via sensory sensitivity mechanism. No conflict — both populations require F-06. Result: single policy serves both; no resolution required.

**Design stage actions generated:**
- SD: open-plan spine vs pod layout ratio; pod locations on floor plan; AC and EE briefs at schematic (RT60 targets; loop wiring routes)
- DD: hearing loop field strength diagram; B-04/B-06 specification; F-06 in FM brief and lease agreement
- CD: per-desk dimming control; loop commissioning; fragrance-free signage

---

#### §5.43 Worked Example C: Mixed-Needs Supported Housing (DEM + MOB + NEU/MS + PAIN)

**Population brief.** 12 apartments; 4 residents DEM (older adults); 8 residents MOB (4 manual wheelchair, 4 ambulant with walking aids); 3 residents NEU/MS (two with Uhthoff's phenomenon); 2 residents PAIN (fibromyalgia, diagnosed MS-fibromyalgia overlap).

**Active conflict domains at design:**

*TEMP-RANGE.* The MS population requires ≤18°C ambient (Uhthoff's — safety-critical). The PAIN population requires warmth (fibromyalgia — cold worsens allodynia). Populations share corridor circulation. Resolution: §5.2 — ≤18°C ambient in all common areas and corridors governs (safety-critical, MS). Individual apartments: individual thermostats (TC-02) allowing residents to set their own thermal environment. Communal spaces: individual radiant heating supplement at all fixed seating positions (portable or wall-mounted radiant panels at ≤22°C output). PAIN residents receive warmth at their own fixed positions; NEU/MS residents retain cool ambient. Insulated grab bar coatings (G-03) throughout — cold metal contact triggers allodynia.

*DOOR-OPERATION.* MOB residents require automatic doors (E-11) at communal entries. DEM residents: §5.2 DOOR-OPERATION resolution applies (motion sensor ≥3 m advance warning; auditory chime; glazed leaf; ≥3 s travel). The automatic door design specified for MOB already incorporates the DEM resolution elements. No additional specification required — single specification serves both.

*COLOUR-CONT.* DEM: plain floor (C-06) in communal areas; high contrast at door frames (≥30 LRV, C-04). MOB: no floor pattern preference; contrast at step edges. NEU: no specific contrast requirement beyond universal. Result: plain floor throughout communal areas satisfies DEM (no pattern-associated falls) and MOB (no trip texture). Perimeter contrast (C-04 at door frames and skirting) satisfies DEM orientation; no population requires floor pattern.

*MOVE-FREE (Tier 2 conflict).* DEM wandering freedom vs MOB powered-wheelchair turning radius: a powered-wheelchair user executing a turn on a loop corridor may temporarily reduce circulation space. In a 12-apartment building on a single loop, the corridor specification (E-08 ≥1500 mm clear; preferred 1800 mm) accommodates both the DEM ambulant wandering user and the powered-wheelchair turning envelope. No architectural conflict at 1800 mm clear. Conflict is irresolvable only if corridor drops below 1500 mm — avoided at schematic.

**Design stage actions generated:**
- SD: corridor ≥1800 mm clear; loop floor plan (D-01); TC-02 individual thermostats in all apartments; supplement heating provision noted in FF&E brief
- DD: G-03 insulated grab bar finish (cold-contact note in specification); E-11 automatic doors all communal entries; radiant panel positions at communal fixed seating
- CD: B-05 gradual light transitions at building entry (OFS/MS photophobia); TC-01 ≤18°C controls confirmed for common-area HVAC

---



### §5.5 Process Specification — The Environment Is Necessary But Not Sufficient

#### §5.5.1 The Evidence Finding

Two Tier 1 findings converge on the most consequential scope question for this guidebook. Douglas et al. (2024, BMJ Open) studied tenants of purpose-built Specialist Disability Accommodation in Australia and found that support quality — the competence and consistency of the people delivering care — was a greater determinant of quality of life than the built environment itself. Ainsworth et al. (2022, Disability and Rehabilitation, PMID 36394257) found that housing adaptation outcomes were co-produced by the environment and the OT process quality: therapists who understood the client's experience of home as their starting point achieved better outcomes than therapists who began with the physical assessment alone.

The implication is structural. A perfectly specified building with poor support produces worse outcomes than a modestly specified building with excellent support. The guidebook's specifications — Parts 4 through 8 — address one half of the equation. This section addresses the other half: the process framework that determines whether built environment provisions translate into lived outcomes.

#### §5.5.2 The CAPABLE Model — Validated Multicomponent Framework

The strongest evidence for a residential process framework comes from the CAPABLE programme (Community Aging in Place, Advancing Better Living for Elders). The definitive RCT (Szanton et al. 2019, JAMA Internal Medicine, PMID 30615024, n=300) demonstrated a 30% reduction in ADL disability (RR 0.70, 95% CI 0.54–0.93, p=0.01) using a three-component model: occupational therapist assessment, registered nurse clinical intervention, and handyperson environmental modification. Six replications across 12 US sites (Szanton et al. 2021, n=1,144) confirmed effect sizes of 0.41–1.47 across all sites.

The CAPABLE model establishes that residential accessibility outcomes require three concurrent inputs, not one. The built environment modification (this guidebook's domain) is the handyperson component. Without the OT assessment directing the modification and the clinical intervention addressing the person's functional trajectory, the modification alone produces smaller and less durable effects.

For residential projects, the process specification is:

1. **OT assessment precedes specification.** The OT assessment determines which guidebook provisions apply to the individual. Part 9 §9.2 defines the OT scope. The assessment must precede the architectural brief for Tier 2 residential work. For Tier 0–1 provisions, the assessment confirms the baseline is correct; for Tier 2 provisions, it resolves the individual's position within specification ranges.

2. **Assessment uses validated instruments.** Malmgren Fänge et al. (2019, PMID 31684916) demonstrated that standardised OT housing assessment produces measurable functional outcomes — OR 9.50 for wheelchair mobility improvement. Unstandardised assessment produces unquantifiable outcomes. The Housing Enabler (Iwarsson & Slaug 2001) and CAPABLE assessment protocol are the validated instruments with the strongest evidence base.

3. **Transition planning is co-primary with design.** Carey et al. (2025, PMID 41175339) documented that families and carers of people with neurological conditions require structured transition support when moving to purpose-built accessible housing. The transition itself — not the destination — is a critical risk period. Design teams must coordinate with support providers on transition timing, orientation programmes, and carer training before occupancy.

4. **Ongoing support quality must be specified.** The ILMI (2021, Ireland) and Douglas et al. (2024) evidence establishes that post-occupancy support frameworks are not ancillary to housing outcomes — they are co-determinant. For supported housing, the design brief must name the support model alongside the built environment specification. Part 9 §9.2 provides the OT coordination protocol.

#### §5.5.3 Relationship to Room Matrices (Parts 6 and 7)

The room matrices in Parts 6 and 7 specify environmental provisions. This section specifies the process provisions that govern whether those environmental provisions produce outcomes. The two are co-primary. A residential project that specifies Part 6 room matrices without the process framework described here has addressed the building but not the living. A project that specifies the process framework without the room matrices has addressed the support but not the environment. Both are required.

#### §5.5.4 Evidence Base

| Source | Tier | Key Finding |
|---|---|---|
| Szanton et al. 2019 (JAMA Intern Med, PMID 30615024) | 1 RCT | 30% ADL disability reduction with OT+nurse+handyperson model (n=300) |
| Szanton et al. 2021 (J Am Geriatr Soc, PMID 34314516) | 1 multi-site | Effect sizes 0.41–1.47 across 6 replications (n=1,144) |
| Douglas et al. 2024 (BMJ Open) | 1 qualitative | Support quality > built environment for QoL in SDA housing |
| Ainsworth et al. 2022 (Disabil Rehabil, PMID 36394257) | 1 qualitative | Outcomes co-produced by environment + OT process quality |
| Malmgren Fänge et al. 2019 (PMID 31684916) | 1 quasi-experimental | Standardised OT assessment: OR 9.50 wheelchair mobility |
| Carey et al. 2025 (PMID 41175339) | Co-1 | Family/carer transition support essential for neurological conditions |
| Sheffield et al. 2013 (PMID 23213082) | 1 RCT | 39% personal care hour reduction with OT home modification |
| ILMI 2021 | Co-1 | Support alongside housing — advocacy evidence from Ireland |

*Cross-reference: Part 9 §9.2 (OT scope); Part 9 §9.10 (OT threshold); Part 11 §11.3.5 (economic evaluation of CAPABLE model); CS-22 (CAPABLE case study in compendium).*

---

*End of Part 5. Cross-references: Part 3 §3.4 (Co-occurrence guidance by pair); Part 4 §3.11 (Population-specific worked examples); Part 7 (Non-residential population matrices); Part 9 §9.6 (DeafBlind specialist consultant).*

