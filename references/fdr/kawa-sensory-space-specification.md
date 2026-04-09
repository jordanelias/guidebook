# Kawa-Informed Sensory Space Specification
**FDR-ENV-05 research output**
**Date:** 2026-04-09 05:30
**Status:** SPECIFICATION DRAFT — requires Opus voice-style pass before Part 4 integration

---

## 1. Problem Statement

PAS 6463:2022 (BSI) specifies a private individual sensory retreat room: a single-occupancy space with individual control over acoustic, lighting, and thermal parameters, designed for a person to withdraw from sensory overwhelm and recover in isolation. This is the most developed sensory space standard internationally and informs A-16 in the guidebook.

The private retreat model encodes three assumptions:
1. The self is autonomous — the person manages their own sensory environment independently.
2. Recovery requires solitude — withdrawal from others is the mechanism of relief.
3. The space serves one person at a time — sizing, controls, and acoustic isolation are single-occupancy.

These assumptions transfer well to Western institutional contexts (UK hospitals, Australian aged care, North American workplaces). They transfer poorly to collectivist cultural contexts where:
- The self is embedded in family and community — individual withdrawal may be experienced as isolation, not relief.
- Recovery is relational — the presence of a trusted companion is calming, not stimulating.
- Space is shared — single-occupancy retreat is neither culturally expected nor architecturally feasible in many dwelling types.

The Kawa model (Iwama 2006) provides the theoretical basis for an alternative specification: the built environment is part of the river channel, and well-being is the flow. Widening the channel (reducing environmental press across a shared space) enables flow for all occupants simultaneously, without requiring any individual to exit the river.

---

## 2. Specification: Shared Calm Space (Kawa-Informed)

### 2.1 Physics Layer (universal — transfers across all cultural contexts)

These parameters derive from the same evidence base as PAS 6463 and A-16. They specify the sensory environment, not the spatial model.

| Parameter | Specification | Evidence basis |
|---|---|---|
| Acoustic | Background noise ≤ NC-25; RT60 ≤ 0.4s; no mechanical noise sources within space; NRC ≥ 0.85 on ceiling and two walls | PAS 6463 §5.3; ndv-aut BPC; A-01, A-02, A-06, A-08 |
| Lighting | Dimmable 50–300 lux; CCT adjustable 2700–4000K; no overhead direct downlighting; indirect/cove only; flicker-free (IEEE 1789); no fluorescent | PAS 6463 §5.4; B-03, B-04, B-06, B-07 |
| Visual complexity | Plain walls; muted palette; no patterned surfaces; maximum 2 colours visible from any seated position; no mirrors; no screens unless user-activated | PAS 6463 §5.5; ndv-aut BPC; C-01 |
| Thermal | User-controllable within 18–22 deg C; no forced-air outlets directed at seated positions; radiant preferred over convective | F-06, F-07; ms-thermal BPC |
| Fragrance | Fragrance-free; materials off-gassed before occupancy; no scented products | F-06; project-standards DEM olfactory rule |
| Floor | Non-resonant; carpet or cork; no hard reflective surface | A-05; ndv-aut BPC |

### 2.2 Spatial Model Layer (culturally variable)

This layer specifies the arrangement, sizing, and social configuration of the space. It is the layer that differs between Western private retreat and collectivist shared calm.

**Model A: Private Retreat (PAS 6463 default)**
- Single occupancy (minimum 8 m2 per A-16).
- Individual environmental controls within arm's reach of a single seated/reclined position.
- Door with privacy lock (user-operated from inside).
- No fixed seating for a second person.
- Appropriate for: Western institutional contexts; workplaces; hospitals; airports; any context where individual autonomy and withdrawal are culturally expected recovery mechanisms.

**Model B: Shared Calm Space (Kawa-informed)**
- Multi-occupancy (minimum 12 m2 for 2–3 persons; 18 m2 for 4–6 persons).
- Flexible seating allowing both solitary and paired/grouped arrangement — not fixed in either configuration.
- Environmental controls accessible to any occupant, not reserved for a single user. Zone-level control rather than individual-point control.
- No privacy lock on door (door may be closed but not locked; unlocked signals availability for others).
- Soft partition or curtain available for visual screening without acoustic or social isolation.
- Companion seating: at least one position adjacent to primary calm seating, sized for a family member, carer, or trusted companion.
- Appropriate for: residential care in collectivist-culture contexts; family-oriented health facilities; community centres; educational settings in non-Western jurisdictions; any context where relational recovery is the cultural norm.

**Model C: Hybrid (recommended for new construction in culturally diverse contexts)**
- Space sized for Model B (minimum 12 m2).
- Partition system (acoustic curtain or movable screen) that converts the space between Model A (private) and Model B (shared) configurations.
- Both individual-point and zone-level controls available.
- Companion seating present but repositionable.
- This is the DAR-optimal specification: it preserves future adaptability for either cultural model.

### 2.3 Tier Assignment

- Physics layer (§2.1): Tier 1 — population-informed, evidence-based, applies universally.
- Spatial model selection (§2.2): Tier 2 — determined by cultural context of occupants and building programme. OT and design team resolve in co-design with user community.
- Model C is the Tier 1 default for new construction where cultural context is unknown or diverse.

### 2.4 Population Applicability

| Population | Primary use | Notes |
|---|---|---|
| NDV/AUT, NDV/SENS | Sensory regulation; meltdown/shutdown recovery | Core population; both models valid depending on individual and culture |
| NDV/MH, NDV/MH-PTSD | Anxiety de-escalation; trauma-triggered withdrawal | Model A may be contraindicated for some PTSD presentations where isolation triggers distress |
| DEM | Reduced-stimulation environment for agitation | Model B preferred — DEM agitation often responds to companion presence, not solitude |
| OFS/ME | Rest during post-exertional malaise | Reclined position required; both models valid |
| PAIN | Pain flare management | Both models; thermal control critical |
| NEU/PCS | Post-concussion sensory overload | Model A initially preferred; transition to B as recovery progresses |

---

## 3. Connection Register Entries Generated

CON-0115: A-16 sensory room specification should reference both Model A and Model B spatial configurations, with Model C as DAR default. Current A-16 text references PAS 6463 only.
CON-0116: Kawa shared calm space requires companion seating specification — not currently in any G-category item. Propose G-XX (companion seating in calm/sensory spaces).
CON-0117: Model B door specification (unlocked, closeable) conflicts with NDV/MH PTSD specification requiring lockable retreat. Conflict resolution: Model C hybrid with user-selectable lock.
