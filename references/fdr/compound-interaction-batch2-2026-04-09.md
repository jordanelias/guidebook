# Compound Interaction Audits — CMP-03 and CMP-08
**Date:** 2026-04-09 19:15
**Model:** Opus 4.6
**Prerequisite FDR runs:** FDR-NEW-05 (DEM kitchen), FDR-NEW-15 (tremor controls), FDR-VI-02 (VIS stair)

---

## CMP-03: Seated Wheelchair (MOB) + Dementia (DEM) → Kitchen Meal Preparation

**Compound scenario:** A wheelchair user with moderate dementia prepares a meal. The person has both reduced physical reach/visibility from the seated position AND reduced hazard awareness from cognitive decline.

### Parameter Pair Analysis

| Parameter pair | Classification | Mechanism |
|---|---|---|
| Seated hob visibility (MOB: needs elevated/angled hob or mirror) × simplified controls (DEM: single-knob, auto-shutoff) | **CONVERGENT** | Both populations benefit from induction hob with simplified controls. Seated position actually makes auto-shutoff MORE important because the person may wheel away without turning off. Design solution serves both. |
| Knee clearance under counter (MOB: ≥700mm) × glass-front cabinets (DEM: visible contents) | **INDEPENDENT** | No interaction. Knee clearance is under-counter geometry; glass fronts are upper cabinet. Both specifiable without compromise. |
| Reach envelope (MOB: forward reach ≤1200mm from seated) × open shelving (DEM: visible, ≤2 layers deep) | **CONVERGENT** | Reduced reach + cognitive search difficulty BOTH benefit from single-layer open shelving within seated reach. The compound strengthens the case for both provisions simultaneously. |
| Pull-out shelving (MOB: for access from seated) × simplified storage (DEM: labelled zones) | **CONVERGENT** | Pull-out shelving serves MOB reach; DEM benefits from same mechanism because pull-out makes contents visible without searching. Add pictogram labels to pull-out units. |
| Kitchen-to-living sightline (DEM: supervised cooking from FDR-NEW-05) × wheelchair circulation space (MOB: 1500mm turning) | **CONDITIONAL** | Open-plan kitchen with sightline from living area requires adequate circulation space. If kitchen is too small for wheelchair turning AND supervision sightline, the compound fails. Minimum kitchen area must accommodate both: ≥1500mm turning circle + open plan or pass-through to living area. |

**Result:** 3 CONVERGENT + 1 INDEPENDENT + 1 CONDITIONAL. No antagonistic parameters.

**Synthesis:** MOB+DEM kitchen is a **pure convergence compound with one spatial constraint**. Every provision for either population strengthens the case for the other. The conditional interaction (sightline + turning space) is resolved by adequate kitchen area specification. This compound does NOT require Tier 2 co-design for environmental parameters — a single well-specified kitchen serves both populations. The co-design need is for the supervision/support model, not the physical specification.

**Connection:** CON-0155 (NEW)
**ISW brief:** MOB+DEM kitchen convergence note for Part 6 residential matrix. Minimum kitchen area must accommodate wheelchair turning (1500mm) + living-space sightline. All DEM simplification provisions (glass fronts, open shelving, auto-shutoff) serve MOB equally. Add compound convergence row to Part 3 §3.10 MOB+DEM guidance.

---

## CMP-08: Tremor (NEU) + Visual Impairment (VIS) + Ambulant Mobility (MOB) → Stair Negotiation

**Compound scenario:** A person with essential tremor, low vision, and ambulant mobility impairment negotiates a staircase. This is a triple compound — three concurrent functional constraints during a single high-risk activity.

### Parameter Pair Analysis

| Parameter pair | Classification | Mechanism |
|---|---|---|
| Handrail grip (NEU/tremor: needs larger diameter for tremor-grip stability) × handrail tactile information (VIS: needs readable tactile characters on handrail) | **CONDITIONAL** | Tremor needs 40–45mm diameter for stable grip (wider = more contact area = more stable). VIS needs raised characters on underside of handrail (CAN/ASC 2.2). Both can coexist IF characters are on underside/horizontal section and grip diameter accommodates both. Larger diameter (45mm) actually improves both tremor grip AND provides more surface area for tactile characters. → Resolvable within 40–45mm range. |
| Nosing contrast (VIS: colour-contrasted nosings, LRV ≥50) × step regularity (MOB: all risers equal height ±2mm) | **INDEPENDENT** | Nosing contrast and step regularity address different sensory channels and are independently specifiable. Both are mandatory. |
| Handrail continuity (VIS: continuous handrail for orientation) × handrail as balance support (MOB: continuous for gait stability) | **CONVERGENT** | Both populations require unbroken continuous handrails for different reasons (orientation vs balance). The specification is identical. |
| Lighting level (VIS: ≥300 lux on stair treads) × glare avoidance (VIS/NEU: no direct glare into eyes from stair lighting) | **CONVERGENT** | High illuminance + glare control are complementary, not conflicting. Downward-directed luminaires at 300+ lux with shielding angle ≥30° serves both. |
| Operating force for stair gate/fire door (NEU/tremor: ≤5N, no fine manipulation) × door closer speed (MOB: delayed action ≥3s) | **CONVERGENT** | Low operating force + delayed action both serve all three populations. No conflict. |
| Stair width (MOB: ≥1200mm for handrail + person) × TWSI at top of stair (VIS: tactile warning strip ≥400mm depth) | **INDEPENDENT** | Width and TWSI are independently specifiable. No interaction. |

**Result:** 3 CONVERGENT + 2 INDEPENDENT + 1 CONDITIONAL. No antagonistic parameters.

**Synthesis:** Despite being a triple compound, MOB+NEU/tremor+VIS stair negotiation resolves entirely at Tier 1. No antagonistic parameter pairs exist. The conditional interaction (handrail diameter accommodating both tremor grip and tactile characters) resolves within the existing 40–45mm range. The compound reinforces the case for the existing stair specification package rather than creating new conflicts.

**Clinical note:** The real risk in this triple compound is not parameter conflict — it is cumulative fall probability. Each individual risk factor (tremor-reduced grip × low-vision nosing perception × ambulant balance deficit) independently increases misstep probability. The compound risk is multiplicative, not additive. This means the specification package must be complete — removing ANY single provision (handrail continuity, nosing contrast, TWSI, lighting, step regularity) disproportionately increases fall risk for the compound user. This reinforces Part 11 §11.5.2 value engineering argument: stair accessibility provisions are a system.

**Connection:** CON-0156 (NEW)
**ISW brief:** Add MOB+NEU/tremor+VIS compound convergence note to Part 3 §3.10. Note cumulative fall probability as multiplicative. Cross-ref Part 11 §11.5.2 (VE protection for stair system). Handrail 40–45mm confirmed as valid for triple compound.

---

## Summary

| CMP | Compound | ANTAGONISTIC | CONVERGENT | INDEPENDENT | CONDITIONAL | Resolution |
|---|---|---|---|---|---|---|
| CMP-03 | MOB+DEM kitchen | 0 | 3 | 1 | 1 | Tier 1 — pure convergence with spatial constraint |
| CMP-08 | MOB+NEU+VIS stair | 0 | 3 | 2 | 1 | Tier 1 — all parameters resolve within existing ranges |

Both compounds resolve at Tier 1 without requiring individual co-design for environmental parameters. Both reinforce existing guidebook specifications rather than creating new conflicts.

**CMP-07 status:** Still partially blocked — DEM communication FDR not yet run. The hearing loss (DEAF) + cognitive impairment (DEM) compound requires specific evidence on how DEM affects auditory alarm comprehension and visual alert processing, which has not been systematically researched via FDR. Flag for next session.
