# Opus Synthesis Queue
**Original:** 2026-03-29 · **Cleaned:** 2026-05-08
**Canonical plan:** workplan-co0007-v4.md (Stage C)
**Completed work excised to:** workplan/deprecated/opus-synthesis-queue-completed-2026-05-08.md

---

## Current Status

| Category | Count |
|---|---|
| Original queue (13 slugs) | ALL COMPLETE (O1-O10, 2026-03-29) |
| CO-0005 P1 (6 slugs) | ALL COMPLETE (2026-04-07) |
| CO-0005 P2/P3 expansion reviews | **6 potentially pending** (see below) |
| Blocked stubs | 2 (research not yet scheduled in v4) |

**Total synthesized:** 63+ slugs (21 pre-queue + 42 queue + schema pass)
**Potentially pending:** 8 items (6 expansion reviews + 2 blocked stubs)

---

## Potentially Pending — CO-0005 P2/P3 Expansion Reviews

These slugs have original Opus synthesis (2026-03-29) but CO-0005 expanded their evidence base. The expansion review determines whether new jurisdiction/population evidence is additive or requires revision to the existing synthesis. **Trigger conditions reference CO-0005 Phase 2/3 research completion — verify whether those research sessions occurred before scheduling.**

| Slug | Type | Review question | Trigger | Original synthesis |
|---|---|---|---|---|
| `entrances-and-circulation/threshold-door-hardware` | P2 expansion | New jurisdiction evidence additive or revision? | After CO-0005 Phase 3-A LOG | YES 2026-03-29 (PARTIAL-RETAINED) |
| `health-and-symptom-management/pain-ofs-built-environment-design` | P2 expansion | Expansion review — additive or revision? | After Phase 3-B LOG | YES 2026-03-29 (PROVISIONAL-RETAINED) |
| `sensory-environment/acoustics-speech-intelligibility-disability` | P2 expansion | ALT solutions for low-resource settings | After Phase 3-C LOG | YES (date unclear) |
| `population-general/dementia-built-environment` | P2 expansion | Global South evidence vs existing synthesis | After Phase 3-D LOG | YES 2026-03-29 |
| `population-general/intellectual-disability-built-environment-design` | P2 expansion | Communal/family care vs Western individual-unit assumptions | After Phase 3-E LOG | YES 2026-03-29 |
| `frameworks-and-methodology/post-occupancy-evaluation-global` | P3 new | What performs/fails/unknown in Global South contexts | After CO-0005 Phase 4 LOG | File exists (unverified) |

**Action required:** Check CO-0005 Phase 2/3/4 research log status. If research is complete, schedule Opus expansion review sessions. If research hasn't started, these are blocked on CO-0005 research, not on Opus availability.

---

## Blocked — Cannot Synthesize (research not scheduled in v4)

| Slug | Reason | v4 mapping |
|---|---|---|
| `economics/case-study-economics-financial-data` | STUB — no research completed | v4 C9 (economics prose) |
| `frameworks-and-methodology/accessible-design-failures-poor-performance` | STUB — no research completed | v4 C9 (cross-cutting prose) |

These require research before synthesis. Schedule as part of v4 C9 (Opus sessions).

---

## Opus Session Protocol

1. Switch model picker to Opus 4.6
2. Load queue file + batch's slug files via `batch_read`
3. For each slug: read full BPC entry → synthesize → write `**Opus synthesis:** YES [OPUS-SYNTHESIS]` marker + consensus finding + key evidence hierarchy
4. Commit updated slugs
5. Update this file
