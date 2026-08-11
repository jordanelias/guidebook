# 2026-08-12 — Resolution plan for everything the trials, the sweep and the audits found

**Status:** PROPOSED. Nothing below is executed. Three items are marked DONE because the sessions
that found them fixed them while fixing their own defects; everything else is a proposal with a
gate.
**Provenance.** This is a **rewrite in place** of the plan authored in PR #93 (merged `bc81070`).
Its wave structure, its sequencing rule and most of its content are retained and credited. It is
rewritten rather than superseded by a new file because a second plan is exactly the proliferation
the consolidation work is trying to end. **§0.3 lists every change from the original, so the
rewrite is auditable rather than silent.**
**Sources.** `2026-08-12-commit-91-adversarial-review.md` · `2026-08-12-work-log-audit-four-directions.md`
· `2026-08-12-pipeline-phase-state-map.md` · `2026-08-11-remediation-and-pipeline-anatomy.md` Part 1
· and, added by this rewrite, `2026-08-11-consolidated-review-and-plan.md`,
`2026-08-11-per-stage-table-anatomy.md`, `2026-08-11-fold-or-cut-ledger.md`,
`2026-08-11-reconciled-findings-register.md`.
**Subject:** `d09f923`. **Doctrine SHA:** `0f2f525`.

---

## 0. The organising claim

The predecessor register asked *"does the structure work before content?"* and answered "partly".
Two trials, an audit and a repository-wide sweep sharpen that into **four** statements, and the
plan follows from their order:

1. **The write path is not safe to use.** A foreign-key violation commits; a prose word disables
   enforcement; one failed migration voids every migration behind it. Until that is fixed,
   everything else is built on a substrate that silently accepts bad rows and silently discards
   good ones.
2. **The pipeline determines a state, never a number.** Twelve stages carry evidence to a
   judgement about *how well evidenced* a cell is, and then the value is written by hand. That may
   be correct — but it is undeclared, and every Wave 4 operation is downstream of ruling on it.
3. **Green does not mean examined.** Five of the trial session's seven self-caught errors were
   caught by executing something; none by proofreading. **And the sharpest instance was found
   after the original plan was written:** the repository contains a working detector for a
   data-corruption class, it is quarantined, and **CI runs the *test* of that detector while never
   running the detector** (W5.1).
4. **The hole is not diffuse — it is stage 7.** Counting live writers per table: 13 tables are
   *unwritable outputs* — the pipeline reads them and no code can fill them — and **nine of them
   are in stage 7, value extraction**, with stages 8 and 9 inheriting the gap. Stages 1–5 have
   writers and work. **The pipeline can gather evidence and cannot turn it into a value.**

**Sequencing rule, unchanged from the original:** fix the substrate, then rule on the boundary,
then build. Do not reorder — Wave 3 writes rows, and rows are what make Wave 1 expensive.

**One rule added by the rewrite:** *before building a detector, check whether one exists.* W5.1
and the shared-library finding are the same lesson twice.

### 0.3 Every change from the PR #93 original

| # | Change | Why |
|---|---|---|
| 1 | **New Wave 0** (two items, minutes each) | W5.1's detector already exists and is unwired. Nothing else in the plan is that cheap |
| 2 | **W5.1 expanded 1 → 5 rows, and its sweep executed** | The original called the failure "systematic, not a one-off" and did not run the sweep. Run: 5 bad rows across 3 items, two of which no document had found |
| 3 | **W1.4's fix changed** from "zero-pad to three digits" to "import `db.py`'s function" | `db.py:149` already zero-pads and satisfies the schema. The bug *is* a re-implementation |
| 4 | **W3.2 contested and replaced** | An FK on `target_population` passes trivially on an empty table but 22 of 30 distinct pre-reset values are prose, and R13 needs that richness |
| 5 | **W5.4 widened 2 → 9 identifiers** | The whole-corpus check the original said had never run: 5 of 76 attestations fail, and **only one of the nine unknown ids is a skill** |
| 6 | **Wave 3 given a target order** | Per-stage writer counts say which three unwritable outputs unblock stages 8 and 9 |
| 7 | **New Wave 7 — consolidation** | Absent from the original: folds, cuts, the one-shot layer, the frozen corpus, the shared library |
| 8 | **Net line/file accounting added** | The owner's standing constraint; it changes which items are worth doing |
| 9 | D-B recorded as ratified-with-zero-presence | Unchanged in substance; restated as W3.1 |

---

## Wave 0 — Before anything else. Two items, minutes each.

| # | Action | Evidence | Falsified if |
|---|---|---|---|
| **W0.1** | **Wire `scripts/audit/jurisdictional_divergence.py` into the registry at `informational`.** Not `blocking`, not `advisory` — `informational` is the level the registry already has for a check whose exit code carries no verdict, which is the exact and correct reason it was quarantined on 2026-08-01 | Run today it prints `[candidate_conflation_or_error] 3 (WARN)` naming B-10, E-12 and G-04. `test_jurisdictional_divergence` is meanwhile **registered, active and passing** in the `tests` battery | Its output appears in a CI run and names no defect |
| **W0.2** | **File the three rows it names as W5.1 defects** | see W5.1 | — |

**Why this is Wave 0 and not part of Wave 5.** Every other item requires writing code or taking a
decision. This one requires a registry entry for a script that already works and already knows the
answer. It is also the plan's own lesson in miniature: **the capability existed, the wiring did
not, and the quarantine entry — which is honest and well-reasoned — recorded "not a gate" in a way
that was read as "not run."**

---

## Wave 1 — The write path. No decision required, four files.

Nothing else should ship first. Each is small, each is falsifiable, none needs an owner.

| # | Issue | Fix | Evidence | Falsified if |
|---|---|---|---|---|
| **W1.1** | FK check runs **after** `commit()`; the `except`'s `rollback()` rolls back nothing, so a violating migration is committed *and* ledgered | Move `foreign_key_check` above the `commit()`; commit only on a clean check | `migrate_db.py:161-183`; log Incident A-1 — `search_admissions` 0→1 and `data_migrations` 318→319 on a migration that exited 1 | A violating migration, applied, leaves no row and no ledger entry |
| **W1.2** | `is_bootstrap = "BOOTSTRAP" in body[:500]` — the `--summary` text a session types decides whether FKs are enforced | Delete the substring test. If a bulk load genuinely needs it, gate on an explicit `--allow-fk-violations` flag a human types and the ledger records | `migrate_db.py:174`; log Probe A-3 — identical violation, reworded summary, exit 0 | Re-running Probe A-3's payload with any summary wording is rejected |
| **W1.3** | A failed migration stays pending, is retried first forever, and voids every migration behind it. The documented fix-forward remedy is queued behind the failure it compensates for | Add a quarantine: `--skip <id>` writing an abandonment row, or `migrations/failed/`. Separately, print `N migration(s) not attempted` whenever the loop aborts | `migrate_db.py:150-187`; log Incidents A-4 and A-5 — eight discarded migrations, an error naming a file from two stages earlier | A failure in migration *k* leaves *k+1…n* attempted or explicitly reported as skipped |
| **W1.4** | `next_gap_id` returns `GAP-1` on the post-reset empty table; `schemas/evidence_state.py:167` requires `^GAP-\d{3,4}$`, so the determination writer aborts on the first cell needing a gap | **CHANGED.** Not "zero-pad to three digits" — **replace the local function with `from db import next_gap_id`.** `db.py:149` already returns `GAP-001` on empty and formats `:03d` | `assess_cell.py:426-429` vs `scripts/db.py:149-159`; log Stage 9b.4 traceback | `assess_cell.py` completes a run against an empty `gaps` table |

**W1.4 is the plan's smallest item and its most instructive.** A Wave-1 bug that breaks the only
determination writer is a **re-implementation of a function the repository already had correct**.
See Wave 7.4.

**Also in this wave, carried by the predecessor register and independently confirmed:**

- Guard the three unguarded direct writers. One is
  `scripts/migrations/session_2026_05_11g_replay.py` — **the only `.py` among 347 files in the
  canonical migrations directory**, which replays pre-reset corpus state into `data/guidebook.db`.
  It is the single item in this plan that can silently reverse DR-2026-08-06. Retiring the
  one-shot layer (Wave 7.3) closes all three at once.
- Wire the registry's `deps:` field — declared since the registry was built, read by nothing.
- Repair the malformed `governance` battery YAML (`check-registry.yaml:174`): unquoted commas in a
  flow mapping produce two junk keys and a truncated description. **Reported in three documents,
  still unfixed, one line.**
- Fix `graph_audit.py:277` — **the crash is in the `selftest` path only**; the plain audit exits 0.

**Wave 1 exit condition:** re-run the corridor walk's stage 4a ordering probe and stage 9. The
probe must be rejected *with nothing written*, and `assess_cell.py` must complete.

---

## Wave 2 — Two rulings that gate everything after them

Both are owner decisions. Both are cheap to *decide* and expensive to defer, because Wave 3 writes
rows and rows close the free window.

### D-A · Is value determination a machine stage or a human one? *(D-METH)*

`assess_cell.py` writes `value_min`, `value_max` and `value_unit` as `None`, unconditionally, and
is the only writer of `evidence_cell_state`. There is no code path from N extracted values to one
determined value.

- **If machine:** stage 9 needs a value-reconciliation step, and Wave 4's paradigm and device
  dimensions become its inputs.
- **If human** — which the Opus floor may deliberately intend — say so in
  `governance/pipeline-contract.yaml` as a stage with an input contract, an acceptance condition
  and an attestation. Today it is three `None`s in a column list, indistinguishable from an
  oversight.

**Recommendation: human, declared.** The judgement is doctrinal, not arithmetic. But it must stop
being implicit, because every Wave 4 operation assumes an answer.

**Sharpened by the per-stage view:** stage 7 has **nine unwritable outputs**, so even a machine
ruling has nothing to reconcile until Wave 3 lands. D-A can be decided now and implemented after.

### D-B · The derived-value marker — **ratified, with zero repository presence**

The owner established on 2026-08-12 that derived values carry a **triangle with the same fill
scheme** — ▲ / ◭ / △ parallel to ● / ◐ / ○, shape carrying derivation, fill carrying evidence
strength. This is no longer a ruling to make.

It is a **ratified marker that exists nowhere**: no glyph in `governance/`, `schemas/`, `scripts/`,
`decisions/` or `references/`; no column; no validator; no renderer. What remains for the owner is
narrow — **whether the fill of a derived marker takes the strength of its input evidence or is
capped one band below it.** Everything else is implementation and moves to W3.1.

---

## Wave 3 — Free today, expensive after the first content batch

Every table named is empty. Each is a migration that costs nothing now and requires a backfill
later.

**Target order, added by the rewrite.** Per-stage writer counts identify which three unwritable
outputs unblock the most: **`source_value_extractions` → `evidence_population_match` →
`reasoning_doc_citations`.** Stages 8 and 9 each read all three, and nothing else releases them.

| # | Fix | Why now |
|---|---|---|
| **W3.1** | **Implement the derived-value triangle.** Glyph and fill semantics into `tier-system.md` §5 beside ●/◐/○; a `synthesis_method` column on `evidence_cell_state` using the vocabulary `governance/armature_v4_resolutions.md:23` already specifies (`direct`/`inferred`/`consensus`) plus its `inference_basis` companion; a renderer that emits it | Ratified doctrine, zero implementation. 0 rows |
| **W3.2** | **REPLACED — split `evidence_population_match.target_population`** into `target_population_code` (FK to `populations`, nullable) and `target_population_note` (free text); hand-migrate the 64 archived rows | **The original proposed a bare FK on the strength of "0 rows".** But 22 of its 30 distinct pre-reset values are prose — *"Autistic students in school built environments"*, *"DEAF/HoH adults relying on lipreading"* — and contract rule **R13** grades population-of-study against population-served, which needs that richness. A bare FK passes trivially today and breaks the first writer following the only precedent that exists. The split satisfies the original's aim (a real key, no `WHEELCHAIR-USERS-GENERALLY` umbrellas) without discarding R13 |
| **W3.3** | **Doctrine binding on `evidence_cell_state`** (a `doctrine_sha` column), or widen `attestation.schema.json`'s `artifact` pattern so an attestation can name a row | Leg 4 of DR-2026-08-06's four-leg promise. No doctrine column exists anywhere in the DB |
| **W3.4** | **`CHECK (evidence_type='co1' → tier=1)`** | Doctrine's most distinctive commitment is defended by nothing: no CHECK, no test, no registry entry, and `validate_source_co1_fields()` scans `data/sources/*.yaml`, which does not exist |
| **W3.5** | **`assess_cell.py` must write `cell_source_links`**, not only `governing_refs` | The trial's first real determination carried 7 governing refs and 0 junction rows, so the page stated it had **no governing sources** — false. The honesty mechanism is what misreports |
| **W3.6** | **Render the value, the marker band, and the gap link** (R1–R3) | The determination table has no value column; no ●/◐/○/▲ renders anywhere; `GAP-901` and `[BEST-PRACTICE-PENDING]` appear on no page |
| **W3.7** | **Populate `access_needs.typical_stakes`** — 17 rows, three ratified values | 16 of 17 are NULL, including `A-SIZE` and `A-REACH`, the two that reach corridor width |
| **W3.8** | **NEW — give the six remaining stage-7 outputs a writer**, or record in `pipeline-contract.yaml` that they are hand-authored: `spec_value_probes`, `item_bpc_links`, `cell_source_links`, `extraction_population_links`, `case_studies`, `economics_entries` | **Contract rule R12 instructs sessions to write `economics_entries` and no tool can.** A rule that names an unreachable target is worse than no rule |

**W3.6 depends on W3.1** (the marker set must exist before a renderer can emit it) and on **D-A**
(if the value is human-written, the renderer reads a different field).

---

## Wave 4 — The adjudication apparatus (Part 6's four operations)

Gated on **D-A**. This is the machinery the guidebook's actual product needs, and none of it
exists. Unchanged from the original except where noted.

| # | Operation | Fix |
|---|---|---|
| **W4.1** | Adjudicate one measurement paradigm over another | A **fourth directness dimension**. Add a claim-side field (`claim_manoeuvre`/`claim_construct`) — the schema records `measurement_paradigm` on the *source* and nothing records what the *claim* is about — and a `construct_directness()` beside the existing three in `schemas/directness.py`, with its doctrine table transcribed into `matrix_consistency.py` so code and doctrine cannot drift. Lift `root_type` into the conditioning layer at the same time |
| **W4.2** | Stratify a determination by device class | Either a third key column on `evidence_cell_state` or an explicit ruling that equipment stratification is a Population-Mode sub-key. **A doctrine gap, not a schema one:** the Design Mode ladder is universal/population/person, and device class sits between the last two |
| **W4.3** | Derive one item's value from another's | `evidence_cell_state.derived_from_cell_id` + `derivation_rule`, with `derivation_sha` extended to hash upstream cell ids so an upstream change reddens the downstream cell. Today nothing represents a cross-item dependency and `connection_targets.target` is un-keyed text |
| **W4.4** | Attach the normative premise that licenses a derivation | `access_needs.design_obligation` is the right column shape and reaches only as far as an *item*, via `access_need_axis_map → axes → item_axis_links`. Extend it to cells. Curate any new access-need code **from** `AX-WHM`, never as a coined umbrella |
| **W4.5** | Adjudicate when the above conflict | `conflicts` is keyed `(item_code, pop_a, pop_b)` and the question generates three shapes it cannot hold: paradigm×paradigm, equipment×equipment, item×item. Add `conflict_kind` with an FK-keyed target pair per kind |

---

## Wave 5 — Corpus defects, independent of everything above

Wrong data in the canonical database today. These wait on no ruling.

| # | Defect | Action |
|---|---|---|
| **W5.1** | **EXPANDED 1 → 5 rows.** One extractor failure — *it takes a number from anywhere in the value text and stamps the column's unit on it*: E-12/ISO `81.0 mm` ← "EN 81-41"; **B-10/GB `54.0 Hz` ← "EN 54-23"**, against sibling rows recording the ≤2 Hz photosensitive-epilepsy ceiling; **G-04/FR `1300.0 m²`** ← "1300×1300mm"; **G-04/GB `1500.0 m²`** ← "2200×1500mm"; plus E-07 class ordinals (`R9–R13`→9.0, `P3–P5`→3.0) stored as quantities with NULL unit | Correct all five by migration, then re-run W0.1 and confirm the WARN clears. **The sweep the original called for is done** — by the quarantined detector, in seconds |
| **W5.2** | E-12's six values are all **platform-lift** specifications (ADA §410/ASME A18.1, BS 6440, EN 81-41, AS 1735.12) under an item named *Entrance Landing and Manoeuvring Space for Power Wheelchair Users* | Owner ruling: does E-12 cover platform lifts? If not, the values belong elsewhere and E-12 has none |
| **W5.3** | `references/conflict-matrices/CORRIDOR-W.md` asserts **≥2440 mm** for DEAF signing pairs as Universal Mode; E-08's title asserts **≥1200 mm**. Four months, neither aware of the other. The matrix was also *retired* as a conflict domain on an unrelated axis, so no open domain exists to file against | Reconcile the two values; rule on whether retiring a conflict domain on one axis closes it for all. Depends on **W4.5** for the row shape |
| **W5.4** | **WIDENED 2 → 9 identifiers.** The whole-corpus check the original said had never run, run: **5 of 76 attestations fail CHECK 3**, citing 9 unresolvable ids — and **only `integrity-protocol` is a skill.** The other eight are *governance rule* names (`retire-not-delete`, `commit-msg-format`, `forward-only-migrations`, `doctrine-token-on-synthesis-paths`, `migration-discipline`, `decision-protocol`, `evidence-architecture`, `tier-system`) that `skill-registry.md` has no place for | **"Register both ids" fixes one ninth of this.** First decide whether `rules_in_scope` may cite governance rules at all — a schema question, since `attestation.schema.json` constrains the field. Then register the 2 missing skills, correct the rest forward-only, and add the whole-corpus check (the original's own remedy, and the right one) |
| **W5.5** | **NEW — `weighting_profile`: 5 rows, named by three pipeline stages, touched by no code.** Either the tier-weighting-by-audience model is live and unimplemented, or it is dead and should be retired | Owner ruling. Surfaced by the one true residual of the phase-multiplicity test |

---

## Wave 6 — Method, so the next session does not repeat this one

| # | Issue | Fix | Status |
|---|---|---|---|
| **W6.1** | The trial has a 105-action verbatim log; the review that pronounces CONFIRMED and OVERSTATED on another session's work has none | Route review-lens work through the harness. `run()` logs argv, cwd, exit code, stdout, stderr and per-table deltas at no cost beyond invoking it | `scripts/tests/walk_harness.py` **DONE** |
| **W6.2** | The review cited no log identifier; claims joined to evidence by prose | Log ids on every Break and R-row | **DONE** |
| **W6.3** | A syntax check passed for a test. `ast.parse()` on a module is `EXAMINED: 0` wearing a green tick | Never let a syntax check stand in for an execution | **DONE** for the harness; the general lesson belongs in `references/project-standards.md` |
| **W6.4** | `attestation_evidence` is advisory *and* diff-scoped, so an invalid rule id merged in PR #92 | Whole-corpus validity is established by no registered check | folds into **W5.4** |
| **W6.5** | Clean-room testing: E-08 was chosen for realism, and realism is what made it contaminating | Next trial uses a synthetic item outside the live code space, in units that do not exist | pending |
| **W6.6** | **NEW — a regex classification is a candidate list, never a finding.** Four proxy measurements inflated results across two sessions: 14 unknown rule ids (really 9), 77 "avoidable" f-string SQL interpolations (really ~0, and security-shaped), a table-type classifier that put 56 of 66 tables in one bucket, and a source-document that was nearly dropped because it used prose headings instead of IDs | State it in `references/project-standards.md`. Every count in a finding must come from executing the real check, not from a pattern that approximates it | **proposed** |
| **W6.7** | **NEW — before building a detector, check whether one exists.** W5.1's sweep was called for and never run while the tool that performs it sat quarantined; `db.py` is 1,889 lines of library that 80 scripts each re-implemented | Add to the same rule ledger | **proposed** |

---

## Wave 7 — Consolidation *(new in this rewrite)*

Absent from the original, which planned repairs but not volume. Every item here was measured;
none is speculative. **Two folds proposed during the sweep were retracted** — folding four
population-link tables into one polymorphic table would have traded three enforced foreign keys
for one, and folding `case_study_outcomes` into its parent would have destroyed a per-row tier
grade. The surviving test: **a fold must not destroy a key, and identical column shape is not
identical meaning.**

| # | Action | Net | Gate |
|---|---|---|---|
| **W7.1** | **Retire the one-shot importer layer** to `_archived/` — `scripts/convert/` (13), `scripts/db/` (3), `init_database.py`, `phase_jv_appendix_a.py`, the replay script | **−19 files, −6,074 lines.** Also closes all three unguarded writers in Wave 1 | none — `_archived/`, reversible |
| **W7.2** | **Merge the ten single-invariant audit scripts** behind `scripts/audit/invariants.py --check <id>`. The registry already dispatches by argument in 27 of 65 entries, so each stays individually registered, gated and quarantinable | −9 files, ~−200 lines | none. **Drop this first if the ~1,000-line result feels like `db.py` again** |
| **W7.3** | **Five FK-safe folds:** `bpc_metadata`→`slugs` (both PK `slug`, strictly 1:1) · `citation_mining`→`source_slug_links` (same grain, two key spellings) · `access_duration`+`access_stakes`+`life_stage_modifiers`→one vocabulary table (the first two are column-for-column identical) · `case_study_outcomes`+`case_study_strategies`→one child table (both FK only to `case_studies`) · `search_coverage`+`search_languages`→one axis column | **−8 tables** | DDL only, all empty |
| **W7.4** | **Resolve `scripts/db.py`.** 1,889 lines, 43 functions, **zero importers and zero subprocess callers** — while CLAUDE.md §4 describes it to every session as "the read/query workhorse". **Adopt** (W1.4 makes `assess_cell.py` its first consumer; `connect(readonly=)` follows, enforced by extending `db_path_env_audit.py`) **or delete it.** It cannot stay as it is | 0 or −1,889 lines | owner |
| **W7.5** | **One `governance/frozen-surfaces.yaml`**; `.ignore` and `validate_cross_refs.REFERENCE_ONLY` generated from it. Today the two operative lists **intersect in one entry**, and `rg -l "grab bar"` returns 122 files where the database returns 0 rows | net 0 files (two lists become derived) | owner |
| **W7.6** | **Retire `references/global-reference-registry.{md,json}`** to `_archived/` with a redirect stub. It declares itself *"the single source of truth… the registry governs"* over the DB; 531 ids, **0 live**, 35 that never existed even pre-reset, 367 pre-reset sources missing from it. **The authority sentences go regardless of where the file lives** | −2 files | owner |
| **W7.7** | **One banner on all 85 per-slug BPC files**, generated, with a subject-count floor. 70 name a **superseded** governing event (DR-2026-05-23, which reads as recoverable); 16 carry none, including the slug `sessions/LATEST-RESEARCH` points at | — | owner |
| **W7.8** | **Generate `workplan/INDEX.md`** — date-sorted, with a reset-relative status column and this plan's wave ids, registered for freshness like `context_map_fresh`. 74 workplans, ~34,000 lines, no index. The rename was adjudicated FATAL (278 citing files, 9 immutable migrations, 8 forward-only attestations); **the index was adopted in its place and never built** | +1 generated file | none |
| **W7.9** | **Cut `situations` and `external_root_registry`** (+ the two views policing the latter) — 0 rows in the live *and* the archived database, i.e. never written in the project's history | −2 tables, −2 views | owner, **last** — the only irreversible items here and the smallest prize |
| **W7.10** | **Add `disposition:` to the quarantine schema** — not-a-gate / vacuous / red-with-findings / wrong-venue — and extend `known_debt.yaml`'s proven `warrant:` + `lift_when_sql:` to the check registry. **W0.1 is the argument:** "not a gate" and "not run" were allowed to mean the same thing | — | none |

**Not recommended, and each was adjudicated before:** any bulk rename (K3); deleting a quarantined
script (`tooling-register.md` §6.5 makes quarantine-with-reason terminal — and W0.1 shows the list
has value); promoting checks in the same window as branch protection (K4); folding the three
population-link tables or the 15 substantive audit scripts; touching the 49 skills, which survived
three independent tests with nothing cuttable.

---

## Net accounting

**Baseline:** 133 executables · 40,171 lines · 66 tables · 18 views.

| Action | Files | Lines |
|---|---|---|
| W7.1 one-shot layer | **−19** | **−6,074** |
| W7.2 audit merge | −9 | ~−200 |
| W7.3 five folds | −8 tables | — |
| W7.9 cuts | −2 tables, −2 views | — |
| Injection (2 seams, both into `db.py`) | **0** | ~−150 |
| W7.4 if `db.py` is not adopted | −1 | −1,889 |

**Net: 133 → ~105 executables · ~34,000 lines (−15%) · 66 → 56 tables · 18 → 16 views.**

**W7.1 alone delivers 94% of the line reduction, and closes three Wave-1 findings.** If only one
volume item is done, it is that one.

**On injection and the owner's file constraint.** The three injectable idiom families total **492
lines — 1% of all script code.** Injection is a *consistency* measure and must be argued on the two
correctness grounds only: W1.4's schema violation and the read-only handle. Applying the "fewer
files" constraint honestly **drops two of the four seams originally proposed** — `report()` and
`repo_root()` would each need a module *and* a check, for style conventions with no defect history,
and `report()`'s one verdict-changing convention (`EXAMINED:`) is already enforced by
`run_checks.vacuity_failure()`. What survives — id allocators and `connect(readonly=)` — are
database operations that belong in `db.py`, enforced by editing `db_path_env_audit.py`. **Zero new
files.**

---

## Dependency graph

```
W0 (wire the detector) ──▶ W5.1 (correct 5 rows)
       │
W1 (write path) ──▶ W3 (free migrations) ──▶ W4 (adjudication apparatus)
       │                    ▲                        ▲
       │                    │                        │
       └──────────── D-A (value: machine or human?) ─┘
                            │
                     D-B fill band ──▶ W3.1 ──▶ W3.6

W5 (corpus defects) — independent, except W5.3 which waits on W4.5
W6 (method) — independent; W6.1-W6.3 done
W7 (consolidation) — independent, except W7.1 which closes Wave-1 writers
                     and W7.4 which W1.4 begins
```

**The one ordering that must not be violated:** W3 before content. Every W3 item is a migration
against an empty table. **But empty is not neutral** — W1.4 exists because the reset moved a
counter back to a value its own schema forbids and broke the only determination writer, invisibly,
because nothing runs against an empty corpus. Treat the empty window as cheap *and* as
under-tested.

---

## What I would do first, if only one thing

**W1.1 — move four lines.** A repository whose cardinal rule is *never write the database directly*
currently commits foreign-key violations through its own sanctioned write path and reports them as
errors. Everything else assumes the substrate holds. This is unchanged from the original plan and
remains right.

**But do W0.1 first anyway, because it is not a competing claim on attention** — it is a registry
entry for a script that already works and already knows about five wrong rows in the canonical
database. It takes minutes and it is the only item here that finds defects rather than preventing
them.

---

*Every figure re-derived on 2026-08-11 against `d09f923` by the command quoted beside it. Counts of
the database, the check suite and CI status are volatile — the `run_checks --all` total moved
inside a single session because attestation-scoped checks read the git changeset. Re-derive before
acting, and note W6.6: four proxy measurements inflated results across the two sessions that
produced this plan.*
