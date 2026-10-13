# C-tier-marker — rehearsal report (R7 three markers; plan P6/P18)

Clone: `scratchpad/rehearsals/C-tier-marker`, branch `d3` (implemented), branches `d1` and `d2` (the two rejected designs, kept for inspection). Base `31142552`. Patch: `scratchpad/rehearsals/C-tier-marker.patch` (applies cleanly to `31142552`; DB blob excluded). The rejected designs: `C-tier-marker-design1.patch`, `C-tier-marker-design2.patch`.

## Verdict

- **R7 as a marker rule: EXECUTABLE WITH CHANGES.** Three markers, computed by the engine, one stored home (`specifications.marker`), a CHECK that holds the two invariants, `--rebuild` identical, no gate worse than baseline. The changes: the band source is a pure function, not a `tier_ladder` table; the determination's band needs the owner's 2026-09-13 floor-of-the-mean ruling and LED-020, which R7 does not cite; the proxy determination is not covered by R7's wording.
- **P6 "`tier_ladder` as data": NOT EXECUTABLE as the better design.** Measured as the worst of the three: 9 files, +107/−75, 7 production call sites in 3 files need a connection, and 2 blocking checks plus `build_graph --check` go red.
- **P18 "marker + CHECK + engine INSERT in one PR": EXECUTABLE AS WRITTEN**, and no table rebuild is needed. `ALTER TABLE … ADD COLUMN` with sibling-referencing CHECKs leaves the AUTOINCREMENT sequence, the 065 lens CHECK, 3 inbound FKs, the identity index, the retirement trigger and 7 views untouched.
- **adjudication_integrity: EXECUTABLE AS WRITTEN.** It now prints `EXAMINED: <n>` and flags a NULL tier or type instead of skipping it.

## 1. The three band-source designs, measured as diffs from `31142552`

Each diff is the band source only: the band rule, `floor_mean`, `EvidenceMarker` made three-valued, and whatever existing callers had to change to stay green. The marker column, the engine and the test fixes are common to all three and are measured in §2.

| | (1) band in `TIER_MAP` | (2) `tier_ladder` table | (3) pure function |
|---|---|---|---|
| diff (code) | 4 files, +43/−29 | 9 files, +107/−75 (incl. 32-line migration, 20 lines of `db.py`) | **2 files, +22/−6** |
| callers changed | 10 test sites (TIER_MAP's values become tuples), plus `scope` added to the engine's per-source record [estimated +1, not run] | needs a connection: `assess_cell` 1, `adjudication_integrity` 2 (its pure `tier_violations` and its selftest), `db.py` 4 (including argparse construction at import for `--evidence-type`). 3 test files copy the ladder into fixtures or open the live DB. `expected_scope_from_tier` deleted (no caller) | **0** |
| homes of the band rule | 1 (TIER_MAP) | 1 (table rows, written by a schema migration) | 1 (`band()`) |
| homes of the glyph vocabulary | 2 (`EvidenceMarker`, `specifications.marker` CHECK) | **3** (+ `tier_ladder.band` CHECK) | 2 |
| homes of the `scope` vocabulary | 2 (unchanged) | **3** (+ `tier_ladder.scope` CHECK) | 2 (unchanged) |
| hard-coded literals | 10 per-rung band assignments | 10 data rows plus 3 CHECK lists | 5 tokens (`3`, `3`, `3`, `6`, `"clinical"`): §5 is itself stated in tier numbers |
| ordinal literals (3/2/1) | 0 (enum order) | 0 | 0 |
| testability | pure | needs a DB (selftest now opens the live DB) | pure |
| gates | tests green [only the 3 affected tests run] | `--all`: **`pipeline_completeness_fresh` (blocking), `derived_not_curated_audit` (blocking)**, `pipeline_walk_fresh` go red; `build_graph --check` FAIL (`tier_ladder` not in stage-map). CLAUDE.md §4 would also demand a Pydantic mirror unless R5 lands | green (§2) |
| survives NULL-forwarding `evidence_sources.tier` | yes (keyed on type, scope) | yes | no as written. One line fixes it: `band(derive_tier(type, scope), type)` |

Findings from the measurement:
- **A SQLite CHECK cannot consult another table**, so `tier_ladder.band` could never have constrained `specifications.marker`. A ladder table buys no integrity the function lacks.
- **Design 2 trips the `--tier` literal.** `derived_not_curated_audit` matches the flag name `--tier` to a column named `tier`. Once `tier_ladder.tier BETWEEN 1 AND 6` exists, it flags `add-supersession-check --tier choices=[1,2,3,4,5,6]` as blocking. Today it passes only because no column is literally named `tier` with a CHECK: `evidence_sources.tier` has none, and the flag really writes `supersession_check.anchor_tier`.

**Recommendation: design 3**, implemented in commit `93a1473`. It has the fewest lines, no new table and no new map, one home for the rule, the fewest literals, and it is pure and testable. Its one weakness is that it reads the stored tier, which stops working if tier is NULL-forwarded. That is a one-line change on the day tier retires, and the strengthened `adjudication_integrity` goes red before then.

## 2. Steps implemented (branch `d3`)

| commit | what | files | +/− |
|---|---|---|---|
| `93a1473` | `band(tier, type)` and `floor_mean(bands)` in `schemas/tier_derivation.py`; `EvidenceMarker` = FULL/PARTIAL/WEAK, with the order as the ordinal | 2 | +22/−6 |
| `c47620c` | migration `102_specification_marker.sql`: ADD COLUMN `marker` with 2 CHECKs, and `v_best_practice` redefined without `strength_band`. Engine computes and writes the marker; `EvidenceStateRecord.marker`; 4 tests fixed; marker cases added | 7 | +167/−33 |
| `8a7997d` | `adjudication_integrity`: `EXAMINED: <n>`; NULL tier/type is a violation; selftest inverted | 1 | +9/−7 |
| `6c0d1d4` | regenerated `tools/pipeline-completeness-dashboard.html` (backs a **blocking** check) and `tools/pipeline-walk.html` | 2 | +3/−3 |
| `2ef5ab1`, `e44bc10`, `0ff75c1` | prose callers of `strength_band`: one `assess_cell.py` comment, plus `governance/evidence-architecture.md` :119 and :206 and `evidence-methodology.md` :144 (**owner merge**, doctrine files). :119 keeps the phrase atom EVI-182 quotes, otherwise `build_graph --check` fails | 4 | +9/−9 |
| **total** | | **14** | **+208/−56** |

Split: code +79/−24, tests +79/−25, migration +44, governance prose 3/3, generated HTML 3/3. **The step adds more lines than it removes (net +152).** Of that, the R39 confirmation route alone costs 17 engine lines and 13 test lines, and it reaches 0 live edges (see §4).

**The engine rule as built** (`determine()`, after the H4 cap):
- Only `stated` and `provisional` rows carry a marker.
- Normally, each governing source takes its §5 band, and the cell takes the floor of the mean (owner 2026-09-13). On every governing set the engine can build today, that equals "the governing anchor's band", because sets are single-band by construction.
- If the value comes from the regulatory stratum (`regulatory_stratum_only` or `rests_on_proxy_inference`):
  - each governing code is ○, unless a `confirms` edge from an anchoring finding reaches that code's governing extraction row;
  - such a code takes the confirming study's band (floor-mean when several confirm it);
  - the cell takes the floor-mean.

**Migration 102.** Two column CHECKs:
- `marker IS NULL OR (marker IN ('●','◐','○') AND (regulatory_stratum_only = 0 OR marker = '○'))`
- `retired_at IS NOT NULL OR (state IN ('stated','provisional')) = (marker IS NOT NULL)`

`dbcore.check_values('specifications','marker')` reads `{●,◐,○}` from the CHECK. SQLite 3.45 validates an added CHECK against existing rows: an un-retired provisional row made the ALTER fail on a probe copy. The migration declares `-- AFTER_DATA: 20261010002423`. With the marker removed, `--rebuild` still passes, because 095's marker (20260920060857) already places 102 after every `specifications` write (the last is `data_20260918201549`). So the marker records the chronology, as 086's does. It is not load-bearing today.

**The four tests.** Measured with their baseline text against the live CHECK, all four fail:
- `test_evidence_cell_state_2_3`, `test_validate_evidence_state_2_4`, `test_db_amend_writers`: `IntegrityError`.
- `test_assess_cell_pilot`: 4 FAILs in the DDL probe.

The fixes:
- Every live stated/provisional row these tests write or un-retire now carries a marker taken from `EvidenceMarker` (never a typed glyph).
- In `test_db_amend_writers`, X12 and E10 un-retire with `○`, which is legal on any row; E10 restores `marker=NULL` along with the retirement.

The fixes are also what keeps the refusal assertions meaningful. Without a marker, every `reject(...)` in `test_evidence_cell_state_2_3`, and `test_assess_cell_pilot`'s "population_only … REFUSED", would pass vacuously on the marker CHECK. In the probe, only the positive control exposed this.

**Gates** (base = this clone at `31142552`, measured; earlier figures not reused):

| check | baseline | after |
|---|---|---|
| `run_checks --all` | 67 green / 7 none / 11 advisory red | 66 green / 7 none / 12 advisory red |
| `research_tooling_separation` (advisory) | PASS | FAIL: **clone artefact**, `origin/main` = `3077b99` is older than the base and carries 3 later data migrations; `--base 31142552` → PASS, EXAMINED 11 |
| `pipeline_completeness_fresh` (blocking) | PASS | PASS after regeneration (red before it) |
| `pipeline_walk_fresh` | PASS | PASS after regeneration |
| advisory reds already red at baseline | `validate_pydantic_schemas` 213, `retired_vocabulary` 86, `research_protocol_audit` 18, `migration_reproducibility_deep` and `validate_schema_cross_check` bodies | identical counts and bodies (`EvidenceStateRecord.marker` keeps the pydantic drift at 213) |
| `--selftest` | PASS | PASS |
| `schema_reference_audit` | PASS, 1111 refs | PASS, 1114 refs |
| `build_graph --check` | 0 failures, 5 warnings | 0 failures, 5 warnings |
| `--rebuild` vs clone DB | — | 82 tables, 21 views, 95 indexes, 1 trigger: identical names and DDL; every row count equal except `pipeline_runs` 6/0 (exempt); `specifications` rows identical; sequence 8/8 |
| `--changed-from 31142552` | — | PASS, no blocking red |

**End to end on a scratch copy:**
- `assess_cell.py --parameter-id 3 --identity MOB` writes `provisional ● basis=T1`, capped by an open H4 gate. Two fresh copies emit byte-identical SQL.
- `validate_evidence_state --db` on the scratch copy: PASS.
- `data/guidebook.db` in the real repository was never written. The clone's own DB moved only through `migrate_db.py`.

**Sweep (rule 4):**
- `strength_band` has no code reader. `tools/evidentiary_audit.py` has a slice-level variable of that name, not the view's column. Its other remaining home is the empty `item_taxonomy_links` table, which step 1.2 drops.
- `EvidenceMarker`'s old members had **zero readers anywhere**.
- No view or trigger reads `v_best_practice`.

## 3. Owner-merge edits made in the clone (list separately)

- `governance/evidence-architecture.md` :119 and :206, and `governance/evidence-methodology.md` :144: "`strength_band` column" → the row's `marker` (migration 102).
  - :119 keeps the quoted phrase, so atom EVI-182 still resolves. EVI-182's claim is now historical; whoever next rebuilds the graph should mark it SUPERSEDED.
  - :144's "3 weak-band rows are queryable today" was already false (all 8 rows are retired); it is now dated 2026-08-05.
- **Not made (rotates the doctrine sha):** `governance/mission-and-epistemics.md:136`, R7's mission line. Proposed text: "Every Part-4 specification carries an evidence marker per `tier-system.md` §5/§8: ● (T1, Co-1, T2, Co-2, T3-clinical), ◐ (T4, T5: standards basis), ○ (T3-grey, T6, expert consensus, thin base); a determination carries the band `assess_cell` computes. Unmarked = error."

## 4. What the documents determine, and exactly what they do not

**Determined and implemented:**
- §5 source bands.
- Option A §2.3: a T4–T6-only determination takes ○, even with T4/T5 sources present.
- Owner 2026-09-13: a multi-input band is floor(mean(ordinals)), with ordinals 3/2/1. All five rows of the owner's table are asserted in `test_assess_cell_pilot`.
- Owner 2026-09-13: a code value without research backing is ○, and a code value confirmed by study is upgraded.
- Ledger "mechanism": a `confirms` edge triggers the upgrade and a `tested_at` edge does not. Both are asserted.
- LED-020: ● needs value-level support. A proxy's direction-only basis therefore never reaches ●.

**Not determined; the reading implemented is marked:**
1. **The upgraded band.** The ledger says "Do not assume which band an upgraded value takes — that is unruled". Only the proposed R39 says it is the study's band. Implemented as R39, so it depends on R39 being entered.
2. **Partial confirmation**, where some but not all governing codes are confirmed. Reading: the floor-mean over confirmed (study band) and unconfirmed (○) codes.
3. **A `confirms` edge whose referent is a `to_label`**, not a row. It cannot reach a governing figure, so it upgrades nothing. All 3 live `confirms` edges are `to_label`, so **the upgrade fires on 0 live edges**.
4. **A T3-clinical confirming study.** The engine's direction anchors are T1/Co-1/T2/Co-2 only, so such a cell stays `regulatory_stratum_only = 1`, and the CHECK pins it at ○. R39 read literally gives ● (T3-clinical is ● at source level). REF-01003 is exactly this shape.
5. **The proxy determination**, where the value comes from codes and the direction from anchoring findings (owner 2026-09-16; migration 086).
   - R7's "T4–T6-only" does not reach it, because the engine sets `regulatory_stratum_only = 0` there.
   - Implemented as ○ unless confirmed: the 2026-09-13 upgrade ruling was put to the owner as exactly "finding T1, value from a code".
   - The CHECK cannot enforce this, because confirmation is not on the row. The rule lives only in the engine.
6. **The band of a `figure_role='derived'` row from its inputs** (floor-mean of the `derived_from` inputs) is ruled but **not built**. The engine bands a derived row by its recording source's tier. There are 0 derived rows today.
7. **Species §5 does not place:** T1 `grey` and T3 `standard_eb`, which tier-system §1 lists as "occasionally". `band()` gives ● and ○ respectively. Neither has a `TIER_MAP` rung, so both are tier-inconsistent and non-anchoring today.
8. **Inputs are weighted per distinct source, not per extraction.** This follows `gather_sources`' DISTINCT: one code's clauses do not outvote it.
9. **What the marker means on a provisional row.** A T3-clinical-only cell, or a stated cell capped by H4, is `provisional ●`. That is coherent (band = evidence strength, state = epistemic status), but 3.R must render both.

**◐ never appears on a determination the engine writes today.** Stated sets are all ●, regulatory sets are ○, and ◐ arises only from mixed inputs (a derived figure, or partial confirmation). In practice, ◐ is the citation-level marker Option A §2.3 says it is.

**Residual risk:** `derivation_sha` hashes the graded link set and `RULE_VERSION`, not `extraction_relations`. A `confirms` edge added after a determination changes its marker without moving the sha, so K01 cannot see the stale marker. `db.py` refuses re-tiering a source a live determination rests on (`determinations_resting_on`), but the relation writer has no equivalent refusal. Recorded, not fixed.

## 5. Defects in R7 and R9 found by implementing them

**R7:**
1. **Wrong section.** "Option A §3 (`:47-51`)" is DR-2026-07-21 **§2.3** ("Interpretive resolutions", item 3); §3 is "Doc edits applied". tier-system §8 itself cites §2.3. The plan and this brief repeat the error.
2. **Two premises omitted:**
   - The owner's 2026-09-13 rulings "a derived figure takes a WEIGHTED AVERAGE … not the weakest one" and "mean of band ordinals, ROUNDED DOWN". The first ruling's CONDITION names "implementing the band rule in the determination engine".
   - LED-020 (● needs value-level support).

   R7's "the governing anchor's band" is undefined for a mixed set; these rulings define it.
3. **The proxy determination is not covered.** "A T4–T6-only cell takes ○" does not reach a proxy cell (`regulatory_stratum_only = 0` by the engine's own rule). Read literally, R7 would give it the codes' §5 band (◐ for T4/T5), which contradicts the 2026-09-13 upgrade ruling.
4. **Confirmation by study rests on an unentered ruling.** "A code value confirmed by a study takes the study's band (R39)" overrides the ledger's "do not assume which band… unruled", so it depends on R39 being entered. In addition:
   - the trigger cannot fire on any live edge (all 3 are `to_label`);
   - a T3-clinical confirmer conflicts with the ○ CHECK (§4, item 4).
5. **"`EvidenceMarker` is fixed in code" misplaces the drift.** The enum had **no reader at all**. The defect was that nothing computed or stored a determination's marker; the enum becomes meaningful only once the engine and the model read it (they do now).
6. **"The plan's sequencing (ladder, then marker…) stands" is wrong.** The ladder is not a prerequisite, and as data it is the worst design measured (§1).
7. **Source-level list.** It omits §5's `[UNSUPPORTED]` (○) and says nothing about the two species §1 lists that §5 leaves unplaced (§4, item 7).

**R9:**
1. **Wrong line.** Engine line `:1510` is the H4 determination-gate cap, not "regulatory at richness → provisional". The richness branch is `:1329` at `31142552`.
2. **Mislabelled atom.** "PIP-03 (methodology 2.2: T3-grey alone → pending; single T6 → pending)": PIP-03 is the contract's tier3-alone-threshold criterion (`pipeline-contract.yaml:264`, "all Tier 3 … is provisional"). The atoms for T3-grey alone and a single T6 are EVI-326 and EVI-338.
3. **The inference "parity holds inside the weak band (one source → pending, converged sources → provisional)" is false for T3-grey.** `classify()` puts every non-clinical T3 source in `t3g`, and `elif b["t3g"]: state = "pending"` holds whatever the count. Three converging T3-grey sources stay pending, while three T6 codes in distinct jurisdictions reach provisional ○.
4. **R9 omits the owner's 2026-09-13 ruling** "grey literature that states a code's value is regulatory stratum". That ruling moves echoing T3-grey onto the T6 path, where it can reach provisional ○. The engine does not implement it (it buckets by stored tier; the rebuttable presumption is a proposal).
5. **Consequence for the marker:** "band only" changes no engine output. A T3-grey-only cell never carries a marker, so ○ on a determination comes only from the regulatory stratum.

## 6. Exact wording for the v4 plan's Phase 3 rows

**evidence** (replace the "**Tier**" sentences through "…`BETWEEN` CHECK."):

> **Tier and band** (`COMPARISON.md` P6; R7). Stop asking the operator for `--tier` in `add-source` and `amend-source`; derive it with `derive_tier(evidence_type, scope)`; keep the stored column. `adjudication_integrity` prints `EXAMINED: <n>` and reports a NULL tier or evidence_type as a violation (rehearsed: 1 file, +9/−7), so `tier` is never NULL-forwarded while it stands; promote it under 1.6. **No `tier_ladder` table.** The band is the pure function `band(tier, evidence_type)` in `schemas/tier_derivation.py` (tier-system §5), beside `floor_mean(bands)` (owner rulings 2026-09-13: floor of the mean of ordinals, the ordinal being `EvidenceMarker`'s order), and `EvidenceMarker` becomes FULL/PARTIAL/WEAK (rehearsed: 2 files, +22/−6, no caller changed). A ladder table was measured at 9 files, +107/−75, with a connection threaded into 7 production call sites, `pipeline_completeness_fresh` and `derived_not_curated_audit` (both blocking) and `build_graph --check` red, and it could not constrain `specifications.marker`, because a CHECK cannot read another table. The literal `choices=[1,2,3,4,5,6]` in `add-supersession-check --tier` is recorded, not fixed: the derivation is the one-for-one `dbcore.schema_range("supersession_check", "anchor_tier")` (no fewer lines), and the real defect is that the flag retypes `evidence_sources.tier` for the `--ref` it already names (rules 5 and 8). Fix `Co1SourceType` against the live values.

**specification** (replace "The determination's `marker` is deferred … (fifth pass)."):

> **The determination's marker** (`COMPARISON.md` P18; R7, R39). One tooling PR.
>
> - **Migration.** `NNN_specification_marker.sql` adds `specifications.marker` by `ALTER TABLE … ADD COLUMN`. It is not a table rebuild: the AUTOINCREMENT sequence, 065's lens CHECK, the three inbound foreign keys, `idx_spec_row_identity`, `trg_spec_retire_needs_reason` and the seven views stay untouched.
> - **CHECKs.** Two column CHECKs:
>   - `marker IS NULL OR (marker IN ('●','◐','○') AND (regulatory_stratum_only = 0 OR marker = '○'))`
>   - `retired_at IS NOT NULL OR (state IN ('stated','provisional')) = (marker IS NOT NULL)`
> - **Ordering.** It declares `-- AFTER_DATA: <latest data migration>`. SQLite checks an added CHECK against existing rows; 095's marker already orders it after every `specifications` write.
> - **View.** It redefines `v_best_practice` without `strength_band`, a second two-valued band that reads `anchored` over a ○ proxy cell and has no code reader.
> - **Engine, same PR.** `assess_cell.determine` computes the marker and `main` writes it. Each governing source carries its §5 band, and the cell takes their floor-mean. A value read off the regulatory stratum (floor claim or proxy threshold) is ○ unless a `confirms` edge from an anchoring finding reaches a governing extraction row; then that code takes the confirming study's band (R39; it fires on 0 live edges, all three being `to_label`).
> - **Model and tests.** `EvidenceStateRecord` gains `marker`. The four tests the fifth pass named supply a marker wherever they write or un-retire a live stated or provisional row (without it their refusal assertions pass vacuously), and `test_assess_cell_pilot` asserts the bands, the CHECK, and the owner's five-row floor-mean table.
> - **Regeneration.** Regenerate `tools/pipeline-completeness-dashboard.html` (blocking freshness check) and `tools/pipeline-walk.html`.
> - **Owner merge.** Correct the three prose callers of `strength_band` (`evidence-architecture.md` :119 keeping atom EVI-182's quoted phrase, :206; `evidence-methodology.md` :144) and the mission line (doctrine sha).
>
> Rehearsed: 14 files, +208/−56 (code +79/−24, tests +79/−25, migration +44); `--rebuild` identical; no gate worse than baseline. **Not built:** the band of a `figure_role='derived'` row from its inputs (0 rows); a T3-clinical confirming study (the engine does not treat T3 findings as direction, so the CHECK pins the cell at ○); `derivation_sha` does not cover `extraction_relations`, so a later `confirms` edge leaves a stale marker under an unchanged sha.

**render** (replace the sentence "The marker is the engine's output … Until then the view reads the state and flags the engine already writes."):

> The marker is the engine's output and has one home, `specifications.marker` (specification row). `v_best_practice` carries it through `SELECT *`, and the one view to be built reads it, so the band half of the register invariants holds by construction: the CHECK refuses a regulatory-stratum-only row above ○ and a live stated or provisional row without a marker. What the renderer still owns is the weak/code-derived flag text and the register map, plus rendering `provisional ●` (T3-clinical-only, or an H4-capped cell) distinctly from `stated ●`. All 8 live `specifications` rows are retired, so the view returns 0 rows until a determination is written.

## 7. Not verified

- Design 1's engine-side change (adding `scope` to the per-source record) was estimated, not run. Its `--all` was not run; only its three affected tests were.
- Design 2's remaining same-PR edits (stage-map entry, Pydantic mirror, dashboard regeneration, the forced `--tier` fix) were not made. Only the reds they cause were measured.
- Whether the owner accepts the readings in §4, items 2, 4, 5 and 8 [owner].
- `research_tooling_separation` against the real `origin/main` [UNVERIFIED]: in this clone `origin/main` is stale. Against the pinned base it passes.
