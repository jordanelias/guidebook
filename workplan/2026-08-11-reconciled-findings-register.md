# 2026-08-11 — Reconciled findings register

**Status:** REGISTER — the single reconciled list of open findings. Nothing here is executed.
This document does not add findings for their own sake; it merges six overlapping sources into
one, deduplicates them, adjudicates where they contradict each other, and **re-derives every
status against `3eed5d4` rather than trusting the status the source recorded.**
**Supersedes, for the purpose of "what is open":** the finding registers inside the six
documents listed in §0.2. It does not supersede those documents — their reasoning, method and
evidence stay where they are, and this register cites into them.
**Doctrine SHA:** `0f2f525`. **Environment:** `pydantic==2.13.3`, `PyYAML`, `jsonschema` present.

> **The reconciliation is not clerical.** It refuted one source claim outright and demoted the
> item that claim was the reason to prioritise (§2.1); found the "fix this first" item still
> live at a path no source recorded correctly, inside the migrations directory itself (R-01);
> and produced three findings no single source held — including a **safety-relevant false value
> in the live database** (R-07) that the method which found its sibling would have found too,
> had anyone run that method twice. It also nearly dropped a BLOCKER by matching on ID format
> (§6, R-17b).

---

## Part 0 — What was merged, and the problem that made merging necessary

### 0.1 Sources

| Document | Lines | Findings it carries |
|---|---|---|
| `workplan/2026-08-11-remediation-and-pipeline-anatomy.md` | 6,775 | A1–A4, B1–B4, C1–C13, D1–D11, K1–K11 |
| `workplan/2026-08-12-pipeline-walk-trial-log.md` | 3,875 | the four write-path breaks, the trial's IO log |
| `workplan/2026-08-12-commit-91-adversarial-review.md` | 974 | F1–F13, M1–M5, and its own corrections |
| `references/tooling-register.md` | 627 | F1–F12 (a *different* F-series), §4 red gates, §6 proposals |
| `workplan/2026-08-11-consolidation-sweep-and-adversarial-pass.md` | 499 | §1.1–§1.9, X1–X4 |
| `workplan/2026-08-09-locator-hierarchy-and-enforcement-probes.md` | 415 | C1–C17, D1–D7 (a *third* C-series) |
| `workplan/2026-08-12-pipeline-phase-state-map.md` | 360 | per-stage state, no independent findings |
| **Total** | **13,525** | |

### 0.2 The namespace collision — why "fix C4" was ambiguous

Four documents use overlapping single-letter ID schemes for unrelated findings:

| ID | In the remediation register | In the commit-91 review | In the locator probes | In `tooling-register` |
|---|---|---|---|---|
| `C1` | `register_integrity_check` selftest misses a mutation | a corridor-width trial claim | a locator-hierarchy finding | — |
| `C4` | the only reasoning doc fails every requirement | (different) | (different) | — |
| `D2` | migration exemption list | (different) | (different) | — |
| `F6` | — | malformed `governance` battery YAML | — | a tooling assessment item |
| `F9` | — | three unguarded direct writers | — | (different) |

**A handoff line saying "C4 is open" does not identify a finding.** This register therefore
assigns one namespace, `R-NN`, and every entry carries its source IDs so the trail back is
exact. That is the reconciliation's first deliverable, ahead of any individual fix.

### 0.3 Method

For each merged entry: (a) collapse the duplicate statements into one; (b) **re-run the
evidence command at `3eed5d4`**; (c) record `CONFIRMED-LIVE`, `RESOLVED`, `REFUTED`, or
`CHANGED` against what the source said; (d) where sources disagree, adjudicate in §2 with a
test rather than a preference.

Status counts below: **28 entries — 24 CONFIRMED-LIVE, 1 REFUTED consequence-clause, 3 NEW.**
One entry (R-21) is carried unverified and one (R-26/R-27) is a merged class, both flagged in §6.

---

## Part 1 — The register

Levels: **BLOCKER** (must precede other work) · **DEFECT** (wrong behaviour or wrong text) ·
**BACKLOG** (real, large, needs a ruling) · **DECISION** (owner-only).

### Class 1 — The write path (highest consequence: these corrupt or lose data)

| ID | Finding | Sources | Status at `3eed5d4` | Level |
|---|---|---|---|---|
| **R-01** | **An unguarded replay script can silently undo the clean-room reset.** `scripts/migrations/session_2026_05_11g_replay.py` — 224 lines, the **only `.py` file among the 347 files in the canonical migrations directory** — reads a JSON dump of pre-reset DB state and applies it to `data/guidebook.db`. It does not import `_legacy_guard`; seven of its nine siblings do. | rem C12 ("fix this first"), c91 F9 | **CONFIRMED-LIVE.** Note the source path was recorded as `scripts/migrate/…`; it is `scripts/migrations/…`, which is *worse* — that directory is the reviewable migration history. | BLOCKER |
| **R-02** | **A migration that violates a foreign key is committed and ledgered, then reported as an error.** `migrate_db.py:161-183`: `conn.commit()` and the `data_migrations` INSERT both execute *before* the FK comparison; the `except` handler's `conn.rollback()` therefore rolls back nothing. | c91 break 1 | **CONFIRMED-LIVE** by code reading at the cited lines | BLOCKER |
| **R-03** | **The word "bootstrap" anywhere in a migration's first 500 bytes downgrades new FK violations from error to warning.** `is_bootstrap = "BOOTSTRAP" in body[:500]…upper()`. FK enforcement is disabled for *every* migration (`PRAGMA foreign_keys = OFF`, unconditional); the flag decides only whether violations raise. | c91 break 2 | **CONFIRMED-LIVE** | DEFECT |
| **R-04** | **A failed migration wedges the queue permanently** — the raise propagates, every migration behind it is never attempted, and the documented remedy cannot run. | c91 break 3 | **CONFIRMED-LIVE** | DEFECT |
| **R-05** | **Two further legacy writers are unguarded:** `scripts/migrate/init_database.py`, `scripts/migrate/phase_jv_appendix_a.py`. | c91 F9 | **CONFIRMED-LIVE** (2 of the 3 named; the third is R-01) | DEFECT |

### Class 2 — False values in the live database

| ID | Finding | Sources | Status | Level |
|---|---|---|---|---|
| **R-06** | **A standard's designation was parsed into a measurement.** `jurisdictional_values`: E-12, ISO 21542:2021 — `value_numeric = 81.0`, `unit = 'mm'`, from a `value_text` that reads only *"Min. Platform (W×D): References EN 81-41; Notes: Defers to regional standards"* — i.e. **no numeric value at all**. The 81 came from "EN 81-41". | c91 (its own new finding) | **CONFIRMED-LIVE** — still present, still labelled mm | DEFECT |
| **R-07** | **NEW — a second instance of the same class, and this one is safety-relevant.** B-10, "BS 5839-1 / EN 54-23" — `value_numeric = 54.0`, `unit = 'Hz'`, from `value_text` *"Flash Rate: Per EN 54-23"*, which again states no rate. The **54 came from "EN 54-23"**. The two sibling rows for the same parameter record **≤2 Hz** with the note *"Seizure Consideration: Yes — ≤2 Hz limit"*. The database therefore asserts a visual-alarm flash rate **27× the photosensitive-epilepsy ceiling** its own neighbouring rows record. | **this reconciliation** | **NEW / CONFIRMED-LIVE** | BLOCKER |
| **R-08** | **NEW — class ordinals stored as quantities with no unit.** E-07 / DIN 51130 → `9.0`, `unit` NULL, from *"Threshold: R9–R13"* (a slip-resistance **class**, not a measurement). E-07 / AS 4586 → `3.0`, NULL, from *"P3–P5"*. 8 of the 75 rows carrying `value_numeric` have a NULL `unit`. | **this reconciliation** | **NEW / CONFIRMED-LIVE** | DEFECT |

> **What R-06 to R-08 mean together.** The commit-91 review found R-06 "in seconds by putting
> three category-E items side by side, which is the one comparison nothing in the repository
> performs." It then stopped at one. Running the same comparison across the other 74 numeric
> rows — twenty minutes of work — yields R-07 and R-08. **The finding is not three bad rows; it
> is that a method known to work was run once.** `jurisdictional_values` survived the reset
> explicitly (DR-2026-08-06 §3) as correctly-cited code values, and it is the *only* populated
> quantitative table, so it is the sole numeric substrate any future determination will rest on.
> A systematic value-vs-text audit of all 75 rows belongs ahead of content, not after it.
>
> **And it compounds with R-17b, which no source connected to it.** The blocking reproducibility
> gate counts rows in six tables; `jurisdictional_values` is not one of them. So the table
> holding the three false values is a table where a correction, a regression, or a wholesale
> `DELETE` of all 109 rows all produce the same verdict: `PASS`. Fixing R-06–R-08 without
> R-17b leaves no mechanism that would notice them coming back.

### Class 3 — The apparatus's own footing

| ID | Finding | Sources | Status | Level |
|---|---|---|---|---|
| **R-09** | **The documented setup command fails.** `pip install -r requirements.txt` → `ERROR: Cannot uninstall PyYAML 6.0.1, RECORD file not found` (Debian-managed PyYAML vs the `==6.0.3` pin). CLAUDE.md §7 gives this as step one. Reproduced in two independent containers. | rem A1, c91 F10, sweep §1.8b | **CONFIRMED-LIVE** | BLOCKER |
| **R-10** | **`requirements.txt` states something false about itself** — *"All scripts … depend only on these two"* — while `scripts/audit/adherence_log_audit.py` imports `jsonschema`, which `ci.yml` hand-installs in two jobs. | rem A2, sweep §1.8b | **CONFIRMED-LIVE** (the A2 *consequence* clause is refuted — §2.1) | DEFECT |
| **R-11** | **Missing dependencies present as five blocking failures.** Without pydantic: `BLOCKING failures (5)`, all `ModuleNotFoundError`. A session that does not read tracebacks concludes the repo is broken. The registry already declares per-battery `deps:`; `run_checks.py` has never read the field. | rem A3, c91 F5 | **CONFIRMED-LIVE** — `grep -n deps scripts/run_checks.py` → nothing | DEFECT |
| **R-12** | **`governance/check-registry.yaml:174` is malformed YAML.** Unquoted commas in a flow mapping parse to `{'description': 'Decision protocol', 'doctrine recheck': None, 'adversarial-use.': None}` — two junk keys, description truncated to a third. `check_yaml` passes because it is *valid* YAML. | rem A3, c91 F6, sweep §1.8a | **CONFIRMED-LIVE** — three documents, one unfixed line, 14 edits to that file this week | DEFECT |

### Class 4 — Gates that certify less than they appear to

| ID | Finding | Sources | Status | Level |
|---|---|---|---|---|
| **R-13** | **`graph_audit.py:277` crashes on an empty `connections` table** — `SELECT con_id … LIMIT 1` → `TypeError: 'NoneType' object is not subscriptable`. A crash hides every assertion behind it. | rem B2 (highest in Class B), c91 F7 | **CONFIRMED-LIVE, refined:** the crash is in the **`selftest` path only**. `graph_audit.py` plain exits 0; `test_graph_audit.py` exits 1. Both source documents state it unqualified. | DEFECT |
| **R-14** | **`register_integrity_check --selftest` reports a missed mutation** — *"COMPLETENESS: a whole cell section deleted"* goes undetected; the harness prints `SELFTEST FAILED`. | rem C1 | **CONFIRMED-LIVE** | DEFECT |
| **R-15** | **Vacuity floors need a warrant, not a blanket.** 23 of 28 blocking checks declare no `min_items`; a blanket floor makes gates red for telling the truth (the repo adjudicated and retired exactly that on 2026-08-06). The proven mechanism already exists — `scripts/audit/graph/known_debt.yaml`'s `warrant:` + `lift_when_sql:`, which re-reports a stale suppression rather than hiding a regression. | rem A4 (supersedes K1, K10) | **CONFIRMED-LIVE — and everything in §4 sequencing depends on it** | BLOCKER |
| **R-16** | **The quarantine list conflates four dispositions under one word** — not-a-gate (4), green-but-vacuous (5), red-with-real-findings (6), wrong-venue (1) — across 3,590 lines of never-run code. `validate_temporal` reads `data/temporal/`, **a directory that has never existed**. | sweep §1.6 | **CONFIRMED-LIVE** | BACKLOG |
| **R-17** | **A check's `--all` result is not citable.** The same `run_checks.py --all` returned `55 green / 10 advisory` and `56 green / 9 advisory` in one session, differing only by what the last commit touched — attestation-scoped checks read the git changeset. The commit-91 review's F12 flagged a version of this; the cause is now identified. | c91 F12, sweep A11 | **CONFIRMED-LIVE** — do not write either number down | DEFECT |
| **R-17b** | **The blocking reproducibility gate watches 2.2% of the database and affirms the rest as reproducible.** `migration_reproducibility` compares `PRAGMA user_version` plus `COUNT(*)` on six tables — **93 of 4,245 rows**, all of it `items`; the other five are empty post-reset. A tampered *committed* migration appending `UPDATE slugs SET status='STUB' WHERE status='ACTIVE'` rewrote 80 of 106 rows and the gate printed `PASS: the committed DB matches what the migration history produces.` Only count-preserving writes are invisible — but `DELETE FROM jurisdictional_values`, all 109 rows, also passes at exit 0. | **locator-probes §2.1–2.2** | **CONFIRMED-LIVE** — carried on that document's demonstration, which reached it by a new vector (tampering committed history) after three probes failed for the wrong reasons | BLOCKER |

### Class 5 — The frozen corpus (unique to the consolidation sweep)

| ID | Finding | Sources | Status | Level |
|---|---|---|---|---|
| **R-18** | **"Frozen" is expressed in three registers whose two operative lists intersect in one entry** (`_archived/`). `.ignore`'s own rationale — *a hit from a frozen record answers a current question wrongly* — describes `references/bpc/` by its own terms, and `references/bpc/` is not covered. `rg -l "grab bar"` → 122 files (39 frozen-reference, 74 in no register); the DB returns 0 rows. | sweep §1.1 | **CONFIRMED-LIVE** | DECISION |
| **R-19** | **A rival source of truth.** `references/global-reference-registry.{md,json}` line 601: *"This registry is the single source of truth. If a BPC Key sources table and this registry conflict, the registry governs."* 531 REF-IDs, dual-stored, **0 live**, 35 that never existed in the DB even pre-reset, 367 pre-reset sources missing from it. | sweep §1.2 | **CONFIRMED-LIVE** | DECISION |
| **R-20** | **Retraction banners name a superseded event; 16 files carry none.** 70 of 102 BPC files banner DR-2026-05-23 ("retracted pending reverification" — reads as recoverable); DR-2026-08-06 made the corpus reference. 16 of the 85 per-slug files carry no marking, including the slug `sessions/LATEST-RESEARCH` points at. 176 cited REF-IDs resolve only in the archived pre-reset DB. | sweep §1.3 | **CONFIRMED-LIVE** | DECISION |
| **R-21** | **The renderer makes evidence-thin populations disappear** — a doctrinal breach in shipped code, not a display bug. | rem §1.0h | **CARRIED** — not independently re-derived here; flagged as the one Class-5 entry this register did not re-verify | DECISION |

### Class 6 — Orientation documents that misdescribe the repository

| ID | Finding | Sources | Status | Level |
|---|---|---|---|---|
| **R-22** | **Three orientation documents describe a check that does not exist.** CLAUDE.md §10 names `session_pointer_resolvable` as **blocking**. Zero hits across `governance/`, `scripts/`, `.github/`. The protection is real under a different mechanism — commit `4fc6304` deleted the watcher and fixed the dispatcher (`run_checks.py:217-229`, blocking + no subject = FAIL not SKIP). The *second* capability CLAUDE.md attributes to it — drift reporting when `LATEST-RESEARCH` falls behind the DB — **has no replacement**. | rem C10, sweep §1.9 | **CONFIRMED-LIVE** | DEFECT |
| **R-23** | **`workplan/` has 66 documents, 28,347 lines, and no index**; 6 mention the reset. The rename was adjudicated FATAL (278 citing files, 9 immutable migrations, 8 forward-only attestations); the replacement — a generated date-sorted index — was adopted and never built. | rem D9/K3, sweep §1.4 | **CONFIRMED-LIVE** — `ls workplan/ \| grep -i index` → nothing | DEFECT |
| **R-24** | **CONVERGED, with a consequence neither source stated.** `integrity-protocol` and `supersession-audit` are active skills absent from `references/skill-registry.md`. The consequence is live and mechanical: `adherence_log_audit` **CHECK 3 fails today** — *"unknown rule identifiers: ['integrity-protocol']"* — and **4 committed attestations cite it**. Because the `reattestation[]` log is forward-only, this cannot be fixed by rewriting the attestations; the registry entry is the only remedy. | sweep §1.7d + live CHECK 3 | **NEW consequence / CONFIRMED-LIVE** | DEFECT |
| **R-25** | **Canonical doctrine rests on a document that disclaims decision-quality.** `governance/functional-taxonomy.md` (canonical) derives its two-layer architecture from `armature_v4.md` — *"PRE-DECISION DRAFT … NOT decision-quality. Sonnet-drafted"* — citing it 13 times; migration `030` carries `armature §5` reasoning in 8 committed rows. The A7/A12 promotion never happened. | sweep §1.5 (after X1 reversal) | **CONFIRMED-LIVE** | DECISION |

### Class 7 — Standing backlogs (real, large, carried unchanged)

| ID | Finding | Sources | Status |
|---|---|---|---|
| **R-26** | Content and render backlogs carried without re-derivation, each still failing in the advisory set: `validate_reasoning` (the only reasoning doc fails every structural requirement — rem C4) · `validate_pydantic_schemas` 246 findings / 49 unmapped tables (rem C5) · `retired_vocabulary` 69 occurrences, one ruling class missing (rem C6) · `site_pages_fresh` 12 stale pages (rem C3) · `parts/v10` stale in all 15 files and ungated (rem C9) · `room_page.py` queries six non-existent tables (rem C2 / K7) · `research_dod` R1 vacuous-but-satisfiable (rem B4) · `test_verification_pipeline` 15/18 and `test_directness_2_2` (rem B1, B3) · attestation corpus checked one commit at a time (rem C13) · no enforcement rung for schema constraints (rem C8b) · the doctrinally important relations the schema cannot enforce (rem C11) | rem C2–C13, B1–B4 | **CARRIED — all nine advisory failures reproduce at `3eed5d4`** |
| **R-27** | Owner decisions D1–D11 (branch protection; migration exemption list; gate promotion; `verification_status` CHECK; five rival (c)-layer tables; `room_page` fix-or-archive; the two unregistered tests; `citation_mining_pipeline`; connection-register retirement) | rem §1.5 | **CARRIED unchanged** — no re-derivation attempted; D10 remains NOT-READY per K5 |

---

## Part 2 — Where the sources contradicted each other

### 2.1 REFUTED — "a missing dependency produces a pass"

The remediation register's **A2** states: *"without `jsonschema`, the attestation audit exits
**0**. A missing dep produces a *pass*, not a failure."* The consolidation sweep's **X4** stated
the opposite. Neither had tested it; both reasoned from the source.

**Test.** Shadow `jsonschema` with a raising stub and run the audit over `6fcfff0a`, a real
commit that adds an attestation:

```
--- jsonschema available ---   CHECK 3: … unknown rule identifiers: ['integrity-protocol']       exit=1
--- jsonschema blocked    ---  CHECK 1: jsonschema not installed; cannot validate  (+ CHECK 3)   exit=1
```

**A2's consequence clause is REFUTED.** `check_1_schema` appends an issue on `ImportError` and
`audit()` returns `1 if issues else 0`. The dependency defect (R-10) is real; the "silent pass"
that made it urgent is not. **A2 was the stated reason to prioritise it; that reason is gone,
and the item drops from BLOCKER to DEFECT.**

One qualification, in A2's favour: `check_1_schema` returns early when the changeset contains no
attestation, so a run *with no attestations* exits 0 either way — but that is vacuity from an
empty subject (R-15), not from the missing dependency.

### 2.2 REFINED — the graph crash

Both sources state `graph_audit.py:277` crashes. Both are right about the line and wrong about
the scope: the plain audit exits 0, the **selftest** exits 1. Recorded at R-13. This matters for
sequencing — the remediation register makes B2 second overall on the grounds that "a crash hides
other findings," which is true of the selftest's assertions but not of the audit's own run.

### 2.3 CORRECTED — the replay script's path, and what it changes

c91 F9 names `session_2026_05_11g_replay.py` under `scripts/migrate/`. It is under
**`scripts/migrations/`**, where it is the only `.py` among 347 files. The finding survives and
gets *more* serious: it sits inside the directory the repo treats as its reviewable migration
history, so anything auditing that directory by extension will not see it.

### 2.4 STALE — a "three unguarded writers" count that is really "one plus two"

F9 lists three unguarded writers as one set. They are not equivalent: R-01 replays **pre-reset
corpus state into the canonical DB** and is the only one that can undo DR-2026-08-06; the other
two (R-05) are ordinary legacy importers. Merging them under one ID is why "fix this first" and
"three unguarded writers" read as the same size of problem. They are not.

### 2.5 NOT A CONTRADICTION — the check-count drift

The commit-91 review recorded `56 green, 9 advisory`; the consolidation sweep recorded
`55 green, 10 advisory`; this register reproduces **both**. Not a regression and not an error in
either: attestation-scoped checks read the git changeset, so the total moves with the last
commit. Promoted to a finding in its own right (R-17) because two documents recorded it as a
fact about the repository when it is a fact about their diff.

---

## Part 3 — What changed since the sources were written

| Source claim | Now |
|---|---|
| rem C12: "an unguarded replay script … **fix this first**" | **Still live**, at a different and worse path (§2.3). Ranked R-01. |
| rem A2: missing dep → silent pass | **Refuted** (§2.1). Priority drops. |
| rem B2 / c91 F7: `graph_audit` crashes | **Live in the selftest path only** (§2.2). |
| c91: one mis-parsed value (E-12, 81 mm) | **Still live, and not alone** — R-07 (54 Hz, safety-relevant) and R-08 (ordinals) found by re-running its own method. |
| sweep §1.7d: two skills missing from the registry | **Has a live mechanical consequence** — CHECK 3 fails, 4 forward-only attestations depend on the fix (R-24). |
| CLAUDE.md §10: `session_pointer_resolvable` is blocking | **No such check**; the guarantee exists at the dispatcher; one capability was dropped silently (R-22). |
| `attestation_evidence` failing | **Now passing** — its subject changed with the commit, not its logic (R-17). |

---

## Part 4 — Sequencing

Revised from the remediation register's §1.6 for the three status changes above. The
`tooling-register.md` §6 warning still governs: **do not promote checks in the same window as
branch protection.**

1. **R-01** — guard or retire the replay script. Nothing else first: it is the only item that
   can silently reverse the governing decision the rest of this register is premised on.
2. **R-07, R-06, R-08** — the false values. A full value-vs-text audit of all 75 numeric rows,
   not three point fixes. R-07 first on safety grounds.
3. **R-17b** — widen the blocking gate's `COUNT(*)` beyond six tables. Pairs with step 2: until
   this lands, nothing would notice the corrected values regressing. The locator document's fix
   list makes this owner-gated behind its exemption ruling, and cheaper than promoting the deep
   gate — take the cheap one first.
4. **R-09, R-10, R-11, R-12** — bootstrap and registry hygiene. No gate, no risk, unblocks every
   future session. (R-10 demoted from the remediation register's ordering per §2.1.)
5. **R-13** — the selftest crash, before anything downstream of `graph_audit`'s assertions.
6. **R-15** — warranted vacuity floors. **Everything in step 7 depends on this.**
7. **R-22, R-23, R-24** — the three orientation fixes. Cheap, reversible, and R-24 is currently
   a red check.
8. **R-27 D1** — branch protection, alone, in its own window, without `DB integrity`.
9. **R-02, R-03, R-04, R-05, R-14** — write-path hardening and the mutation gap.
10. **R-18, R-19, R-20, R-25** — the frozen-corpus and doctrine-provenance decisions, in that
   order (R-18's single declaration is the prerequisite for the other three).
11. **R-16, R-21, R-26, R-27 D2–D11** — backlogs and rulings, unordered.

**Still not recommended:** any bulk rename (K3), any deletion of a quarantined script
(`tooling-register.md` §6.5 makes quarantine-with-reason terminal), and any check promotion
bundled with branch protection (K4, §6 item 6).

---

## Part 5 — What happens to the six source documents

No document is retired by this one, and no file is moved. The proposal is a header line on each,
pointing here for status:

> *Finding statuses in this document are superseded by
> `workplan/2026-08-11-reconciled-findings-register.md`. Its reasoning and evidence stand.*

That is the minimum that stops the next session reading a stale status as current, and it is
consistent with guardrail 2 (redirect, never delete). Two further observations, both for the
owner rather than for action here:

- **The generated index (R-23) should carry this register's ID column**, so the plan list and
  the finding list resolve against one another. That is the single change that would prevent a
  fourth ID namespace appearing.
- **This document will itself go stale**, and faster than the ones it reconciles, because every
  status in it is a re-derived measurement. Its §0.3 method is the durable part; §1 is a
  snapshot of `3eed5d4`. Re-derive before acting on any row.

---

## Part 6 — Honest limits of this reconciliation

- **R-21 was not re-verified.** It is carried on the remediation register's authority alone, and
  it is a doctrinal claim about shipped rendering code — the class of claim this repo has most
  often found overstated. It should be re-derived before it is acted on.
- **R-26 and R-27 were merged but not re-derived item by item.** I confirmed that all nine
  advisory failures reproduce, which establishes the *class* is live; it does not establish that
  each source's characterisation of each item is still accurate. Five of twenty quarantine
  reasons were wrong on first audit in this repo's history; assume a similar rate here.
- **I nearly dropped the locator-probes document, and the drop would have lost a BLOCKER.** My
  first pass grepped it for the ID formats the other documents use, got nothing, and I wrote
  that it "contributed no distinct surviving entry." That was false: it uses prose section
  headings, not IDs, and its §2.1–2.2 carry **R-17b** — the measured 2.2% scope of the blocking
  reproducibility gate, demonstrated by tampering with committed migration history. Corrected
  before this document was committed, but the near-miss is the finding: **a reconciliation that
  matches on ID format silently drops any source that does not use IDs**, which is exactly the
  pattern-matching failure this work was supposed to avoid. Its Part 4 fix list (8 items,
  4 owner-gated) is also live and is folded into R-27 rather than re-enumerated.
- **Coverage is bounded by what the sources found.** This register reconciles six documents; it
  is not an independent audit of the repository, and R-07/R-08 are a warning about exactly that
  — they existed for weeks in a table nothing was examining, and surfaced only because one
  source's method was re-run rather than read.

---

*Every status in Part 1 was re-derived on 2026-08-11 against `3eed5d4` by running the evidence
command named in the source, except where Part 6 says otherwise. Check counts, DB counts and CI
status are volatile — R-17 is a worked example of one moving inside a single session.*
