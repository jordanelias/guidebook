# DR-2026-08-24 — Scaffolding is phase-specific; only table data crosses a stage boundary

**Status:** PROPOSED — awaiting owner ratification.
**Class:** DG-NON (doctrine). **Supersedes in part:** the D-1 directive as recorded in
`workplan/2026-08-20-provenance-walk-execution-plan.md` §D-1, which this generalises.

---

## §0 Why this document exists

**Four owner rulings were given in one exchange on 2026-08-23. None of them existed in this
repository before now, and one of them I had already contradicted in a committed migration.** That is
the defect this DR closes first, before any of its content: **owner rulings have been living in chat
and dying there.** D-1 has sat in a workplan since 2026-08-21 — the weakest surface here — and when
the owner said *"I already ruled there is no 'axis' route"*, a search of `decisions/` and `sessions/`
found no written record of it. A ruling that is not in the repository cannot bind a session that did
not witness it, and this session proved that by acting against one.

**Everything in §1 is recorded verbatim.** Where I extend a ruling beyond its words, §2 says so and
marks it as inference for the owner to confirm or strike.

---

## §1 The rulings, verbatim

### R1 — the ".md → table" directive was never an owner ruling
> *"I didn't rule the morning one — that was machine bundled without my notice. The evening one
> holds."*

**Consequence, and it is a correction against me.** `scripts/migrations/061_reference_stubs.sql:5`
opens *"OWNER DIRECTIVE 2026-08-23: 'anything like citation which is stored in .md should be recorded
in a table.' This executes it."* **That attribution is false.** I built a 531-row table, wired it
into three scripts, and cited an owner directive that the owner did not give. This is the same class
of error as a fabricated citation: an authority asserted for something that had none.

**The migration is not edited.** Migrations are append-only and immutable once committed
(CLAUDE.md §0.3), and 061's table was already dropped by 062. The correction lives here and in the
master plan, where a reader will meet it.

**What holds instead:** the evening ruling — clue material is *"not stored as usable for any case
unless it is being read by a researcher."*

### R2 — the storage question was mis-framed
> *"…we are supposed to be storing things in columns/fields. why are we talking about text strings?"*

**Sustained. My framing was wrong and the question dissolves.** I had put "citation text in a
document" against "citation text in a table" as if they were alternatives. They are not: `authors`,
`pub_year`, `title`, `tier_claimed`, `jurisdiction` are **fields**, and they are already stored as
columns on `source_locators` (migration 062). There is no text-blob to place. **The proposal to move
them back into a markdown clues document is struck** — it would convert structured fields into prose,
which is the direction this project spent the day reversing.

### R8 — there is no "axis route"
> *"I already ruled there is no 'axis' route as per that term being misleading."*

**Sustained, and my first reading of it was wrong.** I initially took this to retire the term
"axis". It does not, and retiring it would have overturned ratified doctrine:
`DR-2026-07-22-work-from-axes` is **ADOPTED — owner directive 2026-07-22** (*"work from axes"*), and
`DR-2026-07-23-population-schema-replace` explicitly **retains** the axes layer as Layer 1,
cross-walked from the access-needs layer.

**What is misleading is "route", and it is my coinage, not doctrine.** The axes layer exists to keep
*design demand* irreducible — POTS→STA+THR+BAL, ME/CFS→STA, MCAS→CHM, which is precisely the
distinction DR-2026-07-22 was written to stop an agent collapsing. It was never a mapping that
answers *"which populations does this item apply to."* By calling
`item_axis_links → population_axis_map` "the axis route" I turned a demand-signature layer into a
rival authority on applicability, and then proposed adjudicating between the two as if both had
standing.

**Consequences:**
1. **The term "axis route" is struck.** `item_population_links` is the route to applicability;
   the axes layer is not a second answer to that question and never was.
2. **The "89 of 93 items disagree" finding is re-framed, not discarded.** As a *measurement* it
   stands: the two structures do produce different population sets. As an *adjudication question* —
   "which route is authoritative" — it is **void**, because only one of them was ever answering the
   question. What the divergence actually measures is how far the scaffold drifts from applicability,
   which is a reason not to read it as applicability, not a tie to break.
3. `governance/pipeline-map.yaml` BRK-20 and `workplan/2026-08-22-master-execution-plan.md` carry the
   misleading framing and are corrected.

**I could not locate a prior written ruling in these words** in `decisions/` or `sessions/`. The
substance is nonetheless recoverable from DR-2026-07-22 and DR-2026-07-23, which is how the error was
caught. Recorded here so the next session does not have to reconstruct it.

### R7 — scaffolding is phase-specific, and only table data crosses
> *"Scaffolding has to be phase specific. As soon as any tools/work cross phases, they become
> illegible. This needs to be a highly procedural process where only the data in tables can hop from
> stage to stage."*

**This is the operative rule of this DR** and it generalises D-1 rather than restating it. D-1 said
no scaffolding *link* may cross into another stage. This says more:

1. **Scaffolding belongs to exactly one phase.** It is built for that phase and has no standing
   outside it.
2. **Tools and work that cross phases become illegible** — the reader of a later phase cannot tell
   what a construct meant in an earlier one, or what warranted it.
3. **Only data in tables hops from stage to stage.** Not tools, not links, not scaffolds, not
   documents.
4. **The process is procedural**, not a matter of a session's judgement at each boundary.

---

## §2 What follows — marked as inference, not ruling

These are my readings of §1 and are for the owner to confirm or strike. **They are not yet binding.**

| # | Inference | From |
|---|---|---|
| I1 | `item_population_links` is the only route to population applicability. The axes layer answers a different question (design-demand signature), so nothing needs adjudicating between them — the earlier "which route is authoritative" question is void | R8 |
| I2 | A table crossing a stage boundary must carry its own warrant, because the phase that built it will not be legible later. `rationale_ref` is that warrant, and D-0164's use-time debt is the mechanism | R7 (2),(3) |
| I3 | `source_locators` may be read across phases **because it is table data** — which resolves the earlier worry that a gate reading clue material breaks the clues rule. What may not cross is the scaffolding, not the table | R7 (3) |
| I4 | "Highly procedural" implies a named, checkable list of what may cross each boundary. **I have not written one, deliberately** — CLAUDE.md §1 puts the burden of proof on adding apparatus, and this DR should be ratified before anything enforces it | R7 (4) |

---

## §3 Corrections this DR carries

1. **`scripts/migrations/061_reference_stubs.sql:5`** — attributes an owner directive that was never
   given. Not edited (append-only); corrected here. The table it created is already dropped.
2. **`schemas/source_locator.py`** — same attribution in its docstring; corrected in place, since it
   is not a migration.
3. **`workplan/2026-08-22-master-execution-plan.md` R1/R2/R8** — framed the .md-to-table instruction
   as an owner directive in tension with another, and framed the scaffold as a "route". Corrected.
4. **The "89 of 93" finding** — retained as a *measurement*, struck as an *adjudication question*.

## §4 Acceptance

Ratified when the owner marks it so. **Nothing mechanical is added by this DR**, and that is
deliberate: R10 and R15 already gate the admission path, and §2 I4 records why no new check is
proposed until the rule is ratified.
