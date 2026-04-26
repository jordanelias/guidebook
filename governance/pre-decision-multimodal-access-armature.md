# Pre-Decision: Multimodal Access Armature — Website Navigation Architecture

**Status:** PRE-DECISION (captures design intent for A7+ formalization)
**Date:** 2026-04-26 20:24
**Decision scope:** Website query architecture + guidebook data model implications

---

## Problem

The guidebook contains a single linear structure. Different users need different slices of it, filtered by who they are, who they're designing for, and what they're looking at. The website must provide an armature — a structured query interface — that lets users arrive at the right content from multiple entry points.

The current population code taxonomy (MOB, VIS, DEAF, NEU, etc.) is too coarse to power this. Sub-population distinctions that change specifications are not captured. Amputees/limb difference are not represented at all.

---

## Three-Dimensional Armature

### Dimension 1 — Role (who are you)

Each role prioritizes different aspects of the same underlying data.

| Role | Prioritizes |
|---|---|
| Designer | Specifications, conflict notes, detail drawings, Tier 0/1 values |
| OT | Ranges, Tier 2 resolution guidance, functional profiles, co-occurrence |
| Policymaker | Compliance mapping, jurisdiction comparisons, economic case |
| Person with lived experience | Plain language, what to ask for, what good looks like, rights |

Same data engine, different presentation layer and prioritization.

### Dimension 2 — Person Profile (who is it for)

Two entry modes, one specification engine:

**Mode A — Diagnosis entry:** User selects a condition (cerebral palsy, MS, bilateral below-knee amputation, retinitis pigmentosa, etc.). System maps to a default impairment profile. User can adjust.

**Mode B — Impairment axis entry:** User builds a profile directly from functional axes. No diagnosis needed or assumed.

Both modes arrive at the same impairment profile — a set of axis values that drive specification selection.

#### Impairment Axes (draft — drives specification selection)

These are the functional dimensions where a change in capacity changes what the built environment must provide:

| Axis | Spectrum |
|---|---|
| Ambulatory capacity | Full > aided (cane/crutch) > walker/rollator > manual wheelchair > power wheelchair > bed-based |
| Upper limb function | Full > reduced grip > reduced reach > reduced grip + reach > minimal/absent |
| Visual capacity | Full > low vision > no functional vision |
| Light tolerance | Normal > photophobic |
| Hearing capacity | Full > hard of hearing > no functional hearing |
| Acoustic processing needs | None > hearing aid/loop dependent > CI dependent |
| Cognitive processing | Intact > reduced speed/executive/memory > severe |
| Sensory regulation | Typical > hyper-responsive > hypo-responsive > mixed |
| Pain/fatigue envelope | Unrestricted > limited (pacing required) > severely limited |
| Thermoregulation | Intact > heat-sensitive > cold-sensitive > both |
| Postural control | Full > reduced (seated balance) > minimal |
| Transfer capacity | Independent > assisted > dependent |

#### Diagnosis-to-Profile Mapping (examples)

| Diagnosis | Default impairment profile (adjustable) |
|---|---|
| Cerebral palsy | Ambulatory [variable], upper limb [variable], postural control [reduced], sensory regulation [may be affected], cognition [typically intact] |
| Bilateral below-knee amputee (with prosthetics) | Ambulatory [aided], upper limb [full], transfer [independent] |
| Bilateral below-knee amputee (without prosthetics) | Ambulatory [wheelchair], upper limb [full], transfer [assisted] |
| Retinitis pigmentosa | Visual capacity [low vision], all others [full unless co-occurring] |
| MS (moderate) | Ambulatory [variable], fatigue [limited], thermoregulation [heat-sensitive], cognition [may be reduced] |
| Advanced Parkinson's | Ambulatory [walker to wheelchair], upper limb [reduced grip], postural control [reduced], cognition [may be reduced] |

This model solves the amputee/limb difference gap without requiring a dedicated population code. "Amputee" is a diagnosis entry point that maps to the relevant impairment axes. The impairment profile drives specifications.

#### Compound Profiles

When multiple axes are affected, the system surfaces conflict notes where specifications for one axis contradict specifications for another. Compound functioning principle applies: co-occurring impairments are supra-additive, not simply additive.

### Dimension 3 — Scope (what are you looking at)

| Filter | Examples |
|---|---|
| Topic | Wayfinding, lighting, acoustics, thermal, flooring |
| Room type | Bathroom, bedroom, kitchen, corridor, entrance |
| Design stage | Brief, schematic, DD, construction, RFO |
| Item category | A (circulation) through K (technology) |

---

## Relationship to Guidebook Text

The guidebook prose continues to use population codes for readability and chapter organization (Part 2). The impairment axis model lives in the data layer and is introduced conceptually in Part 3 as the specification resolution mechanism.

Population codes = human-legible entry points (how people talk about disability).
Impairment axes = specification-driving variables (how built environment parameters actually change).

The website makes both modes interactive. The guidebook makes both modes intellectually legible.

---

## Term

"Multimodal access" — describes the two-entry-point architecture (diagnosis mode + impairment mode). Does not privilege either mode.

---

## Implications for Stage A

| Phase | Impact |
|---|---|
| A7 (Population taxonomy) | Must formalize: (1) impairment axis enum + spectrum values, (2) diagnosis-to-profile mapping table, (3) population code to impairment axis relationship |
| A3 (Conceptual model) | Entity model must support both entry modes querying the same specification data |
| A8 (Jurisdiction) | Role dimension affects how jurisdiction data is presented (designer: code values; policymaker: compliance gaps) |
| Website build | Three-dimensional query interface; specification engine returns tailored views |

---

## Gaps Identified

- **Amputee / limb difference:** Not represented in current taxonomy. Resolved by impairment axis model — diagnosis entry maps to ambulatory + upper limb axes. No dedicated population code needed, but "amputee" must be a recognized diagnosis entry point with validated default profiles.
- **Sub-population granularity:** VIS/BLIND vs VIS/LOW, MOB/PWC vs MOB/MWC vs MOB/WALK — these distinctions exist on the impairment axis spectrum. Population sub-codes may still be useful as shorthand in prose but are secondary to the axis model.
- **Missing limb as distinct from reduced limb function:** Upper limb absence vs. reduced grip are different points on the upper limb function axis. The axis captures this; a binary "present/absent" flag may be needed as a modifier.

---

## Decision Required at A7

Formalize impairment axes, spectrum values, and diagnosis mapping as Pydantic schemas with validation. This pre-decision document captures intent only.
