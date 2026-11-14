# T-102  Decompose the mobility family by device, and carry the rows filed under MOB

> **NOT FOR SONNET** — population taxonomy; re-tagging is a judgment about each figure. Opus-class or above, with the owner's answer. A Sonnet-class executor that opens this file does not start it: it reports that the task is waiting, and for what.

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted (partial)** 2026-11-13: report `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-102-report.md` (the carry and the replay on a sample; the final retirement was not reached because T-054 was not in the stack); defects folded. Expect to find a further defect in this file, and report it rather than work around it.

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
- **Tasks that must be merged to the integration base first:** T-018, T-025, T-054, T-055 merged (T-054 for `retire-identity --to-identity` and `retire-population-icf-link`, which retiring `SCI` to `WHEEL` needs); and the design `T-102-design.md` present (written 2026-11-12 by an Opus-class session under item 1 below and committed beside the task files; its codes and edges were confirmed by the owner on 2026-11-12, fifth set, which discharges item 2's report; T-055 builds from it). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`, and by the tooling check below.
- **Tooling the write path needs, checked on `$BASE` before any row** (added 2026-11-13 from the pilot). The pilot's stack carried T-018's table but not its emitter fix, and the batch could not be replayed: `emit_batch_sql.py` wrote `extraction_lens_links`' INSERTs before its UPDATEs, so the judged link that replaces a carried one was inserted while the carried one was still live, and both the replay and `migrate_db.py --rebuild` failed with `UNIQUE constraint failed: index 'ux_extraction_lens_live'`. Every figure that stays on `MOB` with a judged warrant takes that path. The folded T-018 changes the order (its section 4, item 4; its case T018-08); that is one reason this task waits for T-018's merge. Prove both the order and the rest of the tooling before the first `db.py` call:
```
grep -c -F 'lines += updates + inserts' scripts/research/emit_batch_sql.py     # must print 1
grep -c -F 'lines += inserts + updates' scripts/research/emit_batch_sql.py     # must print 0
python3 scripts/tests/test_db_amend_writers.py 2>&1 | grep -F 'T018-08'        # must print one line beginning [✓]
python3 -I - data/guidebook.db <<'PY'
import sqlite3, sys, subprocess
c = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
cols = lambda t: {r[1] for r in c.execute(f'pragma table_info("{t}")')}
svx = c.execute("select sql from sqlite_master where name='source_value_extractions'").fetchone()[0]
h = subprocess.run(["python3", "scripts/db.py", "-h"], capture_output=True, text=True).stdout
print("T-018 table and view", bool(cols("extraction_lens_links")) and bool(cols("v_live_lens_links")))
print("T-054 successor and crossing retirement", "superseded_by_identity" in cols("base_taxonomy_identity") and "retired_at" in cols("identity_icf_map"))
print("T-055 device values", all(f"'{v}'" in svx for v in ("lower_limb_prosthesis", "crutches", "cane")))
print("verbs", all(v in h for v in ("add-identity", "amend-identity", "add-lens-link", "retire-lens-link", "retire-identity", "retire-population-icf-link")))
PY
```
Every line of the last command must print `True`. Any other output is a stop (section 9): do not reorder the emitted file by hand, and do not start without T-054 (a stack without it can carry the figures but cannot retire `SCI`, and this task has no partial path).
- **Owner decisions that must be answered first.** The answer must be in `references/project-standards.md` (the ledger), in the owner's words. **A delegated resolution does not open this task:** the delegated resolution of OD-14 was withdrawn on independent review and referred back to the owner (`grep -n -F "Correction 2026-11-12 — to the delegated resolution of OD-14" references/project-standards.md`). Start only when the last status line for OD-14 reads `ANSWERED BY THE OWNER` (`grep -F "OD-14 STATUS:" references/project-standards.md | tail -1`); any other value, or none, is a stop.
  - **OD-14** — **Answered by the owner, 2026-11-12 (third set):** "Decompose MOB by device to wheelchair user, prosthetic device user, other mobility aids (or something like that)" (`grep -n -F "OD-14: MOB is decomposed by device" references/project-standards.md`). The exact codes and edges were proposed by the design and **confirmed by the owner, 2026-11-12 (fifth set):** "Confirm all as proposed" (`grep -n -F "OD-14: codes confirmed as proposed in T-102-design.md" references/project-standards.md`): `MOB` stays as the parent, renamed "disabled people with mobility needs", with three device children `WHEEL` (wheelchair users, including ambulatory and part-time wheelchair users), `LLD` (people with lower-limb differences; ninth set, replacing the proposed `PROSTH` (people who use a lower-limb prosthesis)) and `WALKAID` (people who use walking aids: crutches, canes, frames, rollators); `AMB` is not minted; scooter users stay on `MOB` with `device_class = scooter`; `PROSTH` is lower-limb only and `LMB` is unchanged; a person with a mobility need who uses no aid has no child. Write rows on these, **as revised by the owner on 2026-11-12 (sixth to ninth sets): the lower-limb child is `LLD`, "people with lower-limb differences" (condition-defined, replacing `PROSTH`); `SCI` is retired to `WHEEL`; `LMB` becomes `UPL`, outside the family (not this task).** Check: `grep -F "OD-14 STATUS:" references/project-standards.md | tail -1` must read `ANSWERED BY THE OWNER`.
  - **OD-37** — answered with OD-14 (`MOVE` and `VES` are access needs, handled by T-054 and T-114; `MH`, `NDV`, `TALL` retained; `ALL`, `DEAF`, `LMB`, `COM` unchanged). Check: `grep -F "OD-37 STATUS:" references/project-standards.md | tail -1` reads `ANSWERED BY THE OWNER`.
  - **OI-13** (an open item of `OPEN-ITEMS-PLAN.md`, not a register decision) — **answered by the owner, 2026-11-12, sixth to eighth sets:** "SCI is the same as WHEELCHAIR basically"; "LMB should be UPL for upper limb then"; "and that doesnt concern mobility"; and, ninth set, the selected option "LLD — 'people with lower-limb differences'" (`grep -n -E "Owner clarification 2026-11-12 \((eighth|ninth) set\)" references/project-standards.md`). Check: `grep -F "OI-13 STATUS:" references/project-standards.md | tail -1` reads `ANSWERED BY THE OWNER`. The family is `MOB` with `WHEEL`, `LLD`, `WALKAID`; `SCI` is retired to `WHEEL` here (design §6a); `LMB` is not this task's (T-116).
  - **OD-31** — **answered by the owner, 2026-11-12 (fourth set):** "Heading's group; ALL leaves the identity lens" (`grep -n -F "OD-31: a provision that names no one" references/project-standards.md`). Check: `grep -F "OD-31 STATUS:" references/project-standards.md | tail -1` must read `ANSWERED BY THE OWNER`. The design-first and owner-report steps (section 4, items 1 and 2) still precede any row.
  - **OI-03, OI-48, OI-49** (open items, answered by the owner 2026-11-13, tenth set): the children's crossings ("Yes, as proposed"), the `SCI` edge ("Accept": a person with an incomplete injury who walks is placed by aid, never under `WHEEL`), and the wording of `LLD`'s description ("Confirm both"; the confirmed text is in `T-102-design.md` section 2). Check: for each of the three, `grep -F "<id> STATUS:" references/project-standards.md | tail -1` reads `ANSWERED BY THE OWNER`.
- **Tests that must be red (or green) before you start:** AT-62 red (restated in section 6). (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-102-mobility-split "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>            # the session stem: bare in the database, with .md for emit_data_migration --session
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-102" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/base.db"   # s.db is the batch's working copy; base.db is never written: the before-runs read it
```
- **Which database each step reads.** Every after-test of section 6 and of `T-102-design.md` section 8 reads `$DB`, never a literal path. Set `DB="$SCRATCH/base.db"` for the before-run, `DB="$SCRATCH/s.db"` for the run on the finished scratch copy (before the write path), and `DB=data/guidebook.db` for the run after `migrate_db.py` has applied the migration. A test run on `data/guidebook.db` before the migration tests the unchanged copy. A probe of a verb uses `--dry-run` on `s.db`; a seeded defect is made on a throwaway copy (`cp "$SCRATCH/s.db" "$SCRATCH/seed.db"`), deleted afterwards.
- **Shell variables do not survive from one tool call to the next in this harness.** Write the stem down once and begin every later command block by setting `BASE`, `STEM`, `SCRATCH` and `DB` again to the same values.
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

1. **Design first (`tasks/T-102-design.md`, committed 2026-11-12).** It proposes `WHEEL` (wheelchair users), `LLD` (people with lower-limb differences; ninth set, replacing the proposed `PROSTH` (people who use a lower-limb prosthesis)) and `WALKAID` (people who use walking aids) under `MOB`, renamed "disabled people with mobility needs"; `device_class` gains `lower_limb_prosthesis`, `crutches`, `cane`; five open edges with recommendations (its sections 2 to 4). Execute it; where this file and the design differ, the design governs. What it was asked to cover, kept for the record:
   - **The children, each with `parent_code = 'MOB'`** (the column exists; no schema change), `MOB` itself kept `active` as the parent. The plan's starting proposal, which the design confirms or corrects with reasons: `WHEEL` (wheelchair users; the 2026-08-25 code, and a constituency a membership organisation names), a prosthetic-device-user code, and an other-mobility-aids code (crutches, canes, walking frames, rollators). Display names in the communities' own words where a self-named community exists (the fourteenth statement), each with its provenance; a code string that is not an initialism of one organisation.
   - **A person with a mobility need who uses no aid** stays on the parent `MOB` and is reached through the ICF d4 codes and the access needs (`A-EFFORT`, `A-STABLE`, `A-REACH`), not given a child, unless the design finds a self-named community for it.
   - **`AMB` of the 2026-08-25 ruling was an open edge, reported, not decided** (since settled by the owner's fifth-set confirmation: `AMB` is not minted; scooter users on `MOB`; ambulatory and part-time wheelchair users in `WHEEL`; `PROSTH` lower-limb only, `LMB` unchanged; then revised: `LLD` replaces `PROSTH`, `LMB` becomes `UPL`): the design says what the device decomposition does to it (absorbed into the other-aids child and the parent, minted as a further child, or retired unminted) and leaves the choice to the owner. The same for three further edges: scooter users (a wheeled device; liminal by the memo's sources), ambulatory and part-time wheelchair users (on both sides of a device line), and the overlap of a prosthetic-device-user code with `LMB` (limb difference), which OD-37 leaves unchanged.
   - **Descriptors, one home each (rule 5):** wheelchair drive (power, manual, attendant, scooter) stays in `device_class` and never becomes a code; the design names the `device_class` values the children need that the CHECK lacks (a prosthesis, crutches, a cane or stick), which T-055 adds. Impairment level (paraplegia, quadriplegia) stays out of the identity lens: the medical lens when a source names it, ICF b-codes for the function it changes. No division is held both as a code and in `device_class`.
   - **Commonality at the parent** (owner, 2026-11-12, second statement): a determination at `MOB` gathers its children by the parent pointer (T-055 builds the gather); a child's determination gathers only that child.
2. **[DISCHARGED 2026-11-12] The report to the owner.** This item asked that the design's section 10 draft be appended to the ledger before any row. The owner confirmed the codes and edges directly on 2026-11-12 (fifth set, "Confirm all as proposed": `grep -n -F "Owner answers 2026-11-12 (fifth set)" references/project-standards.md`), which discharges the report. **Do not append the draft**; it stays in the design as the record of what was put to the owner. If the owner later changes a code, a name or an edge, the design is corrected first and the rows follow the correction.
3. **Add the children** with T-025's `add-identity`, each with its parent and `--approval-ref "Owner answers 2026-11-12 (fifth set) — the T-102 codes, OD-17 (the contract), the display name of a concept (new OD-38), the link-table supersession (new OD-39)"` (the full heading of the fifth-set entry, the confirmation, found exactly once: `git grep -c -F "<heading>" references/project-standards.md` prints 1; each code's provenance is in `T-102-design.md` section 2); rename `MOB` with T-025's `amend-identity`, with the same `--approval-ref` and a `--reason`. **The children's ICF crossings (`T-102-design.md` section 7, item 3) are written:** the owner confirmed them on 2026-11-13 (tenth set, OI-03, "Yes, as proposed": `grep -n -F "OI-03 STATUS" references/project-standards.md`), after the fifth-set line had named only the codes, names and edges. `add-population-icf-link` requires `--mechanism`; take each crossing's mechanism from `T-102-design.md` section 7, item 3, exactly, and never another value. Write these seven before item 4a, so that its duplicate test finds them. The `SCI` crossings that hold for wheelchair users join them under `WHEEL` (item 4a). `LLD`'s description is the text the owner confirmed (OI-49), as `T-102-design.md` section 2 quotes it.
4. **Carry the rows filed under `MOB`, by judgment, row by row**, with T-018's `add-lens-link` and `retire-lens-link` and the decision table of `T-102-design.md` section 6 (a figure's `MOB` code is a live link in `extraction_lens_links` after T-018, not the retired `identity_code` column): a figure whose own words name wheelchair users goes to `WHEEL` (and its drive, if stated, to `device_class`); one naming a lower-limb difference, limb loss or a lower-limb prosthesis to `LLD` (the prosthesis, if named, also to `device_class`); one naming crutches, canes, frames or rollators to the other-aids child; one naming several goes to each through the link table of T-018, never copied. **A figure that names no one takes the group its heading names (OD-31, answered 2026-11-12):** under a mobility heading it stays on the parent `MOB` (the parent is not superseded) and goes to no child, since it names no device; under a general disability heading ("persons with disabilities", "accessible") it carries **no identity** and is carried by its ICF and access-need lenses alone (T-106 fills them; a row may not be left with no lens, by the column CHECK); universal good design is never tagged `ALL` (`ALL` leaves the identity lens: T-056, T-115), and "universal" is stated only by the determination's `design_scale`. Record the heading that decided each such row in the pull request. **A grade of a study's own participants is never fanned out** (the 2026-08-25 ruling): the `MOB` grade stays as the parent-level grade; a new grade against a child is written only where the study's participants are that child. No grade is retired, so `evidence_population_match` needs no retirement column.
4a. **Retire `SCI` to `WHEEL`** (OI-13), by `T-102-design.md` section 6a, in its order: the `SCI` figures carried by judgment, the grade re-graded against `WHEEL` only where its participants are wheelchair users (never fanned out), each `SCI` crossing moved to `WHEEL` or retired by judgment without duplicating a live `WHEEL` row, then `retire-identity --code SCI --to-identity WHEEL` with the `--approval-ref` of `T-102-design.md` section 6a (the seventh-set heading). The caveat (a person with an incomplete injury may walk; level stays in the medical lens and ICF) was accepted by the owner (OI-48, tenth set): such a figure is placed by aid, never under `WHEEL`, and listed. Not every `SCI` figure names wheelchair users (`T-102-design.md` section 6a, item 1, says how the others are warranted). **A crossing is a duplicate if `WHEEL` already holds a live row with the same ICF code, whatever its mechanism**: the table's UNIQUE and the writer's refusal cover only the same mechanism, and a different mechanism is deliberately accepted, so the test is the executor's query of section 6a, item 3, not the writer. Counts today, re-derived through the link table (after T-018 `source_value_extractions.identity_code` is NULL, so a query on it prints 0 having examined nothing): `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(q,c.execute(q).fetchone()[0]) for q in (\"select count(*) from v_live_lens_links where identity_code='SCI'\",\"select count(*) from identity_icf_map where identity_code='SCI' and retired_at is null\",\"select count(*) from evidence_population_match where target_population='SCI'\")])"`. Do not touch `LMB`.
5. **`MOB`'s display name** ("disabled people with mobility needs; wheelchair users") joins two things in one cell; the design proposes a parent name without "wheelchair users", applied by the identity verb.

## 5. Caller sweep

A research task renames nothing and changes no code, so the sweep that applies is the one for prose that restates a fact your rows change (CLAUDE.md rule 7a). For each row id, code or value you change, search the reading surface and the governance prose, and correct a sentence your rows make false (or stop, if correcting it is not research):

```
V='<the id, code or value you changed>'
git grep -n -w -F -e "$V" -- governance architecture CLAUDE.md skills                    # read row by row
git grep -l -w -F -e "$V" -- references ':(exclude)references/project-standards.md' ':(exclude)references/search-log' | wc -l   # count only
```

**Why two commands** (2026-11-13, from the pilot). A bare two- or three-letter code matches far too many files to read as a caller list. Most of the hits for `MOB` and `SCI` are the prior version's corpus under `references/`, which uses the codes as labels (`bpc/`, `connections/`, `audits/`). Read the first command's hits one by one. For `references/`, record the count, and read only the hits for the exact strings that state a fact your rows change: `MOB`'s old display name, `MOB/AMB`, `MOB/UPL`, and a sentence stating `SCI`'s status. The rest are mentions.

**A known caller that is doctrine, listed and not edited.** `governance/population-taxonomy.md` names `MOB/AMB` and `MOB/UPL` as `MOB`'s sub-codes (`grep -n 'MOB/AMB' governance/population-taxonomy.md`), and says "a sub-code inherits all evidence from its parent" (`grep -n -F 'inherits all evidence from its parent' governance/population-taxonomy.md`). The design goes the other way: the parent gathers its children, and a child gathers only itself. That file is population taxonomy, which is doctrine and the owner's (section 8). List it in the pull request with the open edge E6 of `T-102-design.md` section 3. Change nothing in it beyond the one-line pointer the design's section 11 allows. It blocks no row of this task, because this task writes no determination.

Structures this task touches, for orientation: `MOB`, `SCI` (retired to `WHEEL`), `identity_icf_map`, `evidence_population_match`. The ledger (`references/project-standards.md`), `sessions/` and committed migrations are records and are never edited.

## 6. Verification

**Red before, green after.** AT-62, restated for the device decomposition. Run each test three times, on `$DB` set as section 2 says: on `base.db` (before), on `s.db` (the finished scratch copy, before the write path), and on `data/guidebook.db` once the migration is applied. The commands are in `T-102-design.md` section 8; each reads `$DB`.
(1) the children named in the design exist with `parent_code = 'MOB'` and `MOB` is `active`: `select identity_code, parent_code, status from base_taxonomy_identity where category='mobility' or parent_code='MOB'`;
(2) the owner's confirmation of the codes exists (it precedes the rows by construction): `grep -n -F "OD-14: codes confirmed as proposed in T-102-design.md" references/project-standards.md` prints one line, and no draft report was appended: `grep -c -F "the mobility codes as designed (T-102)" references/project-standards.md` prints 0;
(3) no figure linked to `MOB` names a child's device or group in its own words unless it also carries that child, and no judged `MOB` link is warranted by words naming a child's device: `T-102-design.md` section 8, test 3, read through `v_live_lens_links` (after T-018 the `identity_code` column is NULL, so a query on it prints 0 having examined nothing). It prints a non-zero `EXAMINED`. The expected value is not 0 by fiat: the design keeps a judged `MOB` link beside a child's link where a figure also names a group that stays on the parent (scooter users, E2; a mobility group with no device). The test therefore counts only the figures that are wrong under the design's own table. It must print `defects: 0`, or a number equal to the rows the pull request lists with their reasons. On `base.db` it is red (no child exists);
(4) no grade was fanned out: `select count(*) from evidence_population_match where target_population='MOB'` prints the same on `base.db` and on `$DB`, and every new child grade names its participants;
(4a) `SCI` carried and retired: tests 1, 9 and 10 of `T-102-design.md` section 8;
(5) no division is held twice: `MOB`'s display name holds one thing (no `;`, and no child's device or group), and no display name or description in the family names a wheelchair drive or an impairment level (`T-102-design.md` section 8, test 5; `SCI`'s description is outside the family and reported, not changed). It is red on `base.db`, where `MOB`'s name still reads "…; wheelchair users". Prove the second half can go red with the seeded defect that test 5 describes; and tests 6 to 8 of that section.

**Fixtures.** Before-runs read `$SCRATCH/base.db`; probes of a verb run with `--dry-run` on `$SCRATCH/s.db`; a seeded defect is made on `$SCRATCH/seed.db` and deleted; the batch's own rows are written on `$SCRATCH/s.db` and reach `data/guidebook.db` only through the write path of section 2.

**The gates, once each:**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8   # the research gate
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run each once, after the migration is applied and before the commit.** `preflight.sh` runs the selftest and `run_checks.py --changed-from`; do not run `run_checks.py` separately, and never `--all`.
- **Proof that each gate examined something.** A check scoped to a session id that matches no row passes having read nothing. Confirm the stem is the one stored on your rows. The five tables this task writes do not share their stamp columns: `base_taxonomy_identity` has no session column at all, while `identity_icf_map` and `evidence_population_match` have `created_by_session` but no `updated_by_session`, so one query for every table raises `no such column` (pilot, 2026-11-13). Read each table's own `*_by_session` columns:
```
grep -o -E '^(INSERT INTO|UPDATE) "[a-z_]+"' "$SCRATCH/batch.sql" | sort | uniq -c     # the tables the batch writes
python3 -I - "$DB" "$STEM" <<'PY'
import sqlite3, sys
c = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True); s = sys.argv[2]
for t in ("base_taxonomy_identity", "identity_icf_map", "evidence_population_match", "source_value_extractions", "extraction_lens_links"):
    cols = [r[1] for r in c.execute(f'pragma table_info("{t}")') if r[1].endswith("_by_session")]
    if not cols:
        print(t, "NO SESSION COLUMN"); continue
    print(t, cols, c.execute(f'select count(*) from "{t}" where ' + " or ".join(f"{x}=?" for x in cols), [s] * len(cols)).fetchone()[0])
PY
```
  Every table the first command lists, except `base_taxonomy_identity`, must print a count above 0. `base_taxonomy_identity` prints `NO SESSION COLUMN`, so no session-scoped gate sees its rows: test (1) is their proof. `research_batch_dod` prints its own `EXAMINED:` lines: read them in `dod.txt`.
- **The research gate is red by construction for this batch** (pilot, 2026-11-13). This batch searches nothing and admits nothing. It carries held figures by judgment. `research_batch_dod.py --session` therefore fails three rules whatever the rows: **R1** (no Co-1/T2/Co-2 pass), and **R9a** and **R9b** ("this batch admitted no sources AND logged no searches"). The other rules pass, examining nothing. The research contract (`governance/research-contract.yaml`) provides no reading for a batch that searches nothing. R1's only waiver, `CO1-NOT-APPLICABLE: <reason>`, lives in `search_executions.findings_note`, so it needs a search row, which this batch has none of. R9a and R9b treat a session with neither admissions nor searches as untouched or misnamed, and the registry runs them as the **blocking** `research_dod_session` on whichever session `sessions/LATEST-RESEARCH` names. So: run the gate first on the finished scratch copy, before the write path (`GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/audit/research_batch_dod.py --session "$STEM"`; the script reads that variable). **Any rule red other than R1, R9a or R9b is a defect in your rows: repair it.** If exactly those three are red, with those messages, stop there, before `emit_data_migration.py` (section 9), unless the ledger by then carries the owner's answer to the question below. If it does, follow it, and cite it in the pull request. Report the output, and the owner question: how is a carry-only batch gated? Do not log a search, real or reconstructed, to obtain a waiver, and do not move `LATEST-RESEARCH` to this session. A passing check prints no `EXAMINED:` line in `gate.txt`; any check under `NOTHING-IN-SCOPE` there has not passed. `migration_reproducibility` compares row counts only, so an UPDATE is invisible to it: also run `python3 scripts/audit/migration_reproducibility.py --deep`, which compares every row.

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
- Do not author a specification row (`specifications`, read through `v_best_practice`; CLAUDE.md §6's `best_practice_synthesis` names a table not in the schema: superseded in part by TERM-RESOLUTION-PLAN §2, 2026-11-14) or synthesis prose below the Opus floor.
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
- the tooling check of section 2 prints anything but what it says: the emitter does not write a table's UPDATEs before its INSERTs, T018-08 is not `[✓]`, or a line prints `False` (T-054 absent included);
- `research_batch_dod.py`, run on the scratch copy, is red on exactly R1, R9a and R9b, and the ledger carries no owner answer on how a batch that searches and admits nothing is gated (section 6). That is a question about the research contract, which is the owner's: stop before the write path and report it;
- a figure's placement turns on a doctrine question that `T-102-design.md` section 3 lists as open (E6: a child inheriting its parent's evidence; E7: the mechanism of a new crossing), and the design's table does not settle that row. List the row and leave its carried link. Neither question blocks a row the table settles.

## 10. Rollback

Before the migration is applied: delete the scratch copy; nothing has changed. After it is committed: a data migration is append-only and immutable; correct a wrong row with a compensating migration written through the same verbs (retire, supersede, amend), never by editing or deleting the file.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished. Its first line is the research gate, which is red by construction for this batch until the owner answers the question in section 6. Reaching this step means that answer is in the ledger: apply it here as well.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
