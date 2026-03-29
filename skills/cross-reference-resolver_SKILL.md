---
name: cross-reference-resolver
description: >
  Audit and repair all internal narrative cross-references across any guidebook volume —
  covering section number references, part references, appendix references, and supplementary
  volume references. Detects broken, stale, and ambiguous references; produces a resolution
  register; and hands off mechanical substitutions to find-and-replace. ALWAYS use this
  skill when asked to: check cross-references, find broken links, validate internal
  references, audit "see §X" references, check whether a referenced section still exists,
  repair stale cross-references, or validate that all internal navigation is consistent
  after a structural change. Trigger on: "check cross-references", "broken references",
  "stale section refs", "does this section still exist", "validate internal refs",
  "cross-reference audit", "ref audit", "fix the refs", "internal links", "after restructuring
  check refs", or any task following a structural change (section deletion, renaming,
  renumbering) that may have left references pointing to absent targets.
  Distinct from volii-validator (item codes only) and find-and-replace (mechanical substitution).
  This skill handles discovery and classification; find-and-replace handles execution.
---

**Model:** Haiku 4.5 for discovery passes · Sonnet 4.6 for ambiguity resolution  
**Input:** assembled document (or section map + chunks) · scope (full doc / specific volumes)  
**Output:** cross-reference register (YAML) + resolution table + find-and-replace handoff spec  
**Chunk ceiling:** 500 lines per pass. Always use section map to guide scope.

---

## 1. Reference Pattern Inventory

This skill resolves these reference types. Add new patterns to `references/ref-patterns.md` if the document introduces new conventions.

| Type | Pattern examples | Notes |
|---|---|---|
| Section number | `§1.4`, `§III.2`, `§8.4.1` | Verify target heading exists |
| Part reference | `Part V`, `Part VIII`, `Volume 2, Part IV` | Volume-qualified preferred |
| Appendix reference | `Appendix A`, `Appendix D` | Verify appendix exists in back matter |
| Supplementary volume | `Supplementary Volume IV, Section II` | Verify section exists in supp vol |
| Item code narrative | `see item G-03`, `refer to A-11`, `see K-04` | Verify item heading exists; valid categories A–K. Hand off unresolved to volii-validator |
| "See above" / "See below" | Positional references | Flag as AMBIGUOUS — positional refs are not stable across formats |
| Endnote superscript | `¹`, `²`, `[1]`, `[REF:{slug}:{NN}]` | Post-bibliography-compiler: validate against endnote list. Pre-bibliography-compiler: pass through REF markers unchanged. See §4. |

---

## 2. Stage 1 — Discovery (Haiku)

Run grep passes for each pattern type across the defined scope. Produce the **Raw Reference Register**:

```yaml
cross_references:
  - id: CR-001
    type: section
    pattern: "§1.4"
    source_line: [N]
    source_context: "[surrounding text, ≤2 lines]"
    resolution: PENDING
  - id: CR-002
    ...
```

Report total reference count by type before proceeding.

---

## 3. Stage 2 — Target Verification (Haiku)

For each PENDING reference, search the document (or section map) for the target:

| Resolution class | Condition | Action |
|---|---|---|
| **VALID** | Target heading exists, text matches | No action needed |
| **RENAMED** | Target heading exists with different text | Flag; propose updated reference text |
| **ABSENT** | No matching heading found anywhere in document | Flag as BROKEN |
| **AMBIGUOUS** | Multiple headings match the pattern | Flag; surface candidates for Sonnet resolution |
| **POSITIONAL** | "see above", "see below", "as noted earlier" | Flag as STRUCTURAL — recommend replacing with explicit reference |
| **EXTERNAL** | Reference to a document outside this guidebook | Flag; verify source still exists if web search is available |

Update register with resolution class for each reference.

---

## 4. Stage 3 — Resolution (Sonnet)

For RENAMED, ABSENT, and AMBIGUOUS references, apply resolution rules:

**RENAMED:** Produce the corrected reference text. Check whether the renaming was a deliberate structural decision (session log / gap register) or an oversight.

**ABSENT:** Determine cause:
- Target was deleted (check gap register / structural fix register) → replace with: redirect to current location, or remove the reference
- Target was never created (phantom section) → flag as `[BROKEN REF — target section does not exist; author action required]`
- Target was renumbered → find new number and update

**AMBIGUOUS:** Surface up to 3 candidate targets with their full headings. Confirm correct target with user before producing the fix.

**POSITIONAL:** Propose a specific reference to replace the positional language.

---

## 5. Stage 4 — Resolution Register

Produce the **Resolution Register** — the handoff document for find-and-replace:

```yaml
resolution_register:
  document: "[DOC-ID]"
  date: "[YYYY-MM-DD]"
  total_refs_audited: [N]
  summary:
    valid: [N]
    renamed: [N]
    absent: [N]
    ambiguous: [N]
    positional: [N]
    external: [N]
  resolutions:
    - id: CR-001
      status: RENAMED
      find: "§1.6 Universal Design, Inclusive Design"
      replace: "§1.4 Universal Design, Inclusive Design, and This Guidebook"
      source_lines: [N, N]
      confidence: HIGH
    - id: CR-007
      status: ABSENT
      find: "see Appendix E"
      replace: "[BROKEN REF — Appendix E does not exist; author action required]"
      source_lines: [N]
      confidence: HIGH
  pending_author_decisions:
    - id: CR-012
      issue: "AMBIGUOUS — 3 candidate targets"
      candidates: ["§2.4 DEAF", "§2.3 VIS — Distinct from DEAF subsection", "Abbreviations: DEAF"]
```

---

## Stage 5 — Find-and-Replace Handoff

For all HIGH-confidence resolutions, produce a find-and-replace specification for each substitution:

```
FIND: [exact string]
REPLACE: [corrected string]
SCOPE: [volume/part]
MATCH TYPE: Exact
INSTANCES: [N expected]
```

Pass this specification to find-and-replace skill for execution. Do not execute substitutions directly.

---

## Stage 6 — Per-Part File Awareness (v10.1 addition)

When operating on the v10.1 multi-file architecture (`parts/v10/*.md`):

- **Cross-file references:** A reference in `part-02.md` to `§7.3` targets content in `part-07.md`. Cross-file references are valid — they resolve against the assembled document, not individual files.
- **Scope:** When auditing a single Part file, still verify targets exist. Use the manifest (`parts/v10/manifest.md`) to locate target files. If target file is unavailable: flag as UNVERIFIABLE with note `[target in {filename} — not loaded]`.
- **Category files:** Part 7 category files (`part-07/cat-A.md` through `cat-K.md`) may reference items in other categories. These cross-category references are valid and expected.
- **Assembly prerequisite:** Full cross-reference audit should run on the assembled master document (post-`chunk-assembler`), not on individual Part files. Per-Part audits are preliminary only.

---

## Stage 7 — BPC↔Item Traceability (v10.1 addition)

Bidirectional traceability between BPC entries and item specifications:

**Direction 1: BPC → Items**
For each slug in `references/best-practices-compendium.md`:
- Check: does the BPC entry have a `part7_items` field listing the item codes it informs?
- If missing: flag as `UNMAPPED-BPC — slug {slug} has no part7_items field`
- If present: verify each listed item code exists in Part 7

**Direction 2: Items → BPC**
For each item specification in Part 7:
- Check: does the item's evidence table cite any BPC slug?
- Identify the BPC slug(s) the item's evidence derives from
- Check: does the item carry a `bpc_slugs` field?
- If missing: flag as `UNMAPPED-ITEM — item {code} has no bpc_slugs field`
- If present: verify each listed slug exists in the BPC

**Output:**

```
BPC↔ITEM TRACEABILITY AUDIT
  BPC entries: [N]
  BPC with part7_items: [N] / [N]
  Items with bpc_slugs: [N] / [N]
  Orphaned BPC entries (no items): [list]
  Orphaned items (no BPC): [list]
  Broken links: [list]
```

This pass runs after Phase 3 writing (when both BPC and items are populated) and during Phase 5 QA.

---


## 4. Endnote Superscript Validation

Run this check **only if** `bibliography-compiler` has already run on this volume.

### Pre-run mode detection

Before running, detect the volume's endnote state:

| Condition | State | Action |
|---|---|---|
| `## Endnotes` section present | bibliography-compiler HAS run | Validate superscripts against endnote list |
| `## Endnotes` absent + `[REF:` markers present | bibliography-compiler has NOT run | Skip endnote validation; flag `[BIBLIOGRAPHY-COMPILER NOT YET RUN — REF markers pending]` |
| Neither present | Legacy volume | Skip |

### Superscript validation

| Resolution class | Condition | Action |
|---|---|---|
| **VALID** | Superscript number has matching entry in `## Endnotes` | No action |
| **ABSENT** | Superscript number has no matching endnote entry | Flag BROKEN — bibliography-compiler error |
| **UNPROCESSED** | `[REF:{slug}:{NN}]` marker still present | Flag UNPROCESSED-REF — route to bibliography-compiler |

**Note:** Endnote superscripts (`¹`, `²`, etc.) are NOT broken section or part cross-references. Do not flag them as broken refs in Stage 2 general validation.

## Escalation Triggers

Stop and confirm with user:

- More than 10% of references are ABSENT — indicates a major structural change occurred without cross-reference update; confirm the structural state of the document before resolving
- A BROKEN REF is in a safety-critical section (emergency evacuation, structural specifications) — flag immediately; do not leave with a placeholder
- Positional references are >20 — recommend a systematic rewrite pass via prose-style-checker before resolving individually

---

**Preceded by:** `structure-auditor` (map new structure before resolving refs)
**Feeds into:** `find-and-replace` (execution) · `volii-validator` (item code validation)
