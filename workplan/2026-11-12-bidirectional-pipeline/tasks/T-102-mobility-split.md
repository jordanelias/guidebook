# T-102  Decompose the mobility family by device, and carry the rows filed under MOB

> **NOT FOR SONNET** — population taxonomy; re-tagging is a judgment about each figure. Opus-class or above, with the owner's answer. A Sonnet-class executor that opens this file does not start it: it reports that the task is waiting, and for what.

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Three tasks of this plan were executed in scratch clones (T-006, T-008, T-010) and the defects they showed in the task files were corrected in every file by one generator; this file's own steps have not been executed by anyone. Its evidence command was run on 2026-11-12 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-102 |
| Title | Decompose the mobility family by device, and carry the rows filed under MOB |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET (see the note above) |
| Traces to | IMP-20 in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md`; the owner's answer to OD-14 (2026-11-12, third set: "Decompose MOB by device to wheelchair user, prosthetic device user, other mobility aids (or something like that)"); OD-37; `workplan/2026-11-12-bidirectional-pipeline/POPULATION-UMBRELLAS-MEMO.md` (advisory, not adopted wholesale) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-018, T-025, T-055 merged; and the design `T-102-design.md` present (written 2026-11-12 by an Opus-class session under item 1 below and committed beside the task files; it is reported to the owner by item 2 before any row is written; T-055 builds from it). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions that must be answered first.** The answer must be in `references/project-standards.md` (the ledger), in the owner's words. **A delegated resolution does not open this task:** the delegated resolution of OD-14 was withdrawn on independent review and referred back to the owner (`grep -n -F "Correction 2026-11-12 — to the delegated resolution of OD-14" references/project-standards.md`). Start only when the last status line for OD-14 reads `ANSWERED BY THE OWNER` (`grep -F "OD-14 STATUS:" references/project-standards.md | tail -1`); any other value, or none, is a stop.
  - **OD-14** — **Answered by the owner, 2026-11-12 (third set):** "Decompose MOB by device to wheelchair user, prosthetic device user, other mobility aids (or something like that)" (`grep -n -F "OD-14: MOB is decomposed by device" references/project-standards.md`). The exact codes and edges are this task's design to propose and to report to the owner (item 2); the owner's "(or something like that)" is not a licence to decide the taxonomy without that report. Check: `grep -F "OD-14 STATUS:" references/project-standards.md | tail -1` must read `ANSWERED BY THE OWNER`.
  - **OD-37** — answered with OD-14 (`MOVE` and `VES` are access needs, handled by T-054 and T-114; `MH`, `NDV`, `TALL` retained; `ALL`, `DEAF`, `LMB`, `COM` unchanged). Check: `grep -F "OD-37 STATUS:" references/project-standards.md | tail -1` reads `ANSWERED BY THE OWNER`.
  - **OD-31** — **answered by the owner, 2026-11-12 (fourth set):** "Heading's group; ALL leaves the identity lens" (`grep -n -F "OD-31: a provision that names no one" references/project-standards.md`). Check: `grep -F "OD-31 STATUS:" references/project-standards.md | tail -1` must read `ANSWERED BY THE OWNER`. The design-first and owner-report steps (section 4, items 1 and 2) still precede any row.
- **Tests that must be red (or green) before you start:** AT-62 red (restated in section 6). (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
BASE=$(git cat-file -e origin/main:workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md 2>/dev/null && echo origin/main || echo origin/ccr-408aaa9b-z3e4s0); echo "BASE=$BASE"
git switch -c task/t-102-mobility-split "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>            # the session stem: bare in the database, with .md for emit_data_migration --session
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-102" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/t.db"   # s.db is the batch's working copy; t.db is for probes
```
- **Shell variables do not survive from one tool call to the next in this harness.** Write the stem down once and begin every later command block by setting `BASE`, `STEM` and `SCRATCH` again to the same values.
- **Real execution:** open with `/session-open` (it sets `scratchpad/CURRENT` to the stem and creates the folder of the same name), then `/orient`. Follow `skills/run-pipeline_SKILL.md`. **Pilot or dry run** (a scratch clone): skip `/session-open`, stay on the branch you were given, do the work on the scratch copy only, and stop before the write path below.
- Work only on the scratch copy and point every call at it inline:
```
GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py <verb> ... --session "$STEM"
```
- Land the rows only by the write path, after the work is finished:
```
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH/s.db" --out "$SCRATCH/batch.sql"
python3 scripts/emit_data_migration.py --session "$STEM.md" --summary "<what the batch is>" --input "$SCRATCH/batch.sql"
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"      # must exit 0
```
Research batches are serial: if another research batch merged after you copied the database, `emit_batch_sql.py` refuses ("copied from a different base"). Do not force it; start again from the new base.

## 3. The problem, in the guidebook's terms

The owner split the mobility group on 2026-08-25 (`AMB`, `WHEEL`) and on 2026-11-12 decomposed it by device instead: wheelchair users, prosthetic device users, other mobility aids. Every mobility figure still sits on `MOB`, and the registry has no child of it; device and impairment level have no settled home.

**Evidence command** (run from the repository root; read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select identity_code, parent_code, status from base_taxonomy_identity where category='mobility' order by 1\").fetchall()); print(c.execute(\"select identity_code, count(*) from v_live_lens_links where identity_code is not null group by 1 order by 2 desc\").fetchall()); print(c.execute(\"select x.device_class, count(*) from v_live_lens_links k join source_value_extractions x using(extraction_id) where k.identity_code='MOB' group by 1\").fetchall()); print(c.execute(\"select count(*) from evidence_population_match where target_population='MOB'\").fetchall())"
```

**Expected output today:** `MOB`, `SCI`, `LMB` under mobility, none with a parent; most figures tagged `MOB`; `device_class` empty on most `MOB` rows; grades against `MOB`. Facts behind the design (keyword counts of what each row names, the device vocabulary, the rule-5 risk): `workplan/2026-11-12-bidirectional-pipeline/DECISION-CLOSURE.md` §5. (The figure's lens codes are read through T-018's `v_live_lens_links`: after T-018 the four lens columns of `source_value_extractions` are NULL, and a query on them examines nothing.)

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **Design first (`tasks/T-102-design.md`, committed 2026-11-12).** It proposes `WHEEL` (wheelchair users), `PROSTH` (people who use a lower-limb prosthesis) and `WALKAID` (people who use walking aids) under `MOB`, renamed "disabled people with mobility needs"; `device_class` gains `lower_limb_prosthesis`, `crutches`, `cane`; five open edges with recommendations (its sections 2 to 4). Execute it; where this file and the design differ, the design governs. What it was asked to cover, kept for the record:
   - **The children, each with `parent_code = 'MOB'`** (the column exists; no schema change), `MOB` itself kept `active` as the parent. The plan's starting proposal, which the design confirms or corrects with reasons: `WHEEL` (wheelchair users; the 2026-08-25 code, and a constituency a membership organisation names), a prosthetic-device-user code, and an other-mobility-aids code (crutches, canes, walking frames, rollators). Display names in the communities' own words where a self-named community exists (the fourteenth statement), each with its provenance; a code string that is not an initialism of one organisation.
   - **A person with a mobility need who uses no aid** stays on the parent `MOB` and is reached through the ICF d4 codes and the access needs (`A-EFFORT`, `A-STABLE`, `A-REACH`), not given a child, unless the design finds a self-named community for it.
   - **`AMB` of the 2026-08-25 ruling is an open edge, reported, not decided:** the design says what the device decomposition does to it (absorbed into the other-aids child and the parent, minted as a further child, or retired unminted) and leaves the choice to the owner. The same for three further edges: scooter users (a wheeled device; liminal by the memo's sources), ambulatory and part-time wheelchair users (on both sides of a device line), and the overlap of a prosthetic-device-user code with `LMB` (limb difference), which OD-37 leaves unchanged.
   - **Descriptors, one home each (rule 5):** wheelchair drive (power, manual, attendant, scooter) stays in `device_class` and never becomes a code; the design names the `device_class` values the children need that the CHECK lacks (a prosthesis, crutches, a cane or stick), which T-055 adds. Impairment level (paraplegia, quadriplegia) stays out of the identity lens: the medical lens when a source names it, ICF b-codes for the function it changes. No division is held both as a code and in `device_class`.
   - **Commonality at the parent** (owner, 2026-11-12, second statement): a determination at `MOB` gathers its children by the parent pointer (T-055 builds the gather); a child's determination gathers only that child.
2. **Report to the owner before any row is written.** Append to `references/project-standards.md` the entry drafted in `T-102-design.md` section 10, headed "Report 2026-…: the mobility codes as designed (T-102)" (date from `date -u +%F`; facts re-derived on the day): the codes, display names, parents, descriptors, and the open edges, each with its evidence. It is a report, not an owner statement, and carries no status line. Write no row until it is appended; an owner reply that changes the codes changes the design first.
3. **Add the children** with T-025's identity verb, each with its parent and the ledger pointer to the report of item 2 (which holds each code's provenance); rename `MOB` with T-025's amend verb; write the children's ICF crossings only if the owner confirms them (`T-102-design.md` section 7).
4. **Carry the rows filed under `MOB`, by judgment, row by row**, with T-018's `add-lens-link` and `retire-lens-link` and the decision table of `T-102-design.md` section 6 (a figure's `MOB` code is a live link in `extraction_lens_links` after T-018, not the retired `identity_code` column): a figure whose own words name wheelchair users goes to `WHEEL` (and its drive, if stated, to `device_class`); one naming a prosthesis to the prosthetic child; one naming crutches, canes, frames or rollators to the other-aids child; one naming several goes to each through the link table of T-018, never copied. **A figure that names no one takes the group its heading names (OD-31, answered 2026-11-12):** under a mobility heading it stays on the parent `MOB` (the parent is not superseded) and goes to no child, since it names no device; under a general disability heading ("persons with disabilities", "accessible") it carries **no identity** and is carried by its ICF and access-need lenses alone (T-106 fills them; a row may not be left with no lens, by the column CHECK); universal good design is never tagged `ALL` (`ALL` leaves the identity lens: T-056, T-115), and "universal" is stated only by the determination's `design_scale`. Record the heading that decided each such row in the pull request. **A grade of a study's own participants is never fanned out** (the 2026-08-25 ruling): the `MOB` grade stays as the parent-level grade; a new grade against a child is written only where the study's participants are that child. No grade is retired, so `evidence_population_match` needs no retirement column.
5. **`MOB`'s display name** ("disabled people with mobility needs; wheelchair users") joins two things in one cell; the design proposes a parent name without "wheelchair users", applied by the identity verb.

## 5. Caller sweep

A research task renames nothing and changes no code, so the sweep that applies is the one for prose that restates a fact your rows change (CLAUDE.md rule 7a). For each row id, code or value you change, search the reading surface and the governance prose, and correct a sentence your rows make false (or stop, if correcting it is not research):

```
V='<the id, code or value you changed>'
git grep -n -F -e "$V" -- governance architecture CLAUDE.md references skills ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```

Structures this task touches, for orientation: `MOB`. The ledger (`references/project-standards.md`), `sessions/` and committed migrations are records and are never edited.

## 6. Verification

**Red before, green after.** AT-62, restated for the device decomposition. After, on the migrated database:
(1) the children named in the design exist with `parent_code = 'MOB'` and `MOB` is `active`: `select identity_code, parent_code, status from base_taxonomy_identity where category='mobility' or parent_code='MOB'`;
(2) the owner report exists and precedes the rows: `grep -n -F "the mobility codes as designed (T-102)" references/project-standards.md`;
(3) no figure still linked to `MOB` names a wheelchair, a prosthesis or a walking aid in its own words, read through `v_live_lens_links` (after T-018 the `identity_code` column is NULL, so a query on it prints 0 having examined nothing): run the command of `T-102-design.md` section 8, test 3; it prints a non-zero `EXAMINED` and then 0 (a row the executor judged otherwise is listed in the pull request with its reason);
(4) no grade was fanned out: `select count(*) from evidence_population_match where target_population='MOB'` is unchanged, and every new child grade names its participants;
(5) no division is held twice: no display name or description of `MOB` or a code whose parent is `MOB` names a wheelchair drive or an impairment level (`T-102-design.md` section 8, test 5; `SCI`'s description is outside the family and reported, not changed); and tests 6 to 8 of that section.

**Fixtures.** Probes run on `$SCRATCH/t.db`; the batch's own rows are written on `$SCRATCH/s.db` and reach `data/guidebook.db` only through the write path of section 2.

**The gates, once each:**

```
BASE=$(git cat-file -e origin/main:workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md 2>/dev/null && echo origin/main || echo origin/ccr-408aaa9b-z3e4s0)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8   # the research gate
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run each once, after the migration is applied and before the commit.** `preflight.sh` runs the selftest and `run_checks.py --changed-from`; do not run `run_checks.py` separately, and never `--all`.
- **Proof that each gate examined something.** A check scoped to a session id that matches no row passes having read nothing. Confirm the stem is the one stored on your rows. The tables a batch writes carry `created_by_session` and `updated_by_session`; for each table this task writes, `python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select count(*) from '+sys.argv[2]+' where created_by_session=? or updated_by_session=?',(sys.argv[1],sys.argv[1])).fetchone())" "$STEM" <table>` must be above 0 after the migration is applied. `research_batch_dod` prints its own `EXAMINED:` lines: read them in `dod.txt`. A passing check prints no `EXAMINED:` line in `gate.txt`; any check under `NOTHING-IN-SCOPE` there has not passed. `migration_reproducibility` compares row counts only, so an UPDATE is invisible to it: also run `python3 scripts/audit/migration_reproducibility.py --deep`, which compares every row.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "run-pipeline: decompose the mobility family by device and carry the MOB rows [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, taken from `date -u`. Do not copy trailers from this file; use the ones your session was given.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly. Rows land only by the write path of section 2.
- Do not hand-write SQL against a table a `db.py` verb can reach. A table no verb reaches is a gap to file (`db.py add-gap`), not a licence.
- Do not put tooling in this pull request: no schema migration, no new verb, no new check, no edit under `scripts/`, `schemas/`, `.github/` or `skills/` (CLAUDE.md rule 10). A writer gap found on the way is filed and left.
- Do not write a bibliographic field from memory when a payload is in hand; do not mark a source verified that was not re-retrieved; never leave `verification_status` NULL.
- Do not move, round or re-key an adjudicated figure. Do not back-translate a term. Do not delete an empty search.
- Do not author `best_practice_synthesis` or synthesis prose below the Opus floor.
- Do not decide doctrine (mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory). Stop instead.
- Do not treat any `[A-Z]-NN` code as a container, an example or a name.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push. Do not subscribe to pull-request activity or schedule check-ins.
- Do not hand-type a count into any file or message; write the command that computes it.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller (as defined there) that you cannot repair without adding something section 4 does not name. A caller you can repair is repaired and listed; a mention is left;
- a check or test that was green in the before-run is red in the after-run, at any level (the test files are registered as advisory, so the gate will not stop you: the before-and-after comparison is what does);
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent.
- the last status line for OD-14 is anything but `ANSWERED BY THE OWNER`;

## 10. Rollback

Before the migration is applied: delete the scratch copy; nothing has changed. After it is committed: a data migration is append-only and immutable; correct a wrong row with a compensating migration written through the same verbs (retire, supersede, amend), never by editing or deleting the file.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
