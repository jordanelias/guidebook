# BPC Audit — Pass 2B Citation Verification
**Date:** 2026-05-10
**Auditor model:** [MODEL-CONFLICT: system Opus 4.6 — not independently verifiable; treating as system context]
**Predecessor:** `bpc-audit-pass2-2026-05-10.md` (`9d2731e`)
**Protocol:** research-log-manager CHECK/LOG per standing rule #4

---

## Results

| # | Claim | Verdict | Detail |
|---|---|---|---|
| 2B.1 | Steinfeld 2010, n=500 | **VERIFIED** | 2010 Final Report to U.S. Access Board (Steinfeld, Paquet, D'Souza, Joseph, Maisel). Sample n≈495–500 (AWM Project). Different publication from 2006 RESNA paper (n=275). BPC should specify which publication; turning-space figures need cross-check between the two. |
| 2B.2 | van der Schaaf 2013, n=23,868 across 199 wards | **VERIFIED** | van der Schaaf et al. (2013), British Journal of Psychiatry 202(2):142–149. 199 wards, 23,868 admissions of 14,834 unique patients. Note: n=23,868 is admissions, not unique patients. "Private space per patient" effect confirmed (reduced seclusion risk). |
| 2B.3 | Faerden 2022, Cohen's d = 2.0 patient support RCT | **PARTIALLY VERIFIED — ERRORS FOUND** | Paper exists: Faerden et al. (2022/2023), HERD 16(2):55–72. doi:10.1177/19375867221136558. **Not an RCT** — pre/post quasi-experimental with control group, staff questionnaire. Cohen's d = 2.0 **[UNVERIFIED-QUANT]** after 2 search attempts; cannot confirm from available abstracts/citations. BPC must correct: (a) study design → "quasi-experimental" not "RCT"; (b) effect size needs primary-source verification before re-citation. |
| 2B.4 | Weltens 2023, OR 5.36 overcrowding→aggression | **VERIFIED** | Weltens et al. (2023), BMJ Open 13(2):e067943. OR=5.36, 95% CI 1.69–16.99, p=0.004. "Exceeding the maximum bed capacity" → aggression risk. Wide CI — BPC should cite CI alongside OR. |
| 2B.5 | Avandell NJ $12,000/month vs US avg ~$7,500 → 60% premium | **CONFIRMED FABRICATION** | Avandell (UMC, Holmdel NJ) is a real planned project but is not open — still in zoning review as of 2024. No published pricing exists. $12,000/month figure has no primary source. "60% revenue premium" calculated from fabricated inputs. Matches RULE 2026-04-09 fabrication pattern exactly. GAP-278 updated. Entire Channel 3a claim line must be removed from economics BPC. |

## Actions taken

- GAP-278 description updated to "CONFIRMED FABRICATION" in SQLite
- No BPC files modified (per audit convention — owner applies changes via toc-editor)

## Corrections owed (for Pass 2A application)

1. `mobility-built-environment.md`: clarify which Steinfeld publication (2006 RESNA n=275 vs 2010 Final Report n≈500) contains each cited figure
2. `mental-health-built-environment.md` (van der Schaaf): add "(admissions; 14,834 unique patients)" qualifier to n=23,868
3. `mental-health-built-environment.md` (Faerden): correct "RCT" → "quasi-experimental pre/post with control"; flag d=2.0 as [UNVERIFIED-QUANT]
4. `mental-health-built-environment.md` (Weltens): add 95% CI (1.69–16.99) alongside OR 5.36
5. `accessibility-feature-market-value-uplift-framing.md`: remove entire Avandell Channel 3a claim line

---

**End Pass 2B.**
