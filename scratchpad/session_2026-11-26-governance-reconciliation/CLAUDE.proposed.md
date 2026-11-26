# CLAUDE.md — working guide for the Accessible Built Environments Guidebook

## Goal

The owner's goal, verbatim (2026-11-20): *"we research, we record, we verify we recorded things accurately, we
evaluate things in context with other related things, we synthesize then show"*.

**The project is simple** (owner, 2026-11-25: *"this is a simple project where we build as little machinery as possible to enact our goal"*; also *"Remember that this project is simple!!!"*). Meet the goal with the least machinery: §8's order applies to every task, and a table, verb, check or rule that the goal does not need is not built.

The project is a database that records research properly, and a pipeline that processes it; `base` is the owner's
request layer, standing where the owner would otherwise ask for a topic directly. The owner reads only English, so
three things are never to be got wrong:

1. **Fetch before you write any author, title or figure.** A bibliographic field is never written from memory.
2. **Keep the original beside every translated figure,** and show an English rendering that records who translated
   and who reviewed it, and when (`translations`; `db.py translations --show` prints each reviewed one beside its
   original); never English into `claimed_value` or `claimed_unit`.
3. **Co-1 co-producers are evidence and stay credited.**

A reference on architecture, accessibility and built-environment standards centred on **disabled
people**. Fixed doctrine: a **thinking tool and advocacy project, not an authority** — *"the purpose
of this guidebook is to get people to ask the right questions."* Not a prescription manual, not a
legal authority, not a substitute for professional judgment. "Inclusive / accessible / universal"
here always means *inclusion of persons with disabilities*.

This file holds **process, workflow and rules only**; every volatile fact (counts, versions, CI state) is derived,
never stated. Where it disagrees with `decisions/DR-2026-08-19-research-restart-operative-instrument.md`, that
instrument wins and this file is what to correct — **unless a live owner ruling has superseded the instrument itself,
per rule 0, in which case the ruling wins over both.**

When a sentence in this file is found wrong, fix the sentence and put the account of the error in the commit message;
`git log -p CLAUDE.md` is the record. This file is loaded into every turn, so every line is paid for on every turn.

---

## 1. Run these first

`/orient` starts any session; run `/session-open` before the first Bash call of a batch (§7). SessionStart runs
`.claude/hooks/ensure-deps.sh`, which exits 0 even when it fails, and without `pydantic` the governance battery is red
on untouched `main`: check `python3 -c 'import pydantic, jsonschema'` before believing a red result. **Never
`pip install -r requirements.txt`** (its PyYAML pin cannot replace the system copy, so nothing lands); install packages
individually. The dependency list's one home is `governance/check-registry.yaml`'s `batteries:`.

```
python3 scripts/run_checks.py --list     # registry + quarantine (runs nothing)
scripts/preflight.sh                     # THE gate: registry selftest, then the checks your diff vs origin/main warrants
scripts/preflight.sh --explain           # the same, with why each check was or was not selected
```

**Run the gate once, when the diff is ready to open a PR** (owner, 2026-09-23: *"stop running suites so frequently …
interrogate their merits"*), and never re-run a check when nothing it reads has changed. A targeted question takes
`run_checks.py --battery <name> --kinds <kinds>` (or `--battery <name> --changed-from origin/main`): read `selected N
of M`; exit 2 means the selection was refused or matched nothing. `--all` is for a corpus-wide question only. A bare
`run_checks.py --changed-from` skips the selftest, where a rename fails (rule 4). Before trusting a green result, ask
whether the check could have gone red on the defect in front of you; one red on untouched `main`, or one that examined
nothing (§5(a)), tells you nothing about your diff.

**Use the project's own agents and commands before general-purpose ones.** Agents in `.claude/agents/`: `repo-sweep`
for rule-4 caller sweeps and derived counts, `db-census` for row counts and the UNWRITABLE set (§4), `antagonist` for
the adversarial pass. Commands in `.claude/commands/`: `/orient`, `/session-open`, `/adversarial` after substantive
work, `/batch-done` as the only definition of "finished". Before invoking a skill, check that it does not presuppose
the deleted item layer (§7).

---

## 2. The rules that stop you

Each rule names what enforces it. **"NOT ENFORCED" means you are the gate.**

**0. A live owner statement supersedes every prior ratified record it touches, on contact.** Record
the supersession; never weigh the ruling against the paperwork it changes. A DR, a RULE, an ADOPTED
directive are what a ruling *changes* — never an argument against it. Numbered 0 because the rest of
this file tilts the other way.
*Proof: on 2026-08-18 the owner ruled `axes` a bad coined term, marked "do not relitigate", and the
next day a batch framed four of five searches on bare `axis_code`, hiding a second mechanism.*
→ **PARTLY ENFORCED** by `supersession_backpointer_audit`, for supersessions a `SUPERSEDES` line
names. Naming them is yours.

**1. Commit format.** `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, from
`date -u '+%Y-%m-%d %H:%M'`. Use `governance` when no project skill fits.
→ Enforced by `scripts/ci_helpers/check_commit_msg.py` on **push events only** (the `commit-msg` job of
`.github/workflows/ci.yml`); never on a PR.

**2. Attestation on synthesis paths.** A changed `.md` file under `references/connection-reasoning/`, `decisions/` or
`sessions/` needs `attestations/<dir>_<stem>.json`, valid against `schemas/attestation.schema.json`.
→ Enforced by `attestation_presence` and `attestation_schema` (both blocking). **No gate reads the free text for
meaning**; you are its gate.

**3. Never write `data/guidebook.db` directly.** Migrations only, by the write path of §4. Committed migrations are
append-only and immutable: fix forward with a compensating migration.
→ Enforced by `migration_reproducibility` (blocking), **which compares row COUNTS only** — an UPDATE is invisible to
it. `migration_reproducibility_deep` compares every row and is **advisory**.

**4. A rename or removal is not done until the callers are swept.** **A VIEW IS A CALLER. So is a skill, the check
registry, and prose.** Grep `sqlite_master` as well as the tree, and **treat a 0-row object as unproven, not clean.**
After changing any checked value or name, `git grep` `governance/`, `references/`, `architecture/`, `scripts/`,
`skills/` and `.claude/` for sentences restating it.
→ Enforced by `schema_reference_audit` (blocking) for names that must resolve in the schema, and by
`run_checks.py --selftest` C7 for registry basis refs. **Prose callers are not covered.**

**5. Never write the same fact into a second table. Point, do not copy** (owner, 2026-08-24: *"It is better to have a
table cell point to another table cell than to rewrite."*). Each stage (§3) holds only its own data and reaches earlier
stages by pointer on the shared reference ID. **A parity check is not a fix**: it makes a dual home permanent. To drop
a column a committed data migration INSERTs, the schema migration must replay after every one of them (an
`-- AFTER_DATA:` line, read by `migrate_db.build_plan()`): grep `scripts/migrations/data_*` first, then retire the
writer, then the readers, then NULL forward.
→ **NOT ENFORCED — you are the gate.**

**6. Commit the scratchpad AND the agent transcripts at every natural break**, not at session end.
`python3 scripts/preserve_transcripts.py` copies transcripts out of ephemeral `~/.claude/projects`, which a fresh clone
does not inherit (the SubagentStop hook runs it for subagents; committing is yours); `--check` says what is
unpreserved. If no session directory exists, create it (`/session-open`). `governance: session command log
[YYYY-MM-DD HH:MM]` is a complete commit message.
→ **NOT ENFORCED, deliberately.** `--check` is red for the whole life of a session, and a check that is red by
construction teaches its reader to ignore it.

**7. No hand-written counts.** Derive every volatile fact — row counts, schema version, CI state, the active plan —
from the live repo; where a figure cannot be generated, stamp it with its date and a drift warning.
→ **NOT ENFORCED — you are the gate.**

**7a. A NUMBER IS WRITTEN AS THE COMMAND THAT COMPUTES IT, NOT AS ITS RESULT** (owner, 2026-09-16) — in a document, a
comment, a registry entry, a commit message or a criterion. Where the number must also appear, the command stands
beside it and the reader is told to re-run rather than trust. **Ask of every figure you are about to type: could this
be wrong tomorrow with nothing going red?** If yes, it is hard-coded, whatever its shape — a literal, a threshold, a
`min_items`, a list, a glob, or a sentence.
→ **PARTLY ENFORCED.** `run_checks.py --selftest` C9 falsifies a `no_floor` reason that claims an empty subject over a
live one. **Everywhere else, prose above all, you are the gate.**

**8. DERIVE IT, OR NAME WHO JUDGED IT. Never curate a fact the machine can compute.** A vocabulary comes from the
column's own CHECK; an ordering from the live FK graph; an identifier from the union of its homes; a tier from the
ladder; the set of writable tables from the writers — never from a list kept beside the thing it describes. **Where
judgment IS genuinely required, the script asks for it**, constraining the answer to the live vocabulary, demanding
the evidence, and recording the answer and its warrant in named columns. The model fills a field. It never invents a
value or a vocabulary term, and never supplies a number the schema could have computed.
→ **PARTLY ENFORCED** by `dbcore.check_values()` (vocabularies), `identifier_floor_audit` (identifiers),
`dbcore.writable_tables()` (the capture set) and `adjudication_integrity` (tiers);
`python3 scripts/audit/derived_not_curated_audit.py` judges the shapes it covers — run it, and do not count violations
by grepping `choices=`. Otherwise you are the gate: look for a typed list that duplicates a column's CHECK.

**9. Do not watch PRs. Open the PR last** (owner instruction, 2026-09-23). Do not call
`subscribe_pr_activity` (either server's) and do not schedule `send_later` or `create_trigger`
check-ins: this is the owner saying the PR is not to be watched, which the harness's default-subscribe
instruction defers to. **Creating a PR subscribes the session by itself** (observed on #158: a
`subscription.created` event arrived with no subscribe call), so call `unsubscribe_pr_activity` for
it immediately after `create_pull_request`, before anything else. Open the PR once, when the diff-scoped gate (§1) is clean and the work is
finished, and push nothing afterwards except a deliberate change. A commit that only carries the
append-only logs (§7) goes in with the work, or carries `[skip ci]` before the timestamp. The final
push to a PR is never `[skip ci]`, or its head has no CI result. The owner reads CI on GitHub.
*Proof: in the 2026-09 transcripts most wake-ups on subscribed PRs were a CI run reporting green,
and each did no work but still cost a full-context turn. The batch that opened its PR at the end
used a fraction of the tokens of the batch that opened early.*
→ **PARTLY ENFORCED** once the owner adds both `subscribe_pr_activity` tools, `send_later` and
`create_trigger` to `permissions.deny` in `.claude/settings.json`: that stops explicit subscription
and polling, but not the subscription PR creation makes, so the unsubscribe step is yours. Never
deny `unsubscribe_pr_activity`. `ci.yml`'s `concurrency` block
cancels superseded runs, which saves runner time but does not stop a wake-up.

**10. Research and the tooling it uses ship apart.** A schema migration, a new `db.py` verb, a new check — anything
Layer 0/1/2 (§3) — goes in a tooling-only PR, merged to main first; a research batch's rows go in their own PR after.
A writer gap discovered mid-batch is filed as a GAP and either left unwritten or written through verbs the CLI already
has; it is never patched with hand SQL inside the batch's data migration. `data/guidebook.db` shipping with a
schema-only migration (no `data_*.sql` file alongside) is the ordinary shape of a schema bump, not a violation.
→ **PARTLY ENFORCED** by `research_tooling_separation` (advisory). It classes `governance/check-registry.yaml` as
`governance`, so a registry entry landing new tooling beside research rows is invisible to it.

---

## 3. The layers, and the spine

**Owner ruling 2026-09-09** — the project is five layers:

> **Layer 0** is Claude.md and tools/scripts that ensure that Layer 1's architecture/shape/pipelines/schema etc are working
> **Layer 1** is code architecture and data shape and pipeline orchestration and schematic compliance etc — it is what guides all processes in the pipeline
> **Layer 2** is comprised of each stage in the pipeline including its tools/workflows/processes/scripts etc
> **Layer 3** is the actual data being recorded in the tables
> **Layer 4** is supplementary data

Full record: `references/project-standards.md`, 2026-09-09.

**THE CANONICAL SPINE. This line is checked; do not hand-edit it.**

    SPINE: base -> research -> evidence -> judgment -> synthesis -> specification -> render

`governance/pipeline-contract.yaml`'s `stages:` is the single home of the stage ids; the line above is a rendering of
it, and `base` is the vocabulary layer the machine gates as a stage.
→ Enforced by `claude_md_spine` (blocking). Never spell the stages out a second time in this file.

| Stage | Holds |
|---|---|
| **base** | The vocabularies and registries every other stage points into |
| **research** | What was searched, screened and mined, plus the clue store |
| **evidence** | What was admitted, its identity and its verification |
| **judgment** | What each source asserts for each parameter (the extraction), whether it is sound, and how it weighs |
| **synthesis** | What the judgments say together — weighing, convergence, cross-slug findings |
| **specification** | The determination: *therefore 1200 mm, marked ●* |
| **render** | Book surfaces, read from the database when rendered (owner, 2026-08-27); no committed file is one |

**Rule 5 is unusable without this table.** Table-to-stage judgments live in `governance/stage-map.yaml`. **A
cross-stage view IS the pointer** — a view joining two stages on the shared reference ID is what "point" means in SQL
— **and is therefore the most protected object in the schema: before deleting any view, ask which stages it spans.**
Every stage points into `base`, so a view reading one stage plus `base` is not counted as crossing. A walk may
re-enter an earlier stage (a reasoning document can yield research leads); that is write order, not what a table may
hold.

---

## 4. Writing the database

`data/guidebook.db`, SQLite, committed as a binary blob. `PRAGMA user_version` is the schema version.
**There is no `sqlite3` CLI** — use Python, read-only:

```python
import sqlite3
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
```

**THE WRITE PATH IS ONE SENTENCE:** scratch copy → `scripts/db.py` subcommands →
`scripts/research/emit_batch_sql.py` → `scripts/emit_data_migration.py` → `scripts/migrate_db.py`.
`cp data/guidebook.db $SCRATCH`, then point `GUIDEBOOK_DB_PATH` at it **inline on every call** — the harness resets env
between shells. The canonical DB's sha256 must not move until the migration is applied.

**Do not hand-write SQL against a table the CLI can reach.** If you find one it cannot, that is a coverage bug to fix,
not a licence to bypass; the capture set is `dbcore.writable_tables(conn)`, and a table it misses is a defect fixed
there. Exception (owner, 2026-11-21): a qualitative judgment or wording cell may be corrected by hand in a data migration,
with the old value, the new value, the reason and the session recorded in the migration header and in the gap's
resolution. Ask the owner before treating any other kind of column as qualitative.

**`db.py` refuses, and that is its whole value.** A writer that merely INSERTs is worse than hand SQL because it looks
safe. One refusal is deliberately absent and must stay absent: `add-population-match` does not enforce uniqueness on
(ref_id, population), so a dissenting adversarial grade lands as a second row and divergent grades read as a contest.

**Schema shape (owner, 2026-11-06): one value per cell, and each fact in the cell that names it.** A list, a JSON
array, a delimited string, a prefix that says what the rest of the cell means, or a correction appended to a note is
data joined in a cell or in the wrong one; give each kind its own column (a foreign key where a table exists) and each
repeated value its own row. Run `python3 scripts/audit/joined_cells_census.py` before and after a schema change.

**Vocabularies come from the schema, not a list in code.** `dbcore.check_values()` reads the column's own CHECK; live
rows are a *sample* of a vocabulary, never the vocabulary. **Never compute a ref_id by hand** —
`dbcore.next_ref_id(conn)` (`python3 scripts/db.py next-id ref`) takes the high-water mark over the UNION of every
table holding a ref_id.

**Schema change:** a new `scripts/migrations/NNN_slug.sql` that bumps `user_version`. Verify with
`python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db`.

**A NOT NULL foreign key into an EMPTIED table makes that table unwritable.** The refusal comes only at INSERT, so the
schema looks healthy, a rebuild reproduces it and every gate stays green. Derive the UNWRITABLE set before planning
any write (the `db-census` agent; its file holds the probe), and never quote it.

---

## 5. The three failure modes that are real

**(a) A gate that passes having examined nothing.** Every check must print `EXAMINED: <n>`; `run_checks.py` reports
zero-subject passes as NOTHING-IN-SCOPE and escalates blocking-and-vacuous ones. **When a check passes, confirm it had
a subject.**

**(b) Prose that contradicts the database.** See rules 7 and 7a.

**(c) A fabricated citation passing green gates.** A gate that asks whether author fields are *populated* passes
invented authors — including the erasure of a Co-1 paper's disabled co-authors. **Verification must leave an
artefact:** `scripts/research/retrieval_log.py` logs every retrieval as a manifest line (URL, time, status, byte count,
sha256), and `--verify-authors` diffs stored data against the logged payload. An artefact a search-execution or
admission gate must find is committed; a large PDF, page or extracted text is logged by where it was retrieved from,
not committed (owner, 2026-11-06).

---

## 6. Evidence model

`governance/tier-system.md` is operative. **T1** primary controlled research · **Co-1** lived
experience / participatory design, **co-primary with T1** under CRPD Art 4.3 · **T2** synthesis ·
**Co-2** OT professional-body CPGs · **T3** grey primary · **T4–T6** the regulatory stratum, walled
off from full-strength anchoring.

Markers: **●** confirmed · **◐** policy/standards only · **○** grey, thin or unverified (the source could not be retrieved). Unmarked is an error.
Cell states: the `specifications.state` CHECK (`dbcore.check_values`). No row is stored for a parameter and lens a
determination does not concern (owner, 2026-10-29, OR-1).

**Co-1's warrant is co-production.** The disabled people who produced the work are part of the
evidence, not metadata. Erasing them while claiming the tier is the worst failure available here.

Work from the **ICF/access-need frame with codes AND names**, never bare codes, never population umbrellas. **The
crossing is JUDGMENT's output** (owner, 2026-08-27): harvest concepts at evidence (`db.py observe-term`, verbatim and
unjudged), adjudicate at judgment. Zero links **after judgment** is a defect. Only an Opus-class model or above (Fable-class
included; `governance/decision-protocol.md` §4.2; owner, 2026-07-25) writes a determination (`specifications`).

**Both halves of the determination's key are RULED.** Subject: the canonical parameter, `parameter_id` (owner,
2026-08-26; read its five-clause ACTION before touching any of this: `grep -n 'judgment object is the'
references/project-standards.md`); `items` is a render rollup derived from specifications, never a key. Lens: at least
one of the identity, ICF and access-need columns, with real FKs (owner, 2026-08-28, as relaxed by D-0182);
`population_code` and the medical lens are retired. `slug × population` is no part of the key: `base_taxonomy_identity`
IS the identity lens, and that key is the traversal D-0184 rejected. Verify with `PRAGMA table_info(specifications)`,
and search for both halves of a question before calling either open.

---

## 7. Traps

- **A publisher block (403, JS challenge, new paywall) is not terminal (research contract R10).** Find a snapshot with
  `curl -sS "http://archive.org/wayback/available?url=<host+path, no scheme>"` and fetch
  `https://web.archive.org/web/<timestamp>if_/<original URL>`; on a connection reset, retry once and try the plain
  `/web/<timestamp>/` form. Persist what comes back through `retrieval_log.fetch()`. Resets on every form while a
  known-good control URL also fails mean the session's proxy, not the snapshot.
- **`.ignore` hides frozen records from ripgrep and the Grep tool**; its entries are the list (`cat .ignore`). **Owner
  rulings live overwhelmingly in `sessions/`.** `git grep`, `grep -r` and a Glob that names the directory see through
  it. **Never report a ruling absent from a search that could not have seen it.**
- **`scratchpad/CURRENT` names the session running now, and it moves at OPEN.** `sessions/LATEST` and
  `LATEST-RESEARCH` move at CLOSE, so both name the PREVIOUS session for the whole life of the current one. `CURRENT`
  holds the DB session stem (`session_YYYY-MM-DD-<slug>`), and its scratchpad folder must be named identically;
  `/session-open` sets both. If your PR merges mid-session, move `CURRENT` and the folder together, in one action, or
  the command log is misfiled.
- **Session ids: bare stem in the DB, `.md` in pointers and `emit_data_migration --session`.** The wrong form scopes a
  gate to nothing and it passes green.
- **`git rebase` and `git checkout -B` are blocked in this harness.** `git merge origin/main` reaches the same state
  without rewriting history.
- **THE ITEM LAYER IS GONE FROM THE DATABASE AND STILL LIVE ON THE READING SURFACE.** `references/` and `working/` still
  publish prior-version item codes whose names state their answers (`E-08 Corridor Clear Width (≥1200 mm Minimum on
  All Primary Routes)`). The owner deleted the layer because *"if E-08 already exists then the work is predisposed to
  filing into a container that already exists, and that biases every finding."* **Treat every `[A-Z]-NN` code you meet
  as prior-version content, never as a container to file into.** Derive the live surface before framing anything:
  `grep -rEl '\b[A-Z]-[0-9]{2}\b' references/ working/`
- **If you add a `SessionStart` hook, APPEND it — never insert at index 0.** `research_contract_hook.py` reads
  `SessionStart[0]["hooks"][0]["command"]` by index; an insert turns the blocking `research_contract_sync` red.
- **PI versioning is intentional**: the numerically highest `governance/project-instructions-v*.md`
  (`ls governance/project-instructions-v*.md | sort -V | tail -1`) serves the claude.ai surface and lags doctrine.
  Prefer the ledger and recent DRs.
- **Don't run `scripts/bootstrap.sh`** — PAT-gated, for the claude.ai surface.
- **TWO TRACKED FILES APPEND ON EVERY TURN** (`transcripts/harness_*/main.jsonl`, `scratchpad/<session>/commands.jsonl`),
  so a "tree clean?" gate is unsatisfiable while a session is live. Do not answer the harness stop hook with a commit
  when only these are dirty; commit them at a natural break (rule 6). The real question is
  `git diff --quiet -- :/ ':(exclude)transcripts/' ':(exclude)*commands.jsonl'`. SessionStart runs
  `scripts/fix_stop_hook_loop.sh` silently to add that exclusion to the hook; whether it took:
  `grep -c stophook.ignorePath ~/.claude/stop-hook-git-check.sh`.

---

## 8. Deleting is as cheap as adding

**Adding apparatus carries the burden of proof; removing it does not.**

- **Code, checks, scripts, dead tables and views: delete them.** No owner gate. You need *evidence* — unreferenced,
  vacuous after a real batch, or superseded — not permission. Record it in the commit.
- **Git history is the archive for CODE.** Do not copy scripts to `_archived/`; it is for retired reader-facing
  *content*.
- **Owner sign-off is required for content and doctrine only** — the list in `governance/decision-protocol.md` §2.4.
  Code is not.
- **Before adding a check, script or table, state what wrong thing reaches the *guidebook* if it does not exist, and
  name what reads it.** If the answer is about the apparatus rather than the book, do not add it. An unread field, an
  uncalled script and an unregistered check are the same defect.
- **Minimise code** (owner, 2026-10-12 and 2026-11-06: the minimum that performs the action correctly). Try, in order:
  do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest
  code that closes the defect. A PR touching `scripts/`, `schemas/`, `.github/` or `skills/` names what the added code
  reads, what wrong thing reaches the guidebook without it, and what existing code it replaces or makes deletable;
  refusing writers, typed columns and tests that can go red are not waste. Measure:
  `git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'`. Enforced by review.
- **A specific, ratified authorisation beats a blanket caution.**

Adding a check means editing `governance/check-registry.yaml` — never a workflow. It is the single inventory;
`run_checks.py` is the only thing that invokes a check.

---

## 9. Where to look

Single author, pre-launch. Query the database for the real state.

| Question | Read |
|---|---|
| What to do now | `/orient`; the ACTION lines of the newest entries at the tail of `references/project-standards.md`, and the plan they name |
| Latest owner rulings | the tail of `references/project-standards.md` |
| Research rules | `governance/research-contract.yaml` (the SessionStart hook injects it) |
| Doctrine | `governance/mission-and-epistemics.md` |
| Tiers, markers, weighting | `governance/tier-system.md`, `governance/evidence-architecture.md` |
| Stages and their criteria; which stage a table is in | `governance/pipeline-contract.yaml`; `governance/stage-map.yaml` |
| The schema | `sqlite_master` and `PRAGMA table_info` (§4) |
| ICF codes and the three lenses | §6; `python3 scripts/db.py icf-glossary` |
| Who decides what | `governance/decision-protocol.md` (§2.4 lists what only the owner decides) |
| Checks | `governance/check-registry.yaml`; `python3 scripts/run_checks.py --list` |

**History, not live guidance:** `governance/conceptual-model.md` (built on the deleted item layer),
`governance/functional-taxonomy.md` (built on the retired axis layer), `architecture/project-architecture-guidebook-v2.3.md`
(the claude.ai-surface architecture), `governance/project-instructions-v*.md`, and everything `.ignore` hides.
