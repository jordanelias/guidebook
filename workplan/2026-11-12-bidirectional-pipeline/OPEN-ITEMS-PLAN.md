# Open items: what is still open in the remediation plan, and how each is to be resolved

_Written 2026-11-12 (UTC) by an Opus-class planner on the owner's instructions "resolve all open items" and "plan how to resolve all open items first". **This is a plan; it resolves nothing except the fold of the owner's fifth set of answers (step 1, section 1).** Changed: plan documents in this folder, and the generated `REMEDIATION-PLAN.md`; the ledger was not edited (its fifth-set entry was appended by the coordinating session before this pass); no script, schema, governance file, skill, database row or git state. `sha256sum data/guidebook.db` before and after: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`. Canadian English. Every count is a command; where a figure is printed beside one, re-run the command and trust its output, not the figure (CLAUDE.md rule 7a)._

## 0. Verdict

**The plan is complete as to the owner decisions it registers, and not complete as to open items.** After the fifth set, no register decision a task waits on is CLOSED (D-27 prints nothing), D-27b prints nothing (OD-17 is deferred by the owner), and the generator reports no missing dependency, no cycle and no blocking decision:

```
python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py | head -2
# at writing: tasks 68 batches 8 missing deps [] crit 8
#             decisions 38 blocking [] standing ['OD-17'] open 37 unregistered []
```

What is still open is listed in section 2, one row per item, each classed:

- **A** resolvable now by a plan-document, ledger (append) or generator edit;
- **B** needs a new task (tooling or research, apart, rule 10);
- **C** needs the owner;
- **D** resolvable only at execution time (a pilot, a run, a probe);
- **E** not resolvable now; accepted as a standing limit or declined, with the reason.
- **R** resolved since this plan was written (kept for the record; not counted).

Counts by class, and how many need the owner (re-run; the table is the only home of the classes):

```
F=workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md
grep -E '^\| OI-[0-9]+ \|' "$F" | grep -o -E ' \| [A-E] \| [^|]*\|$' | cut -c4 | sort | uniq -c      # per class (inventory rows only: the class is the second-last cell)
grep -E '^\| OI-[0-9]+ \|' "$F" | grep -o -E ' \| [A-E] \| [^|]*\|$' | wc -l                        # all open items
grep -E '^\| OI-[0-9]+ \|' "$F" | grep -E ' \| C \| [^|]*\|$' | cut -d'|' -f2                       # the ones that need the owner
# at writing (after the OI-13 fold): A 3, B 3, C 12, D 16, E 15; 49 open. A resolved row keeps its id with class R and is not counted (OI-13).
```

**The three findings that matter most**, in the owner's order of criteria (integrity first):

1. **`main` holds a stale copy of this workplan, and every task file would start from it** (OI-01, OI-02). PR #218 merged an earlier version; the three plan commits since, the three design files and the fifth-set ledger entry are not on `main` (`git log --oneline origin/main..origin/ccr-408aaa9b-z3e4s0`). Every task file sets `$BASE` by testing only whether `origin/main` *has* `REMEDIATION-WORKPLAN.md`, so it now picks `origin/main`, and T-018, T-026, T-055 and T-102 would stop on a missing design file, or worse, run on stale text. Nothing can start until the plan is merged.
2. **The prior workplan's agreement rules are carried by no task, yet T-110 writes the first live determinations** (OI-09). `workplan/2026-10-23-pipeline-resolution-workplan.md` is "DRAFT, NOT EXECUTED"; this plan imports its T-1a, T-2 and T-3 (as T-016, T-017, T-019) and replaces T-5 (by T-037), but its T-4 (the owner's rulings OR-4, OR-5 and OR-6: anchoring, Co-1 setting a value, unsatisfiable anchors recorded `divergent`), T-1b and T-8, and its data PRs, have no task here and no recorded decline. A first determination computed without the ruled agreement rules would misstate what the evidence supports. Two of the owner's own questions behind T-4 (OR-5b, OR-6c) are still open in the owner queue (OI-07).
3. **The OD-39 supersession pair, as designed, would have turned a check red** (OI-05, fixed in step 1). The audit cannot anchor a `SUPERSEDES` pair whose target is inside the ledger; tested on a scratch copy, PASS became FAIL. T-018 now records the supersession in prose.

## 1. Step 1: the fold of the fifth set (done in this pass)

The owner's fifth set (`grep -n -F "Owner answers 2026-11-12 (fifth set)" references/project-standards.md`) was folded into the plan documents:

| Answer | What changed | Where |
|---|---|---|
| OD-14: codes confirmed ("Confirm all as proposed") | T-102 item 2 (the report to the owner) **discharged**; the draft is kept in the design as record and is not appended; rows are written on `WHEEL`, `PROSTH`, `WALKAID` under `MOB`; after-test (2) reads the confirmation and checks the draft was not appended. The children's ICF crossings are **not** named by the answer line and are held back (OI-03). T-110 item 2 reads the confirmation. | `tasks/T-102-mobility-split.md` §2, §4 items 1–3, §6; `tasks/T-102-design.md` §0, §7, §10; `tasks/T-110-first-determinations.md` §4 item 2; workplan §3, §5, §6, §8 (OD-14), §10 (D-09) |
| OD-17: deferred ("Ratify after T-022 merges, once I have read the corrected contract") | Register status `DEFERRED BY THE OWNER`; asked again with the contract's diff after T-002 and T-022 merge. D-27b counts it as settled. | workplan §8 (OD-17); `DECISION-CLOSURE.md` §4 |
| OD-38 (new): the English name shown when instruments differ | Registered as answered, with the owner's selected label. T-028 gates on it; `rename-term --from-form` takes a named judge and a reason, recorded in typed columns, not as the `AMENDED` trailer the verb appends to `scope_note` today (a correction joined in a note, forbidden by the 2026-11-06 schema-shape statement). | workplan §3, §5, §8 (`### OD-38`); `tasks/T-028-concept-identity.md` §2, §4 item 2; `tasks/T-028-design.md` §7, §8, §15 |
| OD-39 (new): the link-table ruling supersedes the 2026-08-28 clause | Registered as answered. T-018 gates on it. **The design's machine `SUPERSEDES` pair is withdrawn**: the audit counts the target quote in the raw ledger (so the citation line is itself a second occurrence), the quote already occurs twice under the audit's normalisation (the 2026-08-28 ACTION and the 2026-09-01 entry's quotation of it; the design's "once" was a `grep -c` line count), and the marker must sit beside an immutable paragraph. T-018 records the supersession in a prose ledger entry on the 2026-09-01 precedent and runs the audit before and after. | workplan §3, §5, §8 (`### OD-39`); `tasks/T-018-link-table.md` §2, §4 item 2; `tasks/T-018-design.md` §0, §5 step 6, §13 |

The proof the audit cannot take the pair (re-run it; it writes only to a scratch folder):

```
S="${TMPDIR:-/tmp}/supaudit"; rm -rf "$S"; mkdir -p "$S/scripts/audit" "$S/references"
cp scripts/audit/supersession_backpointer_audit.py "$S/scripts/audit/"; cp scripts/dbcore.py "$S/scripts/"; cp references/project-standards.md "$S/references/"; cp -r decisions "$S/"
for f in $(git grep -h -o -E '^SUPERSEDES:\s*\S+' references/project-standards.md decisions | awk '{print $2}' | sort -u); do mkdir -p "$S/$(dirname $f)"; cp "$f" "$S/$f"; done
(cd "$S" && python3 -I scripts/audit/supersession_backpointer_audit.py | tail -1)        # VERDICT: PASS
printf '\n\n```\nSUPERSEDES: references/project-standards.md :: "real FKs. Never a `population_*` link table."\n  BY: references/project-standards.md :: "link table unless that is more prone to errors"\n```\n' >> "$S/references/project-standards.md"
(cd "$S" && python3 -I scripts/audit/supersession_backpointer_audit.py | tail -2)        # VERDICT: FAIL … target quote occurs 3 time(s)
```

After the fold: D-27 and D-27b print nothing, D-36 prints two equal numbers, and the generator line is the one in section 0. `FOLD-LOG.md` §8 records the fold file by file.

## 2. The inventory

Sources were read in full or by section as the coordinator asked, and searched with these commands (the Grep tool cannot see `sessions/`; `git grep` can): `grep -n -i -E 'not resolved|could not|needs the owner|unverified|not piloted|not examined|referred back|not persisted' workplan/2026-11-12-bidirectional-pipeline/*.md`; the "Found and not fixed" list of `DECISION-CLOSURE.md` §3; every "What could not be resolved" list of `FOLD-LOG.md`; workplan §6 and §11; the "Not resolved" and "owner confirms" sections of the three design files; the owner queue (`python3 -I -c "import yaml;d=yaml.safe_load(open('governance/owner-browser.yaml'));print([q['id'] for q in d['decisions'] if 'answered' not in q])"`); and the acceptance tests no task names (OI-18 to OI-21, command there). Items closed by the fifth set are in section 1, not here.

| Id | Item | Source | Resolved when (an observable test) | Class | Who, batch |
|---|---|---|---|---|---|
| OI-01 | The plan branch is not merged; `main` carries the earlier workplan of PR #218, without the design files, the fifth-set entry or this fold | `REMEDIATION-WORKPLAN.md:44` (§2 step 0); `git log --oneline origin/main..origin/ccr-408aaa9b-z3e4s0` | `git diff --quiet origin/main origin/ccr-408aaa9b-z3e4s0 -- workplan/2026-11-12-bidirectional-pipeline references/project-standards.md && echo current` prints `current` | R | merged 2026-11-12 in jordanelias/guidebook#219; Opus coordinator commits and opens the PR; **the owner merges**; R0 |
| OI-02 | Every task file's `$BASE` line tests only that `origin/main` *has* the workplan, so it picks a stale `main` | §2 set-up of every task file: `grep -l 'git cat-file -e origin/main:workplan' workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md \| wc -l` | the line picks the plan branch whenever it differs from `main` in this folder, and `main` otherwise; checked on a clone where `main` is stale and on one where it is current | R | done in R0 (2026-11-12): hardened line in 70 task files; Opus coordinator, one scripted replace over the task files, in the PR of OI-01; R0 |
| OI-03 | The mobility children's ICF crossings are not named by any answer line. As revised (sixth to ninth sets): `WHEEL` receives `SCI`'s crossings that T-102 judges to hold for wheelchair users (design §6a); the design's proposed `WHEEL` d465 d420 d410, `LLD` (was `PROSTH`) d450 d455 and `WALKAID` d450 d465 wait for an explicit yes | `tasks/T-102-design.md` §6a and §7 item 3; ledger fifth to ninth sets | an owner line naming them, or T-102's PR lists them as not written | R | answered 2026-11-13 (tenth set, "Yes, as proposed"); folded into T-102 item 3 and design §7; owner; R1. Blocks no row |
| OI-04 | OD-17: ratifying the corrected contract, deferred by the owner | workplan `### OD-17` (`REMEDIATION-WORKPLAN.md:486`) | `grep -F "OD-17 STATUS:" references/project-standards.md \| tail -1` reads `ANSWERED BY THE OWNER` | C | owner, after T-002 and T-022 merge, with the diff; R6 |
| OI-05 | A supersession whose target is inside the ledger cannot be verified by `supersession_backpointer_audit` (raw-text target count; marker beside an immutable paragraph) | `scripts/audit/supersession_backpointer_audit.py` docstring; `tasks/T-018-design.md` §5 step 6 | accepted: in-ledger supersessions are recorded in prose (the 2026-09-01 precedent); rule 0 already says "Naming them is yours" | E | — (T-018's own case fixed in step 1). Not worth new code: no wrong thing reaches the book that a prose entry does not prevent |
| OI-06 | `rename-term` records every reason as an `AMENDED` trailer on `scope_note`, a correction joined in a note; OD-38 needs the pick's judge and reason in typed columns | `scripts/db.py` (`grep -n 'def rename_term' scripts/db.py`); `tasks/T-028-concept-identity.md` §4 item 2 | after T-028: `rename-term --from-form` without `--judge` is refused; judge and reason are columns; `python3 scripts/audit/joined_cells_census.py` reports no new candidate | D | Opus executor of T-028 names the one home; R5 |
| OI-07 | Owner-queue prompts OR-5b (how "academically sound" is established for a Co-1 source) and OR-6c (whether "T1 states, T2 dispute noted" covers every divergence); both `gates: True` for the prior workplan's T-4 | `DELEGATED-RESOLUTIONS.md:407`; `governance/owner-browser.yaml` | each has an `answered` mark in the owner queue and a ledger answer line | C | OR-6c answered (tenth set); OR-5b answered in part, its three edges are OI-51; owner; R1. Bears on T-110 through OI-09 |
| OI-08 | Owner-queue prompts OR-22b (the marker of a floor claim a study confirms) and OR-23b (whether a registry citation is a valid route for an unretrievable code or standard) | `DELEGATED-RESOLUTIONS.md:407` | answered marks and ledger lines; T-110 names which of its cells each governs | R | OR-22b and OR-23b answered 2026-11-13 (tenth set); owner; R1. Bears on T-110's markers |
| OI-09 | The prior workplan's T-4 (agreement: OR-4, OR-5, OR-6, OR-6b), T-1b, T-6a, T-6b, T-7, T-8 and data PRs D-1 to D-8 and S-1 are neither mapped to a task here nor declined; only T-1a, T-2, T-3 are imported and T-5 replaced | `workplan/2026-10-23-pipeline-resolution-workplan.md:3`, lines 117–157; `01-handshake-ledger.md:160` (P-01-183: "cited and extended, not restated") | a table in the workplan maps every WP id to a task here or to a decline in the owner's words; T-4's rules are a task T-110 depends on, or T-110 states why none is needed | B | partly done 2026-11-13: mapping table in the workplan, T-059 authored for T-4 steps 1, 2, 4; the rows marked "no task" there are OI-52; Opus-class mapping and task authoring (R4); tooling task Sonnet or Opus per its synthesis content; before T-110 |
| OI-10 | Owner-queue prompt OR-14b: the element page written by the specifications pass, or derived when read | `DELEGATED-RESOLUTIONS.md:407`; AT-46 | an answered mark and ledger line; T-037 says which | R | OR-14b answered 2026-11-13: written by the pass; T-060 is the new task; owner; R1. Bears on T-037 |
| OI-11 | Owner-queue prompt OR-25: does batch 23's extraction cap carry over to scans; possibly answered in substance by the read-once statement, which only the owner can confirm | `DELEGATED-RESOLUTIONS.md:407` | an answered mark and ledger line | R | OR-25 answered 2026-11-13: no cap, one source is the unit; owner; R1. Bears on T-105 |
| OI-12 | Owner-queue prompt OT-2: approve the definition of "barrier-free path of travel" | `DELEGATED-RESOLUTIONS.md:407`; ledger 2026-10-29 OT-1 entry | an answered mark; a data PR mints the term | B | OT-2 approved 2026-11-13 (tenth set); a data PR must mint the term (db.py add-term, observation 68), not yet a task; owner; R1. No task here waits on it |
| OI-13 | ~~Whether `SCI` and `LMB` take `MOB` as parent~~ **ANSWERED 2026-11-12 (sixth to ninth sets):** "SCI and LMB go under MOB"; then "except SCI is the same as WHEELCHAIR basically and LMB is the same as PROSTHETIC"; "LMB should be UPL for upper limb then"; "and that doesnt concern mobility"; and the selected option "LLD — 'people with lower-limb differences'". Family: `MOB` with `WHEEL` (taking in `SCI`), `LLD`, `WALKAID`; `LMB` becomes `UPL`, outside mobility | `tasks/T-102-design.md` §0, §2, §6a; `grep -n -E "Owner (answer|clarification) 2026-11-12 \((sixth|seventh|eighth|ninth) set\)" references/project-standards.md` | folded: T-054 (identity successor, crossing retirement), T-102 (`SCI` to `WHEEL`, `LLD`), T-116 and T-058 (`UPL`), T-025, T-055, T-106, T-110, D-09 | R | — (resolved; its open edges are OI-48 to OI-50) |
| OI-14 | The delegation's [ASSUMPTION] that the owner's criteria are numbered in priority order (integrity, then legibility, then coverage); OD-02's English-only pages rest on it | ledger "Owner delegation 2026-11-12" (`references/project-standards.md:5394`); OD-02 correction 3 | an owner line confirming or reordering | R | answered 2026-11-13: yes, 1 then 2 then 3; owner, one tap; R1 |
| OI-15 | The other unratified [ASSUMPTION] marks in the 2026-11-12 entries (the twelfth instruction's line for "appropriate", "advocacy groups" read as disabled people's own organisations, the OD-10 reconciliation, OD-15's attribution, "(or something like that)") | `sed -n '/^## Owner delegation 2026-11-12/,$p' references/project-standards.md \| grep -c '\[ASSUMPTION'` | accepted as standing readings, each reversible by the owner and none blocking a task | E | — Asking each would cost the owner load the 2026-09-09 statement says he cannot carry |
| OI-16 | OD-15: whether not-for-profit status removes WHO's clause 1.2.4 is [UNVERIFIED]; no legal reading was made | ledger OD-15 answer; `DECISION-CLOSURE.md` §2 (OD-15) | accepted: the owner took the decision and the risk; T-103 keeps attribution and marks the correspondence as the project's own addition | E | — |
| OI-17 | No task builds the base coverage view the owner made the acceptance test on 2026-11-06 (seventh, item 3): AT-23, one state per concept and in-scope pair (form with locator / searched, none found / not yet searched) | `FOLD-LOG.md:212`; `tasks/T-028-design.md` §15; ledger `references/project-standards.md:5193` | a view answers AT-23 by one query; its test is red before and green after; T-107's after-test reads it | B | authored 2026-11-13 as T-057 (to be piloted/executed); new tooling task (next free id, `T-057`), Sonnet, after T-026 and T-028; authored by Opus in R4 |
| OI-18 | Acceptance tests no task names but an existing task or Definition-of-Done line already covers (listed in section 3.1) | `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md` (the AT table) and `hs-improvement-programme.md`; command in section 3.1 | each is named in the "Traces to" or after-test of the task section 3.1 gives, or in a D-line | A | Opus coordinator, plan edits; R0 or R4 |
| OI-19 | Acceptance tests that can be tested only on a live determination (AT-02, AT-05, AT-06, AT-14, AT-20, AT-21, AT-41, AT-76) | same | each run after T-110 on a scratch copy, with `EXAMINED` above 0; a red one becomes a task | D | Opus-class, after T-110; R6 |
| OI-20 | Acceptance tests with no home whose state today is unknown (AT-15, AT-16, AT-17, AT-18, AT-34 first half, AT-47) | same | a read-only probe on a scratch copy prints green, or a task is filed for each red one | R | probed 2026-11-13 (`pilot/R2-probes.md`): AT-15 green; AT-16, AT-17, AT-18 and AT-34 first half RED, AT-47 green on state only. The red ones are OI-56; Sonnet probe session (no code); R2. Red ones become B |
| OI-21 | Acceptance tests withdrawn or not testable in this plan: AT-56 (withdrawn, FA-09), AT-45 (not testable until a page reads rooms) | same | declined here, with the reason | E | — |
| OI-22 | The memo flags `MOB`'s nine `high_predictive` ICF crossings as overstated; no task re-judges them | `tasks/T-102-design.md:132`; `POPULATION-UMBRELLAS-MEMO.md` | a research task re-judges each crossing's confidence with a warrant, or the owner declines it | B | research, Opus-class, after T-102; low priority |
| OI-23 | Unpiloted task files: every file except T-006, T-008 (in part) and T-010; the three designs unexecuted; T-008's redesign (`value_as_written`) and T-049 unpiloted | `REMEDIATION-WORKPLAN.md:844` (§11), §12; count: `grep -l '^\*\*Pilot status.\*\* Not piloted' workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md \| wc -l` | each task in the pilot set of section 4 meets the "piloted" stop line; every other task's first real execution is its pilot (workplan §2 step 5a) | R | piloted 2026-11-13 (see REMEDIATION-WORKPLAN.md, "Pilot results, second round"); T-014 dry, T-102 partial; section 4; R3 |
| OI-24 | Checks red on untouched `main` (`test_scan_contract`, `validate_schema_cross_check`, `research_dod`) and `doctrine_recheck.py` exiting 1 when run bare; a pilot's gate cannot tell its own red from these | `REMEDIATION-WORKPLAN.md:836`, `:837` | a baseline file of failing cases on the merged `main`, made once before the pilots; T-040's report list includes `doctrine_recheck.py` | R | baseline made 2026-11-13: `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/baseline-red-on-main.txt` (incomplete: pilots listed more checks red on the base; re-derive on the day); Sonnet, read-only baseline (R2); T-040 reports causes (R5) |
| OI-25 | Whether `add-source` refuses a NULL standing when a URL is given (not probed) | `REMEDIATION-WORKPLAN.md:838` | T-007's red test covers it either way | D | T-007's executor |
| OI-26 | Whether `derive-extraction` should take the as-written wording | `REMEDIATION-WORKPLAN.md:846` | T-008's pilot reads the verb and its report decides; the orchestrator folds the decision into T-008 item 6 | D | T-008 pilot (R3) |
| OI-27 | Which retained artefacts are a source's full text (T-031's derived re-read flag depends on it) | `REMEDIATION-WORKPLAN.md:840`; `FOLD-LOG.md` §4 | T-031 runs a census before it builds the flag and names the artefacts it treats as text | D | Opus executor of T-031 |
| OI-28 | Paths no stress round exercised: candidate staging to admission, a citation-mining row, merging or declining a parameter that holds figures, a non-English source end to end | `REMEDIATION-WORKPLAN.md:842` | one characterisation run on a scratch copy through T-014's harness, each path logged; a defect becomes a task | D | Opus-class, after Wave 1 merges; R5 |
| OI-29 | `source_value_extractions.jurisdiction` repeats the source's jurisdiction on most rows (a rule-5 question) | `DECISION-CLOSURE.md:160` | T-024 reports the count; if it is a second home, a tooling task writer-retires and reader-retires it (committed data migrations insert it, so it is never dropped) | D | T-024's executor; then B if confirmed |
| OI-30 | T-051: how `owner_browser_build.py` handles the new stage value `cross-stage` was not run | `FOLD-LOG.md:99` | T-051's execution runs it before and after | D | T-051's executor |
| OI-31 | T-050: the re-link rule (a retired edge is never un-retired) is a design choice; the full reader set of `search_admissions` is unverified | `FOLD-LOG.md:100`; `DELEGATED-RESOLUTIONS.md` record | T-050's sweep lists every reader; its adversarial pass rules on the re-link rule | D | T-050's executor |
| OI-32 | T-056: whether `ALL`'s successor is a second column beside T-054's or a generalised successor | `FOLD-LOG.md:181` | T-056 names one home and its PR says why | D | T-056's executor |
| OI-33 | The WHO licence copy read on 2026-11-12 is not persisted through `retrieval_log.fetch()` | `DECISION-CLOSURE.md:164` | a manifest line for it in `retrieval-log/` | D | T-103's executor (R10) |
| OI-34 | Prose that restates the old two-way split (`AMB`/`WHEEL`) or `MOB`'s old name, now false after the fifth set | `tasks/T-102-design.md` §11 | T-102's sweep corrects what is not doctrine and lists the rest; a change to `governance/population-taxonomy.md` beyond a pointer goes to the owner | D | T-102's executor; owner for the listed governance changes |
| OI-35 | `provisional` aligned to OD-10 in live prose, and its third (coverage) meaning retired | `DECISION-CLOSURE.md:163` and §3 (OD-10 row) | `git grep -n -i -E "provisional[^.]{0,80}(re-?read\|read again\|review the source\|second review\|stage)" -- skills governance architecture` prints only frozen records | D | T-001's executor (item 6 and its banner) |
| OI-36 | Workplan §4's note that T-026 waits for T-028's design is stale (the design exists) | `REMEDIATION-WORKPLAN.md:168` | the parenthetical is removed; the "also free" command and `REMEDIATION-PLAN.md` agree | R | done in R0 (2026-11-12); Opus coordinator; R0 |
| OI-37 | Whether the order T-016, T-017, T-019 is forced by the code or only by the prior plan | `REMEDIATION-WORKPLAN.md:839` | accepted: kept because it is the ruled order; a pilot that finds it unnecessary says so | E | — |
| OI-38 | Behaviour at a hundred times the present row counts | `REMEDIATION-WORKPLAN.md:841` | accepted: no measured problem; revisit on one | E | — |
| OI-39 | `scripts/run_checks.py --all` never run in one call | `REMEDIATION-WORKPLAN.md:843` | accepted: the owner's 2026-09-23 instruction; D-25's selftest and the diff-scoped gate stand | E | — |
| OI-40 | `sessions/` searched with `git grep`, not read end to end | `REMEDIATION-WORKPLAN.md:847` | accepted: a ruling found later supersedes on contact (rule 0) | E | — |
| OI-41 | Harm-class warrants may be absent for every current conflict, so T-053's engine may refuse on all of them | `FOLD-LOG.md:182` | accepted: the owner's OD-36 rule working | E | — |
| OI-42 | T-018 moves the "at least one lens" rule from a figure-row CHECK to a writer refusal and a blocking integrity case; a hand INSERT could bypass the writer | `tasks/T-018-design.md:221` | accepted: the same exposure as every cross-table rule; rule 3 forbids hand writes | E | — |
| OI-43 | The population memo read English-language and international pages only, could not reach Disabled Peoples' International, and had no co-production; `WALKAID` is a descriptive name (`LLD` is the owner's own wording, ninth set) | `POPULATION-UMBRELLAS-MEMO.md` §10 (from line 359); `FOLD-LOG.md:209` | accepted and stated as provenance in T-102's rows; reopened on new evidence | E | — |
| OI-44 | The memo's findings on `MH` (clinical naming), `NDV` (a coalition held flat), `TALL`, `DEAF`, `LMB`, `COM` | `FOLD-LOG.md:165`; register `### OD-37` | accepted: OD-37 says they stand unless the owner says otherwise | E | — |
| OI-45 | `device_class` stays a CHECK, not a table | `FOLD-LOG.md:164`; `tasks/T-102-design.md` §12 F | accepted: a rule declared once (workplan §7's line on hard-coding) | E | — |
| OI-46 | Sixteen delegated resolutions had no independent check, and the review did not examine HS-1 C-02, C-03 or HS-A12 | `FOLD-LOG.md:103` | accepted: delegation condition (d) names four; the decisions those handshake rows bear on (OD-01, OD-02) were checked | E | — |
| OI-47 | OD-22's reading of "nearest" as nearest on the safe side | `FOLD-LOG.md:101` | accepted: delegated, reversible, its reversal condition recorded | E | — |
| OI-48 | The `SCI` edge of the owner's "basically": a person with an incomplete spinal cord injury may walk (memo §3.4: SCI does not imply a wheelchair); under the fold such a person is placed by device (`WALKAID`, or `MOB` with ICF d450/d455), never under `WHEEL`, and the injury and its level go to the medical lens and ICF b-codes; the condition community loses a code of its own | ledger seventh set "What it does not decide" (2); `tasks/T-102-design.md` §2 (the `SCI` edge) | an owner line accepting the loss, or restoring a condition code (then T-102's §6a is reversed by a new task) | R | answered 2026-11-13: accept; owner; R1. Blocks no row: every held `SCI` figure names wheelchair users |
| OI-49 | The wording the owner confirms: `UPL`'s display name, description and category (proposed: "people with upper-limb differences or disabilities"; category `general`, the CHECK having no physical-not-mobility value) and `LLD`'s description (proposed in `T-102-design.md` §2) | `tasks/T-116-upl-for-upper-limb.md` §4 item 1; `tasks/T-102-design.md` §2 | an owner line confirming or changing each; a change is one `amend-identity` call (T-025, widened to description and category) | R | answered 2026-11-13: confirm both; owner; R1. Blocks no row: written as proposed and amended if the owner answers otherwise |
| OI-50 | The edges of `UPL` and `LLD` the eighth and ninth sets leave open: an upper-limb prosthesis user is `UPL` and a lower-limb one is `LLD` with `device_class` naming the prosthesis (the ledger's [ASSUMPTION]s); the identity codes are not mutually exclusive (a person with a lower-limb difference who uses a wheelchair is `LLD` and `WHEEL`; ninth-set [ASSUMPTION]); whether `UPL` has children (not asked; none invented) | ledger eighth and ninth sets | an owner line ratifying the two readings; the children question asked only if the owner raises it | R | answered 2026-11-13: confirm (a) and (b); owner; R1. Blocks no row |
| OI-51 | OR-5b's three open edges: (1) what "academic rigour re PubMed" means (indexed in PubMed, or judged by PubMed-grade standards; the first collides with the research contract's R5, which says non-indexation is an indexing fact, not a quality fact); (2) how a DPO position statement or a lived-experience publication (no reporting guideline, not a PubMed study) is shown sound; (3) whether the PRISMA / PubMed / ISO test is for Co-1 only or for every tier | ledger, tenth set, OR-5b "What it does not decide" | an owner line answering each; then the Co-1 step of the prior T-4 becomes a task | C | owner; blocks the Co-1 step (no task yet) and is the reason T-110 stops on a Co-1-set bound |
| OI-52 | Prior-workplan items with a ruling and no task: T-1b steps 8 to 10 (OR-3, OR-10, OR-11a), T-4 step 3, T-6b's buckets and coverage view, T-8's distinct-roots condition, D-4, D-5, D-7, D-8 | `REMEDIATION-WORKPLAN.md`, "The prior workplan mapped" | each row has a task, or a decline recorded in the owner's words | B | Opus-class authoring; before T-110 where the item feeds a determination (T-1b steps, T-8, T-4 step 3), otherwise after |
| OI-53 | OR-14b was answered "written by the pass": T-060 needs its design file before anything is built; the questions are listed in T-060 section 3 | `tasks/T-060-element-determination.md` | `tasks/T-060-design.md` exists and the executor of T-060 builds what it names | B | Opus-class design session |
| OI-54 | The owner queue holds five unanswered prompts this plan never listed: OR-1c, OR-10b, OR-17b, OW-1b, OW-1c (not read) | `governance/owner-browser.yaml` | each read, classed (C, or gates nothing) and the plan told | A | Opus coordinator |
| OI-55 | Owner questions raised by the pilots and folds, none yet asked: (1) how a carry-only research batch (searches nothing, admits nothing) is gated, since `research_dod_session` is red by construction on R1, R9a and R9b; it blocks T-102 and every carry task with the same gate text; (2) `governance/population-taxonomy.md` says a sub-code inherits its parent's evidence, which the 2026-08-25 ruling contradicts (T-102-design E6); (3) the crossings' mechanisms in T-102-design §7.3 (E7); (4) the 17 `lang_jur_map` codes missing from the jurisdiction enum: admit as declared out-of-scope codes or remove their pairs (T-024 §9); (5) whether an identical string attested in one language for one concept clashes with a name in another language (T-028 §9); (6) the E4 reading of `other_source` as attested (T-026 §9); (7) whether `add-lens-link` and `retire-lens-link` refuse while a live determination uses the figure (T-019); (8) OR-5b's three edges (OI-51) with the Opus resolution (a delegated resolution, not the owner's words) and its Q1 on soundness at every tier; (9) whether a gentler value that holds only under a condition may leave the headline in favour of a steeper unconditioned one: OR-2 (2026-10-29) says yes, the 2026-10-30 rulings say the gentlest value is the gentlest value and the steepest code value is never highlighted (T-017 critic finding 5; no live cell is affected); (10) whether OR-1c's link table ("link table unless that is more prone to errors") also covers determinations: the question put to the owner said "a figure or a determination" (`governance/owner-browser.yaml`), but T-018 and its design keep one code per model on `specifications` (T-018 critic finding 3); (11) what a typed name/alias table for lens codes would hold, so the warrant on a lens link can be checked as naming the group: `base_icf.title` is NULL for many d-codes, `access_needs` has no name column, `base_taxonomy_medical` is empty and identity names are rarely in a figure's own words, so T-018 checks where the warrant lies and not that it names the code (T-018 critic finding 1); (12) whether the engine should link out-of-lens figures `excluded` at all: T-019 does so because K02 asks every figure of the parameter to be accounted for, but those rows restate what `v_live_lens_links` already says (rule 5) and couple every cell to every figure of the parameter (a new figure tagged for another group turns K02 red and makes unrelated cells stale; amending it is refused naming them); a design choice for the K02 contract, not for the executor (T-019 critic finding F3) | the fold reports in the pilot folder; `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/OR5B-RESOLUTION-DELEGATED.md` | each has an owner line | C | owner; none blocks the next pilot; (1) and (4) block specific tasks |
| OI-56 | Defects found by the pilots that belong to no task: AT-16 (a zero-result search carries no stated cause), AT-17 (readings have no deferred state or date), AT-18 (a figure has no retire path; `ref_id` is reissued if the highest source is hard-deleted), AT-34 first half (a medical-only specification is accepted); `research_tooling_separation` takes no `--base`; three registered checks print no `EXAMINED:` line (`test_assess_cell_pilot`, `test_validate_evidence_state_2_4`, `test_evidence_cell_state_2_3`); `migration_reproducibility.py` keys its rebuild cache on the migration files only; `emit_batch_sql.py --selftest` unregistered; `derive-extraction` cannot write a row (R3 locator refusal); a verb to set `quantity_kind` and its observation on an existing parameter (blocks T-109); the foreign key on `lang_jur_map.jurisdiction` (after OI-55 (4)); `NAME_TO_CODE` a second hard-coded list; rows 189 and 190 carry no comparator; prose that calls `lang_jur_map` empty; five live `condition_on` edges run from a parameter-12 claim to a parameter-3 claim (extraction 117 to 25, and 81, 100, 109, 110), which makes the parameter-12 row a branch and leaves its parameter-3 partner in the headline (T-017 critic finding 3; a data repair, rule 10) | `pilot/R2-probes.md`; each fold report | each has a task or a decline; the registered-check and `--base` items are one small tooling task | B | Opus-class authoring; tooling, rule 10 |

## 3. The resolution plan, by batch

Batches run in this order; within a batch, items are independent unless a dependency is named. Effort: S (under one session), M (one session), L (several sessions). "Rule 10" means tooling and research never share a pull request.

### R0. Merge the plan, harden the base line (now; Opus coordinator, then the owner)

| Items | What changes | Proof | Risk | Effort |
|---|---|---|---|---|
| OI-02, OI-36, OI-18 | One scripted replace of the `$BASE` line in every task file to: `W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"` (and the same in the workplan's §2 step 0 and each `BASE=` re-derivation in the gate blocks); the §4 parenthetical; the acceptance-test map of section 3.1 written into the named task files' "Traces to" cells | the new line prints the branch on today's clone and `origin/main` after the merge; `python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py` unchanged in its first two lines; D-36 equal | a replace that misses a variant of the line: count before and after with the `grep -l … \| wc -l` of OI-02 | S |
| OI-01 | Commit this fold and R0's edits (rule 1 format; `[skip ci]` not on the final push), push, open one PR, unsubscribe at once (rule 9) | `git diff --quiet origin/main origin/ccr-408aaa9b-z3e4s0 -- workplan/2026-11-12-bidirectional-pipeline references/project-standards.md && echo current` after the owner merges | none to the book: plan documents and an appended ledger entry only | S, plus the owner's merge |

#### 3.1 The acceptance-test map (OI-18)

The tests no task names, by command (the set changes as tasks are edited; trust the command):

```
python3 -I - <<'PY'
import re,glob
A='scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/'
at=set()
for f in (A+'hs-improvement-programme.md',A+'td-requirements-and-interface-spec.md'):
    at|={int(x) for x in re.findall(r'\bAT-(\d+)\b',open(f).read())}
named=set()
for f in glob.glob('workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md'):
    named|={int(x) for x in re.findall(r'\bAT-(\d+)\b',open(f).read())}
print(len(at),len(at&named),sorted(at-named))
PY
```

Where each belongs (the test's text is in the AT table of `td-requirements-and-interface-spec.md` or `hs-improvement-programme.md`):

| AT | Task or line that already carries it | Note |
|---|---|---|
| AT-01 | T-038; D-01, D-02 | the stage-pair gate |
| AT-04 | T-037 | no bibliographic field at synthesis, specification or render |
| AT-09 | T-012, T-031 | OD-10: "provisional reading" is a reading's status; the re-read flag is T-031's |
| AT-10 | T-019, T-034 | restate under OD-08: no `pending` row; every relevant lens without a figure is a typed gap |
| AT-12 | T-047 | the add-by-data test reaches a term and a parameter by verbs |
| AT-13 | T-031; D-17 | the derived re-read flag |
| AT-19 | T-005 (views), T-037 (rendered output) | |
| AT-22 | T-110; D-19 | |
| AT-26 | T-028 | conflation recorded, not merged (design §5) |
| AT-27 | T-101, T-052 | |
| AT-28 | T-024, T-047; D-30 | |
| AT-29 | T-101, T-036 | |
| AT-33 | T-019, T-034 | OD-08 |
| AT-36 | T-037 | the named staleness check of OD-12 correction 3 |
| AT-37 | T-037 | |
| AT-38 | T-037 | the wording half needs a reading (an adversarial pass), not a query |
| AT-40 | T-022 | OD-18: an earlier row records only its own state |
| AT-48 | T-037 | now testable: OD-02 (English pages, originals tagged) |
| AT-49 | T-036 | now testable: OD-01 (one determination, jurisdictions as a spread) |
| AT-61 | T-113; D-34 | |
| AT-101 | T-014 | green today for the refusal; kept as a harness probe (OD-27: serial) |

AT-46 belongs to T-037 only after OR-14b (OI-10). The rest are OI-19 (after T-110), OI-20 (probe first) and OI-21 (declined).

### R1. The owner's sitting (any time; none blocks R0, R2 or Wave 0)

The prompts are in section 6, in the order of what each bears on. On each answer the coordinating session appends the owner's words to the ledger (and, for an owner-queue prompt, T-003's `answered` mark follows in its own PR), then folds the answer into the task it bears on: OI-03 into T-102 item 3; OI-07 and OI-08 into the T-4 carry task of R4 and T-110; OI-10 into T-037; OI-11 into T-105; OI-13 into T-110; OI-14 into the delegation entry's [ASSUMPTION] (a new line, never an edit). **Until answered**, R0 adds a stop to T-110 ("a cell whose marker turns on OR-22b or OR-23b, or whose value turns on OR-5b or OR-6c, is not written") and to T-037 ("no element page until OR-14b") and T-105 ("batch by source, the recommended option, and say so") so that no task runs past an open question without saying it.

### R2. Baselines and probes (after R0 merges; a Sonnet session, read-only, no code)

| Items | What | Proof | Risk | Effort |
|---|---|---|---|---|
| OI-24 | On the merged `main`, run each advisory check that is red today once, as the registry runs it, and save the failing case names to `scratchpad/<session>/baseline-red-on-main.txt`; run `python3 scripts/audit/doctrine_recheck.py` bare and as registered, and record both exit codes | the file exists, one line per failing case, with the command and the date | none | S |
| OI-20 | Probe AT-15, AT-16, AT-17, AT-18, AT-34 (first half), AT-47 on a scratch copy with `GUIDEBOOK_DB_PATH` inline on every write verb; print `EXAMINED` and the verdict of each | each green, or a one-paragraph defect note that R4 turns into a task | a write verb without the inline path touches the canonical database: check `sha256sum data/guidebook.db` before and after | S–M |

### R3. The pilot programme (section 4)

### R4. New tasks and plan edits (Opus-class author; after R1's answers where named)

| Items | What | Proof | Risk | Effort |
|---|---|---|---|---|
| OI-09 | Map every id of the prior workplan (T-1a to T-8, D-1 to D-8, S-1) to a task here or a decline. Expected from the reading: T-1a, T-2, T-3 → T-016, T-017, T-019; T-5 → T-037; T-6a → T-015; T-6b → T-101 and T-026; T-7 → T-029 (and OR-14b); T-8 → T-048 (and whether "convergent needs two distinct roots" is built); **T-4 and T-1b have no task.** Write T-4 as a tooling task (agreement: OR-4 anchoring, OR-5 Co-1 with the OR-5b answer, OR-6 `divergent` with the OR-6c answer; a synthesis approach for a divergent cell written only at the Opus floor) and make T-110 depend on it; carry T-1b's steps as ruled or decline each in the owner's words | a mapping table in the workplan with no unmapped id; the generator shows T-110 behind the new task | it widens T-110's critical path; the alternative is first determinations that contradict rulings already given | M to author; the task itself L |
| OI-17 | Author `T-057` (tooling, Sonnet): one view over concepts × the in-scope pairs of `v_research_scope`, joined to `term_aliases` occurrences (T-028's grain, T-026's attestation and locator) and T-026's search-to-form junction, giving exactly one of three states per cell; AT-23 red before, green after; T-107's after-test reads it | the generator places it after T-026 and T-028; T-107 depends on it | the three states must be derived, never stored (rule 5) | S to author; M to build |
| OI-20 (red ones), OI-22, OI-29 (if confirmed) | One task each, in the standard form | each task's red test | scope creep: each must name what wrong thing reaches the book without it (CLAUDE.md §8) | S each |

### R5. Execution-time items (each rides on its task; the task's executor resolves it and reports it under "Task-file defects")

OI-06 (T-028), OI-25 (T-007), OI-26 (T-008's pilot), OI-27 (T-031), OI-28 (after Wave 1: one Opus-class characterisation run through T-014's harness), OI-29 (T-024), OI-30 (T-051), OI-31 (T-050), OI-32 (T-056), OI-33 (T-103), OI-34 (T-102), OI-35 (T-001), and OI-24's causes (T-040). Test: each task's PR names the item and what it found.

### R6. After the milestones

OI-04 when T-002 and T-022 have merged (the owner reads the contract's diff); OI-19 after T-110, each acceptance test run on a scratch copy with `EXAMINED` above 0, a red one filed as a task.

## 4. The pilot plan

**What a pilot is for.** Workplan §2 step 5a makes the first execution of each task its pilot. A separate dry pilot in a scratch clone costs a session; it is worth it only where a defect found at real execution would stall a chain or put a wrong row in the book. So the dry pilots are: the three design-file tasks, the schema tasks with the most dependants, and the redesigned T-008. Every other task is piloted by its first real execution.

**How tasks were chosen.** Dependants by command (each task's count of tasks that wait on it, directly or not, from the workplan's dependency list):

```
python3 -I - <<'PY'
import re
t=open('workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md').read()
blk=t.split('**Dependency list**')[1].split('```')[1]
deps={}
for l in blk.strip().splitlines():
    m=re.match(r'(T-\d+) <- (.*)',l)
    if m: deps[m.group(1)]=set(re.findall(r'T-\d+',re.sub(r'T-\d+-design','',m.group(2).split('[')[0])))-{m.group(1)}
rev={}
for k,v in deps.items():
    for d in v: rev.setdefault(d,set()).add(k)
def down(x,s):
    for y in rev.get(x,()):
        if y not in s: s.add(y); down(y,s)
    return s
print(sorted(((len(down(x,set())),x) for x in rev),reverse=True)[:12])
PY
grep -l 'Schema migration (this task has one)' workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md   # the schema tasks
```

**The pilot set, in the order it must run** (a stage may start when every pilot it stacks on has a patch):

| Stage | Pilot | Why | Stacks on (patches applied in the clone, in this order) | Executor |
|---|---|---|---|---|
| P0 | T-014, by its real execution (first in the merge order) | the harness every behaviour-preserving pilot diffs against | — | Sonnet |
| P1 | T-008 (re-pilot of the redesign) | most dependants; `value_as_written`, its writers and the digitless refusal are unpiloted | — | Sonnet |
| P1 | T-013 | schema; engine and two writers; T-022, T-034, T-040 wait on it | — | Sonnet |
| P1 | T-012 | schema; T-022 waits on it | — | Sonnet |
| P1 | T-024 | schema; many dependants (T-025, T-036, T-047, T-101, T-113) | — | Sonnet |
| P1 | T-026 | schema; its columns were fixed by T-028's design, so a defect here is a design defect | — | Sonnet |
| P2 | T-016 | the chain's second link | T-008 | Sonnet |
| P2 | T-020 | schema; kinds as rows; T-029, T-030, T-047, T-109 wait on it | T-010 (its committed pilot patch, `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-010.patch`) | Sonnet |
| P2 | T-025 | the base writers T-101 and T-102 call | T-024 | Sonnet |
| P2 | T-049 | schema; translations; unpiloted design | T-008 | Sonnet |
| P2 | T-028 | design file; rewrites every name screen | T-026 | Opus-class |
| P3 | T-017 | the chain's third link | T-008, T-016 | Sonnet |
| P4 | T-018 | design file; the link table every lens task uses | T-008, T-016, T-017 | Sonnet |
| P5 | T-019 | the engine's gather on the links | T-008, T-016, T-017, T-018 | Sonnet |
| P6 | T-055 | the parent gather; the device values | T-008, T-016, T-017, T-018, T-019 | Sonnet |
| P7 | T-102, partial | design file; the carry decision table and after-tests (3) and (5) on a sample of `MOB` figures, through `emit_batch_sql.py` to a scratch migration that is never applied to the canonical copy | T-008, T-016, T-017, T-018, T-019, T-055, T-024, T-025 | Opus-class |

**How a stacked pilot is set up.** In a fresh clone under the scratchpad (`git clone /home/user/guidebook "$PILOT/T-nnn"`), `git switch -c pilot-T-nnn "$BASE"` with `$BASE` as R0 sets it, then for each predecessor in the order of the table `git am "<its pilot patch>"`, then `python3 scripts/migrate_db.py` in the clone so the clone's own database carries the predecessors' schema. Migration numbers in a stack are pilot-local: if two predecessors piloted from the same base took the same number, renumber the later one in the clone and say so in the report; the real execution derives its number again (workplan §2 step 2). A stacked pilot's result is provisional on its predecessors: when they merge with changes, the task's evidence command is re-run before its real execution, and a difference is "the ground has moved" (workplan §2 step 6).

**The brief every pilot executor gets** (the lessons of workplan §12, plus two new ones): only `CLAUDE.md` and the task file; `$BASE` from the hardened line (new: a stale `main` was the base defect this time); one gate, `scripts/preflight.sh --base "$BASE" --explain`, once, before the commit; the sweep's exclusion list and "caller, not mention" definition, stop only on a caller that cannot be repaired in scope; each named check run as the registry runs it, before and after, reading its `EXAMINED` line; case ids prefixed with the task number and checked free, probes derived by query; `GUIDEBOOK_DB_PATH` inline on every write verb; failing cases compared with the R2 baseline (new), so a case red on untouched `main` is not read as the task's; nothing pushed, no PR, no adversarial pass; the canonical `sha256sum data/guidebook.db` unchanged; the report and `git format-patch` saved as `scratchpad/<session>/pilot/T-nnn-report.md` and `T-nnn.patch`, the report ending with "Task-file defects".

**"Piloted" means, as a stop line,** all of: (1) the executor followed only `CLAUDE.md` and the task file in a scratch clone; (2) the evidence command printed what the file states, or the difference was reported; (3) red before and green after, or a stop on a task-file defect that the orchestrator then fixed and a second run took to green; (4) the gate ran once and every named check's `EXAMINED` was read; (5) the patch and report are saved; (6) the Opus-class orchestrator folded every defect into the task file (and, for a mechanical defect common to many files, into all of them) and set its line to `**Pilot status.** Piloted <date>: <report path>; defects folded.`; (7) `REMEDIATION-PLAN.md` was regenerated and its "Pilot" column shows it. A pilot never merges and never writes the canonical database.

**Order relative to real execution.** R0 merges first. P0 is a real execution. P1 pilots run in parallel with the real execution of Wave 0 tasks outside the pilot set, which remain their own pilots. A pilot's real execution follows its pilot and its predecessors' merges, one PR at a time.

**Effort.** Sonnet pilots S to M each; T-028 and T-102 L; the orchestrator's folding S per pilot. The pilot set is the table above (count its rows); it spends sessions, so it needs the owner's yes (section 7).

## 5. What this plan will not do, and why

- **Resolve anything beyond the fifth-set fold in this pass.** The owner asked for the plan first.
- **Merge, push or open a PR from this pass.** Merging is the owner's act (workplan §2 step 2); the coordinator commits and opens the PR in R0.
- **Read the ICF crossings into "Confirm all as proposed".** The answer line names codes, names and edges, not crossings; inferring the owner's words is the act the delegation reserved (criterion 1).
- **Write a machine `SUPERSEDES` pair for an in-ledger target, or extend the audit to accept one.** The pair turns the check red; an audit extension is code with no wrong thing in the book it prevents that a prose entry does not (CLAUDE.md §8).
- **Register the owner-queue prompts (OR-5b, OR-6c, OR-14b, OR-22b, OR-23b, OR-25, OT-2) as register decisions.** They have one home, `governance/owner-browser.yaml`; copying them into the register would be a second home (rule 5). R0 instead adds stops to the tasks they bear on.
- **Ask the owner to ratify every [ASSUMPTION] mark** (OI-15). One is asked (OI-14) because a delegated resolution rests on it.
- **Dry-pilot every task.** Workplan §2 step 5a makes a first execution its pilot; dry pilots are spent where a late defect is costly.
- **Run `scripts/run_checks.py --all`**, edit `scripts/`, `schemas/`, `governance/`, skills or the database, or spawn agents in this pass.
- **Reopen any owner answer** of 2026-11-12, or decide doctrine: mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory.

## 6. Owner questions (class C only; phone-ready)

In the order of what each bears on. None blocks R0, R2 or Wave 0.

**1. Merge the plan (OI-01).** "The plan PR carries the three design files, your fifth-set answers and this open-items plan. Merge it?" — `merge` · `not yet`

**2. Your criteria's order (OI-14).** "When the delegated resolutions weighed your three criteria, they took 1 (integrity, rigour, provenance) before 2 (legibility) before 3 (coverage). Is that your order?" — `yes, 1 then 2 then 3` · `<your order>`

**3. Co-1 soundness (OR-5b, OI-07).** "A Co-1 figure may set a value when its source is academically sound. How is that established?" — `derive: a published academic type that is not grey` · `judge each Co-1 source and record it` · `<other>`

**4. Divergence (OR-6c, OI-07).** "'The T1 figure is stated, the T2 dispute noted': only T1 against T2, or any divergence between different tiers?" — `only T1 against T2` · `any divergence between tiers` · `<other>`

**5. Confirmed floor claim (OR-22b, OI-08).** "When a study confirms a regulation's value by finding no reason to change it, which marker does the cell read?" — `the confirming study's own band` · `lower than the study's: <marker>` · `<other>`

**6. Unretrievable codes (OR-23b, OI-08).** "Is a registry citation (jurisdiction, standard number, clause) a valid route for an unretrievable code or standard (T4 to T6)?" — `yes, a registry citation is a valid route` · `no: no academic route, no tier and no anchor` · `<other>`

**7. ICF crossings of the mobility children (OI-03).** "'Confirm all as proposed' named the codes and edges. Do the proposed crossings also stand: WHEEL to d465, d420, d410 (beside the SCI crossings T-102 carries to WHEEL); LLD to d450, d455; WALKAID to d450, d465 (moderate, contextual)?" — `yes, as proposed` · `none` · `<changes>`

**8. Element pages (OR-14b, OI-10).** "Is a page for an element (a ramp as a whole) derived when read from its parameters' determinations, or written by the specifications pass?" — `derived when read` · `written by the pass` · `<other>`

**9. Scan batches (OR-25, OI-11).** "Does batch 23's extraction cap carry over to scans, or is one source the review unit (recommended)?" — `no cap; one source is the unit` · `the cap carries over`

**10. Term definition (OT-2, OI-12).** "Approve the drafted definition and scope note of 'barrier-free path of travel' (in your queue)?" — `approve` · `change: <what>`

**11. [ANSWERED 2026-11-12, sixth to ninth sets]** SCI and LMB under MOB (OI-13): SCI is held under WHEEL; LMB becomes UPL, outside mobility; the lower-limb child is LLD.

**13. The SCI edge (OI-48).** "You said SCI is basically WHEELCHAIR. People with an incomplete spinal cord injury who walk would then be filed by their aid (walking aid, or mobility with no aid), with the injury in the medical lens, and spinal cord injury would have no identity code of its own. Accept that?" — `accept` · `keep a condition code for SCI as well`

**14. Wording of UPL and LLD (OI-49).** "UPL: 'people with upper-limb differences or disabilities', category general. LLD: 'people with lower-limb differences', described as people with a lower-limb difference, from limb loss or from birth, whether or not they use a prosthesis. Confirm?" — `confirm both` · `change: <what>`

**15. Edges of UPL and LLD (OI-50).** "An upper-limb prosthesis user is UPL; a lower-limb one is LLD, with the prosthesis noted on the figure; and a person can be in two groups at once (for example LLD and WHEEL). Confirm?" — `confirm` · `change: <what>`

**12. OD-17 (OI-04; ask after T-002 and T-022 merge, with the diff).** "Do you ratify the corrected pipeline contract?" — `ratified as corrected` · `not yet`

## 7. Recommended order, and what needs a yes first

1. **R0** (now): the coordinator hardens the `$BASE` line, writes the acceptance-test map and the stops for the open queue prompts, commits this fold, opens one PR; **the owner merges it**.
2. **R1** (any time after R0 opens): the owner answers prompts 2 to 10 in one sitting; each answer is folded into the task it bears on.
3. **R2 then R3**: the red-on-`main` baseline and the six probes; then the pilots P0 to P7, with Wave 0's other tasks executing in parallel as their own pilots, one PR merged at a time.
4. **R4** (before T-110): the prior workplan mapped, T-4 carried as a task T-110 depends on, `T-057` (AT-23) authored, probe defects filed as tasks.
5. **R5 and R6**: execution-time items ride on their tasks; OD-17 after T-022; the live-determination acceptance tests after T-110.

**Needs the owner's yes before it starts:**
- **Publishes:** the R0 merge (prompt 1); later, every task PR (merging is the owner's act).
- **Spends:** the pilot programme of section 4 (one session per pilot row, two of them Opus-class and long), the R2 probe session, and the OI-28 characterisation run.
- **Touches doctrine:** the T-4 carry task (evidence-tier and synthesis rules: needs prompts 3 to 6 answered first); writing the ICF crossings (prompt 7, population taxonomy); prompts 13 to 15 (population taxonomy, all non-blocking); any change to `governance/population-taxonomy.md` beyond a pointer that T-102's sweep lists (OI-34); prompt 11.

Nothing else in this plan needs the owner: plan edits, new tooling tasks and execution-time items are the coordinator's and the executors' under the standing authorisation for code and plans.

## 7a. The OI-13 fold (2026-11-12, after this plan was written)

The owner answered OI-13 and clarified it three times (sixth to ninth sets). The mobility family is `MOB` with `WHEEL` (which takes in `SCI`), `LLD` ("people with lower-limb differences", defined by the condition, replacing `PROSTH`) and `WALKAID`; `LMB` becomes `UPL`, upper limb, outside mobility. New tasks: **T-116** (research, Sonnet, after T-025 and T-054: mint `UPL`, place `LMB`'s six crossings by what each names, retire `LMB` to `UPL`) and **T-058** (tooling, Sonnet, after T-116: the DR-2026-07-23 crosswalk back-pointer, the retired-vocabulary record, prose callers). Changed: T-054 (identity successor; crossing rows retire in place), T-102 and its design (`LLD`; `SCI` retired to `WHEEL`, design §6a), T-025 (amend takes description and category), T-055 (a figure counted once at a parent), T-056, T-106, T-110, D-09. Open edges: OI-48 to OI-50. Record: `FOLD-LOG.md` §9. The pilot plan is unchanged except that T-054 gained items; it stays a real-execution pilot.

## 8. What could not be verified in this pass

- Whether the prior workplan's T-4 was partly built under another name: searched `git log --oneline origin/main | grep -i -E 'agreement|OR-5'` and `grep -n -i 'academically sound' scripts/assess/assess_cell.py`, both empty; not proven absent.
- The current state of AT-15, AT-16, AT-17, AT-18, AT-34 and AT-47 (not probed; R2 does).
- Whether `governance/owner-browser.yaml`'s OR-25 is answered in substance by the read-once statement (only the owner can say).
- The pilot patches of T-006 and T-010 apply cleanly to today's base (not tried; P2 tries T-010's).
- The acceptance-test map of section 3.1 was made by reading each test's one-line text against task titles and designs, not by reading every task's after-test; R0's edit checks each placement against the task's section 6.
