# Session: Stage C slug 3 adversarial + slug 4 circadian + PMP walks
**session_start:** 2026-05-10 20:00 UTC
**session_close:** 2026-05-10 22:00 UTC
**PI version:** v10.6 (v10.7 not yet live in project settings)
**workplan:** workplan-co0007-v4.md

## Summary

Executed Stage C with both protocols across two slugs:

1. **Slug 3 (school-environment-autism):** 13/14 non-EN languages → FULL PROTOCOL adversarial redo. Universal finding: no jurisdiction has building code for autism school design. TEACCH evidence limitations documented (DE/JA/FI). Thin evidence base confirmed (IT Tola 2021: 21/801 studies).

2. **Slug 4 (circadian-lighting-melanopic-edi):** 14/14 languages → FULL PROTOCOL. ZH finding: T/SIEATA 000001-2024 is the ONLY standards-track document globally specifying melanopic EDI for educational spaces. DIN/TS 67600:2022 is the only national-track standard for biologically effective illumination.

3. **PMP walks (3):**
   - A-08 (NC-25, D=down): gap=0. BPC matches ANSI S12.60.
   - A-02 (NRC ≥0.85, D=up): gap=+0.05. **BPC should raise to ≥0.90** (ANSI S12.60 S5.3).
   - B-01 (≥150 EML, D=up): **gap=+135. Largest gap found.** BPC uses outdated metric (EML→melanopic EDI) AND outdated threshold (150→≥250 m-EDI per Brown 2022 consensus).

## Commits (5 total)

| SHA | Content |
|---|---|
| 4d3b8a48d4 | DB: slug 3 adversarial + PMP walks A-08, A-02 |
| 713d8ef6d8 | Session file (initial) |
| fab25118b9 | LATEST pointer |
| 53ed9ac2cf | DB: circadian slug FR+JA |
| ff8728eae7 | DB: circadian slug 14/14 + PMP B-01 |

## DB changes summary

### search_languages
- Slug 3: 13 rows updated (PRE-REMEDIATION → FULL PROTOCOL)
- Slug 4: 14 rows updated (11 NOT-RUN + 3 PRE-REMEDIATION → FULL PROTOCOL)

### evidence_sources (2 added)
| ref_id | Citation | Verified via |
|---|---|---|
| REF-00710 | Tola et al. 2021 (PMC8003767) — Built Environment Design and ASD Scoping Review | PubMed + PMC |
| REF-00711 | Abdelmoula et al. 2024 (PMC11860188) — Inclusive architecture for ASD guidelines review | PMC + Cambridge Core |

### evidence_population_match (5 added, 22 total)
| match_id | source | grade | key note |
|---|---|---|---|
| EPM-S3-001 | REF-00642 Simpson 2025 | PARTIAL | Grey literature, narrative synthesis |
| EPM-S3-002 | REF-00710 Tola 2021 | PARTIAL | 21/801; three-factor model broader than noise+visual |
| EPM-S3-003 | REF-00711 Abdelmoula 2024 | PROXY | Conference abstract; ASPECTSS only framework |
| EPM-C4-001 | REF-00551 Brown 2022 | PARTIAL | Consensus for healthy adults, not all BPC populations |
| EPM-C4-002 | REF-00557 Kolberg 2022 | EXACT | Directly measured m-EDI in dementia units |

Grade distribution: 1 EXACT (5%), 3 PARTIAL (60%), 1 PROXY (20%) — no inflated EXACTs.

### spec_value_probes (18 total this session)
| walk_id | item | V₀ | D | ceiling | gap | steps |
|---|---|---|---|---|---|---|
| PMP-A08-001 | A-08 NC-25 | 25 NC | down | 25.0 | 0 | 3 |
| PMP-A02-001 | A-02 NRC≥0.85 | 0.85 NRC | up | 0.90 | +0.05 | 7 |
| PMP-B01-001 | B-01 ≥150 EML | 150 EML | up | 285.0 | +135 | 8 |

## PMP findings for reviewer

### B-01: CRITICAL — gap=+135 EML
The BPC specifies ≥150 EML (Lucas 2014 metric). Brown 2022 consensus (PMC8929548, peer-reviewed, 16 international co-authors) recommends ≥250 melanopic EDI ≈ 275 EML.

**Two corrections needed:**
1. **Metric migration:** EML (Lucas 2014) → melanopic EDI (CIE S 026:2018). WELL v2 already migrated. IES RP-46-23 uses melanopic EDI. EML is deprecated.
2. **Threshold raise:** 150 EML → ≥250 melanopic EDI. Brown 2022 consensus, IES endorsement.

**Adversarial caveats (to document in BPC):**
- "Whether melanopic EDI provides superior predictive value in real-world is not yet established" (MedRxiv)
- Interindividual variation in light sensitivity acknowledged (PMC7970181)
- Seasonal/latitude: "impractical to require specific melanopic EDI every day of year" (Ticleanu 2025)
- Energy cost: conventional luminaires provide fraction of required vertical-plane illuminance
- Not applicable to shift workers
- Only in voluntary certifications (WELL, UL 24480), no mandatory building code except T/SIEATA (ZH, group standard)

### A-02: gap=+0.05 NRC
BPC: ≥0.85. ANSI S12.60 S5.3: ≥0.90. Straightforward correction.

### A-08: gap=0
BPC matches ANSI S12.60 exactly. Note: ANSI S12.60 explicitly excludes "special education rooms."

## Cross-jurisdictional synthesis (slug 4)

| Finding | Languages |
|---|---|
| No mandatory building code for circadian lighting | ALL 14 |
| DIN/TS 67600 (technical specification, not mandatory) | DE |
| T/SIEATA 000001-2024 (group standard, not mandatory) | ZH |
| WELL certification driving adoption | ALL (varying penetration) |
| Seasonal/latitude challenge for daylight-dependent m-EDI | SV, NO, DA, FI (extreme), NL |
| Commercial interest/potential bias (Signify/Philips) | NL |
| Brown 2022 co-author institution | NL (TU/e Eindhoven) |
| Active implementation examples | JA (Panasonic), DE (Endo), NL (Signify) |

## Tier 1 progress

| Slug | Languages FULL PROTOCOL | Status |
|---|---|---|
| luminance-contrast-lrv-evidence-base | 13/14 + 1 PARTIAL | ✅ DONE (prior session) |
| sensory-room-user-control | 10/14 FULL + 4 PRE-REM | ✅ DONE (prior session) |
| school-environment-autism | 13/14 FULL + 1 PRE-REM (EN) | ✅ DONE (this session) |
| circadian-lighting-melanopic-edi | 14/14 FULL | ✅ DONE (this session) |
| construction-cost-data | 1/14 — 11 NOT-RUN | ❌ |
| visual-fire-alarm-seizure-safety | 2/14 — 11 NOT-RUN | ❌ |
| accessible-design-economics-cost-premium | 4/14 — 9 NOT-RUN | ❌ |
| thermal-comfort-older-adults-care-settings | 4/14 — 8 NOT-RUN | ❌ |

## next_action

1. **Tier 1 remaining:** 4 slugs (construction-cost-data, visual-fire-alarm, economics, thermal-comfort)
2. **PMP backlog:** remaining items with numerical specs (11+ per session 10d handoff)
3. **BPC corrections (reviewer action):**
   - B-01: metric EML→melanopic EDI + threshold 150→250 (gap=+135)
   - A-02: NRC threshold 0.85→0.90 (gap=+0.05)
4. **Pre-existing audit debt:** 12 verified citations lack population_match (CHECK 2)

## blockers

- PI v10.7 still not live (standing rule #8 for PMP not PI-enforced)
- GAP-281 (bpc_source_slug NULL) still open
- GAP-282 (missing RT60-school item) — may overlap with PMP A-02 finding
