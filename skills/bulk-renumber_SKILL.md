---
name: bulk-renumber
description: >
  Context-aware §-reference rewriting across the guidebook. Rewrites all section number
  references, Part references, and cross-references to match a new numbering scheme after
  content consolidation, deletion, or restructuring. ALWAYS use this skill when asked to:
  renumber sections, apply a new Part numbering map, update §-references after restructuring,
  rewrite cross-references to new numbers, or apply a renumbering Change Order. Trigger on:
  "renumber", "apply numbering map", "update section references", "§-reference rewrite",
  "Part renumbering", "numbering pass". Phase 4 skill — runs after content is final, on
  content-complete document. Distinct from find-and-replace (generic substitution) and
  cross-reference-resolver (audit and classify). This skill executes a numbering
  transformation defined by a mapping table.
---

**Model:** Sonnet 4.6
**Input:** Document (or per-Part files) + renumbering map + section map
**Output:** Renumbered document + renumber log
**Prerequisite:** Content must be final. Renumbering is Phase 4 — never run before content editing is complete.

---

## 1. Renumbering Map

A renumbering map is a table of old → new mappings:

```markdown
| Old | New | Scope |
|---|---|---|
| §6.1 | §5.1 | Section reference |
| §6.2 | §5.2 | Section reference |
| Part VI | Part 5 | Part reference |
| Part VII | Part 6 | Part reference |
```

The map is provided by `toc-editor` via a Change Order, or by the workplan. Never infer a renumbering map — it must be explicit.

---

## 2. Reference Types to Rewrite

| Type | Pattern | Example old → new |
|---|---|---|
| Section number | `§N.N`, `§N.N.N` | `§6.1` → `§5.1` |
| Part reference | `Part N`, `Part [roman]` | `Part VI` → `Part 5` |
| Volume-qualified Part | `Volume 2, Part IV` | `Volume 2, Part 4` |
| In-text narrative | "see the section on..." + old number | Context-dependent |
| Heading text | `## §6.1 Title` | `## §5.1 Title` |
| Cross-reference targets | `see §6.1.2` | `see §5.1.2` |
| Item code Part prefix | Where item codes embed Part number | Map-dependent |

---

## 3. Procedure

**Stage 1 — Extract all references (Haiku)**
Grep for all §-patterns and Part references in the document. Produce reference inventory:

```
REF-001 | §6.1 | line 142 | "see §6.1 for corridor specifications"
REF-002 | Part VI | line 3 | heading: "# Part VI: Item Specification Library"
```

**Stage 2 — Apply map**
For each reference in the inventory:
- Look up old value in the renumbering map
- If found: record the new value
- If not found: flag as UNMAPPED — do not guess

**Stage 3 — Ambiguity check (Sonnet)**
For each mapped reference, verify the substitution is unambiguous:
- Does the old pattern appear as a substring in a longer reference? (e.g., `§6.1` inside `§6.12`) → flag for manual review
- Does the replacement create a collision with an existing reference? → flag
- Is the reference inside a direct quote or citation? → flag — do not rewrite citations

**Stage 4 — Execute**
Apply all unambiguous substitutions using Python `str.replace()` with exact matching, processing longest patterns first (to avoid substring collisions).

**Stage 5 — Verify**
After execution:
- Re-extract all references → confirm all old values are gone
- Confirm all new values have valid targets (headings exist)
- Report: N references rewritten · N unmapped · N ambiguous (manual)

---

## 4. Safety Rules

- Never rewrite inside a citation or bibliographic reference
- Never rewrite item codes (A-01, G-03) — these are content identifiers, not structural
- Process longest patterns first: `§6.12` before `§6.1`
- One pass only — do not iterate (iterative renumbering causes cascading errors)
- If >5% of references are UNMAPPED: stop and report — the renumbering map may be incomplete

---

## 5. Per-Part File Mode

When operating on v10.1 per-Part files:
- Apply renumbering to each file independently
- Cross-file references (e.g., `§7.3` in `part-02.md`) are renumbered using the same map
- After per-file renumbering: run `cross-reference-resolver` on assembled document to catch any missed references

---

**Preceded by:** `toc-editor` (provides renumbering map via Change Order) · All Phase 3 writing complete
**Feeds into:** `cross-reference-resolver` (verification) · `chunk-assembler` (assembly)
