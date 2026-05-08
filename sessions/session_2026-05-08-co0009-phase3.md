# Session: 2026-05-08 — CO-0009 Complete + C1 Migration + C3 Calibration Gate (partial)
**Model:** Opus 4.6
**session_close:** 2026-05-08 21:10
**next_action:** C3 calibration gate: 2 more items needed (A-04 medium-sensory, B-10 safety-critical) to complete 5-point calibration. Then revise C3 budget per gate results. Preliminary assessment: median ≤0.75 sessions → REVISE DOWNWARD.
**blockers:** None.

## CO-0009 — COMPLETE (~8 sessions)
All 5 phases done. Pipeline validated end-to-end on I-01. Workplan v4 integrated.

## C1 Migration — COMPLETE
Both DBs substantially populated. Key gains:
- Website DB: +715 doctrine_specification, +181 specialist_specification, +42 specialist_stage_scope, +124 performance_criterion, 141/141 summaries, 92 room_dar_provision, 14 room_conflict
- Tracking DB: 81 BPC slugs, 642 evidence_sources, 1401 source_slug_links, 97 bpc_metadata, 245 connections, 507 connection_targets
- Bug fixed: migrate_slugs.py misinterpreting global-reference-registry
- Script: scripts/db/c1_fill_joins_and_metadata.py

## C3 Calibration Gate — PARTIAL (3/5 items)

### Data points

| Item | Complexity | Pops | Gaps | Pipeline mode | Estimated full session cost |
|---|---|---|---|---|---|
| I-01 | Simple (hardware) | 4 | 8 | Full (8 steps) | 0.5 |
| E-03 | Medium (structural ramp) | 3 | 11 | Abbreviated (4 steps) | ~0.65 |
| G-04 | Complex (bathroom/room) | 4 | 10 | Abbreviated (4 steps) | ~0.75 |

### Preliminary calibration

Median estimated session cost: **~0.65 sessions/item** (≤0.75 threshold → REVISE DOWNWARD per §9.8).

Projected C3 pipeline pre-pass for 86 items (30 simple / 40 medium / 16 complex):
- 30 × 0.5 + 40 × 0.65 + 16 × 0.85 = 15 + 26 + 13.6 = **~55 sessions**
- Add 25-35 for content authoring = **80-90 sessions total C3** (was 70-172)

Remaining calibration items needed: A-04 (medium-sensory), B-10 (safety-critical).

### Gap pattern observations
- FDA-Q2 (population absent) and Economics-C2/C3/C5 produce the most gaps across all items
- SCI absent from applicable groups is systemic (I-01, E-03, G-04)
- Evidence stratum UNSTATED is systemic — no items have stratum annotations
- Economics lifecycle framing absent on all HIGH retrofit items

## All commits this session
| # | SHA | Content |
|---|---|---|
| 1–9 | various | CO-0009 Phases 3-5 |
| 10 | fec0bce | C1 migration: website joins + tracking slugs/bpc/connections |
| 11 | 3c59780 | C1 fix: correct slugs + evidence_sources |
| 12 | a9721f9 | Session file |
| 13 | c375681 | C3 calibration: E-03 + G-04 |
| 14 | (this) | Final session file |

## Tracking DB state: 33 gaps across 4 items
| Section | Gaps | Categories |
|---|---|---|
| I-01 | 8 | AUDT, CR, MX, CD, RP |
| E-01 | 4 | EC, AUDT |
| E-03 | 11 | MX, CD, AUDT, RP, EC |
| G-04 | 10 | AUDT, RP, EC, MX |

## Open for next session
1. Complete C3 calibration gate: A-04 + B-10 pipeline runs (2 items)
2. Revise C3/Stage C/project budget based on 5-point calibration
3. Start C3 production pipeline (or C2 original skills if those are needed first)
