# Decision prompts for items C and D (2026-11-26)

Written read-only against the repository at commit `921b335` (governance content identical to `origin/main` `71b7c58`) and `data/guidebook.db` opened `mode=ro`. Nothing here is applied.

**How to answer.** Each item ends with a recommended answer. You can reply in one line (for example "C4 A; C1 a; D3 moot"), or paste the item's PROMPT block into a fresh Opus session. Each prompt stands on its own.

**Line numbers** are as at `921b335`. The approved A and B edits are being applied to the working tree now, so CLAUDE.md lines after 270 have moved up by one or more. Locate every line by its quoted text, never by number.

**Counts.** No figure here is to be trusted as typed. Where a number matters, the command that derives it is given beside it.

## Terms used throughout

- **The ledger**: `references/project-standards.md`, the append-only record of owner rulings. An entry whose heading begins "Owner" quotes your typed words. Text marked `[ASSUMPTION: …]` in an entry is the recorder's reading, not your words. Every such entry's ACTION says to treat those readings as unratified (`grep -c "unratified except where the owner's words state" references/project-standards.md`).
- **Owner words, how to find them**: `git grep -n -F '<quote>' -- references/project-standards.md`. The Grep tool cannot see `sessions/`, `_archived/` or `workplan/_superseded/`; `git grep` can.
- **Tiers**: T1 is primary controlled research. **Co-1** is lived-experience and participatory work by disabled people, co-primary with T1. T2 is synthesis (systematic reviews, evidence-based standards). **Co-2** is clinical practice guidelines from occupational-therapy professional bodies (CAOT, AOTA, RCOT and others). T3 is lower-control primary research, clinical or grey. T4 to T6 are the regulatory stratum: international standards, national frameworks and statutory codes.
- **Markers**: ● ◐ ○ and ⚠. The table you ruled on 2026-11-14 is: ● T1, T2, Co-1, Co-2; ◐ T3, T4; ○ T5, T6; ⚠ in place of the circle for a grey, unverified or thin basis.
- **OD-nn**: a numbered decision in the remediation plan's register (`workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md` §8). Its standing is the last `OD-nn STATUS:` line in the ledger.
- **Delegated resolution**: a ruling an Opus-class model made under one of your grants. It is recorded as `RESOLVED UNDER DELEGATION`, never as your answer.
- **DR**: a decision record in `decisions/`.
- **DG-NON**: the decisions only you may make. They are listed in `governance/decision-protocol.md` §2.4 (lines 71-84).
- **Rule 0** (CLAUDE.md:79): a live owner statement supersedes every earlier ratified record it touches, on contact.
- **Migration**: the only way the database changes. The path is scratch copy, then `scripts/db.py`, then `scripts/research/emit_batch_sql.py`, then `scripts/emit_data_migration.py`, then `scripts/migrate_db.py`.

## Findings from checking the record that change what you were told earlier

1. **A merge does count as ratification, on your own words.** The approval list (C4) and antagonist-1 said that no owner words support "merge counts as approval". That is wrong. Ledger :582-585 has a RULE dated 2026-07-24 on your words: "always assume I Ratify if I merge it unless I explicitly note otherwise". Its limit (4) is that a merge "does not manufacture a decision the owner never made" on a DG-NON matter. C4 and D4 below use that rule.
2. **Ledger :8209 is not your words.** That line reads "The owner approves the goal sentence, rule 0, rule 9, the tier and Co-1 definitions, and the fate of the layer model". It is part of the coordinator's record of a rewrite proposal. The entry's DATE line (:8215) says "the rewrite content is the coordinator's record of the audits, not an owner statement", and ACTION (3) (:8214) marks it unratified. Where an item below is owner-only, the warrant given is decision-protocol §2.4 or prudence, not that line.
3. **Part of approved item B2 was held back for C4.** The implementer did not change the "What to do now" row (CLAUDE.md:538) or `.claude/commands/orient.md:25`, because the brief held those back until C4 is decided. The same log skipped the §8 sign-off pointer as content, not a pointer fix (`scratchpad/impl-X.md`, B2). C4 carries the routing change.
4. **B6 moved a line that the pipeline contract cites by number.** It inserted a header line into `governance/conceptual-model.md`, so the paragraph `governance/pipeline-contract.yaml:286` cites as `conceptual-model.md:90` is now at :91 (`scratchpad/impl-Z.md`). C6 folds in the fix.
5. **C8 is part of C4,** and its prompt is merged into C4's. C1, C2 and C7(b) edit the same tier lines and can run as one session.
6. **The command log is going to the wrong folder (housekeeping, not a C or D item).** `scratchpad/CURRENT` holds `session_2026-11-22-icf-umbrella-glossary`, a past session's folder, so this session's commands are being appended there (CLAUDE.md §7 trap).

---

## C4 One order of authority (C8 merged)   [class: OWNER-ONLY]

**CONTEXT.**
You rejected the drafted order. You then typed (2026-11-26, 22:26 UTC): "C4 actually does point towards there needing to be one order of authority? why would we want multiple authorities". Find it with `grep -c -F 'why would we want multiple authorities' transcripts/harness_f8d4d6c2/main.jsonl`; the transcript holding it is not yet committed.

Today several documents each claim to say which text wins:

| # | Statement | Where | Owner words? |
|---|---|---|---|
| 1 | "A live owner statement supersedes every prior ratified record it touches, on contact … never weigh the ruling against the paperwork it changes" | CLAUDE.md:79-86 (rule 0) | CLAUDE.md text, ratified by your merges (ledger :582-585). No verbatim owner quote of it was found |
| 2 | "Where it disagrees with `decisions/DR-2026-08-19-…`, that instrument wins and this file is what to correct — unless a live owner ruling has superseded the instrument itself, per rule 0" | CLAUDE.md:21-23 | CLAUDE.md text |
| 3 | "THIS DOCUMENT SUPERSEDES ALL OTHER PLANNING DOCUMENTS … the only planning artifact a session needs to read … binding on nothing" | DR-2026-08-19:3-6 | DR, ratified by you 2026-08-19 (DR :89-92, OD-1) |
| 4 | CLAUDE.md is "a reference, not an instruction set. Where it disagrees with this instrument, this instrument wins … Everything else is superseded." | DR :17-25 (§A) | same DR |
| 5 | "A fresh session reads exactly four … No fifth document may join this set." | DR :561-578 (§8) | same DR; two of the four are marked SPENT or HISTORY in the same list |
| 6 | The successor-plan ban is "SPENT … A successor plan is no longer build-rejected" | DR :636-641 (§11 property 3) | same DR; this undercuts rows 3-5 |
| 7 | DG-NON means "The project owner alone"; the §2.4 list of owner-only decisions | `governance/decision-protocol.md`:47, :71-84 | ratified doctrine. It says who decides, not which text wins |
| 8 | "as always refer to doctrine/mission/claude.md etc for guidance as required" | ledger :8485 | **your words**, 2026-11-25. They name doctrine and CLAUDE.md together, unranked |
| 9 | "A delegate rules against the doctrine and rules the owner has recorded (`governance/mission-and-epistemics.md`, `CLAUDE.md`, `governance/tier-system.md`, `governance/decision-protocol.md`, the ledger)" | ledger :8496, ACTION (4) | recorder's ACTION applying row 8 |
| 10 | OD-79: the grant does not reach population taxonomy, "what the owner meant by the owner's own words", or "a row the schema binds to an 'Owner' ledger entry" | ledger :8503 | delegated resolution, check confirmed |
| 11 | "always assume I Ratify if I merge it unless I explicitly note otherwise" | ledger :582-585 | **your words**, 2026-07-24, with limit (4): DG-NON substance needs your direction |
| 12 | "fold plan into remediation plan and ensure they are commensurate with this newest plan having priority in conflicts" | ledger :7247 | **your words**, 2026-11-14, about two plans |
| 13 | Gate convention: a task needing your own words opens only on `ANSWERED BY THE OWNER` | ledger :5724-5746 | recorder: "a convention for reading the ledger, not an owner ruling" |
| 14 | "What to do now" goes to the DR | CLAUDE.md:538; `.claude/commands/orient.md`:25 | CLAUDE.md and command text |

**Three different answers to "what to do now" exist today:**
1. The DR: CLAUDE.md:538, orient.md:25, DR :3-4, and DR §A :13 ("§A → §3 → §12 (the runbook) → run it"). But DR §12.1 is marked "SUPERSEDED 2026-09-10" (DR :778).
2. `/orient` plus the ledger tail: CLAUDE.md:539 and orient.md item 2.
3. The remediation plan. You typed "i just want to get this remediation plan done asap" (ledger :8483). That it means `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md` is the recorder's [ASSUMPTION] (:8487). You had also named "remediation plan" on 2026-11-14 (:7247).

**Why the earlier draft failed.** It ranked delegated resolutions above doctrine and CLAUDE.md, which contradicts row 8. It wrote a recorder reading into decision-protocol §2.4 as an exception. It added a DR note listing which DR sections "still bind", which is an agent re-ratifying a DG-NON record (DR :87-88). The parts that survive the critique are the evidence and the repair of the "what to do now" route.

**The proposed single order (Order A).** It would replace CLAUDE.md:21-23's second sentence:

> **Order of authority, highest first.**
> 1. **The owner's words**, typed live or quoted verbatim in `references/project-standards.md`. A later statement supersedes every earlier record it touches, on contact (rule 0). A recorder's `[ASSUMPTION]` reading, an ACTION line and a model's summary are not the owner's words. The owner's merge of a pull request ratifies what it carries unless the owner says otherwise. A merge never supplies a decision that `governance/decision-protocol.md` §2.4 reserves and the owner has not given in words.
> 2. **Ratified records**: the doctrine in `governance/` (mission, tier system, decision protocol and the other files marked ratified, canonical or operative), the ledger's RULE entries, the decision records in `decisions/`, and this file, each as amended by later owner words. Where two disagree on a point, the later ratification governs and the older text is corrected. Where that cannot be told, ask the owner.
> 3. **Delegated resolutions** (`RESOLVED UNDER DELEGATION`, check confirmed). They are made against rank 2, within the grant's recorded reach. They never decide what §2.4 reserves and never stand in for an `Owner` ledger entry the schema requires.
> 4. **Plans, task files, conventions and skills** bind only as they apply ranks 1-3. Between plans, the newer governs. The active plan is the one the newest ledger entries name.
> 5. **Frozen records** (`sessions/`, `transcripts/`, `_archived/`, `workplan/_superseded/`, the `decisions` table) are evidence of what was said and when. They bind nothing beyond the owner words they quote.

What each clause rests on:

| Clause | Rests on | Owner words, or a reading? |
|---|---|---|
| One order, not several | "why would we want multiple authorities" (2026-11-26) | owner words |
| 1: owner words first; later supersedes | rule 0 (row 1); applied in every owner-era ledger entry | CLAUDE.md text ratified by merge; no verbatim quote |
| 1: readings and ACTIONs are not owner words | the ACTION in each owner entry ("Treat the readings above as unratified …") | recorder text, consistent practice |
| 1: a merge ratifies, but not DG-NON substance | ledger :582-585, limit (4) | **owner words** (2026-07-24) |
| 2: doctrine and CLAUDE.md at one rank | "refer to doctrine/mission/claude.md etc" (row 8) | **owner words**; they name the two together, unranked |
| 2: the later ratification wins on a point | rule 0 extended from owner statements to ratified records; row 12 states it for plans only | **[UNRATIFIED READING]** |
| 2: ask when it cannot be told | — | **[UNRATIFIED READING]** |
| 3: delegated below rank 2 | rows 8, 9, 10; decision-protocol §2.1 (DG-NON = owner alone) | owner words plus ratified doctrine |
| 3: never in place of a schema-bound Owner entry | OD-79; the guard in `scripts/db.py` (`_owner_approval`) | delegated resolution plus code |
| 4: a newer plan governs | "this newest plan having priority in conflicts" (row 12) | owner words for one fold; **generalizing to all plans is a reading** |
| 4: the ledger names the active plan | CLAUDE.md rule 7 ("Derive … the active plan … from the live repo") | CLAUDE.md text |
| 5: frozen records bind nothing | DR :5-6 ("readable for provenance, binding on nothing"); R30 froze the `decisions` table (`workplan/pipeline-state-graph/RULINGS.md`:72) | ratified DR plus delegated ruling |

What Order A replaces or deletes:
- **CLAUDE.md:21-23**: the "that instrument wins" sentence is replaced. The first sentence ("This file holds process, workflow and rules only …") stays.
- **DR :3-6, :17-25, :13, :561-578**: not edited. One dated pointer note is appended at the top of the DR (this was C8). The text is under IF APPROVED. It lists no "sections that still bind". Rules the DR made that still apply are applied where they now live: the ledger, and CLAUDE.md §4's write path. [UNVERIFIED: that every live DR rule has another home. The prompt asks the session to list any that does not, not to declare it binding.]
- **CLAUDE.md:538-539**: the two rows merge into one: "What to do now, latest rulings | `/orient`; then the tail of `references/project-standards.md`, whose newest entries name the active plan". This was B2's held-back half.
- **orient.md:25**: the DR line is deleted. Item 2 gains "and the plan they name".
- **decision-protocol.md**: unchanged. It says who decides; the order says which text wins.

**Settled answer to "what to do now".** Run `/orient` for the live state, then read the newest ledger entries; they name the active plan. Today those entries name the remediation plan (:8471 heading; :8535 "Part C"). CLAUDE.md names no plan file, because the active plan is a volatile fact (rule 7).

**DECISION NEEDED.** Adopt Order A as the project's one order of authority, with the DR note, the §9 row and `/orient` pointing to it?

**OPTIONS.**
- **(A) Order A, as above.** Edits CLAUDE.md (one paragraph and one table row), orient.md (one line), the DR (one appended note, plus its attestation file) and the ledger (one entry). Reversible: these are text edits, and the DR note is appended, not a rewrite. It ends the DR's claim to outrank CLAUDE.md, and the three "what to do now" answers become one.
- **(B) A fixed ranking by document type:** owner words > `governance/` doctrine > ledger RULEs > DRs > CLAUDE.md > delegated resolutions > plans > frozen records. It is predictable. But no owner words rank doctrine above CLAUDE.md (row 8 names them together). Without "later wins", an old doctrine sentence beats a newer CLAUDE.md correction until someone edits the doctrine. It needs the same file edits as A.
- **(C) Keep CLAUDE.md:21-23 (the DR outranks CLAUDE.md) and add ranks 3-5 under it.** This is the smallest text change. But a plan that is spent by its own §11 stays the senior document, `/orient` keeps routing to it, and two statements of authority remain (the DR's and CLAUDE.md's).

**RECOMMENDATION.** (A). Every rank-to-rank placement except the "later ratification wins" tie-break rests on your words or on ratified text, and that tie-break is marked as a reading for you to accept or strike. Confidence: medium-high. Choose B instead if you want doctrine files always to beat CLAUDE.md regardless of date. Choose C if you want DR-2026-08-19 to stay senior.

**IF APPROVED, I WILL:**
1. **Ledger.** Append an entry "Owner statements 2026-11-26 — one order of authority …". It quotes "C4 actually does point towards there needing to be one order of authority? why would we want multiple authorities" and your answer word. It marks the two readings (the later-ratification tie-break; generalizing "newest plan") as [ASSUMPTION]. CONDITION is any session deciding which text governs. ACTION says to apply the order in CLAUDE.md.
2. **CLAUDE.md.** Replace the sentence beginning "Where it disagrees with `decisions/DR-2026-08-19-…`" with the Order A block. Merge the §9 "What to do now" and "Latest rulings" rows as above.
3. **`.claude/commands/orient.md`.** Delete item 1 ("`decisions/DR-2026-08-19-…` — what to do now"). Item 2 becomes "the tail of `references/project-standards.md` — the latest owner rulings, which supersede every ratified record they touch on contact (rule 0), and the active plan they name".
4. **The DR.** Append this note directly under the title, and update `attestations/decisions_DR-2026-08-19-research-restart-operative-instrument.json` against `schemas/attestation.schema.json` (rule 2):
   > **Read with CLAUDE.md's order of authority (owner, 2026-11-26).** This instrument's claims to supersede all planning documents (header), to outrank CLAUDE.md (§A), its §A routing, its §3 "next act" and its §8 read-set are history. §11 property 3 records the successor ban as spent, §12.1 is marked superseded (2026-09-10), and the owner has since named "this remediation plan" as the work (ledger, 2026-11-14 and 2026-11-25). The active plan is the one the newest ledger entries name. This DR's OD-1 to OD-12 are numbered apart from the remediation register's OD-01 onward; cite them as "DR-2026-08-19 OD-n".
5. **Atoms that quote the old text.** Re-quote or mark the state-graph atoms `CLM-002` (`workplan/pipeline-state-graph/atoms/atoms-claude.jsonl`) and `OPI-003` (`atoms-opi.jsonl`, `ATOMS.tsv`). Then run `python3 workplan/pipeline-state-graph/build_graph.py --check` and confirm no new failure beyond those present on main.
6. **Prose callers.** Sweep with `git grep -n -F -e "that instrument wins" -e "this instrument wins" -e "what to do now" -- . ':(exclude)scratchpad' ':(exclude)transcripts' ':(exclude)sessions'`.
7. **Shipping.** One governance pull request with no research rows (rule 10). Open it last, and unsubscribe from it at once (rule 9).

**PROMPT (copy-paste ready):**
```
Task: write ONE order of authority for the guidebook repository and point every competing statement at it. The owner approved option A (below) on <date>; their words: "C4 actually does point towards there needing to be one order of authority? why would we want multiple authorities" (2026-11-26) and "<answer word>".

Background: several texts each say which document wins. CLAUDE.md lines 21-23 say DR-2026-08-19 wins over CLAUDE.md unless a live owner ruling supersedes it. DR-2026-08-19 (decisions/DR-2026-08-19-research-restart-operative-instrument.md) says at lines 3-6 that it supersedes all planning documents, at §A (lines 17-25) that it beats CLAUDE.md, and at §8 that a session reads exactly four documents. Its own §11 property 3 (lines 636-641) says the successor ban is spent, and §12.1 is marked superseded. CLAUDE.md §9 row "What to do now" and .claude/commands/orient.md item 1 both send sessions to the DR. The owner's 2026-11-25 words "as always refer to doctrine/mission/claude.md etc for guidance as required" (ledger, git grep -n -F "as always refer to doctrine" -- references/project-standards.md) name doctrine and CLAUDE.md together. The owner's 2026-07-24 RULE (git grep -n -F "always assume I Ratify if I merge it" -- references/project-standards.md) makes a merge a ratification unless noted, but not for DG-NON substance. The owner's 2026-11-14 words "this newest plan having priority in conflicts" concern plans. OD-79 (ledger, "Delegated resolutions 2026-11-25") limits delegated rulings.

Do, in this order:
1. Verify each quotation above with git grep before using it; if any differs, stop and report.
2. Append to references/project-standards.md an entry headed "Owner statements 2026-11-26 — one order of authority; DR-2026-08-19 is not the plan". Quote the owner's words verbatim. Mark as [ASSUMPTION] the tie-break "the later ratification governs on a point" and the generalization of "newest plan" to all plans. Add CONDITION, ACTION, DATE lines in the ledger's existing style.
3. In CLAUDE.md, replace only the sentence that begins "Where it disagrees with `decisions/DR-2026-08-19-" with this block, verbatim:
   Order of authority, highest first. (1) The owner's words, typed live or quoted verbatim in references/project-standards.md; a later statement supersedes every earlier record it touches, on contact (rule 0). A recorder's [ASSUMPTION] reading, an ACTION line and a model's summary are not the owner's words. The owner's merge of a pull request ratifies what it carries unless the owner says otherwise, and never supplies a decision governance/decision-protocol.md §2.4 reserves that the owner has not given in words. (2) Ratified records: the doctrine in governance/ (mission, tier system, decision protocol and the files marked ratified, canonical or operative), the ledger's RULE entries, decision records in decisions/, and this file, each as amended by later owner words; where two disagree on a point, the later ratification governs and the older text is corrected; where that cannot be told, ask the owner. (3) Delegated resolutions (RESOLVED UNDER DELEGATION, check confirmed), made against rank 2 and within the grant's recorded reach; never a decision §2.4 reserves, never in place of an Owner ledger entry the schema requires. (4) Plans, task files, conventions and skills bind only as they apply ranks 1-3; between plans the newer governs; the active plan is the one the newest ledger entries name. (5) Frozen records (sessions/, transcripts/, _archived/, workplan/_superseded/, the decisions table) are evidence of what was said and when, and bind nothing beyond the owner words they quote.
   Format it as a numbered list in the file's style. Keep the preceding sentence "This file holds process, workflow and rules only; …" unchanged.
4. In CLAUDE.md §9, merge the rows "What to do now" and "Latest rulings" into: | What to do now, latest rulings | `/orient`; then the tail of `references/project-standards.md`, whose newest entries name the active plan |
5. In .claude/commands/orient.md, delete the item naming DR-2026-08-19 as "what to do now". Renumber, and add "and the active plan they name" to the ledger-tail item.
6. Append directly under the DR's title a blockquote note, exactly: "Read with CLAUDE.md's order of authority (owner, 2026-11-26). This instrument's claims to supersede all planning documents (header), to outrank CLAUDE.md (§A), its §A routing, its §3 "next act" and its §8 read-set are history: §11 property 3 records the successor ban as spent, §12.1 is marked superseded (2026-09-10), and the owner has since named "this remediation plan" as the work (ledger, 2026-11-14 and 2026-11-25). The active plan is the one the newest ledger entries name. This DR's OD-1 to OD-12 are numbered apart from the remediation register's OD-01 onward; cite them as "DR-2026-08-19 OD-n"." Do NOT list DR sections that "still bind". Instead, report any DR rule you find that has no home in the ledger or CLAUDE.md. Update attestations/decisions_DR-2026-08-19-research-restart-operative-instrument.json so it validates against schemas/attestation.schema.json (CLAUDE.md rule 2).
7. Re-quote or mark atoms CLM-002 and OPI-003 under workplan/pipeline-state-graph/. Run `python3 workplan/pipeline-state-graph/build_graph.py --check` and confirm its failures equal those on origin/main.
8. Sweep prose callers: git grep -n -F -e "that instrument wins" -e "this instrument wins" -e "what to do now" -- . ':(exclude)scratchpad' ':(exclude)transcripts' ':(exclude)sessions'. Fix live pointers only.
Constraints: CLAUDE.md rule 0 (owner words supersede; record the supersession). Decision-protocol §2.4 decisions are the owner's only. Add no new machinery (no table, verb, check or script). No hand-typed counts (rules 7 and 7a): give the command instead. Do not touch data/guidebook.db. Edit with the Edit tool and locate lines by quoted text. Commit format: "governance: <action> [YYYY-MM-DD HH:MM]" with the time from date -u. Ship as a governance-only pull request (rule 10). Run scripts/preflight.sh once, at the end. Open the pull request last and unsubscribe from it immediately (rule 9).
Return: the diff summary (git diff --stat), each file:line changed with before and after quotes, any DR rule found with no other home, the build_graph result, and the PR link.
```

---

## C1 Co-2 is co-primary with T2   [class: OWNER-ONLY]

**CONTEXT.**
You typed on 2026-11-26 at 00:41 UTC: "Co-2 is co-primary with tier 2." Find it with `grep -c -F 'Co-2 is co-primary with tier 2.' transcripts/harness_f8d4d6c2/main.jsonl`. No ledger entry holds it yet.

The ledger already says the same. Its core RULE reads "Co-2 = OT professional body CPGs (co-primary with Tier 2)" (:17), and you said on 2026-11-14 "Co-1 stays full, Co-2 full too" (:6989), so both carry ●.

Several homes say "parallel" or leave it out:
- `governance/tier-system.md`:11 ("two parallel community-knowledge tracks")
- tier-system.md:17: the T2 row lists "occasionally `co2`", which files Co-2 inside T2
- tier-system.md:18: the Co-2 row has no co-primacy sentence, while Co-1's row (:16) has one
- `governance/mission-and-epistemics.md`:93 ("parallel to Tier 2")
- `governance/evidence-methodology.md`:49
- `schemas/enums.py`:30 and :109 (docstrings)
- `governance/owner-browser.yaml`:107 (no co-primacy)
- CLAUDE.md:369 (Co-1 is marked co-primary; Co-2 is not)
- `governance/decision-protocol.md`:77, where the owner-only list reads "Evidence-tier definitions (1–6 + Co-1)", so Co-2 is left out

`governance/evidence-architecture.md`:42 already says "co-primary with T2". Elsewhere the files use "parallel" and "co-primary" as synonyms (`governance/co1-operational.md`:56; evidence-methodology.md:30).

Nothing in the code depends on the wording. `schemas/tier_derivation.py`:62 maps `co2` to tier 2. The database holds no Co-2 sources today (`select count(*) from evidence_sources where evidence_type='co2'`).

One question is left open on purpose. OR-6c treats a Co-1 against T1 divergence as same-rank. Whether a Co-2 against T2 divergence is the same is moot for choosing the best value: your 2026-11-14 harm test says tier does not decide which value is best.

**DECISION NEEDED.** Record your statement in the ledger and change every home to say Co-2 is co-primary with T2?

**OPTIONS.**
- **(a) Record and sweep.** One ledger entry, plus text edits in the homes listed (no code or data changes; docstrings only in `schemas/enums.py`). Reversible.
- **(b) Record only.** The ledger entry alone; homes keep "parallel". Decision-protocol keeps Co-2 off the owner-only list.
- **(c) Do nothing.** Ledger :17 already says it, but your 2026-11-26 words stay unrecorded and the omission in §2.4 stays.

**RECOMMENDATION.** (a). It matches a ratified RULE and your typed words, and it closes the §2.4 gap. Confidence: high. It would change only if "co-primary" was meant to alter how divergences are resolved; that question is left open, not applied.

**IF APPROVED, I WILL:**
1. **Ledger.** Append "Owner statement 2026-11-26 — Co-2 is co-primary with Tier 2", quoting your words. Readings: [ASSUMPTION] it restates RULE :17 and leaves the marker table unchanged; [ASSUMPTION, not applied] it implies nothing for OR-6c. ACTION: read Co-2 as co-primary with T2 and correct the passages named.
2. **CLAUDE.md:369.** "**Co-2** OT professional-body CPGs" becomes "**Co-2** OT professional-body CPGs, **co-primary with T2**". The literal "**T4–T6** the regulatory stratum" stays, because `scripts/tests/test_db_amend_writers.py` (T126-30) parses it.
3. **tier-system.md.** :11 "two parallel community-knowledge tracks (Co-1, Co-2)" becomes "two co-primary community-knowledge tracks (Co-1 beside T1, Co-2 beside T2)". At :17, delete "occasionally `co2` for community-of-professional synthesis". At :18, append "Co-2 ranks alongside T2."
4. **The other homes.** mission-and-epistemics.md:93, evidence-methodology.md:49 and the enums.py docstrings at :30 and :109: "parallel to Tier 2" becomes "co-primary with Tier 2". owner-browser.yaml:107: "Co-2 is occupational-therapy body guidelines" becomes "…, co-primary with T2". decision-protocol.md:77: "(1–6 + Co-1)" becomes "(1–6, Co-1 and Co-2)".
5. **mission-PROVISIONAL.md:64** is left alone; mission-and-epistemics.md:2 marks that file superseded.

**PROMPT (copy-paste ready):**
```
Task: record and apply the owner's statement "Co-2 is co-primary with tier 2." (typed 2026-11-26). Co-2 = occupational-therapy professional-body clinical practice guidelines; T2 = syntheses. The ledger's core RULE (references/project-standards.md line 17: "Co-2 = OT professional body CPGs (co-primary with Tier 2)") already says it; verify with git grep -n -F "co-primary with Tier 2" -- references/project-standards.md.
Do:
1. Append a ledger entry "Owner statement 2026-11-26 — Co-2 is co-primary with Tier 2". Quote the words. Mark as [ASSUMPTION] that it restates RULE 17, leaves the marker table unchanged (both ●), and implies nothing for OR-6c's divergence rule. Add CONDITION, ACTION and DATE lines in the ledger's style.
2. Derive the homes: git grep -n -i -E 'co-?2.{0,80}parallel|parallel.{0,40}tier 2|parallel community-knowledge' -- CLAUDE.md governance schemas. Also check CLAUDE.md §6's tier line, governance/owner-browser.yaml (term: tiers) and governance/decision-protocol.md §2.4 item 3. Change each to say Co-2 is co-primary with T2. In tier-system.md: delete "occasionally `co2` for community-of-professional synthesis" from the T2 row, and append "Co-2 ranks alongside T2." to the Co-2 row. In decision-protocol §2.4 item 3, change "(1–6 + Co-1)" to "(1–6, Co-1 and Co-2)". Leave governance/mission-PROVISIONAL.md (superseded) alone. In CLAUDE.md keep the literal "**T4–T6** the regulatory stratum" (a test parses it).
3. If C2 (T3 gloss) or C7(b) (typical evidence types) were also approved, make those edits in the same pass so each line is edited once.
Constraints: CLAUDE.md rule 0; decision-protocol §2.4 (tier definitions are the owner's; this edit applies the owner's words). No new machinery. No hand-typed counts. Do not touch data/guidebook.db. Edit tool only; locate by quoted text. schemas/enums.py: docstring text only. Governance-only pull request (rule 10). Run scripts/preflight.sh once at the end. Open the PR last and unsubscribe at once (rule 9).
Return: each file:line with before and after quotes, the ledger entry text, git diff --stat, the PR link.
```

---

## C2 The T3 gloss   [class: OWNER-ONLY]

**CONTEXT.**
`governance/tier-system.md`:19 defines T3 as "Clinical primary research at lower control level (cross-sectional, observational, qualitative, single-centre) plus grey-literature primary research". The code agrees: lower-control clinical research and grey literature both map to tier 3 (`schemas/tier_derivation.py`:57, :63). Your words of 2026-11-06 fit this: "if government report is academically sound then it can be t3 I think" (ledger :4928).

CLAUDE.md:369 calls T3 "grey primary". `governance/owner-browser.yaml`:107 says "T3 is grey primary work".

This matters for the markers. Under your table, non-grey T3 takes ◐ and a grey basis takes ⚠ (OD-57, ledger :7265 and :7327; "2 triangle for all", :7401). Calling all T3 "grey" invites ⚠ on lower-control clinical research.

Evidence-tier definitions are owner-only (decision-protocol.md:77). This edit brings the summary into line with the ratified definition; it does not change the definition.

**DECISION NEEDED.** Correct the T3 gloss in CLAUDE.md and owner-browser.yaml to "lower-control primary research (clinical or grey)"?

**OPTIONS.**
- **(a) Correct both glosses.** Two phrases; reversible.
- **(b) Replace CLAUDE.md's whole tier line with a pointer to tier-system.md §1.** One home (rule 5), but a larger edit, and the line must still contain "**T4–T6** the regulatory stratum" for the T126-30 test.
- **(c) Leave.** The summaries keep misstating T3.

**RECOMMENDATION.** (a). Confidence: high. Choose (b) if you prefer CLAUDE.md to carry no tier summary at all.

**IF APPROVED, I WILL:** In CLAUDE.md:369, change "**T3** grey primary" to "**T3** lower-control primary (clinical or grey)". In owner-browser.yaml:107, change "T3 is grey primary work" to "T3 is lower-control primary research, clinical or grey". If C1 is approved, make both changes in the same edit.

**PROMPT (copy-paste ready):**
```
Task: correct the T3 tier gloss. governance/tier-system.md §1 (T3 row) defines T3 as "Clinical primary research at lower control level … plus grey-literature primary research", and schemas/tier_derivation.py TIER_MAP maps both lower-control clinical and grey to tier 3. CLAUDE.md §6's tier line says "**T3** grey primary" and governance/owner-browser.yaml (term: tiers) says "T3 is grey primary work". The owner approved the correction on <date>.
Do: change CLAUDE.md's phrase to "**T3** lower-control primary (clinical or grey)" and owner-browser.yaml's to "T3 is lower-control primary research, clinical or grey". Keep the literal "**T4–T6** the regulatory stratum" in CLAUDE.md (scripts/tests/test_db_amend_writers.py parses it). If the Co-2 edit (C1) was approved too, edit the same line once.
Constraints: CLAUDE.md rule 0; decision-protocol §2.4 item 3 (tier definitions are the owner's; this matches the ratified definition, it does not change it). No new machinery; no hand-typed counts; do not touch the database; Edit tool; locate by quoted text. Governance-only PR; preflight once; open the PR last; unsubscribe at once.
Return: before and after quotes with file:line, git diff --stat.
```

---

## C3 Rule 9: the stale enforcement sentence and the deny-list names   [class: OWNER-ONLY]

**CONTEXT.**
Rule 9 (CLAUDE.md:196-212) says: do not watch pull requests, open the PR last, and unsubscribe immediately after creating it. It cites your instruction of 2026-09-23. That instruction is not quoted verbatim in the ledger (`git grep -n -i subscri -- references/project-standards.md` finds nothing); `workplan/2026-09-23-pr-audit-resolution.md`:53 records it as "(owner instruction)".

Its enforcement sentence (CLAUDE.md:208-212) says rule 9 is "PARTLY ENFORCED once the owner adds both `subscribe_pr_activity` tools, `send_later` and `create_trigger` to `permissions.deny`". You have added four entries (`.claude/settings.json`:43-46): `mcp__github__subscribe_pr_activity`, `mcp__Claude_Code_Remote__subscribe_pr_activity`, `mcp__Claude_Code_Remote__send_later` and `mcp__Claude_Code_Remote__create_trigger`.

Cloud sessions such as this one expose the tools as `mcp__claude-code-remote__subscribe_pr_activity`, `…__send_later` and `…__create_trigger`, lower case with hyphens; I verified this from this session's own tool list. Whether permission matching treats the two spellings as the same is [UNVERIFIED]. Testing it would mean calling a tool rule 9 forbids.

Rule 9's text is yours to approve. The ledger line that says so (:8209) is recorder text, but rule 9 records your instruction, so it is treated as yours.

**DECISION NEEDED.** Approve the reworded enforcement sentence, and will you add the three lower-case names to the deny list?

**OPTIONS.**
- **(a) Both.** One CLAUDE.md sentence, plus three lines that you add to `.claude/settings.json`. If matching already treats the spellings alike, the extra entries are harmless duplicates; if it does not, they close the gap. Reversible.
- **(b) Sentence only.** The deny gap, if real, stays.
- **(c) Leave.** The sentence keeps describing a future step that is already done.

**RECOMMENDATION.** (a). Confidence: high that the sentence is stale; medium that the names actually mismatch.

**IF APPROVED, I WILL:** Replace CLAUDE.md's sentence beginning "→ **PARTLY ENFORCED** once the owner adds", up to "deny `unsubscribe_pr_activity`.", with:

> → **PARTLY ENFORCED** by `permissions.deny` in `.claude/settings.json`, which stops explicit subscription and polling only if its names match the tools the session exposes (check the session's tool list); it does not stop the subscription PR creation makes, so the unsubscribe step is yours. Never deny `unsubscribe_pr_activity`.

The `ci.yml` concurrency clause after it stays. You add `mcp__claude-code-remote__subscribe_pr_activity`, `mcp__claude-code-remote__send_later` and `mcp__claude-code-remote__create_trigger` to `permissions.deny`. CLAUDE.md:208 assigns that edit to you. Rule 9's imperatives and its "Proof" text are not touched here.

**PROMPT (copy-paste ready):**
```
Task: update CLAUDE.md rule 9's enforcement sentence (the owner approved on <date>). The sentence beginning "→ **PARTLY ENFORCED** once the owner adds both `subscribe_pr_activity` tools" is stale: .claude/settings.json permissions.deny already lists mcp__github__subscribe_pr_activity, mcp__Claude_Code_Remote__subscribe_pr_activity, mcp__Claude_Code_Remote__send_later and mcp__Claude_Code_Remote__create_trigger. Cloud sessions expose the lower-case hyphenated names mcp__claude-code-remote__…; whether deny matching normalizes them is unverified.
Do: replace that sentence, through "Never deny `unsubscribe_pr_activity`.", with: "→ **PARTLY ENFORCED** by `permissions.deny` in `.claude/settings.json`, which stops explicit subscription and polling only if its names match the tools the session exposes (check the session's tool list); it does not stop the subscription PR creation makes, so the unsubscribe step is yours. Never deny `unsubscribe_pr_activity`." Keep the following ci.yml concurrency clause. Do not edit .claude/settings.json; the owner adds mcp__claude-code-remote__subscribe_pr_activity, mcp__claude-code-remote__send_later and mcp__claude-code-remote__create_trigger. Do not call any subscribe, send_later or create_trigger tool to test matching.
Constraints: rule 9's text is the owner's (approved above); change nothing else in rule 9. No new machinery; no counts; no database. Edit tool. Governance-only PR; preflight once; open the PR last; unsubscribe at once.
Return: before and after quotes, git diff --stat.
```

---

## C5 functional-taxonomy.md: the axis layer, and whether two doctrine files are "history"   [class: OWNER-ONLY]

**CONTEXT.**
`governance/functional-taxonomy.md`:1-10 presents a "Two-Layer Model (Axes × Profiles)", "RATIFIED … Doctrine OPERATIVE". It cites a staged schema that does not exist. The database has no axis tables.

The record of how the axis layer ended:
- **2026-08-24, your words:** "I don't want axis to be used"; "Axis is a term that we should be able to use freely to describe how things are set up" (ledger :810). That ruling is about the word.
- **2026-08-25, your ruling:** the layer "is renamed **`icf_demands`** … and it is NOT folded into `access_needs`" (:1103-1105). That kept the layer.
- **2026-09-13:** "'AX-' for ICF should never ever exist anywhere" (:3399). The recorder then wrote that whether the layer "survives at all … is owner-gated" (:3504-3508).
- **R35, a delegated ruling:** it "Ruled retired" the layer (agent; `workplan/pipeline-state-graph/RULINGS.md`:77, :248), under your delegation of 2026-10-14 (:4425).
- **Migration 109** dropped the tables. Its header leaves this document's edit as "an owner merge" (`scripts/migrations/109_drop_axes.sql`).

So the retirement was a delegated act. No owner words retired the layer.

conceptual-model.md already has its banner (approved item B6, applied). CLAUDE.md §9 (:542) still routes "Entity model, ICF frame" to both files. Population taxonomy structure is owner-only (decision-protocol.md §2.4 item 2).

**DECISION NEEDED.** Add a banner to functional-taxonomy.md saying which parts are history, and re-point CLAUDE.md §9's "Entity model, ICF frame" row away from the two files?

**OPTIONS.**
- **(a) Banner and re-point the §9 row.** One inserted paragraph in a ratified file, plus one table row. Reversible. It does not declare the whole file history: the survivors are named.
- **(b) Banner only.** CLAUDE.md keeps routing sessions to two files built on deleted layers.
- **(c) As (a), and you also say "axis retirement confirmed".** R35 then becomes your ruling rather than a delegated one. That is one more sentence from you; it is low risk because the tables are gone and the word is already banned as a layer name.
- **(d) Leave.**

**RECOMMENDATION.** (a). Add (c)'s sentence only if you want the retirement on your own authority. Confidence: high on the banner. Medium on the exact survivor list: it rests on the antagonists' reading of §5, which I checked against the file's numbering (§5 items 1-8 at :317-367).

**IF APPROVED, I WILL:**
1. Insert after functional-taxonomy.md:10, with no ⚠ (⚠ is now a marker):
   > **Superseded in part (noted 2026-11-26).** The axis layer this document is built on no longer exists. The owner ruled on 2026-08-24 that "axis" is not to name a layer ("I don't want axis to be used") and on 2026-09-13 that "'AX-' for ICF should never ever exist anywhere". The layer was retired by delegated ruling R35 (`workplan/pipeline-state-graph/RULINGS.md`, under the owner's delegation of 2026-10-14) and dropped by `scripts/migrations/109_drop_axes.sql`. The live frame is three lenses: identity, ICF and access need (CLAUDE.md §6). Read §2, the axis half of §3.3, §4, §5 items 1–4 and 8, §6–§8 and §9.2–§9.8 as history. Not touched: §0.5 (except `population_axis_map` and `situations`, both dropped), §3.1, §3.3's diagnosis-optional and naming paragraphs, §5 item 5, §5 item 7's "Co-1 = tier 1 = eligible to anchor ● claims", and §9.1. §5 item 6 (non-DOI intake) is not assessed here.
2. In CLAUDE.md §9, replace "| Entity model, ICF frame | `governance/conceptual-model.md`, `governance/functional-taxonomy.md` |" with two rows: "| The schema | `sqlite_master` and `PRAGMA table_info`, read-only (§4) |" and "| ICF codes and the three lenses | §6; `python3 scripts/db.py icf-glossary` |".
3. With (c), also append a ledger entry quoting your sentence.

**PROMPT (copy-paste ready):**
```
Task: mark governance/functional-taxonomy.md as superseded in part, and re-point CLAUDE.md §9's "Entity model, ICF frame" row. The owner approved on <date> (answer: "<a or c>").
Facts to verify first (git grep -n -F on references/project-standards.md): "I don't want axis to be used" (2026-08-24); "is renamed **`icf_demands`**" (2026-08-25, which kept the layer); "should never ever exist anywhere" (2026-09-13). R35 in workplan/pipeline-state-graph/RULINGS.md ("Ruled retired", agent) is a delegated ruling under the owner's 2026-10-14 delegation. scripts/migrations/109_drop_axes.sql dropped the tables and left this document "an owner merge".
Do:
1. Read functional-taxonomy.md's section numbering. Confirm §5 has items 1-8, item 6 is non-DOI intake, and item 7 contains "Co-1 = tier 1 = eligible to anchor ● claims". If any differs, stop and report.
2. Insert after the Status block, without the ⚠ glyph (it is a marker now), the paragraph: "**Superseded in part (noted 2026-11-26).** The axis layer this document is built on no longer exists. The owner ruled on 2026-08-24 that "axis" is not to name a layer ("I don't want axis to be used") and on 2026-09-13 that "'AX-' for ICF should never ever exist anywhere". The layer was retired by delegated ruling R35 (`workplan/pipeline-state-graph/RULINGS.md`, under the owner's delegation of 2026-10-14) and dropped by `scripts/migrations/109_drop_axes.sql`. The live frame is three lenses: identity, ICF and access need (CLAUDE.md §6). Read §2, the axis half of §3.3, §4, §5 items 1–4 and 8, §6–§8 and §9.2–§9.8 as history. Not touched: §0.5 (except `population_axis_map` and `situations`, both dropped), §3.1, §3.3's diagnosis-optional and naming paragraphs, §5 item 5, §5 item 7's "Co-1 = tier 1 = eligible to anchor ● claims", and §9.1. §5 item 6 (non-DOI intake) is not assessed here."
3. In CLAUDE.md §9, replace the row "Entity model, ICF frame" with "| The schema | `sqlite_master` and `PRAGMA table_info`, read-only (§4) |" and "| ICF codes and the three lenses | §6; `python3 scripts/db.py icf-glossary` |".
4. If the answer included "axis retirement confirmed", append a ledger entry "Owner statement 2026-11-26 — the axis layer's retirement is confirmed" quoting it.
5. Check atoms: run python3 workplan/pipeline-state-graph/build_graph.py --check before and after; no new failures.
Constraints: CLAUDE.md rule 0; population taxonomy structure is owner-only (decision-protocol §2.4 item 2) and this applies the owner's approval. No new machinery; no counts; no database; Edit tool; locate by quoted text. Governance-only PR; preflight once; open the PR last; unsubscribe at once.
Return: before and after quotes with file:line, build_graph result, git diff --stat.
```

---

## C6 The pipeline contract: `ratified: false` and the stage anchors   [class: OWNER-ONLY]

**CONTEXT.**
`governance/pipeline-contract.yaml`:3 reads `ratified: false`. Its comment (:4-7) gives reasons the DR process later removed, and says "Ratifying the corrected contract is owner decision OD-17".

What the ledger records on OD-17:
- 2026-11-12, you deferred it: "Ratify after T-022 merges, once I have read the corrected contract" (:6066-6068).
- 2026-11-19, "Ratify all" marked OD-17 `ANSWERED BY THE OWNER` (:7986-7987). That status rests on the recorder's [ASSUMPTION] that "all" included OD-17, noting "the owner has not been shown the contract diff in this session" (:7983).

So your own condition, reading the contract, is recorded as unmet. Nothing gates on the field; `scripts/audit/pipeline_contract_audit.py`:167 only prints it.

Separately, the stage descriptions ("anchors") disagree with your 2026-08-27 spine: "you research slugs, evidence research, judge evidence, synthesize judgments, specify syntheses, and render specifications" (:1454).
- The judgment anchor (:185) reads "the 4-state determination machine + convergence + directness".
- The contract's own note (:383-389) says "directness belongs to `judgment`, convergence to `synthesis`, and the determination machine to `specification`". It calls the text edit "an OPEN POINT for the owner" with no task (:392-397).
- The specification anchor (:286-287) cites `conceptual-model.md:90`, which the B6 banner moved to :91.
- The synthesis anchor's "Opus-only" wording (:275) is handled by approved item A3.

**DECISION NEEDED.** (1) Keep `ratified: false` until you have read the contract, or ratify it now? (2) Apply your 2026-08-27 spine to the judgment and specification anchors?

**OPTIONS.**
- **(a) Keep false, fix the comment, apply the spine to the anchors.** Edits a header comment and two anchors, and deletes the two trailing notes the edit makes obsolete. Reversible.
- **(b) Ratify now and apply the spine.** `ratified: true` waives your own read condition; a later reading may find text you did not mean to ratify.
- **(c) Comment only.** The anchors keep contradicting the spine.

**RECOMMENDATION.** (a). It costs you no reading now, and the spine edit only carries out your own words (rule 0). Confidence: medium-high. Choose (b) if you no longer need to read the contract before ratifying it.

**IF APPROVED, I WILL:**
1. Replace the comment at :4-7 with: `# OD-17: the 2026-11-19 status line rests on an unratified reading that "Ratify all" included it (ledger: "Owner ratification 2026-11-19"); the owner's condition, reading the corrected contract, is recorded unmet.`
2. Set the judgment anchor to: `'the judgment item: each extracted value of an evidence item, its tier verdict and directness, and its lens tags (owner 2026-08-27: "judge evidence"; 2026-11-14: "yes lens in judgment")'`.
3. Set the specification anchor to: `'the determination and its state machine — "therefore 1200 mm, marked ●" (owner 2026-08-27: "specify syntheses")'`. This drops the conceptual-model line citation.
4. Delete the two trailing comment notes the anchors supersede (:383-397).
5. Re-check the atoms that cite contract lines by number (the note says "hand-written atoms cite the lines above by number") with `build_graph.py --check`.

**PROMPT (copy-paste ready):**
```
Task: two edits to governance/pipeline-contract.yaml, approved by the owner on <date> (answer "<a or b>").
Verify first: ledger references/project-standards.md, "OD-17" lines (git grep -n -F "OD-17" -- references/project-standards.md). The 2026-11-12 deferral reads "Ratify after T-022 merges, once I have read the corrected contract"; the 2026-11-19 ANSWERED status rests on an [ASSUMPTION] that "all" included OD-17. The owner's spine (2026-08-27) is "you research slugs, evidence research, judge evidence, synthesize judgments, specify syntheses, and render specifications"; also "yes lens in judgment" (2026-11-14).
Do:
1. If the answer is (a): keep `ratified: false` and replace the four-line comment under it with: # OD-17: the 2026-11-19 status line rests on an unratified reading that "Ratify all" included it (ledger: "Owner ratification 2026-11-19"); the owner's condition, reading the corrected contract, is recorded unmet. If the answer is (b): set `ratified: true` with a comment citing the owner's <date> words, and append a ledger entry quoting them with "OD-17 STATUS: ANSWERED BY THE OWNER".
2. Set the judgment anchor to: 'the judgment item: each extracted value of an evidence item, its tier verdict and directness, and its lens tags (owner 2026-08-27: "judge evidence"; 2026-11-14: "yes lens in judgment")'.
3. Set the specification anchor to: 'the determination and its state machine — "therefore 1200 mm, marked ●" (owner 2026-08-27: "specify syntheses")'.
4. Delete the two trailing comment notes dated 2026-11-19 that describe this edit as owed. Leave the translation block and any synthesis-anchor wording already changed by item A3.
5. Run python3 workplan/pipeline-state-graph/build_graph.py --check before and after; re-quote any atom that cited the deleted lines. Run python3 scripts/audit/pipeline_contract_audit.py and confirm the contract still loads.
Constraints: CLAUDE.md rule 0; OD-17 is the owner's act. No new machinery; no counts; no database. Edit tool; locate by quoted text. Governance-only PR; preflight once; open the PR last; unsubscribe at once.
Return: before and after quotes, check results, git diff --stat.
```

---

## C7 Two stale doctrine statements: "CANONICAL" population taxonomy, and typical evidence types   [class: OWNER-ONLY]

**CONTEXT.**

(a) `governance/held-tensions.md` is RATIFIED doctrine (:3). It calls `governance/population-taxonomy.md` "(CANONICAL)" at :20 and in its table at :380. But population-taxonomy.md's own status line (:2) reads "SUPERSEDED (population code set)", with a banner pointing to DR-2026-07-23. The live code table is `base_taxonomy_identity`.

(b) `governance/tier-system.md` §1's "Typical `evidence_type`" column disagrees with the code that assigns tiers (`schemas/tier_derivation.py`:55-65, `TIER_MAP`):
- The T1 row (:15) says "occasionally `grey`", but grey always maps to tier 3. Your 2026-11-06 words "if government report is academically sound then it can be t3 I think" (ledger :4928) agree with the code.
- The T3 row (:19) says "occasionally `standard_eb`", but standard_eb maps only to tiers 2 or 4.
- The T5 row (:21) lists `standard_eb`, but T5 is `national_fw` only.

Tier definitions and population taxonomy are both owner-only (decision-protocol §2.4 items 2 and 3). The edits correct labels to match ratified decisions and the code; they change no definition.

**DECISION NEEDED.** Correct both: (a) the two "CANONICAL" labels, and (b) the three typical-type cells?

**OPTIONS.**
- **(a)+(b) Correct both.** Two labels in held-tensions.md and three cells in tier-system.md. Reversible.
- **(a) only, or (b) only.**
- **Leave.** Sessions keep reading a superseded file as canonical, and a tier table that the code contradicts.

**RECOMMENDATION.** Both. Confidence: high for (a). Medium-high for (b), because the cells say "typical", and the code is the rule (CLAUDE.md rule 8: derive, do not curate).

**IF APPROVED, I WILL:**
1. In held-tensions.md:20, change "`governance/population-taxonomy.md` (CANONICAL)" to "`governance/population-taxonomy.md` (SUPERSEDED as to its code set; live codes: `base_taxonomy_identity`)". At :380, change the status cell "CANONICAL" to "SUPERSEDED (code set)".
2. In tier-system.md: :15 "`clinical`, occasionally `grey` for unpublished primary" becomes "`clinical` (high control)"; :19 drops "occasionally `standard_eb` for specialised technical guidance"; :21 "`national_fw` (predominant), `standard_eb`" becomes "`national_fw`". Add one sentence under the table: "The tier a type and scope take is `TIER_MAP` in `schemas/tier_derivation.py`."
3. If C1 is approved, the T2 cell's "occasionally `co2`" deletion goes in the same edit.

**PROMPT (copy-paste ready):**
```
Task: correct two stale doctrine statements (owner approved on <date>: "<answer>").
(a) governance/held-tensions.md calls governance/population-taxonomy.md "(CANONICAL)" in its preamble and in its source table. population-taxonomy.md's own status line says "SUPERSEDED (population code set)". Change the preamble mention to "(SUPERSEDED as to its code set; live codes: `base_taxonomy_identity`)" and the table's status cell to "SUPERSEDED (code set)".
(b) governance/tier-system.md §1's "Typical `evidence_type`" cells must agree with TIER_MAP in schemas/tier_derivation.py. Read TIER_MAP first. Then: T1 row, replace "`clinical`, occasionally `grey` for unpublished primary" with "`clinical` (high control)". T3 row, drop "occasionally `standard_eb` for specialised technical guidance". T5 row, replace "`national_fw` (predominant), `standard_eb`" with "`national_fw`". Add under the table: "The tier a type and scope take is `TIER_MAP` in `schemas/tier_derivation.py`." If the Co-2 edit (C1) was approved, also delete "occasionally `co2` …" from the T2 row in the same pass. If TIER_MAP differs from this description, stop and report.
Constraints: CLAUDE.md rule 0; decision-protocol §2.4 items 2 and 3 are the owner's (approved above). No new machinery; no counts; no database. Edit tool; locate by quoted text. Governance-only PR; preflight once; open the PR last; unsubscribe at once.
Return: before and after quotes with file:line, git diff --stat.
```

---

## C8 DR-2026-08-19 history note   [class: OWNER-ONLY]

**Merged into C4.** It is one decision: the order of authority decides what the DR still governs. C4's IF APPROVED step 4 is the note. It names the spent claims and lists no "sections that still bind", because writing such a list would mean an agent re-ratifying a DG-NON record (DR :87-88). Answering C4 answers C8.

---

## C9 Two meanings of "thin"   [class: OWNER-ONLY]

**CONTEXT.**
On 2026-11-12 you selected OD-10: "Strength: 'provisional' = thin evidence; a re-read is a reading's own status" (ledger :5980-5982). A cell's state `provisional` is computed, for example for a cell resting only on the regulatory stratum, or only on T3.

On 2026-11-14 you made "thin" a cause of ⚠: "thin too" (ACTION: "⚠ in place of the circle for a grey, thin or unverified basis", :7078). You then defined it: "I think thin is when the evidence doesn't directly concern someone but is conjecture" (:7087).

If both "thin"s are the same, every `provisional` cell takes ⚠. The contract keeps every regulatory-stratum-only cell `provisional` (`governance/pipeline-contract.yaml`:299-303). A T4-only cell would then take ⚠, but you ruled "T4 only half circle" (:7195), which is ◐.

**DECISION NEEDED.** Is the "thin evidence" of `provisional` (OD-10) the same "thin" that takes ⚠?

**OPTIONS.**
- **(a) No, two meanings.** `provisional` means limited strength (computed); ⚠-thin means the evidence does not directly concern the people served and is conjecture. Cost: one ledger entry and a wording change wherever `provisional` is glossed as "thin" (derive: `git grep -n -i -E "provisional.{0,30}thin|thin.{0,30}provisional" -- governance CLAUDE.md`).
- **(b) Yes, the same.** Every `provisional` cell takes ⚠. This contradicts "T4 only half circle". It changes how markers are computed (T-117) and needs a decision on which ruling yields.
- **(c) Leave.** Two meanings of one word stay in force.

**RECOMMENDATION.** (a). Your 2026-11-14 definition is about directness, while OD-10's is about strength, and (b) collides with a later ruling of yours. Confidence: high.

**IF APPROVED, I WILL:** Append a ledger entry quoting your answer: "thin" (⚠) is your 2026-11-14 definition, and `provisional` is computed strength, not "thin" in the ⚠ sense. Change each gloss found by the grep above from "thin evidence" to "limited evidence strength". Leave OD-10's recorded words untouched.

**PROMPT (copy-paste ready):**
```
Task: separate two meanings of "thin" (owner answered on <date>: "<answer>").
Verify: git grep -n -F "provisional' = thin evidence" -- references/project-standards.md (OD-10, 2026-11-12); git grep -n -F "doesn't directly concern someone" -- references/project-standards.md (2026-11-14 definition of thin, a cause of the ⚠ marker); git grep -n -F "T4 only half circle" -- references/project-standards.md.
If the answer is (a): append a ledger entry "Owner answer 2026-11-26 — 'provisional' is limited strength; 'thin' (⚠) is evidence that does not directly concern the people served". Quote the owner's words, with readings marked [ASSUMPTION]. Then find glosses with git grep -n -i -E "provisional.{0,30}thin|thin.{0,30}provisional" -- governance CLAUDE.md skills, and change "thin evidence" to "limited evidence strength" where it glosses `provisional`. Do not edit ledger history lines.
If the answer is (b): stop. Report the cells and criteria that conflict (pipeline-contract no-regulatory-stratum-stated; "T4 only half circle"), and ask the owner which ruling yields.
Constraints: CLAUDE.md rule 0; marker and tier meanings are the owner's (decision-protocol §2.4 item 3). No new machinery; no counts; no database; Edit tool. Governance-only PR; preflight once; open the PR last; unsubscribe at once.
Return: the ledger entry, each changed line with before and after quotes, git diff --stat.
```

---

## C10 "Never population umbrellas"   [class: OWNER-ONLY]

**CONTEXT.**
CLAUDE.md:378-379 says "Work from the ICF/access-need frame with codes AND names, never bare axis codes, never population umbrellas". The record has moved on in three steps:
1. The 2026-07-22 RULE "Work from axes — no armchair umbrellas" (ledger :561).
2. It was amended on 2026-07-23 by the design-equivalence exception. An umbrella code "IS permitted when its members do not meaningfully …" differ in design terms, on your words "brain and complex are literally TOO complex to avoid umbrellas" (:567, :570).
3. On 2026-11-21 you answered GAP-379's umbrella question: "3 to umbrella and to specific, yes" (:8290). A need may be keyed on an umbrella identity such as NDV, COM, BRAIN or MH, and on its members, both at once.

You also said on 2026-11-12: "use advocacy groups and disability ethics as a lens for grouping/sorting/taxonomy" (:5927). The word "axis" in CLAUDE.md's sentence names a layer that no longer exists (see C5). Population taxonomy is owner-only (decision-protocol §2.4 item 2).

**DECISION NEEDED.** Replace "never bare axis codes, never population umbrellas" with wording that matches your later rulings?

**OPTIONS.**
- **(a) Narrow the wording** to: "never bare codes; never an umbrella coined without a ruling (an umbrella identity is used only where the owner's rulings admit it: the 2026-07-23 design-equivalence test, and 2026-11-21 'to umbrella and to specific')". One sentence; reversible.
- **(b) Delete "never population umbrellas"** and keep "never bare codes". Shorter, but it loses the guard against armchair umbrellas that the 2026-07-22 RULE still holds.
- **(c) Leave.** CLAUDE.md forbids what you have permitted.

**RECOMMENDATION.** (a). It keeps the guard and admits what you ruled. Confidence: high.

**IF APPROVED, I WILL:** Replace in CLAUDE.md §6 "never bare axis codes, never population umbrellas" with "never bare codes, and never an umbrella identity no ruling admits (the 2026-07-23 design-equivalence test; owner 2026-11-21: \"to umbrella and to specific, yes\")". No other file changes. `functional-taxonomy.md`'s "no armchair umbrellas" text is covered by C5's banner.

**PROMPT (copy-paste ready):**
```
Task: align CLAUDE.md §6's "never bare axis codes, never population umbrellas" with the owner's rulings (approved on <date>).
Verify with git grep -n -F on references/project-standards.md: "Work from axes — no armchair umbrellas" (2026-07-22 RULE); "Design-equivalence exception to the anti-umbrella rule" (2026-07-23); "3 to umbrella and to specific, yes" (2026-11-21). The axis layer no longer exists (scripts/migrations/109_drop_axes.sql).
Do: replace the phrase "never bare axis codes, never population umbrellas" with "never bare codes, and never an umbrella identity no ruling admits (the 2026-07-23 design-equivalence test; owner 2026-11-21: "to umbrella and to specific, yes")". Change nothing else.
Constraints: CLAUDE.md rule 0; population taxonomy is the owner's (decision-protocol §2.4 item 2; approved above). No new machinery; no counts; no database; Edit tool. Governance-only PR; preflight once; open the PR last; unsubscribe at once.
Return: before and after quotes, git diff --stat.
```

---

## D2 OD-77: which mapping did you doubt?   [class: question]

**CONTEXT.**
On 2026-11-22 you typed "I don't think the mapping is correct" (ledger :8407). Your earlier message that day complained of "entire groups like b750 to b789 which are all under "Movement functions"" (:8401).

Two tables could be "the mapping":
- **(A) `identity_icf_map`**: identity to ICF activity codes. It is the only link table that references range codes such as b750-b789. Derive: `select count(*) from identity_icf_map t join base_icf b on b.icf_code=t.icf_code where b.is_range=1`. The same query on `identity_need_icf` and `access_need_icf` returns none.
- **(B) The identity–need–ICF rows of pull request 245.**

OD-77 was resolved under delegation as (A) (:8596). Since then, sessions may not add to `identity_icf_map`, T-128 is withdrawn (OD-87), and the PR-245 rows are "not condemned". What you meant by your own words is outside any grant (OD-79, :8503), so the delegated reading holds only until you answer.

**DECISION NEEDED.** Did you mean (A) `identity_icf_map` or (B) the PR-245 rows?

**OPTIONS.**
- **(A)** No change in data or tasks. OD-77 becomes your answer.
- **(B)** The hold moves to `identity_need_icf`. Its rows need your review, retirements need your ledger entry, and the `identity_icf_map` freeze can be revisited. Cost: a review pass.
- **Leave.** No cost now. The delegated reading stands; nothing on the critical path reads `identity_need_icf` (OD-85).

**RECOMMENDATION.** Answer "A" if it matches what you meant; the range-code evidence points there. If you are unsure, leave it: nothing waits on it. Confidence: medium.

**IF APPROVED, I WILL:** Append "Owner answer 2026-11-26 — OD-77: the mapping doubted is <A or B>" with the line `OD-77 STATUS: ANSWERED BY THE OWNER`. Under B, also list the `identity_need_icf` rows for your review: `select triple_id, identity_code, need_code, icf_code, state from identity_need_icf where retired_at is null`.

**PROMPT (copy-paste ready):**
```
Task: record the owner's answer to OD-77 ("which mapping did you doubt"): "<A or B>" (given <date>).
Verify: git grep -n -F "I don't think the mapping is correct" -- references/project-standards.md; the delegated resolution "OD-77" in "Delegated resolutions 2026-11-25 (second)".
Do: append a ledger entry "Owner answer 2026-11-26 — OD-77, the mapping doubted is <identity_icf_map | the identity-need-ICF rows of PR 245>". Quote the answer, add "OD-77 STATUS: ANSWERED BY THE OWNER", and add CONDITION, ACTION and DATE lines. If B: do not change any row. List the live identity_need_icf rows (read-only query) for the owner's review, and note in the entry that the hold moves to them.
Constraints: CLAUDE.md rule 0; the meaning of the owner's words is the owner's (OD-79). No new machinery; no counts typed; no database writes. Governance-only PR; open it last; unsubscribe at once.
Return: the entry text and the PR link (and, for B, the query output).
```

---

## D3 OD-76: the only open decision in the register   [class: question]

**CONTEXT.**
OD-76 proposed writing `parent_code = MOB` (the mobility umbrella) for SCI and LMB and adding an `amend-identity --parent` writer. It was "withdrawn: superseded by the owner's eighth and ninth sets of 2026-11-12 (LMB leaves mobility; SCI is held with WHEEL)" (ledger :8455-8457).

Its status is `WITHDRAWN, REFERRED BACK TO THE OWNER`. It is the only OD whose last status is neither owner-answered nor delegated. Derive with: `python3 -c "import re;s={};[s.__setitem__(m[1],m[2]) for m in re.finditer(r'^(OD-\d+) STATUS: (.*)$',open('references/project-standards.md').read(),re.M)];print({k:v for k,v in s.items() if v not in ('ANSWERED BY THE OWNER','RESOLVED UNDER DELEGATION')})"`.

The register says it "Releases: nothing" (`REMEDIATION-WORKPLAN.md`:1363), and T-147 adds no parent writer (`tasks/T-147-icf-hierarchy.md`:21). If SCI retires into WHEEL (D4) and LMB becomes UPL outside mobility (your eighth set, :6129), there is nothing left for OD-76 to do.

**DECISION NEEDED.** Close OD-76 as moot?

**OPTIONS.**
- **(a) "Moot".** One ledger line; the register shows no open decision. If you later keep SCI (D4 "no"), SCI's parent edge would be a new question.
- **(b) Leave.** No cost to work, but it reads as open in every count of open decisions.

**RECOMMENDATION.** (a), provided D4 is "yes". Confidence: high.

**IF APPROVED, I WILL:** Append to the same 2026-11-26 owner entry: "OD-76: moot (SCI retires into WHEEL; LMB becomes UPL outside mobility); no parent edges and no parent writer", with `OD-76 STATUS: ANSWERED BY THE OWNER`.

**PROMPT (copy-paste ready):**
```
Task: record the owner's answer "OD-76 moot" (given <date>).
Verify: git grep -n -F "OD-76" -- references/project-standards.md shows it WITHDRAWN, REFERRED BACK TO THE OWNER, superseded by the 2026-11-12 eighth and ninth sets. Check the owner's SCI answer (item D4) first; if the owner kept SCI as an identity, stop and report.
Do: append to a dated "Owner answer 2026-11-26 — …" ledger entry the lines "OD-76: moot (SCI retires into WHEEL; LMB becomes UPL outside mobility); no parent edges and no parent writer" and "OD-76 STATUS: ANSWERED BY THE OWNER", quoting the owner's word.
Constraints: CLAUDE.md rule 0; population taxonomy is the owner's (decision-protocol §2.4 item 2). No new machinery; no database; no counts. Governance-only PR; open it last; unsubscribe at once.
Return: the entry text.
```

---

## D4 SCI retires into WHEEL (OD-83)   [class: question]

**CONTEXT.**
On 2026-11-12 you answered OI-13: "except SCI is the same as WHEELCHAIR basically and LMB is the same as PROSTHETIC" (ledger :6115). In the eighth set you moved LMB out of mobility, which left "only SCI is the same as WHEEL" (:6129; OI-13 `ANSWERED BY THE OWNER`).

On 2026-11-16 the recorder noticed a problem. A separate acceptance (OI-48) had rested on the injury level being held "in the medical lens", which you deleted that day. It put the question to you as OI-77, and its ACTION said not to retire SCI before you answer (:7713-7727).

On 2026-11-25 a delegated resolution, OD-83, ruled that SCI retires into WHEEL, citing your OI-13 words (:8608). The retirement is one-way through the sanctioned verbs; restoring SCI would need a compensating migration. Today SCI is `active`, WHEEL does not exist yet, and GAP-111 (the OI-77 question) is `OPEN`. Derive: `select identity_code,status from base_taxonomy_identity where identity_code in ('SCI','WHEEL')`; `select status from gaps where gap_id='GAP-111'`.

On whether a merge would settle it: your 2026-07-24 RULE makes a merge a ratification unless noted, but not for DG-NON substance you never gave (:582-585, limit (4)). Your OI-13 words are that substance, so merging T-102 would arguably ratify the retirement. An explicit word is cheaper than relying on that, given the retirement is one-way.

**DECISION NEEDED.** Does SCI retire into WHEEL now that the medical lens is gone?

**OPTIONS.**
- **(a) Yes.** OD-83 becomes your answer. T-102 mints WHEEL, carries SCI's rows, closes GAP-111 citing your entry, then retires SCI. An injury's effect is held by ICF body-function codes; you allowed identity-to-b-code links on 2026-11-21 (third). Not reversible without a compensating migration.
- **(b) No, keep SCI as its own identity.** WHEEL is still minted; two codes cover overlapping groups; OD-76's SCI parent edge comes back (D3).
- **Leave.** OD-83 stands under delegation, and T-102 can run on it. A one-way population-code act then rests on a delegated reading.

**RECOMMENDATION.** (a). Your own OI-13 words say it, and the 2026-11-16 premise concerned where the injury level is held, not whether the two groups are one. Confidence: high.

**IF APPROVED, I WILL:** Append "Owner answer 2026-11-26 — SCI retires into WHEEL (OI-77; OD-83 confirmed)", quoting your word, with `OD-83 STATUS: ANSWERED BY THE OWNER`. T-102 then cites that heading for `retire-identity --approval-ref` and `close-gap --resolution-kind ledger`. No database change happens in this step.

**PROMPT (copy-paste ready):**
```
Task: record the owner's answer on SCI: "<yes | no>" (given <date>).
Verify: git grep -n -F "SCI is the same as WHEELCHAIR basically" -- references/project-standards.md (2026-11-12, OI-13); the "Correction 2026-11-16" entry that put OI-77; OD-83 in "Delegated resolutions 2026-11-25 (second)". Read-only: select identity_code,status from base_taxonomy_identity where identity_code in ('SCI','WHEEL'); select status from gaps where gap_id='GAP-111'.
Do: append "Owner answer 2026-11-26 — SCI <retires into WHEEL | stays its own identity> (OI-77)". Quote the owner's word and add "OD-83 STATUS: ANSWERED BY THE OWNER" (for yes) or a line referring OD-83 back (for no). Add CONDITION, ACTION and DATE lines. For yes, the ACTION names T-102's order: mint WHEEL, carry SCI's lens links, carry or retire its identity_icf_map crossings by judgment, close GAP-111 citing this entry, retire SCI. Do not run T-102 here.
Constraints: CLAUDE.md rule 0; population taxonomy is the owner's (decision-protocol §2.4 item 2). No database writes in this task. No new machinery; no counts. Governance-only PR; open it last; unsubscribe at once.
Return: the entry text and its exact heading (T-102 will cite it).
```

---

## D5 D-0184 and the other PENDING rows in the `decisions` table   [class: question]

**CONTEXT.**
The `decisions` table holds rows up to D-0188 of 2026-09-11 (`select max(decision_id), max(decision_date) from decisions`). Some of its rows have `review_status = 'PENDING'` (`select count(*) from decisions where review_status='PENDING'`), D-0184 among them. CLAUDE.md:402 treats D-0184 as settled ("the traversal D-0184 measured and rejected").

The ledger supports that:
- Your ruling entry of 2026-09-11 carries the ACTION "Cite D-0184 for the lens mechanism, not D-0170" (:2898).
- Your OR-1 answer of 2026-10-29 is recorded as "D-0184 stands" (:4630, a recorder reading of your "yes").

R30, a delegated ruling, froze the table: "table frozen as infrastructure residual; ledger the single home" (`workplan/pipeline-state-graph/RULINGS.md`:72). It assigned the decision-protocol edit to "owner merge". No governing document says the table's status columns are not maintained.

**DECISION NEEDED.** Do anything about the stale `PENDING` values?

**OPTIONS.**
- **(a) One sentence in `governance/decision-protocol.md` §0:** "The `decisions` table is frozen (R30); its `status` and `review_status` columns are not maintained; the ledger is the single home of decisions." Reversible.
- **(b) Do nothing.** Sessions may keep reading `PENDING` as open.
- **(c) Update the rows by migration.** This writes to a frozen table that nothing reads; not recommended.

**RECOMMENDATION.** (a). Confidence: medium. (b) is acceptable if you would rather add no text.

**IF APPROVED, I WILL:** Append that sentence to decision-protocol.md §0 (after line 11's sentence naming the ledger and `decisions/`). No database change.

**PROMPT (copy-paste ready):**
```
Task: state in governance/decision-protocol.md §0 that the decisions table is frozen (owner approved on <date>).
Verify: workplan/pipeline-state-graph/RULINGS.md row R30 ("table frozen as infrastructure residual; ledger the single home"); read-only: select review_status, count(*) from decisions group by 1.
Do: append to §0's first paragraph: "The `decisions` table is frozen (R30); its `status` and `review_status` columns are not maintained; the ledger is the single home of decisions." Change nothing else; do not touch the database.
Constraints: CLAUDE.md rule 0; R30 makes this an owner merge. No new machinery; no counts; Edit tool. Governance-only PR; open it last; unsubscribe at once.
Return: before and after quotes, git diff --stat.
```

---

## D6 Which columns may a session correct by hand?   [class: question]

**CONTEXT.**
On 2026-11-21 you typed: "I think GAP-368 points towards Claude having permission to hand edit as required for specific columns". You added: "We don't need a tool for many qualitative judgments/corrections because Claude IS a tool. We just need to ensure that you make transparent and record your hand fixes" (ledger :8269-8271).

The recorder read "specific columns" as "columns whose content is a qualitative judgment or wording", excluding identifiers, keys, vocabularies, counts and bibliographic fields. It marked that reading [ASSUMPTION] and "not decided here" (:8276). ACTION (2) says "Do not extend this to a column outside the owner's meaning of 'qualitative'; ask" (:8281).

CLAUDE.md does not carry the exception. CLAUDE.md:294 says "Do not hand-write SQL against a table the CLI can reach", and rule 10 (:217-218) says a gap is "never patched with hand SQL disguised inside the batch's data migration". GAP-368 is still `OPEN` (`select status from gaps where gap_id='GAP-368'`).

The word "wording" in the reading would also admit verbatim source text, such as a figure's `claim_text`. That text must never be changed, under the fetch-before-write rule (CLAUDE.md Goal item 1).

**DECISION NEEDED.** Which columns count as "qualitative" for hand correction?

**OPTIONS.**
- **(a) Only the value cells of qualitative figures:** the GAP-368 case you named. Narrowest; any new case comes back to you.
- **(b) Any cell holding a qualitative judgment a session wrote:** the value of a qualitative figure, a warrant, a note, a rationale or a review note. Never identifiers, keys, vocabulary codes, numbers, units, bibliographic fields (author, title, year), verbatim source text (`claim_text` and other quotations), or your own quoted words. Each fix records the old value, the new value, the reason and the session in the migration header and the gap's resolution.
- **(c) A named list** of table.column pairs that you supply.

**RECOMMENDATION.** (b). It matches "many qualitative judgments/corrections", adds the one exclusion the recorder's "wording" missed, and you do not have to list columns. Confidence: medium.

**IF APPROVED, I WILL:**
1. Append a ledger entry quoting your answer.
2. Add one sentence to CLAUDE.md §4 after "Do not hand-write SQL against a table the CLI can reach.": "Exception (owner, 2026-11-21; scope <date>): a session may correct by hand, in a data migration, a cell holding a qualitative judgment a session wrote (<scope as answered>), recording the old value, new value, reason and session in the migration header and the gap's resolution; identifiers, keys, vocabulary codes, numbers, units, bibliographic fields, verbatim source text and the owner's words stay behind their writers."
3. Add "(the §4 exception for qualitative cells excepted)" after rule 10's "never patched with hand SQL disguised inside the batch's data migration".

**PROMPT (copy-paste ready):**
```
Task: record the scope of hand correction the owner allowed, and add the exception to CLAUDE.md (answer "<a|b|c>", given <date>).
Verify: git grep -n -F "permission to hand edit as required for specific columns" -- references/project-standards.md and the entry's [ASSUMPTION] on "specific columns" and its ACTION (2) ("ask").
Do:
1. Append a ledger entry "Owner answer 2026-11-26 — the columns a session may correct by hand". Quote the answer and state the scope exactly as chosen. For (b) the scope is: a cell holding a qualitative judgment a session wrote (value of a qualitative figure, warrant, note, rationale, review note); never identifiers, keys, vocabulary codes, numbers, units, bibliographic fields, verbatim source text (claim_text, quotations) or the owner's quoted words.
2. In CLAUDE.md §4, after the sentence "Do not hand-write SQL against a table the CLI can reach.", add: "Exception (owner, 2026-11-21; scope 2026-11-26): <scope>; each hand fix is a data migration whose header records the old value, new value, reason and session, and the gap's resolution points to it."
3. In CLAUDE.md rule 10, after "never patched with hand SQL disguised inside the batch's data migration", add "(the §4 exception for qualitative cells excepted)".
Constraints: CLAUDE.md rule 0. No new machinery (no writer verb, no check). No counts. Do not touch the database in this task. Edit tool; locate by quoted text. Governance-only PR; preflight once; open the PR last; unsubscribe at once.
Return: the entry text, before and after quotes, git diff --stat.
```

---

## D7 A separate working-rules file and a size target for CLAUDE.md   [class: question]

**CONTEXT.**
On 2026-11-20 you typed "overall we need to make this project as simple as possible in infrastructure because the more exceptions we have the more complexity we guard against which is the more we spiral" (ledger :8192).

The coordinator then recorded a rewrite proposal, not your words (DATE :8215):
- move rules 0, 1, 4, 5, 6, 9 and 10, §3 (the layers and the spine), §7 (traps) and §8 into "a referenced working-rules file";
- delete the Proof narratives;
- meet a size test of a quarter of the current word count (:8205-8207).

Its ACTION (1) says "Do not rewrite `CLAUDE.md` until the owner approves the content above" (:8214).

On 2026-11-26 you typed: "ensure we strip out all extraneous stuff like change logs and version discussion etc. we want to make sure that claude.md points correctly but also contains some strict rules of operation for us". On 2026-11-25: "build as little machinery as possible".

The audit found the quarter target unreachable while the owner-reserved text stays in CLAUDE.md (`scratchpad/claude-md-audit.md`, "Size, measured"; measure with `wc -w < CLAUDE.md`). Rule and section numbers are cited across scripts and immutable migrations, so moving rules needs a caller sweep. Rule 10 depends on the layer model ("anything Layer 0/1/2"). The separate CLAUDE.proposed.md (approval list item E) is not decided here.

**DECISION NEEDED.** Keep every rule in CLAUDE.md (no working-rules file, no size target), cutting only history, proofs and stale claims?

**OPTIONS.**
- **(a) Keep the rules in CLAUDE.md;** drop the size target; keep the layer model in §3. This closes the 2026-11-20 proposal's move. One ledger entry; later trimming follows E once corrected.
- **(b) Approve the working-rules file and the size target.** One tooling PR, a new file every session must be pointed to, and a sweep of rule-number callers.
- **(c) Leave open.** ACTION (1) keeps blocking any CLAUDE.md rewrite.

**RECOMMENDATION.** (a). Your 2026-11-26 words ask that CLAUDE.md itself "contains some strict rules of operation", and a second rules file is more machinery. Confidence: medium-high.

**IF APPROVED, I WILL:** Append "Owner answer 2026-11-26 — CLAUDE.md keeps its rules; no working-rules file; no size target", quoting your word. Its ACTION supersedes the 2026-11-20 (third) proposal's move and size test (rule 0). No CLAUDE.md edit in this step.

**PROMPT (copy-paste ready):**
```
Task: record the owner's answer on the CLAUDE.md rewrite proposal: "<a|b>" (given <date>).
Verify: the entry "Owner statements 2026-11-20 (third)" in references/project-standards.md (the moved-rules list, the size test, ACTION (1) "Do not rewrite CLAUDE.md until the owner approves the content above", and the DATE line saying the rewrite content is the coordinator's record). Also verify the owner's 2026-11-26 words "contains some strict rules of operation for us" in transcripts/harness_f8d4d6c2/main.jsonl (grep -c -F).
Do: append "Owner answer 2026-11-26 — CLAUDE.md keeps its rules; no working-rules file; no size target" (for a), or the approval of the move (for b). Quote the answer. The ACTION states what it supersedes in the 2026-11-20 (third) entry. Make no CLAUDE.md edit in this task.
Constraints: CLAUDE.md rule 0. No new machinery; no counts typed (give `wc -w < CLAUDE.md` if size is mentioned). Governance-only PR; open it last; unsubscribe at once.
Return: the entry text.
```

---

## D1 Retire the three pending e120 rows: EXECUTION   [class: answered by the owner]

**Already decided.** You typed "D1 retire" (2026-11-26, 22:25 UTC; `grep -c -F 'D1 retire' transcripts/harness_f8d4d6c2/main.jsonl`). That answers the approval-list question "GAP-379: the three pending e120 rows (A-SIZE with LPA, TALL, BAR): review, or retire?".

**What is retired.** `identity_need_icf` rows tie little people (LPA), tall people (TALL) and fat people / people in larger bodies (BAR) to ICF code e120 ("mobility products & technology") through the access need A-SIZE ("fit the range of bodies"). A read-only query at `921b335` shows exactly three such rows, all `pending` and not retired:

`select triple_id, identity_code, icf_code, state, retired_at from identity_need_icf where need_code='A-SIZE' and icf_code='e120'`

They are triple_id 53 (LPA), 57 (TALL) and 61 (BAR). Each identity keeps its other A-SIZE rows (e115, e150, e155): `select identity_code, icf_code from identity_need_icf where need_code='A-SIZE' and retired_at is null and icf_code<>'e120'`.

**The sanctioned verb** is `scripts/db.py review-identity-need-icf`, with flags `--triple-ids` (comma-separated), `--decision {stated,provisional,reject}`, `--approval-ref`, `--reason` (required for reject), `--session` and `--dry-run`. `reject` retires the rows in place, writing `retired_at`, `retired_by_session`, `retirement_reason` and `retirement_ref`. The verb refuses unless `--approval-ref` is the exact heading of exactly one dated ledger entry whose heading begins "Owner" (`_owner_approval`; `dbcore.LEDGER_OWNER_PREFIX`), and unless that entry names every row as the token `TRIPLE-<id>` (`dbcore.ledger_entry_names`). It reads the ledger file in the working tree when it runs, so the entry must exist on the branch first. Precedent: "Owner review 2026-11-21 — rows 64 and 65 …", which retired TRIPLE-65 this way.

**GAP-379's other open part.** GAP-379 has three parts:
1. The umbrella question, which you answered on 2026-11-21 ("3 to umbrella and to specific, yes").
2. The e120 rows, which this retirement answers.
3. A-TRIGGER's two rows on both EPI and COM (triple_id 45-48; derive `select triple_id, identity_code, icf_code, state from identity_need_icf where need_code='A-TRIGGER'`). OD-85 "settles" these only under delegation, with no row changing state. The gap text also lists the rows "recorded as an inference" (the class-C rows BRAIN with A-NOSPEECH and COM with A-LOWLOAD), which OD-85 rejected under delegation without retiring them.

So GAP-379 stays `OPEN` after this work. A dated correction is appended to it; it is not closed.

**Separation (rule 10).** This is a research-data change: rows only, no tooling. It ships in its own pull request, separate from the governance prose PR that carries the approved A and B edits. The ledger entry is the warrant the rows point to, so it goes in the same data PR, on a branch cut from `origin/main`. The separation check classes the ledger as neither tooling nor research data. Alternative: put the entry in the governance PR, merge that first, and open the data PR after. Either way, the two ledger appends may need a trivial merge at the file's tail.

**Draft ledger entry** (heading must be unique and dated; `[ASSUMPTION]` marks readings):

```markdown
## Owner answer 2026-11-26 — the three e120 rows of A-SIZE on LPA, TALL and BAR are retired (GAP-379)

Given in the session `<session stem>` (<session URL>), in a typed message answering the coordinator's approval list, item D1 ("GAP-379: the three pending e120 rows (A-SIZE with LPA, TALL, BAR): review, or retire?"). Derive the time from the preserved transcript (`git grep -n -F "D1 retire" -- transcripts`). Recorded on contact (rule 0).

**Owner's words, quoted (typed):**

> "approve A and B all; reject C4; D1 retire"

**Readings.**

- [ASSUMPTION: "D1 retire" retires the three `identity_need_icf` rows that tie LPA, TALL and BAR to `e120` through A-SIZE — TRIPLE-53 (LPA), TRIPLE-57 (TALL) and TRIPLE-61 (BAR) — by `db.py review-identity-need-icf --decision reject`, which retires in place — basis: the question put named exactly these rows; derive: `select triple_id, identity_code from identity_need_icf where need_code='A-SIZE' and icf_code='e120'`].
- [ASSUMPTION: the need-side row (`access_need_icf`: A-SIZE with e120) stays, and each identity keeps its other A-SIZE rows (e115, e150, e155) — basis: the question asked about the identity rows only].
- This answers GAP-379's e120 part. It does not answer A-TRIGGER's rows on EPI and COM, or the rows recorded as inferences; GAP-379 stays open for those.

CONDITION: any session reading, reviewing or counting TRIPLE-53, TRIPLE-57 or TRIPLE-61, A-SIZE's ICF coverage of LPA, TALL or BAR, or GAP-379.
ACTION: (1) Retire TRIPLE-53, TRIPLE-57 and TRIPLE-61 with this entry as the reference, by `db.py review-identity-need-icf --decision reject`. (2) Append a dated correction to GAP-379 naming this entry; do not close the gap. (3) Treat the readings above as unratified except where the owner's words state them.
DATE: 2026-11-26 — owner answer (typed words, quoted above).
```

**PROMPT (copy-paste ready):**
```
Task: carry out the owner's answer "D1 retire" (typed 2026-11-26): retire the three pending identity_need_icf rows that tie LPA, TALL and BAR to ICF e120 through access need A-SIZE. This is a RESEARCH-DATA session: rows only, no tooling (CLAUDE.md rule 10). Ship it as its own pull request, separate from the governance prose PR.

0. Open the session: run /session-open with slug "e120-retire" BEFORE any other Bash call, so scratchpad/CURRENT and its folder both equal the stem session_<today>-e120-retire (CLAUDE.md §7). Cut a branch from origin/main. Run `bash .claude/hooks/ensure-deps.sh`.
1. Verify read-only (python3, sqlite3 uri 'file:data/guidebook.db?mode=ro'):
   select triple_id, identity_code, icf_code, state, retired_at from identity_need_icf where need_code='A-SIZE' and icf_code='e120';
   Expect exactly three rows, LPA, TALL and BAR, all 'pending' with retired_at NULL. Take the triple_ids from this output (expected 53, 57, 61); if the output differs, STOP and report. Also run select identity_code, icf_code from identity_need_icf where need_code='A-SIZE' and retired_at is null and icf_code<>'e120' to confirm each identity keeps other A-SIZE rows.
2. Append to references/project-standards.md one entry, headed exactly "Owner answer 2026-11-26 — the three e120 rows of A-SIZE on LPA, TALL and BAR are retired (GAP-379)". Quote the owner's typed message verbatim ("approve A and B all; reject C4; D1 retire") and the question it answered. Name the rows as tokens TRIPLE-<id> for each id from step 1. Mark as [ASSUMPTION]: that "retire" means the review verb's reject; that the access_need_icf row A-SIZE/e120 stays; that each identity keeps its other A-SIZE rows. State that GAP-379 stays open for A-TRIGGER's rows on EPI and COM and for the rows recorded as inferences. Add CONDITION, ACTION and DATE lines in the style of "Owner review 2026-11-21 — rows 64 and 65 …". Confirm the heading is unique: grep -c -F '<heading>' references/project-standards.md must print 1.
3. Scratch copy: SCRATCH=$(mktemp -d)/guidebook.db; cp data/guidebook.db "$SCRATCH"; record sha256sum data/guidebook.db. Pass GUIDEBOOK_DB_PATH="$SCRATCH" inline on EVERY command (the shell resets env).
4. Dry run, then the real write:
   GUIDEBOOK_DB_PATH="$SCRATCH" python3 scripts/db.py review-identity-need-icf --triple-ids <ids> --decision reject --approval-ref "<exact heading>" --reason "Retired by the owner (ledger entry '<exact heading>'): e120 (mobility products and technology) is not part of the body-size identities' ICF coverage through A-SIZE." --session session_<today>-e120-retire --dry-run
   then the same command without --dry-run. If the verb refuses, fix the cause it names (heading, tokens); never work around it.
5. GUIDEBOOK_DB_PATH="$SCRATCH" python3 scripts/db.py amend-gap --gap-id GAP-379 --append-note "e120 part answered by the owner 2026-11-26 (ledger '<exact heading>'): the three rows are retired. Still open: A-TRIGGER's two rows on EPI and COM (settled only under delegation, OD-85; no row reviewed) and the rows recorded as inferences (BRAIN with A-NOSPEECH, COM with A-LOWLOAD; rejected under delegation, not retired)." --session session_<today>-e120-retire
   Do NOT close GAP-379.
6. Capture: python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH" --out /tmp/e120.sql. Read the SQL: it must contain only UPDATEs of the three identity_need_icf rows and the GAP-379 gaps row (plus any bookkeeping the tool always emits). Anything else: STOP and report.
7. python3 scripts/emit_data_migration.py --session session_<today>-e120-retire.md --summary "Retire three e120 identity-need rows on LPA, TALL, BAR (owner, 2026-11-26)" --input /tmp/e120.sql
8. python3 scripts/migrate_db.py --session session_<today>-e120-retire (applies it to data/guidebook.db). Then python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db and confirm, by query on both databases, that the three rows are retired with retirement_ref equal to the heading and that GAP-379 carries the appended note. migration_reproducibility compares counts only and cannot see these UPDATEs, so compare the rows themselves.
9. Read back: python3 scripts/db.py lens-crosswalk --retired lists the three rows; select status from gaps where gap_id='GAP-379' prints OPEN.
10. Run scripts/preflight.sh once. If a research-batch rule is red only because this batch searched and admitted nothing, say so in the PR body (the carry-only convention, OD-84); do not move sessions/LATEST-RESEARCH. Run python3 scripts/preserve_transcripts.py and commit the scratchpad and transcripts (rule 6).
11. Commit as "governance: retire three e120 identity-need rows on owner answer D1 [YYYY-MM-DD HH:MM]" (time from date -u), with the attribution lines your harness requires. Push. Open ONE pull request containing only the ledger entry, the data migration, data/guidebook.db and the session logs. Call unsubscribe_pr_activity for it immediately (rule 9). Do not watch it.
Constraints: CLAUDE.md rule 0; population and need statements are the owner's (decision-protocol §2.4 item 2), and this executes the owner's answer only. Never write data/guidebook.db except through migrate_db.py; never hand-write SQL. No new machinery. No hand-typed counts. No tooling files in this PR (rule 10).
Return: the query output before and after, the ledger heading, the migration file name, the rebuild comparison, the preflight result and the PR link.
```

---

## Summary table

| Item | Decision | Recommended answer | Depends on |
|---|---|---|---|
| C4 (+C8) | One order of authority; the DR note; one answer to "what to do now" | A | none (carries B2's held-back routing half) |
| C1 | Record "Co-2 is co-primary with T2" and sweep the wording | a | edit the tier lines together with C2 and C7(b) |
| C2 | T3 gloss = lower-control primary, clinical or grey | a | C1 (same line) |
| C3 | Rule 9 enforcement sentence; three lower-case deny names | a | none |
| C5 | functional-taxonomy banner; re-point §9's entity-model row | a (add "axis retirement confirmed" if wanted) | none (B6 done) |
| C6 | Contract: keep `ratified: false`, fix the comment, apply the 2026-08-27 spine to the anchors | a | A3 (synthesis anchor), B6 (line shift) |
| C7 | "CANONICAL" population taxonomy label; three typical-type cells | both | C1 (T2 cell) |
| C8 | DR history note | merged into C4 | C4 |
| C9 | Two meanings of "thin" | a (two meanings) | A2 (marker line) |
| C10 | "Never population umbrellas" wording | a | C5 (axis wording) |
| D2 | OD-77: which mapping | A, or leave | none |
| D3 | OD-76 | moot | D4 = yes |
| D4 | SCI retires into WHEEL | yes | none |
| D5 | Frozen `decisions` table PENDING values | a (one sentence) | none |
| D6 | Columns open to hand correction | b | none |
| D7 | Working-rules file and size target | a (keep rules in CLAUDE.md) | E (proposal) follows it |
| D1 | Retire the e120 rows | answered: execute | separate data PR (rule 10) |

A one-line reply covering all of them, if you accept every recommendation: **"C4 A; C1 a; C2 a; C3 a; C5 a; C6 a; C7 both; C9 a; C10 a; D2 A; D3 moot; D4 yes; D5 a; D6 b; D7 a."**
