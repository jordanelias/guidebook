## cross-population-conflict-resolutions

**Updated:** 2026-05-10  **Original search:** 2026-05-10  **Evidence tier range:** Tier 1–Tier 3  **Opus synthesis:** YES [OPUS-SYNTHESIS-PROVISIONAL]
**Status:** PROVISIONAL — initial draft from BPC audit Pass 2C; covers 4 conflicts (corridor width; spatial enclosure; thermal default; lighting kelvin). Cross-population conflict registry from `synthesis-scan-2026-05-06.md` to be merged in next pass.

### Concept boundary notes
| Language | Native alias | Map | Warning |
|---|---|---|---|
| EN | cross-population conflict; harm-asymmetry resolution; broadest-benefit assessment | ✓ CLEAN | — |

### Best-practice synthesis

This BPC resolves spatial conflicts where two or more population codes have evidence-supported preferences on the same parameter. Resolution method per project-standards rule (RULE 2026-04-29 19:06 — values-based conflicts via broadest-benefit assessment; harm-asymmetry per RULE 2026-03-30 23:30):

1. Verify the conflict via Step-0 variable-conflation check (RULE 2026-03-30 23:30) — confirm the populations operate on the same physical variable.
2. If function-based (one population suffers physical harm from the wrong default): apply harm-asymmetry. Default protects higher-harm population; supplementary provision serves lower-harm population.
3. If values-based (no harm asymmetry): apply broadest-benefit assessment per evidence-methodology.md §4.

#### Conflict 1 — Corridor width: DEAF vs NDV/MH vs DEM

**Apparent conflict (per Pass 0 §F-X1):**
- DEAF Co-1/Tier 2/Tier 3 evidence (DSDG Bauman 2010; Vaughn 2018; Cloete & Rout 2025) requires ≥2440mm primary corridor width + glazed intersections for two-signer side-by-side conversation
- NDV/MH (PTSD) Tier 1 evidence (Faerden 2022; Wilson 2023) requires no ambush points, exit always visible, predictable spatial sequence
- DEM Tier 3 evidence (Marquardt & Schmieg 2009 systematic review) requires identifiable bounded compartment sections (loop plan, landmarks at decision points)

**Step-0 variable check:** the populations describe three different physical variables conflated as one:
- DEAF: corridor *cross-section width* (and intersection visibility)
- NDV/MH: *visual sightline geometry* (corner visibility from approach distance)
- DEM: *building plan topology* (loop / dead-end / bounded zones)

**Variables disambiguated, the conflict largely dissolves:**

| Population | Spatial property required | Conflict with 2440mm primary corridor + glazed intersections? |
|---|---|---|
| DEAF | Width 2440mm + glazed intersections | — (the recommendation) |
| NDV/MH (PTSD) | No ambush points + exit sightline | **No** — glazed intersections eliminate ambush; wider corridor reduces approach-distance escalation |
| DEM | Loop topology + bounded compartments + landmarks | **No** — operates at building plan level; corridor cross-section is independent |
| MOB power-WC | Two-WC passing 1525–1800mm | **No** — 2440mm exceeds requirement |
| MOB Steinfeld evidence | 2400mm 180° entire-sample swept-path | **No** — converges, not conflicts |
| OFS / PAIN | Rest seating intervals 25–30m | **No** — width-independent |

**Resolution (Universal Mode primary mixed-population corridors):**

> Primary mixed-population corridors to be ≥2440mm clear width with glazed (transparent or visually-permeable) intersections at all corridor junctions. Bounded compartmentation (residential clusters, retreat zones, sensory rooms) accessed FROM primary circulation, not within it. Loop-plan topology for DEM-populated environments preserves at building-plan level; corridor cross-section is independent of loop topology.

**Why this is not a corridor-width compromise:**
- 2440mm satisfies wheelchair-passing, two-signer conversation, and Steinfeld 2006 entire-sample 180° turning evidence simultaneously.
- Glazed intersections satisfy DEAF visual sightline AND NDV/MH anti-ambush — these are the same spatial property described from two clinical perspectives.
- DEM compartmentalisation operates at the building-plan level, not corridor cross-section.

**Residual divergence (not yet resolved):**
- Some DEM design literature recommends "single-corridor or continuous-loop floor plan" — interpretable as implying a *narrow* defined corridor. The DEM clinical evidence (Marquardt & Schmieg 2009) is about *loop topology*, not corridor narrowness. Vestigial framing assumption rather than clinical requirement. DEM BPC update owed: clarify "loop plan" ≠ "narrow corridor."
- Cost: 2440mm primary corridor uses more floor area than 1800mm. This is a Mode-P trade-off (best practice vs code floor). Cost-driven reductions are Mode-6 / Tier-7 arguments, not best-practice arguments.
- Residential applications: domestic dwellings rarely have 2440mm corridors. Resolution applies to non-residential / care / healthcare / educational settings where mixed populations are anticipated. Domestic single-occupancy → Mode S occupant-co-designed.

**Synthesis approach:** convergent (variables disambiguated; same physical recommendation satisfies all populations).

#### Conflict 2 — Thermal ambient default: PAIN vs MS / SCI / NEU

**Per RULE 2026-04-07 00:22 + RULE 2026-04-09:** PAIN (FMS) requires warmth (cold pain hypersensitivity); MS / SCI / NEU require cool ambient (Uhthoff phenomenon at >22°C; SCI tetraplegia thermoregulation impairment).

**Step-0 variable check:** same physical variable (ambient temperature). Variables not conflated.

**Harm-asymmetry analysis:**
- MS Uhthoff: neurological deterioration is irreversible / potentially permanent; recovery requires cooling and time
- SCI tetraplegia: heat stroke risk in severe cases (Tier 1 — clinical neurology evidence)
- FMS warmth-relief: pain symptom (reversible; not progressive); warmth provides relief but absence does not produce harm equivalent to MS deterioration

**Resolution (per `pain-ofs-built-environment-design.md` and `thermoregulation-built-environment.md`):**

> Default ambient temperature 18–21°C (cool default protects MS / SCI / NEU higher-harm populations). Individual local warmth provision for FMS / PAIN occupants (heated seating, radiant panel, additional clothing insulation) as supplementary provision. Where individual control is unavailable, default-cool prevails over default-warm.

**Synthesis approach:** divergent (genuine disagreement on default value); resolved by harm-asymmetry; both populations served via default + supplementary provision.

#### Conflict 3 — Spatial enclosure: DeafSpace open-plan vs NDV/SENS retreat / DEM compartmentation

**Apparent conflict (per `deaf-acoustic-built-environment.md` Opus note):** DeafSpace 2440mm + glazed = visually permeable / open spatial gestalt; NDV/SENS retreat = enclosed bounded zones; DEM compartmentation = bounded loop sections.

**Resolved via Conflict 1 above:** primary circulation is open + glazed; retreat / bounded zones are *adjacent off-corridor spaces*, not corridor functions. The "open vs bounded" frame applies to *zone type within the building*, not to the corridor itself.

**No genuine conflict** at the corridor level. Conflict at the building-plan level is resolved by zoning: primary circulation (open + glazed) + retreat zones (enclosed + acoustically-isolated) + compartments (bounded clusters).

#### Conflict 4 — Lighting Kelvin temperature: VIS / DEM warm vs DEAF / NDV cool

**[FORWARD-FLAGGED — not resolved this draft]** Multiple populations have lighting-kelvin preferences: VIS warm (3000K) for low-glare reading; DEM warm 2700–3000K for evening orientation; DEAF cool 4000–5000K for sign-language facial-expression contrast; NDV/SENS user-controllable. Resolution method: time-of-day variable lighting + user-control. To be resolved in next pass — out of scope for this draft.

### Consensus findings

| Finding | Languages with evidence | Tier |
|---|---|---|
| Variable conflation produces apparent conflicts that dissolve under disambiguation | EN | Methodological — project-standards RULE 2026-03-30 23:30 |
| Harm-asymmetry governs divergent function-based conflicts | EN, DE, NO, FR (proxied via clinical literature) | 1–3 |
| Glazed corridor intersections serve both DEAF visual sightline and NDV/MH anti-ambush | EN | Co-1 / Tier 2 (DSDG; Faerden 2022 inferred) |
| DEM loop plan operates at building-plan topology, not corridor cross-section | EN | Tier 3 (Marquardt & Schmieg 2009 reinterpreted) |

### Divergent findings

| Topic | Position A | Position B | Cause |
|---|---|---|---|
| Corridor width primary | 1800mm BS 8300 (wheelchair-passing) | 2440mm DSDG (two-signer) | Population evidence base differs (DEAF Co-1 not consulted in BS 8300 development) |
| DEM "single-corridor or continuous-loop" interpretation | Narrow defined corridor | Loop topology with any cross-section | Vestigial framing assumption in design literature; no Tier 1 evidence for narrowness specifically |

### NO-DATA / THIN

| Domain | Reason |
|---|---|
| Co-1 cross-cultural validation of 2440mm | DSDG ASL-derived; BSL/DGS/LSF/LIS/Auslan spatial grammars not measured |
| Cost-benefit Mode-P primary corridor 2440mm vs 1800mm | No published lifecycle costing |
| Loop-plan topology + 2440mm interaction with DEM cohort outcomes | No POE comparing 1800 vs 2440 within loop-plan facilities |

### Citation mining

| Source | Direction | New sources added |
|---|---|---|
| Cloete & Rout 2025 | Backward | DSDG Bauman 2010 (already in deaf-spatial-design BPC) |
| Marquardt & Schmieg 2009 | Cross-ref | Already in dementia-built-environment BPC |
| Steinfeld 2006 RESNA | Cross-ref | Pending IDeA Center 2010 publication retrieval (Pass 2B handoff) |

### Key sources

| REF-ID | Authors | Year | Title | Tier | Jurisdiction | Notes |
|---|---|---|---|---|---|---|
| XPC-01 | Bauman, H-D. | 2010 | DeafSpace Design Guidelines (Gallaudet) | Co-1 / Tier 2 | US | Cross-ref deaf-spatial-design BPC |
| XPC-02 | Cloete, M. & Rout, M. | 2025 | DeafSpace in built school environment: scoping review. *Acta Structilia* 32(2):238–263 | 3 | INT/ZA | Cross-cultural validity |
| XPC-03 | Steinfeld, E., Maisel, J. L., Feathers, D. | 2006 | Wheeled Mobility Space Requirements and Maneuvering: International Comparison. *RESNA 2006 Proceedings* | 3 | US/UK/AU/CA | 2400mm IDEA + BS8300 180° entire sample |
| XPC-04 | Marquardt, G. & Schmieg, P. | 2009 | Dementia-Friendly Architecture: Environments that Facilitate Wayfinding in Nursing Homes. *Am J Alzheimers Dis Other Demen* 24(4):333–340 | 3 | DE | Loop plan topology |
| XPC-05 | Faerden, A. et al. | 2022 | Environmental Transformations Enhancing Dignity — HERD 16(2):55–72, PMID 36567605. **Pass 2B: quasi-experimental (not RCT); staff-rated; d=2.0 unconfirmed.** | DOWNGRADED from Tier 1 → Tier 3 (quasi-experimental) | NO | GAP-279 filed |
| XPC-06 | van der Schaaf, P. et al. | 2013 | Impact of physical environment on seclusion use — BJPsych 202(2):142–149, PMID 23307922. **Pass 2B: VERIFIED (n=23,868/199 wards exact match).** | 1 | NL | Verified |
| XPC-07 | Project standards RULE 2026-04-29 19:06 | 2026 | Values-based broadest-benefit assessment | (governance) | INT | Project doctrine |
| XPC-08 | Project standards RULE 2026-03-30 23:30 | 2026 | Harm-asymmetry resolution; Step-0 variable conflation check | (governance) | INT | Project doctrine |

### Bottom-up findings

None this draft — placeholder for FDR-derived cross-pop interactions per `synthesis-scan-2026-05-06.md` (separate session).

## Metadata

```yaml
slug: cross-population-conflict-resolutions
population: ALL
last_updated: 2026-05-10
co0006_migration: true
status: PROVISIONAL
audit_provenance: bpc-audit-pass2-2026-05-10
covers: corridor-width-deaf-ndv-dem; thermal-default-pain-ms; spatial-enclosure-deafspace-retreat; (forward-flagged) lighting-kelvin
```
