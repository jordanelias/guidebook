# T-073  A fixture source never takes an id the retrieval log already holds

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-57, item (18) (`grep -n -F '(18) The fixtures of' workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 (Opus-class plan integrator). The defect was reproduced on scratch copies (section 3); no fix was prototyped. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-073 |
| Title | A fixture source never takes an id the retrieval log already holds |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 0 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | OI-57 item (18); CLAUDE.md rule 8 ("an identifier from the union of its homes"); the A3 cases X02 and X03 of `scripts/tests/test_run_pipeline_refusals.py` |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** none. Check by running: nothing to check.
- **Owner decisions:** none.
- **Tests that must be red before you start:** the new case `T073-01` (section 6 step 2) is red on the unchanged fixture root. X02 and X03 are red only while a retrieval-log folder holds the next id (section 3); do not create one under the repository's `retrieval-log/` to make them red.
- **Ordering with research.** The next real admission takes the id these fixtures take today (section 3). OI-57 (18) holds that the batch which admits it should not ship before this task; this file does not gate on that batch, and touches nothing of it (do not read, move or edit any folder under `retrieval-log/` that is not tracked: `git status --short retrieval-log/`).
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml, pymupdf"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-073-fixture-ids-free-of-the-retrieval-log "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task has no migration
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-073" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

A batch persists what it fetched under the id its source will take (`retrieval_log.fetch(..., ref_id=...)`) before `db.py add-source` admits the source. Between the two, the retrieval log holds an id the database does not. The test fixtures mint their sources through the writer, which takes `dbcore.next_ref_id(conn)`: the database's high-water mark, the union of every table that holds a `ref_id`, plus one. The retrieval log is not one of those homes, so the first fixture source takes the pre-admission folder's id and inherits its saved text. `--verbatim-exempt` is then refused over "a decodable body held for the source" (`db._refuse_exempt_with_body`), and cases X02 and X03 go red for a reason that has nothing to do with what they test. A red that comes and goes with the working tree teaches the reader to ignore the suite (CLAUDE.md §5 (a)); a false green is as likely the next time, in a case that asserts a refusal. What reaches the guidebook without the fix: nothing directly; what reaches the plan is a refusal suite whose verdict depends on an untracked folder.

**Evidence commands** (read-only on the repository; the reproduction writes only under `$SCRATCH`):

```
# (1) Which retrieval-log folders hold an id above the database's high-water mark (a pre-admission fetch)
python3 -I - <<'PY'
import json, pathlib, re, sqlite3, sys
sys.path.insert(0, 'scripts'); import dbcore
hw = dbcore.ref_id_high_water(sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True))
print('high water', hw)
for m in sorted(pathlib.Path('retrieval-log').glob('*/manifest.jsonl')):
    ids = {json.loads(l).get('ref_id') for l in m.open() if l.strip()}
    ahead = sorted(i for i in ids if i and re.fullmatch(r'REF-(\d{5})', i) and int(i[4:]) > hw)
    if ahead: print(m.parent.name, ahead, '(tracked)' if __import__('subprocess').run(['git','ls-files','--error-unmatch',str(m)],capture_output=True).returncode == 0 else '(untracked)')
PY
# (2) The fixture's shape, twice on fresh copies: without and with a scratch folder holding the next id
cat > "$SCRATCH/repro.py" <<'PY'
import hashlib, json, os, pathlib, sqlite3, subprocess, sys
REPO = pathlib.Path.cwd(); db_path, root, seed = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3] == "1"
root.mkdir(parents=True, exist_ok=True)
for d in sorted({p.split("/")[1] for p in subprocess.run(["git", "ls-files", "retrieval-log"], capture_output=True, text=True).stdout.split() if p.count("/") >= 2}):
    if not (root / d).exists(): os.symlink(REPO / "retrieval-log" / d, root / d)          # tracked folders only
os.environ["GUIDEBOOK_DB_PATH"], os.environ["GUIDEBOOK_RETRIEVAL_LOG"] = db_path, str(root)
sys.path[:0] = [str(REPO / "scripts"), str(REPO / "scripts" / "research"), str(REPO)]
import db, dbcore, retrieval_log
def put(ref, session, artefact, body, **extra):
    d = root / session; d.mkdir(exist_ok=True); (d / artefact).write_bytes(body)
    with open(d / "manifest.jsonl", "a") as fh:
        fh.write(json.dumps({"retrieved_at": "2026-11-13T00:00:00+00:00", "ref_id": ref, "url": "https://example.invalid/" + artefact, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body), "exit": 0, "status": 200, "artefact": artefact, **extra}) + "\n")
    retrieval_log._ARTEFACT_INDEX.clear()
nxt = dbcore.next_ref_id(sqlite3.connect(db_path)); print("next_ref_id on the copy:", nxt)
if seed: put(nxt, "session_t073-preadmission", nxt + "-full-text.txt", b"A decodable text of a real document.\n", content_type="text/plain")
ref = db.insert_evidence_source({"year": 2020, "evidence_type": "code", "scope": "intrinsic", "verification_status": "UNVERIFIED", "title": "T-073 reproduction fixture on handrail finials"}, "session_t073-repro", dry_run=False, authors=db.parse_author_flags(["corp|Fixture Body"]))
print("fixture source took:", ref)
put(ref, "session_fixture", ref + "-undecodable.pdf", b"%PDF-1.4\n" + bytes(range(256)) * 8, content_type="application/pdf")
try: print("X02 shape: exemption ACCEPTED", repr(db._refuse_exempt_with_body(ref, "claim_text", "X02-repro")))
except dbcore.Refusal as e: print("X02 shape: exemption REFUSED:", str(e)[:200])
PY
for s in 0 1; do cp data/guidebook.db "$SCRATCH/c$s.db"; rm -rf "$SCRATCH/rl$s"; python3 -I "$SCRATCH/repro.py" "$SCRATCH/c$s.db" "$SCRATCH/rl$s" $s 2>&1 | tail -3; done
rm -rf "$SCRATCH"/c?.db "$SCRATCH"/rl?
# (3) Every test that mints a fixture source, and which retrieval root it reads
for f in $(git grep -l -E 'insert_evidence_source|"add-source"|next_ref_id' -- scripts/tests); do echo "$f root:$(grep -c 'GUIDEBOOK_RETRIEVAL_LOG' $f) exemption-or-artefact-reads:$(grep -c -E 'verbatim.exempt|decodable|artefacts_for_source|locate_quote' $f)"; done
```

**Expected output** (2026-11-13): (1) prints the high-water mark and one untracked folder, `session_2026-11-13-edmonton-checklist-pass`, holding the next id. (2) without the seed: the fixture takes the next id and the exemption is `ACCEPTED ''`; with the seed: the same id, and `REFUSED: X02-repro: --verbatim-exempt refused (R10) -- 1 decodable body artefact(s) are held for REF-… (session_t073-preadmission/REF-…-full-text.txt)`. So X02 and X03 are red if, and only if, a folder the fixture root reaches holds the next id. (3) prints four files, the first number being how often each names `GUIDEBOOK_RETRIEVAL_LOG`: `test_run_pipeline_refusals.py` (root: a scratch farm of symlinks to **every** folder under `retrieval-log/`, untracked ones included; reads artefacts: yes; **red today**), `test_db_amend_writers.py` (root: **none set**, so it reads the repository's `retrieval-log/` directly; reads artefacts: yes; not red today, because its first fixture, `R1` of section S, uses no exemption; the case that takes a pre-admission id depends on the order fixtures are minted, which is fragile), `test_author_presence.py` (root: an empty temporary folder: isolated, not this shape) and `test_db_integrity.py` (names `next_ref_id` in a comment only). `test_scan_contract.py` is not printed (it mints no source through these names) and also uses an empty temporary root.

If (2) prints `ACCEPTED` with the seed, the defect is fixed: stop and report (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. Doing nothing leaves X02 and X03 red whenever a batch has fetched and not yet admitted. The cause is in the test's fixture root, not in the writer.

1. **One function builds a fixture retrieval root, in one home.** Move `farm` out of `scripts/tests/test_run_pipeline_refusals.py` into a new support module `scripts/tests/_fixture_log.py` (the precedent for a support module there is `scripts/tests/_baseline_ddl.py`), as `fixture_log_root(dest, db_path, source=<repo>/retrieval-log)`: it creates `dest` and symlinks into it each folder of `source`, **except a folder whose `manifest.jsonl` names any `ref_id` above `dbcore.ref_id_high_water` of the database at `db_path`** (opened read-only). The id grammar is `dbcore._MINTABLE` (the pattern `ref_id_high_water` itself uses); do not write a second pattern. For each folder left out, print one line, `fixture root: left out <folder> (holds <ids>, above the copy's high-water mark <n>)`, so the exclusion is never silent. Return `dest`.
   **Chosen (authoring 2026-11-13): isolate the root, not change the id.** Rejected: (a) adding the retrieval log to `dbcore.ref_id_high_water`'s union. A pre-admission folder is filed under the id its source is *meant* to take; with the log in the union the real admission would take the next id instead and its saved bytes would sit under another source's id. The id rule is right for real admissions; only the fixtures must not share a pre-admission id. (b) a HAND row on the copy raising its high-water mark past every manifest id (a `source_locators` placeholder): every staged-lead case (I01 to I06) would see one more lead, and the copy would no longer be the canonical state the suite claims to test. (c) farming only tracked folders (`git ls-files`): a pre-admission folder committed before its data migration would still collide. Excluding by the copy's own high-water mark handles untracked and committed folders alike and goes away by itself when the batch's rows land.
2. **`test_run_pipeline_refusals.py` uses it.** `farm(name)` becomes a call of `fixture_log_root(os.path.join(TMP, name), DB)` (or is replaced by it at its two call sites: `FARM = farm("retrieval-log")` and `farm("farm-f")`). `dbcore` must be importable before the farm is built (put `scripts` on `sys.path` and import `dbcore` first); `retrieval_log` must still be imported **after** `GUIDEBOOK_RETRIEVAL_LOG` is set, because it reads that variable at import (`grep -n 'LOG_ROOT = Path(os.environ.get' scripts/research/retrieval_log.py`). `scratch()` copies whatever is under the current root, so it inherits the exclusion; leave it as it is. Keep the module docstring's paragraph about the scratch root true: it now says the farm leaves out a pre-admission folder, and why.
3. **`test_db_amend_writers.py` reads an isolated root too.** It sets no `GUIDEBOOK_RETRIEVAL_LOG` (`grep -c GUIDEBOOK_RETRIEVAL_LOG scripts/tests/test_db_amend_writers.py` prints 0), so it reads the repository's `retrieval-log/`, untracked folders included. Beside its `os.environ["GUIDEBOOK_DB_PATH"] = DB` line, set `os.environ["GUIDEBOOK_RETRIEVAL_LOG"] = fixture_log_root(<its temp dir>/"retrieval-log", DB)`. It writes nothing to the log (`grep -n -E 'record_file|fetch\(|manifest' scripts/tests/test_db_amend_writers.py` should show reads only; if it shows a write, stop: the root would then need copies, not symlinks).
   **Chosen (authoring 2026-11-13):** include this file although it is not red today: its verdict depends on the working tree and on the order its fixtures are minted, the same shape. Rejected: naming it only (the next re-ordering of its sections would make a case red for this reason with no task to point at).
4. **No other file.** `test_author_presence.py` and `test_scan_contract.py` already use an empty temporary root; leave them.

**What reads what this task adds:** the two test files (their fixture roots); `run_checks.py` through the registry entries `test_run_pipeline_refusals` and `test_db_amend_writers` (both advisory: `python3 -c "import yaml;[print(c['id'],c['level']) for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if c['id'] in ('test_run_pipeline_refusals','test_db_amend_writers')]"`). **What wrong thing reaches the plan without it:** a refusal suite whose result depends on an untracked folder. **What it makes deletable:** `farm` in `test_run_pipeline_refusals.py` (moved, not copied).

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`.

## 5. Caller sweep

Names to sweep: `farm(`, `FARM`, `GUIDEBOOK_RETRIEVAL_LOG`, `_fixture_log`.

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls `farm` or builds a fixture retrieval root; a test docstring or comment that says the scratch root holds every tracked session (it will now leave some out); a registry entry that runs one of these tests. A mention stays true. Fixing a caller is in scope (CLAUDE.md rule 4). Left out: `workplan/`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`, `retrieval-log/`.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
This task adds no verb, table, view or refusal text: `build_graph.py --check` is not needed.

## 6. Verification

**Step 1, before any edit: the before-run.**
```
CHECKS="test_run_pipeline_refusals test_db_amend_writers"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
grep -E '✗ (X02|X03)' "$SCRATCH/before-test_run_pipeline_refusals.txt"
```
Whether X02 and X03 are red here depends on section 3's command (1): red when it prints a folder, green otherwise. Record which.

**Step 2: red before, green after** (case `T073-01` in `scripts/tests/test_run_pipeline_refusals.py`, section A3, after X03; prefix free: `git grep -c 'T073-' scripts/tests/` prints nothing). Write it in two moves so that it is seen red:
- **Move 1:** add `fixture_log_root` with the `source` and `db_path` parameters and **without** the exclusion (every folder symlinked, as `farm` does today), switch both files to it, and add the case. Run the test: `T073-01` is red; nothing else changes against the before-run.
- **Move 2:** add the exclusion. `T073-01` is green.
- **`T073-01`** "a pre-admission folder holding the next id does not reach a fixture source". Inside `with scratch() as c:`: `nxt = dbcore.next_ref_id(c)`; build a source folder under `TMP` holding one session folder, `session_t073-preadmission`, whose manifest names `nxt` for a decodable text artefact (the `put` helper with `session=` writes exactly that shape, pointed at the source folder by `log_root`); build a root from it with `fixture_log_root(<dest>, os.environ["GUIDEBOOK_DB_PATH"], source=<that folder>)`; under `log_root(<that root>)` run X02's own statements (`new_source(verified=True)`, `put` of the undecodable PDF, `hand_scan`, then `ok(db.insert_extraction, …, dry_run=True, verbatim_exempt=…)`). Pass when the fixture took `nxt` **and** the exemption is accepted **and** the left-out line names the folder. Record red, saying which part failed, if the fixture did not take `nxt` (then the case proves nothing).
- **Seeded defect 1:** remove the exclusion again; `T073-01` goes red. Restore.
- **Seeded defect 2:** make the exclusion leave out every folder (compare against 0 instead of the high-water mark); expect a case that reads a tracked artefact to go red (X01, the derived-text refusal, is the first candidate): name which. Restore. This is what shows the exclusion is narrow.
- **No real folder is used.** Never create, move or edit a folder under the repository's `retrieval-log/` for any step of this task.

**Step 3: after-run.** The same loop with `after-`; compare failing lines check by check. X02 and X03 are green whether or not section 3's command (1) prints a folder; nothing green in the before-run is red.

**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run once, in the background. If T-075 is not yet merged, run `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` by hand and report it. `sha256sum data/guidebook.db` must not move.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: fixture sources never take an id a retrieval-log folder already holds [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the reproduction before and after; the folders the root left out; the two seeded defects; callers; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not change `dbcore.next_ref_id` or `dbcore.ref_id_high_water` (section 4 item 1, rejected (a)).
- Do not create, move, edit or delete anything under `retrieval-log/`, tracked or not, and do not commit an untracked folder you find there: another stream owns it.
- Do not write a HAND row to lift the copy's high-water mark.
- Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: section 3's reproduction (2) prints `ACCEPTED` with the seed (the defect is fixed); `test_db_amend_writers.py` writes to the retrieval log (item 3); a case other than X02, X03 and `T073-01` changes colour between the before- and after-runs; seeded defect 2 turns no case red (the suite cannot see an over-broad exclusion: report it, do not add a case for it here); `sha256sum data/guidebook.db` changes.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
