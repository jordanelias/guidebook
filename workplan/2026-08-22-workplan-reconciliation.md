# 2026-08-22 — Workplan reconciliation, scoped to 2026-08-12 → 2026-08-22

**This document is written to be deleted.** §7.3 gives the condition. Every act in §5 is a
deletion, a one-line correction, an in-place amendment, or a fix that makes an existing gate examine
the right set. **No act authors a new plan, check, table or script.** A session that extends this
file rather than executing it has reproduced the defect it was written to remove.

**Scope — owner instruction, 2026-08-22.** This plan is derived from the **ten-day commit window
2026-08-12 → 2026-08-22** (126 non-merge commits) and from the repository's live state. Earlier
material is **out of scope and is not enumerated here.** That instruction is not a convenience: the
measurement in §1 shows the window is where the surface was manufactured, so scoping to it loses
nothing that is live and drops 40 files that were only ever swept, never worked.

**Owner ruling, same date, folded in:** `workplan/bpc-rewrite-workplan-2026-05-11.md` and
`workplan/best-practices-assessment-system.md` are **100% superseded and can be ignored.** An
earlier revision of this file raised both as doctrine-carrying concerns. **They are not concerns.
Do not re-raise them.** Both are out-of-window in any case; the ruling is recorded so the next
session does not rediscover them and file the same non-finding a third time.

**Method.** Two Fable 5 read-only audits (workplan inventory; the commit window), then independent
verification by me of every figure this plan acts on — DB queries, `git ls-files`, `git log
--diff-filter`, YAML parses, and an exhaustive referent scan over every tracked file. Completion
states are derived from the repository, **not from what the plans claim about themselves.** Where a
plan's self-report and the evidence disagree, the disagreement is recorded.

---

## 1. The measurement

Derived 2026-08-22. Re-derive before citing; CLAUDE.md §2(b) applies to this file as to any other.

| | In the ten-day window | Out of window |
|---|---|---|
| Live `workplan/` files | **32** | 40 |
| Live `workplan/` lines | **11,747** | 20,197 |
| Files **authored** in the window | **36** | — |
| Of those, already retired inside the window | **4** (all archived 2026-08-19, `3e1dfc1`) | — |

**Forty-five percent of the entire live workplan surface was written in ten days.** The 40
out-of-window files were *touched* in the window — eight of them, by vocabulary and path sweeps —
but none was authored or advanced. They are history, and this plan treats them as history.

Against those 11,747 lines, the window produced **132 rows** for the deliverable: 10 evidence
sources on one parameter, 18 logged searches, 44 screened candidates, 25 population grades, 7
citation-mining rows, 10 slug links, 5 gaps, 3 decisions. **`specifications` is 0.**

The commit ledger for the same period: **+12,059 lines of apparatus prose against +4,226 of content
and evidence** (2.9:1); **17 of 76 substantive commits — 22% — corrected the window's own errors**;
executable code *fell* by 5,811 lines from a real cull. **The code is being disciplined. The prose
is not.**

### 1.1 The finding that matters

Not "32 files." This: **across those in-window files, four distinct pieces of work are each
specified three or four times, and none is built.**

| Item | Specified in (all in-window unless marked) | Built |
|---|---|---|
| `jurisdictions` / `languages` vocabulary tables | frame proposal §3/§11 · handoff §6 step 5 · digestion "Next" 3 (D-4) | **no** — tables absent |
| `db.py` write helpers (`add-authors`, `next-ref-id`, `add-match`, `finish-search`) | writer plan Phase 2 · walk plan Phase 7 · DR §12.5 | **no** — batch 2 has run and did not automate them |
| `GB` → `UK` in `jurisdictional_values` (20 rows) | handoff §6 step 4 · 08-19 critique §7 item 7 · frame proposal §10.4 · 08-14 I-20 | **no** — and §5 Act 4 argues it should not be |
| OD-5: R9 duplicate gate blind to `source_locators` | digestion "Next" 1 · A-18 adjudication §8 item 6 · walk plan · 08-22 plan F-18 | **no** — `GAP-B01-004` is held open by it |

Rescoping to the window does not weaken this; it sharpens it. **Fourteen of the fifteen citations
above were written inside the same ten days.** The duplication was not inherited. It was
manufactured, at speed, by sessions that did not check whether the thing had already been specified.

---

## 2. Disposition register — all 32 in-window files

Every in-window live file appears exactly once. **The 40 out-of-window files are out of scope by
owner instruction and are deliberately not listed** — enumerating them is the behaviour this plan
exists to stop.

### 2.1 KEEP-OPERATIVE — 2

| File | State | What remains |
|---|---|---|
| `2026-08-22-agonist-antagonist-execution-plan.md` | 4 of 7 acts done; acts 5–6 **BLOCKED** by D-0165; 3 of 7 owner decisions answered | Acts 5–6; OD-D, OD-F, OD-G. **Owes itself a scorecard** — its §6 requires one *in that file* before archival; none has been appended. → Act 7 |
| `2026-08-20-adversarial-adjudication-a18-aut.md` | **Executed as a ruling.** The refusal stands; DR §3 step 5 was amended 2026-08-22 to honour it | §8: 3.5 of 6 done. Open: retrieve Greenland 2026; OD-D; OD-5 |

### 2.2 RETIRE NOW — 13 files, 4,065 lines, referentially closed

**`workplan/execution-plan-2026-08-12/` — the whole directory.** Its own status line reads
*"PROPOSED. Nothing in this directory has been executed."* Verified independently by three
structural probes: Wave L's `work_log` table is absent, Wave 3's `locator_schemes` is absent, and
Wave H is undone — **28 of 93 `items.name` still contain digits** (live query). Its parent authority
already sits at `_archived/workplan/2026-08-12-resolution-plan.md`, so
`00-holistic-execution-plan.md:15` is a live file citing a dead path.

**What makes this the only directory that qualifies:** the referent scan shows it is
**referentially closed.** Every member's referrers are its own twelve siblings, with exactly two
exceptions:

- `governance/retired-vocabulary.yaml:105` — a *comment* naming the directory as "the live example"
  of the `workplan/*20??-??-??*/**` exempt glob. The glob is a pattern and stays valid; only the
  comment goes stale. **Comment edit, no functional change.**
- `workplan/2026-08-16-adversarial-critique-and-execution-plan.md:55` — a table row citing
  `4-adjudication-apparatus.md`. That file is itself SPENT (§2.3), and the row is a historical
  finding *about* a path, not a dependency on it.

**No other live workplan file has zero referents.** Nothing else moves blind. This is the specific
permission that a blanket caution — *"the remaining 54 cannot be archived until their referents are
re-pointed"* — had been overriding for four days. CLAUDE.md §1 names that inversion as the ratchet.

### 2.3 SPENT — 12, retire after Act 5 re-points their citations

Absorbed, discharged, or overturned. Nearly all remaining citations come from
`decisions/DR-2026-08-19-research-restart-operative-instrument.md` §B — the supersession table,
which *records* their supersession rather than depending on them.

| File | Evidence of state |
|---|---|
| `2026-08-19-adversarial-critique-research-restart.md` | ABSORBED — F1–F9 became DR §B; 6/10 of its sequence executed; **the two items it forbade were correctly not run** |
| `2026-08-18-research-restart-plan.md` | ABSORBED into DR §12; its batch has now run twice |
| `2026-08-18-handoff-next-session.md` | **1 of 10 steps executed**; §6 spine overturned by DR §3 |
| `2026-08-18-research-frame-proposal.md` | Rulings stand; **0 build items executed** — no `jurisdictions`, `research_bodies`, `research_indexes`, `icf_codes`; `axes` intact |
| `2026-08-18-structural-census-and-cull-list.md` | Evidence, partially refuted on contact (keep-set 54 not 10; movable 38 not 77) |
| `2026-08-18-model-substitution-log.md` | SPENT — debt discharged |
| `2026-08-17-consolidated-action-plan.md` | **~1 of 45 items executed** |
| `2026-08-16-adversarial-critique-and-execution-plan.md` | Findings stand, sequencing dead |
| `2026-08-15-adversarial-brief-pr103.md` | DISCHARGED, with a recorded deficit: no verdict on claims 2, 5, 6, 7, 8 |
| `2026-08-14-execution-plan.md` + `2026-08-14-remediation-workplan.md` | Track A and part of D executed; Track C 061–066 **LAPSED**; `ratification_sweep_audit.py` never built |
| `2026-08-13-writer-plan.md` | **0 of 5 phases**; Phase 1 explicitly re-decided the other way by DR §12.0 |

**Two SPENT files sit in DR §8's mandatory four-document read-set** — the restart plan and the
handoff — so every fresh session is sent to read a spent procedure and an overturned sequence. Act 5
fixes that at the DR, where it is one edit.

### 2.4 PARTIALLY-EXECUTED — 2

| File | State |
|---|---|
| `2026-08-18-cull-execution-plan.md` | **~15% ran** (23 files / 6,716 LOC deleted, registry 66→63, quarantine 16→4, 38 files archived, Phase 0 record corrections finally landed 2026-08-22). **Most of the remainder is not a session act:** Phase 1's `.ignore` edit is owner-gated by that file's own header and DR-2026-08-06, and Phase 4a was selected by a blind instrument — it culls a script invoked from *skill prose*, invisible to any call-graph. **Three plans scheduled the `.ignore` edit; none of them could have performed it.** |
| `2026-08-20-provenance-walk-execution-plan.md` | **2 of 5 by its own §11 scorecard** — the honest self-score is the point. Its §4.3 determination is INVALIDATED in-file by BRK-20; its forward sections are doubly superseded |

### 2.5 RECORDS — 2, complete, no action

`2026-08-12-step-R-rename-execution-record.md` (the `cell`→`specification` rename; D-0158/D-0159) ·
`2026-08-21-reasoning-doc-digestion.md` (27 leads written and one bad write retracted the same
session — 1 of its 3 next-steps done, and the load-bearing one is OD-5, → Act 6).

### 2.6 This file

`2026-08-22-workplan-reconciliation.md` — deleted by §7.3.

---

## 3. Conflicts still live

Eight were found in the window; five are resolved and recorded. **Three remain.**

1. **`governance/check-registry.yaml` contradicts itself in one file.** Line 171 asserts
   `DB content integrity (35 checks). Red on main - see tooling-register 4.` while the check-level
   note was corrected on 2026-08-22 to *72/72 checks pass*. Two lines, one file, opposite claims —
   **CLAUDE.md §2(b), inside the file that inventories every gate.** → Act 3
2. **R-12 — filed 2026-08-11, refiled 2026-08-18 as cull §15.6 item 1, never fixed.** The
   `governance` battery description is unquoted YAML containing commas, so it parses as
   `{'deps': ['pydantic'], 'description': 'Decision protocol', 'doctrine recheck': None, 'adversarial-use.': None}`
   — two phantom keys where a description should be. Verified live today. Its *content* is stale
   too: it advertises a "doctrine recheck" that OD-10 abolished on 2026-08-19. → Act 2
3. **`DR-2026-08-06` §3 vs. live state.** Its rescue rationale for `jurisdictional_values` cites
   "109/109 on `source_section`"; the 2026-08-12 clearing made that **0/109**. DR-2026-08-19 §1.5
   proposed annotating it; `git log` shows the file untouched since. → Act 5, as a dated forward
   note. **Annotate, never rewrite** — a DR records what was decided on its date.

Resolved in-window, requiring nothing: DR §3 step 4/5 vs. the walk session record (amended in place
2026-08-22); DR §12.1 step 10 vs. the REFERENCE-ONLY ruling (STOP notice in place, strike is OD-G);
BRK-25 vs. BRK-26 (BRK-25 REFUTED, BRK-26 fixed); the adversarial-subject rule vs. practice
(deviation F-9, waiver is OD-F); restart-plan criterion 6 vs. handoff §6 (criterion struck).

---

## 4. What is owner-gated, and what is not waiting on it

**Owner-gated, on the critical path:** the **population-taxonomy pass (D-0165)**. It blocks acts 5–6
of the 08-22 plan, the first determination, and therefore `specifications` moving off zero. **It is
the only thing in this repository whose absence stops the deliverable.**

**Owner-gated, off the critical path:** OD-D (REF-00965/00968 re-grade — both still Tier 1 in the
DB), OD-F, OD-G, OD-2 (five-bucket ratification and the `jurisdiction-philosophy.md` §2.3
amendment), OD-9. **Also owner-gated: the `.ignore` entries** — see §2.4.

**Nothing in §5 waits on any of them.** That is the test this plan had to pass to be worth writing.

---

## 5. Execution

Ordered by cost. Acts 1–3 are one commit. Act 6 is the one that moves research.

### Act 1 — Retire `workplan/execution-plan-2026-08-12/`
**Location:** `workplan/execution-plan-2026-08-12/` → `_archived/workplan/execution-plan-2026-08-12/`
(13 files, 4,065 lines). `_archived/` is the right home for retired *content* and is ratified as
permitted to grow (2026-08-19).
**Do:** `git mv` the directory, then the two referent edits named in §2.2 — correct the
`retired-vocabulary.yaml:105` comment (**keep the glob**; it is a pattern, and removing it would
un-exempt any future dated plan directory), and repoint the path in the 08-16 plan's table row.
**Evidence for the commit:** referentially closed (12 sibling referrers + 2 external, both edited);
0% executed by three independent structural probes; parent authority already archived.
**Falsification:** re-run the referent scan after the move. If any tracked file outside `_archived/`
still names a member file, the sweep is incomplete and Act 1 is not done — CLAUDE.md §0.4. **The
scan cannot see prose callers**; read `skills/*_SKILL.md` directly, because that exact blindness is
what made cull Phase 4a unsafe.

### Act 2 — Fix R-12
**Location:** `governance/check-registry.yaml`, `batteries: governance:`.
**Do:** quote the description so it parses as one string, and drop "doctrine recheck" (abolished by
OD-10, 2026-08-19).
**Verify:** `python3 -c "import yaml;print(yaml.safe_load(open('governance/check-registry.yaml'))['batteries']['governance'])"`
must print exactly two keys — `deps` and `description`.
**Why this is not apparatus:** it removes two phantom keys from the file that inventories every
gate. Nothing is added. Open 11 days, named twice, one line.

### Act 3 — Correct the `db_integrity` battery description
**Location:** `governance/check-registry.yaml:171`.
**Do:** remove the count and the status claim. **Do not substitute a fresh number** — CLAUDE.md
§2(b): a hardcoded count in a derived document is the defect, not the stale value. The check-level
note corrected on 2026-08-22 already carries the measurement.

### Act 4 — Strike `GB` → `UK`, do not execute it
**Locations:** `workplan/2026-08-18-handoff-next-session.md` §6 step 4 ·
`workplan/2026-08-19-adversarial-critique-research-restart.md` §7 item 7 ·
`workplan/2026-08-18-research-frame-proposal.md` §10.4.
**Do:** strike the item in each with a dated note giving the reason. **Write no migration.**
**Reason — this reverses four in-window plans:** `GB` is the ISO 3166-1 alpha-2 code for the United
Kingdom; `UK` is not an ISO code. The change was specified to align with a `jurisdictions` table
that does not exist and is not due until DR §3 step 6. Meanwhile `jurisdictional_values` is under
the owner's REFERENCE-ONLY quarantine — **a write to it on 2026-08-21 was caught by blocking L02 and
retracted the same session.** So the act is premature, its justification is unbuilt, and its
direction is probably wrong. **Four plans scheduled it in ten days and not one asked whether it was
correct.** It goes to the taxonomy pass; it is a naming decision, which is the owner's.

### Act 5 — Reconcile at the DR, not in a new document
**Location:** `decisions/DR-2026-08-19-research-restart-operative-instrument.md`. Amend **in place**,
on the precedent its own 2026-08-22 amendment set, stating the same reason (§5's reversal clause
makes correcting the instrument cheaper than succeeding it).
- **§8 read-set:** mark the restart plan and the handoff *read as history* **at the citation**, not
  in a caveat further down. A session reading a mandatory read-set does not reliably reach the
  paragraph that qualifies it.
- **§3 step 6:** fold §1.1's four items into the step that already owns their territory, with their
  locations. **One open item each, named once.**
- **§B:** add the §2.2–2.5 dispositions, so the supersession table is the single index.
**Then:** append a dated forward note to `decisions/DR-2026-08-06-clean-room-evidence-reset.md` §3
recording that its "109/109 on `source_section`" is now 0/109. **Annotate; do not rewrite.**

### Act 6 — OD-5: make the R9 gate see the stash
**Location:** `scripts/audit/research_batch_dod.py`, the R9 duplicate check.
**Defect:** it queries `evidence_sources` (10 rows) only and is blind to `source_locators`
(**835 rows**) — the lead index that exists precisely to hold identifiers the project already holds.
Batch 02 ran the stash check **by hand** because the gate could not.
**Why this is the highest-value unblocked act:** it is not new apparatus. It is CLAUDE.md §2(a) —
*a gate that passes having examined nothing* — in the one battery guarding research admissions. It
holds `GAP-B01-004` open, four in-window documents name it, and it demonstrated itself three times
in a single batch, once by surfacing Finitzo-Hieber & Tillman 1978 through backward mining after R9
had passed the same DOI space clean.
**Do:** widen the R9 query to `source_locators`; keep `EXAMINED:` printing the true subject count.
**Falsification:** re-run against batch 02's session. If R9's `EXAMINED` count does not rise above
the `evidence_sources` figure, the widening did not take. Then `--selftest` must still print 15/15.
**Then close `GAP-B01-004`** by migration, or record in the gap row why it stays open.

### Act 7 — Score the 08-22 plan; do not archive it
**Location:** `workplan/2026-08-22-agonist-antagonist-execution-plan.md`.
Its §6 requires a scorecard *in that file* before archival and none exists. **Append it:** acts 0–4
done (act 3 with its recorded deviation), acts 5–6 blocked by D-0165, 3 of 7 owner decisions
answered, acceptance 4 undeterminable because both sides of the ledger it defined changed shape.
**Do not archive** — acts 5–6 are blocked, not finished, and archiving a blocked plan loses the
block.

**Deliberately not in this plan:** the DoD gate printing PASS over empty subject sets, and A-18's
empty link set. Both belong in the D-0165 packet — the first needs a determination to have a
subject, the second *is* the taxonomy question.

---

## 6. Acceptance, termination, and how this file ends

**Acceptance.**

1. **In-window live workplan files fall from 32 to 19** (Act 1 removes 13), and total live falls
   from 72 to **59**. After §7.3, **18 and 58**.
2. `governance/check-registry.yaml` parses with no phantom keys and carries no count or status claim
   in any battery description.
3. `research_batch_dod.py` R9 prints an `EXAMINED` count that includes `source_locators`, and
   `--selftest` still prints 15/15.
4. §1.1's four items appear **once each**, at DR §3 step 6.
5. **Zero new checks, scripts, tables or plans exist as a result of executing this document.**

**Termination.** DR §11 property 5: a session committing anything other than fixes, record
corrections, search logs, migrations, or a rendered determination has failed. Acts 1–5 and 7 are
record corrections and one archival move; Act 6 is a fix. **This file is the only thing here that is
none of those five kinds, which is why §6.1 exists.**

### 6.1 Self-retirement
When acts 1–7 are done, **delete this file** — not to `_archived/`. It is scaffolding, not
reader-facing content, and git is the archive for scaffolding (CLAUDE.md §1). The durable outputs
are the amended DR §3/§8/§B, the corrected registry, the widened R9 gate, and the archived
directory. **If any act is still open, leave the file and strike the acts that are done**, so what
remains is visibly shorter than what was planned. *A reconciliation document that survives its own
reconciliation has become the thing it was written to remove.*

**What this plan is honest about not doing.** It does not move `specifications` off zero. Nothing a
session can do moves it, because every determination route runs through the owner-gated
population-taxonomy pass. **The deliverable is blocked on one decision, and 11,747 lines of live
workplan is what ten days built while it waited.**
