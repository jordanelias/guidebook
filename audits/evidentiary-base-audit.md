# Per-Slice Evidentiary Audit
**Data as of:** 2026-07-21 · **Scope:** all 79 ACTIVE research slices (slugs) in `data/guidebook.db` · **Method:** read-only aggregation over `source_slug_links → evidence_sources`, `search_languages`, `search_coverage`, `bpc_metadata`.

This audit scores every research slice on the six requested dimensions — (1) amount of evidence, (2) tiers of evidence, (3) jurisdictions sourced, (4) languages sourced, (5) English/Anglophone bias, and (6) overall quality of the evidentiary base — and rolls them into a transparent 0–100 composite grade. It audits the **raw evidence linked to each slice**, i.e. the material available for (re-)derivation; it does not re-judge synthesis prose.

> **Reproducibility.** Every number here is regenerated from the DB by `tools/evidentiary_audit.py` — nothing is hand-transcribed, and the “data as of” date is the DB’s own `max(updated_at)`, so identical data yields byte-identical output. No grade is stored in the DB; the composite is a *derived* view whose rubric is fully specified in §2, so any reader can recompute it. Companion outputs: `evidentiary-base-audit.json` / `.csv`, and the interactive `tools/evidentiary-audit-dashboard.html` (filter by corpus / category / term).

> **Adversarial review (two passes).** The audit was independently red-teamed twice; all raw counts (volume, tiers, language/jurisdiction distributions, search yield) reproduce exactly through a second code path. Folded in: (i) the **weighted-strength bands** (§8, DR-2026-07-20) — every slice is graded by the strongest band it can anchor at: ● full (T1/Co-1/T2/Co-2/T3-clinical), ◐ partial (T4/T5 standards), ○ weak (T3-grey/T6/grey); a ○ weak-only slice carries the honesty flag in place of the retired binary no-anchor flag (§2, §4); (ii) **DISPUTED sources** (10 instances) stripped of anchoring per the anti-fabrication sweep (§4) — retained in raw totals but counted at no band; (iii) a **convergence discount** (scoped to the ○ weak band) so code-floor-only slices can’t score highly on breadth alone (§2, §6); (iv) full disclosure of the **82 NULL-jurisdiction instances** (§3.5); (v) **true-jurisdiction** breadth scoring of the jurisdiction column (no language codes are currently mis-filed there).

## 1. Executive summary

- **947 source-instances** are linked across **79 of 79 slices**; **0 slices carry zero linked evidence**.
- **Grade distribution:** A=11 · B=29 · C=25 · D=11 · E=3 · F=0  (A≥80, B≥65, C≥50, D≥35, E>0, F=empty).
- **Tier profile is code-and-clinical heavy, synthesis-light.** Of linked instances: T1=95, T2=104, T3=355, T4=81, T5=168, T6=144. Only **104 Tier-2 (systematic-review / evidence-based-standard) instances** exist across the whole corpus — the synthesis tier that best anchors best-practice claims is the thinnest.
- **Anchoring strength, banded.** Under the weighted-strength model (§8) every tier can anchor a best-practice claim, weighted by tier: **483/947 (51%)** of instances anchor at ● full strength (T1/Co-1/T2/Co-2/T3-clinical, adjudicated), 249 at ◐ partial (T4/T5 standards practice), 205 at ○ weak (T3-grey/T6/grey floor). **10 DISPUTED instances anchor at no band** (§4). By slice: **68 full · 11 partial · 0 weak-only** (of 79 evidenced). Every evidenced slice anchors at ● full or ◐ partial strength — none rests on a weak-only base.
- **Anglophone concentration is the dominant quality risk.** **715/947 (76%) of linked sources are English-language**; only 232 are non-English. By jurisdiction, 352 instances are native-Anglophone (US/UK/AU/CA/NZ/IE), 205 supranational (INT/EU/ISO), 308 other, 82 unrecorded.
- **Search breadth ≠ evidentiary yield.** Slices were searched across **19 languages** and ~48 jurisdictions, but 4 searched languages (`ar`, `bn`, `hi`, `sw`) returned **zero** usable sources in **every** slice. The bias lives in what converted to evidence, not in search effort.

## 2. Method & definitions

**Slice = slug.** The 79 ACTIVE slugs are the unit of audit. Evidence is attributed through `source_slug_links`; each linked `evidence_sources` row is one *source-instance* (a source shared by two slices counts once in each). The 947 instances collapse to **739 unique sources** (reuse factor 1.28×; 135 sources span >1 slice, one — `REF-00323` — spans 7). Instance-weighting is deliberate — it measures per-slice coverage — but shared sources are re-counted, so corpus tier/language totals read ~28% above unique-source counts. (65 of the 804 rows in `evidence_sources` are linked to no active slug.)

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
| 4–7 | 26 |
| 8–14 | 32 |
| 15+ | 19 |

Median linked sources among non-empty slices: **9**. Largest bases: `mental-health-built-environment` (37), `wayfinding-dementia-spatial-design` (35), `accessibility-feature-market-value-uplift-framing` (33), `room-acoustic-performance` (32), `threshold-door-hardware` (32).

### (2) Tiers of evidence
| Tier | Instances | Share |
|---|---|---|
| T1 | 95 | ██·················· 10% |
| T2 | 104 | ██·················· 11% |
| T3 | 355 | ███████············· 37% |
| T4 | 81 | ██·················· 9% |
| T5 | 168 | ████················ 18% |
| T6 | 144 | ███················· 15% |

**Strength-band split of instances:** **483/947 (51%)** anchor at ● full (T1/Co-1/T2/Co-2/T3-clinical), 249 (26%) at ◐ partial (T4/T5 standards), and 205 (22%) at ○ weak (T3-grey/T6/grey floor); a further 10 DISPUTED instances anchor at no band (§4). No evidenced slice rests on a ○ weak-only base — every slice anchors at ● full or ◐ partial strength (see the band breakdown in §4).

### (3) Jurisdictions sourced
Distinct jurisdiction strings across the corpus: **50**, none mis-filed as language codes in the `jurisdiction` column. Top: INT (192), US (149), UK (98), DE (50), AU (46), CA (34), JP (30), NL (27), NO (27), SE (20).

**3 non-empty slices draw on ≤1 jurisdiction** — monojurisdictional bases whose values may not transfer across code regimes. Separately, **82 source-instances carry no jurisdiction at all** (NULL) — mostly clinical/synthesis sources with no single national home; these are excluded from every jurisdiction-share denominator.

### (4) Languages sourced
| Language | Instances |
|---|---|
| en | 715 |
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
- **Jurisdiction axis (all 947 instances):** native-Anglophone (US/UK/AU/CA/NZ/IE) **352** · supranational/English-medium (INT/EU/ISO) **205** · English-official + other non-Anglophone **308** · **no jurisdiction recorded 82**. (These four sum to 947 = all instances.)
- **20 slices are doubly-concentrated** (≥90% English *and* ≥50% native-Anglophone jurisdiction): `accessibility-feature-market-value-uplift-framing`, `economics-sources`, `air-quality-voc-chemical-sensitivity-built-environment`, `upper-limb-impairment-built-environment`, `manoeuvring-footprint-vs-turning-radius-methodology`, `ot-built-environment-interface`, `sensory-relief-space-design`, `neurodivergent-built-environment`, `sensory-processing-model-design-application`, `residential-accessible-home-case-studies`, `government-grant-programmes`, `ot-frameworks-built-environment`, `luminance-contrast-lrv-evidence-base`, `ofs-built-environment`, `bariatric-turning-radius-built-environment`, `ot-cpg-built-environment`, `cross-population-case-studies`, `accessible-design-failures-poor-performance`, `case-study-economics-financial-data`, `residential-dar-provisions-priority-register`.
- **Process counter-evidence:** non-English/Global-South *searches were run* (19 languages across 81 of 79 slices in `search_languages`) but `ar`, `bn`, `hi`, `sw` yielded nothing linkable in any slice. The gap is a *yield/recovery* gap, not a *search-effort* gap.

### (6) Overall quality of the evidentiary base
| Grade | Slices | Meaning |
|---|---|---|
| A | 11 | strong, balanced, synthesis-anchored |
| B | 29 | solid, some concentration or tier gaps |
| C | 25 | usable but thin or monolingual |
| D | 11 | weak — few sources / single jurisdiction / English-only |
| E | 3 | very weak — 1 jurisdiction, weak-only or thin base |
| F | 0 | empty — no linked evidence |

## 4. Master per-slice table (ranked by composite score)

Legend: **N** linked sources · **Band** strongest anchoring band (● full / ◐ partial / ○ weak / ⊘ disputed-only) · **●/◐/○** full / partial / weak instance counts · **⊘** DISPUTED instances (anchoring stripped, §4) · **JUR** distinct *true* jurisdictions · **LNG** distinct languages · **%EN** English-language share · **%ANG** native-Anglophone share · **A/B/C/D/E** score components · **†** ○ weak-only slice (breadth discounted, honesty-flagged).

| # | Grade | Score | Slice | Topic | N | Band | ● | ◐ | ○ | ⊘ | Tiers | JUR | LNG | %EN | %ANG | A·B·C·D·E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **A** | 89.6 | `cognitive-wayfinding-design` | wayfinding-and-signage | 25 | ● | 16 | 7 | 2 | 0 | T2×5,T3×12,T5×7,T6×1 | 13 | 9 | 64.0 | 8.3 | 20·25.0·20·15·9.6 |
| 2 | **A** | 88.2 | `wayfinding-dementia-spatial-design` | wayfinding-and-signage | 35 | ● | 25 | 5 | 5 | 0 | T1×6,T2×9,T3×11,T5×5,T6×4 | 19 | 13 | 60.0 | 36.4 | 20·25.4·20·15·7.8 |
| 3 | **A** | 87.4 | `sensory-room-user-control` | sensory-environment | 14 | ● | 13 | 0 | 1 | 0 | T2×6,T3×7,T6×1 | 9 | 4 | 71.4 | 38.5 | 20·28.6·20·12·6.8 |
| 4 | **A** | 85.7 | `stair-ramp-threshold-biomechanics-accessibility` | entrances-and-circulation | 27 | ● | 14 | 3 | 10 | 0 | T2×1,T3×14,T4×1,T5×2,T6×9 | 15 | 12 | 59.3 | 14.8 | 20·21.3·20·15·9.4 |
| 5 | **A** | 85.5 | `mental-health-built-environment` | population-general | 37 | ● | 27 | 3 | 6 | 1 | T1×3,T2×3,T3×28,T4×1,T5×2 | 11 | 5 | 59.5 | 29.7 | 20·25.2·20·12·8.3 |
| 6 | **A** | 85.2 | `residential-kitchen-and-task-surfaces` | kitchens-and-workspaces | 30 | ● | 20 | 5 | 5 | 0 | T1×2,T2×12,T3×6,T4×1,T5×4,T6×5 | 10 | 7 | 80.0 | 46.2 | 20·24.7·20·15·5.5 |
| 7 | **A** | 84.8 | `room-acoustic-performance` | sensory-environment | 32 | ● | 19 | 10 | 3 | 0 | T1×14,T2×1,T3×6,T4×2,T5×8,T6×1 | 13 | 8 | 78.1 | 50.0 | 20·24.4·20·15·5.4 |
| 8 | **A** | 84.4 | `mobility-built-environment` | population-general | 24 | ● | 13 | 5 | 6 | 0 | T1×7,T2×2,T3×5,T5×5,T6×5 | 17 | 9 | 58.3 | 50.0 | 20·22.5·20·15·6.9 |
| 9 | **A** | 84.2 | `deaf-classroom-reverberation-time` | communication-and-alerts | 12 | ● | 2 | 7 | 3 | 0 | T1×2,T4×1,T5×6,T6×3 | 9 | 9 | 25.0 | 25.0 | 20·18.0·20·15·11.2 |
| 10 | **A** | 82.4 | `deaf-spatial-design` | communication-and-alerts | 13 | ● | 8 | 1 | 4 | 0 | T1×5,T2×1,T3×5,T5×1,T6×1 | 8 | 5 | 61.5 | 38.5 | 20·22.9·20·12·7.5 |
| 11 | **A** | 81.2 | `accessible-bathroom-and-grab-bar` | bathrooms-and-wet-areas | 22 | ● | 11 | 5 | 5 | 1 | T1×6,T2×4,T3×3,T5×5,T6×4 | 12 | 7 | 72.7 | 68.4 | 20·21.8·20·15·4.4 |
| 12 | **B** | 79.5 | `wayfinding-global-south` | wayfinding-and-signage | 15 | ● | 1 | 4 | 10 | 0 | T3×1,T4×4,T6×10 | 13 | 7 | 53.3 | 0.0 | 20·13.5·20·15·11.0 |
| 13 | **B** | 78.5 | `accessible-circulation-geometry` | entrances-and-circulation | 14 | ● | 3 | 5 | 6 | 0 | T2×1,T3×2,T4×1,T5×4,T6×6 | 9 | 6 | 64.3 | 50.0 | 20·17.1·20·15·6.4 |
| 14 | **B** | 78.1 | `threshold-door-hardware` | entrances-and-circulation | 32 | ● | 2 | 11 | 19 | 0 | T3×2,T4×1,T5×10,T6×19 | 26 | 13 | 46.9 | 31.2 | 20·14.0·20·15·9.1 |
| 15 | **B** | 77.6 | `residential-entry-and-threshold` | entrances-and-circulation | 20 | ● | 3 | 8 | 8 | 1 | T2×3,T3×1,T4×1,T5×7,T6×8 | 13 | 7 | 65.0 | 50.0 | 20·16.2·20·15·6.4 |
| 16 | **B** | 77.4 | `dementia-built-environment` | population-general | 8 | ● | 4 | 3 | 1 | 0 | T3×5,T5×3 | 5 | 4 | 62.5 | 12.5 | 16·23.0·17·12·9.4 |
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
| 28 | **B** | 69.9 | `circadian-lighting-melanopic-edi` | sensory-environment | 12 | ● | 7 | 5 | 0 | 0 | T2×2,T3×5,T4×2,T5×3 | 4 | 2 | 91.7 | 16.7 | 20·25.0·13·5·6.9 |
| 29 | **B** | 69.6 | `neurological-built-environment` | population-general | 8 | ● | 8 | 0 | 0 | 0 | T1×1,T3×7 | 5 | 1 | 100.0 | 12.5 | 16·30·17·0·6.6 |
| 30 | **B** | 68.2 | `jurisdiction-grant-programmes-comprehensive` | frameworks-and-methodology | 9 | ◐ | 0 | 9 | 0 | 0 | T5×9 | 9 | 6 | 44.4 | 33.3 | 16·8.0·20·15·9.2 |
| 31 | **B** | 67.7 | `economics-sources` | economics | 23 | ● | 23 | 0 | 0 | 0 | T1×3,T2×1,T3×19 | 6 | 1 | 100.0 | 90.9 | 20·30·17·0·0.7 |
| 32 | **B** | 67.5 | `school-environment-autism` | sensory-environment | 17 | ● | 17 | 0 | 0 | 0 | T1×2,T2×3,T3×12 | 4 | 1 | 100.0 | 40.0 | 20·30·13·0·4.5 |
| 33 | **B** | 66.7 | `threshold-and-level-access` | entrances-and-circulation | 15 | ◐ | 0 | 6 | 9 | 0 | T4×1,T5×5,T6×9 | 12 | 8 | 46.7 | 40.0 | 20·3.2·20·15·8.5 |
| 34 | **B** | 66.4 | `body-sizes-supplementary-populations` | frameworks-and-methodology | 11 | ● | 1 | 8 | 2 | 0 | T1×1,T3×2,T4×3,T5×5 | 5 | 3 | 63.6 | 45.5 | 16·17.6·17·9·6.8 |
| 35 | **B** | 66.4 | `jurisdiction-matrix-accessibility-standards` | frameworks-and-methodology | 14 | ◐ | 0 | 4 | 10 | 0 | T4×4,T6×10 | 12 | 6 | 64.3 | 14.3 | 20·2.3·20·15·9.1 |
| 36 | **B** | 66.4 | `therapeutic-lighting-design` | sensory-environment | 8 | ● | 4 | 4 | 0 | 0 | T2×2,T3×2,T4×1,T5×3 | 4 | 2 | 87.5 | 0.0 | 16·24.0·13·5·8.4 |
| 37 | **B** | 66.2 | `pain-ofs-built-environment-design` | health-and-symptom-management | 11 | ● | 4 | 3 | 4 | 0 | T1×1,T2×3,T3×3,T5×3,T6×1 | 6 | 3 | 81.8 | 55.6 | 16·19.5·17·9·4.7 |
| 38 | **B** | 66.0 | `deaf-acoustic-built-environment` | communication-and-alerts | 10 | ● | 4 | 5 | 1 | 0 | T1×2,T2×2,T3×1,T4×3,T5×2 | 5 | 2 | 90.0 | 30.0 | 16·22.0·17·5·6.0 |
| 39 | **B** | 65.8 | `air-quality-voc-chemical-sensitivity-built-environment` | sensory-environment | 12 | ● | 7 | 5 | 0 | 0 | T2×1,T3×6,T4×4,T5×1 | 7 | 1 | 100.0 | 50.0 | 20·25.0·17·0·3.8 |
| 40 | **B** | 65.5 | `upper-limb-impairment-built-environment` | population-general | 16 | ● | 15 | 0 | 1 | 0 | T1×1,T2×2,T3×13 | 4 | 1 | 100.0 | 50.0 | 20·28.8·13·0·3.8 |
| 41 | **C** | 64.4 | `manoeuvring-footprint-vs-turning-radius-methodology` | frameworks-and-methodology | 29 | ● | 28 | 0 | 1 | 0 | T1×14,T2×4,T3×11 | 3 | 1 | 100.0 | 71.4 | 20·29.3·13·0·2.1 |
| 42 | **C** | 62.2 | `ot-built-environment-interface` | frameworks-and-methodology | 15 | ● | 13 | 0 | 2 | 0 | T2×1,T3×14 | 3 | 1 | 100.0 | 75.0 | 20·27.3·13·0·1.9 |
| 43 | **C** | 62.2 | `thermal-comfort-older-adults-care-settings` | health-and-symptom-management | 6 | ● | 4 | 1 | 1 | 0 | T2×1,T3×4,T5×1 | 4 | 2 | 83.3 | 16.7 | 12·24.7·13·5·7.5 |
| 44 | **C** | 61.4 | `ms-thermal-temperature-conflict-resolution` | health-and-symptom-management | 10 | ● | 7 | 3 | 0 | 0 | T1×1,T2×1,T3×5,T4×2,T5×1 | 4 | 1 | 100.0 | 20.0 | 16·26.4·13·0·6.0 |
| 45 | **C** | 61.1 | `acoustics-speech-intelligibility-disability` | sensory-environment | 8 | ● | 5 | 3 | 0 | 0 | T2×3,T3×2,T4×3 | 4 | 1 | 100.0 | 12.5 | 16·25.5·13·0·6.6 |
| 46 | **C** | 60.9 | `reach-range-and-accessible-controls` | controls-and-hardware | 11 | ● | 1 | 6 | 4 | 0 | T3×1,T5×6,T6×4 | 6 | 3 | 81.8 | 81.8 | 16·16.2·17·9·2.7 |
| 47 | **C** | 60.8 | `fold-down-grab-bar-specification` | bathrooms-and-wet-areas | 8 | ● | 2 | 4 | 2 | 0 | T3×2,T4×2,T5×2,T6×2 | 5 | 2 | 87.5 | 62.5 | 16·19.0·17·5·3.8 |
| 48 | **C** | 59.3 | `sensory-relief-space-design` | sensory-environment | 10 | ● | 7 | 1 | 1 | 1 | T2×2,T3×6,T4×1,T6×1 | 6 | 1 | 100.0 | 80.0 | 16·24.8·17·0·1.5 |
| 49 | **C** | 57.4 | `visitability-residential-accessibility-minimum-standards` | frameworks-and-methodology | 7 | ● | 1 | 2 | 4 | 0 | T1×1,T5×2,T6×4 | 5 | 3 | 71.4 | 71.4 | 12·15.1·17·9·4.3 |
| 50 | **C** | 57.0 | `ecological-psychology-haptic-affordances-built-environment` | frameworks-and-methodology | 5 | ● | 5 | 0 | 0 | 0 | T3×5 | 2 | 1 | 100.0 | 20.0 | 12·30·9·0·6.0 |
| 51 | **C** | 57.0 | `neurodivergent-built-environment` | population-general | 9 | ● | 6 | 1 | 0 | 2 | T1×2,T2×2,T3×4,T4×1 | 4 | 1 | 100.0 | 50.0 | 16·24.2·13·0·3.8 |
| 52 | **C** | 56.7 | `biophilic-design-healthcare-workplace` | sensory-environment | 6 | ● | 5 | 0 | 0 | 1 | T1×1,T2×3,T3×2 | 3 | 1 | 100.0 | 33.3 | 12·26.7·13·0·5.0 |
| 53 | **C** | 56.3 | `floor-vibration-wheelchair-disability` | entrances-and-circulation | 7 | ● | 4 | 3 | 0 | 0 | T2×1,T3×3,T4×3 | 3 | 1 | 100.0 | 14.3 | 12·24.9·13·0·6.4 |
| 54 | **C** | 55.7 | `ndv-aut-built-environment-quantified-thresholds` | population-general | 6 | ● | 4 | 1 | 1 | 0 | T2×1,T3×4,T4×1 | 3 | 1 | 100.0 | 20.0 | 12·24.7·13·0·6.0 |
| 55 | **C** | 55.5 | `detectable-gradient-protocol-sensory-zones` | wayfinding-and-signage | 6 | ● | 4 | 2 | 0 | 0 | T2×1,T3×3,T4×2 | 3 | 1 | 100.0 | 40.0 | 12·26.0·13·0·4.5 |
| 56 | **C** | 55.3 | `design-framework-evidence-audit` | frameworks-and-methodology | 9 | ● | 4 | 3 | 2 | 0 | T3×6,T4×2,T5×1 | 4 | 1 | 100.0 | 37.5 | 16·21.6·13·0·4.7 |
| 57 | **C** | 55.3 | `wayfinding-cognitive-science-spatial-design` | wayfinding-and-signage | 7 | ● | 7 | 0 | 0 | 0 | T3×7 | 2 | 1 | 100.0 | 42.9 | 12·30·9·0·4.3 |
| 58 | **C** | 55.2 | `visual-alerting-and-wayfinding-light` | wayfinding-and-signage | 7 | ◐ | 0 | 4 | 3 | 0 | T4×2,T5×2,T6×3 | 7 | 5 | 42.9 | 28.6 | 12·4.6·17·12·9.6 |
| 59 | **C** | 54.0 | `sensory-processing-model-design-application` | sensory-environment | 6 | ● | 4 | 2 | 0 | 0 | T3×4,T4×1,T5×1 | 4 | 1 | 100.0 | 60.0 | 12·26.0·13·0·3.0 |
| 60 | **C** | 53.6 | `residential-accessible-home-case-studies` | frameworks-and-methodology | 8 | ● | 5 | 1 | 1 | 1 | T1×3,T3×4,T5×1 | 4 | 1 | 100.0 | 85.7 | 16·23.5·13·0·1.1 |
| 61 | **C** | 53.0 | `visual-fire-alarm-seizure-safety` | sensory-environment | 7 | ● | 4 | 2 | 1 | 0 | T2×1,T3×3,T4×2,T6×1 | 3 | 1 | 100.0 | 42.9 | 12·23.7·13·0·4.3 |
| 62 | **C** | 52.9 | `government-grant-programmes` | economics | 4 | ● | 4 | 0 | 0 | 0 | T1×1,T2×1,T3×2 | 3 | 1 | 100.0 | 75.0 | 8·30·13·0·1.9 |
| 63 | **C** | 52.9 | `ot-frameworks-built-environment` | frameworks-and-methodology | 4 | ● | 4 | 0 | 0 | 0 | T1×4 | 3 | 1 | 100.0 | 75.0 | 8·30·13·0·1.9 |
| 64 | **C** | 52.3 | `intellectual-disability-built-environment-design` | population-general | 5 | ● | 2 | 3 | 0 | 0 | T3×2,T4×3 | 3 | 1 | 100.0 | 40.0 | 12·22.8·13·0·4.5 |
| 65 | **C** | 51.0 | `luminance-contrast-lrv-evidence-base` | wayfinding-and-signage | 7 | ● | 3 | 2 | 2 | 0 | T3×4,T5×2,T6×1 | 5 | 1 | 100.0 | 85.7 | 12·20.9·17·0·1.1 |
| 66 | **D** | 49.8 | `ofs-built-environment` | health-and-symptom-management | 7 | ● | 4 | 2 | 1 | 0 | T1×3,T3×1,T5×2,T6×1 | 3 | 1 | 100.0 | 85.7 | 12·23.7·13·0·1.1 |
| 67 | **D** | 49.0 | `bariatric-turning-radius-built-environment` | seating-and-rest | 8 | ● | 2 | 5 | 1 | 0 | T3×3,T4×2,T5×3 | 4 | 1 | 100.0 | 100.0 | 16·20.0·13·0·0.0 |
| 68 | **D** | 48.0 | `cross-population-conflict-resolutions` | frameworks-and-methodology | 6 | ● | 2 | 4 | 0 | 0 | T3×2,T4×3,T5×1 | 2 | 1 | 100.0 | 33.3 | 12·22.0·9·0·5.0 |
| 69 | **D** | 47.6 | `ot-cpg-built-environment` | population-general | 6 | ● | 3 | 1 | 0 | 2 | T2×5,T5×1 | 4 | 1 | 100.0 | 83.3 | 12·21.3·13·0·1.3 |
| 70 | **D** | 47.0 | `accessible-laundry-room-design` | room-types | 6 | ◐ | 0 | 6 | 0 | 0 | T4×2,T5×4 | 4 | 3 | 66.7 | 66.7 | 12·8.0·13·9·5.0 |
| 71 | **D** | 47.0 | `cross-population-case-studies` | frameworks-and-methodology | 3 | ● | 3 | 0 | 0 | 0 | T1×1,T3×2 | 2 | 1 | 100.0 | 100.0 | 8·30·9·0·0.0 |
| 72 | **D** | 46.3 | `government-grant-programmes-home-adaptation` | economics | 7 | ◐ | 0 | 7 | 0 | 0 | T5×7 | 6 | 2 | 71.4 | 71.4 | 12·8.0·17·5·4.3 |
| 73 | **D** | 45.8 | `accessible-design-failures-poor-performance` | frameworks-and-methodology | 4 | ● | 3 | 0 | 1 | 0 | T3×4 | 2 | 1 | 100.0 | 50.0 | 8·25.0·9·0·3.8 |
| 74 | **D** | 45.4 | `european-accessibility-act-scope-clarification` | frameworks-and-methodology | 6 | ◐ | 0 | 2 | 4 | 0 | T5×2,T6×4 | 4 | 3 | 66.7 | 16.7 | 12·2.7·13·9·8.7 |
| 75 | **D** | 44.1 | `thermoregulation-built-environment` | health-and-symptom-management | 5 | ● | 2 | 1 | 2 | 0 | T3×4,T4×1 | 1 | 1 | 100.0 | 0.0 | 12·19.6·5·0·7.5 |
| 76 | **D** | 44.0 | `case-study-economics-financial-data` | economics | 4 | ● | 3 | 1 | 0 | 0 | T1×1,T2×1,T3×1,T5×1 | 2 | 1 | 100.0 | 100.0 | 8·27.0·9·0·0.0 |
| 77 | **E** | 33.0 | `residential-dar-provisions-priority-register` | frameworks-and-methodology | 6 | ◐ | 0 | 5 | 1 | 0 | T4×1,T5×4,T6×1 | 3 | 1 | 100.0 | 83.3 | 12·6.7·13·0·1.3 |
| 78 | **E** | 32.5 | `crpd-implementation-built-environment` | frameworks-and-methodology | 5 | ◐ | 0 | 5 | 0 | 0 | T4×5 | 1 | 1 | 100.0 | 0.0 | 12·8.0·5·0·7.5 |
| 79 | **E** | 28.5 | `co1-housing-research-global-south` | frameworks-and-methodology | 3 | ◐ | 0 | 3 | 0 | 0 | T4×3 | 1 | 1 | 100.0 | 0.0 | 8·8.0·5·0·7.5 |

**Anchoring bands across the 79 evidenced slices:** **68 ● full** (adjudicated anchor) · **11 ◐ partial** (standards-practice basis) · **0 ○ weak-only**.
- **† ○ weak-only (0)** — no evidenced slice rests on a weak-only base; every slice anchors at ● full or ◐ partial strength.
- **◐ partial (11)** — strongest anchor is T4/T5 standards: renders as *current standards practice* (“standards basis, not primary evidence”), not a code-floor. `luminance-contrast-and-pattern`, `jurisdiction-grant-programmes-comprehensive`, `threshold-and-level-access`, `jurisdiction-matrix-accessibility-standards`, `visual-alerting-and-wayfinding-light`, `accessible-laundry-room-design`, `government-grant-programmes-home-adaptation`, `european-accessibility-act-scope-clarification`, `residential-dar-provisions-priority-register`, `crpd-implementation-built-environment`, `co1-housing-research-global-south`.

## 5. Evidence-empty slices (0)

Every ACTIVE slice carries at least one linked source-instance — no evidence-empty slices in the current corpus.

## 6. Findings & recommended remediation

1. **Strengthen the ◐ partial and ○ weak bases toward ● full.** 11 slices anchor only at ◐ partial (T4/T5 standards practice) and none rest on a ○ weak-only base. With only 104 systematic-review/evidence-based-standard instances corpus-wide, the ● full synthesis tier is the thinnest. Prioritise SR/meta-analysis + DPO-standard recovery on the partial/weak slices to lift them to full-strength anchoring, and replace the 10 DISPUTED sources (§4) with verifiable citations.
2. **Convert non-English search into non-English evidence.** Searches ran in 19 languages but the corpus is ~76% English. Target the languages already searched-with-results but under-linked, and the zero-yield languages (`ar`, `bn`, `hi`, `sw`) explicitly.
3. **De-risk monojurisdictional slices.** 3 evidenced slices rest on ≤1 jurisdiction; flag their numeric thresholds as non-transferable until a second regime is sourced.
4. **Keep the corpus free of silent gaps.** No ACTIVE slice is currently un-started or evidence-empty; hold that line as new slices are added.
5. **Treat the doubly-concentrated slices as citation-risk.** The 20 ≥90%-English-and-≥50%-Anglophone slices are where global-applicability claims are weakest.

## 7. Limitations & what this audit does *not* claim

- **Instance-weighted, not source-weighted.** The 947 instances are 739 unique sources, so corpus tier/language totals run ~28% above unique-source counts. Per-slice figures are unaffected.
- **The composite is a lens, not ground truth.** Weights (20/30/20/15/15) are a defensible but editorial choice; the six raw dimensions are printed alongside every grade so a reader can re-weight. No grade is stored in the DB — it is recomputed each run.
- **Coverage ≠ correctness.** The audit measures the *shape* of each base (how much, what tier, where from, what language, how concentrated). It does **not** re-verify that any citation resolves, is current, or supports its claim — those are the `url_verification_runs` / `code_currency` / supersession checks, run separately.
- **Jurisdiction shares rest on recorded jurisdictions only.** NULL-jurisdiction instances are excluded from %ANG denominators, so a low %ANG can mean *genuinely non-Anglophone* or *unrecorded* — the master table’s JUR count exposes the denominator.
- **Compound jurisdictions classify by their strongest Anglophone member** (e.g. `US/AU/INT` counts as native-Anglophone). Magnitude ≈1% of instances.

## 8. Per-specification (item) adjudication — inheritance view

The Guidebook’s **93 design specifications** (the `items` table, categories A–K) do **not** carry their own evidence links — each *inherits* the evidentiary base of the research slug it draws on (`items.bpc_source_slug`). This section adjudicates every specification by that inherited base, so a spec built on a thin or unanchored slug is visible as such. (A spec with no source slug cannot inherit and is a coverage gap.)

| Basis health | Specs | Meaning |
|---|---|---|
| full | 84 | inherits a ● full (adjudicated) anchor base |
| partial | 3 | inherits a ◐ partial (standards-practice) anchor base |
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
*Data as of 2026-07-21 · read-only over `data/guidebook.db` · generated by `tools/evidentiary_audit.py`. Independently red-teamed; raw counts reproduce through a second code path. Aligned to `governance/tier-system.md`.*
