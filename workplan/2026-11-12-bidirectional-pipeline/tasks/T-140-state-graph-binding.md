# T-140  An atom is bound to its section and its quote: found once inside the section passes, found only outside it fails

_One task of a stacked pull request (owner instruction 2026-11-15: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). Read `CLAUDE.md` first; beyond it this file is self-contained. Authority: the ratified adjudication `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md` (section 4 item 8; section 3 items 28, 29 and 87, and the limits paragraph "79 to 91"). It extends T-134 (`ee64bf80`); nothing of T-134 is reverted. Every figure was read on 2026-11-19, read-only, with its command: re-run it._

**Pilot status.** Not piloted. Authored 2026-11-19 by an Opus-class task author on the owner's instruction "Author the tooling tasks in order". Expect a defect in this file; report it.

## 1. Identity

| | |
|---|---|
| Task | T-140 |
| Title | An atom is bound to its section and its quote: found once inside the section passes, found only outside it fails |
| Wave | 2 |
| Layer (CLAUDE.md §3) | 0 |
| Kind | **TOOLING** (CLAUDE.md rule 10); the instrument under `workplan/pipeline-state-graph/` (the checker, its stand-alone verifier, one machine's transitions, the atoms' new `section` key), its test; no schema, no database write |
| Executor | Sonnet-class. The rule is fully stated in section 4; no refusal's meaning and no warrant's shape is decided. Escalate to Opus-class only on a stop of section 9 |
| Traces to | adjudication 3 items 28 and 29 ("bind an atom to its enclosing heading (an entry or a section key) and its quote: found once inside that section passes, moved within it reports MOVED, found only outside it FAILS"; "uniqueness within a section also gives a quote floor with no typed length"), item 87 (no quote floor; `verify_atoms` checks presence only), the limits paragraph (M04's retire transition; `OPEN-QUESTIONS.tsv` and `AMBIGUITIES.tsv` publish the line found); the T-134 section of `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/sweep-list.md` (items 1 to 3 and the repair result) |

## 2. Preconditions

- **Set-up: the stacked-branch convention** (`scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 1, or the brief the coordinator names). Stay on the given branch; no `git switch -c`; no `/session-open`. Diffs, the gate and the code-size line use `$BASE_PRE`.
- **Order.** Eighth of section 4: after T-139 (by order only: no shared file). **T-134 and its repair must be on HEAD:** `git merge-base --is-ancestor ee64bf80 HEAD && echo ok` (printed `ok` on 2026-11-19; `ee64bf80` was not yet on `origin/main`, which is why HEAD is the test).
- **Decisions.** Items 28, 29 and 87 carry no OD number; they are ratified by reference in "Owner ratification 2026-11-19" (its ACTION (3) keeps the breadth of "all" an [ASSUMPTION]). No register OD is rested on, so no gate function applies. Check the entry stands:
```
grep -c -F "## Owner ratification 2026-11-19" references/project-standards.md      # printed 1 on 2026-11-19
```
- **Tests that must be red before you start:** `T140-01`, `T140-02`, `T140-03`, `T140-05`, `T140-06` (section 6).
- **Set-up block.**
```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin; BASE_PRE=$(git rev-parse HEAD); echo "BASE_PRE=$BASE_PRE"
sha256sum data/guidebook.db                                 # must not move: this task has no migration
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-140" && mkdir -p "$SCRATCH"
```

## 3. The problem, in the guidebook's terms

T-134 made the instrument find an atom by its quote: found once anywhere in the cited file passes, and a hit far from the cited line prints `MOVED` and does not fail. Two holes follow (T-134 critic, items 1 and 2). **A unique quote fails the day a later ledger entry re-quotes it** (the ledger is append-only and entries quote earlier entries), so each ledger atom is one re-quote from red with nothing wrong: red by construction, the shape rule 6 warns teaches its reader to ignore the check. **And a passage deleted and its quote re-embedded elsewhere (in a sentence repudiating it, 170 lines later) passes as `MOVED`, exit 0**, so the binding of a ruling to its place is lost. With no binding there is also no quote floor: `''`, `a` and `the` pass wherever they occur once (item 87). `verify_atoms.py` checks presence only, by a second copy of the atom rules, and passes atoms the builder fails.

**Evidence command** (read-only; writes nothing):
```
python3 workplan/pipeline-state-graph/build_graph.py --check > "$SCRATCH/before-check.txt" 2>&1; echo "rc=$?"; grep -E "^EXAMINED: +[0-9]+ +atoms whose quote|^FAIL|failure\(s\)" "$SCRATCH/before-check.txt"; grep -c "^MOVED" "$SCRATCH/before-check.txt"
for f in workplan/pipeline-state-graph/atoms/*.jsonl; do python3 workplan/pipeline-state-graph/verify_atoms.py "$f" | tail -1; done | grep -v " 0 problem"
grep -n -E "^(LINE_TOLERANCE|NEAR_FAIL) " workplan/pipeline-state-graph/build_graph.py
```
**Printed 2026-11-19:** `rc=1`; `EXAMINED:   351  atoms whose quote was read …`; one `FAIL   PIP-01: QUOTE NOT FOUND in governance/pipeline-contract.yaml …` (the quote is genuinely gone; T-120 re-quotes it); `1 failure(s), 0 warning(s), 96 moved`; `96`; four atoms files where `verify_atoms.py` reports problems the builder does not share; the two constants. If any differs, stop (section 9).

**What the new rule will find, measured 2026-11-19 by the author with a scratch implementation of section 4's rule over the 351 quote-checked atoms** (re-derive with your built checker; never quote these): 350 bind to a section; `LED-087` and `LED-205` occur more than once inside their own section (`'research → evidence collection → judgment → synthesis → render'`, `'Screen, then you approve'`): the quote floor's first findings; five atoms found more than once in their file but once in their section, which now pass; two atoms sit in the preamble of a file before its first heading.

## 4. The change

1. **A section, defined once** (`build_graph.py`, one function, `section_of(path, lines)`): the enclosing section of a line is the nearest heading at or above it. A heading is, for a `.md` file, an ATX heading line (`#` to `######` and a space) outside a fenced code block; for a `.yaml` or `.yml` file, a line that opens a top-level key (no indentation, a key, a colon); for any other file, the file has no heading and is one section. The text before the first heading is the file's preamble, a section whose key is the empty string. A section's key is the heading's text with its markers stripped and whitespace collapsed (the YAML key name for YAML). Two headings of one file with the same key make that key ambiguous.
2. **The atom stores its section:** a key `section` on each atom line (the key text; `""` for a preamble). `build_graph.py --bind-sections` writes it, for an atom that has none, from the atom's quote: the one hit in the file, or the one hit within `LINE_TOLERANCE` of the cited line; it never overwrites a `section` already present, never edits a quote, a line or any other key, and prints each atom it could not bind (quote not found, several hits none near the cited line, an ambiguous key) with the reason. Run it once in this task over every atoms file and commit the result; an atom T-120 or a later session adds is bound the same way. The atoms' text stays T-120's (T-134 section 8); a new key is not a re-quote.
3. **The check, in `verify_atoms` of `build_graph.py`, for each atom whose quote is read** (the cited set, unchanged):
   - no `section` key: **FAIL** "no section bound" (run `--bind-sections`);
   - its section key is absent from the file, or ambiguous: **FAIL**;
   - the quote occurs **exactly once inside its section**: **PASS**; if that hit is beyond `LINE_TOLERANCE` of the cited line, print `MOVED <id>: cited line A, found at line B` (informational; exit unchanged). A further occurrence OUTSIDE the section does not fail (item 28: a later entry may re-quote it);
   - the quote occurs **more than once inside its section**: **FAIL** "not unique in its section" (item 87's floor: no typed length; `''`, `a`, `the` fail here);
   - the quote occurs **only outside its section**: **FAIL** "found only outside its section", naming the lines (item 29);
   - the quote occurs nowhere: **FAIL** "QUOTE NOT FOUND", as now.
   Each failure wording is a module constant (as `NEAR_FAIL` is today), and the tests assert on the constant, never on a string literal. `NEAR_FAIL` and the near-line disambiguation of a multi-hit quote are deleted (a section decides, not a line); `LINE_TOLERANCE` stays for the `MOVED` report and the binder only. The `found` statistic (`ATOMS.tsv`'s published line) is the in-section hit.
4. **One home for the atom rules.** `verify_atoms.py` becomes a thin command over `build_graph.load_atoms`-style reading of the one file it is given and `build_graph.verify_atoms` with every atom of that file read (`only=None`), printing its failures and the same summary line; its own `REQ`, `MOD`, `SPK`, `STA` and quote test are deleted. So the stand-alone verifier and the builder can no longer disagree (item 87, "passes the seven atoms `build_graph` fails").
5. **The two TSVs publish the line found** (limits paragraph): `OPEN-QUESTIONS.tsv` and `AMBIGUITIES.tsv` take their `source` cell from the same helper `atom_rows` uses for `ATOMS.tsv` (the line the check found the quote on, else the cited source), one helper for all three.
6. **M04 gains its retire transition** (limits paragraph; `workplan/pipeline-state-graph/machines.yaml`, hand-written, swept): a transition `M04.t6` from "a live figure" to "the figure retired in place (`retired_at`, `retired_by_session`, `retirement_reason`)" via `db.py retire-extraction`, its guards read from `retire_extraction`'s refusals (`grep -n "def retire_extraction" scripts/db.py`, then read the function), each with an evidence needle copied from a refusal string it holds; and `M04.t2`'s `from: "any"` becomes "a live figure (a retired one is refused)", with a needle on `_refuse_retired_figure` in `amend_extraction`. Copy each needle from the code as it stands; type none from this file.
7. **Regenerate** the derived files with `python3 workplan/pipeline-state-graph/build_graph.py` (no flag) and commit them. Correct `workplan/pipeline-state-graph/README.md` where it describes the line check and `verify_atoms.py` (the row "stand-alone quote verifier for one atoms file" stays true; the sentence on what passes changes).

**What reads what this task changes:** every task file's before-and-after `build_graph.py --check`; the owner's walkability reading (`STATE-GRAPH.md`, `WALKABILITY.md`); T-120, which re-quotes the atoms its doctrine edits move and now also binds any atom it adds; whoever reads `OPEN-QUESTIONS.tsv` and `AMBIGUITIES.tsv` for an open ruling's place. **What wrong thing reaches the guidebook without it:** a ruling whose passage was deleted (or repudiated) still counted as standing by the instrument that shows which rulings bind a stage; and an instrument that goes red on every re-quote, so its real findings are ignored. **Code it makes deletable:** `verify_atoms.py`'s second rule set; the near-line disambiguation and `NEAR_FAIL`.

**No schema migration**; no file under `scripts/migrations/`; `sha256sum data/guidebook.db` must not move.

**Code size.** Report `git diff --shortstat "$BASE_PRE" -- scripts schemas .github skills workplan/pipeline-state-graph ':!scripts/migrations' ':!workplan/pipeline-state-graph/atoms' ':!workplan/pipeline-state-graph/*.tsv' ':!workplan/pipeline-state-graph/graph.json' ':!workplan/pipeline-state-graph/*.md'` after `git add` (the instrument lives under `workplan/`, so the standard line alone would show nothing), naming what reads each addition.

## 5. Caller sweep

Names to sweep: `NEAR_FAIL`, `LINE_TOLERANCE`, `verify_atoms`, `MOVED`, `not near cited line`, `quote_occurrences`, `M04.t2`, `bind-sections`.

What a caller is, and what the sweep leaves out: as T-050 section 5 states them; here `workplan/pipeline-state-graph/` is in scope except its generated files (`graph.json`, `STATE-GRAPH.md`, the three TSVs, `CONFLICTS.md`, `CAPABILITIES.md`), which are regenerated, not edited.
```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills workplan/pipeline-state-graph ':(exclude)scripts/migrations' ':(exclude)workplan/pipeline-state-graph/graph.json' ':(exclude)workplan/pipeline-state-graph/*.tsv' ':(exclude)workplan/pipeline-state-graph/STATE-GRAPH.md'
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/2026-11-12-bidirectional-pipeline/tasks ':(exclude)references/project-standards.md'
```
**Callers known on 2026-11-19:** `workplan/pipeline-state-graph/build_graph.py` (`verify_atoms`; its `--selftest` case (l), "quote first, line second: a quote found once and cited 40 lines away does not fail and is reported MOVED", and the gate case (m) that mutates a cited atom's quote: rewrite (l) to the section rule (a quote moved within its section passes with `MOVED`; moved out of it fails) and keep each able to fail; `grep -n '# [a-z])' workplan/pipeline-state-graph/build_graph.py` lists them); `scripts/tests/test_state_graph_instrument.py` (T134-01 to T134-05: T134-03b and T134-03c assert that a quote found twice passes when one hit is near the cited line, which the new rule makes false when both hits lie in one section: rewrite them to the section rule and list each rewrite in the commit; T134-04 asserts on `NEAR_FAIL`, which is deleted: point it at the new constants); `workplan/pipeline-state-graph/verify_atoms.py`; `workplan/pipeline-state-graph/README.md`; `workplan/pipeline-state-graph/machines.yaml` (M04); task files that tell an executor how the check treats a moved quote (`git grep -n -F "MOVED" -- workplan/2026-11-12-bidirectional-pipeline/tasks`: T-130 carries a dated amendment naming `MOVED`; it stays true for a move within a section: add one dated line to it saying a quote found only outside its section now fails). The atoms files are data: the only edit to them is the `section` key.

## 6. Verification

**Step 1, the before-run:** `test_state_graph_instrument graph_audit test_graph_audit`, each as the registry runs it (the loop of T-050 section 6 step 1) into `$SCRATCH/before-<id>.txt`; and keep `$SCRATCH/before-check.txt` (section 3) and `python3 workplan/pipeline-state-graph/build_graph.py --selftest > "$SCRATCH/before-selftest.txt" 2>&1`.

**Step 2, red before and green after.** New cases in `scripts/tests/test_state_graph_instrument.py` (confirm the prefix is free: `git grep -c '"T140-' -- scripts/tests` printed nothing on 2026-11-19). Every fixture is a temporary copy of a cited file (`TASK-FIXTURE`), every atom chosen from the live atoms by query (a cited atom whose quote is found once, in a section with a heading; for YAML, one citing `governance/pipeline-contract.yaml` other than PIP-01); no atom id, line or count is typed. Assert on the module's constants, never on a literal message. Each case shown red on the unchanged code or on a named seeded defect, then the defect removed (`cmp`):

- `T140-01` item 28: on a copy of the ledger, append a later entry (a new `## ` heading) that quotes the atom's quote verbatim: the atom still passes. Red before (T-134's rule: found twice, none near, fails).
- `T140-02` item 29: delete the passage from the atom's section and insert the quote in another section 170 lines below: the atom FAILS as "found only outside its section". Red before (passes as `MOVED`, exit 0).
- `T140-03` the floor: an atom whose quote is changed on a copy to a word occurring twice in its section (derived from the section's text) FAILS "not unique in its section"; the same for an empty quote. Red before.
- `T140-04` moved within the section: three lines inserted above the hit inside the section beyond `LINE_TOLERANCE`: passes and prints one `MOVED` line naming the cited and found lines. Green before; seeded defect: make a move fail, and it goes red.
- `T140-05` the binder: `--bind-sections` on a temporary atoms file writes `section` for the atoms it can bind, leaves an existing `section` untouched (byte-equal line), changes no other key (each line's other keys compared), and prints each atom it could not bind. Red before (no flag).
- `T140-06` one home: `verify_atoms.py` and `build_graph.verify_atoms` give the same failing ids on the same temporary atoms file holding one atom of each failing class; `verify_atoms.py` defines none of `REQ`, `MOD`, `SPK`, `STA` (an AST read). Red before.
- `T140-07` the sections: a `#` line inside a fenced block of a temporary `.md` file is not a heading; a top-level key of a temporary `.yaml` file is; a file of another kind is one section. Seeded defect per branch.
- `T140-08` the TSVs: after `build_graph.py` runs against a temporary output folder (or on the tree, then the files compared), the `source` cell of an atom in `OPEN-QUESTIONS.tsv` is the line `ATOMS.tsv` publishes for it. Red before.
- `T140-09` M04: `machines.yaml` M04 has a transition whose `via` names `retire-extraction`, and `build_graph.py --check` re-reads its needles (an evidence needle changed on a temporary copy of `machines.yaml` to a string absent from `retire_extraction` makes the check fail).
- `T140-10` the test is selected for its own subject: `python3 scripts/run_checks.py --changed-from "$BASE_PRE" --explain` lists `test_state_graph_instrument` among the checks selected for this diff (the T-134 critic's finding: a registered test not selected for a diff to its subject). If it is not selected, add the selecting path to the registry entry's kind paths as T-134's repair did, and say so.

**After-run of the instrument itself:** `python3 workplan/pipeline-state-graph/build_graph.py --check > "$SCRATCH/after-check.txt" 2>&1`, then `diff <(grep ^FAIL "$SCRATCH/before-check.txt" | sed 's/:.*//') <(grep ^FAIL "$SCRATCH/after-check.txt" | sed 's/:.*//')`. Expected: PIP-01 still fails; the only new failures are atoms the section rule finds (not unique in their section, found only outside it, or unbound), each listed in the commit with its class; no failure of another kind disappears. `--selftest` passes after, with its rewritten cases.

**Step 3, the after-run:** the step 1 loop with `after-`; compare failure lines check by check.

**Step 4, the gate, once**, in the background, waiting on its file:
```
scripts/preflight.sh --base "$BASE_PRE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```

## 7. Commit

After the gate is clean: `git add -A . ':!transcripts' ':!*commands.jsonl' ':!.claude/worktrees'`; `git commit -m "governance: bind each state-graph atom to its section and its quote [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the rule, the before and after failure lines by class, the atoms the binder could not bind, the tests rewritten>" -m "<the two trailer lines your session instructions give>"`.

## 8. What you must NOT do

- Do not edit an atom's quote, source line, status or any key other than adding `section`; do not delete an atom (T-120 owns the atoms' text).
- Do not add a length threshold, a list of stop-words, a distance limit, or a tolerance for a quote found outside its section.
- Do not change `walkability.py`, the probes, or the cited-atom selection.
- Do not weaken a check, quarantine a test or change a registry level; do not run `run_checks.py --all`.
- Do not hand-type a count, an atom id or a line number into a file, a test or a message.
- No research rows; no database write; do not push, open a pull request, or subscribe to anything.

## 9. Stop conditions

Stop and report what you ran, saw and expected, when:
- T-134's repair is not on HEAD, or section 3 prints otherwise;
- a red test is not red before or not green after, after one honest attempt;
- the after-run loses a failure that was not a binding failure (you weakened the quote check), or adds a failure of a class section 4 does not name;
- the binder cannot bind a cited atom whose check passes today (report it; do not bind it by hand);
- a heading key is ambiguous in a file a cited atom quotes (two equal headings): the rule then needs a decision;
- a check green before is red after.

## 10. Rollback

Before merge: drop the commit on the coordinator's instruction. After merge: `git revert` in a new pull request (the `section` keys go with it). Never rewrite history.

## 11. Adversarial pass

The coordinator runs it on your commit; do not run `/adversarial`, `/batch-done`, push or open a pull request. The critic should attack: a re-quote inside the same section (fails as not unique: the floor working, or a false red?); a preamble atom; a YAML atom whose key line moves; a heading renamed (fails as section gone: is that right for a ledger, whose headings do not change?); and whether each new test can go red.
