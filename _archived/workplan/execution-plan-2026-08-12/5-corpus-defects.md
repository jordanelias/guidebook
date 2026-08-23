# Wave 5 — Corpus defects

**Read `00-holistic-execution-plan.md` first.** **Precondition: L1 exists.**

**The wave's hard gate:** **W9.1 → W5.6 + W5.1 together.** W5.1 does not ship without W5.6, and
W5.6 does not ship without W9.1's exemption DR. Executing W5.6 as written without W9.1
manufactures a permanently-red blocking gate.

**Owner gates:** W5.2 (E-12's scope), W5.5 (retiring `weighting_profile` is a doctrine edit),
W5.4(a) (the 8 residual rule identifiers), W5.8 leg 2 (does `schemas/*.py` mirror SQLite or
YAML?).

---

## W5.1 — The false numeric values. **Nine rows across six items, not eight across five.**

### Objective
Correct every `jurisdictional_values.value_numeric` that does not correspond to a quantity
stated in its own `value_text`, by compensating migration, reconciling the shadow YAMLs in the
same PR.

### The headline re-derivation

**The count moved again.** Its history is 5 → 6 → 8 → **9**, and this decomposition found the
ninth by sweeping all 75 numeric rows rather than re-checking the eight it was handed.

**`jv 52` — E-03 / NO / TEK17 §12-18, `value_numeric = 1.0`, extracted from the "1" in
"Max Gradient: 1:12 indoor".** Its sibling rows jv 48, 49 and 55 encode the identical 1:12
gradient as **8.3** (percent convention under unit `ratio`). At 1.0 the row asserts a 1%
gradient, which its own text does not state.

**Why nobody found it before, and why this matters more than the row itself:** jv 52 evades
**both** detector blind spots at once.

- It has a **non-NULL unit**, so W0.3's new `numeric_without_unit` class will not catch it.
- Its in-item spread is 1.0–8.3 = **×8.3**, below the detector's ×10 conflation threshold at
  `scripts/audit/jurisdictional_divergence.py:141`, so it surfaces only as INFO-level
  "legitimate jurisdictional divergence" — indistinguishable from a real national difference.

**The standing lesson for W0.3: a false value with a unit and a sub-×10 spread is invisible to
every finding class the detector has, before and after unblinding.** Neither the current
detector nor the planned fix would find the next jv 52.

### The nine rows

| jv | item / juris | standard | bad value | mis-extracted from | correction |
|---|---|---|---|---|---|
| 40 | E-12 / ISO | ISO 21542:2021 | `81.0 mm` | "References **EN 81**-41" | **NULL** |
| 104 | B-10 / GB | BS 5839-1 / EN 54-23 | `54.0 Hz` | "Per **EN 54**-23" — siblings jv 103/105 hold the real ≤2 Hz seizure ceiling | **NULL** |
| 46 | G-04 / FR | Arrêté 2014 | `1300.0 m²` | "**1300**×1300mm" | **3.6** |
| 42 | G-04 / GB | BS 8300-2:2018 / Part M | `1500.0 m²` | "2200×**1500**mm" | **4.7** |
| 16 | E-07 / DE | DIN 51130 | `9.0` (unit NULL) | "**R9**–R13" — class ordinal | **NULL** |
| 17 | E-07 / AU | AS 4586:2013 | `3.0` (unit NULL) | "**P3**–P5" — class ordinal | **NULL** |
| 106 | E-15 / GB | Building Regs 2021 | `2021.0` (unit NULL) | the **year**; the row's real quantity is "Min Area: ≥12m²" | **12.0 + `unit='m²'`** |
| 107 | E-15 / US | IBC 2024 / A117.1 | `1.0` (unit NULL) | "Supplement **1** (2024)" — edition ordinal | **NULL** |
| **52** | **E-03 / NO** | **TEK17 §12-18** | **`1.0 ratio`** | **the "1" in "1:12"** | **8.3** |

**The class refinement that must survive into W0.3.** Of the 8 NULL-unit numeric rows, only
**four** are defects (jv 16, 17, 106, 107). The other four — jv 14 (DCOF 0.42), jv 15 (PTV 36),
jv 96 and jv 100 (occupancy thresholds of 50) — are **genuine dimensionless or count
quantities**. A blanket "NULL unit is a defect" rule corrupts them. After this migration the
NULL-unit-numeric set is exactly those four correct rows.

### Preconditions and ordering

1. **W9.1 → W5.6 + W5.1 in one PR.**
2. **W5.1 before W5.2 — newly found ordering trap.** The migration keys jv 40 on
   `item_code='E-12'`. If W5.2's re-key (E-12 → E-02) lands first, that UPDATE silently no-ops
   under its own guard and the false 81.0 survives. Either sequence W5.1 first, or W5.2's
   migration must carry the jv 40 correction forward.
3. W0.3 should precede so that the post-fix all-clear means something.

### Ordered steps

1. Ledger entry (`plan_item: W5.1`) enumerating all nine rows by natural key.
2. Emit the migration:
   `python3 scripts/emit_data_migration.py --session <id> --summary "W5.1: null/correct nine extractor-false value_numeric" --input changes.sql`
3. `changes.sql` — keyed on the natural key `(item_code, jurisdiction, standard_name)` **plus a
   current-value guard**, so re-application and reordering are both no-ops. Never key on
   `jv_id`/rowid: rowids shift on rebuild.

```sql
-- W5.1: nine extractor-false value_numeric corrections.
-- NULL where value_text states no quantity; the stated figure where it does.

UPDATE jurisdictional_values SET value_numeric = NULL          -- jv 40: '81' is EN 81-41's number
 WHERE item_code='E-12' AND jurisdiction='ISO' AND standard_name='ISO 21542:2021'
   AND value_numeric = 81.0;

UPDATE jurisdictional_values SET value_numeric = NULL          -- jv 104: '54' is EN 54-23's number
 WHERE item_code='B-10' AND jurisdiction='GB' AND standard_name='BS 5839-1 / EN 54-23'
   AND value_numeric = 54.0;

UPDATE jurisdictional_values SET value_numeric = 3.6           -- jv 46: text states ~3.6 m²
 WHERE item_code='G-04' AND jurisdiction='FR' AND standard_name='Arrêté 2014'
   AND value_numeric = 1300.0;

UPDATE jurisdictional_values SET value_numeric = 4.7           -- jv 42: text states ~4.7 m²
 WHERE item_code='G-04' AND jurisdiction='GB' AND standard_name='BS 8300-2:2018 / Part M'
   AND value_numeric = 1500.0;

UPDATE jurisdictional_values SET value_numeric = NULL          -- jv 16: R9 is a class ordinal
 WHERE item_code='E-07' AND jurisdiction='DE' AND standard_name='DIN 51130'
   AND value_numeric = 9.0;

UPDATE jurisdictional_values SET value_numeric = NULL          -- jv 17: P3 is a class ordinal
 WHERE item_code='E-07' AND jurisdiction='AU' AND standard_name='AS 4586:2013'
   AND value_numeric = 3.0;

UPDATE jurisdictional_values SET value_numeric = 12.0, unit = 'm²'   -- jv 106: real quantity ≥12 m²
 WHERE item_code='E-15' AND jurisdiction='GB' AND standard_name='Building Regs 2021'
   AND value_numeric = 2021.0 AND unit IS NULL;

UPDATE jurisdictional_values SET value_numeric = NULL          -- jv 107: edition ordinal
 WHERE item_code='E-15' AND jurisdiction='US' AND standard_name='IBC 2024 / A117.1'
   AND value_numeric = 1.0 AND unit IS NULL;

UPDATE jurisdictional_values SET value_numeric = 8.3           -- jv 52 (NEW): '1' from '1:12';
 WHERE item_code='E-03' AND jurisdiction='NO' AND standard_name='TEK17 §12-18'
   AND value_numeric = 1.0;                                    -- siblings encode 1:12 as 8.3
```

**House-style note:** NULL `value_numeric` with `unit` retained has precedent (jv 4, 22, 47,
68–70), so the NULL corrections leave `unit` untouched — except jv 106, which gains `m²`.

4. **Reconcile the shadow YAMLs — six files, not five.** The directory holds exactly 20 per-item
   files (A.1–A.20) plus `migration-report-appendix-a.md`, mirroring the 109 rows 1:1.

| File | Line | Edit |
|---|---|---|
| `a-18_e12.yaml` | :70 | `81.0` → `null` |
| `a-8_b10.yaml` | :22 | `54.0` → `null` |
| `a-19_g04.yaml` | :24 | `1500.0` → `4.7` |
| `a-19_g04.yaml` | :71 | `1300.0` → `3.6` |
| `a-13_e07.yaml` | :33 | `9.0` → `null` |
| `a-13_e07.yaml` | :44 | `3.0` → `null` |
| `a-9_e15.yaml` | :11–12 | `2021.0` → `12.0`; `unit: null` → `unit: m²` |
| `a-9_e15.yaml` | :22 | `1.0` → `null` |
| **`a-1_e03.yaml`** | **:55** | **`1.0` → `8.3`** — the ninth row's mirror |

### Caller sweep
- `scripts/migrate/phase_jv_appendix_a.py` regenerates these YAMLs from a **pre-fix source** —
  do not run it. Its retirement is W7.1.
- `site/specs/*.html` does not render these numerics (`spec_page.py` never SELECTs them — see
  W5.7), so blast radius is the DB plus the six YAMLs.

### Verification
1. Re-run the full dump: nine rows corrected; **running the migration body twice changes 0 rows
   the second time** (the guard proves idempotence).
2. `python3 scripts/audit/jurisdictional_divergence.py`: B-10's ×27 and E-12's ×17 WARNs clear;
   G-04's spread drops ×357 → ~1.5. **Record the EXAMINED count before and after** — per ledger
   interrogation I4, a check whose verdict improves while its subject count moves is the
   repository's named failure mode.
3. `python3 scripts/audit/migration_reproducibility.py` (widened per W5.6) passes with
   `jurisdictional_values` in scope.

### Falsifier
A tenth row in the same class — none found at HEAD after checking all 75 numeric rows. Or the
owner rules jv 52's `1.0` a deliberate numerator convention — refuted by siblings jv 48/49/55.

### Risks
- The corrections are **readings of `value_text`, not of BS 8300, DIN 51130 or Arrêté 2014**.
  Text-vs-standard verification is Phase-B work and is not done here.
- jv 106 gains a unit; no consumer in non-legacy `.py` assumes NULL-unit for E-15.

---

## W5.6 — Widen the reproducibility gate. **With W9.1 first.**

### Objective
Replace the six-table `COUNT(*)` comparison with dynamic enumeration of all non-exempt tables.

### The gate, measured
`scripts/audit/migration_reproducibility.py:55-63` compares `PRAGMA user_version` plus
`COUNT(*)` on six tables: `evidence_sources`, `citation_mining`, `source_slug_links`, `gaps`,
`connections`, `items`. Live row counts: **93 of 4,245 rows — 2.2%.** `jurisdictional_values`,
the one populated evidence-shaped table, is not among them. Widened coverage is **4,239 rows
across 64 non-exempt tables — 99.9%.**

### W9.1 is a harder gate than the plan states

`url_verification_runs` holds **5 rows** in the committed DB, is **created but never populated
by any migration** (`012_baseline` creates it; zero `INSERT INTO url_verification_runs` exists
across `scripts/migrations/`), and is **absent from `EXEMPT_TABLES`** at `:65` (which holds only
`evidence_source_authors` and `pipeline_runs`).

**Therefore the widened gate fails immediately on landing — 5 committed vs 0 rebuilt — not "the
next time the cron runs" as W9.1 says.** The cron is live: `.github/workflows/verify-urls.yml`,
bi-weekly, `permissions: contents: write`, `GUIDEBOOK_DB_PATH: data/guidebook.db`.

### Ordered steps
1. **W9.1's DR lands first.** Then add `url_verification_runs` to `EXEMPT_TABLES` at `:65`. The
   file's own docstring at `:22-27` already names `verify-urls.yml` as an authoritative
   outside-migrations writer and states that adding an exempt table requires a new DR.
2. **Widen `compare()`** at `:175-194`: enumerate `user_tables(committed) | user_tables(rebuilt)`
   (helper already exists at `:205-207`), minus `EXEMPT_TABLES`, `COUNT(*)` per table via the
   existing quoting helper at `:197-202`, plus `user_version`.
3. **Delete the skip branch** at `:184-186` — a table absent on either side becomes a MISMATCH,
   not a skip.
4. **Invert the selftest case** at `:451-459` ("missing tables are skipped, not fatal", asserting
   `r[3].startswith("skip")`) to assert absence is reported as divergence.
5. **`_usable_cache()`'s `needed` set at `:127-131` hardcodes the same six tables** — update or
   derive it, or the cache-validity probe stays six-table-shaped while the gate is not.
6. **Registry note rewrite:** `governance/check-registry.yaml:290-297`'s SCOPE paragraph.
7. **`CLAUDE.md:41-44`:** drop "as does anything in the other 55 tables". **Keep** the UPDATE
   caveat — counts still cannot see an `UPDATE`, which is exactly why W5.1's corrections need
   `migration_reproducibility_deep` eventually.

### Verification
Post-widening the audit prints one row per non-exempt table and passes only if W9.1 landed.
Deleting a table in a scratch rebuilt copy must yield MISMATCH.

### Falsifier
The widened gate stays green with `url_verification_runs` un-exempted. It cannot: 5 ≠ 0,
measured.

### Risk
Both `pipeline_runs` (6 rows) and `url_verification_runs` (5 rows) report against a now-empty
`evidence_sources`. Their counters describe a corpus of 410 verified URLs and 225 resolved DOIs
that no longer exists. **The exemption DR should say so** rather than implying the rows are
current.

---

## W5.4 — Attestation rule-identifier resolution

### Re-derived by running the real `check_3_rule_resolution` over all 76 attestations

| Measure | Value |
|---|---|
| Failures | **4 of 76** |
| Distinct unknown identifiers | **8** |
| Attestations citing `integrity-protocol` as a rule id | **0** |
| Attestations citing `supersession-audit` | **0** |

The four failing files: `decisions_DR-2026-06-11-remove-colonial-role.json`
(`forward-only-migrations`) · `decisions_DR-2026-08-04-verification-status-is-a-standing-not-a-history.json`
(`doctrine-token-on-synthesis-paths`) · `decisions_DR-2026-08-06-clean-room-evidence-reset.json`
(`decision-protocol`, `evidence-architecture`, `migration-discipline`, `retire-not-delete`,
`tier-system`) · `sessions_session_2026-05-19-deployment-state-reconciliation.json`
(`commit-msg-format`).

**The register's "4 committed attestations cite `integrity-protocol`" was a whole-file string
grep hitting artifact paths and `bias_direction` prose. The real count is zero** — a textbook
instance of W6.6 (a regex classification is a candidate list, never a finding).

### Ordered steps
1. **(a) — owner adjudication.** The schema question is already answered:
   `references/skill-registry.md:21-35` states CHECK 3 resolves against the registry **or**
   `EXTRA_RULE_IDS` (`adherence_log_audit.py:84-107`), *"the ratified extension point"* per
   `DR-2026-07-13`. The live decision is only whether the 8 residual names are admitted there.
   **Recommend admit:** 6 of 8 name real governance objects; `forward-only-migrations` and
   `migration-discipline` name real rules under non-canonical spellings — admit or normalise.
2. **(b)** Register `integrity-protocol` and `supersession-audit` in `skill-registry.md` **on
   completeness grounds only** — verified to clear **zero** failures.
3. **(c)** Add `--corpus` to `adherence_log_audit.py`. Today `audit()` at `:551-553` scopes every
   check to `_changed_files(base="HEAD~1", head="HEAD")`, so **corpus validity is established by
   nothing** (W6.4). `--corpus` substitutes the full `ATTESTATIONS_DIR.glob("*.json")` set.
   Register as `attestation_corpus`, advisory, `governance` battery, printing `EXAMINED: 76` so
   a pass is never subject-free.

### Verification
`python3 scripts/audit/adherence_log_audit.py --corpus --check rules` prints `attestations: 76`
and, pre-adjudication, exactly the 4 failures above.

---

## W5.7 — Renderer omissions

**All claims re-verified at code level; line drift ≤1.**

| Location | Defect |
|---|---|
| `spec_page.py:73-79` | The cells SELECT omits `value_min`, `value_max`, `value_unit` **and** `gap_register_id` |
| `spec_page.py:196-198` | A `pending` cell renders as the bare word — no `[BEST-PRACTICE-PENDING]`, no gap link |
| `population_page.py:75-80` | Same SELECT, same four omissions |
| both | Determination tables iterate cell rows only, so a population linked with no cell is absent from the table |
| `pilot_renderings.py:213-237` | **A working implementation exists** — its SELECT includes `gap_register_id` and its pending text reads `[BEST-PRACTICE-PENDING] — evidence gap logged (→ gap register)`. Its only importer is `register_integrity_check.py:34`. **Wired to nothing in site generation.** |

**The refinement that makes this latent rather than live:** the population is not erased from
the *page* — a separate "Applicable populations" table renders it from `item_population_links`
(`spec_page.py:51`, `population_page.py:55`), and the all-empty case is honestly bannered. **So
the breach fires on the first partial determination**, in exactly the thinnest-evidence
populations. `governance/mission-and-epistemics.md:120`: *"Silence on evidence-thin populations
is not the default."*

### Ordered steps
1. Add the four columns to both SELECTs and their dict-mappings.
2. Render `pending` as `[BEST-PRACTICE-PENDING]` with an anchor to `gap_register_id`; honest
   banner when the gap link is NULL.
3. Rebuild the determination table from `item_population_links LEFT JOIN specifications`,
   emitting an explicit "no determination recorded" row.
4. Port `pilot_renderings.py`'s marker text — **do not** duplicate its audience-register
   machinery, which is W3.6/D-A scope.
5. **Regenerate in the same PR as W5.8 leg 4** so the 12 stale pages are rebuilt once, post-fix.

### Verification
Fixture on a scratch DB copy: one `pending` cell with a gap id, one `stated` cell with values,
one linked population with no cell. Assert marker, link, and explicit-absence row. *(Appendix D
concedes this behavioural demonstration was never run — it becomes this item's acceptance test.)*

### Risk
**Rendering values before D-A rules on the write path re-creates the hard-coding class Wave H
exists to purge.** Render only what a cell actually holds.

---

## W5.8 — The nine standing advisory failures, each re-run at HEAD

**Do not clear by silencing.**

| # | Check | Verdict at HEAD | Resolution |
|---|---|---|---|
| 1 | `validate_reasoning` | exit 1 — **15 ERROR findings** on `references/bpc-reasoning/room-acoustic-performance.md` (4 header fields, 1 bad status `PILOT`, 10 missing sections) | Content work. The registry note at `:884-892` says "1 doc missing 'F. Provenance trail'" — badly understated. Plan's "~14" → **15** |
| 2 | `validate_pydantic_schemas` | exit 1 — **246 drift findings** (registry note's "236" at `:618` is stale) | **Owner decision:** does `schemas/*.py` mirror SQLite or the YAML layer? |
| 3 | `retired_vocabulary` | exit 1 — `RESULTS: 69 occurrence(s)` | Text fixes / `exempt_paths` / `[RETIRED-VOCAB-OK]` |
| 4 | `site_pages_fresh` | exit 1 — **12 stale pages** incl. `c-06, e-06, e-08, e-12, f-07, g-03` | Regenerate — **sequenced with W5.7** |
| 5 | `research_dod` | exit 1 — `R1: 0 searches targeted co1/co2 and 0 co1/co2 sources admitted`, **examined 0** | R-15 warrant, not content. Note R13 simultaneously reports "PASS on all 0 admissions" — a vacuous green beside a vacuity-shaped red, in one output |
| 6 | `test_verification_pipeline` | exit 1 — `RESULTS: 15/18` | The three failures are exactly the G-legs: G01 language ≥50 sources, G02 ORCID ≥30 authors, G03 COMPLETE ≥100 — production floors asserted against a 0-row table. R-15 warrant |
| 7 | `test_directness_2_2` | **standalone exit 0 / dispatched exit 1** | `run_checks.py:389-390` sets `GUIDEBOOK_DB_PATH`, so the live-smoke leg runs against the empty canonical table instead of skipping. **The registry note's "(it is, in CI)" at `:1002-1004` is wrong.** Make the leg SKIP loudly when its subject table is empty |
| 8 | `test_graph_audit` | exit 1 — `TypeError: 'NoneType' object is not subscriptable` at `graph_audit.py:277` | **Selftest-path-only** — the same run prints `[PASS] graph_audit clean run exits 0`. Guard leg 3 with `[SKIP] NOT-TESTABLE`, never a fabricated pass |
| 9 | `register_integrity_check` | exit 1 — five mutations FIRED, then `SILENT — MUTATION MISSED: COMPLETENESS: a whole cell section deleted` | `specifications` = 0 makes the set-diff vacuous, and **`:182`'s `if db_rows:` disables the doc→DB direction entirely on an empty table**. Make the empty-DB case an explicit NOT-TESTABLE in both selftest and live check |

### Plus the two adjacent items

**`parts/v10` staleness — 15 files, all stale.** `part00.md`–`part13.md` + `manifest.md`, last
touched 2026-07-21 while `data/guidebook.db` last changed 2026-08-06. `scripts/generate_parts.py`
has **no `--check` flag** (zero grep hits) — this is **the one place in the whole plan where a
new check is the correct resolution**: a `parts_fresh` check on the `site_pages_fresh` pattern.
Wave-H relevance: E-08's hard-coded name ships at `parts/v10/part04.md:92`.

**`room_page.py` — the plan's "four, not six" is only half right.** The generator queries **six**
table names absent from the live DB: `room` (`:26`, `:29`), `room_item` (`:35`),
`room_item_population` (`:44`, `:84`), `specification` (`:51`), `room_dar_provision` (`:66`),
`room_conflict` (`:75`). **Two are singular/plural misnames** with live counterparts —
`room`→`rooms` (17 rows), `room_item`→`room_items` — and **four have no counterpart at all**.
State it as *"six queried names are absent; two are misnames, four have no table."* Resolution:
port to the live schema or quarantine the generator.

---

## W5.2 — E-12's platform-lift values

**Owner ruling required. Hold pending Wave H.**

**Three facts no prior document assembled, all confirmed:**
1. E-12 (`Entrance Landing and Manoeuvring Space for Power Wheelchair Users`) carries jv 35–40 —
   all platform-lift dimensions (`Min. Platform (W×D)`, door width, 0.15 m/s speed), all
   `source_section='A.18'`.
2. The source YAML `data/jurisdictional_values/a-18_e12.yaml:2` is titled **`Platform Lift
   Dimensions`**.
3. **`E-02 Platform Lift` already exists, active, with zero `jurisdictional_values` rows** — and
   with 2 `item_population_links` and 1 `item_axis_links`, so the re-key creates no orphan.

**Migration, post-ruling and post-W5.1:**
```sql
UPDATE jurisdictional_values SET item_code='E-02'
 WHERE item_code='E-12' AND source_section='A.18';
```
FK-safe — all 14 inbound FKs target `item_code`, and E-02 exists.

**The trap the plan names and this decomposition confirms:** filing these values under
`E-02 Platform Lift (Where Full Passenger Lift Not Achievable)` files them under a name that is
**itself a specification**. Wave H's H2 must strip the condition clause first.

---

## W5.3 — CORRIDOR-W vs E-08. **Dissolved as stated by Wave H.**

`references/conflict-matrices/CORRIDOR-W.md` (24 lines) asserts **≥2440 mm** at `:9`, `:16` and
`:18`, with **zero citation anywhere in the file** — no REF-id, no DOI, no named source.
`[UNVERIFIED-QUANT]`-shaped. E-08's *name* asserts ≥1200 mm against recorded values US 915 / AU
1000 / GB 1200 / ISO 1200 / DE 1500 / NO 1500 — two below, two above.

**So this is not two rival claims. It is two unevidenced assertions**, and Wave H removes one of
them outright.

**A nuance the plan omits:** `references/methodology/value-genealogy-worked-example-corridor-width.md:15`
traces the 2440 figure's genealogy (REF-00338 Bauman, REF-00737 Steinfeld). **The number has a
paper trail elsewhere; the file cites none of it.** The banner should point at the genealogy
document rather than implying the figure was invented.

**Second-order ruling stands:** CORRIDOR-W was reclassified NOT-A-CONFLICT solely on the
DEAF-vs-NDV/AUT sensory-load axis (`:9-16`), then declared retired as a **domain** (`:20`,
`:23`). **Retirement verdicts should be per-axis**, and a domain file's banner should name the
axis it adjudicated. Depends on W4.5's `conflict_kind`.

---

## W5.5 — `weighting_profile` and the 11 unread views

**Owner ruling. Retiring is a doctrine edit, not dead-code removal.**

`weighting_profile` holds 5 rows (designer, disabled_person ×2, policymaker, ot), each with a
JSON `tier_weights` foreground list. **Touched by no code — and the finding is stronger than
claimed:** a repo-wide `grep -rn weighting_profile --include=*.py` including legacy paths
returns **zero** hits. References are governance prose only, and
`governance/evidence-architecture.md` **I3 at `:142`** binds renders *"in any register, under any
weighting profile"* — so retiring the table amends doctrine.

**The 11 views: reader-count 0 in non-legacy `.py` for every one.** `v_coverage_priority` holds
**7,210 rows**; the other ten hold 0. Classify three ways before putting it to the owner:

- **contract-cited** — `v_value_independence` (`governance/pipeline-contract.yaml:100`, the H1
  mechanism);
- **context-map-declared** — `v_code_floor_only`, `v_coverage_priority`, `v_pending`,
  `v_source_admission`, and others at `governance/context-map.yaml:185-201`;
- **cited nowhere.**

**Wire-or-retire ruling, not a cut.** Flag explicitly to the owner that retiring
`v_coverage_priority` discards the only populated coverage surface in the database.

---

## Re-derivation notes

| Plan claim | Status | Evidence |
|---|---|---|
| W5.1 is 8 rows across 5 items | **REVISED — 9 across 6** | jv 52 (E-03/NO) found by sweeping all 75 numeric rows |
| The eight cited rows, values, units, source texts | **CONFIRMED verbatim** | full-row dump at HEAD |
| Five shadow YAMLs | **REVISED — six** | `a-1_e03.yaml:55` added |
| The 8 NULL-unit rows are one defect class | **REFUTED** | 4 are genuine quantities; 4 are defects |
| W9.1: gate goes red "next time the cron runs" | **REVISED — red immediately** | 5 committed rows vs 0 rebuilt |
| `migration_reproducibility` covers 93 of 4,245 rows (2.2%) | **CONFIRMED** | live measurement |
| W5.4: 4 of 76, 8 identifiers, `integrity-protocol` cited by zero | **CONFIRMED exactly** | real check logic run corpus-wide |
| W5.7's omissions and the wired-to-nothing implementation | **CONFIRMED** | `spec_page.py:73-79`, `:196-198`; `pilot_renderings.py:213-237` |
| `validate_reasoning` ~14 findings | **REVISED — 15** | run at HEAD |
| `validate_pydantic_schemas` 246 findings | **CONFIRMED** | registry note's 236 is stale |
| `retired_vocabulary` 69 · `site_pages_fresh` 12 · `test_verification_pipeline` 15/18 | **CONFIRMED** | each run at HEAD |
| `test_directness_2_2` green standalone, red dispatched | **CONFIRMED** | `run_checks.py:389-390` |
| `room_page.py` queries four non-existent tables | **REVISED** | six names absent; two misnames, four with no table |
| `weighting_profile` touched by no code | **CONFIRMED and strengthened** | zero hits repo-wide including legacy |
| CORRIDOR-W's 2440 carries no citation | **CONFIRMED** | and its genealogy lives in a separate methodology doc |
