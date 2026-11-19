# Remediation batch 1, third tooling stack: T-028 to T-031, T-078, T-083, T-119, T-126, T-134; the third adjudication and its ratification; the tooling tasks it names

**Session id:** `session_2026-11-18-remediation-batch-1-tooling-stack-2`
**Branch:** `ccr-cc893571-i4lug4`; pull request #240 (opened once, last, and unsubscribed at once: CLAUDE.md rule 9).
**Session kind:** tooling only (CLAUDE.md rule 10). No research row and no `scripts/migrations/data_*` file.
**Pointers:** `sessions/LATEST` moves to this session; `sessions/LATEST-RESEARCH` does not (no research was done).

**Derive every figure.** Re-run the command beside a number rather than trust the sentence. `git log --oneline origin/main..HEAD` lists the commits; the schema migrations are `ls scripts/migrations | tail -20`.

## 1. What this session did

- **Executed** nine tasks of the remediation plan, each as one executor commit, an independent read-only adversarial pass, and a repair commit: T-028, T-029, T-030, T-031, T-078, T-083, T-119, T-126, T-134. What each changed is in `workplan/2026-11-12-bidirectional-pipeline/BATCH-1-EXECUTION-NOTES.md`, section "Third stack".
- **Reverted** T-027's edition writer (`c9c84466`, reverted in the next commit): the critic wrote editions the source does not state. The task is rewritten (below).
- **Stopped, not run:** T-052 (names a flag that does not exist), T-056 (OD-48 was closed), T-091 (design file missing), T-135 (the form of OD-69 was open).
- **Recorded the owner's statements** of 2026-11-18 on contact (OD-69, OD-71, OD-72) and applied OD-71 to `term_label_picks` (T-028), `term_relations` (T-029) and `base_parameters.quantity_kind_*` (T-083).
- **Opened the pull request** once, after one diff-scoped gate: `scripts/preflight.sh --base origin/main --explain` (`SELFTEST: PASS`, `PREFLIGHT: PASS`, advisory failures listed in the pull request).
- **Third adjudication** (`workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md`), by an Opus-class adjudicator on the owner's instruction ("have Opus adjudicate all open decisions …"); the owner ratified it ("Sure, append. Ratify all."); the ledger entry is "Owner ratification 2026-11-19".
- **Authored** the tooling tasks of the adjudication's section 4: T-136 to T-143 (new), T-135 and T-027 (rewritten with dated amendments), and dated amendments to T-029, T-031, T-052, T-078, T-083, T-109, the T-028 design file and two governance files. The index and the generated plan are updated (`python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`).

## 2. The adversarial passes

Every executor commit above had a critic pass; the critics' findings, what was repaired and what was not are in `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/sweep-list.md`. Passes that found a defect the executor had called done: T-083 (a weakened warrant), T-078 (the owner's execution condition did not hold), T-126 (an audit that judged nothing), T-027 (fabricated editions), T-134 (a test that could not fail). The T-078 repair and the repairs of T-083, T-126 and T-134 had no second pass. The T-136 to T-143 task files had no critic pass.

## 3. Disclosures

- **Refusal record incomplete.** The T-029 executor deleted `scratchpad/<session>/refusals.jsonl` before 2026-11-18 20:45 UTC; `refusal_register.py classes --session` reads `EXAMINED: 0` for the refusals up to then.
- **Shared scratchpad.** Two critics ran `rm` by glob in the shared scratchpad; another agent's scratch files may be gone.
- **Task authors' reads.** The three authors of T-136 to T-143 report files they read in part (`T-059`, `T-129-design`, `T-132`, `T-056`, `db.py`, the ledger, `OPEN-ITEMS-PLAN.md`); the gaps are in their reports and in each file's own stop conditions.
- **Three readings to confirm before execution:** T-142 is written to run before the research task T-107 (the adjudication said after; after breaks rule 10 because T-107's rows would land with no issuing body); T-143 stores a degrees bound by a reading T-137's exact-fraction storage does not cover, and stops at step 0 until its datum is in hand; item 68's change to `governance/pipeline-contract.yaml` and `governance/pipeline-operations.md` is a rule change and was not made (a prose note only).
- **Open owner questions.** After the ratification none from the third adjudication remains open except the readings above; derive the rest with `grep -F "STATUS:" references/project-standards.md | tail -30`.
- **Assumptions of the ratification entry** the owner has not confirmed: the breadth of "all" (every resolution, not only the nine reserved items) and that "all" includes OD-17, whose contract diff the owner has not seen in this session.

## 4. Next

None mandatory (OD-10 item 4). The tasks of the adjudication's section 4 are authored and indexed; each is its own pull request, tooling before research. Execute in the order of the adjudication's section 4 after this pull request merges.
