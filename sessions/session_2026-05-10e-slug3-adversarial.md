# Session: Stage C slug 3 adversarial redo + PMP walks
**session_start:** 2026-05-10 20:00 UTC
**session_close:** 2026-05-10 21:15 UTC
**PI version:** v10.6 (v10.7 not yet live in project settings)
**workplan:** workplan-co0007-v4.md

## Summary

Executed Stage C slug 3 (school-environment-autism) with both protocols:
1. Adversarial multilingual redo for 13 non-EN languages (all upgraded PRE-REMEDIATION → FULL PROTOCOL)
2. PMP walk A-08 (NC-25, D=down): gap_signed=0 — BPC matches ANSI S12.60 exactly
3. PMP walk A-02 (NRC ≥0.85, D=up): gap_signed=+0.05 — BPC is below ANSI S12.60 S5.3 minimum of NRC 0.90

Key cross-jurisdictional findings from adversarial searches:
- **Universal:** No jurisdiction has a building code for autism school design (confirmed across all 13 languages)
- **TEACCH criticism:** DE/JA/FI all document evidence limitations of TEACCH structured environments
- **Thin evidence base:** IT scoping review (Tola 2021, PMC8003767) found only 21/801 studies met criteria
- **Three-factor model vs noise+visual:** Tola 2021 identifies sensory quality + intelligibility + predictability (broader than Simpson 2025's noise+visual dominance)
- **FI strongest built-env connection:** Autismiliitto names open learning environments as harmful; Opetushallitus mentions making spaces "less reverberant"
- **Inclusive vs specialized:** Active debate in SV (reversal from inclusion), NO (neurodivergent identity framework), KO (separation → isolation)

## Commits

| SHA | Content |
|---|---|
| 4d3b8a48d4 | data/guidebook.db — slug 3 adversarial + PMP walks |

## DB changes

### search_languages (13 rows updated)
All 13 non-EN languages for slug school-environment-autism: status → SEARCHED, notes updated with adversarial findings, PROTOCOL COMPLIANCE: FULL.

### evidence_sources (2 added)
| ref_id | Citation | Verified via |
|---|---|---|
| REF-00710 | Tola et al. 2021 (PMC8003767, DOI:10.3390/ijerph18063203) | PubMed + PMC |
| REF-00711 | Abdelmoula et al. 2024 (PMC11860188, DOI:10.1192/j.eurpsy.2024.272) | PMC + Cambridge Core |

### evidence_population_match (3 added)
| match_id | source_ref | grade | key note |
|---|---|---|---|
| EPM-S3-001 | REF-00642 (Simpson 2025) | PARTIAL | Grey literature; narrative synthesis, not quantified |
| EPM-S3-002 | REF-00710 (Tola 2021) | PARTIAL | 21/801; three-factor model broader than noise+visual |
| EPM-S3-003 | REF-00711 (Abdelmoula 2024) | PROXY | Conference abstract; confirms ASPECTSS only framework |

### spec_value_probes (10 added)
| walk_id | item | V₀ | D | ceiling | gap_signed | steps |
|---|---|---|---|---|---|---|
| PMP-A08-001 | A-08 NC-25 | 25 NC | down | 25.0 | 0.0 | 3 (1 outer-stop, 1 refinement-stop, 1 final) |
| PMP-A02-001 | A-02 NRC ≥0.85 | 0.85 NRC | up | 0.90 | +0.05 | 7 (1 outer-stop, 1 refinement-pass, 4 refinement-stop, 1 final) |

### items (2 updated)
- A-08: pmp_empirical_ceiling=25.0, pmp_gap_signed=0.0, pmp_direction=down
- A-02: pmp_empirical_ceiling=0.90, pmp_gap_signed=+0.05, pmp_direction=up

## Audit status

Simplified audit run:
- CHECK 1 (protocol fields): CLEAN
- CHECK 2 (verified citations without pop match): 12 pre-existing failures from prior session (REF-VERIFIED-001 through 012). NOT from this session's work.
- CHECK 3 (EXACT distribution): CLEAN (0 EXACT out of 8 total — well below 70% threshold)
- CHECK 9 (PROTOCOL: markers): CLEAN after NO fix

Full audit script not run (path dependency on repo clone). Pre-existing CHECK 2 failures documented in HANDOFF-2026-05-10.md.

## PMP findings for reviewer

### A-08 (NC-25, D=down): No gap
- BPC spec = NC-25 = ANSI S12.60 HVAC component for schools
- NC-20 (20% step down) is studio/library territory — no evidence supports NC-20 for school sensitive spaces
- **Important caveat:** ANSI S12.60 explicitly states it "does not apply for... special education rooms such as those for severely acoustically challenged students." So NC-25 is the GENERAL classroom standard, not an autism-specific standard.
- **Adversarial note:** One study (PMC2955636) found white noise at 78 dB IMPROVED performance for inattentive children — complicating the "lower is always better" assumption for D=down

### A-02 (NRC ≥0.85, D=up): Gap of +0.05
- BPC spec = NRC ≥0.85
- ANSI S12.60 S5.3 specifies NRC ≥0.90 minimum for classroom ceilings
- ANSI/GBI 01-2019 requires NRC 0.90 for patient/eldercare areas
- Sonavyx/Construction Specifier: "NRC 0.90 or higher is the single most effective treatment"
- **Recommendation:** BPC should raise threshold from NRC ≥0.85 to NRC ≥0.90 to match standards evidence

## next_action

1. **Continue Tier 1 multilingual:** circadian-lighting-melanopic-edi (11 NOT-RUN languages)
2. **PMP backlog:** remaining items with numerical specs need walks (11+ items per session 10d handoff finding F)
3. **BPC correction:** A-02 NRC threshold should be reviewed — evidence supports ≥0.90 not ≥0.85
4. **Pre-existing audit debt:** 12 verified citations (REF-VERIFIED-001 through 012) lack population_match entries — separate cleanup task

## blockers

- PI v10.7 still not live in project settings (standing rule #8 for PMP not PI-enforced, only workplan-enforced)
- GAP-281 (bpc_source_slug NULL) still open — does not block current work
- GAP-282 (missing RT60-school item) still open — PMP walk A-02 finding may overlap (ANSI S12.60 RT60 ≤0.6s)
