# 2026-08-22 — Workplan reconciliation: what is live, what is spent, and the four items that are real

**This document is written to be deleted.** It is the 72nd file in a directory of 71, and that is
the finding it exists to act on, not an irony it is unaware of. Its §7 gives the condition under
which it is removed, and every act in §5 is either a deletion, a one-line correction, a migration,
or a code fix that makes an existing gate examine the right set. **No act in this plan authors a
new plan, a new check, a new table or a new script.** If a future session finds itself extending
this file rather than executing it, that session has reproduced the defect.

**Method.** Two Fable 5 read-only audits (workplan inventory; the 2026-08-15 → 2026-08-22 commit
window), then independent verification by me of every figure this plan acts on. The completion
states below are derived from the repository — DB queries, `git ls-files`, YAML parses, an
exhaustive referent scan over every tracked file — **not from what the plans claim about
themselves.** Where a plan's self-report and the evidence disagree, the evidence is recorded and
the disagreement is named.

---

## 1. The measurement

Derived 2026-08-22. Re-derive before citing; §2(b) of CLAUDE.md applies to this file as to any other.

| | |
|---|---|
| Live `workplan/` files | **71** (58 top-level + 13 in `execution-plan-2026-08-12/`) |
| Live `workplan/` lines | **31,617** |
| Frozen alongside | 20 `_superseded/`, 16 `deprecated/`, 38 `_archived/workplan/` — 26,064 lines |
| Rows the deliverable gained in the audited week | **132** (10 sources, 18 searches, 44 candidates, 25 population grades, 7 mining, 10 slug links, 5 gaps, 3 decisions) |
| `specifications` | **0** |

The week's ledger, from the commit audit: **+12,059 lines of apparatus prose against +4,226 lines
of content and evidence**, a 2.9:1 ratio; **17 of 76 substantive commits (22%) corrected the
week's own errors**; net executable code *fell* by 5,811 lines because of a real cull. So the code
is being disciplined and the prose is not. **`workplan/` is where the recursion now lives.**

The number that matters is not 71. It is this: across those 71 files, **four distinct pieces of
work are each specified between three and four times, and none of the four has been built.**

| Item specified repeatedly | Specified in | Built |
|---|---|---|
| `jurisdictions` / `languages` vocabulary tables | 08-02 plan · frame proposal §3/§11 · handoff §6 step 5 · digestion "Next" 3 (D-4) | **no** — tables absent |
| `db.py` write-path helpers (`add-authors`, `next-ref-id`, `add-match`, `finish-search`) | writer plan Phase 2 · walk plan Phase 7 · DR §12.5 | **no** — batch 2 has run and did not automate them |
| `GB` → `UK` in `jurisdictional_values` (20 rows) | handoff §6 step 4 · 08-19 critique §7 item 7 · frame proposal §10.4 · 08-14 I-20 | **no** — and §5 Act 4 argues it should not be |
| OD-5: R9 duplicate gate blind to `source_locators` | digestion "Next" 1 · A-18 adjudication §8 item 6 · walk plan · 08-22 plan F-18 | **no** — `GAP-B01-004` is held open by it |

Re-specifying a thing is not progress toward it. **Four open items are wearing fourteen costumes.**

---

## 2. Disposition register — all 71 live files

Five dispositions. **RETIRE** = move to `_archived/workplan/` (content archival, owner-ratified
2026-08-19 as permitted and growing). **KEEP-LOAD-BEARING** = other files depend on it; moving it
breaks them. **KEEP-OPERATIVE** = it still directs work. **SPENT** = its work is done or absorbed;
retire once its citations are re-pointed. **HISTORICAL** = frozen record, harmless, low priority.

### 2.1 KEEP-OPERATIVE — 2 files

| File | State | What remains |
|---|---|---|
| `2026-08-22-agonist-antagonist-execution-plan.md` | **4 of 7 acts done**; acts 5–6 BLOCKED by D-0165; 3 of 7 owner decisions answered | Acts 5–6; OD-D, OD-F, OD-G. **Owes itself a scorecard** — its own §6 says "scored the same way, in this file, before it is archived"; none has been appended. |
| `2026-08-20-adversarial-adjudication-a18-aut.md` | **Executed as a ruling.** The refusal stands and DR §3 step 5 was amended 2026-08-22 to honour it | §8 items: 3.5 of 6 done. Open: retrieve Greenland 2026; OD-D; OD-5. |

### 2.2 KEEP-LOAD-BEARING — 6 files, do not move

Referent counts are from an exhaustive scan of **every tracked file** for the literal path and the
bare filename, with frozen zones (`_archived/`, `sessions/`, `audits/`, `versions/`,
`references/search-log/`, `workplan/_superseded/`, `workplan/deprecated/`) counted separately.

| File | Live referents | Note |
|---|---|---|
| `best-practices-assessment-system.md` | **108** | The most-cited document in the repository. Untouchable until its content is relocated, which is not this plan's business. |
| `ratification-execution-register-2026-07-13.md` | **18** | Cited by 8+ attestations and DRs. |
| `bpc-rewrite-workplan-2026-05-11.md` | **11** | Its B-before-E gate is cited as *live doctrine* by DR §12.5 and restart-plan §6.5. **STALE-BUT-CITED: doctrine is being carried by a May workplan.** See §6. |
| `search-coverage-completion-workplan.md` | 3 + **2 code** | Cited at runtime by `scripts/db.py:294,317,572` in the `FrozenGridError` message. Archiving it breaks a live error message. |
| `website-v0-path-forward-2026-07-12.md` | 5 | Website architecture lock. |
| `multilingual-search-remediation.md` | 4 | Cited by `skills/adversarial-research_SKILL.md` — a **prose caller**, invisible to any call-graph. This is the class of defect that blocked cull Phase 4a. |

### 2.3 RETIRE NOW — 13 files, 4,065 lines, referentially closed

**`workplan/execution-plan-2026-08-12/` — the whole directory.** Fable's verdict: *"DEAD/SUPERSEDED,
essentially 0% executed"*; its own status line reads *"PROPOSED. Nothing in this directory has been
executed."* Verified independently: its Wave L `work_log` table is absent, its Wave 3
`locator_schemes` is absent, and its Wave H (strip determinations from item names) is undone —
**28 of 93 `items.name` still contain digits**, live query. Its parent authority already lives at
`_archived/workplan/2026-08-12-resolution-plan.md`, so `00-holistic-execution-plan.md:15` is a live
file citing a dead path.

**The evidence that makes this cheap, and the reason it is the only directory that qualifies:** the
referent scan shows the directory is **referentially closed**. Every file's only referrers are its
own twelve siblings, with exactly two exceptions:

- `governance/retired-vocabulary.yaml:105` — a *comment* naming the directory as "the live example"
  of the `workplan/*20??-??-??*/**` exempt glob. The glob is a pattern and stays valid; only the
  comment goes stale. **Comment edit, no functional change.**
- `workplan/2026-08-16-adversarial-critique-and-execution-plan.md:55` — a table row citing
  `4-adjudication-apparatus.md`. That file is itself SUPERSEDED (§2.4) and its citation is a
  historical finding about a path, not a dependency.

**No other live workplan file has zero referents.** Nothing else can be moved blind. This is the
answer to cull §16 remedy 3 — *"the remaining 54 cannot be archived until their referents are
re-pointed"* — which is true in general and false for this directory specifically. **A blanket
caution beat a specific permission for four days; CLAUDE.md §1 names that as the ratchet.**

### 2.4 SPENT — 14 files, retire after §5 Act 5 re-points their citations

Absorbed, discharged, or overturned. Each is still cited, almost entirely by
`decisions/DR-2026-08-19-research-restart-operative-instrument.md` §B, which is the supersession
table — a citation that *records* supersession, not one that depends on the file.

`2026-08-19-adversarial-critique-research-restart.md` (ABSORBED — F1–F9 became DR §B; 6/10 of its
sequence executed; the two items it forbade were correctly not run) ·
`2026-08-18-research-restart-plan.md` (ABSORBED into DR §12; batch has run twice) ·
`2026-08-18-handoff-next-session.md` (**1 of 10 steps executed**, §6 spine overturned by DR §3) ·
`2026-08-18-research-frame-proposal.md` (rulings stand, build items 0/n) ·
`2026-08-18-structural-census-and-cull-list.md` (evidence, partially refuted on contact) ·
`2026-08-18-model-substitution-log.md` (SPENT — debt discharged) ·
`2026-08-17-consolidated-action-plan.md` (**~1 of 45 items executed**) ·
`2026-08-16-adversarial-critique-and-execution-plan.md` (findings stand, sequencing dead) ·
`2026-08-15-adversarial-brief-pr103.md` (DISCHARGED, with a recorded deficit: no verdict on claims
2, 5, 6, 7, 8) · `2026-08-14-execution-plan.md` + `2026-08-14-remediation-workplan.md` (Track A and
part of D executed; Track C 061–066 **LAPSED**; `ratification_sweep_audit.py` never built) ·
`2026-08-13-writer-plan.md` (**0 of 5 phases**; Phase 1 explicitly re-decided the other way by DR
§12.0) · `2026-08-11-reconciled-findings-register.md` · `2026-08-05-archive-fork-execution.md`
(**DEAD** — 0 of 5 steps; its premise was reversed by the 2026-08-19 ruling that `_archived/` may
grow).

**Two SPENT files are in DR §8's mandatory four-document read-set** — the restart plan and the
handoff — so every fresh session is directed to read a spent procedure and an overturned sequence.
§5 Act 5 fixes that at the DR, which is where it is cheap.

### 2.5 HISTORICAL — the remaining 36 files

The 2026-08-12 cluster (4 files: trial log, phase-state map, step-R rename record, work-log audit —
all complete or frozen test artefacts), `2026-08-11-remediation-and-pipeline-anatomy.md`,
`2026-08-09-locator-hierarchy-and-enforcement-probes.md` (status line reads "IN PROGRESS" — stale),
`2026-08-02-architecture-decision-and-execution-plan.md` (**DEAD** — its premise was destroyed by
DR-2026-08-06's clean-room reset and its metric instrument was deleted in the 08-20 cull),
`P1-D2-D3-co0004-remapping.md` (**misfiled** — a March part-numbering table with no live referent,
belongs in `deprecated/`), and the 31 pre-August files.

**Not scheduled for action.** They are cheap to leave and expensive to sweep, and the referent map
shows every one of them is cited from somewhere. Retiring them is OD-8's business, and OD-8 is not
on the critical path. **Recording that they are historical is the whole of the work owed here.**

---

## 3. Conflicts still live

Eight were found; five are resolved. **Three remain, and only one costs anything.**

1. **`governance/check-registry.yaml` contradicts itself in one file.** Line 171 (battery
   description) asserts `DB content integrity (35 checks). Red on main - see tooling-register 4.`
   while the check-level note was corrected on 2026-08-22 to *72/72 checks pass*. Two lines, one
   file, opposite claims. **Failure mode §2(b), inside the file that inventories the gates.**
   → Act 3.
2. **R-12, filed 2026-08-11, re-filed 2026-08-18 as cull §15.6 item 1, never fixed.** The
   `governance` battery description is unquoted YAML containing commas, so it parses as:
   `{'deps': ['pydantic'], 'description': 'Decision protocol', 'doctrine recheck': None, 'adversarial-use.': None}`
   — two junk keys where a description should be. Verified live today. Its content is *also* stale:
   it advertises a "doctrine recheck" that OD-10 abolished on 2026-08-19. → Act 2.
3. **DR-2026-08-06 §3 vs. live state.** Its rescue rationale for `jurisdictional_values` cites
   "109/109 on `source_section`"; the 2026-08-12 clearing made that **0/109**. DR-2026-08-19 §1.5
   proposed annotating it; `git log` shows the file untouched. → Act 5, as a dated forward note.
   **Annotate, never rewrite** — a DR is a record of what was decided on its date.

Resolved and recorded, requiring nothing: DR §3 step 4/5 vs. the walk session record (amended in
place 2026-08-22); DR §12.1 step 10 vs. the REFERENCE-ONLY ruling (interim STOP notice in place,
the strike is OD-G); BRK-25 vs. BRK-26 (BRK-25 REFUTED, BRK-26 fixed); the adversarial-subject rule
vs. practice (recorded as deviation F-9, waiver is OD-F); restart-plan criterion 6 vs. handoff §6
(criterion struck).

---

## 4. What is owner-gated, and what is not waiting on it

**Owner-gated and on the critical path:** the **population-taxonomy pass (D-0165)**. It blocks acts
5–6 of the 08-22 plan, the first determination, and therefore `specifications` moving off zero. It
is the only thing in this repository whose absence stops the deliverable.

**Owner-gated and off the critical path:** OD-D (REF-00965/00968 tier re-grade — both still Tier 1
in the DB), OD-F (adversarial-subject waiver), OD-G (strike DR §12.1 step 10's clause), OD-2 (the
five-bucket ratification and the `jurisdiction-philosophy.md` §2.3 amendment), OD-8 (pre-August
archival), OD-9 (required-check set). **Also owner-gated: the `.ignore` entries** — its header
makes changing them a work-product judgement per DR-2026-08-06, so cull Phase 1's proposed
`workplan/deprecated/` entry is **not a session act at all**, and three plans that scheduled it
were scheduling something they could not do.

**Nothing in §5 waits on any of them.** That is the test this plan had to pass to be worth writing.

---

## 5. Execution

Ordered by cost. Acts 1–3 are one commit. Act 6 is the one that moves research.

### Act 1 — Retire `workplan/execution-plan-2026-08-12/`
**Location:** `workplan/execution-plan-2026-08-12/` → `_archived/workplan/execution-plan-2026-08-12/`
(13 files, 4,065 lines).
**Do:** `git mv` the directory. Then the two referent edits:
- `governance/retired-vocabulary.yaml:105` — the comment calls the directory "the live example" of
  the `workplan/*20??-??-??*/**` glob. **Correct the comment; do not remove the glob** — it is a
  pattern, it stays valid, and removing it would un-exempt any future dated plan directory.
- `workplan/2026-08-16-adversarial-critique-and-execution-plan.md:55` — repoint the path to
  `_archived/workplan/…`. The row is a historical finding about a path, so repointing preserves it.
**Evidence to record in the commit:** referentially closed (12 sibling referrers + 2 external, both
edited); 0% executed by three independent structural probes (`work_log` absent, `locator_schemes`
absent, 28 of 93 item names still carry digits); parent authority already archived.
**Falsification:** re-run the referent scan after the move. If any tracked file outside
`_archived/` still names a member file, the sweep was incomplete and Act 1 is not done —
CLAUDE.md §0.4. **The scan cannot see prose callers**; check `skills/*_SKILL.md` by reading, since
that exact blindness is what blocked cull Phase 4a.

### Act 2 — Fix R-12
**Location:** `governance/check-registry.yaml`, the `batteries: governance:` entry.
**Do:** quote the description so it parses as one string, and correct its content — drop "doctrine
recheck" (abolished by OD-10, 2026-08-19).
**Verify:** `python3 -c "import yaml;print(yaml.safe_load(open('governance/check-registry.yaml'))['batteries']['governance'])"`
must print exactly two keys, `deps` and `description`.
**Why this is not apparatus:** it removes two phantom keys from the file that inventories every
gate. Nothing is added. Open 11 days, named twice, one line.

### Act 3 — Correct the `db_integrity` battery description
**Location:** `governance/check-registry.yaml:171`.
**Do:** replace `DB content integrity (35 checks). Red on main - see tooling-register 4.` with a
description that carries no count and no status claim. **Do not substitute a fresh number** —
§2(b): a count in a derived document is the defect, not the stale value. The check-level note
corrected on 2026-08-22 already carries the measurement.

### Act 4 — Strike `GB` → `UK`, do not execute it
**Locations:** `workplan/2026-08-18-handoff-next-session.md` §6 step 4 ·
`workplan/2026-08-19-adversarial-critique-research-restart.md` §7 item 7 ·
`workplan/2026-08-18-research-frame-proposal.md` §10.4.
**Do:** strike the item in each, with a dated note giving the reason. **Write no migration.**
**Reason, and this is a reversal of four plans:** `GB` is the ISO 3166-1 alpha-2 code for the
United Kingdom. `UK` is not an ISO code. The change was specified to match a `jurisdictions` table
that does not exist and is not due until DR §3 step 6. Meanwhile `jurisdictional_values` is under
the owner's REFERENCE-ONLY quarantine — **a write to it on 2026-08-21 was caught by blocking L02
and retracted the same session.** So the act is premature, its justification is unbuilt, and its
direction is probably wrong. **Four plans scheduled it and not one of them asked whether it was
correct.** Hand the question to the taxonomy pass; it is a naming decision, which is the owner's.

### Act 5 — Reconcile at the DR, not in a new document
**Location:** `decisions/DR-2026-08-19-research-restart-operative-instrument.md`.
Amend **in place**, using the precedent its own 2026-08-22 amendment established and stating the
same reason (§5's reversal clause makes correcting the instrument cheaper than succeeding it).
- **§8, the four-document read-set:** the restart plan and the handoff are SPENT. Mark both
  *read as history* at the citation, not in a caveat further down. A session reading a mandatory
  read-set does not reliably reach the paragraph that qualifies it.
- **§3 step 6:** fold the four multiply-specified items (§1's table) into the one step that already
  owns their territory, with their locations. **One open item each, named once.**
- **§B:** add the §2.3 and §2.4 dispositions so the supersession table is the single index.
**Then:** append a dated forward note to `decisions/DR-2026-08-06-clean-room-evidence-reset.md` §3
recording that its "109/109 on `source_section`" is now 0/109. **Annotate; do not rewrite.**

### Act 6 — OD-5: make the R9 gate see the stash
**Location:** `scripts/audit/research_batch_dod.py`, the R9 duplicate check.
**Defect:** it queries `evidence_sources` (10 rows) only, and is blind to `source_locators`
(**835 rows**) — the lead index that exists precisely to hold identifiers the project already
holds. Batch 02 ran the stash check **by hand** because the gate could not.
**Why this is the highest-value unblocked act:** it is not new apparatus. It is failure mode §2(a)
— *a gate that passes having examined nothing* — in the one battery that guards research
admissions, and OD-5 has been named in four documents without being fixed. It is what holds
`GAP-B01-004` open, and it demonstrated itself three times in a single batch, once by surfacing
Finitzo-Hieber & Tillman 1978 through backward mining after R9 had passed the same DOI space clean.
**Do:** widen the R9 query to `source_locators`; keep `EXAMINED:` printing the true subject count.
**Falsification:** re-run against batch 02's session. If R9's `EXAMINED` count does not rise from
the `evidence_sources` figure to include the stash, the widening did not take. Then re-run
`--selftest`; it must still print 15/15.
**Then close `GAP-B01-004`** by migration, or record in the gap row why it stays open.

### Act 7 — Score and retire the 08-22 plan
**Location:** `workplan/2026-08-22-agonist-antagonist-execution-plan.md`.
Its §6 requires a scorecard *in that file* before archival, and none exists. **Append it — acts
0–4 done, act 3 with its recorded deviation, acts 5–6 blocked by D-0165, 3 of 7 owner decisions
answered, acceptance 4 undeterminable because both sides of the ledger it defined changed shape.**
Do not archive it yet: acts 5–6 are blocked, not finished, and archiving a blocked plan loses the
block.

**Not in this plan, deliberately:** the DoD gate printing PASS over empty subject sets, and A-18's
empty link set. Both belong in the D-0165 packet — the first because it needs a determination to
have a subject, the second because it *is* the taxonomy question.

---

## 6. One thing this plan does not fix, and names instead

**`bpc-rewrite-workplan-2026-05-11.md` is carrying doctrine.** Its B-before-E gate is cited as live
by DR §12.5 and restart-plan §6.5, and the file itself sits in the pre-August historical stratum
awaiting OD-8 archival. **A May workplan should not be the authority for a gate the research
runbook depends on.** The fix is to relocate the gate's definition into
`governance/` — but that is a doctrine move, DG-NON, and it is the owner's. Naming it here is the
whole of what a session may do. The same shape, less urgent, applies to
`best-practices-assessment-system.md`: **108 live referents on a `workplan/` file** is a content
document filed as a plan, and no amount of retirement discipline touches it while that is true.

---

## 7. Acceptance, termination, and how this file ends

**Acceptance.** Every act carries its own falsification above. This plan as a whole is accepted when:

1. `git ls-files workplan/ | wc -l` has **fallen** — Act 1 removes 13 and this file adds 1, so the
   live count must reach **59** (71 − 13 + 1, minus this file at §7.3). Net **−13**.
2. The registry parses with no junk keys and carries no count-or-status claim in a battery
   description.
3. `research_batch_dod.py` R9 prints an `EXAMINED` count that includes `source_locators`, and
   `--selftest` still prints 15/15.
4. The four multiply-specified items appear **once each**, at DR §3 step 6.
5. **Zero new checks, scripts, tables or plans exist as a result of executing this document.**

**Termination — the property this plan is subject to.** DR §11 property 5: a session that commits
anything other than fixes, record corrections, search logs, migrations, or a rendered determination
has failed. Acts 1–5 and 7 are record corrections and one archival move. Act 6 is a fix. **This
file is the only thing here that is not one of those five kinds, which is why §7.3 exists.**

**§7.3 — self-retirement.** When acts 1–7 are done, **delete this file.** Not `_archived/` — it is
not reader-facing content, it is scaffolding, and git is the archive for scaffolding (CLAUDE.md
§1). The durable outputs are the amended DR §3/§8/§B, the corrected registry, the widened R9 gate,
and the archived directory. **If any act is still open, leave the file and strike the acts that are
done, so what remains is visibly shorter than what was planned.** A reconciliation document that
survives its own reconciliation has become the thing it was written to remove.

**What this plan is honest about not doing.** It does not move `specifications` off zero. Nothing a
session can do moves it, because D-0165 is owner-gated and every determination route runs through
it. **The deliverable is blocked on one decision, and 31,617 lines of live workplan is what the
project built while it waited.**
