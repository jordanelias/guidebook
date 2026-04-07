# Opus Synthesis Queue
**Generated:** 2026-03-29 19:02
**Purpose:** Track which BPC slugs need Opus 4.6 best-practice synthesis

## Status Summary

| Category | Count |
|---|---|
| Opus synthesis complete | 44 |
| Merged (redirect stubs) | 4 |
| Stubs (research blocked) | 2 |
| **Ready for Opus synthesis** | **19** |

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
| O1 | COMPLETE | 2026-03-29 |
| O2 | COMPLETE | 2026-03-29 |
| O3 | COMPLETE | 2026-03-29 |
| O4 | COMPLETE | 2026-03-29 |
| O5 | COMPLETE | 2026-03-29 |
| O6 | COMPLETE | 2026-03-29 |
| O7 | COMPLETE | 2026-03-29 |
| O8 | COMPLETE | 2026-03-29 |
| O9 | COMPLETE | 2026-03-29 |
| O10 | COMPLETE | 2026-03-29 |

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

## v4 Schema Synthesis Pass (2026-03-30)

23 slugs had v4 schema stubs populated with synthesized content from existing Opus prose:

**Batch 1 (7 slugs) — d1e7cba:**
ms-thermal-temperature-conflict-resolution, thermal-comfort-older-adults-care-settings, air-quality-voc-chemical-sensitivity-built-environment, detectable-gradient-protocol-sensory-zones, wayfinding-cognitive-science-spatial-design, wayfinding-dementia-spatial-design, stair-ramp-threshold-biomechanics-accessibility

**Batch 2 (6 slugs) — 3076477:**
accessible-design-economics-cost-premium, government-grant-programmes-home-adaptation, body-sizes-supplementary-populations, design-framework-evidence-audit, ecological-psychology-haptic-affordances-built-environment, european-accessibility-act-scope-clarification

**Batch 3 (7 slugs) — 33180e0:**
jurisdiction-grant-programmes-comprehensive, jurisdiction-matrix-accessibility-standards, multilingual-evidence-convergence-non-english, ot-built-environment-interface, ot-frameworks-built-environment, residential-dar-provisions-priority-register, visitability-residential-accessibility-minimum-standards

**Batch 4 (3 partial slugs) — 7435481:**
circadian-lighting-melanopic-edi, visual-fire-alarm-seizure-safety, deaf-classroom-reverberation-time

**Remaining 19 slugs with stubs=0** already had complete v4 schema content from O1–O10 sessions. No action required.

**GAP-TRIAGE-02 status:** CLOSED-RESOLVED. All CONSUME slugs now have populated v4 schema sections.


---

## CO-0005 Evidence Expansion Programme — Opus Queue Additions (2026-04-05)

| Slug | Type | Synthesis task | Trigger |
|---|---|---|---|
| `thermoregulation-built-environment` | P1 new | Climate-stratified best-practice table (tropical/subtropical/temperate/cold). Identify where F-07/CON-0101/CON-0107 require climate-conditional variants. | After Phase 1-A LOG |
| `sensory-space-global-south` | P1 new | Cross-cultural sensory space transfer analysis. Where PAS 6463 transfers; where it requires adaptation; what low-resource alternatives exist. | After Phase 1-B LOG |
| `wayfinding-global-south` | P1 new | ISO 21542 vs. Global South evidence convergence. Whether tactile/auditory/contrast specs require climate/substrate/maintenance variants. | After Phase 1-C LOG |
| `bathroom-typology-global-south` | P1 new | Typology-classified specification table (enclosed NE / wet room / split / shared). For each: what transfers from BPC, what requires variant, what has no evidence. | After Phase 1-D LOG |
| `co1-housing-research-global-south` | P1 new | Top 10 barriers from Co-1 Global South evidence. Cross-reference to existing BPC. Output = prioritised gap list, not specification table. | After Phase 1-E LOG |
| `crpd-implementation-built-environment` | P2 new | Mapping only — no synthesis. Output feeds back as gap flags on existing slugs. | N/A |
| `threshold-door-hardware` | P2 expansion | Determine whether new jurisdiction evidence is additive or requires revision to existing best_practice_synthesis. | After Phase 3-A LOG |
| `pain-ofs-built-environment-design` | P2 expansion | Expansion review — additive or revision? | After Phase 3-B LOG |
| `acoustics-speech-intelligibility-disability` | P2 expansion | Expansion review — alternative ALT solutions for low-resource settings. | After Phase 3-C LOG |
| `dementia-built-environment` | P2 expansion | Expansion review — Global South dementia-environment evidence vs. existing synthesis. | After Phase 3-D LOG |
| `intellectual-disability-built-environment-design` | P2 expansion | Expansion review — communal/family care typologies vs. current Western individual-unit assumptions. | After Phase 3-E LOG |
| `post-occupancy-evaluation-global` | P3 new | What performs, what fails, what is unknown in Global South contexts. | After Phase 4 LOG |


---

## CO-0005 Phase 1 Research Complete — Synthesis Ready (2026-04-07)

All Phase 1 GAPs (LRP-01 through LRP-05) and Phase 2 initial pass (LRP-11) are now OPEN-RESEARCHED.
Total new slugs ready for Opus synthesis: 6.

| Slug | Status | Synthesis priority | Notes |
|---|---|---|---|
| `thermoregulation-built-environment` | PARTIAL LOG | HIGH — needed for Part 4 thermal specs + conflict matrices | FMS vs MS/SCI conflict requires Opus arbitration; tropical gap requires scope statement |
| `sensory-space-global-south` | PARTIAL LOG | HIGH — PAS 6463 cultural transfer question is unresolved | Collectivist culture transfer problem: Opus to determine whether new BPC section or scope disclaimer |
| `wayfinding-global-south` | PARTIAL LOG | MEDIUM — ISO specs confirmed transferable; implementation/maintenance gap only | Primarily a policy/enforcement finding, not a specification revision |
| `bathroom-typology-global-south` | PARTIAL LOG | HIGH — squat toilet gap requires design decision | Sejong Toilet is Co-1/Tier 1 but unpublished; Opus to determine citation validity |
| `co1-housing-research-global-south` | COMPLETE LOG | HIGH — formal/informal divide scope question must be resolved before any Global South specification is written | Output = scope decision + prioritised gap list |
| `crpd-implementation-built-environment` | PARTIAL LOG | MEDIUM — mapping only, feeds existing slugs | No new specifications; identifies treaty-body endorsement for existing specs |

**Recommended Opus session sequence:**
1. `co1-housing-research-global-south` first — scope decision gates all other Global South synthesis
2. `thermoregulation-built-environment` + `bathroom-typology-global-south` — specification decisions
3. `sensory-space-global-south` — scope/transfer decision
4. `wayfinding-global-south` + `crpd-implementation-built-environment` — mapping passes
