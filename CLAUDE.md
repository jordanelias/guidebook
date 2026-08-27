# CLAUDE.md — working guide for the Accessible Built Environments Guidebook

**Rewritten 2026-08-19** to comply with the mission of the preceding fortnight, after an audit
found this file was itself a recursion engine: it made apparatus **cheap to add and expensive to
remove**, taxed the project's real deliverable more heavily than its cheapest busywork, and
enforced by machine only the rule that blocked deletion. The three guardrails that would have
caught this repository's actual failures had **zero** enforcing code.

> **Read `decisions/DR-2026-08-19-research-restart-operative-instrument.md` first.** It is
> RATIFIED and operative: it carries the execution order, the runbook, and the acceptance
> criterion. It is meant to be **run**, not consulted. This file is the mechanical map — write
> path, gates, traps. Where they disagree, the instrument wins and this file is what to correct.

**The pipeline below is the frame everything else in this file reads against.** It is first
because rule 5 — never write the same fact into a second table — cannot be applied without it:
judging whether a column is a legitimate stage-specific fact or a copy requires knowing which
stage its table belongs to. Owner ruling 2026-08-25.

---

## THE PIPELINE — read this before anything else

**Owner ruling 2026-08-27**, superseding the five-stage list of 2026-08-25:

> **`research → evidence collection → judgment → synthesis → specification → render`**

In the owner's own formulation: *"you research slugs, evidence research, judge evidence, synthesize
judgments, specify syntheses, and render specifications."* **`specification` is a stage again, and it
comes AFTER synthesis** — which restores `governance/conceptual-model.md:90`'s own arrow (*"BPC
synthesis produces specifications"*), unchanged in the entity model since the baseline. The
2026-08-25 wording below is superseded and is not an argument against this; full record in
`references/project-standards.md`, 2026-08-27.

Rule 5 says each stage holds only its own data and anything earlier is reached by pointer. **That
is unusable without knowing which stage a table is in** — you cannot tell a legitimate
stage-specific fact from a copy. So the map is a stopper, not orientation.

**Substrate is not a stage.** The vocabularies and registries — `items`, `populations`, `slugs`,
`terms`, `access_needs`, the crossing maps, `decisions`, `data_migrations` — are the layer all six
stages point into. (`items` is retired as a table name by the 2026-08-27 `-item` ruling; the word was
the ambiguity.)

| Stage | Holds |
|---|---|
| **research** | What was searched, screened and mined, plus the clue store |
| **evidence collection** | What was admitted, its identity, verification and extraction |
| **judgment** | Whether an extraction is sound and how it weighs — grading, population matching |
| **synthesis** | What the judgments say together — weighing, convergence, cross-slug findings |
| **specification** | The determination: *therefore 1200 mm, marked ●*. Writes `specification_items` |
| **render** | Book surfaces — `site/`, `parts/`, `tools/*.html`, and the content tables behind them |

**Every stage's hand-off object is `<stage>_items`.** Owner ruling 2026-08-27. **The KEY SHAPES below
are not the owner's words and must not be quoted as such** — the owner ruled the naming and the
cardinality (*"one-to-many rows of judgment provide one row for syntheses"*); NOT NULL columns,
junctions and the fan-out/fan-in pivot are agent design derived from that cardinality, and the
evidence→judgment shape is **reopened**: the owner said *"each row of evidence provides one row for
judgment"* (1:1) and the first record of it said 1:N. Measured the same day: **not one foreign key in the schema lands on any
stage's hand-off object** — `source_locators` and `bpc_metadata` have zero inbound keys at all, and
`source_value_extractions` and `specifications` have one each, both same-stage. **Re-measured under
the six stages, 2026-08-27: 43 foreign keys cross a boundary and 37 stay inside one, landing on
eight columns** — `slugs.slug` 14 · `items.item_code` 10 · `evidence_sources.ref_id` 7 ·
`populations.population_code` 7 · `gaps.gap_id` 2 · `convergence_assessment.convergence_id` 1 ·
`reasoning_doc_citations.citation_id` 1 · `search_executions.exec_id` 1. *(The widely-quoted 41/39
on seven columns is the FIVE-stage figure and must not be repeated inside this frame.)* Not one of
them is a hand-off. **The walk itself has no keys**, which is why it does not walk. The rename creates
the spine; `judgment_items` is a NEW table, not a rename.

**Derive the table-to-stage assignment; do not read one out of a document.** Every bucket assignment
written before 2026-08-27 — including the 2026-08-25 derivation in
`scratchpad/session_2026-08-25-pipeline-smoke-test-mobility/STAGE-TABLE-MAP.md` — predates the
six-stage ruling and must be re-derived against these six stages before it is relied on again.

**A CROSS-STAGE VIEW *IS* THE POINTER, AND IS THEREFORE THE MOST PROTECTED OBJECT IN THE SCHEMA.**
Rule 5 says point, do not copy. **A view that joins two stages on the shared reference ID is what
"point" MEANS in SQL** — the owner's *"call up information from any one so long as you point to the
correct table and column"*, and *"for rendering a citation, we point towards the evidence table for
that reference ID"*, are descriptions of a join. **Re-measured 2026-08-27, and the count depends on a
convention this file had never stated.** Substrate is not a stage, so a view reading ONE stage plus
substrate crosses nothing. Under that convention — the one this file already uses — **FIVE views
cross a stage boundary**: `v_source_admission`, `v_item_provenance`, `v_source_reach_all`,
`v_code_floor_only`, `v_pending`. `v_coverage_priority` (research + substrate) and
`v_item_extractions` (evidence + substrate) do **not**, and a first pass this session wrongly counted
them, briefly putting "seven" in this file. `v_divergence` reads `specifications` and
`convergence_assessment`, which the six-stage ruling puts in *different* stages — so it crosses, and
the pre-2026-08-27 list was right about it for the wrong reason. **State the convention whenever
quoting this count.**

**Before deleting any view, ask which stages it spans.** A cross-stage view is not apparatus and is
not a candidate for a cull — deleting it removes the pointer and forces the next reader back to
copying, which is the defect the whole pointer-discipline series exists to remove. This is the
missing half of rule 5, and its absence is why `workplan/2026-08-22-master-execution-plan.md` R6
carried a standing order to delete eleven views, two of which are live pointers — one of them the
designated remedy for a violation still on the books, the other repaired at the cost of migration
064 the day before. **R6 is VOID; do not obey it.**

**Re-entrancy still holds and is a different question.** `governance/pipeline-map.yaml` established
2026-08-21 that a walk **re-enters** stages rather than passing through them once — a layer-3
artefact legitimately produces layer-2 rows. That answers *write order*. This map answers *what a
table may hold*. Both are true; do not use one to argue against the other.

**The machine enforces a FIVE-stage spine and has not caught up with the 2026-08-27 ruling.**
`governance/pipeline-contract.yaml`'s `stages:` list and `tools/pipeline_completeness.py`'s `STAGES`
both still read `research → evidence-collection → judgment → synthesis → render`, with no
`specification`. Until that lands, **the declared single home of the stage ids disagrees with this
file**, and this file is the one that changed. What the machine does enforce, under these names:
`governance/pipeline-contract.yaml` (the single home of the stage ids),
`tools/pipeline_completeness.py`, and the blocking `pipeline_completeness_fresh` gate. The id is
`evidence-collection`; its display form is **derived** by `stage_label()`, never stored beside it.

---

---

## 0. What will actually stop you

**Count the list.** Everything else in this file is orientation. *(A prose number stood here
twice and disagreed with the list both times — "Five" over six entries, then "Seven" over eight.
§2(b) forbids hand-written counts in derived documents, and this was one. There is no number now.)*

0. **A live owner statement supersedes every prior ratified record it touches, on contact.** Your
   job on hearing one is to **record the supersession, never to weigh the ruling against the
   paperwork it changes.** A DR, a RULE, an ADOPTED directive — these are what a ruling *changes*.
   They are never an argument against it, and citing one back at the owner is not diligence.
   **This rule is numbered 0 because the rest of this file tilts the other way** — §1 says *"a
   specific, ratified authorisation beats a blanket caution"*, `project-standards.md` says merge
   ratifies with the force of an explicit directive, and DR-2026-08-19 says *"validity in this
   repository flows from ratification"*. All true **between records**. None of them reaches the
   owner.
   *Added 2026-08-24 after an audit found **nine instances** since 2026-07-13 of paperwork being
   argued against a live directive. The worst: on 2026-08-18 the owner ruled `axes` a bad coined
   term and said use ICF codes directly, marked "do not relitigate" — and the **next day** a batch
   pulled the frame as bare `axis_code`, framing four of five searches on one mechanism and hiding
   a second. That one changed research output. In the same class, an agent invented an owner
   directive that was never given and built a 531-row table on it.*

1. **Commit format.** `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last.
   `date -u '+%Y-%m-%d %H:%M'`. Use `governance` when no project skill fits.
2. **Attestation on synthesis paths.** Touching `references/bpc-reasoning/`,
   `references/connection-reasoning/`, `decisions/` or `sessions/` needs
   `attestations/<slug>.json` against `schemas/attestation.schema.json`.
3. **Never write `data/guidebook.db` directly.** Migrations only, via
   `scripts/emit_data_migration.py` → `scripts/migrate_db.py`. Append-only and immutable once
   committed: fix forward with a compensating migration. CI rebuilds and compares.
4b. **Never report an owner ruling absent from a search that could not have seen it.** `.ignore`
   hides `sessions/**` from ripgrep and the Grep tool, and **owner rulings live overwhelmingly in
   `sessions/`**. `grep -r` and `git grep` ignore `.ignore` and find them instantly. On 2026-08-24 I
   twice told the owner a ruling of theirs did not exist in this repository; it was in `CLAUDE.md`
   §6 and in a session record, and §7 trap 1 warns of exactly this. **A ruling can be in the
   repository, in a file the traps name, and still fail to bind — if the search is worse than the
   record.**

4. **A rename or removal is not done until the callers are swept.** Search every non-archived
   caller and fix each one. A sweep that stops at the filename is not a sweep — that exact
   shortcut left two dangling paths inside an attestation on 2026-08-19. **A VIEW IS A CALLER**, and so is a
   skill: migration 064 exists because 063 swept eight Python readers and six skills and missed
   `v_item_provenance`. Grep `sqlite_master` as well as the tree, and **treat a 0-row object as
   unproven, not clean** — `specifications` holds 0 rows, so that view rendered nothing, so a
   byte-exact diff of every regenerated output proved it clean while it was broken.

5. **Never write the same fact into a second table. Point, do not copy.** Owner ruling 2026-08-24
   (`DR-2026-08-24` §2.1, now in `references/project-standards.md`): *"It is better to have a table
   cell point to another table cell than to rewrite."* Each stage — research → evidence → synthesis
   → specification → render — holds only its own data; anything earlier is reached by pointer on the
   shared reference ID. **A parity check is not a fix** — it makes a dual home survivable, therefore
   permanent. And **a column a committed data migration INSERTs can never be dropped**: grep
   `scripts/migrations/data_*` for the name first, then writer-retire, reader-retire, NULL forward.

6. **Commit the scratchpad at every natural break, not at session end.** Owner directive 2026-08-25.
   A scratchpad that lives only in context is not a review surface; compaction, session end and
   container reclamation all take it. This repository paid for that twice in two days — the
   pointer-discipline queue existed only in a conversation while three of its items shipped citing
   labels no file defined. If no session directory exists, create it and commit into it rather than
   waiting for a session record. `governance: session command log [YYYY-MM-DD HH:MM]` is a complete
   commit message.

**The doctrine token is gone.** OD-10 was signed 2026-08-19 and the instrument's §10 item 4 is
executed: the `[DOCTRINE: <sha>]` commit token, its CI step, its enforcing script, the frozen
recheck counter and the "any doctrinal revision" recheck trigger are all removed. It never caught
any of the three failures in §2, and its own gate was push-only — skipped on every PR, with merge
commits exempt — so on the path the workflow actually uses it was never more than convention.

Rule 2 is a **tax on the deliverable**, inverted against rule-free `workplan/` files which cost
nothing at all. It is kept because attestations have caught real deviations — in their free text,
which no gate reads for meaning. It is the next candidate if the ceremony is cut further.

The commit-message format check remains, and is still `if: github.event_name == 'push'`.

---

## 1. Symmetry: deleting is as cheap as adding

**This replaces the old "owner-gate file moves and retirements" guardrail, which was the
pathology.** Adding a check cost a commit; removing one cost an owner decision. A system with
that gradient can only accrete, and it did. **Derive both live figures; do not read a number here.**
This file's own §2(b) forbids hardcoded counts in derived documents, and the "sixty-odd registered
checks and ~35k executable LOC" that stood here until 2026-08-22 was stale from the moment the
2026-08-20 cull removed 6,716 of those lines:

```
python3 -c "import yaml;d=yaml.safe_load(open('governance/check-registry.yaml'));print(len(d['checks']),'checks;',len(d['quarantine']),'quarantined')"
find scripts tools -type f \( -name '*.py' -o -name '*.sh' \) -not -path '*/__pycache__/*' -print0 | xargs -0 cat | wc -l
```

The shape that matters is not the total but the ratio: **most of the executable surface polices the
repository rather than producing the book**, and the cull removed dead weight from both sides without
changing that ratio.

- **Code, checks, scripts, dead tables and views: delete them.** No owner gate. You need
  *evidence* — that it is unreferenced, or vacuous after a real batch, or superseded — not
  permission. Record the evidence in the commit.
- **Git history is the archive for CODE.** Do not copy scripts or checks to `_archived/` to
  "preserve" them; git already did — delete them. **Owner ruling 2026-08-19: `_archived/` IS
  allowed to grow**, and is the right home for retired *content* — superseded plans, prose and
  records a reader may want to find without a git archaeology session. The distinction is
  reader-facing content versus executable surface, not preservation.
- **Owner sign-off is still required for content and doctrine**: mission, audience, CRPD
  posture, population taxonomy, evidence-tier definitions, jurisdiction and work-product
  inclusion, licensing, trajectory (the DG-NON class in `governance/decision-protocol.md`).
  Those are judgements about the book. Code is not.
- **Adding apparatus carries the burden of proof**, not removing it. Before adding a check,
  script or table, state what wrong thing reaches the *guidebook* if it does not exist. If the
  answer is about the apparatus rather than the book, do not add it.
- **Nothing is added without naming what reads it.** This is the mirror of rule §0.4, which taxes
  removal only. An unread field, an uncalled script and an unregistered check are the same defect.
- **A specific, ratified authorisation beats a blanket caution.** On 2026-08-19 a session left 521
  lines of dead code in place, citing a six-word guardrail, when the code's own docstring and
  registry note already authorised its retirement. Blanket removal-friction winning ties against
  specific removal-permission is exactly how this file became a ratchet.

---

## 2. The three failure modes that are real

Derived from what has actually gone wrong here, not from what might.

**(a) A gate that passes having examined nothing.** Produced four separate times. Every check
must print `EXAMINED: <n>`; `scripts/run_checks.py` reports zero-subject passes as
NOTHING-IN-SCOPE and escalates blocking-and-vacuous ones. **When a check passes, confirm it had a
subject.** A blocking check whose session pointer is missing FAILs rather than SKIPs, deliberately.

**(b) Prose that contradicts the database.** *Rule: no hand-written counts in derived documents.
Generate them from the DB, or stamp the document with its generation date and a drift warning.* Counts in this file, in `index.html`, in manifests
and in audits have all drifted. **Derive every volatile fact — row counts, schema version, CI
status, the doctrine SHA, the active plan — from the live repo.** This file hardcodes as few as it
can, and the pipeline section above now carries three (43/37 cross-stage keys on eight columns; five
cross-stage views) because a wrong figure in each was being quoted onward. **Each is stamped
2026-08-27 and each is a re-derivation command away** — treat them as dated, not as current.
On 2026-08-19 a rendered search log claimed "three cells are EXACT" while the DB said two, made
stale within the hour by the same session's own correction.

**(c) A fabricated citation passing green gates.** On 2026-08-19 all five sources in the first
research batch were stored with **invented co-authors** — including the deletion of autistic
community co-authors from a Co-1 paper whose Co-1 warrant *is* their co-authorship. Six gates
passed it, because each asked whether the author fields were *populated*, never whether they were
*true*, while `verified_by_tool='crossref'` asserted the very property that had failed.

The fix, and the general principle: **verification must leave an artefact.**
`scripts/research/retrieval_log.py` persists every retrieved payload under `retrieval-log/`, and
`--verify-authors` diffs stored data against the bytes actually received — offline, no network,
no drift. Storage is cheap; the log is read only when auditing fidelity, which is exactly when it
is irreplaceable. **Never write a bibliographic field from memory when a payload is in hand.**

---

## 3. What this project is

A reference on architecture, accessibility and built-environment standards centred on **disabled
people**. Fixed doctrine: a **thinking tool and advocacy project, not an authority** — "the
purpose of this guidebook is to get people to ask the right questions." Not a prescription
manual, not a legal authority, not a substitute for professional judgment. "Inclusive /
accessible / universal" here always means *inclusion of persons with disabilities*.

Pre-launch, single author (`@jordanelias`). The governance and tooling are elaborate; **the
content is barely started**. Query the DB for the real state.

---

## 4. The data layer

`data/guidebook.db`, SQLite, committed as a binary blob. `PRAGMA user_version` is the schema
version. **There is no `sqlite3` CLI** — use Python, read-only:

```python
import sqlite3
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
```

**Backbone.** `items` (design parameters) × `populations` meet in `specifications`, the
per-(item × population) synthesis record. Evidence lives in `evidence_sources` and attaches via
`source_slug_links`, `evidence_population_match`, `search_admissions`. `source_locators` is a
**lead index of identifiers, not evidence** (`SELECT COUNT(*) FROM source_locators`) — the R9 duplicate gate currently cannot see it,
which is a known live defect (OD-5).

**Changing it.** Schema → new `scripts/migrations/NNN_slug.sql`, bump `user_version`, mirror the
Pydantic model. Data → `emit_data_migration.py --input` then `migrate_db.py`. Verify with
`migrate_db.py --rebuild /tmp/rebuilt.db`. `057_baseline_2026-08-12.sql` is the baseline.

**Research writes go to a scratch copy first.** `cp data/guidebook.db $SCRATCH`, point
`GUIDEBOOK_DB_PATH` at it inline on every call (the harness resets env between shells), then
capture the delta with `scripts/research/emit_batch_sql.py` and ship it as a migration. Every
write-time refusal stays live and the canonical DB's sha256 must not move until the migration is
applied.

**THE WRITE PATH IS ONE SENTENCE, and as of 2026-08-25 there is no longer a second one:**
scratch copy → `scripts/db.py` subcommands → `scripts/research/emit_batch_sql.py` →
`scripts/emit_data_migration.py` → `scripts/migrate_db.py`.

*This paragraph used to end differently. It read: `db.py` has no subcommand for
`search_candidates`, `evidence_population_match`, `economics_entries`, `case_studies` or
`jurisdictional_values`, and `add-source` cannot write `doi_resolution_outcome`, `url` or
`pages` — so **"those need hand-written SQL against the scratch, and that gap is where the
fabrication of 2026-08-19 entered."** The gap was the CAUSE, not the setting, and it is closed:
every one of those tables and columns now has a writer that REFUSES (FK existence, the column's
own CHECK vocabulary, R3 locators, MISMATCH reasons, duplicate identities). Do not hand-write SQL
against a table the CLI can reach; if you find one it cannot, that is a coverage bug to fix, not a
licence to bypass.*

**`db.py` refuses, and that is its whole value.** A writer that merely INSERTs is worse than hand
SQL because it looks safe. Two refusals are deliberately *absent* and must stay absent:
`add-population-match` does **not** enforce uniqueness on (ref_id, population) — a dissenting
adversarial grade lands as a second row (`DR-2026-08-19` §7) and divergent grades read as a
contest — and `add-source` exposes no `--year`/`--journal` for an entry that carries a `ref_id`,
because those are reached through the pointer.

**Vocabularies come from the schema, not from a list in the code.** `dbcore.check_values()` reads
the column's own CHECK. Live rows are a *sample* of a vocabulary, never the vocabulary:
`search_candidates.disposition` declares `OUT-OF-SCOPE` and no live row uses it, so a
refusal built from live rows would reject a legitimate value. **There is no ref_id allocator, and the rule this file gave for weeks was WRONG.** It said mint
above the `source_locators` high-water mark. Measured 2026-08-25: `source_locators` tops out at
**REF-00964** and `evidence_sources` at **REF-00970**, so that rule yields REF-00965 — a live
evidence row. **The high-water mark is the UNION of every table holding a ref_id.** Do not compute
it by hand: `dbcore.next_ref_id(conn)` IS that rule, computed and never stored — a counter table
would be a second home for a fact those columns already jointly state (rule 5).

---

## 5. Running checks

```
bash .claude/hooks/ensure-deps.sh    # pydantic + jsonschema. DO THIS FIRST. See below
scripts/preflight.sh                                    # gate your diff vs origin/main
python3 scripts/run_checks.py --changed-from origin/main --explain
python3 scripts/run_checks.py --list                    # registry + quarantine
python3 scripts/run_checks.py --selftest               # RUN THIS AFTER ANY RENAME. See below
```

> ### **`pydantic` IS NOT INSTALLED IN A FRESH CONTAINER, AND WITHOUT IT THE REPOSITORY LOOKS BROKEN**
>
> `.claude/hooks/ensure-deps.sh` now installs it at `SessionStart`, but it exits 0 on failure by
> design — offline, or with no pip, you are on your own. **Check before you believe any red result.**
> Measured on `origin/main` at `d6ef7e9`, 2026-08-25:
>
> | | Blocking failures | Advisory | Result |
> |---|---|---|---|
> | without `pydantic` | **5** | 10 | **FAIL** |
> | with `pydantic` | **0** | 4 | **PASS**, 50 green |
>
> The five are `validate_schema`, `validate_evidence_state`, `audit_adversarial_use`,
> `decision_capture`, `doctrine_recheck` — **the entire governance battery**, which
> `check-registry.yaml` already declares `deps: [pydantic]`.
>
> **This is the one place §5's advice below inverts, so read it twice.** "Reproduce it locally
> before assuming a red check is yours" normally protects you. Here the reproduction *succeeds* —
> on untouched `main` — and a session that skips the dependency check can spend a day fixing
> governance failures it did not cause and cannot fix.
>
> **Never `pip install -r requirements.txt` in this container.** It pins `PyYAML==6.0.3`; pip
> refuses to uninstall the Debian-managed `PyYAML 6.0.1` that is present and working
> (*"Cannot uninstall PyYAML 6.0.1, RECORD file not found"*), the whole install aborts, and
> nothing lands. Install the individual packages.
>
> **The dependency list has ONE home: `governance/check-registry.yaml`'s `batteries:` block.**
> `requirements.txt` is a second home and it already disagreed — it names `pydantic` and
> `PyYAML` and omits **`jsonschema`**, which the registry declares for the `research` battery and
> which attestation validation needs. Found 2026-08-25 by an attestation validating only after a
> hand install. `ensure-deps.sh` now reads the registry rather than carrying a copy (rule 5).
>
> **`--changed-from` DOES NOT RUN THE SELFTEST, AND THE SELFTEST IS WHERE A RENAME FAILS.**
CI's *Classify change* job runs `--selftest`; `--changed-from origin/main` does not. On 2026-08-25
I renamed a pipeline stage id, swept `scripts/`, `tools/` and `schemas/`, got a green
`--changed-from`, pushed, and CI failed on `C7 every contract basis resolves to a real criterion`:
`governance/check-registry.yaml` encodes stage-qualified `basis: <stage>/<criterion>` references,
and one still named the old stage. **The registry is a caller.** After any rename, run
`--selftest` as well, and grep the registry for the old name.

**If you add a `SessionStart` hook, APPEND it — never insert at index 0.**
> `scripts/generate/research_contract_hook.py` reads
> `SessionStart[0]["hooks"][0]["command"]` **by hardcoded index** and compares it to
> `governance/research-contract.yaml`. Inserting ahead of the contract turns the blocking
> `research_contract_sync` check red with a diff that reads as contract drift and is not.
> Cost me a cycle on 2026-08-25.

`governance/check-registry.yaml` is the single inventory; `run_checks.py` is the only thing that
invokes a check; CI and preflight both call it. Adding a check means editing the registry —
never a workflow — and now carries the burden of proof in §1.

CI is four workflows (`ci.yml` gates `main`; three scheduled). **Before assuming a red check is
yours, read the run and reproduce it locally** — this file deliberately does not record which
gates are currently red, because that claim went stale twice and was still being cited after the
backlog it described had cleared.

---

## 6. Evidence model, briefly

`governance/tier-system.md` is operative. **T1** primary controlled research · **Co-1** lived
experience / participatory design, **co-primary with T1** under CRPD Art 4.3 · **T2** synthesis ·
**Co-2** OT professional-body CPGs · **T3** grey primary · **T4–T6** the regulatory stratum,
walled off from full-strength anchoring.

Markers: **●** confirmed · **◐** policy/standards only · **○** grey/thin. Unmarked is an error.
Cell states: `stated` / `provisional` / `pending` / `not_applicable`.

**Co-1's warrant is co-production.** When you cite lived-experience work, the disabled people who
produced it are part of the evidence, not metadata. Erasing them while claiming the tier is the
worst failure available here.

**Synthesis routing:** only Opus-class models write `best_practice_synthesis`. **Citation
discipline:** confirmed real sources only — "I don't know" beats invention; quantified claims need
a locator or `[UNVERIFIED-QUANT]`.

Work from the **ICF/access-need frame with codes AND names**, never from bare axis codes and never
from population umbrellas. On 2026-08-19 a frame pulled as bare `axis_code` hid that a slug spanned
two demand mechanisms, and four of five searches were framed on one of them.

**The frame is the FULL CROSS-PRODUCT, and applicability is an OUTPUT of synthesis, not an input.**
Owner ruling 2026-08-24 (`DR-2026-08-24` §2.4): *"Every research slug gets cross-referenced against a
population code, access need or ICF code because there is always the chance that there is an
unexpected connection between them… we are waiting until we have finished our syntheses to ensure we
define them with evidenced justification, not presuppositions."* So the question is never *"which
populations does this slug already link to"* — that presupposes the answer. **Zero
`item_population_links` on a slug is the correct pre-synthesis state, not a defect**, and D-0165 does
not block research: it is downstream of it.

---

## 7. Traps

- **`.ignore` hides frozen records from ripgrep** — `_archived/`, `audits/`, `sessions/`,
  `references/search-log/`, `versions/`, `workplan/_superseded/`. "No matches" ≠ absent: confirm
  with `ls` or Glob. `grep -r` and `git grep` ignore it; Python tools see everything. Search those
  paths explicitly when doing history work. **Note the cost:** rendered search logs live under an
  ignored path, so the project's own research output is invisible to search.
- **Two session pointers, and NEITHER ONE NAMES THE SESSION YOU ARE IN.** `sessions/LATEST` is
  continuity; `sessions/LATEST-RESEARCH` is the subject of the blocking citation-mining gate.
  Update `LATEST` on any session close; update `LATEST-RESEARCH` only when the session actually
  did research. **Because both move at CLOSE, both name the PREVIOUS session for the whole life
  of the current one** — so anything that needs "the session running now" must DERIVE it, never
  read a pointer. Measured 2026-08-25: `record-command.py` read `LATEST` and filed three
  sessions' Bash logs into one file named after the earliest (5 lines + 405 + 274), while the two
  later sessions' scratchpad directories held no log at all. That was itself a *fix*, applied
  2026-08-23, for the identical failure under `.claude/session` — swapping one close-out pointer
  for another changed which stale name was written, not that it was stale. The derivation that
  works needs no new pointer: **a session is closed exactly when `sessions/<stem>.md` exists**, so
  a `scratchpad/session_*` directory with no record behind it is open.
- **Session ids: bare stem in the DB, `.md` in pointers and `emit_data_migration --session`.**
  Getting it wrong scopes a gate to nothing and it passes green.
- **Don't hand-edit generated output** (`parts/`, `site/`, `audits/`, `tools/*.html`) — regenerate
  with `scripts/regenerate_derived.sh`. A DB change makes them stale and two blocking checks red.
- **`schemas/*.py` ↔ SQLite drift is a bug**, not a convention.
- **PI versioning is intentional** — highest-numbered `governance/project-instructions-v*.md` is
  live, and it legitimately lags doctrine. Prefer `references/project-standards.md` and recent DRs.
- **Don't run `scripts/bootstrap.sh`** — PAT-gated, for the claude.ai surface.

---

## 8. Where to read for depth

| Question | Read |
|---|---|
| What to do now | `decisions/DR-2026-08-19-research-restart-operative-instrument.md` |
| Doctrine | `governance/mission-and-epistemics.md` |
| Current operative rules | `references/project-standards.md` |
| Tiers, markers, weighting | `governance/tier-system.md`, `governance/evidence-architecture.md` |
| Entity model, ICF frame | `governance/conceptual-model.md`, `governance/functional-taxonomy.md` |
| Decision process | `governance/decision-protocol.md` + recent `decisions/DR-*` |
| Architecture | `architecture/project-architecture-guidebook-v2.3.md` |

*Volatile facts are deliberately absent above. Derive them from the repo.*
