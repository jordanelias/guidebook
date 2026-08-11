# 2026-08-11 — Consolidated adversarial review, register, and remediation plan

**Status:** REVIEW + REGISTER + PLAN. Nothing executed. This document supersedes, **for status
and sequencing**, the four documents this session produced; it does not supersede their evidence.
**Method:** four lenses — factuality, method, logic, impact — applied to my own work first, with
default verdict REFUTED and CONFIRMED only on re-derivation. Then one register. Then a plan
organised on the owner's five axes: inconsistencies, injections, centralisation, deduplication,
consolidation.
**Subject:** `d09f923` (this branch merged with `bc81070`, i.e. PR #93 included).
**Doctrine SHA:** `0f2f525`.

> **The single most important thing found this session was not found by me.** The repository
> already contains a working detector for the data-corruption class I reported as new. It is
> `scripts/audit/jurisdictional_divergence.py`, it is quarantined, it exits 0, and **its report
> names every bad row I found plus two I did not** (§1.1). My contribution was running it.

---

## Part 0 — The answer in one page

| Lens | Verdict on my own work |
|---|---|
| **Factuality** | 4 claims refuted or materially recalibrated, 2 of them headline. Core measurements reproduce. |
| **Method** | The phase-multiplicity test **survives** its own validation (r = 0.73 against code reachability) and its one real disagreement is a finding, not an error. Two proxy measurements inflated counts and were caught by running the real thing. |
| **Logic** | The consolidation reasoning failed the same way twice — structural similarity read as semantic identity — and both folds were retracted. |
| **Impact** | Overstated once (a "safety-relevant" value that is **latent, not published**), understated once (the extractor defect is 5 rows across 3 items, not 1). |

**What survives, ranked by consequence:**

1. **Five false numeric values in the live database**, from one systematic extractor failure — and an existing quarantined check that names all five (§1.1).
2. **The write path is unsafe** — PR #93's W1.1–W1.4, independently confirmed (§1.2).
3. **A 1,889-line shared library with zero consumers**, and a Wave-1 bug that is a
   re-implementation of one of its correct functions (§1.3).
4. **The frozen corpus is unmarked** — 122 files answer a live question, the DB answers zero (§1.4).
5. **Nine unknown rule identifiers** across the attestation corpus; only one is a skill (§1.5).

---

## Part 1 — Adversarial review

### 1.1 FACTUALITY — the finding I was proudest of, corrected twice

**R-07 as I reported it:** *"B-10 carries `value_numeric = 54.0`, `unit = 'Hz'`, parsed from the
standard name 'EN 54-23'… the database therefore asserts a visual-alarm flash rate 27× the
photosensitive-epilepsy ceiling."*

**Correction 1 — impact overstated.** I checked whether the value is rendered. The only match on
a shipped surface is `parts/v10/part13.md`, and it is the **bibliographic string** "BS EN
54-23:2010", not a flash rate. **No rendered surface publishes 54 Hz.** The defect is a wrong row
that would poison the first determination to use it — real, and *latent*, not a false claim
currently shown to a reader. My wording implied the latter.

**Correction 2 — attribution and scope both wrong.** `scripts/audit/jurisdictional_divergence.py`
already detects this class. Run today, unmodified:

```
[candidate_conflation_or_error] 3 (WARN)
  B-10: values span 2.0-54.0Hz across 3 jurisdictions (x27 range) — too wide for one parameter;
        likely different quantities sharing unit 'Hz' or a data error, NOT jurisdictional variation.
  E-12: values span 81.0-1400.0mm across 6 jurisdictions (x17 range) — …
  G-04: values span 4.2-1500.0m² across 5 jurisdictions (x357 range) — …
```

It reaches the same ×27 figure I computed, by a better method, and it names **G-04, which neither
I nor PR #93 found.** Inspecting G-04:

| Jurisdiction | `value_numeric` | `unit` | What the text says |
|---|---|---|---|
| US | 4.2 | m² | "~4.2 m²" ✓ |
| DE | 4.7 / 5.3 | m² | "~4.7 m²" / "~5.3 m²" ✓ |
| AU | 5.0 | m² | "~5.0 m²" ✓ |
| **FR** | **1300.0** | **m²** | "~3.6 m² (**1300**×1300mm + fixtures)" ✗ |
| **GB** | **1500.0** | **m²** | "~4.7 m² (2200×**1500**mm+)" ✗ |

**The defect class is 5 rows across 3 items**, not the 1 that PR #93's W5.1 records or the 2 I
added: E-12 ISO (81 mm from "EN 81-41"), B-10 GB (54 Hz from "EN 54-23"), G-04 FR (1300 m² from a
millimetre dimension), G-04 GB (1500 m² likewise), plus the ordinal-as-quantity rows at E-07.
**The extractor takes a number from anywhere in the text and stamps the column's unit on it.**

**And the fact that matters more than the rows.** The detector is **quarantined** — correctly, on
a real technical ground: *"it is a SURFACING tool… Its exit code carries no verdict. Belongs in a
report, not a gate."* That reasoning is sound. The consequence was not foreseen: **its report is
produced by nothing and read by no one.** Meanwhile `test_jurisdictional_divergence` is a
**registered, active, passing** advisory check in the `tests` battery. **CI runs the test of the
detector. CI does not run the detector.** That is this repository's named failure mode —
a green check that examined nothing — in its purest form yet, and it has been standing since
2026-08-01.

**Other factual claims, re-derived:** `db.py` zero consumers (§1.3) — confirmed against direct
import, `sys.path` manipulation and subprocess; 5 of 76 attestations fail CHECK 3 — confirmed by
running the real function; 66 tables / 18 views / 133 executables — confirmed post-merge.

### 1.2 METHOD — the phase test survived; two proxies did not

**The phase-multiplicity test was validated rather than assumed.** Correlating phase-count
against code-mentions across all 66 tables gives **r = 0.73**, with exactly two disagreements:

- `decisions` — 0 phases, 24 code mentions. Governance infrastructure, outside the content
  pipeline. My ledger already excluded it as infrastructure, so the method and I agreed.
- `weighting_profile` — **3 phases, 0 code mentions, 5 rows.** A table the pipeline anatomy
  assigns to stages 2, 9 and 12 that **no code touches.** The method's one true disagreement
  surfaced a finding I had missed.

A proxy that correlates at 0.73 and whose residual is a finding is a good proxy. It is still a
proxy, and Part 1 of the ledger says so.

**Two of my proxy measurements inflated counts and were caught only by running the real thing:**

| Proxy | Said | Truth | Caught by |
|---|---|---|---|
| regex over `skill-registry.md` for unknown rule ids | **14** | **9** | running `check_3_rule_resolution` — the regex ignored `EXTRA_RULE_IDS`, the allowlist the real check consults |
| regex classifying f-string SQL as value-interpolation | **77 avoidable** | **~0** | reading them — all are `UPDATE {tbl} SET {cols} WHERE id = ?` idioms where identifiers cannot be bound and values still are |

Both would have shipped as findings. The second was security-shaped, which is worse.
**Three times this session a proxy of mine inflated a result.** The pattern is stable enough to
state as a rule: *a measurement that classifies by regex is a candidate list, never a finding.*

### 1.3 LOGIC — the same error twice, and a confound I should name

**Both retracted folds failed identically: structural similarity read as semantic identity.**

- §2.1 — three population-link tables with identical column lists are **not** duplication; they
  are three correctly-keyed tables. Folding them to a polymorphic parent would have traded **three
  enforced foreign keys for one**, because a foreign key can only target one fixed table.
- §2.3 — `case_study_outcomes` is not a duplicate of `case_studies.outcome_data`; it is 1:N
  structured data with a **tier grade per row**. The fold would have destroyed the grading.

The correct rule, which I did not apply until forced: **identical shape is not identical meaning;
check the keys and the cardinality before proposing a merge.**

**A confound in my own headline shared-code argument.** I claimed the enforcement spectrum works
because dimensions with a registered check sit at ~75% compliance and dimensions without one at
~50%. That is a real correlation and it is **not proof of causation**: the dimensions that
received enforcers may be the ones someone already judged important and partly fixed by hand. The
honest form is *consistent with* the spectrum working, and the §1.1 finding is the stronger
evidence anyway — there, an enforcer exists, is not wired, and the defect persisted.

### 1.4 IMPACT — what each finding actually buys, honestly

| Finding | Real impact | Impact I should NOT claim |
|---|---|---|
| 5 false values (§1.1) | Poisons the first determination that reads them; `jurisdictional_values` is the **only** populated quantitative table | Not currently published to any reader |
| Detector quarantined but its test registered | A whole defect class is undetected in CI despite the code existing | It was never *hidden* — the quarantine entry is honest and public |
| Write path unsafe (#93 W1.1–W1.4) | Silently accepts bad rows, silently discards good ones | Nothing has been corrupted yet, because nothing is being written |
| `db.py` zero consumers | One Wave-1 bug is a re-implementation of a correct library function | Style consistency alone buys nothing in a single-author repo |
| Frozen corpus unmarked | A grep for a live question returns 122 files, 39 of them reset-era, and the DB returns 0 rows | No reader has been misled *yet* that anyone has recorded |
| Attestation rule ids | 5 of 76 attestations cite identifiers nothing can resolve | Only 1 of 9 is the skill-registry gap #93 and I both named |

---

## Part 2 — The consolidated register

One namespace. Everything open at `d09f923`, deduplicated across my four documents, PR #93's two,
and the four predecessors. **PR #93's wave structure is adopted**; my IDs map into it.

### Class A — Data correctness (live, wrong, in the canonical DB)

| ID | Finding | Source | Status |
|---|---|---|---|
| **A1** | **Five false numeric values from one systematic extractor failure**: E-12/ISO `81.0 mm` ← "EN 81-41"; B-10/GB `54.0 Hz` ← "EN 54-23"; G-04/FR `1300.0 m²` ← "1300×1300mm"; G-04/GB `1500.0 m²` ← "2200×1500mm"; plus E-07 ordinals (`R9–R13`→9.0, `P3–P5`→3.0) with NULL unit | #93 W5.1 (1 row) · this session (2 more) · **the quarantined detector (all 5)** | **OPEN** |
| **A2** | **The detector for A1 is quarantined while its test is registered and green.** CI runs `test_jurisdictional_divergence`; CI never runs `jurisdictional_divergence.py` | **this review** | **OPEN — new** |
| **A3** | E-12's six values are all *platform-lift* specs under an item named for manoeuvring space — scope ruling needed | #93 W5.2 | OPEN (owner) |
| **A4** | `CORRIDOR-W.md` asserts ≥2440 mm where E-08 asserts ≥1200 mm; four months, neither aware of the other | #93 W5.3 | OPEN (owner) |

### Class B — The write path (PR #93 Wave 1, all independently confirmed)

| ID | Finding | Source |
|---|---|---|
| **B1** | FK check runs after `commit()`; the `except`'s `rollback()` rolls back nothing — a violating migration is committed **and** ledgered | #93 W1.1 = my R-02 |
| **B2** | `"BOOTSTRAP"` appearing in a migration's first 500 bytes downgrades FK violations to a warning | #93 W1.2 = my R-03 |
| **B3** | A failed migration wedges the queue; everything behind it is never attempted | #93 W1.3 = my R-04 |
| **B4** | `next_gap_id` returns `GAP-1` on the empty table; the schema requires `^GAP-\d{3,4}$`, so the only determination writer aborts | #93 W1.4 — **and see D3** |
| **B5** | Three unguarded direct writers, one inside `scripts/migrations/` and able to replay pre-reset state into the canonical DB | my R-01/R-05 |

### Class C — Gates that certify less than they appear to

| ID | Finding | Source |
|---|---|---|
| **C1** | `run_checks.py` has never read the registry's `deps:` field | my R-11 / #93 |
| **C2** | `check-registry.yaml:174` is malformed YAML — two junk keys, truncated description | my R-12 (3 documents, still unfixed) |
| **C3** | `graph_audit.py:277` crashes in the **selftest path only** | my R-13 |
| **C4** | `register_integrity_check --selftest` reports a missed mutation | rem C1 |
| **C5** | 23 of 28 blocking checks declare no vacuity floor; the warrant mechanism exists in `known_debt.yaml` and is not extended to the registry | rem A4 |
| **C6** | Quarantine conflates four dispositions across 3,590 lines — and **A2 shows the cost is not theoretical** | my R-16 |
| **C7** | `--all` totals are not citable; attestation-scoped checks read the changeset | my R-17 |
| **C8** | Blocking reproducibility gate counts 93 of 4,245 rows (2.2%); `jurisdictional_values` — the table in A1 — is not counted | locator-probes §2.1–2.2 |
| **C9** | 5 of 76 attestations cite 9 unresolvable rule ids; **only 1 is a skill**, the other 8 are governance rule names the registry has no place for | my R-24 + #93 W5.4, corrected here |

### Class D — Shared code and re-implementation

| ID | Finding | Source |
|---|---|---|
| **D1** | `scripts/db.py` — 1,889 lines, 43 functions — has **zero** importers, zero subprocess callers | this session |
| **D2** | 4 DB-connection idioms, 4 repo-root idioms, **7 verdict formats** across 133 executables | this session |
| **D3** | **B4 is a re-implementation of `db.py:149`**, which zero-pads and satisfies the schema | this session |
| **D4** | 6 byte-identical function clusters — copy-paste is **not** the problem | this session |

### Class E — Frozen corpus and orientation

| ID | Finding | Source |
|---|---|---|
| **E1** | Three "frozen" registers intersect in one entry; 122 files answer "grab bar", 39 reset-era, DB answers 0 | my R-18 |
| **E2** | `global-reference-registry.{md,json}` declares itself authoritative over the DB; 531 ids, 0 live, 35 never existed, 367 missing | my R-19 |
| **E3** | 70 BPC banners name a superseded event; 16 per-slug files carry none | my R-20 |
| **E4** | CLAUDE.md §10 names a blocking check that does not exist; one dropped capability has no replacement | my R-22 |
| **E5** | 66 workplans, 28,347 lines, no index — now 69 and ~29,000 with this session's | my R-23 / #93 |
| **E6** | Canonical `functional-taxonomy.md` derives its architecture from a document that declares itself not decision-quality | my R-25 |
| **E7** | A ratified derived-value marker (▲/◭/△) with **zero repository presence** | #93 D-B |

### Class F — Consolidation (volume), after two retractions

| ID | Finding | Net |
|---|---|---|
| **F1** | `search_coverage` + `search_languages` are one table on two axes | −1 table |
| **F2** | `situations`, `external_root_registry` never written in either DB; +2 views policing the latter | −2 tables, −2 views |
| **F3** | 16-column locator block written out three times | −32 columns |
| **F4** | `search_executions.admitted_ref_ids` shadows the `search_admissions` junction | −1 shadow store |
| **F5** | One-shot importer layer: 19 scripts, 6,074 lines — retiring it also closes **B5** | −19 executables |
| **F6** | 11 views with no reader need a wire-or-retire ruling; `weighting_profile` is a **table** in the same state (§1.2) | ruling |
| **F7** | ~~4 population-link tables → 1~~ · ~~case-study children → parent~~ | **RETRACTED** (§1.3) |
| **F8** | Skills: **nothing cuttable** on reachability, function-pair overlap, or deprecation hygiene | 0 |

---

## Part 3 — The plan

Organised on the owner's five axes. Every item names its class ID. **PR #93's ordering rule
holds: fix the substrate, then rule on the boundary, then build.**

### 3.0 Do these four first — they are cheap, and A2 changes the priority

| # | Action | Why first |
|---|---|---|
| **P1** | **Wire `jurisdictional_divergence` into CI as an `informational` check** whose output is captured, and file its three `candidate_conflation_or_error` rows as defects (**A2, A1**) | The detector exists and its findings are real. This is the highest value-per-minute item in the whole plan. It does **not** require solving the "surfacing tool vs gate" problem — `informational` is exactly the level the registry already has for a check whose exit code carries no verdict |
| **P2** | **Correct the five A1 rows by migration**, then re-run P1 to confirm the WARN clears | Wrong data in the only populated quantitative table |
| **P3** | **B1–B3**, the write path (four files, no decision) | Everything below writes rows |
| **P4** | **B4 via D3** — replace `assess_cell.py`'s `next_gap_id` with `from db import next_gap_id` rather than zero-padding the copy | Fixes the bug *and* establishes the first library consumer |

### 3.1 Inconsistencies

| Item | Action |
|---|---|
| **C2** | Quote the malformed description. One line. Three documents have now reported it |
| **C7** | Stop citing `--all` totals anywhere; state the battery and the diff instead |
| **E4** | Correct CLAUDE.md §10: name the dispatcher guarantee at `run_checks.py:217-229`, delete the check that does not exist, record the dropped drift-reporting as a known gap |
| **C9** | Decide whether `rules_in_scope` may cite governance rules. If yes, give them stable ids and a home; if no, correct 5 attestations forward-only. **Then** register the 2 missing skills — that is one ninth of the problem, not the problem |
| **E3** | One banner, one wording, one governing DR, on all 85 per-slug BPC files — generated, with a subject-count floor so it cannot pass vacuously |

### 3.2 Injections — four seams, each shipping with its enforcer

**The lever is the check, not the library.** `db.py` proves a shared module without an enforcer
reaches 0% uptake (**D1**). Each seam lands with a registered check that fails a new script
rolling its own.

| Order | Seam | Replaces | Enforcer | Rationale |
|---|---|---|---|---|
| 1 | **id allocators** — `next_gap_id`, `next_con_id`, `next_term_id` | the **D3** class | check: no module defines a `next_*_id` outside `db.py` | This is where a variant becomes a **schema violation**, not a style difference. B4 is the proof |
| 2 | **`connect(readonly=)`** | 4 idioms (**D2**) | extend `db_path_env_audit.py`, which already gets 74% on the env half and 76% on read-only | Prevents a writable handle where read-only was intended |
| 3 | **`report(name, examined, failures)`** | 7 verdict formats (**D2**) | check: every registered check emits `EXAMINED: <n>` | Removes the hazard CLAUDE.md §7 documents as "read the exit code, not the wording", and feeds `run_checks.vacuity_failure()` |
| 4 | **`repo_root()`** | 4 idioms | — | **No correctness argument. Last, or not at all.** Named so it is not smuggled in with the other three |

### 3.3 Centralisation

| Item | Action |
|---|---|
| **E1** | One `governance/frozen-surfaces.yaml`; `.ignore` and `validate_cross_refs.REFERENCE_ONLY` generated from it. Not a fourth register — the two existing lists become derived |
| **C5, C6** | Add `disposition:` (not-a-gate / vacuous / red-with-findings / wrong-venue) to the quarantine schema, and extend `known_debt.yaml`'s proven `warrant:` + `lift_when_sql:` to the check registry. **A2 is the argument**: "not-a-gate" and "not-run" were allowed to mean the same thing |
| **C8** | Widen the blocking reproducibility gate's `COUNT(*)` beyond six tables — pairs with P2, since nothing would currently notice the corrected values regressing |
| **E5** | Generate `workplan/INDEX.md`, date-sorted, with a reset-relative status column and this register's class IDs, registered for freshness like `context_map_fresh` |
| **E7** | Implement the triangle: glyph and fill semantics into `tier-system.md` §5, a `synthesis_method` column, a renderer (#93 W3.1) |

### 3.4 Deduplication

| Item | Action |
|---|---|
| **F3** | One locator representation instead of three copies of a 16-column block |
| **F4** | Drop `admitted_ref_ids`; keep the junction, which has the keys |
| **E2** | Retire `global-reference-registry.{md,json}` to `_archived/` with a redirect stub. **The authority sentences go regardless of where the file lives** |
| **F5** | Retire the one-shot importer layer — 19 scripts, 6,074 lines — which also closes **B5** |
| **D4** | 6 identical function clusters: fold opportunistically when touched. Not worth a dedicated pass |

### 3.5 Consolidation

| Item | Action |
|---|---|
| **F1** | `search_coverage` + `search_languages` → one table with an axis column |
| **F2** | Retire `situations` and `external_root_registry` (+2 views) — D-SCHEMA, owner-gated, **last**: they are the only irreversible items here and the smallest prize |
| **F6** | Wire-or-retire ruling on 11 unread views **and** on `weighting_profile`, a populated table three phases name and no code touches |
| **F7** | **Do not fold.** Both retracted. What remains is a D-SCHEMA decision to split `evidence_population_match.target_population` into a FK'd code column and a note column — which also settles the disagreement with #93's W3.2 |
| **F8** | **Do nothing to the skills.** The volume is not there |

### 3.6 What this plan deliberately does not do

- **No bulk rename** (K3: 278 citing files, 9 immutable migrations, 8 forward-only attestations).
- **No deletion of a quarantined script** — `tooling-register.md` §6.5 makes quarantine-with-reason
  terminal. **A2 argues for changing what quarantine *means*, not for emptying the list.**
- **No check promotion in the same window as branch protection** (K4, §6 item 6).
- **No fourth register.** Every centralisation item above collapses existing registers or extends
  an existing mechanism.

---

## Part 4 — Limits of this document

- **A2 is one session's reading of one quarantine entry.** The entry's technical reasoning is
  sound; my claim is that `informational` was available and unused. Someone should check whether
  that was considered and rejected before treating P1 as obvious.
- **Class B is carried from PR #93** with code-level confirmation of B1–B3 but no re-execution of
  its trial. B4 I confirmed by reading both implementations.
- **C8 is carried from the locator-probes document** on its demonstration, not re-run.
- **The register is deduplicated by my reading**, not mechanically. Two documents describing one
  defect in different vocabulary may still appear twice.
- **Five of the ten source documents were written by other sessions.** Where I record agreement,
  that is agreement between readings, not independent replication — except where a command is
  quoted, which is the standard this repository already sets.

*Every measurement re-derived on 2026-08-11 against `d09f923`. Where a claim has no command
behind it, Part 4 says so. Three proxy measurements of mine inflated results this session and
were caught by running the real thing — re-derive before acting on any row.*

---

## Part 5 — Net accounting: lines and files

*Added against the owner's standing constraint — fewer lines and fewer files is better, with
centralisation exempted where consistency requires it. The measurement changes which items are
worth doing, and it makes one either/or unavoidable.*

**Baseline:** 133 executables · **40,171 lines** · 66 tables · 18 views.

### 5.1 Injection does not buy lines. Say so plainly.

The three injectable idiom families total **492 lines — 1% of all script code**:

| Family | Lines | Files |
|---|---|---|
| DB path + connect boilerplate | 271 | 82 |
| repo-root resolution | 155 | 107 |
| verdict printing | 66 | 36 |

Replacing them with library calls removes perhaps 350 lines net. **That is noise against 40,171.**
Injection is a **consistency** measure, exactly as the owner framed it, and it should be argued
for on the two correctness grounds this review established — the B4/D3 schema violation, and the
read-only handle — never on volume. Anyone who justifies it by line count is selling it wrong.

### 5.2 The caveat does not apply here: injection adds **zero** files

The owner's exemption anticipates centralisation increasing file count. In this repository it
does not. **`db.py` already exists, already provides `connect()`, `now()`, `next_gap_id()`,
`insert_gap()`, `log_search()` and 38 more — and has zero importers.** All four seams in §3.2
belong in that file. The cost was paid in April; nothing has drawn on it since.

### 5.3 The either/or this forces

`scripts/db.py` is **1,889 lines with no consumers** — the single largest inert file in the
codebase. It has exactly two honest futures:

- **Adopt it.** Execute §3.2, starting with P4, which makes `assess_cell.py` its first importer
  and fixes a Wave-1 bug in the same edit. Every seam thereafter is an import, not a new file.
- **Delete it.** If the seams are not going to be wired, 1,889 lines are being carried, read past,
  and maintained for nothing — and CLAUDE.md §4 describes it to every new session as "the
  read/query workhorse," which is false and costs orientation time.

**What it cannot do is stay as it is.** This is the clearest instance in the repository of the
pattern this review keeps finding: *the capability exists, the wiring does not, and the
documentation describes the capability.* It is the same shape as A2 (a detector that runs
nothing), C1 (`deps:` declared and never read), and E7 (a ratified marker with no implementation).

### 5.4 Where the volume actually is

| Action | Files | Lines | Reversible? |
|---|---|---|---|
| **F5** retire the one-shot importer layer | **−18** | **−5,850** | yes — `_archived/`, and it closes **B5** |
| §3.2 injection (all four seams) | **0** | ~−350 | yes |
| **F2** cut 2 tables + 2 views | — | — | **no** — owner-gated, last |
| **F1** fold two coverage tables | — | — | yes, DDL only |
| **F3** one locator block instead of three | — | −32 columns | yes |
| `db.py` if §3.2 is rejected | −1 | −1,889 | yes |

**Net if the plan runs: 133 → 115 executables, ~40,171 → ~34,000 lines (−15%), 66 → 63 tables,
18 → 16 views.** One action — F5 — delivers **94% of the line reduction**, and it is the same
action that closes the unguarded-writer finding. If only one thing is done for volume, it is
that one.

**What is deliberately not cut:** the 16 quarantined scripts (3,590 lines). `tooling-register.md`
§6.5 makes quarantine-with-reason terminal, and **A2 has just demonstrated why the list has
value** — the detector that names five bad rows is on it. The fix is to make quarantine mean
something more precise (§3.3, C6), not to empty it.
