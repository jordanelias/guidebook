---
name: connection-scout
description: >
  Identify connections in the evidence base not yet reflected in the guidebook. Two modes:
  Internal (scans BPC, gap register, session outputs for cross-population overlaps and
  siloed solutions) and External (searches for published cross-references between existing
  BPC sources). ALWAYS use when: looking for cross-population connections, finding evidence
  overlaps, identifying siloed design solutions, or at edition boundaries. Trigger on:
  "find connections", "cross-population scan", "evidence connections", "what links exist".
---

<!-- GOVERNED BY PROJECT INSTRUCTIONS — execution copy only. PI definition governs on conflict. -->
<!-- Updated: CO-0006 2026-04-08 — output restructured to topic-directory architecture -->

**Model:** Opus 4.6 (identification) · Sonnet 4.6 (writes)
**GitHub backend:** `jordanelias/guidebook` · `main`
**Output structure:** `references/connections/{topic}/connections.md` + `references/connections/_index.md`
**Called by:** workplan-orchestrator (edition boundary); literature-review-planner (on demand); user (explicit request)
**Never substitutes for `multilingual-research`.** Operates on assembled outputs, not raw search.

## Purpose

Identify connections that exist in the evidence base but are not yet reflected in the guidebook. Two modes:

**Internal mode:** Scans existing BPC entries, OPEN gap register items, and session research outputs. Finds: design solutions siloed in one population's section that evidence supports for others; gap items sharing root cause resolvable by single spec change; item specifications in one category resolving gaps in another; cross-population overlaps described independently but not synthesised.

**External mode:** Scans current literature via web search. Finds: evidence from adjacent fields not yet applied (ergonomics, environmental psychology, gerontology, sensory science, trauma-informed design, inclusive pedagogy); emerging cross-population research; novel design principles.

Both modes may run in a single session. Internal always before external — internal corpus defines the frontier.

## Inputs

- `references/bpc/{topic}/{slug}.md` — all BPC entries (via slug-registry lookup)
- `gap_register.md` — OPEN items only
- Session research outputs (assembled, not chunked)
- For external mode: web search access

## Process

1. **Internal scan:** Read all BPC entries. For each population code pair: does evidence for A have unremarked implications for B? For each OPEN gap: does another item's spec resolve it? For each category: does evidence in X inform a gap in Y?

2. **Cross-population synthesis:** Rate each candidate: HIGH (directly supported by existing Tier 1–3) · MODERATE (supported by inference; new research would confirm) · SPECULATIVE (plausible but not evidenced).

3. **External scan (external mode only):** Search adjacent fields. Confirm all sources real.

4. **Route to topic directory:**
   - Determine the primary target item (the item that needs to change).
   - Look up target item's category → map to topic directory:

   | Item category | Topic directory |
   |---|---|
   | A (access/entrances) | entrances-and-circulation |
   | B (vertical circulation) | entrances-and-circulation |
   | C (horizontal circulation) | entrances-and-circulation |
   | D (wayfinding/signage) | wayfinding-and-signage |
   | E (controls/hardware) | controls-and-hardware |
   | F (communication/alerts) | communication-and-alerts |
   | G (bathrooms/wet areas) | bathrooms-and-wet-areas |
   | H (kitchens/workspaces) | kitchens-and-workspaces |
   | I (seating/rest) | seating-and-rest |
   | J (room-types) | room-types |
   | K (sensory environment) | sensory-environment |
   | Economics/cost | economics |
   | Population-general | population-general |
   | Health/symptom | health-and-symptom-management |
   | Frameworks/methodology | frameworks-and-methodology |
   | 3+ directories or ambiguous | cross-cutting |

   **Ambiguity tiebreaker:** If connection links items in two directories with no single primary target, file under the directory of the item with the higher item-code letter (later in alphabet = later in specification sequence = more likely to accommodate).

5. **Write to connection register (Sonnet writes):**
   - GET `references/connections/_index.md` + SHA. Append new row.
   - GET `references/connections/{topic}/connections.md` + SHA (create file if it does not exist). Append new entry.
   - PUT both files. Commit: `connection-scout: append {N} connections to {topic} [{YYYY-MM-DD HH:MM}]`

6. **Feed downstream:** HIGH → item-specification-writer briefing. SPECULATIVE → gap_register P3.

## Connection Entry Schema (per-entry, within topic file)

```markdown
### CON-{NNNN}

**Status:** PENDING | CONSUMED | DEFERRED | SPECULATIVE | CLOSED
**Confidence:** HIGH | MODERATE | SPECULATIVE
**Opus-reviewed:** true | false
**Source BPC slug(s):** {slug1}, {slug2}
**Target item(s):** {item-code(s)}
**Target population(s):** {pop-codes}
**Evidence tier:** {tier of supporting evidence}
**Filed:** {YYYY-MM-DD}
**Applied:** {session ref or —}

**Connection:** {1–3 sentence description of the cross-population or cross-item relationship}

**Evidence basis:** {brief citation of supporting evidence from BPC}

**Action required:** {what item-specification-writer needs to do}

**Disposition notes:** {resolution notes, deferred reasons}
```

## _index.md Row Schema

```markdown
| CON-ID | Status | Primary target | Filed in | Confidence | Opus-reviewed | Session applied |
|---|---|---|---|---|---|---|
| CON-{NNNN} | PENDING | {item-code} ({topic}) | {topic-dir} | HIGH | No | — |
```

**CON-ID assignment:** Increment from highest existing CON-ID in `_index.md`. If `_index.md` does not exist yet (pre-migration): start from CON-0120 (119 connections migrated from monolithic register).

## Migration Note (CO-0006 2026-04-08)

The monolithic `references/connection-register-active.md` has been archived. All new connections write to the topic-directory structure above. The migration session (0B-1) parsed existing entries and routed them. Do not read or write to `references/connection-register-active.md` or `references/connection-register.md` — these are archived.

## Token Rules

- Internal mode: ≤40 candidates per run; prioritise P1 gap items and population pair coverage gaps
- External mode: ≤20 new sources; prioritise Tier 1–3
- THIN base (<2 sources) → cannot rate higher than SPECULATIVE
- Checkpoints: 1–2 lines after each population code pair or source batch
