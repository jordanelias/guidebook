## Cross-Domain Synthesis — Three Priority Conflict Domains
**Date:** 2026-03-29 01:40
**Domains completed:** LIGHT-INT, ACOUSTIC-LVL, SPATIAL-OPEN
**Feeds:** Part 5 §5.2 (conflict resolution guidance), Part 3 §3.8 (decision tree)

### Domain Classification

The three domains reveal a critical structural distinction the guidebook must make explicit:

| Domain | Classification | Tier 0 viable? | Key mechanism |
|---|---|---|---|
| LIGHT-INT | **DIVERGENT** | No — cannot specify single lux | Shared ipRGC pathway serves opposing clinical objectives; harm asymmetry favours dim default |
| ACOUSTIC-LVL | **CONVERGENT** | Yes — strictest target serves all | DEAF ≤ 0.3 s RT60 is strict subset containing all other populations' targets |
| SPATIAL-OPEN | **MIXED** | Partial — aligned parameters + zoned divergent parameters | Predictability/sightlines converge; openness/enclosure diverge; prospect-refuge zoning resolves |

### Implication for §5.2

Part 5 §5.2 must distinguish between:

1. **Convergent domains** — where the strictest population-specific target serves all populations. These produce genuine Tier 0 universal specifications. The guidebook can state a single value. Example: RT60 ≤ 0.3 s.

2. **Divergent domains** — where population-specific targets are mechanistically irreconcilable. These cannot produce a single Tier 0 value. The guidebook specifies zoning infrastructure + harm-asymmetry default + individual control. Example: illuminance (shared ipRGC pathway).

3. **Mixed domains** — where some sub-parameters converge and others diverge. The guidebook specifies universal values for convergent sub-parameters and zoning for divergent ones. Example: spatial predictability (universal) + openness/enclosure (zoned).

### Implication for §3.8 Decision Tree

The architect's decision tree at §3.8 should ask:

1. **Is the environmental parameter convergent or divergent for the populations present?**
   - If convergent → adopt strictest target (serves all, excludes none)
   - If divergent → proceed to step 2

2. **For divergent parameters: is individual control feasible?**
   - If yes AND all populations can operate control → individual control (H-02)
   - If yes BUT some populations cannot operate → individual control + staff/carer protocol
   - If no (shared ambient parameter) → proceed to step 3

3. **For shared ambient divergent parameters: is spatial zoning feasible?**
   - If yes → zone with graduated transition (≥3 m) + equivalent functional access in all zones
   - If no (single room, too small to zone) → proceed to step 4

4. **For unzoneable divergent parameters:**
   - Apply harm-asymmetry default (the population that experiences pain/harm takes priority over the population that experiences reduced benefit)
   - Flag as Tier 2 — OT assessment required for individual resolution
   - DAR: design for future adaptation when population changes

### Skill Findings and Corrections

1. **CORRIDOR-W domain** should be removed from the conflict table or reclassified. The NDV/AUT "narrow" preference is a mischaracterisation. The actual NDV need (low visual complexity, predictability) is compatible with DEAF wide corridors (≥2440 mm). Width and sensory load are independent variables.

2. **"Adjustable" audit:** All three domains confirm the skill's constraint — "adjustable" fails for DEM late stage, IntD without support, and shared ambient parameters. The guidebook must specify operability per population for every "adjustable" specification.

3. **Intra-individual conflicts** (NEU/MH/OFS in LIGHT-INT; DEAF+NDV/AUT in SPATIAL-OPEN) are not resolvable by architectural design alone. They require OT assessment at Tier 2. The guidebook's role is to provide the specification range and framework; the clinician resolves the individual.

### Gap Register Summary

| Domain | New gaps | P1 | P2 |
|---|---|---|---|
| LIGHT-INT | 4 (GAP-CONF-LIGHT-01–04) | 1 (LIGHT-04: DEM late-stage + photosensitivity) | 3 |
| ACOUSTIC-LVL | 2 (GAP-CONF-ACOU-01–02) | 0 | 2 |
| SPATIAL-OPEN | 3 (GAP-CONF-SPAT-01–03) | 0 | 3 |
| **Total** | **9** | **1** | **8** |

### Connection Register Updates Needed

The following connection register entries should be updated to CONSUMED or annotated:

| Entry | Update |
|---|---|
| CON-0016 (zone-parameter model) | CONSUMED → LIGHT-INT matrix Resolution 1 |
| CON-0005 (H-02 as Tier 0) | Referenced in LIGHT-INT Resolution 2; ACOUSTIC-LVL aligned parameters |
| CON-0030 (glazed junction conflict) | CONSUMED → SPATIAL-OPEN matrix Resolution 2 |
| CON-0037 (prospect-refuge) | CONSUMED → SPATIAL-OPEN matrix Resolution 1 |
| CON-0038 (circadian multi-population) | Referenced in LIGHT-INT opposition map |

---
*First execution of cross-population-conflict-mapper skill. Three domains completed. Nine gaps added. Convergent/divergent/mixed classification framework established.*
