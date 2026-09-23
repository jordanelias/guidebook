**VERDICT: Six root causes produce almost every finding in the four audits. Two of them are harness and workflow side effects, not research failures: provenance files are tracked on the work branch, and PRs are opened early and watched live. Together they account for about 1.1B of 3.5B orchestrator tokens, all housekeeping churn, merge races and red log-only PRs. The next three are rules kept by prose rather than mechanism: gates that check a record exists, not that it was done correctly; writers and retractions outside the sanctioned path; and schema designed by trial migration. The last cause runs through everything: sessions have no scope and no reset. Seven resolutions follow. Five are mostly deletions. Two need an owner decision on process, not doctrine. As a class, the check suites are worth running at three fixed points per PR, never as reassurance.**

Holistic lens. Read-only; no suites run. Sources are `audit_tokens.md` (T§), `audit_protocol.md` (P-F#), `audit_architecture.md` (A-F#) and `audit_claudemd.md` (C#), plus the repo facts verified below. Every figure is the audits' own measurement, dated 2026-09-23. Re-derive with their scratchpad scripts; do not trust these numbers.

Repo facts I verified for this synthesis:
- CI triggers only on `push: [main]` and `pull_request: [main]` (`.github/workflows/ci.yml` `on:`). A push to any other branch that has no open PR wakes nothing.
- `transcripts/` (227M, 156 tracked files) and `scratchpad/**/commands.jsonl` (218 tracked scratchpad files) are tracked in git.
- The project Stop hook runs `research_batch_dod.py --all` on every turn (`.claude/settings.json` `Stop`).
- The SubagentStop hook runs `preserve_transcripts.py`, which dirties the tree.
- In this container `~/.claude/stop-hook-git-check.sh` is **unpatched** (no `stophook.ignorePath`), so the 2026-09-18 fix is not in force here.
- `verify-urls.yml:110-121` and `resolve-dois.yml:115-131` `git add data/guidebook.db` and push to main. `regenerate-derived.yml` pushes to main as well.
- The registry has 76 checks: 33 blocking, 41 advisory, 2 informational.

---

## Root causes

| # | Root cause | Findings it generates |
|---|---|---|
| RC1 | **The provenance record lives on the work branch.** Transcripts and command logs append every turn. The Stop hook demands a clean tree; SubagentStop dirties it. | T class 2 (396M), T§5.2; P-F8, P-F4 (7 of 8 early merges were log-only heads, and #149/#151 were red log-only PRs), P-F7 partly; C7; 291 of 448 PR commits are log-only; #129, #135, #149, #150 and #151 exist only to carry logs |
| RC2 | **The PR is opened early and watched live.** Each push produces a CI suite, the suite produces a wake, the wake re-reads 300–780k of context, and `send_later` polls on top. No ruleset gates merges. | T class 1 (637M) and class 5 (69M), T§5.1; P-F9; P-F4 (merge gating); T§4 (0e701d1b against ca1ae452) |
| RC3 | **Sessions have no scope and no reset.** Open status prompts ("present current state", "can we research finally?") become multi-day infrastructure rework in one context that runs to automatic compaction at about 784k. | T class 3 (1,475M above 250k; 51% of main above 500k), T§5.3, T§5.5 (292c6e38: 946M for 2 ledger rows); C5 (34.6KB floor); A-F7 (content barely advanced: 0 live determinations, 0 term adjudications) |
| RC4 | **Gates check that a record exists, not that the work was done correctly, and suites are run as reassurance.** | T§2a (3,107 runs, 584M, 546 reruns with no change); P§4.1; P-F1, F2, F5, F6 (DoD blind to identity, direction, timing and order); A-F1 and A-F5 (count-only and name-only gates); A-F9 (curated map); C "22/76 without authority" |
| RC5 | **Writers and retractions run outside the sanctioned path.** Bots commit the blob to main, and owner-ruled clears were done as hand bulk DELETE. | A-F1 (REF-01006 rewritten; the rebuild disagrees with live), A-F6 (the two clears plus their compensation cascades), P-F1 (exec_id reissued), A-F8 (`decisions` has no verb); CLAUDE.md rule 3's timer trap (#128 conflict) |
| RC6 | **Schema is designed by migration, and rulings bind prose before DDL.** | A churn (7 of 31, or 23%, of migrations correct in-period work; 3 rebuilds of `specifications`), A-F2 (`axes` FK five times after the 08-18 ruling), A-F4 (`item_code` table after the 08-26 ruling), A-F3 and A-F11 (rule-5 copies), A-F5 (the 071 view break repeated; `bpc_metadata` does not import), A-F10 (unwritable tables); P-F12 |
| RC7 | **Scaffolding is stale or bypassed.** Skills were unloadable until 09-18; 9 skills target the deleted item layer; the adversarial pass has no invocation and no record; antagonists run as general-purpose Opus. | T§3, T class 9 volume (about 300M in adversarial roles); P-F3 (no adversarial pass on 5 data PRs), P-F10; C6 |

Owner review absent (P-F4, P§4.6) is not a separate cause. It is RC2 plus a ruleset setting, and R2 folds it in.

---

## Resolutions (execution order)

### R1 — Take the provenance record off the work branch (RC1)
**Mechanism**
- Gitignore `transcripts/` and `scratchpad/*/commands.jsonl` on main.
- `record-command.py` keeps writing the same path, which is now untracked.
- `preserve_transcripts.py` gains `--to-branch provenance`. It copies into a `git worktree` of an orphan `provenance` branch and commits and pushes there.
  - When it runs: at `batch-done`, at session close, and on demand when a natural break is reached.
  - Why it is safe: CI does not trigger on that branch and no PR is ever opened for it.
- Delete the `Stop` hook's `research_batch_dod --all`: 1,407 automatic runs and 2.64M characters injected. `/batch-done` already runs the DoD at the only point it means something.
- Keep the SubagentStop preserve, pointed at the worktree.

**What it removes**
- The loop at source, in every container, so `scripts/fix_stop_hook_loop.sh` is no longer needed. Delete it.
- The CLAUDE.md §7 bullet "TWO TRACKED FILES APPEND ON EVERY TURN" and its `git diff --quiet … exclude` workaround.
- Transcript-only PRs.
- 227M of JSONL in every fresh clone of main.

**Addition justified.** One flag on an existing script. What would reach the guidebook without it: nothing new. It exists to keep rule 6 satisfied while removing its side effect, and `/batch-done` and the session close read it.

**Resolves** T class 2; P-F8; the log-head half of P-F4 (7 of 8 early merges); #149/#151 merged red; C7; and it breaks the class 2 → class 1 feedback loop (T(2) last bullet).

**Expected effect**
- Baseline: 396M in housekeeping-only stop-hook turns (802M including all stop-hook-triggered episodes), 617 hook prompts, and 291 of 448 commits log-only.
- Target: 0 hook prompts from provenance, and 1–3 provenance commits per session, none of them on a PR.

**Owner decision: YES.** The 2026-08-20 directive ("scratchpad … saved always for provenance") and rule 6 say *that* the record is kept, not *where*. Moving it to a branch is a change in custody the owner should approve. Rule 6's text would be edited to name the branch.

### R2 — Open the PR once, at the end, and let a ruleset gate the merge (RC2)
**Mechanism**
- `/session-open` and `/batch-done` state the lifecycle: commit and push to the feature branch freely, since CI does not run on it. Open the PR only when `/batch-done` is COMPLIANT.
- Do not call `subscribe_pr_activity` or `send_later` for CI. Read the check status **once** after about 10 minutes.
- Enable the existing `main` ruleset (id 19136391, currently `enforcement: disabled`) with required status checks, so a merge cannot race CI.

**What it removes**
- Wake-driven turns, self-scheduled check-ins, and agent judgement about whether CI is "green enough".
- CLAUDE.md prose about PR watching. There is none today (P-F9), so nothing is added to CLAUDE.md; the lifecycle lives in the two commands already read at the relevant moments.

**Resolves** T class 1 and class 5; T§5.1; P-F9; P-F4 (the #146 substantive early merge, and any recurrence); T§4 points 1 and 6.

**Expected effect**
- Baseline: 637M in 616 no-op wakes, plus 69M in polling.
- 15 of 17 sessions spent 66–99% of their tokens under a live PR (3,303M of 3,509M).
- Exemplar: 0e701d1b opened its PR at call 163 of 166, had 0 wakes and 0 housekeeping, and cost 42M for batch 18. ca1ae452 cost 211M for batch 19.

**Owner decision: YES, for the ruleset only.** It is the owner's repository setting, and required checks also block the owner's own merges. The lifecycle change is process and can proceed without a decision. **The owner may prefer to see the PR early;** a draft PR opened at the end costs the same.

### R3 — One session per deliverable, with a context ceiling, and a CLAUDE.md that is rules only (RC3)
**Mechanism**
- **A session has one deliverable:** one batch, one PR, or one decision.
- `/session-open` asks for the deliverable in one line. For a status question, `/orient` answers from live state and the session closes. Any infrastructure rework that follows must name the guidebook-reaching defect (§8) before it starts.
- Hand off at about 300k context: write the handoff to the scratchpad and start a new session. Do not ride to auto-compaction at 784k.
- **Trim CLAUDE.md to its brief** ("process, workflow and rules only"):
  - Delete the 10 correction-history parentheticals (`grep -c 'until 20' CLAUDE.md`). Git history is their archive (§8).
  - Delete the stale sentences C1–C4 and C8, and the §7 bullet that R1 retires.
  - Replace the two long unwritability narratives in §4 and §6 with the derivation command alone.
  - Name `.claude/agents` and the four workflow commands (C6).

**What it removes:** multi-day single contexts, 7.3-day sessions (6a6f63cd), and about a third of CLAUDE.md.

**Resolves** T class 3; T§5.3; T§5.5; C1–C6 and C8; and indirectly A-F7. The budget went to apparatus, not to judgement. Three of the four largest sessions, 1.93B tokens between them, were framed as open-ended status or readiness questions.

**Expected effect**
- Baseline: 1,475M in context above 250k and 386M above 500k; 2,826 calls above 500k; 10 forced compactions.
- A 300k ceiling would have eliminated most of the 1,475M.
- CLAUDE.md's 77M floor is minor. Halving it saves about 35M; do it for accuracy, not tokens.

**Owner decision: NO for the trim and the handoff norm** (Layer 0 process). **Advisable YES** on the "status questions do not become rework without a named defect" norm, because it constrains how the owner's own prompts are handled.

### R4 — Suites: a fixed run policy, and correctness gates in place of presence gates (RC4)
**Verdict on the check suites as a class**
- **Low merit per token, high merit in a handful.**
- The defects that mattered in this window were caught by adversarial passes, the owner, or a later session: exec_id reissue, the 071 view break, the axes FKs, the rule-5 copies, the REF-01006 rewrite, and the batch-18 author claims.
- Where a gate did catch something, it was one of five: the DoD, `author_fidelity`, `identifier_floor_audit`, `source_locators_integrity` and attestation. Two of those five are advisory.
- The blocking set is blind by design to the shapes that actually recurred: count-only reproducibility, name-only reference resolution, presence-only DoD rules, and no execution of views.
- Meanwhile 11 advisory checks are red by construction, and rule 6 itself says such checks train the reader to ignore them.

**Policy: suites run at exactly three points**
1. `run_checks.py --changed-from origin/main`, once, before the PR is opened. Add `--selftest` only if a name was renamed or removed.
2. CI on the PR.
3. `research_batch_dod --session`, once, inside `/batch-done`.

Also:
- Never re-run with no intervening change.
- Never run `--all` locally unless the question is corpus-wide.
- A direct `scripts/audit/*.py` call is for diagnosing a red result, not for confirming a green one.

**Mechanism, and what it removes**
- *Delete:*
  - the Stop-hook DoD (done in R1);
  - the commit-message CI job, which was skipped on 42 of 42 PRs. Rule 1 stays prose, and its "Enforced by" line is deleted;
  - `claude_md_spine`, which guards CLAUDE.md prose, not the book (P§3). Owner-neutral: it is code.
- *Make meaningful or delete:* each of the 11 always-red advisory checks gets one of two outcomes (§8 puts the burden on keeping them):
  - either scope it to the diff, so it goes red only on new defects, or
  - delete it.
  `author_fidelity` and `source_locators_integrity` guard §5(c), the worst failure available. They go diff-scoped and **blocking**; their historical backlog becomes a tracked gap.
  Reason: this is not new apparatus. It is existing apparatus given a decision it can change.
- *Replace presence with correctness, inside existing checks (no new checks):*
  - DoD R2 counts forward mining, not the mere presence of a mining row (P-F2).
  - R1 checks order by `exec_id`, so no grey or code search precedes the first co1/co2/T2 search in the batch (P-F6).
  - R8 checks `prior_expectation` against the timestamp of the first retrieval (P-F5).
  - `identifier_floor_audit._INT_KEYS` adds `search_executions` and `search_candidates` (P-F1).
- *Swap:*
  - `migration_reproducibility_deep` becomes blocking and the count-only gate is deleted. This comes after R5, because the deep gate is red today only because of the bot write.
  - Register the existing `scripts/audit/rename_insurance.py`, which SELECTs from every view, in place of relying on `schema_reference_audit` for view health (A-F5). Without it, a view that renders empty book surfaces passes today, as happened with 063 and 071.

**Expected effect**
- Baseline: 3,107 suite runs costing 584M issuing plus 90M carry; 546 no-change reruns (95M); 1,407 automatic DoD runs.
- Exemplar: 0e701d1b ran 7 suites; 616bcdf9 ran `test_db_integrity` alone 104 times.
- Target: about 3–10 local runs per PR.

**Owner decision: NO** (code and checks, §8), **except** the R1–R8 correctness edits. Those encode doctrine in DR-2026-08-19 and the research contract, and a stricter reading should be confirmed. "Order" in particular is a judgement the owner has made before (batch 15, exec 64).

### R5 — One write path for the DB, including bots and retractions (RC5)
**Mechanism**
- `verify-urls.yml` and `resolve-dois.yml` stop committing `data/guidebook.db`. They run on a scratch copy, capture their writes through `emit_batch_sql` → `emit_data_migration`, and open a PR carrying the migration and the retrieval-log payload.
  - `pipeline_runs` goes through the same route, or is dropped from the committed DB. It is not reproducible by definition, and its exemption in `EXEMPT_TABLES` is the leak restated.
- Owner-ruled clears use retire-in-place, the 083 pattern, generalised from `specifications` to the tables it cleared. There is **no DELETE on an append-only log**.
- `search_executions` gets AUTOINCREMENT, and the reissued exec 29–48 records are corrected by a note migration.
- Add a `db.py add-decision` verb, so rulings stop arriving as hand SQL (A-F8).

**What it removes**
- Bot pushes of the blob to main, and with them the "every open PR inherits a binary conflict" trap. That deletes the whole rule-3 timer paragraph in CLAUDE.md.
- The `EXEMPT_TABLES` exemption.
- The compensation cascades: 5 data migrations after 09-01, plus 076 and the tombstones after 09-13.

**Addition justified (the verb).** Without it, a ruling's DB record is hand SQL that no writer check covers. Its reader is `decisions` itself, which the context map and DR readers consume.

**Resolves** A-F1, A-F6, A-F8 (the `decisions` part), P-F1; and it unblocks the R4 swap.

**Expected effect**
- Baseline: the live DB differs from a rebuild on 7 rows (A-F1).
- Two clears generated at least 7 compensations.
- 20 exec_ids now point permanently at the wrong rows.

**Owner decision: NO for the plumbing. YES on one point:** whether an owner "clear" means retire (hidden but kept) or delete. Rule 0 made the 09-13 clear a DELETE; retiring the rows is the same ruling executed without losing identity. Ask once and record the answer.

### R6 — Design the schema before the first migration, and make rulings bind DDL mechanically (RC6)
**Mechanism**
- A schema-changing PR carries one design note in its PR body, not a new file. The note states:
  - the stage of each new column (§3 table);
  - the pointer used instead of any copy (rule 5);
  - the grep plus `sqlite_master` sweep output (rule 4).
- The DDL lands **once**, after the note. No draft migrations are merged.
- `retired_vocabulary_audit`, now diff-scoped under R4, gains the retired DDL shapes `REFERENCES axes`, a new `item_code` column, and `population_code`. That puts a ruling into the gate the same day it is made.
- Delete the dead tables:
  - `item_taxonomy_links`, which has been unwritable since #126 (§8: dead tables are deleted);
  - `icf_medical_map` and `identity_medical_map`, which have been unwritable since birth (A-F10).
- NULL-forward the rule-5 copies:
  - `specifications.functional_basis` → point at `population_icf_links.link_id`;
  - `determination_gates.trigger_tier` and `trigger_evidence_type` → derive from `trigger_ref_id` (A-F3).
- Fix `schemas/bpc_metadata.py:78` and `db.py:90` `_BPC_META_COLS` (A-F5).

**What it removes:** correcting migrations, repeated rebuilds of `specifications`, 3 dead tables, 3 copied columns, and one module that does not import.

**Resolves** A churn, A-F2, A-F3, A-F4, A-F5, A-F9 (partly), A-F10, A-F11 (review 087 under the same note).

**Expected effect**
- Baseline: 7–9 of 31 schema migrations (23–29%) correct in-period work.
- `specifications` took 8 DDL passes and 3 rebuilds.
- Target: correction migrations only for defects discovered later, not for sweeps owed by the same PR.

**Owner decision: YES for the medical-lens map tables only.** The four-lens model (D-0170) is doctrine, so removing its only medical tables should be confirmed even though they cannot hold a row. **NO** for the rest.

### R7 — Retire stale scaffolding, and make the adversarial pass one bounded, recorded step (RC7)
**Mechanism**
- Delete the item-layer skills: `item-audit-pipeline`, `audit-consolidator` and `item-consolidation-analyzer`. Strip the `item_code` and `items` passages from the other six that `skill_staleness.py` lists (T§3).
- Retire `multilingual-research`'s CHECK/LOG steps explicitly, since `search_languages` and `search_coverage` hold 0 rows. Alternatively, fold the language rule into the SessionStart contract, which already replaced them in practice (P-F10).
- `/batch-done` runs `/adversarial` **once**, using the `antagonist` project agent at a fixed model and a single round. It writes the verdict into the batch attestation, and the DoD requires that field when the batch touched the data paths (DR §7).

**What it removes**
- 3 skills and the stale passages in 6 more.
- The unrecorded CHECK/LOG obligation.
- 8-round adversarial loops run as general-purpose agents.

**Addition justified (the attestation field).** Without it, a data diff reaches the book unchallenged. That happened on #140, #143, #144, #146 and #154, and on #155 the pass refuted two headline findings before merge. The DoD reads the field.

**Resolves** P-F3, P-F10, T§3, T class 9 volume, C6.

**Expected effect**
- Baseline: 0 adversarial passes on 5 of the batch PRs.
- About 300M in adversarial-role subagents, with 292c6e38 alone running 8 rounds costing 193M.
- Target: one pass per data PR, at about 7–30M each, which is the measured single-antagonist range.

**Owner decision: YES for retiring `multilingual-research`'s CHECK/LOG,** which carries the 19-language posture. **NO** for the rest.

**Execution order**
1. **R1 and the R2 lifecycle, together, first.** They stop the bleeding and every later PR pays less.
2. **The R4 run policy**, which is immediate and costs nothing.
3. **R3 trim.**
4. **R5**, because R4's reproducibility swap depends on it.
5. **R4 check edits.**
6. **R6.**
7. **R7.**

The R2 ruleset can be switched on whenever the owner approves it.

---

## Findings I believe are wrong or overstated

1. **T "32% of tokens were waste" is correct as a token count but is not a cost.** 98.6% of tokens are cache reads, billed at a fraction of input price. The *ratios* hold, because waste turns are the same cache-read-dominated shape as work turns. The 4.24B headline should not be read as a bill.
2. **"None of those 44 checks changes a decision" (T§5.4) is overstated, and it contradicts P§3.**
   - "Never red locally" is weak evidence: CI logs are absent, outputs were cut with `| tail`, and a rarely-firing check such as `check_yaml` or `schema_reference_audit` can still be cheap insurance.
   - The always-red list includes `author_fidelity` and `source_locators_integrity`, which P§3 shows caught real §5(c) defects. They are red because a real backlog has no repairing writer, not because they cannot discriminate.
   - The right test is §8's (what wrong thing reaches the book), not the pass/fail distribution.
3. **P-F4 as HIGH is overstated.**
   - 7 of 8 early merges were on `session command log` heads, and #149/#151 carried only logs. Nothing reached the book.
   - "0 GitHub reviews" on a single-author project whose owner directs in-session is not a protocol breach. No protocol text requires a GitHub review.
   - The real residue is #146's substantive head, which merged 44 seconds into its suite. That is **MEDIUM**, and a symptom of RC1 and RC2.
4. **P-F1 as CRITICAL is better rated HIGH.**
   - The damage is real: session records now resolve to the wrong rows, and R8's gate is defeated.
   - But the rows involved had been ruled untrusted, and no evidence reaching the book changed.
   - The gate blindness belongs under RC4.
5. **A-F7 "built on a population umbrella" is partly overstated.**
   - `identity_code` is one of the four ruled lenses, and D-0182's CHECK requires at least one. `MOB`-only is legal.
   - All 8 specifications are retired, so judgement has not completed. §6's "zero links **after judgment** is a defect" is therefore not yet triggered.
   - The valid core is a direction-of-travel signal: the ICF lens is 0 of 48 on extractions, and the umbrella framing is creeping back.
6. **P-F11's "39 stamps more than 5 minutes off" is noise.** Amends and merges explain it, and rule 1's check is itself vacuous (R4 deletes it).
7. **A-F1 is correct on reproducibility.** But the Crossref enrichment probably made REF-01006 *more* accurate. The defect is the missing path and the missing retrieval artefact, not wrong data. Verify the six author rows against the payload before calling it a §5(c) event.
8. **C7 ("fix script not executable by agent") is the design working, not a defect.** The script says so itself. The defect is that the fix is per-container: it is unpatched in this container today. R1 makes it unnecessary.
9. **T§5.5 measures value as "net DB rows".** That undercounts sessions whose output was schema (556a3270's re-key). 292c6e38's verdict still stands: 68% housekeeping.

---

## Handshake (with resolution_granular.md G1–G18)

The CLAUDE.md items are done (e3846fa): the correction histories are removed, the stale sentences corrected, the agents and commands named, and a suite-frequency rule added. That covers R3's trim and R4's run policy, and they are not repeated below.

### R → G mapping

| R | Implemented by | Contradicting G-item, and resolution |
|---|---|---|
| **R1** provenance off the work branch | G13-1, G13-2 | **G13-1 contradicts R1 and wins.** Live logs go to a gitignored path and are copied into tracked paths only at breaks. That fixes the loop with no custody change, so **R1 no longer needs an owner decision** and the orphan `provenance` branch is dropped. G10's reviewer-transcript pointer also needs the transcripts on main, which an orphan branch would break. **G13-2 contradicts R1** (scope the Stop hook where R1 deleted it). I accept G13-2: it keeps the owner's "cannot quietly end non-compliant" rationale at negligible cost. |
| **R2** PR last, ruleset | G13-3, G11-1, G11-2, G11-3 | None. |
| **R3** session scope and context ceiling | G13-4; CLAUDE.md (done) | None. |
| **R4** suites policy and correctness gates | G7, G8-2/3, G9-2, G12, G16, G18, the merit table | **G7 contradicts R4 and wins:** fold the view probe into `schema_reference_audit` rather than register `rename_insurance.py`. **The merit table contradicts R4 and wins:** it demotes `claude_md_spine` where R4 deleted it, because it is nearly free. **source_locators_integrity:** the merit table keeps it advisory where R4 promoted it, and G's order wins (build `amend-locator`, repair, then promote). |
| **R5** one DB write path | G1, G6, G8, G15 | **G1 partly contradicts R5** (the bot pushes the migration and blob to main instead of opening a PR). See the G1 amendment below. |
| **R6** design before migration | G2, G3, G4, G5, G7, G16 | **G4 contradicts R6 and wins:** keep `icf_medical_map` and `identity_medical_map`, because 074's header records the owner leaving them pending content. R6's "retired DDL shapes in `retired_vocabulary`" is not in G; it is added as the G2 amendment below. |
| **R7** skills and adversarial pass | G10, G14 | **G14 contradicts R7:** it keeps `multilingual-research`, where R7 retired its CHECK/LOG steps. The merit table also silently retires them ("drop the `search_languages` clause"), which contradicts G14. Both routes need an owner decision (the 19-language posture). See the G14 amendment below. |

### Verdict on each G-item

- **G1 AMEND.**
  - The claim that committing the migration together with the blob "removes the binary-conflict trap" is wrong: the blob still changes on main while PRs are open.
  - What it actually removes is the *judgement* in resolving the conflict. `git merge origin/main` followed by `migrate_db.py` re-applies the bot's migration deterministically.
  - Say that in rule 3 rather than claiming the trap is gone.
- **G2 AGREE.** Add R6's point: `retired_vocabulary` (once repaired) flags new DDL containing `REFERENCES axes`, a new `item_code` column, or `population_code`. That makes a ruling bind DDL the same day it is made.
- **G3 AGREE.**
- **G4 AGREE.** This supersedes R6's deletion of the medical-lens tables.
- **G5 AGREE.** Do it first.
- **G6 AGREE.**
- **G7 AGREE.**
- **G8 AGREE.** On severity: I rate the provenance damage HIGH, not CRITICAL, but that changes neither the fix nor its order.
- **G9 AGREE.**
- **G10 AGREE.** The data-migration trigger (step 2) is what makes the pass unmissable on batch PRs.
- **G11 AGREE.** G11-1's required checks must name only the checks the classify job always reports, so that a skipped job counts as success. See the CI answer below.
- **G12 AGREE.** R1 exceptions for chain-following batches are an owner question.
- **G13 AMEND (step 1).** State that the copy into tracked paths happens at `/batch-done` and at session close, **never between PR open and merge**. Otherwise each break is a push, and each push is a CI run on the PR.
- **G14 AMEND.** Keep the skill, but put the CHECK/LOG question to the owner: either run them, so `search_languages` and `search_coverage` fill, or retire them explicitly. Do not drop the `research_protocol_audit` clause until that answer is in.
- **G15 AGREE.**
- **G16 AGREE.**
- **G17 AGREE.** Step 2 goes in as advisory now; making it blocking waits on the owner, because it tightens D-0182.
- **G18 AGREE.**

### Owner question: how to make sure the CI wake-ups never happen again

**Verified:** every subscription in the transcripts was an explicit agent call; the harness did not subscribe automatically. The calls used **both** namespaces: `mcp__github__subscribe_pr_activity` 18 times and `mcp__Claude_Code_Remote__subscribe_pr_activity` 10 times. `mcp__Claude_Code_Remote__send_later` was called 67 times.

| Proposed element | Verdict | Why |
|---|---|---|
| `permissions.deny` in `.claude/settings.json` | **AGREE. This is the guarantee.** | It must list both subscribe names plus `mcp__Claude_Code_Remote__send_later`, and `mcp__Claude_Code_Remote__create_trigger` to close the same poll route through a Routine. With no subscription, there is nothing to wake on. The cost: a deny cannot discriminate by argument, so reminders the owner asks for are blocked too. The owner lifts the deny when they want one. |
| CLAUDE.md rule | **AGREE, one line only.** | The mechanism holds the rule. The line only has to say why the tools are denied, so an agent asked to "watch the PR" tells the owner about the deny instead of working around it. |
| Open the PR last | **AGREE.** | This is independent of wakes: it also removes CI runs on intermediate heads and merge races (P-F4). With G13-1, nothing is pushed between PR open and merge. |
| `paths-ignore` in ci.yml | **DISAGREE.** | (1) On `pull_request`, path filters are evaluated over the **whole PR diff**, so once a PR has any substantive file, every log-only push still runs CI. The filter only helps log-only PRs, and G13-1 already eliminates those. (2) With G11-1's required status checks, a workflow skipped by `paths-ignore` leaves those checks pending, which **blocks merge**. The existing `classify` job already routes by path inside the workflow, where skipped jobs count as success. |
| `concurrency` in ci.yml | **AGREE, for CI minutes only.** | Use `group: ${{ github.workflow }}-${{ github.ref }}`, with `cancel-in-progress` for `pull_request` only, never for pushes to main. It does **not** prevent wakes, because a cancelled suite still emits `check_suite.completed`. |

**Net:** the deny list (both namespaces) plus opening the PR last is sufficient. G13-1 removes the pushes that fed the loop. Keep concurrency as a cost measure and drop `paths-ignore`.
