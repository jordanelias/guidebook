<!-- GOVERNED BY PROJECT INSTRUCTIONS — execution copy only. PI definition governs on conflict. -->
---
name: bibliography-compiler
description: >
  Compile volume-end endnote lists from per-item sources-cited tables. Extracts all
  REF-ID markers and sources-cited data from an assembled volume, deduplicates by DOI,
  assigns sequential superscript endnote numbers by order of first appearance, replaces
  REF-ID markers with superscripts in body text, generates the volume-end endnote list,
  and strips per-item sources-cited sections from final output. ALWAYS use this skill
  when asked to: compile endnotes, build bibliography, generate references, produce
  volume-end citations, or as the post-assembly step before cross-reference-resolver.
  Trigger on: "compile endnotes", "build bibliography", "endnote pass", "generate
  references", or automatically during Document Assembly workflow after chunk-assembler.
  DISTINCT from citation-verifier (checks source existence) and research-log-manager
  (manages BPC). This skill compiles existing verified sources into publication format.
---

**Model:** Haiku 4.5 — mechanical extraction and replacement; no judgment required
**Input:** Assembled volume markdown (post-chunk-assembler)
**Output:** Volume markdown with superscript endnotes + appended endnote list; assembly report
**Chunk ceiling:** One volume per run. Multi-volume document → run once per volume boundary.

---

## 0. Position in Pipeline

```
item-specification-writer (emits REF-ID markers + #### Sources cited tables)
  → vol2-item-formatter (validates REF-IDs ↔ sources-cited)
    → chunk-assembler (assembles volume)
      → bibliography-compiler (this skill)
        → cross-reference-resolver (final pass — endnote-aware)
          → guidebook-auditor A
```

**Inputs consumed:**
- `[REF:{slug}:{NN}]` markers in body text (placed by item-specification-writer)
- `#### Sources cited` sections per item (placed by item-specification-writer, validated by vol2-item-formatter)

**Outputs produced:**
- Superscript numbers in body text (¹²³) replacing REF-ID markers
- `## Endnotes` section appended at volume end
- Per-item `#### Sources cited` sections removed from body

**Legacy compatibility:**
- Items with old `**Key citations:**` field (pre-endnote system) are flagged `[LEGACY-CITATION — conversion required]` but not processed. They pass through to output unchanged. Conversion to `#### Sources cited` format happens when items are revised by item-specification-writer.

---

## 1. Extract

### 1a. Extract REF-ID markers from body text

Scan assembled volume for all `[REF:{slug}:{NN}]` patterns. Record:
- Marker string
- Line number (for ordering)
- Surrounding context (≤10 words each side)

### 1b. Extract sources-cited tables

Scan for all `#### Sources cited` sections. Each contains a markdown table with columns:

| REF-ID | Authors | Year | Title | Journal/Publisher | DOI/URL | Tier | Lang | Jurisdiction |
|---|---|---|---|---|---|---|---|---|

Parse each row. Key fields: REF-ID (links to body markers), DOI/URL (deduplication key), Tier, Jurisdiction.

### 1c. Extract legacy Key citations (flag only)

Scan for `**Key citations:**` blocks. For each found:
- Log: `LEGACY-CITATION at line {N} — item {code} — conversion required before endnote compilation`
- Do NOT attempt to parse or convert. These pass through unchanged.
- If a `**Key citations:**` block coexists with a `#### Sources cited` section on the same item: the `#### Sources cited` section is authoritative. Flag the `Key citations` block for removal: `[REDUNDANT — sources-cited table present]`.

---

## 2. Integrity Check

### 2a. Orphan detection (body → sources)

Every `[REF:{slug}:{NN}]` in body text must have a matching row in a `#### Sources cited` table.

- Match found → VALID
- No match → **ERROR: ORPHAN-REF** — `[REF:{slug}:{NN}] at line {N} has no sources-cited entry`

**ORPHAN-REF is a blocking error.** Do not proceed to numbering. Report all orphans. Resolution: item-specification-writer must add the missing source to the sources-cited table, or the marker must be removed if the citation was erroneous.

### 2b. Orphan detection (sources → body)

Every row in a `#### Sources cited` table should have at least one matching `[REF:...]` marker in body text.

- Match found → VALID
- No match → **WARNING: UNUSED-SOURCE** — `{REF-ID} in sources-cited for item {code} has no body reference`

**UNUSED-SOURCE is non-blocking.** Include the source in endnotes but flag: `[cited in sources table but not referenced in text]`. Author decision whether to add inline reference or remove source.

### 2c. DOI validation

Every source should have a DOI or URL. Missing → append `[DOI required]` to endnote entry. Non-blocking.

---

## 3. Deduplicate

Sources may be cited across multiple items. Deduplicate:

**Priority 1: DOI match** — same DOI = same source regardless of author string variations.
**Priority 2: Author+Year+Title fuzzy match** — where DOI is absent, match on (first author surname + year + first 6 words of title, case-insensitive). If match confidence <90%: treat as separate sources.

After deduplication, each unique source gets one entry. Record which items cited it (for the assembly report).

---

## 4. Assign Endnote Numbers

Number sequentially by **order of first appearance** in the volume text:
- Scan body text top-to-bottom
- First `[REF:...]` encountered → endnote ¹
- Second unique source → endnote ²
- Same source encountered again → reuses its assigned number
- Continue through volume

**Numbering resets at each volume boundary.** Volume 1 starts at ¹. Volume 2 starts at ¹. Supplementary volumes start at ¹.

---

## 5. Replace Markers

Replace each `[REF:{slug}:{NN}]` marker in body text with its assigned superscript number.

**Single marker:** `[REF:threshold-door-hardware:03]` → `³`

**Adjacent markers:** `[REF:threshold-door-hardware:03][REF:grab-bar-placement:07]` → `³˙⁷` (superscript with raised period separator)

**Placement:** Superscript appears immediately after the claim, before any punctuation:
- `Threshold height not to exceed 13 mm³.` — correct
- `Threshold height not to exceed 13 mm.³` — incorrect

---

## 6. Generate Endnote List

Append at volume end, before glossary/index/appendices:

```markdown
## Endnotes

¹ Smith, J., Lee, K., & Patel, R. (2021). Door threshold height and wheelchair access: A clinical study. *American Journal of Occupational Therapy*, 75(3), 7503205010. doi:10.5014/ajot.2021.044263 [Tier 1; US]

² Bauman, H. (2014). DeafSpace Design Guidelines. Gallaudet University. [Co-1; US]

³ Standards Australia. (2021). AS 1428.1:2021 Design for access and mobility — General requirements for access — New building work. SAI Global. [Tier 6; AU]
```

### Endnote entry format

```
{superscript} {Authors} ({Year}). {Title}. *{Journal/Publisher}*{, Volume(Issue), Pages}. {DOI/URL} [Tier {N}; {Jurisdiction}]
```

- Tier and jurisdiction included — readers assess evidence weight at point of citation
- Italic journal/publisher name
- DOI as `doi:` prefix or full URL
- Missing DOI: `[DOI required]`
- Missing tier: `[Tier unclassified]`
- UNUSED-SOURCE entries: append `[cited in sources table; no inline reference]`

---

## 7. Strip Per-Item Sources-Cited Sections

Remove all `#### Sources cited` sections (heading + table + any blank lines) from the body. Their data is now in the endnote list.

Do NOT strip `**Key citations:**` blocks — those are legacy items awaiting conversion.

Where a `**Key citations:**` block and `#### Sources cited` section coexist on the same item: strip `#### Sources cited` (consumed into endnotes) and strip `**Key citations:**` (redundant — flagged in §1c).

---

## 8. Output

1. **Volume markdown** — body text with superscripts, endnote list appended, sources-cited sections stripped.
2. **Assembly report** — written to `misc/bibliography-assembly-{volume}-{YYYY-MM-DD-HHMM}.md`:

```markdown
## Bibliography Assembly Report — {Volume}

**Date:** YYYY-MM-DD HH:MM
**Volume:** {N}
**Unique sources:** {N}
**Endnotes generated:** {N}
**REF-ID markers processed:** {N}

### Errors
| Type | Count | Details |
|---|---|---|
| ORPHAN-REF | {N} | {list} |

### Warnings
| Type | Count | Details |
|---|---|---|
| UNUSED-SOURCE | {N} | {list} |
| DOI-MISSING | {N} | {list} |
| LEGACY-CITATION | {N} | {list} |

### Deduplication
| DOI/Match | Merged from items | Assigned endnote |
|---|---|---|

### Source tier distribution
| Tier | Count |
|---|---|
| 1 | {N} |
| Co-1 | {N} |
| 2 | {N} |
| Co-2 | {N} |
| 3 | {N} |
| 4 | {N} |
| 5 | {N} |
| 6 | {N} |
| Unclassified | {N} |
```

Commit assembly report to GitHub: `bibliography-compiler: assembly report {volume} [{YYYY-MM-DD HH:MM}]`

---

## 9. Error States

| Error | Severity | Action |
|---|---|---|
| ORPHAN-REF (body marker, no sources-cited row) | BLOCKING | Halt. Report all. Route to item-specification-writer. |
| UNUSED-SOURCE (sources-cited row, no body marker) | WARNING | Include in endnotes with flag. Author decision. |
| DOI-MISSING | WARNING | Include entry with `[DOI required]`. |
| TIER-MISSING | WARNING | Include entry with `[Tier unclassified]`. |
| LEGACY-CITATION (old Key citations format) | INFO | Pass through. Flag for conversion. |
| DUPLICATE-DOI across volumes | INFO | Each volume numbers independently. Same source may have different endnote numbers in different volumes. |
| SOURCES-CITED + KEY-CITATIONS on same item | WARNING | Sources-cited is authoritative. Strip both at §7. |

---

## 10. Token Rules

- Haiku 4.5: mechanical task. No judgment, synthesis, or framing decisions.
- One volume per run.
- ORPHAN-REF errors block output — do not attempt partial compilation.
- Checkpoint after each stage: `CHECKPOINT [YYYY-MM-DD HH:MM] — bibliography-compiler — stage: {N} — {status}`

---

