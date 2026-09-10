# Conformance schema — verified findings

Source: a read-only Fable analysis of 2026-09-10, against the live tree at
`user_version` 72 (72 tables, 18 views, 0 triggers). Every claim below was executed or
read, never inferred. Hidden directories were searched with `grep -r` / `git grep`.

This is the INPUT to the per-layer meta-scripts. It is not the meta-scripts.

## The organising principle — the layers are a recursion

Owner, 2026-09-10: *"layer 1 is ensuring that layer 2 works properly when project
parameters"*, and *"you can decide at layer 2 … layer 2 is reserved for actual project
materials"*.

> **Layer 0 ensures Layer 1 works. Layer 1 ensures Layer 2 works. Layer 2 is the
> project's real stage work. Layer 3 is what that work produces.**

Every layer's conformance question is the same one — *does it ensure the layer below it
works?* Each meta-script measures that relationship, not a checklist of desirable
properties. Two consequences that change the requirements below:

1. **Deciding at Layer 2 is NOT prohibited.** A stage tool decides constantly; that is
   what a stage does. The rule is TENANCY: apparatus does not live in project materials.
   A check may invoke a Layer 2 tool and let it decide its own stage's business; a check
   may not *live* at Layer 2. Any "decides vs invokes" test is the wrong test.
2. **The ten defects are one defect.** `scope` had a CHECK — Layer 1 stated what a valid
   value was — and no writer could set it, so Layer 2 could not produce one. Every
   founding defect is **Layer 1 failing to ensure Layer 2 works**: a vocabulary with no
   writer, a table outside the capture path, a CHECK value no verb produces, a mirror
   missing a live column, a criterion pointed at a retired object, a rule whose only home
   is the stage it governs. So the L1 meta-script asks *"for every Layer 1 statement
   about what Layer 2 must produce, can Layer 2 produce it?"* and the L0 meta-script asks
   *"for every Layer 1 property, is something gating it?"*

**Notation.** **R** = requirement · **D** = mechanical detector · **caught** = which
known defect it would have caught. *A requirement with no detector is not a requirement*
— those are listed under "not mechanical" and dropped or made conditional on something
that must exist first.

---

## The ten founding defects

Each is a broken edge in the coupling graph, and each is verified.

| # | Defect | Broken edge |
|---|---|---|
| 1 | `evidence_sources.scope` had a CHECK and drove `derive_tier`, but was absent from `_ES_COLS` — the sanctioned writer could not write it. 9 of 9 sources NULL; 9 of 9 tiers underivable | column → writer |
| 2 | Six capture-path blindnesses in `WRITABLE_TABLES` | table → capture |
| 3 | `base_parameters` writable with no CLI verb; `source_value_extractions.parameter_id` readable by a view, no writer at all | table → writer |
| 4 | `adjudicate-term --outcome NAMES-NEW` refused unless the term existed, and nothing created one | CHECK value → writer |
| 5 | `check_rendered_docs` is BLOCKING, raises for a human, returns `EXAMINED: 0` for CI before opening the DB | check → subject |
| 6 | `validate_items` red at `EXAMINED: 0` against `min_items: 1`; `basis: base/base-parameter-vocabulary` points at `items` while the layer is `base_parameters` | check → criterion object |
| 7 | `emit_batch_sql.py`, `rename_insurance.py`, `audit_consolidator.py` read as inert; their only callers are PROSE | artefact → caller |
| 8 | G2/G3/G6 ratified, implemented only in `assess_cell.py`; `directness.py:80,82` says the opposite | rule → single home |
| 9 | `test_evidence_cell_state_2_3` built fixtures from a FROZEN baseline, asserting FKs on a dropped column | fixture → live schema |
| 10 | Two assertions passed under `except Exception` for a reason other than their claim | refusal → its reason |

## Six further defects found while measuring — all verified

- **N1 — capture hole, live.** `db.py` writes seven tables absent from
  `dbcore.WRITABLE_TABLES`: `bpc_metadata`, `conflicts`, `connection_targets`,
  `connections`, `gap_mining`, `item_audit_runs`, `supersession_check`. **Independently
  re-verified.** Seventh blindness, seven tables at once.
- **N2 — column-level dangling readers.** `schema_reference_audit` resolves TABLE names
  only (`:55-63`). Seven live readers still select `specifications.item_code`, dropped by
  071: `check_rendered_docs.py:96,202,218`, `build_site.py:98`, `pilot_renderings.py:237`,
  `spec_page.py:77`, `population_page.py:79`, `specification-curator_SKILL.md:82,99`.
- **N3 — the mirror lacks `scope`.** `schemas/evidence_source.py` has no `scope` field
  while the table has the column. The audit that would say so is advisory and
  permanently red with 243 findings, so the signal is buried in noise.
- **N4 — stale registry claims.** **Re-verified by execution:** four
  `no_floor: empty-by-decision` exemptions claim "examining 0" and examine
  `source_slug_links_duplicates` **9**, `metadata_integrity_audit` **9**,
  `research_protocol_audit` **28**, `gap_mining_audit` **5**. Quarantine reasons:
  `code_currency_audit` says "RED", exits 0; `adjudication_integrity` says "1 of 5",
  reports 9 of 9.
- **N5 — off-path writers.** `audit_consolidator.py:248` opens a canonical-defaulting
  path read-write and UPDATEs `item_audit_runs` (:270) with no refusal and no FK pragma.
  `resolve_dois.py:597` UPDATEs `evidence_sources`, outside the only exemption register
  (`migration_reproducibility.py:72`).
- **N6 — the ruled naming route has no instructional caller.** 17 `db.py` verbs are named
  by no skill, no CLAUDE.md, no governance file — including `add-term`, `add-parameter`
  and `adjudicate-term`, the route the owner ruled on 2026-09-09.

---

## A. Per-layer requirements

### Layer 0 — CLAUDE.md, the registry, `run_checks.py`, and every tool that proves Layer 1 works

| # | R | D | caught |
|---|---|---|---|
| L0.1 | Every check is registered and invoked only by `run_checks.py` | selftest C3/C5 already. **Add:** grep workflows, shells, hooks for direct invocation of any registry `cmd` or `scripts/audit/*.py`. Known exception `ci.yml:266` | inventory |
| L0.2 | Entry declares `level`, `basis`, `min_items` XOR `no_floor`(reason) | C5, C7, C8 already. **Nothing to add** | — |
| L0.3 | Prints `EXAMINED: <n>` on every run, not only when floored | `run_checks.py:322-324` fails only floored checks. **Add:** parse on every check | 5 |
| L0.4 | `kinds` includes the kind its subject classifies to | Needs a declared `subject:` first. **Not mechanical until then** | 6, 9 |
| L0.5 | **Falsifiability — a check must be able to FAIL** | Fault injection. DB-subject: copy to scratch, DROP every table its SQL names → conformant if exit≠0 or NOTHING-IN-SCOPE; PASS = **UNFALSIFIABLE**. Then DELETE FROM → conformant if `EXAMINED: 0`. File-subject: declare `falsified_by: {selftest: true}` or `none — <reason>`. Cost 67 × (3.6 MB copy + one run); nightly or `--falsify`, not per PR. 13 of 59 targets ship `--selftest` today | **5**, 10 |
| L0.6 | **The verdict is computed at Layer 0/1** (owner 2026-09-10) | "Decides" = a Layer 2 file has a conditional non-zero exit reachable from `main` (`retrieval_log.py:426,486,489,546`; `research_contract_hook.py:145,169`). "Invokes" = a Layer 0 file computes the exit. **Six entries fail today** | new class |
| L0.7 | Coverage in BOTH directions | C7 prints unclaimed as INFO (5 of 27). **Add:** declared `unclaimed:` allowlist with a reason per id | 6 |
| L0.8 | **Every hand-written claim carries a predicate for its own lapse** (rule 7) | `lapses_when:` — see C-CHECK. Fallback: `measured_at:` + `measured:` and a DRIFT warning; a bare integer without `measured_at` fails | **N4**, 6 |
| L0.9 | CLAUDE.md states no volatile fact; SPINE renders the contract | `claude_md_spine` covers the spine. **Add:** `\b\d{2,}\b (rows\|tables\|checks\|sources)` → FAIL unless the sentence says "derive" | — |
| L0.10 | The write-path audits keep their scope honest | **Invoke `db_path_env_audit.py` and `readonly_db_open_audit.py`, do not re-specify.** They do NOT cover: writers (out of scope by construction), the target table/column of a write, whitelist bypass, the FK pragma, YAML-embedded Python (`resolve-dois.yml:69`), skills' prose SQL | N5 |

**Not mechanical, dropped:** "a check is *useful*" — no script can score it.

### Layer 1 — schema, mirrors, contract, and the rules that govern every stage

| # | R | D | caught |
|---|---|---|---|
| L1.1 | Every table/view/**column** named by an executable or instructional caller exists | Table level done by `schema_reference_audit`. **Add column level:** parse the SELECT/SET/WHERE identifier lists of *executed* SQL and of fenced SQL in skills. Skills report-only — a fence cannot distinguish a quoted error from an instruction | **5, N2**, 9 |
| L1.2 | Every view executes | `SELECT * FROM <view> LIMIT 1`. **Cheapest requirement here and not registered today**; 072 exists because a probe, not a check, found three broken views | 072-class |
| L1.3 | A closed vocabulary has exactly one home — the column's CHECK | `dbcore.check_values()` non-empty for every column a writer validates; each `ENUM_GUARDS`/`RANGE_GUARDS` entry must name a column whose CHECK is absent, else it is a second home | 1 (inverse) |
| L1.4 | A mirror exists per written table, is in `MODEL_TABLE_MAP`, fields == columns | `validate_pydantic_schemas --strict`. Red-by-construction today (243 findings), so **per-table with a declared drift allowlist, or unenforceable** | **N3** |
| L1.5 | A ratified rule has ONE executable home, and it is Layer 1 | A Layer 2 file defining a function that returns a Layer 1 vocabulary value without importing the Layer 1 function of that name. Heuristic; report. Note `matrix_consistency.py:19-30` compares code to a transcription *inside the check* and never opens the doctrine document | **8** |
| L1.6 | Post-base population attachment takes four lens columns + COALESCE CHECK | `PRAGMA table_info` over non-base tables: `population_code`/`population`/`target_population` without the four → FAIL. **12 tables fail today**, including five splinter tables the ruling says are deleted and which still exist at 0 rows | ruling unswept |
| L1.7 | A NOT NULL FK into an emptied table is reported | The CLAUDE.md §4 snippet, registered | — |
| L1.8 | **Rule 5 — dual homes are declared; a parity check is a symptom, not a fix** | See C-DERIVED | 1, 3-class |
| L1.9 | A contract criterion names its OBJECT | `schemas/pipeline_contract.py` is `extra="forbid"` — an `object:` field must exist first. **Not mechanical until then**, and it is the only route by which defect 6 becomes checkable | **6** |
