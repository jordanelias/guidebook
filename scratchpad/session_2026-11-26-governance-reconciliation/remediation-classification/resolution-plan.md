# Plan to resolve the remediation plan to the goal (2026-11-27)

Sources: classify-1..4.md, path-to-one-determination.md, antagonist-4.md (all model output, unverified by me except where stated).
Test applied: CLAUDE.md section 8 (what wrong thing reaches the guidebook without it) and the DR-2026-08-19 section 4 criterion (one answered question, published).
Nothing is applied. Every step waits for the owner's approval.

## State
- PR #248 merged to main as 1d52215d. This branch is fast-forwarded to it. T-120 item 2a (marker table) is on main.
- 73 open tasks in the generated list; it is stale (T-145, T-147, T-148 merged; T-128 withdrawn; holds on T-135 and T-084 answered).
- T-112 is NOT done: 11 live non-English figures lack a current reviewed English; the stored originals are truncated (GAP-372, open, no task).
- First published determination: parameter 3 (ramp gradient), probe cell 3 x MOB. Parameter 12 (ramp run length) may be closer; nobody weighed it.

## Owner decisions that change the plan (ask first)
Q1 OD-63 (answered 2026-11-14): render shows minimum, mode, median, maximum, colour-coded by jurisdiction. Relax it for the first page, or not? If not: T-124, T-036, T-108, T-086, T-111, T-113 are on the path.
Q2 Does parameter 3 at MOB pass the umbrella test? Ledger line ~1197 says it fails (members' demands oppose). If it fails: WHEEL route (T-102 stays on the path).
Q3 Does a PROXY grade make a value thin (triangle)? tier-system section 5 lists it as not yet ruled. T-117 implements only what is ruled until answered.
Q4 First cell: parameter 3 (more evidence, more defects) or parameter 12 (one unverified governing source, readable units)?
Q5 Retire or keep T-129, T-130, T-139, T-140, T-141, T-070 (each reverses something the owner asked or ratified)?
Plus the pending C and D items in decision-prompts-C-D.md (C4 order of authority first).

## PR A: plan hygiene (workplan task files and the generated plan; DELEGABLE)
1. Mark T-145, T-147, T-148 done; remove T-128 everywhere; reopen T-112 with GAP-372 as its scope; clear the stale holds on T-135 (OD-69) and T-084 (OD-46).
2. Retire (delete task files; section 8 needs evidence, not permission): T-005, T-038, T-039, T-047, T-085, T-122.
3. Defer (leave file, mark deferred): T-027, T-033, T-040, T-062, T-109, T-118, T-132.
4. Hold for the owner (Q5): T-129, T-130, T-139, T-140, T-141, T-070.
5. Regenerate REMEDIATION-PLAN.md with the generator; commit the regenerated file.
6. Fix the plan's stale texts the classifiers named: T-056 (OD-48 answered), T-106 (OD-47 answered), T-110 dependency list (drop T-128, T-123, T-120; add T-086, T-149, T-150 once they have files), OD-84 text in T-081/T-082/T-102.

## PR B: tooling (rule 10: merged before any data PR)
1. T-117: marker table into band() and the specifications.marker CHECK (accept the triangle), integrity check C10 accepting the triangle; drop its T-068 and T-120 dependencies. Implements only ruled causes (grey, unverified, thin as the owner defined); PROXY waits on Q3.
2. T-059 selection slice plus T-056 item 3a: the tier grades the marker and does not decide eligibility (Unification U1, OD-58); a codes-only determination for a group is not design_scale universal (OD-48 (a)). Drop its T-128 dependency and item 7.
3. amend-search gains a deferred-reason flag (needed for searches 87, 133, 138, 191), or re-run those four.
4. Reduced T-037: one page per determination (value, marker, sources with tiers and translations, population-match grades, the slug's search log); fold in T-036 (the one query). T-124 only if Q1 says keep OD-63.

## Research PRs (data; after PR B merges)
R1 repair what the first cell stands on:
 - GAP-372: retire and re-add the truncated originals (claim_text is not amendable), then translate; rows 30, 102, 105, 112, 115, 141, 202, 207-209, 215.
 - GAP-376 / REF-01015: supersede the transcription (REF-01026 for REF-01032); correct REF-01015 (the 2010 edition recorded as 2022; the real 2022 edition is REF-01018).
 - T-104 rescoped: verify four governing sources; REF-01026 is superseded, not verified; REF-00997 (403 twice, Wayback failed) and REF-01014 (draft proposal) need a decision.
 - T-105 slice: the 27 verified-without-full-reading rows, all on parameter 3.
 - T-081: class the eight zero-result searches that ran (and the four never-run ones after PR B item 3).
 - T-113 for all sub-national instruments (add REF-00997 South Australia and REF-00996 Flemish handbook to the four listed).
R2 D1 (answered by the owner 2026-11-26): retire the three pending A-SIZE e120 rows (53, 57, 61) through db.py review-identity-need-icf, citing the ledger entry. Small separate data PR.
R3 groups: T-102 (mint WHEEL, carry SCI links), then the T-127 slice (judge the 63 parameter-3 code figures' lenses), population-match grades for ungraded sources, gate 1 on REF-01002 (T-133 item 1 is not on the WHEEL route; gate 1 is keyed MOB).
R4 T-110: one cell, then run the engine and publish.
If Q1 keeps OD-63: T-108, T-086, T-111 (unit cleanup: 33 rows, 11 bare ratio, "viisi prosenttia") go into R1.

## What is deliberately not done
Everything else classed NEEDED-LATER (about 35 tasks) stays in the plan, unscheduled. Apparatus Definition of Done lines (D-01, D-02, D-03, D-04, D-13, D-18, D-21) are not pursued; delete or reword them in the workplan if the owner agrees.
Honest size of the core: about 14 to 16 tasks or slices (antagonist-4), not the six the path-finder named and not the 73.

## Defects no task covers (add one line each to the plan or file gaps)
GAP-372, GAP-376 / REF-01015, code_currency_status NULL on all 59 sources, REF-00997 and REF-00996 sub-national filing, the A-SIZE e120 retirement (R2), `%` inside claimed_value on governing rows (unverified whether T-108 covers values).

## Doctrine limits
Do not decide PROXY = thin (Q3); do not reverse OD-63 (Q1); T-116 step 2 (retire the six LMB crossings) is a taxonomy decision and the owner's; the owner keeps T-129, T-130, T-139, T-140, T-141 and T-070 until Q5.
