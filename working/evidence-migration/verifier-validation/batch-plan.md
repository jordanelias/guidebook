# Grading batch plan (Stage −1 substrate inventory → batch order)

*Prepared while the verifier-validation gate runs. **Execution is gated**: no grading proceeds until the
seeded-plant validation (`plant-set.md` → `result.md`) PASSES. `data/guidebook.db`, 2026-07-19.*

## Stage −1 — readiness of the grading-candidate slugs (deepest substrate first)

| slug | state | cm/ss | PMP walks | extractions | items | graded | readiness |
|---|---|---|---|---|---|---|---|
| **room-acoustic-performance** | RETRACTED | ✓/✓ | 13 | 8 | 13 | **1/13 (A-18)** | **readiest — 12 siblings share the acoustic base** |
| cognitive-wayfinding-design | RETRACTED | ✓/✓ | 0 | 0 | 5 | 0/5 | cm+ss done; needs extraction→grade |
| stair-ramp-threshold-biomechanics | RETRACTED | ✓/✓ | 0 | 0 | 2 | 0/2 | cm+ss done; needs extraction→grade |
| mental-health-built-environment | RETRACTED | ✓/✓ | 0 | 0 | 1 | 0/1 | cm+ss done; needs extraction→grade |
| circadian-lighting-melanopic-edi | RETRACTED | ·/· | 8 | 0 | 2 | 0/2 | has PMP walks but cm/ss unflagged — verify substrate |
| mobility-built-environment | RETRACTED | ✓/✓ | 0 | 0 | **0** | — | **0 items mapped → Stage-0 triage (claim vs container)** |
| school-environment-autism | null | ✓/✓ | 10 | 0 | **0** | — | **0 items mapped → triage; 10 PMP walks orphaned from items** |

## Within room-acoustic-performance — per-item readiness (the first batch)

| item | PMP walks | cells | status |
|---|---|---|---|
| A-18 | 13 | 4 | ✅ GRADED (pilot) |
| **A-02** Acoustic Ceiling Panels (NRC ≥0.85) | **7** | 0 | **readiest ungraded — substrate present** |
| **A-08** HVAC Noise Control (NC-25) | **3** | 0 | **second — substrate present** |
| A-01, A-03, A-04, A-05, A-06, A-07, A-09, A-10b, A-14, A-17 | 0 | 0 | bare — extraction from scratch |

## Batch order (post-gate)

1. **Batch 1 — A-02, A-08** (acoustic, PMP substrate already built): finish-the-derivation, same pipeline as
   A-18, each with the separate guilty-until-proven verifier. Small, high-confidence, proves the batch loop.
2. **Batch 2 — bare acoustic items** (A-01/03/04/05/06/07/09/10b/14/17): extraction→grade; note A-05 already
   had honesty rework this session, so re-confirm rather than redo.
3. **Batch 3 — cognitive-wayfinding (5), stair-ramp (2), mental-health (1)**: cm+ss done; extraction→grade.
4. **Triage track (parallel, not grading)** — the 0-item slugs (mobility-built-environment,
   school-environment-autism) and circadian-lighting's flag/PMP mismatch: Stage-0 classify (provision-claim
   vs data-container) and fix the item↔slug / item↔PMP mapping seams before any grading.

**Cadence:** foreground, small batches, checkpoint each item; a separate verifier clears every cell before
`stated`. Re-run the Part I.b flag queries after each batch to confirm movement.
