# Adjudication of the read-only passes on the identity, need and ICF matrix batch

The author is the session `session_2026-11-21-identity-need-icf-triples`. Four read-only critics attacked successive
versions of the rows. Each finding below was confirmed against the artefact before it was acted on. Row ids are
identity|need|code. The final version of the rows (the fifth) had no pass of its own.

| Pass | Read | In the database |
|---|---|---|
| 1 | the first version of the generator and `triples.json` (commit 141b42d) | recorded: the pass and its fourteen findings (derive: select finding_id, lens, verdict, disposition from adversarial_findings where pass_id = (select max(pass_id) from adversarial_passes where subject_session = 'session_2026-11-21-identity-need-icf-triples')) |
| 2 | the second version, as a first emitted migration | not recorded (one pass per session) |
| 3 | the third version, as a second emitted migration | not recorded |
| 4 | the fourth version, as a third emitted migration | not recorded |

Transcripts: `transcripts/harness_de695d5a/subagents/` (the four files named `..._adversarial_<id>.jsonl` of 2026-11-21).

## Pass 1 findings and what became of them

| Finding | Disposition |
|---|---|
| F1 two warrants said no project record states aphasia follows stroke | Sustained. The claim is gone; the pair is recorded as an inference (see pass 4, A1). |
| F2 a quote attributed to the wrong cell | Sustained. Need quotes are now checked against absorbs, notes or the need's ICF notes, and the row is withheld. |
| F3 ICF titles glossed from memory | Sustained. No title appears in any warrant. |
| F4 body-function codes on identities | Sustained. No b-code row is proposed; the question is a recorded gap. |
| F5 trailer, kind prefix, session id, copied mechanism text | Sustained. None remain. |
| F6 evidence labels stronger than their basis | Sustained. The labels are gone. |
| F7 one link's mechanism printed for two links | Sustained. No mechanism is copied; no activity-code row is proposed. |
| F8 rows that are the pair crossed with the need's own rows | Sustained. Not repaired: every row has that shape. Filed as an owner question. |
| F9 identity-map codes with no tie to the need | Sustained. Repaired by removal: no identity-side activity code is proposed. |
| F10 umbrella identities keyed on one member's condition | Sustained. Disclosed in each warrant; not repaired (the view reads the key). Filed as an owner question. |
| F11 omissions | Sustained in part. SCI, MOB and LMB rows were added, then removed (pass 2, B3; pass 3, F1, F2); the other omissions rest on b-codes or on the retired axis layer. |
| F12 quotes that pass a substring test and prove nothing | Sustained. Identity quotes now come from the identity's name or description. |
| F13 axis status not stated | Moot: no axis appears anywhere (the owner retired the layer). |

## Pass 2 (second version)

| Finding | Disposition |
|---|---|
| B1 warrants rest on the retired axis layer (ledger 2026-08-24, 2026-09-13; migration 109) | Repaired: no axis, axis code, status or anchor in any warrant. |
| B2 MOVE and VES keyed as identities (OD-37) | Repaired: no row for either; the registry lag is a recorded gap. |
| B3 SCI rows duplicate MOB; three ties false (seventh and eighth sets, OI-77) | Repaired: no SCI row. |
| M1 LMB and MOB ignore the mobility rulings | Repaired by removal of both (pass 3, F1, F2). |
| M2 to M4 gap text false or off | Repaired: the gaps are rewritten and re-derived. |
| M5 dropping e150 distorted the rest | Repaired: every need-map environmental code is attached. |
| M6 a quote outside the identity's own row | Repaired. |
| M7 half-repaired F7 | Repaired by removing every activity-code row. |
| M8 sentences review makes false | Repaired in part; see pass 4, A2. |
| M9 omissions | NDV is added; its rows rest on its description, not on a shared word. |
| M10 the recorded pass is not on the migrated rows | Recorded as a gap. |
| N1 to N4 | Repaired or moot. |

## Pass 3 (third version)

| Finding | Disposition |
|---|---|
| F1 LMB keyed on a code the owner ruled becomes UPL | Repaired: no LMB row. |
| F2 MOB rows name groups the owner gave their own codes | Repaired: no MOB row. |
| F3 to F5, F9 ground words coincide at identity level; titles only | Repaired by removal: no identity-side activity code. |
| F6 member sentence where the condition is the identity | Repaired in part; recurred (pass 4, A1, A3). |
| F7 warrants copy cells the owner has ruled will change | Repaired in part; see pass 4, A2. |
| F8 gaps contradicted by their derive commands | Repaired in part; recurred (pass 4, A6). |
| F10 BLIND shares the word "vision" with A-NOSIGHT | Not repaired by adding rows (T-128 fills identity-side codes); the reason once given for omitting them is withdrawn. |
| F11 the need's rows crossed with the pair; e120 on body-size identities; the A-TRIGGER split | Filed as owner questions (fan-out; umbrella and e120; the A-TRIGGER rows are now attached to both identities). |
| F12 pairs with no naming on either side | NDV now states its basis ("includes AUT, ADHD"); MOB and LMB removed. |
| NDV x A-LOWLOAD omitted | Added, with NDV x A-CALM. |

## Pass 4 (fourth version)

| Finding | Disposition |
|---|---|
| A1 BRAIN\|A-NOSPEECH: "one member" false for aphasia; populations.json cited though T-120 moves it | Repaired: the pair is recorded as an inference, no file is cited, no member sentence. |
| A2 the past-tense frame did not hold on 34 rows | Repaired: one fixed past-tense template; the generator refuses a present-tense verb outside the quotations. |
| A3 MH\|A-STIMULUS: PTSD called a member | Repaired: the reading "PTSD was read as falling under 'trauma'" is recorded in the warrant. |
| A4 member sentence missing where a member or subtype is named | Repaired: COM\|A-EFFORT, EPI\|A-TRIGGER, MH\|A-CALM carry the member basis. |
| A5 this file was not a faithful record | Repaired: this file, rewritten. |
| A6 GAP-378's text contradicted by its own queries | Repaired: rewritten; the activity-code query now selects what it says. |
| A7 NDV rows duplicate AUT and ADHD code for code; the ruling does not cover the carry | Not repaired; the rows stay pending and the question is filed (umbrella question). |
| A8 standing findings not filed as gaps | Repaired: filed (umbrella and e120; fan-out). |
| A9 the A-TRIGGER split rests on retired vocabulary | Repaired: both rows attached to both identities; the question is filed. |
| A10 gap text: typed locator, typed count, unsupported "identities are MOB, LMB, SCI", stale "three passes" | Repaired. |
| A11 docstring prose | Repaired. |
| A12 COM x A-LOWLOAD omitted | Added, recorded as an inference. |

## Pass 5 (the whole final state, read while it changed)

The fifth critic read the rows, the ledger entries, the gaps and the migrations. Dispositions:

| Finding | Disposition |
|---|---|
| F1 GAP-378 closed on a "yes" the owner did not give | Sustained. The closing and the imperative ACTION were mine. Repaired before commit: the closing migration is removed, the gap is open, and the fifth ledger entry now says the statements bear on the question and do not answer it. The question is put to the owner again. |
| F2 row 64 (BLIND, A-NOSIGHT, b210): the code is not named by the owner; its meaning came from the coordinator's general knowledge; the need has no b210 row | Sustained. The row is in a committed migration and cannot be edited. Disclosed in GAP-377; for the owner's review. |
| F3 row 65 (COM, A-TIME, b164): a quotation from the need's ICF notes labelled registry text; an inference | Sustained. Committed and not editable. Disclosed; recommended for rejection. |
| F4 gap text false or misleading | Sustained. Repaired by correction notes on GAP-377, 378, 379, 380 and 382 (a migration of this pull request). |
| F5 pass 10 covers none of the final rows; two dispositions contradicted by rows 64 and 65 | Sustained. Disclosed in GAP-382 and the pull request; the dispositions cannot be amended. |
| F6 hand-written rows bypass the tense guard | Sustained, note. The two hand rows that remain (64, 65) carry reported-content clauses that review does not falsify. |
| F7 ledger quoting: a message's tail dropped; the second entry names COM, BRAIN and MH as umbrellas though the registry holds no members; the first entry's supersession sits outside an assumption bracket | The tail is now stated in the fourth entry. The other two are in committed entries and are recorded here: the second entry's ACTION is read as applying to NDV, the only umbrella with member identities; the first entry's supersession of the earlier means is the coordinator's reading of "I think". |
| F8 a migration summary naming content the file lacked | Moot: the file is removed. |
| F9 MH rows 42 to 44 stretch the template; DEAFBLIND quote weak; the A-AT pairing was selective; repeated codes across needs | Rows 42 to 44 and the DEAFBLIND rows are committed and are for the owner's review. The A-AT pairing (rows 66, 67) is removed: the owner's answer settled A-AT's scope and named no identity. Repeats are by design. |
