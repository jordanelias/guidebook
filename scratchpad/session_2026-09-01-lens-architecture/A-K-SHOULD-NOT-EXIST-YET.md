# `A–K should not exist yet`

Owner ruling, 2026-09-01, in response to my proposing that A–K be **named** in the database.

## The recommendation was wrong, and wrong in the same direction as the two before it

I proposed *"name A–K in the database"* — which would have made a presupposition **cheap to keep
and expensive to remove**. That is the ratchet `CLAUDE.md` §1 was rewritten to stop, and it is the
third time in this exchange I have proposed entrenching a coined vocabulary the owner then ruled
against: the coined `AX-*` axes, then `e150` as a lens, now A–K. The pattern is mine, not the
repository's, and it is worth naming: **when a vocabulary already exists in the schema I have been
treating its existence as evidence that it should exist.**

## The ruling is continuous with D-0171, not new

`D-0171` (owner ruling, 2026-08-27) already carries it in its own `notes`:

> *"items.category holds 10 distinct bare letters A-K with no category-name table anywhere — the
> same collapse a second time."*

and in its rationale:

> *"42 of 93 item names carry a determination in the label because `items` conflates the element
> (door), the parameter (STC) and the determination (≥35), with no element table and no parameter
> registry to hold them apart."*

So A–K is a **fourth** conflation on a table already ruled to be conflating three things. It is a
design-domain taxonomy posited before any synthesis has run — the same defect as `ALL` in the
identity lens, the coined `AX-*` axes in the ICF lens, and `e150`'s modal subject.
`DR-2026-08-24` §2.4 is the governing rule and it is unambiguous: applicability and its categories
are an **output** of synthesis, *"not presuppositions"*.

## What A–K costs to remove, measured

**The cheap half — `items.category` is a derived copy and can go now.**

```
substr(item_code, 1, 1) = category   on 93 of 93 items
```

One fact, two homes, in the same row. That is rule 5 with no ambiguity, and dropping the column is
correct **whatever A–K turns out to be** — even if the taxonomy survives synthesis intact, it
should not be stored twice.

**The expensive half — the letter is inside the primary key of every item.**

| carrier | rows |
|---|---|
| `item_taxonomy_links` | 540 |
| `term_item_links` | 147 |
| `jurisdictional_values` | 109 |
| `items` | 93 |
| **total rows carrying an `item_code`** | **889** |

Plus `[A-K]` hardcoded in six executable files — `scripts/validate_items.py` (×4),
`scripts/db.py` (×4), `scripts/audit/graph/extract_db.py`,
`scripts/audit/graph/extract_content.py`, `scripts/audit/graph_audit.py`,
`schemas/population.py` — and in prose in `tools/evidentiary_audit.py`, `tools/README.md` and two
dashboards.

## The replacement identifier already exists, and is empty

`items.item_id` — format `ITEM-NNNN`, **NULL on all 93 rows**. `D-0141`, which created the table,
provisioned it and deferred it: *"item_id (ITEM-NNNN) nullable — formal assignment is out of
CO-0009 scope."*

So the category-free identifier was designed, provisioned, and never populated. It is the
sanctioned migration path, already on the books, waiting.

## And `schemas/item.py` contradicts the decision that created the table

`D-0141`, in its own outcome text:

> *"category_name omitted (derivable from category letter; storing it creates drift risk)."*

`schemas/item.py:32` declares:

```python
    category_name: str  # "Circulation" etc.
```

**required**, with no database column behind it. So my "name A–K in the database" would have
implemented the Pydantic model *against* the ruling that deliberately refused it. The drift is
real and `CLAUDE.md` §7 calls it a bug — but the fix is to **delete `category_name` from the
model**, not to add the column.

`J` is declared in the CHECK constraint with **zero items** — a category posited and never used.
The presupposition, visible as a hole.

## What I would do, and what I would not

**Do now, because it presupposes nothing:**
1. Drop `items.category`. It is a derived copy of the `item_code` prefix on all 93 rows (rule 5).
2. Remove `category_name` from `schemas/item.py`, per `D-0141`'s explicit refusal to store it.

Both are true whatever happens to A–K, neither pre-decides anything, and both *reduce* the
apparatus rather than adding to it — which is the direction `CLAUDE.md` §1 asks for.

**Do NOT do, because it needs a ruling:**

Removing the letter from `item_code` is a rename of every item's identity across 889 rows. It
cannot be done until something replaces it — and by the owner's own logic, nothing can, because
the categories are supposed to come **out of** synthesis and synthesis has not run.

So the question to settle is narrower than "should A–K exist":

> **Is the `A` in `A-01` a taxonomy claim, or an opaque identifier that merely looks like one?**

`D-0017` (2026-03-15) says item codes are *"Part-independent and do not change with renumbering"* —
which reads as *opaque identifier*. If that is the reading, `item_code` can stand untouched as an
arbitrary label while `items.category` goes and no taxonomy is asserted anywhere. If instead the
letter is read as a live categorical claim, then all 93 identifiers assert a taxonomy that does not
yet exist, and `item_id` is where they should move.

**That is the owner's to rule, and it is the cheaper question.** One reading costs a column; the
other costs 889 rows.
