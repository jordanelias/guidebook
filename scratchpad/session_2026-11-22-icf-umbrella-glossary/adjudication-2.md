# Adjudication 2: the referred-back questions, ruled for the smallest change

Written 2026-11-25 by an Opus-class adjudicator on the owner's words of 2026-11-25 (sixth), quoted below. Ledger reference: `grep -n -F "## Owner statements 2026-11-25 (sixth)" references/project-standards.md`.

> "Opus to adjudicate all of the above and log it"
> "I don't want to answer these right now so just make it happen"
> "Remember that this project is simple!!!"

This file is read-only work. No tracked file, row or ledger line was changed. Every ruling below is a **delegated resolution**, and its CHECK line reads `pending` until a different instance has checked it.

**Method.** Each question is put through the order of CLAUDE.md §8:
1. do nothing, and say why;
2. change a rule or a convention;
3. reuse what exists;
4. delete the cause;
5. only then, the smallest code.

**Result in brief.** No ruling below adds a table, a verb, a check or a migration. Two rulings withdraw work (T-128, and the crossing writes inside T-102). One changes a gate convention. The rest are "do nothing".

**Reach.** The sixth statement names these questions, so on contact it supersedes the limit OD-79 placed on them (rule 0). It does **not** supply an "Owner" heading. `review-identity-need-icf --approval-ref` and the `retirement_ref LIKE 'Owner%'` CHECK (`grep -n "LIKE 'Owner" scripts/migrations/166_identity_need_icf_owner_review.sql`) stay unmet by anything written here. Decision-protocol §2.4 still governs anything these words do not name.

---

## 1. Rulings

**OD-73: may an identity–need pair be recorded before any ICF code? Do nothing; no pairs table.**
- The owner answered "should be all three" (2026-11-20, fifth). The independent check found that a pairs table reverses that answer. This ruling keeps the answer.
- "We should be able to map them to one another" (2026-11-22) is **already met** by the table that exists. A pair is recorded as an `identity_need_icf` row whose ICF code is one of the need's own `access_need_icf` codes.
- The owner ruled that such rows "count as identity's ICF coverage" (2026-11-21, sixth: `grep -n -F "they count as identity" references/project-standards.md`).
- `v_lens_crosswalk` already reads identity ↔ need from these rows.
- "And from there, perhaps, we select ICF codes" means further rows for the same pair carrying a body-function or activity code, when one is grounded (see OD-78). No meaning is read into "perhaps" beyond that.
- Basis: the 2026-11-20 (fifth) answer; the 2026-11-21 (sixth) answer; CLAUDE.md §8 ("reuse what exists").
- **Opens:** nothing. Nothing is to be built.
- **Reversal cost:** none, because nothing is built.

**The 63 rows that repeat a need's own codes. Do nothing; keep them.**
- They are the owner-ruled coverage (2026-11-21, sixth). Under OD-73 above, they are also the record of each pair.
- Rule 5 ("point, do not copy") is the owner's general ruling of 2026-08-24. The 2026-11-21 (sixth) answer is the later and more specific one, on exactly these rows, so it governs (rule 0).
- Retiring them would also need an "Owner" `retirement_ref`, which no delegate can supply.
- Derive the rows with: `select count(*) from identity_need_icf t where retired_at is null and exists (select 1 from access_need_icf a where a.need_code=t.need_code and a.icf_code=t.icf_code)`.
- **Opens:** nothing. **Reversal cost:** none.

**The 29 pairs: accept classes A and B under delegation; reject class C under delegation. No row changes.**
- Derive the pairs with: `select identity_code, need_code, warrant from identity_need_icf where retired_at is null`.
- **Class A** (17 pairs): the need's registry text names the identity's group, or each side names the other. Accepted.
- **Class B** (10 pairs): the need names a condition that the identity's own description lists. Accepted. This includes COM and EPI with A-TRIGGER: the need lists "photosensitive epilepsy, MCAS", EPI lists "photosensitivity", and COM lists "MCAS". That answers GAP-379's open part.
  - Basis: `governance/mission-and-epistemics.md`, doctrinal commitment 1: "Population codes are organizing scaffolding … Co-occurring conditions are the norm".
  - The check's point stands that the umbrella answer alone does not reach class B. The sixth statement's delegation does.
- **Class C** (BRAIN–A-NOSPEECH, COM–A-LOWLOAD): the warrant reads "recorded as an inference". Rejected, on the owner's own ground for rejecting TRIPLE-65: "the pair is an inference no record states".
- **What stays undone.** The rows stay `pending`. Marking A and B `stated`, and retiring C, needs an owner-headed entry, and a delegate's ruling cannot be one.
- **Is leaving it harmless to the plan? Yes.**
  - No gather, determination or gate reads `identity_need_icf` (D-0184: a crosswalk never filters).
  - No task's gate reads the state of these rows. Check with `grep -l "identity_need_icf" workplan/2026-11-12-bidirectional-pipeline/tasks/*.md`: none gates on `stated`.
  - The one effect is on proposals. The ACTION below tells T-127 not to take the two class C rows as proposals.
- **Opens:** nothing. **Reversal cost:** none; a later owner review overrides it.

**Which mapping the owner doubted: `identity_icf_map`. It stays frozen, and nothing more is added to it.**
- The check's corrected timing points here. Its table of identities with their `identity_icf_map` codes was printed at 04:04:06 UTC on 2026-11-22. The owner wrote "I don't think the mapping is correct" at 04:04:08.
- The message spoke of "entire groups like b750 to b789". Of the ICF link tables, only `identity_icf_map` holds range codes.
- The PR 245 rows are not condemned by this ruling. They are all `pending` except the owner's own TRIPLE-64, so they are not treated as correct either way.
- Smallest course: keep OD-77's freeze, and make it permanent as to additions.
  - **T-128, whose whole purpose is to add rows to this map, is withdrawn** (delete the cause).
  - T-102 does not write new crossings into it (see OD-82).
  - The map's existing rows still print as proposals beside T-126's warning. A proposal is not a link (MAPPING-DESIGN).
  - No row is retired, except SCI's rows as part of SCI's own retirement (see below).
- Basis: OD-77 as checked (`grep -F "OD-77 STATUS:" references/project-standards.md | tail -1`); CLAUDE.md §8.
- **Opens:** T-127 and T-059 without T-128 (see OD-89).
- **Reversal cost:** re-author T-128 from its file. No row was ever written by it.

**OD-78, clauses 3 and 4: may a session propose a body-function code on an identity or pair? Do nothing.**
- No proposal path is added, and no task waits on one.
- A body-function code reaches the database the way any ICF code does: on a figure, as a lens link, when the clause names the function (`add-lens-link`, `named_in_text` or `context`).
- On an identity, it arrives only from the owner's words, as TRIPLE-64 did. The 2026-11-21 (third) ACTION (2) and the 2026-11-23 interim stand unchanged, so no owner answer is reversed.
- Basis: CLAUDE.md §8 ("do nothing and say why"). The "why": nothing on the critical path reads an identity-level body-function code (the generator's dependency columns name none).
- **Opens:** nothing. **Reversal cost:** none.

**OI-77 (and OD-82): SCI. Retire SCI into WHEEL, as the owner said.**
- The owner answered OI-13: "SCI is the same population as WHEEL"; ACTION (1): "Hold `SCI` and `WHEEL` as one population under `WHEEL`" (`grep -n -F "OI-13 STATUS: ANSWERED BY THE OWNER" references/project-standards.md`).
- OI-77 was raised by a correction, not by the owner. It asked whether deleting the medical lens changes that answer. The owner deleted the lens and did not restore SCI. The simple reading is that the answer stands.
- The injury and its level are not held. The correction's ACTION (3) already forbids keying a determination on a diagnosis term.
- `retire-identity --to-identity WHEEL` takes as `--approval-ref` the owner's own heading, "Owner clarification 2026-11-12 (eighth set) — LMB becomes UPL (upper limb) and is not part of mobility; only SCI is the same as WHEEL". That heading names SCI and is the owner's ruling, so **no heading is forged**.
- With SCI retired in T-102, T-127's stated reason (a row is tagged once and never swept twice) holds. That cures the check's objection to the earlier OD-82.
- What T-102 does to SCI's rows:
  - its `identity_icf_map` rows are **retired**, not moved (`retire-population-icf-link`), because moving them would extend the frozen map;
  - its lens links and its gap are carried to WHEEL by judgment, as T-102-design §6a says.
- What T-102 skips: the children's crossings, which the owner confirmed on 2026-11-13 (OI-03), are **not written** into the frozen map. They are deferred, not deleted, and T-102-design §7.3 keeps them.
- Basis: OI-13 (owner); the eighth set; T-127 §2; CLAUDE.md §8.
- **Opens:** T-102 as a whole, with the gate convention below.
- **Reversal cost:**
  - SCI is retired in place (`status='deprecated'`). Restoring it is an `amend-identity` back to active, plus re-tagging the few rows carried. Count them per table with `select count(*) from <t> where identity_code='SCI'` over `extraction_lens_links`, `gaps` and `identity_icf_map`.
  - The deferred crossings can be written later from the design file.

**OI-55 item 1: how a carry-only research batch is gated. Change a convention; write no code.**
- A batch that searches nothing and admits nothing is red on R1, R9a and R9b by construction (T-102 §6). Its red on those three rules is expected and is recorded in its pull request body.
- It is gated by its own task tests and the rebuild.
- It does **not** move `sessions/LATEST-RESEARCH`, because it is not a research batch in the contract's sense. The blocking `research_dod_session` therefore keeps reading the last batch that did search, and stays meaningful.
- Basis: CLAUDE.md §8 (change a convention before adding code); CLAUDE.md §5(a) (a gate red by construction teaches its reader to ignore it, the same argument as rule 6).
- **Opens:** T-102, and every other carry-only task with the same gate text: T-114, T-115, T-116 and T-127. Check each with `grep -l "R9a" workplan/2026-11-12-bidirectional-pipeline/tasks/*.md`.
- **Reversal cost:** the convention is withdrawn. Nothing is stored.

**OD-67 (T-128's list): not reached, and now moot.**
- The sixth statement's "all of the above" is the report's five questions. OD-67 was not among them, and its ACTION (4) says not to resolve it under delegation. It is not resolved here.
- T-128 is withdrawn, so its list is never put. If T-128 is ever reinstated, OD-67's confirmation of the list is owed again.

---

## 2. Draft ledger text (not written; the recorder appends it)

```
## Delegated resolutions 2026-11-25 (second) — the referred-back questions ruled for the smallest change: no pairs table, the repeated rows kept, the 29 pairs classed, the doubted mapping frozen and T-128 withdrawn, no body-function proposals, SCI retired into WHEEL, carry-only batches gated by their own tests (OD-73, OD-77, OD-78, OD-82, OD-83 to OD-89)

Written by the coordinating session from `scratchpad/session_2026-11-22-icf-umbrella-glossary/adjudication-2.md`, an Opus-class adjudication made on the owner's words of 2026-11-25 (sixth) ("Opus to adjudicate all of the above and log it"; "I don't want to answer these right now so just make it happen"; "Remember that this project is simple!!!"). **Not an owner statement.** No ruling writes an "Owner" heading or relaxes a guard that binds `stated` or a retirement to one.

OD-73 (a pair before an ICF code) — no pairs table. A pair of an identity and an access need is recorded as an `identity_need_icf` row whose ICF code is one of the need's own `access_need_icf` codes; "should be all three" (2026-11-20, fifth) stands; a later row for the same pair carries a body-function or activity code when one is grounded.
OD-73 STATUS: RESOLVED UNDER DELEGATION
OD-73 CHECK: pending

OD-77 (which mapping) — the mapping doubted on 2026-11-22 is read as `identity_icf_map` (printed at 04:04:06; the message at 04:04:08 speaks of ranges, which only that table holds among the ICF link tables). It stays frozen and nothing is added to it; its rows remain proposals; none is retired except the rows of a retired identity. The pending rows of `identity_need_icf` are not treated as correct either way.
OD-77 STATUS: RESOLVED UNDER DELEGATION
OD-77 CHECK: pending

OD-78 (body-function codes), clauses 3 and 4 — no proposal path. A body-function code reaches a figure as a lens link when its clause names the function; it reaches an identity only from the owner's words. The 2026-11-21 (third) ACTION (2) and the 2026-11-23 interim stand.
OD-78 STATUS: RESOLVED UNDER DELEGATION
OD-78 CHECK: pending

OD-82 (the mobility split) — superseded by OD-83: T-102 runs whole, SCI retired into WHEEL; it writes no new crossing into `identity_icf_map` (the children's crossings of OI-03 are deferred, kept in `T-102-design.md` section 7.3).
OD-82 STATUS: RESOLVED UNDER DELEGATION
OD-82 CHECK: pending

OD-83 (OI-77: SCI) — SCI retires into WHEEL as the owner answered OI-13 ("SCI is the same population as WHEEL"); `retire-identity --approval-ref` cites the owner's own heading "Owner clarification 2026-11-12 (eighth set) — …", which names SCI; SCI's `identity_icf_map` rows are retired, its lens links and gap carried by judgment. The injury level is not held.
OD-83 STATUS: RESOLVED UNDER DELEGATION
OD-83 CHECK: pending

OD-84 (OI-55 item 1: a carry-only batch) — a batch that searches nothing and admits nothing is gated by its task's tests and the rebuild; its red on R1, R9a and R9b is recorded in its pull request body; it does not move `sessions/LATEST-RESEARCH`.
OD-84 STATUS: RESOLVED UNDER DELEGATION
OD-84 CHECK: pending

OD-85 (the 29 pairs) — classes A (17) and B (10, A-TRIGGER with COM and EPI included, closing GAP-379's open part) accepted under delegation; class C (BRAIN with A-NOSPEECH, COM with A-LOWLOAD) rejected under delegation, on the ground of the owner's rejection of TRIPLE-65. No row changes: `stated` and retirement need an owner-headed entry. Class C rows are not read as proposals.
OD-85 STATUS: RESOLVED UNDER DELEGATION
OD-85 CHECK: pending

OD-86 (the rows that repeat a need's own codes) — kept: they are the coverage the owner ruled on 2026-11-21 (sixth) and the record of each pair under OD-73.
OD-86 STATUS: RESOLVED UNDER DELEGATION
OD-86 CHECK: pending

OD-87 (T-128) — withdrawn: its rows would extend the frozen map. T-127, T-059, T-143 and T-110 no longer wait for it; a code T-128 would have minted is minted by `add-icf-code` when a figure needs it. OD-67 is not resolved and becomes moot; if T-128 is reinstated, its confirmation is owed again.
OD-87 STATUS: RESOLVED UNDER DELEGATION
OD-87 CHECK: pending

CONDITION: any session executing or planning T-102, T-114 to T-116, T-127, T-128, T-059, T-143, T-110; any session reading `identity_need_icf` or `identity_icf_map`; GAP-379; OI-55; OI-77.
ACTION: (1) Build no pairs table, no proposal verb and no check for these rulings. (2) Edit the task files and the register to match (T-102: SCI retired, crossings skipped, the carry-only gate; T-127, T-059, T-143, T-110: T-128 removed from their dependencies; T-128: marked withdrawn; §8: entries OD-73 to OD-87; BATCH-1-EXECUTION-NOTES: T-145 merged, T-112 in part). (3) Act on none of these until each CHECK line reads confirmed. (4) The owner may review the pairs, or restore SCI, at any time; a later owner entry governs.
DATE: 2026-11-25 — delegated resolutions on the owner's words of 2026-11-25 (sixth), not an owner statement.
```

---

## 3. What to do now (the short list)

| # | Action | Kind (rule 10) | Smallest form | Waits for PR 246? |
|---|---|---|---|---|
| 1 | A different Opus instance checks this file; the recorder appends §2 | governance text | ledger lines only | no |
| 2 | Edit the plan to match: T-102, T-127, T-059, T-143, T-110, T-128, the §8 register, BATCH-1 notes | governance text (tooling-side) | text edits, no code | no. It may ride in PR 246 to save the owner a review; otherwise its own small PR |
| 3 | **T-102**, the mobility split, whole | research | existing verbs only (`add-identity`, carries, `retire-population-icf-link`, `retire-identity`) | not logically. In practice, land it after PR 246, because both move `data/guidebook.db`. Whichever merges second re-derives from the new base (research batches are serial, OD-27) |
| 4 | **T-120** (doctrine) and **T-137** (units) | tooling | as their files say | no. T-137's migration number is re-derived after PR 246 |
| 5 | **T-148**, import the ICF blocks and held codes | research | `import-icf-tree` on a scratch copy | **yes**: it needs migration 167 and the verb |
| 6 | **T-127** after T-102 | research | context judgment (T-126); the two class C rows are not taken as proposals | no; it waits only for T-102 |

**Exactly what is behind PR 246's merge:** T-148, and any session that needs `base_icf.parent_code`, the import or `icf-glossary`. That is the owner's umbrellas and glossary, and the gather of an umbrella-keyed cell.

**Not behind it:** every ruling here, the plan edits, T-102, T-120, T-137, T-127, and the READY Sonnet tasks.

**The critical chain after these rulings:** T-102 → T-127 → T-059 (with T-143, after T-120 and T-137) → T-068 → T-117 → T-122 → T-037 → T-038, closed by T-110. **No owner answer remains on it.**

---

## 4. What I could not decide, and why

- **The `stated` state of any pair, and the retirement of the class C rows.** The schema binds both to an owner-headed entry. They are left `pending`. That is harmless to the plan (§1 above).
- **OD-67.** It was not named, and its own ACTION forbids delegating it. It is moot while T-128 is withdrawn.
- **OD-81 (the grain of the ICF import).** It was not among the five questions. It stays as checked: blocks and held codes first, the rest proposed with T-148.
- **Whether WHEEL's crossings (OI-03, owner-confirmed) should ever be written.** That depends on the owner's view of `identity_icf_map`, which only the owner can give. They are deferred, not lost.
- **Whether the eighth-set heading passes `_owner_approval`** for `retire-identity` (dated, found once, names SCI). I read the heading, but did not run the verb on a scratch copy. T-102 runs it first in `--dry-run`.
