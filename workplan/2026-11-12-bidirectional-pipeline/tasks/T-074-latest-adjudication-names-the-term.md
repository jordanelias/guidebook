# T-074  An alias or a rename rests on the latest adjudication of its observation

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-57, item (6) (`grep -n -F '(6) `db._names_term`' workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md`), found by the author of T-069 (`grep -n -F 'Chosen (authoring 2026-11-13): the latest adjudication governs' workplan/2026-11-12-bidirectional-pipeline/tasks/T-069-promote-adjudicated-observations.md`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 (Opus-class plan integrator). The defect was reproduced on a scratch copy (section 3); no fix was prototyped. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-074 |
| Title | An alias or a rename rests on the latest adjudication of its observation |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | OI-57 item (6); T-069 (research: promotes adjudicated observations to forms of their terms through `add-alias`, and selects by the latest adjudication); `db.adjudicate_term`'s docstring ("Divergent adjudications are DELIBERATELY permitted") |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** none. Check by running: nothing to check. (T-069 should run after this task; that edge belongs to T-069's file, not to this one.)
- **Owner decisions:** none.
- **Tests that must be red before you start:** the new cases `T074-01`, `T074-02` and `T074-04` (section 6) are red on the unchanged code; `T074-03` is green before and after.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-074-latest-adjudication-names-the-term "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task has no migration
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-074" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

An alias says that the phrase a source uses names one of our concepts; a rename takes a concept's name from such a phrase. Both rest on a judgment, an adjudication of the observation that records the phrase. Adjudications are appended, never edited: a second one that disagrees lands as a second row (`db.adjudicate_term`). `db._names_term`, which `add-alias` (the observation route) and `rename-term --from-observation` call, asks whether **any** adjudication of the observation names the term. An observation first judged to name a term and later judged NOT-OURS (or re-pointed at another term) still passes, so a phrase the project has since decided is not ours can become a form of the concept, or its name. What reaches the guidebook: a term shown under a name or alias its own latest judgment rejects.

**Evidence commands** (read-only on the repository; the probe writes only to a scratch copy):

```
grep -n -A5 'def _names_term' scripts/db.py
git grep -n '_names_term(' -- scripts
python3 -I - <<'PY'
import sqlite3
c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
LATEST = ("with latest as (select a.* from term_adjudications a where a.adjudication_id = "
          "(select max(b.adjudication_id) from term_adjudications b where b.observation_id = a.observation_id)) ")
print('observations adjudicated more than once:', c.execute("select observation_id, count(*) from term_adjudications group by 1 having count(*) > 1 order by 1").fetchall())
print('pairs some adjudication names but the latest does not:', c.execute(LATEST + "select distinct a.observation_id, a.term_id from term_adjudications a join latest l using(observation_id) where a.term_id is not null and l.term_id is not a.term_id").fetchall())
PY
cp data/guidebook.db "$SCRATCH/p.db"; mkdir -p "$SCRATCH/emptylog"
GUIDEBOOK_DB_PATH="$SCRATCH/p.db" GUIDEBOOK_RETRIEVAL_LOG="$SCRATCH/emptylog" python3 -I - <<'PY'
import os, sqlite3, sys
sys.path[:0] = ['scripts', 'scripts/research', '.']
import db
c = sqlite3.connect(os.environ['GUIDEBOOK_DB_PATH'])
obs = c.execute("select observation_id from observed_terms o where not exists (select 1 from term_adjudications a where a.observation_id = o.observation_id) order by 1 limit 1").fetchone()[0]
term = c.execute("select term_id from terms order by term_id limit 1").fetchone()[0]
db.adjudicate_term(obs, 'NAMES-EXISTING', 'probe: names it', session='session_t074-probe', term_id=term)
db.adjudicate_term(obs, 'NOT-OURS', 'probe: on re-reading, not ours', session='session_t074-probe')
c = sqlite3.connect(os.environ['GUIDEBOOK_DB_PATH'])
print('probe', obs, term, '_names_term ->', db._names_term(c, obs, term), '| latest outcome:', c.execute("select outcome from term_adjudications where observation_id = ? order by adjudication_id desc limit 1", (obs,)).fetchone()[0])
PY
rm -rf "$SCRATCH/p.db" "$SCRATCH/emptylog"
```

**Expected output** (2026-11-13): the function is a single `SELECT 1 … WHERE observation_id = ? AND term_id = ?`; it has two callers, `rename_term` and `add_alias`. Two observations are adjudicated twice, 88 (DEFERRED, then NAMES-EXISTING) and 97 (DEFERRED twice); **no** live pair is named by an earlier adjudication and not by the latest, so the fix changes no present act. The probe prints `_names_term -> True | latest outcome: NOT-OURS` (and `adjudicate_term`'s own `NOTE: … Writing a second row` line on stderr): the defect.

If the probe prints `False`, the defect is fixed: stop and report (section 9). If the second query prints a pair, the fix changes a present act: list the pair in the pull request and stop before merging (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. Doing nothing leaves a write path that ignores the project's own later judgment. The change is one query and two messages.

1. **`_names_term`, in `scripts/db.py`:** ask the question of the latest adjudication only.
   ```python
   def _names_term(conn, observation_id: int, term_id: str) -> bool:
       """Does the LATEST adjudication of this observation name this term?

       Adjudications are appended, never edited (adjudicate_term: a disagreeing judgment is a second
       row), so the latest one is the observation's standing judgment; an earlier one that named the
       term and was later declined or re-pointed warrants nothing. Latest = highest adjudication_id
       (the order the writer assigns; created_at is minute-resolution and can tie)."""
       row = conn.execute(
           "SELECT term_id FROM term_adjudications WHERE observation_id = ? "
           "ORDER BY adjudication_id DESC LIMIT 1", (observation_id,)).fetchone()
       return row is not None and row[0] == term_id
   ```
   **Chosen (authoring 2026-11-13): the latest adjudication governs.** It is what both refusals already tell the operator to do ("adjudicate-term … first": a new row is the remedy, so the newest row must be the one that counts), and what T-069 selects by. Rejected: refusing while the observation's adjudications disagree (a "contest" reading of `adjudicate_term`'s docstring). That reading would refuse observation 88 (DEFERRED, then NAMES-EXISTING), where nothing is contested, and it decides a question the docstring does not raise: the docstring permits a second row, it does not say the first one still warrants a write. **Chosen:** order by `adjudication_id`, not `created_at` (minute resolution: two adjudications in one minute tie).
2. **The two refusals that call it** (`grep -n -F 'no adjudication of observation' scripts/db.py` finds both): they say "no adjudication of observation N names T", which is false when an earlier one does. Make each say `the latest adjudication of observation N does not name T (none does, or a later one declined it or named another term)`, keeping the rest of each message (the remedy command) as it is. The prefix (`rename-term:` and `add-alias:`) stays.
3. **No other reader changes.** `research_batch_dod.py` R16-adjudicate deliberately counts any adjudication ("Any row answers it": `grep -n -F 'Any row answers it' scripts/audit/research_batch_dod.py`): whether an observation has been judged at all is a different question. The promotion check in `db.py` (`grep -n -F "ORDER BY adjudication_id LIMIT 1\", [term_id]" scripts/db.py`) asks of a term, not of an observation: a mention. Say so in the pull request.

**What reads what this task changes:** `add-alias` (observation route) and `rename-term --from-observation`; T-069 (research) writes aliases through the first. **What wrong thing reaches the guidebook without it:** an alias or a canonical name taken from a phrase the project's latest judgment declined. **What it makes deletable:** nothing.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`.

## 5. Caller sweep

Names to sweep: `_names_term`, `no adjudication of observation`, `term_adjudications`.

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls `_names_term`; a test that asserts one of the two messages' old wording (`AL02` and `N04` in `scripts/tests/test_scan_contract.py` assert only the needle `adjudicat`, which stays true: confirm); a skill or governance sentence saying an alias needs "an adjudication" naming the term (true but now incomplete: make it "the latest adjudication" where it states the rule); a view or trigger over `term_adjudications` (none on 2026-11-13: the `sqlite_master` line below). A mention stays true. Fixing a caller is in scope (CLAUDE.md rule 4). Left out: `workplan/` except `workplan/pipeline-state-graph/machines.yaml`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where type in (\"view\",\"trigger\") and sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
This task changes the text of two refusals: run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference (only a failure count above the before-run is yours).

## 6. Verification

**Step 1, before any edit: the before-run.**
```
CHECKS="test_scan_contract test_run_pipeline_refusals test_db_amend_writers"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
`test_scan_contract` failed G01 and G02 on 2026-11-12, and `test_run_pipeline_refusals` X02 and X03 on 2026-11-13 (T-073's): record and carry on.

**Step 2: red before, green after** (cases `T074-01` to `T074-04` in `scripts/tests/test_scan_contract.py`, directly after the add-alias cases `AL01`…; prefix free: `git grep -c 'T074-' scripts/tests/` prints nothing). Terms: three entries of the file's own `FREE` list that no other case uses, `FREE[27:30]` (check: `grep -o 'FREE\[[0-9:]*\]' scripts/tests/test_scan_contract.py | sort -u` shows no index at or above 27; if `len(FREE) < 30`, print `SKIPPED-NO-FIXTURE` for the four cases, as the T026 repair cases do). Observations: new ones made the way `OCW` is made (`attempt(observe, obs("door leaf", "PDF page 1 / T074a", "the clear width of a door leaf is measured here"), S)`, with a distinct locator suffix per observation, as T026-11 does), so their quote verifies against the fixture text. Adjudications through `adj` (`db.adjudicate_term`), never by SQL.
- `T074-01` an observation adjudicated NAMES-EXISTING to term X and then NOT-OURS: `add_alias(X, obs, "SYNONYM", S)` is refused, the message holds `latest adjudication`, and `term_aliases` gains no row. **Red before** (the old function accepts and writes the alias).
- `T074-02` the same observation: `rename_term(X, "door leaf", "fixture", S, from_observation=obs)` is refused with `latest adjudication`. **Red before.**
- `T074-03` positive control, the live shape of observation 88: an observation adjudicated DEFERRED and then NAMES-EXISTING to term Y: `add_alias(Y, obs, "SYNONYM", S)` is accepted. Green before and after.
- `T074-04` an observation adjudicated NAMES-EXISTING to Y and then NAMES-EXISTING to Z: an alias to Y is refused (**red before**), and an alias to Z is accepted.
- Seeded defect 1: order `ASC` instead of `DESC`; `T074-01` (earliest names X) and `T074-03` (earliest is DEFERRED) go red. Restore.
- Seeded defect 2: restore the old any-row query; `T074-01`, `T074-02` and `T074-04` go red. Restore.

**Fixtures** go to the copy the test makes, are labelled with the test's own session, and never reach `data/guidebook.db`.

**Step 3: after-run.** The same loop with `after-`; compare failing lines check by check; nothing new may fail. `AL02` and `N04` still pass (they assert the needle `adjudicat`).

**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run once, in the background. If T-075 is not yet merged, run `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` by hand and report it. `sha256sum data/guidebook.db` must not move.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: an alias or a rename rests on the latest adjudication of its observation [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the probe before and after; the live pairs query; the two messages; callers; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not add a uniqueness constraint or a refusal on a second adjudication: divergent adjudications are permitted by design (`adjudicate_term`'s docstring; CLAUDE.md §4 names the same mechanic for `add-population-match` as a refusal that must stay absent).
- Do not change `research_batch_dod.py`'s R16-adjudicate reading (section 4 item 3).
- Do not adjudicate, alias or rename anything on the canonical database (T-069's, research).
- Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: the probe of section 3 prints `False` (the defect is fixed); section 3's second query prints a live pair (the fix would change a present act: list it, and ask the coordinator before merging); `FREE` has fewer than 30 entries and the cases cannot run; a check green before is red after; `sha256sum data/guidebook.db` changes.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
