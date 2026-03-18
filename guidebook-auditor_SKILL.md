---
name: guidebook-auditor
description: >
  Audit accessibility guidebook documents for format consistency, structural integrity, style compliance,
  and section-level quality. ALWAYS use this skill for: format checks, consistency reviews, structural
  audits, heading hierarchy reviews, cross-reference validation, terminology consistency, table/figure
  numbering checks, glossary audits, and any task asking "is this document consistent" or "audit this
  section". Designed for repeated use on Accessible Built Environments Guidebook versions.
---

**Intake:** ≤20 sections per run. Full document → haiku-chunker first.
**Model:** Haiku 4.5 (Modes A/C/E extraction) · Sonnet 4.6 (Mode B/D judgment)
**Section map:** GET `references/section-map.md` before first scan; PUT back after update (Project Instructions §GitHub API). Reuse until version changes.
**Mode A requires:** `references/format-rules.md` — stop and flag if missing.
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API

## Modes
**A – Format & Structure:** heading hierarchy · section numbering · table/figure numbering + captions · note/caution box consistency · cross-reference format
**B – Terminology:** flag deprecated terms ("wheelchair-bound", "suffers from", "special needs") · acronym first-use · person-first vs. identity-first inconsistency (flag; do not auto-correct) → GET/PUT `references/terminology.md` on GitHub (Project Instructions §GitHub API)
**C – Cross-Reference Integrity:** internal section refs exist · figure/table callouts exist · standards format consistency
**D – Content Completeness:** each section has — purpose statement · ≥1 evidence rationale · measurable criteria · ≥1 example · cross-references. Flag absent elements only.
**E – Glossary:** term consistent with body text? · jurisdiction-variable terms flagged? · deprecated terms present? · OT terms aligned with current practice frameworks? · terms used in body but absent from glossary?

## Output
**Audit Report: [Document] [Sections] [Mode(s)] [Date]**
| # | Location | Mode | Issue | Severity | Recommendation |

Summary: X issues — Y 🔴 / Z 🟡 / W 🟢
