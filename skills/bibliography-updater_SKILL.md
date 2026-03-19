---
name: bibliography-updater
description: >
  Compile, reconcile, and update the Guidebook bibliography from all active source files.
  ALWAYS use this skill when asked to: update the bibliography, add new references, reconcile
  sources from lit review files or BPC entries, rebuild the reference list, or produce a
  current bibliography draft. Trigger on: "update bibliography", "add references", "reconcile
  sources", "rebuild reference list", "bibliography out of date", "new sources to add",
  "missing references", or after any multilingual-research run that logged new sources.
  Do NOT use citation-verifier for this task — that skill audits existing claims; this skill
  compiles and reconciles the reference list itself.
---

**Model:** Sonnet 4.6
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API
**Output:** updated `bibliography-v8.md` (or named per active version) — written to `/mnt/user-data/outputs/` and committed to GitHub
**All timestamps: `YYYY-MM-DD HH:MM`**

## Intake
- Requires: path to current `bibliography-v8.md` (or equivalent)
- Requires: one or more source files to reconcile against (lit review files, BPC entries, compendium, session outputs)
- Optional: list of specific new sources to add

## Steps

### Step 1 — Load Current Bibliography
Read current bibliography file. Extract all existing entries as a keyed list:
`{author-year-slug} → {full citation, verification status}`

Count: total entries · ✅ verified · ⚠ flagged · ❌ audit-flagged.

### Step 2 — Extract New Sources from Input Files
For each input source file:
1. Identify all citations, references, standards, and named sources.
2. Normalise to `author-year-slug` key.
3. Flag as: NEW (not in current bibliography) · DUPLICATE (already present) · CONFLICT (same key, different citation text).

### Step 3 — Reconcile
- NEW entries → add to bibliography with `[UNVERIFIED — added YYYY-MM-DD HH:MM]` flag
- DUPLICATE entries → confirm match; no action if identical
- CONFLICT entries → flag both; append `[CONFLICT — manual review required]`; do not silently resolve

### Step 4 — Standards and Grey Literature
For any standard cited (ISO, EN, BS, DIN, AS, CSA, ADA, etc.) not already in bibliography:
- Add entry in format: `Issuing Body (Year). *Standard identifier: Title*. Publisher.`
- Flag `[UNVERIFIED — standard currency unconfirmed]` unless jurisdiction-tracker has confirmed CURRENT status in `references/standards-registry.md`

### Step 5 — Format and Sort
Apply APA 7th edition throughout. Sort: alphabetical by first author surname (or issuing body for standards). Group sections:
1. Peer-reviewed research
2. Standards and regulatory documents
3. Guidelines and grey literature
4. Conference proceedings and reports

Preserve existing editorial key (✅ / ⚠ / ❌ / [translated from X] / [Vol 2B: unverified]).

### Step 6 — Output
Produce updated bibliography `.md` file:
- Header: `# Bibliography — [version] · Updated: YYYY-MM-DD HH:MM`
- Counts: total entries · new additions · conflicts · unverified flags
- Full sorted bibliography

Write to `/mnt/user-data/outputs/bibliography-[version]-updated-YYYY-MM-DD.md`.

Commit to GitHub:
- GET current `bibliography-v8.md` + SHA
- PUT updated content
- Commit: `bibliography-updater: reconcile + update [YYYY-MM-DD HH:MM]`

### Step 7 — Change Summary
Output compact table:

| Action | Count | Notes |
|---|---|---|
| New entries added | N | |
| Duplicates confirmed | N | |
| Conflicts flagged | N | Require manual review |
| Unverified flags added | N | |
| Existing ⚠ cleared | N | Only if verified this session |

## Constraints
- Never remove an existing entry without explicit author instruction
- Never silently resolve conflicts
- Never mark a source ✅ verified without tool-based confirmation (PubMed / Consensus / Scholar Gateway / web)
- Standards: defer currency status to `references/standards-registry.md`; do not independently assert CURRENT without jurisdiction-tracker confirmation
- Grey literature: always flag provenance and verification status
