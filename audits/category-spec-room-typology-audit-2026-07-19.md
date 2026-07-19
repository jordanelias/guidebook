# Category / Specification / Room / Typology Audit

**Date:** 2026-07-19
**Author:** Claude Code — five parallel deep-investigation passes (one per dimension: categories, specifications, rooms, typologies, research-driven missing techniques), each grounded in file+line or DB query, followed by direct verification of the five highest-stakes claims against actual file contents.
**Scope:** the four content-model axes the website navigates — the A–K **category** taxonomy (Part 4), the **specification** layer, the **room** taxonomy (Part 6 + `site/rooms/`), and the non-residential **building-typology** taxonomy (Part 7). Two questions per axis: *what are we missing that our research supports*, and *what should we consolidate that our syntheses justify*.
**Companion to, not replacement of:** `audits/consolidation-sweep-2026-07-12.md` (repo/process fragmentation) and `audits/project-shape-audit-2026-06-22.md` (pipeline shape). This audit is the **content-model** layer those two deliberately did not cover.
**Lens:** the deliverable is now a website (`workplan/website-v0-path-forward-2026-07-12.md`, `architecture/navigation-modes.md`). Every axis below is a live navigation surface — `/specs` category filter, `/rooms` Room Navigator (split residential/non-residential), `/specs/[item_code]`. One axis (rooms) is already a **named, blocking open gap** for v0. Findings are framed against that build.

**Confidence key:** **[C]** CONFIRMED (verified against source this session) · **[H]** HYPOTHESIS (reasoned from evidence, needs owner judgment).

---

## Executive summary

The evidence corpus is mature; the **content model that renders it is not reconciled**. Across all four axes the same pattern recurs: multiple stores describe the "same" structure and silently disagree, while the research has moved ahead of the taxonomy it is supposed to populate. None of the four axes is currently in a state a website could ship a clean navigation surface on top of without a reconciliation pass.

| Axis | Headline "missing" | Headline "consolidate" | Website-blocking? |
|---|---|---|---|
| **Categories (A–K)** | A **Thermal / Environmental-Comfort** category — F-04, F-07, F-08, K-05 and the Appendix-C TC-items are homeless or misfiled **[C]** | Two conflicting A–K naming schemes; **two dead consolidation manifests** (88→65 and CO-0003/D2) whose strikes the DB never applied **[C]** | Yes — `/specs` category filter + Master Index need one canonical name per letter |
| **Specifications** | 69 of 93 items have **no structured value in any queryable store** (prose-only); genuine qualitative-gaps at F-02, A-13, D-09 **[C]** | Retire `specification-database.json` — its `item_code`s silently point at the **wrong items**; duplicate specs (turning-circle ×4) and garbage records inside it **[C]** | Yes — Template 1 (Spec Page) queries a `specification` table that does not exist |
| **Rooms** | The **sensory / quiet room** — the most-mandated non-residential space (A-16) — is absent from all 17 site rooms **[C]** | R-HAL/R-COR and R-BA/R-WC are residential↔non-residential duplications of one space **[C]** | **Yes — this is the named open v0 gap**: no room table exists; seed matrices are *wrong*, not just thin |
| **Typologies (7 NR)** | **NR-CARE** (residential-institutional / dementia-village care) — the project's deepest evidence base has no Part-7 home **[C]** | Split the incoherent **NR-HOS** bundle; NR-RET/CUL/HOS/TRP are headings with **zero case studies** behind them **[C]** | Indirect — `/rooms/non-residential/` needs a resolved model |

**The one cross-cutting structural finding (both the rooms and typology passes reached it independently):** residential is modeled as **rooms** (Part 6) and non-residential as **building types** (Part 7), and the website flattens both into 17 generic rooms — losing the typology axis entirely and *still* not covering the room set. The clean resolution is a **two-axis model: building-type × space**, with residential treated as one more typology. This single decision resolves the Part-6/Part-7 inconsistency, the site-flattening, and gives the missing NR-CARE typology a natural home — see §5.

**What this audit does NOT do:** it does not execute any consolidation, create any item, or edit the taxonomy. Per the project's own standing posture (`workplan/next-steps-synthesis-2026-07-14.md`: hold solo-adjudicated determinations behind the PROVISIONAL banner; govern by Change Order), every actionable below is a **candidate for owner ruling / a scoped CO**, not a fait accompli.

---

## §0 · Cross-cutting structural finding — the two-axis model

**[C]** Three facts, independently confirmed by the rooms and typology passes:

1. **Part 6 (residential) is room-based** — 9 rooms R-ENT…R-STA, 1:1 with `site/rooms/` residential slugs (`parts/88_to_90/part06_v9-0_2026-03-20.md:47–518`).
2. **Part 7 (non-residential) is typology-based** — 7 building types NR-EDU…NR-TRP, each of which *internally* re-decomposes into a space/room table (`parts/88_to_90/part07_v9-0_2026-03-20.md:25,33–36,62,71–76,102,112–114`).
3. **The website flattens both into 17 generic rooms** (`site/rooms/`, `scripts/db/seed_room_items.py`), inventing 8 non-residential "rooms" (R-REC/R-COR/R-OFC/R-CAN…) that have **no Part-7 source as rooms**, and dropping Part-7's own most-mandated space (the A-16 sensory/quiet room). The typology axis — per-building-type population priorities, signature items, IntD/DBL provisions — is **lost entirely** on the site.

The two sides answer different questions (residential users think in rooms; non-residential designers think in building types), and the flat-17 site model is the worst of both — it neither preserves typology context nor completely covers the rooms.

**Recommendation [H]:** adopt a **building-type × space** model.
- **Space** (reception, WC, corridor, sensory room, bedroom…) is the reusable unit, built from the shared A–K item library.
- **Building type / typology** is the entry axis; it selects which spaces appear and overrides item values per space (e.g. corridor width steps to ≥1800 mm specifically for Healthcare/Transport — `part07_v9:11`; reception A-10/G-06 treatment differs HLT `:70` vs TRP `:239`).
- **Residential becomes the 8th typology**, not a separate room-only Part 6 — it already behaves as one (NR-HOS imports "Part 5 residential spec" for hotel rooms, `part07_v9:209,218`).

For the website: `/rooms` should become (or be paralleled by) a typology entry that resolves `/[typology]/[space]`, rather than a flat 17-room list. This is the scoped room-data-model decision `website-v0-path-forward` §"What is explicitly NOT done" is waiting on.

---

## §1 · Categories (A–K)

### 1.1 The taxonomy is real but its *names* live nowhere canonical
**[C]** DB `items` has a `category` letter but **no `category_name` column** (though `schemas/item.py:33` declares one). Category names exist only in prose/TOC — which is exactly how two schemes drifted unchecked. The site sidesteps it, rendering only `category: <letter>` (`site/specs/k-03.html:40`).

### 1.2 Two conflicting naming schemes — `part04-item-index.md` is wrong for G/H/I/K
**[C]** The **part-file + TOC scheme is canonical and matches item contents**; the `part04-item-index.md` "Category Summary" (lines 106–115) is a stale earlier scheme that **matches no current items**:

| Ltr | Canonical (part files + `toc.md`) | `part04-item-index.md` (STALE — matches nothing) | Contents cohere under canonical? |
|---|---|---|---|
| A | Acoustics | "Acoustic & Sensory Environment" | ✓ |
| B | Lighting | "Lighting & Visual Environment" | ✓ |
| C | Colour and Surface Finish | "Colour, Contrast & Pattern" | ✓ |
| D | Spatial Layout and Wayfinding | "Wayfinding & Signage" | ✓ (D-11 garden outlier) |
| E | Entry and Circulation | "Entrances, Circulation & Thresholds" | ✓ |
| F | Sensory Zoning | "Environmental Controls & Air Quality" | **partial — thermal F-07/F-08 don't fit** |
| G | Furniture, Fixtures and Interior Elements | "Bathroom & Wet Area" | canonical ✓; index wrong (only 2/9 are bathroom) |
| H | Controls, Technology & Environmental Control | "Kitchen, Workspace & Controls" | canonical ✓; index wrong (0 kitchen items) |
| I | Upper Limb and Amputation Provisions | "Seating, Rest & Recovery" | canonical ✓; index **completely wrong** (0 seating items) |
| K | **Deafblind Environment Provisions** (`part05-k…:1`) | "Safety, Grab Bars & Support" | neither perfect; canonical fits K-01…K-04, index wrong (grab bars live in G-03) |

Secondary: **TOC omits Category K entirely** (ends at I) and is stale on membership (missing F-06/07/08, H-05, I-04, A-18, E-15 — all active in DB).

### 1.3 The J question — RESOLVED: the no-J sequence is *deliberate*
**[C]** There were two different Category J's:
- **Original J = Bariatric Provisions (J-01…J-05)** — struck by `CO-0001-2026-03-18-1900.md:198–206` and redirected to the Supplementary Volume; now a hard standing rule (`references/project-standards.md:29`: "No J-code is permitted in Volumes I–II. Delete on sight.").
- **Deafblind provisions were briefly drafted as J, then renumbered J→K** to avoid reusing the struck label — hence two sibling files with identical content: `parts/88_to_90/part05-j_v9-0…:1` ("CATEGORY J: DEAFBLIND…") and `part05-k_v9-0…:1` ("CATEGORY K: DEAFBLIND…").

So **A–K-minus-J is intentional**, not an accidental gap. **Cleanup debt:** the stale `part05-j_v9-0…` duplicate should be deleted, and K should be added to `references/toc.md`.

### 1.4 MISSING category — Thermal / Environmental-Comfort **[C, HIGH]**
Thermal specification is scattered with **no coherent home**:
- **F-04, F-07, F-08** (air quality/thermal stability, thermal zoning, thermal transition) sit under Category **F = "Sensory Zoning"** — a poor fit.
- **K-05 "Thermal Comfort Assessment for Thermoregulation-Impaired Populations"** sits under **K = Deafblind** — an outright misfile (verified: DB K-05 name confirmed; DB F-07 = "Thermal Zoning").
- **TC-01…TC-05** are exiled to Appendix C (`toc.md:424–430`).
- The research corpus has a *dedicated* domain (`references/bpc/.../thermoregulation-built-environment`), so thermal is a first-class evidence area with no first-class category.

**Candidate ruling:** create a Thermal / Environmental-Comfort category, re-homing F-04, F-07, F-08, K-05 and the Appendix-C TC-items. (This is the only *genuine* missing category — safety, outdoor, digital, and operational were each evaluated and found adequately housed or too thin; see the category pass for the negative cases.)

### 1.5 Misfiled items **[C/H]**
- **K-05** (thermal) under K=Deafblind — **[C] HIGH**, unambiguous.
- **I-03 "Bathroom (…Bilateral Grab Bars…)" duplicates G-03 "Grab Bars…"** — **[C]** verified: both are grab-bar items. Redundancy across I (upper-limb) and G (fixtures).
- **G-09** (bedroom emergency call **and overnight lighting**) straddles G/B(B-12)/H(H-05); **H-02** carries temperature control that belongs with the thermal group; **D-11** (garden) is an outdoor item in an interior-wayfinding category — all **[H]**.

### 1.6 CONSOLIDATION — two dead manifests
**[C]** **Neither of the two consolidation plans on record was executed against the DB or Part 4 files:**
- **`consolidation-manifest-2026-05-05.md` (88→65, −23 items):** header says "SQLite COMPLETE. Part 4 file modifications PENDING"; **every item it marks STRIKE is still `active`** (A-06/07/09/11/12/13/14/17, B-03/06/07/08/11, C-05/06, D-05/09, E-02/04, F-03/06).
- **CO-0003/D2 partial merges** recorded only as markers in `part04-item-index.md` (B-04 "[MERGED INTO B-03]", C-06 "[MERGED INTO C-03]", A-17 "[ABSORBED INTO G-02]", F-05 "[CONTENT MOVED TO G-08]") — **also unexecuted**; all four still active.

So there are **two conflicting, both-unexecuted consolidation plans**, and the item-index carries "merged"/"absorbed" labels for items that still exist — a live correctness hazard for any generator that reads those markers. **Owner ruling needed:** execute one plan, or formally retire both. Category A (19 items, largest) and Category G (most heterogeneous) are the primary split/merge candidates either way **[H]**.

---

## §2 · Specifications

### 2.1 Five overlapping spec stores; the JSON is orphaned and mis-mapped
**[C]** There are **five** stores, not one:

| Store | Rows / coverage | Taxonomy | Verdict |
|---|---|---|---|
| **Part 4 prose** (`parts/…/part04.md`) | 93 items | current | **CANONICAL / maintained** |
| `jurisdictional_values` (DB) | **109 rows / 20 items** | **current** | live per-jurisdiction values |
| `spec_value_probes` (DB) | **31 rows / 4 items** (A-02, A-08, A-18, B-01) | current | live PMP empirical-ceiling walks |
| `source_value_extractions` (DB) | **8 rows / 1 slug** (RT60 pilot → A-18) | current | live but pilot-only |
| `specification-database.json` | 73 records | **STALE Apr-2026, 100% uncurated** | **RETIRE (see 2.4)** |

Verified counts: `conflicts`=0, `jurisdictional_values`=109, `spec_value_probes`=31, `source_value_extractions`=8. **No `specification` DB table exists** — yet Template 1 (Spec Page) in `navigation-modes.md` §4 queries `FROM specification`. This is the spec-side analogue of the phantom-`room` bug.

### 2.2 The JSON's `item_code` silently points at the wrong items **[C — verified]**
The "19 items covered" figure is **illusory**. Spot-verified this session: JSON record `item_code="F-07"` carries `parameter="visual_alarm_flash_rate"` with a `summary` about "2440 mm corridors", while the **real F-07 is "Thermal Zoning"**. All 73 records are `curation_status="automated"`; the `_meta` note itself says item_code assignment is "pending ISW validation." The JSON cannot be trusted for item mapping. By contrast the DB `jurisdictional_values` uses the current taxonomy correctly (and even *fixes* JSON errors — the 50 m rest-seating interval the JSON misfiled under I-02 is correctly under E-10 in the DB).

### 2.3 MISSING specs
**[C]** The 74 "uncovered" items are mostly a **JSON-staleness artifact, not a prose gap** — spot-checks (A-02, C-04, F-01, A-16, E-05/06) all have fully quantified prose specs. The real, queryable structured gap: **only 24 of 93 items have any structured value in a live store; 69 rely on prose alone.**

Genuine **qualitative-only items where research would support a number [C]:**
- **F-02 Olfactory Control** — binary prose; could inherit a TVOC/ppb threshold (cf. F-06's `TVOC ≤0.5 mg/m³`).
- **A-13 No Sound Masking** — a prohibition; its own cross-refs cite quantified neighbours (RT60 ≤0.3 s, ≤35 dBA, STI ≥0.60) never stated as its specs.
- **D-09 Consistent Furniture Layout** — no dimensional spec.
- The **entire F-series OFS/PAIN** carries a standing disclosure that *"zero built-environment spatial parameters exist in any jurisdiction"* — qualitative by evidence necessity, not omission.

Best-evidenced item absent from the JSON: **A-18 RT60** (Tier 1, Iglehart 2020 `REF-00325`, PMP strict-termination PASS) exists only in the DB substrate + prose.

### 2.4 CONSOLIDATION — retire the JSON, do not regenerate in place **[C, HIGH]**
Internal duplicates inside the JSON: turning-circle 1500 mm ×4 (SPEC-0001/0024/0030/0053), corridor width 1200 mm ×3, grab-bar height ×2, illuminance 200–500 lux ×2. Garbage: SPEC-0018 `8,725,382 N`, 8 `parameter="unclassified"`, SPEC-0015 `illuminance = 30%`, 7 `[UNASSIGNED]` + 4 `[CROSS-CUTTING]` never mapped. **Recommendation:** harvest the few not-yet-migrated numeric values into the DB, then archive the JSON; regenerating it as-is would re-import the broken taxonomy. Also **[C]**: `specification-database-schema.md` documents 21 fields / "143 records / batch 1"; the JSON carries 44 fields / 73 records / "batch 2" — the schema doc is badly out of date and `schemas/specification.py`'s pydantic rules would reject the live JSON.

### 2.5 Conflict data is a fourth fragmentation axis **[C]**
The DB `conflicts` table is **empty (0 rows)**, yet `references/conflict-matrices/` holds **13 populated markdown matrices** (ACOUSTIC-LVL, COLOUR-CONT, TEMP-RANGE…) and the JSON references 7 `conflict_domains`. Conflict resolution — which is where much of the *consolidation logic across overlapping specs* actually lives (e.g. ACOUSTIC-LVL resolves the RT60/masking/SFA overlaps across A-02/A-08/A-13/A-18) — is stranded in prose, not queryable. Template 4 (Conflict Page) has nothing to render.

---

## §3 · Rooms

### 3.1 Three disagreeing room stores; the site is generated from a *wrong* matrix
**[C]** Room data lives in three places that disagree: Part 6/7 v9 prose, `scripts/db/seed_room_items.py`, and `site/rooms/*.html` (site generated from the seed). The 9 residential rooms map 1:1 to Part 6; the 8 non-residential (R-REC/COR/MTG/OFC/ASM/CAN/CHW/WC) are cross-typology inventions with no Part-7 room source.

**The serious finding [C]:** the seed matrices do **not match Part 6 prose** — they are *wrong*, not merely thin. R-BA: Part 6 prose lists turning-circle-first (G-01), anti-scald (I-03), lever taps (I-02), heated floor (TC-05), mirror (G-07), visual alarm (B-10); the seed (`seed_room_items.py:18–29`) shares **only G-03/G-04/C-04** and is polluted with **bedroom items** (G-09 emergency call, H-05 nurse-call). Same pattern at R-BED. Downstream, `site/rooms/r_ba.html` shows an empty criticality note and **titles corrupted with population codes** ("A-09 → PAIN", "F-07 → DEAF"). Reader (Part 6) and site are two different documents. Prose also uses `TC-01/02/05` codes the schema rejects (`schemas/room.py:33` enforces `^[A-K]-\d{2}$`), so the seed silently dropped every thermal item. And per `consolidation-sweep-2026-07-12.md` finding 8b, the `room`/`room_item` tables the seed writes **don't exist in the live DB** — so this matrix likely never lands anyway.

### 3.2 MISSING room — the sensory / quiet room **[C, HIGH]**
The single strongest room gap: **A-16 "Sensory Room / Quiet Room Provision (≥8 m²)"** is the most-mandated non-residential accessible space (required across NR-EDU/HLT/WRK/CUL — `part07_v9:35,44,74,85,112,121,180`; dedicated research `sensory-room-user-control` BPC), yet there is **no `r_sen`/quiet-room slug** in the 17. Secondary **[H]**: outdoor/garden/balcony/terrace (secure dementia loop is "normative best practice", `ALL-ROOMS.md:463`) has no room home either.

### 3.3 Matrix completeness — thin *and* wrong **[C]**
R-BA (wrong, per 3.1); R-BED (missing hoist — a Part-6 DAR ceiling-blocking provision — plus thermal/acoustic/visual-alarm); R-STA, R-GAR (3 items), R-LAU, R-CAN all suspiciously thin. **No room seeds any DAR provision, conflict register, criticality note, or schematic checklist** (the seed only writes `room_item`), so those `schemas/room.py` fields render empty on the site. Data-quality bug: bathroom item **I-03 is mis-assigned to corridors** R-HAL/R-COR (`seed:89,127`).

### 3.4 CONSOLIDATION **[C/H]**
- **R-HAL (residential hallway) vs R-COR (non-residential corridor)** — the same "circulation" concept split only by building type; R-HAL items are a near-subset of R-COR. Merge to one Circulation space with a res/non-res column. **[C]**
- **R-BA vs R-WC** — residential bathroom and non-residential accessible WC are the "same room" duplicated across building types (both share G-03/G-04/E-07). **[C]** — the same res↔non-res duplication as hallway/corridor. Both are symptoms the two-axis model (§0) dissolves: one *space*, two *typology* contexts.

---

## §4 · Building typologies (Part 7)

### 4.1 Scope and status
**[C]** The live Part 7 (`parts/v10/part07.md:10`) is a **STUB** ("renders from item_population links at Phase E"); the authored 7-typology prose survives only in `parts/88_to_90/part07_v9-0…`. So the model is documented but **currently unbuilt in shipping data.** The 7: NR-EDU, NR-HLT, NR-WRK, NR-RET, NR-CUL, NR-HOS, NR-TRP.

### 4.2 MISSING typology — NR-CARE (residential-institutional / dementia-village care) **[C, HIGH]**
The largest evidence-vs-taxonomy mismatch in the whole model. The project's **deepest** evidence base points here: 5 dedicated dementia *care-facility* case studies (De Hogeweyk, Village Landais, Carpe Diem, Il Paese Ritrovato, Verbeek — all tagged `building_type | Residential (care facility)` in `case-study-compendium.md`), the single most-covered population (DEM), and dedicated care-thermal/wayfinding-dementia research. Yet these institutional care buildings are filed under **"Residential"** in the compendium while Part 7 routes dementia through **NR-HLT (clinical/acute)** — neither home is right (a 152-resident village is not a dwelling; long-stay domestic-scale care is not acute healthcare). Worked Example 5 ("Supported Housing — Mixed Needs") confirms the project treats this as first-class elsewhere with no Part-7 home. **Candidate: create NR-CARE**, sitting on the residential↔healthcare boundary — which the two-axis model (§0) accommodates naturally.

Negative cases (evaluated, **not** missing) **[C]**: civic/justice (0 research files; folds into retail/transport per the project's own LPA-BT-01/BAR-BT-02 "Public Buildings" bundle); faith/worship (a coherent NR-CUL sub-type row, no independent evidence); childcare (already a distinct matrix CHD-BT-03, but in the Supplementary volume). **Partial [H]:** sport/leisure/aquatic is real but thin (item A-10b hydrotherapy exists; no dedicated research or case study) — best as an explicit **leisure/aquatic sub-block promoted out of NR-HOS**, not a standalone typology.

### 4.3 CONSOLIDATION — split NR-HOS; keep the rest **[C/H]**
- **NR-HOS is over-broad — split [C]:** it bundles hotels (explicitly "temporary residential", routed to Part 5), restaurants (retail-like, overlaps NR-RET café row), conference (assembly, overlaps NR-CUL/WRK), and leisure/pool (the orphaned aquatic block). Its own sub-types point at three other typologies.
- **NR-CUL is broad but coherent — do NOT split [H]:** museums/libraries/theatres/galleries/worship share the defining requirement spine (assembly acoustics + hearing loop/CART + audio description + sensory transition).
- **No merges among EDU/HLT/WRK/RET/TRP** — each has a distinct primary-population profile and signature items.

### 4.4 Coverage inversion — the taxonomy's evidence weight is inverted at both ends **[C]**
**NR-RET, NR-CUL, NR-HOS, NR-TRP have ZERO case studies and no setting-specific research** — headings with universal-item cross-references but no independent evidence base. Meanwhile the project's *deepest* evidence (5 dementia-care case studies + dominant DEM research) supports **NR-CARE, which doesn't exist**. For a website that surfaces evidence confidence per page, this inversion means four typology landing pages would render as confident headings with nothing behind them.

---

## §5 · Missing techniques (research-driven "what are we missing" at the item level)

These are design provisions our research supports that **no item covers** — the item-level answer to "what are we missing." Ranked by research support × accessibility impact. Several are **self-flagged in the corpus's own gap registers** (`references/connections/cross-domain-gap-analysis-2026-04-09.md` GAPs A–H; the FDR "New item" registers in the pain-ofs and mental-health BPCs).

**CONFIRMED — clear research value, no item home:**

| # | Missing item | Populations | Evidence | Nearest existing (why insufficient) |
|---|---|---|---|---|
| 1 | **Accessible fire-evacuation refuge** (seating + two-way comms incl. DBL + wayfinding-to-refuge) | MOB, OFS, PAIN, DEAF, DBL | Self-flagged **GAP-C CONFIRMED** (verified verbatim, `cross-domain-gap-analysis:77–82`); CAN/ASC 2.2, ITU V.18 | None — refuge exists only as Part 8 SE structural enclosure; no accessibility spec. **Safety-critical.** |
| 2 | **Supine / recumbent recovery space** (OFS/ME-PEM lie-down) | OFS, PAIN | Self-flagged **GAP-OFS-RECUMBENT-01**; CDC/NICE NG206/Bateman-Horne (Tier 2) | A-16 is seated sensory regulation, not horizontal PEM recovery; no surface/duration spec anywhere |
| 3 | **DeafSpace circulation geometry** (≥2440 mm signing-pair corridor; movable armless furniture) | DEAF, DBL | DSDG/Gallaudet (Co-1/Tier 2); closes the "DEAF structurally invisible" gap (`bpc-audit-pass0 §S6.1`) | E-08 (1200 mm) is mobility-derived; D-09 is the *opposite* (fixed furniture). Caveat: zone vs NDV/DEM enclosure conflict |
| 4 | **Audio wayfinding / beaconing** for VIS at entries & lift call points | VIS | RNIB (Tier 2) + crossings Tier 6 | E-09 TWSI (tactile) + K-02 tactile map (static) give no dynamic audio orientation |
| 5 | **MH de-escalation / safe-retreat room** (distinct from A-16: exit-sightline-from-inside, staff monitoring, ≥9 m²) | NDV/MH, PTSD | Tier 1 ward evidence (van der Schaaf 2013 n=23,868; Faerden 2022) — BPC explicitly rules out combining with A-16 | A-16/D-05 — corpus states a single quiet room "fails MH users **and** NDV users" |
| 6 | **Female-only / single-gender area** in mixed MH inpatient settings | NDV/MH, trauma | Self-flagged GAP (Tier 3/Co-1: Rodríguez-Labajos 2024, Wilson 2023) | None |
| 7 | **Emergency photoluminescent wayfinding** (ISO 16069) / low-level exit guidance under degraded conditions | VIS, DEM | Self-flagged **GAP-D CONFIRMED** | No D-series item; LRV/colour signage fails under smoke/power-loss |
| 8 | **Fire-door electromagnetic hold-open** (release on alarm) | DEM, DEAF | Self-flagged **GAP-B CONFIRMED** (Marquardt 2011) | None — closed fire doors break DEM spatial continuity & DEAF sightlines |
| 9 | **Biophilic interior nature-views / indoor vegetation** | NDV, DEM, NEU, OFS, MH | Tier 3 SR (Al Khatib 2024, 61 sources) — strongest raw evidence | B-09 (daylight only), D-11 (DEM garden) don't capture interior views/planting; voluntary-standard caveat |

**HYPOTHESIS (thinner corpus, or better as a spec-note than a new item):** seated service-point option for OFS/POTS (→ G-06 note); acoustic-privacy STC for therapy/de-escalation rooms (GAP-H, research owed); anti-fatigue resilient flooring for PAIN (Tier 4, "novel"); property-boundary demarcation for DEM wandering (Tier 2, "novel"); prospect-refuge nooks (Tier 2, but `theory-gap-analysis §5.4` argues *against* the framework — tension to resolve); bidet rough-in; touchless-interface accessibility (GAP-E, but "zero coverage — no BPC yet", so a *research* gap, not yet itemisable); anti-ligature (single thin mention — needs a dedicated BPC first).

**Deliberately homeless (not oversights) [C]:** supplementary-population specs (CHD children, LPA short-stature, EXH extreme-height, BAR bariatric) have concrete values in `body-sizes-supplementary-populations.md` but are **scoped to the Supplementary Volume by `project-standards`** — surface only if the owner wants to reconsider that scope.

**INVERSE — items with weak/contradicted evidence (re-spec, not demote) [C]:**
- **A-09** HVAC vibration "0.1 m/s RMS" — *not in ISO*; "UNVERIFIED flag must appear before publication" (`spec-db-part4-reconciliation §C1`); no disability-specific floor-vibration standard exists. Strongest flag candidate.
- **A-02** NRC ≥0.85 — criterion contradicted (Amlani & Russo 2016: NRC-compliant panels can *reduce* STI); STI ≥0.60 should be the performance criterion, NRC a procurement proxy.
- **B-01** circadian ≥150 EML — *under*-calibrated; research supports ≥250 melanopic EDI (Brown 2022). A strengthening fix, not weak-basis.
(No item is evidence-free — 100% have ≥1 BPC mapping — so these are threshold problems, not empty items.)

---

## §6 · Consolidation register (the "what should we consolidate" answer)

| # | Consolidation | Axis | Action | Conf |
|---|---|---|---|---|
| CR-1 | **Two dead consolidation manifests** (88→65 and CO-0003/D2) — DB still holds every struck item; index carries false "MERGED" labels | Categories | Execute one, or formally retire both; strip stale merge markers | **[C]** |
| CR-2 | **Retire `specification-database.json`** — wrong item_codes, garbage, superseded by DB tables | Specs | Harvest residual values → DB; archive JSON; update schema doc | **[C]** |
| CR-3 | **Adopt part-file/TOC category names as canonical**; correct/delete `part04-item-index.md` Category Summary; add K to TOC; delete stale `part05-j` duplicate | Categories | One reconciling naming pass | **[C]** |
| CR-4 | **Fold thermal into one category** (F-04, F-07, F-08, K-05, Appendix-C TC-items) | Categories | New Thermal/Env-Comfort category (§1.4) | **[C]** |
| CR-5 | **I-03 ↔ G-03 grab-bar duplication**; A-16 vs D-05 vs (new MH room) sensory-space family | Specs/Categories | De-dup grab bars; clarify the three distinct "quiet space" types | **[C]** |
| CR-6 | **R-HAL/R-COR** and **R-BA/R-WC** are res↔non-res duplications of one space | Rooms | Collapse under the two-axis model (§0) | **[C]** |
| CR-7 | **Split NR-HOS**; promote leisure/aquatic to a sub-block | Typologies | Re-home hotel→residential, restaurant→NR-RET, conference→assembly | **[C]** |
| CR-8 | **Consolidate the four spec/conflict stores** onto the DB (`jurisdictional_values` + a real `specification` + `conflicts` table); populate `conflicts` from the 13 markdown matrices | Specs | Build the missing DB tables the site templates already assume | **[H]** |

---

## §7 · Website-build implications & prioritized path

The four axes are the site's navigation spine, and three of them cannot currently render cleanly:

1. **`/rooms` is the named blocking gap** (`website-v0-path-forward` §"NOT done"). Do not build `room_page.py` against invented flat rooms. **Resolve the two-axis model (§0) first**, then seed a room×typology matrix *from Part 6/7 prose* (not the current wrong seed). Fix the population-code title corruption and empty criticality notes before any regeneration. Until then, `site/rooms/*.html` should be treated as dead output, per that doc's step 4.
2. **`/specs` category filter + Master Index (Template 6) need one canonical name per letter** — ship CR-3 before the filter. The A–K letters are safe; the *names* are not.
3. **Template 1 (Spec Page) queries a non-existent `specification` table** and Template 4 (Conflict Page) a 0-row `conflicts` table — CR-2/CR-8 are prerequisites for those two page types, exactly as population/spec-page generators were rebuilt against the real schema in July.
4. **Evidence-confidence rendering will expose the coverage inversion (§4.4):** four typology pages and 69 prose-only items would render as confident headings with no queryable backing. This is consistent with the mission's honesty posture (`navigation-modes.md §6` ethics rules; `next-steps-synthesis` "ship the map, not false authority") — the site should surface these as *thin*, not hide them.

**Suggested sequencing (all owner-gated; none executed here):**
- **P0 (unblocks the site, low-risk, high-clarity):** CR-3 (category names) · CR-2 (retire JSON) · resolve §0 two-axis model as a Decision Record.
- **P1 (structural):** CR-1 (pick one item-consolidation plan) · CR-4 (thermal category) · CR-6 (room de-dup under two-axis) · seed the room×typology matrix from prose.
- **P2 (new content, needs research/synthesis + external review per project posture):** the §5 missing items — starting with the **safety-critical refuge area (#1)** and the two self-flagged, evidence-backed OFS/MH items (#2, #5/#6) · NR-CARE typology (§4.2) · CR-7 (split NR-HOS) · CR-8 (conflict-store consolidation).

**Standing caveat:** every §5 new item and every re-spec in the INVERSE list is a *solo-adjudicated determination* until external review returns — hold behind the PROVISIONAL banner per `workplan/next-steps-synthesis-2026-07-14.md`. This audit surfaces the gaps and consolidation candidates; it does not settle any value.

---

## Provenance & confidence

Method: five parallel general-purpose investigation passes, each instructed to ground every claim in file+line or DB query and to separate CONFIRMED from HYPOTHESIS. The five highest-stakes claims were re-verified directly this session: (a) JSON `F-07` = visual-alarm content while DB F-07 = Thermal Zoning **✓**; (b) K-05 = thermal item under K=Deafblind **✓**; (c) I-03/G-03 grab-bar duplication **✓**; (d) GAP-C refuge-area text verbatim **✓**; (e) `conflicts`=0 / `jurisdictional_values`=109 / `spec_value_probes`=31 / `source_value_extractions`=8 **✓**. Where an agent's brief contained a mis-stated premise (e.g. "source_value_extractions is empty"), the pass corrected it against live data and the correction is carried above. Rooms and typology passes reached the two-axis finding (§0) **independently**, which raises confidence in it.

Nothing in this audit modifies the taxonomy, the data, or any item. It is an analysis deliverable: a map of what the research says we are missing and what the syntheses say we should consolidate, for owner ruling and scoped Change Orders.
