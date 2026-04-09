# FDR Compound-Interaction Audit Methodology
**Reference document for functional-deficit-researcher §11.1 and connection-scout Step 2b**
**Date:** 2026-04-09 05:30
**Status:** ACTIVE

---

## 1. Purpose

Systematically identify which FDR findings interact non-additively when co-occurring in a single person. This is distinct from connection-scout's standard cross-population scan (which finds shared solutions across populations) and from Part 5's conflict resolution (which resolves inter-group conflicts in shared spaces). The compound-interaction audit operates at the intra-individual level.

---

## 2. Input Requirements

For each compound scenario in fdr-slug-registry-v2.md §C:
1. Both constituent constraints must have COMPLETE individual FDR findings (granular scenarios already run).
2. The individual FDR findings must contain extractable spatial parameters (not GAP results).
3. The compound scenario's environment context must be specified.

If requirement 1 is not met: run the missing granular scenario first. Compound audit requires both inputs.

---

## 3. Audit Protocol

### Step 1: Parameter extraction from individual findings

For each constituent constraint (A and B), list all spatial parameters with their values and conditions from the relevant FDR file(s).

Example (CMP-01):
- Constraint A (hemiplegia): affected-side vertical bar, 5cm from WC edge, 70-140cm height (FDR-BAB-01)
- Constraint B (chronic pain): pain-side avoidance during loading; seated rest between transfer phases

### Step 2: Interaction classification

For each parameter pair (one from A, one from B), classify:

| Classification | Definition | Action |
|---|---|---|
| INDEPENDENT | Parameters operate on different physical variables with no functional interaction | No compound entry needed |
| CONVERGENT | Parameters point in the same direction through different mechanisms | Specify the convergent requirement; note dual evidence basis |
| ANTAGONISTIC | Parameter A assumes a capacity that condition B impairs, or vice versa | COMPOUND-INTERACTION connection; Tier 2 routing |
| CONDITIONAL | Parameters are compatible under some conditions but not others | Document conditions; Tier 2 resolves which conditions apply to individual |

### Step 3: Mechanism documentation

For ANTAGONISTIC and CONDITIONAL interactions, document:

```yaml
compound_scenario: "{CMP-ID}"
parameter_A: "{parameter from constraint A}"
parameter_B: "{parameter from constraint B}"
interaction_type: "ANTAGONISTIC | CONDITIONAL"
mechanism: "{1-2 sentence clinical reasoning for why A and B interact}"
assumption_violated: "{what assumption does one constraint make that the other invalidates?}"
tier2_resolution: "{what the OT determines — e.g., transfer approach, device selection, spatial arrangement}"
```

### Step 4: Output

- INDEPENDENT + CONVERGENT pairs: no further action. Log as "audited, no compound interaction."
- ANTAGONISTIC pairs: create COMPOUND-INTERACTION connection entry. Route to ISW with compound-synthesis brief.
- CONDITIONAL pairs: create COMPOUND-INTERACTION connection entry with conditions documented. Route to ISW with conditional specification template.

### Step 5: Specification limit check

If the audit identifies a compound where NO environmental specification can resolve the interaction (both population's wayfinding systems depend on faculties the other condition impairs — CMP-04 pattern):
- Document as SPECIFICATION-LIMIT.
- Flag for Part 1 §1.9 Scope: the guidebook's environmental specification capacity has a boundary here.
- Recommend: human assistance provision (Part 9 §9.9 OT collaboration protocol).

---

## 4. Diminishing Return Gate

If 3 consecutive compound scenarios within the same environment context produce only INDEPENDENT or CONVERGENT classifications: stop auditing that environment. The compound interactions in that context are not architecturally significant.

---

## 5. Token Budget

- Compound audit: count as 1x per compound scenario (lighter than search, since both inputs already exist).
- Maximum: 8 compound audits per session.
- ANTAGONISTIC findings require Opus synthesis for ISW brief.

---

## 6. Integration Points

| Output | Destination |
|---|---|
| COMPOUND-INTERACTION connections | connection-scout _index.md + topic file |
| ISW compound-synthesis briefs | item-specification-writer queue |
| SPECIFICATION-LIMIT flags | Part 1 §1.9 Scope; gap_register.md |
| CONVERGENT findings | FDR file annotation (strengthens evidence for converging spec) |
