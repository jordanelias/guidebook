---
name: vol2-item-formatter
description: >
  Format, render, and validate Volume 2 Category Items in the canonical guidebook markdown
  format. ALWAYS use this skill when asked to: format a Volume 2 item, render a spec item
  to canonical format, convert a draft item into guidebook output, check whether an existing
  item conforms to the Volume 2 item template, or produce a publication-ready item block.
  Trigger on: "format this item", "render the item", "convert to guidebook format",
  "canonical item format", "Volume 2 item", "produce the item block", "does this item
  conform", "item template check", or whenever the deliverable is a structured item block
  with code, title, applicable groups, description, specifications, design stage, retrofit
  note, key citations, and cross-references. DISTINCT from item-specification-writer, which
  drafts content; this skill formats and validates output structure.
---

**Model:** Haiku 4.5 for structure validation; Sonnet 4.6 for content judgment (framing, heading rule, population code completeness)  
**Input:** Draft item content in any form (prose, structured notes, partial item block, completed item)  
**Output:** Publication-ready item block in canonical Volume 2 markdown format  
**Chunk ceiling:** ≤50 items per run. Larger batches → haiku-chunker first.

---

## Canonical Item Format

Every Volume 2 Category Item must follow this structure **exactly**, in this field order:

```markdown
### [CODE] [Title — Descriptive Only; No Values or Thresholds in Heading]

**Applicable Groups:** [population codes, comma-separated]

**Description:** [Prose summary of the provision. One paragraph. Includes key dimensional
parameters, material specs, and functional purpose. Written in soft imperative subjunctive
register. ≤80 words.]

**Specifications:**
- [Bullet 1 — concise, one claim per bullet]
- [Bullet 2]
- [...]
- [Final bullet — LRV, contrast, or sensory spec if applicable, with citation]

**Design Stage:** [Schematic Design / Design Development / Technical Architecture /
Construction Documents / Post-Occupancy]

**Retrofit:** [HIGH / MODERATE / LOW penalty description] — [Explanation of why retrofit
is penalised at this level. One to three sentences. Cross-reference to Part VII or Part VIII
section as applicable.]

**Key citations:**
[Author/Organisation. (Year). Title. Publisher/URL.]
[One citation per line. Minimum 2, maximum 6 per item.]

**Cross-reference:** [CODE (Label); CODE (Label); ...]
```

---

## Field Rules

### Code and Title
- Code format: `[Letter]-[NN]` (e.g., `E-01`, `G-03`, `D-07`)
- Title: descriptive label only. **No values, ranges, dimensions, or thresholds.**
  - ✓ `Accessible Lift (All Floors Served)`
  - ✓ `Grab Bars in All Accessible Bathrooms (Clinical Positioning and Bilateral)`
  - ✗ `Accessible Lift (1400×1100 mm Car, All Floors Served)` — dimensions in heading
  - ✗ `Grab Bars (32–45 mm Diameter, 200 kg Rated)` — specs in heading
- **Exception:** Parenthetical qualifiers that distinguish an item *type* (not a value) are permitted: `(Clinical Positioning and Bilateral)`, `(All Floors Served)`.

### Applicable Groups
- List only population codes that are **genuinely applicable** to the item.
- Use canonical codes only: MOB, VIS, VIS/DEAF, NEU, DEM, NDV, NDV/MH, PAIN, DBL, OFS, ALL
- Sub-codes (MOB/AMB, MOB/UPL, OFS/ME, etc.) may be used where specificity matters.
- BAR is **not** a main-taxonomy applicable group. Do not list BAR here. Large body size provisions belong in the supplementary volume cross-reference only.
- Do not list ALL unless the item genuinely serves every disability population.
- UPL is not a standalone code; use MOB/UPL.

### Description
- Prose, not bullets.
- Soft imperative subjunctive register: "to be", "not to exceed", "to provide".
- State the functional purpose and key parameters in one paragraph.
- ≤80 words. One sentence per claim where practical.
- No citations embedded in Description — citations belong in Key citations field.
- Note contrast/LRV requirement in Description only if it is a defining feature.

### Specifications
- Bulleted list.
- One claim per bullet. ≤25 words per bullet.
- **Evidence markers (mandatory):** Every specification bullet carries exactly one marker prefix.
  - `● ` (filled circle + space) = evidence-based — Tier 1–6 source directly supports this value
  - `○ ` (empty circle + space) = inferred — clinical reasoning, expert consensus, or extrapolation; gap disclosed
  - See `evidence-marker` skill for classification criteria.
- Dimensions in mm. Loads in kN. Contrast as LRV delta (≥30 LRV).
- Include unit on every numeric value.
- Where a spec references another item, include the item code in parentheses: `(VI-03)`.
- Citation may appear inline at end of bullet where it is the direct source for that value: `(JOTA, 2022)`.
- Do not duplicate Description content verbatim in Specifications — Specifications provide the structured enumerated form.

### Design Stage
- One of: `Schematic Design` · `Design Development` · `Technical Architecture` · `Construction Documents` · `Post-Occupancy`
- Where the item spans multiple stages, list all: `Schematic Design · Design Development`
- Design Stage identifies the **earliest** stage at which the provision must be decided or committed.

### Retrofit
- One of three penalty levels: `HIGH` · `MODERATE` · `LOW`
- Use the compound form: `**Retrofit:** HIGH penalty` or `**Retrofit:** LOW–MODERATE penalty`
- Follow with one to three sentences explaining the structural or technical driver of the penalty.
- Always cross-reference to Part 11 (DAR provisions) or Part 13 §13.x (case studies) as applicable.
- Do not estimate costs in dollar figures unless a verified citation supports the figure.

### Key Citations
- Minimum 2, maximum 6 citations per item.
- Format: `Author/Organisation. (Year). Title. Publisher.`
- One citation per line. No bullet prefix — plain lines.
- Real citations only. Unverified citations: append `[UNVERIFIED — DOI required]`.
- If fewer than 2 verified citations are available: append `[CITATION GAP — evidence-auditor referral required]`.

### Cross-Reference
- Format: `CODE (Label); CODE (Label)`
- Semicolon-separated on one line.
- Reference items in the same volume and supplementary volume codes where applicable.
- BAR provisions: cross-reference the supplementary volume item code (e.g., `SV-B-04`), not a main-volume BAR item.

---

## Validation Checklist

Run before finalising any item output:

| Check | Pass condition |
|---|---|
| Code format | `[Letter]-[NN]` — letter, hyphen, two digits |
| Heading rule | No values, ranges, or thresholds in title |
| Applicable Groups | Canonical codes only; no BAR; no UPL standalone |
| Description length | ≤80 words |
| Description register | Soft imperative subjunctive throughout |
| Specifications | One claim per bullet; ≤25 words; units on all numeric values; ● or ○ marker on every bullet |
| Evidence markers | Every spec bullet has exactly one ● or ○ prefix; no unmarked bullets |
| Design Stage | One of five permitted values |
| Retrofit | Penalty level stated; structural driver explained; cross-ref to Part 11 or Part 13 |
| Key Citations | ≥2 verified citations; unverified flagged |
| Cross-reference | Semicolon-separated; no BAR main-volume codes |

---

## Common Errors to Catch

1. **Values in heading** — move to Description or Specifications.
2. **BAR in Applicable Groups** — remove; add SV cross-reference if needed.
3. **Citation in Description field** — move to Key Citations.
4. **Dollar cost estimates without citation** — flag `[UNSUPPORTED — citation required]`.
5. **Retrofit penalty without structural explanation** — expand to one sentence minimum.
6. **Sub-codes collapsed** — e.g., `MOB` where `MOB/AMB` or `MOB/UPL` is the correct level of specificity.
7. **Missing Design Stage** — required on every item; infer from structural commitment point if not supplied.
8. **Duplicate content between Description and Specifications** — Description = prose summary; Specifications = enumerated values. They should complement, not repeat.

---

## Register

All output text to follow the project prose register:
- Voice: soft imperative subjunctive — "to be", "not to exceed", "to provide"
- No active imperative: not "install", "use", "ensure"
- Concision: ≤25 words per specification sentence; one claim per sentence
- No informal language in any field

---

## Escalation

Stop and flag to user if:
- Fewer than 2 verified citations available and item cannot be flagged as a gap item
- Applicable Groups list is ambiguous (e.g., draft says "all users")
- Design Stage cannot be determined from context
- Item code conflicts with an existing registered item code

---

**Preceded by:** `item-specification-writer` (drafts content) · `citation-verifier` (verifies citations)  
**Feeds into:** `framing-checker` · `prose-style-checker` · `volii-validator`  
**Parallel:** `evidence-auditor` (may run on same item concurrently)
