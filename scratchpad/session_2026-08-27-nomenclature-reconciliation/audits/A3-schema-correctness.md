# A3 — Schema correctness and best practice: NOMENCLATURE.md Parts B/D/E/I/K/L and the 2026-08-27 RULEs

**Adversarial audit, 2026-08-27.** Lens: would the proposed schema and migration mechanics actually
work as written. Every figure below is measured against `data/guidebook.db` (`user_version` 64,
SQLite 3.45.1, `legacy_alter_table` 0) or tested on a scratch DB under the session scratchpad; no
tracked file and no canonical DB was touched.

**Verdict up front.** The hand-off keys are the right idea with two wrong placements and one
unenforceable clause; the baseline plan's conclusion is defensible but two of its three supporting
arguments are measured false and its procedure, followed as written, turns the blocking
`migration_reproducibility` gate red on its first run. Neither is sound *as written*.

---

## 1 · The hand-off keys (Part B, Part E, the `<stage>_items` RULE)

### F1 — BLOCKER. Part E specifies the key shape Part B rejects, for both fan-in stages.

Part B and the RULE are explicit: judgment→synthesis and synthesis→specification are **junctions**,
because "a hand-off column can only express the fan-out half" and a back-pointer column would
"forbid one judgment feeding two syntheses." Two sections later, Part E writes the opposite:

- Part E §4, `bpc_metadata` → `syn_items`: "**Gains `judgment_item_id NOT NULL`**"
- Part E §5, `specifications` → `spe_items`: "**gains `synthesis_item_id NOT NULL`**"

A `NOT NULL judgment_item_id` **on `syn_items`** pins each synthesis to exactly one judgment —
contradicting the owner cardinality ("one-to-many rows of judgment provide one row for syntheses")
that the same document quotes as the reason for the junctions. Part E is the table a
migration-writer will transcribe DDL from; as written it produces the wrong schema for stages 4–5.

**Failure scenario:** the executing session builds the migration from Part E's per-table notes,
ships `syn_items.judgment_item_id NOT NULL`, and the first multi-judgment synthesis is unwritable —
or is written by duplicating the synthesis row per judgment, which inverts the fan-in.

**Smallest fix:** strike the two "gains … NOT NULL" notes in Part E §4/§5 and replace with "junction
per Part B". The only NOT NULL hand-off *columns* are `evi_items.research_item_id` and
`jud_items.evidence_item_id`.

### F2 — BLOCKER. "≥1 required per synthesis" has no enforcer, and the proposal names none.

SQLite cannot declare "a parent must have at least one child":

- an FK enforces the other direction (junction row → existing parent);
- a CHECK cannot read another table;
- there are no deferred cross-table constraints or assertions;
- a trigger `AFTER INSERT ON syn_items` fires **before** any junction row can exist, because the
  junction is written by the downstream stage after creating its item — the proposal's own write
  order guarantees the trigger sees zero links.

So a `syn_items` row with zero `syn_judgment_links` is representable, permanently, and nothing in
the migration prevents it. The table in Part B/the RULE presents "≥1 per synthesis" as if it were a
property of the junction. It is not a property of anything proposed.

**Failure scenario:** a synthesis is committed in one transaction, the session dies before the
links land, and the spine — the entire point of the exercise — has a silent gap that every
"the walk now walks" claim rests on.

**Smallest fix:** name the two enforcers in the proposal: (a) a transactional writer —
`db.py add-synthesis` takes `--judgment-items REF…` and **refuses** to write the item without ≥1,
inserting item and links in one transaction (none of `add-extraction`, `add-synthesis`,
`add-specification` exists today; the parser list in `scripts/db.py` confirms it); (b) a blocking
registered check scanning for `syn_items`/`spe_items` rows with zero links, printing `EXAMINED:`
per §2(a). DDL alone cannot carry this invariant.

### F3 — MAJOR. `evi_items.research_item_id` puts a per-source fact on a per-extraction row — a rule-5 violation that can disagree with itself.

The lead→paper edge is **source-grained**: one clue-store row produced one admitted document. An
extraction is a row *about that document*. Putting `research_item_id NOT NULL` on
`source_value_extractions` copies the same fact into every extraction from the same `ref_id`, and
nothing constrains two extractions from one paper to agree — extraction 1 from REF-00931 can name
lead A while extraction 2 names lead B, and both pass every FK. That is "the same fact written into
a second table," N times, with divergence representable.

And the NOT NULL is not free in the direction that matters. Measured: **six admitted sources have
no clue-store row** (`REF-00965`–`REF-00970`). Any extraction from them is unwritable under the
proposed key. The only escapes are (a) refusing to extract from admitted evidence, or (b)
backfilling pseudo-leads after the fact — retroactive provenance, which is the §2(c) fabrication
class with better paperwork. Part I.5's "resolve or record as legacy" is not a mechanism: a NOT
NULL column admits no "legacy" NULL.

Note also that J.4's claim that `search_admissions` becomes redundant ("once
`evi_items.research_item_id` names the lead and the lead names its search") is built on this
misplaced edge — it only holds if the extraction, rather than the admission, carries the lead.

**Smallest fix:** hang the NOT NULL lead key on the **admission** — `evi_sources.research_item_id`
(or the admission junction) — keep the existing `extraction.ref_id → evidence_sources` FK, and
reach the lead from an extraction by join. Backfill the six no-lead sources with
`origin='hand-entered'` lead rows in the same migration, declared as legacy in its header. This
still satisfies the owner's RULE (the hand-off is a NOT NULL FK; the stage still hands off through
its items via the pointer chain) without the copied fact.

### F4 — MAJOR. `res_items` = `source_locators` reverses a ratified demotion nothing supersedes.

Migration 062's header, carrying DR-2026-08-06: the clue store is *"not stored as usable for any
case unless it is being read by a researcher"* — *"Nothing joins it, no determination may cite
it."* The proposed spine makes it the **root of every citation walk**: `evi_items.research_item_id
NOT NULL` means every future determination transitively resolves to a REFERENCE-ONLY clue row —
875 rows whose `recovered_from` defaults to `'corpus-pre-reset-2026-08-06'`, the corpus whose
bibliographic fidelity is exactly what failed in §2(c). The proposal never mentions the conflict.

The 2026-08-27 `-item` ruling does not resolve it either: the owner named the stage's hand-off
object; the *identification* of that object with `source_locators` is this document's derivation,
and it collides with a ratified record. Under rule 0 that needs a recorded supersession, not
silence.

**Failure scenario:** either the key ships and the DR's wall is breached silently (unverified clue
bibliography becomes joinable provenance), or a later session greps the DR, quotes "nothing joins
it," and refuses the migration — both outcomes from the same unrecorded contradiction.

**Smallest fix:** one paragraph in the supersession record distinguishing what becomes joinable
(the lead's *identity*, as provenance-of-discovery) from what stays non-citable (the lead's
bibliographic fields), plus a writer refusal: admission PROMOTEs the lead
(`status='PROMOTED'`) before anything downstream may reference it.

### F5 — answered directly, for the record

- **Is the NOT-NULL-is-free claim true?** At DDL time, yes: `source_value_extractions` holds 0
  rows and the 875 `source_locators` rows are parents, which cost nothing. Tested on 3.45.1:
  `ALTER TABLE … ADD COLUMN x TEXT NOT NULL REFERENCES …` succeeds on an empty table, with FK ON
  or OFF. The cost is semantic, not mechanical — F3's six no-lead sources.
- **Insertion order / circularity:** none. Junctions are written by the downstream stage after its
  item exists; `res_items.parent_item_id` is a nullable self-FK; `source_locators.ref_id` is
  `TEXT PRIMARY KEY` (verified — a legal FK target, all 875 distinct, none NULL).
- **`jud_items.evidence_item_id` NOT NULL, not UNIQUE:** legal and right for the dissent case. But
  nothing distinguishes a dissent row from an accidental duplicate — the `add-population-match`
  precedent pairs the missing UNIQUE with a writer; `jud_items` needs a discriminator column
  (pass/grader) and a writer refusal on exact duplicates, neither proposed (F.1 must cover it).

---

## 2 · The baseline-rebuild claim (Part I)

### F6 — BLOCKER. The procedure as written turns the blocking `migration_reproducibility` gate red on its first run.

`scripts/audit/migration_reproducibility.py` hardcodes its seven invariants:
`CORE_INVARIANTS` includes `SELECT COUNT(*) FROM items`, `… FROM citation_mining`, `… FROM
connections` — **all three retired or renamed by Part E**. After the baseline, the blocking gate
throws `no such table: items` against both the committed and the rebuilt DB, on every run, until
the script is rewritten. Its own selftest hardcodes `items` in six places. The list is annotated
*"Keep this list and the DR in sync; it is the contract"* — so the sweep is a contract/DR change,
not a grep-and-replace.

Part G's caller list — views, `db.py`, `dbcore`, `schemas/`, pipeline-contract,
`pipeline_completeness.py`, check-registry `basis:` refs, skills, `data_*` — **omits it**. It also
omits every generator: `build_site.py` (`FP_TABLES` names five of seven tables being
renamed/retired, and `build_specs` walks `SELECT item_code FROM items`), `spec_page.py`,
`population_page.py`, `generate_parts.py`, and the `tools/` audit writers. This is precisely the
064 failure class the document cites as its cautionary tale, being re-armed by the document.

**Smallest fix:** add `scripts/audit/migration_reproducibility.py` (+ its contract DR),
`scripts/generate/*`, and `tools/*` to Part G's sweep list by name.

### F7 — MAJOR. Part I omits the runner edit that 057's own header names as part of the mechanism.

`BASELINE_DATA_CUTOFF_TS = "20260812083255"` is a **hardcoded constant in `migrate_db.py`**, and
057's header lists moving it as an explicit step. A new baseline requires (a) moving the 33 live
`data_*.sql` files to `_archived/` — I.6 covers this — **and** (b) moving the constant past
`20260825215123`. Part I claims "nothing new has to be invented" but never mentions that the
mechanism includes editing the runner. If missed: the guard the constant exists for is dead — any
of the 33 archived files restored by mistake replays onto a baseline that already contains its
rows, and its ledger `INSERT` hits the `data_migrations` PK the baseline baked in; rebuild exits 1
and the failure surfaces as a mystery, which is the exact anti-pattern the runner's comments warn
about.

Also unstated: the runner applies **schema** migrations with `fk_blocking=False` — a baseline's FK
violations are *advisory stderr*, not failures. 057 compensated with an out-of-band 0-diff
verification. A transforming baseline (F8) cannot repeat that verification, so its FK integrity
rests on nothing but the author's care.

### F8 — MAJOR. "Exactly the way `057_baseline` was made" is false: 057 was content-preserving; this baseline transforms.

057's entire verification story was identity: *"0 sqlite_master differences either direction, 0
row-count divergences, 0 content divergences row-by-row"* against the pre-baseline committed DB.
The proposed baseline renames 66 tables, moves 6 across stages, re-keys `specifications`, retires
`items` (93 rows, 10 inbound FKs re-pointed), fans MOB 31→62, possibly re-mints 288 `AX-` cells,
and creates three stages clean-sheet. **There is no identity to verify.** Every transformed row is
hand-written SQL that passes through no refusing writer — §4's "do not hand-write SQL against a
table the CLI can reach" applies to the baseline's body more than anywhere else, and the 2026-08-19
fabrication entered through exactly this gap. Worse, transforms executed inside a schema baseline
produce **no `data_migrations` ledger rows** — the fan-out and the re-mint become acts invisible to
the project's own record of acts. I.6's "do not lose the ledger" guards the 352 old rows and misses
that the new acts never enter it.

**Smallest fix:** land every data transform first as ordinary `emit_data_migration.py` files — MOB
fan-out, the `AX-` decision's data half, the six-lead backfill — each with its own ledger row and
header; then cut a **content-preserving** baseline over the result, verifiable exactly as 057 was.
The baseline then carries only DDL shape (renames, keys, clean-sheet stages) plus a byte-faithful
data load.

### F9 — MAJOR. The "sixty-six rebuilds" necessity argument is measured false; the incremental path is also one migration.

Tested on this container's SQLite 3.45.1 with `legacy_alter_table=0`, under the runner's own
execution state (`PRAGMA foreign_keys=OFF`, inside `BEGIN IMMEDIATE`):

- `ALTER TABLE parent RENAME TO res_items` **rewrote the child table's REFERENCES clause and the
  view body automatically** (`REFERENCES "res_items"(id)`; the view joined `"res_items"`), and DML
  plus `foreign_key_check` were clean afterwards.
- `ADD COLUMN … NOT NULL REFERENCES …` succeeds on an empty table.
- `RENAME COLUMN` and `DROP COLUMN` are both available at 3.45.

So the incremental path is ~60 one-line renames, two ADD COLUMNs, three junction CREATEs, and a
create-copy-swap for only the genuinely re-keyed tables (`specifications`, `bpc_metadata` — see
F10) — **3–5 rebuilds, not 66**. The replay-collision argument is real (14 live data migrations
name `source_locators`, 19 name `evidence_sources`, 9 name `items`) but a single
`-- AFTER_DATA: 20260825215123` marker on the rename migration orders it after all 33 — the
mechanism 057's own header calls *"the documented escape for the next rename that collides with
replay."* Citing AFTER_DATA's creation cost as a reason to avoid the path it now makes free is
arguing from a bill already paid.

One inversion worth stating: **the incremental path is safer for the 18 views.** SQLite rewrites
every view body mechanically and provably; a baseline hand-transcribes all 18 — eighteen chances
at the `v_item_provenance` error that cost migration 064, on 0-row objects where a byte-diff
proves nothing (§0.4's own trap). The baseline remains a defensible *choice* — clean-sheet stage
DDL and absorbed pending work are real benefits — but I.2's claim of technical necessity does not
survive measurement, and the choice should be recorded as a choice.

### F10 — MAJOR. `syn_items` keeps PK `slug`, and both the junctions and Part J.2 break on it.

`bpc_metadata`'s PK is `slug` (verified). Part E's synthesis row is a *rename plus a column* — no
re-key. But `syn_judgment_links(synthesis_item_id, …)` then keys on a slug string, and J.2's
comparative syntheses — "same table … assign a new reference ID" — require **multiple rows per
slug**, which PK `slug` forbids outright (as does `bpc_metadata.population NOT NULL`, one
population per slug row). The first comparative synthesis, and the second primary synthesis on a
re-entered slug, are both unwritable. The re-key (minted id; slug demoted to an attribute) is a
structural change stated nowhere in Part E, Part B, or the RULE, and belongs in F.1's design debt
explicitly.

---

## 3 · `parameter_canonical` as the specification key (2026-08-26 RULE)

### F11 — MAJOR. Identity from an unregistered normalized string, with the vocabulary's shape and grain both undecided.

The RULE already concedes no CHECK, no registry, no writer. The deeper problems its
"vocabulary lands in or before the migration" remedy does not reach:

1. **Homonyms.** "clear-width" of a doorway and of a corridor are one string unless the string
   embeds context — and then it is a composite key smuggled into free text, ungreppable and
   unenforceable. Normalization ("lowercase, hyphens") lives in a code comment; nothing can verify
   that a given string *is* the canonical form of anything.
2. **No stability.** Correcting a canonical form rewrites a PK plus every junction row
   (`spe_synthesis_links`, `spe_source_links`, three cross-reference junctions) — the exact defect
   F.4 records against surrogate rowids, reproduced in text.
3. **The remedy recreates `items`.** A registry of design parameters keyed by a label, landing in
   the same migration that retires `items` for being a registry of design parameters. The
   difference (parameter grain vs Part-4 rollup grain) is real but stated nowhere; unstated, the
   retirement is a rename with extra steps.
4. **The CHECK branch of the RULE is the wrong branch.** The vocabulary constrains two tables
   (`evi_items.parameter_canonical`, `spe_items`' key). A CHECK carrying the list on each is two
   homes for one vocabulary — rule 5. Only a registry table both FK into gives it one home.
5. **Grain vs the conflicts case.** One `spe_item` per parameter cannot state divergent
   per-population determinations — and the project's own example (ramp gradient, ambulant vs
   wheeled) is an opposed demand *on one parameter*. Where the second value lives is unanswered;
   "two canonical strings for one parameter" reintroduces problem 1 deliberately.

**Smallest fix:** a substrate registry minting **stable parameter codes** (`code` PK,
`canonical_label` UNIQUE), both stages FK the code; and the spec grain decided against the
conflicts case, in writing, before the migration.

---

## 4 · The `figures` table (Part K)

### F12 — MAJOR. The design violates Part J two sections earlier, and its NOT NULL forces a rule-5 violation.

1. **`figure_links(figure_id, target_kind, target_id)` is the polymorphic key Part J forbids** —
   *"SQLite cannot key a polymorphic column"* — proposed with the compliant design demoted to a
   parenthetical ("or one junction per stage, per Part J's caution"). The junction-per-stage form
   must be the design, not the footnote; as the primary text stands, the migration-writer ships
   the unkeyable one.
2. **`derived_from` is itself polymorphic and half-unenforceable**: "the spec/view a generated
   figure computes from" mixes a row reference with a schema-object *name* in one column. A view
   rename silently orphans every generated figure; no FK can exist to `sqlite_master`.
3. **`text_equivalent NOT NULL, always` mandates a second home for the determination.** For
   `kind=generated` the text equivalent restates the value the figure encodes; stored as an
   authored row it drifts the moment the spec moves — the *exact* defect K.3 names for the image
   ("a drawn diagram showing 1200 mm beside a spec that says 1800 mm is §2(b) in pictures"),
   reproduced in the alt text. Generated figures need their text equivalent **generated by the
   same code path from the same determination**, not stored. Store (and gate) `text_equivalent`
   for `kind=asset` only.
4. **The sketch omits its own conditional constraints**: nothing stops `kind='generated'` with
   `asset_path` set, or `''` satisfying NOT NULL. Needed:
   `CHECK ((kind='generated') = (derived_from IS NOT NULL))`,
   `CHECK ((kind='asset') = (asset_path IS NOT NULL))`,
   `CHECK (length(trim(text_equivalent)) > 0)` where stored.
5. **No writer.** No `add-figure` subcommand exists or is proposed; under §4 a table without a
   refusing writer is where fabrication enters — and this is the alt-text table of an
   accessibility guidebook. The refusals write themselves: kind vocabulary from the CHECK, target
   existence per typed junction, non-empty text equivalent.
6. **No stage.** Part D's grammar makes an unprefixed table substrate, but `figures` derives from
   stage-5 output — the same substrate-pointing-downstream inversion Part E flags on
   `item_population_elaborations`. It needs a stage (render is the natural one) or an explicit
   exemption.

---

## 5 · The vocabulary check (Part L.3, as corrected at commit 8dc74bd)

*Note: L.3 was rewritten mid-audit (commit `8dc74bd`, 02:55). The original "nine of 93" count —
which this audit independently measured as wrong (28 digit-bearing names) — is corrected in place
to the instrument's ratified taxonomy: 28 numeric, 23 prescriptive, 9 overlap, **42 distinct, "a
floor"**. The count defect is therefore closed. What follows audits the check as now specified.*

### F13 — MAJOR. The check still has no implementable matcher for half its subject, sweeps columns where quantities are legitimate, and targets a table the same document retires.

1. **The prescriptive half has no mechanical form.** The corrected L.3 requires the check be
   "built against the instrument's taxonomy (numeric · prescriptive · overlap)". The numeric half
   is buildable: comparators (`≥ ≤ ±`), ranges, `n:m` ratios, and a unit/rating lexicon
   (mm, m², lux, K, dB, N, EML, GU, PTV, NRC, STC, NC, MERV…). The **prescriptive** half —
   "Minimum on All Primary Routes", "in Occupied Spaces", "One-Fist Operable" — is a clause
   grammar no document specifies, and the instrument declares its own 42 "a floor". A check whose
   matcher is unspecified against a subject whose true count is only bounded below cannot print an
   honest finding count: it will pass having examined an unknown fraction, which is §2(a)'s
   vacuous-pass defect wearing a green light. The registry entry must either scope itself to the
   numeric grammar and say so in its note, or the prescriptive matcher must be designed and
   selftest-pinned (the `retired_vocabulary_audit.py` pattern — register entries, boundary-pinned
   compiled matchers, a selftest per mode — is the house form to copy).
2. **"No label, name or description" sweeps columns where quantities are legitimate.** Measured:
   `terms.definition` has 2 digit-bearing rows (definitions of measurement concepts must state
   quantities to define them) and `axes.falsification_condition` has 5 (methodological thresholds
   — study counts, effect bounds — are its content). An unscoped check drowns; the register's own
   principle applies: *"Flagging it produces noise and teaches the reader to ignore the check."*
   The scope must be an explicit column list (identity labels: name/label columns of registries),
   not the three-word category "label, name or description".
3. **The target table is retired by the same document, and L.6's ordering hides it.** The check's
   subject today is `items.name`; Part E retires `items` outright at the Part I baseline. L.6 puts
   the check at step 2 and the baseline at step 4 — so the check is written against a table with
   weeks to live, then its subject vanishes and a blocking `min_items:1` check goes
   NOTHING-IN-SCOPE (or red) at the exact commit that lands the baseline. Written instead against
   the successor vocabulary (F11's parameter registry), its subject does not exist until step 4.
   Either order is workable; the proposal must pick one and say which table the check reads after
   the rename.
4. **Registry conventions**: implementable as a DB-walking check with `EXAMINED:` = cells scanned
   and a `min_items` floor derived from the scoped column list — but with the exemption grammar,
   the clause matcher and the retarget above, this is a designed check with a selftest, not the
   free-standing sentence L.6 step 2 prices.

---

## 6 · L.6 step 1 — wiring `build_site.py`, promoting `site_pages_fresh`

### F14 — MAJOR. The promotion is safe today and a guaranteed CI break at Part I, and the same document sets both.

Read directly: `--check` forces `dry_run`, opens the DB `mode=ro`, writes no site files, no temp
state — no side effects. Without `--check` it writes the 93 pages, which is the point of wiring it
into `regenerate_derived.sh`. The render is deterministic (no timestamps; green byte-diff on all
93 today). So step 1 in isolation is executable.

But: `build_specs` walks `SELECT item_code FROM items`; `orphan_pages` reads `items`; `FP_TABLES`
names `items`, `specifications`, `specification_source_links`, `item_bpc_links`,
`item_population_links` — **five of seven tables Part E renames or retires**. The moment the Part I
baseline lands, the now-**blocking** `site_pages_fresh` dies on `no such table: items` and main is
red until `build_site.py` and `spec_page.py` are rewritten against a successor (`ren_items`) whose
design F.2 declares open. The registry note's own `min_items:1` rationale — "`items` is populated
repo content … not a corpus that legitimately empties" — is voided by the same document. Neither
L.6 nor Part G names the generators in the sweep (F6).

Also over-claimed: the check guards `site/specs/` **only**. `site/populations/` (11 files) and
`site/rooms/` (17) have driverless generators — `build_site.py`'s own docstring says so and says
`room_page.py` crashes against the live schema — so "after this, an `e-08`-class page edit cannot
be committed" is true for 93 of ~121 reader-facing files.

**Smallest fix:** promote, but add `build_site.py` + `spec_page.py` + the registry note to Part G's
sweep as work due **inside** the Part I change, and scope L.6's claim to `site/specs/`.

---

## 7 · Remaining conflicts with written practice

- **F15 — the RULE's "five hand-off keys land in the same migration" is unimplementable while F.2
  is open.** The fifth junction needs `ren_items` as an FK target; F.2 says render's item may not
  be a table, and I.6 bars execution before Part F closes. As written, the migration either
  violates the RULE (four keys) or invents `ren_items` ad hoc. The spec→render junction also has
  no name (Part D's grammar owes it one). Resolve F.2 first, or scope the RULE's action item to
  the decided stages, recorded.
- **F16 — no writers for the spine.** None of the five keyed objects has a writer:
  `add-extraction` is future work (P1.2), `add-synthesis`/`add-specification`/`add-figure`/the
  junction writers do not exist. Creating refusal-less keyed tables invites exactly the hand-SQL
  gap §4 closed; the migration and the writers need one sequencing statement.
- **F17 — `res_items.origin` backfill would assert unknown provenance.** J.1 adds `origin` to a
  table of 875 rows with, per the document's own measurement, "no record of where any of them came
  from." A `DEFAULT 'searched'` backfill writes a claim the repository cannot support (§2(c) in a
  column). The vocabulary needs an explicit `unknown-legacy` value and the backfill must use it.
- **F18 — grain change in the `evidence_population_match` move.** F.1 folds the population-match
  grade into `jud_items`, but the grade is per **source** (`ref_id`, population) while `jud_items`
  is per **extraction**. Folding it in either copies one grade across N extractions (rule 5) or
  re-grades per extraction (re-reasoning). Keeping `jud_population_grades` as a satellite keyed on
  the source, as Part E's own table does, is correct; F.1's "moving in" sentence contradicts it and
  should be struck.

---

## Answers to the direct questions

| question | answer |
|---|---|
| Would the five hand-off keys work in SQLite as written? | **No.** Two of the five are specified twice with contradictory shapes (F1); the ≥1 clause is unenforceable and unowned (F2); one column is on the wrong table (F3); one junction has no possible target yet (F15); the fan-in parent keeps a PK that forbids the proposal's own J.2 (F10). |
| Is "NOT NULL FK is free at 0 rows" true? | Mechanically yes (tested); semantically no — six admitted sources have no lead to point at (F3/F5). |
| Does the baseline approach work with the existing runner? | Only with a runner code edit (`BASELINE_DATA_CUTOFF_TS`) and a rewrite of the blocking gate's hardcoded invariant list, neither of which Part I mentions (F6, F7). |
| Would a new baseline pass `migration_reproducibility`? | **No** — the gate itself queries `items`, `citation_mining`, `connections` by name and crashes (F6). |
| Is "the incremental path IS a rebuild done 66 times" correct? | **No** — measured: renames are one-liners that rewrite REFERENCES and view bodies automatically even with FK off; 3–5 tables need real rebuilds; one AFTER_DATA marker absorbs all 33 data-migration collisions (F9). |
| Does `build_site.py --check` have side effects? | No (verified in source); the promotion's hazard is sequencing against Part I, not the check itself (F14). |

