# Search Log — energy-conservation-rest-points-seating

**Topic:** seating-and-rest
**Status:** PARTIAL LOG — batch 1 (first search ever run on this slug)
**Slug status:** STUB → sources now linked; remains STUB pending synthesis
**Governing axis:** `AX-STA` (Sustained-exertion demand; ICF b455, b130 · d230, d450) — ESTABLISHED.
Secondary: `AX-PAI`, `AX-AMB`, `AX-BAL`.
**Session:** session_2026-07-25-energy-conservation-rest-points-seating
**Last updated:** 2026-07-25
**opus_synthesis:** false

---

## Scope — worked from axes, not umbrellas

Per `DR-2026-07-22-work-from-axes` and `governance/functional-taxonomy.md` §3.3, this slug is
scoped to the **demand layer**, not to a population umbrella. No umbrella term
("energy-limiting chronic illness", "the fatigued", "physically disabled") is coined or used.

The demand this slug serves, stated as environment-side parameters:

| Demand parameter | Axis | Why it is the unit |
|---|---|---|
| Distance traversable before a rest is required | `AX-STA` | The interval between rest points is the environment-side variable |
| Sit-to-stand capability at a given seat | `AX-STA`, `AX-BAL` | Seat height / armrest presence determine whether a rest point is *usable* |
| Load tolerance while seated | `AX-PAI` | Backrest, seat angle, surface |
| Continuous-gait capability | `AX-AMB` | Interacts with, but does not equal, exertion demand |

**Explicitly rejected framing.** "Provide seating for people who get tired" collapses opposed
demands: a person who cannot stand and a person who cannot sit for long need *different*
provisions, and a single bench serves one at the other's expense. Interval, height variety and
setback are therefore tracked as separate parameters, not as one "seating" provision.

---

## Pre-LOG completeness — accepted blockers

| Blocker | Rationale |
|---|---|
| Non-EN jurisdictions NOT SEARCHED | Batch 1 is EN-only. This is a **deliberate deferral**, logged per-cell with `deferred_reason`, not a claim of absence. |
| Consensus engine near-exhausted | Connector quota: **2 searches remained at batch start** and 1 was spent. Recorded so a later batch does not mistake thin Consensus coverage for thin literature. |
| No code/standard values filed to `jurisdictional_values` | That table is `item_code NOT NULL` FK'd to `items`. This slug is at the **research stage and does not work from items**. Clause-cited values are recorded here and on the source rows instead of fabricating an item_code. Registered as a gap. |
| FDR not run | Out of scope for a first search batch. |
| `bpc_path` / `sl_path` pointed at non-existent files | Both files were absent from disk while the DB recorded paths for them. Created in this batch. |

---

## Coverage

| Axis | Target | Completed this batch |
|---|---|---|
| Language | 19 | EN only |
| Jurisdiction | 48 | UK (clause-level), US (grey), NO/FI/US (primary literature) |
| Engines | — | PubMed, Consensus, Scholar Gateway, web |

---

## Queries executed (verbatim, logged before screening — R8)

Empties are **retained**. A zero-yield search is a completed unit of work.

| # | Engine | Query (verbatim) | Found | Outcome |
|---|---|---|---|---|
| 1 | consensus | `lived experience of disabled people needing rest points and seating along pedestrian routes` | 20 | On-target; 4 leads |
| 2 | scholar_gateway | `What do co-produced and participatory studies with disabled people report about the provision of public seating and rest points along walking routes, and how does the absence of seating restrict their travel?` | 16 | **Low precision** — semantic drift |
| 3 | pubmed | `outdoor mobility older adults benches resting places walking` | 0 | **Query-shape failure** |
| 4 | pubmed | `street furniture seating provision pedestrian environment disability barrier` | 0 | **Query-shape failure** |
| 5 | pubmed | `benches AND walking AND aged[MeSH Terms]` | 49 | Well-formed; yield |
| 6 | pubmed | `"resting places" AND outdoor mobility` | 4 | Well-formed; **4/4 admitted** |
| 7 | web | `Transport for All disabled-led research street design seating rest points report` | 9 | Co-1 + T5 leads |
| 8 | web | `disabled people's organisation report public seating benches "rest points" campaign accessibility streets` | 8 | Co-1 lead (WfW) |
| 9 | web | `"Inclusive Mobility" 2021 Department for Transport seating "50 metres" rest seats pedestrian section` | 8 | Clause located |

### R14 — why the empties were empty

Queries 3 and 4 returned zero. This is **not evidence of absence**. PubMed's
`query_translation` shows it AND-chained every concept:

- Q3 → `outdoor AND mobility AND aged AND bench AND rest AND place AND walking` (7 concepts)
- Q4 → `street AND furniture AND seating AND provision AND pedestrian AND environment AND disability AND barrier` (8 concepts)

An 7–8 concept AND-chain over a literature this small returns zero by construction. Re-running
the same intent as a 3-concept query (Q5) returned **49 records**, and a phrase-anchored
2-concept query (Q6) returned **4 records of which all 4 were admitted**. Classification:
**query-shape failure, not genuine absence, not wrong index.**

Query 2 (Scholar Gateway) returned 16 articles of which ~1 was on-topic — the rest were heat
mapping, food retail, commuting. Classification: **wrong-index / semantic-drift failure**, again
not absence.

---

## R1 — Co-1 / Co-2 lived-experience pass (run FIRST, before any other admission)

| Source | Disability-led? | Verified how | Verdict |
|---|---|---|---|
| Wheels for Wellbeing — *Benches and Seating in Public Spaces* (11/2025) | Organisation's own About page states: *"Informed by life-changing personal experience of Disabled trustees, staff and volunteers"* and *"All our work is informed by practical experience of Disabled people"* | Re-retrieved the About page specifically to test the claim | **Co-1** — named disability-organisation output. Recorded with the org's exact self-description; the page does **not** use the phrase "disabled-led", so that phrase is not asserted on its behalf. |
| Rosenberg 2012 (Gerontologist) | No — investigator-led academic qualitative interviews | — | **T3, not Co-1.** Interviewing disabled people is not the same as a disability-led publication. Logged explicitly to prevent lived-experience-adjacent academic work being inflated into Co-1. |
| Transport for All — *Are We There Yet?* (2023) | Disabled-led transport charity | Not yet re-retrieved | **Candidate**, not admitted (R10). |
| Transport Scotland — Appendix C, *Perspectives of disabled street users* | Focus groups with disabled street users, inside a national framework | Not yet re-retrieved | **Candidate**, not admitted (R10). |

**Co-2 (OT professional-body CPG):** none found this batch. Not searched to exhaustion —
deferred, not declared absent.

---

## Sources confirmed (all re-retrieved this batch — R10; all DOI-prechecked — R9)

| REF | Source | Year | Tier | Content |
|---|---|---|---|---|
| REF-00945 | Rantakokko et al., *J Am Geriatr Soc* 58(11) | 2010 | T3 clinical | n=589, aged 75–81, Finland. Cross-sectional, LISREL path model. Lack of resting places / long distances → poorer QoL; **distances had a direct association with QoL**, other barriers acted through fear of moving outdoors. |
| REF-00946 | Rantakokko et al., *J Am Geriatr Soc* 58(4) | 2010 | T3 clinical | n=643 baseline / 314 at 2yr, aged 75–81, Finland. Prospective cohort. **Lack of resting places correlated with unmet physical activity need; association especially strong in those with walking difficulties.** All participants could walk ≥500 m at baseline. |
| REF-00947 | Rosenberg et al., *The Gerontologist* 53(2) | 2012 | T3 clinical | n=35, age 50–86, US, assistive-device users (canes 57%, walkers 57%, wheelchairs 46%). Qualitative + GPS-prompted interviews. **Availability of resting places and shelter on streets** emerged as a key theme. |
| REF-00948 | Portegijs et al., *BioMed Res Int* 2013:769645 | 2013 | T3 clinical | n=81 hip-fracture patients, Finland. RCT secondary analysis. 60–62% perceived ≥1 outdoor barrier incl. lack of resting places. **Negative result — see harm/failure findings.** |
| REF-00949 | DfT, *Inclusive Mobility* | 2021 | T5 national_fw | UK. §4.5 (p.31) 50 m urban interval; p.102 seat dimensions; p.124 100 m countryside interval. Clause-cited. |
| REF-00950 | Wheels for Wellbeing, *Benches and Seating in Public Spaces* | 2025 | **Co-1** | UK. Full dimensional guidance incl. **multiple seat heights**. |
| REF-00951 | ASLA, *Universal Design Guide — Streets* | n.d. | T3 grey | US. Asserts a 20 m interval. **See mis-citation finding.** |
| REF-00952 | *Improving walking conditions for older adults* (Eur J Ageing) | 2016 | T3 clinical | n=1,761 survey + 44 participatory observation + workshop, Kristiansand, Norway, aged 67+ (mean 76.1). The source ASLA cites. |

Tier assignment note — **REF-00948 is T3, not T1**, despite being an RCT. The tier definition
requires *"intervention-level control on the parameter under design."* The parameter here is the
rest point; the trial randomised an **individual rehabilitation programme**, not the environment.
Relative to this slug's parameter it is uncontrolled. Recorded so the reasoning is auditable.

---

## Consensus findings

| Finding | Evidence | Band |
|---|---|---|
| Absence of resting places is associated with reduced quality of life and unmet physical-activity need among people with walking difficulty | REF-00945, REF-00946 (two independent cohorts, same group) | **● full** (T3-clinical) |
| Availability of resting places is a salient environmental barrier named by assistive-device users themselves | REF-00947, REF-00950 | **● full** |
| Seat *usability* (height, armrests, setback) governs whether a rest point functions at all | REF-00949 §11.5, REF-00950 | ◐ / ● |

## Divergent findings

| Topic | Position A | Position B | Cause |
|---|---|---|---|
| Rest-point interval | **50 m** — DfT *Inclusive Mobility* §4.5 p.31, "commonly used pedestrian areas, and transport interchanges and stations" | **100 m** — same document, p.124, countryside paths | **Not a contradiction — context-dependent.** Same authority, two settings. Recorded because a naive read of "Inclusive Mobility says 50 m" is wrong. |
| Rest-point interval | **50 m** (UK, T5) | **20 m / 65 ft** (ASLA, US, T3-grey) | Unresolved — Position B is **unsupported by its own cited source** (below). |
| Seat height | **470–480 mm**, single band — REF-00949 p.102 | **380 / 480 / 580 mm**, deliberately plural — REF-00950 | **Substantive.** The standard assumes one height serves; the Co-1 guidance says a single height excludes, and specifies variety. Co-1 sits at the ● band, T5 at ◐. |

---

## R7 — Failure / harm / inadequacy findings (first-class)

**1. Individual rehabilitation does not remove an environmental barrier (REF-00948).**
A 12-month home-based rehabilitation programme aimed at improving mobility and function produced
**no additional benefit over standard care** on perceived outdoor environmental barriers
(time p=0.199, group p=0.911, interaction p=0.430). Barriers including lack of resting places
were still perceived by ~60% of participants. This is direct evidence that the intervention point
for this demand is **environmental provision, not individual capacity** — an argument the
guidebook should be able to make with a citation rather than an assertion.

**2. A widely-syndicated design figure is unsupported by its own source (REF-00951 → REF-00952).**
The ASLA *Universal Design Guide* states: *"Providing places to rest, benches or low retaining
walls, at least every 65 feet (20 meters) along street edges increases the number of older adults
and mobility-disabled people who feel comfortable traveling by sidewalk."* Its sole citation is a
hyperlink to PMC5549237. That article was re-retrieved in full. It contains:

- **no bench-spacing figure of any kind** — the only bench passage is qualitative: *"Benches are
  a measure that can be helpful for elders with reduced motor skills and balance. During the
  participatory observation, many suggested places where they would want a bench situated, usually
  close to steep gradients and especially in areas outside the city centre."*
- a study population of **community-dwelling Norwegians aged 67+ (mean 76.1)**, with the paper
  itself noting *"the least mobile groups living in institutions are not represented"*
- **no disabled cohort** — the "mobility-disabled people" in ASLA's sentence has no basis in the
  cited study

Both the **quantity** (20 m) and the **population claim** are therefore unsupported by the
citation offered. Filed `[UNVERIFIED-QUANT]`; population match graded **MISMATCH**.

---

## Adversarial pass — independence check (DR-2026-05-09)

**The 50 m interval has no independent evidence base, and the corpus must not double-count it.**

Wheels for Wellbeing (Co-1) also gives "no more than 50 m". It would be easy — and wrong — to
read that as lived-experience corroboration of the DfT standard. WfW's own reference list cites
**Inclusive Mobility (2021)**. It is the *same figure restated by a second organisation*, not a
second observation of the world.

Consequence under the weighted-strength model (`tier-system.md` §8) + Option A
(`DR-2026-07-21`): the interval figure's entire basis is **T5 + a Co-1 restatement of that T5**.
No T1/T2/T3 primary study anywhere in this batch measures the distance at which people with
sustained-exertion demand require a rest. The interval therefore anchors **only at the weak band
(○)** as *"best practice as currently known"*, flagged convergence-not-evidence — never rendered
unflagged and never at ●/◐.

The **need** for rest points is ● (T3-clinical, two cohorts + qualitative + Co-1).
The **interval value** is ○. These are different claims with different strengths, and the
distinction is the finding of this batch.

---

## Citation mining (R2)

| Source | Direction | Result |
|---|---|---|
| REF-00950 (WfW) | backward | Reference list yields Blackler et al. 2018 *Seating in Aged Care* (SAGE Open Med); HSE HSG57; BS 8300-1:2018; DfT Reference Wheelchair Report 2022; City of York Accessible Seating Review → all staged as candidates |
| REF-00951 (ASLA) | backward | Single citation → REF-00952; resolved and admitted; mis-citation established |
| REF-00945 / REF-00946 | backward/forward | **Deferred to batch 2** — same research group (Jyväskylä), so forward mining must be constructed to escape a single-group citation cluster rather than confirm it |

## Gaps registered

| Gap | Content |
|---|---|
| GAP-304 | Rest-point interval has no primary-evidence basis at any tier; 50 m (T5) and 20 m (grey, unsupported) diverge with nothing measuring the underlying distance |
| GAP-305 | `jurisdictional_values` is `item_code NOT NULL`, so clause-cited code values discovered at the slug/research stage have no structured home until an item exists |
| GAP-306 | Two independent primary cohorts on this slug come from one research group; independence untested |

## NO-DATA / THIN

| Jurisdiction | Language | Reason | Co-1 attempted? | T5 attempted? |
|---|---|---|---|---|
| All non-UK/US | non-EN | Deliberately deferred — batch 1 is EN-only | No | No |
