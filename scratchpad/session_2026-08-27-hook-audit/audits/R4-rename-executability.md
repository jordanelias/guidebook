# R4 — Rename executability: does the reconciled map execute in a Sonnet session's hands?

**Auditor R4 of 4 · 2026-08-27 · lens: hand RENAME-MAP.md to a Sonnet session — does it execute, or
does it break the repo?** Everything below is bound to a measurement, a test actually run on a
scratch copy (SQL given), or file:line. DB read-only throughout; all writes were to
`/tmp/claude-0/…/scratchpad/` copies. SQLite 3.45.1 via Python, the same engine every repo tool uses.

**Verdict in one line: the mechanics execute — the marker works, ALTER TABLE propagates, one
migration suffices — but the plan as written ships four silent failures: a numbering trap that is
invisible to the blocking gate, a reproducibility gate that goes vacuous-green, a capture tool that
silently drops the first post-rename batch, and an `items` retirement that is not a rename at all.**

---

## 1 · Ordering — the P0.1 claim is TRUE; the three-migration question has a measured answer

**P0.1 claim verified TRUE, with a stale line number.** `grep -n is_canonical` across
`scripts/ tools/ governance/ .claude/`: the only call sites are `dbcore.py:469-470` — the
function's own selftest. (RENAME-MAP says `dbcore.py:438-439`; the file has grown. Substance right,
citation stale — DEFECT.) `connect()` (`dbcore.py:92-127`) never calls it; `db_path()`
(`dbcore.py:55-63`) defaults to `REPO_ROOT/data/guidebook.db` when `GUIDEBOOK_DB_PATH` is unset. So
yes: **the guard against the largest write this project will ever attempt is unwired**, and
`migrate_db.py` writes `DB_PATH` (its own default, `migrate_db.py:44`) with no canonical check
either — which is correct for migrations but means *nothing on the write path* refuses the
canonical file today. Note P0.1 is **code, not a migration** — it cannot be sequenced by migration
number; it gates by commit order only, and the rehearsals below are exactly the step it must precede.

**One migration or three? ONE schema migration, with P0.1+P0.2 as a preceding code commit — and the
data says so, not taste:**

- **P0.6 folds in or the project renames twice.** `axes`, `item_axis_links`, `population_axis_map`,
  `access_need_axis_map` have **zero** references — DML or mention — in all 33 committed
  `data_*.sql` files (measured, §4). So P0.6 needs no AFTER_DATA marker of its own and nothing in
  replay history pins its order. But under C-2 the ruled name `icf_demands` becomes
  `base_icf_demands` (or `base_taxonomy_icf`): executing P0.6 first and the map second renames the
  same four tables twice, which RENAME-MAP's own premise ("renaming against the wrong map means
  renaming twice") forbids. **Fold it in; the §R8 register entry lands in the same commit** (P0.6's
  own "rename first, entry last, one change" rule is satisfied inside one commit). P0.6 is
  owner-gated — the fold needs the owner's word, so put it to them as a question, not a default.
- **P1.0 folds in or `specifications` is rebuilt twice and `items` cannot drop at all.**
  `specifications` has 0 rows and **zero DML references** in data migrations (3 comment mentions
  only — measured). Renaming it to `spe_items` in migration A and re-keying it (drop `item_code`,
  `population_code`, add `parameter_canonical` key + three junctions) in migration B is two
  rebuilds of one 0-row table. Worse: `items` cannot be retired while
  `specifications.item_code REFERENCES items` stands, so the rename migration either includes
  P1.0's drops or must leave `items` alive — half-executing Part E. Fold it in.
- **P0.1/P0.2 stay a separate, prior commit** — they are Python and skill-prose, not SQL, and the
  scratch rehearsals of the rename (which this audit ran, and the implementer will run) are the
  exact moment an unwired guard lets a rehearsal land on the canonical file.

**Conflict check:** P0.6's "rename BEFORE register entry" and P1.0's "window closes on first
determination" are both satisfied inside one migration — 0 rows everywhere downstream (verified:
`specifications`, `specification_source_links`, `bpc_metadata`, `source_value_extractions` all 0).
No ordering contradiction exists **except** the C-1 gate: `items` retirement has no destination
until C-1 is answered (§5), so the one migration is not writable today.

## 2 · Separator — tested; underscore is right; the dot is worse than RENAME-MAP says

Ran on SQLite 3.45.1 (the repo's engine):

```sql
CREATE TABLE base.models (x);          -- OperationalError: unknown database base
CREATE TABLE "base.models" (x);        -- OK, but:
SELECT * FROM base.models;             -- OperationalError: no such table: base.models
SELECT * FROM "base.models";           -- OK (quoted forever, every caller, every tool)
ATTACH ':memory:' AS base;             -- then SELECT * FROM base.models still fails:
                                       --   the quoted-name table is NOT reachable via schema syntax
```

So a dot-named table is not merely awkward: **unquoted it is a syntax error, and if anyone ever
ATTACHes a database named `base`, the identical spelling `base.models` resolves to a different
namespace than `"base.models"`** — a permanent ambiguity with no error. A real ATTACH-based schema
would work syntactically but means multiple committed database files, and `migrate_db.py`,
`emit_batch_sql.py`, the sha256 discipline and the reproducibility gate are all built on ONE
committed blob. **Underscore is correct. RENAME-MAP C-3 stands, strengthened.** (`dbcore` itself is
dot-safe — it quotes `PRAGMA table_info("%s")` — which makes the failure surface *inconsistent*,
the worst kind: some tools would work, most would not.)

## 3 · The rename itself executes — proven on a copy of the live DB

Copied `data/guidebook.db` (canonical untouched; pre-existing `PRAGMA foreign_key_check` = 0 rows)
and executed **51 `ALTER TABLE … RENAME TO …`** — every Part E rename in one transaction:

- **51/51 succeeded.** No live view is broken pre-rename (all 18 compile).
- **View bodies, FK clauses and indexes auto-update** (SQLite ≥3.25, `legacy_alter_table=0`
  verified): after `ALTER TABLE items RENAME TO base_building`, the test view's stored SQL reads
  `FROM "base_building"` and `PRAGMA foreign_key_list` on the child shows the new parent. Nested
  views survive. A rename inside a transaction rolls back cleanly.
- **Therefore the "18 views must be swept" burden is smaller than NOMENCLATURE Part G implies**:
  views need *manual* DDL only where a table is **dropped**, or where the view itself is renamed.

**But the `items` retirement broke everything it touched — it is not a rename and must stop being
costed as one:**

- `DROP TABLE items` succeeds silently, then **3 views are broken** (`v_source_reach_all`,
  `v_item_extractions`, `v_item_provenance`: `no such table: main.items`) — and, the sharp part:
  **any subsequent `ALTER TABLE … RENAME` on ANY table then fails** with
  `error in view v_source_reach_all: no such table: main.items`. SQLite re-parses every view on
  every rename. **Ordering inside the migration is therefore fixed: all renames first, then
  DROP/CREATE the three items-reading views, then the drop.** A Sonnet session that orders it
  drop-first gets an opaque error on an unrelated table.
- `PRAGMA foreign_key_check` after the drop: **786 dangling rows** — `item_population_links` 372,
  `item_axis_links` 158, `term_item_links` 147, `jurisdictional_values` 109. These are live data,
  and the schema-phase runner is `fk_blocking=False` (`migrate_db.py` `run_migrations`), so the
  migration **commits with 786 advisory violations** and nothing stops it. Re-pointing those FKs is
  a full 12-step table rebuild per table (SQLite cannot ALTER a FK) — with **no destination until
  C-1 is answered**. Part G's "the renames and the NOT NULL hand-off keys are DDL / cheapest it
  will ever be" is TRUE for the 0-row pipeline tables and **FALSE for `items`**. — **BLOCKER until
  C-1; then MAJOR (the 4-table rebuild must be in the migration).**
- One more shape problem RENAME-MAP does not name: the architecture note's `base.building` "lists
  all building typologies **and** all architectural and design elements" — that is `rooms` (17)
  **plus** `items` (93). A **merge**, not a rename. No ALTER TABLE expresses it. C-1's answer must
  say merge/don't-merge, or the re-derived map inherits the ambiguity.

## 4 · Replay collisions — measured both ways, and the marker mechanism proven end-to-end

**Convention stated (prior audits disagreed on exactly this):** *executable DML reference* = the
table name appears in `INSERT INTO / UPDATE / DELETE FROM / FROM / JOIN` position after stripping
`--` and `/* */` comments; *mention* = bare word-boundary token anywhere in the file, comments
included. 33 `data_*.sql` files; 66 live tables; script run 2026-08-27.

| table (top of each class) | DML files | mention files |
|---|---:|---:|
| `evidence_sources` | 16 | 19 |
| `decisions` (unrenamed) | 8 | 9 |
| `citation_mining` / `search_executions` / `search_candidates` | 7 each | 7–8 |
| `source_locators` | 5 | 14 |
| `evidence_population_match` / `evidence_source_authors` | 4 | 4–5 |
| `gaps`, `source_slug_links`, `jurisdictional_values`, `search_admissions`, `reference_stubs` | 2 each | 2–3 |
| `items`, `specifications`, `rooms`, `conflicts`, … | **0** | 1–9 (comments/strings only) |

13 tables carry executable DML references; **every one of the 33 files references at least one
renamed table**; 44 tables appear in no data migration at all. The mention counts overshoot the DML
counts by up to 9 files (`items`: 0 vs 9) — **whichever prior audit counted mentions was counting
comments.** Only the DML set can break replay.

**Does one `-- AFTER_DATA:` marker solve it? TESTED — yes.** Copied the full real migration corpus
to a scratch dir, added `068_rename_smoke.sql` containing `-- AFTER_DATA: 20260825215123`,
`PRAGMA user_version = 68`, and renames of the four hardest tables (`evidence_sources`,
`search_executions`, `source_locators`, `source_value_extractions`); ran
`GUIDEBOOK_MIGRATIONS_DIR=… migrate_db.py --rebuild`:

- **With the marker: rebuild succeeds** — 9 schema + 33 data applied, `res_items` = 875 rows,
  `evi_sources` = 10, `user_version` 68. All 33 data migrations replay against old names first;
  the rename runs last. One marker, cutoff = the newest data timestamp (today `20260825215123`),
  covers all 33, because `build_plan()` drains every data migration `<= cutoff` before the marked
  schema migration (`migrate_db.py build_plan`).
- **Without the marker: rebuild dies** on the first post-baseline batch
  (`data_20260819134359…: no such table: evidence_sources`). The marker is not optional.
- No live migration currently carries a real marker (`AFTER_DATA` appears only in comments and
  decision strings; the pattern `^-- AFTER_DATA: \d{14}$` matches nothing — grepped 057 and the
  baseline data file).
- **Race worth one sentence in the runbook:** a concurrent branch landing a data migration with a
  timestamp **after** the cutoff, written in old vocabulary, replays after the rename and kills the
  rebuild — loudly (C1 rebuild ERROR, blocking `data` battery), so it is caught, not silent.
- The deferred alternative (a fresh baseline, per DR-2026-08-12's own alternatives list) also
  works but requires editing the hardcoded `BASELINE_DATA_CUTOFF_TS` (`migrate_db.py`,
  `discover_data_migrations`) — one more landmine — and forfeits replay-proof of the rename. The
  marker is lighter and now proven.

## 5 · The caller sweep — RENAME-MAP's list is a fraction of the measured set

**Convention:** tracked files (`git ls-files`), excluding `_archived/ sessions/ audits/ versions/
workplan/_superseded/ references/search-log/ scratchpad/ scripts/migrations/` (frozen records and
the immutable corpus §4 already handles), bare word-boundary token match. Two rename sets, because
the reconciled map isn't settled:

- **Part E set (52 renamed tables): 769 live files** name at least one — 88 python, 50 of 61
  skills, 14 yaml, 68 json (60+ of them `attestations/` — frozen, not callers), 3 js, 1 shell,
  108 generated html (regenerate, don't sweep), 437 md.
- **Architecture-note set (57 — the note also renames `slugs`→`base_topics`,
  `populations`→`base_taxonomy_identity`, `access_needs`, `terms`/`term_aliases`): 809 files.**
  `slugs.slug` carries 14 inbound FKs; renaming it is the single biggest sweep-widener the note
  smuggles in. The re-derivation step must say explicitly whether the substrate vocabularies
  rename, because the two maps differ by ~40 files and every FK clause auto-updates either way.

**RENAME-MAP §5's "3 views, 16 Python files, 22 skills, 4 governance YAMLs, plus the generators"
against measurement — MAJOR:**

- **Python: 88 files** mention a renamed table (executable-reader core ≈ the 40+ under `scripts/`
  and `tools/` that open the DB). 16 is off by 5×.
- **Skills: 50**, not 22.
- **Governance YAMLs: 7 live** — `check-registry.yaml` (29 tables), `context-map.yaml` (**66** —
  regenerable via `context_map.py`), `pipeline-map.yaml` (**65** — hand-maintained, no generator
  found), `research-contract.yaml` (10, and it is the SessionStart-injected contract; its R4
  sentence is already owed an amendment by P1.0), `retired-vocabulary.yaml` (11),
  `pipeline-contract.yaml` (7), `scripts/audit/graph/known_debt.yaml` (5). Plus 2 workflow yamls
  (`regenerate-derived.yml`, `verify-urls.yml`), `bootstrap.sh` (6 tables), and
  `scripts/workflows/anchor-correctness-sweep.js`.
- **Views: "3" is right for a different reason than the map can know** — my test (§3) shows ALTER
  TABLE auto-updates all 18 view bodies; exactly 3 need manual DDL, and only because of the `items`
  drop. If the map means "3 views reference renamed tables", that is wrong (all 18 do); the number
  survives on mechanics it doesn't state.
- **The SessionStart hook itself is clean**: the 2,903-char injected command in
  `.claude/settings.json` names zero tables (checked against the high-traffic names), so
  `research_contract_sync` does not fire on the rename — one feared caller that ISN'T one.
- **The ungreppable residue — nobody's list has it:** `items`, `gaps`, `conflicts`, `rooms`,
  `decisions`, `connections`, `terms`, `situations` are English words. `\bitems\b` alone hits
  **163 md files** under `skills/ governance/ references/` (measured with `grep -rlP`), and
  `run_checks.py`'s three "table" hits are the prose word "items" in comments. **The sweep for the
  retired `items` cannot be executed by grep; it requires per-file classification**, and Part E
  retires precisely the worst-named table in the repo. Budget it as its own work item.

## 6 · Landmines — every hardcoded table name that breaks a gate, with its failure MODE

Probed by pointing each check at the fully-renamed scratch DB (`GUIDEBOOK_DB_PATH=…`). The split
that matters is not blocking/advisory — it is **loud-red versus vacuous-green**:

**Class A — vacuous-green (the dangerous class; these MUST be swept in the rename commit):**

1. **`migration_reproducibility.py` CORE_INVARIANTS (14 `\bitems\b` occurrences in the file —
   RENAME-MAP's "×14" confirmed). PROVEN VACUOUS:** ran the blocking check against a
   marker-rebuilt renamed DB — `evidence_sources count  skip (no such table…)` …
   **`EXAMINED: 7` … `VERDICT: PASS`, exit 0.** `compare()` catches `OperationalError` as "skip"
   *and counts the skip as examined*. Under the full rename, 6 of 7 invariants skip and the
   blocking gate passes forever. Also `_usable_cache()` requires the six OLD names, so the rebuild
   cache goes permanently dead (fresh ~33s rebuild, twice per CI run) until updated; the selftest
   fixtures (`items` et al., 6 sites) also pin old names. — **BLOCKER.** Smallest fix: new names in
   `CORE_INVARIANTS` + `_usable_cache` + selftest, same commit; and make `EXAMINED` count non-skips.
2. **`dbcore.WRITABLE_TABLES`** (13 old names, `dbcore.py` TABLES block) — imported by
   `emit_batch_sql.py:49`, which diffs scratch-vs-canonical **only for listed tables**. Post-rename
   a batch writes `evi_sources` and the capture emits **zero statements for it, no error** — the
   exact 32-of-40 silent-loss mechanism the list exists to prevent, at full width. Partially
   self-guarding: `dbcore --selftest` asserts `WRITABLE_TABLES[0] == "evidence_sources"`, so
   `--selftest` goes red IF anyone runs it — and §5 of CLAUDE.md already records that
   `--changed-from` does not. — **BLOCKER; sweep in the rename commit + run `--selftest`.**
3. **`validate_evidence_state.py` (blocking): exit 0 against the renamed DB** while printing "FAIL
   specifications machine … tables absent (run migration 024)" — it treats missing tables as
   pre-migration state and passes. A missed sweep here is silent. — **MAJOR.**
4. **`build_site.py` FP_TABLES (`:65`)** — 6 of 7 renamed; `fingerprint()` catches the error as
   `"NA"` per table, so freshness fingerprints silently degrade (though `--check` happens to crash
   red later on an unguarded `items` query — the fingerprint itself is the vacuous part). —
   **MAJOR.** (`check_rendered_docs --all` is EXAMINED-0 green today regardless.)

**Class B — loud-red (safe, but each is a broken gate until swept):** verified by execution:
`test_db_integrity.py` (blocking, 28 table names) crashes `no such table: source_slug_links`;
`validate_verification_consistency.py`, `source_slug_links_duplicates.py`, `validate_axes.py`
crash; **`tools/pipeline_completeness.py --check` (blocking `pipeline_completeness_fresh`) crashes
`no such table: gaps`** — and its `STAGES` (`:37`) plus `governance/pipeline-contract.yaml:35` are
still the FIVE-stage machine, so the six-stage catch-up is a co-requisite, not an afterthought.
Registry checks whose YAML text names renamed tables (measured 25 checks; blocking among them:
`test_db_integrity`, `citation_mining_session`, `validate_evidence_state`, `validate_axes`,
`validate_verification_consistency`, `source_slug_links_duplicates`, `pipeline_completeness_fresh`)
plus `db.py` (31 tables), `generate_parts.py` (12), `spec_page.py` (11), `assess_cell.py` (12),
`research_batch_dod.py` (17), `regenerate_vetting_surface.py` (13), `evidentiary_audit.py` (12),
`graph/topology.py` (16), `validate_pydantic_schemas.py` (19) and the `schemas/*.py` mirrors
(blocking `validate_schema` passed against the renamed DB — its subject is entity YAML, so the
mirror sweep is enforced by `validate_pydantic_schemas`/`validate_schema_cross_check` instead).

## 7 · Migration numbering — the reservation is prose, the trap is proven, and the gate can't see it

Highest on disk: `064`. REPAIR-PLAN reserves **065 (P1.1), 066 (P2.2), 067 (P2.5) in prose only** —
nothing in `migrate_db.py` knows a reservation exists; `discover_schema_migrations()` just sorts,
and (tested) a corpus that jumps 064→068 rebuilds fine. The enforcement that DOES exist is the trap:

**Tested:** simulated the rename landing as 068 with 065 still unwritten, then landing
`065_late_reserved.sql` afterwards. On the live path `run_migrations` reports **"Schema at version
68; 0 applied"** — `version <= current` silently skips 065 forever. `--rebuild` applies it. The two
databases now diverge (`late_check_home` exists in one) — **and the blocking reproducibility check
cannot see it** post-rename: `user_version` matches (both 68) and the count invariants compare
equal (or skip, §6.1). Only the **advisory** `migration_reproducibility_deep` reports
EXTRA-IN-REBUILD. — **BLOCKER as planned.**

**Answer: the rename takes the next FREE number at landing time — 065 today — and REPAIR-PLAN's
reservations shift.** Reserving numbers ahead of an interleaving migration is incompatible with
`migrate_db.py`'s forward-only `version <= current` skip; the plan's allocations are unwritten
files, renumbering them costs one edit to REPAIR-PLAN. If the owner insists 065–067 land first,
then the rename waits — but "rename now, backfill 065–067 later" is the one sequence that is
provably broken and provably invisible to the blocking gate. Smallest structural fix beyond
renumbering: `run_migrations` should FAIL (not skip) on a pending migration numbered below
`user_version` — five lines, and it converts this whole class from silent to loud.

## 8 · The acceptance test — what actually proves the rename correct

A byte-identical `--rebuild` is impossible (schema changed) and a 0-row table proves nothing
(CLAUDE.md rule 4: `v_item_provenance` rendered "clean" while broken). The test is five parts, all
runnable, none owner-gated:

1. **Replay proof:** `migrate_db.py --rebuild /tmp/x.db` green with the marker (proven possible,
   §4), and `migration_reproducibility --deep` green **after** its constants are swept — run the
   deep form explicitly once and record it, because the blocking shallow form is proven blind (§6.1,
   §7).
2. **Content-equivalence under the name map:** for every (old→new) pair,
   `COUNT(*)` pre == post, and `sha256` of the ordered full-row dump equal (rename moves no pages;
   any difference is the migration doing more than it claims). My smoke run: 875/875, 10/10.
3. **Every view compiles:** `SELECT * FROM "<v>" LIMIT 0` across all 18 — this exact probe caught
   the 3 items-broken views in §3. Compiling is necessary, not sufficient, hence:
4. **A seeded walk, because 0 rows prove nothing:** on a scratch copy, insert one fixture row per
   hand-off table down the spine (res→evi→jud→syn→spe with their NOT NULL keys) and select it back
   through every cross-stage view; then write one row via `db.py add-source` against scratch and
   assert `emit_batch_sql` **emits a statement count equal to the rows written** — the counting
   test that catches a missed `WRITABLE_TABLES`, per the 32-of-40 precedent. (`walk_e2e.sh` is the
   eventual full form; this is its rename-shaped core.)
5. **Sweep proof:** `run_checks.py --changed-from origin/main` AND `--selftest` (the registry
   `basis:`/C7 surface broke exactly here on 2026-08-25) AND every blocking check prints
   `EXAMINED > 0` (catches the Class-A vacuous gates) AND `grep -rP` for every old
   non-English-word table name over the live tree returns only frozen paths — with the
   English-word residue (`items`, `gaps`, `conflicts`, `rooms`…) enumerated file-by-file as its
   own reviewed list, since grep cannot adjudicate it (§5).

## What I attacked and could NOT break

- **The AFTER_DATA marker**: full rebuild over the real 33-file corpus with a marked rename —
  correct order, correct rows, correct `user_version`; removing the marker fails exactly as
  predicted. One marker suffices for all 33.
- **ALTER TABLE RENAME at scale**: 51/51 renames on a live-copy DB in one transaction; views, FK
  clauses, indexes and nested views all auto-updated; rollback clean; zero pre-existing FK
  violations or broken views to trip over.
- **`_prepare_body`/user_version hoisting** handled the rename file without modification.
- **`dbcore.ref_id_homes`** is genuinely schema-derived now — renamed tables carrying `ref_id`
  stay in the mint (the pre-fix silent REF-00001 failure is closed, as RENAME-MAP §4 records).
- **The SessionStart research-contract hook** carries no table names; `research_contract_sync`
  does not fire on this change.

---

**DIGEST (5 lines):**
**B1** Numbering: rename must take the next FREE number (065 today); reserved-065-lands-after-068 is PROVEN silently skipped live, applied on rebuild, and invisible to the blocking reproducibility gate — renumber REPAIR-PLAN or wait.
**B2** Vacuous gates: `migration_reproducibility` PROVEN to PASS post-rename with 6/7 invariants "skip"; `WRITABLE_TABLES` silently drops the first post-rename batch's capture; `validate_evidence_state` exits 0 with its tables absent — all three sweep in the rename commit itself.
**B3** `items` is not a rename: DROP leaves 786 dangling rows (372/158/147/109), breaks 3 views, and then blocks EVERY later ALTER TABLE RENAME (proven) — renames first, views recreated, 4-table FK rebuild included, and none of it writable until C-1 (which is actually a rooms+items MERGE question).
**M1** Sweep truth: 769 live files (88 py, 50 skills, 7 governance yamls) name a renamed table vs RENAME-MAP's "16 Python, 22 skills, 4 YAMLs"; views need manual work only at the drop (auto-update proven); the English-word tables (`items` in 163 md files) are ungreppable and need per-file review.
**OK** The mechanics hold: one migration (folding P0.6+P1.0, owner consent asked), one AFTER_DATA marker at `20260825215123` (proven end-to-end), underscore separator (dot proven broken two ways), P0.1 claim TRUE (`dbcore.py:469-470`, not 438-439), acceptance = rebuild+deep-compare, mapped row-sha equality, 18-view compile, seeded spine walk, EXAMINED>0 everywhere.
