# Connection Application Queue — ISW Briefings
**Generated:** 2026-04-24 07:28
**Source:** connection-scout Opus run Block 18
**Connections:** CON-0181 through CON-0186, CON-0188 (7 HIGH confidence)
**CON-0187 excluded:** MODERATE confidence — deferred to gap register P3

---

## ISW-BRIEF-01: CON-0181 — Floor Vibration Population Extension

**Target spec:** A-09 (floor surface specification)
**Current state:** A-09 specifies surface characteristics for wheelchair users (MOB). WBV evidence is siloed in floor-vibration BPC slug.
**Change required:**
1. Add population tags: PAIN, NEU, OFS to A-09 floor surface spec
2. Add specification note: "Floor surfaces in primary circulation zones shall minimise whole-body vibration transmission. Surfaces exceeding 0.5 m/s² RMS vertical acceleration (ISO 2631-1 EAV threshold) are contraindicated for chronic pain (spinal disorder risk amplification), neurological tremor (tremor amplification), and fatigue-spectrum populations (vibration-induced fatigue compounds reduced activity tolerance)."
3. Add cross-reference to floor-vibration BPC slug from chronic-pain and fatigue-spectrum slugs
**Evidence:** Garcia-Mendez 2013 PMID:23820152; Koontz 2012 DOI:10.1123/jab.28.4.412; Chénier 2014 PMID:25276802
**Opus note:** The 0.5 m/s² threshold derives from ISO 2631-1 EAV. Garcia-Mendez found wheelchair users routinely exceed this on common surfaces (0.83 ± 0.17 m/s²). The clinical implications for PAIN/NEU/OFS are inferred from the shared physiological mechanism (spinal loading, neuromuscular fatigue) — not directly tested in those populations. Mark ○ (inferred) not ● (evidence-based).

---

## ISW-BRIEF-02: CON-0182 — Circadian Lighting Compound Interaction

**Target spec:** K-03 (circadian lighting)
**Current state:** K-03 specifies melanopic EDI ≥250 lux daytime. Divergent finding exists for NDV/AUT photosensitivity.
**Change required:**
1. Add compound-interaction annotation to K-03
2. Add specification clause: "In buildings serving NDV/AUT or OFS/ME populations alongside DEM or MH populations, circadian-optimised lighting (≥250 lux melanopic EDI) shall be applied to communal spaces with a mandatory opt-out zone (A-16 sensory quiet room or equivalent) maintained at ≤50 lux within 25m of any primary occupancy space."
3. Cross-reference A-16 as the resolution mechanism
**Evidence:** CIE S 026/E:2018; PAS 6463:2022; van Hoof 2010 DOI:10.1016/j.buildenv.2009.06.017
**Opus note:** This is a genuine compound interaction, not a simple divergence. The dose-response curves are opposed: DEM/MH benefit from high melanopic lux; NDV/OFS are harmed by it. Spatial zoning is the only resolution — compromise (e.g., 150 lux) serves neither population adequately. The A-16 quiet room provides the opt-out mechanism.

---

## ISW-BRIEF-03: CON-0183 — RT60 ≤0.3s Cross-Population Tagging

**Target spec:** K-01 (reverberation time)
**Current state:** K-01 specifies RT60 ≤0.3s for DEAF/hearing device users in spaces ≤283 m³. NDV and MH reach the same threshold independently.
**Change required:**
1. Add population tags: NDV, MH to the ≤0.3s tier of K-01
2. Revise specification note: "RT60 ≤0.3 s applies to all spaces designated for DEAF, NDV, or MH populations (volumes ≤283 m³). Evidence converges from three independent clinical mechanisms: speech intelligibility with hearing devices (DEAF), reduced auditory processing load (NDV/AUT per PAS 6463), and noise reduction in trauma-informed environments (MH per Owen & Crane 2022)."
3. Update room-acoustic BPC slug to cite NDV and MH sources alongside DEAF
**Evidence:** BB93:2015; PAS 6463:2022 §10; Oostermeijer 2021 PMID:34233981; Weber 2022 PMID:35046849; van der Schaaf 2013 DOI:10.1192/bjp.bp.112.118422
**Opus note:** The numerical convergence on ≤0.3s from three independent evidence bases is unusually strong. All three are ● (evidence-based). This should be presented as a convergent specification, not three separate requirements.

---

## ISW-BRIEF-04: CON-0184 — PMV/PPD Contraindication

**Target spec:** K-05 (thermal comfort assessment method)
**Current state:** K-05 may reference ISO 7730 PMV/PPD as default assessment.
**Change required:**
1. Add contraindication note: "PMV/PPD thermal comfort assessment (ISO 7730) is contraindicated for DEM (inability to self-report thermal discomfort or operate environmental controls), NEU/MS (thermoregulation impairment invalidates metabolic rate assumptions), and OFS (orthostatic intolerance modulated by ambient temperature). For these populations, specify objective physiological monitoring (skin temperature sensors, behavioural observation protocols) or proxy-reported assessment."
2. Add population tags: DEM, NEU, OFS to K-05
3. Cross-reference thermoregulation BPC slug Cluster 1
**Evidence:** Van Hoof et al. 2010 DOI:10.1016/j.buildenv.2009.06.017 (confirmed T3-027)
**Opus note:** Van Hoof 2010 is the primary source demonstrating PMV/PPD failure for cognitively impaired populations. The extension to NEU and OFS is inferred from the shared mechanism (inability to thermoregulate normally or self-report accurately). Mark DEM as ● and NEU/OFS as ○.

---

## ISW-BRIEF-05: CON-0185 — Grab Bar Biomechanics Extension

**Target spec:** G-03, G-04 (grab bar height and configuration)
**Current state:** Grab bar specs reference MOB wheelchair and ambulant transfer biomechanics. Lee 2017/18 bilateral fold-down at 813mm is the strongest evidence for toilet transfer.
**Change required:**
1. Add population tags: PAIN, OFS to G-03 (grab bar height) and G-04 (grab bar configuration)
2. Add specification note: "Bilateral grab bar configuration (G-04) also serves pain-modified transfers (PAIN: weight-bearing avoidance on affected side changes handedness requirement — bilateral provision eliminates directionality constraint) and fatigue populations (OFS: grab bars within easy reach without stretching minimises energy expenditure per transfer). Reference FDR-CMP-01."
3. Cross-reference FDR-CMP-01 compound scenario
**Evidence:** Lee et al. 2018 PMID:28952364; Sekiguchi et al. 2017 PMID:28528238; Guitard et al. 2011 PMID:22256669; Lee et al. 2019 PMID:29522366
**Opus note:** The bilateral configuration is the key insight. Unilateral grab bars force a transfer direction. Pain-modified transfers and fatigue-limited transfers both benefit from directional flexibility. The 813mm height serves MOB, PAIN, and OFS simultaneously — no dimensional conflict.

---

## ISW-BRIEF-06: CON-0186 — A-16 Sensory Relief Space Elevation

**Target spec:** A-16 (sensory quiet room)
**Current state:** A-16 is specified for NDV populations (PAS 6463). Located in sensory-environment domain.
**Change required:**
1. Elevate A-16 to cross-population universal provision with explicit tags: NDV, MH, DEM, OFS
2. Revise specification: "Every occupied building shall provide at least one sensory-relief space per floor plate, accessible within 25m of any primary occupancy space. Specification: user-controlled lighting (2700–5000 K, 10–500 lux dimmable), acoustic attenuation ≤30 dBA, no fluorescent or stroboscopic lighting. This room type serves four independent clinical functions: sensory overload recovery (NDV/AUT), de-escalation and safety (MH), calm retreat and wandering management (DEM), and post-exertional malaise rest (OFS/ME)."
3. Add A-16 cross-references to mental-health, dementia, and fatigue-spectrum BPC slugs
4. Update sensory-relief-space BPC consensus findings to cite all four population evidence bases
**Evidence:** PAS 6463:2022; Oostermeijer 2021 PMID:34233981; Weber 2022 PMID:35046849; DSDC EADDAT 2022; Unwin et al. 2021 (T3-085)
**Opus note:** This is the single strongest cross-population connection in the evidence base. The convergence is remarkable because all four populations arrive at the same physical specification via entirely different clinical mechanisms. This should be presented prominently in Part 3 as a paradigm example of universal design emerging from population-specific evidence.

---

## ISW-BRIEF-07: CON-0188 — Owen & Crane Neuroscience Framework

**Target:** Part 3 compound-functioning chapter; cross-cutting design framework
**Current state:** MH, NDV, and DEM design principles are presented as separate design traditions with occasional cross-references.
**Change required:**
1. Add methodology note to Part 3 §3.2: "Owen & Crane (2022) demonstrate that trauma-informed design (MH), sensory-responsive design (NDV), and dementia-friendly design (DEM) share a common neuroscience mechanism: built environment modulation of threat/safety neural circuits (amygdala-prefrontal regulation, autonomic nervous system response). The shared design principles — control, predictability, safety, reduced sensory load — are not coincidental convergences but expressions of the same underlying brain-environment interaction."
2. Create cross-cutting reference note in frameworks-and-methodology BPC domain
3. Cite Owen, C. & Crane, J. (2022). IJERPH 19(21):14279. DOI:10.3390/ijerph192114279. PMID:36361166.
**Evidence:** Owen & Crane 2022 (citation-verified; attribution corrected from "Holohan 2022")
**Opus note:** This is a methodological connection, not a specification change. It restructures how the guidebook explains why cross-population convergences occur. The neuroscience framework provides the theoretical scaffolding for CON-0183 (RT60), CON-0186 (A-16), and future compound-interaction specifications. Route to Part 3 chapter author, not ISW.

---

## Disposition

| Brief | CON-ID | Route to | Priority |
|---|---|---|---|
| ISW-BRIEF-06 | CON-0186 | ISW (A-16 spec rewrite) | P1 — strongest connection |
| ISW-BRIEF-03 | CON-0183 | ISW (K-01 population tags) | P1 — simple tag addition |
| ISW-BRIEF-05 | CON-0185 | ISW (G-03/G-04 population tags) | P1 — simple tag addition |
| ISW-BRIEF-04 | CON-0184 | ISW (K-05 contraindication note) | P1 — safety-relevant |
| ISW-BRIEF-02 | CON-0182 | ISW (K-03 compound annotation) | P2 — requires zoning design |
| ISW-BRIEF-01 | CON-0181 | ISW (A-09 population extension) | P2 — inferred evidence |
| ISW-BRIEF-07 | CON-0188 | Part 3 chapter author | P3 — methodological |
