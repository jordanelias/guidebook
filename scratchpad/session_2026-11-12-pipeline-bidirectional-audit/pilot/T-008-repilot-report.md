# T-008 re-pilot report (Sonnet-class executor, pilot mode)

Task file: `workplan/2026-11-12-bidirectional-pipeline/tasks/T-008-claimed-number-check.md` (the redesigned file: `value_as_written`, its writers, the digitless refusal). Stage P1, stacked on nothing. The earlier T-008 report and patch were not read and not overwritten.

**Base commit:** `d0952279b2c741406793bb86cfad57e586a7c80e` (tip of `origin/claude/peaceful-noether-kvf3sf` in the clone). I overrode the task file's own `BASE` line (which picks `origin/ccr-408aaa9b-z3e4s0` or `origin/main`) with `BASE=origin/claude/peaceful-noether-kvf3sf`, as the pilot brief orders: PR 220 is unmerged and `origin/main` is stale.

Canonical `data/guidebook.db` sha256 before and after: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d` (equal). The migration was applied only to the clone's copy.

## Outcome: PILOTED (green after, red before), with one design hole that the file's own rule permits

| Held? | |
|---|---|
| (1) followed only CLAUDE.md and the task file | Yes. I did not open other task files, the audit folders, the ledger, or the earlier T-008 report/patch. I read the repo's code and tests (necessarily) and `PILOT-BRIEF.md`. |
| (2) evidence command printed what the file says | Yes. Six `ACCEPTED`; `[(0,)]`; rows 30 and 80 as described (30: claims `5` under the Dutch quote; 80: Finnish words as value). After the change the same command prints `REFUSED` on all six lines. But see defect D2 (the command passes no `claim_type`). |
| (3) red before, green after | Yes. On unchanged `db.py`/`dbcore.py`/`retrieval_log.py` with the new test section in place: 41 `T008` cases, 23 red (`FAILED: 23`, `EXAMINED: 216`); the 18 green ones are the "accepted" cases the old code also accepted, the one refusal old code already made (`1:8` under "1 in 12": digit 8 absent), and the cases that cannot go red. After: `EXAMINED: 215 cases`, `PASS: all 215 cases` (175 before, +40 mine; the 216 in the red run is one extra `feature()` record for the missing `dbcore.QUANTITY_CLAIM_TYPES`). |
| (4) gate ran once; EXAMINED read for every named check | The gate ran TWICE (see D6: the first run exposed a stale generated file, which I regenerated and re-gated). Every named check's `EXAMINED:` is in the table below. |
| (5) patch and report saved | Yes: `T-008-repilot.patch` (one commit; `format-patch` without `--binary` so the `data/guidebook.db` change is a "Bin" stub; a stacked successor must run `python3 scripts/migrate_db.py`) and this report. |

## What I built (the minimum the file's section 4 names)

- `scripts/research/retrieval_log.py`: `numbers_stated(text, quote=False)` beside `normalise_quote` (about 65 lines). Reads decimal point/comma, space/NBSP/thin-space grouping, point/comma grouping, Indian grouping, symbol ratios (`:`, `/`, `∶`, `⁄`), ambiguous `1.200`/`1,200` carrying both readings; quote side also emits ratio operands and space-group pieces. No number-word list of any language.
- `scripts/db.py`: `_require_claimed_number` (called from `_require_verbatim` and from `amend_extraction`); `_verbatim_norm` deleted (`git grep -n _verbatim_norm -- scripts` is empty); `--value-as-written` on `add-extraction`, `value_as_written` in `insert_extraction`'s column whitelist and in `_AMENDABLE_SVE_FIELDS`. `derive-extraction` left alone (D5).
- `scripts/dbcore.py`: `QUANTITY_CLAIM_TYPES = ("numerical", "range")` with the "judged rule" comment.
- `scripts/migrations/126_value_as_written.sql`: derived number (`ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gave 125). `ALTER TABLE ... ADD COLUMN value_as_written TEXT CHECK (value_as_written IS NULL OR length(trim(value_as_written)) > 0)`, `PRAGMA user_version = 126`.
- Tests: 40 cases `T008-01`..`T008-40` at the end of `scripts/tests/test_run_pipeline_refusals.py` (before `finish()`; `grep -c '"T008-'` was 0 first). Refused and accepted lists are the file's; plus end-to-end through `insert_extraction` (one refusal, one acceptance), through `amend_extraction` (set on a row whose quote spells the number; refuse a wording not in the quote; refuse a wording where the quote states the numeral), the blank-wording CHECK, and the `QUANTITY_CLAIM_TYPES` ⊆ live `claim_type` vocabulary case. Probe `pid` comes from `P_ACTIVE` (query-derived); the sentences are typed fixtures.
- Callers repaired: `skills/run-pipeline_SKILL.md` (one sentence), `workplan/pipeline-state-graph/machines.yaml` (M04.t2 `to:` lists the amendable fields), `governance/context-map.yaml` (regenerated; D6).

## Check-by-check, before and after (each run as the registry runs it; `EXAMINED:` read)

| check | before | after | EXAMINED (before / after) | note |
|---|---|---|---|---|
| test_run_pipeline_refusals | rc 0 | rc 0 | 175 cases / 215 cases | +40 mine |
| test_scan_contract | rc 1, 2 failed | rc 1, 2 failed | 119 / 119 | G01, G02: the R2 baseline, not mine; failing-line diff empty |
| test_db_amend_writers | rc 0 | rc 0 | 161 / 161 | |
| observation_verbatim_audit | rc 0 | rc 0 | 96 / 96 | |
| extraction_relations_integrity | CLEAN | CLEAN | 271 / 271 | |
| test_author_presence | rc 0 | rc 0 | no summary `EXAMINED:` in the grep (P01 "EXAMINED 3" is per-case text); the file ends `EXAMINED: 13 assertion(s)` / 13 | the file's grep line shows a mid-file case, not the summary (D8) |
| test_search_log_completeness | rc 0 | rc 0 | 23 / 23 | |
| test_assess_cell_pilot | rc 0 | rc 0 | prints no `EXAMINED:` line | examined nothing by the brief's rule; prints "PASS: all pilot-engine branch tests" |
| test_validate_evidence_state_2_4 | rc 0 | rc 0 | prints no `EXAMINED:` line | same; prints "ALL PASS (0 failed)" |
| migration_reproducibility | PASS | PASS | 57 / 57 | `--deep` also PASS, 56 tables identical, `EXAMINED: 56` |
| schema_reference_audit | rc 0 | rc 0 | 1125 / 1128 | +3 references from my migration/test |
| test_db_integrity | 56/56 | 56/56 | 3659 / 3660 inspections; 10 passed having examined nothing (B04, I3, I3b, B09, C10, C05, D02, G03, K01, K02), same ten before and after | |
| column_vocabulary_audit | CLEAN | CLEAN | 56 tables, 818 columns / 56 tables, 819 columns | +1 column |

Failing-line diff (`before` vs `after`, the file's `grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL'`): empty for all thirteen.

Other commands the file names:
- `joined_cells_census.py`: before and after both end `EXAMINED: 457 text column(s) with data; 66 candidate(s)`; the bodies are identical.
- `migrate_db.py --rebuild`: rc 0. `migration_reproducibility.py --deep`: PASS.
- `skill_vocabulary_audit.py`: output byte-identical before and after (`76 token(s) in 18 file(s)`; red on base, in the R2 baseline).
- `build_graph.py --check`: `109 failure(s), 5 warning(s)` both before and after (red on the base too, and not in the R2 baseline; D9).

### The gate (`scripts/preflight.sh --base "$BASE" --explain`)

- Run 1 (all edits except the regenerated context map): `RESULT: PASS — 50 check(s) green, 4 nothing-in-scope, 11 advisory failure(s)`, `SELFTEST: PASS`. One of the 11 was `context_map_fresh` (mine, D6). The other ten: `scan_debt`, `verified_scan_integrity` (140 pairs), `validate_schema_cross_check`, `retired_vocabulary`, `research_dod`, `search_log_completeness`, `research_tooling_separation`, `research_protocol_audit`, `metadata_integrity_audit`, `test_scan_contract`. I ran the five that are not in the R2 baseline (`scan_debt`, `verified_scan_integrity`, `search_log_completeness`, `research_protocol_audit`, `metadata_integrity_audit`) on the stashed base: same rc and same `EXAMINED`/`FAIL:` lines. `research_tooling_separation` reads `origin/main`, not `$BASE` (D7). `search_log_completeness` failed inside the gate ("4 WebSearch ledger line(s) match no search_executions") but prints NOTHING-IN-SCOPE when run alone; it reads the coordinator session's ledger, not my diff.
- Run 2 (after `python3 scripts/generate/context_map.py`): `RESULT: PASS — 60 check(s) green, 4 nothing-in-scope, 11 advisory failure(s)`, `SELFTEST: PASS`, `PREFLIGHT: PASS`. `context_map_fresh` green. The 11 are the R2 baseline cases plus the base-red five and `research_tooling_separation` above. No blocking FAIL.
- NOTHING-IN-SCOPE (4): `extraction_follow_up_audit`, `citation_mining_session`, `adversarial_pass_recorded`, `medical_lens_integrity`. Not mine; none reads this change.

## Stored rows, by report only

Over every stored figure with no `[VERBATIM-EXEMPT` note (the changed function, `db._verbatim` stubbed to true): the census reads `examined 186 refused 2`, and the two are extraction 30 (`5` under the Dutch quote) and extraction 80 (`viisi prosenttia`). No other row is refused. (186 plus the exempt rows is the 214 `source_value_extractions` rows `extraction_relations_integrity` counts; the exempt count was not separately printed.)

## Sweep result

Names: `_require_verbatim`, `_verbatim_norm`, `_cjk_to_arabic`, `--claimed-value`, `--verbatim-exempt`, `_AMENDABLE_SVE_FIELDS`. The four commands (git grep over code; `sqlite_master`; check registry; prose and needles) ran for each. The hit lists match the file's lists exactly. `sqlite_master` and the registry returned `[]` for every name (stated as unproven-not-clean: the six views name the table, not these names; `ADD COLUMN` changes none, confirmed by the rebuild). Callers repaired: `skills/run-pipeline_SKILL.md` (sentence on `--value-as-written`), `workplan/pipeline-state-graph/machines.yaml` M04.t2 (found by reading the field list, not by the name sweep; D4), `governance/context-map.yaml` (regenerated; not in the sweep at all; D6). Mentions left: the `--verbatim-exempt` help/refusal strings (still true), `extraction_relations_integrity.py:144` comment (about `derive-extraction`, still true), `check-registry.yaml:162` (still true). `build_graph.py --check`: 109 failures before and after, unchanged.

## Code-size line

`git diff --cached --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` → ` 5 files changed, 256 insertions(+), 38 deletions(-)`. Of that, about 65 lines are the reader, about 90 the rule and writers (including comments), 68 are tests. What reads what is added: `numbers_stated` is read by `_require_claimed_number`; `value_as_written` is read by that rule at write time (and by T-111, T-037, T-049 later); `QUANTITY_CLAIM_TYPES` by the rule and T-016. `_verbatim_norm` and the old digit-substring block are deleted.

## Residual design hole the file's rule permits (the worst finding)

**`--value-as-written` launders any number.** Item 4 requires the wording only to occur in `claim_text` under the quote normalisation, and says the meaning is the extractor's judgment. As written (and as I built it), each of these is ACCEPTED, via the real function:

- `12` under "no higher than 1.2 m" with `--value-as-written "1.2 m"` (the decimal shift the task exists to catch, now passable with one flag);
- `1:12` under "...not steeper than 1:20 where the run exceeds 12 m" with `"1:20"`;
- `9999` under "no higher than 1.2 m" with `"higher"` (any word of the quote).

That reopens the 2026-08-19 shape ("a number attached to a quote") behind a flag. Word-to-number checking cannot be mechanical without a word list (forbidden). But a cheap, list-free tightening exists: refuse a `value_as_written` that itself contains an unambiguous numeral token (`numbers_stated(vaw, quote=True)` has an entry with one reading). `"1.2 m"` and `"1:20"` are then refused; `"vijf procent"`, `"viisi prosenttia"` and the ambiguous `"1,200"` (two readings) still pass. I verified the reader's output for those strings; I did not build or test the tightening, because section 4 does not name it. The residual (`9999` with `"higher"`) is real and by the owner's design; the file should say so in section 3 and require the adversarial pass to read every row with a non-NULL `value_as_written`.

## Task-file defects

Count: 11. The three worst are D1, D2 and D6.

**D1 (design; worst). `value_as_written` is a free pass.** Section 4 items 2(d) and 4 send every unmatched or ambiguous claimed number to the wording path, whose only check is "occurs in `claim_text`". Command and observed output above: `12`/"1.2 m"/`"1.2 m"`, `1:12`/"1:20 ..."/`"1:20"` and `9999`/"1.2 m"/`"higher"` are all ACCEPTED. The headline defect of the task (a shifted decimal) is closable again by one flag. Needs: either the numeral-in-wording refusal above, or an explicit statement in section 3 that the hole is accepted and the adversarial pass's duty.

**D2. The section 3 evidence command passes no `claim_type`; the file never says what the default means.** Item 5 says a no-number `claimed_value` is refused "for a `claim_type` that states a quantity". The command calls `_require_verbatim(..., claimed_value='twelve')` with no claim type and must print `REFUSED` on all six lines (the file says so). I had to decide that `claim_type=None` is treated as a quantity (so `twelve` refuses); a `qualitative` call must pass the type explicitly. Nothing in the file says this. Needs: one sentence in item 5 ("an unspecified `claim_type` is treated as a quantity") or `claim_type='numerical'` in the command.

**D3. Item 2 rule (b) leaves two cases open.** (i) "if the quote states any [symbol ratio]": a standard number such as `AS 1428.1:2021` is a symbol ratio token, so a sentence that cites it and writes the gradient in words (`1 in 12`) disables operand matching for a claimed `1:12` (it must equal `1428.1:2021`). (ii) When the quote states a symbol ratio and the claimed ratio differs, the file lists refusals (`1:12` under `1:20 ... 12 m`) but does not say whether this is a hard refusal or the "not stated as a numeral" path of item 4. I chose the latter (the case is refused without a wording, accepted with one, see D1). Needs a sentence for each.

**D4. The name sweep cannot find a prose caller that lists the fields.** `machines.yaml` M04.t2 says `"any (extraction_method, extraction_status, figure_role, comparator, root_type, root_ref_id only)"`; the swept name `_AMENDABLE_SVE_FIELDS` appears there only as an unrelated needle. I found the stale list by grepping `root_ref_id`. Section 5's "Callers already known" should name it, and the swept names should include the field names that item 6 changes.

**D5. Item 6's `derive-extraction` rule is ambiguous for this verb.** `derive_extraction` passes a quoted `claim_text` and an optional own `--claimed-value`, but computes `claimed_value` from base+delta when it is omitted. The file's "pass through only if it already passes a quoted claim_text and a claimed_value of its own; if it computes the value, leave it" fits both branches. I left it (a computed sum is not a source wording). The last stop-condition bullet ("`derive-extraction` needs a different treatment than item 6 foresees") was not triggered by my reading; the file should say which branch is meant.

**D6. A schema bump makes the generated `governance/context-map.yaml` stale, and nothing in the file says so.** The first gate run failed `context_map_fresh` (`STALE: governance/context-map.yaml differs from a fresh generation. Run: python3 scripts/generate/context_map.py`; diff: `db_fingerprint`, `schema_version: 125 -> 126`, and a new `writers` entry). It is not in section 5's hit lists, not in section 6's check list, and not in the commit instructions. It cost a second gate run of about four minutes, which the "run the gate once" rule forbids. Needs: a step in section 4's migration paragraph ("regenerate `governance/context-map.yaml` with `python3 scripts/generate/context_map.py` and include it") and `context_map_fresh` in section 6 step 1's list.

**D7. `research_tooling_separation` is red on this base for a reason the file's text contradicts.** It prints `Changeset vs origin/main: 738 path(s)` and lists twelve `data_*.sql` files as research, so its verdict is `FAIL — this changeset carries both research data and tooling`, while section 4 states "The pull request contains no `scripts/migrations/data_*` file". It diffs against `origin/main`, not `$BASE`, and CLAUDE.md rule 10 itself says a schema-only change with `data/guidebook.db` is not a violation. Section 6 step 4's "name it in the pull request" does not list which advisory failures to expect; an executor cannot tell mine from the base's without re-running ten checks on a stash, which is what I did.

**D8. Section 6 step 1's per-check line is not always a subject.** The file says "Each line shows the check's subject (`EXAMINED:`)". `test_assess_cell_pilot` and `test_validate_evidence_state_2_4` print no `EXAMINED:` at all; `test_author_presence`'s `grep` returns a mid-file case ("EXAMINED 3"), not its summary (`EXAMINED: 13 assertion(s)`). The brief tells me to call the first two "examined nothing", but they run and pass real assertions; the file should name the checks whose output has no summary line.

**D9. `build_graph.py --check` is red on the base (109 failures), and the file asks to "report its result" as if it were a signal.** Before and after counts are equal (`109 failure(s), 5 warning(s)`). Not in the R2 baseline file. Section 5 should give the base value to compare against.

**D10. The migration paragraph steers toward the wrong technique and leaves a header unexplained.** "SQLite cannot add a NOT NULL foreign key or change a CHECK in place: use create, copy, drop, rename ... list every view and index that names the table" is irrelevant to a nullable column with a CHECK: `ALTER TABLE ... ADD COLUMN` works (precedent: migration 119) and a rebuild of a table that many tables and views point into is the riskier path. The file should say "use `ADD COLUMN`; the rebuild list is for a NOT NULL/FK change". The neighbouring `-- AFTER_DATA:` header (migration 125 carries one) is not mentioned; mine needs none, and I judged that from `migrate_db.py`'s docstring.

**D11. Minor friction.** (a) Section 6 step 4's gate takes over two minutes and the harness moved it to the background at 120 s; say "run it in the background and poll". (b) Section 6 step 2 says the pilot's patch "shows one way" to build the fixture; the sentence is a pointer to a record I was told not to use. The file should give the three lines itself (`new_source(verified=True)` inside `with scratch() as c:`, `held_text(ref, "\n".join(sentences))`, and `hand_scan(c, ref, "full")` for the end-to-end rows). (c) `CLAUDE.md` rule 7a: my first draft of the migration comment carried hand-typed counts ("six views, three indexes"); I replaced them with the `sqlite_master` command. The file's own example text ("the pilot found two") is dated but is labelled with a command. (d) The `value_as_written` under `--verbatim-exempt` is never checked (the exempt branch returns before the number rule, "unchanged" per item 5); an exempt row can store any wording. Consistent with the file; worth a sentence.

## Behaviours worth knowing (not file defects)

- `_cjk_to_arabic` is now applied to the quote always, not only as a fallback. A kanji such as 一 inside a word (一般) becomes a stated "1" on the quote side. Pre-existing conversion, unchanged, and only loosens CJK sources slightly.
- Plain claimed numbers are matched without consuming a quote token (only ratio operands consume), so `1200-1200` style duplicates match one token. Not specified; harmless.
- A date such as `12.03.2021` is read as 12.03 and 2021; a table run `2021 200` is read as 2021 and 200 (a space group needs a first group of at most three digits).
