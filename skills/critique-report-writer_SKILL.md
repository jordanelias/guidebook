---
name: critique-report-writer
description: >
  Produce structured critique reports for versions of the Accessible Built Environments Guidebook.
  ALWAYS use this skill when asked to: write a critique, produce a review report, assess a guidebook
  version, evaluate evidence quality, generate a revision recommendation document, or produce any
  formal output assessing the guidebook. Trigger on: "critique", "review report", "assess this
  version", "write up findings", "generate critique", "produce the report". Outputs .md by default;
  use docx skill only if user explicitly requests Word format.
---

**Intake:** Confirm scope (version, sections, dimensions) before writing. Assemble upstream outputs only — do not re-run analysis. Missing upstream → note "Pending [skill-name]".
**Model:** Sonnet 4.6
**Output:** `Critique_Report_Guidebook_[Version]_[YYYY-MM-DD].md` · Word only if explicitly requested
**Severity:** 🔴 HIGH · 🟡 MED · 🟢 LOW · Status: ✅ CONFIRMED · ⚠️ UNSUPPORTED · ❌ NOT_FOUND
**Sources:** content-gap-analyzer · citation-verifier · guidebook-auditor · multilingual-research · evidence-auditor · framing-checker

## Report Structure

**Front Matter:** Title, date, reviewer, scope. Executive summary ≤300 words: overall assessment, top 3 strengths, top 3 critical issues.

**§1 Evidence Accuracy** (citation-verifier): citation counts (confirmed/unverified/not found/mismatch) · flagged citations with replacements · OT case study coverage · rating: STRONG/ADEQUATE/WEAK/INSUFFICIENT

**§2 Bias Review** (content-gap-analyzer heatmap): for each type — instances · severity · corrective action.
Types: population · geographic · recency · design paradigm · language

**§3 Educational Value:** per section — comprehensible to non-specialist? · actionable criteria? · examples? · rationale explained? · OT context?
Rating: CLEAR / NEEDS CLARIFICATION / INACCESSIBLE

**§4 Usability** (guidebook-auditor): navigation · findability by trade · format/terminology consistency · quick-reference features

**§5 Utopianism** (evidence-auditor): flag — aspirational without evidence · criteria exceeding standards without justification · missing cost/feasibility context · mandatory vs. best practice confusion.
Distinguish: evidence-based aspiration (OK) vs. unsupported idealism (flag)

**§6 Standards & Specifications** → `references/critique-standards-section.md`

**§7 Citation Audit Table** (citation-verifier):
| ID | Section | Claim | Original Citation | Status | Recommended Replacement |

**§8 Information Gaps:** missing evidence · unverified citations · content gaps by population · sections requiring redevelopment.
Each: description · severity · next action · skill to deploy

**Appendix: Multilingual Evidence Summary** (multilingual-research): non-English sources grouped by language/jurisdiction
