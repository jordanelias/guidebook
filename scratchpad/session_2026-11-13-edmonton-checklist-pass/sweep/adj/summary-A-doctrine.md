# A-doctrine: adjudication summary

(Written by the coordinator from the adjudicator's report: the harness blocked the subagent from writing this file. The counts are re-derivable from `adjudication-A-doctrine.jsonl`.)

60 findings, 60 records. Re-run rather than trust the counts: `python3 -c "import json,collections as C;A=[json.loads(l) for l in open('adjudication-A-doctrine.jsonl')];[print(k,C.Counter(a[k] for a in A)) for k in ('verdict','status','resolution','unify')]"`

## 1. Counts (at writing)
- Verdict: CONFLICT 39, HELD 10, NOT-CONFLICT 11.
- Status: operative 48, frozen-record 8, label 2, data 1, other 1.
- Resolution: AMEND 31, LEAVE 21, SUPERSEDE 7, OWNER-Q 1.

## 2. Canonical sentences, by key (passages governed)
- **U1 (14):** the best is the most accommodating value our research identified for a lens and context; any source that states a value makes it eligible; the tier sets its marker and weight, not whether it is eligible.
- **U2 (13):** "convergence is not evidence of best practice but most common practice"; agreement, at any tier and including agreement among codes, gives the mode and is never the basis of best.
- **U3 (2):** the minimum is the least accommodating value in the code stratum, or the least accommodating identified value where there is no code data; it is never the best.
- **U4 (2):** show the minimum, mode, median and maximum, ordered by the parameter's accessibility direction; the best is the maximum in that order; the median is not a default.
- **U5 (5):** "we gather and show"; show each value with its citation; never call it specified, recommended, acceptable or required on the project's own authority.
- **U6 (19):** "if the only values are from code then code determines the ideal/best"; the best is then the most accommodating code value, and its code marker says where it came from (never ●).
- **U7 (2):** the circles by tier are held: T1, T2, Co-1 and Co-2 take ●; T3 and T4 take ◐; T5 and T6 take ○; keep `band()` as it is until the owner rules.
- **U9 (3):** labels and document genres stay as they are; the rename is held.

## 3. Needs an owner decision
- When a Tier 1 value and a Co-1 value for the same lens and context diverge, is the best the more accommodating of the two, or the one an Opus-class approach names? (`governance/mission-and-epistemics.md:132`)
- Does a cell resting on T4 and T5 sources together take ◐ or ○ once the circle table is applied? Eight HELD passages (`evidence-architecture.md`, `pipeline-contract.yaml`, `tier-system.md:100`) wait on this.
- Does "no anchoring evidence" (the doctrine's trigger) mean the same as the owner's "only values are from code" when a T3 value exists for the cell?

## 4. Rulings that pull against each other
- **OR-6c (tenth set) against the 2026-11-14 definition of best.** OR-6c says the higher tier states the value and the lower tier's dispute is noted; the 2026-11-14 entries say the tier sets the marker, not which value is eligible. Affected: `evidence-methodology.md:96`, `mission-and-epistemics.md:107` and `:132`.
- **"Showing data, not determining" against the specification stage's word "determination" and the doctrine's "best-practice determination".** The ledger records this tension and leaves it unresolved; it touches every evidence-architecture passage that says "determination".

## 5. Not flagged by the sweep, but contradicted by the rulings
- `governance/evidence-methodology.md:409`: "Its recommendations are grounded in the evidence hierarchy" (U5).
- `governance/jurisdiction-philosophy.md:75`: ranks code consensus by how many jurisdictions agree; under the convergence entry, significance comes from the tiers and the independent-roots count (U2).
- `governance/evidence-architecture.md:122`: calls the best of a code-only cell "most-accommodating **floor** selection" (U3).
- `governance/tier-system.md:22` and `:49` use the warning sign as a superseded-banner glyph; U+26A0 is now the warning marker, so in rendered governance the two meanings would collide.
- `governance/adversarial-use-framework.md:29` and `:85` contradict each other inside the same file: one allows a weak-band code-only best; the other says no Tier 6 source can underpin one.
