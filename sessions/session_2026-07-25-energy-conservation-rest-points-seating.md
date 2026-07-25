# Session — energy-conservation-rest-points-seating, batch 1

**Date:** 2026-07-25
**Slug:** `energy-conservation-rest-points-seating` (STUB, `seating-and-rest`)
**Axis:** `AX-STA` Sustained-exertion demand (ICF b455, b130 · d230, d450); secondary `AX-PAI`, `AX-AMB`, `AX-BAL`
**Doctrine SHA:** `0f2f525`
**Model:** Opus-class (synthesis floor satisfied; no `best_practice_synthesis` authored — see §6)
**DoD gate:** COMPLIANT on all 15 rules

---

## 1. Why this slug

Popped from `v_coverage_priority` (migration 035), which returned 7,210 uncovered required cells
but ties every zero-search slug at score 5 — the methodology defers open-gap and branch-thinness
weighting to out-of-view judgment. That narrowed to the 20 STUB slugs holding **zero sources and
zero logged searches**; the owner selected this one from four candidates.

State at entry: **0 linked sources, 0 logged searches**, and both `bpc_path` and `sl_path`
recorded in the DB pointed at files that did not exist on disk. Both files were created in this
batch.

## 2. Scope discipline — worked from axes

Per `DR-2026-07-22-work-from-axes`. The slug is scoped to the **demand layer** — distance
traversable before rest, sit-to-stand capability at a given seat, load tolerance while seated —
and **no umbrella was coined**. In particular "energy-limiting chronic illness" was explicitly
not used as a grouping, because it collapses opposed demands: a person who cannot stand and a
person who cannot sit for long are not served by the same bench. Interval, height variety and
setback are tracked as separate parameters for that reason.

## 3. What was admitted (8 sources, REF-00945 … REF-00952)

All DOIs pre-checked absent from the corpus (R9); all locators re-retrieved before admission (R10).

| REF | Tier | Contribution |
|---|---|---|
| REF-00945 | T3 | n=589, FI. Lack of resting places → QoL, **direct** association |
| REF-00946 | T3 | n=643/314, FI. Lack of resting places → unmet activity need, **strongest in those with walking difficulty** |
| REF-00947 | T3 | n=35, US, assistive-device users. Resting places named as key theme. **EXACT population match** |
| REF-00948 | T3 | n=81, FI. **Negative RCT** — see §5 |
| REF-00949 | T5 | DfT *Inclusive Mobility* 2021, clause-cited |
| REF-00950 | **Co-1** | Wheels for Wellbeing benches guidance |
| REF-00951 | T3-grey | ASLA — admitted to document its mis-citation |
| REF-00952 | T3 | The study ASLA cites |

**Two tiering calls made deliberately and recorded:**

- **REF-00948 is T3, not T1, despite being an RCT.** The tier definition requires
  intervention-level control *on the parameter under design*. The trial randomised an individual
  rehabilitation programme, not the built environment; relative to rest-point provision it is
  uncontrolled.
- **REF-00947 is T3, not Co-1.** Investigator-led academic qualitative research *with* disabled
  participants is not a disability-led publication. Logged explicitly to stop lived-experience-
  adjacent academic work drifting into the Co-1 track.

**Co-1 status was verified, not assumed.** Wheels for Wellbeing's About page was re-retrieved
specifically to test the classification. It states *"Informed by life-changing personal experience
of Disabled trustees, staff and volunteers."* It does **not** use the phrase "disabled-led", so
that phrase is not asserted on the organisation's behalf; the source row records the exact wording.

## 4. The batch's principal finding — need is evidenced, value is not

**The 50 m rest-point interval has no independent evidence base.**

Wheels for Wellbeing (Co-1) also states "no more than 50 m", which reads as lived-experience
corroboration of the DfT standard. It is not. WfW's own reference list cites *Inclusive Mobility
(2021)*. It is **the same figure restated by a second organisation**, not a second observation of
the world. Counting it as Co-1 support would double-count one number across two tiers.

Consequence under `tier-system.md` §8 + `DR-2026-07-21` Option A:

- The **need** for rest points anchors at **● full band** — two cohorts, a qualitative study with
  an exact population match, and Co-1 testimony.
- The **interval value** anchors at **○ weak band only** — its entire basis is T5 plus a Co-1
  restatement of that T5. No primary study located anywhere measures the distance at which people
  with sustained-exertion demand require rest.

Rendering the interval at ●/◐ or unflagged would be in error. Registered as **GAP-304**.

A second, smaller divergence: *Inclusive Mobility* itself gives **50 m** urban (§4.5, p.31) and
**100 m** countryside (p.124). Same authority, two settings — context-dependent, not contradictory,
but a naive "Inclusive Mobility says 50 m" is wrong.

## 5. R7 — failure / harm / inadequacy findings

**(a) Individual rehabilitation does not remove an environmental barrier.** REF-00948: a 12-month
home-based programme produced **no benefit over standard care** on perceived outdoor barriers
(time p=0.199, group p=0.911, interaction p=0.430); ~60% still perceived them. Direct evidence
that the intervention point is environmental provision, not individual capacity — now citable
rather than assertable.

**(b) A syndicated professional-body figure is unsupported by its own source.** ASLA's *Universal
Design Guide* asserts benches "at least every 65 feet (20 meters)… increases the number of older
adults **and mobility-disabled people** who feel comfortable traveling by sidewalk", citing one
bare hyperlink. Resolved and read in full: the cited study contains **no bench-spacing figure of
any kind**, studied community-dwelling Norwegians aged 67+ (mean 76.1), states *"the least mobile
groups living in institutions are not represented"*, and has **no disabled cohort**. Both the
quantity and the population attribution are unsupported. Filed `[UNVERIFIED-QUANT]`; population
graded **MISMATCH** on both REF-00951 and REF-00952.

## 6. What was deliberately NOT done

- **No `best_practice_synthesis` authored.** `opus_synthesis: false` retained. Batch 1 established
  the evidence position; synthesis is a separate act and the doc is queued at that boundary.
- **Non-English: deferred, not searched-and-empty.** Logged as one `deferred_reason` row. This
  slug has no `term_aliases` vocabulary, so a non-EN query would be back-translation (R11).
- **Mining on the Finnish cluster: deferred with reason.** REF-00945/946/948 share authors and
  institution (Jyväskylä). Naive citation-walking would return co-citations that *look like*
  independent replication. Registered as **GAP-306**; REF-00947 (US, independent) is flagged as
  batch 2's highest-value forward-mining target.

## 7. Substrate bug found and fixed

The DoD gate's R5 failure exposed a real defect rather than a data error.
`search_executions.language` carried **mixed case** — 37 rows lowercase `en`, others uppercase —
while `lang_jur_map` and `search_languages` are uppercase throughout. `v_coverage_priority`
suppresses a queue cell via `se.language = ljm.language`, and SQLite `=` on TEXT is
case-sensitive. **57 of 68 logged searches were therefore never suppressing their own coverage
cell: the priority queue was reporting completed work as un-done.**

Fixed forward: `search_executions.language` normalised to uppercase (mechanical; changes no
evidence claim and moves no adjudicated figure), and the R5 check in `research_batch_dod.py`
made case-insensitive. The gate selftest still passes, so the fix narrowed a false positive
without defanging the check.

## 8. Gate results

| Check | Result |
|---|---|
| `research_batch_dod --session` | **COMPLIANT**, 15/15 |
| `research_batch_dod --all` | COMPLIANT; all inherited-debt counters at baseline, none raised |
| `research_batch_dod --selftest` | PASS |
| Migration reproducibility (7 invariants) | PASS |
| `test_db_integrity.py` | 26/35 — **equal to pre-batch baseline**; a one-check regression I introduced (`NOT-APPLICABLE` outside the `doi_resolution_outcome` vocabulary) was found and corrected before commit |
| `validate_bpc.py` | 102/102 |
| `validate_cross_refs.py` | 0 issues |
| `source_slug_links_duplicates` | 0 |
| `db_path_env_audit` | 46/48 + 2 documented exemptions |

## 9. Batch 2 entry points

1. Resolve the 6 staged candidates — Ulahannan 2025, Gant 1997 (possible 1997 seating harm
   finding), Transport for All, Transport Scotland Appendix C, **Blackler 2018** (possibly the
   only primary basis for the seat-dimension figures), Access Association.
2. Forward-mine REF-00947 to test independence of the resting-places finding (GAP-306).
3. Build `term_aliases` for this slug to unblock non-EN work.
4. GAP-305: clause-cited values found at slug stage still have no structured home.
