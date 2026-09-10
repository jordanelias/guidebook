# What is inert — strand 1 of 3: the check registry

Not "what might break if I change something" but "what is already dead, and how would
anyone know". Every line below was produced by running the check, not by reading it.

## The finding

**The 2026-08-06 corpus reset and the 2026-09-01 item-layer deletion were swept through
the check registry only PARTLY.** Six checks were correctly retired to `no_floor` on
2026-09-01 with a reason recorded in the registry itself. Four more were missed, and are
now permanently red or permanently vacuous against a corpus that no longer exists. That
permanent red is the thing CLAUDE.md rule 6 warns about — *a check that is red by
construction teaches its reader to ignore it* — and it is currently training its reader
across the whole battery, not just those four.

## Vacuous by design — NOT a problem, and the registry already says so

The `NOTHING-IN-SCOPE (10)` headline oversells the trouble. Nine of the ten carry a
recorded reason and are behaving correctly:

| Class | Checks | Why 0 is right |
|---|---|---|
| `empty-by-decision` | `validate_schema`, `validate_evidence_state`, `validate_verification_consistency`, `population_integrity_audit`, `pmp_audit`, `reasoning_doc_citations_audit` | corpus emptied deliberately; they fire again when the book has content |
| `changeset-scoped` | `attestation_presence`, `attestation_schema`, `attestation_verdict` | they examine HEAD~1..HEAD, not the 79 attestations on disk. 0 means *this commit owed none*. A floor would fail every non-synthesis commit |

The three attestation checks should arguably not appear in that headline at all: they
are working exactly as designed, and listing them beside genuinely dead gates is what
makes the list easy to skim past.

## Genuinely inert or miscalibrated — four

| Check | Level | State | Why |
|---|---|---|---|
| `validate_items` | advisory | **RED, floor 1, EXAMINED 0** | Floor never retired when `items` was emptied, unlike its six siblings. Worse: its declared `basis` is `base/base-parameter-vocabulary`, and after migration 071 that vocabulary is `base_parameters` — a table that exists and *can* be checked. The check is pointed at the deleted layer while its stated authority points at the live one. |
| `site_pages_fresh` | advisory | **RED, floor 1, EXAMINED 0** | Same class: `site/` holds no pages, floor never retired. |
| `test_verification_pipeline` | advisory | **RED, 3 of 18** | G01 wants language on ≥50 sources (live: 0). G02 wants ORCID on ≥30 authors (0). G03 wants COMPLETE ≥100 (8). All three are **pre-reset thresholds asserted against a post-reset corpus** — they were calibrated when the old corpus existed and were never recalibrated. |
| `check_rendered_docs` | **blocking** | NOTHING-IN-SCOPE | `examines-none-by-policy`: `specs/` holds one brief, `--all` deliberately declines to check it because it cites REF-ids the reset removed. And it would RAISE if it ran — its SQL selects `specifications.item_code`, dropped by 071 — and it derives its DB key from a *filename*, `specs/e-08-brief.html` → `E-08`. A blocking gate keyed on the contamination example CLAUDE.md §7 names. |

## Red with REAL findings — three, and these are work, not calibration

| Check | Finding |
|---|---|
| `retired_vocabulary` | Retired terms still taught by the reading surface: `applicable_groups` (1), `UNVERIFIED-1` (12), `VERIFIED-WITH-CORRECTION` (36) — overwhelmingly in `references/bpc/`. Couples directly to the unresolved archive question: moving `references/bpc/` would clear most of these and strand two other blocking gates. |
| `metadata_integrity_audit` | 8 COMPLETE/COMPLETE-STATUTORY rows carrying an open integrity flag. EXAMINED 9, so this one has a real subject and a real verdict. |
| `validate_reasoning` | `references/bpc-reasoning/room-acoustic-performance.md` is missing three required header fields (**BPC file**, **BPC population**, **Generated**). Small and fixable. |

## Red by construction — one

`validate_pydantic_schemas` reports 243 drift findings and is explicitly *"a REPORTING
tool, not a gate ... Exit code is always 0 unless run with --strict"*. It is red every
run and always will be until a per-model accept/reject policy exists, which its own
docstring defers as separate work. It is the single loudest contributor to the battery's
background noise.

---

# Strand 2 — inert executable surface (91 scripts swept)

## The one the sweep got WRONG, and why it matters for the deletion rule

`scripts/research/emit_batch_sql.py` came back INERT. It is not. **CLAUDE.md:163 names it
as a step in THE WRITE PATH**, `governance/context-map.yaml:612` lists it, and **seven
attestations record sessions actually using it** — *"Every row reached the canonical DB
through the sanctioned path... captured by emit_batch_sql.py"*
(`attestations/sessions_session_2026-09-02-research-batch-05-circulation-icf.json:16`).
Deleting it would remove the capture step from the write path.

The sweep's criteria were registry / CI / hooks / Python importers / skills /
context-map. **None of those cover "a human or agent follows CLAUDE.md."** So any script
whose only caller is the documented procedure reads as inert.

**This is a required guard on the deletion rule.** "Nothing invokes it" must mean
*including no prose procedure in CLAUDE.md, a skill, or an attested session*, or the rule
deletes the write path. The narrower true finding here: no *skill* names
`emit_batch_sql.py`, so an agent working from a skill rather than CLAUDE.md skips the
capture step — which is how a table gets written and not captured.

## Genuinely inert — nine, none load-bearing

Confirmed: none of the nine is named as a step in CLAUDE.md, a skill, a hook or a
governance document. None defines anything a live file imports.

| file | status |
|---|---|
| `scripts/audit/rename_insurance.py` | nothing invokes it, no mention anywhere |
| `scripts/generate_parts.py` | nothing invokes it, no mention anywhere |
| `scripts/generate/population_page.py` | `build_site.py:6-11` says it *"has never had a driver"*; appears in `governance/retired-vocabulary.yaml` |
| `scripts/generate/room_page.py` | `build_site.py:7` says it *"does NOT drive"* it and that it *"crashes against the live schema"* — see the exemption note below |
| `scripts/tests/test_adjudication_integrity.py` | the registry's own quarantine note (`check-registry.yaml:1492`) records that a prior cull spared code on the false premise this was a live check — *"It is not, and never was"* |
| `scripts/audit/graph/__init__.py` | siblings load via `sys.path.insert` + bare import; the package is never imported as one |
| `scripts/audit/adjudication_integrity.py` | **quarantined** |
| `scripts/audit/code_currency_audit.py` | **quarantined** |
| `scripts/audit/pre_rehab_banner_audit.py` | **quarantined** |

**Quarantine is real, and verified**: `run_checks.py` selftest C5 asserts *"quarantined
checks are unreachable by --all"*, and the runner prints `(N quarantined, never selected)`.
So "registered" and "runs" are different things, and three of the nine are registered but
provably unreachable — a category worth naming rather than trusting the YAML's presence.

## Where broken things are parked — and it is NOT hiding

`governance/schema-reference-exemptions.yaml` holds nine exemptions, and reading it
changes the shape of the deletion question. Its entries are honest and self-dating:

- **`room` and three siblings** — `room_page.py` queries *"four tables that have never
  existed in this schema"*. Exempted, not fixed, *"because fixing it means deciding what
  the room stratum IS, which is content doctrine (DG-NON), not a sweep"* — recorded
  2026-08-02 as disposal item flag 3, **awaiting owner decision 8**.
- **`specification`** — the phantom table, and it records that
  `skills/question-author_SKILL.md`'s *"entire write path has never been runnable"* and
  that `question_heading` exists in **no table in the schema**.

So a material share of the repo's broken paths are **not sweep misses awaiting a fix —
they are parked awaiting an owner decision that has been open since 2026-08-02.** A
non-compliance rule that deletes on brokenness alone would delete work that is waiting on
the owner, and would discard the record of what it is waiting for.

---

# Strand 3 — SQL that raises (976 candidate hits, executed not inferred)

## The finding that explains the whole problem

**`scripts/audit/check_rendered_docs.py` raises in the mode a human runs it, and passes
green in the mode CI runs it.**

- Run bare, or with `--doc specs/e-08-brief.html`: `OperationalError: no such column:
  item_code` at `:95-97`, and independently at `:201-203` and `:218-219`. Migration 071
  dropped the column.
- Run `--all`, which is the registered CI form: short-circuits to `EXAMINED: 0` **by
  policy, before opening the database**. Exit 0.

It is a **blocking** gate. So the one invocation that would have caught its own breakage
is the one CI never makes. This is failure mode (a) — a gate that passes having examined
nothing — with the additional property that the vacuity is what conceals the fault.

## A. RAISES — verified by execution

| file:line | error | cause |
|---|---|---|
| `check_rendered_docs.py:95-97, 201-203, 218-219` | `no such column: item_code` | 071 |
| `generate/population_page.py:75-80` | `no such column: item_code` | 071 — `populations` has 23 rows, so any invocation reaches it |
| `generate/pilot_renderings.py:234-237` | `no such column: item_code` | 071 — fails at SQL-compile time, so it raises **regardless of row count** |
| `generate/room_page.py` (8 sites) | `no such table: room` | **NOT 071.** Pre-existing and owner-gated: flagged 2026-08-02, before the live `rooms`/`room_items` tables existed at all |

## B. DORMANT — valid SQL the loop never reaches

`generate/spec_page.py:73-79` and `generate/build_site.py:96-100` both name the dropped
columns and would raise identically, but both are driven by `SELECT ... FROM items`, and
`items` has 0 rows, so neither is reached. Broken and unreachable are different states and
only one of them is urgent.

Everything else that reads now-empty tables was executed and **none raises** — the columns
still exist, the tables are simply at 0 rows, which is an empty result, not an error.
`register_integrity_check.py` and `validate_verification_consistency.py` were already
swept post-071 and pass. All 18 views execute (072's repair holds).
`PRAGMA foreign_key_check`: **0 violations** — the corruption CLAUDE.md describes is
entirely prospective, never present in the committed blob.

## C. UNWRITABLE TABLES — twenty-one, not two

CLAUDE.md §4 names `specifications` and `item_taxonomy_links` as examples and says to
derive the live set. Derived, it is **21 tables** whose NOT NULL foreign key points into an
empty parent:

- into **`items`** (11): `item_taxonomy_links`, `item_bpc_links`, `item_audit_runs`,
  `item_population_elaborations`, `jurisdictional_values`, `spec_value_probes`,
  `term_item_links`, `room_items`, `case_study_specs`, `economics_entry_specs`
- into **`base_parameters`**: `specifications`
- into **`specifications`**: `specification_source_links`
- into **`case_studies`** (3): outcomes, populations, strategies
- into **`economics_entries`** (2), **`connections`**, **`reasoning_doc_citations`**,
  **`spec_value_probes`**, **`source_value_extractions`**

`conflicts.item_code` is correctly ABSENT: it is nullable, so `conflicts` stays writable
with `item_code = NULL`.

**The one that matters right now:** `specifications.parameter_id → base_parameters`, and
`base_parameters` holds **0 rows in the canonical DB**. `db.py add-parameter` now exists
and a determination was proven writable — but on a *scratch* copy. Until a parameter is
minted into the canonical DB through the migration path, `specifications` remains
unwritable there. The tool exists; the row does not.

---

# CORRECTION — applying the layer model changes the answer

Owner ruling (2026-09-10): *deciding at Layer 2 isn't allowed, and owner-gated stuff
stays.* Applying that, plus §3's layer model, to the inert list above: **"nine genuinely
inert" was wrong.** The honest number is at most two, and the real findings are different.

## The method error, twice

**Layer 0 tools are invoked by a human following a procedure, not by CI.** An inertness
test built on registry / CI / hooks / Python imports is structurally blind to exactly the
apparatus Layer 0 is made of. It flagged:

- `scripts/research/emit_batch_sql.py` — the capture step of THE WRITE PATH (CLAUDE.md:163)
- `scripts/audit/rename_insurance.py` — **"prove a table rename changed NAMES ONLY"**, whose
  docstring cites rule 4, the rule that exists because migration 063 swept fourteen callers
  and missed `v_item_provenance`.

Both work. `rename_insurance.py --snapshot` runs clean: EXAMINED 70 tables, 18 views, 90
foreign keys. **Nothing invokes it because you invoke it when you do a rename — and
migration 071 was a re-key, and it was not run.** That is not a dead tool. That is a Layer
0 tool that was available and unused during the exact operation it exists for.

**So the layer must be an INPUT to the inertness test**, not a conclusion drawn after it.

## Quarantine is not death — the registry says so itself

All three quarantined scripts stay. Their own entries say why:

| script | what the registry records |
|---|---|
| `code_currency_audit.py` | quarantine says *"a content backlog, not a gate"* — but `governance/tier-system.md:55` names it as **the mechanical enforcement** of a doctrine rule, *"promoted from text rule (Level 1) to audit script (Level 2)"*. tier-system.md is **operative** (CLAUDE.md §6). Deleting it deletes the enforcement of live doctrine. |
| `pre_rehab_banner_audit.py` | the entry **corrects an earlier claim** that it was permanently red: *"It is not. It is a 4-invariant file↔DB drift gate… it PASSES when the banners and the DB agree."* It fails today on invariant 2 only — 6 slugs carrying a retraction banner while sitting at `evidence_state='PARTIAL'`. A working gate with a real, fixable finding. |
| `adjudication_integrity.py` | the entry states outright *"why this entry is NOT retired"*: `scope` was NULL on all five admitted sources, and `schemas/tier_derivation.py` keys the ratified tier on it. |

## Owner-gated — stays, per the ruling

`scripts/generate/room_page.py` and `skills/question-author_SKILL.md`, parked in
`schema-reference-exemptions.yaml` awaiting decision 8 since 2026-08-02.

## What is actually left

`scripts/generate_parts.py` writes `parts/v10/`, which **does not exist** — `parts/` holds
only `88_to_90`, `_archived`, `deprecated`. But three live skills still name it
(`cross-reference-resolver`, `session-consolidator`, `structure-auditor`, plus two
deprecated ones). Deleting it creates the broken path the rule is meant to eliminate,
pointing the other way. It belongs to the render cluster awaiting decisions, not to a cull.

`scripts/audit/graph/__init__.py` is a one-line comment never imported as a package —
genuinely deletable, and worth almost nothing either way.

**Conclusion: the cull is not the win here.** Three working gates are in quarantine, one
enforcing operative doctrine; two Layer 0 tools are invisible to the test that was
supposed to find dead code; and one blocking gate is broken in the mode a human runs it.
Those are the repairs.
