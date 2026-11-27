# impl-A: PR A, plan hygiene (2026-11-27)

Branch ccr-64231823-gqy3xr at 253c2dcc (origin/main 1d52215d plus the session log commit). Nothing committed, staged or pushed. data/guidebook.db and the migrations untouched.

## Generator counts (derive: `grep -o -E 'from the [0-9]+ task files \([0-9]+ open, [0-9]+ merged\)' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-PLAN.md`)
- Committed plan at HEAD (stale text): 129 task files (70 open, 59 merged).
- Generator re-run at HEAD before any edit (`gen-before.txt` here): 73 open, 59 merged, 9 batches, missing [], blocking ['OD-69'].
- After (`gen-after.txt` here): 125 task files (63 open, 62 merged), 8 batches, missing deps [], no CYCLE, blocking [], unregistered []. T-145, T-147, T-148 are in Merged; none of the seven deleted ids appears in the plan (`grep -c -E '\bT-(005|038|039|047|085|122|128)\b' REMEDIATION-PLAN.md` prints 0). T-135 is "NOT FOR SONNET" (no OWNER stop); T-084 is READY.

## Item 1: DONE (deletions plus caller sweep)
Deleted (plain rm): tasks/T-005, T-038, T-039, T-047, T-085, T-122, T-128.
Callers swept: every tasks/T-*.md, REMEDIATION-WORKPLAN.md, the generator, governance/ (check-registry included), scripts/, skills/, .claude/ (`git grep -n -E 'T-(005|038|039|047|085|122|128)-'` over governance, .claude, scripts and skills: no path callers). What changed:
- T-037: dropped T-122 from the dependency bullet and the step-2 sentence "Fill the `check:` of T-122's render criteria" (now "Register this test file"). Render's own logic does not need T-122.
- T-124: dropped "T-122's criterion `spec-four-figures`" from its readers.
- T-137 (open): dropped T-047 from "What reads it".
- T-084: dropped "T-085 (the foreign key, which needs this first)" from Traces; "Do not add the foreign key (T-085)" now "Do not add a foreign key".
- T-059: dropped T-128 and its clause from the dependency bullet (consistent with its existing OD-87 header).
- T-127: dropped T-128 from the dependency bullet, the check command and the stop conditions; removed "OD-67 holds T-128 ..."; repointed "(T-128's)" map-row ban to OD-77, the d4452 sentence to `add-icf-code` (OD-87), and two descriptive mentions. Its OD-87 header and pilot-status history kept.
- T-143: dropped T-128 from the dependency bullet. Left its step-0 datum command and its "Output on 2026-11-19" (they list T-128 as a recorded run; the stop rule reads T-059's own section 2).
- T-110: see item 4.
- skills/run-pipeline_SKILL.md: "the map gap T-128 fills" now "a map gap".
- scripts/tests/test_db_amend_writers.py: comment "(the Reaching code before T-128)" now "(before it is minted)". Comment only.
- REMEDIATION-WORKPLAN.md: deleted the index rows and dependency-list lines of the seven tasks and the "Before T-128" stop row; removed the ids from the verdict list, the MAPPING-DESIGN row, the T-037/T-059/T-110/T-127 index and dependency rows, Wave 0 (list, merge order renumbered, the Independent group), the wave table (waves 2, 3, 5, 6), the lane note, the walkability stop row, the T-084 stop row, the tracks table (REQ-102 proof now "each task's after-test"; REQ-103 tasks), section 9's probe list, the critical-path paragraph's T-128/OD-67 sentences, the OD-04 "Releases", the T-126 row, the register "Read by" and "Tasks blocked" lines of OD-20, OD-24, OD-26, OD-46, OD-67 (and OD-67's dead evidence link), and D-51's "T-128's map rows".
- Stopped on no task: no live task's logic needs what a deleted task provided. Judgment noted: T-037 needed T-122 only to fill the `check:` of T-122's own criteria.
- Not edited (merged task files, records of executed work) and still naming a deleted id: T-020, T-024, T-025, T-030 (T-047), T-078 (T-005), T-126, T-145 (T-128). Open files keep the id only in their OD-87 header or history: T-059 (header, item 7 title), T-110 (header), T-127 (header, pilot status), T-143 (recorded datum).
- REMEDIATION-WORKPLAN.md history passages still naming them (left, history): line ~356 (struck-through passed stop), OD-46 earlier status and options, OD-63/64/65 "it held ... T-122", OD-67 status/question/options, OD-77/OD-82/OD-87 headings, sections 12 and 13. Dead links remain in those history passages: `grep -n -o -E '\(tasks/T-(005|038|039|047|085|122|128)-[^)]*\)' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md` (OD-65 applied note, OD-67 status, sections 12, 13 twice).
- Frozen files still mentioning the ids (derive: `git grep -o -h -E '\bT-(005|038|039|047|085|122|128)\b' -- <file> | sort -u`): OPEN-ITEMS-PLAN.md (T-005 T-038 T-047 T-085 T-128); FOLD-LOG.md (T-038 T-039 T-047); DELEGATED-RESOLUTIONS.md (T-038 T-039 T-047); DELEGATED-RESOLUTIONS-2.md (T-085); DECISION-CLOSURE.md (T-038 T-039 T-085 T-122 T-128); ISSUES-REGISTER.md (T-128); MAPPING-DESIGN.md (T-128); TERM-PLAN-FOLD.md (T-122 T-128); TERM-RESOLUTION-PLAN.md (T-128); PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md (T-128); OPEN-DECISIONS-ADJUDICATION-3.md (T-047 T-085 T-128); BATCH-1-EXECUTION-NOTES.md (T-047 T-085, its "Later tasks" section). The two DELEGATED-RESOLUTIONS-*-REVIEW.md files name none. Also outside the folder: references/project-standards.md (ledger, frozen) and many scratchpad records.
- For the owner: the Definition of Done lines D-02 (walkability registered as a check; T-038's deliverable) and D-13 (the AT-104 add-by-data test; T-047's deliverable) now have no task that delivers them. Neither evidence command names a task file, so I left them (the resolution plan says to delete or reword the apparatus DoD lines only if the owner agrees).

## Item 2: DONE
Verified from git: T-145 is PR #244 (merge 778e1626, migration 165 commit 57fcbf35); T-147 is PR #246 (merge 71b7c582, commits 263baa55 and b561ffa5, migration 167); T-148 is PR #247 (merge 4645a618, commits 86d714ad and 903884b8). The generator's `_executed` reads the first "## Executed" section of BATCH-*-EXECUTION-NOTES.md and counts every T-nnn not followed by " (in part)". Added one bullet at the end of that section of BATCH-1-EXECUTION-NOTES.md: merged outside the batches, each in its own pull request, with the PR numbers and a re-derive grep.

## Item 3: DONE
GAP-372 verified: status OPEN in `gaps`, category SW, P2, naming extraction ids 30, 102, 105, 112, 115, 141, 202, 207, 208, 209, 215. claim_text not amendable verified (`_NOT_AMENDABLE_SVE` in scripts/db.py: claim_type, claim_text, source_section). The derivation query (live extraction, source language per `_translations_owed`'s rule `coalesce(lang_detected, language, 'EN') <> 'EN'`, no current `reviewed` row in `v_translations_current` for its claim_text) returns exactly the GAP-372 rows. Added a blockquote "Not done" paragraph at the top of T-112 with the gap query, the derivation query and the db.py grep; no count and no id list typed. Both embedded commands run and print as expected. Note: GAP-372's own text says "repair each claim_text ... through the extraction writer", which the writer refuses; the paragraph says retire and re-add, as briefed and as the code allows.

## Item 4: DONE, with one brief claim false
- T-135: "Owner decisions" bullet now "none" (it had an [Amended 2026-11-19] note for that passage; replaced with the current fact); new "Delegated resolutions this task rests on" bullet carries OD-69's resolution, the owner's "Ratify all" (Owner ratification 2026-11-19), the ledger grep, the superseded ACTION (2), and `for n in OD-69; do gate $n; done` so the generator reads it as delegated. Ledger: last OD-69 STATUS RESOLVED UNDER DELEGATION, CHECK confirmed (lines 8016-8017).
- T-084: removed the stale HELD banner; the "Owner decisions" bullet now states OD-46 ANSWERED BY THE OWNER 2026-11-19 "admit as declared, scoped-out codes" (ledger 7989-7990) with its grep and the approval-pointer heading, and that section 4's first branch applies. OI-55 (1) sentence left (OD-84 not added there: that bullet does not start with "none", so the generator would read OD-84 as needing the owner's words and close T-084).
- T-056: OD-48 now answered by the owner 2026-11-19, "whom it is for" (option (a)), grep given; items 3 and 3a no longer held; item 3a's "Chosen: held" replaced with "Chosen: (a)". The OD-48 (c) stop line in section 9 left (moot, not false).
- T-106: OD-47 now answered 2026-11-19 ("the document's stated audience judged per item by context, the audience words quoted") with its grep; the task's scope unchanged.
- T-081, T-082: "follow the coordinator's ruling ... when it exists" replaced by OD-84's ruling and grep (red by construction on R1, R9a, R9b; recorded in the PR body; every other rule passes; tests and rebuild gate it; LATEST-RESEARCH not moved). Both bullets start "none in the register", so the generator does not gate on OD-84.
- T-102: did not contain "when it exists"; its OD-84 header already stated the ruling, but section 6, the stop conditions and section 11 step 2 still said to stop until the owner answered. Replaced those three passages with OD-84 and its grep (stop now only on a rule other than R1/R9a/R9b, or if OD-84's status/check changes). Verified `.claude/commands/batch-done.md` line 5 names OD-84.
- T-110: dependency bullet now T-019, T-059, T-102, T-104, T-030, T-068, T-117, T-127, T-133 and T-086. Dropped T-128 (OD-87) and T-123 (parameters 3 and 12 already carry `lower_is_better`; command given in the bullet; T-123 not named in the bullet because the generator would parse it as a hard dependency). Added T-086 (file exists; its 11 bare-ratio rows are all on parameter 3, derive: `select parameter_id, count(*) from source_value_extractions where claimed_unit='ratio' and retired_at is null group by 1`; the engine leaves them out of the value, and OD-63's answer is "all identified values when synthesising and determining"). T-149 and T-150 have no file: nothing added or said. T-133 kept. T-123's "What reads" now says "T-110" without "(which depends on this task)".
- FALSE claim in the brief/plan: "T-110 should drop T-120". T-120 is not in T-110's dependency bullet (it was never there; T-110 reaches T-120 only through T-059). Nothing to drop. T-120 item 2a on main: commit 183a6d66 in PR #248 wrote the circle table into tier-system section 5; not relevant to T-110's bullet.
- OD-87 re-read: T-059 and T-110 drop the d4452-from-T-128 clause; T-127 waits for PR 246 or T-148, both merged. OD-63 re-read (ledger 7421).

## Item 5: DONE (nothing touched)
T-129, T-130, T-139, T-140, T-141, T-070, T-133 and the deferred T-027, T-033, T-040, T-062, T-109, T-118, T-132 unchanged (`git status --short` lists none of them).

## Item 6: DONE
Regenerated with `python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`; output above. Generator defect found, not fixed (out of brief): in its "**Merged**" line, `"## Executed"` inside a double-quoted string closes the string and starts a Python comment, so the rest of that source line is dropped; the generated plan's Merged sentence reads "... names the task's branch, or the re-derive: ..." (truncated).

## Item 7: this file.

## Stale claims found but not in the brief (left, reported)
- T-127's "Owner decisions" bullet still says "**OD-47 stays open**" (answered 2026-11-19). It starts "none as a gate", so no gate effect.
- REMEDIATION-WORKPLAN.md's register still shows OD-46, OD-47, OD-48, OD-67 as REFERRED BACK (the ledger answered all four on 2026-11-19), and the "Before T-084" and "Before T-056" stop rows still wait on OD-46 and OD-48. The generator reads the ledger, not the register, so the plan is right; the workplan text is stale.
- T-086, T-110 and others still carry old pilot and dated-evidence text; not touched.

## Files changed (`git status --short`, less the two append-only logs)
M scripts/tests/test_db_amend_writers.py; M skills/run-pipeline_SKILL.md; M BATCH-1-EXECUTION-NOTES.md; M REMEDIATION-PLAN.md; M REMEDIATION-WORKPLAN.md; D tasks/T-005, T-038, T-039, T-047, T-085, T-122, T-128; M tasks/T-037, T-056, T-059, T-081, T-082, T-084, T-102, T-106, T-110, T-112, T-123, T-124, T-127, T-135, T-137, T-143 (all under workplan/2026-11-12-bidirectional-pipeline/ unless stated).
Code-size line (CLAUDE.md section 8): `git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'` gives 2 files, one line each (prose and a comment).
