# Summary — area G-stategraph (`workplan/pipeline-state-graph/`)

(Written by the coordinator from the adjudicator's report: the harness blocked the subagent from writing this file. The counts are re-derivable from `adjudication-G-stategraph.jsonl`.)

The area is an audit instrument that is not registered as a check.
- **Atoms** quote governance passages word for word.
- **Generated files** (the TSVs, `CONFLICTS.md`, `STATE-GRAPH.md`) are built from the atoms.
- **A conflict is fixed at the source passage** (areas A, B and C), then recorded in the instrument in four places: the atom's `ambiguity` field; `conflicts.yaml` (`status_corrections`, C-004, C-005); new ADD atoms quoting the 2026-11-14 entries; and a rebuild with `build_graph.py`.
- **Generated copies are never edited by hand.**

## 1. Counts
Derive: `python3 -c "import json,collections as c;a=[json.loads(l) for l in open('adjudication-G-stategraph.jsonl')];[print(k,dict(c.Counter(x[k] for x in a))) for k in ('verdict','status','resolution','unify')]"`
At writing: verdict 31 CONFLICT, 30 HELD, 18 NOT-CONFLICT; status 70 data, 7 label, 1 frozen-record, 1 operative; resolution 42 LEAVE, 32 AMEND, 5 OWNER-Q.

## 2. Canonical sentences (records per key)
- **U6 (46):** "if the only values are from code then code determines the ideal/best"; the best is the most accommodating code value, shown with its code source, and "the empty circle makes it clear that it's not academically or clinically derived".
- **U1 (12):** best is the most accommodating identified value; a source that "simply asserts the value" is eligible; tier sets the marker and the weight, never eligibility.
- **U2 (11):** "convergence is not evidence of best practice but most common practice"; no best value is derived from code consensus.
- **U9 (4):** `v_best_practice` and `code_floor_only` keep their names until the owner rules on the held rename.
- **U3 (2):** "we have best, most common, and floor"; the weak band is never "a floor/convergence claim".
- **U5 (2):** "acceptable isn't relevant as that's a value judgment"; show the attributed threshold instead.
- **U8 (2):** the flag and the citation travel with every rendering of the value.

## 3. Owner decisions
- In a cell with research values, is a code value that is more accommodating than every research value the best? (EVI-094, EVI-131, EVI-134.) *Answered by the owner after this report: the most accommodating value stands unless research shows worse results for it.*
- Does a T4–T6-only basis still take ○ when T4 is present? (26 HELD records.) *Answered by the owner after this report: a T4-only cell takes ◐; T5/T6 only, ○.*
- Does the wording "best practice as currently known" stand for a code-only best? The code-only entry does not decide it.

## 4. Rulings that pull apart
- **Code-only ruling against the minimum ruling:** "code determines the best" and "minimum is code stratum" pick different code values whenever the codes differ; calling the output a "floor claim" merges the two.
- **"Simply asserts" against "if the only values":** the definition makes any asserted value eligible; the code-only ruling is worded for cells with no other values (the mixed-cell question, since answered by the harm-evidence test).
- **"Gather and show" against "code determines" and "determination":** recorded in the ledger as unresolved.

## 5. Unflagged
- Depend on the held circle table: `atoms-contracts.jsonl:24` (register invariants, "no above-weak-band best-practice language on regulatory-stratum cells") and `atoms-evi.jsonl:77` (EVI-081, "T4/T5 citations carry ◐").
- Consistent, and settles the floor dispute: EVI-184 (`atoms-evi.jsonl:179`, "most accommodating available value … not largest-number"). 29 first-sweep "floor called best" conflict votes fall on records the adjudicator did not rule CONFLICT; this anchor is the main reason.
- Outside the area: `governance/co1-operational.md:149` ("the converged best-practice value is [value]") conflicts with U2; `scripts/assess/assess_cell.py:1389` and `:1508` ("FLOOR CLAIM") conflict with U3 and U6.

## Largest-consequence passages (from the adjudicator's report)
1. EVI-394 (`governance/evidence-methodology.md:289`, the voice line "[N] jurisdictions' standards converge on [value] — best practice as currently known"): names the most common value best practice.
2. The mixed-cell question (EVI-094, EVI-131, EVI-134).
3. `machines.yaml:277` (M05.t2 guard) and the engine's comments at `scripts/assess/assess_cell.py:1389` and `:1508`: both call a code-only cell's output "a floor claim, never best practice"; the engine in fact picks the most accommodating code value, which is the best under the code-only ruling.
