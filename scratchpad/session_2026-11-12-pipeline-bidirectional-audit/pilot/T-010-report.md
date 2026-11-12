# T-010 pilot report: `add-parameter` refuses a term that is not a design quantity

Clone: `/tmp/claude-0/pilot/T-010`, branch `pilot-T-010`, commit `4c82d6f`. Patch: `T-010.patch` (same folder). Nothing pushed; no PR; adversarial pass not run (as instructed). Canonical DB sha256 unchanged: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d` before and after.

## Verdict: PARTLY (the task file sufficed for the core change, but its caller sweep, as written, would have halted a literal executor, and two instructions do not match the tree)

The change, the red test and the green test were completed from the file alone. Three things needed judgment the file does not give: (1) the sweep found a real caller the file does not name (a test that went red from this change), (2) the file's base branch instruction does not fit the clone, (3) the refusal message needs a "what to do next" the file does not specify and no verb exists for.

## BEFORE (section 3 evidence command, on a scratch copy; output verbatim)

```
{ "parameter_id": 13, "term_id": "TERM-041", "canonical_en": "Reach & manipulation", "status": "active",
  "provenance": "base-vocabulary", "adjudicated_by": null, "outcome": null, "dry_run": false }
rc=0
[('TERM-041', 'Reach & manipulation', 'functional_axis'), ('TERM-075', 'jurisdictional accessibility standards', 'legal')]
[('circulation',), ('hardware',), ('acoustic',), ('wayfinding',), ('lighting',)]
```
Matches the file's "Expected output today": created rc=0; domains functional_axis and legal; no live parameter in either.

Red test BEFORE (new case AP1 in `scripts/tests/test_run_pipeline_refusals.py`, section A7b, on unchanged code):
```
Section A7b: add-parameter refuses a term filed under a lens, method or law domain (T-010)
  [✗] P01: dbcore.NON_QUANTITY_DOMAINS names the refused domains      (case later renamed AP1)
      feature absent: dbcore.NON_QUANTITY_DOMAINS
EXAMINED: 176 cases / SKIPPED-NO-FIXTURE: 0 / FAILED: 1
```
(AP2 to AP5 are gated on AP1's feature probe, so they do not run when it is absent; the suite's own test-design rule.)

## AFTER

CLI, scratch copy (`add-parameter --term-id TERM-041`, then `TERM-075`):
```
REFUSING: TERM-041 ('Reach & manipulation') is filed under the domain 'functional_axis', which names a lens, a method or a body of law, not a quantity of the built environment. A parameter is what is under determination in a room, a route or a fitting.
Domains of the live parameters: ['acoustic', 'circulation', 'hardware', 'lighting', 'wayfinding']. Refused domains: ['economics', 'functional_axis', 'legal', 'medical', 'methodology', 'population'] (dbcore.NON_QUANTITY_DOMAINS).
If the term is a quantity filed under the wrong domain, no verb corrects a term's domain today: file it as a GAP; do not hand-write SQL. Nothing was written.
rc=1
```
TERM-075 identical shape with domain 'legal', rc=1. A circulation term still promotes: `--term-id TERM-048` and `TERM-022` give parameter_id 13, status active, rc=0 on the scratch copy.

Green test AFTER:
```
  [✓] AP2: add-parameter refuses TERM-031 'Ambulant movement' (domain functional_axis), naming the domain and printing the live parameter domains
  [✓] AP3: add-parameter refuses TERM-067 'CRPD (...)' (domain legal), naming the domain and printing the live parameter domains
  [✓] AP4: a circulation term (TERM-014) is still promoted
  [✓] AP5: no live parameter sits in a refused domain (the rule orphans nothing)
EXAMINED: 179 cases / SKIPPED-NO-FIXTURE: 0 / PASS: all 179 cases
```
Can it fail? Seeded defect (refusal disabled with `if False and ...`): `AP2 [✗]`, `AP3 [✗]`, `FAILED: 2`; AP4 and AP5 stay green (control cases). Seed reverted (checked).

Probes in the test are derived (first unpromoted, undeclined term of each domain), not the file's hard-coded TERM-041/TERM-075 (CLAUDE.md rule 8); the CLI demonstration above uses the file's ids.

## What the change does to the pipeline's behaviour

Base stage, term to parameter. Before, `db.py add-parameter` promoted any term that was not declined, value-bearing or already a parameter, whatever the term was: a lens (a functional axis such as "Reach & manipulation"), a method ("universal design") or a body of law ("CRPD"). Each such promotion created a `base_parameters` row, so every held source then owed a reading for it and the engine would determine it as a pending cell with a gap for any group named. Now `insert_parameter` looks at `terms.domain` and, if it is in the single constant `dbcore.NON_QUANTITY_DOMAINS`, refuses with the domain, the live parameter domains and the next action, and writes nothing. Example: input `add-parameter --term-id TERM-041` (domain functional_axis) went from rc=0 and a new parameter_id 13 to rc=1 with a refusal; `--term-id TERM-048` (circulation route) is unchanged, rc=0. Effect on the guidebook: no new non-quantity "parameters" reach the scan ledger or the engine. It does not touch existing rows, `grab bar`-type element terms (T-020), or terms with a NULL domain.

## Caller sweep result (section 5) and the extra change it forced

Ran all five commands for `insert_parameter` and `add-parameter` (output: `/tmp/claude-0/pilot/scratch-t-010/sweep.txt`, 205 lines). Views/triggers/indexes: `[]` for both. Registry: `[]` for both. Skills/.claude: `skills/run-pipeline_SKILL.md:70` and `.claude/settings.json:77` mention the verb, neither states the refused set; no edit needed. Behavioural callers found:
- `scripts/tests/test_scan_contract.py` builds `FREE` terms by term_id order and promotes `FREE[10]` (TERM-017 "universal design", domain methodology) in case V03. **V03 went red because of this change** (before: V03 green; G01 and G02 were already red on this tree). Fixed in this diff: `FREE` excludes `dbcore.NON_QUANTITY_DOMAINS`. After: back to 117/119 with only the pre-existing G01, G02 red.
- `scripts/tests/test_db_amend_writers.py` (calls `insert_parameter`): unchanged, 161 assertions pass before and after.
- `scripts/audit/research_batch_dod.py:987-992` (prose in a comment): says add-parameter's only refusal exception is a value-bearing name. Now stale; one sentence added naming the second exception (rule 7's prose caller).
- `workplan/pipeline-state-graph/machines.yaml:156-158` uses needles on refusal strings in `insert_parameter`; none of the three needles was touched.
- `scripts/validate_parameters.py:26` and `governance/research-contract.yaml:311`, `stage-map.yaml:64`: prose, not affected.
Literal strict reading of section 9 ("the caller sweep finds a caller this file does not mention") would stop here, since the file names no caller at all.

## Checks

`scripts/preflight.sh` (once; 1m40s): `PREFLIGHT: PASS`, 22 green, 2 advisory failures: `retired_vocabulary` (113 occurrences, identical before and after: 113 / 27 register entries) and `test_scan_contract` (G01, G02, red on the base before my edit). Then `run_checks.py --changed-from origin/main --explain` (identical result; duplicate of the wrapper). `--selftest` not run (nothing renamed, no registry edit). EXAMINED lines visible: test_run_pipeline_refusals 179, test_scan_contract 119, test_db_amend_writers 161, retired_vocabulary 27 register entries; no check printed NOTHING-IN-SCOPE. Passing checks print no EXAMINED line unless failing or floorless (see defect 7).

## Diff stat

`git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'` in the clone, with `origin/main` set to the starting commit (see defect 1): `5 files changed, 63 insertions(+), 4 deletions(-)`. Files: `scripts/dbcore.py` (+11, the constant), `scripts/db.py` (the refusal, docstring, help text), `scripts/tests/test_run_pipeline_refusals.py` (+28), `scripts/tests/test_scan_contract.py` (fixture), `scripts/audit/research_batch_dod.py` (+2 comment lines). Reads the constant: `insert_parameter`, `test_scan_contract`, `test_run_pipeline_refusals`. Replaces nothing.

## Defects, ambiguities and omissions in the task file

1. **Section 2 set-up, base branch.** `git fetch origin main && git switch -c ... origin/main`: in the clone `origin/main` is 106 commits behind the branch that holds the task file and the workplan (`git rev-list --count origin/main..HEAD` gives 106). Switching to it would have lost the task file and changed the DB and scripts the evidence command expects; `git diff origin/main` would also include 106 commits. I branched from the clone's HEAD and pointed local `refs/remotes/origin/main` at it (clone only). The file should name the branch to start from, or the index should say the workplan must be on `main` first.
2. **Section 2 "Open the session with `/session-open`"**: not available/meaningful in a pilot clone; CURRENT already named the audit session. Not exercised.
3. **Section 4.1 does not say what the refusal should tell the reader to do.** The natural text ("correct the term's domain") points to a verb that does not exist (`_AMENDABLE_TERM_FIELDS = ("definition", "scope_note")`). I wrote "file it as a GAP; do not hand-write SQL". The file should state this, or file the missing domain-correction writer as a gap.
4. **Section 4.1 "have the refusal message print the live parameter domains"**: fine, but does not say whether to include the refused set too; I did. Also the constant's comment "giving the query that justifies it and the date": the date is the task's own (2026-11-12), not the executor's `date`; I used 2026-11-12.
5. **Section 5, the sweep is mechanical but the instructions give no method for judging a hit.** The sweep returns about 200 lines of mostly irrelevant prose (workplan/, pipeline-state-graph/). The task omits the one caller that matters: `scripts/tests/test_scan_contract.py` (V03 regresses via `FREE`), and the stale comment in `research_batch_dod.py`. Section 9's stop condition ("a caller this file does not mention") together with a file that mentions none is unsatisfiable as written; it should list the known callers or define "affected".
6. **Section 6 "Add the cases to `scripts/tests/test_run_pipeline_refusals.py`" names no section or id convention.** Ids `P01-P09` already exist in that file (collision on first try; I used `AP1-AP5`). Also the test hard-coding TERM-041/TERM-075 would break the file's own rule ("Nothing here types an id the database can derive"); I derived the probes.
7. **Section 6 "find every check this task touches and read its EXAMINED: line"**: passing checks print no EXAMINED line in either `preflight.sh` or `--explain` output (only failures and floorless-with-live-subject notices do). The instruction cannot be followed for the other checks without opening each. Also the gate block runs `preflight.sh` and then `run_checks.py --changed-from ... --explain`, which is the same run twice (preflight wraps run_checks), against CLAUDE.md §1 "never re-run a check when nothing has changed".
8. **Section 6 "promoting a `circulation` term that is not yet a parameter still works"**: the first circulation candidate by id (TERM-089 "ramp") is DECLINED, so a naive probe fails on the declination, not the new rule; the file should say to exclude declined terms. I excluded them.
9. **Section 8/9 vs. what was needed**: the file forbids adding anything it does not name, but fixing the test fixture (`test_scan_contract.py`) and the comment (`research_batch_dod.py`) were needed. Section 5 permits "fixed in this same pull request", so this is consistent, but sections 8 and 5 pull different ways.
10. **Section 9, second-last bullet** ("a live parameter has one of the refused domains") is checked by AP5 in the test; good, no defect. The pre-existing red `test_scan_contract` G01/G02 and `retired_vocabulary` are not mentioned in the file; it points to row B-82 of `hs-stress-audit.md` for standing failures, which I did not open (not required reading).
11. **Section 7 commit message** uses the skill name `governance`, correct per CLAUDE.md rule 1; trailers supplied by the session as the file directs.

## Commands run (clone `/tmp/claude-0/pilot/T-010`, scratch `/tmp/claude-0/pilot/scratch-t-010`)

`git clone`, `git checkout -b pilot-T-010`, `bash .claude/hooks/ensure-deps.sh`; `git update-ref refs/remotes/origin/main HEAD`; `sha256sum data/guidebook.db`; evidence command (three parts) on `t.db`; `python3 scripts/tests/test_run_pipeline_refusals.py` (red, green, seeded-defect); `db.py add-parameter` for TERM-041, TERM-075, TERM-048, TERM-022, TERM-089 on scratch copies; sweep commands from section 5 (stash/pop around them so they ran against the pre-change tree); `scripts/tests/test_scan_contract.py` and `test_db_amend_writers.py` before and after; `scripts/preflight.sh`; `scripts/audit/retired_vocabulary_audit.py` before and after; `python3 scripts/run_checks.py --changed-from origin/main --explain`; `git commit`; `git format-patch -1 --stdout`.
