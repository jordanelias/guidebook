## Conflict Domain: COLOUR-CONT
**Parameter:** LRV contrast levels
**Status:** MIXED — partial reclassification; Opus synthesis complete [2026-03-30]
**Date created:** 2026-03-30
**Opus synthesis:** 2026-03-30
**Feeds:** Part 5 §5.2 conflict resolution table; C-series item specifications

### Opposition Map (corrected from skill domain table)

The original domain table describes the opposition as "VIS, DEM: high contrast ≥30 LRV everywhere" vs "NDV/SENS: muted, low contrast." This conflates two independent perceptual variables:

- **LRV contrast** (luminance difference between adjacent surfaces) — a lightness parameter. Detectable by photometer. Governs hazard perception, wayfinding boundary detection, surface differentiation.
- **Chroma** (colour saturation/intensity) — a colourfulness parameter. Governs visual complexity, sensory stimulation, palette "loudness."

A muted, desaturated palette CAN have high LRV contrast. Example: pale cream wall (LRV 80) + charcoal grey skirting (LRV 15) = 65 LRV points, fully muted. Conversely, high-chroma surfaces CAN have low LRV contrast. Example: vivid red (LRV 15) + vivid blue (LRV 12) = 3 LRV points, highly saturated but nearly invisible to contrast-dependent VIS users.

The NDV/SENS need (per NDV BPC, 2026-03-29) is: "muted, low-chroma palette (NCS chroma ≤4)" — this is a chroma specification, not an LRV contrast specification. NDV/SENS populations do not need LOW contrast; they need LOW CHROMATIC STIMULATION.

### Corrected Opposition

| Sub-parameter | VIS/DEM need | NDV/SENS need | Opposition? |
|---|---|---|---|
| **LRV contrast at critical junctions** | ≥30 LRV (regulatory floor); ≥50 LRV (guidebook target); ≥65% Michelson (severe VI) | No evidence against. NDV/SENS literature does not identify luminance contrast as a sensory trigger. | **NO CONFLICT** |
| **Colour coding saturation** | DEM: colour-coded wayfinding cues (traditionally high-saturation primaries for maximum salience) | NDV/SENS: NCS chroma ≤4; muted palette; no vivid/high-saturation surfaces | **PARTIAL CONFLICT** (on saturation of wayfinding colour coding only) |
| **Pattern complexity** | VIS: no requirement for pattern. DEM: no requirement for pattern (dark patterns contraindicated per DEM BPC — perceived as holes). | NDV/SENS: no patterned flooring; minimal wall patterns | **NO CONFLICT** (all populations aligned against complex patterns) |

### Domain Classification: MIXED (largely compatible)

**LRV contrast sub-parameter: COMPATIBLE (no conflict)**
High LRV contrast using desaturated colours serves VIS, DEM, and NDV/SENS simultaneously. The LRV BPC (2026-03-29) finding — 30% LRV is a regulatory floor with unknown empirical basis; guidebook target ≥50% — is achievable within a fully muted, NCS chroma ≤4 palette. No population conflict exists for LRV contrast.

Universal Mode specification: ≥30 LRV contrast at all critical junctions (code compliance). Guidebook target: ≥50 LRV. Achievable in muted palette.

**Colour coding saturation sub-parameter: PARTIAL CONFLICT**
DEM wayfinding literature traditionally uses high-saturation colour coding (bright red toilets, vivid yellow activity rooms) for maximum cognitive salience. NDV/SENS requires NCS chroma ≤4 (muted, desaturated).

However, the cognitive-wayfinding BPC (2026-03-29, Opus synthesis) establishes that 3D objects — not colour — are the primary wayfinding mechanism for DEM: "3D object landmarks at decision points > colour-coded walls for DEM orientation" (Tier 3: Marquardt 2011; van Buuren 2022). Colour coding is secondary, not primary. This reduces the conflict from "opposing needs" to "secondary aid calibration."

### Resolution Evidence

**Resolution 1 — Desaturated colour coding with LRV differentiation:**
DEM colour coding can use muted but LRV-distinct hues rather than high-saturation primaries. Example: sage green (LRV 45, NCS chroma 2) for lounge, dusty rose (LRV 55, NCS chroma 3) for bedrooms, warm grey (LRV 35, NCS chroma 1) for corridors. These are distinct from each other in LRV AND hue while remaining within NDV/SENS chroma tolerance.

Evidence: cognitive-wayfinding BPC — 3D objects are primary cue; colour is secondary. Therefore colour coding does not need maximum chromatic salience. The LRV BPC confirms that luminance (not chroma) is the dominant perceptual variable for surface differentiation.

Status: **RESOLVED-CONSENSUS** — desaturated colour coding with high LRV contrast satisfies both populations. 3D objects carry the primary wayfinding load.

**Resolution 2 — Pattern elimination as universal:**
All three populations (VIS, DEM, NDV/SENS) are aligned against complex floor/wall patterns. DEM BPC: "no dark-coloured floor mats at thresholds (perceived as holes)." NDV BPC: "no patterned flooring." VIS BPC: "no high-gloss or reflective flooring." This is a convergent elimination — Universal Mode universal: no complex geometric floor patterns, no high-gloss surfaces, no dark threshold mats.

Status: **CONVERGENT** — universal specification.

### Guidebook Specification Implications

| Specification | Tier | Note |
|---|---|---|
| LRV contrast ≥30 at critical junctions (code) | Universal Mode | No conflict. Universal. |
| LRV contrast ≥50 at critical junctions (guidebook target) | Universal Mode | No conflict. Achievable in muted palette. |
| Muted palette (NCS chroma ≤4) as default in shared spaces | Tier 1 (NDV/SENS) | Compatible with DEM colour coding via desaturated hues. |
| 3D object landmarks as primary wayfinding (not colour) | Universal Mode (DEM + NDV compatible) | Cognitive-wayfinding BPC resolution. |
| No complex geometric floor patterns | Universal Mode | Universal elimination. All populations aligned. |
| No dark threshold mats | Universal Mode | DEM, VIS, and general safety aligned. |

### Unresolved Gaps

| Gap ID | Description | Priority |
|---|---|---|
| GAP-CONF-CCONT-01 | No controlled study comparing DEM wayfinding performance with high-chroma vs desaturated colour coding (holding 3D objects and LRV contrast constant). Resolution 1 is inferred from the primacy of 3D objects over colour. | P3 |

### Skill Table Correction

The conflict domain table (cross-population-conflict-mapper §1) should be annotated: COLOUR-CONT opposition is primarily between colour SATURATION (chroma) for DEM wayfinding vs NDV/SENS low-stimulation palette — NOT between LRV contrast levels. LRV contrast is NOT a conflict dimension. Rename sub-parameter "Colour coding chroma" to clarify.

---
*Cross-population-conflict-mapper COLOUR-CONT domain. Opus synthesis 2026-03-30. Classification: MIXED (LRV contrast compatible — no conflict; colour coding chroma partially conflicting — resolved via desaturated coding + 3D object primacy; pattern elimination convergent). Original domain table corrected: chroma and LRV contrast are independent variables.*
