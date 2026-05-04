# OP-G: Part 3 §3.8/3.9 Methodology Review
**Generated:** 2026-04-03 05:27
**Model:** Opus 4.6

## 1. §3.7 ↔ §3.8 Internal Consistency

§3.7 has 6 steps. §3.8 decision tree operationalises the same 6 steps. Mapping:

| §3.7 Step | §3.8 Node | Consistent? |
|---|---|---|
| Step 1: Identify conflict type (INTRA/INTER/BOTH) | Step 1: Conflict classification | YES |
| Step 2: Safety-critical check | Step 2: Safety-criticality check | YES |
| Step 3: Evidence-tier comparison | Step 3: Evidence-tier comparison | YES — §3.7 says "most constrained" but §3.8 Step 3 says "evidence-tier comparison." §3.7 Step 3 is actually about constraint, not evidence. |
| Step 4: Range specification test | Step 5: Range or zone test | **ORDERING MISMATCH** — §3.7 puts range at Step 4; §3.8 puts constraint at Step 4 and range/zone at Step 5 |
| Step 5: Zoning test | Step 5: Range or zone test (combined) | §3.7 separates range (Step 4) and zone (Step 5); §3.8 combines them as Step 5 |
| Step 6: Irresolvable | Step 6: Irresolvable | YES |

**Finding OPG-01 (MEDIUM):** §3.7 Step 3 says "most constrained" and Step 4 says "range." §3.8 inserts "evidence-tier comparison" at Step 3 and "constraint comparison" at Step 4. The logic is equivalent but the numbering diverges. §3.7 has: safety → constraint → range → zone → irresolvable. §3.8 has: safety → evidence tier → constraint → range/zone → irresolvable. The evidence-tier step is an addition in §3.8 not present in §3.7.

**Correction required:** Add evidence-tier comparison to §3.7 as Step 3, renumbering constraint to Step 4. Or: remove Step 3 from §3.8 and merge evidence-tier into the safety-criticality check (Step 2). The BPC resolution hierarchy lists evidence tier at position 2, consistent with §3.8 but not §3.7.

## 2. §3.8 → §5.2 Conflict Resolution Verification

For each of the 11 §5.2 entries, I apply §3.8 and check whether the tree produces the stated resolution.

| §5.2 Domain | §3.8 Path | §5.2 Resolution | Tree produces same? | Notes |
|---|---|---|---|---|
| COLOUR-CONT | Step 1: INTER-GROUP → Step 2: VIS safety-critical (fall prevention) → VIS governs primary routes → Step 5: zone resolves NDV in Zone 3 | Zone-based: ≥30 LRV primary; ≤20 LRV Zone 3 | YES | Tree correctly produces safety-governs + zoning |
| ACOUSTIC-LVL | Step 1: INTER-GROUP → Step 2: DEAF safety-critical (fire evacuation) → DEAF governs → Step 5: TS separates loop audio from broadcast | Loop with independent audio; RT60 ≤0.3 s universal | YES | TS strategy correctly applied |
| GRAB-BAR | Step 1: INTER-GROUP → Step 5: Range 32-45mm serves both | Range specification | YES | §3.8 Step 5 range branch |
| TEMP-RANGE | Step 1: BOTH → Step 2: NEU/MS safety-critical (Uhthoff's) → SRW governs | ≤18°C ambient + individual radiant | YES | SRW correctly applied |
| SURFACE-TEXT | Step 1: INTER-GROUP → Step 2: VIS safety-critical → VIS governs primary → PARTIAL for secondary (compromise) | ISO 23599 primary; flush edging secondary | YES | Status correctly marked PARTIAL |
| SPATIAL-OPEN | Step 1: INTER-GROUP → Step 5: Zone (graduated model) | Open spine + enclosed sub-zones | YES | SZ strategy |
| LIGHT-INT | Step 1: BOTH → Step 2: Neither exclusively safety-critical → Step 3: DEM circadian has Tier 3 evidence; NDV has Tier 5 → DEM governs → Step 5: Zone (three-zone model) | Three-zone illuminance + individual dimming | YES | Evidence tier + zoning |
| VIS-COMPLEX | Step 1: INTER-GROUP → Step 5: Design solution (pictogram system serves both) | Pictogram + matte sign field | **PARTIAL** | Not a classic tree resolution — it's a design synthesis. Tree doesn't have a "both served by same design" branch. This is closest to PP (Plain Provision) but not labelled as such. |
| MOVE-FREE | Step 1: INTER-GROUP (residential) / BOTH (institutional) → Step 2: Both safety-critical (falls for MOB; autonomy for DEM) → Step 5: Zone (garden loop with handrails) | Resolved residential; Tier 2 institutional | YES | Correctly splits by setting |
| FRAGRANCE | Step 1: INTER-GROUP → Step 2: OFS/MCAS safety-critical (anaphylaxis risk with severe MCAS) → F-06 governs → residual DEM accommodation via natural scents | F-06 baseline; natural food smells for DEM | **PARTIAL** | Status correctly marked PARTIAL. Tree would produce RESOLVED if OFS/MCAS is classified safety-critical, but §5.2 marks it PARTIAL because DEM olfactory cueing remains compromised. |
| DOOR-OPERATION | Step 1: INTER-GROUP → Step 5: TS (separate requirements served by combined spec) | Automatic with advance warning | YES | Combined specification serves both |

**Finding OPG-02 (LOW):** VIS-COMPLEX resolution is not cleanly derivable from §3.8 tree. The resolution is a design synthesis ("pictogram system serves both") rather than a hierarchy resolution. The tree lacks a branch for "design both populations' needs into a single specification element." This is closest to PP (Plain Provision) or T0 (Universal Mode Universal) in §3.9 but neither code is applied in §5.2 for this entry. Minor gap — the resolution is correct; the tree path is ambiguous.

**Finding OPG-03 (LOW):** FRAGRANCE resolution path depends on whether OFS/MCAS chemical sensitivity is classified as safety-critical. Severe MCAS can produce anaphylaxis (safety-critical). Mild chemical sensitivity is comfort-level. §5.2 does not distinguish severity — it applies F-06 as baseline, which is the correct practical outcome regardless of safety classification. No correction needed.

## 3. §3.9 Strategy Code Completeness

Strategies in §3.9: IEC, SZ, TS, DAR, SRW, PP, T0, OT-REF (8 strategies).

Strategy codes actually used in §5.2 resolution descriptions (implicit — §5.2 does not use short codes):

| §5.2 Domain | Strategy actually applied | §3.9 code |
|---|---|---|
| COLOUR-CONT | Safety governs + zoning | SRW + SZ |
| ACOUSTIC-LVL | Technical separation (independent loop audio) | TS |
| GRAB-BAR | Range specification | **NO CODE** |
| TEMP-RANGE | Safety rule wins + individual supplement | SRW + IEC |
| SURFACE-TEXT | Safety governs primary; compromise secondary | SRW (partial) |
| SPATIAL-OPEN | Sensory gradient zoning | SZ |
| LIGHT-INT | Zoning + individual control | SZ + IEC |
| VIS-COMPLEX | Design synthesis serving both | PP or T0 (unlabelled) |
| MOVE-FREE | Zoning (outdoor) + OT referral (institutional) | SZ + OT-REF |
| FRAGRANCE | Policy provision + architectural adjacency | PP (partial) |
| DOOR-OPERATION | Technical separation (combined spec) | TS |

**Finding OPG-04 (MEDIUM):** §5.2 does not use §3.9 strategy codes explicitly. Each resolution should be tagged with its governing strategy code(s) to make the connection between methodology (§3.9) and application (§5.2) explicit.

**Finding OPG-05 (MEDIUM):** "Range specification" is a resolution strategy used in §5.2 (GRAB-BAR) and described in §3.7 Step 4, but it does not have a short code in §3.9. Add: **RS — Range Specification.** "Where a parameter value range satisfies both populations' evidence basis, specify the range."

## 4. §3.11 Worked Examples → §3.8 Consistency

Five worked examples in §3.11. Checking each:

| Example | Populations | §3.8 applied correctly? | Notes |
|---|---|---|---|
| WE1: Memory Care | DEM+MOB+MOB/WC | YES | Loop plan = T0; door = TS; circadian = IEC; grab bars = T0; plain floor = PP. All derivable from tree. |
| WE2: NDV/OFS Co-Working | NDV+DEAF+OFS | YES | Loop audio = TS; pods = SZ; dimming = IEC; fragrance-free = PP/T0. |
| WE3: Primary School | NDV+MOB+DEAF | YES | Quiet room = T0; RT60 ≤0.3 = NDV governs (stricter); visual alarm = TS (vibrotactile supplement). |
| WE4: Hospital Ward | MOB+DEM+NEU+OFS | YES | TEMP-RANGE = SRW correctly applied. Plain floor = PP. |
| WE5: Supported Housing | MOB+DEM+NDV/MH+OFS | YES | Individual thermostats = IEC at apartment level. Loop plan. |

All five worked examples produce decisions consistent with §3.8 tree and §3.9 strategies. No inconsistencies found.

## 5. §5.4 Worked Examples → §3.8 Consistency

Three worked examples in §5.4. Checking:

| Example | Active conflicts | §3.8 applied correctly? | Notes |
|---|---|---|---|
| §5.4.1: DEM Care Home | COLOUR-CONT, LIGHT-INT, MOVE-FREE, FRAGRANCE | YES | Each resolution matches §5.2 entry. Design stage actions logically follow. |
| §5.4.2: NDV Co-Working | ACOUSTIC-LVL, SPATIAL-OPEN, LIGHT-INT, FRAGRANCE | YES | Loop/pod layout = TS+SZ. Individual dimming = IEC. |
| §5.4.3: Supported Housing | TEMP-RANGE, DOOR-OPERATION, COLOUR-CONT, MOVE-FREE | YES | ≤18°C ambient + individual = SRW+IEC correctly applied. |

All three §5.4 examples are consistent with §5.2 table and §3.8 tree.

## 6. Cross-Population-Conflict-Resolutions BPC → §5.2 Consistency

BPC lists 9 resolved conflicts. §5.2 has 11 entries. Mapping:

| BPC # | §5.2 Domain | Consistent? |
|---|---|---|
| 1. Visual contrast | COLOUR-CONT | YES — values match |
| 2. Hearing loop vs NDV | ACOUSTIC-LVL | YES — same resolution |
| 3. Grab bar diameter | GRAB-BAR | YES — 32-45mm |
| 4. Temperature | TEMP-RANGE | YES — ≤18°C + individual |
| 5. Tactile indicators | SURFACE-TEXT | YES — ISO 23599 primary |
| 6. Acoustic diff. | **NOT IN §5.2** | **MISSING** |
| 7. Automatic doors | DOOR-OPERATION | YES |
| 8. Nature/planting | **NOT IN §5.2** | **MISSING** |
| 9. Floor pattern | **MERGED INTO COLOUR-CONT** | Partially — §5.2 mentions plain floor within COLOUR-CONT |
| N/A | SPATIAL-OPEN | Not in BPC 9 | **ADDITION** |
| N/A | LIGHT-INT | Not in BPC 9 | **ADDITION** |
| N/A | VIS-COMPLEX | Not in BPC 9 | **ADDITION** |
| N/A | MOVE-FREE | Not in BPC 9 | **ADDITION** |
| N/A | FRAGRANCE | Not in BPC 9 | **ADDITION** |

**Finding OPG-06 (MEDIUM):** Two BPC conflict resolutions are absent from §5.2:
- **BPC #6: Acoustic differentiation (VIS navigation vs DEM sensory calm)** — 200-300mm hard floor strip at junctions for VIS acoustic cue; NRC ≥0.70 panels within 2m for DEM. This is a legitimate conflict with an evidence-based resolution that should be in §5.2.
- **BPC #8: Nature/planting (VIS vs DEM/MH)** — interior planting ≥600mm from circulation; species with clear contrast. This may be too minor for §5.2 but is a documented conflict.

**Finding OPG-07 (LOW):** §5.2 has 5 domains not in the original BPC 9 (SPATIAL-OPEN, LIGHT-INT, VIS-COMPLEX, MOVE-FREE, FRAGRANCE). These are additions from the Phase 3 writing. They are consistent with the BPC evidence and the resolution hierarchy. No issue — §5.2 correctly extends beyond the BPC.

## Summary of Corrections Required

| ID | Severity | Location | Action |
|---|---|---|---|
| OPG-01 | MEDIUM | Part 3 §3.7 | Add evidence-tier comparison step (currently only in §3.8 but not §3.7). Renumber §3.7 steps to match §3.8: 1=classify, 2=safety, 3=evidence tier, 4=constraint, 5=range/zone, 6=irresolvable |
| OPG-04 | MEDIUM | Part 5 §5.2 | Add §3.9 strategy codes to each resolution (e.g. "Resolution: SRW + SZ — ...") |
| OPG-05 | MEDIUM | Part 3 §3.9 | Add RS (Range Specification) as 9th strategy code |
| OPG-06 | MEDIUM | Part 5 §5.2 | Add acoustic differentiation conflict (BPC #6) and consider nature/planting (#8) |
| OPG-02 | LOW | Part 5 §5.2 VIS-COMPLEX | Tag with PP or T0 strategy code |
| OPG-03 | LOW | None | No action — FRAGRANCE resolution is correct |
| OPG-07 | LOW | None | No action — §5.2 additions are valid |
