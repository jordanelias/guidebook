---
name: table-formatter
description: >
  Fix, standardize, and enforce consistent table formatting across all Accessible Built
  Environments Guidebook volumes. ALWAYS use this skill when asked to: fix tables, repair
  broken tables, standardize table formatting, convert table styles, audit table consistency,
  or when table cells are spilling/wrapping incorrectly. Trigger on: "fix tables", "broken
  table", "table formatting", "standardize tables", "table audit", "pipe tables", "grid
  tables", "matrix table", "cell overflow", "column misalignment". Also trigger if any skill
  produces a file and the user or a prior stage flags a table formatting problem. Run after
  any bulk find-and-replace pass that touches table rows.
---

**Model:** Haiku 4.5 (detection + extraction) · Sonnet 4.6 (judgment on ambiguous cases)

---

## Canonical Table Standard

All tables in all volumes must conform to **GFM pipe table format** (GitHub Flavored Markdown).  
Grid/pandoc tables (space-padded, dash-separated rows) are **legacy format** — convert on sight.

### Rule 1 — Pipe Table Structure
```
| Header 1 | Header 2 | Header 3 |
|---|---|---|
| Cell | Cell | Cell |
```
- Every row starts and ends with `|`
- Separator row uses `|---|---|---|` (no padding required)
- One row per logical table row — **no cell wrapping to next line**
- Column count must match header row exactly on every data row

### Rule 2 — Matrix Tables (population × item)
Used in Vol 2A residential/non-residential matrices. Canonical format:

```
| Item | Title | MOB | VIS | DEAF | DEM | NDV | OFS | NEU | PAIN | DBL | UPL | Stage |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A-01 | Acoustic performance | ● | — | ● | ● | ● | ● | ● | ● | ● | — | SD |
```

Population column order (canonical, never reorder):
`MOB | VIS | DEAF | DEM | NDV | OFS | NEU | PAIN | DBL | UPL`

Symbols:
- `●` = primary design requirement
- `○` = secondary / conditional requirement  
- `—` = not applicable

### Rule 3 — Specification Tables
Used in Vol 2A Part IV item specifications:

```
| Attribute | Value |
|---|---|
| Item code | A-01 |
| Category | Acoustics |
| Populations | MOB, VIS, DEAF |
| Evidence tier | Tier 1 |
```

### Rule 4 — DAR / Cost Tables
Multi-column cost tables. Canonical 4-column format:

```
| Provision | At Construction | Retrofit Cost | Multiplier |
|---|---|---|---|
| Grab bar blocking | £40 (CAD <$68) | £3,000 (CAD $680–$5,100) | ~75× |
```

**Currency rules:**
- Use plain `£`, `$`, `€` — never escaped (`\$`, `\£`, `\~`)
- Use `–` (en-dash) for ranges, not `--`
- Use `~` for approximations, not `\~`
- Use `<` and `>` unescaped in table cells

### Rule 5 — No Cell Footnotes
Footnotes and notes do not belong inside table cells. Extract to below the table:

Exception: Short parenthetical codes like `(BAR: ≥1000 mm)` or `(→ Supp Vol IV)` are acceptable inline.

### Rule 6 — No Grid/Pandoc Tables
Grid tables (space-padded columns with `----` separators) must be converted to pipe tables.

Grid table wrapping is the #1 source of broken table display. Conversion is mandatory.

### Rule 7 — Bold and Emphasis in Cells
- `**bold**` is permitted in cells for item codes and stage designations
- `*italic*` is permitted for notes
- Never use `***bold italic***` in cells — renders inconsistently
- Stage criticality: `**SD**`, `**CD-CRITICAL**` — acceptable

### Rule 8 — Long Cell Content
If any single cell exceeds ~120 characters, consider:
1. Can the content be split into two rows? (preferred)
2. Can a footnote extract the long text? (second choice)
3. If neither: keep as-is, note in audit log

---

## Breakage Detection Checklist

Run this check on every file after any edit pass:

| Check | Pattern to detect | Action |
|---|---|---|
| Grid table rows | Line matches `^  ----+` | Convert entire table to pipe format |
| Missing opening pipe | `^[A-Z\*]` inside table block | Add leading `|` |
| Column count mismatch | `\|` count ≠ header row | Fix row or extract footnote |
| Escaped currency | `\$`, `\£`, `\~`, `\<`, `\>` in table cell | Remove backslash |
| Cell wrapping (grid legacy) | Two-line cell with whitespace indent | Merge to single pipe row |
| Footnote in cell | `*Note:` or `*Sources:` inside `|...|` | Extract below table |
| BAR column in matrix | `BAR` column header in matrix table | Flag for author decision — do not auto-remove |
| Missing separator row | No `|---|` after header | Insert `|---|---|...` |

---

## Conversion Procedure: Grid → Pipe

1. Identify boundaries (lines of `----` dashes)
2. Extract header row (first non-dash row)
3. Merge multiline grid cells into single pipe cells
4. Write as pipe table with `|---|---|` separator
5. Unescape: `\$`→`$` · `\£`→`£` · `\~`→`~` · `\<`→`<` · `\>`→`>`

---

## Execution Protocol

### Mode A — Full File Audit
Input: one markdown file  
Output: corrected file + audit log (counts of each fix type)

1. Scan file for all table blocks (pipe and grid)
2. Apply Rules 1–8 to each table
3. Log: tables found, tables converted, cells fixed, footnotes extracted
4. Write corrected file
5. Checkpoint: `[TABLE-AUDIT] {filename}: {n} tables, {x} grid→pipe, {y} escapes, {z} footnotes extracted`

### Mode B — Targeted Fix
Input: specific table(s) identified by line number or section heading  
Output: corrected table(s) only

### Mode C — New Table Generation
Input: data (list, dict, or prose description)  
Output: correctly formatted pipe table in canonical style

Always confirm table type before generating:
- Population matrix → Rule 2
- Specification attributes → Rule 3
- Cost/DAR → Rule 4
- General reference → Rule 1

---

## Token Efficiency

- Process grid→pipe conversion with Haiku 4.5 (pattern substitution, no judgment needed)
- Use Sonnet 4.6 only for: ambiguous multi-line cell merges, footnote extraction decisions
- Process files in sections of ≤400 lines to avoid context overflow
- Use `haiku-chunker` if file >500 lines before running Mode A

---

## Integration Points

- Run after: `item-specification-writer`, `supplemental-integrator`, any bulk str_replace pass
- Run before: `guidebook-auditor` (Mode A format check), `docx` conversion
- Output feeds into: `guidebook-auditor` checkpoint, final editorial pass (Stage 9)
