# Item Specification Consolidation Manifest
**Date:** 2026-05-05
**Session:** B2-S4-citation-corrections
**Status:** SQLite COMPLETE. Part 4 file modifications PENDING.

## Summary
88 items → 65 items (−23). All connection_targets remapped in SQLite. Part 4 file edits to be performed in subsequent sessions.

---

## Changes by file

### part05-a (9 remaining from 17)

| Item | Action | Absorbed into | Key content to migrate |
|---|---|---|---|
| A-01 | KEEP | — | — |
| A-02 | EXPAND | — | Absorbs A-06 (fabric wall panels NRC ≥0.70) + A-07 (flutter echo as design note). Rename: "Acoustic Absorption Surfaces (NRC ≥0.85 Ceiling, ≥0.70 Wall)" |
| A-03 | EXPAND | — | Absorbs A-14 (double-leaf partition STC ≥50). Rename: "Acoustic Separation (STC ≥35 Door, ≥50 Partition)" |
| A-04 | KEEP | — | — |
| A-05 | KEEP | — | — |
| A-06 | STRIKE | A-02 | Wall panel NRC spec, reflection point placement |
| A-07 | STRIKE | A-02 | Flutter echo design note (parallel surface avoidance) |
| A-08 | EXPAND | — | Absorbs A-09 (vibration isolation, floating plant room) + A-13 (no sound masking prohibition). Rename: "HVAC Acoustic and Vibration Control" |
| A-09 | STRIKE | A-08 | Floating plant room spec, resilient mounting |
| A-10 | EXPAND | — | Absorbs A-11 (room perimeter loop) + A-12 (Auracast). Rename: "Assistive Listening Technology" |
| A-11 | STRIKE | A-10 | Room perimeter loop spec, spill management |
| A-12 | STRIKE | A-10 | Auracast infrastructure readiness |
| A-13 | STRIKE | A-08 | No sound masking prohibition → note in HVAC item |
| A-14 | STRIKE | A-03 | Double-leaf partition STC ≥50 spec |
| A-15 | KEEP | — | — |
| A-16 | EXPAND | — | Absorbs D-05 (focus rooms, breakout alcoves). Rename: "Low-Stimulation Spaces (Sensory Room, Focus Room, Breakout Alcove)" |
| A-17 | RECLASSIFY | G-09 | Move to G-category as "Upholstered Seating." Remove from A-file, add to GHI-file. |

### part05-b (6 remaining from 12)

| Item | Action | Absorbed into | Key content to migrate |
|---|---|---|---|
| B-01 | EXPAND | — | Absorbs B-11 (warm CCT ≤2700K evening) + B-12 (melanopic EDI daylight quality). Rename: "Circadian-Effective Light (≥250 Melanopic EDI, Daytime + Evening)" |
| B-02 | KEEP | — | — |
| B-03 | STRIKE | B-04 | Fluorescent prohibition → sub-clause in B-04 |
| B-04 | EXPAND | — | Absorbs B-03 (no fluorescent) + B-07 (indirect/cove as design note). Rename: "Luminaire Quality (Flicker-Free, Non-Fluorescent, Indirect Preferred)" |
| B-05 | KEEP | — | — |
| B-06 | STRIKE | H-02 | Individual dimming ≥300 lux range → spec within H-02 |
| B-07 | STRIKE | B-04 | Indirect/cove lighting → design note in B-04 |
| B-08 | STRIKE | C-04 | Matte floors ≤30 GU → spec within C-04 |
| B-09 | KEEP | — | — |
| B-10 | KEEP | — | Flag: code-standard, coordination notes only |
| B-11 | STRIKE | B-01 | Warm CCT evening → evening sub-spec in circadian item |
| B-12 | STRIKE | B-01 | Melanopic EDI daylight → daylight sub-spec in circadian item |

### part05-cd (4 remaining from 6+6=12)

| Item | Action | Absorbed into | Key content to migrate |
|---|---|---|---|
| C-01 | KEEP | — | — |
| C-02 | KEEP | — | — |
| C-03 | EXPAND | — | Absorbs C-06 (plain flooring). Rename: "Pattern-Free Surfaces (Plain Flooring and Walls)" |
| C-04 | EXPAND | — | Absorbs C-05 (DEM low contrast) + B-08 (matte ≤30 GU). Rename: "Surface Contrast and Reflectance Management" |
| C-05 | STRIKE | C-04 | DEM inverse contrast rule |
| C-06 | STRIKE | C-03 | Near-duplicate of C-03 |
| D-01 | KEEP | — | — |
| D-02 | KEEP | — | — |
| D-03 | KEEP | — | — |
| D-04 | KEEP | — | — |
| D-05 | STRIKE | A-16 | Focus rooms, breakout alcoves → absorbed into A-16 |
| D-06 | KEEP | — | — |
| D-07 | KEEP | — | — |
| D-08 | KEEP | — | — |
| D-09 | STRIKE | — | Operational/FM instruction, not design. Move to commissioning brief. |
| D-10 | KEEP | — | — |
| D-11 | KEEP | — | — |

### part05-e (9 remaining from 13)

| Item | Action | Absorbed into | Key content to migrate |
|---|---|---|---|
| E-01 | EXPAND | — | Absorbs E-02 (platform lift as fallback sub-spec) |
| E-02 | STRIKE | E-01 | Platform lift → "where full lift not achievable" clause |
| E-03 | KEEP | — | — |
| E-04 | STRIKE | — | Code-standard. Not design-relevant. |
| E-05 | KEEP | — | — |
| E-06 | KEEP | — | Note: file has duplicates at L305-412 — dedup required |
| E-07 | KEEP | — | — |
| E-08 | KEEP | — | — |
| E-09 | KEEP | — | — |
| E-10 | EXPAND | — | Absorbs E-14 (entrance seating as location sub-spec). Rename: "Rest Seating Provision (Routes ≤20m + Entrance ≤5m)" |
| E-11 | KEEP | — | — |
| E-14 | STRIKE | E-10 | Entrance rest seating → entrance sub-spec |
| E-15 | STRIKE | — | Code-standard (UK). Not core design. |

### part05-fg (6 remaining from 8)

| Item | Action | Absorbed into | Key content to migrate |
|---|---|---|---|
| F-01 | EXPAND | — | Absorbs F-03 (graduated re-entry as sensory room sub-case) |
| F-02 | EXPAND | — | Absorbs F-06 (whole-building governance section added) |
| F-03 | STRIKE | F-01 | Graduated re-entry → sub-case of sensory gradient |
| F-04 | KEEP | — | Note: thermal stability specs overlap F-07/F-08 — review at prose stage |
| F-05 | KEEP | — | — |
| F-06 | STRIKE | F-02 | Whole-building fragrance-free → governance section in F-02 |
| F-07 | KEEP | — | — |
| F-08 | KEEP | — | — |

### part05-ghi (9+5+4=18 remaining)

| Item | Action | Absorbed into | Key content to migrate |
|---|---|---|---|
| G-01–G-08 | KEEP | — | — |
| G-09 | NEW | — | Reclassified from A-17 (Upholstered Seating) |
| H-01 | KEEP | — | — |
| H-02 | EXPAND | — | Absorbs B-06 (individual dimming ≥300 lux range as lighting sub-spec) |
| H-03–H-05 | KEEP | — | H-05 flag: safety/static form, lower design interest |
| I-01–I-04 | KEEP | — | — |

### part05-j (4 remaining, unchanged)

J-01 through J-04: no changes.

---

## Execution plan for file modifications (subsequent sessions)

Each file requires:
1. Delete struck item sections (remove ### heading through next ### heading)
2. Expand parent items: add absorbed specs to Specifications list, update Applicable Groups, update Cross-reference, update title
3. For reclassifications: cut from source file, paste into target file
4. E-file: dedup E-06 through E-09 simultaneously
5. GHI-file: resequence H-05 (currently after I-03)

Estimated: 3–4 sessions at file-modification effort level.

---

## Connection_targets status

SQLite remapping COMPLETE. 31 remapped, 15 deduplicated, all struck codes cleared.
Unique targets reduced: 203 → 188.
