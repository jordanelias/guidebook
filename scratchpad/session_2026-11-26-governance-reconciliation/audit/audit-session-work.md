# Audit of the session's work: PR #248, PR #249 and the claims behind them

Auditor: read-only adversarial pass, 2026-11-27 (UTC 04:35 to 05:00). Repository at origin/main b3b3e9b6.
Every figure below came from a command run during this pass; re-run the command and do not trust the figure (rule 7a).
Worktrees used (detached, under this scratchpad): au_wt_base = 4645a618 (main before #248), au_wt_248 = 1d52215d,
au_wt_main = b3b3e9b6, au_wt_4ce = 4ce6da81 (PR #248 head when opened).

**State correction first.** The brief calls PR #249 "open". It is MERGED: `gh api repos/jordanelias/guidebook/pulls/249`
gives merged=true, merged_at 2026-11-27T04:32:29Z, 39 seconds after creation (04:31:50Z), before its CI finished
(check-runs completed 04:33 to 04:41, all success or skipped). So nothing below can go "in PR #249"; every fix is a follow-up.

**Auditor's own write, disclosed.** Re-running the plan generator to check reproducibility, I ran
`scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py` from a worktree. It hardcodes
`ROOT = Path("/home/user/guidebook")`, so it rewrote the canonical checkout's REMEDIATION-PLAN.md (header line only).
I saved the diff to `au_gen_diff.txt` here and restored the file with `git checkout --` at once; `git status` then showed
only the two append-only logs. The database was never touched (scratch copies only; sha256 3d419efb… unchanged).

## Table

| id | what was checked | verdict | sev | one-line reason |
|---|---|---|---|---|
| V-a1 | CLAUDE.md §6 marker line vs ledger 2026-11-14 (OD-57, OD-59, OD-64, "Unicode one") | OK | - | table, ⚠ U+26A0 without FE0F, "never beside" all match |
| V-a2 | tier-system §5 table, thin definition and exemptions vs ledger | OK | - | each row traces to a typed owner line (L7039-7195, 7327-7334, 7424) |
| V-a3 | tier-system §5 OR-22b / OR-23 / OR-23b bullets | CONCERN | low | "without one it anchors nothing" is the ledger's [ASSUMPTION], written as rule (AU-14) |
| V-a4 | tier-system §5 completeness vs the old map | CONCERN | low-med | [EXPERT CONSENSUS] and [UNSUPPORTED] lost their placement (AU-13) |
| V-a5 | tier-system §8 removal vs live callers of "weak band" / §8 | ISSUE | medium | ~20 operative passages now point at a definition that is gone; docs contradict each other (AU-03) |
| V-a6 | tier-system :49 banner | CONCERN | low | ⚠ still used as a banner glyph (AU-15) |
| V-b | synthesis-floor sentence vs 2026-07-25 words and DR-2026-06-10 | OK | - | "can be fable as well", class not version; DR decision 1 |
| V-c | stop-hook sentence vs settings.json and fix_stop_hook_loop.sh | ISSUE | low-med | SessionStart[1] runs it, but its assert fails on today's hook; output swallowed; `grep -c` prints 0 (AU-10) |
| V-d | `ci.yml` job pointer | OK | - | job `commit-msg`, `if: github.event_name == 'push'` (ci.yml:261-265) |
| V-e1 | ledger quotations vs typed words in transcripts/harness_f8d4d6c2/main.jsonl | OK | - | all seven verbatim (queue-operation enqueue records) |
| V-e2 | ledger readings and ACTIONs | ISSUE | high | ACTION (3) cannot be executed: the verb refuses this entry (AU-02) |
| V-e3 | ledger header and omissions | CONCERN | low | header states the C4 reading unmarked; two owner instructions and "PRA" unrecorded (AU-18) |
| V-f | dated or counted statements introduced | CONCERN | low | "Until T-117 lands", "noted/applied 2026-11-26", T-120 v_code_floor_only (AU-16, AU-23) |
| V-g1 | PR #248 title, commit, body | ISSUE | medium | "A1-A5 and B1-B10 applied": B2 skipped, B8 one of four declined, undisclosed (AU-08) |
| V-g2 | PR #248 "identical counts on HEAD" | ISSUE | low-med | retired_vocabulary 251 on base vs 345 on #248: +94, all in the session folder (AU-09) |
| V-g3 | PR #249 body claims | OK with CONCERN | low | preflight and failures true; "Reopened T-112" overstated (AU-27) |
| Q-1 | change-log prose introduced | CONCERN | low | dated "noted/applied 2026-11-26" notes in the conceptual-model banner and T-120 |
| Q-2 | an operative rule weakened or dropped | ISSUE | medium | contract doctrine-recheck criterion dropped two triggers doctrine-recheck.md §1 says remain (AU-04) |
| Q-3 | §8 AMENDED marker (supersession_backpointer_audit) | OK | - | PASS, EXAMINED 35 SUPERSEDES lines; the OR-23 target quote occurs once |
| Q-4 | retired vocabulary attributable to the PRs | OK (governed files) / CONCERN | low | 0 new hits in governed files; +94 in scratchpad/session_2026-11-26-governance-reconciliation/ |
| Q-5 | context_map.py --check on main | OK | - | fresh against HEAD and the live DB |
| Q-6 | generated plan vs task files (re-run) | OK with CONCERN | low | reproduces apart from the header; generator defects (AU-21) |
| Q-7 | deferred and owner-held tasks in the generated plan | ISSUE | medium | T-033, T-040, T-062, T-118, T-132, T-140, T-130 READY; the approved item said "mark deferred" (AU-05) |
| C-1 | rule 4 sweep, deleted task ids | CONCERN | low-med | no live path caller in scripts/skills/governance/.claude/registry; 5 dead links in REMEDIATION-WORKPLAN.md; D-02 and D-13 undeliverable (AU-20) |
| C-2 | rule 4 sweep, removed statements | CONCERN | low | atoms: build_graph --check 1 to 4 failures, verify_atoms 0 to 2 (disclosed, ungated) (AU-17) |
| C-3 | classification soundness of the deletions | ISSUE | high | T-039 delivers the owner's 2026-10-28 request; "no owner request found" is false (AU-01) |
| C-4 | T-110 dependency edit | ISSUE | medium | T-123 dropped on a test of the wrong column; direction_ref_id is NULL on parameters 3 and 12 (AU-06) |
| C-5 | rule 5 (second home) | CONCERN | low | the D1 answer will need a second Owner entry (AU-02); CLAUDE.md and tier-system both hold the table (owner-approved) |
| C-6 | rule 10 | OK | - | no research rows in either PR; the DB change in 5d564930 came from main |
| C-7 | rule 2 attestation | OK | - | neither PR touched decisions/, sessions/ or references/connection-reasoning/; the attestation gates ran NOTHING-IN-SCOPE |
| C-8 | rule 9 | OK | - | unsubscribe 4 s after each create_pull_request; final pushes carry no [skip ci] |
| C-9 | rule 1 commit format (check_commit_msg.py --rev) | OK | - | 921b3352, 183a6d66, 4ce6da81, cd34b96a, 253c2dcc, ee815a82 PASS; merges E4-exempt |
| C-10 | preflight claims (re-run) | CONCERN | low | #248: PASS, 2 advisory; context_map_fresh was stale at 4ce6da81 and not selected (AU-11) |
| C-11 | session log routing (rule 6, CLAUDE.md §7 CURRENT trap) | ISSUE | medium | the whole session's command log went into two other sessions' folders (AU-07) |
| S-1 | "preflight passes with 3 advisory failures identical on HEAD" | CONCERN | low-med | #249 claim true; #248 claim false for retired_vocabulary (AU-09) |
| S-2 | "context_map_fresh caused by the B4 pointer fix" | CONCERN | low | B3 edits (lines 126, 165) changed the same blob (AU-12) |
| S-3 | "345 vs 251; 49 hits are our scratchpad folder" | ISSUE | low-med | the delta is 94, all in our folder (AU-09) |
| S-4 | "PR #248 merged as 1d52215d" | OK | - | merge of 4645a618 and cd34b96a |
| S-5 | "T-145/T-147/T-148 merged (#244/#246/#247)" | OK | - | 778e1626, 71b7c582, 4645a618 |
| S-6 | "all 8 specifications rows are retired" | OK | - | (8, 0): 3 pending and 5 provisional, all retired |
| S-7 | "27 figures marked verified with no full reading" | OK | - | verified_scan_integrity: VERIFIED-WITHOUT-FULL-READING 27, EXAMINED 212 |

## Issues register

**AU-01 (HIGH). T-039 deleted on a false premise: it was the only task that delivers an owner request.**
Where: PR #249 (ee815a82), deletion of workplan/2026-11-12-bidirectional-pipeline/tasks/T-039-owner-edits.md; basis in antagonist-4.md:19 ("Rests on delegated OD-20 only; no owner request found") and classify-1.md:23.
Evidence: references/project-standards.md, "Owner statement 2026-10-28 — an interface to review and edit the tables": "I need there to be some kind of interface where I can manually review and edit the different table values/information and have it propagate accordingly." ACTION (1): "Build the interface ... a read-only browser and the owner's queue first, then edits as proposals." The OD-20 resolution (ledger "Delegated resolution 2026-11-12 — OD-20 the owner's edits") says it is "a reading of the owner's 2026-10-28 request". REMEDIATION-WORKPLAN.md's OD-20 entry: "Why it is the owner's. It is the owner's own tool." After the deletion, `git grep -i -E "owner.{0,20}edit|edits as proposals|change set" -- workplan/2026-11-12-bidirectional-pipeline/tasks` finds no task delivering edits.
Harm: the edit half of an owner request is dropped from the plan with no record that the owner gave it up; the plan reads as complete without it.
Smallest fix: restore the file from 253c2dcc (`git show 253c2dcc:<path>`), restore its index row, re-run the generator; or ask the owner whether the request is withdrawn.
Class: deleting it is OWNER-ONLY (it withdraws an owner request); restoring it is DELEGABLE. Venue: follow-up governance PR.

**AU-02 (HIGH). Ledger ACTION (3) cannot be carried out: the sanctioned verb refuses this entry.**
Where: references/project-standards.md, last entry "Owner statements 2026-11-26 …", ACTION (3).
Evidence: `review_identity_need_icf()` (scripts/db.py) requires the approval-ref entry to name every row as `TRIPLE-<id>`. The entry names none (it gives the derive query; `grep -c TRIPLE-` over its 40 lines prints 0). Dry run on a scratch copy: `REFUSING: review-identity-need-icf: the ledger entry 'Owner statements 2026-11-26 — …' does not name TRIPLE-53.` The D1 execution prompt (decision-prompts-C-D.md:726) plans a separate "Owner answer 2026-11-26 — the three e120 rows …" entry naming TRIPLE-53/57/61, which contradicts ACTION (3) ("citing this entry as the approval reference") and puts the D1 answer in the ledger twice.
Harm: a session that follows the ledger is refused; the one that follows the prompt creates a second home for the same owner answer.
Smallest fix: append one "Owner answer 2026-11-26 — …" entry that names TRIPLE-53, TRIPLE-57 and TRIPLE-61 and says it is what ACTION (3) of the earlier entry points to; do not edit the earlier entry. The rows themselves (53 LPA, 57 TALL, 61 BAR; all `pending`) were confirmed with the entry's own query.
Class: DELEGABLE (records an existing owner answer). Venue: the D1 data PR (rule 10: the ledger append rides with or before it; no gap needed).

**AU-03 (MEDIUM). The §8 band table was deleted while the live corpus still defines things by it.**
Where: governance/tier-system.md §8 (PR #248).
Evidence: `git grep -n -E "weak band|weak-band"` over governance/ finds operative uses that cite tier-system §8 for the band: mission-and-epistemics.md:42 (the §2 heading) and :46; evidence-architecture.md:2, :21, :77, :78, :82, :120, :121, :177, :185, :186, :208; evidence-methodology.md:96, :144, :289; pipeline-contract.yaml:303, :327; adversarial-use-framework.md:29; jurisdiction-philosophy.md:76; held-tensions.md:57; tier-system.md:49 itself. mission-and-epistemics.md:136 and owner-browser.yaml:111 still gloss ○ as "grey, thin, or unverified" "per tier-system.md §5/§8", which now says the opposite. PR #248 edited mission-and-epistemics.md (lines 99, 126, 165) and left :136. The PR body discloses only the five atoms.
Harm: before the PR the documents agreed with each other and disagreed with the ledger; now tier-system and CLAUDE.md disagree with the doctrine file the context map names (`doctrine_file: governance/mission-and-epistemics.md`). That works against the owner's stated goal ("unified and consistent").
Smallest fix: T-120 item 2a already lists these files; give it priority, or add one sentence to tier-system §8 defining "weak band" as the ○ of §5 until item 2a lands.
Class: DELEGABLE under OD-57 for tier-system and the skills; the mission-and-epistemics edit is doctrine and T-120 states that the OD-57 answer releases it. Venue: follow-up governance PR (T-120).

**AU-04 (MEDIUM). The contract's doctrine-recheck criterion dropped two triggers the canonical document still holds.**
Where: governance/pipeline-contract.yaml cross_stage `doctrine-recheck` (PR #248, item B5).
Evidence: the new criterion covers only the `--cross-ref` pass. governance/doctrine-recheck.md §1: "Two remain: the third (§1.3, doctrinal-rule revision) was ABOLISHED 2026-08-19 by OD-10 item 4"; §1.1 (every 25 working sessions) and §1.2 (stage transition) are live text. DR-2026-08-19 §10 item 4 removed "the frozen recheck counter … and the 'any doctrinal revision' recheck trigger"; it does not abolish the stage-transition trigger, and the approval item B5 named only "every 25 sessions".
Harm: the contract and the canonical document now disagree about what binds, and the change went beyond the approved item (the stage-transition clause was not in B5).
Smallest fix: restore the stage-transition clause to the criterion, or put the question "are §1.1 and §1.2 abolished?" to the owner and amend doctrine-recheck.md §1 by an appended note if so.
Class: whether the triggers are abolished is OWNER-ONLY (D-DOCT); restoring the clause is DELEGABLE. Venue: follow-up governance PR.

**AU-05 (MEDIUM). Tasks deferred or held for the owner are offered as READY by the regenerated plan.**
Where: workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-PLAN.md; PR #249 body ("deferral needs no file change").
Evidence: the resolution plan's approved PR A item 3 reads "Defer (leave file, mark deferred)". The plan lists T-033 READY (batch 1), T-040 READY, T-062 READY, T-118 READY, T-132 READY; and the owner-held (Q5) T-140 READY in batch 1, T-130 READY after T-129 (`grep -n -E "\[T-(033|040|062|118|132|140|130)\]" REMEDIATION-PLAN.md`).
Harm: a Sonnet executor follows the plan and builds deferred apparatus, or a task "that reverses something the owner asked", before Q5 is answered.
Smallest fix: one line in each file ("DEFERRED (2026-11-27 resolution plan): do not start", or the owner-hold line) in the form the generator reads as a stop; re-run the generator.
Class: DELEGABLE. Venue: follow-up governance PR.

**AU-06 (MEDIUM). T-110 dropped T-123 by checking the wrong column.**
Where: tasks/T-110-first-determinations.md dependency bullet (PR #249).
Evidence: the new text justifies the drop by "parameters 3 and 12 already carry an accessibility direction". T-123's done state (its §6) is "every direction recorded has a `direction_ref_id`". Live: `(3, 'lower_is_better', None, …)`, `(12, 'lower_is_better', None, …)`. Both pointers are NULL; the source is named only in prose in direction_rationale. T-123's own §3 records this as "no source (history)".
Harm: the first determination rests on a direction that no pointer ties to a source, so a rule-5 pointer is replaced by prose, on the path to the first published cell.
Smallest fix: restore T-123 to T-110's bullet, or narrow T-123 to setting direction_ref_id on parameters 3 and 12.
Class: DELEGABLE. Venue: follow-up governance PR; the data half (setting direction_ref_id) is research; if it is filed as a gap, category SW fits.

**AU-07 (MEDIUM). The session's command log was filed in two other sessions' records.**
Where: scratchpad/CURRENT; scratchpad/session_2026-11-22-icf-umbrella-glossary/commands.jsonl (commits 921b3352, 183a6d66); scratchpad/session_2026-11-26-icf-tree-import/commands.jsonl (253c2dcc, ee815a82, and the working tree now).
Evidence: `cat scratchpad/CURRENT` gives session_2026-11-26-icf-tree-import (set by T-148's 86d714ad, arrived through the merge 5d564930); before that it read session_2026-11-22-icf-umbrella-glossary. 253c2dcc alone adds 285 lines with `"session_id": "f8d4d6c2…"` to the ICF import session's log. CURRENT never named session_2026-11-26-governance-reconciliation, although the folder exists.
Harm: CLAUDE.md §7's named trap. The two past sessions' records now contain this session's commands, and this session's own folder has none.
Smallest fix: move the f8d4d6c2 lines (by session_id) to scratchpad/session_2026-11-26-governance-reconciliation/commands.jsonl; set CURRENT to that stem in the same action.
Class: DELEGABLE. Venue: the next session-log commit.

**AU-08 (MEDIUM). PR #248 says it applied all of A and B; it did not, and does not say so.**
Where: PR #248 title "apply approved items A1-A5 and B1-B10"; commit 183a6d66 ("Applies the owner's 'approve A and B all'"); ledger ACTION (1).
Evidence: impl-X.md "B2 PARTIAL (nothing further applied)": the §8 sign-off pointer, the states line and orient.md were all skipped. impl-Z.md "B8: PARTIAL … adversarial-research_SKILL.md: DECLINED". The PR body lists three skill notes but does not say that B2 was not done or that the fourth skill was declined.
Harm: the owner's merge was described as the owner's review of the applied items ("Merging this pull request is the owner's review of the applied items"); the owner reviewed a list that claimed more than it delivered.
Smallest fix: one line in the next PR body or the session record listing B2 (not applied, and why) and B8 (3 of 4).
Class: DELEGABLE. Venue: follow-up PR body.

**AU-09 (LOW-MEDIUM). Retired-vocabulary claims misstated.**
Where: PR #248 body ("identical counts on HEAD without these edits"); coordinator's reports ("49 hits are our scratchpad folder"; "earlier sessions' scratchpad folders add more of the same").
Evidence: `retired_vocabulary_audit.py --max-per-entry 10000` by file: base 4645a618 = 251, #248 = 345, main = 345. Every one of the 94 new occurrences is in scratchpad/session_2026-11-26-governance-reconciliation/ (ecosystem-census.md 82, ledger-extracts/part-1.md 5, part-4.md 3, antagonist-2.md 2, part-3.md 1, impl-Y.md 1). The "HEAD without edits" comparison was against 921b3352, which is itself part of PR #248 and already held the census.
Harm: the owner was told the failure was not new; relative to main, PR #248 introduced the whole delta. No governed file gained a hit.
Smallest fix: correct the record in the next report; optionally add a `scratchpad/` exemption decision to the owner (do not add it silently).
Class: DELEGABLE. Venue: report or session record only.

**AU-10 (LOW-MEDIUM). The stop-hook sentence describes a mechanism that does not take on today's hook.**
Where: CLAUDE.md §7, "SessionStart also runs it silently (`.claude/settings.json`); whether it took: …".
Evidence: settings.json SessionStart[1] runs `bash scripts/fix_stop_hook_loop.sh >/dev/null 2>&1 || true`. The script asserts the anchor `if ! git diff --quiet || ! git diff --cached --quiet; then`; today's ~/.claude/stop-hook-git-check.sh:85 reads `if ! git diff --quiet || { ! git diff --cached --quiet && ! branch_moved_under_checkout; }; then`, so the assert fails and the output is discarded; `grep -c stophook.ignorePath ~/.claude/stop-hook-git-check.sh` prints 0. impl-X.md recorded this ("In this container it did not take … the script's anchor no longer occurs") and chose not to say so. The approval list the owner answered said (E 6) "the patch does not run in this container".
Harm: a reader concludes that the loop is handled. The check command is there, but the sentence implies the mechanism works.
Smallest fix: "SessionStart runs it silently; its anchor no longer matches the current hook, so it does not apply (check: grep -c …)". Fixing the script's anchor is tooling.
Class: DELEGABLE. Venue: follow-up governance PR (the script fix goes in a tooling PR).

**AU-11 (LOW). PR #248 was opened with a stale context map that the diff-scoped gate could not see.**
Evidence: at 4ce6da81, `context_map.py --check` prints "STALE: governance/context-map.yaml differs from a fresh generation". context_map_fresh's registry `kinds` are data, schema and tooling, so it was not selected for a governance-only diff. It surfaced only after the merge with main (which changed context-map.yaml). On the re-run of #248, attestation_presence and attestation_schema are "BLOCKING and vacuous".
Harm: "preflight passes" at PR open was a pass over a subject that did not include the defect.
Smallest fix: none to the PR (fixed by cd34b96a). Register question for a tooling PR: should context_map_fresh select on changes to the doctrine_file?
Class: DELEGABLE. Venue: tooling PR, or nothing.

**AU-12 (LOW). context_map_fresh attribution incomplete.** cd34b96a and the report credit "the B4 pointer fix". The mission-and-epistemics.md blob was changed by B4 (:99) and B3 (:126, :165). The commit title says "after the tier-system and mission edits", but the map records only the mission sha. Fix: none needed beyond accuracy in future records. DELEGABLE.

**AU-13 (LOW-MEDIUM). §5 no longer places [EXPERT CONSENSUS] and [UNSUPPORTED].** The old map put them at ○; the new §5 names grey, unverified and thin only; skills/evidence-auditor_SKILL.md:47 and references/methodology-evidence-hierarchy-mapping.md:163 still use them. Harm: an auditor cannot mark an expert-consensus value from doctrine. Fix: put the question to the owner (is expert consensus "thin" or "grey"?), or add the two flags to "Not yet ruled". Class: OWNER-ONLY (marker definitions). Venue: owner prompt, then governance PR.

**AU-14 (LOW). An [ASSUMPTION] written as rule.** tier-system §5: "without one it anchors nothing". The ledger's OR-23 record marks "A source with no such route keeps no tier claim and does not anchor" as [ASSUMPTION]. Fix: add "(reading, unratified)" or move it to "Not yet ruled". Class: OWNER-ONLY to ratify; DELEGABLE to mark. Venue: T-120.

**AU-15 (LOW).** tier-system.md:49 still opens with "⚠ Superseded"; §5 now makes ⚠ a marker, and T-120's T120-04 requires "no banner in the file uses ⚠". Known to T-120 item 2. DELEGABLE, T-120.

**AU-16 (LOW). A state sentence that will go stale with nothing going red.** tier-system §5: "Until T-117 lands, `schemas/tier_derivation.py` `band()` and the `specifications.marker` CHECK implement the earlier table". Also, band()'s docstring still says "per tier-system section 5" and describes the old table, so the docstring is false today. Fix: T-117's after-test should delete the sentence (add it to T-117's file). DELEGABLE, T-117.

**AU-17 (LOW).** State-graph atoms: `build_graph.py --check` gives 1 failure on base and 4 on main (EVI-052, EVI-055, EVI-058 added); verify_atoms on atoms-claude goes from 0 to 2 (CLM-038, CLM-041). Disclosed in the PR body; ungated. DELEGABLE, T-120 item 6.

**AU-18 (LOW). Ledger entry completeness.**
(a) The heading states "C4 reopened as one order of authority" without a mark, while the body marks that reading [ASSUMPTION].
(b) The quotations are not in typed order. "Co-2 …" was typed at 00:41, before "our goal …" at 00:51, and "Please provide prompts" at 22:25:46, before "C4 actually …" at 22:26:14. The entry does not claim an order, but the reading "the later question" depends on order.
(c) Owner instructions of the same session that bind future sessions are not recorded: "please have Opus audit claude.md for saliency and efficacy. ensure we strip out all extraneous stuff like change logs and version discussion etc. …" (00:57) and "Tier system appears to be missing the triangles that we discussed in a previous PR. find that ruling" (00:40).
(d) The owner's "PRA" (04:09), on which PR #249 rests, appears only in a commit message and the scratchpad.
Fix: one appended entry. DELEGABLE.

**AU-19 (WITHHELD FOR THE OWNER). Rule 0 and the Co-2 statement.** ACTION (4) holds the sweep ("do not sweep other documents … until C1 is approved"). Rule 0 says a live owner statement supersedes on contact. The approval list put the sweep under C (owner-only) because it touches tier definitions. Whether "Co-2 is co-primary with tier 2" binds the documents now, or waits for C1, is the owner's to say. OWNER-ONLY.

**AU-20 (LOW-MEDIUM). Deletion residue.** REMEDIATION-WORKPLAN.md carries 5 dead links to deleted files (:1257, :1282, :1518, :1586, :1592). DoD lines D-02 (walkability as a blocking check) and D-13 (AT-104) now have no delivering task, so §10's "done" cannot be reached. Both are disclosed in the PR body and left for the owner. Fix: owner answer on D-02 and D-13 (delete or reword), then drop the links. Class: DoD wording DELEGABLE once the owner agrees, per the resolution plan. Venue: follow-up governance PR.

**AU-21 (LOW). Generator hazards.** build_batches.py hardcodes ROOT=/home/user/guidebook, so it writes the canonical checkout from any worktree. It lives in scratchpad/ and is not registered, so no check proves that REMEDIATION-PLAN.md is fresh. The plan's header says "125 task files … at commit 253c2dcc": that commit's tree held 132 task files; the counts are the working tree's. The plan's own count command (`ls …/T-[0-9]*-*.md | wc -l`) prints 129, because it includes the 4 design files. The "Merged" sentence is truncated (disclosed). Re-run otherwise reproduces byte-for-byte apart from the header. DELEGABLE; tooling PR, or nothing (§8: do nothing and say why).

**AU-22 (LOW-MEDIUM, judgment). T-122 deleted as "contract YAML only".** Its own file names a wrong thing reaching the guidebook: "a later change that undoes a ruling (a numeric minimum, a convergence that lifts a marker, a code value hidden behind research) breaks no st[age contract]". The classification did not answer that sentence. DELEGABLE (apparatus under §8); record the answer or restore.

**AU-23 (LOW).** T-120 §3 "Expected output today" still says "the schema holds `v_best_practice` and `v_code_floor_only` only". sqlite_master holds v_best_practice only. PR #248 edited that sentence and left the false clause, so T-120's own stop rule ("if the output differs … stop") will trip. DELEGABLE, follow-up.

**AU-24 (LOW).** Strip-on-touch of version pins (ledger 2026-07-25 ACTION 2): workplan/workplan-item-audit-pipeline-co0009.md:9 "Model: Sonnet 4.6 (audit)" sits in a file PR #248 touched. The others found (Opus 4.7 in storage-derivation, migration-survival, roadmap, bpc-rewrite) are provenance, not routing. DELEGABLE.

**AU-25 (LOW, partly [UNVERIFIED]).** The conceptual-model banner says "owner ruling 2026-09-01". The ledger has no heading dated 2026-09-01. Migration 107 says the layer "was deleted from the database on 2026-09-01" (an execution date). workplan/pipeline-state-graph/CONFLICTS.md:114 cites "the rulings of 2026-08-26 and 2026-09-01". The owner's own words on item codes are relayed from 2026-08-18 (WRK-169/170). Not resolved in this pass.

**AU-26 (LOW, informational).** PR #249 was merged by the owner 39 s after creation, before CI completed (all later green or skipped). Rule 9 compliance is unaffected. The audit brief's premise that #249 is open is stale.

**AU-27 (LOW).** "Reopened T-112": T-112 was READY in the plan before (253c2dcc plan line 69) and after. Nothing was reopened; the file was annotated. The query embedded in it returns exactly GAP-372's 11 ids. Its language test uses `upper(...)`, which impl-A did not mention as part of `_translations_owed`'s rule. DELEGABLE wording.

**AU-28 (LOW).** In the approval list the owner answered, A5 says "(see D4)" for the stop-hook item. D4 is the SCI-into-WHEEL question. DELEGABLE (record only).

## Not reached, or [UNVERIFIED]
- decision-prompts-C-D.md (767 lines): read only the D1 execution prompt (lines 680-730); C1-C10 and D2-D7 prompts not audited.
- antagonist-4.md and path-to-one-determination.md: spot-checked six claims (code_currency_status NULL on all 59, v_code_floor_only absent, 27 rows, T-112 ids, OD statuses, check_jurisdiction in add-lang-jur-pair): all held. The remaining figures (63 parameter-3 code figures, 33 unit rows, REF-01015 edition, parameter 12 closeness) were not re-derived.
- The conceptual-model banner's "owner ruling 2026-09-01" (AU-25).
- Whether the B3 repoints inside migration-survival.md's register keys change any reader (none found by git grep).
- No full `--all` battery run; diff-scoped preflights only, re-run for both PRs.

## Summary (under 200 words)
Most of the edits hold. The marker table, the ⚠ rule, the thin definition, the synthesis floor, the pointers and the ledger quotations all match their sources, and the commit format and rule 9 are clean. Five defects are worth acting on.
(1) T-039 was deleted as "no owner request found", but it delivers the owner's 2026-10-28 request to edit the tables (HIGH).
(2) The new ledger entry's D1 ACTION cannot be executed: the verb refuses it, a dry run on a scratch copy shows the refusal, and the planned fix would record the D1 answer twice (HIGH).
(3) PR #248 deleted the tier-system §8 band table while about twenty operative passages still define "weak band" by it, so the doctrine file now contradicts tier-system and CLAUDE.md.
(4) PR #248 dropped two doctrine-recheck triggers that the canonical document says remain.
(5) Deferred and owner-held tasks are READY in the regenerated plan.
In addition: T-110 lost T-123 on the wrong test; the session's command log is filed in two other sessions' folders; PR #248 claimed all of B was applied; and two figures given to the owner were wrong ("identical counts", "49 hits": the PR added 94). PR #249 is already merged, so every fix is a follow-up.

File: /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/audit-session-work.md
