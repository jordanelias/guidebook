# Antagonist 3: adversarial check of CLAUDE.proposed.md and claude-md-audit.md

Written 2026-11-26 by a read-only antagonist. Repository at `71b7c58` (HEAD = origin/main = worktree for CLAUDE.md; `diff` empty). Nothing in the repository was edited. Scratch work is in `/tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/a3/`. "P:n" = a line of CLAUDE.proposed.md, "C:n" = a line of the current CLAUDE.md.

Operating limit: this agent attacks and does not draft. Under CORRECTIONS, "exact text" is given only where the right text already exists (the current file, an owner quotation, a ratified record). Where new wording would be needed, the authority it must match is named instead.

## 1. Verdict table

| Item | Verdict | Reason (detail in section 2) |
|---|---|---|
| C-01 | SURVIVES | Verbatim move; the doctrine paragraph is byte-identical (fid.py) |
| C-02 | SURVIVES | Operative sentence kept; atom CLM-003 no longer resolves, but nothing cites it |
| C-03 | WOUNDED | SessionStart[0] hook 1 does run ensure-deps (verified). The reword removes needle "exits 0 on failure by design" (machines.yaml M10.t1) and atom CLM-023, so `build_graph.py --check` goes red |
| C-04 | SURVIVES | session-open.md:6 carries "before the first Bash call" |
| C-05 | WOUNDED | preflight runs the selftest and passes extra arguments through (read, not run). Removing the "Run suites rarely" heading breaks atom CLM-024, which machines.yaml cites |
| C-06 | SURVIVES | `scripts/preflight.sh` runs `run_checks.py --selftest` before the diff gate |
| C-07 | SURVIVES | |
| C-08 | SURVIVES | |
| C-09 | SURVIVES | ci.yml has the `commit-msg:` job at 261, `if: push` at 265 and the call at 274 |
| C-10 | SURVIVES | SYNTHESIS_PATH_RE matches `.md` only, and `_attestation_path_for` builds `<dir>_<stem>`. Note: the rule now equals the gate's scope |
| C-11 | WOUNDED | Atoms CLM-012 (cited by build_graph.py) and CLM-013 no longer resolve |
| C-12 | WOUNDED | The sweep list is a hand-curated directory list. It omits `workplan/` and `decisions/`, which is exactly where the caller this audit missed lives |
| C-13 | WOUNDED | Same content. Breaks CLM-015 (cited by conflicts.yaml) and the phrase "survivable, therefore permanent" (quoted at test_db_integrity.py:1012 and in T-133) |
| C-14 | SURVIVES | SubagentStop runs preserve_transcripts.py (settings.json) |
| C-15 | SURVIVES | |
| C-16 | SURVIVES | `citation_mining_session` is `level: advisory` (registry) |
| C-17 | WOUNDED | Both examples are false today (db.py:3403 and :2119). Deleting them drops the registry `note:`/`floor_basis:`/`no_floor:` instruction, which has live targets, and misses a live instance of the anti-pattern (`add-supersession-check --tier`, required) |
| C-18 | SURVIVES | P:139 is blank |
| C-19 | SURVIVES | |
| C-20 | SURVIVES | Low-value disambiguation lost |
| C-21 | SURVIVES | Removes an owner quotation, but under the checked "never spell the stages out a second time" rule. Medium confidence |
| C-22 | WOUNDED | Drops the warning that any table-to-stage assignment written before 2026-08-27 predates the seven stages |
| C-23 | FALSE | Rewords away "base is not a stage" but keeps that dead convention's exemption. Contradicts the owner ruling of 2026-08-27 (base is stage 1; base+research view protected). Also breaks CLM-028 |
| C-24 | WOUNDED | Breaks CLM-029, cited by conflicts.yaml and build_graph.py |
| C-25 | WOUNDED | "wording" comes from the recorder's [ASSUMPTION], not the owner's words. The conflict with rule 10 ("never patched with hand SQL") is not named |
| C-26 | WOUNDED | The stated reason misreads the sentence: the absent thing is the CLI flags. The constraint survives at its home (db.py: "Do not 'fix' it by adding the flags") |
| C-27 | SURVIVES | |
| C-28 | SURVIVES | `next-id` choices include `ref` |
| C-29 | WOUNDED | The probe is identical in db-census.md. "Breaks: none found" is false: the audit's own grep finds two architecture callers |
| C-30 | SURVIVES | No root index.html |
| C-31 | SURVIVES | Low: "autistic community co-authors" becomes "disabled co-authors" (L5) |
| C-32 | WOUNDED | The OR-1 paraphrase drops OR-1's lens clause, which bears directly on §6's "at least one" |
| C-33 | WOUNDED | Substance right. Breaks CLM-039, cited by conflicts.yaml |
| C-34 | SURVIVES | |
| C-35 | WOUNDED (low) | Floor class matches the 2026-07-25 ACTION (3)(4); no version pin. The subject is narrowed to `specifications` on a delegate's mapping (T-120). The SessionStart contract keeps the old name |
| C-36 | WOUNDED | Narrows the lens ruling from "any table attaching a determination to a group of disabled people" to the determination only. Drops "one CHECK". Breaks CLM-042 and CLM-043 (both cited) |
| C-37 | WOUNDED (low) | Drops the `/__agentproxy/status` `recentRelayFailures` diagnostic |
| C-38 | WOUNDED | "a Glob that names the directory" replaces the Grep tool's `glob` parameter. The content-search technique is lost |
| C-39 | WOUNDED | The hook name is dropped. "In one action" is narrowed to the merge case, while session-open.md:35 cites §7 for the general rule. Breaks CLM-046 (cited) |
| C-40 | SURVIVES | Low: meta-scripts-spec.md L4.3 prose caller |
| C-41 | SURVIVES | |
| C-42 | WOUNDED | The owner said strip "version discussion". The PI-version trap is expanded, and duplicated in the §9 history list |
| C-43 | WOUNDED | "False in both halves" is overclaimed: "an agent cannot apply it" is still true. The proposal drops that constraint and asserts an effect the script fails to produce on the current hook |
| C-44 | n/a | Merged into C-07 |
| C-45 | WOUNDED | §2.4 as the exhaustive owner list omits owner-gated items (CLAUDE.md's own reserved blocks, `.ignore` entries). The quoted sentence "Nothing is added without naming what reads it" disappears |
| C-46 | WOUNDED | "What to do now" conflicts with the retained authority sentence, with DR-2026-08-19 §A and with orient.md:25. The history list reclassifies owner-ratified doctrine (DG-NON) |
| O-01 | SURVIVES (class) | Arguably already settled by the owner's 2026-11-26 "strip out … change logs" |
| O-02 | SURVIVES (class) | Same as O-01 |
| O-03 | SURVIVES | All four deny entries exist (settings.json). Whether the names match is [UNVERIFIED] |
| O-04 | SURVIVES (class) | Not a CLAUDE.md change; harness configuration |
| O-05 | SURVIVES | Content already settled by the ratified ledger RULE (project-standards.md:17) |
| O-06 | WOUNDED | Misclassed as pending. The owner answered OD-57 "yes" to a question that names "replacing the ○ gloss in `CLAUDE.md` §6". Under rule 0 the retained line is already superseded |
| O-07 | WOUNDED | Not on the ledger's owner-approval list by the audit's own criterion, yet C-46 cannot stand without deciding it |
| O-08 | SURVIVES | |
| O-09 | SURVIVES | |
| O-10 | SURVIVES | |

## 2. Detail, worst first

### F1 (HIGH). C-23 keeps a convention the owner ended, under a new rationale
- P:201: "Every stage points into `base`, so a view reading one stage plus `base` is not counted as crossing."
- The owner's ruling of 2026-08-27 (references/project-standards.md:2298-2345): "**This ends the "not a stage" convention entirely.** … It is dead. `base` is stage 1." Its ACTION (4): "`v_coverage_priority` is protected". Its table ("retired convention (`base` excluded)" against "RULED: `base` is stage 1") counts base+research views as cross-stage.
- decisions/DR-2026-08-27-seven-stage-spine-base-is-first.md:28: "Because a cross-stage view IS the pointer, the protected set grows, and the view that joins it is v_coverage_priority (base+research …)". Under "Alternatives considered" it rejects "Keep substrate outside the stage set (the retired convention)".
- The exemption has already been used: scripts/migrations/164_drop_unread_views.sql:10, "Neither is a cross-stage pointer (CLAUDE.md section 3): v_code_floor_only reads specifications plus base", followed by DROP VIEW. `v_coverage_priority` is still live (sqlite_master).
- The audit (C-23) called this "remove an internal contradiction" and resolved it toward the dead convention. The 2026-09-10 sweep entry (project-standards.md:2849) restates the convention, but it is a sweep record, not an owner ruling. It postdates and contradicts the 2026-08-27 owner ruling, and rule 0 makes the ruling win.
- Shows it: `sed -n 2298,2345p references/project-standards.md`; `sed -n 20,40p decisions/DR-2026-08-27-seven-stage-spine-base-is-first.md`.

### F2 (HIGH). A third mechanical caller of CLAUDE.md was missed, and the proposal breaks it
- Audit: "Two callers parse CLAUDE.md mechanically". False. `workplan/pipeline-state-graph/build_graph.py --check` verifies atom quotes and machine needles against CLAUDE.md. `workplan/2026-10-12-simplification-workplan.md:62` names it: "`build_graph.py --check` fails on … a quote an atom cites from a file the step edits (CLAUDE.md, …)", and requires 0 failures after each PR.
- Emulated (CLAUDE.md read replaced by the proposal, nothing written): main gives 1 failure (PIP-01, pre-existing); the proposal gives 12. The new failures are CLM-012, 015, 023, 024, 028, 029, 039, 042, 043, 046, plus machine needle M10.t1 ("exits 0 on failure by design").
- The standalone `verify_atoms.py` on the 49 CLAUDE.md-sourced atoms gives 0 problems on the current file and 19 on the proposal.
- It is not a registered check, so CI stays green over it. That is §5(a)'s shape.
- Shows it: `python3 -I scratchpad/a3/bg_emul.py scratchpad/CLAUDE.proposed.md | grep FAIL`; `python3 -I workplan/pipeline-state-graph/verify_atoms.py scratchpad/a3/claude_atoms.jsonl --repo scratchpad/a3/repo_pro`.

### F3 (MEDIUM-HIGH). The marker line is kept although the owner has already replaced it
- P:275 is byte-identical to C:372: "◐ policy/standards only · ○ grey, thin or unverified".
- Ledger :7265, OD-57 as registered: "apply the circle table now? … (● T1, T2, Co-1, Co-2; ◐ T3, T4; ○ T5, T6; ⚠ in place of the circle for a grey, unverified or thin basis) … and replacing the ○ gloss in `CLAUDE.md` §6." Ledger :7327-7328: "OD-57: yes / OD-57 STATUS: ANSWERED BY THE OWNER".
- Under rule 0 the current gloss is superseded on contact. The proposal hands every session a marker definition the owner has inverted: under the answer, grey, thin or unverified takes ⚠, not ○.
- O-06 treats this as pending owner timing. The only real open point is coordinating with T-120 item 2a, not approval.
- Item 2 of the brief (byte-identity) passes here, and that pass is itself the defect.

### F4 (MEDIUM-HIGH). Three different answers to "what to do now"
- P:369 routes "What to do now" to `/orient` and the ledger tail.
- P:27-29 keeps, verbatim: "Where it disagrees with `decisions/DR-2026-08-19-…`, that instrument wins and this file is what to correct".
- DR-2026-08-19:3-4: "THIS DOCUMENT SUPERSEDES ALL OTHER PLANNING DOCUMENTS … the only planning artifact a session needs to read". Its §A (lines 19-21) says CLAUDE.md "Where it disagrees with this instrument, this instrument wins".
- `.claude/commands/orient.md:25`: "1. `decisions/DR-2026-08-19-…` — what to do now". So the proposed pointer sends the reader to `/orient`, and `/orient` sends them back to the DR.
- By the proposal's own precedence sentence, the new row loses to the DR unless a supersession is recorded. None exists: there is no SUPERSEDES line against DR-2026-08-19's planning claim (`git grep -n 'SUPERSEDES: decisions/DR-2026-08-19'` returns two unrelated clauses).
- The audit's warrant ("the owner named the remediation plan on 2026-11-25") rests on a recorder [ASSUMPTION]. Ledger :8487: "[ASSUMPTION: "this remediation plan" is the plan of `…REMEDIATION-WORKPLAN.md` … the owner did not name a file]".
- Answer to brief item 5: yes, the DR's self-precedence creates a conflict, and the proposal does not name it.

### F5 (MEDIUM). The §9 history list reclassifies owner-ratified doctrine
- P:380-382 declares `governance/conceptual-model.md` and `governance/functional-taxonomy.md` "History, not live guidance".
- conceptual-model.md:4: "**Status:** SIGNED OFF 2026-04-26". functional-taxonomy.md:3: "**Status: RATIFIED — owner directive "Ratify all", 2026-07-21. Doctrine OPERATIVE".
- Neither file carries a whole-file supersession marker (`grep -n -i superseded` finds only clause-level notes).
- `governance/decision-protocol.md` §2.4 item 2 ("Population taxonomy structure") is DG-NON. The classification comes from ADJ-01/ADJ-02, not the owner. Classed DELEGABLE by the audit; it is owner-only.

### F6 (MEDIUM). C-45 makes §2.4 the exhaustive owner list, and drops a quoted sentence
- P:345: "Owner sign-off is required for content and doctrine only — the list in `governance/decision-protocol.md` §2.4."
- §2.4 (read in full) omits items that live records reserve to the owner: `.ignore` entries (".ignore": "Changing the ENTRIES in this file is OWNER-GATED"); the CLAUDE.md blocks the ledger reserves (:8204 "The owner approves the goal sentence, rule 0, rule 9, the tier and Co-1 definitions, and the fate of the layer model"); schema-bound owner reviews (:8487 `review-identity-need-icf --approval-ref`).
- Lost sentence: C:505 "**Nothing is added without naming what reads it.**" It is quoted verbatim by the immutable `scripts/migrations/095_drop_amendments_no_reader.sql:9` and `073`, by ledger :2837 and :2975, and in the `retired_vocabulary_audit.py` docstring.
- The audit's quote sweep (3b, "all eight present") was line-based and could not see these multi-line quotes (L8).

### F7 (MEDIUM). The lens half of the key is narrowed, and OR-1's lens clause omitted
- C:386-388: "any table attaching a determination to a group of disabled people takes **three lens columns (identity, ICF, access need), one CHECK, real FKs**". P:289-291 attaches the lens to "the determination's key" only and drops "one CHECK".
- P:276-277 cites OR-1 for cell states but omits its next sentence (ledger :4614): "a determination should never be limited to only one lens because we have different models … we need to have each model filled out accordingly". That clause qualifies the "at least one" stated four lines later.

### F8 (MEDIUM). C-43 drops the self-modification constraint and asserts an effect that does not occur
- P:331-333: "SessionStart runs `scripts/fix_stop_hook_loop.sh` silently to add that exclusion to the hook; whether it took: `grep -c …`".
- Verified in this container: settings.json SessionStart[1] runs the script; `~/.claude/stop-hook-git-check.sh.bak` is identical to the hook; `grep -c stophook.ignorePath` prints 0; `git config --get-all stophook.ignorePath` exits 1. The script stops at its `assert` (set -e) before the git-config step.
- C:482-483 "**An agent cannot apply it:** the harness classifier blocks it as self-modification" is still true of an agent. The script's own header says so: "editing ~/.claude/ is refused here as self-modification, which is the right refusal".
- The proposal gives a probe with no action. A session that sees 0 has nothing telling it not to patch `~/.claude` by hand. The harm the audit found (the patch fails) did not reach the replacement text (S1).

### F9 (MEDIUM-LOW). C-25 writes an unratified reading as the rule
- Owner, ledger :8270-8272: "permission to hand edit as required for specific columns"; "many qualitative judgments/corrections".
- "qualitative judgment or wording cell" (P:224) takes "wording" from the reading at :8275, which ACTION (3) says to treat as unratified.
- Rule 10 (P:160-161) still says "never patched with hand SQL inside the batch's data migration", and the exception does not name it.
- The ACTION (1) record places (migration header, gap resolution) and the ACTION (2) "ask" are carried faithfully.

### F10 (MEDIUM-LOW). Rule 4's sweep list is a curated list
- P:96-97 lists six directories. It omits `workplan/` (the atoms and machines of F2) and `decisions/`.
- Rule 8 ("never from a list kept beside the thing it describes") would require the whole tree.

### F11 (LOW). C-38 swaps the content-search technique for a file-listing tool
- C:425 "A `glob` that names the directory (`references/**`, `sessions/**`) overrides `.ignore`": the Grep tool's parameter. Verified: Grep with `glob: sessions/**` returns a hit in `sessions/session_2026-08-25-…md`; without it, the hit is absent.
- P:305 says "a Glob", which per `.ignore`'s header ignores `.ignore` but only lists names.

### F12 (LOW). C-39 narrows "one action" and drops the hook
- C:443-444: "rename the folder in the SAME action that changes `CURRENT`" (always). P:310 says it only for "If your PR merges mid-session".
- `.claude/commands/session-open.md:35` cites "change both in one action (CLAUDE.md section 7)".
- The hook (`record-command.py` `open_session()`) and the misfile remedy (find by `session_id`, move by hand) are gone. session-open.md carries the hook; nothing carries the remedy.

### F13 (LOW). C-29's "Breaks: none" is false
- `git grep -n -E 'CLAUDE\.md.{0,30}(probe|snippet|derivation below|UNWRITABLE)'` (the audit's own command) prints `architecture/meta-scripts-spec.md:305` and `architecture/conformance-schema-findings.md:117`, both "The CLAUDE.md §4 snippet".

### F14 (LOW). C-35's subject narrowing
- DR-2026-06-10 Consequences: the floor covered "cell-state and convergence authoring".
- P:284-285 binds it to `specifications` only, a mapping from T-120 item 3 (a delegated task, not owner words).
- The SessionStart contract still says "Never author best_practice_synthesis below the Opus floor", so each session gets two names for one floor.
- Floor class and the no-version requirement: SURVIVE (ledger :606-609; decision-protocol §4.2 "`fable` is a synthesis-capable tier alongside `opus`").

### F15 (LOW). C-17 misses a live instance
- `db.py add-supersession-check --tier` is `required=True` (db.py:3548) and stores a referenced source's tier and evidence type unchecked (`add_supersession_check`).
- Registry notes with hand figures still exist, for example `note: ~27s` on the check before `test_state_graph_instrument`. The deleted rule-8 sentence was the only pointer at that shape.

### F16 (LOW). Rule 7 against the proposal itself
- P:365 "Single author, pre-launch." is a project-state claim, kept while "the content is barely started" is deleted as volatile.
- "the three lenses" (P:376) is a count that already changed on 2026-11-16 (four to three).
- "TWO TRACKED FILES" (P:328) and "One refusal is deliberately absent" (P:229) are counts with no command.

### F17 (LOW). The audit's own figure
- "Words in OWNER-ONLY verbatim blocks: about 800" and "the OWNER-ONLY text alone is more than half of it".
- Measured over the blocks it names: 699 against a target of 1452 (48 per cent). Command in section 6.

### F18 (LOW). C-42 against the owner's words
- "strip out … version discussion": the PI-version trap is expanded (P:324-326) and the PI files are listed again in P:382.

### F19 (LOW). C-37
- The proxy-status diagnostic (C:420-421, `/__agentproxy/status`'s `recentRelayFailures`) is the command that tells a proxy failure from a dead snapshot. It is deleted; only the control-URL test remains.

### F20 (LOW). C-26's reason
- "Two refusals are deliberately absent": the second absent thing is the `--year`/`--journal` CLI flags (db.py `insert_economics_entry`: "through argparse it is unreachable, and that is the point … Do not "fix" it by adding the flags"). The sentence was not self-contradictory. The constraint survives at its code home, so the deletion is tolerable.

## 3. Brief items answered

1. **Rule loss.** See LOST RULES. Rule 3, the migration path, rule 5's column-drop condition, rule 6, rule 10, the Wayback procedure, the session-id and git-rebase traps, §5(c) and the "search both halves" warning are all present. The UNWRITABLE probe moved to db-census.md, which holds it byte-for-byte apart from the connect line.
2. **Owner-text fidelity.** Byte-identical: the goal sentence, the simplicity sentence, the three things, the authority sentence, rule 0 (C:79-86), rule 9 (C:196-210), the layer quote (C:232-239), the tier line (C:367-370), the marker line, the Co-1 warrant and the doctrine paragraph. Method: `python3 scratchpad/a3/fid.py`. The spine block differs only by C-21's deletion of the owner formulation. Byte-identity of the marker line is substantively wrong (F3).
3. **Pinned text.**
   - claude_md_spine logic emulated: one SPINE line, equal to the contract. PASS.
   - T126-30 regex finds tier 4 in both files. PASS.
   - retired_vocabulary scan emulated: no hit in either file.
   - Numbering callers (`git grep … CLAUDE\.md[^a-z]*(rule|section|§)`; 369 non-migration lines): no rule or section number disappears. The content breaks are F2, F6, F12 and F13.
4. **The four "false today" claims.**
   - preflight and the selftest: TRUE, and the replacement is accurate.
   - The --tier examples: TRUE, but the replacement loses a live target (F15).
   - The model floor: TRUE (the current text is narrower than the owner's words). The replacement agrees and does not re-pin (F14 low).
   - The stop hook: half true. The replacement is defective (F8).
5. **Added text.** The hand-correction sentence is substantially accurate (F9). The "What to do now" pointer conflicts with the DR's self-precedence and with orient.md, and the proposal does not name it (F4).
6. **Rule 7a.**
   - `wc -w`: 5809 current, 4040 proposed. Both match the audit.
   - Target 1452; the proposal is 2.8 times it (the target is unratified).
   - Volatile facts: F16. Owner-locator dates are fixed and acceptable.
7. **Findability.**
   - Lines 1-35 of the proposal give: the goal; simplicity; fetch-before-write; translations; Co-1; doctrine; DR-2026-08-19 as senior authority (a spent plan, F4); the correction rule. Line 38 gives `/orient` and `/session-open` timing.
   - Not on the first screen: never write the database directly (P:89), the read-only open (P:212-215), rule 0 (P:70), the `.ignore` blindness (P:304).
   - All 34 path pointers resolve (`git ls-files --error-unmatch`, scratch loop); `icf-glossary` exists.
8. **Owner-only list.**
   - O-06 and O-05 are settled by owner words, or a ratified rule, and need only confirmation.
   - O-01 and O-02 are arguably settled by the owner's 2026-11-26 instruction (transcript main.jsonl, uuid 9c1f9e86): "strip out all extraneous stuff like change logs".
   - Owner-only items wrongly classed DELEGABLE: C-23 (owner-ruled), C-46's history list (DG-NON), and C-46's "What to do now" row (coupled to O-07 and orient.md).

## 4. LOST RULES (constraint, enforcement note or command missing or weakened)

1. C:466-468 / CLAUDE §3 convention: not lost; wrongly retained in effect (F1).
2. C:386-388: the lens scope "any table attaching a determination to a group of disabled people" and "one CHECK" (F7). Proof: P:289-291.
3. C:505: "Nothing is added without naming what reads it." (F6). Proof: `grep -c -i 'nothing is added without naming' scratchpad/CLAUDE.proposed.md` prints 0.
4. C:482-483: "An agent cannot apply it: the harness classifier blocks it as self-modification" (F8). Proof: P:331-333.
5. C:443-444: rename the folder in the same action whenever `CURRENT` changes (not only on merge), plus the `record-command.py` `open_session()` mechanism (F12).
6. C:425: the Grep `glob` technique for seeing through `.ignore` (F11).
7. C:192-195: read the registry `note:`/`floor_basis:`/`no_floor:` fields for literal figures, with its grep (F15).
8. C:420-421: the `/__agentproxy/status` `recentRelayFailures` diagnostic (F19).
9. C:264-265: "every assignment written before 2026-08-27 predates them" (C-22).
10. C:45-46: `python3 scripts/run_checks.py --selftest # AFTER ANY RENAME`. Its timing is weakened to "once, at PR time" through preflight. Low.
11. C:51-52: `--all --battery <name>` runs the whole battery. That command is gone. Low.
12. C:240-241: `layer-N` in a frozen record is the retired map's bucketing, not the owner's layers. Low.
13. C:401-402: the reason behind "search for both halves" (a search stops at the first answer). The imperative is kept; low.
[NULL: rule 3, the write path, rule 5's column-drop condition (`AFTER_DATA` verified in migrate_db.py:282), rule 6, rule 10's imperatives and enforcement, the session-id trap, the git-rebase trap, the SessionStart APPEND trap, §5(a), §5(c) mechanism and committed-artefact clause — examined, nothing lost.]

## 5. CORRECTIONS (restorations and authorities only)

- **F1 (C-23).** Delete P:201's sentence "Every stage points into `base`, so a view reading one stage plus `base` is not counted as crossing." Any replacement must agree with DR-2026-08-27:28 ("the view that joins it is v_coverage_priority (base+research)") and with the 2026-08-27 ACTION (4) "`v_coverage_priority` is protected".
- **F2.** The same pull request must leave `python3 workplan/pipeline-state-graph/build_graph.py --check` at its main-branch failure set (PIP-01 only). Each of CLM-012, 015, 023, 024, 028, 029, 039, 042, 043 and 046, and needle M10.t1, either keeps its quoted CLAUDE.md text or is re-quoted in that pull request (T-120 item 6 is the precedent).
- **F3 (marker line).** The authority is ledger :7265 as answered at :7327: "● T1, T2, Co-1, Co-2; ◐ T3, T4; ○ T5, T6; ⚠ in place of the circle for a grey, unverified or thin basis".
- **F6.** Restore, verbatim: "**Nothing is added without naming what reads it.**". The owner-sign-off sentence must not read §2.4 as exhaustive while `.ignore` (owner-gated) and the ledger :8204 reservations exist.
- **F7.** Restore: "any table attaching a determination to a group of disabled people takes three lens columns (identity, ICF, access need), one CHECK, real FKs". This is the current text less the medical lens.
- **F8.** Restore: "**An agent cannot apply it:** the harness classifier blocks it as self-modification".
- **F11.** Restore: "A `glob` that names the directory (`references/**`, `sessions/**`) overrides `.ignore` and returns them."
- **F12.** Restore: "rename the folder in the SAME action that changes `CURRENT`", and the hook name "`.claude/hooks/record-command.py`'s `open_session()`".
- **F13.** C-29's "Breaks" line must name `architecture/meta-scripts-spec.md:305` and `architecture/conformance-schema-findings.md:117`.
- **C-13.** Restore: "**A parity check is not a fix** — it makes a dual home survivable, therefore permanent."
- **F19.** Restore: "confirmed session-level … via `/__agentproxy/status`'s `recentRelayFailures`".
- **F9 (C-25).** The authority is the owner's "specific columns" and "qualitative judgments/corrections". "wording" is the recorder's [ASSUMPTION] (:8275).

## 6. Commands (re-run; figures are not to be trusted)

- `wc -w scratchpad/CLAUDE.proposed.md; git show HEAD:CLAUDE.md | wc -w`
- `f=scratchpad/a3/current.md; for r in 5,6 8,8 10,18 79,86 196,210 232,239 367,370 372,372 375,376; do sed -n "${r}p" $f; done | wc -w`
- `python3 scratchpad/a3/fid.py` (owner blocks)
- `python3 -I scratchpad/a3/bg_emul.py <file>` (state-graph check with CLAUDE.md overridden)
- `python3 -I scratchpad/a3/mlq.py` (multi-line quoted-phrase sweep)

## 7. APPROVAL LIST for the owner (smallest change first)

| # | Change | Class | Confidence |
|---|---|---|---|
| 1 | Marker line to the OD-57 table (F3, O-06). Content already answered "yes"; only the timing with T-120 item 2a remains | Settled by owner words; owner confirms timing | High |
| 2 | Tier line: T3 "lower-control primary (clinical or grey)", Co-2 "co-primary with T2" (O-05), keeping the literal "**T4–T6** the regulatory stratum" | Owner-only; content matches ratified RULE :17 | High |
| 3 | Delete the Proof narratives of rule 0 and rule 9 (O-01, O-02); imperatives untouched | Owner-only; arguably settled by the 2026-11-26 "strip out … change logs" | Medium-high |
| 4 | Remove the base+one-stage exemption (F1, C-23) | Owner-ruled already (2026-08-27); needs the record, not a new decision | High |
| 5 | Rule 9 enforcement sentence (O-03) | Owner-only | High that it is stale; medium on the replacement ([UNVERIFIED] name matching) |
| 6 | §9 "What to do now", the authority sentence and orient.md:25, decided together (C-46, O-07, F4) | Owner-only (precedence over a ratified instrument) | Medium |
| 7 | Whether conceptual-model.md and functional-taxonomy.md are "history" (C-46, F5) | Owner-only (DG-NON §2.4) | Medium |
| 8 | Whether "wording" cells are "qualitative" for hand fixes (C-25, F9) | Owner-only (the ledger says "ask") | Medium |
| 9 | settings.json deny names (O-04) | Owner applies | Medium |
| 10 | Layer model kept or moved (O-08) | Owner-only | n/a |
| 11 | Working-rules file and size target (O-09) | Owner-only | n/a |

## 8. Not verified or not reached

- [UNVERIFIED] The MCP tool names this harness exposes (O-03, O-04). This agent's tool list does not show them.
- [UNVERIFIED] `preflight.sh --explain` end to end. It was read, not run; no suites were run.
- [UNVERIFIED] Whether the stop-hook patch fails in other containers. Verified here only.
- [UNVERIFIED] Whether the 2026-11-14 owner rulings also make the tier line's "walled off from full-strength anchoring" stale. T-120 says a code value was made eligible; not traced.
- `git rebase` blocking was not tested, deliberately: it would mutate the repository. `scripts/bootstrap.sh`'s PAT gate is verified (line 17).
- The 369 numbering-caller lines were swept for removed sections and quoted phrases mechanically, not read one by one.
- `.claude/README.md` and the restatements of the write path in other files were not audited.

## Summary

All the owner-reserved text is byte-identical, the SPINE and T4–T6 pins pass, no retired token is added, and every §9 path resolves. Three of the four "false today" claims hold.

The proposal still fails in three ways:
- **It keeps an exemption the owner ended.** C-23 retains the dead "base is not a stage" exemption, which contradicts the owner's ruling of 2026-08-27 and has already licensed one dropped view.
- **It breaks a caller the audit missed.** The audit says two scripts read CLAUDE.md; a third, the state-graph instrument, goes from 1 failure to 12 and is in no gate.
- **It keeps superseded or unresolved text.**
  - The marker line the owner replaced (OD-57 "yes") stays.
  - The new "What to do now" row loses to the DR-precedence sentence the proposal keeps, and `/orient` points back to the DR.
  - It reclassifies owner-ratified taxonomy doctrine as history on its own authority.

Lesser defects: dropped constraints (the lens scope, "Nothing is added…", the self-modification limit, the Grep `glob` technique, "one action"), an unratified reading written as a rule, and a curated sweep list.

File: /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/antagonist-3.md
