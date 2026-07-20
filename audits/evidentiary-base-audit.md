# Per-Slice Evidentiary Audit
**Data as of:** 2026-07-20 · **Scope:** all 79 ACTIVE research slices (slugs) in `data/guidebook.db` · **Method:** read-only aggregation over `source_slug_links → evidence_sources`, `search_languages`, `search_coverage`, `bpc_metadata`.

This audit scores every research slice on the six requested dimensions — (1) amount of evidence, (2) tiers of evidence, (3) jurisdictions sourced, (4) languages sourced, (5) English/Anglophone bias, and (6) overall quality of the evidentiary base — and rolls them into a transparent 0–100 composite grade. It audits the **raw evidence linked to each slice**, i.e. the material available for (re-)derivation; it does not re-judge synthesis prose.

> **Reproducibility.** Every number here is regenerated from the DB by `tools/evidentiary_audit.py` — nothing is hand-transcribed, and the “data as of” date is the DB’s own `max(updated_at)`, so identical data yields byte-identical output. No grade is stored in the DB; the composite is a *derived* view whose rubric is fully specified in §2, so any reader can recompute it. Companion outputs: `evidentiary-base-audit.json` / `.csv`, and the interactive `tools/evidentiary-audit-dashboard.html` (filter by corpus / category / term).

> **Adversarial review (two passes).** The audit was independently red-teamed twice; all raw counts (volume, tiers, language/jurisdiction distributions, search yield) reproduce exactly through a second code path. Folded in: (i) the **best-practice split** — *anchor* (T1/Co-1/T2/Co-2, the only tiers §3 lets anchor a best-practice claim) is now separated from *confirmed* (adds T3-clinical, ● per §5); a T3-clinical-only slice is confirmed evidence but flagged **no-anchor** (§2, §4); (ii) a **convergence discount** so code-floor-only slices can’t score highly on breadth alone (§2, §6); (iii) full disclosure of the **77 NULL-jurisdiction instances** (§3.5); (iv) **true-jurisdiction** breadth scoring that excludes the 0 language codes () mis-filed in the `jurisdiction` column (§3.3).

## 1. Executive summary

- **948 source-instances** are linked across **79 of 79 slices**; **0 slices carry zero linked evidence**.
- **Grade distribution:** A=7 · B=14 · C=27 · D=17 · E=14 · F=0  (A≥80, B≥65, C≥50, D≥35, E>0, F=empty).
- **Tier profile is code-and-clinical heavy, synthesis-light.** Of linked instances: T1=93, T2=113, T3=350, T4=86, T5=155, T6=151. Only **113 Tier-2 (systematic-review / evidence-based-standard) instances** exist across the whole corpus — the synthesis tier that best anchors best-practice claims is the thinnest.
- **Best-practice anchoring is thin.** Only **206/948 (22%)** of instances can *anchor* a best-practice claim (T1/Co-1/T2/Co-2, §3); a further 290 are confirmed-but-supporting T3-clinical (● §5). **30 slices have no anchor at all** (13 code-floor, 17 T3-clinical-only).
- **Anglophone concentration is the dominant quality risk.** **716/948 (76%) of linked sources are English-language**; only 232 are non-English. By jurisdiction, 353 instances are native-Anglophone (US/UK/AU/CA/NZ/IE), 210 supranational (INT/EU/ISO), 308 other, 77 unrecorded.
- **Search breadth ≠ evidentiary yield.** Slices were searched across **19 languages** and ~48 jurisdictions, but 4 searched languages (`ar`, `bn`, `hi`, `sw`) returned **zero** usable sources in **every** slice. The bias lives in what converted to evidence, not in search effort.

## 2. Method & definitions

**Slice = slug.** The 79 ACTIVE slugs are the unit of audit. Evidence is attributed through `source_slug_links`; each linked `evidence_sources` row is one *source-instance* (a source shared by two slices counts once in each). The 948 instances collapse to **781 unique sources** (reuse factor 1.21×; 120 sources span >1 slice, one — `REF-00050` — spans 6). Instance-weighting is deliberate — it measures per-slice coverage — but shared sources are re-counted, so corpus tier/language totals read ~21% above unique-source counts. (23 of the 804 rows in `evidence_sources` are linked to no active slug.)

**Tiers** follow `governance/tier-system.md` (OPERATIVE 2026-05-25). Tier number reflects *what kind of claim a source can anchor*, not raw quality:

| Tier | Character | Anchors |
|---|---|---|
| T1 / Co-1 | primary research / disability-led lived experience | best-practice claims |
| T2 / Co-2 | systematic review · meta-analysis · evidence-based standard / OT CPG | best-practice claims |
| T3 | lower-control clinical (●) + grey primary (○) | supporting |
| T4 | international standards (ISO/IEC/CEN) | code-baseline |
| T5 | national beyond-code frameworks (BS 8300, DIN 18040) | code-baseline |
| T6 | statutory code (ADA, AS 1428.1) | code-floor only |

**Two distinct measures, per the doctrine.** §3 and §5 answer different questions, so the audit tracks both:

- **Best-practice *anchor* (§3)** = T1, Co-1, T2, Co-2. These are the *only* tiers that can anchor a best-practice claim. This is the primary strength signal (column **BP** in §4).
- **Confirmed evidence (§5, ●)** = the anchor set *plus* T3-clinical (lower-control primary research — confirmed, but “rarely the sole basis” per §1, so it *supports* rather than *anchors*). T3-grey (○), T4, T5, T6 are not confirmed.

A slice with sources but **zero anchors** is flagged **no-anchor**: either *code-floor* (0 confirmed — the T4–T6 “convergence-is-not-evidence” trap of §3) or *supporting-only* (confirmed T3-clinical but no anchor). Neither can carry a best-practice claim on its own.

**Anglophone classification** of a jurisdiction: *native-Anglophone* = US, UK, AU, CA, NZ, IE; *supranational/English-medium* = INT, EU, ISO, ASEAN; *English-official (non-native)* = SG, HK, IN, NG, GH, ZA, MY, AE, SA; everything else *non-Anglophone*. Language uses `lang_detected` (`en`/`eng`→English).

**Composite score (0–100)** = five transparent components, higher = stronger base:

| Comp | Max | Measures |
|---|---|---|
| A Volume | 20 | count of linked source-instances |
| B Tier strength | 30 | anchor share (full weight) + T3-clinical share (partial) + anchor-present bonus |
| C Jurisdictional breadth | 20 | distinct *true* jurisdictions (mis-filed language codes excluded) |
| D Linguistic breadth | 15 | distinct languages; capped at 4 if English-only |
| E Anglophone balance | 15 | rewards distance from 100% English + 100% Anglo-core concentration |

Grades: **A**≥80 · **B**≥65 · **C**≥50 · **D**≥35 · **E**>0 · **F**=empty. The score rewards a *balanced, multi-jurisdiction, multi-language, synthesis-anchored* base and penalises thin or monolingual ones; it is a triage lens, not a verdict on any single citation.

**Convergence discount.** Per §3, a slice whose entire base is code-floor (T4–T6 + grey; **zero confirmed** evidence) is a *convergence* base: breadth of such sources across many jurisdictions is “convergence, not evidence.” Without a correction it can out-score a genuinely well-evidenced but narrow slice purely on breadth. The rubric therefore **halves the breadth components (C, D) for code-floor slices**, each flagged *convergence-only* (‡). A *supporting-only* slice (T3-clinical but no anchor) keeps its breadth credit — that breadth is real primary evidence — but still earns low B and carries the **no-anchor** flag (†).

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

**Best-practice-anchor share: 206/948 (22%)** (T1/Co-1/T2/Co-2, §3). Adding confirmed-but-supporting T3-clinical brings *confirmed* evidence to 496/948 (52%). The remaining 452 are T4–T6 code/standards + T3-grey that carry no confirmed evidence. Slices with zero anchors are the sharpest risk — see the no-anchor list in §4.

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
| id | 2 |
| ar | 2 |
| bn | 1 |

Distinct source languages: **17** (`en`/`eng` merged; raw ISO codes may be one more). English dominates at 76%. The non-English corpus is overwhelmingly Western-European + East-Asian; the only languages outside that group to yield *any* linked source are: ar (2); id (2); bn (1).

**36 non-empty slices are English-only** (46% of evidenced slices).

### (5) English / Anglophone bias
- **Language axis:** 76% English. 36 slices 100% English.
- **Jurisdiction axis (all 948 instances):** native-Anglophone (US/UK/AU/CA/NZ/IE) **353** · supranational/English-medium (INT/EU/ISO) **210** · English-official + other non-Anglophone **308** · **no jurisdiction recorded 77**. (These four sum to 948 = all instances.)
- **19 slices are doubly-concentrated** (≥90% English *and* ≥50% native-Anglophone jurisdiction): `manoeuvring-footprint-vs-turning-radius-methodology`, `economics-sources`, `air-quality-voc-chemical-sensitivity-built-environment`, `upper-limb-impairment-built-environment`, `ot-cpg-built-environment`, `sensory-relief-space-design`, `accessibility-feature-market-value-uplift-framing`, `ot-frameworks-built-environment`, `ot-built-environment-interface`, `residential-accessible-home-case-studies`, `sensory-processing-model-design-application`, `ofs-built-environment`, `government-grant-programmes`, `case-study-economics-financial-data`, `cross-population-case-studies`, `bariatric-turning-radius-built-environment`, `luminance-contrast-lrv-evidence-base`, `accessible-design-failures-poor-performance`, `residential-dar-provisions-priority-register`.
- **Process counter-evidence:** non-English/Global-South *searches were run* (19 languages across 81 of 79 slices in `search_languages`) but `ar`, `bn`, `hi`, `sw` yielded nothing linkable in any slice. The gap is a *yield/recovery* gap, not a *search-effort* gap.

### (6) Overall quality of the evidentiary base
| Grade | Slices | Meaning |
|---|---|---|
| A | 7 | strong, balanced, synthesis-anchored |
| B | 14 | solid, some concentration or tier gaps |
| C | 27 | usable but thin or monolingual |
| D | 17 | weak — few sources / single jurisdiction / English-only |
| E | 14 | very weak — 1 jurisdiction, no anchor |
| F | 0 | empty — no linked evidence |

## 4. Master per-slice table (ranked by composite score)

Legend: **N** linked sources · **BP** best-practice-anchor count (T1/Co-1/T2/Co-2) · **CF** confirmed (incl T3-clinical) · **JUR** distinct *true* jurisdictions · **LNG** distinct languages · **%EN** English-language share · **%ANG** native-Anglophone share · **A/B/C/D/E** score components · **‡** convergence-only (code-floor, breadth discounted) · **†** no-anchor supporting-only (confirmed T3-clinical but nothing to anchor best practice).

| # | Grade | Score | Slice | Topic | N | BP | CF | Tiers | JUR | LNG | %EN | %ANG | A·B·C·D·E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **A** | 83.7 | `wayfinding-dementia-spatial-design` | wayfinding-and-signage | 35 | 15 | 25 | T1×6,T2×9,T3×11,T5×5,T6×4 | 19 | 13 | 60.0 | 36.4 | 20·20.9·20·15·7.8 |
| 2 | **A** | 82.6 | `cognitive-wayfinding-design` | wayfinding-and-signage | 25 | 6 | 16 | T2×6,T3×11,T5×7,T6×1 | 13 | 9 | 64.0 | 8.0 | 20·18.0·20·15·9.6 |
| 3 | **A** | 81.4 | `residential-kitchen-and-task-surfaces` | kitchens-and-workspaces | 30 | 14 | 20 | T1×2,T2×12,T3×6,T4×2,T5×3,T6×5 | 10 | 7 | 80.0 | 46.2 | 20·20.9·20·15·5.5 |
| 4 | **A** | 81.4 | `sensory-room-user-control` | sensory-environment | 14 | 6 | 13 | T2×6,T3×7,T6×1 | 9 | 4 | 71.4 | 38.5 | 20·22.6·20·12·6.8 |
| 5 | **A** | 81.1 | `mobility-built-environment` | population-general | 24 | 9 | 14 | T1×7,T2×2,T3×6,T5×4,T6×5 | 17 | 9 | 58.3 | 50.0 | 20·19.2·20·15·6.9 |
| 6 | **A** | 80.8 | `room-acoustic-performance` | sensory-environment | 32 | 15 | 19 | T1×14,T2×1,T3×6,T4×2,T5×8,T6×1 | 13 | 8 | 78.1 | 50.0 | 20·20.4·20·15·5.4 |
| 7 | **A** | 80.0 | `deaf-spatial-design` | communication-and-alerts | 13 | 6 | 8 | T1×5,T2×1,T3×5,T5×1,T6×1 | 8 | 5 | 61.5 | 38.5 | 20·20.5·20·12·7.5 |
| 8 | **B** | 79.9 | `accessible-bathroom-and-grab-bar` | bathrooms-and-wet-areas | 23 | 11 | 13 | T1×7,T2×4,T3×3,T4×1,T5×4,T6×4 | 13 | 7 | 73.9 | 65.0 | 20·20.3·20·15·4.6 |
| 9 | **B** | 79.5 | `deaf-classroom-reverberation-time` | communication-and-alerts | 12 | 2 | 2 | T1×2,T4×1,T5×6,T6×3 | 9 | 9 | 25.0 | 25.0 | 20·13.3·20·15·11.2 |
| 10 | **B** | 79.0 | `stair-ramp-threshold-biomechanics-accessibility` | entrances-and-circulation | 27 | 1 | 14 | T2×1,T3×14,T4×1,T5×1,T6×10 | 15 | 12 | 59.3 | 14.8 | 20·14.6·20·15·9.4 |
| 11 | **B** | 78.5 | `mental-health-built-environment` | population-general | 37 | 6 | 28 | T1×3,T2×3,T3×28,T4×1,T5×2 | 11 | 5 | 59.5 | 27.0 | 20·18.0·20·12·8.5 |
| 12 | **B** | 74.8 | `residential-entry-and-threshold` | entrances-and-circulation | 20 | 3 | 4 | T2×3,T3×1,T4×1,T5×6,T6×9 | 13 | 7 | 65.0 | 50.0 | 20·13.4·20·15·6.4 |
| 13 | **B** | 74.3 | `deafblind-built-environment-design` | population-general | 9 | 7 | 7 | T1×3,T2×4,T3×1,T6×1 | 5 | 3 | 66.7 | 44.4 | 16·25.6·17·9·6.7 |
| 14 | **B** | 74.0 | `accessible-circulation-geometry` | entrances-and-circulation | 14 | 1 | 3 | T2×1,T3×2,T4×1,T5×3,T6×7 | 9 | 6 | 64.3 | 50.0 | 20·12.6·20·15·6.4 |
| 15 | **B** | 72.7 | `visual-impairment-built-environment` | population-general | 8 | 1 | 1 | T2×1,T3×1,T4×2,T5×1,T6×3 | 7 | 6 | 25.0 | 12.5 | 16·12.5·17·15·12.2 |
| 16 | **B** | 71.2 | `assistive-listening-systems` | communication-and-alerts | 8 | 2 | 2 | T2×2,T3×2,T4×1,T5×1,T6×2 | 5 | 5 | 50.0 | 0.0 | 16·15.0·17·12·11.2 |
| 17 | **B** | 70.0 | `sensory-space-global-south` | sensory-environment | 15 | 4 | 9 | T1×3,T2×1,T3×9,T5×1,T6×1 | 7 | 2 | 60.0 | 7.1 | 20·18.0·17·5·10.0 |
| 18 | **B** | 68.6 | `pain-ofs-built-environment-design` | health-and-symptom-management | 12 | 5 | 5 | T1×2,T2×3,T3×3,T5×3,T6×1 | 6 | 3 | 83.3 | 60.0 | 20·18.3·17·9·4.3 |
| 19 | **B** | 68.3 | `bathroom-typology-global-south` | bathrooms-and-wet-areas | 8 | 2 | 4 | T1×1,T2×1,T3×2,T4×1,T6×3 | 4 | 4 | 62.5 | 0.0 | 16·17.0·13·12·10.3 |
| 20 | **B** | 67.8 | `post-occupancy-evaluation-global` | frameworks-and-methodology | 10 | 3 | 10 | T2×3,T3×7 | 8 | 2 | 90.0 | 40.0 | 16·21.6·20·5·5.2 |
| 21 | **B** † | 66.5 | `wayfinding-global-south` | wayfinding-and-signage | 15 | 0 | 1 | T3×1,T4×4,T6×10 | 13 | 7 | 53.3 | 0.0 | 20·0.5·20·15·11.0 |
| 22 | **C** † | 64.6 | `threshold-door-hardware` | entrances-and-circulation | 32 | 0 | 2 | T3×2,T4×1,T5×9,T6×20 | 26 | 13 | 46.9 | 31.2 | 20·0.5·20·15·9.1 |
| 23 | **C** | 62.0 | `deaf-acoustic-built-environment` | communication-and-alerts | 10 | 4 | 4 | T1×2,T2×2,T3×1,T4×3,T5×2 | 5 | 2 | 90.0 | 30.0 | 16·18.0·17·5·6.0 |
| 24 | **C** | 61.6 | `circadian-lighting-melanopic-edi` | sensory-environment | 12 | 2 | 7 | T2×2,T3×5,T4×2,T5×3 | 4 | 2 | 91.7 | 16.7 | 20·16.7·13·5·6.9 |
| 25 | **C** † | 60.5 | `construction-cost-data` | economics | 12 | 0 | 6 | T3×11,T6×1 | 8 | 3 | 58.3 | 41.7 | 20·4.0·20·9·7.5 |
| 26 | **C** | 60.5 | `manoeuvring-footprint-vs-turning-radius-methodology` | frameworks-and-methodology | 30 | 18 | 28 | T1×14,T2×4,T3×11,T4×1 | 3 | 1 | 100.0 | 62.5 | 20·24.7·13·0·2.8 |
| 27 | **C** † | 59.2 | `multilingual-evidence-convergence-non-english` | frameworks-and-methodology | 8 | 0 | 3 | T3×6,T5×2 | 7 | 4 | 50.0 | 0.0 | 16·3.0·17·12·11.2 |
| 28 | **C** | 59.1 | `neurological-built-environment` | population-general | 8 | 1 | 8 | T1×1,T3×7 | 5 | 1 | 100.0 | 12.5 | 16·19.5·17·0·6.6 |
| 29 | **C** † | 59.0 | `accessible-design-economics-cost-premium` | economics | 14 | 0 | 7 | T3×13,T6×1 | 7 | 3 | 57.1 | 23.1 | 20·4.0·17·9·9.0 |
| 30 | **C** | 59.0 | `school-environment-autism` | sensory-environment | 17 | 5 | 17 | T1×2,T2×3,T3×12 | 4 | 1 | 100.0 | 40.0 | 20·21.5·13·0·4.5 |
| 31 | **C** † | 58.4 | `dementia-built-environment` | population-general | 8 | 0 | 4 | T3×5,T5×3 | 5 | 4 | 62.5 | 12.5 | 16·4.0·17·12·9.4 |
| 32 | **C** | 58.3 | `neurodivergent-built-environment` | population-general | 9 | 6 | 8 | T1×2,T2×4,T3×2,T4×1 | 4 | 1 | 100.0 | 44.4 | 16·25.1·13·0·4.2 |
| 33 | **C** | 57.3 | `economics-sources` | economics | 23 | 3 | 23 | T1×2,T2×1,T3×20 | 6 | 1 | 100.0 | 90.9 | 20·19.6·17·0·0.7 |
| 34 | **C** | 56.8 | `thermal-comfort-older-adults-care-settings` | health-and-symptom-management | 6 | 2 | 4 | T2×2,T3×3,T5×1 | 4 | 2 | 83.3 | 16.7 | 12·19.3·13·5·7.5 |
| 35 | **C** | 56.5 | `air-quality-voc-chemical-sensitivity-built-environment` | sensory-environment | 12 | 1 | 7 | T2×1,T3×6,T4×4,T5×1 | 7 | 1 | 100.0 | 50.0 | 20·15.7·17·0·3.8 |
| 36 | **C** | 56.4 | `upper-limb-impairment-built-environment` | population-general | 17 | 3 | 16 | T1×1,T2×2,T3×14 | 4 | 1 | 100.0 | 50.0 | 20·19.6·13·0·3.8 |
| 37 | **C** | 56.3 | `ot-cpg-built-environment` | population-general | 6 | 6 | 6 | T2×6 | 4 | 1 | 100.0 | 83.3 | 12·30·13·0·1.3 |
| 38 | **C** | 56.0 | `biophilic-design-healthcare-workplace` | sensory-environment | 6 | 4 | 6 | T1×1,T2×3,T3×2 | 3 | 1 | 100.0 | 33.3 | 12·26.0·13·0·5.0 |
| 39 | **C** | 55.2 | `visitability-residential-accessibility-minimum-standards` | frameworks-and-methodology | 7 | 1 | 1 | T1×1,T5×1,T6×5 | 5 | 3 | 71.4 | 71.4 | 12·12.9·17·9·4.3 |
| 40 | **C** | 55.1 | `acoustics-speech-intelligibility-disability` | sensory-environment | 8 | 3 | 5 | T2×3,T3×2,T4×3 | 4 | 1 | 100.0 | 12.5 | 16·19.5·13·0·6.6 |
| 41 | **C** | 54.5 | `sensory-relief-space-design` | sensory-environment | 10 | 3 | 8 | T2×3,T3×5,T4×1,T6×1 | 6 | 1 | 100.0 | 80.0 | 16·20.0·17·0·1.5 |
| 42 | **C** † | 53.2 | `accessibility-feature-market-value-uplift-framing` | economics | 33 | 0 | 8 | T3×10,T4×4,T5×15,T6×4 | 11 | 3 | 90.9 | 78.8 | 20·1.9·20·9·2.3 |
| 43 | **C** | 53.0 | `ms-thermal-temperature-conflict-resolution` | health-and-symptom-management | 10 | 2 | 7 | T1×1,T2×1,T3×5,T4×2,T5×1 | 4 | 1 | 100.0 | 20.0 | 16·18.0·13·0·6.0 |
| 44 | **C** | 52.9 | `ot-frameworks-built-environment` | frameworks-and-methodology | 4 | 4 | 4 | T1×4 | 3 | 1 | 100.0 | 75.0 | 8·30·13·0·1.9 |
| 45 | **C** ‡ | 52.5 | `luminance-contrast-and-pattern` | wayfinding-and-signage | 13 | 0 | 0 | T5×4,T6×9 | 13 | 13 | 0.0 | 0.0 | 20·0.0·10.0·7.5·15.0 |
| 46 | **C** | 52.2 | `ot-built-environment-interface` | frameworks-and-methodology | 16 | 1 | 14 | T2×1,T3×15 | 3 | 1 | 100.0 | 80.0 | 20·17.8·13·0·1.5 |
| 47 | **C** | 51.6 | `residential-accessible-home-case-studies` | frameworks-and-methodology | 8 | 3 | 7 | T1×2,T2×1,T3×5 | 4 | 1 | 100.0 | 85.7 | 16·21.5·13·0·1.1 |
| 48 | **C** | 50.5 | `ndv-aut-built-environment-quantified-thresholds` | population-general | 6 | 2 | 4 | T2×2,T3×3,T4×1 | 3 | 1 | 100.0 | 16.7 | 12·19.3·13·0·6.2 |
| 49 | **D** | 49.3 | `detectable-gradient-protocol-sensory-zones` | wayfinding-and-signage | 6 | 2 | 4 | T2×2,T3×2,T4×2 | 4 | 1 | 100.0 | 33.3 | 12·19.3·13·0·5.0 |
| 50 | **D** | 48.9 | `design-framework-evidence-audit` | frameworks-and-methodology | 9 | 1 | 4 | T2×1,T3×5,T4×2,T5×1 | 4 | 1 | 100.0 | 33.3 | 16·14.9·13·0·5.0 |
| 51 | **D** | 47.7 | `floor-vibration-wheelchair-disability` | entrances-and-circulation | 7 | 1 | 4 | T2×1,T3×3,T4×3 | 3 | 1 | 100.0 | 14.3 | 12·16.3·13·0·6.4 |
| 52 | **D** ‡ | 46.6 | `jurisdiction-matrix-accessibility-standards` | frameworks-and-methodology | 14 | 0 | 0 | T4×4,T6×10 | 12 | 6 | 64.3 | 14.3 | 20·0.0·10.0·7.5·9.1 |
| 53 | **D** | 46.1 | `sensory-processing-model-design-application` | sensory-environment | 6 | 1 | 4 | T2×1,T3×3,T4×1,T5×1 | 4 | 1 | 100.0 | 50.0 | 12·17.3·13·0·3.8 |
| 54 | **D** ‡ | 46.0 | `threshold-and-level-access` | entrances-and-circulation | 15 | 0 | 0 | T4×1,T5×4,T6×10 | 12 | 8 | 46.7 | 40.0 | 20·0.0·10.0·7.5·8.5 |
| 55 | **D** | 45.8 | `ofs-built-environment` | health-and-symptom-management | 7 | 3 | 4 | T1×3,T3×1,T5×2,T6×1 | 3 | 1 | 100.0 | 85.7 | 12·19.7·13·0·1.1 |
| 56 | **D** | 45.6 | `visual-fire-alarm-seizure-safety` | sensory-environment | 7 | 1 | 4 | T2×1,T3×3,T4×2,T6×1 | 3 | 1 | 100.0 | 42.9 | 12·16.3·13·0·4.3 |
| 57 | **D** † | 45.4 | `reach-range-and-accessible-controls` | controls-and-hardware | 11 | 0 | 1 | T3×1,T5×5,T6×5 | 6 | 3 | 81.8 | 81.8 | 16·0.7·17·9·2.7 |
| 58 | **D** | 43.9 | `government-grant-programmes` | economics | 4 | 1 | 4 | T2×1,T3×3 | 3 | 1 | 100.0 | 75.0 | 8·21.0·13·0·1.9 |
| 59 | **D** † | 43.8 | `fold-down-grab-bar-specification` | bathrooms-and-wet-areas | 8 | 0 | 2 | T3×2,T4×2,T5×2,T6×2 | 5 | 2 | 87.5 | 62.5 | 16·2.0·17·5·3.8 |
| 60 | **D** ‡ | 42.7 | `jurisdiction-grant-programmes-comprehensive` | frameworks-and-methodology | 9 | 0 | 0 | T5×9 | 9 | 6 | 44.4 | 33.3 | 16·0.0·10.0·7.5·9.2 |
| 61 | **D** | 39.0 | `case-study-economics-financial-data` | economics | 4 | 2 | 3 | T1×1,T2×1,T3×1,T5×1 | 2 | 1 | 100.0 | 100.0 | 8·22.0·9·0·0.0 |
| 62 | **D** | 39.0 | `cross-population-case-studies` | frameworks-and-methodology | 3 | 1 | 3 | T1×1,T3×2 | 2 | 1 | 100.0 | 100.0 | 8·22.0·9·0·0.0 |
| 63 | **D** ‡ | 36.5 | `body-sizes-supplementary-populations` | frameworks-and-methodology | 11 | 0 | 0 | T3×2,T4×4,T5×5 | 5 | 3 | 63.6 | 36.4 | 16·0.0·8.5·4.5·7.5 |
| 64 | **D** ‡ | 36.1 | `visual-alerting-and-wayfinding-light` | wayfinding-and-signage | 7 | 0 | 0 | T4×2,T5×2,T6×3 | 7 | 5 | 42.9 | 28.6 | 12·0.0·8.5·6.0·9.6 |
| 65 | **D** † | 35.0 | `ecological-psychology-haptic-affordances-built-environment` | frameworks-and-methodology | 5 | 0 | 5 | T3×5 | 2 | 1 | 100.0 | 20.0 | 12·8.0·9·0·6.0 |
| 66 | **E** † | 33.3 | `wayfinding-cognitive-science-spatial-design` | wayfinding-and-signage | 7 | 0 | 7 | T3×7 | 2 | 1 | 100.0 | 42.9 | 12·8.0·9·0·4.3 |
| 67 | **E** † | 32.7 | `intellectual-disability-built-environment-design` | population-general | 5 | 0 | 2 | T3×2,T4×3 | 3 | 1 | 100.0 | 40.0 | 12·3.2·13·0·4.5 |
| 68 | **E** ‡ | 31.7 | `european-accessibility-act-scope-clarification` | frameworks-and-methodology | 6 | 0 | 0 | T5×2,T6×4 | 4 | 3 | 66.7 | 16.7 | 12·0.0·6.5·4.5·8.7 |
| 69 | **E** † | 31.0 | `bariatric-turning-radius-built-environment` | seating-and-rest | 8 | 0 | 2 | T3×3,T4×2,T5×3 | 4 | 1 | 100.0 | 100.0 | 16·2.0·13·0·0.0 |
| 70 | **E** † | 29.6 | `luminance-contrast-lrv-evidence-base` | wayfinding-and-signage | 7 | 0 | 4 | T3×4,T5×2,T6×1 | 4 | 1 | 100.0 | 100.0 | 12·4.6·13·0·0.0 |
| 71 | **E** † | 28.7 | `cross-population-conflict-resolutions` | frameworks-and-methodology | 6 | 0 | 2 | T3×2,T4×3,T5×1 | 2 | 1 | 100.0 | 33.3 | 12·2.7·9·0·5.0 |
| 72 | **E** ‡ | 28.0 | `accessible-laundry-room-design` | room-types | 6 | 0 | 0 | T4×3,T5×3 | 4 | 3 | 66.7 | 66.7 | 12·0.0·6.5·4.5·5.0 |
| 73 | **E** † | 27.7 | `thermoregulation-built-environment` | health-and-symptom-management | 5 | 0 | 2 | T3×4,T4×1 | 1 | 1 | 100.0 | 0.0 | 12·3.2·5·0·7.5 |
| 74 | **E** ‡ | 27.3 | `government-grant-programmes-home-adaptation` | economics | 7 | 0 | 0 | T5×7 | 6 | 2 | 71.4 | 71.4 | 12·0.0·8.5·2.5·4.3 |
| 75 | **E** † | 26.8 | `accessible-design-failures-poor-performance` | frameworks-and-methodology | 4 | 0 | 3 | T3×4 | 2 | 1 | 100.0 | 50.0 | 8·6.0·9·0·3.8 |
| 76 | **E** ‡ | 26.4 | `therapeutic-lighting-design` | sensory-environment | 4 | 0 | 0 | T4×1,T5×3 | 3 | 2 | 75.0 | 0.0 | 8·0.0·6.5·2.5·9.4 |
| 77 | **E** ‡ | 22.0 | `crpd-implementation-built-environment` | frameworks-and-methodology | 5 | 0 | 0 | T4×5 | 1 | 1 | 100.0 | 0.0 | 12·0.0·2.5·0.0·7.5 |
| 78 | **E** ‡ | 19.8 | `residential-dar-provisions-priority-register` | frameworks-and-methodology | 6 | 0 | 0 | T4×1,T5×4,T6×1 | 3 | 1 | 100.0 | 83.3 | 12·0.0·6.5·0.0·1.3 |
| 79 | **E** ‡ | 18.0 | `co1-housing-research-global-south` | frameworks-and-methodology | 3 | 0 | 0 | T4×3 | 1 | 1 | 100.0 | 0.0 | 8·0.0·2.5·0.0·7.5 |

**No-anchor slices (30)** — real sources but **zero best-practice anchors** (no T1/Co-1/T2/Co-2), so the base cannot carry a best-practice claim on its own. Two kinds:
- **‡ Code-floor / convergence-only (13)** — 0 confirmed evidence (pure T4–T6/grey); breadth is discounted. Read grades as coverage, not quality: `luminance-contrast-and-pattern`, `jurisdiction-matrix-accessibility-standards`, `threshold-and-level-access`, `jurisdiction-grant-programmes-comprehensive`, `body-sizes-supplementary-populations`, `visual-alerting-and-wayfinding-light`, `european-accessibility-act-scope-clarification`, `accessible-laundry-room-design`, `government-grant-programmes-home-adaptation`, `therapeutic-lighting-design`, `crpd-implementation-built-environment`, `residential-dar-provisions-priority-register`, `co1-housing-research-global-south`.
- **† Supporting-only (17)** — confirmed T3-clinical primary evidence but no anchor; genuine supporting evidence that still needs a T1/Co-1/T2/Co-2 anchor to make a best-practice claim: `wayfinding-global-south`, `threshold-door-hardware`, `construction-cost-data`, `multilingual-evidence-convergence-non-english`, `accessible-design-economics-cost-premium`, `dementia-built-environment`, `accessibility-feature-market-value-uplift-framing`, `reach-range-and-accessible-controls`, `fold-down-grab-bar-specification`, `ecological-psychology-haptic-affordances-built-environment`, `wayfinding-cognitive-science-spatial-design`, `intellectual-disability-built-environment-design`, `bariatric-turning-radius-built-environment`, `luminance-contrast-lrv-evidence-base`, `cross-population-conflict-resolutions`, `thermoregulation-built-environment`, `accessible-design-failures-poor-performance`.

## 5. Evidence-empty slices (0)

These carry **zero** linked source-instances. `bpc_metadata.evidence_state` distinguishes:

**Retracted pending rehabilitation (0)** — prior work cleared, awaiting re-derivation:

**Un-started / placeholder (0)** — `evidence_state` unset, search not run:

Several name high-salience topics where an empty base is a material coverage gap, not bookkeeping.

## 6. Findings & recommended remediation

1. **Thicken the anchor tiers (T1/Co-1/T2/Co-2).** With only 113 systematic-review/evidence-based-standard instances corpus-wide, most best-practice claims lean on individual T1 primary studies or on code convergence (T4–T6, disallowed as best-practice warrant). Prioritise SR/meta-analysis + DPO-standard recovery on the 30 no-anchor slices — especially the 17 supporting-only ones, which already hold confirmed T3-clinical evidence and need only an anchor to become citable.
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
| ok | 63 | inherits a graded base |
| no-anchor | 16 | base has no best-practice anchor |
| code-floor | 8 | base is code-floor / convergence-only |
| no-source | 6 | no source slug — cannot inherit |

**63 of 93 specs inherit a fully-graded, anchored base; 30 rest on a weak or missing base** and are the priority remediation set.

### By category
| Cat | Specifications | Specs | On weak/missing base |
|---|---|---|---|
| A | Acoustics | 19 | 2 |
| B | Lighting | 12 | 7 |
| C | Colour and Contrast | 6 | 4 |
| D | Wayfinding and Cognition | 11 | 1 |
| E | Circulation and Access | 14 | 3 |
| F | Sensory Environment | 8 | 2 |
| G | Furniture, Fixtures and Spatial Layout | 9 | 5 |
| H | Controls and Technology | 5 | 4 |
| I | Hardware and Fixtures | 4 | 1 |
| K | DeafBlind Provisions | 5 | 1 |

### Specifications resting on a weak or missing base

| Item | Category | Specification | Source slug | Basis | Inh. grade |
|---|---|---|---|---|---|
| `A-13` | A | No Sound Masking in Neurological Population Environm | — | no-source | — |
| `A-15` | A | Acoustic Differentiation Between Spaces (Navigation  | — | no-source | — |
| `B-03` | B | Elimination of Fluorescent Overhead Lighting | `therapeutic-lighting-design` | code-floor | E |
| `B-04` | B | Flicker-Free LED Luminaires (IEEE 1789-2015 Complian | `therapeutic-lighting-design` | code-floor | E |
| `B-05` | B | Gradual Lighting Transition Zones (≥5 m at All Major | `therapeutic-lighting-design` | code-floor | E |
| `B-06` | B | Individual Dimming Control (≥300 Lux Range) | `therapeutic-lighting-design` | code-floor | E |
| `B-07` | B | Indirect and Cove Lighting in Sensitive Spaces | `therapeutic-lighting-design` | code-floor | E |
| `B-08` | B | Matte, Low-Reflectance Floor Finishes (≤30 Gloss Uni | — | no-source | — |
| `B-12` | B | Sensor-Activated Overnight Pathway Lighting | `visual-alerting-and-wayfinding-light` | code-floor | D |
| `C-03` | C | Pattern Avoidance (Plain Flooring and Walls in Sensi | `luminance-contrast-lrv-evidence-base` | no-anchor | E |
| `C-04` | C | LRV Contrast (≥30 at All Critical Junctions) | `luminance-contrast-lrv-evidence-base` | no-anchor | E |
| `C-05` | C | Low LRV Differential at Adjacent Floor Materials (DE | `luminance-contrast-lrv-evidence-base` | no-anchor | E |
| `C-06` | C | Plain, Low-Contrast Flooring Throughout (No Geometri | `luminance-contrast-lrv-evidence-base` | no-anchor | E |
| `D-04` | D | Landmarks at Every Decision Point | `wayfinding-cognitive-science-spatial-design` | no-anchor | E |
| `E-05` | E | Weather Protection at Entry (Covered Canopy Minimum  | `threshold-and-level-access` | code-floor | D |
| `E-06` | E | Level Entry (Zero Step at All Accessible Entrances) | `threshold-and-level-access` | code-floor | D |
| `E-11` | E | Automatic Sliding Entry and Internal Doors | `threshold-door-hardware` | no-anchor | C |
| `F-07` | F | Thermal Zoning — Building-Wide Temperature Managemen | — | no-source | — |
| `F-08` | F | Thermal Transition — Heating and Cooling System Resp | `thermoregulation-built-environment` | no-anchor | E |
| `G-02` | G | Variety of Seating Types (Three Heights at Every Sea | — | no-source | — |
| `G-06` | G | Reception Counter (Accessible Height Section — 760-- | `reach-range-and-accessible-controls` | no-anchor | D |
| `G-07` | G | Waiting Area Seating (Accessible Configuration — Adj | — | no-source | — |
| `G-08` | G | Bedroom Wardrobe and Storage Reach Configuration | `reach-range-and-accessible-controls` | no-anchor | D |
| `G-09` | G | Bedroom Emergency Call Provision and Overnight Light | `reach-range-and-accessible-controls` | no-anchor | D |
| `H-01` | H | All Controls at Accessible Height (400--1100 mm AFF, | `reach-range-and-accessible-controls` | no-anchor | D |
| `H-02` | H | Individual Environmental Control (Lighting and Tempe | `reach-range-and-accessible-controls` | no-anchor | D |
| `H-04` | H | Accessible Intercom and Video Door Entry with Visual | `threshold-door-hardware` | no-anchor | C |
| `H-05` | H | Emergency Call — Multi-Position Reach Envelope | `reach-range-and-accessible-controls` | no-anchor | D |
| `I-01` | I | Hardware Throughout (Lever, D-Pull, One-Hand Operabl | `threshold-door-hardware` | no-anchor | C |
| `K-05` | K | Thermal Comfort Assessment for Thermoregulation-Impa | `thermoregulation-built-environment` | no-anchor | E |

The full per-specification table (all 93 items with inherited grade and dimension snapshot) is in `evidentiary-base-audit-items.csv` and the `items` array of the JSON; the dashboard’s **Specifications** view filters them by corpus / category / term.

---
*Data as of 2026-07-20 · read-only over `data/guidebook.db` · generated by `tools/evidentiary_audit.py`. Independently red-teamed; raw counts reproduce through a second code path. Aligned to `governance/tier-system.md`.*
