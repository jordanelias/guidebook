---
name: file-splitter
description: >
  Decompose a master guidebook document into per-Part and per-Category .md files for
  the v10.1 multi-file architecture. ALWAYS use this skill when asked to: split the
  master document into parts, decompose the guidebook into separate files, create
  per-Part files, create per-Category files, prepare for multi-file architecture,
  or break a monolithic document into its component parts. Trigger on: "split the
  document", "decompose into parts", "create part files", "file architecture",
  "per-Part files", "break into files", "multi-file split". Phase 4 skill — runs
  after content is final, before cross-reference resolution.
---

**Model:** Haiku 4.5 for splitting · Sonnet 4.6 for validation
**Input:** Assembled master document + section map (from haiku-chunker Mode A)
**Output:** Per-Part .md files + per-Category .md files + manifest file + split log
**Prerequisite:** Content must be final. Do not split a document that will undergo further content edits.

---

## 1. Split Architecture

v10.1 produces two levels of files:

| Level | Scope | Filename pattern | Example |
|---|---|---|---|
| Part | One Part per file | `parts/v10/part-{NN}.md` | `parts/v10/part-01.md` |
| Category | One Item Specification Library category per file | `parts/v10/part-07/cat-{X}.md` | `parts/v10/part-07/cat-A.md` |
| Front matter | Title, version, ToC, reading paths | `parts/v10/front-matter.md` | — |
| Back matter | Bibliography, glossary, appendices | `parts/v10/back-matter.md` | — |
| Supplementary | Supplementary volume(s) | `parts/v10/supp-{name}.md` | `parts/v10/supp-body-sizes.md` |

Part 7 is the only Part that decomposes to Category level. All other Parts remain single files.

---

## 2. Split Procedure

**Stage 1 — Load section map.** Read the section map produced by haiku-chunker Mode A. Identify all H1 (Volume) and H2 (Part) boundaries with line numbers.

**Stage 2 — Identify split points.** For each Part boundary:
- Record the line number of the Part heading
- Record the line number of the next Part heading (or end of document)
- Extract the content between those boundaries

**Stage 3 — Split Part 7 into Categories.** Within Part 7:
- Identify each Category heading (H3 level: `### Category [A-K]`)
- Split at each Category boundary
- Produce one file per Category

**Stage 4 — Extract front matter and back matter.**
- Front matter: everything before Part 1 heading
- Back matter: everything after the last Part heading (appendices, bibliography, glossary)

**Stage 5 — Write files.** For each split:
- Add a header comment: `<!-- Part {NN}: {Title} — split from master v10.1 [YYYY-MM-DD HH:MM] -->`
- Preserve all markdown formatting exactly — no reformatting on split
- Write to `parts/v10/` on GitHub using github-io

---

## 3. Manifest File

After splitting, produce `parts/v10/manifest.md`:

```markdown
# v10.1 File Manifest
**Split date:** YYYY-MM-DD HH:MM
**Source:** [master document filename]
**Total files:** [N]

| Order | File | Part | Title | Lines | Headings |
|---|---|---|---|---|---|
| 1 | front-matter.md | — | Front Matter | [N] | [N] |
| 2 | part-01.md | 1 | Foundations of Accessible Design | [N] | [N] |
| 3 | part-02.md | 2 | Disability Categories | [N] | [N] |
| ... | | | | | |
| [N] | back-matter.md | — | Back Matter | [N] | [N] |

## Part 7 Categories
| Order | File | Category | Title | Lines | Items |
|---|---|---|---|---|---|
| 1 | part-07/cat-A.md | A | [Title] | [N] | [N] |
| ... | | | | | |
```

The manifest is the authoritative assembly order for `chunk-assembler`.

---

## 4. Validation

After splitting, verify:

| Check | Method |
|---|---|
| Line count preservation | Sum of all split files = master document line count |
| No content loss | Concatenation of all split files (in manifest order) = master document |
| Heading count preservation | Sum of headings across splits = master heading count |
| No duplicate content | No line appears in more than one split file |

Report validation results. Any failure → stop and report; do not commit split files.

---

## 5. Escalation Triggers

- Master document has no clear Part boundaries → stop; document needs structure-auditor first
- Part 7 Category headings are inconsistent → stop; flag for structure-auditor
- Line count mismatch after split → stop; do not commit
- Master document is still in DRAFT state → stop; splitting is Phase 4 only

---

**Preceded by:** All Phase 3 writing complete · `structure-auditor` (confirm clean structure)
**Feeds into:** `cross-reference-resolver` · `chunk-assembler` (uses manifest for reassembly)
