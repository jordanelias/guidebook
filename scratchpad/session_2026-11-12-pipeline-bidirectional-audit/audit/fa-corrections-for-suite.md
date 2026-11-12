# FA corrections for the suite — every audit claim that changed, and what it affects

_Handshake leg, resolution pass, 2026-11-12 (UTC). Source of the objections: `fa-antagonist-objections.md` (FA-01 to FA-34). Each was re-run before disposal; the evidence is in `hs-adversarial-findings.md` §5. `sha256sum data/guidebook.db` before and after this pass: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`. All engine and check runs were on fresh copies under `/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/hs2/`._

## 0. Verdict first

**Every objection (count: `grep -c -E '^\| FA-[0-9]{2} ' fa-antagonist-objections.md`) held at least in part, and the suite must be updated from this file wherever it was written from the first versions of the `hs-*` files.** The database measurements did not change. What changed is the programme: what can start now, what must precede a first determination, three deletions that had readers, two entries that rested on superseded ledger text, one ratified question that was re-asked, and the headline that a wrong-lens determination "passes every gate".

**No verdict in the handshake table changed.** The distribution is still given by the command in `hs-handshake-matrix.md` §0. Evidence and wording changed on the rows listed in §1.

Counts: changed claims `grep -c '^| C-[0-9]' <this file>`; dispositions by severity, the command at the head of `hs-adversarial-findings.md` §5.

**Status marks.** VERIFIED = re-run or re-read by the handshake leg in this pass. INFERRED = basis named. UNVERIFIED = not run.

---

## 1. Claims that changed

| # | FA | File § | Old claim | New claim | Status | Ids affected |
|---|---|---|---|---|---|---|
| C-01 | FA-02 | HS-2 F-01, §0; HS-1 §0 D4, §6; HS-3 §0 | A determination for the wrong people passes every gate. | No gate tests the lens. A wrong-lens `provisional` determination passes three specification checks and fails the blocking `test_db_integrity` at C10, because four governing sources are not `VERIFIED`. C10 fails equally for the correct lens. | VERIFIED | REQ-024, REQ-077, HS-A02; IMP-08, IMP-10; R-5, R-6 |
| C-02 | FA-02 | HS-3 §0, IMP-04, R-5 | Before a first determination: IMP-04, IMP-08, IMP-10 and OD-14. | Before a first determination: the lens fix with its link table (IMP-08, IMP-40), the mobility codes (IMP-20), the cell's governing sources verified (R-6, so C10 is green), and the blocking battery green on the scratch copy. IMP-04 is a reporting fix and not a precondition. | VERIFIED for C10; INFERRED for the list | R-5, new R-6; IMP-04, IMP-08, IMP-20, IMP-40 |
| C-03 | FA-01, FA-22 | HS-3 IMP-04, AT-54 | The specification checks print `EXAMINED:` as the live count; a blocking check turning nothing-in-scope on `main` is correct. Three checks named. | The `EXAMINED:` token and the registry floors are not touched: a live-only count would be 0 and `run_checks` returns FAIL below `min_items: 1` on three blocking checks. IMP-04 adds a separate live/retired line to four checks (`validate_evidence_state`, `validate_verification_consistency`, `adjudication_integrity`'s readiness line, `derivation_handshake_integrity`). | VERIFIED | IMP-04, AT-54, REQ-020 |
| C-04 | FA-03, FA-20, FA-32 | HS-3 IMP-05; HS-1 §7 | Delete: four unlinked skill files, `assess_cell --slug`, `reasoning_doc_citations`, `connections.opus_reviewed`, `v_item_provenance`; "nothing reads it". | Nothing is deleted. The four skills have readers and lack only a `description:` line; `--slug` is validated and written into each gap; `v_item_provenance` reads a different junction from the view it was called a subset of; the other two have callers and are candidates only behind a caller sweep. | VERIFIED | IMP-05; HS-1 §7 orphans |
| C-05 | FA-04, FA-18 | HS-3 §0, §3 | First wave doable now with no owner decision: Wave 0 plus IMP-07, 08, 10, 11. | Doable now: IMP-02, IMP-03a, IMP-04, IMP-06, IMP-12, IMP-13 (two values), IMP-23, and the workplan's T-1a and T-6a. IMP-01 needs one owner reply. See §2. | INFERRED from each entry's gate and dependencies | all Wave 0–2 items |
| C-06 | FA-05 | HS-3 IMP-08 | IMP-08: dependency IMP-10 only; owner gate OD-16; first wave. | IMP-08 is the workplan's T-3. Chain: T-1a → T-2 → IMP-40 → IMP-08 (with IMP-09, IMP-10) → D-2. T-1a's done-when is unmet. No owner gate. | VERIFIED for the workplan text and T-1a; INFERRED that the order is forced | IMP-08, IMP-09, IMP-10, R-3 |
| C-07 | FA-05 | HS-3 (absent) | No improvement carried the ruled link table (REQ-076 UNMET). | IMP-40: the link table for several codes of one model (PS:4926, PS:4941), a tooling pull request before T-3. | VERIFIED | new IMP-40; REQ-076, REQ-073; AT-32 |
| C-08 | FA-06 | HS-3 IMP-16 | `stale_determinations` should also recompute the marker; three unguarded routes (PS:4508) should be closed. | Withdrawn. The marker is already recomputed and tested; PS:4560 says those routes "no longer stand as listed". | VERIFIED | IMP-16 withdrawn; AT-20, AT-21 lose their improvement; AT-76 stays unproven |
| C-09 | FA-07 | HS-3 OD-16 | Open: does an engine change bump the rule version (PS:4491 item 4)? | Withdrawn. Answered at PS:4546, which replaces that item; the workplan derives the bumps (WR-2). | VERIFIED | OD-16 withdrawn; IMP-08 |
| C-10 | FA-08 | HS-3 IMP-10, AT-55; HS-2 F-18 | No negative case anywhere; six seeded-defect fixtures to add. | Three registered test files already seed and catch the other defects. One fixture is missing: a wrong-lens determination. | VERIFIED | IMP-10, AT-55 |
| C-11 | FA-09, FA-25 | HS-2 F-15; HS-1 §0 D2, REQ-025; HS-3 IMP-11, AT-56 | The engine cannot determine two cells independently; "dynamic" means one cell per merged pull request; seven runs each allocated id 9 and `GAP-103`. | Several cells on one scratch copy take distinct ids and capture as one delta. Ids collide only between separate copies of one base. Only pending runs allocate a gap. Replay of two copies was not tested. | VERIFIED; replay UNVERIFIED | IMP-11 withdrawn; AT-56 withdrawn; D2 verdict text |
| C-12 | FA-10 | HS-1 §6; HS-2 F-01; HS-3 IMP-08; BU §0 problem 3 | Built from wheelchair evidence / wheelchair-tagged rows. | Governed by 35 figures tagged `MOB`, all T4–T6 code provisions, none device-scoped, none mentioning a wheelchair. | VERIFIED | HS-A02, REQ-077 (wording only) |
| C-13 | FA-11 | HS-1 REQ-022, REQ-098, §5.2; HS-3 OD-23, AT-65 | 23 of 58 live sources hold a text layer; 35 hold none. | Per the command in `hs-adversarial-findings.md` §2.7 with `derivation_kind` tallied (re-run, do not trust): 48 of 58 hold an artefact on disk; 20 a derived text-extraction or extraction record; three more only page renders or a bibliography extract; 10 nothing. Some artefacts are text as retrieved. Which sources hold full text a sweep could read is not established. | VERIFIED for the tallies; the conclusion UNVERIFIED | REQ-098, OD-23, AT-65, IMP-28 |
| C-14 | FA-12 | HS-3 IMP-07, AT-53; HS-1 REQ-006 | Register now, non-zero only when an existing path is lost, absent pairs derived from empty stages; `NO PATH` five times. | The ruled gate fails on any `NO PATH` line; it is red today (`python3 workplan/pipeline-state-graph/walkability.py | grep -c 'NO PATH'`; five pairs ending at render, in two sections), and render is not an empty stage. Registration waits for a render view; until then the instrument is a phase-end command. An interim form is OD-26. | VERIFIED | IMP-07, AT-53, new OD-26 |
| C-15 | FA-13 | HS-1 REQ-074; HS-3 IMP-09, AT-52 | Second example: `pending` + gap for parameter 7 × `DEAF` contradicts the owner. | Withdrawn as evidence: parameter 7 is reverberation time, which concerns Deaf people; that run breaks only the ledger's unratified assumption. The verdict rests on ramp gradient × `DEAF`, its basis marked inferred. AT-52 uses parameter 3 × `DEAF`. | VERIFIED facts; INFERRED reading | REQ-074, IMP-09, AT-52, OD-08 |
| C-16 | FA-14 | HS-3 OD-14, IMP-20; HS-2 F-02 | Confirm the two codes; say whether `MOB` survives as a tag; retire the eight determinations' cell. | The codes and the fate of `MOB` are ratified (PS:1291-1296) and not asked. Open: how rows written under `MOB` since are carried (most come from T4–T6 instruments), and how part-time wheelchair users are named. All eight determinations are already retired. | VERIFIED | OD-14, IMP-20, HS-A01 |
| C-17 | FA-15 | HS-4 Document 7 | Verb list by a line-based search. | Verb list from the syntax tree; the line-based search returns fewer names than the tree holds (both commands in `hs-adversarial-findings.md` §5, FA-15). | VERIFIED | Document 7 |
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
| IMP-12 | typed gap subject; `gap_id` on a search | none | AT-73 | VERIFIED that the columns are absent |
| IMP-13 (two values) | follow-up reasons for a skimmed figure and an absence finding | none | AT-08, AT-11 | VERIFIED vocabulary |

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

- **New:** IMP-40 (link table); R-6 (verify a cell's governing sources); OD-26 (interim stage-pair gate).
- **Withdrawn, ids kept so references do not shift:** IMP-11, IMP-16, OD-16, AT-56.
- **Split:** IMP-03 into IMP-03a and IMP-03b.
- **Restated:** AT-50, AT-51, AT-52, AT-54, AT-55, AT-65, AT-69, AT-74; OD-04, OD-14, OD-22.
- **Unchanged:** every REQ and HS-A verdict; every database figure in HS-1 except the retained-text figures (C-13) and the two counts of C-11.

## 4. What a suite document written from the old claims must change

1. Wherever "passes every gate" or "no gate can go red" appears: C-01.
2. Wherever a first determination's preconditions are listed: C-02.
3. Wherever the lens-tag rule is called an owner ruling: C-21. Wherever the mobility codes or the rule-version label are asked of the owner: C-16, C-09.
4. Wherever a first wave is named: §2.
5. Wherever IMP-05's deletions, IMP-11, IMP-16, OD-16 or AT-56 are cited: C-04, C-08, C-09, C-11.
6. Wherever "23 of 58" or "35 of 58" appears: C-13.
7. Wherever "wheelchair evidence" appears: C-12.
8. Line references: C-26.

## 5. Not resolved

- Whether two separately captured scratch copies fail at replay (not run).
- Whether the workplan's task order is forced or only planned (taken from its §5 and §7).
- Which retained artefacts are a source's full text.
- Whether a withdrawal of the mobility split exists in `sessions/` in words that do not name the codes (searched, not read).
- `migration_reproducibility`, `schema_reference_audit`, `research_dod_session`, `claude_md_spine` and `run_checks.py` in any mode remain unrun.
