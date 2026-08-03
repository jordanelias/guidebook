# Website Data Schema — Unified Reference
**Created:** 2026-04-09 22:45
**Phase:** 0.2 — economics entity expanded (2026-05-04)
**Status:** DRAFT — economics entity updated to v2.0 (7 sub-entities); cross-referential integrity check pending

---

## Overview

Six primary entity types serve six website interfaces. All entities cross-reference via stable IDs. The specification entity is the atomic unit — everything else references it or is referenced by it.

```
specifications ←→ populations (many-to-many via population tags)
specifications ←→ room_types (many-to-many via room matrices)
specifications ←→ conflicts (many-to-many via conflict domains)
specifications ←→ case_studies (many-to-many via case study tags)
specifications ←→ economics (one-to-many via cost records + spec_cross_refs)
populations ←→ conflicts (many-to-many via conflict participants)
economics.throughlines → specifications (many-to-many via spec_cross_refs)
economics.health_outcomes → economics.grant_programmes (jurisdiction linkage)
economics.housing_deficit → economics.retrofit_multipliers (jurisdiction linkage)
economics.research_gaps → all economics sub-entities (pillar linkage)
```

---

## Entity 1: Specifications

**Source:** Part 4 item specifications + BPC synthesis files
**Interface:** Specification Explorer
**Current state:** 73 records in `specification-database.json` from batch 1 (10 BPC files). Schema exists in `specification-database-schema.md`.
**Target:** 400–600 records from all 93 BPC files + Part 4 items.

### Schema (extends existing)

```json
{
  "spec_id": "SPEC-0001",
  "item_code": "A-01",
  "item_title": "Acoustic Buffer Zones at Noisy Adjacencies",
  "category": "A",
  "category_name": "Acoustics",
  "bpc_source_slug": "room-acoustic-performance",
  "topic": "sensory-environment",

  "parameter": "buffer_zone_depth",
  "parameter_label": "Buffer zone depth",
  "value_type": "range",
  "value_min": 3000,
  "value_max": 5000,
  "value_median": 4000,
  "unit": "mm",
  "unit_display": "3–5 m",

  "universal_value": null,
  "population_value": {"min": 3000, "max": 5000, "median": 4000},
  "person_specific_note": "OT assessment resolves position within range based on adjacency noise level and population sensitivity",

  "evidence_tier": "Tier 4–5",
  "evidence_marker": "◐",
  "evidence_summary": "PAS 6463:2022 (BSI); WELL v2; Bettarello et al. 2021",
  "opus_synthesized": false,
  "recommendation_strength": "Conditional",

  "populations": ["ALL", "NDV", "NEU", "DEM", "OFS", "PAIN"],
  "population_primary": ["NDV", "NEU/PCS"],
  "population_secondary": ["DEM", "OFS", "PAIN"],

  "jurisdictions_supporting": ["UK", "US", "AU"],
  "jurisdictions_divergent": [],
  "jurisdiction_count": 14,
  "language_count": 24,

  "conditions": [
    {"condition": "DEM or NEU/PCS primary occupant", "value_min": 5000, "value_max": 5000, "note": "Clinical requirement"}
  ],

  "retrofit_penalty": "LOW — PLANNING",
  "retrofit_note": "Zero cost at design stage. Retrofit requires spatial reorganisation.",
  "dar_relevant": true,
  "dar_note": "Adjacency planning decision; cannot be retrofitted without major disruption",

  "cross_references": ["A-02", "A-08", "A-16"],
  "connection_ids": ["CON-0039", "CON-0069"],
  "conflict_domains": ["ACOUSTIC-LVL"],

  "ot_evidence_basis": "EHP Framework (alter strategy); Dunn's Sensory Processing Model",
  "fdr_findings": ["FDR-IntD-02"],

  "citations": [
    {"ref": "PAS 6463:2022", "tier": 5, "language": "EN"},
    {"ref": "Bettarello et al. 2021", "tier": 3, "language": "EN"},
    {"ref": "WELL v2 2024", "tier": 5, "language": "EN"}
  ],

  "percentile_basis": null,
  "extraction_batch": "batch1",
  "last_updated": "2026-04-09",
  "curation_status": "automated"
}
```

### New fields vs existing schema

| Field | New? | Rationale |
|---|---|---|
| `item_title` | YES | Display name for web UI |
| `category_name` | YES | Human-readable category label |
| `parameter_label` | YES | Human-readable parameter name |
| `unit_display` | YES | Formatted display string |
| `universal_value` / `population_value` / `person_specific_note` | YES | Three-tier hierarchy values for interactive display |
| `evidence_marker` | YES | ● / ◐ / ○ for visual display |
| `evidence_summary` | YES | Short citation string for card view |
| `population_primary` / `population_secondary` | YES | Distinguishes design-driver populations from beneficiary populations |
| `jurisdiction_count` / `language_count` | YES | Summary counts for credibility display |
| `retrofit_penalty` | YES | Structured retrofit category (LOW/MODERATE/HIGH + qualifier) |
| `dar_relevant` / `dar_note` | YES | DAR integration |
| `cross_references` | YES | Item-to-item links |
| `connection_ids` | YES | Links to connection register |
| `conflict_domains` | YES | Links to conflict entity |
| `ot_evidence_basis` | YES | OT framework citation |
| `fdr_findings` | YES | Links to FDR findings |
| `citations` | YES (replaces context_note) | Structured citation array with tier and language |
| `last_updated` | YES | Content currency |
| `curation_status` | YES | automated / reviewed / opus-synthesized |

---

## Entity 2: Populations

**Source:** Part 2 disability categories + population BPC files
**Interface:** Population Navigator
**Target:** 14 records (11 primary codes + 3 sub-code expansions)

### Schema

```json
{
  "population_id": "MOB",
  "label": "Mobility and Strength",
  "sub_codes": ["MOB/AMB", "MOB/UPL"],
  "sub_code_labels": {
    "MOB/AMB": "Ambulant with mobility aid",
    "MOB/UPL": "Upper limb and amputation"
  },

  "functional_profile": "Wheelchair users (manual/power), scooter users, ambulant with walking aids, lower limb weakness, balance impairment, reduced walking endurance",
  "primary_barriers": ["Steps", "Thresholds >6mm", "Gradients >1:20", "Inadequate clear widths", "High rolling resistance", "Grip/twist hardware", "Absent rest seating", "Inadequate grab bars"],

  "key_specifications": ["E-06", "E-08", "E-01", "I-04", "G-03", "G-05", "K-01", "H-01"],
  "specification_count": 45,

  "conflict_domains": ["GRAB BAR DIAMETER", "SURFACE-TEXT", "MOVE-FREE"],
  "conflict_summary": "MOB has zero conflict flags with any other population's core provisions — MOB provisions are beneficial or neutral for all categories",

  "co_occurrence_notes": "Most common compound profiles: MOB+PAIN, MOB+OFS, MOB+DEM (ageing population)",
  "evidence_confidence": "HIGH",
  "evidence_sources": ["IDeA Center AWM Project (Tier 1)", "Clemson et al. 2023 Cochrane", "24-jurisdiction convergence"],

  "bpc_slugs": ["mobility-built-environment", "upper-limb-impairment-built-environment", "stair-ramp-threshold-biomechanics-accessibility", "accessible-bathroom-and-grab-bar"],

  "co1_status": "Partial — KR and BR Co-1 sources not retrieved",
  "co1_gap_note": "Lived experience evidence from Korean and Brazilian disability organisations not confirmed",

  "last_updated": "2026-04-09"
}
```

---

## Entity 3: Room Types

**Source:** Parts 6–7 application matrices
**Interface:** Room Configurator
**Target:** ~25–30 records (residential + non-residential room types)

### Schema

```json
{
  "room_id": "R-ENT",
  "room_label": "Entry",
  "building_type": "residential",
  "part_source": 6,
  "section": "§6.1",

  "criticality_note": "The entry is the most consequential zone in the residence. Failure here blocks all other provisions.",
  "primary_populations": ["MOB", "VIS", "DEAF", "DBL", "OFS"],

  "item_matrix": [
    {
      "item_code": "E-06",
      "item_title": "Step-free threshold",
      "design_stage": "SD",
      "must_appear_on": "Site plan; floor plan",
      "population_applicability": {
        "MOB": "primary",
        "VIS": "secondary",
        "DEAF": null,
        "DEM": "primary",
        "NDV": null,
        "OFS": "primary",
        "DBL": "primary",
        "IntD_proxy": "secondary"
      }
    }
  ],

  "dar_provisions": [
    {
      "item_code": "I-03",
      "description": "Grab bar structural blocking in all bathrooms",
      "stage": "CD",
      "drawing": "Structural/blocking drawings"
    }
  ],

  "conflict_register": [
    {
      "conflict_domain": "LIGHT-INT",
      "populations_involved": ["DEM", "NDV"],
      "resolution_ref": "§5.2 LIGHT-INT",
      "status": "RESOLVED-CONSENSUS"
    }
  ],

  "last_updated": "2026-04-09"
}
```

---

## Entity 4: Conflicts

**Source:** Part 5 §5.2–5.3 + connection register
**Interface:** Conflict Resolver
**Target:** ~15–20 records (11 resolved + 3 unresolvable + compound scenarios)

### Schema

```json
{
  "conflict_id": "COLOUR-CONT",
  "conflict_label": "Luminance contrast (LRV)",
  "domain": "Colour and contrast",

  "population_a": {
    "codes": ["VIS", "DEM"],
    "specification": "≥30% LRV differential at step edges, door frames, counter edges; ≥50% at critical junctions"
  },
  "population_b": {
    "codes": ["NDV/SENS", "NDV/AUT"],
    "specification": "Muted palette; ≤20 LRV differential in sensory retreat zones"
  },

  "resolution": {
    "status": "RESOLVED-EVIDENCE",
    "strategy_codes": ["SZ", "PP"],
    "strategy_labels": ["Sensory Zoning", "Parallel Provision"],
    "description": "Zone-based: ≥30 LRV on all primary accessible routes (safety-critical; governs); ≤20 LRV in sensory retreat spaces (NDV comfort served). Plain floor (C-06) throughout primary routes satisfies both DEM fall prevention and VIS orientation via perimeter contrast.",
    "evidence_quality": "●"
  },

  "governing_principle": "Safety-critical provisions take priority (Resolution Hierarchy §5.1, Rule 1)",

  "specifications_involved": ["C-04", "C-06", "F-01"],
  "connection_ids": [],

  "citations": [
    {"ref": "DSDC EADDAT 2022", "finding": "DEM plain floor; +15% pattern-associated falls"},
    {"ref": "CNIB 2024", "finding": "VIS contrast minimum"},
    {"ref": "PAS 6463:2022", "finding": "NDV muted palette"}
  ],

  "decision_tree": {
    "root": "Is this a primary accessible route?",
    "yes": "Apply ≥30 LRV contrast (safety-critical — VIS/DEM governs)",
    "no": {
      "question": "Is this a designated sensory retreat zone (F-01 Zone 3)?",
      "yes": "Apply ≤20 LRV; VIS orientation via wall contrast and architectural landmarks",
      "no": "Apply ≥30 LRV with matte/non-reflective finishes"
    }
  },

  "unresolvable_residual": null,
  "tier_2_trigger": null,

  "last_updated": "2026-04-09"
}
```

### Unresolvable conflict schema extension

```json
{
  "conflict_id": "CONF-UNRESOLV-01",
  "conflict_label": "Ambient temperature in non-zoned shared sleeping space",
  "resolution": {
    "status": "UNRESOLVABLE-MODE-S",
    "description": "Non-zoned shared sleeping space where ambient temperature is truly shared and individual supplemental heating is not operationally feasible"
  },
  "tier_2_trigger": "Building or space simultaneously serves MS-spectrum diagnosis and fibromyalgia/cold-aggravated pain in shared non-zoned sleeping space",
  "mitigation": "Insulated coated grab bars; warm bedding specification; individual heated throw/vest as FM provision",
  "ot_assessment_mandatory": true
}
```

---

## Entity 5: Economics

**Source:** Part 11 + `references/methodology/throughline-*.md` + `references/cost-data/`
**Interface:** Economics Engine
**Current state:** `economics.json` with 8 cost premiums, 3 retrofit multipliers, 9 grant programmes, 10 health outcome studies, 5 market-value throughlines, 5 housing deficit records, 11 research gaps. Organized by four-pillar economic case.
**Target:** ~80–120 records across seven sub-entities
**Data file:** `references/website/data/economics.json`

**Four-pillar framework:**
| Rank | Pillar | Strength | Throughline file |
|------|--------|----------|-----------------|
| 1 | Health Outcomes | Strong | `throughline-health-outcomes.md` |
| 2 | Cost of Inaction | Strong | `throughline-cost-of-inaction.md` |
| 3 | Construction Cost | Moderate–Strong | `throughline-construction-cost.md` |
| 4 | Market Value | Weak-direct / Framework-strong | `throughline-market-value.md` |

### 5a: Cost Premiums (Pillar 3)

```json
{
  "cost_id": "COST-PREM-001",
  "source": "TERRAGON/DStGB 2017",
  "jurisdiction": "DE",
  "building_type": "residential",
  "building_detail": "Model five-storey residential building, Berlin, 20 dwellings, 1500 m²",
  "standard": "DIN 18040-2",
  "finding": "138 of 148 criteria produce zero additional cost at design stage",
  "premium_percent_min": 0.54,
  "premium_percent_max": 1.26,
  "premium_per_sqm": 21.50,
  "currency": "EUR",
  "year": 2017,
  "evidence_tier": "E-3/E-4",
  "methodology": "Bottom-up elemental cost comparison",
  "single_source_flag": false,
  "commercial_interest_flag": true,
  "commercial_interest_note": "TERRAGON AG is a residential developer. Corroborated by Bundesfachstelle Barrierefreiheit.",
  "pillar": "construction",
  "spec_cross_refs": [],
  "last_updated": "2026-05-04"
}
```

### 5b: Retrofit Multipliers (Pillar 2)

```json
{
  "multiplier_id": "RETRO-MUL-001",
  "jurisdiction": "DE",
  "source": "TERRAGON AG / KfW / Prognos",
  "new_build_cost": 1600,
  "retrofit_cost": 19100,
  "multiplier": 12,
  "currency": "EUR",
  "unit": "per 75 m² apartment",
  "year": 2017,
  "evidence_tier": "E-3",
  "traceability_flag": false,
  "pillar": "inaction",
  "last_updated": "2026-05-04"
}
```

### 5c: Grant Programmes (Pillar 2)

```json
{
  "grant_id": "GRANT-001",
  "programme_name": "Disabled Facilities Grant (DFG)",
  "jurisdiction": "UK",
  "administering_body": "Local authorities (England)",
  "type": "Mandatory grant",
  "max_funding": 30000,
  "currency": "GBP",
  "eligibility": "Means-tested adults; not means-tested for children under 18",
  "annual_budget": 761000000,
  "budget_year": 2025,
  "source": "UK Government",
  "evidence_tier": "E-1",
  "status": "Active",
  "pillar": "inaction",
  "last_updated": "2026-05-04"
}
```

### 5d: Health Outcomes (Pillar 1) — NEW

Evidence hierarchy ranked by study design quality. Cross-jurisdictional convergence: NZ (RCT, 9:1 BCR at $500/person) and US (quasi-experimental, 10:1 BCR at $1,300/person).

```json
{
  "health_id": "HEALTH-001",
  "source": "Clemson et al. 2023",
  "study_design": "Cochrane Systematic Review",
  "sample": "6 RCTs, N=3,298",
  "journal": "Cochrane Database of Systematic Reviews",
  "jurisdiction": "Multi-jurisdictional",
  "finding": "21% falls risk reduction from home modifications",
  "bcr": null,
  "cost_per_person": null,
  "evidence_tier": "Tier 1",
  "evidence_rank": 1,
  "pillar": "health",
  "spec_cross_refs": [],
  "last_updated": "2026-05-04"
}
```

### 5e: Market Value (Pillar 4) — NEW

Contains three nested structures: `throughlines` (5 records mapping accessibility specs to property-value mechanisms), `anchor_data_point` (CvV Universal Design Bath 61% ROI), and `dual_read_thesis` (NAHB 2024 accessibility↔mainstream label mappings).

```json
{
  "throughline_id": "THRU-001",
  "label": "Square-footage inheritance",
  "evidence_tier": "Tier 1 (by inheritance from Sirmans 2006)",
  "description": "Accessibility minimums are dimensional minimums. Floor area is the most consistently priced hedonic variable.",
  "mechanism": "Dimensional generosity",
  "spec_cross_refs": ["E-04", "E-08", "E-12", "G-04", "G-08", "D-05"],
  "strength_pct": 95,
  "pillar": "market"
}
```

### 5f: Housing Deficit (Pillar 2) — NEW

Cross-jurisdictional accessible housing supply gaps.

```json
{
  "deficit_id": "DEFICIT-001",
  "jurisdiction": "US",
  "accessible_pct": 5,
  "accessible_label": "<5% moderate mobility accessible",
  "gap_units": 300000,
  "source": "HUD USER / AHS 2011; GAO 2023",
  "pillar": "inaction",
  "last_updated": "2026-05-04"
}
```

### 5g: Research Gaps — NEW

Consolidated gap register tracking 11 open research priorities across all pillars.

```json
{
  "gap_id": "GAP-ECON-01",
  "priority": "critical",
  "pillar": "market",
  "label": "Peer-reviewed hedonic accessibility premium",
  "description": "No peer-reviewed hedonic regression isolates an accessibility premium in any jurisdiction.",
  "status": "open"
}
```

---

## Entity 6: Case Studies

**Source:** Part 12
**Interface:** Case Study Library
**Target:** 8–12 records (current Part 12 entries + failure cases)

### Schema

```json
{
  "case_study_id": "CS-001",
  "title": "Maggie's Centre, Inverness",
  "building_type": "Cancer support centre",
  "architect": "Snøhetta",
  "year": 2021,
  "jurisdiction": "UK",
  "setting": "NHS Highland, Scotland",

  "primary_populations": ["MH", "PAIN", "OFS"],
  "population_note": "Cancer patients, family members, clinical staff",

  "evidence_quality": "Tier 2",
  "evidence_note": "Independent RHFAC certification + NHS post-occupancy evaluation",

  "design_strategies": [
    {"item_code": "E-06", "description": "Single-storey, step-free throughout"},
    {"item_code": "BIO-01", "description": "≥75% of occupied spaces with direct nature views"},
    {"item_code": "A-16", "description": "Low RT60 spaces with individual quiet rooms"},
    {"item_code": "F-01", "description": "Sensory gradient from entry to quiet room"},
    {"item_code": "B-03", "description": "Warm CCT 2700–3000 K; no fluorescent"}
  ],

  "verified_outcomes": [
    {
      "metric": "RHFAC certification",
      "result": "Accessible Level",
      "tier": 5,
      "source": "RHFAC",
      "sample_size": null
    },
    {
      "metric": "User wellbeing rating",
      "result": "Majority positive/very positive",
      "tier": 3,
      "source": "NHS Highland POE 2023",
      "sample_size": 87
    }
  ],

  "cost_data": {
    "available": false,
    "note": "Standard NHS healthcare construction rates (approx. £3,500–£4,500/m²)"
  },

  "limitations": "Self-selected population; post-occupancy survey not independently audited",

  "is_failure_case": false,
  "failure_analysis": null,

  "images": [],
  "external_links": [],

  "community_contributions": [],

  "last_updated": "2026-04-09"
}
```

---

## Cross-Cutting Entity: Connections

**Source:** `references/connections/` (27 per-topic files + `_index.md`)
**Not a primary interface — serves as the relationship layer between specifications.**

```json
{
  "connection_id": "CON-0039",
  "status": "CONSUMED",
  "confidence": "HIGH",
  "primary_targets": ["A-01", "A-02", "A-08"],
  "topic_file": "sensory-environment",
  "description": "RT60 ≤0.3 s mid-frequency Universal Mode for speech-critical rooms",
  "opus_reviewed": true,
  "session_applied": "2026-04-03",
  "last_updated": "2026-04-09"
}
```

---

## Cross-Cutting Entity: Citations

**Normalized citation table — deduplicated across all entities.**

```json
{
  "citation_id": "CIT-0001",
  "short_ref": "PAS 6463:2022",
  "full_ref": "British Standards Institution. (2022). PAS 6463:2022 — Design for the mind. Neurodiversity and the built environment. BSI.",
  "type": "standard",
  "language": "EN",
  "jurisdiction": "UK",
  "year": 2022,
  "doi": null,
  "url": null,
  "evidence_tier": 5,
  "verified": true,
  "referenced_by_specs": ["SPEC-0001", "SPEC-0005", "SPEC-0012"],
  "referenced_by_conflicts": ["COLOUR-CONT", "ACOUSTIC-LVL"],
  "last_verified": "2026-04-09"
}
```

---

## Foreign Key Map

| From | To | Relationship | Key field |
|---|---|---|---|
| specifications | populations | many-to-many | `populations[]` |
| specifications | room_types | many-to-many | `room_types.item_matrix[].item_code` |
| specifications | conflicts | many-to-many | `conflict_domains[]` / `conflicts.specifications_involved[]` |
| specifications | case_studies | many-to-many | `case_studies.design_strategies[].item_code` |
| specifications | economics.retrofit | one-to-many | `economics.retrofit.item_code` |
| specifications | connections | many-to-many | `connection_ids[]` |
| specifications | citations | many-to-many | `citations[].citation_id` (after normalization) |
| populations | conflicts | many-to-many | `conflicts.population_a.codes[]` / `population_b.codes[]` |
| populations | specifications | many-to-many | reverse of spec→pop |
| room_types | specifications | many-to-many | `item_matrix[].item_code` |
| case_studies | specifications | many-to-many | `design_strategies[].item_code` |
| conflicts | specifications | many-to-many | `specifications_involved[]` |

---

## Data Integrity Rules

1. Every `item_code` in any entity must exist in the specifications table.
2. Every `population_id` referenced anywhere must exist in the populations table.
3. Every `conflict_id` / `conflict_domain` must exist in the conflicts table.
4. Every `connection_id` must exist in the connections table and match `_index.md`.
5. Every citation `short_ref` should resolve to a normalized citation record.
6. No specification may have `evidence_tier: null` AND `curation_status: "reviewed"`.
7. Every population must have at least one linked specification.
8. Every conflict must reference at least two populations and at least one specification.

---

## Version and Migration

- Schema version: `0.1.0` (this document)
- All records carry `last_updated` for staleness detection
- All records carry a source-tracing field (`bpc_source_slug`, `part_source`, `extraction_batch`)
- Migration from existing `specification-database.json`: add new fields with null/empty defaults; existing data preserved

---

## Next Steps

- **Phase 0.2:** Populate `populations.json` from Part 2 + BPC population files
- **Phase 0.3:** Populate `room_types.json` from Parts 6–7
- **Phase 0.4:** Populate `conflicts.json` from Part 5
- **Phase 0.5:** Populate `case_studies.json` from Part 12
- **Phase 0.6:** Populate `economics.json` from Part 11 + cost-data files
- **Phase 0.7:** Cross-referential integrity validation across all entities
