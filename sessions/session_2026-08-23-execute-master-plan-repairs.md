# Session 2026-08-23 — Executing the master plan's repair track, adversarially

**Kind:** execution (fixes, record corrections, one archival move). **No research batch; no
determination.** `specifications` is 0 at open and 0 at close, and every route to changing that runs
through the owner-gated population-taxonomy pass (D-0165).

**Method.** Each act ran agonist → antagonist → falsification, per DR-2026-08-19 §7. The antagonist
was not decoration: **it overturned two acts before they were committed and corrected a third
mid-flight.** Those three reversals are the substance of this session and are recorded first, because
a session that reports only what it built is reporting half of what happened.

---

## 1. What the antagonist overturned

### 1.1 A1 — the naive R9 widening would have broken the next batch
**Agonist:** OD-5 says R9 is blind to `source_locators`; widen it to fail when an admitted DOI is
already in the stash.
**Antagonist:** `source_locators` is a **lead index**. A lead becoming an admission is the pipeline
*working*. Checked the data before writing the check: **all four DOIs then held in both tables carry
the SAME `ref_id` in each.** A check failing on mere overlap would have failed all four correct
promotions — and would have failed act B2's planned promotion of REF-00327/576/577/579, the very work
the fix exists to enable.
**Resolution:** the defect is *one source wearing two identities*, not overlap. Implemented as
`R9a` (DOI held under a different ref_id) and `R9b` (ref_id held against a different DOI — real,
because there is no `next_ref_id` allocator). Selftest **15/15 → 17/17**; corpus stays COMPLIANT;
subject sets measured at 4 rows each against **441 stash DOIs now visible where 10 were before**.

### 1.2 A5 — I was reversing four plans on a fact the project had already ruled on
**Agonist (as the plan had it):** strike `GB`→`UK`, because `GB` is the ISO 3166-1 code and `UK` is
not.
**Antagonist:** true, and irrelevant. `governance/jurisdiction-philosophy.md` §3.3:
*"The project uses `UK` instead of `GB` (ISO 3166-1 alpha-2) per project convention… enforced by the
validator."* Graded **ERROR**. **The project knew ISO said `GB` and overrode it deliberately.**
**Resolution:** nothing was struck. The four plans were right; the item is **blocked, not wrong** —
`jurisdictional_values` is under the REFERENCE-ONLY quarantine, and a write to it on 2026-08-21 was
caught by blocking L02 and retracted.
**And the finding that explains the whole thing:** `scripts/validate_jurisdiction.py` **never opens
the database.** It parses YAML only, so an ERROR-level rule is enforced against a surface with no
`GB` rows while all 20 real violations sit unreachable in `jurisdictional_values`. That is why the
item survived four schedulings. `2026-08-18-research-frame-proposal.md:606` suspected exactly this
and never checked. **Same defect shape as OD-5, which A1 fixed an hour earlier.**
Deliberately **not** wired: it would go red on 20 rows the quarantine forbids fixing, producing a
permanently-red gate — which trains people to ignore it.

### 1.3 A2 — the plan told me to delete a true description
The instruction was to drop "doctrine recheck" from the governance battery description as abolished
by OD-10. **I made the edit, then the antagonist pass caught it.** OD-10 abolished the
`[DOCTRINE: <sha>]` commit token, its CI step and its enforcing script — **not**
`scripts/doctrine_recheck.py`, which is alive and registered in that same battery
(`--cross-ref`, passes 2.2–2.3). Restored, and each of the three clauses is now asserted to map to a
registered check id.

---

## 2. What was executed

| Act | Result |
|---|---|
| **A1** — OD-5 | `R9a`/`R9b` added. Selftest 17/17, both new rules fire, seeds cannot cross-fire (one joins on DOI, the other on ref_id). Non-vacuity measured, not assumed. |
| **A2** — R-12 | Open **12 days** (filed 08-11, refiled 08-18). Unquoted YAML with commas parsed to two phantom keys in the file that inventories every gate. Fixed; asserted **every** battery now parses to exactly `{deps, description}`. |
| **A3** — battery line | `db_integrity` claimed "35 checks. Red on main" while the check-level note in the same file said 72/72. Replaced with no count and no status claim (CLAUDE.md §2(b)). |
| **A4** — archival | 13 files / 4,065 lines to `_archived/`. Live workplan **72 → 59**. Prose callers read directly in `skills/`, `governance/`, `.claude/` because the referent scan is blind to them — the blindness that made cull Phase 4a unsafe. |
| **A5** — `GB`→`UK` | **REFUTED.** See §1.2. Nothing struck. |
| **A6** — DR reconciliation | §8 caveats moved *to* the citations; §3 step 6 now owns all four multiply-specified items, named once each; §B extended to be the single index; forward note appended to DR-2026-08-06. |
| **A7** — scorecard | The 08-22 plan scored **1 of 5** in its own file. Not archived — acts 5–6 are blocked, not finished. |

---

## 3. My own errors

| Error | Caught by | Cost |
|---|---|---|
| Wrote the naive R9 widening as the plan specified | Checking the data before committing | None — caught pre-commit |
| Deleted "doctrine recheck" from a live check's description | Antagonist pass, post-edit | One restore |
| Wrote A5's reversal into the plan on ISO reasoning | Reading `jurisdiction-philosophy.md` §3.3 | The plan carried a wrong instruction for a day |
| Set A1's falsification as *"R9's EXAMINED must rise"* | Reading the code | The clause was **unsatisfiable** — `EXAMINED:` is emitted only by `check_baseline()` and counts rule codes, not subjects. Corrected in the plan. |

**The pattern in all four: the plan was wrong, and it was wrong because I wrote it from a reading
rather than from the primary source.** A1's falsification, A2's instruction and A5's entire rationale
were all authored in this repository within the last two days by me, and all three failed on first
contact with the code and the doctrine they claimed to describe.

---

## 4. Where this leaves the deliverable

**Unmoved, and that must not be softened.** `specifications` 0 → 0; `evidence_sources` 10 → 10;
all five gaps still `OPEN`. This session repaired the machinery around the blocker and did not touch
the blocker, because the blocker is owner-gated.

**On D-0165 specifically** — a read-only search of the past month (sessions, decisions, DRs, the
`decisions` table, the ripgrep-blind paths) found **no session and no decision that rules on it**;
`supersedes` is `[]` on every row from D-0151 to D-0166 and D-0166 is the last. But the pass is **not
starting from nothing**: `DR-2026-07-23-population-schema-replace` (ADOPTED) fixes the 23-code flat
set and ratifies the umbrella exception, and `references/project-standards.md` lines 563–566 carry
the three-part permitted-umbrella test. Those are the precedent the pass extends. **D-1, which
quarantines the axis-map route and is what made A-18 undeterminable, is recorded only in a workplan
and was never lifted into a ratified DR** — the weakest surface in the repo carrying a load-bearing
directive.

### 4.1 A defect this session caused and then found in its own record

**Every Bash call of this session was filed under the *previous* session's scratchpad**
(`scratchpad/session_2026-08-22-research-batch-02-.../commands.jsonl`). The provenance hook resolved
the session stem from `.claude/session`, a second pointer to a fact that `sessions/LATEST` already
holds. `LATEST` is updated by the close-out ritual and has **six code readers**; `.claude/session`
had **one** — the hook — and nothing maintained it, so it went stale the moment a session closed.

Fixed by removing the divergent copy rather than syncing it: the hook now reads `sessions/LATEST`
and strips the `.md` suffix, and `.claude/session` is deleted. **This is the same defect as the
identifier registry, the four DOI columns and the two item→population routes — one fact with two
homes — found for the fourth time in one session, in this session's own provenance record.**

**This session's command log therefore lives under the 08-22 directory and is left there.** Moving it
would rewrite a record to look like something that did not happen; the record says where it is.

**And a second half of an older fix, found the same way.** The 2026-08-21 commit `e387888` named a
livelock — the hook records the command that commits the record, so the tree is never clean — and
closed it for `git commit`/`git push` only. **`git status` was left in**, so the command whose whole
purpose is to check the tree is clean was dirtying it. Observed across three turns today: commit,
check, dirty, commit. The skip class now covers read-only queries of git's own state
(`status`, `diff`, `log`, `rev-parse`, `rev-list`, `ls-files`, `show`, `branch`, `stash list`);
mutating commands are still recorded. **Recording a query OF git INTO a git-tracked file was the
purest instance of the recursion this repository exists to resist**, and it sat inside the hook
written to document that resistance.

**Next:** Phase 2 (research batch 03) is unblocked and untouched — forward mining has never been run
on any of the seven mined anchors, and B4's content gaps close only by reading the five sources.
