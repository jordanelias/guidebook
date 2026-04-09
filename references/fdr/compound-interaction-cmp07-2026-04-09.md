# CMP-07: Hearing Loss (DEAF) + Cognitive Impairment (DEM) → Shared Care Environment
**Date:** 2026-04-09 19:30
**Model:** Opus 4.6
**Note:** DEM communication FDR not formally run; audit proceeds on existing BPC evidence (DEM and DEAF BPCs both comprehensive). Classified as reduced-confidence per PI §Architecture rule 6.

---

## Scenario

A care environment (residential aged care, memory care unit, or supported housing) serves residents who are Deaf/hard-of-hearing AND residents with dementia. Both populations coexist in the same common areas, corridors, and dining spaces. Some individuals may have co-occurring DEAF+DEM (acquired hearing loss + cognitive decline — common in aged care).

## Parameter Pair Analysis

| Parameter pair | Classification | Mechanism |
|---|---|---|
| Visual fire alarm strobe (DEAF: requires VAD) × visual calm (DEM: reduced visual stimulation) | **CONDITIONAL** | Strobe activates only during emergency — not a continuous environmental stressor. However, DEM users may not understand the strobe's meaning (alarm semantics, not alarm perception). Resolution: pair strobe with staff-mediated evacuation for DEM. The strobe alerts DEAF users; staff training addresses DEM response. No environmental specification change needed — this is a procedural, not physical, resolution. |
| Hearing loop (DEAF: induction loop in common areas) × acoustic simplicity (DEM: quiet environment, no confusing sound sources) | **INDEPENDENT** | Hearing loop delivers sound only through hearing aid T-coil — no ambient acoustic effect. DEM users without hearing aids are unaffected. No interaction. |
| Wide corridor for signing (DEAF: ≥1800mm for parallel signing conversation) × loop floor plan (DEM: simple circulation, no dead ends) | **CONVERGENT** | Wider corridors serve both signing space AND DEM wayfinding clarity. Loop plan with wide corridors is the optimal configuration for both. |
| Visual paging/captioning (DEAF: text-based information display) × cognitive processing limit (DEM: cannot process complex text) | **CONDITIONAL** | DEAF users need detailed text alerts; DEM users need simple pictogram-based information. Resolution: two-layer information design — simple pictogram + alarm colour at eye level (DEM layer); detailed text/captioning on secondary screen or at staff station (DEAF layer). Spatial: pictogram signage throughout corridors (serves DEM); captioning screens in common rooms and staff areas (serves DEAF). |
| Open sightlines for signing (DEAF: need visual connectivity across rooms) × wandering privacy (DEM: dignity in personal care; wandering into visible spaces) | **CONDITIONAL** | Open sightlines in common areas serve DEAF communication. DEM privacy needs apply to personal care spaces and bedroom areas. Resolution: spatial zoning — common areas maintain open sightlines; bedroom corridors and bathroom approaches have visual screening. This is standard good practice and does not require compromise from either population. |
| Colour-coded wayfinding zones (DEM: distinct colour per wing) × no specific colour requirement (DEAF: no conflict) | **INDEPENDENT** | No interaction. DEAF users are unaffected by colour-coded wayfinding. DEM colour coding may actually benefit DEAF users with mild cognitive decline (aged care co-occurrence). |

## Result

| ANTAGONISTIC | CONVERGENT | INDEPENDENT | CONDITIONAL |
|---|---|---|---|
| **0** | 1 | 2 | 3 |

## Synthesis

DEAF+DEM resolves at Tier 1. No antagonistic parameter pairs exist. The three conditional interactions all resolve through **spatial zoning** (common vs personal areas) or **two-layer information design** (pictogram for DEM, text for DEAF). The convergent parameter (wide corridors + loop plan) reinforces both populations simultaneously.

The most significant finding is the **alarm comprehension gap**: DEM users may not understand what a fire alarm means, regardless of the sensory channel. This is not a DEAF×DEM environmental conflict — it is a DEM-only cognitive processing limitation that applies equally whether the alarm is auditory, visual, or vibrotactile. The resolution is procedural (staff-mediated evacuation protocol) rather than environmental. The environment's role is to ensure the alarm reaches both populations through their respective channels; the comprehension gap is addressed through staffing and training, not specification.

**Reduced-confidence disclosure:** This audit was conducted without a dedicated DEM communication FDR run (opus_synthesis: false for communication-specific DEM evidence). The conclusions are consistent with existing DEM BPC evidence but carry reduced confidence per PI §Architecture rule 6. Recommend Opus verification if communication-specific DEM evidence surfaces.

## Connection

**CON-0157 (NEW)**
**Status:** PENDING
**Confidence:** HIGH (reduced-confidence on DEM communication layer)
**Target items:** B-10, H-03, D-08, E-08
**Target populations:** DEAF, DEM
**Filed in:** cross-cutting
**Action required:** Add DEAF+DEM compound note to Part 3 §3.10. Note two-layer information design principle. Note alarm comprehension gap as procedural (Part 9 staffing), not environmental.
