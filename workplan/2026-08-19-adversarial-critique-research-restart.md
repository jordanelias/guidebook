# 2026-08-19 — Adversarial critique of the research restart plan and the handoff

**Status:** CRITIQUE. Nothing here is executed. No schema change, no DB write, no migration.
**Subjects:** `workplan/2026-08-18-research-restart-plan.md` (the plan),
`workplan/2026-08-18-handoff-next-session.md` (the handoff, `aac7388`), and the execution
sequence in handoff §6.
**Method:** read-only. Every finding below marked **[PROVEN]** was reproduced by running code
against a throwaway copy of the database, not inferred from reading it. Findings marked
**[READ]** rest on file contents only.

---

## 0. What makes this pass different from the eight before it

The past eight days produced 106 commits, ~25 of which are explicit self-corrections of a
previous Claude session's claims (~30% of authored commits). The dominant failure mode, named
in the handoff's own §7, is *a count read without reading the rows it counted* — a claim that
is correct as arithmetic and wrong as a claim.

Reading harder does not fix that. So this pass ran things:

| Probe | What it established |
|---|---|
| `sqlite3` transaction probe | executescript/ledger atomicity, PRAGMA-in-transaction semantics |
| copy-and-mutate probe | whether a read command changes the committed binary |
| copy-and-DROP probe | what handoff §6 step 8 actually does to the schema |
| `research_batch_dod.py --selftest` | which rules are proven to fire |
| `table_connectivity.py` | the live walk metric and its exit code |
| direct DB queries | every count cited below |

Four of the six findings that block are ones no amount of document review would have surfaced.

---

## 1. Verdict

**The plan's research design is sound and should run. The handoff's execution sequence should
not run in the order given, and steps 5 and 8 should not run at all yet.**

The restart plan is the best document this repository has produced in a month: it is small, it
names its own weakest call, it writes acceptance before work, and its §7 correctly argues that
no other phase is a prerequisite. The handoff then buries it at position 10 of 10, behind a
schema refactor whose cost is not stated and whose effect is to disarm the only blocking data
gate the repository has — at the exact moment research starts writing data.

Six blocking findings follow. Four are proven by execution.

---

## 2. Blocking findings

### F1 — Step 8 breaks 17 tables and 4 views, and the schema-migration path will not notice **[PROVEN]**

Handoff §6 step 8: *"Expand `population_axis_map`→population↔ICF, retire `axes` and
`item_axis_links`, archive `items` to `_archived/`."* Step 5 folds this into **"one D-SCHEMA
migration."**

Against the live schema:

- **17 tables carry `REFERENCES items`**: `item_audit_runs`, `item_population_elaborations`,
  `item_population_links` (372 rows), `item_bpc_links`, `specifications`,
  `jurisdictional_values` (**109 live rows**), `economics_entry_specs`, `case_study_specs`,
  `source_value_extractions`, `spec_value_probes`, `term_item_links`, `item_axis_links`,
  `room_items`, `conflicts`.
- **3 tables carry `REFERENCES axes`**: `access_need_axis_map`, `item_axis_links`,
  `population_axis_map` (53 rows).
- **4 views read `items`**: `v_item_provenance`, `v_source_reach_all`, `v_item_extractions`
  (and `v_source_reach_all` also reads `specifications`).

I reproduced step 8 on a copy, using **this repository's own migration idiom** — migrations
057, 058 and 060 all open with `PRAGMA foreign_keys = OFF`:

```
DROP with FK OFF: SUCCEEDED SILENTLY (no error raised)
PRAGMA foreign_key_check      -> 702 violations
read jurisdictional_values    -> 109 rows (reads still fine)
INSERT INTO jurisdictional_values -> OperationalError: no such table: main.items
SELECT * FROM v_item_provenance   -> OperationalError: no such table: main.items
SELECT * FROM v_source_reach_all  -> OperationalError: no such table: main.items
```

The shape of the damage is the worst available one: **the drop raises nothing, every read
keeps working, and the failure only appears on the next write.** Every read-only audit in
`scripts/audit/` would report the database healthy.

It gets worse in one specific way. `migrate_db._apply_one_data_migration()` compares
`PRAGMA foreign_key_check` before and after and **raises on new violations** — but that guard
is on the **data**-migration path only. The schema path (`migrate_db.py:247`) runs
`conn.executescript()`, sets `user_version`, commits, and performs **no FK check at all**.
Step 5 is declared a D-SCHEMA migration. It would take the unguarded path. And because the
*next* data migration computes its `pre_violations` set after the fact, those 702 violations
would be baselined as pre-existing and forgiven permanently.

**This is not one migration.** It is a ~20-object dependency cascade requiring, at minimum:
drop-and-recreate of 4 views, a decision for each of 17 dependent tables, and a plan for two
populated dependents (`jurisdictional_values` 109, `item_population_links` 372).

### F2 — Step 8 disarms the repository's only blocking data gate, exactly when research starts writing **[PROVEN]**

`migration_reproducibility` is blocking. Its full invariant set is `PRAGMA user_version` plus
`COUNT(*)` on six tables (`scripts/audit/migration_reproducibility.py:57-62`). Live counts:

| Table | Rows |
|---|---|
| `evidence_sources` | **0** |
| `citation_mining` | **0** |
| `source_slug_links` | **0** |
| `gaps` | **0** |
| `connections` | **0** |
| `items` | **93** |

Five of six are already zero after the clean-room reset. `items` is the **only** table in the
gate's invariant set currently capable of detecting anything. Step 8 archives it.

After step 8 the blocking gate compares six zeros and a version integer. It is not weakened —
it is **vacuous**, and it becomes vacuous in the same migration that precedes the first batch
of real data writes. The repository's signature failure, named four times in CLAUDE.md §10, is
a green gate that examined nothing. Step 8 manufactures one on purpose.

### F3 — The plan's "fixed and non-negotiable" write path contradicts CLAUDE.md §4 **[PROVEN]**

Restart plan §1: *"The write path is fixed and non-negotiable: `scripts/db.py log-search` /
`add-source` for research rows, then `scripts/emit_data_migration.py` → `scripts/migrate_db.py`.
Never hand-edit the DB."*

`scripts/db.py:58-73`:

```python
def connect(dry_run: bool = False):
    conn = sqlite3.connect(str(DB_PATH), timeout=10)     # canonical DB, READ-WRITE
    conn.execute("PRAGMA journal_mode=WAL")
    ...
        if not dry_run:
            conn.commit()                                 # writes land in data/guidebook.db
```

`log-search` and `add-source` **write directly to the committed canonical database.**
CLAUDE.md §0 rule 4 names this exact case as forbidden: *"including ad-hoc `scripts/db.py`
writes to the committed DB."*

And there is no bridge. `emit_data_migration.py` accepts `--input <path>` or stdin — a
hand-authored SQL file. It has **no capture mode**: nothing reads what `db.py` just wrote and
renders it as a migration. So the prescribed sequence resolves to one of two bad outcomes:

- write via `db.py`, then hand-author SQL describing the same rows → the migration replays
  inserts that are already present, or drifts from them; or
- write via `db.py` and skip the migration → the committed DB carries rows with no migration
  provenance, which is the condition `migrate_db --rebuild` exists to detect.

**Steelman, and a correction to my own first reading:** past practice is clean. Fable's sweep
verified that all 11 commits touching `data/guidebook.db` this week shipped a
`scripts/migrations/` file — **11/11 compliance**. The defect is in the *plan's prose*, not in
the repository's habits. But the plan is what the next session will follow, and it instructs
that session to do the forbidden thing and calls the instruction non-negotiable.

**Fix, and it is small:** add `--emit-sql <path>` to `db.py`'s write subcommands, so they
render the INSERT they would have executed and commit nothing. One code path, no schema change.
Do it before the batch, not after.

### F4 — Any `db.py` invocation, including a pure read and including `--dry-run`, mutates the committed binary **[PROVEN]**

The committed database is in `journal_mode=delete`. `db.py connect()` unconditionally executes
`PRAGMA journal_mode=WAL` before yielding — on every subcommand, read or write.

```
sha before: 99fb2e58c70af6ff
sha after : 814680a6af3dfeb2
READ-ONLY COMMAND MUTATED THE COMMITTED BLOB
journal_mode now: wal
```

That was a bare `SELECT COUNT(*) FROM slugs`. `--dry-run` does not help: it calls
`conn.rollback()`, but `PRAGMA journal_mode` is not transactional and has already persisted.

`scripts/audit/readonly_db_open_audit.py` exists precisely to catch this class and **cannot see
it**, by its own scope rule: a script is in scope only if it *"executes NO write SQL"*
(criterion 3). `db.py` contains write SQL, so the whole file — including its ~30 read
subcommands — is exempt. **The audit's granularity is per-script; the defect is per-invocation.**

Consequence for the plan: the first research session runs `db.py` many times. Every invocation
dirties a tracked binary blob in ways the blocking gate cannot see (F2) and the read-only audit
does not cover.

### F5 — A data migration and its ledger row commit in two separate transactions **[PROVEN]**

`emit_data_migration.py:777` wraps every generated body in `BEGIN TRANSACTION; … COMMIT;`.
`migrate_db.py:194-199` then runs:

```python
conn.executescript(body)                       # body's own COMMIT closes the transaction
conn.execute("INSERT INTO data_migrations …")  # NEW implicit transaction starts here
conn.commit()
…
except sqlite3.Error:
    conn.rollback()                            # rolls back only the ledger INSERT
```

Probe result:

```
PROBE1 caught: IntegrityError: UNIQUE constraint failed: data_migrations.migration_id
PROBE1 rows in t after rollback: 1  -> ATOMICITY BROKEN (body survived)
```

The migration body is committed and permanent; the `rollback()` in the handler discards only
the ledger row. The migration is then **applied but unrecorded**, so the next `migrate_db.py`
run rediscovers it as pending and replays it. Migration DML here is plain `INSERT` with no
`ON CONFLICT` clause, so a replay either duplicates rows or dies on a PK collision.

`executescript()` also force-commits any pending work before it starts (PROBE3 confirmed), so
there is no outer transaction that could have held both halves.

**Fix:** strip the body's `BEGIN`/`COMMIT`, open one explicit transaction in `migrate_db.py`
around body-plus-ledger, commit once. Or keep the body transactional and move the ledger INSERT
inside the generated SQL.

### F6 — Schema migrations have no transaction wrapper and no FK check **[PROVEN/READ]**

Data migrations wrap in `BEGIN`/`COMMIT`. Schema migrations do not: `057`, `058`, `060` have no
top-level `BEGIN` — only `PRAGMA foreign_keys = OFF; … PRAGMA foreign_keys = ON; PRAGMA
user_version = N;`. Under `executescript()` each statement autocommits individually.

A schema migration that fails at statement 40 of 80 leaves the database **half-migrated with
`user_version` unbumped** — the bump is the last statement. The next run replays from statement
1 and dies on `table already exists`, with no clean recovery and no rollback. `057` is 6,828
lines. Step 5 proposes creating five tables, altering two, adding an FK and renaming a table in
one such file.

Related, and a live trap for whoever writes step 5: **`PRAGMA foreign_keys` is a silent no-op
inside a transaction.** Probe: `BEGIN; PRAGMA foreign_keys = OFF;` → reading the pragma returns
`1`. Today's schema migrations get away with it because they have no `BEGIN`. Fixing F6 by
adding a transaction wrapper, without moving the pragma outside it, would silently re-enable FK
enforcement mid-bulk-load and break the migration. **The two fixes must land together.**

---

## 3. Cross-document contradiction

### F7 — Two live documents from the same session name opposite success criteria **[PROVEN]**

Restart plan §4, acceptance criterion 6:

> `scripts/audit/table_connectivity.py` moves off **`FULLY-EVIDENCED WALKS: 0 of 80`**. One is
> the target. **This is the number that says research restarted**; every other metric in this
> repository can move without it.

Handoff §6, on the same first batch:

> `table_connectivity`'s walk metric will stay zero correctly.

Both are live. Both were written in the same session, hours apart. The handoff is right and the
plan is wrong, for a reason neither document states: `table_connectivity.py` stages 6, 7 and 8
all read **`FROM items`** (lines 44-48) — stage 6 is literally
`SELECT 1 FROM items i WHERE i.bpc_source_slug = :s`. Live: 87 of 93 items carry a
`bpc_source_slug`, resolving to **27 distinct slugs** — exactly the `27/80` in the audit's
"independent" column.

Archive `items` (step 8) and stages 6-8 read a table that does not exist. The metric the plan
names as *the* proof that research restarted becomes **permanently unreachable**, and the
audit itself starts raising `OperationalError`.

One of these two sentences has to be struck. Strike the plan's, and replace criterion 6 — see §6.

### F8 — A content catastrophe renders as a green check **[PROVEN]**

`table_connectivity.py` currently prints `!!` on **7 of its 8 stages**, reports
`FULLY-EVIDENCED WALKS: 0 of 80`, and **exits 0**.

The registry is blunter than I expected, and it makes this worse rather than better.
`governance/check-registry.yaml:1386` records `table_connectivity` as **`status: quarantined`**,
with the reason beginning: *"NOT A GATE, and registered here so that fact is recorded rather
than inferred from its absence."*

So the restart plan's headline acceptance signal — the number it says *"says research
restarted"* — is a **quarantined, explicitly non-gating instrument that cannot exit non-zero**,
and which F7 shows is scheduled to become unreachable. If any form of criterion 6 survives, it
needs a `--strict` mode with a floor, or it has to be read by a human every time and named as a
human judgment rather than a check.

### F9 — The gate's selftest proves 12 of 15 rules, and the plan claims 15 **[PROVEN]**

Restart plan §1: *"The gate … enforces R1–R15 … It has a `--selftest` that proves its checks
fire."*

Actual output: `SELFTEST: PASS — gate rejected the corpus AND all 12 seeded rules fired`, listing
R1–R8, R10, R11, R13, R14.

**Steelman, and the claim survives in weakened form:** R9, R12 and R15 *are* implemented
(`research_batch_dod.py:438`, `:484`, `:538`). They are not absent. They simply have **no seeded
selftest case**, so nothing proves they fire. Given that this repository has shipped a check that
examined nothing four separate times, "implemented but never observed to fire" is precisely the
state that has burned it before. Three seeded cases; small, bounded work.

---

## 4. SQL practice — DDL, DML, DQL, TCL, DCL

### DDL — better than the tooling's own prose suggests

`emit_data_migration.py` repeatedly warns *"SQLite has no CHECK on this column, so a bad value
applies silently."* True of the two columns it guards; misleading as a general statement. Live
schema: **123 CHECK constraints across 47 of 66 tables, 81 FK declarations, 20 tables with no
FK at all.** The declarative floor is real. `ENUM_GUARDS` covers exactly two columns
(`doi_resolution_outcome`, `url_resolution_outcome`) — it is a patch over specific known gaps,
not the primary defence, and the prose should say so.

Forward-looking, for step 5:

- **SQLite cannot `ALTER TABLE … ADD CONSTRAINT`.** The proposed FK on
  `search_executions.engine` requires the 12-step table rebuild — or, since `search_executions`
  is empty, a drop-and-recreate. Either way **5 views must be dropped and recreated in the same
  migration**: `v_coverage_jurisdiction`, `v_coverage_language`, `v_coverage_branch`,
  `v_coverage_priority`, `v_source_admission`. The step-5 list does not mention views.
- Renaming `term_item_links` → `term_slug_links`: that table also carries `REFERENCES items`, so
  it sits inside the F1 cascade. Do not treat the rename as independent of step 8.
- Forward-only + immutable-once-committed is correct and is being honoured (migration 060
  compensates 058 rather than editing it). No change needed.

### DML — one specific write the gate cannot see, scheduled as step 4

Handoff §6 step 4: *"Fix `GB`→`UK` (20 rows) before any FK exists."* Verified: 20 rows.

That is an `UPDATE`. `migration_reproducibility` compares `COUNT(*)` — **an UPDATE changes no
count and is invisible to the blocking gate by construction** (CLAUDE.md §0 rule 4 says exactly
this). The step is correct and should happen; it simply cannot be verified by the gate that
nominally guards it. Verify it with an explicit assertion in the migration or a registered
check, not by watching CI go green.

Second DML point: generated migrations use bare `INSERT`. Combined with F5's applied-but-
unrecorded window, replay is unsafe. `INSERT … ON CONFLICT DO NOTHING` for reference data would
make replay harmless; it is not a substitute for fixing F5, but it bounds the blast radius.

### DQL — the read path is the write path

Two defects, both already covered: F4 (every read opens read-write and flips to WAL) and the
scope hole in `readonly_db_open_audit.py`. The repository *knows* the right pattern — CLAUDE.md
§4 documents `sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)` and I used it for
every query in this document. `db.py` does not follow it.

**Fix:** `connect()` takes a `write: bool = False`; read-only opens use the `mode=ro` URI and add
`PRAGMA query_only = ON`; `journal_mode=WAL` is set only on write opens — or, better, dropped
entirely, since the committed artifact is `delete` mode and WAL's benefit (concurrent readers)
is worthless for a single-author repository whose database is a git blob.

### TCL — the weakest layer, and the one nobody has audited

F5 and F6 are both transaction-control defects, both proven, and neither appears in any of the
91 documents in `workplan/` or in `references/tooling-register.md`. There is no registered check
covering transaction behaviour at all. Concretely, the invariants that should hold and do not:

1. A migration body and its `data_migrations` row commit together or not at all. **(F5: they do not.)**
2. A schema migration and its `user_version` bump commit together or not at all. **(F6: they do not.)**
3. `PRAGMA foreign_keys` is set outside any transaction. *(Holds today by accident — no `BEGIN`
   in schema migrations. Would break the moment F6 is fixed naively.)*
4. Both migration paths run `foreign_key_check` before and after. *(Data path: yes. Schema path:
   no — F1.)*

### DCL — there is none, and the honest move is to say so

**SQLite has no `GRANT`, no `REVOKE`, no roles, no users.** There is no DCL layer in this
repository and there cannot be one. Everything currently performing access control is:

| Mechanism | Strength |
|---|---|
| CODEOWNERS on `governance/`, `schemas/`, `scripts/`, `.github/` | advisory; requires the required-check set to be configured |
| Branch protection on `main` | real (`"protected": true`) — but *which* checks are required is still an open owner decision (CLAUDE.md §7) |
| `mode=ro` URI convention | convention; F4 shows the main tool ignores it |
| POSIX file permissions | single author, single container — no separation at all |

The blocking-gate analysis in F2 is the load-bearing point: with five of six invariant tables at
zero, **the technical access control over the canonical database is currently near-nil**, and
step 8 takes it to nil. The three substitutes worth having, in order of cost:

1. `PRAGMA query_only = ON` on every read path — enforceable, cheap, and the closest thing to a
   `GRANT SELECT` that SQLite offers.
2. Settle the required-check set on `main`. Branch protection without required checks is a lock
   with no bolt. CLAUDE.md §7 already flags this as an open owner decision and warns not to
   require `DB integrity` until its backlog clears.
3. Promote `migration_reproducibility_deep` from advisory to blocking **once F1/F2 are resolved**.
   It is the only mechanism that would catch an `UPDATE`, and it is the answer to the DML gap
   above. It is currently advisory pending an owner decision — that decision is now load-bearing
   in a way it was not when it was deferred.

---

## 5. Steelman — where the plan survives attack

I tried to break these and could not.

- **The slug choice** (`room-acoustic-performance`) is correct, and the plan's §6.2 doubt about
  it is over-modest. Verified: `references/bpc-reasoning/` contains exactly two files, and one is
  `_template.md`. It is genuinely the only prior instance of the primary deliverable. The
  anchoring objection is real but is answered by the contamination design in §5 — and the
  alternative (a slug with no prior walk) would make pipeline failure and research failure
  indistinguishable, which is a strictly worse trade for a first batch whose purpose is to test
  the machinery.
- **The contamination design** (§5, the author's least confident call) is adequate as written.
  Reading the old doc after step 12 cannot contaminate the *record*, because the record is the
  migration and the search log — both immutable once committed and both timestamped before the
  read. The residual risk is only to the *narrative*, and the stated three-outcome frame already
  binds that. A second session doing the comparison is nicer but is not worth blocking on.
- **The Opus floor boundary** (§6.4) is settled by the plan's own structure and does not need an
  owner ruling. Steps 1-11 are search, retrieval and admission — mechanical. Step 12 is the DoD
  gate, also mechanical. Neither writes `best_practice_synthesis`. The reasoning doc is the
  Opus-gated artifact, and it is not in this batch's scope.
- **"No cull phase is a prerequisite"** (§7) is right, and I would extend it: **no schema phase
  is a prerequisite either.** See §6.
- **Migration-only discipline in practice** is clean — 11 of 11 DB-touching commits this week
  shipped a migration. F3 is a defect in the plan's prose, not in the repository's behaviour.

---

## 6. The recursive infrastructure loop — measured, and the way out

### The measurement

| | |
|---|---|
| Commits, past 8 days | **106** |
| Touching `workplan/`, `governance/`, `decisions/`, `sessions/` | **74** |
| Touching content paths (`references/bpc/`, `references/bpc-reasoning/`, `data/guidebook.db`) | **12** |
| Explicit self-corrections of a prior session's claims | **~25 of 84** (~30%) |
| Commits adding a BPC synthesis, evidence source, or specification | **0** |
| `workplan/` | **3.9 MB, 91 documents** |
| `references/bpc-reasoning/` (the primary deliverable) | **56 KB, 2 files — one is the template** |
| Python scripts / audit scripts / registered checks | **104 / 30 / 65** |
| Database tables empty | **43 of 66** |
| `evidence_sources`, `specifications`, `gaps`, `search_executions` | **0, 0, 0, 0** |

**The apparatus outweighs the deliverable it exists to produce by roughly 70:1 by volume, and
this week it outproduced it 84:1 by commit.** One commit this week is literally titled *"census
the apparatus by recursion depth."* The current branch is an adversarial critique of a workplan,
following a session whose adversarial pass overturned four claims made by a plan written to
correct a digest broken by a previous critique.

### The diagnosis

The loop is not caused by bad judgment, laziness, or insufficient rigour. It is caused by a
structural property of the acceptance criteria: **every criterion in play can be satisfied by
the apparatus alone.**

Look at the restart plan's own §4. Criteria 1-5 are "a gate exits 0", "a rebuild reproduces",
"a test scores 72/72". Criterion 6 is "a metric moves" — and F7 shows that even that one is
scheduled to be made unreachable. Not one criterion is *"a disabled person could get an answer
to a question they could not answer before."*

When every acceptance criterion is an apparatus criterion, building more apparatus is always a
locally valid way to make progress — and it is always cheaper and more certain than research.
Each pass is individually correct. The loop is the sum of correct passes optimising a measure
that content does not move.

The census-and-cull approach treats this as a *volume* problem: too much apparatus, cull some.
That is the wrong axis and will not work — cutting 5,000 of 101,300 lines (Fable's own verdict
on the cull plan) leaves the incentive untouched, and the cull plan itself has now consumed two
sessions and produced a document that another pass found under-scoped.

### The exit

**Add one acceptance criterion that no amount of apparatus can satisfy, and put it first.**

> **One answered question, published.** A single research question, with a determination, its
> governing sources, its population-match grading, and its search log including empties — visible
> as rendered output, not as a row count or a green check.

That criterion cannot be met by a script, a registry entry, a check, a decision record, or a
plan. It can only be met by doing the research. It is also almost exactly the restart plan's own
first batch — which is why the plan is right and its position in the queue is wrong.

**Replacement for restart-plan criterion 6** (which F7 kills): the handoff already proposed a
better one and it should be promoted into the plan verbatim — *one consolidation bucket holds ≥2
independent roots, every search logged per R8 including its empties.* Add: **and the resulting
determination is rendered and readable.** The rendered artifact is the part the apparatus cannot
fake.

---

## 7. Recommended sequence — inverted from the handoff

The handoff runs schema first (steps 4-9) and research last (step 10). **Invert it.** Nothing in
steps 5-9 is required to log a search or admit a source. The tables the first batch writes —
`search_executions`, `search_candidates`, `evidence_sources`, `source_slug_links`,
`evidence_population_match` — all exist today. The inputs it reads — `slugs` (106),
`term_aliases` (2,382), `jurisdictional_values` (109) — are all populated today.

**Steps 5 and 8 are a schema refactor for a research programme that has never run one batch.
They optimise a pipeline with zero throughput, and F1/F2 show the cost is far higher than "one
D-SCHEMA migration."**

Proposed order:

| # | Action | Blocks on | Why here |
|---|---|---|---|
| 1 | Fix F3 — add `--emit-sql` to `db.py` write subcommands | — | The batch cannot comply with CLAUDE.md §4 without it |
| 2 | Fix F4 — read-only default + `query_only` in `db.py connect()` | — | Same session, same file, ~20 lines |
| 3 | Fix F5 + F6 **together** — one transaction for body+ledger; wrap schema migrations; keep `PRAGMA foreign_keys` outside the wrapper; add `foreign_key_check` to the schema path | — | F6's naive fix breaks migrations; they must land as one change |
| 4 | Seed 3 selftest cases for R9, R12, R15 (F9) | — | Small; closes the "never observed to fire" gap before the gate is first used in anger |
| 5 | **Run the first research batch** (restart plan §§2-3, unchanged) | 1-4 | The exit criterion. Everything above exists to make this batch's writes legitimate |
| 6 | Render the determination and read it | 5 | The part apparatus cannot fake |
| 7 | `GB`→`UK` (20 rows), with an explicit in-migration assertion (DML §4) | — | Independent; do it whenever, but verify it deliberately |
| 8 | Owner ratifies buckets / amends `jurisdiction-philosophy.md` §2.3 / settles O1 | owner | Genuinely owner-gated; unblocked by nothing above |
| 9 | Re-scope step 8 as its own migration with the full F1 cascade | 5, 8 | Needs the batch first — see below |
| 10 | Re-declare the retired `min_items` guards; promote `migration_reproducibility_deep` | 5 | Both need non-zero subjects to be meaningful |

**On step 9 specifically:** do not archive `items` until the reproducibility gate has a non-zero
invariant table that is not `items` (F2). The first batch supplies exactly that — it populates
`evidence_sources` and `source_slug_links`, two of the gate's six. **Running the batch first is
what makes step 8 safe to run at all.** The handoff's ordering has this precisely backwards.

---

## 8. Owner-gated / unsettled — flagged, not decided

1. **Strike restart-plan §4 criterion 6** and adopt the handoff's replacement plus a render
   requirement (F7, §6). Editorial, but it changes a plan's stated success condition — worth an
   explicit nod.
2. **Promote `migration_reproducibility_deep` to blocking** once F1/F2 are resolved. Currently an
   open owner decision (`references/tooling-register.md` §4.2); F2 makes it materially more
   urgent than when it was deferred.
3. **Settle the required-check set on `main`** (CLAUDE.md §7, DCL above). Branch protection with
   no required checks is the whole of this repository's access control.
4. **Whether step 8 happens at all.** F1 prices it honestly for the first time: ~20 objects, 4
   views, 2 populated dependents. That price was not visible when it was ratified as part of R3.
   It may still be worth paying — but it should be re-ratified against the real number.
5. **Deferred, not answered:** I did not evaluate the cull plan (independent per its own §7), the
   ICF expansion floor (O1), municipality selection (O4), or whether `slugs` needs a type column
   (O5). None blocks the sequence in §7.

---

*Every count, SHA, line reference and probe result above was derived from the live repository on
2026-08-19. Nothing was carried forward from a prior document without re-deriving it. Where I
corrected my own first reading — F3's steelman — the correction is shown rather than silently
folded in.*
