# Citation Tagging Protocol — Step 2 of Citation Infrastructure
<!-- Generated 2026-04-19 — to be executed across multiple desktop sessions -->

## Overview

**Goal:** Populate `ref_ids` for all 1,382 claims in `claim-reference-join.json` so every claim on the website can show a Wikipedia-style footnote linking to a full citation.

**Prerequisites (both complete):**
- Step 1: `global-reference-registry.md` + `.json` — 531 unique references ✅
- Step 3: `claim-reference-join.md` + `.json` — 1,382 claims enumerated with PENDING status ✅

**Workflow per session:**
1. Select a scope (one Part, or one Part 4 category, or one topic cluster)
2. For each claim in that scope:
   a. Identify the BPC file(s) covering the topic
   b. Find the supporting source in that BPC's Key sources table
   c. Look up the global REF-ID in `global-reference-registry.md`
   d. Add REF-ID(s) to the claim's `ref_ids` array
   e. Update `status` to `TAGGED`
3. If no supporting reference found → set `status: ORPHANED` (flag for review)
4. If claim is definitional/cross-reference → set `status: DEFERRED`
5. Commit the updated JSON with scope summary

## Claim count by Part (work estimate)

| Part | Claims | Est. sessions | Priority |
|---|---|---|---|
| Part 1 | 7 | 0.1 | P3 — mostly framework |
| Part 2 | 83 | 1 | P2 — population facts |
| Part 3 | 42 | 0.5 | P2 — conflict resolution |
| **Part 4** | **558** | **4–6** | **P1 — item specifications (core)** |
| Part 5 | 79 | 1 | P2 — conflict res application |
| Part 6 | 115 | 1.5 | P2 — residential matrices |
| Part 7 | 111 | 1.5 | P2 — non-residential matrices |
| Part 8 | 116 | 1.5 | P2 — engineering targets |
| Part 9 | 10 | 0.2 | P3 — mostly process |
| Part 10 | 23 | 0.3 | P3 — DAR specs |
| Part 11 | 191 | 2 | P2 — economics figures |
| Part 12 | 47 | 0.5 | P2 — case study facts |
| **TOTAL** | **1,382** | **~14 sessions** | |

## Session execution order (recommended)

**Phase 2a — P1 (Part 4 core specs):**
- Session 1: Part 4 Category A (acoustics) — ~60 claims
- Session 2: Part 4 Category B-C (lighting, surfaces) — ~100 claims
- Session 3: Part 4 Category D-E (spatial, circulation) — ~120 claims
- Session 4: Part 4 Category F-G (sensory, fixtures) — ~90 claims
- Session 5: Part 4 Category H-K (controls, upper limb, outdoor) — ~80 claims
- Session 6: Part 4 remaining + verification pass — ~100 claims

**Phase 2b — P2 (supporting Parts):**
- Session 7: Part 2 (disability categories) — ~83 claims
- Session 8: Part 3 + Part 5 (conflict resolution) — ~120 claims
- Session 9: Part 6 (residential matrices) — ~115 claims
- Session 10: Part 7 (non-residential matrices) — ~111 claims
- Session 11: Part 8 (engineering targets) — ~116 claims
- Session 12: Part 11 (economics) — ~191 claims
- Session 13: Part 12 (case studies) — ~47 claims

**Phase 2c — P3 (residuals):**
- Session 14: Parts 1, 9, 10 + ORPHANED resolution — ~40 claims

## Status values

| Status | Meaning |
|---|---|
| `PENDING` | Not yet tagged (default) |
| `TAGGED` | Ref IDs assigned; first pass complete |
| `VERIFIED` | Second-pass check: cited refs genuinely support claim |
| `ORPHANED` | No supporting reference found — spec may be derived/unreferenced |
| `DEFERRED` | Not a citable claim (definitional, cross-ref, calculation) |

## Inline tagging syntax (optional, deferred)

**Current decision:** Citation tags live in the JSON join table only, not inline in Part files. This keeps the source text clean and makes the citation layer machine-readable without polluting the prose.

**Phase B parsers** read both files and render `[CLAIM-ID → REF-ID]` links at the matching line/position.

**Alternative (if inline tags required later):** Insert HTML comments at claim locations: `<!-- cite: REF-00234 -->`. This is reversible; do not add unless Phase B parser design requires it.

## Quality gates

**Per-session checkpoint:**
- All claims in scope reach non-PENDING status
- ORPHANED rate ≤15% (higher indicates either spec-without-evidence or missed BPC)
- No claim has both TAGGED and empty `ref_ids` (invariant check)

**Final completion gate (Phase A addition → closed):**
- 0 PENDING claims
- ORPHANED claims logged in gap register for Phase B content review
- ≥95% of claims have ≥1 Tier 1–3 supporting reference

## Handoff to Phase B

When Step 2 is complete, Phase B parsers can:
1. Read `parts/v10/partNN.md` for specification text
2. For any claim, look up its `CLAIM-ID` in `claim-reference-join.json`
3. Get `ref_ids` array
4. Resolve each REF-ID via `global-reference-registry.json`
5. Render footnote with full citation + DOI link

**Backend query examples:**
- "All claims citing REF-00234" → filter claim-ref join by ref_ids contains
- "Orphaned claims in Part 4" → filter by part=4 and status=ORPHANED
- "Claims without Tier 1 evidence" → join ref_ids to registry, check all tiers >1
