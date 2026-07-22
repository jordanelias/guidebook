# DR-2026-07-20: The intra-category cross-test — every specification adjudicated against its category-siblings before determination

- Status: **ACCEPTED — owner ratification "Yes, ratify ALL recent work", 2026-07-21; forks X2 (functional-neighbourhood granularity) and X5 (gate strength) accepted as drafted; execution (cross_test_pairs migration + connection-discovery `--mode category-crosstest` + assess_cell ICCT gate) staged per `decisions/RATIFICATION-RECORD-2026-07-21.md` §Addendum.** Authored on owner directive 2026-07-20 ("ensure that our work in deriving best practices includes a step whereby every item/specification within a category gets tested against the other items in that same category… considering these items beyond script prescription / silos by title / too-specific topics").
- Date: 2026-07-20
- Prepared by: Claude. Grounded in the corridor-width value genealogy (`references/methodology/value-genealogy-worked-example-corridor-width.md`), the swept-path / manoeuvring-footprint methodology (`references/bpc/frameworks-and-methodology/manoeuvring-footprint-vs-turning-radius-methodology.md`), the live determination engine (`evidence_cell_state`, 13 pilot cells), and the connection register (`connections`, 273 rows / 507 targets).
- Affects (if ratified): one follow-on migration (a `cross_test_pairs` worklist table + `v_cross_test_open` view); `skills/connection-discovery_SKILL.md` (gains `--mode category-crosstest`); `scripts/assess/assess_cell.py` (post-ratification: an ICCT gate in the `stated` predicate, under a new `rule_version`); `workplan/best-practices-assessment-system.md` §3 (the determination algorithm gains a cross-item step); companion demonstration `references/methodology/intra-category-cross-test-methodology.md`.
- Related: DR-2026-07-13-value-genealogy-and-derivation-handshake (ACCEPTED — this DR is the missing **inter-item** level above H1's intra-cell root counting and H2's derivation-path counting); DR-2026-07-20-weighted-strength-anchor-model; `governance/tier-system.md` §3 (convergence-not-evidence) + §8 (weighted-strength bands); `governance/armature_v4_resolutions.md` (compound-interaction surfacing); `governance/mission-and-epistemics.md` §4 + doctrine #3; project-standards conflict-resolution-at-Population-Mode rule.

---

## Context — the engine adjudicates cells in isolation; the corridor case proves that isn't enough

The best-practices assessment engine (`workplan/best-practices-assessment-system.md`; live in `evidence_cell_state`) assesses each **cell = (item_code × population × design_scale)** on its own evidence. DR-2026-07-13 H1 counts *roots, paradigms and device-classes within a cell*; H2 counts *derivation paths into a cell*. Both look **inward**. Nothing in the pipeline requires a determination to be tested against the **other items in its own category** before it ships.

The corridor-width worked example is the proof that inward-only adjudication is insufficient. E-08's correct determination did not emerge from E-08's own evidence — it emerged from testing E-08 **against neighbouring specifications and functional programs**:

- **Subsumption** — 2440 mm signing width ⊃ 1800 mm passing width (CON-0122, HIGH; "a designer specifying MOB-only silently deletes DEAF signing space"). The wider sibling silently satisfies *or* silently deletes the narrower's function; neither fact is visible from either cell alone.
- **Geometric interaction** — rest seating must be recessed **≥200 mm off the clear width** so it never subtracts from passing space (Co-2 root; worked example §5, OFS/PAIN row). E-08's usable value is a *joint* function of E-08 and the seating item; assessed alone, either is wrong.
- **Variable-conflation dissolution** — the once-live "CORRIDOR-W" conflict was **retired 2026-03-30**: "Width and sensory load are independent variables… no study shows wide corridors harm" (worked example §5, AUT/SENS/NDV row). A phantom conflict between two differently-titled strands dissolved once each side's physical variable was named.
- **Shared element, distinct program** — the same physical width serves signing (DEAF), passing (MOB/SCI), and linked travel (VIS/DBL/DEM), each with its own evidence stream and grain (worked example §4).

That cross-item reasoning was done **by hand**. The connection register captures fragments of it — CON-0122 is exactly a subsumption verdict — but **opportunistically and untyped**: `connection-discovery` fires on new-item / new-mining triggers, `spec` mode reads author-declared cross-reference tables (inheriting the very title-silos the owner names), and `connection_type` is NULL on every migrated row. **Coverage is non-exhaustive and title-driven.** A determination can therefore reach `stated` having never been tested against a category-sibling that subsumes it, interacts with it, or is in fact the same variable under a different title.

This is the **item-level analogue of the measurement-paradigm error** the swept-path methodology corrected. Reading corridor width as a title-siloed "width" number — rather than as a swept-path envelope interacting with everything that moves through and sits beside it — is the same failure as reading item E-08 as its heading rather than as one member of a coupled category. The owner's directive generalizes the swept-path correction from *within a parameter* to *across a category*.

---

## Proposed decision — the intra-category cross-test (ICCT), a required derivation step

The ICCT is a pass that sits **between extraction (H1) and determination (H2 / assessment §3)** and gates exactly like H4: for every category, every item is adjudicated against every other item in that category before any of its cells can reach `stated`. Six separately ratifiable items.

### X1 — The pass: enumerate every unordered pair, classify each

For each category, enumerate all unordered item pairs `C(n,2)` and record a controlled **relationship verdict** per pair (X3). No pair is skipped; an unexamined pair is a queryable worklist row (X6), never an assumed non-relationship. Enumeration is mechanical; classification is Claude-synthesis validated against schema (the connection-discovery execution pattern).

### X2 — "Category" is a functional neighbourhood, not a title silo  *(flagged judgment call — granularity)*

The pass runs over two partitions and one leakage check:

1. **Item-code category** (A–K) — the enumerable unit the owner named ("items within a category").
2. **Functional/thematic BPC group** (`entrances-and-circulation`, `sensory-environment`, `seating-and-rest`, …) — where physical and movement interactions actually concentrate.
3. **Cross-partition leakage detection** — a *mandatory* check for any pair whose **shared physical element, shared movement/acoustic/air envelope, or shared population** links items across a category or group boundary. This is non-negotiable because a pure within-silo pass would have missed **corridor ↔ rest-alcove** — the very interaction that reframed E-08, and one that crosses `entrances-and-circulation` × `seating-and-rest`.

**Recommendation:** run the primary enumeration on the functional/thematic group (adjacency is where interactions live), carry the letter-category as a coarse secondary partition, and treat leakage detection as a first-class output, not an afterthought. The "category" is defined by what shares a physical event, not by what shares a heading.

### X3 — The verdict vocabulary (generalized from the relationship types the corridor case surfaced), recorded per *(pair × program)*

A verdict is recorded **per (pair × functional program / population lens)**, not once per pair — the same grain as the cell (`item × population`) and the grain the corridor fan-out already used, where one pair reads differently under different populations. This is not optional precision: the acoustic demonstration shows **A-08 (NC-25) × A-18 (RT60)** is `INTERACTS` under speech intelligibility (ALL-ENV.md L91/L169) and `INDEPENDENT` under VIS acoustic wayfinding (VIS.md L23) — both corpus-grounded and opposite. A one-verdict-per-pair rule would suppress one of them, and the natural pick (the citable coupling) would erase a finding the corpus flags as an "Important correction."

`SHARED_ELEMENT_DISTINCT_PROGRAM` is therefore **not a peer verdict** but the **decomposition trigger**: when a pair shares one physical element across distinct programs (one corridor width serving signing / passing / linked travel; one acoustic field serving intelligibility / wayfinding), the pass splits it by program and assigns one of the five atomic verdicts *within each program*:

| Verdict | Meaning | Corridor-case exemplar |
|---|---|---|
| `INDEPENDENT` | Different physical variables sharing an architectural element; recording independence is itself a finding (it forecloses phantom conflicts) | "Width and sensory load are independent variables" (CORRIDOR-W dissolution) |
| `SUBSUMES` / `SUBSUMED_BY` | One spec's requirement geometrically/physically contains another's — the wider silently satisfies *or* deletes the narrower's function | 2440 ⊃ 1800 (CON-0122), under the signing-vs-passing programs |
| `INTERACTS` | One item's value modifies the usable value of another; the pair must be solved jointly | rest seating recessed ≥200 mm off clear width |
| `CONFLATED_VARIABLE` | Two differently-titled items are the same underlying variable named as if commensurable — a merge/rename finding | turning circle vs swept envelope named as one number |
| `GENUINE_CONFLICT` | Competing requirements on the **same** variable and paradigm for overlapping populations — and *only* these are true conflicts | routes to Part 5 / cross-population resolution |

Only `GENUINE_CONFLICT` invokes the conflict-resolution protocol. Distinguishing it from the non-conflict relationships is most of the value: the corridor history shows the project repeatedly mistook subsumption and variable-independence for conflict.

### X4 — Commensurability guards (swept-path faithful), scoped to the value-comparison verdicts

The guard governs the verdicts that **compare values** — `CONFLATED_VARIABLE` (are these two the *same* value?) and `GENUINE_CONFLICT` (are these two *competing* values?). For those, a pair is read **only within `measurement_paradigm` and within `device_class` / functional class** (the DR-2026-07-13 H1 fields): a cross-paradigm or cross-class pairing is recorded as a **derivation** (down-weighted, its transfer named), **never as an identity**, and **can never register `CONFLATED_VARIABLE` or `GENUINE_CONFLICT`** — a static turning circle cannot contradict a swept envelope. This imports the corridor doctrine verbatim: *"values are commensurable only within a measurement paradigm."*

`INTERACTS` and `SUBSUMES` are **not** value comparisons — they are causal or geometric relations *between different quantities* (NC-25 background noise and an RT60 target are not one number; absorption in sabins and reverberation in seconds are a cause and its effect). They are checked for **dimensional/physical consistency** (does the mechanism connect these two quantities?), not for value-commensurability. Treating a causal `INTERACTS` pair as "paradigm-commensurable" is a category error — the guard simply does not apply to it.

### X5 — Gate semantics  *(flagged judgment call — gate strength)*

**Recommendation (hard gate, H4-shaped):** a cell cannot reach `stated` until every pair in which its item participates carries a recorded ICCT verdict. Rationale: an unexamined `SUBSUMES` or `INTERACTS` pair can silently invalidate the cell's value (the DEAF-deletion / alcove-subtraction failure modes). A cell whose ICCT pass is incomplete sits at `provisional` with an `icct_incomplete` flag, exactly as H4 holds cells at `provisional` until a triggered check resolves. **Deadlock discipline (per H4):** the gate binds only where the pass has actually run for the category; it never silently pretends coverage, and a `GENUINE_CONFLICT` verdict routes to the named resolver (Part 5 / evidence-auditor at Population Mode) rather than pinning the cell indefinitely.

**Weaker alternative:** advisory enrichment only — ICCT verdicts populate the connection register and surface to the reader, but do not gate `stated`. This is cheaper and non-blocking but re-admits exactly the silent-invalidation the corridor case warns against.

### X6 — Output is worklist rows, not prose (mirrors H5's engine-driven gap-filling)

Enumeration writes one row per *(unordered pair × program)* into a `cross_test_pairs` worklist table (`item_a`, `item_b`, `category`, `partition`, `program`, `verdict`, `commensurability_gate` — `pass` / `fail` / `n/a-causal`, `rationale`, `spawned_con_id`, `spawned_gap_id`, `spawned_conflict_id`, provenance). The `program` column is what lets A-08 × A-18 hold `INTERACTS` and `INDEPENDENT` rows at once; a pair with a single program collapses to one row. Downstream:

- `SUBSUMES` / `INTERACTS` → a typed `connections` row (reuse the 273-row register; finally populate `connection_type`).
- `CONFLATED_VARIABLE` → a merge/rename finding (gap or decision item).
- `GENUINE_CONFLICT` → a conflict-register entry routed to Population-Mode resolution.
- Unexamined pair → an open `cross_test_pairs` row surfaced by `v_cross_test_open` — the pass's live "what we owe," identical in spirit to `v_pending`.

---

## Where this sits across the three design modes (and the readiness question)

The engine computes at **Universal** and **Population** scale; **Person Mode is not an engine determination** — it is OT co-design resolving a value within the Population-Mode range (mission §4; project-standards range doctrine). The ICCT respects that split:

- **Universal Mode** — the cross-test raises the code floor's *coherence*: sibling specs that subsume or interact must be reconciled so the universal set is internally consistent (an acoustic panel spec that can't deliver the stated RT60 is an incoherent floor).
- **Population Mode** — where the ICCT does its substantive work, exactly as source-ranking does (mission §107). Subsumption, interaction and variable-conflation are adjudicated here; `GENUINE_CONFLICT` routes to Part-5 cross-population resolution, **Population Mode only** (project-standards).
- **Person Mode** — the ICCT computes no value. The `INTERACTS` / `SUBSUMES` / `GENUINE_CONFLICT` pairs it surfaces become the **OT co-design inputs** (armature compound-interaction surfacing, `armature_v4_resolutions.md`) — never an override of co-design.

So, on readiness: the *method* for cross-mode best-practice adjudication is ratified (DR-2026-07-13) and demonstrated on the hardest cell (E-08); the *substrate* is live (genealogy fields + `v_value_independence`; the determination engine has produced its first 13 cells across Universal and Population scale). We can begin — and have. The ICCT is the **missing required step** that makes "begin" safe to scale: without it, corpus-wide determination would ship title-siloed cells at exactly the moment the engine turns 13 hand-checked cells into ~1,800 machine-checked ones.

---

## What this extends (and deliberately does not do)

Extends without contradiction: **DR-2026-07-13** (its `measurement_paradigm` / `device_class` fields are the ICCT's commensurability inputs; ICCT is the inter-item level its intra-cell and derivation-path counting implied but did not build); **connection-discovery** (the ICCT is the exhaustive, non-opportunistic pass the register always wanted — and the first population of `connection_type`); **tier-system §3/§8** (subsumption and independence are how convergence-not-evidence and the weighted-strength bands play out *between* items); **mission doctrine #3** (convergence-as-evidence, now also across sibling specifications); **project-standards** (conflict resolution at Population Mode).

Deliberately does **not**: compute at Person Mode (co-design is not an engine output); auto-merge `CONFLATED_VARIABLE` pairs (a merge is a decision, surfaced not executed); or treat cross-reference tables as ground truth (they are an input to the pass, not a substitute for it — that is the silo being dismantled).

---

## Consequences if ratified

One follow-on migration (the `cross_test_pairs` table + `v_cross_test_open`; can ride the next data migration). The pilot's 13 cells get their first ICCT pass — the acoustic cluster A-02 / A-06 / A-08 / A-18 (all four already share `bpc_source_slug=room-acoustic-performance` yet carry **zero registered connections among them** — direct evidence that the opportunistic register leaves intra-BPC couplings untyped; demonstrated in the companion methodology doc, where A-08 × A-18 resolves to opposite verdicts by program), the corridor pair E-08 × E-12 (power-wheelchair manoeuvring envelope; E-06 level-entry is largely width-independent and is a control, not a coupling), and G-03. `connection-discovery` gains `--mode category-crosstest`; `assess_cell.py` gains the X5 gate under a new `rule_version`. The corridor worked example is retro-designated the ICCT **acceptance test at the inter-item level**: its subsumption, alcove-interaction, and variable-independence findings must reproduce as `cross_test_pairs` rows with the corresponding verdicts, per program.

---

## Flagged judgment calls (owner attention)

1. **X2 — category granularity.** Recommendation: functional/thematic group as the primary partition, letter-category secondary, cross-partition leakage mandatory. The alternative (letter-category only, literal reading of the directive) is enumerable but would silo out corridor ↔ alcove.
2. **X5 — gate strength.** Recommendation: hard gate (no `stated` until the item's pairs are examined), H4-shaped. The alternative (advisory only) is non-blocking but re-admits silent invalidation.

Both are named here rather than inherited silently, per the DR-2026-07-13 precedent for flagging the dignity/architecture judgment calls the owner should rule on explicitly.

## Revision history

- v1 (2026-07-20): initial proposal on owner directive.
- v2 (2026-07-20) — adversarial-review corrections (self-review + corpus verification against the acoustic cluster): **the verdict grain is now per *(pair × program)*, not one-per-pair** — falsified by A-08 (NC-25) × A-18 (RT60), which is `INTERACTS` under speech intelligibility (ALL-ENV.md L91/L169) and `INDEPENDENT` under VIS acoustic wayfinding (VIS.md L23), both corpus-grounded; the v1 rule also contradicted this DR's own acceptance test (the corridor fan-out records per-population verdicts). `SHARED_ELEMENT_DISTINCT_PROGRAM` demoted from peer verdict to **decomposition trigger** (resolving its overlap with `SUBSUMES` on the corridor case). **X4 commensurability guard scoped** to the value-comparison verdicts only (`CONFLATED_VARIABLE`/`GENUINE_CONFLICT`); `INTERACTS`/`SUBSUMES` are causal/geometric relations between different quantities and are checked for dimensional consistency, not value-commensurability — the v1 "paradigm-commensurable" framing of an `INTERACTS` pair was a category error. X6 row grain gains a `program` column. Consequences corrected: the acoustic pilot is A-02/A-06/A-08/A-18 with zero registered inter-connections (positive evidence for the exhaustive pass), and E-06 reclassified as a width-independent control rather than a cluster member.
