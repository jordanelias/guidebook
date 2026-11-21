# Adjudication of the read-only passes on the identity, need and ICF matrix batch

The author is the session `session_2026-11-21-identity-need-icf-triples`. Each finding below was confirmed against the
artefact before it was acted on; a finding the author could not reproduce would say so. Row ids are identity|need|code.
Pass 1 is the one recorded in `adversarial_passes` (its subject commit holds the first version of the rows). Pass 2
attacked the first emitted migration; pass 3 attacks the final one. Only one pass per session can be recorded.

## Pass 1 (recorded; findings in `adversarial_findings`, derive: select finding_id, lens, verdict, disposition from adversarial_findings where pass_id = (select max(pass_id) from adversarial_passes where subject_session = 'session_2026-11-21-identity-need-icf-triples'))

| Finding | Verdict | Disposition |
|---|---|---|
| F1 warrants said no project record states aphasia follows stroke | sustained | Repaired: the warrant cites populations.json, verified present. |
| F2 a quote attributed to the wrong cell (COM|A-TIME) | sustained | Repaired: the row is withheld (its only code is a b-code); the quote is checked against the need's absorbs, notes and ICF notes by name. |
| F3 ICF titles glossed from memory | sustained | Repaired: no gloss; no title is copied. |
| F4 body-function codes on identities | sustained | Repaired: no b-code row is proposed; the question is a recorded gap. |
| F5 trailer, kind prefix, session id, copied mechanism text | sustained | Repaired: none remain. |
| F6 evidence labels stronger than their basis | sustained | Repaired: the labels are gone. |
| F7 one link's mechanism printed for two links | sustained | Repaired: no mechanism is copied; a tie names a verified word. |
| F8 rows that are the pair crossed with the need's own rows | sustained in part | Disputed: need-side environmental codes are attached to every judged pair by design (derived from access_need_icf); the consequence for coverage queries is a recorded gap. |
| F10 umbrella identities | sustained | Repaired: each such row states that the named condition is one member and the row is keyed on the whole identity; NDV has its own rows. |
| F11 omissions | sustained in part | Disputed: SCI rows were added then removed (pass 2, B3); the other omissions rest on b-codes or axis anchors. |

## Pass 2 (read the first emitted migration; not recorded)

| Finding | Confirmed by the author against | Disposition |
|---|---|---|
| B1 warrants rest on the retired axis layer | ledger 2026-08-24 ("I don't want axis to be used") and 2026-09-13 ("'AX-' for ICF should never ever exist anywhere"); migration 109 | Repaired: no warrant names an axis, an axis code or status, or the taxonomy's axis mapping; axis anchors are no basis. The withheld b-code rows that rested on axes are not offered. |
| B2 MOVE and VES keyed as identities | ledger third set, OD-37, ACTION (2) | Repaired: no row for either; the registry lag is a recorded gap. |
| B3 SCI rows duplicate MOB; three ties false | ledger seventh and eighth sets, OI-77 | Repaired: no SCI row. |
| M1 LMB and MOB ignore the mobility rulings | ledger eighth set (LMB outside the mobility family) | Repaired: LMB's e120 is excluded with the reason; MOB rows carry the family sentence. |
| M2 GAP-378 stated a false fact | the gap's own derive query | Repaired: the gap is rewritten. |
| M3 GAP-379 command and list | `lens-crosswalk --uncovered` reads reviewed rows only | Repaired: derive queries replace the typed list. |
| M4 the b-code question not truthfully stated | taxonomy lines 38-41, seventh-set ACTION (4), OI-48, OI-77 | Repaired: the gap cites each and states only what the project's maps hold. |
| M5 dropping e150 distorted the rest | base_icf e150 and e155 | Repaired: every need-map environmental code is attached; exclusions are listed in exclusions.json with the reason. |
| M6 a quote outside the identity's own row | the DEM identity quote was a link mechanism | Repaired: identity quotes come from the identity's name or description only. |
| M7 half-repaired F7 | links 41, 55, 42, 56 | Repaired: the BLIND activity rows are not proposed (no verified shared word). |
| M8 sentences review makes false | the trigger forbids editing a warrant | Repaired: no such sentence remains; no mutable cell is copied. |
| M9 omissions | links 17 and 50 | NDV is added (ground: "sensory"). BRAIN|A-LOWLOAD|d460 is not added: the identity's map text holds no verified word shared with the need. |
| M10 the recorded pass is not on the migrated rows | adversarial_pass_audit prints NOTHING-IN-SCOPE | Recorded as a gap (one pass per session); this file is the record of the later passes. |
| N1 to N4 | | N1 repaired in the gap text; N2, N3 repaired in the warrants; N4 moot (no axis). |

## Pass 3 (read the second emitted migration; not recorded)

| Finding | Confirmed by the author against | Disposition |
|---|---|---|
| F1 LMB rows keyed on a code the owner ruled becomes UPL | ledger eighth set ACTION (2), tenth set OI-49; no UPL, WHEEL, WALKAID or LLD registry row | Repaired: no LMB row; recorded in the coverage gap. |
| F2 MOB rows name groups with their own codes | ledger 2026-08-25 ACTION (1), fifth set OD-14, OD-31 | Repaired: no MOB row; recorded in the coverage gap. |
| F3 a mechanism claimed for two links when one lacks the word | links 43, 44 against 58, 59 | Repaired by removal: no activity-code row is proposed. |
| F4, F5 ground rows rest on a title only, or on another identity's condition | triples.json | Repaired by removal. |
| F6 "one member of this identity" where the condition is the identity | BRAIN, MOB warrants | Repaired: the sentence is only on rows whose quote names a member condition. |
| F7 warrants copy cells the owner has ruled will change (absorbs, MOB and LMB names) | ledger fifth set, OI-49, 2026-11-20 (fifth) | Repaired: every warrant is written in the past tense of its own recording ("As recorded when this row was written ... read:"), so it stays true after the cell changes. |
| F8 gap rows contradicted by their own derive commands and the ledger text | the gaps | Repaired: the gaps are rewritten; the quoted phrase is the ledger's. |
| F9 a shared word coincides at identity level and does not tie the code | the generator's own test on sibling codes | Repaired by removal: identity-side activity codes belong to T-128. |
| F10 BLIND shares the word "vision" with A-NOSIGHT | links 55, 56, 57 | Not repaired by adding rows: BLIND's activity rows are T-128's. The earlier reason (no shared word) is withdrawn. |
| F11 most rows are the pair crossed with the need's own rows; e-only identities | triples.json | Not repaired; filed as an owner question (the fan-out), with its derive command. |
| F12 pairs where neither side names the other are not disclosed as inference | NDV, MOB, LMB | Repaired: NDV now rests on its description ("includes AUT, ADHD") and carries the member sentence; MOB and LMB have no row. |
| NDV x A-LOWLOAD omitted | NDV description, need names ADHD | Added, with A-CALM. |
