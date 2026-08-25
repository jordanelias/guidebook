# The determination's grain — the owner's objection, tested against the record

**Raised by the owner 2026-08-25:** *"if we eliminated 'specifications' from the pipeline as a term
but still have a table, then why does it still exist? population-code × item-code is an old thing
that keeps cropping up which is a big problem because it is begging the question, ie setting
parameters before we are in a position to set them. we don't WANT to define specifications
according to a population code because we have a multimodal approach that includes ICF and access
needs, and we don't want there to be an 'item' because the specification IS the item."*

Investigated read-only before answering. Nothing below is a proposal; it is what the record says.

---

## 1. The direct answer: why the table exists

**The term was not eliminated — it was *adopted*, by owner directive.**
`decisions/DR-2026-08-12-specification-rename-and-replay-order.md`:

> **Decision by:** Owner directive 2026-08-12 (*"product cell as (item x population) is confusing
> terminology. **rename to specification**"*).

So `specifications` is the *new* name; "cell" is the retired one. What was eliminated on 2026-08-25
is `specifications` as a **stage** — `CLAUDE.md` now reads *"`specifications` is a TABLE, not a
stage — `judgment` writes it."* Both rulings stand and neither retires the table.

**But note precisely what that 2026-08-12 ruling did and did not touch.** Its own title is *"Rename
the (item × population) determination to `specification`"*. It fixed a **terminology collision**
between "cell" and the Specification layer. **It left the grain exactly where it found it.** The
question now being raised — whether the determination should be keyed on `(item × population)` at
all — was never its subject, and is therefore open, not settled.

---

## 2. The objection is correct, and the record supports it three ways

### (a) The schema contradicts the entity model

`governance/conceptual-model.md:76` and `:100`:

> `Population (ENT-11) ──── applies_to ──── Specification (ENT-01) [N:N]`
>
> **ENT-11 → ENT-01 (population → specification): N:N — a specification serves multiple
> populations, and a population is served by many specifications.**

The live schema:

```sql
item_code        TEXT NOT NULL REFERENCES items(item_code),
population_code  TEXT NOT NULL REFERENCES populations(population_code),
UNIQUE (item_code, population_code)
```

**A specification serves exactly one population, by construction.** The canonical entity model's
N:N is not merely unimplemented — it is *unimplementable* in this table. One of the two is wrong and
they have coexisted since the baseline.

### (b) R4 contradicts itself inside one line

`governance/research-contract.yaml:119`, injected into every session by the SessionStart hook:

> *"Cross slug x **population / access-need / ICF / axis**. Cells are (item x **population**)."*

**Four cross-reference dimensions named, then the cell collapses to one of them.** The multimodal
frame the owner describes is already stated in R4's first sentence and discarded by its second. Any
session obeying R4 literally is told to search across four dimensions and record against one.

### (c) It begs the question — and the project already has a rule against exactly that

`DR-2026-08-24` §2.4, an owner ruling:

> *"Every research slug gets cross-referenced against a population code, access need or ICF code
> because there is always the chance that there is an unexpected connection… **we are waiting until
> we have finished our syntheses to ensure we define them with evidenced justification, not
> presuppositions.**"*

And `CLAUDE.md` §6: **"applicability is an OUTPUT of synthesis, not an input."**

A `NOT NULL population_code` in the determination's own uniqueness key forces the applicability
decision **before the determination can be written at all**. That is presupposition in the primary
key. The owner's phrase — *"setting parameters before we are in a position to set them"* — is a
precise description of a NOT NULL constraint on a fact that doctrine says is an output.

---

## 3. "The specification IS the item" — what the model already implies

`governance/conceptual-model.md:92`:

> **ENT-01 → ENT-08 (specification → item):** Many specifications roll up into one item. The
> `item_code` field on Specification already encodes this. **Item is the Part-4 [rollup].**

So by the model's own account, **`item` is a rendering aggregate for Part 4** — a way of grouping
determinations for presentation. It is not an evidentiary object and nothing is extracted "about" an
item.

Under the owner's 2026-08-25 stage ruling — *each stage holds only its own data; anything earlier is
reached by pointer* — a `NOT NULL item_code` on a **judgment**-stage record makes a **render**-stage
construct part of that record's identity. That is a stage violation in the primary key, and it is
the same defect class as the copies retired in PR #119, one layer deeper.

The owner's formulation goes further than the model does: not "item is a rollup" but "the
specification *is* the item". The model supports the weaker claim outright and does not contradict
the stronger one.

---

## 4. What this does NOT settle

**This is DG-NON doctrine of the deepest kind and I am not deciding it.** What the record
establishes is that the current grain is *inconsistent with three other things the record says* —
not what should replace it. Replacing it is a schema question with real consequences:

- `specifications` is the table `judgment` writes; changing its key changes the judgment stage's
  entire output contract.
- `specification_source_links`, `spec_value_probes`, `case_study_specs`, `economics_entry_specs`
  and `conflicts` all FK to it.
- `v_best_practice`, `v_pending`, `v_code_floor_only`, `v_divergence` read it.
- **The zero-row state is the opportunity.** `specifications` holds **0 rows**. A grain change now
  costs a schema migration; the same change after a batch costs re-reasoning every determination.

## 5. What it does to work currently in flight

- **F5's population-split design is not wasted.** Splitting `MOB` into ambulatory and wheelchair
  user is a fix to the *populations vocabulary*, which stands whether or not the determination is
  keyed on it. The 33 substrate rows (`item_population_links`, `population_axis_map`) are unaffected
  by this question.
- **`WALK-REPAIR-PLAN.md` P1.3 is affected.** It specifies `db.py add-specification` against the
  current grain. If the grain changes, P1.3's signature changes with it. **P1.3 should not be
  implemented until this is ruled on** — and it sits behind P1.2 anyway, so the critical path is
  not lengthened by waiting.
- **P1.7/P1.8 (the value path) are unaffected.** A determination needs a value and a renderer that
  shows it regardless of what its key is.
