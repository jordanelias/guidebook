# Throughline Analysis: specification-database.json

**Date:** 2026-04-26 18:22
**Input:** specification-database.json v0.1 (73 records, 25 BPC files processed)
**Purpose:** Inform Pydantic schema design for CO-0008 Layer 1

---

## 1. Data Shape Summary

73 specifications across 21 unique item codes, 56 unique parameters, drawn from 21 BPC source slugs. Every record has 22 fields. Two value types: fixed (50) and range (23).

---

## 2. Findings

### F-01: Evidence tier encoding is compound and inconsistent

Current `evidence_tier` values use free-text compound strings:

| Pattern | Count | Example |
|---|---|---|
| Tier N-M (range) | 48 | "Tier 4-5", "Tier 3-5" |
| Single tier | 13 | "Tier 3", "Tier 5" |
| Co-1/Tier N | 4 | "Co-1/Tier 3", "Co-1/Tier 4" |
| Tier N-M (wide) | 8 | "Tier 1-3", "Tier 2-5" |

**Schema implication:** Cannot use a simple enum. Need either: (a) a structured object with `tier_floor` and `tier_ceiling` fields plus a `co1_present` boolean, or (b) a validated string pattern. Option (a) is mechanically verifiable and supports range queries.

### F-02: Recommendation strength is free-text with embedded semantics

21 records: `[UNSET — Opus review required]`. 27 records: `Conditional at Tier 1`. 17 records: `Strong at Universal Mode`. Remaining 8 use compound descriptions with parenthetical qualifiers.

**Schema implication:** Enum with values {UNSET, STRONG_UNIVERSAL, CONDITIONAL_POPULATION, CONDITIONAL} plus optional `qualifier` text field. Parenthetical detail moves to qualifier.

### F-03: Parameter naming is inconsistent

Three variants for door width: `door_clear_width`, `door_clear_width_minimum`, `door_clear_width_wheelchair`. Similar duplication for corridor width and turning space. 8 records use `unclassified` as parameter name.

**Schema implication:** Parameter should be a constrained string (snake_case, no "unclassified" sentinel). Need a parameter registry or at minimum a validation rule rejecting sentinels. Full normalization is an A3 task — schema accepts current values but flags sentinels.

### F-04: percentile_basis is vestigial

100% null across all 73 records. No BPC file populates it.

**Schema implication:** Include as Optional[str] with deprecation note. Do not require. Flag for removal at A3 review.

### F-05: conditions and person_specific_note are sparse

`conditions`: 70/73 empty. `person_specific_note`: 62/73 empty. `divergence_note`: 50/73 empty.

**Schema implication:** All Optional. Sparsity is not an error — these fields carry signal when present (conditions capture context-dependent applicability).

### F-06: Zero Opus synthesis completed

0/73 records have `opus_synthesized: true`. All recommendation_strength values marked UNSET are awaiting Opus review. The 52 with values were set during batch extraction — not Opus-validated.

**Schema implication:** `opus_synthesized` should be a boolean with default False. Add `opus_synthesis_date` as Optional[str] for tracking when synthesis occurs.

### F-07: Item code sentinels need structured handling

7 records: `[UNASSIGNED]`. 4 records: `[CROSS-CUTTING]`. These are not item codes — they are assignment states.

**Schema implication:** `item_code` is Optional[str] (nullable when unassigned). Separate `assignment_status` enum: {ASSIGNED, UNASSIGNED, CROSS_CUTTING}. The sentinel strings become structured state.

### F-08: Population codes match canonical list but sub-codes vary

All population values map to canonical codes from workplan-orchestrator. Sub-codes (MOB/AMB, MOB/UPL, NDV/AUT) appear in the populations array alongside top-level codes.

**Schema implication:** PopulationCode enum must include both top-level and sub-codes. Validation: sub-code implies parent (MOB/AMB → MOB must also be present or be inferrable).

### F-09: Jurisdiction codes are informal

UK, AU, ISO, DE, US, FR, NO, CA, IN, EU, NL, NZ, ID, BD, NG. Mix of ISO 3166-1 alpha-2 and informal codes (UK not GB, ISO not a country). "EU" is ambiguous.

**Schema implication:** Define JurisdictionCode enum with the canonical 24 jurisdictions from jurisdiction-tracker plus ISO, EU as meta-codes. Validate against this enum.

### F-10: value_min/value_max/value_median are nullable for qualitative specs

2 records have null min/max/median — qualitative parameters where presence matters but no number applies.

**Schema implication:** All three are Optional[float]. When `value_type` is "fixed", min == max == median (validate). When "range", min < max and median is between them (validate). When all null, parameter is qualitative (presence-only).

---

## 3. Schema Design Decisions

Based on findings:

1. **EvidenceTierRange** model: `floor: EvidenceTier`, `ceiling: EvidenceTier`, `co1_present: bool` — replaces compound string (F-01)
2. **RecommendationStrength** enum: UNSET, STRONG_UNIVERSAL, CONDITIONAL_POPULATION, CONDITIONAL — with qualifier text (F-02)
3. **Parameter names:** Accept current values; reject "unclassified" sentinel; normalize in A3 (F-03)
4. **percentile_basis:** Optional, deprecated (F-04)
5. **item_code + assignment_status:** Decouple code from state (F-07)
6. **PopulationCode enum:** 12 top-level + 8 sub-codes (F-08)
7. **JurisdictionCode enum:** 24 canonical + 2 meta-codes (F-09)
8. **Value validation:** Cross-field rules tied to value_type (F-10)

---

## 4. Conversion Risk Assessment

| Risk | Severity | Mitigation |
|---|---|---|
| Evidence tier string parsing | MEDIUM | Regex parser with exhaustive test against all 73 records |
| Recommendation strength normalization | MEDIUM | Mapping table; unmapped values → UNSET + warning |
| Item code sentinel replacement | LOW | Direct mapping: [UNASSIGNED]→null, [CROSS-CUTTING]→status field |
| Jurisdiction code validation | LOW | Known set; new codes rejected until added to enum |
| Qualitative spec handling | LOW | null value fields + value_type validation |

All 73 records convertible with current parser. Zero data loss expected.
