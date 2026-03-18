---
name: haiku-chunker
description: >
  Pre-process full guidebook documents into task-specific chunks and indexes for analysis skills.
  ALWAYS use this skill when a full document (>500 lines) is provided and needs to be analyzed by
  any analysis skill. Trigger on: full document provided to any skill, "chunk this document",
  "prepare for analysis", "extract sections", "build section map", or when any analysis skill
  refuses a full-document input and requests chunking first.
---

**Model:** Haiku 4.5. Chain of Draft: max 5 words per reasoning step. Structural extraction only — no content judgment.
**Requires:** document version label for section map naming.

## Modes
**A – Section Map:** extract all headings → `references/section-map.md` (output file; reuse across sessions; regenerate only on version change)
Format: `| Heading | Level | Line range | Est. tokens | Parent |`

**B – Section Extraction:** extract sections by heading or line range → `chunk_[section-code]_[slug].md`
Target: 200–500 lines/chunk. Split at sub-heading boundaries if >500 lines.

**C – Citation Extraction:** extract all citation strings → `citations-raw.md`
Format: `[line] | [citation string] | [5 words context before/after]`
Extraction only — no verification. Feed to citation-verifier.

**D – Item Code Extraction:** extract all Vol II codes (A-01, B-10 pattern) → `item-codes-raw.md`
Format: `[line] | [code] | [heading context] | [declared categories if visible]`
Extraction only — no assessment. Feed to volii-validator.

## Output
Confirm modes with user. Report: sections found · chunk count · estimated tokens/chunk.
