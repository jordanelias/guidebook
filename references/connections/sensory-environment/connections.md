# Connections — sensory-environment
<!-- CO-0006 Phase 0B-1 migration 2026-04-08 — from connection-register-active.md -->

### CON-0050

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** K-01, fold-down-grab-bar-specification
**Target population(s):** BAR, MOB, MOB/UPL
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Fold-down grab bar load specification (200 kg SWL minimum per fold-down-grab-bar-specification BPC) conflicts with bariatric requirement documented in body-sizes-supplementary-populations BPC (300 kg user weight, WC + user). Bariatric WC users require ≥300 kg rated fold-down bars; standard MOB specification is structurally insufficient. Not currently cross-referenced in guidebook.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| fold-down-grab-bar-specification BPC | 3 | MOB | BAR load requirement |
| body-sizes-supplementary-populations BPC | 3 | BAR | grab bar loading |

**Action required:** Specify bariatric-rated fold-down grab bars (≥300 kg SWL) where BAR provision required; flag standard 200 kg bars as inadequate for BAR populations. Cross-reference K-01 with BAR body-sizes profile.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0090

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** K-01, bathroom items
**Target population(s):** MOB, ALL
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Carnemolla, Mackinnon, Darcy & Almond (2025, Smart and Sustainable Built Environment) conducted embodied inquiry with 12 powered/manual wheelchair users on public bathroom design. Findings organised around safety, hygiene, planning/avoidance, and privacy/dignity themes. Co-1 evidence revealing gap between regulatory compliance and actual user experience — compliant bathrooms still fail wheelchair users. First study of its kind examining how wheelchair users actually use accessible bathrooms versus how standards assume they do.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Carnemolla et al. 2025 (SSBE) | Co-1 | MOB | bathroom item revision |

**Action required:** Add Carnemolla 2025 to bathroom BPC as Co-1 evidence. Key finding: regulatory compliance ≠ usability. Supports guidebook's beyond-code approach.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

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

---

### CON-0122

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** deaf-spatial-design, mobility-built-environment
**Target item(s):** A-02 (corridor width)
**Target population(s):** DEAF, MOB
**Evidence tier:** Co-1 (DeafSpace 2010) + Tier 3 (IDeA Center / Steinfeld 2010)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** DEAF corridor width (2440mm for signing conversation, DeafSpace 2010) subsumes MOB corridor width (1800mm turning, IDeA Center). In any building serving DEAF populations, the DEAF signing-width specification automatically satisfies the MOB turning-space requirement. This is a *subsumption connection* — the higher specification contains the lower. No conflict exists, but the cost and space implication is significant and undocumented: a designer who specifies for DEAF first (2440mm) does not need a separate MOB corridor width specification. Conversely, a designer who specifies for MOB only (1800mm) creates inadequate signing space for DEAF users.

The secondary implication: A-02 currently has 18 connection edges (highest in the network) but none documents the DEAF signing-width as the governing specification for mixed DEAF+MOB buildings. The corridor width is silently determined by whichever population has the larger requirement — this subsumption logic should be made explicit.

**Evidence basis:** deaf-spatial-design BPC: 2440mm (8 ft) primary corridors for signing. mobility-built-environment BPC: 1800mm turning for power wheelchair (IDeA Center; Habinteg/RCOTSS). 2440mm > 1800mm — DEAF governs.

**Action required:** Add subsumption note to A-02: "Where DEAF populations are primary users, corridor width is governed by signing-space requirement (2440mm), which automatically satisfies MOB turning requirement (1800mm). Where MOB only, 1800mm governs." This prevents redundant specification and makes the governing logic transparent.

**Disposition notes:** — First "subsumption connection" in the register. Consider systematising: for each item, identify which population specification governs (is widest/most restrictive).

---

---

### CON-0127

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** deaf-spatial-design, sensory-processing-model-design-application, dementia-built-environment
**Target item(s):** C-04 (wall colour), B-06 (lighting CCT)
**Target population(s):** DEAF, NDV, DEM
**Evidence tier:** Co-1 (DeafSpace 2010) + Tier 3 (Dunn model) + Tier 5 (DSDC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Three-way interaction on wall colour/finish:

- **DEAF:** Muted green/blue walls for sign language legibility — skin tone must contrast against background (DeafSpace 2010). Single, consistent colour per space.
- **NDV:** Reduced visual noise/complexity — minimal pattern, calm palette, low visual stimulation (PAS 6463, Dunn model). Supports muted single-colour approach.
- **DEM:** Colour-coded zones for spatial wayfinding — different colours per functional area (DEM BPC, DSDC). Requires colour VARIATION between zones.

DEAF and NDV are synergistic: both want muted, single-colour walls. DEM conflicts with both: DEM wants colour differentiation between zones, which increases the visual complexity that NDV aims to reduce and may place non-optimal colours (warm reds, yellows) in signing spaces where DEAF needs neutral tones.

Resolution: colour-zone wayfinding for DEM uses door colour and floor colour banding — NOT wall colour. Walls remain muted neutral (serving DEAF + NDV). Zone identity carried by floor and door (consistent with CON-0116 door-as-wayfinding-element). This preserves all three populations' requirements: DEAF signing legibility, NDV visual calm, DEM zone differentiation.

**Evidence basis:** deaf-spatial-design BPC: muted greens/blues, no busy patterns, skin tone contrast. sensory-processing-model BPC: visual noise reduction. dementia-built-environment BPC: colour-coded wayfinding. No source addresses the three-way interaction.

**Action required:** (1) Part 5 conflict note: DEAF/NDV/DEM wall colour three-way interaction. Resolution: walls muted neutral; zone coding via floor and door colour only. (2) C-04 specification: separate wall colour (muted neutral for DEAF/NDV) from zone-coding colour (floor/door for DEM). (3) This resolution is ○ (expert synthesis) — no study validates the floor/door-only colour coding approach.

**Disposition notes:** — First three-way conflict identified by this scan. Resolution is architecturally elegant (preserves all three requirements) but unvalidated.

---

---

### CON-0131

**Status:** CONSUMED
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

**Connection:** CON-0039 proposes RT60 ≤0.3 s as Universal Mode universal for speech-critical rooms, based on DEAF evidence (Iglehart 2020). The room-acoustic-performance BPC documents that NDV/AUT evidence (Bettarello 2021, Caniato 2024) indicates existing standards (calibrated to neurotypical populations) are insufficient and that autistic users are "significantly more affected by modest background noise increases (52→55 dBA)." The BPC suggests sub-0.3s RT60 may be needed for NDV/AUT but no quantified target exists.

This creates a population-within-specification hierarchy for acoustic items:
- General population: 0.6 s (code compliance, Tier 6)
- DEAF/hearing devices: 0.3 s (Universal Mode per CON-0039)
- NDV/AUT primary spaces: <0.3 s (Tier 1 — specific value unquantified; ○ marker)

The practical implication: in NDV-primary spaces (autism schools, sensory rooms, A-16), the DEAF Universal Mode of 0.3 s is a floor, not a ceiling. Additional acoustic treatment beyond what satisfies DEAF requirements may be needed. Background noise threshold for NDV/AUT is also more stringent: the 3 dBA increase (52→55) that is perceptually negligible for neurotypical and minimally impactful for DEAF is functionally significant for NDV/AUT.

**Evidence basis:** room-acoustic-performance BPC: Bettarello 2021 (Tier 1), Caniato 2024 (Tier 1) — autistic populations significantly more affected by modest noise increases. NDV BPC Opus synthesis: "no internationally agreed quantified RT60 target specific to autistic users."

**Action required:** Add NDV/AUT acoustic annotation to A-01/A-02: "In NDV/AUT-primary spaces, RT60 ≤0.3 s (Universal Mode) is a floor. Additional acoustic treatment to achieve lowest practicable RT60 and background noise level is recommended (○ — no quantified NDV/AUT-specific target; gap flagged for v11 research)." Cross-reference CON-0039.

**Disposition notes:** — MODERATE because no quantified NDV/AUT-specific target exists. The direction is clear; the value is not.

---

### CON-0141

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** deaf-spatial-design, sensory-relief-space-design
**Target item(s):** A-16, Part 7 NR-EDU
**Target population(s):** DEAF, NDV/AUT
**Evidence tier:** Co-1 (DeafSpace) + Tier 3 (sensory-relief BPC)

**Connection:** A-16 specifies acoustic isolation (STC ≥50, RT60 ≤0.3s, NC ≤25). This creates a communication isolation hazard for DEAF users — a sound-isolated room without visual alerting or transparent sightlines prevents a DEAF user inside from receiving emergency alerts or communicating with people outside. Project-standards already flags this for D-05 (CON-0036: "sound attenuation creates emergency egress and communication isolation risk for DEAF"). The same logic applies to A-16 but is undocumented.

Resolution per CON-0036 precedent: visual emergency alerts inside A-16; transparent sidelight or vision panel at door; vibrotactile alerting device (K-04) connected to building fire alarm. A-16 acoustic isolation serves NDV/AUT; DEAF communication access prevents isolation becoming entrapment.

**Action required:** Apply CON-0036 pattern to A-16: visual emergency alert + vision panel + K-04 vibrotactile. Prevents A-16 from being a communication-isolation hazard for DEAF/DBL users.

---

---

### CON-0144

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** sensory-relief-space-design, neurodivergent-built-environment
**Target item(s):** A-16
**Target population(s):** NDV/AUT
**Evidence tier:** Tier 3 (Rashid/Al-Harasis 2025)

**Connection:** The sensory-relief BPC notes: "Rashid et al. (2025) taxonomy identifies that most frameworks overemphasise interior elements relative to spatial configuration (adjacency, sequencing, approach). This is a gap in A-16's current specification scope." CON-0023 (CONSUMED) independently flags the same finding from Al-Harasis 2025: "current autism design frameworks rely on intuition sensory zoning as the main driver for spatial topology without quantifying the sensory drivers."

Two independent sources in two connection entries identify the same gap: A-16 specifies finishes and fixtures (lighting, acoustic treatment, materials) but NOT spatial configuration (where A-16 sits relative to other spaces, what the approach sequence is, what adjacencies are required). The sensory-relief BPC already identifies "proximity to sanitary facilities" as a NEW requirement from Amaze/Architecture & Access 2025.

**Action required:** A-16 spatial configuration specification: (a) adjacent to primary circulation without passing through high-stimulation zones; (b) proximity to accessible toilet (≤15m); (c) approach via transition/decompression zone (≥3m, per PAS 6463); (d) not adjacent to high-noise sources (kitchens, plant rooms, playgrounds); (e) not at dead-end of corridor (DBL/DEM egress). These are spatial-configuration requirements distinct from the interior specification.

---

---

### CON-0145

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** true
**Source BPC slug(s):** acoustics-speech-intelligibility-disability, deaf-acoustic-built-environment
**Target item(s):** A-10, H-04
**Target population(s):** DEAF, NDV, VIS
**Evidence tier:** Tier 4 (IEC 60118-4)

**Connection:** Hearing loop field uniformity (±3 dB per IEC 60118-4) requires specific spatial conditions: metal structures, underfloor heating, and electrical wiring interfere with magnetic field. H-04 (digital infrastructure) specifies conduit routing but does not cross-reference hearing loop installation constraints. When H-04 conduit and A-10 hearing loop are designed independently, the conduit routing may degrade loop performance.

Additionally: underfloor heating (specified as OFS/PAIN thermal provision via F-07 heated bathroom floor) creates magnetic field interference with hearing loops in the same space. A heated bathroom floor and a hearing loop cannot coexist without a phased-array or cancellation loop design — an engineering coordination requirement not documented.

**Action required:** Part 8 (Engineering): heating system type and electrical conduit routing must be coordinated with hearing loop design. Underfloor heating in looped spaces requires phased-array loop or cancellation coil. Cross-reference F-07 ↔ A-10 ↔ H-04.

---

---

### CON-0146

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** visual-impairment-built-environment, deaf-spatial-design, deafblind-built-environment-design
**Target item(s):** B-06, B-07 (lighting)
**Target population(s):** DEAF, VIS, DBL
**Evidence tier:** Co-1 (DeafSpace) + Tier 4-6 (VIS BPC)

**Connection:** DEAF BPC: ≥300 lux diffuse, matte-reflected, shadow-free lighting in communication zones; backlighting eliminated; lighting serves sign language visibility. VIS BPC: ≥300 lux in circulation without glare; no sudden illuminance transitions >5:1. These targets are identical in value (≥300 lux) and complementary in character (both require diffuse, glare-free light). But the rationale is different: DEAF needs light on the signer's face and hands; VIS needs light on environmental surfaces for legibility.

The practical implication: lighting placement differs. DEAF requires frontal/lateral light on the person (face illumination for lip-reading and signing). VIS requires light on the environment (surface illumination for contrast detection). A single luminaire position cannot optimise for both simultaneously. The specification should distinguish: ambient/surface lighting (VIS) and communication-zone lighting (DEAF) as two coordinated layers.

DBL needs BOTH: high ambient for residual vision + shadow-free for tactile reading of faces/hands.

**Action required:** B-06/B-07: specify two lighting layers in shared DEAF+VIS spaces — (a) ambient surface illumination ≥300 lux for VIS legibility; (b) communication-zone face/hand illumination for DEAF signing, positioned to eliminate backlighting on signers. Both diffuse, both glare-free, but different placement geometry.

---

---

### CON-0015

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** F-04, F-02
**Target population(s):** NDV, OFS, PAIN, MH
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Air quality / fragrance-free specifications carry OFS, NDV, NEU, PAIN. MH absent despite TID framework emphasis on environmental predictability and trigger avoidance. Chemical stimuli can trigger PTSD hyperarousal.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Steinemann 2018 | 3 | General | MH |
| TID framework | 2–3 | MH | MH (chemical triggers) |

**Action required:** Add MH as co-population for F-02/F-04.

**Disposition notes:** - [ ] MODERATE → P2 gap item

---

---

---

## Connections CON-0131+ (Write-back from Opus batches 3-4 + 5-8 corrected, 2026-04-09)

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

**Connection:** CON-0039 proposes RT60 ≤0.3 s as Universal Mode universal for speech-critical rooms, based on DEAF evidence (Iglehart 2020). The room-acoustic-performance BPC documents that NDV/AUT evidence (Bettarello 2021, Caniato 2024) indicates existing standards (calibrated to neurotypical populations) are insufficient and that autistic users are "significantly more affected by modest background noise increases (52→55 dBA)." The BPC suggests sub-0.3s RT60 may be needed for NDV/AUT but no quantified target exists.

This creates a population-within-specification hierarchy for acoustic items:
- General population: 0.6 s (code compliance, Tier 6)
- DEAF/hearing devices: 0.3 s (Universal Mode per CON-0039)
- NDV/AUT primary spaces: <0.3 s (Tier 1 — specific value unquantified; ○ marker)

The practical implication: in NDV-primary spaces (autism schools, sensory rooms, A-16), the DEAF Universal Mode of 0.3 s is a floor, not a ceiling. Additional acoustic treatment beyond what satisfies DEAF requirements may be needed. Background noise threshold for NDV/AUT is also more stringent: the 3 dBA increase (52→55) that is perceptually negligible for neurotypical and minimally impactful for DEAF is functionally significant for NDV/AUT.

**Evidence basis:** room-acoustic-performance BPC: Bettarello 2021 (Tier 1), Caniato 2024 (Tier 1) — autistic populations significantly more affected by modest noise increases. NDV BPC Opus synthesis: "no internationally agreed quantified RT60 target specific to autistic users."

**Action required:** Add NDV/AUT acoustic annotation to A-01/A-02: "In NDV/AUT-primary spaces, RT60 ≤0.3 s (Universal Mode) is a floor. Additional acoustic treatment to achieve lowest practicable RT60 and background noise level is recommended (○ — no quantified NDV/AUT-specific target; gap flagged for v11 research)." Cross-reference CON-0039.

**Disposition notes:** — MODERATE because no quantified NDV/AUT-specific target exists. The direction is clear; the value is not.

### CON-0141

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** deaf-spatial-design, sensory-relief-space-design
**Target item(s):** A-16, Part 7 NR-EDU
**Target population(s):** DEAF, NDV/AUT
**Evidence tier:** Co-1 (DeafSpace) + Tier 3 (sensory-relief BPC)

**Connection:** A-16 specifies acoustic isolation (STC ≥50, RT60 ≤0.3s, NC ≤25). This creates a communication isolation hazard for DEAF users — a sound-isolated room without visual alerting or transparent sightlines prevents a DEAF user inside from receiving emergency alerts or communicating with people outside. Project-standards already flags this for D-05 (CON-0036: "sound attenuation creates emergency egress and communication isolation risk for DEAF"). The same logic applies to A-16 but is undocumented.

Resolution per CON-0036 precedent: visual emergency alerts inside A-16; transparent sidelight or vision panel at door; vibrotactile alerting device (K-04) connected to building fire alarm. A-16 acoustic isolation serves NDV/AUT; DEAF communication access prevents isolation becoming entrapment.

**Action required:** Apply CON-0036 pattern to A-16: visual emergency alert + vision panel + K-04 vibrotactile. Prevents A-16 from being a communication-isolation hazard for DEAF/DBL users.

### CON-0144

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** sensory-relief-space-design, neurodivergent-built-environment
**Target item(s):** A-16
**Target population(s):** NDV/AUT
**Evidence tier:** Tier 3 (Rashid/Al-Harasis 2025)

**Connection:** The sensory-relief BPC notes: "Rashid et al. (2025) taxonomy identifies that most frameworks overemphasise interior elements relative to spatial configuration (adjacency, sequencing, approach). This is a gap in A-16's current specification scope." CON-0023 (CONSUMED) independently flags the same finding from Al-Harasis 2025: "current autism design frameworks rely on intuition sensory zoning as the main driver for spatial topology without quantifying the sensory drivers."

Two independent sources in two connection entries identify the same gap: A-16 specifies finishes and fixtures (lighting, acoustic treatment, materials) but NOT spatial configuration (where A-16 sits relative to other spaces, what the approach sequence is, what adjacencies are required). The sensory-relief BPC already identifies "proximity to sanitary facilities" as a NEW requirement from Amaze/Architecture & Access 2025.

**Action required:** A-16 spatial configuration specification: (a) adjacent to primary circulation without passing through high-stimulation zones; (b) proximity to accessible toilet (≤15m); (c) approach via transition/decompression zone (≥3m, per PAS 6463); (d) not adjacent to high-noise sources (kitchens, plant rooms, playgrounds); (e) not at dead-end of corridor (DBL/DEM egress). These are spatial-configuration requirements distinct from the interior specification.

### CON-0145

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** true
**Source BPC slug(s):** acoustics-speech-intelligibility-disability, deaf-acoustic-built-environment
**Target item(s):** A-10, H-04
**Target population(s):** DEAF, NDV, VIS
**Evidence tier:** Tier 4 (IEC 60118-4)

**Connection:** Hearing loop field uniformity (±3 dB per IEC 60118-4) requires specific spatial conditions: metal structures, underfloor heating, and electrical wiring interfere with magnetic field. H-04 (digital infrastructure) specifies conduit routing but does not cross-reference hearing loop installation constraints. When H-04 conduit and A-10 hearing loop are designed independently, the conduit routing may degrade loop performance.

Additionally: underfloor heating (specified as OFS/PAIN thermal provision via F-07 heated bathroom floor) creates magnetic field interference with hearing loops in the same space. A heated bathroom floor and a hearing loop cannot coexist without a phased-array or cancellation loop design — an engineering coordination requirement not documented.

**Action required:** Part 8 (Engineering): heating system type and electrical conduit routing must be coordinated with hearing loop design. Underfloor heating in looped spaces requires phased-array loop or cancellation coil. Cross-reference F-07 ↔ A-10 ↔ H-04.

### CON-0146

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** visual-impairment-built-environment, deaf-spatial-design, deafblind-built-environment-design
**Target item(s):** B-06, B-07 (lighting)
**Target population(s):** DEAF, VIS, DBL
**Evidence tier:** Co-1 (DeafSpace) + Tier 4-6 (VIS BPC)

**Connection:** DEAF BPC: ≥300 lux diffuse, matte-reflected, shadow-free lighting in communication zones; backlighting eliminated; lighting serves sign language visibility. VIS BPC: ≥300 lux in circulation without glare; no sudden illuminance transitions >5:1. These targets are identical in value (≥300 lux) and complementary in character (both require diffuse, glare-free light). But the rationale is different: DEAF needs light on the signer's face and hands; VIS needs light on environmental surfaces for legibility.

The practical implication: lighting placement differs. DEAF requires frontal/lateral light on the person (face illumination for lip-reading and signing). VIS requires light on the environment (surface illumination for contrast detection). A single luminaire position cannot optimise for both simultaneously. The specification should distinguish: ambient/surface lighting (VIS) and communication-zone lighting (DEAF) as two coordinated layers.

DBL needs BOTH: high ambient for residual vision + shadow-free for tactile reading of faces/hands.

**Action required:** B-06/B-07: specify two lighting layers in shared DEAF+VIS spaces — (a) ambient surface illumination ≥300 lux for VIS legibility; (b) communication-zone face/hand illumination for DEAF signing, positioned to eliminate backlighting on signers. Both diffuse, both glare-free, but different placement geometry.

### CON-0164
*[formerly CON-0153]*

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** visual-fire-alarm-seizure-safety, deaf-acoustic-built-environment, sensory-relief-space-design
**Target item(s):** B-10, A-16, K-04
**Target population(s):** DEAF, NEU (photosensitive epilepsy), NDV/AUT
**Evidence tier:** Tier 3–4 (Jordan & Vanderheiden 2024, BS EN 54-23)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** A-16 requires acoustic isolation (NDV/AUT) → DEAF needs visual alerting inside (CON-0141) → NEU photosensitive users need flash protection. Three-way interaction. Resolution: K-04 vibrotactile wearable as primary (serves DEAF/DBL without visual/acoustic trigger); VAD at 0.5 Hz synchronised; voice alarm emergency-only with visual pre-alert; no unsynchronised strobes.

**Evidence basis:** Jordan & Vanderheiden 2024 (0.5–1 Hz safe below 3 Hz seizure threshold). BS EN 54-23 (synchronisation). CON-0141 (DEAF isolation in sound-attenuated spaces).

**Action required:** A-16 emergency notification: (1) K-04 vibrotactile connected to fire alarm; (2) VAD at 0.5 Hz synchronised; (3) voice alarm emergency-only with 5-second visual pre-alert; (4) no unsynchronised strobes.

**Quality assessment:** Strong. Safety-critical. Novel multi-population specification.

### CON-0166
*[formerly CON-0155]*

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** therapeutic-lighting-design, circadian-lighting-melanopic-edi, sensory-processing-model-design-application
**Target item(s):** B-01, B-06, B-07, A-16
**Target population(s):** DEM, NDV/AUT, NEU
**Evidence tier:** Tier 1 (circadian RCTs) + Tier 3 (Dunn model)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Circadian lighting requires ≥250 melanopic EDI daytime. A-16 needs calming function — low melanopic EDI (≤10, ≤2700K CCT). If A-16 is on the building's circadian programme, mid-morning users receive ≥250 melanopic EDI contradicting the room's calming function. A-16 must be independent from the circadian system.

**Action required:** A-16 lighting: independent from building circadian system. Max melanopic EDI ≤10 (occupant may increase). CCT ≤2700K default. Dimmer to 1%. No automatic circadian programme in A-16. Cross-reference B-01 with exclusion note.

**Quality assessment:** Strong system-interaction finding. Clear, actionable.

### CON-0148

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Target item(s):** A-16
**Target population(s):** NDV/MH, NDV/AUT

**Connection:** MH de-escalation room specification — separation from NDV quiet room [DESCRIPTION PENDING — source session file required]

### CON-0149

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Target item(s):** G-XX (proposed)
**Target population(s):** NDV/MH, NDV/AUT

**Connection:** Proposed new item — sensory room furniture specification [DESCRIPTION PENDING]

### CON-0150

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Target item(s):** A-16 door spec
**Target population(s):** NDV/MH, NDV/AUT

**Connection:** A-16 door specification detail [DESCRIPTION PENDING]


### CON-0182

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** circadian-lighting-melanopic-edi, neurodivergent-built-environment, fatigue-spectrum-built-environment
**Target item(s):** K-03 (circadian lighting)
**Target population(s):** DEM, MH, NDV/AUT, OFS
**Evidence tier:** 3–4
**Filed:** 2026-04-24
**Applied:** —

**Connection type:** COMPOUND-INTERACTION
**Connection:** Circadian lighting specification (melanopic EDI ≥250 lux daytime) serves DEM and MH circadian entrainment needs but compounds with NDV/AUT photosensitivity and OFS/ME light-triggered symptom exacerbation. This is not a simple divergence — it is a compound interaction where the dose that treats circadian disruption in one population actively harms sensory processing in another. Resolution requires spatial zoning: circadian-optimised communal areas with opt-out low-lux zones accessible within 25m.

**Evidence basis:** CIE S 026/E:2018 (melanopic EDI); PAS 6463:2022 §NDV lighting; van Hoof 2010 (DEM thermoregulation, confirmed T3-027); BPC circadian-lighting divergent finding NDV/AUT.

**Action required:** Add compound-interaction note to circadian lighting spec. Cross-reference sensory-relief-space A-16 as the mandatory opt-out mechanism.

**Disposition notes:** —


### CON-0183

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** room-acoustic-performance, deaf-acoustic-built-environment, neurodivergent-built-environment, mental-health-built-environment
**Target item(s):** K-01 (RT60), K-02 (background noise)
**Target population(s):** DEAF, NDV, MH
**Evidence tier:** 3–5
**Filed:** 2026-04-24
**Applied:** —

**Connection type:** CROSS-POPULATION
**Connection:** RT60 ≤0.3 s specification converges across three independent evidence bases via different clinical mechanisms: DEAF (speech intelligibility with hearing devices), NDV/AUT (reduced reverberation decreases auditory processing load, PAS 6463), MH (noise reduction in trauma-informed environments, Owen & Crane 2022). The convergence is strong because all three arrive at the same numerical threshold independently — this is a genuine cross-population specification that should be tagged for all three populations rather than siloed in DEAF.

**Evidence basis:** BB93:2015; PAS 6463:2022 §10; Oostermeijer et al. 2021 (PMID:34233981); Weber et al. 2022 (PMID:35046849); van der Schaaf et al. 2013 (DOI:10.1192/bjp.bp.112.118422). All verified.

**Action required:** Add NDV and MH population tags to RT60 ≤0.3s specification. Reference PAS 6463 and MH evidence alongside DEAF sources.

**Disposition notes:** —


### CON-0186

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** sensory-relief-space-design, mental-health-built-environment, dementia-built-environment, fatigue-spectrum-built-environment
**Target item(s):** A-16 (sensory quiet room)
**Target population(s):** NDV, MH, DEM, OFS
**Evidence tier:** Co-1, 3
**Filed:** 2026-04-24
**Applied:** —

**Connection type:** CROSS-POPULATION
**Connection:** Four independent evidence bases converge on an identical room-type specification — a quiet, low-stimulation, user-controlled space within 25m of primary occupancy: NDV/AUT (sensory quiet room, PAS 6463 A-16), MH (de-escalation space in psychiatric facilities, Oostermeijer 2021 PMID:34233981, Weber 2022 PMID:35046849), DEM (calm/retreat zone in dementia environments, DSDC EADDAT), OFS/ME (rest space during post-exertional malaise episodes). Each arrives via different clinical mechanisms but the specification is identical. This is the strongest cross-population convergence in the evidence base.

**Evidence basis:** PAS 6463:2022; Oostermeijer et al. 2021; Weber et al. 2022; DSDC EADDAT 2022; Unwin et al. 2021 (T3-085); BPC sensory-relief-space consensus findings.

**Action required:** Elevate A-16 to cross-population universal provision. Tag all four populations explicitly. This room type resolves gaps across NDV, MH, DEM, and OFS simultaneously.

**Disposition notes:** —

---

## CON-0196

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** pain-ofs-built-environment-design, sensory-relief-space-design, dementia-built-environment, neurodivergent-built-environment, neurological-built-environment, mobility-built-environment
**Target item(s):** B-12, D-05
**Target population(s):** DEM, MOB, NEU, OFS, PAIN
**Evidence tier:** 2-3
**Filed:** 2026-05-04
**Applied:** —

**Connection type:** CROSS-POPULATION
**Connection:** Overnight bed-to-bathroom path lighting (motion-sensor, 300-400mm AFF, ≥5 lux, 2700-3000K) serves 5+ populations: DEM (nocturnal wayfinding), MOB (fall prevention — Keall 2015 Cochrane), NEU (spatial orientation post-ABI), OFS (orthostatic fall risk), PAIN (night navigation with limited mobility). Universal Mode candidate — no conflict identified.

**Evidence basis:** Dementia Australia 2022 (Tier 2); Keall et al. 2015 Cochrane (Tier 1); bathroom BPC FDR scenario 14.

**Action required:** B-12: elevate to Universal Mode with multi-population evidence. Tag DEM, MOB, NEU, OFS, PAIN.

**Disposition notes:** —

---

## CON-0211

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** acoustics-speech-intelligibility-disability, deaf-acoustic-built-environment, neurodivergent-built-environment, dementia-built-environment
**Target item(s):** Part 8 Engineering
**Target population(s):** DEAF, NDV, DEM
**Evidence tier:** 3
**Filed:** 2026-05-04
**Applied:** —

**Connection type:** CROSS-ITEM
**Connection:** Building acoustic multi-zone system: speech-critical RT60 ≤0.3s NC-25, circulation RT60 ≤0.6s NC-35, A-16 RT60 ≤0.3s NC-25, hearing loop RT60 ≤0.4s NC-25, DEM common RT60 ≤0.4s NC-30, NDV-primary RT60 <0.3s NC-25. Partition STC between adjacent zones must be calibrated to acoustic delta. A-14 single STC ≥50 is insufficient — required STC varies by adjacency.

**Evidence basis:** Acoustics BPC; DEAF acoustic BPC; NDV BPC; DEM BPC.

**Action required:** Part 8: acoustic zoning coordination matrix. A-14: reference matrix.

**Disposition notes:** —

---

## CON-0214

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** sensory-relief-space-design, neurodivergent-built-environment
**Target item(s):** B-12, B-01
**Target population(s):** NDV, DEM, OFS
**Evidence tier:** 3
**Filed:** 2026-05-04
**Applied:** —

**Connection type:** CROSS-ITEM
**Connection:** B-12 sensor lighting must be isolated from B-01 circadian programme. Night-time sensor trigger could activate ≥250 melanopic EDI, fully waking circadian system during sleepy toileting. NDV photosensitivity: sudden activation may startle. Specification: B-12 at ≤10 lux, ≤2700K, independent circuit. Extends CON-0166 principle to bedroom sensor lighting.

**Evidence basis:** CON-0166; B-01/B-12 specifications; NDV BPC photosensitivity; journey sequencing.

**Action required:** B-12: independence from B-01. Max ≤10 lux ≤2700K nocturnal. Part 8: separate circuit.

**Disposition notes:** —

---

## CON-0217

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** visual-impairment-built-environment, deaf-acoustic-built-environment, neurodivergent-built-environment, dementia-built-environment, neurological-built-environment
**Target item(s):** B-10, A-16, K-04
**Target population(s):** NDV, NEU/epilepsy, DEM, DEAF, DBL
**Evidence tier:** 3
**Filed:** 2026-05-04
**Applied:** —

**Connection type:** CROSS-POPULATION
**Connection:** Simultaneous multi-modal alarm is itself an accessibility barrier: NDV strobe+siren → sensory overload → freeze; NEU/epilepsy unsynchronized strobe → seizure; DEM alarm without comprehension → undirected panic. Extends CON-0164 into temporal SEQUENCE: T+0s vibrotactile, T+3s steady amber pre-alert, T+5s VAD 0.5Hz + voice instruction, staff-mediated DEM evacuation concurrent.

**Evidence basis:** CON-0164; NDV BPC; NEU BPC epilepsy; DEM BPC alarm comprehension; journey sequencing.

**Action required:** B-10: sequenced multi-modal alarm replacing simultaneous. K-04: temporal sequence. Part 9: staff-mediated DEM evacuation.

**Disposition notes:** —

---

## CON-0220

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** sensory-relief-space-design, neurodivergent-built-environment
**Target item(s):** A-16, F-01, F-03
**Target population(s):** NDV, MH
**Evidence tier:** 3
**Filed:** 2026-05-04
**Applied:** —

**Connection type:** CROSS-ITEM
**Connection:** CON-0144 specifies A-16 exit decompression ≥3m. No specification addresses APPROACH. Person in sensory overload navigates through stimulating building to reach A-16. Last 10m of approach should have: reduced lighting ≤200 lux, no through-traffic routing, acoustic treatment RT60 ≤0.4s. Creates bidirectional decompression: calming on approach, graduated on exit.

**Evidence basis:** CON-0144; F-01; F-03; NDV BPC; room synthesis.

**Action required:** A-16: add approach decompression (10m). F-01: reference as gradient terminus. F-03: link bidirectional.

**Disposition notes:** —
