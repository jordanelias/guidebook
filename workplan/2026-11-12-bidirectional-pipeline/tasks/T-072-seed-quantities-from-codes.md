# T-072  Seed the list of quantities from the phrases the held codes use

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Every number in this file was read on 2026-11-13 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 (Opus-class, cluster B). Its evidence command was run read-only on 2026-11-13 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-072 |
| Title | Seed the list of quantities from the phrases the held codes use |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET: whether a phrase names a design quantity, which held term it names or whether it is new, and which quantity kind it is, are judgments read in the code's own language |
| Traces to | prior workplan D-8 (`grep -n '^| D-8 ' workplan/2026-10-23-pipeline-resolution-workplan.md`; the report: `sed -n '/^### D-8 quantity seeding/,/^### S-1/p' scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md`); OR-13 (`grep -n -F 'OR-13: "From the codes held"' references/project-standards.md`); OR-17 (`grep -n -F 'OR-17: "Yes, bulk, with me reading the PR' references/project-standards.md`); the 2026-11-06 answers E1 and E12 (`grep -n -E '^\| E(1|12) ' references/project-standards.md`); the owner's battery question "A robust, value-free list of slugs and parameters" (`grep -n -F 'A robust, value-free list of slugs and parameters' workplan/2026-10-23-pipeline-resolution-workplan.md`); OI-52 |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`).
- **Tasks that must be merged to the integration base first:** T-020 (a parameter states its quantity kind, with an observation as warrant; `add-parameter` takes both), T-028 (a term minted from an observation is named by the observed phrase and gets its first member row; E1's naming), T-101 (the research scope recorded on every pair, so "the codes held" in scope is read from `v_research_scope`, not from a list), T-105 (the full reading of held sources, whose open pass records every quantity phrase a source uses with `observe-term`; OR-13 seeds from that pass). Check by running each task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F 'task/t-<nnn>'` for each.
- **Owner decisions:** none in the register. Rulings: OR-13 ("From the codes held": the quantities are seeded by an open-pass scan of the codes already held, not slug by slug); OR-17 (the assistant approves vocabulary in bulk; the owner reads the pull request; no phrase the model generated); E1 (a concept first met outside English is named by the instrument's own phrase, in its own language, until an English-language instrument of the scope names it; no English gloss typed); E12 (the functional-axis and method terms are declined as parameters). **One gate already stated elsewhere holds part of this task:** a parameter whose quantity kind is not yet in `base_quantity_kinds` waits for the owner to approve the new kind in a dated ledger entry (T-109 section 4 item 1: "a new kind is proposed with its warrant for the add-kind verb, never typed into a cell"). This task proposes such kinds in a table; it does not add them.
- **Open owner question bearing on this task (not its gate; added 2026-11-13):** OD-50 (the Edmonton adjudication's AQ-4), OPEN, not yet asked: may a source that is not a code add a parameter, or only mint the term and wait for a code? This task's subject is the held codes (OR-13), so it proceeds whatever the answer; if the answer is "any admitted source" or "two independent sources", the coordinator widens its subject or authors a sibling task then. Its item 6 (leftover terms) is also where the terms a single-source batch may not decline land, if OD-53 (AQ-7) is answered "the catalogue task only". Not put in the bullet above: neither holds this task.
- **Tests that must be red before you start:** section 6's count of observations from in-scope held codes that are neither adjudicated nor the warrant of a parameter is above 0.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-072-seed-quantities-from-codes "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-072" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/t.db"
```
- **Shell variables do not survive between tool calls.** Set `BASE`, `STEM` and `SCRATCH` again at the top of every block.
- **Real execution:** `/session-open`, then `/orient`; follow `skills/run-pipeline_SKILL.md`. **Pilot or dry run:** work on the scratch copy only and stop before the write path.
- Work only on the scratch copy: `GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py <verb> ... --session "$STEM"`. Land the rows only by the write path:
```
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH/s.db" --out "$SCRATCH/batch.sql"
python3 scripts/emit_data_migration.py --session "$STEM.md" --summary "<what the batch is>" --input "$SCRATCH/batch.sql"
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"      # must exit 0
```

## 3. The problem, in the guidebook's terms

The guidebook's parameters are the questions its pages answer. The list is short, and the codes the project already holds treat many more things as design quantities (a handrail's height, a landing's length, a surface's slip resistance). A page can only ask about what is on the list, so the list decides what a reader is prompted to ask. The owner ruled that the list is seeded from the codes held, in their own words, and never from the old item index (OR-13; the report: "Never take a name from the old Part 4 item index").

**Evidence command** (read-only):

```
python3 -I - <<'PY'
import sqlite3, sys; sys.path.insert(0, 'scripts'); import db
c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
REG = sorted(db._regulatory_pairs()); q = " or ".join("(e.evidence_type=? and e.scope=?)" for _ in REG); P = [x for p in REG for x in p]
print("active parameters:", c.execute("select count(*) from base_parameters where status='active'").fetchone()[0])
print("held regulatory sources in scope, not superseded:", c.execute(f"select count(*) from evidence_sources e where ({q}) and e.superseded_by_ref_id is null and e.jurisdiction in (select jurisdiction from v_research_scope)", P).fetchone()[0])
print("  of them with a full reading and an open pass:", c.execute(f"select count(distinct e.ref_id) from evidence_sources e join source_scans s on s.ref_id=e.ref_id where ({q}) and e.superseded_by_ref_id is null and e.jurisdiction in (select jurisdiction from v_research_scope) and s.text_scope='full' and s.open_pass_done=1", P).fetchone()[0])
LATEST = "with latest as (select a.* from term_adjudications a where a.adjudication_id=(select max(adjudication_id) from term_adjudications b where b.observation_id=a.observation_id)) "
print("their observations by latest outcome:", c.execute(LATEST + f"select coalesce(l.outcome,'UNADJUDICATED'), count(*) from observed_terms o join evidence_sources e on e.ref_id=o.ref_id left join latest l on l.observation_id=o.observation_id where ({q}) and e.jurisdiction in (select jurisdiction from v_research_scope) group by 1", P).fetchall())
print("terms minted from an observation that are not parameters and not declined:", c.execute(LATEST + "select distinct l.term_id from latest l where l.outcome='NAMES-NEW' and l.term_id not in (select term_id from base_parameters) and l.term_id not in (select term_id from parameter_declinations where revoked_at is null) order by 1").fetchall())
PY
```

**Expected output today** (2026-11-13): a short list of active parameters (10); a few dozen held regulatory sources in the scope as it stands before T-101 (26); **none of them read in full with an open pass** (0), which is why this task waits for T-105; their observations, most already adjudicated NAMES-EXISTING, a few UNADJUDICATED, NAMES-NEW, NOT-OURS and DEFERRED; and a few terms minted from observations that are neither parameters nor declined (TERM-090, TERM-092, TERM-093, TERM-094 on 2026-11-13).

## 4. The change

Order of preference, from CLAUDE.md §8. Every verb this task needs exists once its dependencies merge; it adds no code.

1. **The subject**, derived, never listed: the observations recorded from held sources in the regulatory stratum (`db._regulatory_pairs()`, as section 3 reads it), not superseded, whose jurisdiction is owed by `v_research_scope`. After T-105 these include every quantity phrase the open pass recorded. **Chosen (authoring 2026-11-13): this task works from observations already recorded and does not run its own open pass.** Rejected: a second open pass here, which would read the same codes twice (OD-23: duplicate reads are to be minimised) and split one scan contract across two tasks. If T-105 has merged and a held in-scope code still has no full reading with an open pass, list it; do not read it here.
2. **Adjudicate each unadjudicated observation of the subject** (`db.py adjudicate-term --observation-id N --outcome ... --rationale "<why, from the quote>"`), reading the phrase in its own language: NAMES-EXISTING with the held term, NOT-OURS for a real phrase that is not a design quantity of ours (a legal heading, a procedure), DEFERRED only when the source alone cannot settle it. Include the observations T-069 left unadjudicated as naming a new concept.
3. **Mint a term for each phrase that names a design quantity we do not hold:** `db.py add-term --from-observation N --canonical-en "<label>" --rationale "..." --session "$STEM"` as T-028 leaves the verb. The label follows E1: the observed phrase in its own language until an English-language instrument of the scope is observed naming the same concept; never a typed English gloss, never a value (the writer's screen refuses digits, comparators and min/max words; never work around it). If the same concept is observed in several codes, mint once and adjudicate the others NAMES-EXISTING.
4. **Promote a term to a parameter only when it is a quantity:** `db.py add-parameter --term-id T --quantity-kind K --quantity-kind-observation-id N --session "$STEM"` (T-020's flags), where `N` is an observation whose quote states a value of that quantity with its unit (T-020's writer refuses a warrant with no digit). The kind is read from `base_quantity_kinds`; the split rule is T-020's: two cases are two parameters only when they cannot be placed on one scale or their accessibility directions differ. A term that is a functional axis or a method is not promoted (E12); where it should be recorded as declined, use `decline-parameter` with its reason.
5. **A quantity whose kind is not held** (slip resistance, for example, if no held kind fits): mint the term (item 3), do not promote it, and add a row to a table in the pull request: the term, the proposed kind's id and definition (no digit), the observation that warrants it, and the parameters it would carry. That table is for the owner to approve in a dated entry; the kind is then added with `add-quantity-kind --approval-ref "<that heading>"` and the parameters promoted in a later batch. **Chosen:** the owner approves a new kind, as T-109 says; OR-17's bulk approval by the assistant covers phrases, names and aliases, and a kind is none of those.
6. **The terms already minted from observations and not yet parameters** (section 3's last line): judge each by item 4, and promote, decline with a reason, or leave with the reason (for example, E2 holds a rename for TERM-090 and TERM-092: `grep -n '^| E2 ' references/project-standards.md`; a rename is not this task's).
7. **Never** take a name from the old Part 4 item index, from an `[A-Z]-NN` code, from `references/` prose or from memory. The 2026-10-09 catalogue route (`mint-term-from-catalogue`, owner-approved table) is not this task's.

**What reads what this task adds:** the scan contract of every later reading (every source is read against the whole parameter list, so a new parameter widens every reading); `v_scan_ledger` (new parameters become owed readings of every held source); T-067's view; the page list.

**Data migration.** Rows land through `scripts/emit_data_migration.py` only. No schema migration and no file under `scripts/` other than that one `scripts/migrations/data_*` file.

## 5. Caller sweep

A research task changes no code. For prose that restates a fact your rows change (rule 7a): a sentence that lists the parameters, or states how many there are, is a caller; replace a list or count with the command that derives it, or stop if the sentence is doctrine.
```
git grep -n -i -e 'active parameters' -e 'the ten parameters' -e 'parameters 4 to 12' -- governance architecture references skills ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
`stress/listing.py` (committed with the 2026-10-22 report) regenerates the list of slugs and parameters; run it after the migration and report its hits for existing names, each dispositioned in the pull request (the prior workplan's proof for this battery question): `python3 -I scratchpad/session_2026-10-22-pipeline-stress-test/stress/listing.py` (if it is not at that path, `git ls-files | grep 'stress/listing.py'`).

## 6. Verification

**Red before, green after.** Re-run section 3's command on the migrated database. Before: the subject holds unadjudicated observations, or NAMES-NEW terms that are neither parameters nor declined. After: no observation of the subject is unadjudicated except those listed with a reason; every NAMES-NEW term of the subject is a parameter, declined with a reason, or listed (kind awaiting approval, or rename held by E2); every new parameter has a `quantity_kind` and a `quantity_kind_observation_id` whose quote holds a digit:
```
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select p.parameter_id, t.canonical_en, p.quantity_kind, p.quantity_kind_observation_id from base_parameters p join terms t using(term_id) where p.created_by_session=?',(sys.argv[1],)).fetchall())" "$STEM"
```
prints no row with a NULL kind or warrant. The pull request carries the new-kind table of item 5 (or says it is empty) and every adjudication's outcome by command.

**The gates, once each:**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
python3 scripts/audit/migration_reproducibility.py --deep
```
Proof each gate examined something: `terms`, `term_adjudications` and `base_parameters` rows with `created_by_session = "$STEM"` above 0 after the migration (any table you did not write is said so). `research_dod_session` is red by construction on a batch that searches and admits nothing (OI-55 (1)): report its lines and say so.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "run-pipeline: seed quantities from the phrases the held codes use (D-8, OR-13) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: each new term and parameter with its observation and code; the adjudications; the new-kind table for the owner>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly. Do not type a phrase, a gloss or a name; every name comes from an observation (OR-17, E1).
- Do not take a name from the old item index or any `[A-Z]-NN` code. Do not mint from a registry here.
- Do not add a quantity kind, or promote a parameter under a kind that is not held. Do not promote a functional-axis or method term (E12).
- Do not read a source here that T-105 should have read; list it. Do not decide doctrine.
- Do not put tooling in this pull request (rule 10). Do not run `run_checks.py --all`, `bootstrap.sh`, or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push. Do not subscribe to pull-request activity.
- Do not hand-type a count; write the command.

## 9. Stop conditions

Stop and report when: a precondition is not met (in particular, T-105 has not merged, or T-020's flags are absent from `add-parameter --help`); section 3's output differs in shape; a writer refuses a name or a warrant you would have to work around; a phrase can be named only by typing English; the same concept seems to need two parameters and T-020's split rule does not settle it; you would have to guess a value, a kind, a name or an owner's intent.

## 10. Rollback

Before the migration is applied: delete the scratch copy. After it is committed: a wrong parameter is retired (`retire-parameter`) or merged (`merge-parameter`), a wrong term renamed by its route, in a compensating batch; never edit the data migration.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (recorded with `record-adversarial-pass`, closed with `close-adversarial-pass`); `/batch-done`; push; open the pull request last, once, for the owner to read (OR-17); call `unsubscribe_pr_activity` at once; push nothing afterwards except a deliberate change.
