# 2026-08-18 — Research frame proposal

**Status:** PROPOSAL. D-SCHEMA and DG-NON — frame definition is owner-only. Nothing executed.
**Authority:** owner ruling, 2026-08-18: `items × populations` is outmoded and removed; item names are
stripped of their determinations and become research slugs; the frame is slugs, three population
lenses, multilingual aliases, and jurisdictions; research is polynomial search across them.
**Marked for Fable 5**, which is returning to improve this — §7 lists what I could not settle.

**Revised 2026-08-18** on two further owner rulings: **§9** corrects this document's own §7.6 (
`specifications` is a derived output at the end of the pipeline, not a table to re-key now), and
**§10** answers §7.3 by adopting three prioritised jurisdiction buckets, with four corrections. §8
is rewritten to match. The superseded text is struck rather than deleted.

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
**nothing in the frame supplies that priority rule.**

> **Partly answered, 2026-08-18 — §10.** The owner supplied three prioritised jurisdiction buckets of
> ten. They order the *jurisdiction* dimension and are adopted. They do not shrink the problem much:
> at 30 jurisdictions the space is ~387,000 cells and bucket 1 alone is ~129,000. Jurisdiction was
> always the smallest of the three factors. **The slug × lens product — ~12,900 cells — is the real
> queue and still has no ordering rule** (§10.6).

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
3. ~~**The prioritisation rule (§4).**~~ **ANSWERED by owner, 2026-08-18 — see §10.** Three
   prioritised jurisdiction buckets of ten were supplied. They are adopted as the *jurisdiction*
   dimension's fill order, subject to four corrections recorded in §10.1–§10.4. The slug and lens
   dimensions still have no ordering rule and §10.5 says why that is now the smaller question.
4. **Which jurisdiction count** — 12 / 27 / 48. Open as owner decision #6 since 2026-08-14.
5. **Whether `slugs` needs a type column** once item-derived topics join. A design-parameter topic
   (`corridor-clear-width`) and a population topic (`mobility-built-environment`) may not be the same
   kind of research unit, and merging them silently may be the next umbrella error.
6. ~~**Whether `specifications` survives at all.**~~ **WITHDRAWN AND CORRECTED — see §9.** My
   proposal to re-key it to `(slug, lens_type, lens_code)` was wrong in the same way the thing it
   replaced was wrong: it fixes the shape of a determination before any data exists to shape it.
   `specifications` is not re-keyed now. It is deferred to derived-output status at the *end* of the
   pipeline.

---

## 8. Sequence

**Revised 2026-08-18 after the two owner rulings in §9 and §10.** The change from the first draft is
that steps 5 and 6 are no longer "decide the prioritisation rule" and "first batch" — the rule is
decided, and the terminal steps of the *pipeline* (derive categories, then specify) are pushed out
past the end of this frame's work entirely.

| # | Step | Gate |
|---|---|---|
| 1 | Settle §7.1 (e-codes), §7.4 (jurisdiction scope — but see §10.4, the buckets largely settle it) | **owner, DG-NON** |
| 2 | Reconcile the buckets against `governance/jurisdiction-philosophy.md` §1.2 (§10.1) | **owner, DG-NON** |
| 3 | Build `icf_codes`, `jurisdictions`; rename `term_item_links` → `term_slug_links` | D-SCHEMA, one migration |
| 4 | Convert 93 items → slugs by hand; dedup 199 → *n* | research judgment, not mechanical |
| 5 | Expand `population_axis_map` → population↔ICF; retire `axes`, `item_axis_links`; archive `items` | same migration batch |
| 6 | Seed `search_coverage` with `NOT-RUN` for bucket 1 (slug × bucket-1 jurisdiction) | D-OP, no new schema (§10.5) |
| 7 | First batch, per `workplan/2026-08-18-research-restart-plan.md`, acceptance criterion per §9.5 | R1–R15 DoD gate |
| — | *Stage 6 (derive categories) and stage 7 (specify) are **not** in this sequence* | §9.3 — they have no mechanism and no input yet |

**Nothing in the cull plan blocks any of this.** They are independent, and this one is upstream of
research actually starting.

---

## 9. Correction — specifications come last, not first

**Owner ruling, 2026-08-18:** *"Specifications should be occurring after we have already done a bunch
of research, identified a whole bunch of values and figures, consolidated this data into specific
buckets, analyzed and synthesized the info in each bucket, cross-examined analyses and syntheses
these buckets against each other, and only then would we be in a position to actually derive
categories and specific items."*

**This is correct, and it invalidates my §7.6 proposal.** I proposed re-keying `specifications` from
`(item_code, population_code)` to `(slug, lens_type, lens_code)`. That is the same error one level
down: it fixes the shape of a determination before any data exists to give it a shape. The lens keys
are no more knowable in advance than the item keys were. **Recorded as a defect in my own draft, not
as a refinement of it.**

### 9.1 The ordering, mapped to tables

| # | Stage | Table | State today |
|---|---|---|---|
| 1 | Search | `search_coverage` (slug × jurisdiction, `SEARCHED`/`THIN`/`NO-DATA`/`NOT-RUN`) | **0 rows** — provisioned, empty |
| 2 | Admit sources | `evidence_sources`, `source_slug_links` | reset per DR-2026-08-06 |
| 3 | Extract values | `source_value_extractions` | **0 rows** — provisioned, empty |
| 4 | Consolidate into buckets | `source_value_extractions.parameter_canonical` | the bucketing column, nullable |
| 5 | Analyse / synthesise within a bucket | `v_value_independence`, BPC synthesis | view exists |
| 6 | **Cross-examine buckets → derive categories** | **nothing** | **no mechanism at all** |
| 7 | Specify | `specifications` | 0 rows, keyed to the axis being removed |

### 9.2 The extraction layer already supports record-then-bucket

This is the part that does *not* need changing, and it is worth stating because it is the reason the
correction is cheap:

- `source_value_extractions.parameter` is **`TEXT NOT NULL`** — free text. An extractor records the
  parameter *as the source names it*, with no pre-declared vocabulary to fit into.
- `parameter_canonical` is **nullable** — the bucket assignment is a later, separate act.
- `v_value_independence` groups by **`COALESCE(parameter_canonical, parameter)`** — *not* by
  `item_code`. Independence is already computed over the bucket, falling back to the raw string.

So stages 3–5 are built the way the ruling describes: values are recorded before categories exist, and
consolidated afterward. `item_code` survives on the extraction table as one nullable column among 48;
it is a convenience tag, not a key, and nothing groups on it.

### 9.3 Stage 6 is the real hole

Stages 1–5 are provisioned and empty, which is the correct state. Stage 7 exists and is mis-keyed.
**Stage 6 — cross-examining the consolidated buckets against each other to derive the categories — has
no table, no view, no script and no protocol.** It is the step at which the guidebook's actual
structure would be *discovered*, and it is the one step nothing in the repository represents.

Naming what it would need, without building it:

1. A record of which buckets were compared, so a comparison that was never run is not read as agreement
   (the vacuity failure mode this repo has produced four times).
2. A record of the *disagreements* — two buckets whose values diverge is a finding, and per R7 the
   failure and inadequacy cases are first-class evidence, not residue.
3. A derivation trail from a set of buckets to each category that is proposed out of them, so the
   category can be falsified by re-reading its inputs.

**I am not proposing that table now.** Its shape depends on what the buckets turn out to look like,
which is the same argument that just invalidated my §7.6 proposal. It is named here so that stage 6's
absence is on the record rather than being discovered at the moment it is needed.

### 9.4 What this changes in the frame

| Was | Now |
|---|---|
| `items` = removed axis, rows archived | unchanged — **archive now**, they bias research at this stage |
| `specifications` = re-key to `(slug, lens_type, lens_code)` | **do not re-key.** Leave it 0-row and unbuilt; it is a stage-7 output whose key is a stage-6 finding |
| The 93 stripped item names = slugs | unchanged — but their status changes meaning: they are demoted from *categories* to *questions* |

That last row is the point of the whole conversion and is worth being explicit about. `E-08 Corridor
Clear Width (≥1200 mm)` asserts a category *and* an answer. `corridor-clear-width` asserts only that
someone should go look. The conversion is a demotion, and demotion is the direction the ruling wants.

**One claim I flag rather than assert:** whether the 93 have value even as questions. They were
selected by the same process that supplied their determinations, so their *selection* may carry the
same bias their names did — 93 topics that someone already believed were the topics. The dedup pass in
step 4 is the only place that gets examined, and it should be run as "is this a real research
question?" and not merely as "does this duplicate an existing slug?"

### 9.5 The first-batch acceptance criterion must change

Deferring stages 6–7 has a direct consequence that the restart plan does not yet carry: **no
determination can be recorded until substantial research is done.** Therefore:

- `table_connectivity`'s "fully-evidenced walk" metric **cannot move** on the first batch, and a red
  or zero reading from it is the correct reading, not a failure. Anything that treats it as a
  completion signal will misreport.
- The first-batch success criterion changes from *"one determination exists"* to something the batch
  can actually reach. Proposed: **one consolidation bucket holds enough independent roots to be worth
  synthesising** — that is, `v_value_independence` returns ≥1 bucket with ≥2 independent roots, with
  the search that produced them logged per R8 including its empties.
- That criterion is measurable on day one, it exercises stages 1–4 end to end, and it does not require
  inventing a determination to prove the pipeline works — which is exactly the failure the clean-room
  reset was called for.

---

## 10. Jurisdiction staging — the buckets, assessed

**Owner proposal, 2026-08-18:**

| Bucket | Members |
|---|---|
| **1** | UN · ISO · Canada · USA · UK · Germany · Norway · Sweden · Japan · Australia |
| **2** | EU · Singapore · New Zealand · Ireland · France · Spain · Portugal · Finland · Netherlands · South Korea |
| **3** | Brazil · China · Italy · Denmark · Switzerland · Mexico · Austria · Belgium · Colombia · Chile |

**Verdict: yes — this is the right staging mechanism, and it is better than the three candidates I
listed in §7.3.** Those three (highest-population-count, lens-disagreement, existing-code-value) all
prioritise by a property you can only measure *after* searching, which makes them circular as a queue
order. The buckets prioritise by a property known in advance, and they are stable — the queue does not
re-sort itself as results arrive. Four corrections follow, in descending order of consequence.

### 10.1 J1 — the buckets conflict with a CANONICAL selection criterion (owner decision required)

`governance/jurisdiction-philosophy.md` is **CANONICAL**. Its §1.2 lists four coverage criteria for the
canonical jurisdiction set; criterion 1 is *"Geographic diversity — all inhabited continents
represented; **Global South ≥8 jurisdictions**."* The canonical table selects BD, EG, ID, IN, KE, NG,
ZA and BR on exactly that ground, each with a stated rationale (`KE — Sub-Saharan representation`,
`IN — Harmonised Guidelines; 1.4B population`, and so on).

**The three buckets contain BR alone, in bucket 3.** BD, EG, ID, IN, KE, NG and ZA appear in no
bucket. Seven of the eight jurisdictions the canonical doctrine selected *for* Global South coverage
are absent from all thirty slots.

This is not a defect in the buckets as a *sequencing* device — deferring a jurisdiction is not
dropping it. It becomes a doctrine conflict only if the buckets are read as the new jurisdiction
*list*. **Which of the two they are is a DG-NON call and I am not making it.** The two readings:

- **Sequencing (recommended).** Buckets 1–3 are the first thirty in fill order; the canonical set is
  unchanged; the seven Global South jurisdictions sit in an unnumbered bucket 4 and are `NOT-RUN`
  until reached. Costs nothing doctrinally. Costs honesty only if bucket 4 is never written down —
  so **write it down**, or the deferral is indistinguishable from a silent reversal.
- **Replacement.** The canonical set is amended, criterion 1 is withdrawn or restated, and that
  requires a DR. In a project whose doctrine centres disabled people and holds a CRPD posture, quietly
  dropping Global South coverage from a coverage strategy that named it as a reason is the kind of
  change that should be argued in the open, not absorbed as a staging decision.

I recommend the first reading and recommend writing bucket 4 explicitly in the same commit that adopts
buckets 1–3.

### 10.2 J2 — the buckets sequence only the tier stratum that cannot anchor best practice

`jurisdiction-philosophy.md` §1.3 is explicit: *"the 24-jurisdiction requirement applies to
code/standards research (Tier 4–6), not to clinical evidence."* §2.1 is equally explicit that codes
are Tier 6, the compliance floor, and that a synthesis resting on code consensus alone is a **weak-band
(○)** claim at best.

So the jurisdiction dimension governs **T4–T6 only**. Bucketing it sequences the regulatory stratum —
the layer that, per the tier system, is walled off from full-strength (●/◐) anchoring. **T1, Co-1, T2
and Co-2 search is not jurisdiction-bucketed and is not ordered by this at all.**

That matters because of what happened last time. The pre-reset corpus reached 863 sources of which
**824 had no admission edge**, and it was demoted wholesale. A staging plan that orders the T4–T6
dimension and leaves T1/Co-1 unordered will, if followed literally, reproduce that shape: a large,
tidy, well-covered pile of code values and nothing that can carry a claim.

**Corrective, and it is small:** `search_coverage` already carries `co1_attempted`, `tier5_attempted`
and `tier6_attempted` as separate flags per (slug, jurisdiction). The buckets set the fill order for
`tier5_attempted` / `tier6_attempted`. **`co1_attempted` must not be bucket-gated** — R1 puts Co-1/T2/
Co-2 first, before any admission, and that ordering outranks a jurisdiction queue. State this in the
adopting DR, because the flags make it enforceable rather than aspirational.

### 10.3 J3 — bucket 1 alone cannot lift any entry out of PROVISIONAL

`jurisdiction-philosophy.md` §2.3: *"A BPC entry is PROVISIONAL until all 24 jurisdictions are recorded
AND the Co-1 pass covers ≥9 languages."*

Measured against `lang_jur_map`, counting **primary** languages only:

| | Jurisdictions | Primary languages | New vs. prior buckets | Cumulative |
|---|---|---|---|---|
| Bucket 1 | 10 | **6** — EN, DE, FR, JA, NO, SV | 6 | 6 |
| Bucket 2 | 10 | 8 | +5 — ES, PT, FI, NL, KO | 11 |
| Bucket 3 | 10 | 8 | +3 — ZH, IT, DA | **14** |

Two consequences:

1. **Bucket 1 is 6 languages, below the ≥9 floor.** Nothing reaches non-PROVISIONAL inside it. That is
   fine and expected — but it must be *said*, or the first bucket completing will read as a milestone
   that it is not. Pair it with §9.5: the honest first-bucket criterion is coverage recorded and
   buckets consolidated, never a status promotion.
2. **Bucket 3 adds no new language capability** beyond what bucket 2 already required — it is the same
   eight languages redistributed. Bucket 3 is therefore *cheap per jurisdiction* once bucket 2 is done,
   and the marginal cost curve is 6 → +5 → +3, not linear. Four of bucket 1's ten are English-only
   (US, UK, AU, plus NZ/IE in bucket 2), which is why bucket 1 starts cheap.

This is the strongest argument **for** the buckets as proposed: they are ordered by ascending
multilingual cost, whether or not that was the intent. It is also the argument that **buckets 1+2 are
the minimum viable unit** — 11 primary languages, first point at which the ≥9-language floor is
clearable.

### 10.4 J4 — membership, verified row by row

Every bucket member was checked against three stores: the `JurisdictionCode` enum (27 codes),
`lang_jur_map` (48 jurisdictions), and `jurisdictional_values` (12 with recorded values).

| Finding | Detail |
|---|---|
| **UN is in none of the three.** | Not in the enum, not in `lang_jur_map`, no recorded values, and `standard_name LIKE '%CRPD%'` returns **0 rows**. But CRPD appears in **18 files under `governance/`** — the UN's instrument is already the project's doctrinal anchor (Co-1 co-primacy rests on CRPD Art. 4.3). **UN is a different kind of object from a standards body:** it issues rights obligations, not dimensional values. Adding it as a jurisdiction row is defensible only if the intent is to search UN work-products (CRPD General Comment No. 2, UN DESA accessibility guidance) as *sources*. Recommend `kind = international`, `instrument = CRPD`, and an explicit note that it yields obligations rather than values. |
| **9 of 30 are outside the enum** | ES, PT, FI, IT, MX, AT, BE, CO, CL. **All nine are present in `lang_jur_map`.** |
| **The buckets therefore settle open decision #6** | The three candidate scopes were 12 / 27 / 48. Bucket membership requires the **48-scope** (or 48 + UN). This closes §7.4 as a side effect — worth noting because it has been open since 2026-08-14 and was blocking the matrix sizing. |
| **ISO is a meta-code, not a country** | Already `kind: international` in the enum; carries 5 recorded standards (ISO 21542:2021, ISO 23599:2019, IEC 60118-4:2018). Bucket 1 mixes `kind` values (UN, ISO, and eight countries). **That is correct, not a defect** — the `kind` column in the §3 schema exists precisely so one bucket can hold all three. |
| **UK vs GB is inconsistent in live data** | The enum and §3.3 of the philosophy mandate `UK`; `validate_jurisdiction.py` §4.1 lists `GB` as an **ERROR**. `jurisdictional_values` stores **`GB` on 20 rows**. Either the validator is not reaching that table or the rule is not enforced there. Small, but it will bite the moment `jurisdictions` is built with a foreign key. **Fix before step 3 of §8.** |
| **Bucket 1 holds 8 of the 12 jurisdictions with existing values** | US (20 rows / 19 bodies), GB (20/17), DE (20/16), AU (18/11), ISO (13/5), NO (5/5), CA (1/1), JP (1/1). Missing: SE (0), UN (0). Bucket 2 adds FR (5/2), EU (4/4), SG (1/1); bucket 3 adds CH (1/1). **Bucket 1 is where the seed data already is**, which independently supports the ordering. |

### 10.5 The mechanism already exists — no schema change

This is the part that makes the buckets cheap to adopt. `search_coverage` is keyed
**`PRIMARY KEY (slug, jurisdiction)`** with `status` constrained to
`SEARCHED / THIN / NO-DATA / NOT-RUN`.

`NOT-RUN` **is** the bucket marker. Staging is a fill order over an existing table:

- Seed every (slug × jurisdiction) pair across the adopted scope as `NOT-RUN`.
- Bucket 1's pairs move to `SEARCHED` / `THIN` / `NO-DATA` as work proceeds.
- Buckets 2–4 sit at `NOT-RUN`, which is queryable, honest, and already the denominator §4 asked for.

**No new table, no new column, no migration for the staging itself** — only the `jurisdictions` table
from §3, which was already proposed. The bucket assignment is the one thing that could arguably be a
column (`jurisdictions.bucket`), and I recommend it: one nullable integer, so the queue order is data
rather than prose in a workplan that will go stale.

### 10.6 What the buckets do not solve

§4's arithmetic is unchanged in kind. At ~150 slugs × 86 lenses × 30 jurisdictions the space is
~387,000 cells; bucket 1 alone is ~129,000. **Bucketing the jurisdiction dimension divides the space
by three, and the space needed dividing by four orders of magnitude.**

The jurisdiction dimension was never the expensive one — 30 is the smallest of the three factors, and
per §10.2 it only governs T4–T6 anyway. **The slug × lens product (~12,900 cells) is the real queue,
and it still has no ordering rule.** The buckets answer the question I flagged in §7.3, and answering
it reveals that I flagged the wrong dimension.

What would order slug × lens is a genuinely different kind of rule, and it is the next thing to decide
after this frame lands. It is left open here deliberately, and marked for Fable 5 alongside §7.1 and
§7.2.
