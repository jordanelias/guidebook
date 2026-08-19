# DR-2026-08-19 — The 93 items become leads; the apparatus freezes until one batch lands

**Category:** D-OP, with D-DOCT consequences · **Delegation:** DG-NON — work-product
inclusion/exclusion and trajectory are owner-only
**Status:** **PROPOSED** — this document proposes; the owner decides. Nothing here is executed.
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

1. Owner adopts or rejects this DR. *(Owner act. ~1 hour with R5/R6/O1.)*
2. Fix the write path, the read path and the two transaction defects — F3–F6 of the adversarial
   critique. *(Agent. Bounded; no schema change.)*
3. Seed the three missing DoD selftest cases (R9, R12, R15). *(Agent.)*
4. **Run the first research batch** — restart plan §§2–3, unchanged, under the §1.4 quarantine.
5. Render the determination and read it.
6. Only then: re-key or retire `jurisdictional_values`; re-scope handoff step 8 with its full
   dependency cascade; re-arm the retired `min_items` guards.

Step 4 populates `evidence_sources` and `source_slug_links` — two of the six invariant tables the
blocking reproducibility gate compares. **Running the batch first is what makes the later schema
work safe to run at all.**

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
