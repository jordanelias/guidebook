# 2026-08-12 — Resolution plan for everything this session found

**Status:** PROPOSED. Nothing below is executed. Two items are marked DONE because this session
did them while fixing its own defects; everything else is a proposal with a gate.
**Sources:** `2026-08-12-commit-91-adversarial-review.md` (Breaks 1–4, render gaps R1–R4,
Parts 6–7) · `2026-08-12-work-log-audit-four-directions.md` (directions 1–4, addendum 2) ·
`2026-08-12-pipeline-phase-state-map.md` (boundary losses).
**Predecessor register:** `workplan/2026-08-11-remediation-and-pipeline-anatomy.md` Part 1.
This plan does **not** restate that register; it adds what the trials found and sequences both.

---

## 0. The organising claim

The predecessor register asked *"does the structure work before content?"* and answered
"partly". Two trials and an audit sharpen that into three statements, and the plan follows from
their order:

1. **The write path is not safe to use.** A foreign-key violation commits; a prose word disables
   enforcement; one failed migration voids every migration behind it. Until that is fixed, every
   other item on this list is being built on a substrate that silently accepts bad rows and
   silently discards good ones.
2. **The pipeline determines a state, never a number.** Twelve stages carry evidence to a
   judgement about *how well evidenced* a cell is, and then the value is written by hand. That
   may be correct — but it is undeclared, and everything in Part 6 (paradigm adjudication, device
   stratification, cross-item derivation) is downstream of ruling on it.
3. **Green does not mean examined.** Five of this session's seven self-caught errors were caught
   by executing something; none by proofreading. The apparatus's own worst failure mode reproduced
   inside the review of it, twice.

**Sequencing rule:** fix the substrate, then rule on the boundary, then build. Do not reorder —
items in Wave 3 write rows, and rows are what make Wave 1 expensive.

---

## Wave 1 — The write path. No decision required, four files.

Nothing else should ship first. Each is small, each is falsifiable, none needs an owner.

| # | Issue | Fix | Evidence | Falsified if |
|---|---|---|---|---|
| **W1.1** | FK check runs **after** `commit()`; the `except`'s `rollback()` rolls back nothing, so a violating migration is committed *and* ledgered | Move the `foreign_key_check` above the `commit()`; commit only on a clean check | `migrate_db.py:161-183`; log Incident A-1 — `search_admissions` 0→1 and `data_migrations` 318→319 on a migration that exited 1 | A violating migration, applied, leaves no row and no ledger entry |
| **W1.2** | `is_bootstrap = "BOOTSTRAP" in body[:500]` — the `--summary` text a session types decides whether FKs are enforced | Delete the substring test. If a bulk load genuinely needs it, gate on an explicit `--allow-fk-violations` flag that a human types and the ledger records | `migrate_db.py:174`; log Probe A-3 — identical violation, reworded summary, exit 0 | Re-running Probe A-3's payload with any summary wording is rejected |
| **W1.3** | A failed migration stays pending, is retried first forever, and voids every migration behind it. The documented fix-forward remedy is queued behind the failure it compensates for | Add a quarantine: `--skip <id>` writing an abandonment row, or `migrations/failed/`. Separately, print `N migration(s) not attempted` whenever the loop aborts | `migrate_db.py:150-187`; log Incidents A-4 and A-5 — two authoring mistakes, eight discarded migrations, an error naming a file from two stages earlier | A failure in migration *k* leaves migrations *k+1…n* attempted or explicitly reported as skipped |
| **W1.4** | `next_gap_id` returns `GAP-1` on the post-reset empty table; `schemas/evidence_state.py` requires 3–4 digits, so the determination writer aborts on the first cell needing a gap | Zero-pad to three digits | `assess_cell.py:426-429`; log Stage 9b.4 traceback | `assess_cell.py` completes a run against an empty `gaps` table |

**Also in this wave, already carried by the predecessor register and independently confirmed:**
guard the three unguarded direct writers; wire the registry's `deps:` field; repair the malformed
`governance` battery YAML; fix the `graph_audit.py:277` crash.

**Wave 1 exit condition:** re-run the corridor walk's stage 4a ordering probe and stage 9. The
probe must be rejected *with nothing written*, and `assess_cell.py` must complete.

---

## Wave 2 — Two rulings that gate everything after them

Both are owner decisions. Both are cheap to *decide* and expensive to defer, because Wave 3
writes rows and rows are what close the free window.

### D-A · Is value determination a machine stage or a human one? *(D-METH)*

`assess_cell.py` writes `value_min`, `value_max` and `value_unit` as `None`, unconditionally, and
is the only writer of `evidence_cell_state`. There is no code path from N extracted values to one
determined value.

- **If machine:** stage 9 needs a value-reconciliation step, and Wave 4's paradigm and device
  dimensions become its inputs.
- **If human** — which the Opus floor may deliberately intend — then say so in
  `governance/pipeline-contract.yaml` as a stage with an input contract, an acceptance condition
  and an attestation. Today it is three `None`s in a column list, which is indistinguishable from
  an oversight.

**Recommendation: human, declared.** The judgement is doctrinal, not arithmetic. But it must stop
being implicit, because every Part 6 operation assumes an answer.

### D-B · What tier does a derived value carry? *(D-DOCT, owner-only)*

**Superseded in scope by the owner's correction of 2026-08-12**, which establishes that derived
values are marked by a **triangle with the same fill scheme** — ▲ / ◭ / △ parallel to ● / ◐ / ○,
shape carrying derivation and fill carrying evidence strength.

So this is no longer a ruling to make. It is a **ratified marker with zero repository presence**:
no glyph in `governance/`, `schemas/`, `scripts/`, `decisions/` or `references/`; no column; no
validator; no renderer. What remains for the owner is narrow — whether the fill of a derived
marker takes the strength of its *input evidence* or is capped one band below it. Everything else
is implementation, and it moves to W3.1.

---

## Wave 3 — Free today, expensive after the first content batch

Every table named is empty. Each of these is a migration that costs nothing now and requires a
backfill later.

| # | Fix | Why now |
|---|---|---|
| **W3.1** | **Implement the derived-value triangle.** Glyph and fill semantics into `tier-system.md` §5 beside ●/◐/○; a `synthesis_method` column on `evidence_cell_state` using the vocabulary `governance/armature_v4_resolutions.md:23` already specifies (`direct` / `inferred` / `consensus`) plus its `inference_basis` companion; a renderer that emits it | Ratified doctrine, zero implementation. 0 rows |
| **W3.2** | **FK on `evidence_population_match.target_population`** → `populations` | 0 rows. Today the column accepts `WHEELCHAIR-USERS-GENERALLY` — the umbrella the work-from-axes rule prohibits — and it fails *silently*, because `assess_cell.py:180` matches by regex so a malformed value reads as absent |
| **W3.3** | **Doctrine binding on `evidence_cell_state`** (a `doctrine_sha` column), or widen `attestation.schema.json`'s `artifact` pattern so an attestation can name a row | Leg 4 of DR-2026-08-06's four-leg promise. No doctrine column exists anywhere in the DB |
| **W3.4** | **`CHECK (evidence_type='co1' → tier=1)`** | Doctrine's most distinctive commitment is defended by nothing: no CHECK, no test, no registry entry, and `validate_source_co1_fields()` scans `data/sources/*.yaml`, which does not exist. One table constraint, 0 rows |
| **W3.5** | **`assess_cell.py` must write `cell_source_links`**, not only `governing_refs` | The trial's first real determination carried 7 governing refs and 0 junction rows, and the page therefore stated it had **no governing sources** — false. The honesty mechanism is what misreports |
| **W3.6** | **Render the value, the marker band, and the gap link** (R1–R3) | The determination table has no value column; no `●`/`◐`/`○`/▲ renders anywhere; `GAP-901` and `[BEST-PRACTICE-PENDING]` appear on no page |
| **W3.7** | **Populate `access_needs.typical_stakes`** — 17 rows, three ratified values | 16 of 17 are NULL, including `A-SIZE` and `A-REACH`, the two that reach corridor width. This is the dimension that decides whether a parameter is a comfort question or an exclusion threshold |

**W3.6 depends on W3.1** (the marker set must exist before a renderer can emit it) and on **D-A**
(if the value is human-written, the renderer reads a different field).

---

## Wave 4 — The adjudication apparatus (Part 6's four operations)

Gated on **D-A**. This is the machinery the guidebook's actual product needs, and none of it
exists.

| # | Operation | Fix |
|---|---|---|
| **W4.1** | Adjudicate one measurement paradigm over another | A **fourth directness dimension**. Add a claim-side field (`claim_manoeuvre` / `claim_construct`) — the schema records `measurement_paradigm` on the *source* and nothing anywhere records what the *claim* is about — and a `construct_directness()` function beside the existing three in `schemas/directness.py`, with its doctrine table transcribed into `matrix_consistency.py` so code and doctrine cannot drift. Lift `root_type` into the conditioning layer at the same time; it is construct validity in embryo and never reaches `classify()` |
| **W4.2** | Stratify a determination by device class | Either a third key column on `evidence_cell_state` or an explicit ruling that equipment stratification is a Population-Mode sub-key. **This is a doctrine gap, not a schema one:** the Design Mode ladder is `universal` / `population` / `person`, and device class sits between the last two |
| **W4.3** | Derive one item's value from another's | `evidence_cell_state.derived_from_cell_id` + `derivation_rule`, with `derivation_sha` extended to hash upstream cell ids so an upstream change reddens the downstream cell. Today nothing represents a cross-item dependency and `connection_targets.target` is un-keyed text |
| **W4.4** | Attach the normative premise that licenses a derivation | `access_needs.design_obligation` is the right column shape and reaches only as far as an *item*, via `access_need_axis_map → axes → item_axis_links`. Extend it to cells. Curate any new access-need code **from** `AX-WHM`, never as a coined umbrella |
| **W4.5** | Adjudicate when the above conflict | `conflicts` is keyed `(item_code, pop_a, pop_b)` and the question generates three shapes it cannot hold: paradigm×paradigm, equipment×equipment, item×item. Add `conflict_kind` with an FK-keyed target pair per kind |

---

## Wave 5 — Corpus defects, independent of everything above

These are wrong data in the canonical database today. They do not wait on any ruling.

| # | Defect | Action |
|---|---|---|
| **W5.1** | `jurisdictional_values.jv_id=40`: E-12 / ISO / **`value_numeric = 81.0 mm`**, parsed out of the standard designation *"References EN 81-41"* in the value text | Correct by migration. Then sweep `jurisdictional_values` for other numerics extracted from standard designations — the extractor's failure mode is systematic, not a one-off |
| **W5.2** | E-12's six jurisdictional values are all **platform-lift** specifications (ADA §410 / ASME A18.1, BS 6440, EN 81-41, AS 1735.12) under an item named *Entrance Landing and Manoeuvring Space for Power Wheelchair Users* | Owner ruling: does E-12 cover platform lifts? If not, the values belong elsewhere and E-12 has none |
| **W5.3** | `references/conflict-matrices/CORRIDOR-W.md` asserts **≥2440 mm** for DEAF signing pairs as Universal Mode; E-08's title asserts **≥1200 mm**. Four months, neither aware of the other. The matrix was also *retired* as a conflict domain on an unrelated axis, so there is no open domain to file a new conflict against | Reconcile the two values; and rule on whether retiring a conflict domain on one axis should close it for all axes. Depends on **W4.5** for the row shape |
| **W5.4** | `integrity-protocol` and `supersession-audit` are authored skills on disk with no identifier in `references/skill-registry.md`, so no attestation may cite them. The check that catches this fires only when an attestation names one — the wrong end — and is advisory *and* diff-scoped, so the 74-attestation corpus has never been checked | Register both ids. Add a check that compares `skills/*_SKILL.md` against the registry directly, and one that validates the whole attestation corpus rather than the diff |

---

## Wave 6 — Method, so the next session does not repeat this one

| # | Issue | Fix | Status |
|---|---|---|---|
| **W6.1** | The trial has a 105-action verbatim log; the review that pronounces CONFIRMED and OVERSTATED on another session's work has **none**. 19 load-bearing verdicts have their commands quoted in prose and their outputs unrecorded | Route review-lens work through the harness. `run()` already logs argv, cwd, exit code, stdout, stderr and per-table deltas for any command, at no cost beyond invoking it | `scripts/tests/walk_harness.py` **DONE** — mandatory `WALK_TREE`, refuses the canonical repository by name, `--selftest` 3/3 |
| **W6.2** | The review cited **no** log identifier; claims joined to evidence by prose | Log ids on every Break and R-row | **DONE** |
| **W6.3** | A syntax check passed for a test. `ast.parse()` on a module is `EXAMINED: 0` wearing a green tick — and the file it passed defaulted to the canonical database | Never let a syntax check stand in for an execution. Where a shipped file has a guard, the guard needs a selftest that must import the module to prove it fires | **DONE** for the harness; the general lesson belongs in `references/project-standards.md` |
| **W6.4** | A blocking-adjacent check (`attestation_evidence`) is advisory *and* diff-scoped, so an invalid rule identifier merged in PR #92 | Same shape as `attestation_schema`, already noted in the predecessor register. Whole-corpus validity is established by no registered check | folds into **W5.4** |
| **W6.5** | Clean-room testing: E-08 was chosen for realism, and realism is what made it contaminating | Next trial uses a synthetic item outside the live code space, a parameter that does not exist in the built environment, in units that do not exist. Real `population_code` values only where an FK demands one | pending the next test |

---

## Dependency graph, compressed

```
W1 (write path)  ──▶ W3 (free migrations) ──▶ W4 (adjudication apparatus)
       │                    ▲                        ▲
       │                    │                        │
       └──────────── D-A (value: machine or human?) ─┘
                            │
                     D-B (derived-marker fill band) ──▶ W3.1 ──▶ W3.6

W5 (corpus defects) — independent, except W5.3 which waits on W4.5
W6 (method) — independent; W6.1-W6.3 already done
```

**The one ordering that must not be violated:** W3 before content. Every W3 item is a migration
against an empty table. The predecessor register made this argument and the trials sharpened it —
but with one correction that matters. Its framing was that the empty state is a pure
opportunity. **Empty is not neutral.** W1.4 exists because the clean-room reset moved a counter
back to a value its own schema forbids and broke the only determination writer, invisibly,
because nothing runs against an empty corpus. Treat the empty window as cheap *and* as
under-tested.

---

## What I would do first, if only one thing

**W1.1 — move four lines.** A repository whose cardinal rule is *never write the database
directly* currently commits foreign-key violations through its own sanctioned write path and
reports them as errors. Everything else on this list assumes the substrate holds.
