# 2026-08-11 — Remediation plan and pipeline anatomy

**Status:** PROPOSED — no fix in Part 1 has been executed. This document proposes; it does not act.
**Method:** agonist–antagonist, 10 agents, 2 adversarial lenses per unit of work (Part 3).
**Predecessor:** `workplan/2026-08-09-locator-hierarchy-and-enforcement-probes.md`
**Governing context:** `decisions/DR-2026-08-06-clean-room-evidence-reset.md`

> **Read Part 0 first.** Four of this document's own first-draft proposals were killed by its
> antagonist pass, and one was refuted outright. The correction log is §0.2, not an appendix.
> A document that quietly absorbs its own corrections teaches the next session nothing.

---

## Part 0 — What this is, and what it got wrong

### 0.1 Scope and governing question

**The owner's stated goal is to "ensure that our structure actually works before we do
content."** That sets the bar for this document: description is not the deliverable, and a
defect list is not an answer. The question is whether the machine can carry a row from topic
creation to a rendered, walkable claim — and the only honest way to answer it is to try.

So Part 2 is validated by an **end-to-end structural walk**: one synthetic topic pushed through
all twelve stages in a scratch copy of the database, recording at each stage whether the insert
was accepted, which validators fired, and whether the row remained reachable from the previous
stage. Three deliberately illegal rows are pushed alongside it, because **a gate that passes a
bad row is worse news than a gate that blocks a good one.** §2.13 reports the result.

This is the cheapest moment such a test will ever have: the reset emptied the corpus, so a
synthetic walk collides with nothing and every table starts from a known state.

Three parts:

1. **Remediation register** — every issue standing on 2026-08-11, with a method, a gate, an
   evidence command, and a falsification condition.
2. **Pipeline anatomy** — twelve stages from topic creation to render, each answering (a)–(h),
   where (h) is the acceptance conditions a single row/file must satisfy to be admitted.
3. **The agonist–antagonist protocol** — proposed as standing method.

Every number here was derived on 2026-08-11 by running the command quoted beside it. Where a
claim has no command, treat it as unaudited (§9 guardrail 1).

### 0.2 Correction log — what the antagonist pass killed

| # | The first draft proposed | Verdict | What replaced it |
|---|---|---|---|
| K1 | A new `subject:` / `on_empty_subject:` block in the check registry, to distinguish "examined nothing" from "found nothing" | **FATAL** | `min_items` + the `EXAMINED: <n>` convention **already exist and work**. The proposal reinvented them *and* `scripts/audit/graph/known_debt.yaml`, and its `SKIP`-on-empty policy would have restored the disarm-by-declaration mode `run_checks.py` documents as this repo's fifth occurrence. Replaced by A4 — declare `min_items` on the 23 blocking checks that lack it. |
| K2 | Move the failing reasoning doc to `working/pilot/` so `validate_reasoning --strict` goes green | **FATAL** | `references/bpc-reasoning/` holds exactly one real doc; `validate_reasoning.py` returns 0 on an empty file list, so the move converts a red check into a **vacuous green**. The path also leaves `SYNTHESIS_PATH_RE`, dropping the doctrine token and blocking `attestation_presence`. Replaced by C4 — fix the document in place. |
| K3 | Execute the 57-file `workplan/` rename | **FATAL** | 278 distinct files cite those filenames, including 9 committed migrations (immutable) and 8 attestations (forward-only). `tooling-register.md` §6.5 already withdrew a smaller version of this as unwise. Replaced by D9 — generate a date-sorted index instead. |
| K4 | Enable branch protection *and* promote `site_pages_fresh` and `migration_reproducibility_deep` to blocking | **FATAL** | `tooling-register.md` §6 item 6 withdrew exactly this, verbatim: promoting checks in the same window that protection goes on "would make the repository unmergeable outright." Replaced by the sequencing in §1.6. |
| K5 | "Retiring the three connection registers — prerequisites are done, recommend EXECUTE" | **REFUTED** | No document records the prerequisite (reconciling the md registers against DB `connections`) as executed, and the DB side is now **0 rows** post-reset, where it held 273 in July. The claim came from a handoff summary, not from a verified state. |
| K6 | Require the `DB integrity (content checks)` job under branch protection, since it is 70/70 | **OVERSTATED** | It is 70/70, but roughly 30 of those 70 checks reference only empty tables. Requiring it today locks in a **vacuous green**. Requires A4 first. |
| K7 | `room_page.py` needs "three queries" repointed — "one afternoon" | **OVERSTATED** | Six phantom tables across eight queries, and `room_items`' columns differ from what the script expects. Three of the six have no substitute at all. |
| K8 | The `retired_vocabulary` backlog is concentrated in the PI snapshot | **OVERSTATED** | Read off the audit's truncated default output. The PI is 7 of 69, and 2 of those 7 are `UNVERIFIED-1` tokens, not workflow names. A third class — a hit in Python code — has no ruling at all. |
| K9 | "No mechanical enforcement of the Opus floor is possible from inside the repo" | **OVERSTATED** | The *fact* of authorship is unverifiable; the *declaration* is schema-enforceable through the attestation apparatus that already exists. |
| K10 | A4's replacement for K1: "declare `min_items` on the 23 blocking checks that lack it" | **OVERSTATED** | The repo adjudicated this on 2026-08-06 and retired a floor it had just added, on the reasoning that the guard catches *accidentally* empty subjects and "an empty subject that is the declared state of the project is not that." A blanket floor makes blocking gates red for telling the truth. Replaced by the warrant-and-lift mechanism in A4. |
| K11 | "A source comment asserts a `min_items` protection that does not exist" | **OVERSTATED** | The floor existed when the comment was written and was retired hours later by the reset. The comment is **stale**, not false — which is a smaller defect, but the *hole it leaves* is the larger finding (§1.1). |

Eleven corrections against roughly forty claims — and two of them (K10, K11) were corrections
to corrections. That ratio is consistent with this repo's history: five of twenty quarantine
reasons wrong on first audit, seventeen corrections in the 2026-08-09 draft. It is the argument
for Part 3, and the K1→K10 sequence is the argument for **lens diversity** specifically: the
method lens and the vacuity lens killed the same item for opposite reasons, and the fix that
survives is the one neither proposed alone.

---

## Part 1 — Remediation register

### 1.0 The answer to the owner's question

**Does the structure work, before content?** Partly — and the part that does not work cannot be
fixed by writing content.

A backward trace of the seven hops from a rendered page to the evidence beneath it, read at
code level against the live schema, returns:

| # | Hop | Verdict |
|---|---|---|
| 1 | rendered page → determination | PASSABLE-BUT-WEAK — the page prints `item_code` + `population_code`, never `cell_id`; recovery relies on the `UNIQUE(item_code, population_code)` constraint. `parts/` renders no determination at all. |
| 2 | determination → governing sources | PASSABLE-BUT-WEAK — the renderer reads the FK junction; three *blocking* validators read the un-FK'd JSON; blocking H01/H02 hold the two equal, **but the only writer emits JSON only** |
| 3 | source → the value it supports | PASSABLE-BUT-WEAK — the `item_code` FK is real, but `reasoning_doc_citations` has no `item_code`, so promotion falls back to free-text `parameter` |
| 4 | source → population served | **BROKEN** — `target_population` has no FK; recovered by a regex over prose (`assess_cell.py:180`); three scripts treat the column as three different types |
| 5 | source → the search that found it | PASSABLE — the junction is authoritative and `v_source_admission` returns the verbatim query in one hop. The strongest hop on the walk |
| 6 | determination → doctrine | **BROKEN** — no doctrine column exists anywhere in the DB; `attestation.schema.json` pattern-restricts `artifact` to `.md` paths, so no attestation can name a row |
| 7 | code value → anything | **BROKEN** — one FK (`item_code`); no `ref_id`; `spec_id` keys a table that has never existed |

**DR-2026-08-06 §1 states the project's constitutive claim in four legs:** a published best
practice must walk back to *the values it rests on*, *the sources those came from*, **the
population it serves**, and **the doctrine that governed the judgement**.

The narrow walk — page → determination → governing source → verbatim search query — **is
possible in principle**: four hops, all declared FKs, and the SQL parses against the live schema
today (returning zero rows, because every table is empty). That is the good news, and it is
real.

**But two of the four named legs cannot be recorded at all.** "The population it serves" has no
key — it is free text matched by regex. "The doctrine that governed the judgement" has no
column anywhere in the database. **No quantity of new rows fixes either. Both require a
migration.**

This is the finding that most directly answers the goal. The reset was executed because 0 of
306 topics could show their work; a project that resumes content now would still be unable to
show two of the four things it promises — not through neglect, but because there is nowhere to
put them. **Both migrations are free today and get more expensive with every row written.**

They are N1-adjacent but distinct, and they belong at the top of the pre-content list:
1. Give `evidence_population_match.target_population` a real FK to `populations`.
2. Give `evidence_cell_state` a doctrine binding (a `doctrine_sha` column, mirroring what
   `attestations/*.json` already does for documents), or widen `attestation.schema.json`'s
   `artifact` pattern so an attestation can name a row rather than only a file.

### 1.0b The structural walk — result

One synthetic topic (`zz-walk-test`, `REF-99001`) was pushed through all twelve stages in a
scratch copy of the database, alongside three deliberately illegal rows.

**BREAK POINT: none. The row traversed all twelve stages.** The chain joins by key end to end,
the foreign keys are real in the production path, and `spec_page.py` round-trips a
determination back to REF-99001 — while honestly flagging a `stated` cell with no governing
sources, because it deliberately reads the `cell_source_links` junction rather than the
`governing_refs` JSON. **It is the one component that anticipated this exact failure**, and it
is the model the rest should copy.

**The verdict is not "it works". It is: the structure can carry content today, and that is the
problem.** Enforcement is strong exactly where a foreign key happens to exist, and absent
everywhere the evidence actually lives. Concretely, in the walk:

- `tier=99` and `evidence_type='not-a-real-evidence-type'` **propagated untouched into
  `part13.md` as a fabricated tier band "T99" in the published bibliography.**
- The determined value itself (`value_min=1200.0`, `value_unit='mm'`) **does not render at all
  — no generator reads those columns.** The number the whole pipeline exists to produce is
  the one thing that does not reach the page.
- Of three illegal rows, only one was caught: a `stated` cell whose `governing_refs` named a
  nonexistent REF-ID, stopped cleanly by two independent blocking gates. That is the
  anti-hallucination gate working, and it is genuinely good news.

**Seven validators stayed silent, four of them blocking:**

| Validator | Level | What it passed |
|---|---|---|
| `validate_axes` | blocking | never reads `serves_axes`; accepted `banana not even json` with 0 errors |
| `validate_schema` | blocking | examines 20 YAML files and never opens a research table — so the Pydantic tier and enum validators never execute against a DB row |
| `test_db_integrity` | blocking | catches `verification_status`/`metadata_quality`/`source_type`; has **zero checks on `tier` or `evidence_type`** |
| `check_rendered_docs` | blocking | rc=0 on EXAMINED 0 (C8) |
| migration-053 locator hierarchy | — | **no enforcer anywhere in the repo** |
| `validate_reasoning --strict` | advisory | passed a document whose entire evidence inventory cites `REF-00000-NONEXISTENT` |
| `metadata_integrity_audit` | advisory | printed "1/1 eligible rows lack a cross-check record (100.0%)" and returned PASS |

**Two ordering defects surfaced that no static reading had found:**

1. **The documented stage order is unsatisfiable.** `search_admissions.ref_id REFERENCES
   evidence_sources(ref_id)`, so stage 4 (admission) cannot complete before stage 5 (the source
   exists). The real order is 4a → 5 → 4b, and getting it wrong fails with a bare
   `IntegrityError: FOREIGN KEY constraint failed` that names nothing useful.
2. **Validation is inverted at stage 7.** The *well-formed* extraction — full locator
   hierarchy, claim text, `full-read` provenance — was **rejected** for one wrong population
   code, while the *malformed* one (`claimed_value='9999'`, `extraction_status='verified'`, all
   sixteen `loc_*` columns NULL) was **accepted**.

**The single highest-value fix follows directly:** point the existing Pydantic models at DB rows
instead of only at 20 YAML files. The models are already correct — they encode the tier and
enum vocabularies the walk violated. Wiring them to the database closes two of the four blocking
gaps by itself, and needs no new validation logic.

**Scope note, stated because it matters:** the walk did not exercise
`scripts/emit_data_migration.py` (it writes into tracked `scripts/migrations/`), so the
sanctioned write path itself remains untested end to end. A real topic must also pass through
it.

### 1.0c External reviewability: retire the committed binary, keep the SQL

**The requirement.** The project must be verifiable by a sceptical stranger through GitHub
alone — concretely, without trusting an assertion.

**The obstacle, stated fairly.** `.gitattributes` declares `data/guidebook.db binary`, so on
every data PR GitHub renders "Binary file not shown". **The canonical source of truth is
unreviewable in the web interface.** A reviewer cannot see what a data commit changed.

**But the reviewable form already exists, and it is exact.** Measured on 2026-08-11:

```
$ python3 scripts/migrate_db.py --rebuild /tmp/ext-rebuild.db
  Applying 42 schema migration(s)
  Applying 289 data migration(s)
Rebuilt successfully.                                    real 0m15.062s

committed user_version 53 | rebuilt 53
tables only in committed: none
tables only in rebuilt  : none
ROW-COUNT DIVERGENCE: 0 table(s) of 66
```

**345 SQL migrations reproduce the committed database exactly, in fifteen seconds.** Every one
of them is plain text, diffable, and reviewable on GitHub. The binary is not the source of
truth — it is a **cache of the source of truth**, and today it is a faithful one.

**Recommendation: stop committing `data/guidebook.db`. Make it a build artifact.**

What that buys, against the stated requirement:

| Today | After |
|---|---|
| A data PR shows "Binary file not shown" | A data PR shows the exact SQL that changed |
| "Never write the DB directly" is a text rule the write-map shows 16 scripts breaking | The rule becomes **self-enforcing** — you cannot hand-edit a file that is not there |
| The blob and the migrations are a dual representation with a partial reconciler | One representation. The largest instance of C11's disease, removed at the root |
| Two branches touching the DB produce an unresolvable conflict (no merge driver) | Migrations merge like any text file |
| `migration_reproducibility` compares `user_version` + `COUNT(*)` on six tables | The question it asks stops mattering — there is nothing to diverge |

**The one real blocker, and why the window is open right now.** Three tables are written by
scheduled jobs outside the migration system — `evidence_source_authors`, `pipeline_runs`
(both exempt) and `url_verification_runs` (**not** exempt). A rebuild would drop any rows they
hold that no migration replays. **Today it drops none**: the measurement above shows zero
divergence across all 66 tables, because migration 012's baseline dump froze the current job
rows. **The next fortnightly `verify-urls.yml` run breaks that**, and every run after widens it.

So the sequence is forced, and it is short:
1. **Rule on D2** (the exemption list) — this is the decision the 2026-08-09 workplan enumerated
   and it now has a second, larger reason to be taken.
2. Either pause the two cron workflows, or have them emit migrations, so job state is replayable.
3. Remove `data/guidebook.db` from the index; add it to `.gitignore`; add
   `python3 scripts/migrate_db.py --rebuild data/guidebook.db` to the bootstrap in CLAUDE.md §7
   and to every CI job that needs a database.
4. Retire `migration_reproducibility` — its subject no longer exists — and reallocate the
   guarantee to a build step.

**Cost and risks, stated plainly.** Every session and CI job gains a 15-second build step.
`scripts/db/**` targets a different legacy path and is out of scope. Any tool that assumes the
file is present must tolerate building it. And the repo loses the ability to inspect the DB
without running anything — which is a real convenience, and the reason to decide deliberately
rather than by default.

**Gate:** owner. This is an architecture change (D-OP, arguably D-SCHEMA-adjacent) and it
touches `.gitattributes`, CI, and the onboarding contract. **But it is the single highest-value
external-verifiability change available**, it converts a trust into a check, and the
measurement says it is safe *today* in a way it will not be after the next cron run.

### 1.0d Every binary database in the repo, and what each costs

Three tracked binary artifacts, plus two files that should never have been committed at all:

```
$ git ls-files | grep -Ei '\.(db|db-shm|db-wal)$'
_archived/data/corpus-pre-reset-2026-08-06.db        7.3M
_archived/data/corpus-pre-reset-2026-08-06.db-shm     20K
_archived/data/corpus-pre-reset-2026-08-06.db-wal       0
data/guidebook.db                                    3.0M
```

**First, a correction to this document's own framing.** An earlier draft implied binary
databases dominate repository weight. Measured, they do not:

```
DB blobs in history:  82 objects,  3.3 MiB on disk
ALL blobs in history:            12.8 MiB on disk
```

**26%, not a majority.** `data/guidebook.db` has been rewritten across 74 commits, but git's
delta compression handles SQLite well — its pages are largely stable between commits. **The
argument for removing the binary is reviewability (§1.0c), not size.** Anyone making the size
case should use this number, not an assumption.

That said, three findings stand, in increasing order of decisiveness:

**1. `.db-shm` and `.db-wal` are tracked, and never should have been.** These are SQLite
*runtime* artifacts — a shared-memory file and a write-ahead log. They are meaningless outside
a live connection, they can encode a mid-transaction state, and committing them is
unambiguously an accident. **Method:** `git rm --cached`, add to `.gitignore`. No decision.

**2. `data/audit_graph.db` is present and untracked** — correctly so, as a build artifact. This
matters as precedent: **the repo already treats a generated database as non-committed**, so
§1.0c's proposal is an extension of existing practice, not a new principle.

**3. The archived corpus is a byte-identical duplicate of a git object the repo already holds.**
DR-2026-08-06 §2 states the pre-reset corpus is "preserved twice" — on branch
`archive/pre-reset-corpus-2026-08-06`, and as `_archived/data/corpus-pre-reset-2026-08-06.db`.
Those are not two copies. They are two pointers to **the same blob**:

```
$ git rev-parse FETCH_HEAD:data/guidebook.db          # the archive branch
62c27b475816703ce64bfd2ac2bfe529b70435e3
$ git hash-object _archived/data/corpus-pre-reset-2026-08-06.db
62c27b475816703ce64bfd2ac2bfe529b70435e3
```

Git stores that object once regardless. So deleting the working-tree file **costs zero
information and saves zero history** — but removes **7.3 MB from every checkout**, making it
the largest single file in the working tree by a wide margin.

The DR names one thing that would be lost: the file is "queryable without a checkout". That is
a genuine convenience, and it is the whole of the case for keeping it. Against it: the DR's own
reasoning for the file — that `_archived/` is `.ignore`-hidden so "repo-wide search returns
zero files from it" — argues for a path nothing resolves, which a branch satisfies at least as
well.

**Method:** delete the file; keep the branch; update DR-2026-08-06 §2 to say the corpus is
preserved **once, on a branch**, and record the blob hash so the equivalence is checkable by a
stranger. **Gate:** owner — this is a retirement (§9 guardrail 4), and guardrail 2 says
redirect rather than delete, so leave a stub naming the branch and the hash.

**Ordering:** finding 1 needs no decision and should ship immediately. Finding 3 is owner-gated
but the evidence is airtight. §1.0c's proposal for the live database is the larger change and
depends on the D2 exemption ruling.

### 1.1 The governing finding

**The clean-room reset changed the subject of every check in the repository, in one commit,
and the checks did not notice.**

`decisions/DR-2026-08-06-clean-room-evidence-reset.md` emptied 38 tables. The apparatus
reports `RESULT: PASS — 55 check(s) green, 9 advisory failure(s)`. Both halves of that verdict
are now unreliable in the same way, and in opposite directions:

- Some checks **fail vacuously** — they assert a non-zero floor over a table that is now
  empty. Nothing is wrong; the subject is gone.
- More seriously, some checks **pass vacuously** — they examine nothing and report success.

This repo has documented the second failure mode five times and built `min_items` +
`EXAMINED: <n>` to stop it. The measurement below is what that mechanism currently covers.

```
$ python3 -c "import yaml; d=yaml.safe_load(open('governance/check-registry.yaml'));
  b=[c for c in d['checks'] if c.get('level')=='blocking'];
  print(len(b), len([c for c in b if c.get('min_items') is not None]))"
28 5
```

**Five of twenty-eight blocking checks declare a vacuity floor.** The five are
`check_utf8_md`, `check_json`, `check_yaml`, `validate_schema`, `research_contract_sync`.
The twenty-three without one include `test_db_integrity`, `validate_evidence_state`,
`citation_mining_session`, `attestation_presence`, `attestation_schema`, and
`check_rendered_docs` — every one of which reads a table the reset emptied, or a corpus that
can be empty.

**The sharpest instance.** `check_rendered_docs` is blocking, and on its registered invocation:

```
$ python3 scripts/audit/check_rendered_docs.py --all
EXAMINED: 0 rendered document(s) — specs/ is reference-only since the 2026-08-06 reset;
pass --doc to check a live one
EXIT=0
```

The `return 0` is deliberate and documented: post-reset, `specs/*.html` are reference documents
citing a corpus the reset deleted, so checking them asks a question the reset already answered.
That reasoning is sound. But eight lines below it, the same file states:

> `min_items: 1` in the registry enforces the pairing from the other side.

**That entry declares no `min_items`.** The registry note explains why: the floor *was*
declared on 2026-08-06 and **retired hours later** by the reset, on the explicit reasoning that
the guard exists to catch an *accidentally* empty subject, and "an empty subject that is the
declared state of the project is not that — leaving the guard would have made a blocking gate
red for telling the truth."

**That reasoning is correct, and it is also where the hole is.** The retirement left a blocking
check that certifies nothing, guarded by a prose sentence — *"Re-declare `min_items` the day
specs/ is regenerated against the live DB"* — that nothing evaluates. The same pattern appears
in at least three registry notes. **A protection whose restoration depends on someone
remembering a note is not a protection**, and the script comment is now stale rather than
false: true when written, never updated when the floor was pulled.

This is what A4 addresses, and it is not "declare `min_items` everywhere."

### 1.2 Class A — the apparatus's own footing

**A1 · The documented setup command fails.** `pip install -r requirements.txt` →
`ERROR: Cannot uninstall PyYAML 6.0.1, RECORD file not found. Hint: The package was installed
by debian.` The pin is `PyYAML==6.0.3`; the container ships 6.0.1 via apt. CLAUDE.md §7 gives
this command as step one.
**Method:** relax to `PyYAML>=6.0,<7` and document `--ignore-installed`.
**Gate:** none. **Falsification:** any script using a yaml API newer than 6.0.1.

**A2 · `requirements.txt` states something false about itself.** Its header says "All scripts
under `scripts/` and the `schemas/` package depend only on these two."
`scripts/audit/adherence_log_audit.py` does `from jsonschema import ...`, and `ci.yml` installs
`jsonschema` explicitly in two jobs — CI already knows the comment is wrong.
**The consequence is worse than a missing dependency:** without `jsonschema`, the attestation
audit exits **0**. A missing dep produces a *pass*, not a failure.
**Method:** add `jsonschema` to `requirements.txt`; delete the false sentence; collapse ci.yml's
four install recipes to one.
**Gate:** none.

**A3 · Missing dependencies present as five blocking failures.** With pydantic absent:
`BLOCKING failures (5): validate_schema, validate_evidence_state, audit_adversarial_use,
decision_capture, doctrine_recheck` — all `ModuleNotFoundError`. After install:
`RESULT: PASS — 55 green, 9 advisory`. A session that does not read the tracebacks concludes
the repo is broken.
**Method — the data already exists.** `governance/check-registry.yaml` declares per-battery
`deps:` (`schema: [pydantic]`, `attestation: [jsonschema]`, `research: [pydantic, jsonschema]`).
`grep -n "deps" scripts/run_checks.py` returns **nothing** — the runner has never read the
field. Wire it: before running a battery, verify its declared deps import, and abort with a
distinct exit code and the exact install command. Two entries are also wrong and must be fixed
in the same commit:
- `tests: {deps: []}` is false — `test_assess_cell_pilot.py`, `test_directness_2_2.py` and
  `test_evidence_cell_state_2_3.py` all import pydantic or `schemas`.
- **`governance` is malformed.** Line 174 reads
  `governance:  {deps: [pydantic], description: Decision protocol, doctrine recheck, adversarial-use.}`
  — unquoted commas inside a YAML flow mapping, which parses as three entries: a truncated
  description plus two junk keys, `doctrine recheck: null` and `adversarial-use.: null`.
  `check_yaml` passes it because it is *valid* YAML. Quote the description.
**Gate:** `scripts/` and `governance/` are CODEOWNERS-protected — owner review, not owner decision.

**A4 · Give retired vacuity floors a warrant and a self-lifting condition.** This replaces both
K1 and the first draft's blanket "declare `min_items` on all 23", and it is the highest-value
item in Part 1 because **every promotion in §1.6 depends on it.**

*Two corrections got us here, from opposite lenses, and both were right.* The method lens
killed inventing a new registry block. The vacuity lens then killed blanket-declaring floors:
the repo had already adjudicated that on 2026-08-06 and concluded, correctly, that a floor on
a *declared*-empty subject makes a blocking gate red for telling the truth.

**The distinction they converge on is `warrant`.** An accidentally-empty subject and a
deliberately-empty one differ by whether a ratified decision authorises the emptiness — and
that is a field, not a judgement call.

**The mechanism already exists and is proven.** `scripts/audit/graph/known_debt.yaml` carries
exactly this shape:

```yaml
  - id: c1-source-value-extractions-empty
    check_id: table.empty_mission_critical
    table: source_value_extractions
    warrant: "DR-2026-05-28-b (B6) + C1 value backfill pending (…)"
    lift_when_sql: "SELECT COUNT(*) FROM source_value_extractions"
    lift_when_ge: 1
```

`graph_audit.py` re-evaluates `lift_when_sql` every run and, once the count is reached, reports
**the suppression itself as STALE** rather than silently hiding a regression. An entry with no
warrant is refused outright (`known_debt.unsound`).

**Method:** every place a registry note currently says "re-declare `min_items` when X" becomes a
warranted suppression with `lift_when_sql` encoding X. Three notes say this today
(`check_rendered_docs`, `source_slug_links_duplicates`, and the specs/ regeneration condition);
none is evaluated by anything. Extend the same evaluation to the check registry, or move these
entries into `known_debt.yaml` and have `run_checks.py` consult it — **the design decision is
which, and it is small.** Then, and only then, declare real floors on the blocking checks whose
subjects are *not* warranted-empty.
**Falsification:** if a check's subject is not expressible as a count query, this shape is
wrong for it — test against all 28 blocking checks before adopting.
**Gate:** none for the mechanism; each warrant cites an existing DR, so no new decision is
created.

### 1.3 Class B — vacuous failures (artefacts of emptiness, not defects)

Four of the nine advisory failures are this and nothing else. **Fixing them one at a time is
the wrong instinct**; but so is one blanket fix (K1). Each needs a leg-level, not check-level,
resolution — a check-level skip would switch off the fifteen assertions in
`test_verification_pipeline` that still pass, and `graph_audit`'s `code.phantom_table`
detector, which is the thing that would catch C2's bug.

- **B1 `test_verification_pipeline` 15/18** — G01/G02/G03 assert floors on `evidence_sources`
  and `evidence_source_authors`, both 0 rows. **Method:** gate the three legs on a non-empty
  subject, reporting `NOT-TESTABLE (subject empty)`; leave the other fifteen asserting.
- **B2 `test_graph_audit` crash** — `graph_audit.py:277`,
  `SELECT con_id FROM connections LIMIT 1` → `TypeError: 'NoneType' object is not subscriptable`.
  `connections` is 0 rows, so the mutation harness dereferences None. **This one is a real bug
  regardless of emptiness**: a crash hides every assertion behind it. **Method:** guard the
  fetch; skip the mutation leg with a stated reason. Highest priority in Class B.
- **B3 `test_directness_2_2`** — passes standalone (`ALL PASS`, live smoke SKIPs on absent
  `/tmp/work14.db`) and fails under the registry against the canonical DB. Same test, two
  verdicts, decided by which DB it finds. **Method:** make the live-smoke leg's subject explicit.
- **B4 `research_dod --all` R1** — 14 rules PASS, R1 NON-COMPLIANT: "0 searches targeted
  co1/co2 and 0 co1/co2 sources admitted." R1 is the only rule of fifteen requiring positive
  evidence, and its stated remedy — record `CO1-NOT-APPLICABLE` in `findings_note` — has
  nowhere to live with 0 `search_executions`. **Corrected:** an earlier draft called R1
  "unsatisfiable" — it is not. `co1_src` reads `evidence_sources`, so admitting a single
  Co-1/Co-2 source turns R1 green with no `search_executions` row at all. Only the *waiver*
  path is genuinely unreachable. The finding survives in weaker form: R1 is **vacuous but
  satisfiable**, and promoting `research_dod` to blocking (W6) would still redden every diff
  until the first source is admitted. **Method:** R1 returns `NOTHING-IN-SCOPE` on an empty
  batch; the other fourteen already do, and that inconsistency is the defect.
  Note the ordering trap: `research_batch_dod` prints no `EXAMINED:` line, and
  `run_checks.vacuity_failure()` hard-fails any check declaring `min_items` without one — so
  the `EXAMINED:` line must land first.

### 1.4 Class C — real defects

**C1 · `register_integrity_check --selftest` reports a missed mutation.**
`**SILENT — MUTATION MISSED**: COMPLETENESS: a whole cell section deleted`.
**Settled by experiment, twice, independently.** Two adversarial passes each copied the DB to a
scratch path and populated `evidence_cell_state` with the 15 pilot rows; the mutation then
**fired**, the selftest reported **12/12** and exited 0. So this is an empty subject, not a
logic bug — the completeness arm reads `evidence_cell_state` (0 rows), and the selftest gates
the tamper on `if db_path:`, which tests a path *string* rather than a subject.
**This is the cleanest available demonstration of the whole Part 1 thesis**: the invariant is
correct, the harness is correct, and the report is still wrong, because nothing distinguishes
"could not test" from "tested and passed".

**And it costs more than the failing line.** A synthesis pass claimed `--selftest` "`sys.exit`s
before `check()` runs, so no document is ever evaluated". **That mechanism is wrong** — the code
exits only *if the selftest fails* (`main():389-392`), and the flag's own help says
"mutation-test the checker itself, **then** check the real document". But the conclusion holds
for today, by a different route, and execution settles it:

```
$ python3 scripts/audit/register_integrity_check.py --selftest ; echo $?    # the REGISTERED cmd
SELFTEST FAILED — a tampered invariant went undetected
1
$ python3 scripts/audit/register_integrity_check.py ; echo $?               # plain
PASS: I1–I5 hold across 15 cells × 6 registers (DB cross-check on)
0
```

So the real document check **works and passes**, and the registered invocation never reaches
it, because the empty-subject selftest short-circuits first. **Fixing C1 restores a working
check that is currently unreachable** — which raises its priority above "tidy a confusing
message". The distinction also matters for the fix: this needs no change to `main()`'s control
flow, only to how the selftest classifies an untestable leg.

One caveat on that passing plain run, because it is the same disease: it reports
`(DB cross-check on)` while `evidence_cell_state` holds 0 rows, and the cross-check body is
guarded by `if db_rows:`. The doc→DB leg is therefore skipped, silently, inside a line that
announces it as on.
**Method:** gate on the subject, and report `NOT-TESTABLE (subject empty)`. Then the harder
half: the overall selftest must still refuse to report a clean pass while any leg is
NOT-TESTABLE. "I could not test this" is not "this passed" — which is the whole thesis of §1.1.
**Gate:** `scripts/audit/` is CODEOWNERS-protected.

**C2 · `room_page.py` queries six tables that do not exist.** Not a rename: `rooms` has
`room_code`/`name`/`category` where the script expects `room_id`/`room_label`/`building_type`;
`room_items` has 0 rows and different columns again; and `room_item_population`,
`room_dar_provision` and `room_conflict` have **no substitute at all**. The population
dimension per room-item is a D-SCHEMA decision, not a repoint.
**This partly falsifies N2** ("No `rooms` table") — there is one, with 17 rows.
**Method:** repoint the three tables that have referents; render the missing dimensions as an
explicit "not yet modelled" banner rather than inventing a schema. **Do not** add rooms to
`build_site.py` in the same change (see C7).
**Gate:** owner, for the population dimension (D-SCHEMA).

**C3 · 12 stale `site/specs/` pages — and this is not housekeeping.** Diffing `e-08` and
`a-02` against a fresh render: **the committed pages publish pre-reset determinations**
(`DEAF | stated | CO1+T2`; `ALL | provisional | T4-6-only`) and name `REF-003xx` sources the
reset deleted. The fresh render replaces all of it with "not yet computed". Eleven of the
twelve are the pilot cohort.
**So the stale pages are the last place the deleted corpus is still published as current.**
**Method:** regenerate in a commit that says exactly that, and treat it as the visible half of
the reset rather than as a build step.
**Gate:** owner — the committed-vs-generated policy is still open, and this is the change that
makes it concrete.

**C4 · The project's only reasoning document fails every structural requirement.**
`references/bpc-reasoning/` holds two files: `_template.md` and
`room-acoustic-performance.md`. `validate_reasoning.py --strict` reports **16 errors** on the
latter — four header fields, all eleven required sections, and `Status: PILOT` outside the
enum. `references/connection-reasoning/` holds **only its template — zero real documents**.
The registry's note ("1 doc missing 'F. Provenance trail'") is wrong.
**Worse:** the 9-step rule has **never been mechanically evaluated in the project's history**
— the check sits inside `if b_section_m:`, the only real document has no `## B.` header, so it
silently skips. Zero parameter blocks have ever been checked.
**Method:** bring the document to template conformance in place; then declare `min_items: 1`
on `validate_reasoning` so an empty corpus can never read as clean; then make the 9-step check
report when it finds no `B.` section rather than skipping.
**Gate:** none. (K2's "move it" is withdrawn.)

**C5 · `validate_pydantic_schemas --strict` — 246 findings, 49 unmapped live tables.**
**Method:** treat as a backlog, not a sweep. Split *unmapped table* from *column drift*; rank
by position on the topic→render walk, not by count; adopt **backfill-on-touch** — the first
migration touching an unmapped table adds its model — which converts a 246-item sweep into a
per-change obligation.
**Gate:** `schemas/` and `references/project-standards.md` are both CODEOWNERS-protected, and
unlike the attestation rule this copies, **there is no diff-aware enforcer** — so
backfill-on-touch lands as a level-1 text rule unless one is written. Say so rather than
pretending otherwise.

**C6 · `retired_vocabulary` — 69 occurrences, three classes, one ruling missing.**
The PI snapshot is 7 of 69, and 2 of those are `UNVERIFIED-1` tokens rather than workflow
names. The bulk sits in `references/tier*-verified-sources.json` — a JSON store whose status
against the DB is **unruled**, and which post-reset holds a verified-source list while the DB
holds zero sources. A third class, a hit in Python code, has no ruling at all.
**Method:** rule on the JSON store first (canonical / reference / retire); the vocabulary
question then answers itself. Exempt the PI snapshots only for the workflow-name entries, with
the reason recorded — a blanket PI exemption would also hide genuinely wrong doctrine.
**Gate:** owner, for the JSON store.

**C7 · `build_site.py` drives 93 of ~121 pages.** Its own docstring: `site/populations/` (11)
and `site/rooms/` (17) "have generators … that it does NOT drive". So `site_pages_fresh` — the
freshness gate — is blind to 28 committed pages, and declares no `min_items`.
**Method:** fold populations in (its generator works). **Sequencing matters:** widening the
driver changes the check's subject, and C3 defers the committed-vs-generated policy to the
owner. Widen *after* C3 is ruled, not before, or the redness lands on an unratified policy.

**C8 · `check_rendered_docs`, blocking, certifies nothing.** See §1.1. **Method:** part of A4.

**C8b · The enforcement spectrum has no rung for schema constraints — so every acceptance
condition in this repo has been mislabelled, in both directions.**
CLAUDE.md §2 defines five levels: text rule → audit script → CI non-blocking → CI blocking →
pre-commit hook. **A SQLite `CHECK`, `UNIQUE` or `FOREIGN KEY` is none of them.** Two
independent adversarial passes, working on different pipeline segments, arrived at this
finding separately — which is the strongest signal available here that it is real.

The consequence runs both ways, and the second direction is the dangerous one:

- **`CHECK` and `UNIQUE` are stronger than the spectrum can express.** SQLite enforces them at
  write time on every connection, including a migration. Labelling one "level 2 audit script"
  understates a constraint that cannot be bypassed at all.
- **`FOREIGN KEY` is weaker than it looks.** SQLite leaves FK enforcement **off** per
  connection unless `PRAGMA foreign_keys=ON`, and `scripts/migrate_db.py` sets it explicitly
  `OFF` (lines 164, 251) before every migration script. A `REFERENCES` clause in the DDL
  therefore does not, by itself, stop a migration writing an orphan.
- **But FK constraints are not unenforced, and saying so would be its own error.**
  `migrate_db.py:162-183` runs a *differential* check: snapshot `PRAGMA foreign_key_check`,
  disable FKs for the bulk load, re-enable, diff the violation sets, and raise
  `sqlite3.IntegrityError` on **new** violations. Three caveats belong with that: a
  pre-existing violation baseline is permanently grandfathered (the code comments it as ~18),
  any migration whose first 500 bytes contain `BOOTSTRAP` downgrades the failure to a
  warning, and its CI reach is indirect — through the blocking `migration_reproducibility`,
  which rebuilds from migration history.

**Method:** add a **D (schema constraint)** rung to CLAUDE.md §2's spectrum, distinguishing
`D` (write-time, absolute) from `D(fk)` (deferred differential, with the three caveats). Part 2
uses this rung throughout; it is proposed here because the spectrum is doctrine, not tooling.
**Gate:** CLAUDE.md is a derived map, so amending it is not a doctrine change — but §2's
spectrum is quoted from `architecture/project-architecture-guidebook-v2.3.md`, so confirm the
source before editing the map.

**C9 · `parts/v10/` is stale in all 15 files and entirely ungated.** Fingerprint
`3d7fb5d50de6` (user_version 25, against a live 53); `part13.md` still publishes "640 sources"
with a full tier distribution — a corpus that no longer exists. `generate_parts.py` appears in
no workflow and no registry entry.
**This is C3's problem without C3's advisory check.** Method: regenerate with C3, and register
a freshness check.

**C10 · Three of the repo's own orientation documents describe a check that does not exist.**
`session_pointer_resolvable` is named as "registered blocking" in `CLAUDE.md:424` and
`sessions/handoff-next-session.md:12`. It appears in **no registry entry and no code**, and
`scripts/audit/session_pointer_audit.py` does not exist.

**The alarming reading is wrong, and was tested.** The script was *deliberately* deleted on
2026-08-06 — the registry records that it "patrolled a hazard whose root cause was a five-line
fix in the dispatcher it was watching" — and its function was redistributed to `run_checks.py`,
`validate_cross_refs` and `test_db_integrity` L04. An adversarial pass proved by execution that
the redistribution holds in **both** failure modes: a missing pointer file FAILs
(`run_checks.py:217-232`), and a *dangling* pointer target FAILs inside
`citation_mining_completeness.py`. **No gate is disarmed.**

So this is a documentation defect — but a compounding one, and the two worst instances were
missed by the first pass:
- `sessions/handoff-next-session.md:12` asserts the check is "registered blocking", which will
  be read as authoritative by the next session, because the handoff is where CLAUDE.md §9 sends
  it to start.
- `CLAUDE.md:425` still describes the **SKIP** behaviour as current — *"an unresolvable pointer
  makes `run_checks.py` SKIP the checks that read it, which disarms a blocking gate silently"*
  — when that is the hazard that was **fixed**. The onboarding document warns about a live
  danger that no longer exists, in the same breath as naming a checker that never existed.
**Method:** correct all three call sites to name the three real enforcers. **Gate:** none.

**C10b · No blocking check covers generated render output.**
`scripts/audit/check_rendered_docs.py:227` globs `REPO / "specs"` — the **top-level** `specs/`
directory, which holds 2 hand-authored briefs. The 93 generated pages under `site/specs/` have
never been in its scope.

**That scoping is deliberate, not a bug.** `DR-2026-07-25-rendered-document-integrity-gate.md`
sets the gate's subject as hand-authored pages under `specs/`, anticipates the objection "this
is a gate for one page", and provides for new hand-authored pages entering scope automatically.
An adversarial pass reported this as a misdirected glob; that reading is wrong and is recorded
here so it is not re-found as a bug.

**The consequence survives the correction, and is sharper than the bug would have been.** The
only *blocking* rendered-document gate covers 2 hand-authored pages by design, and examines 0
of them today. The 93 generated pages are covered only by the **advisory** `site_pages_fresh`.
So generated output — the thing an actual reader sees — has no blocking coverage at all, which
is precisely why the 12 stale pages publishing deleted determinations (C3) can ship.
**Method:** this is the same owner ruling as C3 and C7 — settle the committed-vs-generated
policy, then decide whether `site_pages_fresh` becomes blocking. Do not widen
`check_rendered_docs`; its DR-defined subject is a different thing.

**C11 · The most doctrinally important relationships are the ones the schema cannot enforce.**
A sweep of every identifier-shaped column (`*_id`, `*_ids`, `*_ref`, `*_refs`, `*_code`,
`*_slug`, `*_sha`) that is neither a primary key nor covered by a foreign key returns **19**:

```
$ python3 -c "…PRAGMA foreign_key_list / table_info sweep…"
IDENTIFIER-SHAPED COLUMNS WITH NO FK AND NOT A PK: 19
```

Most are benign (`content_sha`, `item_id`). Seven are load-bearing — relationships the schema
*models* but cannot *check*:

| Column | The relationship it carries |
|---|---|
| `evidence_cell_state.governing_refs` | determination → its governing sources — **the anti-hallucination field** |
| `search_executions.admitted_ref_ids` | search → the sources it admitted |
| `evidence_population_match.source_ref` | a *second* source key beside the real FK `ref_id` |
| `evidence_sources.superseded_by_ref_id` | the supersession chain |
| `supersession_check.superseding_ref_ids` | the same chain again, as a JSON array |
| `jurisdictional_values.spec_id` | points at a `specification` table that has never existed |
| `source_value_extractions.root_id` | the value-genealogy root |

**Two findings, and the second is the sharper one.**

First: `governing_refs` is a JSON array, so SQLite cannot resolve it. That is *why* the blocking
`validate_evidence_state` can accept a `stated` cell whose governing refs name nothing — there
is no key to resolve them against. The field that makes a claim answerable is the field the
database cannot check.

Second: **three relationships are stored twice** — `governing_refs` beside the proper junction
`cell_source_links`; `admitted_ref_ids` beside `search_admissions`; `superseding_ref_ids`
beside the `supersession_check` row itself. In each pair one side is FK-checkable and one is
not, **and nothing checks that the two agree.** CLAUDE.md §9 guardrail 5 already rules on this
shape — when two stores disagree, reconcile then retire the shadow. Here the shadow is the JSON
column and the canonical form is the junction.

**Method:** for each of the three pairs, make the junction authoritative, have code read it,
and add a consistency assertion to `test_db_integrity` for as long as both exist. **Do this
before content, not after** — every row written in the meantime doubles the reconciliation.
The junctions are empty today, so the migration is free.
**Gate:** owner — retiring a column is a schema decision (D-SCHEMA), and the JSON columns are
read by existing code that must be swept first (§0 rule 5).

**C12 · An unguarded replay script can silently undo the clean-room reset. Fix this first.**

`scripts/migrations/session_2026_05_11g_replay.py` writes `evidence_sources`,
`source_slug_links`, `citation_mining` and `gaps` **directly to the canonical database**. Every
property below was verified:

```
$ grep -n "DEFAULT_DB\|add_argument" scripts/migrations/session_2026_05_11g_replay.py
33:DEFAULT_DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
38:    p.add_argument("--db", default=DEFAULT_DB)      # no required args
$ ls -la scripts/migrations/session_2026_05_11g_data.json
-rw-r--r-- 1 root root 45944 …                          # the payload is present
```

Its payload holds **14 new `evidence_sources`, 14 `source_slug_links`, 21 `citation_mining`
rows, 5 source updates, 8 new gaps and 2 gap closures** — 64 pre-reset rows.

Four properties compound into the hazard:
1. **It runs with no arguments** and defaults to the canonical DB.
2. **Its payload is committed and present**, so it would succeed, not fail safe.
3. **It lives in `scripts/migrations/`** — the directory CLAUDE.md §0 rule 4 names as *the*
   sanctioned write path — so it reads as blessed.
4. **`migrate_db.py` globs `*.sql`**, so running it leaves **no `data_migrations` row**. The
   write would be invisible to the ledger that exists to record writes.

**It would reintroduce, without a trace, precisely the corpus DR-2026-08-06 deliberately set
aside** — and the blocking `migration_reproducibility` gate compares `COUNT(*)` on six tables,
so it *would* catch this one (the counts change). That is luck, not design: the same script
shape doing `UPDATE`s would pass.

**Its seven siblings are already guarded.** `scripts/migrate/` carries `_legacy_guard.py`, added
2026-08-04, and seven of nine scripts there import it. **Three writers were missed:**
```
$ for f in scripts/migrate/*.py scripts/migrations/*.py; do grep -q _legacy_guard "$f" || echo "$f"; done
scripts/migrate/init_database.py
scripts/migrate/phase_jv_appendix_a.py
scripts/migrations/session_2026_05_11g_replay.py
```
**Method:** import `_legacy_guard` into all three. It is a five-line change, it needs no
decision, and it should land before anything else in this document. Then consider whether a
`.py` file belongs in `scripts/migrations/` at all — the directory's contract is `*.sql`.
**Gate:** none. **Falsification:** if `_legacy_guard` does not in fact refuse the canonical DB,
this fix is theatre — read it before relying on it.

**The wider finding:** a write-map of all 67 tables classifies **16 scripts as TOOL writers** —
direct writers of the canonical DB, contrary to §0 rule 4. `scripts/db.py` alone carries 22
write statements across 15 tables, while CLAUDE.md §4 describes it as the tool to "use to *read*
freely". The rule is real and the practice diverged from it long ago; the honest options are to
enforce the rule or to amend it, not to keep asserting it.

**Also surfaced: 11 tables have no writer at all** — `case_studies` and its four satellites,
two `economics_entry_*` junctions, `external_root_registry`, `extraction_population_links`,
`situations`, and `room_items` (which has never had a single DML statement in repo history,
only `CREATE TABLE`). Two views, `v_unregistered_roots` and `v_root_id_conflicts`, read
`external_root_registry` and can therefore only ever return the trivial answer. **A table
nothing can fill and a table waiting for unwritten code look identical in a schema dump** —
which is exactly the ambiguity the pre-content review exists to resolve.

**C13 · Attestation validity is checked one commit at a time; the 74-file corpus is checked by
nothing.**

```
$ grep -n "base=" scripts/audit/adherence_log_audit.py
551:def audit(check_filter=None, base="HEAD~1", head="HEAD"):
$ ls attestations/*.json | wc -l
74
```

Both blocking attestation checks — `attestation_presence` and `attestation_schema` — are
registered without a `--base` override, so each examines only the files changed in the last
commit. Of the four registered `--check` groups, only one reads all 74 attestations at HEAD.

**Half of this is correct design and must not be "fixed".** *Presence* is a property of a
change: the question "did this commit's synthesis-path edit bring an attestation?" is only
answerable against a diff, and widening it would be meaningless.

**The other half is a real hole.** *Schema validity* is a property of a file. An attestation
that was schema-invalid when committed stays invalid forever and is never re-examined, because
the only check that would catch it looks at one commit's diff. The corpus-wide validity figure
(74/74 today, established by hand during this review) rests on no registered check.

**Method:** keep `attestation_presence` diff-scoped. Add a corpus-scoped schema pass — either a
second registered entry with `--base` widened, or the existing `--check` group that already
reads all 74, registered in its own right. Cheap, no decision required.

### 1.4b The handshake layer — what the stage contracts actually assert

`governance/pipeline-contract.yaml` declares **19 criteria** across five stages plus six
cross-stage. Its own auditor reports 14 VERIFIABLE / 5 INCOMPLETE / 0 BROKEN. An independent
reconciliation finds **11 of the 19 overstate reality** — six because their subject is empty,
two because the named enforcer checks a different artifact, one because the registered
invocation exits before the check runs (C1), one because the contract and the registry disagree
about whether an enforcer exists, and two because the enforcer is narrower than the prose.

Three findings from that layer belong in the pre-content list:

- **The `[ADHERENCE-LOG — stage N]` boundary emits nothing.** The numbered stage list it keys
  on lives only in the deployed claude.ai preferences, which are not in the repo — so the
  contract's stage ids are a repo-side reconstruction, and its enforcer cannot see the artifact
  it names. This also blocks ratification: `DR-2026-07-13-pipeline-contract.md` reads
  ACCEPTED-with-outstanding-precondition while the YAML still says `PROPOSED / ratified: false`,
  and **the ratifying act requires a document that does not exist in git.**
- **The B-before-E phase gate exists only in prose.** The workplan's strict "no BPC is rewritten
  until its linked sources pass Phase B verification" is attributed to `validate_reasoning.py`,
  which **never opens the database** — so it cannot evaluate the condition. This is the gate
  protecting the project's primary deliverable from being written on unverified evidence, and
  it is a sentence.
- **Ten ordering assumptions are neither declared nor guaranteed by the runner** — checks that
  presuppose another check has run, share a fixture, or read state a sibling may rebuild.

### 1.5 Class D — owner decisions, with a recommendation each

| # | Decision | Recommendation |
|---|---|---|
| **D1** | Branch protection on `main` | **ENABLE — alone, in its own window.** Use the nine-job required set in `tooling-register.md` §6.7 and its three traps (especially: require `Classify change`, or a broken classifier silently skips every battery into a green PR). **Do NOT add `DB integrity` yet** — it is 70/70, but ~30 of those 70 reference only empty tables, so requiring it today locks in a vacuous green. Add it after A4. |
| **D2** | Migration exemption list | The enumeration is now solid: `resolve_dois.py` writes `evidence_sources` (UPDATE), `evidence_source_authors`, `pipeline_runs`; `verify_urls.py` writes `evidence_sources` (UPDATE) and `url_verification_runs`. The exempt tuple is exactly `(evidence_source_authors, pipeline_runs)` — **two of five write targets**. **But the obvious fix does not exist:** `EXEMPT_TABLES` is whole-table, so exempting `evidence_sources` blinds the deep gate to hand-edited tiers and titles — the exact tamper it was built to catch — and `VOLATILE_COLUMNS` matches by name across all tables. Recommend: exempt `url_verification_runs` (clean, whole-table, job-owned) and **defer** `evidence_sources` until column-level exemption exists. |
| **D3** | Promote reproducibility gates | **After D1 and A4, in a separate window.** Cheap one first: widen the blocking `COUNT(*)` from six tables to all non-exempt. `migration_reproducibility_deep` second. |
| **D4** | `verification_status` CHECK | **DEFER.** The migration is free with an empty table; the *vocabulary ratification* is the real decision, and ratifying with zero rows to test against is how a mistake gets frozen. |
| **D5** | Five rival (c)-layer tables | Needs the consolidation analysis, not a vote. |
| **D6** | `room_page.py` fix-or-archive | **FIX** the three repointable tables; the population dimension is a separate D-SCHEMA question (C2). |
| **D7** | `test_adjudication_integrity`, `test_generate_parts_4_2` | Re-run the first — its blocking reason was content debt the reset cleared. The second exits 0 having asserted nothing. **Do not delete either**: `tooling-register.md` §6.5 sets quarantine-with-reason as the terminal state, and deletion removes a script from the enumeration the register exists to maintain. |
| **D8** | `citation_mining_pipeline.py` | See Part 2 stage 6. |
| **D9** | `workplan/` naming | **Do not rename** (K3). Generate `workplan/INDEX.md`, date-sorted, from file front-matter — which is what CLAUDE.md §9's instruction actually needs. Keep the forward-only naming check. |
| **D10** | Retire three connection registers | **NOT READY** (K5). The prerequisite reconciliation is not recorded as executed, and DB `connections` is now 0 rows. Re-establish the finding before acting on it. |
| **D11** | `.ignore` | No change proposed. |

### 1.6 Sequencing — this is load-bearing

`tooling-register.md` §6 withdrew, as unwise, the exact bundle this document's first draft
proposed. The order below exists so that is not repeated:

1. **A1–A3** (bootstrap) — no gate, no risk, unblocks every future session.
2. **B2** (the crash) — hides other findings while it stands.
3. **A4** (`min_items` on blocking checks) — **everything downstream depends on this.**
4. **D1** (branch protection) — alone, nothing else promoted in the same window.
5. **C1, C4, B1, B3, B4** — mechanical, reversible.
6. **D2 → D3** (exemption ruling, then gate widening) — in that order, separate window.
7. **C3 ruling → C7 → C9** (render policy, then scope, then parts).
8. **C5, C6, D5–D10** — backlogs and rulings, unordered.

---

## Part 2 — Pipeline anatomy

*(Twelve stages, each answering (a)–(h). See §2.0 for the reading key.)*

### 2.0 Reading key

Every tool, table and mechanism carries one of three states, because the reset made the
distinction load-bearing:

- **BUILT+EXERCISED** — code exists, has run, and rows or artifacts prove it.
- **BUILT+UNEXERCISED** — code exists and runs, but its table is empty or no artifact exists.
- **DESIGNED-ONLY** — named in doctrine or a workplan; no code, or code that crashes.

Enforcement levels use the repo's 5-level spectrum from CLAUDE.md §2:
**1** text rule · **2** audit script · **3** CI non-blocking · **4** CI blocking · **5** pre-commit hook.
No level-5 hook is installed anywhere in this repo (single author), so **4 is the ceiling.**

### 2.1 Stage 1 — Topic & taxonomy creation

#### (a) Tools, tables, methodology

**Tables** (all in `data/guidebook.db`; counts from a single read-only enumeration of
`sqlite_master`):

| Object | Rows | State | Note |
|---|---|---|---|
| `slugs` (mig. 001; `serves_axes` added mig. 034) | 106 — ACTIVE 80 / STUB 23 / MERGED 3 | **BUILT+EXERCISED** | `SELECT status,COUNT(*) FROM slugs GROUP BY 1` |
| `slugs.serves_axes` | **1 of 106 non-null** | **BUILT+UNEXERCISED** | only `vestibular-balance-built-environment` = `["AX-BAL"]` |
| `axes` (mig. 030) | 17 — ESTABLISHED 10 / PARTIAL 2 / STUB 5 | **BUILT+EXERCISED** | the operative demand layer |
| `access_needs` (mig. 031) | 17 | **BUILT+UNEXERCISED** | 16 of 17 have `typical_stakes IS NULL`; wiring in (b) |
| `access_need_axis_map` | 21 | BUILT+EXERCISED | `A-AT`, `A-TIME` map to no axis; `AX-PAI`, `AX-THR` are reached by no need |
| `access_need_icf` | 43, all `confidence='confirmed'` | BUILT+EXERCISED | |
| `populations` (mig. 032) | 23, flat, `parent_code` non-null on **0** rows | **BUILT+EXERCISED** | matches `schemas/enums.py PopulationCode` in both directions |
| `population_axis_map` (mig. 030) | 53 | BUILT+EXERCISED | 3 populations (`ALL`, `ID`, `MOVE`) map to **zero** axes |
| `population_reclass` (mig. 030) | 29 | **obsolete scaffolding** | 14 rows dangle against `populations`; no FK declared, so `PRAGMA foreign_key_check` returns `[]` |
| `life_stage_modifiers` (mig. 032) | 2 — `SEN`, `CHD` | BUILT+UNEXERCISED | live table; nothing joins to it |
| `access_duration` / `access_stakes` (mig. 031) | 3 / 3 | BUILT+UNEXERCISED | vocabulary tables no column references |
| `terms` | 88 across 18 domains; 17 rows `domain='functional_axis'` | BUILT+EXERCISED | |
| `term_aliases` | 2382 across **15** languages | BUILT+EXERCISED | provenance in (f) |
| `lang_jur_map` (mig. 023, populated 2026-07-24) | 70 = 50 PRIMARY + 20 SECONDARY; 19 languages × 48 jurisdictions | **BUILT+EXERCISED** | |
| `situations` (mig. 030) | **0** | **DESIGNED-ONLY in effect** | `grep -rn "situations" --include=*.py scripts/ tools/ schemas/` returns **no hits** — zero readers as well as zero rows |

**Scripts and validators** (registry ids and levels read from
`governance/check-registry.yaml`; verdicts from running each script):

| Path | Registered id · level | State | What it actually does |
|---|---|---|---|
| `scripts/validate_axes.py` | `validate_axes` · **blocking** (battery `schema`, kinds `schema,data`) | BUILT+EXERCISED — `OK axis-layer integrity: 0 errors, 1 coverage warnings` | Resolves axis codes in `population_axis_map`, `item_axis_links`, `access_need_axis_map`; asserts `role ∈ {PRIMARY,SECONDARY,ALIAS,SITUATIONAL}`; **warns** on axes with 0 population maps (`AX-COG-L`) and on axes with 0 item links (none — 17/17 covered). Carries a `--selftest` mutation harness. |
| `scripts/validate_population.py` | `validate_population` · **advisory** | BUILT+EXERCISED — `PASS (23 live codes; 428 value(s) across 14 column(s) all resolve)` | P1 enum↔table parity both ways; P2 every discovered `population*` column resolves; P3 retired-code crosswalk; P4 packed CSV codes; P5 unregistered scope markers. Columns are **discovered, not transcribed**. Downgraded blocking→advisory 2026-08-05; the registry note records that its predecessor was blocking, green, and had never validated anything (it scanned BPC front matter that does not exist — 0 of 102 files). |
| `scripts/audit/alias_provenance_audit.py` | `alias_provenance_audit` · **blocking** (battery `data`) | BUILT+EXERCISED — **exit 0** | Classifies each alias's provenance by substring match on the free-text `notes` column. Today: `all 2382 | verified 15 | model-gen 1163 | curated 304 | code 20 | UNKNOWN 880`. Also prints `REQUIRED BUT UNSEARCHABLE — no aliases at all: AR, BN, HI, SW`. Passes because 880 pre-2026-07-24 rows are grandfathered: `RESULTS: all post-2026-07-24 aliases carry provenance`. |
| `scripts/audit/population_integrity_audit.py` | `population_integrity_audit` · **advisory** (battery `research`) | **BUILT+UNEXERCISED post-reset** — `ISSUES: 0` with all three junctions at 0 rows | Its registry note still reads `RED on main (31 issues)` — **stale**; the reset emptied its subjects. Checks 1–5 each report `0 rows` or `(empty)`. |
| `scripts/validate_jurisdiction.py` | `validate_jurisdiction` · **blocking** | BUILT+EXERCISED — `PASS: 0 errors, 55 warnings`, exit 0 | Warns 38 times on jurisdictions "not in canonical 24"; the enum it reads (`schemas/enums.py JurisdictionCode`) actually has 27 members. |
| `scripts/audit/retired_vocabulary_audit.py` | `retired_vocabulary` · advisory · kinds `always` | BUILT+EXERCISED — 69 occurrences | `governance/retired-vocabulary.yaml` has 19 entries. **RV-010 `physically disabled` and RV-011 `energy-limiting chronic illness` carry `severity: doctrine`** — the anti-umbrella rule is genuinely mechanised. The 13 population codes DR-2026-07-23 retired are **not** entries. |
| `scripts/audit/validate_pydantic_schemas.py` | `validate_pydantic_schemas` · advisory | BUILT+EXERCISED, **FAILS** (advisory) — `Discovered 65 Pydantic models …; 17 mapped to a live table`, `Total drift findings: 246` | `MODEL_TABLE_MAP` is a hand-curated 17-entry list. **None of `axes`, `access_needs`, `access_need_axis_map`, `access_need_icf`, `population_axis_map`, `terms`, `term_aliases`, `lang_jur_map`, `situations` is mapped.** `population.Population` is mapped and shares zero fields with its table. |
| `scripts/db.py` | — | BUILT+EXERCISED **as a reader only** | There is **no CLI write path for any stage-1 entity**. `db.py --help` lists 33 subcommands; none is `add-slug`, `add-term`, `add-alias`, `add-population`, `add-axis`. `next_term_id()` exists at line 420 and is exposed by nothing. Every stage-1 row is hand-written SQL routed through `scripts/emit_data_migration.py`. |

**Governance / methodology documents.** `governance/functional-taxonomy.md` (RATIFIED v1.2,
2026-07-21) is the two-layer doctrine. `governance/population-taxonomy.md` still carries a
CANONICAL header but its code set is superseded (see (g)).
`decisions/DR-2026-07-21-two-layer-functional-taxonomy.md`,
`DR-2026-07-22-work-from-axes.md`, `DR-2026-07-23-population-schema-replace.md`,
`DR-2026-07-24-lang-jur-map-roles.md`,
`DR-2026-07-25-controlled-vocabulary-grouping-and-provenance.md` are the operative decisions.
`references/project-standards.md` lines 557 (work-from-axes), 563 (design-equivalence exception),
571 (body-size group served by `A-SIZE`) and 574 (operative population source) are the rule-ledger
entries. `references/native-alias-verification.md` defines the
MODEL-GENERATED → VERIFIED-{GLOSSARY,NATIVE,CROSS} promotion route.

#### (b) How they relate to each other — the internal wiring

The stage has one real hub and several unattached satellites. The hub is `axes`. Every other
stage-1 vocabulary either hangs off it by foreign key or hangs off nothing.

`axes` is reached by three FK junctions — `population_axis_map` (53 rows, binding 20 of 23
populations), `item_axis_links` (158 rows, binding **93 of 93** items, and therefore the stage-1 →
stage-2 edge), and `access_need_axis_map` (21 rows) — plus one text edge, the JSON
`slugs.serves_axes`, populated on a single row. `populations` is reached only through
`population_axis_map` and through stage-2's `item_population_links`; it has no children of its own
because `parent_code` is non-null on zero rows, which is exactly what DR-2026-07-23 decreed. `terms`
is the parent of `term_aliases` (FK on `term_id`) and of `term_item_links` (147 rows, 69 items,
0 orphans verified by left join), so the retrieval vocabulary reaches items but not slugs.

**Which layer is real and which is scaffolding.** `axes` is the operative demand layer: it is the
only stage-1 vocabulary with a blocking validator, the only one with an FK edge into stage 2, and
the only one that covers its downstream fully (17/17 axes carry at least one item link). `populations`
is real, but doctrinally it is a *vector over axes*, not a bucket — `functional-taxonomy.md` §3.3
states it in those words and `references/project-standards.md` RULE 2026-07-22 ratifies it; the
23 codes are enum-parity-checked in both directions by `validate_population` P1. `access_needs` is
a parallel vocabulary that is **not wired**: it touches the rest of the graph through exactly one
edge, `access_need_axis_map.axis_code → axes`, and `grep -rn "access_needs" --include=*.py scripts/
tools/ schemas/` finds only `validate_axes.py` (which reads the *axis* column of that junction) and
a comment in `research_batch_dod.py`. There is no `population_access_need` table anywhere in the
67-table schema, no `item_access_need_link`, and no Pydantic model. The field that would carry the
population relation, `access_needs.absorbs`, is prose by declaration — migration 031 comments it
"populations/situations it covers (prose, audit-side)". `situations` is worse: 0 rows, 0 readers,
and its three attachment columns (`attaches_items`, `attaches_axes`, `attaches_profiles`) are CSV
`TEXT` with no FK, so even a populated row could dangle silently.

**Four places where the join is by text rather than by key, each a live fault line.**

1. **Language.** `term_aliases.language` holds 15 **lowercase** values
   (`da de en es fi fr id it ja ko nl no pt sv zh`); `lang_jur_map.language` holds 19 **UPPERCASE**
   values (the same set plus `AR BN HI SW`). Nothing reconciles them. There is no `languages` table
   and no `LanguageCode` in `schemas/enums.py` (43 enum classes; none for language). That this
   hazard is not theoretical is recorded in the repo itself: `scripts/generate_search_queries.py:271`
   carries a `BUG FIX 2026-07-24` comment stating that the absence of a `lang.upper()` normalisation
   made adversarial query generation **inert for its entire prior existence**; the fix is
   `lang_key = (lang or '').upper()` at line 276.
2. **Jurisdiction.** Five vocabularies are live at once and none is canonical: `lang_jur_map` has
   48 jurisdictions and writes `UK`; `jurisdictional_values` has 12 and writes **`GB`** (20 rows),
   with no `UK` at all; `schemas/enums.py JurisdictionCode` has 27 members;
   `skills/multilingual-research_SKILL.md` declares 46; `validate_jurisdiction.py:116` prints
   "not in canonical 24". Five numbers, no table.
3. **Alias provenance** is a substring test over free text (`alias_provenance_audit.classify()`
   does `if "model-generated" in notes`). There is no provenance column.
4. **`population_reclass.population_code` declares no FK**, which is why 14 of its 29 rows dangle
   against `populations` while `PRAGMA foreign_key_check` returns clean.

On that last point one correction to the record is due: of the 14 dangling codes
(`CFS CHD DBL EXH LCOV MCAS NEU OAD OFS PCS POTS SENS UPL VIS`), **13 were retired by
DR-2026-07-23 and one, `CHD`, was re-homed, not retired** — DR-2026-07-23 lines 39-41 move life
stage (`SEN` older adults, `CHD` children) to `life_stage_modifiers` as "orthogonal modifiers", and
that table is live with exactly those two rows. The dangling count and the missing-FK mechanism are
unaffected; only the label on one row changes.

#### (c) Relation to the previous stage — the entry contract

Stage 1 is the head of the pipeline; its upstream is doctrine, not data. That makes the entry
contract a *governance* contract, and it is the weakest link in the stage.

`governance/pipeline-contract.yaml` (`status: PROPOSED`, `ratified: false`, `enforcement_level: 2`)
declares five stages — `research`, `collection`, `judgment`, `synthesis`, `render`. **There is no
taxonomy stage and no scope stage in the contract at all**, so stages 1 and 2 have no declared entry
criteria of any kind. The real gate is DG-NON delegation: under `governance/decision-protocol.md`
§2.4, population taxonomy and evidence-tier definitions are owner-only — an agent proposes, it does
not decide. `scripts/decision_capture.py` (registered `decision_capture`, **blocking**, battery
`governance`) checks that a decision record exists and is well-formed. It does **not** check that a
DB taxonomy change carries one.

So: **NOTHING ENFORCES** that a new `populations`, `axes` or `access_needs` row was authorised by a
Decision Record. The only coupling is incidental — migration 032 and the `schemas/enums.py` edit
land in the same commit, and `validate_population` P1 fails if they subsequently diverge. That is
an after-the-fact parity check between two artifacts, not an authorisation check on either.

#### (d) Relation to the next stage — the exit / handoff contract

| Handoff stage 2 depends on | Enforcer | Level |
|---|---|---|
| Every `item_population_links.population_code` resolves to a live population | `test_db_integrity` **A03** (`RESULTS: 70/70`); re-checked by `validate_items` V5, which re-verifies both FKs by hand because "SQLite enforces FKs per-connection and they are OFF by default" | **4** (`test_db_integrity`, blocking) + **3** (`validate_items`, advisory) |
| Every `item_axis_links.axis_code` resolves to a live axis | `validate_axes` | **4** |
| Every `term_item_links.item_code` resolves | no entry in `test_db_integrity`'s A-series; 0 orphans verified by hand | **UNENFORCED** |
| Every slug carries `serves_axes` (≥1) — `functional-taxonomy.md:326`, curation rule 3, "Slug discipline" | **NOTHING ENFORCES THIS.** `grep -rn serves_axes --include=*.py scripts/ tools/ schemas/` returns exactly one hit, `schemas/slug.py:31` (`Optional[str] = None`, never read). 1 of 106 rows populated | **UNENFORCED** |
| Every population is a non-empty vector over axes | `validate_axes` warns the *converse* only (`WARN: 1 axes with zero population mappings: ['AX-COG-L']`). Populations with no axes are not reported: `ALL`, `ID`, `MOVE` | **UNENFORCED** |
| Aliases exist in every required search language | `alias_provenance_audit` prints `REQUIRED BUT UNSEARCHABLE — AR, BN, HI, SW` and **exits 0** | **4, non-failing on this condition** |

The `serves_axes` hole has a second face worth recording: the field is authored in two places and
lands in neither. `references/bpc/seating-and-rest/energy-conservation-rest-points-seating.md:12`
carries `serves_axes: [AX-STA, AX-PAI, AX-AMB, AX-BAL]` in markdown front matter that never reaches
the DB. So the doctrinal requirement has one column at 1/106, one front-matter convention with no
importer, and zero validators.

#### (e) The goal of the stage

Stage 1 exists to build the **curation gate**. `functional-taxonomy.md` §0 states it in a sentence:
*"A source is only findable if some entity names what it is evidence about; it is only curatable if
an entity exists for it to attach to."* Concretely the stage must produce (i) a **demand vocabulary**
(`axes`) framed as person-environment interaction rather than bodily deficit, so that mechanism
evidence has somewhere diagnosis-neutral to attach; (ii) a set of research **topics** (`slugs`) that
carve the built-environment/disability space without gaps or overlaps, each declaring which axes it
serves; (iii) a **community vocabulary** (`populations`) naming specific self-identified communities
as vectors over those axes, never as umbrellas that absorb them; (iv) a **retrieval vocabulary**
(`terms` / `term_aliases`) in every language the project claims to search, so non-English literatures
are reachable at all; and (v) the **jurisdiction × language scope map** (`lang_jur_map`) that decides
which search cells are *required* versus genuinely not-applicable. The deliverable is not content.
It is the coordinate system every later stage indexes into, and every honest denominator downstream
— "we searched 3 of 70 required cells" — is a stage-1 artifact.

#### (f) How the tools support that goal — and where they do not

**Where they support it.** The axis register does the anti-erasure work it was built for, and it is
checkable. `references/project-standards.md:563` ratifies `COM` and `BRAIN` as design-equivalence
exceptions on condition that the union of member axis signatures is preserved, and names the
expected signatures; against the DB, `COM` carries `AX-BAL(SITUATIONAL) AX-CHM(PRIMARY)
AX-COG-O(SECONDARY) AX-STA(PRIMARY) AX-THR(SECONDARY)` and `BRAIN` carries `AX-AMB AX-ARO AX-BAL
AX-COG-O AX-COM-E AX-SPR AX-STA` — both sets match the rule text exactly, row for row. A doctrine
claim that is verifiable against data, and verifies, is rarer in this repo than it should be.
`validate_population` was rewritten to *discover* population-bearing columns rather than transcribe
a code list, which is the structurally right fix and the reason it now resolves 428 values across
14 columns instead of validating an empty file set. `retired_vocabulary_audit` carrying the two
forbidden umbrella phrases at `severity: doctrine` is a genuine promotion of a doctrinal rule to
mechanical enforcement. And `alias_provenance_audit`'s `REQUIRED BUT UNSEARCHABLE` block is exactly
the honesty the mission asks for: it names structural zero-coverage instead of letting it read as
"no results found".

**Where they do not.** Four things, in descending order of consequence.

*The demand layer has no confidence column.* `functional-taxonomy.md` §3.2 makes mapping-confidence
the honesty mechanism — "This replaces v1.0's flat PRIMARY/SECONDARY roles … the staged schema
carries both (role for query weighting, confidence for disclosure)". `PRAGMA
table_info(population_axis_map)` returns `population_code, axis_code, role, note, created_at,
created_by_session`. Only `role` shipped. The only `mapping_confidence` column in the live schema is
on `population_reclass`, the obsolete scaffolding table. The disclosure half of §3.2 does not exist
in the data, which means a navigation hypothesis and a confirmed relation are stored identically.

*The retrieval vocabulary is 49% model-generated and 37% unprovenanced.* 15 of 2382 aliases carry a
verification marker; 1163 are model-generated; 880 predate the provenance convention and are
grandfathered as UNKNOWN. Four of the 19 required languages (AR, BN, HI, SW) have **zero** aliases,
so a stage whose entire purpose is findability ships a vocabulary that cannot be trusted for most
languages and cannot be used at all for four of them.

*The access-need layer is a doctrinal defect, not merely an unwired table.*
`references/project-standards.md:571` states that LPA, TALL and BAR "form the body-size-and-stature
group, **served by the A-SIZE access need**". `A-SIZE` exists in `access_needs`. There is **no
column anywhere in the 67-table schema** in which a population↔access-need relation can be stored.
So doctrine asserts a relation that the data model cannot represent, and the assertion survives only
in prose. Add that `A-AT` and `A-TIME` map to no axis, `AX-PAI` and `AX-THR` are reached by no need,
and 16 of 17 needs have `typical_stakes IS NULL`, and the vocabulary is not merely unwired — it is
unfinished in the direction doctrine most depends on.

*Two quarters of the owner-defined frame have no canonical table.*
`DR-2026-08-06-clean-room-evidence-reset.md` §4.4 says so in terms: "The frame has two quarters with
no canonical table … Building those two vocabularies is the first frame work after this reset."
Five days later there is still no `languages` table and no `jurisdictions` table, and
`jurisdictional_values` still writes `GB` while `lang_jur_map` writes `UK`.

*And there is no write tooling at all.* Every stage-1 row is hand-authored SQL. The `db.py` write
paths that do exist for later stages (`log_search`, `add_source`) demonstrate that this project
knows how to put invariants at the point of writing — `log_search()` refuses H05 and H07 violations
before the row lands, with a named cause. Stage 1 has none of that, which is why its acceptance
conditions below fall so heavily into the D and UNENFORCED columns.

#### (g) How doctrine conditions the stage — what it FORBIDS

`governance/mission-and-epistemics.md` @ `0f2f525`:

**Commitment 1** ("Specifications serve questions; questions serve people; people are not uniform")
**forbids** a taxonomy that treats a population code as a homogeneous bucket.
`functional-taxonomy.md` §0.5.2 executes it: "`population_axis_map` (§4) is therefore a retrieval
index and navigation hypothesis … never a portrait. A person is never the join of their axis values."
**Commitment 3** (Co-1 co-primary with T1, CRPD Art. 4.3) **forbids** subordinating profile-level or
lived-experience corpora to axis-derived guidance — §3.1: "Profile-level and Co-1 evidence … are
never subordinated … Conflicts … display at parity … no precedence rule exists."
**Commitment 4** (Design Modes; the population range "neither bounds nor defines the person")
**forbids** reading any axis value as a stored attribute of a person (§0.5.3).
**Commitment 7** (teaches judgment, does not substitute for it), with
`DR-2026-07-21-product-posture-thinking-tool-not-authority`, **forbids** presenting the taxonomy as
an authority on who anybody is.

`decisions/DR-2026-07-22-work-from-axes.md` (D-METH, ADOPTED, owner directive) carries the sharpest
prohibition at this stage. Curation proceeds **from the axes** — the specific, non-erasing demand
layer — and broad umbrellas are forbidden as profile codes; umbrellas "may exist only as additive
cross-cutting tags over specifics, never as replacement codes". The DR records three self-caught
erasures as its evidence base. It is **superseded in part** by
`DR-2026-07-23-population-schema-replace` sub-decision 6, which ratifies `COM` and `BRAIN` under a
three-part design-equivalence test (comorbidity/overlap; union of member axis signatures preserved;
no opposed demand). Both are operative: the base rule stands for every case the test does not clear,
and the exception is conditional on a property that is verifiable and today verifies.

`decisions/DR-2026-07-23-population-schema-replace.md` (D-DOCT + D-SCHEMA, **DG-NON**) is the
operative population source. It **forbids** parent codes, slash sub-codes, and any umbrella that
contains its members. Its "Deferred / follow-up" list (lines 76-86) — caller sweep of retired codes,
`DROP COLUMN parent_code`, retiring `population_reclass`, axis mappings for
MOVE/ID/VES/LPA/TALL/BAR — remains **open**: `parent_code` is nulled but not dropped,
`population_reclass` is still present with 14 dangling rows, and of the six codes owed axis
mappings, VES/LPA/TALL/BAR received them while **ID and MOVE did not** (`SELECT population_code FROM
populations p WHERE NOT EXISTS(SELECT 1 FROM population_axis_map m WHERE
m.population_code=p.population_code)` → `['ALL','ID','MOVE']`; `ALL` is a licensed scope marker).

`decisions/DR-2026-07-24-lang-jur-map-roles.md` (**DG-NON**, RATIFIED, register D-0152) **forbids**
populating `lang_jur_map` from an armchair. Its binding precedent,
`DR-2026-06-11-remove-colonial-role`, withdrew a previous auto-population **as fabrication**. Every
row must carry a verifiable official-language basis in `notes`, and a jurisdiction whose authoring
language falls outside the 19 must carry `[PRIMARY-LANGUAGE-GAP]` — present today on exactly
`ZA, CY, ET, TH`.

Research contract **R11** (`governance/research-contract.yaml`, `status: OPERATIVE`, enforcer
`scripts/audit/research_batch_dod.py`) **forbids** generating a non-English alias by translating
from English: "No back-translation. Every alias carries its in-language source, else
`[UNVERIFIED-TERMS]`." Current state: 856 against a baseline of 856 in
`governance/research-contract-baseline.json` — reported as inherited debt, not as a regression.

**Doctrine conflicts to name at this stage.** `governance/population-taxonomy.md` still carries a
CANONICAL header and an 11-code slash-notation scheme, and `governance/functional-taxonomy.md` §4
(lines 272-316) reasons over the full retired set `VIS UPL OFS NEU DBL SENS CFS MCAS POTS PCS LCOV
OAD` while §1 (lines 117-137) uses 8 of those 12. Neither document carries a supersession banner and
functional-taxonomy is RATIFIED. **Operative is `schemas/enums.py PopulationCode` + DR-2026-07-23**,
stated explicitly at `references/project-standards.md:574`: "Treat `schemas/enums.py` PopulationCode
+ DR-2026-07-23 as the operative population source, not population-taxonomy.md's superseded body."
Separately, `functional-taxonomy.md` §7 asserts "`lang_jur_map` remains empty pending owner-defined
PRIMARY/SECONDARY criteria per DR-2026-06-11" — false since 2026-07-24 (70 rows, roles
`[('PRIMARY',50),('SECONDARY',20)]`). §7 is titled "what this document does NOT change" and its list
terminates "— until ratification", which frames it as a pre-ratification compatibility note and
softens the drift; it does not remove it, because the document is now RATIFIED and the sentence
still reads as a present-tense fact. DR-2026-07-24 supersedes it.

#### (h) ACCEPTANCE CONDITIONS — stage 1

*What makes a single new slug, axis, population, access-need, term or alias row admissible.* Levels
per the legend above; **4 is the ceiling** (no level-5 hook exists in this repo).

**Slug rows**

1. **`status ∈ {ACTIVE, MERGED, STUB, PROVISIONAL}`.** — Field: `slugs.status`. — Level **D**
   (`CHECK(status IN (…))`, enforced at write time by SQLite). — `schemas/slug.py` carries the same
   constraint as a Pydantic validator but is never invoked against DB rows, and `slugs` is not in
   `validate_pydantic_schemas`'s `MODEL_TABLE_MAP`.
2. **`merged_into` resolves to a live slug when `status='MERGED'`.** — Field: `slugs.merged_into`.
   — Level **D(fk)** (`REFERENCES slugs(slug)`; deferred differential check in `migrate_db.py`, new
   violations fail, pre-existing baseline grandfathered, bootstrap migrations exempt, reaching CI
   only via the blocking `migration_reproducibility`). The conditional — that it is *required* when
   MERGED — is **UNENFORCED**.
3. **The slug declares `serves_axes` with ≥1 axis code.** — Field: `slugs.serves_axes` (JSON text).
   — Level **UNENFORCED**. — Doctrine at `governance/functional-taxonomy.md:326` curation rule 3
   ("Slug discipline"); 1 of 106 rows populated; the only code reference is
   `schemas/slug.py:31` (`Optional`, never read). A second authoring surface exists in BPC front
   matter with no importer.
4. **Axis codes inside `serves_axes` resolve to live axes.** — Field: `slugs.serves_axes`. — Level
   **UNENFORCED**. — JSON text, no FK, no validator; `validate_axes` does not read the column.

**Axis rows**

5. **`coverage_status ∈ {ESTABLISHED, PARTIAL, STUB}` and is non-null.** — Field:
   `axes.coverage_status`. — Level **D** (`NOT NULL CHECK (…)`, migration 030).
6. **`falsification_condition` is non-null** — every axis states what would refute it. — Field:
   `axes.falsification_condition`. — Level **D** (`TEXT NOT NULL`). No registered check asserts
   non-emptiness or substantive content; a single space satisfies it.
7. **The axis is framed as an environmental demand, not a bodily deficit; ICF `b`-anchors serve
   findability only.** — Fields: `axes.mechanism`, `axes.icf_b_anchors`. — Level **1 text rule** —
   `governance/functional-taxonomy.md` §0 and §2. Unmechanisable as written; no enforcer.
8. **Every axis is reachable from at least one population and at least one item.** — Fields:
   `population_axis_map`, `item_axis_links`. — Level **3 CI non-blocking in effect** —
   `validate_axes` is registered **blocking**, but this specific finding is emitted as a *warning*
   that does not affect exit status: `WARN: 1 axes with zero population mappings: ['AX-COG-L']`,
   exit 0. Item-side coverage is complete (17/17).

**Population rows and their axis mappings**

9. **The code is one of the ratified 23 and matches `schemas/enums.py PopulationCode` in both
   directions.** — Field: `populations.population_code`. — Level **3 CI non-blocking** —
   `validate_population` P1, registered advisory (`P1 PASS: enum and populations table agree on 23
   codes`).
10. **`parent_code` is NULL — the set is flat (DR-2026-07-23).** — Field: `populations.parent_code`.
    — Level **UNENFORCED** — the column is nulled on all 23 rows but not dropped, and no check
    asserts NULL. The DR's own `DROP COLUMN parent_code` follow-up is still open.
11. **A new population names a specific self-identified community, not a broad umbrella** — unless
    it passes the three-part design-equivalence test (comorbidity/overlap; union of member axis
    signatures preserved; no opposed demand). — Field: conceptual; realised in `populations` +
    `population_axis_map`. — Level **1 text rule** (`references/project-standards.md` 557/563,
    `DR-2026-07-22-work-from-axes`) **plus partial 3** — `retired_vocabulary` (advisory, kinds
    `always`) catches RV-010 `physically disabled` and RV-011 `energy-limiting chronic illness` at
    `severity: doctrine`. **A newly-coined umbrella phrase is UNENFORCED**, because the audit
    patrols a fixed token list, not a shape.
12. **An umbrella exception preserves the union of its members' axis signatures.** — Field:
    `population_axis_map` rows for that code. — Level **1 text rule** — verified by hand at
    ratification and re-verified here against the DB for `COM` and `BRAIN`; **no script re-checks
    it**, so the exception's ratifying condition can silently lapse if a mapping is later removed.
13. **Every population maps to ≥1 axis — it is a vector, not a bucket.** — Field:
    `population_axis_map`. — Level **UNENFORCED** — `validate_axes` checks only the converse.
    `ALL`, `ID`, `MOVE` violate today; `ID` and `MOVE` are DR-2026-07-23's open follow-up.
14. **`population_axis_map.role ∈ {ALIAS, PRIMARY, SECONDARY, SITUATIONAL}`.** — Field:
    `population_axis_map.role`. — Level **D** (`NOT NULL CHECK`) **and 4 CI blocking** —
    `validate_axes` independently asserts the role vocabulary, so this is the one stage-1 condition
    with both a schema constraint and a real CI gate behind it.
15. **Both codes in a `population_axis_map` row resolve.** — Fields:
    `population_axis_map.population_code`, `.axis_code`. — Level **4 CI blocking** — `validate_axes`
    resolves them explicitly (not relying on the FK), backed by **D(fk)** at write time.
16. **The mapping carries a disclosed confidence grade (`functional-taxonomy.md` §3.2).** — Field:
    *no column exists*. — Level **UNENFORCED — DESIGNED-ONLY**. §3.2's stated "role for query
    weighting, confidence for disclosure" pair shipped only its first half.

**Access-need rows**

17. **`family ∈ {perceiving, communicating, operating, pacing, environment_safety}`.** — Field:
    `access_needs.family`. — Level **D** (`NOT NULL CHECK`).
18. **`typical_stakes ∈ {safety-critical, exclusion, friction}` when present.** — Field:
    `access_needs.typical_stakes`. — Level **D** for the vocabulary; **UNENFORCED** as a
    requirement — the column is nullable and 16 of 17 rows are NULL.
19. **The need reaches at least one axis, and the populations it serves are recorded in a queryable
    relation.** — Fields: `access_need_axis_map`; **for the population half, no column exists**. —
    Level **UNENFORCED** for both halves. `A-AT` and `A-TIME` reach no axis; and
    `references/project-standards.md:571` asserts LPA/TALL/BAR are "served by the A-SIZE access
    need" with no table in the schema able to hold that fact.

**Term and alias rows**

20. **`alias_type ∈ {SYNONYM, TRANSLATION, NARROWER, BROADER, DEPRECATED, DOMAIN}` and the row is
    unique on `(term_id, alias, language)`.** — Field: `term_aliases.alias_type`, PK. — Level **D**
    (`CHECK` + `PRIMARY KEY`, both enforced at write time by SQLite).
21. **`term_id` resolves to a live term.** — Field: `term_aliases.term_id`. — Level **D(fk)**
    (`REFERENCES terms(term_id)`; deferred differential check as described in the legend). No
    registered check re-resolves it.
22. **An alias created on or after 2026-07-24 carries a recognised provenance marker.** — Field:
    `term_aliases.notes` (substring match — there is no provenance column). — Level **4 CI
    blocking** — `alias_provenance_audit`, registry `level: blocking`, battery `data`. It passes
    today (`RESULTS: all post-2026-07-24 aliases carry provenance`) with the 880 pre-cutoff rows
    grandfathered and reported, not failed.
23. **No alias was produced by back-translation from English; otherwise it is flagged
    `[UNVERIFIED-TERMS]` (R11).** — Field: `term_aliases`. — Level **3** for detection
    (`research_dod` R11, advisory) **plus 4 for the ratchet** —
    `research_contract_baseline_ratchet` (blocking, kinds `always`) fails on any *rise* above the
    856 recorded in `governance/research-contract-baseline.json`. Detection of an individual bad
    alias is **UNENFORCED**; only the aggregate is held.
24. **`language` uses the same case and membership vocabulary as `lang_jur_map.language`.** — Field:
    `term_aliases.language`. — Level **UNENFORCED** — 15 lowercase values against 19 uppercase, no
    `languages` table, no `LanguageCode` enum. This is the condition whose failure makes
    `v_coverage_priority` and `search_executions` unjoinable in stage 3.

**Scope-map rows**

25. **`lang_jur_map.role ∈ {PRIMARY, SECONDARY}` and the row is unique on `(language,
    jurisdiction)`.** — Field: `lang_jur_map.role`, PK. — Level **D**.
26. **The role is grounded in a verifiable official-language fact recorded in `notes` — no
    armchair, no fabrication (DR-2026-07-24, precedent DR-2026-06-11).** — Field:
    `lang_jur_map.notes`. — Level **1 text rule**. No script reads `notes`. This is the condition a
    prior fabrication event was withdrawn over, and it is enforced by nothing.
27. **A jurisdiction whose primary authoring language falls outside the 19 carries
    `[PRIMARY-LANGUAGE-GAP]`.** — Field: `lang_jur_map.notes`. — Level **1 text rule** — present on
    `ZA, CY, ET, TH`; **UNENFORCED**.

**Meta-conditions on the change itself**

28. **The change ships as a forward-only migration and the DB rebuilds from migration history.** —
    Field: `scripts/migrations/`. — Level **4 CI blocking** — `migration_reproducibility`. Note its
    real reach: it compares `PRAGMA user_version` and `COUNT(*)` on six tables. **None of the
    stage-1 tables is among the six**, so a taxonomy `UPDATE` that preserves row counts passes it
    untouched. The full comparison is `migration_reproducibility_deep`, **advisory**.
29. **A schema change is mirrored in the matching Pydantic model.** — Fields: `schemas/*.py`. —
    Level **3 CI non-blocking** — `validate_pydantic_schemas`, advisory, currently failing with 246
    drift findings. **It covers no stage-1 vocabulary table**: `axes`, `access_needs`,
    `access_need_axis_map`, `access_need_icf`, `population_axis_map`, `terms`, `term_aliases`,
    `lang_jur_map` and `situations` are all absent from its 17-entry `MODEL_TABLE_MAP`. `slugs` and
    `populations` are mapped; `population.Population` shares zero fields with its table.
30. **The change is authorised by a DG-NON decision record.** — Field: `decisions/DR-*.md`. — Level
    **UNENFORCED for the data act**. `decision_capture` (blocking) validates DR *form*; nothing ties
    a taxonomy migration to a DR id, and `scripts/migrations/*.sql` has no field in which to record
    one.

---
---

### 2.2 Stage 2 — Scope & question framing

#### (a) Tools, tables, methodology

| Object | Rows | State | Note |
|---|---|---|---|
| `items` (categories A–K) | 93, all `status='active'` | **BUILT+EXERCISED** | `A19 B12 C6 D11 E14 F8 G9 H5 I4 K5` — no `J` rows, though `J` **is** in the DDL CHECK |
| `items.bpc_source_slug` | 87 non-null → **27 distinct slugs** | **BUILT+EXERCISED** | the *de facto* item↔slug bridge. 6 items carry none: `A-13 A-15 B-08 F-07 G-02 G-07` |
| `item_bpc_links` (mig. 013) | **0** | **BUILT+UNEXERCISED** | the *decreed* bridge; the reset deleted its 3 rows (`DELETE FROM item_bpc_links; -- 3 rows`, line 57) |
| `item_population_links` | 372 across **92** of 93 items | **BUILT+EXERCISED** | |
| `item_axis_links` (mig. 030) | 158 across **93 of 93** items | **BUILT+EXERCISED** | carries `strength_band ∈ {full,partial,weak}` and `use_mode ∈ {independent,assisted,collective}` |
| `term_item_links` | 147 across 69 items, 0 orphans | BUILT+EXERCISED | |
| `item_population_elaborations` | 3 | BUILT+UNEXERCISED | the reset pruned the evidence-bearing rows |
| `rooms` (mig. 042) | 17, all active | **BUILT+UNEXERCISED** | a 17-row island — see (f) |
| `room_items` (mig. 042) | **0** | **BUILT+UNEXERCISED** | never populated; **not** in the reset's DELETE list (`grep -c room_items` on the reset migration → 0) |
| `bpc_metadata` (carries `pico_complete`, `search_complete`, `bpc_complete`) | **0** | **BUILT+UNEXERCISED** | the reset deleted 83 rows |
| `v_coverage_priority` (mig. 035) | **7210** | **BUILT+EXERCISED as a view** | anatomy in (b) |
| `jurisdictional_values` | 109; `standard_name` and `source_section` both non-empty on **109/109** | **BUILT+EXERCISED** | retained by the reset on the R3 class-relative-locator argument (DR §3) |
| `weighting_profile` | 5 | BUILT (consumed at stage 12) | |

| Script / skill | Registered id · level | State |
|---|---|---|
| `scripts/validate_items.py` | `validate_items` · **advisory** (battery `data`) | **BUILT+EXERCISED** — `items validation: PASS (93 items, 372 population links across 92 items, all codes valid)`. Re-checks both junction FKs by hand rather than trusting SQLite's per-connection FK setting |
| `scripts/validate_item.py` | **quarantined** | — |
| `skills/question-author_SKILL.md` | not a registered check | **DESIGNED-ONLY / INOPERATIVE.** Its own banner: "every SQL statement below targets a table that does not exist … there is no `specification` table, and no column named `question_heading` anywhere in the database." Verified: `SELECT name FROM sqlite_master WHERE name='specification'` → `[]`, against 67 tables. `schemas/specification.py` still models it — a live Pydantic-model-without-a-table |
| `skills/item-specification-writer_SKILL.md` | — | carries the same `specification`-table banner |
| `scripts/generate/room_page.py` | — | **BUILT, CRASHES.** `python3 scripts/generate/room_page.py R-BA` → `sqlite3.OperationalError: no such table: room`. It queries `room` and `room_item`; the tables are `rooms` and `room_items` |
| `scripts/audit/table_connectivity.py` | **quarantined** (registry reason "NOT A GATE") | BUILT+EXERCISED — it measures the item↔slug seam and is the clearest instrument for it |
| `tools/pipeline_completeness.py` | `pipeline_completeness_fresh` · **blocking** (battery `render`) | BUILT+EXERCISED as a renderer; **its slug-denominated metrics are now vacuous** — see (f) |

#### (b) How they relate to each other — the internal wiring

Stage 2 attaches four different vocabularies to `items` and one view to `slugs`, and the two halves
do not meet.

The item-side attachments are all real and all FK-bound: `item_population_links` (372 rows,
`population_code → populations`, `item_code → items ON DELETE CASCADE`), `item_axis_links` (158
rows, both codes FK-bound, `PRIMARY KEY (item_code, axis_code)`), `term_item_links` (147 rows), and
`jurisdictional_values` (109 rows, bound to items but with `jurisdiction` as free text bound to
nothing). `room_items` would be the fifth and holds no rows.

**The item↔slug binding does not exist as designed.** `item_bpc_links` was decreed authoritative by
DR-2026-07-12 and migration 013, and by an owner directive recorded at
`references/bpc-reasoning/room-acoustic-performance.md:72` — "Option B — add `item_bpc_links` join
table; `items.bpc_source_slug` retained read-only … until all 91 items migrated, then deprecated".
It holds **0 rows**. Every consumer therefore reads the deprecated single-valued column:
`scripts/generate_search_queries.py` resolves items with `SELECT item_code FROM items WHERE
bpc_source_slug = ?` and falls back to token-matching the slug string when that returns nothing.
The fallback is not hypothetical — running the generator prints it:

```
$ python3 scripts/generate_search_queries.py corridor-clear-width
No items linked to slug 'corridor-clear-width'. Using slug name as concept basis.
```

That happens for **79 of 106 slugs** (`SELECT COUNT(*) FROM slugs s WHERE NOT EXISTS (SELECT 1 FROM
items i WHERE i.bpc_source_slug = s.slug)` → 79). Migration 013 did ship one constraint: a partial
unique index, `CREATE UNIQUE INDEX idx_ibl_primary_per_item ON item_bpc_links(item_code) WHERE
link_type = 'primary'`. That is a **cardinality ceiling** — at most one primary per item. The
**floor** the same owner directive promised at line 76 ("CI structure check extended to verify every
ACTIVE item has ≥1 link with `link_type='primary'`") was never built.

**What that costs the coverage grid.** The grid's rows are `(slug × jurisdiction × language)`. Items
never enter it. So the coverage grid is *slug*-shaped while the evidence cell is
*(item × population)*-shaped — research contract R4 states "Cells are (item x population)" — and the
only bridge between the two shapes is a single-valued legacy column covering 27 of 103 in-scope
slugs. The quarantined `table_connectivity.py` measures exactly this seam:

```
   1 topic                     80/80        80/80
!! 6 has a spec                 0/80        27/80     ← the independent 27 = the bpc_source_slug distinct count
!! 8 BEST PRACTICE              0/80         0/80
the two halves of the pipeline are populated but do not meet on the same topic.
```

**`v_coverage_priority` — what its 7210 rows actually are.** Read from `sqlite_master` and from
`scripts/migrations/035_coverage_priority_view.sql`, the view is an unqualified `JOIN` with no `ON`
clause — a deliberate CROSS JOIN, annotated as such in the DDL — between the in-scope slugs
(`WHERE s.status IN ('ACTIVE','STUB')`, i.e. 80 + 23 = 103) and the 70 rows of `lang_jur_map`,
filtered by `NOT EXISTS (SELECT 1 FROM search_executions se WHERE se.slug = s.slug AND
se.jurisdiction = ljm.jurisdiction AND se.language = ljm.language)`.

`103 × 70 = 7210`. Since `search_executions` is empty, **the filter removes nothing and the view is
currently the entire Cartesian product** — not a prioritised subset but the complete undone
universe. The score distribution confirms it: `SELECT priority_score, COUNT(*) FROM
v_coverage_priority GROUP BY 1` → `[(3, 2060), (5, 5150)]`, i.e. `50 PRIMARY × 103 = 5150` and
`20 SECONDARY × 103 = 2060`, every row carrying the same `+2` slug-starvation bonus. Two distinct
priorities across 7210 rows: as a queue it is currently undifferentiated, ordering PRIMARY before
SECONDARY and nothing else. The DDL says why — the open-gap and branch-thinness bonuses "are omitted
here because `gaps` has no slug FK (linkage is free-text)".

**PICO.** There is no PICO table, no PICO column, and no PICO validator. `bpc_metadata.pico_complete`
is a self-asserted `0/1` flag settable by `python3 scripts/db.py update-bpc --pico-complete {0,1}`.
`scripts/validate_bpc.py:28-31` lists `PICO` among "Pre-CO-0006 schema … optional enrichment in
CO-0006 files and should not be validated as mandatory"; its `MANDATORY_SECTIONS` is only
`["## Key sources", "## Metadata"]`. The three consumers of `pico_complete` are a legacy migrator,
the `db.py` setter, and `tools/pipeline_completeness.py`, which renders it as a dashboard number.
**Nothing checks that a slug claiming `pico_complete=1` contains any PICO text.**

#### (c) Relation to stage 1 — the entry contract

| Requirement on the taxonomy before an item may be scoped | Enforcer | Level |
|---|---|---|
| `item_population_links.item_code` and `.population_code` both resolve | `test_db_integrity` **A02**/**A03** (`RESULTS: 70/70`); re-checked by `validate_items` V5 | **4** + **3** |
| `item_axis_links.axis_code` resolves | `validate_axes` | **4** |
| `items.bpc_source_slug` resolves to a live slug | declared FK, 0 violations verified; **no named check asserts it** — the A-series has no entry for it | **D(fk)** only |
| `term_item_links` both FKs resolve | nothing | **UNENFORCED** (0 orphans verified by hand) |
| Item scoping proceeds *from the axes*, not from population umbrellas (R4, RULE 2026-07-22) | nothing at item level | **UNENFORCED** |
| Every ACTIVE item carries ≥1 `item_bpc_links` row with `link_type='primary'` | **never built** — the promised CI check does not exist; the only index that shipped is the *ceiling* `idx_ibl_primary_per_item` | **UNENFORCED**; 0 of 93 items satisfy it |

#### (d) Relation to stage 3 — the exit / handoff contract

| Requirement | Enforcer | Level |
|---|---|---|
| A search's `slug` resolves to a live slug | `search_executions.slug REFERENCES slugs(slug)` on a STRICT table | **D(fk)** |
| The searchable set is `slugs WHERE status IN ('ACTIVE','STUB')` | the `v_coverage_priority` definition *is* the contract | **UNENFORCED on write** — a `MERGED` slug satisfies the FK and nothing rejects it |
| A cell is *required* iff `(language, jurisdiction) ∈ lang_jur_map` | the same view definition (DR-2026-07-24: "This is the bridge the empty table currently denies the priority queue") | **UNENFORCED on write** — `db.py log-search` accepts any `--language` / `--jurisdiction` string with no membership check |
| The item↔slug bridge is populated, so a search result can reach a cell | nothing | **UNENFORCED.** `working/pilot/PILOT-MANIFEST.md:39` records routing around it — "`item_bpc_links` … is populated for 1 of 92 items … The slug→item mapping below is therefore manual, pilot-cells-only" — and GAP-297 records a cell forced to `pending` purely because sibling-slug evidence was "unreachable at cell grain until `item_bpc_links` is backfilled" |
| PICO framed before searching | `bpc_metadata.pico_complete`, self-asserted; `pipeline_completeness` reports it, gates only on dashboard freshness | **1 text rule** — `literature-review-planner` ("PICO sequence (mandatory)"), `multilingual-research` §PICO Framing |
| `bpc_metadata.search_complete` reflects reality | nothing; 0 rows | **UNENFORCED** |

#### (e) The goal of the stage

Stage 2 turns a taxonomy into an **answerable question set**. Working in the doctrinal order —
from the demand layer outward, never from a population umbrella inward — it must decide (i) which
design parameters (`items`, A–K) the guidebook will specify at all; (ii) for each item, which
functional demands it acts on and how strongly (`item_axis_links`, carrying `strength_band` and
`use_mode`), and only then which populations it applies to and in what manner
(`item_population_links.applicability ∈ applies / applies_strictly / applies_loosely /
context_dependent / does_not_apply`); (iii) which research topic (`slug`) owns the evidence for it;
(iv) which spatial contexts it appears in (`rooms` / `room_items`); and (v) for each topic, the
**PICO frame** that fixes what would count as an answer *before* anything is searched — the
doctrinal point being that the question must precede the standard value rather than be
reverse-engineered from it. The stage's output is the **coverage grid**: the enumerated set of cells
that research owes an answer to, so that "not searched" stays distinguishable from "searched,
nothing found". That distinction is what the entire downstream apparatus rests on, and it is
manufactured here, in the denominator.

#### (f) How the tools support that goal — and where they do not

**Where they support it.** `item_axis_links` is complete — 93 of 93 items — and carries real
methodological content rather than a bare edge: `strength_band ∈ {full, partial, weak}` and
`use_mode ∈ {independent, assisted, collective}`, the latter directly executing
`functional-taxonomy.md` §5.5 ("the solo-user default is a disclosed bias, not a frame"). That the
axis binding is complete while the slug binding is empty is itself the stage's most important
signal about which layer the project actually built. `item_population_links.applicability` has a
five-value vocabulary that includes `does_not_apply`, so scope can record a *negative determination*
rather than an absence — a distinction most schemas lose. `v_coverage_priority` closed a real
executability gap: migration 035's header records that the coverage loop "said 'pop the highest-value
required cells from the priority queue' but no such artifact existed (adversarial review 2026-07-24,
finding C1)". And the `lang_jur_map` bridge means the denominator is *required* cells rather than
`19 × 48`; DR-2026-07-24 argues the point explicitly — treating all pairs as required "inflates the
denominator with cells that are genuinely not-applicable (searching Korean sources for a Moroccan
code)".

**Where they do not.**

*The question-framing half of the stage is inoperative.* The skill named for it, `question-author`,
targets a table that does not exist, by its own banner. PICO has no home in the schema.
`schemas/specification.py` models the missing table, which per CLAUDE.md §10 is "a bug, not a
convention". So "scope & question framing" reduces in practice to scope.

*The item↔slug bridge is the single largest structural hole in stages 1–3.* The decreed mechanism
holds 0 rows; the deprecated column it replaced covers 27 of 103 in-scope slugs; and the coverage
grid is slug-shaped while the evidence cell is item×population-shaped. The consequence is not
abstract: a search can be "complete" for a slug that reaches no item, and an item can be starved by
a slug boundary rather than by an evidence absence, which is precisely what GAP-297 records.

*The dashboard that reports this stage now reads complete-by-vacuity, and it is gated blocking.*
`tools/pipeline_completeness.py:75` derives its slug denominator as `SELECT COUNT(*) FROM
bpc_metadata` — a table the clean-room reset emptied. Every slug-denominated metric in the committed
dashboard therefore reads `0 / 0 · 0%`: "Slugs with search complete", "Slugs with a logged search",
"PICO formalized", "Gaps closed", "Sources verified", "Metadata complete", "Citation-mining complete
(slugs)", "Slugs with a reasoning doc". The dashboard can no longer express "106 topics exist and
none has a PICO"; it says the pipeline is 0-of-0. The contrast is diagnostic, because metrics keyed
to *surviving frame* tables still read honestly on the same page — `0 / 372` cells, `0 / 93` items,
`0 / 87` live item-facing syntheses, `0 / 3840` slug × jurisdiction cells. `pipeline_completeness_fresh`
is registered **blocking** and gates the dashboard's freshness, not the truth of its denominators.

*`rooms` is a 17-row island.* `room_items` has never held a row — it is absent from the reset
migration entirely — and the generator meant to consume it crashes on a table-name mismatch
(`room` vs `rooms`, `room_item` vs `room_items`). `schemas/room.py` models a third shape again
(`room_id`, `design_stage`, `must_appear_on`) and is not in `validate_pydantic_schemas`'s
`MODEL_TABLE_MAP`, so nothing compares any two of the three.

*`jurisdictional_values` is bound to items but to no jurisdiction vocabulary.* It writes `GB` (20
rows) where `lang_jur_map` writes `UK`; the enum has 27 codes; `validate_jurisdiction` is registered
**blocking**, warns 38 times about codes "not in canonical 24", and exits 0.

*The coverage grid cannot express partial coverage.* A cell appears in `v_coverage_priority` iff it
has *no* `search_executions` row at all. One logged scoping search in one language removes the cell
from the queue entirely, regardless of `depth_method`, `saturation_signal`, or whether the search
was deferred. The asymmetry is visible in the view body itself: the `NOT EXISTS` predicate filters
on `(slug, jurisdiction, language)` only, while the view's own `slug_searches` column filters
`deferred_reason IS NULL`. So a **deferred** search — one deliberately not run — removes a cell from
the queue while not counting as a search anywhere else.

#### (g) How doctrine conditions the stage — what it FORBIDS

**Mission commitment 1** — specifications serve questions — **forbids** an item whose scope is
asserted without a question it answers. That is why `question_heading` exists as a concept at all,
and it is why the absence of a `specification` table and of any PICO column is a *doctrinal* failure
rather than a tooling inconvenience.

**Mission commitment 5** — "Universal design is co-extensive with code compliance — the floor, not
an aspiration" — **forbids** scoping an item at the code floor and calling the result best practice.
`governance/tier-system.md` §3 ("Best-practice ≠ convergence") makes it operative at this stage:
T4–T6 are the regulatory stratum and code convergence is **not evidence**.

**Mission commitment 6**, with `governance/audience-priority.md`, requires the project's distinctive
epistemic claim to be "acknowledged as a claim, not asserted as established" — which **forbids**
scoping an item so that a contested position is framed as settled.

**`governance/evidence-architecture.md` §3–§4** conditions scope through the three Design Modes and
through directness. The mode × stratum matrix transcribed at `evidence-architecture.md:189`
**forbids** code-class evidence from anchoring at population or person scale
(`code × population NON-ANCHORING`, `code × person NON-ANCHORING`). Checked by
`scripts/audit/matrix_consistency.py` (`matrix_consistency`, **advisory**).

**Research contract R4** (`while-searching`) — "Cross slug x population / access-need / ICF / axis.
Cells are (item x population)" — **forbids** treating a slug-level search as satisfying a cell. This
is the rule the empty `item_bpc_links` makes unsatisfiable in practice. Its enforcer,
`research_batch_dod` R4, currently prints `PASS — 0 population linkages produced across 0 searches`.

**Research contract R12** — "Code values -> jurisdictional_values. Never leave them in prose notes"
— **forbids** scoping a jurisdictional value into a markdown note instead of the table.

**`DR-2026-07-21-entity-code-namespace-rename`** **forbids** conflating item codes `A-01…K-NN` with
entity-type codes `ENT-01…ENT-20`; the rename exists specifically to end that collision (`ENT-08` is
the *Item* entity type; `E-08` is the *Corridor Clear Width* parameter).
**`DR-2026-07-12-website-architecture-lock`** governs the `/rooms/` URL family that `rooms` serves,
which is why the empty `room_items` is a published-surface commitment and not only an internal gap.

**`DR-2026-07-22-work-from-axes` and `references/project-standards.md` RULE 2026-07-22 bind this
stage's ordering.** Item scope is derived from the axis layer; a population link is a consequence of
an axis relation, not a starting point. The stage's own data reflects the doctrine better than its
tooling does — 93/93 items axis-linked against 92/93 population-linked — but nothing enforces the
direction of derivation, and an item scoped umbrella-first would be indistinguishable in the DB from
one scoped axis-first.

#### (h) ACCEPTANCE CONDITIONS — stage 2

*What makes a single item, scope link or coverage cell admissible.*

1. **`item_code` matches `[A-K]-NN` and `category` is one of the eleven letters.** — Fields:
   `items.item_code`, `items.category`. — Level **D** for `category` (`NOT NULL CHECK(category IN
   ('A'…'K'))`) — and note that **`'J'` is in the CHECK**: J is struck by convention, not by
   constraint, so a J-category item would be admitted by the schema. The `[A-K]-NN` *pattern* is
   asserted only in `schemas/item.py` / `schemas/room.py` validators, which never see DB rows ⇒
   **UNENFORCED** on the table.
2. **`status ∈ {draft, active, merged, retired}`.** — Field: `items.status`. — Level **D**
   (`NOT NULL DEFAULT 'draft' CHECK`).
3. **The item links to ≥1 axis.** — Field: `item_axis_links`. — Level **UNENFORCED** as a floor.
   93/93 satisfy it today; nothing fails on the 94th.
4. **`item_axis_links.axis_code` resolves and `strength_band ∈ {full, partial, weak}`,
   `use_mode ∈ {independent, assisted, collective}` when present.** — Fields:
   `item_axis_links.axis_code`, `.strength_band`, `.use_mode`. — Level **4 CI blocking** for code
   resolution (`validate_axes`); **D** for both vocabularies (`CHECK`). Both value columns are
   nullable, so an axis link need not state how strong it is or in what use mode.
5. **The item links to ≥1 population.** — Field: `item_population_links`. — Level **UNENFORCED** —
   92 of 93 items are linked; nothing fails on the 93rd.
6. **Both FKs on a population link resolve.** — Fields: `item_population_links.item_code`,
   `.population_code`. — Level **4 CI blocking** — `test_db_integrity` A02/A03, re-checked by
   `validate_items` V5 (**3**), over **D(fk)** at write time.
7. **`applicability ∈ {applies, applies_strictly, applies_loosely, context_dependent,
   does_not_apply}`.** — Field: `item_population_links.applicability`. — Level **D**
   (`NOT NULL DEFAULT 'applies' CHECK`). `validate_items` deliberately does *not* re-check it; the
   registry note records why — "the schema's CHECK constraint owns it, and a fault-injection run
   caught the first draft re-transcribing it two values too narrow". That is the correct division of
   labour, and it is the clearest statement in the repo that D is a real level.
8. **The item binds to ≥1 slug via `item_bpc_links`, exactly one of which is
   `link_type='primary'`.** — Field: `item_bpc_links`. — Level: **ceiling only.** The *at most one*
   half is **D** (`CREATE UNIQUE INDEX idx_ibl_primary_per_item … WHERE link_type = 'primary'`). The
   **≥1 floor is UNENFORCED**, the promised CI check was never built, and **0 of 93 items satisfy
   it**. `link_type ∈ {primary, parameter, context, secondary}` is **D**.
9. **`items.bpc_source_slug` resolves to a live slug.** — Field: `items.bpc_source_slug`. — Level
   **D(fk)** only; no registered check asserts it, and the A-series has no entry for it.
10. **The item appears in ≥1 room.** — Field: `room_items`. — Level **UNENFORCED** — 0 rows, and the
    generator that would consume them crashes.
11. **The slug has a PICO frame before search begins.** — Field: `bpc_metadata.pico_complete`
    (self-asserted `0/1`). — Level **1 text rule** — `literature-review-planner` ("PICO sequence
    (mandatory)"), `multilingual-research` §PICO Framing. `validate_bpc.py:28-31` explicitly demotes
    the `PICO` section to "optional enrichment … should not be validated as mandatory", and
    `MANDATORY_SECTIONS` is only `["## Key sources", "## Metadata"]`. **Content is UNENFORCED**:
    nothing checks that a slug claiming `pico_complete=1` contains any PICO text.
12. **The question heading is yes/no-answerable from site inspection and references lived
    experience.** — Field: *no column exists*. — Level **1 text rule** — `question-author_SKILL.md`
    §1, whose §2–§4 SQL targets a table that does not exist. **DESIGNED-ONLY.**
13. **A coverage cell is *required* iff slug `status ∈ {ACTIVE, STUB}` and `(language, jurisdiction)
    ∈ lang_jur_map`.** — Field: `v_coverage_priority` (derived). — Level **2 audit** — the view
    *defines* requiredness and is the only artifact that does; nothing rejects a search logged
    outside it, and nothing rejects a search against a `MERGED` slug.
14. **A jurisdictional value carries `standard_name` and `source_section` (R3, class-relative
    locator).** — Field: `jurisdictional_values.standard_name`, `.source_section`. — Level
    **UNENFORCED (1 text rule only)**. The condition holds today — 109 of 109 rows have both
    non-empty — but **nothing checks it**. `research_batch_dod` R3 reads
    `SELECT ref_id FROM evidence_sources WHERE tier >= 4 AND …` (line ~320) and never queries
    `jurisdictional_values` at all; `grep -n jurisdictional_values scripts/audit/research_batch_dod.py`
    returns two comment strings and no query. Its `R3: PASS — all regulatory sources clause-cited or
    flagged [UNVERIFIED-QUANT]` is a pass over `evidence_sources`, which has 0 rows. This is the one
    place in stages 1–3 where a protection is claimed that does not exist anywhere.
15. **The jurisdiction code is drawn from a single canonical vocabulary.** — Field:
    `jurisdictional_values.jurisdiction`. — Level **UNENFORCED** — no canonical table; `GB` and `UK`
    live in different tables for the same jurisdiction; `validate_jurisdiction` (blocking) warns 55
    times and exits 0.
16. **Item scope is derived from the axis layer, not from a population umbrella.** — Field:
    conceptual; realised as the relative ordering of `item_axis_links` and `item_population_links`.
    — Level **1 text rule** — `references/project-standards.md` RULE 2026-07-22 and
    `DR-2026-07-22-work-from-axes`. Direction of derivation leaves no trace in the schema, so this
    is **UNENFORCED** and structurally unenforceable as the tables stand.
17. **The change ships as a forward migration and the DB rebuilds from migration history.** —
    Field: `scripts/migrations/`. — Level **4 CI blocking** — `migration_reproducibility`, with the
    same caveat as stage 1 #28: it compares `PRAGMA user_version` plus `COUNT(*)` on six tables, so
    an `UPDATE` to `item_population_links.applicability` passes it untouched. The full comparison is
    `migration_reproducibility_deep`, **advisory**.

---
---

### 2.3 Stage 3 — Search execution

#### (a) Tools, tables, methodology

| Object | Rows | State |
|---|---|---|
| `search_executions` (mig. 033, **STRICT**) | **0** (held 84; reset line 73) | **BUILT+UNEXERCISED** |
| `search_admissions` (mig. 050) | **0** (held 39) | BUILT+UNEXERCISED |
| `search_candidates` (mig. 036, STRICT) | **0** (held 18) | BUILT+UNEXERCISED |
| `search_coverage` (legacy grid) | **0** (held 4960) | **FROZEN** — the write path raises `FrozenGridError` |
| `search_languages` (legacy grid) | **0** (held 1558) | **FROZEN** — same |
| `v_coverage_jurisdiction` / `v_coverage_language` / `v_coverage_branch` | 0 / 0 / 0 | BUILT+UNEXERCISED — all derive from an empty log |
| `v_coverage_priority` | 7210 | BUILT+EXERCISED |
| `lang_jur_map` | 70 | BUILT+EXERCISED |
| `citation_mining`, `gap_mining` | 0 / 0 | stage 6 |

| Script / skill | Registered id · level | State |
|---|---|---|
| `scripts/db.py log-search` (`log_search()`, line 328) | not itself a check | **BUILT+UNEXERCISED post-reset**, and the **only** live write path. It refuses **H07** (a repeated id inside one edge array) and **H05** (`results_admitted` disagreeing with the edge count) **at write time**, with a named cause; writes `admitted_ref_ids` JSON and the `search_admissions` junction in one transaction; and names a missing `ref_id` rather than raising a bare FK error. Its own comment states the principle: "A gate that catches a bad write after it lands is strictly worse than a write path that cannot make it." |
| `scripts/db.py upsert-coverage` / `upsert-language` | — | **BUILT, deliberately fatal.** `FrozenGridError` (`db.py:251`, raised at 319 and 325) with a message printing the `log-search` replacement command |
| `scripts/generate_search_queries.py` | not registered | **BUILT+EXERCISED, with a silent defect.** `python3 scripts/generate_search_queries.py corridor-clear-width --adversarial --harm` emits JSON for **14** languages (`da de en es fi fr it ja ko nl no pt sv zh`) with standard / adversarial / harm queries and a `harm_suffix_available` flag. `id` (Indonesian) is **silently dropped** — see (f) |
| `skills/multilingual-research_SKILL.md` | — | **BUILT+UNEXERCISED** — 584 lines; 19 languages × 46 jurisdictions; Step 1 = Co-1 / T2 / Co-2 "first; no exceptions"; per-jurisdiction Co-2 OT-body target tables |
| `skills/literature-review-planner_SKILL.md` | — | **BUILT, with a doctrinally wrong tier ladder** — see (g) |
| `skills/adversarial-research_SKILL.md` | declares enforcement "Level 2 (`scripts/audit/research_protocol_audit.py`)" | **BUILT+UNEXERCISED** — the audit prints `TOTAL ISSUES: 0` across 9 checks, every one over an empty subject |
| `skills/research-log-manager_SKILL.md` | — | CHECK-before / LOG-after protocol; "Skipping either is an error" |
| `scripts/audit/research_batch_dod.py` | `research_dod` **advisory** · `research_dod_selftest` **blocking** · `research_contract_baseline_ratchet` **blocking** (kinds `always`) | **BUILT+EXERCISED.** `--all` today: **13 of 15 rules PASS on zero subjects**, R11 reports 856 against baseline 856, **R1 FAILS honestly**, exit 0 |
| `scripts/generate/research_contract_hook.py --check` | `research_contract_sync` · **blocking**, `min_items: 10` | BUILT+EXERCISED, green, and **non-vacuous**: it prints `EXAMINED: 51 contract line(s)`. Generates the SessionStart hook in `.claude/settings.json` from `governance/research-contract.yaml`, the single source since DR-2026-08-01 |
| `scripts/audit/citation_mining_completeness.py` | `citation_mining_session` · **blocking**, `session_pointer: LATEST-RESEARCH` | **BUILT+UNEXERCISED in effect** — a blocking check exiting 0 having examined nothing; see (f) |
| `schemas/search_execution.py` | — | BUILT; **absent from `validate_pydantic_schemas`'s 17-entry `MODEL_TABLE_MAP`**, so nothing compares it to the table DR-2026-07-24 shipped it to mirror |

#### (b) How they relate to each other — the internal wiring

The stage has three parts that should form a loop and do not: a contract generator that feeds the
session, a query generator that feeds the human, and a logger that feeds the DB. Only the first is
mechanically closed.

`governance/research-contract.yaml` is the single source for R1–R15. `scripts/generate/research_contract_hook.py`
renders it into the `.claude/settings.json` SessionStart hook, and `research_contract_sync`
(**blocking**, `min_items: 10`) fails if the two drift. The same YAML drives the rule table in
`scripts/audit/research_batch_dod.py`. This is the highest-leverage drift surface in the repo and it
is genuinely held: the check prints an `EXAMINED:` count, so its `min_items` guard is live rather
than declarative.

`scripts/generate_search_queries.py` reads `term_aliases`, resolves items through
`items.bpc_source_slug` (falling back to slug-token matching, which fires for 79 of 106 slugs), and
emits `{standard, adversarial, harm}` query text per language. A human then runs the query.
`db.py log-search` writes the result into `search_executions` and, in the same transaction, the
`search_admissions` junction and the `admitted_ref_ids` JSON array — the two representations that
`test_db_integrity` H03/H04 hold equal in both directions. From `search_executions`,
`v_coverage_jurisdiction` / `_language` / `_branch` derive coverage, and its *absence* drives
`v_coverage_priority`.

**Four wiring facts determine what this stage can and cannot prove.**

*Coverage is derived, never hand-written.* That is the substance of DR-2026-07-24
(search-executions-substrate) and of `FrozenGridError`. The DR's diagnosis of the state it replaced:
"Coverage is two hand-maintained placeholder grids … joined by nothing … No table records what was
searched. A cell reading `SEARCHED` today cannot prove what was searched."

*The query generator and the logger do not touch each other.* `search_executions.terms_used` is a
JSON array of term ids, and `db.py log-search --terms-used`'s own help text says it "is 0%
populated today, so no logged search can yet show which terms it used". There is no
`--from-generator` path and no check that `query_text` contains any alias from `term_aliases`. So
the one column that would tie a logged search back to the controlled vocabulary is unpopulated **by
design of the workflow**, not by the reset.

*The `(slug, jurisdiction, language)` join between `search_executions` and `v_coverage_priority` is
a bare text comparison with no normalisation on either side.* `log_search()` passes `language` and
`jurisdiction` straight into the INSERT; the STRICT table has no CHECK on either; the CLI help says
"ISO 639-1, uppercase (EN, FR)" and enforces nothing. A search logged as `de`/`gb` leaves the
`(DE, DE)` and `(EN, UK)` cells sitting in the priority queue forever and creates a phantom language
in `v_coverage_language`. The precedent that this hazard is live rather than theoretical is in the
generator's own history: the identical case mismatch made `--adversarial` inert for its entire
existence until the 2026-07-24 fix.

*`search_candidates` is the off-slug spillover route R7 requires*
(`REHOME / MISCELLANEOUS / PENDING-VERIFICATION / OUT-OF-SCOPE / ADMITTED`), and its `exec_id` FK is
**nullable** (`notnull=0`), so a candidate can exist with no search that found it.

#### (c) Relation to stage 2 — the entry contract

| Requirement | Enforcer | Level |
|---|---|---|
| `slug` exists | `search_executions.slug REFERENCES slugs(slug)` on a STRICT table | **D(fk)** |
| The slug is in scope (`ACTIVE` / `STUB`) | nothing — a `MERGED` slug satisfies the FK | **UNENFORCED** |
| `(language, jurisdiction)` is a required cell per `lang_jur_map` | nothing — no CHECK, no FK, no CLI validation | **UNENFORCED** |
| `language` is one of the 19 research languages | nothing — bare `TEXT` in a STRICT table; the schema comment "ISO; one of the 19 research languages" is a comment | **UNENFORCED** |
| PICO framed first — "Begin with population need and functional outcome (optimal first) — not standard values" | `multilingual-research` §PICO Framing; `literature-review-planner` "PICO sequence (mandatory)"; `bpc_metadata.pico_complete` self-asserted and 0 rows | **1 text rule** |
| `research-log-manager` CHECK run before the search | skill front matter: "Skipping either is an error" | **1 text rule** |
| Vocabulary exists in the target language | `alias_provenance_audit` names AR/BN/HI/SW as unsearchable and exits 0 | **4, non-failing on this condition** |

#### (d) Relation to stage 4 (screening & admission) — the exit contract

| Requirement | Enforcer | Level |
|---|---|---|
| Query text logged verbatim, before screening (R8) | presence: `query_text TEXT NOT NULL` on a STRICT table; `research_dod` R8 | **D** for presence + **3** for the rule (`R8: PASS — 0 zero-yield searches retained; log intact (no deleted rows)` — vacuous today) |
| `results_admitted` equals the admission-edge count | write-time refusal in `log_search()` (invariant H05) **and** `test_db_integrity` **H05** | write-path refusal + **4 CI blocking** (vacuous today: 0 rows) |
| `admitted_ref_ids` JSON and the `search_admissions` junction agree both ways | `test_db_integrity` **H03/H04** | **4 CI blocking** (vacuous today) |
| No id repeats inside one edge array | write-time refusal (H07) + `test_db_integrity` **H07** | write-path refusal + **4** (vacuous today) |
| Every `search_admissions.ref_id` resolves to a real source | `log_search()` names the missing id at write time; `test_db_integrity` **A12/A13** | write-path refusal + **4** (vacuous today) |
| Findings never smuggled into `deferred_reason` (R6) | `research_dod` R6 | **3** (vacuous) |
| A zero-yield search records *why* — query shape vs wrong index vs genuine absence (R14) | `search_executions.findings_note`; `research_dod` R14 | **3** (vacuous) |
| Empties and deferrals never deleted or backfilled (R8) | `search_executions.backfill`; `research_dod` R8 asserts "log intact (no deleted rows)" | **3** — and the clean-room reset deleted all 84 rows by owner decision, the licensed exception |
| Off-slug / unverified material routed to `search_candidates`, not prose (R7) | `research_dod` R7 | **3** (`PASS — 0 candidates for 0 screened; 0 harm/failure flagged`) |

#### (e) The goal of the stage

Stage 3 is where the project's central epistemic distinction is manufactured: **the difference
between "we looked and found nothing" and "we never looked."** A search is a completed unit of work
whether or not it yields a source, and a search deliberately *not* run is also a unit of work, with
its reason recorded in `deferred_reason`. The stage must therefore (i) execute retrieval across the
required `(slug × jurisdiction × language)` cells in native-language conceptual vocabulary, with the
Co-1 / T2 / Co-2 pass first and without exceptions; (ii) interrogate on **two separate adversarial
axes** — is the evidence weak (`--adversarial`), and does the provision *harm* somebody (`--harm`);
and (iii) log every query **verbatim and before screening**, with its engine, depth, target
hierarchy branch and yield, so that coverage can be *derived* rather than asserted and any future
session can replay the search instead of repeating it blind. The output is an auditable, resumable
memory of the search frontier, plus the admission edge (`search_admissions`) that lets any admitted
source be walked back to the exact query that found it.

#### (f) How the tools support that goal — and where they do not

**Where they support it.** `search_executions` is the best-designed table in the stage-1–3 surface:
`STRICT`, with `CHECK`s on every closed vocabulary, `json_valid()` on both JSON columns, an explicit
`executed_at` for rebuild determinism, `deferred_reason` making an honest non-search a first-class
counted outcome, and `backfill` isolating reconstruction from contemporaneous logging. Refusals live
**at the write path** rather than only in a gate — `log_search()` rejects H05 and H07 violations
before the row lands, and names the cause. The frozen legacy grids are frozen *loudly*:
`FrozenGridError` prints the replacement command instead of failing silently or, worse, succeeding.
The harm axis is real and separate — `HARM_SUFFIXES` is deliberately not a synonym set of
`ADVERSARIAL_SUFFIXES` ("those question the source, these question the outcome") — and the generator
flags its own limits (`TRANSLATION STATUS: first pass, EN-anchored … flagged, not silently trusted`)
and emits `harm_suffix_available` per language. And the research contract is *generated* into the
SessionStart hook from one YAML, gated by a blocking sync check whose vacuity guard is live and
verified (`EXAMINED: 51 contract line(s)`).

**Where they do not.**

*Thirteen of fifteen contract rules currently pass by examining nothing.* Verbatim from
`python3 scripts/audit/research_batch_dod.py --all`: `R2: PASS — 0 citation_mining rows for 0
anchors`, `R4: PASS — 0 population linkages produced across 0 searches`, `R7: PASS — 0 candidates
for 0 screened; 0 harm/failure flagged`, `R8: PASS — 0 zero-yield searches retained`,
`R13: PASS — all 0 tier-1..3 admissions carry a graded population match`. R1 is the only rule that
fails, and it fails because it tests for the *presence* of a Co-1 pass rather than a ratio — the
shape that survives an empty corpus. R3 is worth singling out because it is the rule most easily
mistaken for live: it reads `SELECT ref_id FROM evidence_sources WHERE tier >= 4 AND …` and never
touches `jurisdictional_values`, so its pass is over 0 rows, not over the 109 populated ones.
CLAUDE.md §10 names this failure mode — "A gate reporting zero may have examined zero" — and records
that the repo has produced it four times.

*The remedy here is not a `min_items` floor, and the reason matters.* `research_dod` carries no
`min_items` key, and adding one today would **hard-fail it**: `scripts/run_checks.py:274-300`
(`vacuity_failure`) requires a declaring check to print a line matching `^\s*EXAMINED:\s*(\d+)`, and
treats its absence as the failure — "an unverifiable count cannot be trusted to be non-zero".
`python3 scripts/audit/research_batch_dod.py --all | grep -c EXAMINED` → **0**. So the first,
unconditional fix is that `research_batch_dod` should emit an `EXAMINED:` count per rule; that
stands on its own merits and blocks nothing. The *floor* is a different question, and the repo has
already adjudicated it: on 2026-08-06 a floor added to a subject that was empty **by ratified
decision** was retired, because a floor on a declared-empty subject makes a blocking gate red for
telling the truth. `search_executions` and `evidence_sources` are empty by
`DR-2026-08-06-clean-room-evidence-reset`, which is precisely that case. The correct instrument is a
**warranted, self-lifting suppression** in the shape already ratified at
`scripts/audit/graph/known_debt.yaml` — an entry carrying `warrant:` (naming DR-2026-08-06),
`lift_when_sql:` (`SELECT COUNT(*) FROM search_executions`) and `lift_when_ge: 1`, so the
suppression is re-evaluated against the live DB on every run and reports *itself* as STALE the
moment research resumes. Five checks declare `min_items` today — `check_utf8_md` (1000),
`check_json` (50), `check_yaml` (20), `validate_schema` (1), `research_contract_sync` (10) — and all
five guard subjects that are not empty by decree.

*A blocking check in this stage is passing on an empty subject right now.*
`citation_mining_session` is registered **blocking** with `session_pointer: LATEST-RESEARCH`.
Running it against the current pointer:

```
$ python3 scripts/audit/citation_mining_completeness.py \
    --session "$(cat sessions/LATEST-RESEARCH)" --tier-max 2
  Examined (slug-linked T1-2 sources in scope): 0
  Outstanding (no citation_mining row): 0
  VERDICT: NOTHING-IN-SCOPE
  Nothing was checked. … this run found no violation by having no subject — which is not the same
  as compliance.
$ echo $?   →  0
```

The tool is honest in prose — it prints an `Examined` count and a `NOTHING-IN-SCOPE` verdict
precisely so a pass cannot be confused with coverage — but the exit code is 0 and the gate is
blocking, so CI records it as green. This is the same condition the `research_dod` rules are in,
one enforcement level higher.

*The generator silently drops the only language whose vocabulary is fully verified.*
`scripts/generate_search_queries.py:226-256` iterates all 15 `term_aliases` languages, then does
`if not aliases: continue` — emitting nothing, with no marker and no diagnostic. Indonesian has 15
aliases but only across a narrow term set, so it vanishes from the output for every slug tested
(14 languages emitted, not 15). The bite is that per `alias_provenance_audit`, `id` is the **only**
language whose aliases are 100% VERIFIED (`id  15  15  0  0  0  0`). The generator earns real credit
for `harm_suffix_available` making a missing *translation* visible rather than silent — and there is
no equivalent flag one level up, where an entire language disappears.

*AR / BN / HI / SW coverage is structurally impossible.* `lang_jur_map` requires all four;
`term_aliases` has zero rows in any of them; the generator iterates `SELECT DISTINCT language FROM
term_aliases`, so it cannot emit a query in them at all. They nevertheless contribute **618** rows to
`v_coverage_priority` (`SELECT COUNT(*) FROM v_coverage_priority WHERE language IN ('AR','BN','HI','SW')`).
The queue contains 618 cells that no tool in this repo can service.

*The cell key is unnormalised text on both sides*, as described in (b) — no `languages` table, no
CHECK, no normalisation in `log_search()`.

*`v_coverage_priority` treats one scoping search as full coverage of a cell.* Its `NOT EXISTS`
predicate ignores `depth_method`, `saturation_signal` and even `deferred_reason`, while the view's
own `slug_searches` column excludes deferred rows — so a deliberate non-search retires a cell from
the queue while not counting as a search.

#### (g) How doctrine conditions the stage — what it FORBIDS

**Research contract R1–R15** (`governance/research-contract.yaml`, `status: OPERATIVE`, adopted by
`DR-2026-07-25-research-contract-mechanical-enforcement`, single-sourced by
`DR-2026-08-01-research-contract-single-source`) is injected verbatim into every session by the
`.claude/settings.json` SessionStart hook. At this stage it **forbids**:

- **R1** — starting with a general academic search. The Co-1 / T2 / Co-2 pass runs **first, no
  exceptions**. The rule text carries a 2026-08-01 correction recording that both prior copies said
  "Co-1/Co-2", dropping T2 and "narrow[ing] a three-part obligation to two parts in the text
  injected into every session".
- **R2** — leaving a confirmed **T1–T2** anchor unmined backward and forward. Its `resolution` block
  records that the hook previously said "T1–T3", "obliging work on a tier band the rule ledger does
  not require, which is a real cost silently imposed on every session".
- **R4** — a one-dimensional search pass. Cross slug × population / access-need / ICF / axis; cells
  are (item × population).
- **R5** — demoting non-English peer-reviewed work to grey literature. Non-indexation in
  PubMed/Scopus is an *indexing* fact, not an evidence-quality fact.
- **R6** — putting findings in `deferred_reason`. That field means DELIBERATELY NOT SEARCHED.
- **R7** — treating failure, harm or inadequacy as a by-product; it is first-class evidence, and
  off-slug or unverified material goes to `search_candidates`, **not prose**.
- **R8** — deleting or backfilling a query log. Log every query verbatim before screening; KEEP
  EMPTIES.
- **R11** — back-translation. Every alias carries its in-language source, else `[UNVERIFIED-TERMS]`.
- **R14** — reading a zero-yield search as evidence of absence without establishing that the query
  was well-formed; `findings_note` must distinguish query-shape failure from wrong index from
  genuine absence. (PubMed AND-chains every term, so a long query returns zero for mechanical
  reasons.)

**Mission** @ `0f2f525`: **commitment 3** (Co-1 co-primary with T1, CRPD Art. 4.3) is what makes R1
a floor rather than a preference. Under *Citation discipline*: "Source authenticity: confirmed real
before citation. 'I don't know' governs over invention", and "Two failed independent searches →
CLOSED-DELETED". Under *Evidence-state machine*: "Silence on evidence-thin populations is not the
default", with the Cochrane absence-of-evidence / evidence-of-absence yardstick (Altman & Bland
1995, DOI 10.1136/bmj.311.7003.485) honoured at cell level — **this is the doctrinal source of both
R14 and `deferred_reason`.**

**`governance/tier-system.md`** §2 places `sr_meta` at **T2, not T3**; §3 ("Best-practice ≠
convergence") walls T4–T6 off from full-strength anchoring; §4 makes the code-currency check part of
citing T4–T6, so a stage-3 search that retrieves a code must also target that code's currency.

**`decisions/DR-2026-05-09-adversarial-research-protocol.md`** **forbids** closing a research gap
without a prior expectation, the search queries used, a numerical confidence interval with shift
conditions, a **named dissenter** (or "NONE FOUND — searched [queries]"), and a falsification
condition. Vague conditions such as "better evidence" are explicitly not acceptable.

**`decisions/DR-2026-06-11-remove-colonial-role.md`** is the binding precedent that **forbids**
inventing search-scope rows without ratified definitions; it withdrew an entire `lang_jur_map`
population as fabrication.

**`decisions/DR-2026-08-06-clean-room-evidence-reset.md`** §4.1 is the operative instruction for
restarting this stage: "Research resuming does not restore these rows. It writes new ones under the
logged-search discipline (`db.py log-search`), carrying the admission edge that 95% of the frozen
corpus lacked."

**Two live doctrine conflicts to name at this stage.**

*The tier ladder in `skills/literature-review-planner_SKILL.md` is wrong.* Line 59 reads: "Co-1
(lived experience) = Tier 1 (OT clinical) in authority. Both precede Tier 2 (NGO/advocacy) → Co-2
(OT CPGs …) → **Tier 3 (systematic reviews / meta-analyses)** → Tier 4 …". The operative ladder puts
systematic reviews and meta-analyses at **T2** — `governance/tier-system.md` §2 is titled
"sr_meta placement — T2, not T3", and `governance/mission-and-epistemics.md:92` defines Tier 2 as
"(a) systematic reviews / meta-analyses". The skill also inverts T2's content. **Operative: mission
+ tier-system**, because tier-system is CANONICAL/OPERATIVE, §7 records the migration provenance for
the correction, and `DR-2026-05-29-evidence-hierarchy-reconciliation` post-dates the skill text. A
planner working from the skill would tier every systematic review one band too low, at the exact
point in the pipeline where target tier is chosen.

*`db.py log-search` writes the committed DB directly, which CLAUDE.md §0 rule 4 forbids.*
`connect()` (`scripts/db.py:57-63`) opens `DB_PATH` read-write with `PRAGMA foreign_keys=ON` and
commits. CLAUDE.md forbids "ad-hoc `scripts/db.py` writes to the committed DB"; DR-2026-08-06 §4.1
names exactly that command as the write path for resumed research. **Operative: the DR** — later,
owner-decided, and specific — but the reconciliation is unwritten, so a session following CLAUDE.md
and a session following the DR will do different things. And the discrepancy is not self-correcting:
`migration_reproducibility` (blocking) compares `user_version` plus `COUNT(*)` on six tables, none of
which is `search_executions`, so a direct `log-search` write would not be caught.

**One documentation defect that is *not* a disarmed gate, stated precisely.** `session_pointer_resolvable`
is named in `CLAUDE.md` §10 and in `sessions/handoff-next-session.md:12` (which asserts it is
"registered blocking"), and it exists in **no registry entry and no code**
(`grep -rn "session_pointer_resolvable" . --include=*.py --include=*.yaml --include=*.md | grep -v
_archived` returns four hits, all prose: `CLAUDE.md:424`, `sessions/handoff-next-session.md:12`, and
two workplan files). `scripts/audit/session_pointer_audit.py` was **deliberately deleted** on
2026-08-06 and its function redistributed to three existing places, per the registry note near line
475: `run_checks.py` (which FAILS a blocking check whose pointer does not resolve, where it used to
SKIP), `validate_cross_refs` (which checks the handoff's named record and plan), and
`test_db_integrity` **L04** (which reports when `LATEST-RESEARCH` drifts out of the gate's Tier 1–2
scope). So **the name is phantom while pointer honesty is partly enforced elsewhere** — partly,
because the redistribution covers a missing pointer *file* and a drifting pointer *target*, and the
CLAUDE.md sentence describing the mechanism ("an unresolvable pointer makes `run_checks.py` SKIP the
checks that read it") describes the hazard that was *fixed*, not current behaviour. The handoff file
is the first file a fresh session reads.

#### (h) ACCEPTANCE CONDITIONS — stage 3

*What makes a single `search_executions` row admissible.* Every condition marked **4** below is
**vacuous today** — `search_executions`, `search_admissions` and `evidence_sources` all hold 0 rows,
so the checks pass over nothing. The level is real; the current evidence of its operation is not.

1. **`slug` resolves to a live slug.** — Field: `search_executions.slug`. — Level **D(fk)** —
   `REFERENCES slugs(slug)` on a STRICT table, with the deferred differential check in
   `migrate_db.py` behind it and CI reach only via `migration_reproducibility`.
2. **The slug is `ACTIVE` or `STUB`.** — Field: `search_executions.slug` against `slugs.status`. —
   Level **UNENFORCED** — a `MERGED` slug satisfies the FK.
3. **`language` is one of the 19 research languages.** — Field: `.language`. — Level **UNENFORCED**
   — bare `TEXT NOT NULL` in a STRICT table; the "one of the 19 research languages" in the DDL is a
   comment. No `languages` table, no `LanguageCode` enum.
4. **`language` case and vocabulary match `lang_jur_map` so the coverage join works.** — Field:
   `.language`. — Level **UNENFORCED** — this is the live text-join hazard, with a documented
   precedent of the same mismatch silently disabling a whole feature.
5. **`(language, jurisdiction)` is a *required* cell per `lang_jur_map`.** — Field: `.jurisdiction`.
   — Level **UNENFORCED** — `v_coverage_priority` defines requiredness downstream; nothing rejects
   an out-of-scope write.
6. **`query_text` is present, verbatim, and logged before screening (R8).** — Field: `.query_text`.
   — Level **D** for presence (`TEXT NOT NULL`, STRICT); **1 text rule** for "verbatim" and "before
   screening", which are **unverifiable from data**.
7. **`engine` is recorded.** — Field: `.engine`. — Level **D** for presence (`TEXT NOT NULL`); the
   value set `pubmed|crossref|scholar|biorxiv|medrxiv|consensus|web|registry|manual` is a **comment
   only, with no CHECK**, so the vocabulary is **UNENFORCED**.
8. **`depth_method ∈ {scoping, systematic}`.** — Field: `.depth_method`. — Level **D**
   (`NOT NULL CHECK`), reinforced by `argparse choices` at the CLI.
9. **`target_tier ∈ 1..6`, and `target_evidence_type` / `target_scope` fall in their closed sets.**
   — Fields: `.target_tier`, `.target_evidence_type`, `.target_scope`. — Level **D** for the
   vocabularies. All three are **nullable**, so a search need not declare which branch of the
   hierarchy it targeted — which is the column the "diffable against what was FOUND" design depends
   on.
10. **`mining_direction ∈ {none, backward, forward, both}`.** — Field: `.mining_direction`. — Level
    **D** (`CHECK`, nullable).
11. **`saturation_signal ∈ {none, partial, saturated}`.** — Field: `.saturation_signal`. — Level
    **D** (`CHECK`, nullable).
12. **`terms_used` is valid JSON and names the aliases actually fired.** — Field: `.terms_used`. —
    Level **D** for validity (`CHECK (terms_used IS NULL OR json_valid(terms_used))`); **UNENFORCED**
    for presence and truth — the column is 0% populated by workflow design, and no check compares
    `query_text` to `term_aliases`.
13. **`admitted_ref_ids` is a valid JSON *array*, not a scalar.** — Field: `.admitted_ref_ids`. —
    Level: **D** covers *validity only*, not array-ness — `SELECT json_valid('5')` returns **1**, so
    a scalar passes the DDL. Array-ness rests entirely on **4 CI blocking** — `test_db_integrity`
    **H06** ("edge JSON columns hold arrays, not scalars or malformed text").
14. **No id repeats inside one edge array.** — Field: `.admitted_ref_ids`. — Level: **write-path
    refusal** in `log_search()` (invariant H07, named cause, before the row lands) **plus 4 CI
    blocking** — `test_db_integrity` **H07**.
15. **`results_admitted` equals the admission-edge count.** — Field: `.results_admitted`. — Level:
    **write-path refusal** (invariant H05) **plus 4 CI blocking** — `test_db_integrity` **H05**.
16. **Every entry in the JSON array has a `search_admissions` row and vice versa.** — Field:
    `search_admissions` ↔ `.admitted_ref_ids`. — Level **4 CI blocking** — `test_db_integrity`
    **H03/H04**, which hold the two equal in both directions.
17. **Every `search_admissions.ref_id` resolves to a real source.** — Field:
    `search_admissions.ref_id`. — Level: **write-path refusal** (`log_search()` names the missing
    `ref_id` rather than raising a bare FK error) **plus 4 CI blocking** — `test_db_integrity`
    **A12/A13**; **D(fk)** underneath.
18. **`deferred_reason` is non-NULL iff the search was deliberately not run, and never carries
    findings (R6).** — Field: `.deferred_reason`. — Level **3 CI non-blocking** — `research_dod` R6,
    advisory and vacuous today. The *iff* is **UNENFORCED**: nothing prevents a row with both
    `deferred_reason` and a non-zero yield.
19. **A zero-yield search records why it was empty — query shape vs wrong index vs genuine absence
    (R14).** — Field: `.findings_note`. — Level **3** — `research_dod` R14, vacuous today. This is
    the condition doctrine cares about most at this stage (Altman & Bland via the mission's
    evidence-state machine) and it is the one carried at the lowest effective level.
20. **Harm, failure and inadequacy findings are flagged (R7).** — Field: `.harm_finding`
    (`INTEGER NOT NULL DEFAULT 0`). — Level **3** — `research_dod` R7, vacuous. Nothing checks that a
    harm-shaped query set produces `harm_finding=1`, so the default silently reads as "no harm
    found".
21. **The Co-1 / T2 / Co-2 pass ran first for the batch (R1).** — Fields:
    `.target_evidence_type ∈ {co1, co2}`, or `findings_note` carrying `CO1-NOT-APPLICABLE:
    <reason>`. — Level **3 CI non-blocking** — `research_dod` R1, **the one rule currently failing**,
    and failing honestly: `NO Co-1/Co-2 pass: 0 searches targeted co1/co2 and 0 co1/co2 sources
    admitted`. Doctrine makes this a floor (commitment 3, CRPD Art. 4.3); enforcement puts it at
    advisory.
22. **Non-English peer-reviewed work is not pre-classified as grey (R5).** — Field: downstream
    `evidence_sources.grey_flag`. — Level **3** — `research_dod` R5, vacuous.
23. **Empties and deferrals are never deleted or backfilled; `backfill=1` only for honest
    reconstruction (R8).** — Field: `.backfill` (`NOT NULL DEFAULT 0 CHECK (backfill IN (0,1))`). —
    Level **D** for the vocabulary; **3** for the rule. The clean-room reset deleted all 84 rows by
    owner decision, which is the licensed exception and is recorded as such.
24. **The row is never written to a legacy grid.** — Fields: `search_coverage`, `search_languages`.
    — Level: **write-path refusal**, unconditional — `FrozenGridError` (`db.py:251`, raised at 319
    and 325) with a message printing the `log-search` replacement command. This is the strongest
    refusal in the stage and the closest thing in the repo to a pre-commit-level block; note it is
    still a *code* refusal, not a level-5 hook, because no hook exists.
25. **The batch's inherited contract debt did not rise.** — Field:
    `governance/research-contract-baseline.json` (`R13: 494, R3: 303, R9: 29, R10: 1, R11: 856`). —
    Level **4 CI blocking** — `research_contract_baseline_ratchet` (`--check-baseline origin/main`,
    `kinds: [always]`); "an unreadable base ref exits 2 rather than passing — absent is not
    innocent". The file's own comment states the direction: "Lower these numbers as debt is
    remediated; never raise them to make a batch pass."
26. **The contract text the session was given matches the YAML source.** — Fields:
    `.claude/settings.json` ↔ `governance/research-contract.yaml`. — Level **4 CI blocking** —
    `research_contract_sync`, `min_items: 10`, non-vacuous (`EXAMINED: 51 contract line(s)`).
27. **The DoD gate itself still detects violations.** — Field: — . — Level **4 CI blocking** —
    `research_dod_selftest`, blocking from day one and deliberately ungated: "a gate that has
    stopped detecting anything manufactures false confidence".
28. **The gate that reads this stage's output had a subject.** — Field: `sessions/LATEST-RESEARCH`
    → `evidence_sources.created_by_session`. — Level **4 CI blocking, currently passing on zero** —
    `citation_mining_session`. It prints `Examined … 0` and `VERDICT: NOTHING-IN-SCOPE` and exits 0.
    Pointer *resolvability* is separately held by `run_checks.py` (FAIL for a blocking check with no
    subject) and `test_db_integrity` **L04**; what is not held is the case where the pointer resolves
    correctly and the subject is legitimately empty. Per the 2026-08-06 adjudication, the fix here is
    **not** a `min_items` floor — the emptiness is ratified by DR-2026-08-06 — but a warranted,
    self-lifting suppression in the `known_debt.yaml` shape (`warrant:` DR-2026-08-06,
    `lift_when_sql: SELECT COUNT(*) FROM evidence_sources`, `lift_when_ge: 1`), so the gate stops
    reading as green-by-coverage without going red for telling the truth.

---

### 2.4 Stage 4 — Screening & admission

`search_candidates` → `search_admissions` → `evidence_sources`

> **Live state, re-derived 2026-08-11 at HEAD `6c2d179`.** `PRAGMA user_version` 53 ·
> `search_candidates` 0 · `search_admissions` 0 · `search_executions` 0 · `evidence_sources` 0
> (97 columns) · `source_slug_links` 0 · `evidence_population_match` 0 · `v_source_admission`
> (view) 0 · `slugs` 106 · `items` 93.
> ```
> $ python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);
>   print(c.execute('PRAGMA user_version').fetchone()[0],
>         [c.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0] for t in
>          ('search_candidates','search_admissions','search_executions','evidence_sources',
>           'source_slug_links','slugs','items')])"
> 53 [0, 0, 0, 0, 0, 106, 93]
> ```
> The clean-room reset (`decisions/DR-2026-08-06-clean-room-evidence-reset.md`, executed by
> `scripts/migrations/data_20260806222208_2026-08-06-clean-room-reset.sql`) emptied every table
> this stage owns. **Stage 4 is BUILT+UNEXERCISED in its entirety** against the current DB. The
> only stage-4 code labelled BUILT+EXERCISED below is code that demonstrably *runs* — its
> subject is empty.

#### (a) Tools, tables, methodology

**Tables.**

| Object | State | Provenance / evidence |
|---|---|---|
| `search_candidates` (0 rows, **14 columns**) | BUILT+UNEXERCISED | Created by `scripts/migrations/036_search_findings_and_candidates.sql`; FKs declared by `039_declare_soft_edges_as_foreign_keys.sql`. `STRICT` table. |
| `search_admissions` (0 rows) | BUILT+UNEXERCISED | `scripts/migrations/050_search_admissions.sql`; `PRIMARY KEY (exec_id, ref_id)` |
| `evidence_sources` (0 rows, 97 columns) | BUILT+UNEXERCISED | DDL read live from `sqlite_master` |
| `source_slug_links` (0 rows) | BUILT+UNEXERCISED | `PRIMARY KEY (ref_id, slug)`, `local_ref_id TEXT NOT NULL` |
| `evidence_population_match` (0 rows) | BUILT+UNEXERCISED | R13's subject |
| `v_source_admission` (view, 0 rows) | BUILT+UNEXERCISED | `scripts/migrations/051_admission_provenance_view.sql` |
| `search_executions.admitted_ref_ids` (TEXT JSON) | BUILT+UNEXERCISED | the pre-050 carrier, kept in parallel |
| `search_coverage`, `search_languages` (0 / 0) | superseded | `scripts/db.py` help: `log-search … (replaces upsert-coverage/-language)` |

The `search_candidates` DDL is unusually well constrained for this repo. `disposition` is a SQL
`CHECK` over exactly five values — `'REHOME','MISCELLANEOUS','PENDING-VERIFICATION',
'OUT-OF-SCOPE','ADMITTED'`; `locator_status ∈ {UNVERIFIED, RESOLVED, DEAD}`; `tier_guess BETWEEN
1 AND 6`; `harm_finding IN (0,1)`; and the table carries the `STRICT` keyword, so type coercion
cannot smuggle a wrong type past those checks. Its fourteen columns are:

```
$ python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);
  cols=[r[1] for r in c.execute('PRAGMA table_info(search_candidates)')];print(len(cols),cols)"
14 ['candidate_id','exec_id','found_under_slug','suggested_slug','disposition','title',
    'locator','locator_status','tier_guess','harm_finding','why_not_admitted','notes',
    'session','created_at']
```

**Scripts.**

| Path | Role | State |
|---|---|---|
| `scripts/audit/research_batch_dod.py` (735 ln) | the R1–R15 definition-of-done gate; `--session`, `--all`, `--selftest`, `--write-baseline`, `--check-baseline` | BUILT+EXERCISED — runs; the selftest builds a synthetic violating corpus from live DDL and asserts the gate rejects it |
| `scripts/db.py log-search` | the only writer for `search_executions` **and** `search_admissions`, both in one transaction (`scripts/db.py:392-417`) | BUILT+UNEXERCISED |
| `scripts/db.py add-source`, `insert_source_slug_link` | writers for `evidence_sources` / `source_slug_links` | BUILT+UNEXERCISED |
| `scripts/audit/source_slug_links_duplicates.py` | duplicate `(slug, local_ref_id)` audit; blocking | BUILT+EXERCISED — prints `EXAMINED: 0 source_slug_links row(s)` |
| `scripts/audit/research_protocol_audit.py` | 9 adversarial-protocol checks; advisory | BUILT+EXERCISED, 0 issues on an empty corpus |
| `scripts/audit/population_integrity_audit.py` | R13-adjacent; advisory | BUILT; unexercised in substance |
| **no writer at all for `search_candidates`** | — | **DESIGNED-ONLY.** `python3 scripts/db.py --help` lists **33** subcommands and none writes candidates; `grep -rn "INSERT INTO search_candidates" scripts/migrations/` returns 4 hand-written `data_202607*` migrations |

**Registered checks** (`governance/check-registry.yaml` — 64 active, 16 quarantined, counted with
`yaml.safe_load`):

| id | battery | level | kinds | verdict today |
|---|---|---|---|---|
| `research_dod` | research | advisory | data, synthesis | **FAIL — R1 only** |
| `research_dod_selftest` | research | **blocking** | always | PASS |
| `research_contract_baseline_ratchet` | research | **blocking** | always | PASS (`EXAMINED: 5 baselined rule(s)`) |
| `research_contract_sync` | research | **blocking** | governance, tooling | PASS (`EXAMINED: 51 contract line(s)`; `min_items: 10`) |
| `source_slug_links_duplicates` | data | **blocking** | data | PASS on 0 examined |
| `test_db_integrity` (A01/A12/A13/D01/D04/D05/H03–H07) | db_integrity | **blocking** | data, schema | PASS 70/70 |
| `research_protocol_audit` | research | advisory | data, synthesis | PASS |
| `population_integrity_audit` | research | advisory | data, schema | PASS |

```
$ python3 scripts/run_checks.py --kinds data --battery research | tail -2
NON-BLOCKING failures (1): research_dod
RESULT: PASS — 9 check(s) green, 1 advisory failure(s)
```

**Doctrine / methodology documents.** `governance/research-contract.yaml` is **OPERATIVE**
(`status: OPERATIVE`, `adopted_by: DR-2026-07-25-research-contract-mechanical-enforcement.md`,
`resolved_by: DR-2026-08-01-research-contract-single-source.md`) and is the canonical R1–R15
text; the SessionStart hook in `.claude/settings.json` is *generated* from it and parity is a
blocking check (`python3 scripts/generate/research_contract_hook.py --check` →
`PASS: contract and enforcer agree on 15 rule ids`). `governance/pipeline-operations.md` is
**PROPOSED** and supplies the stage's conceptual boundary: adjudication "is not a sixth
operation — it is the gate between 1–3 and 4, recorded on the source itself
(`verification_status`, `tier`, `search_candidates.disposition`)".
`governance/pipeline-contract.yaml` is PROPOSED/advisory, stage `collection`.

#### (b) How they relate to each other

Read off the live DDL and `scripts/db.py:380-417`, the wiring is:

```
search_executions(exec_id)                    ← written by db.py log-search
    │  FK exec_id  (NULLABLE on the candidate side)
    ├──────────────► search_candidates          disposition ∈ 5 values
    │                   found_under_slug ─FK→ slugs.slug   (NOT NULL)
    │                   suggested_slug   ─FK→ slugs.slug   (NULL = MISC / undecided)
    │
    └──────────────► search_admissions ─FK→ evidence_sources.ref_id
                        ∥  held equal in BOTH directions by test_db_integrity H03/H04
                     search_executions.admitted_ref_ids   (JSON array, legacy carrier)

evidence_sources(ref_id)
    ├──► source_slug_links(ref_id, slug, local_ref_id)     ← the topic attachment
    └──► evidence_population_match(ref_id, …)              ← R13's graded match
```

**Where the join is by key.** `search_admissions.exec_id → search_executions`,
`search_admissions.ref_id → evidence_sources`, `search_candidates.exec_id / found_under_slug /
suggested_slug`, `source_slug_links.ref_id / slug`. `test_db_integrity` A12/A13 assert the
`search_admissions` FKs have no orphans and A01 asserts `source_slug_links → evidence_sources`;
the A-series is a table-driven orphan scan (`scripts/tests/test_db_integrity.py:121-124`).

**Where the join is by text, or absent — three places, all load-bearing.**

1. **`search_candidates` → `evidence_sources`: there is no join at all.** The disposition
   `ADMITTED` records that admission happened; nothing on the row names the `ref_id` it became.
   The fourteen columns above contain no `admitted_ref_id`. The loop closes one level up —
   `exec_id → search_admissions → ref_id` — but only at the grain of the whole search. If one
   execution screened forty candidates and admitted three sources, `search_admissions` says
   *which three refs exist*, never *which three candidates became them*. This is workplan
   finding N4, and it is open at `user_version = 53`.
2. **`source_slug_links.local_ref_id`** is free TEXT, slug-scoped, with no uniqueness constraint
   beyond the `(ref_id, slug)` primary key. It is the join key stage 6 depends on (§2.6(b)), and
   duplicates in it are a *separate blocking check* — `source_slug_links_duplicates` — precisely
   because the schema cannot prevent them.
3. **`search_executions.admitted_ref_ids`** is a JSON array duplicating `search_admissions`.
   Migration 050's header states the two "coexist, held equal by a parity check in both
   directions (test_db_integrity H02/H03)" — **the header's ids are off by one**: the live parity
   pair is H03/H04 (`_parity("H03","H04","search_admissions ↔ admitted_ref_ids", …)` at
   `scripts/tests/test_db_integrity.py:820`), while H01/H02 guard `cell_source_links ↔
   governing_refs`. Doc drift only; the checks are correct and pass.

`scripts/db.py:399-417` is the one place both carriers are written together, inside a single
transaction, behind a named pre-check that refuses an `--admitted-ref-id` absent from
`evidence_sources`: *"File the source first (`db.py add-source`), then log the search that
admitted it."* That ordering is the admission contract expressed in code, and it rolls the whole
execution row back rather than raising a bare `FOREIGN KEY constraint failed`.

#### (c) Relation to the previous stage (Stage 3 — search execution)

**Entry contract.** A candidate may be screened only if it came out of a logged search:
`search_candidates.exec_id` references `search_executions(exec_id)`, and `session` /
`created_at` are `NOT NULL`.

| Requirement | Enforcer | Level |
|---|---|---|
| `exec_id` resolves to a real search *when set* | `test_db_integrity` A-series (direct) + the migration-039 FK | 4 blocking + **D(fk)** — see §(h) preamble; FKs are `OFF` during migration scripts and checked differentially afterwards |
| The search log is append-only (empties not deleted) | `research_batch_dod` **R8** (`max(exec_id) > COUNT(*)` ⇒ deletion) | 2 — advisory registration |
| A zero-yield search says why | **R14** (`results_found=0 AND deferred_reason IS NULL AND findings_note=''`) | 2 — advisory |
| Findings not smuggled into `deferred_reason` | **R6** | 2 — advisory |
| A search that screened N results staged ≥ N/25 candidates | **R7** (`R7_SCREENED_PER_CANDIDATE = 25`) | 2 — advisory |

**`exec_id` is nullable.** The DDL reads `exec_id INTEGER REFERENCES search_executions(exec_id)`
with no `NOT NULL`, one line above `found_under_slug TEXT NOT NULL REFERENCES slugs(slug)` which
has it. A foreign key fires only on a non-NULL value, so a candidate can exist with no search
behind it and pass every check. **Nothing enforces** that a screened candidate names its search.

**Nothing blocking gates stage 3 → stage 4 at all.** The R1–R15 contract's only *blocking*
registrations are `research_dod_selftest` (proves the checks fire against a synthetic corpus)
and `research_contract_baseline_ratchet` (proves the amnesty file only ratchets down). The
contract itself — `research_dod` — is registered `advisory`. That is recorded, not hidden:
`workplan/2026-08-02-architecture-decision-and-execution-plan.md` W6 says "Promote `research_dod`
to blocking — the R1–R15 contract has no blocking enforcement anywhere today."

#### (d) Relation to the next stage (Stage 5 — source verification)

**Exit contract.** An admitted row must be something a verifier can act on: a locator
(`doi` / `url` / `pmid`) or a `verified_by_tool`, a `tier`, and a topic attachment through
`source_slug_links`.

| Handoff requirement | Enforcer | Level |
|---|---|---|
| No admission without re-retrieval of the locator | **R10**, two-part: (a) `VERIFIED` with no `doi`/`url`/`pmid`/`verified_by_tool`; (b) `VERIFIED` with a `doi` whose `doi_resolution_outcome` is neither `RESOLVED` nor `NO-MATCH` | 2 advisory; baselined at 1 |
| No duplicate-DOI admission | **R9** (batch-scoped) + `test_db_integrity` **D01** (corpus-wide) | R9 advisory (baselined 29); D01 **4 blocking** |
| DOI-less sources still get a dedup key | `test_db_integrity` **D04/D05** | 4 blocking |
| Every tier-1–3 admission carries a graded population match | **R13** | 2 advisory, baselined 494 |
| A candidate marked ADMITTED was re-described from the source | **R15** (`disposition='ADMITTED' AND notes NOT LIKE '%RESOLVED%'`) | 2 advisory |
| `search_admissions` ↔ `admitted_ref_ids` agree both ways; `results_admitted` = edge count | `test_db_integrity` **H03/H04/H05** | 4 blocking |

`governance/research-contract-baseline.json` forgives R13 at 494, R3 at 303, R9 at 29, R10 at 1
and R11 at 856, captured `2026-08-06`. Four of those five now describe debt that no longer exists
in the DB; only `R11: 856` still matches live `term_aliases` debt, which the reset did not clear
(`research_batch_dod --all` reports `~ R11: 856 (baseline 856) — INHERITED DEBT`). They ratchet
down only and cannot rise without `research_contract_baseline_ratchet` failing against
`origin/main`, so they are harmless but stale; the honest post-reset move is to re-run
`--write-baseline` and let the four fall to 0.

#### (e) The goal of the stage

Stage 4 is the project's **admission gate**. It converts the undifferentiated yield of a search
into two disjoint records: a *staged candidate*, which is a hypothesis about a document, and an
*admitted source*, which is a claim that the document exists, has been re-retrieved, carries a
tier, and belongs to a topic. Its purpose is to make the difference between "we saw this" and
"we hold this" a queryable fact rather than a matter of narrative. Everything downstream —
verification, mining, extraction, cell determination — reads `evidence_sources`, so the corpus's
honesty is decided entirely here. The stage also exists to **prevent evaporation**: R7's whole
point is that off-slug, unverified and out-of-scope material must land in `search_candidates`
with a coded disposition rather than in prose that disappears, so a later session can distinguish
"we rejected this, and here is which kind of rejection" from "we never saw it". The reset is the
proof of what happens when it fails: `DR-2026-08-06-clean-room-evidence-reset.md` §1 gives the
governing number in one line — **"sources with no recorded admission: 824 of 863"** — i.e. the
corpus was emptied *because* stage 4's provenance record did not exist for 95% of it.

#### (f) How the tools support that goal — and where they do not

**Support.**

*The disposition vocabulary is a real taxonomy of non-admission.* `REHOME` (right material, wrong
slug — `suggested_slug` carries the destination), `MISCELLANEOUS` (`suggested_slug` NULL by
design), `PENDING-VERIFICATION` (R10 not yet satisfied), `OUT-OF-SCOPE`, `ADMITTED`. Four of the
five are ways of saying "not admitted, and here is which kind of not", with `why_not_admitted` as
the prose companion. That is exactly the distinguish-absence-from-decision discipline
`governance/pipeline-operations.md` §4 argues for, and it is enforced by a SQL `CHECK` on a
`STRICT` table, which is the strongest enforcement available short of inexpressibility.

*The dual-carrier plus parity-check pattern is genuinely load-bearing.* `search_admissions`
normalises what was a JSON array; rather than dropping the array — which would require a caller
sweep under CLAUDE.md §0 rule 5 — both are kept and held equal in both directions by blocking
checks H03/H04/H05. Migration 050's header is explicit that "Dropping it is a separate act
requiring a caller sweep."

*R7 and R15 close the two prose leaks specifically.* R7 makes candidate registration a *ratio* of
results screened (one per 25) rather than `> 0`; the enforcer's own hardening note records that
the `> 0` version was "gameable forever by one row". R15 makes an `ADMITTED` candidate's own
description a hypothesis until a `RESOLVED` note re-describes it from the source.

**Where they do not.**

*The candidate→source pointer is missing.* A staged candidate that is admitted leaves no forward
pointer (§(b) item 1). R15's check — `disposition='ADMITTED'` and `notes NOT LIKE '%RESOLVED%'` —
is the only mechanism connecting a candidate to its resolution, and it operates on a substring of
a free-text column. That is a text join standing in for a foreign key.

*There is no writer for `search_candidates`.* Thirty-three `db.py` subcommands, including
`log-search`, `add-source`, `log-mining` and `add-gap-mining`, and none for candidates. Every
historical row arrived by hand-written data migration. A stage whose contract table has no tool
is a stage whose contract gets skipped under load — which is precisely the 2026-07-24 failure
`research_batch_dod` was written about. (Note the inconsistency cuts both ways: migrations-only
is the *correct* posture under CLAUDE.md §0 rule 4, which makes `log-search`, `add-source` and
`log-mining` — all of which open the committed DB read-write — the anomaly. The three are
inconsistent with each other whichever posture is right.)

*R7 cannot fire when nothing was screened.* `expected = max(1, screened // 25) if screened else 0`,
guarded by `if total and cand < expected` (`scripts/audit/research_batch_dod.py:392-396`). A batch
whose searches all report `results_screened = 0` has `expected = 0`, `cand = 0`, and passes. The
proportionality fix protected against under-staging relative to yield; it left "declare no yield"
wide open.

*`search_candidates.exec_id` is nullable*, so the provenance FK the stage depends on is optional
in the schema and mandatory only in intent.

*Nothing requires an `evidence_sources` row to have ever been a candidate.* Migration 050's header
is candid about the historical case — "The other 824 sources predate the search-execution
substrate (DR-2026-07-24). They were admitted by searches nobody logged." — and treats that
absence as the correct record. Post-reset that reasoning no longer applies to new work, and no
check has been added to require it of new work either.

*R1's enforcer implements two of the three parts the canonical contract requires.*
`governance/research-contract.yaml` R1 is titled **"Co-1 / T2 / Co-2 pass FIRST"** and its
`resolution` block records the 2026-08-01 correction: dropping T2 "narrowed a three-part
obligation to two parts in the text injected into every session. Restored to the source." The
hook was restored; the enforcer was not. `research_batch_dod.py:276-280` counts
`search_executions WHERE target_evidence_type IN ('co1','co2')` and `evidence_sources WHERE
evidence_type IN ('co1','co2')` — no tier-2 term anywhere. A batch that runs a Co-1 pass and no
disability-led-NGO Tier-2 pass satisfies R1. `research_contract_sync` cannot see this: it
cross-references **rule ids** (`agree on 15 rule ids`), never rule content.

*R1 is the stage's one live failure, and it is vacuous — but it is not unsatisfiable.*
`research_batch_dod.py --all` exits 1 on R1 alone; the other fourteen rules pass by absence of
violation ("0 … for 0 …"). R1 is the only rule whose pass requires *positive* evidence, so the
corpus scores fourteen vacuous passes and one vacuous failure. The fail condition is a three-way
conjunction over three independent counters, and **`co1_src` reads `evidence_sources`, not
`search_executions`**:

```python
co1        = COUNT(*) FROM search_executions WHERE target_evidence_type IN ('co1','co2')
co1_src    = COUNT(*) FROM evidence_sources  WHERE evidence_type IN ('co1','co2')
co1_waiver = COUNT(*) FROM search_executions WHERE findings_note LIKE '%CO1-NOT-APPLICABLE%'
if co1 == 0 and co1_src == 0 and co1_waiver == 0:      # :287
```

Admitting one Co-1/Co-2 source — which is what actually doing the Step-1 pass produces — turns R1
green with no `search_executions` row at all. There are two remedy paths, and neither requires
fabricating a search. The narrower true statement is that **the waiver path alone is unreachable**:
`co1_waiver` predicates on `search_executions.findings_note`, and that table is empty, so the
"record `CO1-NOT-APPLICABLE`" half of the failure message names a column with nowhere to live.
That asymmetry is worth recording. The remaining objection is about *information content per
diff*, not correctness — "no Co-1 pass has been done" is a true statement about a project that has
done no research. It matters only because W6 proposes promoting `research_dod` to blocking; doing
so today reddens every data/synthesis diff for a reason no diff can fix. The correct
pre-condition is **not** a bare `min_items`: an empty corpus here is empty *by ratified decision*
(`DR-2026-08-06`), and the repo already adjudicated that case on 2026-08-06 and retired a floor it
had just added, on the reasoning that the guard catches an *accidentally* empty subject and "an
empty subject that is the declared state of the project is not that". The right shape is a
**warranted, self-lifting suppression** in the form `scripts/audit/graph/known_debt.yaml` already
proves — `warrant:` citing DR-2026-08-06, `lift_when_sql: "SELECT COUNT(*) FROM search_executions"`,
`lift_when_ge: 1` — so R1's floor returns mechanically the moment research resumes, and the
suppression itself is reported STALE rather than silently hiding a regression.

#### (g) How doctrine conditions the stage

**`governance/mission-and-epistemics.md` § Citation discipline**, verbatim:

> - Quantified outcome claims require DOI + page/table reference, or failing that, direct URL to
>   source. Unverified claims carry `[UNVERIFIED-QUANT]` flag.
> - Two failed independent searches → CLOSED-DELETED disposition for unverifiable values; do not
>   accumulate unresolvable UNVERIFIED flags.
> - **Source authenticity: confirmed real before citation. "I don't know" governs over invention.**

That last line is the stage's governing forbiddance: **admission of an unconfirmed source is
forbidden outright**, not discounted. R10 is its mechanical form.

**Doctrinal commitment 3 — "Co-1 evidence is co-primary with Tier 1"** (§ Doctrinal commitments
#3, citing CRPD Art. 4.3). This forbids a batch that admits only clinical and academic sources and
calls the pass complete. R1 is its mechanical form, and the enforcer's own hardening note records
that R1's first version accepted a substring match in `query_text` and duly passed a run with zero
Co-1 sources because one unrelated query contained the words "lived experience": *"The project's
most important doctrinal commitment had the weakest check."*

**Doctrinal commitment 2 — best practice is graded by the evidence hierarchy; code consensus
anchors it only at the weak band.** At stage 4 this bears on `tier_guess` and `tier`: T4–T6 is the
regulatory stratum, and admitting a code as though it were evidence is the error the tier system
exists to prevent. `governance/tier-system.md` §3 ("Best-practice ≠ convergence") is operative;
§4 additionally requires that citing a T4–T6 source confirm the cited edition is the current
legally-in-force edition — a stage-4 obligation discharged by stage-5 machinery
(`code_currency_audit.py`, currently quarantined; §2.5).

**Research contract R1/R6/R7/R9/R13/R15 — what each forbids** (canonical text,
`governance/research-contract.yaml`):

- **R1** forbids a batch with zero co1/co2-targeted searches, zero co1/co2 sources and no
  `CO1-NOT-APPLICABLE` waiver. Its title is the three-part "Co-1 / T2 / Co-2 pass FIRST".
- **R6** forbids using `deferred_reason` as a findings field: it means "deliberately NOT
  searched", and coverage views filter on it.
- **R7** forbids leaving off-slug or unverified material in prose — "Off-slug or unverified
  material -> search_candidates (REHOME/MISC/PENDING), not prose" — and, in its primary clause,
  forbids treating failure/harm/inadequacy as a by-product rather than first-class evidence.
- **R9** forbids creating a second row for a DOI already in the corpus. Enforced three times:
  advisory at batch scope, blocking corpus-wide via `test_db_integrity` D01, and pre-emptively in
  `db.py add_source`, which raises `ValueError` naming the existing `ref_id`.
- **R13** forbids an admission with no `evidence_population_match` row, because absence "silently
  claim[s] they are the same" — the population studied and the population served. The three worked
  examples in the enforcer's docstring (a chamber emissions test with no human participants; a
  general-population autistic-traits sample; a general-population children sample) are the
  doctrine's teeth.
- **R15** forbids letting a staged candidate's own description harden into fact.

**DRs bearing on this stage.** `DR-2026-07-25-research-contract-mechanical-enforcement.md` (adopts
R1–R15 under the owner directive "RESEARCH IS INVALID IF IT IS NOT COMPLIANT WITH OUR GOVERNANCE
AND VERIFICATION TOOLS AND RULES AND ETHOS"); `DR-2026-08-01-research-contract-single-source.md`
(makes the YAML canonical and resolves the R1/R2/R3 drift); `DR-2026-07-24` (introduces the
search-execution substrate); `DR-2026-08-06-clean-room-evidence-reset.md` (empties the corpus, for
this stage's failure).

#### (h) ACCEPTANCE CONDITIONS

Levels use the repo's 5-level spectrum (1 text · 2 audit script · 3 CI non-blocking · 4 CI
blocking · 5 pre-commit hook). **No level-5 hook is installed anywhere in this repo, so 4 is the
ceiling.**

**The spectrum has no rung for DDL constraints, and that omission is itself a finding.** A great
many of this stage's strongest guarantees are SQL `CHECK`, `UNIQUE`/`PRIMARY KEY`, `NOT NULL` and
`FOREIGN KEY` declarations, and mapping them onto 1–4 misdescribes them in both directions. This
document therefore uses a distinct level **D (schema constraint)** with two forms:

- **`D — enforced at write time by SQLite`** for `CHECK`, `UNIQUE`, `PRIMARY KEY` and `NOT NULL`.
  These fire on every connection regardless of any pragma; the write fails. They are arguably
  stronger than a level-4 CI check, since there is no window in which the bad row exists.
- **`D(fk) — deferred differential check`** for `FOREIGN KEY`. SQLite leaves FK enforcement **off
  per connection** unless `PRAGMA foreign_keys=ON`, and `scripts/migrate_db.py` sets
  `PRAGMA foreign_keys = OFF` before every migration script (`:164` for schema migrations, `:251`
  for data migrations) so bulk inserts can arrive in any order. FKs are not therefore unenforced:
  `migrate_db.py:160-183` snapshots `PRAGMA foreign_key_check` before the script, disables FKs for
  the load, re-enables after, diffs the two violation sets, and raises `sqlite3.IntegrityError` on
  **new** violations. Three caveats belong in every FK row: (i) a pre-existing violation baseline
  is permanently grandfathered by design — the code comment reads "Pre-existing production drift
  (~18 violations) should not fail a clean migration"; (ii) any migration whose first 500 bytes
  contain `BOOTSTRAP` downgrades the failure to a printed WARNING and continues; (iii) its reach
  into CI is *indirect*, via the blocking `migration_reproducibility` check, which rebuilds the DB
  from migration history.

For one **`search_candidates` row**:

1. **`disposition` is one of the five values.** Column `search_candidates.disposition`.
   *Level: **D — enforced at write time by SQLite***. SQL `CHECK` in migration 036, on a `STRICT`
   table, so type coercion cannot smuggle a value past it either.
2. **The candidate names the search that surfaced it.** Column `exec_id`.
   *Level: **UNENFORCED*** — the column is nullable, so the FK declared by migration 039 has
   nothing to fire on. Even `D(fk)`'s differential check sees no violation in a NULL.
3. **`found_under_slug` is a real slug.** Column `found_under_slug`.
   *Level: **D** (`NOT NULL`, write-time) + **D(fk)** (`REFERENCES slugs(slug)` — deferred
   differential check in `migrate_db.py`; new violations fail, pre-existing baseline grandfathered,
   bootstrap migrations exempt; reaches CI via `migration_reproducibility`, blocking) + 4 blocking*
   — `test_db_integrity`'s A-series orphan scan is the direct CI enforcer.
4. **A `REHOME` candidate names its destination.** Column `suggested_slug`.
   *Level: **UNENFORCED*** — no CHECK ties `suggested_slug` to `disposition='REHOME'`.
5. **A non-ADMITTED candidate says why.** Column `why_not_admitted`.
   *Level: 1 (text rule)* — the migration-036 DDL comment says "required in practice"; the column
   is nullable and nothing checks it. Enforcer: the comment.
6. **`tier_guess` ∈ 1..6; `locator_status` ∈ {UNVERIFIED, RESOLVED, DEAD}; `harm_finding` ∈ {0,1}.**
   Those columns. *Level: **D — enforced at write time by SQLite*** — SQL CHECKs, migration 036.
7. **An `ADMITTED` candidate carries a `RESOLVED` note re-describing it from the source.**
   Column `notes` (substring `RESOLVED`). *Level: 2 (audit script, registered advisory)* —
   `research_batch_dod` R15.
8. **The batch registered ≥ `results_screened / 25` candidates.** Count vs
   `search_executions.results_screened`. *Level: 2 advisory*, and **vacuous when
   `results_screened = 0`.** Enforcer: `research_batch_dod` R7.
9. **Harm / failure / inadequacy findings are flagged.** Column `harm_finding` (and
   `search_executions.harm_finding`). *Level: 1 — reported, never asserted.* R7 prints the harm
   count in its pass message; the pass condition is the candidate ratio only.

For one **admitted `evidence_sources` row**:

10. **`ref_id` is unique and this is not a re-admission.** Column `ref_id`.
    *Level: **D — enforced at write time by SQLite** (PRIMARY KEY) + writer pre-check* —
    `db.py add_source` additionally raises `ValueError` naming the existing row.
11. **Its DOI is not already in the corpus.** Column `doi`.
    *Level: 4 blocking corpus-wide* (`test_db_integrity` D01), *2 advisory batch-scoped*
    (`research_batch_dod` R9, baselined 29), plus a pre-flight in `db.py add_source`.
12. **A DOI-less source has a computable dedup key.** Columns `first_author_last`, `pub_year`,
    `pub_title`. *Level: 4 blocking* — `test_db_integrity` D04/D05.
13. **It was re-retrieved before admission — a locator or a verifying tool exists.** Columns
    `doi` / `url` / `pmid` / `verified_by_tool`. *Level: 2 advisory* — `research_batch_dod` R10(a),
    baselined at 1.
14. **If it holds a DOI and claims VERIFIED, the resolution outcome is on record.** Column
    `doi_resolution_outcome` ∈ {RESOLVED, NO-MATCH}. *Level: 2 advisory* — R10(b).
15. **It is attached to at least one topic.** A `source_slug_links` row.
    *Level: **UNENFORCED as a requirement**, and the absence is load-bearing downstream* — it
    silently exempts the source from the blocking citation-mining gate (§2.6(h) #10).
16. **Its `(slug, local_ref_id)` is unique within the slug.** Column
    `source_slug_links.local_ref_id`. *Level: 4 blocking only — **no D is available***. The table's
    `PRIMARY KEY (ref_id, slug)` does not constrain `(slug, local_ref_id)`, which is precisely why
    `scripts/audit/source_slug_links_duplicates.py` exists as a separate blocking check rather than
    as a `UNIQUE` index.
17. **If tier 1–3, it carries a graded population match.** An `evidence_population_match` row.
    *Level: 2 advisory*, baselined at 494 — `research_batch_dod` R13.
18. **If tier ≥ 4, it carries a clause/section/page locator or `[UNVERIFIED-QUANT]`.** Columns
    `article_number` / `pages` / `notes`. *Level: 2 advisory*, baselined at 303 — R3.
19. **Non-English peer-reviewed work is not pre-classified `grey`.**
    `search_executions.target_evidence_type` vs `language`. *Level: 2 advisory* — R5.
20. **A Co-1 / T2 / Co-2 pass was run, or waived with a reason.**
    `search_executions.target_evidence_type` / `evidence_sources.evidence_type` /
    `findings_note LIKE '%CO1-NOT-APPLICABLE%'`. *Level: 2 advisory* — `research_batch_dod` R1.
    **Two caveats:** the enforcer implements the co1/co2 pair only, not the contract's T2 third
    part; and on the current empty corpus the *waiver* branch is unreachable while the
    *source* branch (`co1_src`, over `evidence_sources`) remains satisfiable.
21. **The admission edge exists in both carriers and they agree.** `search_admissions` +
    `search_executions.admitted_ref_ids` + `results_admitted`. *Level: 4 blocking* —
    `test_db_integrity` H03/H04/H05, plus H06/H07 for array-ness and duplicate ids. The junction's
    own `PRIMARY KEY (exec_id, ref_id)` adds **D** against a duplicate edge.
22. **The `search_admissions` row points at real rows on both ends.** `exec_id`, `ref_id`.
    *Level: 4 blocking + **D(fk)*** — `test_db_integrity` A12/A13 is the direct blocking enforcer;
    the declared FKs to `search_executions` and `evidence_sources` are `D(fk)` — deferred
    differential check in `migrate_db.py` (FKs are OFF during every migration script), new
    violations fail, pre-existing baseline grandfathered, `BOOTSTRAP` migrations exempt, reaching
    CI only indirectly through the blocking `migration_reproducibility` rebuild. The A-series is
    what makes this a live guarantee rather than a load-time one.
23. **The row was written through a migration, not by hand.** *Level: 4 blocking, but only at
    COUNT grain* — `scripts/audit/migration_reproducibility.py` compares `PRAGMA user_version`
    plus `COUNT(*)` on six tables (`evidence_sources`, `citation_mining`, `source_slug_links`,
    `gaps`, `connections`, `items`). An `UPDATE` moves no count; nothing in the other 55 tables is
    seen at all. The full row-level comparison exists as `migration_reproducibility_deep` and is
    **advisory** pending an owner decision.

---

### 2.5 Stage 5 — Source verification

`resolve_dois` (Channel 1) · `verify_urls` (Channel 2) · `metadata_quality` · the four-column
verification standing

#### (a) Tools, tables, methodology

**The vocabulary is the centre of gravity of this stage.**
`decisions/DR-2026-08-04-verification-status-is-a-standing-not-a-history.md` (D-0157, ADOPTED
under owner directive 2026-08-04) split one column into four. **The migration has landed**, which
means the DR's own opening caveat — *"Ratified ≠ executed. The migration implementing §5 has not
run; B01/B02/B05 stay red until it does"* — is now **stale** and should not be read as live
guidance. Verified on four surfaces:

```
$ ls scripts/migrations/ | grep -E "^049"        → 049_verification_standing_columns.sql
$ PRAGMA user_version                            → 53  (≥ 49)
$ live evidence_sources DDL                      → verification_disposition CHECK (…'OPEN','CLOSED')
                                                    verification_method      CHECK (…5 values)
                                                    verification_closure_reason CHECK (…6 values)
$ grep -ln verification_disposition scripts/migrations/data_*.sql
    data_20260804161658_2026-08-04-d0157-remap.sql
    data_20260804164915_2026-08-04-d0157-corrections.sql
$ python3 scripts/tests/test_db_integrity.py | tail -2   → RESULTS: 70/70 checks passed
```

DR §5.1's demand — *"The ratification migration therefore ships with an audit and update of the
write vocabulary in `scripts/resolve_dois.py` and `scripts/verify_urls.py`, in the same change"* —
**was honoured**: both writers now set `verification_disposition` and `verification_method` in the
same UPDATE that sets `verification_status` (`scripts/resolve_dois.py:126-134`,
`scripts/verify_urls.py:238-247`). The four-column model is therefore **BUILT** in schema, in
Pydantic (`schemas/enums.py` carries `VerificationDisposition` / `VerificationMethod` /
`VerificationClosureReason`; `VerificationStatus` is `{VERIFIED, UNVERIFIED}` and nothing else),
in the blocking check, and in both writers — and **UNEXERCISED on data**, because
`evidence_sources` holds 0 rows.

| Column | Vocabulary | Answers |
|---|---|---|
| `verification_status` | `VERIFIED` · `UNVERIFIED` | is it established? |
| `verification_disposition` | `OPEN` · `CLOSED` | is more effort owed? |
| `verification_attempt_count` | integer | how much was spent? |
| `verification_method` | `direct-render`, `co1-attestation`, `corroborated-not-retrieved`, `citing-bibliography`, `tool` | how was it established? |
| `verification_closure_reason` | `paywalled`, `print-only`, `access-denied-persistent`, `withdrawn`, `not-found-after-search`, `disputed-existence` | why did effort stop? |
| `metadata_quality` | `COMPLETE`, `COMPLETE-STATUTORY`, `AUTHOR-TITLE-ONLY`, `GREY`, `PMID-ONLY`, `NULL` (`PARTIAL` retired by D-0157 §4.5) | how complete is the record? |

**One correction that matters for §(h): only the three *new* columns carry SQL CHECKs.**
`verification_status` is bare `TEXT`. Migration 049's header says so and gives the reason:

> "`verification_status` itself is **NOT altered here**. Its **CHECK-less TEXT shape stays**, the
> data migration narrows its values to {VERIFIED, UNVERIFIED}, and test_db_integrity's B01 becomes
> the enforcer. Adding a CHECK constraint would require a table rebuild of 94 columns — migration
> 039's header warns that hand-copying such a definition 'is how a rebuild silently changes a
> type, default, or CHECK' — for an invariant a registered check already covers."

Confirmed live: `verification_status TEXT,` with no CHECK anywhere in the `evidence_sources` DDL
mentioning it. `metadata_quality` is likewise bare `TEXT`. So the standing vocabulary is protected
at **level 4 (blocking check)**, not at the database. The write does not fail.

**Scripts.**

| Path | Writes | Runs where | State |
|---|---|---|---|
| `scripts/resolve_dois.py` (1070 ln) | `evidence_sources` UPDATE; `evidence_source_authors` DELETE+INSERT; `pipeline_runs` CREATE-IF-NOT-EXISTS + INSERT/UPDATE | `.github/workflows/resolve-dois.yml`, weekly Mon 06:00 UTC | **BUILT+EXERCISED** — 6 `pipeline_runs` rows, all minute-format keys, latest `2026-05-12 19:21` |
| `scripts/verify_urls.py` (522 ln) | `evidence_sources` UPDATE; `url_verification_runs` CREATE-IF-NOT-EXISTS + INSERT OR REPLACE / UPDATE | `.github/workflows/verify-urls.yml`, `0 06 1,15 * *` | **BUILT+EXERCISED — but by exactly one row.** See below. |
| `scripts/verify_resolved_dois.py` (287 ln) | `evidence_sources` UPDATE only | **nowhere** | **BUILT, ORPHANED** |
| `scripts/audit/metadata_integrity_audit.py` | read-only | registered advisory | BUILT+EXERCISED — `VERDICT: PASS`, 0/0 |
| `scripts/audit/code_currency_audit.py` | read-only | **QUARANTINED** | BUILT+EXERCISED — 5 checks, `TOTAL ISSUES: 0` |
| `scripts/validate_verification_consistency.py` | read-only | registered **blocking**, kinds schema+data | BUILT+EXERCISED — `0 stated/provisional cells consistent` |
| `scripts/audit_evidence_metadata.py` | read-only, rule-#10 gate | registered advisory | BUILT; D-0157-aware |
| `scripts/audit/full_db_metadata_verification.py` | read-only, network | **QUARANTINED** ("~298 seconds, network-bound… Correct as a scheduled job, never as a PR gate") | BUILT |
| `scripts/tests/test_url_verifier.py` | — | registered advisory, `tests` battery | BUILT+EXERCISED, **green** — `RESULTS: 25/25 tests passed` |
| `scripts/tests/test_verification_pipeline.py` | — | registered advisory, `tests` battery | **BUILT+EXERCISED, currently RED** — `RESULTS: 15/18 tests passed`, `EXIT=1` |

**Stage 5's own regression test is failing, and will stay failing until the corpus is
repopulated.** The three red checks are live-DB floors the reset removed:

```
$ python3 scripts/tests/test_verification_pipeline.py ; echo "EXIT=$?"
  [✗] G01: Live DB has language populated on ≥50 sources after Phase 4 production run
  [✗] G02: Live DB has ORCID populated on ≥30 authors (was 0)
  [✗] G03: COMPLETE metadata count ≥ 100 (was 67 pre-V1.2)
RESULTS: 15/18 tests passed      EXIT=1
$ python3 scripts/run_checks.py --kinds tooling --battery tests | tail -2
NON-BLOCKING failures (3): test_graph_audit, test_verification_pipeline, test_directness_2_2
RESULT: PASS — 6 check(s) green, 3 advisory failure(s)
```

This is a **vacuous failure** of the same species as R1: nothing is wrong with the code, the
subject is gone. The remedy is the same shape — a warranted, self-lifting suppression carrying
`warrant:` (DR-2026-08-06) and `lift_when_sql: "SELECT COUNT(*) FROM evidence_sources"` with a
`lift_when_ge` matching the floor — not deletion of the assertions and not a bare `min_items`.

**Tables.** `evidence_sources` (the verification columns), `evidence_source_authors` (0),
`pipeline_runs` (6), `url_verification_runs` (5). The latter two are the only evidence in the DB
today that any part of stage 5 has ever run — **and the `url_verification_runs` evidence is one
row, not five**:

```
$ python3 -c "…SELECT run_id, started_at FROM url_verification_runs…"
('url-verify-58f78e57',            '2026-05-13T01:33:33Z')
('cluster-verify-088f6d06',        '2026-05-13T03:53:21Z')
('cluster-verify-din-4c97678d',    '2026-05-13T04:13:15Z')
('cluster-verify-as1428-fad59df9', '2026-05-13T04:16:19Z')
('2026-05-15 08:40',               '2026-05-15 08:40')   ← attempted 0, verified 0
$ grep -n "now_iso = " scripts/verify_urls.py
406: now_iso = time.strftime("%Y-%m-%d %H:%M", time.gmtime())     # → run_id at :424
```

The four `*-verify-<hash>` rows carry ISO-8601 `started_at` and a `run_id` shape the current
script cannot produce; they belong to a `session_2026-05-13a-url-verification` manual pass.
**Exactly one row proves `verify-urls.yml` has ever run**, and that row attempted 0 and verified 0.
`pipeline_runs` is clean by contrast — all six carry the minute-format key `resolve_dois.py`
writes.

#### (b) How they relate to each other — and the migration-system question

**Channel 1 (`resolve_dois.py`, weekly).** Six phases: 0 = PMC-id regex (no network); 1a PMID→DOI
via NCBI; 1b PMCID→DOI; 2a CrossRef structured; 2b CrossRef bibliographic; 3 CrossRef
`type:standard`; 4 CrossRef metadata enrichment. All ten write paths funnel through one function,
`write_verification()` at `scripts/resolve_dois.py:103`, which is exactly why the D-0157 standing
columns could be added "here rather than at the call sites, so a future phase cannot forget" (its
own comment). Five call sites pass `"VERIFIED"`; five pass `status=None, doi_outcome="NO-MATCH"`.

**Channel 2 (`verify_urls.py`, bi-weekly).** Fetch URL → extract `<title>` / `citation_title` /
`og:title` → token-Jaccard against `pub_title`. `TITLE_MATCH_HIGH = 0.50` ⇒ `VERIFIED` + `CLOSED`;
`0.20 ≤ sim < 0.50` ⇒ `UNVERIFIED` + `OPEN` (the file's header records that "D-0157 retired
PROBABILISTIC: a partial title match is not a weaker grade of verified, it is not verified");
404/410 ⇒ Wayback fallback then `UNVERIFIED` + `OPEN` with `url_resolution_outcome='DEAD'`;
403/429/5xx/timeout ⇒ **no write at all**, because a transient block is not evidence of anything.

**Every write target in both jobs, read from source:**

```
resolve_dois.py  :149  UPDATE evidence_sources        (write_verification, ×10 call sites)
                 :552  DELETE FROM evidence_source_authors
                 :558  INSERT INTO evidence_source_authors
                 :590  UPDATE evidence_sources        (metadata enrichment)
                 :643  UPDATE evidence_sources        (pmcid backfill)
                 :681  CREATE TABLE IF NOT EXISTS pipeline_runs
                 :726  INSERT OR REPLACE INTO pipeline_runs      :1013 UPDATE pipeline_runs
verify_urls.py   :260  UPDATE evidence_sources        (write_verification)
                 :377  CREATE TABLE IF NOT EXISTS url_verification_runs
                 :429  INSERT OR REPLACE INTO url_verification_runs   :483 UPDATE
verify_resolved_dois.py  → evidence_sources UPDATE only (:139,:152,:199,:223,:248) — unreachable
```

**The DR-2026-05-28 exemption list is exactly two tables.**
`scripts/audit/migration_reproducibility.py:65`:

```python
EXEMPT_TABLES = ("evidence_source_authors", "pipeline_runs")
```

and `decisions/DR-2026-05-28-migration-ledger-and-reproducibility-reconciliation.md:83`:
*"…are hereby declared **job-owned tables**… These jobs MAY write these two tables directly…
**Any OTHER table written outside migrations remains a violation.** Adding a table to the
job-owned exemption requires a new DR."* CLAUDE.md §4 repeats it.

| Written outside migrations by a scheduled job | On the exemption list? |
|---|---|
| `pipeline_runs` (resolve_dois) | **YES** |
| `evidence_source_authors` (resolve_dois) | **YES** |
| **`url_verification_runs` (verify_urls)** | **NO** |
| **`evidence_sources` — UPDATEs from both jobs** | **NO** |

`url_verification_runs`'s five rows do not currently show as a divergence, and the reason looks
like coverage and is not: **they were laundered into the migration history by the 012 baseline
snapshot**, which is a full SQLite dump. Tested by rebuild, not inferred:

```
$ grep -c 'INSERT INTO "url_verification_runs"' scripts/migrations/012_baseline_2026-05-15.sql
5
$ python3 scripts/migrate_db.py --rebuild <scratch>/rebuild.db
  Applying 42 schema migration(s) / 289 data migration(s) … successfully.
$ …count in the REBUILD…  url_verification_runs 5 · pipeline_runs 6 · evidence_sources 0
```

No other migration touches the table. **The next `verify-urls.yml` run writes a sixth row that
reproduces from nothing.** It will not fail the blocking gate — `url_verification_runs` is not one
of the seven core invariants (`PRAGMA user_version` plus `COUNT(*)` on `evidence_sources`,
`citation_mining`, `source_slug_links`, `gaps`, `connections`, `items`) — but it will surface
under `migration_reproducibility_deep`, which is **advisory** pending the owner decision recorded
in `references/tooling-register.md` §4.2 and in the registry note itself.

**The `evidence_sources` case is worse and simpler: the blocking gate compares `COUNT(*)`, and an
UPDATE changes no count.** Both jobs write only UPDATEs to `evidence_sources`. So the weekly and
bi-weekly jobs can rewrite `verification_status`, `verification_disposition`,
`verification_method`, `doi`, `pmcid`, `metadata_quality` and more on every row in the corpus,
commit the binary blob straight to `main` (`verify-urls.yml:110` `git add data/guidebook.db` →
`:121` `git push origin main`; `resolve-dois.yml:115` / `:131` identically), and the blocking
reproducibility gate stays green. Only the advisory `--deep` comparison sees it — and the registry
note for `migration_reproducibility_deep` already names both findings: "evidence_sources diverges
on 277 rows … because scripts/resolve_dois.py writes Crossref enrichment straight into it, and
url_verification_runs diverges by one row because verify-urls.yml inserts its run record. Both
are written by the same scheduled workflows that DR-2026-05-28 already exempted
evidence_source_authors and pipeline_runs for — they were simply never added." This is CLAUDE.md
§0 rule 4's caveat ("The rule is absolute; the enforcement is not") in its concrete, scheduled,
automated form.

**Internal wiring, by key vs by text.**

- `evidence_source_authors.ref_id → evidence_sources.ref_id` — declared FK; `test_db_integrity`
  **G01** asserts no orphans; `UNIQUE(ref_id, position, role)` prevents duplicate author slots.
- `pipeline_runs` and `url_verification_runs` have **no FK to anything**. They are run ledgers
  keyed on `run_id`. Both are workplan finding N7 ("tables holding data with no provenance
  anchor").
- `url_verification_runs.run_id` is `time.strftime("%Y-%m-%d %H:%M")` written with
  `INSERT OR REPLACE` (`verify_urls.py:406/424/429`). Two runs beginning in the same minute
  silently overwrite each other's ledger row; `pipeline_runs` uses the same minute-granularity
  key. Concurrency groups make same-minute collisions unlikely between *scheduled* runs, not
  between a scheduled run and a `workflow_dispatch`.
- `verification_status` ↔ `evidence_cell_state.has_unverified_sources` is joined **through a JSON
  array**: `validate_verification_consistency.py` parses `evidence_cell_state.governing_refs` and
  looks each entry up in a Python dict of `{ref_id: verification_status}`. The typed edge table
  `cell_source_links` (migration 044) exists and this check does not use it.

#### (c) Relation to the previous stage (Stage 4)

**Entry contract:** a source is verifiable when it holds a locator the tools can act on.

- Channel 1's candidate predicate: `pmid`/`pmcid` present (phases 1a/1b), or an eligible
  `source_type` plus author, title and year (2a/2b), or a standard-number prefix (phase 3); and
  **not** already DOI-bearing; and **not** `doi_resolution_outcome = 'REVERTED'` or a `NO-MATCH`
  inside `SKIP_NO_MATCH_DAYS`.
- Channel 2's candidate predicate, verbatim (`scripts/verify_urls.py:441-450`):
  `url IS NOT NULL AND url != '' AND verification_status IS NULL AND (url_resolution_outcome IS
  NULL OR (url_resolution_outcome='NO-MATCH' AND last_verified_at < cutoff))`.

**What enforces the entry contract: NOTHING ENFORCES THIS as a gate.** Both channels *self-select*
their pool with a `WHERE` clause; a source failing the predicate is silently skipped, never
reported. `research_batch_dod` R10 is the nearest thing to an entry gate, and it runs at stage 4,
is advisory, and is baselined at 1.

**The consequence of Channel 2's `verification_status IS NULL` clause is structural: once a source
has any status, Channel 2 never looks at it again.** A row written `UNVERIFIED` + `OPEN` by a
previous run — which is the `OPEN` disposition's entire meaning, "a return pass is owed" — is
thereby permanently excluded from the only automated mechanism that could perform that return
pass. D-0157 §4.2's invariant **I4** ("`disposition = 'OPEN'` ⟹ the row is in the return queue.
Nothing is parked silently") is stated in the DR, is **not implemented** — the I-series in
`test_db_integrity` is I1, I2, I3, I3b, I4 *(the method rule)* and I4b, with no check for the DR's
I4 — and is **contradicted in code** by this predicate. The `OPEN` return queue does not exist.

#### (d) Relation to the next stage (Stage 6 — citation mining, and 7–9 beyond)

**Exit contract:** a verified source is one a miner may treat as an *anchor* and a synthesis may
treat as a *basis*.

| Handoff requirement | Enforcer | Level |
|---|---|---|
| Standing vocabulary is binary | `test_db_integrity` **B01** — **check only; `verification_status` has no SQL CHECK** (migration 049 declined it deliberately) | 4 blocking |
| `VERIFIED` ⇒ `CLOSED` (no "verified but still owed") | **I1** | 4 blocking |
| `VERIFIED` ⇒ `attempt_count ≥ 1` | **I2** | 4 blocking |
| `CLOSED` + not-`VERIFIED` ⇒ closure reason present | **I3** | 4 blocking |
| `CLOSED` + not-`VERIFIED` ⇒ `attempt_count ≥ 2` | **I3b** | 4 blocking |
| `VERIFIED` ⇒ method obtains the artefact | **I4** (`method NOT IN ('direct-render','co1-attestation','tool')`) — fires only when `verification_method IS NOT NULL` | 4 blocking, conditional |
| `method='tool'` names the tool | **I4b** (`verified_by_tool <> ''`) | 4 blocking |
| Every `VERIFIED` row has an audit trail (locator or tool) | **C01** | 4 blocking |
| Vocabulary of the three new columns | **B07 / B08 / B09** + SQL CHECKs from migration 049 | 4 blocking + **D** (write-time) |
| No published cell rests on a non-`VERIFIED` source | **C10** (`OK_VSTATUS = ("VERIFIED",)`) | 4 blocking |
| `has_unverified_sources` tells the truth | `validate_verification_consistency` | 4 blocking |
| A rule-#10-ineligible source is not cited by a reasoning doc | `reasoning_doc_citations_audit` CHECK 4 (`metadata_quality='AUTHOR-TITLE-ONLY'` OR status NULL/empty OR (`UNVERIFIED` AND `CLOSED`)) | 2 advisory |
| T4–T6 citations use the current in-force edition | `code_currency_audit.py` | **2, QUARANTINED — never selected** |
| A `COMPLETE` row really is complete | `metadata_integrity_audit` (advisory) + `test_db_integrity` C03/C04/G02 (blocking) | mixed |

**The structural elegance here is real and worth naming.** I1–I4b are only *expressible* because
D-0157 split the columns. The DR says so and the code proves it: *"Under the old vocabulary the
claim and its evidence were the same string… Split into peer columns, the corpus reports its own
inconsistency on day one — 43% of it."* Seven blocking invariants now cross-check four columns
against each other. That is the strongest single piece of engineering in stages 4–6.

#### (e) The goal of the stage

Stage 5 exists to make the difference between **"we have a citation"** and **"we have the thing"**
a recorded, queryable, four-dimensional fact, and to keep that fact honest under the pressure that
makes people fudge it. Its object is explicitly *not* to raise a "verified" count; DR-2026-08-04 §5
says the opposite in terms — *"the corpus's 'verified' count drops by at least 71 (~8%)… the
headline number falls because it was overstated. That is the DR working, not failing."* The four
questions are deliberately orthogonal: *is it established* (status), *is more effort owed*
(disposition), *how much was spent* (attempt count), *how was it established* (method) — plus,
when effort has stopped, *why* (closure reason). The design goal is that no single string can ever
again assert a fact another column contradicts, and that the tuple can audit itself.

#### (f) How the tools support that goal — and where they do not

**Support.**

*The four-column split is the fix, and it was validated against data before adoption.* The DR's
§2.1 evidence — `UNVERIFIED-1` claimed one attempt while `verification_attempt_count` said 0 in
**25 of 31** rows — is exactly the measurement that justifies a schema change rather than a style
guide.

*The invariants are implemented and blocking.* I1/I2/I3/I3b/I4/I4b plus B07/B08/B09 all sit in
`test_db_integrity`, the one blocking DB check in the registry: `RESULTS: 70/70 checks passed`.
(Read that number with §1.1's caveat: roughly thirty of the seventy reference tables the reset
emptied, so 70/70 today is substantially a vacuous green.)

*Both writer jobs were updated in the same act*, as the DR demanded. This is unusual and worth
crediting: a vocabulary decision that reaches only the checks and not the writers "has not been
made, only announced" (DR §5.1), and this one reached the writers.

*The 403/429/5xx "no write at all" branch in `verify_urls.py` is correct doctrine in code.* A
transient block is not evidence of anything, so it writes nothing and retries rather than
recording a failure that would later read as a finding.

*`code_currency_audit.py` mechanises tier-system §4* with per-tier freshness thresholds (T4: 7
years; T5/T6: 5) and a 365-day suppression window, and its worked example/counter-example pair
(DIN 18040-1:2010 still in force; NZS 4121:2001 twenty-four years old and still the NZ Acceptable
Solution) shows the author knew age does not predict supersession.

**Where they do not.**

*`VERIFIED` as written by the tools does not meet the doctrine's own definition of `VERIFIED`.*
DR §3: *"VERIFIED — the source document itself was obtained, and the metadata recorded here was
read from it. Not from a citing bibliography, not from a search-result summary, **not from a
publisher's landing page describing it**."* `verify_urls.py:306-311` writes `VERIFIED` on a fetched
landing page's `<title>` at ≥ 0.50 token Jaccard; `resolve_dois.py:760/794/836/881/927` writes
`VERIFIED` on a CrossRef *metadata record* match, having fetched no document. Both are permitted:
§4.3's implication clause reads `VERIFIED ⟹ method ∈ {direct-render, co1-attestation}` **or**
`verified_by_tool IS NOT NULL`, and I4 implements that carve-out faithfully including `'tool'`.
So this is a **doctrine seam, not a code bug** — and the seam is *inside §4.3*, not merely between
§3 and §4.3: §4.3's own method table annotates `direct-render` as *"The document was fetched and
read. The only method compatible with `VERIFIED`"* while listing `tool` in the same table and
permitting it in the implication rule two lines below. The practical consequence is that the
corpus's future `VERIFIED` count will again mix "we read the artefact" with "an API agreed the
artefact exists" — the exact conflation §2.4 of the DR retired `VERIFIED-2` to end. Resolving
which clause governs is an owner call.

*The `OPEN` return queue does not exist* — §(c). DR §4.2's I4 is unimplemented and Channel 2's
predicate actively excludes the rows it names.

*Stage 5's own regression test is red* — `test_verification_pipeline.py`, 15/18, three live-DB
floors the reset removed (§(a)). Advisory, so it changes no verdict; but a reader scanning
`RESULT: PASS` will not see it.

*The two run ledgers are unprovenanced and collision-prone* — no FK to anything, minute-granularity
`run_id` with `INSERT OR REPLACE` (workplan finding N7).

*`url_verification_runs` and the `evidence_sources` UPDATEs sit outside both the migration system
and the exemption list*, and the blocking gate is blind to both — §(b).

*Three of stage 5's audits are quarantined or orphaned.* `code_currency_audit` is quarantined on a
reason the reset has falsified — the registry says "RED. Flags standards lacking a currency
marker; a content backlog, not a gate", and it now reports `TOTAL ISSUES: 0  Audit clean.` across
all five checks. `full_db_metadata_verification` is correctly quarantined for cost (~298s,
network-bound) but has never been added to the verification schedule its own quarantine reason
recommends. `verify_resolved_dois.py` is invoked by nothing: `git grep -ln verify_resolved_dois`
returns six *documentation* files and zero executables — not `governance/check-registry.yaml`
(active or quarantine), not any of the four workflows under `.github/workflows/`, not any `.py` —
while it has been *maintained through the D-0157 migration*, writing `verification_disposition` at
`:201`, `:225`, `:251`. 287 lines, unreachable.

*`metadata_quality` still admits the literal string `"NULL"`* —
`VALID_MQ = ("COMPLETE","AUTHOR-TITLE-ONLY","GREY","PMID-ONLY","NULL","COMPLETE-STATUTORY")`
(`scripts/tests/test_db_integrity.py:149`). A state written as a four-character string in a value
column: precisely the pattern C07 forbids one column over, and the pattern D-0157 §2 diagnoses.

#### (g) How doctrine conditions the stage

**`governance/mission-and-epistemics.md` § Citation discipline** is the *whole* stage here:
*"Source authenticity: confirmed real before citation. 'I don't know' governs over invention"* and
*"Two failed independent searches → CLOSED-DELETED disposition for unverifiable values; do not
accumulate unresolvable UNVERIFIED flags."* The second clause is now `disposition='CLOSED'` +
`closure_reason='not-found-after-search'` + `attempt_count ≥ 2`, and D-0157 §5 records the
correspondence exactly: *"the two failed searches are exactly the `attempt_count ≥ 2` that I3
requires, so the rule that produces this state and the invariant that guards it are the same
statement."*

**Doctrinal commitment 3 (Co-1 co-primary with Tier 1, CRPD Art. 4.3)** forbids defining
`VERIFIED` in a way only documentary sources can satisfy. DR §3.1 is the correction: *"For a Co-1
source the artefact being obtained is the **attestation**… This is not a weaker verification. It is
the same standard applied to a different kind of artefact, which is what co-primacy requires."*
Method `co1-attestation` carries it; migration 049's header records that a literal reading would
have demoted all 41 rows carrying `verified_by_tool='co1-manual-pre-pipeline'`; and
`test_db_integrity` C04 carves out `co1%` explicitly.

**`governance/tier-system.md` §4** makes code-currency part of citation for T4–T6 rather than a
courtesy: *"the citation must additionally confirm that the cited edition is the current
legally-in-force edition."* It names its own enforcement level — *"Enforcement (Level 2 audit
script, added 2026-05-25)"* — which is what it is, and less, since that script is quarantined.

**`governance/evidence-architecture.md` §5** conditions the exit: a determination's basis must be
established evidence, which is why C10 narrows to `OK_VSTATUS = ("VERIFIED",)`.

**What doctrine FORBIDS at this stage:**

- **Grades of verified.** D-0157 §4.1: *"Verification is finished or it did not happen; there is no
  'verified but still owed'."* Enforced by I1 and by the binary `VerificationStatus` enum.
- **Asserting closure without earning it.** §4.1/§4.2 I3: *"'Can't be verified after effort spent'
  — closure has to be earned and reasoned, not asserted."* Enforced by I3 + I3b.
- **Parking a row silently.** §4.2 I4. **Unenforced, and contradicted by Channel 2's predicate.**
- **Loading verification closure into `processing_blocked_reason`.** §4.2: *"a DR that diagnosed
  the disease and then reproduced it would deserve to be rejected."* Enforced by two separate CHECK
  vocabularies (migration 040 vs 049).
- **Citing an edition without checking currency** (tier-system §4). Enforcer quarantined.
- **A synthesis claim on an `AUTHOR-TITLE-ONLY` or status-NULL source** (PI rule #10,
  `DR-2026-05-13`, `DR-2026-05-20`) — the `evidence-verification-gate` criterion in
  `governance/pipeline-contract.yaml` stage `collection`, whose named enforcer is
  `scripts/audit/metadata_integrity_audit.py`.

**DRs:** `DR-2026-08-04-verification-status-is-a-standing-not-a-history.md` (governing);
`DR-2026-05-28-migration-ledger-and-reproducibility-reconciliation.md` (the exemption list);
`DR-2026-05-19` (manual-track explicit-cause states, the Co-1 manual channel); `DR-2026-05-20`
(`metadata_integrity_status`); `DR-2026-05-13` (rule #10 / locator ladder); `DR-2026-07-20`
(coined `DISPUTED`, retired by D-0157 into the closure reason `disputed-existence`);
`DR-2026-05-18` (`COMPLETE-STATUTORY`).

#### (h) ACCEPTANCE CONDITIONS

Level ceiling is 4 (no pre-commit hook exists in this repo). Level **D** is used as defined in
§2.4(h) — the repo's 5-level spectrum has no rung for DDL constraints, so `CHECK` / `UNIQUE` /
`NOT NULL` are recorded as **`D — enforced at write time by SQLite`** and `FOREIGN KEY` as
**`D(fk) — deferred differential check in migrate_db.py`** (FKs are `OFF` during every migration
script at `:164` / `:251`; new violations raise `sqlite3.IntegrityError`, a pre-existing ~18-row
baseline is grandfathered, `BOOTSTRAP` migrations are downgraded to a warning, and CI reach is
indirect via the blocking `migration_reproducibility` rebuild).

**This stage is where the distinction bites hardest**, because D-0157 deliberately did *not* take
the D route for the column that matters most — see condition 1.

1. **`verification_status ∈ {VERIFIED, UNVERIFIED}`.** Column `verification_status`.
   *Level: 4 blocking — **no D***. Migration 049 explicitly declined to add a `CHECK` (it would
   require a 94-column table rebuild, and 039's header warns that hand-copying such a definition
   "is how a rebuild silently changes a type, default, or CHECK") and designated `test_db_integrity`
   **B01** the enforcer instead. The write does not fail; the check does. This is a deliberate,
   reasoned trade of D for 4 — and worth flagging precisely because §(a)'s vocabulary table reads
   as though all six columns were constrained alike, and they are not.
2. **`VERIFIED` ⇒ `verification_disposition = 'CLOSED'`.** Both columns. *Level: 4 blocking* — **I1**.
3. **`VERIFIED` ⇒ `verification_attempt_count ≥ 1`.** *Level: 4 blocking* — **I2**.
4. **`VERIFIED` ⇒ method ∈ {direct-render, co1-attestation, tool}.** Column
   `verification_method`. *Level: 4 blocking, **conditional*** — the check carries
   `AND verification_method IS NOT NULL`, so a `VERIFIED` row with a NULL method passes. Enforcer:
   **I4**.
5. **`method='tool'` ⇒ `verified_by_tool` non-empty.** *Level: 4 blocking* — **I4b**.
6. **`VERIFIED` ⇒ some audit trail (doi / url / pmid / verified_by_tool).** *Level: 4 blocking* —
   **C01**.
7. **`CLOSED` + not-`VERIFIED` ⇒ `verification_closure_reason` set.** *Level: 4 blocking* — **I3**.
8. **`CLOSED` + not-`VERIFIED` ⇒ `attempt_count ≥ 2`.** *Level: 4 blocking* — **I3b**.
9. **`OPEN` ⇒ the row is in a return queue.** *Level: **UNENFORCED, and contradicted in code***
   — DR §4.2 I4 has no implementation, and `verify_urls.py:444` (`AND verification_status IS NULL`)
   excludes every row the tool itself wrote `OPEN`.
10. **Disposition / method / closure-reason vocabularies.** Those three columns.
    *Level: **D — enforced at write time by SQLite** + 4 blocking* — SQL `CHECK`s added by
    migration 049 (the three *new* columns did get them); `test_db_integrity` **B07 / B08 / B09**
    exist on top because "a pre-049 database or a hand-edited blob would not" carry them (the
    check's own comment).
11. **`doi_resolution_outcome ∈ {RESOLVED, NO-MATCH, REVERTED}`.** *Level: 4 blocking* — **B03**.
12. **`url_resolution_outcome` within the union of the two parallel vocabularies.**
    *Level: 4 blocking* — **B04**, which accepts eleven values and whose own comment records that
    the two sets "are NOT equivalent" and are accepted in parallel rather than merged.
13. **`metadata_quality` vocabulary.** *Level: 4 blocking — **no D***; `metadata_quality` is bare
    `TEXT` in the live DDL. Enforcer **B02**, whose `VALID_MQ` tuple admits the literal string
    `"NULL"` — a state written as a value, the pattern C07 forbids one column over.
14. **`COMPLETE` ⇒ has an author, or `is_corporate_primary`.** Columns `first_author_last` /
    `is_corporate_primary`. *Level: 4 blocking* — **C03**.
15. **`COMPLETE` ⇒ has a DOI, or is co1-verified, or has `NO-MATCH` on record.** Columns `doi`,
    `verified_by_tool LIKE 'co1%'`, `doi_resolution_outcome`. *Level: 4 blocking* — **C04**.
16. **`COMPLETE` and person-authored ⇒ ≥ 1 `evidence_source_authors` row.** *Level: 4 blocking* —
    **G02**. Adjacent guarantees on that table: `UNIQUE(ref_id, position, role)` is **D**, and
    `evidence_source_authors.ref_id → evidence_sources.ref_id` is **D(fk)** backed by the blocking
    **G01** orphan scan.
17. **No `COMPLETE` row carries an open metadata-integrity flag.** Column
    `metadata_integrity_status`. *Level: 2 advisory* — `scripts/audit/metadata_integrity_audit.py`.
18. **No placeholder prose in a value column.** Columns `first_author_last`, `author_display`,
    `publisher`, `evidence_source_authors.corporate_name`. *Level: 4 blocking* — **C07**
    (`LIKE '[%'`, `'%pending%'`, `'%TBD%'`, `'%TBC%'`, `'%unknown (%'`).
19. **A cited T4–T6 source is the current in-force edition, or currency-verified within 365 days.**
    Columns `code_currency_status`, `code_currency_verified_at`. *Level: 2 audit script,
    **QUARANTINED — never selected**, so effectively **UNENFORCED*** — `code_currency_audit.py`,
    which now reports zero issues, i.e. its quarantine reason is stale.
20. **A published cell's `has_unverified_sources` flag matches its refs' actual statuses.**
    `evidence_cell_state.has_unverified_sources` vs `evidence_sources.verification_status`.
    *Level: 4 blocking* — `validate_verification_consistency.py`.
21. **No published cell rests on a non-`VERIFIED` source.** `governing_refs` × `verification_status`.
    *Level: 4 blocking* — **C10**.
22. **The verification write reproduces from migration history.**
    *Level: **NOT ENFORCED for these columns*** — `evidence_sources` UPDATEs change no `COUNT(*)`,
    and `url_verification_runs` is neither a core invariant nor on the DR-2026-05-28 exemption
    list. The blocking `migration_reproducibility` is blind to both; the advisory `--deep`
    comparison sees them and names them.
23. **The run left a ledger row.** `pipeline_runs` / `url_verification_runs`.
    *Level: 4 blocking, weakly* — `test_db_integrity` **F01–F04** assert no DOI/VERIFIED count
    regressions and that `completed_at` is set; **E02/E03** assert the tables and their Phase-4
    columns exist. Nothing asserts the ledger row is attributable, and nothing prevents a
    same-minute `INSERT OR REPLACE` from erasing one.

---

### 2.6 Stage 6 — Citation mining

anchor-driven (`citation_mining`) and gap-driven (`gap_mining`) discovery

#### (a) Tools, tables, methodology

**Tables.**

| Object | State | Notes |
|---|---|---|
| `citation_mining` (0 rows) | BUILT+UNEXERCISED | `PRIMARY KEY (slug, local_ref_id)`; `global_ref_id` **nullable** FK → `evidence_sources.ref_id`; `backward`/`forward` `CHECK IN (0,1)`; `connections_produced TEXT NOT NULL DEFAULT '[]'`; `deferred_reason` nullable free text |
| `gap_mining` (0 rows) | BUILT+UNEXERCISED | `gap_mining_id` PK; FK → `gaps.gap_id`; 5-value `outcome` CHECK; 6-value `check_method` CHECK; **three table-level integrity CHECKs** |
| `gaps` (0 rows) | BUILT+UNEXERCISED | `mining_addressability ∈ {ADDRESSABLE, NOT-ADDRESSABLE, TRIAGE-NEEDED}` |
| `evidence_sources.citation_mining_status` | BUILT+UNEXERCISED | `NOT NULL DEFAULT 'pending' CHECK IN ('pending','mined','deferred','not-applicable')` |
| `evidence_sources.processing_blocked_reason` | BUILT+UNEXERCISED | 9-value CHECK |
| `connections` / `connection_targets` (0 / 0) | BUILT+UNEXERCISED | mining's output, referenced by `connections_produced` |
| `citation_population_links` (0) | BUILT+UNEXERCISED | FK → `reasoning_doc_citations`, **not** to `citation_mining` — a different object despite the name |

**Scripts and skills.**

| Path | Role | State |
|---|---|---|
| `scripts/audit/citation_mining_completeness.py` (320 ln) | the R2 completeness gate | BUILT+EXERCISED; three registrations |
| `scripts/audit/gap_mining_audit.py` (282 ln) | 7 checks over `gap_mining` | BUILT+EXERCISED — `PASS` on 0 rows |
| `scripts/probes/citation_mining_pipeline.py` (254 ln) | Crossref reference-pool prospector; "No DB writes. Pure search/analysis." | **BUILT, UNREGISTERED, UNEXERCISED** — network-bound, invoked by nothing; hardcodes `DB_PATH` rather than honouring `GUIDEBOOK_DB_PATH` (legal — `scripts/probes/**` is out of scope for `db_path_env_audit.py`) |
| `scripts/db.py is-mined / log-mining / unmined / update-bpc` | the anchor-driven CLI the skill calls | BUILT+UNEXERCISED |
| `scripts/db.py add-gap-mining / update-gap-addressability / unmined-gaps` | the gap-driven CLI | BUILT+UNEXERCISED |
| `skills/citation-miner_SKILL.md` (254 ln) | anchor-driven discovery protocol | BUILT (prose + CLI recipes) |
| `skills/gap-driven-mining_SKILL.md` (345 ln) | gap-driven discovery protocol | BUILT |
| `sessions/LATEST-RESEARCH` | names the blocking gate's subject | BUILT+EXERCISED — currently `session_2026-07-26-energy-conservation-rest-points-seating-b3.md`, and that file does exist in `sessions/` |

**Registered checks.**

| id | level | invocation | verdict today |
|---|---|---|---|
| `citation_mining_session` | **blocking** | `citation_mining_completeness.py --session @SESSION@ --tier-max 2`, `requires_session: true`, `session_pointer: LATEST-RESEARCH` | **PASS — `NOTHING-IN-SCOPE`** |
| `citation_mining_backlog_t2` | informational | `--tier-max 2` | PASS |
| `citation_mining_backlog_t3` | informational | `--tier-max 3` | PASS |
| `gap_mining_audit` | advisory | `gap_mining_audit.py` | PASS |
| `test_db_integrity` A07 / C08 / C09 | **blocking** | — | PASS |
| `research_dod` **R2** | advisory | — | PASS (`0 citation_mining rows for 0 anchors`) |

**The `.md`-vs-bare-stem join bug is genuinely fixed.** `citation_mining_completeness.py:64-81`
and `:148-151` add a normaliser and a two-value `IN` predicate:

```python
def session_keys(session):
    stem = session[:-3] if session.endswith(".md") else session
    return stem, stem + ".md"
...
skey, skey_md = session_keys(session) if session else (None, None)
where_session = ("AND es.created_by_session IN (:session, :session_md)" if session else "")
```

The same normalisation is applied in three further places — the session-resolvability probe
(`:133-135`), the `examined` denominator (`:186-192`), and the stub-row Python filter (`:220`) —
and `test_db_integrity` **L04** independently applies the same `(stem, stem+'.md')` pair. The
docstring is candid about why the earlier pointer split was insufficient alone: *"the split is
correct and necessary, but on its own it moved the gate from one name that matched nothing to
another name that matched nothing. Normalising here is what actually puts rows in scope."*

**One adjacent fix landed with it and one did not.** The `NOTHING-IN-SCOPE` verdict and the
`Examined` count are present, so a pass on merits and a pass for want of subjects no longer render
identically. The `global_ref_id`-only join was fixed **in the outstanding query only**
(`:166-171`: `LEFT JOIN citation_mining cm ON cm.global_ref_id = es.ref_id` **and**
`LEFT JOIN citation_mining cm2 ON cm2.slug = ssl.slug AND cm2.local_ref_id = ssl.local_ref_id`,
with `WHERE cm.global_ref_id IS NULL AND cm2.slug IS NULL`; without the second join the gate
produced "48 false positives at session close"). **The stub-row scan was not fixed**
(`:207-217`):

```sql
FROM citation_mining cm
JOIN evidence_sources es ON cm.global_ref_id = es.ref_id     -- INNER, global_ref_id only
WHERE es.tier BETWEEN 1 AND ?
  AND cm.backward = 0 AND cm.forward = 0
  AND (cm.deferred_reason IS NULL OR cm.deferred_reason = '')
```

By the same file's own comment eleven lines earlier, `global_ref_id` "is NULL on 146 of 183 rows".
**A stub mining row with a NULL `global_ref_id` — the majority shape — is invisible to the
blocking gate's stub scan.** The repo-wide coverage statistic (`total_with_cm`, `:227-233`) has the
identical single-join flaw, so reported coverage understates. There is also dead code immediately
above (`:194-205`): a first `bad_cm` query terminated by `… ).fetchall() if False else []` and
containing a `.replace("es.", "cm.created_by_session = :session OR es.")` string mangle on an
f-string SQL fragment — harmless, and visibly the abandoned draft of the fix. **This vacuity
survives the corpus being repopulated**, unlike the emptiness one below, which resolves itself the
moment research resumes.

**And the gate is vacuous today for a second, independent reason.** It is BLOCKING and it examined
nothing:

```
$ python3 scripts/audit/citation_mining_completeness.py \
    --session "$(cat sessions/LATEST-RESEARCH)" --tier-max 2 ; echo "EXIT=$?"
  Examined (slug-linked T1-2 sources in scope): 0
  VERDICT: NOTHING-IN-SCOPE
EXIT=0
$ python3 scripts/run_checks.py --kinds data --battery data | grep citation_mining_session
[PASS] citation_mining_session                   0.0s
```

Two holes, and they compound. **(i)** The registry entry declares no `min_items`; only five of the
sixty-four checks do (`check_utf8_md` 1000, `check_json` 50, `check_yaml` 20, `validate_schema` 1,
`research_contract_sync` 10), and `run_checks.vacuity_failure()` returns `None` immediately when
the key is absent (`scripts/run_checks.py:290-292`). **(ii)** Even with `min_items` the output
could not satisfy the contract: `EXAMINED_RE = re.compile(r"^\s*EXAMINED:\s*(\d+)\b", re.MULTILINE)`
requires the literal upper-case token immediately followed by a colon, while the script prints
`Examined (slug-linked T1-2 sources in scope): 0` — lower-case, with a parenthetical between the
word and the colon. Two independent reasons it cannot match; verified by running the regex against
the script's real output, which returns `None`.

**The remedy is not "add `min_items`", and this is decided.** The repo adjudicated exactly this
question on 2026-08-06 and ruled against it. `source_slug_links_duplicates` is a *blocking* check
that today prints `EXAMINED: 0 source_slug_links row(s)` and passes; its registry note records the
ruling verbatim:

> "`min_items: 1` was declared alongside it and **RETIRED the same day by the clean-room reset**,
> which emptied `source_slug_links` by decision. The guard exists to catch a check passing on an
> ACCIDENTALLY empty subject; **an empty subject that is the declared state of the project is not
> that**, and leaving the guard would have made a blocking gate red for telling the truth."

A blanket floor here would redden `main` for every data/synthesis diff for a reason no diff can
fix — the identical objection that applies to promoting `research_dod` (§2.4(f)). **The correct
two-part remedy is:** (1) make the script print `EXAMINED: <n>` in the token form the dispatcher
recognises — that edit stands on its own merits and is required by any later floor; and (2) rather
than a bare `min_items`, declare a **warranted, self-lifting suppression** in the shape
`scripts/audit/graph/known_debt.yaml` already proves and `graph_audit.py` already evaluates —
`warrant:` citing `DR-2026-08-06-clean-room-evidence-reset.md`,
`lift_when_sql: "SELECT COUNT(*) FROM evidence_sources WHERE tier BETWEEN 1 AND 2"`,
`lift_when_ge: 1` — so the floor returns mechanically when the subject refills, and the
suppression itself is reported STALE rather than silently hiding a regression. An entry with no
warrant is refused outright (`known_debt.unsound`), and an unverifiable warrant is refused rather
than applied, so a broken warrant cannot suppress forever.

#### (b) How they relate to each other

```
evidence_sources(ref_id, tier, citation_mining_status)
      │  JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id            [KEY, INNER]
      ▼
source_slug_links(ref_id, slug, local_ref_id)
      │  cm2.slug = ssl.slug AND cm2.local_ref_id = ssl.local_ref_id     [composite TEXT, no FK]
      ▼
citation_mining(slug, local_ref_id) ──global_ref_id (nullable FK)──► evidence_sources
      │
      └── connections_produced TEXT '[]' ─────────────────────────────► connections [JSON, no FK]

gaps(gap_id, mining_addressability) ──FK──► gap_mining(gap_id, outcome, check_method,
                                              discoveries_logged '[]', candidate_dois '[]')
                                                  └── JSON, no FK ─────► evidence_sources
```

**Joins by key.** `citation_mining.global_ref_id → evidence_sources.ref_id` (declared FK;
`test_db_integrity` **A07** asserts `citation_mining global_ref_id → source_slug_links` has no
orphans); `citation_mining.slug → slugs.slug`; `gap_mining.gap_id → gaps.gap_id`.

**Joins by text or JSON — three, all load-bearing.**

1. **`citation_mining.(slug, local_ref_id)` ↔ `source_slug_links.(slug, local_ref_id)`** is a
   composite match on a free-TEXT column with no foreign key, and it is the *primary* resolution
   path rather than a fallback: migration 051's header measured `global_ref_id` NULL on 146 of 183
   rows. `source_slug_links_duplicates` (blocking) exists specifically because a duplicated
   `(slug, local_ref_id)` would make this join ambiguous.
2. **`citation_mining.connections_produced`** is the sharpest single finding in the stage.
   Migration 051's header records the measurement verbatim: *"25 rows carry a non-empty value;
   **13 of those hold a BARE INTEGER** (`1`, `0`, `5`) — a COUNT, in a column whose other rows hold
   a LIST. Of the 81 array entries: 15 are global `REF-#####` ids, 50 are slug-scoped
   `local_ref_id` values… and **3 resolve to nothing**. Three vocabularies and two cardinalities in
   one column."* 051 deliberately declined to normalise — *"an edge object over a column whose
   vocabulary is undecided would harden the ambiguity into a schema"* — and those rows are gone
   with the reset, but **the column and its undecided vocabulary remain**: `TEXT NOT NULL DEFAULT
   '[]'`, with **no `json_valid()` CHECK**. `test_db_integrity` H06/H07 police edge JSON columns
   for array-ness and duplicate ids, but their scope is
   `EDGE_JSON = (("evidence_cell_state","governing_refs"), ("search_executions","admitted_ref_ids"))`
   — **not** `connections_produced`. The next mining pass can reintroduce all three vocabularies
   with nothing to stop it.
3. **`gap_mining.discoveries_logged` and `.candidate_dois`** are JSON arrays of `ref_id` / DOI with
   no FK. `gap_mining_audit.py` chases them in Python — CHECK 6 (`discoveries_logged` ids not in
   `evidence_sources`), CHECK 7 (`candidate_dois` already verified and INSERTed).

**The source-grain status columns (migration 040).** `citation_mining_status` and
`data_capture_status` live on `evidence_sources` rather than in `citation_mining` for a stated
reason: *"citation_mining's primary key is (slug, local_ref_id) and a source appears under up to 7
slugs, so a per-source state does not fit its grain — one backlog row per source would mean picking
an arbitrary slug or writing up to 7 rows."* The biconditional binding them is `test_db_integrity`
**C08**, whose comment records the cost of its earlier absence: *"the original backfill joined on
global_ref_id alone — NULL in 146 of 183 rows — and left 80 sources reading 'pending' while holding
a non-deferred mining row… A status column without a biconditional is an assertion nobody checks."*
**C09** covers the states nobody could otherwise contradict: `deferred` / `none-extractable` ⇒ a
coded `processing_blocked_reason`; a reason attached to a non-stopped state; and
`citation_mining_status='deferred'` with no deferred mining row.

#### (c) Relation to the previous stage (Stage 5 — verification)

**Entry contract:** mining is owed on a **confirmed Tier 1–2 anchor**. Both halves matter, and only
one is enforced.

*Tier scope* is enforced. `governance/research-contract.yaml` R2's `resolution` records the
2026-08-01 correction: *"(a) SCOPE: the hook said 'T1-T3'. The operative RULE says 'every confirmed
Tier 1-2 source'. T1-T2 governs; the hook had been obliging work on a tier band the rule ledger
does not require, which is a real cost silently imposed on every session."* The blocking
registration pins `--tier-max 2`.

*Confirmed* is **NOT** enforced. `citation_mining_completeness.py`'s outstanding query filters only
on `es.tier BETWEEN 1 AND :tier_max`; `es.verification_status` appears in the SELECT list, for
display in the `STATUS` column of the outstanding table, and **never in a predicate**. An
`UNVERIFIED` + `OPEN` Tier-1 source is demanded of the miner exactly as a `VERIFIED` one is, which
inverts the pipeline order — stage 6 is supposed to consume stage 5's output. **NOTHING ENFORCES
THIS.**

And the CLI a miner would actually run is wider than the rule requires:
`get_unmined_for_all_slugs(tier_max: int = 3)` (`scripts/db.py:1690`), invoked in
`citation-miner_SKILL.md:74,76` as `db.py unmined --tier-max 3`. That is the exact over-obligation
`DR-2026-08-01-research-contract-single-source.md` corrected in the SessionStart hook and did not
sweep into the CLI or the skill.

#### (d) Relation to the next stage (Stage 7 — value extraction)

**Exit contract:** every T1–T2 source is either mined in both directions, or carries a
`deferred_reason`; its `citation_mining_status` agrees with the mining register; and discovered
sources are inserted and handed off rather than recursed into.

| Handoff requirement | Enforcer | Level |
|---|---|---|
| Every slug-linked T1–T2 source has a `citation_mining` row | `citation_mining_completeness.py` outstanding query | 4 blocking, session-scoped — **vacuous today** (§(a)) |
| No stub row (`backward=0 AND forward=0 AND deferred_reason` empty) | same script, `bad_cm` scan | **4 blocking, but only for rows carrying a non-NULL `global_ref_id`** |
| `citation_mining_status='mined'` ⟺ a non-deferred mining row resolves to it | `test_db_integrity` **C08** (biconditional) | 4 blocking |
| `citation_mining_status='deferred'` ⇒ a mining row with a non-empty `deferred_reason` | **C09** | 4 blocking |
| `deferred` / `none-extractable` ⇒ coded `processing_blocked_reason` | **C09** | 4 blocking |
| `citation_mining.global_ref_id` resolves when set | **A07** | 4 blocking |
| Mining is proportionate, ≥ anchors/4 | `research_batch_dod` **R2** (`R2_MINING_PER_ANCHORS = 4`) | 2 advisory |
| Depth-1 per pass: discoveries are inserted, not recursed | skills prose only | **1 (text rule). NOTHING ENFORCES THIS.** |
| A discovered source passes R10 before admission | R10, at stage 4 | 2 advisory |
| `gap_mining` closure carries a discovery | table-level SQL CHECK | **D** — write-time |
| `gap_mining` recategorisation / deferral carries ≥ 20 / ≥ 10 chars of reason | table-level SQL CHECK | **D** — write-time |
| A mining-addressable gap is not closed without a `gap_mining` row | `gap_mining_audit.py` CHECK 1 ("backdoor closures") | 2 advisory |
| Closure outcomes carry the rule-#7 falsifiable fields | `gap_mining_audit.py` CHECK 2 | 2 advisory |
| Numerical-spec closures have a PMP walk | `gap_mining_audit.py` CHECK 3 | 2 advisory |
| `LATEST-RESEARCH` actually gives the blocking gate a subject | `test_db_integrity` **L04** | **4 blocking — currently satisfiable by emptiness** |

**L04 is satisfiable by the very condition it was written to detect.** Traced at
`scripts/tests/test_db_integrity.py:1083-1115`: `_in_scope` is
`SELECT DISTINCT es.created_by_session FROM evidence_sources es JOIN source_slug_links ssl …` over
two empty tables → `[]` → `_pairs = []` → `_newest = None` → `_drifted = False`. The pass condition
is `not (_drifted and _own == 0)` = `not (False and True)` = **True**, while `_own` is 0 — i.e.
while the state L04's own failure message describes ("With 0 subjects that BLOCKING gate examines
nothing and passes") is exactly what is happening.

```
$ python3 scripts/tests/test_db_integrity.py | grep L04
  [✓] L04: sessions/LATEST-RESEARCH gives citation_mining_session a subject
```

L04 is correct in intent and correct for the drift case it names; it has no guard for the case
where *nothing* is in scope. Its own comment already frames the live question — *"Advance the
pointer (and expect it to go red on a real backlog), or demote the gate to advisory until it has
work."*

#### (e) The goal of the stage

Citation mining is the project's **second discovery channel**, and its purpose is to make the
evidence base's shape a function of the literature rather than of whatever a search engine returned
that day. Backward mining reads a confirmed anchor's own reference list; forward mining finds the
works that cite it. Together they traverse the citation graph the search stage cannot see.
`governance/pipeline-operations.md` fixes its boundaries with unusual precision: it is *discovery*
(it produces sources, not values and not statements); it is *anchor-driven* (as against gap-driven
mining, which starts from a `gaps` row); and it **reads a source's bibliography, not its content** —
*"A source can be fully mined and hold no captured value, or hold captured values and never have
been mined. They are independent axes, which is why migration 040 gave `evidence_sources` two
separate status columns rather than one 'processed' flag."* The stage's deeper purpose is
anti-parochial: it is the mechanism by which the corpus can discover that it has been reading only
one literature.

#### (f) How the tools support that goal — and where they do not

**Support.**

*The completeness gate is the most-repaired check in the repo, and every repair is documented in
situ with the count of what it was getting wrong.* Four distinct defects were closed in it: the
`.md` join (matched nothing, for every session, under either pointer), the `global_ref_id` join in
the outstanding query (48 false positives), the unresolvable-session pass
(`--session no-such-session-xyz.md` printed compliance), and the missing `Examined` denominator.
That is a check that has been adversarially maintained.

*The three-way outcome vocabulary — `OUTSTANDING` / `CLEAN` / `NOTHING-IN-SCOPE` — is the right fix
for the class of bug this repo keeps producing.* CLAUDE.md §10 records the class: "this repo has
now produced that failure mode four separate times, and it looks exactly like success in CI."

*`gap_mining`'s integrity CHECKs live in the schema, not in a script.* `closure_evidence_found` ⇒
non-empty `discoveries_logged`; `gap_recategorized` ⇒ `notes` ≥ 20 chars; `deferred` ⇒ `notes` ≥ 10
chars. A write that lies about a closure fails at the database — the strongest available
enforcement short of not being able to express it.

*The skills' connector doctrine is empirically grounded and correctly negative.*
`citation-miner_SKILL.md` §0 rules out Scholar Gateway for forward mining on measured grounds
("confirmed empirically 2026-07-20 — spot-checked results were topically similar but did not
verifiably cite the anchor") and rules out PubMed `find_related_articles` as a substitute
("word-weighted similarity, not actual citers"), naming Semantic Scholar's citations endpoint as
the genuine citation-graph source. It also establishes that a partial state (`backward=1,
forward=0`, `deferred_reason` set) is **valid**, while `backward=0 AND forward=0` with no reason is
a protocol violation — and the gate implements exactly that distinction, for the rows it can see.

*Migration 040's status columns each ship with a biconditional* (C06 for capture, C08 for mining) —
the rule `governance/pipeline-operations.md` §4 states as "Any future status column ships with its
check or it does not ship."

**Where they do not.**

*The blocking gate has two independent vacuities.* One is emptiness-driven and self-resolving
(§(a) — `NOTHING-IN-SCOPE`, no `min_items`, and an `EXAMINED` line the dispatcher's regex cannot
read). The other is **durable**: the stub-row scan and the coverage statistic still join on
`global_ref_id` alone, so the majority row shape (NULL `global_ref_id`, per the file's own
measurement of 146 of 183) is invisible to the blocking half of the gate *even after the corpus is
repopulated*. That is the more serious of the two.

*A source with no `source_slug_links` row is exempt from the gate entirely.* Both the outstanding
query (`:156-157`) and the `examined` denominator (`:188-189`) open with
`JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id` — an INNER join. Admit a Tier-1 source, omit
its slug link, and the blocking gate does not see it — and `examined` does not count it either, so
the escape does not even surface as a shrunken denominator.
`workplan/2026-08-02-architecture-decision-and-execution-plan.md` W2 lists this defect and marks it
"closed by W6.1"; the same document's status table lists W6 as **open**. It is recorded-as-closed
and open. *[UNCERTAIN: whether the INNER join is intentional scoping. A source with no topic link
arguably has no slug under which to be mined, since `citation_mining`'s PK is `(slug, local_ref_id)`.
If so the honest fix is a separate orphan check — `source_orphan_audit`, already proposed in W6 —
rather than an outer join here.]*

*Depth-1 is prose only.* Both skills state it emphatically ("Depth-1 enforced (both modes)") and
nothing in the schema, the CLI, or any check can distinguish a depth-1 pass from a depth-3 one.

*The skills instruct writes that CLAUDE.md forbids.* `citation-miner_SKILL.md` §1 (INLINE step 5,
BATCH steps 1 and 3) and `skills/gap-driven-mining_SKILL.md` §1 both instruct
`python3 scripts/db.py log-mining …`, `db.py unmined`, `db.py update-bpc`, `db.py add-gap-mining`.
`scripts/db.py:58` opens `sqlite3.connect(str(DB_PATH))` — read-write, on `data/guidebook.db` — and
commits at `:66`. CLAUDE.md §0 rule 4: *"Never write `data/guidebook.db` directly… Direct writes
(including ad-hoc `scripts/db.py` writes to the committed DB) break the reproducibility gate."*
Neither skill mentions `emit_data_migration.py`. `governance/pipeline-operations.md` §4 flags the
unresolved question ("⚑8… three possible homes and no fourth"), but the skills currently document
the forbidden home as the procedure.

*`connections_produced` remains a three-vocabulary, two-cardinality column with no check* (§(b)).

*`citation_mining_pipeline.py` is a probe wired to nothing*, and its Crossref-pool approach
(backward mining by reference-list harvesting) duplicates the skill's manual protocol without being
reconciled to it.

*R2's floor is `anchors // 4`.* The enforcer's docstring is honest about this ("Deliberately
weak-ish: it is a floor against doing NOTHING, not a definition of systematic mining"), but it means
a batch admitting 40 anchors satisfies R2 with 10 mining rows — and the *completeness* gate that
would demand the other 30 is session-scoped and currently vacuous.

#### (g) How doctrine conditions the stage

**Research contract R2**, canonical text (`governance/research-contract.yaml`):

> *title:* "Citation mining on admitted anchors, backward AND forward"
> *hook:* "Mine every CONFIRMED T1-T2 anchor backward AND forward. Depth 2-3 via citation-miner;
> gap-driven mode is depth-1 per pass and hands off."
> *anchor:* "`references/project-standards.md` RULE (2026-04) 'Forward + backward citation mining
> mandatory for every confirmed Tier 1-2 source'"

Its `resolution` block resolves what reads as a contradiction and is not: *"'depth 2-3' and
gap-driven-mining's 'Depth-1 enforced (both modes)' are NOT in conflict… Depth 2-3 is the traversal
target for citation-miner. Depth-1 is a per-PASS bound in gap-driven mode."* Both are stated in the
canonical file so the apparent contradiction cannot be rediscovered as a defect.

**Doctrinal commitment 3 (Co-1 co-primary with Tier 1, CRPD Art. 4.3)** conditions *which* graph is
worth traversing. `gap-driven-mining_SKILL.md` §0 forbids the obvious substitution: *"Do NOT
substitute PubMed for Scholar Gateway on Co-1: they index different corpora, and PubMed will miss
the lived-experience / DPO publications that are exactly what Co-1 gaps require."*

**`governance/mission-and-epistemics.md` § Citation discipline** — *"Source authenticity: confirmed
real before citation"* — is what makes a discovered reference a *candidate*, never an admission.
`gap_mining` implements this at the schema: `candidate_dois` exists so that "candidates returned
but not yet verified are recorded as DOIs only, **NOT INSERTed to evidence_sources**" (DDL comment).

**`governance/pipeline-operations.md`** supplies the naming rule: *"**No column, check, or skill may
use 'mining' unqualified.** Name the operation."* Migration 040 obeys it (`citation_mining_status`,
not `mining_status`) and says so.

**What doctrine FORBIDS at this stage:**

- **Mining as a topic search.** `citation-miner_SKILL.md` §0: PubMed `find_related_articles` "is not
  a forward-mining substitute" — doing so is "the topic-evidence vs claim-evidence anti-pattern PI
  standing rule #7 fights".
- **Web-search-only verification of a mined reference.** "If [PubMed is] unavailable, ABORT the
  mining pass… Do NOT proceed with web-search-only verification (high fabrication risk per GAP-278)."
- **A stub mining row.** `backward=0 AND forward=0` with no `deferred_reason` is "a PROTOCOL
  VIOLATION (see GAP-283)" — enforced by the gate's `bad_cm` scan, for rows with a non-NULL
  `global_ref_id`.
- **Recursing into discovered sources in the same pass** (depth-1 per pass). Unenforced.
- **Closing a mining-addressable gap without a `gap_mining` row** — `gap_mining_audit.py` CHECK 1
  ("backdoor closures"); `DR-2026-05-26-gap-driven-mining-protocol.md`.
- **Recording `closure_evidence_found` with no discovery** — a table-level SQL CHECK, so it is not
  merely forbidden, it is inexpressible.

**DRs:** `DR-2026-05-26-gap-driven-mining-protocol.md` (creates `gap_mining` +
`mining_addressability`, migration 017); `DR-2026-07-20-citation-mining-methodology-corrections.md`
(retires Scholar Gateway for forward mining); `DR-2026-08-01-research-contract-single-source.md`
(fixes R2's tier scope and reconciles the depth statements); `DR-2026-05-24` (supersession protocol,
whose cluster-search pattern `gap_mining.check_method='composite'` mirrors); and the migration-051
header, which is a decision record in all but name for `connections_produced`.

#### (h) ACCEPTANCE CONDITIONS

Level ceiling is 4. Level **D** is used as defined in §2.4(h): **`D — enforced at write time by
SQLite`** for `CHECK` / `UNIQUE` / `PRIMARY KEY` / `NOT NULL`, and **`D(fk) — deferred differential
check in migrate_db.py`** for `FOREIGN KEY` (FKs are `OFF` during every migration script,
`:164` / `:251`; new violations raise `sqlite3.IntegrityError`, the pre-existing ~18-violation
baseline is grandfathered by design, `BOOTSTRAP` migrations are downgraded to a warning, and the
reach into CI is indirect via the blocking `migration_reproducibility` rebuild).

**This stage is the repo's best argument for level D existing at all.** `gap_mining` puts three
semantic integrity rules — not type rules — into table-level `CHECK`s, so a write that lies about a
closure fails at the database. Nothing on the 1–4 spectrum describes that, and calling it "4" both
understates its strength and misattributes it to CI.

For one **`citation_mining` row**:

1. **`(slug, local_ref_id)` is unique.** Primary key.
   *Level: **D — enforced at write time by SQLite***.
2. **`slug` is a real slug.** Column `slug`.
   *Level: **D** (`NOT NULL`) + **D(fk)** (`REFERENCES slugs(slug)`, deferred differential check) +
   4 blocking* — `test_db_integrity` A-series.
3. **`global_ref_id`, when present, resolves.**
   *Level: 4 blocking + **D(fk)*** — `test_db_integrity` **A07** is the direct enforcer; the
   declared FK to `evidence_sources` is `D(fk)` and, being nullable, fires on nothing when NULL.
   That nullability is exactly what conditions #5 below.
4. **`backward` / `forward` ∈ {0,1}.** *Level: **D — enforced at write time by SQLite***.
5. **Not a stub — not (`backward=0 AND forward=0 AND deferred_reason` empty).** Columns `backward`,
   `forward`, `deferred_reason`. *Level: **4 blocking, but only for rows carrying a non-NULL
   `global_ref_id`***. The `bad_cm` scan INNER-joins `evidence_sources` on `cm.global_ref_id`
   alone; by the file's own measurement that excluded 146 of 183 rows. Enforcer:
   `citation_mining_completeness.py` (registered `citation_mining_session`).
6. **A partial pass names its blocker.** Column `deferred_reason`. *Level: 1 (text rule)* — free
   text, no minimum length and no vocabulary, in contrast with `gap_mining.notes` which carries
   ≥ 10 / ≥ 20-char SQL CHECKs. Enforcer: `citation-miner_SKILL.md` §0.
7. **`connections_produced` is a JSON array of resolvable ids.** *Level: **UNENFORCED*** —
   `TEXT NOT NULL DEFAULT '[]'` is the only constraint; there is no `json_valid()` CHECK, and
   H06/H07's `EDGE_JSON` scope covers `governing_refs` and `admitted_ref_ids` only. Migration 051
   measured 13 bare integers, three vocabularies and 3 unresolvable ids, and deliberately declined
   to normalise.
8. **Provenance fields present.** `created_at` / `created_by_session` / `updated_at` /
   `updated_by_session`. *Level: **D — enforced at write time by SQLite*** (`NOT NULL`). Note D
   guarantees the fields are *populated*, not that they are *true*: nothing validates that
   `created_by_session` names a session that exists — which is the same class of gap as #11.

For one **T1–T2 `evidence_sources` row, as a mining subject**:

9. **Has a `citation_mining` row resolving by `global_ref_id` **or** by `(slug, local_ref_id)`.**
   *Level: 4 blocking, session-scoped* — `citation_mining_session`. The dual-path resolution is
   correct here (unlike #5). **Vacuous today**: `NOTHING-IN-SCOPE`.
10. **…and is actually in scope — i.e. has a `source_slug_links` row.**
    *Level: **UNENFORCED as a requirement, and its absence is an escape from #9*** — both the
    outstanding query and the `examined` denominator INNER-join `source_slug_links`.
11. **…and the session pointer names a session that gives the gate a subject.**
    `sessions/LATEST-RESEARCH`. *Level: 4 blocking in name, **satisfiable by emptiness in fact**.*
    Enforcement here is **partial and distributed, and one commonly-cited enforcer does not exist**:
    - `test_db_integrity` **L04** — 4 blocking; reports pointer *drift* out of the gate's Tier 1–2
      scope. Passes vacuously when nothing is in scope (`_newest is None ⇒ _drifted False`).
    - `scripts/run_checks.py:220-237` — the dispatcher FAILs a *blocking* check whose pointer file
      is missing or empty (it used to SKIP, which disarmed the gate in silence), and SKIPs at
      advisory level. **It checks the pointer file, not the pointer's target**: it never verifies
      the named session exists on disk or has rows. `sessions/LATEST-RESEARCH` currently names
      `session_2026-07-26-…-b3.md` and that file does exist — which is luck, not a check.
    - `validate_cross_refs` — checks the handoff's named record and plan.
    - **`session_pointer_resolvable` is not a check.** It is named in CLAUDE.md §10 (as
      "(blocking)") and in two workplans, and it appears in **no registry entry and no code**:
      `grep -n session_pointer_resolvable governance/check-registry.yaml scripts/run_checks.py`
      returns nothing. The standalone `scripts/audit/session_pointer_audit.py` was **deliberately
      deleted on 2026-08-06** and its function redistributed to the three enforcers above — the
      registry's own note on `citation_mining_session` records this: it "patrolled a hazard whose
      root cause was a five-line fix in the dispatcher it was watching." So the *name* is phantom;
      pointer honesty is partly enforced elsewhere, and the part that is missing is exactly the
      part this condition needs — that the pointed session have subjects.
12. **`citation_mining_status ∈ {pending, mined, deferred, not-applicable}`.**
    *Level: **D — enforced at write time by SQLite*** — `NOT NULL DEFAULT 'pending'` plus a
    `CHECK`, migration 040. Unusually, the D here is complete: there is no CI check policing the
    vocabulary because there is no way to write an invalid one.
13. **`citation_mining_status='mined'` ⟺ a non-deferred mining row resolves to it.**
    *Level: 4 blocking, biconditional* — `test_db_integrity` **C08**.
14. **`citation_mining_status='deferred'` ⇒ a mining row with a non-empty `deferred_reason`.**
    *Level: 4 blocking* — **C09**.
15. **`deferred` / `none-extractable` ⇒ a coded `processing_blocked_reason` from the 9-value set.**
    *Level: **D** (the 9-value `CHECK`, migration 040) + 4 blocking (the *implication*, which no
    CHECK expresses)* — **C09**. The split is the point: D constrains the vocabulary, only the
    check can constrain the relationship between two columns on different rows' worth of state.
16. **A `processing_blocked_reason` is not attached to a non-stopped state.**
    *Level: 4 blocking* — **C09**.
17. **The batch mined ≥ `anchors // 4`.** *Level: 2 advisory* — `research_batch_dod` **R2**.
18. **Mining was owed only on a *confirmed* anchor.** Column `verification_status`.
    *Level: **NOTHING ENFORCES THIS*** — the gate never predicates on status; it only displays it.
19. **The tier band searched matches the contract's.** *Level: 4 blocking at the gate
    (`--tier-max 2` pinned in the registry), **1 at the CLI*** — `db.py unmined` defaults to
    `tier_max=3` and `citation-miner_SKILL.md:74,76` instructs `--tier-max 3`, both wider than R2's
    ratified scope.

For one **`gap_mining` row**:

20. **`gap_id` resolves.** Column `gap_id`.
    *Level: **D** (`NOT NULL`) + **D(fk)** (`REFERENCES gaps(gap_id)` — deferred differential check
    in `migrate_db.py`; new violations fail, pre-existing baseline grandfathered, `BOOTSTRAP`
    migrations exempt, CI reach indirect via `migration_reproducibility`)*. **No CI check covers
    this FK** — there is no A-series entry for `gap_mining → gaps`, so unlike #2 and #3 the D(fk)
    is the whole of the protection.
21. **`outcome` ∈ the 5-value set** (`closure_evidence_found`, `partial_evidence_found`,
    `null_result`, `gap_recategorized`, `deferred`).
    *Level: **D — enforced at write time by SQLite***.
22. **`check_method` ∈ the 6-value set** (`pubmed_cluster`, `scholar_gateway_lived_experience`,
    `cochrane_direct`, `standards_body_direct`, `multilingual_research`, `composite`).
    *Level: **D — enforced at write time by SQLite***.
23. **`closure_evidence_found` ⇒ non-empty `discoveries_logged`.**
    *Level: **D — enforced at write time by SQLite***, table-level `CHECK`. A closure that lies
    about having found something is not merely forbidden, it is **inexpressible**.
24. **`gap_recategorized` ⇒ `notes` ≥ 20 chars.**
    *Level: **D — enforced at write time by SQLite***, table-level `CHECK`.
25. **`deferred` ⇒ `notes` ≥ 10 chars.**
    *Level: **D — enforced at write time by SQLite***, table-level `CHECK`.
26. **`search_strategy_record` is a replayable JSON strategy list.**
    *Level: **D for presence only** (`NOT NULL`), **1 (text rule) for the content*** — the DDL
    documents an elaborate schema
    (`{"strategies":[{"tool":…,"query":…,"connectors_used":[…],…}]}`) and constrains only
    `NOT NULL`; there is **no `json_valid()` CHECK**, in contrast with `search_executions`, which
    carries `CHECK (terms_used IS NULL OR json_valid(terms_used))`. A one-character string
    satisfies it.
27. **Every id in `discoveries_logged` is in `evidence_sources`.** *Level: 2 advisory* —
    `gap_mining_audit.py` CHECK 6.
28. **`candidate_dois` holds only *unverified* candidates.** *Level: 2 advisory* —
    `gap_mining_audit.py` CHECK 7.
29. **An ADDRESSABLE gap is not CLOSED-FIXED without a `gap_mining` row.**
    `gaps.status` × `mining_addressability`. *Level: 2 advisory* — `gap_mining_audit.py` CHECK 1.
30. **A closure carries the rule-#7 falsifiable fields.** `gaps.falsification_condition` and
    siblings. *Level: 2 advisory* — `gap_mining_audit.py` CHECK 2; `research_protocol_audit.py`
    CHECK 1.

---

*Derivation note. Every count, verdict and line reference in §§2.4–2.6 was produced on 2026-08-11
at HEAD `6c2d179` by running the command quoted beside it, against
`data/guidebook.db` opened read-only. Doctrine SHA at the time of writing:
`git rev-parse HEAD:governance/mission-and-epistemics.md | cut -c1-7` → `0f2f525`.*

---

### 2.7 Stage 7 — Value extraction

*Substrate: `source_value_extractions`, `jurisdictional_values`, `reasoning_doc_citations`,
`spec_value_probes`, `external_root_registry`, the locator hierarchy, the value genealogy.*

#### (a) Tools, tables, methodology

**Tables**

| Object | Rows | State | Notes |
|---|---:|---|---|
| `source_value_extractions` | 0 | **BUILT+UNEXERCISED** | **49 columns** (`PRAGMA table_info` → 49), after migrations 028 (genealogy), 041 (overflow), 052 (`item_code`), 053 (16 locator columns). Constraints live in the DDL: `claim_type` CHECK (5 values), `extraction_method` CHECK (4), `extraction_status` CHECK (5), `root_type` CHECK (5), `measurement_paradigm` CHECK (9), `device_class` CHECK (9), `contested` CHECK (0,1), a table-level compound CHECK forcing `claimed_value IS NULL ⟺ claim_type='absent'`, and FKs to `evidence_sources(ref_id)`, `slugs(slug)`, `populations(population_code)`, `items(item_code)`, `reasoning_doc_citations(citation_id)`, plus `root_ref_id → evidence_sources(ref_id)`. |
| `jurisdictional_values` | **109** | **BUILT+EXERCISED** | 32 columns. The only stage-7 table with data, and the only research-shaped table the clean-room reset deliberately preserved (`DR-2026-08-06-clean-room-evidence-reset.md` §3). |
| `reasoning_doc_citations` | 0 | **BUILT+UNEXERCISED** | 34 columns. Table-level compound CHECK: `claim_type ∈ {numerical_spec, jurisdiction_value}` ⇒ `claimed_value` and `value_match` non-NULL; `∈ {qualitative, definitional}` ⇒ `claim_text` and `claim_match` non-NULL. |
| `spec_value_probes` | 0 | **BUILT+UNEXERCISED** | 21 columns. PMP walk substrate; `passes_strict` is the corroboration input `schemas/directness.py` names for value-directness. Typed `item_code` FK and `slug` FK. |
| `external_root_registry` | 0 | **BUILT+UNEXERCISED** | Registry of out-of-corpus roots that `v_value_independence` requires an unkeyed `root_id` to resolve against. |

**Views** (all verified to execute; `SELECT COUNT(*)` over all 18 views → 18 OK, 0 FAIL)

- `v_item_extractions` — **BUILT+UNEXERCISED** (0). `items ⋈ source_value_extractions ⋈
  evidence_sources`. This join is what migration 052 exists to make possible.
- `v_value_independence` — **BUILT+UNEXERCISED** (0). The best-practice-vs-consensus
  discriminator: `COUNT(DISTINCT COALESCE(root_ref_id, root_id))` per
  `(COALESCE(parameter_canonical, parameter), population_code)`, filtered to
  `root_type IN ('measurement_primary','participatory_finding','derived_calculation')` **and**
  root-resolution (`root_ref_id IS NOT NULL OR root_id IN (SELECT root_id FROM
  external_root_registry)`). `committee_assertion` and `untraced` are excluded by
  construction — that exclusion *is* the anti-laundering mechanism.
- `v_root_id_conflicts` — **BUILT+UNEXERCISED** (0). A `UNION ALL` of both directions:
  one `root_ref_id` with >1 `root_id`, and one `root_id` spanning >1 `root_ref_id`.
  Migration 028's header records that this hardens a gap in the ratified DR text — "one root ⇒
  one id" was never guaranteed.
- `v_unregistered_roots` — **BUILT+UNEXERCISED** (0). Rows with a minted `root_id`, no
  `root_ref_id`, and no registry entry.
- `v_registry_duplicate_descriptions` — **BUILT+UNEXERCISED** (0).

**Scripts**

| Script | State | Evidence (run 2026-08-11) |
|---|---|---|
| `scripts/audit/jurisdictional_divergence.py` | **BUILT+EXERCISED** | Exit 0. `SURFACED: 2 within-jurisdiction candidate contradiction(s), 3 candidate conflation/error(s), 9 cross-jurisdiction divergence(s), 12 unadjudicated`. Real findings over real rows — the only stage-7 tool with a non-empty subject. `--selftest` mutation harness: 6/6 PASS. |
| `scripts/audit/reasoning_doc_citations_audit.py` | **BUILT+UNEXERCISED** | `Total rows: 0 … No claim-level audit possible yet.` exit 0. Checks 1–7 unreachable. |
| `scripts/audit/adjudication_integrity.py` | **BUILT+UNEXERCISED** (quarantined) | Exit 0; readiness block prints `source_value_extractions: 0 row(s) — EMPTY: value-level convergence not yet assessable (pre-C1)`. |
| `scripts/audit/research_batch_dod.py` rule **R3** | **BUILT+UNEXERCISED** | Lines 320–330: predicate is `evidence_sources WHERE tier >= 4 AND (article_number IS NULL OR ='') AND (pages IS NULL OR ='') AND COALESCE(notes,'') NOT LIKE '%UNVERIFIED-QUANT%'`. `evidence_sources` = 0 ⇒ vacuous. Output: `R3: PASS — all regulatory sources clause-cited or flagged [UNVERIFIED-QUANT]`. |
| `scripts/audit/research_batch_dod.py` rule **R12** | **BUILT+UNEXERCISED and PARTIAL** | R12's contract hook is *"Case studies → `case_studies`. Economics → `economics_entries`. Code values → `jurisdictional_values`."* The implementation (lines 462–477) compares `economics_entries` count against a `LIKE '%cost%' OR '%grant%' OR '%bcr%'` scan of `search_executions.findings_note`. **It never queries `case_studies` and never queries `jurisdictional_values`** — the only mention of the latter in the file is inside R12's *failure-message string*. Two-thirds of the rule it names is unimplemented. |
| `scripts/audit/population_integrity_audit.py` | **BUILT+UNEXERCISED** | Exit 0, `ISSUES: 0`, every leg over 0 rows. |
| `scripts/audit/table_connectivity.py` | **BUILT+EXERCISED (as a report)** | `4 values captured 0/80`. Registry-quarantined as "NOT A GATE". |
| `scripts/emit_data_migration.py` + hand-authored `data_*.sql` | **BUILT+EXERCISED (historically)** | `grep -l "INSERT INTO source_value_extractions\|INSERT INTO jurisdictional_values" scripts/migrations/*.sql` → ~20 files (e.g. `data_20260712150000_jurisdictional-values-backfill.sql`, `data_20260714210000_rap_rt60_extraction_substrate.sql`). **This is the only writer of either table.** |

**Schema modules**
(`python3 scripts/audit/validate_pydantic_schemas.py --strict`)

| Module | State | Note |
|---|---|---|
| `schemas/source_value_extraction.py` | **BUILT, DRIFTED** | `DRIFT … DB-only (not in Pydantic): ['contested','device_class','echo_of','file_anchor','measurement_paradigm','root_classification_basis','root_id','root_population_note','root_ref_id','root_type','setting']` — **all 11 value-genealogy columns are absent from the model.** The 16 locator columns *are* present. The module's own docstring declares the gap rather than hiding it. |
| `schemas/jurisdictional_value.py` | **BUILT, mild drift** | `DB-only: ['created_at','created_by_session','jv_id','updated_at','updated_by_session']` — bookkeeping only. Was never mapped into `MODEL_TABLE_MAP` until 2026-08-09. |
| `schemas/reasoning_doc_citation.py` | **BUILT, clean** | `OK reasoning_doc_citation.ReasoningDocCitation <-> reasoning_doc_citations` (34/34). Written 2026-08-09; before that the table had no model at all. |
| `spec_value_probes` | **no model** | Among the *49 / 66 live tables with no mapped Pydantic model* the audit reports. |

**Registered checks touching stage 7** (levels read from `governance/check-registry.yaml`)

| id | level | battery | kinds |
|---|---|---|---|
| `reasoning_doc_citations_audit` | advisory | research | data, synthesis |
| `population_integrity_audit` | advisory | research | data, schema |
| `validate_pydantic_schemas` (`--strict`) | advisory | schema | schema, data |
| `research_dod` | advisory | research | data, synthesis |
| `research_dod_selftest` | **blocking** | research | always |
| `research_contract_sync` | **blocking** | research | governance, tooling |
| `test_db_integrity` | **blocking** | db_integrity | data, schema |
| `migration_reproducibility` | **blocking** | data | data, schema |
| `test_jurisdictional_divergence` | advisory | tests | tooling |
| `validate_jurisdiction` | **blocking** | schema | schema, data |

**`jurisdictional_divergence` itself is NOT a registered check** — only its unit test is. It sits
in the registry's `quarantine` block with the reason: *"Green, but it is a SURFACING tool …
Its exit code carries no verdict. Belongs in a report, not a gate."* So the one stage-7 tool with
real data is at **level 2** by explicit decision, not by neglect.

A second, sharper gap in the same family: `research_dod_selftest` is **blocking**, and its
`expected` set (line 655–656) is `{R1,R2,R3,R4,R5,R6,R7,R8,R10,R11,R13,R14}`. **R12 is not in
it.** So R12 is both wrongly implemented *and* outside the harness that would have caught the
implementation rotting.

**Workplan.** `workplan/2026-08-09-locator-hierarchy-and-enforcement-probes.md` — IN PROGRESS,
adversarially reviewed and self-corrected (Part 5 is a 17-row correction log). Its stage-7
substance: the locator-scheme registry question (§1.1), the round-trip loss detector (§1.2), the
`UNIQUE(item_code, jurisdiction, standard_name)` re-key (§1.3), the 18(+1) multi-document rows
(§1.4), and the finding that migration 053's committed header carries unaudited numbers summing
to 97 not 109 (§1.5). Everything in its Part 1 is **DESIGNED-ONLY** — no splitting migration, no
scheme registry, no decomposer exists in the repo.

#### (b) How they relate to each other

Two disconnected sub-systems share the stage number.

**Sub-system A — the academic-class extraction spine (empty).**

```
evidence_sources.ref_id ──FK──> source_value_extractions.ref_id
slugs.slug              ──FK──> source_value_extractions.slug
items.item_code         ──FK──> source_value_extractions.item_code       (migration 052)
populations             ──FK──> source_value_extractions.population_code (scalar, DEPRECATED)
                        ──FK──> extraction_population_links              (junction, migration 021)
source_value_extractions.promoted_to_rdc_id ──FK──> reasoning_doc_citations.citation_id
source_value_extractions.root_ref_id        ──FK──> evidence_sources.ref_id
source_value_extractions.root_id            ──(NO FK)──> external_root_registry.root_id
```

The `root_id` edge is the one un-keyed join in the genealogy layer: a bare TEXT column with no
FK, and `v_unregistered_roots` exists precisely to catch what an FK would have refused.
`v_value_independence` groups on `COALESCE(parameter_canonical, parameter)` — **a text key**,
not an item key, even though `item_code` has existed since migration 052. Migration 028's header
flags the consequence itself: *"a parameter split across canonicalised / raw rows under-counts."*

Migration 052's header explains why the text key was insufficient: all 8 pre-reset extraction
rows carried `parameter='RT60'` and *two* items are RT60 items (`A-18` classroom, `A-10b`
hydrotherapy), while 13 items share `bpc_source_slug='room-acoustic-performance'`. Neither
`parameter` nor `slug` resolved the item. `test_db_integrity` J01/J02/J03 pin the resulting
adjudication; J03 is an explicit snapshot check on extraction_ids 1–8 that now examines 0 rows.

**Sub-system B — the code-class jurisdictional spine (109 rows, evidentially orphaned).**

```
items.item_code ──FK──> jurisdictional_values.item_code       (20 distinct items)
jurisdictional_values.jurisdiction   TEXT, no FK, no CHECK     (12 distinct values)
jurisdictional_values.standard_name  TEXT — carries BOTH document identity AND clause
jurisdictional_values.spec_id        TEXT — "informational only … no specification table
                                             exists to FK against"  (schema comment, verbatim)
jurisdictional_values.ref_id         DOES NOT EXIST
```

Verified from `SELECT sql FROM sqlite_master WHERE name='jurisdictional_values'`: no `ref_id`
column; `spec_id` carries the inline comment quoted above; `UNIQUE (item_code, jurisdiction,
standard_name)`. `SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%spec%'`
returns `economics_entry_specs`, `case_study_specs`, `spec_value_probes` — **there is no
specifications table**, so all 26 non-NULL `spec_id` values point at nothing. This is not a
hidden dead end but a documented one; its cost is that
`governance/conceptual-model.md` names Specification as **ENT-01**, and
`pipeline-contract.yaml`'s spine is `EvidenceSource (ENT-02) -> BPC entry (ENT-03) ->
Specification (ENT-01) -> Item (ENT-08) -> render`. **The spine's third hop has no table.**

`jurisdictional_divergence.py` is the only consumer. It reads
`(item_code, jurisdiction, unit, value_numeric, is_code_minimum, standard_name, evidence_tier)`
(line 66) and groups by `(item_code, unit)` — again a **text join on `unit`** — with an explicit
order-of-magnitude guard (`ratio >= 10 → candidate_conflation_or_error`, line 140) because
same-unit does not mean same quantity. Two facts sharpen the fragility of that grouping, both
derived here: **34 of 109 rows have `value_numeric IS NULL`** and **22 have no `unit`**, so
roughly a fifth of the corpus cannot enter the comparison at all. It joins forward to stage 9 by
a single query at line 89 — `SELECT DISTINCT item_code FROM evidence_cell_state WHERE state IN
('stated','provisional')` — which today returns nothing, so all 12 divergent items report
`unadjudicated_divergence` with the message *"no evidence_cell_state best-practice determination
exists to adjudicate (judgment stage unbuilt)."*

**Where the two sub-systems meet, precisely.** They meet **at the item key, for the code-floor
delta surface, and nowhere in the evidentiary chain.** `v_code_floor_only` joins them directly
and was built for exactly that:

```sql
CREATE VIEW v_code_floor_only AS
    SELECT ecs.*, jv.jurisdiction, jv.standard_name,
           jv.value_numeric AS code_value, jv.unit AS code_unit
    FROM evidence_cell_state ecs
    LEFT JOIN jurisdictional_values jv ON jv.item_code = ecs.item_code
    WHERE ecs.code_floor_only = 1
```

Migration 026's header: *"ADDS `v_code_floor_only` as a join against `jurisdictional_values` so
the code-floor-delta surface promised in `best-practices-assessment-system.md` §4 Phase 4 is
actually computable from structured columns."* `evidence-architecture.md` §6 G5 names the same
join as the mechanism behind the advocacy-brief delta.

**What they cannot do is meet in `governing_refs`.** That column is a JSON array of `REF-NNNNN`
ids; the only typed store of the same edge is `cell_source_links.ref_id`, FK'd to
`evidence_sources(ref_id)`. `jurisdictional_values` has no `ref_id` and no `evidence_sources`
row, so a code value cannot appear in a determination's governing set without a human minting a
`REF-NNNNN` for it first. `test_db_integrity` line 341 concedes this conditionally, in a comment
on its `CAPTURED` predicate: *"gives `jurisdictional_values` a `ref_id`, add it to this predicate
AND to …"*.

#### (c) Relation to the previous stage (6 — citation mining)

**Entry contract as designed.** A source may be extracted from when it is (i) admitted
(`search_admissions` row), (ii) verified (`verification_status='VERIFIED'` with a
`verification_method`, per D-0157), (iii) mined (`citation_mining_status`), and (iv) marked
`data_capture_status='pending'`. `evidence_sources.data_capture_status` (migration 040, column
confirmed present) is the declared handle: enum `pending / captured / none-extractable /
deferred`, NOT NULL DEFAULT `'pending'`.

**A structural note before the enforcement list.** `governance/pipeline-contract.yaml` (status
**PROPOSED**) has five stages — `research`, `collection`, `judgment`, `synthesis`, `render`.
**There is no extraction stage.** Value extraction has no entry criterion, no exit criterion and
no `check:` of its own anywhere in the contract; it lives in the unnamed gap between
`collection`'s exit and `judgment`'s entry. Every enforcement claim below is therefore made by
something that was aimed at a neighbouring stage.

**What actually enforces it:**

- `citation_mining_session` — **blocking**, battery `data`, kinds `data, synthesis`,
  `session_pointer: LATEST-RESEARCH`. Gates stage 6 *output*, not stage 7 *entry*.
- `research_dod` (advisory) rule **R2** requires `citation_mining` rows proportionate to
  admitted anchors before filing.
- **NOTHING ENFORCES** that `data_capture_status` transitions `pending → captured` only when a
  `source_value_extractions` row exists. No registered check references the column as a
  stage-7 precondition; `grep -rn "data_capture_status" scripts/ | grep -v migrations` finds it
  in `db.py` and reporting tools only.
- **NOTHING ENFORCES** the entry contract for `jurisdictional_values` at all. It has no
  upstream: `SELECT created_by_session, COUNT(*) FROM jurisdictional_values GROUP BY 1` →
  `[(None, 109)]`. No admission edge, no session attribution, no search that found them.

#### (d) Relation to the next stage (8 — population matching)

**Exit contract as designed.** An extraction hands off (i) a typed value (`claimed_value` +
`claimed_unit` + `claim_type`), (ii) a located value (`source_section`, and since migration 053
the 16-column locator hierarchy), (iii) a genealogy (`root_type` + `root_ref_id`/`root_id` +
`measurement_paradigm` + `device_class`), (iv) an item edge (`item_code`, migration 052), and
(v) a population edge (`extraction_population_links`, migration 021).

**What actually enforces it:**

- `test_db_integrity` **J01** (blocking): an extraction's `item_code` must belong to its slug via
  `item_bpc_links` or `items.bpc_source_slug`. Its own inline comment concedes the assumption
  out loud — *"this holds while extractions describe items their own BPC governs. If a legitimate
  cross-slug extraction ever appears, this check is the thing that should be revisited — not
  silently widened."* It guards the least-likely class: an adversarial injection that moved a row
  to `A-10b`, the *other* RT60 item on the same slug, passed J01.
- `test_db_integrity` **J02** (blocking): where `root_classification_basis` names a probe id, the
  probe's `item_code` must agree. Text-`LIKE` join.
- `test_db_integrity` **J03** (blocking): the 8 adjudicated RT60 extractions still carry `A-18`.
  A frozen snapshot; post-reset it examines 0 rows.
- `population_integrity_audit` (**advisory**): scalar `population_code` ↔
  `extraction_population_links` consistency. 0 rows; `ISSUES: 0`.
- **NOTHING ENFORCES** that `root_type` is set before an extraction is used. `v_value_independence`
  merely *excludes* untyped rows, which is silent under-counting, not a gate. Migration 028's
  header names this as its own fix A/B: the v1 view counted NULL-`root_type` rows.
- **NOTHING ENFORCES** the locator hierarchy. All 16 `loc_*` columns are NULL/empty on all 109
  `jurisdictional_values` rows — verified per column, all sixteen return 0. Migration 053
  "touched no row" by design, and no follow-on splitting migration exists.
- **NOTHING ENFORCES** the derivation handshake. `derivation_paths` (dual / population_only /
  function_only) and `functional_basis`, ratified in
  `DR-2026-07-13-value-genealogy-and-derivation-handshake.md`, **do not exist as columns**:
  `SELECT name FROM sqlite_master WHERE sql LIKE '%derivation_path%' OR sql LIKE
  '%functional_basis%'` → `[]`. `pipeline-contract.yaml` `judgment/derivation-handshake` carries
  `check: null` with an honest comment: *"this criterion is honestly DECLARED-BUT-UNENFORCED, not
  phantom-VERIFIABLE."* The contract understates it — it is not merely unenforced; **the storage
  does not exist.**

#### (e) The goal of the stage

Stage 7 converts a *source* into *claims about parameters*. It is where the corpus stops being a
bibliography and starts being data: a number, a unit, a population, a jurisdiction, a point
inside the document where it was found, and — the project's distinctive addition — a
**genealogy** saying whether that number is an original measurement, a participatory finding, a
committee assertion, a derived calculation, or untraceable; by what measurement paradigm; and for
what device class. The genealogy exists to answer one question the tier ladder alone cannot:
*is this value convergence, or is it one unevidenced ancestor echoed by twelve documents?*
`v_value_independence` is the operationalisation of that question, and `root_type`'s structural
exclusion of `committee_assertion` and `untraced` is its teeth.

The second job is the locator: recording *where* a claim lives, at the level of granularity the
document class actually uses, so a reader can check the project's work and a later session can
detect supersession at clause granularity rather than document granularity.

#### (f) How the tools support that goal — and where they do not

**Where they do.** The genealogy design is genuinely sharp. Migration 028's adversarial review
closed three inflation vectors *before a single row existed* — counting NULL-`root_type` rows;
two rows citing one source under two `root_id` strings scoring as two roots; registry duplicate
stubs — which is the right order of operations, and the header says so ("columns before
extraction row 1 … retrofit is the expensive path"). `measurement_paradigm` is doing real
epistemic work: it makes "a static turning circle can never corroborate a swept-path envelope"
a *query* rather than a reviewer's memory. `jurisdictional_divergence.py`'s refusal to compare
across units, and its order-of-magnitude reclassification, are the restraint that makes a
surfacing tool trustworthy.

**Where they do not.**

1. **The genealogy has no Pydantic mirror.** All 11 genealogy columns are missing from
   `schemas/source_value_extraction.py`. The only structural validation is the SQLite CHECKs,
   which constrain *vocabulary* but not *presence*. `root_type` is nullable; nothing requires it.
2. **`jurisdictional_values` cannot participate in genealogy at all.** No `ref_id`, no
   `root_type`, no locator populated. Structurally the 109 code values are a spreadsheet attached
   to `items`. `DR-2026-08-06` §3 defends the missing `ref_id` on class-relative grounds ("the
   source of a code value is the code standard itself") — a genuinely good argument about
   *identification*. It does not address *reachability*: no view, no audit and no determination
   can walk from a cell back to a code value through the evidentiary chain, because there is no
   shared key. `v_code_floor_only` reaches it by `item_code` for the delta surface only.
3. **`standard_name` is overloaded and load-bearing.** It carries document identity *and* clause
   (`'ADA 2010 §404.2.5'`), and it is a component of the UNIQUE key. Workplan §1.3 establishes
   that the key is unique *only because* of the overload — and that post-unpack there are **zero
   live collisions across all 109 rows**, so the re-key is future-proofing, not repair. The
   workplan corrects its own first draft on this (C7, C8).
4. **The round-trip verifier does not exist, and would verify less than claimed.** Workplan §1.2
   is candid: it detects *loss*, is blind to render-identical misassignment (ADA's `.5` in
   `loc_subsection` vs `loc_paragraph` renders identically), decomposer and renderer share one
   author, and the "or an explicit normalization note" escape hatch was used by authorial fiat on
   the one row that failed. n = 8 hand-picked rows.
5. **R3's enforcer checks the wrong table.** R3 says *"Code/standard values: clause/section/page."*
   Its implementation checks `evidence_sources.article_number` / `.pages` for tier ≥ 4 sources. It
   does not look at `jurisdictional_values.source_section`, nor at any `loc_*` column, nor at
   `source_value_extractions.source_section`. So the rule that `DR-2026-08-06` §3 cites as the
   justification for keeping all 109 rows is enforced against a table those rows are not in.
6. **R12's enforcer implements one of the three structured homes it names**, and R12 is absent
   from the blocking selftest's `expected` set.

#### (g) How doctrine conditions the stage

**`governance/mission-and-epistemics.md`**

- **§Citation discipline**, bullets 2–3: *"Quantified outcome claims require DOI + page/table
  reference, or failing that, direct URL to source. Unverified claims carry `[UNVERIFIED-QUANT]`
  flag."* · *"Two failed independent searches → CLOSED-DELETED disposition for unverifiable
  values; do not accumulate unresolvable UNVERIFIED flags."*
  **FORBIDS:** recording a quantified value with no locator *and* no flag; letting UNVERIFIED
  flags accumulate as a permanent state.
- **§Citation discipline**, bullet 4: *"Source authenticity: confirmed real before citation.
  'I don't know' governs over invention."* **FORBIDS:** inventing a `root_id`, a clause number,
  or a value.
- **Doctrinal commitment 1:** *"Every parameter exposes its within-population variability …
  Within-population variation is shown as a first-class data dimension, not buried in narrative
  caveats."* **FORBIDS** collapsing a range to a point at extraction time; `claim_type='range'`
  exists for this.
- **Doctrinal commitment 2** (amended 2026-07-21, Option A): a code-consensus claim is a
  weak-band claim, *"never rendered unflagged or above the weak band."* This bites at stage 7
  through `is_code_minimum` and `evidence_tier`: `GROUP BY evidence_tier` → `[(6, 109)]`;
  `GROUP BY is_code_minimum` → `[(1, 109)]`. Every row in the table is self-declared T6 code
  floor, which is the fact stage 9 will band on.

**`governance/tier-system.md`**

- **§4** — *"When a BPC cites a T4–T6 source, the citation must additionally confirm that the
  cited edition is the current legally-in-force edition."* Enforcement is declared at Level 2
  (`scripts/audit/code_currency_audit.py`) — and that script is **quarantined**: *"RED. Flags
  standards lacking a currency marker; a content backlog, not a gate."*
  **FORBIDS** extracting from a superseded edition without recording that fact. Unenforced today.
- **§8** — the weighted-strength bands. Stage 7 must record enough (`evidence_tier`,
  `standard_name`, jurisdiction) that stage 9 can assign a band at all.

**`governance/evidence-architecture.md`**

- **§4 G1** — a T4/T5 source is re-grained `GRAIN_AGGREGATE` *"**only** when its evidence basis is
  documented as traceable to T1/T2 evidence, with that provenance recorded on the source record.
  Otherwise it keeps `GRAIN_CODE`. Untraceable standards convergence stays in the regulatory
  stratum where §2 put it."* **FORBIDS** silently promoting a standard out of the regulatory
  stratum. The provenance field this needs is `evidence_sources.derivation_chain` (column
  confirmed present); `pipeline-contract.yaml` `collection/discovery-provenance` records it with
  `check: null`.
- **§9 / `evidence-methodology.md` §2.4** — *absence-of-evidence ≠ evidence-of-absence*
  (Altman & Bland 1995), which is why `claim_type='absent'` and
  `extraction_status='absent-confirmed'` are distinct first-class values rather than a missing
  row. **FORBIDS** recording "we found nothing" by omission.

**Research contract** (`governance/research-contract.yaml`, `status: OPERATIVE`, adopted by
`DR-2026-07-25-research-contract-mechanical-enforcement.md`, single-sourced by
`DR-2026-08-01-research-contract-single-source.md`)

- **R3** (when-filing, *"Quantified values carry a locator, or carry the flag"*): *"Quantified
  values need a locator or `[UNVERIFIED-QUANT]`. Code/standard values: clause/section/page.
  Outcome claims: DOI + page/table, or a direct URL."* Its `resolution` field records that the
  two hand-transcribed copies had each kept only one of the two **source classes**, and that both
  are now stated — the split is the doctrinal content `DR-2026-08-06` §3 relies on.
- **R12** (when-filing): *"Case studies → `case_studies`. Economics → `economics_entries`. Code
  values → `jurisdictional_values`. Never leave them in prose notes."* **FORBIDS** a code value
  living in a BPC's prose.
- **R15** (when-filing): *"A staged candidate description is a HYPOTHESIS. On resolution,
  re-describe it from the source and CORRECT it if you over-claimed. Do not let your own guess
  harden into fact."* Applies directly to `extraction_status='preliminary' → 'verified'`.

**Decision Records.** `DR-2026-07-13-value-genealogy-and-derivation-handshake.md` — the genealogy
and the handshake, carrying the **cultural-claim protection**: community-rooted claims, bounded
to Co-1/participatory provenance so the exemption cannot be self-declared, are fully assertable
as `population_only` and never require mechanical reduction. Also
`DR-2026-08-06-clean-room-evidence-reset.md` §3 (class-relative adequacy),
`DR-2026-05-13` (Track 3, `reasoning_doc_citations`), `DR-2026-05-28-b`
(`source_value_extractions` as the value substrate).

#### (h) ACCEPTANCE CONDITIONS — stage 7

##### 7-A · A `source_value_extractions` row

| # | Condition | Column / field | Level | Named enforcer |
|---:|---|---|---|---|
| 1 | `ref_id` resolves to a real source | `ref_id` | **D(fk)** | Declared FK to `evidence_sources(ref_id)`; deferred differential check in `migrate_db.py:162–183` / `:250–267`; reaches CI via `migration_reproducibility` (**blocking**). **No `test_db_integrity` A-check covers this table** — the A-battery is A01 `source_slug_links`, A02/A03 `item_population_links`, A04 `spec_value_probes`, A05 `evidence_population_match`, A06 `bpc_metadata`, A07 `citation_mining`, A08 `item_population_elaborations`, A09 `evidence_sources.superseded_by_ref_id`, A10/A11 `cell_source_links`, A12/A13 `search_admissions`. And `grep -c foreign_key_check scripts/tests/test_db_integrity.py` → **0**. |
| 2 | `slug` resolves to a real slug | `slug` | **D(fk)** | Declared FK to `slugs(slug)`; same mechanism as #1 |
| 3 | `claim_type ∈ {numerical, range, qualitative, framework, absent}` | `claim_type` | **D** | SQLite CHECK — refuses at insert, every connection |
| 4 | `claimed_value` present ⟺ `claim_type ≠ 'absent'` | `claimed_value` | **D** | Table-level compound SQLite CHECK |
| 5 | `extraction_method ∈ {skim, full-read, re-read, auto-mined}` | `extraction_method` | **D** | SQLite CHECK |
| 6 | `extraction_status ∈ {preliminary, reviewed, verified, contradicted, absent-confirmed}` | `extraction_status` | **D** | SQLite CHECK |
| 7 | A locator is recorded | `source_section` and/or `loc_*` | **UNENFORCED** | R3's enforcer reads `evidence_sources.article_number`/`.pages`, never this table; no check reads any `loc_*` column anywhere |
| 8 | `[UNVERIFIED-QUANT]` present when no locator | `notes` | **UNENFORCED for this table** | R3 scans `evidence_sources.notes` only |
| 9 | `item_code`, if set, belongs to the row's slug | `item_code` | **4 blocking** | `test_db_integrity` **J01** — genuine registered blocking check; but see (d), it passes on the realistic same-slug error |
| 10 | `item_code` agrees with any probe its `root_classification_basis` names | `item_code` | **4 blocking** | `test_db_integrity` **J02** (text `LIKE` join) |
| 11 | `root_type` set, from the 5-value vocabulary | `root_type` | **D for vocabulary · UNENFORCED for presence** | SQLite CHECK constrains values; column is nullable and nothing requires it. `v_value_independence` silently drops NULLs — under-counting, not a gate |
| 12 | A `root_id` with no `root_ref_id` is registered | `root_id` ↔ `external_root_registry` | **2 audit (view only)** | `v_unregistered_roots` — a view; **no registered check queries it** |
| 13 | One in-corpus source ⇒ one `root_id`, and vice versa | `root_ref_id` ↔ `root_id` | **2 audit (view only)** | `v_root_id_conflicts`; **no registered check queries it** |
| 14 | `measurement_paradigm` ∈ 9-value vocabulary | `measurement_paradigm` | **D (vocabulary only)** | SQLite CHECK; column nullable |
| 15 | `device_class` ∈ 9-value vocabulary | `device_class` | **D (vocabulary only)** | SQLite CHECK; column nullable |
| 16 | `contested ∈ {0,1}` | `contested` | **D** | SQLite CHECK, NOT NULL DEFAULT 0 |
| 17 | Population membership is expressed relationally | `extraction_population_links` | **3 CI non-blocking** | `population_integrity_audit` (**advisory**, battery `research`) — scalar↔junction consistency only; **does not require a junction row to exist** |
| 18 | The row validates against its Pydantic model | `schemas/source_value_extraction.py` | **3 CI non-blocking, structurally incomplete** | `validate_pydantic_schemas --strict` (advisory) — and its own output reports the model is missing all 11 genealogy columns, so passing it certifies nothing about the genealogy |
| 19 | `derivation_paths` / `functional_basis` recorded | — | **DESIGNED-ONLY** | Columns do not exist; `pipeline-contract.yaml judgment/derivation-handshake` → `check: null` |

##### 7-B · A `jurisdictional_values` row

| # | Condition | Column / field | Level | Named enforcer |
|---:|---|---|---|---|
| 1 | `item_code` resolves | `item_code` | **D(fk)** | Declared FK to `items(item_code)`; differential check in `migrate_db.py`; CI via `migration_reproducibility` (blocking) |
| 2 | `(item_code, jurisdiction, standard_name)` is unique | — | **D** | SQLite UNIQUE — enforced at write time, every connection |
| 3 | `evidence_tier` is 6 | `evidence_tier` | **1 text rule** | Column `NOT NULL DEFAULT 6`, no CHECK. All 109 rows are 6 in fact; a 3 would insert cleanly |
| 4 | `is_code_minimum ∈ {NULL, 0, 1}` | `is_code_minimum` | **D** | SQLite CHECK |
| 5 | A clause/section locator is recorded (R3) | `source_section` | **1 text rule** | 109/109 populated in fact; **no CHECK, no NOT NULL, no registered check**. `DR-2026-08-06` §3 cites the 109/109 as its reason to keep the table — an observation, not a gate |
| 6 | `jurisdiction` is a canonical code | `jurisdiction` | **UNENFORCED** | No FK, no CHECK. **20 rows carry `'GB'`**, which `schemas/enums.JurisdictionCode` does not contain (it has `UK`) and which `scripts/validate_jurisdiction.py`'s own docstring says is *"GB rejected (must be UK)"* — but that **blocking** check never opens the database (`grep -c "sqlite3\|guidebook.db" scripts/validate_jurisdiction.py` → 0; run → `PASS: 0 errors, 55 warnings`, exit 0). Full distribution: DE 20, GB 20, US 20, AU 18, ISO 13, FR 5, NO 5, EU 4, CA 1, CH 1, JP 1, SG 1 |
| 7 | `spec_id` resolves | `spec_id` | **UNENFORCED, and unenforceable** | 26 non-NULL values; no specifications table exists. The spine's ENT-01 hop has no table |
| 8 | YAML mirror record count matches the table | `data/jurisdictional_values/` (21 files) | **4 blocking** | `test_db_integrity` **L02** — genuine registered blocking check; **count parity only**, never content |
| 9 | Values are traceable to a source record | — | **N/A by ratified decision** | `DR-2026-08-06` §3, class-relative adequacy; no `ref_id` by design. Not a gap to close — a boundary to respect |
| 10 | Same-(item, unit) values across jurisdictions are adjudicated | — | **2 audit, non-gating** | `jurisdictional_divergence.py`, registry-**quarantined** as a report: *"Its exit code carries no verdict."* Currently 12 items `unadjudicated_divergence` |
| 11 | Locator hierarchy decomposed | 16 `loc_*` columns | **DESIGNED-ONLY** | 0/109 populated on every one of the sixteen; splitting migration is owner-gated and unwritten |

##### 7-C · A `reasoning_doc_citations` row

| # | Condition | Column / field | Level | Named enforcer |
|---:|---|---|---|---|
| 1 | `source_ref_id` resolves | `source_ref_id` | **D(fk)** | Declared FK to `evidence_sources(ref_id)`, NOT NULL; differential check via `migrate_db.py`; CI via `migration_reproducibility` (blocking) |
| 2 | `reasoning_doc_slug` resolves | `reasoning_doc_slug` | **D(fk)** | Declared FK to `slugs(slug)`, NOT NULL; same mechanism |
| 3 | numeric/jurisdiction claim ⇒ `claimed_value` + `value_match`; qualitative/definitional ⇒ `claim_text` + `claim_match` | compound | **D** | Table-level SQLite CHECK |
| 4 | `value_match` / `claim_match` drawn from the closed vocabularies | both | **D** | SQLite CHECKs (6 values / 5 values) |
| 5 | `paywall_purchase_candidate ∈ {0,1}` | same | **D** | SQLite CHECK, NOT NULL DEFAULT 0 |
| 6 | No `NOT-FOUND` / `CONTRADICTED` row ships | `value_match`, `claim_match` | **3 CI non-blocking** | `reasoning_doc_citations_audit` CHECK 1/2 (**advisory**) — 0 rows today |
| 7 | PAYWALL rows carry a downgrade or corroboration note | `notes` | **3 CI non-blocking** | same audit, CHECK 3 |
| 8 | Cited source is synthesis-eligible (`metadata_quality ≠ 'AUTHOR-TITLE-ONLY'`, `verification_status` non-NULL) | joined | **3 CI non-blocking** | same audit, CHECK 4; also `metadata_integrity_audit` (advisory, basis `collection/evidence-verification-gate`) |
| 9 | `source_section` recorded | `source_section` | **3 CI non-blocking** | same audit, CHECK 5 |
| 10 | Model parity | `schemas/reasoning_doc_citation.py` | **3 CI non-blocking** | `validate_pydantic_schemas --strict` → `OK … <-> reasoning_doc_citations` (34/34) |

> **Registry-note drift, recorded here because it inverts the vacuity guard.**
> `reasoning_doc_citations_audit`'s registry note says *"the other checks are clean over 14 rows"*;
> the run prints `Total rows: 0`. `population_integrity_audit`'s note says *"RED on main
> (31 issues)"*; the run prints `ISSUES: 0`. `adjudication_integrity`'s quarantine reason says
> *"RED — 274 tier inconsistencies"*; the run prints `VERDICT: PASS (tier inconsistencies=0)`.
> All three were true before the clean-room reset. This is the registry asserting findings over
> an emptied subject — the mirror image of a check passing over one.

---
---

### 2.8 Stage 8 — Population matching & directness

*Substrate: `evidence_population_match`, the three `*_population_links` junctions,
`schemas/directness.py`, the grain × design-scale matrix.*

#### (a) Tools, tables, methodology

**Tables**

| Object | Rows | State | Notes |
|---|---:|---|---|
| `evidence_population_match` | 0 | **BUILT+UNEXERCISED** | 11 columns. `match_grade TEXT NOT NULL CHECK(match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH'))`. Carries **two** source keys: `source_ref TEXT NOT NULL` (no FK) and `ref_id TEXT REFERENCES evidence_sources(ref_id)` (nullable). `target_population TEXT NOT NULL` — no FK, no CHECK. Also `gap_id TEXT REFERENCES gaps(gap_id)`, and `created_by_session TEXT NOT NULL`. |
| `extraction_population_links` | 0 | **BUILT+UNEXERCISED** | Migration 021; PK `(extraction_id, population_code)`, both FK'd |
| `citation_population_links` | 0 | **BUILT+UNEXERCISED** | Migration 021 |
| `probe_population_links` | 0 | **BUILT+UNEXERCISED** | Migration 021 |
| `populations` | **23** | **BUILT+EXERCISED** | Self-referencing `parent_code` |
| `axes` / `access_needs` / `population_axis_map` / `access_need_axis_map` | 17 / 17 / 53 / 21 | **BUILT+EXERCISED** | The functional-axis layer `DR-2026-07-22-work-from-axes` makes primary |

**Modules**

- `schemas/directness.py` — **BUILT+EXERCISED.** The model: 3 scales, 3 grains, 3 dimensions,
  4 consolidated conditioning grades. `scale_directness(grain, scale)` is the grain × design-scale
  matrix in code. `consolidate()` is the combining rule. `directness_from_primitives()` is the
  single entry point. `check_directness_record()` is the vocabulary audit. Its BOUNDARY note is
  explicit: *"This module is the model. Storage of the consolidated directness — including a
  `scale_directness` column — is Stage 2.3's `evidence_cell_state` / `convergence_assessment`
  tables."*
- `schemas/population_links.py` — **BUILT+UNEXERCISED**; all three junction models report `OK`
  against their tables under `validate_pydantic_schemas --strict`.
- `schemas/enums.PopulationCode` — **BUILT, DRIFTED.** `assess_cell.validate_population()` carries
  a comment recording the drift ("the enum's 25 values do not match the table's 22 codes");
  `SELECT COUNT(*) FROM populations` → **23**, so the comment is itself stale in the third
  direction.

**Scripts and checks**

| Item | State | Evidence (run 2026-08-11) |
|---|---|---|
| `scripts/tests/test_directness_2_2.py` | **BUILT+EXERCISED (partially vacuous, declared)** | `ALL PASS (0 failed)`, 31 assertions, plus `[SKIP] live smoke — /tmp/work14.db absent`. Registered **advisory**, battery `tests`, kinds `tooling, data`. The registry note declares the skip: *"Partially vacuous by design … Recorded so the pass is not read as broader than it is."* It **does** call `check_directness_record()` (lines 101 and 111). |
| `scripts/audit/matrix_consistency.py` | **BUILT+EXERCISED** | `PASS: 10/10 outcomes match evidence-architecture.md §3`, exit 0. Registered **advisory**, battery `governance`, kinds `governance, schema`, basis `render/mode-stratum-matrix-consistency`. **The only check in stages 7–9 that verifies doctrine against code over a non-empty subject.** |
| `scripts/audit/population_integrity_audit.py` | **BUILT+UNEXERCISED** | Exit 0, `ISSUES: 0`, all legs 0 rows. Registered **advisory**. |
| `scripts/audit/research_batch_dod.py` rule **R13** | **BUILT+UNEXERCISED (vacuous)** | Lines 479–497: for every `evidence_sources` row with tier 1–3, require an `evidence_population_match` row keyed by `ref_id`. Output verbatim: `R13: PASS — all 0 tier-1..3 admissions carry a graded population match`. |
| `scripts/validate_population.py` | **BUILT** | Registered `validate_population`, **advisory**, battery `schema` |
| `scripts/assess/assess_cell.py::population_match()` | **BUILT+UNEXERCISED** | The only consumer of `evidence_population_match` in the determination path |

**The grain × design-scale matrix** (`evidence-architecture.md` §3; reproduced verbatim from the
`matrix_consistency.py` run, doc and code columns identical on all ten):

```
aggregate × person      DOWN-WEIGHTED
aggregate × population  DIRECT
aggregate × universal   ADJACENT
code      × person      NON-ANCHORING
code      × population  NON-ANCHORING
code      × universal   DIRECT
specific  × person      DIRECT
specific  × population  DIRECT      (DOWN-WEIGHTED if generalizes_beyond_measured)
specific  × universal   ADJACENT
```

#### (b) How they relate to each other

**The three dimensions and their substrates** (`schemas/directness.py` docstring, lines 19–26):

| Dimension | Substrate table.column | Rows today |
|---|---|---:|
| population-directness | `evidence_population_match.match_grade` | 0 |
| value-directness | `reasoning_doc_citations.value_match` (+ `spec_value_probes.passes_strict` corroboration; home substrate `source_value_extractions`) | 0 / 0 / 0 |
| scale-directness | computed — `scale_directness(grain, claim_scale)`; **no substrate** | n/a |

Grain is **derived, not stored**. `GRAIN_FROM_EVIDENCE_TYPE` maps the 8 `evidence_type` values to
3 grains; verified live:

```
{'sr_meta':'aggregate', 'co2':'aggregate', 'clinical':'specific', 'co1':'specific',
 'grey':'specific', 'standard_eb':'code', 'national_fw':'code', 'code':'code'}
```

`assess_cell.source_grain()` overrides that map **engine-side** for G3 (Co-1 grain follows
`co1_source_type`) and G6 (`standard_eb` grain follows tier: T2 → aggregate, T4/T5 → code),
tagged `rule_version="pilot-2"` so the PROPOSED doctrine does not silently change
`schemas/directness.py` before ratification. **This is a real fork:** the schema module and the
engine disagree about `standard_eb`, and `matrix_consistency.py` checks only the schema module.

`consolidate()` rule order (most restrictive first):

1. scale `NON-ANCHORING` → `NON-ANCHORING`
2. population `MISMATCH` or value `CONTRADICTED` → `DISCOUNTED`
3. every applicable dimension at full grain-match → `DIRECT`
4. otherwise → `DOWN-WEIGHTED`

**`None` means "not applicable — does not block"** (`pop_full = population_directness in
(POP_EXACT, None)`). Reproduced live: `consolidate(None, None, 'DIRECT')` → `DIRECT`. That is
exactly the G2 hazard: an *unassessed* dimension grades as fully direct. `evidence-architecture.md`
§4 G2 states the fix and its reason — *"only 27 of 640 sources carry any
`evidence_population_match` row — so at backfill scale, 'never assessed' would silently grade as
fully direct"* (a ratio now stale in both terms, post-reset, but the argument is unaffected).
The fix is implemented **only in `assess_cell.py`**, via a module-level constant
`NOT_ASSESSED = "NOT_ASSESSED"` (line 84) deliberately *not* added to `schemas/directness`'s
vocabulary, which makes `pop_full` False and caps consolidation at `DOWN-WEIGHTED`. So
`schemas/directness.consolidate()` still carries the pre-G2 semantics for every other caller.

**The join into `evidence_population_match` is by text.** `assess_cell.population_match()`
(lines 168–182) selects rows by `ref_id`, then attributes each to a population with
`re.search(rf"\b{re.escape(population)}\b", target_population, re.I)` against the free-text
`target_population` column. The docstring says why, and says it well: *"`target_population` is
free text, so attribution is conservative: the row must name the population code as a word …
Rows that exist but cannot be attributed to this population are NOT evidence of directness for
it — the dimension stays NOT_ASSESSED."* There is no FK from `evidence_population_match` to
`populations` and no junction table for it.

**The dual source key is an unchecked back door.** `source_ref` is `NOT NULL` with no FK;
`ref_id` is nullable with an FK. `test_db_integrity` **A05** checks `ref_id` only
(`WHERE ref_id IS NOT NULL AND NOT EXISTS (…)`), R13 queries `ref_id`, and
`assess_cell.population_match()` queries `ref_id`. So a row whose `source_ref` names a
nonexistent source and whose `ref_id` is NULL **satisfies every check and is seen by nobody.**

**Junctions.** Migration 021's header states the design: the three junctions replace
comma-separated free text (`'AUT, PCS, DEM, MH, PAIN, OFS'`); the scalar columns are "RETAINED
but DEPRECATED … kept in sync (denormalized) as a transition convenience"; and
`population_integrity_audit.py` is the companion Level-2 audit for scalar↔junction consistency.
Note that `evidence_population_match` was **not** given a junction —
`SELECT name FROM sqlite_master WHERE name LIKE '%population_links'` returns
`citation_population_links`, `probe_population_links`, `extraction_population_links` only. It is
the one population-bearing table still on free text.

#### (c) Relation to the previous stage (7)

**Entry contract as designed.** Directness may be assessed once (i) the source exists and is
tier-classified, (ii) its `evidence_type` and `scope` are set (grain derives from `(type, tier)`
per G6, and `scope` is what `tier_derivation.check_tier_consistency()` validates), (iii) for Co-1,
`co1_source_type` is set (G3 grain), and (iv) a value claim exists to grade value-directness
against.

**What actually enforces it:**

- **R13** (`research_dod`, **advisory**) is the only rule that requires a match row, and it fires
  per *admission*, not per extraction. Vacuous at 0 sources.
- `test_db_integrity` **A05** (**blocking**): `evidence_population_match.ref_id` →
  `evidence_sources`. Genuine, registered, blocking — and partial, per (b).
- `population_integrity_audit` (**advisory**): junction codes canonical, scalar↔junction
  consistent. Does **not** require a junction row to exist.
- **NOTHING ENFORCES** that a source has `co1_source_type` set before its Co-1 grain is computed.
  `assess_cell.source_grain()` falls through to `GRAIN_SPECIFIC` with the note
  `"G3:individual-grain co1"` for any unrecognised value, including NULL. G3's own text says
  `peer_reviewed_literature` and `validated_tool` should *"default per the study's own design,
  recorded per source"*; the code does not distinguish them.
- **NOTHING ENFORCES** that value-directness has a substrate. `assess_cell` hard-codes
  `val = NOT_ASSESSED` for every source (line 200), with a comment locating the blocker precisely:
  *"What is still absent is any assessment RULE for grading a value dimension from them — writing
  one is a judgment act, not a caller sweep."*

#### (d) Relation to the next stage (9)

**Exit contract as designed.** A cell determination may consult a source only with its
conditioning grade in hand; `anchoring()` in `assess_cell.py` drops any source whose conditioning
is `NON-ANCHORING` or `DISCOUNTED`, and `convergence_assessment` has dedicated columns
`down_weighted_sources` and `discounted_sources` to record the rest.

**What actually enforces it:**

- `validate_evidence_state` (**blocking**, battery `schema`, kinds `schema, data, synthesis`):
  `validate_convergence_db()` enforces that a `discounted_sources` entry is not also listed as
  anchoring (`overlap = set(disc) & anchoring`). **This is the one directness rule with blocking
  enforcement — and it fires only if the assessor already recorded the source as discounted.
  Nothing checks that the discount was computed.**
- `matrix_consistency` (**advisory**): doctrine ↔ `schemas/directness.py` agreement, 10/10.
- **NOTHING ENFORCES** that `evidence_cell_state` records the conditioning at all.
  `schemas/directness.py`'s BOUNDARY note assigns storage to Stage 2.3, and **Stage 2.3 did not
  build it**: `PRAGMA table_info(evidence_cell_state)` returns 27 columns, none named
  `scale_directness`, `population_directness` or `conditioning`. The consolidated grade is
  computed in memory by `assess_cell` and survives only as
  `convergence_assessment.down_weighted_sources` / `.discounted_sources` JSON arrays.
  **DESIGNED-ONLY storage.**
- **NOTHING ENFORCES** G2 at the cell level. No check anywhere requires that a source anchoring a
  `stated` cell carries an `evidence_population_match` row.

#### (e) The goal of the stage

Stage 8 answers *"does this source's evidence apply to the people, and at the resolution, this
claim is about?"* — as a categorical conditioning layer over a single ladder, never as a second
ladder and never as a number. Two distinct questions live here. **Population-directness** asks
whether the population studied is the population served: a chamber-emissions test with no human
participants filed against a chemical-sensitivity population is `PROXY`, not `EXACT`, and R13's
LESSON comment records both real instances by name (Jinno 2007, a chamber emissions test with no
human participants, filed against COM; Amos 2019, a general-population autistic-*traits* sample,
filed against AUT — *"Both are legitimate as PROXY evidence and dangerous as anything else."*).
**Scale-directness** asks whether the evidence's grain matches the claim's grain,
*bidirectionally* — the project's explicit rejection of a specificity gradient. An aggregate
systematic review is the *right* grain for a population claim and the *wrong* grain for an
individual; a single-subject intervention study is the reverse. That bidirectionality is GRADE's
indirectness domain applied in both directions.

The stage's deepest commitment is negative: **absence of assessment is never evidence of
directness.** That is G2, and it is the Altman & Bland rule turned on the project's own metadata.

#### (f) How the tools support that goal — and where they do not

**Where they do.** `schemas/directness.py` is the most complete artifact in stages 7–9: a clean
model, a full unit-test suite (31 assertions, all passing, including one that exercises
`check_directness_record()` directly), and a doctrine-vs-code sweep (`matrix_consistency.py`,
10/10) that runs green in CI over a non-empty subject. The categorical-not-numeric choice is
defended in the module's own BOUNDARY note. The `generalizes_beyond_measured` flag encodes the
one asymmetry that would otherwise be lost — `specific × population` is DIRECT unless the study
over-claims.

**Where they do not.**

1. **The model has no storage.** The BOUNDARY note assigns it to Stage 2.3; Stage 2.3 built
   `evidence_cell_state` without a single directness column. Every conditioning grade the pilot
   engine computes is discarded except as two JSON ref-lists on `convergence_assessment`.
2. **G2 is engine-side only.** `consolidate(None, None, 'DIRECT')` → `DIRECT`, live, today.
   `test_directness_2_2.py` asserts this as correct behaviour
   (`[PASS] all-None -> None (nothing to condition on)`), so the registered test suite currently
   **pins** the pre-G2 semantics in the shared model while the engine overrides them locally.
3. **G6 is engine-side only, with a sharper consequence.** `GRAIN_FROM_EVIDENCE_TYPE['standard_eb']`
   → `'code'`, and `scale_directness('code','population')` → `NON-ANCHORING`. So for every caller
   except the pilot engine, **a T2 named-organisation evidence-based standard is NON-ANCHORING at
   Population Mode** — contradicting `evidence-methodology.md` §1.6 and §2.2 condition 2 (G7),
   which make exactly that source class a `stated` anchor.
4. **The population dimension is joined by regex on free text.** `target_population` has no FK, no
   CHECK, and no junction. Word-boundary matching on short population codes is fragile in both
   directions.
5. **The dual `source_ref` / `ref_id` key gives an unchecked back door** — see (b).
6. **The matrix check verifies 9 cells and one branch, and nothing else.** It does not verify
   `consolidate()`'s rule order, does not verify `GRAIN_FROM_EVIDENCE_TYPE`, and does not verify
   the G3/G6 overrides that only the engine implements. Its `EXPECTED` dict is a hand
   transcription; the script's own header names the discipline it depends on ("change BOTH the
   document and this table in the same commit").
7. **R13 is vacuous, and historically it was worse than vacuous.** Workplan §2.3 moved it from
   UNENFORCED to VACUOUS with the reasoning: *"Calling R13 '100%-observed practice' was compliance
   asserted over an empty set … `DR-2026-08-06` §1 records 824 of 863 sources with no recorded
   admission. The reset happened because R13 was not practised."* Workplan §4 fix 8 declines to
   harden R13 now, on the grounds that hard-coding a population-of-study grading obligation before
   `DR-2026-08-06` §3's class-relative correction lands would re-freeze the academic default the
   DR repudiated — **a T6 statutory code has no study population to grade.**

#### (g) How doctrine conditions the stage

**`governance/mission-and-epistemics.md`**

- **§Two orthogonal axes of coverage; directness as a conditioning layer** —
  *"**Directness is a conditioning layer over a single population-anchored ladder, not a separate
  hierarchy per scale.** … The project explicitly rejects a 'most-specific-to-least-specific'
  gradient: directness is grain-matching, not specificity-ranking."*
  **FORBIDS:** building a per-scale ladder; ranking sources by specificity; expressing
  conditioning as a confidence score.
- Same section — *"The Person scale is occupational-therapy resolution of the individual's own
  functional needs … the population range informs the assessment but does not bound the answer,
  which may fall outside it."* **FORBIDS** letting any population-grain source — including
  population-grain Co-1 — resolve a Person-Mode value.
- **Doctrinal commitment 1** — *"Population codes are organizing scaffolding, not a description of
  any individual within the population."*
- **Doctrinal commitment 3** — Co-1 is co-primary with Tier 1; *"The two answer different
  questions."* **FORBIDS** grading a Co-1 source down merely for being Co-1.

**`governance/evidence-architecture.md`**

- **§4** — the three dimensions, the four consolidated grades, the bidirectional principle.
- **§4 G2** — *"A NOT_ASSESSED dimension caps consolidation at DOWN-WEIGHTED and flags the source
  for assessment. Absence of assessment is never treated as evidence of directness."*
  **FORBIDS** grading an unassessed dimension as EXACT.
- **§4 G3** — Co-1 grain follows `co1_source_type`, with its ethical content explicit:
  *"a DPO position paper is community consensus — it anchors Population-Mode claims *and does not
  override an individual at Person Mode*; an individual narrative is the reverse."*
  **FORBIDS** letting population-grain community speech stand in for an individual.
- **§4 G6** — *"Grain assignment is a function of the (type, tier) pair."*
  **FORBIDS** grading `standard_eb` by type alone.
- **§3 footnote ††** — the two senses of "anchoring" are kept apart: mechanical grain-directness
  `NON-ANCHORING` is *unchanged by Option A*, which is a render/state-layer decision.
  **FORBIDS** reading Option A as a re-grain. (`DR-2026-07-21` §5: any re-grain of
  `schemas/directness.py` is a separately reviewed follow-up.)
- **§10 check 1** — the matrix sweep, *"each must be shown firing on injected bad data before its
  pass counts."*

**`governance/tier-system.md` §10 — the role-appropriate-authority gate.** *"A firm/architect
source can anchor a descriptive/measured claim … at its method strength, but **cannot anchor a
functional-need claim** ('disabled people need X / X works because Y') on its own — that requires
Co-1 (lived experience) or Co-2 (OT). A firm asserting a functional-need claim alone is flagged
'designer assertion, unadjudicated.'"* This is a directness-shaped rule with **no encoding**:
there is no `practice`/Co-3 `evidence_type` in `GRAIN_FROM_EVIDENCE_TYPE` and no check.
**DESIGNED-ONLY** — the section itself says the audit representation "is deferred to the audit
rework."

**Research contract R13** (while-searching): *"Grade population-of-STUDY vs population-SERVED on
every admission. No match row = silently claiming they are the same.
Children/general-population/no-participants = PROXY."*

**Decision Records.** `DR-2026-07-12-evidence-architecture-unification.md` (G1–G6) ·
`DR-2026-07-21-evidence-architecture-option-a-execution.md` §5 ·
`DR-2026-07-22-work-from-axes.md` (curate from functional axes; never coin population umbrellas —
`governance/functional-taxonomy.md` §3.3).

#### (h) ACCEPTANCE CONDITIONS — stage 8

##### 8-A · An `evidence_population_match` row

| # | Condition | Column / field | Level | Named enforcer |
|---:|---|---|---|---|
| 1 | `match_grade ∈ {EXACT, PARTIAL, PROXY, MISMATCH}` | `match_grade` | **D** | SQLite CHECK, NOT NULL |
| 2 | `ref_id`, when set, resolves to a source | `ref_id` | **4 blocking** | `test_db_integrity` **A05** — a genuine registered blocking check (`WHERE ref_id IS NOT NULL AND NOT EXISTS …`), backed by **D(fk)** on the declared FK |
| 3 | `source_ref` names a real source | `source_ref` | **UNENFORCED** | NOT NULL, **no FK**. A05 skips NULL-`ref_id` rows entirely; R13 and `assess_cell` both key on `ref_id`. A row keyed only by `source_ref` satisfies everything and is read by nothing |
| 4 | `target_population` is a canonical population code | `target_population` | **UNENFORCED** | Free text; no FK, no CHECK, no junction table. Consumed by `re.search(rf"\b{code}\b", …)` |
| 5 | `MISMATCH` / `PROXY` carries a note | `mismatch_note` | **UNENFORCED** | Nullable; no check |
| 6 | `study_population` / `sample_size` recorded | both | **UNENFORCED** | Nullable |
| 7 | `created_by_session` recorded | `created_by_session` | **D** | SQLite NOT NULL — the one provenance guarantee this table gives |
| 8 | Every tier 1–3 admission has ≥ 1 row | — | **3 CI non-blocking, currently vacuous** | `research_dod` **R13** (advisory). Actual output string: `R13: PASS — all 0 tier-1..3 admissions carry a graded population match`. It carries no `EXAMINED:` line — that convention belongs to `citation_mining_completeness.py`, not here |
| 9 | `gap_id`, when set, resolves | `gap_id` | **D(fk)** | Declared FK to `gaps(gap_id)`; differential check in `migrate_db.py`; CI via `migration_reproducibility` (blocking). **No A-battery check covers `evidence_population_match.gap_id`** |

##### 8-B · A directness assessment (the record `directness_from_primitives()` returns)

| # | Condition | Field | Level | Named enforcer |
|---:|---|---|---|---|
| 1 | `population_directness` in vocabulary | — | **3 CI non-blocking** | `schemas.directness.check_directness_record()`, called by `scripts/tests/test_directness_2_2.py:101,111` — which **is** a registered check (`test_directness_2_2`, advisory, battery `tests`, kinds `tooling, data`) |
| 2 | `value_directness` in vocabulary; `PAYWALL` → `None` | — | **3 CI non-blocking** | same |
| 3 | `evidence_grain ∈ {aggregate, specific, code}` | — | **3 CI non-blocking**, plus `ValueError` at call time | same; `scale_directness()` raises on an unknown grain |
| 4 | `claim_scale ∈ {universal, population, person}` | — | **3 CI non-blocking**, plus `ValueError` at call time | same |
| 5 | `scale_directness` matches doctrine §3 | — | **3 CI non-blocking** | `matrix_consistency` (advisory), 10/10, doc column regenerated from `evidence-architecture.md` §3 |
| 6 | An unassessed *applicable* dimension caps at DOWN-WEIGHTED (G2) | — | **UNENFORCED in the shared model** | Implemented only in `assess_cell.py` via a local `NOT_ASSESSED` constant. `consolidate(None, None, 'DIRECT')` → `DIRECT`, and `test_directness_2_2` **asserts that as correct**, pinning the pre-G2 semantics |
| 7 | Co-1 grain follows `co1_source_type` (G3) | — | **UNENFORCED in the shared model** | `assess_cell.source_grain()` only; `GRAIN_FROM_EVIDENCE_TYPE['co1'] = 'specific'` unconditionally |
| 8 | `standard_eb` grain follows (type × tier) (G6) | — | **UNENFORCED in the shared model** | `assess_cell.source_grain()` only; `GRAIN_FROM_EVIDENCE_TYPE['standard_eb'] = 'code'` unconditionally, so a T2 named-org standard is NON-ANCHORING at Population Mode for every caller except the pilot engine — contradicting §2.2 condition 2 (G7) |
| 9 | The consolidated grade is stored | — | **DESIGNED-ONLY** | No `scale_directness` / `population_directness` / `conditioning` column exists on `evidence_cell_state` (27 columns, verified) |
| 10 | A discounted source is not also anchoring | `convergence_assessment.discounted_sources` | **4 blocking** | `validate_evidence_state.validate_convergence_db()` — genuine registered blocking check. Fires only on what the assessor recorded |

##### 8-C · A population junction row (`extraction_` / `citation_` / `probe_population_links`)

| # | Condition | Column / field | Level | Named enforcer |
|---:|---|---|---|---|
| 1 | `population_code` is canonical | `population_code` | **D(fk)** + **3 CI non-blocking** | Declared FK to `populations(population_code)` (deferred differential check, CI via `migration_reproducibility`), plus `population_integrity_audit` CHECK 1 — which is registered **advisory**, not blocking |
| 2 | Parent id resolves | `extraction_id` / `citation_id` / `probe_id` | **D(fk)** | Declared FK; `migrate_db.py` differential check; CI via `migration_reproducibility` (blocking) |
| 3 | Scalar column agrees with the junction | parent's scalar `population_code` | **3 CI non-blocking** | `population_integrity_audit` CHECK 2/3 (**advisory**) |
| 4 | A junction row *exists* for every population-bearing parent | — | **UNENFORCED** | The audit checks consistency, never presence |
| 5 | Model parity | `schemas/population_links.py` | **3 CI non-blocking** | `validate_pydantic_schemas --strict` → `OK` on all three link models |
| 6 | Codes curated from functional axes, not umbrellas | — | **1 text rule** | `governance/functional-taxonomy.md` §3.3; `references/project-standards.md` RULE 2026-07-22; `DR-2026-07-22-work-from-axes`. No mechanical check exists — and the `axes` (17) / `population_axis_map` (53) substrate that would make one possible is populated |

---
---

### 2.9 Stage 9 — Cell determination

*Substrate: `evidence_cell_state`, `convergence_assessment`, `cell_source_links`, `gaps`,
`assess_cell.py`, `validate_evidence_state.py`, the register map.*

#### (a) Tools, tables, methodology

**Tables and views**

| Object | Rows | State |
|---|---:|---|
| `evidence_cell_state` | 0 | **BUILT+UNEXERCISED** (15 pre-reset) |
| `convergence_assessment` | 0 | **BUILT+UNEXERCISED** (14 pre-reset) |
| `cell_source_links` | 0 | **BUILT+UNEXERCISED** (61 pre-reset) |
| `gaps` | 0 | **BUILT+UNEXERCISED** (313 pre-reset) |
| `weighting_profile` | **5** | **BUILT+EXERCISED** (seeded: designer/decision-frame, disabled_person/representation-checking, disabled_person/advocacy-brief, policymaker/jurisdiction-comparison, ot/specialist-handoff) |
| `v_best_practice`, `v_pending`, `v_code_floor_only`, `v_divergence`, `v_item_provenance` | 0 | **BUILT+UNEXERCISED** (all execute; all read `evidence_cell_state`) |

`evidence_cell_state` DDL, the columns that carry the doctrine (27 total):
`state` CHECK `('stated','provisional','pending','not_applicable')` · `design_scale` CHECK
`('universal','population','person')` · `convergence_id` FK · `gap_register_id` FK ·
`tier_basis` TEXT *(comment: `-- e.g. 'T1+CO1' / 'T3' / 'T6-only'` — **no CHECK**)* ·
`governing_refs TEXT CHECK (governing_refs IS NULL OR json_valid(governing_refs))` ·
`rule_version` · `derivation_sha` · `code_floor_only INTEGER NOT NULL DEFAULT 0 CHECK (0,1)` ·
`regulatory_stratum_only INTEGER NOT NULL DEFAULT 0 CHECK (0,1)` (migration 027) ·
`value_min` / `value_max` / `value_unit` · `falsification_condition` ·
`confidence_dimensions_present` / `_absent` / `confidence_synthesis_basis` ·
`not_applicable_rationale` · `has_unverified_sources` · `all_sources_disqualified` ·
`UNIQUE (item_code, population_code)`.

**The engine**

`scripts/assess/assess_cell.py` — **BUILT+UNEXERCISED, and currently unrunnable.** 625 lines,
`RULE_VERSION = "pilot-2"`. It is a *pilot* in three explicit senses:

1. **It refuses the canonical DB.** `python3 scripts/assess/assess_cell.py --db data/guidebook.db
   --emit-sql /dev/null` → `REFUSING: this engine never writes the canonical DB (owner-gated).`
   exit 1. `--db` is `required=True` with the help string *"pilot DB (NEVER the canonical
   data/guidebook.db)"*. It is one of the two documented exemptions in
   `scripts/audit/db_path_env_audit.py` (line 48).
2. **Its subject is a hardcoded 7-cell list** — `PILOT_CELLS` (lines 114–129): E-08×DEAF,
   E-12×MOB, G-03×MOB, C-02×DEM, E-06×MOB, G-03×SCI, B-10×NEU. Not a sweep over `items ×
   populations`, not over `item_population_links` (372 rows), not over the 2,139 possible cells.
3. **It does not write the DB it determines against.** It emits a replayable SQL artifact
   (`--emit-sql`) whose header says *"Replayable onto the canonical DB ONLY after owner
   ratification."*

**And post-reset it crashes**, reproduced on a scratch copy:

```
cp data/guidebook.db $SCRATCH/s2.db
python3 scripts/assess/assess_cell.py --db $SCRATCH/s2.db --emit-sql $SCRATCH/o.sql
 -> pydantic_core._pydantic_core.ValidationError: 1 validation error for EvidenceStateRecord
    gap_register_id
      Value error, gap_register_id must match GAP-NNN or GAP-NNNN, got: GAP-1
    EXIT=1
```

An empty `gaps` table makes `next_gap_id()` return `GAP-1`, which the model's regex rejects.
**Combined with (1), stage 9 has no runnable engine path at all today.**

**What has ever written a determination.** Not the engine, mostly. Reconstructed from migration
history:

| cell_ids | migration | `rule_version` | origin |
|---|---|---|---|
| 9001–9007 | `data_20260713000000_pilot-cell-backfill.sql` | `pilot-2` | engine artifact, replayed |
| 9008–9011 | `data_20260716220832_2026-07-16-pilot-rt60-cell-state.sql` | `phase-e-pilot-2026-07` | hand-authored |
| 9012 | `data_20260719003303_…-batch1-a02-grading.sql` | `batch1-2026-07-19` | hand-authored |
| 9013 | `data_20260719023539_…-batch1-a08-grading.sql` | `batch1-2026-07-19` | hand-authored |
| 9014 / 9015 | `data_20260724…vestibular-phase-b.sql` | `vestibular-phase-b-2026-07-24` (labelled retroactively) | hand-authored |

Only **7 of the ~15** determinations ever written came from the engine. There is no production
determination path; every determination that has existed in the canonical DB arrived through a
hand-reviewed data migration.

**Validators and checks**

| Item | Level | State | Evidence (run 2026-08-11) |
|---|---|---|---|
| `validate_evidence_state` (`scripts/validate_evidence_state.py`) | **blocking**, battery `schema`, kinds `schema, data, synthesis`, basis `judgment/governing-refs-nonempty` + `judgment/no-regulatory-stratum-stated` + `judgment/tier3-alone-threshold` | **BUILT+UNEXERCISED (vacuous today)** | `OK cell-state machine: 0 cells, 0 convergence rows validated from guidebook.db` / `PASS: 0 records checked, 0 errors, 0 warnings`. `min_items:` is **absent** from its registry entry |
| `scripts/tests/test_validate_evidence_state_2_4.py` | advisory, `tests` | **BUILT+EXERCISED** | fixture-driven |
| `scripts/tests/test_evidence_cell_state_2_3.py` | advisory, `tests` | **BUILT+EXERCISED, `:memory:` only** | `sqlite3.connect(":memory:")` at line 68. It mutation-tests the *constraint text*; it asserts nothing about rows in `data/guidebook.db` |
| `scripts/tests/test_assess_cell_pilot.py` | advisory, `tests` | **BUILT+EXERCISED** | `PASS: all pilot-engine branch tests`, exit 0. **Imports `determine` only** — never `main()`, so the DB-insert path, `next_gap_id()` and `validate_with_models()` are untested (which is why D-9.3 was not caught by it) |
| `scripts/tests/test_db_integrity.py` | **blocking**, `db_integrity` | **BUILT+EXERCISED** | `RESULTS: 70/70 checks passed`. Relevant: **A10/A11** (`cell_source_links` FKs), **C10**, **H01/H02**, **H06/H07**, **K01**, **L02** |
| `migration_reproducibility` | **blocking**, `data` | **BUILT+EXERCISED** | C1 shells out to `migrate_db.py --rebuild`; C2 compares `PRAGMA user_version`; C3 compares `COUNT(*)` over 7 core invariants (`evidence_sources`, `citation_mining`, `source_slug_links`, `gaps`, `connections`, `items`) |
| `scripts/audit/register_integrity_check.py --selftest` | advisory, `render` | **BUILT, SELFTEST FAILING** | exit **1**; 11 mutations FIRED, one `**SILENT — MUTATION MISSED**: COMPLETENESS: a whole cell section deleted`, then `SELFTEST FAILED — a tampered invariant went undetected` |
| `scripts/audit/jurisdictional_divergence.py` check 5 | level 2, unregistered | **BUILT+EXERCISED** | 12 items `unadjudicated_divergence` — the 7→9 handoff measured from the stage-7 side |
| `scripts/audit/adjudication_integrity.py` | quarantined | **BUILT+UNEXERCISED** | `evidence_cell_state: 0 determination cell(s)` |
| `tools/pipeline_completeness.py` (`--check` as `pipeline_completeness_fresh`) | **blocking**, `render` | **BUILT** | Not run here — it is a generator behind a freshness gate and writes derived artifacts. Its `0/372` denominator matches `item_population_links` = 372 |
| `scripts/audit/table_connectivity.py` | quarantined | **BUILT+EXERCISED** | `7 spec has a cell 0/80` · `8 BEST PRACTICE 0/80` |

#### (b) How they relate to each other

##### The doctrinal core: tier basis → state → flag → band → marker

This is the highest-value content in this segment, and it survived adversarial attack intact.
It is assembled from `governance/evidence-methodology.md` §2.2/§2.3,
`governance/evidence-architecture.md` §3 ††/§5/§6, `governance/tier-system.md` §5/§8 as amended
by Option A, and `mission-and-epistemics.md` commitment 2 — and verified against
`assess_cell.determine()` and `scripts/generate/pilot_renderings.tuple_class()`.

| Governing (anchoring) basis | State | `code_floor_only` | `regulatory_stratum_only` | `design_scale` | Determination band | Register-map key |
|---|---|:--:|:--:|---|---|---|
| T1 (primary clinical, tier 1) alone | `stated` | 0 | 0 | population | **● full** | `stated_single_axis` |
| Co-1 alone, `verification_status='VERIFIED'` | `stated` | 0 | 0 | population | **● full** | `stated_single_axis` |
| T2 alone — *either* stream, `sr_meta` **or** `standard_eb`@T2 (G7) | `stated` | 0 | 0 | population | **● full** | `stated_single_axis` |
| Co-2 alone | `stated` | 0 | 0 | population | **● full** | `stated_single_axis` |
| ≥ 2 of {clinical, co1, co2} axes | `stated`, convergence `pending_assessment` | 0 | 0 | population | **● full** | `stated_multi_axis` (carries the G8 value-convergence-pending disclosure) |
| T3-**clinical** alone | `provisional` | 0 | 0 | population | **●** at source level, cell flagged | `provisional_t3` |
| T3-**grey** alone | `pending` + gap | 0 | 0 | — | — | `pending` |
| T4/T5 only, meets §2.3 richness | `provisional` | 0 | **1** | **universal** | **○ weak** | `rso_weak_broad` / `rso_weak_single` |
| T4–T6 mixed, meets richness | `provisional` | 0 | **1** | **universal** | **○ weak** | `rso_weak_*` |
| T6 only, ≥ 3 codes across ≥ 3 jurisdictions | `provisional` | **1** | **1** | **universal** | **○ weak** | `rso_weak_*` |
| T4–6 present but **below** §2.3 richness | `pending` + gap | 0 / 1 | **1** | **universal** | — | `pending` |
| nothing | `pending` + gap | 0 | 0 | — | — | `pending` |

> **Note the second-to-last row.** A below-richness regulatory cell is `pending` **and** tagged
> `design_scale='universal'` **and** `regulatory_stratum_only=1` — the engine sets all three
> before the richness split (`assess_cell.py:370–381`: `elif regulatory: design_scale =
> SCALE_UNIVERSAL; regulatory_stratum_only = 1; code_floor_only = 1 if (b["t6"] and not
> b["t45"]) else 0`, then `if rich: … else: state = "pending"`). `tuple_class()` tests
> `state == "pending"` **before** `rso`, so it still routes to the `pending` register-map row.

**Which flag sets which.** `code_floor_only = 1 ⇒ regulatory_stratum_only = 1` by construction
(T6 ⊂ T4–6), from the same branch. `evidence-architecture.md` §5 says the same in words:
`regulatory_stratum_only` *"extend[s] migration 026's `code_floor_only`, which covers only the
T6-only case, to the full T4–6-only case."*

**§2.3 richness, exactly** (`evidence-methodology.md` §2.3, implemented in
`assess_cell.regulatory_richness()`, lines 251–274 — with the engine's own admissions of what it
does *not* check, taken from the rationale strings it emits):

- **≥ 1 T4** international standard (ISO, IEC, EN) *"with an evidence-based value directly
  addressing the parameter"* — the engine checks **presence only**, and says so:
  `">=1 T4 international standard present (§2.3; the clause's 'value directly addressing the
  parameter' is unverified — value extraction pending)"`; **or**
- **≥ 2 T4–T5** sources from **different jurisdictions** *with convergent findings* — the engine
  checks count ≥ 2 **and** distinct-jurisdiction ≥ 2, but **not** convergence:
  `">=2 T4-5 sources, distinct jurisdictions (§2.3)"`; **or**
- **≥ 3 T6** codes from **different jurisdictions** *converging on the same value or range* — the
  engine checks count ≥ 3 and distinct-jurisdiction ≥ 3, and says:
  `">=3 T6 codes from {n} distinct jurisdictions (§2.3; value-level convergence unverified —
  extraction pending)"`.

Below richness (a single T6, or divergent T6s) the cell is `pending`, per §2.3's last sentence:
*"the evidence is too sparse to synthesize even provisionally."*

##### Band assignment — the sentence that matters most

`tier-system.md` §8 and `evidence-architecture.md` §3 †† both state it, and **they agree**:

> **Band assignment at determination level:** a cell whose entire basis is T4–T6 takes ○ even
> where T4/T5 sources are present; the ◐ "current standards practice" band in the table above
> applies to individual T4/T5 *citations* within an otherwise-anchored cell, and to source-level
> `●◐○` markers (§5), which are unchanged (DR-2026-07-21 §2.3).
> — `tier-system.md` §8

> **Band assignment:** any `regulatory_stratum_only` cell renders at ○ weak even where T4/T5
> sources are present; §8's ◐ "current standards practice" band applies to individual T4/T5
> *citations* within an otherwise-anchored cell, and to source-level ●◐○ markers.
> — `evidence-architecture.md` §3 footnote ††

**So: three markers exist at source level; only two bands exist at cell level. There is no
determination-level ◐ band.** Source-level markers, `tier-system.md` §5 verbatim:

| Marker | Applies to |
|---|---|
| **●** confirmed evidence base | T1, T2 (sr_meta + standard_eb + co2), **T3 clinical**, Co-1, Co-2 |
| **◐** policy or standards basis only, not primary evidence | T4, T5 |
| **○** grey literature, expert consensus, thin base, unconfirmed | T3 grey, `[EXPERT CONSENSUS]`, `[THIN BASE]`, `[UNSUPPORTED]`, T6 (code-floor) |

Mechanically corroborated: `v_best_practice.strength_band` emits exactly two strings —
`CASE WHEN regulatory_stratum_only = 1 THEN 'weak' ELSE 'anchored' END`.

##### What is forbidden, stated precisely

**A T4–T6-only basis is never `stated`.** Three canonical sources say so, and a blocking
validator implements it:

- `evidence-architecture.md` §5: *"its state remains `provisional`, never `stated`."*
- `evidence-methodology.md` §2.3: *"Its state remains `provisional`, never `stated`."*
- `mission-and-epistemics.md` commitment 2 (amended 2026-07-21, Option A): a code-consensus
  best-practice claim is *"**not in error**; it is a weak-band (○) best-practice claim ('best
  practice as currently known'), valid only when flagged code-derived with the
  convergence-not-evidence caveat, never rendered unflagged or above the weak band. (An unflagged
  or above-weak-band code-consensus best-practice claim **is** still in error.)"*
- `scripts/validate_evidence_state.py:262–270` (**blocking**) checks the **column and the
  `tier_basis` suffix string**, so a pre-027 row is still caught:

```python
elif state == "stated":
    if code_floor_only: errors.append(… "a Tier-6-only cell can never be 'stated'")
    if rso == 1 or (tier_basis or "").endswith("(regulatory_stratum_only)"):
        errors.append(… "never 'stated' (G1b, unification DR ACCEPTED)")
```

**Every rendering carries the flag — not only best-practice-phrased ones.**
`evidence-architecture.md` §6, amended **I3**:

> **I3 (amended 2026-07-21, Option A — absolute form repealed) — Regulatory-stratum-only cells
> carry no *unflagged* and no *above-weak-band* best-practice language,** in any register, under
> any weighting profile. **Every rendering of such a cell's value — whether or not it uses
> best-practice phrasing —** must carry the weak/code-derived flag and the
> convergence-not-evidence caveat, and no rendering may exceed the register map's
> `(provisional, regulatory_stratum_only)` row.

**I5** supplies the ceiling and forecloses the brevity escape:

> A register may say *less* than the maximum (brevity), never *more* (inflation). Brevity never
> licenses omission of an integrity flag or caveat mandated by I3, G8, or the cell's map row.

**And where anchoring evidence exists, weak-band code-derived phrasing is unavailable at all** —
`tier-system.md` §8.1, on the corridor-width case: *"calling 1800mm 'best practice' remains
forbidden here in every register (weak-band code-derived phrasing exists only for cells with *no*
anchoring evidence)."*

The six register-map keys, verified live
(`from pilot_renderings import REGISTER_MAP; sorted(REGISTER_MAP)`):
`['pending','provisional_t3','rso_weak_broad','rso_weak_single','stated_multi_axis',
'stated_single_axis']`. `tuple_class()` branches on `state == "pending"` first, then on `rso`,
then on `state == "provisional"` — which is why the `rso` flag failing to reach the row (below)
has a rendering consequence and not just a query consequence.

##### The wiring

```
                         source_slug_links ⋈ evidence_sources
                                    │  (assess_cell.gather_sources, by SLUG — not by item)
                                    ▼
                        assess_source() per source
                       grain(G3/G6) → scale_directness → consolidate
                                    │
                                    ▼
                classify() → {t1, co1, t2, co2, t3c, t3g, t45, t6}
                                    │
                                    ▼
                            determine()  ── pure function ──▶ derivation_sha
                                    │
              ┌─────────────────────┼──────────────────────┐
              ▼                     ▼                      ▼
   convergence_assessment   evidence_cell_state         gaps
      (explicit ids)          (explicit ids)        (next_gap_id)
                                    │
                                    │  governing_refs   = JSON array (TEXT)
                                    │  cell_source_links = junction (FK)  ← NEVER WRITTEN
                                    ▼
       v_best_practice / v_pending / v_code_floor_only / v_divergence
                                    ▼
              pilot_renderings.tuple_class() → REGISTER_MAP → 6 registers
```

**Facts about that wiring:**

- **`derivation_sha`** = `sha256("{item}|{population}|" + "|".join(sorted(governing_refs)) + "::"
  + RULE_VERSION)`. It attests *cell identity + governing set + rule version* — **not** the state,
  not the tier basis, not the sources' tiers. A cell whose *state* changed while its governing set
  did not keeps its sha unchanged. `test_db_integrity` **K01** recomputes it; its comment records
  that two live cells had gone stale from ordinary maintenance (a `NEU→BRAIN` population rename; a
  governing-set narrowing). K01 treats a NULL sha as `unattested` and **reports rather than
  fails** — observed on the injected fixture: *"1 determination(s) carry no sha or no rule_version
  and are unattested — reported, not failed (owner question)."*
- **`rule_version` has two downstream readers, not one.** `test_db_integrity` K01 (blocking), and
  `register_integrity_check.py`, which selects it (line 144) and carries it in the **I1
  determination tuple** (`rule_version=rv`, line 154; `("rule-version","rule_version")`, line 191)
  — so `rule_version` is part of the identity every register must render identically (advisory).
- **`governing_refs` and `cell_source_links` are dual stores of one edge.** Migration 044's header
  is unusually clear about why the junction exists: the JSON array *"cannot be foreign-keyed, so a
  ref that does not exist is indistinguishable from one that does … cannot be indexed … cannot be
  joined; there are nine of them today."* It deliberately did not drop the column (caller sweep
  across nine scripts + `v_best_practice`) and said *"a consistency check should hold them
  equal"* — which is `test_db_integrity` H01/H02. **`assess_cell.py` writes `governing_refs` and
  never writes `cell_source_links`** (`grep -c cell_source_links scripts/assess/assess_cell.py`
  → **0**), so any engine-produced cell fails H02 on arrival.
- **`regulatory_stratum_only` is computed and then dropped on insert.** `determine()` returns it;
  the report prints it; the INSERT column list (lines 563–569, 26 columns) contains
  `code_floor_only` and **not** `regulatory_stratum_only`. The historical pilot backfill had to
  compensate with `UPDATE evidence_cell_state SET regulatory_stratum_only = 1 WHERE tier_basis
  LIKE '%(regulatory_stratum_only)'` — **a string-suffix join standing in for a boolean the
  engine already knew.** The hand-authored path did it properly: the two `batch1-2026-07-19`
  migrations set `regulatory_stratum_only = 1` directly in the INSERT column list. **Only the
  engine drops the flag.**
- **The engine downgrades `v_best_practice`.** Lines 596–601 unconditionally
  `DROP VIEW IF EXISTS v_best_practice` and recreate the *pilot-2 interim* definition — no
  `strength_band` column, exclusion by `tier_basis NOT LIKE '%(regulatory_stratum_only)'`. Three
  migrations define the view (026 creates, 027 amends, 029 amends; 044 mentions it in a comment
  only), and the engine's interim definition sits between 026 and 027 — so running the engine
  against any DB **reverts the view by two amendments (027 and 029)**, losing Option A's
  queryable weak band.
- **`v_best_practice` still excludes `code_floor_only = 1`.** Live definition:
  `WHERE state IN ('stated','provisional') AND code_floor_only = 0`. Migration 029's header flags
  this deliberately: *"there are currently 0 `code_floor_only` cells, so the choice is moot for
  present data. Extending to `code_floor_only` is a one-line follow-up once the owner confirms
  intent."* So a **pure-T6 cell — the canonical Option A case — is still suppressed from the
  best-practice view**, while the T4–T6 superset surfaces. `code_floor_only = 1 ⇒
  regulatory_stratum_only = 1`, so the view filters on the strict subset and bands on the
  superset.

#### (c) Relation to the previous stage (8)

**Entry contract as designed** (`pipeline-contract.yaml`, stage `judgment`, `entry:` —
*"verified sources linked to an (item x population) cell"*):

1. **Sources reach the cell.** In practice they reach a **slug**, not a cell:
   `gather_sources()` queries `source_slug_links WHERE l.slug = ?`, and the slug→item mapping is
   *"manual … recorded there"* in `working/pilot/PILOT-MANIFEST.md` §3. The typed bridge is
   `item_bpc_links`, which `assess_cell`'s own gap description calls out as **"1/92 populated"**
   at pilot time (line 518) and which is **0 rows** today.
2. **Population directness assessed (G2).** Enforced only inside the engine.
3. **Value directness assessed.** Hard-coded `NOT_ASSESSED` for every source.
4. **Verification standing resolved.** `classify()` requires `verification_status='VERIFIED'` for
   Co-1 to count toward `stated` (§2.2 condition 3); `_is_disqualified()` implements D-0157's
   disposition-based disqualification, and `evidence-methodology.md` §2.8 gives the interaction
   table (an all-disqualified cell downgrades to `pending` and a gap entry is created).

**What actually enforces it:**

- `validate_evidence_state` (**blocking**), basis `judgment/governing-refs-nonempty`: a
  `stated`/`provisional` cell must carry a non-empty, well-formed JSON `governing_refs`.
  **It does not check that the refs resolve.** Reproduced on a scratch copy: a `stated` cell whose
  `governing_refs` is `["REF-99999"]` (no such source) →
  `OK cell-state machine: 1 cells, 1 convergence rows validated` / `PASS: 2 records checked,
  0 errors, 0 warnings`, exit 0 — and `SELECT cell_id, state, strength_band FROM v_best_practice`
  → `[(1, 'stated', 'anchored')]`.
- `test_db_integrity` **C10** (**blocking**): no published cell rests on a source that is not
  `VERIFIED`. Implemented as `JOIN evidence_sources e ON e.ref_id = j.value` — an **inner join**,
  so a `governing_refs` entry with no matching source is *dropped*, not flagged. On the same
  fixture, C10 passed.
- `test_db_integrity` **H02** (**blocking**): every `governing_refs` entry has a
  `cell_source_links` row. Combined with **A11** (`cell_source_links.ref_id` →
  `evidence_sources`) this *does* close the phantom-ref hole. On the same fixture, H02 **failed**
  — `RESULTS: 68/70`, `FAILED: [H02] cell_source_links ↔ governing_refs: every JSON entry is in
  the junction`. **So the hole is closed — but by a different check, in a different battery, keyed
  on a different store, and not by the check the pipeline contract names.**
- **NOTHING ENFORCES** G2 at the cell level: no check requires that a source anchoring a cell has
  an `evidence_population_match` row.
- **NOTHING ENFORCES** the `item_bpc_links` bridge: no check that a cell's sources are reachable
  from its item.

#### (d) Relation to the next stage (10 / 12 — synthesis and render)

**Exit contract as designed** (`pipeline-contract.yaml`, stage `render`, `entry:` —
*"determinations tagged with design_scale, ready to present per audience"*): a determination hands
off (i) `state` + `design_scale`, (ii) `tier_basis` + `governing_refs`, (iii) the convergence
tuple, (iv) `code_floor_only` / `regulatory_stratum_only`, (v) `rule_version` + `derivation_sha`,
(vi) `falsification_condition`, (vii) `value_min`/`value_max`/`value_unit`, and (viii) for
`pending`, a resolvable `gap_register_id`.

**What actually enforces it:**

- `register_integrity_check` (**advisory**, battery `render`, basis `render/register-invariants`):
  the amended I1–I5 over `working/pilot/pilot-renderings.html`, with a `--selftest` mutation
  harness. **Its selftest exits 1 today.** The completeness mutation is missed because
  `evidence_cell_state` has 0 rows, so `set(db_rows) - set(cells)` is empty whatever is deleted
  and the `if db_rows:` gate disables the doc→DB direction entirely. This is **vacuity, not
  deletion-blindness** — and the harness self-reports and exits 1 rather than passing silently,
  which is the right failure mode.
- `matrix_consistency` (**advisory**): the directness matrix, 10/10.
- `check_rendered_docs` (**blocking**, `render`) — and note its registry entry records that
  `min_items: 1` *"was added and RETIRED on 2026-08-06"*, because the reset made `specs/`
  reference-only: those briefs cite REF-ids the reset removed, deliberately, so `--all` now
  examines nothing **by decision**.
- `pipeline_completeness_fresh` / `evidentiary_audit_fresh` (**blocking**, `render`):
  derived-artifact freshness.
- **`value_min` / `value_max` are unenforced — but they have been used.** `assess_cell` inserts
  `None, None, None` for all three (line 559), so no *engine*-produced determination has ever
  carried a number. Five **hand-authored** determinations did:
  9008 `A-18×DEAF` 0.3/0.3 `'s'` · 9009 `A-18×ALL` 0.55/0.57 `'s'` · 9010 `A-18×DEM` 0.5/0.5
  `'s'` · 9012 `A-02×ALL` 0.90/0.935 `'NRC'` · 9013 `A-08×ALL` 25/25 `'NC'`. Nothing checks them
  either way.
- **NOTHING ENFORCES** `falsification_condition` presence, despite `evidence-architecture.md` §9
  listing it among the standing commitments and `mission-and-epistemics.md` commitment 6 sitting
  behind it.
- **NOTHING ENFORCES** direction-aware most-accommodating floor selection.
  `evidence-architecture.md` §5 carries its own tag: *"`[ENGINE-LAG → DR-2026-07-21 §5:
  assess_cell.py does not yet implement direction-aware selection, a direction=contested state, or
  per-parameter accessibility-direction metadata; this bullet states the ratified target.]`"*
  Confirmed: no such column, no such code. **DESIGNED-ONLY** — and it is the mechanism doctrine
  relies on for population-contested parameters (flush thresholds, acoustic absorption,
  illuminance), where §5 says *no single value is anchored* and the conflict routes to the
  `conflicts` machinery. `conflicts` = **0 rows**.

#### (e) The goal of the stage

Stage 9 is where the project makes a claim. It takes an (item × population) cell, gathers the
evidence that reaches it, applies the directness conditioning, and returns **one of four states**
plus everything a reader needs to argue with it: which sources govern, what tier basis they
constitute, whether the axes converge, what would overturn the claim, and — the load-bearing
distinction — whether the whole basis is regulatory, in which case the answer is *"best practice
as currently known, given that nothing stronger says otherwise"* at the flagged weak band, and
never anything more.

The stage exists to make one specific laundering impossible: turning "twelve jurisdictions agree"
into "best practice", unflagged. Option A (2026-07-21) changed the mechanism from *suppression* to
*mandatory flagging* — the value may now be rendered, but never unflagged, never above the weak
band, never with the caveat dropped. `evidence-architecture.md` §5 states why that is the stronger
form: scale-tagging plus the weak/code-derived flag make the laundering path *mechanically
impossible rather than editorially discouraged*. Note the symmetry the doctrinal test now carries
(`mission-and-epistemics.md` §Test, item 3): *"treating code consensus as the weak (○) band,
flagged, rather than as full strength **or as excluded**"* — **excluding** the weak band is now as
much a failure as inflating it.

The stage is also a **pure function**: same evidence + same `rule_version` ⇒ same state and same
`derivation_sha`. Determinism is not a nicety; it is what makes a determination auditable rather
than an opinion.

#### (f) How the tools support that goal — and where they do not

**Where they do.** `assess_cell.determine()` is a careful piece of work. It refuses the canonical
DB. It fixes its timestamps so a double run is byte-identical. It uses explicit cell ids rather
than autoincrement so the artifact is reproducible. Its `pilot-2` header enumerates the five
adversarial-review corrections that produced it, including one — *"pending cells no longer share
one constant sha"* — that would otherwise have made staleness undetectable across every `pending`
cell. It emits a rationale that *names its own unchecked clauses*. Its gap descriptions are
slug-scoped and say so: *"This records absence of a slug-link, NOT corpus-level absence."*
`regulatory_richness()` enforces jurisdiction **distinctness**, which is the checkable half of
§2.3's convergence clause, and declines to claim the other half. `classify()` never claims
`convergent` over ungraded values — it emits `pending_assessment`, which is the honest status, and
G8 exists so those cells render with mandatory disclosure rather than be hidden.

**Where they do not.**

1. **It is not wired.** No production path writes a determination. The engine's subject is 7
   hardcoded cells out of 2,139, it refuses the canonical DB by design, and post-reset it crashes.
2. **The Pydantic "gate before insert" validates almost nothing of what is inserted.**
   `validate_with_models()` runs `EvidenceStateRecord(...)` before every INSERT, but
   `validate_pydantic_schemas --strict` reports `DRIFT evidence_state.EvidenceStateRecord ↔
   evidence_cell_state · DB-only: ['cell_id','code_floor_only','confidence_dimensions_absent',
   'confidence_dimensions_present','confidence_synthesis_basis','convergence_id','created_at',
   'created_by_session','derivation_sha','falsification_condition','governing_refs',
   'population_code','regulatory_stratum_only','rule_version','tier_basis','updated_at',
   'updated_by_session','value_max','value_min','value_unit']` — 20 drift columns, of which
   **19 are among the 26 columns the engine actually inserts** (the twentieth,
   `regulatory_stratum_only`, is the one the engine drops). Every column that carries the doctrine
   is unknown to the model.
3. **The anti-hallucination gate is split across two checks, and the named one is the weaker.**
   `pipeline-contract.yaml` names `validate_evidence_state.py` for `governing-refs-nonempty`; that
   check verifies non-emptiness and JSON well-formedness only. The hole is closed by
   `test_db_integrity` H02 + A11 — a different check, a different battery, a different store.
4. **`code_floor_only` and `regulatory_stratum_only` are redundant and disagree in the view.**
   The strict subset is excluded from `v_best_practice`; the superset surfaces.
5. **`convergence_assessment` records axis co-presence, not convergence.** Its `status` vocabulary
   is `convergent / divergent / single_axis / pending_assessment`, but the engine can only ever
   produce `single_axis` and `pending_assessment`, because value-level agreement is ungradeable
   with `source_value_extractions` empty. `v_divergence` therefore cannot return a row the engine
   produced, and `validate_evidence_state`'s `divergent ⇒ rationale + synthesis_approach` rule is
   unreachable from the engine path.
6. **The `stated` threshold has inconsistent statements in canonical documents** — see the
   disagreement table below.
7. **Doctrine now understates its own state in the other direction.**
   `evidence-methodology.md` §2.3 says the Option A view follow-up landed and *"3 weak-band rows
   are queryable today"* — corrected on 2026-08-05 from a sentence that had understated the
   engine. Post-reset, `SELECT COUNT(*) FROM v_best_practice` → **0**. The sentence is stale in
   the third direction now; it is a prose count, and CLAUDE.md §10's rule applies.

#### (g) How doctrine conditions the stage

**`governance/mission-and-epistemics.md`**

- **Doctrinal commitment 2** (amended 2026-07-21, Option A) — quoted in full in (b).
  **FORBIDS:** an unflagged code-consensus claim; a code-consensus claim at ● or ◐;
  `state='stated'` on a regulatory-stratum-only cell.
- **Doctrinal commitment 3** — Co-1 co-primary; *"Where they diverge, the divergence is documented
  and a synthesis approach is specified per parameter."*
- **§Treatment of evidence convergence and divergence** — *"A synthesis that suppresses divergence
  is in error."* **FORBIDS** recording `single_axis` or `convergent` where axes actually disagree.
- **§Evidence-state machine** — the four states and their validator behaviours. **Its `stated` row
  reads *"Best practice derived from ≥Tier 3 OR Co-1 OR Co-2 evidence"*** (line 115), which
  contradicts `evidence-methodology.md` §2.2 and `DR-2026-07-12-tier3-stated-threshold`. See the
  disagreement table.
- **§Test against which all downstream decisions are evaluated**, item 3 — *"Does it grade best
  practice by the evidence hierarchy — treating code consensus as the weak (○) band, flagged,
  rather than as full strength or as excluded?"*

**`governance/tier-system.md`** — §3 (convergence-not-evidence, retained *as the weak-band honesty
rule*) · §5 (the three source-level markers) · §8 (the three bands and the determination-level
rule) · §8.1 (the corridor-width case: where anchoring evidence exists, weak-band code-derived
phrasing is unavailable at all).

**`governance/evidence-architecture.md`**

- **§5** — the four states; the pure-function requirement; *"no `stated` or `provisional`
  determination can exist without non-empty `governing_refs`"* (anti-hallucination, DR-2026-07-12
  item 10); scale-tagging G1b; direction-aware most-accommodating floor selection with its
  `[ENGINE-LAG]` tag; and **Person Mode produces no stored determinations at all** — what is
  stored is the *handoff* (the functional parameter driving assessment, plus the population-range
  scaffold). **FORBIDS:** writing a Person-Mode determination row; letting a population value bound
  an individual.
- **§5 G7** — §2.2 must admit T2 anchors explicitly, both streams.
- **§5 G8** — a `pending_assessment` cell may render **only** with the value-level-convergence-
  pending disclosure, in every register.
- **§6 I1–I5** — the five integrity invariants, *"mechanically checked by
  `scripts/audit/register_integrity_check.py`, which must be demonstrated firing on injected
  violations before its passes count."* I3 as amended and I5 are quoted in (b). **I2** adds:
  *"On a `regulatory_stratum_only` cell no anchored value (hence no delta) exists: the policymaker
  register renders the weak-band value under amended I3's mandatory flag and caveat, with the
  jurisdiction spread visible."*
- **§10** — the four mechanical checks and the doctrinal falsification conditions.

**`governance/evidence-methodology.md`** §2.2 (the four `stated` conditions and the *"Tier 3 alone
is not"* clause) · §2.3 (the `provisional` threshold, the richness clauses, the confidence flag) ·
§2.4 (`pending`) · §2.5 (`not_applicable` and its rationale requirement) · §2.7 (transitions,
including the two that must not occur) · §2.8 (the verification-status interaction table).

**Research contract R4** (while-searching): *"Cross slug x population / access-need / ICF / axis.
**Cells are (item x population).**"* The only contract rule that names the cell grain.

**Decision Records.** `DR-2026-07-12-evidence-architecture-unification.md` (G1b, item 10) ·
`DR-2026-07-12-evidence-cell-state-schema-reconciliation.md` (cell identity/storage) ·
`DR-2026-07-12-tier3-stated-threshold.md` · `DR-2026-07-20-weighted-strength-anchor-model.md` ·
`DR-2026-07-21-evidence-architecture-option-a-execution.md` (Option A; §5 lists the engine-lag
items) · `DR-2026-07-21-product-posture-thinking-tool-not-authority.md` (cited by migration 029:
*"a weak-band figure is a figure for thought, flagged, never suppressed and never promoted"*) ·
`RATIFICATION-RECORD-2026-07-13.md`.

##### Where documents disagree

| Question | Document A | Document B | Operative, and why |
|---|---|---|---|
| Does T3 alone reach `stated`? | `mission-and-epistemics.md` line 115: *"derived from ≥Tier 3 OR Co-1 OR Co-2"* | `evidence-methodology.md` §2.2: *"**Tier 3 alone is not**"*; `DR-2026-07-12-tier3-stated-threshold` | **B.** The DR is later and specific; `evidence-architecture.md` §5 and `pipeline-contract.yaml judgment/tier3-alone-threshold` both encode B; `validate_evidence_state` enforces B at **blocking** level. Mission's row is unamended drift. |
| How many evidence markers? | `mission-and-epistemics.md` **line 136**: two, ● / ○ | `tier-system.md` §5 lines 69–71: three, ● / ◐ / ○ | **B.** `tier-system.md` is `**Status:** OPERATIVE`. **The drift is internal to `mission-and-epistemics.md`, and it is one line.** `grep -n "●\|◐\|○"` returns lines 46, 136, 177; lines **46** (commitment 2) and **177** (the doctrinal test) were swept to Option A's three-band vocabulary on 2026-07-21, and line 136 was not. **`◐` appears nowhere in the doctrine file** (`grep -n "◐" governance/mission-and-epistemics.md` → no hits). CLAUDE.md §6's summary calls this a drift between two files; the truth is narrower and more fixable — a single unamended bullet at line 136. |
| Does `v_best_practice` include T6-only cells? | `evidence-architecture.md` §5 / `tier-system.md` §8: a T4–**T6**-only basis anchors at the weak band as *"a queryably distinct weak-band row"* | Migration 029's live view: `WHERE … code_floor_only = 0` | **The doctrine.** The view is a knowingly-narrower execution, flagged in 029's own header as an owner follow-up: *"Extending to `code_floor_only` is a one-line follow-up once the owner confirms intent."* |
| Is a `pending_assessment` cell rendered? | `evidence-methodology.md` §3.4: *"not rendered"* | `evidence-architecture.md` §5 **G8**: renders with mandatory disclosure | **G8**, ratified 2026-07-13; §3.4 *"is amended accordingly"* by G8's own text. |

#### (h) ACCEPTANCE CONDITIONS — stage 9

##### 9-A · An `evidence_cell_state` row (any state)

| # | Condition | Column / field | Level | Named enforcer |
|---:|---|---|---|---|
| 1 | `item_code` and `population_code` resolve | both | **D(fk)** | Declared FKs to `items` / `populations`, both NOT NULL; `migrate_db.py` differential check; CI via `migration_reproducibility` (**blocking**). `test_evidence_cell_state_2_3` mutation-tests the constraint text but is registered **advisory** and connects to `":memory:"` (line 68) — it asserts nothing about rows in `data/guidebook.db` |
| 2 | One row per (item, population) | — | **D** | SQLite `UNIQUE (item_code, population_code)` |
| 3 | `state ∈ {stated, provisional, pending, not_applicable}` | `state` | **D** | SQLite CHECK, NOT NULL |
| 4 | `design_scale ∈ {universal, population, person}` or NULL | `design_scale` | **D** + **4 blocking** | SQLite CHECK **and** `validate_evidence_state` (checks against `schemas.directness.ALL_SCALES`) |
| 5 | `governing_refs` is valid JSON | `governing_refs` | **D** | Table-level `CHECK (governing_refs IS NULL OR json_valid(governing_refs))` |
| 6 | `code_floor_only`, `regulatory_stratum_only`, `has_unverified_sources`, `all_sources_disqualified` ∈ {0,1} | each | **D** | Four SQLite CHECKs, all `NOT NULL DEFAULT 0` |
| 7 | `convergence_id`, `gap_register_id` resolve | both | **D(fk)** | Declared FKs to `convergence_assessment` / `gaps`; `migrate_db.py` differential check; CI via `migration_reproducibility` (blocking) |
| 8 | No stored Person-Mode determination | `design_scale` | **UNENFORCED** | `design_scale='person'` is accepted by the CHECK and by `validate_evidence_state`; `evidence-architecture.md` §5 forbids it outright (*"Person Mode produces no stored determinations at all"*) |
| 9 | Conditioning grades stored | — | **DESIGNED-ONLY** | No `scale_directness` / `population_directness` / `conditioning` column among the 27 |

##### 9-B · A `stated` cell

| # | Condition | Column / field | Level | Named enforcer |
|---:|---|---|---|---|
| 1 | Non-empty, well-formed `governing_refs` (anti-hallucination) | `governing_refs` | **4 blocking** | `validate_evidence_state` — the check `pipeline-contract.yaml judgment/governing-refs-nonempty` names |
| 2 | Every `governing_refs` entry **resolves to a real source** | — | **UNENFORCED by the named check; 4 blocking via a different one** | `validate_evidence_state` passes `["REF-99999"]` clean (reproduced above, exit 0, `v_best_practice` shows it `anchored`). `test_db_integrity` **H02** + **A11** catch it via the junction — different check, different battery, different store |
| 3 | Every governing source is `VERIFIED` | joined | **4 blocking** | `test_db_integrity` **C10** — `JOIN evidence_sources e ON e.ref_id = j.value`, an **inner** join, so phantom refs are silently dropped rather than flagged |
| 4 | A convergence assessment exists | `convergence_id` | **4 blocking** | `validate_evidence_state` (*"state 'stated' requires a convergence assessment (≥1 source axis, §2.2)"*) |
| 5 | `code_floor_only = 0` | `code_floor_only` | **4 blocking** | `validate_evidence_state` (*"a Tier-6-only cell can never be 'stated'"*) |
| 6 | `regulatory_stratum_only = 0` **and** `tier_basis` does not end `(regulatory_stratum_only)` | both | **4 blocking** | `validate_evidence_state:262–270` — checks the **column and the marker string**, so a pre-027 row is still caught |
| 7 | Not Tier-3-alone (single_axis convergence, all clinical refs tier = 3) | via `convergence_assessment` | **4 blocking, with a hole** | `validate_evidence_state`; the rule is **skipped when `_ref_tiers()` returns `{}`** — i.e. when the refs do not resolve. A phantom-ref Tier-3-alone cell escapes both #2 and #7 in the same check |
| 8 | Anchoring basis is T1 / T2 (either stream) / Co-1 (VERIFIED) / Co-2 | `tier_basis` | **UNENFORCED** | `tier_basis` is free TEXT with an illustrative comment and **no CHECK**; nothing validates it against the governing set. It is also in the `EvidenceStateRecord` DB-only drift list, so the Pydantic gate does not see it either |
| 9 | `falsification_condition` recorded | `falsification_condition` | **UNENFORCED** | Nullable; no check, despite `evidence-architecture.md` §9 |
| 10 | `rule_version` + `derivation_sha` recorded and correct | both | **4 blocking when present; NULL is reported, not failed** | `test_db_integrity` **K01** recomputes the sha; a NULL sha counts as `unattested` — observed verbatim: *"1 determination(s) carry no sha or no rule_version and are unattested — reported, not failed (owner question)"* |
| 11 | A `cell_source_links` row per governing ref, and no orphan junction rows | junction | **4 blocking** | `test_db_integrity` **H01** (junction ⊆ JSON) / **H02** (JSON ⊆ junction), plus **H06** (edge JSON columns hold arrays) and **H07** (no id repeats). **The pilot engine writes neither direction** — `grep -c cell_source_links scripts/assess/assess_cell.py` → 0 — so every engine-produced cell fails H02 on arrival |

##### 9-C · A `provisional` cell

| # | Condition | Column / field | Level | Named enforcer |
|---:|---|---|---|---|
| 1 | Non-empty, well-formed `governing_refs` | `governing_refs` | **4 blocking** | `validate_evidence_state` (same anti-hallucination gate; same phantom-ref hole as 9-B#2) |
| 2 | Confidence flag complete: `dimensions_present`, `dimensions_absent`, `synthesis_basis` all non-empty | 3 columns | **4 blocking** | `validate_evidence_state` (§2.3) |
| 3 | A convergence assessment exists | `convergence_id` | **4 blocking** | `validate_evidence_state` |
| 4 | If T4–6-only: `regulatory_stratum_only = 1` **and** `design_scale = 'universal'` | both | **UNENFORCED** | Nothing infers either from the basis. The engine computes `regulatory_stratum_only` and then **omits it from its 26-column INSERT**; the pilot backfill compensated with `UPDATE … WHERE tier_basis LIKE '%(regulatory_stratum_only)'`. The hand-authored `batch1-2026-07-19` migrations set it in the INSERT properly |
| 5 | If T6-only: `code_floor_only = 1` | `code_floor_only` | **UNENFORCED** | Same — nothing infers it from the basis; it is merely `NOT NULL DEFAULT 0` with a `D`-level CHECK on its domain |
| 6 | §2.3 richness met (≥1 T4, or ≥2 T4–5 across ≥2 jurisdictions, or ≥3 T6 across ≥3 jurisdictions) | — | **2 audit, engine-side only** | `assess_cell.regulatory_richness()`; **no validator re-checks it**, and the engine verifies only presence/jurisdiction-distinctness — never the "convergent findings" or "evidence-based value directly addressing the parameter" halves, by its own emitted rationale |
| 7 | Direction-aware most-accommodating value selected | `value_min` / `value_max` | **DESIGNED-ONLY** | `evidence-architecture.md` §5's own `[ENGINE-LAG]` tag; no column, no code |
| 8 | Population-contested direction routes to `conflicts` | `conflicts` | **DESIGNED-ONLY** | `conflicts` = 0 rows; no code path. Doctrine §5 is explicit that in this case *no single value is anchored* |
| 9 | Renders only at the ○ weak band, flagged **and** caveated, in every register, best-practice phrasing or not | render | **3 CI non-blocking, selftest failing** | `register_integrity_check` (**advisory**; `--selftest` exit **1**, one mutation missed because the DB subject is empty). I3 + I5 are the doctrine; the check is the only mechanism |

##### 9-D · A `pending` cell

| # | Condition | Column / field | Level | Named enforcer |
|---:|---|---|---|---|
| 1 | `gap_register_id` is present | `gap_register_id` | **4 blocking** | `validate_evidence_state` (§2.4) |
| 2 | It resolves in the `gaps` table | `gap_register_id` | **D(fk)** + **4 blocking** | Declared FK to `gaps(gap_id)`, plus `validate_evidence_state` against `load_gap_ids_db()` — *"gap_register_id {id!r} not in gaps table"* |
| 3 | The gap id matches `GAP-\d{3,4}` | `gap_register_id` | **UNENFORCED** | The regex lives in `schemas/evidence_state.py:167`, and **no registered check applies the model to DB rows**: `validate_evidence_state.validate_db()` reads raw SQL and never instantiates `EvidenceStateRecord` (which is used only by `validate_file()` over YAML paths). A DB row with `gap_register_id = 'GAP-1'` passes every registered check. The regex binds only inside `assess_cell.validate_with_models()` — and `assess_cell` is not a registered check. **This is also the failure that makes the engine crash post-reset**, because `next_gap_id()` on an empty `gaps` table returns `GAP-1` |
| 4 | The gap description does not claim corpus-level absence | `gaps.description` | **1 text rule** | Engine convention only (*"This records absence of a slug-link, NOT corpus-level absence"*) |
| 5 | The gap carries the adversarial fields (`falsification_condition`, `confidence_interval`, `shift_conditions`, `named_dissenter`) before `CLOSED` | `gaps` | **3 CI non-blocking** | `research_protocol_audit` (**advisory**, basis `research/adversarial-fields-complete`) |

##### 9-E · A `not_applicable` cell

| # | Condition | Column / field | Level | Named enforcer |
|---:|---|---|---|---|
| 1 | `not_applicable_rationale` present | `not_applicable_rationale` | **4 blocking** | `validate_evidence_state` (§2.5); model-tested by `test_assess_cell_pilot` |
| 2 | Rationale is population-specific, not "not relevant" | same | **1 text rule** | `evidence-methodology.md` §2.5 sets the standard verbatim (*"'not relevant' is insufficient; 'this parameter addresses [function X] which is not impacted by [population]'s functional profile' is the minimum"*); no mechanical check |
| 3 | Not reached directly from `stated`, and `not_applicable → stated` passes through `pending` | — | **UNENFORCED** | No transition validator exists anywhere; §2.7's two forbidden transitions are text only, and nothing stores a prior state to compare against |

##### 9-F · A `convergence_assessment` row

| # | Condition | Column / field | Level | Named enforcer |
|---:|---|---|---|---|
| 1 | `status ∈ {convergent, divergent, single_axis, pending_assessment}` | `status` | **D** | SQLite CHECK, NOT NULL |
| 2 | `divergent` ⇒ `rationale` **and** `synthesis_approach` | both | **4 blocking** | `validate_evidence_state` (§3.2) — but unreachable from the engine path, which can only emit `single_axis` / `pending_assessment` |
| 3 | `single_axis` ⇒ `rationale`, and ≤ 1 axis populated | — | **4 blocking** | `validate_evidence_state` |
| 4 | `convergent` ⇒ ≥ 2 axes | — | **4 blocking** | `validate_evidence_state` |
| 5 | All five ref-list columns are JSON arrays | `clinical_sources`, `co1_sources`, `co2_sources`, `down_weighted_sources`, `discounted_sources` | **4 blocking** | `validate_evidence_state._bad_json()` |
| 6 | A `discounted_sources` entry is not also anchoring | — | **4 blocking** | `validate_evidence_state` (§1.7) — the one directness rule at blocking level |
| 7 | Convergence counts **independent** axes, not documents | — | **DECLARED-BUT-UNENFORCED** | `pipeline-contract.yaml judgment/convergence-independence` → `check: null`. The root-count layer is `v_value_independence`, over an empty table |
| 8 | `pending_assessment` renders only with the G8 disclosure | render | **3 CI non-blocking** | `register_integrity_check` (**advisory**); the disclosure lives in the claim-strength row, so I4/I5 equality enforces it — when the check has a subject, which today it does not |

---

##### One remedy note, in the shape the repo has already ratified

Three blocking checks in this segment pass over an empty subject:
`validate_evidence_state` (`PASS: 0 records checked`), `check_rendered_docs`, and roughly 30 of
`test_db_integrity`'s 70 checks. The reflex remedy — *declare `min_items`* — is **wrong here**,
and the repo has already adjudicated why. The registry's own note on `source_slug_links_duplicates`
records it:

> `min_items: 1` was declared alongside it and RETIRED the same day by the clean-room reset,
> which emptied `source_slug_links` **by decision**. The guard exists to catch a check passing on
> an *accidentally* empty subject; an empty subject that is the declared state of the project is
> not that, and leaving the guard would have made a blocking gate red for telling the truth.

And on `check_rendered_docs`: *"Re-declare `min_items` the day `specs/` is regenerated against the
live DB"* — a prose sentence that nothing evaluates.

The correct shape is a **warranted, self-lifting suppression**, and it already exists and works in
this repo: `scripts/audit/graph/known_debt.yaml`, whose entries carry `warrant` +
`lift_when_sql` + `lift_when_ge`, and which `graph_audit.py` re-evaluates every run — reporting
the *suppression* as STALE once the debt clears, rather than silently hiding a real regression.
Two of its live entries are stage-7/9 subjects already:

```yaml
  - id: c1-source-value-extractions-empty
    check_id: table.empty_mission_critical
    table: source_value_extractions
    warrant: "DR-2026-05-28-b (B6) + C1 value backfill pending (ratification-execution-register-2026-07-13)"
    lift_when_sql: "SELECT COUNT(*) FROM source_value_extractions"
    lift_when_ge: 1

  - id: c1-evidence-cell-state-pilot-only
    check_id: table.empty_mission_critical
    table: evidence_cell_state
    warrant: "DR-2026-07-12 A2 + C1 determination backfill pending (7 pilot rows today)"
    lift_when_sql: "SELECT COUNT(*) FROM evidence_cell_state"
    lift_when_ge: 20
```

The stage-7/8/9 rows that warrant the same treatment, with their warrants already ratified:
`validate_evidence_state` (`warrant: DR-2026-08-06-clean-room-evidence-reset`;
`lift_when_sql: SELECT COUNT(*) FROM evidence_cell_state`; `lift_when_ge: 1`),
`research_dod` R13 and R3 (same warrant; `lift_when_sql: SELECT COUNT(*) FROM evidence_sources`),
and `register_integrity_check`'s completeness leg (same warrant, same lift as
`validate_evidence_state`). Note the second `known_debt` entry's `lift_when_ge: 20` is itself now
stale — it was written when `evidence_cell_state` held 7 pilot rows; it holds 0. That is the
mechanism working as designed: the warrant is re-evaluated, not remembered.

---

### 2.10 Stage 10 — Synthesis

## (a) Tools, tables, methodology

| Artefact | Path | State | Evidence |
|---|---|---|---|
| BPC corpus | `references/bpc/**.md` | **BUILT+EXERCISED** (as *pre-reset legacy text*) | `find references/bpc -name '*.md' ! -name '_template.md' ! -name 'index.md' \| wc -l` → **100**; the validator counts 102 including template + index |
| BPC template | `references/bpc/_template.md` | BUILT+EXERCISED | CO-0006 canonical template |
| BPC structural validator | `scripts/validate_bpc.py` | **BUILT+EXERCISED** | `python3 scripts/validate_bpc.py --all` → `validate_bpc.py: 102/102 files passed`, exit 0 |
| Reasoning-doc corpus | `references/bpc-reasoning/` | **BUILT+UNEXERCISED (1 non-conforming artefact)** | `ls` → exactly **2 files**: `_template.md`, `room-acoustic-performance.md`. One real doc, and it fails validation |
| Connection-reasoning corpus | `references/connection-reasoning/` | **DESIGNED-ONLY** | `ls` → **1 file, `_template.md`**. Zero real docs. Workplan target is 245 CON docs |
| Reasoning validator | `scripts/validate_reasoning.py` | **BUILT+EXERCISED, RED** | `--strict` → exit 1; without `--strict` → exit 0 |
| 9-step rule (PI rule #9) | `workplan/bpc-rewrite-workplan-2026-05-11.md` §2 + `validate_reasoning.py:54-64` `NINE_STEPS` | **BUILT+UNEXERCISED** | the nine labels are encoded in code but reachable only inside a `^## B\.` section; the one real doc has none |
| `bpc_metadata` closure flags | DB; `pico_complete`, `search_complete`, `bpc_complete`, `citation_mining_complete`, `supersession_check_complete`, `closure_definition_version` | **BUILT+UNEXERCISED** | 0 rows. Only writer in the tree is the legacy one-shot `scripts/migrate/migrate_bpc_metadata.py` |
| `item_bpc_links` | DB; PK `(item_code, slug)`, `link_type` CHECK | **BUILT+UNEXERCISED** | 0 rows (reset deleted 3) |
| Opus-class floor | PI rule #2 · `decisions/DR-2026-06-10-synthesis-model-floor.md` · `governance/pipeline-contract.yaml` `synthesis/opus-routing` | **DESIGNED-ONLY** | `governance/pipeline-contract.yaml:117` → `check: null`; `pipeline_contract_audit.py` lists `stage:synthesis/opus-routing` as INCOMPLETE |
| Phase-E execution plan | `workplan/phase-e-execution-plan-v1.md` | **DESIGNED-ONLY (ratified, unexecuted)** | v1.1 ratified 2026-06-10; its preflight ground truth (DB v24, 640 sources, 82 slugs) is falsified by the reset |
| BPC-rewrite workplan | `workplan/bpc-rewrite-workplan-2026-05-11.md` | DESIGNED-ONLY | phases A–G, "B before E" gate |
| Registered check | `validate_bpc` — `battery: structure`, `kinds: [always]`, **level: blocking** | wired, green | `governance/check-registry.yaml` |
| Registered check | `validate_reasoning` — `cmd: […, --strict]`, `battery: research`, `kinds: [synthesis]`, **level: advisory** | wired, red | registry note understates the failure — see (f) |
| Registered check | `reasoning_doc_citations_audit` — advisory, `kinds: [data, synthesis]` | **BUILT+UNEXERCISED** | `reasoning_doc_citations` = 0 rows |
| Skills | `skills/reasoning-doc-citations_SKILL.md`, `adversarial-research_SKILL.md`, `progressive-measurement_SKILL.md`, `multilingual-research_SKILL.md`, `cell-curator_SKILL.md`, `item-specification-writer_SKILL.md` | text protocols | `ls skills/` |

### The BPC corpus, honestly counted

```
grep -rl '### Best-practice synthesis' references/bpc --include=*.md | wc -l   → 75
grep -rli 'RETRACTED'                  references/bpc --include=*.md | wc -l   → 70
grep -rl '●' references/bpc --include=*.md | wc -l → 7
grep -rl '◐' references/bpc --include=*.md | wc -l → 3
grep -rl '○' references/bpc --include=*.md | wc -l → 7
```

**70 of 100 BPC files carry a retraction banner, and only 7 carry the `●` marker** that
`governance/tier-system.md` §5 requires on every spec sentence (CLAUDE.md §6: "unmarked = error").
Nothing checks markers in BPC files: `grep -rln '●\|◐' --include=*.py scripts/ tools/` returns only
renderers plus `check_rendered_docs.py` and `register_integrity_check.py`, which check *rendered
HTML* and never `references/bpc/**`.

## (b) How they relate to each other

The stage has **two parallel artefact chains that are not joined by any key.**

**1 · File chain.** `references/bpc/<topic>/<slug>.md` (the product) ↔
`references/bpc-reasoning/<slug>.md` (the audit trail). The join is **by filename stem only** —
`validate_reasoning.py:254` globs `BPC_REASONING_DIR.glob("*.md")` and never opens the BPC file it
names. The template's `**BPC file:**` header is a *string*; nothing resolves it. So a reasoning doc
can name a BPC that does not exist, and a BPC can have no reasoning doc, with no error from either
validator. Confirmed structurally: neither validator opens the database at all —
`grep -c sqlite3 scripts/validate_reasoning.py scripts/validate_bpc.py` → `0` and `0`.

**2 · DB chain.** `slugs` (106) → `bpc_metadata` (0 rows; PK `slug` FK→`slugs.slug`) →
`item_bpc_links` (0 rows; PK `(item_code, slug)`, FKs to `items` and `slugs`, `link_type` CHECK ∈
`primary`/`parameter`/`context`/`secondary`) → `items` (93). `items.bpc_source_slug` is a *second*,
denormalised text pointer to the same slug; the pilot reasoning doc's own "Item 4" argues for
`item_bpc_links` precisely to end that duplication. The table now exists and is empty, so the
denormalised pointer is the only live one — visible directly in the rendered output, where
`site/specs/a-18.html`'s fresh render falls back to
`room-acoustic-performance | legacy bpc_source_slug | — | item_bpc_links (the intended many-to-many bridge)…`.

**Nothing writes the file chain into the DB chain.** No script parses `references/bpc-reasoning/*.md`
and emits `bpc_metadata` or `reasoning_doc_citations` rows; those rows were hand-authored by
migration (the reset deleted all 14). `scripts/audit/reasoning_doc_citations_audit.py` audits the
table, not the documents.

Within `validate_reasoning.py` the internal wiring is status-conditioned (lines 152-175):
`Status: COMPLETE` → every missing 9-step is an **error**; `OPUS-PENDING` → steps 1–4 error, steps
5–9 warn (the facts/judgment split standing in for the Opus floor); `DRAFT` → all warn;
unknown/absent status → treated as COMPLETE (strict). That last branch is the right default, and
the OPUS-PENDING branch is the only place in the repo where the Opus floor has any mechanical
shadow at all.

## (c) Relation to the previous stage (9 — cell determination)

**Entry contract as designed.** `governance/pipeline-contract.yaml` stage `synthesis` declares its
input as *"a determination with a resolved value, ready for cross-jurisdictional synthesis"* — an
`evidence_cell_state` row at `stated`/`provisional` with non-empty `governing_refs`, plus a
`convergence_assessment` row. The content workplan adds the **"B before E" gate**: no BPC is
rewritten until its linked sources pass Phase B verification.

**What actually enforces it: NOTHING ENFORCES THIS.**

- No registered check reads a cell-state row as a precondition for a reasoning-doc or BPC commit.
  `validate_reasoning` (advisory) and `validate_bpc` (blocking) are both pure text checks that
  never open the database.
- `scripts/check_phase_a_complete.py`, the only script that could gate phase order, is
  **quarantined** in the registry: *"RED, and correctly so — it reports Phase B cannot begin. A
  workplan status report, not a regression gate."*
- Post-reset the upstream is empty regardless: `evidence_cell_state` 0,
  `convergence_assessment` 0. `python3 scripts/validate_evidence_state.py` →
  `OK cell-state machine: 0 cells, 0 convergence rows validated` / `PASS: 0 records checked`. The
  stage-9 validator is blocking and vacuously green, so it certifies nothing about the handoff.

The one genuine entry-side enforcement is level D: `evidence_cell_state`'s
`CHECK (state IN ('stated','provisional','pending','not_applicable'))` and its
`UNIQUE (item_code, population_code)` make a malformed or duplicated determination unwritable by
any code path. That is a real floor — but it constrains the *shape* of an upstream row, not its
*existence*, and synthesis never reads it.

## (d) Relation to the next stage (11 — adversarial QA & audit)

**Exit contract as designed.** The reasoning doc's §E ("Adversarial protocol pass, per standing
rule #7") must carry `Confidence interval` / `Shift conditions` / `Named dissenter` /
`Falsification condition`; numeric parameters must have a PMP walk (rule #8); every citation must
have a `reasoning_doc_citations` row (rule #10 sub-rules 2/3); the commit must carry
`[DOCTRINE: <sha>]` and an attestation.

**What enforces it:**

- §E field presence → `validate_reasoning.py:177-185`, but these emit **warnings, never errors**,
  so they cannot fail even `--strict`. Level 1 in effect.
- Doctrine token → `scripts/ci_helpers/check_doctrine_token.py`, level 4 blocking but **push-only**
  (`.github/workflows/ci.yml:248 if: github.event_name == 'push'`).
- Attestation → `scripts/audit/adherence_log_audit.py --check presence|schema`, level 4 blocking —
  with the diff-scope limit from cross-cutting finding 3.
- **Critical gap.** Both the token gate and the attestation audit define synthesis paths as
  `^(references/bpc-reasoning|references/connection-reasoning|decisions|sessions)/`
  (`check_doctrine_token.py:46`, `adherence_log_audit.py:74`). **`references/bpc/` is in neither
  regex**, yet `governance/check-registry.yaml`'s `kinds.synthesis.paths` **does** include
  `references/bpc/**`. So a diff touching only the actual synthesis product is classified
  `synthesis`, routed to the attestation battery, and the battery then reports `synthesis: 0` and
  passes.

  Proved empirically on a real commit rather than by regex alone. `b35f3f9` touches
  `references/bpc/seating-and-rest/energy-conservation-rest-points-seating.md`:

  ```
  python3 scripts/audit/adherence_log_audit.py --check presence --base b35f3f9~1 --head b35f3f9
  → changed files: 8; attestations: 1; synthesis: 1   / No issues.
  ```

  Testing all eight changed paths against `SYNTHESIS_PATH_RE`, exactly one matches:
  `sessions/session_2026-07-26-…-adversarial.md`. **The BPC file was not counted.** The synthesis
  product is classified as synthesis by the work-kind router and gated as nothing by the gates that
  routing selects.
- PMP linkage → `scripts/audit/pmp_audit.py`, advisory, and structurally vacuous (see stage 11 (f)).

## (e) The goal of the stage

Stage 10 is where the project's actual deliverable is made: turning a set of per-cell
determinations into a **defensible, reader-facing best-practice statement plus the audit trail that
lets a stranger re-derive it**. The BPC file is the claim; the reasoning document is the warrant.
The 9-step rule exists so that the move from "these codes say X and these studies say Y" to "the
guidebook says Z for population P" is performed in public, step by step — with the worst-case user
named, the lowest-barrier code named, the tier evidence tabulated, the chosen value stated per
population, the trade-offs owned, and cross-population conflicts *flagged rather than reconciled
inline*. The Opus floor exists because that particular move — judgment under conflicting evidence —
is where a weaker model produces plausible text and the project's whole epistemic posture
("thinking tool, not authority") collapses into fabricated confidence.

## (f) How the tools support that goal — and where they do not

**Support.** `validate_reasoning.py` is the best-designed validator in the repo for its purpose: it
encodes the template as structure, it is status-aware in exactly the way the facts/judgment split
requires, and its `--strict`/default asymmetry is documented in the registry rather than hidden
(the registry entry states plainly that the unflagged invocation "is a green tick that means
nothing"). `validate_bpc.py` gives cheap, always-on structural hygiene, correctly ungated at
`kinds: [always]`.

**Where they do not.**

**1 · `validate_bpc.py` does not validate synthesis.** `MANDATORY_SECTIONS = ["## Key sources",
"## Metadata"]` (lines 32-36); `### Best-practice synthesis` sits in `OPTIONAL_SECTIONS`
(lines 38-45). The blocking gate over the entire BPC corpus checks for a REF-ID table and a
metadata block — nothing about markers, tiers, retraction state, or whether a synthesis exists at
all. 102/102 pass while 70 of 100 files are retracted and 93 of 100 carry no `●`.

**2 · The 9-step check is unreachable on the only real document.**
`validate_reasoning.py:126-128` locates the B section with
`re.search(r"^## B\..*?(?=^## C\.|^## [D-Z]\.|\Z)", …)` and everything about the nine steps
(lines 131-175) lives inside `if b_section_m:`. `grep -n '^## B\.' references/bpc-reasoning/room-acoustic-performance.md`
returns nothing, so `b_section_m` is `None` and the whole block is skipped — *including* its own
"Section B has no `### B.N Parameter:` blocks" warning, which would at least have said so.

The document *does* carry the nine steps, as `### Step 1 — Parameter declaration` …
`### Step 9 — Cross-population conflict flag`, under `## Pass 2 — Rule #9 steps 4 through 9` and
similar headings. But even placed under a `## B.` header, two of the nine labels would still miss:
`NINE_STEPS[0]` is `"Step 1 — Direction"` against the doc's `"Step 1 — Parameter declaration"`, and
`NINE_STEPS[4]` is `"Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence"` against the doc's
`"Step 5 — Tier evidence per population"`. The effect claim ("the steps are invisible to the
checker") is right; a rename alone would not fix it.

**Net effect: the corpus-wide 9-step gate is advisory, red for an unrelated reason, and has
evaluated zero parameter blocks in the project's history.** This is the project's primary
methodological invariant.

**3 · The one reasoning document fails every structural requirement — 15 errors, not 16.**
`python3 scripts/validate_reasoning.py --strict` → `Reasoning-doc validation — 3 docs checked` /
`Summary: 0 clean, 0 with warnings, 1 with errors, 2 skipped (templates)`, exit 1. The errors are
**4 header + 11 sections = 15**:

*Header (4):* `Missing required header field: **BPC file**` · `**BPC population**` · `**Generated**` ·
`Status 'PILOT' not in ['COMPLETE', 'DRAFT', 'OPUS-PENDING']`

*Sections (11):* `A. Evidence inventory` · `A.1 Sources formally linked` · `A.2 Sources cited in
this BPC but NOT formally linked` · `A.3 Practitioner / secondary sources` · `A.4 Primary
regulatory documents retrieved` · `A.5 Gaps in the evidence inventory` · `B. Per-parameter
reasoning` · `C. Synthesis claims that did NOT survive evidence review` · `D. Cross-references` ·
`E. Adversarial protocol pass` · `F. Provenance trail`

(A `grep -c` over the output returns 16 only because the `[ERROR] <filename>` banner line also
matches; the substantive count is 15.)

**Correction to the registry.** `governance/check-registry.yaml`'s `validate_reasoning` note says
*"RED today (1 doc missing 'F. Provenance trail'), hence advisory."* It is missing **all eleven**
sections and four header fields. Per the registry's own stated discipline elsewhere
(`schema_reference_drift_audit`: *"DO NOT WRITE A FIXED NUMBER HERE — re-run it"*), this note should
be corrected or replaced with a re-run instruction.

Two independent remedies exist and should not be conflated: (i) bring the pilot doc onto the
template (a synthesis-path edit → doctrine token + attestation required), or (ii) add `PILOT` to
`BPC_STATUS_ENUM` with `DRAFT`-equivalent severity, which is the smaller change and matches what
the document actually is. Both are owner calls.

**4 · The Opus floor: the enforceable part is the declaration, not the identity.**

Nothing in the schema records an authoring model.
`grep -rn "Opus-class\|model_floor\|authored_by_model" --include=*.py scripts/ tools/ schemas/` →
no matches. The only schema object matching `/model|authored_by|agent/i` is `decisions.model_routing`
— a routing-budget string on the *governance record*, not on any synthesis artefact
(`legacy/none/none` 105, `opus/150/synth` 19, `opus/100/route` 13, `opus/100/extract` 10,
`opus/125/extract` 5, `sonnet/100/route` 2, `opus/200/synth` 1, `opus/200/arbitrate` 1,
`human/none/none` 1). `schemas/attestation.schema.json`'s `properties` are exactly eleven —
`artifact`, `bias_direction`, `deviations`, `doctrine_sha`, `independent_reviewer_counterclaim`,
`per_rule_status`, `reattestation`, `rules_in_scope`, `schema_version`, `session`, `verdict` — with
no model field.

The three candidate enforcements, assessed correctly:

- ***Weak — self-reported declaration.*** Add `authored_by_model` to
  `schemas/attestation.schema.json`, required when any `rules_in_scope` entry is
  `best-practice-synthesis-routing`, resolved against an allowlist
  (`governance/model-floor.yaml`) that the DR's "Opus-class or above" phrase can be evaluated
  against. This does **not** verify capability — a sub-floor model writes the string itself — so it
  detects honesty lapses, not capability lapses.
- ***Medium — the queue boundary.*** The status machine already exists and already encodes the
  facts/judgment split (`validate_reasoning.py:152-175`: `OPUS-PENDING` ⇒ steps 1–4 error, 5–9
  warn). Promoting "missing steps 5–9 at `Status: COMPLETE`" from warn to error costs one line, and
  needs no schema change, no DR and no model-identity claim. This is a real, cheap, mechanically
  checkable floor on the boundary the PI actually describes ("lower-tier models … queue the doc for
  an Opus session"). **On cost-effectiveness this ranks first.**
- ***"Strong" — a workflow.*** A GitHub Actions job that calls a pinned model and commits as the
  bot. **This is not the verification it looks like.** It proves what model *that run* used; it does
  not prove the committed synthesis text came from it, and it does not stop a human or a sub-floor
  agent from authoring `references/bpc-reasoning/foo.md` by hand and pushing it. Closing that
  requires additionally refusing non-bot authorship on synthesis paths — i.e. branch protection plus
  a required check. **`main` is not branch-protected**, so the workflow option is *inert* without an
  owner action the repo has not taken, and it inherits precisely the enforcement ceiling that makes
  level 4 weak here.

**The honest statement: model identity is not self-attestable, but the declaration is, and the
queue boundary is. The repo has taken neither cheap half.** `check: null` on
`pipeline-contract.yaml:117` is a choice, not a physical limit — and the repo's own
`pipeline_contract_audit.py` is designed to report exactly that choice as `INCOMPLETE` rather than
hide it (`VERDICT: PASS (broken=0, quarantined=0, unregistered=0, incomplete=5, verifiable=14)`,
`EXAMINED: 19 contract criteria`). The enforceable part is the **declaration**, and its home already
exists: the attestation schema, which already demands `bias_direction` and
`independent_reviewer_counterclaim` and already validates them.

**5 · `bpc_metadata` closure flags are write-once-by-migration and gate nothing.**
`grep -rn "bpc_complete" --include=*.py` finds only `scripts/migrate/migrate_bpc_metadata.py`.
Readers exist — `scripts/generate_parts.py`, `tools/evidentiary_audit.py`,
`tools/pipeline_completeness.py`, `scripts/assess/assess_cell.py`, `spec_page.py`,
`population_page.py`, `validate_population.py`, `test_db_integrity.py` — but every one of them
*reports* the flags; none gates on them. Their 0/1 domain is enforced at level D
(`CHECK(bpc_complete IN (0,1))` and siblings), which guarantees the flags are well-formed and
guarantees nothing about whether they are consulted.

## (g) How doctrine conditions the stage

- **`governance/mission-and-epistemics.md` §Doctrinal commitment 2** — best practice is graded by
  the evidence hierarchy; **code consensus anchors it only at the weak band**. This **FORBIDS** a
  BPC synthesis sentence that reads a T4–T6 convergence as a best-practice claim at `●` or `◐`. The
  pilot doc obeys explicitly: its "Item 2" ruling requires NDV/AUT RT60 ≤ 0.4 s to be rendered as
  *"conjecture rationally informed by literature"*, inline, not as an appended caveat.
- **§Commitment 3** — Co-1 is co-primary with T1 (CRPD Art. 4.3). **FORBIDS** treating a
  lived-experience source as "supporting" or down-weighting it beneath T2.
- **§Commitment 7 / §Purpose** — "teaches professional judgment, does not substitute for it."
  **FORBIDS** prescriptive imperative phrasing in a BPC; the synthesis must be a graded claim with
  its warrant attached.
- **Test 3 and Test 7** (`mission-and-epistemics.md` §"Test against which all downstream decisions
  are evaluated"): *"Does it grade best practice by the evidence hierarchy — treating code
  consensus as the weak (○) band, flagged…?"* and *"Is the underlying data verifiable (clean data)
  and the methodology declared?"* The reasoning document **is** the declared methodology, so a BPC
  without one fails Test 7 by construction. **99 of 100 BPC files currently fail it.**
- **`governance/tier-system.md` §5** — every spec sentence carries `●`/`◐`/`○`; unmarked = error.
  Level 1 only on `references/**` (see (h) C10).
- **`governance/evidence-architecture.md`** + `DR-2026-07-20` (weighted strength) +
  `DR-2026-07-21` ("Option A") — a regulatory-stratum-only claim may anchor best practice **only**
  at the flagged weak band. **FORBIDS** an unflagged rendering.
- **Research contract** (`governance/research-contract.yaml`, R1–R15, enforcer
  `scripts/audit/research_batch_dod.py`): **R3** — quantified values carry a locator or carry the
  flag; a numeric without DOI + page/table must read `[UNVERIFIED-QUANT]`. **R7** — failure, harm
  and inadequacy are first-class evidence, which **FORBIDS** a synthesis that cites only what
  works. **R15** — a resolved candidate is re-described from the source, which forbids carrying a
  staged hypothesis description into a synthesis claim.
- **`decisions/DR-2026-06-10-synthesis-model-floor.md`** — rule #2 is a *capability floor*, not a
  brand pin. **FORBIDS** a sub-Opus model authoring `best_practice_synthesis`; explicitly
  **permits** it doing inventories, per-population logging and Pass-1 facts.
- **`decisions/DR-2026-08-06-clean-room-evidence-reset.md`** — dominates everything above right
  now. With the corpus emptied, any synthesis authored today would be authored against zero
  evidence rows and would violate the state machine's `stated`/`provisional` ⇒ non-empty
  `governing_refs` requirement on arrival.

## (h) ACCEPTANCE CONDITIONS — stage 10

What one **BPC entry** and its **reasoning document** must satisfy to be admitted. Enforcement
levels per the preamble: 1–5 are the repo's spectrum; **D** is the schema-constraint rung the
spectrum omits.

**The reasoning document**

1. **Header carries `**BPC file:**`, `**BPC population:**`, `**Generated:**`, `**Status:**`** ·
   field: doc header, bold-colon form at line start · **level 2** (registered advisory ⇒ effectively
   an audit script) · enforcer `validate_reasoning.py:102-104` via registry `validate_reasoning`.
   *Currently failing on the only real doc — 3 of 4 fields absent.*
2. **`Status ∈ {DRAFT, OPUS-PENDING, COMPLETE}`** · field: `**Status:**` · **level 2** · enforcer
   `validate_reasoning.py:111-116`. *Currently failing: the doc reads `PILOT`.*
3. **All 11 required sections present (A, A.1–A.5, B, C, D, E, F)** · field: `##`–`####` headers ·
   **level 2** · enforcer `validate_reasoning.py:119-123`. *Currently failing on all 11.*
4. **Every `### B.N Parameter:` block contains all 9 steps** (severity by status: COMPLETE → error;
   OPUS-PENDING → 1–4 error, 5–9 warn; DRAFT → warn) · field: `## B.` body · **level 2, and
   currently unreachable** · enforcer `validate_reasoning.py:126-175`. The block is guarded by
   `if b_section_m:` and the only real doc has no `## B.` header, so **zero parameter blocks have
   ever been evaluated.**
5. **§E names Confidence interval, Shift conditions, Named dissenter, Falsification condition** ·
   field: `## E.` body · **level 1 in practice** · `validate_reasoning.py:177-185` emits
   **warnings only** and cannot fail `--strict`.
6. **Every cited REF has a `reasoning_doc_citations` row confirming the source contains what the
   doc says** · field: `reasoning_doc_citations` · **level 2** · enforcer
   `scripts/audit/reasoning_doc_citations_audit.py` (advisory). **UNEXERCISED** — table 0 rows.
7. **Every numeric parameter cites an active PMP walk** · field: `spec_value_probes` ·
   **level 2, and structurally vacuous** · enforcer `scripts/audit/pmp_audit.py` (advisory) — its
   CHECK 1 can only flag items that already have a walk (stage 11 (f)).
8. **Reasoning doc and BPC file resolve to each other** · field: `**BPC file:**` string ·
   **UNENFORCED** · the join is filename-stem-only and `validate_reasoning.py:254` never opens the
   named BPC.

**The BPC entry**

9. **`## Key sources` present with REF-ID / Authors / Year / Title columns, and `## Metadata`
   present with slug / population / last_updated** · field: BPC markdown · **level 4 blocking** ·
   enforcer `scripts/validate_bpc.py --all`, registry `validate_bpc`, `kinds: [always]`. Live:
   `102/102 files passed`.
10. **A `### Best-practice synthesis` section exists** · field: BPC markdown · **UNENFORCED** —
    explicitly listed in `OPTIONAL_SECTIONS` (`validate_bpc.py:38-45`). 75 of 100 files have one;
    nothing requires it.
11. **Every spec sentence carries `●` / `◐` / `○`** · field: BPC + reasoning prose · **UNENFORCED**
    on `references/**`. Enforced only on *rendered HTML* by `register_integrity_check.py`, which is
    advisory and — per cross-cutting finding 1 — currently evaluates no document.
12. **A regulatory-stratum-only claim is flagged weak-band, never `●`/`◐`** · field: BPC prose ·
    **UNENFORCED** on markdown. Same rendered-HTML-only coverage as C11.
13. **Retraction state is declared and consistent** · field: BPC banner text · **UNENFORCED** —
    `validate_bpc.py` does not read retraction banners; 70 of 100 files carry one and pass.

**The DB row behind the entry**

14. **`bpc_metadata.slug` resolves to a real `slugs` row** · field: `bpc_metadata.slug` (PK, FK) ·
    **D(fk)** — deferred differential check in `migrate_db.py`; new violations fail, pre-existing
    baseline grandfathered, bootstrap exempt; reaches CI via `migration_reproducibility` (blocking).
15. **Closure flags are 0/1 and `closure_definition_version ∈ {v1, v2}` or NULL** · field:
    `bpc_metadata.pico_complete`, `.search_complete`, `.bpc_complete`, `.citation_mining_complete`,
    `.supersession_check_complete`, `.closure_definition_version` · **D — enforced at write time by
    SQLite** (`CHECK(… IN (0,1))`, `CHECK(closure_definition_version IS NULL OR … IN ('v1','v2'))`).
    Well-formedness is guaranteed; **consultation is not** — no gate reads them.
16. **`item_bpc_links.link_type ∈ {primary, parameter, context, secondary}`** · field:
    `item_bpc_links.link_type` · **D — enforced at write time by SQLite** (`CHECK`).
17. **At most one `item_bpc_links` row per (item, slug)** · field: `PRIMARY KEY (item_code, slug)` ·
    **D — enforced at write time by SQLite** (UNIQUE via PK).
18. **`item_bpc_links` item and slug resolve** · field: FKs to `items(item_code)`, `slugs(slug)` ·
    **D(fk)** — as row 14.
19. **A `stated`/`provisional` cell has non-empty `governing_refs`** · field:
    `evidence_cell_state.governing_refs` · **level 4 blocking, and vacuous** · enforcer
    `scripts/validate_evidence_state.py` → `PASS: 0 records checked`. Note the DDL only enforces
    `CHECK (governing_refs IS NULL OR json_valid(governing_refs))` — **level D covers well-formed
    JSON, not non-emptiness**; the state↔refs pairing is the validator's job alone.
20. **The cell's `state` is one of the four legal values, and (item, population) is unique** ·
    field: `evidence_cell_state.state`, `UNIQUE (item_code, population_code)` · **D — enforced at
    write time by SQLite**.

**The commit that carries them**

21. **Commit subject carries `[DOCTRINE: 0f2f525]` before the timestamp** · field: commit subject ·
    **level 4 blocking, push-only** · enforcer `scripts/ci_helpers/check_doctrine_token.py`
    (`ci.yml:244-271`, `if: github.event_name == 'push'` at :248). **Does not cover
    `references/bpc/`** — `SYNTHESIS_RE` at line 46 omits it.
22. **`attestations/<slug>.json` present for every synthesis-path file in the changeset** · field:
    `attestations/*.json` · **level 4 blocking, diff-scoped** · enforcer
    `adherence_log_audit.py --check presence`. **Does not cover `references/bpc/`** — proven on
    `b35f3f9`, where the BPC file was not counted.
23. **That attestation is schema-valid: each `FIRED` has `evidence_path`, each `SKIPPED` has
    `reason`, `bias_direction` ≥ 30 chars, `independent_reviewer_counterclaim` ≥ 30 chars,
    `verdict` in enum** · field: `per_rule_status`, `bias_direction`,
    `independent_reviewer_counterclaim`, `verdict` · **level 4 blocking for files in the diff;
    UNENFORCED for the committed corpus** · enforcer `adherence_log_audit.py --check schema` +
    `schemas/attestation.schema.json`. The schema constraints are real
    (`minLength: 30` on both prose fields; `allOf` conditionals on `per_rule_status`), but the check
    is diff-scoped — see cross-cutting finding 3.
24. **The author is Opus-class or above** · field: **nowhere — no column, no schema property** ·
    **level 1 text rule only** · PI rule #2 + `DR-2026-06-10`; `pipeline-contract.yaml:117` is
    `check: null` and `pipeline_contract_audit.py` reports `stage:synthesis/opus-routing` as
    INCOMPLETE.
25. **Linked sources passed Phase B verification before rewrite ("B before E")** · field:
    `evidence_sources.verification_status` · **UNENFORCED** — the only candidate gate,
    `check_phase_a_complete.py`, is quarantined as a workplan status report.

**Remedies, in the shape the repo already ratifies.** Rows 6, 7, 19 and 25 all currently pass or
abstain because their subject is empty — and the emptiness is **ratified**
(`DR-2026-08-06-clean-room-evidence-reset`), not accidental. Declaring `min_items` on these would
turn a correct abstention into a permanently red gate and teach the next session to ignore it. The
correct instrument is a warranted self-lifting suppression in the
`scripts/audit/graph/known_debt.yaml` shape — e.g. for row 6:

```yaml
- id: reasoning-doc-citations-empty-post-reset
  check_id: reasoning_doc_citations_audit.empty_subject
  table: reasoning_doc_citations
  warrant: "DR-2026-08-06-clean-room-evidence-reset — research corpus deliberately emptied"
  lift_when_sql: "SELECT COUNT(*) FROM reasoning_doc_citations"
  lift_when_ge: 1
```

which suppresses the finding while the warrant holds and reports **the suppression itself** as
STALE the moment the first row lands. Rows 2, 3, 4, 10, 11, 12 are *not* in this class — their
subject exists (one document, 100 BPC files) and they fail or abstain on their own merits.

---

# STAGE 11 — ADVERSARIAL QA & AUDIT

### 2.11 Stage 11 — Adversarial QA & audit

## (a) Tools, tables, methodology

| Artefact | Path / table | State | Evidence |
|---|---|---|---|
| Item audit orchestrator | `scripts/item_audit_pipeline.py` | **BUILT+UNEXERCISED, and a manual harness** | 8 `PIPELINE_STEPS`; lines 400-407 print `"→ Invoke {step} skill protocol now (manual — see SKILL.md)"`. Only step 8 (`audit_consolidator.py`) actually executes |
| `item_audit_runs` | DB | **BUILT+UNEXERCISED** | 0 rows (reset deleted 87) |
| `supersession_check` | DB | **BUILT+UNEXERCISED** | 0 rows (reset deleted 134); FK `ref_id → evidence_sources(ref_id)` now unsatisfiable, `evidence_sources` being empty |
| `spec_value_probes` (PMP) | DB | **BUILT+UNEXERCISED** | 0 rows (reset deleted 31) |
| PMP audit | `scripts/audit/pmp_audit.py` | **BUILT+EXERCISED, now vacuously green** | `python3 scripts/audit/pmp_audit.py` → `ISSUES: 0`, exit 0 |
| Progressive Measurement Protocol | `skills/progressive-measurement_SKILL.md`, DR-2026-05-10 | DESIGNED-ONLY (protocol text) | — |
| Claims docket | `scripts/audit/claims_docket.py` + `working/claims-docket.md` | **BUILT+EXERCISED** | `claims_docket.py check` → `PASS: 68/68 docket claims carry warrant annotations`, exit 0 |
| Attestation audit | `scripts/audit/adherence_log_audit.py` | **BUILT+EXERCISED, diff-scoped** | 4 registered subchecks; clean tree → `changed files: 1; attestations: 0; synthesis: 0` / `No issues.` |
| Attestation corpus | `attestations/*.json` (74) + `schemas/attestation.schema.json` | **BUILT+EXERCISED** | `ls attestations/*.json \| wc -l` → 74; `ls decisions/*.md \| wc -l` → 57; 74/74 schema-valid by hand-run `jsonschema` |
| Adjudication integrity | `scripts/audit/adjudication_integrity.py` | **BUILT+EXERCISED, now vacuously green** | `VERDICT: PASS (tier inconsistencies=0)`, exit 0. Registry still quarantines it as *"RED — 274 tier inconsistencies"* — falsified by the reset |
| Integrity protocol | `skills/integrity-protocol_SKILL.md` (3 modes, DR-2026-07-13) | **BUILT+EXERCISED as practice, level 1–2** | Mode 2's docket is mechanised; Modes 1 and 3 are human/agent protocol |
| Doctrine recheck | `governance/doctrine-recheck.md` + `scripts/doctrine_recheck.py` | **BUILT+EXERCISED** | `--cross-ref` → `11 CANONICAL govs · 8 CANONICAL rules · 155 ACTIVE decisions · 102 BPC files`, 5 `[2.3]` warnings, exit 0 |
| Doctrine token gate | `scripts/ci_helpers/check_doctrine_token.py` (+ `commit_gate.py`) | **BUILT+EXERCISED**, level 4, push-only | `ci.yml:244-271`. **Not in `check-registry.yaml`** — so `run_checks.py`/`preflight.sh` never runs it |
| Conflict matrices | `references/conflict-matrices/*.md` (**13 files**) | **BUILT+EXERCISED (files) / UNEXERCISED (DB)** | `ls references/conflict-matrices/*.md \| wc -l` → **13**: ACOUSTIC-LVL, COLOUR-CONT, CORRIDOR-W, FRAGRANCE, LIGHT-INT, LIGHT-QUAL, MOVE-FREE, PREDICT, SPATIAL-OPEN, SURFACE-TEXT, SYNTHESIS, TEMP-RANGE, VIS-COMPLEX. `conflicts` table = 0 rows |
| Conflict validators | `scripts/validate_conflict.py` (file-side) / `validate_conflicts.py` (DB-side) | both **quarantined** | file-side *"RED — 11 errors, all unknown population codes ('IntD', 'VIS')"*; DB-side *"Green but vacuous"* |
| Matrix consistency | `scripts/audit/matrix_consistency.py` | **BUILT+EXERCISED, green** | `PASS: 10/10 outcomes match evidence-architecture.md §3` |
| Contract audit | `scripts/audit/pipeline_contract_audit.py` | **BUILT+EXERCISED** | `EXAMINED: 19 contract criteria`; `VERDICT: PASS (broken=0, quarantined=0, unregistered=0, incomplete=5, verifiable=14)` |
| Companion test | `scripts/tests/test_adjudication_integrity.py` | **UNREGISTERED** | per CLAUDE.md §7 and the registry quarantine entry |

## (b) How they relate to each other

Three loosely-coupled sub-systems, not one pipeline.

**1 · Per-item audit loop.** `item_audit_pipeline.py` → writes `item_audit_runs` (`run_id`,
`steps_complete` JSON, `status ∈ IN-PROGRESS/COMPLETE/HANDED-OFF`, `spec_hash`, `brief_path`) →
step 8 `scripts/audit_consolidator.py` → writes `references/audit-briefs/<item>_brief.md`.
`spec_hash` is an MD5 of item text pulled from
`versions/current/Guidebook_for_Accessible_Design_v9-0_2026-03-20.md` (line 30) — a file that still
exists but is a **v9-0 snapshot**, so the audit's staleness detector is anchored to a frozen
document rather than to `items`.

**2 · Evidence-integrity audits.** `pmp_audit` (`items` × `spec_value_probes` × `evidence_sources`),
`adjudication_integrity` (`evidence_sources.tier` vs `derive_tier(evidence_type, scope)`),
`matrix_consistency` (`governance/evidence-architecture.md` §3 grain × scale table vs
`schemas/directness.py`), `reasoning_doc_citations_audit`. All read-only; all advisory.

**3 · Attestation / doctrine ledger.** Commit → `check_commit_msg.py` + `check_doctrine_token.py`
(sharing `commit_gate.py`'s `is_bot`/`is_merge` so the two gates cannot drift) →
`adherence_log_audit.py`, which maps `references/bpc-reasoning/foo.md` →
`attestations/bpc-reasoning_foo.json` at lines 123-125 by **pure string transform, no index** →
`schemas/attestation.schema.json`. `doctrine_recheck.py` cross-references
`governance/doctrine-deltas.json` and the CANONICAL inventory against `decisions/` and
`references/bpc/`.

**Where the join is by text rather than by key:** attestation ↔ artifact (path slugification);
attestation `rules_in_scope` ↔ `references/skill-registry.md` (string identifiers — the gap
`DR-2026-07-13-attestation-rule-identifier-registry-gap` records); commit token ↔ doctrine SHA
(7-hex string); audit brief ↔ item (filename); conflict matrix ↔ `populations` (bare codes, and it
is exactly this text join that produces the quarantined `validate_conflict.py`'s 11 "unknown
population code" errors for `IntD` / `VIS`).

**Where the join is by key, it is level D.** `item_audit_runs.item_code` FK→`items`,
`spec_value_probes.{slug, item_code, ref_id}` FKs, `supersession_check.{slug, ref_id}` FKs — all
`D(fk)`. And `supersession_check` carries the richest CHECK block in the schema (see (h) A6).

## (c) Relation to the previous stage (10 — synthesis)

**Entry contract as designed:** a synthesis artefact exists, is `Status: COMPLETE`, cites only
gate-eligible sources (rule #10: no `metadata_quality = AUTHOR-TITLE-ONLY`, no NULL
`verification_status`), and its numeric claims each name a PMP walk (rule #8 / #10.1).

**What enforces it:**

- Rule-#10 eligibility → `scripts/audit/metadata_integrity_audit.py`, registry id
  `metadata_integrity_audit`, **advisory**, `kinds: [data, synthesis]`. Now examines 0 sources.
- Rule-#8 linkage → `pmp_audit` (advisory) — **structurally incapable** of firing (see (f) 2).
- Attestation-on-touch → `attestation_presence` (**blocking**) — but blind to `references/bpc/`,
  proven on `b35f3f9`.
- Reasoning-doc structure → `validate_reasoning` (advisory, red).

**There is no check anywhere that refuses to audit an item whose synthesis is absent.** The audit
loop's own precondition — that there be something to audit — is unstated and unchecked. This is the
same class as CLAUDE.md §10's *"a gate reporting zero may have examined zero"*, and stage 11 is
where it has bitten hardest: three of its audits went green **because** the reset emptied their
subject.

## (d) Relation to the next stage (12 — render)

**Exit contract as designed** (`governance/pipeline-contract.yaml` stage `render`): the
determination tuple that reaches a register must be the audited one; I1–I5 hold across all six
registers; the mode × stratum matrix matches doctrine.

**What enforces it:**

- `register_integrity_check` (advisory) — I1–I5 + DB cross-check + DB→doc completeness. **Two
  compounding problems.** Its DB arm is vacuous because `evidence_cell_state` is empty (settled by
  experiment, cross-cutting finding 2); *and* its registered `cmd` is `--selftest`, which
  `sys.exit`s before `check()` runs, so at HEAD **no document is evaluated at all** (cross-cutting
  finding 1). The audit→render handoff is verified by nothing in its registered form.
- `matrix_consistency` (advisory) — green, `10/10`.
- `check_rendered_docs` (**blocking**) — C1 citation fidelity, epistemic persistence, doc↔DB drift,
  grade preconditions. Its registered `--all` invocation examines 0 documents *by decision* (see
  stage 12 (f)).
- Nothing carries `item_audit_runs.status = 'COMPLETE'` or `supersession_check.outcome` into a
  render precondition. `grep -rn "item_audit_runs" scripts/generate/ tools/` → no matches:
  **the render layer does not know whether an item was ever audited. NOTHING ENFORCES THIS.**

## (e) The goal of the stage

Stage 11 exists because the project's stated failure mode is *its own author's confidence*. The
integrity-protocol skill states it plainly and evidences it: "4/4 real defects were caught by a
gate, an independent pass, or a selftest; 0/4 by the author's own narrative confidence." The stage's
goal is therefore not "find mistakes" — it is to make specific, recurring defect classes
*structurally visible*: an absolute asserted without a recount; a value that travelled without its
caveat; a numeric spec asserted without probing whether a stricter value is also supported (PMP); a
source superseded since admission (`supersession_check`); a tier stored inconsistently with its own
evidence type; a claim rendered at a strength its evidence does not carry. And to bind each of
those to a durable, dated record — the attestation — so the audit is falsifiable later rather than
remembered.

## (f) How the tools support that goal — and where they do not

**Support.** The attestation schema is the strongest single mechanism in the repo: requiring
`bias_direction` and `independent_reviewer_counterclaim` at ≥ 30 chars each forces the author to
name the direction of their own thumb on the scale, and 74 files show it has actually been done —
including one (`attestations/bpc-reasoning_room-acoustic-performance.json`) whose counterclaim
argues *against the rule that required it* ("three near-identical attestations for a
find-and-replace are ceremony that devalues the attestation record"). `pipeline_contract_audit.py`
is unusually honest: it prints `EXAMINED: 19 contract criteria` and names its own coverage gaps
(`incomplete=5`) rather than passing silently. `claims_docket.py check` is a genuine Mode-2 gate
with a working `--selftest`.

**Where they do not.**

**1 · Most of stage 11's substrate is empty, and three audits went green because of it.**
`pmp_audit` 3 → 0 issues; `adjudication_integrity` 274 → 0; `validate_conflicts` was already
vacuous. A reader of `check-registry.yaml` today is told `adjudication_integrity` is *"RED — 274
tier inconsistencies"* and `pmp_audit` has *"3 issues … walks PMP-A08-001/A18-003/A18-004"*. Both
statements are now false: the tool prints `VERDICT: PASS (tier inconsistencies=0)` and `ISSUES: 0`
respectively, and those 31 `spec_value_probes` rows were deleted by the reset. The registry's own
articulated discipline — `schema_reference_drift_audit`: *"DO NOT WRITE A FIXED NUMBER HERE — re-run
it"* — was not applied to either entry. Both are green-for-the-wrong-reason and neither says so.

**2 · `pmp_audit` CHECK 1 cannot detect the thing it is named for.** Its docstring names the target
population as *"Items asserting numerical specs but lacking a PMP walk (rule #8 mandatory
invocation gap)"*. The SQL (`pmp_audit.py:60-73`) reads:

```sql
SELECT i.item_code, … FROM items i
WHERE i.pmp_last_walk_at IS NULL
  AND i.status NOT IN ('archived','superseded')
  AND EXISTS (SELECT 1 FROM spec_value_probes svp
              WHERE svp.item_code = i.item_code AND svp.spec_value_origin IS NOT NULL)
```

The `EXISTS` clause requires the item to **already have** a `spec_value_probes` row, so an item with
a numeric spec and *no* walk — exactly the target population — is excluded by construction. What the
query actually detects is a bookkeeping desync: probes exist but `items.pmp_last_walk_at` was never
backfilled. This is independent of the reset (the predicate was self-defeating before
`spec_value_probes` was emptied), but the reset makes it unconditionally silent. The comment at
lines 55-60 already names the blocker: `items` carries no `spec_value` / `spec_value_origin` column,
so "has a numerical spec" is not queryable. Two honest options: add `items.spec_value` +
`spec_unit` (a D-SCHEMA decision) and drop the `EXISTS`; or, until then, replace CHECK 1 with an
explicit `EXAMINED: 0 items — 'has a numerical spec' is not representable in the schema; see rule
#8` line, so the 0 is a stated absence rather than a pass. The second is the CLAUDE.md §10
discipline and costs nothing.

**3 · `item_audit_pipeline.py` writes the canonical DB outside the migration path.** `connect()` at
line 62 does `sqlite3.connect(str(DB_PATH))` — read-write, `DB_PATH` defaulting to
`data/guidebook.db` — and `db_update_run()` / `step_started()` / `step_complete()` INSERT and UPDATE
`item_audit_runs`. That table is **not** on the `DR-2026-05-28` exempt list, which is
`evidence_source_authors` + `pipeline_runs` only, and whose §3 states: *"Any OTHER table written
outside migrations remains a violation. Adding a table to the job-owned exemption requires a new
DR."* So the tool's designed operation violates CLAUDE.md rule 4.
`python3 scripts/audit/readonly_db_open_audit.py` → `39/39 read-only consumers open read-only`,
exit 0 — the audit scopes to *read-only consumers*, so a writer is out of scope by design and this
is not a false negative in that tool. The remedy is a decision, not a patch: either add
`item_audit_runs` to the exempt list via a DR (it is genuinely job-owned state, like
`pipeline_runs`), or have the pipeline emit a data migration at run close. Neither has been decided;
the code currently just does it.

**4 · Only 3 of 11 unique contract enforcers ship a `--selftest`.** `pipeline_contract_audit.py`
reports the other 8 by name: `adherence_log_audit`, `matrix_consistency`,
`metadata_integrity_audit`, `pmp_audit`, `research_protocol_audit`, `doctrine_recheck`,
`validate_evidence_state`, `validate_reasoning`. Mode 1 rule 3 of the integrity protocol says *"a
verifier that has only ever passed is unverified"*; by the repo's own rule, 8 of its 11 contract
enforcers are unverified.

**5 · The one enforcer that does selftest currently blocks its own document check.** This is the
sharpest finding in the stage, and it inverts how `register_integrity_check` has been read. Its
registered `cmd` is `--selftest` (`governance/check-registry.yaml`), and `main()` at lines 389-392
runs `sys.exit("SELFTEST FAILED …")` **before** `errors = check(doc, …)`. The selftest currently
fails (one missed mutation, itself caused by an empty subject — cross-cutting finding 2), so
**at HEAD the registered invocation evaluates I1–I5 against no document whatsoever.** The repo has
been recording an advisory FAIL that reads like "one invariant is weak" when the true state is "the
render invariants have not been evaluated." Fixing the subject fixes both at once — which is worth
stating, because the fix looks cosmetic and is not.

**6 · Whole-corpus attestation validity is established by no registered check.**
`attestation_schema` is **blocking**, which reads as strong coverage. It is **diff-scoped**: it runs
`adherence_log_audit.py --check schema` over `--base HEAD~1 --head HEAD`, so it validates only
attestation files appearing in the diff. On a clean tree it reports `attestations: 0` and passes.
The 74/74 validity of the committed corpus is a fact I established by running `jsonschema` by hand,
not a fact CI establishes. **A corrupted attestation that is never re-touched is permanently
invisible to a blocking gate.** This is the same defect class as the `references/bpc/` gap, applied
to files these checks are nominally scoped to — which makes it the more serious of the two.

**7 · `supersession_check`'s own stated invariant is verified by nothing.** The table *is* read by
`scripts/audit/` — `grep -rn "supersession_check" scripts/audit/` returns **5 matches**, in
`code_currency_audit.py` (line 105 runs `SELECT 1 FROM supersession_check sc` inside real SQL) and
`gap_mining_audit.py`. But `code_currency_audit` is **quarantined**, and it uses the table as a
*suppression predicate* for its own currency check — "a supersession check within 365 days with a
current-best outcome suppresses this finding" — not as a supersession audit. The schema's own
comment names the invariant that matters (`'pending'` … *"should not appear on closed slug"*), and
**nothing verifies it**: it is a comment, not a CHECK, and no script tests it.

## (g) How doctrine conditions the stage

- **`governance/mission-and-epistemics.md` §"Citation discipline"** — sources confirmed real;
  "I don't know" > invention; two failed searches → `CLOSED-DELETED`; quantified claims need
  DOI + page/table else `[UNVERIFIED-QUANT]`. This **FORBIDS** an audit that certifies a claim whose
  source it did not open — which is what `reasoning_doc_citations` (rule #10 sub-rules 2/3)
  mechanises, and what `check_rendered_docs.py --doc specs/e-08-brief.html` shows is currently
  violated by the committed briefs (26 failures, all "REF-XXXXX is cited but not in
  `evidence_sources`").
- **§Commitment 2 + `DR-2026-07-21` "Option A"** — **FORBIDS** an audit that lets a
  regulatory-stratum determination reach a register unflagged or above the weak band. That is I3.
- **`governance/doctrine-recheck.md`** — a recheck **must** fire every 25 working sessions, at every
  stage transition, and on any doctrinal-rule revision. **FORBIDS** advancing the global drift
  baseline from a targeted recheck (the integrity-protocol skill records that exact over-reach being
  caught and reverted on 2026-07-24).
- **`skills/integrity-protocol_SKILL.md` Mode 3 clause 4** — **FORBIDS** requesting ratification,
  declaring "done", or marking a PR ready while adversarial findings are unapplied. Level 1.
- **Research contract R8 / R14** — *"KEEP EMPTIES — a zero-yield search is a finding"*; *"a
  zero-yield search is evidence of ABSENCE only if the query was well-formed."* Generalised, this is
  the rule the whole stage keeps breaking: **a zero-finding audit is evidence of cleanliness only if
  it had a subject.** Findings 1, 2, 5 and 6 above are all instances.
- **`decisions/DR-2026-05-28-…-migration-ledger-and-reproducibility-reconciliation.md`** — defines
  the two exempt tables and **FORBIDS** adding to that list without a DR. This is what makes
  `item_audit_pipeline.py`'s direct write a violation rather than a convention.
- **`decisions/DR-2026-07-13-integrity-protocol-three-modes.md`** — ratifies the three modes.

## (h) ACCEPTANCE CONDITIONS — stage 11

What one **audit run** and one **attestation** must satisfy to be admitted.

**The audit run**

1. **An `item_audit_runs` row exists with `status='COMPLETE'` and `steps_complete` covering all 8
   `PIPELINE_STEPS`** · field: `item_audit_runs.status`, `.steps_complete` · **UNENFORCED** —
   `scripts/validate_audit_runs.py` is quarantined (*"Green (87 runs) but unreferenced by any
   contract. Wire only with a stated owner."*).
2. **`status ∈ {IN-PROGRESS, COMPLETE, HANDED-OFF}`** · field: `item_audit_runs.status` ·
   **D — enforced at write time by SQLite** (`CHECK(status IN (…))`). The *value domain* is
   guaranteed; nothing requires the value to be `COMPLETE` before downstream use (row 1).
3. **`item_audit_runs.item_code` resolves to a real item** · field: FK → `items(item_code)` ·
   **D(fk)** — deferred differential check in `migrate_db.py`; new violations fail, pre-existing
   baseline grandfathered, bootstrap exempt; reaches CI via `migration_reproducibility` (blocking).
4. **`spec_hash` matches the current item text** · field: `item_audit_runs.spec_hash` · **level 1** —
   computed at `item_audit_pipeline.py:69` and compared in-run only, and anchored to the v9-0
   snapshot `versions/current/Guidebook_for_Accessible_Design_v9-0_2026-03-20.md`, not to `items`.

**The PMP walk behind a numeric claim**

5. **Every numeric spec has a walk reaching `phase='final'` with ≥ 1 `passes_strict=1` step** ·
   field: `spec_value_probes.phase`, `.passes_strict` · **level 2, vacuous** ·
   `pmp_audit.py` CHECK 2/3 — see (f) 2.
6. **`phase` is one of the seven legal phases; `direction ∈ {up, down}`;
   `claim_type ∈ {minimum, maximum, target, range_low, range_high}`; `passes_strict ∈ {0,1}`** ·
   field: those columns · **D — enforced at write time by SQLite** (four separate `CHECK`s).
7. **`direction` agrees with `claim_type` (minimum → up, maximum → down)** · field:
   `spec_value_probes.direction` × `.claim_type` · **level 2** · `pmp_audit.py` CHECK 6. Note the
   *agreement* is not a CHECK — level D guarantees each column's domain independently, never their
   pairing.
8. **Every passing step carries a `ref_id` to a gate-eligible source** · field:
   `spec_value_probes.ref_id` × `evidence_sources.metadata_quality` / `.verification_status` ·
   **level 2** · `pmp_audit.py` CHECK 4/5. Unexercised (0 rows both sides). Referential existence
   of `ref_id` is separately **D(fk)** → `evidence_sources(ref_id)`.

**The supersession record**

9. **`outcome` is one of the six legal outcomes** · field: `supersession_check.outcome` ·
   **D — enforced at write time by SQLite**.
10. **`superseded_by` / `refined_by` / `divergent_no_supersession` name superseding refs; `refined_by`
    names a refinement dimension; `divergent_no_supersession` carries divergence notes;
    `co1_addition_logged` only on a Co-1 anchor; `anchor_tier` between 1 and 6; `check_method` in
    enum** · field: the corresponding columns · **D — enforced at write time by SQLite** (five
    table-level `CHECK`s plus two column `CHECK`s). This is the richest DDL-enforced contract in the
    schema and it is genuinely strong.
11. **Every T1/T2 anchor on a closed slug has a row with `outcome != 'pending'`** · field:
    `supersession_check.outcome` · **UNENFORCED**. The schema *comment* states it (*"should not
    appear on closed slug"*) but a comment is not a constraint, and the only readers
    (`code_currency_audit.py`, quarantined; `gap_mining_audit.py`) use the table as a suppression
    predicate, not as a supersession audit.

**The evidence-integrity audits**

12. **Stored `tier` == `derive_tier(evidence_type, scope)` for every source** · field:
    `evidence_sources.tier` · **level 2, quarantined and vacuous** ·
    `adjudication_integrity.py`. Registry says *"RED — 274"*; live run says
    `VERDICT: PASS (tier inconsistencies=0)` over 0 sources.
13. **Every triggered prose claim in the diff carries a Mode-1 warrant marker (`VERIFIED-BY` /
    `PREDICTED` / `REPORTED-BY` / `RECOUNTED`)** · field: `working/claims-docket.md` ·
    **level 3 advisory** · `claims_docket.py check`, live `PASS: 68/68`. Registry itself warns:
    *"with no docket file it prints 'nothing to check' and exits 0."*
14. **Every conflict-matrix population code resolves to `populations`** · field:
    `references/conflict-matrices/*.md` (**13 files**) · **UNENFORCED** — `validate_conflict.py` is
    quarantined RED with 11 unknown-population-code errors (`IntD`, `VIS`).
15. **The mode × stratum matrix matches `evidence-architecture.md` §3** · field:
    `schemas/directness.py` · **level 3 advisory** · `matrix_consistency.py` → `10/10 PASS`.

**The attestation**

16. **An attestation exists for every synthesis-path file in the changeset (backfill-on-touch)** ·
    field: `attestations/<slug>.json` · **level 4 blocking, diff-scoped** ·
    `adherence_log_audit.py --check presence`. Blind to `references/bpc/`.
17. **The attestation is schema-valid: each `FIRED` has `evidence_path`, each `SKIPPED` has
    `reason`** · field: `per_rule_status` · **level 4 blocking *for files in the diff only*;
    UNENFORCED for the committed corpus** · `--check schema` + `schemas/attestation.schema.json`
    (`allOf[{if status==SKIPPED then required:[reason]}, {if status==FIRED then
    required:[evidence_path]}]`). See (f) 6 — this is the sharpest vacuity in the attestation layer.
18. **`bias_direction` ≥ 30 chars and `independent_reviewer_counterclaim` ≥ 30 chars** · field:
    those fields · **level 4 blocking, same diff-scope limit** · schema `minLength: 30` on both.
19. **`rules_in_scope` uses stable identifiers from `references/skill-registry.md`, not numbers** ·
    field: `rules_in_scope` · **level 3 advisory** · enforcer is the registered
    **`attestation_evidence`** (`--check evidence`, advisory). The underlying functions
    `check_3_rule_resolution` and `check_5_cross_reference` live inside `CHECK_GROUPS["evidence"]`;
    there is no registered `--check rules` or `--check cross-ref` subcommand — those are debug-only
    invocations CI never runs.
20. **`doctrine_sha` equals the current doctrine SHA, or a `reattestation[]` entry lands within
    `RE_ATTESTATION_WINDOW` = 5 commits** · field: `doctrine_sha`, `reattestation[]` ·
    **level 3 advisory** · same enforcer as row 19 (`attestation_evidence`); the underlying
    functions are `check_2_doctrine_sha` and `check_7_reattestation_window`, again not separately
    registered.
21. **`verdict ∈ {CLEAN, DEVIATION-LOGGED, NON-COMPLIANT, REVERT}`, and `NON-COMPLIANT` is
    surfaced** · field: `verdict` · **informational by design** · `attestation_verdict` — registry:
    *"Never blocking by design."* The enum itself is enforced by the JSON schema.
22. **Commit carries `[DOCTRINE: <7-hex>]` matching HEAD's doctrine SHA** · field: commit subject ·
    **level 4 blocking, push-only, bot/merge/doctrine-self-edit exempt** · `check_doctrine_token.py`
    C1/C2, E1–E4. Note it is a real blocking CI job (`ci.yml:244`) but is **not in
    `check-registry.yaml`**, so `run_checks.py` and `preflight.sh` never run it and CLAUDE.md §7's
    "adding a check means editing the registry" does not describe it.
23. **A doctrine recheck has fired within 25 sessions / at the stage transition** · field:
    `data/doctrine_recheck/` · **level 4 blocking** · `doctrine_recheck.py --cross-ref`, exit 0
    today with 5 unresolved `[2.3]` warnings.

**The review of the review**

24. **Every registered enforcer demonstrates firing on tampered input before its pass counts** ·
    field: enforcer `--selftest` · **level 1 text rule** (integrity-protocol Mode 1 r3) — reported,
    not enforced: `pipeline_contract_audit.py` finds 3 of 11 have one.
25. **A selftest that passes must also have checked the real document** · field: enforcer exit path ·
    **UNENFORCED, and currently violated** · `register_integrity_check`'s registered `--selftest`
    `sys.exit`s at line 391 before `check()` at line 392, so a selftest failure suppresses document
    coverage entirely. Nothing in the registry can express "this check must examine a document"
    because `min_items` reads an `EXAMINED:` line the script does not print.
26. **An audit that reports zero must state its examined count** · field: stdout · **level 1 text
    rule, partially mechanised** · done by `citation_mining_completeness.py`,
    `check_rendered_docs.py`, `pipeline_contract_audit.py`; **not** done by `pmp_audit.py`,
    `adjudication_integrity.py`, `register_integrity_check.py`.

**Remedies.** Rows 5, 8, 12 and — for the committed corpus — the empty-subject half of 1 are all
ratified-empty under `DR-2026-08-06`. Declaring `min_items` on `pmp_audit` or
`adjudication_integrity` would produce a permanently red advisory that the next session learns to
ignore. The `known_debt.yaml`-shaped suppression is the right instrument: `warrant:` naming the
reset DR, `lift_when_sql: "SELECT COUNT(*) FROM spec_value_probes"` / `"… FROM evidence_sources"`,
`lift_when_ge: 1`, so the suppression reports *itself* STALE the moment research resumes. Rows 11,
17, 25 and 26 are **not** in that class — they are unenforced by construction and no amount of data
returning will change them.

---

# STAGE 12 — RENDER

### 2.12 Stage 12 — Render

## (a) Tools, tables, methodology

| Artefact | Path | State | Evidence |
|---|---|---|---|
| Parts generator | `scripts/generate_parts.py` | **BUILT+EXERCISED, output STALE, ungated** | regenerating to scratch differs in **all 15 files** (`diff -rq parts/v10 $T \| wc -l` → 15) |
| Parts output | `parts/v10/manifest.md`, `part00–13.md` | **STALE** | committed fingerprint `3d7fb5d50de6` vs fresh `a6bc6d4851ef`; `part13.md` publishes `640 sources in the evidence base` against a fresh `0 sources in the evidence base` |
| Site driver | `scripts/generate/build_site.py` | **BUILT+EXERCISED** | drives `site/specs/` only; docstring says so explicitly |
| Spec page | `scripts/generate/spec_page.py` | **BUILT+EXERCISED** | 93 pages, 0 orphans; `ls site/specs \| wc -l` → 93, `items` = 93 |
| Population page | `scripts/generate/population_page.py` | **BUILT+EXERCISED, no driver** | works when called directly; `ls site/populations \| wc -l` → **11** vs `populations` = **23** |
| Room page | `scripts/generate/room_page.py` | **BROKEN — crashes on the live schema** | `python3 scripts/generate/room_page.py R-BA` → `sqlite3.OperationalError: no such table: room`, exit 1 |
| Room output | `site/rooms/r_*.html` (17) | **ORPHANED** | generated pre-schema-rename at `eafab6d`; regenerable by nothing today |
| Pilot renderings | `scripts/generate/pilot_renderings.py` (`REGISTER_MAP`, `ROLES`, `tuple_class`) | **BUILT+UNEXERCISED** | fresh run → `0 cells rendered × 6 roles` (984-byte file) vs the committed 87,730-byte `working/pilot/pilot-renderings.html` holding 15 cells |
| Register integrity | `scripts/audit/register_integrity_check.py` (I1–I5) | **BUILT, SELFTEST FAILING, DOCUMENT NOT EVALUATED** | `--selftest` → 11 FIRED, 1 `**SILENT — MUTATION MISSED**`, exit 1 before `check()` |
| `weighting_profile` | DB, 5 rows | **BUILT+UNEXERCISED** | `grep -rln "weighting_profile" --include=*.py scripts/ tools/` → **0**. No renderer reads it |
| Vetting surface | `tools/regenerate_vetting_surface.py` → `tools/spec-curation-vetting-surface.html` | **BUILT+EXERCISED, current, UNGATED** | regenerates byte-identical; **no `--check` flag** (`error: unrecognized arguments: --check`); no registry entry |
| Rendered-doc gate | `scripts/audit/check_rendered_docs.py` | **BUILT, registered invocation examines nothing by decision** | `--all` → `EXAMINED: 0 …`, exit 0; `--doc specs/e-08-brief.html` → 26 failures, exit 1 |
| Browser render audit | `scripts/audit/render_audit.js` | **BUILT+EXERCISED, green** | `RESULTS: 12/12 checks passed (2 document(s), 0 failure(s))`, exit 0 |
| Dashboards | `tools/evidentiary_audit.py`, `tools/pipeline_completeness.py` | **BUILT+EXERCISED, current** | `--check` on each → `OK: all audit outputs are up to date.` / `OK: pipeline-completeness-dashboard.html is current.` The registry's `evidentiary_audit_fresh` note (*"STALE on main as of 2026-08-01"*) is out of date |
| Mockup | `index.html` + `assets/guidebook.css` | **HAND-AUTHORED, not generated** | 39,180 bytes; **95** `href="#"` placeholders; 7 internal links, 6 of them `specs/e-08.html` variants |
| Site index | `site/index.html` | **hand-authored, a different document from the mockup** | 15,461 bytes; **10** `href="#"`; no `honest-banner` markup; no script writes it |
| Workflow | `.github/workflows/regenerate-derived.yml` | **BUILT+EXERCISED** | 3-leg matrix: vetting-surface, evidentiary-audit, pipeline-completeness |
| Registered render checks | `pipeline_completeness_fresh` (blocking) · `evidentiary_audit_fresh` (blocking) · `check_rendered_docs` (blocking) · `site_pages_fresh` (advisory) · `register_integrity_check` (advisory) · `render_audit_browser` (advisory, `optional_exit2`) | — | `governance/check-registry.yaml` |

## (b) How they relate to each other

Three *independent* render paths over one DB, with no shared driver and no shared freshness model.

**Markdown path.** `generate_parts.py` → `parts/v10/*.md`. Its DB fingerprint hashes
`items;populations;bpc_metadata;slugs;connections;conflicts;evidence_sources;gaps;evidence_cell_state;convergence_assessment;terms;user_version`,
written into `manifest.md` and each part header. **No check compares it to a fresh render.**

**HTML path.** `build_site.py` walks `items ORDER BY item_code`, calls `spec_page.query_item` →
`render_html`, and its `--check` mode compares `sha256(disk)` vs `sha256(fresh)` — the only
content-addressed freshness gate in the repo, and the only mechanism that can detect a hand-edit of
generated output. It deliberately does **not** drive `population_page.py` or `room_page.py`. Its
docstring states the scope plainly: *"this drives `site/specs/` only. `site/populations/` (11 files)
and `site/rooms/` (17 files) have generators — population_page.py and room_page.py — that it does
NOT drive; room_page.py additionally crashes against the live schema (no `rooms` table). Naming this
'build every page' would be false for 28 of ~121 files."* `build_site.py` uses its own `FP_TABLES`
fingerprint, deliberately the same shape as `generate_parts.py:83` — but the two are separate
constants that must be kept in step by hand.

**Register path.** `pilot_renderings.py` reads `evidence_cell_state` (plus `evidence_sources` for
jurisdiction breadth), computes `tuple_class(state, tier_basis, conv, rso, n_reg_refs, n_reg_jur)`,
and emits one `<div class='rendering'>` per cell × 6 roles, with claim text taken verbatim from
`REGISTER_MAP`. `register_integrity_check.py` **imports `REGISTER_MAP`, `ROLES` and `tuple_class`
from the renderer** (line 34) — a single source of truth — which is why the registry classifies it
under `kinds: [render, data, tooling]`. That shared import is also exactly why the checker adds
`lint_register_map()`: shared-constant equality would otherwise confirm the document matches a map
that had stopped telling the truth.

**Text joins:** `site/specs/<item_code.lower()>.html` ↔ `items.item_code`;
`site/rooms/<room_id.lower().replace('-','_')>.html` (`room_page.py:261`) — note the *underscore*
convention, unlike specs' hyphens, so anything later driving both must not assume one convention;
`attestations/<path-slug>.json`; and `REGISTER_MAP` keys ↔ `tuple_class` return strings.

## (c) Relation to the previous stage (11 — adversarial QA & audit)

**Entry contract as designed:** only an audited, attested determination reaches a register; the
determination tuple rendered must be the one the DB holds; I1–I5 hold.

**What enforces it:**

- Doc→DB tuple equality → `register_integrity_check.check()` lines 181-196, guarded by
  `if db_rows:`, and `db_rows` is built from `evidence_cell_state` (0 rows). Verified:
  `m.check(doc, 'data/guidebook.db')` → **0 errors** on a document asserting 15 determinations with
  SHAs, tier bases and reg-ref counts.
- DB→doc completeness (suppression detection) → same function, lines 158-170, same guard, same
  vacuity. **Settled by experiment** (cross-cutting finding 2): populate the 15 rows and both
  directions come alive, 12/12 mutations fire, exit 0.
- **And above both:** the registered invocation is `--selftest`, which `sys.exit`s before `check()`
  runs at all. So even the document's own self-reported attributes are not being checked in CI
  today.
- Audit status → **NOTHING ENFORCES THIS.** `grep -rn "item_audit_runs" scripts/generate/ tools/` →
  no matches.
- Citation fidelity of rendered docs → `check_rendered_docs` is **blocking**, and its registered
  `--all` examines 0 documents by decision (see (f) 4).

## (d) Relation to the next stage — there is none; this is the terminus

The exit is the reader. The only downstream contract is the product posture itself.

- **Honest banners.** `spec_page.py` emits
  `<p class="honest-banner">Best-practice determination: <strong>not yet computed</strong> for this
  item, for any population.</p>` when an item has no cells. This is the doctrinally correct output
  today, and it is exactly what 11 of the 12 stale pages are missing.
- **Determinism.** `build_site.py`'s docstring records the owner directive of 2026-08-04: *"the site
  must not depend on an expiring CI artifact… the same DB and the same generators reproduce it
  exactly."* `--check` is the mechanisation. Enforcement: **advisory** (`site_pages_fresh`), so the
  site can and does ship stale.
- **Write-back.** `regenerate-derived.yml` commits regenerated dashboards back to `main` as the bot.
  Its header (lines 16-22) claims the PR-side `--check` duty *"now belongs to ci.yml's `render`
  battery, which runs the same `--check` gates from governance/check-registry.yaml."* **That claim
  is false for one of its own three legs**: `tools/regenerate_vetting_surface.py --check` →
  `error: unrecognized arguments: --check`, and `grep -n vetting governance/check-registry.yaml`
  returns nothing. Its own phrasing — *"Two of the three old workflows also ran a check job"* — is
  the tell that the third never had one. Currently benign (the artifact regenerates byte-identical)
  but it is an unguarded write-back path whose documentation asserts a guard that does not exist.

## (e) The goal of the stage

Render is where the project's epistemics either survive contact with a reader or are laundered away.
The design is unusually explicit about this: one determination, six audience registers (`designer`,
`ot`, `policymaker`, `disabled_person`, `carer`, `advocacy_brief`), and a finite `REGISTER_MAP` from
which all claim-strength language must be drawn verbatim — so that "translating for the audience"
cannot become "strengthening for the audience." I1 forces the six renderings to carry an identical
determination tuple; I2 forces the policymaker view to pair FLOOR with ANCHOR so a code minimum
cannot be read as a target; I3 (as amended by Option A) forces a regulatory-stratum determination to
render as flagged weak-band (○) — never suppressed, never above the band; I4/I5 force claim text to
*equal* its map row. `weighting_profile` is the designed mechanism for re-ranking *which* cells are
foregrounded per audience without ever moving a claim to a different row of that map
(`governance/evidence-architecture.md:136`). The goal, in one sentence: **make it mechanically
impossible for the guidebook to say something stronger to one audience than the evidence lets it
say to any other.**

## (f) How the tools support that goal — and where they do not

**Support.** The `REGISTER_MAP`-imported-by-the-checker pattern, plus `lint_register_map()`, is
genuinely good design: it closes the loop where a checker and a renderer sharing a constant "agree"
while both being wrong. `build_site.py --check`'s content-addressed comparison is the only freshness
mechanism in the repo that can detect a hand-edit of generated output. `render_audit.js`'s exit-code
discipline (2 = environment cannot run it → loud SKIP; 3 = crash → fail) is the correct answer to a
class of silent-skip bug, and the registry honours it via `optional_exit2` at
`run_checks.py:251,262`. `spec_page.py`'s honest banner is the doctrinally right default.

**Where they do not.**

**1 · The register layer is doubly disarmed.** Every I1–I5 check that would run does so against the
document's own `data-*` attributes, because `db_rows` is empty; and none of them runs at all under
the registered `cmd`, because `--selftest` exits first. The checker's *own comment* (lines 158-164)
names the failure mode it was built to catch — *"this document sat frozen at 7 of 15 cells for weeks
because its generator crashed"* — and the fix it installed is now disarmed by the reset. To be
precise about the diagnosis, because it changes the remedy: **the invariant, the tamper and the
regex are all correct; only the subject is missing.** That is settled by experiment, not inferred.

**2 · Eleven committed pages publish determinations for evidence the database no longer holds.**
`python3 scripts/generate/build_site.py --check` → exit 1, **12** stale:
`a-02, a-08, a-18, b-08, b-10, c-02, c-06, e-06, e-08, e-12, f-07, g-03`. The same 12 via the
registry: `run_checks.py --kinds render --battery render` → `[FAIL] site_pages_fresh (advisory) …
12 staleness finding(s)`.

The 12 are **not** one phenomenon. Rendering each fresh in-process and classifying the diffs:

| pages | determination table lost | governing-sources block lost | `item_bpc_links` row lost |
|---|---|---|---|
| a-02, a-08, b-08, b-10, c-02, c-06, e-06, e-08, e-12, g-03 (10) | **yes** | **yes** | no |
| a-18 | **yes** | **yes** | **yes** |
| **f-07** | **no** | **no** | **yes** |

So **11 pages lost determination tables**, not 12. `site/specs/e-08.html` publishes
`DEAF | stated | CO1+T2 | … | Overturned if the anchoring sources are retracted…` plus
`<h3>DEAF — 7 governing sources</h3>` with REF-00338/339/342/343/344/345/347, tier badges and
`VERIFIED`; its fresh render is the single honest banner. `site/specs/a-02.html` publishes
`ALL | provisional | T4-6-only(regulatory_stratum_only)` with the full Option-A caveat and
`REF-00563` (ANSI/ASA S12.60-2010/Part 1, T4, VERIFIED); fresh render, the honest banner.

**`f-07` is a different mechanism entirely.** It carries **no determination on disk at all**. Its
whole 5-line content diff is the BPC table losing two `item_bpc_links` rows
(`ms-thermal-temperature-conflict-resolution` primary, `thermal-comfort-older-adults-care-settings`
secondary, both `RETRACTED-PRE-REHAB`) and gaining `No governing BPC recorded for this item.` The
reset's `DELETE FROM item_bpc_links; -- 3 rows` removed exactly three rows: two were F-07's, the
third A-18's. F-07 lost BPC links, not cells.

**The framing that follows.** This is **the visible half of the reset**, not routine housekeeping.
Eleven committed pages publish `stated`/`provisional` best-practice determinations with named
`VERIFIED` governing sources against a corpus of `evidence_sources` = 0. Regenerating is a one-liner
but it is a doctrinal correction, not a chore — and `site_pages_fresh` is **advisory**, so it ships.
The stale cohort is also almost exactly the pilot cohort: `working/pilot/pilot-renderings.html`
contains exactly 11 distinct item codes and all 11 are in the stale set, F-07 being the twelfth by a
different route.

**3 · `parts/v10/` is stale in all 15 files and no check or workflow covers it.**
`python3 scripts/generate_parts.py --out $T; diff -rq parts/v10 $T` → 15 files differ. Fingerprint
`3d7fb5d50de6` → `a6bc6d4851ef`. `part13.md`: `640 sources in the evidence base.` → `0 sources in
the evidence base.` `manifest.md` fingerprint inputs
`items=92;populations=22;bpc_metadata=82;slugs=82;connections=273;…evidence_sources=640;gaps=296;terms=30;user_version=25`
→ `93;23;0;106;0;…0;0;88;53`. Why nothing catches it: `grep -rn "generate_parts" governance/
.github/` → **0 matches**. `parts/**` appears in `check-registry.yaml` only as a *kind path* under
`kinds.render.paths`, which routes a parts-touching diff to the render battery — a battery
containing no parts check. `regenerate-derived.yml`'s matrix has three legs and `generate_parts.py`
is not one of them. The remedy is a real gap-fill, not a suppression: add `generate_parts.py
--check` (the same sha256-vs-fresh comparison `build_site.py` already implements), register it as
`parts_fresh` in the `render` battery on `kinds: [data, render]`, and add a fourth matrix leg.

**4 · `check_rendered_docs --all` examines nothing BY DECISION — and the honest finding is narrower
and sharper than "a blocking gate that cannot fire."** The exclusion is documented as deliberate in
**both** places. The registry entry: *"`min_items: 1` was added and RETIRED on 2026-08-06… retired
hours later by the clean-room reset, which made specs/ reference-only: those briefs cite REF-ids the
reset removed, deliberately, so `--all` now examines nothing **BY DECISION**. The distinction the
guard exists for still holds — a check passing on an ACCIDENTALLY empty subject is worthless — and
it does not apply to a subject that is empty because the owner said so… Re-declare `min_items` the
day specs/ is regenerated against the live DB."* And the script's own comment (lines 229-234):
*"specs/*.html are hand-authored briefs preserved as REFERENCE by the 2026-08-06 clean-room reset…
by design, not by breakage."* Calling this a defect misreads a ratified decision.

The real finding is three-part and worth more than the discarded one:

- **A blocking check now certifies nothing.** `check_rendered_docs` is `level: blocking` and returns
  exit 0 having examined 0 documents. Whatever its reason, the *state* of the render battery is that
  its strongest gate contributes no assurance, and a reader of the registry sees "blocking" and
  infers coverage.
- **Its restoration is guarded only by a prose note that nothing evaluates.** The instruction
  "re-declare `min_items` the day specs/ is regenerated" lives in a YAML `note:` field. No code
  reads it, no check tests for it, and nothing fires when `specs/` is regenerated. Compare the
  `known_debt.yaml` mechanism the repo already has, where `lift_when_sql` + `lift_when_ge` make
  exactly this kind of "restore when X" condition *executable* and report the suppression as STALE
  when the condition is met. The rendered-docs exclusion is the same shape of debt expressed in the
  one form that cannot self-lift.
- **Re-declaring `min_items` today would correctly turn the check red.** `vacuity_failure()`
  (`run_checks.py:274-300`) reads the `EXAMINED:` line; `EXAMINED: 0` < `min_items: 1` yields
  *"examined 0 item(s), below the declared minimum of 1 — the check passed by having nothing to look
  at"* and a **blocking** failure. So the guard is not merely absent, it is *withheld* — and
  correctly so while the warrant holds, which is precisely why the warrant needs to be executable
  rather than prose.

One residual mechanical point survives independently of the decision: the short-circuit at lines
235-238 is **unconditional**, returning before the `EXAMINED: {len(docs)}` line and before the
`if not docs:` FAIL path. So a *newly regenerated* brief dropped into `specs/` would also be
skipped — the code cannot distinguish the reference cohort from a live document. A manifest-driven
exclusion (a `specs/REFERENCE-ONLY` list, or an in-file `<!-- reference-only: DR-2026-08-06 -->`
marker) with `EXAMINED: N (M excluded as reference-only)` would make the exclusion precise and make
`min_items: 1` meaningful again the moment a live brief exists.

*Cosmetic sub-defect:* the results line computes passes as `4 - failures`, producing
`RESULTS: -22/4 checks passed` on `--doc specs/e-08-brief.html`.

**5 · `weighting_profile` is a table nothing reads.** Its 5 rows encode the entire audience-emphasis
doctrine, including the policymaker row's `"anti_laundering"` foreground and the
`disabled_person`/`advocacy_brief` mandatory instrument-status caveat.
`grep -rln "weighting_profile" --include=*.py scripts/ tools/` → **0**. Register behaviour is
instead hard-coded in `REGISTER_MAP`. Two stores for one doctrine, and per CLAUDE.md §2 the DB is
canonical — so **the operative implementation is currently the non-canonical one.** (The table's
own `CHECK (json_valid(tier_weights))` guarantees the rows are well-formed, which is level D
enforcement of data nobody consumes.)

**6 · `room_page.py` queries six tables that do not exist, and it is the odd one out by omission.**
`python3 scripts/generate/room_page.py R-BA` → `sqlite3.OperationalError: no such table: room`,
exit 1.

| Queried | Line(s) | Exists | Live equivalent | Rows |
|---|---|---|---|---|
| `room` | 26, 29 | No | `rooms` | 17 |
| `room_item` | 35 | No | `room_items` | **0** |
| `room_item_population` | 44, 84 | No | **none** | — |
| `specification` | 51 | No | `items` | 93 |
| `room_dar_provision` | 66 | No | **none** | — |
| `room_conflict` | 75 | No | **none** | — |

It is not a rename-only fix: `rooms` columns are `(room_code, name, category, description, status,
notes, created_at, created_by_session, updated_at, updated_by_session)` — no `room_id`, and no
`room_label`, `building_type`, `evidence_density` or `criticality_note`, all of which
`render_html()` reads at lines 93-97. `items` has `name`, not `title`. `room_item_population`,
`room_dar_provision` and `room_conflict` have **no substitute**; per-(room, item) population
applicability is simply not modelled, and substituting the room-agnostic `item_population_links`
(372 rows) would silently change the page's meaning from "this population needs this item *in this
room*" to "*anywhere*" — a D-SCHEMA decision, not a code edit. And even after every rename, **every
room page renders zero items**, because `room_items` has 0 rows.

**The damning part is that both siblings record having been fixed for exactly this reason and this
one was not.** `spec_page.py`'s docstring: *"there is no canonical `specification` table (confirmed
absent from data/guidebook.db) … This is a rewrite of the previous version of this script, which
queried the non-existent `specification` table and **failed on every invocation**."*
`population_page.py`'s docstring: *"…queried against a `population`/`specification`/`room` schema
that was never migrated into the canonical DB … a rewrite of the previous version, which queried the
non-existent `population`, `specification`, and `conflict` tables and **failed on every
invocation**."* `population_page.py` names `room` as one of the never-migrated tables **while fixing
itself and leaving `room_page.py` broken in the same directory**. Two of three generators were fixed
in the same pass under `DR-2026-07-12-website-architecture-lock.md` item 4; the third was left
crashing.

**7 · `site/populations/` has 11 files for 23 populations** and no driver. `population_page.py`
works when called directly; nothing calls it in a loop, and no check notices the 12 missing pages.
`build_site.py`'s `orphan_pages()` covers only `site/specs/`.

### The mockup vs the generated site — the honest current state

- `index.html` (39,180 bytes) is **hand-authored**. `grep -o 'href="[^"]*"' index.html | sort | uniq
  -c` → **95 × `href="#"`**, against **7 internal links, 6 of them `specs/e-08.html` variants**
  (`specs/e-08.html` ×3, `?mode=question`, `#populations`, `#conflicts`) plus `index.html` itself.
  CLAUDE.md §1's "wired only for a lone exemplar" is exactly right. It links to **root** `specs/`,
  which holds exactly 2 files (`e-08.html`, `e-08-brief.html`) — *not* to `site/specs/` (93 files).
  Root `specs/` is the "hand-authored briefs preserved as REFERENCE" cohort.
- **On `specs/e-08.html?mode=question`:** the link works. A query string on a static file served over
  HTTP is simply ignored and the page loads. The real finding is that `specs/e-08.html` contains
  **no query-string handler at all** — `grep -c "searchParams\|mode=question" specs/e-08.html` → 0,
  its five "mode" hits being `class="mode-spec"` and prose. **The link resolves; the *mode* does
  nothing.**
- `site/index.html` (15,461 bytes) is **a materially different document**, not a copy of the mockup.
  Root has **95** `href="#"`; `site/index.html` has **10**. Root's `<h2>All 91 provisions by
  category</h2>` directory — the section carrying those 95 dead links — is **absent** from
  `site/index.html` (`grep -c "All 91 provisions by category"` → root 1, site 0), replaced by
  `Specifications · last modified` / `One record, many lenses` / `How to read this site`. Same visual
  language, different document. It is still **not generated by anything** (`grep -rn "site/index"
  scripts/ tools/` → nothing) and carries none of `spec_page.py`'s `honest-banner` markup
  (`grep -c honest-banner site/index.html` → 0): a hand-authored front door sitting on top of a
  generated corpus.
- The generated corpus is `site/specs/` (93 real pages, 0 orphans, 12 stale) plus two
  generated-once-and-orphaned directories: `site/populations/` (11 of 23) and `site/rooms/` (17
  files whose generator no longer runs).
- **Honest summary:** the guidebook has one real generated surface (`site/specs/`), one hand-authored
  mockup (`index.html`), a second hand-authored front door under `site/` that is *related to but not
  identical with* the mockup, and two abandoned generated directories. CLAUDE.md §1's framing is
  accurate; the correction is that `site/index.html` is its own hand-authored document, so a reader
  who opens it expecting generated output gets prose that no generator produced.

## (g) How doctrine conditions the stage

- **`governance/mission-and-epistemics.md` §Commitment 2 + §Evidence-state machine** — a rendering
  must show the *state* of the claim, not just the claim. **FORBIDS** rendering a `pending` cell as a
  bare value; `[BEST-PRACTICE-PENDING]` + gap link is required. Mechanised as I3 + G8 ("pending cells
  render with disclosure", cited at `register_integrity_check.py:164`).
- **§Commitment 7** ("teaches judgment, does not substitute") + §Purpose — **FORBIDS** the site
  presenting a value as a compliance answer. This is what I2's FLOOR↔ANCHOR pairing exists for.
- **`governance/tier-system.md` §5 + §8** — regulatory-stratum determinations sit at ○. **FORBIDS**
  `[●` or `[◐` on an RSO rendering: `ABOVE_BAND_RE = re.compile(r"\[●|\[◐")`,
  `register_integrity_check.py:70`.
- **`governance/evidence-architecture.md` §6** — the five register invariants I1–I5 are stated
  there; §3 is the mode × stratum matrix `matrix_consistency.py` checks; line 136 is the sentence
  that **FORBIDS** `weighting_profile` from ever moving a rendering to a different row of the map.
- **`decisions/DR-2026-07-21` "Option A"** — repealed the absolute I3 ("no best-practice language on
  an RSO cell, ever") and replaced it with the narrower prohibition.
  `register_integrity_check.py:228-251` implements the amendment, and its docstring records that it
  enforced the repealed form until 2026-08-04 — a live example of the repo correcting a checker that
  had outlived its rule.
- **`decisions/DR-2026-07-25`** — the rendered-document integrity gate (`check_rendered_docs`).
- **`decisions/DR-2026-07-12-website-architecture-lock.md`** + `workplan/website-v0-path-forward-2026-07-12.md`
  — the owner-gated tracking of `room_page.py`'s phantom tables (named in the
  `schema_reference_drift_audit` quarantine entry as *"room_page.py's 6 phantom tables — an
  already-tracked, owner-gated gap"*).
- **`decisions/DR-2026-08-06-clean-room-evidence-reset.md`** — **FORBIDS** the project proceeding as
  though research has been performed. The 11 spec pages still publishing determinations, and
  `part13.md` still publishing "640 sources in the evidence base" with a full tier distribution
  (T1 93 / T2 67 / T3 206 / T4 66 / T5 119 / T6 89), are direct, currently-shipping violations.
- **Research contract R3** — quantified values carry a locator; a rendered numeric without one must
  carry `[UNVERIFIED-QUANT]`. Checked on rendered docs only via `check_rendered_docs.py`, whose
  registered invocation examines 0 documents.

## (h) ACCEPTANCE CONDITIONS — stage 12

What one **rendered page** must satisfy to be admitted.

**Freshness — the page matches its source**

1. **`sha256(site/specs/<item>.html)` equals a fresh `spec_page.render_html` from the committed DB** ·
   field: file bytes · **level 3 advisory** · `build_site.py --check`, registry `site_pages_fresh`.
   **Currently failing on 12 pages**, 11 of which publish determinations the DB no longer holds.
2. **No page in `site/specs/` lacks a row in `items`** · field: filename ↔ `items.item_code` ·
   **level 3 advisory** · `build_site.orphan_pages()`. Clean today.
3. **`parts/v10/*.md` matches a fresh `generate_parts.py` run** · field: file bytes ·
   **UNENFORCED** — no check, no registry entry, no workflow leg. Stale in all 15 files.
4. **`tools/spec-curation-vetting-surface.html` matches a fresh regeneration** · field: file bytes ·
   **UNENFORCED** — the tool has no `--check` flag and no registry entry, while
   `regenerate-derived.yml`'s header claims otherwise. Currently byte-identical, so benign today.
5. **`tools/pipeline-completeness-dashboard.html` is current** · field: file bytes ·
   **level 4 blocking** · `tools/pipeline_completeness.py --check` (`pipeline_completeness_fresh`).
   Green.
6. **`audits/evidentiary-base-audit.*` + dashboard are current** · field: file bytes ·
   **level 4 blocking** · `tools/evidentiary_audit.py --check` (`evidentiary_audit_fresh`). Green
   (the registry's "STALE on main" note is out of date).
7. **`site/populations/` has a page per population** · field: `populations` (23) vs
   `site/populations/` (11) · **UNENFORCED** — no driver, no check.
8. **Room pages are regenerable from the DB** · field: `rooms`, `room_items` · **BROKEN** —
   `room_page.py` crashes on `no such table: room`; six queried tables do not exist.
9. **Generated output is never hand-edited** · field: `parts/`, `site/` · **level 1 text rule**
   (CLAUDE.md §10), partially mechanised for `site/specs/` only, by row 1.

**Register invariants — the six audience renderings**

> **All of rows 10–18 carry the same overriding caveat.** They are registered under
> `register_integrity_check`, whose registered `cmd` is `--selftest`, and whose `main()`
> `sys.exit`s at line 391 before `check()` at line 392. Each row's `--selftest` demonstrates the
> invariant **firing on tampered input**; **none of them is currently evaluated against
> `working/pilot/pilot-renderings.html` by the registered invocation.** "level 3 advisory,
> selftest FIRES" is a true statement about the mutation harness and a misleading one about
> document coverage.

10. **All six `ROLES` present for every cell** · field: `data-role` attrs · **level 3 advisory;
    not evaluated at HEAD** · `check()` lines 171-175.
11. **I1 — identical `(state, tier-basis, conv, rso, cfo, sha, rule-version, reg-refs, reg-jur)`
    across all six registers** · field: `data-*` attrs · **level 3 advisory; not evaluated at
    HEAD** · lines 176-180. Selftest fires.
12. **I2 — policymaker body pairs `FLOOR` with `ANCHOR`** · field: `<p class='emphasis'>` bodies ·
    **level 3 advisory; not evaluated at HEAD** · lines 267-273. Selftest fires.
13. **I3 (amended) — no `[●`/`[◐` on an RSO rendering; best-practice language only in an element
    that also carries a weak-band flag, per element not per rendering** · field: `claim` + each
    `<p class='emphasis'>` · **level 3 advisory; not evaluated at HEAD** · lines 228-251. Selftest
    fires on both the marker case and the synonym-smuggling bypass.
14. **I4/I5 — claim text *equals* `REGISTER_MAP[tuple_class][role]` after `.format(basis, n_refs,
    n_jur)`** · field: `<p class='claim-strength'>` · **level 3 advisory; not evaluated at HEAD** ·
    lines 257-266. Selftest fires.
15. **No inflation lexicon anywhere in any rendering** · field: claim + body · **level 3 advisory;
    not evaluated at HEAD** · `INFLATION_LEXICON`, lines 252-256. Selftest fires.
16. **`data-tuple-class` equals `tuple_class(...)` recomputed from the attrs, and `data-rso` agrees
    with the tier-basis marker** · field: attrs · **level 3 advisory; not evaluated at HEAD** ·
    lines 207-226. Selftest fires.
17. **No Python `None` repr in `data-sha` / `data-rule-version`** · field: attrs · **level 3
    advisory; not evaluated at HEAD** · lines 202-206. Selftest fires.
18. **Every weak-band `REGISTER_MAP` row carries, per register, a flag *and* the
    code-is-not-evidence caveat** · field: `REGISTER_MAP["rso_weak_broad"/"rso_weak_single"]` ·
    **level 3 advisory** · `lint_register_map()`, which runs unconditionally and is therefore the
    one register invariant not dependent on the document. Selftest fires.

**Register invariants — the DB binding**

19. **Rendered attrs equal the `evidence_cell_state` row (doc → DB)** · field:
    `evidence_cell_state` · **VACUOUS** — guarded by `if db_rows:`, and the table has 0 rows.
    **Settled by experiment:** populate the 15 rows the document renders and this direction comes
    alive and passes clean.
20. **Every `evidence_cell_state` row has a rendering (DB → doc; suppression is an integrity
    failure)** · field: `evidence_cell_state` · **VACUOUS** — same guard. The selftest reports it as
    a MISSED MUTATION; the experiment shows it is a missing subject, not a broken invariant.
21. **The determination rendered corresponds to a row whose `state` is legal and whose (item,
    population) is unique** · field: `evidence_cell_state.state` CHECK, `UNIQUE (item_code,
    population_code)` · **D — enforced at write time by SQLite**. This is the one binding in the
    render path that cannot be disarmed by an empty table — because it constrains what may ever be
    written, not what is currently there.
22. **`weighting_profile.tier_weights` is valid JSON** · field: `weighting_profile.tier_weights` ·
    **D — enforced at write time by SQLite** (`CHECK (json_valid(tier_weights))`). Well-formed data
    that **no renderer reads** — see row 25.

**Rendered-document integrity**

23. **Every REF cited in a rendered document exists in `evidence_sources`** · field: rendered HTML ↔
    `evidence_sources` · **level 4 blocking; the registered `--all` invocation examines 0 documents
    BY DECISION** · `check_rendered_docs.py`. `--doc specs/e-08-brief.html` → 26 C1 failures, exit 1.
    The restoration condition ("re-declare `min_items` the day specs/ is regenerated") lives in a
    YAML `note:` that nothing evaluates.
24. **Rendered docs preserve epistemic markers, grade preconditions, and no doc↔DB drift** · field:
    rendered HTML · **same as row 23** · `check_epistemic_persistence`, `check_doc_db_drift`,
    `check_grade_preconditions`.
25. **Audience emphasis derives from `weighting_profile`** · field: `weighting_profile` ·
    **UNENFORCED — and unimplemented.** No renderer reads the table; the behaviour is hard-coded in
    `REGISTER_MAP`, i.e. the non-canonical store is operative.
26. **Browser-level render checks pass, or SKIP loudly on exit 2 (crash = exit 3 = fail)** · field:
    DOM · **level 3 advisory, `optional_exit2`** · `node scripts/audit/render_audit.js` →
    `RESULTS: 12/12 checks passed (2 document(s), 0 failure(s))`.

**Remedies, correctly shaped.** Rows 19, 20 and 23 are empty **by ratified decision**
(`DR-2026-08-06`), so `min_items` is the wrong instrument for all three — on row 23 it would
correctly turn a blocking check red today, which is the point. The right instrument is a warranted
self-lifting suppression carrying the reset DR as `warrant` and the condition as executable SQL, in
the `scripts/audit/graph/known_debt.yaml` shape:

```yaml
- id: rendered-docs-reference-only-post-reset
  check_id: check_rendered_docs.empty_subject
  warrant: "DR-2026-08-06-clean-room-evidence-reset — specs/ preserved as REFERENCE; briefs cite removed REF-ids"
  lift_when_sql: "SELECT COUNT(*) FROM evidence_sources"
  lift_when_ge: 1

- id: register-db-crosscheck-no-subject
  check_id: register_integrity_check.db_arm_empty
  table: evidence_cell_state
  warrant: "DR-2026-08-06-clean-room-evidence-reset — determinations deliberately emptied"
  lift_when_sql: "SELECT COUNT(*) FROM evidence_cell_state"
  lift_when_ge: 1
```

This makes "restore the gate when research resumes" a thing the machine evaluates rather than a
sentence in a `note:` field, and reports the suppression **itself** as STALE the moment the first
row lands.

Rows 3, 4, 7, 8, 25 and the `--selftest`/`check()` ordering behind rows 10–18 are **not** in that
class. Their subject exists today and their absence is a genuine gap: `parts/v10/` has 15 files
right now, `site/populations/` has 23 populations to render right now, `weighting_profile` has 5
rows right now, and `register_integrity_check` has a 15-cell document sitting in `working/pilot/`
right now. Suppressing those would be mislabelling a gap as debt.

---

## Correction log — what the first pass said, and what replaced it

Recorded rather than absorbed, per AQ5.

| # | First pass said | Correction |
|---|---|---|
| 1 | The reasoning doc has **16** errors (4 header + 12 sections) | **15** (4 header + **11** sections) — the agonist's own enumeration listed 11; a `grep -c` counted the `[ERROR]` banner line |
| 2 | **12** stale pages assert determinations with VERIFIED sources | **11**. `f-07` asserts no determination; its entire 5-line diff is two lost `item_bpc_links` rows. This also resolves the open `[UNCERTAIN: f-07]` |
| 3 | `references/conflict-matrices/` holds **10** files | **13** (the "10" was borrowed from `matrix_consistency`'s unrelated `10/10 outcomes` line) |
| 4 | `site/index.html` is "the same mockup", "identical link inventory", "the same `href="#"` skeleton" | **Deleted.** Root has **95** `href="#"`, `site/index.html` has **10**; root's 91-provision directory is absent from it entirely. Materially different documents |
| 5 | `specs/e-08.html?mode=question` is "a dead link — a query string on a static file resolves to nothing" | **Deleted.** The mechanism is wrong: the query string is ignored and the page loads. The real finding is that `specs/e-08.html` has **no query-string handler** — the link works, the *mode* does nothing |
| 6 | `index.html` has "6 real internal links, of which 5 point at a single exemplar" | **7** internal links, **6** of them e-08 variants (the 7th is `index.html`) |
| 7 | `supersession_check` "has no audit at all — no script in `scripts/audit/` reads it" | **Deleted.** `grep -rn "supersession_check" scripts/audit/` returns **5 matches** in two files. The surviving point is narrower: `code_currency_audit.py` uses it as a *suppression predicate* and is quarantined, and nothing verifies the schema's own `'pending'`-on-closed-slug invariant |
| 8 | DEFECT-12-3: "a blocking gate that cannot fire, in code rather than in config" | **Reframed.** The exclusion is documented as deliberate in both the registry entry and the script comment. The honest finding is that a blocking check certifies nothing, its restoration is guarded only by an unevaluated prose note, and re-declaring `min_items` today *would* correctly turn it red |
| 9 | `register_integrity_check`'s R7–R15 rows: "3 advisory · Selftest FIRES" | The registered `cmd` is `--selftest`, which `sys.exit`s before `check()`. **At HEAD no document is evaluated.** Now stated on every affected (h) row and in (f) |
| 10 | `attestation_schema` is blocking ⇒ attestation validity is enforced | It is blocking **and diff-scoped**. Whole-corpus validity is established by **no registered check** |
| 11 | The missed COMPLETENESS mutation might be a logic bug or an empty subject | **Settled by experiment**: 15 rows + 17 synthetic sources → 12/12 fire, exit 0. Empty subject, no logic bug |
| 12 | Opus floor: "nothing short of [a workflow] is verification" | **Overstated.** A workflow proves the run, not the artefact, and is inert without the branch protection this repo lacks. The enforceable part is the **declaration**, via the existing attestation schema; the queue boundary is the cheapest real floor |
| 13 | DDL-enforced acceptance rows labelled "4 CI blocking" | **Systematically wrong**, and demoting to 1 or 2 is equally wrong. Introduced **level D**, noting the repo's 5-level spectrum has no rung for schema constraints; `CHECK`/`UNIQUE` = `D`, `FOREIGN KEY` = `D(fk)` with the deferred-differential caveats |
| 14 | Remedy for empty-subject checks: "add `min_items`" | Wrong where the subject is empty **by ratified decision** — it converts correct abstention into a permanently red gate. Rewritten as warranted self-lifting suppressions in the `known_debt.yaml` shape (`warrant` + `lift_when_sql` + `lift_when_ge`) |
| 15 | Diff-line counts "e-08 (28)" / "a-02 (22)" | Format artefact — `git diff --no-index` adds 5 header lines. Content account was correct; raw counts dropped from this document in favour of the classification table |

## Residual uncertainty

- `[UNCERTAIN: whether site/rooms/*.html were ever generated by the current room_page.py]` — they
  match its `r_*.html` underscore naming and its embedded CSS variable block, and were committed at
  `eafab6d` alongside the rest of `site/`. Neither pass reconstructed the schema at that commit to
  confirm a `room` table existed then.
- `[UNCERTAIN: the exact provenance of all 15 pre-reset evidence_cell_state rows]` — the reset
  migration's comment says 15 and the pilot HTML renders 15, but
  `working/pilot/data_20260712_pilot-cell-backfill.sql` inserts only 7 when replayed against the
  current schema. The other 8 came from a migration neither pass traced. This does not affect the
  settled experiment above, which reconstructed all 15 from the document's own attributes rather
  than from a migration.

---

## Part 3 — The agonist–antagonist protocol

### 3.1 Why this shape, for this repo

The recorded failure mode here is not carelessness. It is **plausible wrongness that survives
review** — a claim that reads correctly, passes its own check, and is false:

- a CI condition that could never evaluate true, so three jobs never ran on any PR in the
  repo's history;
- a blocking commit-message gate skipped rather than evaluated on every push to `main`;
- a scoping predicate that matched nothing for every session since it was added, reporting
  `Outstanding: 0` as success;
- a quarantine register in which **five of twenty stated reasons were factually wrong** on
  first audit;
- a workplan draft requiring a seventeen-item correction log;
- and, found today, a source comment asserting a `min_items` protection that its registry
  entry does not declare (§1.1).

Every one was caught by an adversarial pass run **separately from the pass that made the
claim**. None was caught by an author re-reading their own work. That is the case for this
protocol, and it is why its central rule is *separation*, not *rigour*.

### 3.2 The three roles

**AGONIST** — proposes. Attaches to every assertion (i) the command that produced it and
(ii) a **falsification condition**. An assertion with no falsification condition is not
reviewable and is rejected unread.

**ANTAGONIST** — refutes. Runs with **no access to the agonist's reasoning**, only to its
output and the repo. Default verdict is REFUTED; CONFIRMED requires personal reproduction.
Four verdicts, fixed: **CONFIRMED / REFUTED / OVERSTATED / UNVERIFIABLE**. Two would collapse
"partly true" into whichever pole the reviewer prefers — and OVERSTATED is where most real
findings land. In this document's own run: 28 confirmed, 1 refuted, 5 overstated, 3
unverifiable on the fix register alone.

**ADJUDICATOR** — resolves contested items by re-deriving from source, and may find both sides
wrong. Owner-gated items never reach adjudication; they surface as decisions.

### 3.3 Lens diversity is the load-bearing constraint

N identical antagonists converge on one blind spot. The 2026-08-09 review established this in
practice: three passes with *separate* lenses, and the methodology lens produced two findings
neither other lens reached. This document's run reproduced the effect — the factual lens
confirmed C1's symptom, and only the causal experiment (populating a scratch DB) distinguished
"empty subject" from "logic bug"; the method lens killed four proposals the factual lens had
confirmed as accurate. **Accurate and unwise are different verdicts, and one lens cannot
return both.**

| Lens | Asks | Catches |
|---|---|---|
| **Factual** | Is this reproducible right now? | stale numbers, phantom tables, misquoted schema |
| **Method** | If we did this, what breaks? | guardrail violations, mis-gated decisions, bad sequencing |
| **Vacuity** | Did this examine anything? | empty subjects, disarmed gates, tests asserting nothing |
| **Doctrine** | Does this contradict the mission? | umbrella coining, code-consensus over-claiming, unflagged ○ |

**The vacuity lens is not optional in this repo**, and after the reset it is the primary one.

### 3.4 Scaling rule — cost tracks irreversibility, not size

| Work | Agonists | Antagonists | Adjudication |
|---|---|---|---|
| Reversible, mechanical | 1 | 1 (factual) | no |
| Writes the DB, or promotes a check to blocking | 1 | 2 (factual + vacuity) | on contest |
| Doctrine, schema enum, taxonomy, retirement, file move | 1 | 3 | always |
| `best_practice_synthesis` | 1 Opus-class | 2, one doctrine | always |

### 3.5 This adds no new apparatus

CLAUDE.md §9 guardrail 3 forbids spinning up a new register. This protocol adds no table, no
file convention, no register. It **names roles for machinery already ratified**:

| Element | Existing home |
|---|---|
| Adversarial pass mandatory before "done" | `pipeline-contract.yaml` `cross_stage/definition-of-done`; `scripts/audit/claims_docket.py` |
| Per-rule FIRED / NOT-FIRED / SKIPPED | `[ADHERENCE-LOG — stage N]`; `scripts/audit/adherence_log_audit.py` |
| A counterclaim from someone who is not the author | `attestations/*.json` → `independent_reviewer_counterclaim` (≥30 chars, already required) |
| The author's declared slant | `attestations/*.json` → `bias_direction` (≥30 chars, already required) |
| Verdict vocabulary | `attestations/*.json` → `verdict` |
| Three-mode integrity check | `skills/integrity-protocol_SKILL.md` Mode 3 |
| Research definition-of-done | `scripts/audit/research_batch_dod.py` (R1–R15) |
| Vacuity floor | `min_items` + `EXAMINED: <n>` in `governance/check-registry.yaml` |

**The one genuinely new demand:** that the counterclaim be produced by a pass which never saw
the agonist's reasoning. Today nothing stops one author writing both sides, and a
self-authored counterclaim is the field most likely to be filled in with something agreeable.

### 3.6 The adversarial quality checks

Five, run against the **review**, not the work:

- **AQ1 · Subject check.** Every check invoked reports its examined count. A verdict resting on
  an empty-subject check is downgraded to UNVERIFIABLE. (This is `min_items` used as a review
  instrument rather than a gate.)
- **AQ2 · Mutation check.** Any invariant claimed as enforced must be shown firing on a
  deliberately broken input. `register_integrity_check --selftest` is the model — and its
  current `SILENT — MUTATION MISSED` output is the model *working*.
- **AQ3 · Refutation-rate check.** An antagonist returning zero REFUTED and zero OVERSTATED is
  re-run with a different lens. The base rate here is high; a clean sheet is evidence about the
  reviewer, not the work.
- **AQ4 · Re-derivation check.** Every number in the final document is re-derived from the live
  repo at write time, never copied from an input document (guardrail 1).
- **AQ5 · Correction log.** Corrections are recorded, not absorbed. §0.2 is this document's.

### 3.7 What this run taught about the method itself

**Reviewers are far better at detecting that something is wrong than at diagnosing why.**
Three times in this run, a pass reported a real defect with a false mechanism, and each time the
consequence survived adjudication while the explanation did not:

| Claim | Mechanism | Consequence |
|---|---|---|
| `register_integrity_check --selftest` never checks the document | **wrong** — it exits only if the selftest *fails* | **right** — today's failing selftest short-circuits it, and fixing C1 restores a working check |
| `check_rendered_docs` globs the wrong directory | **wrong** — the scope is set by DR-2026-07-25 | **right** — no *blocking* check covers generated output |
| FK constraints "fail outright" under `PRAGMA foreign_keys = OFF` | **wrong** — a differential check raises on new violations | **right** — the spectrum has no rung for DDL, so every acceptance row was mislabelled |

**The operational lesson: never accept a proposed mechanism without re-deriving it, even when
the finding is obviously correct.** A right conclusion with a wrong cause produces the wrong
fix — and in the first row above, the wrong cause would have sent someone rewriting `main()`'s
control flow rather than the eight lines that actually matter.

This is why the adjudicator role is not ceremonial, and why AQ4 (re-derive every number at write
time) should extend to re-deriving every *causal claim*, not just every count.

### 3.8 Failure modes of the protocol, stated up front

- **Antagonist theatre.** A reviewer rewarded for finding things will find things. AQ3 guards
  the empty case, not the inflated one; adjudication must be willing to reject an objection as
  manufactured, and record that it did.
- **Cost.** Three lenses on every commit would stop the project. Hence §3.4.
- **Shared blind spot.** Both roles reading the same wrong document agree. Mitigation: the
  antagonist is pointed at the repo and the artifact, never at the agonist's sources, and at
  least one lens must re-derive from the DB rather than from prose.
- **False confidence.** CONFIRMED means "reproduced today". It is not durable, and guardrail 1
  says re-verify against current files.
