# 2026-08-12 — Resolution plan for everything the trials, the sweep and the audits found

**Status:** PROPOSED. Nothing below is executed. Three items are marked DONE because the sessions
that found them fixed them while fixing their own defects; everything else is a proposal with a
gate.
**Provenance.** Rewrite in place of the plan authored in PR #93 (merged `bc81070`), retaining its
wave structure, its sequencing rule and most of its content.
**Revision 3** (this one) acts on an independent read-only adjudication of the whole 2,523-line
document set. Revision 1 dropped nine findings while claiming to reconcile its sources; revision 2
restored them and fixed four arithmetic errors; **revision 3 encodes the remaining fifteen
cross-document contradictions, the per-document correction specs, and the guardrail breaches the
adjudication found in this session's own output.** §0.3–§0.5 log all three hops.
**Sources.** `2026-08-12-commit-91-adversarial-review.md` · `2026-08-12-work-log-audit-four-directions.md`
· `2026-08-12-pipeline-phase-state-map.md` · `2026-08-11-remediation-and-pipeline-anatomy.md` Part 1
· `2026-08-09-locator-hierarchy-and-enforcement-probes.md` · `references/tooling-register.md` ·
`2026-08-11-consolidated-review-and-plan.md` · `2026-08-11-per-stage-table-anatomy.md` ·
`2026-08-11-fold-or-cut-ledger.md` · `2026-08-11-reconciled-findings-register.md` ·
`2026-08-11-consolidation-sweep-and-adversarial-pass.md` · `2026-08-11-pr93-reconciliation-and-shared-code.md`.
**Subject:** `adfb675`. **Doctrine SHA:** `0f2f525`.

> **The finding that governs revisions 2 and 3.** Four generations of consolidation ran in 78
> minutes — findings → register → re-register → plan — and **each hop lost findings while claiming
> to supersede its predecessor.** The clearest casualty: the register paired "correct the bad
> values" with "widen the reproducibility gate, because nothing would otherwise notice them coming
> back." Revision 1 kept the correction and dropped the pairing. **A plan that fixes data without
> restoring the detector that guards it is the same defect as W0.1, committed by the plan itself.**

---

## 0. The organising claim

Four statements, and the plan follows from their order:

1. **The write path is not safe to use.** A foreign-key violation commits; a prose word disables
   enforcement; one failed migration voids every migration behind it.
2. **The pipeline determines a state, never a number.** Twelve stages carry evidence to a judgement
   about *how well evidenced* a cell is, then the value is written by hand. That may be correct —
   but it is undeclared, and every Wave 4 operation is downstream of ruling on it.
3. **Green does not mean examined.** The repository contains a working detector for a
   data-corruption class; it is quarantined; **CI runs the *test* of that detector and never the
   detector** (W0.1).
4. **The hole is not diffuse — it is stage 7.** 13 tables are *unwritable outputs* — the pipeline
   reads them, no code can fill them — and **nine are in stage 7**, with stages 8 and 9 inheriting
   the gap. Stages 1–5 work. **Evidence can be gathered and cannot become a value.**

**Sequencing rule, unchanged from PR #93:** fix the substrate, then rule on the boundary, then
build. Wave 3 writes rows, and rows are what make Wave 1 expensive.

**Three rules added by rewriting:**
- *Before building a detector, check whether one exists.* W0.1 and `db.py` are the same lesson.
- *Consolidation without a loss-audit is how findings die.* Every supersession lists what it
  dropped (W6.9).
- *A correction that does not propagate is not a correction.* Nine of the fifteen contradictions in
  Appendix A are a fix applied in one document and left stale in another (W8).

### 0.3 Changes from the PR #93 original

| # | Change | Why |
|---|---|---|
| 1 | New **Wave 0** | The W5.1 detector already exists and is unwired |
| 2 | **W5.1 expanded 1 → 6 rows**, sweep executed | The original called the failure "systematic, not a one-off" and did not run the sweep |
| 3 | **W1.4's fix changed** to "import `db.py`'s function" | `db.py:149` already zero-pads. The bug *is* a re-implementation |
| 4 | **W3.2 contested and replaced** | A bare FK passes trivially on an empty table; 22 of 30 distinct pre-reset values are prose |
| 5 | **W5.4 widened 2 → 9 identifiers** | Only one of the nine is a skill |
| 6 | **Wave 3 given a target order** | Per-stage writer counts identify what unblocks stages 8 and 9 |
| 7 | New **Wave 7 — consolidation** | Absent from the original |
| 8 | Net line/file accounting | The owner's standing constraint |
| 9 | D-B recorded as ratified-with-zero-presence | Restated as W3.1 |

### 0.4 Revision 2 — nine findings restored, four errors fixed

Each was live in a predecessor and absent from revision 1, verified by grep returning 0 hits.

| Restored as | Finding | Was live in | Class |
|---|---|---|---|
| **W1.5** | `pip install -r requirements.txt` fails; header falsely claims two deps suffice | register:107–108 | **BLOCKER** |
| **W1.6** | CLAUDE.md §10 names `session_pointer_resolvable`, a blocking check that does not exist | register:136 | DEFECT |
| **W5.6** | Blocking reproducibility gate compares 93 of 4,245 rows — **2.2%** — excluding `jurisdictional_values` | register:121 | **BLOCKER** |
| **D-C** | Branch protection as an affirmative decision | register:240 | DECISION |
| **W5.7** | The renderer makes evidence-thin populations disappear | register:130 | DECISION |
| **W5.8** | The nine standing advisory failures | register:145 | BACKLOG |
| **W3.9** | The 16-column locator block written out three times | consolidated:216 | DEFECT |
| **W6.8** | The convention-vs-enforcement gap detector | ledger:364–383 | proposed |
| **W7.11** | `references/methodology/` un-finished split; `working/` in no register | sweep:266–268, 280–283 | BACKLOG |

| # | Was | Is | Verification |
|---|---|---|---|
| 1 | W7.3 "−8 tables" | **−6** | G1 −1, G2 −1, G3 −2, G4 −1, G5 −1. The −8 double-counted W7.9's cuts |
| 2 | Net "66 → 56" | **66 → 58** | 66 − 6 folds − 2 cuts |
| 3 | W5.1 "5 rows across 3 items" | **6 rows across 4 items** | `SELECT` returns E-12, B-10, G-04×2, E-07×2 |
| 4 | W7.8 "~34,000 lines" of workplan | **31,189** | `cat workplan/*.md \| wc -l`. The 34,000 was the script-line figure, cross-contaminated |

### 0.5 Revision 3 — what revision 2 left undone

Revision 2 fixed *this plan*. It did not touch the documents feeding it, six of which carry stale
text at HEAD in `workplan/` — a directory **not** covered by `.ignore`, so a future grep hits them
as current. That is CLAUDE.md §9 guardrail 1 (the stale-anchor hazard) reproduced by the very
session that cited it.

| # | Added in revision 3 | Why |
|---|---|---|
| 1 | **Wave 8 — document hygiene**, with per-document correction specs and line numbers | Fifteen contradictions were identified; revision 2 encoded six |
| 2 | **Appendix A — the full contradiction ledger** | So the porting pass in W7.12 has a checklist rather than a memory |
| 3 | **W7.2's quarantine collision resolved**, not merely flagged | Two of the ten scripts it would merge are `status: quarantined`, and `tooling-register.md` §6.5 makes quarantine terminal |
| 4 | **W8.4 — `pr93-reconciliation`'s Part 3 is actively false**: it announces register edits that were never made | It reads as done; two of five clauses are false at HEAD |
| 5 | **Three guardrail breaches by this session's own output** recorded as items | Guardrail 3 (three registers in 78 minutes), guardrail 1 (live stale anchors), and the plan's own R-17 rule (hardcoded volatile figures) |
| 6 | **Revision 3's own loss-audit** — §0.6 | W6.9 applies to this document too |

### 0.6 Revision 3's loss-audit

Carried forward from the adjudication but **not** encoded as plan items, with reasons:

- **The occurrence-matrix statistics** (~35–40% of 2,523 lines restate content stated elsewhere;
  fifteen findings appear in three to five documents). Evidence for W7.12, not an action.
- **A lower-effort variant of W7.12** — keep the ledger as a fifth document with a supersession
  banner instead of retiring it. Recorded here as the fallback; W8.3 makes it viable either way.
- **The confound in W6.8's evidence** — enforcers may have been applied to conventions someone had
  already judged important, so the 75%-vs-50% split is *consistent with* the enforcement spectrum
  working, not proof of it. Stated in W6.8 rather than dropped.

---

## Wave 0 — Before anything else. Two items, minutes each.

| # | Action | Evidence | Falsified if |
|---|---|---|---|
| **W0.1** | **Wire `scripts/audit/jurisdictional_divergence.py` into the registry at `informational`** — the level that already exists for a check whose exit code carries no verdict, which is the correct and honest reason it was quarantined on 2026-08-01 | Run unmodified it prints `[candidate_conflation_or_error] 3 (WARN)` naming B-10, E-12, G-04. `test_jurisdictional_divergence` is meanwhile **registered, active and passing** in the `tests` battery | Its output appears in CI and names no defect |
| **W0.2** | **File the rows it names as W5.1 defects** | see W5.1 | — |

**Why Wave 0.** Every other item needs code or a decision. This needs a registry entry for a script
that already works and already knows about six wrong rows. **The quarantine entry is well-reasoned
and honest; "not a gate" was simply read as "not run."**

---

## Wave 1 — The write path and the bootstrap. No decision required.

| # | Issue | Fix | Evidence | Falsified if |
|---|---|---|---|---|
| **W1.1** | FK check runs **after** `commit()`; the `except`'s `rollback()` rolls back nothing, so a violating migration is committed *and* ledgered | Move `foreign_key_check` above `commit()`; commit only on a clean check | `migrate_db.py:161-183`; Incident A-1 — `search_admissions` 0→1, `data_migrations` 318→319 on a migration that exited 1 | A violating migration leaves no row and no ledger entry |
| **W1.2** | `is_bootstrap = "BOOTSTRAP" in body[:500]` — the `--summary` a session types decides whether FKs are enforced | Delete the substring test; if bulk load needs it, gate on `--allow-fk-violations` a human types and the ledger records | `migrate_db.py:174`; Probe A-3 — identical violation, reworded summary, exit 0 | Probe A-3's payload is rejected under any wording |
| **W1.3** | A failed migration stays pending, is retried first forever, and voids everything behind it | `--skip <id>` writing an abandonment row, or `migrations/failed/`; print `N migration(s) not attempted` whenever the loop aborts | `migrate_db.py:150-187`; Incidents A-4, A-5 | A failure at *k* leaves *k+1…n* attempted or explicitly skipped |
| **W1.4** | `next_gap_id` returns `GAP-1` on the empty table; `schemas/evidence_state.py:167` requires `^GAP-\d{3,4}$`, so the determination writer aborts | **`from db import next_gap_id`** — `db.py:149` already returns `GAP-001` and formats `:03d` | `assess_cell.py:426-429` vs `db.py:149-159` | `assess_cell.py` completes against an empty `gaps` table |
| **W1.5** | **The documented setup command fails.** `pip install -r requirements.txt` → `Cannot uninstall PyYAML 6.0.1, RECORD file not found`. The header states "All scripts … depend only on these two" — false: `adherence_log_audit.py` imports `jsonschema`, hand-installed by `ci.yml` in two jobs | Relax to `PyYAML>=6.0,<7`; add `jsonschema`; delete the false sentence | Reproduced in two independent containers. **CLAUDE.md §7 gives this as step one** | A clean container runs the documented command and gets a working environment |
| **W1.6** | **Three orientation documents describe a check that does not exist.** CLAUDE.md §10 names `session_pointer_resolvable` as blocking; zero hits across `governance/`, `scripts/`, `.github/`. The protection is real under another mechanism — `4fc6304` deleted the watcher and fixed the dispatcher (`run_checks.py:217-229`: blocking + no subject = FAIL, not SKIP) — but the drift-reporting capability it also names **has no replacement** | Name the dispatcher guarantee; delete the phantom check; record the dropped capability as a known gap | grep; `run_checks.py:217-229` | The named check exists |

**Also in this wave:** guard the three unguarded direct writers — one is
`scripts/migrations/session_2026_05_11g_replay.py`, **the only `.py` among 347 files in the
canonical migrations directory**, which replays pre-reset corpus state into `data/guidebook.db` and
is the single item here that can silently reverse DR-2026-08-06 (**W7.1 closes all three**); wire
the registry's `deps:` field, declared since the registry was built and read by nothing; repair
`check-registry.yaml:174`, whose unquoted commas parse to two junk keys and a truncated description
— **reported in four documents, still unfixed, one line**; fix `graph_audit.py:277`, where the crash
is in the **`selftest` path only**.

**Exit condition:** re-run the corridor walk's stage 4a ordering probe and stage 9. The probe must
be rejected *with nothing written*, and `assess_cell.py` must complete.

---

## Wave 2 — Rulings that gate everything after them

### D-A · Is value determination a machine stage or a human one? *(D-METH)*

`assess_cell.py` writes `value_min`, `value_max`, `value_unit` as `None`, unconditionally, and is
the only writer of `evidence_cell_state`. No code path runs from N extracted values to one value.

- **If machine:** stage 9 needs a value-reconciliation step, and Wave 4's paradigm and device
  dimensions become its inputs.
- **If human** — which the Opus floor may deliberately intend — declare it in
  `governance/pipeline-contract.yaml` with an input contract, an acceptance condition and an
  attestation. Today it is three `None`s in a column list, indistinguishable from an oversight.

**Recommendation: human, declared.** Sharpened by the per-stage view: stage 7 has nine unwritable
outputs, so even a machine ruling has nothing to reconcile until Wave 3 lands. Decide now,
implement after.

### D-B · The derived-value marker — ratified, zero repository presence

The owner established on 2026-08-12 that derived values carry a **triangle** — ▲ / ◭ / △ parallel
to ● / ◐ / ○, shape for derivation, fill for evidence strength. Not a ruling to make: a ratified
marker that exists **nowhere** — no glyph in `governance/`, `schemas/`, `scripts/`, `decisions/` or
`references/`; no column; no validator; no renderer. What remains is narrow: **does a derived
marker's fill take the strength of its input evidence, or cap one band below?** Everything else is
W3.1.

### D-C · Branch protection *(D-OP, owner)*

`main` **is not branch-protected**, so a blocking check paints a red X and stops nothing.

**Recommendation: ENABLE — alone, in its own window.** Use the nine-job required set in
`tooling-register.md` §6.7 and heed its three traps, especially: **require `Classify change`**, or a
broken classifier silently skips every battery into a green PR. **Do not add `DB integrity` yet** —
it is 70/70, but roughly 30 of those 70 reference only empty tables, so requiring it today locks in
a vacuous green. It goes in after the vacuity-warrant work.

Revision 1 kept only the negative half ("don't bundle promotions with protection") and dropped the
affirmative recommendation. **Both halves are the decision.**

---

## Wave 3 — Free today, expensive after the first content batch

Every table named is empty. **Target order:** `source_value_extractions` →
`evidence_population_match` → `reasoning_doc_citations`; stages 8 and 9 each read all three.

| # | Fix | Why now |
|---|---|---|
| **W3.1** | **Implement the derived-value triangle.** Glyph and fill semantics into `tier-system.md` §5 beside ●/◐/○; a `synthesis_method` column on `evidence_cell_state` using the vocabulary `armature_v4_resolutions.md:23` already specifies (`direct`/`inferred`/`consensus`) plus `inference_basis`; a renderer that emits it | Ratified doctrine, zero implementation |
| **W3.2** | **Split `evidence_population_match.target_population`** into `target_population_code` (FK to `populations`, nullable) and `target_population_note` (free text); hand-migrate the 64 archived rows | A bare FK passes trivially on 0 rows, but **22 of 30 distinct pre-reset values are prose** and R13 grades study-population against served-population. The split gets a real key with no umbrellas, without discarding R13 |
| **W3.3** | **Doctrine binding on `evidence_cell_state`** (a `doctrine_sha` column), or widen `attestation.schema.json`'s `artifact` pattern so an attestation can name a row | Leg 4 of DR-2026-08-06's four-leg promise |
| **W3.4** | **`CHECK (evidence_type='co1' → tier=1)`** | Doctrine's most distinctive commitment is defended by nothing; `validate_source_co1_fields()` scans `data/sources/*.yaml`, which does not exist |
| **W3.5** | **`assess_cell.py` must write `cell_source_links`**, not only `governing_refs` | The trial's first determination carried 7 governing refs and 0 junction rows, so the page said it had **no governing sources** — false. The honesty mechanism misreports |
| **W3.6** | **Render the value, the marker band, and the gap link** | No value column; no ●/◐/○/▲ anywhere; `GAP-901` and `[BEST-PRACTICE-PENDING]` on no page. Depends on **W3.1** and **D-A** |
| **W3.7** | **Populate `access_needs.typical_stakes`** — 17 rows, three ratified values | 16 of 17 NULL, including `A-SIZE` and `A-REACH`, the two that reach corridor width |
| **W3.8** | **Give the six remaining stage-7 outputs a writer**, or record in `pipeline-contract.yaml` that they are hand-authored: `spec_value_probes`, `item_bpc_links`, `cell_source_links`, `extraction_population_links`, `case_studies`, `economics_entries` | **R12 instructs sessions to write `economics_entries` and no tool can.** A rule naming an unreachable target is worse than no rule |
| **W3.9** | **One locator representation instead of three.** The identical 16-column block sits in `jurisdictional_values` (16 of 32 columns — half the table), `source_value_extractions` (16 of 49) and `reasoning_doc_citations` (16 of 34): **48 columns for one concept** | Free while empty. Pairs with the 2026-08-09 scheme-registry proposal |

---

## Wave 4 — The adjudication apparatus

Gated on **D-A**. Carried from PR #93 unchanged.

| # | Operation | Fix |
|---|---|---|
| **W4.1** | Adjudicate one measurement paradigm over another | A **fourth directness dimension**: a claim-side field (`claim_manoeuvre`/`claim_construct`) — the schema records `measurement_paradigm` on the *source* and nothing records what the *claim* is about — plus `construct_directness()` beside the existing three in `schemas/directness.py`, its doctrine table transcribed into `matrix_consistency.py` so code and doctrine cannot drift. Lift `root_type` into the conditioning layer |
| **W4.2** | Stratify by device class | A third key column on `evidence_cell_state`, or an explicit ruling that equipment stratification is a Population-Mode sub-key. **A doctrine gap:** the Design Mode ladder is universal/population/person, and device class sits between the last two |
| **W4.3** | Derive one item's value from another's | `derived_from_cell_id` + `derivation_rule`, with `derivation_sha` extended to hash upstream cell ids so an upstream change reddens the downstream cell. `connection_targets.target` is un-keyed text |
| **W4.4** | Attach the normative premise licensing a derivation | `access_needs.design_obligation` is the right shape and reaches only to an *item*. Extend to cells. Curate any new access-need code **from** `AX-WHM`, never as a coined umbrella |
| **W4.5** | Adjudicate when the above conflict | `conflicts` is keyed `(item_code, pop_a, pop_b)`; the question generates paradigm×paradigm, equipment×equipment and item×item. Add `conflict_kind` with an FK-keyed target pair per kind |

---

## Wave 5 — Corpus defects, independent of everything above

| # | Defect | Action |
|---|---|---|
| **W5.1** | **One extractor failure — six rows, four items.** It takes a number from anywhere in the value text and stamps the column's unit on it: E-12/ISO `81.0 mm` ← "EN 81-41"; **B-10/GB `54.0 Hz`** ← "EN 54-23", against sibling rows recording the ≤2 Hz photosensitive-epilepsy ceiling; **G-04/FR `1300.0 m²`** ← "1300×1300mm"; **G-04/GB `1500.0 m²`** ← "2200×1500mm"; **E-07/DE `9.0`** and **E-07/AU `3.0`**, class ordinals (`R9–R13`, `P3–P5`) stored as quantities with NULL unit | Correct all six by migration, then re-run W0.1 and confirm the WARN clears. **Do not ship without W5.6** |
| **W5.6** | **Pairs with W5.1.** The blocking `migration_reproducibility` gate compares `PRAGMA user_version` plus `COUNT(*)` on six tables: **93 of 4,245 rows, 2.2%.** A tampered *committed* migration appending `UPDATE slugs SET status='STUB'` rewrote 80 of 106 rows and the gate printed PASS. **`jurisdictional_values` is not among the six** — a correction, a regression, or `DELETE`ing all 109 rows all return PASS | Widen the blocking `COUNT(*)` to all non-exempt tables — cheaper than promoting the deep gate and independent of it. **Fixing W5.1 without this leaves nothing that would notice the values coming back** |
| **W5.2** | E-12's six values are all **platform-lift** specifications under an item named *Entrance Landing and Manoeuvring Space for Power Wheelchair Users* | Owner ruling: does E-12 cover platform lifts? If not, the values belong elsewhere and E-12 has none |
| **W5.3** | `CORRIDOR-W.md` asserts **≥2440 mm** for DEAF signing pairs; E-08 asserts **≥1200 mm**. Four months, neither aware of the other; the matrix was retired as a conflict domain on an unrelated axis, so no open domain exists to file against | Reconcile; rule on whether retiring a domain on one axis closes it for all. Depends on **W4.5** |
| **W5.4** | **5 of 76 attestations fail CHECK 3**, citing 9 unresolvable ids — and **only `integrity-protocol` is a skill.** The other eight are governance rule names (`retire-not-delete`, `commit-msg-format`, `forward-only-migrations`, `doctrine-token-on-synthesis-paths`, `migration-discipline`, `decision-protocol`, `evidence-architecture`, `tier-system`) that `skill-registry.md` has no place for. Valid universe = 60 = 47 skill ids + 13 `EXTRA_RULE_IDS` | **"Register both ids" fixes one ninth.** First decide whether `rules_in_scope` may cite governance rules — a schema question. Then register the 2 missing skills, correct the rest forward-only, add the whole-corpus check |
| **W5.5** | `weighting_profile`: 5 rows, named by three pipeline stages, **touched by no code** | Owner ruling: implement the audience-weighting model or retire it |
| **W5.7** | The renderer makes evidence-thin populations disappear — a doctrinal breach in shipped code | **Carried unverified** from the remediation register §1.0h. Re-derive before acting — it is a doctrinal claim about rendering code, the class this repository has most often found overstated |
| **W5.8** | **The nine standing advisory failures**, all reproducing: `validate_reasoning` · `validate_pydantic_schemas` (246 findings, 49 unmapped tables) · `retired_vocabulary` (69 occurrences) · `site_pages_fresh` (12 stale pages) · `research_dod` R1 · `test_verification_pipeline` 15/18 · `test_directness_2_2` · `test_graph_audit` · `register_integrity_check` selftest. Plus `parts/v10` stale in all 15 files and ungated, and `room_page.py` querying six non-existent tables | Backlog. **Do not clear by silencing** — each needs a leg-level resolution, not a check-level skip |

---

## Wave 6 — Method

| # | Issue | Fix | Status |
|---|---|---|---|
| **W6.1** | The trial has a 105-action verbatim log; the review pronouncing verdicts on another session's work has none | Route review work through the harness | `walk_harness.py` **DONE** |
| **W6.2** | The review cited no log identifier | Log ids on every Break and R-row | **DONE** |
| **W6.3** | A syntax check passed for a test — `ast.parse()` is `EXAMINED: 0` wearing a green tick | Never let a syntax check stand for an execution | **DONE** for the harness |
| **W6.4** | `attestation_evidence` is advisory *and* diff-scoped | Whole-corpus validity is established by no registered check | folds into **W5.4** |
| **W6.5** | E-08 was chosen for realism, and realism made it contaminating | Next trial: synthetic item, units that do not exist | pending |
| **W6.6** | **A regex classification is a candidate list, never a finding.** Four proxy measurements inflated results: 14 unknown rule ids (really 9), 77 "avoidable" f-string interpolations (really ~0, security-shaped), a table-type classifier that put 56 of 66 tables in one bucket, and a source document nearly dropped for using prose headings instead of IDs | State it in `references/project-standards.md` | proposed |
| **W6.7** | **Before building a detector, check whether one exists.** W0.1's sweep was called for and never run while the tool sat quarantined; `db.py` is 1,889 lines that 80 scripts each re-implemented | Same ledger | proposed |
| **W6.8** | **A convention-vs-enforcement gap detector.** For each convention the repo states anywhere, does a registered check enforce it? **Evidence:** dimensions with an enforcer sit at ~75% compliance (`GUIDEBOOK_DB_PATH` 74%, read-only opens 76%); without one, ~50%. **Confound, stated:** enforcers may have gone to conventions already judged important, so this is *consistent with* the spectrum working, not proof | One script against the existing registry. **If it cannot be expressed as a registry check, that is evidence not to build it** | proposed |
| **W6.9** | **Every supersession must publish a loss-audit.** Revision 1 dropped nine findings, two BLOCKER, while claiming to reconcile its sources | A document superseding another lists what it did not carry. §0.4 and §0.6 are the first instances | proposed |
| **W6.10** | **A correction that does not propagate is not a correction.** Nine of the fifteen contradictions in Appendix A are a fix applied in one document and left stale in another — including a retraction whose own document's closing paragraph still states the pre-retraction figure | Same ledger; enforced by W8 | proposed |

---

## Wave 7 — Consolidation

Two folds proposed during the sweep were **retracted**: folding four population-link tables into one
polymorphic table would have traded three enforced foreign keys for one, and folding
`case_study_outcomes` into its parent would have destroyed a per-row tier grade. **The surviving
test: a fold must not destroy a key, and identical column shape is not identical meaning.**

| # | Action | Net | Gate |
|---|---|---|---|
| **W7.1** | **Retire the one-shot importer layer** to `_archived/` — `scripts/convert/` (13), `scripts/db/` (3), `init_database.py`, `phase_jv_appendix_a.py`, the replay script | **−19 files, −6,074 lines.** Closes all three unguarded writers | none, reversible |
| **W7.2** | **Merge the ten single-invariant audit scripts** behind `scripts/audit/invariants.py --check <id>`. The registry dispatches by argument in 27 of 65 entries, so each stays individually registered and quarantinable. **Quarantine collision resolved:** two of the ten — `table_connectivity.py` and `pre_rehab_banner_audit.py` — are `status: quarantined`, and `tooling-register.md` §6.5 makes quarantine terminal. **Merge only the eight unquarantined scripts; leave the two in place.** §6.5 governs the *script's registry status*, and moving a quarantined script's code into a shared module without an owner ruling would empty the quarantine list by the back door | −7 files, ~−150 lines *(revised from −9)* | **Drop first if the result feels like `db.py` again** |
| **W7.3** | **Five FK-safe folds:** `bpc_metadata`→`slugs` (both PK `slug`, 1:1) · `citation_mining`→`source_slug_links` (same grain, two key spellings) · `access_duration`+`access_stakes`+`life_stage_modifiers`→one vocabulary table · `case_study_outcomes`+`case_study_strategies`→one child table · `search_coverage`+`search_languages`→one axis column | **−6 tables** | DDL only, all empty |
| **W7.4** | **Resolve `scripts/db.py`.** 1,889 lines, 43 functions, **zero importers, zero subprocess callers** — while CLAUDE.md §4 calls it "the read/query workhorse". **Adopt** (W1.4 makes `assess_cell.py` its first consumer; `connect(readonly=)` follows, enforced by extending `db_path_env_audit.py`) **or delete** | 0 or −1,889 lines | owner |
| **W7.5** | **One `governance/frozen-surfaces.yaml`**; `.ignore` and `validate_cross_refs.REFERENCE_ONLY` generated from it. The two operative lists **intersect in one entry**, and `rg -l "grab bar"` returns 122 files where the database returns 0 rows | net 0 files | owner |
| **W7.6** | **Retire `references/global-reference-registry.{md,json}`** with a redirect stub. It declares itself *"the single source of truth… the registry governs"* over the DB; 531 ids, **0 live**, 35 that never existed even pre-reset, 367 pre-reset sources missing. **The authority sentences go regardless of where the file lives** | −2 files | owner |
| **W7.7** | **One banner on all 85 per-slug BPC files**, generated, with a subject-count floor. 70 name a **superseded** governing event; 16 carry none | — | owner |
| **W7.8** | **Generate `workplan/INDEX.md`** — date-sorted, reset-relative status column, wave ids, registered for freshness. **74 workplans, 31,189 lines, no index** | +1 generated file | none |
| **W7.9** | **Cut `situations` and `external_root_registry`** (+2 views policing the latter) — 0 rows in the live *and* archived databases | −2 tables, −2 views | owner, **last** |
| **W7.10** | **Add `disposition:` to the quarantine schema** — not-a-gate / vacuous / red-with-findings / wrong-venue — and extend `known_debt.yaml`'s `warrant:` + `lift_when_sql:` to the check registry. **W0.1 is the argument: "not a gate" and "not run" were allowed to mean the same thing** | — | none |
| **W7.11** | **Two unregistered surfaces.** `references/methodology/` carries an un-finished split (`economics-research-methodology-v1.9-archived.md` contains four descendant files at 83–98% containment, kept in the live directory); `working/` — 39 files, ~1.1 MB, wholly corpus-derived — is in no register | — | owner |
| **W7.12** | **Consolidate this session's seven documents to four.** ~35–40% of 2,523 lines restate content stated elsewhere; fifteen findings appear in three to five documents. **Keep:** this plan · `consolidated-review-and-plan.md` (register of record) · `consolidation-sweep-and-adversarial-pass.md` (frozen-corpus evidence) · `per-stage-table-anatomy.md` (unchanged). **Retire with redirect stubs, after the W8 porting pass:** `reconciled-findings-register.md`, `pr93-reconciliation-and-shared-code.md`, `fold-or-cut-ledger.md` | −3 files, ~−900 lines | owner. **W8 first — every prior consolidation here lost findings** |
| **W7.13** | **Rename the consolidated review's Class IDs.** `A1`–`F8` collide with the remediation register's `A1`/`C1`/`D1`, the locator probes' `C1`, and two existing `F`-series — reintroducing at generation 3 the defect the generation-2 register existed to fix. Cited nowhere outside their own document | — | none |
| **W7.14** | **Preserve `scratchpad/stages.json` as committed data; discard the rest.** It is the stage→table extraction behind the phase-multiplicity test, the ledger's Part 1 and the r = 0.73 validation — a judgment extraction from a 6,775-line document that none of them reproduces. `allpy.txt`, `gb.txt`, `gb2.txt`, `ga.err`, `purpose.json`, `blk/` are mechanically reproducible | +1 data file | none |

**Not recommended, each adjudicated before:** bulk renames (K3); deleting a quarantined script
(§6.5 — and W0.1 shows the list has value); promoting checks in the same window as branch
protection (K4); folding the three population-link tables or the 15 substantive audit scripts;
touching the 49 skills, which survived three independent tests with nothing cuttable.

---

## Wave 8 — Document hygiene: port the unique content, then correct the stale text

**The precondition for W7.12.** Every document below carries text that is stale at HEAD, in
`workplan/`, which `.ignore` does **not** cover — so a future grep hits it as current. This is
CLAUDE.md §9 guardrail 1 reproduced by the session that cited it.

| # | Document | Port before retiring | Correct in place | Then |
|---|---|---|---|---|
| **W8.1** | `reconciled-findings-register.md` | §0.2 namespace-collision table (37–52) · §2.1's executed A2 refutation, the only run adjudication of a source contradiction (152–174) · Part 6 near-miss (282–290) → into `consolidated-review-and-plan.md` as appendices | **R-07 (line 85)** still asserts the database "asserts a 27× flash rate"; the impact was recalibrated to *latent, not published* and never propagated. **R-24 (line 138)** still frames the finding as two missing skills / four attestations; superseded by 9 identifiers, only one a skill. **Part 4 (220–248)** was declared retired by a document that never edited it | retire with stub |
| **W8.2** | `pr93-reconciliation-and-shared-code.md` | §1.1 R↔W cross-map (27–37) — **the only Rosetta stone joining the two ID systems** — into §0.3 of this plan · the 60-identifier decomposition (line 92) into W5.4 | **Part 3 (235–246) is actively false.** It announces that the register "gains R-28…R-32" and that its Part 4 "is retired" — neither happened. Two of five clauses false at HEAD | retire with stub |
| **W8.3** | `fold-or-cut-ledger.md` | Part 1 phase-multiplicity distribution (35–53) · §2.6 `v_coverage_priority`, 7,210 rows and no reader (192–195) · Part 4 bucket census (223–229) · Part 5 three-way skill test (258–280) · §7.2 measured consistency percentages (338–383) | **Line 110** says "corrected from −9 to **−6 (66 → 60)**" — reflects only the §2.1 retraction, never updated for §2.3. **Line 124** heading still asserts "Case studies **5 → 3**, economics **3 → 2**" above its own correction box concluding "Net: 0 tables". **Lines 304–307** — the document's *closing paragraph* — still say "removes **9 tables**… **seven of the nine table folds** are free", contradicting its own Part 0 (line 20: −3) and §7.1 (line 332). **Lines 243–252** propose retiring two quarantined scripts while line 228 says quarantine is terminal | retire with stub, **or** keep as a fifth document with a supersession banner — the fallback in §0.6 |
| **W8.4** | `consolidated-review-and-plan.md` *(a keeper)* | — | **Part 2 Class F (216–217) and §3.5 (284–292)** still net −3 tables with no G1–G5 rows; Part 6 (422–496) revises to −8 and was never propagated back, so a reader of the register alone gets the superseded figure. **§5.4 (403) and §6.4 (481)** use −18 files / −5,850 lines for the one-shot layer; measured is **19 / 6,074** — the 224-line delta is exactly the replay script. **Executables "~106" (410, 481)** follows from the wrong 18; correct is **105**. **Part 3 (225–301)** duplicates this plan's waves ~85% and should reduce to the P1–P4 rationale plus a pointer here — **today two documents both present themselves as the plan** | keep, corrected |
| **W8.5** | `consolidation-sweep-and-adversarial-pass.md` *(a keeper)* | — | **Part 3 (463–493)** is the first of four generations of sequencing and is dead — mark superseded by this plan. Add the header the register proposed and never applied | keep, banner |
| **W8.6** | `per-stage-table-anatomy.md` *(a keeper)* | — | Header says "66 tables" (line 11) while Part 3 says "24 of 67" (line 265). Both correct — 67 counts `sqlite_sequence` — but the convention is stated nowhere. **State it once, here and there** | keep, one line |
| **W8.7** | **All six superseded/keeper documents** | — | None carries the supersession header the register's Part 5 (253–258) proposed. **Apply it** — one line each, pointing at this plan for status | the cheapest item in Wave 8 |

**W8 sequencing:** W8.7 first (seven one-line headers stop the bleeding immediately), then W8.1–W8.3
porting, then W8.4–W8.6 corrections, then W7.12 retirement. **Retiring before porting is the one
ordering that reproduces the defect this wave exists to fix.**

---

## Net accounting

**Baseline:** 133 executables · 40,171 script lines · 66 tables · 18 views · 74 workplans (31,189 lines).

**Two ledgers, kept separate** — an earlier draft of this table put executables and workplan
documents in one "Files" column, which is the same conflation §0.4 corrected in the workplan
line-count. Scripts and prose are not fungible.

**Executables and script lines**

| Action | Files | Lines |
|---|---|---|
| W7.1 one-shot layer | **−19** | **−6,074** |
| W7.2 audit merge (8 of 10) | −7 | ~−150 |
| Injection (2 seams, both into `db.py`) | **0** | ~−150 |
| W7.4 if `db.py` is not adopted | −1 | −1,889 |
| **Net** | **133 → 107** | **40,171 → ~33,800 (−16%)** |

**Database objects**

| Action | Tables | Views |
|---|---|---|
| W7.3 five folds | −6 | — |
| W7.9 cuts | −2 | −2 |
| **Net** | **66 → 58** | **18 → 16** |

**Workplan documents**

| Action | Files | Lines |
|---|---|---|
| W7.12 consolidation (7 → 4) | −3 | ~−900 |
| W7.8 generated index | +1 | small |
| **Net** | **74 → 72** | **31,189 → ~30,300** |

**W7.1 alone is 94% of the executable line reduction** and closes three Wave-1 findings.

**On injection and the file constraint.** The three injectable idiom families total **492 lines — 1%
of script code.** Injection is a *consistency* measure, argued only on its two correctness grounds:
W1.4's schema violation and the read-only handle. Applying "fewer files" honestly **drops two of the
four seams originally proposed** — `report()` and `repo_root()` each need a module *and* a check, for
style conventions with no defect history, and `report()`'s one verdict-changing convention
(`EXAMINED:`) is already enforced by `run_checks.vacuity_failure()`. What survives — id allocators
and `connect(readonly=)` — are database operations belonging in `db.py`, enforced by editing
`db_path_env_audit.py`. **Zero new files.**

---

## Dependency graph

```
W0 (wire the detector) ──▶ W5.1 (correct 6 rows) ──▶ W5.6 (widen the gate)
       │                          ▲                        │
       │                          └── must ship together ──┘
       │
W1 (write path + bootstrap) ──▶ W3 (free migrations) ──▶ W4 (adjudication)
       │                              ▲                        ▲
       └──────────── D-A (value: machine or human?) ───────────┘
                            │
                     D-B fill band ──▶ W3.1 ──▶ W3.6
                     D-C branch protection — alone, its own window

W5 — independent, except W5.3 (waits on W4.5) and W5.1 (pairs with W5.6)
W6 — independent; W6.1-W6.3 done
W7 — independent, except W7.1 (closes Wave-1 writers), W7.4 (begun by W1.4)
W8 ──▶ W7.12   (port and correct BEFORE retiring — non-negotiable)
```

**The ordering that must not be violated:** W3 before content. Every W3 item is a migration against
an empty table. **But empty is not neutral** — W1.4 exists because the reset moved a counter to a
value its own schema forbids and broke the only determination writer, invisibly, because nothing
runs against an empty corpus.

---

## What to do first

**W8.7, W0.1, then W1.1.**

**W8.7** is seven one-line headers. Six documents in `workplan/` carry stale text that a grep will
return as current, including a retraction whose own closing paragraph states the pre-retraction
figure. It costs minutes and stops the repository from lying to its next session.

**W0.1** is a registry entry for a script that already works and already names six wrong rows. It is
the only item here that *finds* defects rather than preventing them.

**W1.1** is four lines. A repository whose cardinal rule is *never write the database directly*
commits foreign-key violations through its own sanctioned write path and reports them as errors.

**And W5.1 does not ship without W5.6.** Correcting six values in a table the blocking gate does not
watch leaves nothing to notice them coming back — the defect this plan opens by describing.

---

## Appendix A — The contradiction ledger

Fifteen cross-document contradictions, each verified at `adfb675`. **Nine are a correction applied
in one document and left stale in another** (W6.10). Dispositions are W8 items.

| # | Contradiction | Locations | Adjudication | Fixed by |
|---|---|---|---|---|
| **C1** | Ledger: "corrected from −9 to −6 (66 → 60)" vs Part 0 "66 → 63, net −3" vs §7.1 "falls from −9 to −3" | ledger:110, 20, 332 | Line 110 stale — reflects only the §2.1 retraction, not §2.3 | W8.3 |
| **C2** | §2.3 heading asserts "Case studies 5 → 3, economics 3 → 2" above its own box concluding "Net: 0 tables" | ledger:124 vs 149 | Heading never updated | W8.3 |
| **C3** | Closing paragraph: "removes 9 tables… seven of the nine table folds are free" | ledger:304–307 | **Pre-retraction figures in the document's own conclusion** | W8.3 |
| **C4** | Consolidated Part 2 + §3.5 net −3 tables; Part 6 says −8 | consolidated:216–217, 284–292 vs 477–484 | Part 6 declares itself a revision; register and plan sections never amended | W8.4 |
| **C5** | Tables end-state 58 vs 56 | consolidated:479 vs plan rev-1 | **Plan was wrong**; folds are −6, cuts −2 | §0.4 ✓ |
| **C6** | One-shot layer 19/6,074 vs 18/5,850 → executables 105 vs ~106 | ledger:250, consolidated:218 vs 403, 481 | **19/6,074/105 correct**; the 224-line delta is the replay script | W8.4, §0.4 ✓ |
| **C7** | "5 rows across 3 items" vs an enumeration listing six across four | consolidated:75 vs 76–77; plan rev-1 | Arithmetic never matched its own list | §0.4 ✓ |
| **C8** | Executables 132 vs 133 | ledger:12 vs consolidated:91, plan:250 | Both right at their subjects; **133 at HEAD**, excluding the package marker — convention unstated | W8.6 |
| **C9** | R-24 framing: two missing skills / four attestations vs 9 identifiers, one a skill | register:138 vs consolidated:187 | Correction never propagated back | W8.1 |
| **C10** | R-07: database "asserts" a 27× rate vs "no rendered surface publishes 54 Hz" | register:85 vs consolidated:45–52 | Recalibration never propagated back | W8.1 |
| **C11** | Workplans 66 → 69 → 74; lines 28,347 → ~29,000 → ~34,000 | sweep:169–177, consolidated:206, plan rev-1 | **74 files correct; 31,189 lines** — the 34,000 was cross-contaminated from the script total | §0.4 ✓ |
| **C12** | Tables 66 vs 67 | sweep:29 vs ledger:12, per-stage:11 vs per-stage:265 | Both right — 67 counts `sqlite_sequence`; convention unstated | W8.6 |
| **C13** | Ledger says quarantine is terminal, then proposes retiring two quarantined scripts | ledger:228 vs 243–252; also `tooling-register.md` §6 item 5 | Internal contradiction; collides with a withdrawn proposal | W8.3, W7.2 |
| **C14** | pr93 Part 3 announces register edits that were never made | pr93:237–246 vs register at HEAD | Reads as done; two of five clauses false | W8.2 |
| **C15** | The register was created to end ID collisions, then the consolidated review minted colliding Class IDs | register:37–52, 265–266 vs consolidated:160–221 | Generation 3 reintroduced the generation-2 defect | W7.13 |

---

## Appendix B — Guardrail compliance of this session's own output

**Complied.** Nothing was executed: no file moved, no register edited, no DB write. Every
owner-gated class — retirements, `.ignore`, D-SCHEMA, DG-NON — is proposed, satisfying CLAUDE.md §9
guardrails 2 and 4. All commits touch only `workplan/`, so no doctrine token or attestation was
owed; formats pass. Bulk renames and quarantine deletion are refused in every generation. **The
rewrite-in-place with a change log, rather than an eighth file, is the right instinct** and the one
this plan keeps.

**Breached.**

1. **Guardrail 3 — "don't spin up a new register; extend the existing apparatus."** Three
   registers/sequences in 78 minutes, none extending the other in place. The register's own Part 5
   knew the fix — a header line — and no header was ever applied. **→ W8.7.**
2. **Guardrail 1 — "re-verify divergence claims; stale anchors cause real errors."** Six documents
   carry live stale text at HEAD in a directory `.ignore` does not cover. **→ W8.1–W8.6.**
3. **The plan's own R-17 rule — "neither number should be written down anywhere."** The terminal
   documents hardcoded volatile figures and got four of them wrong, after three documents had
   demonstrated why not to. **→ §0.4, and W6.6.**

**Does the W7.12 merge violate anything?** No — provided it runs the sanctioned way: retirement to
`_archived/workplan/` mirroring origin paths, redirect stubs (guardrail 2), owner sign-off
(guardrail 4). The caller sweep is done: the only non-archived inbound citations are intra-set, so
stubs fully discharge rule 5. **What would breach it is deletion without stubs, or culling before
W8 — because every consolidation attempted in this session without a porting pass lost findings.**

---

*Every figure re-derived on 2026-08-11 against `adfb675` by the command quoted beside it. Revision 2
restored nine findings and fixed four arithmetic errors; revision 3 encodes fifteen contradictions,
seven per-document correction specs and three guardrail breaches. §0.6 is revision 3's own
loss-audit. Counts of the database, the check suite and CI are volatile — the `run_checks --all`
total moved within a single session because attestation-scoped checks read the git changeset.
Re-derive before acting.*
