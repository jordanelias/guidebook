# T-128  The population-to-ICF rows the writer's proposals need: reaching, seated and standing posture, and the groups with no row

> **WITHDRAWN 2026-11-25 (OD-87, delegated resolution; ledger "Delegated resolutions 2026-11-25 (second)").** Its purpose was to add rows to `identity_icf_map`, which OD-77 holds (no session adds a row to it). The reach code `d4452` and the posture codes are minted by `add-icf-code` when T-127 needs them, after pull request 246 has merged, so they are parented at mint. If this task is reinstated, OD-67's confirmation of its list is owed again**

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: the mapping design `workplan/2026-11-12-bidirectional-pipeline/MAPPING-DESIGN.md` section 2(b), and the coordinator's entry of 2026-11-15 that corrected the sixteenth set's ACTION and registered OD-67 (`grep -n -F "Correction and registration 2026-11-15" references/project-standards.md`); the writer that reads these rows as proposals is T-126; with T-126 this resolves `OPEN-ITEMS-PLAN.md` OI-73. Migration 109's header calls the five groups' rows "an owner item" (`grep -n -F 'an owner item' scripts/migrations/109_drop_axes.sql`). Every number in this file was read on 2026-11-15 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-15 by the integrator of the mapping design. Expect to find a defect in this file, and report it rather than work around it.

> **HELD** until the owner answers OD-67 (may the batch's full list of new population-to-ICF rows be confirmed in one answer?). An executor may prepare the list on a scratch copy before the answer (sections 3 and 4, items 1 to 4), but lands nothing, and opens no pull request, until the gate below prints `OD-67 OPEN (owner)`.

## 1. Identity

| | |
|---|---|
| Task | T-128 |
| Title | The population-to-ICF rows the writer's proposals need: reaching, seated and standing posture, and the groups with no row |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request; the rows are base rows landed by a data migration, written only through verbs `scripts/db.py` already has; no new tooling) |
| Executor | NOT FOR SONNET (Opus-class: each row is a judgment of which group is limited in which activity, by what mechanism, with what confidence) |
| Traces to | OD-67 (referred to the owner, `grep -n -F "OD-67 STATUS:" references/project-standards.md`); OI-73; WRK-181's direction as migration 109 records it; OD-14 and OI-03 (the mobility family and its crossings, T-102); OD-37 (VES is an access need, T-114); the 2026-09-11 "no anchor" ruling migration 109 cites for BAR, LPA and TALL |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it). Every command uses `$BASE`.
- **Tasks that must be merged to the integration base first:** T-102 merged (`WHEEL` minted, `SCI` retired to it; through it T-054, whose `retired_at` on `identity_icf_map` and refusal of a deprecated identity this batch relies on, and T-055). Check: `git log "$BASE" --format=%s | grep -c -E 'task/t-102-mobility-split|^T-102:|execute workplan T-102'` prints at least 1, and `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select identity_code, status from base_taxonomy_identity where identity_code in ('WHEEL','SCI')\").fetchall())"` shows `WHEEL` active.
- **Owner decisions that must be answered first.** The answer must be in `references/project-standards.md` (the ledger), in the owner's words; a delegated resolution does not open this task (the coordinator's entry: "Do not resolve it under delegation").
  - **OD-67** — REFERRED TO THE OWNER, registered 2026-11-15 (`grep -n -F "Correction and registration 2026-11-15" references/project-standards.md`): may the batch's full list of new population-to-ICF rows be confirmed in one answer? These rows decide which groups the writer proposes for every code value, which is population taxonomy and the owner's (the mobility crossings went to the owner as OI-03). The batch prepares the full list on its scratch copy (section 4, items 1 to 4) and the coordinator puts it to the owner in that one question (`OWNER-SHEET-PLAIN.md`, question 18). Run the gate before you land anything and again before you open the pull request; it must print `OD-67 OPEN (owner)`, else stop (section 9). The gate reads the status class only; the answer is the last `OD-67:` line (`REMEDIATION-WORKPLAN.md` section 13, "What the gate reads"); an answer that strikes or changes rows of the list is applied row by row, and nothing outside the confirmed list is written.
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-67; do gate $n; done
```
- **Delegated resolutions this task rests on:** none.
- **Tests that must be red before you start:** `T128-A` (section 6): no `base_icf` row for `d4452`, and no `identity_icf_map` row joining `WHEEL` to a reach code.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-128-population-icf-rows-for-proposals "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-population-icf-rows            # bare in the database, with .md for emit_data_migration --session
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-128" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: set `BASE`, `STEM` and `SCRATCH` again at the head of every block. **Real execution:** `/session-open`, then `/orient`. **Pilot:** no `/session-open`, scratch copy only, stop before the write path.
- **The verbs, verified by command before use** (rule 4; a verb renamed since this file was written is a stop): `git grep -n -E '"(add-icf-code|set-icf-title|add-population-icf-link)"' -- scripts/db.py` prints the three parsers; `python3 scripts/db.py add-icf-code --help`, `set-icf-title --help` and `add-population-icf-link --help` show `--title-payload`, and `--mechanism`, `--mapping-confidence` (its choices read from the column's CHECK) and `--provenance`.
- Work only on the scratch copy: `GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py <verb> ... --session "$STEM"`. Persist every WHO retrieval through `scripts/research/retrieval_log.py`'s `fetch()` (R10: the bytes are written before anything is parsed; a page that is not JSON returns `None` but is saved; a block is not terminal, try the Internet Archive per CLAUDE.md §7), with `GUIDEBOOK_RETRIEVAL_LOG` pointed at `retrieval-log/$STEM/`. Land the rows only by the write path:
```
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH/s.db" --out "$SCRATCH/batch.sql"
python3 scripts/emit_data_migration.py --session "$STEM.md" --summary "<what the batch is>" --input "$SCRATCH/batch.sql"
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"      # must exit 0
```
Research batches are serial: if another merged after you copied the database, `emit_batch_sql.py` refuses; start again from the new base.

## 3. The problem, in the guidebook's terms

T-126's writer proposes, for each code value being recorded, the groups the maps tie to its ICF codes and needs; the recording session judges and writes them. The proposals are only as good as the map rows. Three gaps leave the owner's own defaults without a proposal and some groups with none at all:

- **Reaching has no code.** The owner's mounting-height default concerns reaching from a seated position. ICF nests *Reaching* (d4452) under *Hand and arm use* (d445), and *Maintaining a sitting position* (d4153) and *Maintaining a standing position* (d4154) under *Maintaining a body position* (d415) [titles from the designer's knowledge, unverified: item 1 fetches them]. The d-chapter records activity limitations: wheelchair users are limited in reaching, from a seated reach range, not in hand and arm use as a whole, so the child is the true claim and the parent over-claims. `base_icf` holds d445 and an untitled d415, and neither child; `identity_icf_map` ties d445 to `LMB` only and d415 to no group, so the mounting-height default proposes no wheelchair-user group.
- **Five groups have no row** (ADHD, DEAFBLIND, EPI, MS, VES): migration 109 dropped `population_axis_map` and said their population-to-ICF rows were to be re-derived, "an owner item".
- **Three groups take no anchor** (BAR, LPA, TALL; the 2026-09-11 ruling migration 109 cites): they are judged directly at recording, never proposed. This batch writes nothing for them.

**Evidence commands** (read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select icf_code, title from base_icf where icf_code in ('d445','d4452','d415','d4153','d4154')\").fetchall());print(c.execute(\"select icf_code, group_concat(identity_code) from identity_icf_map where icf_code in ('d445','d4452','d415','d4153','d4154','d465') group by 1\").fetchall())"
python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select identity_code, status from base_taxonomy_identity where status='active' and identity_code not in (select identity_code from identity_icf_map)\").fetchall())"
grep -n -E "ADHD, DEAFBLIND, EPI|an owner item|take no anchor" scripts/migrations/109_drop_axes.sql
grep -E 'INSERT INTO "?population_axis_map' scripts/migrations/057_baseline_*.sql | grep -c -E "'(ADHD|DEAFBLIND|EPI|MS|VES)'"
grep -n -E '^\| `AX-' governance/functional-taxonomy.md | cut -c1-120
```

**Output on 2026-11-15:** d445 titled *Hand and arm use*, d415 present with no title, no d4452, d4153 or d4154; d445 tied to `LMB` only, d415 to no group, d465 to `MOB` and `SCI`; the identities with no map row (ADHD, MS, EPI, ALL, DEAFBLIND, MOVE, ID, VES, LPA, TALL, BAR); migration 109's sentences; the baseline's axis-map rows for the five groups (the retired map's only source: 109 found no data migration that writes it); the axis register with each axis's ICF anchors. If d4452 is already in `base_icf` with a `WHEEL` row, the ground has moved: stop.

## 4. The change

1. **Fetch the WHO titles (R10).** For d4452, d4153, d4154 and d415, retrieve the WHO's own ICF entry (the ICF browser page for the code, or the WHO classification API) through `retrieval_log.fetch()`, and confirm in the saved bytes the code, its title and its parent. A title is never written from memory (CLAUDE.md §5(c)): if the bytes do not hold it, the code is not minted, and the gap is reported.
2. **Mint and title, from the payload.** `add-icf-code --icf-code d4452 --title "<the WHO title>" --title-payload <the saved path>`, and the same for d4153 and d4154; `set-icf-title --icf-code d415 --title "<the WHO title>" --title-payload <the saved path>` (it refuses to overwrite a title; d415 has none today). `component` and `is_range` are derived by the verb.
3. **The wheelchair-user rows.** `add-population-icf-link --population WHEEL --icf-code d4452`, and `WHEEL` to d4153 or d4154 (the batch judges which posture the wheelchair user's limitation is recorded under, and may judge both, each a row with its own mechanism), each with `--mechanism` (how the limitation arises: for reaching, the seated reach range), `--mapping-confidence` (from the column's CHECK) and `--provenance` (the payload, or the ref_id of a source the batch holds that states the limitation). One row per (population, code, mechanism), the table's own UNIQUE.
4. **The five groups' rows, re-derived** (WRK-181's direction). For each of ADHD, DEAFBLIND, EPI and MS: read its rows in the retired axis map (`grep -E 'INSERT INTO "?population_axis_map' scripts/migrations/057_baseline_*.sql | grep -F "'<CODE>'"`), each axis's ICF anchors in `governance/functional-taxonomy.md` §2.1 (`grep -n -E '^\| `AX-' governance/functional-taxonomy.md`), and the axis map's `role` and `note`; propose one row per ICF anchor the batch judges the group is limited in (the d-codes; a b-code where the anchor is a body function and the group's limitation is there), each with mechanism, confidence (a `SITUATIONAL` or `SECONDARY` axis role is not `high_predictive` by default) and provenance naming the baseline rows it was derived from. Write each through `add-population-icf-link`; write none for an anchor the code is not live in `base_icf` for (mint only codes item 1 fetched; another missing code is reported, not minted). **VES:** the owner ruled VES an access need (OD-37, `grep -n -F "OD-37: identity-lens rule" references/project-standards.md`) and T-114 retires it; this batch writes no identity row for VES, whatever its status when the batch runs, and lists VES's re-derived anchors in the pull request as rows withheld, with that reason, so the owner can overrule in the OD-67 answer. (No writer reaches `access_need_icf`: `git grep -n 'access_need_icf' -- scripts/db.py` prints nothing on 2026-11-15; the need side of VES is not this batch's.)
5. **BAR, LPA and TALL get no anchor; ID and MOVE get none here** (ID had no axis-map row to re-derive from; MOVE is retired to the access needs by T-114). Nothing is written for them; the pull request says so.
6. **The list for the owner.** Before landing anything, print every proposed row (population, ICF code, title, mechanism, confidence, provenance) and every withheld row with its reason, as one list, and hand it to the coordinator for OD-67 (`OWNER-SHEET-PLAIN.md` question 18). When the ledger carries the owner's answer and the gate prints OPEN, land exactly the confirmed rows by the write path of section 2.

**What reads what this task adds:** T-126's proposal display and its warning, and `code_value_identity_audit.py` (both read `identity_icf_map` and `base_icf`); T-127, which judges the stored code values' links from these proposals (it runs after this batch, so rows are tagged `WHEEL` and d4452 once, not `MOB` and d445 and then swept again); T-110 (its first determinations compare code values through the links T-127 writes from them); T-059's flip of the audit to blocking. **Not read by the engine:** `_lens_clause` matches a figure's own links and never walks the map (D-0184; OR-1), so a map row changes no cell by itself; and `base_icf` holds no hierarchy, so a d4452 figure does not reach a d445 cell (`OPEN-ITEMS-PLAN.md`, the d4452/d445 item). **Data migration.** Through `scripts/emit_data_migration.py`, which names the file; never type a migration name or number. No schema migration, no new verb.

## 5. Caller sweep

A research task renames nothing; sweep only prose that restates a fact your rows change (rule 7a): `git grep -n -E 'identity_icf_map|d4452|d445\b|d415\b' -- governance architecture references skills ':(exclude)references/project-standards.md'`, and correct a sentence the rows make false (or stop, if correcting it is not research). Report the map's live counts after the batch by command (`select count(*), count(distinct identity_code), count(distinct icf_code) from identity_icf_map`), never as typed figures.

## 6. Verification

**Red before, green after.**
- `T128-A` (live after-test). Before: the first evidence command shows no d4452 and no `WHEEL` reach row. After, on the migrated database: `select count(*) from identity_icf_map where identity_code='WHEEL' and icf_code='d4452'` prints at least 1; d4452, d4153 and d4154 are in `base_icf` with a `title_source` naming a payload under `retrieval-log/`; d415 has a title. And on a scratch copy of the migrated database, a tier 6 fixture row "Controls shall be mounted at a height of not more than 1200 mm" recorded with T-126's verbs (d4452, `A-REACH`, `WHEEL`, basis `context`) lists `WHEEL` among `identities_proposed`, and `determine` for the `WHEEL` lens returns the figure in lens. Catches a map gap.
- Every new row has a non-blank mechanism and provenance, and a confidence from the CHECK; no row names VES, BAR, LPA, TALL, ID or MOVE; the rows landed are exactly the list the owner confirmed (diff the printed list against the landed rows in the pull request).

**The gates, once each:**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
python3 scripts/audit/migration_reproducibility.py --deep
```
Confirm the stem is the one on your rows: `python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select count(*) from identity_icf_map where created_by_session=?',(sys.argv[1],)).fetchone(), c.execute('select count(*) from base_icf where created_by_session=?',(sys.argv[1],)).fetchone())" "$STEM"` is above 0 in both.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "functional-deficit-researcher: population-to-ICF rows for reaching, posture and the groups with no row, as the owner confirmed (OD-67) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the WHO payloads; the codes minted and titled; each row with its mechanism, confidence and provenance; the rows withheld and why (VES, BAR, LPA, TALL, ID, MOVE); the owner's answer line>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not land a row before the gate prints `OD-67 OPEN (owner)`, or a row outside the list the owner confirmed. Do not resolve OD-67 under delegation.
- Do not put tooling in this pull request: no schema migration, no new verb, no edit under `scripts/`, `schemas/`, `.github/` or `skills/`, no registry edit (rule 10). A verb that cannot hold a row is a GAP filed, not a patch.
- Do not write a title from memory, or mint a code whose title the saved bytes do not hold (CLAUDE.md §5(c)).
- Do not write an anchor for BAR, LPA or TALL, a row for VES (OD-37), or a needs-to-identity row anywhere; do not rebuild the dropped axis maps (retired vocabulary, "do not relitigate").
- Do not write a lens link: the code values' links are T-127's.
- Do not write `data/guidebook.db` directly or hand-write SQL against a table a verb reaches. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: the gate prints CLOSED for OD-67; T-102 is not merged or `WHEEL` is not active; a verb named in section 2 is missing or takes other flags; the WHO bytes do not hold a title or give another parent than section 3 states (report it: the design's titles were unverified); the evidence output differs; a check green before is red after; the rebuild does not reproduce the database.

## 10. Rollback

Before the migration is applied: delete the scratch copy. After it is committed: a data migration is append-only; correct a wrong map row with a compensating batch (`retire-population-icf-link`, T-054's verb, with its reason, then `add-population-icf-link`), never by editing the file.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (recorded with `db.py record-adversarial-pass`, closed with `close-adversarial-pass`); `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
