# The rename — every open decision, argued both ways, resolved on measurement

**Owner instruction 2026-08-27:** *"Perform carefully all agonist-antagonist."*

Method, as established this session: the agonist states the case for the position on the table; the
antagonist attacks it; **the resolution binds to a measurement, never to preference or authority.**
Where no measurement reaches, the contest is declared owner-owed rather than settled quietly.

Measured against `user_version` 64, read-only, 2026-08-27. Commands inline.

---

## C-A · `base_building` — one table, or three?

**AGONIST (three tables).** J.4's rule: a new table is warranted only when the ROW-KIND is new. A
building type (*residential*), a room type (*kitchen*) and a component (*door handle*) are three
different kinds of thing with three different attribute sets. Three tables — `base_building_types`,
`base_room_types`, `base_elements` — keep each one's columns honest and every foreign key real.

**ANTAGONIST.** Two objections, and the second is the owner's own words.

1. **The owner said "that table", singular** — *"Building types…, room types…, construction elements
   … are what I wanted for **that table**."* Three tables is a reading, not a quotation.
2. **The owner ruled parent columns in the same breath** — *"yes, we need parent columns or however
   this would work with SQL terminology."* A parent column across three tables is **polymorphic**,
   which SQLite cannot key — the exact defect J.4 itself forbids. Within one table it is a
   **self-referential FK**, which SQLite enforces natively.

**Measured.** The cost of folding is trivial: `rooms` holds 17 rows and has exactly **one** inbound
foreign key — `room_items`, which holds **0 rows**. One empty child to re-point.

```bash
python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);
print(c.execute('SELECT COUNT(*) FROM rooms').fetchone(), c.execute('SELECT COUNT(*) FROM room_items').fetchone())"
```

**RESOLUTION — ONE table, self-referential.** `base_building(code, level, parent_code, name)` where
`level ∈ (building_type, room_type, element)` and `parent_code REFERENCES base_building(code)`.

This is the only shape that satisfies **both** owner rulings at once: it is one table, and its parent
column is a real enforceable FK rather than a polymorphic one. J.4's concern is met on its own terms —
the objection to polymorphism was that *"SQLite cannot key a polymorphic column"*, and a
self-referential parent is the case where it can.

*Three levels do differ in attributes. That is a `level`-conditional CHECK, not three tables.*

---

## C-B · The six replacement names §R8 selected are orphaned

**AGONIST (keep them).** §R8's family was ruled and only the head noun moved: `demand_code`,
`item_demand_links`, `population_demand_map`, `access_need_demand_map`, `serves_demands`,
`attaches_demands` (`project-standards.md:2171-2172`).

**ANTAGONIST.** The family was **derived from** `icf_demands`. The owner has replaced that noun with
`base_taxonomy_icf`, and `base_taxonomy_icf` does not yield `demand_code`. A derived family whose
root is gone is not "surviving in full" — **which is the overclaim R2 already caught me making.**

**Measured — and the naive re-derivation collides with a live table.** If `axes` → `base_taxonomy_icf`,
then `access_need_axis_map` → `access_need_icf_map`. But **`access_need_icf` already exists, with 43
rows**:

| table | rows | maps |
|---|---:|---|
| `access_need_icf` | **43** | `need_code` → `icf_code`, with `icf_type` |
| `access_need_axis_map` | **21** | `need_code` → `axis_code` |

They are **not** duplicates — `axes` anchors ICF **b**/**d** (person functioning) and `access_needs`
anchors **e** (environment), per the 2026-08-25 anti-fold ruling. But `access_need_icf` beside
`access_need_icf_map` is two names one letter apart for two different relationships. **That is the
`items` ambiguity again, being created on purpose.**

**RESOLUTION — the seven RETIRED tokens stand; the six REPLACEMENTS are owner-owed.** The register
entries name what is retired (`axes`, `axis_code`, `item_axis_links`, `population_axis_map`,
`access_need_axis_map`, `serves_axes`, `attaches_axes`) and are unaffected by any replacement noun.
**I will not invent the replacements** — that is the attribution expansion this session has already
committed once. Flagged with the collision measured, for the owner.

---

## C-C · Stage id — `specification` or `specifications`?

**AGONIST (plural).** The owner wrote it: *"Base Research Evidence Judgment Synthesis **Specifications**
Render."*

**ANTAGONIST.** Every other stage id is singular, and the id becomes a table prefix: the hand-off
object would read `specifications_items`. The grammar's *"head noun always plural"* rule governs
**table** names, not stage ids.

**RESOLUTION — owner-owed, recorded as written.** No measurement reaches a naming preference, and
this one is permanent and cosmetic. Recommend **singular** for prefix consistency; the owner's plural
is recorded verbatim and unaltered pending a word.

---

## C-D · One migration, or three? — **the answer changed**

**AGONIST (three: P0.6, then P1.0, then the rename).** Smaller diffs, each independently revertible,
and `REPAIR-PLAN` §1 already sequences P0.6 ahead of everything.

**ANTAGONIST — P0.6's target name is dead.** P0.6 is specified as `axes` → **`icf_demands`**. The
owner has since ruled **`base_taxonomy_icf`**. Executing P0.6 as written renames the table to a name
that is already superseded, then the full rename renames it **again**.

> **Two renames of one table is two caller sweeps.** Migration 064 exists because migration 063 swept
> eight Python readers and six skills and missed one view. Doubling the sweeps doubles that exposure
> for no benefit.

And P1.0 is free to fold in: `specifications` holds **0 rows** and `specification_source_links` holds
**0 rows**, so dropping `item_code` and `population_code` costs nothing and needs no data migration.

**RESOLUTION — ONE migration.** P0.6's *substance* executes (retire the axis vocabulary, paired
register entry, rename-then-register order) with the **ruled** target name. P1.0 folds in at zero
cost. `REPAIR-PLAN` §1's ordering is superseded on this point by a ruling that postdates it.

---

## C-E · `source_locators` — research or base? — **NOT OPEN**

Settled by owner instruction, `project-standards.md:1911`: *"Items #3 and #4 of the architecture note
are **NOT adopted** — owner instruction, same contact. `base.clues` is not moved to substrate."*

R1's independent derivation reached the same place and adds the reason: `source_locators` has **0
inbound and 0 outbound FK edges**, and the ratified DR-2026-08-06 wall says *"nothing joins it, no
determination may cite it."* A base layer that nothing may join is a contradiction in terms.
**Research. Closed.**

---

## C-F · Is P0.1 (the canonical-write guard) blocking? — **REPAIR-PLAN's premise is false**

**AGONIST.** `REPAIR-PLAN` P0.1 is unambiguous: *"safety: nothing else runs first."* A rename is the
largest write this project has attempted, and `dbcore.is_canonical()` — which exists solely to refuse
writes to the committed database — has **no callers but its own selftest**
(`scripts/dbcore.py:468-470`, verified).

**ANTAGONIST — the guard would never have been in this path.** Measured:

```
scripts/migrate_db.py:366   conn = sqlite3.connect(str(DB_PATH), isolation_level=None)
scripts/migrate_db.py:440   conn = sqlite3.connect(str(target), isolation_level=None)
scripts/migrate_db.py:504   c = sqlite3.connect(str(db), isolation_level=None)
```

**`migrate_db.py` never touches `dbcore` at all.** It opens the database with raw `sqlite3.connect`.
So:

1. The guard **cannot block the rename**, because the rename runs through `migrate_db.py`.
2. `REPAIR-PLAN` P0.1's stated consequence — *"Migrations need an explicit override; F6 specifies its
   shape"* — rests on a **false premise**. Migrations do not pass the guard, so they need no override.

**RESOLUTION — do P0.1, but NOT as a blocker on this change.** It protects against an *ad-hoc script*
writing canonical, which is a real hazard in a rename session that will run many one-off scripts —
so it is worth doing first on its own merits. But *"nothing else runs first"* is not true of the
rename specifically, and the override work it was thought to require is unnecessary. **The ordering
claim is corrected; the task is kept.**

---

## C-G · What does `items` become? — **the ruling describes a state that does not yet exist**

**AGONIST.** Ruled 2026-08-26: `items` is *"the Part-4 render rollup … **derived from** specifications
rather than keyed by them."* So it belongs in render and takes a render name.

**ANTAGONIST — it is not derived, and cannot currently be.** Measured:

| | |
|---|---:|
| inbound foreign keys on `items.item_code` | **14** |
| rows in `specifications`, from which it is supposedly derived | **0** |

**A table with 14 things keying into it and a source of 0 rows is not a rollup — it is the
vocabulary.** The ruling states a target, and reaching it requires re-pointing 14 foreign keys onto
whatever replaces the identity. That is not a rename; it is the P1.0 re-key plus thirteen more edges.

**RESOLUTION — rename `items` for what it IS, and record the derivation as unfinished.** It holds 93
**design provisions**, so a provision name is honest and a rollup name would assert a property the
schema does not have. Do not claim the 08-26 ruling is executed by renaming the table; **it is
executed when the 14 keys move.** Flag as owed.

*Second-order, same cause:* `items.category` holds **10 distinct bare letters** (`A`–`K`) and **no
category-name table exists anywhere**. The name collapse has a sibling in the category collapse.

---

## What this pass changed

| # | before | after | on what |
|---|---|---|---|
| C-A | three tables | **one, self-referential** | polymorphic parent is unkeyable; 17 rows, 1 empty inbound FK |
| C-B | "§R8 survives in full" | **six replacements are owner-owed** | the family's root noun is superseded; `access_need_icf` collision |
| C-D | three migrations | **one** | P0.6's target name is dead; two sweeps double the 064 exposure |
| C-F | P0.1 blocks the rename | **it does not** | `migrate_db.py` never calls `dbcore` |
| C-G | rename `items` to a rollup name | **rename it for what it is** | 14 inbound FKs, 0 source rows |

**Two of the five reverse a position I argued earlier in this session, and one reverses
`REPAIR-PLAN`'s own ordering claim.**
