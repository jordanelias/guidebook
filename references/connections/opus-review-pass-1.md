# Connection Register — Opus Review Pass 1
**Date:** 2026-04-08
**Model:** Opus 4.6
**Scope:** All 30 PENDING connections

---

## Summary

| Finding type | Count |
|---|---|
| Routing errors | 7 |
| Confidence adjustments recommended | 3 |
| Target items incomplete | 3 |
| Application cluster identified | 1 |
| Entries correct as-is | 20 |

---

## Routing Errors

These connections are filed in the wrong topic directory. The routing rules (CO-0006 §2) specify: file under the topic of the **primary target item**.

| CON-ID | Current routing | Correct routing | Reason |
|---|---|---|---|
| CON-0041 | kitchens-and-workspaces | bathrooms-and-wet-areas | Primary target is residential bathroom matrix entries (thermal differential). Kitchen is not a target. |
| CON-0042 | kitchens-and-workspaces | communication-and-alerts | Primary targets are B-10, K-04 alerting items — not kitchen items. |
| CON-0043 | communication-and-alerts | wayfinding-and-signage | Primary targets are C-items (visual contrast) and D-items (wayfinding). Neither is communication. |
| CON-0102 | communication-and-alerts | cross-cutting | F-04/F-06/F-07/F-08 are environmental comfort items spanning air quality and thermal. Not communication. Spans 4 items across 2 subcategories → cross-cutting per routing rule 3. |
| CON-0012 | wayfinding-and-signage | frameworks-and-methodology | Target is DAR items — a methodology/policy precedent (Italian adattabilità), not wayfinding content. |
| CON-0015 | communication-and-alerts | sensory-environment | F-04 (Air Quality) and F-02 are sensory environment items, not communication items. |
| CON-0111 | wayfinding-and-signage | frameworks-and-methodology | Target is Part 10 DAR, Part 1 Foundations, Part 12 Economics — all methodology/framework content. |

**Action required:** Move connection entries to correct topic files. Update _index.md "Filed in" column.

---

## Confidence Adjustments

| CON-ID | Current | Recommended | Rationale |
|---|---|---|---|
| CON-0009 | MODERATE | HIGH | Kos et al. 2015 (AJOT, Tier 1 RCT) directly establishes energy conservation as OT intervention for OFS. Step elimination is the architectural expression of that intervention. The mechanism is not speculative — it is a direct application of Tier 1 evidence. |
| CON-0016 | SPECULATIVE | MODERATE | Both sides of the conflict are well-documented: TWSI contrast requirements (ISO 23599, Tier 4) and DEM floor pattern avoidance (DSDC, Tier 5/Co-1). The interaction itself is the coordination note — the mechanism is established, not speculative. |
| CON-0096 | MODERATE | HIGH | Multi-jurisdiction evidence across UK (£711m DFG), AU (NDIS), Nordic (uncapped), FR (MaPrimeAdapt'), CA (HATC) all confirm the same structural pattern: all major programmes fund retrofit only. This is a robust finding, not a moderate-confidence inference. |

---

## Target Items Incomplete

| CON-ID | Current target | Recommended target |
|---|---|---|
| CON-0033 | — | Part 5 §5.x (new process specification section), Part 6 residential matrices |
| CON-0034 | — | G-03, G-04, G-05 (bathroom), kitchen items, E-12/E-13 (threshold), A-02/A-08 (corridor) — all MOB wheelchair dimensional provisions |
| CON-0035 | — | Part 5 §5.x (support framework section), Part 9 §9.x (OT assessment quality) |

---

## Application Cluster: Part 5 Process Specification

CON-0033, CON-0034, CON-0035, and CON-0049 form a tightly coupled cluster. All four target Part 5 and converge on the same finding: the guidebook needs a process specification co-primary with the built environment specification.

| CON-ID | Specific contribution to Part 5 |
|---|---|
| CON-0033 | CAPABLE as governing multicomponent intervention model; Sheffield as economic justification |
| CON-0034 | Malmgren Fänge OR 9.50 as dimensional evidence anchor for wheelchair provisions |
| CON-0035 | Support framework, transition planning, family/carer support as co-primary with physical design |
| CON-0049 | Scope decision: support quality > built environment for QoL (Douglas 2024 Tier 1) |

**Recommendation:** Apply all four as a single coordinated Part 5 expansion in one ISW session rather than four separate passes. Load all four connection entries simultaneously. CON-0049 provides the framing; CON-0033 provides the model; CON-0035 provides the components; CON-0034 provides the dimensional anchor.

---

## Individual Entry Reviews — HIGH Confidence PENDING

### CON-0033 — CORRECT (target incomplete)
Confidence HIGH justified: four Tier 1 sources converging on residential assessment protocol. See target items correction and cluster note above.

### CON-0034 — CORRECT (target incomplete)
Confidence HIGH justified: OR 9.50 is a large effect size from Tier 1 quasi-experimental. Single-study basis would normally indicate MODERATE, but the effect size magnitude and direct built-environment relevance justify HIGH.

### CON-0035 — CORRECT (target incomplete)
Confidence HIGH justified: four sources including two Tier 1 qualitative studies + Co-1. See cluster note above.

### CON-0039 — CORRECT
Confidence HIGH justified: strongest multi-stream convergence in the register (DEAF Tier 1, NDV/AUT Tier 1, DEM Tier 2, NEU Tier 3). Routing to entrances-and-circulation acceptable — Category A items are housed there. ISW action (Universal Mode elevation of RT60 ≤0.3 s) is correct.

### CON-0040 — CORRECT
Confidence HIGH justified. Cross-cutting routing correct (spans 4+ categories). The ○ marker disclosure for the synthesised zone matrix is the right call — no single study validates the complete matrix.

### CON-0041 — ROUTING ERROR (see above)
Otherwise correct. HIGH confidence justified by 6,073 deaths/year mortality data. ISW action (≤5°C inter-room differential as P1 safety specification) is correct.

### CON-0042 — ROUTING ERROR (see above)
Otherwise correct. HIGH confidence justified. ISW action (unified multi-channel alerting) is correct and extends CON-0014 appropriately.

### CON-0043 — ROUTING ERROR (see above)
Otherwise correct. HIGH confidence justified — this is an internal consistency correction backed by the guidebook's own LRV BPC. ISW action (propagate ≥50% LRV to all contrast-dependent provisions) is correct.

### CON-0045 — CORRECT
Confidence HIGH justified: confirmed not-found after full multilingual research pass. Routing to health-and-symptom-management acceptable. ISW action (evidence confidence weighting in Part 1 + Part 13 gap disclosure) is correct.

### CON-0046 — CORRECT
Confidence HIGH justified: NDTi/NHS England 2022 is Tier 1 Co-1 peer-reviewed. The shift from "recommended" to "required" is justified by documented systematic harm. Routing to cross-cutting correct.

### CON-0047 — CORRECT
Confidence HIGH justified: CONFIRMED NOT FOUND globally. ISW action (epistemic disclosure) strengthens rather than weakens the guidebook.

### CON-0048 — CORRECT
Confidence HIGH justified: four sources spanning Tier 1 RCT (CAPABLE) to Tier 3 Cochrane (Clemson). ISW action (unified economic continuum presentation) is correct.

### CON-0049 — CORRECT
Confidence HIGH justified: two Tier 1 qualitative studies + CAPABLE RCT. Overlaps substantially with CON-0035 — see cluster note. ISW action (Part 5 process specification) is the single most important scope decision outstanding.

### CON-0102 — ROUTING ERROR (see above)
Otherwise correct. HIGH confidence justified: three F-items with documented HVAC interdependency that creates a coherence gap when specified independently.

---

## Individual Entry Reviews — MODERATE Confidence PENDING

### CON-0005 — CORRECT
MODERATE justified: PAIN flooring evidence is thin (expert consensus). MOB evidence strong but PAIN extension requires clinical rationale link only.

### CON-0006 — CORRECT
MODERATE justified: circadian+MH/OFS clinical relevance clear but direct evidence thin. Routing to entrances-and-circulation acceptable per current B-item convention.

### CON-0008 — CORRECT
MODERATE justified: hyperacusis as FMS symptom (Geisser 2021 Tier 3) is documented but acoustic-specific built-environment impact on PAIN/OFS is not directly studied.

### CON-0009 — CONFIDENCE ADJUSTMENT (see above)
Recommend upgrade MODERATE → HIGH. Otherwise correct.

### CON-0012 — ROUTING ERROR (see above)
Otherwise correct. MODERATE justified for single-jurisdiction statutory precedent.

### CON-0013 — CORRECT
MODERATE justified. Population coding update, no specification change.

### CON-0015 — ROUTING ERROR (see above)
Otherwise correct. MODERATE justified.

### CON-0030 — CORRECT
MODERATE justified: bioRxiv preprint not yet peer-reviewed. Quantified wayfinding uncertainty model is promising but needs validation.

### CON-0032 — CORRECT
MODERATE justified: single scoping review for structural validation; no specification change required.

### CON-0044 — CORRECT
MODERATE is conservative. Foundational theory (Gibson 1979) would normally carry higher weight, but the applied implications (haptic continuity specification) need translation work. MODERATE acceptable.

### CON-0095 — CORRECT
MODERATE justified: regulatory compliance note, jurisdiction-limited.

### CON-0096 — CONFIDENCE ADJUSTMENT (see above)
Recommend upgrade MODERATE → HIGH. Otherwise correct.

### CON-0098 — CORRECT
MODERATE justified: theoretical framework adoption, not direct specification evidence.

### CON-0099 — CORRECT
MODERATE justified: programme data, not specification evidence.

### CON-0111 — ROUTING ERROR (see above)
Otherwise correct. MODERATE justified: emerging convergence.

---

## SPECULATIVE Review

### CON-0016 — CONFIDENCE ADJUSTMENT (see above)
Recommend upgrade SPECULATIVE → MODERATE. Both sides well-documented; the interaction is the coordination concern.

---

## CONSUMED Entries — Spot-Check (10 of 82)

Spot-checked 10 CONSUMED entries for obvious errors: CON-0001, CON-0010, CON-0017, CON-0019, CON-0023, CON-0024, CON-0052, CON-0074, CON-0093, CON-0097.

| CON-ID | Finding |
|---|---|
| CON-0001 | Correct. Universal Mode circulation legibility supported by 5-population convergence. |
| CON-0010 | Correct. Biophilic outdoor convergence across DEM/OFS/NDV/MH. |
| CON-0017 | Correct. H-02 Universal Mode user control supported by 5+ BPC entries. |
| CON-0019 | Correct. Environmental refuge Universal Mode supported by 4-population convergence + PAS 6463 + ASPECTSS. |
| CON-0023 | Correct. Al-Harasis 2025 taxonomy is a significant addition to NDV evidence base. |
| CON-0024 | Correct. Prospect-refuge theory provides non-disability-specific grounding. |
| CON-0052 | Correct. DBL residual hearing → hearing loop cross-reference. |
| CON-0074 | Correct. DEAF glazed junction conflict resolution — matte glazing specification appropriate. |
| CON-0093 | Correct. Ramp gradient → shoulder PAIN prevention mechanism well-documented. |
| CON-0097 | Correct. Wellecke 2022 (Tier 1, n=144) as independent OT validation of visitability priority ordering. |

No errors found in spot-checked CONSUMED entries.

---

## Revision History

| Date | Change | Author |
|---|---|---|
| 2026-04-08 | Pass 1 — all 30 PENDING + 10 CONSUMED spot-check | Opus 4.6 |
