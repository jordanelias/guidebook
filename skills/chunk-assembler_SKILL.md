---
name: chunk-assembler
description: >
  Final assembly of a guidebook document from working chunks, draft sections, or
  session outputs into a single coherent master file. ALWAYS use this skill when asked
  to: combine chunks into the master document, merge volume drafts, assemble a final
  output file, resolve cross-references across assembled sections, apply version numbering,
  or produce the publication-ready .md file from working parts. Trigger on: "assemble",
  "merge chunks", "combine sections", "final output", "produce the master file",
  "consolidate the drafts", or any request to combine multiple guidebook files into one.
  Always run before any .docx conversion. Do NOT use for editing content — this skill
  handles file assembly and integrity only.
---

**Model:** Haiku 4.5 for ordering and cross-ref extraction · Sonnet 4.6 for conflict resolution  
**Input:** section map (from haiku-chunker) + working chunk files + version record  
**Output:** single assembled .md file + assembly log + unresolved cross-ref list  
**Chunk ceiling:** Do not load all chunks simultaneously. Process in volume order; validate after each volume.

---

## 0. Pre-Assembly Requirements

Confirm all four before starting:

| Requirement | Check |
|---|---|
| Section map exists and is current | `references/section-map_[DOC-ID].md` present and reflects the latest structural state |
| All chunks are version-stamped | Each chunk file carries the session and date it was last edited |
| No chunk is in DRAFT/PENDING state | All chunks to be assembled are marked COMPLETE or REVIEWED |
| Version number confirmed | New version string ready (follow project version convention); supersession statement drafted |

If any check fails, stop and report to user.

---

## 1. Assembly Order

**Assembly order is derived entirely from the current section map — never hardcoded.**

Read the section map to determine:
- Volume sequence (H1 headings)
- Part sequence within each volume (H2 headings)
- Section sequence within each part (H3 headings)

Assemble in the order the section map specifies. If the section map and a chunk's internal heading conflict, flag the conflict — do not silently resolve it.

**Standard document zones** (derive positions from section map; do not assume fixed positions):
1. Front matter (title, version block, contents, section map, quick reference, reading paths)
2. Volume 1 parts in section-map order
3. Volume 2 parts in section-map order
4. Volume 3 parts in section-map order
5. Supplementary volumes in section-map order
6. Back matter (bibliography, glossary, index, appendices)

---

## 2. Cross-Reference Integrity Check

After assembly, run a grep pass for all internal cross-reference patterns:
- `§[0-9]` — section number references
- `V2-P4-XX` style item codes — validate against item heading list
- `Part [IVX]+` — part references
- `Appendix [A-Z]` — appendix references
- `Supplementary Volume` — supplementary volume references

For each cross-reference found:
- Confirm the target heading exists in the assembled document
- Flag any reference whose target heading is absent: `[BROKEN REF — target not found: "§X.Y"]`
- Do not auto-correct broken references — flag for cross-reference-resolver

---

## 3. Phantom Item Detection

Scan all cross-references for item codes that appear in cross-reference text but have no corresponding `### [CODE] — [Title]` heading in the document. List all phantom items:

```
PHANTOM ITEMS DETECTED:
  - [CODE]: referenced at lines [N, N, N] — no heading found
```

Phantom items are not auto-removed. Flag for author decision.

---

## 4. Version Record

Append to the assembled document's front matter:

```markdown
**Version:** [N]
**Date:** [YYYY-MM-DD]
**Supersedes:** [prior version]
**Assembly log:** [assembly-log_[DOC-ID]_[DATE].md]
**Status:** WORKING DRAFT / REVIEW / PUBLICATION CANDIDATE
```

Write a separate `assembly-log_[DOC-ID]_[DATE].md` recording:
- Chunk files assembled (filename + last-edited date)
- Chunks skipped and reason
- Cross-references flagged
- Phantom items detected
- Version record

---

## 5. Escalation Triggers

Stop and confirm with user before proceeding:

- Two chunks claim the same section heading — do not merge silently
- A chunk's internal heading hierarchy differs from the section map — do not reorder silently
- Any volume is entirely absent from the chunk set — confirm intentional omission
- Assembly produces a file >20,000 lines — confirm this is expected before writing

---

**Preceded by:** `haiku-chunker` (section map required)
**Feeds into:** `cross-reference-resolver` · `table-formatter` · `guidebook-auditor` Mode A
