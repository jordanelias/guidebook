# T-008 pilot report: the claimed number is checked as a number

## Verdict

**Did the task file suffice to complete it: PARTLY.** The mechanics (set-up, evidence command, change location, sweep, red/green test, gate, commit) all worked. The change itself could not be completed from the file alone. Section 4 prescribes a rule that is under-specified (which claim types state a quantity, how to read ratios and groupings, how to treat an ambiguous quote) and one prescribed rule (item 2) creates a dead end that the file does not see. I made the decisions below and flagged each. No stop condition was formally triggered, but section 9's last two bullets were exercised.

Work was done in `/tmp/claude-0/pilot/T-008`, branch `pilot-T-008`, one commit: `governance: compare claimed values as numbers in the verbatim check [2026-11-12 05:51]`. The canonical `data/guidebook.db` sha256 is unchanged (`c9ecb846...c4d`). Nothing was pushed.

## Before and after (headline)

BEFORE, section 3 evidence command, verbatim:

```
12 | no higher than 1.2 m -> ACCEPTED
0.6 | a time of 6.0 s -> ACCEPTED
1:1 | not steeper than 1:12 -> ACCEPTED
112 | not steeper than 1:12 -> ACCEPTED
twelve | not steeper than 1:12 -> ACCEPTED
```

(Matches "expected output today".) The evidence command only exercises the old logic, so it does not show the AFTER. AFTER, same inputs through the real `db._require_verbatim` (quote lookup stubbed, since only the number rule is under test):

```
12      -> REFUSED: add-extraction: claimed_value '12' contains ['12.0'], which are not numbers the verified --claim-text states (compared as numbers, so 1.2 is not 12, 6.0 is not 0.6 and 1:12 is not 1:1). ...
1.2     -> ACCEPTED   (against "no higher than 1.2 m")
1:12    -> ACCEPTED   (against 勾配は、十二分の一を超えないこと。)
1.200   -> REFUSED: ... holds a number that reads two ways (1.2 or 1200.0) ... Write the unambiguous form (1200, or 1.2) ...
twelve  -> REFUSED: claim_type='numerical' states a quantity but claimed_value 'twelve' contains no number ...
```

Red test (section 6), `python3 scripts/tests/test_run_pipeline_refusals.py`:
- BASELINE on untouched code (before adding my cases): `EXAMINED: 175 cases`, `PASS: all 175 cases`. `test_scan_contract.py`: `RESULTS: 117/119 tests passed`, `FAILED: 2` (advisory, red on the base).
- RED (new cases added, old `db.py` and `retrieval_log.py`): `EXAMINED: 199 cases`, `FAILED: 8`. Red cases: T8-01 (`12` vs `1.2 m`), T8-02 (`0.6` vs `6.0 s`), T8-03 (`1:1` vs `1:12`), T8-04 (`112` vs `1:12`), T8-05 (`120.0` vs `1 200`), T8-15 (ambiguous `1.200`), T8-16 (end to end, decimal-shifted value through `insert_extraction`), T8-17 (end to end, `twelve`).
- GREEN (change applied): `EXAMINED: 199 cases`, `PASS: all 199 cases`. The accept cases (`1.2` vs `1,2 m`, `1200` vs `1 200 mm`, `1:12` vs `十二分の一`, `1:12` vs `1 in 12`, `150000` vs `1,50,000`, `1234.56` vs `1.234,56`) were green before and after, as regression guards.
- `test_scan_contract.py` after: `117/119`, `FAILED: 2`, identical to the base.

## What the change does to the pipeline's behaviour

`add-extraction` and `derive-extraction` (both reach `insert_extraction`, which is the only caller of `_require_verbatim`) used to accept a `claimed_value` if every digit run in it occurred as a substring of the quote after `normalise_quote` had deleted all punctuation. They now read the numbers the quote states before punctuation is removed (`retrieval_log.read_numbers`: decimal point or comma, thousands grouping, Indian grouping, ratios `1:12` / `1/12` / `1 in 12` / `12分の1` / `8분의 1`), compare them as numbers, and refuse otherwise. Concrete example: an extraction with claim text "The handrail is to be no higher than 1.2 m above the floor." and `--claimed-value 12` was written before (digits `12` are a substring of `12`, the normalised digits of `1.2`) and could govern a determination as 12 m. It is now refused with the message above, while `--claimed-value 1.2` still lands. A `numerical` or `range` row whose `claimed_value` has no number at all (`twelve`) is refused instead of passing unchecked. A lone `1.200` or `1,200` in `claimed_value` is refused with a request for the unambiguous form.

## Census of stored rows (section 6, read-only)

`select count(*) from source_value_extractions where claimed_value glob '*[0-9]*'` gives 183 rows. I ran the real `_require_verbatim` (quote lookup stubbed) over those plus numerical/range rows without digits: 184 examined, 5 would be refused, of which 3 carry a `[VERBATIM-EXEMPT` note and so never reach the number check in the writer. The 2 real ones:
- extraction 30 (REF-00995, `numerical`, claimed `5`, quote "vijf procent bij niveauverschillen van 50 cm of groter"). The old check passed it only because `5` is a substring of `50`. The Dutch word is a legitimate five, so this is a true catch of a wrong mechanism and a row the new rule makes unfilable.
- extraction 80 (REF-01017, `numerical`, claimed `viisi prosenttia`). This is the GAP-056 workaround row, refused by item 2.
Not amended (as instructed). The census script is `/tmp/claude-0/pilot/census.py`.

## Task-file defects (section numbers)

1. **Section 1/2, set-up.** `git switch -c ... origin/main` is wrong in this clone: `origin/main` is an ancestor of the workplan branch and does not contain the task files (106 commits behind). I branched from the cloned HEAD instead. Consequently `git diff --shortstat origin/main ...` and `scripts/preflight.sh` (which diffs against `origin/main`) report the whole workplan, not the task: `29 files changed, 4538 insertions(+), 1051 deletions(-)`. I measured against `HEAD~1` and ran the gate as `--changed-from HEAD`.
2. **Section 4 item 2 creates a dead end (decisive).** "A `claimed_value` that contains no number... is refused unless the row carries `--verbatim-exempt`." But `_require_verbatim` refuses the exemption whenever the text verifies, and a spelled-out value always sits under a verifying quote. So Finnish, Dutch, Swedish, French and German spelled-out cardinals become unfilable. This is exactly the open GAP-056 (`sessions/session_2026-09-28-research-batch-22-selection.md` section 4, REF-01017, extraction 80), and the file does not mention it or the live row it refuses. The file should say either that GAP-056 is fixed first, or what path replaces the exemption. I implemented item 2 as written and flagged it.
3. **Section 4 item 2, "a `claim_type` that states a quantity" is not named.** The CHECK has `numerical, range, qualitative, framework, absent`. I used `numerical` and `range` (hard-coded; rule 8 would want it derived, and it cannot be from the CHECK).
4. **Section 4 item 1, the list of number forms is incomplete against live rows.** It names decimals, grouping and `1:12`, `1/12`, CJK. Live rows also need: `1 in 12` (extractions 75 and 79; without it they are false refusals), the Korean/Chinese n-th-part forms, and operands of a colon form. A naive atomic ratio reading refused `AS 1428.1:2021` (read as a ratio 1428.1/2021) and a table cell `800 750` (read as 800750; extractions 169 to 174). I had to add "ratio operands and space-group pieces also count as stated numbers on the quote side" and typed readings (`n` plain, `r` ratio) so `1:1` still fails against `1:12`. Residual: a plain `12` is still accepted under `1:12`, and `1:12` is not matched by "1 zu 12" or "1 sur 12" (per-language wording is not covered; GAP-056's family).
5. **Section 4 / section 9, ambiguity in the quote is undecided.** Section 9 says refuse an ambiguous format "asking for the unambiguous form", which is only actionable for `claimed_value`. For a quote that says `1,200` I admit both readings (1200 and 1.2), so a claimed `1.2` against a quote `1,200 mm` would pass. The file should state the intended policy.
6. **Section 4 "What reads what" lists `amend-extraction`.** `amend_extraction` only amends `_AMENDABLE_SVE_FIELDS` and never calls `_require_verbatim`; the readers are `add-extraction` and `derive-extraction` (via `insert_extraction`). Minor.
7. **Section 5, sweep names `_verbatim_norm`.** Its only caller was the block I replaced, so after the change it is unread; I deleted it (CLAUDE.md section 8). The file does not say keep-or-delete. `_cjk_to_arabic` stays in `db.py` and is composed with the reader, not moved (the file says "one home beside `normalise_quote`" for the reader only).
8. **Section 5, prose callers.** The five prose paths are clean, but `gaps` descriptions in the committed data migrations and `sessions/session_2026-09-28-research-batch-22-selection.md` section 4 (GAP-056) restate the old digit-check behaviour. They are outside the listed paths (frozen), so I left them; the file should say a GAP-056 note is owed.
9. **Section 6, evidence command reads only the old logic.** It reimplements the old test inline, so it cannot show the AFTER; I added a second probe through the real function. The "three tests" `test_scan_contract` is red on base (2 failing), as the file warns; fine.
10. **Section 6, the "new check over the stored rows" step** says "run the new check" but no standalone check exists; I stubbed `_verbatim` and called the writer function. A one-line recipe would help.
11. **Section 7, the commit body** is left to the executor; fine, but the timestamp format and trailers were clear.
12. **Rule 7/7a.** The test file now has the cases but no `EXAMINED` change is needed; the test prints its own count (199 cases, derived).

## Checks

Gate: `python3 scripts/run_checks.py --changed-from HEAD --explain` (the file's `origin/main` form diffs the whole workplan here). Work kind `tooling`, 24 of 75 checks selected, `RESULT: PASS — 22 check(s) green, 2 advisory failure(s)`. Advisory failures: `retired_vocabulary` (`RESULTS: 113 occurrence(s)`, identical on the base) and `test_scan_contract` (`117/119`, identical on the base). Examined: `test_run_pipeline_refusals` EXAMINED 199; `test_db_amend_writers` 161; `retired_vocabulary` 27 register entries; `test_scan_contract` 119; nothing under NOTHING-IN-SCOPE. `--selftest` (run once because a private function was removed): `SELFTEST: PASS`. `scripts/preflight.sh` itself was not run: it diffs against the stale `origin/main`.

## Code size

`git diff --shortstat HEAD~1 -- scripts schemas .github skills ':!scripts/migrations'`: `3 files changed, 173 insertions(+), 33 deletions(-)` (numstat: `db.py` +37/-33, `retrieval_log.py` +72, test file +64). Against the stale `origin/main` the same command gives `29 files changed, 4538 insertions(+), 1051 deletions(-)` (not meaningful). Added code is read by `_require_verbatim`, which `add-extraction` and `derive-extraction` call; it makes `_verbatim_norm` deletable (deleted).

## Commands run (abridged)

`ls tasks | grep T-008`; `git clone --quiet /home/user/guidebook /tmp/claude-0/pilot/T-008`; `git switch -c pilot-T-008`; `bash .claude/hooks/ensure-deps.sh`; `sha256sum data/guidebook.db`; the section 3 evidence command; baseline `python3 scripts/tests/test_run_pipeline_refusals.py` and `test_scan_contract.py`; added cases, ran them on old code (red) then new code (green); `/tmp/claude-0/pilot/census.py` under `python3 -I` with `GUIDEBOOK_DB_PATH` set to the clone's DB (read-only); the section 5 sweep for `_require_verbatim`, `_verbatim_norm`, `_cjk_to_arabic` and `read_numbers`; `python3 scripts/run_checks.py --changed-from HEAD --explain`; `python3 scripts/run_checks.py --selftest`; `git commit`; `git format-patch -1 --stdout`.
