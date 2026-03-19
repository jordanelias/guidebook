---
name: markdown-formatter
description: >
  Enforce consistent markdown heading hierarchy and formatting conventions throughout
  any guidebook volume — correcting heading levels, fixing escaped markdown artifacts,
  standardising bold/italic application, and repairing list formatting errors. Distinct
  from structure-auditor (which audits and reports) — this skill corrects. ALWAYS use
  this skill when asked to: fix heading levels, enforce heading hierarchy, correct markdown
  inconsistency, repair escaped markdown, standardise H levels, apply consistent formatting,
  fix bold or italic misuse, repair list styles, or enforce the Volume→Part→Section→
  Subsection→Item markdown hierarchy. Trigger on: "fix heading levels", "heading hierarchy
  wrong", "markdown inconsistent", "escaped markdown", "H levels wrong", "enforce heading
  structure", "bold misused", "formatting pass", "markdown pass", "standardise the
  markdown", "headings are off", "fix the markdown", "heading levels inconsistent",
  or after any document conversion from .docx or other formats where markdown may have
  been corrupted or escaped. Run after structure-auditor (audit first, correct second).
---

**Model:** Haiku 4.5 — pattern matching and substitution only; no content judgment  
**Input:** section map (from haiku-chunker) + document chunk (≤500 lines)  
**Output:** corrected chunk + change log per chunk  
**Rule:** Never change heading text. Only change heading level (number of `#` characters) or fix escaping artifacts.

---

## Heading Hierarchy — Canonical Map

This guidebook uses the following heading level convention. Apply it without exception.

| Level | Markdown | Scope |
|---|---|---|
| H1 `#` | Volume | One per volume + title page. No H1 within a volume body. |
| H2 `##` | Part | Major divisions within a volume (Part I, Part II, Category A, Appendix A) |
| H3 `###` | Section | Named sections within a part (§1.1, §2.3, A-01) |
| H4 `####` | Subsection | Named subsections within a section (§1.4.1, sub-specifications) |
| H5 `#####` | Item sub-element | Evidence tables, cross-reference blocks, conflict notes — use sparingly |

**Item specification headings** (`### A-01 Title`) are H3. Sub-elements within an item (Specification, Evidence basis, Cross-references, Retrofit note) are H4.

---

## Correction Rules

### Rule 1 — No escaped headings
Escaped markdown headings (`**# Heading**`, `**## Heading**`) must be unescaped.  
- `**# Volume 1**` → `# Volume 1`  
- `**## Part I**` → `## Part I`  
- Do not touch bold text that is not a heading (`**Key term:**` in body text is correct and stays).

### Rule 2 — No H1 within volume body
After the volume H1, no H1 should appear until the next volume. Any H1 found within a volume body is demoted to H2.  
Exception: title-page H1 (`# Guidebook for Accessible Design`) — retained.

### Rule 3 — No heading level skips
An H4 must not appear without a parent H3. An H3 must not appear without a parent H2. If a skip is detected, check the section map before correcting — the parent heading may have been deleted and the orphaned child needs flagging, not auto-promotion.

### Rule 4 — No values in headings
Specification values, thresholds, and ranges must not appear in H3 or H4 headings. If found:
- Flag as `[VALUE-IN-HEADING — prose-style-checker action required]`
- Do not rewrite the heading — pass to prose-style-checker

### Rule 5 — ALL-CAPS headings → Title Case
ALL-CAPS headings (`## CATEGORY A: ACOUSTICS`) are standardised to Title Case (`## Category A: Acoustics`).  
Exception: Acronyms within headings retain all-caps (`## CRPD Framework Alignment` → `## CRPD Framework Alignment`).

### Rule 6 — Consistent bold usage
- `**Term:**` (key term followed by colon) — correct; retain
- `**Entire paragraph wrapped in bold**` — incorrect; remove outer bold, retain any inner bold on specific terms
- `**heading text**` not on a heading line — check if it should be an H3/H4; if yes, convert; if no, remove bold

### Rule 7 — List formatting
- Unordered lists: `- item` (hyphen + space). Not `* item`, not `• item`.
- Ordered lists: `1. item`. Not `1) item`.
- No mixed list markers within a single list block.
- Nested lists: indent 2 spaces per level.

---

## Change Log Format

For each chunk, produce a change log before writing the corrected output:

```
CHUNK: [chunk label / line range]
CHANGES:
  [line N]: ## CATEGORY A → ## Category A (Rule 5 — ALL-CAPS → Title Case)
  [line N]: **## Part I** → ## Part I (Rule 1 — escaped heading)
  [line N]: #### §1.4 → ### §1.4 (Rule 3 — heading level skip: no parent H3 found)
  [line N]: [VALUE-IN-HEADING] ### A-03 Acoustic Door (STC ≥35) — flagged for prose-style-checker
NO_CHANGE: [N lines unchanged]
```

Write the change log before producing the corrected output. If no changes needed, report `NO_CHANGE` and stop.

---

## Escalation Triggers

Stop and confirm with user:

- A heading level violation cannot be resolved without knowing what the parent heading was (parent is absent — possible deletion) — flag and wait; do not auto-promote
- Rule 5 (ALL-CAPS → Title Case) would change an acronym that is ambiguous — flag for confirmation
- More than 50 heading level violations in a single chunk — indicates a conversion artifact rather than individual errors; confirm the source of the corruption before bulk-correcting

---

**Preceded by:** `structure-auditor` (audit before correction)
**Feeds into:** `guidebook-auditor` Mode A · `prose-style-checker` (heading text rewrites)
