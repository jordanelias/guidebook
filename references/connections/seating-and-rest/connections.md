# Connections — seating-and-rest
<!-- CO-0006 Phase 0B-1 migration 2026-04-08 — from connection-register-active.md -->

### CON-0057

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** I-03
**Target population(s):** DEM, NEU, OFS, PAIN
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Thermostatic shower valve ≤37°C specified for OFS heat intolerance (pain-ofs-built-environment-design BPC) also prevents scalding risk for DEM and NEU populations documented in thermal-comfort-older-adults-care-settings BPC. Single specification serves four populations through two mechanisms: therapeutic temperature control (OFS) and safety (DEM/NEU).

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| pain-ofs-built-environment-design BPC | 3 | OFS | DEM, NEU safety |
| thermal-comfort-older-adults-care-settings BPC | 2 | DEM, older adults | thermostatic valve cross-ref |

**Action required:** Add DEM and NEU as co-populations for thermostatic shower valve specification. Dual mechanism: OFS therapeutic + DEM/NEU/PAIN safety.

**Disposition notes:** - [x] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0062

**Status:** CONSUMED
**Confidence:** MODERATE
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** I-02, residential-kitchen-and-task-surfaces
**Target population(s):** LPA, MOB, OFS, PAIN, VIS
**Evidence tier:** —
**Filed:** 2026-03-28
**Applied:** —

**Connection:** Height-adjustable kitchen worktop (685-900 mm, per residential-kitchen-and-task-surfaces BPC) specified for MOB wheelchair users also serves LPA (lower reach range), OFS/PAIN (seated work), and VIS (tactile work surface at consistent height). Currently coded MOB-primary; other populations documented in respective BPCs but not cross-referenced.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| residential-kitchen-and-task-surfaces BPC | 2 | MOB | LPA, OFS, PAIN, VIS |
| reach-range-and-accessible-controls BPC | 4 | MOB, LPA | kitchen items |
| body-sizes-supplementary-populations BPC | 3 | LPA | kitchen worktop |

**Action required:** Add LPA, OFS, PAIN, VIS as co-populations for height-adjustable kitchen worktop specification. Mechanism: adjustability serves five populations via different reach/work-position requirements.

**Disposition notes:** - [ ] HIGH → item-specification-writer briefing
- [x] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item

---

### CON-0103

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** I-04, G-03, G-04, Part 9 §9.5
**Target population(s):** MOB, UPL, NEU, OFS
**Evidence tier:** —
**Filed:** 2026-04-03
**Applied:** —

**Connection:** I-04 (Ceiling Hoist) specifies structural ceiling blocking rated ≥1.5 kN/m² along the full transfer path from bed to bathroom. G-03 (Grab Bars) specifies wall blocking zones for bilateral grab bar mounting at WC, shower, and bath positions. G-04 (Wet Room Configuration) specifies floor gradient, turning circle, and drainage positions.

The three specifications interact physically:
1. Ceiling hoist track path must align with G-04 turning circle and G-03 grab bar positions — the user transfers from hoist sling to WC/shower seat at specific positions defined by G-03/G-04 layout.
2. Hoist track mounting may require structural reinforcement that conflicts with ceiling-mounted shower heads, exhaus…

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| RCOT Adaptations Without Delay 2019 | Co-2 | MOB | I-04/G-03/G-04 coordination |
| BS 8300:2018 | 5 | ALL | Ceiling hoist structural |
| accessible-bathroom-and-grab-bar BPC | 2–4 | MOB, UPL | I-04 spatial coordination |

**Action required:** Add reciprocal cross-references: G-03 add note "Where ceiling hoist provision (I-04) is specified, grab bar wall blocking zones must align with hoist transfer positions — coordinate at Schematic Design." G-04 add note "Ceiling hoist track (I-04) requires continuous ceiling level across the full transfer path — verify no step-down between shower zone and WC zone ceiling heights." Part 9 §9.5 struct…

**Disposition notes:** - [x] MEDIUM → APPLIED 2026-04-03: G-03 cross-ref updated (I-04 coordination note: hoist track alignment with grab bar blocking zones). G-04 CON-0103 note embedded within I-04 CON-0107 retrofit note (ceiling continuity across hoist transfer path).

---

### CON-0105

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** H-05, I-04
**Target population(s):** MOB, UPL, NEU, OFS
**Evidence tier:** —
**Filed:** 2026-04-03
**Applied:** —

**Connection:** I-04 (Ceiling Hoist) does not specify an emergency lowering procedure. If the ceiling hoist motor fails during a transfer, the occupant is suspended. H-05 (Nurse Call) is the emergency communication channel in care environments, but H-05 does not reference hoist failure as a scenario requiring call activation.

Safe practice requires: (1) hoist motor with manual emergency lowering; (2) nurse call point accessible from the hoist sling position (not just from bed and WC positions); (3) wireless pendant (H-05 specification) carried during all hoist transfers.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| RCOT Adaptations Without Delay 2019 | Co-2 | MOB | Emergency lowering protocol |
| NHS HTM 08-03 | 5 | ALL | Nurse call coverage in hoist zone |

**Action required:** Add to I-04: "Hoist motor to include manual emergency lowering mechanism operable by a single carer. Nurse call point (H-05) to be accessible from the hoist sling position — either wireless pendant or wall-mounted call point within reach of transfer path." Add to H-05: "Coverage must include the ceiling hoist transfer path (I-04) — pendant or wall-mounted call point within reach of a suspended occ…

**Disposition notes:** - [x] MEDIUM → APPLIED 2026-04-03: I-04 Design Stage section updated with emergency lowering mechanism specification (manual, single-carer operable) and nurse call coverage requirement at hoist sling position.

---

### CON-0107

**Status:** CONSUMED
**Confidence:** HIGH
**Opus-reviewed:** false
**Source BPC slug(s):** — (pre-migration)
**Target item(s):** I-04, F-07, F-08
**Target population(s):** MOB, NEU, OFS, PAIN
**Evidence tier:** —
**Filed:** 2026-04-03
**Applied:** —

**Connection:** I-04 (Ceiling Hoist) specifies provision in all accessible bathrooms and primary bedrooms in specialist residential, care, and healthcare settings. F-07 (Thermal Zoning) specifies ambient ≤18°C with individual supplemental heating. A user requiring a ceiling hoist in a care bedroom is likely to have high co-occurrence with NEU/MS (progressive conditions requiring hoist transfer) or OFS (weight-bearing intolerance requiring hoist transfer).

The supplemental radiant heating panels (F-07) must not obstruct the ceiling hoist track path (I-04). Wall-mounted radiant panels in I-04 bedrooms must be positioned outside the hoist sweep zone. This spatial coordination is not documented.

**Evidence basis:**
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|
| ms-thermal BPC | 2–4 | NEU/MS | I-04 bedroom heating coordination |
| RCOT 2019 | Co-2 | MOB | Hoist track clearance zone |

**Action required:** Add coordination note to I-04: "Where F-07 supplemental radiant heating is specified in bedrooms with ceiling hoist provision, radiant panels to be wall-mounted outside the hoist track sweep zone. Verify no thermal panel obstruction of hoist motor travel path at Detailed Design." Add reciprocal note to F-07: "In care bedrooms with ceiling hoist (I-04), supplemental radiant heating panels must clea…

**Disposition notes:** - [x] MEDIUM → APPLIED 2026-04-03: I-04 Retrofit section updated with hoist track/radiant panel spatial coordination note. F-07 Population conflict section updated with CON-0107 reciprocal coordination note.

---
