# Delegated resolutions 2026-11-27 (revised, v2): draft for the ledger, with the owner's summary

This revision applies every correction in `checker-delegated-resolutions.md`. Version 1 is left as it was.

The adjudicator is an Opus-class instance working under the owner's delegation.

**Versions read.**
- `origin/main` is `b3b3e9b6`.
- HEAD `adc0bd9d` adds only session logs and the committed scratchpad copies of the inputs (`git diff --stat b3b3e9b6 adc0bd9d`). The ledger is identical on both, and `references/project-standards.md` line numbers below hold on both.
- The canonical database was opened read-only (`file:data/guidebook.db?mode=ro`, `PRAGMA user_version` 167). It was not changed.

**Method.**
- Nothing was edited, committed or applied.
- Every figure is given as the command that computes it (CLAUDE.md rule 7a).
- An owner's words are quoted. A reading of them is marked [ASSUMPTION].
- Anything not checked is marked [UNVERIFIED].

**Grant.**
- The owner's words of 2026-11-27: "Opus to resolve conflicts like Q1 and others. Further, prepare context and potential answers for me to use for the slate of C and D issues". They are verbatim in `transcripts/harness_f8d4d6c2/main.jsonl` according to the checker, and are not yet in the ledger.
- They continue "authority granted to opus to approve and ratify" (ledger 8481) and "Opus to adjudicate all of the above and log it" (8547).
- They are bounded by OD-79 (8503).

**Numbering.** OD-89 is the highest number in use (`git grep -n -E '\bOD-(9[0-9]|1[0-9]{2})\b'` prints nothing). These drafts use OD-90 to OD-113.

**Gate note.** `ANSWERED BY LEDGER` is not a gate value. A task gates on the entry the line cites, never on this line. Every CHECK line reads "pending: to be checked by a different instance".

---

## Part A. For the owner: one page

**What I ruled (no answer needed from you).**

1. **Page one keeps your four figures (Q1, OD-90).** OD-63 binds the first page. A delegate may not show the four figures computed over only the figures that can be read. Whether that is still the minimum, mode, median and maximum "colour coding the jurisdiction code bodies that we surveyed" is your meaning to give.
2. **Which cell goes first (Q4, OD-91).** Both ramp cells must first move to wheelchair users (your 2026-08-25 mobility split). The first cell is then whichever can be shown without relaxing a ruling of yours. On today's data that is ramp run length (parameter 12): every one of its code figures can be read, and all its code bodies are in P1+P2+P3. It is also the run between rest landings, which you raised on 2026-10-30. Ramp gradient follows.
3. **What starts now and what waits (OD-110).** These start now:
   - the marker table (T-117);
   - `design_scale` from the cell's key (T-056 item 3a);
   - the deferred-search flag;
   - the wheelchair-user move (T-102);
   - T-120's doctrine work.

   The selection change (T-059's slice), and with it the four-figure tooling, waits for T-120's doctrine section 0 and for the lens task T-127. T-127 waits for T-102 and for T-149, a tooling task that has no file yet and depends on a delegated ruling whose check is pending.
4. **Disabled people's own research.** An unverified Co-1 source may govern exactly as an unverified T1 source may. A Co-1 research publication counts under your harm test exactly as a T1 one does (OD-93, OD-101).
5. **No machinery over zero rows.** The record for your harm test moves to its own later pull request (OD-102).
6. **Smaller items.**
   - The engine's "proxy" flag alone does not make a value thin (OD-98).
   - The "academic route" record waits for a real case (OD-95).
   - T-039, your edit request, is restored (OD-106).
   - The stage-transition recheck goes back into the contract (OD-107).
   - "Expert consensus" is mostly answered by your rulings on thin (OD-108).
   - Four conflicts found in the inputs are ruled (OD-111 to OD-113, and OD-110's dependency edits).

**What waits on you.** Each item has a recommended answer. Work continues around all of them except where the last column says so.

| # | Question in plain words | Recommended | Meanwhile |
|---|---|---|---|
| OD-92 (Q-B2) | Several sources state the shown value with different markers: which marker does the value take? | The strongest marker among the stating sources that are verified and not grey; ⚠ only if all of them are grey or unverified. | The engine refuses such a cell. **Ramp gradient waits.** |
| OD-94 (Q-B3, rest) | Under your harm test, do these count: an advocacy organisation's statement, a grey research report, a national evidence-based standard (T2), an international standard (T4)? | Yes to the first three. No to T4, which is the code side of your test. | Nothing is built; no harm statement is held. |
| OD-96 (Q-B5, code half) | May a cell whose only values are code values show its value as "provisional" when fewer codes exist than doctrine's richness rule asks? | Yes. | Such cells stay "pending". None is on the path. |
| OD-97 (Q-B5, grey half) | May a cell whose only values are grey show its value, marked ⚠, as "provisional"? | Yes. | Such cells stay pending. None is on the path. |
| OD-99 (two parts) | (1) A source whose document was retrieved, but whose identity or edition is not yet confirmed: does its value carry ⚠ or its tier's circle? Your 2026-10-21 words tie "unverified" to "can't be retrieved". (2) How is "could not be retrieved" told from the record? | (1) ⚠ until confirmed. (2) No logged retrieval of the document, or a record that says it was not obtained. | These sources are kept and may govern. A cell whose shown value one of them states is refused. **Ramp gradient waits; run length does not.** |
| OD-100 | May a source that could not be retrieved, and has no academic or registry route, govern a value? | No: it is shown with ⚠ but does not govern. Low confidence: your 2026-10-21 words lean the other way. | It is shown and listed as excluded. One source, on ramp gradient only. |
| OD-104 | (i) Is a page built from the database on request and never committed allowed? (ii) May page one carry the audience lens later? (iii) Does a private page you read meet DR §4? | Yes to all three. | The page is built as a DRAFT. **Nothing is called published until you answer.** |
| OD-105 | Who may write the "Owner" entry naming the three D1 rows (TRIPLE-53, -57, -61), which the retirement tool needs? | You type one line naming or adopting them. The draft is in `d1-identification-entry-draft.md`. | D1 is not carried out. Nothing on the path reads those rows. |
| OD-109 | Two Definition-of-Done lines trace to your words: the walkability gate ("Yes, register it") and flexibility ("pipeline must be flexible"). Their tasks were deleted. Withdraw them, or restore the tasks? | Restore both tasks, deferred. | The task files are restored, deferred. The lines stay. |
| T-113 act (in OD-91) | Approve sub-national codes for England and Flanders, so the colour code does not label their codes "UK" and "BE". The tool needs an "Owner" entry. | Approve. | **Page one's colour code waits for this.** |
| Q3 (slate) | Does a PROXY grade, or a lens assigned by contextual judgment, make a value thin? | Neither does, unless the step across groups is the project's own conjecture. | T-117 derives no thin from either. |

Q2 is answered by the ledger. Q5's six held tasks stay with you.

**What each ruling releases.**

| Ruling | Releases |
|---|---|
| OD-90 | T-124 on the path, with its precondition narrowed (OD-110). |
| OD-91 | The order of work and the test for the first cell. |
| OD-110 | PR B part 1's ready pieces (T-117, T-056 3a), the deferred-search flag, T-102 and T-120. |
| OD-93, OD-101, OD-102 | Constraints on the selection slice and on the later harm pull request. |
| OD-106, OD-107, OD-108 | One governance pull request. |
| OD-111 to OD-113 | Corrections to T-120, the page design and the first cell's batch. |

**Corrections to the decision slate** (`scratchpad/session_2026-11-26-governance-reconciliation/slate/decision-slate.md`):
- Q-B2's card says the refusal "does not fire on parameters 3 or 12 today". It fires on 3 × MOB (`prb-antagonist-1.md` D2).
- Q1's card lists T-036 and omits T-059 and T-068, which T-124 §2 requires.
- D1's "What happens next" plan is not delegable as written (OD-105).

---

## Part B. Draft ledger text, ready to append

> DRAFT text only. Append it after the coordinator has recorded the owner's 2026-11-27 words under rule 0. It contains no "Owner" heading, no `ANSWERED BY THE OWNER` line and no embedded entry, and it relaxes no guard. The D1 identification text is a separate file (OD-105), not part of this block.

## Delegated resolutions 2026-11-27 — the first page and its order; marker, route and harm rules for PR B; T-039 and two audit findings; nine questions referred back (OD-90 to OD-113)

Written by an Opus-class adjudicator under the owner's words of 2026-11-27 ("Opus to resolve conflicts like Q1 and others"), within the reach OD-79 records (8503). An independent check (`checker-delegated-resolutions.md`) has been applied.

Inputs, as committed under `scratchpad/session_2026-11-26-governance-reconciliation/`:
- `slate/decision-slate.md`
- `prb/prb-design-1.md`, `prb/prb-design-2.md`
- `prb/prb-antagonist-1.md`, `prb/prb-antagonist-2.md`
- `audit/audit-session-work.md`
- `remediation-classification/resolution-plan.md`, `remediation-classification/path-to-one-determination.md` and `remediation-classification/antagonist-4.md`

**Not an owner statement.** Each ruling names the passage it rests on. Each CHECK line is pending until a different instance checks it.

**Commands used below** (run from the repository root, read-only):
- **C1(P)**, the code-stratum quantity figures of parameter P, how many `dbcore.figure_refusal` refuses, and the jurisdictions they name:
  `python3 -I -c "import sys,sqlite3;sys.path.insert(0,'scripts');import dbcore;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);q=dbcore.QUANTITY_CLAIM_TYPES;r=[v for v in c.execute('select x.claimed_value,x.claimed_unit,x.comparator,x.claim_type from source_value_extractions x join evidence_sources e using(ref_id) where x.parameter_id=P and x.retired_at is null and e.tier>=4').fetchall() if v[3] in q];print('quantity',len(r),'refused',sum(1 for v in r if dbcore.figure_refusal(c,*v)),'bodies',sorted({j for (j,) in c.execute('select distinct e.jurisdiction from source_value_extractions x join evidence_sources e using(ref_id) where x.parameter_id=P and x.retired_at is null and e.tier>=4')}))"`
- **C2**, the unverified sources and how each records its verification:
  `select ref_id, tier, evidence_type, jurisdiction, verification_method, standard_number from evidence_sources where verification_status='UNVERIFIED'`
- **C3(ref)**, a source's logged retrievals: `retrieval_log.manifest_lines_for(ref_id, url, doi)`. Read each line: the log does not type whether a line is the document, an index record or a probe.

**OD-90 (Q1: may the first page leave out the four figures of OD-63, or compute them over only the figures that parse?): OD-63 binds the first page, and a delegate does not adopt a partial computation.**
- **The owner's words** (7399): "1. good point. all values when synthesizing and making determinations, but on the render page itself, we just have the minimum, mode, median and maximum colour coding the jurisdiction code bodies that we surveyed for comparison purposes".
- **The gate.** "OD-63: … the render shows the minimum, mode, median and maximum as a colour code on the surveyed jurisdictional code bodies" with its status line answered by the owner (7421-7422). The ACTION reads "T-124 and T-037 follow OD-63" (7434, ACTION (5)).
- **Why a partial is not for a delegate.** Showing the four figures over the figures that parse, with a count of those left out, decides whether such figures are the ones the owner described. That is the owner's meaning (OD-79).
- **The live fact.** C1(3) prints the quantity figures and how many are refused. Any refused figure may be the true minimum or maximum.
- **The owner may relax OD-63; no delegate can.**
- **Opens:** T-124 on every page's path. Its §2 precondition is narrowed under OD-110 to the slices it reads (the T-059 selection slice and T-068's cluster step). It therefore waits for what those wait for (OD-110).
- **Rests on:** 7399, 7421-7422, 7434; 8503; CLAUDE.md line 79.

OD-90 STATUS: ANSWERED BY LEDGER (OD-63; read OD-63's gate)
OD-90 CHECK: pending: to be checked by a different instance

**OD-91 (Q4: which cell first, and the order of work): a test, run after the wheelchair-user carry, picks the first cell. On today's data that is ramp run length (parameter 12) at WHEEL.**

*Why WHEEL.* Neither cell may be keyed on MOB. The ruling reads "RULE: `MOB` is split … 'As to "mobility", separate out into "ambulatory" and "wheelchair user" to start.' … not to be relitigated" (1184-1187). Its analysis names run length and gradient together: "an ambulant person with fatigue or spasticity often wants a shorter run, and therefore a steeper one" (1197-1199). Both cells follow T-102 (OD-83, 8608; carry-only under OD-84, 8614).

*The test.* After T-102 and the T-127 slice, run the engine for 3 × WHEEL and 12 × WHEEL on a scratch copy. The first cell is the one that meets all four conditions:
1. the engine composes a value;
2. no refusal names an open owner question (OD-92, OD-99);
3. C1(P) shows no refused code figure, so OD-63 can be met in full;
4. every code body it names is in P1+P2+P3 (4835, 4866 ACTION (5); the list in `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md` §3, a reading the ledger marks [ASSUMPTION] under item 7).

If neither cell passes, report to the coordinator. Whether either keeps a value at WHEEL is [UNVERIFIED] until the run.

*Today's data.*
- C1(12) shows no refused figure, and every jurisdiction it prints is in the HANDOFF list.
- C1(3) shows refused figures and names UG and INT, which are outside the list.
- 12 × MOB's only stating source today is a verified T5 (`prb-antagonist-1.md` row 1a), so neither OD-92 nor OD-99 fires on it.

*Why the order is reasonable apart from the test.* The owner's words: "I think the issue is not the slope of the ramp, but the lack of a rest landing" (4836). [ASSUMPTION: parameter 12 is that quantity — basis: its `notes`, "The maximum run between rests is this parameter's run".]

*Order of work.* Tooling merges before the data that uses it (CLAUDE.md rule 10). OD-110 gives each task's start condition.
- Tooling now: PR B part 1's ready pieces; PR B part 2's deferred-search flag; T-120.
- Data now: T-102.
- Then the T-127 slice. It waits for T-102 and, under OD-89 ACTION (1) ("T-127 waits for T-149 (tooling) and prefers T-150", 8639), for T-149. T-149 has no task file (`ls workplan/2026-11-12-bidirectional-pipeline/tasks | grep -c T-149` prints 0), and the delegated OD-88 that opens it has a pending check (8632). This ruling does not override OD-89 ACTION (1).
- Then the T-059 selection slice, T-068's cluster step and T-124.
- Then the page.
- Then the first cell's repairs, and T-110.

*The first cell's repairs (parameter 12).*
- **GAP-372 for extraction 141** (REF-01027). `select status, description from gaps where gap_id='GAP-372'` lists it. The truncated original is retired and re-added with existing verbs, then translated. Data.
- **The T-113 slice, which needs the owner.** REF-00992 is filed `UK` though Approved Document M is England's. REF-00995 is filed `BE` though it is a Flemish decree. `base_jurisdictions` holds no sub-national code (`select kind, count(*) from base_jurisdictions group by 1`). `db.py add-jurisdiction` requires an approval heading that begins "Owner" (`scripts/db.py`, `def add_jurisdiction`, its call to `_owner_approval`), and the checker's dry run was refused. **Minting the codes is an owner act.** Until it is done, OD-63's colour code would label these bodies as countries, so page one's colour code waits for it.
- **Population-match grades** against WHEEL for its ungraded governing sources. Data.
- **T-123's direction pointer cannot be recorded with existing verbs** (OD-110), so it is not on this path.

*Duplicates.*
- GAP-376's pairs are REF-01026 with REF-01032, and REF-01019 with REF-01031 (`select description from gaps where gap_id='GAP-376'`).
- REF-01015's false edition is a separate defect (`antagonist-4.md` F2).
- None of REF-01026, REF-01019, REF-01031 or REF-01015 holds a parameter 12 row (`select distinct ref_id from source_value_extractions where parameter_id=12 and retired_at is null`).

*Parameter 3 then needs:* OD-92 and OD-99 answered, T-104, GAP-376, its GAP-372 rows, T-108, T-086, T-111, the T-105 slice, T-113 for REF-00997 and REF-00996, and the in-scope filter (OD-112).

- **Rests on:** 1184-1199; 8608; 8614; 8632; 8639; 7421-7422; 4835, 4836, 4866; 8503 (ordering).

OD-91 STATUS: RESOLVED UNDER DELEGATION
OD-91 CHECK: pending: to be checked by a different instance

**OD-92 (Q-B2: several sources state the shown value with different markers): referred back to the owner.**
- **What is ruled.** OD-59 answered the question as registered (7273). The words were "od59 yes" (7307), with gate 7333-7334. The recorder's reading: "the showcased value carries the grade of its own source, with ⚠ only when that value's own basis is grey, unverified or thin" (7319).
- **What is not.** Several stating sources leave "its own source" unnamed. The owner's "no, triangle instead if the value is coming from grey or unverified" (7053) does not say whether a value stated by a verified source and by an unverified one is "coming from" the unverified one. The entry lists the combined case as undecided (7059).
- **Why it is the owner's.** It decides what a marker means (`governance/decision-protocol.md` line 77, "Evidence-tier definitions") and the owner's meaning of "coming from" (OD-79).
- **Options and consequences.**
  - (a) The strongest marker among the stating sources that are verified and not grey; ⚠ only when every stating source is grey or unverified. Adding a source never lowers a marker.
  - (b) The weakest. A newly found unverified source would turn a verified code's ○ into ⚠.
  - (c) Leave it. The engine keeps refusing such cells.
- **Recommended:** (a).
- **Meanwhile:** PR B part 1's engine refuses such a cell, naming this question. It blocks 3 × MOB, not 12 (OD-91).

OD-92 STATUS: REFERRED BACK TO THE OWNER
OD-92 CHECK: pending: to be checked by a different instance

**OD-93 (Q-B3, Co-1 research publications under OD-58): a Co-1 source that is itself a research publication counts under OD-58 exactly as a T1 research publication does.**
- **The owner's standard** (7305; gate 7330-7331): "od58 research publication or clinical guidelines state that a person with disability struggles more or has more difficulties or some kind of negative statement with a parameter being at a certain value compared to the one it proposes".
- **The owner's rank:** "Co-1 and T1 are same value" (6176), confirmed as one rank (6176-6178).
- **The recorder's reading:** "whether a statement from a lived-experience source (Co-1) also counts is not stated and is read as yes … flagged" (7318). It is held open "beyond the reading above" (7325).
- **The doctrine:** "Co-1 evidence is co-primary with Tier 1" (`governance/mission-and-epistemics.md` line 50), whose forms include "peer-reviewed lived-experience literature" and "Co-1-authored academic narratives" (line 91).
- **The ruling.** A peer-reviewed lived-experience paper is a research publication in the owner's plain words, so this ruling applies the words to such a source and supplies no meaning. Treating it worse than a T1 paper would contradict OR-6c and CLAUDE.md line 374 ("Erasing them while claiming the tier is the worst failure available here").
- **What stays open.** Co-1 sources that are not research publications go to OD-94.
- **Effect today:** none. The constraint binds the harm-record pull request (OD-102).

OD-93 STATUS: RESOLVED UNDER DELEGATION
OD-93 CHECK: pending: to be checked by a different instance

**OD-94 (Q-B3, the rest): referred back to the owner.**
- **The question.** Under OD-58 (7305), do these count as "research publication or clinical guidelines": a Co-1 statement that is not a research publication (a named advocacy organisation's position); a T3 grey research report; a T2 national evidence-based standard (`standard_eb` at tier 2); a T4 international standard (`standard_eb` at tier 4)?
- **Why it is the owner's.** The recorder read Co-1 as yes, flagged (7318), and held it open (7325). The others are not addressed. Each is the owner's meaning (OD-79).
- **The live case.** The one harm sentence in the ramp-gradient evidence is extraction 77, from REF-01014 (`select ref_id from source_value_extractions where extraction_id=77`). C2 shows REF-01014 as tier 4, `standard_eb`, UNVERIFIED, a draft ISO standard.
- **Options and consequences.**
  - (a) All four count. The harm test then sets any source's statement against the most accommodating value.
  - (b) The first three count and T4 does not. T4 is the regulatory stratum, on the code side of "if so, research wins. if no, code wins" (7177). Extraction 77 would not displace a value.
  - (c) Only Co-1 counts.
  - (d) None counts.
- **Recommended:** (b). A statement of struggle by disabled people's own organisations is what OD-58 describes. A grey report's weakness is shown by ⚠ (OD-64, 7424). A T2 standard is evidence-based synthesis.
- **Meanwhile:** nothing is built (OD-102).

OD-94 STATUS: REFERRED BACK TO THE OWNER
OD-94 CHECK: pending: to be checked by a different instance

**OD-95 (Q-B4: how OR-23's academic route is recorded for an unretrievable T1 to T3 source): do nothing now. The existing records are named for the first live case.**
- **Why nothing now.** No cell on the path needs it. The one unverified T1 source, REF-01002 (C2), is not gathered for either ramp cell (`prb-design-1.md` §1.8).
- **What REF-01002's records show.** C3(REF-01002) returns lines that the checker read as index, metadata and probe records, not the document. Its `verification_method` is `corroborated-not-retrieved` (C2). It is therefore a source that could not be retrieved, and that record is its route candidate.
- **The route, when a case arises,** is read from existing records, with no new field:
  - a DOI or PMID on the source;
  - `verification_method` in (`corroborated-not-retrieved`, `citing-bibliography`);
  - a logged index record.
  
  [ASSUMPTION: these are a "valid academic route" — basis: the recorder's reading at 4758, unratified, used here as method.]
- **Meanwhile:** a route-less unretrievable T1 to T3 source does not anchor. That follows the owner's "only" ("This applies only when the source is properly cited in an academic context", 4725) and is subject to OD-100.

OD-95 STATUS: RESOLVED UNDER DELEGATION
OD-95 CHECK: pending: to be checked by a different instance

**OD-96 (Q-B5, code half: may a code-only cell below the richness threshold reach `provisional`?): referred back to the owner.**
- **The question.** `governance/evidence-methodology.md` line 144 lets a T4–T6-only cell be `provisional` only when "rich enough". The owner's words: "if the only values are from code then code determines the ideal/best" (U6, quoted at 7875). Does that also let a code-only cell below the richness threshold show its value as `provisional`, instead of staying `pending`?
- **Why it is the owner's.** U6 speaks of which value is best. Whether it supersedes a state condition is the owner's meaning (OD-79). The checker found that version 1 decided it.
- **Options and consequences.**
  - (a) Yes. Such a cell shows its value with its tier's marker (◐ for T4, ○ for T5 and T6; 7195).
  - (b) No. It stays `pending` with no value shown until enough codes are held.
- **Recommended:** (a). [ASSUMPTION: "code determines the ideal/best" means a value is shown when only code values exist.]
- **Meanwhile:** such cells stay `pending`. None is on the path. Which cells are affected: `prb-antagonist-1.md`'s `union.py` lists them; re-run it.

OD-96 STATUS: REFERRED BACK TO THE OWNER
OD-96 CHECK: pending: to be checked by a different instance

**OD-97 (Q-B5, grey half): referred back to the owner.**
- **The question.** A cell whose only values come from grey sources stays `pending` (DR-2026-07-12 item 2). The owner's words: "let's return to keeping them but they get a triangle warning" (7005), and "2 triangle for all" (7401). Does such a cell show its most accommodating value, marked ⚠, as `provisional`?
- **Why it is the owner's.** "keeping them" was recorded as admission (7009, 7016). Whether it reaches the cell's state is the owner's meaning.
- **Options.**
  - (a) Yes, with ⚠.
  - (b) No value until a non-grey source exists.
- **Recommended:** (a). [ASSUMPTION: "presents all values/approaches/data for comparative purposes" (6836) reaches such cells.]
- **Meanwhile:** they stay pending. None is on the path (`prb-design-1.md` §2.6).

OD-97 STATUS: REFERRED BACK TO THE OWNER
OD-97 CHECK: pending: to be checked by a different instance

**OD-98 (Q3b: does `specifications.rests_on_proxy_inference` make a value thin?): not by itself. Under the project-inference cause, a value is thin only when no source in the cell's lens states it, that is, when the project composed it.**
- **The owner's words:** "because if it mixes then it's a new value proposed for something so it's conjecture because we don't have authority" (7159). The conjecture lies in the value being new.
- **The live case.** The 3 × MOB headline (1:20, 5 %) is stated by extraction 25 (REF-00992). It is also stated by extraction 30 (REF-00995), whose stored quote is truncated (GAP-372) and owed repair. It is chosen by the most-accommodating rule (U1, 7870; 7177), so no new value is proposed.
- **What this does not decide** (put to the owner with Q3):
  - whether a PROXY population grade makes a value thin (7093; `governance/tier-system.md` line 80);
  - whether a lens assigned by contextual judgment under OD-65 ("use contextual judgment", 7403) is conjecture.
- **Meanwhile:** T-117 derives thin from neither.

OD-98 STATUS: RESOLVED UNDER DELEGATION
OD-98 CHECK: pending: to be checked by a different instance

**OD-99 (the route gate and C10): two questions referred back to the owner. What ships meanwhile is stated below.**

*The record against version 1.* Version 1 read "unverified" as "not yet confirmed" and limited the route gate to sources never retrieved. The owner's own record ties "unverified" to retrieval:
- The owner's words of 2026-10-21 (4540-4541): "if we can't retrieve a study, then we can't verify it as a primary source, which means that we can't claim it as a top tier. add unverified in this context where something can't be retrieved to the empty circle alongside grey or thin".
- The recorder's gloss of 2026-11-14 (7007): "*Unverified*: a source that could not be retrieved, stored with `verification_status` `UNVERIFIED`".
- `governance/tier-system.md` line 70: "unverified (the source could not be retrieved)".

So the owner's rulings do not say what marker a source carries when its document was retrieved and logged but it is stored UNVERIFIED (identity or edition unconfirmed, as REF-00994's GAP-371). Nor do they say how the record tells "could not be retrieved".

*Question 1.* A source whose document was retrieved, but which is stored UNVERIFIED: when it states the shown value, does the value carry ⚠, or its tier's circle?
- (a) ⚠, as for any source stored UNVERIFIED. A value never carries a circle on a source whose identity is unconfirmed.
- (b) Its tier's circle. ⚠ only when the document could not be retrieved, as the 2026-10-21 words describe.
- Recommended: (a). [ASSUMPTION: an unconfirmed identity carries the risk CLAUDE.md §5(c) names, a citation that may be wrong, so the warning is the honest mark until the identity is confirmed.] Low-to-medium confidence: the owner's words tie "unverified" to retrieval.

*Question 2.* How is "could not be retrieved" told from the record?
- (a) No usable logged retrieval (`retrieval_log.manifest_lines_for`, C3). This misreads REF-01002 as retrieved, because the log counts index and probe records.
- (b) No logged retrieval of the document, or `verification_method` in (`corroborated-not-retrieved`, `citing-bibliography`), whose CHECK comment defines existence established without retrieval. REF-00997's `direct-render` beside a recorded HTTP 403 is then a data error, corrected by `correct-source`.
- (c) A field the verifying session sets, with its warrant.
- Recommended: (b). It reuses typed records.

*What ships meanwhile (delegated: ordering and method, reversible).*
- **The retrieved code sources** that C2 and C3 identify among the governing sources of 3 × MOB (REF-00994, REF-01013, REF-01014, REF-01016, REF-01026; re-derive with C2 and C3) are kept and may govern, with no route required. OR-23 and OR-23b speak of an "unretrievable" source (4758, 6186), and these were retrieved.
- **Which marker they carry is the owner's to say (Question 1).** Until then, the engine refuses a cell whose shown value one of them states, naming this question. This blocks 3 × MOB (REF-00994 states the headline). It does not block 12 × MOB, where REF-01016 governs but does not state the headline (`prb-antagonist-1.md` row 1a).
- **The interim test for "not retrieved"** is Question 2's option (b).
- **The engine meanwhile.** A source that fails the interim test and has no route (OR-23 for T1 to T3 and Co; OR-23b's jurisdiction, standard number and clause for T4 to T6) is shown and listed as excluded with its reason. It does not govern; see OD-100.
- **Four standard numbers held in titles.** For REF-01013, REF-01014, REF-01016 and REF-01026 the number sits in `pub_title` and not in `standard_number` (C2). That is a data gap, mended by `correct-source` in a research PR. The gate never parses titles (CLAUDE.md §4).
- **C10 meanwhile** (`scripts/tests/test_db_integrity.py`) fails a live cell when:
  - (1) a governing source fails the interim test and has no route; or
  - (2) every governing source is non-VERIFIED or grey and the marker is a circle.
  
  It no longer fails a cell only because a retrieved, unverified source governs. T-117 item 4a's "C10 passes when the marker is ⚠" is not built: under OD-59 a value may rightly carry a circle beside an unverified governing source.
- **Two retrieved sources stay out of the comparison.** REF-00994 is filed `INT`, outside P1+P2+P3. REF-01014 is a 2007 draft, not a current edition (2026-10-30 item 7). They are kept as sources but are not rows in the jurisdiction comparison (OD-112).

- **Rests on:** 4540-4541, 4725, 4758, 6186, 7005, 7007, 7053; `governance/tier-system.md` lines 70 and 77; OD-79.

OD-99 STATUS: REFERRED BACK TO THE OWNER
OD-99 CHECK: pending: to be checked by a different instance

**OD-100 (a source that could not be retrieved and has no route: may it govern a value?): referred back to the owner.**
- **The record, in order.**
  - 2026-10-21, the owner: "add unverified in this context where something can't be retrieved to the empty circle alongside grey or thin" (4541). This gives such a source's value a marker, which presupposes the value is shown.
  - 2026-10-29, OR-23: "This applies only when the source is properly cited in an academic context" (4725). It confirmed that an unretrievable source "may still anchor … only when" it has a route (4758).
  - 2026-11-14: "let's return to keeping them but they get a triangle warning" (7005), with the recorder's gloss "*Unverified*: a source that could not be retrieved" (7007).
- **The question.** Does the later "keeping them" let a route-less, unretrievable source govern a value, marked ⚠?
- **Options and consequences.**
  - (a) No. It is shown and listed with ⚠ but does not govern, and OR-23's "only" stands.
  - (b) Yes. It governs with ⚠, and OR-23 no longer limits anchoring. 4541 and 7005 support this reading.
- **Recommended:** (a), with low confidence. "Only" is explicit and later than 4541, while 7005 is later still. [ASSUMPTION: "keeping" answered whether such sources stay in the book (7009).]
- **Meanwhile:** OD-99's engine behaviour, which is (a) and reversible. Its reach is REF-00997 (C2), on parameter 3 only.

OD-100 STATUS: REFERRED BACK TO THE OWNER
OD-100 CHECK: pending: to be checked by a different instance

**OD-101 (the eligibility union): an unverified Co-1 source is eligible to govern on the same terms as an unverified T1 source.**
- **The defect.** `prb-design-1.md` §2.3 item 1 adds `b["t1"]` and omits `b["co1_unverified"]`. That contradicts "Co-1 and T1 are same value" (6176), CLAUDE.md line 366 ("co-primary with T1") and line 373.
- **Correction:** `eligible = anchoring(b["t1"]+b["co1"]+b.get("co1_unverified", [])+b["t2"]+b["co2"]+b["t3c"]+b["t3g"]) + b["t45"] + b["t6"]`. OD-99's interim and route conditions apply identically to both.
- **What it does not change.** Eligibility is not the `stated` threshold. `governance/evidence-methodology.md` §2.2 condition 3 (line 131) still requires a VERIFIED Co-1 source for `stated`, while condition 1 (line 129) carries no such clause for T1. That asymmetry is doctrine and is not changed here; it is noted for the owner.
- **Red test:** an unverified Co-1 source with a logged retrieval of the document, stating the most accommodating value alone, governs. Its marker follows OD-99 Question 1.
- **Live reach:** C2 lists no Co-1 source.
- **Opens:** a correction to the T-059 selection slice, which waits (OD-110).

OD-101 STATUS: RESOLVED UNDER DELEGATION
OD-101 CHECK: pending: to be checked by a different instance

**OD-102 (`worse_at` and the `extraction_relations` rebuild for OD-58): deferred to a separate tooling pull request that lands with or before T-125's capture path. Not dropped.**
- **Why not dropped.** "T-059 builds the selection with the OD-58 standard" (7343, ACTION (3)).
- **The live writer.** A harm writer exists: `db.py add-extraction --harm-finding` (the `add-extraction` parser, `scripts/db.py`; `grep -n -- '--harm-finding' scripts/db.py`), and `amend-search --set-harm-finding` for searches.
- **What the writer records.** It refuses a harm flag without an `insufficient` edge in the same call (`grep -n "needs an \`insufficient\` edge" scripts/db.py`). So it records harm at a **less** accommodating value, the opposite of OD-58's statement (struggle at the more accommodating value).
- **Nothing reads it.** `grep -c harm_finding scripts/assess/assess_cell.py` prints 0. No live row is flagged: `select harm_finding, count(*) from source_value_extractions group by 1` shows only 0.
- **Why deferral loses nothing.** No OD-58 statement can be recorded by any writer today, so none can be silently ignored. A flag the writer does record argues for the most accommodating value, which the selection already shows.
- **Why not now.** The rebuild, the refusals, the reader and the Q-B3 list would read nothing (CLAUDE.md line 506).
- **When it lands,** the record carries OD-93's constraint and the owner's answer to OD-94.

OD-102 STATUS: RESOLVED UNDER DELEGATION
OD-102 CHECK: pending: to be checked by a different instance

**OD-103 (the render page: what a delegate decides): the method only.**
- **How it is generated.** A pure function over one read-only connection (`page(conn, specification_id)`), runnable from the database each time. It writes outside the repository (the guard in `scripts/generate/owner_browser_build.py`, refusing `scratchpad/` too) and is never committed.
- **Where it is published.** As a private Artifact for the owner, on the precedent "the page is generated to `$TMPDIR` and published privately, never committed" (4584).
- **One database only.**
  - `translations_shown()` and `cell_status()` bind to `dbcore.db_path()`, not to the passed connection (`prb-antagonist-2.md` D1). Either they take the connection, or the page refuses when `--db` and the resolved `GUIDEBOOK_DB_PATH` differ.
  - "DRAFT" is printed when `dbcore.is_canonical` is false (D2).
- **What it carries:**
  - DR-2026-08-19 §4's elements (lines 373-375);
  - OD-63's figures from T-124, never computed by the page;
  - in-scope rows only (OD-112);
  - originals beside reviewed English (CLAUDE.md lines 15-17; OD-30);
  - every grade row (OD-113);
  - the stored marker only.
- **What it never prints:** engine prose fields or `design_scale` (`prb-design-2.md` §2.4).
- **What it never claims:** an accessibility test not run (2026-10-30 item 6; 4866 ACTION (4)).
- **Rests on:** CLAUDE.md line 260; 4584, 4589, 4866; DR lines 373-375; OD-79.

OD-103 STATUS: RESOLVED UNDER DELEGATION
OD-103 CHECK: pending: to be checked by a different instance

**OD-104 (the render page: the owner's meanings): referred back to the owner.**
- **(i) Is an on-request page allowed?**
  - The owner's words: "the entire pipeline is dynamic rendering on site" and "do not rely on artifacts for rendering the site" (quoted at 1658); "i want it to be coming from database directly in ideal world" (4840).
  - The ACTION reads "do not restore a static generator" (4866, ACTION (3)). Its narrowing to committed HTML is the recorder's [ASSUMPTION] (item 3), unratified by ACTION (7).
  - Is a page generated from the database on request, never committed and published privately allowed? (a) Yes. (b) No: only the owner browser's view-time read, with refusals re-implemented in its JavaScript (a second home).
  - Recommended: (a).
- **(ii) May page one carry the audience lens later?**
  - The owner's words: "There is an audience lens (the four audiences) and a disability lens (population, ICF, access needs)" (4841). ACTION (4) reads "Offer the audience and disability lenses". No ruling says what the audience lens changes on a one-determination page.
  - (a) Page one carries the disability lens; the audience lens comes with the first audience-specific content, and the page says so. (b) Both now.
  - Recommended: (a).
- **(iii) Does a private page meet DR §4?**
  - Does a private page the owner reads meet DR-2026-08-19 §4's "rendered and readable as output" before launch?
  - (a) Yes. (b) No, publication waits for a public surface. This bears on C4.
  - Recommended: (a).
- **Meanwhile:** OD-103's page is built against a scratch copy and marked DRAFT. Nothing is called published.

OD-104 STATUS: REFERRED BACK TO THE OWNER
OD-104 CHECK: pending: to be checked by a different instance

**OD-105 (carrying out "D1 retire": who may author the "Owner" entry the retirement tool needs?): referred back to the owner.**
- **The guard, read in the code.**
  - `db.review_identity_need_icf` calls `_owner_approval` (`scripts/db.py`, `def _owner_approval`), which refuses any heading not beginning "Owner" and any delegated resolution.
  - It then requires `dbcore.ledger_entry_names(heading, "TRIPLE-<id>")` for every row (`scripts/dbcore.py`, `def ledger_entry_names`, which reads only the entry's own text up to the next `## ` heading and finds nothing when a heading occurs other than once).
  - The owner's answer (`git grep -n -F "D1 retire" -- references/project-standards.md`) sits in an entry that names no TRIPLE token. The audit's dry run was refused (`audit-session-work.md`, AU-02).
- **The rows.** `select triple_id, identity_code, state from identity_need_icf where need_code='A-SIZE' and icf_code='e120' and retired_at is null` prints TRIPLE-53 (LPA), TRIPLE-57 (TALL) and TRIPLE-61 (BAR).
- **Why it is the owner's.** The guard exists "so that no session states its own row" (8490). A session writing an "Owner" entry that carries no new owner words would be that, and a row the schema binds to an Owner entry is outside the grant (OD-79). The precedent differs: in "Owner review 2026-11-21 — rows 64 and 65" (8377-8389) the owner typed the row numbers ("Reject Row 65. Accept Row 64."); here the owner typed "D1".
- **Options and consequences.**
  - (a) The owner types one line naming or adopting the rows. The coordinator records it under an "Owner" heading using the draft text in `scratchpad/…/d1-identification-entry-draft.md` (a separate file, not part of this block). The guard is met as designed.
  - (b) The owner rules that a recorder may write the identification under an "Owner" heading when the owner's earlier answer names the rows by description. That is a standing convention, applied here.
  - (c) Leave D1 unexecuted.
- **Recommended:** (a). It costs one line, and it is the path the guard was built for.
- **Meanwhile:** nothing is retired. Nothing on the path reads `identity_need_icf` (OD-85, 8592). GAP-379 stays open.

OD-105 STATUS: REFERRED BACK TO THE OWNER
OD-105 CHECK: pending: to be checked by a different instance

**OD-106 (T-039, the owner's edits as proposals): restored.**
- **The owner's request:** "I need there to be some kind of interface where I can manually review and edit the different table values/information and have it propagate accordingly" (4580). ACTION (1) reads "a read-only browser and the owner's queue first, then edits as proposals" (4589).
- **Why it is restored.** T-039 was the only task for the edit half. It was deleted in PR #249 as having "no owner request found", which is false (AU-01). Withdrawing an owner request is the owner's; restoring the task is not.
- **The action.** Restore `workplan/2026-11-12-bidirectional-pipeline/tasks/T-039-owner-edits.md` and its index row from `253c2dcc`, then re-run the generator.
- **What stops an executor.** The generator's `status()` (`scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`, `def status`) reads three things only: closed owner gates, missing design files, and "NOT FOR SONNET" in the Executor cell. A "DEFERRED" line is inert, and so are AU-05's proposed stop lines.
  - T-039's Executor cell already reads "NOT FOR SONNET", so the restored task is listed as a stop for a Sonnet executor.
  - For an Opus-class executor the only stop is the file's banner ("design after the owner's answer"), which is prose.
  - AU-05's deferred tasks need the same Executor-cell edit to be stopped mechanically.
- **Offered to the owner, not referred.** The 2026-11-21 words "We don't need a tool for many qualitative judgments/corrections because Claude IS a tool" may mean the edit half is no longer wanted. Only the owner can withdraw it.
- **Opens:** the governance PR. **Closes:** AU-01.

OD-106 STATUS: RESOLVED UNDER DELEGATION
OD-106 CHECK: pending: to be checked by a different instance

**OD-107 (AU-04, doctrine-recheck triggers): the stage-transition clause is restored to the contract. The removal of the 25-session trigger stands as the owner's approved item B5.**
- **The 25-session trigger.** Item B5 of the list the owner approved reads "'every 25 sessions' was abolished by DR-2026-08-19 section 10 item 4". The owner's words were "approve A and B all" (8656; ACTION (1), 8671). DR-2026-08-19 lines 616-617 removed "the frozen recheck counter".
  - `governance/doctrine-recheck.md` §1.1 gets one dated line pointing to B5's approval.
  - Its line 21 ("**Two remain**") is swept to say one remains, §1.2.
- **The stage-transition trigger.** It was in neither B5 nor DR §10 item 4. The criterion before PR #248 read "A doctrine recheck fires at every stage transition and every 25 sessions" (`git show 4645a618:governance/pipeline-contract.yaml`, line 361).
  - Its removal went beyond the approved item, so the clause is restored beside the retained `--cross-ref` clause. In today's file the entry's id is at line 361 and its criterion at line 362.
  - Restoring it reverses an unapproved change and needs no other warrant. Whether to abolish it is the owner's (the document calls itself CANONICAL). Nothing waits on that.
- **Opens:** the governance PR.

OD-107 STATUS: RESOLVED UNDER DELEGATION
OD-107 CHECK: pending: to be checked by a different instance

**OD-108 (AU-13, are "expert consensus" values thin or grey?): mostly answered by the ledger. The remainder goes on the "Not yet ruled" list and is not asked now.**
- **Answered by the ledger:**
  - A clinician's vetted professional judgment is not thin. The owner's words: "this is not thin. a clinician has rendered a professional judgment that has been vetted by colleagues based upon available information" (7105).
  - A derivation by a clinician or academic counts: "derivation by a clinician or academic counts" (7141).
  - Grey follows `evidence_type`, and every grey basis takes ⚠ (OD-64, 7424).
  - A statement no source makes is the project's own and thin: "we aren't clinicians so it is flagged as thin" (7123).
- **The remainder.** A consensus of experts who are neither clinicians nor academics is added to `governance/tier-system.md` line 80's "Not yet ruled (owner)". Marking is delegable; ruling is the owner's (§2.4 item 3).
- **Callers repointed to §5:** `skills/evidence-auditor_SKILL.md` line 47 and `references/methodology-evidence-hierarchy-mapping.md` line 163. Both still put `[EXPERT CONSENSUS]` at ○.
- **No live cell is known to need it** [UNVERIFIED: no column marks expert consensus].

OD-108 STATUS: RESOLVED UNDER DELEGATION
OD-108 CHECK: pending: to be checked by a different instance

**OD-109 (AU-20, Definition-of-Done lines D-02 and D-13): referred back to the owner. The two retired tasks are restored as stopped tasks meanwhile.**
- **The record.**
  - D-02 ("…and a lost path is seen", `REMEDIATION-WORKPLAN.md` line 1416) asks for the walkability gate. It traces to the owner's OW-2, "Yes, register it" (4731). The recorded reading registers `walkability.py` "as the stage-pair gate" (4761, item 10).
  - D-13 ("flexible: the base changes by data alone", line 1426) traces to the owner's "pipeline must be flexible" (5307) and "and that means pipeline must not have hard coded behaviours" (5322).
  - Their tasks, T-038 (traces to IMP-07) and T-047 (traces to REQ-102, AT-104; `git show 253c2dcc:workplan/2026-11-12-bidirectional-pipeline/tasks/T-047-add-by-data-test.md`, line 17), were deleted in PR #249.
  - The owner's merge ratifies what it carries but "never supplies an owner-only decision" (585 and its limit). Withdrawing an owner request is the owner's.
- **The question.** Are the walkability gate and the by-data flexibility test still wanted?
- **Options and consequences.**
  - (a) Yes, later. Both tasks are restored, stopped, and the lines stay.
  - (b) Withdraw the gate only. The OW-2 reading itself notes that pairs ending at render print NO PATH by construction (4761). D-02 is reworded and T-047 restored.
  - (c) Withdraw both. The lines are reworded to record it.
- **Recommended:** (a). Nothing is built now, and nothing the owner asked for is withdrawn.
- **Meanwhile (delegated, as for T-039 in OD-106).** Restore both task files from `253c2dcc` with "NOT FOR SONNET" in the Executor cell, so the generator stops them. D-02 and D-13 stay as written. Separately, the dead links at `REMEDIATION-WORKPLAN.md` lines 1257, 1282, 1518, 1586 and 1592 point at T-128 (withdrawn by OD-87), T-005 and T-122, not at T-038 or T-047 (test each linked path with `[ -e ]`). They are repointed to `git show 253c2dcc:<path>`.

OD-109 STATUS: REFERRED BACK TO THE OWNER
OD-109 CHECK: pending: to be checked by a different instance

**OD-110 (what PR B part 1 can start now; dependency edits): T-117 and T-056 item 3a start now. The T-059 selection slice waits. T-124's precondition is narrowed. T-123 is a gap, not a task step.**

*Starts now* (each checked against its task file's §2):
- **T-056 item 3a** (`design_scale` from the key).
  - §2 requires T-054, which is merged (`grep -c 'T-054-identity-retires-to-need' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-PLAN.md` finds it in the Merged list).
  - Its owner decisions OD-31 and OD-48 are answered (7995-7996).
  - The plan shows T-056 READY.
- **T-117** (the marker table; the CHECK widened to ⚠ with no ordinal; the regulatory override deleted; the marker from the stating sources (OD-59); OD-92's refusal and OD-99's interim; C10 as OD-99 states it).
  - Its owner decisions OD-57, OD-59 and OD-64 are answered (7327-7334, 7424).
  - Its §2 requires T-119, T-120, T-068 and T-102. T-119 is merged. The other three are dropped under this ruling (ordering, OD-79):
    - T-120: the doctrine T-117 builds to is on main in `governance/tier-system.md` §5 (PR #248). T-120's `evidence-architecture.md` §0 is the selection rule's home, which T-117 does not build.
    - T-102: it was added so PROXY-thin is tested on WHEEL cells, and PROXY-thin is not built (OD-98).
    - T-068: it was ordered first only because both edit `determine`. T-068 itself waits for T-059 and T-120, so it follows T-117 and re-runs T068-10.
- **PR B part 2 (IV), the deferred-search flag.**
  - Its ruling, OD-45, is delegated and its check confirmed (6387-6397).
  - It has no task file of its own [UNVERIFIED]. It is T-081's tooling.
- **Also now:** T-120 (doctrine tooling; its file's own gates govern) and T-102 (research; OD-83 and OD-84).

*Waits:*
- **The T-059 selection slice, with OD-101.** Its §2 requires T-120, which writes `governance/evidence-architecture.md` §0 (`grep -c -F '## 0.' governance/evidence-architecture.md` prints 0). It also requires T-127, which waits for T-102 and, under OD-89 ACTION (1), for T-149 (OD-91).
- **T-068's cluster step.** Its §2 requires T-059 and T-120.
- **T-124.** Its §2 is narrowed to the T-059 selection slice and T-068's cluster step ("T-059 builds selection in the accessibility direction and the no-direction case this task reuses; T-068 builds the cluster step, with the tolerance in one home, which is the mode"). It waits for both.

*T-110's list for the first cell:*
- T-117, the T-059 slice, T-102 and the T-127 slice;
- OD-91's repairs, including the owner's T-113 act;
- T-124 (OD-90);
- T-086 and T-104 only for parameter 3;
- T-133 dropped: gate 1 is keyed `MOB`, and "a gate on the parent's code does not reach a child's cell" (`scripts/assess/assess_cell.py`, `grep -n "does not reach a child" scripts/assess/assess_cell.py`).

*T-123.*
- OD-71 reads "`direction_ref_id` and `term_aliases.observation_id` become provenance only or are dropped" (8019). The 2026-10-30 ACTION (6) asks for a direction "recorded from an admitted source and not hand-set" (4866).
- `db.py set-parameter-direction` refuses a parameter that "already carries" a direction (`grep -n "already carries" scripts/db.py`), and no other writer sets `direction_ref_id`. So the pointer for parameters 3 and 12 cannot be recorded with existing verbs.
- File it as a gap: a writer change, in a tooling PR (rule 10), with no hand SQL. It is off the first cell's path, because the engine reads `accessibility_direction`, not the pointer. AU-06's rule-5 concern stays open in that gap.

- **Opens:** edits to the T-117, T-124 and T-110 task files, the gap, and a regenerated plan.

OD-110 STATUS: RESOLVED UNDER DELEGATION
OD-110 CHECK: pending: to be checked by a different instance

**OD-111 (`design_scale` prose callers against OD-48): answered by the ledger.**
- **The gate:** "OD-48: whom it is for (the adjudication's recommended default, ratified)", with its status line answered by the owner (7995-7996).
- **What it supersedes, on contact (rule 0):**
  - `governance/evidence-methodology.md` line 144 ("a T4–6-only determination is a *Universal-Mode regulatory determination* — `design_scale='universal'`");
  - `governance/evidence-architecture.md` line 121;
  - atom EVI-331 (`workplan/pipeline-state-graph/ATOMS.tsv` line 1208).
- **The action.** T-120 writes SUPERSEDES back-pointers there.

OD-111 STATUS: ANSWERED BY LEDGER (OD-48; read OD-48's gate)
OD-111 CHECK: pending: to be checked by a different instance

**OD-112 (the in-scope jurisdiction filter): the page shows only P1+P2+P3 jurisdictions.**
- **The owner's words:** "Yes it is P1+P2+P3" and "do not include countries outside of the major identified countries for now" (4835). ACTION (5) reads "Show only in-scope jurisdictions" (4866).
- **The list.** The codes come from `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md` §3. [ASSUMPTION: that file holds the ranking — basis: the ledger's own reading under item 7, unratified.]
- **The home** for scope is `lang_jur_map.scope_status`, NULL on every row (`select count(*), sum(scope_status is not null) from lang_jur_map`). T-036 waits for T-101.
- **Parameter 12.** C1(12)'s jurisdictions are all in the HANDOFF list, so the filter changes nothing. The page states the rule, and the reviewer checks it.
- **Parameter 3.**
  - C1(3) names UG and INT, so T-101's scope rows and T-036's query are on parameter 3's path.
  - REF-00994 (IPC) is filed `INT` and is not a comparison row, though it stays a source (OD-99).
  - REF-01014 is a 2007 draft and fails "current editions only" (2026-10-30 item 7).
- **No list is typed into the page** (CLAUDE.md rule 8).

OD-112 STATUS: RESOLVED UNDER DELEGATION
OD-112 CHECK: pending: to be checked by a different instance

**OD-113 (contested population-match grades): the page prints every grade row. The engine is not changed now.**
- **The defect.** `assess_cell.population_match` returns the lowest `match_id`. For REF-01012 to REF-01017 that is a PARTIAL grade, which a later PROXY row's `mismatch_note` calls a misapplication of a 2026-09-25 owner ruling (`prb-antagonist-2.md` claim 6).
- **Why the page shows both.** CLAUDE.md §4 keeps both rows ("divergent grades read as a contest").
- **The page** prints both and notes which is the later correction.
- **The engine is not changed:**
  - under the WHEEL route, governing sources are graded afresh;
  - no output reads the grade while Q3 is unanswered [UNVERIFIED: not every engine branch was audited; check before PR B part 1 merges].

OD-113 STATUS: RESOLVED UNDER DELEGATION
OD-113 CHECK: pending: to be checked by a different instance

CONDITION: any session building PR B (T-117, T-056 3a, the T-059 slice, the deferred-search flag, the page), T-124 or T-068's cluster step, T-102, T-127, T-110, or the governance pull request; any session asking which cell is published first, which unverified sources govern and how they are marked, or whether the four figures may be left off a page.

ACTION:
1. Treat OD-90 and OD-111 as pointers to OD-63 and OD-48, and read those gates.
2. Start T-117 and T-056 item 3a as OD-110 states. Hold the T-059 slice until T-120 and T-127 have merged.
3. Run OD-91's test before T-110, and publish nothing before it.
4. Put OD-92, OD-94, OD-96, OD-97, OD-99, OD-100, OD-104, OD-105 and OD-109, the T-113 owner act and Q3 to the owner in plain form.
5. Write no "Owner" heading for D1 without the owner's typed words.
6. Re-derive every figure by its command.
7. Treat the readings here as delegated, not as the owner's.

DATE: 2026-11-27 — delegated resolutions, revised after an independent check; checks pending; not an owner statement.

---

## Part C. Notes for the coordinator (not ledger text)

1. **Record the owner's words first** (rule 0), in one "Owner statements" entry before this block: the owner's 2026-11-27 grant and the 2026-11-26 CLAUDE.md audit instruction.
2. **Still unverified:**
   - whether any engine branch besides the marker reads `population_match` (OD-113);
   - whether the T-127 slice needs an ICF code `base_icf` lacks (OD-91);
   - whether conditioned run-length rows belong in T-124's four figures. Most of parameter 12's rows are gradient-conditioned branches: `prb-antagonist-1.md` row 1a; re-derive from `extraction_relations`. This is a T-124 design point to settle before page one;
3. **The D1 draft** is `d1-identification-entry-draft.md`, for the owner to adopt or amend. Do not append it without the owner's words.
4. **Not ruled, because not asked:** AU-22 (T-122's deletion) and the other PR #249 deletions (T-005, T-085). Check each against the owner's words as OD-106 and OD-109 did.
