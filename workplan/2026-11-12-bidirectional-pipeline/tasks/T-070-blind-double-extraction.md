# T-070  Blind double extraction: do two readers, and do model and effort, record the same rows?

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Every number in this file was read on 2026-11-13 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 (Opus-class, cluster B). Its evidence command was run read-only on 2026-11-13 and printed what section 3 states. **HELD on owner question Q-T070 (the second test source; section 2), and it needs an owner act (launching the rater sessions).** Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-070 |
| Title | Blind double extraction: do two readers, and do model and effort, record the same rows? |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 (a measurement of Layer 3; it writes no row into `data/guidebook.db`) |
| Kind | **RESEARCH** (a measurement: no row is emitted, no migration is written, and no file under `scripts/` changes; CLAUDE.md rule 10) |
| Executor | NOT FOR SONNET: this task's executor is the coordinator of the measurement, who writes the raters' brief, checks their blindness and interprets the agreement; the raters themselves are an Opus-class and a Sonnet-class session by design |
| Traces to | prior workplan D-5 (`grep -n '^| D-5 ' workplan/2026-10-23-pipeline-resolution-workplan.md`; the report: `sed -n '/^### D-5 inter-rater/,/^### D-6/p' scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md`); OR-15 (`grep -n -F "OR-15: \"Yes, use batch 23's material\"" references/project-standards.md`); OR-18 (`grep -n -F 'OR-18: "Transcripts suffice"' references/project-standards.md`); the owner's battery question "Do model and effort change what is recorded" (`grep -n -F 'Do model and effort change what is recorded' workplan/2026-10-23-pipeline-resolution-workplan.md`); OI-52 |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`).
- **Tasks that must be merged to the integration base first:** T-016 (the writer's reading refusals, so every rater meets the same refusals; merged as #227). Check with `git log "$BASE" --oneline | grep -F 'task/t-016-wp-t1a-reading'`. The measurement compares the raters with each other, not with the corpus, so it does not wait for the full reading of held sources; it needs only the two sources' derived full text (section 4 item 1).
- **Owner decisions:** OD-44 (registered 2026-11-13, not yet asked; this file's Q-T070, below). Rulings: OR-15 (batch 23's material) and OR-18 (the transcripts are the model and effort telemetry). **One owner question, raised by this authoring and not yet asked, holds the task:**
  - **Q-T070: which second source?** OR-15 answered "Yes, use batch 23's material" to a prompt that described that material as "one code with a step table and one T1 paper with findings" (`grep -n -F 'one code with a step table and one T1 paper with findings' governance/owner-browser.yaml`). Batch 23 admitted no T1 source and holds no T1 or T2 figure: its sources are tiers 3, 5 and 6 only (section 3). The code half exists; the T1 half does not. The second source is there because "a code converges trivially" (the report). Options: **(a)** the T1 or T2 source with the most `finding` rows in the whole corpus, chosen by the report's own query (section 3 prints it), though it is not batch 23's; on 2026-11-13 that source had no saved PDF or HTML (`python3 scripts/research/full_text.py --ref-id <it> --session probe --dry-run` printed "NOTHING TO DERIVE"), so (a) also needs the document retrieved first (R10); **(b)** batch 23's non-code source with the most rows of its own (a grey report or a national framework), keeping to batch 23 but losing the T1 test; **(c)** the owner names one. Until a ledger line in the owner's words answers, do not launch raters.
- **An owner act:** the raters are separate harness sessions that **the owner launches**, each with its model and effort named (the report's design, which OR-15 accepted as "D-5 as written"). This task writes their brief and waits for them.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-070-blind-double-extraction "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-070" && mkdir -p "$SCRATCH"
sha256sum data/guidebook.db | tee "$SCRATCH-canonical.sha"   # the sha every rater copies from; it must not move during the measurement
```
- **Shell variables do not survive between tool calls.** Set `BASE`, `STEM` and `SCRATCH` again at the top of every block.
- **Real execution:** `/session-open`, then `/orient`. **Pilot or dry run:** do not launch raters; stop after item 2 of section 4 (the brief), and say it was a pilot.

## 3. The problem, in the guidebook's terms

The guidebook's figures are read out of sources by a model. Whether a second reader, blind to the first, would record the same figures with the same role, comparator and unit has never been measured, and neither has whether a cheaper model or a lower effort records fewer or different rows. A reader of the book cannot be told how far an extraction is the source and how far it is the reader.

**Evidence command** (read-only):

```
python3 -I - <<'PY'
import sqlite3; c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
B = 'session_2026-10-01-research-batch-23'
print("batch 23 sources by tier:", c.execute("select tier, evidence_type, count(*) from evidence_sources where created_by_session=? group by 1,2", (B,)).fetchall())
print("material (a), batch 23's code with the most condition rows:", c.execute("select x.ref_id, sum(x.figure_role='condition'), count(*) from source_value_extractions x join evidence_sources e using(ref_id) where e.tier=6 and e.created_by_session=? group by 1 order by 2 desc, 3 desc, 1 limit 1", (B,)).fetchall())
print("T1/T2 source with the most finding rows, corpus-wide:", c.execute("select x.ref_id, e.tier, e.created_by_session, count(*) from source_value_extractions x join evidence_sources e using(ref_id) where e.tier in (1,2) and x.figure_role='finding' group by 1 order by 4 desc, 1 limit 1").fetchall())
print("batch 23 non-code source with the most rows:", c.execute("select x.ref_id, e.tier, e.evidence_type, count(*) from source_value_extractions x join evidence_sources e using(ref_id) where e.created_by_session=? and e.tier<6 group by 1 order by 4 desc, 1 limit 1", (B,)).fetchall())
PY
grep -c '"effort"' "$(ls -d transcripts/harness_* | head -1)/main.jsonl"
```

**Expected output today** (2026-11-13): batch 23's sources at tiers 3, 5 and 6 only (grey, national framework, code), no tier 1 or 2; a code (REF-01031 on 2026-11-13); a T1 source from another session (REF-01033, admitted by the 2026-10-30 ramp session); a batch-23 national framework (REF-01030); and a non-zero count of `"effort"` fields in a preserved transcript (so OR-18's telemetry can be read). `full_text.py --dry-run` exited 0 for the code and for the batch-23 national framework, and 1 for the corpus-wide T1 source (no saved document).

## 4. The change

Order of preference, from CLAUDE.md §8. Nothing in `scripts/` is added: the scoring is a measurement, run once, and its script lives with its report.

1. **The two sources and their text.** Source A is the code of section 3 (chosen by query, never typed). Source B is the owner's answer to Q-T070, chosen by its query. For each, `python3 scripts/research/full_text.py --ref-id <R> --session "$STEM" --dry-run` must exit 0 (the bytes are held and the text derivable); if not, stop: a rater cannot be blind and complete over text it cannot read. Then run it without `--dry-run`, so both raters read the same derived text.
2. **The raters' brief**, written to `scratchpad/$STEM/RATER-BRIEF.md` and committed: read `CLAUDE.md`; copy `data/guidebook.db` from the commit named by `$STEM`'s branch (its sha recorded in the brief) to a scratch path; for the two `ref_id`s only, read the derived text from start to end and record every figure, condition and finding with `db.py add-extraction` (and `relate-extraction` for a condition) on that copy, against every active parameter; **do not query `source_value_extractions`, `extraction_relations` or `observed_terms` for those `ref_id`s, and do not open any earlier session's notes on them**; when finished, `python3 scripts/research/emit_batch_sql.py --scratch <copy> --out scratchpad/<rater stem>/rater.sql`, `python3 scripts/preserve_transcripts.py`, commit both to the rater's own branch `task/t-070-rater-<A|B|C>`, push it, and open no pull request.
3. **The raters** (launched by the owner): A, an Opus-class session; B, a Sonnet-class session at the same effort as A; C, A's model at a different effort. Each is told the brief's path and nothing about the sources' existing rows.
4. **Blindness, checked from each rater's transcript** (OR-18: the transcripts are the record). For each rater's harness folder: no tool call whose input names one of the two `ref_id`s together with `source_value_extractions`, `extraction_relations` or `observed_terms` before that rater's first `add-extraction`. A rater that looked is excluded and named; it is not re-run silently.
5. **The scoring script**, `scratchpad/$STEM/inter_rater.py`, run with `python3 -I`. **Chosen (authoring 2026-11-13): a scratchpad script, not `scripts/`.** Rejected: a registered tool under `scripts/audit/`, which would be tooling with one run and no further reader (CLAUDE.md §8), and would need its own tooling pull request (rule 10). The script:
   - builds one copy of the canonical database per rater and applies that rater's `rater.sql` to it (the copies stay under `$SCRATCH`; the canonical database is never written);
   - **match key** (`ref_id`, `parameter_id`, `figure_role`, the claim text normalised by `dbcore`'s own normaliser if it has one, else whitespace-folded and case-folded, said in the report); a second pass keys on the locator columns (`loc_*`) in place of the text;
   - **coverage**: matched keys over the union of keys, per rater pair;
   - **field agreement** on matched keys: `claim_type`, `comparator`, the bound (read with `dbcore.bound_on_scale`, never re-implemented), `claimed_unit`, and the set of `condition_on` targets;
   - **Cohen's kappa for `figure_role`**, over rows matched on (`ref_id`, `parameter_id`, normalised text) alone: a key that includes the role would force agreement;
   - **telemetry per rater from its transcript** (OR-18): the `model` and `effort` fields, the sum of `output_tokens`, the count of tool calls, the wall time from first to last timestamp;
   - prints `EXAMINED: <rows compared>` and writes `scratchpad/$STEM/inter-rater-report.md`, each figure beside the command or query that produced it (rule 7a). No figure is typed into the report.
6. **The rows are measurement, not corpus.** Nothing from the raters is emitted to `scripts/migrations/`. If the owner later adopts one rater's reconciled rows, that is an ordinary research batch through the write path, not this task.

**What reads what this task adds:** the owner (the battery question above); T-105 and every later reading batch (the agreement figures say which fields need a second reader); the run-pipeline skill's choice of model for extraction, if the owner decides on it.

**What wrong thing reaches the guidebook without it:** figures whose reading depends on the reader are presented as the source's, with no measure of how much.

## 5. Caller sweep

A measurement renames nothing and changes no code or row. The sweep for prose (rule 7a): if the report contradicts a sentence that states how reliable extraction is or which model extracts, list that sentence in the pull request for the owner; do not edit doctrine.
```
git grep -n -i -e 'inter-rater' -e 'double extraction' -e 'second extractor' -- governance architecture skills references ':(exclude)references/project-standards.md'
```

## 6. Verification

- **Red before:** `ls scratchpad/*/inter-rater-report.md` finds nothing. **Green after:** the report exists, was written by the script, prints `EXAMINED:` above 0, and every figure in it sits beside its command.
- **The script can fail:** before scoring the real raters, run it on two copies where one has a row deleted and one row's `comparator` changed (`TASK-FIXTURE`, on `$SCRATCH` copies only): coverage drops below 1 and the comparator agreement drops below 1. Show the output.
- **The canonical database did not move:** `sha256sum -c "$SCRATCH-canonical.sha"` prints OK at the end.
- **The gate, once:** `scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1` and `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`; the diff holds only `scratchpad/` files and transcripts.

## 7. Commit

```
git add scratchpad/"$STEM" transcripts
git commit -m "run-pipeline: blind double extraction measured on two sources (D-5) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the sources and their queries, the raters (model, effort), the blindness check, the agreement figures by command>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not launch raters while Q-T070 is unanswered, and do not launch them yourself in place of the owner.
- Do not emit, migrate or apply any rater's rows to `data/guidebook.db`. Do not write `data/guidebook.db` at all.
- Do not tell a rater what the corpus already holds for its sources. Do not re-run an excluded rater silently.
- Do not add anything under `scripts/`, `schemas/`, `.github/` or `skills/`. Do not decide doctrine (which model extracts is the owner's).
- Do not hand-type a figure into the report; the script writes every figure. Do not run `run_checks.py --all`, `bootstrap.sh`, or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push. Do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: Q-T070 is unanswered; a source's text is not derivable; a rater's branch lacks `rater.sql` or its transcript; the blindness check excludes a rater (report it; the owner decides whether to re-launch); the canonical sha moved during the measurement; the script cannot apply a rater's SQL to a copy of the canonical database (the rater copied another base); you would have to guess a value, a name or an owner's intent.

## 10. Rollback

Nothing reaches the database. Before merge: close the pull request; delete the rater branches only if the owner says so (they are the measurement's record).

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once on the report and script; `/batch-done`; push; open the pull request last, once, for the owner; call `unsubscribe_pr_activity` at once; push nothing afterwards except a deliberate change.
