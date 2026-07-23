# Reasoning: category-e-circulation (cross-slug synthesis run)

<!--
Cross-slug synthesis for the whole Category E circulation family, plus the two
wayfinding slugs and the floor-vibration slug that feed E items. This is a
best_practice_synthesis run (Opus-class authorship, PI rule #2 / DR-2026-06-10
routing satisfied). It re-derives the specification set from evidence, tests
each specification within Category E against the others, and stress-tests the
whole set against every other category (A–K) per owner directive 2026-07-23.
Structure follows references/bpc-reasoning/_template.md so it validates against
scripts/validate_reasoning.py.
-->

**BPC file:** references/bpc/entrances-and-circulation/accessible-circulation-geometry.md; references/bpc/entrances-and-circulation/stair-ramp-threshold-biomechanics-accessibility.md; references/bpc/entrances-and-circulation/threshold-and-level-access.md; references/bpc/entrances-and-circulation/threshold-door-hardware.md; references/bpc/entrances-and-circulation/residential-entry-and-threshold.md; references/bpc/entrances-and-circulation/floor-vibration-wheelchair-disability.md; references/bpc/wayfinding-and-signage/detectable-gradient-protocol-sensory-zones.md; references/bpc/wayfinding-and-signage/cognitive-wayfinding-design.md
**BPC population:** Curated FROM axes (work-from-axes, RULE 2026-07-22): AX-WHM (wheeled movement & transfer), AX-AMB (ambulant movement), AX-BAL (balance/postural), AX-STA (sustained-exertion), AX-REA (reach & manipulation), AX-VIS-N / AX-VIS-L (non-visual / low-vision information), AX-COG-O (orientation), AX-AUD (auditory access & alerting), AX-PAI (pain-load). Population vectors touched: MOB (incl. SCI, UPL, ambulant share), OFS/POTS, PAIN, VIS, DBL, DEAF, DEM, NDV/AUT, NEU, ALL.
**Generated:** 2026-07-23 by session_2026-07-23-category-e-circulation-synthesis
**Status:** DRAFT
**Opus session ref:** session_2026-07-23-category-e-circulation-synthesis

---

## §0. Scope, doctrine posture, and headline caveats

**What this run does.** It reads the migrated circulation corpus (146 verified
`source_slug_links` across 8 slugs; the sources *are* migrated into
`evidence_sources`, contrary to an early worry — what is missing is the
per-cell synthesis output), interrogates what each source actually governs,
names the throughlines, re-derives a graded specification set, and runs two
robustness passes: (1) within Category E, spec-against-spec; (2) against all
other categories A–K. It closes with an adversarial pass.

**What best practice means here (read before every claim below).** Best
practice is **aspirational and evidence-anchored**, graded by the
weighted-strength anchor model (`governance/tier-system.md` §8; DR-2026-07-20;
Option A DR-2026-07-21):

- **● Full** — T1, Co-1, T2, Co-2, T3-clinical. Anchors outright.
- **◐ Partial** — T4, T5. Anchors as *current standards practice*, flagged "standards basis, not primary evidence."
- **○ Weak** — T3-grey, T6 (code-floor), expert-consensus / thin base. Anchors only a floor/convergence claim, flagged "best available given current regulation/practice, NOT academically adjudicated."

**Code consensus is NOT best practice.** A claim of the form "BS 8300, DIN
18040-1, Part M and AS 1428.1 all specify X" is a *convergence* claim across
the regulatory stratum (T4–T6); the jurisdictions can be wrong together
(`tier-system.md` §3; `project-standards.md:20`). A cell whose **entire** basis
is T4–T6 takes **○** even where T4/T5 sources are present, renders as
"best practice as currently known" *always flagged code-derived*, and its state
stays **`provisional`, never `stated`** (`evidence-architecture.md:105`;
`tier-system.md:101`). The ◐ band applies to individual T4/T5 *citations* inside
an otherwise ●-anchored cell, not to a code-only determination.

**Headline caveat 1 — the numbers are not yet value-level verified.**
`source_value_extractions` holds **zero** rows for any circulation slug (only
`room-acoustic-performance` has extractions). The marker rule
(`project-standards.md:26`) requires that for a *quantitative* specification the
`●` confirmed marker "additionally requires value-level support, not only
direction." Therefore, throughout this document, **the evidence anchors the
DIRECTION of every parameter; the specific magnitude is rendered
value-level-PENDING** unless a source states the number directly. Promotion of
any parameter to a `stated` cell requires the value-level extraction pass named
in §A.5 and is deliberately *not* performed in this run.

**Headline caveat 2 — this run proposes; it does not execute structural moves.**
Item renames/splits/relinks and the population of `evidence_cell_state` are
owner-gated structural / data acts (CLAUDE.md §5, §9; caller-sweep rule). This
document is the synthesis and the proposal. Operationalization (migrations,
cell writes, item re-linking) is the owner-gated follow-on in §G.

**Headline caveat 3 — no fabrication.** Where evidence is absent, this run says
so (rest-seating interval has no building code in any jurisdiction; TWSI and
slip-resistance evidence is not linked to the E items that name them). No number
is invented to fill a gap.

---

## §0b. Throughlines across the circulation corpus

Six throughlines organize everything below.

1. **Evidence-rich, cell-poor.** The circulation family holds some of the
   strongest primary evidence in the whole guidebook — Steinfeld's *Anthropometry
   of Wheeled Mobility* (T1, REF-00059/60), the stair/ramp/threshold T3-clinical
   biomechanics cluster (Al Lawati, Pavol, Kim, Rouvier T2, Templer T4), Brandt's
   door-force study (T3, REF-00204), Roxburgh's ME/CFS time-diary work (T3,
   REF-00426) — yet only **3** of ~70 possible Category-E cells are populated
   (`E-06/MOB` provisional, `E-08/DEAF` stated, `E-12/MOB` stated). The synthesis
   exists as BPC prose; it has not been turned into graded cells.

2. **The regulatory stratum is over-catalogued and mis-read as best practice.**
   The corpus is dominated by T4–T6 code citations (the great majority of the
   146 links). Every circulation BPC is currently banner-marked
   **RETRACTED PENDING REVERIFICATION** (pre-2026-05-23 rehabilitation cohort),
   and several commit the **convergence-as-best-practice** error the doctrine
   names explicitly: the ACG BPC calls 1800 mm two-way "preferred"; the door BPC
   calls ≤20 N "best practice" — both are code-convergence values, not the
   evidence anchor. This run replaces those with the evidence anchors and demotes
   the code values to their honest band.

3. **Geometry descends from the swept ENVELOPE, not a turning RADIUS.** Corridor
   width, lift-car size, entrance landing, and door manoeuvring clearance are all
   the same problem: the 2-D area a wheeled-mobility device *sweeps*, across the
   real device range (manual WC → power WC → scooter; footplate/anti-tip castor
   geometry; occupied anthropometry), worst-case device governing, median at
   Population Mode. A single "1500 mm turning circle" code floor is a radius
   proxy that Steinfeld's AWM and Ringaert 2001 (T3, *"Determination of New
   Dimensions for Universal Design Codes"*) show to be systematically too small.
   Every geometry spec below is tested on the envelope, not the circle.

4. **Contested-direction parameters recur and must anchor nothing universally.**
   Flush thresholds aid wheeled mobility but remove the tactile cue cane users
   rely on; tactile walking-surface indicators aid VIS but are a
   trip/roll/pain precipitant for some ambulant, wheeled, balance and pain
   users; DeafSpace open sightlines conflict with NDV/MH compartmentalisation.
   Per `evidence-architecture.md:106`, where the accessibility direction is
   population-contested there is **no** most-accommodating single value: anchor
   nothing, record the conflict, render the spread per population. This run flags
   each such parameter rather than papering it over.

5. **The item scaffold predates the evidence and is unreliable.** Item→slug
   links point at the wrong BPCs (E-07 "Slip Resistance" → a slug with no slip
   evidence; E-09 "TWSI/ISO 23599" → a slug with no tactile-paving evidence);
   E-13 duplicates D-02/D-07/D-08/D-10 (shared slug); E-15 "Changing Places" is a
   bathroom item mis-filed in E; E-14 is vacant. Category E must be re-derived
   from axes, not patched (§G).

6. **Value-level extraction is the missing floor under everything.** Because
   `source_value_extractions` is empty for circulation, no quantitative value can
   currently earn a `●`. This is the concrete, mechanical next step and it gates
   every `stated` promotion.

---

## §0c. The corridor is not a width — it is an experiential system worked in all directions, iteratively

The corpus (and the doctrine's own worked example) fixate on corridor *width*.
But a corridor is a **space-time experience** a disabled person moves through,
and it modulates that experience along every axis. Best practice must be
derived by iterating across **all** of these directions and refining each
against the others (that iterative cross-refinement is the robustness method
itself), not by fixing width alone:

- **Lateral (width)** — the swept-envelope + signed-conversation problem (§B.3).
- **Longitudinal (length / run)** — an uninterrupted corridor *length* is an
  **exertion cliff** for AX-STA (ME/CFS, POTS) and AX-AMB fatigue (MS) exactly as
  a gradient is: distance-without-rest is itself a barrier. The corpus already
  holds the anchor — **rest landing every 10 m run (or 750 mm rise)** (RCOT /
  Scottish TH, Co-2/T5 ◐) — but it is buried in the residential-entry ramp spec.
  **Corridor length is a first-class parameter (§B.10), not a footnote to width.**
- **Vertical (grade change within the run)** — ramps, landings, and level
  changes *inside* a circulation route (E-03/E-12), with landings sized to the
  turning envelope and placed at rest intervals; a corridor that changes level is
  a ramp and inherits §B.1.
- **Rest and refuge** — seating/alcoves recessed from the passing envelope
  (E-10, §B.4); passing places on narrow secondary runs.
- **Longitudinal support and information — the handrail** — the one *continuous*
  element that runs the whole length and can carry **balance support (AX-BAL)**
  *and* **tactile wayfinding information (AX-VIS-N)** simultaneously (§B.9). This
  is where vestibular and sight needs enter a geometry the corpus frames almost
  entirely around wheels.
- **Sequence / sensory modulation** — the corridor's rhythm of decision points,
  sightlines, luminance/acoustic zoning, and landmark placement modulates
  orientation load (AX-COG-O) and arousal (AX-SPR/AX-ARO): this is where
  Category A/B/C/D land *on* the corridor surface (detectable-gradient protocol;
  cognitive-wayfinding).
- **Edge and adjacency — what opens onto the corridor** — door placement (swing
  into vs out of circulation; latch-side approach clearance), **corners** (blind
  vs curved/mirrored, and the swept turn at every corner), **closets/storage**,
  and **kitchens/rooms** opening off the route. A corridor's usable width is set
  by what projects into it and where doors demand approach clearance; corners are
  where the turning envelope (not radius) governs. These pull in I-02 (kitchen
  one-handed), G-05 (work surfaces), D-07 (no blind corners), and every door spec.

**"Work all directions iteratively."** Each direction constrains the others:
a rest alcove (longitudinal) must not intrude on the swept envelope (lateral);
a door opening off the run (edge) consumes width and needs latch-side clearance
that must not collide with the passing envelope or a corner turn; a handrail
(support/info) occupies wall zone that trades against clear width. The
derivation is a loop, refined until all directions are mutually satisfied — not a
single number.

## §0d. Three modes × the top-down/bottom-up dichotomy — how a circulation spec is even generated

Every circulation specification must declare **which design mode** it speaks in
and acknowledge **which generative direction** produced it. These are two
different doctrinal frames and Category E needs both.

**The three modes** (`governance/evidence-architecture.md` §3;
`project-standards.md:32`):

- **Universal Mode** — population-agnostic, *fixed* values; cites the code floor;
  voice "the code requires." E.g. a minimum clear door width applied everywhere.
- **Population Mode** — *ranges*, **median as default**; cites the *evidence*.
  E.g. corridor width derived from the wheeled-mobility device range, median at
  design stage. **Never write a range without saying which end applies at which
  mode.**
- **Person Mode** — OT co-design; the population informs but does **not bound**
  the individual; authority sits in the assessment + the person. E.g. the exact
  rest interval, handrail height, or car size for a specific user's device and
  endurance.

Applied to rest-seat height: **450–500 mm range** (Population Mode); **median for
generic design; ≥480 mm end at the POTS-relevant Person case; resolved in
co-design at Person Mode** — this is the mandated "which end at which mode"
statement (§B.4).

**The top-down ↔ bottom-up dichotomy.** Category E is precisely where the two
generative directions meet and must be reconciled:

- **Top-down Universal Design** starts from the built form and applies
  general accessible-design principles (the codes, the standards, "an accessible
  corridor is ≥X mm"). It is efficient and comprehensive but tends to encode the
  *regulatory floor* and the *typical* wheeled user — and it is exactly the mode
  that produces convergence-as-best-practice error.
- **Bottom-up Functional-Deficit design (FDR/FDA)** starts from a specific
  functional demand (an ICF d-code + a device/impairment) and asks what the
  environment must do — the worst-case-user, scenario-driven derivation (the
  `functional-deficit-researcher`/`-auditor` skills; the "Bottom-up findings"
  passes already in the BPCs, e.g. Scenario 11 power-WC entrance manoeuvre).
  It surfaces what top-down misses: the power-WC deceleration envelope, the
  POTS seat height, the vestibular precipitant, the tactile-handrail need.

**The synthesis rule this run follows:** top-down UD sets the *floor and the
coverage map*; bottom-up FDR sets the *aspiration and the worst-case*. Where they
disagree, the evidence hierarchy governs (bottom-up FDR evidence is usually the
● anchor; top-down code convergence is the ○/◐ floor). Corridor width is the
canonical case: top-down UD gives 1800 mm (floor, ○); bottom-up FDR from the
swept envelope + DeafSpace gives 2440 mm (aspiration, ●).

## §0e. Thesis: Category E is its own category **and** a highly-impacted host surface

Circulation is a category in its own right (its own geometry, its own evidence
spine — the AWM envelope, the biomechanics cluster). But it is also the **host
surface every other category lands on**: the corridor *floor* is jointly
specified by E-08 (width), E-07 (slip), A-05 (carpet-for-VIS), C-03/C-05/C-06
(pattern/LRV), B-08 (gloss), A-09/floor-vibration (resilience); the corridor
*volume* by the sensory gradient (A/B/F) and wayfinding (D); its *edges* by
doors/hardware (I, H) and adjacent rooms (G kitchens/bathrooms). A vestibular
user's corridor is defined as much by C-06 (no repeating pattern), B-08 (no
specular floor) and D-10 (glazed-edge caution) — the **AX-BAL precipitants** —
as by E's own width. **Therefore E specs cannot be finalised in isolation from
A–K** (this is why the cross-category stress test in §D.3 is not optional), and
the item scaffold must record E as a coordinating host, not a silo.

---

## A. Evidence inventory

### A.1 Sources formally linked to these slugs (from `source_slug_links`)

146 links across the 8 slugs, essentially all `VERIFIED` in `evidence_sources`.
Distribution by tier (counts are live-queried, not transcribed as fixed truth):

| Slug | Links | Tier profile | Strongest anchor(s) |
|---|---|---|---|
| accessible-circulation-geometry | 14 | T2×1, T3×2, T4×1, T5×4, T6×6 | Russell/RCOT 2019 (T2 ●); Roxburgh 2024, Omura 2022 (T3 ●) |
| stair-ramp-threshold-biomechanics | 27 | T2×1, T3×14, T4×1, T5×2, T6×9 | Rouvier 2022 (T2 ●); Al Lawati 2017, Pavol 2001, Kim 2014 + cluster (T3-clinical ●) |
| threshold-and-level-access | 15 | T4×1, T5×5, T6×9 | ISO 21542 (T4 ◐); otherwise regulatory stratum |
| threshold-door-hardware | 32 | T3×2, T4×1, T5×11, T6×18 | Brandt 2016 (T3 ●, value-level 30 N/94.7 %); Putthinoi 2017 (T1 ●) |
| detectable-gradient-protocol-sensory-zones | 6 | T2×1, T3×3, T4×2 | Williams 2024 (T2 ●); Mostafa 2014, Kaplan 1989 (T3 ●) |
| cognitive-wayfinding-design | 25 | T2×5, T3×12, T5×7, T6×1 | Marquardt 2011 + van Buuren (T3 ●); Mostafa 2023, DSDC EADDAT (T2/Co-1 ●) |
| floor-vibration-wheelchair-disability | 7 | T2×1, T3×3, T4×3 | Larivière 2021 (T2 ●); Garcia-Mendez, Misch (T3 ●) |
| residential-entry-and-threshold | 20 | T2×3, T3×1, T4×1, T5×7, T6×8 | Russell 2019, DSDC 2020 (T2 ●); Putthinoi 2017 (T3 ●) |

Two verification exceptions to carry forward: **NZS 4121:2001** (TDH-09,
REF-00450) is `UNVERIFIED`; **Dementia Australia Built Environment Guidelines**
(RET-08, REF-00381) is `DISPUTED` (issuing-body ambiguity — do not lean on it
without resolution).

**The envelope-evidence spine (the ● anchors that matter most for geometry),**
already carrying the two `stated` cells:

- `E-12/MOB` (stated, T1+Co1+T2): Steinfeld 2010 AWM (T1, REF-00059/60 — the
  wheeled-mobility anthropometry *catalogue*), Davies 2021 / Habinteg IHDG 2024 /
  MLIT 2024 / Ifop-APF 2020 / Invalidiliitto ESKEH 2018 (Co-1), Sawatzky 2015
  (T1), Ringaert 2001 (T3), plus Norwegian & German T2 standards.
- `E-08/DEAF` (stated, Co1+T2): Bauman DeafSpace 2010 (Co-1, REF-00338/339),
  Vaughn DeafScape 2018 (Co-1), Bauman "Deaf Gain" 2014 (T2), Kusters Adamorobe
  2015 (Co-1).

### A.2 Sources cited in this BPC but NOT formally linked to the E item that names them

This is a structural defect, not a citation gap — the evidence exists and is
verified, but it is linked to the *wrong* slug:

- **E-09 "Tactile Walking Surface Indicators (ISO 23599:2019)"** is linked to
  `detectable-gradient-protocol-sensory-zones`, whose 6 sources are about
  *multi-sensory zone gradients* (RT60/lux/LRV transitions) and contain **no**
  tactile-paving evidence. The real TWSI corpus — ISO 23599:2019 (REF-00199,
  REF-00506), GB 50763-2012 tactile guiding (REF-00016/510), JIS T braille
  blocks (REF-00017), ABNT NBR 16537:2024 (REF-00019), Korean 편의증진법 tactile
  advocacy/critique (REF-00021), REF-00015 — is linked to VIS, DBL, and
  wayfinding-global-south. **Action:** re-home E-09 to the TWSI evidence (§G).
- **E-07 "Slip Resistance (PTV ≥36)"** is linked to
  `stair-ramp-threshold-biomechanics`, which carries **no** PTV / pendulum /
  slip-coefficient evidence. Slip evidence lives in
  `accessible-bathroom-and-grab-bar` and ALL-ROOMS. **Action:** re-home E-07 (§G).

### A.3 Practitioner / secondary sources

The BPC prose leans on standards-body and DPO guidance (Habinteg, RCOT, DSDC,
DeafSpace, RHFAC, Livable Housing Australia). Per the role-appropriate-authority
gate (`tier-system.md` §10): a firm/architect guide **cannot** anchor a
functional-need claim alone — that needs Co-1 or Co-2. Habinteg/RCOT outputs
qualify as Co-1/Co-2 (disability-led / OT professional body) and DO anchor;
generic practitioner white-papers do not and are flagged where they appear.

### A.4 Primary regulatory documents retrieved (the T4–T6 stratum)

Comprehensively catalogued across 24 jurisdictions: EN 81-70:2021 (lifts),
ISO 21542:2021, BS 8300-2:2018, DIN 18040-1/-2, ADA 2010, AS 1428.1:2021,
TEK17, BFS 2024:12, Part M, GB 50763, NBR 9050, and national equivalents. These
are valid for **code-floor** claims and jurisdiction-tracking only. **Code
currency (§4 tier-system):** DIN 18040-1:2010 is 15 years old but still in force
(MVV TB 2024/1) with draft E:2023 pending; NZS 4121:2001 remains in force per NZ
Building Act — age does not predict supersession, but any T4–T6 citation that
crosses the tier freshness thresholds (T4: 7 y; T5/T6: 5 y) must be
currency-checked before it anchors even a ◐/○ claim.

### A.5 Gaps in the evidence inventory

Open and newly-surfaced gaps, with adversarial fields where held:

- **GAP-019 (OPEN, P3)** — Ramp 1:20 SCI-specificity. 1:20 rests substantially
  on general-WC evidence; the "Yang et al. 2.09× handrim force" and "Japanese
  cervical-SCI 0.23–0.26 W/kg" figures are **NOT VERIFIED** in indexed
  literature → carry **[UNVERIFIED-QUANT]**. Named dissenter path: Lalumière
  PLOS One 2022 SR (34 articles on slope biomechanics) is the proper primary
  source and is unread. *Falsification:* recommendation changes if the 2022 SR
  finds a safe SCI gradient ≠ 1:20.
- **GAP-008 / GAP-011 (I-01, cross-category)** — the ≤22 N door force cites ISO
  21542 + CSA B651 = **code standards** (regulatory stratum), not evidence.
  Directly relevant to E-11/door-force reconciliation (§B.5, §D).
- **GAP-016 / GAP-023 (E-03)** — 3× energy-expenditure claim, 9 m max run,
  1500×1500 rest platform carried without stratum annotation / citation → treat
  as value-level-PENDING.
- **NEW — value-level extraction empty for circulation.** No
  `source_value_extractions` rows exist for any circulation slug. Every
  quantitative magnitude below is direction-anchored, value-PENDING. *This is
  the gating next step.*
- **NEW — E-07 and E-09 evidence mis-linkage** (see A.2).
- **NEW — E-14 vacant; E-15 mis-categorised** (see §G).
- **NEW — `item_axis_links` table is empty.** The work-from-axes frame is
  doctrine but not operationalised in the DB join table; the axis mappings in
  this document are authored from `axes.design_domains` prose, not from a
  populated link table.

---

## B. Per-parameter reasoning (9-step rule)

Nine-step blocks for the load-bearing parameters. Direction is graded now;
magnitude is value-level-PENDING per Headline Caveat 1. Markers on every
spec sentence (`●` full / `◐` partial / `○` weak).

### B.1 Parameter: Ramp gradient (rise:run) — E-03

**Step 1 — Direction**: LOWER gradient is better (gentler). Direction is
POPULATION-CONVERGENT for wheeled propulsion, ambulant fatigue (MS/OFS), and
pain-load; no population wants a steeper ramp.

**Step 2 — Per-population worst-case user**: AX-WHM worst case = manual-WC user
with reduced propulsive capacity (high cervical SCI, C5–C6) — highest handrim
force per unit slope. AX-AMB/AX-STA worst case = MS/OFS ambulant user for whom
gradient is a temporal-accessibility / post-exertional-malaise driver, not a
one-off effort. Cross-population conflict: **NO** (all favour gentler).

**Step 3 — Jurisdiction comparison (worst-case-point)**: statutory maxima cluster
at 1:12 (8.3 %) as the *floor* (ADA, most codes); 1:20 (5 %) appears as the
"self-propulsion" recommended value in BS 8300 / national frameworks. These are
◐/○ code values; convergence on them is not evidence.

**Step 4 — Lowest-barrier code per population**: for AX-WHM the gentlest code
recommendation is 1:20 (T5 ◐); statutory floor 1:12 (T6 ○).

**Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence**: Kim 2014 (T3-clinical ●, REF-00030) —
propulsion effort and fall risk rise sharply above ~6 % gradient. Rouvier 2022
(T2 sr_meta ●, REF-00037) — manual-WC biomechanics overcoming environmental
barriers, synthesis-level support for gentler-is-better. Waters 1988 (T3 ●,
REF-00385) — energy-speed baseline. These anchor the **direction** at ●.

**Step 6 — Guidebook chosen value per population**: ≤1:20 (5 %) as the aspirational value ●
*for direction*; **magnitude value-level-PENDING** — the "1:20" number is a
code+single-study convergence, not yet value-extracted. Statutory 1:12 is the
compliance floor ○, never the aspiration.

**Step 7 — Rationale**: gentler gradients reduce shoulder-injury cumulative load
(propulsion) and post-exertional cost (ambulant fatigue). `[OPUS-DECISION
session_2026-07-23]`: render as "≤1:20 ● (direction); magnitude PENDING," not
"≤1:20 best practice ●," because value-level support is absent and GAP-019's
SCI-specific caveat is open.

**Step 8 — Trade-offs**: gentler ramps consume more plan length / rise-to-run
footprint (cost, retrofit feasibility); handrails + rest landings interact (§B
stair). Ambulant-disabled users (cane/frame) often prefer a stepped route *with*
handrail alongside the ramp (residential-entry BPC; Scottish TH) — provide both.

**Step 9 — Cross-population conflict flag**: N/A for gradient direction. (The
ramp-vs-steps *provision* question is a plan-level, not gradient-level, matter —
resolved by providing both routes.)

### B.2 Parameter: Threshold height at level entry (mm upstand) — E-05/E-06

**Step 1 — Direction**: LOWER upstand is better **for wheeled mobility**;
**CONTESTED** overall — a fully flush threshold removes the tactile/visual cue
some cane and low-vision users use to detect a doorway/level change.

**Step 2 — Per-population worst-case user**: AX-WHM worst case = manual-WC caster
(≈75 mm dia.) at low approach speed — tips on upstands >~6 mm (Al Lawati). AX-VIS-N
worst case = long-cane user relying on a detectable threshold lip / contrast for
door location. These pull in **opposite** directions → CONTESTED.

**Step 3 — Jurisdiction comparison**: DE/NO/JP mandate 0 mm (Nullschwelle /
段差なし); US ≤13 mm; UK ≤15 mm; DE draft ≤10 mm; FR/NL/BR ≤20 mm; NO ≤25 mm as
"trinnfri." Wide spread; all T6/T5 ◐/○.

**Step 4 — Lowest-barrier code per population**: for AX-WHM the most-accommodating
value is 0 mm (DE/NO/JP). For AX-VIS-N no code specifies a *minimum* detectable
upstand — the tactile-cue need is served by contrast + TWSI, not by keeping a lip.

**Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence**: Al Lawati 2017 (T3-clinical ●,
REF-00025) — a 2 cm threshold defeats **45.8 %** of manual-WC users on first
attempt (DOI/PMID present → value verified, cite directly). Pavol 2001 (T3 ●,
REF-00387) — upstands >6 mm intercept older-adult gait. Rouvier 2022 (T2 ●).
These anchor the **wheeled/ambulant** direction (lower-is-better toward zero) at
**●** — so the level-entry parameter for AX-WHM is NOT merely a regulatory-stratum
claim. **This is a correction to the current `E-06/MOB` cell (see §C).**

**Step 6 — Guidebook chosen value per population**: AX-WHM: **0 mm** flush at all accessible
thresholds; where a weather/structural upstand is unavoidable **≤6 mm** vertical
then bevel — ● direction (Al Lawati/Pavol), value 6 mm value-level-PENDING but
grounded in the 75 mm-caster tip geometry. AX-VIS-N: the detectability need is
met by **luminance contrast + TWSI/attention indicator at the door**, NOT by
retaining an upstand ● — so the contest is *resolvable by substitution* rather
than by compromise on the upstand.

**Step 7 — Rationale**: the "13/15/20/25 mm" jurisdictional spread reflects
different *weather-protection* assumptions, not different functional
requirements; the functional requirement (caster geometry) is uniform and
favours zero. `[OPUS-DECISION session_2026-07-23]`: resolve MOB↔VIS by
substitution (contrast + attention indicator) not by upstand compromise —
provided the substitution is specified; if it is not, the parameter is CONTESTED
and anchors nothing (record conflict).

**Step 8 — Trade-offs**: zero threshold needs a drainage channel + thermally-broken
threshold unit (cost); the substitution obligation (contrast + indicator) must be
carried or the VIS need is silently dropped.

**Step 9 — Cross-population conflict flag**: **QUEUE** to
`cross-population-conflict-resolutions` — MOB(flush) ↔ VIS(detectable) — with the
recommended resolution = substitution (contrast + attention indicator + TWSI at
door), NOT upstand retention. Until logged, render the jurisdiction spread with
each population's direction stated (`evidence-architecture.md:106`).

### B.3 Parameter: Corridor clear width (mm) — E-08

**Step 1 — Direction**: WIDER is better up to the point that satisfies the
worst-case swept envelope and the widest anticipated simultaneous use (signed
conversation, two-device passing). Not unbounded (over-wide corridors harm
VIS trailing and DEM legibility) — so **POPULATION-DEPENDENT ceiling**, wider floor.

**Step 2 — Per-population worst-case user**: AX-WHM worst case = two power-WC /
scooter users passing, footplate-to-footplate, from the **swept envelope** (not
turning circle). AX-AUD/DEAF worst case = two people signing while walking
(needs sightline + arm space). AX-VIS-N counter-consideration = a shoreline to
trail; over-wide open corridors lose it. Conflict at the *ceiling*, convergent at
the *floor*.

**Step 3 — Jurisdiction comparison**: code floors 900–1200 mm single passage;
"1800 mm two-way passing" converges across BS 8300 / DIN 18040-1 / Part M / AS
1428.1. **This 1800 mm convergence is the canonical convergence-not-evidence trap
(`tier-system.md:45`) — it is the regulatory floor, NOT best practice.**

**Step 4 — Lowest-barrier code per population**: 1800 mm (◐/○) for two-WC passing;
no code addresses signed-conversation width.

**Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence**: Steinfeld AWM 2010 (T1 ●, REF-00059/60)
+ Steinfeld 2006 RESNA swept-path → **2400 mm** clear floor to accommodate the
entire-sample 180° turn (envelope, not radius). Bauman DeafSpace 2010 (Co-1 ●,
REF-00338/339) + Vaughn 2018 (Co-1 ●) → **2440 mm** primary corridors with glazed
intersections for signed conversation. Ringaert 2001 (T3 ●, REF-00073) —
code turning dimensions are demonstrably too small. Two independent evidence
streams (swept envelope + DeafSpace) converge at ~2400–2440 mm at **●**.

**Step 6 — Guidebook chosen value per population**: **primary mixed-population corridors
≥2440 mm ●** (DeafSpace Co-1 + Steinfeld swept-envelope T1, converging; this is
the `E-08/DEAF` stated anchor extended to AX-WHM); **secondary corridors
≥1830 mm ○** (code-floor band); glazed/transparent intersections ● (DeafSpace +
serves NDV/MH anti-ambush simultaneously). Magnitude 2440 mm carries genuine
convergent support but remains value-level-PENDING in the extraction table.

**Step 7 — Rationale**: derive from the swept ENVELOPE across the device range,
worst-case device (power-WC/scooter) governing, median at Population Mode. The
1800 mm code convergence describes the floor; the 2440 mm evidence describes best
practice — labelling 1800 mm "preferred" (as the current ACG BPC does) is the
named failure mode. `[OPUS-DECISION session_2026-07-23]`.

**Step 8 — Trade-offs**: 2440 mm costs plan area; VIS shoreline is preserved by a
detectable wall/guide edge, not by narrowing; the ceiling is bounded so corridors
don't become disorienting open plan es for DEM.

**Step 9 — Cross-population conflict flag**: resolved at building-plan level
(glazed intersections satisfy DEAF sightline + NDV/MH anti-ambush); VIS shoreline
preserved by edge definition. Log the resolution; no unresolved conflict at the
cross-section.

### B.4 Parameter: Rest-seating interval and seat height — E-10

**Step 1 — Direction**: SHORTER max interval is better (AX-STA); HIGHER seat
(to a physiologic point) is better for POTS venous pooling. Convergent.

**Step 2 — Per-population worst-case user**: AX-STA worst case = ME/CFS or POTS
user for whom uninterrupted distance is a post-exertional-malaise / orthostatic
trigger, not mere tiredness. Ambulant MOB / PAIN secondary. Conflict: **NO**.

**Step 3 — Jurisdiction comparison**: **no building code in any of 14 languages
specifies a maximum rest-seating interval** (confirmed absence). This parameter
has NO regulatory floor — it exists purely on evidence.

**Step 4 — Lowest-barrier code per population**: none exists.

**Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence**: Roxburgh 2024 (T3-clinical ●,
REF-00426) — ME/CFS time-diary / energy-conservation; POTS seat-height rationale
(standard 420 mm bench promotes hip-flexion venous pooling; ≥480 mm reduces it).
Omura 2022 (T3 ●, REF-00427) — energy-conservation scoping. Russell/RCOT 2019
(T2 ●, REF-00053) — alcove geometry (≥450 mm seat depth + ≥200 mm recess; ≥900 mm
width per person for companion). These anchor **direction and some magnitudes**
at ●.

**Step 6 — Guidebook chosen value per population**: rest seating at **≤25–30 m intervals ○** on
primary routes (expert-consensus/thin — no code, derived from clinical energy
literature; render flagged); **seat height ≥480 mm AFF for POTS ●** (Roxburgh,
value-stated); **alcove ≥450 mm deep + ≥200 mm recess, ≥900 mm wide ●** (RCOT
Co-2, value-stated); **tilt/recline option for OFS ○** (expert-consensus). Note
the interval magnitude is the weakest link (○), the seat/alcove geometry the
strongest (●).

**Step 7 — Rationale**: this is the cleanest demonstration in the category that
best practice ≠ code — there is *no* code, and the spec is wholly
evidence-derived. The interval band (25–30 m) is honestly ○ until a study
value-anchors a threshold; the seat/alcove dimensions are ● from RCOT/Roxburgh.

**Step 8 — Trade-offs**: seating consumes circulation/plan area and must not
obstruct the passing envelope (the ≥200 mm recess is exactly this reconciliation
with §B.3).

**Step 9 — Cross-population conflict flag**: N/A (convergent). Cross-links to
G-02/G-07/F-05/A-17 seating items — see §D.

### B.5 Parameter: Door operating force / powered operation — E-11 (and I-01, H-04)

**Step 1 — Direction**: LOWER operating force is better (AX-REA/AX-WHM/AX-STA);
powered/automatic operation removes the force barrier entirely.

**Step 2 — Per-population worst-case user**: AX-REA worst case = UPL user with
reduced grip/one-handed operation; AX-WHM worst case = manual-WC user pushing
a door while stabilising the chair; AX-STA = low-force-budget user for whom a
heavy door is an exertion cliff.

**Step 3 — Jurisdiction comparison**: force maxima 20–50 N across codes: AU/NO
≤20 N (strictest); UK Part M / KR / IT ≤30 N; FR ≤50 N (outlier). Threshold-door
BPC calls ≤20 N "best practice" — **but ≤20 N is the AU/NO CODE value; calling it
best practice is a convergence claim, not evidence.**

**Step 4 — Lowest-barrier code per population**: ≤20 N (AU/NO, T6 ○).

**Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence**: **Brandt 2016 (T3-clinical ●,
REF-00204) — 30 N acceptable to 94.7 % of WC users; 40 N to 92.1 %; walker users
30 N = 100 %.** This is the one circulation parameter with a **directly stated,
value-level** empirical anchor. Putthinoi 2017 (T1 ●, REF-00407) — combined
threshold+landing barrier effect on home-bound elders.

**Step 6 — Guidebook chosen value per population**: **eliminate operating force via automatic
sliding doors at primary entrances and on primary routes ●** (functional-need
anchored by Brandt: force is a measured barrier); where manual, **≤30 N operating
force ●** (Brandt value-level: acceptable to 94.7 %). ≤20 N is a *more
conservative code value* ○ — acceptable to specify, but its authority is the code,
not evidence; it must not be rendered "best practice ●." FR ≤50 N is below the
empirical acceptability curve (Brandt) — flag as sub-standard.

**Step 7 — Rationale**: `[OPUS-DECISION session_2026-07-23]` — the honest anchor
is Brandt's ≤30 N/94.7 % (●, value-level), not the ≤20 N code convergence. This
inverts the current BPC's framing. Powered operation is the aspiration (removes
the parameter); ≤30 N is the manual-fallback evidence anchor.

**Step 8 — Trade-offs**: automatic doors cost more and need maintenance / safe
sensing; ≥5 s closing sweep (ADA/BS 8300 ◐) interacts with fire-door
requirements (H-04, egress).

**Step 9 — Cross-population conflict flag**: N/A for force direction. **Cross-category
reconciliation REQUIRED** with I-01 (≤22 N, code-anchored per GAP-008/011) and
H-04 (video door entry, same slug) — see §D. One door force anchor should govern
E-11/I-01/H-04, and it should be Brandt's ● value, not three different code
numbers.

### B.6 Parameter: Lift car internal dimensions — E-01 (and E-02 platform lift)

**Step 1 — Direction**: LARGER car is better up to the worst-case device +
companion/transfer envelope; bounded above by shaft cost/feasibility.

**Step 2 — Per-population worst-case user**: AX-WHM worst case = large power-WC or
scooter + accompanying person / assisted transfer (independent AND assisted —
`axes.AX-WHM`). Manual-WC + companion is the lower bound; power-WC + companion the
governing envelope.

**Step 3 — Jurisdiction comparison**: EN 81-70:2021 Type 2 = 1100×1400 mm (T4 ◐,
the international minimum); BS 8300 recommends 1100×2000 mm for new build (T5 ◐);
ADA §407 uses a different geometry (1370 mm depth). Convergence on Type 2 is a
floor.

**Step 4 — Lowest-barrier code per population**: Type 2 1100×1400 (◐).

**Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence**: Steinfeld AWM 2010 (T1 ●) / IDeA Center
Steinfeld 2010 — power-WC users need ≈1400×1600 mm minimum for independent use
(envelope evidence). This exceeds Type 2 depth-for-width and anchors the ● best
practice.

**Step 6 — Guidebook chosen value per population**: **≥1100×1800 mm car (stretcher/large-power-WC
capable) ●** as the envelope-derived aspiration; Type 2 1100×1400 mm is the ◐
international floor; landing **≥1500×1500 mm** clear turning is the code value ○
but per the swept-envelope logic a power-WC landing should be ≥1800×1800 mm ●
(BS 8300 Annex G / Steinfeld). Magnitudes value-level-PENDING.

**Step 7 — Rationale**: same envelope-not-radius logic as corridor; the Type 2
car is a floor calibrated to manual-WC+companion, not to the power-WC/scooter
worst case.

**Step 8 — Trade-offs**: larger cars raise structural/shaft cost sharply (E-01 is
the category's most cost-significant item — GAP-004/005/006 economics; documented
~20× retrofit penalty vs design-stage). Platform lift (E-02) is the fallback only
where a full passenger lift is unachievable.

**Step 9 — Cross-population conflict flag**: N/A. Cross-links: lift controls →
H-01 (reach range); call buttons → I-01 hardware; DEAF/VIS in-car alerting →
K-04/H-03.

### B.7 Parameter: Tactile Walking Surface Indicators — E-09 (evidence not yet linked)

**Step 1 — Direction**: detectability of hazard/guidance underfoot HIGHER is
better for AX-VIS-N; **CONTESTED** — raised TWSI is a trip/roll/pain precipitant
for some AX-AMB, AX-WHM, AX-BAL and AX-PAI users.

**Steps 2–4**: cannot be responsibly completed in this run because the TWSI
evidence is **not linked to E-09's slug** (§A.2). The governing corpus (ISO
23599:2019 REF-00199/506; GB 50763; JIS T; NBR 16537:2024 REF-00019; Korean
편의증진법 advocacy/critique REF-00021) sits under VIS/DBL/wayfinding-global-south.

**Step 5 — evidence (from where it actually lives)**: ISO 23599 (T4 ◐, dimensional
standard); the Korean advocacy source (REF-00021) is Co-1-adjacent lived critique
documenting 20+ years of deformed/irregular tactile blocks and maintenance
failure — a caution that *installation/maintenance quality*, not just presence,
governs whether TWSI helps. DBL corpus adds the deafblind reliance case.

**Step 6 — Guidebook chosen value per population**: **DEFERRED** pending re-linkage. Provisional
direction: provide ISO 23599-conformant warning (dot) + directional (bar)
surfaces at hazards/decision points ◐, with the **CONTESTED-direction flag** for
ambulant/wheeled/pain trip-and-roll and a substitution note (contrast +
detectable edge) where TWSI would harm those users.

**Steps 7–9**: `[OPUS-DECISION session_2026-07-23]` — do not author a full TWSI
spec on a slug that lacks the evidence; re-link first (§G), then run the 9-step
against the real corpus. Log MOB/PAIN ↔ VIS as CONTESTED (anchor nothing
universally; render per-population).

### B.8 Parameter: Entrance cognitive legibility — E-13 (overlaps D-suite)

**Step 1 — Direction**: HIGHER legibility (single clear route, landmark at
decision points, toilet visible, warm-colour door reading as "door" at 3 m) is
better for AX-COG-O; low visual clutter better for NDV/AUT.

**Step 2 — worst-case user**: AX-COG-O worst case = DEM user with topographical
disorientation; NDV/AUT worst case = user over-loaded by complex wall surfaces.
Historically a conflict (DEM wants high-contrast landmarks; AUT wants low
clutter) — **resolved** by using isolated 3-D object landmarks only at
navigationally-relevant decision points (Marquardt; the strongest resolution in
the compendium).

**Step 3–4**: no code specifies entrance cognitive legibility (Tier 5/Co-1
guidance only: DSDC, KDA, Dementia Australia).

**Step 5 — evidence**: Marquardt 2011 (T3 ●, REF-00202); van Buuren 2022/2025
(T3 ●); Mostafa 2023 (T2 ●); DSDC EADDAT 2022 (Co-1 ●); Dementia Australia (T2 ●,
but see RET-08 DISPUTED note). Strong ● base.

**Step 6 — chosen value**: 3-D object landmark at each decision point ●; single
clear route / no dead ends ●; toilet visible from primary occupied space ●;
warm-colour door legible at 3 m ● (RCOT Dementia Guidance Co-2); PIR entrance
lighting ≥150 lux ● (RCOT); house/room identifier ≥150 mm numerals ○ (AOTA, GREY).

**Step 7–9**: `[OPUS-DECISION session_2026-07-23]` — E-13 is largely a
**duplicate** of D-02/D-07/D-08/D-10 (all `cognitive-wayfinding-design`). The
9-step here is sound but the *item boundary* is the real issue: E-13 should be
either the entrance-scoped slice of the D-suite or merged (§D, §G). Conflict
resolution (3-D landmark) logged.

### B.9 Parameter: Handrails — continuity + tactile information (serves AX-BAL + AX-VIS-N) — NO ITEM EXISTS

**Step 1 — Direction**: continuous, graspable, correctly-heighted handrail
support is better for AX-BAL (balance/vestibular) and AX-AMB; a handrail that
additionally carries **tactile information** (directional/end indicators,
floor-level/room info) is better for AX-VIS-N. POPULATION-CONVERGENT on
presence; the *information* layer is VIS-specific and additive.

**Step 2 — Per-population worst-case user**: AX-BAL worst case = a user with
vestibular dysfunction / fall risk for whom loss of continuous support at a gap,
corner, or level change is a fall trigger — and who is *also* destabilised by
the AX-BAL environmental precipitants (repeating-pattern floors, specular/glossy
floors, glazed edges at height, large uniform visual fields). AX-VIS-N worst
case = a blind/low-vision user trailing the rail as a shoreline and reading
tactile cues at decision points. AX-AMB (cane/frame) and OFS/NEU users who
"prefer steps with handrail" (residential-entry BPC).

**Step 3 — Jurisdiction comparison**: handrail height, continuity, extensions,
and profile are specified in ISO 21542 (T4 ◐), BS 8300 (T5 ◐), and national
codes (T6 ○) — REF-00883 (T4), REF-00759 (T5), REF-00767/769 (T6) located in the
corpus but **not linked to circulation slugs**. Tactile-end/round-off indicators
appear in ISO 21542 / national handrail provisions (◐).

**Step 4 — Lowest-barrier code per population**: continuous bilateral handrails
to ramps/stairs with extensions at top/bottom (◐, ISO 21542 / BS 8300).

**Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence**: **THIN.** Lord 1993 (T3 ●, REF-00390)
supports sit-to-stand/balance as a falls predictor generally, but **no located
primary source anchors handrail continuity, height, or tactile-information
handrails specifically** — consistent with AX-BAL being a STUB axis ("zero
b-codes, zero slugs, zero searches" — `axes.AX-BAL`). Vestibular circulation
evidence is a single T5 hit (REF-00761). **Do not fabricate a ● here.**

**Step 6 — Guidebook chosen value per population**: continuous, graspable (≈32–45 mm profile)
bilateral handrails on all ramps and stairs, with top/bottom extensions ◐
(standards basis, ISO 21542 / BS 8300 — not primary evidence); **tactile
directional/end information on handrails at decision points ◐/○** (design
technique with standards footing but no located primary anchor — flag
**[THIN BASE]**); handrail continuity through the corridor run for AX-BAL where
fall-risk is anticipated ○ (functional-need direction real; magnitude/height
value-level-PENDING and evidence thin). **AX-BAL environmental precipitants are
handled in Category A/B/C, not here** (see §D.3): plain non-repeating flooring
(C-06), matte non-specular floor (B-08), caution at glazed edges (D-10).

**Step 7 — Rationale**: `[OPUS-DECISION session_2026-07-23]` — the honest state
is that circulation handrails and tactile-info handrails are a **real functional
need with only standards-level (◐) and thin evidence**, and — critically — **no
item exists** to carry them (§G proposal 5/10). This is a coverage gap, not a
solved spec. The vestibular/sight framing the owner raised is exactly what
top-down UD (wheel-framed) misses and bottom-up FDR surfaces.

**Step 8 — Trade-offs**: bilateral rails consume clear width (trade against
§B.3); tactile-info rails need maintenance and standardised legends to be
usable (cf. the Korean TWSI maintenance-failure caution).

**Step 9 — Cross-population conflict flag**: mild — a mid-corridor handrail can
narrow the passing envelope; resolve by recessing or by rail-zone additive to the
2440 mm clear. AX-BAL precipitant control (no specular/pattern floor) is fully
convergent with VIS and DEM needs (C/B). QUEUE a handrail item creation (§G).

### B.10 Parameter: Corridor length / uninterrupted run (m before rest) — NO ITEM (folded into E-08/E-10)

**Step 1 — Direction**: SHORTER uninterrupted run before a rest opportunity is
better for AX-STA and AX-AMB fatigue; unbounded length is an exertion cliff.

**Step 2 — Per-population worst-case user**: AX-STA worst case = ME/CFS/POTS user
for whom a long corridor is a post-exertional-malaise trigger (the same
mechanism as gradient); AX-AMB = MS fatigue; AX-BAL = user who needs continuous
support over the run (§B.9).

**Step 3–4 — Jurisdiction comparison**: **no code specifies a maximum corridor
run before rest** (parallel to the rest-seating-interval absence, §B.4). The only
run-based rule is the ramp/stair **rest landing every 10 m run (or 750 mm rise)**
(RCOT / Scottish TH, Co-2/T5 ◐).

**Step 5 — evidence**: Roxburgh 2024 / Omura 2022 (T3 ●) — energy-conservation /
distance-as-barrier direction; RCOT (Co-2 ◐) — the 10 m landing rule.

**Step 6 — Guidebook chosen value per population**: rest opportunity (seating alcove §B.4 or
landing) at **≤25–30 m on the level ○** (mirrors the seating interval; no code,
clinical-inference) and **≤10 m on any graded run ◐** (RCOT). State: this is a
*length* parameter of the corridor, presently invisible because it is buried in
the ramp spec; it should be an explicit circulation parameter.

**Step 7–9**: `[OPUS-DECISION session_2026-07-23]` — surface corridor *length*
as a first-class parameter co-located with E-08 (width) and E-10 (rest); the two
absences (no interval code, no run code) are honest ○/◐, not gaps to be filled
with invented numbers. Convergent across AX-STA/AX-AMB/AX-BAL; no conflict.

---

## C. Synthesis claims that did NOT survive evidence review

1. **"1800 mm two-way corridor is preferred / best practice"** (ACG BPC). RETRACTED
   as best practice: it is a T5/T6 convergence value (◐/○ floor). Replacement:
   ≥2440 mm primary ● (DeafSpace Co-1 + Steinfeld swept-envelope T1); 1800 mm is
   the code floor only.
2. **"≤20 N door operating force is best practice"** (threshold-door BPC).
   RETRACTED as ●: ≤20 N is the AU/NO code value (○). Replacement: eliminate force
   via powered doors ●; manual fallback ≤30 N ● (Brandt value-level, 94.7 %
   acceptable). ≤20 N may still be specified as a conservative code target ○.
3. **`E-06/MOB` rendered as regulatory_stratum_only ○ / "no anchoring dimension
   exists."** RETRACTED: the wheeled-mobility level-entry direction IS ●-anchored
   (Al Lawati T3 45.8 %; Pavol T3; Rouvier T2). The cell under-grades the
   evidence AND mishandles the MOB↔VIS contest. Replacement: ● direction for
   AX-WHM toward zero upstand + CONTESTED flag vs AX-VIS-N with substitution
   resolution (§B.2). *(This is a proposed cell correction, owner-gated — §G.)*
4. **A-09 "0.1 m/s RMS" floor-vibration threshold** (feeds circulation surfaces).
   Carries **[UNVERIFIED]** — does not correspond to any ISO 2631-1 value (which
   uses weighted acceleration m/s², not RMS velocity); may be a mis-import from
   DIN 4150-2 (structural, not accessibility). Retain the directional claim
   (resilient flooring reduces WBV — Larivière T2 ●) but the specific threshold
   number stays flagged.
5. **Ramp "2.09× handrim force" / "0.23–0.26 W/kg cervical-SCI"** (GAP-019).
   **[UNVERIFIED-QUANT]** — not located in indexed literature; do not publish the
   number. Direction (gentler-better) survives at ●; the SCI-specific magnitude is
   open pending Lalumière 2022 SR.
6. **"30 % LRV contrast" as an evidence-based threshold.** Manandhar 2022 (T3-grey
   ○, REF-00393) documents that the 30 % value lacks a published evidence basis.
   Retain as ○ interim ("highest achievable contrast" as the real aspiration);
   do not render 30 % as ●.
7. **All PRE-REHABILITATION banners.** Every circulation BPC still says
   "RETRACTED PENDING REVERIFICATION." This run performs that reverification at
   the reasoning-doc level; the BPC banners should be updated to point here once
   the cells are operationalised (§G).

---

## D. Cross-references

### D.1 Items derived from this synthesis (current E map)

E-01/E-02 lift (B.6) · E-03 ramp (B.1) · E-04 parking · E-05 weather protection
(B.2 threshold + canopy) · E-06 level entry (B.2) · E-07 slip (mis-linked, A.2) ·
E-08 corridor (B.3) · E-09 TWSI (mis-linked, B.7) · E-10 rest seating (B.4) ·
E-11 doors (B.5) · E-12 landing/manoeuvring (envelope, stated) · E-13 entrance
legibility (B.8) · E-14 vacant · E-15 Changing Places (bathroom, mis-filed).

### D.2 Within-Category-E robustness test (spec-against-spec)

| Test | Interacting E specs | Finding |
|---|---|---|
| Passing envelope vs rest seating recess | E-08 (≥2440 mm) × E-10 (≥200 mm alcove recess) | CONSISTENT — recess is defined precisely so seating never intrudes on the swept passing envelope. Robust. |
| Threshold zero vs slip/weather | E-06 (0 mm) × E-05 (canopy/drainage) × E-07 (slip) | CONSISTENT if the thermally-broken drained threshold unit is specified; E-05 canopy reduces the wet-threshold slip case (E-07). |
| Ramp vs landing vs stair | E-03 (≤1:20) × E-12 (landing) × stair route | CONSISTENT — provide ramp + complementary stepped route with handrail; rest landing interacts with E-10. |
| Corridor width vs lift/landing | E-08 × E-01 car × E-12 landing | CONSISTENT under one envelope logic — all three must derive from the same AWM device range, worst-case device governing. **Currently they don't** (car = Type 2 code floor; landing = 1500 mm code floor) → tighten to envelope. |
| Door force vs manoeuvring | E-11 (≤30 N / powered) × E-12 (latch-side clearance) | CONSISTENT — powered operation removes the force×clearance interaction entirely. |
| Level entry vs TWSI | E-06 (flush) × E-09 (detectable) | **CONTESTED** — flush removes tactile cue; TWSI/contrast substitution reconciles. Must be co-specified. |

### D.3 Cross-category robustness test (E vs A–K) — owner directive 2026-07-23

Tested via the **swept-envelope / device-range** lens where geometric, and the
**weighted-strength band** lens where evidential.

| E spec | Interacts with | Nature | Finding / required action |
|---|---|---|---|
| E-11 door force | **I-01** (≤22 N, code-anchored, GAP-008/011) · **H-04** (video door entry, same slug) | Duplication + contradiction | Three different force numbers (≤20/≤22/≤30) across items; only Brandt ● (≤30 N) is evidence. **Reconcile to one Brandt-anchored force spec.** |
| E-08 corridor floor | **A-05** (carpet where VIS navigation) · **C-03/C-06** (plain, no pattern) · **C-05** (low LRV differential, DEM) · **B-08** (matte ≤30 gloss) · **E-07** (slip PTV≥36) · **A-09/floor-vibration** (resilient) | Multi-item convergence on ONE surface | A single corridor floor must be: ≥2440 mm wide, plain/low-pattern (C), low LRV differential (DEM), matte (B-08), slip-resistant (E-07), resilient for WBV (A-09), and trailing-detectable at edges (VIS). **Mostly compatible; the tension is patterned-carpet-for-VIS (A-05) vs plain-for-DEM/vestibular (C-06) — resolve to plain resilient surface with edge/contrast shoreline, not surface pattern.** |
| E-10 rest seating | **G-02** (three seat heights) · **G-07** (waiting seating) · **F-05** (seated-task OFS) · **A-17** (upholstered) · **D-05/D-11** (alcoves, garden seating) | Seat-height + provision reconciliation | E-10 ≥480 mm (POTS) vs stair-ramp 450–500 mm vs G-02 "three heights." **Reconcile: range 450–500 mm with ≥480 mm as the POTS end; state which end applies at which mode (Population median vs Person co-design) per `project-standards.md:32`.** |
| E-09 TWSI | **K-02** (tactile map) · **K-04** (vibrotactile) · **A-15/A-05** (acoustic navigation) · **C-04** (LRV at junctions) · **B-12** (pathway lighting) | Redundancy layer for VIS/DBL | TWSI is one channel in a multi-channel VIS/DBL system; must be specified alongside K-02/A-15/C-04, not alone. Re-link E-09 (§G) then coordinate. |
| E-13 entrance legibility | **D-02/D-07/D-08/D-10** (same slug) · **C-01/C-02** (colour) · **B-05** (lighting transition) | Duplication | E-13 and the D-suite draw from `cognitive-wayfinding-design`. **Define the boundary: E-13 = entrance-scoped legibility; D-suite = internal wayfinding — or merge.** |
| E-01 lift controls | **H-01** (controls 400–1100 mm) · **I-01** (hardware) | Reach envelope | Lift call/car controls must obey H-01 reach range and I-01 operation — inherit, don't re-derive. |
| E-06/E-05 threshold | **G-04** (wet-room zero threshold) · **I-03** (bathroom one-hand) | Same zero-threshold logic | Consistent — G-04 wet room is the same flush-threshold + drainage problem indoors; share the resolution. |
| E-07 slip | **G-03/G-04/I-03** (bathroom slip) · **B-08** (gloss) · **C-06** (flooring) | Shared evidence home | E-07's real evidence lives in the bathroom slip corpus; **re-link and coordinate PTV across wet + circulation surfaces.** |
| E-15 Changing Places | **G-03/G-04/I-03/I-04** (bathroom + hoist) | Mis-categorisation | E-15 is a bathroom/hoist item (uses `accessible-bathroom-and-grab-bar`); **belongs in Category G, not E.** |
| E-05 canopy | **K-05** (thermal comfort) · **F-08** (thermal transition) · AX-THR | Thermal cross-link | Sheltered entry interacts with thermoregulation-impaired users (MS/OFS); coordinate canopy with thermal-transition provisions. |
| **Handrails** (B.9, no item) | **G-03/I-03** (grab bars, bathroom) · **C-06/B-08** (floor pattern/gloss — AX-BAL precipitants) · **D-10** (glazed edges) · **E-09** (TWSI, tactile info) | Missing item + vestibular/sight | No circulation-handrail item exists; grab bars (G) are bathroom-only. Handrail-with-tactile-info bridges AX-BAL + AX-VIS-N. AX-BAL environmental precipitants are actually controlled in A/B/C (plain, matte, non-glazed-edge floors), so a vestibular-safe corridor is a *cross-category* achievement, not an E-only one. **Create a handrail item (§G).** |
| **Corridor corners / door placement** (§0c edge dimension) | **D-07** (no blind corners) · door swing + latch-side clearance (E-11/I-01/H-04) · **I-02** kitchen · **G-05** work surfaces · closets | Edge geometry governs usable width | At every corner the swept *envelope* (not radius) governs the turn; blind corners (D-07) need curve/mirror; doors opening onto the run consume width and demand latch-side clearance that must not collide with the passing envelope or a corner; kitchens/closets opening off circulation inherit door + reach specs. **Corridor clear width must be assessed with doors, corners, and openings in place, not as an empty tube.** |
| **Vestibular / sight lens on E geometry** | AX-BAL precipitants: **C-03/C-06** (pattern), **B-08** (specular gloss), **D-10** (glazed edges at height), escalators; AX-VIS: **E-09** TWSI, **C-04** LRV, **A-15/A-05** acoustic navigation, handrail tactile info | Re-frames "mobility circulation geometry" | A user with vestibular or sight impairment needs the *same* corridor to also: avoid dizziness precipitants (A/B/C), provide continuous graspable + informational handrails (B.9), a trailing shoreline and TWSI/contrast at decision points (E-09/C-04/K-02), and acoustic navigation cues (A-15). **"Mobility circulation geometry" is mis-named if read as wheels-only** — it is a multi-axis surface; this is the §0e host-surface thesis in concrete form. |

### D.4 Connections and gaps

Connections: CON-0242 (luminance-contrast chain shared with stair-ramp BPC).
Gaps: GAP-019 (ramp SCI, OPEN), GAP-008/011 (I-01 force, cross-cat), GAP-016/023
(E-03 numerics), plus the NEW structural gaps in §A.5.

---

## E. Adversarial protocol pass

Per standing rule #7, for every surviving synthesis claim: confidence interval,
shift conditions, named dissenter, falsification condition.

| Claim | Confidence | Shift conditions | Named dissenter | Falsification |
|---|---|---|---|---|
| Corridor ≥2440 mm primary is best practice (●) | High (two independent ● streams converge) | Rises with value-level extraction of DeafSpace + AWM; drops if extraction shows the streams measured different things | NONE FOUND that argues *narrower* is better for mixed population; over-wide critique exists (VIS shoreline) but addresses ceiling not floor | Overturned if DeafSpace corpus retracted OR AWM swept-path re-analysis yields <2000 mm for entire-sample turn |
| Door manual force ≤30 N (● Brandt) beats ≤20 N (○ code) | High for the anchor, medium for "which number to publish" | Rises if a second empirical force study replicates 94.7 % at 30 N; ≤20 N could re-earn ● only via evidence, not more codes | AU/NO codes assert ≤20 N — but as codes (○), not evidence; not a valid ● dissent | Overturned if Brandt is retracted or a larger study shows 30 N unacceptable to a substantial minority |
| Level entry: AX-WHM direction is ●, not regulatory-only | High | Rises with value-extraction of Al Lawati 45.8 % | The MOB↔VIS contest is a genuine dissent on *universality*, not on the MOB direction | Overturned if Al Lawati/Pavol/Rouvier are shown not to support sub-6 mm for casters |
| Ramp ≤1:20 direction ● (magnitude PENDING) | Medium (GAP-019 open) | Rises to 65–80 % if Lalumière 2022 SR confirms 1:20 in the safe SCI envelope; drops to 20–30 % if the 2.09× figure stays unlocatable | Lalumière PLOS One 2022 SR is the unread primary source | Overturned if the 2022 SR finds safe SCI gradient ≠ 1:20 |
| Rest-seating interval 25–30 m is ○ (not ●) | Deliberately weak | Rises only if a study value-anchors an interval threshold | NONE — but honestly, no code and only clinical inference support any specific interval | Overturned trivially by any building code or study specifying a different max interval |
| TWSI spec deferred pending re-link | N/A (procedural) | — | The Korean advocacy source warns presence≠benefit (maintenance) | — |

**Category-level adversarial challenges (self-directed):**

- *"You are just relabelling code values with markers."* — No: where evidence
  exists (corridor, door force, level entry, rest seating), the ● anchor
  *replaces* the code value as the aspiration and the code is demoted to ○/◐. The
  numbers change (1800→2440; 20→30-or-powered), not just the labels.
- *"You are inflating confidence by citing envelope evidence you haven't
  value-extracted."* — Acknowledged and flagged as Headline Caveat 1 throughout;
  every magnitude is value-level-PENDING and no cell is promoted to `stated`.
- *"Work-from-axes is decorative here."* — Partially fair: `item_axis_links` is
  empty, so the axis mapping is authored from prose. Flagged in §A.5 as a
  required operationalisation.
- *"Deferring TWSI is avoidance."* — It is the honest move: authoring a TWSI spec
  on a slug with zero TWSI evidence would be fabrication-by-proximity. Re-link
  first (§G).

---

## F. Provenance trail

- **Opus authorship**: all synthesis decisions tagged `[OPUS-DECISION
  session_2026-07-23]`. Synthesis routing (PI rule #2 / DR-2026-06-10) satisfied
  — this run is Opus-class.
- **Doctrine SHA**: 0f2f525 (`governance/mission-and-epistemics.md` at authoring).
- **Evidence provenance**: every ● anchor cited by REF-ID resolvable in
  `evidence_sources` with `verification_status=VERIFIED` (exceptions NZS 4121
  UNVERIFIED, RET-08 DISPUTED, noted and not leaned on).
- **Value-level provenance**: DEFERRED — `source_value_extractions` for
  circulation is empty; this run does not assert value-level convergence.
- **Co-1 provenance**: DeafSpace (Bauman/Vaughn/Kusters), Habinteg/RCOT, MLIT,
  Ifop-APF, Invalidiliitto, DSDC — the functional-need anchors; role-appropriate
  authority satisfied.
- **No fabrication**: unverifiable numbers (2.09× handrim; 0.1 m/s RMS; 30 % LRV
  basis) are flagged, not published as fact.

---

## G. Proposed Category E restructuring (OWNER-GATED — proposal only, not executed)

Per CLAUDE.md §5/§9 (structural moves and item relinks are owner-gated; caller
sweep required), the following are **proposals**, staged for owner sign-off. None
is executed in this commit. "None of the Category E specs are sacrosanct" (owner,
2026-07-23) licenses the proposal; governance gates the execution.

1. **Re-link E-07 (Slip Resistance)** from `stair-ramp-threshold-biomechanics`
   (no slip evidence) to `accessible-bathroom-and-grab-bar` / ALL-ROOMS slip
   corpus; coordinate PTV across wet + circulation surfaces (cross-cat with
   G-03/G-04/I-03/B-08).
2. **Re-link E-09 (TWSI/ISO 23599)** from `detectable-gradient-protocol-sensory-zones`
   (no TWSI evidence) to the ISO 23599 / GB 50763 / JIS / NBR 16537 / Korean TWSI
   corpus (currently under VIS/DBL/wayfinding-global-south); then run the B.7
   9-step against the real evidence and log the MOB/PAIN↔VIS contest.
3. **Resolve E-13 ↔ D-suite duplication**: scope E-13 to entrance-only legibility
   or merge into D-02/D-07/D-08/D-10; caller-sweep both categories.
4. **Re-categorise E-15 (Changing Places)** to Category G (bathroom/hoist) — it
   already uses the bathroom slug; caller-sweep references.
5. **Create a circulation handrail item (fills E-14, or a new code)** carrying
   continuity + height + tactile-information handrails, serving AX-BAL + AX-AMB +
   AX-VIS-N (§B.9). Presently there is **no** handrail item anywhere in A–K (only
   bathroom grab bars G-03/I-03); handrails are named across AX-BAL/AX-AMB and the
   stair-ramp/residential-entry BPCs but have no home. Grade honestly as ◐/thin
   and register the evidence gap (AX-BAL is a STUB axis) — do not stamp it ●.
6. **Surface corridor LENGTH/run and MODULATION as explicit parameters** (§0c,
   §B.10) co-located with E-08 (width) and E-10 (rest): rest opportunity ≤25–30 m
   level / ≤10 m graded; sequence/sensory-modulation coordinated with A/B/D/F.
   Corridor is an experiential system, not a cross-section.
7. **Correct the `E-06/MOB` cell** from `regulatory_stratum_only ○` to a ●-direction
   determination for AX-WHM with a CONTESTED flag vs AX-VIS-N (§B.2, §C.3).
8. **Operationalise cells + value extraction**: run the circulation value-level
   extraction pass (populate `source_value_extractions` / `spec_value_probes`),
   then promote the ●-direction parameters with value support to `stated`
   cells via `scripts/emit_data_migration.py` (never a direct DB write). This is
   the gating step for every `stated` promotion.
9. **Populate `item_axis_links`** for Category E from the axis `design_domains`
   so the work-from-axes frame is enforced in data, not only prose.
10. **Update BPC banners**: replace "RETRACTED PENDING REVERIFICATION" on the
   circulation BPCs with a pointer to this reverification once cells land.

Every item above touches items/schema/links and is therefore withheld from this
commit pending owner direction.
