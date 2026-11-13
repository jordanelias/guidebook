# T-019  The engine gathers by the lens tags on the figure (the prior workplan's T-3)

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** **Piloted** 2026-11-13: report `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-019-report.md`, patch `.../T-019.patch` (stacked on the T-008, T-016, T-017 and T-018 pilots); defects folded. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-019 |
| Title | The engine gathers by the lens tags on the figure (the prior workplan's T-3) |
| Wave | 1 (chain, last) |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | IMP-08, IMP-09, IMP-10 (first fixture) in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-016, T-017, T-018 merged. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none outstanding. The decisions this task needed are resolved under delegation (next bullet); none is still the owner's.
- **Delegated resolutions this task rests on.** OD-08 (`### OD-08` in `REMEDIATION-WORKPLAN.md`; ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-08" references/project-standards.md`): an absent cell has no row. No determination row is written for a cell that no figure of the parameter is stated in. A lens judged relevant to the parameter that no figure carries is recorded as an open gap naming the parameter and the lens, by the judgment session that judges it relevant (`db.py add-gap`), never by the engine: the engine cannot judge relevance. What OD-08 leaves open is not this task's to decide: whether the `pending` and `not_applicable` values leave the `specifications.state` CHECK (a later tooling question; history rows hold them), and how the three meanings of absence are derived (T-034). Each is a resolution by an Opus-class model under the owner's delegation of 2026-11-12: not the owner's words, reversible by the owner, and read only through the ledger's gate (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). Run it before you start and again before you open the pull request; the expected line is `OD-08 OPEN (delegated; not required)` (OPEN means in force: proceed); if any line prints CLOSED, stop (section 9):
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-08; do gate $n; done
```
- **Not a precondition: T-013** (`tasks/T-013-typed-gaps.md`, the typed `gaps` columns and `add-gap --parameter/--identity/--icf/--needs/--medical`). OD-08's reasoning file says the sub-case "needs T-013 merged"; it does not, for this task. The engine writes no gap for an absent cell (it refuses and writes nothing, section 4 item 5), so no code here reads or writes those columns. Recording the gap is the judgment session's act, and it is typed only once T-013 has merged; until then `add-gap` records it in its description. So the refusal text names `db.py add-gap` and no flag that only T-013 adds. Whether T-013 is in `$BASE`: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print('parameter_id' in [r[1] for r in c.execute('pragma table_info(gaps)')])"`. If it is (`True`), its cases in `scripts/tests/test_run_pipeline_refusals.py` (`T013-*`) are callers of this change (section 5); T-013 also edits the engine's pending-gap INSERT, which this task leaves in place.
- **Tests that must be red (or green) before you start:** AT-50, AT-51, AT-52 red. (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; AT-50 to AT-52 are in the first file's §4. The tests this task must turn are restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-019-lens-gather "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-019" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

The engine selects evidence by parameter alone. A determination for Deaf people, for blind people or "for everyone" is computed from the figures tagged for another group, marked and published. This is the gravest defect in the pipeline.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it copies the canonical database first and writes one determination into that copy, so it can be re-run):

```
cp data/guidebook.db "$SCRATCH/d.db" && python3 scripts/assess/assess_cell.py --db "$SCRATCH/d.db" --emit-sql "$SCRATCH/d.sql" --parameter-id 3 --slug accessible-circulation-geometry --identity DEAF --session session_task-probe --stamp '2026-01-01 00:00' --report-json "$SCRATCH/d.json" | head -1; python3 -I -c "import sqlite3,os;c=sqlite3.connect('file:'+os.environ['SCRATCH']+'/d.db?mode=ro',uri=True);print(c.execute('select l.role, x.identity_code, count(*) from specification_extraction_links l join v_live_lens_links x using(extraction_id) where l.specification_id=(select max(specification_id) from specifications) group by 1,2').fetchall())"; sed -n '/\*\*T-3 Lens/,/Code +55/p' workplan/2026-10-23-pipeline-resolution-workplan.md
```

**Expected output today:** a first line beginning `param 3×DEAF provisional` (the rest of that line, the proxy basis and the counts, may differ); a list of `(role, identity_code, count)` in which no identity is `DEAF` (every linked figure is tagged for another group; the pilot saw `MOB`, `SCI`, `MS` and some `None`); the workplan paragraph for T-3. Compare only those three things. (The figure's lens codes are read through T-018's `v_live_lens_links`: after T-018 the four lens columns of `source_value_extractions` are NULL, and a query on them examines nothing.)

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

**This section is the whole change; you do not need to open anything else to execute it.** It was extracted from T-3 in `workplan/2026-10-23-pipeline-resolution-workplan.md` (the paragraph the evidence command prints) and from the T-3 section of `scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md` (`grep -n '^### T-3 lens' scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md`: its steps 1 to 10, tests L1 to L5 and mutations M9 to M12), rewritten for T-018's link table and for OD-08, with the pilot's corrections. That report predates both, and section 5 excludes `scratchpad/` from the sweep as frozen, so it is cited here and never edited. If you do open it, these parts **do not apply** and this file overrides them:
- its common protocol (§3.0, P-1 to P-10), its net-negative exception, its commit subject and its acceptance lines (sections 2, 4 (code size), 6, 7 and 11 here govern those);
- step 1's `_lens_clause`, which reads the four lens columns of `source_value_extractions` with "NULL or equal, and at least one equal": T-018 holds those columns NULL by CHECK, so it would examine nothing, and "NULL or equal" is not the rule. The rule is `T-018-design.md` section 4: a figure must carry every code the cell states (item 2);
- step 1's `OR identity_code = 'ALL'` clause: OR-1b was answered no (`grep -n -F 'OR-1b: "No, ALL reaches only an ALL determination"' references/project-standards.md`), so no clause is added and test L4 takes its "excluded" branch;
- step 4 (`n_extractions_in_lens` and a `gap_account` branch naming the lens), test L1 (an AUT cell over MOB figures is `pending` with a gap naming AUT) and test L5 (a cell with no rows has NULL paths): each describes a `pending` row for a lens no figure carries, and OD-08 says no row (item 5). The prior workplan's acceptance-table row "the AUT, BLIND, ADHD and d450 cells `pending` with a gap naming the lens" is superseded the same way; its T-3 paragraph ("no row is stored for a lens no figure carries") is the one that holds;
- step 7 and mutation M12 (the lens columns into `dbcore.ENGINE_EXTRACTION_COLUMNS` and `db.py`'s `_AMENDABLE_SVE_FIELDS`, `amend-extraction` filling a NULL lens column with warrant), and the three `test_db_amend_writers.py` amend tests: T-018 retired the columns, `amend-extraction` gains no lens arguments (`T-018-design.md` section 6, "Not changed"), and a lens is added or retired with T-018's `add-lens-link` and `retire-lens-link`. What step 7's "amend under a live determination is refused" test protected (a lens changed under a live determination) is not settled by this task: do not add a refusal to T-018's verbs; name it in the pull request as not verified;
- step 6's derivation of K01's closed set with `git log -p -S'RULE_VERSION = '` (the prior workplan's WR-2 repeats it): `-S` finds commits that change the *number of occurrences* of the string, and a commit that changes the label keeps that number, so it derives the wrong set (on 2026-11-13 it listed one commit and none of the label changes). Item 4 gives the `-G` command;
- step 10 (rewording the population-only rationale for ICF and need cells): not in the prior workplan's T-3, not built by the pilot, and the report itself leaves the path semantics to the owner; leave that text as it is;
- the tests' `synth_db` change as the report states it (`row_lens` setting the four lens columns on each figure): those columns are dead; item 8 writes link rows.

Locate code by symbol, never by line number.

1. **The red test first.** Before editing the engine, make the fixture change of item 8 and add the cases T019-01 to T019-12 of section 6 to `scripts/tests/test_assess_cell_pilot.py`, then run the file against the unchanged engine and keep the output for the pull request. It must be red (the pilot saw eight `FAIL` lines, then `KeyError: 'unkeyed_models'` stopped the run). Do not commit at this point: the change is one commit, made after the gate (section 7).
2. **The predicate, in `scripts/assess/assess_cell.py`.** Add, directly below `lens_key`:
   ```python
   def _lens_clause(lens, alias):
       """`AND <every lens the cell states is among the figure's live links>` and its parameters.

       A figure reaches a cell when, for each lens the cell states, it has a live link carrying that
       code; a lens the cell leaves NULL imposes nothing (T-018 design section 4). Read from
       `v_live_lens_links`, never from the retired lens columns of `source_value_extractions`, and
       never through a crossing map (D-0184): a figure tagged for another group, or for everyone,
       does not reach a cell that does not state that tag (OR-1b). A cell stating no lens would
       impose nothing and gather by parameter alone, which is the defect this closes, so it is refused."""
       parts = [(f"EXISTS (SELECT 1 FROM v_live_lens_links k WHERE "
                 f"k.extraction_id = {alias}.extraction_id AND k.{c} = ?)", lens[c])
                for c in LENS_ORDER if lens.get(c)]
       if not parts:
           raise Refusal("a cell states at least one lens (D-0182); gathering without one would "
                         "select evidence by parameter alone")
       return "AND " + " AND ".join(p for p, _ in parts), tuple(v for _, v in parts)
   ```
   (`Refusal` is defined further down the module; it is resolved when the function runs.) Give `gather_sources`, `gather_findings`, `gather_confirmers` and `count_extractions` a third parameter `lens`, and append `_lens_clause(lens, "x")`'s SQL to each one's `where` and its values to the end of its parameters. In `gather_confirmers` the clause applies to `x`, the finding row that is gathered; the confirmed row `t` is not filtered there, because it reaches the cell, or not, through `gather_sources`. `count_extractions` selects `FROM source_value_extractions x WHERE x.parameter_id = ? <clause>`. In `determine`, pass `lens` to all four.
3. **Every figure stays linked (K02).** Give `gather_extraction_links` the signature `(conn, parameter_id, governing_refs, lens)` and pass `lens` from `determine`. Compute the in-lens set once, with the same clause: `{r[0] for r in conn.execute(f"SELECT x.extraction_id FROM source_value_extractions x WHERE x.parameter_id = ? {lens_sql}", (parameter_id, *lens_vals))}`. In the loop, **before every other branch**, a figure not in that set gets `role, why = "excluded", (f"not stated in this cell's lens ({cell}): no live lens link of this figure carries every code the cell states; a figure reaches a cell only through the lens codes written on it")`, where `cell` is `", ".join(f"{c}={lens[c]}" for c in LENS_ORDER if lens.get(c))`; keep the prefix `not stated in this cell's lens (` exactly, because section 6 matches it. Add `"in_lens": eid in in_lens` to each link dict, and count `n_extractions_superseded` over in-lens links only (`l["superseded"] and l["in_lens"]`). **Out-of-lens figures are linked, never dropped:** K02 of `scripts/tests/test_db_integrity.py` requires the junction of a live determination to hold every extraction of its parameter, each once, with a role, so an out-of-lens figure is linked `excluded` with that reason and gathered nowhere. K02 needs no edit. Add a sentence saying so to the `excluded` entry of the function's docstring.
4. **The hash and the label.**
   - `sha()`: the payload hashes all four codes: `payload = (f"{parameter_id}|{'|'.join(lens.get(c) or '' for c in LENS_ORDER)}|" + link_payload(links) + "::" + RULE_VERSION)`. Its caller in `determine` becomes `sha(parameter_id, lens, links)`; `lens_key` stays for display and for the gap text. Correct the docstring sentence "`lens` is the COALESCE value, not the whole dict — see lens_key()" to say that `lens` is the four-code dict from this label on, and that the earlier link-set labels hashed the COALESCE key, which K01 keeps for them.
   - `RULE_VERSION`: derive the next label at branch time, and again after any `git merge "$BASE"` (section 11 item 5), with the command T-017 uses; never type it from this file:
     ```
     git fetch origin
     python3 -I - "$BASE" <<'PY'
     import re, subprocess, sqlite3, sys
     git = lambda *a: subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout
     others = git("log", "--remotes", "--not", "HEAD", "-p", "-G^RULE_VERSION = ", "--", "scripts/assess/assess_cell.py")
     on_base = git("show", f"{sys.argv[1]}:scripts/assess/assess_cell.py")
     stored = " ".join(v or "" for (v,) in sqlite3.connect("file:data/guidebook.db?mode=ro", uri=True).execute(
         "SELECT DISTINCT rule_version FROM specifications"))
     used = {int(n) for n in re.findall(r'RULE_VERSION = "pilot-(\d+)"', others + on_base) + re.findall(r"pilot-(\d+)", stored)}
     print("on $BASE:", re.search(r'^RULE_VERSION = "([^"]+)"', on_base, re.M).group(1), "| next: pilot-%d" % (max(used) + 1))
     PY
     ```
     Set `RULE_VERSION` to the printed next label and put above the existing comment block: `# <next label> (T-019, prior workplan T-3): a figure reaches a cell only through the live lens links written on it (_lens_clause), and derivation_sha hashes all four lens codes of the cell. The payload changed: test_db_integrity K01 keeps the earlier link-set labels on the COALESCE key (COALESCE_LENS_SHA_VERSIONS).` The pilot's stack gave `pilot-6` only because the T-017 pilot had taken `pilot-5`.
   - **K01, in `scripts/tests/test_db_integrity.py`, moves with `sha()` in this pull request** (`sha`'s docstring: the two "move together or not at all"). Unchanged, K01 reports every row this engine writes as stale (pilot: `[✗] K01 (3 examined)` on the scratch determinations). Derive the closed set of labels whose sha hashed the COALESCE key: every label in the history of `assess_cell.py` on `$BASE` and every label stamped on a stored row, minus `LEGACY_SHA_VERSIONS`. Run it **before** you set the new label, against `$BASE`, so your own label is not in it:
     ```
     python3 -I - "$BASE" <<'PY'
     import re, subprocess, sqlite3, sys
     git = lambda *a: subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout
     hist = git("log", "-p", "-G^RULE_VERSION = ", sys.argv[1], "--", "scripts/assess/assess_cell.py")
     stored = {v for (v,) in sqlite3.connect("file:data/guidebook.db?mode=ro", uri=True).execute(
         "SELECT DISTINCT rule_version FROM specifications WHERE rule_version IS NOT NULL")}
     legacy = set(re.findall(r'"([^"]+)"', re.search(r"^LEGACY_SHA_VERSIONS = \(([^)]*)\)",
                  git("show", f"{sys.argv[1]}:scripts/tests/test_db_integrity.py"), re.M).group(1)))
     labels = (set(re.findall(r'^[-+]RULE_VERSION = "([^"]+)"', hist, re.M)) | stored) - legacy
     print("COALESCE_LENS_SHA_VERSIONS =", tuple(sorted(labels, key=lambda s: int(re.sub(r"\D", "", s) or 0))))
     PY
     ```
     On 2026-11-13, on the workplan branch without the predecessors, it printed `('pilot-3', 'pilot-4')`; with T-017 merged it also holds T-017's label (the pilot's stack: `pilot-3`, `pilot-4`, `pilot-5`). If it prints a label not of the form `pilot-N`, or omits the label on `$BASE`, stop (section 9). Add below `LEGACY_SHA_SQL` the tuple it prints, with this comment: `#: The link-set labels whose derivation_sha hashed the cell's COALESCE lens key alone. History, so it cannot grow: every later label hashes all four lens codes (T-019). Derived with git log -p -G'^RULE_VERSION = ' (not -S, which misses a changed label) plus the stored labels, minus LEGACY_SHA_VERSIONS.` In K01's loop, select the four lens columns in place of the `COALESCE(...)` (`for cid, pid, *lens4, gr, rv, sha_rec in conn.execute("SELECT specification_id, parameter_id, identity_code, icf_code, needs_code, medical_code, governing_refs, rule_version, derivation_sha FROM specifications WHERE retired_at IS NULL")`), and just before the payload line set `lens = next((c for c in lens4 if c), None) if rv in LEGACY_SHA_VERSIONS + COALESCE_LENS_SHA_VERSIONS else "|".join(c or "" for c in lens4)`. In the `stale.append` message, print the first code (`next((c for c in lens4 if c), None)`) where it printed `lens`. Leave `LEGACY_SHA_VERSIONS` and K02 as they are.
   - **Consequence: every `derivation_sha` moves** (the label and the lens are both in the payload). None is live on the canonical database (`SELECT COUNT(*) FROM specifications WHERE retired_at IS NULL`); K01 and K02 verify each row against its own stored `rule_version`.
5. **The absent cell (OD-08): no row.** In `determine`, compute `n_extractions = count_extractions(conn, parameter_id, lens)` before `gather_sources`, and when it is zero raise:
   ```python
           raise Refusal(
               f"no figure of parameter {parameter_id} is stated in this lens "
               f"({', '.join(f'{c}={lens[c]}' for c in LENS_ORDER if lens.get(c))}): the cell has no "
               f"row. If the lens is relevant to the parameter, record the absence as a gap at "
               f"judgment (db.py add-gap, naming the parameter and the lens); a figure is "
               f"given a lens only with warrant (db.py add-lens-link). Nothing was written.")
   ```
   with a comment citing OD-08. The refusal lives in `determine`, not in `main`, so every caller sees it: `main` already turns a `Refusal` into a `REFUSING:` line and exit 1 with nothing written, and `stale_determinations` catches it (item 6). "Stated in" means: an extraction row of the parameter whose live links carry every code the cell states, whatever its `figure_role`, its `extraction_method` or its source's supersession. A cell that has such figures but too little evidence keeps its computed state, `pending` included (`governance/evidence-methodology.md` §2); OD-08 does not touch it, and the engine's existing pending-cell gap stays. A parameter with no extraction at all is the same case and is refused too. **Remove the path this makes unreachable:** the first branch of `gap_account`, `if det_x == 0:` (cause "the parameter has never been read out of a document", with its remedy); the branch after it becomes the `if`, and a one-line comment says why there is no zero branch. That is the only path removed. Do not change the `specifications.state` CHECK: history rows hold `pending` and `not_applicable`.
6. **A pending cell claims no derivation.** In `determine`, directly after the H4 cap (`if state == "stated" and any(g["binds"] for g in gates):` and its block), add:
   ```python
       # A PENDING CELL HAS NO ANSWER, so it derives nothing and claims no path (T-019, prior workplan T-3).
       if state == "pending":
           functional_basis = derivation_paths = derivation_rationale = cultural_claim_anchor = None
   ```
   `cultural_claim_anchor` is cleared too: it only ever excuses the rationale a `population_only` row owes, and `derivation_handshake_integrity` notes an anchor on a row whose paths are not `population_only`. The `specifications` CHECKs permit all four NULL. Then two callers of the new shape:
   - `scripts/audit/derivation_handshake_integrity.py`, its `if paths is None:` note ("written before migration 080, or by a route that skips the engine"): make it `if paths is None and s["state"] == "pending": pass  # a pending cell has no answer and claims no path (T-019)` followed by `elif paths is None:` with the note unchanged.
   - `stale_determinations` in the engine: wrap its `determine(...)` call in `try`/`except Refusal:` and report the row as `(sid, ["lens (no figure is stated in it now)"])`; the figures behind a stored cell can leave its lens when a link is retired.
7. **AT-32's second half: the models the cell key leaves out.** Add beside `count_extractions`:
   ```python
   def unkeyed_models(conn, lens, links):
       """The lens columns this cell's key leaves NULL but that some governing figure's live links
       carry, in LENS_ORDER: reported, never acted on. Several codes of one model are several cells."""
       gov = [l["extraction_id"] for l in links if l["role"] == "governing"]
       marks = ",".join("?" * len(gov))
       return [c for c in LENS_ORDER if gov and not lens.get(c) and conn.execute(
           f"SELECT 1 FROM v_live_lens_links WHERE extraction_id IN ({marks}) "
           f"AND {c} IS NOT NULL LIMIT 1", gov).fetchone()]
   ```
   Put `"unkeyed_models": unkeyed_models(conn, lens, links)` in the determination dict `determine` returns; add `"unkeyed_models"` to the key list `main` copies into the report JSON (the tuple that names `"n_extractions"`); and print, after the per-cell summary line (the one ending `sha={r['derivation_sha'][:12]}`), `    lens model(s) its governing figures also carry, which the cell key leaves NULL: <names>` when the list is not empty. It is column names (`icf_code`, …), not codes. Nothing is stored.
8. **The fixture, in `scripts/tests/test_assess_cell_pilot.py`.** `synth_db` builds its own schema and writes `'MOB'` into the retired `identity_code` column; it has no `extraction_lens_links` and no `v_live_lens_links`, so once the engine reads the view every existing case gathers nothing (about sixty cases fail, and some pass for the wrong reason). Change it:
   - add to its schema a minimal `extraction_lens_links (link_id INTEGER PRIMARY KEY AUTOINCREMENT, extraction_id INT, identity_code TEXT, icf_code TEXT, needs_code TEXT, medical_code TEXT, retired_at TEXT)` and `v_live_lens_links` as `SELECT link_id, extraction_id, identity_code, icf_code, needs_code, medical_code FROM extraction_lens_links WHERE retired_at IS NULL` (the engine reads only those columns of the view);
   - stop writing `identity_code` on the figure; take the new row's id (`.lastrowid`) and write one link row per entry of the source's `lenses` key, defaulting to a new keyword `row_lens=({"identity_code": "MOB"},)` (most cases are stated in `MOB`);
   - the four existing calls whose cell is not `MOB` pass `row_lens` equal to their cell's lens (`grep -n '"identity_code": "DEM"\|"identity_code": "NEU"\|"icf_code": "AX-AMB"' scripts/tests/test_assess_cell_pilot.py`: two `DEM`, one `NEU`, one `AX-AMB`), so they keep testing what they were written for;
   - the `_proxy_cell` helper inserts confirming finding rows with no link: give each a `MOB` link, or the cases that expect a `WEAK` marker pass for the wrong reason (pilot: only R39 went red without it);
   - case B5a-2 ("a parameter with no extraction at all is `pending` with a gap") asserts the behaviour item 5 removes: rewrite it to expect the `Refusal` whose text contains `has no row`. Import `Refusal` from `assess_cell` beside `determine`.
   T-018 does not edit `synth_db` (its design lists this file as a mention). T-018 does edit the fixtures of `scripts/tests/test_scan_contract.py` and the `extraction()` builder of `scripts/tests/test_run_pipeline_refusals.py`; it merges first, so you edit those files on top of its versions (section 5).

**What reads what this task adds or changes:** every determination: `determine` reads `_lens_clause` through the four gathers and `count_extractions`; K01 reads the new sha payload; `derivation_handshake_integrity` reads `stale_determinations` and the pending rows' NULL paths; the report JSON and the summary line read `unkeyed_models`. The `det_x == 0` branch of `gap_account` is deleted; nothing else becomes deletable.

**Code size.** Report in the pull request the output of the command below (run it after `git add` and before the commit, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. It measures from the point where your branch left `$BASE`, unless T-018's commit is on your branch but not in `$BASE` (a stacked run, as in the pilot, where the merge-base also counted T-008's to T-018's work: 14 files, +1479/-377 against this task's own 8 files); it then measures from T-018's commit, so only this task is counted:

```
T018=$(git log -1 --format=%H --fixed-strings --grep="governance: add the lens link table for figures" HEAD); FROM=$(git merge-base HEAD "$BASE")
[ -n "$T018" ] && ! git merge-base --is-ancestor "$T018" "$BASE" && FROM="$T018"
git diff --cached --shortstat "$FROM" -- scripts schemas .github skills ':!scripts/migrations'
git diff --cached --shortstat "$FROM" -- scripts schemas .github skills ':!scripts/migrations' ':!scripts/tests'   # non-test code alone
```

## 5. Caller sweep

Names to sweep: `gather_sources`, `gather_findings`, `gather_confirmers`, `gather_extraction_links`, `count_extractions`, `stale_determinations`, `RULE_VERSION`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`, which list every verb and are rebuilt by their builder; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger: a sentence there is superseded by a new entry, never edited); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` (it writes nothing) before your change and after it, and report the difference. This task adds a refusal, so run it. It is red on the base: its failure count there is the base state, not yours; only a count above your before-run is yours (the pilot saw the same count before and after). An object that returns 0 rows is unproven, not clean.

**The name sweep misses the callers that matter most here, because the behaviour changes and the names do not.** Run the behavioural sweep as well; on 2026-11-13 it found four callers the name sweep did not:
1. **Run every registered check whose script names the engine** (section 6 step 1 derives the list and runs each before and after). A check that goes red after the change is a caller even when no name in it changed.
2. **Grep for the behaviour, not the name**, in prose and code: `git grep -n -i -E 'every lens of|same extractions|lens should filter|never been read out|written before migration 080|gather(s|ed)? by parameter|pending.{0,40}(gap|row).{0,40}lens' -- skills governance architecture .claude scripts CLAUDE.md ':(exclude)scripts/migrations'`. Judge each hit by the definition above.
3. **Regenerate the generated files that list what each script reads:** after the change, `python3 scripts/generate/context_map.py`, then `python3 scripts/generate/context_map.py --check` (exit 0). The engine now reads `extraction_lens_links` through the view, so `governance/context-map.yaml` changes (the pilot: two lines) and `context_map_fresh` is red until it is regenerated.
4. **Run the engine itself on a scratch copy** for the cells of section 6 step 2b, and `python3 scripts/audit/derivation_handshake_integrity.py --db <that copy>`: a note or failure that appears only after the change is a caller.

**Hits when this file was written** (2026-11-13; the two `git grep` lines above with `-l`, and the behavioural sweep; re-run them, a new file in your output is a hit to judge):

- `gather_sources`: `scripts/assess/assess_cell.py` (yours), `scripts/tests/test_assess_cell_pilot.py` (item 8), `scripts/tests/test_scan_contract.py` (a caller: case E01 calls `ac.gather_sources(con, PE)` and `ac.gather_extraction_links(con, PE, [REF_A, REF_S])` with the old signatures and crashes with `TypeError` rather than going red; build `lens = {"identity_code": POP, "icf_code": None, "needs_code": None, "medical_code": None}` once and pass it to both and to the `determine` call beside them), `scripts/db.py` and `scripts/tests/test_db_amend_writers.py` (docstring and comment: mentions). Prose: none.
- `gather_findings`, `gather_confirmers`, `count_extractions`: `scripts/assess/assess_cell.py` only. Prose: none.
- `gather_extraction_links`: `scripts/assess/assess_cell.py`, `scripts/tests/test_scan_contract.py` (above). Prose: none.
- `stale_determinations`: `scripts/assess/assess_cell.py`, `scripts/audit/derivation_handshake_integrity.py` (a caller: item 6), `scripts/tests/test_assess_cell_pilot.py` (its cases run on `synth_db`: item 8). Prose: none.
- `RULE_VERSION`: `scripts/assess/assess_cell.py` (yours), `scripts/tests/test_assess_cell_pilot.py` (imports it: a caller that needs no edit), `scripts/tests/test_db_integrity.py` (a caller: K01, item 4). The views command also prints `specifications`: a false hit (`LIKE` ignores case and matches the column `rule_version`), a mention. Prose: none.
- Found by the behavioural sweep, not by a name:
  - `scripts/tests/test_run_pipeline_refusals.py` (a caller): its `assess()` helper runs the engine as a CLI on a cell keyed on `IDENT` (the first registry identity) and `ICF` (the first `base_icf` code), and no figure carries both, so E01, E02, E03, E06 and E12 go red (the cell is refused). Repair: key the cell on an identity taken by query from a live link of the cell's own parameter (`SELECT l.extraction_id, l.identity_code FROM source_value_extractions x JOIN v_live_lens_links l USING (extraction_id) WHERE x.parameter_id=? AND l.identity_code IS NOT NULL ORDER BY 1 LIMIT 1`, for `CELL_P`), use it in `assess()` and in E02's expected summary text, and give that figure a link for `ICF` on the test's copy (no live figure carries two lenses). Write that link with T-018's `db.py add-lens-link --extraction-id <id> --icf <ICF> --basis named_in_text --basis-text <a word of that figure's claim_text> --session <the file's session>` on the copy (the pilot hand-wrote the row with SQL; the verb is the sanctioned path and checks the warrant); if no such figure exists, extend the existing skip line for E01-E03, E05, E06, E11 and E12 to say so. If T-013 has merged (section 2), its `T013-*` engine case also keys a cell on a `needs_code` chosen by query that no figure carries; give the same figure a `--needs` link the same way, or that case is refused.
  - `scripts/audit/derivation_handshake_integrity.py` (a caller): item 6.
  - `skills/run-pipeline_SKILL.md`, the sentence "today every lens of a parameter gathers the same extractions, and whether a lens should filter them is an open owner question" (a caller: false after this change). Replace it with: a figure reaches a cell only through the live lens links written on it (`v_live_lens_links`); every lens the cell states must be among them and a lens it leaves NULL imposes nothing; a lens no figure of the parameter carries has no cell (the engine refuses and writes nothing; if the lens is relevant, raise the gap at judgment with `add-gap`).
  - `governance/context-map.yaml` (generated): regenerate it (behavioural sweep, step 3).
  - `governance/owner-browser.yaml`, OR-1's option text "Those five determinations read 'pending' with a gap that names the lens" (a mention): the record of the question as it was put to the owner on 2026-10-29, marked answered; OD-08 now governs the absent cell. Do not edit it.
  - `governance/evidence-architecture.md` ("Every determination records `functional_basis` … and `derivation_paths`") and the `derivation-handshake` criterion of `governance/pipeline-contract.yaml` (quoted as atom PIP-05 in `workplan/pipeline-state-graph/ATOMS.tsv`): a `pending` row now records neither. Read as applying to a determination that reaches an answer; the prior workplan's T-3, which the owner's OR-1 answer released "as written", says a pending cell claims no path. Do not edit ratified text or a quoted atom: name both in the pull request as mentions, with this reason.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `test_assess_cell_pilot`, `test_run_pipeline_refusals`, `test_scan_contract`, `test_validate_evidence_state_2_4`, `test_db_integrity`, `derivation_handshake_integrity`, `context_map_fresh`, `derived_not_curated_audit` (blocking; it scans `assess_cell.py` for curated tuples). The list is typed, so derive the rest as well. This prints every registered check whose `cmd` names a file that names the engine:
```
python3 -I -c "import yaml,subprocess;h=set(subprocess.run(['git','grep','-l','-E','assess_cell','--','scripts',':(exclude)scripts/migrations'],capture_output=True,text=True).stdout.split());print(sorted((c['id'],c.get('level')) for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if any(f in ' '.join(map(str,c.get('cmd') or [])) for f in h)))"
```
On 2026-11-13 it also printed `db_path_env_audit`, `extraction_follow_up_audit` and `medical_lens_integrity`: their scripts name the engine in a path table or a message and do not call it, so they are mentions (the gate runs them). Add any other id it prints to `CHECKS`, or name it in the pull request as a mention with the reason. Run each check as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="test_assess_cell_pilot test_run_pipeline_refusals test_scan_contract test_validate_evidence_state_2_4 test_db_integrity derivation_handshake_integrity context_map_fresh derived_not_curated_audit"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request. Two are known to print no whole-run line (pilot, 2026-11-13): `test_assess_cell_pilot` prints `PASS:` lines and "PASS: all pilot-engine branch tests", and `test_validate_evidence_state_2_4` prints "ALL PASS (0 failed)". Report each as "no EXAMINED line" before and after, count its `PASS:` lines (`grep -c '^ *PASS:' "$SCRATCH/before-test_assess_cell_pilot.txt"`), and compare their failing lines as for the rest. On the canonical database `test_db_integrity`'s K01 and K02 examine 0 (no live determination): their subject is the populated scratch of step 2b, not this run.

**Step 2a: red before, green after, in `scripts/tests/test_assess_cell_pilot.py`.** Fixture cases (item 8's `synth_db`; the codes are fixture labels, because the gather never reads a registry), each with `direction="lower_is_better"` and figures that state a ratio with comparator `<=`:

| Case | Fixture | Expect after | Red before / mutation |
|---|---|---|---|
| T019-01 (AT-50 on a fixture; the seeded wrong-lens test) | one parameter, a `MOB` figure 1:12 and a `DEAF` figure 1:20; cell `MOB` | `governing_refs` is the `MOB` source only; `n_sources == 1` | red before; M9 |
| T019-02 | same | `value_max` is the `MOB` figure's, not the looser `DEAF` one | red before; M9 |
| T019-03 | same | both figures linked; the `DEAF` one `excluded` with the reason prefix of item 3 (K02) | red before |
| T019-04 | same; cell `DEAF` | the `DEAF` source only | red before; M9 |
| T019-05 (AT-51 on a fixture; was L4) | a `MOB` figure and an `ALL` figure | cell `MOB` gathers only the `MOB` one; cell `ALL` only the `ALL` one (OR-1b: no) | red before; M9 |
| T019-06 (was L3) | figure A linked `MOB` and `d450`, figure B linked `MOB` only | cell `MOB`: A and B; cell `(d450)`: A; cell `(MOB, d450)`: A | red before; M9 |
| T019-07 (was L2) | **one** figure linked `MOB` and `d450` | cells `(MOB)` and `(MOB, d450)` have equal links and different `derivation_sha` | M10 (the payload back to `lens_key`). Two figures will not do: the cells then differ in links and the mutation cannot collapse them (the pilot's first version did not go red) |
| T019-08 (AT-32, second half) | as T019-06 | cell `MOB`: `unkeyed_models == ["icf_code"]`; cell `(MOB, d450)`: `[]` | red before (`KeyError`) |
| T019-09 | one `MOB` figure whose link is retired (`UPDATE` of the fixture's own table) | cell `MOB` refused: a retired link carries no lens | red before |
| T019-10 (AT-52 on a fixture; OD-08; was L1) | one `MOB` figure; cell `AUT` | `Refusal` whose text contains `has no row`; nothing returned | red before; M9 |
| T019-11 | one `MOB` figure; cell `{}` | `Refusal` (a cell states at least one lens) | red before |
| T019-12 (was L5) | one T3 `grey` source with `MOB` links and `icf_links=MOB_LINK` (a cell that has a figure and stays `pending`) | `state == "pending"` and `derivation_paths`, `functional_basis`, `derivation_rationale`, `cultural_claim_anchor` all `None` | M11 (delete item 6's `if state == "pending":` block): the pilot saw `('pending', 'dual')` |

Live-database cases, read-only (`determine` writes nothing), printing the file's `SKIPPED-NO-FIXTURE` line when the database has no `v_live_lens_links` or offers no probe. Choose every probe by query from the figures' own live links; never type a parameter or a code:

| Case | Probe | Expect |
|---|---|---|
| T019-13 (AT-50) | every distinct (parameter, identity code) pair on live links | for each cell, every figure it reaches (`in_lens`) carries the cell's code, and none is empty (pilot: 17 cells) |
| T019-14 (AT-51) | the first parameter whose figures carry `ALL` and another identity | the `ALL` cell reaches only `ALL` figures; the other cell reaches an `ALL`-tagged figure only if that figure also carries its code |
| T019-15 (AT-52) | the first (parameter with live links, registry identity) that no figure of the parameter carries | `Refusal` containing `has no row` |

**AT-50 and K02, reconciled.** AT-50 as the programme states it reads "every figure linked (any role) to the determination for parameter 3 × `MOB` carries the lens `MOB`". Literally, that contradicts K02, which requires every extraction of the parameter in the junction: the out-of-lens figures are there, linked `excluded` (the pilot: 66 such links). This file reads AT-50 as two assertions, and both must hold: every figure linked with a role other than `excluded` carries `MOB`, and the set is not empty; every linked figure that does not carry `MOB` is `excluded` with the lens reason (item 3). AT-51 is read the same way ("linked" means reached). Say this reading in the pull request.

**The (MOB) and (MOB, d450) sha difference has no live probe.** No live figure carries both an identity and an ICF code (the only `d450` figure carries `d450` alone), so the engine refuses the live `(MOB, d450)` cell; T019-07 is the test. Do not add a live case for it, and do not print `SKIPPED-NO-FIXTURE` for T019-07.

**Step 2b: the populated scratch.** On a fresh copy, determine the cells AT-50 to AT-52 name, then read the junction, then run K01, K02 and the handshake audit with a subject (the ids are the programme's probes; the assertion is by query):
```
cp data/guidebook.db "$SCRATCH/p.db"
for cell in "3 MOB" "9 ALL" "9 MOB" "3 DEAF"; do set -- $cell; python3 scripts/assess/assess_cell.py --db "$SCRATCH/p.db" --emit-sql "$SCRATCH/p-$1-$2.sql" --parameter-id $1 --slug accessible-circulation-geometry --identity $2 --session session_task-probe --stamp '2026-01-01 00:00' 2>&1 | head -1; echo "rc=${PIPESTATUS[0]}"; done
python3 -I - "$SCRATCH/p.db" <<'PY'
import sqlite3, sys
c = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
for pid, code in ((3, "MOB"), (9, "ALL"), (9, "MOB"), (3, "DEAF")):
    s = c.execute("SELECT specification_id FROM specifications WHERE parameter_id=? AND identity_code=? AND icf_code IS NULL "
                  "AND needs_code IS NULL AND medical_code IS NULL AND retired_at IS NULL", (pid, code)).fetchone()
    if not s: print(pid, code, "no row"); continue
    rows = c.execute("SELECT l.role, l.extraction_id IN (SELECT extraction_id FROM v_live_lens_links WHERE identity_code=?), "
                     "l.extraction_id IN (SELECT extraction_id FROM v_live_lens_links WHERE identity_code='ALL'), "
                     "COALESCE(l.exclusion_reason,'') LIKE 'not stated in this cell''s lens (%', count(*) "
                     "FROM specification_extraction_links l WHERE l.specification_id=? GROUP BY 1,2,3,4", (code, s[0])).fetchall()
    print(pid, code, "(role, carries code, tagged ALL, lens reason, n):", rows)
PY
GUIDEBOOK_DB_PATH="$SCRATCH/p.db" python3 scripts/tests/test_db_integrity.py > "$SCRATCH/p-integrity.txt" 2>&1; grep -E 'K01|K02|C10' "$SCRATCH/p-integrity.txt"
python3 scripts/audit/derivation_handshake_integrity.py --db "$SCRATCH/p.db"
```
Expected after the change: `3 DEAF` exits 1 with `REFUSING: no figure of parameter 3 is stated in this lens` and prints `no row` (AT-52; before the change it writes a `provisional` row); for `3 MOB` and `9 ALL`, every row whose role is not `excluded` has "carries code" 1, every row with "carries code" 0 is `excluded` with "lens reason" 1, and at least one row is not `excluded` (AT-50, AT-51); for `9 MOB`, no row with "tagged ALL" 1 and "carries code" 0 has a role other than `excluded` (AT-51). K01 and K02 print PASS with a non-zero subject (the pilot: 3 examined each). C10 may fail on unverified sources: that is T-104's subject, not a failure of this task. The handshake audit prints no "written before migration 080" note. Show K01 red twice and restore: once with K01 unchanged (item 4) and once on a copy whose `derivation_sha` is set to `'00'` by SQL on that copy.

**Step 2c: the mutations.** Each is applied by hand, the file run, the result recorded, and the mutation removed: M9 (`_lens_clause` returns `("", ())` for a cell that states a lens) turns T019-01 to T019-06, T019-10 and the live T019-13 to T019-15 red; M10 (the payload back to `lens_key(lens)`) turns T019-07 red; M11 (delete item 6's pending block) turns T019-12 red. M12 does not apply (section 4).

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T019-01`, `T019-02`, …) and confirm the prefix is free first (`grep -c '"T019-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Then compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number may only change by the cases you added. `context_map_fresh` is green after you regenerate the map (section 5); the B5a-2 rewrite is the one existing case whose assertion changes, and it is named in the pull request.

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards. Regenerate the context map (section 5) **before** the gate, so it is not the file you change afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`.
- **The gate takes several minutes.** Run it in the background with a long timeout and read `$SCRATCH/gate.txt` when it ends; do not re-run it because the first call timed out.
- **`research_tooling_separation` reads `origin/main`, not `$BASE`** (its registered `cmd` takes no `--base`), so on any other base it can FAIL on paths you never touched (pilots saw far more paths than their diff touched). Run it once by hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`, report that result, and treat a gate FAIL that disappears with `--base` as not yours.
- **In a pilot stacked on other pilots' patches** (the predecessors applied as commits on your branch, not merged into `$BASE`), `--base "$BASE"` gates the predecessors' work too: run the gate with `--base HEAD` (the stack head, before your commit) and say so in the report.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.

**The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: execute workplan T-3 lens routing with its wrong-lens fixture [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, taken from `date -u`. Do not copy trailers from this file; use the ones your session was given.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. Only `scripts/migrate_db.py` changes it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine: mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory. If the task seems to need such a decision, stop.
- Do not author `best_practice_synthesis` or any synthesis prose. A Sonnet-class model is below that floor.
- Do not treat any `[A-Z]-NN` code (old item codes met in `references/`, `working/`) as a container, an example or a name.
- Do not put research rows (`scripts/migrations/data_*`, new evidence, extractions, determinations) in a tooling pull request, or tooling in a research one (CLAUDE.md rule 10).
- Do not push to `main`, rebase, or force-push. Do not subscribe to pull-request activity or schedule check-ins.
- Do not hand-type a count into any file or message; write the command that computes it. Do not type into a test an id, a code or a count the database can derive.
- Do not add a table, column, check, verb or script that section 4 does not name. If one seems needed, stop and report. **This does not forbid fixing a caller:** a test fixture, a comment, a skill sentence or a help string that the sweep of section 5 shows is made false or red by your change is in scope, is fixed in this pull request, and is listed there.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller (as defined there) that you cannot repair without adding something section 4 does not name. A caller you can repair is repaired and listed; a mention is left;
- a check or test that was green in the before-run is red in the after-run, at any level (the test files are registered as advisory, so the gate will not stop you: the before-and-after comparison is what does);
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent.
- the delegation gate of section 2 prints CLOSED for a decision this task rests on (the owner has reversed it, a correction has withdrawn it, or its independent check is not recorded); a delegated resolution is never the owner's words;
- the closed-set command of section 4 item 4 prints a label not of the form `pilot-N`, or a set that lacks the label on `$BASE`;
- you find yourself widening the gather, or writing a `pending` row, because most cells are refused: that is expected until figures carry every relevant model (T-106). Do not widen the gather or restore the row to compensate; if the refusals look wrong, stop and report them.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it (the B5a-2 rewrite among them); each check you ran with its `EXAMINED:` line, before and after; the red-before output of section 4 item 1; the populated-scratch output of section 6 step 2b and the mutation results of step 2c; the reading of AT-50 (section 6); the derived label and closed set (section 4 item 4); the code-size line; what was not verified (at least: whether `add-lens-link` and `retire-lens-link` should refuse under a live determination, section 4). End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4. Derive the `RULE_VERSION` label and K01's closed set again too (section 4 item 4), against the updated `$BASE`: a label another task merged before yours hashed the COALESCE key, so it joins the closed set, and your label must be above it.
