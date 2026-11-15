# Adjudication summary — area F-workplan

(Written by the coordinator from the adjudicator's report: the harness blocked the subagent from writing this file. The counts are re-derivable from `adjudication-F-workplan.jsonl`.)

Input `findings-F-workplan.json` (88 findings); output `adjudication-F-workplan.jsonl` (88 records, same order).

## 1. Counts
Derive them, do not trust these: `python3 -c "import json,collections as c;r=[json.loads(l) for l in open('adjudication-F-workplan.jsonl')];[print(k,dict(c.Counter(x[k] for x in r))) for k in ('verdict','status','resolution','unify')]"`

At writing: verdict CONFLICT 34, NOT-CONFLICT 48, HELD 6. Status frozen-record 62, data 15, operative 6, quoted-for-rejection 3, label 2. Resolution LEAVE 53, SUPERSEDE 31, AMEND 3, OWNER-Q 1.

Most of this area is frozen: dated plans, attestations and structural test artefacts. Each conflict sits in a dated record whose operative home is a doctrine file in area A (mission commitment 2 and Test 3, tier-system §3, §8 and §8.1, evidence-architecture §6 I3). So the 31 SUPERSEDEs should be **one** ledger entry with one `SUPERSEDES` line per document, and the doctrine homes should be corrected in area A. Copying the fix into each record would break rule 5.

## 2. Canonical sentences (passage counts per key)
- **U1** (26): "The most accommodating value is one that has been identified in our research … enough if the research source itself simply asserts the value." The tier sets the marker and the weight, not eligibility.
- **U2** (14): "convergence is not evidence of best practice but most common practice."
- **U3** (2): "minimum is code stratum unless there is no code data."
- **U4** (1): "remember that value direction of parameter matters."
- **U5** (6): "we are showing data, not determining"; the project "does not claim with own authority that something is the correct way to design."
- **U6** (32): "if the only values are from code then code determines the ideal/best"; "the empty circle makes it clear that it's not academically or clinically derived."
- **U7** (5): held. The working table (● T1, T2, Co-1, Co-2; ◐ T3, T4; ○ T5, T6) is not applied.
- **U9** (2): held. Renaming best-practice names is not decided.

## 3. Owner decisions needed
- `workplan/2026-11-12-bidirectional-pipeline/tasks/T-059-wp-t4-agreement.md:44`: when two claims cannot both hold, does the higher tier's figure become the stated value (OR-6c), or is the most accommodating value shown as best with the other shown beside it?
- The five U7 passages (I3 and its checks: `workplan/2026-08-11-remediation-and-pipeline-anatomy.md` lines 4886, 4888, 5253, 5625, 6522 as the adjudicator cites them): does a T4-only basis stay capped at ○ (the doctrine now) or carry ◐ (the held table)?

## 4. Rulings that pull apart
- **T-059:44.** OR-4 and the 2026-11-14 definition (best = most accommodating, whatever the tier) pull against OR-6c (between ranks, the higher rank states the value). The convergence entry keeps OR-6c standing ("additive").
- **Code stratum = T4–T6 against the held circle table.** Every "T4–T6-only → ○" passage is correct under the doctrine now and wrong for T4 under the held table.
- **"Gather and show" against the specification stage's "determination"** (render contract E1; phase-e step 11): the ledger records this tension and does not resolve it.

## 5. Not flagged by either sweep
- `workplan/2026-10-30-ramp-spec-pages/data/E-03.json:1339`: `"note": "Guidebook working position for this item; provisional"` gives the guidebook a position (U5); inert data, so LEAVE, but it must not be revived as written.
- `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md:276` (P-01-82): "A determination resting on codes alone is best practice at the weak band": agrees with U6, but the ○ cap for T4 depends on the held table (U7).
- `T-059-wp-t4-agreement.md:44`, same line: "the T1 figure is stated and the T2 dispute is noted": the same OR-6c tension as in §3.

## Largest-consequence passages (from the adjudicator's report)
1. `workplan/2026-11-12-bidirectional-pipeline/OWNER-SHEET-PLAIN.md:72` (CONFLICT, AMEND, U6): the live owner sheet for the open decision OD-48 tells the owner that a protection against code-only values ever being shown as best practice is being kept, which contradicts "code determines the ideal/best" and misframes the choice the owner is asked to make.
2. `workplan/2026-10-30-ramp-spec-pages/RENDER-CONTRACT-parameters-3-and-12.md:30` and `:41` (CONFLICT, AMEND, U1 and U5): defines best practice as "practice the evidence best supports" and presents the best value as "the guidebook's own choice"; replacement wording is in the jsonl.
3. `T-059-wp-t4-agreement.md:44` (HELD, OWNER-Q): OR-6c against the 2026-11-14 rulings.
