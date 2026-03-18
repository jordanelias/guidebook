---
name: fix-linebreaks
description: >
  Fix broken paragraph lines in guidebook markdown files caused by hard-wrapped
  text export (typically from DOCX → MD conversion). ALWAYS use this skill when
  asked to: fix line breaks, fix broken paragraphs, join wrapped lines, clean up
  soft wraps, fix mid-sentence line breaks, or repair text that has been broken
  across lines. Trigger on: "fix line breaks", "broken paragraphs", "wrapped
  lines", "join lines", "line wrap", "mid-sentence breaks", "clean up the
  markdown", "the paragraphs are broken", or when a document has been freshly
  converted from DOCX and prose reads as one sentence per line. Run before any
  analysis skill that processes prose (framing-checker, prose-style-checker,
  evidence-auditor) if the source file is a DOCX conversion. Do NOT use for
  intentional line breaks within specification items or code blocks.
---

**Model:** Haiku 4.5 — mechanical transform, no judgment required
**Input:** any `.md` file with hard-wrapped prose
**Output:** `.md` file with broken lines joined; structural elements untouched
**Script:** Python script `fix_linebreaks.py` in the project scripts directory (confirm path from session context before running)
**Chunk ceiling:** none — script operates on full file in one pass

---

## Join rule

A single blank line between two content lines triggers a join if ALL of the following are true:

| Condition | Signal |
|---|---|
| Second line starts with lowercase letter, `(`, or bare digit | Continuation |
| Preceding line does not end with `.` `!` `?` | Sentence did not end |
| Neither line is a structural element | Not heading, table row, list item, code fence, blockquote |

Two or more consecutive blank lines → intentional separator → always preserved.

**Structural elements never joined:** ATX headings · table rows (`|`) · horizontal rules · code fences · blockquotes · list items (`* - + 1.`)

---

## Usage

Run the linebreak-fix script against the source file. Pass the input path and a distinct output path. Use `--inplace` only when explicitly directed by the user.

Confirm the script path from the session working directory before executing. Typical invocation:
- Input: the current working copy of the file (not the read-only project mount)
- Output: a new file in the session outputs directory

`--inplace` flag overwrites source. Omitting output path writes to `<input>.fixed.md`.

Report join count. Typical range for full-volume DOCX conversion: 800–1,500 joins. Outside this range → spot-check.

---

## Verification (run before presenting output)

1. Pick one `**Description:**` block — confirm text is a single line.
2. Pick one `**Specifications:**` block — confirm spec lines still separated by double blank lines.
3. Find one `**Key citations:**` entry that wrapped — confirm it is now a single line.

If any check fails: do not deliver output. Inspect failure pattern; adjust join rule before re-running.

---

## Workflow position

Run **before** haiku-chunker when input is a fresh DOCX conversion:

```
fix-linebreaks → haiku-chunker → [analysis skills]
```

Do not re-run on files already confirmed clean in the same session.
