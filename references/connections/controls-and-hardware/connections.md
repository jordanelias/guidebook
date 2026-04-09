# Connections — controls-and-hardware
<!-- CO-0006 Phase 0B-1 migration 2026-04-08 — from connection-register-active.md -->

### CON-0007

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** E-01, E-06, E-08
**Target population(s):** DEAF, DBL, MH, DEM
**Evidence tier:** —
**Filed:** 2026-03-26
**Applied:** —

**Connection:** Three populations require circulation wide enough for two people side-by-side (one providing communication or support) from independent rationales:

- **DEAF:** 2440mm for signed conversation (ASL proxemics).
- **DBL:** ≥1500mm for intervenor accompaniment (Nordic ledsagarservice statutory right).
- **MH:** Support person/companion accompaniment (PTSD, agoraphobia). Not currently specified.
- **DEM:** Carer accompaniment on all routes; escort width implicit, not specified.

2440mm DEAF specification accommodates all. Currently coded DEAF-only.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| Deaf-spatial-design BPC (ASL proxemics) | Co-1 | DEAF | DEAF, DBL, MH, DEM |
| Nordic ledsagarservice statutes | 5 | DBL | DBL |
| DbI World Access guidelines | 2 | DBL | DBL, DEM |

**Action required:** Create Tier 0 companion-width specification: primary routes ≥1500mm clear (best practice 2440mm where DEAF primary). Unifies siloed specifications; resolves GAP-STEP6-03.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing

---

### CON-0054

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** E-14
**Target population(s):** OFS, PAIN, MOB/AMB, DEM
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Entrance recline seating within 5 m of all accessible entrances (GAP-FDR-T0-04) serves four populations: OFS (orthostatic recovery), PAIN (joint relief), MOB/AMB (rest before walking), DEM (orientation pause point). Documented as Tier 0 candidate in gap register; not yet in guidebook item specifications.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| pain-ofs-built-environment-design BPC | 2 | OFS, PAIN | Tier 0 universal |
| mobility-built-environment BPC | 2 | MOB/AMB | entrance seating |
| dementia-built-environment BPC | 2 | DEM | entrance seating |

**Action required:** Create new item: entrance recline seating ≤5 m from accessible entrance (E-14). Specify as Tier 0 universal provision — essential for OFS/PAIN/MOB/AMB/DEM; beneficial for all.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0061

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** E-08, accessible-circulation-geometry
**Target population(s):** DEAF, VIS, DBL, DEM, IntD
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Corridor width ≥1500 mm for two-person side-by-side walking specified for DEAF signing conversation (deaf-spatial-design BPC) also accommodates VIS sighted guide, DBL intervenor, DEM support person, and IntD care companion — all requiring side-by-side width. Five populations, single dimensional requirement, currently siloed.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| deaf-spatial-design BPC (Gallaudet 2010) | 2 | DEAF | VIS, DBL, DEM, IntD |
| accessible-circulation-geometry BPC | 4 | MOB | DEAF, VIS, DBL, DEM, IntD |
| deafblind-built-environment-design BPC | 4-5 | DBL | corridor width |

**Action required:** Consolidate 1500+ mm corridor width as multi-population provision (DEAF, VIS, DBL, DEM, IntD, MOB). Mechanism: side-by-side communication/support width universal across populations.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0037

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration; from archive register)
**Target item(s):** E-05, E-10
**Target population(s):** OFS, PAIN, MOB/AMB, DEM
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Entrance recline seating within 5 m of all accessible entrances serves OFS, PAIN, MOB/AMB, and DEM with no identified conflicts. More stringent than existing E-10 (≤25 m interval) and complements E-05 (weather protection). PARTIAL Tier 0 status confirmed for entrance-specific application; neutral for VIS, DEAF, NEU, NDV.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| PAIN/OFS FDR 2026-03-26 | THIN (expert consensus) | OFS, PAIN | MOB/AMB, DEM |
| RCOT HAwD 2019 + Roxburgh 2024 BJOT | Co-2 / Tier 1 | MOB, OFS, PAIN | Entrance-specific recline requirement |

**Action required:** Create new Tier 0 item **E-14 Entrance Rest Seating** — reclinable or tilt-capable seating within 5 m of threshold, seat height ≥480 mm AFF, arms both sides, alcove ≥900 mm wide, ≥200 mm recess from circulation path. Cross-reference E-05 and E-10. Evidence tier: THIN pending empirical validation.

**Disposition notes:** - [x] Draft E-14 as new Tier 0 item — parts/v10/e14-entrance-rest-seating.md
- [x] Cross-reference E-05 and E-10
- [x] Update GAP-FDR-T0-04 → CONSUMED (gap_register.md updated 2026-03-28)

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

---

---

## Connections CON-0131+ (Write-back from Opus batches, 2026-04-09)

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

