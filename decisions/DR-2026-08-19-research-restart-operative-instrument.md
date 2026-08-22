# DR-2026-08-19 — The operative instrument: restart research, end the loop

> **THIS DOCUMENT SUPERSEDES ALL OTHER PLANNING DOCUMENTS IN THIS REPOSITORY.**
> It is the only planning artifact a session needs to read, and it is meant to be **run**, not
> consulted. On ratification, every document in the supersession table below becomes historical
> record: readable for provenance, binding on nothing.

## §A How to use this document

| If you are | Read |
|---|---|
| The owner, ratifying | §9 (twelve decisions, one sitting), then sign §2.5 |
| A session about to work | §A → §3 (order) → §12 (the runbook) → run it |
| A session tempted to write a plan | §11. The check will reject your commit |
| Anyone checking what binds | §B below |

Two documents remain live alongside this one, and neither is a plan:

- **`CLAUDE.md`** — the repo's mechanical map (write path, gates, traps). Auto-loaded; a reference,
  not an instruction set. Where it disagrees with this instrument, this instrument wins and CLAUDE.md
  is the thing to correct.
- **`references/project-standards.md`** — the append-only operative rule ledger. Rules land there by
  design and machinery reads it. This instrument cites it; it does not restate it.

Everything else is superseded.

## §B Supersession table

| Document | Status on ratification |
|---|---|
| `workplan/next-steps-synthesis-2026-07-14.md` | **DISCHARGED** — freeze unsatisfiable (§2.5); §5 identity question answered by DR-2026-07-21 |
| `workplan/phase-e-execution-log-2026-07-14.md` | **SPENT** — pilot substrate destroyed by DR-2026-08-06; the "external review DECLINED" ruling carries forward per §10.2 |
| `workplan/2026-08-11-reconciled-findings-register.md` | **HISTORICAL** — R-01, R-06/07/08 verified resolved; **R-12 and R-17b transferred forward** (§10.7) |
| `workplan/2026-08-16-adversarial-critique-and-execution-plan.md` | **SUPERSEDED** — findings stand, sequencing dead |
| `workplan/2026-08-17-consolidated-action-plan.md` | **SUPERSEDED** — throughlines T1–T5 retained as diagnosis; only I-08 ever landed; §5's migration-number allocation table survives as the sole allocator |
| `workplan/2026-08-18-structural-census-and-cull-list.md` | **EVIDENCE, not instruction** — governs the cull where it and the cull plan differ |
| `workplan/2026-08-18-cull-execution-plan.md` (incl. §14, §15) | **DEFERRED behind the batch** — §15 is the route; §0.3 governs its value ("adds zero rows") |
| `workplan/2026-08-18-research-frame-proposal.md` | **RULING RECORD** — R1–R6 preserved; R1's strip *mechanism* overturned by §1 |
| `workplan/2026-08-18-handoff-next-session.md` | **HISTORICAL** — §2 rulings and §7 traps absorbed here; **§6 sequence overturned** by §3 |
| `workplan/2026-08-18-research-restart-plan.md` | **ABSORBED** — §§2–3 and §5 become §12 of this instrument; §4 criterion 6 struck (§3) |
| `workplan/2026-08-19-adversarial-critique-research-restart.md` | **ABSORBED** — F1–F9 are the defect list; §7's inverted order is §3 |
| `workplan/2026-08-18-model-substitution-log.md` | **SPENT** — debt discharged (§10.9) |
| `sessions/handoff-next-session.md` | **SUPERSEDED** — was already stale |
| The remaining ~80 `workplan/*.md` | **HISTORICAL** — archived post-batch under OD-8 |

**No successor to this document may be written.** §11 makes that mechanical, not aspirational.

---

## §C What this instrument decides, in one page

1. **The 93 items are leads, not research topics** (§1). 42 of 93 names embed a determination; the
   sources behind them were 97.8% unadmitted. Quarantine protocol in §1.4, zero migrations required.
2. **The dead 2026-07-14 freeze is discharged and succeeded** (§2, §2.5), with a reachable exit
   (`evidence_sources ≥ 1`) and a blocking check instead of a prose tripwire.
3. **Every DOI this project has ever held is preserved as a dedup and lead index** (§6). ~4,081
   exist; 397 are indexed; **R9 currently passes everything** because the gate cannot see the stash.
4. **Adversarial review is repointed** (§7): bound to data and synthesis diffs, forbidden on plans.
5. **Research runs before the schema refactor** (§3). Nothing in the refactor is a prerequisite;
   the batch is what makes the refactor safe.
6. **Acceptance is one answered question, published** (§4) — the only criterion apparatus cannot satisfy.

---

## §0 Original framing — why a Decision Record and not a plan

### The original title

**The 93 items become leads; the apparatus freezes until one batch lands**

**Category:** D-OP, with D-DOCT consequences · **Delegation:** DG-NON — work-product
inclusion/exclusion and trajectory are owner-only
**Status:** **RATIFIED 2026-08-19** by the owner (@jordanelias), as OD-1 of §9 — freeze
supersession, amnesty, items-as-leads, the §3 order, the §4 acceptance criterion and the
mechanical check, adopted together. §2.5 (a)–(d) are signed below. The remaining owner
decisions OD-2 through OD-12 are **still open**; nothing gated behind them is executed.
(This line read PROPOSED until ratification.)
**Relates to:** extends `DR-2026-08-06-clean-room-evidence-reset.md` §4.1 to the `items` table;
records, for the first time in a Decision Record, the substance of owner rulings R1–R6 of
2026-08-18, which currently exist only as prose in `workplan/2026-08-18-research-frame-proposal.md`.

---

## §0 Why this is a DR and not a workplan document

The six owner rulings of 2026-08-18 (R1–R6) are DG-NON decisions of doctrinal weight. They live
in a workplan proposal. The `decisions` table stops at **D-0163 (2026-08-15)** and `decisions/`
holds no record dated later than 2026-08-15.

That gap is not clerical. It is the mechanism of the recursion this repository is trying to
escape: **a decision recorded in a plan must be re-derived, re-litigated and re-rendered by every
session that follows it**, and each re-rendering is a new document that itself needs correcting.
Eight sessions in eight days have done exactly that, and ~30% of authored commits in that window
are corrections of a previous session's rendering of a decision nobody recorded.

A Decision Record is read once and cited thereafter. A plan is re-read and re-argued. This
document is therefore a DR, and it deliberately does not go in `workplan/`.

---

## §1 Decision 1 — the 93 items are LEADS, not research topics

### §1.1 The finding

Ruling R1 converts the 93 `items` names into research slugs by manual strip. Measured against
the live database:

| | |
|---|---|
| `items` rows | 93, all `status='active'`, **all created before the 2026-08-06 reset** |
| names embedding a numeric determination | **28** — e.g. `A-02 Acoustic Ceiling Panels (NRC ≥0.85) in Occupied Spaces`; `E-08 Corridor Clear Width (≥1200 mm Minimum on All Primary Routes)`; `A-08 HVAC Noise Control (NC-25 Maximum in Sensitive Spaces)` |
| names embedding a prescriptive condition clause | **23** — e.g. `E-02 Platform Lift (Where Full Passenger Lift Not Achievable)`; `D-04 Landmarks at Every Decision Point` |
| overlap of those two sets | 9 |
| **distinct names carrying a determination** | **42 of 93** — and 42 is a floor: looser condition-words reach 49, and whole-prescription names (`A-04 Acoustic Zoning: Graduated from Arrival to Primary Occupation`) are counted by neither test |
| items carrying `bpc_source_slug` | 87 of 93, resolving to **27 distinct slugs, all ACTIVE** among the live 106 |
| pre-reset sources behind those 27 slugs | 366 distinct, of which **358 (97.8%) had no admission edge** |

**The contamination is in the `name` column, and the name column is precisely what R1 converts
into a research question.** Nearly half the 93 names state an answer. Those answers rest on a
corpus the owner set aside on 2026-08-06 *because it could not show its work* — and the specific
sources behind these specific items were 97.8% unadmitted, worse than the 95% corpus-wide figure
that justified the reset.

### §1.2 The second vector: the determinations are still rendered

`DR-2026-08-06` §2 states: *"The file surfaces are untouched. `references/bpc/**`,
`references/bpc-reasoning/**`, `references/connections/**`, `specs/`, `site/` and `parts/`
remain exactly as they were, as reference."*

That was correct and deliberate for sources. For **items** it means the determinations are live on
every readable surface:

- `index.html` — 91 item-name spans on the repo's front page, values included
- `site/specs/` — **93 per-item HTML pages**, each `<h1>` a full determination-bearing name
- `parts/v10/part04.md` — the complete items table
- `versions/current/…_v9-0_2026-03-20.md` — prose determinations (`A-03 STC ≥35 acoustic door…`)
- `tools/*.html` — embedded JSON carrying item codes and full names
- `references/bpc-reasoning/room-acoustic-performance.md` — the sole surviving reasoning doc, and
  the restart plan's **first slug**: it cites item codes densely and states per-population values
  (`RT60 ≤ 0.3 s` for DEAF, `≤ 0.4 s` labelled *"conjecture rationally informed by literature"*)
  resting on REF-ids that no longer exist

**Archiving the `items` rows quarantines none of this.** A researcher who greps the repository for
their slug will meet the old answer before they have logged their first search.

### §1.3 The decision proposed

**Apply to `items` exactly the ruling already adopted for the corpus.** `DR-2026-08-06` §4.1:

> *"Research resuming does not restore these rows. It writes new ones under the logged-search
> discipline, carrying the admission edge that 95% of the frozen corpus lacked."*

And as the restart plan puts it for the pre-reset database: *"a lead list, not a backup.
Consulting it to find candidate sources is legitimate; every one still has to be searched for,
logged, re-retrieved and admitted on its own evidence."*

**The 93 items are a lead list of research questions. They are not research questions.** No new
doctrine is needed; this is the existing ruling extended to the one table that was exempted from it.

### §1.4 The quarantine protocol — six rules

1. **No item name becomes a slug by strip.** A slug is authored from the ICF/access-need frame
   first; the item list may then be consulted to check *coverage* — "did we miss a topic?" — never
   to supply one.
2. **No value crosses.** No numeric, dimension, threshold, range, or prescriptive clause from an
   item name, `item_axis_links.mechanism_note`, or any rendered surface may appear in a
   `search_executions` row, a `search_candidates` row, an admitted source's fields, or a
   determination. Item values live in `_archived/` and in reference surfaces only.
3. **Item-derived topics land as `PROVISIONAL`.** `slugs.status` already permits
   `'PROVISIONAL'` by CHECK constraint and **zero rows currently use it**. This needs no
   migration, no new column, no new table. A `PROVISIONAL` slug may be searched against; it may
   not carry a determination until an owner promotes it to `ACTIVE`.
4. **Provenance is recorded, not hidden.** `created_by_session` names the session that derived the
   topic; the session record names the item code it came from. The lead is auditable precisely so
   that a later reader can test whether it anchored the result.
5. **Blind-first ordering.** For any slug with a rendered predecessor — which is all 27 —
   the search log is written before the predecessor is read. This is not a new rule: the restart
   plan §5 already mandates it for `room-acoustic-performance` (*"Do not read
   `references/bpc-reasoning/room-acoustic-performance.md` until step 12 is complete"*). This
   decision generalises it from one doc to the whole reference surface.
6. **Dedup is real work, not hygiene.** "106 + 93 = 199 topics, no dedup" is true as a string
   statement and misleading as a topical one: 87 of 93 items descend from 27 existing slugs, and
   **13 items descend from `room-acoustic-performance` alone**. The dedup pass is a topic-modelling
   judgement, and it is owner-gated.

### §1.5 A consequence R1 did not price: `jurisdictional_values`

`DR-2026-08-06` §3 rescued `jurisdictional_values` from the reset, over an explicit correction by
the owner, on this reasoning:

> *"All 109 rows carry `standard_name` **and** `source_section` — 109/109 on both… A standard cited
> by clause is fully located; demanding a DOI of it imports an academic model onto a class that
> never used one."*

**That reasoning no longer holds, and the DR was never annotated.** Live, the table retains exactly
five populated columns — `jv_id`, `item_code`, `jurisdiction`, `standard_name`, `evidence_tier`.
**`source_section` is 0/109.** The values and locators were cleared by a later owner ruling
(2026-08-12), recorded only in the YAML headers: *"RETIRED TO REFERENCE-ONLY… it names which
document to go and get, never what it says."*

So the table the owner personally intervened to save is now a pointer list whose **only subject
column is `item_code`** — and it carries a foreign key to `items`. Retiring `items` (R1, handoff
§6 step 8) leaves 109 rows of (jurisdiction, standard_name, tier) with nothing to be *about*, on
top of the FK breakage separately recorded as F1 in
`workplan/2026-08-19-adversarial-critique-research-restart.md`.

**Proposed:** `DR-2026-08-06` §3 is annotated to record the 2026-08-12 clearing, and
`jurisdictional_values` is re-keyed to slugs — or explicitly retired — as its own decision, before
`items` is touched. It must not be collateral damage of a step whose stated subject is `axes`.

---

## §2 Decision 2 — the apparatus freezes until one batch lands

### §2.1 The finding

The repository pays for meta-work and charges for research. Measured:

| Path | Required artifacts |
|---|---|
| Add a `workplan/*.md` | commit-message format only — **and that check is push-only, skipped on PRs** |
| Admit one evidence source | session id · pre-state DoD run · verbatim query log before screening · tier-ordered screening · DOI pre-check · locator re-retrieval ladder · 5 metadata fields · population-match grading · class routing · **a committed SQL migration** · DoD gate exit 0 with EXAMINED > 0 · session record · **two** pointer updates · doctrine token · attestation JSON with a written self-counterclaim |

Meanwhile the machinery keeps a permanent "unfinished" signal alive that only apparatus work
appears to answer:

- The **Stop hook** in `.claude/settings.json` runs `research_batch_dod.py --all` at *every*
  session close and prints *"this session closed non-compliant"*. The evidence tables are empty
  **by owner decision**, so this cannot be cleared by any session, research or not.
- **13 registered checks currently examine zero subjects**, 12 of them flagged `empty-by-decision`.
- The doctrine-recheck counter at `data/doctrine_recheck/working_session_counter.yaml` reads
  `counter: 12, last_updated: 2026-05-02` — frozen for 3.5 months, with the note *"Next periodic
  recheck at counter == 25."* A standing obligation with a dead odometer: it can never fire, and
  can always be cited as owed.
- The backlog grows monotonically: markers (`DEFERRED|PENDING|OPEN`) across
  `workplan/ governance/ decisions/` went **318 → 389 → 418** and workplan files **95 → 110 → 139**
  over two weeks. 23 of 163 decisions sit `review_status='PENDING'`.

Every session-close is also contractually obliged to emit a `next_action`, and the adversarial-pass
convention requires each critique to run in a *fresh* session. Meta-work is self-catalysing by
construction.

### §2.2 The decision proposed

**Until `evidence_sources` holds at least one admitted source with a complete walk, the following
are frozen** — no new instances, corrections to existing ones excepted:

1. No new file in `workplan/`.
2. No new check in `governance/check-registry.yaml`.
3. No new register, sweep, census, or ledger.
4. No adversarial pass whose subject is a plan, critique, handoff, or census. **An adversarial pass
   may only take as its subject a diff that wrote data or synthesis.** This single rule ends the
   critique→plan→critique loop; the document that precedes this one is third-order and would not
   have been authorised under it.
5. No schema migration whose purpose is frame refactoring — specifically handoff §6 steps 5 and 8,
   for the reasons in §1.5 and in F1/F2 of the adversarial critique.

**Mechanically enforceable**, and cheaply: one entry in `governance/check-registry.yaml` plus one
script, blocking, kinds `[governance]`, failing any commit that adds a file to `workplan/` or an
entry to the check registry while `evidence_sources` is empty. The registry's entry schema is
`id / cmd / battery / kinds / level / basis / cost / min_items`, and the three attestation checks
are existing precedent for changeset-scoped gating. **A check that blocks new checks is the
smallest possible reversal of the cost gradient.**

### §2.3 Three companion changes, each one edit

- **`skills/session-consolidator_SKILL.md`** — make `next_action` optional, defaulting to *"none —
  resume the restart plan at step N"*. Delete the Step 1c heuristic that converts a plan pivot into
  a D-OP record. Retire the dead recheck counter.
- **`governance/doctrine-recheck.md` §1.3** — drop "any doctrinal-rule revision" as a recheck
  trigger. It makes governance edits self-breeding.
- **`.claude/settings.json`** — gate the Stop hook's FAIL print on `EXAMINED > 0`. *This is harness
  configuration and is proposed for the owner to make, not executed here.*

### §2.4 What the freeze does not do

It does not cull. `workplan/2026-08-18-cull-execution-plan.md` remains independent and unaffected;
this decision neither adopts nor rejects it. It does not retire any check — the 13 zero-subject
checks stay registered, and re-arm when their subjects repopulate, exactly as `DR-2026-08-06` §4.2
already instructs. It does not touch the R1–R15 research contract, which is the one piece of
apparatus that acts on research rather than on itself.

---

## §3 What this unblocks, and in what order

The restart plan §7 already establishes that no cull phase is a prerequisite. This decision
extends that: **no schema phase is a prerequisite either.** Every input the first batch reads is
live today — `slugs` 106, `term_aliases` 2,382, `axes`/`access_needs` and their 232 mapping rows,
`jurisdictional_values` 109. Every table it writes exists and is empty.

1. ~~Owner adopts or rejects this DR.~~ **DONE 2026-08-19 — RATIFIED (OD-1).**
2. ~~Fix the write path, the read path and the two transaction defects — F3–F6.~~ **DONE
   2026-08-19.** `db.py connect()` no longer sets `journal_mode`, and 16 pure-read call sites
   pass `readonly=True` (F4); `migrate_db.py` applies body, FK verdict and ledger row in one
   transaction with the pragmas hoisted (F5/F6); `emit_data_migration.py` no longer wraps bodies;
   `scripts/research/emit_batch_sql.py` is the capture path (F3). Proved by
   `migrate_db.py --selftest` (14 cases) and `emit_batch_sql.py --selftest` (9 cases), and by a
   rebuild that reproduces every table count identically.
3. ~~Seed the three missing DoD selftest cases (R9, R12, R15).~~ **DONE 2026-08-19** —
   `research_batch_dod.py --selftest` now asserts all fifteen rules and prints 15/15.
4. ~~**Run the first research batch** — restart plan §§2–3, unchanged, under the §1.4 quarantine.~~
   **DONE 2026-08-19** — `session_2026-08-19-research-batch-01-room-acoustic-performance`:
   9 `search_executions`, 5 `evidence_sources`, 5 `source_slug_links`, 12 `evidence_population_match`.
   Its five admissions were first written with **fabricated author lists**, corrected the same day
   against persisted Crossref payloads; `GAP-B01-001` holds the content re-read open.
4a. **The owner decision batch OD-A … OD-G** —
   `workplan/2026-08-22-agonist-antagonist-execution-plan.md` §2. **← THIS IS THE NEXT ACT, and it
   is the owner's, not a session's.** OD-A (are `item_population_links` substrate or scaffolding —
   all 372 carry `rationale_ref` NULL), OD-B (do deaf and hard-of-hearing people belong on
   `room-acoustic-performance`), OD-C (A-18's applicability set), OD-D/OD-E (two tier re-grades),
   OD-F (the adversarial-subject waiver), OD-G (strike step 10's `jurisdictional_values` clause).
   **Nothing in step 5 can be authored until OD-A, OD-B and OD-C are answered.**
5. Render **a** determination and read it — for a cell chosen **applicability-edge-first**, not
   the cell this DR's original framing implied. **AMENDED 2026-08-22.** As written, step 5 pointed
   at A-18 × AUT; `BRK-20` established that A-18 carries **zero** `item_population_links` and its
   only route to a population is the axis map, which owner directive D-1 quarantines. Authoring
   that cell today would render a coverage failure as an epistemic finding — the
   `workplan/2026-08-20-adversarial-adjudication-a18-aut.md` refusal, which stands.
6. Only then: re-key or retire `jurisdictional_values`; re-scope handoff step 8 with its full
   dependency cascade; re-arm the retired `min_items` guards.

Step 4 populated `evidence_sources` and `source_slug_links` — two of the six invariant tables the
blocking reproducibility gate compares. **Running the batch first is what made the later schema
work safe to run at all.**

> **AMENDMENT 2026-08-22 — why this section was edited rather than superseded.** Step 4 read
> *"← THIS IS THE NEXT ACT"* for three days after it was completed, so an agent obeying CLAUDE.md
> lines 9–12 (*"the instrument wins"*) was directed at step 5, and step 5 pointed at the one cell
> the project had already refused on evidence. The halt was recorded only in
> `sessions/session_2026-08-20-provenance-walk.md` §7, which does not bind. That is a defect in
> this instrument, not in the session record, and §5's reversal clause makes correcting it here
> the cheaper repair. **No successor DR is written, and none is owed.**

---

## §4 Acceptance — the one criterion apparatus cannot satisfy

Every criterion currently in play can be met by building apparatus: a gate exits 0, a rebuild
reproduces, a test scores 72/72, a metric moves. That is why apparatus is always the locally valid
move, and it is the whole of the loop.

**Proposed single criterion, replacing restart-plan §4 criterion 6** (which F7 of the adversarial
critique shows is made unreachable by handoff step 8):

> **One answered question, published.** One research question, with a determination, its governing
> sources, its population-match grading, and its search log *including the empty searches* —
> rendered and readable as output, not as a row count and not as a green check.

No script, registry entry, check, decision record, or plan can satisfy that. Only research can.

---

## §5 Reversal

Both decisions are reversible by a later DR recorded here. The freeze expires by its own terms the
moment `evidence_sources` is non-empty; it needs no repeal. Decision 1 is a handling rule for a
table that is archived rather than deleted under R1, so nothing it governs is destroyed.

**This DR proposes no successor document, and none is owed.** The next artifact should be a search
log.

---

# AMENDMENTS — 2026-08-19, after six read-only adjudication passes

The sections below were added after the audit that this DR's §2 anticipated. They convert it from
two decisions into **the single binding instrument** the adjudication ruled for. Sections 0–5 above
stand unchanged.

## §2.5 Freeze supersession — the clause the owner signs

A governance freeze already exists. `workplan/next-steps-synthesis-2026-07-14.md` §2.6 declared it;
`workplan/phase-e-execution-log-2026-07-14.md` records the owner adopting it ("Owner chose **A** …
holds the governance freeze that protects it"); `decisions/DR-2026-07-21-product-posture-thinking-tool-not-authority.md`
re-imposed it as a **ratified** consequence clause. Its tripwire read: *"If a week passes with
`reasoning_doc_citations` unchanged and any governance commit landed, the freeze was breached —
stop and re-read this section."*

Measured 2026-08-19: **five weeks elapsed; `reasoning_doc_citations` = 0** (its baseline was 7);
**60 Decision Records, 87 attestations and 140 workplan documents** added since. The firing
condition was met every week for five weeks and no session checked it.

**Ruling: the 2026-07-14 freeze is discharged as unsatisfiable, and Decision 2 of this DR succeeds
it.** Not honored-as-is, not amended. Its exit condition ("until the pilot reaches
COMPLETE-behind-banner") and its metric were both destroyed by the owner's own ratified
`DR-2026-08-06`. A freeze whose exit is unreachable and whose odometer is dead is the identical
pathology this DR §2.1 names in the recheck counter: *it can never fire, and can always be cited as
owed.* Amending it produces the same instrument wearing the old name; two documents where one
suffices is the disease.

Four clauses, **signed together by the owner on 2026-08-19** (OD-1):

- **(a) Discharge.** The 2026-07-14 freeze is discharged as unsatisfiable, its exit condition and
  metric having been destroyed by ratified `DR-2026-08-06`.
- **(b) Amnesty, recorded once.** The five-week breach is recorded and amnestied **as to artifact
  validity**, not re-litigated per artifact. Validity in this repository flows from ratification and
  the migration/gate record, not from freeze compliance — and every major in-window artifact
  (`DR-2026-08-06`, the 2026-08-12 baseline DRs, `DR-2026-08-14/15`) was **owner-ratified**. The
  owner ratifying work during the owner's own freeze is the freeze authority waiving itself in fact.
  What was missing was the record of the waiver. This clause is that record.
- **(c) Succession.** Decision 2 of this DR succeeds it, with the blocking check of §2.2 landed in
  the same PR as ratification. Its exit is reachable and self-executing: `evidence_sources ≥ 1`.
- **(d) Non-repeal.** `DR-2026-07-21` consequence 2 remains in force and is **implemented by** this
  mechanism, not replaced. A future session must not read this succession as loosening ratified
  doctrine.

**Signed 2026-08-19.** Clause (c)'s blocking check was `meta_work_freeze`
(`scripts/audit/meta_work_freeze.py`, blocking, kinds `[always]`), landed in the same commit as
this ratification. **CORRECTION, same day:** that check has since been RETIRED and deleted. It
discharged itself exactly as designed — its exit condition `evidence_sources >= 1` was met when
the first batch landed, after which it passed unconditionally and forever while still executing
on every changeset. Clause (c) is therefore SATISFIED AND SPENT, not repealed: the freeze it
enforced ended by its own terms. §11 property 3 below is corrected to match. The 2026-07-14 freeze is discharged from this date; the
five-week breach is amnestied as to artifact validity and is not re-litigated per artifact.

## §6 The identifier stash — every DOI this project has ever held

**Finding.** ~4,081 distinct DOIs are recoverable across the repository. **397 are in the live
`source_locators` store — under 10%.** ~3,203 sit in fourteen B11 citation-mining artifacts under
`sessions/artifacts/2026-05-2[34]-b11-*-discoveries.json`, of which 2,337 carry title + year + first
author. `sessions/` is hidden from ripgrep by the root `.ignore`, so **two-thirds of this project's
identifier capital has been invisible to every session that searched for it.** Also recoverable:
221 PMIDs, 111 PMCIDs, 243 standard-clause numbers, ~35 ISBNs.

**Why this is urgent, not housekeeping.** Rule **R9** — *"Pre-check the DOI. If it exists, cross-file
the existing ref_id — never duplicate"* — is enforced by `scripts/db.py add-source` (~L1651) and
`scripts/audit/research_batch_dod.py` (L432–436), and **both query `evidence_sources` only**. That
table holds 0 rows. **R9 currently passes everything.** The dedup index exists, holds 835 rows, and
the gate cannot see it. Restarting research without wiring it re-mints identifiers for sources this
project already found and paid to verify. No live Python reads or writes `source_locators`, and no
registry check protects it.

**Doctrine.** This is not a new decision. On **2026-08-12** — six days *after* the reset — the owner
ruled DOIs and URLs kept, into a table whose own migration header states: *"Reference-only registry…
NOT an evidence table… this table only prevents duplicate lookups and names documents worth
sourcing,"* with the standing rule *"consumed and retired as sources are admitted."* A DOI is a
name, not a finding. `DR-2026-08-06` §4.1 sets the corpus aside because it *could not show its work*
— an argument about assertions, not identifiers. The restart plan already blesses the practice:
*"Consulting it to find candidate sources is legitimate; every one still has to be searched for,
logged, re-retrieved and admitted on its own evidence."* This section mechanises that sentence.

**Design.** Widen `source_locators`; do not build a new table and do not use `search_candidates`
(which requires `found_under_slug` and `session` NOT NULL — recovered leads have neither, and its
disposition vocabulary describes screening inside a logged search these rows never had).

```sql
ALTER TABLE source_locators ADD COLUMN title             TEXT;     -- re-findability, not bibliography
ALTER TABLE source_locators ADD COLUMN pub_year          INTEGER;
ALTER TABLE source_locators ADD COLUMN first_author_last TEXT;
ALTER TABLE source_locators ADD COLUMN lead_status       TEXT NOT NULL DEFAULT 'LEAD'
  CHECK (lead_status IN ('LEAD','SUPERSEDED-TWIN','CONSUMED','DEAD-LOCATOR'));
ALTER TABLE source_locators ADD COLUMN consumed_by_ref_id TEXT REFERENCES evidence_sources(ref_id);
CREATE UNIQUE INDEX ux_source_locators_doi_active
  ON source_locators (lower(doi)) WHERE doi IS NOT NULL AND lead_status='LEAD';
```

R9 becomes a case-insensitive union across both stores. An `evidence_sources` hit keeps today's hard
error (cross-file). A `source_locators` hit is **not a block** — it is the promotion path: this DOI
is a known lead, admit it reusing the stash's ref_id. Promotion runs the ordinary R1–R15 pipeline and
closes with `lead_status='CONSUMED', consumed_by_ref_id=<new ref_id>` — the owner's *"consumed and
retired"* rule, without deleting the row.

**Two defects to repair at load.** (i) `workplan/dedup-audit-same-doi-multi-refid-2026-07-21.md`
adjudicated **29 DOI groups spanning 73 ref_ids** and merged 20 twin-groups via
`superseded_by_ref_id` — a column `source_locators` does not have, so that adjudication is invisible
in the live store and 50 superseded rows sit unmarked. Replay it as `SUPERSEDED-TWIN`. (ii) Mark the
69 `NO-MATCH` DOIs `DEAD-LOCATOR` so the unique index ignores them.

**The back door, closed mechanically.** The risk is a lead index that quietly becomes a citation
source, readmitting the 95.5%-unadmitted corpus. **A foreign key is insufficient** — `migrate_db.py`
applies with `foreign_keys = OFF`, so orphans are accepted. Triggers fire regardless of the pragma:

```sql
CREATE TRIGGER no_cite_leads BEFORE INSERT ON source_slug_links
WHEN NOT EXISTS (SELECT 1 FROM evidence_sources WHERE ref_id = NEW.ref_id)
BEGIN SELECT RAISE(ABORT, 'lead not admitted'); END;
```

Plus an `AFTER INSERT ON evidence_sources` trigger auto-marking any lead sharing the DOI as
`CONSUMED`, so stash and admissions cannot diverge silently; plus a registered blocking
`source_locators_floor` check, since nothing today would detect the stash's corruption.

**Owner-gated within this section:** extending the ruled-on scope from 835 to ~4,081 (same doctrine,
larger population, DG-NON class); whether title/pub_year/first_author ride along (they are metadata,
not identifiers, and cross from *name* toward *description*); whether the 28 identifier-less archive
rows justify relaxing the table CHECK.

## §7 Adversarial review — preserved as a truth-instrument, abolished as a plan-instrument

**The finding.** ≥10 adversarial passes ran in five weeks. **Not one examined research output**,
because there is none. The convention that each runs in a fresh session is epistemically correct and
is simultaneously the mechanism guaranteeing a new session per critique. Critique → plan → critique
is the tightest loop in this repository.

**The precedent already exists.** `sessions/session_2026-07-26-energy-conservation-rest-points-seating-adversarial.md`
is the only adversarial pass ever run on research output — owner-prompted, one session, **seven
findings, all against the author's own admitted batch**, catching error in *both* directions (A4 a
T1-candidate under-tiered at T3; A5 a no-participants discussion piece over-tiered; A2 the same
dataset admitted twice; A3 a circular value; A6 a wrong R14 zero-yield diagnosis). Its own synthesis:
*"a claim pitched at a confidence the retrieval didn't earn."* **That session is the standard form.**

**The agonist already exists and costs nothing extra.** R1–R15 already compel the authoring session
to file its complete affirmative case *as rows* — verbatim queries, re-retrieved locators, match
grades, prior expectation, named dissenter, falsification condition. There is no live debate to
build: the agonist's brief **is the batch's data.** The antagonist is a fresh session attacking that
recorded case. The cheapest agonist–antagonist mechanic is **blind-then-compare**: re-grade tier and
population-match independently *before* seeing the author's grades, then diff. That is precisely what
caught A4 and A5.

**Eight lenses**, each naming its claim and its evidence obligation: **L1 Existence** (source
resolves) · **L2 Fidelity** (the source *says* what is claimed; the locator holds the value) ·
**L3 Independence** (same dataset twice; circular values) · **L4 Tier** (wrong in either direction,
incl. R5 non-English) · **L5 Population** (study vs served) · **L6 Contrary** (was "NONE FOUND" a
search failure) · **L7 Recognition** (Co-1 cited faithfully; would a disabled person served by this
recognise it) · **L8 Query-shape** (R14).

**Adjudication without a third agent** — adding a judge adds a loop stage. Sustained and accepted →
row correction by migration **in the same pass**. Disputed → the cell caps at `provisional` with the
dispute recorded. Doctrine-level → the owner. **L5 needs no schema change**: `evidence_population_match`
has only `match_id` as its primary key, so a dissenting grade lands as a second row distinguished by
`created_by_session`, and divergent grades read as a contest.

**Optional single migration:** an `adversarial_findings` table in which **`SURVIVED` rows are
mandatory** — so a zero-finding pass is auditable rather than indistinguishable from a pass that
never ran. That targets this repository's signature failure directly.

**Cost:** ~15–25%, front-loaded onto the claims that ship. Exhaustive on every `stated`
determination, every synthesis doc, and every mechanically flagged source; sampled at ~1 in 3 for
full-read fidelity and 2–3 queries per batch for L6/L8.

The binding rule is appended to `references/project-standards.md` in the same PR.

## §8 The four documents

A fresh session reads exactly four. Everything else is reached by citation.

1. **`CLAUDE.md`** — mechanics, gates, the write path.
2. **This DR** — the binding instrument: freeze, items quarantine, identifier stash, adversarial
   architecture, execution order, acceptance criterion, and the supersession pointers below.
3. **`workplan/2026-08-18-research-restart-plan.md`** — the batch procedure, with §4 criterion 6
   struck and §8's runbook appended.
4. **`workplan/2026-08-18-handoff-next-session.md`** — orientation, the six settled rulings, the
   corrected record, the eight traps. **Its §6 sequence is read as history**; this DR §3 supersedes it.

**No fifth document may join this set.** That is the termination property, not a preference.

## §9 The owner-decision batch — one sitting

| # | Question | Recommended | Unblocks |
|---|---|---|---|
| **OD-1** | Ratify this DR as amended — freeze supersession + amnesty + items-as-leads + §3 order + §4 criterion + the mechanical check | **RATIFIED 2026-08-19.** Every clause extends a ruling already made; the only novelty is enforcement and a reachable exit | Everything — §3 steps 2 and 3 executed; step 4 (the batch) is now the next act |
| **OD-2** | R5 bucket fill order (D-OP) + R6 §2.3 amendment (D-DOCT, needs its own DR; keep ruling and disclosure clause separate) | **Ratify as drafted**, noting the bucket 4/5 split is authored, not the owner's words | Scale-out past batch 1 |
| **OD-3** | O1 — ICF expansion by chapter-level enumeration, interim floor 51 | **Chapter-level.** The axes' 46 omits the entire d5 self-care chapter | The demand lens |
| **OD-4** | O2 — slug queue by readiness (aliases exist, leads exist) vs importance | **Readiness.** Importance is circular before searching | Queue for batch 2+ |
| **OD-5** | §6 scope: extend the identifier stash from 835 to ~4,081; do title/year/author ride along? | **Extend; yes to metadata**, marked as re-findability aids | R9 can function at all |
| **OD-6** | D6 `.ignore` edit (with the `exempt_paths` pairing) and MOVE `workplan/deprecated/` per the census | **Approve** — 7,480 lines off the search surface, two-line reversal | Search-surface safety |
| **OD-7** | D2 retire the decisions YAML · D5 schemas mirror SQLite · D7 add the blocking `PRAGMA foreign_key_check` gate | **Yes × 3.** D7 especially — nothing blocking observes referential integrity | Kills a dual store; makes later FK work safe |
| **OD-8** | D1 workplan keep-set (census answer: 1 active + 9 attestation-pinned; 77 move) | **Approve now, execute after the batch** | Phase 5 |
| **OD-9** | Required-check set on `main` + D3 (merge the two reproducibility gates, deep as blocking) | **Approve in principle, wire AFTER the batch** — the gate needs non-zero subjects first | The repo's entire real access control |
| **OD-10** | The close-out DR of §10 | **SIGNED 2026-08-19.** Item 4 executed the same day; items 1-3 and 5-9 are recorded closed; item 10 proceeds under the owner's ruling that `_archived/` may grow | Removes every zombie obligation |
| **OD-11** | G6/I-45 — the Universal/Population doctrine tension, invisible since 2026-07-13 | **Explicit deferral**, recorded — never silently dropped again | Prevents a seventh invisible week |
| **OD-12** | Step 8 / `jurisdictional_values` disposition (§1.5) | **Defer, recorded.** Items-archival SUSPENDED pending post-batch re-pricing against F1 | Makes the schema track safe to reopen |

OD-1 through OD-7 are yes/no against drafted text. Under an hour.

## §10 Abandonment — one close-out DR

> **SIGNED by the owner 2026-08-19 (OD-10).** Item 4 is EXECUTED: the `[DOCTRINE: <sha>]` commit
> token, its CI step, `scripts/ci_helpers/check_doctrine_token.py`, the frozen recheck counter
> `data/doctrine_recheck/working_session_counter.yaml` and the "any doctrinal revision" recheck
> trigger are removed. The `doctrine_recheck --cross-ref` CHECK is deliberately **retained** — it
> validates doctrinal_basis cross-references, which is a different thing from the commit token and
> is not named by item 4. Item 10 proceeds under the owner's ruling that `_archived/` may grow.
> This is the first use of the supersession mechanism in 163 decisions.

Killed together, each with a reopen condition. This also breaks the **0-of-163-ever-superseded**
pattern by *using* the supersession mechanism the protocol has never once employed.

1. The 07-14 pilot program — **SUPERSEDED-DEAD**; substrate destroyed by `DR-2026-08-06`.
2. External-review outreach obligations — owner **DECLINED** 2026-07-14, yet the queue files still
   read as owed. **ABANDONED**, consequence carried to any future publish gate.
3. I-10's full COLD discharge — **DEVIATION-ACCEPTED** (partial), brief restated honestly.
4. The doctrine-token apparatus, the frozen recheck counter, the mandatory `next_action`, and the
   "any doctrinal revision" recheck trigger — **ABOLISHED** per §2.3 and the cull route §15.4.
5. The 19 stale PENDING reviews (~110 days) — **bulk ADJOURNED**; reopen when the subject repopulates.
6. The 20-claim digest — already dead; recorded as such.
7. The reconciled findings register's snapshot — **HISTORICAL**; method retained, **R-12** and
   **R-17b** transferred forward, the rest verified resolved or absorbed.
8. The 061–066 re-prototyping debt — **LAPSED**; §5's allocation table alone survives.
9. The PART 3 substitute-model artifact — **CLOSED**, discharged; the committed-path rule is its residue.
10. The workplan backlog beyond the D1 keep-set (77 files) — **ARCHIVED post-batch**, never stubbed
    where attestation-pinned.

## §11 Termination — the five properties

This is the last plan **iff** all five hold. Each is checkable.

1. **Self-expiring authority.** The freeze dies automatically at `evidence_sources ≥ 1`. No lift
   ceremony exists to be planned, breached, or adjudicated — the 2026-07-14 failure mode is
   structurally absent.
2. **Externalised acceptance.** §4's criterion cannot be met by any script, check, register, DR, or
   plan. Apparatus stops being a locally valid move the moment this is the metric.
3. **Mechanical successor-prohibition.** ~~The §2.2 check fails any commit adding a `workplan/`
   file or a registry entry while `evidence_sources` is empty.~~ **SPENT 2026-08-19.** It held
   until the first batch landed and then self-expired at `evidence_sources >= 1`, which is what it
   was built to do; the check was retired the same day. This property was true while it mattered
   and is now historical. **A successor plan is no longer build-rejected** — nothing mechanical
   prevents one, and a reader should not assume otherwise.
4. **A monotone document set.** Via §10 this instrument only *closes*. Every outstanding obligation
   is exactly one of: done, in the §9 batch, or killed. It opens zero new DEFERRED/PENDING markers —
   inverting the 318 → 389 → 418 curve for the first time.
5. **Its successor artifact class is data.** The operational test: **if the first session after
   ratification commits anything other than the §3 fixes, the record-correction PR, search logs,
   migrations, or the rendered determination, the plan has failed its own termination property** —
   and the check makes that commit fail rather than relying on anyone noticing.

*This DR still proposes no successor document, and none is owed. The next artifact is a search log.*

---

# §12 THE RUNBOOK — run this

Absorbs `workplan/2026-08-18-research-restart-plan.md` §§2–3, §5. Every command is literal.

## §12.0 Four defects fixed first — one PR, before any research

### F3/F4 — the write path. **Ruling: session-scoped scratch DB, not `--emit-sql`.**

`--emit-sql` was the obvious fix and it loses. `db.py`'s write functions are **validators, not
renderers**: `log_search()` (`scripts/db.py:328-417`) does a live `SELECT 1 FROM evidence_sources`
before writing an admission edge and needs `cur.lastrowid` to key the junction;
`insert_evidence_source()` (L1638-1659) does live duplicate-ref_id and duplicate-DOI lookups — **R9
enforcement *is* a DB query.** Rendering SQL without a live DB either drops those refusals or
reimplements them against a database, which is the scratch approach with extra steps and ~200 LOC of
dual-mode surgery through a 1,881-line file.

`db.py` already honours `GUIDEBOOK_DB_PATH` (L41) — the repo's ratified redirection mechanism.
Point it at a scratch copy: every write-time refusal stays live (R9, H05/H07, D-0157, CHECK
constraints), real `exec_id`s are allocated, and because the canonical research tables are empty the
delta is trivially extractable. **The canonical DB is opened read-write by nothing but `migrate_db.py`.**

Also reject "ratify db.py-then-reconcile": the blocking reproducibility gate compares `user_version`
plus six table counts, and **`search_executions`, `search_admissions`, `search_candidates`,
`evidence_population_match` and `jurisdictional_values` are not among the six** — a direct batch that
failed to reconcile would be invisible to the only blocking gate.

**New: `scripts/research/emit_batch_sql.py` (~180 LOC).**
`--scratch <path> --canonical data/guidebook.db --out batch.sql`. Opens both `mode=ro`. Walks a
fixed FK-ordered table list (`evidence_sources → source_slug_links → search_executions →
search_admissions → search_candidates → evidence_population_match → citation_mining →
jurisdictional_values → economics_entries → case_studies → gaps`), emitting INSERTs for PKs present
in scratch and absent in canonical (explicit column lists, explicit PKs, ordered by PK for
determinism) and UPDATEs for PKs present in both that differ. Its output feeds the existing
`emit_data_migration.py --input`, which runs its own ENUM/RANGE guards. **The scratch DB is the
capture path** — no `db.py` change is needed for it.

**F4 in `db.py` (~25 LOC).** Delete L61 (`PRAGMA journal_mode=WAL`) outright — it is the only
*persistent* pragma in `connect()`, and it flips the committed blob's header on every invocation
including pure reads. Add `readonly=True` opening `file:{DB_PATH}?mode=ro` with `PRAGMA
query_only=ON`, and flip the 15 pure-read call sites (`next_con_id` L112, `next_gap_id` L150,
`next_term_id` L421, `next_conf_id` L597, `is_mined` L203, `get_open_gaps` L440, `get_connections`
L456/477, `get_unmined_sources` L482, `get_coverage_completeness` L514, `get_synonyms` L571,
`get_conflicts` L661, `get_items` L699, `get_audit_runs` L753, `get_unmined_for_all_slugs` L1688,
`get_unmined_gaps` L1861).

**Owned honestly:** `db.py` has **no subcommand at all** for `search_candidates`,
`evidence_population_match`, `jurisdictional_values` values, `economics_entries`, `case_studies`; and
`add-source`'s `_ES_COLS` whitelist (L1587-1603) **excludes `url`, `pages`, `article_number`,
`standard_number`, `notes`, `doi_resolution_outcome`**. R3, R10, R12 and R13 therefore cannot be
satisfied through the CLI as it stands. Under the scratch approach this survives — those writes are
hand-written SQL against the scratch, validated by STRICT CHECKs at write time and emit's guards at
migration time. Batch 2 promotes the recurring ones (§12.8).

### F5/F6 — transactions. **The ordering that cannot break.**

F5: the migration file carries its own `BEGIN TRANSACTION;…COMMIT;` (`emit_data_migration.py:777`),
so `executescript` commits the body *inside the script*; the ledger INSERT commits separately; and
the post-hoc FK gate runs **after** `conn.commit()` — a "rolled back" FK failure leaves bad data
committed. F6: schema migrations have no wrapper, and the naive fix breaks because 057/058/060
contain their own `PRAGMA foreign_keys = OFF/ON` and **that pragma is a silent no-op inside a
transaction**.

Open with `isolation_level=None` (true autocommit). Add `_split_statements()` using
`sqlite3.complete_statement` (quote- and comment-aware, so a title containing `;` cannot desync it)
and `_hoist_pragmas()` stripping `PRAGMA foreign_keys` and `PRAGMA user_version` out of the body.
Then, for a data migration:

```
1. PRAGMA foreign_keys=OFF          # autocommit → takes effect
2. pre = set(PRAGMA foreign_key_check)
3. BEGIN IMMEDIATE
4. execute body statements          # wrapper stripped
5. new = set(PRAGMA foreign_key_check) - pre    # a read; legal inside the txn
   if new and not bootstrap: ROLLBACK; PRAGMA foreign_keys=ON; raise
6. INSERT INTO data_migrations (...) VALUES (?,?,?,?)   # same txn
7. COMMIT                           # body + ledger become visible atomically
8. PRAGMA foreign_keys=ON
```

Schema migrations take the same shape, with `PRAGMA user_version = N` **inside** the transaction —
it lives in the DB header and is fully transactional, so DDL and version stamp commit or vanish
together. **`emit_data_migration.py:777` drops the wrapper** (`body = sql`); `--no-transaction`
becomes an accepted no-op. The five already-committed data migrations are immutable, so the runner
strips one leading `BEGIN;` and one trailing `COMMIT;` line before splitting. ~70 LOC + 1 line.

### F9 — the three unproven rules

`research_batch_dod.py` seeds 12 of 15. R9/R12/R15 are implemented (L432-442, L476-490, L534-543) and
**never observed to fire**. Seed: R9 — two `evidence_sources` rows sharing a DOI, one from a prior
session, both tier 6 with `article_number` set so they perturb no other rule's arithmetic. R12 — one
`search_executions` row whose `findings_note` contains a cost trigger word with `economics_entries`
empty, `exec_id=4` to preserve the R8 gap and `results_screened=50`. R15 — one `search_candidates`
row `disposition='ADMITTED'` with no `RESOLVED` note. **State the interaction in the commit:** the
R15 candidate raises `cand` to 1 and R7 fires only while `cand < max(1, screened//25)`; total
screened 55 → expected 2 > 1, so R7 still fires. Lower the R12 fixture below 50 and R7 goes silent —
which the selftest will then fail on, correctly. Finally set `expected = {"R1"…"R15"}`.

## §12.1 The batch, command by command

`S=session_2026-08-19-research-batch-01-room-acoustic-performance` (**bare stem** — the DB stores
stems; only pointer files and `emit_data_migration --session` take `.md`).
`SCRATCH=<scratchpad>/batch01.db`. **The harness resets env between shell calls — prefix every
`db.py` call inline with `GUIDEBOOK_DB_PATH=$SCRATCH`; `export` does not protect you.**

Slug context, verified: 13 items, 4 axes (AX-AUD ×13, AX-SPR ×9, AX-PAI ×2, AX-VIS-N ×1), 10
populations (DEM 8, NDV 7, BRAIN 7, MH 5, PAIN 4, AUT 4, ALL 3, COM 2, SCI 1, MOB 1), 5 access needs,
**225 distinct aliases across 14 languages**, 5 `jurisdictional_values` rows on A-04 (values cleared).

**Step 0 — pre-state.**
```
sha256sum data/guidebook.db                                 # must not change until step 11
python3 scripts/audit/research_batch_dod.py --selftest       # SELFTEST: PASS, 15/15 after F9
python3 scripts/audit/research_batch_dod.py --session "$S"   # EXPECT exit 1, exactly ONE failure: R1
python3 scripts/tests/test_db_integrity.py                   # record RESULTS: X/Y
python3 scripts/migrate_db.py --rebuild /tmp/rebuilt-pre.db
python3 scripts/audit/table_connectivity.py                  # record 0 of 80
```
An empty session trips **R1 only**. Any other rule firing pre-batch means the session id is contaminated.

**Step 1 — scratch.** `cp data/guidebook.db "$SCRATCH"` (safe: `journal_mode=delete`, no sidecars).

**Step 2 — pull the frame (R4, R11).** All reads against `$SCRATCH`, never canonical:
```
GUIDEBOOK_DB_PATH=$SCRATCH python3 scripts/db.py items --category A
GUIDEBOOK_DB_PATH=$SCRATCH python3 scripts/db.py synonyms --item A-18
GUIDEBOOK_DB_PATH=$SCRATCH python3 scripts/db.py synonyms --item A-08 --language DE
GUIDEBOOK_DB_PATH=$SCRATCH python3 scripts/db.py coverage --slug room-acoustic-performance
```
plus one `mode=ro` join over `item_axis_links` / `item_population_links` / `access_need_axis_map` /
`lang_jur_map`. Output: the query plan — populations × languages × tier bands, `terms_used` term_ids per query.

**Step 3 — log every query verbatim BEFORE screening (R8), tier-ordered (R1: Co-1 → Co-2 → T2 → T1 → T4-T6).**
`results_screened`/`results_admitted` stay 0 until step 7.
```
GUIDEBOOK_DB_PATH=$SCRATCH python3 scripts/db.py log-search \
  --slug room-acoustic-performance --language EN \
  --query-text 'autistic adults lived experience classroom noise reverberation participatory' \
  --engine web --depth-method scoping --target-tier 1 --target-evidence-type co1 \
  --target-scope intrinsic --terms-used '["TERM-0012","TERM-0031"]' \
  --results-found 14 --session "$S"
```
Variants: `--target-evidence-type co2` (OT professional-body CPG); `--target-tier 2
--target-evidence-type sr_meta --engine pubmed`; `--target-tier 1 --engine pubmed`; non-English code
work `--language DE --jurisdiction DE --target-tier 5 --target-evidence-type national_fw --engine
registry --query-text 'DIN 18041 Hörsamkeit in Räumen Nachhallzeit'`. A kept zero-yield:
`--results-found 0 --findings-note 'ZERO-YIELD: query-shape failure — PubMed AND-chained 4 concepts;
re-run split'`. A deliberate non-search: `--deferred-reason '…'`.
**Traps:** `--depth-method` is only `scoping|systematic` (citation chases are `--mining-direction`);
a zero-yield row without a `findings_note` fails R14; if Co-1 retrieval is genuinely impossible the
waiver is the literal token `--findings-note 'CO1-NOT-APPLICABLE: <reason>'`.

**Step 4 — screen and stage (R7, R15).** No CLI; scratch SQL. `disposition ∈
REHOME|MISCELLANEOUS|PENDING-VERIFICATION|OUT-OF-SCOPE|ADMITTED`. R7 floor: ≥1 candidate per 25
screened. **A staged description is a HYPOTHESIS** — it gets re-described from the source at step 7.

**Step 5 — DOI pre-check (R9).** Per candidate, against the scratch and — once §6 lands — against
`source_locators` case-insensitively. An `evidence_sources` hit means cross-file; a lead hit means
admit reusing the stash ref_id.

**Step 6 — re-retrieve every locator (R10).** `curl -sI https://doi.org/<doi>` → Crossref
(`api.crossref.org/works/<doi>`) → PubMed esummary → publisher → repository. Record which rung
resolved; it becomes `verified_by_tool` and `doi_resolution_outcome`. **A publisher block is not a
terminal answer.**

**Step 7 — admit (R3, R5), then enrich.**
```
GUIDEBOOK_DB_PATH=$SCRATCH python3 scripts/db.py add-source \
  --ref-id REF-00001 --authors 'Kanakri S; Shepley M' --year 2017 \
  --title '…' --tier 1 --doi 10.xxxx/yyyy --evidence-type clinical --lang-detected en \
  --metadata-quality COMPLETE --verification-status VERIFIED \
  --verification-method tool --verified-by-tool crossref \
  --slug room-acoustic-performance --local-ref-id RAP-01 --session "$S"
```
(`COMPLETE-STATUTORY` for T4-T6; `--verification-method ∈ tool|corroborated-not-retrieved|
co1-attestation|citing-bibliography`; `tool` requires `--verified-by-tool`.) **Then the mandatory
companion UPDATE**, because `_ES_COLS` cannot carry these:
```sql
UPDATE evidence_sources SET doi_resolution_outcome='RESOLVED', pages='e0189087', url='…'
 WHERE ref_id='REF-00001';
-- T4-T6: article_number='§5.2', standard_number='DIN 18041:2016', or notes='[UNVERIFIED-QUANT] …'
```
**Without `doi_resolution_outcome='RESOLVED'`, every VERIFIED DOI-bearing source fails R10.** Then,
in one transaction: `UPDATE search_executions SET results_screened=…, results_admitted=…,
admitted_ref_ids='[…]'`; `INSERT INTO search_admissions (exec_id, ref_id, …)`; `UPDATE
search_candidates SET disposition='ADMITTED', notes='RESOLVED: re-described from source — …'`. The
JSON array, the junction rows and the count must agree exactly (H03/H04/H05, blocking). `RESOLVED:`
is R15's literal predicate.

**Step 8 — population grading (R13).** One `evidence_population_match` row per tier-1..3 admission.
Grades `EXACT|PARTIAL|PROXY|MISMATCH`. Children-for-adults, chamber tests and general-population are
**PROXY at best**, with the mismatch note written. No match row = silently claiming study and served
populations are the same.

**Step 9 — mine (R2).** Floor `admissions//4`, min 1: `db.py log-mining --direction backward|forward`,
and log the chase itself as a search row with `--mining-direction`.

**Step 10 — route by class (R12).** ~~Code values → `jurisdictional_values` (5 cleared rows on A-04
await backfill).~~ Economics → `economics_entries`. Case studies → `case_studies`. **If a
`findings_note` contains cost/grant/bcr, a structured row is owed** — that is R12's literal trigger.

> **STOP — 2026-08-22. Do not write a value into `jurisdictional_values`.** The struck clause above
> instructs a write the owner's **2026-08-12 REFERENCE-ONLY ruling forbids**: the table names which
> document to go and get, never what it says. On 2026-08-21 a session followed this clause, wrote 12
> rows marked `[UNVERIFIED-QUANT]`, and was caught by the blocking `test_db_integrity` L02 cardinality
> parity (109 YAML records vs 121 table rows); `data_20260821185514` retracts them. Live state: 109
> rows, and `value_text` / `value_numeric` / `unit` / `is_code_minimum` / `spec_id` / `source_section`
> are **0 non-null of 109**. An `[UNVERIFIED-QUANT]` marker is not a licence to write where writing is
> forbidden. Code values are staged as **leads** in `search_candidates`, which is where D-1 puts them.
>
> **A table emptied by ruling looks identical to a table empty for want of data**, and until OD-G lands
> the only record of the ruling is a comment in a YAML header. Deleting the clause outright is
> **OD-G**, an owner decision (`workplan/2026-08-22-agonist-antagonist-execution-plan.md` §2); this
> notice is the interim guard, not the decision.

**Step 11 — gate, emit, apply.**
```
GUIDEBOOK_DB_PATH=$SCRATCH python3 scripts/audit/research_batch_dod.py --session "$S"   # to exit 0
sha256sum data/guidebook.db                      # MUST still equal step 0
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH" --out /tmp/batch01.sql
python3 scripts/emit_data_migration.py --session "$S.md" \
  --summary 'research batch 1: room-acoustic-performance end-to-end under R1-R15' \
  --input /tmp/batch01.sql
python3 scripts/migrate_db.py --session "$S"     # the ONLY canonical write of the session
```

**Step 12 — gate on canonical, pointers, record, commit.** DoD exit 0; `citation_mining_completeness
--session "$S.md"` → CLEAN with `Examined > 0`; write **both** `sessions/LATEST` and
`sessions/LATEST-RESEARCH`; write the session record (synthesis path → doctrine token + attestation).
**Then, and only then**, open `references/bpc-reasoning/room-acoustic-performance.md` and record
convergence or divergence as a finding.

## §12.2 Scope

**Minimum viable** (every gate non-vacuous, margin 1): 10–12 searches — 2 Co-1, 1 Co-2, 2 T2, 2 T1,
2 T5/T6 (≥1 non-English), 1 kept zero-yield, 1 deferred-with-reason; 30–60 screened; **3–4
admissions**; 2–4 candidates; 1–2 mining rows; matches on all; 1–2 `jurisdictional_values` backfills;
**0 economics rows** (and therefore no cost/grant/bcr words in any note).
**Target** (one long session): 20–30 searches across all 5 tier bands × top 4 populations
(DEM/NDV/BRAIN/AUT) × 3–4 languages; 150–250 screened; **8–12 admissions**. **Do not exceed** — the
step-7 enrichment is hand-written this time, and a failed batch of 30 remediates far worse than one of 10.

## §12.3 Acceptance

1. `research_batch_dod.py --session "$S"` → `COMPLIANT`, exit 0, **every PASS line showing non-zero
   subjects** (R13's line prints the admission count; it must equal yours).
2. `--all` → failures only at or below `research-contract-baseline.json`; `--check-baseline
   origin/main` → ratchets down only.
3. `citation_mining_completeness.py --session "$S.md"` → `CLEAN`, `Examined > 0`. **`NOTHING-IN-SCOPE`
   means the stem/`.md` mismatch bit you.**
4. `migrate_db.py --rebuild /tmp/rebuilt.db` then `migration_reproducibility.py` → exit 0, with
   `evidence_sources` / `citation_mining` / `source_slug_links` counts now equal to the batch's —
   proving the migration, not a direct write, carries the rows. Run `--deep` too.
5. `test_db_integrity.py` → no regression; specifically H03/H04/H05/H07, D01 (no dup DOIs), B03, and
   **L04** (LATEST-RESEARCH points at a session with subjects).
6. `run_checks.py --changed-from origin/main --explain` → classifies as `data`; all blocking green.
7. `sha256sum data/guidebook.db` differs from step 0; `git status` shows exactly the DB, one
   `data_*.sql`, two pointers, the session record, one attestation. **Nothing else.**
8. **The determination is rendered and readable.** This is §4's criterion; the rest is machinery.

## §12.4 Failure modes, most likely first

1. **A `db.py` call lands on canonical** — env resets between shell calls; even a read flips
   `journal_mode` to WAL. *Land F4 first; prefix inline; `sha256sum` after every phase.*
2. **R10 fails on every admission** — `add-source` cannot write `doi_resolution_outcome`. *The step-7
   companion UPDATE is mandatory.*
3. **H03/H04/H05 divergence** from hand-written enrichment. *Parity query before emitting:
   `SELECT exec_id FROM search_executions WHERE json_array_length(COALESCE(admitted_ref_ids,'[]'))
   <> (SELECT COUNT(*) FROM search_admissions a WHERE a.exec_id=search_executions.exec_id)` must
   return zero rows.*
4. **Session stem/`.md` mismatch** → gates scope to nothing and pass green. **This repo has produced
   that failure four times.** *Bare stem everywhere; check `Examined:` on every gate.*
5. **R3 unsatisfiable via CLI for T4-T6** — same shape as 2.
6. **R12 tripped by vocabulary** — "cost"/"grant"/"bcr" in any note creates an economics debt.
7. **R14/R6 misuse** — `deferred_reason` is for searches *not run*, never a findings channel.
8. **F5 window during apply** — if §12.0 has not landed, immediately verify the `data_migrations` row
   exists before doing anything else.
9. **Emit-guard false refusal** — ALL-CAPS tokens like `'PENDING'` near `doi_resolution_outcome`.
10. **New `term_aliases` without provenance** → R11 fires per row.
11. **Pointers not updated** → the blocking `citation_mining_session` gate keeps auditing the
    2026-07-26 session.
12. **Reading the reasoning doc early** — contaminates the falsification design. Nothing in steps
    1–11 needs it.

## §12.5 What batch 2 automates

`db.py add-candidate`, `add-population-match`, `finish-search` (the step-7 enrichment as one
validated transaction); extend `add-source` with `--url --pages --article-number --standard-number
--notes --doi-resolution-outcome`; harden `emit_batch_sql.py` with `--check` (re-apply to a copy and
byte-compare) and register it; a wrapper that generates the command prefix rather than typing it;
re-declare the two retired `min_items` floors.

**Permanently manual:** query design and tier targeting; screening judgment; tier and evidence-type
assignment; population-of-study grading and its mismatch note; R15 re-description from the source;
the Co-1 waiver text; anything touching `specifications` or the reasoning doc, which sits at the
Opus synthesis floor behind the B-before-E gate. The contract's premise is that these are judgment
acts machinery can only *check*.
