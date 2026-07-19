# Per-Slice Evidentiary Audit
**Data as of:** 2026-07-19 · **Scope:** all 82 ACTIVE research slices (slugs) in `data/guidebook.db` · **Method:** read-only aggregation over `source_slug_links → evidence_sources`, `search_languages`, `search_coverage`, `bpc_metadata`.

This audit scores every research slice on the six requested dimensions — (1) amount of evidence, (2) tiers of evidence, (3) jurisdictions sourced, (4) languages sourced, (5) English/Anglophone bias, and (6) overall quality of the evidentiary base — and rolls them into a transparent 0–100 composite grade. It audits the **raw evidence linked to each slice**, i.e. the material available for (re-)derivation; it does not re-judge synthesis prose.

> **Reproducibility.** Every number here is regenerated from the DB by `tools/evidentiary_audit.py` — nothing is hand-transcribed, and the “data as of” date is the DB’s own `max(updated_at)`, so identical data yields byte-identical output. No grade is stored in the DB; the composite is a *derived* view whose rubric is fully specified in §2, so any reader can recompute it. Companion outputs: `evidentiary-base-audit.json` / `.csv`, and the interactive `tools/evidentiary-audit-dashboard.html` (filter by corpus / category / term).

> **Adversarial review.** The first pass was independently red-teamed: all raw counts (volume, tiers, language/jurisdiction distributions, search yield) were recomputed through a second code path and reproduce exactly. Three changes are folded in — (i) a **convergence discount** so code-floor-only slices can’t score highly on breadth alone (§2, §6), (ii) full disclosure of the **18 NULL-jurisdiction instances** (§3.5), and (iii) a flagged **data-integrity defect**: 5 instances carry a language code (`DA`×1, `JA`×1, `ZH`×3) mis-filed in the `jurisdiction` column (§3.3).

## 1. Executive summary

- **749 source-instances** are linked across **69 of 82 slices**; **13 slices carry zero linked evidence**.
- **Grade distribution:** A=8 · B=19 · C=20 · D=13 · E=9 · F=13  (A≥80, B≥65, C≥50, D≥35, E>0, F=empty).
- **Tier profile is code-and-clinical heavy, synthesis-light.** Of linked instances: T1=100, T2=75, T3=218, T4=76, T5=146, T6=134. Only **75 Tier-2 (systematic-review / evidence-based-standard) instances** exist across the whole corpus — the synthesis tier that best anchors best-practice claims is the thinnest.
- **Anglophone concentration is the dominant quality risk.** **553/749 (74%) of linked sources are English-language**; only 196 are non-English. By jurisdiction, 295 instances are native-Anglophone (US/UK/AU/CA/NZ/IE), 192 supranational (INT/EU/ISO), 244 other, 18 unrecorded.
- **Search breadth ≠ evidentiary yield.** Slices were searched across **19 languages** and ~47 jurisdictions, but 5 searched languages (`ar`, `bn`, `hi`, `id`, `sw`) returned **zero** usable sources in **every** slice. The bias lives in what converted to evidence, not in search effort.

## 2. Method & definitions

**Slice = slug.** The 82 ACTIVE slugs are the unit of audit. Evidence is attributed through `source_slug_links`; each linked `evidence_sources` row is one *source-instance* (a source shared by two slices counts once in each). The 749 instances collapse to **651 unique sources** (reuse factor 1.15×; 68 sources span >1 slice, one — `REF-00050` — spans 6). Instance-weighting is deliberate — it measures per-slice coverage — but shared sources are re-counted, so corpus tier/language totals read ~15% above unique-source counts. (24 of the 675 rows in `evidence_sources` are linked to no active slug.)

**Tiers** follow `governance/tier-system.md` (OPERATIVE 2026-05-25). Tier number reflects *what kind of claim a source can anchor*, not raw quality:

| Tier | Character | Anchors |
|---|---|---|
| T1 / Co-1 | primary research / disability-led lived experience | best-practice claims |
| T2 / Co-2 | systematic review · meta-analysis · evidence-based standard / OT CPG | best-practice claims |
| T3 | lower-control clinical (●) + grey primary (○) | supporting |
| T4 | international standards (ISO/IEC/CEN) | code-baseline |
| T5 | national beyond-code frameworks (BS 8300, DIN 18040) | code-baseline |
| T6 | statutory code (ADA, AS 1428.1) | code-floor only |

**Best-practice-capable** instances = T1, Co-1, T2, Co-2, and T3-clinical. T4–T6 are code-baseline and, per §3 of the tier doctrine, *cannot* anchor best-practice claims on their own (the “convergence-is-not-evidence” rule).

**Anglophone classification** of a jurisdiction: *native-Anglophone* = US, UK, AU, CA, NZ, IE; *supranational/English-medium* = INT, EU, ISO, ASEAN; *English-official (non-native)* = SG, HK, IN, NG, GH, ZA, MY, AE, SA; everything else *non-Anglophone*. Language uses `lang_detected` (`en`/`eng`→English).

**Composite score (0–100)** = five transparent components, higher = stronger base:

| Comp | Max | Measures |
|---|---|---|
| A Volume | 20 | count of linked source-instances |
| B Tier strength | 30 | best-practice-capable share + presence of a T1/Co-1/T2/Co-2 anchor |
| C Jurisdictional breadth | 20 | distinct jurisdictions sourced |
| D Linguistic breadth | 15 | distinct languages; capped at 4 if English-only |
| E Anglophone balance | 15 | rewards distance from 100% English + 100% Anglo-core concentration |

Grades: **A**≥80 · **B**≥65 · **C**≥50 · **D**≥35 · **E**>0 · **F**=empty. The score rewards a *balanced, multi-jurisdiction, multi-language, synthesis-anchored* base and penalises thin or monolingual ones; it is a triage lens, not a verdict on any single citation.

**Convergence discount.** Per §3 of the tier doctrine, a slice with **zero** best-practice-capable sources is a *code-floor / convergence* base: breadth of T4–T6 sources across many jurisdictions is “convergence, not evidence.” Without a correction such a slice can out-score a genuinely well-evidenced but narrow one purely on breadth. The rubric therefore **halves the breadth components (C, D) for any slice with 0 best-practice-capable sources**, and every such slice is flagged *convergence-only* (‡) — its grade must be read as *code-floor coverage, not best-practice quality*.

## 3. Portfolio view, by dimension

### (1) Amount of evidence
| Linked sources | Slices |
|---|---|
| 0 (empty) | 13 |
| 1–3 | 2 |
| 4–7 | 26 |
| 8–14 | 28 |
| 15+ | 13 |

Median linked sources among non-empty slices: **8**. Largest bases: `accessibility-feature-market-value-uplift-framing` (33), `room-acoustic-performance` (32), `threshold-door-hardware` (32), `stair-ramp-threshold-biomechanics-accessibility` (26), `mental-health-built-environment` (25).

### (2) Tiers of evidence
| Tier | Instances | Share |
|---|---|---|
| T1 | 100 | ███················· 13% |
| T2 | 75 | ██·················· 10% |
| T3 | 218 | ██████·············· 29% |
| T4 | 76 | ██·················· 10% |
| T5 | 146 | ████················ 19% |
| T6 | 134 | ████················ 18% |

**Best-practice-capable share: 362/749 (48%).** The remaining 387 are T4–T6 code/standards instances that can only carry code-baseline claims. Slices whose base is *entirely* code-baseline are the sharpest risk (see the convergence-only list in §4).

### (3) Jurisdictions sourced
Distinct jurisdiction strings across the corpus: **49** — but **3 are language codes mis-filed in the jurisdiction column** (`DA`×1, `JA`×1, `ZH`×3 = 5 instances; a data-integrity defect, see the note below), leaving **~46 true jurisdictions**. Top: INT (181), US (126), UK (84), AU (38), DE (35), CA (28), NL (24), NO (22), JP (19), FR (17).

**3 non-empty slices draw on ≤1 jurisdiction** — monojurisdictional bases whose values may not transfer across code regimes. Separately, **18 source-instances carry no jurisdiction at all** (NULL) — mostly clinical/synthesis sources with no single national home; these are excluded from every jurisdiction-share denominator.

> **Data-integrity note (§3.3).** The audit *surfaces rather than propagates* the mis-filed language codes: language codes appearing as `jurisdiction` values are almost certainly the source language leaking into the wrong column. Recommend a data fix moving these to `lang_detected` and recovering the true jurisdiction.

### (4) Languages sourced
| Language | Instances |
|---|---|
| en | 553 |
| de | 35 |
| ja | 23 |
| fr | 21 |
| no | 20 |
| nl | 16 |
| sv | 15 |
| zh | 11 |
| pt | 11 |
| it | 10 |
| ko | 9 |
| fi | 8 |
| da | 7 |
| es | 6 |
| ar | 2 |
| bn | 1 |
| id | 1 |

Distinct source languages: **17** (`en`/`eng` merged; raw ISO codes may be one more). English dominates at 74%. The non-English corpus is overwhelmingly Western-European + East-Asian; the only languages outside that group to yield *any* linked source are: ar (2); bn (1); id (1).

**29 non-empty slices are English-only** (42% of evidenced slices).

### (5) English / Anglophone bias
- **Language axis:** 74% English. 29 slices 100% English.
- **Jurisdiction axis (all 749 instances):** native-Anglophone (US/UK/AU/CA/NZ/IE) **295** · supranational/English-medium (INT/EU/ISO) **192** · English-official + other non-Anglophone **244** · **no jurisdiction recorded 18**. (These four sum to 749 = all instances.)
- **14 slices are doubly-concentrated** (≥90% English *and* ≥50% native-Anglophone jurisdiction): `upper-limb-impairment-built-environment`, `accessibility-feature-market-value-uplift-framing`, `air-quality-voc-chemical-sensitivity-built-environment`, `sensory-relief-space-design`, `residential-accessible-home-case-studies`, `manoeuvring-footprint-vs-turning-radius-methodology`, `ot-cpg-built-environment`, `ot-frameworks-built-environment`, `sensory-processing-model-design-application`, `luminance-contrast-lrv-evidence-base`, `ofs-built-environment`, `cross-population-case-studies`, `case-study-economics-financial-data`, `residential-dar-provisions-priority-register`.
- **Process counter-evidence:** non-English/Global-South *searches were run* (19 languages across 81 of 82 slices in `search_languages`) but `ar`, `bn`, `hi`, `id`, `sw` yielded nothing linkable in any slice. The gap is a *yield/recovery* gap, not a *search-effort* gap.

### (6) Overall quality of the evidentiary base
| Grade | Slices | Meaning |
|---|---|---|
| A | 8 | strong, balanced, synthesis-anchored |
| B | 19 | solid, some concentration or tier gaps |
| C | 20 | usable but thin or monolingual |
| D | 13 | weak — few sources / single jurisdiction / English-only |
| E | 9 | very weak — 1 jurisdiction, no anchor |
| F | 13 | empty — no linked evidence |

## 4. Master per-slice table (ranked by composite score)

Legend: **N** linked sources · **BP** best-practice-capable · **JUR** distinct jurisdictions · **LNG** distinct languages · **%EN** English-language share · **%ANG** native-Anglophone-jurisdiction share · **A/B/C/D/E** score components · **‡** convergence-only (0 best-practice-capable sources; grade = code-floor coverage).

| # | Grade | Score | Slice | Topic | N | BP | Tiers | JUR | LNG | %EN | %ANG | A·B·C·D·E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **A** | 88.1 | `cognitive-wayfinding-design` | wayfinding-and-signage | 22 | 15 | T1×1,T2×4,T3×10,T5×7 | 11 | 7 | 63.6 | 9.1 | 20·23.6·20·15·9.5 |
| 2 | **A** | 86.8 | `sensory-room-user-control` | sensory-environment | 13 | 12 | T2×4,T3×8,T6×1 | 9 | 4 | 76.9 | 38.5 | 20·28.5·20·12·6.3 |
| 3 | **A** | 86.5 | `wayfinding-dementia-spatial-design` | wayfinding-and-signage | 22 | 12 | T1×1,T2×3,T3×9,T5×5,T6×4 | 16 | 13 | 40.9 | 18.2 | 20·20.9·20·15·10.6 |
| 4 | **A** | 84.9 | `deaf-spatial-design` | communication-and-alerts | 13 | 10 | T1×5,T2×3,T3×4,T5×1 | 8 | 5 | 61.5 | 38.5 | 20·25.4·20·12·7.5 |
| 5 | **A** | 84.4 | `mobility-built-environment` | population-general | 24 | 15 | T1×11,T2×2,T3×2,T5×4,T6×5 | 17 | 9 | 58.3 | 50.0 | 20·22.5·20·15·6.9 |
| 6 | **A** | 82.7 | `room-acoustic-performance` | sensory-environment | 32 | 20 | T1×16,T2×1,T3×4,T4×2,T5×8,T6×1 | 13 | 7 | 81.2 | 50.0 | 20·22.5·20·15·5.2 |
| 7 | **A** | 80.8 | `mental-health-built-environment` | population-general | 25 | 16 | T1×3,T2×2,T3×17,T4×1,T5×2 | 8 | 4 | 84.0 | 36.0 | 20·22.8·20·12·6.0 |
| 8 | **A** | 80.0 | `accessible-bathroom-and-grab-bar` | bathrooms-and-wet-areas | 19 | 9 | T1×5,T2×4,T3×1,T4×1,T5×4,T6×4 | 12 | 8 | 57.9 | 68.4 | 20·19.5·20·15·5.5 |
| 9 | **B** | 79.5 | `deaf-classroom-reverberation-time` | communication-and-alerts | 12 | 2 | T1×2,T4×1,T5×6,T6×3 | 9 | 9 | 25.0 | 25.0 | 20·13.3·20·15·11.2 |
| 10 | **B** | 78.2 | `residential-kitchen-and-task-surfaces` | kitchens-and-workspaces | 13 | 3 | T1×3,T4×2,T5×3,T6×5 | 10 | 8 | 38.5 | 46.2 | 20·14.6·20·15·8.6 |
| 11 | **B** | 77.3 | `wayfinding-global-south` | wayfinding-and-signage | 15 | 1 | T1×1,T4×4,T6×10 | 13 | 7 | 53.3 | 0.0 | 20·11.3·20·15·11.0 |
| 12 | **B** | 76.9 | `dementia-built-environment` | population-general | 8 | 5 | T1×1,T3×4,T5×3 | 5 | 4 | 62.5 | 12.5 | 16·22.5·17·12·9.4 |
| 13 | **B** | 75.7 | `accessible-design-economics-cost-premium` | economics | 11 | 9 | T1×1,T2×2,T3×6,T6×2 | 7 | 3 | 72.7 | 30.0 | 16·26.4·17·9·7.3 |
| 14 | **B** | 75.2 | `threshold-door-hardware` | entrances-and-circulation | 32 | 2 | T1×1,T3×1,T4×1,T5×9,T6×20 | 26 | 13 | 46.9 | 34.4 | 20·11.2·20·15·8.9 |
| 15 | **B** | 75.2 | `visual-impairment-built-environment` | population-general | 8 | 2 | T2×2,T4×2,T5×1,T6×3 | 7 | 6 | 25.0 | 12.5 | 16·15.0·17·15·12.2 |
| 16 | **B** | 75.0 | `residential-entry-and-threshold` | entrances-and-circulation | 20 | 4 | T1×1,T2×3,T4×1,T5×6,T6×9 | 13 | 7 | 65.0 | 55.0 | 20·14.0·20·15·6.0 |
| 17 | **B** | 74.5 | `stair-ramp-threshold-biomechanics-accessibility` | entrances-and-circulation | 26 | 13 | T3×14,T4×1,T5×1,T6×10 | 15 | 12 | 57.7 | 15.4 | 20·10.0·20·15·9.5 |
| 18 | **B** | 74.4 | `assistive-listening-systems` | communication-and-alerts | 8 | 4 | T2×4,T4×1,T5×1,T6×2 | 7 | 5 | 50.0 | 25.0 | 16·20.0·17·12·9.4 |
| 19 | **B** | 74.3 | `deafblind-built-environment-design` | population-general | 9 | 7 | T1×3,T2×4,T3×1,T6×1 | 5 | 3 | 66.7 | 44.4 | 16·25.6·17·9·6.7 |
| 20 | **B** | 72.2 | `construction-cost-data` | economics | 10 | 8 | T1×2,T2×4,T3×2,T6×2 | 8 | 2 | 80.0 | 50.0 | 16·26.0·20·5·5.2 |
| 21 | **B** | 70.9 | `upper-limb-impairment-built-environment` | population-general | 14 | 13 | T1×2,T3×12 | 3 | 2 | 92.9 | 50.0 | 20·28.6·13·5·4.3 |
| 22 | **B** | 69.6 | `neurological-built-environment` | population-general | 8 | 8 | T1×2,T3×6 | 5 | 1 | 100.0 | 12.5 | 16·30·17·0·6.6 |
| 23 | **B** | 69.3 | `school-environment-autism` | sensory-environment | 17 | 16 | T1×2,T2×2,T3×13 | 3 | 1 | 100.0 | 0.0 | 20·28.8·13·0·7.5 |
| 24 | **B** | 69.0 | `accessible-circulation-geometry` | entrances-and-circulation | 12 | 3 | T1×1,T2×1,T3×1,T4×1,T5×2,T6×6 | 7 | 4 | 75.0 | 58.3 | 20·15.0·17·12·5.0 |
| 25 | **B** | 68.6 | `pain-ofs-built-environment-design` | health-and-symptom-management | 12 | 5 | T1×2,T2×3,T3×3,T5×3,T6×1 | 6 | 3 | 83.3 | 60.0 | 20·18.3·17·9·4.3 |
| 26 | **B** | 67.4 | `accessibility-feature-market-value-uplift-framing` | economics | 33 | 10 | T1×2,T3×8,T4×4,T5×15,T6×4 | 11 | 3 | 90.9 | 78.8 | 20·16.1·20·9·2.3 |
| 27 | **B** | 67.4 | `sensory-space-global-south` | sensory-environment | 8 | 4 | T1×2,T2×1,T3×3,T5×1,T6×1 | 5 | 2 | 75.0 | 0.0 | 16·20.0·17·5·9.4 |
| 28 | **C** | 62.5 | `air-quality-voc-chemical-sensitivity-built-environment` | sensory-environment | 12 | 7 | T2×1,T3×6,T4×4,T5×1 | 7 | 1 | 100.0 | 50.0 | 20·21.7·17·0·3.8 |
| 29 | **C** | 60.8 | `thermal-comfort-older-adults-care-settings` | health-and-symptom-management | 6 | 4 | T2×1,T3×4,T5×1 | 4 | 2 | 83.3 | 16.7 | 12·23.3·13·5·7.5 |
| 30 | **C** | 60.7 | `deaf-acoustic-built-environment` | communication-and-alerts | 10 | 5 | T1×2,T2×3,T4×3,T5×2 | 4 | 2 | 90.0 | 20.0 | 16·20.0·13·5·6.7 |
| 31 | **C** | 60.5 | `sensory-relief-space-design` | sensory-environment | 10 | 8 | T1×1,T2×3,T3×4,T4×1,T6×1 | 6 | 1 | 100.0 | 80.0 | 16·26.0·17·0·1.5 |
| 32 | **C** | 60.1 | `residential-accessible-home-case-studies` | frameworks-and-methodology | 8 | 8 | T1×4,T2×2,T3×2 | 4 | 1 | 100.0 | 85.7 | 16·30·13·0·1.1 |
| 33 | **C** | 60.0 | `biophilic-design-healthcare-workplace` | sensory-environment | 6 | 6 | T1×1,T3×5 | 3 | 1 | 100.0 | 33.3 | 12·30·13·0·5.0 |
| 34 | **C** | 59.3 | `manoeuvring-footprint-vs-turning-radius-methodology` | frameworks-and-methodology | 8 | 7 | T1×5,T3×2,T4×1 | 3 | 1 | 100.0 | 62.5 | 16·27.5·13·0·2.8 |
| 35 | **C** | 59.0 | `ms-thermal-temperature-conflict-resolution` | health-and-symptom-management | 10 | 7 | T1×1,T3×6,T4×2,T5×1 | 4 | 1 | 100.0 | 20.0 | 16·24.0·13·0·6.0 |
| 36 | **C** | 58.1 | `acoustics-speech-intelligibility-disability` | sensory-environment | 8 | 5 | T1×1,T2×1,T3×3,T4×3 | 4 | 1 | 100.0 | 12.5 | 16·22.5·13·0·6.6 |
| 37 | **C** | 56.3 | `ot-cpg-built-environment` | population-general | 6 | 6 | T2×6 | 4 | 1 | 100.0 | 83.3 | 12·30·13·0·1.3 |
| 38 | **C** | 55.2 | `visitability-residential-accessibility-minimum-standards` | frameworks-and-methodology | 7 | 1 | T1×1,T5×1,T6×5 | 5 | 3 | 71.4 | 71.4 | 12·12.9·17·9·4.3 |
| 39 | **C** | 54.8 | `ot-frameworks-built-environment` | frameworks-and-methodology | 4 | 4 | T1×4 | 3 | 1 | 100.0 | 50.0 | 8·30·13·0·3.8 |
| 40 | **C** | 54.5 | `ndv-aut-built-environment-quantified-thresholds` | population-general | 6 | 4 | T2×2,T3×3,T4×1 | 3 | 1 | 100.0 | 16.7 | 12·23.3·13·0·6.2 |
| 41 | **C** | 53.3 | `detectable-gradient-protocol-sensory-zones` | wayfinding-and-signage | 6 | 4 | T1×1,T2×1,T3×2,T4×2 | 3 | 1 | 100.0 | 33.3 | 12·23.3·13·0·5.0 |
| 42 | **C** | 52.9 | `design-framework-evidence-audit` | frameworks-and-methodology | 9 | 4 | T2×1,T3×5,T4×2,T5×1 | 4 | 1 | 100.0 | 33.3 | 16·18.9·13·0·5.0 |
| 43 | **C** ‡ | 52.5 | `luminance-contrast-and-pattern` | wayfinding-and-signage | 13 | 0 | T5×4,T6×9 | 13 | 13 | 0.0 | 0.0 | 20·0.0·10.0·7.5·15.0 |
| 44 | **C** | 52.1 | `sensory-processing-model-design-application` | sensory-environment | 6 | 4 | T1×2,T2×1,T3×1,T4×1,T5×1 | 4 | 1 | 100.0 | 50.0 | 12·23.3·13·0·3.8 |
| 45 | **C** | 51.0 | `ot-built-environment-interface` | frameworks-and-methodology | 5 | 2 | T1×1,T3×4 | 3 | 2 | 80.0 | 80.0 | 12·18.0·13·5·3.0 |
| 46 | **C** | 50.7 | `circadian-lighting-melanopic-edi` | sensory-environment | 10 | 5 | T3×5,T4×2,T5×3 | 4 | 2 | 90.0 | 20.0 | 16·10.0·13·5·6.7 |
| 47 | **C** | 50.7 | `visual-fire-alarm-seizure-safety` | sensory-environment | 7 | 4 | T2×1,T3×3,T4×2,T6×1 | 3 | 1 | 100.0 | 42.9 | 12·21.4·13·0·4.3 |
| 48 | **D** | 49.3 | `luminance-contrast-lrv-evidence-base` | wayfinding-and-signage | 7 | 5 | T2×1,T3×4,T5×1,T6×1 | 4 | 1 | 100.0 | 100.0 | 12·24.3·13·0·0.0 |
| 49 | **D** | 47.5 | `ofs-built-environment` | health-and-symptom-management | 7 | 4 | T1×3,T3×1,T5×2,T6×1 | 3 | 1 | 100.0 | 85.7 | 12·21.4·13·0·1.1 |
| 50 | **D** | 47.0 | `cross-population-case-studies` | frameworks-and-methodology | 3 | 3 | T1×2,T3×1 | 2 | 1 | 100.0 | 100.0 | 8·30·9·0·0.0 |
| 51 | **D** | 47.0 | `ecological-psychology-haptic-affordances-built-environment` | frameworks-and-methodology | 5 | 5 | T3×5 | 2 | 1 | 100.0 | 20.0 | 12·20.0·9·0·6.0 |
| 52 | **D** | 46.5 | `reach-range-and-accessible-controls` | controls-and-hardware | 11 | 1 | T3×1,T5×5,T6×5 | 6 | 3 | 81.8 | 81.8 | 16·1.8·17·9·2.7 |
| 53 | **D** ‡ | 46.0 | `threshold-and-level-access` | entrances-and-circulation | 15 | 0 | T4×1,T5×4,T6×10 | 12 | 8 | 46.7 | 40.0 | 20·0.0·10.0·7.5·8.5 |
| 54 | **D** | 45.3 | `wayfinding-cognitive-science-spatial-design` | wayfinding-and-signage | 7 | 7 | T3×7 | 2 | 1 | 100.0 | 42.9 | 12·20.0·9·0·4.3 |
| 55 | **D** ‡ | 42.7 | `jurisdiction-grant-programmes-comprehensive` | frameworks-and-methodology | 9 | 0 | T5×9 | 9 | 6 | 44.4 | 33.3 | 16·0.0·10.0·7.5·9.2 |
| 56 | **D** | 42.0 | `case-study-economics-financial-data` | economics | 4 | 3 | T1×1,T2×1,T3×1,T5×1 | 2 | 1 | 100.0 | 100.0 | 8·25.0·9·0·0.0 |
| 57 | **D** | 39.6 | `residential-dar-provisions-priority-register` | frameworks-and-methodology | 6 | 1 | T2×1,T4×1,T5×4 | 3 | 1 | 100.0 | 83.3 | 12·13.3·13·0·1.3 |
| 58 | **D** | 38.8 | `floor-vibration-wheelchair-disability` | entrances-and-circulation | 7 | 4 | T3×4,T4×3 | 2 | 1 | 100.0 | 14.3 | 12·11.4·9·0·6.4 |
| 59 | **D** | 37.5 | `intellectual-disability-built-environment-design` | population-general | 5 | 2 | T3×2,T4×3 | 3 | 1 | 100.0 | 40.0 | 12·8.0·13·0·4.5 |
| 60 | **D** ‡ | 36.1 | `visual-alerting-and-wayfinding-light` | wayfinding-and-signage | 7 | 0 | T4×2,T5×2,T6×3 | 7 | 5 | 42.9 | 28.6 | 12·0.0·8.5·6.0·9.6 |
| 61 | **E** ‡ | 33.8 | `body-sizes-supplementary-populations` | frameworks-and-methodology | 11 | 0 | T3×2,T4×4,T5×5 | 5 | 2 | 72.7 | 36.4 | 16·0.0·8.5·2.5·6.8 |
| 62 | **E** | 32.7 | `cross-population-conflict-resolutions` | frameworks-and-methodology | 6 | 2 | T3×2,T4×3,T5×1 | 2 | 1 | 100.0 | 33.3 | 12·6.7·9·0·5.0 |
| 63 | **E** | 32.5 | `thermoregulation-built-environment` | health-and-symptom-management | 5 | 2 | T3×4,T4×1 | 1 | 1 | 100.0 | 0.0 | 12·8.0·5·0·7.5 |
| 64 | **E** ‡ | 31.7 | `european-accessibility-act-scope-clarification` | frameworks-and-methodology | 6 | 0 | T5×2,T6×4 | 4 | 3 | 66.7 | 16.7 | 12·0.0·6.5·4.5·8.7 |
| 65 | **E** ‡ | 28.0 | `accessible-laundry-room-design` | room-types | 6 | 0 | T4×3,T5×3 | 4 | 3 | 66.7 | 66.7 | 12·0.0·6.5·4.5·5.0 |
| 66 | **E** ‡ | 27.3 | `government-grant-programmes-home-adaptation` | economics | 7 | 0 | T5×7 | 6 | 2 | 71.4 | 71.4 | 12·0.0·8.5·2.5·4.3 |
| 67 | **E** ‡ | 26.4 | `therapeutic-lighting-design` | sensory-environment | 4 | 0 | T4×1,T5×3 | 3 | 2 | 75.0 | 0.0 | 8·0.0·6.5·2.5·9.4 |
| 68 | **E** ‡ | 22.0 | `crpd-implementation-built-environment` | frameworks-and-methodology | 5 | 0 | T4×5 | 1 | 1 | 100.0 | 0.0 | 12·0.0·2.5·0.0·7.5 |
| 69 | **E** ‡ | 18.0 | `co1-housing-research-global-south` | frameworks-and-methodology | 3 | 0 | T4×3 | 1 | 1 | 100.0 | 0.0 | 8·0.0·2.5·0.0·7.5 |
| 70 | **F** | 0 | `accessible-design-failures-poor-performance` | frameworks-and-methodology | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 71 | **F** | 0 | `bariatric-turning-radius-built-environment` | seating-and-rest | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 72 | **F** | 0 | `bathroom-typology-global-south` | bathrooms-and-wet-areas | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 73 | **F** | 0 | `chronic-pain-built-environment` | health-and-symptom-management | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 74 | **F** | 0 | `economics-sources` | economics | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 75 | **F** | 0 | `fatigue-spectrum-built-environment` | health-and-symptom-management | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 76 | **F** | 0 | `fold-down-grab-bar-specification` | bathrooms-and-wet-areas | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 77 | **F** | 0 | `government-grant-programmes` | economics | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 78 | **F** | 0 | `hearing-impairment-built-environment` | population-general | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 79 | **F** | 0 | `jurisdiction-matrix-accessibility-standards` | frameworks-and-methodology | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 80 | **F** | 0 | `multilingual-evidence-convergence-non-english` | frameworks-and-methodology | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 81 | **F** | 0 | `neurodivergent-built-environment` | population-general | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 82 | **F** | 0 | `post-occupancy-evaluation-global` | frameworks-and-methodology | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |

**Convergence-only slices (11) ‡** — real sources but **zero best-practice-capable** evidence; the base can cite a regulatory floor but cannot anchor a best-practice claim. Read their grades as coverage, not quality: `luminance-contrast-and-pattern`, `threshold-and-level-access`, `jurisdiction-grant-programmes-comprehensive`, `visual-alerting-and-wayfinding-light`, `body-sizes-supplementary-populations`, `european-accessibility-act-scope-clarification`, `accessible-laundry-room-design`, `government-grant-programmes-home-adaptation`, `therapeutic-lighting-design`, `crpd-implementation-built-environment`, `co1-housing-research-global-south`.

## 5. Evidence-empty slices (13)

These carry **zero** linked source-instances. `bpc_metadata.evidence_state` distinguishes:

**Retracted pending rehabilitation (6)** — prior work cleared, awaiting re-derivation:
- `bariatric-turning-radius-built-environment` (seating-and-rest)
- `bathroom-typology-global-south` (bathrooms-and-wet-areas)
- `fold-down-grab-bar-specification` (bathrooms-and-wet-areas)
- `jurisdiction-matrix-accessibility-standards` (frameworks-and-methodology)
- `multilingual-evidence-convergence-non-english` (frameworks-and-methodology)
- `neurodivergent-built-environment` (population-general)

**Un-started / placeholder (7)** — `evidence_state` unset, search not run:
- `accessible-design-failures-poor-performance` (frameworks-and-methodology)
- `chronic-pain-built-environment` (health-and-symptom-management)
- `economics-sources` (economics)
- `fatigue-spectrum-built-environment` (health-and-symptom-management)
- `government-grant-programmes` (economics)
- `hearing-impairment-built-environment` (population-general)
- `post-occupancy-evaluation-global` (frameworks-and-methodology)

Several name high-salience topics where an empty base is a material coverage gap, not bookkeeping.

## 6. Findings & recommended remediation

1. **Thicken the synthesis tier (T2).** With only 75 systematic-review/evidence-based-standard instances corpus-wide, most best-practice claims lean on individual primary studies (T1/T3) or on code convergence (T4–T6, disallowed as best-practice warrant). Prioritise SR/meta-analysis recovery on the 11 slices with **zero** best-practice-capable sources.
2. **Convert non-English search into non-English evidence.** Searches ran in 19 languages but the corpus is ~74% English. Target the languages already searched-with-results but under-linked, and the zero-yield languages (`ar`, `bn`, `hi`, `id`, `sw`) explicitly.
3. **De-risk monojurisdictional slices.** 3 evidenced slices rest on ≤1 jurisdiction; flag their numeric thresholds as non-transferable until a second regime is sourced.
4. **Fill or formally park the empty slices.** Move the 7 un-started slices into an active search queue or an explicit deferred state so they stop reading as silent gaps.
5. **Treat the doubly-concentrated slices as citation-risk.** The 14 ≥90%-English-and-≥50%-Anglophone slices are where global-applicability claims are weakest.
6. **Fix the mis-filed jurisdiction codes.** Move the 5 `DA`×1, `JA`×1, `ZH`×3 values out of `evidence_sources.jurisdiction` and recover the true jurisdiction — a one-off migration.

## 7. Limitations & what this audit does *not* claim

- **Instance-weighted, not source-weighted.** The 749 instances are 651 unique sources, so corpus tier/language totals run ~15% above unique-source counts. Per-slice figures are unaffected.
- **The composite is a lens, not ground truth.** Weights (20/30/20/15/15) are a defensible but editorial choice; the six raw dimensions are printed alongside every grade so a reader can re-weight. No grade is stored in the DB — it is recomputed each run.
- **Coverage ≠ correctness.** The audit measures the *shape* of each base (how much, what tier, where from, what language, how concentrated). It does **not** re-verify that any citation resolves, is current, or supports its claim — those are the `url_verification_runs` / `code_currency` / supersession checks, run separately.
- **Jurisdiction shares rest on recorded jurisdictions only.** NULL-jurisdiction instances are excluded from %ANG denominators, so a low %ANG can mean *genuinely non-Anglophone* or *unrecorded* — the master table’s JUR count exposes the denominator.
- **Compound jurisdictions classify by their strongest Anglophone member** (e.g. `US/AU/INT` counts as native-Anglophone). Magnitude ≈1% of instances.

---
*Data as of 2026-07-19 · read-only over `data/guidebook.db` · generated by `tools/evidentiary_audit.py`. Independently red-teamed; raw counts reproduce through a second code path. Aligned to `governance/tier-system.md`.*
