# DR-2026-08-24 — Scaffolding is phase-specific; only table data crosses a stage boundary

**Status:** PROPOSED — awaiting owner ratification.
**Class:** DG-NON (doctrine). **Supersedes in part:** the D-1 directive as recorded in
`workplan/2026-08-20-provenance-walk-execution-plan.md` §D-1, which this generalises.

---

## §0 Why this document exists

**Four owner rulings were given in one exchange on 2026-08-23, and this document exists because I
mishandled all four differently.** One I contradicted in a committed migration by inventing an owner
directive that was never given (§1 R1). One I mis-framed as a choice between storage shapes when it
was a category error of mine (§1 R2). One I twice reported as *"not found in the repository"* when it
was in `CLAUDE.md` §6 the whole time (§1 R8). One was given in wider terms than the D-1 directive it
supersedes, and had never been written down anywhere (§1 R7).

**Two distinct failures sit underneath that, and conflating them would produce the wrong fix.**

1. **Rulings that never reached the repository.** D-1 has sat in
   `workplan/2026-08-20-provenance-walk-execution-plan.md` since 2026-08-21 — the weakest surface
   here — and R7's wider form existed nowhere. A ruling not in the repository cannot bind a session
   that did not witness it. **The fix is to write rulings down**, which is what this DR does.
2. **A ruling that WAS in the repository and still failed to bind.** R8 is recorded in `CLAUDE.md`
   §6, the file every session loads, including this one. I searched `decisions/` and `sessions/` for
   the string "axis" and reported absence. **The record was adequate; my search was not.** This is
   the more uncomfortable failure, because writing more rulings down does not fix it — and it is why
   §3 lists a corrections pass rather than only an addition.

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

### R8 — "axis" is a bad term for ICF codes
> *"I already ruled there is no 'axis' route as per that term being misleading."*
> *"I literally had a session within past week where I explicitly addressed the term axis as being a
> bad one to use for ICF codes."*

**Sustained. The ruling IS in the repository, in the one file every session loads, and I missed it
twice.** `CLAUDE.md` §6, lines 203–205:

> *"Work from the **ICF/access-need frame with codes AND names**, never from bare axis codes and
> never from population umbrellas. On 2026-08-19 a frame pulled as bare `axis_code` hid that a slug
> spanned two demand mechanisms, and four of five searches were framed on one of them."*

My first correction to this section was also wrong: I wrote that "axis route" was merely my coinage
and the axes layer was fine. **The ruling is narrower and sharper than that** — it is about the
*term* being wrong **for ICF codes**, and the schema shows why. `axes` carries `icf_b_anchors` and
`icf_d_anchors`: **the table called "axes" holds ICF-anchored demand mechanisms.** Calling them axes
hides what they are, and CLAUDE.md's worked example is the cost — a frame pulled as bare `axis_code`
concealed that a slug spanned two mechanisms, and four of five searches were built on one of them.

**The operative vocabulary is access-need + ICF code, with names**, not axis codes.

**A duplication this exposes, measured 2026-08-24 and not previously recorded:**

| Table | Rows | What it is |
|---|---|---|
| `axes` | 17 | ICF-anchored demand mechanisms under a misleading name |
| `access_needs` | 17 | the same cardinality, under the ratified name |
| `access_need_axis_map` | 21 | a map between two 17-row vocabularies |
| `access_need_icf` | 43 | need → ICF code, the frame CLAUDE.md §6 actually mandates |

**Two parallel 17-row vocabularies with a 21-row map between them is the one-fact-one-home defect at
the vocabulary layer.** Whether `axes` is retired into `access_needs` is a schema question and is
**not decided here** — it is named so it stops being invisible.

**Consequences:**
1. **"Axis route" is struck**, and so is the wider habit of framing work on bare `axis_code`.
   `item_population_links` is the route to applicability; `item_axis_links → population_axis_map` is
   doubly disqualified — wrong layer *and* the vocabulary CLAUDE.md §6 forbids working from.
2. **The "89 of 93" finding is re-framed, not discarded.** The measurement stands; the adjudication
   question — *"which route is authoritative"* — is **void**, because one side was never entitled to
   answer and was expressed in a forbidden vocabulary besides.
3. `governance/pipeline-map.yaml` BRK-20 and `workplan/2026-08-22-master-execution-plan.md` carry the
   misleading framing and are corrected.

**The process failure, stated plainly because it is the point of §0.** I twice reported being unable
to find this ruling. It was in `CLAUDE.md` — loaded into every session including this one — and I
searched `decisions/` and `sessions/` for the word "axis" instead of reading the file that governs.
**A ruling can be in the repository and still fail to bind, if the search for it is worse than the
record.**

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
