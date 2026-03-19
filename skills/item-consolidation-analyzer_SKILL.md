---
name: item-consolidation-analyzer
description: >
  Analyze design items in any Part or Section for consolidation — merging redundant items,
  splitting overloaded items, assigning typology scope.
  Run before any Part is finalised.
  Trigger on: "consolidate", "merge items", "reduce items", "split this item",
  "typology review", "item-by-item analysis", "tighten the section", "standalone justification".
---

**Intake:** ≤30 items per run. Full Part → haiku-chunker first.
**Model:** Sonnet 4.6
**Typology system:** Residential (R) · Non-Residential (NR) · Both (note scope differences)
**Population codes:** → `references/project-standards.md`
**Run after:** content-gap-analyzer · **Run before:** critique-report-writer

## Decision Framework

**MERGE flags** (≥2 of):
- Fewer than 3 distinct citations
- Fewer than 150 words of substantive specification text
- Specification fully contained within an adjacent item's scope
- Same specification/drawing package as adjacent item
- No distinct OT ADL impact from adjacent item

**SPLIT flags** (≥2 of):
- Two or more distinct specification packages reviewed by different engineers
- Two or more distinct practitioner audiences (e.g. OT + structural)
- Population codes with conflicting design requirements bundled unresolved
- Item would exceed 400 words after full evidence write-up

**Typology:** R · NR · BOTH (note scope differences inline). Flag missing or incorrect assignments.

## Steps
1. Extract per item: code · title · word count · citation count · population codes · evidence tier · typology assigned.
2. Apply merge/split flags.
3. Assign/correct typology.
4. Report net item count delta.
5. Citation floor check: any surviving item must have ≥2 verified citations. Below floor → P2 gap register entry.

## Output
```
## Consolidation Analysis — [Part/Section] [DOC-ID] [Date]
Items reviewed: N · Retained: N · Merges: N · Splits: N · Net: N→N · Typology corrections: N

| Code | Title | Decision | Rationale | Typology | Citations |

### Merge Details / Split Details [where applicable]

### Gap Register Entries [citation floor failures — YAML]
```

Do not auto-merge if merge would delete a P1 gap register item — flag for manual review.
Typology decisions are editorial — do not override without author confirmation.
