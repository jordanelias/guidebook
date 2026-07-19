# Content-Model Audit — Categories · Specifications · Rooms · Typologies (Comprehensive)

**Date:** 2026-07-19 · **Status:** definitive rewrite. Supersedes this file's first-pass version and consolidates the six-direction working papers in `category-spec-room-typology-audit-INTENSIFICATION-2026-07-19.md` (retained for per-claim file:line grounding). This is the single record.

**What it is.** An audit of the four content-model axes the website navigates — the A–K **category** taxonomy (Part 4, 93 items), the **specification** layer, the **room** taxonomy (Part 6 + `site/rooms/`), and the non-residential **building-typology** taxonomy (Part 7) — answering, for each: *what is missing that our research supports*, and *what should be consolidated that our syntheses justify*. Then interrogated from six cross-cutting directions (population, jurisdiction, evidence, lifecycle, network, functional-deficit) and adversarially reconciled.

**Companion to, not overlapping with:** `audits/consolidation-sweep-2026-07-12.md` (repo/process fragmentation) and `audits/project-shape-audit-2026-06-22.md` (pipeline shape). Those two already establish that the *judgment/weighting/render* layer is largely unbuilt; this audit does not re-litigate that — it specifies **which content-model structures and axes** that unbuilt layer needs.

**Method.** A structural four-axis pass (five parallel grounded agents) → a six-direction interrogation (six parallel agents, each tasked to *refute* the structural pass) → **two adversarial self-reviews** → **~25 highest-stakes claims re-verified directly against the live DB/files this session; every checked claim held.** Findings are **[C]** confirmed against source this session or **[H]** reasoned (owner judgment). Nothing here modifies the taxonomy, data, or any item — every action is a candidate for owner ruling / a scoped Change Order, and every new value remains behind the project's PROVISIONAL banner.

**Lens.** The deliverable is a website (`architecture/navigation-modes.md`: four-door IA — `/specs` category filter, `/populations`, `/rooms`, `/economics`). Three of the four axes cannot currently render a clean surface; one (`/rooms`) is a *named blocking gap* for v0. Findings are framed against that build.

---

## 1 · Executive verdict

The evidence **library** is mature; the **content model that renders it is not reconciled, is under-dimensioned, and sits on a deliberately-retracted evidentiary substrate.** No single fact is fatal; the *pattern* is the finding. Seven throughlines (§2) recur across every axis and direction. The practical consequence: **item-gap-filling and duplicate-merging — the two things this audit was asked to find — are real but downstream of restoring the evidence and adding the axes the model needs to express its own doctrine.**

| Axis | Sharpest MISSING | Sharpest CONSOLIDATE | Website-blocking? |
|---|---|---|---|
| **Categories A–K** | Thermal is **fragmented**, not missing — Appendix C (decided home) + Category-F items + misfiled K-05 **[C]** | Two conflicting name schemes; **three dead consolidations** (88→65, CO-0003/D2, population hierarchy) never executed **[C]** | Yes — `/specs` filter needs one canonical name per letter |
| **Specifications** | **69/93 items** have no structured value; the evidentiary substrate is **retracted corpus-wide (68/82 BPCs)** **[C]** | Retire `specification-database.json` (item_codes point at wrong items) — but fix the broken authority pointer first **[C]** | Yes — Template 1 queries a `specification` table that doesn't exist |
| **Rooms** | The **sensory/quiet room** (A-16) is absent from all 17 site rooms **[C]** | R-HAL/R-COR & R-BA/R-WC are res↔non-res duplicates of one *space* **[C]** | **Yes — named v0 gap**: no room table; seed matrices are *wrong* and write to a phantom path |
| **Typologies (7 NR)** | **NR-CARE** (dementia-village/residential care) — deepest (Global-North) evidence, no Part-7 home **[C]** | Split the incoherent **NR-HOS**; NR-RET/CUL/HOS/TRP have no dedicated case studies **[C]** | Indirect — `/rooms/non-residential/` needs a resolved model |
| **Cross-cutting** | The model lacks **activity (ICF), lifecycle/DAR, conflict/population-pair, and building-type×space** axes **[C]** | The same "N stores silently disagree" recurs on **every** axis **[C]** | Yes — determines the whole schema |

---

## 2 · Throughlines (the recurring patterns — the intellectual spine)

Seven patterns cut across every axis and direction. Every specific finding in §§4–5 is an instance of one or more of these. They are the takeaway-level structure.

**T-1 · Multi-store drift is the model's default state — not a spec-layer bug.** The same structure is described by several stores that silently disagree, on *every* axis: **specs** (Part-4 prose · `jurisdictional_values` · `spec_value_probes` · `source_value_extractions` · dead JSON) · **populations** (bare code · `subtype` · enum sub-code · evidence-match string — four encodings) **[C]** · **jurisdictions** (enum 24 · values 12 · search 47 · CRPD 46, + a UK/GB code seam) **[C]** · **versions** (TOC v8.9.3 · parts v9-0 · versions/8.10 · v10-predraft · site v10.5 — 5 vintages + 3 orthogonal schemes) **[C]** · **item-numbering** (DB · `part04-item-index` · a *second* stale surface in Part-4 stage tables & Part-8 O&M) **[C]** · **conflicts** (empty DB table · 12 markdown matrices · 0 population codes in the graph) **[C]**. **And the authority pointer that should resolve this is itself broken:** `versions/current/DEPRECATED.md` designates as canonical a DB path that does not exist (`data/db/guidebook.db`, "141 specs"; the live DB is `data/guidebook.db`, 93 items) plus the very JSON slated for retirement **[C]**. *Reconciliation cannot begin until "which store is canonical" is fixed.*

**T-2 · The evidentiary substrate is in a deliberate pre-rehabilitation hold.** `bpc_metadata`: **68/82 slices = `RETRACTED-PRE-REHAB`, 13 NULL, `co1_pass_count = 0` and `pico_complete = 0` for all 82** **[C]**. This is not newly-discovered decay — it is the state the project deliberately put the corpus in, consistent with the PROVISIONAL banner and the "hold, don't publish as authority" posture of `workplan/next-steps-synthesis-2026-07-14.md`. The audit's contribution is to **quantify** it and draw the consequence: every A–K value is provisional, so consolidation and gap-filling operate on values not yet re-derived. *The banner is correct; the work below is what happens behind it.*

**T-3 · The model is under-dimensioned for its own doctrine.** It expresses **category (component) + population**. It has **no queryable axis** for the four things its doctrine and website need: **ICF activity** (one incidental `d440` in the whole DB, though §1.3 says "design addresses functional *deficits*") **[C]**, **design-stage / DAR / lifecycle** (schema-only fields on a non-existent table; zero stored rows) **[C]**, **conflict / population-pair** (empty table; 0 population codes in the connection graph) **[C]**, and **building-type × space** (armature_v4's own already-designed spatial axis, deferred to v2) **[C]**. *The project knows the judgment/render layer is unbuilt; this names the specific axes it must add.*

**T-4 · Coverage is inverted — richest evidence ≠ richest structure.** The deepest research supports structures that don't exist, while thin structures carry confident headings: NR-CARE (5 care-village case studies) has **no typology**, while NR-RET/CUL/HOS/TRP (0 dedicated case studies) are headings **[C]**; at the item layer DEM(55)+VIS(43)+OFS(31)+SCI(26) span all 10 categories while **DEAF has 0 circulation items, 0 in C/F/I** (GAP-268 quantified), UPL touches 3 categories, and single-item tails render as broken stubs **[C]**.

**T-5 · Designed-but-never-executed is a chronic mode.** Structure gets planned and stops before landing: **three dead consolidations** — the 88→65 manifest and the CO-0003/D2 merges (DB still holds every struck item; index carries false "MERGED" labels) and the **population hierarchy** (enum specifies rollup; DB half-parents and never reads `parent_code`) **[C]**; armature_v4's two-axis spatial model deferred; the spec-migration target table never built; `seed_room_items.py` writes to a **phantom `data/db/` path** **[C]**. *Do not resurrect the dead plans; re-derive (T-7 test).*

**T-6 · The taxonomy is Western-anchored.** `jurisdictional_values` is **72% four-Western-jurisdictions** (DE/GB/US/AU; only SG=1, JP=1 from the Global South); **Swahili/Hindi/Bengali/Arabic/Indonesian are 0-searched**; the four `*-global-south` BPCs are complete research but **orphaned** (no item links, gaps not in the DB, banner-retracted) **[C]**. The most-covered typology (NR-CARE evidence) is also the most geographically parochial.

**T-7 · Phantom and orphan hazards are pervasive — and gate consolidation.** Phantom **tables** (`room`, `specification` queried by generators, absent from the DB); phantom **items** (E-14 with inbound P1 references; I-05/I-06 cited in Part-8; E-12 double-booked as "Refuge enclosure") **[C]**; **32 graph orphans** (up from 28 — new items created un-wired) **[C]**; the keystone node **A-16 carries 23 edges** (splitting it is high-blast-radius) **[C]**. *This yields the merge discipline below.*

**The reconciled merge test (resolves the session's internal contradiction).** My first pass said "execute or retire the 88→65 manifest"; the evidence direction said "merge by evidence cleavage"; the network direction said "don't merge I-03/G-03 (Jaccard 0.09)"; the functional-deficit direction said "merging seating erases ICF coverage." These are reconciled into a **three-gate test — merge two items only if all three hold:** (a) **evidence cleavage** — they share one BPC the evidence cannot separate; (b) **network role** — their connection neighborhoods overlap (not disjoint); (c) **activity coverage** — no distinct ICF activity loses its only (proxy) provision. The dead manifests are inputs to retire, not plans to execute.

---

## 3 · The adversarial-reconciliation log (what my own session work got wrong)

Baked in, per this project's on-record-correction discipline. Two self-reviews ran; the material corrections:

| Claim (first draft) | Resolution | Dir |
|---|---|---|
| "Thermal is a **missing category** [C, HIGH]" | **Downgraded** — `decision_register.yaml:292` places Thermal Comfort (TC-01–05) in **Appendix C** by standing decision; the real finding is *fragmentation* (Appendix C + Category-F items + misfiled K-05), remedy [H]. | self-review 1 |
| "Adopt a **new** two-axis model" | **Reattributed** — building-type × space is **armature_v4's own** spatial axis (`armature_v4.md:111`; `page-templates.md:209`), deferred to v2. The site flattening *contradicts an existing design*. | self-review 1 |
| "Retire the JSON" (clean) | **Caveat** — four live migration/convert scripts consume it; and `DEPRECATED.md` names it authoritative, so **fix the authority pointer first**. | self-review 1 / lifecycle |
| §5: "100% of items have ≥1 BPC mapping — no item is evidence-free" | **REFUTED [C]** — 5 items (A-13, A-15, B-08, G-02, G-07) have no slug and no `item_bpc_links` (verified; `item_bpc_links` covers only A-18/F-07). | evidence dir |
| §2.5: "13 conflict matrices" | **12 domains** + 1 synthesis roll-up; 2 reclassified as non-conflicts. | network dir |
| CR-5: I-03 ↔ G-03 "**duplication**" | **Downgraded to "naming/scope overlap"** — Jaccard 0.09, disjoint neighborhoods; fails the merge test's network gate. | network dir |
| "over-fit to **dementia**" | **Reattributed** to a DEM+VIS+OFS+SCI four-way; VIS is co-dominant. | population dir |
| NR-CARE "deepest evidence base" | **Global-North caveat** added. | jurisdiction dir |
| "zero case studies" (NR-RET) | **"no *dedicated*"** — one mixed-use study touches retail. | jurisdiction/typology |
| Premise: SCI/EPI/POTS are "rogue DB codes" | **Corrected** — the DB FK is clean; the drift is DB↔enum (SCI/EPI/MS are *enum*-homeless). | population dir |

No correction overturned a spine finding; the §5 missing-item list survived every direction unrefuted and was *strengthened* on #1/#2/#3. Anti-fabrication held on both self-reviews and all ~25 verifications.

---

## 4 · The four structural axes (reconciled)

### 4.1 Categories A–K
- **Canonical names live nowhere queryable** (DB has the letter, not the name; `schemas/item.py:33` declares a `category_name` field that isn't in the table) — which is *how* two schemes drifted. **[C]**
- **Two conflicting name schemes; `part04-item-index.md` is wrong for G/H/I/K** (it labels G "Bathroom", I "Seating" — the part files + TOC say G "Furniture, Fixtures…", I "Upper Limb…", verified against `part05-*` headings, which match item contents). **Adopt the part-file/TOC scheme; correct the index; add K to the TOC.** **[C]**
- **The no-J sequence is deliberate** — bariatric J struck by CO-0001 (`project-standards.md:29` "delete on sight"), deafblind briefly J then renumbered to **K = "Deafblind Environment Provisions"** (both `part05-j` and `part05-k` carry that heading; the stale `part05-j` duplicate should be deleted). **[C]**
- **K is a real, well-evidenced category** (K-01…K-04 are the **best-anchored items in the model** — 68% research anchor, 3 Co-1; evidence direction refuted the assumption K is "thin"). **Only K-05 is misfiled** — it is a thermal item (Thermal Comfort Assessment) sitting under Deafblind; it belongs with the thermal group (its SCI linkage is *correct*, since thermoregulation is an SCI need). **[C]**
- **Thermal is fragmented, not missing** (T-3 instance): Appendix C (TC-01–05, decided home) + F-04/F-07/F-08 (in Category F "Sensory Zoning") + misfiled K-05. Reconcile into one home. **[C]**
- **[H] narrow category-restructure candidate:** the connection network shows A/B/F (acoustics/lighting/sensory-zoning) as one tightly-coupled sensory supercluster (Jaccard 0.44–0.67) — consider an A/B/F "Sensory Environment" supercategory. This does *not* mean categories are artificial (63% of edges cross letters — they are well-integrated); it is a narrow, specific mis-cut.

### 4.2 Specifications
- **Five overlapping stores; Part-4 prose is canonical; the JSON is orphaned and mis-mapped** — its `item_code` silently points at wrong items (JSON "F-07" holds visual-alarm/2440mm-corridor content; real F-07 = Thermal Zoning). **Retire it** — but it has four live consuming scripts and is named authoritative by the broken `DEPRECATED.md` pointer, so **fix the pointer (T-1) first**, harvest residual values into the DB, then archive. **[C]**
- **Structured-value coverage is 24/93** (verified: `jurisdictional_values` 20 ∪ `spec_value_probes` 4); **69 items are prose-only**; **6 items have no evidence slug at all** (A-13/A-15/B-08/G-02/G-07 + F-07); `item_bpc_links` covers **2 items**. Most "missing specs" are prose-present (a JSON-staleness artifact), but F-02/A-13/D-09 are genuinely qualitative where research supports a number. **[C]**
- **Conflict data is stranded** — `conflicts` table empty (0 rows) vs 12 markdown matrices; and structurally the item model **cannot express conflicts** (`connection_targets` holds 0 population codes; a conflict needs a `(pop_A, pop_B, parameter, resolution)` tuple). Template 4 renders nothing. **[C]**
- **The canonical divergence has no item** — turning-circle values (US 1524 / GB 1500 / DE 1500 / AU 1540 / ISO 1524) survive only as free-text inside **E-08's (corridor) `value_text`**; there is no turning-circle item (and DB G-01 = "Defensible Seating," not "turning circle" — a further prose↔DB drift). **[C]**

### 4.3 Rooms
- **Three disagreeing stores; the site is generated from a *wrong* matrix.** 9 residential rooms map 1:1 to Part 6; the 8 non-residential site rooms are cross-typology inventions with no Part-7 room source. The seed matrices don't match Part-6 prose (R-BA shares only 3 of 12 items, polluted with bedroom/nurse-call items), use `TC-` codes the schema rejects, and the seed writes to a **phantom `data/db/` path**; `site/rooms/r_ba.html:88` renders **`A-09 | PAIN`** (population code in the specification cell) with an empty criticality note. **[C]**
- **Missing room: the sensory/quiet room (A-16)** — the most-mandated non-residential space, absent from all 17 (that A-16 isn't in the 17 is [C]; whether it *should* be a distinct space entry is [H], but the target model in §6 treats it as one). Secondary [H]: outdoor/garden/terrace. **[C/H]**
- **Consolidate: R-HAL/R-COR and R-BA/R-WC** are residential↔non-residential duplicates of one *space* — dissolved by the building-type×space model (§6). (Network layer can't corroborate room merges — rooms aren't graph nodes — so these rest on seed/prose evidence.) **[C]**

### 4.4 Typologies (Part 7, currently a STUB in `parts/v10`)
- **Missing: NR-CARE** (residential-institutional / dementia-village care) — the project's deepest evidence base (5 care-village case studies, dominant DEM research) is split awkwardly between "Residential" and NR-HLT with neither fitting. *Observation* [C]; *new-typology remedy* [H]; the evidence base is **Global-North-only** (T-6). **[C/H]**
- **Consolidate/split: NR-HOS is incoherent** (bundles hotels→residential, restaurants→retail, conference→assembly, leisure/pool→orphaned aquatic) — split. NR-CUL is broad but coherent — keep. **[C/H]**
- **Coverage inversion (T-4):** NR-RET/CUL/HOS/TRP have no dedicated case studies or setting-specific research — confident headings with no queryable backing. **[C]**

---

## 5 · The six directions (condensed — full grounding in the intensification working papers)

**WHO · Population.** SCI(26)/EPI/MS are **enum-homeless**; `IntD` is enum-only (0 items). The population **hierarchy is a third dead consolidation** (enum rollup half-executed; `parent_code` never read → single-item tails ship as broken 1-item pages). Compounds are **four-way encoded**. **DEAF×circulation=0** (GAP-268). **SCI is a 25/26 copy of MOB** (only K-05 unique). Site ships **11 population pages** (SCI/AUT/PCS missing). **New:** CR-9 execute/retire the hierarchy; CR-10 parent-union resolver; CR-11 collapse compound-encoding + build a co-occurrence table; CR-12 de-dup SCI.

**WHERE · Jurisdiction.** 72% four-Western; five Global-South languages 0-searched; `lang_jur_map` empty; three jurisdiction universes + UK/GB seam; four Global-South BPCs orphaned & banner-retracted. **New missing (gated on reverifying the retracted GS BPCs):** squat-toilet, wet-room gradient (→G-04), split-facility bathroom, local-script wayfinding (→E-09/K-02), cultural A-16 variant. **New:** CR-13 populate `lang_jur_map` + AR/BN/HI/ID/SW vocabulary; CR-14 reconcile jurisdiction universes; CR-15 canonical turning-circle item + conflicts row.

**HOW-SOUND · Evidence.** Retracted substrate (T-2). **Co-1 systemic gap** — categories **A(0/19)/H(0/5)/I(0/4) have zero lived-experience evidence**; Co-1 never governs a value. **Code-floor repackaging** — **H = 88% code-floor / 0 anchor / 0 Co-1** (one grade-D BPC behind all 5 items); E=68%, B=56%; `convergence_assessment` = 0 convergent / 9 single-axis (confirms GAP-271). **Merge clusters** (pass the evidence gate): B-03…07; G-06/08/09+H-01/02/05; F-08/K-05; B-01/11 → ~11 items toward ~4. **Priority inversion:** re-anchor/merge before adding new items — only DeafSpace (#3, grade-A) is a safe addition now.

**WHEN · Lifecycle.** Stage/DAR/structural-backing are **schema-only + prose-only** (zero stored rows). **RFO/post-occupancy is the dead stage.** Three stage vocabularies; a **second stale item-numbering surface** (E-12 "Refuge enclosure", phantom I-05/I-06). **DAR is an orthogonal missing-item family** — only I-04 (hoist) is itemised; stairlift channel / through-floor-lift zone / wet-room recess / adjustable carcass / control conduit are homeless. **No entity type for programming/operational/commissioning** provisions. Good news: standard *editions* are current (AS 1428.1:2021) — decay is governance/versioning, not evidence.

**HOW-RELATED · Network.** 32 orphans (D-01, A-18, A-03/14, E-15, I-01 the highest-value under-wired). A-16 = 23-edge keystone (gate any split). Item model can't express conflicts or population-pairs (0 pop codes; `connection_type` 89% NULL; CROSS-POPULATION/prerequisite = 0 rows). Co-occurrence: 12 doctrinal pairs → **2 graph edges**. **New:** CR-16 evaluate A/B/F supercategory; CR-20 wire the orphans.

**WHAT-FOR · Functional-deficit/ICF.** No activity axis in the DB. **Whole ICF activities have zero items** (verified by name-search): **d550 eating, d640 laundry, d570 medication, d465 device-charging**; **d310–d360 expressive/AAC communication** under-covered vs hearing hardware; **d530 continence fixtures** (bidet/stoma/disposal) homeless. **E-14 is a real phantom** with inbound P1 references. **New:** CR-17 add the ICF-activity facet (+ lifecycle + conflict facets); new ADL items; resolve E-14.

---

## 6 · The target content model (reconciled)

Resolving the base/intensification model contradiction into one schema. The website needs an **item** entity carried on **six axes/facets**, over **reconciled single-source stores**:

1. **Category (component, A–K)** — canonical names fixed; thermal reconciled; A/B/F supercategory [H].
2. **Population (+ compound)** — hierarchy executed or flattened (one encoding); enum ⊇ SCI/EPI/MS; parent-union resolver; a co-occurrence/population-pair table.
3. **Building-type × space** — armature_v4's spatial axis, *implemented* (not the flat-17 site model), residential as one typology; NR-CARE added; NR-HOS split.
4. **ICF activity** — a new facet so "eating has no home" is queryable and consolidation can be activity-gated.
5. **Design-stage / DAR / lifecycle** — a real facet (SD/DD/CD/RFO + DAR rough-in vs end-state), so stage-gated workflow and adaptability are expressible.
6. **Conflict / population-pair** — a populated `conflicts` entity (from the 12 matrices) so Template 4 renders and the 12 co-occurrence pairs exist as edges.

Over stores where **one is canonical** per axis (T-1), with the **`DEPRECATED.md` authority pointer fixed first**, the dead JSON retired, and the phantom `room`/`specification` tables either built against real data or the generators retired.

---

## 7 · Consolidated register — what to fix (reconciled, de-duplicated)

**MISSING — items/axes our research supports.** Ranked by (research support × impact), gated by the priority in §8.
1. Accessible fire-evacuation refuge (safety-critical; GAP-C; note E-12 is already occupied — refuge has no code home) **[C]**
2. DeafSpace circulation geometry — ≥2440 mm signing-pair corridor (grade-A evidence; the **one safe addition now**; closes DEAF×E=0) **[C]**
3. OFS supine/recumbent recovery space (GAP-OFS-RECUMBENT-01) **[C]**
4. MH de-escalation room + female-only area (both self-flagged) **[C]**
5. ICF ADL items: device-charging (d465), eating (d550), laundry (d640), medication (d570), continence fixtures (d530), expressive/AAC communication **[C that no item exists; H that each becomes one]**
6. VIS audio wayfinding; emergency photoluminescent wayfinding; fire-door hold-open; biophilic interior views **[C/H]**
7. DAR rough-in family (stairlift channel, through-floor-lift zone, wet-room recess, adjustable carcass, conduit) **[H]**
8. Global-South set (squat-toilet, wet-room gradient, split-facility, local-script wayfinding, cultural A-16 variant) — gated on reverifying the retracted GS BPCs **[H]**
9. Resolve the E-14 phantom; the sensory/quiet room as a space **[C]**
- **Missing axes:** ICF-activity, lifecycle/DAR, conflict/population-pair, building-type×space (§6).

**CONSOLIDATE — what our syntheses justify** (every merge must pass the three-gate test, T-1 §2).
| # | Action | Conf |
|---|---|---|
| C-1 | Retire both dead item-consolidation manifests (88→65, CO-0003/D2) as inputs; strip false "MERGED" labels; re-derive merges via the three-gate test | **[C]** |
| C-2 | Retire `specification-database.json` — *after* fixing the `DEPRECATED.md` authority pointer (C-8) and its 4 consumer scripts | **[C]** |
| C-3 | Adopt part-file/TOC category names; correct `part04-item-index`; add K to TOC; delete stale `part05-j` | **[C]** |
| C-4 | Reconcile thermal into one home (Appendix C or a promoted category); fix K-05 misfile | **[C]** |
| C-5 | Merge evidence-cluster items that pass all three gates (candidates: B-03…07; reach-range G-06/08/09+H-01/02/05; F-08/K-05; B-01/11); demote the 5 no-slug items | **[H]** |
| C-6 | Collapse R-HAL/R-COR & R-BA/R-WC into single spaces under the building-type×space model | **[C]** |
| C-7 | Split NR-HOS; keep NR-CUL | **[C/H]** |
| C-8 | **Fix the governance authority pointer** (`DEPRECATED.md` → phantom path + condemned JSON) — prerequisite to all store reconciliation | **[C]** |
| C-9 | Execute or flatten the population hierarchy (one encoding; enum ⊇ SCI/EPI/MS; parent-union resolver); de-dup SCI vs MOB | **[C]** |
| C-10 | Reconcile the three jurisdiction universes + UK/GB seam; populate `lang_jur_map` | **[C]** |
| C-11 | Create a canonical turning-circle item + `conflicts` row; populate `conflicts` from the 12 matrices | **[C]** |
| C-12 | Wire the 32 orphan items (D-01, A-18, A-03/14, E-15, I-01 first) | **[C]** |
| C-13 | [H] Evaluate the A/B/F "Sensory Environment" supercategory | **[H]** |

---

## 8 · Prioritized roadmap (one reconciled sequence; all owner-gated)

- **P-1 · Governance prerequisite.** C-8 fix the authority pointer. Until "which store is canonical" is settled, every reconciliation below is undefined.
- **P0 · Unblock the site (low-risk, high-clarity).** C-3 (category names) · C-2 (retire JSON, post-C-8) · resolve the building-type×space model as a Decision Record · C-9/C-10 minimum (so `/populations` and `/rooms` don't ship broken stubs).
- **P1 · Structural.** C-1 (retire dead manifests) · C-4 (thermal) · C-6 (room de-dup) · C-11 (turning-circle + conflicts) · C-5 (merge zero-evidence clusters via the three-gate test) · add the missing axes (§6) · resolve E-14 · seed the room×typology matrix *from prose*, fix the population-code title corruption.
- **P2 · New content — only after the substrate is re-rehabilitated (T-2).** The §7 MISSING list, **starting with DeafSpace (#2, the one grade-A-backed addition) and the safety-critical refuge (#1)** · the ICF ADL items · NR-CARE · the Global-South set (post-reverification).

**The inversion that matters:** do **not** add new items first. Re-anchor the retracted substrate, fix the multi-store drift, and merge the zero-evidence clusters before growing the library — otherwise new PROVISIONAL items deepen the anchor deficit while 6 existing items still have no evidence at all.

---

## 9 · Takeaways for future work

1. **Fix the authority pointer before anything else.** `DEPRECATED.md` points at a non-existent DB and a condemned JSON. Every "which is canonical?" question — categories, specs, rooms, versions — is undefined until this one file is corrected. It is the cheapest highest-leverage action in the audit.
2. **Treat multi-store drift as the default, and add a parity check per axis.** The pattern (schema ≠ prose ≠ DB ≠ site) recurs everywhere; a cheap CI parity check per axis (DB↔enum populations, DB↔prose item names, values-store↔jurisdiction-enum) would catch the next drift before it ships — the same discipline the consolidation-sweep recommended for bpc/search-log twins.
3. **Add the four missing axes; the website's own templates already assume them.** Template 1 queries a `specification` table, Template 3 a `room` table, Template 4 a `conflicts` table — none exist. Building them is not scope creep; it is building what the IA already specifies. Draw the spatial axis from armature_v4, not a new invention.
4. **Consolidate with the three-gate test, never by name.** Evidence cleavage ∧ network role ∧ activity coverage. I-03/G-03 look like duplicates and aren't; seating items look mergeable but hold the only proxy for three ICF activities. The dead manifests are cautionary, not executable.
5. **Sequence: substrate → structure → content.** Re-rehabilitate the retracted evidence and merge zero-evidence clusters before adding items. Adding first is the failure mode the project's own next-steps synthesis warns about.
6. **Widen the evidence base along the two thin axes that most affect the mission:** Co-1 (lived experience — absent from acoustics, controls, upper-limb) and the Global South (72% Western; five languages unsearched; recovered research orphaned). Both are mission commitments the current structure quietly under-delivers.
7. **Guard the phantom/orphan surface.** E-14 has inbound P1 references to an item that doesn't exist; 32 items are graph-isolated; generators write to non-existent paths. A "no inbound reference to a non-existent code / no un-wired new item" check would keep the census honest.
8. **Render thin honestly on the site.** 69 prose-only items, four evidence-hollow typologies, and the retracted substrate should surface *as* provisional/thin — consistent with the mission's honesty posture and the ethics rules in `navigation-modes.md §6`. The disagreement and the gaps are part of the product, not something to paper over.

---

## Provenance & confidence

**Method:** structural four-axis pass (5 agents) → six-direction interrogation (6 agents, each tasked to refute) → two adversarial self-reviews → direct verification. **~25 highest-stakes claims re-verified against the live DB/files this session; every checked claim held**, including: the two conflicting category schemes; the deliberate no-J sequence; the JSON item_code mis-mapping; `conflicts`=0 / `jurisdictional_values`=109 (72% four-Western) / `spec_value_probes`=31; the 5 no-slug items and `item_bpc_links`={A-18,F-07}; `bpc_metadata` 68 RETRACTED / co1_pass_count=0 ×82; `connection_type` 89% NULL / 0 CROSS-POPULATION; 32 orphans; 24/93 structured coverage; DB G-01="Defensible Seating" + turning-circle in E-08 text; `seed_room_items.py` → phantom `data/db/`; SCI 25/26=MOB; E-12 double-booked; 4 Global-South BPCs banner-retracted; no eating/laundry/medication/charging item by name; 11 site population pages; the `DEPRECATED.md` phantom authority pointer.

**Confidence discipline:** [C] = verified this session; [H] = reasoned/owner-judgment. All new items and re-specs are HYPOTHESES held behind the PROVISIONAL banner; the merge groupings, the A/B/F supercategory, and the DAR/ICF facet decisions are modeling judgments the owner may resolve differently. **Anti-fabrication:** both self-reviews and all verifications passed — no checked agent claim failed; the project's documented failure mode (citation fabrication) did not appear. This document modifies no taxonomy, data, or item; it is the analysis on which owner rulings and scoped Change Orders can act.
