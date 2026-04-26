# A3 — Conceptual Model
**Phase:** A3 (Conceptual model · 6–8 sessions per CO-0008)
**Session:** 1 of 6–8
**Status:** DRAFT — entity inventory and relationship mapping
**Resolves:** T-06 (design-stage cross-cutting), T-07 (entity list incomplete), N-03 (cross-cutting axes)
**Co-production:** governance document + schemas + validators + converters (per CO-0008)

---

## 1. Entity Inventory

### 1.1 Entities with existing data stores

These entities already have data in the repository. Schema priority is HIGH — converting these to validated YAML proves the data layer and unlocks mechanical validation.

| # | Entity | Current store | Records | Format | Schema priority |
|---|---|---|---|---|---|
| E-01 | **Specification** | specification-database.json → data/specifications/ | 73 | JSON→YAML | DONE (CO-0008) |
| E-02 | **Evidence Source** | global-reference-registry.md, tier*-verified-sources.json | 531 | Md table + JSON | HIGH — A3 |
| E-03 | **BPC Entry** | references/bpc/{topic}/{slug}.md | ~76 | Markdown | HIGH — A3 metadata |
| E-04 | **Connection** | references/connections/_index.md + per-topic files | 181 | Markdown | HIGH — A3 |
| E-05 | **Slug** | references/slug-registry.md | ~60 | Md table | MEDIUM — A3 |
| E-06 | **Search Log** | references/search-log/{topic}/{slug}.md | ~76 | Markdown | LOW — mirrors BPC |
| E-07 | **Gap** | gap_register.md | variable | Md table | MEDIUM — A3 |
| E-08 | **Item** | references/part04-item-index.md | ~90 | Md table | MEDIUM — A6 |
| E-09 | **Conflict** | references/conflict-matrices/ | variable | Markdown | MEDIUM — A6 |
| E-10 | **FDR Scenario** | references/fdr/ | variable | Markdown | LOW — C-stage |

### 1.2 Entities requiring new definition

These entities are identified in the workplan but have no structured data store yet.

| # | Entity | Source of truth | Schema priority |
|---|---|---|---|
| E-11 | **Population** | schemas/enums.py (PopulationCode) | DONE (CO-0008 enum) |
| E-12 | **Sub-population** | Embedded in population descriptions | MEDIUM — A7 |
| E-13 | **Jurisdiction** | schemas/enums.py (JurisdictionCode) | DONE (CO-0008 enum) |
| E-14 | **Audience** | governance/audience-priority.md | LOW — A4 |
| E-15 | **Co-1 Collaborator** | N/A pre-launch (per D-03 revision) | DEFERRED |
| E-16 | **Building Type** | Implicit in room matrices (Parts 6/7) | MEDIUM — A6 |
| E-17 | **Room/Space** | Implicit in room matrices | MEDIUM — A6 |
| E-18 | **Specialist Handoff** | Part 9 §9.9, §9.10 | LOW — C-stage |
| E-19 | **Time-Version** | Metadata on all entities | MEDIUM — A9 |
| E-20 | **Question** | Embedded in Part prose | LOW — B3 |

### 1.3 Cross-cutting axes

These are not entities in the data-store sense — they are dimensions that interact orthogonally with specifications, items, and room matrices.

| Axis | Definition | Interaction |
|---|---|---|
| **Design Stage** | DD (Design Development) / RFO (Ready for Occupancy) / retrofit | Specifications may have different values or applicability at different stages |
| **Project Type** | New construction / major renovation / minor adaptation / maintenance | Constraints on achievable specification compliance vary by type |

These axes produce a **Design Stage × Project Type matrix** that modifies how specifications apply. Not separate entities — they are attributes on Specification and Item entities, plus filter dimensions in Room matrices.

---

## 2. Entity Relationship Map

```
Evidence Source (E-02)
    │ cited_by (1:N)
    ▼
BPC Entry (E-03) ──────── uses_slug ──────── Slug (E-05)
    │ synthesized_into (N:1)                    │ searched_in
    ▼                                           ▼
Specification (E-01)                     Search Log (E-06)
    │ assigned_to (N:1)     conflicts_with (N:N)
    ▼                       ▼
Item (E-08) ◄──── Conflict (E-09)
    │ placed_in (N:N)
    ▼
Room/Space (E-17) ──── typed_as ──── Building Type (E-16)

Population (E-11) ──── applies_to ──── Specification (E-01) [N:N]
                  ──── has_sub ──── Sub-population (E-12) [1:N]

Gap (E-07) ──── blocks ──── any entity (polymorphic reference)

Connection (E-04) ──── links ──── Item × Item (N:N with notes)

FDR Scenario (E-10) ──── informs ──── Specification (E-01)

Time-Version (E-19) ──── attached_to ──── all mutable entities (metadata)
```

### 2.1 Key relationships

**E-02 → E-03 → E-01 (evidence flow):** Sources feed into BPC entries. BPC synthesis produces specifications. This is the primary content pipeline. The `bpc_source_slug` field on Specification already encodes this. The `used_in_slugs` field on Evidence Source encodes the inverse.

**E-01 → E-08 (specification → item):** Many specifications roll up into one item. The `item_code` field on Specification already encodes this. Item is the Part 4 organizing unit.

**E-08 → E-17 (item → room/space):** Items are placed in rooms via matrices (Parts 6/7). This is an N:N relationship — an item appears in multiple room types, and a room type includes many items.

**E-04 (connections):** Connections link items to each other with explanatory notes. They are integration instructions: "when writing specification X, also consider specification Y because of Z." The connection register tracks consumption status.

**E-09 (conflicts):** Conflicts are specific incompatibilities between specifications when two populations occupy the same space. Resolution follows Part 3 §3.8 decision tree.

**E-11 → E-01 (population → specification):** N:N — a specification serves multiple populations, and a population is served by many specifications. The `populations` array on Specification encodes this.

---

## 3. Schema Priority Order (A3 Sessions 2–8)

### Session 2: Evidence Source (E-02) schema + conversion
- **Input:** global-reference-registry.md (531 records), verified-sources JSON files
- **Schema:** EvidenceSource model with REF-ID, authors, year, title, DOI, PMID, tier, evidence_type (per T-03), jurisdiction, metadata_quality
- **Conversion:** convert_sources.py — parses markdown table + JSON files → validated YAML under data/sources/
- **Validator:** validate_sources.py — referential integrity (REF-ID uniqueness, tier validity)
- **Cross-system check:** every REF-ID cited in a BPC key sources table must exist in data/sources/

### Session 3: BPC Metadata (E-03) schema + conversion
- **Input:** bpc/ directory (76 files), validate_bpc.py (existing)
- **Schema:** BPCMetadata model — extracted YAML frontmatter from BPC markdown files
- **Fields:** slug, population, topic, last_updated, opus_synthesis status, T-04 state, key_sources (list of REF-IDs), co1_pass_summary, jurisdiction_coverage
- **Conversion:** convert_bpc_metadata.py — extracts metadata from BPC markdown → YAML under data/bpc-metadata/
- **Validator:** validate_bpc.py rewrite — consumes Pydantic model instead of regex parsing
- **Cross-system check:** every slug in data/bpc-metadata/ must exist in slug-registry; every REF-ID in key_sources must exist in data/sources/

### Session 4: Connection (E-04) schema + conversion
- **Input:** connections/_index.md (181 records) + per-topic connection files
- **Schema:** Connection model — CON-ID, status, primary_target, filed_in, confidence, opus_reviewed, session_applied
- **Conversion:** convert_connections.py — parses index + per-topic files → YAML under data/connections/
- **Validator:** validate_cross_refs.py rewrite — referential integrity (CON-IDs, target item codes, filed_in topic)
- **Cross-system check:** every item_code referenced in a connection's primary_target must exist in part04-item-index

### Session 5: Slug (E-05) + Gap (E-07) schemas
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

## 6. Audit: Cross-System Coherence Check

Infrastructure pour schemas (CO-0008) must align with A3 entity model:

| CO-0008 artifact | A3 alignment status |
|---|---|
| schemas/enums.py — PopulationCode | ✓ Matches canonical list. Sub-population detail deferred to A7. |
| schemas/enums.py — EvidenceTier | ✓ Simplified to 1–6 per T-03 (Session 2). Co-1/Co-2 are evidence_types. |
| schemas/enums.py — EvidenceType | ✓ Added Session 2. 9 values: clinical, co1, co2, sr_meta, standard_eb, national_fw, code, grey, unknown. |
| schemas/enums.py — JurisdictionCode | ✓ 25 countries + 2 meta-codes. Full 24 to confirm at A3. |
| schemas/specification.py — Specification | ✓ Primary entity. EvidenceTierRange updated per T-03. |
| schemas/base.py — EvidenceTierRange | ✓ co1_present replaced with evidence_types_present (Session 2). |
| schemas/evidence_source.py — EvidenceSource | ✓ Built Session 2. 531/531 records convert and validate. |
| scripts/validate_schema.py | ✓ ENTITY_REGISTRY: specifications + sources. 604 files validate. |

**Session 2 complete. Next: Session 3 (BPC Metadata) or Session 4 (Connection).**
