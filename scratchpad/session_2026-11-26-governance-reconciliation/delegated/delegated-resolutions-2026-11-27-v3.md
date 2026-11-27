# Delegated resolutions 2026-11-27 (v3): the owner's summary, then draft ledger text

Version 3 applies both checks: `checker-delegated-resolutions.md` and `checker-v2.md`. Versions 1 and 2 are left as they were.

- **Repository.** `origin/main` is `b3b3e9b6` and HEAD is `807e7c8c`. The commits between them carry only session logs and scratchpad copies (`git diff --stat b3b3e9b6 807e7c8c`), so the ledger is identical on both. Ledger line numbers below are `references/project-standards.md`.
- **Database.** Opened read-only (`file:data/guidebook.db?mode=ro`, `PRAGMA user_version` 167) and not changed.
- **Method.** Nothing was edited, committed or appended. Every figure is given as the command that computes it (CLAUDE.md rule 7a). The owner's words are quoted, and my readings are marked [ASSUMPTION]. Anything I did not check is marked [UNVERIFIED].

---

## Part A. For the owner: one page

**What I ruled (no answer needed).**
1. **The first page keeps your four figures.** You answered OD-63; it is not a question (OD-90). A delegate may not show the figures computed over only the figures that can be read.
2. **Which cell goes first** is fixed by a test, run after the mobility figures are carried to wheelchair users (OD-91). On today's data the test favours ramp run length (parameter 12): every one of its code figures can be read, and every code body it names is in your OD-04 scope. Ramp gradient follows.
3. **Tooling that can start once this ruling's check is confirmed and four task files are edited (OD-110):**
   - the marker table (T-117);
   - `design_scale` taken from the cell's key (T-056 item 3a);
   - a deferred-search flag, which has no task file yet.

   T-117's own file still requires four tasks merged first. Dropping that requirement needs OD-110's check *and* an edit to that file, and the edit has not been made. The selection change (the T-059 slice) and the four-figure tooling wait for T-120 and T-127.
4. **An unverified Co-1 source may govern on the same terms as an unverified T1 source.** A Co-1 research publication counts under your harm test as a T1 one does (OD-93, OD-101).
5. **Smaller items.**
   - The harm record waits for its own pull request (OD-102).
   - The engine's "proxy" flag does not by itself make a value thin (OD-98).
   - "Expert consensus" is mostly answered by your rulings on thin (OD-108).
   - Three conflicts in the inputs are ruled (OD-111 to OD-113).

**What waits on you** (recommended answer first; what continues meanwhile after it):

| # | Question | Recommended | Meanwhile |
|---|---|---|---|
| OD-92 | Several sources state the shown value, with different markers: which marker does the value take? | The strongest verified, non-grey marker; ⚠ only if every stating source is grey or unverified | The engine refuses such a cell. **Ramp gradient waits.** |
| OD-94 | Under your harm test, do these count: an advocacy organisation's statement, a grey report, a national (T2) standard, an international (T4) standard? | Yes to the first three; no to T4 | Nothing is built |
| OD-96 | May a code-only cell below doctrine's richness threshold show its value as "provisional"? | Yes | Such a cell stays "pending"; none is on the path |
| OD-97 | May a grey-only cell show its value, marked ⚠, as "provisional"? | Yes | Stays pending; none is on the path |
| OD-99 | (1) A source that was retrieved but whose identity is not confirmed: ⚠, or its tier's circle? (2) How does the record show "could not be retrieved"? | (1) ⚠. (2) No logged retrieval of the document, or a record saying it was not obtained | These sources are kept and govern. A cell whose shown value one of them states is refused. **Ramp gradient waits.** |
| OD-100 | May a source that could not be retrieved, and has no route, govern a value? | No: it is shown with ⚠ but does not govern (low confidence) | It is shown and excluded |
| OD-104 | (i) Is a page built from the database on request, and never committed, allowed? (ii) May the audience lens come later? (iii) Does a private page you read meet DR-2026-08-19 §4? | Yes to all three | The page is built as a DRAFT. **Nothing is called published.** |
| OD-105 | Who may write the "Owner" entry naming TRIPLE-53, -57 and -61, which the retirement tool needs? | You type one line; a draft is ready | D1 is not carried out |
| OD-106 | Did your "PRA" withdraw your 2026-10-28 request to edit the tables (task T-039, deleted in PR #249)? | No; restore T-039, stopped | Nothing is restored |
| OD-107 | PR #248, which you merged, also dropped the stage-transition doctrine recheck, which item B5 did not name. Keep it dropped? | Restore it | It stays dropped |
| OD-109 | Two done-lines trace to your words ("Yes, register it"; "pipeline must be flexible"), and their tasks were deleted under "PRA". Withdraw them, or restore the tasks? | Restore, stopped | Nothing is restored |
| Q3 (slate) | Does a PROXY grade, or a lens assigned by contextual judgment, make a value thin? | Neither, unless the step across groups is the project's own conjecture | T-117 derives no thin from either |

Q2 is answered by the ledger. Q5's six held tasks stay with you.

**Slate corrections.**
- Q-B2's card says the refusal "does not fire" on parameter 3. It fires on 3 × MOB.
- Q1's card omits T-059 and T-068, which T-124 requires.

---

## Part B. Draft ledger text

> DRAFT only. Append it after the owner's 2026-11-27 words are recorded (Part C). The text holds no "Owner" heading and no `ANSWERED BY THE OWNER` line, and it relaxes no guard.

## Delegated resolutions 2026-11-27 — the first page and its order; marker, route and harm rules for PR B; questions referred back (OD-90 to OD-113)

Written by an Opus-class adjudicator under the owner's words of 2026-11-27, "Opus to resolve conflicts like Q1 and others", within OD-79 (8503). Two independent checks were applied. **Not an owner statement.**

Inputs are committed under `scratchpad/session_2026-11-26-governance-reconciliation/`: `slate/decision-slate.md`; `prb/prb-design-1.md`, `prb-design-2.md`, `prb-antagonist-1.md`, `prb-antagonist-2.md`; `audit/audit-session-work.md`; and `remediation-classification/resolution-plan.md`, `path-to-one-determination.md` and `antagonist-4.md`.

Status values below are the convention's (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). An item that is not a question says so in its body.

**Commands used.** Run from the repository root, read-only.
- **C1(P)**: the code-stratum quantity figures of parameter P, how many `dbcore.figure_refusal` refuses, and the jurisdictions they name:
  `python3 -I -c "import sys,sqlite3;sys.path.insert(0,'scripts');import dbcore;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);q=dbcore.QUANTITY_CLAIM_TYPES;r=[v for v in c.execute('select x.claimed_value,x.claimed_unit,x.comparator,x.claim_type from source_value_extractions x join evidence_sources e using(ref_id) where x.parameter_id=P and x.retired_at is null and e.tier>=4').fetchall() if v[3] in q];print('quantity',len(r),'refused',sum(1 for v in r if dbcore.figure_refusal(c,*v)),'bodies',sorted({j for (j,) in c.execute('select distinct e.jurisdiction from source_value_extractions x join evidence_sources e using(ref_id) where x.parameter_id=P and x.retired_at is null and e.tier>=4')}))"`
- **C2**: `select ref_id, tier, evidence_type, jurisdiction, verification_method, standard_number, superseded_by_ref_id from evidence_sources where verification_status='UNVERIFIED'`
- **C3(ref)**: `retrieval_log.manifest_lines_for(ref_id, url, doi)`. Read each line yourself: the log does not type whether a line is the document, an index record or a probe.
- **C4**: `select ref_id, role from specification_source_links where specification_id = <the cell>`, run on a scratch copy after the engine has written the cell.

**OD-90 (Q1, the four figures on the first page).** This is not a question: it is answered at OD-63.
- The owner's words (7399): "1. good point. all values when synthesizing and making determinations, but on the render page itself, we just have the minimum, mode, median and maximum colour coding the jurisdiction code bodies that we surveyed for comparison purposes". The gate is at 7421-7422, and ACTION (5) at 7434 reads "T-124 and T-037 follow OD-63".
- A delegate may not show the four figures computed over only the figures that parse, even with a count of those left out. Whether those are the figures the owner described is the owner's meaning (OD-79).
- C1(3) prints how many figures are refused today. Any refused figure could be the true minimum or maximum.
- T-124 joins the page's path. The narrowing of its §2 precondition is a task-file edit owed under OD-110.

OD-90 STATUS: RESOLVED UNDER DELEGATION
OD-90 CHECK: pending: to be checked by a different instance

**OD-91 (Q4, the first cell and the order of work): a test picks the first cell, after T-102 and the T-127 slice have run.**
- **Basis.** RULE (1184-1187): "As to 'mobility', separate out into 'ambulatory' and 'wheelchair user' to start", marked "not to be relitigated". The recorder's analysis there names gradient and run length together (1197-1199). [ASSUMPTION: neither ramp cell may therefore be keyed on MOB.] The cells follow T-102 (OD-83, 8608; carry-only under OD-84, 8614).
- **The test.** Run the engine for 3 × WHEEL and 12 × WHEEL on a scratch copy. The first cell is the one that meets all four conditions:
  1. the engine composes a value;
  2. no refusal names an open owner question (OD-92, OD-99);
  3. C1(P) shows no refused figure, so OD-63 can be met in full;
  4. every jurisdiction C1(P) prints is inside OD-04's scope.

  OD-04's gate reads: "OD-04: scope = P1+P2+P3 as recorded; UN: out; sub-national: counts toward its country" (5947-5948). If neither cell passes, report to the coordinator. Whether either cell keeps a value at WHEEL is [UNVERIFIED].
- **Sub-national codes.** OD-04's "sub-national: counts toward its country" applies here. [ASSUMPTION: the page's comparison shows a sub-national instrument under its country and names the instrument — basis: OD-04's own settles line (5949) includes "page".] Page one therefore does not wait on T-113's sub-national codes. Those codes would need an "Owner" approval entry: `db.py add-jurisdiction` calls `_owner_approval`.
- **Why parameter 12 is likely first.** The owner's words: "I think the issue is not the slope of the ramp, but the lack of a rest landing" (4836). [ASSUMPTION: parameter 12 measures that run — basis: its `notes`.]
- **Order of work** (tooling before the data that uses it, CLAUDE.md rule 10):
  1. the tooling OD-110 lists and T-102;
  2. the T-127 slice, which waits for T-102 and, under OD-89 ACTION (1) (8639), for T-149. T-149 has no task file, and OD-88, which opens it, has a pending check (8632);
  3. the T-059 slice, then T-068's cluster step, then T-124;
  4. the page;
  5. the chosen cell's repairs;
  6. T-110.
- **The chosen cell's repairs, if it is parameter 12:**
  - extraction 141 under GAP-372 (`select description from gaps where gap_id='GAP-372'`);
  - population-match grades against WHEEL;
  - T-123 cannot run with existing verbs (OD-110).
- **Duplicates.** GAP-376 names REF-01026 with REF-01032, and REF-01019 with REF-01031 (`select description from gaps where gap_id='GAP-376'`). REF-01015's edition is a separate defect. To see which of them hold parameter 12 rows: `select distinct ref_id from source_value_extractions where parameter_id=12 and retired_at is null`.

OD-91 STATUS: RESOLVED UNDER DELEGATION
OD-91 CHECK: pending: to be checked by a different instance

**OD-92 (Q-B2: several stating sources carry different markers).**
- OD-59 answered the question as registered at 7273: "od59 yes" (7307). The recorder's reading is at 7319, and the gate at 7333-7334. Neither names one source when several state the value. The owner's "no, triangle instead if the value is coming from grey or unverified" (7053) leaves "coming from" open, and 7059 lists the combined case as undecided.
- This decides what a marker means (`governance/decision-protocol.md` §2.4 item 3).
- Options:
  - (a) The strongest marker among the stating sources that are verified and not grey; ⚠ only if every stating source is grey or unverified. Adding a source never lowers the marker.
  - (b) The weakest marker. A newly found unverified source would demote a verified code's ○.
  - (c) Leave it open.
- Recommended: (a).
- Meanwhile: the engine refuses the cell and names this question. That blocks 3 × MOB, not 12 × MOB.

OD-92 STATUS: REFERRED BACK TO THE OWNER
OD-92 CHECK: pending: to be checked by a different instance

**OD-93 (Q-B3, Co-1 research publications): a Co-1 source that is a research publication counts under OD-58 as a T1 research publication does.**
- Basis:
  - the owner's OD-58 words (7305): "od58 research publication or clinical guidelines state …";
  - the owner's "Co-1 and T1 are same value" (6176);
  - the recorder's reading, Co-1 "read as yes … flagged" (7318), held open at 7325;
  - `governance/mission-and-epistemics.md` lines 50 and 91 (Co-1 forms include "peer-reviewed lived-experience literature");
  - CLAUDE.md line 374.
- A peer-reviewed lived-experience paper is a research publication in the owner's plain words, so this ruling applies the words and decides no further meaning. Other Co-1 forms go to OD-94.
- This constrains the harm-record pull request (OD-102).

OD-93 STATUS: RESOLVED UNDER DELEGATION
OD-93 CHECK: pending: to be checked by a different instance

**OD-94 (Q-B3, the rest).**
- Which of these count as "research publication or clinical guidelines" (7305): a Co-1 statement that is not a research publication; a T3 grey report; a T2 `standard_eb`; a T4 `standard_eb`?
- It is held open (7318, 7325), so it is the owner's meaning.
- The live harm sentence is extraction 77. Its source shows with `select ref_id from source_value_extractions where extraction_id=77`, then C2.
- Options:
  - (a) All four count.
  - (b) The first three count; T4 does not. T4 is the code side of "if so, research wins. if no, code wins" (7177).
  - (c) Only Co-1 counts.
  - (d) None counts.
- Recommended: (b).
- Meanwhile: nothing is built (OD-102).

OD-94 STATUS: REFERRED BACK TO THE OWNER
OD-94 CHECK: pending: to be checked by a different instance

**OD-95 (Q-B4, the academic-route record): do nothing now.**
- No cell on the path holds an unretrievable T1 to T3 source. REF-01002 (C2: `corroborated-not-retrieved`) is not gathered for either ramp cell.
- When a live case arises, what counts as a "valid academic route" is settled then, or put to the owner. The recorder's reading at 4758 is unratified and is not adopted here.
- Meanwhile, a route-less unretrievable T1 to T3 source does not anchor, from the owner's word "only" (4725). OD-100 holds the rest of that question.

OD-95 STATUS: RESOLVED UNDER DELEGATION
OD-95 CHECK: pending: to be checked by a different instance

**OD-96 (Q-B5, code half).**
- `governance/evidence-methodology.md` line 144 makes a T4–T6-only cell `provisional` only when it is "rich enough". The owner's words (U6, 7875): "if the only values are from code then code determines the ideal/best".
- Does U6 let a code-only cell below the richness threshold show its value as `provisional`? That is the owner's meaning.
- Options:
  - (a) Yes, with its tier's marker (7195).
  - (b) No; it stays `pending`.
- Recommended: (a).
- Meanwhile: such cells stay pending, and none is on the path. To list them, re-run `prb-antagonist-1.md`'s `union.py`.

OD-96 STATUS: REFERRED BACK TO THE OWNER
OD-96 CHECK: pending: to be checked by a different instance

**OD-97 (Q-B5, grey half).**
- A grey-only cell stays `pending` (DR-2026-07-12 item 2). The owner's words: "let's return to keeping them but they get a triangle warning" (7005) and "2 triangle for all" (7401).
- Does such a cell show its value, marked ⚠, as `provisional`?
- Options:
  - (a) Yes.
  - (b) No value until a non-grey source exists.
- Recommended: (a). [ASSUMPTION: "presents all values" (6836) reaches these cells.]
- Meanwhile: such cells stay pending; none is on the path.

OD-97 STATUS: REFERRED BACK TO THE OWNER
OD-97 CHECK: pending: to be checked by a different instance

**OD-98 (Q3b): `rests_on_proxy_inference` is not, by itself, a thin cause.**
- A value is thin under the project-inference cause only when no source in the lens states it. The owner's words: "because if it mixes then it's a new value proposed for something so it's conjecture because we don't have authority" (7159).
- The 3 × MOB headline (1:20, 5 %) is stated by extraction 25 (REF-00992) and extraction 28 (REF-00994). It is also stated by extraction 30 (REF-00995), whose stored quote is truncated (GAP-372).
- Not decided here; it goes with Q3: a PROXY grade (7093; `governance/tier-system.md` line 80), and a lens assigned by contextual judgment under OD-65 (7403). T-117 derives thin from neither.

OD-98 STATUS: RESOLVED UNDER DELEGATION
OD-98 CHECK: pending: to be checked by a different instance

**OD-99 (the route gate and C10): two questions for the owner.**
- **The record.**
  - The owner's words of 2026-10-21 (4540): "if we can't retrieve a study, then we can't verify it as a primary source, which means that we can't claim it as a top tier. add unverified in this context where something can't be retrieved to the empty circle alongside grey or thin".
  - The recorder's gloss (7007): "*Unverified*: a source that could not be retrieved".
  - `governance/tier-system.md` line 70: "unverified (the source could not be retrieved)".
  - OR-23 is the owner's "Confirm -- This applies only when the source is properly cited in an academic context" (4725). The recorder's statement of what was confirmed, "an unretrievable source keeps its tier and may still anchor", is at 4758. OR-23b is at 6186.
- **Question 1.** A source that was retrieved and logged but is stored UNVERIFIED, its identity or edition unconfirmed: when it states the shown value, does the value carry ⚠ or its tier's circle?
  - (a) ⚠.
  - (b) Its tier's circle.
  - Recommended: (a). [ASSUMPTION: an unconfirmed identity carries the CLAUDE.md §5(c) risk.] The owner's words tie "unverified" to retrieval, so confidence is low to medium.
- **Question 2.** How does the record show "could not be retrieved"?
  - (a) C3 is empty. This misreads REF-01002 as retrieved, because the log counts index records.
  - (b) No logged retrieval of the document, or `verification_method` in (`corroborated-not-retrieved`, `citing-bibliography`).
  - (c) A field the verifying session sets.
  - Recommended: (b).
- **Meanwhile** (ordering, reversible):
  - The governing sources that C2 and C3 show as retrieved but UNVERIFIED (re-derive with C2, C3 and C4) are kept and may govern without a route. OR-23 and OR-23b speak of unretrievable sources (4758, 6186).
  - **Which marker those sources carry is the owner's to say.** A cell whose shown value one of them states is refused, naming this question. That blocks 3 × MOB, where extraction 28 is REF-00994's. Whether REF-01019 (superseded by REF-01031, per C2) governs 3 × MOB is [UNVERIFIED].
  - The interim test for "could not be retrieved" is Question 2's (b). A source that fails it and has no route is shown and excluded (OD-100).
  - Some unverified sources carry their standard number only in `pub_title` (C2's `standard_number` column against the title). That is a `correct-source` data fix. The gate never parses titles.
  - C10 meanwhile fails a live cell when a governing source fails the interim test and has no route, or when every governing source is non-VERIFIED or grey and the marker is a circle.

OD-99 STATUS: REFERRED BACK TO THE OWNER
OD-99 CHECK: pending: to be checked by a different instance

**OD-100 (a source that could not be retrieved and has no route).**
- **The record.**
  - The owner on 2026-10-21 (4540) put such a source's value at a marker.
  - OR-23 on 2026-10-29: "only when the source is properly cited in an academic context" (4725).
  - `governance/tier-system.md` line 77: "without one it anchors nothing". This is the recorder's reading written as rule (AU-14).
  - On 2026-11-14 the owner wrote "let's return to keeping them" (7005).
- **Question.** May such a source govern a value, marked ⚠?
  - (a) No: it is shown and listed, but does not govern.
  - (b) Yes. 4540 and 7005 lean this way.
  - Recommended: (a), with low confidence. [ASSUMPTION: "keeping" answered whether such sources stay in the book (7009).]
- **Meanwhile:** (a), which is reversible. It reaches REF-00997 (C2), on parameter 3 only.

OD-100 STATUS: REFERRED BACK TO THE OWNER
OD-100 CHECK: pending: to be checked by a different instance

**OD-101 (the eligibility union): an unverified Co-1 source is eligible to govern on the same terms as an unverified T1 source.**
- The correction to `prb-design-1.md` §2.3 item 1 adds `b.get("co1_unverified", [])` to the union. It rests on "Co-1 and T1 are same value" (6176) and CLAUDE.md lines 366 and 373.
- Eligibility is not the `stated` threshold. `governance/evidence-methodology.md` §2.2 condition 3 still requires a VERIFIED Co-1 source for `stated`; condition 1 has no such clause for T1. That asymmetry is noted for the owner and not changed.
- Today C2 lists no Co-1 source.
- This waits with the T-059 slice (OD-110).

OD-101 STATUS: RESOLVED UNDER DELEGATION
OD-101 CHECK: pending: to be checked by a different instance

**OD-102 (the harm record): deferred to a tooling pull request that lands with or before T-125's capture path.**
- The ledger requires it: "T-059 builds the selection with the OD-58 standard" (7343).
- **The live writer.** `db.py add-extraction --harm-finding` refuses a harm flag without an `insufficient` edge in the same call (`grep -n "needs an \`insufficient\` edge" scripts/db.py`). So it records harm at the less accommodating value, the opposite of OD-58's statement.
- **Nothing reads it.** `grep -c harm_finding scripts/assess/assess_cell.py` prints 0.
- **No row is flagged.** `select harm_finding, count(*) from source_value_extractions group by 1` shows 0 only.
- No OD-58 statement can be recorded today, so none is ignored. Building the record now would serve nothing (CLAUDE.md line 506).

OD-102 STATUS: RESOLVED UNDER DELEGATION
OD-102 CHECK: pending: to be checked by a different instance

**OD-103 (the page: method only).**
- The page is a pure function over one read-only connection. It is written outside the repository by `owner_browser_build.py`'s guard and is never committed.
- `translations_shown()` and `cell_status()` must take that connection, or the page refuses when `--db` and `GUIDEBOOK_DB_PATH` differ. "DRAFT" prints when `dbcore.is_canonical` is false.
- It carries:
  - DR-2026-08-19 §4's elements;
  - T-124's figures;
  - in-scope rows (OD-112);
  - originals beside their reviewed English;
  - every grade row;
  - the stored marker.
- It prints no engine prose or `design_scale`, and claims no accessibility test that was not run (4866).
- The page may be shown to the owner privately as a DRAFT review copy (precedent at 4584). Whether that form is allowed, and whether it counts as published, are OD-104's questions.

OD-103 STATUS: RESOLVED UNDER DELEGATION
OD-103 CHECK: pending: to be checked by a different instance

**OD-104 (the page: the owner's meanings).**
- **(i) Is an on-request page allowed?**
  - The owner's words: "the entire pipeline is dynamic rendering on site" and "do not rely on artifacts for rendering the site" (1658), and "i want it to be coming from database directly in ideal world" (4840). ACTION (3) at 4866 reads "do not restore a static generator"; its "committed HTML" narrowing is the recorder's [ASSUMPTION].
  - Options: (a) a page built from the database on request, never committed, is allowed; (b) it is not.
  - Recommended: (a).
- **(ii) May the audience lens come later?**
  - The owner's words: "There is an audience lens (the four audiences) and a disability lens" (4841).
  - Options: (a) the disability lens now and the audience lens with the first audience-specific content, said on the page; (b) both now.
  - Recommended: (a).
- **(iii) Does a private page meet DR §4?**
  - Does a private page the owner reads meet DR-2026-08-19 §4's "rendered and readable as output"? (a) Yes; (b) no.
  - Recommended: (a).
- Meanwhile: the page is a DRAFT, and nothing is called published.

OD-104 STATUS: REFERRED BACK TO THE OWNER
OD-104 CHECK: pending: to be checked by a different instance

**OD-105 (carrying out "D1 retire": who may author the entry the tool needs).**
- **What the guard checks.** `review_identity_need_icf` requires a heading that begins "Owner" (`_owner_approval`) and an entry whose text names each row as `TRIPLE-<id>` (`dbcore.ledger_entry_names`, which reads one entry whose heading occurs once). It checks the heading's form and the tokens, **not** that the words are the owner's. A placeholder entry would pass once dated.
- **What the ledger says.** The guard was added "so that no session states its own row" (8490). The owner's answer (`git grep -n -F "D1 retire" -- references/project-standards.md`) sits in an entry with no TRIPLE token.
- **The rows.** `select triple_id, identity_code from identity_need_icf where need_code='A-SIZE' and icf_code='e120' and retired_at is null`.
- **A recorded departure.** The 2026-11-26 ACTION (3) (8671) says to cite "this entry" as the approval reference. Any route below cites a new entry instead, and that departure must be recorded.
- **Options:**
  - (a) The owner types one line naming or adopting the rows. It is recorded with the draft in `d1-identification-entry-draft.md`, which is separate from this block.
  - (b) The owner rules that a recorder may name rows the owner described.
  - (c) Leave D1 undone.
- **Recommended:** (a).
- **Meanwhile:** nothing is retired. Nothing on the path reads `identity_need_icf` (OD-85, 8592).

OD-105 STATUS: REFERRED BACK TO THE OWNER
OD-105 CHECK: pending: to be checked by a different instance

**OD-106 (T-039, the owner's edit request).**
- **The request.** The owner's words: "I need there to be some kind of interface where I can manually review and edit the different table values/information and have it propagate accordingly" (4580). ACTION (1) reads "then edits as proposals" (4589).
- **The deletion.** T-039 was deleted under resolution-plan PR A item 2, which the owner approved by typing "PRA" (`git grep -n -F '"PRA"' -- transcripts`). The owner then merged PR #249.
- **The merge rule.** RULE (582) says a merge ratifies what it carries, "UNLESS the owner explicitly notes otherwise". Its ACTION (4) (584) reads: "Do not use this rule to auto-complete DG-NON substance the owner never decided, to skip named external preconditions, or to promote evidence-maturity states".
- **Why it is the owner's.** The deletion rested on the premise "no owner request found", which is false (AU-01). Whether "PRA" withdrew the 2026-10-28 request is the owner's meaning.
- **Options:**
  - (a) Not withdrawn: restore T-039.
  - (b) Withdrawn.
- **Recommended:** (a), with T-039 stopped by its Executor cell ("NOT FOR SONNET"). The generator's `status()` reads only closed gates, missing design files and that cell; a "DEFERRED" line stops nothing. Note the owner's 2026-11-21 words, "We don't need a tool for many qualitative judgments/corrections because Claude IS a tool".
- **Meanwhile:** nothing is restored.

OD-106 STATUS: REFERRED BACK TO THE OWNER
OD-106 CHECK: pending: to be checked by a different instance

**OD-107 (AU-04, the doctrine-recheck triggers).**
- **The 25-session trigger is answered.** Item B5, which the owner approved ("approve A and B all", 8656; ACTION (1), 8671), reads "'every 25 sessions' was abolished by DR-2026-08-19 section 10 item 4". `governance/doctrine-recheck.md` §1.1 and its "Two remain" line are owed a pointer to that approval.
- **The stage-transition trigger is referred.** It was also dropped by commit 183a6d66 in PR #248, which the owner merged. B5 did not name it. Under RULE 582 the merge ratifies what it carries, unless DG-NON (584). Cadence is not on the §2.4 list.
- **Question.** Keep the stage-transition recheck dropped?
  - (a) Restore it.
  - (b) Keep it dropped, and amend doctrine-recheck.md §1.2 to match.
- **Recommended:** (a). The approved item named only the 25-session trigger.
- **Meanwhile:** it stays dropped.

OD-107 STATUS: REFERRED BACK TO THE OWNER
OD-107 CHECK: pending: to be checked by a different instance

**OD-108 (AU-13, expert consensus): mostly answered by the ledger.**
- **Answered:**
  - a clinician's vetted professional judgment is not thin (7105);
  - "derivation by a clinician or academic counts" (7141);
  - grey takes ⚠ (OD-64, 7424);
  - the project's own inference is thin (7123).
- **Remainder:** consensus of experts who are neither clinicians nor academics. It is added to `governance/tier-system.md` line 80's "Not yet ruled (owner)".
- **Callers owed a pointer to §5,** each still putting expert consensus at ○ (`grep -n -i "expert consensus"` on each file):
  - `skills/evidence-auditor_SKILL.md`;
  - `references/methodology-evidence-hierarchy-mapping.md`;
  - `governance/armature_v4.md`;
  - `references/case-study-compendium.md`.
- No live cell is known to need it [UNVERIFIED].

OD-108 STATUS: RESOLVED UNDER DELEGATION
OD-108 CHECK: pending: to be checked by a different instance

**OD-109 (AU-20, done-lines D-02 and D-13).**
- **The record.**
  - D-02 traces to the owner's OW-2, "Yes, register it" (4731). The recorded reading registers walkability as "the stage-pair gate" (4761).
  - D-13 traces to "pipeline must be flexible" (5307) and "and that means pipeline must not have hard coded behaviours" (5322).
  - Their tasks, T-038 and T-047 (`git show 253c2dcc:workplan/2026-11-12-bidirectional-pipeline/tasks/T-047-add-by-data-test.md`, "Traces to"), were deleted under PR A item 2, approved by "PRA" and merged in PR #249. The merge limit is RULE 582 with its ACTION (4) at 584.
- **Question.** Are the walkability gate and the by-data test still wanted?
  - (a) Yes, later: restore both tasks, stopped.
  - (b) Withdraw the gate only. The OW-2 reading itself notes that render pairs print NO PATH by construction (4761).
  - (c) Withdraw both.
- **Recommended:** (a).
- **Meanwhile:** nothing is restored, and D-02 and D-13 stay. The dead links in `REMEDIATION-WORKPLAN.md` point at T-128, T-005 and T-122, not at these tasks (test each link with `[ -e <path> ]`). They are repointed to `git show 253c2dcc:<path>`.

OD-109 STATUS: REFERRED BACK TO THE OWNER
OD-109 CHECK: pending: to be checked by a different instance

**OD-110 (what can start, and the task-file edits owed).**
- **T-056 item 3a.** Its §2 needs T-054, which is merged (the plan's Merged list), and OD-31 and OD-48 are answered. It is READY in the plan.
- **T-117.** Its §2 still requires T-119, T-120, T-068 and T-102 merged; T-119 is merged. This ruling drops the other three, as an ordering decision:
  - T-120: the marker table is already doctrine in `governance/tier-system.md` §5 (PR #248).
  - T-102: it was needed only for PROXY-thin, which is not built (OD-98).
  - T-068: it waits for T-059 and T-120 itself, so it follows T-117.

  T-117 starts only once **both** this ruling's check is confirmed and T-117's §2 is edited.
- **The deferred-search flag.** This is `amend-search --set-deferred-reason`, together with the converse refusal on `--set-absence-class` (`prb-antagonist-2.md`). It has no task file (`grep -l set-deferred-reason workplan/2026-11-12-bidirectional-pipeline/tasks/*.md` prints nothing). It is not T-081's tooling: T-081 is research. Its ruling OD-45 has a confirmed check (6404). One task file is owed.
- **Also startable now:** T-120 (by its own gates) and T-102 (research).
- **What waits:**
  - The T-059 slice needs T-120 (`grep -c -F '## 0.' governance/evidence-architecture.md` prints 0) and T-127 (OD-91).
  - T-068 needs T-059 and T-120.
  - T-124 needs the T-059 slice and T-068's cluster step.
- **T-123 cannot run.** `set-parameter-direction` refuses a parameter that "already carries" a direction (`grep -n "already carries" scripts/db.py`). This is a gap for a writer change (rule 10). It is off the path, because the engine reads `accessibility_direction`. OD-71's words: "`direction_ref_id` and `term_aliases.observation_id` become provenance only or are dropped" (8019).
- **T-133 drops from T-110 for a WHEEL cell.** `select parameter_id, identity_code from determination_gates` shows the gate's key, and "a gate on the parent's code does not reach a child's cell" (`grep -n "does not reach a child" scripts/assess/assess_cell.py`).
- **Task-file edits owed** (tooling edits, not made here):
  - T-117 §2 (drop T-120, T-068 and T-102, with the reasons above);
  - T-068 §2 (follows T-117);
  - T-124 §2 (narrow to the T-059 slice and T-068's cluster step);
  - T-110 §2 (the first cell's list);
  - a new task file for the deferred-search flag;
  - a register entry for each of OD-90 onward in `REMEDIATION-WORKPLAN.md` §8, so that task files may name them.

OD-110 STATUS: RESOLVED UNDER DELEGATION
OD-110 CHECK: pending: to be checked by a different instance

**OD-111 (`design_scale` prose against OD-48).** This is not a question: it is answered at OD-48 (7995-7996, "whom it is for").
- The following are superseded on contact (rule 0) and are owed SUPERSEDES back-pointers under T-120:
  - `governance/evidence-methodology.md` line 144;
  - `governance/evidence-architecture.md` line 121;
  - atom EVI-331 (`grep -n EVI-331 workplan/pipeline-state-graph/ATOMS.tsv`).

OD-111 STATUS: RESOLVED UNDER DELEGATION
OD-111 CHECK: pending: to be checked by a different instance

**OD-112 (the in-scope filter): only OD-04's jurisdictions are shown.**
- OD-04 is the owner's answer: "P1+P2+P3 as recorded; UN out; sub-national counts toward its country" (5947-5948). 2026-10-30 ACTION (5) reads "Show only in-scope jurisdictions" (4866). Jurisdictions are `governance/decision-protocol.md` §2.4 item 4; the owner has answered, so this ruling applies the answer.
- The home is `lang_jur_map.scope_status`. To see how many rows are set: `select count(*), sum(scope_status is not null) from lang_jur_map`.
- **Parameter 12.** C1(12)'s jurisdictions all fall in OD-04's set, so the page states the rule.
- **Parameter 3.** C1(3) names jurisdictions outside it (`INT`, which is REF-00994's, and UG), so T-101's scope rows and T-036 are on parameter 3's path. REF-01014 is a draft and fails "current editions only" (2026-10-30 item 7). Both stay as sources but are not comparison rows.
- No list is typed into the page (CLAUDE.md rule 8).

OD-112 STATUS: RESOLVED UNDER DELEGATION
OD-112 CHECK: pending: to be checked by a different instance

**OD-113 (contested grades): the page prints every grade row.**
- `assess_cell.population_match` returns the lowest `match_id`. For the sources `prb-antagonist-2.md` claim 6 names, that is a PARTIAL grade, which a later PROXY row corrects.
- The grade feeds `assess_source`, then `population_directness_from_match_grade`, then `consolidate` (`schemas/directness.py`), which sets each source's conditioning. Today the outcome is unchanged: PARTIAL and PROXY both give DOWN-WEIGHTED (`consolidate`'s rule 4).
- The engine is not changed now. Under the WHEEL route the sources are graded afresh.
- The page prints both rows and notes which is the later correction (CLAUDE.md §4).

OD-113 STATUS: RESOLVED UNDER DELEGATION
OD-113 CHECK: pending: to be checked by a different instance

CONDITION: any session building PR B, T-124, T-068, T-102, T-127 or T-110, or asking which cell goes first, which unverified sources govern, or whether the four figures may be left off a page.
ACTION:
1. Make OD-110's task-file edits and the register entries before acting on OD-90 to OD-113 in a task.
2. Start nothing on OD-110 until its check is confirmed.
3. Put the referred questions and Q3 to the owner in plain form.
4. Write no "Owner" heading without the owner's typed words.
5. Re-derive every figure by its command.

DATE: 2026-11-27 — delegated resolutions after two independent checks; checks pending; not an owner statement.

---

## Part C. Notes for the coordinator (not ledger text)

1. **Owner words to record under rule 0, before this block,** each verified in `transcripts/harness_f8d4d6c2/main.jsonl` with `git grep -n -F '<phrase>' -- transcripts`:
   - "Opus to resolve conflicts like Q1 and others. Further, prepare context and potential answers for me to use for the slate of C and D issues" (2026-11-27);
   - "PRA" (2026-11-27, 04:09 UTC; it approved resolution-plan PR A);
   - the 2026-11-26 CLAUDE.md audit instruction.
2. **Still unverified:**
   - every engine branch that reads `population_match`;
   - whether the T-127 slice needs an ICF code that is not held;
   - whether REF-01019 governs 3 × MOB;
   - whether conditioned run-length rows belong in T-124's figures. Most of parameter 12's rows are gradient-conditioned branches: re-derive from `extraction_relations`.
3. **`build_batches.py` writes `REMEDIATION-PLAN.md` on any invocation, `--help` included.** Run it only in the change that intends that write.
4. **Not ruled:** AU-22 (T-122) and the other "PRA" deletions (T-005, T-085). Check each against the owner's words as OD-106 does.
