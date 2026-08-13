# Wave 4 — The adjudication apparatus

**Read `00-holistic-execution-plan.md` first.** **All five items are gated on D-A.**

**Nothing here is half-built.** Every vocabulary is verified absent at HEAD —
`claim_manoeuvre`, `claim_construct`, `construct_directness`, `derived_from_cell_id`,
`derivation_rule`, `conflict_kind` return **zero hits** across `scripts/`, `schemas/`,
`governance/` and `decisions/`. They exist only in workplan documents. Each item is green-field on
a defined substrate.

---

## W4.1 — A fourth directness dimension: `construct_directness()`

### Objective
Grade whether the **measured construct** matches the **claimed construct** — the E-12 lesson:
`static_turning_circle` 1500 mm and `swept_path_dynamic` 1830 mm on the same parameter, with
`contested = 0`, and nothing in the pipeline able to see the difference.

### Substrate
The evidence side already exists: `source_value_extractions.measurement_paradigm` carries a
9-value vocabulary (`swept_path_dynamic`, `static_turning_circle`, `static_clearance`,
`anthropometric_percentile`, `instrumented_physical_measurement`, `route_metric`,
`field_observation`, `participatory_spatial`, `stated_unmeasured`). **The claim side has
nothing.**

### Steps
1. Schema migration adding to `specifications`: `claim_manoeuvre TEXT` (what manoeuvre the
   parameter is about — `pass`, `turn_180`, `transfer`) and `claim_construct TEXT CHECK (… IN
   (<the same paradigm vocabulary>))`. Mirror in `EvidenceStateRecord`.
2. `schemas/directness.py` gains Dimension 4 beside the three existing (population `:89-107`,
   value `:110-137`, scale `:147-193`): `CON_MATCH` / `CON_ADJACENT` / `CON_MISMATCH`, plus
   `construct_directness(measurement_paradigm, claim_construct)` with an explicit compatibility
   table — `static_turning_circle` vs `swept_path_dynamic` = **MISMATCH** (the E-12 pair);
   `static_clearance` vs `route_metric` = ADJACENT.
3. Extend `consolidate()` (`directness.py:207-236`, currently
   `consolidate(population_directness, value_directness_grade, scale_directness_grade,
   value_corroborated=False)`) with `construct_directness_grade: Optional[str] = None`.
   `None` = "not applicable, does not block" per the module's own convention; MISMATCH →
   `COND_DISCOUNTED`; ADJACENT → caps at DOWN-WEIGHTED via the existing rule 4.
4. Wire `assess_cell.py:201` to pass the fourth grade, with NOT_ASSESSED semantics per G2
   (`:35-38`) when the cell carries no `claim_construct`.

### Caller sweep
`consolidate(` callers: `assess_cell.py:201`, `schemas/directness.py:262`
(`directness_from_primitives`), and **8 call sites in `scripts/tests/test_directness_2_2.py:62-76`**.
A keyword-default addition keeps all of them valid — **but the tests must gain MISMATCH and
ADJACENT cases, including the None-propagation case at `:76`, or the dimension ships untested.**

### Falsifier
`contested = 1` plus the existing dimensions already capture the E-12 pair. **They do not:**
`contested` is a manual flag, set 0 in the trial, and no dimension reads paradigms at all.

### Risk
The paradigm vocabulary is extraction-side D-SCHEMA. Reusing it as `claim_construct`'s domain
couples the two enums — **a deliberate coupling; name it in the DR.**

---

## W4.2 — Device-class stratification

### Objective
Let a determination stratify by device class instead of collapsing manual / power / scooter /
bariatric into one range.

### The taxonomy constraint
**Stratify on `device_class` — an equipment property, already in the extraction schema
(manual/power/scooter/bariatric/walker/mixed) — never by coining device-population umbrellas.**
Population-taxonomy adjacency is DG-NON, and the work-from-axes rule prohibits umbrellas.

### Two shapes, and the recommendation
- **Widen the cell key** — `specifications.device_class` plus
  `UNIQUE(item_code, population_code)` → `UNIQUE(item_code, population_code, device_class)`.
  UNIQUE cannot be altered, so this is a **table rebuild** — free now at 0 rows, and only now.
- **A child table** — `cell_device_strata(specification_id FK, device_class, value_min, value_max,
  value_unit)`, keeping the cell singular.

**Recommend the child table.** It leaves the cell key untouched (14 inbound FKs on `item_code`
argue against key churn) and composes with D-A's one-value-per-judgment contract. It also touches
none of the existing consumers, where the rebuild would touch `assess_cell.py`'s insert, both
page renderers, and `test_evidence_cell_state_2_3.py:103`'s duplicate-cell assertion.

### The open sub-question this decomposition surfaces
**W4.2 depends on an extraction-to-cell provenance edge that no wave explicitly builds.** Strata
without evidence separation manufacture precision: each stratum row must trace to extractions
carrying that `device_class`, and the 7→9 boundary is exactly where the pipeline currently passes
nothing. **Surface this to the owner rather than discovering it mid-implementation.**

### Also a D-METH question
Which class governs the headline range? That is an aggregation judgment — **put it beside D-A;
do not decide it in schema.**

---

## W4.3 — Derivation lineage: `derived_from_cell_id` + `derivation_rule`

### Objective
Record when a cell's value derives from other cells, with the rule named and staleness
mechanically checkable.

### Steps
1. `ALTER TABLE specifications ADD COLUMN derived_from_cell_id INTEGER REFERENCES
   specifications(specification_id);` and `ADD COLUMN derivation_rule TEXT;` — a self-FK is legal in
   SQLite `ADD COLUMN` with a NULL default.
   **But recommend the junction from the start:** `cell_derivations(specification_id, upstream_cell_id,
   PRIMARY KEY(specification_id, upstream_cell_id))`. The corridor case — width derived from turning space
   **and** swept path — is already multi-parent, so a single-parent column is wrong on its first
   real use.
2. **Extend `derivation_sha`.** Current implementation at `assess_cell.py:277-281` hashes
   `item|population|sorted(governing_refs)::RULE_VERSION`. Extend the payload to
   `…|sorted(upstream cell derivation_shas)::RULE_VERSION` — **hashing the upstream *shas*, not
   their ids, makes staleness transitive:** an upstream re-derivation changes its sha, which
   invalidates every downstream sha without a graph walk.
3. Mirror the model; `derivation_rule` mandatory when lineage is non-empty.
4. Advisory check: no cycles, via a recursive CTE over the junction.

### The precedent for changing a sha payload
`derivation_sha` consumers include two committed migrations —
`data_20260804185632_…-derivation-sha-restamp.sql` and `…190706…-backfill.sql`. **Those prove the
house pattern: a payload change is handled by a compensating migration, never by editing
history.** A payload change is also a `rule_version` bump by definition (the determinism contract
in `assess_cell.py`'s docstring `:12`).

### Risk
Historical shas were stamped under the old payload. **The staleness check must key on
`rule_version`, comparing like with like.**

---

## W4.4 — Extend `design_obligation` to cells; curate from `AX-WHM`

### Objective
Let a cell name the access-need obligations it discharges.

### The curation source, verified live
`axes` row **`AX-WHM` — "Wheeled movement & transfer"**, mechanism *"Turning, clearance, transfer
geometry — independent and assisted"*, design domains naming `E-01/E-12`, `G-04`, turning
circles, clear widths, hoist clearances; ICF anchors b730, b710 / d465, d420, d410; status
ESTABLISHED.

### Steps
1. Junction `cell_access_needs(specification_id INTEGER NOT NULL REFERENCES specifications(specification_id),
   need_code TEXT NOT NULL REFERENCES access_needs(need_code), obligation_note TEXT,
   PRIMARY KEY(specification_id, need_code))`.
   **Not a copied prose column** — `design_obligation` stays on `access_needs`, whose 17 rows are
   the canonical obligations. **A cell links; it never re-states.**
2. **`access_needs` has no Pydantic model** (confirmed; `design_obligation` has zero `.py`
   references). **Create `schemas/access_need.py` as part of this item** — it closes a real gap.
3. If corridor work shows the 17 needs do not cover a cell — e.g. wheeled-transfer geometry
   beyond A-REACH's own span note *"Spans three axes (REA/WHM/AMB)"* — **propose the new `A-*`
   code derived from AX-WHM's mechanism text, to the owner, as DG-NON.** Never coin an umbrella.

### Risk
Two-hop redundancy (item→axis, cell→need) can drift. An advisory coherence check — the cell's
need family against the item's axes — is cheap and worth registering **with** the junction, not
after it.

---

## W4.5 — `conflict_kind` with an FK-keyed target pair

### Objective
Type the conflict register so each kind carries a properly-keyed pair.

### What the current DDL reveals (0 rows — rebuild is free)
`conflicts` has `conflict_id TEXT PK`, `item_code` FK, `domain TEXT NOT NULL`, and **`pop_a` /
`pop_b` TEXT NOT NULL with NO foreign key to `populations`.** *The conflict register cannot
currently guarantee its own parties exist.* Also `gap_id` is un-FK'd, and the `status` CHECK
still carries **`MODE-S-ONLY`** — retired vocabulary, since
`governance/evidence-architecture.md:150-156` retires Mode-S naming.

### The rebuild
```sql
CREATE TABLE conflicts_new (
    conflict_id   TEXT PRIMARY KEY,
    item_code     TEXT REFERENCES items(item_code),
    conflict_kind TEXT NOT NULL CHECK (conflict_kind IN
                    ('population_vs_population','axis_vs_axis','need_vs_need')),
    pop_a  TEXT REFERENCES populations(population_code),
    pop_b  TEXT REFERENCES populations(population_code),
    axis_a TEXT REFERENCES axes(axis_code),
    axis_b TEXT REFERENCES axes(axis_code),
    need_a TEXT REFERENCES access_needs(need_code),
    need_b TEXT REFERENCES access_needs(need_code),
    CHECK ( (conflict_kind='population_vs_population' AND pop_a IS NOT NULL AND pop_b IS NOT NULL
             AND axis_a IS NULL AND axis_b IS NULL AND need_a IS NULL AND need_b IS NULL)
         OR (conflict_kind='axis_vs_axis' AND axis_a IS NOT NULL AND axis_b IS NOT NULL
             AND pop_a IS NULL AND pop_b IS NULL AND need_a IS NULL AND need_b IS NULL)
         OR (conflict_kind='need_vs_need' AND need_a IS NOT NULL AND need_b IS NOT NULL
             AND pop_a IS NULL AND pop_b IS NULL AND axis_a IS NULL AND axis_b IS NULL) ),
    domain TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('RESOLVED-EVIDENCE','RESOLVED-CONSENSUS',
             'RESOLUTION-PROPOSED','UNRESOLVED','PERSON-MODE-ONLY')),
    resolution TEXT, evidence TEXT,
    gap_id TEXT REFERENCES gaps(gap_id),
    source_skill TEXT NOT NULL DEFAULT 'cross-population-conflict-mapper',
    created_at TEXT NOT NULL, created_by_session TEXT NOT NULL,
    updated_at TEXT NOT NULL, updated_by_session TEXT NOT NULL
);
```

**The `MODE-S-ONLY` → `PERSON-MODE-ONLY` rename inside this DDL is a D-SCHEMA enum change —
Change-Order gated.** If it is not ruled, **keep the old literal and file the rename separately**;
do not smuggle a vocabulary change inside a structural rebuild.

### Six nullable columns for three kinds is deliberate
A polymorphic `target_a`/`target_b` pair could not be FK'd — **the same ground on which W3.9
rejected Candidate A.** State the symmetry in the migration comment.

### Caller sweep
`scripts/validate_conflict.py` (quarantined, old taxonomy) and `scripts/validate_conflicts.py`
(**also quarantined** — AC-25). **Both must be updated or their quarantine notes amended in the
same commit.** Plus `references/conflict-matrices/` prose.

### Downstream
**W5.3's per-axis retirement-verdict refinement depends on this item.**

---

## Re-derivation notes

| Claim | Status |
|---|---|
| All five W4 vocabularies absent at HEAD | **CONFIRMED** — zero hits |
| Three-dimension directness model and `consolidate()` signature | **CONFIRMED** — `directness.py:19-25`, `:207-236` |
| `measurement_paradigm` / `device_class` exist extraction-side and are read by nothing | **CONFIRMED** — the stage-7 terminus finding |
| `derivation_sha` payload at `:277-281`; restamp-migration precedent | **CONFIRMED** on disk |
| `AX-WHM` row contents | **CONFIRMED** — full row read |
| `access_needs` has no Pydantic model | **CONFIRMED** |
| `conflicts` has no FK on `pop_a`/`pop_b`; `MODE-S-ONLY` is retired vocabulary still in the enum | **NEW** — recorded in no prior document |
| W4.2 needs an extraction-to-cell edge no wave builds | **NEW** — open sub-question |
| E-12 trial facts (REF-90010/90011, `contested=0`) | **CARRIED** — trial artifacts; the tables are now 0 rows, so not re-derivable |
