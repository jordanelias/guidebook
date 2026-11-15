# Resweep brief (second sweep, current rulings)

You are one of eight readers. Your part is `rpart-N.hits` in this folder (`/home/user/guidebook/scratchpad/session_2026-11-13-edmonton-checklist-pass/sweep/`): one `git grep -n` line per hit (`path:line:text`), for the terms *best practice*, *ideal*, *most accommodating*, *most forgiving* and *acceptable*. Write `rout-N.jsonl` in this folder. Do not open any earlier result file (`out-*`, `check-*`, `CONFLICTS.md`): you are blind to the first sweep. Do not edit anything else and do not run the project's checks. Use `git grep`, not the Grep tool.

## Task

For every hit, decide whether the passage **conflicts with the owner's current rulings**. Read the whole paragraph, list item or table row and the nearest heading above it (and a file's status or header block if the passage depends on it). A hit classified from its line alone is a defect. Passages quoted in order to be rejected by the file that quotes them are not themselves conflicts: say so.

## The owner's current rulings (typed words, 2026-11-14; they supersede every earlier ratified record they touch)

1. **What best practice is.** "best practice is the best/most forgiving/etc of all values/approaches for a given term." "The most accommodating value is one that has been identified in our research ... it is based in the evidence that we have collected enough if the research source itself simply asserts the value." "The most accommodating, then, is the one that best responds to an ICF/access need/identity within whatever context, and that means it is the ideal from what we have found." **"best practice IS the same as ideal IS the same as most accommodating."** It belongs to a cell (a parameter by a lens) and its context, and is chosen from values our research has identified.
2. **Three or four different quantities.** "we have best, most common, and floor" and "we just have minimum, mode, median, maximum". *Most common* = the mode = where values come together (convergence); convergence "is not evidence of best practice but most common practice." *Floor / minimum* = the least accommodating value the code stratum allows (or, with no code data, the lowest identified value), a factual data point. **Direction matters**: "the minimum in some contexts may be the highest allowable number in absolute terms" (an operating force of at most 38 N: the minimum is the highest number). The figures are ordered by the parameter's accessibility direction, not numerically.
3. **Data, not determining.** "we are showing data, not determining. the minimum is a factual data point. acceptable isn't relevant as that's a value judgment. our ideals are simply data points." "we gather and show." The project "is radically transparent, presents all values/approaches/data for comparative purposes, provides citations ..., does not claim with own authority that something is the correct way to design but instead simply showcases the best/ideal value/approach/datum for the parameter in whatever context it's in."
4. **Code-only cells.** "if the only values are from code then code determines the ideal/best." The marker carries the provenance: "we can say something is best practice but the empty circle makes it clear that it's not academically or clinically derived." (Working view of the circles by tier: ● T1, T2, Co-1, Co-2; ◐ T3, T4; ○ T5, T6 — held, not yet applied: do not flag a passage for using the present mapping.) Grey, thin and unverified sources are kept and carry a ⚠ warning.

## Conflict tests (CONFLICT when a passage does any of these; record the code in `tests`)

- **C1** uses best/ideal/best practice **for the most common, consensus, convergent or agreed figure**, or derives it by counting agreement (jurisdictions, sources, roots).
- **C2** uses best/ideal/best practice **for the floor**, minimum or the baseline the code requires.
- **C3** ranks "ideal" apart from "best practice", **or ranks "acceptable"/"adequate"/"satisfactory" as a tier of value** (the prose register's Ideal → Best Practice → Acceptable → Minimum is the known case).
- **C4** states a best, minimum or convergent value as what a design **must, should or may** do on the project's own authority (a verdict, not a data point). A source's own requirement attributed to that source is not C4.
- **C5** reads the minimum, maximum or best **numerically, ignoring the parameter's direction** (for example "best = the highest number", or a ceiling-only claim treated as irrelevant to the minimum).
- **C6** says a value **cannot be called best practice because it rests on code, or on a lower tier alone** (eligibility by tier), against ruling 4. A rule that the *marker* is weaker for such a value is not C6.
- **C7** asserts best practice is not a data point of a cell and context: one best figure for a parameter for everyone, with no lens or context, where the passage is about what the guidebook shows.

## Not a conflict

Naming the most accommodating identified value best/ideal, with its source or citation, including from code alone and with a marker that shows its derivation; saying best practice is not convergence; keeping floor, most common and best apart; a label or name (a table, view, heading, marker text, file) that does not say what the value is; ordinary English or a source title; a source's own use of the phrase attributed to the source. **A passage about the held marker table, the old gloss of ○ or the old numeric reading is not a conflict for that reason alone.** Mark it TENSION only if it also fails a test above.

## Record (one JSON object per hit, in order, one line each, exactly one record per hit)

```
{"file": "...", "line": N, "text": "<hit text, 160 chars max>",
 "flag": "CONFLICT" | "TENSION" | "none" | "UNCLEAR",
 "tests": ["C1", ...], "reason": "<required unless none; 200 chars max: what the passage says, which test and why>",
 "read": "paragraph" | "section" | "file"}
```

TENSION means the passage can be read both ways, or is consistent but its wording invites a C1–C7 reading. UNCLEAR means you could not decide; say what you tried. `none` needs no reason.

## Method rules

Work in order. For a file with many hits, read it once in full if under about 400 lines, then classify each hit from its own passage. For JSONL, TSV and JSON data files, read the record around the hit. Quote nothing you did not read. When finished, check `wc -l rout-N.jsonl` equals `wc -l rpart-N.hits`, that every line parses (`python3 -c "import json;[json.loads(l) for l in open('rout-N.jsonl')]"`), and that the sequence of (file, line) pairs matches the hits.

## Report (under 150 words)

Part number, the two counts, records per flag (derive with a command), the three most consequential CONFLICT records by path and line, and any passage the tests did not fit.
