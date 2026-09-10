# CLAUDE.md — working guide for the Accessible Built Environments Guidebook

**Layer 0.** This file and the checks are what ensure Layer 1's architecture, shape and schema are
working (owner, 2026-09-09). It holds **process, workflow and rules only**. Every volatile fact —
counts, versions, CI state — is derived here, never stated. Where it disagrees with
`decisions/DR-2026-08-19-research-restart-operative-instrument.md`, that instrument wins and this
file is what to correct.

---

## 1. Run these first

```
bash .claude/hooks/ensure-deps.sh                          # pydantic + jsonschema. DO THIS FIRST
scripts/preflight.sh                                       # gate your diff vs origin/main
python3 scripts/run_checks.py --changed-from origin/main --explain
python3 scripts/run_checks.py --selftest                   # AFTER ANY RENAME — see rule 4
python3 scripts/run_checks.py --list                       # registry + quarantine
```

**A fresh container has no `pydantic`, and without it the whole governance battery fails on
untouched `main`.** `ensure-deps.sh` exits 0 on failure by design, so check before you believe any
red result. **Never `pip install -r requirements.txt`** — it pins `PyYAML==6.0.3` against the
Debian-managed 6.0.1, pip refuses to uninstall it, and nothing lands. Install packages
individually. `governance/check-registry.yaml`'s `batteries:` is the one home of the dependency
list.

**`--changed-from` does not run `--selftest`, and the selftest is where a rename fails.** The
registry encodes stage-qualified `basis: <stage>/<criterion>` refs; CI runs the selftest and your
local gate does not.

---

## 2. The rules that stop you

Each rule carries what enforces it. **"NOT ENFORCED" means you are the gate** — no check will catch
you, and every one of this session's nine defects broke a rule in that state.

**0. A live owner statement supersedes every prior ratified record it touches, on contact.** Record
the supersession; never weigh the ruling against the paperwork it changes. A DR, a RULE, an ADOPTED
directive are what a ruling *changes* — never an argument against it. Numbered 0 because the rest of
this file tilts the other way.
*Proof: on 2026-08-18 the owner ruled `axes` a bad coined term, marked "do not relitigate", and the
next day a batch framed four of five searches on bare `axis_code`, hiding a second mechanism.*
→ **NOT ENFORCED — you are the gate.**

**1. Commit format.** `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, from
`date -u '+%Y-%m-%d %H:%M'`. Use `governance` when no project skill fits.
→ Enforced by `check_commit_msg.py`, **push events only** (`ci.yml:257`) — skipped on every PR.

**2. Attestation on synthesis paths.** Touching `references/bpc-reasoning/`,
`references/connection-reasoning/`, `decisions/` or `sessions/` needs `attestations/<slug>.json`
against `schemas/attestation.schema.json`.
→ Enforced by `attestation_presence`, `attestation_schema` (both blocking). **No gate reads the free
text for meaning**, which is where attestations have actually caught deviations.

**3. Never write `data/guidebook.db` directly.** Migrations only:
`scripts/emit_data_migration.py` → `scripts/migrate_db.py`. Append-only and immutable once
committed — fix forward with a compensating migration.
→ Enforced by `migration_reproducibility` (blocking), **which compares row COUNTS only** — an UPDATE
is invisible to it. `migration_reproducibility_deep` compares every row and is **advisory**.
→ **And the repository breaks this rule on a timer.** The scheduled `source-verification` workflow
commits a `pipeline_runs` row straight into the blob. `migration_reproducibility` cannot see it —
`pipeline_runs` is in that script's `EXEMPT_TABLES`, because it is not reproducible from migrations,
which is the same fact stated as an exemption. A rebuild does not reproduce it, and **every open PR
touching the DB inherits a binary conflict when it fires** (2026-09-07 did exactly that to PR #128).
Resolving such a conflict costs nothing: take the branch's DB and let the next run re-emit.

**4. A rename or removal is not done until the callers are swept.** **A VIEW IS A CALLER. So is a
skill. So is the check registry.** Grep `sqlite_master` as well as the tree, and **treat a 0-row
object as unproven, not clean.**
*Proof: migration 064 exists because 063 swept eight Python readers and six skills and missed
`v_item_provenance`; a byte-exact diff proved it clean because the view rendered 0 rows.*
→ Enforced by `schema_reference_audit` (blocking) for names that must resolve in the schema, and by
`run_checks.py --selftest` C7 for registry basis refs. **Prose callers are not covered.**

**5. Never write the same fact into a second table. Point, do not copy.** Owner ruling 2026-08-24:
*"It is better to have a table cell point to another table cell than to rewrite."* Each stage holds
only its own data; anything earlier is reached by pointer on the shared reference ID.
**A parity check is not a fix** — it makes a dual home survivable, therefore permanent. **A column a
committed data migration INSERTs can never be dropped**: grep `scripts/migrations/data_*` first, then
writer-retire, reader-retire, NULL forward.
→ **NOT ENFORCED — you are the gate.**

**6. Commit the scratchpad AND the agent transcripts at every natural break**, not at session end.
`python3 scripts/preserve_transcripts.py` copies them out of ephemeral container storage; `--check`
says what is unpreserved. A read-only subagent writes nothing at all, so its entire workings live in
`~/.claude/projects`, which a fresh clone does not inherit. If no session directory exists, create it.
`governance: session command log [YYYY-MM-DD HH:MM]` is a complete commit message.
→ **NOT ENFORCED, deliberately.** `--check` is red for the whole life of a session — the
orchestrator's own transcript grows until it ends — and a check that is red by construction teaches
its reader to ignore it.

**7. No hand-written counts in derived documents.** Generate them, or stamp the document with its
generation date and a drift warning. Derive every volatile fact — row counts, schema version, CI
state, the active plan — from the live repo.
*Proof: this file carried three figures under a paragraph warning they were dated. All three were
false within a fortnight, and one contradicted the list beneath it.*
→ **NOT ENFORCED — you are the gate.**

---

## 3. The layers, and the spine

**Owner ruling 2026-09-09** — the project is five layers:

> **Layer 0** is Claude.md and tools/scripts that ensure that Layer 1's architecture/shape/pipelines/schema etc are working
> **Layer 1** is code architecture and data shape and pipeline orchestration and schematic compliance etc — it is what guides all processes in the pipeline
> **Layer 2** is comprised of each stage in the pipeline including its tools/workflows/processes/scripts etc
> **Layer 3** is the actual data being recorded in the tables
> **Layer 4** is supplementary data

Full record: `references/project-standards.md`, 2026-09-09. `layer-N` in a frozen record is the
retired `pipeline-map.yaml`'s old table bucketing, not this.

**THE CANONICAL SPINE. This line is checked; do not hand-edit it.**

    SPINE: base -> research -> evidence -> judgment -> synthesis -> specification -> render

`governance/pipeline-contract.yaml`'s `stages:` is the single home of the stage ids; the line above
is a rendering of it. Owner's own formulation, 2026-08-27: *"you research slugs, evidence research,
judge evidence, synthesize judgments, specify syntheses, and render specifications."* `base` is the
vocabulary layer the machine gates as a stage; the id is `evidence`, and its display form is
**derived** by `stage_label()`, never stored beside it.
→ Enforced by `claude_md_spine` (blocking). Never spell the stages out a second time in this file.

| Stage | Holds |
|---|---|
| **base** | The vocabularies and registries every other stage points into |
| **research** | What was searched, screened and mined, plus the clue store |
| **evidence** | What was admitted, its identity, verification and extraction |
| **judgment** | Whether an extraction is sound and how it weighs |
| **synthesis** | What the judgments say together — weighing, convergence, cross-slug findings |
| **specification** | The determination: *therefore 1200 mm, marked ●* |
| **render** | Book surfaces — `site/`, `parts/`, `tools/*.html` |

**Rule 5 is unusable without this table** — you cannot tell a stage-specific fact from a copy
without knowing which stage a table is in. **Derive any table-to-stage assignment against these
seven stages**; every assignment written before 2026-08-27 predates them.

**A cross-stage view IS the pointer, and is therefore the most protected object in the schema.** A
view joining two stages on the shared reference ID is what "point" MEANS in SQL. **Before deleting
any view, ask which stages it spans** — deleting it forces the next reader back to copying.
Convention: `base` is not a stage, so a view reading one stage plus base crosses nothing.

**Re-entrancy.** A walk **re-enters** stages rather than passing through them once — digesting a
reasoning document produced research leads, a backward edge, and that is normal. That answers *write
order*; the table above answers *what a table may hold*. Both are true.

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
`cp data/guidebook.db $SCRATCH`, then point `GUIDEBOOK_DB_PATH` at it **inline on every call** — the
harness resets env between shells. The canonical DB's sha256 must not move until the migration is
applied.

**Do not hand-write SQL against a table the CLI can reach.** If you find one it cannot, that is a
coverage bug to fix, not a licence to bypass — `dbcore.WRITABLE_TABLES` has been blind to a live
table three times, and each time the temptation was to write around it.

**`db.py` refuses, and that is its whole value.** A writer that merely INSERTs is worse than hand SQL
because it looks safe. **Two refusals are deliberately absent and must stay absent:**
`add-population-match` does not enforce uniqueness on (ref_id, population) — a dissenting adversarial
grade lands as a second row and divergent grades read as a contest — and `add-source` exposes no
`--year`/`--journal` for an entry carrying a `ref_id`, because those are reached through the pointer.

**Vocabularies come from the schema, not a list in code.** `dbcore.check_values()` reads the column's
own CHECK. Live rows are a *sample* of a vocabulary, never the vocabulary. **Never compute a ref_id
by hand** — `dbcore.next_ref_id(conn)` is the rule, and the high-water mark is the UNION of every
table holding a ref_id.

**Schema change:** new `scripts/migrations/NNN_slug.sql`, bump `user_version`, mirror the Pydantic
model. Verify with `migrate_db.py --rebuild /tmp/rebuilt.db`.

**A NOT NULL foreign key into an EMPTIED table makes that table unwritable, and the owner emptied
the item layer on 2026-09-01.** The refusal is `FOREIGN KEY constraint failed` at INSERT — never at
migration time — so the schema looks healthy, a rebuild reproduces it exactly, and every gate stays
green over a table that cannot accept a row. `specifications` is in this state, which is why **no
determination can be written today**; so is `item_taxonomy_links`, which means **D-0184's own object
cannot accept a row either**. This is rule 4's "treat a 0-row object as unproven, not clean" with
teeth. Derive the live set before planning any write, and never quote it:

```
python3 - <<'PY'
import sqlite3; con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
empty = {t for (t,) in con.execute("select name from sqlite_master where type='table'")
         if con.execute(f'select count(*) from "{t}"').fetchone()[0] == 0}
for (t,) in con.execute("select name from sqlite_master where type='table'"):
    dead = {f[3] for f in con.execute(f'PRAGMA foreign_key_list("{t}")') if f[2] in empty}
    for c in con.execute(f'PRAGMA table_info("{t}")'):
        if c[1] in dead and c[3]: print(f"UNWRITABLE  {t}.{c[1]} -> empty table")
PY
```

---

## 5. The three failure modes that are real

**(a) A gate that passes having examined nothing.** Produced four separate times. Every check must
print `EXAMINED: <n>`; `run_checks.py` reports zero-subject passes as NOTHING-IN-SCOPE and escalates
blocking-and-vacuous ones. **When a check passes, confirm it had a subject.**

**(b) Prose that contradicts the database.** See rule 7. Counts in this file, in `index.html`, in
manifests and in audits have all drifted.

**(c) A fabricated citation passing green gates.** On 2026-08-19 all five sources in the first
research batch were stored with **invented co-authors** — including the deletion of autistic
community co-authors from a Co-1 paper whose Co-1 warrant *is* their co-authorship. Six gates passed
it, because each asked whether the author fields were *populated*, never whether they were *true*.
**Verification must leave an artefact:** `scripts/research/retrieval_log.py` persists every payload,
and `--verify-authors` diffs stored data against the bytes actually received.
**Never write a bibliographic field from memory when a payload is in hand.**

---

## 6. Evidence model

`governance/tier-system.md` is operative. **T1** primary controlled research · **Co-1** lived
experience / participatory design, **co-primary with T1** under CRPD Art 4.3 · **T2** synthesis ·
**Co-2** OT professional-body CPGs · **T3** grey primary · **T4–T6** the regulatory stratum, walled
off from full-strength anchoring.

Markers: **●** confirmed · **◐** policy/standards only · **○** grey/thin. Unmarked is an error.
Cell states: `stated` / `provisional` / `pending` / `not_applicable`.

**Co-1's warrant is co-production.** The disabled people who produced the work are part of the
evidence, not metadata. Erasing them while claiming the tier is the worst failure available here.

Work from the **ICF/access-need frame with codes AND names**, never bare axis codes, never population
umbrellas. **The crossing is JUDGMENT's output** (owner, 2026-08-27, overruling `DR-2026-08-24`
§2.4): harvest concepts at evidence (`db.py observe-term`, verbatim and unjudged), adjudicate at
judgment. Zero links **after judgment** is a defect. Only Opus-class models write
`best_practice_synthesis`.

**The lens half is RULED; only the subject half is open — do not confuse them.** Owner ruling
2026-08-28 (`references/project-standards.md`): any table attaching a determination to a group of
disabled people takes **four lens columns, one CHECK, real FKs, and `population_code` is retired in
favour of the four**. D-0182 then relaxed that CHECK from "exactly one" to **at least one**
(`COALESCE(...) IS NOT NULL`), which is what migration 065 built and what the live table says in its
own comment. So `specifications.population_code` is not a question — it is a sweep owed.

**THE SUBJECT IS ALSO RULED, AND THIS FILE SAID OTHERWISE FOR A DAY.** Owner ruling **2026-08-26**
(`references/project-standards.md`, `grep -n 'judgment object is the'`): *"The judgment object is the
**canonical parameter**, and `items` is the render rollup the entity model already calls it."* The
determination is keyed on **the design parameter under determination**; `specifications.item_code`,
presently NOT NULL, *"is dropped alongside `population_code` in the same P1.0 migration"*; `items` is
demoted from identity to a Part-4 render aggregate **derived from** specifications rather than keyed
by them. That ruling carries a five-clause ACTION — read it before touching any of this.

*This paragraph read "an owner decision — do not invent one" until 2026-09-09, while the ruling had
stood since 2026-08-26. It was written in the same change that added rule 4b's mirror to the ledger
— **declaring open a question already answered** — and by an author who had just caught that error
on the lens half and did not re-run the search for the subject half. A ruling can be in the
repository, in the file §9 sends you to, and still fail to bind if the search stops at the first
answer it finds.*

**So neither half is open. Both are sweeps owed**, and `item_taxonomy_links` and `specifications`
stay unwritable until they are done. Do not read `slug × population` as any part of the answer:
`populations` IS the identity lens (`base_taxonomy_identity`), so that key reintroduces the
traversal D-0184 measured and rejected.

---

## 7. Traps

- **`.ignore` hides frozen records from ripgrep and the Grep tool** — `_archived/`, `audits/`,
  `sessions/`, `references/search-log/`, `versions/`, `workplan/_superseded/`, and the JSONL under
  `transcripts/`. **Owner rulings live overwhelmingly in `sessions/`.** "No matches" ≠ absent:
  `grep -r` and `git grep` ignore `.ignore` and find them instantly. **Never report a ruling absent
  from a search that could not have seen it.**
- **`scratchpad/CURRENT` is the anchor for the running session, and it moves at OPEN.**
  `sessions/LATEST` and `LATEST-RESEARCH` move at CLOSE, so **both name the PREVIOUS session for the
  whole life of the current one.** Anything needing "the session running now" reads `CURRENT`. Set it
  when you create the batch folder. **It also goes stale when your PR merges mid-session** — the
  folder it names is then a merged PR's, and your command log appends to someone else's record until
  you move it. Name the folder for the branch and `git mv` once the PR number exists; never guess a
  number, because a guess that lands teaches nobody.
- **`git rebase` and `git checkout -B` are blocked in this harness** as history-rewriting. When a
  merged PR leaves unmerged commits on your branch, `git merge origin/main` reaches the same state
  without rewriting anything — the branch carries a merge commit rather than a replay.
- **THE ITEM LAYER IS GONE FROM THE DATABASE AND STILL LIVE ON THE READING SURFACE.** `items` holds
  0 rows and a rebuild does not restore it — but the prior version's corpus still publishes the
  codes and their names across `references/` and `working/`, which `.ignore` does **not** hide.
  (`versions/` carries them too and **is** hidden — `.ignore` line 106. This bullet claimed
  otherwise until 2026-09-09; the bullet above it was right. **And it named `index.html` as a live
  surface until 2026-09-10, when that file and `references/part04-item-index.md` had both already
  moved under `_archived/`, which `.ignore` line 63 DOES hide** — so the bullet asserted the
  opposite of the state on that clause, and both of its derivation commands below pointed at paths
  that no longer resolve. A trap whose command errors out teaches the reader to distrust the trap.)
  So a session that greps for a topic still meets **`E-08 Corridor Clear Width
  (≥1200 mm Minimum on All Primary Routes)`** — a container whose name states its answer, which is
  the whole reason the owner deleted the layer: *if E-08 already exists then the work is predisposed
  to filing into a container that already exists, and that biases every finding.* **Treat every
  `[A-Z]-NN` code you meet as prior-version content, never as a container to file into.** `db.py
  add-item` refuses for this reason. **The prefixes run wider than any range you would guess** —
  derive them, and note the archived index is now their only home:
  `grep -rhoE '\b[A-Z]-[0-9]{2}\b' _archived/references/part04-item-index.md | cut -c1 | sort -u`.
  Then derive the LIVE surface before framing anything — the two are different questions and only
  the second one bounds what a grep will hand you:
  `grep -rEl '\b[A-Z]-[0-9]{2}\b' references/ working/`
- **Session ids: bare stem in the DB, `.md` in pointers and `emit_data_migration --session`.** Wrong
  form scopes a gate to nothing and it passes green.
- **If you add a `SessionStart` hook, APPEND it — never insert at index 0.**
  `research_contract_hook.py` reads `SessionStart[0]["hooks"][0]["command"]` by hardcoded index; an
  insert turns the blocking `research_contract_sync` red with a diff that reads as contract drift.
- **Don't hand-edit generated output** (`parts/`, `site/`, `audits/`, `tools/*.html`) — regenerate
  with `scripts/regenerate_derived.sh`.
- **`schemas/*.py` ↔ SQLite drift is a bug**, not a convention.
- **PI versioning is intentional** — highest-numbered `governance/project-instructions-v*.md` is live
  and legitimately lags doctrine. Prefer `references/project-standards.md` and recent DRs.
- **Don't run `scripts/bootstrap.sh`** — PAT-gated, for the claude.ai surface.

---

## 8. Deleting is as cheap as adding

**Adding apparatus carries the burden of proof; removing it does not.**

- **Code, checks, scripts, dead tables and views: delete them.** No owner gate. You need *evidence* —
  unreferenced, vacuous after a real batch, or superseded — not permission. Record it in the commit.
- **Git history is the archive for CODE.** Do not copy scripts to `_archived/` to "preserve" them.
  `_archived/` is the right home for retired reader-facing *content*, not executable surface.
- **Owner sign-off is required for content and doctrine only** — mission, audience, CRPD posture,
  population taxonomy, evidence-tier definitions, jurisdiction, licensing, trajectory. Code is not.
- **Before adding a check, script or table, state what wrong thing reaches the *guidebook* if it does
  not exist.** If the answer is about the apparatus rather than the book, do not add it.
- **Nothing is added without naming what reads it.** An unread field, an uncalled script and an
  unregistered check are the same defect.
- **A specific, ratified authorisation beats a blanket caution.** Blanket removal-friction winning
  ties against specific removal-permission is how this file became a ratchet.

Adding a check means editing `governance/check-registry.yaml` — never a workflow. It is the single
inventory; `run_checks.py` is the only thing that invokes a check.

---

## 9. What this project is

A reference on architecture, accessibility and built-environment standards centred on **disabled
people**. Fixed doctrine: a **thinking tool and advocacy project, not an authority** — *"the purpose
of this guidebook is to get people to ask the right questions."* Not a prescription manual, not a
legal authority, not a substitute for professional judgment. "Inclusive / accessible / universal"
here always means *inclusion of persons with disabilities*.

Pre-launch, single author (`@jordanelias`). The governance and tooling are elaborate; **the content
is barely started.** Query the DB for the real state.

| Question | Read |
|---|---|
| What to do now | `decisions/DR-2026-08-19-research-restart-operative-instrument.md` |
| Latest rulings | the tail of `references/project-standards.md` |
| Doctrine | `governance/mission-and-epistemics.md` |
| Tiers, markers, weighting | `governance/tier-system.md`, `governance/evidence-architecture.md` |
| Entity model, ICF frame | `governance/conceptual-model.md`, `governance/functional-taxonomy.md` |
| Decision process | `governance/decision-protocol.md` + recent `decisions/DR-*` |
| Architecture | `architecture/project-architecture-guidebook-v2.3.md` |
