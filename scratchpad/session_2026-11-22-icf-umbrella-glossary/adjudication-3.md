# Adjudication 3: the ICF import's grain (OD-81), and triage of the T-148 adversarial findings

Written 2026-11-26 by an Opus-class adjudicator. Authority: the owner's words of 2026-11-25 (sixth), "Opus to adjudicate all of the above", "make it happen" and "this project is simple". This is a delegated resolution: every CHECK line stays `pending` until a different instance has checked it. Read-only: no tracked file, row or ledger line was changed.

## 1. Rulings

**OD-88. Import every 3-digit ICF category, in two steps, with one small importer change.**

The owner's own words, typed on 2026-11-22, are all this ruling needs:
- "some kind of glossary that shows all the codes bundled under those classification umbrellas";
- "I had been expecting ICF codes like b210, b230, b265, b280".

After T-148 the glossary cannot meet either. b265 is not held, and Movement functions shows 2 of WHO's 8 categories (finding F4). Re-derive both: `python3 scripts/db.py icf-glossary --umbrella "b750–b789"` and `select count(*) from base_icf where icf_code='b265'`.

The rows are WHO's vocabulary. The verb derives them from the persisted payload, with no judgment, so decision-protocol §2.4 is not reached. This ruling supersedes the clause of OD-81 that said "proposed to the owner with T-148, not run before it": the owner has said they will not answer, and the words above state the grain.

**Smallest course:**
- **Tooling (T-149, its own PR; CLAUDE.md rule 10).** Add one switch to `import-icf-tree`, `--all-categories`.
  - In the loop, a 3-digit category the project does not hold is minted instead of skipped.
  - The insert's hard-coded `"is_range": 1` becomes `1 if n["block"] else 0`.
  - Add one test case: b265 is minted, titled from the payload, and sits under its block.
- **Research (T-150, its own PR, after T-149 merges).** Run the import with the switch on a scratch copy and emit the data migration.
- It does **not** go into T-148's PR. That would put tooling and rows in one PR (rule 10).

**Reversal cost:** a compensating data migration deletes the minted rows that nothing references.

**OD-89. T-148 is a carry-only batch.**

T-148 searches nothing and admits nothing. Its red on R1, R9a and R9b is the case OD-84 (adjudication-2) names. Two cases:
- **If OD-84's check is confirmed before T-148's PR is opened:** add T-148 (and T-150) to OD-84's list, record the three reds in the PR body, and do not move `sessions/LATEST-RESEARCH`.
- **If it is not:** record the same in the PR body, and the owner merges knowing it.

No new task file is needed. Record T-148 as executed in `BATCH-1-EXECUTION-NOTES.md`, which is what the generator reads.

## 2. Triage of the findings

| Finding | Where it is fixed | Smallest form |
|---|---|---|
| F1: DoD red on R1, R9a and R9b; no task file | T-148 PR (prose) | OD-89 above; the PR body; a line in the BATCH-1 notes. No task file. |
| F3: GAP-ICF-TITLES still OPEN, with false figures | T-148 PR (data) | `close-gap` through the existing verb (T-144). The resolution states that the one untitled row, `d910–d920`, is not a WHO code and has no WHO title. Derive the figures with `select count(*), sum(title is null) from base_icf`. |
| F8: dead path; "casing"; `access_need_icf.note` | T-148 PR (data) | The T-148 migration is committed, so it is not edited (rule 3). The header of the gap-closure data migration corrects it: the path is `skills/functional-deficit-researcher_SKILL.md`, no casing changed, and the column is `notes`. |
| F9: spans are derived as the minimum and maximum keys | nowhere; do nothing | OD-74 already records this (the tabulation holds no range string). State it in the PR body. |
| F4: partial umbrellas; unlisted level-2 blocks | **removed by OD-88**; no code | Once every 3-digit category is held, every block has children. The glossary then lists every block, and the umbrellas are complete at the owner's grain. A "partial" marker would be apparatus whose cause is deleted. |
| F2: parenting at mint works only from the repo root; the Refusal is swallowed | T-149 (tooling) | Resolve the `title_source` payload path against the repository root, not the working directory. Do not swallow the Refusal. Print the parent in `add-icf-code`'s result. |
| F5: `--title-payload` verifies a title by substring | T-149 (tooling) | For an ICF code the payload names, take the title from that code's own row in the tree, and refuse a typed title that differs. This deletes the substring path for ICF codes. |
| F6: a minted code arrives untitled | T-149 (tooling) | The same change as F5: the code takes its title at mint. |
| F10: `add-population-icf-link` does not normalise a hyphen span | nowhere; do nothing | That verb writes into `identity_icf_map`, which is frozen (OD-77). No session is to use it, so no defect reaches the guidebook. |
| Docstrings saying "ICF titles 43 of 72" | T-149 (tooling) | Replace each figure with its command (rule 7a). |

## 3. Order

1. **T-148 PR (research):** the import, plus F1, F3, F8 and F9 in data and prose. It waits for PR 246, whose tooling it uses.
2. **T-149 (tooling):** F2, F5, F6, the docstrings and OD-88's switch. It waits for PR 246 to merge, because it edits the same verb.
3. **T-150 (research):** the import with `--all-categories`, after T-149 merges.
4. **T-127 (research):** after T-102. **T-149 must precede T-127**, because T-127 may mint ICF codes (F2, F5, F6). T-150 should also precede it, so that a minted 4-digit code finds its 3-digit parent. This is preferred, not required.
   - T-102 mints no ICF code, so neither T-149 nor T-150 blocks it.

## 4. Draft ledger lines (not written)

```
OD-88 (the grain of the ICF import) — every 3-digit ICF category is imported from the persisted WHO payload, on the owner's words "a glossary that shows all the codes bundled under those classification umbrellas" and "I had been expecting ICF codes like b210, b230, b265, b280" (2026-11-22); one switch on `import-icf-tree` (T-149, tooling), then one data batch (T-150, research). Supersedes OD-81's clause that the rest be proposed to the owner first.
OD-88 STATUS: RESOLVED UNDER DELEGATION
OD-88 CHECK: pending

OD-89 (T-148 and T-150 as carry-only batches) — each searches nothing and admits nothing; it is gated as OD-84 says once OD-84's check is confirmed; until then its red on R1, R9a and R9b is recorded in its pull request body; neither moves `sessions/LATEST-RESEARCH`.
OD-89 STATUS: RESOLVED UNDER DELEGATION
OD-89 CHECK: pending

CONDITION: any session running `import-icf-tree`, minting an ICF code, closing GAP-ICF-TITLES, or executing T-127, T-148, T-149 or T-150.
ACTION: (1) T-148's pull request carries data and prose only (the gap closed through `close-gap`; F8 corrected in the next migration's header). (2) T-149 is one tooling pull request: F2, F5, F6, the docstring figures, and OD-88's switch. (3) T-150 runs the switch after T-149 merges. (4) T-149 precedes T-127. (5) Do not use `add-population-icf-link` while OD-77 freezes `identity_icf_map`.
DATE: 2026-11-26 — delegated resolutions, not an owner statement.
```

**Correction to adjudication-2.md.** Its mapping ruling says "Opens: T-127 and T-059 without T-128 (see OD-89)". That should read **OD-87**.
