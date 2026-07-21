# Intra-category cross-test — worked demonstration: the acoustic cluster (A-02 · A-08 · A-18)

**Status:** OPERATIVE methodology demonstration (companion to `decisions/DR-2026-07-20-intra-category-cross-test.md`, PROPOSED). Authored on owner directive 2026-07-20. This document *demonstrates* the intra-category cross-test (ICCT) on one cluster; like the corridor value-genealogy worked example, **it does not itself change any determination** — its verdicts are recorded as falsifiable predictions binding to their inputs, to be confirmed or overturned by the built pass.

**Why this cluster:** the corridor case demonstrated the ICCT relationships on a *spatial* parameter (swept-path width). This one demonstrates the identical method on an *acoustic* one — three items that read, by title, as three unrelated specifications but are in fact one coupled system. It is the cleanest available proof that "silos by title" and "too-specific topics" (the owner's words) hide the real determination. All three items are already live in `evidence_cell_state`.

---

## 0. The three items, and where the silo actually is

| Item | Name (as written) | `bpc_source_slug` | Pilot cell state |
|---|---|---|---|
| **A-02** | Acoustic Ceiling Panels (NRC ≥0.85) in Occupied Spaces | `room-acoustic-performance` | `provisional` · universal · T4–6-only |
| **A-08** | HVAC Noise Control (NC-25 Maximum in Sensitive Spaces) | `room-acoustic-performance` | `provisional` · universal · T4–6-only |
| **A-18** | RT60 in Occupied Learning and Listening Spaces | `room-acoustic-performance` | `stated`/`provisional` by population (A-18×ALL `stated` T1; ×AUT T3; ×DEAF T1; ×DEM T2) |

The silo is **not** at the topic layer: all three (with A-06, Fabric Wall Panels NRC ≥0.70) already share one `bpc_source_slug`, `room-acoustic-performance` — the corpus *already knows* they are one acoustic BPC. The silo is one layer down, at the **relationship** layer: there are **zero registered `connections` among the four** (verified against the register), and each item's cell is assessed **inward** on its own evidence. So a determination on A-18 can ship without the A-08 background-noise floor being represented in it, and without recording that A-02 is the mechanism that delivers A-18's number — even though all four descend from the same synthesis. That relationship-layer silence is exactly what opportunistic, title-driven connection-discovery leaves behind, and exactly what the ICCT's exhaustive pass fills.

## 1. What the cross-test finds — the pairwise verdicts, per program

Enumerating `C(3,2) = 3` pairs. A verdict is **not one-per-pair**: it is recorded per *(pair × functional program / population lens)* — the same cell grain the engine already uses, and the grain the corridor fan-out already demonstrated (a pair reads differently under different programs). The commensurability guard (X4) is invoked only where a verdict *compares values* (`CONFLATED_VARIABLE`, `GENUINE_CONFLICT`); `INTERACTS` and `SUBSUMES` are causal/geometric relations between **different** quantities, so they are checked for dimensional consistency, not value-commensurability — labelling NRC and RT60 "commensurable" would be a category error.

| Pair | Program / lens | Verdict | Mechanism (the physical event the titles hide) · anchor |
|---|---|---|---|
| **A-02 × A-18** | any listening program | `INTERACTS` (directional A-02 → A-18) | Porous absorption **produces** the reverberation outcome (Sabine: RT60 falls as total absorption rises). Ceiling NRC ≥0.85 (A-02) + fabric panels (A-06, NRC ≥0.70) are named in the corpus as the *technique layer* that delivers the A-18 target (`working/evidence-migration/pilot-A18-rt60/rehab-analysis.md` L78). Assessed alone, A-18 is a target with no delivery path and A-02 a material with no stated purpose. |
| **A-08 × A-18** | **speech intelligibility** (hearing-device / learning) | `INTERACTS` (joint) | Intelligibility depends on **both** reverberation **and** SNR: *"Reverberation above 0.6 sec prevents 100% speech perception even at high SNR… affected by both reduced SNR and reverberation"* (`references/bpc/ALL-ENV.md` L91); the corpus co-specifies RT60 ≤0.3 s **and** background ≤30–35 dB(A) for the same listeners (L169). RT60-alone silently drops the SNR half. |
| **A-08 × A-18** | **VIS acoustic wayfinding** (zone cueing) | `INDEPENDENT` | *"RT60 change… and NC change… are independent acoustic parameters — do not substitute one for the other"* (`references/bpc/VIS.md` L23): a zone boundary may be cued by *either*, non-equivalently. Under this program the very same pair is independent. |
| **A-02 × A-08** | any | `INDEPENDENT` | Sound *absorption* (A-02) and *source noise emission* (A-08) are different physical variables acting on the same room. Recording independence forecloses a phantom "which acoustic spec governs?" conflict — as the corridor case recorded width ⟂ sensory-load. |

**The load-bearing result** — and the finding that most tests the method: **A-08 × A-18 is `INTERACTS` under speech intelligibility and `INDEPENDENT` under VIS wayfinding**, both corpus-grounded, in direct opposition. A one-verdict-per-pair pass would have to pick one and suppress the other — and the natural pick (the citable intelligibility coupling) would erase a VIS finding the corpus explicitly flags as an *"Important correction."* The program-conditioned grain is therefore not a refinement; it is what keeps the pass from manufacturing a false universal. The real object is **one architectural element (the room's acoustic field) carrying distinct functional programs, each with its own pairwise structure** — the acoustic transposition of the corridor's "same width, distinct programs."

## 2. Why this is the swept-path lesson, transposed

The corridor correction was: *corridor width is not a "width" number; it is a swept-path envelope interacting with everything that moves through and sits beside it.* The acoustic correction is identical in shape: *RT60 is not a "reverberation" number; it is one term in an intelligibility relationship coupled to absorption below it and background noise beside it.* In both cases the title is a silo, the real variable is a relationship, and the relationship is only recoverable by testing the item against its category-siblings.

The failure mode the ICCT prevents is also identical. In the corridor case, specifying MOB-only width silently deleted DEAF signing space (CON-0122). Here, specifying A-18 RT60 alone — the most citable, most "stated" of the three — silently ships a room that misses intelligibility because its A-08 noise floor was never adjudicated against it under the intelligibility program. In this cluster the strongest cell is the one most exposed to isolation error, because its citational strength is what makes shipping it alone feel safe.

## 3. What the pass writes (per DR X6)

Predicted `cross_test_pairs` rows for this cluster (falsifiable against the built pass):

```
(A-02, A-18, program=listening,             verdict=INTERACTS,   commensurability_gate=n/a(causal),
   rationale="absorption delivers Sabine RT60; corpus technique-layer link (rehab-analysis L78)",
   spawned_con_id=<new, typed INTERACTS>)
(A-08, A-18, program=speech-intelligibility, verdict=INTERACTS,   commensurability_gate=n/a(causal),
   rationale="intelligibility = f(RT60, SNR); NC-25 sets noise floor (ALL-ENV L91/L169)",
   spawned_con_id=<new, typed INTERACTS>)
(A-08, A-18, program=VIS-acoustic-wayfinding, verdict=INDEPENDENT,
   rationale="RT60 vs NC non-substitutable zone cues (VIS.md L23)")     -- SAME pair, opposite verdict
(A-02, A-08, program=any,                    verdict=INDEPENDENT,
   rationale="absorption vs source emission — distinct variables; forecloses phantom conflict")
```

Note the two A-08 × A-18 rows: the worklist carries one row per *(pair × program)*, not one per pair, so the intelligibility-`INTERACTS` and wayfinding-`INDEPENDENT` readings coexist instead of one overwriting the other. `commensurability_gate` fires only for value-comparison verdicts (`CONFLATED_VARIABLE` / `GENUINE_CONFLICT`); on causal/geometric verdicts it is `n/a`, which is why no `paradigm_commensurable` flag appears on the `INTERACTS` rows.

Under the recommended hard gate (DR X5): A-18's `stated` determinations **hold** — its participating pairs are now examined and recorded — but each carries the coupled-cell link, so a reader (or a downstream OT at Person Mode) sees that the RT60 target presupposes an A-02-class provision and, under an intelligibility program, an A-08 noise floor. A-18 assessed *before* the ICCT ran would have sat at `provisional` with `icct_incomplete` until these pairs were adjudicated.

## 4. Three-mode reading of the cluster

- **Universal Mode:** the three specs must be internally coherent — a universal RT60 floor that no universal absorption provision can deliver is an incoherent floor. The ICCT makes the coherence checkable.
- **Population Mode:** the coupling is where the substantive adjudication happens. A-18×DEAF and A-18×AUT carry different RT60 targets (DEAF `stated` T1; AUT `provisional` T3); the A-08 noise floor interacts with each differently (auditory-processing populations need a larger SNR margin). The `INTERACTS` verdict is what forces the per-population joint solve instead of a single room number.
- **Person Mode:** no engine value. The two `INTERACTS` pairs become OT co-design inputs — "this person's intelligibility target sets a joint constraint on reverberation *and* background noise; resolve both together" — never an override of the individual's assessed need.

## 5. Generalization — the pass over the rest of category A and beyond

These verdict types recur across the corpus and are exactly what the register has been recording ad hoc and untyped: CON-0122 (`SUBSUMES`, corridor), the alcove rule (`INTERACTS`, circulation × seating), the CORRIDOR-W retirement (`INDEPENDENT`, width × sensory load). The ICCT's contribution is to make the pass **exhaustive** (every pair, not the pairs an author happened to cross-reference), **typed** (a controlled verdict, not free-text folklore), and **program-resolved** (a verdict per program, so a pair that is `INTERACTS` for one population and `INDEPENDENT` for another — A-08 × A-18 — records both), so that no determination — least of all a strong one — ships having been read as its title rather than as a program-situated member of its category.

---

## Changelog

- 2026-07-20 v1: initial demonstration, companion to DR-2026-07-20-intra-category-cross-test.
- 2026-07-20 v2 — adversarial-review corrections (self-review + corpus verification): the A-08 × A-18 pair split into its two corpus-grounded, opposite verdicts — `INTERACTS` under speech intelligibility (ALL-ENV.md L91/L169) and `INDEPENDENT` under VIS acoustic wayfinding (VIS.md L23) — falsifying the v1 single-verdict-per-pair reading and re-grounding the demo on the *(pair × program)* grain the corridor fan-out already used; the "paradigm-commensurable, X4 satisfied" line removed as a category error (commensurability gates value-comparison verdicts only, not causal `INTERACTS`/`SUBSUMES`); §0 reframed — the four items already share `bpc_source_slug=room-acoustic-performance`, so the silo is at the relationship layer (zero registered connections among them), not the topic layer; the "most evidence-rich cell is most dangerous" claim scoped to this cluster rather than asserted as a universal.
