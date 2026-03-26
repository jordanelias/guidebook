# Research Output — Mixed High-Impact Cluster
**Session:** 2026-03-26  
**Gaps addressed:** GAP-STEP5-01 (P1), GAP-RAP-06 (P2), GAP-SRS-01 (P2), GAP-034 (P2)

---

## 1. GAP-STEP5-01 — B-10 Strobe VAD Seizure Risk (P1 SAFETY)

### Issue
B-10 (Visual Fire Alarm Strobe VAD) specifies BS EN 54-23 compliant VADs at 1–3 Hz flash rate. This rate falls within or near the photosensitive seizure trigger range. Item does not disclose seizure risk for NEU (epilepsy) or NDV/AUT populations.

### Evidence Retrieved

**Clinical threshold data:**
- Seizure-triggering flash frequencies: 3–30 Hz is the primary risk range; sensitivity below 3 Hz is uncommon but not zero (Epilepsy Society UK; Angelini Pharma citing Martins da Silva & Leal 2017, Seizure 50:209-218, PMID: 28532712)
- Epilepsy Foundation Professional Advisory Board recommends flash rate below 2 Hz with breaks between flashes
- Prevalence: ~1 in 4,000 general population; ~5% of people with epilepsy are photosensitive
- Risk factors: magnitude of flash, colour (red-blue most provocative), flash count per time frame, area of flash in visual field — all four must combine (Jordan & Vanderheiden 2024, ACM TACCESS 17(3):1-35, PMC11872230, DOI: 10.1145/3694790)

**Fire alarm standards — flash rate specifications:**

| Standard | Flash rate | Synchronisation requirement |
|---|---|---|
| BS EN 54-23:2010 | 0.5–2 Hz | Synchronisation function to prevent composite rates causing adverse effects including epileptic fits |
| NFPA 72 (US) | Changed from <3 Hz to <2 Hz in 1996 | ≤2 strobes in any field of view unsynchronised; >2 must be synchronised to prevent composite rate reaching 5 Hz |
| ADA/ADAAG (US) | Defers to NFPA 72 | — |

**Key finding — safety conflict confirmed:**
- BS EN 54-23 specifies 0.5–2 Hz. The standard itself acknowledges the epilepsy risk by requiring a synchronisation function specifically to avoid inducing epileptic fits (Apollo Fire Detectors technical note, 2025)
- NFPA 72 reduced from 3 Hz to 2 Hz specifically because adjacent unsynchronised strobes could create composite rates reaching 5 Hz — within the seizure trigger range
- Jordan & Vanderheiden (2024) gap analysis of international PSE guidelines notes that building alarm systems are not currently covered by content accessibility guidelines (WCAG, ITU-R BT.1702, Ofcom) — a gap in protection
- NFPA 72-2022 public input record includes submissions from DARAC (Disability Access Review and Advisory Committee) noting that notification appliances can "frighten or cause undue panic" in autistic populations and small children; DARAC recommends voice alarm systems for these environments

**Alternative VAD designs (non-strobe):**
- BS EN 54-23 applies only to pulsing or flashing devices; continuous light output devices are explicitly excluded from its scope — meaning continuous-light alternatives are not currently certifiable under EN 54-23
- No current standard certifies diffuse-light or continuous-light VADs as primary fire notification devices
- Best available mitigation: synchronisation (to prevent composite rates), low flash rate (0.5–1 Hz), minimum necessary candela intensity, and supplementary notification via vibrotactile devices and voice alarm systems

### Specification Recommendation for B-10

Add safety conflict note to B-10:

> **Safety Note — Photosensitive Seizure Risk:** VAD flash rates of 0.5–2 Hz (BS EN 54-23) are below the primary seizure trigger range (3–30 Hz) but composite flash rates from multiple unsynchronised devices can reach hazardous frequencies. Where NEU (epilepsy), NDV/AUT, or PCS populations are primary occupants: (a) all VADs must be synchronised per BS EN 54-23 §synchronisation or NFPA 72 §18.5.4.3; (b) flash rate set to minimum effective (0.5–1 Hz preferred); (c) supplementary notification via vibrotactile and/or voice alarm system (NFPA 72-2022 DARAC recommendation); (d) candela output set to minimum coverage volume requirement, not maximum. ● [Tier 3–4; Jordan & Vanderheiden 2024; BS EN 54-23:2010; NFPA 72-2022]

Add NEU (epilepsy) and NDV/AUT to B-10 Applicable Groups.

### Evidence Tier
Tier 3 (Jordan & Vanderheiden 2024 — gap analysis/review) + Tier 4 (BS EN 54-23; NFPA 72) + Tier 6 (ADA requirements). Safety conflict is Tier 3 confirmed.

### Gap Status
**GAP-STEP5-01: RESOLVED** — safety disclosure language drafted; evidence confirmed; ready for item-specification-writer.

---

## 2. GAP-RAP-06 — DEAF-Specific RT60 ≤0.3s Target

### Issue
ANSI/ASA S12.60-2010/Part 1 specifies RT60 ≤0.3s for classrooms with hearing-impaired students (≤283 m³). Guidebook does not state a DEAF-specific RT60 sub-target; general target is ≤0.5–0.6s.

### Evidence Retrieved

**Primary source — Iglehart (2020):**
- Iglehart, F. (2020). Speech Perception in Classroom Acoustics by Children With Hearing Loss and Wearing Hearing Aids. *American Journal of Audiology*, 29(1), 6–17. DOI: 10.1044/2019_AJA-19-0010. PMID: 31835909. PMC7229780.
- **Findings:** First peer-reviewed published data comparing 0.3s vs 0.6s RT for children with hearing aids. Children achieved >90% speech perception at +15 dB SNR only in 0.3s RT, not in 0.6s RT. Sound booth testing did not predict classroom performance at 0.3s RT.
- **Conclusion:** Directly supports the ANSI/ASA S12.60-2010 requirement of 0.3s RT for hearing-impaired learners.
- **Evidence tier:** Tier 1 (OT-adjacent clinical research — audiology intervention, person-environment-occupation alignment)

**Standard specification:**
- ANSI/ASA S12.60-2010/Part 1, Table 1 Footnote e + Section 5.3.2: core learning spaces ≤283 m³ "shall be readily adaptable to allow reduction in reverberation time to 0.3 s"
- Annex B Commentary-5.3.1: "a reverberation time of 0.3 s… is necessary for children with hearing impairment and/or other communicative issues"
- The 2002 version specified 0.6s for all students without differentiation; 2010 revision added the 0.3s hearing-impaired requirement

**Supporting evidence:**
- American Academy of Audiology (2023) Position Statement: confirms 0.3s requirement in revised standard
- ASHA (2018): cites +15 dB SNR as condition for "full" perception; achievable only in 0.3s RT
- Finitzo-Hieber & Tillman (1978): only other published study of hearing-aid users in classroom-like RTs — compared 1.2s to 0.4s; foundational but did not test 0.3s
- ANSI/ASA S12.60-2010 adopted into International Building Code (2016 edition) via A117.1

**Cross-jurisdictional status:**
- US: ANSI/ASA S12.60-2010 (mandatory where adopted via IBC/A117.1)
- UK: BB93 Acoustic Design of Schools (similar guidance; RT ≤0.6s general; ≤0.4s for hearing-impaired in some configurations)
- DE: DIN 18041:2016 — covers hearing-impaired classroom acoustics (identified in GAP-058)
- No equivalent DEAF-specific RT target found in FR, JA, ZH, KO standards

### Specification Recommendation for A-02/A-08 + NR-EDU Matrix

Add population-differentiated RT60 note:

> **DEAF-specific RT60 sub-target:** Where DEAF users (hearing aid or cochlear implant users) are primary occupants of a learning space ≤283 m³: RT60 target is ≤0.3 s (not the general ≤0.5–0.6 s). Spaces shall be designed to be readily adaptable to achieve this target. ● [Tier 1; Iglehart 2020, PMID: 31835909; ANSI/ASA S12.60-2010/Part 1 §5.3.2; DIN 18041:2016]

Add to NR-EDU matrix DEAF column.

### Evidence Tier
Tier 1 (Iglehart 2020) + Tier 4 (ANSI/ASA S12.60-2010; DIN 18041:2016)

### Gap Status
**GAP-RAP-06: RESOLVED** — specification language drafted; Tier 1 evidence confirmed; ready for item-specification-writer.

---

## 3. GAP-SRS-01 — Sensory Room A-16 User Control

### Issue
A-16 (Sensory Room) lists H-02 (Individual Environmental Control) as secondary cross-reference. Evidence suggests user control of sensory inputs is the primary design variable, more important than static environmental parameters.

### Evidence Retrieved

**Primary source — Unwin, Powell & Jones (2022):**
- Unwin, K.L., Powell, G., & Jones, C.R.G. (2022). The use of Multi-Sensory Environments with autistic children: Exploring the effect of having control of sensory changes. *Autism*, 26(6), 1379–1394. DOI: 10.1177/13623613211050176. PMID: 34693744. PMC9340127.
- **Design:** Within-subjects comparison; 41 autistic children aged 4–12 years; Active-Change (control) vs Passive-Change (no control) conditions in MSE
- **Findings:** Having control over sensory equipment was associated with: increased attention, reduced repetitive motor behaviours, reduced sensory behaviours, reduced activity levels, reduced stereotyped speech and vocalisations
- **Mechanism:** Consistent with predictive coding frameworks (Pellicano & Burr 2012; Van De Cruys et al. 2014) — autistic children benefit from environmental predictability; control provides this
- **Evidence tier:** Tier 3 (controlled comparison study, n=41, replicated in 2021 practitioner study and 2024 Italian replication)

**Supporting source — Unwin, Powell & Jones (2021):**
- Unwin, K.L., Powell, G., & Jones, C.R.G. (2021). A sequential mixed-methods approach to exploring the experiences of practitioners who have worked in multi-sensory environments with autistic children. *Research in Developmental Disabilities*, 118, 104061. DOI: 10.1016/j.ridd.2021.104061. PMID: not retrieved.
- Practitioners identified child control over sensory environment as a key mechanism for behavioural change
- Tier 2 (practitioner-experience evidence; Co-1 adjacent)

**Supporting source — Unwin, Powell, Price & Jones (2024):**
- Unwin, K.L., Powell, G., Price, A., & Jones, C.R.G. (2024). Patterns of equipment use for autistic children in multi-sensory environments: Time spent with sensory equipment varies by sensory profile and intellectual ability. *Autism*, 28, 644–655. DOI: 10.1177/13623613231180266. PMC not retrieved.
- Heterogeneity in equipment preferences confirms need for user control rather than fixed environmental specification
- Tier 3

**Italian replication:**
- Referenced in PMC11277603 (JCM 2024, 13(14):4162): consistent with Unwin et al. findings; significant reduction in sensory and seeking behaviours with targeted, personalised MSE use

**Architecture & Access / Amaze (2025):**
- Already identified in GAP-SRS-01: proximity to accessible sanitary facilities as key location requirement

### Specification Recommendation for A-16

Two changes:

1. **Elevate H-02 to PRIMARY cross-reference:**

> H-02 (Individual Environmental Control) is the PRIMARY design requirement for A-16 Sensory Room. Occupant-controlled dimming, sound management, and blackout capability are the primary design variables; static environmental parameters (STC, RT60, NC) are the necessary enabling context. ● [Tier 3; Unwin, Powell & Jones 2022, PMID: 34693744; replicated 2021 practitioner study and 2024 Italian study]

2. **Add location requirement:**

> A-16 location specification: adjacent to accessible WC facility; accessible without passing through high-stimulation area. ● [Tier 2; Architecture & Access / Amaze 2025]

### Evidence Tier
Tier 3 (Unwin et al. 2022 — controlled comparison) + Tier 2 (practitioner evidence) with replication

### Gap Status
**GAP-SRS-01: RESOLVED** — specification language drafted; evidence hierarchy established; ready for item-specification-writer.

---

## 4. GAP-034 — Circadian Lighting EML/MEDI Evidence

### Issue
B-01 specifies ≥150 EML daytime. This is ahead of all statutory standards globally. Evidence basis assessment requested: is the specification supported, and what is the current best-practice consensus value?

### Evidence Retrieved

**International consensus — Brown et al. (2022):**
- Brown, T.M., et al. (2022). Recommendations for daytime, evening, and nighttime indoor light exposure to best support physiology, sleep, and wakefulness in healthy adults. *PLOS Biology*, 20(3), e3001571. DOI: 10.1371/journal.pbio.3001571. PMC8929548.
- Product of Second International Workshop on Circadian and Neurophysiological Photometry (Manchester, 2019)
- **Consensus recommendations:**
  - Daytime: melanopic EDI ≥250 lux at the eye (vertical plane, 1.2m height)
  - Evening (≥3 hours before bedtime): melanopic EDI ≤10 lux
  - Sleep environment: melanopic EDI <1 lux
- melanopic EDI = 0.9058 × EML; therefore 250 melanopic EDI ≈ 276 EML
- **Key evidence:** Brown (2020) showed melanopsin is the best single opsin predictor of melatonin suppression, circadian phase resetting, and self-reported alerting responses across a wide range of conditions (1–1000 melanopic EDI lux)
- **Evidence tier:** Tier 3 (expert consensus based on systematic evidence review; published in PLOS Biology)

**Standards landscape:**

| Standard/Framework | Metric | Daytime value | Evening value | Status |
|---|---|---|---|---|
| WELL v2 (IWBI) | EML | ≥150 EML (electric only) or ≥200 EML (incl. daylight) | ≤50 EML nighttime | Voluntary — Tier 5 |
| WELL v6 (IWBI) | EML | ≥250 EML (breakrooms, living environments) | ≤50 EML nighttime | Voluntary — Tier 5 |
| DIN SPEC 67600:2013 → DIN/TS 67600:2022 (DE) | MEDI | ≥250 MEDI for ≥4 hours morning | — | Voluntary — Tier 5 |
| CIE S 026/E:2018 | melanopic EDI | Defined metric; no mandatory threshold | — | Metric definition — Tier 4 |
| ISO/CIE TR 21783 | — | References integrative lighting concept | — | Technical report — Tier 4 |
| Brown et al. (2022) consensus | melanopic EDI | ≥250 lux | ≤10 lux; <1 lux (sleep) | Expert consensus — Tier 3 |
| National building codes | — | No national code mandates circadian metric | — | — |

**Guidebook's current specification vs. evidence:**
- Guidebook B-01: ≥150 EML daytime = ~136 melanopic EDI
- Brown et al. consensus: ≥250 melanopic EDI ≈ ≥276 EML
- WELL v2 minimum: 150 EML (electric only); WELL v6: 250 EML (certain space types)
- DIN/TS 67600:2022: 250 MEDI (≈276 EML)

**Assessment:** The guidebook's ≥150 EML specification aligns with WELL v2 minimum for electric lighting but is **below** the 2022 international expert consensus (≥250 melanopic EDI ≈ 276 EML) and below DIN/TS 67600:2022. The guidebook is not ahead of all standards globally — it matches the WELL v2 baseline but falls short of the 2022 consensus and the German voluntary standard.

**Metric note:**
- EML (Lucas et al. 2014) and melanopic EDI (CIE S 026:2018) are closely related: EML = 1.104 × melanopic EDI
- CIE S 026 is the SI-compliant formalisation; EML is the earlier proposal
- Some debate exists about whether melanopic sensitivity function (MSF, peaking ~490 nm) fully captures circadian response — Brainard et al. (2001) found 464 nm most effective for melatonin suppression, which MSF underweights. However, Brown (2020) validated MSF as "sufficiently reliable" across real-world conditions.

**Disability-specific relevance:**
- DEM: circadian disruption is a major contributor to sundowning and agitation; adequate daytime circadian stimulus reduces behavioural symptoms (multiple DEM care studies)
- OFS/ME: circadian rhythm disruption is a documented feature; adequate daytime light exposure may support circadian entrainment (ME Association guidance)
- NDV/AUT: sensory sensitivity to bright light must be balanced against circadian needs — individual control (H-02/B-06) resolves this conflict
- Older adults: reduced crystalline lens transmittance means older eyes receive less melanopic light at the retina — Ticleanu et al. (2025) note this must be considered in recommendations

### Specification Recommendation for B-01

Upgrade B-01 specification:

> **B-01 Circadian Lighting:** Daytime maintained melanopic EDI ≥250 lux (≈276 EML) at the eye on the vertical plane at 1200mm AFF. Where electric lighting alone cannot achieve this, design for ≥150 EML (≈136 melanopic EDI) from electric lighting with daylight supplementation to meet the ≥250 melanopic EDI threshold. Evening (≥3 hours before habitual bedtime): melanopic EDI ≤10 lux (≈11 EML). Sleep environment: melanopic EDI <1 lux. ● [Tier 3; Brown et al. 2022, DOI: 10.1371/journal.pbio.3001571; CIE S 026/E:2018; DIN/TS 67600:2022; WELL v2/v6]

Add note on metric equivalence: melanopic EDI (CIE S 026) = 0.9058 × EML (Lucas et al. 2014). Guidebook adopts melanopic EDI as primary metric, with EML conversion noted.

Add population notes:
- DEM/NEU: circadian lighting is therapeutic, not merely amenity
- NDV/AUT/PCS: circadian benefit must be balanced with glare/photosensitivity via individual dimming control (B-06, H-02)
- Older adults: reduced retinal melanopic sensitivity requires specification to be met at the eye, not at a work surface

### Evidence Tier
Tier 3 (Brown et al. 2022 international consensus) + Tier 4 (CIE S 026; DIN/TS 67600) + Tier 5 (WELL v2/v6)

### Gap Status
**GAP-034: RESOLVED** — specification upgrade drafted; evidence confirms guidebook value was below current consensus; new value aligned with 2022 consensus.

---

## Citation Mining — Key Sources

### From GAP-STEP5-01 (B-10):
| Source | Direction | New sources |
|---|---|---|
| Jordan & Vanderheiden (2024) | Backward | Harding (1994); Binnie et al. (1980, 1984); Wilkins et al. (1979); ITU-R BT.1702:2023 |
| Jordan & Vanderheiden (2024) | Forward | Not yet searched — 2024 publication |

### From GAP-RAP-06 (DEAF RT60):
| Source | Direction | New sources |
|---|---|---|
| Iglehart (2020) | Backward | Finitzo-Hieber & Tillman (1978); Iglehart (2016); ASHA (2018) |
| Iglehart (2020) | Forward | Not yet searched |

### From GAP-SRS-01 (Sensory Room):
| Source | Direction | New sources |
|---|---|---|
| Unwin et al. (2022) | Backward | Unwin et al. (2021); Jones et al. (2020); Pellicano & Burr (2012); Boulter et al. (2014) |
| Unwin et al. (2022) | Forward | Unwin et al. (2024); Italian replication PMC11277603 (2024); Williams et al. (2024) scoping review |

### From GAP-034 (Circadian):
| Source | Direction | New sources |
|---|---|---|
| Brown et al. (2022) | Backward | Lucas et al. (2014); Brown (2020); CIE S 026/E:2018; Zeitzer et al. (2000); Brainard et al. (2001) |
| Brown et al. (2022) | Forward | Ticleanu et al. (2025) BRE; DIN/TS 67600:2022 |

---

## Summary — Actions Required

| Gap | Status | Next action | Skill |
|---|---|---|---|
| GAP-STEP5-01 | RESOLVED | Draft B-10 safety note; add NEU/NDV populations | item-specification-writer |
| GAP-RAP-06 | RESOLVED | Draft A-02/A-08 DEAF RT60 sub-target; update NR-EDU matrix | item-specification-writer |
| GAP-SRS-01 | RESOLVED | Elevate H-02 in A-16; add location spec | item-specification-writer |
| GAP-034 | RESOLVED | Upgrade B-01 from ≥150 EML to ≥250 melanopic EDI; add metric equivalence note | item-specification-writer |
