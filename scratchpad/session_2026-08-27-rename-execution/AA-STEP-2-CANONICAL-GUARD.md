# Step 2 — P0.1/P0.2, the canonical-write guard, argued both ways

---

## C-4 · Wire the guard at all?

**AGONIST.** `dbcore.is_canonical()` exists **solely** to refuse writes to the committed database.
Measured: its only callers are its own selftest (`scripts/dbcore.py:469-470`). `connect()` never calls
it, and `db_path()` **defaults to canonical** when `GUIDEBOOK_DB_PATH` is unset
(`dbcore.py:51-59`). So any script that forgets the env var writes the committed file — failure mode
#1 in the instrument's §12.4, with the written mitigation unwired.

**ANTAGONIST — I already proved this guard does not cover the biggest write.** C-F established that
`scripts/migrate_db.py` opens the database with raw `sqlite3.connect` at `:366`, `:440`, `:504` and
**never imports `dbcore`**. The rename migration will not pass through this guard. So what does it
actually protect, and is it worth a change at all?

**Measured — the blast radius is small and entirely `db.py`:**

```bash
grep -rln "import dbcore\|from dbcore" --include=*.py scripts/ tools/   # -> 3 files
```

`db.py` is the only substantive consumer, using `connect(dry_run)` to write and
`connect(readonly=True)` to read.

**RESOLUTION — wire it, on a narrower and more honest claim than `REPAIR-PLAN` makes.** It does not
protect migrations and never did. It protects **the CLI writers**, which is exactly where an ad-hoc
session forgets the env var — and a rename session runs many ad-hoc scripts. `REPAIR-PLAN`'s
*"safety: nothing else runs first"* remains overstated; the task is kept on its own smaller merit.

---

## C-5 · Does the guard need an override? — **`REPAIR-PLAN` says yes; the measurement says no**

**AGONIST (`REPAIR-PLAN` P0.1).** *"Migrations need an explicit override; F6 specifies its shape."*

**ANTAGONIST.** Migrations do not pass through `dbcore.connect()` at all (C-4), so there is nothing
for an override to unblock. And the runbook is explicit that **every** `db.py` write goes to a scratch
copy: *"cp data/guidebook.db $SCRATCH, point `GUIDEBOOK_DB_PATH` at it inline on every call"*
(`CLAUDE.md` §4). So there is **no legitimate canonical write through this path to permit.**

**RESOLUTION — no override, and that is the stronger design.** §1: do not add what nothing needs. **A
bypass that exists will be used**, and an escape hatch on a guard whose entire value is refusal is the
thing most likely to make it decorative. If a legitimate canonical write through `dbcore` ever
appears, the override is added then, with the case that justifies it. `REPAIR-PLAN`'s override
requirement rests on the same false premise as its ordering claim.

---

## C-6 · Refuse a `--dry-run` against canonical too?

**AGONIST (refuse only real writes).** `dry_run=True` rolls back, so it cannot commit. Refusing it
blocks a harmless rehearsal.

**ANTAGONIST.** It still opens the committed file **read-write**. The runbook's discipline is not
"don't commit to canonical", it is *point the env var at a scratch copy **on every call***, and the
sha256 check the runbook uses to prove the canonical file was untouched does not distinguish a
rollback from a write at open time. `dbcore`'s own `connect()` docstring records a prior incident of
exactly this class: setting `PRAGMA journal_mode` *"rewrote the committed blob on EVERY invocation …
including pure reads and including `--dry-run`"*.

**RESOLUTION — refuse ANY non-readonly open of canonical.** The precedent is in the file: a rehearsal
that opens the committed blob read-write has already dirtied it once here. Reads are unaffected —
`readonly=True` opens `mode=ro` and sets `query_only`.

---

## C-7 · P0.2 — how many skill lines actually break?

**`REPAIR-PLAN` says four.** Measured across `skills/`, eleven lines set
`GUIDEBOOK_DB_PATH=data/guidebook.db`, but classifying each by the command it runs:

| | lines | effect under the guard |
|---|---:|---|
| reads (`db.py connections`, `next-id`) | 5 | unaffected — `readonly=True` |
| inline python inspection | 2 | unaffected — read-only queries |
| **writes** (`update-connection` ×2, `add-gap`, `add-connection`) | **4** | **would raise** |

`connection-auditor_SKILL.md:185,192,199` · `connection-discovery_SKILL.md:219`.

**RESOLUTION — `REPAIR-PLAN`'s four is exactly right**, and the reason it is four rather than eleven
is that the guard is write-scoped. They ship in the same commit as the guard, because landing the
guard alone turns those four skill lines into runtime failures.
