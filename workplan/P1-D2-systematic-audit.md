# Systematic Audit of P1-D2 Decision Register
## Internal Connections · Synergies · Incoherencies · Gaps

**Date:** 2026-03-26 19:00
**Method:** Cross-reference D2 decisions against: all 32 connections (19 HIGH, 9 MODERATE, 4 SPECULATIVE), 123 OPEN gap register items, FDR findings, critique report, systematic audit, and Part 7 item inventory.

---

## 1. INCOHERENCIES (decisions that contradict each other or existing structure)

### 1.1 F-05 (Seated-Task Design) is now a Category F outlier

**Problem:** D2 expands Category F to cover "all sensory environment zoning decisions across all modalities" — acoustic (F-01, F-03), olfactory (F-02), air quality (F-04 expanded), thermal (F-06, F-07). F-05 (Seated-Task Design) is not a sensory specification. It is an ergonomic/postural specification about whether tasks can be completed without sustained standing.

**Severity:** MODERATE. The category description now highlights the misfit. F-05 was arguably already miscategorised — seated-task design is about occupational posture, not sensory zoning.

**Options:**
- (a) **Relocate F-05 → G-08** (Furniture, Fixtures). G-02 covers seating variety; G-05 covers adjustable surfaces; G-06 covers counter height. F-05's seated-task principle is the governing design rationale for G-05 and G-06 — it could sit as G-08 "Seated-Task Design Principle."
- (b) **Rename Category F** from "Sensory Zoning" to "Environmental Zoning and Occupational Ergonomics" — but this weakens the coherent sensory-modality scope.
- (c) **Keep and note.** F-05 is a design principle that governs multiple items across categories; its placement in F (the environmental/zoning category) is defensible as "the building environment must not require sustained standing" — an environmental condition, even if not sensory.

**Recommendation:** Option (a). F-05 → G-08. Category F becomes purely sensory-modality zoning (7 items: F-01 through F-04, F-06, F-07, renumber or leave gap at F-05). This maintains the clean scope. F-05's content (service counter seating, queue seating, kiosk access) is functionally furniture/fixture specification.

### 1.2 F-06 (Thermal Zoning) and Part 8 conflict register overlap

**Problem:** TC-01 (now F-06) contains the MS/PAIN thermal conflict resolution: ambient ≤18°C + individual supplemental heating for PAIN users who need ≥20°C. This conflict is also documented in D1-32 as Part 8 §8.4 content (domain: thermal ~4 entries). D2 creates F-06 but doesn't clarify whether the conflict resolution lives in F-06, in Part 8, or both.

**Resolution:** F-06 states the specification and the conflict. Part 8 §8.4 documents the resolution methodology and cross-references F-06. Both reference each other. Not a true incoherency — but needs explicit cross-reference instruction for Phase 3 writers.

### 1.3 D2-38 underestimates the retreat/reset convergence

**Problem:** D2-38 treats the sensory relief / MH retreat / OFS rest convergence (CON-0002 + CON-0019) as a population addition to A-16. But the convergence is broader than D2-38 captures:

| Source | Finding |
|---|---|
| CON-0002 | Sensory relief + MH overlap |
| CON-0004 | Seated/reclined work provision (4 OPEN gaps share root cause) |
| CON-0019 | A-16 + NDV/MH retreat + OFS rest — 4 populations independently need "a quiet place to lie down" |
| GAP-B4-08 | Reclining/tilt seating — no spec exists |
| GAP-NEW-11 | Same finding, independently |
| GAP-FDR-06 | Adjustable bed elevation for OFS |
| GAP-FDR-07 | Supine recovery space (lie-down room) in workplaces |
| GAP-FDR-T0-03 | Retreat/reset room — Tier 0 candidate, 6+ populations |
| GAP-FDR-T0-04 | Entrance recline seating — Tier 0 candidate |

**That's 9 independent signals.** D2-37 defers the reclining provision to Phase 2C. D2-38 treats the retreat/reset room as "just add PAIN/OFS to A-16."

**Severity:** HIGH. This is the strongest convergence signal in the entire cross-analysis. A-16 is a sensory room — occupant-controlled dimming, sound, blackout. The retreat/reset need is different: it's a recovery space requiring recumbent posture, thermal comfort, proximity to sanitary facilities, and quiet. A-16 can serve this function if its specification is expanded, but the current A-16 spec (≥8 m², one per floor) doesn't include recumbent provision, recovery time allowance, or adjacency to WC.

**Recommendation:** Elevate D2-37 from DEFER to PROVISIONAL-CREATE. Not a full new item yet, but A-16 must be substantively revised in Phase 3 to include:
- Recumbent rest configuration option (fold-flat seating or day-bed)
- WC adjacency requirement (per GAP-FDR-02: ≤5 m for OFS)
- Minimum occupancy time allowance (not a "10-minute break room")
- Tier 0 candidacy note (6+ populations converge)

If Phase 2C research confirms specification parameters, upgrade to standalone item. If A-16 revision absorbs the need, close.

---

## 2. MISSED CONNECTIONS (MODERATE connections not addressed in D2)

D2 Pattern 2A captured population additions from HIGH connections only. 7 MODERATE connections imply additional population additions not yet scheduled:

| CON | Items | Missing population | Evidence |
|---|---|---|---|
| CON-0005 | A-09 (vibration isolation) | PAIN (joint-loading from floor vibration) | MODERATE — MOB WBV evidence extends to PAIN by mechanism. GAP-B4-09 same. |
| CON-0006 | B-01 (circadian lighting) | MH, OFS (sleep disruption as core symptom) | MODERATE — circadian entrainment mechanism identical. |
| CON-0008 | A-02, A-08, A-13 | PAIN, OFS (acoustic sensitivity/hyperacusis) | MODERATE — THIN-POPULATION-SPEC. GAP-CON-08 same. |
| CON-0009 | Entry/threshold items | OFS (PEM from step negotiation), PAIN (joint loading) | MODERATE — energy conservation rationale. GAP-CON-09 same. |
| CON-0013 | Kitchen items (G-05/G-06) | OFS, PAIN (seated work, joint-loading reduction) | MODERATE — GAP-B4-07 same. |
| CON-0015 | F-02, F-04 | MH (TID: chemical stimuli as PTSD triggers) | MODERATE — already noted in D2 §F but not in formal population addition table. |
| CON-0025 | Outdoor/biophilic provisions | NDV (sensory-responsive outdoor design) | MODERATE — SREF framework not in D2. |

**Systemic finding:** These are not 7 independent gaps. They reveal a single structural pattern: **PAIN and OFS are systematically under-coded across Part 7.** The FDR PAIN/OFS run confirmed 18 NOVEL findings for 2 populations that were virtually absent from the original item library. D2's individual population additions (Pattern 2A) address the HIGH connections but miss the MODERATE ones.

**Recommendation:** Add D2-41 standing instruction:

> **D2-41: PAIN/OFS Systematic Population Audit.** During Phase 3 writing, every Category A through M item must be assessed for PAIN and OFS population applicability. This is not item-by-item — it is a systematic pass. The 9 MODERATE connections (CON-0005/0006/0008/0009/0013/0015/0025) and 18 FDR NOVEL findings provide the assessment framework. Items confirmed as PAIN/OFS-applicable gain the population code. Items where evidence is thin gain THIN-POPULATION-SPEC disclosure. Items where PAIN/OFS is not applicable are annotated "assessed — not applicable" to prevent re-analysis.

---

## 3. GAPS (decisions that should exist in D2 but don't)

### 3.1 VI-xx legacy references unresolved

VI-02 ("Sensory Budget"), VI-03 ("Temporal Accessibility"), VI-08 ("Proprioceptive Design") appear 5+ times in Part 7 cross-references. D2 addresses J-items (delete) and I-items (create/absorb) but not VI-xx.

**Finding:** These are conceptual labels from a prior numbering scheme that point to ideas, not items. "Sensory Budget" is a design principle, not a specification. "Temporal Accessibility" describes the principle that accessibility changes over time — covered by DAR doctrine. "Proprioceptive Design" is a sensory modality concept — partially covered by BIO-03 (tactile texture variety).

**Decision needed (D2-42):** DELETE all VI-xx references. Replace with inline text where the concept is meaningful (e.g., "VI-03 (Temporal Accessibility)" → "see DAR doctrine, Part 11"). Phase 3 find-and-replace pass.

### 3.2 "MIS" population code in A-01 and BIO-04

"MIS" (misophonia) appears in A-01 Applicable Groups and BIO-04. It is defined in the NDV section (line 559) as a sub-type of NDV but is not in the canonical population code table. The code system uses NDV/SENS for sensory processing differences including misophonia.

**Decision needed (D2-43):** Replace all "MIS" → "NDV/SENS" in Phase 3. Add misophonia as a named condition under NDV/SENS in the Population Code Reference table footnote.

### 3.3 E-12 (Emergency Evacuation) phantom status

E-12 is referenced in NR matrices, worked examples, and Part 9 engineering tables. It has engineering specs (evacuation lift power, stairwell pressurisation, refuge intercom) but no Part 7 design entry. Same pattern as H-05 (now resolved by D2-31).

**However:** Appendix D explicitly states the guidebook defers evacuation to jurisdiction codes. This is intentional — evacuation procedures are life-safety regulated and jurisdiction-specific.

**Decision (D2-44): KEEP E-12 as a reference code, not a Part 7 item.** E-12 points to Appendix D + Part 9 engineering specs. It is deliberately not a design specification because evacuation requirements vary by jurisdiction and must be determined by the fire engineer, not the guidebook. Add a one-line definition in Part 7 introduction: "E-12 (Emergency Evacuation) is a reference code for coordination items in Part 9 and Appendix D; it is not a design specification."

### 3.4 R-STA-02 room-specific code

D2-16 notes R-STA-02 as an error in the Universal Residential Provisions table but doesn't resolve it.

**Decision (D2-45):** R-STA-02 is a DAR annotation within the R-STA room matrix, not a Part 7 item. Remove from Universal Residential Provisions table. The content (stair structural channel for stairlift) is already in R-STA DAR provisions.

### 3.5 A-12 Auracast technology currency

A-12 specifies a Bluetooth technology (Auracast/LE Audio) that launched in 2023 and is still in early adoption. The specification is sound (broadcast audio replacing induction loops for high-noise environments) but carries technology-specific risk that other items don't.

**Decision (D2-46):** Add technology-currency disclosure to A-12: "[Technology specification current as of March 2026. Auracast/LE Audio is an emerging standard; deployment coverage varies by jurisdiction. Infrastructure readiness (conduit, antenna positions) is the specification target; specific hardware is not specified.]" This is consistent with how A-11 (hearing loop) specifies infrastructure, not hardware.

---

## 4. SYNERGIES (structural patterns emerging from cross-analysis)

### 4.1 Category F now has a clean design logic

Post-D2 revision, Category F covers environmental zoning by sensory modality:

| Item | Modality | Zoning principle |
|---|---|---|
| F-01 | Multi-sensory | Gradient: high → low from entry to occupation |
| F-02 | Olfactory | Zone: fragrance-free in sensitive areas |
| F-03 | Multi-sensory | Transition: graduated re-entry from low to general |
| F-04 | Air quality + ventilation | Zone: filtration, ACH, CO₂ monitoring |
| ~~F-05~~ | ~~Postural~~ | ~~(relocate to G-08 per §1.1)~~ |
| F-06 | Thermal | Zone: ambient temperature management by zone |
| F-07 | Thermal | Transition: heat shock prevention at room boundary |

This creates a conceptual symmetry: F-01/F-03 are gradient/transition principles; F-02/F-04/F-06 are zone specifications; F-07 is the thermal-specific transition parallel to F-03. If F-05 moves to G, renumber F-06 → F-05, F-07 → F-06? Or leave gap? **Recommendation: leave gap.** Renumbering costs cascade changes for marginal benefit.

### 4.2 The "user control" meta-connection

CON-0017 identified "user control over environment" as the single highest-impact provision across 7 populations. H-02 (Individual Environmental Control) is the enabling item. But user control appears in 5 other items independently:

| Item | User control element |
|---|---|
| H-02 | Lighting + temperature per space |
| B-06 | Individual dimming ≥300 lux range |
| F-06 (new) | Individual thermostat per zone |
| A-16 | Occupant-controlled dimming/sound/blackout |
| BIO-04 | Switchable water feature |
| D-09 | No rearrangement without consultation |

H-02 is the governing principle; the others are modality-specific implementations. This hierarchy is implicit but never stated. Part 8 or Part 1 should articulate it: "Individual Environmental Control (H-02) is the governing design principle. Items B-06, F-06, A-16, BIO-04, and D-09 are modality-specific implementations. Where any of these items conflicts with a fixed environmental parameter, the user-control provision takes precedence at Tier 2."

### 4.3 The Tier 0 candidates cluster

FDR identified 4 Tier 0 candidates. CON-0001 identified a fifth. These are specifications where ≥5 population codes converge — candidates for universal application regardless of identified population:

| Source | Provision | Populations |
|---|---|---|
| FDR-T0-01 | Universal reach zone 380–1220 mm | MOB, UPL, DEM, PAIN, OFS, aging |
| FDR-T0-02 | Rest seating on circulation ≤20 m | MOB, OFS, PAIN, DEM, aging, NDV |
| FDR-T0-03 | Retreat/reset room | OFS, PAIN, NDV, NEU, DEM, NDV/MH |
| FDR-T0-04 | Entrance recline seating ≤5 m | OFS, PAIN, MOB, DEM, aging |
| CON-0001 | Loop circulation legibility | DEM, VIS, DBL, IntD, NDV/AUT |

E-10 (rest seating ≤20 m) is already a Part 7 item — FDR-T0-02 confirms it as Tier 0. H-01 (controls 400–1100 mm) partially covers FDR-T0-01 but the universal reach zone is broader (includes storage, shelving, display).

**Synergy:** These 5 provisions should be flagged in Part 1 as Tier 0 universal specifications — items that apply regardless of whether any disability population is identified, because convergence across 5+ populations makes population-specific justification unnecessary. This strengthens the Three-Tier Hierarchy doctrine with concrete examples.

### 4.4 Part 9 gains thermal engineering content

TC-02+TC-03 moving to Part 9 Mechanical Engineering adds passive thermal engineering alongside the existing active systems (HVAC noise, vibration isolation). This strengthens Part 9's scope: it now covers acoustic engineering (existing), electrical engineering (existing), mechanical engineering (existing + TC-02/TC-03), and the evacuation coordination items. The combined TC-02+TC-03 item should sit in §9.1.4 (Mechanical Engineering Items) with a clear cross-reference to F-06 and F-07 as the design-facing specifications these engineering items enable.

---

## 5. QUALITY ISSUES

### 5.1 D2-16 cross-reference errors may be more extensive than documented

D2-16 identifies 4 code errors in the Universal Residential Provisions table. But the table has 11 entries and the code-checking only compared against known Part 7 items. A comprehensive code audit of all matrix tables (Parts 5+6) against the post-D2 Part 7 inventory has not been done.

**Action:** Add to Phase 3 pre-writing checklist: `cross-reference-resolver` run on all matrix tables against confirmed Part 7 inventory (88 items post-D2). This is a Haiku-scale structural task.

### 5.2 Connection register disposition tracking incomplete

D2 Pattern 2 addresses 19 HIGH connections but doesn't record dispositions in the connection register itself. After author approval, each CON-NNNN entry needs its disposition checkbox updated:
- HIGH → item-specification-writer briefing (Phase 3) ✓
- Or: absorbed into D2 decision (note which D2-xx) ✓

9 MODERATE connections are addressed by D2-41 (systematic pass) but individual dispositions not recorded.

**Action:** After D2 approval, update `references/connection-register.md` disposition blocks for all 32 entries.

### 5.3 Gap register items duplicated

Two entries share the ID `GAP-CON-05` (one for Part E conflict formalisation, one for A-09 PAIN co-population). Two entries share `GAP-FDR-01` (bidet spatial spec and OFS shower temperature). IDs must be unique.

**Action:** Deduplicate in Phase 0R or next gap register write. Assign new IDs to the second instance of each duplicate.

---

## 6. SUMMARY OF PROPOSED ADDITIONS TO D2

| ID | Decision | Priority |
|---|---|---|
| D2-41 | PAIN/OFS Systematic Population Audit — standing instruction for Phase 3 | HIGH |
| D2-42 | DELETE all VI-xx legacy references; replace with inline text | MODERATE |
| D2-43 | Replace "MIS" → "NDV/SENS" throughout | MODERATE |
| D2-44 | E-12 is a reference code, not a Part 7 item — add one-line definition | LOW |
| D2-45 | Remove R-STA-02 from Universal Residential Provisions table | LOW |
| D2-46 | A-12 Auracast technology-currency disclosure | LOW |
| D2-47 (revised D2-37) | Retreat/reset/recline: elevate from DEFER to PROVISIONAL — substantive A-16 revision in Phase 3 with recumbent, adjacency, and Tier 0 note | HIGH |
| D2-48 (from §1.1) | F-05 → G-08 relocation (seated-task is furniture/ergonomic, not sensory zoning) | MODERATE |
| D2-49 (from §4.2) | Articulate H-02 user-control hierarchy in Part 1 or Part 8 — governing principle for B-06, F-06, A-16, BIO-04, D-09 | MODERATE (Phase 3 Part 1 writing) |
| — | Fix duplicate GAP IDs (GAP-CON-05, GAP-FDR-01) | Housekeeping |
| — | Update connection register dispositions after D2 approval | Housekeeping |
| — | Add cross-reference-resolver matrix audit to Phase 3 pre-writing | Process |

---

## 7. REVISED ITEM COUNT (if all audit recommendations accepted)

| Cat | Items | Change from D2 |
|---|---|---|
| F | 6 | −1 (F-05 relocated to G-08) |
| G | 8 | +1 (F-05 becomes G-08) |
| **Total Part 7** | **85** | Net zero vs D2 |

---

*End of Systematic Audit*
