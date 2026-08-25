# S3 — JUDGMENT STAGE smoke test log

Agent: S3. Stage: `judgment` (`specifications`, `specification_source_links`,
`convergence_assessment`, `spec_value_probes`, `probe_population_links`, `conflicts`,
`weighting_profile`, `external_root_registry`, `item_audit_runs`, and the `v_*` judgment views).
Scratch DB: `$SMOKE/s3-judgment.db`. Canonical DB opened read-only only; sha256 confirmed
`30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf` at start **and** end of run
(unchanged — see entry 25).

---

### 1. Mechanical search for a `specifications` writer
INVOKED   : `grep -n "add_parser" scripts/db.py`; `grep -rn "INSERT INTO specifications" scripts/ skills/`
STAGE     : judgment
EXIT      : 0   RUNTIME: <1s
READS     : `scripts/db.py` (full subcommand list, ~40 `add_parser` calls); `scripts/assess/assess_cell.py:572,574`; `scripts/validate_verification_consistency.py:101`; `scripts/tests/test_*.py`
WRITES    : NONE
EXAMINED  : entire `scripts/db.py` subcommand registry (40 subcommands) + a full-tree grep for the string
OUTPUT    : `scripts/db.py` subcommand list contains `add-candidate, add-population-match, add-jurisdictional-value, add-economics-entry, add-case-study, add-locator, add-gap, close-gap, add-connection, update-connection, add-source, add-conflict, update-conflict, add-item, add-audit-run, update-audit-run, add-supersession-check, add-gap-mining, update-gap-addressability` and query commands — **no `add-specification`, no `update-specification`.** The only production `INSERT INTO specifications` in the whole tree is `scripts/assess/assess_cell.py:572`. The only other two hits are `scripts/validate_verification_consistency.py:101` (a test/self-check fixture) and `scripts/tests/test_*.py` (unit-test fixtures, not runnable production writers).
FINDING   : ABSENT
LOCATION  : `scripts/db.py` (no subcommand exists); production writer is `scripts/assess/assess_cell.py:572-575`
NOTE      : This is the single largest finding of the run (elaborated in entries 2-5, 22). CLAUDE.md §4 claims the write-path gap that caused the 2026-08-19 fabrication was "closed" for every table `db.py` could not previously reach — but `specifications`, the judgment stage's own primary output table, was **never in scope for that closure**: it has no CLI writer at all, sanctioned or refusing.

---

### 2. `scripts/assess/assess_cell.py --help`
INVOKED   : `python3 scripts/assess/assess_cell.py --help`
STAGE     : judgment
EXIT      : 0   RUNTIME: 0.16s
READS     : `scripts/assess/assess_cell.py:1-635` (full file)
WRITES    : NONE
EXAMINED  : 1 (the script itself)
OUTPUT    : `usage: assess_cell.py [-h] --db DB --emit-sql EMIT_SQL [--report-json REPORT_JSON]`
FINDING   : PASS (as a --help invocation) but see finding below
LOCATION  : `scripts/assess/assess_cell.py:483-486` (argparse block)
NOTE      : **There is no `--item` / `--population` / `--slug` argument at all.** The script does not accept an arbitrary (item × population) target. It iterates a hardcoded `PILOT_CELLS` list (`assess_cell.py:116-131`, 7 entries) baked into the source. To assess a different cell you must edit the Python source — there is no invocation-level way to target E-03×MOB (ramp gradient, the PROTOCOL's own example) at all. `--db` explicitly refuses the canonical DB (`assess_cell.py:494-495`: `sys.exit("REFUSING: this engine never writes the canonical DB (owner-gated).")`), and the module docstring calls the whole thing a "pilot determination engine," "Replayable onto the canonical DB ONLY after owner ratification" (`assess_cell.py:501-503`). This is not a general judgment-writing tool; it is a one-time backfill demo for 7 named cells.

---

### 3. `assess_cell.py` run #1 — crashes on cell 1 (gap-id format drift)
INVOKED   : `python3 scripts/assess/assess_cell.py --db $SMOKE/s3-judgment.db --emit-sql $SMOKE/out/pilot-cells.sql --report-json $SMOKE/out/pilot-report.json`
STAGE     : judgment
EXIT      : 1   RUNTIME: 0.17s
READS     : `$SMOKE/s3-judgment.db` tables `gaps`, `items`, `populations`, `evidence_sources`, `source_slug_links`, `evidence_population_match`
WRITES    : NONE (crashed before commit; `conn.commit()` at `assess_cell.py:611` never reached)
EXAMINED  : 1 of 7 pilot cells (E-08×DEAF, the first in `PILOT_CELLS`)
OUTPUT    : `pydantic_core._pydantic_core.ValidationError: 1 validation error for EvidenceStateRecord / gap_register_id / Value error, gap_register_id must match GAP-NNN or GAP-NNNN, got: GAP-1`
FINDING   : FAIL
LOCATION  : `scripts/assess/assess_cell.py:427-428` (`next_gap_id()`: `return f"GAP-{mx + 1}"`, no zero-padding) vs `gaps.gap_id` live format
NOTE      : Root cause (confirmed in entry 4's debug trace): the live `gaps` table's 5 rows are all slug-scoped `GAP-B0N-NNN` (e.g. `GAP-B01-001`), not the flat numeric `GAP-NNN` `next_gap_id()` was written against. Its own regex (`g.split("-")[1].isdigit()`) correctly excludes the `B01`-style ids from the max-finding scan, so `mx` computes to `0`, and `next_gap_id()` emits the un-padded `"GAP-1"`, which the schema's own `EvidenceStateRecord` pydantic model (which the script itself calls as a pre-insert gate, `assess_cell.py:530`) rejects. **The repository's only writer for its primary judgment-stage table cannot complete a single determination against the live DB state as committed today, unmodified.**

---

### 4. `assess_cell.py` debug run — gap-id patched, crashes on cell 6 (bad population code)
INVOKED   : local diagnostic copy `$SMOKE/assess_cell_debug.py` (copy of `scripts/assess/assess_cell.py` with one line patched: `next_gap_id()` zero-pads to `GAP-{n:03d}`, plus a one-line debug print before `validate_with_models`). Run: `PYTHONPATH=/home/user/guidebook python3 $SMOKE/assess_cell_debug.py --db $SMOKE/s3-judgment.db --emit-sql ... --report-json ...`
STAGE     : judgment
EXIT      : 1   RUNTIME: <1s
READS     : same as entry 3, plus `populations` table
WRITES    : NONE (crashed mid-loop, before `conn.commit()`)
EXAMINED  : 6 of 7 pilot cells before crash (E-08×DEAF, E-12×MOB, G-03×MOB, C-02×DEM, E-06×MOB, G-03×SCI all reached `validate_with_models` successfully with the patch; the 7th, B-10×NEU, crashed earlier)
OUTPUT    : `ValueError: population 'NEU' not in populations table`
FINDING   : FAIL
LOCATION  : `scripts/assess/assess_cell.py:129` (`PILOT_CELLS` entry `("B-10", "NEU", ...)`) vs live `populations` table (23 valid codes: `ADHD, ALL, AUT, BAR, BLIND, BRAIN, COM, DEAF, DEAFBLIND, DEM, EPI, ID, LMB, LPA, MH, MOB, MOVE, MS, NDV, PAIN, SCI, TALL, VES` — no `NEU`)
NOTE      : This debug copy required an out-of-band edit to run at all (the gap-id zero-pad patch) — logged loudly per protocol, and made only to a throwaway copy in `$SMOKE/`, never to the tracked file. Even patched, the script's own hardcoded pilot data references a population code that does not exist in the live schema. **This is the only file in the repository that is simultaneously (a) the sole production writer for the judgment stage's primary table and (b) internally broken against the current DB two different ways in the first 7 rows it tries to write.**

---

### 5. `assess_cell.py` debug run — full completion with NEU row dropped
INVOKED   : same debug copy, `PILOT_CELLS`'s 7th entry (`B-10`/`NEU`) commented out (logged, not silently dropped)
STAGE     : judgment
EXIT      : 0   RUNTIME: <1s
READS     : same as entry 4
WRITES    : `$SMOKE/s3-judgment.db` — `specifications` rows 9001-9006 (6 rows, `specification_id` 9001-9006); `gaps` rows `GAP-001`..`GAP-006` (6 rows). `convergence_assessment`: 0 rows written (none of the 6 cells reached the `anchors`/`t3c` branches).
EXAMINED  : 6
OUTPUT    :
```
E-08×DEAF  pending      basis=-  scale=population refs=0 rso=0 cfo=0 sha=d2c26c00ebe5
E-12×MOB   pending      basis=-  scale=population refs=0 rso=0 cfo=0 sha=3a324b51c226
G-03×MOB   pending      basis=-  scale=population refs=0 rso=0 cfo=0 sha=b35942f48258
C-02×DEM   pending      basis=-  scale=population refs=0 rso=0 cfo=0 sha=26749e151c61
E-06×MOB   pending      basis=-  scale=population refs=0 rso=0 cfo=0 sha=37c2fc07b003
G-03×SCI   pending      basis=-  scale=population refs=0 rso=0 cfo=0 sha=d57fb855ee58
```
FINDING   : PASS (mechanically) / FAIL (substantively)
LOCATION  : `scripts/assess/assess_cell.py:116-131` (`PILOT_CELLS` inline comments) vs actual outcome
NOTE      : **Every single one of the 7 pilot cells — including the ones the source comments describe as rich demonstration cases ("Co-1-anchored corridor width," "full-mix; convergence assessed from real data," "Co-2 + T2 anchoring," "T4-6 only; decisive G1 regulatory-stratum test") — resolves to `pending` with zero governing refs.** The pilot script's own demonstration data is stale against the current corpus (see entry 6: the root cause is that `source_slug_links` is now almost entirely empty). This means even a bug-fixed `assess_cell.py` produces no `stated`/`provisional` cells at all for its own advertised examples, two of which (E-12×MOB, E-06×MOB) are squarely inside the mobility batch's subject.

---

### 6. Why: `source_slug_links` slug mismatch and near-total emptiness
INVOKED   : direct read-only queries against `data/guidebook.db` (`sqlite3` via Python, `mode=ro`)
STAGE     : judgment / evidence-collection boundary
EXIT      : 0   RUNTIME: <1s
READS     : `items.bpc_source_slug`, `source_slug_links`, `evidence_sources`, `evidence_population_match` (canonical DB, read-only)
WRITES    : NONE
EXAMINED  : all 8 slugs named by `PILOT_CELLS` + `items.bpc_source_slug` for every mobility-batch item named in PROTOCOL.md
OUTPUT    :
```
source_slug_links total rows: 10          (ALL on ONE slug: room-acoustic-performance)
distinct slugs with any link: 1
evidence_sources total: 10
evidence_population_match total: 25 (none targeting MOB)
```
Also: `items.bpc_source_slug` for `E-08` is `accessible-circulation-geometry`, but `PILOT_CELLS` hardcodes slug `deaf-spatial-design` for the same item (`assess_cell.py:117-118`) — a slug that itself has 0 `source_slug_links` rows.
FINDING   : FAIL / ABSENT
LOCATION  : `source_slug_links` table (10/106 slugs linked); `scripts/assess/assess_cell.py:117-118` (E-08's hardcoded slug doesn't match `items.bpc_source_slug`)
NOTE      : **This is the substrate fact that makes entry 5's "all pending" outcome inevitable, not a bug in the determination logic.** For a real mobility batch (E-08, E-03, E-11, G-04, B-08, C-03, C-05, C-06, E-01, E-04), only A-05 shares a slug (`room-acoustic-performance`) with ANY admitted evidence at all, and that evidence is acoustic-performance research, not mobility research. Every other mobility item's slug has zero linked sources. A real judgment run today for corridor width, ramp gradient, thresholds, or parking would `pending` on evidence-collection grounds before any judgment logic even applies.

---

### 7. `validate_evidence_state.py` against 0-row (then 6-row) `specifications`
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s3-judgment.db python3 scripts/validate_evidence_state.py` — run twice, before and after entry 5's writes
STAGE     : judgment
EXIT      : 0 both times   RUNTIME: <1s each
READS     : `specifications`, `convergence_assessment`, `gaps` (via `$GUIDEBOOK_DB_PATH`, correctly honored — `validate_evidence_state.py:432-433`)
WRITES    : NONE (read-only validator)
EXAMINED  : 0 (before entry 5) / 6 (after)
OUTPUT    : before: `OK cell-state machine: 0 cells, 0 convergence rows` / `PASS: 0 records checked, 0 errors, 0 warnings` / `EXAMINED: 0`. After: `OK cell-state machine: 6 cells, 0 convergence rows` / `PASS: 6 records checked, 0 errors, 0 warnings` / `EXAMINED: 6`.
FINDING   : VACUOUS (before) / PASS (after, with real subject)
LOCATION  : `scripts/validate_evidence_state.py` (script correctly prints `EXAMINED` per CLAUDE.md §2(a) and distinguishes the two cases in its own output)
NOTE      : This is what running any judgment gate against the **canonical DB unmodified** looks like today: a green pass with `EXAMINED: 0` — CLAUDE.md failure mode (a) exactly, and it is not hypothetical: it is the canonical DB's actual current state, confirmed live in this run before I wrote anything.

---

### 8. Nine synthetic `specifications` rows written by hand SQL (loud, deliberate)
INVOKED   : `$SMOKE/write_test_cells.py` (custom script, raw `sqlite3` INSERTs against `$SMOKE/s3-judgment.db` — **no sanctioned writer exists per entry 1**, so this is intentional, logged hand SQL against a table `db.py` cannot reach)
STAGE     : judgment
EXIT      : 0   RUNTIME: <1s
READS     : NONE beyond the connection itself
WRITES    : `specifications` rows 9101-9109 (9 rows); `convergence_assessment` rows 9201-9206 (6 rows). Full manifest:
| id | item×pop | state | designed to test |
|---|---|---|---|
| 9101 | E-03×MOB | stated, `governing_refs=NULL` | anti-hallucination gate |
| 9102 | E-01×MOB | stated, `regulatory_stratum_only=1` | G1b no-regulatory-stratum-stated |
| 9103 | E-04×MOB | stated, sole basis 1×T3-clinical ref | tier3-alone-threshold |
| 9104 | B-08×MOB | stated, `code_floor_only=1` | code_floor_only-stated rule |
| 9105 | E-03×VIS | provisional, no confidence flag | provisional-requires-confidence-flag |
| 9106 | G-04×VIS | not_applicable, no rationale | NA-requires-rationale |
| 9107 | A-05×MOB | pending, no `gap_register_id` | pending-requires-gap-link |
| 9108 | E-11×MOB | provisional, T3-alone (correctly *not* stated) | clean-pass contrast to 9103 |
| 9109 | C-05×DEAF | not_applicable, with rationale | clean-pass |
EXAMINED  : n/a (writer, not a check)
OUTPUT    : all 9 rows + 6 convergence rows committed without error (schema CHECK constraints satisfied for every row)
FINDING   : BLOCKED (no sanctioned path existed) — hand SQL used as the only option, exactly as CLAUDE.md §4 anticipates for a genuine coverage gap ("that is a coverage bug to fix, not a licence to bypass" — logged here as the licence-free workaround it is)
LOCATION  : no `scripts/db.py` subcommand exists for any of this (see entry 1)
NOTE      : Every governing ref used (`REF-00325`, `REF-00561`, `REF-00578`, `REF-00965`) is a **real, already-admitted** evidence source from the canonical corpus — no evidence was fabricated or admitted, only recombined into synthetic determination rows, per PROTOCOL rule 4.

---

### 9. `validate_evidence_state.py` against the 9 synthetic rows — all three contract criteria trip correctly, plus more
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s3-judgment.db python3 scripts/validate_evidence_state.py`
STAGE     : judgment
EXIT      : 1   RUNTIME: <1s
READS     : `specifications` (15 rows: 6 from entry 5 + 9 from entry 8), `convergence_assessment` (6 rows), `gaps`
WRITES    : NONE
EXAMINED  : 21 (15 specifications + 6 convergence rows)
OUTPUT    :
```
FAIL specifications machine (s3-judgment.db):
  cell 9101 (E-03×MOB): state 'stated' requires non-empty governing_refs (anti-hallucination gate)
  cell 9102 (E-01×MOB): state 'stated' but the cell is regulatory-stratum-only (T4-6 basis) — never 'stated' (G1b, unification DR ACCEPTED)
  cell 9103 (E-04×MOB): state 'stated' but single-axis convergence is Tier-3-alone (['REF-00561']) — Tier 3 is 'rarely the sole basis' (tier-system.md); must be 'provisional'
  cell 9104 (B-08×MOB): state 'stated' but code_floor_only=1 — a Tier-6-only cell can never be 'stated' (best-practices-assessment-system.md §3)
  cell 9105 (E-03×VIS): state 'provisional' requires confidence flag — dimensions_present, dimensions_absent, synthesis_basis (§2.3)
  cell 9106 (G-04×VIS): state 'not_applicable' requires not_applicable_rationale (§2.5)
  cell 9107 (A-05×MOB): state 'pending' requires gap_register_id (§2.4)

FAIL: 21 records checked, 7 errors, 0 warnings
EXAMINED: 21
```
FINDING   : PASS (the validator itself — every designed violation tripped with the correct, specifically-attributed message; the two designed-clean rows 9108/9109 produced no error)
LOCATION  : `scripts/validate_evidence_state.py:222-296` (`validate_cell_states_db`)
NOTE      : **This is the best news of the run.** All three pipeline-contract judgment criteria — `governing-refs-nonempty`, `no-regulatory-stratum-stated`, `tier3-alone-threshold` — fire exactly as documented, correctly attributed, the instant they have a real subject. `validate_evidence_state.py` is not the weak point of this stage; the total absence of anything upstream that would ever hand it a row to check is.

---

### 10. `external_root_registry` / `source_value_extractions` schema and emptiness
INVOKED   : direct read-only queries against canonical `data/guidebook.db`
STAGE     : judgment
EXIT      : 0   RUNTIME: <1s
READS     : `sqlite_master` (both table definitions), row counts
WRITES    : NONE
EXAMINED  : both tables in full
OUTPUT    : `external_root_registry`: 0 rows. `source_value_extractions`: **0 rows** (not "8 rows on a single slug as of 2026-07-20" as `governance/pipeline-contract.yaml`'s `convergence-independence` criterion text and `evidence-architecture.md` §5.5's H3 note both currently state — that figure is now stale; the corpus reset zeroed it). `source_value_extractions.root_id` carries **no FK** to `external_root_registry.root_id` — only `ref_id`, `population_code`, `promoted_to_rdc_id`, and `item_code` have FKs on that table.
FINDING   : ABSENT (registry enforcement) / drift (stale row-count claim)
LOCATION  : `governance/pipeline-contract.yaml` line ~118 ("8 rows on a single slug as of 2026-07-20"); `data/guidebook.db` schema for `source_value_extractions` (no `root_id` FK)
NOTE      : Confirms the PR #103 P1 finding named in the task brief: root registration is enforced by nothing mechanical. This also means the "convergence-independence" criterion (`check: null` in pipeline-contract.yaml, honestly marked `DECLARED-BUT-UNENFORCED`) has had **zero real subjects since at least 2026-07-20 through today** — the pilot data it was demonstrated against is itself gone.

---

### 11. Synthetic `source_value_extractions` rows, including one deliberate root-id typo
INVOKED   : `$SMOKE/write_sve_test.py` (raw SQL — no writer exists for this table either; `db.py` has no subcommand touching `source_value_extractions` or `external_root_registry`)
STAGE     : judgment
EXIT      : 0   RUNTIME: <1s
READS     : NONE
WRITES    : `external_root_registry` 2 rows (`ROOT-corridor-swept-path-2019`, `ROOT-corridor-anthropometric-2021`, both real registrations); `source_value_extractions` 3 rows (9301, 9302 correctly root-linked; 9303 assigned root id `ROOT-corridor-swept-path-2O19` — digit `0` replaced with letter `O`, meant to represent the SAME root as 9301 but typo'd and left unregistered)
EXAMINED  : n/a (writer)
OUTPUT    : 3 rows committed, all schema-valid (root_type CHECK, claim_type CHECK satisfied)
FINDING   : BLOCKED (no sanctioned path) — hand SQL used, logged
LOCATION  : `scripts/db.py` (no subcommand)
NOTE      : Item/slug used: `E-08` / `room-acoustic-performance` (slug reused for schema validity only — no claim is made that this slug is substantively about corridor width; see PROTOCOL rule 4, no evidence admitted, only structural test data).

---

### 12. `v_value_independence`, `v_unregistered_roots`, `v_root_id_conflicts` against the typo case
INVOKED   : `SELECT * FROM v_value_independence` / `v_unregistered_roots` / `v_root_id_conflicts` against `$SMOKE/s3-judgment.db`
STAGE     : judgment
EXIT      : 0   RUNTIME: <1s
READS     : `sqlite_master` (view SQL, entries pulled in full: `governance/pipeline-contract.yaml` cross-checked against `schemas/directness.py` naming), `source_value_extractions`, `external_root_registry`
WRITES    : NONE
EXAMINED  : 3 `source_value_extractions` rows, 2 `external_root_registry` rows
OUTPUT    :
```
v_value_independence:  ('corridor_clear_width', 'MOB', 2)
v_unregistered_roots:  (9303, 'room-acoustic-performance', 'corridor_clear_width', 'ROOT-corridor-swept-path-2O19')
v_root_id_conflicts:   (empty)
```
FINDING   : FAIL (the independence count) / PASS (the unregistered-roots flag, which did catch the typo)
LOCATION  : `v_value_independence`'s definition (`sqlite_master`): `... AND (root_ref_id IS NOT NULL OR root_id IN (SELECT root_id FROM external_root_registry)) ...`
NOTE      : **This is exactly the under-count the pipeline-contract text warns about, reproduced mechanically.** Three sources contributed extractions for `corridor_clear_width`×MOB; the view reports independence count **2**, not 3, because the typo'd root silently fails the registry-membership test and is dropped from the count entirely — the third source's contribution to independence evidence vanishes without any error. `v_unregistered_roots` *does* separately flag row 9303 — but nothing requires it to be consulted before a determination is made, there is no FK or CHECK forcing the fix, and `assess_cell.py` does not query either view (confirmed by grep: neither view name appears anywhere in `scripts/assess/assess_cell.py`). The independence machinery is real SQL that computes correctly *given clean input*, sitting entirely outside the write path that would need it.

---

### 13. `evidence_population_match` — full dump and duplicate-grade check
INVOKED   : `SELECT match_id, ref_id, target_population, match_grade FROM evidence_population_match ORDER BY ref_id, match_id`; `GROUP BY ref_id, target_population HAVING COUNT(*)>1`
STAGE     : judgment (consumer side) / evidence-collection (writer side)
EXIT      : 0   RUNTIME: <1s
READS     : `evidence_population_match` (canonical DB, read-only, all 25 rows)
WRITES    : NONE
EXAMINED  : 25
OUTPUT    : all 25 rows target one of `AUT`, `NDV`, `DEM`, `COM` — **zero target `MOB`, `VIS`, `DEAF`, `SCI`, or any other mobility-relevant population.** Duplicate-pair query returns 0 rows (no divergent-grade duplicates exist in the live table today).
FINDING   : PASS (mechanically, no data-integrity problem) / relevant-absence for the batch subject
LOCATION  : `evidence_population_match` table content
NOTE      : For the mobility batch specifically, the entire population-match substrate judgment would consume is currently empty of anything relevant — 0 of 25 rows apply. See entry 15 for what this does to a determination in practice.

---

### 14. `db.py insert_population_match` — confirmed by-design absence of uniqueness refusal
INVOKED   : `grep -n "epm\|evidence_population_match" scripts/db.py`; read `scripts/db.py:2306-2358` (`insert_population_match`)
STAGE     : judgment (consumer) / substrate (writer)
EXIT      : 0   RUNTIME: <1s
READS     : `scripts/db.py:2306-2358`
WRITES    : NONE
EXAMINED  : 1 function, in full
OUTPUT    : explicit code comment (`db.py:2325-2331`): *"DELIBERATELY NOT REFUSED: a second row for the same (ref_id, target_population)... DR-2026-08-19 §7 rules that a DISSENTING grade... lands as a second row... A uniqueness refusal here would silently abolish the adversarial mechanic."* A `prior` query does warn to stderr when a second grade is written, but does not block it.
FINDING   : PASS (matches CLAUDE.md's own characterization exactly — confirmed, not merely asserted)
LOCATION  : `scripts/db.py:2325-2340`
NOTE      : Directly relevant to the judgment consumer: `assess_cell.py`'s `population_match()` function (`assess_cell.py:169-182`) does `for grade, target in rows: ... return grade` on the **first** row that regex-matches the population — see entry 15. If a dissenting second grade existed, the judge would never see it; only the first-inserted row (by `match_id` sort order) would ever be read. **The contest DR-2026-08-19 §7 intends is invisible to the only code that currently reads this table for a determination.**

---

### 15. Real determination for A-05×SCI using real evidence, real (but inapplicable) population-match data — HEADLINE FINDING
INVOKED   : `scripts/assess/assess_cell.py`'s `determine()` function, called directly (read for observation, then written) against `$SMOKE/s3-judgment.db` for item `A-05` (Carpet in Corridors), population `SCI` (spinal cord injury — canonical mobility-adjacent code), slug `room-acoustic-performance` (the one slug in the whole corpus with real admitted evidence)
STAGE     : judgment
EXIT      : 0   RUNTIME: <1s
READS     : `evidence_sources` (10 real rows), `source_slug_links` (10 real rows), `evidence_population_match` (25 real rows, none targeting SCI or MOB), `populations`
WRITES    : `specifications` row 9110 (A-05×SCI, `state='stated'`); `convergence_assessment` row 9207
EXAMINED  : 10 sources assessed for this cell
OUTPUT    :
```
state = stated
design_scale = population
tier_basis = T1+CO1+T2
governing_refs = ['REF-00325','REF-00578','REF-00607','REF-00965','REF-00966','REF-00968']
per-source: EVERY governing source has population_directness = NOT_ASSESSED, conditioning = DOWN-WEIGHTED
```
Then `validate_evidence_state.py` (entry 9's re-run after adding this row) raised **zero errors for cell 9110** — it is not even mentioned in the FAIL list.
FINDING   : FAIL (of the architecture's own stated intent, though every individual mechanism behaved as coded)
LOCATION  : `scripts/assess/assess_cell.py:174-176` (`population_match()` returns `None`→`NOT_ASSESSED` when no row targets this population, per G2, correctly) chained into `scripts/assess/assess_cell.py:246` (`anchoring()`: `conditioning not in (COND_NON_ANCHORING, COND_DISCOUNTED)`) — **`COND_DOWN_WEIGHTED` is not excluded**, so a source whose population-directness for this exact population was *never assessed at all* still counts as an anchor, and `state='stated'` is reached with `n_axes>=2`.
NOTE      : **This is the run's central finding.** `evidence-architecture.md` G2 states, as doctrine: *"Absence of assessment is never treated as evidence of directness."* Mechanically, that is honored at the level of the *directness grade* (NOT_ASSESSED is correctly never graded EXACT) — but it is **not** honored at the level of the *state machine*: a cell can reach the highest-confidence `stated` state, meant to render at full `●` anchoring strength, while **zero** of its governing sources have ever had their applicability to the named population checked. Nothing in `validate_evidence_state.py`'s three contract criteria (entry 9) catches this, because none of them inspect per-source `population_directness`; they operate on `governing_refs`, `code_floor_only`, `regulatory_stratum_only`, and convergence-`status` only. For the mobility batch, this matters directly: the only slug with real evidence is not a mobility slug, and if it were ever cross-linked to a mobility item, a `stated` cell could result with no population vetting at all, undetected by every gate exercised in this run.

---

### 16. `pmp_audit.py` against canonical DB — vacuous pass
INVOKED   : `GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/audit/pmp_audit.py`
STAGE     : judgment (feeds from research stage, per pipeline-contract.yaml `pmp-strict-termination` is filed under `research`, but the walk *writer* and its consuming table `spec_value_probes` sit in my table list, so exercised here)
EXIT      : 0   RUNTIME: <1s
READS     : `spec_value_probes` (0 rows), `items` (via `pmp_last_walk_at` presence check)
WRITES    : NONE (read-only audit)
EXAMINED  : 0
OUTPUT    : `[CHECK 1..6] ... 0` for every check, `ISSUES: 0`, `EXAMINED: 0`
FINDING   : VACUOUS
LOCATION  : `scripts/audit/pmp_audit.py:181` (does correctly print `EXAMINED`, so the vacuity is visible to a caller who checks — but a caller who only checks exit code 0 would not notice)
NOTE      : Another live, present-tense CLAUDE.md §2(a) instance, exactly like entry 7.

---

### 17. Four synthetic PMP walks written by hand SQL (no writer exists)
INVOKED   : `$SMOKE/write_pmp_test.py` — raw SQL against `spec_value_probes`; confirmed via `grep -n "probe\|pmp" scripts/db.py` (0 hits) that no CLI subcommand exists. `skills/progressive-measurement_SKILL.md:128-138` itself teaches a raw `INSERT INTO spec_value_probes (...)  VALUES (...)` block — the skill's own sanctioned procedure IS hand SQL.
STAGE     : judgment
EXIT      : 0   RUNTIME: <1s
READS     : NONE
WRITES    : `spec_value_probes` 11 rows across 4 walks on item `E-03` (ramp gradient) × MOB, slug `stair-ramp-threshold-biomechanics-accessibility`:
  - `WALK-E03-A`: complete, compliant (5 steps, ends `phase='final'`, consistent `claim_type='maximum'`/`direction='down'`)
  - `WALK-E03-B`: incomplete (2 steps, no `final` phase)
  - `WALK-E03-C`: direction/claim_type mismatch (`claim_type='minimum'`, `direction='down'`, should be `'up'`)
  - `WALK-E03-D`: `passes_strict=1` step with `ref_id=NULL` (ungrounded pass)
EXAMINED  : n/a (writer)
OUTPUT    : all 11 rows committed, schema-valid
FINDING   : BLOCKED (no sanctioned path) — hand SQL used, logged, matches the skill's own taught procedure exactly
LOCATION  : `skills/progressive-measurement_SKILL.md:128-138`; `scripts/db.py` (no `probe`/`pmp` subcommand)
NOTE      : n/a (see entry 18)

---

### 18. `pmp_audit.py` against the 4 synthetic walks — every injected defect caught, plus one absence exposed
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s3-judgment.db python3 scripts/audit/pmp_audit.py`
STAGE     : judgment
EXIT      : 1   RUNTIME: <1s
READS     : `spec_value_probes` (11 rows), `items` (`pmp_last_walk_at` column)
WRITES    : NONE
EXAMINED  : 11
OUTPUT    :
```
[CHECK 1] Items with numerical specs lacking PMP walk: 1   ⚠ E-03 [...]  <- fires even for the item with a COMPLETE compliant walk
[CHECK 2] Incomplete PMP walks (no 'final' phase reached): 1  ⚠ walk=WALK-E03-B
[CHECK 3] PMP walks with no passing strict step: 0
[CHECK 4] PMP passing steps citing ineligible sources (rule #10): 0
[CHECK 5] Passing PMP steps without ref_id: 1  ⚠ PMP-E03-D-1
[CHECK 6] direction/claim_type inconsistency: 2  ⚠ PMP-E03-C-1, PMP-E03-C-2
ISSUES: 5   EXAMINED: 11
```
FINDING   : PASS (checks 2, 5, 6 correctly caught their designed defects) / FAIL (check 1, see location)
LOCATION  : `scripts/audit/pmp_audit.py:60-79` (CHECK 1 gates on `items.pmp_last_walk_at IS NULL`) vs `scripts/db.py` (**no `update-item` subcommand exists at all** — confirmed by grep, 0 hits for `update-item`/`update_item`)
NOTE      : Even `WALK-E03-A` — a fully complete, internally consistent, correctly-terminated walk exactly per the skill's own algorithm — still trips CHECK 1, because the walk's own final step (`skills/progressive-measurement_SKILL.md:110`: `update_item(item_code, pmp_empirical_ceiling=..., pmp_gap_signed=..., pmp_last_walk_at=now())`) has **no writer anywhere in the codebase.** `add-item` exists (insert-only); nothing updates an existing item's `pmp_*` columns. The skill's own algorithm pseudocode names a write operation that the CLI cannot perform and that no other script performs either.

---

### 19. `db.py add-conflict` — a real, sanctioned, working writer (positive finding)
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s3-judgment.db python3 scripts/db.py add-conflict --item-code C-05 --domain flooring --pop-a DEM --pop-b MOB --status ACTIVE --evidence "..." --session session_2026-08-25-pipeline-smoke-test-mobility-S3`
STAGE     : judgment
EXIT      : 0   RUNTIME: <1s
READS     : `_VALID_CONFLICT_STATUS` vocabulary, `items` (FK check on `C-05`)
WRITES    : `conflicts` row `CONF-0001` (C-05 flooring conflict, DEM vs MOB — the PROTOCOL's own canonical mobility conflict case: low-LRV-differential flooring for DEM vs firm/low-pile wheeled-mobility surfaces)
EXAMINED  : n/a (writer)
OUTPUT    : `{"conflict_id": "CONF-0001", "dry_run": false}`
FINDING   : PASS
LOCATION  : `scripts/db.py:1127-1141` (`add-conflict` subcommand), auto-generates `conflict_id`
NOTE      : **This is a genuinely functional sanctioned writer, unlike entries 1/8/11/17.** `conflicts` is the one judgment-adjacent table in this whole run with real, working CLI coverage — no hand SQL required.

---

### 20. Nothing forces a judgment to acknowledge a registered conflict
INVOKED   : `grep -rn "conflicts" scripts/assess/assess_cell.py scripts/validate_evidence_state.py scripts/audit/*.py`; `sqlite_master` scan for any view joining `specifications` to `conflicts`
STAGE     : judgment
EXIT      : 0   RUNTIME: <1s
READS     : `scripts/assess/assess_cell.py` (0 hits for "conflict"), `scripts/validate_evidence_state.py` (0 hits), all views in `sqlite_master`
WRITES    : NONE
EXAMINED  : both scripts in full, all views in the schema
OUTPUT    : no hits in either script; no view joins `specifications` and `conflicts`
FINDING   : ABSENT
LOCATION  : n/a — the absence itself is the finding
NOTE      : `CONF-0001` (entry 19) now sits in the DB stating that C-05 is contested between DEM and MOB. Nothing prevents (or even flags) a `specifications` row for C-05×MOB or C-05×DEM being written — by hand SQL or, if it existed, by a sanctioned path — with no reference to the registered conflict. `skills/cross-population-conflict-mapper_SKILL.md:212,220` names `item-specification-writer` as a downstream consumer in prose only; `item-specification-writer_SKILL.md`'s own "Before writing" query list (steps 1-5) never queries `conflicts`.

---

### 21. `item_audit_runs` — a real, sanctioned, working writer (positive finding)
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s3-judgment.db python3 scripts/db.py add-audit-run --item-code E-03 --session session_2026-08-25-pipeline-smoke-test-mobility-S3 --status IN-PROGRESS`, then `update-audit-run --run-id ... --status COMPLETE --steps-complete '["evidence-auditor","functional-deficit-auditor"]'`, then `audit-runs --item E-03`
STAGE     : judgment
EXIT      : 0 (all three calls)   RUNTIME: <1s each
READS     : `_VALID_RUN_STATUS` vocabulary, `items` FK
WRITES    : `item_audit_runs` row `E-03_session_2026-08-25-pipeline-smoke-test-mobility-S3`, created then updated
EXAMINED  : n/a (writer) then 1 (query)
OUTPUT    : clean JSON round-trip; `audit-runs --item E-03` returns the row with `status: "COMPLETE"`, `steps_complete` correctly JSON-encoded
FINDING   : PASS
LOCATION  : `scripts/db.py:1191-1216` (`add-audit-run`/`update-audit-run`/`audit-runs`)
NOTE      : `item_audit_runs` is process bookkeeping only (which pipeline steps ran, in what order) — it is read downstream only by `scripts/audit_consolidator.py` (which writes a markdown brief to `references/audit-briefs/`, not `specifications` rows). It proves a *pipeline ran*, never that a *determination is correct*.

---

### 22. Judgment-stage skills swept — mechanical attempt on each
INVOKED   : direct reads of all 8 named skill files + targeted greps
STAGE     : judgment
EXIT      : n/a (read-only survey)   RUNTIME: <1s per file
READS     : `skills/item-specification-writer_SKILL.md` (234 lines, full), `skills/specification-curator_SKILL.md` (99 lines, full), `skills/cross-population-conflict-mapper_SKILL.md` (grep only), `skills/progressive-measurement_SKILL.md` (140/225 lines), `skills/item-audit-pipeline_SKILL.md` (grep + first 50 lines), `skills/functional-deficit-auditor_SKILL.md` (grep + targeted sections), `skills/evidence-auditor_SKILL.md` (grep), `skills/adversarial-research_SKILL.md` (grep)
WRITES    : NONE
EXAMINED  : 8 skill files
OUTPUT    : per-skill verdict table below (see S3 SUMMARY)
FINDING   : mixed — see summary table
LOCATION  : see summary table
NOTE      : Two defects worth naming individually here:
  1. **`item-specification-writer_SKILL.md:73-94` and `specification-curator_SKILL.md:67-69`** both instruct writing `specifications` "via migration" / "ships as a migration" — **neither names `assess_cell.py` or any script**, and per entry 1 no CLI writer exists. The skills teach exactly the hand-SQL-then-migration pattern CLAUDE.md §4 says the 2026-08-19 fabrication entered through, for the one table where that gap was never actually closed.
  2. **`functional-deficit-auditor_SKILL.md` §2 (lines 77-155)** hardcodes a "Population↔ICF Mapping" table directly in skill markdown prose. `evidence-architecture.md` §5.5 (H3) calls exactly this pattern out by name as needing to become "data, not skill prose" via a `population_icf_links` table — confirmed absent from the live schema (`sqlite_master` has no such table). The skill still operates exactly the way the doctrine says is the problem.
  3. **`adversarial-research_SKILL.md:58-72,137-140`**: the four falsifiable fields (`falsification_condition`, `confidence_interval`, `shift_conditions`, `named_dissenter`) are written via `UPDATE gaps SET ...` — landing on the **`gaps`** table, which independently carries all four columns (confirmed via schema read). `specifications` *also* has its own `falsification_condition` column, populated by `assess_cell.py`'s own English-sentence generation (`assess_cell.py:398-399` etc.), with no pointer between the two. The two columns hold different semantic content by design (gap-level dissent-tracking vs cell-level derivation-overturn condition) so this is not a clean rule-5 duplicate — but it is the same field name doing related work in two stage-owned tables with no cross-reference, which is exactly the shape rule 5 exists to prevent drifting into one.

---

### 23. `specification_source_links` — the render join table has zero rows and no writer
INVOKED   : `sqlite_master` schema read; `grep -n "specification_source_links" scripts/assess/assess_cell.py scripts/db.py`
STAGE     : judgment / render boundary
EXIT      : 0   RUNTIME: <1s
READS     : `specification_source_links` schema + row count; `scripts/generate/spec_page.py:87-100` (its own code comment)
WRITES    : NONE
EXAMINED  : full schema + both scripts
OUTPUT    : `specification_source_links`: 0 rows. `assess_cell.py` never inserts into it — it writes `governing_refs` as a JSON array column on `specifications` instead. `spec_page.py:88-91`'s own comment: *"Until migration 044 this edge lived only as a JSON array in specifications.governing_refs, which this generator never read -- so every page it produced cited nothing at all while presenting a confident determination. specification_source_links makes it a join."*
FINDING   : FAIL
LOCATION  : `scripts/generate/spec_page.py:87-100` (reads `specification_source_links`); no writer anywhere in `scripts/assess/assess_cell.py` or `scripts/db.py`
NOTE      : The historical bug `spec_page.py`'s own comment describes ("every page cited nothing while presenting a confident determination") is functionally **still live today**, just relocated: the render code was fixed to read the *correct* table, but nothing was ever built to populate that table. `assess_cell.py` still only writes the JSON-array `governing_refs` column the comment says the render code no longer reads. A `stated` cell rendered today would show its determination with **zero citations**, silently — precisely the "0-row object as unproven, not clean" trap CLAUDE.md §0.4 names for `v_item_provenance`, recurring one migration later, one layer over.

---

### 24. Handoff to synthesis — mechanically does not exist
INVOKED   : `sqlite_master` search for any table/view containing "synthesis"; `grep -rln "FROM specifications\|JOIN specifications" scripts/`
STAGE     : judgment / synthesis / render boundary
EXIT      : 0   RUNTIME: <1s
READS     : full `sqlite_master`, `scripts/generate/spec_page.py:77-79`, `scripts/generate/population_page.py:79-81`, `scripts/generate/build_site.py:66-100`
WRITES    : NONE
EXAMINED  : entire schema (all tables/views), 3 render-generator scripts
OUTPUT    : No table or view named `best_practice_synthesis` (or containing "synthesis" at all) exists anywhere in `data/guidebook.db` — only `bpc_metadata` and `item_bpc_links`, which track markdown-file synthesis metadata, not synthesis content. Every reader that queries `specifications` forward is a **render**-stage script (`spec_page.py`, `population_page.py`, `build_site.py`) querying it **directly**: `spec_page.py:77`: `"...FROM specifications WHERE item_code = ?"`.
FINDING   : ABSENT
LOCATION  : `governance/pipeline-contract.yaml`'s `synthesis` stage anchor names `best_practice_synthesis` as the stage's table (line ~93: `anchor: "best_practice_synthesis / ISW; ..."`) — this table does not exist in the live schema.
NOTE      : The literal, mechanical answer to "what does synthesis receive from judgment, and is the handoff enforced": **there is no DB-level synthesis-stage artifact for judgment to hand off to.** Render reads `specifications` (judgment's own output table) directly. Synthesis, as a stage, exists in doctrine (BPC markdown prose on GitHub, `references/bpc/{slug}.md`, per `item-specification-writer_SKILL.md` step 5) and partially inside judgment's own code (`assess_cell.py` computes `convergence_assessment`, which pipeline-contract.yaml's own synthesis-stage description calls "weighing, convergence, cross-slug findings" — yet `convergence_assessment` is one of *my* assigned judgment-stage tables per this run's brief). The stage boundary between judgment and synthesis is not just unenforced — it is not consistently drawn between governing documents, exactly the ambiguity CLAUDE.md's 2026-08-25 "THE PIPELINE" section (added the same day as this test) was written to force a re-derivation against, rather than reading off any one document.

---

### 25. Final integrity check
INVOKED   : `sha256sum data/guidebook.db`
STAGE     : n/a (protocol compliance check)
EXIT      : 0
READS     : `data/guidebook.db` bytes only
WRITES    : NONE
EXAMINED  : 1 file
OUTPUT    : `30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf  data/guidebook.db` — identical to the hash recorded at the start of this run.
FINDING   : PASS
LOCATION  : n/a
NOTE      : Canonical DB confirmed untouched throughout. All writes in this run landed exclusively in `$SMOKE/s3-judgment.db`.

---

## S3 SUMMARY

### (a) Verdict table — every skill/script/gate invoked

| # | Surface | Sanctioned writer exists? | Runs? | Teaches/requires hand SQL? | Retired vocab / wrong stage names? | Verdict |
|---|---|---|---|---|---|---|
| 1 | `scripts/db.py` (`specifications` coverage) | **NO** | n/a | — | — | **ABSENT** |
| 2 | `scripts/assess/assess_cell.py` | N/A (only writer, but hardcoded to 7 cells, refuses canonical DB) | Crashes unmodified (entry 3) | No (it's Python, but is the *only* alternative to hand SQL, and can't target arbitrary cells) | No | **FAIL** (broken) |
| 3 | `scripts/validate_evidence_state.py` | n/a (validator) | Yes, correctly | No | No | **PASS** (once given a subject) |
| 4 | `external_root_registry` / `v_value_independence` / `v_unregistered_roots` | **NO** | Views run fine | Yes (only option) | No | **FAIL** (undercounts on typo; no writer; stale row-count claim in governance doc) |
| 5 | `evidence_population_match` consumption | n/a (reader) | `assess_cell.py` reads it | — | — | **FAIL** (NOT_ASSESSED sources still anchor `stated`; dissenting duplicates invisible to reader) |
| 6 | `scripts/audit/pmp_audit.py` | n/a (auditor) | Yes, correctly | — | — | **PASS** (all injected defects caught) |
| 7 | `spec_value_probes` writer | **NO** | n/a | Yes (skill teaches raw INSERT) | No | **ABSENT** |
| 8 | `items.pmp_*` writer (`update_item`) | **NO** | n/a | Skill names it, gives no SQL | No | **ABSENT** |
| 9 | `scripts/db.py add-conflict`/`update-conflict`/`conflicts` | **YES** | Yes | No | No | **PASS** |
| 10 | conflict→judgment enforcement | **NO** | n/a | — | — | **ABSENT** |
| 11 | `scripts/db.py add-audit-run`/`update-audit-run`/`audit-runs` | **YES** | Yes | No | No | **PASS** (process bookkeeping only) |
| 12 | `item-specification-writer` skill | n/a | Teaches unenforceable step | Yes (implicitly, "via migration") | No | **FAIL** |
| 13 | `specification-curator` skill | n/a | Teaches unenforceable step | Yes (implicitly) | No | **FAIL** |
| 14 | `cross-population-conflict-mapper` skill | writer exists (#9) | Yes | No | No | **PASS** (doctrine-only tie to specifications) |
| 15 | `progressive-measurement` skill | **NO** | Teaches unenforceable steps | Yes (explicit SQL) | No | **FAIL** |
| 16 | `item-audit-pipeline` skill | writer exists (#11) | Yes | No | No | **PASS** |
| 17 | `functional-deficit-auditor` skill | writer exists (`add-gap`) | Yes for gaps; ICF mapping is unvalidated prose | No for gaps; the ICF table itself is hardcoded prose | No | **PASS**/FAIL split (see #22.2) |
| 18 | `evidence-auditor` skill | writer exists (`add-gap`) | Yes | No | No | **PASS** |
| 19 | `adversarial-research` (falsifiable fields) | writer exists (`gaps` via raw SQL in skill text) | Yes | Yes (raw `UPDATE`) | No | **PASS**/caution (dual-home risk with `specifications.falsification_condition`, #22.3) |
| 20 | `specification_source_links` (render join) | **NO** | n/a | — | — | **ABSENT/FAIL** |
| 21 | Synthesis handoff (`best_practice_synthesis`) | **NO — table doesn't exist** | n/a | — | Stage-boundary disagreement between governing docs | **ABSENT** |

### (b) Ranked blockers for a real mobility batch

1. **No sanctioned writer for `specifications` at all** (entry 1). The judgment stage cannot record a determination for any item×population pair through anything `scripts/db.py` provides. `scripts/assess/assess_cell.py:483-486` (no `--item`/`--population` args, hardcoded `PILOT_CELLS:116-131`).
2. **The one writer that exists is currently broken against the live DB**, crashing on cell 1 of 7 (`assess_cell.py:427-428`, gap-id zero-padding vs `gaps.gap_id`'s current `GAP-B0N-NNN` format) and, once patched, on cell 7 (`assess_cell.py:129`, population code `NEU` not in `populations`).
3. **Even patched and complete, it produces zero `stated`/`provisional` cells** for any of its 7 demonstration pairs, mobility ones included (E-12×MOB, E-06×MOB), because `source_slug_links` now links only 1 of 106 slugs to any evidence at all (entry 6), and that one slug is not a mobility slug.
4. **A determination CAN reach `stated` with zero population-directness assessment for its target population** (entry 15) — `assess_cell.py:246`'s `anchoring()` doesn't exclude `COND_DOWN_WEIGHTED`, and no gate in `validate_evidence_state.py` checks per-source `population_directness` before allowing `stated`. This is the most consequential live defect for correctness, not just completeness.
5. **The render-stage citation join (`specification_source_links`) has no writer and 0 rows** (entry 23) — even a correctly-written `stated` cell renders with no visible citations, a recurrence of a bug the code comments say was already fixed once.
6. **`spec_value_probes` and `items.pmp_*` have no writers**, only skill-taught raw SQL (entries 17-18) — PMP's own audit still flags a fully complete, compliant walk as "missing" because the walk's own completion step cannot be performed by any tool.
7. **Conflicts are recorded but never consulted** (entries 19-20) — a real, working writer exists, but nothing connects a registered conflict to a determination for the same item.
8. **Root-independence counting silently undercounts on a one-character root-id typo** (entries 11-12), and nothing enforces registration.
9. **No mechanical handoff to synthesis exists** (entry 24) — `best_practice_synthesis` is absent from the schema; render reads judgment's table directly.

### (c) The ABSENT list

- `scripts/db.py add-specification` / `update-specification` — does not exist.
- `scripts/db.py` writer for `spec_value_probes` (PMP probe rows) — does not exist; skill teaches raw SQL.
- `scripts/db.py` writer/updater for `items.pmp_empirical_ceiling` / `pmp_gap_signed` / `pmp_last_walk_at` / `pmp_direction` / `pmp_delta_min` — does not exist at all (not even `add-item` covers update).
- `scripts/db.py` writer for `external_root_registry` / `source_value_extractions` — does not exist.
- `scripts/db.py` writer for `specification_source_links` — does not exist; `assess_cell.py` doesn't write it either.
- `population_icf_links` table (named in `evidence-architecture.md` H3 as the fix for "unvalidated skill prose") — does not exist.
- `best_practice_synthesis` table (named as the synthesis stage's own anchor in `governance/pipeline-contract.yaml`) — does not exist.
- Any FK/CHECK/trigger enforcing `source_value_extractions.root_id ∈ external_root_registry.root_id` — does not exist.
- Any mechanism reading `conflicts` from `assess_cell.py`, `validate_evidence_state.py`, or `item-specification-writer`'s query steps — does not exist.
- Any view or code path consuming `v_value_independence`, `v_unregistered_roots`, or `v_root_id_conflicts` from inside the determination engine — does not exist; these views compute correctly but are orphaned from the write path.

### (d) Direct answer

**Can this repository record a judgment about a mobility item today, through sanctioned means?** No. There is no CLI subcommand, no `db.py` path, and no working general-purpose script that can write a `specifications` row for an arbitrary item×population pair. The only production writer (`assess_cell.py`) is hardcoded to 7 non-mobility-representative pairs, crashes on the live DB unmodified, and — even repaired — produces no positive determination for any mobility pair because the evidence substrate it would need (`source_slug_links`) is empty for every mobility slug. Recording one requires hand-written SQL against a table `db.py` cannot reach, exactly the pattern CLAUDE.md §4 says should no longer be necessary anywhere in this codebase — and here, for the judgment stage's own primary output, it still is.

**If the judgment were wrong, would anything catch it?** Partially, and unevenly. The three pipeline-contract criteria that exist (`governing-refs-nonempty`, `no-regulatory-stratum-stated`, `tier3-alone-threshold`) all fire correctly and precisely the moment they have a subject (entry 9) — that machinery is sound. But this run also demonstrated, with real corpus evidence and no fabrication, a `stated` determination (A-05×SCI, entry 15) that no existing gate flags, built entirely from sources whose applicability to the target population was never checked — because the state machine treats "down-weighted for lack of assessment" the same as "anchoring." A wrong judgment of exactly that shape — the shape most likely to occur for the mobility batch, given the population-match table's complete silence on MOB (entry 13) — would pass every check exercised in this run.
