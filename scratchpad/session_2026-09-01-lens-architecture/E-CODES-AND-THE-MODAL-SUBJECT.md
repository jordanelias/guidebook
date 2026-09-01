# `e150` is not a lens, and the reason it isn't is doctrinal

Owner, 2026-09-01: *"e150 is building design. there are no users who use this guidebook who have
the code 'e150' apply to themselves."* · *"it does raise the point that e150 and universal design
etc etc etc all touch on the idea of utopian/idealized building design for mode population all"*

## The correction, first

I framed the 38 `e`-typed rows in `access_need_icf` as *"this project's ICF usage is overwhelmingly
environmental"* and concluded that adopting the 44 WHO domains *"would delete the environmental
dimension."* **That treats `e` codes as lens data being lost. They were never lens data.**

A lens is **how a reader identifies themselves**. `e` codes are Environmental Factors — they
describe the world. Nobody *is* an `e150`. So:

- **The 44 are right for the ICF lens, with no caveat.** The lens is person-side and `b`/`d` are the
  person-side ICF chapters. The owner's ruling stands unqualified; my caveat was misframed.
- **My "fifth lens" and "`environment_code` column on the link table" options were a category
  error** — they would have put world-facts in a table of person-facts.

## The distinction that was missing

**A lens is who the reader IS. A filter is what the reader is LOOKING FOR.**

The stated goal carries both: *"presented according to which lens the user chooses and what filters
they have selected."* `e` codes are filter vocabulary, never lens vocabulary. Getting that
backwards is what produced the wrong recommendation.

## But the filter vocabulary already exists, and it is better

`items.category`, A–K, measured against the live items:

| | domain | items |
|---|---|---|
| A | acoustics | 19 |
| B | lighting | 12 |
| C | colour, pattern, finish | 6 |
| D | plan and wayfinding | 11 |
| E | circulation and vertical movement | 14 |
| F | sensory gradient and olfactory | 8 |
| G | furniture, seating, grab bars | 9 |
| H | controls and information systems | 5 |
| I | hardware and fittings | 4 |
| K | DeafBlind, tactile, intervenor | 5 |
| J | *declared in the CHECK, zero items* | 0 |

This is **more specific than ICF `e`, not less.** `A-18 RT60 in Occupied Learning and Listening
Spaces` is `e250 Sound` made specific. `E-08 Corridor Clear Width` is `e150 building design
(public)` made specific. Adding the `e` codes on top would be a **second home for a fact
`items.category` already states** — rule 5.

## And the owner's second point is why it would be worse than redundant

`e150 building design (public)` and *universal design* both name **a building designed well for
everyone** — a modal subject. This project's own data already rejects that frame, in its own words.
`populations.description` for `BAR`:

> *"Body-size group; frame as the environment wrongly normed to an average body."*

**The defect is in the norm, not in the person.** That is the guidebook's doctrine, written down,
about the exact thing `e150` presupposes. Importing `e150` as vocabulary would import the
presupposition the project exists to interrogate.

## `ALL` is that presupposition already inside the identity lens

Measured 2026-09-01 against the live database:

| | |
|---|---|
| identity-lens rows | 382 |
| carrying `identity_code = 'ALL'` | **9** (2.4%), across **9 items of 93** |
| of those, carrying a `rationale_ref` | **0** |
| written by | 8 from `session_2026-05-11-items-population-normalization`, 1 from `session_2026-07-13-contradiction-sweep-f07-recovery` |

And `populations.description` for `ALL` reads:

> *"Item is not population-specific; applies to everyone"*

That is the utopian claim, unwarranted, sitting in the data. Nine assertions that something applies
to everyone, none of them examined, all from normalisation passes rather than synthesis. Under
`D-0175` (OD-A) every one is a use-time debt nobody has paid, and under the full-cross-product
ruling (`DR-2026-08-24` §2.4) applicability is an **output** of synthesis, never an input — which
is exactly what a blanket `ALL` asserts as an input.

`ALL` also sits in `populations.category = 'general'` beside `BAR`, `LPA` and `TALL`, which are
three real identities. A scope marker bundled with three constituencies is its own defect.

**This is DG-NON and it is the owner's.** The options are: retire `ALL` and require the nine items
to name their populations; keep it but move it out of `populations` into something that is honestly
a scope marker rather than a population; or keep it and require a `rationale_ref` on every use, so
"applies to everyone" becomes a claim someone made rather than a default.

## A real drift found on the way

`schemas/item.py` declares **`category_name: str`** as a required field — its own comment says
`"Circulation" etc.` — and the `items` table has **no `category_name` column**. So the design-domain
vocabulary A–K has names **in the Pydantic model and nowhere in the database**. `CLAUDE.md` §7:
*"`schemas/*.py` ↔ SQLite drift is a bug, not a convention."*

Which means the recommendation is not "add ICF `e` codes to items" but its opposite:

> **Name A–K in the database.** The filter vocabulary this project needs already exists, is already
> specific to the built environment, and is already scoped to what the guidebook covers. What it
> lacks is names — and `J`, declared with zero items, needs either a meaning or removal from the
> CHECK.

## Net effect on what was owed

| previously owed | now |
|---|---|
| decide where `e` codes live (items / fifth column / one ICF vocabulary) | **withdrawn** — they live nowhere; `items.category` already does the work |
| the 44 replace the coined axes, with an environmental caveat | **caveat withdrawn**; the replacement is clean |
| `access_need_icf`'s 5 person-side rows re-point at the 44 | unchanged — and 3 of the 5 map exactly (`d510`→`VW20`, `d540`→`VW23`, `d550`→`VW24`) |
| — | **new:** `access_need_icf`'s 38 `e` rows are need→design-domain knowledge; re-express them against `items.category`, not against ICF |
| — | **new:** name A–K in the database; rule on `J` |
| — | **new:** rule on `ALL` |
