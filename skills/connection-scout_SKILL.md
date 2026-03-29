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

**Model:** Opus 4.6
**GitHub backend:** `jordanelias/guidebook` · `main`
**Output file:** `references/connection-register.md`
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

4. **Write to connection register:** Append to `references/connection-register.md`. GET + SHA before writing. PUT back. Commit: `connection-scout: append connections [{YYYY-MM-DD HH:MM}]`.

5. **Feed downstream:** HIGH → item-specification-writer briefing. SPECULATIVE → gap_register P3.

## Connection Register Entry Schema

```markdown
## CON-{NNNN} [{YYYY-MM-DD HH:MM}]

**Mode:** Internal | External
**Confidence:** HIGH | MODERATE | SPECULATIVE
**Disposition:** PENDING | CONSUMED | DEFERRED | SUPERSEDED | CLOSED
**Populations involved:** {code list}
**Items involved:** {item code list or NONE}
**Gap register items:** {GAP-XXX list or NONE}

### Connection description
{What is the unmade connection? Mechanism, evidence basis, why not currently in guidebook.}

### Evidence basis
| Source | Tier | Population currently cited for | Proposed extension to |
|---|---|---|---|

### Proposed synthesis direction
{What should the guidebook say? What spec change, new item, or cross-reference?}

### Disposition
- [ ] HIGH → item-specification-writer briefing
- [ ] MODERATE → P2 gap item
- [ ] SPECULATIVE → P3 gap item
- [ ] Superseded by existing content — CLOSED
```

## Token Rules

- Internal mode: ≤40 candidates per run; prioritise P1 gap items and population pair coverage gaps
- External mode: ≤20 new sources; prioritise Tier 1–3
- THIN base (<2 sources) → cannot rate higher than SPECULATIVE
- Checkpoints: 1–2 lines after each population code pair or source batch
