# A3 — Conceptual Model
**Phase:** A3 (Conceptual model)
**Sessions:** 7 (infrastructure pour + S1–S6 + S7 sign-off)
**Status:** SIGNED OFF 2026-04-26 · **Amended 2026-07-21** — entity codes renamed `E-##` → `ENT-##` to remove a namespace collision with `items.item_code` (per `decisions/DR-2026-07-21-entity-code-namespace-rename.md`; no entity semantics changed).
**Resolves:** T-06 (design-stage cross-cutting), T-07 (entity list incomplete), N-03 (cross-cutting axes)
**Co-production:** governance document + 6 schemas + 6 converters + 1 validator + CI integration (per CO-0008)

---

## 1. Entity Inventory

> **Namespace note.** The `ENT-01`…`ENT-20` codes below name **entity types** in the data model. This is a *distinct namespace* from `items.item_code` (the letter-category codes `A-01`…`K-05` that name individual design parameters — e.g. `E-08` = "Corridor Clear Width"). The two must never be conflated: `ENT-08` is the **Item entity type**; `E-08` is the **corridor parameter**. These entity codes were renamed from `E-##` to `ENT-##` on 2026-07-21 precisely to end that collision (`decisions/DR-2026-07-21-entity-code-namespace-rename.md`).

### 1.1 Entities with existing data stores

| # | Entity | Schema | Converter | Records | Status |
|---|---|---|---|---|---|
| ENT-01 | **Specification** | specification.py | convert_spec_db.py | 73 | **DONE** (CO-0008 + A3 S2 T-03) |
| ENT-02 | **Evidence Source** | evidence_source.py | convert_sources.py | 531 | **DONE** (A3 S2) |
| ENT-03 | **BPC Entry** | bpc_metadata.py | convert_bpc_metadata.py | 78 | **DONE** (A3 S3) |
| ENT-04 | **Connection** | connection.py | convert_connections.py | 191 | **DONE** (A3 S4) |
| ENT-05 | **Slug** | slug.py | convert_slugs.py | 64 | **DONE** (A3 S5) |
| ENT-06 | **Search Log** | — | — | ~76 | DEFERRED — mirrors BPC; schema not needed until C-stage |
| ENT-07 | **Gap** | gap.py | convert_gaps.py | 161 | **DONE** (A3 S5) |
| ENT-08 | **Item** | — | — | ~90 | DEFERRED to A6 |
| ENT-09 | **Conflict** | — | — | variable | DEFERRED to A6 |
| ENT-10 | **FDR Scenario** | — | — | variable | DEFERRED to C-stage |

**A3 total: 6 entity types schematized, 1098 records, 6 converters, cross-entity integrity checking operational.**

### 1.2 Entities requiring new definition

| # | Entity | Status | Deferred to |
|---|---|---|---|
| ENT-11 | **Population** | DONE (enum) | — |
| ENT-12 | **Sub-population** | Deferred | A7 |
| ENT-13 | **Jurisdiction** | DONE (enum) | — |
| ENT-14 | **Audience** | Deferred | A4 |
| ENT-15 | **Co-1 Collaborator** | Deferred | Post-launch |
| ENT-16 | **Building Type** | Deferred | A6 |
| ENT-17 | **Room/Space** | Deferred | A6 |
| ENT-18 | **Specialist Handoff** | Deferred | C-stage |
| ENT-19 | **Time-Version** | Deferred | A9 |
| ENT-20 | **Question** | Deferred | B3 |

### 1.3 Cross-cutting axes

Implemented as optional list attributes on Specification (A3 S7). Not separate entities — they are filter dimensions.

| Axis | Enum | Values | Implementation |
|---|---|---|---|
| **Design Stage** | `DesignStage` | DD, RFO, retrofit, all | `design_stages: list[str]` on Specification |
| **Project Type** | `ProjectType` | new_construction, major_renovation, minor_adaptation, maintenance, all | `project_types: list[str]` on Specification |

Empty list = applies to all stages/types. Populated during specification authoring (A6+), not during A3.

---

## 2. Entity Relationship Map

```
Evidence Source (ENT-02)
    │ cited_by (1:N)
    ▼
BPC Entry (ENT-03) ──────── uses_slug ──────── Slug (ENT-05)
    │ synthesized_into (N:1)                    │ searched_in
    ▼                                           ▼
Specification (ENT-01)                     Search Log (ENT-06)
    │ assigned_to (N:1)     conflicts_with (N:N)
    ▼                       ▼
Item (ENT-08) ◄──── Conflict (ENT-09)
    │ placed_in (N:N)
    ▼
Room/Space (ENT-17) ──── typed_as ──── Building Type (ENT-16)

Population (ENT-11) ──── applies_to ──── Specification (ENT-01) [N:N]
                  ──── has_sub ──── Sub-population (ENT-12) [1:N]

Gap (ENT-07) ──── blocks ──── any entity (polymorphic reference)

Connection (ENT-04) ──── links ──── Item × Item (N:N with notes)

FDR Scenario (ENT-10) ──── informs ──── Specification (ENT-01)

Time-Version (ENT-19) ──── attached_to ──── all mutable entities (metadata)
```

### 2.1 Key relationships

**ENT-02 → ENT-03 → ENT-01 (evidence flow):** Sources feed into BPC entries. BPC synthesis produces specifications. This is the primary content pipeline. The `bpc_source_slug` field on Specification already encodes this. The `used_in_slugs` field on Evidence Source encodes the inverse.

**ENT-01 → ENT-08 (specification → item):** Many specifications roll up into one item. The `item_code` field on Specification already encodes this. Item is the Part 4 organizing unit.

**ENT-08 → ENT-17 (item → room/space):** Items are placed in rooms via matrices (Parts 6/7). This is an N:N relationship — an item appears in multiple room types, and a room type includes many items.

**ENT-04 (connections):** Connections link items to each other with explanatory notes. They are integration instructions: "when writing specification X, also consider specification Y because of Z." The connection register tracks consumption status.

**ENT-09 (conflicts):** Conflicts are specific incompatibilities between specifications when two populations occupy the same space. Resolution follows Part 3 §3.8 decision tree.

**ENT-11 → ENT-01 (population → specification):** N:N — a specification serves multiple populations, and a population is served by many specifications. The `populations` array on Specification encodes this.

---

## 3. Schema Priority Order (A3 Sessions 2–8)

### Session 2: Evidence Source (ENT-02) schema + conversion
- **Input:** global-reference-registry.md (531 records), verified-sources JSON files
- **Schema:** EvidenceSource model with REF-ID, authors, year, title, DOI, PMID, tier, evidence_type (per T-03), jurisdiction, metadata_quality
- **Conversion:** convert_sources.py — parses markdown table + JSON files → validated YAML under data/sources/
- **Validator:** validate_sources.py — referential integrity (REF-ID uniqueness, tier validity)
- **Cross-system check:** every REF-ID cited in a BPC key sources table must exist in data/sources/

### Session 3: BPC Metadata (ENT-03) schema + conversion
- **Input:** bpc/ directory (76 files), validate_bpc.py (existing)
- **Schema:** BPCMetadata model — extracted YAML frontmatter from BPC markdown files
- **Fields:** slug, population, topic, last_updated, opus_synthesis status, T-04 state, key_sources (list of REF-IDs), co1_pass_summary, jurisdiction_coverage
- **Conversion:** convert_bpc_metadata.py — extracts metadata from BPC markdown → YAML under data/bpc-metadata/
- **Validator:** validate_bpc.py rewrite — consumes Pydantic model instead of regex parsing
- **Cross-system check:** every slug in data/bpc-metadata/ must exist in slug-registry; every REF-ID in key_sources must exist in data/sources/

### Session 4: Connection (ENT-04) schema + conversion
- **Input:** connections/_index.md (181 records) + per-topic connection files
- **Schema:** Connection model — CON-ID, status, primary_target, filed_in, confidence, opus_reviewed, session_applied
- **Conversion:** convert_connections.py — parses index + per-topic files → YAML under data/connections/
- **Validator:** validate_cross_refs.py rewrite — referential integrity (CON-IDs, target item codes, filed_in topic)
- **Cross-system check:** every item_code referenced in a connection's primary_target must exist in part04-item-index

### Session 5: Slug (ENT-05) + Gap (ENT-07) schemas
- Lightweight entities — small record count, simple structure
- Slug schema validates against BPC and search-log existence
- Gap schema enforces priority/status state machine

### Session 6: Cross-cutting axes + entity interaction
- Design Stage and Project Type as attributes on Specification and Item
- Room/Space and Building Type entity scaffolding (deferred data population to A6)
- validate_entities.py — master validator that runs all entity-type validators

### Sessions 7–8: Integration testing + governance document finalization
- End-to-end referential integrity across all entity types
- Conceptual model diagrams
- Governance document sign-off

---

## 4. T-03 Schema Encoding (from pre-Stage-A decisions)

Per T-03 resolution: `tier` + `evidence_type` taxonomy.

```python
class EvidenceType(str, Enum):
    CLINICAL = "clinical"       # OT intervention-tested
    CO1 = "co1"                 # Lived experience / participatory
    CO2 = "co2"                 # OT professional body CPGs
    SR_META = "sr_meta"         # Systematic reviews / meta-analyses
    STANDARD_EB = "standard_eb" # International standards with evidence basis
    NATIONAL_FW = "national_fw" # National beyond-code frameworks
    CODE = "code"               # Statutory codes

# On EvidenceSource:
tier: int           # 1–6
evidence_type: EvidenceType
```

**Schema impact:** ~~The `EvidenceTierRange` model in schemas/base.py (built in infrastructure pour) uses `floor/ceiling/co1_present`. This needs reconciliation with T-03.~~ **RESOLVED (A3 Session 2, 2026-04-26):** EvidenceTier enum simplified to 1–6 (Co-1/Co-2 removed as tier values). EvidenceTierRange.co1_present replaced with evidence_types_present: list[str]. EvidenceType enum added to enums.py. EvidenceSource schema built with tier + evidence_type per T-03. Converter handles all observed tier formats (531/531 pass). Cross-system check: evidence type distribution aligns with tier counts (clinical+co1=91=tier1 ✓).

**Resolution:** COMPLETE. See schemas/enums.py (EvidenceType), schemas/base.py (EvidenceTierRange), schemas/evidence_source.py (EvidenceSource).

---

## 5. Decisions Required (for A3 Session 3+)

| Decision | Options | Impact |
|---|---|---|
| D-A3-01: Sub-population as separate entity vs attribute? | Entity: separate YAML records. Attribute: field on Population enum with metadata. | Schema complexity. A7 dependency. |
| D-A3-02: Room/Space entity timing | Now (scaffold) vs A6 (with matrices) | Data availability. Current matrices are prose, not structured. |
| D-A3-03: Question entity definition | Structured YAML records vs embedded prose markers | B3 dependency. Questions don't exist as data yet. |
| D-A3-04: Time-Version as entity vs metadata pattern | Separate entity with version history vs `version_created` + `version_superseded` fields on all entities | Schema complexity vs audit trail. A9 dependency. |

---

## 6. Final Audit

| Component | Status |
|---|---|
| schemas/enums.py — PopulationCode (24 codes) | ✓ |
| schemas/enums.py — EvidenceTier (1–6 per T-03) | ✓ |
| schemas/enums.py — EvidenceType (9 values per T-03) | ✓ |
| schemas/enums.py — JurisdictionCode (27 codes) | ✓ |
| schemas/enums.py — DesignStage, ProjectType (cross-cutting) | ✓ |
| schemas/specification.py (73 records, cross-cutting fields) | ✓ |
| schemas/evidence_source.py (531 records) | ✓ |
| schemas/bpc_metadata.py (78 records) | ✓ |
| schemas/connection.py (191 records) | ✓ |
| schemas/slug.py (64 records) | ✓ |
| schemas/gap.py (161 records) | ✓ |
| scripts/validate_schema.py (6 entity types + cross-check) | ✓ |
| CI schema job (validate + cross-entity) | ✓ |
| T-03 reconciliation (tier + evidence_type) | ✓ |

**Cross-entity integrity:** 17 diagnostic issues (1 population-code-as-slug, 16 slug registry gaps). All expected — data quality items, not schema errors.

---

## 7. Sign-off

**A3 is SIGNED OFF.** The conceptual model defines 20 entities across three categories. 6 entity types are schematized with Pydantic models, converters, and CI validation. 4 entities are deferred to A6 (Item, Conflict, Room/Space, Building Type). 6 entities are deferred to later phases (A4, A7, A9, B3, C-stage, post-launch). 2 cross-cutting axes are implemented as attributes on Specification.

The data layer pattern is proven: schema → converter → validator → CI. All subsequent governance phases (A6–A13) follow this pattern per CO-0008.

**Resolved findings:** T-06 (design stage cross-cutting — DesignStage enum + Specification attribute), T-07 (entity inventory — 20 entities mapped), N-03 (cross-cutting axes — DesignStage × ProjectType).

**Next phase:** A4 (Voice). Prose-only phase — no schema co-production. Key task: retire "shall be" convention in Part 4 text per advocacy identity rule (project-standards 2026-04-26).
DATE: 2026-04-26
