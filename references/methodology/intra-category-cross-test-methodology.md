# Intra-category cross-test — worked demonstration: the acoustic cluster (A-02 · A-08 · A-18)

**Status:** OPERATIVE methodology demonstration (companion to `decisions/DR-2026-07-20-intra-category-cross-test.md`, PROPOSED). Authored on owner directive 2026-07-20. This document *demonstrates* the intra-category cross-test (ICCT) on one cluster; like the corridor value-genealogy worked example, **it does not itself change any determination** — its verdicts are recorded as falsifiable predictions binding to their inputs, to be confirmed or overturned by the built pass.

**Why this cluster:** the corridor case demonstrated the ICCT relationships on a *spatial* parameter (swept-path width). This one demonstrates the identical method on an *acoustic* one — three items that read, by title, as three unrelated specifications but are in fact one coupled system. It is the cleanest available proof that "silos by title" and "too-specific topics" (the owner's words) hide the real determination. All three items are already live in `evidence_cell_state`.

---

## 0. The three items, as their titles present them

| Item | Name (as written) | Pilot cell state |
|---|---|---|
| **A-02** | Acoustic Ceiling Panels (NRC ≥0.85) in Occupied Spaces | `provisional` · universal · T4–6-only |
| **A-08** | HVAC Noise Control (NC-25 Maximum in Sensitive Spaces) | `provisional` · universal · T4–6-only |
| **A-18** | RT60 in Occupied Learning and Listening Spaces | `stated`/`provisional` by population (A-18×ALL `stated` T1; ×AUT T3; ×DEAF T1; ×DEM T2) |

Read as titles, these are a *material spec*, a *mechanical-systems spec*, and a *room-acoustics metric* — three topics, three chapters, three silos. A determination engine assessing each cell inward would anchor each on its own evidence and ship three independent numbers.

## 1. What the cross-test finds — the pairwise verdicts

Enumerating `C(3,2) = 3` pairs, within the acoustic measurement paradigm (all three are `instrumented_physical_measurement`, so all three pairs are paradigm-commensurable — X4 satisfied, no cross-paradigm derivation needed):

| Pair | Verdict | Mechanism (the physical event the titles hide) |
|---|---|---|
| **A-02 × A-18** | `INTERACTS` (directional: A-02 → A-18) | Porous absorption **produces** the reverberation outcome. RT60 ∝ V/(S·ᾱ) (Sabine); ceiling NRC ≥0.85 (A-02) plus fabric panels (A-06, NRC ≥0.70) are named in the corpus as the *technique layer* that delivers the A-18 target (`working/evidence-migration/pilot-A18-rt60/rehab-analysis.md` L78). A-18's value is not achievable without an A-02-class provision; assessed alone, A-18 is a target with no delivery path and A-02 is a material with no stated purpose. |
| **A-08 × A-18** | `INTERACTS` (joint) | Speech intelligibility is a function of **both** reverberation (A-18) **and** signal-to-noise ratio, whose noise floor is the HVAC background (A-08, NC-25). A short RT60 over a noisy floor and a quiet floor with long RT60 both fail intelligibility; the two must be solved jointly. They are **not** commensurable as one number (X4) — treating "the acoustic spec" as RT60-alone silently drops the SNR half. |
| **A-02 × A-08** | `INDEPENDENT` | Sound *absorption* (A-02) and *source noise emission* (A-08) are different physical variables acting on the same room. Recording independence is itself the finding: it forecloses a phantom "which acoustic spec governs?" conflict, exactly as the corridor case recorded width ⟂ sensory-load. |

**The one-line result:** the real object is not three specs but **one functional program — speech intelligibility in an occupied room — delivered by a coupled triple** (absorption sets RT60; RT60 and the HVAC noise floor jointly set intelligibility). None of that is visible from any single title, and an inward-only engine would never surface it.

## 2. Why this is the swept-path lesson, transposed

The corridor correction was: *corridor width is not a "width" number; it is a swept-path envelope interacting with everything that moves through and sits beside it.* The acoustic correction is identical in shape: *RT60 is not a "reverberation" number; it is one term in an intelligibility relationship coupled to absorption below it and background noise beside it.* In both cases the title is a silo, the real variable is a relationship, and the relationship is only recoverable by testing the item against its category-siblings.

The failure mode the ICCT prevents is also identical. In the corridor case, specifying MOB-only width silently deleted DEAF signing space (CON-0122). Here, specifying A-18 RT60 alone — the most citable, most "stated" of the three — silently ships a room that misses intelligibility because its A-08 noise floor was never adjudicated against it. **The most evidence-rich cell in a cluster is the one most dangerous to determine in isolation**, because its strength masks the coupling.

## 3. What the pass writes (per DR X6)

Predicted `cross_test_pairs` rows for this cluster (falsifiable against the built pass):

```
(A-02, A-18, category=A, partition=sensory-environment, verdict=INTERACTS,
   paradigm_commensurable=1, class_commensurable=1,
   rationale="absorption delivers Sabine RT60; corpus technique-layer link",
   spawned_con_id=<new, typed INTERACTS>)
(A-08, A-18, category=A, partition=sensory-environment, verdict=INTERACTS,
   paradigm_commensurable=1, class_commensurable=1,
   rationale="intelligibility = f(RT60, SNR); NC-25 sets the noise floor",
   spawned_con_id=<new, typed INTERACTS>)
(A-02, A-08, category=A, partition=sensory-environment, verdict=INDEPENDENT,
   paradigm_commensurable=1, class_commensurable=1,
   rationale="absorption vs source emission — distinct variables; forecloses phantom conflict")
```

Under the recommended hard gate (DR X5): A-18's `stated` determinations **hold** — both its `INTERACTS` pairs are now examined and recorded — but each carries the coupled-cell link, so a reader (or a downstream OT at Person Mode) sees that the RT60 target presupposes an A-02-class provision and an A-08 noise floor. A-18 assessed *before* the ICCT ran would have sat at `provisional` with `icct_incomplete` until these pairs were adjudicated.

## 4. Three-mode reading of the cluster

- **Universal Mode:** the three specs must be internally coherent — a universal RT60 floor that no universal absorption provision can deliver is an incoherent floor. The ICCT makes the coherence checkable.
- **Population Mode:** the coupling is where the substantive adjudication happens. A-18×DEAF and A-18×AUT carry different RT60 targets (DEAF `stated` T1; AUT `provisional` T3); the A-08 noise floor interacts with each differently (auditory-processing populations need a larger SNR margin). The `INTERACTS` verdict is what forces the per-population joint solve instead of a single room number.
- **Person Mode:** no engine value. The two `INTERACTS` pairs become OT co-design inputs — "this person's intelligibility target sets a joint constraint on reverberation *and* background noise; resolve both together" — never an override of the individual's assessed need.

## 5. Generalization — the pass over the rest of category A and beyond

The same three verdicts recur across the corpus and are exactly what the register has been recording ad hoc and untyped: CON-0122 (`SUBSUMES`, corridor), the alcove rule (`INTERACTS`, circulation × seating), the CORRIDOR-W retirement (`INDEPENDENT`, width × sensory load). The ICCT's contribution is to make the pass **exhaustive** (every pair, not the pairs an author happened to cross-reference) and **typed** (a controlled verdict, not free-text folklore), so that no determination — least of all a strong one — ships having been read as its title rather than as a member of its category.

---

## Changelog

- 2026-07-20 v1: initial demonstration, companion to DR-2026-07-20-intra-category-cross-test.
