# DR-2026-07-22 — Population-representation reconciliation: one canonical code set across enum, DB, and the axis layer

- Status: **PROPOSED — pending owner ratification.** States and does not execute
  (posture per `DR-2026-07-21-product-posture-thinking-tool-not-authority`). No enum,
  DB row, or migration changes with this commit; it lays out the reconciliation and
  its forks for ratification. The rename/add migration is written **after** the
  enum-addition decisions below are ratified (same sequencing the taxonomy used:
  DR ratified → migration executed).
- Date: 2026-07-22
- Category: **D-SCHEMA** (enum / canonical code set) + a bug-fix component (enum↔DB
  drift). Enum changes are owner-gated per `governance/population-taxonomy.md` §5.
- Prepared by: Claude, on owner directive 2026-07-22 ("Yes" — lay out the
  reconciliation of the parallel population representations surfaced after the
  functional-taxonomy migration 030 landed).
- Affects (if ratified): `schemas/enums.py` `PopulationCode`; the DB `populations`
  table + `item_population_links` + `population_axis_map` (code alignment);
  `governance/population-taxonomy.md` (documents the reconciled set + the two-table
  layering); `population_reclass` (the `(proposed)` suffixes cleared on ratification).
- Related: `DR-2026-07-21-two-layer-functional-taxonomy` (v1.2; created the axis layer
  and `population_reclass`); `governance/functional-taxonomy.md` §1 (named the
  three-representation divergence as a reconciliation item); `governance/population-
  taxonomy.md` §5 (the enum-change process this DR follows).

## Context — what migration 030 left, and the drift it exposed

The taxonomy migration was **additive**: it created `axes` / `population_reclass` /
`population_axis_map` alongside the untouched `populations`, `slugs`, and `items`
tables. Nothing was re-done. But standing the new layer next to the old surfaced a
**pre-existing drift** the additive work did not cause:

`schemas/enums.py PopulationCode` — the *declared* single source of truth
(`population-taxonomy.md` §5) — uses **slash notation** (`NDV/AUT`, `OFS/ME`,
`NEU/PCS`; and it already contains `CHD/LPA/EXH/BAR`). The DB `populations` table
drifted to **flat** names (`AUT`, `CFS`, `PCS`). So the DB has been violating its own
canonical enum — the "schema↔DB drift is a bug, not a convention" gotcha, now
concrete for the population layer. Three misalignments:

1. **Naming drift (a bug fix — targets already canonical).** 9 flat DB codes whose
   slash forms already exist in the enum: `AUT→NDV/AUT`, `ADHD→NDV/ADHD`,
   `SENS→NDV/SENS`, `CFS→OFS/ME`, `POTS→OFS/POTS`, `MCAS→OFS/MCAS`, `PCS→NEU/PCS`,
   `MH→NDV/MH`, `UPL→MOB/UPL`. Aligning these is *fixing a bug*, not a new decision.
2. **New codes not yet in the enum (owner-gated D-SCHEMA).** `MOB/SCI`, `NEU/MS`,
   `NEU/EPI` (taxonomy-proposed sub-codes; currently flat `SCI`/`MS`/`EPI` in the DB)
   + the 3 new profiles `OAD`, `VES`, `LCOV`.
3. **Enum has, `populations` lacks.** `CHD/LPA/EXH/BAR` — in the enum + in
   `population_reclass`, but absent from the `populations` table (they live only in
   the Supplementary Volume today).

The full rename map is already recorded in `population_reclass.canonical_code`.

## Decision — the canonical structure (proposed)

**There is no new canonical to invent; align everything to the enum that is already
declared canonical.** The reconciled model is a clear separation of roles — not two
competing identity tables:

| Role | Home | Notes |
|---|---|---|
| **Canonical code definition** | `schemas/enums.py PopulationCode` + `governance/population-taxonomy.md` | slash notation; the validator's source of truth |
| **Profile identity (Layer 2 data)** | `populations` table | display_name, category, parent_code — **aligned to the enum** |
| **Profile → axis disposition (bridge)** | `population_reclass` | alias/profile/qualifier, mapping-confidence, emergent corpus |
| **Functional dimensions (Layer 1)** | `axes` | the new canonical for *functional* retrieval |
| **Links** | `item_population_links` (profile→item), `population_axis_map` (profile→axis), `item_axis_links` (item→axis, pending E3) | |

`population_reclass` is **not** a competing population table — it is the disposition
bridge. This DR formalizes that so future sessions don't read the two as rivals.

### Recommendation, in two sequenced layers

- **Bucket A — bug-fix alignment (recommended, not really a fork).** Rename the 9
  drifted DB codes to their already-canonical slash forms; carry the links (below).
  This just makes the DB obey the enum it already declares canonical.
- **Bucket B — enum additions (owner-gated D-SCHEMA, the real decisions).** Add
  `MOB/SCI`, `NEU/MS`, `NEU/EPI`, `OAD`, `VES`, `LCOV` to the enum; promote
  `CHD/LPA/EXH/BAR` into the `populations` table (they are already enum-valid).
  Clear the `(proposed)` suffixes in `population_reclass` on ratification.

### PCS is a rename + an add, not a destructive split

`PCS` (post-concussion, 20 item links) → **`NEU/PCS`** (carries all 20 links — the
canonical code already exists). The post-COVID content is a **new** profile `LCOV`
(0 existing links). So the "split" is non-destructive: an existing rename that keeps
its evidence + a green-field addition.

## Link carryover (how existing work carries over — nothing is lost)

- `item_population_links` (366 total): the renamed codes carry their links by
  `UPDATE population_code` — SCI(26)→MOB/SCI, PCS(20)→NEU/PCS, AUT(19)→NDV/AUT,
  CFS(2)→OFS/ME, MS(2)→NEU/MS, ADHD(1)→NDV/ADHD, EPI(1)→NEU/EPI, MCAS(1)→OFS/MCAS,
  POTS(1)→OFS/POTS, plus UPL/MH/SENS where present. ~73 rows updated, 0 dropped.
- `population_axis_map` (69): same rename applied so the axis mappings keep pointing
  at the right profiles.
- New profiles (OAD/VES/LCOV) and promoted archetypes (CHD/LPA/EXH/BAR) start with
  no item links — correct; they are new or supplementary-sourced.
- `slugs`, `items` (A–K), `search_coverage`, `evidence_sources`: **untouched** — none
  keys on these population codes. (Slug↔population is derived, per the taxonomy's
  `serves_axes` model; the one-slug-one-population rule is unaffected.)

## Alternatives rejected

- **Relax the enum to flat codes** (make the enum match the drifted DB). Rejected: it
  discards the parent-encoding the slash notation carries, contradicts the enum's
  existing design and the `CHD/LPA/EXH/BAR` entries already there, and rewrites the
  *canonical* to match a *bug*.
- **Make `population_reclass` the single population table** (deprecate `populations`).
  Rejected for now: it would re-key 366 `item_population_links` and every
  `schemas/*.py` reference — a large rip-and-replace against the additive-preservation
  ethos. The two-table split (identity + disposition) is cleaner and keeps all
  existing FKs intact. Revisit only if the split proves confusing in practice.
- **Do nothing** — leaves the DB violating its canonical enum and two population
  representations reading as rivals; blocks clean E2/E3 (annotations would attach to
  drifted codes and be redone).

## Consequences if ratified

The DB conforms to its own canonical enum; there is one code set across enum, DB,
governance doc, and the axis layer; E2 (`serves_axes`) and E3 (item↔axis harvest) then
attach to correct canonical codes instead of being done against drifted ones and
redone. Cost: one migration (renames + adds + link carryover, deterministic,
reproducibility-verified like 030) + the `schemas/enums.py` edit + a
`population-taxonomy.md` update. No existing research is discarded; ~73 links are
re-pointed, 0 dropped.

## Explicitly not decided here

The `axes` register itself (ratified separately); E3 harvest scope; whether
`CHD/LPA/EXH/BAR` gain main-taxonomy matrix columns (they stay supplementary-scoped
unless a separate DR promotes them — this DR only adds them to the `populations`
table as valid profiles); any change to `item_population_links` semantics beyond the
code rename.

## Ratification checklist (owner)

1. **Bucket A** — confirm aligning the 9 drifted DB codes to their canonical slash
   forms (the bug fix). Recommended.
2. **Bucket B** — approve the enum additions (D-SCHEMA): `MOB/SCI`, `NEU/MS`,
   `NEU/EPI`, `OAD`, `VES`, `LCOV`; and adding `CHD/LPA/EXH/BAR` to `populations`.
3. Confirm the canonical-structure table (enum+governance = definition; `populations`
   = identity; `population_reclass` = disposition bridge; `axes` = Layer-1).
4. Confirm PCS→NEU/PCS (carries 20 links) + new LCOV.
5. On ratification: I write the deterministic rename/add migration (`031_*`), apply +
   reproducibility-verify (as with 030), edit `schemas/enums.py` +
   `population-taxonomy.md`, and clear the `(proposed)` suffixes. **Then** E2/E3 run
   against the reconciled codes.
