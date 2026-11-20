# T-138  The lens and figure writers refuse what the rulings forbid, a withdrawn figure's pair is owed again, and the regulatory stratum has one home

_One task of a stacked pull request (owner instruction of 2026-11-15: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). The ratification entry of 2026-11-19 says "each its own pull request" in its ACTION (2); those are the recorder's words, the owner's instruction of 2026-11-15 is stacked, and the stack stands. Read `CLAUDE.md` first; beyond it this file is self-contained. Why, and the options weighed: `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md`, items 17, 19, 20, 21, 22, 23 and 24 (section 3), the limit of item 86 ("`repoint-extraction-relation` gains the retired-figure refusal … repaired with item 21's tooling", section 3, items 79 to 91) and section 4 item 4, ratified by the owner (`grep -n -F "## Owner ratification 2026-11-19" references/project-standards.md`). Every number was read on 2026-11-19 with the command that produces it: re-run it._

**Pilot status.** Not piloted. Authored 2026-11-19 from the ratified adjudication; evidence run read-only at `a6c478e0` (schema 159). Expect a defect in this file; report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-138 |
| Title | The lens and figure writers refuse what the rulings forbid, a withdrawn figure's pair is owed again, and the regulatory stratum has one home |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (rule 10); one schema migration (two views recreated), refusals in `scripts/db.py`, `scan_debt.py`, one constant moved to `dbcore.py`, a dated line in T-056 |
| Executor | NOT FOR SONNET: Opus-class: which warrant a link may claim, when a lens is frozen, when a withdrawn reading is owed, when a merge or a kind is refused |
| Traces to | OD-31, OD-48 (ratified: `universal` states whom a determination is for), OD-65 (`context`), OD-23 ("We can flag a source to be read again"), OD-24 (delegated), OI-55 (7); sweep list lines 91, 92, 121, 123, 130, 150, 151, 158 (`scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/sweep-list.md`) |

## 2. Preconditions

- **The integration base.** A task named below is merged if its commit is on `HEAD` (the batch's branch) or on `origin/main`. `$BASE` serves preconditions only; `BASE_PRE` every diff, gate and count.
- **Tasks that must be merged to the integration base first:** T-126, T-078 and T-083, with their repairs. Check by subject: `git log --oneline HEAD | grep -F -e "repair T-126 after the adversarial pass" -e "repair T-078 after the adversarial pass" -e "repair T-083 after the adversarial pass"` prints three lines. If T-136 or T-137 is also on the branch, derive your migration number after it.
- **Owner decisions:** OD-31, OD-48, OD-65 and OD-23, answered by the owner.
- **Delegated resolutions this task rests on:** OD-24, read through the gate of the convention of 2026-11-12, before you start and before you commit; anything but OPEN is a stop:
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-31 OD-48 OD-65 OD-23 OD-24; do gate $n; done
grep -c -F "## Owner ratification 2026-11-19 — the third adjudication" references/project-standards.md
```
  Printed on 2026-11-19: `OD-31 OPEN (owner)`, `OD-48 OPEN (owner)`, `OD-65 OPEN (owner)`, `OD-23 OPEN (owner)`, `OD-24 OPEN (delegated; not required)`, `1`. Items 17 and 19 to 24 carry no OD number; they are ratified by reference (the last line must print `1`). If a later entry narrows "Ratify all", stop.
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
- **Shell variables do not survive between calls:** begin each block with the `export SCRATCH=…` line and `BASE_PRE=$(cat "$SCRATCH/base_pre")`; probe with `GUIDEBOOK_DB_PATH="$SCRATCH/t.db"` inline and `--session session_task-probe`; never delete `refusals.jsonl`. `/session-open` is the coordinator's.

## 3. The problem, in the guidebook's terms

A figure is stated "for" groups of disabled people through lens links; a determination is computed from the figures in its lens. `ALL` (a scope marker the owner removed from the identity lens) is refused only under `context`. A session may record as its own judgment (`context`) a link the clause already names, storing a checkable warrant as an uncheckable one. A lens link can change under a figure a live determination was computed from. A figure withdrawn as a misreading leaves its pair reading "read in full, nothing found", and nothing asks for a re-read. An open gate blocks `set-parameter-kind` (a later stage ordering a base fact), while `merge-parameter` folds a parameter into one of another quantity or none. `repoint-extraction-relation` points an edge at a withdrawn figure. The regulatory stratum's bound is a literal `4` in several places.

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

**Printed on 2026-11-19:** `11284:` (the one `ALL` refusal, `context` only); `add_lens_link 1` (it already calls `_refuse_retired_figure`; it reads no live determination: `awk "/^def add_lens_link\(/{p=1;next} p&&/^def /{exit} p" scripts/db.py | grep -c live_determinations_linked` prints 0), `retire_lens_link 0`, `repoint_extraction_relation 0`, `merge_parameter 0`; `7866:` (the gate refusal on `set-parameter-kind`); tier literals at `scripts/audit/research_batch_dod.py` lines 379, 384, 395 and 1382 (395 is code, the rest comments) and `scripts/db.py` lines 6756, 10847 and 11741, beside the named constant `_REGULATORY_FROM_TIER` (`grep -n _REGULATORY_FROM_TIER scripts/db.py`); `False` (`v_scan_ledger` never reads a retired figure); `(0,) (0,) [(1, 3, 'UNLINKED')] [('carried', 34)] (0,)`: no figure is retired, no determination is live, one gate is open, 34 live `ALL` identity links are all `carried` (T-115's, not this task's), and no parameter is merged. This agrees with the adjudication (items 20, 21, 23, 24). Every subject of items 21, 22 and 24 is empty today, so each is proven on a fixture: say so in your report.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. Every refusal names the next act and writes nothing.

**Seven items, each its own test group (section 6). Do them in this order. You may stop after any complete item and report; never commit a half-built item.**

1. **`ALL` is refused under every basis (item 20; T-056 part 1).** `_refuse_all_by_context` becomes a refusal of `ALL` as an identity under every basis a writer may state (the basis CHECK minus `carried`, `_lens_basis_choices()`), renamed for what it does; its three callers (`add-extraction`, `derive-extraction`, `add-lens-link`) are unchanged in shape. The message cites OD-31 and says that universality is stated once, by the determination's `design_scale` (OD-48, ratified: whom it is for), and that a provision naming no one is carried by its ICF and access-need lenses. The stored `carried` links stay (T-115 moves them; count: `select count(*) from extraction_lens_links where identity_code='ALL' and retired_at is null`). **Open point O-2:** with `ALL` refused, a clause of a source below tier 4 naming no one has no identity route (OD-47's floor exception has no tooling task in the adjudication's section 4); its ICF and need lenses remain. Every live `ALL` link today is tier 6 (`select e.tier, count(*) from extraction_lens_links l join source_value_extractions x using(extraction_id) join evidence_sources e using(ref_id) where l.identity_code='ALL' and l.retired_at is null group by 1`), so nothing is stranded today. Append to `workplan/2026-11-12-bidirectional-pipeline/tasks/T-056-all-leaves-identity-lens.md`, after its last line, this dated line and nothing else:

   > **Amended 2026-11-19 (third adjudication item 20, ratified 2026-11-19):** T-056 is split. Part 1, built by T-138: `add-extraction`, `derive-extraction` and `add-lens-link` refuse `ALL` as an identity under every basis a writer states. This task keeps item 1 (the retirement mechanism), item 2's general refusal through `retire-identity` and the deletion of the `add-conflict` special case, items 3 and 3a (the engine; OD-48 is answered: (a), whom it is for) and item 5.

2. **`context` is refused where the clause names that group (item 19; this author's reading, open point O-1).** In `_require_lens_warrant`, basis `context`, for an identity code: refuse when a recorded name of **that identity** occurs in the figure's own `claim_text`, naming `--basis named_in_text` with those words as the next act ("provenance demands the strongest warrant the words support"). Names are read from the base, never typed: the identity's `display_name` in `base_taxonomy_identity` (live rows only; that cell joins several names with `;` in some rows, `select count(*) from base_taxonomy_identity where status='active' and display_name like '%;%'`, so split on that separator for this read only and name it as the joined-cells defect it is), and the attested forms (`v_attested_term_forms`) of any term the base links to the identity: no such link exists today (no table carries both `identity_code` and `term_id`: derive with `pragma table_info`), so this adds nothing now and is read when one exists. Matching uses the script-derived containment of T-136 item 3 (substring for a name holding a wide character, word boundaries otherwise; reuse that helper if it is on the branch). Otherwise the judged link stands: a clause whose words are not a recorded name of the group is exactly what `context` is for (OD-65; OD-47's ratified use), and its `basis_reason` is kept. Do not tighten `named_in_text` here (its docstring says it does not check that the words name the code; that is not this item). **Why not the literal "would pass the `named_in_text` test":** that test accepts any word found in the clause or the saved file, so it would turn nearly every judged link into a falsely "named" one and refuse its reason. Residual: names recorded only in English miss a clause naming the group in another language, so the judged link stands there (the safe direction). A superseded source's figure is not a lens question: change nothing for it.
   > **Amended 2026-11-20 (T-126 second repair):** the `context` and `named_in_text` warrant matching (`_as_whole_words`, shared, from T-018) must switch to T-136's script-aware containment helper too, not only this item's new refusal: today `勾配` and `傾斜路` are refused under `context` though present in the claim text, because only a whole punctuation-bounded run matches.

3. **A lens does not change under a live determination (item 21, OI-55 (7)), and no edge points at a withdrawn figure (item 86).** `add-lens-link` and `retire-lens-link` refuse while `dbcore.live_determinations_linked(conn, extraction_id)` is non-empty, naming each determination and the walk back: `retire-specification`, then the link change, then re-determine (the pattern `retire-extraction` already uses). `repoint-extraction-relation` calls `_refuse_retired_figure` on both ends, as `relate-extraction` does.
4. **A withdrawn figure's pair is owed until it is read again (item 22).** One schema migration (number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`, plus one; `scripts/migrations/NNN_withdrawn_pair_owed.sql`, ending `PRAGMA user_version = NNN`) recreates `v_scan_ledger` from its CURRENT text in `sqlite_master` (migration 158 set it). **The ratified rule, kept:** a pair with no live figure, at least one retired figure, and no covering reading recorded after the latest `retired_at` of its figures takes one new status, `WITHDRAWN-UNREAD`, placed after `STATED-ABSENT` and before `READ-NOTHING-FOUND`. For such a pair a reading recorded before that retirement covers nothing, so once a later reading exists the existing statuses are read over the later readings only (a later partial reading gives `READ-PARTIAL`, never `READ-NOTHING-FOUND` through the old full one). Strictly later: both columns carry the minute stamp of `dbcore.now()`, so a reading in the same minute owes (the safe side; say so in the header). Timestamps only; never parse `retirement_reason`. Extend the header's precedence list and "WHY THIS ORDER". Recreate `v_reading_owed` so it owes `WITHDRAWN-UNREAD` (its `text_scope <> 'full'` test would otherwise pass over a pair whose old reading was full); `v_deferred_acts` reads it unchanged. **Routing, stated because the status matches pairs never read in full** (58 of the 94 `EXTRACTED` pairs had no full covering reading on 2026-11-19: `select count(*) from v_scan_ledger where status='EXTRACTED' and coalesce(text_scope,'')<>'full'`): in `scripts/audit/scan_debt.py` the status is debt (`DEBT`, the printed list, the docstring); `--reread` routes a `WITHDRAWN-UNREAD` pair whose source had a full reading before the withdrawal by the existing re-read routes (inventory, retained text, the flag: OD-23), and a pair with no earlier full reading by the existing first-reading route (plain debt), never as "read in full once". In `db.py cell-status`, add the status to the `owed` bucket under its own key, so no pair drops out of every bucket. Every other reader the sweep finds that lists statuses gains it or is shown not to need it.
5. **An open gate no longer blocks a kind (item 23).** `set-parameter-kind` asks `_refuse_live_work` for live determinations only (a keyword that skips the gate query; the gate refusal stays for `retire-parameter` and `merge-parameter`, which it protects, adjudication item 71 (a)). Remove the `gate_why` text then unread.
6. **A merge keeps one quantity (item 24, OD-24).** `merge-parameter` refuses when the two parameters' `quantity_kind` differ, NULL against a kind included (`IS NOT`): when one is NULL, name `set-parameter-kind` on it with the other's kind first; when both are set and differ, say they are two quantities and so two parameters (OD-24), and name no route (a kind is write-once). Read the kinds with `_parameter_row` (extend its SELECT) before any re-point. The reshaping of the merge to T-129's form (OI-78) is not this task.
7. **One home for the regulatory stratum (item 17).** Move `_REGULATORY_FROM_TIER` from `scripts/db.py` to `scripts/dbcore.py` as `REGULATORY_FROM_TIER`, its comment naming `governance/tier-system.md` rows T4 to T6 (it applies a tier definition, it sets none). Every comparison of a tier against a literal `4`, and every refusal, help or docstring sentence stating the bound in words ("(a source of tier 4 to 6)" in `_require_lens_warrant`, "tier 4 or above" in help texts, the docstring of `code_value_identity_audit.py`), in `scripts/` outside tests and migrations, reads it (section 3's grep lines, `_regulatory_pairs`, `_warn_identity_omitted`, `research_batch_dod.py`'s code and comments). The engine's tier buckets (`t in (4, 5)`, `t == 6` in `assess_cell.py`) partition the stratum, and changing them moves `RULE_VERSION`: leave them and name them in the report.

   > **Amended 2026-11-20 (T-126 second repair):** the move is made: the bound is `dbcore.REGULATORY_FROM_TIER`, and db.py's three code literals and `research_batch_dod.py`'s code literal read it (the line numbers printed in section 3 have moved). What stays for this item: the prose literals ("tier 4 to 6", "tier 4 or above") and T138-14.

**What reads it:** the refusals: their callers (the run-pipeline skill, research batches). `WITHDRAWN-UNREAD`: `scan_debt.py`, `v_reading_owed` (so `defer-reading`, `v_deferred_acts`), `cell-status`. The constant: every tier comparison above. **Without it**, a determination stands on a lens its evidence no longer has; a group is stated "for everyone" by a removed marker; a misread figure's source reads examined and empty; a merged parameter's figures sit under another quantity; a tier-ladder change moves some readers only.

**Not in this task:** the T-078, T-083 and T-109 amendments (the coordinator's plan edits); T-056's engine; `add-conflict`; OD-47's `context` floor exception.

**Migration discipline (item 4).** Apply only with `migrate_db.py`; prove with `migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `migration_reproducibility.py --deep` (PASS); no `data_*` file; regenerate `governance/context-map.yaml` if it changed.

**Code size.** Report `git diff --shortstat "$BASE_PRE" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`), naming what each addition reads and replaces.

## 5. Caller sweep

Names to sweep: `_refuse_all_by_context`, `ALL by basis`, `_require_lens_warrant`, `add-lens-link`, `retire-lens-link`, `repoint-extraction-relation`, `v_scan_ledger`, `v_reading_owed`, `READ-NOTHING-FOUND`, `DEBT`, `set-parameter-kind`, `_refuse_live_work`, `merge-parameter`, `_REGULATORY_FROM_TIER`, `regulatory stratum`.

A caller is a hit whose behaviour or truth changes; a hit that stays true is a mention. **Fixing a caller is in scope** (rule 4). Left out: `workplan/` except `machines.yaml`, the ledger, `scripts/migrations/`, the frozen records.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
New refusal texts and a view: run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after; report the difference. `machines.yaml` names `add-lens-link`, `retire-lens-link`, `set-parameter-kind` and `merge-parameter`: correct any transition stating a changed guard.

**Callers found on 2026-11-19** (re-run): `scripts/db.py` (section 4's functions, `cell_status` and its precedence docstring, `_parameter_row`); `scripts/dbcore.py`; `scripts/audit/scan_debt.py`, `code_value_identity_audit.py`, `research_batch_dod.py`, `verified_scan_integrity.py`, `skill_vocabulary_audit.py` (read whether they list statuses); views `v_scan_ledger`, `v_reading_owed` (`v_deferred_acts` and `source_scans`' comment: mentions unless a sentence changes); tests `test_db_amend_writers.py` (T-126 cases accepting `ALL` under `named_in_text` or `heading`, `T083-04`'s gate refusal, the reader of `db._REGULATORY_FROM_TIER`), `test_run_pipeline_refusals.py` (status lists, `cell-status` bucket sums), `test_scan_contract.py` (ledger statuses); `skills/run-pipeline_SKILL.md`; `governance/pipeline-contract.yaml`; `governance/context-map.yaml`. A test asserting the gate on a kind is a caller updated to the ruling, named in the commit body.

## 6. Verification

**Step 1, before any edit: the before-run.** Checks that read what this task touches: `test_db_amend_writers test_run_pipeline_refusals test_scan_contract test_db_integrity code_value_identity_audit scan_debt verified_scan_integrity schema_reference_audit derived_not_curated_audit migration_reproducibility context_map_fresh`.

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-138"
CHECKS="test_db_amend_writers test_run_pipeline_refusals test_scan_contract test_db_integrity code_value_identity_audit scan_debt verified_scan_integrity schema_reference_audit derived_not_curated_audit migration_reproducibility context_map_fresh"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
Record any check red here (`scan_debt` is red while debt exists, by design); no `EXAMINED:` line, or `EXAMINED: 0`, means it examined nothing.

**Step 2: red before, green after, one group per item.** Case ids `T138-NN` (`git grep -c '"T138-' -- scripts/tests` printed nothing on 2026-11-19), in `scripts/tests/test_db_amend_writers.py`. A live determination is built as that file's G04 fixture builds one (it un-retires a determination on the test's copy; derive it by query); other fixtures with the writers on the copy, labelled `TASK-FIXTURE`. Type nothing the database can derive. Show each case red on a seeded defect you then remove (`cmp`).

| Item | Case | Red before (or the seeded defect) | Green after |
|---|---|---|---|
| 1 | T138-01 | `add-lens-link --identity ALL --basis named_in_text` with found words is accepted | refused under `named_in_text` and `heading` on all three writers, naming `design_scale`; nothing written |
| 1 | T138-02 | seeded: restore the `context`-only condition | a non-`ALL` identity under `named_in_text` still passes (a probe no other refusal stops); the T-056 line is present (`grep -c -F "Amended 2026-11-19 (third adjudication item 20"` prints 1) |
| 2 | T138-03 | `context` is accepted on a fixture figure whose `claim_text` holds a recorded name of the identity (read from `base_taxonomy_identity`, not typed) | refused naming `--basis named_in_text`; one case with a name holding a wide character, matched as a substring |
| 2 | T138-04 | seeded: refuse on any word of the warrant found in `claim_text` | `context` whose words occur in `claim_text` but name no recorded name of the identity (the clause's first word, chosen by query) still passes with its `basis_reason`; a retired identity's names refuse nothing |
| 3 | T138-05 | `add-lens-link` on a figure a live determination links succeeds | refused naming the determination and `retire-specification`; the same for `retire-lens-link` |
| 3 | T138-06 | seeded: test `governing_only=True` | a figure linked only `excluded` to a live cell is refused too (the helper's own "linked" meaning); with the determination retired both verbs pass |
| 3 | T138-07 | seeded: drop the new call | `repoint-extraction-relation` to or from a retired figure is refused, nothing written |
| 4 | T138-08 | a pair whose only figure is retired, read in full before the retirement, reads `READ-NOTHING-FOUND` | it reads `WITHDRAWN-UNREAD`; `scan_debt.py` counts it as debt and `--reread` routes it by a re-read route; a pair never read in full takes the first-reading route; `v_reading_owed` holds both; `cell-status` lists them under `owed` |
| 4 | T138-09 | seeded: use `>=`; then seeded: let a reading before the retirement cover | a later partial reading gives `READ-PARTIAL`; a later full reading gives `READ-NOTHING-FOUND`; a reading in the same minute owes. The writers cannot place a reading and a retirement in chosen minutes, so this case writes the stamps directly on its own scratch copy, labelled `TASK-FIXTURE` |
| 4 | T138-10 | seeded: drop the "no live figure" condition | a pair with one live and one retired figure reads `EXTRACTED`; every other ledger row is unchanged (compare the whole view before and after on the canonical copy: no figure is retired there, so the two must be equal row for row) |
| 5 | T138-11 | `set-parameter-kind` on the parameter with the open gate (derive it by query) is refused | it writes the kind; the gate is still open; with a live determination built as G04 builds one it is still refused |
| 6 | T138-12 | merging a parameter with a kind into one without (fixtures) succeeds | refused naming `set-parameter-kind`; two different kinds refused naming OD-24; equal kinds pass; the refusal precedes any re-point (row hashes unchanged) |
| 6 | T138-13 | seeded: compare with `!=` (NULL passes) | NULL against a kind is refused |
| 7 | T138-14 | the grep of section 3 finds code comparing a tier with a literal `4` | none outside `dbcore.REGULATORY_FROM_TIER`'s definition (code lines of `scripts/`, tests and migrations excluded); and no prose literal of the bound in a refusal, help or docstring (`grep -n -E "tier 4|tiers? 4 to 6|4 or above|4 and above" scripts/db.py scripts/audit/code_value_identity_audit.py` and the same over `scripts/`): each is built from the constant; seeded: re-type one `>= 4`, then one "tier 4 to 6" |

**Step 3: the after-run.** The same loop with `after-`; diff the failing lines check by check (`grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL'`). No new failing case, except one asserting a behaviour changed by ruling, updated and named.

**Step 4: the gate, once**, when every edit is made, in the background with a long timeout, waiting with an until-loop on its output file:

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-138"; BASE_PRE=$(cat "$SCRATCH/base_pre")
scripts/preflight.sh --base "$BASE_PRE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Read the `RESULT` line, any `NOTHING-IN-SCOPE` (not a pass), any blocking `FAIL` (one red on `$BASE_PRE` too is not yours: give both lines).

## 7. Commit

After the gate is clean, staged with `git add -A . ':!transcripts' ':!*commands.jsonl' ':!.claude/worktrees'` (check `git status`):
```
git commit -m "governance: lens and figure writers refuse what the rulings forbid, a withdrawn figure's pair is owed again, and the regulatory stratum has one home [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the items done (and any not done), the evidence before and after, each caller and what was done, the reading of item 19>" -m "<the attribution trailers your session instructions give>"
```
If you stopped after a complete item, say which in the subject's body and list the items left.

## 8. What you must NOT do

- Do not write `data/guidebook.db` except through `scripts/migrate_db.py`; do not move or retire the `carried` `ALL` links, or any row (rule 10; T-115's).
- Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`; do not push, open a pull request, subscribe, or run `/adversarial` or `/batch-done`.
- Do not parse `retirement_reason`, type a list of group names, scripts or languages, or grade a `basis_reason` (item 18).
- Do not change the engine, its tier buckets or `RULE_VERSION`; do not touch T-056's engine items, `retire-identity` or `add-conflict`.
- Do not remove the gate refusal from `retire-parameter` or `merge-parameter`.
- Add no table, column, flag, status or verb section 4 does not name; list any helper; hand-type no count. Fixing a caller is in scope.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level. The one refusal section 4 narrows (the gate on `set-parameter-kind`) is narrowed by the ratified item 23.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, saw and expected) when:
- a precondition of section 2 is not met, or the gate prints anything but OPEN, or a later ledger entry narrows the ratification;
- an evidence command of section 3 prints otherwise (in particular: a retired figure, a live determination or a merged parameter exists, which turns a fixture-only proof into a live change to read first);
- a red test is not red before or not green after one honest attempt;
- the sweep finds a caller you cannot repair without adding something section 4 does not name (for instance a reader that would need a new status bucket this file does not name);
- a check green in the before-run is red after, other than a case asserting a behaviour section 4 changes by ruling;
- `migrate_db.py --rebuild` does not reproduce the database, or the ledger's rows change on the canonical copy (T138-10);
- the recorded output of section 3 differs (it records `add_lens_link 1`: that writer already refuses a retired figure; a 0 there means the ground moved);
- a clause is found that the `ALL` refusal leaves with no identity route and that the session judged needs one (O-2): report it, change nothing for it;
- you would have to guess a value, a code, a group or an owner's intent.

**Open points for the owner (carried in the report, not decided here).** O-1: item 2 is this author's reading of item 19 (a recorded name of that identity in the clause), withheld by the critic too; the literal reading is in section 4 with why it was not taken. If the coordinator or the owner holds the literal reading, stop before item 2. O-2: a clause below tier 4 naming no one has no identity route once `ALL` is refused (OD-47's floor exception has no tooling task). O-3: item 3 freezes the lens of every figure a live determination links, in its lens or not (`dbcore.live_determinations_linked`'s meaning), so adding a new group's link to any figure of the parameter first needs every live cell of it retired; item 21 ratified the refusal, and the owner's walkability instruction touches it.

## 10. Rollback

Before merge the coordinator drops the commit; after merge, `git revert` in a new pull request. A committed migration is never edited: fix forward (rule 3).

## 11. Adversarial pass and pull request

The coordinator runs `/adversarial`, `/batch-done`, the push and the pull request. Report per `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 3, with a heading "Task-file defects".
