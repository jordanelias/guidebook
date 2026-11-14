# Reader brief — the "best practice" sweep

You are one of seven readers. Each has its own part: `part-N.hits` in this folder (`/home/user/guidebook/scratchpad/session_2026-11-13-edmonton-checklist-pass/sweep/`), one `git grep -n` line per hit (`path:line:text`), and `part-N.files` (the files). You write `out-N.jsonl` in this folder. Do not edit anything else. Do not run the checks.

## Why

The owner's concern: the term "best practice" appears across the tools and doctrines, and readers (including earlier model sessions) keep taking it to mean *the most common figure*. The sweep must pair the grep with a **contextual reading**: a hit is classified by what its passage means, not by the words around it.

## The owner's definition (2026-11-13 and 2026-11-14, typed words)

> "best practice is the best/most forgiving/etc of all values/approaches for a given term"
>
> "The most accommodating value is one that has been identified in our research, which in turn means that it is based in the evidence that we have collected enough if the research source itself simply asserts the value"
>
> (and, the same day) "convergence is not evidence of best practice but most common practice"
>
> (and, later) "The most accommodating, then, is the one that best responds to an ICF/access need/identity within whatever context, and that means it is the ideal from what we have found"

Components: (a) the best-practice value is the most accommodating of the values our research has identified for a parameter; (b) it is chosen from values held as extractions, not computed outside them; (c) a source that merely asserts a value is enough for eligibility (the tier sets the marker and the weight, not eligibility); (d) it is a different quantity from the most common value, which is what convergence describes; (e) it is relative to the lens (an ICF code, an access need, an identity) and to the context (use, indoor or outdoor, new or existing, design scale): it belongs to a cell and its circumstances, not to a parameter across everyone.

## What to read

For every hit, read **the whole paragraph, list item or table row, and the nearest heading above it**, not just the line. If the line sits in a table, read the header row. If a definition is made elsewhere and the passage points to it, open that place. Read a file's top status or header block if the passage depends on it. A hit you classified from the line alone is a defect in your output.

## The record

One JSON object per hit, one per line, in `out-N.jsonl`, in the order of `part-N.hits`. Every hit must have exactly one record: that is checked by count.

```
{"file": "...", "line": N, "text": "<the hit's text, 160 chars max>",
 "sense": "<one primary sense, below>", "also": ["<other senses present in the same passage>"],
 "flag": "none" | "CONFLICT" | "TENSION" | "UNCLEAR",
 "reason": "<required unless flag is none; 200 chars max: what the passage says and what part of the owner's definition it departs from>",
 "read": "paragraph" | "section" | "file"}
```

### Senses (choose the one that the passage's meaning needs; do not choose by the words nearest)

- `ACCOMMODATING`: it means the most accommodating, most forgiving, most inclusive value or approach among those identified (the owner's definition), including "best practice exceeds the code floor where evidence supports a value above it" when it is the value that serves most people.
- `EVIDENCE-GRADED`: it means a claim whose strength is set by the evidence hierarchy (a `stated` cell is "a best-practice claim"; "anchored by Tier 1 / Co-1 / T2 / Co-2"; "graded by the evidence hierarchy"). This is the doctrine's own sense; it is about *how strongly the claim is held*, not *which value*.
- `NOT-COMMON`: it says outright that best practice is not convergence, consensus, code agreement or the most common value ("best practice ≠ convergence", "convergence-not-evidence", "not by code consensus"). Consistent with the owner.
- `COMMON`: it uses best practice **as** the most common, consensus, convergent, agreed, standard-practice or code-derived figure: the reading the owner is worried about. Examples to look for: "standards converge on X, best practice as currently known"; "best practice (what most jurisdictions specify)"; a threshold or count of agreeing sources used to name the best-practice value; a task or check that derives the best-practice value by counting agreement.
- `LABEL`: the phrase only names a thing: a table, view, column, file, directory, section heading, marker text (`[BEST-PRACTICE-PENDING]`), skill name, `best_practice_synthesis`, `v_best_practice`. The passage does not say what the value is.
- `GENERIC`: ordinary English or a quoted source title that uses the phrase for something unrelated to a parameter value (for example "best practices for survey design").
- `PROCESS`: it means a method the project follows ("follow best practice for database migrations").
- `MIXED`: one passage uses the phrase in two or more of the senses above without separating them (give both in `also`; flag it).

### Flags

- `CONFLICT`: the passage defines or applies best practice in a way that departs from the owner's definition: it equates it with the most common/consensus/code figure; it computes it from agreement counts; it requires a synthesised value outside the identified ones; it makes a source's mere assertion insufficient for eligibility *of the value* (a rule about the **marker** is not a conflict; say so in `reason` when you saw that distinction).
- `TENSION`: the passage can be read both ways, or it is consistent with the owner but its wording invites the common-figure reading (for example "best practice as currently known" next to "standards converge").
- `TENSION` also applies where a passage states **one** best-practice figure for a parameter with no lens or context at all (component (e)); say so in `reason`. Do not flag a passage that is already about a cell or a named group.
- `UNCLEAR`: you could not decide from the paragraph, section or file. Say what you tried.
- `none`: consistent with the owner's definition, or a label/generic use.

Do not decide the project's remedy. Do not edit the passage. Do not soften a conflict because the passage is old or in a deprecated folder: record where it lives (the path is in the record) and flag it.

## Method rules

- Work from `part-N.hits` in order. For a file with many hits, read the file once in full if it is under about 400 lines, then classify every hit in it from the passage, not from memory of the first one; a long file can use the term in different senses in different sections.
- JSONL and data files (`*.json`, `*.jsonl`, `*.tsv`): the hit is a field value. Read the record around it (the neighbouring fields, the id) and classify what the record says.
- If a hit's meaning depends on a definition you cannot find, flag `UNCLEAR` rather than guess.
- Quote nothing you did not read. `text` is copied from the hit line.
- When finished, check your own count with `wc -l out-N.jsonl` against `wc -l part-N.hits` (both must match) and that `python3 -c "import json;[json.loads(l) for l in open('out-N.jsonl')]"` passes.

## Report (to the person who briefed you)

Under 200 words: your part number, the two counts, how many records per sense and per flag (derive with a command, do not count by eye), the three most consequential `CONFLICT` records by path and line, and anything in the brief that did not fit the passages you met (a sense the list lacks). Add `[NULL: ...]` if a file had no hits you could read.
