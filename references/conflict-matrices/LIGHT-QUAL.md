## Conflict Domain: LIGHT-QUAL
**Parameter:** Flicker, colour temperature
**Status:** MIXED — Opus synthesis complete [2026-03-30]
**Date created:** 2026-03-30
**Opus synthesis:** 2026-03-30
**Feeds:** Part 5 §5.2 conflict resolution table; Part 3 §3.8 decision tree

### Opposition Map (corrected from skill domain table)

The original domain table describes the opposition as "NDV/AUT: no flicker, warm ≤3000K" vs "DEM: cool daylight simulation ≥4000K." This mischaracterises the NDV/AUT position. Per NDV BPC divergent findings (2026-03-29), NDV/AUT prefers **consistent 4000K (no dynamic shift)**, not warm ≤3000K. The NDV/MH population prefers dynamic CCT (4000K day → 2700K evening) for circadian support.

Corrected opposition map:

| Sub-parameter | Populations | Need | Evidence |
|---|---|---|---|
| **Flicker** | NDV/AUT, NDV/SENS, NEU, PAIN | Elimination of all flicker (fluorescent, stroboscopic, PWM dimming) | ● NDV BPC; PAS 6463:2022; NDV-AUT thresholds BPC |
| **Flicker** | ALL other populations | No population benefits from flicker; neutral-to-negative | — |
| **CCT — daytime** | DEM | Cool daylight ≥4000K for circadian stimulus (melanopic EDI ≥250) | ● Circadian BPC: Brown et al. 2022; DIN/TS 67600:2022 |
| **CCT — daytime** | NDV/AUT | Consistent 4000K; predictability; no dynamic shift | ● NDV BPC divergent findings |
| **CCT — daytime** | VIS (low vision) | Cooler light improves contrast perception | ● VIS BPC |
| **CCT — evening** | DEM, NDV/MH | Warm shift (≤3000K evening) for circadian support | ● Circadian BPC: Brown et al. 2022 (≤10 melanopic EDI evening) |
| **CCT — evening** | NDV/AUT | No automated shift; predictability preferred | ● NDV BPC: predictability > circadian support |

### Domain Classification: MIXED

**Flicker sub-parameter: CONVERGENT**
Universal elimination of flicker serves all populations. No population requires or benefits from flicker. This is a genuine Tier 0 universal specification. Specify: no fluorescent sources (T8, T12, CFL); LED sources with flicker index ≤0.05 and flicker percentage ≤5%; no visible PWM dimming.

**CCT daytime sub-parameter: CONVERGENT**
DEM (≥4000K circadian), NDV/AUT (consistent 4000K), and VIS (cooler light for contrast) all align on daytime ≥4000K. No conflict during occupied daytime hours.

**CCT transition/evening sub-parameter: DIVERGENT**
The genuine conflict is between **automated dynamic CCT** (which DEM and NDV/MH need for circadian entrainment) and **static predictable CCT** (which NDV/AUT needs for environmental predictability). This is not a conflict about the CCT value itself — both populations can accept 4000K during daytime. The conflict is about whether the lighting system changes state autonomously.

### Resolution Evidence

**Resolution 1 — User-controlled vs automated CCT programmes:**
- In NDV/AUT-designated spaces: user-selectable CCT (manual control, no automatic shifting). User can choose warm or cool, but the system does not change without user action. H-02 individual control.
- In DEM-designated spaces: automated circadian CCT programme (4000K+ daytime → 2700K evening, per Brown et al. 2022 thresholds). Automation is clinically necessary because DEM users cannot be expected to self-manage circadian exposure.
- Evidence: Circadian BPC resolution note — "resolve via individual dimming control (B-06, H-02); daytime circadian stimulus delivered via diffuse/indirect lighting (B-07) to avoid glare triggers."
- Status: **RESOLVED-CONSENSUS** (for spaces serving a single population type)

**Resolution 2 — Shared spaces (DEM + NDV/AUT co-occurrence):**
- The automation-vs-predictability conflict is irreconcilable in a single ambient system serving both populations simultaneously.
- Resolution: temporal or spatial zoning.
  - **Spatial:** DEM-primary zones (dining, lounge, corridors) use automated circadian programme. NDV/AUT-primary zones (sensory rooms, bedrooms, quiet areas) use manual control with predictable defaults.
  - **Temporal:** In aged care facilities where NDV/AUT and DEM residents co-occur, circadian programme governs ambient lighting (harm asymmetry: circadian disruption causes measurable health deterioration for DEM; static CCT causes discomfort but not measurable harm for NDV/AUT). NDV/AUT residents have individual control in personal spaces.
- Harm asymmetry: DEM circadian disruption → increased agitation, sleep-wake cycle deterioration, medication burden. NDV/AUT CCT shift exposure → discomfort, anxiety, but manageable via predictable scheduling + personal space retreat. DEM harm > NDV/AUT harm → circadian programme as default in shared ambient spaces.
- Status: **RESOLUTION-PROPOSED** (harm asymmetry logic is sound but untested in co-occurrence settings)

**Resolution 3 — Graduated transition:**
- Where automated CCT programmes operate: transition rate ≤50K/hour. No step-changes. NDV/AUT sensitivity is to SUDDEN change, not to gradual drift. Predictable, gradual transitions may be tolerable.
- Evidence: NDV/AUT BPC — "predictability" is the core need, not static-ness per se. A perfectly predictable, slow, clock-synchronised transition may satisfy predictability requirements.
- Status: **RESOLUTION-PROPOSED** (clinical plausibility, no direct evidence)

### Guidebook Specification Implications

| Specification | Tier | Note |
|---|---|---|
| Flicker elimination (all sources) | Tier 0 | Universal. No conflicts. |
| Daytime CCT ≥4000K in all primary occupied spaces | Tier 0 | Convergent across DEM, NDV/AUT, VIS |
| Automated circadian CCT programme in DEM-designated spaces | Tier 1 (DEM) | B-01/B-06 specification |
| Manual CCT control in NDV/AUT-designated spaces | Tier 1 (NDV/AUT) | H-02 cross-reference |
| Shared spaces: circadian programme as default + graduated transition ≤50K/hr | Tier 1 (harm asymmetry) | Part 5 §5.2 conflict entry |
| Personal spaces: individual CCT control regardless of population | Tier 2 | H-02 universal |

### Unresolved Gaps

| Gap ID | Description | Priority |
|---|---|---|
| GAP-CONF-LQUAL-01 | No evidence on NDV/AUT tolerance of graduated CCT transitions (≤50K/hr). Resolution 3 is clinical plausibility only. | P3 |
| GAP-CONF-LQUAL-02 | No co-occurrence facility POE measuring circadian programme impact on NDV/AUT residents in aged care. | P2 |

### Connection Register Updates
| Entry | Update |
|---|---|
| CON-0038 (circadian multi-population) | CONSUMED → LIGHT-QUAL Resolution 2 |

---
*Cross-population-conflict-mapper LIGHT-QUAL domain. Opus synthesis 2026-03-30. Classification: MIXED (flicker convergent; daytime CCT convergent; evening CCT divergent). Original domain table corrected: NDV/AUT position is consistent 4000K, not warm ≤3000K.*
