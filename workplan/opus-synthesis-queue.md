# Opus Synthesis Queue
**Generated:** 2026-03-29 19:02
**Purpose:** Track which BPC slugs need Opus 4.6 best-practice synthesis

## Status Summary

| Category | Count |
|---|---|
| Opus synthesis complete | 21 |
| Merged (redirect stubs) | 4 |
| Stubs (research blocked) | 2 |
| **Ready for Opus synthesis** | **42** |

Tier A (population-specific): 1
Tier B (topic-specific evidence): 26
Tier C (framework/methodology): 13
Provisional (partial evidence, synthesize what exists): 2

## Blocked — Cannot Synthesize

| Slug | Reason |
|---|---|
| `economics/case-study-economics-financial-data` | STUB — research scheduled Phase 2B Session 7 |
| `frameworks-and-methodology/accessible-design-failures-poor-performance` | STUB — research scheduled Phase 2B Session 8 |

## Proposed Session Batching

Batches grouped by domain for context efficiency. ~4–6 slugs per session.

### Session O1: Population + Health (6 slugs)
- `population-general/intellectual-disability-built-environment-design`
- `health-and-symptom-management/ms-thermal-temperature-conflict-resolution`
- `health-and-symptom-management/ofs-built-environment`
- `health-and-symptom-management/thermal-comfort-older-adults-care-settings`
- `health-and-symptom-management/pain-ofs-built-environment-design` [PROVISIONAL — THIN BASE]
- `entrances-and-circulation/threshold-door-hardware` [PARTIAL — 12/24 searched]

### Session O2: Sensory Environment (1) (4 slugs)
- `sensory-environment/air-quality-voc-chemical-sensitivity-built-environment`
- `sensory-environment/biophilic-design-healthcare-workplace`
- `sensory-environment/circadian-lighting-melanopic-edi`
- `sensory-environment/room-acoustic-performance`

### Session O3: Sensory Environment (2) (3 slugs)
- `sensory-environment/sensory-room-user-control`
- `sensory-environment/therapeutic-lighting-design`
- `sensory-environment/visual-fire-alarm-seizure-safety`

### Session O4: Wayfinding (1) (4 slugs)
- `wayfinding-and-signage/cognitive-wayfinding-design`
- `wayfinding-and-signage/detectable-gradient-protocol-sensory-zones`
- `wayfinding-and-signage/luminance-contrast-lrv-evidence-base`
- `wayfinding-and-signage/visual-alerting-and-wayfinding-light`

### Session O5: Wayfinding (2) (2 slugs)
- `wayfinding-and-signage/wayfinding-cognitive-science-spatial-design`
- `wayfinding-and-signage/wayfinding-dementia-spatial-design`

### Session O6: Entrances + Circulation (5 slugs)
- `entrances-and-circulation/accessible-circulation-geometry`
- `entrances-and-circulation/floor-vibration-wheelchair-disability`
- `entrances-and-circulation/residential-entry-and-threshold`
- `entrances-and-circulation/stair-ramp-threshold-biomechanics-accessibility`
- `entrances-and-circulation/threshold-and-level-access`

### Session O7: Controls + Rooms + Comms (5 slugs)
- `communication-and-alerts/deaf-classroom-reverberation-time`
- `controls-and-hardware/reach-range-and-accessible-controls`
- `kitchens-and-workspaces/residential-kitchen-and-task-surfaces`
- `room-types/accessible-laundry-room-design`
- `seating-and-rest/bariatric-turning-radius-built-environment`

### Session O8: Framework (1) (5 slugs)
- `economics/accessible-design-economics-cost-premium`
- `economics/government-grant-programmes-home-adaptation`
- `frameworks-and-methodology/body-sizes-supplementary-populations`
- `frameworks-and-methodology/design-framework-evidence-audit`
- `frameworks-and-methodology/ecological-psychology-haptic-affordances-built-environment`

### Session O9: Framework (2) (4 slugs)
- `frameworks-and-methodology/european-accessibility-act-scope-clarification`
- `frameworks-and-methodology/jurisdiction-grant-programmes-comprehensive`
- `frameworks-and-methodology/jurisdiction-matrix-accessibility-standards`
- `frameworks-and-methodology/multilingual-evidence-convergence-non-english`

### Session O10: Framework (3) (4 slugs)
- `frameworks-and-methodology/ot-built-environment-interface`
- `frameworks-and-methodology/ot-frameworks-built-environment`
- `frameworks-and-methodology/residential-dar-provisions-priority-register`
- `frameworks-and-methodology/visitability-residential-accessibility-minimum-standards`

## Opus Session Protocol

Each session:
1. Switch model picker to Opus 4.6
2. Load this queue file + the batch's slug files via `batch_read`
3. For each slug: read full BPC entry → synthesize → write `**Opus synthesis:** YES [OPUS-SYNTHESIS]` marker + consensus finding + key evidence hierarchy
4. Commit updated slugs to GitHub
5. Mark session complete in this file

## Completion Tracker

| Session | Status | Date |
|---|---|---|
| O1 | PENDING | — |
| O2 | PENDING | — |
| O3 | PENDING | — |
| O4 | PENDING | — |
| O5 | PENDING | — |
| O6 | PENDING | — |
| O7 | PENDING | — |
| O8 | PENDING | — |
| O9 | PENDING | — |
| O10 | PENDING | — |

## Already Complete (21 slugs)

- `bathrooms-and-wet-areas/accessible-bathroom-and-grab-bar`
- `bathrooms-and-wet-areas/fold-down-grab-bar-specification`
- `communication-and-alerts/assistive-listening-systems`
- `communication-and-alerts/deaf-acoustic-built-environment`
- `communication-and-alerts/deaf-spatial-design`
- `frameworks-and-methodology/cross-population-case-studies`
- `frameworks-and-methodology/cross-population-conflict-resolutions`
- `frameworks-and-methodology/residential-accessible-home-case-studies`
- `population-general/deafblind-built-environment-design`
- `population-general/dementia-built-environment`
- `population-general/mental-health-built-environment`
- `population-general/mobility-built-environment`
- `population-general/ndv-aut-built-environment-quantified-thresholds`
- `population-general/neurodivergent-built-environment`
- `population-general/neurological-built-environment`
- `population-general/ot-cpg-built-environment`
- `population-general/upper-limb-impairment-built-environment`
- `population-general/visual-impairment-built-environment`
- `sensory-environment/acoustics-speech-intelligibility-disability`
- `sensory-environment/sensory-processing-model-design-application`
- `sensory-environment/sensory-relief-space-design`
