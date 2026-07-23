# DR-2026-07-23 — Retire the disability-population code schema; replace with the Access-Taxonomy Axis-2 set

- Status: **ADOPTED — owner directive 2026-07-23** ("retire existing code schema for
  disability populations to replace with these"; three gating decisions answered same day).
- Category: **D-DOCT + D-SCHEMA**, delegation **DG-NON** (population taxonomy is owner-only).
- Supersedes: `DR-2026-07-21-two-layer-functional-taxonomy` and
  `DR-2026-07-22-population-representation-reconciliation` **as to the population code scheme**
  (their slash-notation, parent-child nesting model). The `axes` layer (Layer 1) they created
  is retained and is now cross-walked from the new access-needs layer (see the access-needs
  migration 031).
- Prepared by: Claude, on owner direction, integrating the uploaded **Access Taxonomy (v0.1)**.

## Context

The prior scheme nested populations under parents via slash codes (`NDV/AUT`, `OFS/ME`) with a
`parent_code` hierarchy. The owner adopted the Access Taxonomy's **Axis 2** model: populations
grouped by **community self-organization**, **no parent codes**, no umbrella containing its
members. The taxonomy is a v0.1 draft (self-flagged "not validated with disabled people"); it
is adopted as the operative population set with that provenance recorded, and remains revisable.

## Decision — the new population set (23 codes, flat)

BLIND, DEAF, DEAFBLIND, MOB, LMB, SCI, MOVE, NDV, AUT, ADHD, ID, DEM, BRAIN, COM, PAIN, MS, EPI,
VES, MH, LPA, TALL, BAR, ALL. No parent codes; `NDV` is a selectable peer view, not a container.

**Crosswalk from the retired scheme:** VIS→BLIND, UPL→LMB, DBL→DEAFBLIND (renames);
{NEU,PCS}→BRAIN and {OFS,CFS,MCAS,POTS,LCOV}→COM (merges); SENS→NDV (fold); EXH→TALL.
New codes with no prior work: MOVE, ID, VES, LPA, TALL, BAR. Legacy free-text codes swept:
IntD→ID, ABI→BRAIN.

## Owner-gated sub-decisions (2026-07-23)

1. **`ALL`** — **kept** as a scope-marker ("applies to all populations"), not retired. The
   taxonomy has no ALL code, but the 3 populated `ALL` evidence cells + 9 links are preserved;
   migration to situational-duration expression is deferred to the access-need tagging step.
2. **`MH`** (mental health) — **kept as its own population** (distinct functional profile:
   trauma-informed design, control over environment). Not folded into NDV.
3. **Life stage (`SEN` older adults, `CHD` children)** — **orthogonal modifiers**, not
   population rows (a child or older adult can hold any access profile). Housed in the new
   `life_stage_modifiers` table.
4. **`ID`** (intellectual disability) — **first-class**, superseding the former
   "proxy IntD through DEM+NDV" rule (project-standards 2026-03-25).
5. **Body size** (`LPA`/`TALL`/`BAR`) — retained as a population group, framed as *the
   environment being wrongly normed to an average body*, served by the `A-SIZE` access need.

## Execution (this session)

- Schema migration `032_population_schema_replace.sql` — creates `life_stage_modifiers`.
- Data migration `data_20260723..._population-schema-replace.sql` — the code re-key
  (INSERT new → repoint every code-bearing column → DELETE retired). Authored as a **data**
  migration so it runs in the data phase (after all data loads) and stays rebuild-reproducible.
- `schemas/enums.py` — `PopulationCode` replaced with the 23-set; `LifeStageModifier` added.
- Verified: rebuild-reproducible (byte-parity committed vs `--rebuild`); `test_db_integrity`
  A03 (population FK) passes and **no new integrity failures** vs the pre-change baseline; 366→363
  item-links (3 genuine duplicate-merges deduped); 13 evidence cells preserved.

## Conservation & losses

No synthesis work discarded. Of 13 evidence cells: 12 unchanged, 1 renamed (NEU→BRAIN). Item
links 366→363: F-04, F-05 (→COM) and A-13 (→BRAIN) collapsed to single rows on merge (correct
dedup). On a merge collision the surviving row keeps the first-updated row's attributes.

## Deferred / follow-up (tracked, not in this change)

- **Caller sweep** of derived markdown (BPC/search-log frontmatter, `validate_items.py`
  hardcoded list, `scripts/convert/*`) from retired codes — non-gating (`validate_population.py`
  is not a CI gate); scoped as follow-up.
- Physical `DROP COLUMN parent_code` (nulled here; drop once validators stop reading it).
- `population_reclass` (held-031 scaffolding) — now obsolete; retire in a follow-up.
- Axis mappings for the new codes (MOVE/ID/VES/LPA/TALL/BAR) — re-derive.
- `governance/population-taxonomy.md` full rewrite to the community-organized model (code lists
  + supersession note updated this session; deeper reconciliation with `functional-taxonomy.md`
  is its own step).

## Alternatives rejected

- **Keep the slash/parent scheme** — rejected by owner; conflicts with the community
  self-organization principle (no umbrella owns its members).
- **Full Path-2 in one migration** (drop ALL, re-express universal specs, retire MH) — rejected;
  ALL and MH retained per decisions 1–2 to preserve populated cells and a distinct community.
