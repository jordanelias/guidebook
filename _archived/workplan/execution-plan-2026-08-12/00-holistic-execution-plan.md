# 00 — The holistic execution plan

**The connective document.** It runs in tandem with the twelve per-wave documents in this
directory and is the only one that should be read before every session. The per-wave documents
say *how* to execute an item; this one says *what may execute at all right now*, *in what
order*, and *what must be true before it does*.

**Status:** PROPOSED. Nothing in this directory has been executed. Owner-gated items are marked
and must not be executed on a session's own authority.

**Subject:** `fd4c09d` (the PR #95 merge). **Doctrine SHA:** derive with
`git rev-parse HEAD:governance/mission-and-epistemics.md | cut -c1-7` — deliberately not
hardcoded here.

**Source:** `workplan/2026-08-12-resolution-plan.md` revision 4, decomposed into executable
steps. The resolution plan remains the authority on *why*; this set is the authority on *how*.
Where a per-wave document contradicts the resolution plan, the per-wave document states the
re-derived evidence and wins — that is the point of the decomposition.

---

## 1. How to use this document set

| Document | Wave | Executes when |
|---|---|---|
| `00-holistic-execution-plan.md` | — | always read first |
| `L-execution-ledger.md` | **L** | **first — gates everything, including H** |
| `H-hard-coding-remediation.md` | **H** | after L1; owner has already ruled |
| `0-detector-activation.md` | 0 | after L1 |
| `1-write-path-and-bootstrap.md` | 1 | after L1 |
| `2-rulings.md` | 2 | owner decisions; gate Waves 3 and 4 |
| `3-schema-while-free.md` | 3 | after Wave 1; before any content |
| `4-adjudication-apparatus.md` | 4 | after D-A rules |
| `5-corpus-defects.md` | 5 | W5.1 only with W5.6, only after W9.1 |
| `6-method-rules.md` | 6 | any time after L1 |
| `7-consolidation.md` | 7 | W7.12 only after all of Wave 8 |
| `8-document-hygiene.md` | 8 | W8.7 immediately; rest before W7.12 |
| `9-dropped-inheritance.md` | 9 | W9.1 is on the critical path |

**The reading contract.** Every per-wave document carries, per item: Objective · Preconditions
and gates · Ordered steps · Caller sweep · Verification · Falsifier · Re-derivation notes. **The
Falsifier is not decoration** — if the observation it names is true when you look, the item does
not execute, and that is a finding to record in the ledger, not a blocker to work around.

---

## 2. The fact base, re-derived at `fd4c09d`

Revision 4's own governing rule is *re-derive facts, not only arithmetic* (W6.11). This
decomposition re-ran them again. What follows is what was observed, not what was inherited.

### 2.1 Confirmed

| Claim | Status |
|---|---|
| 28 of 93 `items.name` carry a numeric determination | **CONFIRMED** — list at `H-hard-coding-remediation.md` |
| `items.name` is not a key; all 14 inbound FKs target `item_code` | **CONFIRMED** |
| `specifications` = 0 rows; `evidence_sources` = 0 rows | **CONFIRMED** |
| Emitted migration bodies self-commit (`emit_data_migration.py:201`) | **CONFIRMED** — so W1.1's four-line reorder cannot work |
| FK check runs *after* `commit()` | **CONFIRMED** at `migrate_db.py:162 / :171 / :174` |
| `is_bootstrap` substring test exists twice | **CONFIRMED** at `:176` and `:261` |
| `MIGRATIONS_DIR.glob("*.sql")` is non-recursive | **CONFIRMED** at `:81`, `:95`, `:114` |
| `db.py:next_gap_id()` takes no `conn`; `assess_cell.py` refuses the canonical DB | **CONFIRMED** at `db.py:149-158`, `assess_cell.py:487/:492` |
| `assess_cell.py` writes `None, None, None` for the value triple | **CONFIRMED** at `:559`, columns at `:567` |
| `grep -c deps scripts/run_checks.py` → 0 | **CONFIRMED** |
| `check-registry.yaml:174` parses to a wrong shape | **CONFIRMED** — `governance` battery yields keys `{deps, description, 'adversarial-use.', 'doctrine recheck'}` |
| Quarantine holds 15 `quarantined` + 1 `vacuous` | **CONFIRMED** — 16 entries, 65 checks |
| `validate_conflicts` is quarantined | **CONFIRMED** |
| The value detector is blind to NULL-unit rows | **CONFIRMED** — neither E-07 nor E-15 appears in its output |
| `scripts/db.py` = 1,889 lines, 43 functions, no real importers | **CONFIRMED** |
| One-shot layer = 6,074 lines | **CONFIRMED** |
| 23 `data_migrations` ids correspond to no file | **CONFIRMED** — 314 ledger vs 292 files |
| The archive tag was never created | **CONFIRMED** — only `phase-a-complete-20260419` exists; the branch does exist at `4fc6304` |
| `RR-` is free repo-wide | **CONFIRMED** |

### 2.2 Corrected or newly found

These change what executes. Each is carried into its per-wave document.

**The seven that change a wave's scope or premise:**

| # | Finding | Consequence |
|---|---|---|
| 1 | **W5.1 is NINE rows across SIX items, not eight across five.** `jv 52` (E-03/NO, `1.0 ratio` from the "1" in "1:12"; siblings encode it as 8.3) | A sixth shadow YAML (`a-1_e03.yaml`). And it **evades both detector blind spots** — it has a unit, and its ×8.3 spread sits below the ×10 conflation threshold. **W0.3 does not close this class** |
| 2 | **H3 is a FOUR-class partition, not two** — 5 (a), 17 (b), **4 (n)** standard/metric designations, 2 mixed. No class (c) is currently possible | The migration comment must not claim a two-way split. And **7 names carry multiple numbers — ~35 determinations, not 28** |
| 3 | **W9.1's gate goes red IMMEDIATELY, not at the next cron** — 5 committed rows vs 0 rebuilt | Sharpens the critical path: W9.1 is not a precaution, it is a prerequisite |
| 4 | **W7.4's DELETE branch sweeps ~29 live files (26 of them `skills/*_SKILL.md`), not 12** | Materially strengthens ADOPT. The plan's sweep would have left ~17 files instructing sessions to run a deleted tool |
| 5 | **W7.9 breaks three views, not one** — `v_value_independence`, `v_registry_duplicate_descriptions`, **`v_unregistered_roots`** (named in no document) | The under-sweep is itself the finding |
| 6 | **There is no `sessions` table** in the database | Wave L's "joins to `sessions`" is impossible as an FK — TEXT plus a check |
| 7 | **Wave L's write-path tension is unresolved by the plan** — entries are written *before* the change, but migrations are immutable | Needs an owner ruling before L1 lands. Three options in `L-execution-ledger.md` |

**And the counts that moved:**

- **W7.1 retires 20 files / 7,086 lines**, not 19 / 6,074 — the JSON dump is real weight.
- **H2's "23 condition clauses" is unreproducible** — no criterion is stated; ~31 by enumeration.
  Pin the criterion before cutting the migration.
- **W7.6's "367 missing" is not reproducible from any surface examined. Do not propagate it.**
- **W9.2's "12 compounds" re-derives as 8**, and the figures describe the *archived*
  `evidence_sources`, not any live table.
- **Migration 053's header is not merely wrong, it is inverted**: "85 rows cite one level" is
  actually the count of rows with **no** locator (24 of 109 carry a `§`).
- **`validate_reasoning` is 15 findings, not ~14**; `validate_pydantic_schemas` is 246, and the
  registry's "236" is stale.

**Three sequencing dependencies no prior document states:**

1. **W7.7's audit rewrite must follow W7.3-G1** — the banner audit reads `bpc_metadata`.
2. **W7.3-G5's ruling should precede W7.4** — the `FrozenGridError` guard lives *in* `db.py`.
3. **W9.5 depends on W7.4-ADOPT** — `db.py log-search` is the admission discipline a PMP walk
   needs.

**And two more items of live scope:**

1. **`items.E-15`'s name is truncated in the data** — `Changing Places Facility
   (Height-Adjustable Bench, Overhead`, an unclosed parenthesis, the only unbalanced name in the
   table. **Recorded in no prior document.** Folded into Wave H's migration.
2. **The value detector reports 26 findings, not none.** The resolution plan's W0.1 falsifier —
   *"its output appears in CI and names no defect"* — is far too weak. At HEAD it names 2
   within-jurisdiction contradictions, 3 conflation candidates, 9 cross-jurisdiction divergences
   and 12 unadjudicated items. The correct statement is that it names 26 findings **and cannot
   name the 8 that matter most**, because its own row filter excludes them.
3. **Four of the eight NULL-unit rows are genuine dimensionless quantities** (jv14 DCOF 0.42,
   jv15 PTV 36, jv96 and jv100 occupant/seat thresholds of 50). Only four are non-quantities
   (jv16 R-class, jv17 P-class, jv106 a year, jv107 an edition ordinal). **W5.1 and W0.3 must
   distinguish these** — a blanket "NULL unit is a defect" rule would corrupt four correct rows.
4. **`requirements.txt` pins `PyYAML==6.0.3`, not 6.0.1.** W1.5's quoted error message is stale;
   whether the failure still reproduces must be re-tested before the fix is written.
5. **`workplan/` is 75 files / 32,411 lines**, not 74 / 31,338 — and this decomposition is
   itself part of why. A live instance of AC-11: the count went stale during authorship.
6. **`site/rooms/` cannot be regenerated at all** — `room_page.py` reads six relations absent
   from the live schema. This **blocks Wave H's mechanism as written**; the 9 stale pages need an
   owner disposition.
7. **`jurisdictional_values` has zero locator adoption** — `locator_scheme` and all 16 `loc_*`
   columns are NULL on all 109 rows; locators live in free-text `source_section`. Migration
   053's hierarchy is unenforced *and* unused, which strengthens W3.9's case and weakens any
   claim that the locator work is partly done.
8. **Three populations (`MOVE`, `ID`, `TALL`) have zero `item_population_links`**, and 14 of the
   29 `population_reclass` codes do not exist in `populations`. Neither is in any wave.

### 2.3 Not re-derived — carried on the plan's authority

Per Appendix D, and extended here. **Do not treat these as verified:**

- `validate_pydantic_schemas`' 246 findings / 49 unmapped tables.
- Branch-protection *configuration* (only the boolean is readable from a session).
- The ~30-of-70 vacuous-assertion estimate in `test_db_integrity`.
- The archived-DB row counts behind W7.3 and W3.2.
- Every text-vs-standard reading in W5.1 — these are readings of `value_text`, not of BS 8300
  or DIN 51130. Verifying them against the standards is Phase-B work, not this plan's.

---

## 3. The critical path

```
  L1  work_log record shape + migration
   │   (nothing else executes until this exists)
   ├──────────────┬────────────────┬──────────────────┐
   ▼              ▼                ▼                  ▼
  H3            W8.7            W0.3 ──▶ W0.1       W1.1+W1.2+W1.3
  classify      7 headers       unblind   wire      (ONE edit, 35 lines)
  before        (minutes)       detector            │
  renaming                          │               ▼
   │                                │             W1.4 ──▶ W1.5, W1.6
   ▼                                ▼
  H1/H2/H4/H5   W8.1-W8.3      W9.1 ──▶ W5.6 ──▶ W5.1
  rename        port            exempt   widen     correct 8 rows
   │             │              DR       gate      (must ship together)
   ▼             ▼
  W5.2         W8.4-W8.6 ──▶ W7.13 ──▶ W7.12
  (E-12)                              (retire — LAST)

  D-A ──▶ W3 (free while empty) ──▶ W4
  D-B ──▶ W3.1 ──▶ W3.6
  D-C ──▶ configuration audit only (premise dead)
  W9.2 (frame vocabularies) — Wave 3 class, cheapest now
```

**Five ordering rules that must not be violated:**

1. **L1 before everything.** Including Wave H. The plan's entire failure history is changes that
   recorded themselves and not their consequences; building the ledger after the first execution
   makes the first execution the one thing never logged.
2. **H3 before H1.** Classify all 28 values as "already held in `jurisdictional_values`" versus
   "held nowhere else" *before* any rename. It is a read-only query and it is the difference
   between a rename and a data loss.
3. **W9.1 before W5.6, and W5.6 with W5.1.** Widening the reproducibility gate without the
   `url_verification_runs` exemption manufactures a permanently-red blocking check the next time
   the bi-weekly cron runs. Correcting the eight values without widening the gate leaves the
   corrected table outside the comparison that would protect it.
4. **W0.3 before W0.1.** Wiring a detector whose row filter is anti-correlated with its own
   defect class produces a green that means nothing.
5. **All of Wave 8 before W7.12.** Retiring documents before porting their unique content is the
   one ordering that reproduces the defect Wave 8 exists to fix.

---

## 4. Owner gates — the complete inventory

**Nothing in this column executes on a session's authority.** DG-NON means *propose, do not
decide*. Per `CLAUDE.md` §5 and §9 guardrail 4, file moves, retirements, `.ignore` scope changes
and all DG-NON classes need owner sign-off.

| Item | Class | What is being asked |
|---|---|---|
| **Wave H** | DG-NON | **Already ruled 2026-08-11** — strip determinations from item names. Execution shape only remains. |
| H2 | DG-NON | Whether scope clauses are part of a parameter's identity |
| H4 | — | Whether standard designations (`ISO 23599:2019`) stay in names |
| H6 | DG-NON | `rooms`: register as frame, or reset |
| D-A | D-METH | Is value determination a machine stage or a human one? |
| D-B | D-METH | Does a derived marker inherit its input's strength, or cap one band below? |
| D-C | D-OP | Branch-protection *configuration* audit (the switch is already on) |
| W3.7 | — | The 16 `typical_stakes` grades are judgment acts |
| W5.2 | — | Does E-12 cover lifts? |
| W5.5 | D-DOCT | Retiring `weighting_profile` amends `evidence-architecture.md` I3 |
| W5.8 | — | Does `schemas/*.py` mirror SQLite or the YAML layer? |
| W7.1, W7.5, W7.6, W7.7, W7.9, W7.11, W7.12 | — | Retirements and `.ignore` scope |
| W7.4 | — | ADOPT or DELETE `db.py` (recommend ADOPT) |
| W9.1 | D-OP | Extend the migration exemption to `url_verification_runs` |
| W9.3(5) | — | `CHECK` on `verification_status` — register D4 already ruled DEFER |
| W9.6 | — | Create the archive tag; protect the archive branch |

**Nineteen gates.** A session that finds itself about to execute one has misread this document.

---

## 5. The working protocol for every session in this plan

1. **Write the ledger entry first.** Six mandatory blocks, five standing interrogations. An
   entry authored afterwards records what a session remembers; an entry authored before records
   what it intended, and the delta is the finding.
2. **Re-derive before acting.** Every count in this directory is volatile and several were
   already stale when written. Run the command beside the claim.
3. **Migrations only.** Never hand-edit `data/guidebook.db`. `emit_data_migration.py` →
   `migrate_db.py`. Data migrations are append-only and immutable once committed — fix forward.
4. **Check that a check had a subject.** A gate reporting zero may have examined zero. This
   repository has produced that failure four times and it looks exactly like success.
5. **Search for an existing tool before building one.** W6.7; the repository has paid twice.
6. **A rename is not done until the caller sweep is done** — enumerated, not counted.
7. **Commit format:** `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last.
   `workplan/` is **not** a synthesis path, so no doctrine token and no attestation are owed for
   documents in this directory. **The trap:** a commit that also touches `sessions/LATEST` *is* a
   synthesis path — keep the pointer update in its own commit with the token.

---

## 6. What to do first, concretely

**In one session, in this order:**

1. **L1** — the `work_log` schema migration and the record shape. (`L-execution-ledger.md`)
2. **H3** — the read-only (a)/(b) classification of all 28 values. Minutes, and it is the
   precondition for the rename. (`H-hard-coding-remediation.md`)
3. **W8.7** — seven one-line supersession headers. Minutes, and it stops the repository lying to
   its next session. (`8-document-hygiene.md`)
4. **W0.3 then W0.1** — unblind the detector, then wire it. (`0-detector-activation.md`)
5. **W1.1+W1.2+W1.3 as one edit** — the scratch-snapshot write path.
   (`1-write-path-and-bootstrap.md`)

**Then, before any content work at all:** Wave 3, because every table it changes is empty today
and expensive after the first content batch — and W9.2, the two frame vocabularies the reset DR
requires, for the same reason.

---

## 7. What this plan does not do

- It does not resume research. Every wave is substrate, ruling, or hygiene.
- It does not populate a single evidence cell. The pipeline stays empty until the write path is
  safe (Wave 1), the boundary is ruled (Wave 2) and the schema is settled (Wave 3).
- It does not decide any DG-NON question. It states each one with its evidence and stops.
- **It does not verify a single quantitative claim against a standard.** W5.1's corrections are
  readings of `value_text`. Nothing here admits evidence.

---

*Decomposed 2026-08-12 against `fd4c09d`. Every count re-derived at that commit and volatile by
construction. The per-wave documents carry the detail; this one carries the order. Re-derive
before acting.*
