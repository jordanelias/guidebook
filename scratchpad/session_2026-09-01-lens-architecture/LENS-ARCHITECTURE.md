# What best supports a dynamically-rendering, multi-lens, filterable site

**Read-only investigation, 2026-09-01.** Everything below is measured against the live
database. The owner's goal, stated this session:

> a dynamically rendering website with a multimodal lens and filters so that we can have
> specifications that are presented according to which lens the user chooses and what
> filters they have selected

with three constraints given during the investigation:

1. taxonomies **abstracted** so downstream tables reference them dynamically — one fact may
   concern an ICF code *and* an identity *and* a medical code at once;
2. **absence in a lens is OK** — a link need not exist in every taxonomy;
3. but a link **MUST tie to at least one**, and **ideally ties into many**.

## The finding, in one line

**One wide link row carrying a nullable column per taxonomy, with a CHECK that at least one
is present.** The lens becomes a *column choice* at render; no traversal, no inference, no
UNION, and absence is representable.

## Why the alternative fails, measured

The obvious alternative — store the fact in ONE lens and traverse the crossing maps at
render — is what the schema is shaped for today. Two measurements kill it.

**(a) The crossings are incomplete, and every gap is a silently empty page.**

```
identity -> ICF    20/23   MISSING: ALL, ID, MOVE
ICF -> identity    16/17   MISSING: AX-COG-L
needs -> ICF       15/17   MISSING: A-AT, A-TIME
ICF -> needs       15/17   MISSING: AX-PAI, AX-THR
identity <-> needs         NO DIRECT MAP — must route through ICF
medical <-> anything       NO TABLE — D-0170 ruled it exists; it does not
```

A reader who picks the medical lens gets an empty site. A reader who picks ICF and filters
`AX-COG-L` gets nothing, silently — not "no results", but *no route*.

**(b) Traversal manufactures inference, and it changes the answer.**

Asking the identity lens for `DEAF` returns **20 items**. Asking the ICF lens for `AX-AUD` —
the axis `DEAF` crosses to — returns **38 rows**, because `DEAFBLIND` also crosses to
`AX-AUD` and is pulled in. Neither number is wrong; they are answers to *different
questions*. But only the first is a recorded fact. The second is produced by a JOIN.

That distinction is load-bearing here. `D-0174` reserves applicability to synthesis, and
`CLAUDE.md` §2(c) exists because inference hardened into fact once already. A site whose ICF
lens is a crossing traversal is **manufacturing applicability judgements in the render
layer**, where nothing reviews them and no attestation covers them.

## The recommended shape

```sql
CREATE TABLE item_taxonomy_links (
  item_code      TEXT NOT NULL REFERENCES items(item_code) ON DELETE CASCADE,
  identity_code  TEXT REFERENCES base_taxonomy_identity(code),
  icf_code       TEXT REFERENCES base_taxonomy_icf(code),
  needs_code     TEXT REFERENCES base_taxonomy_needs(code),
  medical_code   TEXT REFERENCES base_taxonomy_medical(code),
  applicability  TEXT NOT NULL DEFAULT 'applies' CHECK (applicability IN (...)),
  rationale_ref  TEXT REFERENCES decisions(decision_id),
  subtype        TEXT NOT NULL DEFAULT '',
  CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)
);
```

Proven in SQLite: the owner's own wheelchair example stores as ONE row —
`('A-42','WHEELCHAIR','d465-mobility-device','A-REACH','paraplegia')` — a single-lens fact
stores with three NULLs, and a row with no lens at all is refused.

### Render: one query shape, four lenses

```
identity   WHERE identity_code = ?
icf        WHERE icf_code      = ?
needs      WHERE needs_code    = ?
medical    WHERE medical_code  = ?
```

The lens the reader picks selects the **column**. Nothing else about the query changes.

### Filters compose without special cases

| filter | SQL |
|---|---|
| one code in a lens | `identity_code = ?` |
| several codes, OR | `identity_code IN (?,?)` |
| cross-lens, same fact | `identity_code=? AND needs_code=?` |
| cross-lens, same item | self-join on `item_code` |

### No UNION appears anywhere

A UNION would only be forced if the four taxonomies lived in **separate link tables**: every
render becomes a 4-way `UNION ALL`, every filter is written four times, and a fifth taxonomy
touches every query in the site. That is the splintering the owner already ruled against.

## What this does to the crossing maps

It **demotes them, and that is the point.** They stop being load-bearing render machinery
and become an *authoring aid*: when someone records an identity link, the crossings suggest
the ICF and needs codes that probably belong on the same row — a human or a synthesis step
confirms, and the row is written wide. Their measured gaps stop being silent render failures
and become a backlog with no user-facing consequence.

`base_taxonomy_medical` still has to exist and be populated before the medical lens renders
anything. That is content (DG-NON), not schema.

## This reverses my own parked design

Migration **065** (the seven-stage rename, parked) gives every downstream table four lens
columns with `CHECK (... ) = 1` — **exactly one lens per row**. That is now wrong: it forbids
the wheelchair row the owner described. The constraint must become
`COALESCE(...) IS NOT NULL`, i.e. **at least one, many encouraged**.

Also revised by this: my in-flight migration for `rationale_ref` was going to change only
that column's type. It should instead reshape the table to the wide form in one migration,
since rebuilding `item_population_links` twice is the double-sweep rule 4 warns about.

## What is NOT changed by this

The ten OD-B/OD-C links stay **identity-only**, with the other three lens columns NULL. The
rulings were made in the identity lens; deriving their ICF and needs codes from the crossing
maps would be manufacturing exactly the inference this document argues against. Absence is
legitimate — the owner said so — and those columns get filled when evidence or a ruling
supplies them, not when a JOIN can guess them.
