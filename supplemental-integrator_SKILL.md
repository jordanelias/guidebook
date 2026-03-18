---
name: supplemental-integrator
description: >
  Integrate a new supplementary volume into the Accessible Built Environments Guidebook suite.
  Updates population taxonomy, cross-references, gap register, and item codes across all volumes.
  Handles population code relocation (remove from disability taxonomy, register as supplementary code),
  Option A (full removal) or Option B (interim cross-reference) matrix strategies.
  Trigger on: "integrate supplementary volume", "integrate supp vol", "relocate population code",
  "add new population code", "remove [code] from taxonomy", "update cross-references for new volume",
  "supplement integration", any task where a new body-size, paediatric, or non-disability volume
  is being added to the guidebook suite.
---

**Model:** Sonnet 4.6 for all stages with framing judgment. Haiku 4.5 for extraction-only passes (Stage 3 chunking).
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API
**Intake:** confirm before starting — supplemental volume file · list of codes to relocate · Option A or B · target volumes in scope.
**Output:** amended .md files per volume + integration log (`supp_integration_log_[VOL-ID]_[DATE].md`)

---

## 0. Pre-Integration Checklist

Run before any file edits:

1. Confirm supplemental volume has a Section V (Guidebook Revision Notes) or equivalent amendment schedule. If absent: stop and request author to supply.
2. Extract from revision notes:
   - Codes to **remove** from disability taxonomy (list)
   - Codes to **add** as supplementary codes (list + sub-codes)
   - New gap register entries (YAML blocks)
   - Matrix strategy: Option A or Option B
3. Count BAR/code instances per target file. Log in integration plan.
4. Confirm no open P1 blockers in `gap_register.md` that conflict with taxonomy changes.

---

## 1. Stage 1 — Taxonomy & Standards Amendments

**File:** `project-standards.md` — GET + SHA before editing; PUT back after (Project Instructions §GitHub API)
**Model:** Sonnet 4.6

### 1a. Remove relocated code(s) from disability taxonomy table
- Locate the population taxonomy table.
- Remove the row(s) for codes being relocated.
- Add footnote immediately below the table:

> *[Code] design provisions (formerly listed as [old label]) are addressed in the Supplementary Volume "[Volume Title]," Section [X]. [Code] is not classified as a disability or impairment under this guidebook's taxonomy.*

### 1b. Register new supplementary-volume codes
- Locate or create a section: `## Supplementary Volume Population Codes`
- Add table with all new codes from the supplemental volume's V.3 (or equivalent):

| Code | Full name | Volume | Section |
|------|-----------|--------|---------|
| [code] | [label] | [supp vol title] | [section] |

- Add note: *These codes are supplementary-volume-specific and are not part of the main guidebook's disability taxonomy.*

### 1c. Gap register
- Add new gap entries (YAML) from supplemental volume revision notes → GET `gap_register.md` + SHA, append, PUT back (Project Instructions §GitHub API).
- Append only. Never overwrite existing entries.

---

## 2. Stage 2 — Vol 1 Amendments

**Files:** `vol1_v8_draft.md` (or equivalent Vol 1 draft)
**Model:** Sonnet 4.6
**Passes:** 2 (framing judgment required for §2.x population description rewrites)

### 2a. Population description section (§2.x for relocated code)
- Locate the population description section for the relocated code.
- Replace the full description with a relocation notice:

> **[Code label]** design provisions have been relocated to the Supplementary Volume *"[Volume Title],"* Section [X]. Large body size / [population] is not classified as a disability under this guidebook's taxonomy. See the supplementary volume for full design specifications.

- Retain the section heading and code reference for navigational continuity.

### 2b. Population taxonomy table (Vol 1 front matter or Part II)
- Remove the relocated code's row.
- Add footnote (same text as 1a).

### 2c. Comorbidity / interaction matrix (if present)
Apply **Option A or B** per intake:
- **Option A:** Remove the relocated code's row and column entirely. Add `*[Code] provisions: see Supplementary Volume, Section [X].*` below the matrix.
- **Option B:** Retain row/column heading. Change all cell entries to `→ Supp Vol [Section]`. Add matrix header note: `*[Code] provisions relocated: see Supplementary Volume, Section [X].*`

---

## 3. Stage 3 — Vol 2 Amendments (haiku-chunker required if >500 lines)

**Files:** `vol2a_draft_v8.md`, `VOLUME2_v72_DRAFT_S2.md` (and equivalent Vol 2 files)
**Model:** Haiku 4.5 for extraction/replacement; Sonnet 4.6 for any framing edits

### 3a. Item tag replacements
- For each item that had `[CODE]` in its population tag list:
  - **Option A:** Remove the tag entirely. Add to item notes: `*[Code] provisions: → Supp Vol [Section], [item code].*`
  - **Option B:** Change `[CODE]` tag to `[CODE]→ Supp Vol [Section]`
- Category L (or equivalent bariatric/relocated-code category) relabelling:
  - Change category header from `Category [X] — [Old Label]` to `Category [X] — [New Label] (see Supplementary Volume, Section [Y])`
  - Retain all item codes and specifications — do not delete.

### 3b. Structural/equipment specifications that reference the relocated code
- Do **not** remove structural or equipment specifications (e.g., 300 kg ratings, turning circle dimensions).
- Add a note to each: `*Specification retained for cross-reference. Population: see Supplementary Volume, Section [Y].*`

---

## 4. Stage 4 — Vol 3 + Room Matrices

**Files:** `vol3_v8_draft.md`, `sessions_3to6.md` (or equivalent)
**Model:** Haiku 4.5 sufficient for Option B; Sonnet if Option A

### 4a. Room matrices (Option B — standard interim)
For each matrix row/column with `[CODE]` entries:
- Change entry from specific dimension/provision to: `→ Supp Vol [Section], [item code]`
- Add matrix-level note (once per matrix, not per cell): `*[Code] provisions relocated to Supplementary Volume, Section [Y].*`

### 4b. Population code key (in-document keys)
Locate all in-document population code keys (format: `BAR = bariatric` or similar).
Replace with: `[CODE]: see Supplementary Volume "[Title]," Section [Y] — [description] design provisions`

---

## 5. Stage 5 — Verification Pass

**Model:** Haiku 4.5 (pattern matching)

1. Grep all amended files for the relocated code in isolation (e.g., `\bBAR\b`).
2. For each remaining instance: classify as:
   - ✅ CORRECT — relocation notice or cross-ref already in place
   - ⚠️ RESIDUAL — still appears as a disability code; flag for manual review
   - ℹ️ STRUCTURAL — retained for specification continuity; note in log
3. Flag any `RESIDUAL` instances to user; do not auto-correct.
4. Confirm new codes (CHD/LPA/EXH etc.) are registered in `project-standards.md` (GET to verify; PUT if update required).

---

## 6. Integration Log Output

`supp_integration_log_[VOL-ID]_[YYYY-MM-DD].md`

```markdown
# Supplemental Integration Log
**Volume:** [supplemental volume title]
**Date:** [YYYY-MM-DD HH:MM]
**Strategy:** Option [A/B]
**Codes relocated:** [list]
**New codes registered:** [list]

## Files Amended
| File | Changes made | Residuals flagged |
|------|-------------|-------------------|
| ... | ... | ... |

## Residual Instances (manual review required)
| File | Line | Context | Action required |
|------|------|---------|----------------|

## Gap Register Updates
[list of gap IDs added]

## Notes
[any deviations from skill protocol; blockers encountered]
```

---

## Token Rules
- Never re-read a file already processed in the same session. Use extraction output.
- haiku-chunker output for large files → consume chunks; do not re-chunk.
- Structural specs retained (never deleted) → note in log, not in main output.
- Integration log is the only new file created. All other outputs are amendments to existing files.
