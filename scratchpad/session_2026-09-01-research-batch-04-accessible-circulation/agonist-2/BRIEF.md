# AGONIST-2 BRIEF — batch 04, accessible circulation
## The T1 / T2 academic pass: biomechanics, ergonomics, anthropometrics, human factors

**Session:** `session_2026-09-01-research-batch-04-accessible-circulation`
**Agent:** AGONIST-2 (T1 primary controlled research + T2 systematic reviews/meta-analyses)
**Date:** 2026-09-01
**Retrieval log:** `/home/user/guidebook/retrieval-log/session_2026-09-01-research-batch-04-accessible-circulation/`
**Scope discipline:** 17 query units (13 discovery searches across 5 engines + 4 identifier-resolution
queries), ≈110 titles/abstracts screened, **6 admissions proposed**, 11 candidates staged.

**Vocabulary confirmed read-only from the live schema, 2026-09-01:**
`search_executions.target_evidence_type CHECK IN ('clinical','sr_meta','standard_eb','national_fw','code','co1','co2','grey')`;
`engine` free-text, conventional values `pubmed|crossref|scholar|biorxiv|medrxiv|consensus|web|registry|manual`;
`depth_method IN ('scoping','systematic')`; `search_candidates.disposition IN ('REHOME','MISCELLANEOUS','PENDING-VERIFICATION','OUT-OF-SCOPE','ADMITTED')`.

---

## 1. QUERY LOG (R8 — every query, verbatim, empties kept)

`lang` = en throughout unless stated. `depth` = scoping unless stated.

| # | slug | engine | target_tier | target_evidence_type | verbatim query | found | screened | R14 classification |
|---|---|---|---|---|---|---|---|---|
| 1 | accessible-circulation-geometry | scholar (Scholar Gateway, Wiley corpus) | 1 | clinical | `What clear floor width and manoeuvring footprint do power wheelchair and scooter users actually require, measured empirically, and how does the occupied manoeuvring footprint differ from a nominal turning radius or turning circle?` | 12 | 12 | **NOT empty but effectively so — WRONG INDEX.** (Engine returned 20 passages spanning 12 unique articles; the article is the screening unit, so 12 is the stored figure for both.) 8 of 12 off-target (fish turning dynamics, UAV path optimisation, wheelchair cushion FEA). Scholar Gateway is the Wiley corpus only; the wheeled-mobility anthropometry literature is in SAGE (TRR), Taylor & Francis and IDeA Center reports. One genuine hit (Geoerg 2019). Do not read this as absence. |
| 2 | accessible-circulation-geometry | consensus | 1 | clinical | `wheelchair user anthropometry occupied space clear width corridor doorway requirements` | 9 | 9 | Non-empty. Highest-yield single query of the batch. |
| 3 | accessible-circulation-geometry | pubmed | 1 | clinical | `(wheelchair) AND (anthropometry OR "clear width" OR "turning space" OR maneuvering)` | 474 | **0** | Non-empty, and **executed but not mined**. The 2-concept OR-chain design is deliberate (not a 4-concept AND-chain), so recall is high and precision low — but I received 30 bare PMIDs and **resolved none of them to titles under this query**. Its top PMID (42596791) also appeared in query #12's list and was resolved there; it is counted as screened under #12, not here, so no record is double-counted. Screened = 0 is the honest figure. |
| 4 | stair-ramp-threshold-biomechanics-accessibility | consensus | 1 | clinical | `ramp slope gradient physiological energy cost and shoulder load during manual wheelchair propulsion` | 10 | 10 | Non-empty. Dense, mature literature. |
| 5 | stair-ramp-threshold-biomechanics-accessibility | pubmed | 1 | clinical | `(ramp OR slope OR incline OR gradient) AND wheelchair AND (energy expenditure OR physiological OR exertion OR shoulder)` | 112 | **0** | Non-empty, and **executed but not mined** — 30 bare PMIDs returned, none resolved to titles. Query #4 (Consensus) covered the same construct and was mined instead; that is where this cell's yield actually came from. |
| 6 | stair-ramp-threshold-biomechanics-accessibility | consensus | 1 | clinical | `pendulum test value slip resistance flooring and slip fall risk in older and disabled pedestrians` | 10 | 10 | Non-empty, but **subject drift**: 8 of 10 are tribology/metrology (device validity), not human outcome. See §9 — the PTV↔fall-outcome link is *genuinely* thin, the metrology is not. |
| 7 | threshold-door-hardware | consensus | 1 | clinical | `door opening force handle torque grip strength requirements for people with impaired hand function` | 10 | 10 | Non-empty but **9 of 10 off-parameter** (FES gloves, hand orthoses, grip strength as a mortality biomarker). The query collided with the rehabilitation-device literature. One decisive hit (Chang & Drury 2007). The *building-hardware* human-factors literature is genuinely tiny — see §9. |
| 8 | threshold-and-level-access | pubmed | 1 | clinical | `(threshold OR doorstep OR "level change" OR curb OR kerb) AND wheelchair AND (negotiat* OR barrier OR height)` | 37 | 30 | Non-empty. Small absolute yield (37) is itself informative: this is a thin literature, corroborated independently by Rouvier 2022 (2 curb studies in a 34-study systematic review). |
| 9 | threshold-door-hardware | consensus | 1 | clinical | `automatic door and revolving door entrapment injuries pedestrians` | 10 | 10 | Non-empty. R7 harm goldmine. |
| 10 | stair-ramp-threshold-biomechanics-accessibility | pubmed | 1 | clinical | `(stair OR staircase OR step) AND (fall OR falls) AND (riser OR going OR tread OR geometry OR dimensions OR handrail)` | 263 | **0** | Non-empty, and **executed but not mined** — 30 bare PMIDs returned, none resolved to titles. — the stair-geometry/falls literature is large and deserves its own dedicated pass rather than 30 skimmed titles. Flagged as a deliberate deferral, not a finding. |
| 11 | accessible-circulation-geometry | consensus | 1 | clinical | `maximum walking distance without rest and need for seating rest points among older and mobility impaired pedestrians` | 10 | 10 | Non-empty. |
| 12 | accessible-circulation-geometry | pubmed | 1 | clinical | `(bariatric OR obese OR "body size") AND (wheelchair OR "mobility device") AND (anthropometr* OR dimensions OR accommodation)` | 23 | **7** | **Non-empty but a NULL RESULT for the question asked** — *at the depth actually reached.* The query is exhaustive (`has_more: false`, all 23 PMIDs returned), but **I resolved only 7 of the 23 to full metadata**; the other 16 were never screened beyond the PMID. Of the 7 read, not one measures the *spatial* accommodation of a large-bodied wheeled-mobility user — they are body-composition/obesity-diagnosis work (BMI validity in SCI, weight-prediction equations, MMC anthropometry) plus one clinic-equipment checklist. **See the corrected, downgraded claim in §9. Corrected 2026-09-01 after recomputing screened counts: an earlier version of this row said "23 (all)", which would have laundered an inference over 16 unread records into a coverage claim.** |
| 13 | stair-ramp-threshold-biomechanics-accessibility | consensus | 1 | sr_meta | `multiple sclerosis fatigue and post-exertional malaise limiting mobility and energy cost of walking in the built environment` | 10 | 10 | Non-empty. Note: the query's "post-exertional malaise" term returned **zero** PEM/ME-CFS work — every hit was MS oxygen-cost. PEM is a distinct construct and is absent here; see §9. |
| 14 | accessible-circulation-geometry | crossref | 1 | clinical | `https://api.crossref.org/works?query.bibliographic=wheelchair+turning+space+manoeuvring+footprint+built+environment+accessibility` | 2,324,867 | 15 | **WRONG TOOL, not absence.** Crossref `query.bibliographic` is a citation-matching endpoint, not a semantic index; it returned 2.3M "results" led by BSI standard stubs (`10.3403/*`) and a ships-manoeuvring standard. Crossref is excellent for *resolving* a known reference and useless for *discovering* one. Logged so no future session re-reads this as evidence of a sparse literature. |
| 15 | threshold-door-hardware | pubmed | — | — | `automatic door injuries National Electronic Injury Surveillance System emergency department` (identifier resolution) | 1 | 1 | Resolution query. Recovered PMID 41192188 → real DOI `10.1016/j.ajem.2025.10.042`. |
| 16 | stair-ramp-threshold-biomechanics-accessibility | pubmed | 2 | sr_meta | `"Oxygen Cost of Walking in People With Multiple Sclerosis and Its Association With Fatigue"[Title]` | **0** | 0 | **EMPTY — and well-formed as a title-phrase query, so this IS interpretable.** Classification: **wrong index.** The paper exists (Crossref `10.7224/1537-2073.2020-128`); *International Journal of MS Care* has patchy PubMed coverage. Lesson for the project: a zero-result exact-title PubMed query does **not** license "does not exist". Resolved on the Crossref rung. |
| 17 | accessible-circulation-geometry | web | 1 | clinical | `Geoerg Schumann Holl Hofmann "Influence of Wheelchair Users on Movement in a Bottleneck and a Corridor" corridor width 1.2 m PDF` | 10 | 10 | Resolution query that turned productive — surfaced two stronger companions (Geoerg 2022 *Sci Rep*, Geoerg 2025 *Fire Technology* SR/meta-analysis) that no bibliographic-database query had returned. |

**Engines used: 5** — Scholar Gateway (semantic/Wiley), Consensus, PubMed, Crossref API, WebSearch.
Also used for verification only: Semantic Scholar Graph API, Europe PMC, Unpaywall, DOAJ API, PMC.

---

## 2. SCREENING

**Screened ≈110 records.** Rejected, with reasons:

- **Rehabilitation-device engineering** (robotic curb-climbing wheelchairs, FES gloves, assistive grip gloves, anti-rollback mechanisms, retractable handrails on sliding doors, honeycomb revolving-door linkages). Rejected: these study *the device*, not *the environmental parameter*. They cannot anchor a specification about a building.
- **Wheelchair-skills assessment instruments** (WST 4.2 Spanish validation; 5-AML/FIM items; Canadian skills-training survey). Rejected as off-parameter — they measure the *person's* trained capability, which is exactly the frame the project rejects (the building is the object of design, not the user's skill deficit). Retained one as a *harm* datum only (see §6).
- **Obesity clinical measurement** (BMI validity in SCI, circumference-based weight-prediction equations, vulval oedema case report, myelomeningocele body composition). Rejected as OUT-OF-SCOPE for a spatial specification.
- **Slip-resistance metrology** (Cui 2022 & 2024 BPN→COF simulation; Grönqvist 2000 tester comparison; Clarke 2015 BS 7976-2 vs ISO 13287; Benson 2022 wear-degradation; Sarıışık 2025 ML/DCOF; Ito 2023 femur-fracture pendulum). Not admitted, but **not discarded** — they are the reason the E-07 "PTV ≥36" number is less determinate than it looks (§9). Staged.
- **Off-topic Scholar Gateway returns** (fish fast-start turning dynamics, UAV routing, wheelchair cushion FEA, hospital evacuation tool HEPTAD). Rejected outright.
- **Non-disability pedestrian/walkability modelling** (15-minute city, walking-accessibility scoping reviews, older-pedestrian road-crossing SRs, solar-radiation walkability thresholds). Rejected as not bearing on a circulation-element dimension, except Horák 2025 which *does* model width and gradient thresholds directly.
- **Ramp studies using able-bodied participants as their whole sample** (Bertocci 2018 n=7 able-bodied non-users; Choi 2015 n=24 healthy; Arnet 2025 n=10 able-bodied). **Not admitted as anchors — this is a deliberate R13 exclusion.** They are recorded in §5/§9 because their existence, and the fact that Choi 2015's conclusion "1:12 and 1:10 are suitable ramp slopes" rests entirely on healthy young adults, is itself a finding about how gradient values enter the standards.
- **Huang 2025** (PLoS One, Chinese campus, n=30 "students with wheelchair experience"): rejected as an anchor. Its headline — "challenging to pass curb ramps with slopes steeper than **1:5**" — is a permissive result from a sample whose disability status is not established ("wheelchair experience" ≠ wheelchair user). Admitting it would import a 1:5 tolerance claim on a proxy sample. Staged with that warning attached.

---

## 3. PROPOSED ADMISSIONS (6)

Every bibliographic field below comes from a payload retrieved this session and saved to the retrieval
log. **No field is written from memory.** Author lists are given complete and in Crossref/PubMed
sequence order.

---

### A1 — Rouvier et al. 2022 · **T2 `sr_meta`** · slug `stair-ramp-threshold-biomechanics-accessibility`

- **Authors, in order:** Rouvier, Théo; Louessard, Aude; Simonetti, Emeline; Hybois, Samuel; Bascou, Joseph; Pontonnier, Charles; Pillet, Hélène; Sauret, Christophe *(8 authors)*
- **Title:** Manual wheelchair biomechanics while overcoming various environmental barriers: A systematic review
- **Journal:** PLOS ONE · **Vol/Iss/Art:** 17(6):e0269657 · **Year:** 2022 (issued 2022-06-23)
- **DOI:** `10.1371/journal.pone.0269657` · **PMID:** 35737733 · **PMCID:** PMC9223621 · **ISSN:** 1932-6203 · **Publisher:** PLoS
- **PubMed article type:** "Systematic Review" → `sr_meta`, T2 per `tier-system.md` §2/§9.
- **Tier justification:** A *systematic* review (defined search, inclusion/exclusion, 34 studies, numerical synthesis, five methodological recommendations) — not a scoping review, so T2 not T3 (§9).
- **Retrieval rung:** Crossref (`api.crossref.org/works/10.1371/journal.pone.0269657`) → PubMed esummary → PMC full text read.
- **Payloads:** `crossref_10.1371_journal.pone.0269657.json`; full text read at PMC9223621.
- **R9:** ⚠ **ALREADY HELD, AND THE HOLDING IS CORRUPT.** This DOI appears in `source_locators` **twice** — `REF-00037` and `REF-VERIFIED-003`. But `REF-00037`'s own `title`/`authors`/`pub_year`/`tier_claimed` fields read *"Inclusive Housing Design Guide. RIBA/Habinteg/CAE. DOI:10.4324/9781003564164" · Runnalls, J. & Walker, M. · 2024 · Co-2 · UK*. **The DOI column and the bibliographic columns of that row describe two different works.** `REF-VERIFIED-003` carries the DOI with no title at all. See §9 for why this matters beyond this one row.

---

### A2 — D'Souza, Steinfeld, Paquet & Feathers 2010 · **T1 `clinical`** · slug `accessible-circulation-geometry`

- **Authors, in order:** D'Souza, Clive; Steinfeld, Edward; Paquet, Victor; Feathers, David *(4 authors)*
- **Title:** Space Requirements for Wheeled Mobility Devices in Public Transportation: Analysis of Clear Floor Space Requirements
- **Journal:** Transportation Research Record: Journal of the Transportation Research Board · **Vol/Iss/Pages:** 2145(1):66–71 · **Year:** 2010
- **DOI:** `10.3141/2145-08` · **ISSN:** 0361-1981, 2169-4052 · **Publisher:** SAGE
- **Affiliations (from payload):** authors 1–3 Center for Inclusive Design and Environmental Access (IDeA Center), University at Buffalo SUNY; author 4 SHED Lab, Cornell.
- **Tier justification:** T1. Primary anthropometric measurement (n = 369 wheeled mobility device users) analysed against a design parameter (clear floor area). This is measurement *on the parameter under design*, which is the T1 test in `tier-system.md` §1.
- **Retrieval rung:** Crossref bibliographic query → Crossref work record.
- **Payload:** `crossref_10.3141_2145-08.json`
- **R9:** **NEW.** Not in `source_locators`, not in `evidence_sources`. Thematically adjacent stash rows exist (`REF-00044` "Anthropometry and Standards for Wheeled Mobility. Assist Technol 22(1):51–67"; `REF-00468` "Anthropometry of Wheeled Mobility Project — Final Report. IDeA Center / US Access Board") — same research programme, different outputs. Cross-file rather than treat as duplicates.

---

### A3 — Geoerg, Schumann, Holl & Hofmann 2019 · **T1 `clinical`** · slug `accessible-circulation-geometry`

- **Authors, in order:** Geoerg, Paul; Schumann, Jette; Holl, Stefan; Hofmann, Anja *(4 authors)*
- **Title:** The Influence of Wheelchair Users on Movement in a Bottleneck and a Corridor
- **Journal:** Journal of Advanced Transportation · **Vol/Pages:** 2019:9717208, pp. 1–17 · **Year:** 2019 (2019-06-20)
- **DOI:** `10.1155/2019/9717208` · **ISSN:** 0197-6729, 2042-3195 · **Publisher:** Wiley (originally Hindawi) · **Licence:** CC-BY (per Unpaywall)
- **Affiliations:** BAM (Bundesanstalt für Materialforschung und -prüfung), Berlin; Forschungszentrum Jülich.
- **⚠ AUTHOR-COUNT CORRECTION — READ THIS.** The Consensus result for this paper listed **five** authors, adding *"Haghani, M."*. **Three independent payloads — Crossref, Semantic Scholar Graph API, and the DOAJ API — all return exactly four authors, and none of them is Haghani.** Haghani is almost certainly the Hindawi academic editor, which that journal prints in the citation line. **The Consensus author string is wrong and must not be stored.** This is the 2026-08-19 fabrication class exactly, arriving through a tool rather than through memory.
- **Tier justification:** T1. Controlled large-scale laboratory movement experiments with an experimentally varied environmental parameter (passage width) — biomechanical/behavioural control on the parameter under design.
- **Retrieval rung:** Scholar Gateway (discovery) → Crossref (identity) → Semantic Scholar (corroboration) → Unpaywall (OA locations) → DOAJ API (third corroboration). **Full text NOT obtained**: `downloads.hindawi.com` and `onlinelibrary.wiley.com/pdfdirect` both returned HTTP 403; the DOAJ record's only "fulltext" link is the DOI itself. Four rungs taken; the block is at the publisher and is currently terminal for this session.
- **Payloads:** `crossref_10.1155_2019_9717208.json`, `s2_10.1155_2019_9717208.json`, `unpaywall_10.1155_2019_9717208.json`, `doaj_geoerg.json`.
- **R9:** **NEW.**
- **Admission caveat:** admit for its **abstract-level methodological finding only** (below). No quantified value may be drawn from this paper until the full text is obtained. Its quantified companion, Geoerg 2022 (§7, C-a), is open access and I *have* extracted numbers from that one.

---

### A4 — Chang & Drury 2007 · **T3 `clinical`** · slug `threshold-door-hardware`

- **Authors, in order:** Chang, Shih-Kai; Drury, Colin G. *(2 authors)*
- **Title:** Task demands and human capabilities in door use
- **Journal:** Applied Ergonomics · **Vol/Iss/Pages:** 38(3):325–335 · **Year:** 2007 (issued 2007-05)
- **DOI:** `10.1016/j.apergo.2006.04.023` · **PMID:** 16765902 · **ISSN:** 0003-6870 · **Publisher:** Elsevier
- **Tier justification — argued, not assumed:** **T3 `clinical`, not T1.** It is primary human-factors research with real measurement (2,400 observed interactions plus door wear-pattern measurement), but it is *observational field* work without experimental control of the door parameter. Under `tier-system.md` §1 that is "lower control level" → T3-clinical, which still maps to the **● full band** per §5/§8, so it anchors outright. I am flagging this because a reader will be tempted to call it T1 on the strength of its sample size; sample size is not control.
- **Retrieval rung:** Consensus (discovery) → Crossref (identity) → **Europe PMC `resultType=core` (independent abstract corroboration, PMID recovered)**.
- **Payloads:** `crossref_10.1016_j.apergo.2006.04.023.json`, `europepmc_10.1016_j.apergo.2006.04.023.json`, `s2_10.1016_j.apergo.2006.04.023.json`.
- **R9:** **NEW.** No door-force primary research is held. The stash's door rows (`REF-00155` BS 8300-2, `REF-00198`/`REF-00200` CAN/CSA B651-18, `REF-00461` AS 1428.1, `REF-00499` ADA §404, `REF-00210` DIN 18040) are **all T4–T6 code**. This admission is the first non-code evidence on doors in the project.

---

### A5 — Lalumiere, Gagnon, Hassan, Desroches, Zory & Pradon 2013 · **T1 `clinical`** · slug `threshold-and-level-access`

- **Authors, in order:** Lalumiere, Mathieu; Gagnon, Dany H.; Hassan, Jessica; Desroches, Guillaume; Zory, Raphael; Pradon, Didier *(6 authors)*
- **Title:** Ascending curbs of progressively higher height increases forward trunk flexion along with upper extremity mechanical and muscular demands in manual wheelchair users with a spinal cord injury
- **Journal:** Journal of Electromyography and Kinesiology · **Vol/Iss/Pages:** 23(6):1434–1445 · **Year:** 2013 (issued 2013-12; PubMed entry 2013-07-16)
- **DOI:** `10.1016/j.jelekin.2013.06.009` · **PMID:** 23866992 · **ISSN:** 1050-6411 · **Publisher:** Elsevier
- **Tier justification:** T1. Repeated-measures experiment with the environmental parameter (curb height: 4 / 8 / 12 cm) as the controlled independent variable, kinematics + kinetics + EMG on 15 manual wheelchair users **with SCI** — actual users, not simulators.
- **Retrieval rung:** PubMed (discovery + esummary) → Crossref (identity).
- **Payload:** `crossref_10.1016_j.jelekin.2013.06.009.json`
- **R9:** **NEW.**

---

### A6 — Rooney, McWilliam, Wood, Moffat & Paul 2021 · **T2 `sr_meta`** · slug `stair-ramp-threshold-biomechanics-accessibility`

- **Authors, in order:** Rooney, Scott; McWilliam, Gavin; Wood, Leslie; Moffat, Fiona; Paul, Lorna *(5 authors)*
- **Title:** Oxygen Cost of Walking in People With Multiple Sclerosis and Its Association With Fatigue: A Systematic Review and Meta-analysis
- **Journal:** International Journal of MS Care · **Vol/Iss/Pages:** 24(2):74–80 · **Issued (Crossref):** 2021-07-09
- **DOI:** `10.7224/1537-2073.2020-128`
- **⚠ Year discrepancy, stated not resolved:** Crossref `issued` = **2021**; the volume/issue (24(2)) belongs to a **2022** issue; Consensus rendered it "2021". Store the Crossref `issued` value and the volume/issue together and flag `pub_year_note`. Do not silently pick one.
- **Tier justification:** T2 `sr_meta` — an explicit systematic review *and meta-analysis* (four databases, defined inclusion, pooled SMD).
- **Why this is on-slug and not a stray medical paper:** E-03's item name frames ramp gradient as **"MS Fatigue and Temporal Accessibility"** with `icf=AX-STA band=full`. The determination that a 1:20 ramp is required *for that reason* has to rest on evidence that ambulant demand is elevated in MS. This is that evidence, at the highest synthesis tier available.
- **Retrieval rung:** Consensus (discovery) → **PubMed exact-title search returned 0 (see query #16)** → Crossref (resolution).
- **Payload:** `crossref_10.7224_1537-2073.2020-128.json`
- **R9:** **NEW.** Adjacent stash rows on fatigue exist (`REF-00032` energy conservation scoping review; `REF-00053`/TERM-053 fatigue and PEM) but no DOI collision.

---

## 4. QUANTIFIED FINDINGS (R3 — every number with its locator)

**Locator honesty convention used below:** `[abstract]` = the value is in the abstract of a payload I
retrieved; the page within the article is not confirmed. `[full text §x]` = read in the full text.
Anything with no locator carries the literal flag `[UNVERIFIED-QUANT]`.

### 4.1 On ramp gradient (E-03) — and what it does to the ≤1:20 claim

| Value | Source | Locator |
|---|---|---|
| 34 studies, 756 participants (mean 22, SD 25) | Rouvier 2022 | `[full text Table 1]` |
| 22 of 34 studies used SCI participants; **10 of 34 used able-bodied participants** | Rouvier 2022 | `[full text Table 1 / §3]` |
| Slope: **25 studies, and every one of them studied ASCENT ONLY** | Rouvier 2022 | `[full text Table 2, §3.1.2.1, §4.1]` |
| Slope grades studied across the literature: 0.6°, 1.1°, 1.4°, 1.7°, 2°, 2.3°, 2.7°, 3°, 3.5°, 3.6°, 3.7°, 4°, 4.1°, 4.6°, 4.8°, 5°, 6°, 6.8°, 7.1°, 9.4°, 9.8°, 12°, 15° | Rouvier 2022 | `[full text Table 2]` |
| Handrim mean *and* peak total force increase with grade — consistent across studies | Rouvier 2022 | `[full text §3.1.2.3]` |
| Glenohumeral **joint contact force** increases in all three components with grade | Rouvier 2022 | `[full text §3.1.2.3]` |
| "Muscle activity of all of the studied muscles was found to consistently increase with the grade" | Rouvier 2022 | `[full text §3.1.2.4]` |
| Cross-slope: **only 4 studies**, 7–25 participants (mean 14, SD 8); grades 0°, 1.4°, 2°, 3°, 6° | Rouvier 2022 | `[full text Table 3, §3.2]` |
| Ground type: 12 studies; grass gave the highest handrim forces/torque/power of any surface; lowest fraction of effective force on smooth concrete, **highest on grass** | Rouvier 2022 | `[full text Table 5, §3.4.2.3]` |
| Muscle work **doubled** for anterior deltoid from tile to padded carpet | Rouvier 2022 | `[full text §3.4.2.4]` |
| Oxygen cost of walking, MS vs controls: **SMD 2.21, 95% CI 0.88–3.54, P = .001** (9 studies; 7 comparative, MS n=176, controls n=142) | Rooney 2021 | `[abstract]` |

**Reference conversions, computed here, not taken from any source (arithmetic, flagged as such):**
1:20 = 2.86°; 1:12 = 4.76°; 1:10 = 5.71°; 1:8 = 7.13°.

**What this does to the item name.** E-03 asserts ≤1:20. The evidence:
- **Does not confirm a threshold at 1:20.** Every reviewed slope study reports demand rising *monotonically and continuously* with grade. There is no knee in the curve at 2.86°, and no reviewed study is designed to find one. A gradient specification is a point chosen on a continuous burden function, not a boundary the literature located.
- **Rests on a literature that has never studied descent.** 25 of 25 slope studies, ascent only (`[Rouvier §4.1]`). The authors themselves say descending slopes "deserve to be studied". Descent is where forward tipping and braking-through-the-handrim occur. **A ramp gradient specified from ascent-only evidence is specified from half the problem.**
- **Rests on a literature that has never studied threshold crossing.** Rouvier: *"technically challenging situations such as crossing a door threshold with or without a ramp deserve to be studied"* `[§4.1]`. There is no biomechanical study of the transition E-06 and E-05 are about.
- **Under-serves the item's own stated rationale.** E-03 is framed on MS fatigue (AX-STA, full band). **Not one of Rouvier's 34 studies is an MS study.** The wheelchair-propulsion literature answers a shoulder-load question; the item asks a sustained-exertion question. Rooney 2021 supplies the MS side, but for *walking*, not propulsion, and the two do not join up. **The gradient item currently has no single body of evidence that spans its own framing.**

### 4.2 On corridor clear width and manoeuvring footprint (E-08, E-12)

| Value | Source | Locator |
|---|---|---|
| n = 369 wheeled mobility device users measured; current US transport clear-floor-area dimensions **"are inadequate for accommodating many users of wheeled mobility devices, especially those who use power chairs and scooters"** | D'Souza 2010 | `[abstract]` |
| Method is **occupied device length × width**, not a turning circle | D'Souza 2010 | `[abstract]` |
| n = 500 (updated dataset); prescribed minimum dimensions "are too small to accommodate the size of many occupied wheeled mobility devices, especially power chairs and scooters" | Bharathy & D'Souza 2018 *(staged, §7)* | `[abstract]` |
| **The specific-flow concept "fits for the nondisabled subpopulation but it is not valid for scenario considering wheelchair users in the population"** | Geoerg 2019 | `[abstract]` |
| "Flow and movement speed are in a complex relation and **do not depend on density only**" | Geoerg 2019 | `[abstract]` |
| Bottleneck widths experimentally tested: **0.90 m and 1.20 m**; bottleneck length 2.4 m; waiting area ≈30 m² at 12 m from the bottleneck | Geoerg 2022 *(staged, §7)* | `[full text, Methods "Study configuration" + Fig 1 caption — table/figure numbering as reported by the retrieval tool, not independently confirmed against the PDF]` |
| Flow at 0.90 m width: **J = 1.30 s⁻¹ (reference, no disabled participants) vs J = 0.91–0.95 s⁻¹ (heterogeneous groups)** — a reduction of roughly 30% | Geoerg 2022 *(staged)* | `[full text Table 5 / Results "Effect of Crowd heterogeneity" — same caveat]` |
| Median neighbour distances: wheelchair group 0.89 m; reference 0.86 m; mixed 0.80 m | Geoerg 2022 *(staged)* | `[full text, Results "Distances" — same caveat]` |
| Sample: N = 252 across 12 studies; **5 manual wheelchair users, 2 electric wheelchair users**, 1 white-cane user, 1 Deaf participant, 2 assistance-dependent — 12 disabled participants in total | Geoerg 2022 *(staged)* | `[full text Tables 2–3 — same caveat]` |
| Meta-analysis: **9 studies**, all controlled experiments; egress-time difference with vs without wheelchair users **"close to three standard deviations"**; no evidence of publication bias | Geoerg 2025 *(staged)* | `[abstract]` — exact pooled estimate and CI **NOT VERIFIED**, Springer redirects to an auth wall |
| Path-width thresholds at which walking accessibility collapses: **150 cm and 90 cm**; gradient thresholds **5% and 12.5%**; a fully barrier-free network model reduces walking access to shops by **40–70%**, and **up to 37% of inhabitants lose walking access to shops entirely** if they acquire a mobility disability | Horák 2025 *(staged)* | `[abstract]` |

**No millimetre figure was extracted from D'Souza 2010 or Bharathy 2018** — both are paywalled and I read
only abstracts. **Any specific mm value attributed to them carries `[UNVERIFIED-QUANT]` until the
percentile tables are obtained.** I am stating this rather than reporting a plausible number.

**What this does to the item name.** E-08 asserts ≥1200 mm.
- **1200 mm is inside the tested band, and the tested band shows a capacity penalty.** Geoerg 2022 tested 0.90 m and 1.20 m and found ~30% flow reduction with disabled participants present at 0.90 m.
- **The deeper problem is the model, not the number.** "Specific flow" — flow proportional to width — is the engineering logic underneath *every* per-metre width rule, including egress-derived corridor minima. Geoerg 2019 reports that this relation **does not hold** when wheelchair users are in the population. So a corridor width justified by a flow-per-metre calculation is justified by a model its own target population invalidates. That is a stronger and more transferable finding than any single millimetre value.
- **The manoeuvring-footprint / turning-radius seam is real and the primary work exists.** The IDeA Center line (D'Souza 2010 n=369 → Bharathy 2018 n=500) measures **occupied device footprint**, and both papers conclude the prescribed clear-floor dimensions are too small — specifically for **power chairs and scooters**, the devices a nominal turning radius represents worst. This is the primary anthropometric and kinematic work the slug `manoeuvring-footprint-vs-turning-radius-methodology` is looking for.

### 4.3 On door hardware and operating force (I-01, E-11, H-04)

| Value | Source | Locator |
|---|---|---|
| Doors are involved in **over 300,000 injuries per year (USA)** | Chang & Drury 2007 | `[abstract]` |
| Study 1: **1,600** human/door interactions observed | Chang & Drury 2007 | `[abstract]` |
| Study 2: **800** push-door interactions observed | Chang & Drury 2007 | `[abstract]` |
| Use of **force-enhancing strategies increased for larger doors, particularly for people of smaller stature** | Chang & Drury 2007 | `[abstract]` |
| Force is exerted **higher for taller individuals and closer to the centre of the door than is typically assumed** for handle placement | Chang & Drury 2007 | `[abstract]` |
| Recommendation: **restoring torque below 30 N·m**; handle/push plate **250–350 mm from the door edge** and **1000–1500 mm above the floor** | Chang & Drury 2007 | `[abstract; corroborated independently via Europe PMC core record, PMID 16765902]` |
| **8.3% of men in a sample of 338 SCI wheelchair users produced NO grip force at all** | Kim 2026 *(staged, §7)* | `[abstract]` |
| Same sample: seated heights **9–27% lower** than a general adult comparison sample; "the height accommodating 90% of users fell below common accessible work-surface ranges" | Kim 2026 *(staged)* | `[abstract]` |

**What this does to the item name.** I-01 asserts "Lever, D-Pull, One-Hand Operable, ≤22 N".
- **The measured evidence is a TORQUE, not a force.** Chang & Drury recommend **<30 N·m restoring torque**. A 22 N figure is a linear force with no stated moment arm. **These two quantities are not interconvertible without the handle-to-hinge distance**, and Chang & Drury's second finding is precisely that the assumed point of force application is wrong. So the project's ≤22 N and the only primary human-factors number on doors **cannot currently be reconciled**, and the item's number does not have this paper behind it.
- **The force threshold is the wrong binding constraint for a substantial minority.** If 8.3% of men in an SCI wheelchair-user sample produce zero grip force, then for those users no value of "≤22 N" is operable, because the limiting variable is not magnitude but **modality** — grasp versus non-grasp. Kim's own conclusion points at "low-force non-grasp interfaces". **A determination phrased purely as a force ceiling silently excludes the users at the tail.** This is the `A-SIZE`/tails argument, transposed from body dimension to hand function, and it is the single most consequential finding in this brief for item I-01.
- **The "smaller stature" result is an A-SIZE finding hiding in a 2007 ergonomics paper.** People of smaller stature had to recruit force-enhancing strategies on larger doors. That is the environment normed to an average body, measured, in 1,600 observations.

### 4.4 On thresholds and level change (E-06, E-05)

| Value | Source | Locator |
|---|---|---|
| Curb heights experimentally varied: **4 cm, 8 cm, 12 cm**, 3 trials each, approach from 3 m | Lalumiere 2013 | `[abstract]` |
| n = 15 manual wheelchair users **with SCI** | Lalumiere 2013 | `[abstract]` |
| Movement excursion, net joint moments and **muscular utilisation ratio all increased with curb height**, mainly at the shoulder; significant at p < 0.0167 for most outcomes | Lalumiere 2013 | `[abstract]` |
| Greatest effort generated by **shoulder flexors and internal rotators, and elbow flexors** | Lalumiere 2013 | `[abstract]` |
| The entire curb literature is **2 studies** (heights 4, 8, 10, 12 cm), with "extremely high variability" in upper-limb joint kinetics | Rouvier 2022 | `[full text Table 4, §3.3.2.2]` |
| **Only 26.9% of surveyed curb ramps achieved a smooth transition ≤13 mm**; only 43.6% had slopes ≤1:12; only 57.7% had gutter counter-slopes ≤1:20; mean score 5.6 ± 1.1 of 8; **only 2.6% of 79 intersections met all eight criteria** | Bennett, Kirby & Macdonald 2009 *(staged, §7)* | `[abstract]` |
| Electric powered wheelchair sideways tips: curb heights 0.30–0.41 m, approach angles 5–63°, speeds 0.6–1.5 m/s. Head impact force **unrestrained 6181 ± 2372 N vs restrained 1336 ± 827 N (p = 0.00053)**; HIC **610 ± 634 vs 29 ± 38 (p = 0.00013)**; several tips gave **HIC > 1000 (severe head injury)** | Erickson 2016 *(staged, §7)* | `[abstract]` |
| Oxygen cost in progressive MS vs controls: **climbing steps 3.60×**, rolling in bed 3.53×, walking 3.10×, lying-to-sitting 2.50×, sitting-to-standing 1.82×; **mean 2.81× across tasks**; task-induced fatigue ↔ oxygen cost of walking ρ(13) = 0.626, P = .022 | Devasahayam 2019 *(staged, §7)* | `[abstract]` |

**What this does to the item name.** E-06 asserts zero-step entry.
- **The evidence supports the *direction* but does not test the *value*.** Lalumiere's smallest curb is 4 cm — roughly three times the 13–15 mm upstand that threshold clauses actually turn on. The finding is that demand rises monotonically from 4 cm upward. **Nothing in this literature tests 0 mm against 13 mm against 15 mm.** Rouvier confirms why: threshold crossing has never been studied (§4.1). The zero-step specification is directionally supported and quantitatively unevidenced, and it is honest to say so.
- **Climbing steps is the single most energetically expensive mobility task measured in progressive MS — 3.60× controls.** That is the strongest available number for why a step is not a minor inconvenience, and it comes from an MS sample using walking aids, i.e. the ambulant disabled users a zero-step entry also serves.
- **The specification is met by about a quarter of installations.** Bennett 2009's 26.9% ≤13 mm transition rate says the failure is in delivery, not in the clause.

### 4.5 On slip resistance (E-07)

| Value | Source | Locator |
|---|---|---|
| Slip probability rises from ca. **17% to 41%** with surface wear, depending on material; wear greatest at **staircase edges and lift entrances**; least dangerous surface roofing **SVR 73 ± 8**, most dangerous laminated wood-based **SVR 29 ± 12**; rubber sole / bare foot **SVR 55 ± 5**; felt sole **SVR 29 ± 3**; 16 surfaces tested across three stages, one public-utility building in Poznań | Waluś et al. 2022 *(staged, §7)* | `[abstract]` |
| Explicitly tested a **rubber sample representing the ferrule tip of assistive devices** (crutches, sticks, tripods) as well as footwear | Waluś et al. 2022 *(staged)* | `[abstract]` |
| Frictional resistance is reduced when tested wet **and further exacerbated on a slope**; "the perceived affordance of certain features such as **tactile indicators providing a better grip or traction requires urgent attention**" | Chew et al. 2024, *Buildings* *(staged, §7 — identity not resolved)* | `[abstract]` |
| Different British Pendulum units produce BPN readings differing by **more than 20%**, from slider force–deflection differences; the BPN↔COF relation is **nonlinear and device-specific**, so a single regression between them "does not correctly represent the relationship" | Cui et al. 2022, *J Testing & Evaluation* *(staged, §7 — identity not resolved)* | `[abstract]` |

**What this does to the item name.** E-07 asserts PTV ≥36 wet.
- **PTV ≥36 is a value with a stated instrument tolerance of over 20% between devices.** If two compliant pendulums can disagree by >20%, a specification stated to two significant figures is stated more precisely than it can be measured. This does not make PTV ≥36 wrong; it makes an unqualified "≥36" a false precision.
- **It is an installation value for a property that decays.** Waluś measures degradation with use and locates the worst wear exactly at **stair nosings and lift entrances** — the two places E-07 most needs to hold, and the two places E-01/E-02 put people. **A specification stated once at handover, for a property that halves in service, is a specification that is not in force when it matters.** Recommending a maintenance/re-test interval alongside the value is better supported by this evidence than the value itself is.
- **Waluś reports "SVR"/"Slip Resistance Value" and "PTV" in the same abstract.** I could not confirm from the abstract that SVR and PTV are the same scale. **Do not map any SVR figure onto the PTV ≥36 threshold until the full text is read.** Flagged rather than assumed.
- **Tactile indicators may not do what they are assumed to do.** Chew 2024 explicitly questions whether tactile walking surface indicators provide the traction they are credited with. The project holds `REF-00306` (ISO 23599:2019) and `REF-00326` (JIS T 9251:2001) on TWSIs — both T4 standards, both with no traction evidence behind them in this corpus.

### 4.6 On rest seating intervals (E-10)

| Value | Source | Locator |
|---|---|---|
| **65%** of elderly persons satisfied if the interval between resting places is **shorter than 100 m**; **70%** satisfied if shorter than **50 m** | Usui & Hino 2019 *(staged, §7)* | `[abstract]` — **⚠ SECOND-HAND, see below** |
| Japanese government technical guidance: continuous walking distance **500–700 m**, shortening with age | Usui & Hino 2019 *(staged)* | `[abstract]` |
| Around Tokyo Central and Otemachi stations, actual continuous walking distance **exceeds 100 m** and resting places are insufficient | Usui & Hino 2019 *(staged)* | `[abstract]` |
| Present bench locations around Tokyo Central Station require continuous walking distances of **100–350 m**; optimal bench count computed as **681** | Usui 2022, *Applied Spatial Analysis and Policy* *(staged, §7 — identity not resolved)* | `[abstract]` |

**⚠ THE CRITICAL CAVEAT.** Usui & Hino state the 65%/100 m and 70%/50 m figures as *"In the literature,
it was found that…"* — **these are not their measurements.** Usui & Hino 2019 is therefore a
**secondary report** of those percentages and must not be cited as their primary source. Its own
contribution is the furthest-neighbour-distance theory. **Do not admit it as the anchor for E-10.**
The primary Japanese source behind 65%/70% is a backward-mining target (§8).

**What this does to the item name.** E-10 asserts "rest seating at regular intervals" without a number.
The project's stash already holds **two different intervals from code-tier sources** — `REF-00162`
(BS 8300-1:2018 + Manual for Streets, 100 m) and `REF-00511` (Make Your Business Accessible §5, 50 m).
**The 65%/70% satisfaction pair maps onto exactly those two numbers.** That is a strong hint that
50 m and 100 m entered the standards from a single Japanese satisfaction survey — which would make the
apparent BS-vs-guidance "convergence" a common-ancestor artefact, i.e. `tier-system.md` §3's
convergence-not-evidence trap with a traceable ancestor. **I have not proved this and am not asserting
it.** It is a hypothesis worth one backward-mining pass, and it is the highest-value single lead in
this brief for E-10.

---

## 5. POPULATION GRADING (R13 — population of STUDY vs population SERVED)

Graded ruthlessly. `EXACT | PARTIAL | PROXY | MISMATCH`.

### A1 Rouvier 2022 (34 studies, 756 participants)
| Served | Study population | Grade | Mismatch note |
|---|---|---|---|
| SCI | 22 of 34 studies SCI | **PARTIAL** | SCI-dominant but the pooled synthesis silently blends in able-bodied studies. |
| MOB | manual wheelchair users | **PARTIAL** | **Manual chairs only.** Power chairs and scooters are absent from the entire review. |
| LMB, PAIN | lower-limb amputee, CP, neuropathy, Friedreich's ataxia present but few | **PARTIAL** | Small sub-samples, not separately synthesised. |
| — | **10 of 34 studies used able-bodied participants** | **PROXY** | ≈29% of the primary literature this review pools studied people simulating wheelchair use. The review does not stratify its conclusions by this. |
| MS | none | **MISMATCH** | No MS study included. E-03's own framing is unserved by its own best synthesis. |
| BAR, LPA, TALL | not stratified | **MISMATCH** | No body-size stratification anywhere in the review. |

### A2 D'Souza 2010 (n = 369)
| Served | Study population | Grade | Mismatch note |
|---|---|---|---|
| MOB, SCI | wheeled mobility device users — manual, power, scooter | **EXACT** | Actual device users across device classes; the correct population for a footprint question. |
| BAR | large-bodied users present in the dataset but **stratification not verified from the abstract** | **PARTIAL** | I did not obtain the percentile tables. Do not claim bariatric accommodation from this until they are read. |
| LPA, TALL | not verified | **PARTIAL** | Same limitation. |
| — | US sample | **PARTIAL** | Device populations differ by procurement regime; US power-chair prevalence is not universal. |
| — | measured in a **static** occupied-footprint protocol | **PARTIAL** | The footprint-vs-turning-radius question is partly *dynamic*. A static occupied footprint is necessary and not sufficient. |

### A3 Geoerg 2019
| Served | Study population | Grade | Mismatch note |
|---|---|---|---|
| MOB, SCI | mixed crowds including wheelchair users of different types | **PARTIAL** | In the 2022 companion the disabled participants are **12 of 252**, of whom 7 are wheelchair users. The disabled sample is small in absolute terms by experimental design. |
| ALL | German adult volunteer crowds | **PARTIAL** | Volunteers able to attend a controlled crowd experiment — a fitness-selected sample. |
| BLIND, DEAF | 1 each (2022 companion) | **PROXY** | n = 1 cannot support a population claim. |
| BAR, LPA, TALL | none reported | **MISMATCH** | |

### A4 Chang & Drury 2007
| Served | Study population | Grade | Mismatch note |
|---|---|---|---|
| LMB, MOB, PAIN, SCI, DEM | **unselected general public; disability status never recorded** | **PROXY** | This is the honest grade and it should not be softened. The 30 N·m recommendation is derived from the capability distribution of a *predominantly non-disabled* stream of door users. Applying it to a disabled population is an extrapolation the study does not license. |
| LPA, TALL | **stature was directly measured and stratified** | **PARTIAL** | Stature is the study's own variable, which is unusually good — but no little-person or very-tall sample was recruited; the range is the range that walked through the door. |
| — | single door type, single US site | **PARTIAL** | |

### A5 Lalumiere 2013 (n = 15)
| Served | Study population | Grade | Mismatch note |
|---|---|---|---|
| SCI | 15 manual wheelchair users with SCI | **EXACT** | |
| MOB | manual wheelchair users | **PARTIAL** | **Power chairs excluded**, and a power chair negotiates a level change by an entirely different mechanism. |
| BAR, LPA, MS, LMB | not represented | **MISMATCH** | |
| — | curb heights 4/8/12 cm vs a 13–15 mm specification | **PARTIAL on the parameter itself** | The study's smallest condition is ~3× the height the item turns on. Extrapolating downward from 4 cm to 15 mm is an inference, not a measurement. |

### A6 Rooney 2021 (9 studies; MS n = 176, controls n = 142)
| Served | Study population | Grade | Mismatch note |
|---|---|---|---|
| MS | adults with MS | **PARTIAL** | The review states the pooled sample has **"predominantly mild-to-moderate disability"**. The people for whom ramp gradient is decisive — EDSS ≥ 6, walking-aid users — are the least represented. The effect is likely conservative, but that is an argument, not a measurement. |
| COM (ME/CFS, post-exertional malaise) | none | **PROXY at best** | **Elevated oxygen cost of walking is not post-exertional malaise.** They are different constructs with different time courses. TERM-053 names both fatigue *and* PEM; this evidence reaches only the first. Treating MS oxygen cost as PEM evidence would be a mechanism substitution. |
| PAIN | not studied | **MISMATCH** | |
| MOB, SCI, WHM | **ambulant sample by inclusion criterion** | **MISMATCH** | Anyone who cannot walk is excluded by design. |

### The endemic-PROXY pattern, stated plainly
Across the ramp-gradient literature specifically, the sequence is: **Bertocci 2018** (n = 7 able-bodied,
*"having no propulsion experience"*), **Choi 2015** (n = 24 healthy adults, concluding *"the 1:12 and
1:10 slopes are suitable ramp slopes for wheelchairs"*), **Arnet 2025** (n = 10 able-bodied), and
**10 of Rouvier's 34 included studies**. **A gradient recommendation of 1:12 has been published on the
basis of healthy young adults pushing an empty-of-disability wheelchair up a ramp.** Any determination
that leans on the general ramp-gradient literature is leaning, in part, on that.

---

## 6. HARM / FAILURE / INADEQUACY FINDINGS (R7)

1. **Automatic doors — 38,720 US emergency-department visits over 2015–2024.** Older adults 36.5% of
   visits, head/neck injuries 39.1% and trunk/internal 23.8% in that group, admission rate 18.4% (vs
   4.2% for adults), **odds of severe injury 3.18 (95% CI 1.33–7.56) versus adults**. Paediatric OR 0.03
   (95% CI 0.003–0.332). Shapovalov et al. 2025, `10.1016/j.ajem.2025.10.042`, PMID 41192188 `[abstract]`.
   **This directly qualifies E-11.** Automatic sliding doors are specified as an accessibility
   provision; the population they most serve — older and disabled people — is the population that
   sustains the severe injuries when they fail. The item as written carries no safety-envelope,
   force-limitation or sensor-coverage condition.
2. **Automatic revolving door fatality.** A 19-month-old boy killed by compression in a 4 cm gap in an
   automatic revolving door; cause of death combined skull/brain and thoracic compression. Cortis et al.
   2015, *International Journal of Legal Medicine* `[abstract]` — **identity not resolved to a DOI, see §10.**
3. **Doors generally: over 300,000 injuries per year in the USA** (Chang & Drury 2007 `[abstract]`).
4. **Electric powered wheelchair tips at level changes cause head-injury-criterion values above 1000.**
   Unrestrained head impact 6181 ± 2372 N; HIC 610 ± 634, several events HIC > 1000. Curb height and
   approach angle were the significant predictors; **driving speed was not.** Erickson et al. 2016,
   `10.1186/s12984-016-0128-7` `[abstract]`. Bears on E-06 and on any drop-off at a platform lift (E-02).
5. **Compliance failure at curb transitions.** Only 26.9% of 79 surveyed intersections achieved a
   ≤13 mm transition; only 43.6% achieved ≤1:12; **only 2.6% met all eight accessibility criteria.**
   Bennett, Kirby & Macdonald 2009, `10.1080/17483100802542603`, PMID 19172477 `[abstract]`.
6. **Slip resistance degrades exactly where it is most needed.** Wear is greatest at **staircase edges
   and lift entrances**; slip probability rises from ~17% to ~41% with use. Waluś et al. 2022 `[abstract]`.
7. **Cross-slope imposes asymmetric propulsion load and is barely studied.** Four studies in the whole
   literature (Rouvier 2022 Table 3). A theoretical analysis estimates a **critical cross slope of 3% at
   zero running slope**, above which the user must brake on the upslope pushrim — *"fatiguing over long
   distances"*. Flemmer et al. 2026, *Disabil Rehabil Assist Technol* `[abstract]` — **identity not
   resolved, see §10.** Cross-slope is absent from all four slugs' item set and should probably be in it.
8. **Upper-extremity injury is the mechanism the whole ramp literature is measuring.** Shoulder
   flexors/internal rotators and elbow flexors at curbs (Lalumiere 2013); glenohumeral contact force
   rising in all three components with grade (Rouvier §3.1.2.3). The project already holds `REF-00442`
   ("Upper extremity preservation in manual wheelchair users") and `REF-00341` ("Shoulder moment
   contributions to wheelchair propulsion") in `source_locators`. **The harm here is cumulative and
   iatrogenic to the built environment: a compliant-but-steep ramp is a shoulder-destruction device
   operated once per visit for a lifetime.**
9. **The literature's own admission of absence.** Rouvier et al., §4.1: descending slopes, descending
   curbs, and **door-threshold crossing with or without a ramp** all "deserve to be studied". The
   authors of the field's only systematic review say the descent and threshold cases are unstudied.

---

## 7. CANDIDATES TO STAGE (R7 / R15)

Disposition vocabulary as per the `search_candidates.disposition` CHECK constraint.

**Metadata fully verified from a saved payload; held back only by the 4–6 admission cap.** These are
admission-ready and I would take all of them next. Disposition `PENDING-VERIFICATION` with
`why_not_admitted` = "batch cap; identity fully verified, full text not read".

| Candidate | Identity | Slug | Tier guess | Note |
|---|---|---|---|---|
| **C-a** Geoerg, Paul; Schumann, Jette; Boltes, Maik; Kinateder, Max (2022). *How people with disabilities influence crowd dynamics of pedestrian movement through bottlenecks.* **Scientific Reports 12:14273** | DOI `10.1038/s41598-022-18142-7`, PMID 35995966, PMCID PMC9395390, OA | accessible-circulation-geometry | T1 | **Open access and I extracted quantified widths and flows from it (§4.2).** Strictly better than A3 for R3 purposes; A3 is better for the specific-flow claim. Take both. |
| **C-b** Geoerg, Paul; Bode, Nikolai W. F.; Berthiaume, Maxine; Kinateder, Max (2025). *The Effect of Wheelchair Users on the Egress Time of Pedestrian Crowds: A Systematic Literature Review and Meta-analysis.* **Fire Technology 61(6):4331–4348** | DOI `10.1007/s10694-025-01740-y` | accessible-circulation-geometry | **T2 `sr_meta`** | 9 controlled experiments; effect "close to three standard deviations"; no publication bias. **The only meta-analysis in existence on wheelchair users and circulation capacity.** Exact CI unverified (Springer auth wall). |
| **C-c** Bharathy, Aravind; D'Souza, Clive (2018). *Revisiting Clear Floor Area Requirements for Wheeled Mobility Device Users in Public Transportation.* **Transportation Research Record 2672(8):675–685** | DOI `10.1177/0361198118787082` | accessible-circulation-geometry | T1 | n = 500. The updated IDeA/Michigan dataset. Pairs with A2. |
| **C-d** Kim, Jang-Hyeon (2026). *Seated anthropometry, functional reach, and hand strength in Korean wheelchair users with spinal cord injury: reference percentiles for assistive-technology and accessible design.* **Disability and Rehabilitation: Assistive Technology, pp. 1–14** | DOI `10.1080/17483107.2026.2716524`, PMID 42596791, published online 2026-08-14, **single author** | threshold-door-hardware (I-01) + accessible-circulation-geometry (E-12) | T1 | **Carries the 8.3%-zero-grip finding (§4.3), which is the most consequential single datum in this brief.** Held back only because it is very recent, single-authored, paywalled, and I read only the abstract. **Verify before relying on it.** |
| **C-e** Shapovalov, Vadym; Lagunzad, Isabella; Tran, Quincy K.; Groussis, Maria; Abdelsayed, Nolan; Pourmand, Ali (2025). *Injury patterns and epidemiology of automatic door-related trauma: A retrospective analysis.* **Am J Emerg Med 99:411–415** | DOI `10.1016/j.ajem.2025.10.042`, PMID 41192188 | threshold-door-hardware (E-11) | T3 clinical | `harm_finding = 1`. **⚠ See §10 — I initially guessed this DOI and guessed WRONG.** |
| **C-f** Bennett, Sean; Kirby, Ronald Lee; Macdonald, Blair (2009). *Wheelchair accessibility: descriptive survey of curb ramps in an urban area.* **Disabil Rehabil Assist Technol 4(1):17–23** | DOI `10.1080/17483100802542603`, PMID 19172477 | threshold-and-level-access | T3 clinical | `harm_finding = 1`. **⚠ Crossref returns a duplicated author list** (Bennett/Kirby each twice, 5 entries). **PubMed's 3-author list is correct; store PubMed's.** |
| **C-g** Erickson, Brett; Hosseini, Masih A.; Mudhar, Parry Singh; Soleimani, Maryam; Aboonabi, Arina; Arzanpour, Siamak; Sparrey, Carolyn J. (2016). *The dynamics of electric powered wheelchair sideways tips and falls.* **J Neuroeng Rehabil 13:20** | DOI `10.1186/s12984-016-0128-7`, PMID 26935331 | threshold-and-level-access | T1 | `harm_finding = 1`. Note: crash-test-dummy reconstruction + rigid-body model, **not human participants** — grade population accordingly. |
| **C-h** Devasahayam, Augustine J.; Kelly, Liam P.; Wallack, Elizabeth M.; Ploughman, Michelle (2019). *Oxygen Cost During Mobility Tasks and Its Relationship to Fatigue in Progressive Multiple Sclerosis.* **Arch Phys Med Rehabil 100(11):2079–2088** | DOI `10.1016/j.apmr.2019.03.017` | stair-ramp-threshold-biomechanics + threshold-and-level-access | T3 clinical | n = 14 MS + 8 controls. **The 3.60× step-climbing figure.** Small n; grade PARTIAL. |
| **C-i** Waluś, Konrad J.; Warguła, Łukasz; Wieczorek, Bartosz; Krawiec, Piotr (2022). *Slip risk analysis on the surface of floors in public utility buildings.* **Journal of Building Engineering 54:104643** | DOI `10.1016/j.jobe.2022.104643` | stair-ramp-threshold-biomechanics (E-07) | T3 clinical | **The only slip study found that tests assistive-device ferrule tips.** Resolve the SVR↔PTV scale question before use. |
| **C-j** Horak, Jiri; Kukuliac, Pavel; Koktava, Nikola; Orlikova, Lucie; Maresova, Petra (2025). *Impact of street-level barriers on walking accessibility for persons with declining mobility: Comparison of two cities.* **Cities 166:106220** | DOI `10.1016/j.cities.2025.106220`; preprint also exists at `10.2139/ssrn.4973837` (2024) — **do not store the preprint DOI as the citation** | accessible-circulation-geometry | T3 clinical | Network-scale modelling of width (150/90 cm) and gradient (5%/12.5%) thresholds. |
| **C-k** Usui, Hiroyuki; Hino, Kimihiro (2019). *Density of resting places and maximum continuous walking distance of elderly persons.* **Journal of Architecture and Planning (Transactions of AIJ) 84(762):1779–1787** | DOI `10.3130/aija.84.1779`, ISSN 1340-4210 / 1881-8161, Architectural Institute of Japan | accessible-circulation-geometry (E-10) | T3 | **R5 NOTE: this is a Japanese peer-reviewed academic journal — ACADEMIC, not grey.** Abstract is in English; body language not confirmed. **Its 65%/70% figures are second-hand (§4.6) — stage for citation mining, do not admit as the E-10 anchor.** |

**Identity NOT resolved — `PENDING-VERIFICATION`, do not store any bibliographic field:**

| Candidate | What I have | Why held |
|---|---|---|
| **C-l** Cortis, Judith et al. (2015). "Traumatic asphyxia — fatal accident in an automatic revolving door." *International Journal of Legal Medicine.* | Title, first author, year, journal — **from a Consensus rendering only.** No DOI retrieved. | **HYPOTHESIS (R15).** High-value harm case for E-11. Resolve before any use. |
| **C-m** Flemmer, C. et al. (2026). "Analysis of the effect of path cross slope on manual wheelchair propulsion." *Disabil Rehabil Assist Technol.* | Title, first author, year, journal — Consensus only. No DOI. Reports a **3% critical cross slope**. | **HYPOTHESIS.** Theoretical mechanics, not empirical — tier accordingly (likely T3). |
| **C-n** Chew, Michael Yit Lin et al. (2024). "An Evidence-Driven Approach to Slip and Fall Prevention in Large Campus Facilities." *Buildings.* | Consensus only. Carries the tactile-indicator traction warning. | **HYPOTHESIS.** MDPI *Buildings*; verify. |
| **C-o** Cui, X. et al. (2022). "Improved Interpretation of British Pendulum Test Measurements for Evaluation of Floor Slip Resistance." *J Testing and Evaluation.* | Consensus only. Carries the >20% inter-device variation figure. | **HYPOTHESIS.** Metrology, but decisive for how precisely E-07 can be stated. |
| **C-p** Usui, Hiroyuki (2022). "Furthest Neighbour Distance Distribution Function…" *Applied Spatial Analysis and Policy.* | Consensus only. | **HYPOTHESIS.** |
| **C-q** Higuchi, T. et al. (2004, *J Exp Psychol Appl*) and (2009, *J Physiological Anthropology*) — perception of passable aperture width, including **tetraplegic** participants. | Consensus only. | **HYPOTHESIS.** Genuinely novel angle for E-08: whether users can *judge* a passable width, not just fit through it. |
| **C-r** Floyd, W. et al. (1965). "A study of the space requirements of wheelchair users." *Paraplegia* — 91 male + 36 female patients, Stoke Mandeville; 5th/95th percentile diagrams. | Consensus only. | **HYPOTHESIS.** Likely the **historical origin** of European wheelchair space standards. High archaeological value. |
| **C-s** Ownsworth, Anne (1973). *Housing for the Disabled, Part One: An Ergonomic Study of the Space Requirements of Wheel-chair Users for Doorways and Corridors.* Institute for Consumer Ergonomics, Loughborough. Surfaced via a 1974 *Ergonomics* review by Convie, L. | Consensus only. | **HYPOTHESIS.** Possibly the origin of UK corridor/doorway widths. Grey-tier report. |

**`OUT-OF-SCOPE`:** FES/orthotic glove studies; wheelchair-cushion FEA; robotic curb-climbing wheelchairs;
BMI-validity-in-SCI work; weight-prediction equations; UAV routing; fish turning dynamics.

**`MISCELLANEOUS` (on-topic, no clear slug home):** Huang et al. 2025 `10.1371/journal.pone.0335663`
(campus wheelchair travel speeds 1.03 m/s assisted vs 0.67 m/s unassisted) — the **speed differential is
useful for temporal accessibility**, but the 1:5 curb-ramp tolerance claim must not travel with it.

---

## 8. CITATION-MINING LEADS (R2)

All DOIs below were resolved against Crossref this session. **All checked against `source_locators` — every
one is NEW (not held).**

**Backward from A1 (Rouvier 2022) — its included-study set. This is the primary ramp/curb corpus:**
| Reference | DOI | Why |
|---|---|---|
| Chow, John W.; Millikan, Tim A.; Carlton, Les G.; Chae, Woen-sik; Lim, Young-tae; Morse, Marty I. (2009). *Kinematic and Electromyographic Analysis of Wheelchair Propulsion on Ramps of Different Slopes for Young Men With Paraplegia.* Arch Phys Med Rehabil 90(2):271–278 | `10.1016/j.apmr.2008.07.019` | Slopes 0–12°; **"major adjustments in stroking kinematics and significant increases in muscle activity occurred at slopes between 4° and 10°"** — i.e. the change-point sits at and above 1:12, not at 1:20. n = 10 young men with paraplegia (**EXACT diagnosis, narrow demographic**). |
| Gagnon, Dany; Babineau, Annie-Claude; Champagne, Audrey; Desroches, Guillaume; Aissaoui, Rachid (2015). BioMed Research International 2015:636319 | `10.1155/2015/636319` | **n = 18 SCI, slopes 0°, 2.7°, 3.6°, 4.8°, 7.1° — this set brackets 1:20 (2.86°) and 1:12 (4.76°) precisely.** The single best-designed study for the E-03 question. **Take this one first.** |
| Gagnon, Dany H. et al. (2014). J Rehabil Res Dev 51(5):789–802 | `10.1682/jrrd.2013.07.0168` | Pushrim kinetics, same slope-increment design. |
| Morrow, Melissa M.B.; Hurd, Wendy J.; Kaufman, Kenton R.; An, Kai-Nan (2010). J Electromyogr Kinesiol 20(1):61–67 | `10.1016/j.jelekin.2009.02.001` | 12 experienced MWC users; **ramp propulsion produced significantly higher shoulder moments than any other daily task except weight relief.** |
| van Drongelen et al. (2005) — 10 cm curb, n = 5 | not resolved | The other of only two curb studies. |

**Forward / adjacent:**
| Reference | DOI | Why |
|---|---|---|
| Gauthier, Cindy; Grangeon, Murielle; Ananos, Ludivine; Brosseau, Rachel; Gagnon, Dany H. (2017). Ann Phys Rehabil Med 60(5):281–288 | `10.1016/j.rehab.2017.02.007` | **Cardiorespiratory** responses to slope increments — the aerobic-cost bridge between the propulsion literature and the AX-STA framing. |
| Kwarciak, Andrew M.; Cooper, Rory A.; Fitzgerald, Shirley G. (2008). J Rehabil Res Dev 45(1):73–84 | `10.1682/jrrd.2006.11.0142` | **Curb DESCENT**, 5/10/15 cm, whole-body vibration. One of the very few descent studies. Complements the project's held WBV rows `REF-00183`, `REF-00249`, `REF-00347`, `REF-00373`. |
| Briley, Simon J.; Vegter, Riemer J.K.; Goosey-Tolfrey, Vicky L.; Mason, Barry S. (2021). J Biomech 126:110626 | `10.1016/j.jbiomech.2021.110626` | **Longitudinal** shoulder pain ↔ propulsion biomechanics — the cumulative-harm link. |
| Moon, Y. et al. (2013). Clin Biomech 28(9–10):967–972 | `10.1016/j.clinbiomech.2013.10.004` | Peak shoulder force in users **with and without shoulder pain**. |
| Sivakanthan, S. et al. (2021). Sensors 21(23):7810 | `10.3390/s21237810` | Curb negotiation; device-side, low priority. |

**Backward from E-10 (highest-value lead in this brief):** the Japanese primary source behind
**65% satisfied at <100 m / 70% at <50 m**, cited second-hand by Usui & Hino 2019 (`10.3130/aija.84.1779`).
Mine that paper's reference list. If it resolves to a single survey, it plausibly explains **both**
`REF-00162` (BS 8300-1 / Manual for Streets, 100 m) **and** `REF-00511` (50 m) — turning an apparent
cross-jurisdiction convergence into a single-ancestor artefact (`tier-system.md` §3).

**Held-but-thematically-adjacent stash rows to cross-file rather than re-acquire:** `REF-00044` and
`REF-00468` (IDeA Center wheeled-mobility anthropometry — same programme as A2/C-c); `REF-00467`
(RESNA wheelchair turning radius, GREY, DOI required); `REF-00153` (BS 8300-2:2018 Annex G Tables
G.7–G.8, power WC turning geometry); `REF-00008`/`REF-00043` (wheelchair & walker users passing through
doors, AAATE 2016 — **note `REF-00008`'s stored DOI `10.1080/09602011.2021.1893192` is a
neuropsychological-rehabilitation DOI and cannot be this paper**); `REF-00277` (CLARITY achondroplasia
anthropometrics n = 1,374 — **the only LPA anthropometric lead the project holds, and it needs a DOI**);
`REF-00474` (Templer, *The Staircase*, MIT Press).

---

## 9. MY ADJUDICATION OF VALUE

**What bears on an actual determination, versus what is merely topical.**

*Bears on a determination:*
- **Rouvier 2022** is the highest-value single source in the batch, and mostly for what it says is
  **missing**: ascent-only, no descent, no threshold crossing, four cross-slope studies, two curb
  studies, ~29% able-bodied samples. A systematic review's map of an absence is the strongest form of
  "evidence of absence" available, and it is stronger than any single positive finding here.
- **Geoerg 2019's specific-flow invalidity** is the batch's best transferable finding. It attacks the
  *derivation* of width rules rather than a width number, so it survives being wrong about any
  particular millimetre.
- **D'Souza 2010 / Bharathy 2018** are the primary anthropometric work the
  `manoeuvring-footprint-vs-turning-radius-methodology` slug was looking for, and both conclude the
  prescribed dimensions are too small — specifically for power chairs and scooters.
- **Kim 2026's 8.3% zero grip force** reframes I-01 from a magnitude question to a modality question.
- **Lalumiere 2013** gives the level-change demand gradient, though not at the height the clause uses.

*Merely topical, and I am saying so:*
- The wheelchair-skills-training literature. It measures the user's trained capability. Admitting it
  would put the burden on the person rather than the building.
- The slip-resistance metrology cluster. Real and rigorous, but about *instruments*, not outcomes.
- Most of the walkability/15-minute-city corpus.

**Where the evidence contradicts or qualifies the item names.** Five places, in order of force:
1. **I-01 (≤22 N).** The only primary human-factors number on doors is a **torque** (<30 N·m), not a
   force, and the two are not interconvertible without the moment arm that the same study says is
   habitually assumed wrong. And for 8.3% of men in an SCI wheelchair-user sample, **no** force ceiling
   is operable, because they generate no grip at all. The item measures the wrong quantity for the
   wrong constraint.
2. **E-03 (≤1:20).** No threshold at 1:20 exists in the literature — demand rises continuously. The
   nearest thing to a change-point is Chow 2009's *"major adjustments… between 4° and 10°"*, which is
   1:12 and steeper. Worse, the whole evidence base is ascent-only, and **none of it studies MS**,
   which is the item's own stated rationale.
3. **E-08 (≥1200 mm).** The flow-per-metre model underneath width rules does not hold when wheelchair
   users are present (Geoerg 2019), and at 0.90 m the measured flow penalty was ~30% (Geoerg 2022).
   Separately, the IDeA Center line says prescribed clear floor areas are already too small for power
   chairs. 1200 mm is not refuted; its *derivation* is.
4. **E-07 (PTV ≥36 wet).** Inter-device variation exceeds 20%; the property degrades in service, worst
   at stair edges and lift entrances; and Waluś's own abstract mixes PTV and SVR. The number is stated
   more precisely than it can be measured or maintained.
5. **E-11 (automatic sliding doors).** Specified as an access provision; 38,720 US ED visits per decade,
   with older adults at **3.18× the odds of severe injury**. The item carries no safety condition.

**What is genuinely absent from the literature, as distinct from absent from my search.** I am
separating these carefully because R14 requires it.

*Genuinely absent — adjudicated by a systematic review, not by my failure to find it:*
- **Descending slopes.** 25 of 25 slope studies are ascent-only, and Rouvier says so explicitly.
- **Door-threshold crossing.** Named by Rouvier as unstudied. E-05, E-06 and the whole
  `threshold-and-level-access` slug rest on a biomechanical literature that does not exist.
- **Cross-slope.** Four studies, 7–25 participants each.
- **Curbs.** Two studies in the entire review.

*Suggestive of absence, but NOT established — my own null result (query #12), stated at its true strength:*
- **The spatial accommodation of large-bodied wheeled-mobility users.** A well-formed, deliberately
  broad three-concept PubMed query returned its complete result set (23 records, `has_more: false`).
  **I resolved 7 of those 23 to full metadata. Not one of the 7 measures how much space a bariatric
  wheelchair user occupies or needs** — all are obesity *diagnosis* or body-composition work. **The
  remaining 16 I never read.**
  **Corrected 2026-09-01.** The first version of this brief said "all 23 returned… not one measures"
  and called this "close to genuine absence" and "the most important negative finding in the batch".
  That overstated it: 7 records read cannot license a claim about 23, and the slide from *returned* to
  *screened* is exactly the move R14 exists to prevent. **The honest status is: suggestive, unproven,
  and cheap to settle** — resolving 16 PMIDs would either confirm the gap or refute it in one pass.
  It should be recorded as an open question, not as a finding.
  The underlying concern still stands on its own terms: **`A-SIZE` is framed in this repository as the
  environment being wrongly normed to an average body**, and this project currently holds no
  large-bodied wheeled-mobility anthropometry at all. Same for **LPA** and **TALL** — the only LPA
  anthropometric lead held is `REF-00277` (CLARITY, achondroplasia, n = 1,374), which is GREY and has
  no DOI. Those are statements about *the project's corpus*, which I have checked, rather than about
  *the literature*, which I have not.
- **Post-exertional malaise in the built environment.** Query #13 named PEM explicitly and returned zero
  PEM work — every hit was MS oxygen cost. TERM-053 covers "fatigue **and** post-exertional malaise";
  the evidence reaches only the first, and the two are not the same construct.

*Absent from my search, not from the literature — do not read these as gaps:*
- **Stair geometry and falls** (query #10, 263 PubMed results, deliberately not mined). This is a large
  literature and deserves a dedicated pass. E-07's stair-nosing dimension and any future rise/going
  item should not be written until it is run.
- **Lifts (E-01, E-02).** I ran **no** dedicated lift-dimension search. The project's lift evidence is
  currently all code-tier (`REF-00173` EN 81-70, `REF-00352` ADM guidance). **E-01's 1400×1100 mm has no
  primary evidence in this batch and I did not look for any.** Stated so nobody infers absence.
- **H-04 (intercom / video entry).** Not searched at all. Zero coverage from me; it is closer to
  AGONIST-1's sensory territory.
- **E-04 (parking 3600 mm) and E-05 (canopy 3000×2000 mm).** Not searched. No coverage.

**A methodological finding about this repository, not about the literature.** The R9 pre-check
surfaced something that should go to the orchestrator regardless of what is admitted:
- `source_locators` contains **32 DOIs held under two or more `ref_id`s**, up to **five** for one DOI
  (`10.31030/1803049` → REF-00144, REF-00207, REF-00323, REF-00412, REF-00431).
- **`REF-00037` holds Rouvier 2022's DOI in its `doi` column while its `title`, `authors`, `pub_year`
  and `tier_claimed` columns describe the RIBA/Habinteg *Inclusive Housing Design Guide*.** The DOI and
  the bibliography in one row belong to two different works. `REF-00008` shows the same shape (a
  wheelchair/walker door-passage title carrying a neuropsychological-rehabilitation DOI).
- **Consequence for method:** a keyword scan of `source_locators.title` **cannot** find held DOIs, and
  my own first-pass title scan missed Rouvier entirely. **R9 pre-checks must be run on the `doi` column
  directly.** This is a concrete instance of the OD-5 defect (the R9 duplicate gate cannot see
  `source_locators`) and it is worse than a coverage gap — the index actively mis-associates.
- My recommendation: **mint a new `ref_id` for Rouvier** rather than promoting `REF-00037`, whose
  bibliographic identity belongs to the Habinteg guide, and raise the cross-contamination separately.

---

## 10. WHAT I COULD NOT VERIFY

Named field by field. Nothing below should be stored.

1. **I guessed a DOI and it was wrong.** Reaching for Shapovalov et al., I constructed
   `10.1016/j.ajem.2025.09.049`. It resolved — to *"Inequities in imaging: The association between
   patient demographics and use of point-of-care ultrasound in the ED"* by Brown, Meeker, Samuels-Kalow
   et al. A plausible-looking DOI resolved cleanly to an entirely different paper. The correct
   identifier, obtained via PubMed (PMID 41192188), is **`10.1016/j.ajem.2025.10.042`**. The bad payload
   is still in the retrieval log as `crossref_10.1016_j.ajem.2025.09.049.json` — **it is evidence of the
   error, not a source; do not read it as one.**
2. **Geoerg 2019 (A3) full text — NOT obtained.** `downloads.hindawi.com` → HTTP 403;
   `onlinelibrary.wiley.com/doi/pdfdirect` → HTTP 403; DOAJ record's only "fulltext" link is the DOI.
   Four rungs taken (Crossref → Semantic Scholar → Unpaywall → DOAJ). **Unverified: every quantified
   value in that paper — corridor widths, bottleneck widths, flows, densities, speeds, sample
   composition.** Only the abstract is verified.
3. **Geoerg 2025 (C-b) — pooled effect size and confidence interval NOT verified.** Springer redirects
   to `idp.springer.com`. All I have is the abstract's "close to three standard deviations". **Do not
   store a numeric effect size or CI.**
4. **D'Souza 2010 (A2) and Bharathy 2018 (C-c) — no millimetre values verified.** Both paywalled;
   abstracts only. **Unverified: every percentile, every clear-floor-area dimension, the device-class
   breakdown, and whether the samples stratify by body size.** Any mm figure attributed to them is
   `[UNVERIFIED-QUANT]`.
5. **Chang & Drury 2007 (A4) — numbers are abstract-level.** The 30 N·m / 250–350 mm / 1000–1500 mm
   values were corroborated independently in two payloads (Crossref-linked publisher abstract and Europe
   PMC `resultType=core`), but **I have not read the full text and cannot give a page or table number.**
   Unverified: the door population sampled, the site, the measured torque distribution, and whether the
   sample contained any disabled participants (I infer not; it is not stated).
6. **Lalumiere 2013 (A5) — no moment or MUR magnitudes verified.** Paywalled; abstract only. Unverified:
   every numeric moment, every MUR value, participant demographics beyond "15 MWU with SCI".
7. **Rooney 2021 (A6) — publication year unresolved.** Crossref `issued` = 2021-07-09; volume/issue
   24(2) belongs to a 2022 issue. **I did not resolve which is the citable year.** Store both with a
   `pub_year_note`. Also unverified: the individual study characteristics behind the pooled SMD.
8. **Kim 2026 (C-d) — abstract only, single author, very recent.** Unverified: the 26 seated measures,
   all percentile values, the definition and protocol behind "no grip force", and whether the Size Korea
   wheelchair subsample is representative. **The 8.3% figure is important enough that it must be read in
   full before it anchors anything.**
9. **Waluś 2022 (C-i) — the SVR↔PTV scale relationship is unverified.** The abstract uses both terms.
   Until the full text is read, no SVR figure may be compared with "PTV ≥36".
10. **Geoerg 2022 (C-a) — table and figure numbers are as reported by the retrieval tool.** I read a
    rendered full text, not the PDF. The values (0.9/1.2 m, 2.4 m, J = 1.30 vs 0.91–0.95 s⁻¹, 0.89/0.86/
    0.80 m, the 5 manual / 2 electric split) are from that rendering. **The specific "Table 3"/"Table 5"
    attributions should be re-checked against the PDF before they appear in a citation.** The abstract-level
    facts (N = 252, 12 studies, the three main findings) are independently confirmed via Europe PMC.
11. **Candidates C-l through C-s — NOTHING verified.** For each I have a title, a first author, a year
    and a journal **as rendered by Consensus, and nothing else.** No DOI was retrieved for any of them.
    **Per R15 every description of them in §7 is a HYPOTHESIS.** No author list, no page range, no
    volume, no DOI from that block may be stored.
12. **Author-list corrections made this session, and the one I could not make.**
    - **Corrected:** Consensus gave Geoerg 2019 five authors including "Haghani, M."; Crossref, Semantic
      Scholar and DOAJ each independently give **four**, without Haghani. Consensus's string is wrong.
    - **Corrected:** Crossref returns Bennett 2009 with a **duplicated** author list (5 entries, Bennett
      and Kirby each twice). PubMed's three-author list is correct.
    - **Could not correct:** I have no way to confirm, for any paywalled paper here, that the Crossref
      author list is *complete* — Crossref truncation is silent. For A2, A4, A5 and A6 I am relying on
      Crossref alone for completeness. **None of these has been diffed against the published byline.**
13. **Not searched at all, so nothing is verified either way:** lift car dimensions (E-01), platform
    lifts (E-02), accessible parking bay width (E-04), entrance canopy dimensions (E-05), intercom and
    video door entry (H-04), and stair rise/going geometry (E-07's stair component).
