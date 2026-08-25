# Wave H — scope for review. NOT EXECUTED.

Owner ruling 2026-08-25: *scope it, don't execute*. Nothing below has been applied; `data/guidebook.db`
is untouched. This is the review surface before any migration.

## The rule being executed

`workplan/2026-08-20-provenance-walk-execution-plan.md:405` — **"An item name states *what is being
specified*, never *what the specification is*. The embedded values are unevidenced claims and must be
treated as such: extracted as leads, and the names reduced to their parameter."**

Ruled repeatedly: 2026-07-12 (verify-and-register or purge, E-08 specifically), 2026-08-15 (owner
decisions Group 4, "the 28 item names that state their own answers"), 2026-08-19
(`instrument.md` §1.2 names `site/specs/` as the second vector; §1.4 rule 2 "no value crosses").
Recorded undone at `workplan/2026-08-22-master-execution-plan.md:307`.

## Correction to the plan's own cost estimate

The provenance-walk plan calls this *"a sweep, not an edit… touches item identity across
`item_population_links`, `item_axis_links`, `term_item_links`"*. **Measured: it does not.** All 14
tables that reference `items` key on `item_code`:

```
item_audit_runs · item_population_elaborations · item_population_links · item_bpc_links
specifications · jurisdictional_values · economics_entry_specs · case_study_specs
source_value_extractions · spec_value_probes · term_item_links · item_axis_links
room_items · conflicts          — every one FK'd on items(item_code), none on items(name)
```

So renaming breaks **no referential integrity**. It is a one-column data migration plus a
regeneration of derived surfaces. The identity concern is real for *readers*, not for the schema.

## The three tests, re-measured today

| Test | Count | What it catches |
|---|---:|---|
| A — numeric value | 21 | `≥1200 mm`, `NRC ≥0.85`, `1:20` — matches the 2026-08-21 measurement exactly |
| B — prescriptive clause only | 20 | `Where Full Passenger Lift Not Achievable`, `Graduated from Arrival…` |
| C — either (wide net) | 41 | instrument §1.1 says 42 and calls it a floor; my test is one narrower |

Overlap of A and B: 6.

## The list

`LEAD` = the value to extract into `search_candidates` before stripping (§1.4 rule 2, and the
operative consequence's "extracted as leads"). `JUDGEMENT` = the whole name is a prescription;
reducing it needs a decision about what the parameter even is.

| Item | Current name | Proposed reduced name | Class |
|---|---|---|---|
| `A-02` | Acoustic Ceiling Panels (NRC ≥0.85) in Occupied Spaces | Acoustic Ceiling Panels in Occupied Spaces | **LEAD** |
| `A-03` | Acoustic Door (STC ≥35) at All Sensitive Space Boundaries | Acoustic Door at All Sensitive Space Boundaries | **LEAD** |
| `A-04` | Acoustic Zoning: Graduated from Arrival to Primary Occupation | — | JUDGEMENT |
| `A-05` | Carpet in Corridors and Occupied Spaces (Where VIS Navigation Maintained) | — | JUDGEMENT |
| `A-06` | Fabric Wall Panels (NRC ≥0.70) at Acoustic Reflection Points | Fabric Wall Panels at Acoustic Reflection Points | **LEAD** |
| `A-07` | Flutter Echo Elimination (Parallel Hard Surface Avoidance) | — | JUDGEMENT |
| `A-08` | HVAC Noise Control (NC-25 Maximum in Sensitive Spaces) | — | JUDGEMENT |
| `A-13` | No Sound Masking in Neurological Population Environments | — | JUDGEMENT |
| `A-14` | Double-Leaf Partition (STC ≥50) for Sensitive Adjacencies | Double-Leaf Partition for Sensitive Adjacencies | **LEAD** |
| `A-16` | Sensory Room / Quiet Room Provision (≥8 m², one per floor or per 500 m² GFA) | Sensory Room / Quiet Room Provision | **LEAD** |
| `A-17` | Upholstered Seating Throughout Occupied Spaces | — | JUDGEMENT |
| `B-01` | Circadian Lighting (≥150 EML Minimum at Eye Level in Daytime Spaces) | Circadian Lighting | **LEAD** |
| `B-05` | Gradual Lighting Transition Zones (≥5 m at All Major Illuminance Changes) | Gradual Lighting Transition Zones | **LEAD** |
| `B-06` | Individual Dimming Control (≥300 Lux Range) | Individual Dimming Control | **LEAD** |
| `B-08` | Matte, Low-Reflectance Floor Finishes (≤30 Gloss Units) | Matte, Low-Reflectance Floor Finishes | **LEAD** |
| `B-10` | Visual Fire Alarm (Strobe VAD Throughout Building) | — | JUDGEMENT |
| `B-11` | Warm Colour Temperature for Evening (≤2700 K After 19:00) | Warm Colour Temperature for Evening | **LEAD** |
| `C-03` | Pattern Avoidance (Plain Flooring and Walls in Sensitive Environments) | — | JUDGEMENT |
| `C-04` | LRV Contrast (≥30 at All Critical Junctions) | LRV Contrast | **LEAD** |
| `C-06` | Plain, Low-Contrast Flooring Throughout (No Geometric Patterns) | — | JUDGEMENT |
| `D-01` | Loop Floor Plan (No Dead-End Corridors in DEM Environments) | — | JUDGEMENT |
| `D-03` | Toilet Visibility from Primary Occupied Spaces (No Navigation Required) | — | JUDGEMENT |
| `D-04` | Landmarks at Every Decision Point | — | JUDGEMENT |
| `D-07` | No Blind Corners (Curved or Mirrored at All Hidden Junctions) | — | JUDGEMENT |
| `D-08` | Pictogram + Single-Word Signage Throughout | — | JUDGEMENT |
| `D-09` | Consistent Furniture Layout (No Rearrangement Without User Consultation) | — | JUDGEMENT |
| `D-11` | Safe Accessible Garden (Loop Path, Secured Perimeter, Seating Every 20 m) | — | JUDGEMENT |
| `E-01` | Accessible Lift (1400×1100 mm Car, All Floors Served) | Accessible Lift | **LEAD** |
| `E-02` | Platform Lift (Where Full Passenger Lift Not Achievable) | — | JUDGEMENT |
| `E-03` | Ramp Gradient (≤1:20 — MS Fatigue and Temporal Accessibility) | Ramp Gradient | **LEAD** |
| `E-04` | Accessible Parking (3600 mm Width, Covered, Closest to Entry) | Accessible Parking | **LEAD** |
| `E-05` | Weather Protection at Entry (Covered Canopy Minimum 3000×2000 mm) | Weather Protection at Entry | **LEAD** |
| `E-07` | Slip Resistance (PTV ≥36 Wet Throughout All Circulation and Entry) | Slip Resistance | **LEAD** |
| `E-08` | Corridor Clear Width (≥1200 mm Minimum on All Primary Routes) | Corridor Clear Width | **LEAD** |
| `F-03` | Graduated Stimulation Re-entry (Sensory Room to General Space Transition) | — | JUDGEMENT |
| `G-02` | Variety of Seating Types (Three Heights at Every Seating Area) | — | JUDGEMENT |
| `G-05` | Adjustable-Height Work Surfaces and Desks (650--870 mm AFF Range) | Adjustable-Height Work Surfaces and Desks | **LEAD** |
| `G-06` | Reception Counter (Accessible Height Section — 760--860 mm AFF) | Reception Counter | **LEAD** |
| `H-01` | All Controls at Accessible Height (400--1100 mm AFF, One-Fist Operable) | All Controls at Accessible Height | **LEAD** |
| `I-01` | Hardware Throughout (Lever, D-Pull, One-Hand Operable, ≤22 N) | Hardware Throughout | **LEAD** + JUDGEMENT |
| `I-02` | Kitchen (One-Handed Operation Throughout) | — | JUDGEMENT |

## Caller sweep — the real inventory

**Writers/readers of `items.name` in code (14):** `scripts/generate/spec_page.py` (renders it as the
`<h1>` at :299 — this is why deleting `site/specs/e-08.html` regenerates it), `generate_parts.py`,
`generate/population_page.py`, `db.py`, `validate_items.py`, `audit/population_integrity_audit.py`,
`audit_consolidator.py`, `tests/test_db_integrity.py`, `research/retrieval_log.py`, `verify_urls.py`,
`resolve_dois.py`, `tools/regenerate_vetting_surface.py`, `tools/evidentiary_audit.py`,
`tools/pipeline_completeness.py`.

**Rendered surfaces to regenerate:** `site/specs/` (93 pages) · `parts/v10/part04.md` ·
`index.html` (91 item-name spans) · `tools/*.html` (embedded JSON) · the vetting surface.

**Not affected:** every FK table above; `_archived/` (retains the values as reference, per §1.4
rule 2's "Item values live in `_archived/` and in reference surfaces only").

## What executing it would be

1. Extract each stripped value into `search_candidates` as a lead, with `found_under_slug` and a
   note naming the item it came from (§1.4 rule 4, provenance recorded not hidden).
2. One data migration on `items.name` via `emit_data_migration.py` → `migrate_db.py`.
3. `scripts/regenerate_derived.sh`; confirm `site/specs/e-08.html` `<h1>` no longer carries a figure.
4. Gate: `run_checks.py --changed-from origin/main`; `test_db_integrity`; render freshness.

**Open question for the owner:** Test A (21) or Test C (41)? And for the JUDGEMENT rows, what a
reduced name should say when the whole name is the prescription — e.g. `A-13 No Sound Masking in
Neurological Population Environments` has no parameter left once the prescription is removed.
