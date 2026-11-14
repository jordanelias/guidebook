# Adjudication summary: B-decisions

(Written by the coordinator from the adjudicator's report: the harness blocked the subagent from writing this file. The counts are re-derivable from `adjudication-B-decisions.jsonl`.)

All 51 findings are in `decisions/`, so every passage is a record. Where a record conflicts with a ruling, the remedy is a ledger SUPERSEDES line, never an edit (rule 0). `DR-2026-07-21-evidence-architecture-option-a-execution.md` calls itself OPERATIVE, but it is still a dated record, and its live text is in `governance/`.

## 1. Counts
Re-derive: `python3 -c "import json,collections as C;L=[json.loads(x) for x in open('adjudication-B-decisions.jsonl')];[print(k,dict(C.Counter(r[k] for r in L))) for k in ('verdict','status','resolution','unify')]"`.
At writing: verdict CONFLICT 13, NOT-CONFLICT 33, HELD 5. Status frozen-record 38, label 6, quoted-for-rejection 4, other 3. Resolution SUPERSEDE 13, LEAVE 37, OWNER-Q 1.

## 2. Canonical sentences (passages per key, from the `unify` count)
- **U1 (7):** the best value is the most accommodating of the values our research identified for the cell and its context; a source that merely asserts a value makes it eligible, and the tier sets only the marker and the weight.
- **U2 (8):** "convergence is not evidence of best practice but most common practice"; the roots count is shown beside a convergence and never chooses the best.
- **U3 (5):** "we have best, most common, and floor"; the minimum is the least accommodating value in the code stratum, and code floors that differ are the inputs from which the code-only best is selected.
- **U5 (1):** "we are showing data, not determining".
- **U6 (25):** "if the only values are from code then code determines the ideal/best"; that best is the most accommodating code value, shown with its code source.
- **U7 (4):** the marker carries provenance; which circle a T4-only cell carries waits on the held circle table.
- **U9 (1):** `v_best_practice` keeps its name until the held rename is decided.

## 3. Needs the owner
- `DR-2026-07-21-product-posture-thinking-tool-not-authority.md:45`: does the 2026-07-21 "the machinery must adjudicate … to surface the best" still stand under "we gather and show", if adjudicating means ordering by direction and marking by tier, not giving a verdict on the design?
- The four HELD marker passages (`DR-2026-07-20…:43`; `DR-2026-07-21…:15, 24, 75`) wait on whether a T4-only cell carries ○ or ◐.

## 4. Rulings in tension
- The 2026-07-21 "no, it's just weak" (doctrine #2: a best-practice claim from code consensus is valid at ○) against the 2026-11-14 "convergence is not evidence of best practice" plus the code-only ruling: both allow a code-only best, and disagree on where it comes from (consensus against most accommodating). Bears on `DR-2026-07-21-evidence-architecture-option-a-execution.md:130, 132`.
- The 2026-07-21 "the adjudication is the product" against "we gather and show" (`DR-2026-07-21-product-posture…:45`).

## 5. Not flagged by the sweeps, and contradicted by the rulings
- `decisions/DR-2026-05-26-gap-driven-mining-protocol.md:126` repeats "Grounds best practice in evidence hierarchy? Yes"; it needs the same treatment as `DR-2026-05-24…:85`.
- `.claude/skills/supersession-audit/SKILL.md:19` names DR-2026-05-24 as authoritative, so that DR's supersession reaches a live skill.
- Live copies that belong to other areas: `governance/mission-and-epistemics.md:42, 46, 177` (best practice "graded by the evidence hierarchy" and "derived solely from code consensus" at ○) and `governance/evidence-architecture.md:122` ("most-accommodating floor selection": the result should be named the best, with the minimum kept as the least accommodating value): both need AMEND under U2 and U3.
- `DR-2026-07-12-evidence-cell-state…:11` calls `evidence_cell_state` "the project's central per-cell best-practice determination", which meets the recorded tension over the word "determination".

Checks run by the adjudicator: 51 lines, the same as the input; every line parses; each (file, line) appears once, in input order; every record has `unify`.
