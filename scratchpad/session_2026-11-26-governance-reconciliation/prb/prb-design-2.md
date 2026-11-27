# PR B, part 2: the agonist's design for (IV) the deferred-search flag and (V) the reduced render page

Agonist report, 2026-11-27, for DR-2026-08-19 §7 (agonist-antagonist; a blind antagonist attacks this next).
Branch head `ee815a82`, schema `user_version` 167. **Design only; nothing is implemented.** Read-only on the
repository and on `data/guidebook.db`, whose sha256 was `3d419efb…edb9` before and after every probe
(`sha256sum data/guidebook.db`). Dry runs used scratch copies only: my own at
`/tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/p2/s.db`, and, read-only,
the path-finder's `…/scratchpad/pf/r3MOB.db`, which holds the live 3 × MOB determination the engine wrote
(specification 9) on the same canonical base.

Rule 7a: every figure below was read today, and its command sits beside it. Re-run the command rather than
trust the figure.

---

## 0. Answer in brief

- **(IV) Add one flag, `amend-search --set-deferred-reason TEXT`, and the converse refusal on
  `--set-absence-class`. No migration.** `deferred_reason` already exists, is nullable `TEXT` with no CHECK,
  and the write path already carries an UPDATE of it (dry run, §1.3). Re-running the four searches does not
  fix the defect on its own: the four old rows would still read as searches that ran and found nothing,
  because every reader classes a zero-result row as empty when `deferred_reason` is NULL. That is OD-45's
  ACTION (4), and five readers follow it today. Re-running is owed in addition (OD-45 ACTION (3)), as
  research.
- **(IV) A second defect, found in the dry run:** `amend-search --set-absence-class` today writes a row that
  is both deferred and classed. On a scratch copy, exec 9 took `genuine_absence` beside its
  `deferred_reason`, rc 0. That is the state `log-search` refuses as "A row cannot assert both".
- **(V) A new static-HTML script, `scripts/generate/determination_page.py`.** Its core is a pure function,
  `page(conn, specification_id) -> str`, and the CLI writes the result outside the repository (refused
  inside it, including the committed `scratchpad/`), for publication as a private Artifact.
  `owner_browser_build.py` is a whole-database table browser (sql.js with the database embedded), so it
  cannot be the renderer. A page that embeds every row can refuse nothing. Only its out-of-repo guard and its
  stamp are reused.
- **(V) The page refuses four things:** a determination that is not live; any non-English cell it would
  print that lacks a current, reviewed, hash-matching English rendering; a printed source with no
  verification standing (NULL); a governing source with no population-match row for the cell's identity
  lens. It does **not** refuse an UNVERIFIED source. The owner ruled "keeping them but they get a triangle
  warning", and C10 (after T-117 4a) is the one gate for that.
- **(V) It must show every population-match row, never `assess_cell.population_match`'s first.** On the 3 ×
  MOB cell, six governing sources carry contested grades (PARTIAL and PROXY), and that function returns
  PARTIAL for each, which hides the dissent.
- **Two variants of the four OD-63 figures.** Which one is built depends on the owner's Q1. Variant B
  depends transitively on **T-124, T-059 and T-068** (T-124's own preconditions), plus the unit cleanup data
  (T-108, T-086, T-111) and T-113. It needs **no T-036 view and no migration**. It must refuse while any
  code-stratum figure of the cell is unparsed: 28 of 51 such rows on 3 × MOB today.

---

## 1. (IV) The deferred-search flag

### 1.1 The wrong thing that reaches the guidebook today (proved)

DR-2026-08-19 §4 publishes the determination's "search log *including the empty searches*". Four
zero-result rows on parameter 3's slug never ran:

```
$ python3 - <<'PY'   (canonical, read-only)
... select exec_id, slug, engine, results_found, absence_class, deferred_reason, substr(findings_note,1,200)
    from search_executions where results_found=0 order by exec_id
(87,  'accessible-circulation-geometry', 'googlebooks', 0, None, None, 'NOT A ZERO-YIELD — AN UNFIRED QUERY, AND I RECORDED IT AS A NULL THREE TIMES BEFORE A CHECK CAUGHT IT. All three requests returned HTTP 429: …')
(133, 'accessible-circulation-geometry', 'web', 0, None, None, "RETRIEVAL FAILURE, NOT ABSENCE: curl exit 35 (connection reset by peer) …")
(138, 'accessible-circulation-geometry', 'web', 0, None, None, 'RETRIEVAL FAILURE, NOT ABSENCE: HTTP 403 (919-byte interstitial) …')
(191, 'accessible-circulation-geometry', 'web', 0, None, None, 'RETRIEVAL FAILURE, NOT ABSENCE: … HTTP 202 with a 180-byte HTML stub …')
```
Totals: `select count(*), sum(absence_class is null), sum(deferred_reason is not null), sum(results_found=0) from search_executions` gives `(203, 203, 1, 13)`.

**The reader a page would use already publishes them as empty.** `db.cell_status` (T-034) is the one home
of "which searches belong to a parameter". Run on a scratch copy:
```
GUIDEBOOK_DB_PATH=$S/s.db python3 -c "import sys;sys.path.insert(0,'scripts');import db;r=db.cell_status(3)['stages']['research'];print([e for e in (87,133,138,191) if e in r['examined_empty']])"
in examined_empty: [87, 133, 138, 191]
```
`examined_empty` is documented as "looked at and found nothing" (`grep -n 'examined_empty' scripts/db.py`,
the docstring of `cell_status`). Five more readers treat `results_found = 0 AND deferred_reason IS NULL` as
an empty search, and all of them count these four:
- `research_batch_dod.py` R8 and R14;
- `alias_provenance_audit.py:136`;
- `test_scan_contract.py:1492`;
- `v_coverage_parameter_via_admission`;
- every `v_coverage_*` view through `deferred_reason IS NULL`.

**No typed home exists.**
```
$ GUIDEBOOK_DB_PATH=$S/s.db python3 scripts/db.py amend-search --exec-id 87 --append-note "TASK-FIXTURE probe" --set-deferred-reason "HTTP 429" --session session_p2-probe --dry-run
db.py: error: unrecognized arguments: --set-deferred-reason HTTP 429     rc=2
$ ... amend-search --help | grep set-absence-class
  --set-absence-class {genuine_absence,query_shape_failure,wrong_index}
```
The page could separate these rows only by parsing the `findings_note` prefix ("RETRIEVAL FAILURE, NOT
ABSENCE"). That is a fact read out of prose, which CLAUDE.md §4's schema-shape rule forbids ("a prefix that
says what the rest of the cell means").

**Second defect (the converse).** On a scratch copy:
```
$ GUIDEBOOK_DB_PATH=$S/s.db python3 scripts/db.py amend-search --exec-id 9 --append-note "TASK-FIXTURE probe: classing a deferred row" --set-absence-class genuine_absence --session session_p2-probe
{ "exec_id": 9, "appended": true, ..., "absence_class": "genuine_absence" }   rc=0
row after: (9, 0, 'genuine_absence', 1)     # results_found, absence_class, deferred_reason IS NOT NULL
```
`log-search` refuses this exact state (`scripts/db.py`, `log_search`: "--deferred-reason says the search was
not run, and --absence-class … says it ran and found nothing. A row cannot assert both"). No CHECK or
trigger holds it: the table CHECKs name `absence_class` only against `results_found`, and
`select name from sqlite_master where type='trigger' and sql like '%search_executions%'` prints `[]`.
Whichever flag lands second must refuse a row that already carries the other.

### 1.2 The ruling text applied

- **OD-45**, delegated, check confirmed (`references/project-standards.md:6391`–`6404`). *"A logged search
  whose request returned no result list (a 403 or bot challenge, a 429, a connection reset, a stub page) is a
  search not run: recorded with `deferred_reason` naming the failure, with no absence class, and owed a
  re-run."* ACTION: *"(1) Log a request with no result list as deferred, with its reason. (2) Give it no
  absence class. (3) Re-run it. (4) Read a zero-result search as a finding only where `deferred_reason` is
  NULL."*
- **DR-2026-08-19** line 1039: *"`deferred_reason` is for searches *not run*, never a findings channel."*
  Lines 373–375: the acceptance criterion quoted above.
- **CLAUDE.md rule 8**: *"Vocabularies come from the schema, not a list in code"*. `deferred_reason` has
  **no CHECK** (schema above: `deferred_reason TEXT, -- non-NULL => deliberate no-search for this cell`), so
  it holds no vocabulary to read. It is free text naming the failure, exactly as `log-search
  --deferred-reason` takes it. Adding a vocabulary would mean inventing terms (rule 8: "never invents a
  vocabulary term") and writing a migration nothing needs. `absence_class` keeps its three values: OD-45
  (option (c)) adds none, and T-081 §3 says so.

### 1.3 The smallest change

**Files:** `scripts/db.py` only (one function, its argparse, its dispatch), plus the test, the skill prose
and the stale comment (§1.6).

*Before* (`scripts/db.py`, `amend_search`; locate by symbol): the SELECT reads `… results_found,
absence_class` and has no `deferred_reason`. The `set_absence_class` block checks `results_found` and
write-once, not deferral.

*After*, in outline:
```python
def amend_search(..., set_absence_class: str = None, set_deferred_reason: str = None):
    row = conn.execute("SELECT …, results_found, absence_class, deferred_reason FROM search_executions …")
    any_setter = (... or set_absence_class or set_deferred_reason is not None)
    ...
    if set_absence_class:
        ...existing refusals...
        if row["deferred_reason"] or (set_deferred_reason or "").strip():
            raise Refusal(f"exec {exec_id}: deferred_reason says this search was not run; an absence class "
                          f"says it ran and found nothing. A row cannot assert both (OD-45). Nothing was written.")
    deferral_set = None
    if set_deferred_reason is not None:
        reason = set_deferred_reason.strip()
        if not reason:
            raise Refusal(f"exec {exec_id}: a blank --set-deferred-reason states no cause. Nothing was written.")
        if row["results_found"] != 0:
            raise Refusal(f"exec {exec_id}: results_found={row['results_found']}. A search that returned a result "
                          f"list ran; deferred_reason means NOT run, never a findings channel (R6). Nothing was written.")
        if row["absence_class"]:
            raise Refusal(f"exec {exec_id}: absence_class is {row['absence_class']!r}: the row says it ran. A row cannot "
                          f"assert both (OD-45). Nothing was written.")
        if row["deferred_reason"]:
            raise Refusal(f"exec {exec_id}: deferred_reason is already set. It is write-once. Nothing was written.")
        conn.execute("UPDATE search_executions SET deferred_reason=? WHERE exec_id=?", [reason, exec_id])
        trail = f"{marker}deferred_reason set (OD-45: the request returned no result list; a search not run, owed a re-run)"
        conn.execute("UPDATE search_executions SET findings_note=? WHERE exec_id=?", [(merged or "").rstrip() + trail, exec_id])
        merged = (merged or "").rstrip() + trail
        deferral_set = reason
    ... return {..., "absence_class": absence_set, "deferred_reason": deferral_set}
```
Argparse, beside `--set-absence-class`:
```python
p_am.add_argument("--set-deferred-reason",
    help="OD-45: a search logged as run whose request returned no result list (blocked, rate-limited, reset, "
         "a stub page) was NOT run. Records why in deferred_reason (free text; the column has no CHECK). "
         "Write-once; refused when the search found anything or carries an absence class.")
```
Dispatch: pass `set_deferred_reason=args.set_deferred_reason`.

- **What each part reads:** the same row SELECT as today, plus `deferred_reason`. No vocabulary is read,
  because none exists.
- **Rollback is already sound.** A refusal raised after the note append rolls back. Measured on a scratch
  copy: a refused `--set-absence-class` on exec 1 (results 20) left its note length at 88 before and 88 after.
- **Dry run of the write path, scratch only.** I set `deferred_reason` on exec 87 by hand on
  `p2/s.db` and ran `python3 scripts/research/emit_batch_sql.py --scratch $S/s.db --out /dev/stdout`. It
  printed `UPDATE "search_executions" SET "deferred_reason" = '…' … WHERE "exec_id" = 87;` and `0
  insert(s), 1 update(s), 0 delete(s)`.
- **After that write:** `cell_status(3)` moves 87 out of `examined_empty` and into
  `never_examined.deferred_searches == [87]`, and `v_deferred_acts` lists `('search', 'exec 87
  accessible-circulation-geometry')`.
- **Size estimate** (an estimate, not a count): about 25 lines in `db.py` and about 45 lines of tests.

**Re-running is not an alternative.** A re-run is a new row (R8, append-only), and the old row stays as it
is. `v_deferred_acts`' header says so: "A search later run is a new row that names nothing it discharges"
(`select sql from sqlite_master where name='v_deferred_acts'`). Without the flag, the four old rows keep
publishing as empty searches whether or not they are re-run. The flag is the fix; the re-run is the debt
OD-45 ACTION (3) records, and it is research (log-search rows, with the Internet Archive route, CLAUDE.md §7).

### 1.4 The red test first

File `scripts/tests/test_run_pipeline_refusals.py` (registered, advisory, battery `tests`: `grep -n -A8 'id:
test_run_pipeline_refusals' governance/check-registry.yaml`). New section `T081A` placed after `T080`.
Prefix check: `git grep -c -E 'T081A' -- scripts/tests` prints nothing today.

**Fixture.**
- Inside the file's own `scratch()` copy, the subject row is chosen by query: `SELECT exec_id FROM
  search_executions WHERE results_found=0 AND deferred_reason IS NULL AND absence_class IS NULL ORDER BY
  exec_id LIMIT 1`.
- If that returns nothing, build the row by HAND on a second copy, marked TASK-FIXTURE. This follows the
  file's R3-10 rule, because `log-search` can no longer write such a row (T-080).
- A deferred row is chosen by `deferred_reason IS NOT NULL`, a found row by `results_found > 0`, and a
  classed row by building one with `log_search(..., absence_class=…, dry_run=False)` on the copy.
- A feature probe (`'set_deferred_reason' in inspect.signature(db.amend_search).parameters`) makes each case
  go **red by name** on today's tree instead of crashing.

| Case | Assertion | Red today because |
|---|---|---|
| `T081A-01` | `amend_search(eid, note, set_deferred_reason="TASK-FIXTURE HTTP 429")` succeeds. The row's `deferred_reason` is set and `absence_class` stays NULL. The row leaves `cell_status(P)["stages"]["research"]["examined_empty"]` and joins `never_examined.deferred_searches`. It appears in `v_deferred_acts`. | no such parameter (probe red); the CLI exits 2 on an unrecognized argument |
| `T081A-02` | Each of these is refused with "Nothing was written" and leaves the row unchanged: a blank reason; a row with `results_found > 0` (names R6); a row with `absence_class` set ("cannot assert both"); a row already deferred ("write-once"); both flags in one call. | flag absent |
| `T081A-03` | `--set-absence-class` on a deferred row is refused ("cannot assert both"), and `absence_class` stays NULL. | **red on a real defect:** today it succeeds (exec 9, rc 0, §1.1) |
| `T081A-04` | Through the CLI, `amend-search --help` lists `--set-deferred-reason`, and a refused call prints the `REFUSING` prefix. | flag absent |

**After-test:** all four pass. The `T080` cases still pass. `test_db_amend_writers.py` (its `v_deferred_acts`
counts are derived: `git grep -n 'deferred_reason IS NOT NULL' scripts/tests/test_db_amend_writers.py`),
`research_batch_dod.py --selftest` and `test_scan_contract.py` give the same before/after failure lines.

### 1.5 Migration needs (rule 3)

**None for the tooling.**
- The column exists, nullable `TEXT` with no CHECK: read `PRAGMA table_info(search_executions)` and the
  table's DDL.
- It is writable, because `amend-search` already writes `search_executions`, so `dbcore.writable_tables`
  covers it.
- The write path captures the UPDATE (dry run above).

The **data** (deferring 87, 133, 138 and 191, each with its reason in the note's words) is T-081's research
PR (R1), landed through `emit_data_migration.py` after this merges (rule 10). Prove that PR with
`migration_reproducibility.py --deep`: the row-count check cannot see an UPDATE (rule 3).

### 1.6 Callers to sweep (rule 4)

- **Code:** `scripts/db.py`, three places (argparse `p_am`, the `elif args.command == "amend-search"`
  dispatch, the `amend_search` signature). Also the stale comment in `log_search` (`grep -n "amend-search\`
  writes only" scripts/db.py`: "amend-search writes only findings_note and harm_finding"), false already and
  made more false by this change. Correct that one line.
- **Readers whose behaviour changes as intended**, re-run before and after with nothing edited:
  - `v_deferred_acts`;
  - the `v_coverage_*` views and `v_coverage_parameter_via_admission`: the four rows' pairs return to owed,
    which is correct, because nothing ran;
  - `db.cell_status`;
  - `research_batch_dod.py` R6, R8 and R14 (R8's empties count falls by the rows deferred; R6 stays clean
    because the flag refuses `results_found > 0`);
  - `alias_provenance_audit.py`;
  - `test_scan_contract.py` T026-14 (its expected `EXAMINED` is derived from the same predicate, so it moves
    with the data).
- **Skills (prose callers):**
  - `skills/run-pipeline_SKILL.md:135`–`137`: add "or, for a row already written as run whose request
    returned no result list, `amend-search --exec-id N --append-note … --set-deferred-reason '<the failure>'`".
  - `skills/research-log-manager_SKILL.md` step 3: one sentence for the same case.
- **Workplan:** `workplan/2026-11-12-bidirectional-pipeline/tasks/T-081-classify-zero-result-searches.md`
  §4 item 1 (third bullet), §6 and §8 say "`amend-search` has no deferred-reason flag … the row is not
  amended here". Once this merges, that is false, and T-081's research procedure must say to defer the four
  through the flag. Edit it in this PR, or in PR A's hygiene follow-up.
- **Graph:** `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after, because a
  refusal's text is added. Report the difference only.
- **Mention only:** `architecture/meta-scripts-spec.md:59`. `governance/research-contract.yaml` R6 stays true.

### 1.7 What reads the addition (§8)

T-081's research batch writes it for the four rows. `cell_status`, `v_deferred_acts` and the coverage views
read the column, and the render page (V) reads it to print "not run, owed a re-run". **Without it**, four
retrieval failures publish as evidence that nothing exists on the ramp slug.

### 1.8 What I would delete

Nothing in code. In the workplan, T-081's "list it in the pull request as a deferral" workaround.

### 1.9 Stop conditions

- `deferred_reason` gains a CHECK or a trigger before this lands (re-read the schema).
- The dry-run UPDATE is not captured by `emit_batch_sql.py`.
- Any reader in §1.6 holds a typed count that goes red, rather than a derived one.
- The owner reverses OD-45 (its reversal condition: "the owner wants a blocked request kept as a finding
  about a source's reachability").

### 1.10 Open owner inputs

None required. OD-45 is delegated and confirmed. The owner may reverse it, which would turn this flag into
the wrong home.

---

## 2. (V) The reduced T-037 render page

### 2.1 The wrong thing that reaches the guidebook today (proved)

**Nothing renders at all**, and the acceptance criterion is *"rendered and readable as output"*
(DR-2026-08-19:373–375). `ls scripts/generate/` lists `context_map.py`, `owner_browser.html`,
`owner_browser_build.py` and `research_contract_hook.py`. `git ls-files | grep -i -E 'render|template|site'`
finds no generator.

**What a naive page would print**, measured on the live 3 × MOB cell (specification 9 in `pf/r3MOB.db`,
read-only):
```
v_best_practice: (9, 3, 'MOB', 'provisional', '○', None, 5.0, '%', '[{"notation": "%", … "max": "5" …}, {"notation": "rise:run ratio", … "max": "1:20" …}]', 'universal', 1, 1, None)
specification_source_links: 27 rows; governing_refs JSON: NULL
v_determination_provenance roles: conditioning 21, excluded 66, governing 35
governing not VERIFIED: REF-00994 (T4), REF-00997 (T5), REF-01013 (T6), REF-01014 (T4), REF-01016 (T6), REF-01026 (T6), all UNVERIFIED
governing with no population-match row for MOB: REF-00988, REF-00990, REF-00991, REF-00992, REF-01010
governing non-English claim texts: 24; without a current reviewed English: (30, REF-00995, NL), (105, REF-01030, FR)
conditioning non-English without a reviewed English: (115, REF-00995, NL)
open gate binding the cell: gate 1, UNLINKED, REF-01002
```
**Contested grades that a reused function would hide:**
```
$ python3 … assess_cell.population_match(c, r, 'MOB') vs every row
REF-01012 governing population_match -> PARTIAL   rows: …-MOB:PARTIAL  …-MOB-2:PROXY
REF-01013 governing population_match -> PARTIAL   rows: …-MOB:PARTIAL  …-MOB-2:PROXY
REF-01014, REF-01015, REF-01016, REF-01017: the same
```
CLAUDE.md §4: *"`add-population-match` does not enforce uniqueness … a dissenting adversarial grade lands as
a second row and divergent grades read as a contest."* A page that reads `population_match` prints PARTIAL
and hides the PROXY.

**What else a naive page would print wrongly:**
- engine prose that contradicts later rulings (`value_note`, `falsification_condition`; path-finder §1.6);
- `design_scale = 'universal'` on a group cell, which means "for everyone" under OD-48 (antagonist-4 F4);
- the marker ○ where the owner's table gives ⚠ (T-117);
- 87, 133, 138 and 191 as empty searches (§1).

### 2.2 The ruling text applied

- **CLAUDE.md §3** (line 260), render row: *"Book surfaces, read from the database when rendered (owner,
  2026-08-27); no committed file is one."*
- **Owner, 2026-08-27**, quoted in the ledger's second-pass correction (`references/project-standards.md:1656`–`1662`):
  *"the entire pipeline is dynamic rendering on site"* and *"do not rely on artifacts for rendering the
  site"*. RULINGS R1 (commit `ea8b9635`, 2026-10-14) deleted the committed static apparatus.
- **Owner statement 2026-10-28** (`references/project-standards.md:4576`–`4590`), the precedent for a page
  built from the database: *"the page is generated to `$TMPDIR` and published privately, never committed"*.
- **CLAUDE.md, three things #2** (lines 15–17): *"Keep the original beside every translated figure, and show
  an English rendering that records who translated and who reviewed it, and when … never English into
  `claimed_value` or `claimed_unit`."* The owner reads only English.
- **OD-30** (5711, delegated): *"A reader is shown only a translation reviewed by an Opus-class instance other
  than its translator … beside the original."*
- **OD-02** (5422; corrected 5779–5797, delegated, confirmed): *"Every non-English quotation, term and clause
  is shown in its own language and script, with our translation beside it marked as a translation with its
  translator and review status; the original carries its language tag."* ACTION (2): *"Prove a second page
  language works by data alone."*
- **OD-12**, correction 2 and 3 (5803–5806): the page says when discussion is unreviewed. The staleness hash
  *"is named in the render task, or the hash is not added"*.
- **Owner, 2026-11-14** (7005, 7053): *"let's return to keeping them but they get a triangle warning"*;
  *"triangle instead if the value is coming from grey or unverified"*.
- **tier-system §5**: line 70 (⚠ for grey, unverified or thin) and line 101 ("An unretrievable source keeps
  its tier and may still anchor a determination"). These rulings forbid the page from refusing an UNVERIFIED
  source.
- **OD-63**, owner (7399, 7421–7422): *"all values when synthesizing and making determinations, but on the
  render page itself, we just have the minimum, mode, median and maximum colour coding the jurisdiction code
  bodies that we surveyed for comparison purposes"*. **OD-64** (7424–7425): triangle for every grey basis.
  **OD-66** (7453–7454): the 2 % tolerance; placeholder colours chosen by the assistant.
- **DR-2026-08-19 §4** (373–375): *"One research question, with a determination, its governing sources, its
  population-match grading, and its search log including the empty searches — rendered and readable as
  output."*

### 2.3 Can `owner_browser_build.py` be reused?

Read in full (145 lines, plus `owner_browser.html`, 626 lines).
- It base64-embeds **the whole database** and sql.js into one HTML file (`__DB_B64__`, `__WASM_B64__`).
- Its JS browses tables, rows and views, and serves the owner's decision queue (`homePage`, `tablePage`,
  `rowPage`, `viewPage`, `waitingPage`).
- It composes nothing for a question.

**It is a table browser only.** A page that embeds every row cannot refuse anything: unreviewed
translations, retired determinations and engine prose would all be one query away in the viewer's hands.
Using it as the renderer would also put the refusals in client JavaScript, a second language beside the
Python that holds `translations_shown` and `cell_status`.

**The smallest reuse** is two pieces, factored as two module-level functions in `owner_browser_build.py`
and imported by the new script (`sys.path` insert of `scripts/generate`, as `test_scan_contract.py:2417`
already imports the module):
1. **The out-of-repo guard** (`main`, the `out == REPO or out.startswith(REPO + os.sep)` refusal). It also
   covers the repository's `scratchpad/`, which rule 6 commits.
2. **The stamp**: database sha256, `PRAGMA user_version`, `git rev-parse HEAD`, currently inline in `meta()`.

The alternative is a `--determination ID` mode inside `owner_browser_build.py`. It would mix two outputs in
one entry point, one of which embeds the database. I prefer the separate script.

### 2.4 The design (variant-independent core)

**Script:** `scripts/generate/determination_page.py`.
- **Core:** `page(conn, specification_id, templates=EN) -> str`, a pure function over a read-only
  connection. It is the function a dynamic server would call per request.
- **CLI:** `--specification-id N --out PATH [--db PATH] [--templates FILE --lang xx]`. Exit 0 on success; 2
  on a refusal, printing every refusal at once, not only the first.
- **Output:** static, semantic HTML: no script, no external resource, no colour carrying meaning alone.
  Written to `--out`, which the guard refuses inside the repository. Suggested location:
  `/tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/pages/spec-<id>.html`.
  Published to the owner as a private Artifact; never committed.

**What it reads, by name:**

| Page element | Read from | Never read |
|---|---|---|
| The value, state, marker | `v_best_practice` (state, `value_min`, `value_max`, `value_unit`, `value_notations`, `marker`) for the id | `value_note`, `falsification_condition`, `confidence_*`, `tier_basis`, `derivation_rationale`, `design_scale`, `governing_refs` (a JSON joined cell; the junction is the home) |
| Parameter name | `base_parameters` → `terms.canonical_en` (as `v_determination_provenance` joins it) | |
| Lens, code **and** name | identity: `base_taxonomy_identity.display_name`; ICF: `base_icf.title`; need: `access_needs.family` and `design_obligation` (that table has no name column: `PRAGMA table_info(access_needs)`) | bare codes alone |
| Governing and conditioning figures | `v_determination_provenance` for the id, roles `governing` and `conditioning`: `extraction_id`, `claimed_value`, `claimed_unit`, `comparator`, `claim_text`, `ref_id`, `tier`, `evidence_type`, `verification_status` | `excluded` rows (counted only, with their `exclusion_reason` tallied) |
| Governing set | `specification_source_links` for the id | |
| Citation | `evidence_sources` (`author_display`, `pub_year`, `pub_title`, `standard_number`, `jurisdiction`, `doi`, `url`) | `pub_title_en` (NULL on all 33 of the cell's sources; a legacy column; the translations table is the home) |
| Population-match grades | `evidence_population_match` where `ref_id` is the source and `target_population` names the identity code as a word: **every row**, with `match_id`, `match_grade` and `study_population` | `assess_cell.population_match` (returns the first row only) |
| Translations | `db.translations_shown()` (the one home of the OD-30 filter and the `source_sha256` check), keyed by `source`; the need for English from `db._cell_language` | `v_translations_current` read raw (it admits `translated`, per T-037's amendment note) |
| Search log | `db.cell_status(parameter_id)["stages"]["research"]`, its `held`, `examined_empty` and `never_examined.deferred_searches`. For each `exec_id`: `engine`, `language`, `jurisdiction`, `results_found`, `results_admitted`, `absence_class`, `deferred_reason`, `query_text` | `findings_note` (prose) |
| Open gates | `v_open_determination_gates` for (parameter, lens) | |

**Search log grouping.** The page sorts each search into one of four groups by typed columns only:
1. found and admitted (`held`);
2. found results, admitted none (`examined_empty`, `results_found > 0`);
3. **found nothing** (`examined_empty`, `results_found = 0`), with the `absence_class` in words, or "cause
   not yet recorded";
4. **not run, owed a re-run** (`deferred_searches`), with `deferred_reason`.

Group 3 is DR §4's "empty searches". Without (IV), group 4 is empty, and the four rows print in group 3.

**What it refuses** (exit 2, every reason listed, nothing written):
1. **A determination that is not live:** the id is not in `v_best_practice` (retired, superseded, `pending`,
   `not_applicable`). Retired rows exist to test against: `select count(*) from specifications where retired_at is not null`.
2. **A printed non-English cell without English:** the `claim_text` of a printed figure or the `pub_title`
   of a printed source, whose language (`_cell_language`) is not EN, with no `translations_shown()` entry, or
   whose entry carries a `problem`. The problem is either "the original cell changed after it was
   translated" (the hash) or "does not resolve". The owner reads only English. OD-30 alone would allow
   showing the original only, but CLAUDE.md's three things #2 requires an English rendering, and the stricter
   rule governs a published page. Today this refuses extractions 30, 105 and 115 (GAP-372's truncated
   originals; their repair is research R1).
3. **A printed source with no verification standing:** `verification_status IS NULL`. The vocabulary is
   `{'UNVERIFIED', 'VERIFIED'}` by `dbcore.check_values(c,'evidence_sources','verification_status')`, and
   the column is nullable. An **UNVERIFIED** source is printed, with the words "not retrieved: identity not
   confirmed against a payload" beside its citation, and the cell's stored marker (⚠ once T-117 lands)
   carries the warning. The page does not re-decide what C10 decides.
4. **A governing source with no population-match row** for the cell's identity code: DR §4 requires "its
   population-match grading". It would refuse today for REF-00988, -00990, -00991, -00992 and -01010.
   Conditioning sources without a row print "not graded".
5. **`--out` inside the repository**, including `scratchpad/` (the guard).

**What it shows rather than refuses:**
- Open gates, by id, kind and source.
- A non-canonical database (`--db` is not `dbcore.db_path()`'s canonical file). The header prints "DRAFT:
  built from a scratch copy, not a publication", so a page built before T-110 merges cannot pass as
  published.
- "No judged discussion is recorded for this determination" (OD-12 correction 2, honoured at the cost of one
  template line).
- Non-English `query_text` in the search log, printed with its `lang` attribute and "no English rendering
  recorded". It is not refused, because no rule owes it a translation today: `_translations_owed` lists
  titles and claim texts only. See the open inputs.

**How each figure traces to a row.**
- Every value, grade, translation and search is wrapped in an element whose `data-row` names its table and
  key: `specifications:9`, `source_value_extractions:25`, `evidence_population_match:<match_id>`,
  `translations:<id>`, `search_executions:87`.
- The footer prints the database sha256, `user_version`, the commit, and the build time.
- The page computes no figure of its own. Variant A prints stored values. Variant B prints what `cell_figures`
  returns.

**How the owner sees originals beside translations.** Each non-English cell prints as:
```html
<blockquote lang="nl" data-row="source_value_extractions:30">…original, verbatim…</blockquote>
<p class="tr" data-row="translations:<id>">English (our translation): …
   Translated by model: <name>; reviewed by model: <other name>, <reviewed_at>.</p>
```
The original comes first, tagged (WCAG 3.1.2), and the English is marked as ours. Both come from
`translations_shown()`, which is the same output `db.py translations --show` prints, so the owner can check
the page against that command. The value cells print `claimed_value` / `claimed_unit` as stored, never an
English rewrite (three things #2).

**Templates (OD-12, OD-02).** Every fixed sentence lives in one dict `EN` in the script. `--templates FILE`
(YAML, the same keys) and `--lang` emit the page in a second language by data alone, which satisfies OD-02
ACTION (2) at about ten lines. The fixed sentences contain no "must", "should", "required", "recommended" or
"acceptable" of the project's own (T-037 item (v); C9 in the draft contract).

**Left out, with the reason:**
- the render table and its staleness hash (OD-12 correction 3 allows "or the hash is not added"; the stamp
  makes staleness visible);
- T-032 discussion rows;
- the T-122 criteria;
- audience filters (one determination per page; the site's "filters first" requirement concerns a
  multi-cell surface);
- the gaps element (DR §4 does not name it).

**Size estimate** (an estimate): 200–260 lines of script, 150–200 lines of test, plus or minus 10 in
`owner_browser_build.py`. This is new code with no offset: it replaces nothing, because nothing renders.

### 2.5 The four OD-63 figures: both variants (the choice is the owner's Q1)

**Variant A, the page without the four figures.** Everything in §2.4: the headline is the stored
`value_min`/`value_max` in each stored notation, with the stored marker.
- **Tooling dependencies:** T-117 merged (the stored marker can hold ⚠, and C10 4a keeps UNVERIFIED sources
  with ⚠), and (IV).
- **Data dependency:** a live cell (T-110), whose rows clear refusals 2 and 4 (GAP-372 repair; grades for
  the five).
- **Open conflict:** this variant contradicts OD-63 ("on the render page itself, we just have the minimum,
  mode, median and maximum") unless the owner relaxes it for the first page. Antagonist-4 F6 holds that
  rule 0 makes OD-63 binding by default. I agree that it binds until relaxed, so variant A is buildable only
  on a "yes" to Q1.

**Variant B, the page with minimum, mode, median and maximum, colour-coded by jurisdiction code body.**
Everything in §2.4, plus a comparison element:
- **Figures:** from **T-124**'s `cell_figures(conn, parameter_id, lens)` in `scripts/assess/assess_cell.py`,
  called by the page, never re-computed. It returns each figure's value, unit and stating rows, each row with
  its source's jurisdiction (T-124 §4 item 2).
- **Code bodies:** the code-stratum (T4–T6) rows among `cell_figures`' rows, grouped by
  `evidence_sources.jurisdiction`, with the sub-national parent named through `base_jurisdictions.parent_code`
  (T-113's filing). Each body's entry carries the colour, **text label** and **shape** of the figure it is.
  T-037 item (iv)'s defaults cover a body with several values ("each value its own entry"), a value that is
  none of the four ("between the figures"), a value that is several, and a cell with no code body.
- **The key, placeholders from T-037 item (iii):**
  - MIN, `#D55E00`, ▼
  - MODE, `#0072B2`, **■** (the square replaces ●, because ● is also the evidence marker; T-037 itself
    orders this)
  - MEDIAN, `#009E73`, ◆
  - MAX, `#882255`, ▲
  
  The label is visible text (WCAG 1.4.1), and each colour is measured against the page background (1.4.11).
  MODE is glossed "most common practice" (OD-43). The headline determination stays above the comparison and
  is never labelled as a figure (T-124 keeps the selection and the maximum apart).
- **No T-036 view and no migration.** `cell_figures` already returns each row's jurisdiction, so the
  "comparison" is a GROUP BY inside the page over rows T-124 hands it. A view would be a second reader of the
  same rows with no other caller (CLAUDE.md §8: "Nothing is added without naming what reads it").
- **Extra refusal:** if any code-stratum figure of the cell is unparsed (`dbcore.figure_refusal` returns a
  sentence), the colour code is refused, because the four figures would be taken over a fraction of the code
  bodies and be wrong. Measured on 3 × MOB (`pf/r3MOB.db`): **51 code-stratum governing or conditioning rows,
  28 unparsed**, for example ids 74, 76, 78, 79 (`rise:run ratio (general maximu…`) and 80 (`viisi
  prosenttia`). So variant B cannot render this cell until T-108, T-086 and T-111 land as data.
- **Dependencies:** T-124, and T-124's own preconditions **T-059 and T-068** (T-124 §2: "T-059 and T-068
  merged (T-059 builds selection in the accessibility direction …; T-068 builds the cluster step, with the
  tolerance in one home, which is the mode)"); data T-108, T-086, T-111, T-113 (rescoped to REF-00997 and
  REF-00996, antagonist-4 F8); and T-117 and (IV) as in variant A.
- **The path-finder's conditional "+5" set (T-124, T-036, T-108, T-086, T-111) is wrong both ways.** It
  omits T-059 and T-068, which T-124 requires, and includes T-036, which this design shows is not needed.

**Which depends on Q1:** a "yes" (relax OD-63 for the first page) permits variant A. A "no" or no answer
requires variant B (rule 0), and with it T-124, T-059's selection, T-068's cluster step and the unit-cleanup
data. I do not decide it.

### 2.6 The red test first

**File:** new `scripts/tests/test_determination_page.py`, registered in `governance/check-registry.yaml`
(battery `tests`, kinds `tooling`, advisory, like `test_run_pipeline_refusals`). Prefix `T037R-`; `git grep
-c 'T037R' -- scripts/tests` prints nothing today.

**Fixture.**
- Copy the canonical database to a temporary directory, and run the engine on the copy to write a live cell:
  `assess_cell.py --db <copy> --emit-sql <tmp> --parameter-id P --slug S --identity I --session
  session_TASK-FIXTURE-t037r --stamp "2026-01-01 00:00"`.
- P, S and I are derived by query: an active parameter with a non-NULL `accessibility_direction`, its most
  linked identity code from `v_live_lens_links`, and a slug its figures carry.
- If the engine refuses every candidate, print `SKIPPED-NO-FIXTURE`.
- States the live data no longer offers are built by HAND on a second copy (TASK-FIXTURE): a missing
  translation, a NULL `verification_status`, a deleted grade, a second divergent grade (via
  `db.add_population_match`), a changed `claim_text`.
- Every page is written under the test's temporary directory.

**Every case is red today for the stated reason:** `scripts/generate/determination_page.py` does not exist,
and the case reports "renderer absent" by name.

| Case | Assertion |
|---|---|
| `T037R-01` | Exit 0 for a cell that clears every refusal. The page holds: each stored notation's value; the stored marker; the lens code **and** its registry name; every `ref_id` of `specification_source_links`, each with tier, evidence type and verification status in words; every `evidence_population_match` row for (ref × identity), including a seeded second divergent grade; every `exec_id` that `cell_status` returns, each in exactly one of the four groups. All sets are compared by query, never typed. |
| `T037R-02` | Each refusal fires, exits 2, names its subject, and writes nothing: a retired id; a governing non-EN figure with no reviewed English; the same figure with its `claim_text` changed after translation (the hash); a NULL verification status; a governing source with no grade; `--out` inside the repository, and inside `scratchpad/`. An UNVERIFIED source does **not** refuse. |
| `T037R-03` | None of the cell's `value_note`, `falsification_condition`, `confidence_synthesis_basis`, `tier_basis` or `derivation_rationale` contents (any 30-character substring) appears; `design_scale` is not printed; the fixed templates contain no "must", "should", "required", "recommended" or "acceptable". |
| `T037R-04` | Each printed non-EN cell's original sits in an element whose `lang` equals its recorded language, followed by the reviewed English, the translator's name and the reviewer's name, as `translations_shown()` returns them. |
| `T037R-05` | Every `data-row` resolves (`SELECT 1 FROM <table> WHERE <pk> = ?`); the footer's sha256 equals the database file's; a `--db` other than the canonical file prints "DRAFT". |
| `T037R-06` | (Needs IV.) After `amend_search(..., set_deferred_reason=…)` on a slug search in the copy, that `exec_id` appears under "not run" and not under "found nothing". |
| `T037R-07` | A fixture template file whose every sentence begins `XX:` with `--lang xx` yields a page whose fixed sentences all begin `XX:` and whose root has `lang="xx"` (OD-02 ACTION 2). |
| Variant B only | T-037's `T037-F1` to `T037-F5` as written there (red until T-124 is merged), plus `T037R-B1`: a cell with one code-stratum figure whose unit is a sentence refuses the colour code, naming that `extraction_id`. |

**After-test:** all cases green. `test_assess_cell_pilot.py` and `test_scan_contract.py` (which imports
`owner_browser_build.meta`) give the same before/after failure lines.

### 2.7 Migration needs

None for variant A or variant B as designed: the page reads, and T-124 stores nothing. A T-036 view, if the
owner or the antagonist insists on one, would be a schema migration plus a regenerated context map.

### 2.8 Callers to sweep (rule 4)

- `owner_browser_build.py` (the two factored helpers), and its importer `test_scan_contract.py:2417`.
- `skills/run-pipeline_SKILL.md` §7 (lines 407–420). "No specification renderer exists … walking the contract
  by hand" becomes false. "No committed file and no static generator" must be reconciled with a script that
  writes an uncommitted HTML file. State the distinction the owner drew: nothing committed, rendered from the
  database at request time.
- `governance/check-registry.yaml`: the new test entry, then `run_checks.py --selftest`.
- `workplan/2026-11-12-bidirectional-pipeline/tasks/T-037-render.md`: reduce it to this design, or mark it
  superseded by it.
- If T-117's C10 change and this land in either order, the second sweeps the other: the page's refusal 3
  assumes C10 4a.
- Re-run `walkability.py` (D-01): unchanged, because render holds no table.

### 2.9 What reads each addition (§8)

- `page()`: the CLI and the tests. `T037R-*`: `run_checks.py`.
- The two factored helpers: both generators.
- The `--templates` path: OD-02's test.

**What wrong thing reaches the guidebook without each addition:**
- without the page: no answered question can be published, and DR §4 cannot be met;
- without each refusal: a retired value, an English-less foreign clause, a citation with no standing, or an
  ungraded governing source;
- without reading every grade row: a hidden contest;
- without variant B's unparsed-figure refusal: four wrong figures.

### 2.10 What I would delete

- From T-037 as written: the render table, the staleness check, the T-032 dependency and the T-122
  dependency.
- From the plan: T-036 as a separate migration task (its query is the page's GROUP BY; under variant A it is
  not needed at all).
- The draft contract (`workplan/2026-10-30-ramp-spec-pages/RENDER-CONTRACT-…`) stays as reference.

### 2.11 Stop conditions

- The owner does not answer Q1 and variant B's dependencies are not merged. Build nothing that prints a
  headline without the four figures and calls it published.
- The engine cannot write a live cell on a scratch copy (no fixture).
- `translations_shown()` or `cell_status()` changes contract.
- Any refusal would have to re-implement C10, `population_match`'s attribution or the four figures (a second
  home).
- A WCAG 2.2 AA test cannot be run and recorded. The owner's standing requirement is "tested and recorded,
  never self-certified" (T-037 item 2). [UNVERIFIED: whether an automated checker such as axe-core is
  reachable in this environment.]

### 2.12 Open owner inputs

1. **Q1:** relax OD-63 for the first page (variant A) or not (variant B).
2. **Is the page's form "rendered and readable" for DR §4?** A static file built from the database on
   request and published as a private Artifact, against the owner's "dynamic rendering on site". The
   precedent is the 2026-10-28 browser page.
3. **Do non-English search queries owe an English rendering?** 76 of the slug's 168 searches are non-EN
   (`select upper(language), count(*) from search_executions where slug='accessible-circulation-geometry' group by 1`).
   Read with OD-02 ("every non-English quotation, term and clause"), they might; `_translations_owed` does
   not list them.
4. **Should an ungraded conditioning source refuse the page as well?** I chose not.

---

## 3. The agonist's case: claims for the antagonist to break

**Claim 1. The smallest correct fix for (IV) is a flag; re-running alone fixes nothing, and no migration is
needed.** [CONFIDENCE: high, because each step was run.]
- *Evidence:*
  - `cell_status(3)` puts 87, 133, 138 and 191 in `examined_empty` today.
  - OD-45 ACTION (4) and five readers class an empty search by `deferred_reason IS NULL`.
  - A re-run is a new row that discharges nothing (`v_deferred_acts` header).
  - `absence_class` has no "not run" value, and OD-45 (c) adds none.
  - `deferred_reason` is nullable `TEXT` with no CHECK, and `emit_batch_sql.py` captured its UPDATE as
    `1 update(s)`.
  - After the update, `cell_status` moves the row to `deferred_searches`.
- *Falsified if:* any published reader can tell the four apart without the column and without parsing prose;
  or a CHECK, trigger or rule (R8 in `governance/research-contract.yaml`) forbids amending `deferred_reason`
  on a logged row; or `emit_batch_sql.py` drops the UPDATE in a real batch.

**Claim 2. `amend-search --set-absence-class` today writes the state `log-search` forbids, so the converse
refusal must ship with the flag.** [CONFIDENCE: high, reproduced on a scratch copy.]
- *Evidence:* exec 9 took `genuine_absence` beside its `deferred_reason`, rc 0. The `log-search` refusal text
  is quoted in §1.1. The table has no trigger, and no CHECK pairs the two columns.
- *Falsified if:* the probe, re-run on a fresh scratch copy, refuses; or a gate (C-check, `research_batch_dod`)
  already fails such a row on every run, so it cannot reach main.

**Claim 3. `owner_browser_build.py` cannot be the renderer, but its guard and stamp can be reused, and a
pure `page()` function behind an uncommitted file is compatible with the owner's dynamic-rendering target.**
[CONFIDENCE: high for "cannot be the renderer"; medium for compatibility with R1, because "dynamic rendering
on site" may be read as requiring a server.]
- *Evidence:* the browser embeds the whole database (`__DB_B64__`) and composes no question page. The
  2026-10-28 owner entry accepts "generated to `$TMPDIR` and published privately, never committed". CLAUDE.md
  §3 asks only that render be "read from the database when rendered" and that no committed file be one.
- *Falsified if:* the browser has a filtered or non-embedding mode I missed; or an owner statement forbids any
  uncommitted HTML file as a render surface; or "dynamic" is ruled to mean served on request, which would
  make the file form an apparatus.

**Claim 4. The page's refusal set is exactly the four in §2.4, and adding a refusal of UNVERIFIED sources
would contradict the owner.** [CONFIDENCE: medium, because the refusal of an ungraded governing source and
the choice of the stricter translation rule over OD-30 are my readings.]
- *Evidence:*
  - The owner (ledger 7005, 7053) and tier-system §5 (lines 70, 77, 101) keep unverified sources with ⚠.
  - C10 refuses them today (`test_db_integrity.py:536`–`587`), and T-117 4a amends it.
  - The cell would refuse today on translations for 30, 105 and 115, and on grades for five sources.
  - Six governing sources carry contested grades that `population_match` hides.
- *Falsified if:* a ruling says an unverified source is not published; or DR §4's "population-match grading"
  is satisfied by printing "not graded"; or OD-30's original-only display is ruled sufficient for the owner;
  or reading every grade row is shown to double-count a superseded grade (no supersession column exists on
  `evidence_population_match`: read its schema).

**Claim 5. Variant B needs no T-036 view, must refuse while code-stratum figures are unparsed, and pulls in
T-059 and T-068, which the path-finder's "+5" omits.** [CONFIDENCE: medium. T-124's interface is a task file,
not code, and "the code bodies that we surveyed" could be read to include bodies that state no value for the
cell.]
- *Evidence:*
  - T-124 §4 item 2: the function returns "the rows that state it and each row's jurisdiction … so render can
    tell which code body carries which figure without a second computation".
  - T-124 §2 requires T-059 and T-068.
  - On 3 × MOB, 28 of 51 code-stratum rows fail `dbcore.figure_refusal`.
- *Falsified if:* "surveyed code bodies" is ruled to include bodies that were searched but state no value
  (then a coverage query over `search_executions` and `v_research_scope` is needed, possibly a view); or
  T-124 is rewritten to take the mode without T-068's cluster step; or the unparsed count is wrong when
  re-run.

---

## 4. Summary (under 150 words)

(IV): add `amend-search --set-deferred-reason`, write-once and refused on a found or classed row, and make
`--set-absence-class` refuse a deferred row. A scratch run showed it accepts one today. No migration: the
column exists without a CHECK, and the write path carries the UPDATE. Re-running alone leaves 87, 133, 138
and 191 in `cell_status`'s "examined, found nothing". (V): add `scripts/generate/determination_page.py`, a
pure `page()` read at render time and written outside the repository. It reuses only the browser's guard and
stamp, because the browser embeds the whole database. It refuses a non-live cell, missing reviewed English,
NULL standing and ungraded governing sources, never UNVERIFIED sources (the owner's triangle). It prints
every grade row: six contested governing grades exist. Variant B needs T-124, with T-059 and T-068, plus the
unit data and no T-036 view, and must refuse while 28 of 51 code figures are unparsed. Q1 decides which
variant.

File: /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/prb-design-2.md
