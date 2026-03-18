---
name: neufert-image-analyzer
description: >
  Analyze spatial diagrams and typological figures from Neufert Architects' Data (4th Edition)
  to extract dimensional data, spatial relationships, and typological conventions for comparison
  against guidebook specifications. ALWAYS use this skill when asked to: analyze a Neufert
  figure, extract dimensions from Neufert, compare Neufert conventions with guidebook specs,
  use Neufert as a reference for spatial standards, or review Neufert typology data.
  Trigger on: "Neufert", "architects data", "typology figure", "extract dimensions from figure",
  "compare with Neufert", or when a Neufert source document is provided as input.
  Input is always an image or extracted page from the Neufert reference documents in project files.
---

**Model:** Sonnet 4.6 (vision required for diagram analysis)
**Input:** image of Neufert figure or page; task specification (what to extract and why)
**Output:** dimensional table + spatial relationship notes + comparison against guidebook item (if specified)
**Source documents:** Neufert Architects' Data 4th Edition — available as project reference files

---

## Scope Boundary

This skill extracts and interprets spatial data from Neufert for use in guidebook development. It does not:
- Treat Neufert as an accessibility standard (it is not; ADA, BS 8300, DIN 18040, etc. are standards)
- Import Neufert dimensions directly into specifications without comparison to accessibility evidence
- Replace multilingual-research for evidence-grounded specifications

Use Neufert data to:
- Identify conventional spatial allowances as a baseline for comparison
- Find cases where Neufert conventions fall short of accessibility requirements
- Provide typological context for specification items (e.g., typical kitchen layout vs. accessible kitchen layout)

---

## Steps

### 1. Figure identification
Identify: figure number · chapter · page · topic · typology (residential / non-residential / both).

### 2. Dimensional extraction
For each dimension visible in the figure:
- Label (as shown in figure, translated to English if needed)
- Value (mm preferred; convert if in cm or m)
- Whether it is a minimum, typical, or maximum value (interpret from context)
- Which user population the dimension appears to serve (if inferable)

Output as table: `Label | Value (mm) | Type (min/typ/max) | Population served (if stated) | Notes`

### 3. Spatial relationship analysis
Describe the key spatial relationships shown (e.g., clearance zones, circulation paths, adjacency requirements). Note any dimensions that imply a specific user body size or mobility assumption.

### 4. Accessibility gap assessment (if guidebook item specified)
Compare Neufert dimensions against the corresponding guidebook item specification:

| Dimension | Neufert value | Guidebook Tier 0 | Guidebook Tier 1 (range) | Gap | Action |
|---|---|---|---|---|---|

Gap codes:
- `NEUFERT-SHORT`: Neufert dimension is below guidebook minimum — flag as design risk if used uncritically
- `NEUFERT-CONSISTENT`: Within guidebook range
- `NEUFERT-EXCEEDS`: Neufert dimension exceeds guidebook specification — note as positive precedent
- `NOT-COMPARABLE`: Dimensions cover different elements

### 5. Output summary
One paragraph: what this figure shows, how it compares to accessible design requirements, and whether it is safe to use as a design reference or requires supplementary accessible design guidance.

---

## Framing rule

Never present Neufert as an accessibility authority. When Neufert dimensions fall short of accessibility requirements, state this explicitly: "The Neufert convention of [X] mm falls below the Tier 1 minimum of [Y] mm for [population]. Do not use this figure as a basis for accessible design without modification."
