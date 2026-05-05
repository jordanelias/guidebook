# Item-Code Discrepancy Audit
**Date:** 2026-05-05 06:50
**Session:** B2-S4-citation-corrections
**Scope:** All connection_targets (510 rows) cross-referenced against Part 4 canonical item codes (83 items)

---

## Summary

| Metric | Count |
|---|---|
| Canonical Part 4 items | 83 |
| Unique item codes in connections | 64 |
| In connections, NOT in Part 4 | 9 |
| In Part 4, NOT in any connection | 28 |
| Malformed targets | 3 |
| Free-text with embedded phantom codes | 1 |

---

## Finding 1: Phantom item codes (9 codes referenced in connections but absent from Part 4)

### Critical (≥3 connection references)

**F-07 (Thermal Zoning)** — 7 connections reference this item. Not in Part 4.
- CON-0041, CON-0101, CON-0102, CON-0107, CON-0119, CON-0142, CON-0191, CON-0224
- Scope: individual supplemental radiant heating, three-zone thermal system, 18–22°C working target
- Resolution: CREATE F-07 in Part 4, or reassign connections to existing items (F-04 Air Quality or new thermal category)

**F-08 (Thermal Transition)** — 4 connections reference this item. Not in Part 4.
- CON-0101, CON-0102, CON-0107, CON-0108
- Scope: entry vestibule thermal buffer ≥2m depth
- Resolution: CREATE F-08 in Part 4, or merge with F-07

**K-05 (Thermal Comfort Assessment)** — 3 connections reference this item. Created in B2-S3 session but NOT added to Part 4 file.
- CON-0184, CON-0224, CON-0233
- Resolution: ADD K-05 heading to parts/88_to_90/part05-k_v9-0_2026-03-20.md

**B-12 (Daylight)** — 3 connections reference this item. Not in Part 4.
- CON-0196, CON-0214, CON-0215
- Scope: daylight provision, overlap with circadian lighting (B-01) and biophilic design
- Resolution: CREATE B-12 or consolidate into B-09 (Maximisation of Natural Light)

### Moderate (1–2 connection references)

**G-08 (Storage)** — 3 connections (CON-0005, CON-0038, CON-0129). Storage layout as bracing surface, PAIN storage height 750-1050mm.
- Resolution: CREATE G-08 or merge into G-05 (Adjustable-Height Work Surfaces)

**E-14 (Entrance Rest Seating)** — 2 connections (CON-0054, CON-0108). Draft EXISTS at parts/v10/e14-entrance-rest-seating.md but NOT in Part 4 main file.
- Resolution: MERGE v10 draft into Part 4 consolidated file

**E-13** — 1 connection (CON-0108). No specification exists anywhere.
- Resolution: INVESTIGATE — may be a numbering error (E-14 exists, E-13 does not)

**G-09** — 1 connection (CON-0213). No specification exists.
- Resolution: INVESTIGATE — CON-0213 description mentions bathroom/bedroom proximity

### Typo

**B-0** — 1 connection (CON-0017, CONSUMED). Clearly B-01 or B-10.
- Resolution: FIX to correct code (context: "User control over environment" → likely H-02)

---

## Finding 2: Orphaned Part 4 items (28 items with zero connections)

These items have no cross-item or cross-population connections. Some are expected (standalone), but the following warrant review:

**Potentially missing connections:**
- A-03 (Acoustic Door STC ≥35) — should connect to DEAF items
- A-14 (Double-Leaf Partition STC ≥50) — should connect to A-03
- A-15 (Acoustic Differentiation for VIS) — should connect to VIS wayfinding items
- D-01 (Loop Floor Plan) — should connect to DEM wayfinding items
- E-15 (Changing Places Facility) — should connect to MOB, ceiling hoist items
- I-01 (Hardware Throughout) — should connect to MOB/UPL items

**Likely standalone (no connection expected):**
- A-05 (Carpet), A-06 (Fabric Panels), A-12 (Auracast), A-17 (Upholstered Seating)
- B-02, B-03, B-05, B-08, B-09, B-11
- C-02, C-05, C-06
- D-03, D-07, D-10, D-11
- E-02, E-04, E-11
- G-01

---

## Finding 3: Malformed targets (3)

| Target | CON-ID | Should be |
|---|---|---|
| `A-16 door spec` | CON-0150 | `A-16` (remove free text) |
| `B-01 circadian lighting` | CON-0241 | `B-01` (remove free text) |
| `F-01 zone boundaries` | CON-0043 | `F-01` (remove free text) |

---

## Finding 4: Embedded phantom code

CON-0246 target contains `I-08` in free text. I-08 does not exist (I-series goes I-01 to I-04). Likely a reference to an ASI code, not a guidebook item code.

---

## Finding 5: E-series numbering gap

E-01 through E-11 exist. E-15 exists. E-12, E-13 do not exist. E-14 exists only as v10 draft.
- E-12: not referenced anywhere — gap in numbering sequence
- E-13: referenced in CON-0108 but no specification exists
- E-14: v10 draft exists, not in Part 4 main
- E-15: in Part 4 main

This suggests E-12 through E-14 were planned but never created (except E-14 draft). The skip to E-15 may indicate items were created out of sequence.

---

## Recommended actions (priority order)

1. **CREATE** F-07, F-08 in Part 4 (7+4 connection refs — highest impact)
2. **ADD** K-05 heading to Part 4 file (already specified in session, 3 pending connections)
3. **MERGE** E-14 v10 draft into Part 4 main file
4. **RESOLVE** B-12 — create or consolidate into B-09
5. **RESOLVE** G-08 — create or merge into existing G-item
6. **FIX** B-0 → correct item code in connection_targets
7. **FIX** 3 malformed targets (strip free text)
8. **INVESTIGATE** E-13, G-09 — determine if items need creation
9. **REVIEW** 28 orphaned items for missing connections (6 flagged as potentially missing)
