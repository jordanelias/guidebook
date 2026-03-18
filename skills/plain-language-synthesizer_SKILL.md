---
name: plain-language-synthesizer
description: >
  Produce plain-language summaries of Accessible Built Environments Guidebook sections for
  practitioner audiences. Targets Flesch-Kincaid Grade 8–9. Summaries are 3,000–5,000 words
  and cover the essential design requirements, evidence rationale, and OT application of a
  full guidebook Part or Chapter. ALWAYS use this skill when asked to: write a plain-language
  summary, produce a practitioner digest, create a non-specialist version, simplify a guidebook
  section, or produce a Stage 8 output. Trigger on: "plain language summary", "practitioner
  summary", "simplify this section", "plain language version", "readable summary", "Stage 8",
  "digest", "non-specialist version", "FK Grade 8".
  DISTINCT from practice-note-generator (field tools) — this skill produces full narrative
  summaries for practitioners who need to understand a section, not checklists or briefs.
---

**Model:** Sonnet 4.6
**Input:** haiku-chunker output for the target section/Part + upstream skill outputs (framing-checker, evidence-auditor)
**Output:** `.md` summary file (3,000–5,000 words; FK Grade 8–9)
**Audience:** Occupational therapists and architects without specialist research backgrounds
**Chunk ceiling:** ≤500 lines input. Full Part → haiku-chunker first.

---

## Governing Principles

- **Plain language, not dumbed-down.** Preserve technical precision; replace jargon with plain equivalents where possible. Define unavoidable technical terms on first use.
- **Social model framing throughout.** The built environment creates barriers. Disability is not a personal deficit. Mirrors framing-checker rules — run framing-checker on upstream input before synthesizing.
- **Evidence-grounded but accessible.** Every major recommendation should be traceable to evidence, stated simply. Do not strip citations — translate them: "Research across six countries shows..." not "(Smith et al., 2023)".
- **No ABSENT-stratum fabrication.** Where evidence is absent or thin, say so plainly: "There is currently little research on this for [population]. The guidance here is based on clinical experience and professional consensus."
- **OT application prominent.** Each section should include a paragraph on what this means for OT assessment and practice.

---

## Flesch-Kincaid Grade 8–9 Rules

Apply throughout. Check before delivering output.

| Rule | Target |
|---|---|
| Average sentence length | ≤15 words |
| Average syllables per word | ≤1.7 |
| Passive voice | ≤10% of sentences |
| Paragraph length | 3–5 sentences |
| Technical terms on first use | Always define inline |
| Headings | Descriptive, plain — no jargon |

---

## Structure

Every plain-language summary contains the following sections. Adjust section order if the source Part has a different logical flow, but do not omit sections.

### 1. What This Section Covers (100–150 words)
One paragraph. Plain statement of scope: which spaces, which populations, which design elements.

### 2. Why It Matters (200–300 words)
Connect to everyday occupational performance. Use concrete examples. Avoid clinical abstraction.
Example: "For a person using a power wheelchair, a doorway that is 50 mm too narrow means they cannot enter their own bathroom without assistance — a loss of privacy and independence that accumulates daily."

### 3. Key Design Requirements (600–900 words)
Summarise the main specifications in plain language. Group by logical theme (e.g., Entry and Approach · Interior Circulation · Bathroom · Kitchen). For each requirement:
- State the requirement in one plain sentence
- Give the key dimension or standard (e.g., "doorways to be at least 850 mm wide")
- Explain why in one sentence
- Flag if Tier 0 (applies everywhere) or Tier 1 (for buildings serving identified populations)

### 4. The Evidence Behind This (400–600 words)
Summarise the evidence base accessibly. Note: where evidence is strong (multiple independent studies); where it is emerging (early research, expert consensus); where it is absent (professional judgment only). Be honest about gaps.

### 5. What This Means for OT Practice (400–600 words)
Two sub-sections:
- **Assessment:** what to look for in a site assessment, framed as observable criteria
- **Advocacy:** how to use this guidance to advocate for design changes in pre-occupancy planning, renovation briefs, or new builds

### 6. Common Mistakes (200–300 words)
Three to five common design errors for this section. Plain statement of each: what goes wrong, why, and what to specify instead.

### 7. Further Reading (100–150 words)
Three to five resources the practitioner can consult for more depth. Favour accessible formats (guidelines, practice frameworks, summary documents) over academic papers.

---

## Quality Check (run before delivering output)

1. Paste summary into Flesch-Kincaid calculator. Confirm Grade 8–9. If Grade >9: identify longest sentences and most complex vocabulary; revise.
2. Read aloud at moderate pace. Any sentence requiring a second reading → simplify.
3. Check: does the summary contain any ABSENT-stratum claims presented as established fact? If yes → revise with appropriate qualification.
4. Check: does every numbered specification in §3 match the source document? Do not paraphrase dimensions — copy exact values.
