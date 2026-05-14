# B2.5 Field Population Report
**Date:** 2026-05-04
**Model:** Opus 4.6
**Input:** 73 records in specification-database.json

## Coverage

| Field | Populated | Total | Source |
|---|---|---|---|
| question_heading | 62 | 73 | data/question-headings.yaml |
| summary | 67 | 73 | BPC "Most inclusive provision" or "Consensus findings" |
| conflict_domains | 21 | 73 | references/website/data/conflicts.json |
| dar_relevant | 56 | 73 | Part 6 item code extraction |
| structural_backing_required | 8 | 73 | Part 4 + Part 8 structural blocking references |
| person_specific_note | 11 | 73 | Renamed from tier_2_note (73/73 renamed) |
| curation_status | 73 | 73 | Set to "automated" |

## Field gaps

- **question_heading (11 missing):** Records with item_code = [CROSS-CUTTING] or [UNASSIGNED] — no matching entry in question-headings.yaml. Requires ISW item_code assignment first.
- **summary (6 missing):** BPC files without "Most inclusive provision" or "Consensus findings" sections (stubs or framework files).
- **conflict_domains (52 missing):** Only 26 unique item codes appear in conflicts.json specifications_involved arrays. Remaining items have no documented cross-population conflicts — this is expected for items where populations agree.
- **dar_relevant (17 false):** Items not referenced in Part 6 DAR sections. May need manual review — some may be DAR-relevant but not yet tagged in Part 6 prose.
- **structural_backing_required (65 false):** Only items with explicit "structural backing/blocking" keyword proximity in Part 4/8. Conservative extraction — may undercount. Full audit at C-stage.

## Additional changes

- `tier_2_note` renamed to `person_specific_note` (73/73)
- `recommendation_strength` sentinel values normalized to `UNSET`
- `_meta.field_population_date` set to 2026-05-04
- `_meta.amendment_1_fields_added` set to true
- 15 new null fields initialized for future population (question_summary, evidence_summary, why_md, schedule_md, diagram_svg, diagram_type, dar_note, retrofit_category, ot_evidence_basis, failures_json, install_notes_json, detail_groups_json, pop_reasons_json, topics_json)
