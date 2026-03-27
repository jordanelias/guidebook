# Phase 2A Output Register
**Session:** 4
**Date:** 2026-03-27
**Operations:** (1) Pre-v4 slug triage · (2) Case study evidence mining · (3) Gap register post-decision triage

---

## Operation 1: Pre-v4 Slug Triage

**Basis:** Existing triage file (`workplan/pre-v4-slug-triage.md`) plus newly identified slug.
**Total slugs in registry:** 64 (confirmed — directory names excluded from count).
**Triage file coverage:** 63 slugs classified in prior session. One slug requires triage now.

### New Slug: `jurisdiction-matrix-accessibility-standards`

**Status in SL file:** 13/14 languages SEARCHED, 1 NOT-RUN (1 language gap), no BPS.
**Content:** 17-jurisdiction comparative standards matrix. Core reference for Appendix A and §1.5.
**Decision: SUPPLEMENT** — coverage is strong (13/14) but BPS absent and 1 language gap. Targeted gap-fill: add missing language + write BPS. Phase 2B Session 5 (Foundations batch).

### Complete Triage Summary (all 64 slugs)

| Class | Count | Phase 2B session | Est. work |
|---|---|---|---|
| KNOWN — no action | 4 | — | — |
| CONSUME — metadata backfill | 11 | Session 5 (batch) | ~500 tok/slug |
| SUPPLEMENT — targeted gap-fill | 17 | Sessions 5–6 | ~1,500 tok/slug |
| RE-RUN (item-level, full v4) | 21 | Sessions 5–8 | ~2,000+ tok/slug |
| RE-RUN (framework/methodology) | 8 | Sessions 5–7 | ~1,500 tok/slug |
| RE-RUN (economics/policy) | 3 | Session 7 | ~1,500 tok/slug |

### Decision Register Eliminations

Post-D2/D3 Decision Register, the following slugs are affected:

| Slug | Impact | Action |
|---|---|---|
| `bariatric-turning-radius-built-environment` | Category J deleted; BAR → Supp Vol only | RE-RUN classification unchanged — Supp Vol still needs this evidence |
| `body-sizes-supplementary-populations` | BAR → Supp Vol confirmed | SUPPLEMENT classification unchanged |
| `biophilic-design-healthcare-workplace` | BIO stays Appendix B (reformatted) | SUPPLEMENT P3 — still needed for Appendix B |
| `ot-frameworks-built-environment` | §1.8 → Appendix F confirmed | RE-RUN P3 — still needed for Appendix F content |
| `design-framework-evidence-audit` | §1.8 → Appendix F | RE-RUN P3 — feeds Appendix F |
| `accessible-design-economics-cost-premium` | Part 12 Economics kept + expanded | SUPPLEMENT P1 — priority unchanged |
| `government-grant-programmes-home-adaptation` | Top-10 grants decision (DEC-18) | RE-RUN P1 — scope now top-10 jurisdictions only |
| `jurisdiction-grant-programmes-comprehensive` | Top-10 grants decision (DEC-18) | RE-RUN P1 — scope top-10 jurisdictions |
| `sensory-relief-space-design` | F-02 policy relocated to Appendix D | RE-RUN P2 — sensory relief spec still needed for D-05/A-16 |

**No slugs eliminated by Decision Register.** All content survived the cut — BAR/TC slugs redirect to new locations rather than being discarded.

### Duplicate Merge Decisions (carried from triage file)

| Pair | Decision |
|---|---|
| `chronic-pain-built-environment` + `pain-ofs-built-environment-design` | Assess merge post-research. Likely: chronic-pain absorbed into pain-ofs. |
| `government-grant-programmes-home-adaptation` + `jurisdiction-grant-programmes-comprehensive` | MERGE into single slug post-Session 7. |
| `luminance-contrast-and-pattern` + `luminance-contrast-lrv-evidence-base` | MERGE post-research — one is evidence base, one is application of same evidence. |
| `fatigue-spectrum-built-environment` + `ofs-built-environment` | Assess post-research. OFS-specific may absorb fatigue-spectrum. |

---

## Operation 2: Case Study Evidence Mining

**Source:** 14 existing case studies (Part 12/13 v9.0).
**Method:** Population code extraction + Part 7 item cross-reference + evidence tier assessment.

### Evidence Map

| Study | Populations | Key items | Evidence tier | Evidence contribution |
|---|---|---|---|---|
| §12.01 Maggie's Centre Inverness | MH, OFS, PAIN | A-16, B-03, BIO-01, E-06, E-11, F-01 | Tier 5 (design publication) | CONFIRMS: sensory gradient (F-01), sensory room (A-16), biophilic (BIO-01) for MH/OFS |
| §12.02 Gallaudet DeafSpace Campus | DEAF, DBL | A-08, A-10, B-02, B-10, D-10 | Tier 4 (programme documentation) | CONFIRMS: sightline items (D-10), no fluorescent (B-03→B-03), hearing loop (A-10) for DEAF |
| §12.03 The Kelsey Civic Commons | uncoded | A-14, E-06, E-08, F-01, G-03, G-04, H-02, I-01 | Tier 5 | CONFIRMS: compound disability co-design process; populations need coding (MOB, NDV, MH likely) |
| §12.04 DSDC Iris Murdoch | DEM | A-02, A-05, B-03, B-06, BIO-01, C-02, C-04, C-06→C-03 | Tier 4 | CONFIRMS: DEM acoustic + colour + biophilic provisions; C-06 ref → update to C-03 |
| §12.05 AtkinsRéalis HQ | uncoded | A-03, A-14, A-16, B-03, B-04→B-03, BIO-02 | Tier 5 | CONFIRMS: NDV/MH office provisions (needs population coding); B-04 ref → update to B-03 |
| §12.06 Lyngby-Taarbæk Acoustic | NDV, DEM | A-02 | Tier 3 (published evaluation) | CONFIRMS: RT60 ≤0.4s benefit for NDV; sparse item coverage |
| §12.07 Singapore HDB UD Flats | uncoded | none | Tier 5 (programme report) | SUPPLEMENTS: MOB/DEM residential; needs item coding and population assignment |
| §12.08 Gallaudet SLCC | DEAF, DBL | none | Tier 4 | CONFIRMS: DeafSpace spatial principles (D-10 family); needs item coding |
| §12.09 De Hogeweyk | DEM | BIO-01, C-06→C-03, D-01, D-04, D-09, D-11 | Tier 3 (published evaluation) | CONFIRMS: DEM loop circulation (D-01), landmark objects (D-04), consistent layout (D-09) |
| §12.10 DSDC Dementia Audit | DEM | A-02, C-03, C-06→C-03, D-03, D-04, D-08 | Tier 3 (multi-site audit) | CONFIRMS: DEM toilet visibility (D-03), pictogram signage (D-08); strongest DEM evidence study |
| §12.11 ASPECTSS Autism Retrofit | NDV | A-02, A-06, A-16, C-02, D-05, F-01 | Tier 2 (intervention study) | CONFIRMS: NDV/AUT acoustic (A-02/A-06), sensory room (A-16), sensory gradient (F-01); highest tier |
| §12.12 Village Landais Dax | DEM | B-09, BIO-01, C-02, C-06→C-03, D-01, D-03, E-06 | Tier 4 | CONFIRMS: DEM biophilic, loop circulation, toilet visibility; 4th DEM village study |
| §12.13 Carpe Diem Bærum | DEM | BIO-01, BIO-02, D-01, D-11, E-06 | Tier 4 | CONFIRMS: DEM biophilic + loop circulation; 5th DEM study |
| §12.14 BC Housing HAFI | DEM, MOB, OFS, PAIN | E-03, E-06, G-03, G-04, I-01, I-02 | Tier 3 (programme evaluation) | CONFIRMS: MOB bathroom + circulation; SUPPLEMENTS: OFS/PAIN home adaptation; only compound study |

### Population Coverage Assessment

| Population | Studies with primary coverage | Gap |
|---|---|---|
| DEM | 6 (§12.04, 12.09, 12.10, 12.12, 12.13 + §12.14 partial) | Over-represented — no action |
| DEAF/DBL | 3 (§12.02, 12.08 + §12.02 partial) | Adequate |
| NDV | 2 (§12.06, 12.11) | §12.11 is Tier 2 — strongest study; adequate |
| MOB | 1 partial (§12.14) | **UNDERREPRESENTED** — needs new study |
| MH | 1 partial (§12.01) | **UNDERREPRESENTED** |
| PAIN/OFS | 2 partial (§12.01, §12.14) | **UNDERREPRESENTED — 0 dedicated studies** |
| NEU/ABI | 0 | **ABSENT — priority for new study (D3-25 confirmed)** |
| NDV/MH | 0 | **ABSENT — priority for new study (D3-25 confirmed)** |
| VIS | 0 | **ABSENT** — but VIS often embedded in uncoded studies |
| IntD | 0 | Per DEC-05: condensed proxy; no case study required |

### Stale Item References (update in Phase 3)

| Study | Stale ref | Correct ref |
|---|---|---|
| §12.02 | B-03/B-04 cited as unit | → B-03 (post-merger) |
| §12.04 | C-06 | → C-03 (post-merger) |
| §12.05 | B-04 | → B-03 |
| §12.09 | C-06 | → C-03 |
| §12.10 | C-06 | → C-03 |
| §12.12 | C-06 | → C-03 |
| Multiple | TC-05 Heated Floor | → F-07 |
| Multiple | Appendix C refs | → Part 9 or F-category |

### New Case Studies Required (D3-25)

| Priority | Population | Target study type | Phase |
|---|---|---|---|
| P1 | PAIN/OFS | Residential or workplace with thermal/rest provisions documented | Phase 2B Session 8 |
| P1 | NDV/MH | Mental health facility or therapeutic environment with spatial/sensory evidence | Phase 2B Session 8 |
| P1 | NEU/ABI | Rehabilitation facility or supported housing with evidence of design impact | Phase 2B Session 8 |
| P2 | MOB (dedicated) | Residential adaptation programme with outcome data | Phase 2B Session 8 |
| P3 | Economics ROI | Building with documented cost-benefit outcome at design vs retrofit stage | Phase 2B Session 8 |
| P3 | Cross-population compound | MOB+NDV+OFS building with all three populations co-designed for | Phase 2B Session 8 |

### Evidence Contribution Field (new template requirement per D3-26)

All 14 existing studies require the following field added in Phase 3 (Session 13):

```
**Evidence Contribution:**
- Items confirmed: [list]
- Items supplemented: [list]  
- Evidence tier: [Tier N per hierarchy]
- Relationship to BPC: CONFIRMS / SUPPLEMENTS / CONTRADICTS
- Populations: [codes]
```

---

## Operation 3: Gap Register Post-Decision Triage

**Starting count:** 116 OPEN + 5 EXEC-READY = 121 actionable items.

### Gaps Eliminated by Decision Register

| Gap ID | Reason eliminated | New status |
|---|---|---|
| GAP-STRUCT-01 | Category J BAR deletion confirmed (CO-0004) | CLOSE-ELIMINATED — decision made |
| GAP-STRUCT-02 | BIO stays Appendix B; TC split executed (CO-0003) | CLOSE-ELIMINATED — decision made |
| GAP-CR-07 | "Part 11I §8.x" stale refs — will be fixed in Phase 3 Appendix B reformat | EXEC-READY Phase 3 S16 |
| GAP-CR-08 | "Developed Design" → "Design Development" — Phase 3 find-and-replace | EXEC-READY Phase 3 |
| GAP-CR-09 | "Commissioning" → "Ready for Occupancy" — Phase 3 find-and-replace | EXEC-READY Phase 3 |
| GAP-NEW-09 | K-01 expansion approved in D2-39 | EXEC-READY Phase 3 S16 |
| GAP-CO02-01 | CO-0002 (IntD matrix deletion) execution scheduled Phase 3 S11 | EXEC-READY Phase 3 S11 |
| GAP-066 | Tier marker renumber — Phase 3 find-and-replace pass | EXEC-READY Phase 3 |

**Net reduction from eliminations:** 8 items reclassified (2 CLOSE-ELIMINATED; 6 EXEC-READY).

### Phase 3 Session Assignments (EXEC-READY items)

| Gap ID | Content | Phase 3 Session |
|---|---|---|
| GAP-STEP5-01 | B-10 seizure risk disclosure | S15 (Part 7 Cat A–E) |
| GAP-034 (EXEC-READY) | B-01 circadian lighting upgrade | S15 |
| GAP-059 | CHD-10 + Supp Vol neuroinclusive school | S11 (Part 2) |
| GAP-060 | A-16 sensory spaces NCSE | S15 |
| GAP-063 | G-03/G-04 Guay biomechanics | S15 |
| GAP-CR-07 | Appendix B stale refs | S16 |
| GAP-CR-08 | DD terminology | All — find-and-replace S19 |
| GAP-CR-09 | RFO terminology | All — find-and-replace S19 |
| GAP-NEW-09 | K-01 expansion | S16 |
| GAP-CO02-01 | CO-0002 IntD deletion | S11 |
| GAP-066 | Tier marker renumber | S19 (Phase 4) |

### Remaining OPEN Count

| Category | Before | Eliminated | EXEC-READY | Remaining OPEN |
|---|---|---|---|---|
| P1 | 7 | 0 | 0 | 7 |
| P2 | 98 | 2 | 8 | 88 |
| P3 | 11 | 0 | 3 | 8 |
| P4 | 1 | 0 | 0 | 1 |
| **Total** | **117** | **2** | **11** | **104** |

**Updated OPEN: 104. EXEC-READY: 16 (5 prior + 11 new).**

### Notable P1 items still OPEN (unresolved — require Phase 2B research)

| Gap ID | Content | Resolution path |
|---|---|---|
| GAP-DBL-BE-01 | No Tier 1 DBL evidence | Phase 2B Session 6 — deafblind-built-environment-design SUPPLEMENT |
| GAP-CR-01 | Bibliography empty | Phase 3 S18 — bibliography-compiler |
| GAP-CR-02 | Numbering collisions | Phase 4 S19 — bulk-renumber |
| GAP-CR-03 | 68+ phantom cross-refs | Phase 4 S20 — cross-reference-resolver |
| GAP-CR-04 | Duplicate E-06/E-07/E-08/E-09 | Phase 3 S15 — delete duplicate block |
| GAP-CR-05 | ToC mismatch | Phase 4 S19 — toc-editor |
| GAP-CO2-TIER | Co-2 tier unpopulated | Phase 2B Session 5 |

---

## Phase 2A Summary

| Operation | Output | Status |
|---|---|---|
| Slug triage | 64 slugs classified; 1 new slug triaged (SUPPLEMENT); no eliminations | COMPLETE |
| Case study evidence map | 14 studies mapped; 6 new studies needed; stale refs logged; template field added | COMPLETE |
| Gap register triage | 104 OPEN remaining; 16 EXEC-READY; 2 CLOSE-ELIMINATED | COMPLETE |

**Phase 2A gate: PASSED.** Phase 2B research scope is now fixed.

### Phase 2B Research Scope (confirmed)

| Session | Work | Slug classes |
|---|---|---|
| 5 | Foundations: Co-2 + CRPD + CONSUME batch + threshold-door-hardware completion + jurisdiction-matrix SUPPLEMENT | 11 CONSUME + 2 SUPPLEMENT + 1 PARTIAL completion |
| 6 | Population: NDV/MH + NEU supplement + DEM supplement + DBL supplement + residential | 4 SUPPLEMENT + partial RE-RUN |
| 7 | Cross-population conflict evidence + economics deep-dive | cross-population-conflict-resolutions RE-RUN + economics cluster |
| 8 | Case study sourcing (6 new) + remaining SUPPLEMENT/RE-RUN slugs | case studies + overflow |

*End of Phase 2A Output Register*
