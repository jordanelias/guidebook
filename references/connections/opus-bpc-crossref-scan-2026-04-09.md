# Connection Scout — Opus BPC Cross-Reference Scan (Batch 2)
**Date:** 2026-04-09
**Model:** Opus 4.6
**Method:** Population-pair analysis + mechanism-intersection mapping across 10 BPC files
**BPCs read:** deafblind, intellectual-disability, neurological, ofs, visual-impairment, pain-ofs, dementia, sensory-relief-space, upper-limb-impairment, deaf-spatial-design, mobility, acoustics-speech-intelligibility

---

## New Connections

### CON-0122

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** deaf-spatial-design, mobility-built-environment
**Target item(s):** A-02 (corridor width)
**Target population(s):** DEAF, MOB
**Evidence tier:** Co-1 (DeafSpace 2010) + Tier 3 (IDeA Center / Steinfeld 2010)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** DEAF corridor width (2440mm for signing conversation, DeafSpace 2010) subsumes MOB corridor width (1800mm turning, IDeA Center). In any building serving DEAF populations, the DEAF signing-width specification automatically satisfies the MOB turning-space requirement. This is a *subsumption connection* — the higher specification contains the lower. No conflict exists, but the cost and space implication is significant and undocumented: a designer who specifies for DEAF first (2440mm) does not need a separate MOB corridor width specification. Conversely, a designer who specifies for MOB only (1800mm) creates inadequate signing space for DEAF users.

The secondary implication: A-02 currently has 18 connection edges (highest in the network) but none documents the DEAF signing-width as the governing specification for mixed DEAF+MOB buildings. The corridor width is silently determined by whichever population has the larger requirement — this subsumption logic should be made explicit.

**Evidence basis:** deaf-spatial-design BPC: 2440mm (8 ft) primary corridors for signing. mobility-built-environment BPC: 1800mm turning for power wheelchair (IDeA Center; Habinteg/RCOTSS). 2440mm > 1800mm — DEAF governs.

**Action required:** Add subsumption note to A-02: "Where DEAF populations are primary users, corridor width is governed by signing-space requirement (2440mm), which automatically satisfies MOB turning requirement (1800mm). Where MOB only, 1800mm governs." This prevents redundant specification and makes the governing logic transparent.

**Disposition notes:** — First "subsumption connection" in the register. Consider systematising: for each item, identify which population specification governs (is widest/most restrictive).

---

### CON-0123

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** intellectual-disability-built-environment-design, dementia-built-environment
**Target item(s):** D-02, D-06, D-08, C-04
**Target population(s):** IntD, DEM
**Evidence tier:** Tier 3-4 (IntD: AU NDIS SDA) + Tier 3-5 (DEM: Marquardt 2011, DSDC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** IntD and DEM wayfinding specifications converge more completely than any other population pair in the guidebook. CON-0001 identified the circulation geometry overlap (loop/linear, no dead-ends). The full convergence extends to the entire wayfinding system:

| Parameter | IntD specification | DEM specification | Match |
|---|---|---|---|
| Circulation geometry | One-way legible, loop/radial, no dead-ends | Loop/linear, minimal directional changes | IDENTICAL |
| Signage type | Pictogram + single-word | Pictographic + colour-coded | OVERLAPPING |
| Colour coding | Colour-zone per functional area | Colour-coded toilet doors, landmarks | COMPLEMENTARY |
| Ceiling differentiation | Zone-differentiated ceiling heights | Not specified (but 3D landmarks at decision points) | ADDITIVE |
| Floor treatment | Tactile floor material differentiation per zone | Plain, no high-gloss, no dark mats | COMPATIBLE |
| Landmark objects | Not specified | Distinctive 3D landmark at every decision point | ADDITIVE |

The IntD "zone-differentiated ceiling heights" specification is unique — it does not appear in any other population's BPC. This should be evaluated for DEM applicability (spatial differentiation aids cognitive mapping). Conversely, DEM's "3D landmark objects at decision points" is absent from IntD but functionally relevant (reduces cognitive load at route choices).

**Evidence basis:** IntD BPC: all findings AU (NDIS SDA) and CA (CSA B651) derived, Tier 4-5. DEM BPC: Marquardt 2011 (Tier 3), DSDC (Tier 5), 10+ jurisdictions. IntD evidence base is thinner but the convergence pattern suggests DEM evidence can be applied by analogy to IntD.

**Action required:** (1) Cross-reference IntD and DEM as co-populations for ALL wayfinding items (D-02, D-06, D-08). (2) Evaluate IntD ceiling-height specification for DEM: does zone-differentiated ceiling height aid DEM spatial mapping? If yes, add to DEM wayfinding specification. (3) Add 3D landmark objects (DEM) to IntD wayfinding specification. (4) Note in Part 2: IntD and DEM wayfinding evidence bases are independent but convergent — provisions validated for DEM can be applied to IntD with MODERATE confidence.

**Disposition notes:** — Strongest population-pair convergence in the evidence base. Implications for Part 3 co-occurrence framework: IntD+DEM in shared spaces (aged care with ID residents) requires no conflict resolution — provisions are additive.

---

### CON-0124

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** upper-limb-impairment-built-environment, deafblind-built-environment-design
**Target item(s):** G-03, G-04
**Target population(s):** MOB/UPL, DBL
**Evidence tier:** Tier 3 (Levine 2025, Kennedy 2015) + Tier 2 (DbI)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** UPL BPC documents that optimal grab bar grasp location varies with body height (r=0.67, Levine 2025) — fixed placement cannot serve all users. CON-0120 (this session) proposes grab bars as haptic spatial landmarks for DBL. These two findings interact: if grab bar height is variable (UPL Tier 2 provision), then DBL users cannot rely on consistent haptic landmarks for spatial orientation.

Resolution requires distinguishing two grab bar functions in the same room:
1. **Navigation grab bars** (horizontal, at fixed consistent height) — serve DBL haptic wayfinding. Height: 900mm AFF (standard waist height for standing haptic scan). Fixed, never adjusted.
2. **Transfer grab bars** (vertical or L-shaped, height per OT assessment) — serve UPL/MOB postural support. Position determined by individual's functional capacity.

Currently G-03/G-04 treat all grab bars as a single specification category. The UPL evidence (variable placement needed) and DBL evidence (consistent placement needed) create a design tension resolvable only by distinguishing function.

**Evidence basis:** UPL BPC: Levine 2025 (grasp location varies with height, r=0.67). Kennedy 2015: vertical bars produce smallest COP deviation. DBL BPC: consistent tactile layout is highest priority (DbI). CON-0120: grab bar as haptic landmark.

**Action required:** Split G-03/G-04 specification into: (a) navigation-function grab bars (fixed, consistent, DBL/DEM-serving) and (b) transfer-function grab bars (adjustable/OT-assessed, UPL/MOB-serving). Both coexist in the same bathroom. The navigation bar provides the tactile route; the transfer bar provides the postural support.

**Disposition notes:** — Resolves a real design tension between two valid requirements. The distinction (navigation vs. transfer function) is novel — not in any existing standard.

---

### CON-0125

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** neurological-built-environment, visual-impairment-built-environment
**Target item(s):** D-02, D-06, D-08
**Target population(s):** NEU, VIS
**Evidence tier:** Tier 1 (NEU Opus synthesis) + Tier 4-6 (VIS: ISO 23599, BS 8300)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** NEU BPC Opus synthesis establishes bilateral redundancy as the Tier 1 provision for hemispatial neglect: environmental cues on BOTH sides of corridors, because unilateral neglect makes one side invisible. VIS BPC specifies signage at eye level on both sides of corridors for legibility from either approach direction. Both populations independently require bilateral environmental cues — NEU for neglect compensation, VIS for approach-direction legibility.

This convergence is currently undocumented. The shared specification: all wayfinding cues, environmental landmarks, signage, contrast bands, and tactile indicators shall be bilateral (both corridor walls, both sides of doorways, both stair stringers). Unilateral placement is a specification error for both populations.

Additionally, NEU Opus synthesis notes: "wayfinding provisions (D-02, D-04, D-08) should cross-reference NEU explicitly, not only DEM." This cross-reference has not been made.

**Evidence basis:** NEU BPC Opus synthesis: bilateral redundancy is Tier 1 for unilateral neglect. VIS BPC: signage on both sides is standard practice (BS 8300, ISO 21542). The convergence is mechanistically different (NEU = compensating for perceptual deletion; VIS = compensating for approach uncertainty) but specificationally identical.

**Action required:** (1) Add NEU as co-population for D-02, D-06, D-08. (2) Add "bilateral placement" as explicit specification requirement for all wayfinding cues — currently implicit in VIS practice but not codified. (3) Note: bilateral placement serves NEU (hemispatial neglect), VIS (approach-direction coverage), and DEM (reinforcement) — Tier 0 candidate.

**Disposition notes:** — NEU is under-represented in wayfinding items despite NEU Opus synthesis explicitly flagging this gap.

---

### CON-0126

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** true
**Source BPC slug(s):** ofs-built-environment, visual-impairment-built-environment
**Target item(s):** I-03
**Target population(s):** OFS, VIS
**Evidence tier:** Tier 5 (BS 8300 / VisitEngland) + Tier 4 (ISO 23599)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** OFS BPC specifies rest seating every 25-30m on primary routes (tightened from BS 8300's 50m for MOB). VIS BPC specifies continuous TWSI on primary routes with attention indicators at decision points (ISO 23599). These specifications occupy the same physical space — the primary circulation route — but are specified independently.

The unmade connection: if rest seating is placed at 25-30m intervals on primary routes, each seat becomes a cane-detectable physical landmark for VIS users. Seating benches are among the most reliably detectable objects by cane scan (consistent height, solid base, predictable profile). By coordinating seating placement with TWSI attention indicators, each rest point doubles as a TWSI-anchored wayfinding landmark.

The practical implication: rest seating (I-03) should be placed AT TWSI attention indicator positions — not offset from them. The seating location becomes the wayfinding anchor. Currently, I-03 and TWSI placement are specified by different consultants (interior design vs. wayfinding consultant) with no coordination requirement.

**Evidence basis:** OFS BPC: 25-30m rest intervals. VIS BPC: ISO 23599 attention indicators at decision points + facilities. The coordination is logical inference — no study validates the dual function, but the mechanism (cane-detectable furniture as landmark) is established in VIS wayfinding literature.

**Action required:** Add coordination note to I-03: "Rest seating to be located at TWSI attention indicator positions on primary circulation routes. Seating serves dual function: energy conservation (OFS/PAIN/MOB) and cane-detectable wayfinding landmark (VIS/DBL)." Cross-reference I-03 ↔ C-04 (TWSI items).

**Disposition notes:** — MODERATE because dual-function is inferred, not studied. But the coordination cost is zero.

---

### CON-0127

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** deaf-spatial-design, sensory-processing-model-design-application, dementia-built-environment
**Target item(s):** C-04 (wall colour), B-06 (lighting CCT)
**Target population(s):** DEAF, NDV, DEM
**Evidence tier:** Co-1 (DeafSpace 2010) + Tier 3 (Dunn model) + Tier 5 (DSDC)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** Three-way interaction on wall colour/finish:

- **DEAF:** Muted green/blue walls for sign language legibility — skin tone must contrast against background (DeafSpace 2010). Single, consistent colour per space.
- **NDV:** Reduced visual noise/complexity — minimal pattern, calm palette, low visual stimulation (PAS 6463, Dunn model). Supports muted single-colour approach.
- **DEM:** Colour-coded zones for spatial wayfinding — different colours per functional area (DEM BPC, DSDC). Requires colour VARIATION between zones.

DEAF and NDV are synergistic: both want muted, single-colour walls. DEM conflicts with both: DEM wants colour differentiation between zones, which increases the visual complexity that NDV aims to reduce and may place non-optimal colours (warm reds, yellows) in signing spaces where DEAF needs neutral tones.

Resolution: colour-zone wayfinding for DEM uses door colour and floor colour banding — NOT wall colour. Walls remain muted neutral (serving DEAF + NDV). Zone identity carried by floor and door (consistent with CON-0116 door-as-wayfinding-element). This preserves all three populations' requirements: DEAF signing legibility, NDV visual calm, DEM zone differentiation.

**Evidence basis:** deaf-spatial-design BPC: muted greens/blues, no busy patterns, skin tone contrast. sensory-processing-model BPC: visual noise reduction. dementia-built-environment BPC: colour-coded wayfinding. No source addresses the three-way interaction.

**Action required:** (1) Part 5 conflict note: DEAF/NDV/DEM wall colour three-way interaction. Resolution: walls muted neutral; zone coding via floor and door colour only. (2) C-04 specification: separate wall colour (muted neutral for DEAF/NDV) from zone-coding colour (floor/door for DEM). (3) This resolution is ○ (expert synthesis) — no study validates the floor/door-only colour coding approach.

**Disposition notes:** — First three-way conflict identified by this scan. Resolution is architecturally elegant (preserves all three requirements) but unvalidated.

---

### CON-0128

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** deafblind-built-environment-design, mobility-built-environment
**Target item(s):** G-04, Part 6 residential bathroom matrices
**Target population(s):** DBL, MOB
**Evidence tier:** Tier 2 (DbI) + Tier 3 (IDeA Center)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** MOB BPC specifies 1800mm turning circle in bathrooms. DBL BPC specifies intervenor clear floor space ≥900×1500mm at service counters (GAP-NEW-01). In a residential bathroom, a DBL user with an intervenor needs BOTH MOB turning space AND intervenor standing space simultaneously — the intervenor stands alongside the DBL user during transfers and orientation.

The spatial requirement is additive, not overlapping: 1800mm turning circle + 900×1500mm intervenor zone = bathroom footprint significantly larger than MOB-only specification. For bathrooms in DBL-designated residential settings, the MOB turning circle alone is insufficient.

No existing standard specifies the combined spatial requirement. The DBL BPC notes GAP-NEW-01 (intervenor space at service counters) but does not extend this to residential bathrooms — arguably the highest-risk environment for DBL users.

**Evidence basis:** DBL BPC: intervenor clear floor space ≥900×1500mm (DbI guidelines). MOB BPC: 1800mm turning (IDeA Center). Additive spatial requirement is geometric — no study needed to confirm that two bodies occupy more space than one.

**Action required:** Add DBL intervenor space provision to Part 6 residential bathroom matrix for DBL-designated units. Minimum bathroom footprint: MOB turning circle (1800mm) + intervenor standing zone (900×1500mm) adjacent to toilet and shower transfer positions. This is a DAR provision for residential settings: conduit and structural reinforcement for future ceiling hoist (I-04) should assume combined space requirement.

**Disposition notes:** — Extends GAP-NEW-01 from public service counters to residential bathrooms.

---

### CON-0129

**Status:** PENDING
**Confidence:** MODERATE
**Opus-reviewed:** true
**Source BPC slug(s):** pain-ofs-built-environment-design, intellectual-disability-built-environment-design
**Target item(s):** G-08 (bedroom storage), kitchen items
**Target population(s):** PAIN, IntD
**Evidence tier:** Tier 5 (PAIN) + Tier 4 (IntD: AU NDIS SDA)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** PAIN BPC specifies storage at 750-1050mm throughout — the zone between hip and shoulder that avoids bending or overhead reaching. IntD BPC does not specify storage height, but IntD users benefit from predictable, visible, consistent storage heights — not because of physical limitation but because finding items in unpredictable locations increases cognitive load and triggers frustration/distress.

The PAIN specification (consistent 750-1050mm band) secondarily serves IntD by creating a predictable storage zone. Items are always at the same height range; visual scanning is confined to one band; the environment communicates where things are through consistency.

Additionally, DEM shares this mechanism: DEM users who cannot remember where items are stored need visual accessibility at eye level. The PAIN height range (750-1050mm) is slightly below standing eye level for an average adult — but ideal for a seated user (DEM in care settings frequently seated in chairs).

**Evidence basis:** PAIN/OFS BPC: storage 750-1050mm (energy conservation). IntD BPC: no storage guidance but "consistent predictable layout" is the highest-priority principle. DEM BPC: visual accessibility for items in daily use.

**Action required:** Add IntD and DEM as co-populations for storage height specification (750-1050mm). Mechanism for IntD: cognitive load reduction from predictable storage. Mechanism for DEM: visual accessibility at seated eye level. No specification change — population coding extension only.

**Disposition notes:** — Low-cost connection (population tag addition). The PAIN→IntD→DEM chain demonstrates that physical-accommodation specifications often incidentally serve cognitive-accommodation populations.

---

### CON-0130

**Status:** PENDING
**Confidence:** HIGH
**Opus-reviewed:** true
**Source BPC slug(s):** dementia-built-environment, intellectual-disability-built-environment-design, ofs-built-environment
**Target item(s):** D-02 (wayfinding), Part 7 NR-HLT (healthcare matrices)
**Target population(s):** DEM, IntD, OFS
**Evidence tier:** Tier 3 (Marquardt 2011) + Tier 4 (IntD: NDIS SDA) + Co-1 (OFS)
**Filed:** 2026-04-09
**Applied:** —

**Connection:** DEM BPC specifies toilet visible from primary occupied space (CON-0018, Marquardt 2011 — reduces incontinence). IntD BPC specifies reception/assistance point within sight of entrance (CSA B651 §4.7). OFS BPC specifies rest seating within 25-30m of any point.

All three specifications use the same spatial mechanism: **critical facility sightline** — a person in a primary occupation zone can visually locate the critical facility without navigation or search. DEM: toilet. IntD: assistance point. OFS: nearest rest provision.

This should be generalised as a Tier 0 spatial planning principle: **critical facilities shall be visible from primary occupation zones.** Facilities qualifying as "critical": toilet/bathroom, reception/assistance, exit, rest provision, environmental refuge (A-16). The sightline requirement eliminates the search/navigation burden that DEM, IntD, NEU, and OFS populations all experience from different clinical causes.

CON-0018 partially captures this for DEM+toilet. CON-0068 extends to NEU/NDV/OFS. This connection adds IntD reception sightline and generalises the principle beyond toilet to all critical facilities.

**Evidence basis:** DEM BPC: Marquardt 2011 (toilet visibility strongest environmental factor). IntD BPC: CSA B651 §4.7 (reception within sight of entrance). OFS BPC: rest provision intervals. CON-0018: toilet sightline for DEM. CON-0068: toilet visibility for DEM/NEU/NDV/OFS.

**Action required:** Elevate "critical facility sightline" to Tier 0 spatial planning principle in Part 3 §3.x or Part 1 §1.4: all primary occupation zones shall provide unobstructed sightline to at least one of: toilet door, reception/assistance, building exit, rest seating. In healthcare settings (Part 7 NR-HLT): nurse station visible from all patient positions.

**Disposition notes:** — Generalises CON-0018/CON-0068 from toilet-specific to facility-class principle. Tier 0 candidate.
