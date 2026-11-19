# T-138  The lens and figure writers refuse what the rulings forbid, a withdrawn figure's pair is owed again, and the regulatory stratum has one home

_One task of a stacked pull request (owner instruction of 2026-11-15: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). Read `CLAUDE.md` first; beyond it this file is self-contained. Why this task exists, and the options it chose between: `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md`, items 17, 19, 20, 21, 22, 23 and 24 (section 3), the limit of item 86 ("`repoint-extraction-relation` gains the retired-figure refusal … repaired with item 21's tooling", section 3, items 79 to 91) and section 4 item 4, ratified by the owner (`grep -n -F "## Owner ratification 2026-11-19" references/project-standards.md`). Every number in this file was read on 2026-11-19 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-19 by an Opus-class task author from the ratified third adjudication; its evidence commands were run read-only on 2026-11-19 against branch `ccr-cc893571-i4lug4` at `a6c478e0` (schema version 159) and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-138 |
| Title | The lens and figure writers refuse what the rulings forbid, a withdrawn figure's pair is owed again, and the regulatory stratum has one home |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10); one schema migration (`v_scan_ledger`, `v_reading_owed` recreated), refusals in `scripts/db.py`, `scripts/audit/scan_debt.py`, one constant moved to `scripts/dbcore.py`, a dated amendment line in `tasks/T-056-all-leaves-identity-lens.md` |
| Executor | NOT FOR SONNET: Opus-class. Seven refusals or derivations whose meaning the task fixes (which warrant a lens link may claim, when a figure's lens is frozen, when a withdrawn reading is owed, when a merge or a kind is refused) |
| Traces to | OD-31 (owner: "Heading's group; ALL leaves the identity lens"), OD-48 (owner, ratified 2026-11-19: `universal` states whom a determination is for), OD-65 (owner: the `context` basis), OD-23 (owner: "We can flag a source to be read again"), OD-24 (delegated: two cases are two parameters when "they cannot be placed on one scale"), OI-55 (7); the T-126, T-078 and T-083 sweep items (`scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/sweep-list.md` lines 91, 92, 121, 123, 130, 150, 151, 158) |

## 2. Preconditions

- **The integration base.** On this stacked batch the earlier tasks are commits on the batch's branch (`ccr-cc893571-i4lug4`); a task named below is merged if its commit is on `HEAD` or on `origin/main`. The set-up block sets `$BASE` (preconditions only) and records `BASE_PRE` (every diff, gate and count).
- **Tasks that must be merged to the integration base first:** T-126, T-078 and T-083, with their repairs. Check by subject: `git log --oneline HEAD | grep -F -e "repair T-126 after the adversarial pass" -e "repair T-078 after the adversarial pass" -e "repair T-083 after the adversarial pass"` prints three lines. If T-136 or T-137 is also on the branch, derive your migration number after it.
- **Owner decisions:** OD-31, OD-48, OD-65 and OD-23, answered by the owner.
- **Delegated resolutions this task rests on:** OD-24, read only through the gate of the convention of 2026-11-12 (`grep -n -F "## Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). Run before you start and again before you commit; anything but OPEN is a stop:
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-31 OD-48 OD-65 OD-23 OD-24; do gate $n; done
grep -c -F "## Owner ratification 2026-11-19 — the third adjudication" references/project-standards.md
```
  Printed on 2026-11-19: `OD-31 OPEN (owner)`, `OD-48 OPEN (owner)`, `OD-65 OPEN (owner)`, `OD-23 OPEN (owner)`, `OD-24 OPEN (delegated; not required)`, `1`. Items 17 and 19 to 24 carry no OD number; they are ratified by reference (the last line must print `1`). If a later entry narrows the ratification (its ACTION (3): "the breadth of 'all' is the first to confirm"), stop.
- **Tests that must be red before you start:** `T138-01`, `T138-03`, `T138-05`, `T138-08`, `T138-11`, `T138-12`, `T138-14` (section 6).
- **Set-up** (stacked-branch convention, `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 1):

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-138" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
git rev-parse HEAD > "$SCRATCH/base_pre"; sha256sum data/guidebook.db | tee "$SCRATCH/db.sha"   # no git switch -c: stay on the batch's branch
```
- **Shell variables do not survive between tool calls.** Begin every later block with the `export SCRATCH=…` line and `BASE_PRE=$(cat "$SCRATCH/base_pre")`; pass `GUIDEBOOK_DB_PATH="$SCRATCH/t.db"` inline on every probe, under `--session session_task-probe` (never the running session; never delete `refusals.jsonl`). `/session-open` and `scratchpad/CURRENT` are the coordinator's.

## 3. The problem, in the guidebook's terms

A figure is stated "for" groups of disabled people through lens links, and a determination is computed from the figures in its lens. Five writers still let that record say less than the rulings require. `ALL` (a scope marker the owner removed from the identity lens) is refused only under the `context` basis. A session may record a link as its own judgment (`context`) when the clause it rests on already says so, so a checkable warrant is stored as an uncheckable one. A lens link can be added to or retired from a figure that a live determination was computed from, so the stored determination silently stops matching its evidence. A figure withdrawn as a misreading leaves its pair reading "read in full, nothing found", which is false, and nothing asks for the source to be read again. `set-parameter-kind` is blocked by an open determination gate (a later stage's question ordering a base fact), while `merge-parameter` lets a parameter of one quantity be folded into a parameter of another or of none. `repoint-extraction-relation` points an edge at a withdrawn figure. And "the regulatory stratum" (tiers 4 to 6) is a literal `4` in several places, so a change to the tier ladder would move some readers and not others.

**Evidence commands** (read-only):

```
grep -n -F 'if basis == "context" and "ALL"' scripts/db.py | cut -c1-8
for f in add_lens_link retire_lens_link repoint_extraction_relation merge_parameter; do printf "$f "; awk "/^def $f\(/{p=1;next} p&&/^def /{exit} p" scripts/db.py | grep -c -E "live_determinations_linked|_refuse_retired_figure|quantity_kind"; done
grep -n -F 'gate_why="must be resolved before the parameter is given its kind' scripts/db.py | cut -c1-8
git grep -n -E "tier.{0,40}(>=|<) ?4\b" -- scripts ':(exclude)scripts/migrations' ':(exclude)scripts/tests' | cut -d: -f1,2
python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print('retired_at IS NOT NULL' in c.execute(\"select sql from sqlite_master where name='v_scan_ledger'\").fetchone()[0])
print(c.execute('select count(*) from source_value_extractions where retired_at is not null').fetchone(), c.execute('select count(*) from specifications where retired_at is null').fetchone(), c.execute('select gate_id,parameter_id,verdict from determination_gates where resolved_at is null').fetchall(), c.execute(\"select basis,count(*) from extraction_lens_links where identity_code='ALL' and retired_at is null group by 1\").fetchall(), c.execute(\"select count(*) from base_parameters where status='merged'\").fetchone())"
```

**Printed on 2026-11-19:** `11284:` (the one `ALL` refusal, `context` only); `add_lens_link 0`, `retire_lens_link 0`, `repoint_extraction_relation 0`, `merge_parameter 0` (none reads a live determination, a retired figure or a kind); `7866:` (the gate refusal on `set-parameter-kind`); tier literals at `scripts/audit/research_batch_dod.py` lines 379, 384, 395 and 1382 (395 is code, the rest comments) and `scripts/db.py` lines 6756, 10847 and 11741, beside the named constant `_REGULATORY_FROM_TIER` (`grep -n _REGULATORY_FROM_TIER scripts/db.py`); `False` (the ledger never reads a retired figure); `(0,) (0,) [(1, 3, 'UNLINKED')] [('carried', 34)] (0,)`: no figure is retired, no determination is live, one gate is open, 34 live `ALL` identity links are all `carried` (T-115's, not this task's), and no parameter is merged. This agrees with the adjudication (items 20, 21, 23, 24). Every subject of items 21, 22 and 24 is empty today, so each is proven on a fixture: say so in your report.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. Every refusal names the next act and writes nothing.

**Seven items, each its own test group (section 6). Do them in this order. You may stop after any complete item (its code, its callers swept, its tests red then green, its after-run clean) and report what is done and what is not; do not commit a half-built item.**

1. **`ALL` is refused under every basis (item 20; T-056 part 1).** `_refuse_all_by_context` becomes a refusal of `ALL` as an identity under every basis a writer may state (the basis CHECK minus `carried`, `_lens_basis_choices()`), renamed for what it does; its three callers (`add-extraction`, `derive-extraction`, `add-lens-link`) are unchanged in shape. The message cites OD-31 and says that universality is stated once, by the determination's `design_scale` (OD-48, ratified: whom it is for), and that a provision naming no one is carried by its ICF and access-need lenses. The 34 stored `carried` links stay (T-115 moves them). Append to `workplan/2026-11-12-bidirectional-pipeline/tasks/T-056-all-leaves-identity-lens.md`, after its last line, this dated line and nothing else:

   > **Amended 2026-11-19 (third adjudication item 20, ratified 2026-11-19):** T-056 is split. Part 1, built by T-138: `add-extraction`, `derive-extraction` and `add-lens-link` refuse `ALL` as an identity under every basis a writer states. This task keeps item 1 (the retirement mechanism), item 2's general refusal through `retire-identity` and the deletion of the `add-conflict` special case, items 3 and 3a (the engine; OD-48 is answered: (a), whom it is for) and item 5.

2. **`context` is refused where the clause states it (item 19).** In `_require_lens_warrant`, basis `context`: when the warrant words are found on word boundaries in the figure's own `claim_text` (the clause), refuse, naming `--basis named_in_text` with the same words as the next act ("provenance demands the strongest warrant the words support"). **The reading this file takes, stated so it can be disputed:** the adjudication says "when the same code would pass the `named_in_text` test"; that test also accepts words found anywhere in a file saved for the source, and applying that half would refuse every `context` link resting on a scope, application or purpose clause (the very use OD-65 made `context` for). The question it answers is "the clause itself names the group", so only the clause (`claim_text`) is read. **Residual, stated in the docstring:** a session that quotes other words while the clause names the group (the critic's "wheelchair" case) still passes, because whether words name a group is the judge's (D-2) and the registries hold no name for every code; the adversarial pass reads `basis_text` and `basis_reason`. A superseded source's figure is not a lens question (adjudication item 19): change nothing for it.
3. **A lens does not change under a live determination (item 21, OI-55 (7)), and no edge points at a withdrawn figure (item 86).** `add-lens-link` and `retire-lens-link` refuse while `dbcore.live_determinations_linked(conn, extraction_id)` is non-empty, naming each determination and the walk back: `retire-specification`, then the link change, then re-determine (the pattern `retire-extraction` already uses). `repoint-extraction-relation` calls `_refuse_retired_figure` on both ends, as `relate-extraction` does.
4. **A withdrawn figure's pair is owed until it is read again in full (item 22).** One schema migration (number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`, plus one; `scripts/migrations/NNN_withdrawn_pair_owed.sql`, ending `PRAGMA user_version = NNN`) recreates `v_scan_ledger` from its CURRENT text in `sqlite_master` (migration 158 set it) with one new status, `WITHDRAWN-NOT-REREAD`, placed after `STATED-ABSENT` and before `READ-NOTHING-FOUND`: the pair has no live figure, at least one retired figure, and no **full-scope** covering reading (the ledger's own coverage rule) whose `created_at` is later than the latest `retired_at` of the pair's figures. Strictly later: the two columns share the minute stamp of `dbcore.now()`, so a reading in the same minute as the withdrawal owes (the safe side; say so in the header). Full scope, not any reading: a partial reading cannot say a quantity is absent (the reason `scan_debt.py` gives for `READ-PARTIAL`), and the adjudication's "no reading recorded after the retirement" would otherwise let a later abstract reading turn the pair back into `READ-NOTHING-FOUND` through the old full reading. Derived from timestamps only; never parse `retirement_reason`. Extend the header's precedence list and its "WHY THIS ORDER". Recreate `v_reading_owed` (it reads `COALESCE(text_scope, '') <> 'full'`, which a withdrawn pair with an old full reading passes, so it would refuse a deferral of a pair that is owed) to owe `WITHDRAWN-NOT-REREAD` too; `v_deferred_acts` reads it unchanged. In `scripts/audit/scan_debt.py` the status is debt (`DEBT`, the printed status list, the docstring), and `--reread` routes it (the source was read in full once, so it takes the inventory, retained-text or re-read route, OD-23's flag). In `db.py cell-status`, add the status to the `owed` bucket under its own key, so no pair drops out of every bucket. Every other reader the sweep finds that lists statuses gains it or is shown not to need it.
5. **An open gate no longer blocks a kind (item 23).** `set-parameter-kind` asks `_refuse_live_work` for live determinations only (a keyword that skips the gate query; the gate refusal stays for `retire-parameter` and `merge-parameter`, which it protects, adjudication item 71 (a)). Declaring a NULL kind names the quantity the parameter already measures and leaves the gate's question intact. Remove the `gate_why` text that is then unread.
6. **A merge keeps one quantity (item 24, OD-24).** `merge-parameter` refuses when the two parameters' `quantity_kind` differ, NULL against a kind included (`IS NOT`): when one is NULL, name `set-parameter-kind` on it with the other's kind first; when both are set and differ, say they are two quantities and so two parameters (OD-24), and name no route (a kind is write-once). Read the kinds with `_parameter_row` (extend its SELECT) before any re-point. The reshaping of the merge to T-129's form (OI-78) is not this task.
7. **One home for the regulatory stratum (item 17).** Move `_REGULATORY_FROM_TIER` from `scripts/db.py` to `scripts/dbcore.py` as `REGULATORY_FROM_TIER`, its comment naming `governance/tier-system.md` rows T4 to T6 as the ratified definition (it applies a tier definition; it does not set one). Every comparison of a tier against a literal `4` in `scripts/` outside tests and migrations reads it (the code lines of section 3's grep, `_regulatory_pairs`, `_warn_identity_omitted`, `_require_lens_warrant`, `scripts/audit/code_value_identity_audit.py`, `scripts/audit/research_batch_dod.py`), and the comments of `research_batch_dod.py` stop stating the number. The engine's tier buckets (`t in (4, 5)`, `t == 6` in `assess_cell.py`) partition the stratum, not bound it, and changing the engine moves `RULE_VERSION`: leave them, and name them in your report.

**What reads what this task adds:** the refusals: the writers' callers (the run-pipeline skill's steps, research batches). `WITHDRAWN-NOT-REREAD`: `scan_debt.py` (and its `--reread` worklist), `v_reading_owed` (so `defer-reading` and `v_deferred_acts`), `cell-status`. `dbcore.REGULATORY_FROM_TIER`: every tier comparison named above. **Without this task**, a determination can stand on a lens its evidence no longer has; a group is stated "for everyone" by a marker the owner removed; a misread figure's source reads as examined and empty; a merged parameter's figures sit under another quantity; and a change to the tier ladder moves some readers and not others.

**Not in this task (plan edits the coordinator makes, adjudication section 4 item 13):** the T-078, T-083 and T-109 file amendments. Not here either: T-056's engine, the `add-conflict` refusal, the `context` tier floor's exception for a clause naming no one (OD-47's follow-on).

**Migration discipline (item 4).** Apply only with `python3 scripts/migrate_db.py`; prove with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). No `data_*` file. Then `python3 scripts/generate/context_map.py` and include `governance/context-map.yaml` if it changed.

**Code size.** Report `git diff --shortstat "$BASE_PRE" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`); name what each addition reads and what it replaces (the literal `4`s, the gate branch of `set-parameter-kind`).

## 5. Caller sweep

Names to sweep: `_refuse_all_by_context`, `ALL by basis`, `_require_lens_warrant`, `add-lens-link`, `retire-lens-link`, `repoint-extraction-relation`, `v_scan_ledger`, `v_reading_owed`, `READ-NOTHING-FOUND`, `DEBT`, `set-parameter-kind`, `_refuse_live_work`, `merge-parameter`, `_REGULATORY_FROM_TIER`, `regulatory stratum`.

A caller is a hit whose behaviour or truth changes (code, a test exercising it, a view, index or trigger, a registry entry, a skill or governance sentence stating it); a hit that stays true is a mention. **Fixing a caller is in scope** (rule 4). Left out: `workplan/` except `machines.yaml` and the T-056 line, the ledger, `scripts/migrations/`, and the frozen records.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
New refusal texts and a view change: run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference (`machines.yaml` names `add-lens-link`, `retire-lens-link`, `set-parameter-kind` and `merge-parameter`: `grep -c -F -e add-lens-link -e merge-parameter workplan/pipeline-state-graph/machines.yaml`; read each transition and correct any that states a changed guard).

**Callers found on 2026-11-19** (each in scope; re-run): `scripts/db.py` (the functions named in section 4, `cell_status` and its docstring at the ledger precedence list, `_parameter_row`); `scripts/dbcore.py`; `scripts/audit/scan_debt.py`, `scripts/audit/code_value_identity_audit.py`, `scripts/audit/research_batch_dod.py`, and the other readers of `v_scan_ledger` (`scripts/audit/verified_scan_integrity.py`, `scripts/audit/skill_vocabulary_audit.py`: read whether they list statuses); views `v_scan_ledger`, `v_reading_owed` (and `v_deferred_acts`, which reads it, and `source_scans`, whose DDL comment names the ledger: mentions unless a sentence changes); tests `scripts/tests/test_db_amend_writers.py` (T-126 cases accepting `ALL` under `named_in_text` or `heading`, T-083's `T083-04` asserting the gate refusal, the test reading `db._REGULATORY_FROM_TIER`), `scripts/tests/test_run_pipeline_refusals.py` (the cases enumerating ledger statuses, and `cell-status` bucket sums), `scripts/tests/test_scan_contract.py` (ledger status cases); skills `skills/run-pipeline_SKILL.md` (ledger statuses, the lens bases, `set-parameter-kind`); prose `governance/pipeline-contract.yaml` (ledger and stratum sentences), `governance/context-map.yaml` (regenerated). A test that asserted a refusal this task removes (the gate on a kind) is a caller updated to the ruled behaviour, named in the commit body.

## 6. Verification

**Step 1, before any edit: the before-run.** Checks that read what this task touches: `test_db_amend_writers test_run_pipeline_refusals test_scan_contract test_db_integrity code_value_identity_audit scan_debt verified_scan_integrity schema_reference_audit derived_not_curated_audit migration_reproducibility context_map_fresh`.

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-138"
CHECKS="test_db_amend_writers test_run_pipeline_refusals test_scan_contract test_db_integrity code_value_identity_audit scan_debt verified_scan_integrity schema_reference_audit derived_not_curated_audit migration_reproducibility context_map_fresh"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
A check red here was red before you touched anything: record it (`scan_debt` is red whenever debt exists, by design). No `EXAMINED:` line, or `EXAMINED: 0`, means it examined nothing: say so.

**Step 2: red before, green after, one group per item.** Case ids `T138-NN` (`git grep -c '"T138-' -- scripts/tests` printed nothing on 2026-11-19), in `scripts/tests/test_db_amend_writers.py` beside the T-126 and T-078 cases (items 1 to 6) and in the same file for item 7. A live determination is built as the G04 fixture of that file builds one (it un-retires a determination on the test's scratch copy; derive it by query); a retired figure, a full reading and a later reading are built with the writers on the scratch copy, labelled `TASK-FIXTURE`. Never type an id, code, tier or count the database can derive. Show each case red on a seeded defect you then remove (restore byte for byte; `cmp`).

| Item | Case | Red before (or the seeded defect) | Green after |
|---|---|---|---|
| 1 | T138-01 | `add-lens-link --identity ALL --basis named_in_text` with found words is accepted | refused under `named_in_text` and `heading` on all three writers, naming `design_scale`; nothing written |
| 1 | T138-02 | seeded: restore the `context`-only condition | a non-`ALL` identity under `named_in_text` still passes (a probe no other refusal stops); the T-056 line is present (`grep -c -F "Amended 2026-11-19 (third adjudication item 20"` prints 1) |
| 2 | T138-03 | `context` with words found in the figure's `claim_text` is accepted | refused naming `--basis named_in_text` |
| 2 | T138-04 | seeded: read `source_section` or the saved file too | `context` with words found only in a saved file (a scope clause) or only in `source_section` still passes |
| 3 | T138-05 | `add-lens-link` on a figure a live determination links succeeds | refused naming the determination and `retire-specification`; the same for `retire-lens-link` |
| 3 | T138-06 | seeded: test `governing_only=True` | a figure linked only `excluded` to a live cell is refused too (the helper's own "linked" meaning); with the determination retired both verbs pass |
| 3 | T138-07 | seeded: drop the new call | `repoint-extraction-relation` to or from a retired figure is refused, nothing written |
| 4 | T138-08 | a pair whose only figure is retired, read in full before the retirement, reads `READ-NOTHING-FOUND` | it reads `WITHDRAWN-NOT-REREAD`; `scan_debt.py` counts it as debt and `--reread` routes it; `v_reading_owed` holds it; `cell-status` lists it under `owed` |
| 4 | T138-09 | seeded: use `>=`, or any scope | a later partial reading leaves it owed; a later full reading makes it `READ-NOTHING-FOUND`; a reading in the same minute as the retirement leaves it owed |
| 4 | T138-10 | seeded: drop the "no live figure" condition | a pair with one live and one retired figure reads `EXTRACTED`; every other ledger row is unchanged (compare the whole view before and after on the canonical copy: no figure is retired there, so the two must be equal row for row) |
| 5 | T138-11 | `set-parameter-kind` on the parameter with the open gate (derive it by query) is refused | it writes the kind; the gate is still open; with a live determination built as G04 builds one it is still refused |
| 6 | T138-12 | merging a parameter with a kind into one without (fixtures) succeeds | refused naming `set-parameter-kind`; two different kinds refused naming OD-24; equal kinds pass; the refusal precedes any re-point (row hashes unchanged) |
| 6 | T138-13 | seeded: compare with `!=` (NULL passes) | NULL against a kind is refused |
| 7 | T138-14 | the grep of section 3 finds code comparing a tier with a literal `4` | it finds none outside `dbcore.REGULATORY_FROM_TIER`'s definition (scan the code lines of `scripts/`, tests and migrations excluded); seeded: re-type one `>= 4` |

**Step 3, after the change: the after-run.** The same loop with `after-`; compare check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before, except a case asserting a behaviour this task changes by ruling, updated and named.

**Step 4: the gate, once**, when every edit is made, in the background with a long timeout, waiting with an until-loop on its output file:

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-138"; BASE_PRE=$(cat "$SCRATCH/base_pre")
scripts/preflight.sh --base "$BASE_PRE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Read the `RESULT` line, any `NOTHING-IN-SCOPE` (not a pass), any blocking `FAIL`; a FAIL red on the base is not yours (run its `cmd` once on `$BASE_PRE` in a worktree and give both lines).

## 7. Commit

After the gate is clean, staged with `git add -A . ':!transcripts' ':!*commands.jsonl' ':!.claude/worktrees'` (check `git status`):
```
git commit -m "governance: lens and figure writers refuse what the rulings forbid, a withdrawn figure's pair is owed again, and the regulatory stratum has one home [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the items done (and any not done), the evidence before and after, each caller and what was done, the reading of item 19>" -m "<the attribution trailers your session instructions give>"
```
If you stopped after a complete item, say which in the subject's body and list the items left.

## 8. What you must NOT do

- Do not write `data/guidebook.db` except through `scripts/migrate_db.py`; do not move or retire the 34 `carried` `ALL` links, or any row (rule 10; T-115's).
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`; do not push, open a pull request, subscribe, run `/adversarial` or `/batch-done`.
- Do not parse `retirement_reason`, build a list of group names, or grade a `basis_reason` (adjudication item 18: no mechanical rule).
- Do not change the engine, its tier buckets or `RULE_VERSION`; do not touch T-056's engine items, `retire-identity` or `add-conflict`.
- Do not remove the gate refusal from `retire-parameter` or `merge-parameter`.
- Do not add a table, column, flag, status or verb that section 4 does not name; list any helper you add. Fixing a caller is in scope.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level. The one refusal section 4 narrows (the gate on `set-parameter-kind`) is narrowed by the ratified item 23.
- Do not hand-type a count into any file or message.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, saw and expected) when:
- a precondition of section 2 is not met, or the gate prints anything but OPEN, or a later ledger entry narrows the ratification;
- an evidence command of section 3 prints otherwise (in particular: a retired figure, a live determination or a merged parameter exists, which turns a fixture-only proof into a live change to read first);
- the coordinator or the owner reads item 19 as the full `named_in_text` test (saved file included): the reading of section 4 item 2 is then wrong, and the file is rewritten first;
- a red test is not red before or not green after one honest attempt;
- the sweep finds a caller you cannot repair without adding something section 4 does not name (for instance a reader that would need a new status bucket this file does not name);
- a check green in the before-run is red after, other than a case asserting a behaviour section 4 changes by ruling;
- `migrate_db.py --rebuild` does not reproduce the database, or the ledger's rows change on the canonical copy (T138-10);
- you would have to guess a value, a code, a group or an owner's intent.

## 10. Rollback

Before merge: the coordinator drops the commit from the stack. After merge: `git revert` in a new pull request. A committed migration is never edited: fix forward with a compensating migration (rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

On this stack the coordinator runs `/adversarial` on your commit and sends any repair; `/batch-done`, the push, the one pull request and the immediate `unsubscribe_pr_activity` are the coordinator's. Report per `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 3, with a heading "Task-file defects".
