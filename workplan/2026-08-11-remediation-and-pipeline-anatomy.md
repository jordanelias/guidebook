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
  nowhere to live with 0 `search_executions`. **It is currently unsatisfiable without
  fabricating a search.** Promoting `research_dod` to blocking (W6) would redden every diff
  for a reason no diff can fix. **Method:** R1 returns `NOTHING-IN-SCOPE` on an empty batch;
  the other fourteen already do, which is the inconsistency to remove.

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

*Sections 2.1–2.12 follow.*

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

### 3.7 Failure modes of the protocol, stated up front

- **Antagonist theatre.** A reviewer rewarded for finding things will find things. AQ3 guards
  the empty case, not the inflated one; adjudication must be willing to reject an objection as
  manufactured, and record that it did.
- **Cost.** Three lenses on every commit would stop the project. Hence §3.4.
- **Shared blind spot.** Both roles reading the same wrong document agree. Mitigation: the
  antagonist is pointed at the repo and the artifact, never at the agonist's sources, and at
  least one lens must re-derive from the DB rather than from prose.
- **False confidence.** CONFIRMED means "reproduced today". It is not durable, and guardrail 1
  says re-verify against current files.
