---
name: practice-note-generator
description: >
  Generate practitioner-facing field tools from Accessible Built Environments Guidebook findings.
  ALWAYS use this skill when asked to: write a practice note, generate a site visit checklist,
  create OT reference material, write practitioner guidance, produce a design brief prompt,
  or create field tools for occupational therapists or architects.
  Trigger on: "write a practice note", "generate field tool", "create OT reference",
  "practitioner guidance", "site visit checklist", "design brief prompt".
  Output is for OT practitioners and design teams — NOT for critique reports or authors.
---

**Model:** Sonnet 4.6
**Intake:** Requires (a) design element or population focus AND (b) source skill output. If neither → ask before proceeding.
**No ABSENT-stratum claims in output. EMERGING claims → "emerging evidence suggests..."**
**Language:** occupation-based, plain language (Flesch-Kincaid ≤10). Dimensions in mm; imperial in parentheses.
**Output:** `PracticeNote_[Element]_[Population]_[YYYY-MM-DD].md` · Word only if explicitly requested.

## Output Types

**Type A — Two-Page Practice Note:**
1. What this covers (1 sentence)
2. Why it matters for occupational performance (3–5 sentences, CMOP-E or MOHO framing)
3. Site assessment checklist (observable criteria)
4. Design brief language (for architect/planner)
5. Evidence basis (cited, tiered)
6. When to escalate (red flags requiring specialist OT assessment)

**Type B — Site Visit Checklist:**
Yes/no observable criteria grouped by functional area. Measurement criteria in mm where relevant (PTV, LRV). Guidebook item codes in margin notes.

**Type C — Design Brief Prompt:**
Brief-stage appropriate (concept / developed / technical). Design intent language — not clinical. Include guidebook item codes for traceability.
