# T-069  Promote the adjudicated non-English observations to forms of their terms

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Every number in this file was read on 2026-11-13 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 (Opus-class, cluster B). Its evidence command was run read-only on 2026-11-13 and printed what section 3 states. **Partly held:** the observations whose source is outside the regulatory stratum wait on an owner question (section 2); the rest may proceed once the dependencies merge. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-069 |
| Title | Promote the adjudicated non-English observations to forms of their terms |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET: each form's alias type, and each adjudication of a phrase in Portuguese, Norwegian or Finnish, is a judgment of what the phrase names, read in its own language |
| Traces to | prior workplan D-4 (`grep -n '^| D-4 ' workplan/2026-10-23-pipeline-resolution-workplan.md`; the report: `sed -n '/^### D-4 aliases/,/^### D-5/p' scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md`); OR-17 (`grep -n -F 'OR-17: "Yes, bulk, with me reading the PR' references/project-standards.md`); OI-52 |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`.
- **Tasks that must be merged to the integration base first:** T-026 merged (the observation route of `add-alias` and the `attestation` column; merged as #226), T-028 merged (one row per occurrence: before it, a second observation of a form a term already holds in that language is refused, "a second occurrence waits for T-028's occurrence grain": `grep -n -F "waits for T-028's occurrence grain" scripts/db.py`). Check by running those tasks' own after-tests (their section 6), or `git log "$BASE" --oneline | grep -F 'task/t-028'`.
- **Owner decisions:** none in the register. The ruling is OR-17: the assistant approves vocabulary in bulk and the owner reads the pull request, on the owner's conditions that every phrase is "present in their prescribed jurisdiction/language" and that the model does not "generate its own phrases/names/aliases". **One open owner question holds part of this task:** OI-55 (6) in `OPEN-ITEMS-PLAN.md`, the reading of the 2026-11-06 answer E4 (`grep -n '^| E4 ' references/project-standards.md`): E4 makes a form vocabulary "only when an instrument in its language is read and the phrase is found there", and T-026's design counts a phrase found in another kind of source (`other_source`) as attested too (`grep -n -F "E4's own words make a seed vocabulary only" workplan/2026-11-12-bidirectional-pipeline/tasks/T-026-alias-attestation.md`). Until the owner answers it, **promote only observations whose source is in the regulatory stratum** (attestation `instrument`), and list the others (Co-1, grey, clinical sources) in the pull request as held on OI-55 (6). If the owner answers that `other_source` attests, promote those too, in this task if it is still open or in a follow-up batch.
- **Tests that must be red before you start:** the section 6 count of promoted forms is 0 for this batch's candidates.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-069-promote-adjudicated-observations "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>            # the session stem: bare in the database, with .md for emit_data_migration --session
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-069" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/t.db"   # s.db is the batch's working copy; t.db is for probes
```
- **Shell variables do not survive from one tool call to the next in this harness.** Write the stem down once and begin every later command block by setting `BASE`, `STEM` and `SCRATCH` again to the same values.
- **Real execution:** open with `/session-open`, then `/orient`. Follow `skills/run-pipeline_SKILL.md`. **Pilot or dry run:** skip `/session-open`, stay on the branch you were given, work on the scratch copy only, and stop before the write path.
- Work only on the scratch copy, pointing every call at it inline: `GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py <verb> ... --session "$STEM"`.
- Land the rows only by the write path, after the work is finished:
```
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH/s.db" --out "$SCRATCH/batch.sql"
python3 scripts/emit_data_migration.py --session "$STEM.md" --summary "<what the batch is>" --input "$SCRATCH/batch.sql"
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"      # must exit 0
```
Research batches are serial: if another research batch merged after you copied the database, `emit_batch_sql.py` refuses; start again from the new base.

## 3. The problem, in the guidebook's terms

Phrases that codes and papers in other languages actually use for our concepts have been read, quoted with their locator and judged to name a term we hold, but none is yet a form of that term. Searches in those languages still run on unattested words (no non-English form is attested today), which is the condition the owner's OR-17 forbids for vocabulary: the model's own phrases. The attested phrases are already in the database; they are one verb away from being the forms searches use.

**Evidence command** (read-only):

```
python3 -I - <<'PY'
import sqlite3; c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
LATEST = ("with latest as (select a.* from term_adjudications a where a.adjudication_id = "
          "(select max(adjudication_id) from term_adjudications b where b.observation_id = a.observation_id)) ")
print("non-EN observations by latest outcome:", c.execute(LATEST + "select coalesce(l.outcome,'UNADJUDICATED'), count(*) from observed_terms o left join latest l using(observation_id) where upper(o.language) <> 'EN' group by 1").fetchall())
rows = c.execute(LATEST + """select o.observation_id, upper(o.language), e.jurisdiction, l.term_id, e.tier, e.evidence_type,
  exists(select 1 from lang_jur_map m where m.language = upper(o.language) and m.jurisdiction = e.jurisdiction),
  exists(select 1 from term_aliases t where t.term_id = l.term_id and t.alias = o.surface_form and upper(t.language) = upper(o.language))
  from observed_terms o join latest l using(observation_id) join evidence_sources e on e.ref_id = o.ref_id
  where upper(o.language) <> 'EN' and l.outcome = 'NAMES-EXISTING' order by 1""").fetchall()
print("candidates (obs, lang, jur, term, tier, type, pair held, form held):"); [print(" ", r) for r in rows]
print("candidates already promoted:", c.execute("select count(*) from term_aliases where observation_id is not null").fetchone()[0])
print("observations with more than one adjudication:", c.execute("select observation_id from term_adjudications group by 1 having count(*) > 1").fetchall())
PY
```

**Expected output today** (2026-11-13): non-English observations by latest outcome, with NAMES-EXISTING the largest group (22) and a few UNADJUDICATED (4), DEFERRED (3), NAMES-NEW (2) and NOT-OURS (2); the candidate list, every candidate's pair held in `lang_jur_map` (so OR-17's jurisdiction-and-language condition can be met for each), most from codes and national frameworks, a few (7, 14 Co-1; 81, 85, 87 grey) from other sources, two whose text the term already holds as a legacy row (17, 81), and two pairs of observations of one text (75 and 89; 76 and 77); 0 already promoted; two observations adjudicated twice (88, 97). The latest adjudication of an observation is the one that governs (adjudications are appended, never edited).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. Every verb this task needs exists; it adds no code.

1. **Select by the latest adjudication.** The candidates are the rows of section 3's query, re-run on `$SCRATCH/s.db`. **Chosen (authoring 2026-11-13): the latest adjudication governs**, not any adjudication. Rejected: the writer's own test, which accepts an observation if *some* adjudication names the term (`grep -n -A4 'def _names_term' scripts/db.py`); an observation re-adjudicated NOT-OURS after an earlier NAMES-EXISTING would pass it. That is a writer defect reported to the coordinator, not patched here (rule 10).
2. **Stop on a candidate whose pair is not held.** If any candidate prints `0` in the "pair held" column, do not promote it: OR-17 requires the phrase to be present in its prescribed jurisdiction and language, and a pair `lang_jur_map` does not hold is not prescribed. List it.
3. **Promote, one call per candidate in the regulatory stratum:**
   ```
   GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py add-alias --term-id <term_id> --observation-id <id> --attestation instrument --alias-type <SYNONYM|NARROWER|BROADER> --session "$STEM"
   ```
   - The stratum is the writer's, derived from the tier ladder: `--attestation instrument` is refused for a source outside it, and that refusal is how you learn which candidates are held (item 4). Do not guess it from the tier column.
   - **The alias type is your judgment and carries its warrant:** read the observation's `context_quote` and the latest adjudication's `rationale`, and choose `SYNONYM` (the phrase names the same concept), `NARROWER` (a kind of it) or `BROADER`. Record the reason in the pull request, one line per candidate. Never `TRANSLATION` (refused: a source's own phrase is not a rendering of the English one, R11) and never `DEPRECATED`.
   - **Every refusal is recorded and left, never worked around.** Expected kinds: the quote is not in a file saved for its source (register the text and re-observe in a later batch); the held row is a legacy `TRANSLATION` type or carries another jurisdiction (observations 17 and 81 today: they wait for T-107, which types the legacy rows, `tasks/T-107-attest-forms.md` section 4 item 2 (c)); a second occurrence refused (if T-028 has merged this should not occur: stop and report).
4. **Held on OI-55 (6): candidates outside the regulatory stratum** (those `--attestation instrument` refuses). Do not call `add-alias` for them with `other_source`. List them in the pull request with observation, term, source and tier, and the question they wait on.
5. **Adjudicate the unadjudicated non-English observations** (the section 3 query's `UNADJUDICATED` group): read each in its own language and record `db.py adjudicate-term --observation-id N --outcome <NAMES-EXISTING|NOT-OURS|DEFERRED> [--term-id T] --rationale "<why, from the quote>" --session "$STEM"`. A NAMES-EXISTING outcome reached here is promoted by item 3 in the same batch. **Chosen: a phrase that names a concept we do not hold is not adjudicated NAMES-NEW here;** it is left unadjudicated and listed for T-072 (D-8), because NAMES-NEW needs a term and minting one is vocabulary seeding (OR-13), not promotion. Rejected: recording `DEFERRED` for it, which would say the source cannot settle it when it can. Leave the `DEFERRED` observations as they are: re-judging them needs evidence this batch does not read.
6. **Never type a phrase.** Every form comes from an observation's `surface_form` through the observation route; no `--alias` is written by hand (OR-17: "It is not acceptable for the model to generate its own phrases/names/aliases").

**What reads what this task adds or changes:** `log-search --form-id` (searches in these languages fire attested forms); `alias_provenance_audit.py` (its `attested` column); T-057's coverage view (a form present, with locator); T-107 (which attests further occurrences from instruments and types the legacy rows this task leaves).

**How this task sits beside T-107 and T-112** (the coordinator asked for the placement). T-107 reads instruments anew and writes the forms it finds there (base route) or from fresh observations; it also types legacy rows. This task writes nothing from a new reading: it promotes judgments already in the database. The two use the same verb and do not overlap in rows; either may land first (two research batches never run at once). T-112 translates held claim text for display and writes no form (its section 4 item 2: "Do not translate a term into a new term"); it does not touch this task's rows.

**Data migration.** This task lands rows through `scripts/emit_data_migration.py`, which names the file itself; never type a migration name or number. The pull request contains no schema migration and no file under `scripts/` other than that one `scripts/migrations/data_*` file.

## 5. Caller sweep

A research task renames nothing and changes no code, so the sweep that applies is the one for prose that restates a fact your rows change (CLAUDE.md rule 7a): for each term whose forms you add, search the reading surface and correct a sentence your rows make false, or stop if correcting it is not research:

```
V='<the term id or phrase>'
git grep -n -F -e "$V" -- governance architecture CLAUDE.md references skills ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
A sentence that says no non-English form is attested is a caller. Structures this task touches: `term_aliases`, `term_adjudications`. The ledger, `sessions/` and committed migrations are records and are never edited.

## 6. Verification

**Red before, green after.** Before: the "candidates already promoted" line of section 3 prints 0. After (on the migrated database): every candidate promoted by item 3 is a `term_aliases` row with its `observation_id` and `attestation = 'instrument'`:
```
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select attestation, count(*) from term_aliases where observation_id is not null and coalesce(updated_by_session, created_by_session)=? group by 1\",(sys.argv[1],)).fetchall())" "$STEM"
```
prints only `instrument` rows, their number equal to the candidates promoted (derive it from your call log, never type it), and `python3 scripts/audit/alias_provenance_audit.py` shows an `attested` figure above 0 for each language promoted. The pull request lists, by command output, every candidate with its outcome: promoted, refused (with the refusal text), or held (OI-55 (6)); and every adjudication written.

**Fixtures.** Probes run on `$SCRATCH/t.db`; the batch's rows are written on `$SCRATCH/s.db` and reach `data/guidebook.db` only through the write path.

**The gates, once each:**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- Run each once, after the migration is applied and before the commit; never `--all`.
- **Proof that each gate examined something:** for each table this task writes (`term_aliases`, `term_adjudications`), the count of rows with `created_by_session = "$STEM"` or `updated_by_session = "$STEM"` is above 0 after the migration. `research_dod_session` is red by construction on a batch that searches and admits nothing (OI-55 (1)): report its lines, and say so, rather than adding a search to satisfy it. `migration_reproducibility` compares row counts only, so an UPDATE (a promoted seed) is invisible to it: also run `python3 scripts/audit/migration_reproducibility.py --deep`.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "run-pipeline: promote adjudicated non-English observations to attested forms (D-4) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the candidates and their outcomes, by command output; the held list and the question it waits on>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly. Rows land only by the write path.
- Do not type a phrase, an alias or a translation. Do not use `TRANSLATION`. Do not write a seed (`--seed`).
- Do not promote a candidate outside the regulatory stratum while OI-55 (6) is unanswered; do not mint a term (NAMES-NEW) in this batch.
- Do not put tooling in this pull request (CLAUDE.md rule 10). The `_names_term` defect is reported, not fixed here.
- Do not decide doctrine. Do not treat any `[A-Z]-NN` code as a container. Do not run `run_checks.py --all`, `bootstrap.sh`, or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push. Do not subscribe to pull-request activity.
- Do not hand-type a count into any file or message; write the command that computes it.

## 9. Stop conditions

Stop and report when: a precondition is not met; the section 3 output differs in shape (no NAMES-EXISTING candidates, or some already promoted); a candidate's pair is not held; a second-occurrence refusal appears after T-028 has merged; a refusal you would have to work around to proceed; the owner answers OI-55 (6) in a form this file does not foresee; you would have to guess a value, a term, a name or an owner's intent.

## 10. Rollback

Before the migration is applied: delete the scratch copy. After it is committed: a data migration is immutable; correct a wrong row with a compensating migration written through the same verbs.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once, recorded with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`; `/batch-done`; push; open the pull request last, once, for the owner to read (OR-17: "with me reading the PR"), listing every promoted form with its quote, locator and source; call `unsubscribe_pr_activity` at once; push nothing afterwards except a deliberate change.
