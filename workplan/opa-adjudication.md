# OP-A: Part 5 §5.2 Conflict Resolution Table Adjudication
**Generated:** 2026-04-03
**Model:** Opus 4.6

## Entry-by-Entry Adjudication

### 1. COLOUR-CONT (VIS/DEM vs NDV)
- **Resolution status:** RESOLVED-EVIDENCE — **CORRECT**
- **Governing provision:** VIS safety-critical (fall prevention) — **CORRECT** (DSDC 2024: +15% pattern-associated falls is Tier 3 safety evidence)
- **Strategy:** SRW + SZ — **CORRECT**
- **BPC consistency:** Matches BPC conflict #1 and #9. Values (≥30 LRV primary, ≤20 LRV Zone 3) consistent.
- **Higher-ambition resolution available?** No. This is the correct resolution.

### 2. ACOUSTIC-LVL (DEAF vs NDV)
- **Resolution status:** RESOLVED-CONSENSUS — **CORRECT**
- **Governing provision:** DEAF safety-critical (fire evacuation context, though primary domain is speech access) — **ACCEPTABLE** but note: the acoustic conflict is primarily about speech intelligibility, not fire evacuation. The safety-critical classification applies to the fire alarm strobe conflict (SURFACE-TEXT worked example in §3.8), not to the hearing loop conflict itself.
- **Strategy:** TS — **CORRECT** (independent audio input to loop)
- **BPC consistency:** Matches deaf-acoustic BPC (IEC 60118-4 loop zones) and conflict BPC #2.
- **Correction:** RT60 ≤0.3 s is stated as universal. The deaf-acoustic BPC confirms ≤0.4 s for DEAF; the NDV BPC confirms ≤0.3 s for NDV. The neurodivergent BPC Opus synthesis explicitly states "where NDV and DEAF share the same space, the stricter NDV target governs." This means ≤0.3 s is correct as the governing value, but the rationale should state "NDV governs (stricter subset)" not "universal." **MINOR CORRECTION NEEDED.**

### 3. GRAB-BAR DIAMETER (MOB vs UPL)
- **Resolution status:** RESOLVED-EVIDENCE — **CORRECT**
- **Strategy:** RS (Range Specification) — **CORRECT** (now has a code per OPG-05)
- **BPC consistency:** Matches BPC #3. Guay 2020 correctly cited.

### 4. TEMP-RANGE (NEU/MS vs PAIN)
- **Resolution status:** RESOLVED-CONSENSUS — **SHOULD BE RESOLVED-EVIDENCE**
- **Correction:** Uhthoff's mechanism has Tier 1 clinical evidence (Davis 2010 neurophysiology). The ms-thermal BPC classifies this as safety-critical with Tier 2-4 evidence. The resolution IS evidence-based (safety-critical provision governs), not merely consensus. Change status to RESOLVED-EVIDENCE.
- **Strategy:** SRW + IEC — **CORRECT**
- **BPC consistency:** Matches ms-thermal BPC and conflict BPC #4.

### 5. SURFACE-TEXT (VIS vs PAIN/MOB)
- **Resolution status:** PARTIAL — **CORRECT**
- **BPC consistency:** Matches conflict BPC #5. Residual gap (no product meets both profiles) correctly identified.

### 6. SPATIAL-OPEN (DEAF vs NDV)
- **Resolution status:** RESOLVED-CONSENSUS — **CORRECT**
- **Strategy:** SZ — **CORRECT**
- **BPC consistency:** Not in original BPC 9 — this is a §5.2 addition. Resolution is well-grounded in DeafSpace 2010 and PAS 6463.

### 7. LIGHT-INT (DEM/VIS vs NDV/OFS)
- **Resolution status:** RESOLVED-CONSENSUS — **CORRECT** (could be RESOLVED-EVIDENCE given Brown 2022 Tier 1 consensus)
- **Strategy:** SZ + IEC — **CORRECT**
- **Consistency:** Three-zone model aligns with F-01 sensory gradient.

### 8. VIS-COMPLEX (DEM/IntD vs NDV)
- **Resolution status:** RESOLVED-CONSENSUS — **CORRECT**
- **Strategy:** PP (unlabelled — per OPG-02, should be tagged) — **MINOR**

### 9. MOVE-FREE (DEM vs MOB)
- **Resolution status:** RESOLVED-CONSENSUS (residential) / TIER-2-ONLY (institutional) — **CORRECT**
- **Strategy:** SZ + OT-REF — **CORRECT**
- **BPC consistency:** Not in original BPC 9. Resolution is sound.

### 10. FRAGRANCE (OFS vs DEM)
- **Resolution status:** PARTIAL — **CORRECT**
- **Strategy:** PP (partial) — **CORRECT**
- **Residual gap correctly identified:** Synthetic lavender contraindicated for OFS/MCAS; natural food smells acceptable.

### 11. DOOR-OPERATION (MOB vs NDV/MH)
- **Resolution status:** RESOLVED-CONSENSUS — **CORRECT**
- **Strategy:** TS — **CORRECT**
- **BPC consistency:** Matches conflict BPC #7.

## §5.3 Unresolvable Conflicts

### CONF-UNRESOLV-01 (ambient temperature in shared sleeping)
**ADJUDICATION: CORRECT.** The residual case (non-zoned shared sleeping space) is genuinely irresolvable at Tier 1. The mitigations (insulated grab bars, warm bedding, individual heated throw) are appropriate OT-mediated solutions. Correctly flagged as Tier 2.

### CONF-UNRESOLV-02 (acoustic amplification in shared open-plan)
**ADJUDICATION: CORRECT.** The Auracast technology note is appropriate — personal receiver resolves the technology path but doesn't eliminate the ambient access right. Correctly flagged as Tier 2.

### CONF-UNRESOLV-03 (visual glazing DEAF vs DEM/NDV)
**ADJUDICATION: CORRECT.** The dimensional compromise (clear upper band >1400mm for signing; frosted lower band for DEM/NDV) is the best available mitigation. Correctly noted as "dimensional compromise, not evidence-based resolution."

**Are these three genuinely irresolvable?** Yes. Each represents a case where the underlying physiological mechanisms are directly opposed and no architectural solution can satisfy both simultaneously in a shared non-zoned space.

## Corrections to Apply

| # | Severity | Action |
|---|---|---|
| OPA-01 | MEDIUM | §5.2 TEMP-RANGE: Change status from RESOLVED-CONSENSUS to RESOLVED-EVIDENCE (Uhthoff's has Tier 1 clinical evidence) |
| OPA-02 | LOW | §5.2 ACOUSTIC-LVL: Add note "RT60 ≤0.3 s: NDV governs as stricter subset of DEAF ≤0.4 s target" |
| OPA-03 | LOW | All §5.2 entries: Add strategy codes per OPG-04 (deferred to SONNET-A) |
| OPA-04 | MEDIUM | Add BPC conflict #6 (acoustic differentiation VIS vs DEM) as 12th §5.2 entry (deferred to SONNET-A — requires item spec content) |
