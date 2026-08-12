# Wave 1 — The write path and the bootstrap

**Read `00-holistic-execution-plan.md` first.** **Precondition: L1 exists.**

**Owner gates: none.** Every item here is session-executable.

**The wave's claim:** the repository whose cardinal rule is *never write the database directly*
commits foreign-key violations through its own sanctioned write path — and the fix four
documents agreed on would not have stopped it.

**W1.1, W1.2 and W1.3 land as ONE edit** to the same ~35 lines. Do not attempt them separately;
the second and third are structurally inside the first.

---

## W1.1 — The write path. **The agreed fix is refuted; here is the one that works.**

### Objective
Make a foreign-key-violating migration be **rejected with nothing written** — neither the data
nor its ledger row.

### The defect, re-derived at `fd4c09d`

`scripts/migrate_db.py:154-189`. Real line numbers below; the resolution plan cites `159-188`
and earlier documents cite `161-183`, both drifted.

```python
162    pre_violations = set(tuple(r) for r in conn.execute("PRAGMA foreign_key_check").fetchall())
164    conn.execute("PRAGMA foreign_keys = OFF")
165    try:
166        conn.executescript(sql)
167        conn.execute("INSERT INTO data_migrations (...) VALUES (?, ?, ?, ?)", ...)
171        conn.commit()                                    # ◀── DATA AND LEDGER NOW DURABLE
173        conn.execute("PRAGMA foreign_keys = ON")
174        post_violations = set(...PRAGMA foreign_key_check...)
175        new_violations = post_violations - pre_violations
176        is_bootstrap = "BOOTSTRAP" in body[:500].decode(...).upper()
177        if new_violations:
182            if not is_bootstrap:
183                raise sqlite3.IntegrityError(...)
184    except sqlite3.Error as e:
185        conn.rollback()                                  # ◀── ROLLS BACK NOTHING
188        raise
```

**Three failures stacked, in order of severity:**

1. **The FK check is downstream of `commit()`.** By line 174 the data and its `data_migrations`
   row are both durable. The `rollback()` at `:185` has nothing to undo. This is Break 1 from
   the corridor-walk trial: *exit 1, and it wrote the row anyway, and ledgered the migration.*
2. **`PRAGMA foreign_keys = OFF` at `:164`** means SQLite never rejects the write in the first
   place; the check at `:174` is a post-mortem, not a guard.
3. **Moving the check above `:171` — the fix four documents specified — still cannot work.**
   `scripts/emit_data_migration.py:201` wraps every emitted body:
   ```python
   body = sql if args.no_transaction else f"BEGIN TRANSACTION;\n\n{sql}\n\nCOMMIT;\n"
   ```
   **The migration script commits itself.** Python's `sqlite3.executescript()` additionally
   issues an implicit COMMIT before running. By the time `executescript` returns at `:166` the
   data is already durable — before the runner's own `commit()` is even reached. A reorder
   inside the runner cannot meet this wave's exit condition, *"rejected with nothing written."*

### The fix that meets the condition: verify on a scratch snapshot, then apply

Take a `conn.backup()` snapshot to a tempfile, run the migration **there**, compare
`PRAGMA foreign_key_check` before and after, and apply to the real database only on a clean
result. Nothing touches the canonical DB until the migration has been proven clean somewhere
else.

### Ordered steps

1. Ledger entry (`plan_item: W1.1`), written first, naming `migrate_db.py:154-189` as the locus.
2. Add `import tempfile` and `import shutil` at the module head if absent.
3. Replace the body of the `for ts, migration_id, path in pending:` loop
   (`:154-189`) with the structure below. **This single replacement also discharges W1.2 and
   W1.3** — the `is_bootstrap` test disappears rather than being deleted, and the failure branch
   is where W1.3's quarantine and remainder-print live.

```python
    not_attempted = 0
    for idx, (ts, migration_id, path) in enumerate(pending):
        body = path.read_bytes()
        sha  = hashlib.sha256(body).hexdigest()
        sql  = body.decode('utf-8')
        print(f"    Applying {path.name}...")
        if dry_run:
            continue

        # ---- 1. VERIFY on a scratch snapshot. The canonical DB is untouched here. ----
        with tempfile.TemporaryDirectory() as td:
            scratch_path = Path(td) / "verify.db"
            scratch = sqlite3.connect(str(scratch_path))
            try:
                conn.backup(scratch)                     # byte-faithful copy
                scratch.execute("PRAGMA foreign_keys = OFF")
                pre = set(tuple(r) for r in
                          scratch.execute("PRAGMA foreign_key_check").fetchall())
                scratch.executescript(sql)               # self-committing; harmless here
                scratch.execute("PRAGMA foreign_keys = ON")
                post = set(tuple(r) for r in
                           scratch.execute("PRAGMA foreign_key_check").fetchall())
                new_violations = post - pre
                verify_error = None
            except sqlite3.Error as e:
                new_violations, verify_error = set(), e
            finally:
                scratch.close()

        # ---- 2. REJECT without writing, if the scratch run was not clean. ----
        if verify_error is not None or new_violations:
            if verify_error is not None:
                print(f"    ERROR: {migration_id} failed to execute: {verify_error}",
                      file=sys.stderr)
            else:
                print(f"    ERROR: {len(new_violations)} new FK violation(s) introduced by "
                      f"{migration_id} — REJECTED, nothing written", file=sys.stderr)
                for v in list(new_violations)[:5]:
                    print(f"      {v}", file=sys.stderr)
            not_attempted = len(pending) - idx - 1
            print(f"    {not_attempted} migration(s) not attempted.", file=sys.stderr)
            print(f"    Quarantine it and re-run:\n"
                  f"      git mv {path} scripts/migrations/failed/{path.name}",
                  file=sys.stderr)
            raise sqlite3.IntegrityError(
                f"{migration_id} rejected on scratch verification; "
                f"{not_attempted} not attempted")

        # ---- 3. APPLY for real, only now. ----
        conn.execute("PRAGMA foreign_keys = OFF")
        try:
            conn.executescript(sql)
            conn.execute(
                "INSERT INTO data_migrations (migration_id, applied_at, content_sha, "
                "applied_by_session) VALUES (?, ?, ?, ?)",
                (migration_id, now, sha, applied_by_session)
            )
            conn.commit()
        finally:
            conn.execute("PRAGMA foreign_keys = ON")
    return len(pending)
```

4. Apply the same replacement shape to the **rebuild path** at `:238-267`, which carries an
   undocumented duplicate of the whole mechanism.

### Verification
Re-run the corridor walk's **stage 4a ordering probe** — a `search_admissions` row whose
`ref_id` has no `evidence_sources` parent. Required result:

- exit non-zero;
- `SELECT COUNT(*) FROM search_admissions` unchanged;
- `SELECT COUNT(*) FROM data_migrations WHERE migration_id = '<probe id>'` returns **0**;
- the remainder line `N migration(s) not attempted.` printed.

Then `python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db` must still reproduce the
committed DB.

### Falsifier
If a violating migration already leaves no row and no ledger entry at HEAD, the defect is fixed
and this item does not execute. *(Checked: it does not — `commit()` precedes the check.)*

### Risks
- **Cost:** every migration now executes twice and copies the database once. At the current
  ~4,245 rows this is negligible; state the cost in the ledger so a future large-corpus session
  can revisit it.
- `conn.backup()` requires no open transaction on `conn`. Ensure the loop is not entered inside
  one.
- The scratch DB inherits `PRAGMA user_version`; schema migrations are a separate path
  (`:126-140`) and are **out of scope for this item** — note that they carry the same
  self-committing exposure and file it as a follow-on.

---

## W1.2 — Delete the prose-word FK escape hatch

### Objective
Stop the `--summary` a session types from deciding whether foreign keys are enforced.

### The defect
`migrate_db.py:176` (plan cites `:174`; corrected) — and an **undocumented duplicate at
`:261`** in the rebuild path:

```python
is_bootstrap = "BOOTSTRAP" in body[:500].decode('utf-8', errors='ignore').upper()
```

The first 500 bytes of a migration body contain the header comment built from `--summary`. A
session that types the word "bootstrap" anywhere in its summary disables FK enforcement for
that migration. This is Break 2 from the trial: *re-submitting the identical violation with the
word "bootstrap" in the summary was accepted at exit 0.*

### Ordered steps
**No separate edit is required.** W1.1's replacement removes both occurrences structurally —
there is no bootstrap branch in the new code, because a violating migration is rejected on the
scratch snapshot regardless of its wording. Confirm both `:176` and `:261` are gone.

### Verification
`grep -n "BOOTSTRAP\|is_bootstrap" scripts/migrate_db.py` → **zero hits.**
Then re-run trial probe A-3's payload with the word "bootstrap" in the summary: it must be
rejected.

### Falsifier
If a legitimate, currently-passing migration depends on the bootstrap escape, deleting it breaks
a working path — check `data_migrations` for migrations whose bodies contain the token before
removing it.

---

## W1.3 — A failed migration must not void everything behind it

### Objective
Stop one failed migration from being retried first forever and blocking every migration queued
after it.

### The defect
A failed migration stays pending. `discover_data_migrations()` returns it first on the next run,
it fails again, and everything behind it is never attempted — silently, with no count printed.
This is Break 3 from the trial: *the corrected 7-row admission collided on the primary key of
the row that "had not been written", failed, and wedged the queue.*

### The mechanism that makes the fix work
`MIGRATIONS_DIR.glob("*.sql")` at `:81`, `:95` and `:114` is **non-recursive**, so a
`scripts/migrations/failed/` subdirectory is invisible to both the schema and data discovery
paths. Quarantining by moving the file therefore needs no code change to the discovery logic.

**Not a `data_migrations` skip row.** `--rebuild` regenerates the ledger from files and would
apply the abandoned migration anyway.

### Ordered steps
1. Create `scripts/migrations/failed/` with a `README.md` stating what it holds, that files here
   are invisible to the runner by virtue of the non-recursive glob, and that a quarantined
   migration is **corrected forward as a new migration**, never edited in place.
2. The `not_attempted` counter and its print are already in W1.1's replacement. Confirm the
   count is `len(pending) - idx - 1`.
3. **The runner prints the `git mv` command; it does not move the file itself.** A runner that
   silently relocates repository files during a migration run mutates the working tree mid-run
   and makes `--rebuild` behaviour depend on run history. The move is a deliberate act, recorded
   in the ledger with the failure it responds to.

### Verification
Queue three migrations where the second violates. Required: the first applies, the second is
rejected, `1 migration(s) not attempted.` is printed, and the third is untouched — confirmed by
`SELECT COUNT(*) FROM data_migrations`.

### Falsifier
If a failure at *k* already leaves *k+1…n* explicitly skipped or attempted, the defect does not
exist.

---

## W1.4 — The gap-id allocator returns an id its own schema forbids

### Objective
Make `assess_cell.py` able to complete a determination against an empty `gaps` table.

### The defect, re-derived
Two allocators exist and they disagree:

| | `assess_cell.py:426-429` | `scripts/db.py:149-158` |
|---|---|---|
| Signature | `next_gap_id(conn)` — takes a connection | `next_gap_id()` — **takes none** |
| Empty-table result | `GAP-1` | `GAP-001` |
| Padding | none | `:03d` |
| DB opened | the caller's `--db` | `GUIDEBOOK_DB_PATH`, its own connection |

`schemas/evidence_state.py:167` requires `^GAP-\d{3,4}$`. **`GAP-1` fails it**, so the only
determination engine in the repository aborts on its first gap-bearing write against the
post-reset empty table. The reset moved a counter to a value its own schema forbids and broke
the writer invisibly.

### Why the obvious fix is a trap
The resolution plan's remedy — `from scripts.db import next_gap_id` — **silently reads the wrong
database.** The library function opens `GUIDEBOOK_DB_PATH` itself, while `assess_cell.py:487`
requires `--db` and `:492` **refuses the canonical DB by design**:

```python
487    ap.add_argument("--db", required=True, help="pilot DB (NEVER the canonical data/guidebook.db)")
492        sys.exit("REFUSING: this engine never writes the canonical DB (owner-gated).")
```

A literal import would allocate ids from the canonical DB while writing to a pilot DB — and
`assess_cell.py` is **exempt** from `db_path_env_audit`, so nothing would catch it.

### Ordered steps
1. Ledger entry (`plan_item: W1.4`). Record both allocators under `culling.duplicate_of` — this
   is a live instance of interrogation I5.
2. **First**, give the library function an optional connection:
   ```python
   def next_gap_id(conn=None) -> str:
       own = conn is None
       if own:
           conn = connect().__enter__()   # preserve existing context-manager semantics
       try:
           row = conn.execute(
               "SELECT gap_id FROM gaps "
               "WHERE gap_id GLOB 'GAP-[0-9]*' "
               "ORDER BY CAST(SUBSTR(gap_id,5) AS INTEGER) DESC LIMIT 1"
           ).fetchone()
       finally:
           if own:
               conn.close()
       if not row:
           return "GAP-001"
       return f"GAP-{int(row[0].split('-')[1]) + 1:03d}"
   ```
   Note the row-access change: `db.py`'s own `connect()` sets a row factory, but a caller's
   connection may not — index by position, not by name.
3. **Then** delete `assess_cell.py:426-429` and import the library function, passing the engine's
   own connection explicitly: `gap_id = next_gap_id(conn)` at `:513`.
4. Leave `assess_cell.py`'s canonical-DB refusal exactly as it is.

### Verification
- `python3 scripts/assess/assess_cell.py --db /tmp/pilot.db …` completes against an empty `gaps`
  table and emits `GAP-001`.
- The emitted id validates against `schemas/evidence_state.py`'s regex.
- The pilot DB is the only database opened — confirm by pointing `GUIDEBOOK_DB_PATH` at a
  non-existent path and observing that the run still succeeds.

### Falsifier
If `assess_cell.py` already completes against an empty `gaps` table reading only `--db`, the
defect does not exist.

---

## W1.5 — The documented setup command

### Objective
Make `pip install -r requirements.txt` — **step one of `CLAUDE.md` §7** — produce a working
environment.

### Re-derivation
`requirements.txt` at HEAD is nine lines:

```
8   pydantic==2.13.3
9   PyYAML==6.0.3
```

**The plan's quoted failure is NOT stale — both versions are real and refer to different
things.** An earlier pass of this decomposition recorded the pin/error mismatch as a staleness
finding; that was wrong, and the mechanism resolves it: the error
`Cannot uninstall PyYAML 6.0.1, RECORD file not found` names the version **installed in the
container**, while `==6.0.3` is the version **requested by the file**. The pin forces pip to
uninstall the pre-installed 6.0.1 first, and that distribution has no RECORD file, so the
uninstall — and therefore the whole install — fails. Verified in this container via
`importlib.metadata`: PyYAML 6.0.1 is present and its distribution files contain no RECORD.

**Line 4 is false regardless of the pin question:**
> `# All scripts under scripts/ and the schemas/ package depend only on these two.`

The attestation audits need `jsonschema`, and `.github/workflows/ci.yml` hand-installs it —
which is the evidence that the sentence is wrong.

### Ordered steps
1. Ledger entry (`plan_item: W1.5`).
2. Relax the pin to `PyYAML>=6.0,<7`. This succeeds precisely because a pre-installed 6.0.1
   already satisfies the range, so pip attempts no uninstall.
3. Do **not** relax `pydantic==2.13.3`. It is the same latent failure class if a base image ever
   ships a RECORD-less pydantic, but widening it is a separate judgment — note it for the owner.
4. Add `jsonschema>=4,<5`.
5. Delete the false sentence at line 4 and replace it with an accurate one.
6. Remove the hand-installs from `ci.yml` (the plan cites `:215` and `:227` — verify at HEAD)
   so the workflow and the file stop disagreeing.

### Verification
A clean container runs the documented command and then completes
`python3 scripts/run_checks.py --all` without a `ModuleNotFoundError`.

### Falsifier
The documented command already works in a clean container — in which case only the false
sentence and the CI hand-installs need fixing.

---

## W1.6 — `session_pointer_resolvable` does not exist. **But the capability it names does.**

### Objective
Correct `CLAUDE.md` §10, which names a check that is not in the repository.

### Re-derivation
`grep` for `session_pointer_resolvable` across `governance/`, `scripts/` and `.github/` returns
**zero hits**. `CLAUDE.md` §10 describes it as blocking, and describes behaviour — failing when
either pointer dangles, reporting drift when `LATEST-RESEARCH` falls behind the DB — that no
registered check performs under that name.

**The capability is not missing, though.** All four source documents state the drift-reporting
capability *"has no replacement."* It has one: `scripts/tests/test_db_integrity.py:1063-1115`,
check **L04** — *"sessions/LATEST-RESEARCH gives citation_mining_session a subject"* — reads the
pointer, queries for the newest session holding slug-linked Tier 1–2 sources, and fails when the
pointer has drifted to a session holding zero subjects. It is in the **blocking** `db_integrity`
battery and documented at `check-registry.yaml:473`. It was created by the same commit the sweep
cites, whose message says so explicitly. The sweep quoted the headline and not the message.

**What is true: L04 is dormant, not absent.** With `evidence_sources` at **0 rows** it has
nothing to compare and passes regardless of how stale `LATEST-RESEARCH` is. That is a vacuous
green — the repository's named failure mode — and it must be written down as such.

### Ordered steps
1. Ledger entry (`plan_item: W1.6`).
2. Rewrite `CLAUDE.md:424-427` to name **two real things**: the dispatcher guarantee at
   `run_checks.py:217-238`, and **L04** as the drift detector.

   **The sentence is wrong twice, not once.** Besides naming a check that does not exist, it
   claims an unresolvable pointer "makes `run_checks.py` SKIP the checks that read it." That is
   the *pre-fix* behaviour, and the comment at `run_checks.py:221-230` documents the repair: a
   **blocking** check whose `session_pointer:` does not resolve now returns **FAIL** with a
   restore-the-pointer message (`:231-236`); only *advisory* checks SKIP (`:237-238`). Correct
   both errors in the same edit.
3. State L04's dormancy explicitly: *"L04 is blocking but currently vacuous — with
   `evidence_sources` empty it has no subject to compare and passes regardless of pointer
   staleness. It arms itself when the corpus is repopulated."*
4. File the vacuity under R-15's warranted-floor work (`min_items` / `EXAMINED:`), not as a new
   check.

### Verification
`grep -rn "session_pointer_resolvable" governance/ scripts/ .github/ CLAUDE.md` → hits only in
the corrected prose, if at all. L04's dormancy is stated where the claim used to be.

### Falsifier
A check named `session_pointer_resolvable` is found to exist — then §10 is right and this item
does not execute.

---

## Also in this wave

### The replay script — R-01, ranked first in the register
`scripts/migrations/session_2026_05_11g_replay.py:33` defaults to the **canonical DB**
(`os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")`), does not import `_legacy_guard`,
and replays a pre-reset JSON dump. It is the only `.py` among the files in the canonical
migrations directory.

**Path correction:** the guard lives at **`scripts/migrate/_legacy_guard.py`**, not
`scripts/migrations/`. Importing it across directories needs the `sys.path` insert pattern
already used by `scripts/migrate/migrate_gaps.py:26,:34`. Note also that
`assert_not_canonical` refuses any path merely **named** `guidebook.db`, so a scratch copy used
in testing must be renamed (e.g. `scratch.db`) or the guard will refuse it too.

The directory holds 347 entries: 345 `.sql`, this 1 `.py`, and the 1 `.json` dump.

- **Interim fix (this wave):** import `assert_not_canonical` and make `--db` required
  (`p.add_argument("--db", required=True)`, deleting the `DEFAULT_DB` fallback at `:33`).
  **No live code invokes this script** — the caller sweep returns only frozen session records,
  generated `context-map.yaml`, and workplan documents.
- **Permanent fix:** W7.1 retires it — **and its dump**,
  `scripts/migrations/session_2026_05_11g_data.json`, the 20th file nobody counted. Retire both
  together or the dump is orphaned.

### R-05 recalibrated — "three unguarded direct writers" is **one**
- `scripts/migrate/init_database.py:18` hardcodes `data/db/guidebook.db`, a path that does not
  exist on disk — it cannot touch the canonical DB.
- `scripts/migrate/phase_jv_appendix_a.py` contains **no sqlite code** — no `import sqlite3`, no
  `.connect(`. *Precision note:* the plan's "no sqlite reference at all" is true of the code but
  false of the prose — its docstring at `:7` does say "for the SQLite database". It writes YAML
  to `data/jurisdictional_values/`. It is still dangerous in a different way: it overwrites the
  dual-store YAML of the very table carrying W5.1's false values, unguarded — but it is not a DB
  writer.
- **Only the replay script writes `data/guidebook.db`.**
- `_legacy_guard` is imported by exactly **7 of the 9** siblings. Importers:
  `migrate_bpc_metadata`, `migrate_connections`, `migrate_decisions`, `migrate_evidence_sources`,
  `migrate_gaps`, `migrate_items`, `migrate_slugs`. Non-importers: `init_database.py`,
  `phase_jv_appendix_a.py` — i.e. exactly the two that cannot reach the canonical DB anyway.

### `deps:` — R-11
`grep -c deps scripts/run_checks.py` → **0**. The registry declares dependencies per battery and
the runner never reads them, so a missing `pydantic` presents as **five blocking
`ModuleNotFoundError` failures** rather than one actionable message.

**Fix:** verify each selected battery's declared deps before running anything; abort with the
install command and **exit 2** — *the runner could not run*, which is a different fact from *a
check failed*. Also correct `check-registry.yaml:172`: `tests: {deps: []}` is false, since three
of the ten registered tests import pydantic transitively.

### `check-registry.yaml:174` — R-12
Still unquoted at HEAD, and reproduced this session: the `governance` battery parses to

```python
{'deps': ['pydantic'], 'description': 'Decision protocol',
 'doctrine recheck': None, 'adversarial-use.': None}
```

Two colons in an unquoted YAML scalar silently split one description into three keys. Reported
in five documents; still one line.

**Fix:** quote the string. **And add a `--selftest` assertion that every battery has exactly the
keys `{deps, description}`** — a successfully-parsing wrong shape is invisible to the current
C1–C7, which is why this survived five reports.

### `graph_audit.py:277` — R-13
The crash is in the **selftest path only**; the plain audit exits 0. Guard leg 3 with a loud
`[SKIP] … NOT-TESTABLE` that does **not** append a fabricated pass.

---

## Wave exit condition

Re-run the corridor walk's **stage 4a ordering probe** and **stage 9**:

- the probe is rejected **with nothing written** — no row, no ledger entry;
- `assess_cell.py` completes against an empty `gaps` table;
- `python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db` still reproduces the committed DB.

---

## Re-derivation notes

| Plan claim | Status | Evidence |
|---|---|---|
| FK check runs after `commit()`; `rollback()` rolls back nothing | **CONFIRMED** | `:162` / `:171` / `:174` / `:185` |
| Cited as `migrate_db.py:159-188` / `:161-183` | **CORRECTED** | the loop is `:154-189` |
| Emitted bodies self-commit | **CONFIRMED** | `emit_data_migration.py:201` |
| The four-line reorder cannot work | **CONFIRMED** | follows from the above |
| `is_bootstrap` at `:174` | **CORRECTED** | `:176`, plus the duplicate at `:261` |
| Undocumented duplicate in the rebuild path | **CONFIRMED** | `:250-267` |
| `MIGRATIONS_DIR.glob("*.sql")` non-recursive | **CONFIRMED** | `:81`, `:95`, `:114` |
| `next_gap_id` returns `GAP-1`; schema requires `^GAP-\d{3,4}$` | **CONFIRMED** | `assess_cell.py:429`, `schemas/evidence_state.py:167` |
| `db.py:next_gap_id` takes no `conn` | **CONFIRMED** | `db.py:149-158` |
| `assess_cell.py` refuses the canonical DB | **CONFIRMED** | `:487`, `:492` |
| W1.5's quoted PyYAML error | **CONFIRMED** | the file pins `==6.0.3`; the error names the *installed* 6.0.1, which has no RECORD. An earlier pass of this document called the quotation stale — that was wrong and is corrected here |
| `requirements.txt:4` is false | **CONFIRMED** | jsonschema is needed and CI hand-installs it |
| `session_pointer_resolvable` does not exist | **CONFIRMED** | zero hits |
| `grep -n deps scripts/run_checks.py` → nothing | **CONFIRMED** | 0 occurrences |
| `check-registry.yaml:174` parses to a wrong shape | **CONFIRMED** | reproduced this session |
| "Three unguarded direct writers" | **REFUTED — one** | the other two cannot reach the canonical DB |
