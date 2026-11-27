# Decision slate: items C and D, and the new questions from the remediation plan

Prepared 2026-11-27 (05:05 UTC). I only read the repository and the database: the database was opened read-only, and I edited, committed and applied nothing. I checked every quotation from the ledger against `references/project-standards.md` on `origin/main` at `b3b3e9b6`. The line numbers below are from that version; the ledger only grows at the end, so earlier line numbers do not move. I also re-ran every database figure today. The search strings that find each quotation are collected in the appendix at the end, so the cards themselves contain no code. Anything I could not check is marked [UNVERIFIED].

**How to answer.** Each card ends with a short reply. Paste one card's reply, several separated by semicolons, or the combined line in the reply card at the end.

---

## Terms used on the cards

- **The ledger.** The project's append-only record of your rulings (`references/project-standards.md`). A heading that begins "Owner" quotes your typed words. Text marked [ASSUMPTION] in an entry is the recorder's reading of your words, not your words.
- **Rule 0.** CLAUDE.md's rule that a live statement from you replaces every earlier record it touches, at once.
- **Owner-only decisions (DG-NON).** The ten kinds of decision listed in `governance/decision-protocol.md` section 2.4, which only you may make. Three matter here: item 2, population taxonomy (which groups of people have codes); item 3, evidence-tier definitions; and item 1, mission.
- **Delegated resolution.** A ruling an Opus-class model makes under one of your grants. It is recorded as "RESOLVED UNDER DELEGATION", never as your answer.
- **OD-79.** The recorded limit on your 2026-11-25 grant ("authority granted to opus to approve and ratify"). The grant covers approving the coordinator's work and deciding schema, method and ordering under methods you have already ruled. It does not cover population taxonomy, what a group of people needs, what you meant by your own words, or a database row that must point to an "Owner" ledger entry.
- **Tiers.** How strong a source is.
  - T1: primary controlled research.
  - Co-1: lived-experience and participatory research by disabled people. It ranks equal with T1 ("co-primary").
  - T2: syntheses of research (systematic reviews, and evidence-based standards from named organizations).
  - Co-2: clinical practice guidelines from occupational-therapy professional bodies.
  - T3: lower-control primary research, either clinical or "grey" (reports outside peer review).
  - T4 to T6: the regulatory stratum (international standards, national frameworks, statutory codes).
- **Markers.** Your table of 2026-11-14: ● for T1, T2, Co-1 and Co-2; ◐ for T3 and T4; ○ for T5 and T6. The warning triangle ⚠ replaces the circle when the basis is grey, unverified or thin.
- **Thin.** Your definition (2026-11-14): "when the evidence doesn't directly concern someone but is conjecture".
- **Provisional.** A computed state of a determination, meaning limited evidence. Your OD-10 answer glossed it as "thin evidence".
- **PROXY grade.** The population-match grade a source gets when it studied or addressed a group other than the one the determination is for, so it stands in for that group.
- **Umbrella test.** Your 2026-07-23 rule that an umbrella group code (such as MOB, "mobility") may be used only where its members do not need opposite things for the design point in question.
- **MOB, WHEEL, SCI, LMB.**
  - MOB: the mobility umbrella group.
  - WHEEL: wheelchair users. The code is not yet created.
  - SCI: spinal cord injury.
  - LMB: limb difference, which you moved out of mobility as UPL (upper limb).
- **Determination.** The project's computed answer for one design parameter and one group, for example "ramp gradient for wheelchair users: 5 % (1:20), marked ○".
- **OD-nn, T-nnn.** OD-nn is a numbered decision in the remediation plan's register. T-nnn is a numbered task in that plan.
- **DR-2026-08-19.** The decision record of 2026-08-19 that restarted research. It still claims to outrank CLAUDE.md.

## What has changed since the earlier prompts (check before answering)

1. **PR #249 is merged, not open.** You merged it at 04:32 UTC as `b3b3e9b6`. Both #248 (`1d52215d`) and #249 are on main, so every fix below goes in a new pull request.
2. **The ledger now holds your 2026-11-26 words** (lines 8642-8672): "Co-2 is co-primary with tier 2.", "approve A and B all; reject C4; D1 retire", and "C4 actually does point towards there needing to be one order of authority? why would we want multiple authorities". C1 therefore asks only whether to update the other documents to match.
3. **A merge counts as ratification, on your own words** (2026-07-24, lines 580-585): "always assume I Ratify if I merge it unless I explicitly note otherwise". Its limit (4) is that a merge does not supply an owner-only decision you never made.
4. **Ledger line 8209 is not your words.** It is the coordinator's record of a proposal; its own DATE line says so. Wherever a card below says "owner-only", the warrant is decision-protocol section 2.4 or prudence, not that line.
5. **The D1 retirement cannot run as the ledger currently instructs.** The retirement tool requires the cited "Owner" entry to name each row as TRIPLE-53, TRIPLE-57 and TRIPLE-61. The 2026-11-26 entry names none, and a scratch run of the tool refused it (`audit-session-work.md`, AU-02). See D1.
6. **T-039 was deleted on a false premise** (audit AU-01). It was the only task delivering your 2026-10-28 request "some kind of interface where I can manually review and edit the different table values/information". This is covered on card Q5.
7. **Two of your typed instructions are not yet in the ledger:**
   - "Opus to resolve conflicts like Q1 and others" (2026-11-27).
   - "please have Opus audit claude.md for saliency and efficacy. ensure we strip out all extraneous stuff like change logs and version discussion etc. we want to make sure that claude.md points correctly but also contains some strict rules of operation for us" (2026-11-26).

   I checked both against this session's transcript, which is not yet committed. They will be recorded with the next change, under rule 0.
8. **A separate Opus adjudication is coming.** The coordinator said it will run one on Q1 to Q5 and Q-B2 to Q-B5 after the PR B antagonists report. I have not seen its brief or its output [UNVERIFIED as to scope]. Each card in the last section says what that adjudication may rule on, so you are not asked the same thing twice.

---

# Part 1. C4 first: one order of authority

### C4 One order of authority (C8 merged in)   (who may decide: OWNER-ONLY. It settles which of your own records and rules wins over which. That is beyond OD-79, and DR-2026-08-19 is owner-ratified, DG-NON material.)

- **WHY IT IS ON THE LIST:** Four texts each claim to say which document wins, and three different answers exist to "what do I do now". A session can follow any of them and still be "right", so the inconsistency you asked us to remove stays.
- **CONTEXT:**
  - You rejected the first draft of this item.
  - You then asked: "C4 actually does point towards there needing to be one order of authority? why would we want multiple authorities" (ledger line 8658).
  - On 2026-11-25 you wrote: "as always refer to doctrine/mission/claude.md etc for guidance as required" (line 8485). This names doctrine and CLAUDE.md together, with no ranking between them.
  - On 2026-07-24 you made a merge count as ratification (line 585).
  - On 2026-11-14 you wrote "this newest plan having priority in conflicts" (line 7247), about two plans.

**Today's competing statements, side by side:**

| Statement | Where | Whose words |
|---|---|---|
| A live owner statement supersedes every earlier ratified record it touches, on contact | CLAUDE.md rule 0 (line 79) | CLAUDE.md text, ratified by your merges |
| Where CLAUDE.md disagrees with DR-2026-08-19, "that instrument wins", unless a live ruling of yours superseded it | CLAUDE.md lines 21-23 | CLAUDE.md text |
| The DR "supersedes all other planning documents"; CLAUDE.md is "a reference, not an instruction set" and the DR wins; a session reads exactly four documents | DR-2026-08-19, header, §A and §8 | DR you ratified 2026-08-19 |
| The DR's own §11 calls its ban on successor plans "SPENT", and its §12.1 runbook is marked "SUPERSEDED 2026-09-10" | same DR | same DR, which undercuts the row above |
| "What to do now": read the DR | CLAUDE.md §9 (line 539); the `/orient` command, item 1 | CLAUDE.md and command text |
| "What to do now": the remediation plan | your "i just want to get this remediation plan done asap" (line 8483) | your words; that "this plan" means the remediation-workplan file is the recorder's reading |
| Delegated rulings are made against doctrine, CLAUDE.md, the tier system, the decision protocol and the ledger | ledger line 8496, ACTION (4) | recorder applying your 2026-11-25 words |

**The proposed single order (Order A).** It replaces the second sentence of CLAUDE.md lines 21-23. Each clause is marked with what it rests on.

| Rank | Clause | Rests on |
|---|---|---|
| 1 | **Your words**, typed live or quoted word for word in the ledger, come first. | rule 0; your question of 2026-11-26. OWNER WORDS (your question) plus ratified CLAUDE.md text |
| 1 | A later statement of yours replaces every earlier record it touches. | rule 0. RATIFIED CLAUDE.md TEXT (no word-for-word quote of yours found) |
| 1 | A recorder's [ASSUMPTION], an ACTION line or a model's summary is not your words. | every owner entry's own ACTION ("treat the readings as unratified"). RECORDER PRACTICE |
| 1 | Your merge ratifies what it carries unless you say otherwise. It never supplies an owner-only decision you have not given in words. | ledger lines 580-585. OWNER WORDS |
| 2 | **Ratified records**, all at one rank: the doctrine in `governance/`, the ledger's RULE entries, the decision records in `decisions/`, and CLAUDE.md, each as amended by your later words. | "refer to doctrine/mission/claude.md etc" names them together. OWNER WORDS |
| 2 | Where two ratified records disagree on a point, the later ratification wins and the older text is corrected. | RECORDER'S READING (rule 0 extended to records) |
| 2 | Where it cannot be told which is later, ask you. | RECORDER'S READING |
| 3 | **Delegated resolutions**, made against rank 2 and within the grant's recorded reach. Never an owner-only decision. Never in place of an "Owner" entry the database requires. | your 2026-11-25 words; OD-79; decision-protocol §2.4. OWNER WORDS plus ratified doctrine |
| 4 | **Plans, task files, conventions and skills** bind only as they apply ranks 1-3. Between plans the newer wins. The active plan is the one the newest ledger entries name. | "this newest plan having priority in conflicts" (line 7247). OWNER WORDS for one fold; GENERALIZING TO ALL PLANS IS A READING |
| 5 | **Frozen records** (old sessions, transcripts, archives, superseded workplans, the old decisions table) are evidence of what was said and when, and bind nothing beyond the words of yours they quote. | DR header ("readable for provenance, binding on nothing"). RATIFIED DR TEXT |

**What Order A changes.**
- CLAUDE.md's "that instrument wins" sentence is replaced.
- CLAUDE.md §9's "What to do now" and "Latest rulings" rows merge into one row: run `/orient`, then read the newest ledger entries, which name the active plan.
- The `/orient` command drops its line sending sessions to the DR.
- The DR gains one dated note at its top saying that its claims to outrank everything are history. Nothing else in the DR is rewritten, and the note does not list "sections that still bind", because that would be an agent re-ratifying your DR. This is the former C8.
- One ledger entry records your answer.
- Ships as one governance pull request.

- **ANSWERS YOU CAN GIVE:**
  - **(A) Order A, as above.** Doctrine, CLAUDE.md, ledger RULEs and decision records rank together, and the later ratification wins on any point.
    I will then edit CLAUDE.md (one paragraph and one §9 row) and `.claude/commands/orient.md` (one line). I will append one note to the DR, with its attestation file, and append one ledger entry. I will also re-quote two state-graph atoms and sweep prose for "that instrument wins". One governance PR.
  - **(A-strict) Order A without the two recorder's readings.** Ranks as in A, but where two ratified records disagree you are always asked, and plans are not ranked by date except as you rule case by case.
    Same edits as A, but the two marked clauses are replaced by "ask the owner". You will be asked more often.
  - **(B) A fixed ranking by document type:** your words, then doctrine in `governance/`, then ledger RULEs, then DRs, then CLAUDE.md, then delegated resolutions, then plans, then frozen records.
    Same edits as A. It is predictable, but an old doctrine sentence beats a newer CLAUDE.md correction until someone edits the doctrine, and none of your words rank doctrine above CLAUDE.md.
  - **(Leave) Keep today's text.**
    No edits. The DR keeps claiming seniority over CLAUDE.md, `/orient` keeps sending sessions to a plan that is spent by its own §11, and three answers to "what to do now" remain. Not safe to leave: this is the inconsistency you asked us to remove.
- **MY RECOMMENDATION:** (A). Every placement except the "later wins" tie-break and the all-plans generalization rests on your words or on ratified text. Those two are marked for you to accept, and A-strict is the same order with them struck. [CONFIDENCE: medium-high]
- **REPLY WITH:**
  - (A): `C4 A`
  - (A-strict): `C4 A-strict`
  - (B): `C4 B`
  - (Leave): `C4 leave`

---

# Part 2. Items that bear on the first published determination

The first published determination is planned as "ramp gradient for wheelchair users". It needs the WHEEL code (task T-102), the correct marker (task T-117), and a page.

What these four items do to that path:
- **D4 is the only one that changes a one-way database act on the path.** T-102 can already run on the delegated ruling, so answering D4 makes that act yours rather than a delegate's.
- **D3 and D2 do not block the path.** They are housekeeping that reads as open.
- **C9 decides what the marker means for a provisional page.** It pairs with Q3.

### D4 SCI (spinal cord injury) retires into WHEEL (wheelchair users)   (who may decide: OWNER-ONLY in substance, because it is population taxonomy, §2.4 item 2. A delegate already ruled it (OD-83) under your "Opus to adjudicate all of the above", but that the grant reached SCI is itself the recorder's reading.)

- **WHY IT IS ON THE LIST:** Retiring a population code is one-way through the tools; undoing it needs a compensating migration. Today it rests on a delegated reading of your words, not on a word from you about it.
- **CONTEXT:**
  - On 2026-11-12 you wrote "except SCI is the same as WHEELCHAIR basically and LMB is the same as PROSTHETIC" (line 6115).
  - Your eighth-set heading reads "only SCI is the same as WHEEL" (line 6129).
  - On 2026-11-16 the recorder asked again, because an earlier acceptance had relied on the medical lens, which you deleted that day (GAP-111).
  - On 2026-11-25 OD-83 ruled, under delegation, that SCI retires into WHEEL (line 8608).
  - Database today: SCI is active, WHEEL does not exist, and GAP-111 is open.
- **ANSWERS YOU CAN GIVE:**
  - **(a) Yes, SCI retires into WHEEL.**
    I append "Owner answer 2026-11-27: SCI retires into WHEEL (OI-77; OD-83 confirmed)" to the ledger. T-102 then creates WHEEL, moves SCI's links, closes GAP-111 citing your entry, and retires SCI. The entry is in one governance PR, and the rows follow in T-102's own data PR.
  - **(b) No, keep SCI as its own code.**
    I record that OD-83 is reversed. WHEEL is still created, two codes then cover overlapping people, and OD-76's question of SCI's parent code comes back (D3).
  - **(Leave) Let the delegated ruling stand.**
    T-102 runs on OD-83. The retirement tool accepts the eighth-set heading, so nothing is blocked. Cost: a one-way change to who the book is about rests on a delegate's reading.
- **MY RECOMMENDATION:** (a). Your own words say it, and the 2026-11-16 concern was about where the injury level is recorded, not whether the two groups are one. [CONFIDENCE: high]
- **REPLY WITH:**
  - (a): `D4 yes`
  - (b): `D4 no`
  - (Leave): `D4 leave`

### D3 OD-76: the only decision in the register still referred back to you   (who may decide: OWNER-ONLY. Parent codes for SCI and LMB are population-taxonomy structure. Once D4 is answered it has nothing left to decide.)

- **WHY IT IS ON THE LIST:** OD-76 (put SCI and LMB under MOB, and add a tool for parent codes) was withdrawn because your 2026-11-12 answers overtook it, but its status still reads "referred back to the owner" (lines 8455-8457). Every count of open decisions shows it as open, though nothing waits on it.
- **CONTEXT:** It was withdrawn because LMB leaves mobility (eighth set, line 6129) and SCI goes with WHEEL. The plan's register says it "Releases: nothing" [carried from the earlier prompts; register line not re-read today].
- **ANSWERS YOU CAN GIVE:**
  - **(a) Moot.**
    I add one line to the same ledger entry as D4 marking OD-76 answered: no parent codes for SCI or LMB, and no parent tool. One governance PR, together with D4.
  - **(Leave).**
    No cost to any task. It keeps reading as open.
- **MY RECOMMENDATION:** (a), provided D4 is "yes". If D4 is "no", leave it, because SCI's parent code becomes a real question. [CONFIDENCE: high]
- **REPLY WITH:**
  - (a): `D3 moot`
  - (Leave): `D3 leave`

### D2 OD-77: which "mapping" did you doubt?   (who may decide: OWNER-ONLY. What you meant by your own words is outside every grant, per OD-79.)

- **WHY IT IS ON THE LIST:** On 2026-11-22 you wrote "I don't think the mapping is correct" (line 8407), and two tables could be "the mapping". A delegate chose one (line 8596), but your meaning is yours to give.
- **CONTEXT:**
  - Earlier that day you complained of "entire groups like b750 to b789" (line 8401).
  - Candidate (A) is the identity-to-ICF list (`identity_icf_map`). It is the only ICF link table that holds range codes like b750-b789: 11 range rows there today, none in the other two tables.
  - Candidate (B) is the identity-need-ICF rows added in pull request 245.
  - The delegate took (A) and froze additions to it. T-128 was withdrawn (OD-87).
  - Nothing on the path to the first page reads either table (OD-85).
- **ANSWERS YOU CAN GIVE:**
  - **(A) I meant the identity-to-ICF list.**
    I append one ledger entry making OD-77 your answer. No data or task changes. One governance PR.
  - **(B) I meant the PR-245 identity-need-ICF rows.**
    I append the entry and list those rows for your review. The freeze moves to them, and the freeze on the identity-to-ICF list can be reconsidered. Cost: one review pass by you.
  - **(Leave).**
    No cost now. The delegated reading stands until you speak.
- **MY RECOMMENDATION:** Answer (A) only if it matches what you meant; the range-code evidence points there. If you are unsure, leave it, because nothing waits on it. [CONFIDENCE: medium]
- **REPLY WITH:**
  - (A): `D2 A`
  - (B): `D2 B`
  - (Leave): `D2 leave`

### C9 Two meanings of "thin"   (who may decide: OWNER-ONLY. It is what a marker means, under §2.4 item 3. `governance/tier-system.md` §5 lists it as "Not yet ruled (owner)", line 80.)

- **WHY IT IS ON THE LIST:** Your OD-10 answer glossed "provisional" as "thin evidence" (line 5980), and on 2026-11-14 you made "thin" a cause of ⚠ (lines 7071, 7087). If the two are the same, every provisional determination takes ⚠, which collides with "T4 only half circle" (line 7195).
- **CONTEXT:**
  - Your definition of thin: "I think thin is when the evidence doesn't directly concern someone but is conjecture" (line 7087). That is about directness.
  - Provisional is computed from strength: for example, a cell resting only on codes.
  - The first planned page is provisional. Under reading (b) below it would be marked ⚠ whatever its sources.
- **ANSWERS YOU CAN GIVE:**
  - **(a) Two meanings.** "Provisional" means limited strength; ⚠-thin means the evidence does not directly concern the people served and is conjecture.
    I append one ledger entry and reword the places that gloss provisional as "thin evidence" to "limited evidence strength". OD-10's recorded words stay untouched. One governance PR.
  - **(b) One meaning.** Every provisional cell takes ⚠.
    I stop and bring you the conflicting rules ("T4 only half circle"; code-only cells stay provisional) to say which yields. The marker code (T-117) changes.
  - **(Leave).**
    The two meanings stay. T-117 is built without treating provisional as thin, and tier-system §5 keeps it under "Not yet ruled".
- **MY RECOMMENDATION:** (a). Your 2026-11-14 definition is about directness and OD-10's is about strength, and (b) contradicts a later ruling of yours. [CONFIDENCE: high]
- **REPLY WITH:**
  - (a): `C9 a`
  - (b): `C9 b`
  - (Leave): `C9 leave`

---

# Part 3. The rest of C and D

### C1 Bring every document in line with "Co-2 is co-primary with tier 2"   (who may decide: OWNER-ONLY. Evidence-tier definitions are §2.4 item 3, and the 2026-11-26 ledger entry's ACTION (4) holds the update for your approval.)

- **WHY IT IS ON THE LIST:** Your statement is now recorded (line 8654), but several documents still call Co-2 "parallel" to T2 or leave it out, and the owner-only list in decision-protocol §2.4 item 3 reads "(1–6 + Co-1)", omitting Co-2. Sessions meet two descriptions of the same tier.
- **CONTEXT:**
  - The ledger's core RULE already says "Co-2 = OT professional body CPGs (co-primary with Tier 2)" (line 17).
  - You also said "Co-1 stays full, Co-2 full too" (line 6989).
  - Places that still say "parallel" or omit it:
    - `governance/tier-system.md`: line 11, and the T2 row ("occasionally co2");
    - `governance/mission-and-epistemics.md` line 93;
    - `governance/evidence-methodology.md` line 49;
    - two descriptive comments in `schemas/enums.py`;
    - `governance/owner-browser.yaml` line 107;
    - CLAUDE.md line 367;
    - decision-protocol line 77.
  - No code depends on the wording, and the database holds no Co-2 sources today.
  - The audit asked whether rule 0 makes your statement bind now without this update (AU-19). The ledger entry already tells every session to treat Co-2 as co-primary, so the open part is the documents.
- **ANSWERS YOU CAN GIVE:**
  - **(a) Update every document.**
    I edit the places above to say "co-primary with T2" and change decision-protocol to "(1–6, Co-1 and Co-2)". I do this in the same pass as C2 and C7(b) so each tier line is edited once. One governance PR, with descriptive comments only in `schemas/enums.py`.
  - **(b) Update decision-protocol §2.4 only.**
    One line. The "parallel" wording stays elsewhere, and the ledger entry still governs.
  - **(Leave).**
    Safe for the book: no code or data depends on it. The documents keep disagreeing with your words.
- **MY RECOMMENDATION:** (a). It matches a ratified RULE and your words, and closes the §2.4 omission. It does not change how a Co-2 source and a T2 source are weighed against each other; that is left open. [CONFIDENCE: high]
- **REPLY WITH:**
  - (a): `C1 a`
  - (b): `C1 b`
  - (Leave): `C1 leave`

### C2 Correct the one-line description of T3   (who may decide: OWNER-ONLY by §2.4 item 3, although the edit only brings a summary into line with the ratified definition.)

- **WHY IT IS ON THE LIST:** CLAUDE.md (line 367) calls T3 "grey primary", and `owner-browser.yaml` (line 107) says "T3 is grey primary work". The ratified definition (`tier-system.md`, T3 row) and the tier code both include lower-control clinical research. Calling all T3 "grey" invites a ⚠ on clinical research that should carry ◐.
- **CONTEXT:**
  - Your words of 2026-11-06: "if government report is academically sound then it can be t3 I think" (line 4928).
  - Your 2026-11-14 marker answers give non-grey T3 the half circle and every grey basis the triangle (OD-64, "2 triangle for all", line 7401).
- **ANSWERS YOU CAN GIVE:**
  - **(a) Correct both phrases** to "lower-control primary (clinical or grey)".
    Two phrase edits, made together with C1. One governance PR. The words "T4–T6 the regulatory stratum" stay, because a test reads them.
  - **(b) Replace CLAUDE.md's tier summary with a pointer** to `tier-system.md` §1, and correct the owner-browser phrase.
    A larger edit. One home for the definition.
  - **(Leave).**
    The summaries keep misstating T3. Risk: a wrong ⚠ on clinical T3 once T-117 lands.
- **MY RECOMMENDATION:** (a). [CONFIDENCE: high]
- **REPLY WITH:**
  - (a): `C2 a`
  - (b): `C2 b`
  - (Leave): `C2 leave`

### C3 Rule 9 (do not watch pull requests): a stale sentence and three tool names   (who may decide: the sentence could be delegated, because it is a factual correction of rule text you approved. The settings change is yours alone: a session may not change its own permission settings.)

- **WHY IT IS ON THE LIST:** Rule 9's enforcement sentence (CLAUDE.md line 207) says it is "PARTLY ENFORCED once the owner adds" four tools to the deny list. You have already added them (`.claude/settings.json` lines 43-46). This cloud session, though, names the same tools in lower case with hyphens (for example `mcp__claude-code-remote__send_later`), and your entries use `Claude_Code_Remote`.
- **CONTEXT:** I confirmed the lower-case names from this session's own tool list. Whether the deny list treats the two spellings as the same is [UNVERIFIED]; testing it would mean calling a tool rule 9 forbids. Your 2026-09-23 instruction behind rule 9 is not quoted word for word in the ledger. It is recorded in `workplan/2026-09-23-pr-audit-resolution.md` [carried from the earlier prompts].
- **ANSWERS YOU CAN GIVE:**
  - **(a) Both.**
    I reword the sentence to say the deny list stops subscription and polling only if its names match the tools the session shows, and that the unsubscribe step stays the session's job. You add the three lower-case names to the deny list yourself. One governance PR for the sentence.
  - **(b) Sentence only.**
    The sentence is corrected. A name gap, if it is real, stays.
  - **(Leave).**
    Harmless to the book. The sentence keeps describing a step already taken.
- **MY RECOMMENDATION:** (a). [CONFIDENCE: high that the sentence is stale; medium that the names really mismatch]
- **REPLY WITH:**
  - (a): `C3 a`
  - (b): `C3 b`
  - (Leave): `C3 leave`

### C5 Mark the axis-based parts of `functional-taxonomy.md` as history   (who may decide: OWNER-ONLY. It is ratified doctrine about population structure, §2.4 item 2. A delegate already retired the axis layer (R35), and option (c) makes that retirement yours.)

- **WHY IT IS ON THE LIST:** `governance/functional-taxonomy.md` still presents itself as a ratified, operative "Two-Layer Model (Axes × Profiles)", but the database has no axis tables. CLAUDE.md §9 (line 543) still sends sessions to it for the "Entity model, ICF frame".
- **CONTEXT:**
  - Your words: "I don't want axis to be used" (2026-08-24, line 810), and "'AX-' for ICF should never ever exist anywhere" (2026-09-13, line 3399).
  - On 2026-08-25 you renamed the layer rather than deleting it.
  - The retirement itself was a delegated ruling (R35, `workplan/pipeline-state-graph/RULINGS.md`). Migration 109 then dropped the tables.
  - The live frame is three lenses (identity, ICF, access need), CLAUDE.md §6.
  - Which sections survive is the earlier antagonists' reading, which I checked only against the file's numbering [partly UNVERIFIED].
- **ANSWERS YOU CAN GIVE:**
  - **(a) Banner, and re-point the §9 row.**
    I insert one dated paragraph under the file's status line naming the parts that are history and the parts that are not. I replace the §9 row with "the schema: read it from the database" and "ICF codes and the three lenses: §6 and the ICF glossary". One governance PR.
  - **(b) Banner only.**
    CLAUDE.md keeps sending sessions to a file built on a deleted layer.
  - **(c) As (a), and you say "axis retirement confirmed".**
    The same edits plus one ledger entry. R35 becomes your ruling.
  - **(Leave).**
    Sessions keep reading a retired model as operative. A risk of wrong framing, not of wrong figures.
- **MY RECOMMENDATION:** (a). Choose (c) if you want the retirement on your own authority. The tables are gone and the word is already banned, so (c) costs one sentence from you. [CONFIDENCE: high for the banner; medium for the exact list of surviving sections]
- **REPLY WITH:**
  - (a): `C5 a`
  - (b): `C5 b`
  - (c): `C5 c`
  - (Leave): `C5 leave`

### C6 The pipeline contract: `ratified: false`, and the stage descriptions   (who may decide: ratifying the contract (OD-17) is yours alone. Bringing the stage descriptions into line with your own 2026-08-27 sentence could be delegated as method, but the contract itself calls it "an OPEN POINT for the owner".)

- **WHY IT IS ON THE LIST:** `governance/pipeline-contract.yaml` reads `ratified: false`, with a comment giving reasons that no longer apply. Its descriptions of the judgment and specification stages contradict your 2026-08-27 sentence: "you research slugs, evidence research, judge evidence, synthesize judgments, specify syntheses, and render specifications" (line 1454).
- **CONTEXT:**
  - On 2026-11-12 you deferred OD-17: "Ratify after T-022 merges, once I have read the corrected contract" (line 6066).
  - On 2026-11-19, "Ratify all" was read as including OD-17, but the recorder noted you had not been shown the contract.
  - The judgment stage's description currently includes the determination machine and convergence. The contract's own note puts those in specification and synthesis.
  - Nothing reads the field: one audit script only prints it.
- **ANSWERS YOU CAN GIVE:**
  - **(a) Keep `ratified: false`, fix the comment, apply your 2026-08-27 sentence to the two stage descriptions.**
    One governance PR: the header comment, two descriptions, and deletion of the two notes those descriptions settle.
  - **(b) Ratify now, and apply the sentence.**
    The same edits plus `ratified: true` and a ledger entry. This waives your own condition that you read the contract first.
  - **(c) Comment only.**
    The stage descriptions keep contradicting your sentence.
  - **(Leave).**
    Harmless to the book today. The contract stays inconsistent with your spine sentence.
- **MY RECOMMENDATION:** (a). It costs you no reading now, and the description edit only carries out your own words. [CONFIDENCE: medium-high]
- **REPLY WITH:**
  - (a): `C6 a`
  - (b): `C6 b`
  - (c): `C6 c`
  - (Leave): `C6 leave`

### C7 Two stale doctrine statements   (who may decide: part (a) could be delegated, because it only corrects a label to match the target file's own "SUPERSEDED" status and decides no taxonomy. Part (b) is OWNER-ONLY, because it edits the tier table, §2.4 item 3.)

- **WHY IT IS ON THE LIST:**
  - (a) `governance/held-tensions.md` calls `population-taxonomy.md` "(CANONICAL)" at line 20 and in its table, but that file marks itself superseded.
  - (b) Three "typical source type" cells in `tier-system.md` §1 disagree with the code that assigns tiers.
  - Sessions read a superseded file as canonical, and a tier table the code contradicts.
- **CONTEXT:** The three cells:
  - The T1 row says "occasionally grey", but grey always becomes T3. Your "if government report is academically sound then it can be t3" (line 4928) agrees with the code.
  - The T3 row mentions national evidence-based standards, but those become T2 or T4.
  - The T5 row lists evidence-based standards, but T5 is national frameworks only.
- **ANSWERS YOU CAN GIVE:**
  - **(both) Correct (a) and (b).**
    Two labels in held-tensions.md, and three cells plus one pointer sentence in tier-system.md, done in the same pass as C1. One governance PR.
  - **(a only).**
    The labels are fixed. The tier cells keep contradicting the code.
  - **(b only).**
    The reverse.
  - **(Leave).**
    No wrong figure reaches the book. The doctrine keeps misdescribing itself.
- **MY RECOMMENDATION:** both. [CONFIDENCE: high for (a); medium-high for (b), because the cells say "typical" and the code is the rule]
- **REPLY WITH:**
  - (both): `C7 both`
  - (a only): `C7 a`
  - (b only): `C7 b`
  - (Leave): `C7 leave`

### C10 "Never population umbrellas" in CLAUDE.md   (who may decide: OWNER-ONLY. It is population taxonomy, §2.4 item 2.)

- **WHY IT IS ON THE LIST:** CLAUDE.md §6 (line 376) says "never bare axis codes, never population umbrellas". You have since allowed umbrellas in two rulings, and "axis" names a deleted layer. CLAUDE.md forbids what you permitted.
- **CONTEXT:**
  - The 2026-07-22 RULE "Work from axes — no armchair umbrellas" (line 561) was amended on 2026-07-23 by your design-equivalence exception: "brain and complex are literally TOO complex to avoid umbrellas" (line 570). That exception is the umbrella test.
  - On 2026-11-21 you answered "3 to umbrella and to specific, yes" (line 8290).
  - You also said "use advocacy groups and disability ethics as a lens for grouping/sorting/taxonomy" (line 5931).
- **ANSWERS YOU CAN GIVE:**
  - **(a) Narrow the wording** to: never bare codes, and never an umbrella group no ruling admits (citing the 2026-07-23 test and your 2026-11-21 answer).
    One phrase in CLAUDE.md §6. One governance PR.
  - **(b) Delete "never population umbrellas"** and keep "never bare codes".
    Shorter, but it loses the guard against invented umbrellas that the 2026-07-22 RULE still holds.
  - **(Leave).**
    CLAUDE.md keeps contradicting your rulings.
- **MY RECOMMENDATION:** (a). It keeps the guard and admits what you ruled. [CONFIDENCE: high]
- **REPLY WITH:**
  - (a): `C10 a`
  - (b): `C10 b`
  - (Leave): `C10 leave`

### D5 Stale "PENDING" marks in the old decisions table   (who may decide: could be delegated. The delegated ruling R30 already froze the table and left the protocol wording to "owner merge", and under your 2026-07-24 rule your merge of the PR ratifies it.)

- **WHY IT IS ON THE LIST:** The old decisions table (last entry D-0188, 2026-09-11) shows 24 rows as PENDING, including D-0184, which CLAUDE.md treats as settled. No document says the table's status columns are no longer kept up, so a session may read PENDING as open.
- **CONTEXT:**
  - Your 2026-09-11 entry says "Cite D-0184 for the lens mechanism" (line 2898).
  - Your OR-1 answer is recorded as "D-0184 stands" (line 4630; the recorder's reading of your "yes").
  - R30 (a delegated ruling): "Retire both stores; table frozen as infrastructure residual; ledger the single home".
- **ANSWERS YOU CAN GIVE:**
  - **(a) One sentence in `governance/decision-protocol.md` §0:** the decisions table is frozen, its status columns are not maintained, and the ledger is the single home of decisions.
    One governance PR, with no database change.
  - **(b) Update the rows by migration.**
    Writes to a frozen table that nothing reads. Not recommended.
  - **(Leave).**
    Low risk. Sessions may misread PENDING.
- **MY RECOMMENDATION:** (a). Leaving it is acceptable if you would rather add no text. [CONFIDENCE: medium]
- **REPLY WITH:**
  - (a): `D5 a`
  - (b): `D5 b`
  - (Leave): `D5 leave`

### D6 Which database columns may a session correct by hand?   (who may decide: OWNER-ONLY. It is what you meant by "specific columns", which is outside every grant per OD-79.)

- **WHY IT IS ON THE LIST:** On 2026-11-21 you wrote "I think GAP-368 points towards Claude having permission to hand edit as required for specific columns" and "We don't need a tool for many qualitative judgments/corrections because Claude IS a tool. We just need to ensure that you make transparent and record your hand fixes" (lines 8269-8271). CLAUDE.md §4 and rule 10 still forbid hand-written database edits, and the recorder's reading ("qualitative judgment or wording") would wrongly admit verbatim source quotations.
- **CONTEXT:**
  - The ledger entry's ACTION (2) says to ask you before extending the permission to any column.
  - GAP-368 is open.
  - Verbatim source text (the stored quotation of a figure) must never be changed by hand, under CLAUDE.md's first rule: fetch before you write.
- **ANSWERS YOU CAN GIVE:**
  - **(a) Only the value cells of qualitative figures**, the GAP-368 case. Narrowest.
    I write the ledger entry and add one exception sentence to CLAUDE.md §4 and one cross-reference in rule 10. One governance PR.
  - **(b) Any cell holding a qualitative judgment a session wrote:** the value of a qualitative figure, a warrant, a note, a rationale or a review note. Never identifiers, keys, vocabulary codes, numbers, units, author, title, year, verbatim source text, or your quoted words. Each fix records the old value, the new value, the reason and the session.
    The same edits as (a), with this wider scope.
  - **(c) You name the table and column pairs.**
    I wait for your list.
  - **(Leave).**
    GAP-368 stays open, and hand fixes stay forbidden.
- **MY RECOMMENDATION:** (b). It matches "many qualitative judgments/corrections", spares you a column list, and adds the one exclusion the recorder's reading missed. [CONFIDENCE: medium]
- **REPLY WITH:**
  - (a): `D6 a`
  - (b): `D6 b`
  - (c): `D6 c`
  - (Leave): `D6 leave`

### D7 Keep all rules in CLAUDE.md, or move some to a separate file with a size target?   (who may decide: OWNER-ONLY. The 2026-11-20 proposal's own ACTION (1) says CLAUDE.md is not rewritten until you approve.)

- **WHY IT IS ON THE LIST:** A coordinator proposal recorded on 2026-11-20 (not your words; its DATE line says so) would move several rules and sections into a separate "working-rules file" and cut CLAUDE.md to a quarter of its words. Until you answer, that ACTION blocks any rewrite of CLAUDE.md, including the trimming you asked for on 2026-11-26.
- **CONTEXT:**
  - Your 2026-11-20 words: "overall we need to make this project as simple as possible in infrastructure because the more exceptions we have the more complexity we guard against which is the more we spiral" (line 8192).
  - On 2026-11-26 you asked that CLAUDE.md "points correctly but also contains some strict rules of operation for us" (transcript; not yet in the ledger).
  - The audit found the quarter target unreachable while owner-reserved text stays in CLAUDE.md.
- **ANSWERS YOU CAN GIVE:**
  - **(a) Keep the rules in CLAUDE.md; no working-rules file; no size target.** Cut only history, proofs and stale claims.
    I append one ledger entry, which also records your 2026-11-26 "strict rules" words. Later trimming follows the corrected CLAUDE.md proposal (item E).
  - **(b) Approve the separate rules file and the size target.**
    One tooling PR, a new file every session must be pointed to, and a sweep of every place that cites a rule number.
  - **(Leave).**
    ACTION (1) keeps blocking any CLAUDE.md rewrite.
- **MY RECOMMENDATION:** (a). Your 2026-11-26 words ask CLAUDE.md itself to carry the strict rules, and a second rules file is more machinery. [CONFIDENCE: medium-high]
- **REPLY WITH:**
  - (a): `D7 a`
  - (b): `D7 b`
  - (Leave): `D7 leave`

### D1 Retire the three body-size rows on mobility products (e120): ANSWERED   (decided by you: "D1 retire", 2026-11-26, line 8656)

- **STATUS:** Answered. The rows are 53 (little people, LPA), 57 (tall people, TALL) and 61 (people in larger bodies, BAR). Each ties the need "fit the range of bodies" (A-SIZE) to ICF e120 (mobility products and technology). All three are still pending and not retired, as of today. Each group keeps its other A-SIZE rows.
- **WHAT HAPPENS NEXT (no answer needed from you):**
  1. The retirement tool requires the "Owner" entry it cites to name the rows as TRIPLE-53, TRIPLE-57 and TRIPLE-61. The 2026-11-26 entry does not, and the tool refused it on a scratch copy (audit AU-02). So one more ledger entry is appended, headed "Owner answer 2026-11-26 —", which quotes your "D1 retire", names the three rows, and points back to the earlier entry. It does not edit the earlier entry.
  2. The rows are retired through the sanctioned tool and a data migration, in a small data PR of their own (rule 10).
  3. GAP-379 gets a dated note and stays open, because the A-TRIGGER rows on epilepsy (EPI) and communication (COM) remain unreviewed.
- **REPLY WITH:** nothing needed. If you want the second entry worded differently, say so.

---

# Part 4. New questions from the remediation plan

For each question, one of three things is true: the ledger already answers it, it is a sequencing or method choice Opus may make under OD-79, or it is yours alone. "Opus adjudication" marks the questions the coordinator's separate Opus adjudication is also taking up, per its message of 2026-11-27 [scope UNVERIFIED]. Where a question is yours, the adjudication should only frame it, not rule it.

### Q1 May the first page leave out the minimum, mode, median and maximum (OD-63)?   (who may decide: OWNER-ONLY. Relaxing your own answered ruling is your meaning to give. Opus adjudication: may only confirm the default, which is not to relax it.)

- **WHY IT IS ON THE LIST:** You ruled that the render page shows the minimum, mode, median and maximum, colour-coding the surveyed code bodies (OD-63). Producing those four figures correctly adds five or six tasks before the first page:
  - T-124 and T-036: the figures and the jurisdiction comparison;
  - T-108, T-086 and T-111: units, ratios and spelled-out numbers;
  - T-113: sub-national codes.

  Done badly, they would print wrong figures. For example, two instruments are counted twice today (GAP-376).
- **CONTEXT:**
  - Your words: "all values when synthesizing and making determinations, but on the render page itself, we just have the minimum, mode, median and maximum colour coding the jurisdiction code bodies that we surveyed for comparison purposes" (line 7399, fifteenth set).
  - You also wrote "i just want to get this remediation plan done asap" (line 8483).
- **ANSWERS YOU CAN GIVE:**
  - **(a) Keep OD-63 for the first page.**
    T-124, T-036, T-108, T-086, T-111 and T-113 (widened to the two missed sub-national sources) go on the path before the page.
  - **(b) Relax it for the first page only.** The page shows the stated value, its marker and every source, plus a visible line saying the four figures are not yet shown and why. OD-63 applies from the second page, or once those tasks land.
    I record your answer in the ledger. The page is built without the figures, and those tasks are scheduled after it.
  - **(c) Relax it permanently.**
    I record a change to OD-63. Not recommended: it reverses a transparency ruling.
- **MY RECOMMENDATION:** (b). It keeps your transparency rule visible on the page and keeps wrong comparison figures out of the book until the unit and duplicate defects are fixed. It is still a relaxation of your own ruling, which is why it is on the "do not simply accept" line. [CONFIDENCE: medium]
- **REPLY WITH:**
  - (a): `Q1 keep`
  - (b): `Q1 first-page`
  - (c): `Q1 drop`

### Q2 Does ramp gradient at the mobility umbrella (MOB) pass the umbrella test?   (who may decide: ALREADY ANSWERED by the ledger. Not a question. The Opus adjudication was told the same.)

- **WHY IT IS ON THE LIST:** If MOB passed, the first page could skip creating WHEEL (task T-102).
- **CONTEXT:**
  - Your ruling of 2026-08-25: "As to 'mobility', separate out into 'ambulatory' and 'wheelchair user' to start", marked "not to be relitigated" (line 1185).
  - The same entry records that MOB fails the test for ramp gradient: "Ramp gradient is opposed between its members" (lines 1191-1197). That analysis is the recorder's, but the split it supports is yours.
  - Your 2026-11-12 answer (OD-14): "Decompose MOB by device to wheelchair user, prosthetic device user, other mobility aids" (line 6019).
- **ANSWERS YOU CAN GIVE:** none needed. The route is WHEEL (T-102). Reopening it would mean relitigating a ruling you closed.
- **MY RECOMMENDATION:** treat it as answered. [CONFIDENCE: high]
- **REPLY WITH:** nothing, or `Q2 answered` to confirm.

### Q3 Does a PROXY population-match grade make a value "thin" (⚠)?   (who may decide: OWNER-ONLY. `tier-system.md` §5 line 80 lists it as "Not yet ruled (owner)", and your 2026-11-14 entry on thin says it "does not decide" this. Opus adjudication: frame only.)

- **WHY IT IS ON THE LIST:** It decides whether the first page shows ○ or ⚠. The ramp-gradient value (5 %, 1:20) is stated word for word by verified codes from England and Flanders, but some of its sources are graded PROXY. The marker code (T-117) is being built without this rule until you answer.
- **CONTEXT:**
  - Your definition: "I think thin is when the evidence doesn't directly concern someone but is conjecture" (line 7087).
  - You ruled the project's own inferences conjecture (entry at line 7119, words at 7123), and a value that mixes a finding with an inference "conjecture because we don't have authority" (line 7159).
  - Both PR B antagonists flagged one problem: reading every PROXY grade as thin would make a cell's marker worse when more research is added.
- **ANSWERS YOU CAN GIVE:**
  - **(a) No. Thin only when the step across groups is conjecture:** the project's own inference, or a mixed value. A source that itself states the value for a wider group that includes the people served is not thin.
    I record your answer in the ledger. T-117 derives ⚠ from the inference and mixed-value records only.
  - **(b) Yes. Every PROXY-graded basis is thin and takes ⚠.**
    I record it. T-117 marks any value resting on a PROXY grade with ⚠, and the first page shows ⚠.
  - **(Leave).**
    T-117 ships without the rule, the first page shows ○ if its other rules give ○, and tier-system keeps it as "Not yet ruled".
- **MY RECOMMENDATION:** (a). Your definition has two parts ("doesn't directly concern someone" and "is conjecture"), and a code that states the value for all disabled people is not the project's conjecture. [CONFIDENCE: medium-low; this is close to your own judgment of what "conjecture" covers]
- **REPLY WITH:**
  - (a): `Q3 no`
  - (b): `Q3 yes`
  - (Leave): `Q3 leave`

### Q4 Which cell first: ramp gradient (parameter 3) or ramp run length (parameter 12)?   (who may decide: a sequencing choice, which Opus may rule under OD-79. The Opus adjudication is ruling it. One branch is yours: keying parameter 12 on MOB without creating WHEEL would need an umbrella-test judgment for run length, which is population taxonomy.)

- **WHY IT IS ON THE LIST:** Parameter 3 has far more evidence, including four Co-1 sources and sixteen T1 or T2 sources, but more defects: six unverified governing sources, unit cells with sentences in them, and truncated quotations. Parameter 12 has one unverified governing source, readable units and no grey-source gap, but less evidence. Nobody has yet weighed them against each other.
- **CONTEXT:** Under the WHEEL route, both cells need T-102's moves first. Whether a "run length for wheelchair users" cell holds enough figures after those moves is not measured [UNVERIFIED]. The same is true of ramp gradient.
- **ANSWERS YOU CAN GIVE:**
  - **(Opus) Let the adjudication choose.** It chooses on the evidence once T-102's moves show which wheelchair-user cell has a value.
    The adjudication's ruling is logged as delegated.
  - **(3) Parameter 3 first.** The richest demonstration, and the longer repair list.
  - **(12) Parameter 12 first.** Fewer repairs, and the four OD-63 figures need no unit cleanup. Parameter 3 follows.
- **MY RECOMMENDATION:** (Opus). It is ordering, which your grant covers. My own lean is parameter 12, for fewer defects. [CONFIDENCE: medium-low]
- **REPLY WITH:**
  - (Opus): `Q4 Opus`
  - (3): `Q4 3`
  - (12): `Q4 12`

### Q5 Six tasks that would undo something you asked for or ratified, and T-039   (who may decide: OWNER-ONLY. Withdrawing a request or ratification of yours is beyond OD-79. Restoring T-039 is delegable. Opus adjudication: frame only.)

- **WHY IT IS ON THE LIST:**
  - T-129 and T-130 trace to your question "is there an iterative loop with limited repetitions".
  - T-139, T-140 and T-141 trace to items you ratified with "Sure, append. Ratify all."; that this covers those items is the recorder's reading.
  - T-070 is the blind double-extraction task you launched by "apply recommendations".
  - The classifiers called all six apparatus, but deleting them would reverse your acts. Meanwhile the regenerated plan marks several of them READY (audit AU-05), so an executor could start one.
  - T-039, your 2026-10-28 request to "manually review and edit the different table values/information", was deleted in PR #249 on a false premise (AU-01).
- **CONTEXT:** You wrote "Remember that this project is simple!!!" (line 8551), and CLAUDE.md §8 lets code be deleted on evidence. A task you asked for by name is not code, though.
- **ANSWERS YOU CAN GIVE:**
  - **(a) Defer all six, and restore T-039 as deferred.** Keep the files, mark them "deferred: do not start", and restore the T-039 file from git history.
    One governance PR: a stop line in seven task files, the plan regenerated.
  - **(b) Retire all six, and drop the T-039 request.** You withdraw these asks.
    I record a ledger entry quoting your answer, delete the six files, and leave T-039 deleted.
  - **(c) Keep them live as they are.**
    No edit. They stay READY in the plan.
  - **(d) Per task.** Name each one, for example "Q5 retire T-130, defer the rest".
    I follow your list.
- **MY RECOMMENDATION:** (a). It does not reverse anything you asked for, stops an executor building them now, and puts back the only task that delivers your edit request. [CONFIDENCE: medium-high]
- **REPLY WITH:**
  - (a): `Q5 defer`
  - (b): `Q5 retire`
  - (c): `Q5 keep`
  - (d): `Q5 ` followed by your list

### Q-B2 When several sources state the shown value with different markers, which marker does the value carry?   (who may decide: OWNER-ONLY. It is what a marker means, an extension of your OD-59 "yes" to a case OD-59 did not cover. Opus adjudication: frame only.)

- **WHY IT IS ON THE LIST:** OD-59 (line 7334) gave a value "the grade of its own source", which settles the case of one source. When two sources state the same value, say a verified code (○) and an unverified standard (would be ⚠), nothing is ruled. The PR B design makes the engine refuse such a cell until you answer. That does not fire on parameters 3 or 12 today.
- **CONTEXT:** Your words: "no, triangle instead if the value is coming from grey or unverified" (line 7053), and "let's return to keeping them but they get a triangle warning" (line 7005).
- **ANSWERS YOU CAN GIVE:**
  - **(a) The strongest marker among the stating sources that are verified and not grey.** ⚠ only when every stating source is grey or unverified. Every source still shows its own marker beside it.
    I record your answer in the ledger, and T-117's refusal becomes this rule.
  - **(b) The weakest marker among the stating sources** (the cautious reading).
    I record it, and T-117 takes the minimum.
  - **(Leave).**
    The engine refuses such a cell and names the question. There is no live effect today.
- **MY RECOMMENDATION:** (a). If a verified, non-grey source states the value, the value is not "coming from grey or unverified". [CONFIDENCE: medium]
- **REPLY WITH:**
  - (a): `QB2 a`
  - (b): `QB2 b`
  - (Leave): `QB2 leave`

### Q-B3 Do Co-1, T3 grey and T2 national evidence-based standards count under the OD-58 harm test?   (who may decide: OWNER-ONLY. It is what your words "research publication or clinical guidelines" cover, and the ledger records that "Whether Co-1 statements count under OD-58" is not decided. Opus adjudication: frame only.)

- **WHY IT IS ON THE LIST:** Your harm test decides when research overrides the most accommodating value. The PR B design counts clinical research, systematic reviews and Co-2 guidelines, and makes the engine refuse a cell if a Co-1, T3 grey or T2 national-standard statement would change the value. Leaving Co-1 out of a test about who struggles at a value risks the failure this project ranks worst: leaving out disabled people's own evidence.
- **CONTEXT:**
  - Your OD-58 words: "research publication or clinical guidelines state that a person with disability struggles more or has more difficulties or some kind of negative statement with a parameter being at a certain value compared to the one it proposes" (line 7305).
  - Your harm test: "does the research prove that the more accommodating value leads to worse results? if so, research wins. if no, code wins" (line 7177).
  - No live cell is affected: the one harm sentence in the ramp-gradient evidence is from a code.
- **ANSWERS YOU CAN GIVE:**
  - **(a) All three count.** The line OD-58 draws is research or guideline against code or the project. Each source's marker still shows its strength.
    I record your answer in the ledger. The PR B engine counts them instead of refusing.
  - **(b) Co-1 and T3 grey count; T2 national standards do not**, because they are standards rather than research publications.
    I record it, and the engine counts two of the three.
  - **(c) None of the three counts** (the design as drafted).
    I record it, and the refusal becomes an exclusion.
  - **(Leave).**
    The engine refuses the rare cell where one of these would change the value. No live effect today.
- **MY RECOMMENDATION:** (a). Co-1 at least must count: it is co-primary with T1, and its warrant is that disabled people produced it. [CONFIDENCE: medium for (a) as a whole; high that Co-1 should count]
- **REPLY WITH:**
  - (a): `QB3 a`
  - (b): `QB3 b`
  - (c): `QB3 c`
  - (Leave): `QB3 leave`

### Q-B4 How is an "academic route" recorded for a T1 to T3 source that cannot be retrieved?   (who may decide: Opus may rule under OD-79. It is the method and schema of a rule you already gave (OR-23). The Opus adjudication may rule it.)

- **WHY IT IS ON THE LIST:** You ruled that an unretrievable source counts "only when the source is properly cited in an academic context" (OR-23, line 4725). No field records that route for research sources. Until one exists, such a source anchors nothing.
- **CONTEXT:**
  - No live effect: the one unverified T1 source (REF-01002) is not in the ramp-gradient set.
  - The audit noted that tier-system's "without one it anchors nothing" is written as a rule though the ledger marks it as a reading (AU-14). Your word "only" supports it.
- **ANSWERS YOU CAN GIVE:**
  - **(Opus) Leave it to the adjudication,** to design when a live case first needs it.
    No work now.
  - **(Leave) Do nothing until a case arises.**
    The same, without a ruling.
- **MY RECOMMENDATION:** (Leave). Nothing reads it today, and the project is to stay simple. [CONFIDENCE: high]
- **REPLY WITH:**
  - (Opus): `QB4 Opus`
  - (Leave): `QB4 leave`

### Q-B5 Can a cell resting only on grey sources, or on too few code values, reach "provisional"?   (who may decide: Opus may rule under OD-79. It is a state rule implementing your U6 and "keeping them" words, and no live cell is affected. The Opus adjudication may rule it.)

- **WHY IT IS ON THE LIST:** Today such a cell stays "pending", with no value shown. Your later words point the other way: "if the only values are from code then code determines the ideal/best" (U6, line 7875), and grey sources are kept "but they get a triangle warning" (line 7005).
- **CONTEXT:** No current group's cell is grey-only, and both probe cells have enough code values. The ledger leans "yes": a grey-only cell shows its value with ⚠, and a code-only cell shows its value with ○.
- **ANSWERS YOU CAN GIVE:**
  - **(Opus) Let the adjudication rule it** on U6 and "keeping them".
    Delegated ruling logged. The state rule changes in a later tooling PR, not the first one.
  - **(yes) Yes, both reach provisional**, marked as the table says.
    I record your answer in the ledger.
  - **(Leave).**
    Such cells stay pending. No live effect today.
- **MY RECOMMENDATION:** (Opus). Your rulings already point one way and nothing on the path needs it. [CONFIDENCE: medium-high]
- **REPLY WITH:**
  - (Opus): `QB5 Opus`
  - (yes): `QB5 yes`
  - (Leave): `QB5 leave`

---

# Reply card

| Item | Plain title | Recommended reply | Consequence |
|---|---|---|---|
| C4 | One order of authority | `C4 A` | CLAUDE.md, `/orient` and a DR note give one order; "what to do now" becomes `/orient` plus the newest ledger entries |
| D4 | SCI retires into WHEEL | `D4 yes` | The one-way retirement rests on your word; T-102 cites it |
| D3 | OD-76 parent codes | `D3 moot` | No open decision left in the register |
| D2 | Which mapping you doubted | `D2 leave` (or `D2 A` if A is what you meant) | Nothing waits on it |
| C9 | Two meanings of "thin" | `C9 a` | Provisional means limited strength; ⚠ is for conjecture only |
| C1 | Co-2 co-primary everywhere | `C1 a` | Every tier document says it; §2.4 lists Co-2 |
| C2 | T3 description | `C2 a` | No wrong ⚠ on clinical T3 |
| C3 | Rule 9 sentence and tool names | `C3 a` | Sentence corrected; you add three deny names |
| C5 | Axis model marked history | `C5 a` | Sessions stop reading a retired model as live |
| C6 | Pipeline contract | `C6 a` | Stage descriptions match your spine; ratification waits for your reading |
| C7 | Stale "CANONICAL" label and tier cells | `C7 both` | Doctrine matches its own status and the code |
| C10 | Umbrella wording | `C10 a` | CLAUDE.md matches your umbrella rulings |
| D5 | Old decisions table | `D5 a` | PENDING no longer misleads |
| D6 | Hand-correctable columns | `D6 b` | Qualitative cells may be fixed by hand, recorded; quotations never |
| D7 | Rules stay in CLAUDE.md | `D7 a` | CLAUDE.md trimming can proceed |
| D1 | e120 rows | (answered) | Second ledger entry naming the rows, then the data PR |
| Q1 | Four figures on page one | `Q1 first-page` | Page ships sooner, with a visible "not yet shown" line |
| Q2 | MOB and ramp gradient | (answered by ledger) | WHEEL route |
| Q3 | PROXY means thin? | `Q3 no` | First page can show ○ where its sources give ○ |
| Q4 | Parameter 3 or 12 first | `Q4 Opus` | Adjudication chooses after T-102 |
| Q5 | Six tasks, and T-039 | `Q5 defer` | Nothing you asked for is reversed; T-039 restored |
| Q-B2 | Several markers, one value | `QB2 a` | Strongest verified non-grey marker; ⚠ only if all stating sources are weak |
| Q-B3 | Who counts under the harm test | `QB3 a` | Co-1, grey research and T2 standards count |
| Q-B4 | Academic route record | `QB4 leave` | Nothing built until needed |
| Q-B5 | Grey-only or code-only cells | `QB5 Opus` | Delegated ruling, later tooling |

**Accept every recommendation (paste this):**

`C4 A; D4 yes; D3 moot; D2 leave; C9 a; C1 a; C2 a; C3 a; C5 a; C6 a; C7 both; C10 a; D5 a; D6 b; D7 a; Q1 first-page; Q3 no; Q4 Opus; Q5 defer; QB2 a; QB3 a; QB4 leave; QB5 Opus`

**Items where I think you should not simply accept my recommendation, and why:**

`Q1 (it relaxes your own OD-63 ruling; only you know whether page one may omit the four figures); Q3 and QB2 (each decides what a marker means, and my lean rests on a reading of "conjecture" and "coming from" that is yours to give); QB3 (whether disabled people's own research counts in the harm test is the project's central commitment, so say it in your own words); D2 (only you know what you meant); D6 (the scope of hand edits is your meaning of "specific columns"); C4 (check the two clauses marked as readings before adopting the order).`

---

# What each answer releases

- **C4:** the held-back half of approved item B2 (CLAUDE.md §9 row and `/orient`) and the DR note (former C8). One governance PR. After it, every later item has a single rule for which text wins.
- **D4 (with D3):** T-102 runs on your word. It creates WHEEL, moves SCI's links, closes GAP-111 and retires SCI. That opens the T-127 slice (judging the ramp-gradient lens links) and T-110, the first determination.
- **D2:** nothing on the path. Under (B), a review of the PR-245 rows.
- **C9 and Q3:** T-117, the marker table in code, can encode the thin rule rather than ship without it. This decides whether page one shows ○ or ⚠.
- **Q1:** under "first-page", the reduced T-037 page and the six-to-eight-task path. Under "keep", T-124, T-036, T-108, T-086, T-111 and T-113 join the path first.
- **Q-B2, Q-B3, Q-B5:** remove the engine refusals the PR B design leaves in T-117 and the T-059 selection slice. No live cell is blocked today.
- **Q4:** fixes which cell T-110 builds.
- **Q5:** one governance PR adding a stop line to seven task files, with the plan regenerated. This closes audit AU-01 and AU-05.
- **C1, C2, C7:** one governance PR editing the tier lines once. It removes a wrong ⚠ risk before T-117 lands.
- **C3, C5, C6, C10, D5:** one governance PR of text corrections. The deny names in C3 are your own edit to `.claude/settings.json`.
- **D6:** closes GAP-368. Later batches may make recorded hand fixes to qualitative cells.
- **D7:** lifts the block on trimming CLAUDE.md. The corrected proposal (item E) can then come to you.
- **D1:** no answer needed. A second ledger entry naming TRIPLE-53, -57 and -61, then a small data PR retiring them, with GAP-379 left open.

All the governance text edits above can ship as one or two governance PRs. Research rows (D1, T-102) ship separately, after any tooling (rule 10).

**Not on the slate, but raised by the audit for you:**
- whether doctrine-recheck's per-25-sessions and stage-transition triggers are abolished (AU-04);
- whether "expert consensus" values are thin or grey (AU-13);
- whether Definition-of-Done lines D-02 and D-13 are deleted (AU-20).

---

## Appendix: how to check each quotation (for a session, not for you)

Ledger lines are on `origin/main` `b3b3e9b6`. Each was found with `git grep -n -F "<phrase>" -- references/project-standards.md`.

| Phrase | Line |
|---|---|
| always assume I Ratify if I merge it | 585 |
| Co-2 = OT professional body CPGs (co-primary with Tier 2) | 17 |
| Co-1 stays full, Co-2 full too | 6989 |
| if government report is academically sound then it can be t3 | 4928 |
| I think thin is when the evidence doesn't directly concern someone | 7087 |
| T4 only half circle | 7195 |
| provisional' = thin evidence | 5980 |
| thin too | 7071 |
| 3 to umbrella and to specific, yes | 8290 |
| brain and complex are literally TOO complex | 570 |
| Work from axes | 561 |
| use advocacy groups and disability ethics as a lens | 5931 |
| I don't want axis to be used | 810 |
| should never ever exist anywhere | 3399 |
| I don't think the mapping is correct | 8407 |
| entire groups like b750 to b789 | 8401 |
| SCI is the same as WHEELCHAIR basically | 6115 |
| only SCI is the same as WHEEL | 6129 |
| permission to hand edit as required for specific columns | 8269 |
| Claude IS a tool | 8271 |
| the more exceptions we have the more complexity | 8192 |
| Ratify after T-022 merges | 6066 |
| you research slugs, evidence research | 1454 |
| fold plan into remediation plan | 7247 |
| Cite D-0184 for the lens mechanism | 2898 |
| D-0184 stands | 4630 |
| let's return to keeping them but they get a triangle warning | 7005 |
| 2 triangle for all | 7401 |
| separate out into | 1185 |
| Decompose MOB by device | 6019 |
| does the research prove that the more accommodating value | 7177 |
| od58 research publication | 7305 |
| as always refer to doctrine | 8485 |
| why would we want multiple authorities | 8658 |
| Co-2 is co-primary with tier 2. | 8654 |
| D1 retire | 8656 |
| Remember that this project is simple | 8551 |
| on the render page itself, we just have the minimum | 7399 |
| Whether Co-1 statements count under OD-58 | 7325 |
| no, triangle instead if the value is coming from grey | 7053 |
| if the only values are from code then code determines | 7875 |
| only when the source is properly cited in an academic context | 4725 |
| because if it mixes then it | 7159 |

Not in the ledger. Find these with `grep -c -F "<phrase>" transcripts/harness_f8d4d6c2/main.jsonl`, which is not yet committed:
- Opus to resolve conflicts like Q1
- contains some strict rules of operation

Database facts were read today with `sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)`, schema 167:
- `base_taxonomy_identity`: SCI is active and WHEEL is absent.
- `gaps`: GAP-111, GAP-368, GAP-372, GAP-376 and GAP-379 are all OPEN.
- `identity_need_icf`, need A-SIZE with e120: rows 53, 57 and 61, all pending, none retired.
- `decisions`: 24 PENDING, the latest D-0188; D-0184 is PENDING.
- `evidence_sources`, evidence type co2: 0.
- Range codes: 11 in `identity_icf_map`, 0 in `identity_need_icf` and `access_need_icf`.
- `specifications`: 8 rows, all retired.
- Parameters 3 and 12: direction `lower_is_better`, and `direction_ref_id` NULL on both.

Not re-verified today, and carried from the earlier prompts, the antagonists or the audit:
- the C5 list of surviving sections;
- the register line saying OD-76 releases nothing;
- the location of the 2026-09-23 rule 9 instruction;
- the PR B design's engine behaviour (simulated by its author);
- whether the deny list matches tool names regardless of spelling.
