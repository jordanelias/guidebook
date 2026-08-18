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

**Revised again 2026-08-18** on four further owner rulings: **§10.1** is resolved — buckets 4 and 5
hold the remainder and the five buckets partition the scope exactly; **§10.1.2** amends the
PROVISIONAL gate so it no longer waits for buckets 4–5 (**the one ruling here that is a genuine
doctrine amendment and needs a DR**); **§11** splits the jurisdictions table in two so the country
itself, NGOs, advocacy bodies and municipalities are searchable entities; **§12** promotes the
academic-database register out of a skill file and into the schema.

**Reviewed 2026-08-18 by a Fable 5 adversarial pass — §13.** Eleven findings, two HIGH. **The 58%
search-effort statistic in §12.2 was wrong and is corrected**; the PROVISIONAL replacement wording
released more than the owner ruled and is pinned back; a false claim about Canada's language rows is
struck; and §7.1, §7.2 and §10.6 — open since the first draft — are settled. Corrections are made at
their own sites, superseded text struck rather than deleted.

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

> **Superseded 2026-08-18 by §11.** The owner ruled that the country itself, NGOs, advocacy groups
> and leading municipalities must also be searchable entities. That splits this one table into
> `jurisdictions` (geo-political scope) + `research_bodies` (searchable entities within it) — and in
> doing so removes the `languages` repetition cost this section concedes below. **The schema in §11
> is the live proposal; the block immediately following is kept as the record of what it replaced.**

**Proposed shape (SUPERSEDED — see §11) — one table, one row per (country × standard or code):**

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
sharing a `country_code` closes it. ~~**I recommend accepting the repetition rather than normalising into
three tables**~~ — **withdrawn: §11.2.** Country-level attributes did multiply (the `bucket` column
arrived with §10, the country-generic row with §11), so the second table now earns its keep and
`languages` lives exactly once.

`lang_jur_map` (70 rows, 19 languages, 48 jurisdictions) is the seed for the `languages` column. It
already carries the multi-language cases the search must respect — **CH: de/fr/it · BE: de/fr/nl ·
SG: en/zh · MA: ar/fr · EU: 10 languages.**

> **CORRECTED 2026-08-18 by the Fable 5 pass (§13, finding F3).** This sentence used to read
> *"Canada is not currently in that map with both en and fr — a gap to fill, and the ruling's own
> example."* **That is false.** `lang_jur_map` has carried `(EN, CA, PRIMARY)` and `(FR, CA, PRIMARY)`
> since 2026-07-24. Worse, §10.3's bucket-1 language count silently *depends* on the FR row, which is
> sourced only from Canada — so this document asserted a gap and then counted the row it claimed was
> missing. Struck; there was no gap.


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
MERGED` and a `merged_into` column. **Fable 5 pass, F9:** the columns exist, but **three rows have
ever used them** (80 ACTIVE, 23 STUB, 3 MERGED). The schema claim stands; the phrase "built for it"
was doing work the evidence does not support. Unexercised machinery at 199-row scale is a schema
affordance, not a solved problem.

**93 hand re-namings and a 199-row dedup pass. There is no shortcut.**

---

## 7. Marked for Fable 5 — what I could not settle

1. ~~**Do `e`-codes belong in the ICF dimension?**~~ **SETTLED by the Fable 5 pass — see §13, F6.
   They do not.** Two corrections to how I posed it: `access_need_icf` carries **ten** e-codes, not
   the three I listed (e115, e120, e125, e1251, e150, e155, e240, e250, e260, e340), spanning
   assistive products, building design, ambient qualities *and* human support. As lens members they
   would **duplicate lens 3** — a search for `slug × e150` is a search for design standards *by*
   design standard. **The ICF dimension is `b`/`d` only; e-codes stay as crosswalk rows and search
   vocabulary.**
2. ~~**Is 46 the right expansion?**~~ **SETTLED by the Fable 5 pass — see §13, F7. It is not, and the
   repo's own data proves it.** `access_need_icf` names **five `b`/`d` codes outside the axes' union**
   — b164, b765, d510, d540, d550 — which means **the entire d5 self-care chapter is missing from a
   built-environment guidebook's demand lens.** Washing, toileting and dressing are absent from the
   dimension meant to describe functional demand on buildings. **Interim floor is 51, not 46**, and
   the correct method is chapter-level enumeration from the source classification, owner-ratified.
   This is the clearest available demonstration that inheriting the axes' selection inherits their
   bias at finer grain.
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

**Revised twice on 2026-08-18, after the owner rulings in §9–§12.** The pipeline's terminal steps
(derive categories, then specify) are pushed out past the end of this frame's work entirely; the
prioritisation rule is decided; and three new tables join the migration because the registers they
hold already exist in prose and only need promoting.

| # | Step | Gate |
|---|---|---|
| 1 | Settle §7.1 (e-codes) | **owner, DG-NON** |
| 2 | Ratify the five-bucket fill order (§10.1.1) | owner — **D-OP**, §1.2 untouched |
| 2b | **Amend `jurisdiction-philosophy.md` §2.3** — PROVISIONAL gates on declared-bucket scope, not a fixed count; ≥9-language floor retained (§10.1.2) | **owner, DG-NON — a real D-DOCT amendment, needs a DR** |
| 3 | Fix the `GB` / `UK` split before any FK is created (§10.4) | one data migration |
| 4 | Build `icf_codes`, `jurisdictions`, `research_bodies`, `research_indexes`, `research_index_coverage`; add `jurisdictions.bucket`; make `search_executions.engine` an FK; rename `term_item_links` → `term_slug_links` | D-SCHEMA, one migration |
| 5 | Seed `research_bodies` and `research_indexes` from `skills/multilingual-research_SKILL.md` Steps 2a/2b/3 — **excluding `body_type = 'municipality'` (§11.4, F5), and after reconciling the skill's 46-jurisdiction scope against the 50-member bucket scope (F4: AT, CY, UN absent)** | transcription, not authorship |
| 6 | Convert 93 items → slugs by hand; dedup 199 → *n* | research judgment, not mechanical |
| 7 | Expand `population_axis_map` → population↔ICF; retire `axes`, `item_axis_links`; archive `items` | same migration batch |
| 8 | Seed `search_coverage` `NOT-RUN` for bucket 1; seed `research_index_coverage` likewise | D-OP, no new schema (§10.5) |
| 9 | First batch, per `workplan/2026-08-18-research-restart-plan.md`, acceptance criterion per §9.5 | R1–R15 DoD gate |
| — | *Municipality rows deferred until buckets 1–2 are under way* | §11.4 — selection is a finding, not a guess |
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
- **Amended by the Fable 5 pass, F10.** `v_value_independence` was confirmed able to report
  `independent_root_count >= 2` directly, so the threshold is measurable. But PR #103's P1 finding
  stands: **no FK, CHECK or audit enforces root registration**, so a typo in a root id silently
  *under*-counts independence. **The DoD must assert root-registration validity alongside the
  threshold**, or the criterion can be failed by a spelling mistake and passed by two rows pointing at
  the same unregistered root.

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

### 10.1 J1 — RESOLVED by owner ruling, 2026-08-18: buckets 4 and 5

**Original finding (kept for the record).** `governance/jurisdiction-philosophy.md` is CANONICAL. Its
§1.2 criterion 1 is *"Geographic diversity — all inhabited continents represented; **Global South ≥8
jurisdictions**"*, and the canonical table selects BD, EG, ID, IN, KE, NG, ZA and BR on that ground.
Buckets 1–3 as proposed contained BR alone. I flagged the conflict and declined to resolve it.

**Owner ruling:** *"Override canonical doctrine. Buckets 4 and 5 can be all the other ones from Global
South or otherwise missing."*

**On the buckets alone, this is sequence and not selection.** Criterion 1 governs *which*
jurisdictions are in the set; buckets govern *what order* they are filled. With buckets 4 and 5
holding the remainder, nothing is dropped from the set, so §1.2 stands unamended.

**But a second ruling followed and it does change the bar — see §10.1.2.** My first pass at this
paragraph concluded the ruling "costs nothing doctrinally" and that the buckets "change the order of
work, not the bar for finishing it." **That is no longer true and the correction is recorded rather
than silently overwritten**, because the difference between the two rulings is exactly the thing a
future reader needs to be able to see.

### 10.1.2 Second ruling — the completeness gate no longer waits for buckets 4–5

**Owner ruling, 2026-08-18:** *"no longer need global South to move from provisional."*

**This one is a real doctrine amendment, and unlike §10.1 it needs a DR.** The rule it changes is
`governance/jurisdiction-philosophy.md` §2.3:

> *"A BPC entry is PROVISIONAL until all 24 jurisdictions are recorded AND the Co-1 pass covers
> ≥9 languages."*

**Only the first conjunct changes. The second survives untouched**, and that is worth checking rather
than assuming: buckets 1–3 supply **14 primary languages**, so the ≥9-language Co-1 floor is
clearable without buckets 4–5. The amendment is therefore narrower than the ruling's wording implies
— it releases the jurisdiction count, not the language floor.

**Proposed replacement, parameterised rather than re-numbered:**

> A BPC entry is PROVISIONAL until every jurisdiction in **buckets 1–3** is recorded, AND the Co-1
> pass covers ≥9 languages. An entry may declare a **narrower** scope only on an explicit owner
> ruling, and **states the buckets it covers on its face** either way.

> **CORRECTED 2026-08-18 by the Fable 5 pass (§13, finding F2).** My first wording was *"every
> jurisdiction in the buckets it declares in scope"* — which lets an entry declare buckets 1–2 alone,
> or bucket 1 alone, and reach non-PROVISIONAL on twenty jurisdictions or ten. **The ruling released
> buckets 4–5. My wording released bucket 3 as well**, and did so silently, under the appearance of
> merely parameterising what the owner said. Floor pinned at buckets 1–3 above; narrowing is now an
> explicit owner act rather than an author's default.

Three reasons for that shape over the obvious alternative (*"all bucket 1–3 jurisdictions"*):

1. **It does not need re-amending when scope moves.** A fixed number is what produced the current
   problem — §2.3 says "24" while the enum holds 25 countries and the buckets now hold 50.
2. **It keeps the gate non-vacuous.** A rule that drops the jurisdiction conjunct entirely would let
   an entry reach non-PROVISIONAL on one jurisdiction. The gate still bites; it bites against a
   declared scope.
3. **It forces disclosure, which is the doctrinal point.** The guidebook's stated purpose is *"to get
   people to ask the right questions,"* and it is not an authority. An entry that reached
   non-PROVISIONAL without searching the Global South should say so where a reader can see it — not
   because the omission is illegitimate, but because an undisclosed narrowing reads as coverage. That
   is the same failure this repository has produced four times in its own gates (CLAUDE.md §10), now
   pointed at the reader instead of at CI.

**What the amendment actually costs, stated once.** Buckets 4–5 hold every jurisdiction the canonical
§1.2 selected for Global South coverage. Releasing the gate means those twenty are no longer required
for any entry to be considered complete, so in practice they become optional rather than deferred.
§1.2's *selection* is untouched on paper; its *effect* is not. **This is the owner's call to make and
it is made** — recorded here so that the DR states what it is doing rather than describing itself as
a scope clarification.

**Consequence for the buckets themselves:** they are now genuinely open-ended. Buckets 1–3 are the
working set, 4–5 are declared and unscheduled. That is a coherent position, and it is more honest
than a five-bucket plan nobody intends to finish.

**Unchanged by this ruling:** §9.5's first-batch criterion (it never depended on the jurisdiction
count), §10.2's rule that `co1_attempted` is not bucket-gated (R1 outranks a jurisdiction queue
regardless of where the completeness bar sits), and §10.3's finding that bucket 1 alone is 6 languages
— **below the ≥9 floor that survives**, so bucket 1 alone still lifts nothing out of PROVISIONAL.

### 10.1.1 The five buckets close exactly over the scope

Assigning the remainder produces an exact partition, which is a stronger result than the ruling asked
for:

| Bucket | Members | n |
|---|---|---|
| **1** | UN · ISO · CA · US · UK · DE · NO · SE · JP · AU | 10 |
| **2** | EU · SG · NZ · IE · FR · ES · PT · FI · NL · KR | 10 |
| **3** | BR · CN · IT · DK · CH · MX · AT · BE · CO · CL | 10 |
| **4** *(proposed)* | **BD · EG · ET · GH · ID · IN · KE · NG · TZ · ZA** | 10 |
| **5** *(proposed)* | **AR · CR · CY · EC · GT · MA · PE · PH · TH · UY** | 10 |

**Verified:** 50 slots, 50 unique members, and the set is *identical* to `lang_jur_map` (48) plus the
two meta-codes ISO and UN — **zero in the buckets that are outside the scope, zero in the scope that
are unbucketed**. The partition is exact.

**Bucket 4 is the canonical Global South set plus three the apparatus is already prepared for.** It
contains all seven canonical jurisdictions that buckets 1–3 omitted (BD, EG, ID, IN, KE, NG, ZA) and
adds ET, GH, TZ — which `skills/multilingual-research_SKILL.md` already carries organisation lists for
(ECDD/AASTU, GFD/KNUST, CCBRT/UDSM) and which African Journals Online already serves. Bucket 5 is the
Latin American Spanish-language remainder plus PH, CY, TH and MA.

**Language cost of buckets 4–5:** five new primary languages — **AR, BN, HI, ID, SW**. The full curve
across all five buckets is **6 → +5 → +3 → +5 → 0**; bucket 5 introduces no new language capability
at all.

**One known limitation, already flagged in the data and not a new finding.** Four members carry
`[PRIMARY-LANGUAGE-GAP]` notes in `lang_jur_map` because their official languages fall outside the
project's 19 research languages: **ZA and ET** (bucket 4) and **CY and TH** (bucket 5) are searchable
in English only — Amharic, Thai, Greek and Turkish are out of scope. Per R14 a zero-yield search in
those four is an *indexing* fact, not evidence of absence, and must be recorded as such.

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
AND the Co-1 pass covers ≥9 languages."* **The first conjunct is amended by §10.1.2; the ≥9-language
floor below is the half that survives, which is why this finding still stands.**

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

**Answered by the Fable 5 pass — see §13, F8.** Any *importance*-based ordering is circular before
searching, which is the same argument that killed the three candidates above. The only non-circular
rule is **readiness**: order slugs by (a) whether the alias vocabulary exists, since R11 hard-gates
non-English search, and (b) whether leads already exist (`source_slug_links` in the archived lead
list, `jurisdictional_values`, prior reasoning docs).

**The lens dimension needs no ordering rule at all.** R1 already fixes it — Co-1 / T2 / Co-2 first,
before any admission. So §10.6 reduces from a two-dimensional queue to a **slug queue**, which is a
materially smaller problem than the one I named.

**Independent corroboration, from the correction in §12.2.** All 19 deferrals in the pre-reset corpus
give the same reason: *no controlled alias vocabulary* for HI, AR, ID, SW and BN. Those are precisely
the five languages buckets 4–5 introduce. **Buckets 4–5 are not merely deprioritised — they are
vocabulary-blocked**, and the corpus recorded that at the moment it hit it. Readiness ordering is not
a theory here; it is what the last attempt actually ran into.

**Adopting readiness over importance is a trajectory call — owner, DG-NON.**

---

## 11. Research bodies — the country itself, NGOs, municipalities, advocacy groups

**Owner ruling, 2026-08-18:** *"I also need to be including the country itself as a jurisdiction for
generic searching as well as identify all relevant nongovernmental organizations and leading
municipalities and advocacy groups."*

### 11.1 This is not a new register — it exists, in prose, in a skill

Per CLAUDE.md §9 guardrail 3 (*don't spin up a new register — extend the existing apparatus*), the
first question is whether this already exists. **It does.**
`skills/multilingual-research_SKILL.md` carries **three prose registers**:

- **Step 2a** — per-jurisdiction codes and instruments, ~30 jurisdictions
  (`FR | Arrêté du 8 décembre 2014; Code de la Construction (CCH)`).
- **Step 2b** — per-jurisdiction beyond-code / Tier 5 bodies, ~30 jurisdictions. **This is already
  the NGO and advocacy register the ruling asks for:** Habinteg (UK), Rick Hansen Foundation (CA),
  Procap (CH), ONCE (ES), IBDD (BR), Invalidiliitto (FI), CCS Disability Action (NZ), EDF and EIDD
  (EU), CEUD/NDA (IE), KDA (DE).
- **A leading-municipality entry already exists too** — `KR | Seoul Universal Design Guidelines 2022`.

So the ruling is not *"build a register"*; it is **"promote three prose registers into a table so the
DB is canonical and coverage is queryable."** That is the same move §2 of CLAUDE.md prescribes
generally, and it is much cheaper than inventing the content.

> **Seeding caveat — Fable 5 pass, F4.** The skill enumerates **47 jurisdiction codes and declares its
> own scope as "46 jurisdictions"**, with numeric gates written against that figure (23/46, 31/46).
> **That is a fourth jurisdiction count**, and §10.4's "12 / 27 / 48" landscape missed it. Concretely:
> the skill **omits AT and CY**, both bucket members, and has no UN row. Seeding `research_bodies`
> straight from it will silently under-seed three of the fifty. **Reconcile the skill's 46 against the
> bucket scope before step 5, not after.**

### 11.2 The ruling removes the one defect I had conceded in §3

§3 proposed a single `jurisdictions` table keyed one row per (country × standard/code), and I flagged
its one honest cost: `languages` is a property of the *country* but would repeat on every standards
row and could drift. I recommended accepting the repetition.

**Adding the country itself as a searchable entity makes that recommendation obsolete, and in the
right direction.** Once the country is its own row, the natural shape is two tables, and `languages`
lives exactly once:

```
jurisdictions            -- geo-political scope. ~50 rows, one per bucket member.
  jurisdiction_code  PK  -- DE, CA, ISO, EU, UN
  name                   -- Germany, Canada
  kind                   -- country | supranational | international
  languages              -- de   |   en,fr        <- ONE row per jurisdiction, no repetition
  bucket                 -- 1..5, nullable        <- the fill order as data, not prose (§10.5)
  notes

research_bodies          -- the searchable entities WITHIN a jurisdiction
  body_id            PK
  jurisdiction_code  FK -> jurisdictions
  body_type              -- country_generic | standards_body | government
                         -- | ngo | advocacy_org | municipality | research_institute
  level                  -- national | subnational | supranational | international
  acronym                -- CSA · NBC · DIN · ONCE          <- the short form
  full_name              -- Canadian Standards Association
                         -- Organización Nacional de Ciegos Españoles
  instrument             -- CSA B651 / DIN 18040 (nullable; NGOs often have none)
  language_override      -- nullable; a body publishing outside its country's languages
  notes
```

`acronym` and `full_name` remain **two separate columns, never one** — the earlier ruling is
unchanged and applies with more force to advocacy bodies, whose full names are frequently
non-English (*Organización Nacional de Ciegos Españoles*, *Specialpedagogiska skolmyndigheten*).

**`body_type = 'country_generic'` is the row the ruling asks for**: one per jurisdiction, `acronym`
= the country code, `full_name` = the country's own name in its own language, `instrument` NULL. It
is what a generic search targets when no specific body is named.

**Canada, worked through:**

| jurisdiction | body_type | acronym | full_name | instrument |
|---|---|---|---|---|
| CA | country_generic | CA | Canada | — |
| CA | standards_body | CSA | Canadian Standards Association | CSA B651 |
| CA | government | NBC | National Building Code of Canada | NBC Section 3.8 |
| CA | ngo | RHF | Rick Hansen Foundation | RHFAC v4.2 |
| CA | government | CMHC | Canada Mortgage and Housing Corporation | Universal Design Guide |

### 11.3 Why advocacy organisations are the highest-value part of this ruling

Co-1 — lived experience and participatory design — is **co-primary with T1** under CRPD Art. 4.3, and
R1 puts it first in the admission order, *before* anything else. But the project has **no register of
where Co-1 evidence comes from.** Disabled people's organisations and advocacy bodies are the
principal publishers of it.

`search_coverage.co1_attempted` is a boolean per (slug, jurisdiction). It can record *that* Co-1 was
attempted; it cannot record *where*, and therefore cannot distinguish a thorough Co-1 pass from a
cursory one. **`research_bodies` filtered to `body_type IN ('ngo','advocacy_org')` supplies the
denominator that flag has been missing** — which is the same "a gate reporting zero may have examined
zero" problem CLAUDE.md §10 says this repository has produced four times.

**Recommendation:** build `research_bodies` in the same migration as `jurisdictions`, and treat the
advocacy rows as the priority fill, not an afterthought — they are the ones that serve the tier the
doctrine ranks highest and the apparatus currently cannot measure.

### 11.4 Municipalities need a level, not a table

A leading municipality (Seoul, and whichever others survive selection) is a `research_bodies` row with
`level = 'subnational'` and `jurisdiction_code = 'KR'`. It does **not** need its own table, and it
must **not** become its own `jurisdictions` row — a city is not a jurisdiction in the sense the
buckets partition, and admitting one would break the exact 50-member closure in §10.1.1.

> **Contradiction — Fable 5 pass, F5.** §8 step 5 seeds `research_bodies` "from Steps 2a/2b", and
> Step 2b contains `KR | Seoul Universal Design Guidelines 2022` — a municipality row. As written the
> sequence transcribes the very row this section defers. **The seed step must exclude
> `body_type = 'municipality'`**, or this deferral is prose only. Fixed in §8 step 5.

**Open, and genuinely a research-strategy question I am not answering:** what makes a municipality
"leading" enough to include. Unlike standards bodies, there is no enumerable set — every country has
thousands of municipalities and no external list ranks them by accessibility practice. Selecting them
is the same *curate-from-the-specific-layer* problem §1.1 describes, and picking them by reputation is
exactly how an umbrella gets coined. **Suggest deferring municipality rows until buckets 1–2 are under
way**, at which point the research itself will have surfaced which cities the literature keeps naming
— which is a finding, not a guess.

---

## 12. Academic indexes — the search infrastructure

**Owner ruling, 2026-08-18:** *"I should also create a table for academic
repositories/databases/etc or at least some framework so that our research phase also includes
searching academia."*

### 12.1 Half of this is already built, and the half that is missing is the measurable half

**Already built:** `search_executions.engine` is `TEXT NOT NULL` and its comment enumerates
`pubmed|crossref|scholar|biorxiv|medrxiv|consensus|web|registry|manual`. Every query already records
which index it ran against.

**Already written:** `skills/multilingual-research_SKILL.md` Step 3 carries a **21-database register**
with language coverage and run priority — PubMed · OTseeker · Consensus · Scholar Gateway · CINAHL ·
EMBASE · SCOPUS · REHADAT (DE) · J-STAGE · CiNii (JA) · CNKI (ZH) · RISS (KO) · BDTD (PT) ·
OpenEdition (FR) · BASE (multi) — plus a second "additional databases" table keyed by jurisdictions
served: AJOL, IndMED/NLM India, LILACS, EMRO Index Medicus, WPRIM, SciELO. It even carries the
governing doctrine: *"No database priority implies evidence priority… A Tier 1 study in J-STAGE
governs over a Tier 3 study in PubMed."*

**Missing:** the two are not connected. `engine` is free text with the enumeration in a *comment*, not
a CHECK or a foreign key, and the 21-database register is prose in a skill file. Consequently
**nothing can compute which indexes were searched for a slug and which were not** — there is no
denominator, so an academic channel that was never opened is indistinguishable from one that was
opened and yielded nothing.

### 12.2 The measurement that shows why this matters

> **CORRECTED 2026-08-18 by the Fable 5 pass (§13, finding F1). The original claim was wrong and is
> struck below rather than deleted.** I reported *"`web` + `manual` = 49 of 84 — 58% of all recorded
> search effort was general web search or unspecified manual work."* I never read the rows. **All 19
> `manual` rows are deferral records, not searches** — every one carries an explicit
> `deferred_reason` and a `[DEFERRED]` query stub. Counting them as search effort was the error, and
> it is the same error this repository documents four times over: a count read without checking what
> it counted.

The pre-reset corpus (`_archived/data/corpus-pre-reset-2026-08-06.db`) holds **84 `search_executions`
rows — 65 executed searches and 19 logged deferrals**:

| engine | executed | note |
|---|---|---|
| web | 30 | |
| pubmed | 15 | |
| scholar | 12 | |
| crossref | 3 | |
| consensus | 3 | |
| registry | 2 | |
| **manual** | **0** | **19 rows, all deferrals with a stated reason** |

**Corrected figure: web = 30 of 65 executed searches, 46%.** Not 58%, and the second-largest category
does not exist.

**What survives, and it still answers the ruling.** Of the 21 registered databases, **exactly two**
(PubMed, Consensus) were used. CINAHL, EMBASE, SCOPUS and OTseeker — the *English* specialist
databases the register marks "All runs" — recorded **zero**. So did every non-English index.

**What does not survive.** My sentence *"nothing could compare the two because one was prose and the
other was a free-text column"* is contradicted by the corpus itself. The 19 deferrals each state why,
in the field built for it: **no controlled alias vocabulary for HI, AR, ID, SW or BN.** Those are not
unexplained gaps — they are R11 working as designed, and someone recorded the blocker at the moment
they hit it.

**And the 84 rows cannot characterise the phase.** `search_coverage` in the same archive holds
**4,960 rows, 634 of them `SEARCHED`** — so the majority of recorded coverage has no execution log at
all. The execution table covers a three-day window (2026-07-24 → 07-26) of a months-long effort.
**A conclusion about "the research phase" drawn from it is a conclusion about three days.**

**The finding that remains, stated at its true size:** in the only window with query-level logs, the
registered specialist databases went unused and the register could not have told anyone, because
`engine` is free text and the register is prose in a skill file. That is a real gap and it is what
§12.3 fixes. It is not the 58% claim, and it is not a verdict on the whole phase.

### 12.3 Indexes are not bodies — two tables, not one

An index and a publisher are different objects and must not share a table, or the frame commits the
umbrella error one more time:

- A **research body** (§11) *publishes* documents you may cite — DIN, Habinteg, Seoul.
- A **research index** *is infrastructure you search through* to find documents — PubMed, SciELO, CNKI.

A single search execution has both: *"searched J-STAGE (index) for MLIT guidance (body)."* They are
orthogonal, and the same body's output is reachable through several indexes.

```
research_indexes
  index_code        PK   -- pubmed, jstage, cnki, scielo, ajol, web, manual
  full_name              -- 科学技術情報発信・流通総合システム (J-STAGE)
  index_type             -- bibliographic | preprint | repository | citation_graph
                         -- | specialist | web | manual
  languages              -- indexing language coverage (NOT evidence weight -- §12.4)
  jurisdictions_served   -- nullable; SciELO/LILACS/AJOL/WPRIM are regional
  tool_reachable         -- 0/1: reachable by this session's tooling vs. manual/browser only
  access                 -- open | subscription | institutional
  run_priority           -- all_runs | language_conditional | jurisdiction_conditional
  notes

research_index_coverage  -- the denominator, mirroring search_coverage's shape
  slug, index_code, status IN ('SEARCHED','THIN','NO-DATA','NOT-RUN'), ...
  PRIMARY KEY (slug, index_code)
```

Then **`search_executions.engine` becomes a foreign key to `research_indexes.index_code`.** That one
change converts a free-text label into a measurable coverage dimension, and it is the smallest edit
that would have made the 58%-web finding visible while it was happening rather than in an archive
three months later.

**`tool_reachable` is worth carrying explicitly** because a session may have PubMed, Consensus,
bioRxiv and Scholar Gateway available as tools while J-STAGE, CNKI, RISS and SciELO are browser-only.
A register that does not distinguish them will silently over-weight the ones that are easy to reach.
**Amended per the Fable 5 pass, F11:** this encodes a property of *a session's tooling*, which is
volatile — MCP servers connect and disconnect between sessions. Pair the column with a
`tool_reachable_checked_at` date, or it will assert as durable fact something that was true once.

### 12.4 One doctrine line must be carried across, not left in the skill

Step 3's warning is load-bearing and belongs in the table's own documentation, because it is the exact
claim a coverage metric will invite someone to violate:

> **No database priority implies evidence priority.** The list reflects indexing *language coverage*,
> not evidence weight. A Tier 1 study in J-STAGE governs over a Tier 3 study in PubMed.

This is R5 in the research contract (*non-English peer-reviewed work is ACADEMIC, not grey;
non-indexation in PubMed/Scopus is an INDEXING fact, not an evidence-quality fact*). Once
`research_index_coverage` exists, PubMed will be the easiest index to fill and the most tempting to
treat as sufficient. **`run_priority` and the doctrine note are the guard against that**, and neither
works unless it sits with the data.

### 12.5 What this adds to the sequence

| Step | Where it goes |
|---|---|
| Build `research_indexes`; seed from the skill's 21-database register | §8 step 3, same migration |
| Build `research_index_coverage`; make `search_executions.engine` an FK | §8 step 3, same migration |
| Retire the prose register to a generated view of the table | after the table is populated — redirect-stub, do not delete (guardrail 2) |

**Net schema delta across §10–§12:** four new tables (`jurisdictions`, `research_bodies`,
`research_indexes`, `research_index_coverage`), one FK added to an existing column, one nullable
`bucket` column. No table is dropped that was not already being dropped, and the staging itself
(§10.5) still needs no schema at all.

---

## 13. Fable 5 adversarial pass — 2026-08-18

**Authority:** owner ruling, *"Fable 5 available; return suspended work for its use."* Discharges the
§4b/§4c debt in `workplan/2026-08-18-model-substitution-log.md`. Read-only; findings only.

**Why it was owed.** This document was authored by Opus 5 and every subsequent owner ruling was
executed by Opus. Fable was assigned for **model-family independence**. The pass was interrupted
twice by transient API server errors and resumed from its own transcript; it marks each finding
VERIFIED (re-derived this session) or ASSERTED (reasoned). **I independently re-ran F1 and F3 against
the live and archived databases before accepting them**, because both overturn claims I had written.

### 13.1 Findings

| # | Severity | Finding | Site |
|---|---|---|---|
| **F1** | **HIGH** | The 58% statistic is wrong. All 19 `manual` rows are **deferrals, not searches**, each carrying an explicit `deferred_reason`. Executed searches = 65; web = 30 = **46%**. The claim "nothing could compare the two" is contradicted by the corpus's own deferral reasons. And 84 rows cannot characterise a months-long phase — `search_coverage` holds 4,960 rows, 634 `SEARCHED`, with no execution log. | §12.2 |
| **F2** | **HIGH** | The parameterised PROVISIONAL wording **over-releases beyond the ruling**. The owner released buckets 4–5; "the buckets it declares in scope" also releases bucket 3, silently, under the appearance of parameterising. The disclosure clause itself is sound and properly flagged as proposed. | §10.1.2 |
| **F3** | MEDIUM | *"Canada is not currently in that map with both en and fr"* is **false** — both PRIMARY rows exist since 2026-07-24. §10.3's bucket-1 count depends on the FR row it declared missing. | §3 |
| **F4** | MEDIUM | The skill enumerates 47 codes and declares a **"46 jurisdictions"** scope with numeric gates against it — **a fourth jurisdiction count** the "12/27/48" landscape missed. Omits AT and CY, both bucket members. Seeding will under-seed. | §11.1 |
| **F5** | LOW | §8 step 5 seeds from Steps 2a/2b, which contains the Seoul municipality row §11.4 defers. Contradiction. | §11.4, §8 |
| **F6** | — | **§7.1 settled: e-codes stay off the lens.** There are **ten**, not the three I listed; as lens members they duplicate lens 3. | §7.1 |
| **F7** | — | **§7.2 settled: 46 is wrong.** `access_need_icf` names five `b`/`d` codes outside the union — **the whole d5 self-care chapter is missing**. Interim floor 51. | §7.2 |
| **F8** | — | **§10.6 answered: readiness, not importance.** Importance is circular pre-search; R1 already fixes lens order, so the problem reduces to a slug queue. | §10.6 |
| **F9** | LOW | The `MERGED` / `merged_into` machinery has **three rows ever**. "Built for it" overstated. | §6 |
| **F10** | — | §9.5's threshold is measurable, but unenforced root registration means a typo silently under-counts. DoD must assert root-registration validity. | §9.5 |
| **F11** | — | `tool_reachable` encodes a volatile property of a session's tooling; pair it with a checked-date. | §12.3 |

**All eleven are corrected in place above**, each at its own site, with the superseded text struck
rather than deleted.

### 13.2 Two conclusions upheld but re-based

Fable upheld §11.2 (splitting `jurisdictions` from `research_bodies`) and §12.3 (separating indexes
from bodies) — **but rejected the argument I gave for them.** I argued both from "conflating them
would be the umbrella error." Fable's verdict: that is a repo shibboleth applied where it does not
fit, and the real justifications are ordinary ones —

- **§11.2** rests on **functional dependency**: `languages` and `bucket` depend on the jurisdiction
  alone, so they belong in a table keyed by it. That is third normal form, not doctrine.
- **§12.3** rests on **disjoint columns and different FK shape** — `jurisdictions_served` on an index
  versus a single `jurisdiction` FK on a body.

**Recorded because the distinction matters for the DR.** A structural decision justified by doctrine
invites a doctrinal challenge; the same decision justified by normalisation does not. Reaching for the
umbrella argument where a plain one would do is a habit worth naming, and this document did it twice.

### 13.3 What the pass examined that I did not

The **content** of the 84 execution rows — `query_text` and `deferred_reason`, which is what overturned
F1; the register's git provenance against the execution timestamps; the skill's own declared
jurisdiction scope; the `lang_jur_map` rows for Canada; and the ruled-versus-proposed boundary of the
§10.1.2 replacement wording.

**The common shape of F1, F3 and F9: I read counts and did not read rows.** Every one of the three is
a number that was correct as arithmetic and wrong as a claim, because I never opened what it counted.
That is the failure mode CLAUDE.md §10 names — *a gate reporting zero may have examined zero* — and it
recurred here three times in one document.
