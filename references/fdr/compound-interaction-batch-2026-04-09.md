# Connection-Scout Step 2b — Compound Interaction Batch
**Date:** 2026-04-09 05:30
**Scenarios assessed:** FDR-CMP-01 through CMP-08
**Method:** Per compound-interaction-audit-methodology.md

---

## Pre-Audit: Input Readiness Check

| CMP-ID | Constraint A | Constraint B | A FDR data? | B FDR data? | Ready? |
|---|---|---|---|---|---|
| CMP-01 | hemiplegia (MOB) | chronic pain (PAIN) | YES (FDR-BAB-01) | YES (pain-ofs BPC) | YES |
| CMP-02 | visual impairment (VIS) | fatigue (OFS) | YES (FDR-VI-01/02/03) | YES (FDR-ACG-01) | YES |
| CMP-03 | seated wheelchair (MOB) | cognitive impairment (DEM) | YES (FDR-KIT-01) | PARTIAL (DEM kitchen not yet run) | NO — run FDR-NEW-05 first |
| CMP-04 | dementia (DEM) | visual impairment (VIS) | YES (FDR-DEM-01) | YES (FDR-VI-01) | YES |
| CMP-05 | hemiplegia (MOB) | shoulder pain (PAIN) | YES (FDR-BAB-01) | YES (FDR-FGB-02) | YES |
| CMP-06 | lower limb spasticity (NEU) | orthostatic (OFS) | YES (FDR-MOB-03) | YES (ofs BPC) | YES |
| CMP-07 | hearing loss (DEAF) | cognitive impairment (DEM/NEU) | YES (FDR-DEAF-01) | PARTIAL (DEM communication not run) | NO — run FDR-NEW-13 first |
| CMP-08 | tremor + VIS (MOB+NEU+VIS) | triple compound | PARTIAL (tremor not yet run) | YES (FDR-VI-02) | NO — run FDR-NEW-15 first |

**Ready for audit: 5 of 8 (CMP-01, -02, -04, -05, -06)**
**Blocked: 3 (CMP-03, -07, -08) — require granular FDR runs first**

---

## Audit Results

### CMP-01: Hemiplegia + Chronic Pain → Transfer

| Parameter pair | Classification | Mechanism |
|---|---|---|
| Affected-side grab bar (MOB) × pain-side avoidance (PAIN) | **ANTAGONISTIC** | MOB bar position assumes affected-side loading; PAIN prohibits that loading |
| Lateral clearance 45-50cm (MOB) × pain-modified approach angle (PAIN) | **CONDITIONAL** | If pain is ipsilateral to hemiplegia: approach must be front-on, not lateral; if contralateral: standard lateral approach works |
| Seat-relative bar height 28cm (MOB) × shoulder ROM limit (PAIN) | **CONDITIONAL** | Pain in shoulder may reduce ROM for bar grip; bar height must accommodate both hemi trunk support AND pain-limited reach |

**Result:** 1 ANTAGONISTIC + 2 CONDITIONAL. → COMPOUND-INTERACTION connection **CON-0151**
**ISW brief:** Transfer specification for hemiplegia+pain must include front-approach option; bar position cannot assume affected-side loading without OT verification of pain location.

---

### CMP-02: Visual Impairment + Fatigue → Circulation

| Parameter pair | Classification | Mechanism |
|---|---|---|
| Tactile guidance strip (VIS) × rest point interval (OFS) | **INDEPENDENT** | Both specified; no interaction. Tactile strip leads TO rest point — synergistic |
| Cognitive load of navigation (VIS) × cognitive reserve depletion (OFS) | **ANTAGONISTIC** | VIS navigation requires active scanning and counting; OFS fatigue reduces cognitive capacity for this; standard rest point intervals insufficient because cognitive fatigue accumulates faster than physical fatigue |
| Contrast wayfinding (VIS) × lighting level for energy conservation (OFS) | **INDEPENDENT** | OFS does not require dim lighting; contrast works at standard illumination |

**Result:** 1 ANTAGONISTIC + 2 INDEPENDENT. → COMPOUND-INTERACTION connection **CON-0152**
**ISW brief:** Rest point intervals for VIS+OFS compound should be shorter than either population's individual specification (cognitive fatigue accumulates faster). Specify rest points at half the standard OFS interval where VIS tactile navigation is the primary wayfinding method.

---

### CMP-04: Dementia + Visual Impairment → Wayfinding

| Parameter pair | Classification | Mechanism |
|---|---|---|
| Tactile learned route (VIS) × memory loss (DEM) | **ANTAGONISTIC** | VIS tactile route requires learning; DEM impairs learning |
| Colour-coded landmarks (DEM) × absent vision (VIS) | **ANTAGONISTIC** | DEM colour system requires vision; VIS removes it |
| Simplified layout (DEM) × consistent predictable layout (VIS) | **CONVERGENT** | Both populations benefit from simple, predictable spatial geometry |
| Floor texture differentiation (VIS) × plain floor (DEM) | **ANTAGONISTIC** | VIS uses texture for orientation; DEM plain floor prevents perceived obstacles |

**Result:** 3 ANTAGONISTIC + 1 CONVERGENT. → COMPOUND-INTERACTION connection **CON-0153** + **SPECIFICATION-LIMIT** flag
**ISW brief:** No environmental wayfinding system resolves this compound through specification alone. Convergent parameter (simplified layout) is the maximum architectural contribution. Human wayfinding assistance is the Tier 2 resolution. Flag for Part 1 §1.9 Scope as specification boundary.

---

### CMP-05: Hemiplegia + Shoulder Pain → Dressing

| Parameter pair | Classification | Mechanism |
|---|---|---|
| Unaffected arm compensatory dressing (MOB) × shoulder pain on unaffected side (PAIN) | **ANTAGONISTIC** | Hemiplegic dressing relies entirely on unaffected arm; shoulder pain on that arm eliminates the compensatory mechanism |
| Closet pull-down rail (MOB) × overhead reach prohibition (PAIN-shoulder) | **CONVERGENT** | Both populations benefit from waist-height storage; pull-down rail serves both |
| Dressing bench seat height (MOB) × pain-optimal seated posture (PAIN) | **CONDITIONAL** | If pain is in trunk: higher seat reduces trunk flexion demand; if pain is in shoulder: seat height less relevant |

**Result:** 1 ANTAGONISTIC + 1 CONVERGENT + 1 CONDITIONAL. → COMPOUND-INTERACTION connection **CON-0154**
**ISW brief:** Closet geometry for hemiplegia+shoulder-pain compound must eliminate overhead reach AND provide bilateral access options (not just unaffected-side). Motorised wardrobe carousel is the specification candidate.

---

### CMP-06: Spasticity + Orthostatic → Sit-to-Stand

| Parameter pair | Classification | Mechanism |
|---|---|---|
| Slow controlled rise (NEU) × staged positional change (OFS) | **CONVERGENT** | Same direction, different mechanisms |
| Firm non-compliant floor (NEU) × stable surface for standing (OFS) | **CONVERGENT** | Both require firm surface |
| Seat height ≥450mm (NEU-spasticity) × seat height for OFS staged rise (OFS) | **CONVERGENT** | Both benefit from higher seat; 450-500mm serves both |

**Result:** 3 CONVERGENT + 0 ANTAGONISTIC. → No COMPOUND-INTERACTION connection needed.
**Note:** This compound is a pure convergence. Specifications align. Tier 1 sufficient. Document as validation that compound does not always produce conflict.

---

## Summary

| CMP-ID | Antagonistic | Convergent | Conditional | Independent | Connection? | Spec limit? |
|---|---|---|---|---|---|---|
| CMP-01 | 1 | 0 | 2 | 0 | CON-0151 | No |
| CMP-02 | 1 | 0 | 0 | 2 | CON-0152 | No |
| CMP-04 | 3 | 1 | 0 | 0 | CON-0153 | **YES** |
| CMP-05 | 1 | 1 | 1 | 0 | CON-0154 | No |
| CMP-06 | 0 | 3 | 0 | 0 | None | No |

**New connections generated: 4** (CON-0151 through CON-0154)
**Kawa connections: 3** (CON-0148 through CON-0150)
**Total new connections this session: 7**
**Specification limits identified: 1** (CMP-04 DEM+VIS wayfinding)
**Blocked scenarios: 3** (CMP-03, -07, -08 — awaiting granular FDR runs)
