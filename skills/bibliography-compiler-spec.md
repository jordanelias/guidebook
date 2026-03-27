# bibliography-compiler — Skill Specification

## Purpose

Collects all REF-ID markers across a volume's chunks, deduplicates, assigns sequential endnote numbers (¹²³), replaces REF-ID markers with superscripts in the body text, and generates the volume-end endnote list. One run per volume at assembly time.

## Position in Pipeline

```
item-specification-writer (emits REF-ID markers + sources-cited blocks per item)
    → chunk-assembler (assembles volume)
        → bibliography-compiler (endnote compilation)
            → cross-reference-resolver (final pass)
```

## Trigger

`compile endnotes` · `build bibliography` · `endnote pass` · called by `chunk-assembler` at volume assembly · any request to generate volume-end references.

## Model

Haiku 4.5 — mechanical extraction and replacement; no judgment required.

## Inputs

- Assembled volume markdown (from `chunk-assembler` output)
- All `sources-cited` blocks embedded in item specifications

## REF-ID Marker Format (in-text)

```
[REF:{slug}:{NN}]
```

Example: `[REF:threshold-door-hardware:03]` — third source in the threshold-door-hardware BPC.

`item-specification-writer` places these inline in specification prose wherever a claim requires citation. Multiple markers may appear at one point: `[REF:threshold-door-hardware:03][REF:grab-bar-placement:07]`.

## Sources-Cited Block Format (per item, emitted by item-specification-writer)

```markdown
<!-- SOURCES-CITED: {item-code} -->
| REF-ID | Authors | Year | Title | Journal/Publisher | DOI/URL | Tier | Lang | Jurisdiction |
|---|---|---|---|---|---|---|---|---|
| REF:threshold-door-hardware:03 | Smith et al. | 2021 | Door threshold... | AJOT | doi:10.5014/ajot... | 1 | EN | US |
<!-- /SOURCES-CITED -->
```

Hidden in HTML comments — not rendered in body text. `bibliography-compiler` extracts these.

## Process

1. **Extract** all `<!-- SOURCES-CITED -->` blocks from assembled volume.
2. **Extract** all `[REF:...]` markers from body text.
3. **Orphan check:** Any REF-ID in body without a sources-cited entry → ERROR (log, do not silently drop). Any sources-cited entry without a body reference → WARNING (include in endnotes but flag).
4. **Deduplicate** by DOI first, then by author+year+title fuzzy match (same source cited across multiple items gets one endnote number).
5. **Assign numbers** sequentially by order of first appearance in the volume text. Numbers reset per volume.
6. **Replace** `[REF:...]` markers with superscript numbers: `¹` `²` `³`. Adjacent markers merge: `¹˒²` (superscript comma-separated).
7. **Generate endnote list** at volume end:

```markdown
## Endnotes

¹ Smith, J., Lee, K., & Patel, R. (2021). Door threshold height and wheelchair access: A clinical study. *American Journal of Occupational Therapy*, 75(3), 7503205010. doi:10.5014/ajot.2021.044263 [Tier 1; US]

² Bauman, H. (2014). DeafSpace Design Guidelines. Gallaudet University. [Co-1; US]
```

8. **Strip** all `<!-- SOURCES-CITED -->` blocks from final output (data consumed; no longer needed in body).
9. **Output:** Volume markdown with superscripts + appended endnote list.

## Endnote Entry Format

```
{N} {Authors} ({Year}). {Title}. *{Journal/Publisher}*, {Volume}({Issue}), {Pages}. {DOI/URL} [Tier {N}; {Jurisdiction}]
```

Tier and jurisdiction are included because this is a technical reference — readers need to assess evidence weight at point of citation.

## Token Rules

- Haiku 4.5: mechanical task, no judgment.
- One volume per run. Do not process multiple volumes in a single call.
- Orphan errors block output — resolve before proceeding.

## Error States

| Error | Action |
|---|---|
| REF-ID in body, no sources-cited entry | ERROR — halt; log to gap_register |
| Sources-cited entry, no body reference | WARNING — include in endnotes; flag in output |
| Duplicate DOI across items | Merge to single endnote number |
| Missing DOI | Include entry; append `[DOI required]` |
| Missing tier | Include entry; append `[Tier unclassified]` |

---

# item-specification-writer — Modification Spec

## Changes Required

### 1. In-text REF-ID markers (new)

Every prescriptive claim in a specification that cites evidence must include a `[REF:{slug}:{NN}]` marker inline. The `{NN}` maps to the source's position in the item's BPC `Key sources` list (01-indexed).

**Before (current):**
```markdown
Threshold height not to exceed 13 mm (AS 1428.1:2021; Smith et al. 2021).
```

**After (new):**
```markdown
Threshold height not to exceed 13 mm.[REF:threshold-door-hardware:01][REF:threshold-door-hardware:03]
```

### 2. Sources-cited block (new, appended per item)

After each item specification block, emit a hidden sources-cited block:

```markdown
<!-- SOURCES-CITED: V2-P4-E03 -->
| REF-ID | Authors | Year | Title | Journal/Publisher | DOI/URL | Tier | Lang | Jurisdiction |
|---|---|---|---|---|---|---|---|---|
| REF:threshold-door-hardware:01 | Standards Australia | 2021 | AS 1428.1:2021 Design for access and mobility | SAI Global | — | 6 | EN | AU |
| REF:threshold-door-hardware:03 | Smith, J. et al. | 2021 | Door threshold height... | AJOT | doi:10.5014/... | 1 | EN | US |
<!-- /SOURCES-CITED -->
```

### 3. Source data origin

Sources-cited data is drawn from the BPC `Key sources` section for the relevant slug(s). `item-specification-writer` must `research-log-manager RETRIEVE` the BPC before writing. If a source is cited in the specification but absent from BPC Key sources, the writer must add it to the sources-cited block AND flag `[NOT IN BPC — verify]`.

### 4. Existing outputs unaffected

- Population tag table: unchanged.
- Evidence table: unchanged.
- Conflict notes: unchanged.
- The sources-cited block is additive — no existing output is removed or restructured.

---

# PI Amendment — additions needed

## Standing Rule 24 ✓ (committed to project-standards.md)

## Skill Registry — add:

```
| bibliography-compiler | Haiku 4.5 | Endnote compilation; volume-end reference list |
```

## Workflow Reference — modify:

**Document Assembly** becomes:
```
chunk-assembler → bibliography-compiler → cross-reference-resolver → guidebook-auditor A
```

**Item Specification** becomes:
```
item-consolidation-analyzer → item-specification-writer (with REF-ID + sources-cited) → [framing-checker · evidence-auditor] → prose-style-checker → volii-validator
```

## To-build list — update:

Move `bibliography-compiler` from implicit to explicit. Remove from "to build" once skill file is created.
