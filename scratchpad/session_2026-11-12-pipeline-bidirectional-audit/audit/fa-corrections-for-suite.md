# FA corrections for the suite — every audit claim that changed, and what it affects

_Handshake leg, resolution pass, 2026-11-12 (UTC). Source of the objections: `fa-antagonist-objections.md` (FA-01 to FA-34). Each was re-run before disposal; the evidence is in `hs-adversarial-findings.md` §5. `sha256sum data/guidebook.db` before and after this pass: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`. All engine and check runs were on fresh copies under `/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/hs2/`._

## 0. Verdict first

_Amended after the antagonist's confirmation pass (`fa-confirmation.md`) and after the audit of the stress tests (`hs-stress-audit.md`). §4 is rebuilt from the full table; §6 holds the stress-test deltas; §7 the confirmation-pass corrections._

**Every objection (count: `grep -c -E '^\| FA-[0-9]{2} ' fa-antagonist-objections.md`) held at least in part, and the suite must be updated from this file wherever it was written from the first versions of the `hs-*` files.** The database measurements did not change. What changed is the programme: what can start now, what must precede a first determination, three deletions that had readers, two entries that rested on superseded ledger text, one ratified question that was re-asked, and the headline that a wrong-lens determination "passes every gate".

**No verdict in the handshake table changed.** The distribution is still given by the command in `hs-handshake-matrix.md` §0. Evidence and wording changed on the rows listed in §1.

Counts: changed claims `grep -c -E '^\| C-[0-9]{2} \| FA-' <this file>`; stress findings `grep -c -E '^\| S-[0-9]{2} ' <this file>`; dispositions by severity, the command at the head of `hs-adversarial-findings.md` §5.

**Status marks.** VERIFIED = re-run or re-read by the handshake leg in this pass. INFERRED = basis named. UNVERIFIED = not run.

---

## 1. Claims that changed

| # | FA | File § | Old claim | New claim | Status | Ids affected |
|---|---|---|---|---|---|---|
| C-01 | FA-02 | HS-2 F-01, §0; HS-1 §0 D4, §6; HS-3 §0 | A determination for the wrong people passes every gate. | No gate tests the lens. A wrong-lens `provisional` determination passes three specification checks and fails the blocking `test_db_integrity` at C10, because four governing sources are not `VERIFIED`. C10 fails equally for the correct lens. | VERIFIED | REQ-024, REQ-077, HS-A02; IMP-08, IMP-10; R-5, R-6 |
| C-02 | FA-02 | HS-3 §0, IMP-04, R-5 | Before a first determination: IMP-04, IMP-08, IMP-10 and OD-14. | Before a first determination: the lens fix with its link table (IMP-08, IMP-40), the mobility codes (IMP-20), the cell's governing sources verified (R-6, so C10 is green), and the blocking battery green on the scratch copy. IMP-04 is a reporting fix and not a precondition. | VERIFIED for C10; INFERRED for the list | R-5, new R-6; IMP-04, IMP-08, IMP-20, IMP-40 |
| C-03 | FA-01, FA-22 | HS-3 IMP-04, AT-54 | The specification checks print `EXAMINED:` as the live count; a blocking check turning nothing-in-scope on `main` is correct. Three checks named. | The `EXAMINED:` token and the registry floors are not touched: a live-only count would be 0 and `run_checks` returns FAIL below `min_items: 1` on three blocking checks. IMP-04 adds a separate live/retired line to four checks (`validate_evidence_state`, `validate_verification_consistency`, `adjudication_integrity`'s readiness line, `derivation_handshake_integrity`). | VERIFIED | IMP-04, AT-54, REQ-020 |
| C-04 | FA-03, FA-20, FA-32 | HS-3 IMP-05, IMP-12; HS-1 §7 | Delete: four unlinked skill files, `assess_cell --slug`, `reasoning_doc_citations`, `connections.opus_reviewed`, `v_item_provenance`, and (IMP-12) `gap_mining` with its verbs and audit; "nothing reads it". | No entry deletes anything. The four skills have readers and lack only a `description:` line; `--slug` is validated and written into each gap; `v_item_provenance` reads a different junction from the view it was called a subset of; `reasoning_doc_citations`, `opus_reviewed` and the `gap_mining` cluster have callers and are candidates only behind a caller sweep. | VERIFIED | IMP-05, IMP-12, IMP-32, IMP-36; HS-1 §7 orphans |
| C-05 | FA-04, FA-18 | HS-3 §0, §3 | First wave doable now with no owner decision: Wave 0 plus IMP-07, 08, 10, 11. | Doable now: IMP-02, IMP-03a, IMP-04, IMP-06, IMP-12, IMP-13 (two values), IMP-23, and the workplan's T-1a and T-6a. IMP-01 needs one owner reply. See §2. | INFERRED from each entry's gate and dependencies | all Wave 0–2 items |
| C-06 | FA-05 | HS-3 IMP-08 | IMP-08: dependency IMP-10 only; owner gate OD-16; first wave. | IMP-08 is the workplan's T-3. Chain: T-1a → T-2 → IMP-40 → IMP-08 (with IMP-09, IMP-10) → D-2. T-1a's done-when is unmet. No owner gate. | VERIFIED for the workplan text and T-1a; INFERRED that the order is forced | IMP-08, IMP-09, IMP-10, R-3 |
| C-07 | FA-05 | HS-3 (absent), then IMP-40 | No improvement carried the ruled link table (REQ-076 UNMET). | IMP-40: the link table for several codes of one model (PS:4926, PS:4941). The ledger gives its shape to "the tooling PR" (PS:4934) and puts tooling before data (PS:4938); it does not say the table precedes T-3. Placing IMP-40 before or inside T-3 is the handshake leg's sequencing. | VERIFIED for the ruling; the order INFERRED and the leg's own | new IMP-40; REQ-076, REQ-073; AT-32 |
| C-08 | FA-06 | HS-3 IMP-16 | `stale_determinations` should also recompute the marker; three unguarded routes (PS:4508) should be closed. | Withdrawn. The marker is already recomputed and tested; PS:4560 says those routes "no longer stand as listed". | VERIFIED | IMP-16 withdrawn; AT-21 and AT-76 have no improvement (AT-20 is still carried by IMP-39); AT-76 stays unproven |
| C-09 | FA-07 | HS-3 OD-16 | Open: does an engine change bump the rule version (PS:4491 item 4)? | Withdrawn. Answered at PS:4546, which replaces that item; the workplan derives the bumps (WR-2). | VERIFIED | OD-16 withdrawn; IMP-08 |
| C-10 | FA-08 | HS-3 IMP-10, AT-55; HS-2 F-18 | No negative case anywhere; six seeded-defect fixtures to add. | Three registered test files seed and catch four of the five other defects. Two fixtures are missing: a wrong-lens determination, and a retired determination surfaced by a view. | VERIFIED | IMP-10, AT-55, AT-19 |
| C-11 | FA-09, FA-25 | HS-2 F-15; HS-1 §0 D2, REQ-025; HS-3 IMP-11, AT-56 | The engine cannot determine two cells independently; "dynamic" means one cell per merged pull request; seven runs each allocated id 9 and `GAP-103`. | Several cells on one scratch copy take distinct ids and capture as one delta. Ids collide only between separate copies of one base. Only pending runs allocate a gap. Replay of two copies was not tested. | VERIFIED; replay UNVERIFIED | IMP-11 withdrawn; AT-56 withdrawn; D2 verdict text |
| C-12 | FA-10 | HS-1 §6; HS-2 F-01; HS-3 IMP-08; BU §0 problem 3 | Built from wheelchair evidence / wheelchair-tagged rows. | Governed by 35 figures tagged `MOB`, all T4–T6 code provisions, none device-scoped, none mentioning a wheelchair. | VERIFIED | HS-A02, REQ-077 (wording only) |
| C-13 | FA-11 | HS-1 REQ-022, REQ-098, §5.2; HS-3 OD-23, AT-65 | 23 of 58 live sources hold a text layer; 35 hold none. | Per the command in `hs-adversarial-findings.md` §2.7 with `derivation_kind` tallied (re-run, do not trust): 48 of 58 hold an artefact on disk; 20 a derived text-extraction or extraction record; three more only page renders or a bibliography extract; 10 nothing. Some artefacts are text as retrieved. Which sources hold full text a sweep could read is not established. | VERIFIED for the tallies; the conclusion UNVERIFIED | REQ-098, OD-23, AT-65, IMP-28 |
| C-14 | FA-12 | HS-3 IMP-07, AT-53; HS-1 REQ-006 | Register now, non-zero only when an existing path is lost, absent pairs derived from empty stages; `NO PATH` five times. | The ruled gate fails on any `NO PATH` line; it is red today (`python3 workplan/pipeline-state-graph/walkability.py | grep -c 'NO PATH'`; five pairs ending at render, in two sections), and render is not an empty stage. Registration waits for a render view; until then the instrument is a phase-end command. An interim form is OD-26. | VERIFIED | IMP-07, AT-53, new OD-26 |
| C-15 | FA-13 | HS-1 REQ-074; HS-3 IMP-09, AT-52 | Second example: `pending` + gap for parameter 7 × `DEAF` contradicts the owner. | Withdrawn as evidence: parameter 7 is reverberation time, which concerns Deaf people; that run breaks only the ledger's unratified assumption. The verdict rests on ramp gradient × `DEAF`, its basis marked inferred. AT-52 uses parameter 3 × `DEAF`. | VERIFIED facts; INFERRED reading | REQ-074, IMP-09, AT-52, OD-08 |
| C-16 | FA-14 | HS-3 OD-14, IMP-20; HS-2 F-02 | Confirm the two codes; say whether `MOB` survives as a tag; retire the eight determinations' cell. | The codes and the fate of `MOB` are ratified (PS:1291-1296) and not asked. Open: how rows written under `MOB` since are carried (most come from T4–T6 instruments), and how part-time wheelchair users are named. All eight determinations are already retired. | VERIFIED | OD-14, IMP-20, HS-A01 |
| C-17 | FA-15 | HS-4 Document 7 | Verb list by a line-based search. | Verb list from the syntax tree (the command is in HS-4 Document 7). The line-based search `grep -o "add_parser(\s*['\"][a-z0-9-]*" scripts/db.py | wc -l` returns fewer names than the tree holds. | VERIFIED | Document 7 |
| C-18 | FA-16 | HS-4 §1.1 item 7; HS-1 several rows | A text-search hit count is forbidden, while searches were prescribed and marked verified. | The rule is stated with three permitted searches; structural commands replace searches where a structure exists; an absence drawn from a search is inferred. HS-1 rows REQ-006, REQ-017, REQ-020 now carry structural evidence; HS-A01 ("not withdrawn"), HS-A10 ("the engine"), REQ-100 ("no finder code") are inferred. | VERIFIED | REQ-006, REQ-017, REQ-020, REQ-100, HS-A01, HS-A09, HS-A10 |
| C-19 | FA-17 | HS-3 AT-50, AT-51 | Tested on parameter 3 × `DEAF` and × `ALL`. | Parameter 3 holds no `DEAF` or `ALL` figure, so both would pass empty after the fix. AT-50 now reads the figures linked to parameter 3 × `MOB`; AT-51 those linked to parameter 9 × `ALL`. | VERIFIED | AT-50, AT-51 |
| C-20 | FA-19 | HS-3 IMP-24, IMP-25, AT-74 | Write the retired `lang_detected` copies forward to `language`; one case everywhere. | `lang_detected` is the live column. IMP-24 is the workplan's T-6a (fold at writers and in views, no UPDATE of history), extended to three writers. No back-fill (workplan K-9, K-10). | VERIFIED | IMP-24, IMP-25, AT-74 |
| C-21 | FA-21 | HS-1 §0; HS-2 F-01; HS-3 §0, IMP-08; HS-4 §0, Document 2 | The lens-tag gather rule is a live owner ruling. | Owner: the `ALL` answer (PS:4657) and "do not store rows … not relevant" (PS:4614). Ledger reading, marked as the assistant's: the general lens-tag rule (PS:4628-4630). | VERIFIED | HS-A02, IMP-08, Document 2 |
| C-22 | FA-30 | HS-3 OD-04 | Scope undecided between buckets and P1+P2+P3. | The owner's later words are on the record (PS:4835, restated PS:5026). Open only: what that answer covers, `UN`, the set's membership, variants. | VERIFIED | OD-04, IMP-18, REQ-063 |
| C-23 | FA-34 | HS-3 IMP-03 | A convention, Wave 0. | Split: IMP-03a (entry text, doable now); IMP-03b (`re_entry:` key, a schema change because the models forbid extra keys; Wave 2; OD-18). | VERIFIED | IMP-03, AT-43, AT-44 |
| C-24 | FA-18 | HS-3 §3, IMP-17, IMP-19, IMP-34, IMP-35, IMP-36 | Wave 4 items "no gate"; IMP-17 depends on IMP-19. | Only the tables of IMP-29 and IMP-30 are ungated; IMP-34's clause candidates and IMP-36's relation kinds are gated; IMP-17 ships its own writer. | INFERRED from the entries | IMP-17, 19, 29, 30, 34, 35, 36 |
| C-25 | FA-24 | HS-1 §0 | "In two places the code does the opposite of a live owner ruling." | No typed count; the CONTRADICTED rows are counted by the file's command. | VERIFIED | — |
| C-26 | FA-26 | HS-1, HS-2 V27, HS-4 | "5 is three" at PS:2056; Fable-class wording at PS:609; "prompts for research to target" at PS:1967; "without English bias" at PS:5206. | PS:2419; PS:608; PS:1968 (quote spans 1965-1969); PS:5019, with PS:5206 carrying "we are trying to avoid english BIAS". | VERIFIED | REQ-055, REQ-096, HS-A04, HS-A05 |
| C-27 | FA-27, FA-28, FA-29, FA-23 | HS-1 HS-A09; HS-3 OD-22, AT-69, cross-references | A command that returned a hit; a command that listed section names; a census that under-counts; wrong IMP numbers. | Each replaced or corrected. Open prompts are under the `decisions` key of `governance/owner-browser.yaml`. | VERIFIED | HS-A09, OD-22, AT-69 |
| C-28 | FA-33 | HS-4 §0, §2 | Evidence base "three audit files"; documents 4–6 append to 2 and 3. | The audit files of §1 plus this file; additions are proposed in the finding document and folded in a Round 3b with its own antagonist check. | VERIFIED | suite order |

## 2. Corrected "doable now" set, with real dependencies

Doable now means: no owner word needed, no unmet dependency, and nothing turns red on untouched `main`. T-n are tasks of `workplan/2026-10-23-pipeline-resolution-workplan.md`.

| Item | What it is | Depends on | Check after | Status |
|---|---|---|---|---|
| IMP-06 | owner queue's answered marks derived from the ledger | none | builder runs | INFERRED |
| IMP-02 | supersession marks; contract header corrected to what its decision record says (accepted 2026-07-21, precondition outstanding) | none | `claude_md_spine`, `research_contract_sync` | INFERRED |
| IMP-03a | contract entry text for synthesis, specification, research, evidence | none | `pipeline_contract_audit` | INFERRED |
| IMP-04 | live/retired line on four checks; token and floors untouched | none | `run_checks.py --battery schema` verdict unchanged | VERIFIED that the alternative is red |
| T-1a | reading (workplan: "Needs nothing") | none; done-when unmet (`grep -rn "def parse_bound" scripts` returns a line) | the workplan's done-when | VERIFIED |
| T-6a = IMP-24 | language folded at writers and in views | none; done-when unmet (the two counts in AT-74 differ) | AT-74 | VERIFIED |
| IMP-23 | script-aware quote and name guards | none; coordinate with T-1a's numeral gloss | `observation_verbatim_audit`; AT-59, AT-60 | VERIFIED that the guards fail today |
| IMP-12 | typed gap subject; `gap_id` on a search; deletes nothing | none | AT-73 | VERIFIED that the columns are absent |
| IMP-13 (two values) | follow-up reasons for a skimmed figure and an absence finding | none | AT-08, AT-11 | VERIFIED vocabulary |
| IMP-43 | `add-source` requires a verification standing and a source type | none; sweep callers | AT-78 | VERIFIED red (stress) |
| IMP-44 | the claimed-number check compares numbers | none; coordinate with T-1a, IMP-23 | AT-79 | VERIFIED red (live functions) |
| IMP-45 | `delete-connection` refuses a missing id | none | AT-100 | VERIFIED red (stress) |

**Needs one owner reply:** IMP-01.

**Not doable now, and why (first version said otherwise):**

| Item | Blocker |
|---|---|
| IMP-03b | schema change; OD-18; carriers from IMP-12 to IMP-14 |
| IMP-05 | nothing deletable without a caller sweep; three listed objects have readers |
| IMP-07 | red on `main` until a render view exists; OD-26 for an interim form |
| IMP-08, IMP-09, IMP-10 | T-1a → T-2 → IMP-40 first; IMP-09's stored-row question is OD-08 |
| IMP-11, IMP-16 | withdrawn |
| IMP-14 | OD-21 |

## 3. New and withdrawn ids

- **New:** IMP-40 (link table); R-6 (verify a cell's governing sources); OD-26 (interim stage-pair gate). From the stress audit (§6): IMP-41 to IMP-45, OD-27, AT-77 to AT-79, AT-100 to AT-102; IMP-30 split into IMP-30a and IMP-30b.
- **Withdrawn, ids kept so references do not shift:** IMP-11, IMP-16, OD-16, AT-56.
- **Split:** IMP-03 into IMP-03a and IMP-03b.
- **Restated:** AT-50, AT-51, AT-52, AT-53, AT-54, AT-55, AT-65, AT-69, AT-74, AT-76 (its "For" column); OD-04, OD-14, OD-18, OD-22, OD-23.
- **Unchanged:** every REQ and HS-A verdict; every database figure in HS-1 except the retained-text figures (C-13) and the two counts of C-11.

## 4. What a suite document written from the old claims must change

One line per row of §1, in order; a suite document is checked against every line.

| Row | If the document says … | … change it to |
|---|---|---|
| C-01 | "passes every gate", "no gate can go red" | no gate tests the lens; C10 of `test_db_integrity` stops a `provisional` cell for unverified sources |
| C-02 | first determination after IMP-04, IMP-08, IMP-10, OD-14 | after IMP-08 with IMP-40, IMP-20, R-6, blocking battery green |
| C-03 | IMP-04 makes `EXAMINED:` the live count; AT-54 "reports zero examined" | report-only line; token and floors untouched; AT-54 as restated |
| C-04 | any deletion from IMP-05 or IMP-12 | no deletion; candidates behind a caller sweep |
| C-05 | "first wave: Wave 0 plus IMP-07, 08, 10, 11" | the table in §2, as extended in §6 |
| C-06 | IMP-08 depends on IMP-10 only | T-1a → T-2 → IMP-08 (= T-3), then D-2 |
| C-07 | no entry for the link table, or "the ledger orders it before T-3" | IMP-40; its position is the handshake leg's sequencing |
| C-08 | IMP-16 as an improvement | withdrawn |
| C-09 | OD-16 as an open question | withdrawn; answered at PS:4546 |
| C-10 | six fixtures to add, or "only the wrong-lens one is missing" | two missing: wrong lens; retired row in a view |
| C-11 | "one cell per merged pull request"; "seven runs each allocated `GAP-103`" | cells on one copy do not collide; parallel batches do (§6, IMP-41) |
| C-12 | "wheelchair evidence" | 35 code provisions tagged `MOB` |
| C-13 | "23 of 58 hold a text layer", "35 hold none" | the tallies of HS-1 §5.2; what a sweep could read is not established |
| C-14 | IMP-07 in the first wave; AT-53 as a regression test; "`NO PATH` five times" | registered when a render view exists; AT-53 as the ruled gate; ten lines, five pairs |
| C-15 | parameter 7 × `DEAF` as a breach of the owner's sentence | withdrawn; ramp gradient × `DEAF` only, basis inferred |
| C-16 | OD-14 asking the codes or the fate of `MOB` | ratified; OD-14 asks how rows written since are carried |
| C-17 | the verb list from a line search | from the syntax tree |
| C-18 | a search result marked verified as an absence | inferred; structural commands where they exist |
| C-19 | AT-50 on parameter 3 × `DEAF`, AT-51 on parameter 3 × `ALL` | parameter 3 × `MOB` linked set; parameter 9 × `ALL` and × `MOB` |
| C-20 | `lang_detected` as a retired copy; a back-fill of `language` | `lang_detected` is live; IMP-24 is T-6a, no back-fill |
| C-21 | the lens-tag rule as owner speech | ledger reading; the `ALL` answer is the owner's |
| C-22 | scope undecided between two sets | PS:4835 on the record; OD-04 asks what it covers |
| C-23 | IMP-03 as one Wave 0 convention | IMP-03a text now; IMP-03b schema change, Wave 2, OD-18 |
| C-24 | Wave 4 items ungated; IMP-17 depends on IMP-19 | as the §3 table of HS-3 now reads |
| C-25 | "in two places the code does the opposite of a live owner ruling" | no count; the CONTRADICTED rows by command |
| C-26 | PS:2056 for "5 is three"; PS:609; PS:1967; PS:5206 for "without English bias" | PS:2419; PS:608; PS:1965-1969; PS:5019 |
| C-27 | the old HS-A09, OD-22 or AT-69 commands | the replaced commands |
| C-28 | "three audit files"; additions appended in Round 3 | the audit files of the brief's §1 plus this file; Rounds 3b and 4b |

## 5. Not resolved

- Resolved by the stress run: three separately captured batches fail at rebuild (§6).
- Whether the workplan's task order is forced or only planned (taken from its §5 and §7).
- Which retained artefacts are a source's full text.
- Whether a withdrawal of the mobility split exists in `sessions/` in words that do not name the codes (searched, not read).
- Measured by the stress run on a scratch copy: `migration_reproducibility`, `schema_reference_audit`, `claude_md_spine`, `run_checks.py --selftest` and `--changed-from origin/main --explain` (all pass; the last with advisory failures). Still unrun: `run_checks.py --all`, any single battery, `research_dod_session` on its own.

---

## 6. Stress-test deltas

Source: `hs-stress-audit.md` (HS-5). Behaviour ids B-nn are its §1. A suite document absorbs each line.

### 6.1 New defects and their entries
| # | Finding | Evidence | Entry | Test | Status |
|---|---|---|---|---|---|
| S-01 | The claimed-number check accepts a shifted decimal and a digit substring | live functions: `12` against "1.2 m", `0.6` against "6.0 s", `8.33` against "83.3 %"; `scripts/db.py:8559-8563` | IMP-44 | AT-79 | VERIFIED |
| S-02 | `add-parameter` promotes an element, a functional-axis term, a legal concept and an activity | B-05 | IMP-42, IMP-30a | AT-77 | VERIFIED |
| S-03 | Batches captured in parallel fail at rebuild on a shared id | B-40 | IMP-41; OD-27 | AT-101 (unproven at capture) | VERIFIED at rebuild |
| S-04 | `add-source` writes a source with no verification standing and no source type | B-12 | IMP-43 | AT-78 | VERIFIED |
| S-05 | `delete-connection` reports deleting a row that does not exist | B-42 | IMP-45 | AT-100 | VERIFIED |
| S-06 | CLAUDE.md §1's `--battery <name>` needs a selector to run | B-53 | IMP-02 (one more mark) | AT-102 | VERIFIED |
| S-07 | Three more registered checks fail at advisory level on `main`: `test_scan_contract`, `validate_schema_cross_check`, `research_dod` | B-54 | none yet: causes unread | — | names VERIFIED; causes UNVERIFIED |

### 6.2 Audit claims the stress tests change
| # | Old claim (file) | New claim |
|---|---|---|
| S-08 | IMP-11 withdrawn; "replay of two copies untested" (HS-3; C-11 of §1) | Tested: parallel batches fail at rebuild. IMP-11 stays withdrawn as written (cells on one copy do not collide); its subject returns as IMP-41 |
| S-09 | "`run_checks.py` not run in any mode"; `migration_reproducibility`, `schema_reference_audit`, `claude_md_spine` unrun (HS-1 §8, HS-2 §4, §5 here) | Measured on a scratch copy: selftest PASS; diff-scoped gate PASS with advisory failures; the three checks PASS with a subject. No single battery and no `--all` has run |
| S-10 | The round trip is "inferred from the tools' existence" (HS-1 §8) | Holds for one batch by row counts; untested with a determination and by content |
| S-11 | No alias is attested by pointer, the route unexercised (HS-1 REQ-058) | The data fact stands; `add-alias` from an adjudicated observation works (B-49) |
| S-12 | HS-2 F-10 (marks dropped by the normaliser) | Stands. Round 1's "no collisions" is the script: its pairs differ in digits (B-30) |

### 6.3 Confirmed with a reproduction (no change of claim)
IMP-09 and REQ-074 (B-17, B-28); HS-A02 (B-18); IMP-18, REQ-063 and REQ-064 (B-01, B-34); IMP-17 and sub-national codes (B-33); IMP-23 (B-31, B-32); REQ-098 and IMP-28 (B-06); IMP-12 (B-16); B17 of the boundary table (B-23); REQ-025 determinism (B-36); IMP-07 (B-20).

### 6.4 Ordering and preconditions
- Doable now gains IMP-43, IMP-44, IMP-45 (§2).
- IMP-42 with IMP-30a precedes the minting of any further parameter.
- IMP-44, and IMP-23 for non-Latin sources, precede new extractions (R-2, R-3).
- Research batches are serial (IMP-41) unless OD-27 is answered otherwise.
- Preconditions of a first live determination are unchanged (C-02).

### 6.5 What the stress tests did not test (do not cite them for it)
No extraction, candidate or mining row was written in either round; every per-topic determination is `pending`; no determination went through the write path; no battery ran; the backward funnel query failed on the script's own SQL; the "nine topics" are one sequence nine times. Details and the script changes: HS-5 §4.

### 6.6 Round 3 (final): what changed again
| # | Earlier statement (this file or HS-5 §0–§6) | Final |
|---|---|---|
| S-13 | No extraction was written in any round; every determination pending | Three extractions and six `provisional` determinations were written on one database in round 3 |
| S-14 | S-10: the round trip is untested with a determination and by content | Holds by content for a batch with six determinations (handshake leg's clean-clone re-run). Round 3's own failure was a reused clone |
| S-15 | S-09: no single battery has run | All ten batteries ran and PASS; advisory failures and nothing-in-scope checks are listed in HS-5 B-82 |
| S-16 | S-03, AT-101: the parallel-batch collision surfaces at rebuild; capture untested | The second batch is refused at capture. IMP-41 is a sentence in the skill; AT-101 is green for the refusal |
| S-17 | S-01: number check shown on the live functions only | Reproduced at the writer: `1:1`, `1.2`, `112` and `twelve` accepted against a quote stating `1:12` |
| S-18 | S-12: collisions shown on the handshake leg's pairs | Reproduced by the script's probe for Devanagari, Thai, Hebrew, Arabic, kana and decimal forms |
| S-19 | (new) | Retire and re-determine leaves the retired row's supersession pointer NULL: IMP-46, AT-103 |
| S-20 | (new) | A targeted full read of a held text discharges a new parameter's pair for that source; retiring a parameter removes its pairs |
| S-21 | (new) | `add-extraction` accepts prose in the unit cell (the prior workplan's T-1a refusal, unbuilt) |

The single list of what still stands, ranked, is `hs-improvement-programme.md` §8 (Final recommendations). The executable plan is `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`; the other seven suite documents are not to be written.

## 7. Confirmation-pass corrections

The rows of `fa-confirmation.md` marked inaccurate are disposed in `hs-adversarial-findings.md` §6 (K-01 to K-22). Those that change a row of §1 here: C-04, C-07, C-08, C-10, C-17 (rewritten above), and §3 and §4 (rebuilt).

## 8. Final pass: REQ-101 to REQ-103, and what replaces the suite

The eight-document suite is dropped by the owner in favour of one remediation workplan: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md` with one file per task under `tasks/`. `01-handshake-ledger.md` stays as the evidence base; where it differs from this file, this file governs.

| Id | What changed | Where |
|---|---|---|
| S-22 | Three owner statements of 2026-11-12 enter the requirement set: REQ-101 (efficient, centralized, clean; PARTIAL), REQ-102 (flexible, no hard-coded behaviours; PARTIAL), REQ-103 (no dead ends; UNMET). The readings of "hard-coded" and "dead end" are the audit's and unratified. | HS-1 §1 (rows after REQ-100); HS-3 §9 |
| S-23 | A finding carried by CLAUDE.md rule 8 is not reproduced: the `argparse` value lists are already read from the schema (`derived_not_curated_audit` CLEAN); the rule's grep pair cannot see two of the deriving helpers. Task T-042 corrects the sentence. | HS-3 §9.2 |
| S-24 | Splitting `scripts/db.py` is declined; no efficiency task is proposed (measured cost is small). | HS-3 §9.1, §9.2 |
| S-25 | New tests: AT-104 (the base changes by data alone), AT-105 (a root can be registered), AT-106 (every refusal names a next action). New tasks: T-041, T-042, T-043, T-047, T-048. | HS-3 §9; the workplan |
| S-26 | OD-29 added: whether retire-in-place covers link rows (`delete-connection`, `unlink-admission`; HS-1 REQ-018). | the workplan's register; HS-3 §9.7 |

