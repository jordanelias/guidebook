# Adjudication summary: C-tools

(Written by the coordinator from the adjudicator's report: the harness blocked the subagent from writing this file. The counts are re-derivable from `adjudication-C-tools.jsonl`.)

## 1. Counts
Derive with `python3 -I -c "import json,collections;L=[json.loads(l) for l in open('adjudication-C-tools.jsonl')];[print(k,dict(collections.Counter(d[k] for d in L))) for k in ('verdict','status','resolution','unify')]"`; do not trust the figures typed here.
- verdict: CONFLICT 16, NOT-CONFLICT 6, HELD 1 (23 findings)
- status: operative 15, data 4, label 2, frozen-record 2
- resolution: AMEND 7, TOOL 6, LEAVE 6, SUPERSEDE 4

## 2. Canonical sentences
- **U6 (9 passages):** "if the only values are from code then code determines the ideal/best": the engine's most accommodating code value is the best, shown with its code source, and "the empty circle makes it clear that it's not academically or clinically derived". The tier sets the marker. It does not decide eligibility.
- **U5 (4):** "we are showing data, not determining … acceptable isn't relevant as that's a value judgment".
- **U2 (3):** "convergence is not evidence of best practice but most common practice": codes agreeing give the mode, never the best.
- **U1 (2):** best is the value "that best responds to an ICF/access need/identity within whatever context", chosen from the values the research identified; never the middle of an envelope.
- **U4 (2):** values are read in the parameter's accessibility direction: "the minimum in some contexts may be the highest allowable number".
- **U9 (2):** names stay as they are; any rename is held.
- **U7 (1):** "if it mixes then it's a new value proposed … conjecture", so the value takes the warning triangle; that marker edit is held.

## 3. Needing an owner decision
- Whether the proxy branch's value (a code threshold with a direction taken from findings) is a project inference that takes the triangle (`scripts/assess/assess_cell.py:1469`).
- Where the mode and the median sit in the prose register's item sequence once the Acceptable rung is gone (`skills/prose-style-checker_SKILL.md:53`); render (T-037) may own this instead.
- Whether the register's canonical "to be + [value]" voice survives "showing data, not determining": it is the owner's own register, so this is doctrine.

## 4. Rulings pulling apart
- D-0005 (`057_baseline_2026-08-12.sql:1596`): the rule that code consensus is never best practice agrees with the clause "not by code consensus"; the code-only ruling contradicts the clause "solely from code … in error" when codes are the only values. Supersede only the second clause.
- `code_floor_only` and the engine's "floor claim" (`assess_cell.py:1505-1509`, migration 117): the code-only ruling makes the value the best; the minimum-scope answer puts the floor at the code stratum's least accommodating value; the engine's text names the best value a floor.
- "Weak band" for a T4/T5-led code-only cell: the present `band()` and CHECK 116 give ○; the held circle table would give T4 ◐.

## 5. Unflagged conflicts seen
- `scripts/assess/assess_cell.py:1389` calls the regulatory branch a "Universal-Mode FLOOR CLAIM" (U3).
- `skills/prose-style-checker_SKILL.md:27` makes "to be + [value/condition]" the canonical voice, and lines 31–37 turn "We recommend…" into prescriptions: project-authority verdicts (U5).
- `skills/voice-style_SKILL.md:209, 210, 212, 218, 237, 239, 251, 256, 328` contain "this guidebook recommends", "treats X as mandatory" and "The mandate is the guidebook's", against "does not claim with own authority".
- `skills/voice-style_SKILL.md:236` gives a mid-range "Population-Mode default: 33 mm" (U1).
- D-0042 (`057_baseline_2026-08-12.sql:1633`): "OT assessment determines position" is a verdict.
- Rule 10 gap: `scripts/db.py` has no writer for `decisions.status`; the four live ACTIVE decision rows (D-0004, D-0005, D-0042, D-0076) can only be superseded in the ledger until a gap is filed and the writer is built.
