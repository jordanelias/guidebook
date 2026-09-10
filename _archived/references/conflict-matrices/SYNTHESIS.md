## Cross-Domain Synthesis — All 12 Conflict Domains
**Date:** 2026-03-30 (Opus session — supersedes 2026-03-29 three-domain synthesis)
**Domains completed:** All 12
**Feeds:** Part 5 §5.2 (conflict resolution guidance), Part 3 §3.8 (decision tree), Part 4 specifications

### Domain Classification Summary

| Domain | Classification | Universal Mode viable? | Key finding |
|---|---|---|---|
| LIGHT-INT | **DIVERGENT** | No | Shared ipRGC pathway serves opposing clinical objectives; harm asymmetry favours dim default |
| LIGHT-QUAL | **MIXED** | Yes (flicker + daytime CCT) | Flicker convergent; daytime CCT convergent (all align ~4000K); evening CCT divergent (dynamic vs static). Original table corrected: NDV/AUT = 4000K, not ≤3000K. |
| ACOUSTIC-LVL | **CONVERGENT** | Yes | DEAF ≤ 0.3 s RT60 is strict subset containing all populations' targets |
| SPATIAL-OPEN | **MIXED** | Partial | Predictability/sightlines converge; openness/enclosure diverge; prospect-refuge zoning resolves |
| SURFACE-TEXT | **CONVERGENT** | Yes | Pre-resolved: truncated dome sizing per JIS/ISO serves VIS + MOB |
| VIS-COMPLEX | **RESOLVED-CONSENSUS** | Yes | 3D objects at decision points serve DEM while avoiding NDV/SENS clutter triggers. Strongest resolution. |
| CORRIDOR-W | **RECLASSIFIED — NOT A CONFLICT** | N/A | Width and sensory load are independent variables. Domain retired. |
| COLOUR-CONT | **MIXED (largely compatible)** | Yes (LRV contrast) | LRV contrast and chroma are independent variables. High LRV contrast achievable in muted palette. Only colour coding chroma shows partial conflict — resolved via desaturated hues + 3D object primacy. |
| TEMP-RANGE | **DIVERGENT** | No | Most mechanistically irreconcilable conflict. Cool ambient + individual supplemental heating (harm asymmetry). |
| FRAGRANCE | **MINIMAL CONFLICT** | Yes (near-convergent) | DEM olfactory wayfinding claim unsupported as built environment spec. Fragrance-free is near-universal. |
| MOVE-FREE | **DIVERGENT but RESOLVED** | Partial | Containment-based care model rejected per CRPD. Safe free movement via loop design + hazard elimination resolves apparent conflict. |
| PREDICT | **MIXED (largely compatible)** | Yes | MOB needs adequate fixed space, not reconfiguration. Reconfiguration is a workaround for inadequate room sizing. |

### Structural Findings

**1. Three domains reclassified or retired:**
- CORRIDOR-W: not a conflict (width ≠ sensory load)
- FRAGRANCE: minimal conflict (DEM olfactory wayfinding is clinical care, not architectural specification)
- COLOUR-CONT partially reclassified: LRV contrast ≠ chroma; the "contrast conflict" was a variable conflation

**2. Convergent/Divergent/Mixed framework confirmed:**
The three-way classification from the original synthesis (LIGHT-INT, ACOUSTIC-LVL, SPATIAL-OPEN) holds across all domains. The §3.8 decision tree should ask:
1. Is the parameter convergent? → Adopt strictest target (serves all)
2. Is the parameter divergent? → Individual control feasible? → Zoning feasible? → Harm asymmetry default
3. Is it mixed? → Convergent sub-parameters get Universal Mode; divergent sub-parameters get zoning/control

**3. "Adjustable" is confirmed as an inadequate universal resolution:**
Every domain confirms the skill's constraint. "Adjustable" fails when:
- User cannot operate controls (DEM late stage, IntD without support)
- Parameter is shared ambient (cannot zone lighting in a single small room)
- Adjustment requires disability disclosure

Every "adjustable" specification must include: (1) populations who can self-adjust, (2) populations requiring carer/staff operation, (3) default setting when no individual present with harm-asymmetry rationale.

**4. Variable conflation is the most common false conflict:**
Three domains (CORRIDOR-W, COLOUR-CONT, PREDICT) had apparent conflicts that dissolved under analysis because two independent variables were being treated as one:
- Width ≠ sensory load (CORRIDOR-W)
- LRV contrast ≠ chroma (COLOUR-CONT)
- Adequate space ≠ reconfiguration (PREDICT)

The guidebook should systematically check for variable conflation before asserting a cross-population conflict.

**5. Harm asymmetry governs divergent domain defaults:**
Where no single specification serves all populations, the default favours the population that experiences greater harm:
- LIGHT-INT: dim default (NDV/AUT/NEU pain > DEM reduced circadian benefit)
- TEMP-RANGE: cool default (NEU/MS neurological deterioration > PAIN discomfort)
- MOVE-FREE: free movement (CRPD rights > safety paternalism)

### Gap Register Summary (all domains)

| Domain | Gaps | P1 | P2 | P3 |
|---|---|---|---|---|
| LIGHT-INT | 4 (GAP-CONF-LIGHT-01–04) | 1 | 3 | 0 |
| LIGHT-QUAL | 2 (GAP-CONF-LQUAL-01–02) | 0 | 1 | 1 |
| ACOUSTIC-LVL | 2 (GAP-CONF-ACOU-01–02) | 0 | 2 | 0 |
| SPATIAL-OPEN | 3 (GAP-CONF-SPAT-01–03) | 0 | 3 | 0 |
| SURFACE-TEXT | 0 | 0 | 0 | 0 |
| VIS-COMPLEX | 1 (GAP-CONF-VCOMP-01) | 0 | 0 | 1 |
| CORRIDOR-W | 0 (retired) | 0 | 0 | 0 |
| COLOUR-CONT | 1 (GAP-CONF-CCONT-01) | 0 | 0 | 1 |
| TEMP-RANGE | 3 (GAP-CONF-TEMP-01–03) | 0 | 2 | 1 |
| FRAGRANCE | 0 | 0 | 0 | 0 |
| MOVE-FREE | 1 (GAP-CONF-MOVE-01) | 0 | 0 | 1 |
| PREDICT | 1 (GAP-CONF-PRED-01) | 0 | 0 | 1 |
| **Total** | **18** | **1** | **11** | **6** |

### Connection Register Updates Needed

| Entry | Update |
|---|---|
| CON-0016 (zone-parameter model) | CONSUMED → LIGHT-INT matrix Resolution 1 |
| CON-0005 (H-02 as Universal Mode) | Referenced in LIGHT-INT, LIGHT-QUAL, TEMP-RANGE |
| CON-0030 (glazed junction conflict) | CONSUMED → SPATIAL-OPEN matrix Resolution 2 |
| CON-0037 (prospect-refuge) | CONSUMED → SPATIAL-OPEN matrix Resolution 1 |
| CON-0038 (circadian multi-population) | CONSUMED → LIGHT-QUAL Resolution 2 |

### Implication for §5.2 (updated)

Part 5 §5.2 must present:

1. **Convergent domains** (ACOUSTIC-LVL, SURFACE-TEXT, flicker elimination, daytime CCT, pattern elimination, fragrance elimination) — strictest target serves all. Single Universal Mode value.

2. **Divergent domains** (LIGHT-INT, TEMP-RANGE, evening CCT, SPATIAL-OPEN openness) — no single value possible. Specify: zoning infrastructure + harm-asymmetry default + individual control. Operability audit required.

3. **Resolved domains** (VIS-COMPLEX, COLOUR-CONT chroma, MOVE-FREE, PREDICT) — apparent conflicts that dissolve under correct variable analysis or evidence-based design. Document the resolution, not the conflict.

4. **Retired domain** (CORRIDOR-W) — do not list as a conflict.

5. **Near-convergent domain** (FRAGRANCE) — treat as universal elimination.

### Implication for §3.8 Decision Tree (updated)

Step 0 (new): **Is this a genuine conflict or a variable conflation?** Check whether the two "opposing" needs actually operate on the same variable. If independent variables (width vs sensory load; LRV vs chroma; space vs reconfigurability) → specify both independently. No conflict.

Steps 1–4: unchanged from original synthesis.

---
*Full cross-population-conflict-mapper execution complete. 12 domains analysed: 3 convergent, 3 divergent (1 architecturally resolved), 4 mixed, 1 retired, 1 minimal. 18 gaps identified (1 P1, 11 P2, 6 P3). Original domain table requires 4 corrections (CORRIDOR-W retirement, LIGHT-QUAL NDV/AUT CCT, COLOUR-CONT variable conflation, FRAGRANCE DEM claim). Opus 4.6 synthesis 2026-03-30.*
