---
name: find-and-replace
description: >
  Systematic text substitution across any guidebook volume or section — covering
  exact-string replacement, terminology updates, heading corrections, cross-reference
  fixes, and code/label migrations. ALWAYS use this skill when asked to: replace a
  term throughout the document, update a heading or section reference globally, fix a
  systematic naming error, migrate item codes, correct a repeated phrase, rename a
  volume or part, or apply any bulk textual change that appears in more than one location.
  Trigger on: "replace all", "update everywhere", "rename", "find and replace",
  "change X to Y throughout", "fix all instances", "migrate this label", "update this
  reference", "this appears multiple times", "bulk update", or when any correction
  identified in a gap register or style audit affects more than one location.
  Do NOT use for content rewrites, evidence changes, or framing corrections — those
  belong to prose-style-checker, framing-checker, or evidence-auditor respectively.
---

**Model:** Sonnet 4.6
**Input:** target document (chunked if >500 lines) + replacement specification  
**Output:** instance register (YAML) + validated replacement set + downstream impact table
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API  
**Chunk ceiling:** 500 lines per pass. Always run haiku-chunker first on full-document inputs.

---

## Stage 0 — Replacement Specification

Before any search, confirm all four elements with the user:

| Element | Description |
|---|---|
| **FIND** | Exact string, phrase, or pattern to locate. If ambiguous (e.g. acronym used in multiple senses), define disambiguation rule now. |
| **REPLACE WITH** | Exact replacement string. Confirm capitalisation, punctuation, and markdown formatting. |
| **SCOPE** | Which volume(s), part(s), or section(s) to search. Default: all. Narrowing scope reduces false positives and speeds validation. |
| **MATCH TYPE** | Exact · Case-insensitive · Regex · Semantic (requires Sonnet classification pass) |

Do not proceed to Stage 1 without confirmed spec. If user provides a partial spec, surface the missing elements as questions before proceeding.

---

## Stage 1 — Instance Discovery (Haiku)

Run a grep pass across all chunks within the defined scope. Produce the **Raw Instance Register**:

```yaml
find_and_replace:
  find: "[FIND string]"
  replace: "[REPLACE string]"
  scope: "[volume/part/section]"
  instances:
    - id: FR-001
      line: [line number]
      chunk: [chunk label]
      context: "[±2 lines of surrounding text]"
      classification: PENDING
    - id: FR-002
      ...
```

Report total instance count to user before proceeding. If count is unexpectedly high or low, stop and confirm scope is correct.

---

## Stage 2 — Classification (Sonnet)

For each PENDING instance, classify as one of:

| Class | Meaning | Action |
|---|---|---|
| **TARGET** | Correct instance of the pattern; should be replaced | Include in replacement set |
| **FALSE-POSITIVE** | String matches but context shows different meaning | Exclude; note reason |
| **AMBIGUOUS** | Cannot determine from context alone | Flag for user decision |
| **HEADING** | Instance is in a heading — replacement changes navigational structure | Flag separately; requires ToC and cross-ref update |
| **CODE** | Instance is an item code or internal identifier | Flag separately; requires volii-validator or cross-reference-resolver pass |

Update the instance register with classifications. Present AMBIGUOUS instances to user before proceeding.

---

## Stage 3 — Downstream Impact Assessment

Before executing replacements, identify all locations that will be affected by the change but do not contain the FIND string directly:

| Impact type | Check required |
|---|---|
| Table of Contents entries | Does ToC reference the old string? |
| Cross-references (narrative "see §X") | Does any section refer to the old label? |
| Item codes or identifiers | Does any V2-P4-XX code embed the old string? |
| Glossary definitions | Is the old term defined in the glossary? |
| Bibliography entries | Does the old string appear in source titles? |
| Section map / navigation aids | Does any reading path or entry path reference the old label? |

Produce the **Downstream Impact Table**:

| Location | Current text | Required update | Handled by |
|---|---|---|---|
| Table of Contents | "[old volume label]..." | → "[new volume label]" | This skill |
| Narrative cross-ref | "...see [old part label]..." | → "[new part label]" | This skill |
| Glossary entry | "[old term] definition..." | → Update | This skill |

If impact is in scope of another skill (e.g. volii-validator for item codes, cross-reference-resolver for narrative refs), note the handoff and do not duplicate effort.

---

## Stage 4 — Replacement Execution

Apply replacements in this order:
1. Body text — TARGET instances (in chunk order, not random)
2. Headings — HEADING instances (update immediately; flag ToC update required)
3. Downstream impacts in scope of this skill

**Never apply replacements to:**
- AMBIGUOUS instances without user confirmation
- FALSE-POSITIVE instances
- Items in scope of another skill's downstream pass (flag instead)

Log each applied replacement in the instance register: `classification: TARGET → APPLIED`.

---

## Stage 5 — Validation Pass

After all replacements applied:

1. Re-run the FIND pattern across the same scope. Expected result: 0 matches (or only confirmed FALSE-POSITIVES remaining).
2. If any unexpected matches remain, escalate to user — do not auto-apply.
3. Run a spot-check grep for the REPLACE string to confirm it appears in the expected locations.

Report:
```
Instances found:     [N]
Targets replaced:    [N]
False positives:     [N]  (excluded)
Ambiguous:           [N]  (pending user decision)
Downstream flagged:  [N]  (requires separate pass)
Validation:          PASS / FAIL [reason if FAIL]
```

---

## Stage 6 — Gap Register and Session Log Update

For each completed replacement operation, GET `gap_register.md` + SHA, append entry, PUT back (Project Instructions §GitHub API):

```yaml
- id: FR-[DATE]-[SEQ]
  type: find-and-replace
  find: "[FIND]"
  replace: "[REPLACE]"
  instances_replaced: [N]
  scope: "[scope]"
  downstream_open: [true/false]
  status: CLOSED
```

If downstream impacts are unresolved, open a new gap register item for each pending skill handoff.

---

## Escalation Triggers (stop and confirm with user)

- Instance count is >50 — confirm bulk replacement is intended before executing
- Any HEADING instance found — confirm ToC and navigation impact before replacing
- Any CODE instance found — pause; run volii-validator before proceeding
- FIND string appears in locked decisions or evidence hierarchy sections — confirm with user; these sections may have deliberate terminology choices
- Replacement would change a term that appears in a cited source title — flag; do not alter bibliographic references

---

## Relationship to Other Skills

Use this skill for mechanical substitution only. Framing/evidence corrections → `framing-checker` or `evidence-auditor` first. Item code changes → `volii-validator` validation pass. Broken ref repair → `cross-reference-resolver` audit first. Heading level changes → `structure-auditor`. Bibliography strings → do not alter.
