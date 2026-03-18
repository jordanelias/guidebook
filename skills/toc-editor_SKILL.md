---
name: toc-editor
description: >
  Edit the canonical Table of Contents (references/toc.md on GitHub) and generate a
  structured Change Order for the guidebook. ALWAYS use this skill when the user issues
  any statement that would change the structure, labelling, codes, or nomenclature of the
  Guidebook — including removing sections or items, renaming parts or categories,
  renumbering codes, moving content between volumes, adding new entries, or changing
  cross-references. Trigger on: "remove", "rename", "move", "add", "relabel", "renumber",
  "cross-reference to", "retitle", any statement referencing a Part, Section, Volume,
  Category, item code, or section identifier followed by a structural verb.
  DO NOT use for content edits within existing items — use item-specification-writer for
  those. This skill is for structural and nomenclature changes only.
---

# toc-editor

**Purpose:** Maintain `references/toc.md` as the canonical structural record of the Guidebook, and generate typed Change Orders that downstream skills (`find-and-replace`, `cross-reference-resolver`) can execute against the primary document.

**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API  
**Managed file:** `references/toc.md`  
**Change Order output:** `references/change-orders/CO-{NNNN}-{YYYY-MM-DD-HHMM}.md` (new file per operation batch)  
**All timestamps: `YYYY-MM-DD HH:MM`**

---

## Operation Taxonomy

Every directive maps to one of these typed operations. Parse the user's natural-language statement to classify before acting.

| Code | Operation | What it means |
|---|---|---|
| `REMOVE` | Delete entry | Remove a volume, part, section, subsection, or item entirely from the ToC and issue instructions to remove or redirect the corresponding content in the guidebook |
| `RENAME` | Change label/title | Change displayed name, title, or heading text without moving or removing content |
| `RECODE` | Change code/identifier | Change an item code, section number, part letter, or category prefix (e.g. J → BAR, §E.4.3 → §E.4.5) |
| `MOVE` | Relocate entry | Move an entry from one parent to another within the ToC; issue cross-reference chase instructions |
| `ADD` | New entry | Insert a new volume, part, section, or item into the ToC at a specified position |
| `XREF` | Update cross-reference label | Change only the cross-reference annotation on an existing entry (e.g. update "→ Supp Vol §IV" pointers) |
| `MERGE` | Combine entries | Merge two sibling entries into one; resolve content overlap instructions |
| `SPLIT` | Divide entry | Split one entry into two; specify split point |

A single user statement may generate multiple typed operations. List all before executing.

---

## Step 1 — Parse Directive

Read the user's statement. Extract:

1. **Target(s):** The specific entry or entries being changed (volume/part/section/item code + label as it appears in toc.md)
2. **Operation type(s):** From taxonomy above
3. **Parameters:** New name / new code / new location / removal disposition (delete vs. redirect)
4. **Ambiguity flags:** Anything the user's statement doesn't resolve (e.g. "remove J-01 only or all of Category J?")

If ambiguity exists: ask ONE clarifying question before proceeding. Do not guess.

**Removal disposition rule:** When operation is `REMOVE`, determine:
- `DELETE` — content is struck entirely; no guidebook reference should survive
- `REDIRECT` — content exists elsewhere (e.g. in Supplementary Volume); all guidebook references should be updated to point to the new location
- Ask if not clear from context.

---

## Step 2 — Preview

Output a **Pre-flight Summary** to the user:

```
OPERATION(S): [list typed operations]
TARGET(S): [exact ToC entries affected, with current path]
ACTION: [plain-English description of what will change]
DOWNSTREAM IMPACT: [list of known cross-references, item codes, headings in guidebook that will need updating]
AMBIGUITIES: [list or —]
```

Wait for user confirmation before executing. Skip confirmation only if user included "go" or "fast-track".

---

## Step 3 — Update toc.md on GitHub

1. GET `references/toc.md` + SHA.
2. Apply all confirmed operations to the ToC text.
   - `REMOVE`: Delete the line(s). If `REDIRECT`, add an italicised note on the line: `*(removed — see [new location])*`
   - `RENAME`: Update the heading text in place.
   - `RECODE`: Update code prefix/number in place. Note old code in parentheses: `*(formerly J-01)*` — keep for one version cycle, then drop.
   - `MOVE`: Remove from source position; insert at target position with a `*(moved from [old location])*` note.
   - `ADD`: Insert new line at correct position with `*(new — v{version} {date})*` annotation.
   - `XREF`: Update the cross-reference annotation text on the relevant line.
   - `MERGE` / `SPLIT`: Restructure lines accordingly; annotate.
3. PUT updated `toc.md`. Commit: `toc-editor: {operation summary} [{YYYY-MM-DD HH:MM}]`

---

## Step 4 — Generate Change Order

Create a new file: `references/change-orders/CO-{NNNN}-{YYYY-MM-DD-HHMM}.md`

To get the next sequence number: GET `references/change-orders/` directory. Count files. Next number = count + 1, zero-padded to 4 digits.

**Change Order schema:**

```markdown
# Change Order CO-{NNNN}
**Date:** YYYY-MM-DD HH:MM  
**Raised by:** toc-editor  
**Status:** OPEN  
**Operations:** [comma-separated list of operation codes]  
**ToC version post-change:** [SHA of updated toc.md]

---

## Summary
[One paragraph plain-English description of what this Change Order does.]

---

## Guidebook Instructions

For each operation, one block:

### CO-{NNNN}-{A} — {OPERATION}: {target label}

**Find in guidebook:**
- Heading: `{exact heading text as it appears in source}`
- Section identifier: `{§X.X or Part X or Category X}`
- Also search for these strings: `[list all variant forms, cross-reference text, item codes that reference this]`

**Action:**
[Precise instruction — one of the following patterns:]

REMOVE/DELETE:
> Delete the entire section/item block from `{heading}` to the next heading at the same level.
> Remove all cross-references to this entry. Search for: `[strings]`
> If any cross-reference cannot be cleanly removed, replace with: `[replacement text or —]`

REMOVE/REDIRECT:
> Delete the content block for `{heading}`.
> Replace all cross-references with: `{new cross-reference text}`
> Search strings to find cross-references: `[list]`

RENAME:
> Replace heading: `{old text}` → `{new text}`
> Replace all in-text references: `[old label]` → `[new label]`
> Search strings: `[list]`

RECODE:
> Replace item code: `{old code}` → `{new code}` throughout document.
> Search strings: `[list all variant forms: short form, cross-volume form, in-text references]`
> Note: Add `(formerly {old code})` parenthetical at first use in current version cycle.

MOVE:
> Remove section/item block from its current location.
> Insert at: `[target location — after heading X / before heading Y]`
> Update all cross-references: `[old location string]` → `[new location string]`

ADD:
> Insert the following new block after heading: `{preceding heading}`
> [Content block, if provided — or flag as: CONTENT REQUIRED before execution]

---

## Cross-Reference Chase

List all sections/items in the guidebook that contain references to the changed entry,
requiring a follow-up pass with `cross-reference-resolver`:

| Location | Current reference text | Required update |
|---|---|---|
| [Part/Section] | [current text] | [updated text] |

---

## Downstream Skill Actions Required

| Skill | Task | Priority |
|---|---|---|
| find-and-replace | [specific substitution] | P1 |
| cross-reference-resolver | [scope] | P1/P2 |
| guidebook-auditor | Verify heading hierarchy post-change | P2 |
| volii-validator | Re-validate item codes if recoded | P1 if RECODE |

---

## Sign-off
- [ ] toc.md updated on GitHub
- [ ] Change Order committed to GitHub
- [ ] project-standards.md rule appended (if operation establishes a new standing rule)
- [ ] gap_register.md updated if operation resolves or creates a gap
```

PUT the Change Order to GitHub. Commit: `toc-editor: CO-{NNNN} [{YYYY-MM-DD HH:MM}]`

---

## Step 5 — Update project-standards.md (conditional)

If the operation establishes a **standing rule** (e.g. "Category J is removed from Volume 2 — all bariatric provisions are in Supplementary Volume §IV only"), append the rule to `references/project-standards.md`:

```
RULE: {description}
CONDITION: {when this applies}
ACTION: {what to do}
DATE: YYYY-MM-DD HH:MM
```

GET + SHA → append → PUT. Commit: `toc-editor: append rule [{YYYY-MM-DD HH:MM}]`

---

## Step 6 — Update gap_register.md (conditional)

If the operation resolves an existing gap: mark CLOSED.  
If the operation creates a new structural gap (e.g. content removed but replacement not yet written): append new P1 gap item.

GET `gap_register.md` + SHA → update → PUT. Commit: `workplan-orchestrator: {gap update} [{YYYY-MM-DD HH:MM}]`

---

## Step 7 — Report to User

```
✓ toc.md updated (SHA: {sha})
✓ CO-{NNNN} committed
{✓ / —} project-standards.md rule appended
{✓ / —} gap_register.md updated

NEXT STEPS:
1. Run find-and-replace using CO-{NNNN} instructions (P1 items first)
2. Run cross-reference-resolver on scope: [list]
3. Run guidebook-auditor A after all substitutions complete
```

---

## Token Rules

- Parse all operations from a single user statement in one pass.
- Batch multiple operations into one Change Order if issued together.
- If a REMOVE/REDIRECT operation targets a section with >10 downstream cross-references: flag as HIGH-IMPACT and require explicit user confirmation before generating the Change Order.
- Never modify the guidebook source file directly. toc-editor outputs instructions only; execution is performed by find-and-replace and cross-reference-resolver.

---

## Error Handling

- Target not found in toc.md → report exact search attempted; ask user to confirm the entry identifier.
- GitHub PUT fails → output Change Order as fenced code block with manual paste instructions. Never drop state.
- Ambiguous operation → ask one clarifying question; do not proceed with assumptions.
