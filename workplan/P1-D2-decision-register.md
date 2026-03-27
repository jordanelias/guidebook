# Decision Register — P1-D2: Parts 4–7
## Item Consolidation Gate + Editorial Decisions

**Session:** Phase 1 Session 2
**Date:** 2026-03-26
**Basis:** v9.0 document · Critique Report v9.0 · Systematic Audit 2026-03-24 · Connection Register (CON-0001–0032) · Gap Register (127 OPEN) · Decision Register P1-D1 (D1-01–D1-34) · Item Review S2 · Workplan v10.2
**Status:** DRAFT — requires author approval before any Phase 2 work begins.

---

## Cross-Analysis Summary

Before presenting decisions per-Part, these are the structural patterns identified by cross-referencing all source documents.

### Pattern 1: Overlapping Items Within Part 7

| Candidate pair | Overlap | Recommendation | Rationale |
|---|---|---|---|
| C-03 (Pattern Avoidance) + C-06 (Plain Flooring) | Both specify pattern-free floor/wall surfaces. C-03 applies to "sensitive environments"; C-06 applies "throughout". C-06 is the stronger provision. | **MERGE → C-03** (absorb C-06 as "throughout" scope) | Two items specifying the same physical intervention (no geometric patterns). C-06 is C-03 applied universally. One item with tiered scope: sensitive → throughout. |
| B-03 (No Fluorescent) + B-04 (Flicker-Free LED) | B-03 eliminates fluorescent; B-04 specifies IEEE 1789 compliance for replacement LED. Sequential spec — B-04 is meaningless without B-03. | **MERGE → B-03** (rename: "Safe Lighting Source — No Fluorescent, Flicker-Free LED") | Practitioners specify these as a single action. All 5 worked examples and all 7 NR matrices list "B-03/04" as a unit. Never specified independently. |
| A-10 (Counter Loop) + A-11 (Room Loop) | Same technology; different scales. | **KEEP SEPARATE** | Different design stage, spatial scope, trigger thresholds. |
| G-01 (Defensible Seating) + G-07 (Waiting Area Seating) | Adjacent seating function. | **KEEP SEPARATE** | Different populations (MH/NDV vs MOB), different purpose (psychological vs physical access). |
| D-05 (Enclosed Low-Stim) vs A-16 (Sensory Room) | Overlap per CON-0002/CON-0019. | **KEEP SEPARATE + add cross-reference** | D-05 = planning principle (multiple small spaces). A-16 = specific room type with full spec. CON-0002/0019 confirm distinct functions. Add hierarchy note: A-16 > D-05 > general circulation. |
| F-02 (Fragrance-Free) + F-04 (Air Quality) | Related environmental controls. | **KEEP SEPARATE** | F-02 = policy/management (OPS stage). F-04 = engineering (SD/DD). Different responsible parties, different drawings. |
| C-04 (LRV ≥30) vs C-05 (Low LRV Differential) | Both address contrast. | **KEEP SEPARATE** | Opposite principles for different populations. C-04 = maximise contrast (VIS). C-05 = minimise differential (DEM). Merging would cause misapplication. |

**Net item count change from mergers:** −2 (C-06 absorbed; B-04 absorbed)

### Pattern 2: Connection Register → Part 7 Implications

19 HIGH-confidence connections analysed. Sorted into three action categories:

**A — Population additions (existing items; add population codes in Phase 3):**

| CON | Item(s) | Population to add |
|---|---|---|
| CON-0003 | G-03, G-04, G-05 | PAIN, OFS, DEM, NEU |
| CON-0007 | E-01, E-06, E-08 | DEAF, DBL, MH, DEM (side-by-side communication width) |
| CON-0010 | BIO-01–BIO-05, A-16 | Cross-reference consolidation (DEM, OFS, NDV, MH) |
| CON-0011 | A-10, A-11 | DBL (residual hearing loop benefit) |
| CON-0017 | H-02, A-16, B-06, B-07 | 7-population convergence on "user control" → elevate H-02 to PRIMARY in A-16 |
| CON-0018 | D-03 | NDV/AUT, OFS (toilet visibility beyond DEM) |

**B — Cross-reference additions (existing items; Phase 3):**

| CON | Action |
|---|---|
| CON-0001 | D-02, D-06, D-08, D-09, C-04 → add Tier 0 circulation legibility note |
| CON-0014 | B-10 ↔ Part 8 §8.5 unresolvable conflict (DEAF strobe vs NEU/NDV seizure) |
| CON-0024 | Prospect-refuge theory as unifying principle for A-16, D-05, G-01, D-11 → Part 1 §1.4 |

**C — New item or structural implication (decisions below):**

| CON | Implication | Decision ref |
|---|---|---|
| CON-0004 | Seated/reclined work provision → potential new item | D2-37 |
| CON-0019 | A-16 + NDV/MH retreat + OFS rest convergence | D2-38 |
| CON-0029 | Inclusive POE tool → new RFO-stage specification | Deferred to P1-D3 |

### Pattern 3: Gap Register → Part 7 Implications

| Gap | Action | Decision |
|---|---|---|
| GAP-CR-03 | 68+ phantom cross-references | Resolved by DEC-03 (I-04/I-05/I-06), DEC-04 (H-05), GAP-STRUCT-01 (J-items), Phase 4 cleanup |
| GAP-CR-04 | Duplicate E-06/E-07/E-08/E-09 | Delete duplicate block (lines 3651–3755). Phase 3. |
| GAP-STRUCT-01 | Category J (BAR) — strike | Confirmed: delete. Redirect to Supp Vol. |
| GAP-STRUCT-02 | BIO/TC in Vol 2 body | Resolved by DEC-06: promote to Part 7 Categories L/M |
| GAP-SRS-01 | A-16 user control elevation | Phase 3 item revision (H-02 → PRIMARY cross-ref) |
| GAP-IMPL-02 | G-08 resilient flooring | Not created. Single source — insufficient evidence. |
| GAP-NEW-09 | DBL interpreter seating undefined | Folded into K-01 expansion (D2-39) |
| GAP-STEP6-03 | DBL intervenor width E-08 | Phase 3 E-08 population note |
| GAP-DBL-BE-01 | THIN-BASE on all DBL specs | Phase 3 systematic pass |

---

## Part 4 — Synthesis and Sequencing

| ID | Section | Decision | Rationale |
|---|---|---|---|
| D2-01 | §4.1 Why Synthesis Matters | **KEEP** | Core doctrine; four failure modes well-articulated. |
| D2-02 | §4.2 Layered Environment | **KEEP + MINOR EDIT** — update item refs post-merger (B-03/04 → B-03; C-03/06 → C-03) | Layer model is strongest structural concept. |
| D2-03 | §4.3 Four Synthesis Principles | **KEEP** | Non-negotiable. |
| D2-04 | §4.4 Stage-by-Stage | **KEEP + INTEGRATE D1-24** — absorb Entry Path I table. Update DD/RFO terminology. | D1-24 moves Entry Path I here. |
| D2-05 | §4.5 Building Strategies | **KEEP + CONDENSE 10%** — remove stale Part refs | Minimal work. |
| D2-06 | §4.6 Decision Framework | **KEEP** — update "Part C/H" → "Part 8" | Q1–Q4 sequence is excellent. |
| D2-07 | §4.8 Approach | **KEEP** — no cuts | "Most conceptually valuable section" — Critique Report. |
| D2-08 | §4.9 (cross-pop guidance) | **CUT → 2-sentence pointer to Part 8** | Per D1-21: §3.4 content moves to Part 8 §8.4. |

### D2-09: DEC-11 — Worked Examples

**Decision: KEEP 5.**

| # | Type | Primary pop. | Complexity | Unique contribution |
|---|---|---|---|---|
| 1 | Memory Care Residential | DEM | Simple | D-03 Marquardt evidence (47% incontinence reduction) |
| 2 | Co-working Office | NDV+OFS | Moderate | Primary non-residential NDV example |
| 3 | Primary School | NDV+MOB+DEAF | Complex | Highest-NDV-prevalence building type |
| 4 | Hospital Ward | MOB+DEM+BAR(→Supp) | Complex | Highest-risk building type; Supp Vol cross-ref |
| 5 | Supported Housing | MOB+DEM+NDV+PAIN/OFS | Most complex | Only full co-occurrence example |

Reducing to 3 loses either education or hospital — both are critical building types with unique specification challenges. The ascending complexity demonstration across 5 examples is pedagogically valuable. ~300 lines of marginal cost is justified.

**Revision needed:** Update BAR references in Example 4 to Supp Vol. Update DD/RFO terminology throughout.

---

## Part 5 — Residential Application Matrices

| ID | Element | Decision | Rationale |
|---|---|---|---|
| D2-10 | DEC-07: Sub-table structure | **KEEP current 6-part structure; reduce to 5 in final form** by merging "citation additions" into Part 7 items during Phase 3. Final per room: (1) criticality, (2) item table, (3) DAR, (4) conflict register, (5) schematic checklist. Omit empty conflict registers silently. | 6-part structure is what makes matrices practitioners' most useful tool. Condensing to 3 collapses functionally distinct information. |
| D2-11 | §6.x numbering | **RENUMBER → §5.x** — Phase 4 | GAP-CR-02. |
| D2-12 | §6.0a Universal Residential | **ABSORB into §5.0** as second half | Orphan sub-section. Content essential but structurally misplaced. |
| D2-13 | BAR columns in all matrices | **DELETE.** Footnote per room: "Large body size: Supp Vol Part 4." | PI rule. Standing rule. D1-20. |
| D2-14 | IntD cells | **KEEP with ○ + [TIER 4-5]** | Per D1-17. Removal loses proxy guidance. |
| D2-15 | Phantom items in matrices | Resolve per DEC-03/DEC-04 below. J-items → Supp Vol redirect. | GAP-CR-03. |

### D2-16: §6.0a Item Code Errors (data integrity)

The Universal Residential Provisions table has 4 incorrect cross-references:

| Table says | Should be | Fix |
|---|---|---|
| I-04 (phantom) | G-04 (Accessible Bathroom) — unless new I-04 created (see D2-30) | Update after DEC-03 resolution |
| I-03 for "Grab bar blocking" | G-03 | Correct in Phase 3 |
| K-01 for "Lever hardware" | I-01 | Correct in Phase 3 |
| G-04 for "MERV 13 filtration" | F-04 | Correct in Phase 3 |

---

## Part 6 — Non-Residential Application Matrices

| ID | Element | Decision | Rationale |
|---|---|---|---|
| D2-17 | §7.x numbering | **RENUMBER → §6.x** — Phase 4 | GAP-CR-02. |
| D2-18 | §7.0 Universal NR Provisions | **KEEP** — 16 items, well-structured. Minor ref updates. | Strongest non-residential reference table. |
| D2-19 | BAR references | **DELETE** — same as Part 5 | Standing rule. |
| D2-20 | IntD paragraphs | **KEEP with [TIER 4-5]** | Per D1-17. All 7 NR matrices have them. |
| D2-21 | NR matrix structure | **ADD conflict register sub-table** to each NR matrix in Phase 3. Currently only residential matrices have them. CON-0014, CON-0020 provide content. | Structural consistency with Part 5. |

---

## Part 7 — Item Specification Library

### THE CRITICAL GATE: DEC-01 — Item Consolidation

#### A — MERGERS (recommend approval)

| ID | Items | Merged result | Rationale |
|---|---|---|---|
| D2-22 | **C-03 + C-06 → C-03** | C-03 Pattern and Surface Consistency (No Geometric Patterns) | C-06 is C-03 applied universally. Same intervention, same populations (DEM, NDV), same evidence (DSDC, PAS 6463). One item with tiered scope. |
| D2-23 | **B-03 + B-04 → B-03** | B-03 Safe Lighting Source (No Fluorescent; Flicker-Free LED; IEEE 1789) | All 5 worked examples and all 7 NR matrices cite "B-03/04" as unit. Sequential spec — B-04 meaningless without B-03. |
| D2-24 | **A-17 → G-02** | G-02 Variety of Seating Types (Three Heights; Upholstered; Rubber/Felt Feet) | A-17 is categorised as Acoustics but its primary function is seating material specification. Acoustic absorption (NRC 0.15–0.30) is secondary. PAIN allodynia/fibromyalgia benefit is the stronger clinical rationale — belongs with furniture, not acoustics. |

**Code disposition:** C-06, B-04, A-17 retire. All cross-references redirect to merged items.

#### B — ITEMS KEPT SEPARATE (merger rejected)

A-10/A-11 · G-01/G-07 · D-05/A-16 · F-02/F-04 · C-04/C-05 · A-01/A-04 — all kept separate for reasons documented in Pattern 1 above.

#### C — DEC-03: Phantom I-04, I-05, I-06

Systematic audit finding 3.3a: these have engineering specs in Part 9 but no Part 7 design entries.

| Phantom | Decision | Rationale |
|---|---|---|
| **I-04** "Drainage Channel" | **ABSORB into G-04** (Wet Room) | G-04 already specifies zero threshold. I-04 adds drainage engineering detail as sub-section. No new code. |
| **I-05** "Ceiling Hoist" | **CREATE as I-04** (new Part 7 item) | NOT-RETROFITTABLE. ×20–40 retrofit multiplier. Second-highest cost multiplier after grab bar blocking. Populations: MOB, DEM (late-stage), NEU. Design stage: CD-CRITICAL. Deserves standalone spec. |
| **I-06** "Kitchen Power" | **ABSORB into I-02** (Kitchen One-Handed) | I-02 already covers cooktop/oven/microwave positions. I-06 adds socket height detail (400–1100 mm AFF). One additional line in I-02. |

**Net:** +1 new item (I-04 Ceiling Hoist Tracking). All phantom references resolve.

**I-04 specification brief (Phase 3 item-specification-writer):**
- Title: Ceiling Hoist Tracking — Structural Blocking and Motor Infrastructure
- Populations: MOB (primary), DEM (secondary), NEU, OFS
- Core spec: continuous ceiling blocking ≥3600 mm; 13 A switched fused spur; motor ≥200 kg SWL (≥300 kg bariatric)
- Stage: CD-CRITICAL
- Retrofit: ×20–40
- Sources: Lifetime Homes 9+10; Habinteg 2022; BS 8300:2018 §11; RCOT Housing Adaptations Without Delay 2019

#### D — DEC-04: H-05 (Nurse Call)

**Decision: CREATE as H-05 Emergency Pull Cord / Nurse Call.**

Engineering spec exists (Part 9 line 4880). Referenced 7 times. Safety-critical system.

**H-05 specification brief:**
- Populations: MOB, DEM, NEU (fall risk); DEAF (visual indicator); DBL (vibrotactile relay)
- Core spec: dual-height pull cord (100 mm + 800–1100 mm AFF); red cord LRV ≥30; BMS/nurse call connected; visual corridor indicator; K-04 vibrotactile relay for DBL
- Scope: all accessible bathrooms in non-residential healthcare, residential care, supported housing. Residential: DAR conduit.
- Stage: CD
- Cross-refs: B-10, K-04, G-03

#### E — DEC-06: BIO/TC Promotion to Part 7

**Decision: PROMOTE.**

| Argument | Weight |
|---|---|
| Already cross-referenced from Part 7 using Part 7 item codes | HIGH — they function as Part 7 items already |
| Formatting inconsistency (compressed paragraph vs structured template) | MODERATE — Critique Report finding |
| CON-0010/CON-0024: BIO serves multiple populations with cross-population convergence | HIGH — appendix burial understates importance |
| TC-05 carries strongest single epidemiological dataset in entire guidebook | HIGH — appendix is wrong location for strongest evidence |
| GAP-STRUCT-02 flags BIO/TC presence in Vol 2 body as error | HIGH — need canonical home |

**Implementation:**
- BIO-01–BIO-05 → **Category L: Biophilic Design**
- TC-01–TC-05 → **Category M: Thermal Comfort**
- Reformat all 10 to standard Part 7 template
- Appendix B/C become pointers: "See Part 7 Category L/M"
- Fix all "Part 11I §8.4" stale references
- **Structural change → requires CO-0003 + toc-editor**

#### F — DEC-12: F-02 (Fragrance-Free)

**Decision: KEEP.**

4 populations (NDV, PAIN, MH, OFS). CON-0015 adds MH via TID. OFS/MCAS = safety spec (anaphylactic-grade reactions). Referenced in 5/9 residential + 6/7 NR matrices. FDR confirmed as CONFIRMS finding.

#### G — DEC-13: A-17 (Upholstered Seating)

**Decision: ABSORB into G-02** (see D2-24 merger above).

#### H — Category J (BAR)

**Decision: CONFIRM GAP-STRUCT-01 — DELETE Category J.** J-01–J-05 redirect to Supp Vol Part 4. Not content loss — relocation to canonical home.

#### I — Duplicate E-06/E-07/E-08/E-09

**Decision: CONFIRM GAP-CR-04 — DELETE duplicate block (lines 3651–3755).** First instance (3508–3597) is canonical.

#### J — A-10b (Hydrotherapy RT60)

**Decision: KEEP as variant.** Specific acoustic parameter (RT60 ≤1.0 s at 500 Hz) for pool environments. Appropriately coded as A-10 variant.

#### K — New items and expansions from cross-analysis

| ID | Source | Decision |
|---|---|---|
| D2-30 | Phantom I-05 → I-04 | **CREATE** Ceiling Hoist Tracking (see §C above) |
| D2-31 | Phantom H-05 | **CREATE** Emergency Pull Cord / Nurse Call (see §D above) |
| D2-37 | CON-0004 | **DEFER** reclining rest position to Phase 2C. FDR identified as NOVEL — needs spec development. Log as item-specification-writer briefing for Phase 3 Session 15. |
| D2-38 | CON-0002 + CON-0019 | **KEEP existing items; add PAIN/OFS to A-16 population list + rest configuration option.** Not a new item. A-16, D-05, NDV/MH retreat serve distinct functions. |
| D2-39 | GAP-NEW-09 | **EXPAND K-01** beyond service counters to all DBL positions (assembly, classroom, waiting). Rename: "K-01 Intervenor and Interpreter Adjacency (All DBL Positions)." Add 1200×1500 mm clear floor zone. |

### D2-40: ●/○ Notation Guide

**Decision: Adopt dual-meaning with explicit legend.**

| Symbol | Population context (Parts 2, 5, 6) | Evidence context (Part 7 IntD items) |
|---|---|---|
| ● | Primary design driver | — |
| ○ | Secondary benefit | Interim provision [TIER 4-5] |
| — | Not applicable | Not applicable |

No conflict — different sections. Add "Notation Guide" to §5.0 and §7.0 introductions.

---

## Post-D2 Part 7 Inventory

| Cat | Name | Items | Change |
|---|---|---|---|
| A | Acoustics | 16 | −1 (A-17 → G-02); A-10b as variant |
| B | Lighting | 10 | −1 (B-04 → B-03) |
| C | Colour / Surface | 5 | −1 (C-06 → C-03) |
| D | Spatial / Wayfinding | 11 | — |
| E | Entry / Circulation | 11 | Duplicates removed |
| F | Sensory Zoning | 5 | — |
| G | Furniture / Fixtures | 7 | +A-17 spec absorbed |
| H | Controls / Technology | 5 | +1 (H-05) |
| I | Upper Limb | 4 | +1 (I-04 Hoist); I-06 → I-02 |
| K | DeafBlind | 4 | K-01 expanded |
| ~~J~~ | ~~BAR~~ | ~~0~~ | Deleted → Supp Vol |
| **L** | **Biophilic** (new) | **5** | From Appendix B |
| **M** | **Thermal** (new) | **5** | From Appendix C |
| **Total** | | **88** | Was ~90 unique; −3 merged, −5 J deleted, +2 created |

---

## Change Orders Required

| CO | Change | Trigger | Session |
|---|---|---|---|
| CO-0003 | Create Categories L + M; retire Appendix B/C as repositories | DEC-06 | Phase 3 S16 |
| CO-0004 | Delete Category J; update all J-refs → Supp Vol | GAP-STRUCT-01 | Phase 3 S16 |
| CO-0005 | Renumber Part 5 → §5.x, Part 6 → §6.x | GAP-CR-02 | Phase 4 S19 |

---

## Author Approval Required

| Priority | ID | Question |
|---|---|---|
| **CRITICAL** | D2-22 | Approve C-03+C-06 merger? |
| **CRITICAL** | D2-23 | Approve B-03+B-04 merger? |
| **CRITICAL** | D2-30 | Approve I-04 Ceiling Hoist creation from phantom I-05? |
| **CRITICAL** | D2-31 | Approve H-05 Nurse Call creation? |
| **HIGH** | D2-24 | Approve A-17 → G-02 absorption? |
| **HIGH** | DEC-06 | Approve BIO/TC → Categories L/M? |
| **HIGH** | DEC-12 | Confirm F-02 keep? |
| **HIGH** | DEC-11 | Confirm 5 worked examples? |
| MODERATE | D2-37 | Confirm reclining rest deferral? |
| MODERATE | D2-39 | Approve K-01 expansion? |
| MODERATE | D2-40 | Approve ●/○ notation guide? |

---

## Cumulative Totals (D1 + D2)

| Metric | Value |
|---|---|
| Decisions resolved | 74 (D1: 34 + D2: 40) |
| Content removed | ~184 lines |
| Items merged | 3 (C-06→C-03; B-04→B-03; A-17→G-02) |
| Items created | 2 (I-04 Ceiling Hoist; H-05 Nurse Call) |
| Categories added | 2 (L Biophilic; M Thermal) |
| Categories deleted | 1 (J BAR) |
| Change Orders | 4 (CO-0002–CO-0005) |
| Pending: P1-D3 | Parts 8–13 + Appendices (DEC-08 through DEC-20) |

*End of P1-D2 Decision Register Draft*
