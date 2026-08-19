# 2026-08-16 — Adversarial critique of the planned work, and an execution plan for all of it

**Scope.** Everything the repo currently calls "planned": the PR #103 adversarial brief, the
`instrument_status` backfill plan, the 2026-08-14 remediation workplan and its execution plan, the
2026-07-13 ratification register's open rows, and the six findings the 2026-08-16 session recorded.

**Method.** Every claim attacked below was re-derived against the live repo or the live database in
this session. Nothing is inherited from the document it criticises. Where a claim survived, it is
recorded as surviving — a critique that finds only defects has not been run either.

**Baseline, measured before anything else** (`python3 scripts/run_checks.py --all`, after installing
`pydantic`/`jsonschema`, which were absent):

| | |
|---|---|
| Result | **PASS** — 46 green, 13 nothing-in-scope (5 of them blocking and vacuous), 6 advisory failures, 0 blocking |
| `user_version` | 60 |
| Doctrine SHA | `0f2f525` |
| Working tree vs `origin/main` | identical |

That reproduces the 2026-08-16 session's stated baseline **exactly**. It also reproduces the
2026-08-14 execution plan's trap verbatim: `pydantic` is not present in a fresh container, and
without it five blocking checks fail at import. *A red blocking check in this repo is an environment
claim before it is a repo claim.*

---

## Part 1 — Findings

Ten. Severity is about consequence to the next session, not about how wrong the sentence is.

### C1 — HIGH. The stated reason for not fixing the RV-025/026 tripwire does not exist.

**The claim, in three places.** Session record §4 F1, commit `514dea8`, and — most importantly — the
PR #103 brief, where it was handed forward to attack surface A2:

> the tripwire itself was left unchanged, because adding the variants requires a file-level exemption
> for an immutable committed migration comment — the coarse instrument F2 warned about — and that is
> a design call this pass should weigh.

**The test.** `governance/retired-vocabulary.yaml`'s **global** `exempt_paths` already contains
`scripts/migrations/**`, and `scripts/audit/retired_vocabulary_audit.py:191` applies the global list
to every entry before any per-entry list. The migration comment in question
(`data_20260815012107_2026-08-15-owner-decisions-group-1.sql:21`) is therefore already exempt, and
would stay exempt if `Mode-P` and `Mode-S` were added tomorrow.

I then enumerated every live hyphenated occurrence with `git grep` (never ripgrep — the root
`.ignore` would make this exact claim unsafe). All of them fall inside paths the global list already
exempts:

| Location | Occurrences | Exempted by |
|---|---|---|
| `references/audits/bpc-audit-pass{0,1,2}-2026-05-10.md` | 6 | `references/audits/**` |
| `scripts/migrations/data_20260815012107_*.sql` | 1 | `scripts/migrations/**` |
| `workplan/execution-plan-2026-08-12/4-adjudication-apparatus.md` | 1 | `workplan/*20??-??-??*/**` |
| `sessions/**`, `decisions/**`, `attestations/**`, `workplan/2026-08-15-*.md` | 12 | their own globs |

**Verdict: CONFIRMED.** Adding `Mode-P` and `Mode-S` to RV-025/026 today is a two-line registry edit
that produces **zero new flags** and requires **zero new exemptions**. There is no design call for
the adversarial pass to weigh.

**Why this is the highest-severity item here.** The finding it sits inside (F1) is *about* a probe
whose result was read without being derived. The remedy attached to that finding was itself asserted
without being derived, and then written into a binding brief as a fact the next reviewer should
reason from. The failure mode reproduced itself inside its own correction, one paragraph later. The
brief must be corrected before the pass runs, or the pass inherits a false premise on the surface it
was told to attack hardest.

### C2 — MEDIUM. F3 is not an unregistered finding. It is a live advisory red that the session's own baseline printed.

**The claim.** F3 records that `governance/project-instructions-v10_14.md` gates synthesis on
`verification_status ∈ {VERIFIED, UNVERIFIED-1}`, that `UNVERIFIED-1` was retired 2026-08-04, and —
per commit `2176ca5`'s framing — that it is among the findings "in no register".

**The test.** `python3 scripts/audit/retired_vocabulary_audit.py` reports **RV-012 `UNVERIFIED-1`,
16 occurrences**, two of which are `governance/project-instructions-v10_14.md:114` and `:148` —
F3's exact lines. `retired_vocabulary` is one of the six advisory failures in the baseline the
session itself recorded at the top of its record.

**Verdict: the defect is real; the framing is false, and the framing changes the remedy.** This is
not something to discover and file — it is a red gate with a named owner (decision #9) that has been
firing continuously. Filing it as a new finding makes it look like new information rather than an
unactioned alarm.

Related, and worth one line: commit `2176ca5` says "Four of the six findings are in no register" and
then lists all six under that header. One of the two numbers is wrong.

### C3 — MEDIUM-HIGH. The instrument-status plan's compound-name rule is under-specified, its taxonomy is missing a class, and its count reproduces from no rule it states.

**The claim** (`_archived/workplan/2026-08-15-instrument-status-backfill-plan.md` §4):

> Rows that must not be silently "improved": **all 22 rows** whose `standard_name` joins two entities
> in one string. **No organisation has a `/` in its name** — the delimiter always separates two
> things … Instrument compounds (19) … Joint-publication compounds (3).

**The test.** Direct query against `data/guidebook.db`:

- `standard_name LIKE '%/%'` → **21 rows**, not 22.
- rows containing `/` **or** `+` → **23 rows**, not 22.

Neither figure is 22, so the stated rule does not reproduce the stated count. The gap is two specific
rows, and they fail in opposite directions:

- **`jv_id 38` — `DIN 18040 + DIN EN 81-41`.** A genuine two-instrument compound with **no slash at
  all**. An executor applying the rule as written misses it.
- **`jv_id 84` — `EN 81-70:2021+A1:2022`.** A **single** instrument: standard CEN notation for the
  2021 edition consolidated with Amendment 1 of 2022. An executor who generalises the rule to `+` to
  catch jv 38 will bisect this into a phantom "A1:2022" instrument — inventing a standard that does
  not exist, in the table whose whole purpose is telling a disabled reader what the law actually
  says.

**And the two-class taxonomy is missing a third class.** Two of the 22 pair an instrument with
something that is not an instrument:

- `jv_id 15` — `BS 7976-2 / HSE`: a standard beside a *regulator* (the Health and Safety Executive).
- `jv_id 13` — `IPC / ADA reference`: a code beside a *cross-reference note*, not a second document.

Neither splits into "one row per instrument, same jurisdiction" and neither is a joint publication.
Under the plan as written, an executor would manufacture an instrument row named `HSE` and another
named `ADA reference`, then be obliged to give each an `instrument_status`.

**Verdict: CONFIRMED, and this is the executable core of the plan.** The §4 correction box directly
above this passage records the owner catching the author asserting an unverified distinction about
these very rows. The paragraph immediately below the apology does it again.

**The fix is not a better rule — it is no rule.** Twenty-two rows is a list, not a pattern. Enumerate
them by `jv_id` (2, 10, 11, 12, 13, 15, 25, 29, 33, 35, 38, 42, 51, 57, 59, 78, 80, 81, 82, 103, 104,
107), classify each by hand against its own source, and let the delimiter be a discovery aid that
appears nowhere in the executable instruction.

### C4 — MEDIUM. Acceptance test 6 cannot pass, and the reference standard it measures against is itself unguarded.

**The claim** (§7.6): "no canonical `JurisdictionCode` used by the table is absent from
`lang_jur_map`."

**The test.**

```
jv jurisdictions not in lang_jur_map → ['GB', 'ISO']
```

`GB` is D4(a), which the plan owns. **`ISO` is not.** `ISO` is a declared canonical
`JurisdictionCode` meta-code (`schemas/enums.py:176`), it carries **13 rows** — the third-largest
jurisdiction in the table — and `lang_jur_map` has no row for it. So test 6 fails after D4(a) is
fixed, on a row class the plan never mentions.

**The larger half.** The plan treats `lang_jur_map` as the standard `jurisdictional_values` should be
measured against. `lang_jur_map` carries **48** jurisdiction codes, **22 of which are not in
`JurisdictionCode` at all** (AR, AT, BE, CL, CO, CR, CY, EC, ES, ET, FI, GH, GT, IT, MA, MX, PE, PH,
PT, TH, TZ, UY). D4's diagnosis — "there is no CHECK and no FK on `jurisdiction`, and what is
unguarded has drifted" — applies to `lang_jur_map` *more* strongly than to the table the plan is
fixing, and the proposed guard on `jurisdictional_values.jurisdiction` would not touch it.

**Verdict: CONFIRMED.** Test 6 needs `ISO` named explicitly (either added to `lang_jur_map` or scoped
out as a meta-code), and D4 should be restated as a two-table defect. This also feeds owner decision
**#6** (jurisdiction scope): the "27 in the schema enum" figure the workplan quotes is real, but
there is a fourth number nobody has counted — 48 — and it is the one a join actually meets.

### C5 — MEDIUM. The register's own "still owed" list contradicts the session record that wrote it, in the direction that licenses an unlicensed act.

`workplan/ratification-execution-register-2026-07-13.md`, closing section:

> **Executable without owner input:** Q1 remainder, Q3 doctrinal-content half, **Q5-H2/H3/H4
> (schema …), Q6 `instrument_status` (schema …)**, E10 ICCT …

`sessions/session_2026-08-16-ladder-and-vocabulary-sweeps.md` §5, same session, same day:

> Everything owner-gated stayed untouched … **Q5-H2/H3/H4 and Q6 `instrument_status` (D-SCHEMA)**,
> E10 ICCT (same) …

Both cannot be true. D-SCHEMA is Change-Order gated (`CLAUDE.md` §4, §5); the instrument-status plan's
own header says so in its first line. **Verdict: the register is wrong**, and it is wrong in the
sentence a next session reads to decide what it may do. A session that orients from the register —
which is what the register is for — would author a migration it is not licensed to author.

### C6 — MEDIUM. Q19's premise has been overtaken by a taxonomy change. Executing it as written would report a false completion.

Q19 is named in the 2026-08-16 record's "Next" as remaining executable work. Its row reads:
*"11 of 22 populations and 6 of 92 items have no page at all."*

Live, this session:

| | Row says | Live |
|---|---|---|
| Populations | 22 | **23** |
| Populations with no page | 11 | **17** |
| Items | 92 | **93** |
| Items with no page | 6 | **0** |

`site/specs/` holds 93 pages against 93 items with an exact one-to-one match — **the item half of Q19
is already discharged**, by work nobody attributed to it. The population half went the other way, and
not by neglect: the six pages that exist are DEAF, DEM, MH, MOB, NDV, PAIN, while the pages the
2026-07-13 C2 log records generating (DBL, NEU, OFS, VIS, UPL) are gone and fourteen codes that did
not exist then (ADHD, AUT, BLIND, BRAIN, DEAFBLIND, EPI, ID, LMB, LPA, MOVE, MS, SCI, TALL, VES) now
do. That is the "work from axes, not umbrellas" reconciliation (DR-2026-07-22) landing underneath a
workplan row that was never re-derived against it.

**Verdict: Q19 needs re-derivation, not execution.** Its numbers are stale, its item half is done,
and its population half is now a question about a taxonomy that changed after the row was written.

### C7 — MEDIUM. The P3 gate did not gate. PR #103 is merged, and the brief is written for a world that no longer exists.

Verified against the GitHub API this session: PR #103 is `state: closed`, `merged_at:
2026-08-15T22:00:38Z`. Commits `514dea8` and `2176ca5` both call it "the still-open PR #103".

The brief is a **gate condition** — Q22's own register row set it, and the register says "each
execution stage runs the mechanical battery and the whole execution is queued for an independent
adversarial pass." The work merged to `main` without it. Two consequences, and the second is the one
that matters:

1. The brief's remedies are stale. §2 A1 says a hit "is a revert"; §4 says findings come "before
   push". Neither is available. Every finding is now a fix-forward on `main`, in a new PR.
2. **A gate that can be merged past is not a gate.** Either P3 is real — in which case the merge is a
   deviation to record, and the brief needs restating as a post-merge audit with a fix-forward
   remedy — or P3 is advisory, in which case it should say so rather than describing itself in
   blocking language. Leaving it ambiguous is how the repo's own recurring failure mode (a check that
   looks like it gated something) reproduces at the process layer.

I am **not** claiming the merge was wrong. I am claiming that nothing in the repo currently records
that it happened without the gate.

### C8 — LOW/MEDIUM. `working/` is a fourth state: live, git-tracked, cited as authority, and absent from the repository map.

`working/` holds **39 git-tracked files** (`evidence-migration/`, `pilot/`, `mobile-app-prototype-v9/`,
`claims-docket.md`, two complete-provision drafts). It appears nowhere in `CLAUDE.md` §3's repository
map, is not covered by the root `.ignore`, and is not `_archived/`.

It is not inert. `working/pilot/PILOT-MANIFEST.md` is cited as governing authority by register rows
Q7 and Q25. And it carries **10 of the 70** live retired-vocabulary occurrences:
`working/evidence-migration/equity-dashboard.md` ×5, `non-english-coverage-matrix.json` ×2,
`global-south-finding.md` ×2, `working/pilot/PILOT-MANIFEST.md` ×1.

**Verdict:** a directory that is neither current, nor frozen, nor hidden, nor mapped is exactly the
blind spot `CLAUDE.md` §10 exists to prevent. It needs a disposition, and until it gets one it needs
a line in the map.

### C9 — LOW. Two exemptions on the tripwire are dead, and a dead exemption reads as a live licence.

RV-025 and RV-026 each carry `exempt_paths: ['workplan/ratification-execution-register-2026-07-13.md']`.
The global list already exempts `workplan/*20??-??-??*.md`, which matches that filename. Both
per-entry exemptions have never had an effect. They should be deleted — the entries' own notes say
"exempt the FILE, never the token … delete these exemptions rather than widening them", and a
reviewer auditing the escapes (brief A2) will otherwise spend time on two that do nothing.

### C10 — LOW. What survived.

Recorded because a critique that reports only defects has not been run:

- **The 2026-08-16 baseline reproduces exactly.** 46 green / 13 nothing-in-scope / 6 advisory / 0
  blocking, re-measured from a clean tree in a fresh container.
- **The Q1 sweep's counts are true.** `retired_vocabulary_audit.py` reports RV-025 and RV-026 at
  1 occurrence each, both on `site/rooms/r_ba.html:118` — a single line of generated output, exactly
  as claimed — and a register total of **70**.
- **F2's collision is real.** `scripts/migrations/` holds `058_status_vocabulary_ratification.sql`,
  `059_tier1_retirements.sql`, `060_restore_superseded_status.sql`. The remediation workplan's
  original 058–060 allocation would have collided on the first migration written.
- **Every D1–D4 defect in the instrument-status plan is true as stated.** 109 rows; `is_code_minimum`
  NULL on all 109; `evidence_tier = 6` on all 109 (DDL: `NOT NULL DEFAULT 6`, comment "code/regulatory
  values are Tier 6 by definition"); the set does include ISO, BS, DIN, EN, AS/NZS, ANSI instruments
  misgraded as statutory; `GB` joins 0 of 20 rows against `lang_jur_map`; `NZ` has 0 rows.
- **The decision to leave `site/rooms/r_ba.html` alone was right.** It is generated output whose
  regeneration is entangled with an open HOLD. Reporting 33 → 2 honestly beats reporting 33 → 0 by
  hand-editing a generated file.
- **The self-disqualification on the PR #103 pass was right**, and the reasoning given for it
  (independence spent on A1 and A5 before reading the diff) is sound.

---

## Part 2 — The state of the queue, honestly classified

Everything currently planned, with what actually gates it. This replaces the several partial lists
scattered across the register, the session record and the two workplans.

| Gate | Meaning | Items |
|---|---|---|
| **FREE** | No owner input, no schema change, no cold-context requirement | C1–C9 remediation; Q19 re-derivation; the `working/` disposition proposal |
| **COLD** | Needs a session that has not read the authoring reasoning | PR #103 adversarial pass |
| **D-SCHEMA** | Change-Order gated (decision #4) | Migrations 061–066; Q5-H2/H3/H4; Q6 `instrument_status`; E10 ICCT (`cross_test_pairs` — verified absent from the schema) |
| **OWNER** | Decisions #1, #2, #3, #5, #8, #10; retirement approvals; `schema-reconciliation.md` currency | Track D; the reproducibility consolidation |
| **DG-NON** | Owner-only by doctrine; propose, never decide | #6 jurisdiction scope; #7 cross-population; E11 product posture; §5 of DR-2026-07-25; Q15 |
| **RESEARCH** | Evidence work, not a sweep | F4 (source-level tier labels in prose); Q13 external-mining queue |

Two corrections to how that queue is currently written down:

- **Q5 and Q6 move from FREE to D-SCHEMA** (finding C5). They are listed as executable without owner
  input in the register; they are not.
- **E10 ICCT moves with them.** `cross_test_pairs` does not exist in the live schema (verified:
  `sqlite_master` returns 0 rows for it), so building it is a schema migration, not a sweep.

---

## Part 3 — Execution plan

Five waves. Waves 0 and 1 are executable now. Everything after Wave 1 is gated, and the plan's job
there is to say *what unblocks it*, not to pretend it can be done.

### Wave 0 — correct the record before anyone acts on it (FREE, urgent)

Findings-first discipline (the brief's own §4): the corrections go in *after* the findings are
recorded, and this document is that record. Wave 0 is one commit, no DB change, no doctrine.

| # | Edit | Fixes |
|---|---|---|
| 0.1 | `workplan/2026-08-15-adversarial-brief-pr103.md` — strike the "requires a file-level exemption" premise; state that `scripts/migrations/**` is already globally exempt and the widening is a zero-flag edit; restate the brief as a **post-merge audit** with fix-forward remedies; correct "still-open PR #103" | C1, C7 |
| 0.2 | `workplan/ratification-execution-register-2026-07-13.md` — move Q5-H2/H3/H4, Q6 and E10 out of "executable without owner input"; re-derive the Q19 row against 23 populations / 93 items / 0 items-without-page / 17 populations-without-page, and note the DR-2026-07-22 taxonomy turnover as the cause | C5, C6 |
| 0.3 | `_archived/workplan/2026-08-15-instrument-status-backfill-plan.md` §4 — replace the delimiter rule with the enumerated 22 `jv_id`s; add the third class (instrument-beside-non-instrument: jv 13, 15); name jv 38 (`+`, genuine compound) and jv 84 (`+`, **not** a compound) explicitly. §7 — name `ISO` in test 6; add the `lang_jur_map` drift as D5 | C3, C4 |
| 0.4 | `sessions/session_2026-08-16-ladder-and-vocabulary-sweeps.md` — forward-note on F1 (premise false) and F3 (already firing as RV-012; see decision #9). Append-only; the record is not rewritten | C1, C2 |
| 0.5 | `CLAUDE.md` §3 — add `working/` to the repository map with its actual status (live, tracked, cited by two register rows, undisposed) | C8 |

**Acceptance:** `run_checks.py --changed-from origin/main` PASS, 0 blocking; advisory count no worse
than 6; no DB write; `user_version` 60 unchanged.

### Wave 1 — the two mechanical fixes the findings license (FREE)

| # | Edit | Note |
|---|---|---|
| 1.1 | Add `Mode-P` and `Mode-S` to RV-025/026 (or widen `match:` to cover the hyphenated adjectival form) | Verified zero new flags, zero new exemptions. Widening a tripwire is monotone: it can surface drift, never silence it — so it does not compromise brief A2, whose subject is the *escapes*. Record the change in the brief so A2 knows the instrument moved and why |
| 1.2 | Delete the two dead per-entry `exempt_paths` on RV-025/026 | C9 |

**Acceptance:** `retired_vocabulary_audit.py` still reports exactly 70 occurrences and RV-025/026 at
1 each. **If either number moves, 1.1 is wrong and reverts** — that is the test, and it is written
before the work.

`governance/` is CODEOWNERS-protected: this is a review request on the PR, not a bar (per the
2026-08-14 execution plan §6's precedent for registry edits).

### Wave 2 — the PR #103 adversarial pass (COLD)

**This remains the top open item, and it has now been deferred twice.** It cannot be run from this
session: I have read the brief, the 2026-08-16 record, and the register's summary of the author's
self-review — which spends the same independence the previous session disqualified itself for.

Three ways forward, and this is a call for the owner:

1. **A fresh session, briefed only with the corrected brief and the diff.** Cleanest. Costs one
   session.
2. **A cold subagent from a session that does not read the brief's contents into its own context.**
   Faster, and the isolation is real, but it needs explicit authorization.
3. **Accept the pass as undischarged and record it as a deviation**, closing the gate rather than
   leaving it open indefinitely. Legitimate, but it should be a decision, not a drift.

Whichever is chosen, the brief must carry Wave 0.1's corrections first, or the pass reasons from a
false premise on surface A2.

### Wave 3 — the Group 3 schema batch (D-SCHEMA, decision #4)

One owner decision unblocks the largest block of owed work. The batch, with the re-allocation F2
established:

| Slot | Contents | Source |
|---|---|---|
| 061 | `constraint_floor` | Track C, prototyped at 058 |
| 062 | `jurisdictional_values_provenance` | Track C, prototyped at 059 |
| 063 | `claim_capture_uniformity` | Track C, prototyped at 060 |
| 064 | `determination_provenance` | Track C, prototyped at 061 |
| 065 | `specification_claim_links` | Track C, prototyped at 062 |
| 066 | `source_excerpts` | Track C, prototyped at 063 |
| 067 | ratification trigger | Writer plan Phase 0 |

**Three things should join that batch rather than follow it**, all because they open the same tables
while those tables are cheap to open:

- **Q5's H2 columns** (`functional_basis`, `derivation_paths`) — `specifications` is 0 rows. The
  register already raised this collision; it is right.
- **Q6 `instrument_status` + `instrument_status_basis` + the D4/D5 jurisdiction guard** — one pass
  over `jurisdictional_values` for the instrument dimension, the `GB → UK` normalisation, the
  compound-name split and the CHECK, rather than three.
- **E10 `cross_test_pairs`** — unbuilt, and it is a table creation like the rest.

**Preconditions before the batch is authored, not after:**
1. The six prototypes are **re-prototyped at their new numbers** (the renumbering is mechanical, but
   nothing has verified it).
2. Q6's Band-B policy is decided (§4 of the backfill plan) — my recommendation stands with the plan's:
   execute Band A mechanically, leave Band B/C `unclassified`, open a gap row per Band-B family.
3. The 22 compound rows are classified **by hand, by `jv_id`**, per Wave 0.3.
4. Decision **#1** (`jurisdictional_values.evidence_tier` nullable vs. `NOT NULL DEFAULT 6` + CHECK)
   is arbitrated — it changes what migration 062 writes.

**Acceptance is already written** in the backfill plan §7 and Track C's own criteria: rebuild
reproduces shallow **and** `--deep`; every CHECK shown *firing* on a scratch rebuild; `unclassified`
count reported rather than minimised; `test_db_integrity` no worse than baseline.

### Wave 4 — Track B governance, Track D retirement (OWNER)

Unchanged from the remediation workplan; nothing here is mine to move. Sequencing note only: Track B
commit **A** rotates the doctrine SHA, and the re-attestation cascade is materiality-scoped via
`governance/doctrine-deltas.json`, not a commit window. The workplan's claim that the discharged
obligation is **zero of 82 attestations** should be re-verified with
`adherence_log_audit --check window` *at the time*, not inherited from a plan written two days
earlier.

Track D's Tier-1 batch is partly executed already (`059_tier1_retirements.sql`), so the row must be
re-derived against what shipped rather than renumbered — F2 flagged this and it is still outstanding.

### Wave 5 — the research-shaped remainder (RESEARCH)

**F4 and Q13 are not sweeps and must not be executed as sweeps.** F4 (prose carrying pre-2026-05-25
source-level tier labels) is re-grading evidence source by source, and `evidence_sources` is **0 rows**
after the clean-room reset — so the prose is the only surviving record of those gradings. Rewriting it
mechanically would destroy the record and manufacture new gradings in one move.

Two things belong to F4's scope that nobody has counted, and I am recording them rather than acting:

- **RV-016 `VERIFIED-WITH-CORRECTION` — 38 occurrences**, the single largest contributor to the
  advisory red, concentrated entirely in `references/tier{1,2,3}-verified-sources.json` and
  `references/co1-verified-sources.json`. Those files are pre-reset artifacts carrying a retired
  status vocabulary against a table that is now empty.
- **RV-014 `VERIFIED-2` — 9 occurrences**, same class.

Together with RV-012's 16, that is **63 of the 70** live occurrences sitting in one unscoped
question: what happens to the pre-reset verification record. It deserves its own owner decision, and
it is currently filed as a low-urgency finding.

---

## Part 4 — What this plan does not do

- **It does not run the PR #103 pass.** See Wave 2; running it from here would be the third session
  to spend its independence and then use it.
- **It does not author any migration.** Every schema item is D-SCHEMA, and the numbering is spoken
  for by a batch queued for owner decision.
- **It does not touch doctrine, the ledger, or the PI.** F3's remedy is owner decision #9, and the PI
  is not API-writable.
- **It does not sweep F4.** Re-tiering sources is research.
- **It does not resolve `working/`.** It proposes a map line and a disposition question; the
  disposition is a retirement-class call and therefore owner-gated.
