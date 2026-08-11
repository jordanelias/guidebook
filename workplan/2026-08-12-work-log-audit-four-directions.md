# 2026-08-12 — Audit of the work log, in four directions

**Subject:** `workplan/2026-08-12-pipeline-walk-trial-log.md` (3,875 lines, 105 logged actions),
and the two documents that rest on it — `2026-08-12-commit-91-adversarial-review.md` and
`2026-08-12-pipeline-phase-state-map.md`. All three merged at `1f15381` (PR #92).
**Question:** does the log actually support what was built on it, and does it record what happened?
**Method:** four directions — forward (log → reality), backward (claim → log), completeness
(session → log), and internal consistency (document → document).

**Verdict: the log is sound and complete for the trial, and does not cover the review.** Two
number discrepancies, one of which conceals evidence, and both fixed in this commit.

---

## Inventory

| | |
|---|---|
| Logged actions | **105** — 66 COMMAND, 39 QUERY |
| SQL-EMIT payload previews | 25 — *not separate actions*: each shares its sequence number with the emit command that follows it, so the 130 `### [` headers in the file resolve to 105 distinct actions |
| Exit codes recorded | 66, of which **19 non-zero** |
| Table-delta blocks | 66 — one per command. Each compares a snapshot of all 67 `sqlite_master` tables (66 real + SQLite's internal `sqlite_sequence`) and prints only those that changed |
| Emitted migration files, quoted verbatim | 25 |
| Findings recorded inline | 27 |
| Predictions scored | 14 — **10 as predicted, 4 not** |

The scratch tree survives at `/tmp/…/scratchpad/walk` (77 MB) with its end-state intact, which
made direction 1 possible. It is ephemeral and will be reclaimed.

---

## Direction 1 — Forward: do logged results still reproduce?

Five load-bearing results re-derived against the surviving scratch database, without reference
to the log, then compared to what the log recorded.

| logged finding | log recorded | re-derived now | |
|---|---|---|---|
| B-Q1.1 — two paradigms disagree | 2 values, 2 paradigms, 1500–1830, `contested` 0 | `(2, 2, 1500.0, 1830.0, 0)` | **match** |
| A-S9-d — the dual store diverges | 7 `governing_refs`, 0 junction rows | `('MOB', 7, 0)` | **match** |
| B-Q3.2 — un-keyed connection target | 3 targets, 1 unresolvable | `(3, 1)` | **match** |
| A-PROBE-3 cleanup | dangling admission removed | 0 dangling | **match** |
| Break 1 — illegal row persists | `tier=99` survived | `('REF-90099', 99, 'not-a-real-evidence-type')` | **match** |

**PASS.** No drift between what the log says happened and what the database shows.

---

## Direction 2 — Backward: is every claim traceable to a logged action?

**Substance: PASS.** All ten log-level findings (`BASELINE-1`, `A-INC-1/2/4/5`, `A-PROBE-3`,
`B-1/2/3/4`) are carried into the review. None was dropped, softened, or quietly absorbed.

**Citation: FAIL.** Grepping the review for every log identifier — `A-INC-*`, `A-PROBE-*`,
`A-S9-*`, `B-*`, `BASELINE-*` — returns **nothing**. The review renumbers everything as
Break 1–4 and R1–R4 and cites not one log id.

So traceability from a review claim to its evidence runs **by prose correspondence only**. A
reader who wants the verbatim command behind "the FK guard is a post-commit alarm" must read the
log until they recognise the incident. That is precisely the defect the review criticises
elsewhere: §3.3 of the audited plan faults the BPC↔reasoning-doc chain for joining *by filename
stem* rather than by key, and the phase-state map faults `citation_mining.connections_produced`
for being a JSON string where a foreign key belongs. **This review joins its own claims to its
own evidence by prose.**

*Method note.* My first pass at this direction reported ten orphaned findings. That was a
proxy failure — I measured tag citation and read it as coverage. A second check for substance
found all ten present. And that second check itself produced a false negative on `A-INC-5`,
because the review writes "names the *wrong* migration" and my pattern did not allow for the
markdown emphasis. Two bad checks in one direction of one audit, both caught by re-deriving
rather than trusting the first number.

---

## Direction 3 — Completeness: what did the session do that the log does not record?

**Two gaps, and the second is the significant one.**

### 3.1 The driver code was never preserved

`harness.py` and seven stage scripts (`trial_a_stages_1_5.py`, `trial_a_stages_6_9.py`,
`trial_a_unwedge.py`, `trial_a_stage_9.py`, `trial_a_stage_9b.py`, `trial_a_stage_9c_12.py`,
`trial_b.py`) exist **only in the ephemeral scratch tree**. `git ls-files` returns nothing for
any of them.

The log records **66 argv lines, 25 verbatim SQL payloads and 25 emitted migration files quoted
in full**, in execution order, so replaying the trial from the log alone is largely mechanical.
What is lost is thinner than it first appears: the driver code, and with it the *intent* behind
the probe interleaving. That matters because Break 1 (Incident A-1), Break 3 (Incidents A-4 and
A-5) and the ordering probe at stage 4a are all ordering phenomena, and the log preserves the
order without preserving the reasoning that chose it.

*(An earlier draft of this section said the trial would be "reproducible only by reconstructing
the drivers" and attributed the ordering phenomena to "Breaks 1, 3 and 5". There is no Break 5 —
the review names four Breaks and the log names Incidents A-1, A-2, A-4 and A-5, and I conflated
the two numbering schemes. Both corrected.)*

**Closed in this commit** for the reusable half: `scripts/tests/walk_harness.py` is added, since
it is pure logging infrastructure carrying no content and is the thing the next clean-room test
needs. The stage scripts are deliberately **not** preserved — they are saturated with the
pre-existing E-08 material the owner has directed must not seed content research, and their
payloads are already in the log verbatim.

### 3.2 The log covers the trial. It does not cover the review.

This is the finding of the audit.

Probing the log for every subject of the review's factual lens:

| probe | occurrences in log |
|---|---|
| `migration_reproducibility` | **0** |
| `run_checks` | **0** |
| `check-registry` | **0** |
| `graph_audit` | **0** |
| `_legacy_guard` | **0** |
| `requirements.txt` | **0** |
| `70/70` | **0** |

The review carries **13 F-rows** (the factual lens, verdicts CONFIRMED / OVERSTATED /
SUPERSEDED) and **6 C-rows** (Part 7's self-corrections). That is **19 load-bearing verdicts**
produced by direct shell calls whose commands are quoted in prose and whose **outputs were never
recorded**. What survives of them is my summary of what I saw.

The asymmetry is stark and it is the wrong way round:

- The **trial** — whose findings are structural, reproducible on demand, and were re-derived in
  direction 1 above — has a 105-action verbatim log with per-table deltas.
- The **review** — which is where CONFIRMED, OVERSTATED and REFUTED are pronounced on another
  session's work — has none.

This does not make the F-rows wrong. Direction 1's method would settle any of them in minutes,
because they are all single commands against a repository at a known commit. It makes them
**unaudited in the sense the review itself demands of commit #91**: the audited document's own
standard, quoted approvingly in the review's Part 0, is *"Every number here was derived on
2026-08-11 by running the command quoted beside it. Where a claim has no command, treat it as
unaudited."* The review quotes its commands and does not log their output. By its own imported
standard it sits one rung below the document it audits.

---

## Direction 4 — Internal consistency: do the documents agree?

**Two discrepancies. Both fixed in this commit.**

### D4-1 — The log's line count is cited wrong, by my own hand

The review's front matter and the session record both cite the log as **"3,865 lines"**. It is
**3,875**. The quarantine-banner commit (`6f512b9`) added ten lines to the log and did not
update the two documents that cite its length.

Small, and worth recording precisely because of what it is: a derived number, hardcoded in prose,
invalidated by a later commit in the same session, in a repository whose CLAUDE.md opens by
warning that *"every count, value, status, or list in prose (including here) may be stale"* and
whose review found the same defect in commit #91 (F12, where `55 green` was invalidated by that
commit's own diff). **Two instances of one defect class in one session's document set** — mine
and commit #91's.

*(An earlier draft called this the "third instance, in three consecutive documents" and named
only two. The intensifier was unsupported and is withdrawn. The pattern is real and older than
either instance — CLAUDE.md §0 documents its own TL;DR having contradicted §7 about `audit.yml`
for a day — but a claim of three requires naming three.)*

### D4-2 — "23 migrations were emitted" conceals the interventions

The review's §3.0 states *"23 migrations were emitted."* Measured:

| | |
|---|---|
| SQL-EMIT actions in the log | **25** |
| Emitted migration files quoted in the log | **25** |
| Files surviving on disk | **23** |
| Rows in the scratch `data_migrations` ledger | **23** |

**25 were emitted; two were deleted.** Those two are exactly the files removed to escape the
deadlocked queue at Incidents A-4 and A-5 — the interventions the review calls "the second
rule-break the walk required" and logs as deviations in the attestation.

This is worse than a miscount. The figure reported is the one that makes the deletions
invisible: 23 emitted and 23 surviving is a clean story; 25 emitted and 23 surviving is the
story that actually happened, and the gap is the evidence for two of the four Breaks. It was not
deliberate — I counted the surviving files with `ls` at the end rather than the emissions — but
the direction of the error is unlucky, and a reader reconciling the log against the review would
have found a two-file discrepancy with no explanation.

Both figures are corrected in the merged documents by this commit.

---

## What this audit changes

| # | Finding | Direction | Status |
|---|---|---|---|
| 1 | Logged results still reproduce exactly | D1 | **PASS** — no action |
| 2 | All ten log findings reached the review | D2 | **PASS** — no action |
| 3 | The review cites no log identifier; claims join to evidence by prose | D2 | **OPEN** — recommend log ids in the review's Break/R rows |
| 4 | Driver code existed only in an ephemeral tree | D3 | **PARTLY CLOSED** — harness preserved; content-laden stage scripts deliberately not |
| 5 | The review's 19 factual verdicts have no verbatim output log | D3 | **OPEN** — the substantive gap; see below |
| 6 | Log line count cited as 3,865, is 3,875 | D4 | **FIXED** |
| 7 | "23 migrations emitted" — 25 were, and the gap is the deletions | D4 | **FIXED** |

**On finding 5, the recommendation is not "re-run everything".** It is to route review-lens work
through the same harness the trial used. `scripts/tests/walk_harness.py` is content-neutral: its
`run()` logs argv, cwd, exit code, stdout, stderr and per-table deltas for any command. Had the
factual lens run through it, F1–F13 would carry the same verbatim trail the trial does, at no
extra cost beyond invoking it. That is the process change worth making before the next test, and
it is why the harness is preserved and the stage scripts are not.

---

## Addendum — a defect the audit's own preflight caught

Running the attestation battery on this audit's diff surfaced a defect in the attestation that
shipped with PR #92:

```
CHECK 3: attestations/sessions_session_2026-08-12-…json unknown rule identifiers: ['integrity-protocol']
```

`integrity-protocol` is not a stable rule identifier. It is, however, a **skill file that exists
on disk** — `skills/integrity-protocol_SKILL.md`. I took the identifier from the filesystem,
where the schema requires it to come from `references/skill-registry.md`.

Measured, the drift is small and real:

| | |
|---|---|
| active `skills/*_SKILL.md` files | **49** (a further 12 sit under `skills/deprecated/` and are correctly out of scope; `find skills -name '*_SKILL.md'` returns 61) |
| absent from `references/skill-registry.md` | **2** — `integrity-protocol`, `supersession-audit` |

So two skills exist as authored protocols that no attestation may cite, and nothing flags the
skill files themselves — the check fires only when an attestation names one, which is the wrong
end. CLAUDE.md §10 warns that renaming a skill is a governed event *"because attestations
reference the stable identifiers"*; the inverse case, a skill that never acquired one, has no
guard at all.

The attestation is corrected to `structure-auditor`. **Two further observations about the check
that caught it.** It is `advisory`, so on a repository without branch protection an invalid rule
identifier would have merged regardless — as it did, in PR #92. And it is diff-scoped: it
examines attestations in the changeset, so the 74-attestation corpus has never been checked for
this. The review's F-row analysis noted the same shape for `attestation_schema` (blocking **and**
diff-scoped, so whole-corpus validity is established by no registered check). The same is true
of rule-identifier validity, and this is the first instance of it actually biting.

---

## Addendum 2 — adversarial critique of this audit, and what it fixed

At owner direction, this audit was itself critiqued for factuality, logic and method. **Six
defects, one of them mine and serious.** All are fixed above and in this commit; recorded here
rather than absorbed.

### The serious one: I shipped `walk_harness.py` without running it

Direction 3 recommended preserving the harness so review-lens work could be logged. I committed
it having run `ast.parse()` on it — a syntax check — and nothing else. Two consequences, found
only when I finally executed it:

**It defaulted to the canonical database.** The relocation from `_trial/harness.py` to
`scripts/tests/walk_harness.py` moved `Path(__file__).parent.parent` up one level, so `TREE`
resolved to `/home/user/guidebook` and `DB` to `/home/user/guidebook/data/guidebook.db`. Any
session importing it and calling `emit_and_apply()` would have emitted migrations into the real
`scripts/migrations/` and applied them to the real database.

**That is the exact defect class this session spent three documents cataloguing**, introduced by
the fix for one of its own findings, in a file added to a CODEOWNERS-protected directory, in a
commit whose preflight passed. It is also the fourth occurrence in this session of *a check that
passes without examining anything* — `ast.parse` on a module is `EXAMINED: 0` wearing a green tick.

**And my first fix for it was itself untestable.** I added guards that raise at import, then a
`--selftest` entry point — which could never run, because the guard fired before `__main__` was
reached. A check that cannot fire, added to fix a check that examined nothing.

Now: `WALK_TREE` is mandatory, a tree resolving to the canonical repository is refused by name,
the guards are deferred only for the selftest entry point that must import the module to prove
they fire, and `python3 scripts/tests/walk_harness.py --selftest` returns **3/3**, verified
against a real disposable tree.

### The other five

| # | Defect | Class | Fix |
|---|---|---|---|
| 1 | **"130 logged actions"** — the file has 130 `### [` headers, but 25 are SQL-EMIT payload previews sharing a sequence number with the emit command that follows. Distinct actions: **105**. The headline inventory number was inflated 24% | factual | corrected in the inventory, the subject line and Direction 3.2 |
| 2 | **"Breaks 1, 3 and 5 are all ordering phenomena"** — there is no Break 5. The review names four Breaks; the log names Incidents A-1, A-2, A-4, A-5. I conflated two numbering schemes while writing the section that faults the review for having no shared identifiers | factual / ironic | corrected to the incident ids |
| 3 | **"reproducible only by reconstructing the drivers"** — overstated. The log holds 66 argv lines, 25 verbatim payloads and 25 full migration files in execution order; replay is largely mechanical. What is lost is the *intent* behind the probe ordering, not the ordering | logic | rewritten |
| 4 | **"Third instance of one defect class, in three consecutive documents"** — I named two. The intensifier was unsupported | logic | reduced to two, named; the older CLAUDE.md case cited as prior art rather than counted |
| 5 | **"2 of 49 skill files"** — true for active skills, but `find skills -name '*_SKILL.md'` returns **61**; twelve sit under `skills/deprecated/`. Correct to exclude them, wrong to leave a reader unable to reconcile 49 against 61 | precision | scope stated |

### What survives unchanged

Direction 1's five re-derivations, direction 2's substance-versus-citation split, direction 3.2
(the review's 19 verdicts are unlogged), and both direction 4 discrepancies — the log line count
and the 25-versus-23 migration count. Those were the findings; none depended on the numbers
corrected here.

### The pattern across the whole session

Counting only errors I made and caught:

| # | Error | Caught by |
|---|---|---|
| 1 | A-S9-c blamed the retired `NEU` code; the traceback said the gap-id pattern | reading the traceback |
| 2 | Guessed `source_slug_links.link_id`; wedged the queue | the migration failing |
| 3 | "23 migrations emitted"; 25 were | direction 4 |
| 4 | Ten "orphaned" findings; a proxy measuring citation, not coverage | re-deriving |
| 5 | A false negative from a grep that could not match markdown emphasis | re-deriving |
| 6 | `walk_harness.py` defaulting to the canonical DB, shipped on a syntax check | finally running it |
| 7 | The fix for #6 being untestable by construction | running the selftest |

**Six of the seven were caught by executing something rather than by re-reading.** The one
exception, #3, was caught by a cross-document count — also execution. Not one was caught by
proofreading, which is the argument for routing review-lens work through the harness rather than
through ad-hoc shell calls whose output is never recorded.
