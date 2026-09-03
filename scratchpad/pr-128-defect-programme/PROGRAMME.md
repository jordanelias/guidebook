# The thirty-defect programme

**D05-001 … D05-030, resolved as one piece of work against the seven-stage spine.**

Planned by Fable 5.1 (read-only), written out by Opus 5. Every load-bearing figure below was
**re-derived by the writer** against the live repository before being written down — not
transcribed from the plan. Where the two disagreed, the derivation won and the disagreement is
recorded. Baseline: `2a1ef12`, `user_version` 67.

---

## 0. What was verified, and two corrections it forced

| Claim | Derivation | Result |
|---|---|---|
| FKs landing on `evidence_sources.ref_id` | `PRAGMA foreign_key_list` over every table | **12**, not 7 |
| Containment is derivable today | `json_each(connections_produced)` ⋈ `evidence_sources.doi` | **exactly 2 pairs**, both the antagonist's |
| D05-005 manifest contemporaneity | `wc -l`, `grep -c '"reconstructed": true'` | 49 lines, **0** reconstructed |
| D05-006 `LATEST-RESEARCH` staleness | `git log -- sessions/LATEST-RESEARCH` | advanced in `22bc8df` |
| CHECK 7's registry home | `check-registry.yaml` | `basis: research/adversarial-fields-complete`, advisory |
| ~~Retired-vocabulary hits in `transcripts/`~~ | `retired_vocabulary_audit.py` | **WITHDRAWN — it reports 71 and names ZERO transcript paths, before and after the exemption alike. See §7a.** |
| ~~FKs landing on `evidence_sources.ref_id` = 7 is stale~~ | see Correction 1 below | **WITHDRAWN — 7 is the cross-boundary subset, not a total. Not stale.** |

**Correction 1 — WITHDRAWN 2026-09-03. CLAUDE.md's foreign-key figure is NOT stale, and
changing it would have introduced the error it claimed to fix.**

This section originally said `evidence_sources.ref_id` carries 7 inbound keys but really carries
12, and T0.1 was to correct the file accordingly. **The two numbers measure different things.**

CLAUDE.md's sentence reads: *"43 foreign keys cross a boundary and 37 stay inside one, landing on
eight columns"*, and the eight listed figures sum to **exactly 43**. So the list is the breakdown
of the CROSS-BOUNDARY keys, not of total inbound keys. Every listed column is correspondingly
below its total, and consistently so:

| column | CLAUDE.md (crossing) | total inbound |
|---|---|---|
| `slugs.slug` | 14 | 16 |
| `items.item_code` | 10 | 13 |
| `evidence_sources.ref_id` | **7** | **12** |
| `populations.population_code` | 7 | 11 |

Four columns all lower, and the list summing to the stated crossing total, is not four
coincidences. **12 is the total; 7 is the crossing subset; comparing them is a category error.**
Writing 12 into that sentence would have broken the sum, contradicted the neighbouring 43/37, and
put a false figure in the file every session reads first — under the banner of fixing a §2(b)
defect. Caught when executing T0.1 rather than when planning it.

**What T0.1 does instead:** leave the figure alone, and record here that the total inbound count is
12, derived 2026-09-03 by `PRAGMA foreign_key_list` over every table. That is a real and separate
fact; it is simply not what that sentence states.

**Correction 2 — the containment query returns the antagonist's finding exactly.** Run today it
yields two rows and only two:

```
REF-00977 ⊃ REF-00784   10.1016/j.apmr.2010.01.009
REF-00977 ⊃ REF-00971   10.3109/17483107.2010.509885
```

That is F1 precisely — including its scope, which the first antagonist run over-counted as three.
**The database could have answered this from 21:11 on 2026-09-02**, an hour before an adversarial
reader found it by hand. This is the single strongest justification in the programme, and it is why
T0.4 is the one migration worth writing.

---

## 1. Four mechanisms, not thirty defects

The register looks like thirty independent bugs. It is four, and the fourth was not in the
original hypothesis.

**(a) A writer that cannot express a state its own checker accepts.** `insert_source` wrote
`VERIFIED` with disposition `OPEN`, which invariant I1 forbids outright; `log_mining` never set
the status C08's biconditional asserts; the `match_id` derivation made the doctrinal adversarial
dissent unwritable. All fixed. **Still live in half-fixed form: D05-025.** `add-source` gained
`--prior-expectation`, but `insert_source` still refuses `VERIFIED` without
`verification_method` and *not* without a prior — so it can still write rows CHECK 7 rejects.

**The mirror also exists, and is worth naming: a checker with no writer.**
`metadata_integrity_status` has no writer that ever leaves `CORRECTED`, and
`judgment/convergence-independence` has no convergence writer at all. A gate whose satisfying
writer does not exist is a trap; that is why T2.1 waits.

**(b1) A gate examining a proxy where the property IS decidable from data already held.** D05-023.
The remedy is a pointer, then a gate that reads it.

**(b2) A gate examining a proxy where the property is NOT machine-decidable.** D05-021 (harm
findings live in a brief the database never sees), D05-022 (a rationale weighed against a
payload). **The remedy here is emphatically not a new check** — it would be vacuous or red by
construction. The remedy is that the gate stops printing more than it asserted, and the property
is routed to the adversarial pass as a standing subject.

**(c) Provenance depending on memory.** D05-029, D05-018, D05-025. The unifying rule, which the
already-fixed members of this class all obey: *the artefact is written by the tool at capture
time, never reconstructed afterwards.* That is why `prior_expectation` is not backfilled with a
prior, and why D05-029 needs a hook rather than a habit.

**(d) Substrate presuppositions — not in the original hypothesis.** D05-001 and D05-002 are a
column and a table that would hold a **synthesis output** upstream of synthesis. Their correct fix
is the *absence* of work until synthesis exists, plus a doctrine text that currently contradicts
the ruling (§7b).

**The holistic link.** (b2) is gated by the adversarial pass, and the adversarial pass is gated by
leaving its workings on disk. **Fixing D05-029 is what makes D05-021 and D05-022 "gated" at all.**
That is the programme's spine, and it is why a transcript hook sits in the same plan as a
convergence view.

---

## 2. Stage assignment

Contract ids only, from `governance/pipeline-contract.yaml`. Substrate is not a stage.

| Defect | Stage / owning gate | Disposition |
|---|---|---|
| 001 `serves_axes` 1/106 | substrate (`slugs`); content is a **synthesis** output | no work pre-synthesis; §7b |
| 002 no term↔slug link | substrate; same ruling | no work — `terms_used` is correctly held on the research row |
| 003, 007, 015, 016 | no stage — record hygiene | done |
| 004 command-log misfile | no stage — session apparatus | done (`scratchpad/CURRENT`); doc fix in T0.1 |
| 005 manifest contemporaneity | evidence / `discovery-provenance` | **resolved in fact** — register stale |
| 006 stale `LATEST-RESEARCH` | research gate scope | **resolved in fact** — register stale |
| 008–012, 014, 026 | evidence — writer defects | RESOLVED |
| 019 | judgment — hand-off | RESOLVED |
| 020, 027 | research — writer defects | RESOLVED |
| 013 | evidence — the Co-1 screen-out | RESOLVED |
| 017, 028 | not defects | none |
| 018 Goodwin unlogged | evidence / `discovery-provenance` | T1.2 |
| 021 R7 harm unasserted | research → routed to cross_stage `definition-of-done` | T0.5 |
| 022 R13 presence ≠ soundness | research → same routing | T0.5 |
| 023 containment | judgment / `convergence-independence`; data lives at research | T0.4 view, T2.1 gate |
| 024 `results_found` | research (append-only log) | **accept** — §6 |
| 025 `prior_expectation` | evidence (admission-time) | T0.3 writer, T1.1 data |
| 029 transcripts by hand | no stage — artefact of cross_stage `definition-of-done` | T0.2 |
| 030 `.ignore` scope | no stage — owner-gated | §7a |

**What the no-stage cluster reveals.** Nine of thirty (003–007, 015–017, 029–030) concern the
apparatus that *records* work rather than the pipeline that produces the book. That is CLAUDE.md
§1's ratio showing up in the defect register. **None of them warrants a contract criterion**, and
proposing one for any would be the accretion §1 exists to stop.

---

## 3. Tranche 0 — before batch 06

Five single-file edits and one migration. Nothing here blocks research; T0.3 changes one writer's
behaviour and agents satisfy it with one flag.

### T0.1 · Register and map hygiene

**Do.** Mark D05-005 and D05-006 RESOLVED in
`scratchpad/pr-127-research-batch-05-circulation-icf/DEFECT-REGISTER.md`, carrying the derivations
from §0. Correct CLAUDE.md §7 trap 2, which still teaches the superseded anchor — it says the
harness session id is the anchor; `scratchpad/CURRENT` is, and the hook and its tests C01–C04
already say so.

**~~Correct CLAUDE.md's `evidence_sources.ref_id` figure from 7 to 12.~~ STRUCK 2026-09-03 on
execution.** 7 is the cross-boundary subset and 12 the total inbound; they are not the same
measurement, and the eight-column list sums to exactly the stated 43 crossing keys. Making that
edit would have broken the sum and put a false number in the file every session reads first. Full
reasoning in §0 Correction 1, withdrawn there.

**Why.** The register is the declared single home of defect status and is wrong about two entries;
a reader planning work from it would re-do finished work. The CLAUDE.md figure is the §2(b) defect
in the file that forbids it. The trap text actively teaches the mechanism that failed.

**Verify.** `grep -n "harness session id" CLAUDE.md` returns nothing calling it the anchor; the
register's two rows read RESOLVED with their derivation commands; and the eight-column figures in
the pipeline section still sum to 43.

### T0.2 · D05-029 — the transcript hook

**Do.** Append to `.claude/settings.json` a `SubagentStop` and a `Stop` entry, each running
`python3 scripts/preserve_transcripts.py` in copy mode. **Append — never insert at index 0**:
`scripts/generate/research_contract_hook.py` reads `SessionStart[0]["hooks"][0]["command"]` by
hardcoded index, and inserting ahead of it turns the blocking `research_contract_sync` check red
with a diff that reads as contract drift and is not (CLAUDE.md §5).

**Why.** Rule 6 already directs this; the script exists; only the trigger is missing. Copy mode,
never `--check` — `--check` is red for the whole life of a session and would teach its reader to
ignore it.

**Why this is not owner-gated, on reflection.** It edits harness configuration rather than book
content, and CLAUDE.md §1 reserves sign-off for content and doctrine while explicitly freeing
code — "Code is not." More decisively, **rule 6 is already an owner directive to preserve
transcripts**; the script exists and only its trigger is missing. Wiring a trigger for an
instruction already given is executing it, not deciding it. The one real constraint is technical
and is respected above: append, never index 0.

**Verify.** Observation, not inspection: after batch 06's first subagent finishes,
`git status --short transcripts/` shows a new file with nobody having run the script. An unknown
hook event name is ignored silently, so the edit landing is not evidence it fires.

### T0.3 · D05-025 — the writer half

**Do.** In `insert_source` (`scripts/db.py`), refuse `verification_status='VERIFIED'` when
`prior_expectation` is empty — the exact mirror of the existing `verification_method` refusal, in
the same error style, naming the flag and D05-025.

**Why — and this is the burden of proof, stated as §1 requires.** Without it every batch adds rows
CHECK 7 rejects, the check goes permanently red, and a permanently red check is one nobody reads.
More seriously: a prior written *after* reading a source lets expectation curate which sources are
admitted, and that reaches the book's evidence base. This is the field that exists to stop
post-hoc rationalisation; a writer that can skip it defeats it.

**Ordering.** Must land before batch 06's first `add-source`, or the batch adds nine more
non-compliant rows. Batch 06's agonist brief must carry the flag.

**Verify.** CHECK 7's count after batch 06 equals its count before — the nine, and no more.

### T0.4 · D05-023 — the containment pointer

**Do.** Schema migration `068_v_source_containment.sql`, `user_version` 68. A view over
`citation_mining` — `json_each(connections_produced)` on non-deferred rows — joined to
`evidence_sources.doi` and `source_slug_links` on the same slug, emitting
`(container_ref_id, contained_ref_id, slug, doi)`.

**Why.** Measured in batch 05: one line of evidence was about to be counted three times as
convergence, and **the database held the refutation from 21:11**. This is a cross-stage view
(research → evidence) and therefore the pointer CLAUDE.md calls the most protected object in the
schema — the thing that makes a convergence claim walkable back to the mining row that refutes it.

**Named readers**, because §1 forbids adding anything without naming what reads it: the
antagonist's standing query from T0.5 immediately; the T2.1 gate later; and it is the **first
reader `connections_produced` has ever had**.

**Sweep** (rule 4): `schema_reference_audit`, `migrate_db.py --rebuild`, `run_checks --selftest`.
A view is a caller and so is a skill.

**Verify.** `SELECT * FROM v_source_containment` returns exactly the two batch-05 pairs in §0 —
no more, no fewer.

### T0.5 · D05-021 / D05-022 — make the gate say what it asserted

**Do.** In `scripts/audit/research_batch_dod.py`: R7's pass line must stop printing the harm count
as though it were checked — say that candidates ≥ screened/25 is asserted and harm flags are
*reported, not asserted*. R13's must say the match **row** is present and grade soundness is not
tested there. R11's must state how many aliases it examined; it printed "all vocabulary carries
in-language sourcing provenance" over zero.

Then add both properties as standing subjects of the adversarial pass in
`governance/research-contract.yaml`, under a **non-hook** field (the hook text is regenerated from
`hook:` only, so a new key there would drift `research_contract_sync`): R7 — brief harm findings
against `harm_finding=1` rows and their content; R13 — each `mismatch_note` against the retained
payload; R2/R13 — `v_source_containment` for the batch's slug.

**Why.** A gate that prints a number it never checked is indistinguishable from one that checked
it. That is the §2(a) failure at message level, and it is how the exec-32 filing gap stayed
invisible. These two properties cannot be machine-decided, so the honest move is to stop implying
they were and give them a durable home in the pass that *can* decide them.

**Verify.** The R7/R13 lines re-run against batch 05 no longer read as claims about harm or
soundness; batch 06's antagonist cites all three subjects.

---

## 4. Tranche 1 — alongside batch 06

### T1.1 · D05-025 — the data half

**Do.** Write the repository's own idiom for declared absence — a sentinel of the
`[UNVERIFIED-QUANT]` family, e.g. `[NO-PRIOR: flag did not exist at admission; D05-025]` — onto
the nine rows via `db.py amend-source --field prior_expectation`, shipped as a compensating data
migration. CHECK 7 then counts declared-absent separately from NULL.

**Why this is not the backfill I refused.** A fabricated prior invents what someone expected. A
sentinel states that the field was uncapturable at admission. The first is fiction; the second is
the absence recorded in the field that should hold it.

**This reverses a decision I recorded, and the reversal is mine to own — but it must be loud.**
The session record says the nine are "left failing that check and were not backfilled." That
stands as the right call for *inventing priors*. It was the wrong call for *the field staying
silent*: CHECK 7 can now never go green for those nine, and a check that is red forever is one
its reader learns to skip — the exact cry-wolf failure this session fixed in the fidelity
checker. The sentinel is what makes the red meaningful again.

**The trap to avoid, stated because it is easy to fall into.** Writing a sentinel makes the field
non-empty, which would make CHECK 7 pass on rows that have no prior — turning a true red into a
false green, which is the "narrow it until it passes" antipattern §6 forbids. **So the sentinel
alone is not the fix.** `research_protocol_audit` CHECK 7 must be changed in the same commit to
count declared-absent separately from both recorded and NULL, and to report all three.

**Verify.** CHECK 7 reports zero lacking, nine declared-absent, and the count of genuinely
recorded priors — three numbers, not one.

### T1.2 · D05-018 — the Goodwin full text

**Do.** Retry `fetch()` once by routes not yet tried (author-manuscript repository; Wiley
`pdfdirect`). If still blocked, extend `reconstruct_manifest` minimally with
`--ingest <file> --url <url>` — it currently skips non-JSON files — to write a
`reconstructed: true` line whose `purpose` states how the file was obtained, from the committed
`agonist/goodwin2022.pdf`.

**Why.** The batch's page-level `[FULL]` quotes for H-6 and H-7 rest on a file no verifier reads.

**Verify.** `--verify-authors` EXAMINED unchanged (it indexes JSON), manifest line present,
`REF-00975.verification_note` amended to point at it.

### T1.3 · D05-030 — awaiting the single decision in §7a

The only item in the programme that waits on you. Everything else in Tranche 1 proceeds.

---

## 5. Tranche 2 — after batch 06, when judgment is first exercised

### T2.1 · D05-023 — the gate

**Do.** Wire `judgment/convergence-independence` to a check reading `convergence_assessment` ×
`v_source_containment`: a convergence row may not count a container and its contained as separate
sources. **Land it in the same commit as the first `add-convergence` writer.**

**Why the wait.** Until a writer exists, the gate is a trap of exactly the kind this programme
exists to remove — a checker whose satisfying writer does not exist. The view plus the standing
adversarial query is the enforcement in the meantime.

**Specification.** `basis: judgment/convergence-independence`; blocking; `no_floor` with the
reason that the convergence corpus is empty until the first judgment batch; prints
`EXAMINED: <n convergence rows>`.

**Verify.** `pipeline_contract_audit` shows the criterion's `check:` non-null.

### T2.2 · D05-001 / D05-002

Nothing in code. Every ICF-first frame declares the two gaps as batch 05's did. One deletion
candidate under §1: `term_item_links` — 0 rows, FK to the item layer the owner deleted — once
`grep -l term_item_links scripts/migrations/data_*.sql` shows no INSERT.

### T2.3 · D05-028

No change to `metadata_integrity_audit` and no new writer until §7c is answered.

---

## 6. What NOT to do

- **No new tables and no new columns.** Every item is a view, a refusal, a message, a hook, or a

> **SUPERSEDED 2026-09-03 by owner ruling: "harvest now and as you go".** This was a scope rule for this programme and was written as though it were a standing prohibition — which put it against **D-0173**, an ACTIVE DG-NON owner ruling that had already ORDERED the concept-vocabulary harvest and named the two objects it needs. CLAUDE.md rule 0: a live directive is not answerable to paperwork, and a scope rule of mine is paperwork. `observed_terms` and `term_adjudications` landed in migration 068. **D05-002's disposal as "no work" is withdrawn with it** — D-0173 ordered work, and the plan read the ruling's silence on shape as silence on obligation.
  data sentinel.
- **Do not backfill `prior_expectation` with a prior.**
- **Do not add `--set-results-found`** (D05-024). `results_found` is read only at the `=0`/`>0`
  boundary (R6, R8, R14); the log is append-only; the row's own note already carries the
  correction. **Close D05-024 as accepted**, not fixed.
- **Do not make R7 assert a harm floor.** `≥1` is satisfied forever by one row — the hardening R7
  already rejected. Do not text-mine `findings_note` for harm.
- **Do not narrow `metadata_integrity_audit` to make it green.** It is honest.
- **Do not build the T2.1 gate before its writer.**
- **Do not populate `serves_axes`.** Applicability is an output of synthesis.
- **Do not register `preserve_transcripts --check`.**
- **Do not re-plan the eighteen already resolved or not-defects.**

---

## 7. What actually needs you — one decision, and one deferral

Everything else in this programme is executable without asking. The two items below are not
caution; each rests on a specific ratified authority that a general instruction to act
autonomously does not reach.

### (a) D05-030, `.ignore` scope — **DECIDED 2026-09-03, and landed**

**Owner ruled option 1 of three:** hide the transcript JSONL from ripgrep, keep the index
searchable. Landed in this PR. `D05-030` closed.

**The measurement that justified it** — searchable, `REF-00977` returned 174 hits of which 136 were
transcripts, and `next_ref_id` 305 of which 194. After: 39 hits, identical whether or not
transcripts are excluded. Transcripts are conversation *about* the code, including superseded and
plainly wrong statements, so a hit answers a current question with a stale answer.

**Two corrections to what this section originally said, both mine.**

1. **The figure was wrong.** This section claimed *"21 of the live surface's retired-vocabulary
   occurrences are now in `transcripts/`"*. `retired_vocabulary_audit.py` reports **71
   occurrences and names zero transcript paths**, before and after the exemption alike — it
   `rglob`s the whole tree, so transcripts were never contributing. I wrote the figure out
   without deriving it, which is the §2(b) failure this repository names by name. The
   `exempt_paths` entry was still added, but as a *preventative* that keeps the `.ignore`
   header's stated invariant true — every path it hides is already adjudicated on that list —
   not because it fixed a live count.

2. **The recommended mechanism does not work.** This section recommended `transcripts/**` plus
   negations. That **failed a planted-token test**: `README.md` came back and `index.json` did
   not, because `**` excludes the session directory and gitignore cannot re-include a file whose
   parent is excluded. The `.ignore` header says exactly this, and its `sessions/**` +
   `!sessions/LATEST` precedent works only because `LATEST` sits at the *top level* of the
   excluded directory — `index.json` does not. **What landed is `transcripts/**/*.jsonl` plus
   `transcripts/*.jsonl`**, matching the payload by extension so no negation is needed and there
   is nothing left to get subtly wrong. Re-tested: README and index reachable, JSONL not.

**Swept:** `.ignore`, `CLAUDE.md` §7 trap 1, the global `exempt_paths` in
`governance/retired-vocabulary.yaml`, `transcripts/README.md`, and the batch-05 defect register.

### (b) `serves_axes` → `serves_icf` — **deferred, not asked**

The rename is a retired-token sweep across doctrine and schema. It is not in this programme's
scope and nothing here depends on it. Raised only so it is not lost.

### Closed autonomously, previously flagged

**`governance/functional-taxonomy.md` contradicting DR-2026-08-24 §2.4.** The file says every slug
declares `serves_axes` (≥1); the DR makes applicability an *output* of synthesis. I will annotate
the taxonomy text with a pointer to the superseding DR in T0.1. **That is recording a supersession,
which rule 0 says is the job on contact — not making a doctrine judgement**, which would be yours.
The underlying doctrine is untouched.

**The CORRECTED queue (D05-028).** Closed as no-action. Nine rows carry
`metadata_integrity_status='CORRECTED'` because nine rows were corrected, and the advisory red is
an owner-review queue doing its job. Building a `review-source` writer to drain it would be adding
apparatus whose justification is about the apparatus rather than the book — which §1 forbids in as
many words. **If the queue ever obstructs something real, that is the moment to design a drain.**

---

## 8. Autonomy

**Everything in Tranches 0, 1 and 2 executes without asking, with one exception.**

| | |
|---|---|
| Executable now | T0.1 · T0.2 · T0.3 · T0.4 · T0.5 · T1.1 · T1.2 · T2.2 · T2.3 |
| Waits on the batch, not on you | T2.1 (lands with the first `add-convergence` writer) |
| Waits on you | **§7a only** — one yes/no on `.ignore` scope |

Three items were flagged for you in the first draft and should not have been. T0.2 edits harness
apparatus, which §1 frees, and executes an owner directive rule 6 already gave. T1.1 reverses a
decision *I* recorded, not one you made — mine to correct, provided the reversal is loud and the
check is fixed alongside so the sentinel cannot manufacture a false green. The
functional-taxonomy contradiction is a supersession to *record*, which rule 0 makes the job on
contact rather than a judgement to escalate.

**What would make me stop and ask anyway**, stated so autonomy does not become silence: a fix that
turns out to need a new table or column (§6 forbids them, so the need itself would mean the plan
is wrong); a T0.4 view that returns anything other than the two known pairs (it would mean the
containment model is wrong, not the query); or CHECK 7's count moving in a direction T0.3 does not
predict. Each is a signal the analysis failed, not a step to push through.

## 9. Batch 06 is not blocked

Tranche 0 is five single-file edits and one view migration. The only change to research behaviour
is T0.3's refusal, satisfied with one flag. Tranche 1 runs beside the batch. Tranche 2 waits for
judgment to exist.
