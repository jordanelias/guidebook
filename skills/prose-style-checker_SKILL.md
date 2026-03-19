---
name: prose-style-checker
description: >
  Audit and rewrite guidebook text to conform to the project prose register: soft imperative
  subjunctive ("to be", "to provide"), descriptive headings (no values in headings), qualitative
  sequencing (Ideal → Best Practice → Acceptable → Minimum) at item level, concise evidentiary
  sentences, no hedging. ALWAYS use this skill when asked to: check writing style, audit prose
  register, fix hedging language, rewrite for concision, apply style rules, enforce subjunctive
  voice, check sentence structure, or review text before publication. Trigger on: "check the
  style", "fix the writing", "apply the style guide", "too wordy", "too hedging", "rewrite this
  section", "prose audit", "style pass", "register check", "is this too passive", "fix the voice".
  Use proactively on any section being drafted or revised before it is packaged.
---

**Model:** Sonnet 4.6
**Intake:** ≤500 lines. Full document → haiku-chunker first.
**Passes:** 2. Pass 1: flag. Pass 2: rewrite flagged items. Do not rewrite what is not flagged.
**Output:** flagged item table + corrected text block. No commentary outside the table.

---

## Register Specification

### Voice
Soft imperative subjunctive. The construction "to be + [value/condition]" is the canonical form.

| Wrong | Correct |
|---|---|
| The door shall be 900 mm wide | The door width to be 900 mm |
| It is recommended that contrast be ≥30 LRV | Surface contrast to be ≥30 LRV |
| Designers should consider acoustic separation | Acoustic separation to be provided |
| Must not exceed 1:20 | Gradient not to exceed 1:20 |
| We recommend a minimum of 1500 mm | Turning circle to be ≥1500 mm |

Negation: "not to be", "not to exceed", "not to reduce below".
Passive with unknown actor: rewrite to subjunctive. Passive with known actor: keep if cleaner.

### Headings
Descriptive only. Values, ranges, and thresholds belong in the specification text, not the heading.

| Wrong | Correct |
|---|---|
| Door Width: 850–900 mm | Door Width |
| Contrast ≥30 LRV | Surface Contrast |
| Turning Circle (min 1500 mm) | Turning Circle |

### Qualitative Sequencing
At item level, where multiple tiers of provision exist, sequence as:
**Ideal → Best Practice → Acceptable → Minimum**

Not all tiers are required for every item. Use only the tiers that apply.
Do not label tiers with those exact words unless the guidebook uses them explicitly — sequence the content in that order and let the reader infer the gradient.

Example structure:
> Turning circle to be 1800 mm unobstructed.
> Where space is constrained, 1500 mm with passing place at ≤10 m intervals.
> 1200 mm acceptable in retrofit of existing fabric only.
> 900 mm absolute minimum; not to be used in new build.

### Concision
- Sentences in specification text: ≤25 words as target.
- One claim per sentence.
- No preamble ("It is important to note that...", "It should be borne in mind...").
- No hedge stack ("may potentially be considered appropriate in some cases").
- No redundant qualifiers ("very", "quite", "fairly", "relatively").

### Evidentiary Grounding
- Every prescriptive claim to carry a citation or evidence tier marker, or be flagged.
- Unsupported prescriptions: flag `[UNSUPPORTED — citation required]`.
- Do not soften unsupported claims — flag them and leave prescription intact pending evidence.

---

## Flag Categories

| Code | Flag | Example |
|---|---|---|
| IMPERATIVE | "shall", "must", "should" constructions | "The ramp shall not exceed 1:20" |
| RECOMMENDATION | "it is recommended", "designers should consider" | "It is recommended that..." |
| HEDGE | Uncertainty softening without evidence basis | "may be appropriate", "could potentially" |
| PREAMBLE | Introductory padding before the claim | "It is important to note that contrast..." |
| VALUE_IN_HEADING | Numeric or threshold value in heading | "Door Width: 850 mm" |
| PASSIVE_ACTOR | Passive voice where actor is known | "Grab bars are to be installed by..." |
| SEQUENCE_VIOLATION | Tiers out of order or better-than-minimum stated last | Minimum stated before Ideal |
| UNSUPPORTED | Prescriptive claim with no citation | Any specification claim without source |
| OVERLONG | Sentence >35 words | Any run-on specification sentence |

---

## Steps

**Pass 1 — Flag**
1. Scan for each flag category. Record: exact quote · location (heading/line reference) · flag code · severity.
   - 🔴 HIGH: IMPERATIVE, RECOMMENDATION, VALUE_IN_HEADING, SEQUENCE_VIOLATION
   - 🟡 MED: HEDGE, PREAMBLE, PASSIVE_ACTOR, UNSUPPORTED
   - 🟢 LOW: OVERLONG

2. Output flag table:

| ID | Location | Code | Original Text | Severity |
|---|---|---|---|---|

**Pass 2 — Rewrite**
Rewrite flagged items only. Do not alter unflagged text.
For each flagged item: produce corrected version in register.
For UNSUPPORTED: retain claim, append `[UNSUPPORTED — citation required]`. Do not soften.
For SEQUENCE_VIOLATION: reorder tiers; do not alter the specification values.

Output corrected text block in full, with flagged items replaced. Mark each correction inline: `{FIXED: [code]}`.

---

## Output Format

**Section:** [heading]
**Flags found:** X total — Y 🔴 / Z 🟡 / W 🟢
**Register rating:** CLEAN / MINOR CORRECTIONS / SIGNIFICANT REWORK REQUIRED

Flag table (Pass 1).
Corrected text block (Pass 2).

---

## Integration

- Run before: `critique-report-writer`, `practice-note-generator`, final editorial pass
- Run after: `framing-checker` (framing fixes may change sentence structure requiring style pass)
- Output feeds: `find-and-replace` (mechanical substitutions) · `item-specification-writer` (revised items) · `critique-report-writer` (final style rating)
