---
name: structure-auditor
description: >
  Audit document heading hierarchy, section nesting, numbering sequences, and structural
  integrity in any technical guidebook or document. ALWAYS use this skill when asked to:
  check document structure, audit heading hierarchy, find orphaned sections, validate
  section numbering, check nesting depth, find structural inconsistencies, or review
  the skeleton of a document before a content pass. Trigger on: "check the structure",
  "heading hierarchy", "is the nesting right", "section numbering", "orphaned section",
  "structural audit", "document skeleton", "heading audit", "nesting check",
  "is the hierarchy consistent", or any task where structure must be verified before
  content editing begins. Distinct from guidebook-auditor Mode A: this skill operates
  on structure only, produces a structural map, and flags violations without touching
  content or format rules.
---

**Model:** Sonnet 4.6 — structural extraction and validation.
**Intake:** ≤500 lines. Full document → haiku-chunker Mode A first; feed section map to this skill.
**Output:** structural map + violation table. No content changes. No rewrites.

---

## What This Skill Checks

| Check | Description |
|---|---|
| Heading levels | H1 → H2 → H3 sequence; no skipped levels (e.g. H1 → H3) |
| Nesting depth | Flag sections nested >4 levels; recommend flattening |
| Orphaned sections | H3+ with no parent H2; H2 with no parent H1 |
| Numbering sequence | Numeric/alphanumeric sequences: gaps, duplicates, resets |
| Single-child sections | H2 with exactly one H3 child — structural redundancy flag |
| Empty sections | Heading present; no body content before next heading |
| Parallel structure | Sibling headings at same level: consistent grammatical form |
| Part/Section/Sub alignment | Part → Section → Sub-section label consistency |

---

## v10.1 Numbering Expectations

Section numbering follows Part number. Part N uses §N.x subsections.

| Part | Expected H2 pattern | Expected H3 pattern | Notes |
|---|---|---|---|
| 1 | §1.1–§1.x | §1.1.1–§1.x.x | Foundations |
| 2 | §2.1–§2.12 | §2.x.x | Disability categories; alphabetical by code |
| 3 | §3.1–§3.x | §3.x.x | Multiple categories |
| 4 | §4.1–§4.x | §4.x.x | Synthesis and sequencing |
| 5 | §5.1–§5.x | §5.x.x | Residential matrices |
| 6 | §6.1–§6.x | §6.x.x | Non-residential matrices |
| 7 | Category A–K | Item codes A-01, B-01, ..., K-01 | Item Specification Library |
| 8 | §8.1–§8.8 | §8.x.x | Cross-Population Resolution (NEW) |
| 9 | §9.1–§9.x | §9.x.x | Engineering and Coordination |
| 10 | §10.1–§10.5 | §10.x.x | Interdisciplinary Design Team |
| 11 | §11.1–§11.x | §11.x.x | DAR |
| 12 | §12.1–§12.x | §12.x.x | Economics |
| 13 | §13.1–§13.x | §13.x.x | Case Studies |
| Apps | Appendix A–E | — | Back matter |
| Supp | Supp. §1–§4 | — | Supplementary Volume |

Flag as 🔴 HIGH any section where the §-prefix does not match its Part number (e.g., §6.x appearing in Part 5 content).

When operating on per-Part files (`parts/v10/*.md`): validate numbering within the Part file scope. Cross-Part numbering conflicts are detected only on the assembled master document.

---

## Steps

**Stage 1 — Build Structural Map (Haiku)**
Extract all headings in document order.

Output map format:
```
Level | Number | Heading Text | Line | Parent | Children count | Body lines
```

Example:
```
H1  | 3       | Circulation  | 142  | —      | 4              | 2
H2  | 3.1     | Corridors    | 145  | 3      | 2              | 8
H3  | 3.1.1   | Width        | 154  | 3.1    | 0              | 12
H3  | 3.1.2   | Gradient     | 167  | 3.1    | 0              | 9
H2  | 3.2     | Ramps        | 177  | 3      | 1              | 3
H3  | 3.2.1   | Gradient     | 181  | 3.2    | 0              | 14
```

**Stage 2 — Run Violation Checks**
Apply each check in the table above to the structural map.

For each violation:

| ID | Check | Location | Heading | Issue | Severity |
|---|---|---|---|---|---|

Severity:
- 🔴 HIGH: skipped level, orphaned section, numbering gap/duplicate
- 🟡 MED: single-child section, empty section, nesting >4 levels
- 🟢 LOW: parallel structure inconsistency

**Stage 3 — Output**

1. **Structural map** (compact, full document)
2. **Violation table**
3. **Summary:** X headings · Y violations (Z 🔴 / W 🟡 / V 🟢) · Max nesting depth: N · Structural integrity: SOUND / MINOR ISSUES / REQUIRES RESTRUCTURE

---

**Scope boundary:** Structural extraction and violation flagging only — no rewrites. Content/framing/citations → separate skills. Heading wording → `prose-style-checker`. Table/figure numbering → `guidebook-auditor` Mode A.
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API
**Preceded by:** `haiku-chunker` Mode A  ·  **Feeds into:** `guidebook-auditor` · `workplan-orchestrator`
**Escalation:** ≥3 🔴 violations → GET `gap_register.md` + SHA, append REVIEW item, PUT back (Project Instructions §GitHub API)
