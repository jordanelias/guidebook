# Area D-bpc: adjudication summary

(Written by the coordinator from the adjudicator's report: the harness blocked the subagent from writing this file. The counts are re-derivable from `adjudication-D-bpc.jsonl`.)

Re-derive: `python3 -c "import json,collections as c;a=[json.loads(l) for l in open('adjudication-D-bpc.jsonl')];[print(k,dict(c.Counter(x[k] for x in a))) for k in ('verdict','status','resolution','unify')]"`, run in this folder.

## 1. Counts (2026-11-14; re-run rather than trust)
- verdict: CONFLICT 101, NOT-CONFLICT 31, HELD 2
- status: frozen-record 132, operative 1 (`references/bpc/_template.md:33`), label 1 (`_template.md:27`)
- resolution: SUPERSEDE 102, LEAVE 31, AMEND 1

Status basis: the 13 flat partition files carry `FROZEN — historical archive only`. Most per-slug files carry `PRE-REHABILITATION — RETRACTED`. The whole surface is pre-reset reference material that DR-2026-08-06 §2 left as it was and that DR-2026-08-19 §1.4 quarantines ("no value crosses"). Git shows no change under `references/bpc/` since the history root. **The 102 SUPERSEDEs need only one ledger entry**, with a `SUPERSEDES: references/bpc/**` line saying that best practice, ideal, most inclusive, highest-ambition, acceptable and adequate in that corpus are read under the 2026-11-14 entries, and that no wording crosses. The corpus is not edited.

## 2. One sentence for each key (passages governed)
- **U1 (17):** best is "the one that best responds to an ICF/access need/identity within whatever context", chosen from values "identified in our research", and a source that "simply asserts the value" is enough.
- **U2 (23):** "convergence is not evidence of best practice but most common practice."
- **U3 (10):** "minimum is code stratum unless there is no code data", and "the minimum in some contexts may be the highest allowable number".
- **U4 (12):** "we just have minimum, mode, median, maximum", read in the parameter's accessibility direction; the median is never the position.
- **U5 (54):** "we are showing data, not determining … acceptable isn't relevant as that's a value judgment."
- **U6 (5):** "if the only values are from code then code determines the ideal/best", and the marker shows that the value is code-derived.
- **U7 (2):** "thin is when the evidence doesn't directly concern someone but is conjecture", including "we aren't clinicians", so it gets ⚠ (held).
- **U8 (6):** the project "provides citations … does not claim with own authority", so no figure is called "guidebook best practice" without a source.
- **U9 (5):** names stay as they are until the held rename.

## 3. Needs an owner decision
- `references/bpc/cross-population-conflict-resolutions.md:27` and the thermal-comfort file's line 24 (HELD): these are project inferences, which take ⚠ under the rulings; applying ⚠ waits on the held marker table.
- Should `references/bpc/` be added to `.ignore`? The file's header says entries are owner-gated, and the frozen corpus still appears in every search for "best practice".

## 4. Two rulings pulling against each other
- **Code-only best against "do not use one word for another":** at `jurisdiction-matrix…:14` and `ALL-ROOMS:571`, when a cell has a single code value, best, minimum and mode are the same number.
- **"Most accommodating identified" against "incomplete, not wrong" (lens/context):** the lift car 1100×1800 is named best beside 1100×2000 (BS 8300, new build). The adjudicator ruled this a CONFLICT because the guidebook is "only concerned about design itself"; 1400×1600 is a different lens.

## 5. Not flagged by any sweep, and contradicted by the rulings
- `deaf-acoustic-built-environment.md:39` and `DEAF.md:126`: the convergent RT60 0.4 s is written as a prose-register specification ("is to not exceed").
- `NEU.md:36` and `neurological-built-environment.md:32`: a "Highest-ambition actionable specification" in verdict voice.
- Outside the area, but it governs it: `references/project-standards.md:142` "BPC best_practice_synthesis governs as primary evidence basis"; `skills/research-log-manager_SKILL.md:52,133,177` still has sessions read and append to BPC synthesis, for an item-specification-writer that no longer exists.
- Missed by readers: at `DEAF.md:182` and `assistive-listening-systems.md:15`, CEREMA is called "stricter", but its trigger of ≥50 seats is a higher threshold than ≥25.

## How the adjudicator decided
- A "Best-practice synthesis" heading line was judged on the section it heads; recording the heading as a bare LEAVE would have dropped that section's conflicts.
- The template heading (`_template.md:27`) is LEAVE because its content line has its own record.
- Verdict voice in frozen sections ("to be installed", "mandatory", "Highest-ambition actionable specification") counts as a U5 conflict.
- Consensus-table rows that label a value best practice are conflicts where agreement is the warrant or the value is not the most accommodating one identified; a row that only attributes a source's own pair of figures (ideal and minimum) is not.

## Largest-consequence passages
1. `references/bpc/communication-and-alerts/deaf-acoustic-built-environment.md:36` (and `DEAF.md:123`): RT60 ≤0.4 s is called "the consensus best-practice target".
2. `references/bpc/population-general/mobility-built-environment.md:3` (and `MOB.md:10`): "best-practice floor; floor = 1700mm" merges best practice with the floor.
3. `references/bpc/_template.md:33`: the only operative line in the area; it equates best practice with an "actionable specification"; AMEND with replacement wording, or DELETE if BPC files are no longer created.
