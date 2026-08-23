# 2026-08-22 — Master execution plan for the next session

**Read this first, then `decisions/DR-2026-08-19-research-restart-operative-instrument.md` §12 for
the batch runbook.** This document absorbs and replaces
`workplan/2026-08-22-workplan-reconciliation.md`, which was deleted rather than archived — it was
scaffolding, and git is the archive for scaffolding (CLAUDE.md §1). **It adds no file to the
repository.**

**It is written to be executed and then deleted.** §7 gives the condition. Every act below is a
fix, a record correction, a migration, an archival move, or a research batch. **No act authors a
new plan, check, table or script.** A session that extends this file instead of executing it has
reproduced the defect that produced it.

**Scope.** Derived from the ten-day commit window **2026-08-12 → 2026-08-22** (126 non-merge
commits) and the live repository, per owner instruction 2026-08-22. Earlier material is out of
scope and deliberately not enumerated.

**Standing owner rulings folded in, do not re-raise:** `bpc-rewrite-workplan-2026-05-11.md` and
`best-practices-assessment-system.md` are **100% superseded and can be ignored.** An earlier draft
raised both as doctrine-carrying concerns. They are not concerns.

---

## 0. What will stop you

The four rules in CLAUDE.md §0 are unchanged and are what actually blocks a commit. Two matter most
here:

- **Never write `data/guidebook.db` directly.** Scratch copy → `emit_batch_sql.py` (or hand SQL) →
  `emit_data_migration.py` → `migrate_db.py`. The canonical sha256 must not move until the
  migration is applied.
- **A rename or removal is not done until the callers are swept.** Act A1 is a removal; its
  falsification clause is the sweep.

**And one rule from this window, ratified 2026-08-22:** establish facts about this repository from
its structure, never from a text search. Locating a known literal in a known file in order to
change it is fine. **Finding a place to edit is fine; deciding what is true is not.**

---

## 1. Orientation — derive these, do not trust them

Figures below were true at 2026-08-22. **Re-derive before relying on any of them** (CLAUDE.md
§2(b)). They are here to tell you where to look, not what to report.

| | |
|---|---|
| `PRAGMA user_version` | 60 · schema migrations end at `060`; `061–066` were **LAPSED** by DR §10 item 8 |
| Doctrine SHA | `0f2f525` |
| `sessions/LATEST` and `LATEST-RESEARCH` | both `session_2026-08-22-research-batch-02-room-acoustic-performance.md` |
| Corpus | **10** `evidence_sources`, all on **one** slug of 106 · `specifications` **0** |
| Stash | **835** `source_locators`, **441** with a DOI, of which **4** are in the corpus |
| Candidates | **44** — 10 resolved and unadmitted, 31 unresolved, 3 dispositioned |
| Gaps | **5**, all OPEN, all on `room-acoustic-performance` |
| Registered checks | 63 active, 4 quarantined |

**The state in one sentence:** the write path works, one slug has a compliant evidence base, and
nothing has been determined from it.

---

## 2. The one blocker

**The population-taxonomy pass (D-0165, DEFERRED) is the critical path.** It gates acts 5–6 of the
08-22 plan, the first determination, and therefore `specifications` moving off zero. It is the only
thing in this repository whose absence stops the deliverable.

**Nothing in §3 or §4 waits on it.** That is the test this plan had to pass to be worth writing.
Do not idle on the blocker; do not author a determination around it. The refusal recorded in
`workplan/2026-08-20-adversarial-adjudication-a18-aut.md` stands and DR §3 step 5 was amended to
honour it.

---

## 3. Phase 1 — the fix research depends on (do this first)

### A1 · OD-5: make the R9 duplicate gate see the stash
**Location:** `scripts/audit/research_batch_dod.py`, the R9 check.
**Defect:** R9 queries `evidence_sources` (10 rows) and is blind to `source_locators` (**835 rows,
441 with DOIs, only 4 of which the corpus already holds**). So the gate certifies "no duplicate"
against 2% of what the project actually holds. Batch 02 ran the stash check **by hand** because the
gate could not.
**Why first:** it is CLAUDE.md §2(a) — *a gate that passes having examined nothing* — in the one
battery guarding research admissions, and Phase 2 admits sources through it. Four in-window
documents name OD-5; none fixed it. It demonstrated itself three times in a single batch, once by
surfacing Finitzo-Hieber & Tillman 1978 through backward mining after R9 had passed the same DOI
space clean.
**Do:** widen the R9 query to `source_locators`; keep `EXAMINED:` printing the true subject count.
**Falsification — CORRECTED 2026-08-23 during execution.** The original read *"R9's `EXAMINED`
must rise above the `evidence_sources` figure"*, which is **malformed**: `EXAMINED:` is emitted only
by `check_baseline()` and counts *rule codes*, not subjects. There is no per-rule EXAMINED to rise.
The real test is two-sided — seeded violations must fire, **and** the four correct stash-to-corpus
promotions in the live corpus must NOT.
**Then:** close `GAP-B01-004` by migration, or record in the gap row why it stays open.

**This is a fix, not apparatus.** Nothing is added. If you find yourself writing a new check here,
stop — CLAUDE.md §1 puts the burden of proof on addition.

---

## 4. Phase 2 — research batch 03, the work that moves the deliverable

Run under DR §12's runbook and the R1–R15 contract. **Gate before claiming done:**
`python3 scripts/audit/research_batch_dod.py --session <id>`.

Four bodies of work exist, already staged, in dependency order. **Do not start a new slug** — this
slug is not finished, and starting a second one before the first has a determination is how the
corpus ends up 106 slugs wide and zero deep.

### B1 · Discharge the R2 debt — forward mining has never been run
**Evidence:** all 7 `citation_mining` rows record `backward=1, forward=0`, and every one has
`connections_produced='[]'`. **R2 requires backward AND forward.** Three sources are also unmined
entirely — `citation_mining_status='pending'` on **REF-00561** (Bettarello 2021), **REF-00969**
(Rosas-Pérez 2023), **REF-00970** (MARKUSSEN 2024).
**Do:** forward-mine the seven mined anchors; mine the three pending ones both directions. Record
what each produced — **an empty result is a completed unit of work (R8) and must be kept.**
**Trap, cost two hours in this window:** `db.py log-mining --ref` takes the **LOCAL** id
(`RAP-01`), not the global one. Passing the global id leaves `global_ref_id` NULL and the blocking
gate keeps reporting a RULE 124 violation for mining you actually performed.

### B2 · Promote the four mining-surfaced leads
Held in the stash as `source_locators` rows — **REF-00327, REF-00576, REF-00577, REF-00579** — and
staged as candidates **#41–#44**: Neuman 2010, Wroblewski 2012, Anderson & Goldstein 2004, and
**Finitzo-Hieber & Tillman 1978**, the last being the paper backward mining surfaced after R9 had
passed the DOI space clean. **These are the demonstration that A1 was worth doing.** Re-retrieve
every locator (R10), pre-check the DOI (R9), admit or log the refusal.

### B3 · Resolve the ten staged candidates
`search_candidates` #4–#13, `RESOLVED` + `PENDING-VERIFICATION`, each with a DOI. Six are already in
the corpus; **the ones that are not include Marzi 2025 (`10.1038/s41598-025-02358-4`), Marzi 2024
(`10.1016/j.buildenv.2024.112254`), Devos 2019, Black 2022 and Amlani & Russo 2016.**
**R15 applies and is not optional:** a staged candidate description is a **hypothesis**. On
resolution, re-describe it from the source and **correct it if you over-claimed.** In this window a
year was inferred from a DOI slug (`10.1044/2019_AJA-19-0010` → "2019"); the payload says **2020**.
Do not let a guess harden into a fact.

### B4 · Close the two content gaps by reading
**`GAP-B01-001` and `GAP-B02-001` both require a reader other than the authoring session to read
all five sources in full and confirm or correct every claim recorded against them.** GAP-B02-001
names two figures specifically — **0.4–0.7 s and 0.3 s** — which must be verified from the sources
with a locator, or struck.
**This is the highest-value item in Phase 2 and it is not a search.** Every content claim from both
batches is currently unread. No amount of new admission changes that.

### B5 · The Italian-language sweep
Candidate #39 (D'Orazio 2025, the Italian classroom-acoustics standard) and #34 (Tardini 2025,
national target values) both point at a non-English literature that has not been swept. **R5:
non-English peer-reviewed work is academic, not grey; non-indexation is an indexing fact, not an
evidence-quality fact. R11: every alias carries its in-language source, or `[UNVERIFIED-TERMS]` —
no back-translation.**

**Acceptance for Phase 2:** the DoD gate exits 0 with `EXAMINED > 0` on every rule; forward mining
is recorded for every anchor; and **at least one of GAP-B01-001 / GAP-B02-001 is closed by an
actual read.** Admitting more sources without closing a read-gap is not progress.

---

## 5. Phase 3 — record corrections, folded in at session close

Cheap, unblocked, and none of it should be allowed to become its own session.

### A2 · Fix R-12 — filed 2026-08-11, refiled 2026-08-18, still live
**Location:** `governance/check-registry.yaml`, `batteries: governance:`.
The description is unquoted YAML containing commas, so it parses as
`{'deps': ['pydantic'], 'description': 'Decision protocol', 'doctrine recheck': None, 'adversarial-use.': None}`
— two phantom keys where a description should be. Its content is stale too: it advertises a
"doctrine recheck" that **OD-10 abolished on 2026-08-19**.
**Do:** quote it, drop the abolished clause.
**Verify:** `python3 -c "import yaml;print(yaml.safe_load(open('governance/check-registry.yaml'))['batteries']['governance'])"`
prints exactly two keys.

### A3 · Correct the `db_integrity` battery description
**Location:** `governance/check-registry.yaml:171`. It reads
`DB content integrity (35 checks). Red on main - see tooling-register 4.` while the check-level note
was corrected on 2026-08-22 to *72/72 checks pass*. **Two lines in one file, opposite claims.**
**Do:** remove the count and the status claim. **Do not substitute a fresh number** — a hardcoded
count in a derived document is the defect, not the stale value.

### A4 · Retire `workplan/execution-plan-2026-08-12/` — 13 files, 4,065 lines
**Do:** `git mv` to `_archived/workplan/execution-plan-2026-08-12/`. `_archived/` is the right home
for retired content and is ratified as permitted to grow (2026-08-19).
**Evidence, verified 2026-08-22:** its own status line reads *"PROPOSED. Nothing in this directory
has been executed"*, and three independent structural probes agree — `work_log` absent,
`locator_schemes` absent, and **28 of 93 `items.name` still contain digits** (Wave H undone). An
exhaustive referent scan over every tracked file shows the directory is **referentially closed**:
every member's referrers are its own twelve siblings, plus exactly two externals —
`governance/retired-vocabulary.yaml:105` (a *comment* citing it as the live example of the
`workplan/*20??-??-??*/**` glob — **correct the comment, keep the glob**, which is a pattern and
would otherwise un-exempt future dated plan directories) and
`workplan/2026-08-16-adversarial-critique-and-execution-plan.md:55` (a table row citing a path,
repoint it).
**No other live workplan file has zero referents.** Nothing else moves blind.
**Falsification:** re-run the referent scan after the move; if any tracked file outside `_archived/`
still names a member, the sweep is incomplete and A4 is not done. **The scan cannot see prose
callers** — read `skills/*_SKILL.md` directly, because that exact blindness is what made cull
Phase 4a unsafe.

### A5 · Strike `GB` → `UK`; do not execute it
**Locations:** `2026-08-18-handoff-next-session.md` §6 step 4 ·
`2026-08-19-adversarial-critique-research-restart.md` §7 item 7 ·
`2026-08-18-research-frame-proposal.md` §10.4.
**Do:** strike it in each with a dated note. **Write no migration.**
**Reason — this reverses four in-window plans:** `GB` is the ISO 3166-1 alpha-2 code for the United
Kingdom; `UK` is not an ISO code. The change was specified to align with a `jurisdictions` table
that does not exist and is not due until DR §3 step 6. Meanwhile `jurisdictional_values` is under
the owner's REFERENCE-ONLY quarantine — **a write to it on 2026-08-21 was caught by blocking L02 and
retracted the same session.** Four plans scheduled it in ten days and not one asked whether it was
right. It is a naming decision; it goes to the taxonomy pass.

### A6 · Reconcile at the DR, not in a new document
**Location:** `decisions/DR-2026-08-19-research-restart-operative-instrument.md`, amended **in
place** on the precedent its own 2026-08-22 amendment set.
- **§8 read-set** — `2026-08-18-research-restart-plan.md` is absorbed into DR §12 and
  `2026-08-18-handoff-next-session.md` has **1 of 10 steps executed** with its §6 spine overturned.
  Mark both *read as history* **at the citation**, not in a caveat further down; a session reading a
  mandatory read-set does not reliably reach the paragraph that qualifies it.
- **§3 step 6** — fold in the four items below, with their locations, so each is named **once**.
- **§B** — add the §6 dispositions, making the supersession table the single index.
**Then** append a dated forward note to `decisions/DR-2026-08-06-clean-room-evidence-reset.md` §3:
its "109/109 on `source_section`" is **0/109** after the 2026-08-12 clearing. **Annotate; never
rewrite** — a DR records what was decided on its date.

### A7 · Score the 08-22 plan; do not archive it
`workplan/2026-08-22-agonist-antagonist-execution-plan.md` §6 requires a scorecard *in that file*
before archival, and none exists. **Append it:** acts 0–4 done (act 3 with its recorded deviation),
acts 5–6 blocked by D-0165, 3 of 7 owner decisions answered, acceptance 4 undeterminable because
both sides of the ledger it defined changed shape. **Do not archive** — acts 5–6 are blocked, not
finished, and archiving a blocked plan loses the block.

---

## 6. Phase 4 — the cull program, against the L0–L3 frame

**Culling is not a size exercise and must never be run as one.** It is run against the census's
level frame (`workplan/2026-08-18-structural-census-and-cull-list.md` §2), which is the operative
definition and is retained here because that file is otherwise historical:

> **Level is assigned by what the artifact takes as input, not by where it lives.**
> **L0 substance** — input is the world: evidence, items, populations, BPC content, renders, and the
> code that reads and writes them. **L1 first-order** — input is L0: *is the guidebook correct?*
> **L2 second-order** — input is L1: *is the checker correct?* **L3+** — input is L2+: registers
> tracking audits, plans remediating plans, passes reviewing passes.

**The rule that follows from the frame, and the only one that matters:** an artifact earns its place
by the level of its input and by having a reader at a lower level. **An L1 check with no L0 subject,
an L2 check with no L1 subject, and an L3 document with no L2 referent are the same defect** — they
consume attention and return nothing. Cull upward from L3, never downward from L0.

**The census's own figures are pre-cull and must not be quoted.** Everything below was re-derived
2026-08-22. Re-derive again before acting.

### 6.1 Where the mass actually is

| Stratum | Files | Lines | Share |
|---|---|---|---|
| `_archived/` | 610 | 266,666 | **39%** (28.1 MB) |
| governance + references + skills | 726 | 156,317 | 22% |
| generated output | 179 | 84,308 | 12% |
| sessions + provenance | 336 | 69,066 | 10% |
| **executable** | 133 | **40,377** | **5.7%** |
| workplan (live) | 72 | 31,942 | 4.5% |
| **total tracked** | **2,201** | **712,636** | |

Executable is **29,061 LOC** by CLAUDE.md's derivation, down from ~35.4k before the 2026-08-20 cull.

**Finding: the code cull is finished.** It reached 5.7% of the repository and the last pass took the
dead weight. **Further code culling is the ratchet running in reverse** — spending L3 sessions on the
smallest stratum in the building. The remaining mass is `_archived/` at 39%, which the owner ruled on
2026-08-19 **may grow**. So the repository will not get smaller, and that is settled, not a problem
to solve. **What costs a session is not size; it is what it trips over while orienting.** Cull for
attention, not for bytes.

### 6.2 Workstream A — orphans, the sharpest findings in the repository

Derived by scanning all 95 non-migration code files for each object's name. **Limitation, stated
because it changes what may be concluded: a name match in SQL is the only available signal, and a
prose caller — a script invoked from skill text — is invisible to it.** That exact blindness is what
made cull Phase 4a unsafe. **Confirm by reading `skills/*_SKILL.md` before deleting anything here.**

| Orphan | Measured | Act |
|---|---|---|
| **11 of 17 database views are read by no non-migration code.** `v_coverage_priority` **computes 7,208 rows that nothing reads** — the single largest piece of dead machinery in the DB. `v_source_admission` and `v_source_reach_all` return 10 rows each, also unread. The other eight return 0 | live query + code scan | **Drop the unread views by migration**, one migration, evidence in the commit. A view is pure derivation — git holds the DDL, so this is free to reverse |
| **8 empty tables are named by no code at all** — `case_study_populations`, `case_study_specs`, `case_study_strategies`, `economics_entry_populations`, `economics_entry_specs`, `external_root_registry`, `room_items`, `situations`. Never written, never read | live query + code scan | **Distinguish orphan from dormant before dropping.** The case-study and economics children are dormant — R12 routes real content to their parents. `external_root_registry`, `room_items`, `situations` look like true orphans. **Owner call on the dormant set; drop only the true orphans** |
| **0 triggers exist.** The `stated`-ratification refusal ruled in the writer plan was never built; the bar survives only as prose | live query | **Record it; do not build one.** Adding a trigger is apparatus, and §0's burden of proof applies |
| **33 of 65 tables are empty**, including `specifications` | live query | Not a defect — it is the deliverable's shape. **Do not "fix" it by seeding** |
| **The two dead reference registries** — `references/claim-reference-join.json` + `global-reference-registry.json`, **25,979 lines, 0.76 MB, zero code referents**, only prose referrers, most in documents already retiring | referent scan | **Delete. This is the largest genuine deletion left in the repository.** Sweep the five/six prose referrers first — CLAUDE.md §0.4 |

### 6.3 Workstream B — deduplication

| Duplicate | Measured | Act |
|---|---|---|
| **The decisions triple store** — 64 `decisions/*.md` files, a 5,686-line `data/decisions/decision_register.yaml`, and **166 DB rows**, held equal in both directions by `test_db_integrity` L01. An L2 check whose whole function is keeping a duplicate alive | live count | **Not deletable as the cull plan assumed.** The YAML has **9 code referents** including `decision_capture.py` and `doctrine_recheck.py`. **Strike cull item D2 as scoped and re-scope it:** the question is which of the three is canonical, and that is a doctrine call — owner |
| **29 DOIs are held under more than one `source_locators` row** — 441 rows carry 397 distinct DOIs. The stash duplicates itself, and **R9 cannot see this either**, because it is the same blindness Phase 1 fixes | live query | **Fold into Phase 1.** Once R9 reads `source_locators`, point it at intra-stash duplicates too, then dedupe by migration |
| **Four items, fourteen costumes** (§7.1) — one open item each, specified three or four times | referent audit | **Act A6** folds all four into DR §3 step 6 |

### 6.4 Workstream C — wiring

The pipeline map (`governance/pipeline-map.yaml`) is the instrument and is current — its six false
assertions were corrected 2026-08-22 and BRK-25 was REFUTED rather than "fixed", which would have
reverted ratified doctrine via migration 029.

**What wiring work remains is not mapping. It is connecting or cutting.** Every item in §6.2 is a
wiring verdict: a view with no reader is an unconnected edge, and so is a table with no writer. **Do
not produce another map.** A third map of the same wiring would be the L3 defect exactly.

### 6.5 Workstream D — the write path

**Ruled and settled, recorded so it is not re-specified a fourth time.** DR §12.0 ruled the write
path is a **session-scoped scratch DB**, not `--emit-sql`. The nine `db.py` writer helpers were
specified in the writer plan Phase 2, the walk plan Phase 7 and DR §12.5, and **none exists; batch 2
ran without them and shipped.** `scripts/db.py` still cannot write `search_candidates`,
`evidence_population_match`, `economics_entries`, `case_studies` or `jurisdictional_values` values,
and `add-source` cannot write `doi_resolution_outcome`, `url`, `pages`, `first_author_last` or author
rows — those need hand SQL against the scratch.

**Do not build the helpers.** That gap is where the 2026-08-19 fabrication entered, but the fix that
worked was `retrieval_log.py --verify-authors` diffing stored data against the retrieved bytes — an
**L1 check with a real L0 subject** — not a writer. **If a helper is ever built, it must be because a
batch was blocked by its absence.** Two batches were not.

### 6.6 Workstream E — checks, and why not to route to a number

**63 active, 4 quarantined, against the cull plan's declared target of 9.** No phase routes from 63
to 9, which has been true since 2026-08-18 and has not moved.

**Do not write a routing plan.** A document that routes 63 to 9 is an L3 artifact about L1/L2
artifacts, and producing it is the behaviour this whole program exists to stop. **The method is
CLAUDE.md §1: delete a check when you have evidence it is vacuous, unreferenced or superseded —
one at a time, evidence in the commit, no owner gate.** The number falls as a consequence.

**One prerequisite measurement, and it is cheap:** re-run the empty-subject census. The census found
16 of 65 checks examined nothing, with the blocking ones split between *dormant* (guarding corpora
the 2026-08-06 reset emptied) and *defective*. **That split is the cull list.** A dormant check
guarding a corpus batch 3 will populate must stay; a check guarding a corpus that no longer exists
must go. Derive it with `run_checks.py --explain` over a full scope and read the `EXAMINED:` lines —
**a blocking check that passes on zero subjects is CLAUDE.md §2(a), the failure mode produced four
times here.**

### 6.7 Workstream F — L3 prose

The census measured the L3 stratum at ~46,500 lines of live workplan prose against **471 lines of
primary deliverable**. Live workplan is now **31,942** lines and the deliverable has not grown.

**Acts A4 (13 files, 4,065 lines) and A6 are the whole of the sanctioned L3 reduction**, because they
are the only parts with referent evidence. The remaining L3 mass retires under OD-8 once its
referents are re-pointed — **not on this session's authority.** `workplan/deprecated/` remains
outside `.ignore`, and that edit is **owner-gated by that file's own header and DR-2026-08-06**;
three plans have now scheduled something no session could perform.

### 6.8 Order, and the one rule that governs it

**Cull upward from L3. Never downward from L0.**

1. **A4** — the 13-file L3 directory. Referent evidence complete; no owner gate.
2. **The two dead registries** — 25,979 lines, zero code referents. Sweep the prose, then delete.
3. **The unread views** — one migration, after reading `skills/*_SKILL.md` for prose callers.
4. **The empty-subject census** — derive it; it *is* the check cull list.
5. **Then stop.** Everything below this line is owner-gated (the dormant tables, the decisions
   triple store, OD-8, `.ignore`) or is L0 and must not be touched.

**Acceptance for Phase 4 — every one is a subtraction, and none is a document:**
- The unread-view count falls from 11, by migration, with the reader scan in the commit.
- `references/claim-reference-join.json` and `global-reference-registry.json` are gone and no live
  file names them.
- The empty-subject census exists as check-registry annotations — **not as a new file**.
- Cull item D2 is struck and re-scoped as an owner question.
- **Net lines removed exceed net lines written. If this phase produces more prose than it deletes,
  it has failed on its own terms and must be abandoned rather than continued.**

---

## 7. The standing state of the workplan surface

So the next session does not re-audit it. **32 live files were authored inside the ten-day window —
45% of the entire live workplan surface, 11,747 lines, against the window's 132 DB rows.**

| Disposition | n | Files |
|---|---|---|
| **KEEP-OPERATIVE** | 2 | `2026-08-22-agonist-antagonist-execution-plan.md` (4/7 acts, 5–6 blocked) · `2026-08-20-adversarial-adjudication-a18-aut.md` (ruling stands; §8 3.5/6) |
| **RETIRE** → A4 | 13 | `execution-plan-2026-08-12/**` |
| **SPENT** — retire after A6 re-points citations | 12 | 08-19 critique (absorbed) · 08-18 restart plan (absorbed) · 08-18 handoff (**1/10**) · 08-18 frame proposal (**0 build items**) · 08-18 census · 08-18 model-substitution log · 08-17 consolidated (**~1/45**) · 08-16 critique · 08-15 PR103 brief · 08-14 execution plan + remediation workplan (Track C **lapsed**) · 08-13 writer plan (**0/5 phases**) |
| **PARTIALLY-EXECUTED** | 2 | 08-18 cull plan (**~15% ran**; Phase 1's `.ignore` edit is **owner-gated and was never a session act** — three plans scheduled it anyway; Phase 4a was selected by a blind instrument) · 08-20 provenance walk (**2/5 by its own honest scorecard**) |
| **RECORDS**, complete | 2 | 08-12 step-R rename · 08-21 reasoning-doc digestion |
| This file | 1 | deleted by §7 |

**The 40 out-of-window files are out of scope.** Eight were touched by sweeps; none was authored or
advanced. Do not enumerate them again.

### 7.1 Four items, fourteen costumes
The finding that justifies A6. Each is **one** open item, specified three or four times, none built
— and **14 of the 15 citations were written inside the same ten days.** The duplication was not
inherited; it was manufactured, at speed, by sessions that did not check whether the thing had
already been specified.

| Item | Specified in | Built |
|---|---|---|
| `jurisdictions` / `languages` tables | frame proposal §3/§11 · handoff §6 step 5 · digestion D-4 | no |
| `db.py` write helpers | writer plan Phase 2 · walk plan Phase 7 · DR §12.5 | no — batch 2 has run and did not automate them |
| `GB` → `UK` | handoff §6.4 · 08-19 critique §7.7 · frame proposal §10.4 · 08-14 I-20 | no — **and A5 says do not** |
| OD-5 | digestion · A-18 adjudication §8.6 · walk plan · 08-22 F-18 | **A1 builds it** |

---

## 8. Owner decisions outstanding

**Critical path:** the **population-taxonomy pass (D-0165)**. Its packet should carry two things
this window produced and deliberately did not action: the DoD gate printing PASS over empty subject
sets, and **A-18's empty `item_population_links` set** — the second *is* the taxonomy question.

**Off the critical path, none blocking §3–§5:** **OD-D** (REF-00965 / REF-00968 tier re-grade —
both still Tier 1 in the DB) · **OD-F** (adversarial-subject waiver) · **OD-G** (strike DR §12.1
step 10's `jurisdictional_values` clause; the STOP notice is only an interim guard) · **OD-2**
(five-bucket ratification and the `jurisdiction-philosophy.md` §2.3 amendment) · **OD-9** (the
required-check set) · the **`.ignore` entries**, owner-gated by that file's own header and
DR-2026-08-06.

---

## 9. Traps that were hit in this window

1. **`db.py log-mining --ref` takes the LOCAL id.** Cost: a blocking gate reporting a violation for
   work actually done.
2. **Three decision field formats written from memory** — `status` has no `ADOPTED`;
   `model_routing` must match `{model}/{effort}/{purpose}`; `effort_level` is INTEGER;
   `decision_date` is `YYYY-MM-DD HH:MM`. Cost: two compensating migrations. **Read the CHECK
   constraint; do not recall it.**
3. **`search_candidates.title` is NOT NULL** — which is what forced two real titles to be retrieved
   rather than invented, and is how Finitzo-Hieber & Tillman 1978 was identified. The constraint
   did the epistemic work.
4. **A year inferred from a DOI slug was wrong by one.** The payload is in hand; read it.
5. **`grep … || echo "none — clean"` accepted as proof** when the grep had failed on a *missing
   file*. An absent artefact is not a clean result.
6. **`emit_batch_sql` reads a PK change as a deletion** and correctly refuses; use hand SQL.
7. **Never schedule self-check-ins.** Standing owner instruction, given emphatically, twice.
8. **`.ignore` hides frozen records from ripgrep** — "no matches" is not "not present."

---

## 10. Acceptance, termination, and how this file ends

**Acceptance.**
1. `research_batch_dod.py` R9 prints an `EXAMINED` count including `source_locators`, and
   `--selftest` prints **15/15**.
2. Forward mining is recorded for every anchor, empties kept.
3. **At least one of `GAP-B01-001` / `GAP-B02-001` is closed by an actual read of the sources.**
4. `governance/check-registry.yaml` parses with no phantom keys and carries no count or status claim
   in any battery description.
5. In-window live workplan files fall **32 → 19**; total live **72 → 59**; **18 / 58** after §10.1.
6. §7.1's four items appear **once each**, at DR §3 step 6.
7. The unread-view count falls from **11**, by migration, with the reader scan recorded in the
   commit; the two dead reference registries (**25,979 lines**) are gone and no live file names them;
   the empty-subject census exists as check-registry annotations and **not** as a new file.
8. **Zero new checks, scripts, tables or plans exist as a result of executing this document.**
9. **Phase 4 removes more lines than it writes.** If the cull program produces more prose than it
   deletes, it has failed on its own terms and is abandoned, not continued.

**Termination — DR §11 property 5.** A session committing anything other than fixes, record
corrections, search logs, migrations, or a rendered determination has failed. A1 is a fix; Phase 2
is search logs and migrations; A2–A7 and Phase 4 are record corrections, migrations and deletions.
**This file is the only thing here that is none of those five kinds.**

**The one rule that outranks the rest of Phase 4:** cull upward from L3, never downward from L0. A
session that finds itself deleting L0 substance — evidence, items, populations, the code that reads
and writes them — has inverted the program and must stop.

### 10.1 Self-retirement
When Phases 1–4 are done, **delete this file** — not to `_archived/`. The durable outputs are the
widened R9 gate, the batch-03 migrations and session record, the corrected registry, the amended DR
§3/§8/§B, and the archived directory. **If any act is still open, leave the file and strike the acts
that are done**, so what remains is visibly shorter than what was planned.

*A plan that survives its own execution has become the thing it was written to remove.*

**What this plan is honest about not doing.** It does not move `specifications` off zero. Nothing a
session can do moves it, because every determination route runs through the owner-gated
population-taxonomy pass. **The deliverable is blocked on one decision, and 11,747 lines of live
workplan is what ten days built while it waited.**
