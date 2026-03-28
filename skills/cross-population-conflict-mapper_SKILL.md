---
name: cross-population-conflict-mapper
description: >
  Systematically identify and map where population-specific accessibility guidelines
  produce opposing specifications when applied to the same space. Searches by
  CONFLICT DOMAIN (environmental parameter) rather than population pair. Retrieves
  resolution evidence from fragmented single-population literatures that do not
  cross-reference each other. Outputs a conflict matrix with resolution status
  and evidence quality. ALWAYS use this skill when: writing Tier 0 or Tier 1
  specifications for shared spaces; item-specification-writer encounters a space
  serving multiple populations; sensory-coherence-checker finds an unresolved conflict
  needing evidence; connection-scout identifies a cross-population tension; any
  specification mentions "adjustable", "zoned", or "user-controlled" without documenting
  which populations conflict. Trigger on: "cross-population conflict", "competing
  access needs", "accommodation conflict", "which populations conflict here",
  "do these specs oppose", "conflict matrix", "resolution evidence for conflict",
  "opposing requirements", "conflicting disability needs". Phase 2B–3 skill.
---

**Model:** Sonnet 4.6 (retrieval/collation) · Opus 4.6 (resolution synthesis + best-practice determination)
**Input:** Environmental parameter(s) OR item specification draft OR room type
**Output:** Conflict domain matrix + resolution evidence register + unresolved gap flags
**Chunk ceiling:** ≤3 conflict domains per run

---

## 1. Conflict Domains

The finite set of environmental parameters where cross-population conflicts occur.
Search by domain — not by population pair.

| Domain | Parameter | Pop A need | Pop B need | Opposition |
|---|---|---|---|---|
| LIGHT-INT | Illuminance (lux) | DEM: bright circadian (≥300 lux task) | NDV/AUT, NEU, PAIN, OFS: dim, controllable (≤200 lux ambient) | Direct |
| LIGHT-QUAL | Flicker, colour temp | NDV/AUT: no flicker, warm (≤3000K) | DEM: cool daylight simulation (≥4000K) | Direct |
| VIS-COMPLEX | Signage density, pattern | DEM, IntD: high redundancy, pictograms, colour coding | NDV/SENS: minimal visual clutter, muted palette | Direct |
| SPATIAL-OPEN | Sightlines, enclosure | DEAF: open, transparent, 360° visual reach | NDV/AUT: compartmentalised, enclosed, predictable | Direct |
| ACOUSTIC-LVL | Background noise, amplification | DEAF: amplified speech, hearing loops, low reverberation | NDV/SENS, NEU: quiet, low stimulation, no amplification | Direct |
| SURFACE-TEXT | Floor/path texture | VIS, DBL: tactile differentiation, detectable warnings | MOB: smooth traversal, minimal resistance | Partial (resolved: truncated dome sizing) |
| MOVE-FREE | Autonomous movement | DEM: wandering, freedom of circulation | MOB (fall risk): supervised, contained paths | Partial |
| CORRIDOR-W | Corridor/path width | DEAF: wide (≥2400 mm for signing pairs) | NDV/AUT: narrow (reduced sensory exposure) | Partial |
| COLOUR-CONT | LRV contrast levels | VIS, DEM: high contrast (≥30 LRV diff) everywhere | NDV/SENS: muted, low contrast | Partial |
| TEMP-RANGE | Temperature (°C) | OFS/POTS: cool (18–20°C); NEU/MS: cool (Uhthoff's) | PAIN/fibro: warm (22–24°C); MOB (spasticity): warm | Direct |
| PREDICT | Spatial predictability | NDV/AUT, DEM: fixed layout, no reconfiguration | MOB: flexible, reconfigurable for equipment access | Tension |
| FRAGRANCE | Chemical/olfactory | NDV/SENS, OFS/MCAS: zero fragrance | DEM (olfactory therapy): scented cues for orientation | Tension |

---

## 2. Execution Protocol

### Step 1: Identify active domains

From the input (item spec, room type, or explicit domain list):
- List all population codes the space must serve
- For each domain in §1, check if ≥2 populations with opposing needs are present
- Active domains = those with ≥1 opposition

### Step 2: Search for resolution evidence

For each active domain, search in this order:

**Priority 1 — Existing project evidence:**
- `references/bpc/` per-slug files for relevant populations
- `sensory-coherence-checker` known conflict patterns (§3)
- `references/connection-register.md` for PENDING connections

**Priority 2 — Aged care / dementia facility POEs:**
Aged care populations co-occur DEM + MOB + VIS + DEAF by default.
Search: `{domain parameter} dementia care facility evaluation conflict`

**Priority 3 — Single-population design guidelines:**
Retrieve opposing specifications from each population's guideline set.
Key sources per population:
- DEM: Dementia Services Development Centre (Stirling); HBN/HTM; Hogeweyk evaluations
- DEAF: Gallaudet DeafSpace Guidelines (2010); PAS 6463:2022
- NDV/AUT: ASPECTSS (Mostafa 2014); PAS 6463:2022; Enabling Spaces
- VIS: RNIB guidance; ISO 21542; ADAAG detectable warnings
- MOB: ISO 21542; BS 8300; ADAAG
- OFS: limited — functional deficit research primary source
- PAIN: limited — OT CPGs primary source

**Priority 4 — Built project case studies:**
Search: `{domain parameter} post-occupancy evaluation disability accommodation`
Weight: dementia villages > neurodivergent housing > inclusive schools > public buildings

### Step 3: Classify resolution status

For each active conflict:

| Status | Definition |
|---|---|
| RESOLVED-EVIDENCE | Published resolution with outcome data (e.g., truncated dome sizing) |
| RESOLVED-CONSENSUS | Expert/standards consensus without outcome data (e.g., zoned lighting) |
| RESOLUTION-PROPOSED | Resolution exists in guidelines but untested (e.g., adjustable everything) |
| UNRESOLVED | No resolution found; populations cannot share identical specification |
| TIER-2-ONLY | Conflict irreconcilable at Tier 0–1; requires individual co-design |

### Step 4: Output conflict matrix

```markdown
## Cross-Population Conflict Matrix — [scope]
**Date:** YYYY-MM-DD HH:MM
**Space/Item:** [identifier]
**Populations served:** [codes]

### Active Conflicts

| Domain | Pop A | Pop B | A spec | B spec | Resolution | Status | Evidence |
|---|---|---|---|---|---|---|---|
| | | | | | | | ● ◐ ○ |

### Resolution Evidence Register

For each RESOLVED or RESOLUTION-PROPOSED conflict:
- Source(s) with citation
- Resolution mechanism
- Outcome data (if any)
- Guidebook implication (Tier 0 default, Tier 1 range, Tier 2 requirement)

### Unresolved Conflicts → Gap Register

For each UNRESOLVED or TIER-2-ONLY conflict:
- Gap ID (format: GAP-CONF-{DOMAIN}-{NN})
- Populations affected
- Specification implication
- Research needed
```

---

## 3. Resolution Patterns

Known resolution archetypes (apply where evidence supports):

| Pattern | Mechanism | Applicable when |
|---|---|---|
| **Zoning** | Spatial separation of conflicting parameters | Space is large enough to differentiate zones |
| **Adjustable** | User-controlled parameter | Individual can operate controls; not DEM or IntD without support |
| **Temporal** | Time-based alternation | Populations use space at different times |
| **Graduated** | Transition zones between opposing states | Adjacent spaces with gradual parameter change |
| **Layered** | Multiple modalities serving same function | Information via visual + tactile + auditory redundantly |
| **Tier escalation** | Irreconcilable at Tier 0; resolved at Tier 1–2 | Populations identified; co-design available |
| **Dimensional** | Parameter optimised at intersection of acceptable ranges | Ranges overlap even if optima differ |

**CRITICAL:** "Adjustable" is not a universal resolution. It fails when:
- The user cannot operate controls (DEM late stage, IntD without support)
- The parameter is shared ambient (you cannot dim lights for one person in an open room)
- Adjustment requires disclosure of disability

---

## 4. Interdependencies

**Feeds FROM:**
- `item-specification-writer` (item specs requiring conflict check)
- `sensory-coherence-checker` (unresolved conflicts needing evidence)
- `connection-scout` (cross-population tensions discovered)
- `content-gap-analyzer` (population coverage revealing conflict)
- `multilingual-research` / `functional-deficit-researcher` (population-specific evidence)

**Feeds INTO:**
- `item-specification-writer` (conflict matrix informs spec ranges and DAR)
- `sensory-coherence-checker` (pre-populates known conflicts for Phase 5 QA)
- `gap_register.md` (unresolved conflicts as typed gaps: CONF)
- `connection-register.md` (conflict resolutions as connections)
- Part 8 §8.4 (conflict resolution guidance)

**Preceded by:** Population-specific BPC research for relevant populations
**Followed by:** Item specification writing with conflict-aware ranges

---

## 5. Model Assignment

- **Sonnet:** All retrieval, collation, search, and matrix assembly
- **Opus:** Resolution synthesis — determining whether a proposed resolution genuinely serves both populations or merely privileges one. Opus adjudicates when "adjustable" is a real resolution vs. a handwave. All `Resolution` column content in the conflict matrix requires Opus determination.

---

## 6. Constraints

1. Never assume "adjustable" resolves a conflict without evidence that both populations can operate the adjustment
2. Never delete a conflict because one population is smaller — all populations have equal standing per CRPD Art. 4.3
3. Always check whether a proposed resolution for Pop A creates a NEW conflict for Pop C
4. SURFACE-TEXT (VIS ↔ MOB) is the only domain with a fully evidence-based resolution (truncated dome sizing per JIS/ISO). All other domains have weaker evidence.
5. Dementia village literature is the richest source for cross-population conflict evidence because residents co-occur DEM + MOB + VIS + DEAF
6. Do not search by population pair (55 pairs). Search by conflict domain (12 domains).
