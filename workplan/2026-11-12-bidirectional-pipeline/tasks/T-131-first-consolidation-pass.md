# T-131  The first consolidation pass over the base: every candidate pair judged, merged, related or kept apart, with its warrant

_One task, one pull request (since the owner's instruction of 2026-11-15, one task of a stacked pull request: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Why this task exists, and the adjudication that chose its shape over the alternatives: `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md`. Every number in this file was read on 2026-11-17 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-17 by the Opus-class adjudicator of the owner's propagation and consolidation questions; its evidence command was run read-only on 2026-11-17 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-131 |
| Title | The first consolidation pass over the base: every candidate pair judged, merged, related or kept apart, with its warrant |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET: Opus-class. Each verdict is a judgment of what a phrase names, read in its own language |
| Traces to | the owner's questions Q2 and Q3 of 2026-11-16; the adjudication `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md` (G1); `tasks/T-129-design.md` sections B4 and B5 |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`; otherwise the remote branch that carries the newest commit to this folder. Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`.
- **Tasks that must be merged to the integration base first:** T-130, T-069 merged (T-130 gives the proposer and the bound; T-069 promotes the adjudicated non-English observations to attested forms, which is what gives reasons R1 and R2 something to compare across the held languages). Check by running those tasks' own after-tests (their section 6).
- **Owner decisions:** none in the register. A pair either of whose terms has a domain in `dbcore.NON_QUANTITY_DOMAINS` is not merged here: it is listed for the owner in the pull request (design B5).
- **Tests that must be red before you start:** `python3 scripts/db.py consolidation-candidates` on the base prints a `CANDIDATES:` line above 0 (if it prints 0, there is nothing to judge: stop and report that, which is a result).
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-131-first-consolidation-pass "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>            # the session stem: bare in the database, with .md for emit_data_migration --session
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-131" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/t.db"   # s.db is the batch's working copy; t.db is for probes
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

The base holds concepts that may be one under two names, and forms that two concepts share (T-130's evidence command lists them). Until each pair is judged, a figure may be filed under either, and a determination for one rests on half the evidence while the book prints two topics for one thing. Some shared forms are homonyms (one phrase naming two different quantities in a language): those are recorded as two concepts, not merged.

**Evidence command** (read-only):

```
python3 scripts/db.py consolidation-candidates --pass 1
python3 -c "import yaml;print(yaml.safe_load(open('governance/pipeline-contract.yaml'))['consolidation'])"
```

**Expected output today:** one line per (pair, reason) with its evidence rows, then `EXAMINED:` and `CANDIDATES:` lines (counts computed); the contract's bound.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

1. **Pass by pass, to the bound.** On the scratch copy `$SCRATCH/s.db`: run `consolidation-candidates --pass 1`, judge every line, run `--pass 2`, and so on; stop when a pass prints `CANDIDATES: 0`, or after the pass whose number is the contract's `max_passes` (design B4). Keep each pass's output in `$SCRATCH/pass-<n>.txt`.
2. **The verdict for each line** (design B5), each written through `db.py` with `--session "$STEM"`:
   - one concept: `merge-term --from <id> --into <id> --reason "<what in the evidence rows shows they are one, in the phrase's own language>" --candidate-reason <R1..R4>`; direction as design B5 says;
   - related but not one: T-029's writer, with the kind (broader, part of, adjacent, element has parameter, element has provision) and its warrant;
   - two concepts (a homonym, or a near name for another thing): T-029's writer with kind `distinct` and its warrant;
   - cannot tell from what is held: leave it; it is listed again and ends in the pull request's list of unjudged pairs, with what would decide it (a form to attest, a translation to review).
3. **Never merged here:** a pair marked `owner` by the verb (`NON_QUANTITY_DOMAINS`); a pair whose survivor would carry two active parameters (run `merge-parameter` only if the two parameters are one quantity, which is a judgment you state, and before `merge-term`); never re-point, UPDATE or copy a row.
4. Land the rows by the write path of section 2.

**What reads what this task writes:** `v_term_survivor` and every concept reader through it (the screens, `v_term_names`, the base coverage view), so the next minting and the next coverage read see one concept; `consolidation-candidates` (a judged pair is not proposed again until the base grows under it); the owner, in the pull request.

## 5. Caller sweep

A research task renames nothing and changes no code. For each merged pair, search the reading surface for prose that names the folded term as a concept of its own, and correct a sentence your rows make false, or stop if correcting it is not research:

```
V='<the folded term id or label>'
git grep -n -F -e "$V" -- governance architecture CLAUDE.md references skills ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
Structures this task writes: `term_merges`, T-029's relation table. The ledger, `sessions/` and committed migrations are records and are never edited.

## 6. Verification

**Red before, green after.** Before: section 2's `CANDIDATES:` line is above 0. After (on the migrated database): `python3 scripts/db.py consolidation-candidates` prints `CANDIDATES:` equal to the pairs left unjudged or marked `owner` (derive it from your pass files, never type it), and `python3 scripts/audit/term_merge_integrity.py` passes with `EXAMINED:` equal to the merges this batch wrote: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select count(*) from term_merges where created_by_session=?',('<STEM>',)).fetchone())"`.

**The gates, once each:**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run each once, after the migration is applied and before the commit; never `--all`. `migration_reproducibility` compares row counts only: also run `python3 scripts/audit/migration_reproducibility.py --deep`. A batch that searches and admits nothing is red on `research_dod_session` by construction (OI-55 (1)): report its lines rather than adding a search to satisfy it.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "run-pipeline: first consolidation pass: candidate pairs judged, merged, related or kept apart [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: every candidate and its verdict, by command output; what was left and why>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly. Rows land only by the write path.
- Do not merge a pair marked `owner`; do not judge a pair from its English labels alone when its evidence rows are in another language: read the forms.
- Do not mint a term, write a form, a seed or a translation in this batch: the sweep judges what is held (design B4: no form is added within a sweep).
- Do not put tooling in this pull request (CLAUDE.md rule 10), and do not change the registry level of `term_merge_integrity` here: its ratchet is T-132's.
- Do not decide doctrine. Do not treat any `[A-Z]-NN` code as a container. Do not run `run_checks.py --all`, `bootstrap.sh`, or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push. Do not subscribe to pull-request activity.
- Do not hand-type a count into any file or message; write the command that computes it.

## 9. Stop conditions

Stop and report when: a precondition is not met; the verb's output differs in shape from design B1; a writer refuses a verdict you would have to work around; a pair would need a merge of two active parameters whose quantities you cannot show are one; a pair's evidence is in a language you cannot read with confidence (leave it, listed); you would have to guess a value, a term, a name or an owner's intent.

## 10. Rollback

Before the migration is applied: delete the scratch copy. After it is committed: a data migration is immutable; undo a wrong merge with `unmerge-term` (its reason stated) and a wrong relation by retiring it, in a compensating batch through the same verbs.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once, recorded with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`; `/batch-done`; push; open the pull request last, once, listing every candidate with its verdict, reason code and evidence rows, the pairs left unjudged with what would decide each, and the pairs marked `owner` as questions for the owner in plain words; call `unsubscribe_pr_activity` at once; push nothing afterwards except a deliberate change. Its ratchet to blocking is T-132's (a tooling pull request, rule 10).

**Amended 2026-11-19 (ledger: Owner ratification 2026-11-19; adjudication item 11; T-142).** In "What reads what this task writes", `v_term_names` is retired by T-142 (`tasks/T-142-displayed-name-rule.md` section 4 item 7); the concept reader in its place is `term_names` in `scripts/db.py` (`db.py term-names` prints it), and a merge direction taken from `label_is_attested_form` reads that function's field.
