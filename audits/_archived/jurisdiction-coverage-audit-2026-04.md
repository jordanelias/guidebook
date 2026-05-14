# Jurisdiction Coverage Audit — Phase 2A
**Generated:** 2026-04-23
**Scope:** All search-log files (76 topic + 14 population = 90 entries)
**Purpose:** Establish baseline for jurisdiction coverage across BPC research pipeline

---

## Executive Finding

**Per-jurisdiction tracking (Axis 2) essentially does not exist.** Search logs track by language (Axis 1) only. Of ~82 audited search-log files, only ~17 contain any jurisdiction-level metadata, and none track the full 46-jurisdiction status record required by project-standards.md.

This means Phase 2B-E is not "backfill" — it is **new construction** of the jurisdiction tracking layer.

---

## Audit Summary

| Category | Count | % |
|---|---|---|
| OK (≥10 languages searched, 0 NOT-RUN) | ~16 | 20% |
| PARTIAL (some languages, some NOT-RUN) | ~43 | 52% |
| EMPTY (no language data) | ~18 | 22% |
| With any jurisdiction tracking | ~17 | 21% |
| With full 46-jurisdiction tracking | 0 | 0% |

### Language Axis (Axis 1) Status
- **19 canonical languages** (14 original + 5 CO-0005)
- Most search logs track 14 languages max (CO-0005 languages AR/HI/ID/SW/BN not yet integrated)
- ~43 slugs have ≥3 NOT-RUN languages (early-close gate victims — gate now removed)
- Most NOT-RUN languages are NL, ES, PT, KO, IT (blocked by early-close gate)

### Jurisdiction Axis (Axis 2) Status
- **46 canonical jurisdictions** per CO-0005
- No search-log file has per-jurisdiction status records for all 46
- Jurisdiction data exists only implicitly (e.g., EN status references "ADA, BS 8300, Part M")
- No `co1_attempted`, `tier5_attempted`, `tier6_attempted` per-jurisdiction records anywhere

---

## EMPTY Search Logs (no language data — 18 slugs)

These require full multilingual-research runs from scratch:

| Slug | Topic | Item Impact |
|---|---|---|
| assistive-listening-systems | communication-and-alerts | A-10, A-11 |
| bathroom-typology-global-south | bathrooms-and-wet-areas | Global South supplement |
| case-study-economics-financial-data | economics | Part 11 |
| chronic-pain-built-environment | health-and-symptom-management | PAIN population |
| circadian-lighting-melanopic-edi | sensory-environment | B-01 |
| co1-housing-research-global-south | frameworks-and-methodology | Co-1 evidence |
| construction-cost-data | economics | Part 11 |
| crpd-implementation-built-environment | frameworks-and-methodology | Part 1 |
| deaf-classroom-reverberation-time | communication-and-alerts | A-04 |
| fatigue-spectrum-built-environment | health-and-symptom-management | OFS population |
| hearing-impairment-built-environment | population-general | DEAF population |
| ot-built-environment-interface | frameworks-and-methodology | Part 9 |
| post-occupancy-evaluation-global | frameworks-and-methodology | Part 12 |
| residential-accessible-home-case-studies | frameworks-and-methodology | Part 12 |
| sensory-space-global-south | sensory-environment | Global South supplement |
| therapeutic-lighting-design | sensory-environment | B items |
| thermoregulation-built-environment | health-and-symptom-management | F-07, F-08 |
| visual-fire-alarm-seizure-safety | sensory-environment | B-10 |

---

## Worst NOT-RUN (≥5 languages NOT-RUN — 30 slugs)

| Slug | SEARCHED | THIN | NOT-RUN | Item Impact |
|---|---|---|---|---|
| reach-range-and-accessible-controls | 3 | 1 | 10 | H-01 to H-04 |
| cross-population-case-studies | 1 | 5 | 8 | Part 5 |
| sensory-room-user-control | 1 | 0 | 13 | A-16 |
| residential-entry-and-threshold | 8 | 0 | 6 | E-06 |
| threshold-and-level-access | 8 | 0 | 6 | E-06 |
| fold-down-grab-bar-specification | 3 | 4 | 5 | K-01 |
| neurodivergent-built-environment | 9 | 0 | 5 | NDV population |
| upper-limb-impairment-built-environment | 9 | 0 | 5 | MOB/UPL population |
| visual-impairment-built-environment | 9 | 0 | 5 | VIS population |
| (+ 21 more at 5 NOT-RUN) | | | | |

---

## Priority Matrix — What to Fix First

### Priority 1: EMPTY + High Item Impact (7 slugs)
These have zero research AND directly feed Part 4 items:
1. `circadian-lighting-melanopic-edi` → B-01
2. `assistive-listening-systems` → A-10, A-11
3. `deaf-classroom-reverberation-time` → A-04
4. `visual-fire-alarm-seizure-safety` → B-10
5. `therapeutic-lighting-design` → B items
6. `chronic-pain-built-environment` → PAIN population
7. `fatigue-spectrum-built-environment` → OFS population

### Priority 2: High NOT-RUN + High Item Impact (5 slugs)
These have partial research but 5+ languages missing AND feed key items:
1. `reach-range-and-accessible-controls` → H-01 to H-04 (10 NOT-RUN!)
2. `sensory-room-user-control` → A-16 (13 NOT-RUN!)
3. `residential-entry-and-threshold` → E-06 (6 NOT-RUN)
4. `threshold-and-level-access` → E-06 (6 NOT-RUN)
5. `fold-down-grab-bar-specification` → K-01 (5 NOT-RUN)

### Priority 3: OK Languages + No Jurisdiction Tracking (16 slugs)
These have ≥10 languages searched and 0 NOT-RUN, but need jurisdiction-level tracking added:
- `threshold-door-hardware`, `room-acoustic-performance`, `accessible-circulation-geometry`, 
  `mobility-built-environment`, `dementia-built-environment`, `deaf-spatial-design`,
  `accessible-bathroom-and-grab-bar`, and ~9 more

### Priority 4: Population-level files with NOT-RUN (8 files)
Population BPC search logs (NDV, VIS, DBL, DEM, etc.) all have 5 NOT-RUN languages.

---

## Structural Finding: Axis 1 vs Axis 2 Gap

The project-standards.md rule (2026-03-19) requires:
> Per-jurisdiction tier coverage record required: status (SEARCHED|THIN|NO-DATA|NOT-RUN), 
> co1_attempted, tier5_attempted, tier6_attempted.

**Current state:** This structure does not exist in any search-log file. All tracking is by language only.

**Recommendation:** Rather than retrofitting 90 search-log files with 46 jurisdiction records each (= 4,140 individual status entries), the jurisdiction tracking should be built incrementally through Phase 2B-E research passes. Each Phase 2 research session should:
1. Complete missing languages (Axis 1 backfill — clear NOT-RUN)
2. Add per-jurisdiction status block to the search-log file (Axis 2 new construction)
3. Update BPC consensus finding if new jurisdiction data changes synthesis

Estimated work: ~35 sessions to reach full coverage (per workplan Phase 2B-E estimate of 18-24 sessions + overhead).

---

## Recommended Session Sequence for Phase 2B

Start with Priority 1 EMPTY slugs that feed Part 4 items. Each session targets 2-3 slugs:

| Session | Slugs | Category Impact |
|---|---|---|
| 2B-1 | circadian-lighting-melanopic-edi, therapeutic-lighting-design | Cat B (Lighting) |
| 2B-2 | assistive-listening-systems, deaf-classroom-reverberation-time | Cat A (Acoustics) |
| 2B-3 | visual-fire-alarm-seizure-safety | Cat B (Alerts) |
| 2B-4 | chronic-pain-built-environment, fatigue-spectrum-built-environment | PAIN/OFS population |
| 2B-5 | reach-range-and-accessible-controls (10 NOT-RUN) | Cat H (Controls) |
| 2B-6 | sensory-room-user-control (13 NOT-RUN) | A-16 |
| 2B-7 | residential-entry-and-threshold, threshold-and-level-access | Cat E (Entrances) |
| 2B-8 | fold-down-grab-bar-specification + acoustics backfill | Cat K + A |
