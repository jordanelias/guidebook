# Per-layer META-SCRIPTS — specification

**What this is.** A family of five diagnostics, one per layer, that answer *why is this not
working* in seconds. Owner, 2026-09-10:

> *"the meta properties are so that you have a quick diff tool or schema to use to figure out why
> stuff isn't working because it's constant"*

**The thing being optimised is TIME TO DIAGNOSIS.** Not coverage, not completeness, not
governance. A crude tool run every day beats a comprehensive standard nobody runs. Every
requirement below is marked **v1** (works against the repo as it exists today, no new declaration
file, no new field in existing YAML) or **v2** (needs something built first, named explicitly).
v1 is the deliverable.

**These are NOT checks.** They are never registered in `governance/check-registry.yaml`, never
gate a PR, and exit 0 unless `--strict` is passed. Registering them would make them subject to
L0.1 below — which forbids invoking a registered check outside `run_checks.py` — and the whole
point is that a human runs them by hand at the moment of confusion. CLAUDE.md §8 asks what wrong
thing reaches the *guidebook* if they do not exist: the founding-defect class does. Nine sources
were admitted carrying `scope` NULL and therefore nine underivable tiers, while six gates passed
green, because no tool asked whether a thing Layer 1 demanded could be produced by Layer 2 at all.

---

## 0. Verification statement — what was re-executed for this spec

Every number below was produced on 2026-09-10 against a scratch copy
(`cp data/guidebook.db $SCRATCH/gb.db`, opened `mode=ro`). The canonical database was never
opened read-write.

| Claim in `conformance-schema-findings.md` | Result |
|---|---|
| N1 — seven `db.py` write targets absent from `dbcore.WRITABLE_TABLES` | **REPRODUCES exactly.** AST parse of executed SQL in `scripts/db.py` finds 25 write targets; 7 absent: `bpc_metadata`, `conflicts`, `connection_targets`, `connections`, `gap_mining`, `item_audit_runs`, `supersession_check` |
| N4 — four false `no_floor: empty-by-decision` exemptions | **REPRODUCES exactly.** 12 entries carry that reason; running all twelve: `source_slug_links_duplicates` **EXAMINED: 9**, `metadata_integrity_audit` **9**, `research_protocol_audit` **28**, `gap_mining_audit` **5**. The other eight print `EXAMINED: 0` or speak `NOTHING-IN-SCOPE` and are honest |
| L1.2 — every view executes | **REPRODUCES.** All **18** views return from `SELECT * FROM <v> LIMIT 1`; 0 broken. Migration 072 did its job |
| N2 — dangling readers of `specifications.item_code` | **REPRODUCES.** 7 executed-SQL sites in 5 files: `check_rendered_docs.py:95,201,218`, `build_site.py:96`, `pilot_renderings.py:238`, `spec_page.py:73`, `population_page.py:75` (line numbers are the `execute()` call). Plus 4 sites reading the equally-dropped `specifications.population_code` |
| N3 — the Pydantic mirror lacks `scope` | **REPRODUCES.** `schemas/evidence_source.py::EvidenceSource` has 20 fields, none named `scope` |
| N5 — off-path writers | **REPRODUCES.** `audit_consolidator.py:248` raw `sqlite3.connect(str(DB_PATH))` read-write, `UPDATE item_audit_runs` at :270. `resolve_dois.py:597` `UPDATE evidence_sources SET {…}` |
| L1.6 — 12 tables carry a legacy population column with no lens columns | **REPRODUCES, given the base exclusion.** 14 tables carry `population_code`/`population`/`target_population` without the four lens columns; two of them (`populations`, `population_axis_map`) are base registries the ruling scopes out, leaving **12** |

**Claims that did NOT reproduce, corrected:**

1. **Defect 1's writer half is REPAIRED.** `scope` **is** in `_ES_COLS` (`scripts/db.py:2337`) and
   `add-source --scope` exists (`db.py:1288`) with a required-for-evidence-type refusal at
   `db.py:1915`. The findings document was written before that landed the same day. The rows are
   still 9/9 NULL and the mirror is still missing it. **The worked example in §5 uses the corrected
   state**, because a diagnostic that reports a repaired edge as broken is the defect it exists to
   catch.

2. **`user_version` 72, but 70 user tables, not 72.** `sqlite_master` holds 71 `type='table'` rows,
   one of which is `sqlite_sequence`. 18 views, 0 triggers. The version number and the table count
   coinciding at 72 was a coincidence that has since drifted.

3. **N6 measures 14 orphan `db.py` verbs, not 17,** and `add-term` is no longer among them — the
   2026-09-09 ruling recorded in `references/project-standards.md` names it. Method: 47 verbs from
   `add_parser(...)`, matched against `grep -rhoE 'db\.py [a-z0-9-]+'` over
   `skills governance references decisions workplan specs architecture CLAUDE.md`. Orphans:
   `add-case-study`, `add-economics-entry`, `add-item`, `add-jurisdictional-value`, `add-locator`,
   `add-parameter`, `adjudicate-term`, `amend-search`, `amend-source`, `correct-source`,
   `resolve-candidate`, `update-gap-addressability`, `update-locator`, `upsert-language`.
   **The count is method-sensitive**, which is why the script must print its search roots. See
   §9 L2.4 for the `add-item` false positive.

4. **L1.3's proposed detector is inverted and would have missed the canonical case.** The findings
   say to require `dbcore.check_values()` non-empty. Executed: `check_values(conn,
   'evidence_sources', 'scope')` returns **the empty set**, because its regex
   (`dbcore.py:348`) matches only `CHECK (col IN (...))` and the live constraint is
   `CHECK (scope IS NULL OR scope IN (...))`. **16 closed vocabularies in the live schema are
   invisible to it** — `bpc_metadata.closure_definition_version`, `case_studies.cost_data_quality`,
   `economics_entries.confidence`, `economics_entries.quant_status`,
   `evidence_sources.processing_blocked_reason`, `.scope`, `.verification_closure_reason`,
   `.verification_disposition`, `.verification_method`, `gaps.mining_addressability`,
   `jurisdictional_values.is_code_minimum`, `search_candidates.locator_status`,
   `search_executions.mining_direction`, `.saturation_signal`, `.target_evidence_type`,
   `.target_scope` — against 92 that it does read. For all sixteen, `dbcore.check_declared()`
   silently permits any value. **That is a live Layer 1 defect this spec found, not a
   requirement.** L1.3 below is rewritten accordingly.

5. **CLAUDE.md §7's own derivation command is broken.**
   `grep -rhoE '\b[A-Z]-[0-9]{2}\b' references/part04-item-index.md` returns nothing: that file
   does not exist. Deriving from the live surface instead gives **17 distinct prefixes**
   (A E F G H D B I C K T V M J S O L) across **130 files** under `references/`, `working/` and
   `index.html`. See L4.2.

6. **`migration_reproducibility.EXEMPT_TABLES` holds two names, not one.** `pipeline_runs` (the one
   CLAUDE.md §2 rule 3 names) **and `evidence_source_authors`** — the table the 2026-08-19
   fabrication happened in. A count divergence there is invisible to the blocking gate.

**Cost baseline for comparison.** `python3 scripts/run_checks.py --all` = **41.5 s**, 67 checks,
49 green, 10 NOTHING-IN-SCOPE (6 of them blocking), 8 advisory failures.
`run_checks.py --selftest` = **0.84 s**. Every meta-script below is budgeted under 3 s.

---

## 1. The organising principle

Owner, 2026-09-10: *"layer 1 is ensuring that layer 2 works properly when project parameters"* and
*"you can decide at layer 2. why wouldn't you be able to? layer 2 is reserved for actual project
materials tho"*.

> **L0 ensures L1 works. L1 ensures L2 works. L2 is the project's real stage work. L3 is what that
> work produces. L4 is supplementary.**

Every meta-script asks exactly one question, and it is the same question:

| Script | Its one question |
|---|---|
| **L0** | For every Layer 1 property, is something gating it — and can that gate fail? |
| **L1** | For every Layer 1 statement about what Layer 2 must produce, can Layer 2 produce it? |
| **L2** | For every Layer 3 table a stage owns, can that stage's sanctioned tools put a row in it and ship it — and does anything apparatus-shaped live here? |
| **L3** | Is every row the product of that path, and does it stay in its own stage? |
| **L4** | Is any supplementary artefact being read as if it were canonical? |

**Two corrections that are load-bearing and must not be reintroduced.**

- **Deciding at Layer 2 is not prohibited.** A stage tool decides constantly; judgment's entire job
  is to decide. Any "decides vs invokes" test is the WRONG test and no script here implements one.
  The rule is **TENANCY**: apparatus does not live in project materials. A check may invoke a Layer
  2 tool and let that tool decide its own stage's business; a check may not *live* at Layer 2.
- **The founding defects are one defect.** `evidence_sources.scope` had a CHECK — Layer 1 said what
  was valid — and no writer could set it, so Layer 2 could not produce one. A vocabulary with no
  writer, a table outside the capture path, a CHECK value no verb produces, a mirror missing a live
  column, a criterion pointed at a retired object, a rule whose only home is the stage it governs:
  all six are **Layer 1 failing to ensure Layer 2 works**.

---

## 2. Common shell — invocation, output grammar, cost

### 2.1 Files

```
scripts/meta/metacore.py      shared: SQL-literal extraction, schema snapshot, output grammar
scripts/meta/l0.py            gates over Layer 1 properties
scripts/meta/l1.py            Layer 1 statements vs Layer 2's ability to satisfy them
scripts/meta/l2.py            stage tools vs the tables they own
scripts/meta/l3.py            rows vs the path that produced them
scripts/meta/l4.py            supplementary data vs canonical reading
```

`metacore.py` imports `scripts/dbcore.py` for `connect()`, `db_path()` and `is_canonical()` — it
does not re-implement them. It opens **read-only, always**: `dbcore.connect(readonly=True)`. No
meta-script accepts a write flag.

### 2.2 CLI, identical across all five

```
python3 scripts/meta/lN.py                       # whole layer, summary only
python3 scripts/meta/lN.py --explain             # summary + the evidence line for each broken edge
python3 scripts/meta/lN.py --subject <SUBJECT>   # one artefact, every edge, full detail
python3 scripts/meta/lN.py --edge <ID>           # one edge across every subject (e.g. --edge L1.4)
python3 scripts/meta/lN.py --stage <stage-id>    # L2 and L3 only; ids from pipeline-contract.yaml
python3 scripts/meta/lN.py --json                # machine form, same content, for a future check
python3 scripts/meta/lN.py --strict              # exit 1 if any edge is BROKEN (default: always 0)
python3 scripts/meta/lN.py --db PATH             # default: dbcore.db_path()
```

`<SUBJECT>` is layer-shaped and always accepted in the form the error message would print:
`evidence_sources.scope` (L1 column), `evidence_sources` (L1/L2/L3 table), a check id (L0),
a stage id (L2/L3), a path (L4).

### 2.3 Output grammar — the product is the output

Five verdict tokens, fixed width, one per line, so `grep -c MISS` works and the eye finds the
column:

```
OK      the edge resolves
MISS    the edge is absent — the thing at the far end does not exist
STALE   the edge resolves to something that no longer matches (drift)
VACUOUS the edge resolves but has no subject — 0 rows, 0 files, 0 statements
N/A     out of scope, with the reason on the same line
```

Rules the format obeys, each because a prose report failed here before:

1. **One line per edge.** Continuation lines are indented and never carry a verdict token.
2. **Every claim carries its evidence on the same line** — `file:line`, a table name, or a count.
   A verdict with no locator is a bug in the script.
3. **`EXAMINED: <n>` last**, always, in `run_checks.py`'s exact grammar (`EXAMINED_RE`,
   `run_checks.py:282`) so the number can be read by the same regex. A meta-script that examined
   nothing prints `EXAMINED: 0` and says so in the verdict line; it never prints a clean summary.
4. **No volatile fact is written into the script.** Counts, vocabularies, table lists and row
   totals are derived on every run (CLAUDE.md rule 7). The one exception is the tenancy prefix
   table in §7 L0.6, which is declared to be the only home of that fact and fails closed.
5. **Colour never carries meaning** — CI logs and pipes drop it.

### 2.4 Cost budget

| Script | Budget | Measured basis |
|---|---|---|
| `l0.py` | **< 2 s** | registry parse 0.13 s + `--selftest` 0.84 s reused, no check execution |
| `l1.py` | **< 2 s** | AST over 127 files = 0.60 s; schema snapshot 0.05 s; 18 view probes 0.02 s |
| `l2.py` | **< 2 s** | same AST pass, plus a migration-directory scan |
| `l3.py` | **< 3 s** | whole-DB row counts over 70 tables = 0.3 s; provenance scan of `data_migrations` (364 rows) |
| `l4.py` | **< 3 s** | one `grep -rE` over `references/ working/ index.html` (130 hits) |

**Anything slower goes behind a flag.** Named today: `--falsify` (L0.5, fault injection, 67 ×
a 3.6 MB copy + one run ≈ 5 minutes) and `--deep` (L3, per-row comparison). Neither runs by
default, ever.

### 2.5 The four parsing rules that prevent every false positive found so far

These are not style preferences. Each one was reproduced on this repo while writing this spec, and
the numbers are the drop in findings from applying it. Baseline for the L1.1 column detector:
**44 findings, of which 33 were false**.

| # | Rule | What it kills | Measured |
|---|---|---|---|
| **P1** | **Parse identifier lists out of EXECUTED SQL via AST, never a text window.** Walk `ast.Call` where `func.attr in {execute, executemany, executescript}`, take `args[0]`, concatenate its `ast.Constant` string parts **joined by `\n`** (not space — a space-join makes `--` comments swallow the rest of the statement). | Prose in comments, docstrings, error strings, and any `population_code` that is a local variable rather than a column. A naive regex over `scripts/db.py` raw text returns 32 "write targets" including the English words **`a`, `after`, `an`, `connection`, `it`, `search`, `that`, `was`** — and *misses* `source_slug_links`, whose statement is `INSERT OR IGNORE INTO`. AST + a widened verb regex returns exactly 25, all real. | 32 → 25, 8 false gone, 1 false negative fixed |
| **P2** | **Strip SQL comments, then strip single-quoted string literals, before scanning identifiers.** `--[^\n]*` and `/*…*/`, then `'(?:[^']\|'')*'`. Never strip double-quoted text — in SQLite that is identifier quoting. | A quoted VALUE read as a column name. `research_batch_dod.py` seeds `VALUES (1,'s','ID','id','grey',…)` and the bare word `id` was reported as a missing column of `search_executions` seven times; `generate_parts.py:357`'s `evidence_type IN ('standard_eb','national_fw','code')` produced `evidence_sources.code`. Also: a naive `CHECK\s*\([^)]*\btier\b` over the `evidence_sources` DDL reports a CHECK on `tier` — **there is none**; the word appears inside a comment in a different constraint. | removes 12 of 31 |
| **P3** | **A table the file itself CREATEs is a fixture; its schema wins for that file.** Collect `CREATE TABLE/VIEW <name>` from the file's own source and exclude those names from live-schema comparison. | Selftest and unit-test fixtures. `validate_verification_consistency.py:88` builds a 9-column `specifications` in `:memory:`; comparing it to the live table produced 9 findings. `emit_batch_sql.py:200-202` produced 2 more. | removes 11 |
| **P4** | **Bare (unqualified) column mode runs only when the statement resolves to exactly one live table AND contains no interpolation hole.** Represent an `ast.FormattedValue` as a distinctive sentinel (`@HOLE@`), never as `?` — `?` is a legitimate bind placeholder and suppressing on it discards half the corpus. `resolve_dois.py:830` is `FROM {TABLE} e JOIN v_evidence_authors v`: one table resolves, so every `e.`-qualified column was reported against the view. | 6 phantom columns on `v_evidence_authors` | removes 6 |

**Net: 44 → 11 findings, all 11 real,** and the 7 `specifications.item_code` sites N2 names are
among them. Runtime after all four rules: **0.60 s** over 726 executed statements in 127 files.

**Prior art in this repo, and it agrees.** `scripts/audit/schema_reference_audit.py:60-64` carries
a comment recording the identical finding from the table-level sweep: *"Every false positive measured
came from this one keyword reading prose — 'an UPDATE statement's SET clause', 'an UPDATE changes no
count' … and a real UPDATE always names its table then SET."* Its fix was to require the `SET`
keyword. P1–P4 are the same lesson applied at the column level, where a text window cannot work at
all.

**Two further rules that add coverage rather than removing noise:**

- **P5 — constant-propagate single-assignment local string names.** `execute(q)` where `q` is
  assigned once from string literals. **27 of 750** `execute()` call sites under `scripts/` pass a bare `Name`;
  without this, `pilot_renderings.py:238` — one of N2's seven — is invisible. Propagate only when
  the name has **exactly one** assignment in the file; two or more, skip and count it.
- **P6 — count and print what could not be parsed.** `EXAMINED:` must be accompanied by
  `UNPARSED: <n>` (files with `SyntaxError`, `execute()` on a call/subscript — **1** today, names
  with multiple assignments). A detector that silently drops what it cannot read is a gate that
  passes having examined nothing.

---

## 3. `l1.py` — *for every Layer 1 statement about what Layer 2 must produce, can Layer 2 produce it?*

This is the script to write first. It is where the founding defect lives, and it is the one whose
output the owner's sentence describes.

### 3.1 Worked example — the canonical case

```
$ python3 scripts/meta/l1.py --subject evidence_sources.scope

L1  evidence_sources.scope                          db user_version 72   2026-09-10
──────────────────────────────────────────────────────────────────────────────────
 L1.3  vocabulary  OK       5 values declared by the column's own CHECK
                            high_control lower_control national international
                            intrinsic                       evidence_sources DDL
 L1.3b refusal     MISS     dbcore.check_values() returns {} for this column —
                            its regex reads `CHECK (col IN (...))` and this
                            constraint is `CHECK (col IS NULL OR col IN (...))`,
                            so check_declared() permits ANY value  dbcore.py:348
 L1.11 writer      OK       db.py insert_evidence_source, _ES_COLS   db.py:2337
 L1.11 CLI         OK       add-source --scope                       db.py:1288
                            + refusal: required for evidence types spanning
                            two tiers                                db.py:1915
 L1.4  mirror      MISS     schemas/evidence_source.py EvidenceSource declares
                            20 fields, none named scope
 L1.1  reader      OK       schemas/tier_derivation.py derive_tier(evidence_type,
                            scope) — the ratified ladder reads it
 L3.1  rows        VACUOUS  9 of 9 evidence_sources rows carry scope NULL
                            => 9 of 9 stored tiers underivable
──────────────────────────────────────────────────────────────────────────────────
 VERDICT  2 BROKEN EDGES — refusal (L1.3b), mirror (L1.4)
          The writer half was repaired 2026-09-10; the rows predate it.
 EXAMINED: 1 column, 7 edges     UNPARSED: 0
```

Whole-layer form, summary only:

```
$ python3 scripts/meta/l1.py

L1  schema, mirrors, contract, and the rules that govern every stage
    70 tables · 18 views · 0 triggers · user_version 72          2026-09-10
──────────────────────────────────────────────────────────────────────────────────
 L1.1  column readers resolve            MISS     11 sites   --edge L1.1
 L1.2  every view executes               OK       18 of 18
 L1.3  one home per closed vocabulary    OK       0 second homes in 3 guards
 L1.3b refusal can read the vocabulary   MISS     16 of 108  --edge L1.3b
 L1.4  mirror matches the live table     MISS     see --edge L1.4
 L1.5  a ratified rule has one home      STALE    1 pair     --edge L1.5
 L1.6  lens columns after base           MISS     12 tables  --edge L1.6
 L1.7  NOT NULL FK into an emptied table MISS     22 columns, 4 roots
 L1.10 fixture schemas match live        STALE    1 file
 L1.11 every CHECKed column has a writer MISS     see --edge L1.11
 L1.12 contract criterion has a check    MISS     5 no check, 5 unclaimed
──────────────────────────────────────────────────────────────────────────────────
 EXAMINED: 88 objects, 726 executed statements, 27 contract criteria
 UNPARSED: 1 execute() call, 0 files
 4 minutes of reading saved: run --edge L1.7 first, it has the fewest roots
```

### 3.2 Edges

| # | Requirement | Mechanical detector | v | Catches |
|---|---|---|---|---|
| **L1.1** | Every **column** named by an executed statement exists in the live schema | The P1–P6 pass. Resolve `FROM/JOIN/INTO/UPDATE <t> [AS] <alias>`; check every `alias.col`, and every bare identifier when exactly one live table is in scope. **Table level is already done by `scripts/audit/schema_reference_audit.py` (blocking, `base/base-names-resolve`) — invoke it, do not re-implement it.** This edge adds only the column level, which `schema_reference_audit.py:54-65` explicitly does not do — its `CTX` regex captures only the positions that hold a TABLE or VIEW name | **v1** | N2, defect 5 |
| **L1.2** | Every view executes | `SELECT * FROM "<view>" LIMIT 1` for each `type='view'` in `sqlite_master`, catching `sqlite3.Error`. **18 today, all green.** Cheapest edge in the family and unregistered anywhere; migration 072 exists because a hand probe, not a check, found three broken views | **v1** | 072-class |
| **L1.3** | A closed vocabulary has exactly one home — the column's own CHECK | For each entry in `emit_data_migration.ENUM_GUARDS` (2) and `RANGE_GUARDS` (1), assert the named column has **no** CHECK in the live DDL. A guard whose column also has a CHECK is a second home (rule 5). **0 second homes today** — but see P2: the naive form of this test reports a phantom CHECK on `tier` from a word inside a comment | **v1** | 1 (inverse) |
| **L1.3b** | The refusal can actually read the vocabulary it enforces | Extract closed vocabularies from DDL with **both** forms — `CHECK (c IN (...))` and `CHECK (c IS NULL OR c IN (...))` — then call `dbcore.check_values()` for each and flag every column where the DDL has a vocabulary and `check_values()` returns `{}`. **16 of 108 today.** This is the edge that would have caught defect 1 from the refusal side | **v1** | **new, verified** |
| **L1.4** | A mirror exists per written table, is in `MODEL_TABLE_MAP`, and its fields match the live columns | `scripts/audit/validate_pydantic_schemas.py --strict` already does this and is **advisory and permanently red (243 findings)**, so the signal is buried. **v1 does not re-run it**: it runs it per-table for the 22 tables in `dbcore.WRITABLE_TABLES` only, and reports each table's delta separately. That converts one red wall into 22 independent verdicts, of which `evidence_sources` → missing `scope` is the one that matters | **v1** | **N3** |
| **L1.5** | A ratified rule has ONE executable home, and it is Layer 1 | Report-only heuristic: a file under a Layer 2 prefix (§7 L0.6) defining a function that returns a value drawn from a Layer 1 vocabulary, without importing the Layer 1 function of that name. Known pair: G2/G3/G6 in `scripts/assess/assess_cell.py::source_grain()` vs `schemas/directness.py:80,82`, which map `co1 → specific` and `standard_eb → code` unconditionally. Also flag `scripts/audit/matrix_consistency.py:19-30`, which compares code against a transcription **inside the check** and never opens the doctrine document | **v1, report-only** | **8** |
| **L1.6** | A table attaching a determination to a group of disabled people takes four lens columns and a COALESCE CHECK | `PRAGMA table_info` over every non-`base_*` table: presence of `population_code`/`population`/`target_population` **and** absence of all four of `identity_code/icf_code/needs_code/medical_code` → MISS. Exclude the base registries by name — `populations` and `population_axis_map` are the identity lens and a crossing map, and the ruling scopes to "after the base phase". **14 raw, 12 after the exclusion**; five of the twelve are the splinter tables D-0182 says are deleted, all at 0 rows. Assert the surviving CHECK is `COALESCE(...) IS NOT NULL`, **never** a sum `= 1` | **v1** | ruling unswept |
| **L1.7** | A NOT NULL foreign key into an emptied table is reported, and its ROOT named | The CLAUDE.md §4 snippet, plus a transitive collapse. **22 unwritable columns today, but only 4 roots**: `items` (10 columns), `case_studies` (4), `economics_entries` (2), `base_parameters` (1 → `specifications` → `specification_source_links`). Print roots first. Also print the softer class the snippet misses: **8 nullable FKs into empty tables** — `specifications.medical_code → base_taxonomy_medical` means that lens cannot be used even though the row can be written | **v1** | — |
| **L1.8** | Rule 5 — no fact has two stored homes | **v2.** Needs `governance/dual-homes.yaml` declaring each accepted dual home and the retirement plan for it, because "same column name in two tables" is not evidence of a copy — a pointer looks identical. v1 prints the raw signal as INFO only: identically-named non-key columns across tables in different stages, which today cannot be computed at all because stage attribution does not exist (§8) | **v2** | 1, 3-class |
| **L1.9** | A contract criterion names its OBJECT | **v2.** `schemas/pipeline_contract.py` is `extra="forbid"`, so an `object:` field must exist before anything can read it. This is the only route by which defect 6 — `basis: base/base-parameter-vocabulary` pointing at `items` while the layer is `base_parameters` — becomes mechanically checkable | **v2** | **6** |
| **L1.10** | A test fixture's schema matches the live schema | Parse `CREATE TABLE <live-name> (...)` out of `scripts/**/*.py` (after P2 comment-stripping — without it, prose inside the parenthesis parses as the columns `a`, `and`, `but`, `not`, `so`, `when`, `which`), and diff the column set against live. **Report-only**, because a fixture legitimately declares a subset. Flag only columns the fixture has that live does **not**. **1 today** — `emit_batch_sql.py:191` builds `evidence_sources` with `note` and `slug`. This edge exists because P3 deliberately hides fixtures from L1.1, and defect 9 lives exactly there | **v1** | **9** |
| **L1.11** | Every column with a CHECK, a NOT NULL, or a live reader has a sanctioned writer that can set it | Intersect: columns carrying a CHECK or NOT NULL (from DDL) × columns reachable from `db.py`'s per-table column allow-lists (`_ES_COLS` and its siblings, extracted by AST) × columns named by an `add_argument` destination. A column in the first set and absent from both others is the defect-1 shape | **v1** | **1** |
| **L1.12** | Every contract criterion has a check, and every check's basis resolves | `run_checks.py --selftest` C7 already resolves basis refs and prints unclaimed criteria as **INFO (5 of 27)**. **Invoke it and parse its output — do not re-implement C7.** Add the half C7 does not do: a criterion whose `check:` key is literally `None`. **5 of 22 stage criteria today** — `evidence/discovery-provenance`, `judgment/convergence-independence`, `synthesis/opus-routing`, `specification/derivation-handshake`, `render/render-freshness` — all 5 cross_stage criteria do declare one. Note the two sets differ: `render/render-freshness` has no check yet IS claimed by a registry basis, and `cross_stage/attestation-doctrine-binding` declares a check yet is claimed by none. **Print both columns; they are different failures** | **v1** | **6** |

### 3.3 Known false positives, and the parse that avoids them

All four are §2.5 P1–P4 and were each reproduced on this repo. The residue after applying them:

- **11 L1.1 findings, all real.** 7 × `specifications.item_code`, 4 × `specifications.population_code`.
- **`migration_reproducibility.py:478`** was a twelfth until P3 was extended: it creates its fixture
  as `CREATE TABLE {table}` through an f-string, so a literal-name `CREATE` scan does not see it.
  **Extension to P3:** a file that creates ANY table through an interpolated name is fixture-bearing;
  suppress bare mode for that whole file and count it under `UNPARSED`.
- **Not a false positive, do not suppress:** `specifications.population` in
  `scripts/tests/test_evidence_cell_state_2_3.py:151` and
  `test_validate_evidence_state_2_4.py:148,158`. P3 hides these from L1.1 by design; L1.10 is where
  they must surface.

### 3.4 What `l1.py` cannot catch — read this before deleting anything

- **Prose callers are invisible by construction.** A skill that says "write a row to X" in English,
  a DR that names a column, a runbook step — none of these parse. **This nearly caused three
  wrongful deletions in one session.** `emit_batch_sql.py`, `rename_insurance.py` and
  `audit_consolidator.py` all read as inert to a caller scan, because their only callers are prose
  (defect 7). **`l1.py` prints a standing banner: `PROSE CALLERS NOT SCANNED — an object with 0
  detected callers is UNPROVEN, not dead.`**
- **Fenced SQL in skills is report-only, never a verdict.** A fence cannot distinguish an
  instruction from a quoted error message. `skills/specification-curator_SKILL.md:59,66,70,77,83,100`
  names `items.item_code` and `specifications.population_code`; both are gone; the file is still a
  legitimate historical record of a superseded design.
- **A 0-row object is unproven, not clean** (CLAUDE.md rule 4). L1.2 proves a view *parses*, not
  that it *returns the right rows*; migration 064 exists because a byte-exact diff called
  `v_item_provenance` clean while it rendered 0 rows.
- **`user_version` is not compared to anything.** Schema/mirror drift is caught; schema/migration
  drift is `migration_reproducibility`'s job and it compares **row COUNTS only** — an UPDATE is
  invisible to it.
- **It cannot tell a pointer from a copy.** That is L1.8, and it is v2 for a reason: the two look
  identical in DDL.

---

## 4. `l0.py` — *for every Layer 1 property, is something gating it?*

### 4.1 Worked example

```
$ python3 scripts/meta/l0.py --subject metadata_integrity_audit

L0  check `metadata_integrity_audit`                    registry 67 active   2026-09-10
────────────────────────────────────────────────────────────────────────────────────
 L0.1  invoked only by run_checks.py   OK     no direct call in .github/ .claude/
                                              scripts/preflight.sh regenerate_derived.sh
 L0.2  declares level/basis/floor      OK     advisory · evidence/evidence-verification-gate
                                              · no_floor  (selftest C5/C7/C8 green)
 L0.3  prints EXAMINED: <n>            OK     EXAMINED: 9
 L0.8  the no_floor reason is true     STALE  reason says "instrumented and examining 0
                                              because the corpus was emptied by
                                              decision" — it examined 9 and exited 1
                                              check-registry.yaml:401
 L0.6  tenancy: apparatus at L0/L1     OK     scripts/audit/metadata_integrity_audit.py
 L0.5  falsifiable                     ?      no --selftest; needs --falsify
────────────────────────────────────────────────────────────────────────────────────
 VERDICT  1 STALE EDGE — L0.8. The exemption describes a corpus that no longer exists.
 EXAMINED: 1 check, 6 edges
```

Whole-layer form:

```
$ python3 scripts/meta/l0.py

L0  CLAUDE.md, the registry, run_checks.py, and everything that proves L1 works
    67 active checks · 4 quarantined · 27 contract criteria             2026-09-10
────────────────────────────────────────────────────────────────────────────────────
 L0.1  invoked only by run_checks.py    MISS    10 direct call sites   --edge L0.1
 L0.2  registry entry well-formed       OK      selftest C1-C8 PASS in 0.84s
 L0.3  every check prints EXAMINED      MISS    2 of 67   --edge L0.3
 L0.6  apparatus is not tenanted at L2  MISS    6 of 67   --edge L0.6
 L0.7  coverage in both directions      MISS    5 criteria unclaimed, 22 checks
                                                with basis: unattributed
 L0.8  hand-written claims are true     STALE   4 of 12 no_floor reasons,
                                                2 of 4 quarantine reasons
 L0.9  CLAUDE.md states no volatile fact STALE  1 broken derivation command
 L0.5  falsifiability                   N/A     behind --falsify (~5 min)
────────────────────────────────────────────────────────────────────────────────────
 EXAMINED: 67 checks, 27 criteria, 4 quarantine entries
```

### 4.2 Edges

| # | Requirement | Mechanical detector | v | Catches |
|---|---|---|---|---|
| **L0.1** | Every check is registered, and invoked only by `run_checks.py` | `--selftest` **C3** already asserts every registered executable exists on disk — invoke it. Add the inverse: `grep -rn` each of the **63 registered executables** across `.github/`, `.claude/`, `scripts/preflight.sh`, `scripts/regenerate_derived.sh`, discarding lines containing `run_checks`. **10 sites today**, and they are not all wrong: `tools/pipeline_completeness.py` and `tools/evidentiary_audit.py` are dual-purpose (generator + `--check`) and `scripts/regenerate_derived.sh` calls the generator half legitimately. **Print the site, not a verdict**, and require an `# meta:l0.1-ok <reason>` comment on the calling line to clear it. `.claude/settings.json:68` invoking `scripts/audit/research_batch_dod.py` from `SessionStart` is the one that is genuinely un-gated | **v1** | inventory |
| **L0.2** | Entry declares `level`, `basis`, and `min_items` XOR `no_floor(reason)` | **`run_checks.py --selftest` C5/C7/C8 already do all of this.** Shell out, parse, report. **Nothing to add.** Cost 0.84 s | **v1** | — |
| **L0.3** | Every check prints `EXAMINED: <n>` on every run, not only when it declared a floor | `run_checks.py:322-324` fails a check for a missing `EXAMINED` line **only when `min_items` is declared** — 34 of 67 have a floor, so 33 are unpoliced. Detector: run each check once and apply `EXAMINED_RE` (`run_checks.py:282`, import it, do not copy the regex). **Two entries print no `EXAMINED:` line today** — `citation_mining_session` and `citation_mining_backlog_t2` — both because `citation_mining_completeness.py` prints `Examined (…): 5` in its own casing and speaks `NOTHING-IN-SCOPE` instead. That is a documented accommodation, so the verdict is **N/A with the reason**, not MISS. **Cost: this edge needs a real run of every check — 41.5 s. Put it behind `--run-checks`, not in the default path.** Default path parses the last `run_checks.py --all` log if one is on disk, and says `STALE LOG` with its age if not | **v1, flagged** | 5 |
| **L0.4** | `kinds` includes the kind its subject classifies to | **v2.** Needs a declared `subject:` on registry entries. Until then a check's subject is only knowable by running it | **v2** | 6, 9 |
| **L0.5** | **A check must be able to FAIL** | Fault injection, behind `--falsify`. DB-subject: copy to scratch, `DROP` every table the check's SQL names (extracted by the P1 pass), re-run — conformant if exit ≠ 0 or it reports NOTHING-IN-SCOPE; a **PASS is UNFALSIFIABLE**. Then `DELETE FROM` those tables — conformant if `EXAMINED: 0`. File-subject: no injection; require a declared `falsified_by:` (v2) or fall back to "ships a `--selftest`". **13 of the 58 registered Python targets ship one today.** Cost: 67 × (3.6 MB copy + one run) ≈ 5 minutes, so nightly or on demand, never per PR | **v1 for DB-subject checks; v2 for the `falsified_by:` declaration** | **5**, 10 |
| **L0.6** | **Tenancy — apparatus does not live in project materials** | A registry `cmd` whose executable path starts with a Layer 2 prefix. The prefix table is 5 entries — `scripts/research/`, `scripts/assess/`, `scripts/generate/`, `tools/`, `skills/` — and it returns **exactly the six entries the owner named on 2026-09-10**: `author_fidelity`, `research_contract_sync`, `pipeline_completeness_fresh`, `evidentiary_audit_fresh`, `context_map_fresh`, `site_pages_fresh`. **No "decides vs invokes" test. A check may invoke a Layer 2 tool and let it decide its stage's business; the check may not LIVE there.** The remedy is unchanged: the check moves to Layer 0 and calls the Layer 2 tool. **Fails closed:** any registry executable whose path matches no prefix in the table is reported `UNCLASSIFIED — extend the prefix table`, so a new directory forces an edit instead of passing silently. Today the 67 entries bucket as 15 `scripts/`, 33 `scripts/audit/`, 3 `scripts/ci_helpers/`, 10 `scripts/tests/`, 3 `scripts/generate/`, 1 `scripts/research/`, 2 `tools/` | **v1** | new class |
| **L0.7** | Coverage in **both** directions | C7 already prints unclaimed criteria as INFO (**5 of 27**) and checks with no stated authority (**22 of 67 `basis: unattributed`**). v1 promotes both from INFO to a named edge and prints the lists. A declared `unclaimed:` allowlist with a per-id reason is **v2** | **v1 (report) / v2 (allowlist)** | 6 |
| **L0.8** | **Every hand-written claim in the registry carries a predicate for its own lapse** | v1 falsifies the specific claim shape that has failed: a `no_floor` reason containing "examining 0" whose check prints `EXAMINED: <n>` with n > 0. **4 of 12 today** — `source_slug_links_duplicates` (9), `metadata_integrity_audit` (9), `research_protocol_audit` (28), `gap_mining_audit` (5). Same for quarantine reasons: `code_currency_audit` says "RED" and exits 0; `adjudication_integrity` says "1 of 5" and reports 9 of 9. A `lapses_when:` key, or `measured_at:` + `measured:` with a drift warning, is **v2** | **v1 (this shape) / v2 (general)** | **N4** |
| **L0.9** | CLAUDE.md states no volatile fact, and its derivations still run | `claude_md_spine` (blocking) already renders the SPINE from `governance/pipeline-contract.yaml` — invoke it. Add two things. (a) `\b\d{2,}\b\s+(rows\|tables\|checks\|sources\|views)` → FAIL unless the sentence also contains "derive". (b) **Extract every fenced shell command in CLAUDE.md and run it**, reporting one that produces empty output. **§7's prefix derivation is broken today**: it greps `references/part04-item-index.md`, which does not exist | **v1** | rule 7 |
| **L0.10** | The write-path audits keep their scope honest | **Invoke `scripts/audit/db_path_env_audit.py` (0.45 s, 46/48 + 2 documented exemptions) and `scripts/audit/readonly_db_open_audit.py` (0.67 s, 35/35), do not re-specify them.** Print their `EXAMINED` and exemption lines verbatim. **State what they do NOT cover**, because that is the diagnostic value: writers (excluded by construction), the target table or column of a write, a `WRITABLE_TABLES` bypass, whether `PRAGMA foreign_keys` is on, Python embedded in YAML (`.github/workflows/resolve-dois.yml:69`), and SQL written in skill prose | **v1** | N5 |

### 4.3 Known false positives

- **L0.1's dual-purpose generators.** `tools/pipeline_completeness.py` and `tools/evidentiary_audit.py`
  are both a generator and a `--check`; `scripts/regenerate_derived.sh:15,16` calls the generator
  half and `:20,21` the `--check` half. 8 of the 10 hits are this. The `# meta:l0.1-ok` marker
  clears them without weakening the detector.
- **L0.9's number scan** will hit dates, migration numbers, `user_version`, section numbers and
  `1200 mm`. Restrict the pattern to a digit run **followed within 3 words by** a countable noun,
  and exempt any line inside a fenced block. Expect to tune this one; it is the least reliable
  edge in the family and should ship at report-only.
- **L0.8's "examining 0" match** must read the `no_floor` string only, never the entry's other
  prose. Several `floor_basis:` fields legitimately quote a historical figure while explaining that
  it is historical (`check-registry.yaml:163`).

### 4.4 What `l0.py` cannot catch

- **Whether a check is USEFUL.** No script scores that. The findings document dropped this
  requirement and it stays dropped.
- **Whether a check's verdict is CORRECT.** L0.5 proves a check can fail on a mutilated corpus. It
  cannot prove the check fails on the right corpus, and `--falsify`'s DROP/DELETE injection is
  crude: a check that opens the DB and exits before querying passes DROP injection.
- **A check that is red for a reason nobody has read.** 8 advisory failures are standing on `main`
  today. `l0.py` counts them; it cannot tell a backlog from a defect.
- **CI-only behaviour.** `check_commit_msg` runs on **push events only** (`ci.yml:253-266`) and is
  skipped on every PR. `l0.py` can read that condition out of the workflow YAML — it does not
  simulate GitHub's event model, and must not claim to.

---

## 5. `l2.py` — *can this stage's sanctioned tools put a row in the tables it owns, and ship it?*

Layer 2 is *"each stage in the pipeline including its tools/workflows/processes/scripts"* and it is
*"reserved for actual project materials"*. So `l2.py` asks two things: is the capture path whole,
and is anything here not stage work.

### 5.1 Per-stage invocation

```
python3 scripts/meta/l2.py --stage evidence
```

Stage ids come from `governance/pipeline-contract.yaml` `stages[].id`, never from a second list.
The spine is `base -> research -> evidence -> judgment -> synthesis -> specification -> render`,
and `claude_md_spine` already proves that line is a rendering of the contract — `l2.py` asserts
`--stage` against the contract and refuses an id that is not in it, naming the seven.

### 5.2 Worked example

```
$ python3 scripts/meta/l2.py

L2  stage tools and the capture path            22 writable tables · 47 db.py verbs
────────────────────────────────────────────────────────────────────────────────────
 L2.1  db.py write target in WRITABLE_TABLES   MISS   7 of 25   --edge L2.1
              bpc_metadata            db.py:2184,2193
              conflicts               db.py:701,725
              connection_targets      db.py:122,751
              connections             db.py:118,134,752
              gap_mining              db.py:3197
              item_audit_runs         db.py:774,805
              supersession_check      db.py:3155
       => a session writing any of these to a scratch DB emits "no delta"
          and loses the rows silently. Seventh occurrence of this blindness.
 L2.2  WRITABLE_TABLES entry has a verb        MISS   3 of 22
              convergence_assessment, specifications, specification_source_links
              (all three are also L1.7 UNWRITABLE — one defect, not two)
 L2.3  every writer refuses the canonical DB   MISS   2 off-path writers
              audit_consolidator.py:248  raw connect(str(DB_PATH)) read-write
                                         UPDATE item_audit_runs at :270
              resolve_dois.py:597        UPDATE evidence_sources
 L2.4  every verb has an instructional caller  MISS   14 of 47   --edge L2.4
 L2.5  no apparatus tenanted at L2             MISS   6 registry entries (= L0.6)
 L2.6  stage attribution                       N/A    no stage map exists — see §8
────────────────────────────────────────────────────────────────────────────────────
 EXAMINED: 47 verbs, 25 write targets, 22 writable tables    UNPARSED: 0
```

### 5.3 Edges

| # | Requirement | Mechanical detector | v | Catches |
|---|---|---|---|---|
| **L2.1** | Every table `db.py` writes is in `dbcore.WRITABLE_TABLES` | The P1/P2 AST pass over `scripts/db.py`, verb regex `INSERT (OR x)? INTO \| REPLACE INTO \| UPDATE (OR x)? \| DELETE FROM`. Compare against `dbcore.WRITABLE_TABLES` (import it — it is the one home). **7 absent today, verified twice.** `WRITABLE_TABLES` replays in FK order, so also assert every FK parent in the list precedes its child — `terms` before `term_adjudications` was a real near-miss | **v1** | **N1** |
| **L2.2** | Every table in `WRITABLE_TABLES` has a verb that writes it | The inverse of L2.1. **3 today**, and all three are the same defect as L1.7: they were added to the capture path in anticipation of migration 071, and their FK parents are empty. Cross-reference L1.7 in the output and say so, rather than reporting two separate failures | **v1** | 3 |
| **L2.3** | Every writer refuses the canonical DB and passes through the sanctioned path | `dbcore.connect()` already refuses (`dbcore.py:97-125`, no override). Detector: AST-find `sqlite3.connect(` call sites that are **not** in `dbcore.py`/`migrate_db.py` and whose argument is not a `mode=ro` URI, then check whether the enclosing file also contains a write verb from L2.1's regex. **2 today**, both confirmed. `readonly_db_open_audit.py` explicitly excludes writers, so this is the half it does not cover | **v1** | **N5** |
| **L2.4** | A verb the project relies on is named somewhere a session will read | 47 verbs from `add_parser(...)` in `db.py`; instructional surface = `grep -rhoE 'db\.py [a-z0-9-]+'` over `skills/ governance/ references/ decisions/ workplan/ specs/ architecture/ CLAUDE.md`. **14 orphans today.** **Print the search roots in the output** — the count moves when the roots move, which is how the findings document got 17 | **v1, report-only** | **N6** |
| **L2.5** | No apparatus is tenanted at Layer 2 | Same detector as L0.6, reported from the stage side so `--stage render` shows that `site_pages_fresh` and `evidentiary_audit_fresh` are render-stage tenancy failures | **v1** | 2026-09-10 ruling |
| **L2.6** | Each stage's tools and tables are attributable to that stage | **v2 — the blocker for everything per-stage.** See §8 | **v2** | — |
| **L2.7** | Every emitted batch reaches a migration | `scripts/research/emit_batch_sql.py` → `scripts/emit_data_migration.py` → `scripts/migrations/data_*.sql`. Detector: for each table in `WRITABLE_TABLES`, grep `scripts/migrations/data_*` for an INSERT naming it. A column that a committed data migration INSERTs **can never be dropped** (CLAUDE.md rule 5), so this doubles as the pre-drop check the rule demands | **v1** | rule 5 drop-order |

### 5.4 Known false positives

- **`add-item` is an orphan by design.** It refuses on every call, because the item layer was
  deleted on 2026-09-01 and a container that announces its answer biases every finding filed into
  it. L2.4 must carry a suppression list keyed on "the verb's body raises unconditionally", which
  is AST-detectable: a function whose first statement is a `raise`.
- **A verb named only in `_archived/`.** `.ignore` hides `_archived/` from ripgrep and the Grep
  tool but not from `grep -r`. L2.4 uses `grep -r`, so a verb documented only in archived content
  will read as named. **Report the matching path** so the reader can see the citation is archived.
- **The naive write-target regex** returns `a`, `after`, `an`, `connection`, `it`, `search`,
  `that`, `was`. §2.5 P1 exists for this edge specifically.

### 5.5 What `l2.py` cannot catch

- **Whether the stage's work is any good.** It measures whether a row can be written and shipped,
  not whether it should have been.
- **Hand SQL.** A session that writes SQL by hand against a scratch copy leaves no Python for the
  AST to read. `emit_data_migration.py`'s `ENUM_GUARDS`/`RANGE_GUARDS` are the only screen on that
  path, and they cover **3 columns** of the 108 with a closed vocabulary.
- **SQL inside YAML or shell.** `.github/workflows/resolve-dois.yml:69` embeds Python; the AST pass
  reads `.py` files only. Report the count of YAML files containing `sqlite3` as an
  `UNPARSED` line rather than pretending the surface is fully read.
- **Whether a stage's *workflow* ran.** Freshness is what the four `*_fresh` checks do, and they
  are themselves L0.6 tenancy failures.

---

## 6. `l3.py` — *is every row the product of that path, and does it stay in its own stage?*

Layer 3 is *"the actual data being recorded in the tables"*.

### 6.1 Worked example

```
$ python3 scripts/meta/l3.py --subject evidence_sources

L3  evidence_sources                                         9 rows      2026-09-10
────────────────────────────────────────────────────────────────────────────────────
 L3.1  columns with a vocabulary, all NULL   MISS   scope            9/9 NULL
                                                    => derive_tier() cannot run
                                                    for any row in the corpus
 L3.2  audit stamps present                 OK     created_by_session 9/9
 L3.3  reproducible from migrations         N/A    EXEMPT — evidence_source_authors
                                                    and pipeline_runs are in
                                                    migration_reproducibility.EXEMPT_TABLES
 L3.4  no orphan FK                         OK     PRAGMA foreign_key_check: 0 rows
 L3.5  stage tenancy of each column         N/A    no stage map — see §8
────────────────────────────────────────────────────────────────────────────────────
 VERDICT  1 BROKEN EDGE — L3.1 scope. Repaired writer, unrepaired corpus:
          `--scope` landed 2026-09-10; the 9 rows were admitted before it.
 EXAMINED: 9 rows, 97 columns, 6 edges
```

### 6.2 Edges

| # | Requirement | Mechanical detector | v | Catches |
|---|---|---|---|---|
| **L3.1** | A column with a declared vocabulary is not uniformly NULL | For every column carrying a CHECK (both forms — §2.5 P2 and L1.3b), `SELECT COUNT(*), COUNT(col) FROM t`. `COUNT(col) = 0` on a non-empty table is the shape of defect 1: Layer 1 declared a vocabulary, Layer 2 produced nothing. Report `n/m NULL` and, when the column feeds a derivation, name the derivation | **v1** | **1** |
| **L3.2** | Every row carries its audit stamps | `created_at`, `created_by_session`, `updated_at`, `updated_by_session` non-NULL where the column exists. `dbcore.audit()` is the one home of the stamp | **v1** | provenance |
| **L3.3** | The committed blob is reproducible from the migrations | **Invoke `scripts/audit/migration_reproducibility.py`, do not re-implement.** State its limits inline every run: it compares **row COUNTS only**, so an UPDATE is invisible; `--deep` compares every row and is **advisory**; and **`EXEMPT_TABLES` holds two names, `pipeline_runs` and `evidence_source_authors`** — the second is the table the 2026-08-19 fabrication happened in | **v1** | rule 3 |
| **L3.4** | No orphan foreign key | `PRAGMA foreign_key_check` (empty today) plus a dangling-target scan: an FK naming a table that does not exist in `sqlite_master`. **0 today**, and the scan is 0.02 s, so it stays in the default path | **v1** | 064-class |
| **L3.5** | A stage's table holds only that stage's facts (rule 5) | **v2.** Requires the stage map. §8 | **v2** | 5 |
| **L3.6** | Row counts quoted in derived documents match the DB | Parse `parts/`, `site/`, `audits/`, `tools/*.html`, `index.html` for `<n> (rows\|sources\|items\|specifications)` and compare against a live count. **Report-only** — the mapping from an English noun to a table is a guess | **v1, report-only** | failure mode (b) |

### 6.3 Live state that `l3.py` reports today, for calibration

**30 of 70 tables hold rows.** The 40 empty ones are not all the same kind of empty: `items`,
`base_parameters`, `case_studies` and `economics_entries` are **roots** whose emptiness makes 22
columns across 22 tables unwritable (L1.7), while `term_adjudications` is empty beside `terms` at
88 rows — a writer that mints both in one act has not been the source of those 88.

### 6.4 What `l3.py` cannot catch

- **A fabricated value.** Every one of the 2026-08-19 author rows was populated, well-formed,
  correctly stamped and false. Six gates passed it because each asked whether the field was
  *populated*, never whether it was *true*. **Verification must leave an artefact**:
  `scripts/research/retrieval_log.py --verify-authors` diffs stored rows against the bytes actually
  received, and it is the only thing here that can answer this question. `l3.py` prints a banner
  naming it and does not pretend to substitute for it.
- **An UPDATE to the canonical blob.** `migration_reproducibility` compares counts; `l3.py` inherits
  that floor exactly and says so.
- **Semantic drift inside a valid vocabulary.** A `scope` of `national` where `international` was
  meant passes every edge here.
- **Whether the row belongs to this stage.** That is L3.5 and it is v2.

---

## 7. `l4.py` — *is any supplementary artefact being read as if it were canonical?*

Layer 4 is *"supplementary data"*. It sits outside the ensure-chain, so its meta-script asks the
inverse question: not "does it work" but "is it being mistaken for the thing that does".

The failure this exists for is stated in CLAUDE.md §7 and is live: **the item layer is gone from the
database and still on the reading surface.** `items` holds 0 rows and a rebuild does not restore it,
yet the prior corpus still publishes the codes and their names. A session that greps for a topic
meets `E-08 Corridor Clear Width (>=1200 mm Minimum on All Primary Routes)` — a container whose name
states its answer — and files into it.

### 7.1 Worked example

```
$ python3 scripts/meta/l4.py

L4  supplementary data read as canonical                                  2026-09-10
────────────────────────────────────────────────────────────────────────────────────
 L4.1  L4 path read by an executable        MISS   0 literal-prefix reads, but 25
                                                   segment-joined sites; 3 notable:
              context_map.py:59   labels `references` "canonical" in a
                                  GENERATED map — L4 declared L3
              register_integrity_check.py:42  a registered check whose DEFAULT
                                  subject is under _archived/working/pilot/
              validate_schema.py:286  schema validator reads
                                  _archived/data/jurisdictional_values
 L4.2  prior-version codes on live surface  MISS   130 files, 17 prefixes
                                                   A E F G H D B I C K T V M J S O L
                                                   top: A(796) E(551) F(433) G(430)
                                                   H(384) D(379) B(318)
                                                   88 of the 130 carry NO
                                                   prior-version banner in their
                                                   first 5 lines (42 do)
 L4.3  the derivation in CLAUDE.md runs     MISS   `grep ... references/part04-item-
                                                   index.md` -> file does not exist
                                                   CLAUDE.md §7
 L4.4  .ignore claims match reality         OK     versions/ hidden (.ignore:106);
                                                   references/ working/ index.html
                                                   NOT hidden, as §7 states
────────────────────────────────────────────────────────────────────────────────────
 VERDICT  3 BROKEN EDGES. The surface is wider than "A-E": derive, never assume.
 EXAMINED: 130 files, 27 executables, 4 edges
```

### 7.2 Edges

| # | Requirement | Mechanical detector | v |
|---|---|---|---|
| **L4.1** | No executable reads a Layer 4 path as a source of truth | **Two patterns, and the literal one alone is useless: it finds 0 sites.** (a) a string literal starting `references/`, `working/`, `retrieval-log/`, `misc/`, `versions/`, `_archived/` passed to `open`/`read_text`/`glob`/`rglob`; (b) **a bare segment** — `"references"`, `"_archived"`, `"versions"`, `"working"`, `"retrieval-log"` — appearing as an argument to `os.path.join` or an operand of `Path.__truediv__`. Pattern (b) finds **25 sites**. Exclude a gate reading its own corpus (`validate_bpc.py:239`, `validate_reasoning.py:31-32`, `pre_rehab_banner_audit.py:29`, `adherence_log_audit.py:73`) — that is the point of those gates | **v1** |
| **L4.2** | Every `[A-Z]-NN` code on the live reading surface is labelled prior-version | Derive the prefix set from the surface, never from a list: `grep -rhoE '\b[A-Z]-[0-9]{2}\b' references/ working/ index.html \| cut -c1 \| sort -u`. **17 prefixes, 130 files today.** Then require each such file to carry a prior-version banner in its first 5 lines: **88 of the 130 do not** (matching on `prior[- ]version\|superseded\|archiv\|historical\|RETIRED\|pre-rehab`). `_archived/` needs no banner — its path is its label, which is the whole and only benefit of archiving | **v1** |
| **L4.3** | Every derivation command in CLAUDE.md still runs | Extract fenced shell from CLAUDE.md, run it, report empty output. Shared with L0.9 — implement once in `metacore.py` | **v1** |
| **L4.4** | `.ignore` hides what it claims to hide, and nothing more | For each pattern in `.ignore`, confirm ripgrep misses a planted token there and `grep -r` finds it. CLAUDE.md §7's bullet on `versions/` was wrong until 2026-09-09; this is the check that would have said so | **v1** |

### 7.3 Known false positives

- **`[A-Z]-NN` also matches live identifiers.** `T-01`, `V-12` and similar appear in tier and
  version notation. The counts above (`T` 57, `V` 22, `S` 2, `O` 1, `L` 1) are dominated by these.
  **Do not filter them out** — print the per-prefix count and let the reader judge, because the
  moment the script decides which prefixes are "real" it has hard-coded the thing CLAUDE.md tells
  you to derive.
- **A dict key or a YAML field named `references`.** `pipeline_contract_audit.py:211-212` builds a
  fixture containing `"references": "r"` — the contract's own field name. Pattern (b) must require
  the segment to be an argument of a path join, never any string equal to the word. Same class as
  the `population_code` local variable the 400-char-window detector reported.
- **`sessions/`, `audits/`, `versions/`, `_archived/` and the JSONL under `transcripts/` are hidden
  from ripgrep and the Grep tool by `.ignore`.** `l4.py` must use `grep -r` or `git grep`
  throughout, and must print which tool it used. **Never report a ruling absent from a search that
  could not have seen it** — owner rulings live overwhelmingly in `sessions/`.

### 7.4 What `l4.py` cannot catch

- **A code that is meant.** Some `[A-Z]-NN` references are legitimate historical citation. The
  script counts the surface; a human decides.
- **A reader that is a person.** The whole failure mode is a session reading `references/` and
  believing it. No script detects that. `l4.py` measures the size of the hazard, not its use.

---

## 8. The single v2 blocker: there is no stage map

`--stage` is specified for `l2.py` and `l3.py` because the owner asked for the per-stage breakdown,
and **v1 cannot deliver it.** This was measured, not assumed:

- `governance/pipeline-map.yaml` was the old table-to-stage bucketing. It was archived to
  `_archived/governance/` on 2026-09-09 and **its bucketing predates the seven-stage spine**, so it
  is not a substitute even if unarchived.
- Deriving stage from "which stage's checks read this table" — the only route available with zero
  new files — was implemented and run. **It attributes 17 of 89 tables and views (19%), of which
  only 12 are unambiguous.** It puts `evidence_sources` in four stages at once
  (`evidence, render, research, specification`) and `items` in four. That is not a map; it is noise.
- The contract's `stages[].criteria[]` gives a stage→*criterion* map and the registry's
  `basis: <stage>/<criterion>` gives check→stage for **28 of 67** checks (22 more declare `basis: unattributed`). **Both are v1 and both are
  already used above.** Neither says which stage owns a table.

**What must be built first:** `governance/stage-map.yaml`, one entry per table and view naming its
stage id from `pipeline-contract.yaml`, with a `pointer:` list for cross-stage views. It is one
file, ~89 lines, and CLAUDE.md §3 already states the rule it encodes: *"Derive any table-to-stage
assignment against these seven stages; every assignment written before 2026-08-27 predates them."*

Until it exists, `--stage` is accepted and answers:

```
$ python3 scripts/meta/l3.py --stage evidence
L3  stage `evidence`
  STAGE ATTRIBUTION UNAVAILABLE — no table-to-stage map exists.
  17 of 89 objects are weakly attributable via check basis; 12 unambiguously.
  Build governance/stage-map.yaml. Running stage-agnostic instead:
  ...
```

**A wrong stage map is worse than none** — rule 5 is unusable without knowing which stage a table is
in, and a confident wrong answer is how a pointer gets deleted as a copy.

### 8.1 The complete v2 register

| Needs building | Unlocks | Edge |
|---|---|---|
| `governance/stage-map.yaml` — table/view → stage id, with `pointer:` for cross-stage views | per-stage L2 and L3; rule 5 mechanically | L2.6, L3.5, L1.8 |
| `object:` on contract criteria (`schemas/pipeline_contract.py` is `extra="forbid"`, so the model must change first) | a criterion pointed at a retired object becomes checkable | L1.9, defect 6 |
| `subject:` on registry entries | `kinds` can be checked against what the check actually looks at | L0.4 |
| `falsified_by: {selftest: true}` or `none — <reason>` on registry entries | falsifiability for file-subject checks, which fault injection cannot reach | L0.5 |
| `lapses_when:` (or `measured_at:` + `measured:`) on any registry prose carrying a number | rule 7 generally, instead of the one hard-coded "examining 0" shape | L0.8 |
| `governance/dual-homes.yaml` | rule 5 — a declared dual home with a retirement plan, versus a parity check that makes it permanent | L1.8 |
| `unclaimed:` allowlist with a per-id reason | C7's INFO becomes a verdict | L0.7 |

**None of these is a prerequisite for shipping v1.** Every v1 edge above runs against the repo as
it stands on 2026-09-10.

---

## 9. What none of the five can catch — read this before trusting any of them

**A tool trusted past its reach is worse than no tool.** Four limits apply to the whole family.

1. **Prose callers are invisible by construction.** English instructions in skills, DRs, runbooks
   and CLAUDE.md itself are the only callers some scripts have. This nearly caused three wrongful
   deletions in one session. **Every script prints the banner; no script is authority for a
   deletion.** An object with zero detected callers is UNPROVEN, not dead.
2. **Truth is out of scope.** These measure whether an edge resolves. A fabricated citation, a
   plausible wrong number, a scope value that is valid and mistaken — all pass every edge here. The
   only apparatus in this repo that touches truth is `retrieval_log.py --verify-authors`, and it
   works by diffing against bytes actually received.
3. **A 0-row object is unproven, not clean.** Every count printed is a count of what exists now.
   `v_item_provenance` passed a byte-exact diff because it rendered 0 rows, and migration 064 exists
   because of it.
4. **The scripts themselves are Layer 0 apparatus and are subject to their own edges.** `l0.py`
   must include `scripts/meta/*.py` in its own tenancy scan, and the tenancy prefix table in L0.6 is
   a hand-written claim with no lapse predicate — exactly what L0.8 exists to flag. It fails closed
   (any unmatched path is `UNCLASSIFIED`) precisely because it cannot be trusted to stay current.

**And a standing caution about the corpus.** The content is barely started: 9 evidence sources,
30 of 70 tables holding rows, 40 empty. Most edges here will report small numbers or VACUOUS for
some time. **VACUOUS is not PASS** — `run_checks.py` already makes that distinction and escalates
blocking-and-vacuous checks, and these scripts inherit the rule. A meta-script that examined
nothing has diagnosed nothing.

---

## 10. Build order

1. **`l1.py` L1.2 and L1.7.** Ten lines each, sub-second, and they answer "why can I not write a
   row" — the question the repository actually blocks on today.
2. **`metacore.py`'s P1–P6 SQL pass.** Everything else is a consumer of it.
3. **`l1.py` L1.1, L1.3b, L1.11.** The founding-defect family.
4. **`l2.py` L2.1–L2.3.** The capture path, which has now failed seven times by the same mechanism.
5. **`l0.py` L0.2, L0.6, L0.8.** Two of the three are a parse of existing output.
6. **`l4.py`.** Cheap, and the hazard it measures is live.
7. **`l3.py`.** Least urgent while the corpus is 9 rows, and most valuable the moment it is not.
8. **`governance/stage-map.yaml`**, then the v2 edges.
