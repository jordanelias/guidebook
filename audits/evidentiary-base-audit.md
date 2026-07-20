# Per-Slice Evidentiary Audit
**Data as of:** 2026-07-20 · **Scope:** all 79 ACTIVE research slices (slugs) in `data/guidebook.db` · **Method:** read-only aggregation over `source_slug_links → evidence_sources`, `search_languages`, `search_coverage`, `bpc_metadata`.

This audit scores every research slice on the six requested dimensions — (1) amount of evidence, (2) tiers of evidence, (3) jurisdictions sourced, (4) languages sourced, (5) English/Anglophone bias, and (6) overall quality of the evidentiary base — and rolls them into a transparent 0–100 composite grade. It audits the **raw evidence linked to each slice**, i.e. the material available for (re-)derivation; it does not re-judge synthesis prose.

> **Reproducibility.** Every number here is regenerated from the DB by `tools/evidentiary_audit.py` — nothing is hand-transcribed, and the “data as of” date is the DB’s own `max(updated_at)`, so identical data yields byte-identical output. No grade is stored in the DB; the composite is a *derived* view whose rubric is fully specified in §2, so any reader can recompute it. Companion outputs: `evidentiary-base-audit.json` / `.csv`, and the interactive `tools/evidentiary-audit-dashboard.html` (filter by corpus / category / term).

> **Adversarial review (two passes).** The audit was independently red-teamed twice; all raw counts (volume, tiers, language/jurisdiction distributions, search yield) reproduce exactly through a second code path. Folded in: (i) the **weighted-strength bands** (§8, DR-2026-07-20) — every slice is graded by the strongest band it can anchor at: ● full (T1/Co-1/T2/Co-2/T3-clinical), ◐ partial (T4/T5 standards), ○ weak (T3-grey/T6/grey); a ○ weak-only slice carries the honesty flag in place of the retired binary no-anchor flag (§2, §4); (ii) **DISPUTED sources** (10 instances) stripped of anchoring per the anti-fabrication sweep (§4) — retained in raw totals but counted at no band; (iii) a **convergence discount** (scoped to the ○ weak band) so code-floor-only slices can’t score highly on breadth alone (§2, §6); (iv) full disclosure of the **77 NULL-jurisdiction instances** (§3.5); (v) **true-jurisdiction** breadth scoring that excludes the 0 language codes () mis-filed in the `jurisdiction` column (§3.3).

## 1. Executive summary

- **948 source-instances** are linked across **79 of 79 slices**; **0 slices carry zero linked evidence**.
- **Grade distribution:** A=11 · B=27 · C=25 · D=13 · E=3 · F=0  (A≥80, B≥65, C≥50, D≥35, E>0, F=empty).
- **Tier profile is code-and-clinical heavy, synthesis-light.** Of linked instances: T1=93, T2=113, T3=350, T4=86, T5=155, T6=151. Only **113 Tier-2 (systematic-review / evidence-based-standard) instances** exist across the whole corpus — the synthesis tier that best anchors best-practice claims is the thinnest.
- **Anchoring strength, banded.** Under the weighted-strength model (§8) every tier can anchor a best-practice claim, weighted by tier: **486/948 (51%)** of instances anchor at ● full strength (T1/Co-1/T2/Co-2/T3-clinical, adjudicated), 241 at ◐ partial (T4/T5 standards practice), 211 at ○ weak (T3-grey/T6/grey floor). **10 DISPUTED instances anchor at no band** (§4). By slice: **66 full · 13 partial · 0 weak-only** (of 79 evidenced). Every evidenced slice anchors at ● full or ◐ partial strength — none rests on a weak-only base.
- **Anglophone concentration is the dominant quality risk.** **716/948 (76%) of linked sources are English-language**; only 232 are non-English. By jurisdiction, 353 instances are native-Anglophone (US/UK/AU/CA/NZ/IE), 210 supranational (INT/EU/ISO), 308 other, 77 unrecorded.
- **Search breadth ≠ evidentiary yield.** Slices were searched across **19 languages** and ~48 jurisdictions, but 4 searched languages (`ar`, `bn`, `hi`, `sw`) returned **zero** usable sources in **every** slice. The bias lives in what converted to evidence, not in search effort.

## 2. Method & definitions

**Slice = slug.** The 79 ACTIVE slugs are the unit of audit. Evidence is attributed through `source_slug_links`; each linked `evidence_sources` row is one *source-instance* (a source shared by two slices counts once in each). The 948 instances collapse to **781 unique sources** (reuse factor 1.21×; 120 sources span >1 slice, one — `REF-00050` — spans 6). Instance-weighting is deliberate — it measures per-slice coverage — but shared sources are re-counted, so corpus tier/language totals read ~21% above unique-source counts. (23 of the 804 rows in `evidence_sources` are linked to no active slug.)

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
| 0 (empty) | 0 |
| 1–3 | 2 |
| 4–7 | 27 |
| 8–14 | 31 |
| 15+ | 19 |

Median linked sources among non-empty slices: **9**. Largest bases: `mental-health-built-environment` (37), `wayfinding-dementia-spatial-design` (35), `accessibility-feature-market-value-uplift-framing` (33), `room-acoustic-performance` (32), `threshold-door-hardware` (32).

### (2) Tiers of evidence
| Tier | Instances | Share |
|---|---|---|
| T1 | 93 | ██·················· 10% |
| T2 | 113 | ██·················· 12% |
| T3 | 350 | ███████············· 37% |
| T4 | 86 | ██·················· 9% |
| T5 | 155 | ███················· 16% |
| T6 | 151 | ███················· 16% |

**Strength-band split of instances:** **486/948 (51%)** anchor at ● full (T1/Co-1/T2/Co-2/T3-clinical), 241 (25%) at ◐ partial (T4/T5 standards), and 211 (22%) at ○ weak (T3-grey/T6/grey floor); a further 10 DISPUTED instances anchor at no band (§4). The 0 slices whose *strongest* anchor is ○ weak are the sharpest risk — see the band breakdown in §4.

### (3) Jurisdictions sourced
Distinct jurisdiction strings across the corpus: **50** — but **0 are language codes mis-filed in the jurisdiction column** ( = 0 instances; a data-integrity defect, see the note below), leaving **~50 true jurisdictions**. Top: INT (197), US (150), UK (99), DE (50), AU (46), CA (33), JP (30), NL (27), NO (26), SE (20).

**3 non-empty slices draw on ≤1 jurisdiction** — monojurisdictional bases whose values may not transfer across code regimes. Separately, **77 source-instances carry no jurisdiction at all** (NULL) — mostly clinical/synthesis sources with no single national home; these are excluded from every jurisdiction-share denominator.

> **Data-integrity note (§3.3).** The audit *surfaces rather than propagates* the mis-filed language codes: language codes appearing as `jurisdiction` values are almost certainly the source language leaking into the wrong column. Recommend a data fix moving these to `lang_detected` and recovering the true jurisdiction.

### (4) Languages sourced
| Language | Instances |
|---|---|
| en | 716 |
| de | 50 |
| ja | 30 |
| no | 23 |
| fr | 19 |
| nl | 17 |
| sv | 17 |
| zh | 15 |
| pt | 13 |
| ko | 11 |
| it | 10 |
| da | 9 |
| fi | 7 |
| es | 6 |
| ar | 2 |
| id | 2 |
| bn | 1 |

Distinct source languages: **17** (`en`/`eng` merged; raw ISO codes may be one more). English dominates at 76%. The non-English corpus is overwhelmingly Western-European + East-Asian; the only languages outside that group to yield *any* linked source are: ar (2); id (2); bn (1).

**36 non-empty slices are English-only** (46% of evidenced slices).

### (5) English / Anglophone bias
- **Language axis:** 76% English. 36 slices 100% English.
- **Jurisdiction axis (all 948 instances):** native-Anglophone (US/UK/AU/CA/NZ/IE) **353** · supranational/English-medium (INT/EU/ISO) **210** · English-official + other non-Anglophone **308** · **no jurisdiction recorded 77**. (These four sum to 948 = all instances.)
- **19 slices are doubly-concentrated** (≥90% English *and* ≥50% native-Anglophone jurisdiction): `accessibility-feature-market-value-uplift-framing`, `economics-sources`, `air-quality-voc-chemical-sensitivity-built-environment`, `upper-limb-impairment-built-environment`, `manoeuvring-footprint-vs-turning-radius-methodology`, `ot-built-environment-interface`, `sensory-relief-space-design`, `residential-accessible-home-case-studies`, `sensory-processing-model-design-application`, `government-grant-programmes`, `ot-frameworks-built-environment`, `ofs-built-environment`, `ot-cpg-built-environment`, `bariatric-turning-radius-built-environment`, `luminance-contrast-lrv-evidence-base`, `cross-population-case-studies`, `accessible-design-failures-poor-performance`, `case-study-economics-financial-data`, `residential-dar-provisions-priority-register`.
- **Process counter-evidence:** non-English/Global-South *searches were run* (19 languages across 81 of 79 slices in `search_languages`) but `ar`, `bn`, `hi`, `sw` yielded nothing linkable in any slice. The gap is a *yield/recovery* gap, not a *search-effort* gap.

### (6) Overall quality of the evidentiary base
| Grade | Slices | Meaning |
|---|---|---|
| A | 11 | strong, balanced, synthesis-anchored |
| B | 27 | solid, some concentration or tier gaps |
| C | 25 | usable but thin or monolingual |
| D | 13 | weak — few sources / single jurisdiction / English-only |
| E | 3 | very weak — 1 jurisdiction, weak-only or thin base |
| F | 0 | empty — no linked evidence |

## 4. Master per-slice table (ranked by composite score)

Legend: **N** linked sources · **Band** strongest anchoring band (● full / ◐ partial / ○ weak / ⊘ disputed-only) · **●/◐/○** full / partial / weak instance counts · **⊘** DISPUTED instances (anchoring stripped, §4) · **JUR** distinct *true* jurisdictions · **LNG** distinct languages · **%EN** English-language share · **%ANG** native-Anglophone share · **A/B/C/D/E** score components · **†** ○ weak-only slice (breadth discounted, honesty-flagged).

| # | Grade | Score | Slice | Topic | N | Band | ● | ◐ | ○ | ⊘ | Tiers | JUR | LNG | %EN | %ANG | A·B·C·D·E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **A** | 89.6 | `cognitive-wayfinding-design` | wayfinding-and-signage | 25 | ● | 16 | 7 | 2 | 0 | T2×6,T3×11,T5×7,T6×1 | 13 | 9 | 64.0 | 8.0 | 20·25.0·20·15·9.6 |
| 2 | **A** | 88.2 | `wayfinding-dementia-spatial-design` | wayfinding-and-signage | 35 | ● | 25 | 5 | 5 | 0 | T1×6,T2×9,T3×11,T5×5,T6×4 | 19 | 13 | 60.0 | 36.4 | 20·25.4·20·15·7.8 |
| 3 | **A** | 87.4 | `sensory-room-user-control` | sensory-environment | 14 | ● | 13 | 0 | 1 | 0 | T2×6,T3×7,T6×1 | 9 | 4 | 71.4 | 38.5 | 20·28.6·20·12·6.8 |
| 4 | **A** | 85.7 | `mental-health-built-environment` | population-general | 37 | ● | 27 | 3 | 6 | 1 | T1×3,T2×3,T3×28,T4×1,T5×2 | 11 | 5 | 59.5 | 27.0 | 20·25.2·20·12·8.5 |
| 5 | **A** | 85.4 | `stair-ramp-threshold-biomechanics-accessibility` | entrances-and-circulation | 27 | ● | 14 | 2 | 11 | 0 | T2×1,T3×14,T4×1,T5×1,T6×10 | 15 | 12 | 59.3 | 14.8 | 20·21.0·20·15·9.4 |
| 6 | **A** | 85.2 | `residential-kitchen-and-task-surfaces` | kitchens-and-workspaces | 30 | ● | 20 | 5 | 5 | 0 | T1×2,T2×12,T3×6,T4×2,T5×3,T6×5 | 10 | 7 | 80.0 | 46.2 | 20·24.7·20·15·5.5 |
| 7 | **A** | 84.9 | `mobility-built-environment` | population-general | 24 | ● | 14 | 4 | 6 | 0 | T1×7,T2×2,T3×6,T5×4,T6×5 | 17 | 9 | 58.3 | 50.0 | 20·23.0·20·15·6.9 |
| 8 | **A** | 84.8 | `room-acoustic-performance` | sensory-environment | 32 | ● | 19 | 10 | 3 | 0 | T1×14,T2×1,T3×6,T4×2,T5×8,T6×1 | 13 | 8 | 78.1 | 50.0 | 20·24.4·20·15·5.4 |
| 9 | **A** | 84.2 | `deaf-classroom-reverberation-time` | communication-and-alerts | 12 | ● | 2 | 7 | 3 | 0 | T1×2,T4×1,T5×6,T6×3 | 9 | 9 | 25.0 | 25.0 | 20·18.0·20·15·11.2 |
| 10 | **A** | 82.4 | `deaf-spatial-design` | communication-and-alerts | 13 | ● | 8 | 1 | 4 | 0 | T1×5,T2×1,T3×5,T5×1,T6×1 | 8 | 5 | 61.5 | 38.5 | 20·22.9·20·12·7.5 |
| 11 | **A** | 81.8 | `accessible-bathroom-and-grab-bar` | bathrooms-and-wet-areas | 23 | ● | 12 | 5 | 5 | 1 | T1×7,T2×4,T3×3,T4×1,T5×4,T6×4 | 13 | 7 | 73.9 | 65.0 | 20·22.2·20·15·4.6 |
| 12 | **B** | 79.5 | `wayfinding-global-south` | wayfinding-and-signage | 15 | ● | 1 | 4 | 10 | 0 | T3×1,T4×4,T6×10 | 13 | 7 | 53.3 | 0.0 | 20·13.5·20·15·11.0 |
| 13 | **B** | 78.0 | `accessible-circulation-geometry` | entrances-and-circulation | 14 | ● | 3 | 4 | 7 | 0 | T2×1,T3×2,T4×1,T5×3,T6×7 | 9 | 6 | 64.3 | 50.0 | 20·16.6·20·15·6.4 |
| 14 | **B** | 77.8 | `threshold-door-hardware` | entrances-and-circulation | 32 | ● | 2 | 10 | 20 | 0 | T3×2,T4×1,T5×9,T6×20 | 26 | 13 | 46.9 | 31.2 | 20·13.8·20·15·9.1 |
| 15 | **B** | 77.4 | `dementia-built-environment` | population-general | 8 | ● | 4 | 3 | 1 | 0 | T3×5,T5×3 | 5 | 4 | 62.5 | 12.5 | 16·23.0·17·12·9.4 |
| 16 | **B** | 77.2 | `residential-entry-and-threshold` | entrances-and-circulation | 20 | ● | 3 | 7 | 9 | 1 | T2×3,T3×1,T4×1,T5×6,T6×9 | 13 | 7 | 65.0 | 50.0 | 20·15.8·20·15·6.4 |
| 17 | **B** | 76.5 | `construction-cost-data` | economics | 12 | ● | 6 | 0 | 6 | 0 | T3×11,T6×1 | 8 | 3 | 58.3 | 41.7 | 20·20.0·20·9·7.5 |
| 18 | **B** | 76.2 | `post-occupancy-evaluation-global` | frameworks-and-methodology | 10 | ● | 10 | 0 | 0 | 0 | T2×3,T3×7 | 8 | 2 | 90.0 | 40.0 | 16·30·20·5·5.2 |
| 19 | **B** | 75.7 | `multilingual-evidence-convergence-non-english` | frameworks-and-methodology | 8 | ● | 3 | 2 | 3 | 0 | T3×6,T5×2 | 7 | 4 | 50.0 | 0.0 | 16·19.5·17·12·11.2 |
| 20 | **B** | 75.7 | `visual-impairment-built-environment` | population-general | 8 | ● | 1 | 3 | 4 | 0 | T2×1,T3×1,T4×2,T5×1,T6×3 | 7 | 6 | 25.0 | 12.5 | 16·15.5·17·15·12.2 |
| 21 | **B** | 75.0 | `accessible-design-economics-cost-premium` | economics | 14 | ● | 7 | 0 | 7 | 0 | T3×13,T6×1 | 7 | 3 | 57.1 | 23.1 | 20·20.0·17·9·9.0 |
| 22 | **B** | 74.5 | `sensory-space-global-south` | sensory-environment | 15 | ● | 9 | 1 | 5 | 0 | T1×3,T2×1,T3×9,T5×1,T6×1 | 7 | 2 | 60.0 | 7.1 | 20·22.5·17·5·10.0 |
| 23 | **B** | 74.3 | `deafblind-built-environment-design` | population-general | 9 | ● | 7 | 0 | 2 | 0 | T1×3,T2×4,T3×1,T6×1 | 5 | 3 | 66.7 | 44.4 | 16·25.6·17·9·6.7 |
| 24 | **B** | 73.2 | `assistive-listening-systems` | communication-and-alerts | 8 | ● | 2 | 2 | 4 | 0 | T2×2,T3×2,T4×1,T5×1,T6×2 | 5 | 5 | 50.0 | 0.0 | 16·17.0·17·12·11.2 |
| 25 | **B** | 72.5 | `luminance-contrast-and-pattern` | wayfinding-and-signage | 13 | ◐ | 0 | 4 | 9 | 0 | T5×4,T6×9 | 13 | 13 | 0.0 | 0.0 | 20·2.5·20·15·15.0 |
| 26 | **B** | 72.3 | `bathroom-typology-global-south` | bathrooms-and-wet-areas | 8 | ● | 4 | 1 | 3 | 0 | T1×1,T2×1,T3×2,T4×1,T6×3 | 4 | 4 | 62.5 | 0.0 | 16·21.0·13·12·10.3 |
| 27 | **B** | 70.8 | `accessibility-feature-market-value-uplift-framing` | economics | 33 | ● | 8 | 19 | 6 | 0 | T3×10,T4×4,T5×15,T6×4 | 11 | 3 | 90.9 | 78.8 | 20·19.5·20·9·2.3 |
| 28 | **B** | 70.6 | `pain-ofs-built-environment-design` | health-and-symptom-management | 12 | ● | 5 | 3 | 4 | 0 | T1×2,T2×3,T3×3,T5×3,T6×1 | 6 | 3 | 83.3 | 60.0 | 20·20.3·17·9·4.3 |
| 29 | **B** | 69.9 | `circadian-lighting-melanopic-edi` | sensory-environment | 12 | ● | 7 | 5 | 0 | 0 | T2×2,T3×5,T4×2,T5×3 | 4 | 2 | 91.7 | 16.7 | 20·25.0·13·5·6.9 |
| 30 | **B** | 69.6 | `neurological-built-environment` | population-general | 8 | ● | 8 | 0 | 0 | 0 | T1×1,T3×7 | 5 | 1 | 100.0 | 12.5 | 16·30·17·0·6.6 |
| 31 | **B** | 68.2 | `jurisdiction-grant-programmes-comprehensive` | frameworks-and-methodology | 9 | ◐ | 0 | 9 | 0 | 0 | T5×9 | 9 | 6 | 44.4 | 33.3 | 16·8.0·20·15·9.2 |
| 32 | **B** | 67.7 | `economics-sources` | economics | 23 | ● | 23 | 0 | 0 | 0 | T1×2,T2×1,T3×20 | 6 | 1 | 100.0 | 90.9 | 20·30·17·0·0.7 |
| 33 | **B** | 67.5 | `school-environment-autism` | sensory-environment | 17 | ● | 17 | 0 | 0 | 0 | T1×2,T2×3,T3×12 | 4 | 1 | 100.0 | 40.0 | 20·30·13·0·4.5 |
| 34 | **B** | 66.4 | `jurisdiction-matrix-accessibility-standards` | frameworks-and-methodology | 14 | ◐ | 0 | 4 | 10 | 0 | T4×4,T6×10 | 12 | 6 | 64.3 | 14.3 | 20·2.3·20·15·9.1 |
| 35 | **B** | 66.2 | `threshold-and-level-access` | entrances-and-circulation | 15 | ◐ | 0 | 5 | 10 | 0 | T4×1,T5×4,T6×10 | 12 | 8 | 46.7 | 40.0 | 20·2.7·20·15·8.5 |
| 36 | **B** | 66.0 | `deaf-acoustic-built-environment` | communication-and-alerts | 10 | ● | 4 | 5 | 1 | 0 | T1×2,T2×2,T3×1,T4×3,T5×2 | 5 | 2 | 90.0 | 30.0 | 16·22.0·17·5·6.0 |
| 37 | **B** | 65.8 | `air-quality-voc-chemical-sensitivity-built-environment` | sensory-environment | 12 | ● | 7 | 5 | 0 | 0 | T2×1,T3×6,T4×4,T5×1 | 7 | 1 | 100.0 | 50.0 | 20·25.0·17·0·3.8 |
| 38 | **B** | 65.6 | `upper-limb-impairment-built-environment` | population-general | 17 | ● | 16 | 0 | 1 | 0 | T1×1,T2×2,T3×14 | 4 | 1 | 100.0 | 50.0 | 20·28.8·13·0·3.8 |
| 39 | **C** | 64.7 | `manoeuvring-footprint-vs-turning-radius-methodology` | frameworks-and-methodology | 30 | ● | 28 | 1 | 1 | 0 | T1×14,T2×4,T3×11,T4×1 | 3 | 1 | 100.0 | 62.5 | 20·28.9·13·0·2.8 |
| 40 | **C** | 62.2 | `thermal-comfort-older-adults-care-settings` | health-and-symptom-management | 6 | ● | 4 | 1 | 1 | 0 | T2×2,T3×3,T5×1 | 4 | 2 | 83.3 | 16.7 | 12·24.7·13·5·7.5 |
| 41 | **C** | 62.0 | `ot-built-environment-interface` | frameworks-and-methodology | 16 | ● | 14 | 0 | 2 | 0 | T2×1,T3×15 | 3 | 1 | 100.0 | 80.0 | 20·27.5·13·0·1.5 |
| 42 | **C** | 61.4 | `ms-thermal-temperature-conflict-resolution` | health-and-symptom-management | 10 | ● | 7 | 3 | 0 | 0 | T1×1,T2×1,T3×5,T4×2,T5×1 | 4 | 1 | 100.0 | 20.0 | 16·26.4·13·0·6.0 |
| 43 | **C** | 61.1 | `acoustics-speech-intelligibility-disability` | sensory-environment | 8 | ● | 5 | 3 | 0 | 0 | T2×3,T3×2,T4×3 | 4 | 1 | 100.0 | 12.5 | 16·25.5·13·0·6.6 |
| 44 | **C** | 60.8 | `fold-down-grab-bar-specification` | bathrooms-and-wet-areas | 8 | ● | 2 | 4 | 2 | 0 | T3×2,T4×2,T5×2,T6×2 | 5 | 2 | 87.5 | 62.5 | 16·19.0·17·5·3.8 |
| 45 | **C** | 60.2 | `reach-range-and-accessible-controls` | controls-and-hardware | 11 | ● | 1 | 5 | 5 | 0 | T3×1,T5×5,T6×5 | 6 | 3 | 81.8 | 81.8 | 16·15.5·17·9·2.7 |
| 46 | **C** | 59.3 | `sensory-relief-space-design` | sensory-environment | 10 | ● | 7 | 1 | 1 | 1 | T2×3,T3×5,T4×1,T6×1 | 6 | 1 | 100.0 | 80.0 | 16·24.8·17·0·1.5 |
| 47 | **C** | 57.4 | `neurodivergent-built-environment` | population-general | 9 | ● | 6 | 1 | 0 | 2 | T1×2,T2×4,T3×2,T4×1 | 4 | 1 | 100.0 | 44.4 | 16·24.2·13·0·4.2 |
| 48 | **C** | 57.0 | `ecological-psychology-haptic-affordances-built-environment` | frameworks-and-methodology | 5 | ● | 5 | 0 | 0 | 0 | T3×5 | 2 | 1 | 100.0 | 20.0 | 12·30·9·0·6.0 |
| 49 | **C** | 56.7 | `biophilic-design-healthcare-workplace` | sensory-environment | 6 | ● | 5 | 0 | 0 | 1 | T1×1,T2×3,T3×2 | 3 | 1 | 100.0 | 33.3 | 12·26.7·13·0·5.0 |
| 50 | **C** | 56.3 | `floor-vibration-wheelchair-disability` | entrances-and-circulation | 7 | ● | 4 | 3 | 0 | 0 | T2×1,T3×3,T4×3 | 3 | 1 | 100.0 | 14.3 | 12·24.9·13·0·6.4 |
| 51 | **C** | 56.3 | `visitability-residential-accessibility-minimum-standards` | frameworks-and-methodology | 7 | ● | 1 | 1 | 5 | 0 | T1×1,T5×1,T6×5 | 5 | 3 | 71.4 | 71.4 | 12·14.0·17·9·4.3 |
| 52 | **C** | 56.0 | `body-sizes-supplementary-populations` | frameworks-and-methodology | 11 | ◐ | 0 | 9 | 2 | 0 | T3×2,T4×4,T5×5 | 5 | 3 | 63.6 | 36.4 | 16·6.5·17·9·7.5 |
| 53 | **C** | 56.0 | `detectable-gradient-protocol-sensory-zones` | wayfinding-and-signage | 6 | ● | 4 | 2 | 0 | 0 | T2×2,T3×2,T4×2 | 4 | 1 | 100.0 | 33.3 | 12·26.0·13·0·5.0 |
| 54 | **C** | 55.9 | `ndv-aut-built-environment-quantified-thresholds` | population-general | 6 | ● | 4 | 1 | 1 | 0 | T2×2,T3×3,T4×1 | 3 | 1 | 100.0 | 16.7 | 12·24.7·13·0·6.2 |
| 55 | **C** | 55.6 | `design-framework-evidence-audit` | frameworks-and-methodology | 9 | ● | 4 | 3 | 2 | 0 | T2×1,T3×5,T4×2,T5×1 | 4 | 1 | 100.0 | 33.3 | 16·21.6·13·0·5.0 |
| 56 | **C** | 55.3 | `wayfinding-cognitive-science-spatial-design` | wayfinding-and-signage | 7 | ● | 7 | 0 | 0 | 0 | T3×7 | 2 | 1 | 100.0 | 42.9 | 12·30·9·0·4.3 |
| 57 | **C** | 55.2 | `visual-alerting-and-wayfinding-light` | wayfinding-and-signage | 7 | ◐ | 0 | 4 | 3 | 0 | T4×2,T5×2,T6×3 | 7 | 5 | 42.9 | 28.6 | 12·4.6·17·12·9.6 |
| 58 | **C** | 55.1 | `residential-accessible-home-case-studies` | frameworks-and-methodology | 8 | ● | 6 | 0 | 1 | 1 | T1×2,T2×1,T3×5 | 4 | 1 | 100.0 | 85.7 | 16·25.0·13·0·1.1 |
| 59 | **C** | 54.8 | `sensory-processing-model-design-application` | sensory-environment | 6 | ● | 4 | 2 | 0 | 0 | T2×1,T3×3,T4×1,T5×1 | 4 | 1 | 100.0 | 50.0 | 12·26.0·13·0·3.8 |
| 60 | **C** | 53.0 | `visual-fire-alarm-seizure-safety` | sensory-environment | 7 | ● | 4 | 2 | 1 | 0 | T2×1,T3×3,T4×2,T6×1 | 3 | 1 | 100.0 | 42.9 | 12·23.7·13·0·4.3 |
| 61 | **C** | 52.9 | `government-grant-programmes` | economics | 4 | ● | 4 | 0 | 0 | 0 | T2×1,T3×3 | 3 | 1 | 100.0 | 75.0 | 8·30·13·0·1.9 |
| 62 | **C** | 52.9 | `ot-frameworks-built-environment` | frameworks-and-methodology | 4 | ● | 4 | 0 | 0 | 0 | T1×4 | 3 | 1 | 100.0 | 75.0 | 8·30·13·0·1.9 |
| 63 | **C** | 52.3 | `intellectual-disability-built-environment-design` | population-general | 5 | ● | 2 | 3 | 0 | 0 | T3×2,T4×3 | 3 | 1 | 100.0 | 40.0 | 12·22.8·13·0·4.5 |
| 64 | **D** | 49.8 | `ofs-built-environment` | health-and-symptom-management | 7 | ● | 4 | 2 | 1 | 0 | T1×3,T3×1,T5×2,T6×1 | 3 | 1 | 100.0 | 85.7 | 12·23.7·13·0·1.1 |
| 65 | **D** | 49.6 | `ot-cpg-built-environment` | population-general | 6 | ● | 4 | 0 | 0 | 2 | T2×6 | 4 | 1 | 100.0 | 83.3 | 12·23.3·13·0·1.3 |
| 66 | **D** | 49.0 | `bariatric-turning-radius-built-environment` | seating-and-rest | 8 | ● | 2 | 5 | 1 | 0 | T3×3,T4×2,T5×3 | 4 | 1 | 100.0 | 100.0 | 16·20.0·13·0·0.0 |
| 67 | **D** | 48.7 | `luminance-contrast-lrv-evidence-base` | wayfinding-and-signage | 7 | ● | 4 | 2 | 1 | 0 | T3×4,T5×2,T6×1 | 4 | 1 | 100.0 | 100.0 | 12·23.7·13·0·0.0 |
| 68 | **D** | 48.0 | `cross-population-conflict-resolutions` | frameworks-and-methodology | 6 | ● | 2 | 4 | 0 | 0 | T3×2,T4×3,T5×1 | 2 | 1 | 100.0 | 33.3 | 12·22.0·9·0·5.0 |
| 69 | **D** | 47.0 | `accessible-laundry-room-design` | room-types | 6 | ◐ | 0 | 6 | 0 | 0 | T4×3,T5×3 | 4 | 3 | 66.7 | 66.7 | 12·8.0·13·9·5.0 |
| 70 | **D** | 47.0 | `cross-population-case-studies` | frameworks-and-methodology | 3 | ● | 3 | 0 | 0 | 0 | T1×1,T3×2 | 2 | 1 | 100.0 | 100.0 | 8·30·9·0·0.0 |
| 71 | **D** | 46.3 | `government-grant-programmes-home-adaptation` | economics | 7 | ◐ | 0 | 7 | 0 | 0 | T5×7 | 6 | 2 | 71.4 | 71.4 | 12·8.0·17·5·4.3 |
| 72 | **D** | 45.8 | `accessible-design-failures-poor-performance` | frameworks-and-methodology | 4 | ● | 3 | 0 | 1 | 0 | T3×4 | 2 | 1 | 100.0 | 50.0 | 8·25.0·9·0·3.8 |
| 73 | **D** | 45.4 | `european-accessibility-act-scope-clarification` | frameworks-and-methodology | 6 | ◐ | 0 | 2 | 4 | 0 | T5×2,T6×4 | 4 | 3 | 66.7 | 16.7 | 12·2.7·13·9·8.7 |
| 74 | **D** | 44.1 | `thermoregulation-built-environment` | health-and-symptom-management | 5 | ● | 2 | 1 | 2 | 0 | T3×4,T4×1 | 1 | 1 | 100.0 | 0.0 | 12·19.6·5·0·7.5 |
| 75 | **D** | 44.0 | `case-study-economics-financial-data` | economics | 4 | ● | 3 | 1 | 0 | 0 | T1×1,T2×1,T3×1,T5×1 | 2 | 1 | 100.0 | 100.0 | 8·27.0·9·0·0.0 |
| 76 | **D** | 43.4 | `therapeutic-lighting-design` | sensory-environment | 4 | ◐ | 0 | 4 | 0 | 0 | T4×1,T5×3 | 3 | 2 | 75.0 | 0.0 | 8·8.0·13·5·9.4 |
| 77 | **E** | 33.0 | `residential-dar-provisions-priority-register` | frameworks-and-methodology | 6 | ◐ | 0 | 5 | 1 | 0 | T4×1,T5×4,T6×1 | 3 | 1 | 100.0 | 83.3 | 12·6.7·13·0·1.3 |
| 78 | **E** | 32.5 | `crpd-implementation-built-environment` | frameworks-and-methodology | 5 | ◐ | 0 | 5 | 0 | 0 | T4×5 | 1 | 1 | 100.0 | 0.0 | 12·8.0·5·0·7.5 |
| 79 | **E** | 28.5 | `co1-housing-research-global-south` | frameworks-and-methodology | 3 | ◐ | 0 | 3 | 0 | 0 | T4×3 | 1 | 1 | 100.0 | 0.0 | 8·8.0·5·0·7.5 |

**Anchoring bands across the 79 evidenced slices:** **66 ● full** (adjudicated anchor) · **13 ◐ partial** (standards-practice basis) · **0 ○ weak-only**.
- **† ○ weak-only (0)** — no evidenced slice rests on a weak-only base; every slice anchors at ● full or ◐ partial strength.
- **◐ partial (13)** — strongest anchor is T4/T5 standards: renders as *current standards practice* (“standards basis, not primary evidence”), not a code-floor. `luminance-contrast-and-pattern`, `jurisdiction-grant-programmes-comprehensive`, `jurisdiction-matrix-accessibility-standards`, `threshold-and-level-access`, `body-sizes-supplementary-populations`, `visual-alerting-and-wayfinding-light`, `accessible-laundry-room-design`, `government-grant-programmes-home-adaptation`, `european-accessibility-act-scope-clarification`, `therapeutic-lighting-design`, `residential-dar-provisions-priority-register`, `crpd-implementation-built-environment`, `co1-housing-research-global-south`.

## 5. Evidence-empty slices (0)

These carry **zero** linked source-instances. `bpc_metadata.evidence_state` distinguishes:

**Retracted pending rehabilitation (0)** — prior work cleared, awaiting re-derivation:

**Un-started / placeholder (0)** — `evidence_state` unset, search not run:

Several name high-salience topics where an empty base is a material coverage gap, not bookkeeping.

## 6. Findings & recommended remediation

1. **Strengthen the ◐ partial and ○ weak bases toward ● full.** 13 slices anchor only at ◐ partial (T4/T5 standards practice) and none rest on a ○ weak-only base. With only 113 systematic-review/evidence-based-standard instances corpus-wide, the ● full synthesis tier is the thinnest. Prioritise SR/meta-analysis + DPO-standard recovery on the partial/weak slices to lift them to full-strength anchoring, and replace the 10 DISPUTED sources (§4) with verifiable citations.
2. **Convert non-English search into non-English evidence.** Searches ran in 19 languages but the corpus is ~76% English. Target the languages already searched-with-results but under-linked, and the zero-yield languages (`ar`, `bn`, `hi`, `sw`) explicitly.
3. **De-risk monojurisdictional slices.** 3 evidenced slices rest on ≤1 jurisdiction; flag their numeric thresholds as non-transferable until a second regime is sourced.
4. **Fill or formally park the empty slices.** Move the 0 un-started slices into an active search queue or an explicit deferred state so they stop reading as silent gaps.
5. **Treat the doubly-concentrated slices as citation-risk.** The 19 ≥90%-English-and-≥50%-Anglophone slices are where global-applicability claims are weakest.
6. **Fix the mis-filed jurisdiction codes.** Move the 0  values out of `evidence_sources.jurisdiction` and recover the true jurisdiction — a one-off migration.

## 7. Limitations & what this audit does *not* claim

- **Instance-weighted, not source-weighted.** The 948 instances are 781 unique sources, so corpus tier/language totals run ~21% above unique-source counts. Per-slice figures are unaffected.
- **The composite is a lens, not ground truth.** Weights (20/30/20/15/15) are a defensible but editorial choice; the six raw dimensions are printed alongside every grade so a reader can re-weight. No grade is stored in the DB — it is recomputed each run.
- **Coverage ≠ correctness.** The audit measures the *shape* of each base (how much, what tier, where from, what language, how concentrated). It does **not** re-verify that any citation resolves, is current, or supports its claim — those are the `url_verification_runs` / `code_currency` / supersession checks, run separately.
- **Jurisdiction shares rest on recorded jurisdictions only.** NULL-jurisdiction instances are excluded from %ANG denominators, so a low %ANG can mean *genuinely non-Anglophone* or *unrecorded* — the master table’s JUR count exposes the denominator.
- **Compound jurisdictions classify by their strongest Anglophone member** (e.g. `US/AU/INT` counts as native-Anglophone). Magnitude ≈1% of instances.

## 8. Per-specification (item) adjudication — inheritance view

The Guidebook’s **93 design specifications** (the `items` table, categories A–K) do **not** carry their own evidence links — each *inherits* the evidentiary base of the research slug it draws on (`items.bpc_source_slug`). This section adjudicates every specification by that inherited base, so a spec built on a thin or unanchored slug is visible as such. (A spec with no source slug cannot inherit and is a coverage gap.)

| Basis health | Specs | Meaning |
|---|---|---|
| full | 79 | inherits a ● full (adjudicated) anchor base |
| partial | 8 | inherits a ◐ partial (standards-practice) anchor base |
| no-source | 6 | no source slug — cannot inherit |

**87 of 93 specs inherit a ● full or ◐ partial anchored base; 6 rest on a ○ weak, disputed-only, or missing base** and are the priority remediation set.

### By category
| Cat | Specifications | Specs | On weak/missing base |
|---|---|---|---|
| A | Acoustics | 19 | 2 |
| B | Lighting | 12 | 1 |
| C | Colour and Contrast | 6 | 0 |
| D | Wayfinding and Cognition | 11 | 0 |
| E | Circulation and Access | 14 | 0 |
| F | Sensory Environment | 8 | 1 |
| G | Furniture, Fixtures and Spatial Layout | 9 | 2 |
| H | Controls and Technology | 5 | 0 |
| I | Hardware and Fixtures | 4 | 0 |
| K | DeafBlind Provisions | 5 | 0 |

### Specifications resting on a weak or missing base

| Item | Category | Specification | Source slug | Basis | Inh. grade |
|---|---|---|---|---|---|
| `A-13` | A | No Sound Masking in Neurological Population Environm | — | no-source | — |
| `A-15` | A | Acoustic Differentiation Between Spaces (Navigation  | — | no-source | — |
| `B-08` | B | Matte, Low-Reflectance Floor Finishes (≤30 Gloss Uni | — | no-source | — |
| `F-07` | F | Thermal Zoning — Building-Wide Temperature Managemen | — | no-source | — |
| `G-02` | G | Variety of Seating Types (Three Heights at Every Sea | — | no-source | — |
| `G-07` | G | Waiting Area Seating (Accessible Configuration — Adj | — | no-source | — |

The full per-specification table (all 93 items with inherited grade and dimension snapshot) is in `evidentiary-base-audit-items.csv` and the `items` array of the JSON; the dashboard’s **Specifications** view filters them by corpus / category / term.

---
*Data as of 2026-07-20 · read-only over `data/guidebook.db` · generated by `tools/evidentiary_audit.py`. Independently red-teamed; raw counts reproduce through a second code path. Aligned to `governance/tier-system.md`.*
