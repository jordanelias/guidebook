# Per-Slice Evidentiary Audit
**Data as of:** 2026-08-22 · **Scope:** all 80 ACTIVE research slices (slugs) in `data/guidebook.db` · **Method:** read-only aggregation over `source_slug_links → evidence_sources`, `bpc_metadata`, and the frozen pre-log grids `search_languages` / `search_coverage` (labelled as history wherever used — live coverage comes from `search_executions` via `v_coverage_*`).

This audit scores every research slice on the six requested dimensions — (1) amount of evidence, (2) tiers of evidence, (3) jurisdictions sourced, (4) languages sourced, (5) English/Anglophone bias, and (6) overall quality of the evidentiary base — and rolls them into a transparent 0–100 composite grade. It audits the **raw evidence linked to each slice**, i.e. the material available for (re-)derivation; it does not re-judge synthesis prose.

> **Reproducibility.** Every number here is regenerated from the DB by `tools/evidentiary_audit.py` — nothing is hand-transcribed, and the “data as of” date is the DB’s own `max(updated_at)`, so identical data yields byte-identical output. No grade is stored in the DB; the composite is a *derived* view whose rubric is fully specified in §2, so any reader can recompute it. Companion outputs: `evidentiary-base-audit.json` / `.csv`, and the interactive `tools/evidentiary-audit-dashboard.html` (filter by corpus / category / term).

> **Adversarial review (two passes).** The audit was independently red-teamed twice; all raw counts (volume, tiers, language/jurisdiction distributions, search yield) reproduce exactly through a second code path. Folded in: (i) the **weighted-strength bands** (§8, DR-2026-07-20) — every slice is graded by the strongest band it can anchor at: ● full (T1/Co-1/T2/Co-2/T3-clinical), ◐ partial (T4/T5 standards), ○ weak (T3-grey/T6/grey); a ○ weak-only slice carries the honesty flag in place of the retired binary no-anchor flag (§2, §4); (ii) **DISPUTED sources** (0 instances) stripped of anchoring per the anti-fabrication sweep (§4) — retained in raw totals but counted at no band; (iii) a **convergence discount** (scoped to the ○ weak band) so code-floor-only slices can’t score highly on breadth alone (§2, §6); (iv) full disclosure of the **5 NULL-jurisdiction instances** (§3.5); (v) **true-jurisdiction** breadth scoring of the jurisdiction column (no language codes are currently mis-filed there).

## 1. Executive summary

- **5 source-instances** are linked across **1 of 80 slices**; **79 slices carry zero linked evidence**.
- **Grade distribution:** A=0 · B=0 · C=0 · D=1 · E=0 · F=79  (A≥80, B≥65, C≥50, D≥35, E>0, F=empty).
- **Tier profile is code-and-clinical heavy, synthesis-light.** Of linked instances: T1=4, T2=1, T3=0, T4=0, T5=0, T6=0. Only **1 Tier-2 (systematic-review / evidence-based-standard) instances** exist across the whole corpus — the synthesis tier that best anchors best-practice claims is the thinnest.
- **Anchoring strength, banded.** Under the weighted-strength model (§8) every tier can anchor a best-practice claim, weighted by tier: **5/5 (100%)** of instances anchor at ● full strength (T1/Co-1/T2/Co-2/T3-clinical, adjudicated), 0 at ◐ partial (T4/T5 standards practice), 0 at ○ weak (T3-grey/T6/grey floor). By slice: **1 full · 0 partial · 0 weak-only** (of 1 evidenced). Every evidenced slice anchors at ● full or ◐ partial strength — none rests on a weak-only base.
- **Anglophone concentration is the dominant quality risk.** **5/5 (100%) of linked sources are English-language**; only 0 are non-English. By jurisdiction, 0 instances are native-Anglophone (US/UK/AU/CA/NZ/IE), 0 supranational (INT/EU/ISO), 0 other, 5 unrecorded.
- **Search breadth ≠ evidentiary yield.** Per the frozen pre-log coverage grids, slices were searched across **0 languages** and ~0 jurisdictions, but 0 searched languages () returned **zero** usable sources in **every** slice. The bias lives in what converted to evidence, not in search effort.

## 2. Method & definitions

**Slice = slug.** The 80 ACTIVE slugs are the unit of audit. Evidence is attributed through `source_slug_links`; each linked `evidence_sources` row is one *source-instance* (a source shared by two slices counts once in each). The 5 instances collapse to **5 unique sources** (reuse factor 1.0×; 0 sources span >1 slice, one — `REF-00607` — spans 1). Instance-weighting is deliberate — it measures per-slice coverage — but shared sources are re-counted, so corpus tier/language totals read ~0% above unique-source counts. (0 of the 5 rows in `evidence_sources` are linked to no active slug.)

**Tiers** follow `governance/tier-system.md`. Tier number reflects *what kind of claim a source can anchor*, not raw quality. Under the **weighted-strength model** (§8, `DR-2026-07-20`) every tier can anchor a best-practice claim; the claim's *strength* is weighted by the tier of the evidence behind it. The three strength bands reuse the `●◐○` quality markers (§5), now given anchoring semantics:

| Band | Tiers | Anchoring behaviour |
|---|---|---|
| **● full** | T1, Co-1, T2, Co-2, T3-clinical | anchors a best-practice claim outright (adjudicated evidence) |
| **◐ partial** | T4, T5 | anchors as *current standards practice* — “standards basis, not primary evidence” |
| **○ weak** | T3-grey, T6, expert-consensus / thin base | anchors only a floor/convergence claim, honesty-flagged: “best available given current regulation/practice, **not** academically adjudicated” |

Each slice is graded by the **strongest band** it can anchor at (column **Band** in §4). The *convergence-not-evidence* rule is preserved as an honesty rule *within* the ○ weak band: multiple T4–T6 codes agreeing on a value is convergence of floors, stated as regulatory practice at weak strength — never relabelled best practice. A slice whose strongest anchor is ○ weak carries the **weak-only** flag (†), which replaces the retired binary *no-anchor* flag.

**DISPUTED sources.** Sources set `verification_status='DISPUTED'` by the anti-fabrication sweep (§4, `DR-2026-07-20`) have lost their VERIFIED standing and their ability to anchor a claim. They are **not deleted** (a disputed row is a recorded finding): the audit still counts them in raw volume / tier / jurisdiction / language totals, but they anchor at **no band** and earn no strength credit. The **disputed** count is surfaced per slice (§4 table, CSV, JSON) so the stripped anchoring is visible.

**Practitioner practice-stream.** A `practice` evidence_type (conceptually a “Co-3” authority stream, §3 / `DR-2026-07-20`) marks practitioner / firm design work placed *by method, not authorship* and ranked below Co-1/Co-2. The audit surfaces a **practice** count per slice and bands each such source by its method tier like any other source; it does not adjudicate the role-appropriate-authority gate (a firm may anchor a measured/descriptive claim but not a functional-need claim alone), which is a claim-level rather than slice-level judgment.

**Anglophone classification** of a jurisdiction: *native-Anglophone* = US, UK, AU, CA, NZ, IE; *supranational/English-medium* = INT, EU, ISO, ASEAN; *English-official (non-native)* = SG, HK, IN, NG, GH, ZA, MY, AE, SA; everything else *non-Anglophone*. Language uses `lang_detected` (`en`/`eng`→English).

**Composite score (0–100)** = five transparent components, higher = stronger base:

| Comp | Max | Measures |
|---|---|---|
| A Volume | 20 | count of linked source-instances |
| B Tier strength | 30 | ● full-band share (full weight) + ◐ partial-band share (partial) + full-anchor-present bonus |
| C Jurisdictional breadth | 20 | distinct *true* jurisdictions (mis-filed language codes excluded) |
| D Linguistic breadth | 15 | distinct languages; capped at 4 if English-only |
| E Anglophone balance | 15 | rewards distance from 100% English + 100% Anglo-core concentration |

Grades: **A**≥80 · **B**≥65 · **C**≥50 · **D**≥35 · **E**>0 · **F**=empty. The score rewards a *balanced, multi-jurisdiction, multi-language, synthesis-anchored* base and penalises thin or monolingual ones; it is a triage lens, not a verdict on any single citation.

**Convergence discount.** Scoped to the ○ weak band (§8 / `DR-2026-07-20` §1): a slice whose strongest anchor is weak (only T3-grey/T6/grey; no ● full or ◐ partial source) is a code / expert-consensus floor. Breadth of such sources across many jurisdictions is “convergence, not evidence,” and without a correction can out-score a genuinely well-evidenced but narrow slice purely on breadth. The rubric therefore **halves the breadth components (C, D) for ○ weak-only slices** (flagged †). A ◐ partial slice (T4/T5 standards) keeps full breadth credit — it anchors as standards practice, a real if secondary basis, not mere convergence.

## 3. Portfolio view, by dimension

### (1) Amount of evidence
| Linked sources | Slices |
|---|---|
| 0 (empty) | 79 |
| 1–3 | 0 |
| 4–7 | 1 |
| 8–14 | 0 |
| 15+ | 0 |

Median linked sources among non-empty slices: **5**. Largest bases: `room-acoustic-performance` (5).

### (2) Tiers of evidence
| Tier | Instances | Share |
|---|---|---|
| T1 | 4 | ████████████████···· 80% |
| T2 | 1 | ████················ 20% |
| T3 | 0 | ···················· 0% |
| T4 | 0 | ···················· 0% |
| T5 | 0 | ···················· 0% |
| T6 | 0 | ···················· 0% |

**Strength-band split of instances:** **5/5 (100%)** anchor at ● full (T1/Co-1/T2/Co-2/T3-clinical), 0 (0%) at ◐ partial (T4/T5 standards), and 0 (0%) at ○ weak (T3-grey/T6/grey floor). No evidenced slice rests on a ○ weak-only base — every slice anchors at ● full or ◐ partial strength (see the band breakdown in §4).

### (3) Jurisdictions sourced
Distinct jurisdiction strings across the corpus: **0**, none mis-filed as language codes in the `jurisdiction` column. Top: .

**1 non-empty slices draw on ≤1 jurisdiction** — monojurisdictional bases whose values may not transfer across code regimes. Separately, **5 source-instances carry no jurisdiction at all** (NULL) — mostly clinical/synthesis sources with no single national home; these are excluded from every jurisdiction-share denominator.

### (4) Languages sourced
| Language | Instances |
|---|---|
| en | 5 |

Distinct source languages: **1** (`en`/`eng` merged; raw ISO codes may be one more). English dominates at 100%. The non-English corpus is overwhelmingly Western-European + East-Asian; the only languages outside that group to yield *any* linked source are: none.

**1 non-empty slices are English-only** (100% of evidenced slices).

### (5) English / Anglophone bias
- **Language axis:** 100% English. 1 slices 100% English.
- **Jurisdiction axis (all 5 instances):** native-Anglophone (US/UK/AU/CA/NZ/IE) **0** · supranational/English-medium (INT/EU/ISO) **0** · English-official + other non-Anglophone **0** · **no jurisdiction recorded 5**. (These four sum to 5 = all instances.)
- **0 slices are doubly-concentrated** (≥90% English *and* ≥50% native-Anglophone jurisdiction): .
- **Process counter-evidence:** non-English/Global-South *searches were run* (0 languages across 0 of 80 slices per the frozen `search_languages` grid — a pre-log record, not a logged search) but  yielded nothing linkable in any slice. The gap is a *yield/recovery* gap, not a *search-effort* gap.

### (6) Overall quality of the evidentiary base
| Grade | Slices | Meaning |
|---|---|---|
| A | 0 | strong, balanced, synthesis-anchored |
| B | 0 | solid, some concentration or tier gaps |
| C | 0 | usable but thin or monolingual |
| D | 1 | weak — few sources / single jurisdiction / English-only |
| E | 0 | very weak — 1 jurisdiction, weak-only or thin base |
| F | 79 | empty — no linked evidence |

## 4. Master per-slice table (ranked by composite score)

Legend: **N** linked sources · **Band** strongest anchoring band (● full / ◐ partial / ○ weak / ⊘ disputed-only) · **●/◐/○** full / partial / weak instance counts · **⊘** DISPUTED instances (anchoring stripped, §4) · **JUR** distinct *true* jurisdictions · **LNG** distinct languages · **%EN** English-language share · **%ANG** native-Anglophone share · **A/B/C/D/E** score components · **†** ○ weak-only slice (breadth discounted, honesty-flagged).

| # | Grade | Score | Slice | Topic | N | Band | ● | ◐ | ○ | ⊘ | Tiers | JUR | LNG | %EN | %ANG | A·B·C·D·E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **D** | 42.0 | `room-acoustic-performance` | sensory-environment | 5 | ● | 5 | 0 | 0 | 0 | T1×4,T2×1 | 0 | 1 | 100.0 | — | 12·30·0·0·0.0 |
| 2 | **F** | 0 | `accessibility-feature-market-value-uplift-framing` | economics | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 3 | **F** | 0 | `accessible-bathroom-and-grab-bar` | bathrooms-and-wet-areas | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 4 | **F** | 0 | `accessible-circulation-geometry` | entrances-and-circulation | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 5 | **F** | 0 | `accessible-design-economics-cost-premium` | economics | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 6 | **F** | 0 | `accessible-design-failures-poor-performance` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 7 | **F** | 0 | `accessible-laundry-room-design` | room-types | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 8 | **F** | 0 | `acoustics-speech-intelligibility-disability` | sensory-environment | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 9 | **F** | 0 | `air-quality-voc-chemical-sensitivity-built-environment` | sensory-environment | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 10 | **F** | 0 | `assistive-listening-systems` | communication-and-alerts | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 11 | **F** | 0 | `bariatric-turning-radius-built-environment` | seating-and-rest | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 12 | **F** | 0 | `bathroom-typology-global-south` | bathrooms-and-wet-areas | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 13 | **F** | 0 | `biophilic-design-healthcare-workplace` | sensory-environment | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 14 | **F** | 0 | `body-sizes-supplementary-populations` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 15 | **F** | 0 | `case-study-economics-financial-data` | economics | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 16 | **F** | 0 | `circadian-lighting-melanopic-edi` | sensory-environment | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 17 | **F** | 0 | `co1-housing-research-global-south` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 18 | **F** | 0 | `cognitive-wayfinding-design` | wayfinding-and-signage | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 19 | **F** | 0 | `construction-cost-data` | economics | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 20 | **F** | 0 | `cross-population-case-studies` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 21 | **F** | 0 | `cross-population-conflict-resolutions` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 22 | **F** | 0 | `crpd-implementation-built-environment` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 23 | **F** | 0 | `deaf-acoustic-built-environment` | communication-and-alerts | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 24 | **F** | 0 | `deaf-classroom-reverberation-time` | communication-and-alerts | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 25 | **F** | 0 | `deaf-spatial-design` | communication-and-alerts | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 26 | **F** | 0 | `deafblind-built-environment-design` | population-general | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 27 | **F** | 0 | `dementia-built-environment` | population-general | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 28 | **F** | 0 | `design-framework-evidence-audit` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 29 | **F** | 0 | `detectable-gradient-protocol-sensory-zones` | wayfinding-and-signage | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 30 | **F** | 0 | `ecological-psychology-haptic-affordances-built-environment` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 31 | **F** | 0 | `economics-sources` | economics | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 32 | **F** | 0 | `european-accessibility-act-scope-clarification` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 33 | **F** | 0 | `floor-vibration-wheelchair-disability` | entrances-and-circulation | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 34 | **F** | 0 | `fold-down-grab-bar-specification` | bathrooms-and-wet-areas | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 35 | **F** | 0 | `government-grant-programmes` | economics | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 36 | **F** | 0 | `government-grant-programmes-home-adaptation` | economics | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 37 | **F** | 0 | `intellectual-disability-built-environment-design` | population-general | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 38 | **F** | 0 | `jurisdiction-grant-programmes-comprehensive` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 39 | **F** | 0 | `jurisdiction-matrix-accessibility-standards` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 40 | **F** | 0 | `luminance-contrast-and-pattern` | wayfinding-and-signage | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 41 | **F** | 0 | `luminance-contrast-lrv-evidence-base` | wayfinding-and-signage | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 42 | **F** | 0 | `manoeuvring-footprint-vs-turning-radius-methodology` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 43 | **F** | 0 | `mental-health-built-environment` | population-general | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 44 | **F** | 0 | `mobility-built-environment` | population-general | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 45 | **F** | 0 | `ms-thermal-temperature-conflict-resolution` | health-and-symptom-management | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 46 | **F** | 0 | `multilingual-evidence-convergence-non-english` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 47 | **F** | 0 | `ndv-aut-built-environment-quantified-thresholds` | population-general | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 48 | **F** | 0 | `neurodivergent-built-environment` | population-general | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 49 | **F** | 0 | `neurological-built-environment` | population-general | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 50 | **F** | 0 | `ofs-built-environment` | health-and-symptom-management | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 51 | **F** | 0 | `ot-built-environment-interface` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 52 | **F** | 0 | `ot-cpg-built-environment` | population-general | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 53 | **F** | 0 | `ot-frameworks-built-environment` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 54 | **F** | 0 | `pain-ofs-built-environment-design` | health-and-symptom-management | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 55 | **F** | 0 | `post-occupancy-evaluation-global` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 56 | **F** | 0 | `reach-range-and-accessible-controls` | controls-and-hardware | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 57 | **F** | 0 | `residential-accessible-home-case-studies` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 58 | **F** | 0 | `residential-dar-provisions-priority-register` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 59 | **F** | 0 | `residential-entry-and-threshold` | entrances-and-circulation | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 60 | **F** | 0 | `residential-kitchen-and-task-surfaces` | kitchens-and-workspaces | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 61 | **F** | 0 | `school-environment-autism` | sensory-environment | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 62 | **F** | 0 | `sensory-processing-model-design-application` | sensory-environment | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 63 | **F** | 0 | `sensory-relief-space-design` | sensory-environment | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 64 | **F** | 0 | `sensory-room-user-control` | sensory-environment | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 65 | **F** | 0 | `sensory-space-global-south` | sensory-environment | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 66 | **F** | 0 | `stair-ramp-threshold-biomechanics-accessibility` | entrances-and-circulation | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 67 | **F** | 0 | `therapeutic-lighting-design` | sensory-environment | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 68 | **F** | 0 | `thermal-comfort-older-adults-care-settings` | health-and-symptom-management | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 69 | **F** | 0 | `thermoregulation-built-environment` | health-and-symptom-management | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 70 | **F** | 0 | `threshold-and-level-access` | entrances-and-circulation | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 71 | **F** | 0 | `threshold-door-hardware` | entrances-and-circulation | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 72 | **F** | 0 | `upper-limb-impairment-built-environment` | population-general | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 73 | **F** | 0 | `vestibular-balance-built-environment` | health-and-symptom-management | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 74 | **F** | 0 | `visitability-residential-accessibility-minimum-standards` | frameworks-and-methodology | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 75 | **F** | 0 | `visual-alerting-and-wayfinding-light` | wayfinding-and-signage | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 76 | **F** | 0 | `visual-fire-alarm-seizure-safety` | sensory-environment | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 77 | **F** | 0 | `visual-impairment-built-environment` | population-general | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 78 | **F** | 0 | `wayfinding-cognitive-science-spatial-design` | wayfinding-and-signage | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 79 | **F** | 0 | `wayfinding-dementia-spatial-design` | wayfinding-and-signage | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 80 | **F** | 0 | `wayfinding-global-south` | wayfinding-and-signage | 0 | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |

**Anchoring bands across the 1 evidenced slices:** **1 ● full** (adjudicated anchor) · **0 ◐ partial** (standards-practice basis) · **0 ○ weak-only**.
- **† ○ weak-only (0)** — no evidenced slice rests on a weak-only base; every slice anchors at ● full or ◐ partial strength.

## 5. Evidence-empty slices (79)

These carry **zero** linked source-instances. `bpc_metadata.evidence_state` distinguishes:

**Retracted pending rehabilitation (0)** — prior work cleared, awaiting re-derivation:

**Un-started / placeholder (79)** — `evidence_state` unset, search not run:
- `accessibility-feature-market-value-uplift-framing` (economics)
- `accessible-bathroom-and-grab-bar` (bathrooms-and-wet-areas)
- `accessible-circulation-geometry` (entrances-and-circulation)
- `accessible-design-economics-cost-premium` (economics)
- `accessible-design-failures-poor-performance` (frameworks-and-methodology)
- `accessible-laundry-room-design` (room-types)
- `acoustics-speech-intelligibility-disability` (sensory-environment)
- `air-quality-voc-chemical-sensitivity-built-environment` (sensory-environment)
- `assistive-listening-systems` (communication-and-alerts)
- `bariatric-turning-radius-built-environment` (seating-and-rest)
- `bathroom-typology-global-south` (bathrooms-and-wet-areas)
- `biophilic-design-healthcare-workplace` (sensory-environment)
- `body-sizes-supplementary-populations` (frameworks-and-methodology)
- `case-study-economics-financial-data` (economics)
- `circadian-lighting-melanopic-edi` (sensory-environment)
- `co1-housing-research-global-south` (frameworks-and-methodology)
- `cognitive-wayfinding-design` (wayfinding-and-signage)
- `construction-cost-data` (economics)
- `cross-population-case-studies` (frameworks-and-methodology)
- `cross-population-conflict-resolutions` (frameworks-and-methodology)
- `crpd-implementation-built-environment` (frameworks-and-methodology)
- `deaf-acoustic-built-environment` (communication-and-alerts)
- `deaf-classroom-reverberation-time` (communication-and-alerts)
- `deaf-spatial-design` (communication-and-alerts)
- `deafblind-built-environment-design` (population-general)
- `dementia-built-environment` (population-general)
- `design-framework-evidence-audit` (frameworks-and-methodology)
- `detectable-gradient-protocol-sensory-zones` (wayfinding-and-signage)
- `ecological-psychology-haptic-affordances-built-environment` (frameworks-and-methodology)
- `economics-sources` (economics)
- `european-accessibility-act-scope-clarification` (frameworks-and-methodology)
- `floor-vibration-wheelchair-disability` (entrances-and-circulation)
- `fold-down-grab-bar-specification` (bathrooms-and-wet-areas)
- `government-grant-programmes` (economics)
- `government-grant-programmes-home-adaptation` (economics)
- `intellectual-disability-built-environment-design` (population-general)
- `jurisdiction-grant-programmes-comprehensive` (frameworks-and-methodology)
- `jurisdiction-matrix-accessibility-standards` (frameworks-and-methodology)
- `luminance-contrast-and-pattern` (wayfinding-and-signage)
- `luminance-contrast-lrv-evidence-base` (wayfinding-and-signage)
- `manoeuvring-footprint-vs-turning-radius-methodology` (frameworks-and-methodology)
- `mental-health-built-environment` (population-general)
- `mobility-built-environment` (population-general)
- `ms-thermal-temperature-conflict-resolution` (health-and-symptom-management)
- `multilingual-evidence-convergence-non-english` (frameworks-and-methodology)
- `ndv-aut-built-environment-quantified-thresholds` (population-general)
- `neurodivergent-built-environment` (population-general)
- `neurological-built-environment` (population-general)
- `ofs-built-environment` (health-and-symptom-management)
- `ot-built-environment-interface` (frameworks-and-methodology)
- `ot-cpg-built-environment` (population-general)
- `ot-frameworks-built-environment` (frameworks-and-methodology)
- `pain-ofs-built-environment-design` (health-and-symptom-management)
- `post-occupancy-evaluation-global` (frameworks-and-methodology)
- `reach-range-and-accessible-controls` (controls-and-hardware)
- `residential-accessible-home-case-studies` (frameworks-and-methodology)
- `residential-dar-provisions-priority-register` (frameworks-and-methodology)
- `residential-entry-and-threshold` (entrances-and-circulation)
- `residential-kitchen-and-task-surfaces` (kitchens-and-workspaces)
- `school-environment-autism` (sensory-environment)
- `sensory-processing-model-design-application` (sensory-environment)
- `sensory-relief-space-design` (sensory-environment)
- `sensory-room-user-control` (sensory-environment)
- `sensory-space-global-south` (sensory-environment)
- `stair-ramp-threshold-biomechanics-accessibility` (entrances-and-circulation)
- `therapeutic-lighting-design` (sensory-environment)
- `thermal-comfort-older-adults-care-settings` (health-and-symptom-management)
- `thermoregulation-built-environment` (health-and-symptom-management)
- `threshold-and-level-access` (entrances-and-circulation)
- `threshold-door-hardware` (entrances-and-circulation)
- `upper-limb-impairment-built-environment` (population-general)
- `vestibular-balance-built-environment` (health-and-symptom-management)
- `visitability-residential-accessibility-minimum-standards` (frameworks-and-methodology)
- `visual-alerting-and-wayfinding-light` (wayfinding-and-signage)
- `visual-fire-alarm-seizure-safety` (sensory-environment)
- `visual-impairment-built-environment` (population-general)
- `wayfinding-cognitive-science-spatial-design` (wayfinding-and-signage)
- `wayfinding-dementia-spatial-design` (wayfinding-and-signage)
- `wayfinding-global-south` (wayfinding-and-signage)

Several name high-salience topics where an empty base is a material coverage gap, not bookkeeping.

## 6. Findings & recommended remediation

1. **Strengthen the ◐ partial and ○ weak bases toward ● full.** 0 slices anchor only at ◐ partial (T4/T5 standards practice) and none rest on a ○ weak-only base. With only 1 systematic-review/evidence-based-standard instances corpus-wide, the ● full synthesis tier is the thinnest. Prioritise SR/meta-analysis + DPO-standard recovery on the partial/weak slices to lift them to full-strength anchoring.
2. **Convert non-English search into non-English evidence.** The pre-log grids record searches in 0 languages but the corpus is ~100% English. Target the languages already searched-with-results but under-linked, and the zero-yield languages () explicitly.
3. **De-risk monojurisdictional slices.** 1 evidenced slices rest on ≤1 jurisdiction; flag their numeric thresholds as non-transferable until a second regime is sourced.
4. **Fill or formally park the empty slices.** Move the 79 un-started slices into an active search queue or an explicit deferred state so they stop reading as silent gaps.
5. **Treat the doubly-concentrated slices as citation-risk.** The 0 ≥90%-English-and-≥50%-Anglophone slices are where global-applicability claims are weakest.

## 7. Limitations & what this audit does *not* claim

- **Instance-weighted, not source-weighted.** The 5 instances are 5 unique sources, so corpus tier/language totals run ~0% above unique-source counts. Per-slice figures are unaffected.
- **The composite is a lens, not ground truth.** Weights (20/30/20/15/15) are a defensible but editorial choice; the six raw dimensions are printed alongside every grade so a reader can re-weight. No grade is stored in the DB — it is recomputed each run.
- **Coverage ≠ correctness.** The audit measures the *shape* of each base (how much, what tier, where from, what language, how concentrated). It does **not** re-verify that any citation resolves, is current, or supports its claim — those are the `url_verification_runs` / `code_currency` / supersession checks, run separately.
- **Jurisdiction shares rest on recorded jurisdictions only.** NULL-jurisdiction instances are excluded from %ANG denominators, so a low %ANG can mean *genuinely non-Anglophone* or *unrecorded* — the master table’s JUR count exposes the denominator.
- **Compound jurisdictions classify by their strongest Anglophone member** (e.g. `US/AU/INT` counts as native-Anglophone). Magnitude ≈1% of instances.

## 8. Per-specification (item) adjudication — inheritance view

The Guidebook’s **93 design specifications** (the `items` table, categories A–K) do **not** carry their own evidence links — each *inherits* the evidentiary base of the research slug it draws on (`items.bpc_source_slug`). This section adjudicates every specification by that inherited base, so a spec built on a thin or unanchored slug is visible as such. (A spec with no source slug cannot inherit and is a coverage gap.)

| Basis health | Specs | Meaning |
|---|---|---|
| full | 13 | inherits a ● full (adjudicated) anchor base |
| empty-base | 74 | base has zero linked evidence |
| no-source | 6 | no source slug — cannot inherit |

**13 of 93 specs inherit a ● full or ◐ partial anchored base; 80 rest on a ○ weak, disputed-only, or missing base** and are the priority remediation set.

### By category
| Cat | Specifications | Specs | On weak/missing base |
|---|---|---|---|
| A | Acoustics | 19 | 6 |
| B | Lighting | 12 | 12 |
| C | Colour and Contrast | 6 | 6 |
| D | Wayfinding and Cognition | 11 | 11 |
| E | Circulation and Access | 14 | 14 |
| F | Sensory Environment | 8 | 8 |
| G | Furniture, Fixtures and Spatial Layout | 9 | 9 |
| H | Controls and Technology | 5 | 5 |
| I | Hardware and Fixtures | 4 | 4 |
| K | DeafBlind Provisions | 5 | 5 |

### Specifications resting on a weak or missing base

| Item | Category | Specification | Source slug | Basis | Inh. grade |
|---|---|---|---|---|---|
| `A-10` | A | Counter Hearing Loop (Induction Loop at Reception/Se | `assistive-listening-systems` | empty-base | F |
| `A-11` | A | Room Perimeter Hearing Loop (Assembly and Meeting Sp | `assistive-listening-systems` | empty-base | F |
| `A-12` | A | Auracast Infrastructure Readiness | `assistive-listening-systems` | empty-base | F |
| `A-13` | A | No Sound Masking in Neurological Population Environm | — | no-source | — |
| `A-15` | A | Acoustic Differentiation Between Spaces (Navigation  | — | no-source | — |
| `A-16` | A | Sensory Room / Quiet Room Provision (≥8 m², one per  | `sensory-relief-space-design` | empty-base | F |
| `B-01` | B | Circadian Lighting (≥150 EML Minimum at Eye Level in | `circadian-lighting-melanopic-edi` | empty-base | F |
| `B-02` | B | Diffuse Lighting for Lip Reading and Sign Language ( | `deaf-spatial-design` | empty-base | F |
| `B-03` | B | Elimination of Fluorescent Overhead Lighting | `therapeutic-lighting-design` | empty-base | F |
| `B-04` | B | Flicker-Free LED Luminaires (IEEE 1789-2015 Complian | `therapeutic-lighting-design` | empty-base | F |
| `B-05` | B | Gradual Lighting Transition Zones (≥5 m at All Major | `therapeutic-lighting-design` | empty-base | F |
| `B-06` | B | Individual Dimming Control (≥300 Lux Range) | `therapeutic-lighting-design` | empty-base | F |
| `B-07` | B | Indirect and Cove Lighting in Sensitive Spaces | `therapeutic-lighting-design` | empty-base | F |
| `B-08` | B | Matte, Low-Reflectance Floor Finishes (≤30 Gloss Uni | — | no-source | — |
| `B-09` | B | Maximisation of Natural Light (Clerestory, Light Wel | `biophilic-design-healthcare-workplace` | empty-base | F |
| `B-10` | B | Visual Fire Alarm (Strobe VAD Throughout Building) | `visual-fire-alarm-seizure-safety` | empty-base | F |
| `B-11` | B | Warm Colour Temperature for Evening (≤2700 K After 1 | `circadian-lighting-melanopic-edi` | empty-base | F |
| `B-12` | B | Sensor-Activated Overnight Pathway Lighting | `visual-alerting-and-wayfinding-light` | empty-base | F |
| `C-01` | C | Colour Palette (Muted, Low-Chroma, Non-Institutional | `wayfinding-dementia-spatial-design` | empty-base | F |
| `C-02` | C | Colour-Coded Wayfinding Zones (Distinct Warm Colour  | `wayfinding-dementia-spatial-design` | empty-base | F |
| `C-03` | C | Pattern Avoidance (Plain Flooring and Walls in Sensi | `luminance-contrast-lrv-evidence-base` | empty-base | F |
| `C-04` | C | LRV Contrast (≥30 at All Critical Junctions) | `luminance-contrast-lrv-evidence-base` | empty-base | F |
| `C-05` | C | Low LRV Differential at Adjacent Floor Materials (DE | `luminance-contrast-lrv-evidence-base` | empty-base | F |
| `C-06` | C | Plain, Low-Contrast Flooring Throughout (No Geometri | `luminance-contrast-lrv-evidence-base` | empty-base | F |
| `D-01` | D | Loop Floor Plan (No Dead-End Corridors in DEM Enviro | `wayfinding-dementia-spatial-design` | empty-base | F |
| `D-02` | D | Cognitive Simplicity (Single Primary Route from Entr | `cognitive-wayfinding-design` | empty-base | F |
| `D-03` | D | Toilet Visibility from Primary Occupied Spaces (No N | `wayfinding-dementia-spatial-design` | empty-base | F |
| `D-04` | D | Landmarks at Every Decision Point | `wayfinding-cognitive-science-spatial-design` | empty-base | F |
| `D-05` | D | Enclosed Low-Stimulation Spaces (Focus Rooms, Breako | `sensory-relief-space-design` | empty-base | F |
| `D-06` | D | Memory Boxes at Private Office and Residential Room  | `wayfinding-dementia-spatial-design` | empty-base | F |
| `D-07` | D | No Blind Corners (Curved or Mirrored at All Hidden J | `cognitive-wayfinding-design` | empty-base | F |
| `D-08` | D | Pictogram + Single-Word Signage Throughout | `cognitive-wayfinding-design` | empty-base | F |
| `D-09` | D | Consistent Furniture Layout (No Rearrangement Withou | `wayfinding-dementia-spatial-design` | empty-base | F |
| `D-10` | D | Transparent Glazed Panels in Internal Partitions | `cognitive-wayfinding-design` | empty-base | F |
| `D-11` | D | Safe Accessible Garden (Loop Path, Secured Perimeter | `wayfinding-dementia-spatial-design` | empty-base | F |
| `E-01` | E | Accessible Lift (1400×1100 mm Car, All Floors Served | `accessible-circulation-geometry` | empty-base | F |
| `E-02` | E | Platform Lift (Where Full Passenger Lift Not Achieva | `accessible-circulation-geometry` | empty-base | F |
| `E-03` | E | Ramp Gradient (≤1:20 — MS Fatigue and Temporal Acces | `stair-ramp-threshold-biomechanics-accessibility` | empty-base | F |
| `E-04` | E | Accessible Parking (3600 mm Width, Covered, Closest  | `accessible-circulation-geometry` | empty-base | F |
| `E-05` | E | Weather Protection at Entry (Covered Canopy Minimum  | `threshold-and-level-access` | empty-base | F |
| `E-06` | E | Level Entry (Zero Step at All Accessible Entrances) | `threshold-and-level-access` | empty-base | F |
| `E-07` | E | Slip Resistance (PTV ≥36 Wet Throughout All Circulat | `stair-ramp-threshold-biomechanics-accessibility` | empty-base | F |
| `E-08` | E | Corridor Clear Width (≥1200 mm Minimum on All Primar | `accessible-circulation-geometry` | empty-base | F |
| `E-09` | E | Tactile Walking Surface Indicators (ISO 23599:2019) | `detectable-gradient-protocol-sensory-zones` | empty-base | F |
| `E-10` | E | Rest Seating at Regular Intervals on All Accessible  | `accessible-circulation-geometry` | empty-base | F |
| `E-11` | E | Automatic Sliding Entry and Internal Doors | `threshold-door-hardware` | empty-base | F |
| `E-12` | E | Entrance Landing and Manoeuvring Space for Power Whe | `accessible-circulation-geometry` | empty-base | F |
| `E-13` | E | Entrance Cognitive Legibility Provisions | `cognitive-wayfinding-design` | empty-base | F |
| `E-15` | E | Changing Places Facility (Height-Adjustable Bench, O | `accessible-bathroom-and-grab-bar` | empty-base | F |
| `F-01` | F | Sensory Gradient (High to Low Stimulation from Entry | `sensory-processing-model-design-application` | empty-base | F |
| `F-02` | F | Olfactory Control (Fragrance-Free Zones in Sensitive | `air-quality-voc-chemical-sensitivity-built-environment` | empty-base | F |
| `F-03` | F | Graduated Stimulation Re-entry (Sensory Room to Gene | `sensory-relief-space-design` | empty-base | F |
| `F-04` | F | Air Quality (MERV 13+ Filtration, Low-VOC Specificat | `air-quality-voc-chemical-sensitivity-built-environment` | empty-base | F |
| `F-05` | F | Seated-Task Design (All Primary Occupational Tasks A | `ofs-built-environment` | empty-base | F |
| `F-06` | F | Fragrance-Free Policy (Whole-Building Operational St | `air-quality-voc-chemical-sensitivity-built-environment` | empty-base | F |
| `F-07` | F | Thermal Zoning — Building-Wide Temperature Managemen | — | no-source | — |
| `F-08` | F | Thermal Transition — Heating and Cooling System Resp | `thermoregulation-built-environment` | empty-base | F |
| `G-01` | G | Defensible Seating (Back-to-Wall, Entry Sightline Co | `mental-health-built-environment` | empty-base | F |
| `G-02` | G | Variety of Seating Types (Three Heights at Every Sea | — | no-source | — |
| `G-03` | G | Grab Bars in All Accessible Bathrooms (Clinical Posi | `accessible-bathroom-and-grab-bar` | empty-base | F |
| `G-04` | G | Accessible Bathroom (Wet Room Configuration — Zero T | `accessible-bathroom-and-grab-bar` | empty-base | F |
| `G-05` | G | Adjustable-Height Work Surfaces and Desks (650--870  | `residential-kitchen-and-task-surfaces` | empty-base | F |
| `G-06` | G | Reception Counter (Accessible Height Section — 760-- | `reach-range-and-accessible-controls` | empty-base | F |
| `G-07` | G | Waiting Area Seating (Accessible Configuration — Adj | — | no-source | — |
| `G-08` | G | Bedroom Wardrobe and Storage Reach Configuration | `reach-range-and-accessible-controls` | empty-base | F |
| `G-09` | G | Bedroom Emergency Call Provision and Overnight Light | `reach-range-and-accessible-controls` | empty-base | F |
| `H-01` | H | All Controls at Accessible Height (400--1100 mm AFF, | `reach-range-and-accessible-controls` | empty-base | F |
| `H-02` | H | Individual Environmental Control (Lighting and Tempe | `reach-range-and-accessible-controls` | empty-base | F |
| `H-03` | H | Visual Paging and Real-Time Captioning in Assembly S | `assistive-listening-systems` | empty-base | F |
| `H-04` | H | Accessible Intercom and Video Door Entry with Visual | `threshold-door-hardware` | empty-base | F |
| `H-05` | H | Emergency Call — Multi-Position Reach Envelope | `reach-range-and-accessible-controls` | empty-base | F |
| `I-01` | I | Hardware Throughout (Lever, D-Pull, One-Hand Operabl | `threshold-door-hardware` | empty-base | F |
| `I-02` | I | Kitchen (One-Handed Operation Throughout) | `residential-kitchen-and-task-surfaces` | empty-base | F |
| `I-03` | I | Bathroom (UPL Anti-Scald, Bilateral Grab Bars, One-H | `accessible-bathroom-and-grab-bar` | empty-base | F |
| `I-04` | I | Ceiling Hoist Provision | `accessible-bathroom-and-grab-bar` | empty-base | F |
| `K-01` | K | Intervenor Adjacency at Service Counters | `deafblind-built-environment-design` | empty-base | F |
| `K-02` | K | Tactile Building Map Station at Principal Entrance | `deafblind-built-environment-design` | empty-base | F |
| `K-03` | K | Haptic Communication Clear Floor Zone | `deafblind-built-environment-design` | empty-base | F |
| `K-04` | K | Vibrotactile Alert Provision | `deafblind-built-environment-design` | empty-base | F |
| `K-05` | K | Thermal Comfort Assessment for Thermoregulation-Impa | `thermoregulation-built-environment` | empty-base | F |

The full per-specification table (all 93 items with inherited grade and dimension snapshot) is in `evidentiary-base-audit-items.csv` and the `items` array of the JSON; the dashboard’s **Specifications** view filters them by corpus / category / term.

---
*Data as of 2026-08-22 · read-only over `data/guidebook.db` · generated by `tools/evidentiary_audit.py`. Independently red-teamed; raw counts reproduce through a second code path. Aligned to `governance/tier-system.md`.*
