# R1 — Stage assignment: all 66 tables derived to a namespace, disputes resolved

**Adversarial audit, 2026-08-27, lens: stage assignment.** Read-only; every figure below is
derived from `data/guidebook.db` (`user_version` 64) or bound to file:line. Census command,
stated once and reused throughout:

```python
import sqlite3
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
# tables: SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'
# rows:   SELECT COUNT(*) FROM '<t>' per table
# FKs:    PRAGMA foreign_key_list('<t>') per table
```

**Convention.** 66 = tables in `sqlite_master` of `type='table'` excluding `sqlite_%`. Measured:
**66 exactly**. "Inbound FK edges" counts FK *edges* (one child column set → one parent), not
distinct child tables. Row counts are live at audit time. The test applied to every table is
STAGE-TABLE-MAP's own: **whose own work does this record?** — never what it keys on, never who
reads it.

---

## 0. The frame correction that governs everything below

**The architecture note is NOT wholly governing, and RENAME-MAP §2's "The note wins on rule 0"
is refuted for half its own table.** The operative record is
`references/project-standards.md`, which carries the owner's *subsequent* contact on the note:

- Items **#1 and #2 adopted** as owner rulings (`project-standards.md:1836-1870` and
  `:1874-1922`): evidence→judgment is 1:N; the evidence item is the SOURCE, the judgment item
  is the extracted/tiered/categorised value.
- Items **#3 and #4 explicitly NOT adopted** (`project-standards.md:1911-1914`): *"`base.clues`
  is not moved to substrate, and the `~825` reconciliation is not pursued."*
- The owner on the note's status (`project-standards.md:1843-1845`): *"not complete, and not
  definitive — just a thought document."*

Rule 0 says a **live owner statement** supersedes prior records on contact. The adoption
contact is *later* than the note's transcription and *narrower* than the note; it is the live
statement. Executing the rename against the note as-written would therefore move
`source_locators` into substrate **against an explicit owner non-adoption** — see §1.1.

**Mid-audit rulings received via the coordinator, incorporated as owner statements:**

1. `base_building` is **three** tables — `base_building_types` (new), `base_room_types`
   (← `rooms`), `base_elements` (new). `items` is **not** any of them; the 2026-08-26 ruling
   (`items` = Part-4 render rollup, `project-standards.md:1311-1322`) stands unamended.
2. Separator is **underscore** (`base_models`, not `base.models`) — RENAME-MAP C-3 is closed.
3. The four taxonomies keep **parallel names**: `base_taxonomy_medical` / `base_taxonomy_identity`
   (← `populations`) / `base_taxonomy_icf` (← `axes`) / `base_taxonomy_needs`
   (← `access_needs`). This **supersedes the §R8 name `icf_demands`** and bars folding any
   taxonomy into another — which also closes RENAME-MAP C-2.

---

## 1. The four disputes, resolved

### 1.1 `source_locators` → **RESEARCH** (the research hand-off). The note loses.

**Winner: map 1 (STAGE-TABLE-MAP) and map 2's stage (research), against the note's
`base.clues`.**

Evidence, in force order:

1. **The owner did not adopt it.** `project-standards.md:1911`: *"Items #3 and #4 of the
   architecture note are NOT adopted — owner instruction, same contact. `base.clues` is not
   moved to substrate."* That is a live owner instruction about exactly this table.
2. **The wall is ratified and physically present.** The clue-store demotion — *"nothing joins
   it, no determination may cite it"* (`project-standards.md:931`, re-quoted at `:1753` citing
   DR-2026-08-06) — is measured true: `source_locators` has **0 inbound and 0 outbound FK
   edges** (census above). Substrate is by definition *"the layer all stages point into"*
   (`CLAUDE.md`, pipeline section); a substrate table nothing may join is a contradiction in
   terms. Re-homing it to base would reverse a ratified DR with no supersession recorded — the
   exact defect the A3 audit already flagged for the `evi_items.research_item_id` key
   (`project-standards.md:1752-1754`).
3. **By the test.** Whose work is a row of 875 leads? Research's — *"a lead: what to go and
   get"* is the ruled definition of the research item (`project-standards.md`, six-stage spine
   table). With item #2 adopted (evidence item = the source), research's hand-off object is the
   lead, and `source_locators` is the only occupant.

**What breaks if the note is chosen:** the DR-2026-08-06 wall reverses silently; every future
citation walk gains the clue store as a legal join target while 251 of its DOI rows carry no
title/authors (architecture-note transcription, measurement table) — unverified identifiers
become substrate that determinations may point at. That is the 2026-08-19 fabrication surface
reopened at the schema level.

### 1.2 `source_value_extractions` → **JUDGMENT**. The note wins — and it is already ruled.

**Winner: the note, ratified as an owner ruling adopting item #2**
(`project-standards.md:1874-1922`): *"`source_value_extractions` is a JUDGMENT table, not an
evidence-collection table. The value is derived at judgment; collection logs what was found."*

Corroborating measurements:

- The 1:N hand-off ruled in item #1 is **already in this table's DDL**: `ref_id` NOT NULL, FK
  → `evidence_sources(ref_id)`, no UNIQUE on the table (`project-standards.md:1847-1859`,
  re-verified in census: 1 inbound edge on SVE, from `extraction_population_links`). The
  judgment hand-off key exists and has all along.
- The machine has **half caught up**: `governance/pipeline-contract.yaml:59-76` restates
  judgment's entry at the ruled grain (comment dated 2026-08-27), but
  `tools/pipeline_completeness.py:37` still runs five stages and its
  `F["judgment"]` block (`:150-164`) counts `value_extractions` **beside `specifications`
  cells** — i.e. it counts SVE in judgment for the *old* reason (judgment-writes-specs), which
  is coincidentally the right stage under the new frame. `F["evidence-collection"]` (`:135-144`)
  no longer touches SVE. So the completeness gate is accidentally right on this table and
  structurally wrong on the spine.

**What breaks if evidence is chosen:** the owner's quoted definition of judgment —
*"determines category of judgment item, derives value/process/figure/goal"* — becomes a
collection act; the aporia ruling (`project-standards.md:1993-2041`, harvest at evidence /
adjudicate at judgment) loses its adjudication table; and `judgment_items` reverts to "a new
table owed a design", which the ledger explicitly refutes (*"Forty-nine columns prefigure
it"*, `:1859`).

### 1.3 `evidence_sources` → **EVIDENCE, the hand-off object itself**. The note wins.

**Winner: the note, ratified via the same item-#2 adoption** (`project-standards.md:1883-1886`):
the evidence item is *"the source — one row per document, carrying the reference ID and
identifiers"*, table `evidence_sources`. NOMENCLATURE Part E's "`evi_sources` — a satellite,
not the hand-off" is superseded.

Corroborating measurements:

- **13 inbound FK edges** land on `evidence_sources` (census; matches the ledger's figure at
  `:1890`) — more than any table except `items` (14). Seven of them are cross-stage under the
  six-stage frame (`CLAUDE.md`, pipeline section: `evidence_sources.ref_id` 7). A "satellite"
  with the densest hand-off key in the schema was always a misreading.
- The ruled judgment hand-off (`SVE.ref_id → evidence_sources.ref_id`) *presupposes* that
  `evidence_sources` is the evidence item — the key cannot land on a satellite.

**What breaks if Part E is chosen:** with SVE moved to judgment (1.2), the evidence stage would
have **no hand-off object at all** — a stage whose output is nothing. And the rename cost is
real and already measured: renaming `evidence_sources` touches 13 FK edges and 8 hardcodes in
the blocking `migration_reproducibility` gate (`:1890-1891`); the ruling says explicitly that
the rename is *"separate, later, and expensive."* Keep the name; the assignment is the point.

### 1.4 `items` → **RENDER** (Part-4 rollup, name retired). Settled by owner ruling, mid-audit.

The coordinator relayed the ruling: `base_building` holds building types / room types /
construction elements at three levels, and only the middle level exists (`rooms`, 17 rows).
`items` (93 rows) holds **design provisions about elements** — e.g. A-03 "Acoustic Door
(STC ≥35) at All Sensitive Space Boundaries" — which is none of the three levels. So:

- The 2026-08-26 ruling stands: *"`items` is demoted from identity to rollup … derived from
  specifications rather than keyed by them"* (`project-standards.md:1318-1321`), and the
  2026-08-27 `-item` ruling retires the *name* (`:1584-1585`).
- RENAME-MAP **C-1 is closed**: the note never reached `items`, and `base_building` names new
  tables, not a re-homing.

**The conflation question, answered because it was asked:** an `items` name string conflates
**element** (door) + **parameter** (STC) + **determination** (≥35). This does not change where
`items` belongs — it is *why* it belongs in render and nowhere else. Each component has a ruled
home, and two of the three homes do not exist yet:

| component | ruled home | exists? |
|---|---|---|
| element (door) | `base_elements` — this ruling | **no table** |
| parameter (STC) | the canonical-parameter vocabulary P1.0 already **requires** (`project-standards.md:1363-1365`: *"A canonical-parameter vocabulary lands in or before that migration — the key may not be unconstrained free text"*) | **no table, no CHECK, no writer** (`:1344-1346`) |
| determination (≥35) | `specifications` rows | table exists, **0 rows** |

Two consequences worth stating:

1. The 93 names are the best existing *seed* for the parameter vocabulary P1.0 needs — but the
   42 embedded determinations (the instrument's floor,
   `DR-2026-08-19-research-restart-operative-instrument.md:127`) must **never** be parsed into
   `specifications`: they are determinations with no judgment behind them, the E-08 defect
   class.
2. **MAJOR:** 14 inbound FK edges land on `items.item_code` (census), including the three big
   crossing maps — `item_population_links` 372, `item_axis_links` 158, `term_item_links` 147
   (677 substrate rows). Substrate is now keyed on a **render aggregate**. Under the split,
   those junctions' natural parent is `base_elements` or the parameter vocabulary; re-pointing
   them belongs in the same design as the split, or the crossing maps inherit the conflation.

---

## 2. The three assignments STAGE-TABLE-MAP declared arguable

1. **`jurisdictional_values` → research: SURVIVES.** 109 rows, `value_text`/`value_numeric`
   both 0 non-null by the REFERENCE-ONLY ruling (STAGE-TABLE-MAP; re-checkable:
   `SELECT COUNT(value_text), COUNT(value_numeric) FROM jurisdictional_values`). It carries no
   `ref_id` (census: only FK is `items.item_code`) — it is pre-admission by construction, a
   lead index like `source_locators`. Under the adopted frame, a code document *found* becomes
   an evidence item on admission, and its clause values become judgment items — SVE already
   carries the same 15-column `loc_*` apparatus this table duplicates (DDL, census). The
   REFERENCE-ONLY ruling is the only thing keeping it research; **condition: if anyone ever
   fills its value columns, it becomes a second judgment home and a rule-5 violation.** Its
   `item_code` NOT NULL key now points at a render rollup (1.4) — flagged for the re-point
   sweep, not a stage argument.
2. **`weighting_profile` → substrate: SURVIVES.** A 5-row registry of audience×use-pattern
   tier weights that synthesis reads; written as project configuration. The note's `base` has
   no member for it, but base ≠ only the note's members (the note is partial and non-definitive
   by the owner's own statement). Substrate by the write-test.
3. **`supersession_check` → evidence: DOES NOT SURVIVE. Re-assign to JUDGMENT.**
   STAGE-TABLE-MAP's argument — "literature currency, not judgment staleness" — was drawn when
   judgment meant "writes specifications". Under the adopted frame, judgment *"delivers a
   verdict on an evidence item"* (owner, note verbatim), and this table's DDL is a verdict on
   an evidence item by construction: `ref_id` NOT NULL → `evidence_sources`, outcome CHECK
   (`current_best` / `superseded_by` / `refined_by` / `divergent_no_supersession` /
   `co1_addition_logged`), and — decisively — **`anchor_tier INTEGER NOT NULL CHECK(1..6)`**,
   the tier verdict the ruling names as judgment's output
   (`project-standards.md:1903-1905`: the tier move off `evidence_sources` is queued for the
   same reason). Determining supersession is comparative adjudication, not the *"cursory
   scans"* the owner assigns to evidence (`:1998-2001`). 0 rows, so the re-assignment is free
   today.

---

## 3. What nobody asked: tables with no home, and tables with two

**No defensible home under the note's namespaces (4):**

- `decisions` (166), `data_migrations` (352), `pipeline_runs` (1) — registries of the
  **project's own acts**. Every `base` member in the note is domain vocabulary (models,
  buildings, topics, taxonomies, clues, sources, languages); none is a governance ledger. They
  are assigned substrate below **by convention, not by the note**, and the convention should be
  stated wherever the map is quoted — the alternative (a declared `meta`/`ops` namespace) is a
  naming decision the owner has not been asked for. `pipeline_runs` is additionally
  single-purpose (a DOI-resolution batch tracker, per its phase-column DDL), not a general
  pipeline registry; its name will mislead under a six-stage "pipeline" vocabulary.
- `item_population_elaborations` (0 rows) — **homeless twice over.** It stores
  `spec_variant_a`/`spec_variant_b` per (item × population) with an `evidence_ref_id` — i.e.
  determination-grade content at the exact grain **both** halves of which were dropped from
  `specifications`' identity by the 2026-08-25/26 rulings, and it points from substrate into
  evidence (census: FKs to `items`, `populations`, `evidence_sources`), which Part E already
  flagged as *"inverting the substrate model."* No stage may own it: as substrate it violates
  the pointer direction; as specification it presupposes the superseded grain. **Delete
  candidate** (0 rows, evidence of vacuity recordable in the commit per §1 symmetry).

**Claimed by two stages (4), each resolved:**

- `rooms` — render (map 1) vs `base_room_types` (mid-audit ruling). **Base wins, now by
  ruling**; the rows are a hand-authored typology vocabulary, and the render surface is the
  *page*, which is a file, not this table.
- `gaps` (5) — assigned research by map 1, but **3 inbound FK edges** arrive from three
  different stages (census: `gap_mining` research, `evidence_population_match` judgment,
  `specifications` specification), and its category CHECK spans `CONF`/`DEC`/`AUDT`. Any stage
  discovering a gap writes here. Kept in **research** below (a gap's primary producer, and "a
  gap is a first-class finding" is research doctrine), but it is honestly a cross-stage
  registry; if the registries ever get a namespace, `gaps` belongs in it.
- `citation_mining` (10) — writes research output (harvested DOIs) while keyed on an admitted
  anchor (`evidence_sources.ref_id`). **Research** by the write-test; the backward FK is
  re-entrancy (`governance/pipeline-map.yaml`, 2026-08-21: layers are re-entered), not
  membership.
- `jurisdictional_values` — research/judgment tension per §2.1; research while REFERENCE-ONLY
  holds.

**Marginal:** `item_audit_runs` (0 rows) is a workflow tracker (`steps_complete`, `brief_path`,
status machine) keyed on the now-demoted `items` grain — closer kin to `pipeline_runs` than to
any verdict table. Assigned judgment below (both prior maps' choice) but flagged: it records a
project act about a render aggregate, and is a delete candidate on the same §1 evidence basis.

---

## 4. THE DELIVERABLE — all 66 tables, one namespace each

Namespaces per the mid-audit separator ruling: `base` · `research` · `evidence` · `judgment` ·
`synthesis` · `specification` · `render`. Ruled target names are given where a ruling exists;
`—` means naming is out of this lens's scope. Flags: ▲ = stage changed vs STAGE-TABLE-MAP
(08-25) · ⚑ = see §2/§3 caveat.

### BASE — 23 tables, 4,046 rows

| table | rows | ruled/derived target name | note |
|---|---:|---|---|
| `slugs` | 106 | `base_topics` (note; flat — owner wants parent columns, `:100-102` of the note) | |
| `rooms` | 17 | **`base_room_types`** (ruled, mid-audit) | ▲ from render |
| `populations` | 23 | **`base_taxonomy_identity`** (ruled) | |
| `axes` | 17 | **`base_taxonomy_icf`** (ruled; supersedes `icf_demands`) | |
| `access_needs` | 17 | **`base_taxonomy_needs`** (ruled) | |
| `terms` | 88 | `base_multilingual` family | |
| `term_aliases` | 2,382 | 〃 | largest table in the repo |
| `access_need_icf` | 43 | — crossing map | |
| `access_need_axis_map` | 21 | — crossing map (P0.6 rename affected by taxonomy ruling) | |
| `item_axis_links` | 158 | — crossing map | ⚑ keyed on render rollup, §1.4 |
| `population_axis_map` | 53 | — crossing map | |
| `item_population_links` | 372 | — crossing map | ⚑ §1.4 re-point |
| `term_item_links` | 147 | — crossing map | ⚑ §1.4 re-point |
| `lang_jur_map` | 70 | — crossing map | |
| `access_duration` | 3 | — vocabulary | |
| `access_stakes` | 3 | — vocabulary | |
| `life_stage_modifiers` | 2 | — vocabulary | |
| `weighting_profile` | 5 | — registry | ⚑ §2.2, survives |
| `situations` | 0 | — | delete candidate (0 rows, no writer) |
| `decisions` | 166 | — project-act registry | ⚑ §3, no note home |
| `data_migrations` | 352 | — project-act registry | ⚑ §3 |
| `pipeline_runs` | 1 | — project-act registry | ⚑ §3, misleading name |
| `item_population_elaborations` | 0 | — | ⚑ §3, **homeless, delete candidate** |

### RESEARCH — 10 tables, 1,087 rows

| table | rows | note |
|---|---:|---|
| `source_locators` | 875 | **the research hand-off** — §1.1, note's `base.clues` NOT adopted |
| `jurisdictional_values` | 109 | ⚑ §2.1 — research only while REFERENCE-ONLY holds |
| `search_candidates` | 60 | |
| `search_executions` | 28 | |
| `citation_mining` | 10 | ⚑ §3 — re-entrant FK to evidence is not membership |
| `gaps` | 5 | ⚑ §3 — cross-stage registry in truth |
| `search_coverage` | 0 | |
| `search_languages` | 0 | |
| `gap_mining` | 0 | |
| `reference_stubs` | 0 | delete candidate (Part E concurs) |

### EVIDENCE — 6 tables, 67 rows

| table | rows | note |
|---|---:|---|
| `evidence_sources` | 10 | **the evidence hand-off object** — §1.3, ruled; name change separate/later/expensive |
| `evidence_source_authors` | 37 | satellite |
| `source_slug_links` | 10 | |
| `search_admissions` | 10 | the only keyed research→evidence edge; Part J's deletion premise refuted (`:1694-1698`) |
| `url_verification_runs` | 0 | |
| `external_root_registry` | 0 | root identity is a fact established at admission |

### JUDGMENT — 5 tables, 25 rows

| table | rows | note |
|---|---:|---|
| `source_value_extractions` | 0 | **the judgment item** — §1.2, ruled; hand-off key already in DDL | 
| `extraction_population_links` | 0 | follows it |
| `evidence_population_match` | 25 | ▲ from evidence — a grade is a verdict on an evidence item (Part E concurs; `:1899-1900` moot-note concurs) |
| `supersession_check` | 0 | ▲ from evidence — §2.3, verdict + `anchor_tier` in DDL |
| `item_audit_runs` | 0 | ⚑ §3 marginal; delete candidate |

### SYNTHESIS — 8 tables, 0 rows

| table | rows | note |
|---|---:|---|
| `bpc_metadata` | 0 | the synthesis item (PK `slug` = the ruled N:1 fan-in, `:1561-1563`) |
| `item_bpc_links` | 0 | must be re-keyed (references `items`, never `bpc_metadata`) |
| `connections` | 0 | |
| `connection_targets` | 0 | |
| `reasoning_doc_citations` | 0 | |
| `citation_population_links` | 0 | |
| `convergence_assessment` | 0 | ▲ from judgment (map 1) — weighing across judgments is synthesis |
| `conflicts` | 0 | ▲ from judgment — cross-population finding; Part E concurs, marked arguable there too |

### SPECIFICATION — 4 tables, 0 rows

| table | rows | note |
|---|---:|---|
| `specifications` | 0 | the determination; P1.0 re-keys on `parameter_canonical` |
| `specification_source_links` | 0 | |
| `spec_value_probes` | 0 | ▲ from judgment — the probe produces the number |
| `probe_population_links` | 0 | |

### RENDER — 10 tables, 93 rows

| table | rows | note |
|---|---:|---|
| `items` | 93 | ▲ from substrate — **Part-4 rollup, ruled 08-26, reconfirmed mid-audit; name retired** — §1.4 |
| `room_items` | 0 | composes room pages; re-point both ends (`rooms`→base, `items` retiring) |
| `case_studies` | 0 | |
| `case_study_outcomes` | 0 | |
| `case_study_populations` | 0 | |
| `case_study_specs` | 0 | FK lands on `items`, named for specifications — Part E's fault note stands |
| `case_study_strategies` | 0 | |
| `economics_entries` | 0 | |
| `economics_entry_populations` | 0 | |
| `economics_entry_specs` | 0 | same fault |

**Distribution (derived, not hand-written — sums recomputed from the census):**
base 23 / research 10 / evidence 6 / judgment 5 / synthesis 8 / specification 4 / render 10
= **66**. Rows: 4,046 / 1,087 / 67 / 25 / 0 / 0 / 93 = **5,318** — which reproduces the
ledger's independently-derived 5,318-row stage split (`project-standards.md:1824`), a
cross-check this map passes.

---

## 5. Findings, ranked

- **BLOCKER — R1-F1.** RENAME-MAP §2's operating premise, *"The note wins on rule 0"*, is
  wrong for two of its four rows. The owner adopted items #1–#2 only and explicitly did **not**
  adopt `base.clues`→substrate (`project-standards.md:1911`). A rename executed from
  RENAME-MAP's table as written moves `source_locators` against an owner instruction and
  reverses DR-2026-08-06 without a supersession. The rename plan must be re-derived from the
  adoption record (§4 above), not from the note.
- **MAJOR — R1-F2.** The machine disagrees with itself: `pipeline-contract.yaml:59-76` states
  judgment at the ruled grain (six-stage, item #2), while `tools/pipeline_completeness.py:37`
  runs `STAGES` of five and counts `value_extractions` inside a judgment block built on the
  superseded judgment-writes-specs model (`:150-164`), with `specifications` counted as
  judgment cells. The blocking `pipeline_completeness_fresh` gate is enforcing a spine two
  rulings old.
- **MAJOR — R1-F3.** 677 substrate crossing-map rows (`item_population_links` 372 +
  `item_axis_links` 158 + `term_item_links` 147) are keyed on `items.item_code` — now a
  render-stage aggregate slated for retirement. The three-way split ruling (§1.4) gives their
  natural parents (`base_elements`, the parameter vocabulary); the re-point must be designed
  with the split, not after it.
- **MAJOR — R1-F4.** `supersession_check.anchor_tier` (NOT NULL) and
  `jurisdictional_values.evidence_tier` (NOT NULL DEFAULT 6) both store tier verdicts outside
  judgment — the same defect class as the queued `evidence_sources.tier` move
  (`project-standards.md:1903-1908`), not yet on that queue. Grep evidence: DDL in census.
- **DEFECT — R1-F5.** `item_population_elaborations` has no defensible home (§3): superseded
  grain, inverted pointer direction, 0 rows. Delete with evidence per §1 symmetry.
- **DEFECT — R1-F6.** `decisions`, `data_migrations`, `pipeline_runs` have no home under the
  note's namespaces; their substrate assignment is convention. Every future quotation of this
  map should state that convention, per §2(b) discipline on the cross-stage view count.
- **DEFECT — R1-F7.** The taxonomy-name ruling (`base_taxonomy_icf`) supersedes the §R8 name
  `icf_demands`, which is embedded in REPAIR-PLAN P0.6 and a retired-vocabulary register plan
  (`project-standards.md:1378-1443`). P0.6's target name must be re-derived before it executes,
  or the project renames `axes` twice.

## 6. What I attacked and could not break

- **The 5,318-row cross-check.** My independent 7-namespace split reproduces the ledger's
  stage-row total exactly — the two derivations disagree on *placement* (rooms, items, the
  judgment moves) but conserve the census.
- **`evidence_sources` = 13 inbound FK edges** — the ledger's figure (`:1890`) reproduces from
  a cold census.
- **`source_locators` = 0 inbound, 0 outbound edges** — the DR-2026-08-06 wall is physically
  intact; map 1's research assignment survives every test I ran against it.
- **The item-#1 mechanism** — `SVE.ref_id` NOT NULL, FK present, no UNIQUE: reproduced from
  DDL; the "judgment hand-off already exists" claim holds.
- **STAGE-TABLE-MAP's write-test** — applied to all 66 tables, it produced a unique answer for
  62; the 4 residuals (§3) are genuinely cross-stage or homeless, not test failures.
- **`search_admissions` as the only keyed research→evidence edge** — census confirms
  (`exec_id` + `ref_id` FKs); Part J's deletion premise stays refuted.

---

**DIGEST (5 lines):**
1. All 66 tables assigned: base 23 / research 10 / evidence 6 / judgment 5 / synthesis 8 / specification 4 / render 10; rows 5,318, reproducing the ledger's split.
2. Disputes: `source_locators`→research (note NOT adopted, owner instruction + 0-FK wall); `source_value_extractions`→judgment and `evidence_sources`→evidence hand-off (both ruled via item #2); `items`→render rollup (08-26 ruling reconfirmed mid-audit; `base_building` is three new/renamed tables, `rooms`→`base_room_types`).
3. Arguables: `jurisdictional_values` survives in research only while REFERENCE-ONLY holds; `weighting_profile` survives in substrate; `supersession_check` does NOT survive — it is a judgment table (verdict CHECK + NOT NULL tier in DDL).
4. BLOCKER: RENAME-MAP's "the note wins" premise is refuted for 2 of its 4 rows — re-derive the rename from the adoption record, not the note; MAJOR: `pipeline_completeness.py:37` still enforces the five-stage spine against the contract's own restated judgment entry.
5. Homeless/two-home: `decisions`/`data_migrations`/`pipeline_runs` (no note namespace — convention must be stated), `item_population_elaborations` (delete candidate), `gaps` (cross-stage registry kept in research), 677 crossing-map rows keyed on the retiring `items`.
