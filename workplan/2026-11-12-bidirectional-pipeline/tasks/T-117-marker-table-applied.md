# T-117  The marker table applied: a circle by tier, and ⚠ in place of it for a grey, unverified or thin basis

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/TERM-RESOLUTION-PLAN.md` section 4, TT-3, and the W rows of its section 2 (folded 2026-11-14; where that plan and this file differ, that plan governs, and the ledger governs both). Every number in this file was read on 2026-11-14 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-14 by the fold of the term-resolution plan (its TT-3, which named this number). **Held on OD-57 and OD-59** (the plan's Q1 and Q3, referred to the owner). Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-117 |
| Title | The marker table applied: a circle by tier, and ⚠ in place of it for a grey, unverified or thin basis |
| Wave | 6 (after the term-resolution doctrine) |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET: Opus-class. It changes how every evidence tier is marked (an evidence-tier definition applied to code) and derives "thin", a judgment the owner defined in words (see section 2) |
| Traces to | TERM-RESOLUTION-PLAN §4 TT-3 and §2 (rows marked W), §1 U7; the ledger entries from "Owner proposal 2026-11-14 (last) — the three circles by tier" to "Owner answer 2026-11-14 (last) — a cell resting on tier 4 only takes the half circle" (`grep -n -E '^## Owner (proposal|statement|answer|correction) 2026-11-14 \(last\) — .*(circle|triangle|glyph|thin|tier 4|Co-1 and Co-2|grey)' references/project-standards.md`) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-119, T-120 and T-068 merged. T-119 writes the ledger's unification entry, whose BY sentence the decision-record markers of item 6 quote; T-120 amends the doctrine's R rows and writes `governance/evidence-architecture.md` §0, which the W rows of item 6 point to; T-068 edits the same engine function (`determine`) and its test T068-10 asserts the marker "as `band()` gives it on the base", so it must land first and this task re-runs it. Check by running: `git grep -c -F 'Unification 2026-11-14' references/project-standards.md` prints at least 1; `grep -c -F '## 0.' governance/evidence-architecture.md` prints at least 1; `git log "$BASE" --merges --format=%s | grep -c -F 'task/t-068-convergent-counts-roots'` prints 1. If a dependency is not yet merged but its branch is pushed, a draft may be stacked on that branch (`git switch -c task/t-117-marker-table-applied origin/task/t-068-convergent-counts-roots`) and takes `git merge "$BASE"` once it merges; the pull request is opened only after every dependency has merged.
- **Owner decisions:** OD-57 (the term-resolution plan's Q1: apply the circle table now, including lowering T3 clinical from ● to ◐ and replacing ○'s gloss in `CLAUDE.md` §6?) and OD-59 (Q3: does a showcased value carry the grade of its own source, or the floor of the mean of all governing sources?). Both are referred to the owner (ledger: `grep -n -F "## Registration 2026-11-14" references/project-standards.md`) and are never resolved under delegation: evidence-tier definitions are always DG-NON (`grep -n -F 'Evidence-tier definitions' governance/decision-protocol.md`). The rulings this task applies once they open: the table (● T1, T2, Co-1, Co-2; ◐ T3, T4; ○ T5, T6), "T4 only half circle", ⚠ (U+26A0 with no U+FE0F) in place of the circle for a grey, unverified or thin basis, and thin defined as "when the evidence doesn't directly concern someone but is conjecture", the project's own inferences and any mixed value included, a vetted clinician's judgment and a clinician's or academic's derivation excluded. Run the gate before you start and again before you open the pull request; it must print OPEN for both, else stop (section 9):
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-57 OD-59; do gate $n; done
```
- **Delegated resolutions this task rests on:** none.
- **Tests that must be red before you start:** T117-01 to T117-05 (section 6), on the unchanged code.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-117-marker-table-applied "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task has a schema migration
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-117" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

The marker is how a reader sees what a value rests on: the owner's "the empty circle makes it clear that it's not academically or clinically derived". Today the code marks a T4-only cell ○ (an override for regulatory-only cells, then a CHECK that forces ○ on them), marks T3 clinical ● and T3 grey ○, marks T5 ◐, and has no way to say that a value rests on a grey, unverified or conjectural basis: such a value carries a circle that claims a derivation its basis cannot bear.

**Evidence commands** (read-only):

```
sed -n '/^def band(/,/^def floor_mean/p' schemas/tier_derivation.py
grep -n -B2 -A3 'if regulatory_stratum_only:' scripts/assess/assess_cell.py | sed -n '/marker = None/,/floor_mean/p'
python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select sql from sqlite_master where name='specifications'\").fetchone()[0])" | grep -n -F 'marker'
git grep -n -E '○.{0,40}(grey|thin|unverified)' -- CLAUDE.md governance skills scripts
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select count(*), sum(retired_at is null) from specifications').fetchone())"
```

**Output on 2026-11-14:** `band()` returns FULL for T1, T2 and T3 clinical, WEAK for T3 grey and T6, PARTIAL for T4 and T5; the engine sets `source_bands = []` when `regulatory_stratum_only`, so the marker falls to WEAK; the `specifications` marker CHECK (added by migration 116 as a column CHECK) admits `'●', '◐', '○'` only and requires `regulatory_stratum_only = 0 OR marker = '○'`; the ○ gloss "grey, thin or unverified" appears in `CLAUDE.md` §6 and governance; `specifications` holds rows but none live (`(8, 0)`). If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: one function edited, one override deleted, one CHECK relaxed and widened, the prose rows the plan marks W. No new table, view, verb or check.

1. **`band()`** in `schemas/tier_derivation.py`: T3 clinical → PARTIAL; T3 grey → PARTIAL; T5 → WEAK. T1, T2, Co-1, Co-2 stay FULL; T4 stays PARTIAL; T6 stays WEAK. Update its docstring to the table and cite the ledger entries by heading. Derive the Co-1 and Co-2 tiers from `schemas/tier_derivation.py` itself, never a list typed here (rule 8).
2. **Delete the regulatory-only override** in `determine`'s marker block (`scripts/assess/assess_cell.py`, the `if regulatory_stratum_only: source_bands = []` branch; locate by the evidence command, never by line number). `band()` then gives a T4-only cell ◐ and a T5- or T6-only cell ○ ("T4 only half circle"); this one deletion replaces the special case. Re-read the comment block above it (the "Option A section 2.3" note that a floor claim "is weak") and correct it in the same edit.
3. **The marker of a mixed cell (OD-59).** Under the recommended answer ("its own"), the marker is the band of the source or sources that state the showcased value, not the floor mean of every governing source; under the other answer, `floor_mean` stays. Build only the answer the ledger records; if it records neither, stop.
4. **⚠ in place of the circle.** The engine writes `⚠` (U+26A0 alone; assert that U+FE0F is absent) when the showcased value's basis is: **grey** (`evidence_sources.evidence_type` grey, read from the column's CHECK by `dbcore.check_values`, never typed); **unverified** (`evidence_sources.verification_status` `UNVERIFIED`); or **thin**: a governing row whose `evidence_population_match.match_grade` is `PROXY` for the cell's lens, or a determination with `specifications.rests_on_proxy_inference` set, or a value that mixes a source's finding with an inference the project adds. The proxy branch's string (`grep -n -F 'most-accommodatingly within what the' scripts/assess/assess_cell.py`; TT-1 left it here because it waits on OD-57) states the ⚠ and why. **Not thin:** a source that is a vetted professional judgment (Co-2, a peer-reviewed clinical argument) or a derivation a clinician or academic published; their own marker applies. Derive each cause from those columns and store none of them beside it (rules 5 and 8): the marker column holds the result, the causes stay where they are.
5. **Schema migration.** `scripts/migrations/NNN_marker_table.sql` (number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` plus one, zero-padded; ends with `PRAGMA user_version` set to it). The marker CHECK becomes `marker IS NULL OR (marker IN ('●', '◐', '○', '⚠') AND (regulatory_stratum_only = 0 OR marker <> '●'))`; the second CHECK (a live `stated` or `provisional` row has a marker) is unchanged. **SQLite cannot alter a column CHECK in place** (migration 116 added this one with `ALTER TABLE … ADD COLUMN`), so the table is rebuilt: follow `scripts/migrations/114_extraction_slug_and_root.sql` step for step (capture `sqlite_sequence`, drop and recreate every view and trigger that names `specifications`, derived by `select type, name from sqlite_master where sql like '%specifications%'`), with an `-- AFTER_DATA:` marker if a committed data migration writes `specifications` (`git grep -l specifications -- 'scripts/migrations/data_*'`). Prove with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` and `python3 scripts/audit/migration_reproducibility.py --deep`; then the UNWRITABLE derivation of CLAUDE.md §4 (no new line), and `python3 scripts/generate/context_map.py`, output included.
6. **The W prose rows of TERM-RESOLUTION-PLAN §2**, in this pull request because they state what items 1 to 5 build: `governance/evidence-architecture.md` (the "weak band (○)" passages for a T4–T6-only basis, by `grep -n -F 'weak' governance/evidence-architecture.md`, become "the code marker by tier (tier-system §5)"); `governance/evidence-methodology.md` where it names the band of a code-only basis; `governance/mission-and-epistemics.md` (the full-strength anchor list); `governance/tier-system.md` §5 and the line that lists markers (apply the table; the ⚠ row); `governance/pipeline-contract.yaml` (the two band statements for a T4 basis); `references/methodology-evidence-hierarchy-mapping.md` (the row the plan marks W); `CLAUDE.md` §6's marker line ("○ grey, thin or unverified" becomes the table with ⚠, pointing to `governance/tier-system.md` §5); `skills/evidence-auditor_SKILL.md` and `governance/owner-browser.yaml` where they gloss ○ (the ledger's derivation: `git grep -n -E '○.{0,40}(grey|thin|unverified)' -- CLAUDE.md governance skills scripts`); the I3 lines of `workplan/2026-08-11-remediation-and-pipeline-anatomy.md` the plan marks W are frozen prose and are left, superseded in prose by T-119's entry. **Decision-record markers:** for `decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md` (the lines the plan lists as "when the table is applied") and `decisions/DR-2026-07-20-*weighted-strength-reconciliation.md`, append to the ledger the `SUPERSEDES:` / `BY:` pairs in the grammar `scripts/audit/supersession_backpointer_audit.py` reads (its docstring; `dbcore.LEDGER_SUPERSEDES_RE`), each target quote occurring once, with a marker line naming SUPERSEDED in or after the target paragraph carrying the BY quote, and an attestation (`attestations/<slug>.json` against `schemas/attestation.schema.json`, CLAUDE.md rule 2). Re-quote any atom in `workplan/pipeline-state-graph/` whose governance source this changes (`python3 workplan/pipeline-state-graph/verify_atoms.py` on each atoms file), and rebuild with `python3 workplan/pipeline-state-graph/build_graph.py` (generated files are never edited by hand).

**Chosen (authoring 2026-11-14):** one migration that relaxes and widens the CHECK in one rebuild. Rejected: a second marker column for ⚠ (two homes for one fact: the owner's "triangle instead", not beside).

**What reads what this task adds or changes:** `determine` writes the marker; `v_best_practice` and render (T-037) show it; `adjudication_integrity` and `validate_evidence_state` read the marker CHECK's vocabulary. **What wrong thing reaches the guidebook without it:** a T4-only cell shows ○, a T3 clinical figure claims ● the owner lowered, and a grey, unverified or conjectural value shows a circle that claims a derivation. **What it makes deletable:** the regulatory-only special case in the marker block.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`, and name what reads each addition.

## 5. Caller sweep

Names to sweep: `band(`, `EvidenceMarker`, `floor_mean`, `regulatory_stratum_only`, `marker`, `○`, `◐`, `⚠`, `weak band`.

**What a caller is.** A hit whose behaviour or truth changes: a test that asserts a T4-only marker of ○ or a T3 clinical band of ●; a view, trigger or CHECK on `specifications.marker`; a skill, governance or CLAUDE.md sentence that states the old table or glosses ○ as "grey, thin or unverified". Left out: `workplan/` except `workplan/pipeline-state-graph/` (atoms and `machines.yaml`), `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.
```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
This task changes a table's CHECK and rebuilds it: run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference, and `python3 scripts/run_checks.py --selftest` after.

## 6. Verification

**Step 1, the before-run.**
```
CHECKS="test_assess_cell_pilot test_evidence_cell_state_2_3 test_validate_evidence_state_2_4 adjudication_integrity claude_md_spine supersession_backpointer_audit"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
**Step 2: red before, green after** (cases `T117-…` in `scripts/tests/test_assess_cell_pilot.py`; prefix free: `git grep -c 'T117-' scripts/tests/`; fixtures built on the test's scratch copy, as T-017's `_t017_cell` builds them):
- `T117-01` a cell whose governing figures are T4 only: marker ◐; red (○).
- `T117-02` T6 only: ○; T5 only: ○ (red for T5, ◐ before).
- `T117-03` T3 clinical only: ◐ (red, ● before); T3 grey only: ⚠ (grey; red).
- `T117-04` a T1 source with `verification_status` UNVERIFIED as the showcased value's basis: ⚠ (red); a T1 cell whose governing row is graded PROXY for the lens: ⚠ (red); a Co-2 source: ● (control, green).
- `T117-05` the migration on a scratch copy: an INSERT with marker `⚠` is accepted; `●` with `regulatory_stratum_only = 1` is refused; `◐` with `regulatory_stratum_only = 1` is accepted (red before: refused).
- `T117-06` (OD-59, as answered) a cell whose showcased value comes from a T1 source and whose other governing source is T6: marker as the ledger's answer says (its own: ●; floor mean: as `floor_mean` gives).
- T068-10 and T068-11 re-run: the value and state are unchanged; only the marker moves, as items 1 to 4 say.
- Seeded defects, each KILLED: `band()` T4 → WEAK (T117-01); the override restored (T117-01); `⚠` written with U+FE0F (T117-03's code-point assertion).
**Live data, before and after:** every active parameter through the engine on a copy, as T-017 section 6 step 2c does; only `marker` may change, and every change is listed with its sources' tiers.
**Step 3: after-run**, as step 1 with `after-`; nothing new may fail.
**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
python3 scripts/run_checks.py --selftest; python3 scripts/audit/migration_reproducibility.py --deep
```

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: apply the marker table and the warning triangle (OD-57, OD-59) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the two owner answers and their ledger lines; the table; the migration and its rebuild; callers; checks with EXAMINED before and after; the live-data marker changes>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not build this while section 2's gate prints CLOSED for OD-57 or OD-59. Do not apply the table to any file before then (the owner's entries hold it).
- Do not change which value is shown (T-059 selects it) or any state; only the marker.
- Do not store grey, unverified or thin beside its cause; do not add a marker column. Do not write the emoji form of ⚠.
- Do not write research rows here (re-assessing live specifications is research, after this merges). Do not write `data/guidebook.db` except through `scripts/migrate_db.py`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: section 2's gate prints CLOSED for OD-57 or OD-59, or the ledger's answer differs from what item 3 or item 1 can build; a dependency is not merged; the evidence output differs; the rebuild does not reproduce the database or the UNWRITABLE derivation prints a new line; a value or state changes in the live-data comparison; deriving thin would need a list kept beside the columns (rule 8); a check green before is red after.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request, with a compensating migration (CLAUDE.md rule 3).

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
