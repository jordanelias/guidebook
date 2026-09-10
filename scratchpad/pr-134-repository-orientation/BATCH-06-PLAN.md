# Batch 06 — frame and query plan, `accessible-circulation-geometry`

**Written 2026-09-10, BEFORE any search is executed.** R8 requires the prior expectation to exist
before the query runs — *"a prior recorded after seeing results is a rationalisation, not a prior"*
(DR-2026-05-09). This file is that record. Every `--prior-expectation` string below goes into
`search_executions` verbatim.

- Session id (stem, for the DB and every `--session` flag):
  `session_2026-09-10-research-batch-06-circulation-geometry`
- Same id **+ `.md`** for `emit_data_migration --session`, `citation_mining_completeness --session`,
  `sessions/LATEST`, `sessions/LATEST-RESEARCH`.
- Scratch: `<scratchpad>/batch06/walk.db`; canonical sha256 recorded in `PRE.sha256` and must not
  move until step 6c.
- Pre-state probe run: empty session trips exactly **R1, R9a, R9b** — the runbook's stated
  expectation, so the id is uncontaminated.

---

## 1. The frame, pulled ICF-first (runbook step 2)

Pulled from the live vocabulary, not from `items` — §1.4 rule 1 of the operative instrument, and the
step this runbook's predecessor got backwards on 2026-09-01.

| Lens | Column on `specifications` | Vocabulary | Rows |
|---|---|---|---|
| identity | `identity_code` | `populations` | 23 |
| ICF | `icf_code` → **`axes`** | `axes` (each carrying `icf_b_anchors` / `icf_d_anchors`) | 17 |
| access-need | `needs_code` | `access_needs` | 17 |
| medical | `medical_code` | `base_taxonomy_medical` | **0** |

**The medical lens has no vocabulary.** `base_taxonomy_medical` is an empty table with a live
CHECK'd DDL. R4 says cross *every* lens; one of the four cannot be crossed by anyone today. D-0182
relaxed the row CHECK to `COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL`,
so a cell is still writable on the other three. **Recorded as a gap, not filled** — populating a
medical taxonomy is content, and content is owner-gated (`CLAUDE.md` §8).

**Note the ICF lens is the axis vocabulary, not raw ICF codes.** `specifications.icf_code` FKs to
`axes.axis_code`. Raw ICF codes reach the frame indirectly, through `access_need_icf` (43 rows, 15
distinct codes) and through each axis's own anchors. Do not write a `b`/`d`/`e` code into
`icf_code`; the FK will refuse it.

### What batch 05 actually crossed

All 9 admitted sources grade on **MOB**; SCI ×2, PAIN ×1, ALL ×1. Five of the nine are **PROXY** on
MOB. Axis territory was `AX-WHM` / `AX-REA`. Access-need territory was `A-REACH` / `A-SIZE`.

So the slug is, today, a **manual-wheelchair-and-scooter corpus wearing a circulation-geometry
name**. That is the coverage fact batch 06 exists to correct, and it is also why the batch is a
lens-crossing batch rather than a deeper mobility dig.

### Uncrossed, and reachable

- **identity** — BLIND, DEAFBLIND (cane sweep, guide-dog space, tactile wayfinding); LPA, TALL, BAR
  (`A-SIZE`: circulation sized for the range of bodies present, not the 95th-percentile male);
  DEM (`AX-COG-O` orientation demand at decision points); VES (corridor length, visual flow);
  MOVE, MS, COM, PAIN (`A-EFFORT`: rest points along a route).
- **access-need** — `A-EFFORT`, `A-TACTILE`, `A-NOSIGHT`, `A-LOWLOAD`, `A-CALM`.
- **axis** — `AX-AMB` (ambulant movement: d450/d455/d460), `AX-STA` (sustained exertion: b455),
  `AX-BAL` (b235/b240), `AX-COG-O` (b114/b144, d460/d175), `AX-VIS-N` / `AX-VIS-L` (b210, d460).

---

## 2. The parameter — minted from the harvest, not from a placeholder

**`observed_terms` holds 33 rows and `term_adjudications` holds 0.** Batch 05 harvested at evidence
(D-0173's first half) and the judgment half was never run. That backlog is where the parameter comes
from, and working it discharges real debt rather than adding apparatus.

**Chosen: observation 6, `"turning diameter"`, REF-00971, @abstract METHOD.**

Why this one:

- It is a phrase a source **used**, so `add-term --from-observation` is the sanctioned route and the
  parameter's provenance is a real document rather than a guess.
- **It states no answer.** `add-term` refuses a canonical name bearing a digit, a comparator or a
  min/max word — the item-layer defect in miniature. Compare observation 7, `"turning 180° in a
  corridor"`, which that guard would and should refuse.
- **A second source states the same concept in different words**: observation 9, `"turning circle"`
  (REF-00972). That is the NAMES-EXISTING adjudication runbook step 4 exists for.

  > **CORRECTED 2026-09-10 — the rest of this bullet was a fabricated rationale and is struck.**
  > It read: *"and it is the in-data repair for `v_value_independence` fragmenting by verbatim
  > label (audit task 8.7) — two phrasings of one parameter otherwise read as two parameters."*
  > The live view groups by `sve.parameter_id, t.canonical_en`, where `canonical_en` is reached by
  > joining `base_parameters` → `terms` on `parameter_id`. The label is therefore functionally
  > determined by the group key and **cannot fragment anything**. There was no defect to repair,
  > and the audit register's own task-8.7 description no longer matches the view either — it
  > described 071's version, and 072/073 moved it. A justification invented to make a choice look
  > better is the same failure class as a count carried forward from prose.

**Deliberately NOT `"corridor clear width"`**, the runbook's worked example. It is admissible, but it
is also the exact name the deleted `E-08 Corridor Clear Width (≥1200 mm Minimum on All Primary
Routes)` announced its answer under, and batch 06 has a cleaner option sitting in its own harvest.
Where two routes are equally sanctioned, take the one that never touches the quarantined surface.

**Adjudication backlog to work while there (step 4):** obs 9 `turning circle` → NAMES-EXISTING;
obs 10 `three-point turn`, obs 11 `aspect ratios`, obs 5/1 `manoeuvrability`/`Maneuverability`
(spelling variants — note `insert_term`'s clash check is `lower()` with no whitespace normalisation,
audit task 8.1, so do not rely on it to catch a near-duplicate).

---

## 3. The query plan — tier-ordered per R1 (Co-1 → Co-2 → T2 → T1 → T4–T6)

Languages already fired on this slug: **EN ×13, DE ×1, JA ×1**. `lang_jur_map` marks 19 PRIMARY
languages. Batch 05's JA leg found 49 papers and admitted 0 — recorded as the R5 finding of that
batch. Repeating it identically would learn nothing; §3 below re-enters it with a different query
shape.

Every row is logged with `results_screened`/`results_admitted` at 0 until step 7. **Empties are
kept** — a zero-yield search is a completed unit of work (R8) — and each carries an R14 diagnosis
saying *query-shape failure* vs *wrong index* vs *genuine absence*.

### Co-1 first (R1), the tier this project is least able to fake

| # | Lens crossed | Language | Engine | Prior expectation, written now |
|---|---|---|---|---|
| 1 | BLIND / `A-NOSIGHT` / `AX-VIS-N` | EN | web | Expect DPO and guide-dog-organisation output on cane sweep width and corridor obstruction to exist as practice guidance, and expect it NOT to carry measured geometry. If it does carry a dimension, expect it cited from a code rather than measured. |
| 2 | LPA / BAR / TALL — `A-SIZE` | EN | web | Expect little-people and fat-liberation organisations to describe circulation barriers qualitatively and expect near-zero measured anthropometry from them. A genuine absence here is a finding about who gets measured, not about the topic. |
| 3 | DEM — `AX-COG-O` | EN | scholar | Expect co-produced dementia-and-environment work to exist (this is one of the better-developed participatory literatures) and to speak to decision points and legibility rather than to width. |

### Co-2 (OT professional-body CPGs)

| # | Lens | Language | Engine | Prior expectation |
|---|---|---|---|---|
| 4 | `A-EFFORT` / `AX-STA` — rest points on a route | EN | web | Expect OT professional-body guidance on energy conservation and home/route assessment to exist. Batch 05 found RCOT guidelines sit outside PubMed (its exec 35/36 R14 diagnosis); expect the same, so search the body's own site, not an index. |

### T2 synthesis

| # | Lens | Language | Engine | Prior expectation |
|---|---|---|---|---|
| 5 | BLIND/DEAFBLIND — tactile wayfinding | EN | pubmed | Expect a thin systematic-review literature and a real risk of an AND-chain collapse; if 0, split the chain before calling it absence (R14). |
| 6 | VES / MOVE / `AX-BAL` — gait and corridor geometry | EN | consensus | Expect balance and fall literature to be rich but framed on *the person*, not on the corridor. Expect to have to record that mismatch as a finding rather than an admission. |

### T1 primary

| # | Lens | Language | Engine | Prior expectation |
|---|---|---|---|---|
| 7 | BLIND — cane/guide-dog space envelope | EN | pubmed | Expect a small, old anthropometric literature — the long-cane sweep envelope is the kind of figure measured once and cited forever. Expect to find the citing layer before the measurement. |
| 8 | `A-SIZE` — body-size range in circulation | EN | pubmed | Expect anthropometric work keyed to equipment, not to bodies, and expect fat people to be absent from it as subjects. R7: absence of a population from the measurement base is a first-class finding. |
| 9 | AMB / walking aids — `AX-AMB` | EN | consensus | Expect walker and crutch users to be studied for gait, rarely for the space they need. |
| 10 | DEM — orientation at decision points | EN | pubmed | Expect environmental-design-for-dementia work to be real and to be largely non-dimensional. |

### Non-English (R5 — academic, not grey)

| # | Lens | Language | Engine | Prior expectation |
|---|---|---|---|---|
| 11 | `A-SIZE` / `AX-AMB` | DE | consensus | DE was batch 05's highest-yield leg. Expect the German barrier-free literature to keep dimensions in normative documents (DIN 18041 / DIN 18040 family) rather than in journals, so expect leads more than admissions. |
| 12 | wayfinding / tactile | JA | registry (J-STAGE) | Batch 05's JA leg returned 49 and admitted 0. Expect the same volume; the prior is that the **screening**, not the retrieval, was the bottleneck, so this leg is scoped narrower and screens fewer, deeper. |
| 13 | circulation geometry | ES **or** NL | consensus | New language for this slug. Expect low yield and expect that to be an indexing fact rather than an evidence-quality one (R5). |

### T4–T6 regulatory stratum — **leads only**

| # | Lens | Prior expectation |
|---|---|---|
| 14 | tactile/visual circulation provisions across jurisdictions | Expect to find clause-level provisions readily. **They are staged as `research_code_leads` / `search_candidates`, never written into `jurisdictional_values`** — the 2026-08-12 REFERENCE-ONLY ruling stands and the runbook's step 10 clause is struck. A value written here is the 2026-08-21 defect repeated. |

### Deliberate non-search (R6)

| # | Subject | `--deferred-reason` |
|---|---|---|
| 15 | Vertical circulation (lifts, platform lifts, stairs) | Deferred, as batch 05 deferred it at exec 42. It is a distinct sub-construct with its own geometry and its own harm literature, and folding it in here would make the slug unbounded. `deferred_reason` means DELIBERATELY NOT SEARCHED, never a findings channel. |

---

## 4. Floors this batch must clear, and the ones it must not fake

- **R7** — ≥1 candidate per 25 screened, and failure/harm/inadequacy captured as first-class
  evidence. Legs 2, 8 and 12 are where a harm or absence finding is most likely; do not let one
  become a by-product note.
- **R2** — mining floor `admissions // 4`, minimum 1. A deferred mining pass with a reason counts.
- **R13** — one `evidence_population_match` per tier-1..3 admission. Given batch 05 graded 5 of 9
  PROXY on MOB, expect PROXY to be the honest grade often here too. **Children, general-population
  and no-participants are PROXY at best**, with the mismatch note written.
- **R11** — `observe-term` on every admitted source, verbatim and unjudged. `R11-harvest` fails any
  admitted source with zero `observed_terms` rows.
- **R9a/R9b** — DOI pre-check against `evidence_sources` **and** `source_locators` (881 rows). An
  `evidence_sources` hit means cross-file; a lead hit means admit reusing the stash ref_id.
- **R10 / R10b** — every locator re-retrieved through `retrieval_log.fetch()`, payload persisted
  first; `--verification-status` always passed explicitly. A URL-bearing admission left NULL is what
  wakes the scheduled verify-urls cron and pushes a DB blob to `main`.

**And the one that is not a floor:** a `COMPLIANT` gate is not a sound determination. It proves 19
mechanical rules. Whether the cell is believable is a separate question, answered by whether the
governing set holds sources that actually extract *this* parameter — which, after migration 073, is
enforced rather than trusted: `gather_sources(conn, parameter_id)` returns only sources carrying an
extraction for it, so a `stated` cell resting on the slug's other sources is now unconstructible.

---

## 5. Order of execution

1. Step 1 — `observe-term` is already done (obs 6 exists); `add-term --from-observation 6`, then
   `add-parameter`. **This is the write that makes `specifications` and `source_value_extractions`
   writable at all** — both are NOT NULL FKs into `base_parameters`, which holds 0 rows.
2. Steps 2–3 — the 15 legs above, logged before screening; admit; harvest terms per admission.
3. Step 4 — adjudicate the harvest, including batch 05's 33-row backlog as far as it goes.
4. `add-extraction` per source that actually states a value for the parameter. **Without this the
   determination has no governing set.**
5. Step 5 — the engine, on `parameter × lens`. One cell. There is no re-determination path
   (`idx_spec_row_identity`), so choosing the lens is a one-shot decision.
6. Step 6 — `emit_batch_sql` → `emit_data_migration` → `migrate_db` → `regenerate_derived.sh`.
   Discard the engine's own `--emit-sql` file; replaying both collides.
7. Step 7 — gate. Step 8 — record, pointers, attestation.

---

## 6. Step 1 proved on the scratch, 2026-09-10 (dry run, nothing written)

The refusal, fired against observation 7's own phrase:

    REFUSING: --canonical-en 'turning 180° in a corridor' REFUSED: it carries a number,
    a comparator or a min/max word, so it states a determination in its own name.

The chosen parameter, accepted:

    {"term_id": "TERM-089", "canonical_en": "turning diameter", "adjudication_id": 1,
     "from_surface_form": "turning diameter", "from_ref_id": "REF-00971", "dry_run": true}

`add-term` mints the term and writes its NAMES-NEW adjudication in one act, so a second
`adjudicate-term` call for observation 6 will be refused as already adjudicated.

**One limit of that guard, worth knowing before relying on it:** `_VALUE_BEARING`
(`db.py:3061`) is ASCII-only — `١٢٠٠`, `１２００`, "at least twelve hundred millimetres" and
"minimal corridor width" all pass it (audit task 8.2, unfixed). It caught the case above; it is
not a general defence against a name that states its answer. The operator is still the gate.

Canonical `data/guidebook.db` sha256 verified unchanged across the whole frame pull and both dry
runs — every call above ran against `walk.db` with `GUIDEBOOK_DB_PATH` set inline.

---

## 7. THE DEPENDENCY THIS PLAN MISSED, derived 2026-09-10 after the plan was written

Sections 1–6 above treated B5a (the tier gate) and B5b (the four escalated `scope` rows) as two
separately-tracked items, one closed and one pending. **They compose, and the composition decides
whether this batch can produce a believable cell at all.**

### The measurement

`schemas/tier_derivation.check_tier_consistency(evidence_type, scope, stored_tier)` applied to all
nine admitted sources — B5a routes a `False` here through `anchoring()` to `NON-ANCHORING`:

| ref_id | stored | type | scope | derived | |
|---|---|---|---|---|---|
| REF-00784 | T1 | clinical | **NULL** | UNDERIVABLE | **NON-ANCHORING** |
| REF-00971 | T3 | clinical | **NULL** | UNDERIVABLE | **NON-ANCHORING** |
| REF-00972 | T3 | clinical | **NULL** | UNDERIVABLE | **NON-ANCHORING** |
| REF-00973 | T1 | clinical | high_control | 1 | ANCHORABLE |
| REF-00974 | T1 | clinical | high_control | 1 | ANCHORABLE |
| REF-00975 | T3 | clinical | lower_control | 3 | ANCHORABLE |
| REF-00976 | T3 | clinical | **NULL** | UNDERIVABLE | **NON-ANCHORING** |
| REF-00977 | T2 | sr_meta | intrinsic | 2 | ANCHORABLE |
| REF-00978 | T1 | co1 | intrinsic | 1 | ANCHORABLE |

**5 of 9 can anchor.** The four that cannot are exactly the four rows B5b left NULL and escalated to
the owner — the sets are identical, not merely overlapping, because a NULL `scope` makes
`(evidence_type, scope)` underivable and B5a excludes precisely that.

### Why this lands on the parameter chosen above

`"turning diameter"` is observation 6 on **REF-00971**. `"turning circle"` is observation 9 on
**REF-00972**. **Both are non-anchoring.** They are also the only two sources in the corpus whose
abstracts state turning geometry at all — they are the Toronto mobility-scooter pair, and turning
diameter is their measured outcome.

After B4, `gather_sources(conn, parameter_id)` returns only sources holding an extraction **for that
parameter**. So the governing set for `turning diameter` would be drawn from REF-00971/972, and both
would arrive `NON-ANCHORING`. The engine's own `sha()` docstring names this exact case as the one it
added `n_extractions` to the hash payload to distinguish:

> *(b) a parameter READ AND REJECTED — 2 sources, 2 extractions, both non-anchoring on tier (B5a)*

**So the cell is constructible and would come out `pending`, not `stated`** — correctly, and for a
reason that is not about circulation geometry. That is the engine working. But this plan presented
the parameter choice as well-founded without checking it, and "we chose the phrase two independent
sources use" is a weaker recommendation once both of those sources are excluded from anchoring.

### What follows, stated as options rather than a decision

1. **Run it and accept `pending`.** Honest, and it exercises the whole walk end to end. But
   `idx_spec_row_identity` gives no re-determination path, so a `pending` cell on
   `turning diameter × <lens>` **permanently occupies** that cell until a supersede design exists.
   That is a real cost, not a rehearsal.
2. **Choose a parameter whose extractions can come from the five anchorable sources.** Their subject
   matter is shoulder load and propulsion kinetics (REF-00973/974), lived-experience home access
   (REF-00975), a synthesis on inaccessible public space (REF-00977), and a Co-1 access survey
   (REF-00978). A parameter drawn from that set is likelier to be about gradient, effort or route
   length than about turning geometry — which would also serve the lens-crossing purpose in §1
   better than turning diameter does.
3. **Get B5b ratified first.** Four `scope` values land, the four sources become anchorable, and
   `turning diameter` becomes a candidate for `stated`. **Owner-gated** — evidence-tier definitions
   are owner-only (`CLAUDE.md` §8), and `workplan/2026-09-10-b5b-scope-owner-escalation.md` §6 is
   where that ask already sits.

**Option 3 is the only one that makes the chosen parameter reach `stated`, and it is not a session's
to take.** Recorded here rather than resolved.

### One more edge, unevaluated until now

`regulatory_richness()` (`assess_cell.py:409`) builds `jur45 = {r.get("jurisdiction") for r in t45}`
with **no strip, no casefold and no None-dropping** — audit task 4 is **NOT fixed**, verified in the
code rather than inferred from its docstring. Every source in the live corpus has
`jurisdiction` NULL except REF-00978 (`GB`). So a T4–T6 governing set assembled from this corpus
would count `None` as a distinct jurisdiction and could clear a §2.3 richness test it should fail.
This plan's leg 14 targets the regulatory stratum. **Leads only there, per the REFERENCE-ONLY
ruling, so nothing this batch files reaches that code path** — but the interaction is live the moment
a regulatory value is ever adjudicated, and it should be fixed before then.
