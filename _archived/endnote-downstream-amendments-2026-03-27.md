# Endnote System — Downstream Integration Amendments
**Date:** 2026-03-27 14:00

This document specifies all modifications to existing skills and PI sections required to make the endnote pipeline functional end-to-end.

---

## 1. item-specification-writer (PI-governed) — Amendment

### 1a. New output requirement: REF-ID markers

Every prescriptive claim in a specification that cites evidence must include a `[REF:{slug}:{NN}]` marker inline. The `{slug}` is the BPC slug from which the evidence was retrieved. The `{NN}` is the source's position (01-indexed) in that slug's BPC `Key sources` list.

**Mandatory pre-step:** `research-log-manager RETRIEVE` for each relevant slug before writing. The BPC `Key sources` list provides the REF-ID index.

**Placement rules:**
- Marker appears immediately after the claim it supports, before punctuation.
- Multiple markers may appear at one point for claims supported by multiple sources.
- Every specification bullet with a dimensional value, material requirement, or performance threshold must carry at least one REF-ID. If no source exists: `[UNSUPPORTED — citation required]` (existing rule; unchanged).

**Before (current):**
```markdown
- Threshold height not to exceed 13 mm (AS 1428.1:2021; Smith et al. 2021).
```

**After (new):**
```markdown
- Threshold height not to exceed 13 mm[REF:threshold-door-hardware:01][REF:threshold-door-hardware:03].
```

### 1b. New output requirement: Sources cited table

After each item block, emit a `#### Sources cited` section containing a markdown table:

```markdown
#### Sources cited

| REF-ID | Authors | Year | Title | Journal/Publisher | DOI/URL | Tier | Lang | Jurisdiction |
|---|---|---|---|---|---|---|---|---|
| REF:threshold-door-hardware:01 | Standards Australia | 2021 | AS 1428.1:2021 Design for access and mobility | SAI Global | — | 6 | EN | AU |
| REF:threshold-door-hardware:03 | Smith, J. et al. | 2021 | Door threshold height... | AJOT | doi:10.5014/... | 1 | EN | US |
```

**Data source:** BPC `Key sources` section for relevant slug(s), retrieved via `research-log-manager RETRIEVE`.

**If a source is cited in the specification but absent from BPC Key sources:** Add to sources-cited table AND flag `[NOT IN BPC — verify via citation-verifier]`.

### 1c. Replaces Key citations field

For new items and revised items: `#### Sources cited` table replaces the `**Key citations:**` field. Do not emit both.

For legacy items not being revised in the current pass: `**Key citations:**` remains unchanged. `bibliography-compiler` will flag these for future conversion.

### 1d. Existing outputs unchanged

Population tag table, evidence table, conflict notes — no changes.

---

## 2. vol2-item-formatter — Amendments

### 2a. Canonical format update

Replace the `**Key citations:**` field definition with:

```markdown
#### Sources cited

| REF-ID | Authors | Year | Title | Journal/Publisher | DOI/URL | Tier | Lang | Jurisdiction |
|---|---|---|---|---|---|---|---|---|
```

**Field rules:**
- Minimum 2, maximum 12 sources per item (increased from 6 to accommodate multi-slug items).
- Every REF-ID in the Specifications bullets must have a matching row. Mismatch → validation failure.
- Every row must have Authors, Year, Title, Tier, and Jurisdiction populated. DOI/URL recommended but non-blocking if absent (flagged `[DOI required]`).
- Real sources only. Unverified: append `[UNVERIFIED — DOI required]`.
- If fewer than 2 verified sources: append `[CITATION GAP — evidence-auditor referral required]`.

### 2b. Validation checklist additions

Add to existing checklist:

| Check | Pass condition |
|---|---|
| REF-ID format | All markers match `[REF:{slug}:{NN}]` pattern |
| REF-ID ↔ sources-cited | Every body REF-ID has a sources-cited row; every row has ≥1 body REF-ID |
| Sources-cited completeness | ≥2 rows; Tier and Jurisdiction populated on all rows |
| No legacy+new coexistence | Item does not have both `**Key citations:**` AND `#### Sources cited` |

### 2c. Common errors additions

Add:
- **REF-ID without sources-cited row** — ORPHAN-REF. Add row or remove marker.
- **Sources-cited row without body REF-ID** — UNUSED-SOURCE. Add inline reference or remove row.
- **Both Key citations and Sources cited present** — remove Key citations (sources-cited is authoritative).
- **REF-ID slug mismatch** — slug in marker does not match any known BPC slug. Route to research-log-manager CHECK.

### 2d. Legacy compatibility

If an item uses `**Key citations:**` and is not being revised: validation passes with INFO flag `[LEGACY-CITATION — conversion on next revision]`. Do not fail validation for legacy items.

---

## 3. chunk-assembler — Amendments

### 3a. Pipeline note update

Replace line 145:
```
**Feeds into:** `cross-reference-resolver` · `table-formatter` · `guidebook-auditor` Mode A
```

With:
```
**Feeds into:** `bibliography-compiler` · `cross-reference-resolver` (after bibliography-compiler) · `table-formatter` · `guidebook-auditor` Mode A
```

### 3b. Cross-Reference Integrity Check (§2) — addition

Add to the list of cross-reference patterns scanned:

```
- `[REF:{slug}:{NN}]` — endnote source markers. Do NOT flag as broken refs. 
  These are consumed by bibliography-compiler in the next pipeline stage.
  If bibliography-compiler has NOT yet run: these markers are expected and valid.
  If bibliography-compiler HAS run and markers remain: flag as UNPROCESSED-REF.
```

### 3c. Assembly order — back matter update

Update §1 standard document zones item 6:

```
6. Back matter (endnotes [per volume — placed by bibliography-compiler], bibliography [if separate from endnotes], glossary, index, appendices)
```

---

## 4. cross-reference-resolver — Amendments

### 4a. Reference Pattern Inventory (§1) — addition

Add row to pattern table:

| Type | Pattern examples | Notes |
|---|---|---|
| Endnote superscript | `¹`, `²`, `³˙⁷`, `¹²` | Post-bibliography-compiler only. Verify target exists in `## Endnotes` section. Do NOT flag as broken ref. |

### 4b. Stage 2 — Target Verification — addition

For endnote superscript references:

| Resolution class | Condition | Action |
|---|---|---|
| **VALID** | Superscript number has matching entry in `## Endnotes` section | No action |
| **ABSENT** | Superscript number has no matching endnote entry | Flag as BROKEN — bibliography-compiler error |
| **UNPROCESSED** | `[REF:{slug}:{NN}]` marker still present (bibliography-compiler did not run or failed) | Flag as UNPROCESSED-REF — route to bibliography-compiler |

### 4c. Pre-run mode detection

Before running, detect whether bibliography-compiler has already run on this volume:

- `## Endnotes` section present → bibliography-compiler HAS run → validate superscripts against endnote list
- `## Endnotes` section absent AND `[REF:` markers present → bibliography-compiler has NOT run → skip endnote validation; flag `[BIBLIOGRAPHY-COMPILER NOT YET RUN — REF markers pending]`
- Neither present → no endnote system in this volume (legacy) → skip

---

## 5. PI Amendments Required

### 5a. Skill Registry — add row

Under **Reference Management**:

| Skill | Model | Trigger |
|---|---|---|
| `bibliography-compiler` | Haiku 4.5 | Endnote compilation; volume-end reference list; post-assembly |

### 5b. Workflow Reference — modify

**Document Assembly:**
```
chunk-assembler → bibliography-compiler → cross-reference-resolver → guidebook-auditor A
```

**Item Specification:**
```
item-consolidation-analyzer → item-specification-writer (with REF-ID + sources-cited) → vol2-item-formatter → [framing-checker · evidence-auditor] → prose-style-checker → volii-validator
```

### 5c. Standing Rule 24 ✓ (already committed to project-standards.md)

### 5d. item-specification-writer PI definition — append

Add to the end of the current `item-specification-writer` PI section:

```markdown
### Source Citation Protocol (endnote system)

**REF-ID markers:** Every prescriptive claim citing evidence carries `[REF:{slug}:{NN}]` inline. `{slug}` = BPC slug; `{NN}` = 01-indexed position in BPC Key sources. Mandatory `research-log-manager RETRIEVE` before writing.

**Sources-cited table:** `#### Sources cited` section appended after each item block. Markdown table with columns: REF-ID, Authors, Year, Title, Journal/Publisher, DOI/URL, Tier, Lang, Jurisdiction. Replaces `**Key citations:**` for new and revised items. Legacy items retain `Key citations` until revised.

**Downstream:** `vol2-item-formatter` validates REF-ID ↔ sources-cited integrity. `bibliography-compiler` compiles volume-end endnotes. `cross-reference-resolver` validates endnote superscripts.
```

### 5e. To-build list — update

Remove `bibliography-compiler` from implicit/to-build. It is now built.

---

## 6. Data Flow Verification — End-to-End Trace

```
BPC (Key sources list)
  │
  ▼ RETRIEVE
item-specification-writer
  │ emits: [REF:{slug}:{NN}] markers in spec bullets
  │ emits: #### Sources cited table per item
  │
  ▼
vol2-item-formatter
  │ validates: every REF-ID ↔ sources-cited row (bidirectional)
  │ validates: ≥2 sources, Tier+Jurisdiction populated
  │ flags: ORPHAN-REF (blocking), UNUSED-SOURCE (warning), LEGACY-CITATION (info)
  │
  ▼
chunk-assembler
  │ assembles: volume in section-map order
  │ passes through: REF-ID markers + sources-cited sections unchanged
  │ does NOT flag REF-IDs as broken refs (they are expected pre-bibliography-compiler)
  │
  ▼
bibliography-compiler
  │ extracts: all [REF:] markers + all #### Sources cited tables
  │ integrity check: ORPHAN-REF (blocking), UNUSED-SOURCE (warning)
  │ deduplicates: by DOI, then author+year+title
  │ assigns: sequential superscript numbers by first appearance
  │ replaces: [REF:] markers → superscripts (¹²³)
  │ generates: ## Endnotes section at volume end
  │ strips: #### Sources cited sections from body
  │ flags: LEGACY-CITATION items for future conversion
  │
  ▼
cross-reference-resolver
  │ detects: bibliography-compiler has run (## Endnotes present)
  │ validates: every superscript has matching endnote entry
  │ flags: ABSENT endnotes (BROKEN), unprocessed [REF:] markers (UNPROCESSED-REF)
  │ does NOT treat superscripts as broken section/part/appendix refs
  │
  ▼
guidebook-auditor A
  │ standard structural audit on final output
```

### Failure modes caught at each stage

| Stage | Catches | Blocks? |
|---|---|---|
| vol2-item-formatter | REF-ID without source row; source row without REF-ID; legacy coexistence | ORPHAN-REF blocks |
| bibliography-compiler | Same + cross-item orphans; dedup conflicts; DOI gaps | ORPHAN-REF blocks |
| cross-reference-resolver | Missing endnote entries; unprocessed REF markers | Flags only |

### Backward compatibility

| Item state | Behavior |
|---|---|
| New item (post-endnote system) | Full REF-ID + sources-cited pipeline |
| Revised item (Key citations → sources-cited) | item-specification-writer converts on revision |
| Unrevised legacy item | Key citations passes through all stages; flagged LEGACY-CITATION at bibliography-compiler |
| Mixed volume (some new, some legacy) | Endnotes compiled for new items; legacy items retain Key citations; assembly report notes mixed state |
