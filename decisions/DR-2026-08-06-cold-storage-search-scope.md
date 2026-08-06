# DR-2026-08-06 — Cold storage: hide frozen records from agent search, not from code

- Status: **ADOPTED — owner directive 2026-08-06.** The owner asked, in their own words,
  "can we create a directory that won't be scanned by Claude Code or any tools that has all
  the separated materials?", and separately ruled that `audits/` must not hold the active
  content workplan.
- Date: 2026-08-06
- Category: **D-OP** (operational configuration). Not D-DOCT: no doctrine changes. But it is
  epistemically significant — it changes what every future session is able to perceive — so it
  is recorded rather than left as an unexplained dotfile.
- Affects: new root `.ignore`; `CLAUDE.md` §3 and §10; `audits/bpc-rewrite-workplan-2026-05-11.md`
  moved to `workplan/`.
- Supersedes in part: `workplan/2026-08-05-archive-fork-execution.md` — see §5.

---

## 1. The problem this solves

The owner's stated goal is not disk space:

> "I just want a very clean working tree that doesn't get bogged down by Claude Code constantly
> pulling up stale information or getting confused when scanning because too much context."

So the operative metric is: **when a session greps for a fact, how many answers come back and
how many are wrong.** ~630 files across seven directories hold *frozen records* — text that was
true on its date and is preserved unedited on purpose. Every one of them is a candidate wrong
answer to a current question. CLAUDE.md §9 guardrail 1 exists because a stale anchor in an old
document already caused a real error.

## 2. The mechanism, and the distinction that makes it work

A root `.ignore` (ripgrep's non-git ignore file). Measured, not assumed:

| Surface | Honours `.ignore`? |
|---|---|
| ripgrep; Claude Code's **Grep** | **yes** — paths become unsearchable |
| `git`, `grep -r`, `git grep`, `ls`, Claude Code's **Glob** | no |
| **This repo's own Python tooling** (glob/pathlib) | **no** |

That third row is the whole design. `.ignore` separates **visible to code** from **visible to
agent search**. Nothing is deleted, untracked, moved, or hidden from any program.

This dissolves a constraint that had blocked the alternative approach. The 2026-08-05 caller
sweep found `references/search-log/` and `versions/` *unmovable*: `validate_cross_refs.py:115`
globs the search log and is `level: blocking, kinds: [always]`, so removing its subject would
have made it pass vacuously — the exact failure class four gates were repaired for this week —
and `item_audit_pipeline.py:71-73` reads `versions/current/…` behind an `.exists()` guard, so
removal would degrade it *silently*. Both objections are objections to **moving**. Under
`.ignore` both directories keep their subject and their reader, and simply stop answering greps.

Verified after implementation: `validate_cross_refs.py` reports 0 issues, `item_audit_pipeline.py`
runs, `retired_vocabulary_audit.py` still counts 71 occurrences — unchanged.

## 3. Scope, and the rule that set it

**Admission rule: a directory is hidden only if it is already on the global `exempt_paths` list
in `governance/retired-vocabulary.yaml` — i.e. already adjudicated, entry by entry with written
reasons, as an immutable record whose retired vocabulary is licensed rather than a defect — AND
no live workflow discovers content in it by *search*.**

That list is necessary but not sufficient. It also exempts `decisions/`, `references/project-standards.md`
and dated workplans, which are exempt for being **append-only**, not for being **historical**.
Append-only current documents must stay searchable.

Hidden: `_archived/`, `workplan/_superseded/`, `audits/`, `references/audits/`, `sessions/`,
`references/search-log/`, `versions/`. ~630 files, ~12.3 MB.

**Not hidden, deliberately:** `decisions/` (the governance changelog §9 tells sessions to read),
dated `workplan/` files (they *are* the current plan), `attestations/`, and `scripts/migrations/`
— a migration answers "which change dropped this column?" with a **true** hit, so hiding it
would remove a right answer rather than a wrong one.

**One negation:** `!sessions/LATEST`. It is read by path by the blocking `citation_mining_session`
check, and a session debugging that gate must be able to find the pointer it resolves. Add
`!sessions/LATEST-RESEARCH` when the W4 pointer split lands.

`audits/` needed a second negation until the owner ruled the misfiling out of existence: it held
`bpc-rewrite-workplan-2026-05-11.md`, the **active** content workplan, among ten genuine dated
audit reports. Moving it to `workplan/` — where every other workplan lives — removes the
exception instead of encoding it. Its only code reference was a docstring line in
`validate_reasoning.py:4`, not a path anything opens; the live caller sweep updated 11 files and
deliberately left 28 frozen or `SUPERSEDED`-bannered ones as written.

## 4. The objection, and why it does not defeat this

**"Invisible-and-wrong is worse than readable-and-wrong."** A session greps for a path under
`_archived/`, finds nothing, and concludes it does not exist.

Real, and bounded, for three reasons:

1. **It matches the sweep scope the repo already prescribes.** CLAUDE.md §0 rule 5 scopes the
   caller sweep to "all **non-archived** callers". A grep that skips `_archived/` is that rule
   mechanised, not a departure from it.
2. **The prescribed discovery paths are untouched.** §9 says to find current state by *sorting
   `workplan/`, `sessions/`, `audits/` by date* — an `ls`/Glob operation, and neither reads
   `.ignore`.
3. **The failure modes are asymmetric.** Invisible-and-wrong fails loudly and is falsifiable in
   one command (`ls`). Readable-and-wrong fails silently and confidently, and is what this repo
   has actually been bleeding from.

The residual cost is real and is why §10 documentation is load-bearing rather than polish: a
session that cross-checks a Grep result against `git grep` will see a discrepancy with no
visible cause. **An undocumented ignore file is a deception; a documented one is a known tool
property.** Hence the §10 entry, the self-explaining header inside `.ignore`, and this DR.

Second residual cost, minor: the "Measured … N files repo-wide" figures in
`retired-vocabulary.yaml` `note:` fields are no longer reproducible via Grep. They remain
reproducible via `grep -r`, and that register already declares its counts "DATED MEASUREMENTS,
not invariants."

## 5. Effect on the archive fork (⚑1)

The owner ruled ⚑1 as **archive fork** on 2026-08-05, *before* this mechanism was known. It is
blocked anyway: both `create_repository` and `fork_repository` return
`403 Resource not accessible by integration`.

`.ignore` supersedes the fork's **legibility** rationale and exceeds its reach — the fork's own
plan conceded it was "a modest win", covered only the 2 directories the sweep cleared, and
required deletions plus redirect stubs. `.ignore` covers all 7, deletes nothing, and needs no
caller sweep because every caller still resolves.

What the fork would still buy, and `.ignore` cannot: Glob/`ls` surface reduction, `grep -r`
hygiene, and a *destination outside the working tree* for future retirements.

**This DR does not overturn ⚑1** — sessions propose, owners decide (CLAUDE.md §5). It records
that the decision was made on different information and recommends downgrading the fork to
optional. `workplan/2026-08-05-archive-fork-execution.md` is retained: it is a dated record, and
its HELD-directory analysis stays operative for any future *physical* removal.

## 6. Reversal

Delete `.ignore`. One commit, no data implications.
