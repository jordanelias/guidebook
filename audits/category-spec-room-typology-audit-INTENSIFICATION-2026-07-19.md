> **Status: directional working papers (retained for per-claim file:line grounding).** The headline record is `audits/category-spec-room-typology-audit-2026-07-19.md` (comprehensive rewrite), which synthesizes and reconciles everything below into throughlines, one consolidated register, a target model, and takeaways. Read that first; use this for the granular per-direction evidence.

# Intensification — Six-Direction Interrogation & Challenge

**Date:** 2026-07-19
**Companion to:** `audits/category-spec-room-typology-audit-2026-07-19.md` (the base audit). This document does not repeat the base audit; it **queries the same content model from every cross-cutting direction the data exposes, and challenges the base audit from each.**
**Method:** six parallel directional-challenge agents — WHO (population), WHERE (jurisdiction/language/Global-South), HOW-SOUND (evidence/convergence), WHEN (lifecycle: stage/DAR/version), HOW-RELATED (connection network), WHAT-FOR (functional-deficit/ICF) — each instructed to refute or extend the base audit. **11 of the highest-stakes new claims were re-verified directly against the live DB/files this session** (listed in Provenance); every one held.
**Confidence key:** **[C]** verified this session · **[H]** reasoned, owner judgment.

---

## The master finding — the base audit's "multi-store drift" is not a spec problem; it is the shape of the whole model

The base audit found the specification layer split across five stores that silently disagree (§2.1). Interrogated from every direction, **that same pattern recurs on every axis of the content model.** This is the single most important result of the intensification:

| Axis | Stores that describe "the same thing" and disagree | Verified |
|---|---|---|
| Specifications | Part-4 prose · `jurisdictional_values` · `spec_value_probes` · `source_value_extractions` · dead JSON | base audit §2.1 |
| **Populations** | bare link code (`AUT`) · `subtype` string · enum sub-code (`NDV/AUT`) · `evidence_population_match` string — **four encodings** | **[C]** |
| **Jurisdictions** | enum (24) · `jurisdictional_values` (12) · `search_coverage` (47) · CRPD map (46) — **+ a UK/GB code seam** | **[C]** |
| **Versions** | TOC v8.9.3 · part-files v9-0 · versions/8.10 · v10-predraft · site v10.5 — **5 vintages + 3 orthogonal schemes** (DB schema_version, armature v4, PI v10_7–v14) | **[C]** |
| **Item numbering** | DB `items` · `part04-item-index` (base audit §1.2) · **Part-4 stage tables & Part-8 O&M (a *second*, different drift surface)** | **[C]** |
| **Conflicts** | empty DB `conflicts` table · 12 markdown matrices · `connection_targets` (0 population codes) | **[C]** |

**And the governance authority pointer is itself broken [C]:** `versions/current/DEPRECATED.md` designates as authoritative "`data/db/guidebook.db` (141 specifications)" — a path that **does not exist** (the live DB is `data/guidebook.db`, 93 items) — plus the very JSON the base audit says to retire. So "which store is canonical" is unresolved at the governance layer, not just fragmented at the store layer. **Any Change Order must first fix the authority pointer before store-level reconciliation is even well-defined.**

**Two facts reframe the base audit's entire remediation posture:**

1. **The evidentiary substrate is formally retracted. [C]** `bpc_metadata`: **68 of 82 slices = `RETRACTED-PRE-REHAB`, 13 NULL, 1 methodology; `co1_pass_count = 0` for all 82; `pico_complete = 0` for all 82.** Every one of the 93 items' evidence basis is currently retracted pending re-derivation. The base audit's "24/93 items have structured values" is a symptom; **the retracted substrate is the disease**, and it means *no* value in the model is presently adoptable as authority — exactly the "hold behind the PROVISIONAL banner" posture the project already holds, now quantified.

2. **The data model has only two of the axes it needs. [C]** It expresses **category (component A–K)** and **population**. It has **no queryable axis for**: ICF **activity** (design's actual purpose — one incidental `d440` in the whole DB), **design-stage / DAR / lifecycle** (schema-only fields on a non-existent table; zero stored rows), **conflict / population-pair** (empty table; 0 population codes in the connection graph), or **building-type × space** (the base audit's §0 finding). The guidebook's own doctrine — "design addresses functional *deficits*" (`toc.md` §1.3) — is structurally un-queryable.

---

## Corrections the intensification forces on the base audit

Folded into the base audit with markers; recorded here for the audit trail.

| Base-audit claim | Correction | Source |
|---|---|---|
| §5: *"No item is evidence-free — 100% have ≥1 BPC mapping"* | **REFUTED [C].** 5 active items have **no evidence slug and no `item_bpc_links`**: A-13, A-15, B-08, G-02, G-07 (F-07 also NULL-slug). The "100%" came from a prose reconciliation doc, not the link tables. | evidence dir |
| §2.5: *"13 populated conflict matrices"* | **12 conflict domains + 1 synthesis roll-up**, and 2 of the 12 are reclassified as non-conflicts (CORRIDOR-W retired, FRAGRANCE minimal). | relational dir |
| §1.5 / CR-5: I-03 ↔ G-03 grab-bar **"duplication"** | **Downgrade to "naming/scope overlap."** Their connection neighborhoods are near-disjoint (**Jaccard 0.09**, one shared neighbor); they've accreted different network roles (I-03 = UPL bathroom bundle; G-03 = clinical grab-bar positioning). Not a topological duplicate — merging by name would collapse two differently-wired subgraphs. | relational dir |
| §4.2/§4.4: dementia-dominance | **Mis-attributed to dementia alone.** At the *item* layer it is a **DEM(55)+VIS(43)+OFS(31)+SCI(26) four-way** top — VIS is co-dominant and spans all 10 categories. "Over-fit to dementia" overstates; "over-fit to the four best-evidenced populations" is exact. | population dir |
| §4.2: NR-CARE "deepest evidence base" | Add a caveat: that evidence base (De Hogeweyk/Village Landais/Carpe Diem/Il Paese/Verbeek) is **entirely Global-North** — the most-covered typology is also the most geographically parochial. | jurisdiction dir |
| CR-6: room merges (R-HAL/R-COR, R-BA/R-WC) | **Scope limit:** rooms are not nodes in the connection graph (0 room codes in `connection_targets`), so the relational layer can neither corroborate nor refute these merges — they rest on seed/prose evidence only. | relational dir |

None of these overturn the base audit's spine; they sharpen it. The base audit's §5 missing-item list survived every direction unrefuted (population and evidence vantages independently *strengthened* #1 refuge, #2 supine-recovery, #3 DeafSpace).

---

## §I · WHO — Population direction

- **[C] Enum-homeless populations.** The DB `populations` FK is internally clean (22 codes, 0 orphans), but three of the most-covered populations are **absent from the canonical enum** (`schemas/enums.py`): **SCI (26 items — 5th-most-covered), EPI, MS.** Conversely **`IntD` is in the enum but has 0 items** (proxied through DEM+NDV). The drift is DB↔enum, not within the DB. *(This corrects the intensification's own starting premise that SCI etc. were "rogue" DB codes.)*
- **[C] The population hierarchy is a third dead consolidation** (alongside the base audit's two item-consolidation manifests, §1.6). The enum specifies rollup (`NDV/AUT`, `MOB/UPL`, "sub-code implies parent"); the DB **half-executed** it — SCI/ADHD/EPI/MS/CFS/MCAS/POTS are parented, but **AUT/PCS/SENS/MH/UPL are top-level** — and **`parent_code` is never read** (`population_page.py:53` resolves flat, no parent union). So the promised inheritance is unimplemented.
- **[C] Consequence — single-item tail pages are broken stubs.** ADHD/EPI/MCAS/POTS/SENS have 1 item each, and their item is *disjoint* from the parent's set, so with no rollup a generated page renders literally "Applicable items (1)." SENS is `parent_code=None` — a permanent 1-item page.
- **[C] SCI is a 25/26 near-copy of MOB** (verified; only K-05 is SCI-unique — fittingly, the misfiled thermal item, since thermoregulation is an SCI issue). The link table is incoherent about its own semantics: tails store *deltas* needing inheritance, SCI stores a *full copy* needing none.
- **[C] Quadruple compound-encoding.** Upper-limb / mental-health / post-concussion / autism are each encoded up to four ways (bare code · `subtype` · enum sub-code · evidence-match string). Population-axis twin of the five-spec-store finding.
- **[C] Coverage matrix corroborates GAP-268 at the item level:** DEAF has **E=0 (circulation), C=0, F=0, I=0** — quantifying the "DEAF structurally invisible" gap and the base audit's §5-#3 (DeafSpace corridor). AUT (×D=0,E=0) and PCS (×D=0,E=0) — large sensory populations with zero wayfinding/circulation items, an inheritance artifact (un-parented from NDV/DEM).
- **[C] Site invisibility:** only **11 population pages** ship (`site/populations/`); SCI (26 items), AUT (19), PCS (20) — three of the top-9 — have no page.
- **New consolidations — CR-9** execute or retire the population hierarchy; **CR-10** implement parent-union resolution before generating tail pages; **CR-11** collapse the quadruple compound-encoding + build a co-occurrence/compound table; **CR-12** de-duplicate SCI against MOB.

---

## §II · WHERE — Jurisdiction / Language / Global-South direction

- **[C] The structured value store is 72% four-Western-jurisdictions.** `jurisdictional_values` by jurisdiction: DE 20, GB 20, US 20, AU 18, ISO 13, FR 5, NO 5, EU 4, CA 1, CH 1, JP 1, SG 1. DE+GB+US+AU = **78/109 = 72%**; the **only** Global-South presence is SG=1 and JP=1. The base audit called this the "healthy canonical store" — counting rows, not geography.
- **[C] The African / South-Asian / Arab language axis is untouched.** `search_languages`: Swahili, Hindi, Bengali, Arabic, Indonesian all **0 searched / 0 results** across all 81 slugs; `tier6_attempted = 0` for all 47 jurisdictions. The "non-English recovery" recovered European + East-Asian; it did not reach the Global-South language axis. `lang_jur_map` is **empty**, so jurisdiction×language cannot be crossed and English-only-searched jurisdictions (NG/GH/ZA/PH) can't be flagged as missing native standards.
- **[C] Four `*-global-south` BPCs are complete research but structurally orphaned** (verified: all 4 exist, all banner-retracted PRE-REHABILITATION). No item links them; the gaps they cite (GAP-LRP-02…05) aren't in the DB. Stranded provisions with no home: **accessible squat/semi-squat toilet** (4 billion users; "no peer-reviewed design exists globally"), **wet-room floor gradient ≥1:50** (G-04 has no gradient spec), **split-facility two-room bathroom**, **local-script tactile signage + precast/solar wayfinding**, **low-resource sensory space**, **informal-settlement housing scope**.
- **[C] The canonical divergence example has no live item at all.** Turning-circle values (US 1524 · GB 1500 · DE 1500 · AU 1540 · NO 1500 · ISO 1524) survive **only as free-text inside E-08's (corridor) `value_text`** — there is no turning-circle item; DB `G-01` is "Defensible Seating," not "turning circle" (a further item-code/prose naming drift). The base audit found turning-circle duplication only in the *dead* JSON; the *live* DB has no turning-circle item.
- **[C] Challenge:** the base audit's §5 missing-techniques list is entirely Western-evidence-derived and omits every Global-South idiom above — a real blind spot, not a calibration nitpick. And A-16 (sensory room) needs a **cultural variant** — its private-individual-retreat model doesn't transfer to collectivist cultures (family-accompanied / unlabelled / outdoor).
- **New — CR-13** populate `lang_jur_map` + stand up AR/BN/HI/ID/SW vocabulary; **CR-14** reconcile the three jurisdiction universes + UK/GB seam; **CR-15** create a canonical turning-circle item + `conflicts` row; **new missing items** (all [H], and gated on reverifying the retracted GS BPCs): squat-toilet, wet-room gradient (→G-04), split-facility, local-script wayfinding (→E-09/K-02), cultural sensory-room variant (→A-16).

---

## §III · HOW-SOUND — Evidence / Convergence direction

- **[C] Retracted substrate** (68/82; co1_pass_count=0; pico_complete=0 corpus-wide) — see master finding.
- **[C] Co-1 (lived experience) is a systemic, mission-level gap.** No slice has ever passed a Co-1 gate; 30 stray Co-1 sources exist but **categories A (0/19 items), H (0/5), I (0/4) have zero Co-1 evidence** — acoustics (the largest category) and the two categories governing daily autonomy (controls, upper-limb) rest on no lived experience. Where Co-1 sources exist they **never govern a value** (`convergence_assessment`: the 2 Co-1-bearing rows are `pending_assessment`).
- **[C] Code-floor "compliance repackaging."** Category tier profiles: **H = 88% code-floor / 7% anchor / 0 Co-1** (all 5 items on one grade-D retracted BPC); E = 68%; B = 56% (B-03…B-07 all on `therapeutic-lighting-design`, grade **E**, 0 confirmed evidence). Per `tier-system.md` §3, a category built on T4–T6 codes is convergence-not-evidence. `convergence_assessment` status: **0 convergent, 9 single-axis, 3 pending** — not one cell demonstrates genuine multi-axis value agreement (confirms GAP-271); A-02 NRC and A-08 NC-25 are self-documented "convergence-not-evidence" code conventions.
- **[C] Refutes the assumption that K (Deafblind) is thin.** K-01…K-04 are the **best-anchored items in the model** (68% anchor, 3 Co-1, grade A/B BPCs). Only K-05 (the misfiled thermal item) is weak. K is a *real, well-evidenced* category — strengthening the base audit's case to keep it and fix only K-05.
- **[C] The merge case is far larger than the base audit's three items (A-09/A-02/B-01).** Shared-zero-anchor-BPC clusters the evidence cannot separate: **B-03/04/05/06/07** (one grade-E BPC) → 1 item; **G-06/08/09 + H-01/02/05** (one grade-D no-anchor reach-range BPC, spanning two categories) → 1 item; **F-08/K-05** (thermoregulation) → 1; **B-01/B-11** (circadian) → 1. ~11 items collapse toward ~4. Plus the **5 no-slug items** (A-13/A-15/B-08/G-02/G-07) as demotion candidates.
- **[C] Challenge — priority inversion.** The base audit's §5 new items lean on the *weakest* slices (OFS `ofs-built-environment` grade D no-anchor; MH grade B but few anchors, Co-1 non-governing). Only **DeafSpace (#3)** rests on a grade-A BPC (`deaf-spatial-design`, 5 Co-1) — the one addition the evidence clearly supports. **Re-anchor/merge the zero-evidence existing items before adding new PROVISIONAL ones** (DeafSpace excepted).

---

## §IV · WHEN — Lifecycle (stage / DAR / version) direction

- **[C] Stage, DAR, and structural-backing are schema-only for a non-existent table** (`specification.py:79,106,110`), with **zero stored data anywhere queryable** — no `design_stage*`/`dar*`/`adapt*`/`commission*` column exists in any live table. The base audit's "69 prose-only items" understates it: the *lifecycle metadata for all 93* is prose-only. Even building Template 1's missing `specification` table would render empty stage/DAR facets.
- **[C] RFO / post-occupancy is the dead stage** — `part08:54` defines SD·DD·CD·**RFO**, but the room matrix uses only SD/DD/CD; zero items and zero room rows land at RFO. And the room-matrix seed writes to a **phantom `data/db/guidebook.db` path that does not exist** (verified), so its stage data never lands regardless.
- **[C] Three conflicting stage vocabularies** (DD = "Design Development" `part08` vs "Developed Design" `part04` vs a RIBA Schematic/Technical/Construction/Handover scheme `part04 §4.4`). No authoritative stage taxonomy.
- **[C] A second stale item-numbering surface the base audit missed.** Part-4 stage tables and Part-8 O&M map stages onto codes that disagree with the DB: **E-12 is double-booked** (DB "Entrance Landing & Manoeuvring" vs Part-8 "Refuge enclosure / evacuation-lift"); I-03/I-04 are remapped; **phantom items I-05, I-06** are cited in `part04:69` and `part08:302`. Items can't be reliably placed in a stage-gated workflow because their codes don't resolve consistently.
- **[C] DAR is an orthogonal missing-item family.** Only **I-04 (ceiling hoist)** models a DAR rough-in as an item; the library otherwise models installed *end-states*. Homeless rough-ins: **future stairlift channel, through-floor-lift shaft zone, wet-room floor recess, adjustable kitchen carcass void, smart-control conduit** (all in Part-10/Part-6 DAR registers). Whether each should become an item is [H]; the *asymmetry* (end-state itemised, rough-in not) is [C].
- **[C] No entity type for programming / operational / commissioning provisions** — generalizes the base audit's "D-09/F-06 operational" note: F-02, F-06, the CAPABLE model, "private space per patient = programming rule," and the entire Part-8 O&M/commissioning schedule are un-housable in an item model that has only design components.
- **[C] Partial refute (good news):** the stale-*evidence* worry is false — the DB cites current standard editions (AS 1428.1:**2021**, IEC 60118-4:**2018**); supersessions were applied. The decay is **temporal/governance** (5 doc vintages, broken authority pointer, a supersession tracker whose own "monitor" windows for NCC 2025 / ICC A117.1-2026 are now past), **not evidentiary**.

---

## §V · HOW-RELATED — Connection-network direction

- **[C] 32 of 93 items are graph orphans** (zero connection edges) — *up* from the May audit's 28, because phantom→item conversions created under-wired items. High-value isolates that clearly *should* connect: **D-01** loop-plan (cited in every DEM wayfinding matrix, zero edges), **A-18** RT60 (best-evidenced acoustic item, zero edges), **A-03/A-14** acoustic doors, **E-15** Changing Places, **I-01** hardware. These are missing-*connection* findings, not deletion candidates.
- **[C] A-16 (Sensory/Quiet Room) is the keystone node — 23 connections, the single most-connected item**, spanning A/B/D/F/H/I/K. **New caution the base audit missed:** its §3.2 (missing room) and §5-#5/CR-5 (split into 3 quiet-space types) both touch A-16, but decomposing the densest hub is a **high-blast-radius change** (23 edges to re-home) the topology should gate.
- **[C] The item model structurally cannot express conflicts.** `connection_targets` contains **zero population codes** (all 507 are item codes / part pointers / prose); a conflict needs a `(pop_A, pop_B, parameter, resolution)` tuple that exists nowhere (`conflicts`=0). Homeless conflicts: **MOVE-FREE** (DEM wander vs MOB containment — no item, Part-7 matrices only) and **SPATIAL-OPEN** (DEAF sightlines vs NDV enclosure — resolution is building-level zoning, a spec-note on A-16, not a node). The DEAF+NDV enclosure conflict is **not resolvable in the current taxonomy** as a distinct entity.
- **[C] Co-occurrence is the largest representation gap.** 12 doctrinal pairs (Part 3 §3.10) + 5 worked examples + 12 conflict matrices reduce to **2 `COMPOUND-INTERACTION` edges and 0 `CROSS-POPULATION` edges** in the graph. `connection_type` is **89% NULL**; the enum permits CROSS-POPULATION and METHODOLOGY but both have **0 rows**; there is **no reinforces / depends-on / supersedes / prerequisite** relation — so sequencing ("turning circle FIRST," loop-plan-before-everything) is inexpressible.
- **[C] Refutes "artificial category boundaries" for A–K as a whole** — **63% of multi-item connections cross category letters** (E–I, C–D, A–F top edges); the taxonomy is heavily interwoven, not siloed. **But** A/B/F form a tightly-coupled **sensory supercluster** (internal Jaccard 0.44–0.67) — a relational analogue of the thermal-fragmentation finding: acoustics/lighting/sensory-zoning may be one design domain fragmented into three letters. **[H] CR-16:** consider an A/B/F "Sensory Environment" supercategory.

---

## §VI · WHAT-FOR — Functional-deficit / ICF direction (the most literal reading of the source topic)

- **[C] The DB has no activity axis at all** — one incidental `d440` across 41 tables. Items map to populations, never to ICF activities; `schemas/item.py` has no activity field. The guidebook's own §1.3 doctrine ("design addresses functional *deficits*") is the single most literal thing the data model fails to express.
- **[C] Whole ICF activities have zero items** — invisible to an A–K component scan because they were never categories:
  - **d550 Eating** — no dining/eating item (FDR-NEW-06 proxies I-02 kitchen + G-07 seating).
  - **d640 Housework / laundry** — no item, despite a full research file (`fdr/accessible-laundry-room-design.md`).
  - **d570 Health / medication management** — no item (refrigerated-med storage, routine cueing, monitoring — proxied to B-10 fire alarm).
  - **d465 Moving using equipment** — partial: the model covers *manoeuvring* a device (E-12) but never **charging/storing** it (FDR-NEW-10, FDR-ENV-03 register the deficit; no item). Classic omission.
  - **d310–d360 Expressive communication** — dense hardware for *hearing* (loops, captioning) but **nothing for being understood** (AAC/speech-generating-device support; FDR-NEW-14 mis-routed to F-02 Olfactory).
  - **d530 Toileting depth** — facility-level covered (G-03/G-04/E-15) but continence fixtures (bidet/wash-dry rough-in, stoma/catheter, adult sanitary disposal) have no item — confirms the base audit's "bidet rough-in (HYPOTHESIS)" as a real d530 gap.
- **[C] E-14 is a real phantom with inbound P1 references.** FDR-NEW-15/16 (d440 tremor / tetraplegia-ECU, both P1) target **E-14**, which does not exist in the DB (93 items, not 94); it survives only as draft `parts/v10/e14-entrance-rest-seating.md`. The base audit reasoned over the 93 existing items and never checked *inbound* references to a 94th. (Corroborated by the network direction: E-14 is the last remaining phantom target.)
- **[C] Challenge — the missing third axis.** The base audit's §0 two-axis model (building-type × space) is necessary but **not sufficient**: eating happens in cafés/living-rooms/bedrooms, so a missing *room* under-counts a missing *activity*. The complete coverage model is **building-type × space × activity(ICF)**. §5 found *technique*-novel gaps (refuge, DeafSpace…) but structurally missed the *ADL-completeness* gaps (eating, laundry, medication, device-charging) — a complementary gap class.
- **[C] Undercuts a consolidation.** Collapsing the seating family (G-01/G-02/G-07/A-17…) by component similarity would erase the only (proxy) coverage of three distinct ICF activities — d410 sit-to-stand, d550 eating, d540 dressing. **Consolidation must be gated on an activity-coverage check** the base audit never ran.
- **New — CR-17** add an ICF-activity facet to the item entity; **new missing items** (each with a live FDR file/scenario): mobility-device charging & storage (d465), eating/dining environment (d550), laundry (d640), health/medication (d570), continence fixtures (d530), expressive/AAC communication (d310–d360); **resolve E-14** (promote the draft or reassign its inbound P1 references).

---

## Consolidated new register (extends the base audit's CR-1…CR-8)

| # | Item | Direction | Type | Conf |
|---|---|---|---|---|
| CR-9 | Execute or retire the population hierarchy (enum rollup half-done, `parent_code` unread; enumerate SCI/EPI/MS; fix IntD) | Population | consolidate | [C] |
| CR-10 | Implement parent-union item resolution before generating tail/SCI/AUT/PCS pages | Population | fix | [C] |
| CR-11 | Collapse the quadruple compound-encoding; build a co-occurrence/compound-population table | Population/Network | consolidate | [C] |
| CR-12 | De-duplicate SCI (25/26 = MOB) | Population | consolidate | [C] |
| CR-13 | Populate `lang_jur_map`; stand up AR/BN/HI/ID/SW vocabulary | Jurisdiction | fix | [C] |
| CR-14 | Reconcile the three jurisdiction universes + UK/GB code seam | Jurisdiction | consolidate | [C] |
| CR-15 | Create a canonical turning-circle item + `conflicts` row (buried in E-08 text) | Jurisdiction/Network | missing+consolidate | [C] |
| CR-16 | Evaluate an A/B/F "Sensory Environment" supercategory (Jaccard 0.44–0.67) | Network | consolidate | [H] |
| CR-17 | Add an ICF-activity facet to the item entity (+ a lifecycle/DAR facet, + a conflict/pop-pair entity) | Functional/Lifecycle | fix | [H] |
| CR-18 | Fix the governance authority pointer (`DEPRECATED.md` → phantom `data/db` path + condemned JSON) before any store reconciliation | Lifecycle | fix | [C] |
| CR-19 | Merge the shared-zero-anchor-BPC item clusters (B-03…07; G-06/08/09+H-01/02/05; F-08/K-05; B-01/11) — evidence cannot separate them | Evidence | consolidate | [H] |
| CR-20 | Wire the 32 orphan items (priority: D-01, A-18, A-03/14, E-15, I-01) | Network | fix | [C] |

**New missing items (all [H], PROVISIONAL, owner-gated):** mobility-device charging/storage (d465) · eating/dining (d550) · laundry (d640) · health/medication (d570) · continence fixtures (d530) · expressive/AAC communication (d310–d360) · DAR rough-in family (stairlift channel, through-floor-lift zone, wet-room recess, adjustable carcass, control conduit) · Global-South set (squat-toilet, wet-room gradient→G-04, split-facility, local-script wayfinding→E-09/K-02, cultural A-16 variant) · resolve E-14.

## Revised priority (supersedes the base audit's §7 P-order where they conflict)

The intensification inverts one of the base audit's implicit priorities: **do not add new items first.**

- **P-1 (governance prerequisite):** CR-18 fix the authority pointer — until "which store is canonical" is settled, every other reconciliation is undefined.
- **P0 (unblock, low-risk):** base CR-2/CR-3 (retire JSON / canonical category names) · CR-9/CR-10 (population hierarchy + resolver, or the site ships broken tail pages) · CR-13 (lang_jur_map).
- **P1 (structural):** base CR-1/CR-4/CR-6 · CR-11/CR-12/CR-14/CR-15 · CR-17 (add the missing axes) · resolve E-14 · **CR-19 merge the zero-evidence clusters** and re-anchor the 5 no-slug items.
- **P2 (new content — only after the substrate is re-rehabilitated per the project's banner posture):** the §5 list, **starting with DeafSpace (#3, the one grade-A-backed addition)** and the safety-critical refuge (#1); the ICF ADL items; the Global-South set (gated on reverifying the retracted GS BPCs); NR-CARE.

**The deepest single conclusion:** the base audit asked "what's missing / what to consolidate" within the taxonomy. The intensification's answer is that **the taxonomy is under-dimensioned** — it has category and population but lacks activity, lifecycle, and conflict axes — and **its evidentiary substrate is retracted**. Filling item-gaps and merging duplicates is real work, but it is downstream of restoring the evidence and adding the axes the model needs to express its own doctrine.

---

## Provenance & confidence

Six directional-challenge agents, each grounded in DB query or file+line and instructed to refute the base audit. **11 highest-stakes new claims re-verified directly this session — all held:** (1) `bpc_metadata` 68 RETRACTED / co1_pass_count=0 ×82; (2) 5 no-slug items A-13/A-15/B-08/G-02/G-07; (3) `connection_type` 89% NULL / 0 CROSS-POPULATION; (4) DB G-01 = "Defensible Seating"; (5) `jurisdictional_values` 72% DE/GB/US/AU, SG+JP=2; (6) 11 site population pages; (7) turning-circle buried in E-08 `value_text`; (8) `seed_room_items.py` targets non-existent `data/db/`; (9) SCI 25/26 = MOB, only K-05 unique; (10) E-12 double-booked as "Refuge enclosure" in `part08`; (11) 4 Global-South BPCs exist, all banner-retracted. No agent claim that was checked failed — consistent with the anti-fabrication result from the base audit's self-review.

**Residual honesty:** the merge groupings (CR-19), the supercategory (CR-16), and every "new missing item" are HYPOTHESES for owner ruling / scoped Change Orders; the DAR-rough-in-as-item and ICF-facet questions are modeling judgments the project may resolve differently. Nothing here modifies the taxonomy, data, or any item.
