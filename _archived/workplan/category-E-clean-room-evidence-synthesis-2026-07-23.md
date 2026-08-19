# Category-E clean-room evidence synthesis — entrance & circulation domain

**Generated:** 2026-07-23 by `session_2026-07-23-category-e-clean-room-synthesis`
**Status:** PROPOSED — judgment-stage work-product for owner review. **No canonical DB / item-taxonomy
change is made by this document** (propose, don't unilaterally execute — CLAUDE.md §5, §9).
**Doctrine SHA bound:** `0f2f525` (`governance/mission-and-epistemics.md` at HEAD `adbae11`).
**Pipeline anchor:** `governance/pipeline-contract.yaml` — stages `research → collection → judgment →
synthesis → render`.

---

## 0. What this is, and the constraint it was produced under

This is a **clean-room, evidence-first derivation** of the entrance-&-circulation ("category-E")
design parameters and the specifications the current verified evidence base can honestly stand behind.
Per the owner directive for this pass, it was produced **without importing the existing `E-01…E-15`
item definitions or their embedded values** — the parameter set and every claim below are derived
*from the corpus*, and the existing item values are treated only as a reconciliation target in §6, not
as an input to the synthesis.

The governing epistemic constraint (why this is a judgment-stage product and not a finished spec sheet):

> **Category E has a curated, verified source corpus but no value genealogy.** The Progressive-Measurement
> Probe (`spec_value_probes`) and value-extraction (`source_value_extractions`) machinery — the instruments
> that turn a candidate number into a strict-terminated, source-anchored value — have run **only** on the
> A/B acoustic/lighting pilots. **Zero** rows touch category E. Producing resolved numeric specs for E
> right now would require inventing the evidence→value chain, which the doctrine forbids
> (mission-and-epistemics: *"I don't know" > invention*; tier-system §3 *convergence ≠ evidence*;
> tier-system §8 + DR-2026-07-21 Option A: **T4–T6-only claims render only at the weak (○) band**).

So every parameter below is resolved **only to the strength its evidence licenses**: `stated`/● where a
full-band (T1/Co-1/T2/Co-2/T3-clinical) source already anchors it; `provisional`/○ weak-band where the
value is a T4–T6 regulatory convergence; `pending` + gap where the corpus is silent. Numeric resolution
of the ● / mixed cases is explicitly deferred to the PMP/extraction step each parameter names.

---

## 1. Pipeline-stage location of category E (evidence for the claim above)

Derived live from `data/guidebook.db` at HEAD (`adbae11`, `PRAGMA user_version = 30`):

| Stage (pipeline-contract) | Instrument / gate | Category-E status |
|---|---|---|
| research | `spec_value_probes` (PMP, rule #8) | **0 rows** for E (all 31 are A/B: `room-acoustic-performance`, `circadian-lighting-melanopic-edi`, `school-environment-autism`) |
| collection | `evidence_sources` verified + rule-#10 metadata gate | **136 verified source-links (123 distinct sources; 13 shared across slugs)** across the 7 domain slugs (see §3) |
| judgment | `evidence_cell_state` 4-state machine; `source_value_extractions` value-genealogy | **3 of 58** applicable (item×population) cells assessed; **0** extraction rows for E (all 8 are `room-acoustic-performance`) |
| synthesis | `references/bpc-reasoning/<slug>.md`, 9-step, Opus-only | **0** reasoning docs for E |
| render | `site/specs/e-*.html` | honest "not yet computed" banners for all but the 3 assessed cells |

The 3 already-assessed cells (the only prior judgment on this domain):

- `E-08 × DEAF` — `stated`, `CO1+T2`, refs `REF-00338/00339/00342/00343/00344/00345/00347` (DeafSpace corpus).
- `E-12 × MOB` — `stated`, `T1+CO1+T2`, refs incl. `REF-00059` (Steinfeld anthropometry), `REF-00063` (Habinteg).
- `E-06 × MOB` — `provisional`, `regulatory_stratum_only=1`, 15 T4–T6 refs (threshold/level-access codes).

All 7 source BPCs are `evidence_state = RETRACTED-PRE-REHAB` with `pico_complete = 0` — i.e. the
BPC-level synthesis was retracted and not yet rehabilitated. **This is consistent with a curated corpus
that has not been carried through judgment/synthesis**, which is exactly the state this document works from.

---

## 2. Method & guardrails applied

1. **Clean-room clustering.** Sources were grouped by the *design parameter they speak to*, read off
   `evidence_sources` (tier, evidence_type, jurisdiction, title, standard_number, shorthand). The
   resulting parameter set is what the evidence supports; §6 reconciles it against the legacy `E-##`
   list *after the fact*.
2. **Doctrine markers** (`governance/tier-system.md` §5, §8): **●** full band (T1/Co-1/T2/Co-2/T3-clinical);
   **◐** partial (T4/T5 standards basis); **○** weak (T3-grey, T6 code-floor, thin/consensus). Every stated
   specification carries one; unmarked = error.
3. **Convergence-not-evidence wall** (tier-system §3; evidence-architecture I3 as amended by DR-2026-07-21
   Option A): a value whose *entire* basis is T4–T6 code convergence is `provisional` + `regulatory_stratum_only`
   and renders as **weak-band (○) "best practice as currently known,"** flagged code-derived — **never** `stated`,
   **never** above the ○ row. Pipeline-contract `judgment.no-regulatory-stratum-stated` enforces this.
4. **No fabrication.** Where the corpus does not carry a value to a verifiable source, the parameter is
   `pending` + gap. Numeric values are asserted only where a full-band source already anchors them; all
   other numbers are deferred to a named PMP walk / extraction. No DOI/page citation is asserted that was
   not read.
5. **Anti-anchoring honesty note.** I had already seen the legacy `E-01…E-15` titles during initial
   scoping (they embed values such as "PTV ≥36", "≤1:20", "3600 mm"). The derivation below deliberately
   does **not** treat those as evidence; §5 shows several of them are *unsupported by this corpus*, which is
   the check that the clean-room pass was genuine.
6. **No canonical writes.** This document changes no DB row, no item, no attestation, no generated artifact.

---

## 3. Corpus provenance (the raw material)

Verified sources linked via `source_slug_links` (verification_status = VERIFIED). Counts are **per-slug
links** (136 total); there are **123 distinct sources** — 13 are shared across slugs (e.g. DIN 18040-1,
BS 8300-2, ISO 21542, French Arrêté du 8 déc 2014, GB 50763-2012):

| Domain slug | Verified source-links | Tier profile (highlights) |
|---|---|---|
| `accessible-circulation-geometry` | 14 | T2 Russell'19; T3 Roxburgh'24 / Omura'22 (fatigue); T4 EN 81-70; T5 BS 8300-2, DIN 18040-1, BS 6440, NEN 9120; T6 ADA, AS 1428.1, Boverket, Finnish Decree 241/2017, Approved Doc M, MLIT |
| `stair-ramp-threshold-biomechanics-accessibility` | 26 | T2 Rouvier'22 (SR); **T3 clinical cluster** Kim'14, Lawati'17, Ram'24, Harper'25, Simoneau'91, Pavol'01, Wharton'25, Waters'88; T3-grey Manandhar'22; T4 Templer'92; T5/T6 codes |
| `threshold-and-level-access` | 15 | T4 ISO 21542; T5 BS 8300-2, DIN 18040-2, NEN 9120, RHFAC, Inclusive Housing Design Guide; T6 ADA §303, TEK17, NBR 9050, AS 1428.1, draft DIN ≤10 mm, Boverket, MLIT |
| `threshold-door-hardware` | 31 | **T3 clinical** REF-00204 (wheelchair/walker through doors), Putthinoi'17; T4 ISO 21542, EN 17210; large T5/T6 code set (ADA §404, AS 1428.1, ICC A117.1, CSA B651, TEK17, SIA 500, GB 50763, …) |
| `cognitive-wayfinding-design` | 23 | **T2** Tola'21 (SR), Mostafa/ASPECTSS, EADDAT, Dementia Australia; **T3 clinical cluster** Marquardt'09/'11/'14, van Buuren'22/'25, Wiener'21, Calkins'22, Black'22; T5 national dementia frameworks |
| `detectable-gradient-protocol-sensory-zones` | 6 | T2 Williams'24 (SR); T3 Kaplan'89, Mostafa'14, Beranek'04; T4 ISO 21542 §9, PAS 6463:2022 §6.4 |
| `accessible-bathroom-and-grab-bar` | 21 | **T1** Greene'24, Guay'20, Keall'15, BATH-OUT'19, suction-cup'25; **Co-2** CAOT'24, OTA'25; T3 grab-bar grasp'25; T5/T6 codes |

**Directly usable value-content in the corpus** is confined to what verified source *metadata* already
records (e.g. threshold titles literally read "Threshold ≤20mm — NEN 9120:2025", "≤25mm TEK17",
"≤35mm at 1:8 AS 1428.1 retrofit", "draft ≤10mm DIN 18040-2:2023"). Those are code-convergence values →
weak-band ○ only (§4, P-05). Full-band numeric values are **not** yet extracted (that is the missing
`source_value_extractions` step).

---

## 4. Clean-room parameter derivation (the specifications)

Working IDs `CE-P##` are **provisional clean-room labels**, not item codes — deliberately *not* the
legacy `E-##` codes (mapping deferred to §6 / owner). For each: the evidence cluster, the doctrine
evidence-state the corpus licenses today, and the specific value-genealogy step owed.

### CE-P01 — Passenger-lift provision & car dimensions (between-storey vertical circulation)
- **Evidence:** EN 81-70:2021+A1:2022 (T4, REF-00421); code convergence ADA, AS 1428.1, BS 8300-2,
  DIN 18040-1, Approved Doc M, Boverket, NEN 9120, Finnish Decree (T5/T6). **No** T1/Co-1/T2 source
  anchors a car dimension.
- **Doctrine state:** `provisional` · **○ weak-band** · `regulatory_stratum_only`. The ~1100×1400 mm car
  (EN 81-70 Type 2) is a **T4–T6 convergence**, not adjudicated evidence.
- **Owed:** extraction of the exact EN 81-70 clause value; render strictly as weak-band "code baseline".
  Full-band elevation would require primary evidence on the wheeled-mobility envelope inside a car (none in corpus).

### CE-P02 — Alternative lifting where a full lift is infeasible (platform / vertical lifting platform)
- **Evidence:** BS 6440:2011 (T5, REF-00428) only; thin.
- **Doctrine state:** `pending` (leaning ○) — single T5 framework, no primary or convergence base.
- **Owed:** gap registration; multilingual code sweep before any determination.

### CE-P03 — Ramp gradient (sloped between-level access)
- **Evidence:** **T3 clinical** Kim 2014 (REF-00030, ramp slope × height × pushing-force: performance,
  muscle activity, subjective rating), Waters 1988 (REF-00385, energy-speed of gait); **T2 SR** Rouvier
  2022 (REF-00037, manual-wheelchair biomechanics over barriers). Fatigue/temporal angle: Roxburgh 2024
  (ME/CFS), Omura 2022 (energy conservation). Codes give the floor (TEK17 §12-16, DIN, ADA).
- **Doctrine state:** parameter is **●-capable** (primary biomechanics + SR exist) but the *value* is
  **unresolved**. `GAP-019` is **OPEN**: the legacy 1:20 rests on a single study for general wheelchair
  users — do **not** inherit it. Current honest state: `provisional`, value-pending.
- **Owed:** a **PMP walk** on gradient (per population MOB / SCI / PAIN-fatigue) anchored on Kim'14 +
  Rouvier'22; resolve whether the biomechanical ceiling supports ≤1:20 or a population-split.

### CE-P04 — Stair safety where steps remain (edge contrast, nosing, tread/riser, handrail)
- **Evidence:** strong **T3 clinical** cluster — Harper 2025 (REF-00395, high-contrast striping ↔
  fall events), Ram 2024 (REF-00394, stair-fall risk lab vs real homes), Simoneau 1991 (REF-00384,
  visual factors in stair descent), Pavol 2001, Wharton 2025; T3-grey Manandhar 2022 (REF-00393,
  luminance-contrast preferences, VIS); T4 Templer 1992 (REF-00383, *The Staircase*).
- **Doctrine state:** **●-capable** (multiple primary studies) — `provisional` pending value extraction.
  Populations: VIS, MOB-ambulant, older adults, DEM.
- **Owed:** extract the contrast/nosing values Harper'25 & Manandhar'22 actually report; PMP walk on
  step-edge luminance contrast. (Qualitative spec — "mark step edges to a measured luminance contrast;
  avoid interstep dimensional variation" — is already ●-supportable.)

### CE-P05 — Entrance threshold upstand / level access (crossing the door line)
- **Evidence — value:** a large **T4–T6 convergence** on a low upstand — ISO 21542 (T4), and codes at
  ≤20 mm (NBR 9050, French Arrêté Art. 4, DIN 18040-2, NEN 9120), ≤25 mm (TEK17), ≤35 mm at 1:8
  retrofit (AS 1428.1), draft ≤10 mm (DIN 18040-2:2023), zero-step principle (MLIT). **Evidence —
  principle:** **T3 clinical** on the *cost of crossing* — Lawati 2017 (REF-00025, manual wheelchair over
  a threshold, momentum method), REF-00204 (wheelchair/walker passing through doors).
- **Doctrine state (split):** the **≤20 mm value** is `provisional` · **○ weak-band** · `regulatory_stratum_only`
  (convergence-not-evidence — this *is* the archetype; matches existing `E-06 × MOB`). The **directional
  principle** ("minimise/eliminate the upstand; zero-step is the target") is **●-directional** on the T3
  biomechanics — but a *direction*, not a resolved number.
- **Owed:** keep the value weak-band ○ + caveat; extract Lawati'17's effort/tip metrics to state the
  principle at full band without laundering the code number into ●.

### CE-P06 — Doorway passage (clear opening width, opening/operating force, automatic operation)
- **Evidence:** **T3 clinical** REF-00204 (experimental wheelchair/walker door passage), Putthinoi 2017
  (REF-00407); T4 ISO 21542, EN 17210; very large T5/T6 code set (ADA §404, AS 1428.1, ICC A117.1,
  CSA B651, TEK17 §12-17, SIA 500, GB 50763 …). Opening-force thread cross-refs `GAP-008`/`GAP-011`
  (≤22 N, ISO 21542 / CSA B651 — code standard, not evidence).
- **Doctrine state:** clear-width & force **values** are `provisional` · **○ weak-band** (regulatory
  convergence) with *partial* T3 biomechanical support that could elevate the *principle* toward ●.
  Automatic-operation provision is mostly code + practice (Greene 2021 "Decoded", REF-00442 → T6/practice, ○).
- **Owed:** extract REF-00204's measured width/force thresholds (candidate ● anchor for the envelope);
  otherwise widths/forces stay weak-band convergence.

### CE-P07 — Route clear width along corridors/passages
- **Evidence:** **full-band, population-specific** — DeafSpace signing envelope: Bauman 2010 (REF-00338,
  Co-1/T1), Vaughn 2018 (REF-00342, T1), Bauman 2014 (REF-00343, T2), Kusters 2015 (REF-00345, T1) →
  the **2440 mm** primary-corridor anchor documented in tier-system §3. Wheeled-mobility clearance:
  Steinfeld 2010 (REF-00059, T1). Code floor ~1200–1800 mm (convergence).
- **Doctrine state:** `stated` · **●** for **DEAF** (signing space, 2440 mm — already in DB, CO1+T2).
  MOB via Steinfeld anthropometry is ●-anchorable. The 1200–1800 mm **code floor is weak-band ○** and
  **must not** be labelled "preferred" (tier-system §3 corridor-width worked example — the canonical
  convergence trap).
- **Owed:** value extraction of the Steinfeld MOB clearance; keep DEAF 2440 mm and the code floor in
  separate registers (best practice vs regulatory floor).

### CE-P08 — Manoeuvring / turning space (entrance landing and route)
- **Evidence:** Steinfeld 2010 (REF-00059, T1 anthropometry of wheeled mobility) — already anchors
  `E-12 × MOB` `stated` (T1+CO1+T2); Davies 2021 (REF-00062, Co-1), Habinteg 2024 (REF-00063, Co-1),
  MLIT handbook (REF-00066). Code turning-circle (~1500 mm) is convergence.
- **Doctrine state:** `stated` · **●** for **MOB** (T1 anthropometry + Co-1). Value (turning diameter,
  landing dims) T1-anchored but **not yet extracted to a number in-repo**.
- **Owed:** extract Steinfeld's turning/landing envelope to page/table; that resolves the value at ● without invention.

### CE-P09 — Wayfinding & cognitive legibility of routes and entrances
- **Evidence:** the corpus's **densest ●-band cluster** — **T2** Tola 2021 (REF-00710, SR),
  Mostafa/ASPECTSS (REF-00491), EADDAT (REF-00492), Dementia Australia (REF-00501); **T3 clinical**
  Marquardt 2009/2011/2014, van Buuren 2022/2025 (REF-00301/00488, design criteria + behavioural
  patterns), Wiener 2021, Calkins 2022, Black 2022; national frameworks (Singapore DFN, Seoul, Cerema, Norway).
- **Doctrine state:** **●-supportable** for DEM and AUT/NEU — but the specifications are **qualitative /
  typological** (sight-lines to destinations, distinct landmarks, spatial sequencing, contrast, signage
  legibility, minimised decision points), not single numbers. `provisional` → can reach `stated` as a
  *qualitative* determination once written up per the 9-step (Step 6 supports non-numeric values).
- **Owed:** 9-step reasoning doc capturing the typological spec + population split; this is the parameter
  the legacy single item most under-represents.

### CE-P10 — Multi-sensory redundancy & detectable cueing at hazards/transitions
- **Evidence:** **T2** Williams 2024 (REF-00518, SR, sensory-adaptive environments); **T4** ISO 21542 §9
  (REF-00515, multi-sensory redundancy at hazardous transitions), PAS 6463:2022 §6.4 (REF-00516,
  graduated sensory environments); contrast via Manandhar 2022.
- **Doctrine state:** the **principle** (redundant multi-sensory cueing at hazards) is **●** on the T2 SR;
  any specific tactile-indicator *dimensions* are **◐** (T4 standards basis). **Note:** ISO 23599 (the
  legacy `E-09` anchor) is **not in this corpus** — clean-room, its specifics cannot be asserted here.
- **Owed:** if TWSI dimensions are wanted, source ISO 23599 and extract; else state the redundancy
  principle at ● and mark dimensions pending.

### CE-P11 — Rest opportunities along the route (seating at intervals)
- **Evidence:** derived from the **energy-limiting / fatigue** thread — Roxburgh 2024 (REF-00426, ME/CFS
  time diaries), Omura 2022 (REF-00427, energy conservation / minimum steps), Russell 2019 (REF-00053, T2
  adaptations). This is a clean-room *rediscovery*: the parameter falls out of fatigue evidence, not from a
  circulation code.
- **Doctrine state:** `provisional` · ● (T3 clinical) for the *principle* (provide rest points on long
  routes for fatigue/PAIN/energy-limited users); the **interval value** is unresolved.
- **Owed:** PMP/extraction on rest-interval spacing (no in-corpus number yet — do **not** invent one).

### CE-P12 — Grab-bar / transfer support *(surfaced by the corpus but likely out-of-scope for entrance/circulation)*
- **Evidence:** the corpus's **strongest** cluster — **T1** Greene 2024 (REF-00368, wall vs rim grab-bar
  biomechanics + preference), Guay 2020 (REF-00371), Keall 2015 (REF-00373, HIPI falls), BATH-OUT 2019
  (REF-00374, lived experience); **Co-2** CAOT 2024 (REF-00057), OTA 2025 (REF-00380).
- **Doctrine state:** **●, `stated`-capable** on multiple T1 + Co-2. **But** it enters via the
  `accessible-bathroom-and-grab-bar` slug and is a *sanitary/transfer* parameter, not entrance-circulation.
- **Owed:** a **scoping decision (owner, DG-NON adjacent)** — does grab-bar/transfer belong to category E
  or to a bathroom/sanitary category? Flagged, not resolved here. Included to show the clean-room pass did
  not silently drop the corpus's best-evidenced material to fit the legacy category boundary.

---

## 5. Legacy `E-##` values the corpus does NOT support → honest `pending` + gap

The clean-room pass is only credible if it also reports what it *cannot* substantiate. These legacy
category-E specifications have **no supporting source in the verified corpus**; under doctrine they are
`pending` (`[BEST-PRACTICE-PENDING]` + gap), not assertions:

| Legacy value (embedded in item title) | Corpus support | Honest state |
|---|---|---|
| Slip resistance **PTV ≥36 wet** (`E-07`) | **none** — no pendulum-test / PTV source in corpus (cf. `GAP-028`, PTV 36 unannotated) | `pending` + register gap |
| Weather-protection **canopy 3000×2000 mm** (`E-05`) | **none** — no weather-protection source | `pending` + register gap |
| Accessible **parking 3600 mm** (`E-04`) | **none** — no parking-geometry source in corpus | `pending` + register gap |
| **Changing Places** facility (`E-15`) | **none** — no CP-specific source in corpus | `pending` + register gap |
| **TWSI per ISO 23599** (`E-09`) | ISO 23599 not in corpus; only ISO 21542 §9 / PAS 6463 (redundancy principle) | value `pending`; principle ● (see CE-P10) |

This is the substantive payoff of *not* referring to the existing items: four legacy numeric specs turn
out to be floating free of the evidence base, and would have been silently ratified by an
edit-the-existing-spec approach.

---

## 6. Evidence-state summary (what the corpus licenses today)

| Clean-room parameter | Best available band | Determination the corpus licenses now | Value status |
|---|---|---|---|
| CE-P07 Route width (DEAF signing) | ● | `stated` (in DB) | 2440 mm anchored (extract to page) |
| CE-P08 Manoeuvring space (MOB) | ● | `stated` (in DB) | T1-anchored, extract value |
| CE-P04 Stair-edge contrast / fall-safety | ● | `provisional` → ● on write-up | extract contrast/nosing |
| CE-P09 Cognitive wayfinding (DEM/AUT) | ● | `provisional` → `stated` (qualitative) | typological, non-numeric |
| CE-P03 Ramp gradient | ● | `provisional` (value-pending; GAP-019 open) | PMP walk owed |
| CE-P11 Rest interval | ● (principle) | `provisional` | interval unresolved |
| CE-P10 Multi-sensory redundancy | ● principle / ◐ dims | `provisional` | dims pending |
| CE-P05 Threshold ≤20 mm | ○ weak-band | `provisional` · regulatory_stratum_only (in DB: E-06) | code convergence only |
| CE-P06 Door clear-width / force | ○ weak-band (+T3 partial) | `provisional` | convergence + extract REF-00204 |
| CE-P01 Lift car dims | ○ weak-band | `provisional` · regulatory_stratum_only | EN 81-70 convergence |
| CE-P02 Platform lift | ○ / thin | `pending` | thin |
| CE-P12 Grab-bar/transfer | ● (T1+Co-2) | out-of-scope flag → owner | scoping decision |
| Slip / canopy / parking / CP / TWSI-dims | — | `pending` + gap (§5) | corpus silent |

---

## 7. Remaining stage-work to reach finished specifications (the honest to-do)

None of the following is executed by this document; it is the ordered path from here:

1. **Judgment — value extraction (`source_value_extractions`).** Extract per-parameter values from the
   verified sources (page/table anchors), starting with the ● anchors (Steinfeld P07/P08; Harper/Manandhar
   P04; Kim/Rouvier P03) and the code convergences (P05/P06/P01 as weak-band). *Requires a DB migration
   via `scripts/emit_data_migration.py` — owner go-ahead requested before any canonical write.*
2. **Research — PMP walks** (`spec_value_probes`) for the numeric ● parameters (P03 gradient, P04 contrast,
   P11 interval) to strict-terminate an empirical ceiling rather than assert a number.
3. **Judgment — cell determinations** for the 55 unassessed E cells, applying
   `validate_evidence_state.py` gates (governing-refs-nonempty; no-regulatory-stratum-stated;
   tier3-alone-threshold).
4. **Synthesis — 9-step reasoning docs** (`references/bpc-reasoning/<slug>.md`, Opus-authored, validated by
   `scripts/validate_reasoning.py`) per slug.
5. **B-before-E gate:** the source corpus is verified, but the BPCs are `RETRACTED-PRE-REHAB`; confirm
   Phase-B closure per slug before Phase-E rewrite (workplan `bpc-rewrite-workplan-2026-05-11.md`).
6. **Render** (`scripts/generate/*`) once cells carry resolved determinations.

**Owner-gated / DG-NON-adjacent decisions surfaced (propose, don't execute):**
- Whether the clean-room parameter set (§4) **redefines the category-E item taxonomy** (renaming/removing
  item codes → structural change requiring a caller sweep, CLAUDE.md §0 rule 5 + architecture
  `<migration_and_growth>`).
- The **grab-bar/transfer scoping** question (CE-P12).
- Retirement/repair of the four **corpus-silent legacy values** (§5).

---

## 8. Adherence log (cross-stage contract, `pipeline-contract.yaml` `cross_stage.adherence-log`)

**Stage boundaries touched:** collection → judgment (read-only assessment); synthesis **not** entered
(no reasoning doc authored, no value asserted beyond existing DB anchors).

| Rule (stable id) | Fired? | Evidence |
|---|---|---|
| convergence-not-evidence (tier-system §3) | FIRED | P01/P05/P06 held to ○ weak-band; §5 refuses corpus-silent values |
| no-regulatory-stratum-stated (evidence-arch I3 / DR-2026-07-21) | FIRED | P05 kept `provisional`+regulatory_stratum_only, not `stated` |
| weighted-strength band assignment (tier-system §8) | FIRED | every parameter carries an explicit ●/◐/○ band |
| citation discipline (no unverified quant) | FIRED | no numeric value asserted without a full-band anchor or explicit weak-band/pending label |
| Opus synthesis floor (rule #2 / DR-2026-06-10) | SKIPPED | synthesis stage not entered; this is judgment-stage staging authored Opus-class |
| no-canonical-write (CLAUDE.md §4) | FIRED | zero DB / item / attestation / generated-artifact mutation |
| owner-gating (CLAUDE.md §5) | FIRED | taxonomy, scoping, retirements surfaced in §7 as proposals, not executed |

**bias_direction:** This pass is biased toward *under-claiming* — it resolves numbers only where a
full-band source already anchors them and pushes everything else to weak-band or pending. The risk that
direction creates is **omission**: a genuinely well-evidenced value could be sitting extractable in a
source I read only at metadata level (e.g. Steinfeld's exact clearances, Harper's contrast ratio), and by
deferring to the extraction step I may make the corpus look thinner than it is. I did not over-extract to
avoid that appearance, because inventing a page-anchored number would be the worse error under doctrine.

**independent_reviewer_counterclaim:** A skeptical reviewer could argue this document *over*-honors the
convergence-not-evidence wall — that when ISO 21542, ADA, DIN, TEK17, NBR 9050, BS 8300-2 and MLIT all
independently land near a ≤20 mm threshold or an 1100×1400 car, treating that as merely "○ weak-band" and
refusing to call it best practice is itself a defensible-but-contestable doctrinal choice, and a different
project could reasonably read strong multi-jurisdiction convergence as ◐. The rebuttal is that this is
*settled doctrine here* (DR-2026-07-20, DR-2026-07-21 Option A: T4–T6-only → ○), so the weak-band call is
correct *for this repo* — but the counterclaim correctly identifies that the strength of P01/P05/P06 is
doctrine-dependent, not evidence-independent, and would flip if the owner ever revisited the anchor model.

---

*Derived live from `data/guidebook.db` @ `adbae11` (`user_version=30`). Every count, ref-id, and state
above is re-derivable from the repo; none is hand-hardcoded from prose. This document asserts no finished
category-E specification value that is not already anchored in a verified full-band source — the rest is
staged, not stated.*
