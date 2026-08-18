# 2026-08-18 — Research frame proposal

**Status:** PROPOSAL. D-SCHEMA and DG-NON — frame definition is owner-only. Nothing executed.
**Authority:** owner ruling, 2026-08-18: `items × populations` is outmoded and removed; item names are
stripped of their determinations and become research slugs; the frame is slugs, three population
lenses, multilingual aliases, and jurisdictions; research is polynomial search across them.
**Marked for Fable 5**, which is returning to improve this — §7 lists what I could not settle.

---

## 1. The ruling, and what it replaces

| Out | In |
|---|---|
| `items` (93 design parameters) as a grid axis | **Item names, determinations stripped, become slugs** |
| `specifications` = item × population | **Determination keyed to slug × lens** |
| `axes` — 17 coined names | **ICF codes directly** (`b770 Gait pattern functions`) |
| `jurisdiction` as a flat text column | **`jurisdictions`: country → 1..N standards bodies** |

### 1.1 Why the coined layer goes

The 17 `axes` collapse **46 distinct ICF codes** — 24 `b`, 22 `d`. `AX-AMB "Ambulant movement"`
swallows b770 gait pattern, b730 muscle power, d450 walking, d455 moving around, d460 moving around in
different locations. Five functional facts under one invented word.

They are not even disjoint: `AX-AMB`, `AX-WHM` and `AX-REA` all claim `b730`, while presenting as
separate categories.

This is the umbrella failure `governance/functional-taxonomy.md` §3.3 already names — *curate from the
functional layer, never coin broad umbrellas* — committed one level below where the doctrine was
looking. **Going to ICF directly roughly triples the resolution of that dimension and replaces
invented names with a vocabulary maintained externally.**

It is also nearly free: `slugs.serves_axes` is populated on **1 of 106** rows; `item_axis_links` (158)
dies with items regardless. The only real asset is `population_axis_map` (53 rows), and those expand
mechanically into population↔ICF pairs rather than being discarded.

### 1.2 Why converting items to slugs fixes a blocker rather than creating one

`term_aliases` (2,382) → `terms` (88) → `term_item_links` (147) → **items**. There is **no
`term_slug_links` table**. Deleting items outright would have orphaned all 2,382 aliases from the
research units — severing exactly the layer the ruling requires.

**Converting items into slugs carries the bridge over.** `term_item_links` becomes the term→slug link:
147 rows, 69 items, 49 terms, preserved intact.

---

## 2. The three lenses are three theories, and the schema shows it

They do not reduce to one another. The column definitions make the distinction visible:

| Lens | Example | What it asserts | Count |
|---|---|---|---|
| **Disability population** | `AUT`, `BLIND`, `MOB` | identity and community — *who a person is* | **23** |
| **ICF functional demand** | `b770 Gait pattern functions` | body function / activity, externally defined — *what the demand is* | **46** (24 b, 22 d) |
| **Access need** | `A-NOSIGHT` — *"be perceivable and operable without sight; never colour alone as a carrier of meaning"* | a **design obligation** — *what the building must do* | **17** |

A value that appears under only one lens is a finding about that lens. That is the reason for
researching all three, and it is why they must stay separate tables rather than being reconciled into
one taxonomy.

**Partial spine already exists:** `access_need_icf` (43 rows, 15 distinct codes) already maps access
needs → ICF, so lenses two and three touch. Note it carries **`e`-codes** (e150, e155, e240 —
environmental factors) alongside `b` and `d`. See §7.1.

---

## 3. Jurisdictions — country to 1..N standards bodies

The current `jurisdiction` is a flat text column and cannot express this. It must become a real table.

**Germany → DIN.** **Canada → CSA *and* the National Building Code.** The existing data already
demands the one-to-many, extracted from `jurisdictional_values.standard_name`:

| Country | Bodies already recorded |
|---|---|
| **US** | ADA · ANSI · ASA · ASME · IBC · NFPA — **six** |
| **GB** | BS · BS EN · Building Regs · HTM · BB · DfT Guidance — **six** |
| **DE** | DIN · DIN EN · E DIN · DVGW — four |
| **AU** | AS · AS/NZS — two, one of them joint with NZ |
| **CA** | **CSA only** — the National Building Code is absent, exactly as the ruling anticipates |
| CH · JP · NO · SG · EU · ISO | SIA · JIS · NS/TEK · BCA · EN · ISO/IEC |

**Proposed shape — one table, one row per (country × standard or code):**

```
jurisdictions(
  jurisdiction_id   PK
  country_code      -- DE, CA, US            (repeats across rows)
  country_name      -- Germany, Canada
  kind              -- country | supranational | international
  acronym           -- CSA · NBC · DIN · ISO · CEN        <- the short form
  full_name         -- Canadian Standards Association
                    -- National Building Code
                    -- Deutsches Institut fuer Normung    <- always spelled out
  instrument        -- CSA B651 / DIN 18040 / NBC Section 3.8   (nullable)
  languages         -- de   |   en,fr     (the languages to search this row in)
  notes
)
```

`acronym` and `full_name` are **two separate columns, never one**. Searching German sources needs
*Deutsches Institut fuer Normung* as well as *DIN*; a non-English search that only carries the acronym
misses the body's own literature. This is the same principle as the slug aliases one dimension over.

**Canada is two rows:**

| country | acronym | full_name | instrument | languages |
|---|---|---|---|---|
| CA | CSA | Canadian Standards Association | CSA B651 | en,fr |
| CA | NBC | National Building Code | NBC Section 3.8 | en,fr |

**Germany is one** — `DE / DIN / Deutsches Institut fuer Normung / DIN 18040 / de`. The US is six
(ADA, ANSI, ASA, ASME, IBC, NFPA), GB six, DE four.

Note the two are not the same *kind* of thing — CSA is an organisation, NBC is a code — and the ruling
treats them as parallel, which is right for search: both are things you search *by*. If that
distinction later needs to be queryable, it is one nullable `entity_type` column, not a second table.

**The one honest cost of a single table:** `languages` is a property of the *country*, not of the
standard, so it repeats on every row for that country and the copies can drift. At this scale — tens
of countries — that is a real but small risk, and a three-line audit comparing languages across rows
sharing a `country_code` closes it. **I recommend accepting the repetition rather than normalising into
three tables**; the second table earns its keep only if country-level attributes multiply beyond
languages.

`lang_jur_map` (70 rows, 19 languages, 48 jurisdictions) is the seed for the `languages` column. It
already carries the multi-language cases the search must respect — **CH: de/fr/it · BE: de/fr/nl ·
SG: en/zh · MA: ar/fr · EU: 10 languages.** *(Canada is not currently in that map with both en and fr
— a gap to fill, and the ruling's own example.)*


**Three incompatible jurisdiction counts exist today and one must be chosen:** 12 with recorded values,
27 in `schemas/enums.py JurisdictionCode`, 48 in `lang_jur_map`. This is owner decision #6 in the
remediation workplan, still open, and the search matrix cannot be sized until it is settled.

---

## 4. The matrix arithmetic — and the number that matters

**The polynomial:** `slugs × lens × jurisdiction`, searched in that jurisdiction's language(s), with
aliases as the query expansion *within* each cell.

| Dimension | Count |
|---|---|
| Slugs | 106 live + 93 from stripped items = **199 before dedup** |
| Lenses | 23 populations + 46 ICF + 17 access needs = **86** |
| Jurisdictions | **12 / 27 / 48** — unsettled |
| Alias expansion | 2,382 aliases, 15 languages — *within* a cell, not a multiplier of cells |

**Say the honest thing about the size.** At 150 slugs after dedup, 86 lenses and 24 jurisdictions:

> **150 × 86 × 24 ≈ 309,600 cells.**

**That space is not searchable, and no realistic amount of effort makes it so.** Even slug × lens alone
is ~12,900. The pre-reset corpus reached 4,960 `search_coverage` rows in months of work, and that
corpus was then reset for lacking admission edges.

**So the polynomial defines the coverage space, not the work queue.** It is the denominator you measure
completeness against — which is exactly what `search_coverage` is for — and it makes "we have not
looked there" a queryable fact rather than a silence. The queue itself must be prioritised, and
**nothing in the frame supplies that priority rule.** That is the first thing to decide after the frame
lands, and I have deliberately not invented one here (§7.3).

---

## 5. What must be built, what carries over, what is discarded

**Build (three tables):**

| Table | Seed |
|---|---|
| `icf_codes` (code, title, chapter b/d/e) | expand the 17 axes → 46 codes; `access_need_icf` supplies 15 more |
| `jurisdictions` (one row per country x standard/code, acronym + full_name as separate columns) | the 12 countries and ~30 bodies extracted above; `lang_jur_map` (70 rows) seeds `languages` |
| `term_slug_links` | **`term_item_links` renamed as items become slugs** — 147 rows, free |

**Carries over unchanged:** `slugs` (106) · `populations` (23) · `access_needs` (17) ·
`access_need_icf` (43) · `terms` (88) · `term_aliases` (2,382) · `jurisdictional_values` (109, cited to
their own clauses and not research output).

**Re-derived, not discarded:** `population_axis_map` (53) → population↔ICF by mechanical expansion.

**Discarded:** `axes` (17 coined names) · `item_axis_links` (158) · `items` as a grid axis.
`items` rows are **preserved to `_archived/`** — 93 names are a real inventory even with the
determinations stripped out.

---

## 6. The item conversion is manual, not mechanical

Stripping parentheses is not sufficient, and a regex would smuggle the bias through in words instead of
numbers:

| Item | Regex strip | The determination that survives |
|---|---|---|
| `E-08 Corridor Clear Width (≥1200 mm Minimum on All Primary Routes)` | `corridor-clear-width` | clean ✓ |
| `A-03 Acoustic Door (STC ≥35) at All Sensitive Space Boundaries` | `acoustic-door-at-all-sensitive-space-boundaries` | **"at All Sensitive Space Boundaries" is still an answer** |
| `A-04 Acoustic Zoning: Graduated from Arrival to Primary Occupation` | `acoustic-zoning-graduated-from-arrival-to-primary-occupation` | **the whole prescription** |

**28 of 93 names carry a numeric determination; a separate count found 23 of 93 carry a prescriptive
condition clause.** Both must go. `A-03`'s topic is *acoustic door performance*; where it applies is a
finding.

**And zero of the 93 stripped names match an existing slug exactly** — 106 + 93 = 199 topics with no
dedup. `carpet-in-corridors-and-occupied-spaces` almost certainly overlaps an existing acoustics slug.
This is the "hallway vs corridor" problem in its first instance, and `slugs` already carries `status =
MERGED` and a `merged_into` column built for it.

**93 hand re-namings and a 199-row dedup pass. There is no shortcut.**

---

## 7. Marked for Fable 5 — what I could not settle

1. **Do `e`-codes belong in the ICF dimension?** `access_need_icf` carries e150/e155/e240
   (environmental factors — building design, light). Those describe *the building*, not the person, so
   they may be a different kind of object from `b`/`d` and may not belong on the same axis. **This
   decides whether the ICF dimension is 46 codes or ~61.**
2. **Is 46 the right expansion?** I took the union of the 17 axes' anchors. The ICF `b` and `d`
   chapters hold far more codes than 46; the axes were a *selection*, and inheriting their selection
   inherits their bias at finer grain. The alternative — enumerate the relevant ICF chapters from the
   source classification — is more work and less contaminated.
3. **The prioritisation rule (§4).** ~309,600 cells is the space; nothing supplies the queue order.
   Candidates: highest-population-count first; where the three lenses disagree; where
   `jurisdictional_values` already has a code value to test against. **I deliberately did not pick
   one** — it is a research-strategy decision, not a schema one.
4. **Which jurisdiction count** — 12 / 27 / 48. Open as owner decision #6 since 2026-08-14.
5. **Whether `slugs` needs a type column** once item-derived topics join. A design-parameter topic
   (`corridor-clear-width`) and a population topic (`mobility-built-environment`) may not be the same
   kind of research unit, and merging them silently may be the next umbrella error.
6. **Whether `specifications` survives at all.** It is keyed `(item_code, population_code)` and is
   0 rows. With items gone it must be re-keyed to `(slug, lens_type, lens_code)` — which is a
   different table, not an altered one.

---

## 8. Sequence

| # | Step | Gate |
|---|---|---|
| 1 | Settle §7.1 (e-codes), §7.4 (jurisdiction count), §7.6 (specifications re-key) | **owner, DG-NON** |
| 2 | Build `icf_codes`, `jurisdictions`, `standards_bodies`, `jurisdiction_languages`; rename `term_item_links` → `term_slug_links` | D-SCHEMA, one migration |
| 3 | Convert 93 items → slugs by hand; dedup 199 → *n* | research judgment, not mechanical |
| 4 | Expand `population_axis_map` → population↔ICF; retire `axes`, `item_axis_links`; archive `items` | same migration batch |
| 5 | Decide the prioritisation rule (§7.3) | owner |
| 6 | First batch, one cell, per `workplan/2026-08-18-research-restart-plan.md` | R1–R15 DoD gate |

**Nothing in the cull plan blocks any of this.** They are independent, and this one is upstream of
research actually starting.
