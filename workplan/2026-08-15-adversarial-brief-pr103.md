# Adversarial brief — PR #103, the ratified-but-unimplemented sweep

**Authority:** owner directive 2026-08-15 ("call for adversarial pass"). Discharges the P3 gate
condition that Q22's own register row set and that the authoring session did **not** meet.

**Status:** OPEN — awaiting execution by a session that did not author the work.

---

## 0. The one rule that makes this worth doing

**Run this in fresh context.** Do not read the authoring session's reasoning first and then look for
problems in it; that reproduces the author's frame, which is the thing most likely to be wrong. Read
the *diff* and the *live repo*, form your own expectations, and only then compare against what the
author claimed.

The authoring session already ran a self-review (session record §8). It found two medium defects.
**That is evidence the work needed review, not evidence it has now had it** — a self-review cannot
find defects that follow from the author's framing, and it says so. Treat §8 as a list of what one
biased reviewer happened to catch, not as coverage.

**Presume defect.** The brief below is written to be broken.

## 1. Scope

| | |
|---|---|
| PR | `jordanelias/guidebook#103` |
| Commits | `b966836` (doctrine), `20d1c7f` (three ratified items + tripwire), `24bc053` (registers/session/attestation), `b1f03f7` (author's self-review fixes) |
| Base | `main` @ `03fa69a` |
| Claim | four ratified-but-unrendered items executed; three register rows retired as not-owed; a tripwire added; no DB change |

## 2. Named attack surfaces, hardest first

**A1 — the doctrine text is the highest-stakes artifact and got the least scrutiny.**
`governance/evidence-architecture.md` is CANONICAL. Two new sections (§4.5, §5.5) were written **in a
single pass, by the author, with no review**, into a document whose own §10 sets falsification
conditions. The author verified that every *named object* resolves. That is a much weaker test than
the one that matters. Ask instead:
- Does §5.5's cultural-claim protection, **as worded**, actually match what DR-2026-07-13 H2 ratified
  — or has the author's paraphrase widened or narrowed it? Diff the two texts clause by clause. The
  boundary criterion is the load-bearing part: does the wording let a claim gain the exemption by
  assertion?
- Does §4.5 or §5.5 **contradict** anything already in the document, in `tier-system.md`, in
  `evidence-methodology.md`, or in `co1-operational.md`? The author checked internal object names,
  not cross-document consistency.
- §4.5 states "precedent counts documents; evidence counts roots" as doctrine. Is that *new doctrine*
  smuggled in as restatement? If it is new, it needed a DR, not an execution commit.
- The `[BUILD STATE]` and `[ENGINE-LAG]` markers make claims about what is built. Re-derive them.

**A2 — the tripwire already failed once; assume it fails again.**
RV-025/026 shipped with file-level exemptions that hid a live use at `schemas/conflict.py:85`. Fixed
by converting to line-scoped escapes. **Audit every one of the six escapes**: is each escaped line a
genuine licensed *mention*, or is it a *use* that has now been silenced more precisely than before?
Specifically interrogate `architecture/navigation-modes.md:184` ("Mode S trigger and mitigation", a
page-section list) and `page-templates.md:262` — the author called these "naming the column", which
is arguable and self-serving. Also: does the escape mechanism let future authors silence real drift
cheaply? Is `severity: doctrine` the right level, or should this be `broken`?

**A3 — the vocabulary sweep changed meaning, by the author's own admission.**
Two edits in `co1-operational.md` went beyond spelling: "against the Tier 1 range" → "informed by —
not bounded by — the Population-Mode range". The author justified this as the ratified Person Mode
correction. **Test that justification.** Is that correction actually ratified in those words? Did the
same substitution get applied consistently, or only where the author noticed? Check
`skills/voice-style_SKILL.md` and `guidebook-auditor_SKILL.md`, where the same judgment was applied,
and check whether any *behavioural* rule keyed on the old phrasing.

**A4 — three rows were retired as "not owed". Retiring an obligation is the easiest way to look
productive.** Re-derive each independently:
- **Q21** was dissolved on `gaps = 0`. The author checked both `%gap%` tables and read DR-2026-08-06.
  But does B5's adoption gate really dissolve, or does it merely *defer* until gaps repopulate — and
  did anything else depend on it?
- **Q2** was closed via a superseding path. Does `UNRESOLVED` truly carry Q2's intent, or was a
  distinction lost that the author waved at?
- **Q8**: confirm the Koontz anchor is gone from every live surface, not just `specs/`.

**A5 — the framing itself, which the author could not review.**
Four items were closed. The two with the largest consequence for the guidebook's honesty — Q6
(`instrument_status`) and Q5 (H2 columns) — were *not*. The author's own bias note concedes the
selection may have optimised for closures. **Was this the right selection?** If not, say so plainly;
that finding is worth more than any line-level defect below it.

## 3. Author claims to audit — including claims made only in chat

Per P3, the author's conversational claims are in scope, not just the artifacts.

1. "All 6 advisory failures are pre-existing" — baselined via `git stash -u`. **Re-baseline yourself.**
   The `-u` matters; without it the stash leaves untracked files and the comparison is contaminated
   (that exact error happened on 2026-08-15 in a prior session).
2. "`--all` → 46 green / 0 blocking." Re-run.
3. "No DB change; `user_version` 60 throughout." Verify against `main`.
4. "Every schema object named in the new doctrine resolves." Re-run; then ask the better question in
   A1.
5. "The matcher survived 14 boundary probes." The author wrote the probes. **Write different ones.**
6. "33 occurrences." This number was wrong once already (published as 38). Re-measure.
7. "DR-2026-07-22 is superseded, not ratified-by-merge." Check that reading against the merge rule's
   four limits.
8. The `schema-spec.md` currency fill: the author verified the drift evidence *after* acting on it.
   Verify it a third time, and judge whether "NO — historical record" is the right value or whether
   the file should have been retired instead.

## 4. Definition of done

A finding list, each item carrying: the claim attacked, what you did to test it, the verdict, and
severity. **Zero findings is a legitimate outcome** — but a pass that reports zero after a self-review
already found two mediums should say explicitly what it did that the self-review did not, or its
zero means nothing. Record the pass in `sessions/`, attest it, and update this file's status.

Do **not** fix what you find in the same pass unless it is trivial and mechanical — findings first,
so the record shows what was wrong before it shows what was done about it.
