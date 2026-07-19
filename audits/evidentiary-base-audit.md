# Per-Slice Evidentiary Audit
**Data as of:** 2026-07-19 · **Scope:** all 82 ACTIVE research slices (slugs) in `data/guidebook.db` · **Method:** read-only aggregation over `source_slug_links → evidence_sources`, `search_languages`, `search_coverage`, `bpc_metadata`.

This audit scores every research slice on the six requested dimensions — (1) amount of evidence, (2) tiers of evidence, (3) jurisdictions sourced, (4) languages sourced, (5) English/Anglophone bias, and (6) overall quality of the evidentiary base — and rolls them into a transparent 0–100 composite grade. It audits the **raw evidence linked to each slice**, i.e. the material available for (re-)derivation; it does not re-judge synthesis prose.

> **Reproducibility.** Every number here is regenerated from the DB by `tools/evidentiary_audit.py` — nothing is hand-transcribed, and the “data as of” date is the DB’s own `max(updated_at)`, so identical data yields byte-identical output. No grade is stored in the DB; the composite is a *derived* view whose rubric is fully specified in §2, so any reader can recompute it. Companion outputs: `evidentiary-base-audit.json` / `.csv`, and the interactive `tools/evidentiary-audit-dashboard.html` (filter by corpus / category / term).

> **Adversarial review (two passes).** The audit was independently red-teamed twice; all raw counts (volume, tiers, language/jurisdiction distributions, search yield) reproduce exactly through a second code path. Folded in: (i) the **best-practice split** — *anchor* (T1/Co-1/T2/Co-2, the only tiers §3 lets anchor a best-practice claim) is now separated from *confirmed* (adds T3-clinical, ● per §5); a T3-clinical-only slice is confirmed evidence but flagged **no-anchor** (§2, §4); (ii) a **convergence discount** so code-floor-only slices can’t score highly on breadth alone (§2, §6); (iii) full disclosure of the **18 NULL-jurisdiction instances** (§3.5); (iv) **true-jurisdiction** breadth scoring that excludes the 4 language codes (`DA`×1, `ZH`×3) mis-filed in the `jurisdiction` column (§3.3).

## 1. Executive summary

- **753 source-instances** are linked across **69 of 82 slices**; **13 slices carry zero linked evidence**.
- **Grade distribution:** A=6 · B=17 · C=19 · D=15 · E=12 · F=13  (A≥80, B≥65, C≥50, D≥35, E>0, F=empty).
- **Tier profile is code-and-clinical heavy, synthesis-light.** Of linked instances: T1=100, T2=76, T3=218, T4=76, T5=147, T6=136. Only **76 Tier-2 (systematic-review / evidence-based-standard) instances** exist across the whole corpus — the synthesis tier that best anchors best-practice claims is the thinnest.
- **Best-practice anchoring is thin.** Only **176/753 (23%)** of instances can *anchor* a best-practice claim (T1/Co-1/T2/Co-2, §3); a further 187 are confirmed-but-supporting T3-clinical (● §5). **20 slices have no anchor at all** (11 code-floor, 9 T3-clinical-only).
- **Anglophone concentration is the dominant quality risk.** **553/753 (73%) of linked sources are English-language**; only 200 are non-English. By jurisdiction, 295 instances are native-Anglophone (US/UK/AU/CA/NZ/IE), 192 supranational (INT/EU/ISO), 248 other, 18 unrecorded.
- **Search breadth ≠ evidentiary yield.** Slices were searched across **19 languages** and ~47 jurisdictions, but 5 searched languages (`ar`, `bn`, `hi`, `id`, `sw`) returned **zero** usable sources in **every** slice. The bias lives in what converted to evidence, not in search effort.

## 2. Method & definitions

**Slice = slug.** The 82 ACTIVE slugs are the unit of audit. Evidence is attributed through `source_slug_links`; each linked `evidence_sources` row is one *source-instance* (a source shared by two slices counts once in each). The 753 instances collapse to **651 unique sources** (reuse factor 1.16×; 70 sources span >1 slice, one — `REF-00050` — spans 6). Instance-weighting is deliberate — it measures per-slice coverage — but shared sources are re-counted, so corpus tier/language totals read ~16% above unique-source counts. (24 of the 675 rows in `evidence_sources` are linked to no active slug.)

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
| T2 | 76 | ██·················· 10% |
| T3 | 218 | ██████·············· 29% |
| T4 | 76 | ██·················· 10% |
| T5 | 147 | ████················ 20% |
| T6 | 136 | ████················ 18% |

**Best-practice-anchor share: 176/753 (23%)** (T1/Co-1/T2/Co-2, §3). Adding confirmed-but-supporting T3-clinical brings *confirmed* evidence to 363/753 (48%). The remaining 390 are T4–T6 code/standards + T3-grey that carry no confirmed evidence. Slices with zero anchors are the sharpest risk — see the no-anchor list in §4.

### (3) Jurisdictions sourced
Distinct jurisdiction strings across the corpus: **48** — but **2 are language codes mis-filed in the jurisdiction column** (`DA`×1, `ZH`×3 = 4 instances; a data-integrity defect, see the note below), leaving **~46 true jurisdictions**. Top: INT (181), US (126), UK (84), AU (38), DE (35), CA (28), NL (25), NO (22), JP (21), SE (18).

**3 non-empty slices draw on ≤1 jurisdiction** — monojurisdictional bases whose values may not transfer across code regimes. Separately, **18 source-instances carry no jurisdiction at all** (NULL) — mostly clinical/synthesis sources with no single national home; these are excluded from every jurisdiction-share denominator.

> **Data-integrity note (§3.3).** The audit *surfaces rather than propagates* the mis-filed language codes: language codes appearing as `jurisdiction` values are almost certainly the source language leaking into the wrong column. Recommend a data fix moving these to `lang_detected` and recovering the true jurisdiction.

### (4) Languages sourced
| Language | Instances |
|---|---|
| en | 553 |
| de | 35 |
| ja | 21 |
| fr | 21 |
| no | 20 |
| nl | 17 |
| sv | 16 |
| zh | 14 |
| pt | 11 |
| it | 10 |
| ko | 9 |
| fi | 8 |
| da | 8 |
| es | 6 |
| ar | 2 |
| bn | 1 |
| id | 1 |

Distinct source languages: **17** (`en`/`eng` merged; raw ISO codes may be one more). English dominates at 73%. The non-English corpus is overwhelmingly Western-European + East-Asian; the only languages outside that group to yield *any* linked source are: ar (2); bn (1); id (1).

**29 non-empty slices are English-only** (42% of evidenced slices).

### (5) English / Anglophone bias
- **Language axis:** 73% English. 29 slices 100% English.
- **Jurisdiction axis (all 753 instances):** native-Anglophone (US/UK/AU/CA/NZ/IE) **295** · supranational/English-medium (INT/EU/ISO) **192** · English-official + other non-Anglophone **248** · **no jurisdiction recorded 18**. (These four sum to 753 = all instances.)
- **14 slices are doubly-concentrated** (≥90% English *and* ≥50% native-Anglophone jurisdiction): `accessibility-feature-market-value-uplift-framing`, `upper-limb-impairment-built-environment`, `residential-accessible-home-case-studies`, `air-quality-voc-chemical-sensitivity-built-environment`, `manoeuvring-footprint-vs-turning-radius-methodology`, `ot-cpg-built-environment`, `sensory-relief-space-design`, `ot-frameworks-built-environment`, `sensory-processing-model-design-application`, `ofs-built-environment`, `cross-population-case-studies`, `luminance-contrast-lrv-evidence-base`, `residential-dar-provisions-priority-register`, `case-study-economics-financial-data`.
- **Process counter-evidence:** non-English/Global-South *searches were run* (19 languages across 81 of 82 slices in `search_languages`) but `ar`, `bn`, `hi`, `id`, `sw` yielded nothing linkable in any slice. The gap is a *yield/recovery* gap, not a *search-effort* gap.

### (6) Overall quality of the evidentiary base
| Grade | Slices | Meaning |
|---|---|---|
| A | 6 | strong, balanced, synthesis-anchored |
| B | 17 | solid, some concentration or tier gaps |
| C | 19 | usable but thin or monolingual |
| D | 15 | weak — few sources / single jurisdiction / English-only |
| E | 12 | very weak — 1 jurisdiction, no anchor |
| F | 13 | empty — no linked evidence |

## 4. Master per-slice table (ranked by composite score)

Legend: **N** linked sources · **BP** best-practice-anchor count (T1/Co-1/T2/Co-2) · **CF** confirmed (incl T3-clinical) · **JUR** distinct *true* jurisdictions · **LNG** distinct languages · **%EN** English-language share · **%ANG** native-Anglophone share · **A/B/C/D/E** score components · **‡** convergence-only (code-floor, breadth discounted) · **†** no-anchor supporting-only (confirmed T3-clinical but nothing to anchor best practice).

| # | Grade | Score | Slice | Topic | N | BP | CF | Tiers | JUR | LNG | %EN | %ANG | A·B·C·D·E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **A** | 83.4 | `mobility-built-environment` | population-general | 24 | 13 | 15 | T1×11,T2×2,T3×2,T5×4,T6×5 | 17 | 9 | 58.3 | 50.0 | 20·21.5·20·15·6.9 |
| 2 | **A** | 83.3 | `cognitive-wayfinding-design` | wayfinding-and-signage | 24 | 6 | 16 | T1×1,T2×5,T3×10,T5×7,T6×1 | 13 | 9 | 58.3 | 8.3 | 20·18.3·20·15·10.0 |
| 3 | **A** | 83.0 | `deaf-spatial-design` | communication-and-alerts | 13 | 8 | 10 | T1×5,T2×3,T3×4,T5×1 | 8 | 5 | 61.5 | 38.5 | 20·23.5·20·12·7.5 |
| 4 | **A** | 82.1 | `wayfinding-dementia-spatial-design` | wayfinding-and-signage | 22 | 4 | 12 | T1×1,T2×3,T3×9,T5×5,T6×4 | 16 | 13 | 40.9 | 18.2 | 20·16.5·20·15·10.6 |
| 5 | **A** | 81.6 | `room-acoustic-performance` | sensory-environment | 32 | 17 | 20 | T1×16,T2×1,T3×4,T4×2,T5×8,T6×1 | 12 | 7 | 81.2 | 50.0 | 20·21.4·20·15·5.2 |
| 6 | **A** | 80.0 | `accessible-bathroom-and-grab-bar` | bathrooms-and-wet-areas | 19 | 9 | 9 | T1×5,T2×4,T3×1,T4×1,T5×4,T6×4 | 12 | 8 | 57.9 | 68.4 | 20·19.5·20·15·5.5 |
| 7 | **B** | 79.5 | `deaf-classroom-reverberation-time` | communication-and-alerts | 12 | 2 | 2 | T1×2,T4×1,T5×6,T6×3 | 9 | 9 | 25.0 | 25.0 | 20·13.3·20·15·11.2 |
| 8 | **B** | 79.4 | `sensory-room-user-control` | sensory-environment | 13 | 4 | 12 | T2×4,T3×8,T6×1 | 9 | 4 | 76.9 | 38.5 | 20·21.1·20·12·6.3 |
| 9 | **B** | 78.2 | `residential-kitchen-and-task-surfaces` | kitchens-and-workspaces | 13 | 3 | 3 | T1×3,T4×2,T5×3,T6×5 | 10 | 8 | 38.5 | 46.2 | 20·14.6·20·15·8.6 |
| 10 | **B** | 77.3 | `wayfinding-global-south` | wayfinding-and-signage | 15 | 1 | 1 | T1×1,T4×4,T6×10 | 13 | 7 | 53.3 | 0.0 | 20·11.3·20·15·11.0 |
| 11 | **B** | 75.5 | `mental-health-built-environment` | population-general | 25 | 5 | 16 | T1×3,T2×2,T3×17,T4×1,T5×2 | 8 | 4 | 84.0 | 36.0 | 20·17.5·20·12·6.0 |
| 12 | **B** | 75.2 | `visual-impairment-built-environment` | population-general | 8 | 2 | 2 | T2×2,T4×2,T5×1,T6×3 | 7 | 6 | 25.0 | 12.5 | 16·15.0·17·15·12.2 |
| 13 | **B** | 75.0 | `residential-entry-and-threshold` | entrances-and-circulation | 20 | 4 | 4 | T1×1,T2×3,T4×1,T5×6,T6×9 | 13 | 7 | 65.0 | 55.0 | 20·14.0·20·15·6.0 |
| 14 | **B** | 74.8 | `accessible-circulation-geometry` | entrances-and-circulation | 14 | 2 | 3 | T1×1,T2×1,T3×1,T4×1,T5×3,T6×7 | 9 | 6 | 64.3 | 50.0 | 20·13.4·20·15·6.4 |
| 15 | **B** | 74.8 | `threshold-door-hardware` | entrances-and-circulation | 32 | 1 | 2 | T1×1,T3×1,T4×1,T5×9,T6×20 | 26 | 13 | 46.9 | 34.4 | 20·10.9·20·15·8.9 |
| 16 | **B** | 74.4 | `assistive-listening-systems` | communication-and-alerts | 8 | 4 | 4 | T2×4,T4×1,T5×1,T6×2 | 7 | 5 | 50.0 | 25.0 | 16·20.0·17·12·9.4 |
| 17 | **B** | 74.3 | `deafblind-built-environment-design` | population-general | 9 | 7 | 7 | T1×3,T2×4,T3×1,T6×1 | 5 | 3 | 66.7 | 44.4 | 16·25.6·17·9·6.7 |
| 18 | **B** | 70.9 | `dementia-built-environment` | population-general | 8 | 1 | 5 | T1×1,T3×4,T5×3 | 5 | 4 | 62.5 | 12.5 | 16·16.5·17·12·9.4 |
| 19 | **B** | 69.8 | `construction-cost-data` | economics | 10 | 6 | 8 | T1×2,T2×4,T3×2,T6×2 | 8 | 2 | 80.0 | 50.0 | 16·23.6·20·5·5.2 |
| 20 | **B** | 69.1 | `accessible-design-economics-cost-premium` | economics | 11 | 3 | 9 | T1×1,T2×2,T3×6,T6×2 | 7 | 3 | 72.7 | 30.0 | 16·19.8·17·9·7.3 |
| 21 | **B** | 68.6 | `pain-ofs-built-environment-design` | health-and-symptom-management | 12 | 5 | 5 | T1×2,T2×3,T3×3,T5×3,T6×1 | 6 | 3 | 83.3 | 60.0 | 20·18.3·17·9·4.3 |
| 22 | **B** † | 68.5 | `stair-ramp-threshold-biomechanics-accessibility` | entrances-and-circulation | 26 | 0 | 13 | T3×14,T4×1,T5×1,T6×10 | 15 | 12 | 57.7 | 15.4 | 20·4.0·20·15·9.5 |
| 23 | **B** | 65.9 | `sensory-space-global-south` | sensory-environment | 8 | 3 | 4 | T1×2,T2×1,T3×3,T5×1,T6×1 | 5 | 2 | 75.0 | 0.0 | 16·18.5·17·5·9.4 |
| 24 | **C** | 64.5 | `accessibility-feature-market-value-uplift-framing` | economics | 33 | 2 | 10 | T1×2,T3×8,T4×4,T5×15,T6×4 | 11 | 3 | 90.9 | 78.8 | 20·13.2·20·9·2.3 |
| 25 | **C** | 61.4 | `upper-limb-impairment-built-environment` | population-general | 14 | 2 | 13 | T1×2,T3×12 | 3 | 2 | 92.9 | 50.0 | 20·19.1·13·5·4.3 |
| 26 | **C** | 60.9 | `school-environment-autism` | sensory-environment | 17 | 4 | 16 | T1×2,T2×2,T3×13 | 3 | 1 | 100.0 | 0.0 | 20·20.4·13·0·7.5 |
| 27 | **C** | 60.7 | `deaf-acoustic-built-environment` | communication-and-alerts | 10 | 5 | 5 | T1×2,T2×3,T4×3,T5×2 | 4 | 2 | 90.0 | 20.0 | 16·20.0·13·5·6.7 |
| 28 | **C** | 60.6 | `neurological-built-environment` | population-general | 8 | 2 | 8 | T1×2,T3×6 | 5 | 1 | 100.0 | 12.5 | 16·21.0·17·0·6.6 |
| 29 | **C** | 57.1 | `residential-accessible-home-case-studies` | frameworks-and-methodology | 8 | 6 | 8 | T1×4,T2×2,T3×2 | 4 | 1 | 100.0 | 85.7 | 16·27.0·13·0·1.1 |
| 30 | **C** | 56.5 | `air-quality-voc-chemical-sensitivity-built-environment` | sensory-environment | 12 | 1 | 7 | T2×1,T3×6,T4×4,T5×1 | 7 | 1 | 100.0 | 50.0 | 20·15.7·17·0·3.8 |
| 31 | **C** | 56.3 | `manoeuvring-footprint-vs-turning-radius-methodology` | frameworks-and-methodology | 8 | 5 | 7 | T1×5,T3×2,T4×1 | 3 | 1 | 100.0 | 62.5 | 16·24.5·13·0·2.8 |
| 32 | **C** | 56.3 | `ot-cpg-built-environment` | population-general | 6 | 6 | 6 | T2×6 | 4 | 1 | 100.0 | 83.3 | 12·30·13·0·1.3 |
| 33 | **C** | 55.7 | `sensory-relief-space-design` | sensory-environment | 10 | 4 | 8 | T1×1,T2×3,T3×4,T4×1,T6×1 | 6 | 1 | 100.0 | 80.0 | 16·21.2·17·0·1.5 |
| 34 | **C** | 55.2 | `visitability-residential-accessibility-minimum-standards` | frameworks-and-methodology | 7 | 1 | 1 | T1×1,T5×1,T6×5 | 5 | 3 | 71.4 | 71.4 | 12·12.9·17·9·4.3 |
| 35 | **C** | 54.8 | `ot-frameworks-built-environment` | frameworks-and-methodology | 4 | 4 | 4 | T1×4 | 3 | 1 | 100.0 | 50.0 | 8·30·13·0·3.8 |
| 36 | **C** | 54.8 | `thermal-comfort-older-adults-care-settings` | health-and-symptom-management | 6 | 1 | 4 | T2×1,T3×4,T5×1 | 4 | 2 | 83.3 | 16.7 | 12·17.3·13·5·7.5 |
| 37 | **C** | 53.6 | `acoustics-speech-intelligibility-disability` | sensory-environment | 8 | 2 | 5 | T1×1,T2×1,T3×3,T4×3 | 4 | 1 | 100.0 | 12.5 | 16·18.0·13·0·6.6 |
| 38 | **C** ‡ | 52.5 | `luminance-contrast-and-pattern` | wayfinding-and-signage | 13 | 0 | 0 | T5×4,T6×9 | 13 | 13 | 0.0 | 0.0 | 20·0.0·10.0·7.5·15.0 |
| 39 | **C** | 51.8 | `ms-thermal-temperature-conflict-resolution` | health-and-symptom-management | 10 | 1 | 7 | T1×1,T3×6,T4×2,T5×1 | 4 | 1 | 100.0 | 20.0 | 16·16.8·13·0·6.0 |
| 40 | **C** | 50.5 | `ndv-aut-built-environment-quantified-thresholds` | population-general | 6 | 2 | 4 | T2×2,T3×3,T4×1 | 3 | 1 | 100.0 | 16.7 | 12·19.3·13·0·6.2 |
| 41 | **C** | 50.1 | `sensory-processing-model-design-application` | sensory-environment | 6 | 3 | 4 | T1×2,T2×1,T3×1,T4×1,T5×1 | 4 | 1 | 100.0 | 50.0 | 12·21.3·13·0·3.8 |
| 42 | **C** | 50.0 | `biophilic-design-healthcare-workplace` | sensory-environment | 6 | 1 | 6 | T1×1,T3×5 | 3 | 1 | 100.0 | 33.3 | 12·20.0·13·0·5.0 |
| 43 | **D** | 49.3 | `detectable-gradient-protocol-sensory-zones` | wayfinding-and-signage | 6 | 2 | 4 | T1×1,T2×1,T3×2,T4×2 | 3 | 1 | 100.0 | 33.3 | 12·19.3·13·0·5.0 |
| 44 | **D** | 48.9 | `design-framework-evidence-audit` | frameworks-and-methodology | 9 | 1 | 4 | T2×1,T3×5,T4×2,T5×1 | 4 | 1 | 100.0 | 33.3 | 16·14.9·13·0·5.0 |
| 45 | **D** | 48.6 | `ot-built-environment-interface` | frameworks-and-methodology | 5 | 1 | 2 | T1×1,T3×4 | 3 | 2 | 80.0 | 80.0 | 12·15.6·13·5·3.0 |
| 46 | **D** ‡ | 46.0 | `threshold-and-level-access` | entrances-and-circulation | 15 | 0 | 0 | T4×1,T5×4,T6×10 | 12 | 8 | 46.7 | 40.0 | 20·0.0·10.0·7.5·8.5 |
| 47 | **D** | 45.8 | `ofs-built-environment` | health-and-symptom-management | 7 | 3 | 4 | T1×3,T3×1,T5×2,T6×1 | 3 | 1 | 100.0 | 85.7 | 12·19.7·13·0·1.1 |
| 48 | **D** | 45.6 | `visual-fire-alarm-seizure-safety` | sensory-environment | 7 | 1 | 4 | T2×1,T3×3,T4×2,T6×1 | 3 | 1 | 100.0 | 42.9 | 12·16.3·13·0·4.3 |
| 49 | **D** † | 45.4 | `reach-range-and-accessible-controls` | controls-and-hardware | 11 | 0 | 1 | T3×1,T5×5,T6×5 | 6 | 3 | 81.8 | 81.8 | 16·0.7·17·9·2.7 |
| 50 | **D** † | 44.7 | `circadian-lighting-melanopic-edi` | sensory-environment | 10 | 0 | 5 | T3×5,T4×2,T5×3 | 4 | 2 | 90.0 | 20.0 | 16·4.0·13·5·6.7 |
| 51 | **D** | 43.0 | `cross-population-case-studies` | frameworks-and-methodology | 3 | 2 | 3 | T1×2,T3×1 | 2 | 1 | 100.0 | 100.0 | 8·26.0·9·0·0.0 |
| 52 | **D** ‡ | 42.7 | `jurisdiction-grant-programmes-comprehensive` | frameworks-and-methodology | 9 | 0 | 0 | T5×9 | 9 | 6 | 44.4 | 33.3 | 16·0.0·10.0·7.5·9.2 |
| 53 | **D** | 42.4 | `luminance-contrast-lrv-evidence-base` | wayfinding-and-signage | 7 | 1 | 5 | T2×1,T3×4,T5×1,T6×1 | 4 | 1 | 100.0 | 100.0 | 12·17.4·13·0·0.0 |
| 54 | **D** | 39.6 | `residential-dar-provisions-priority-register` | frameworks-and-methodology | 6 | 1 | 1 | T2×1,T4×1,T5×4 | 3 | 1 | 100.0 | 83.3 | 12·13.3·13·0·1.3 |
| 55 | **D** | 39.0 | `case-study-economics-financial-data` | economics | 4 | 2 | 3 | T1×1,T2×1,T3×1,T5×1 | 2 | 1 | 100.0 | 100.0 | 8·22.0·9·0·0.0 |
| 56 | **D** ‡ | 36.1 | `visual-alerting-and-wayfinding-light` | wayfinding-and-signage | 7 | 0 | 0 | T4×2,T5×2,T6×3 | 7 | 5 | 42.9 | 28.6 | 12·0.0·8.5·6.0·9.6 |
| 57 | **D** † | 35.0 | `ecological-psychology-haptic-affordances-built-environment` | frameworks-and-methodology | 5 | 0 | 5 | T3×5 | 2 | 1 | 100.0 | 20.0 | 12·8.0·9·0·6.0 |
| 58 | **E** ‡ | 33.8 | `body-sizes-supplementary-populations` | frameworks-and-methodology | 11 | 0 | 0 | T3×2,T4×4,T5×5 | 4 | 3 | 72.7 | 36.4 | 16·0.0·6.5·4.5·6.8 |
| 59 | **E** † | 33.3 | `wayfinding-cognitive-science-spatial-design` | wayfinding-and-signage | 7 | 0 | 7 | T3×7 | 2 | 1 | 100.0 | 42.9 | 12·8.0·9·0·4.3 |
| 60 | **E** † | 32.7 | `intellectual-disability-built-environment-design` | population-general | 5 | 0 | 2 | T3×2,T4×3 | 3 | 1 | 100.0 | 40.0 | 12·3.2·13·0·4.5 |
| 61 | **E** † | 32.0 | `floor-vibration-wheelchair-disability` | entrances-and-circulation | 7 | 0 | 4 | T3×4,T4×3 | 2 | 1 | 100.0 | 14.3 | 12·4.6·9·0·6.4 |
| 62 | **E** ‡ | 31.7 | `european-accessibility-act-scope-clarification` | frameworks-and-methodology | 6 | 0 | 0 | T5×2,T6×4 | 4 | 3 | 66.7 | 16.7 | 12·0.0·6.5·4.5·8.7 |
| 63 | **E** † | 28.7 | `cross-population-conflict-resolutions` | frameworks-and-methodology | 6 | 0 | 2 | T3×2,T4×3,T5×1 | 2 | 1 | 100.0 | 33.3 | 12·2.7·9·0·5.0 |
| 64 | **E** ‡ | 28.0 | `accessible-laundry-room-design` | room-types | 6 | 0 | 0 | T4×3,T5×3 | 4 | 3 | 66.7 | 66.7 | 12·0.0·6.5·4.5·5.0 |
| 65 | **E** † | 27.7 | `thermoregulation-built-environment` | health-and-symptom-management | 5 | 0 | 2 | T3×4,T4×1 | 1 | 1 | 100.0 | 0.0 | 12·3.2·5·0·7.5 |
| 66 | **E** ‡ | 27.3 | `government-grant-programmes-home-adaptation` | economics | 7 | 0 | 0 | T5×7 | 6 | 2 | 71.4 | 71.4 | 12·0.0·8.5·2.5·4.3 |
| 67 | **E** ‡ | 26.4 | `therapeutic-lighting-design` | sensory-environment | 4 | 0 | 0 | T4×1,T5×3 | 3 | 2 | 75.0 | 0.0 | 8·0.0·6.5·2.5·9.4 |
| 68 | **E** ‡ | 22.0 | `crpd-implementation-built-environment` | frameworks-and-methodology | 5 | 0 | 0 | T4×5 | 1 | 1 | 100.0 | 0.0 | 12·0.0·2.5·0.0·7.5 |
| 69 | **E** ‡ | 18.0 | `co1-housing-research-global-south` | frameworks-and-methodology | 3 | 0 | 0 | T4×3 | 1 | 1 | 100.0 | 0.0 | 8·0.0·2.5·0.0·7.5 |
| 70 | **F** | 0 | `accessible-design-failures-poor-performance` | frameworks-and-methodology | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 71 | **F** | 0 | `bariatric-turning-radius-built-environment` | seating-and-rest | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 72 | **F** | 0 | `bathroom-typology-global-south` | bathrooms-and-wet-areas | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 73 | **F** | 0 | `chronic-pain-built-environment` | health-and-symptom-management | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 74 | **F** | 0 | `economics-sources` | economics | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 75 | **F** | 0 | `fatigue-spectrum-built-environment` | health-and-symptom-management | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 76 | **F** | 0 | `fold-down-grab-bar-specification` | bathrooms-and-wet-areas | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 77 | **F** | 0 | `government-grant-programmes` | economics | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 78 | **F** | 0 | `hearing-impairment-built-environment` | population-general | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 79 | **F** | 0 | `jurisdiction-matrix-accessibility-standards` | frameworks-and-methodology | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 80 | **F** | 0 | `multilingual-evidence-convergence-non-english` | frameworks-and-methodology | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 81 | **F** | 0 | `neurodivergent-built-environment` | population-general | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |
| 82 | **F** | 0 | `post-occupancy-evaluation-global` | frameworks-and-methodology | 0 | 0 | 0 | — | 0 | 0 | — | — | 0·0·0·0·0 |

**No-anchor slices (20)** — real sources but **zero best-practice anchors** (no T1/Co-1/T2/Co-2), so the base cannot carry a best-practice claim on its own. Two kinds:
- **‡ Code-floor / convergence-only (11)** — 0 confirmed evidence (pure T4–T6/grey); breadth is discounted. Read grades as coverage, not quality: `luminance-contrast-and-pattern`, `threshold-and-level-access`, `jurisdiction-grant-programmes-comprehensive`, `visual-alerting-and-wayfinding-light`, `body-sizes-supplementary-populations`, `european-accessibility-act-scope-clarification`, `accessible-laundry-room-design`, `government-grant-programmes-home-adaptation`, `therapeutic-lighting-design`, `crpd-implementation-built-environment`, `co1-housing-research-global-south`.
- **† Supporting-only (9)** — confirmed T3-clinical primary evidence but no anchor; genuine supporting evidence that still needs a T1/Co-1/T2/Co-2 anchor to make a best-practice claim: `stair-ramp-threshold-biomechanics-accessibility`, `reach-range-and-accessible-controls`, `circadian-lighting-melanopic-edi`, `ecological-psychology-haptic-affordances-built-environment`, `wayfinding-cognitive-science-spatial-design`, `intellectual-disability-built-environment-design`, `floor-vibration-wheelchair-disability`, `cross-population-conflict-resolutions`, `thermoregulation-built-environment`.

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

1. **Thicken the anchor tiers (T1/Co-1/T2/Co-2).** With only 76 systematic-review/evidence-based-standard instances corpus-wide, most best-practice claims lean on individual T1 primary studies or on code convergence (T4–T6, disallowed as best-practice warrant). Prioritise SR/meta-analysis + DPO-standard recovery on the 20 no-anchor slices — especially the 9 supporting-only ones, which already hold confirmed T3-clinical evidence and need only an anchor to become citable.
2. **Convert non-English search into non-English evidence.** Searches ran in 19 languages but the corpus is ~73% English. Target the languages already searched-with-results but under-linked, and the zero-yield languages (`ar`, `bn`, `hi`, `id`, `sw`) explicitly.
3. **De-risk monojurisdictional slices.** 3 evidenced slices rest on ≤1 jurisdiction; flag their numeric thresholds as non-transferable until a second regime is sourced.
4. **Fill or formally park the empty slices.** Move the 7 un-started slices into an active search queue or an explicit deferred state so they stop reading as silent gaps.
5. **Treat the doubly-concentrated slices as citation-risk.** The 14 ≥90%-English-and-≥50%-Anglophone slices are where global-applicability claims are weakest.
6. **Fix the mis-filed jurisdiction codes.** Move the 4 `DA`×1, `ZH`×3 values out of `evidence_sources.jurisdiction` and recover the true jurisdiction — a one-off migration.

## 7. Limitations & what this audit does *not* claim

- **Instance-weighted, not source-weighted.** The 753 instances are 651 unique sources, so corpus tier/language totals run ~16% above unique-source counts. Per-slice figures are unaffected.
- **The composite is a lens, not ground truth.** Weights (20/30/20/15/15) are a defensible but editorial choice; the six raw dimensions are printed alongside every grade so a reader can re-weight. No grade is stored in the DB — it is recomputed each run.
- **Coverage ≠ correctness.** The audit measures the *shape* of each base (how much, what tier, where from, what language, how concentrated). It does **not** re-verify that any citation resolves, is current, or supports its claim — those are the `url_verification_runs` / `code_currency` / supersession checks, run separately.
- **Jurisdiction shares rest on recorded jurisdictions only.** NULL-jurisdiction instances are excluded from %ANG denominators, so a low %ANG can mean *genuinely non-Anglophone* or *unrecorded* — the master table’s JUR count exposes the denominator.
- **Compound jurisdictions classify by their strongest Anglophone member** (e.g. `US/AU/INT` counts as native-Anglophone). Magnitude ≈1% of instances.

---
*Data as of 2026-07-19 · read-only over `data/guidebook.db` · generated by `tools/evidentiary_audit.py`. Independently red-teamed; raw counts reproduce through a second code path. Aligned to `governance/tier-system.md`.*
