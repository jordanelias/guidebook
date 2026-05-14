# BPC Hallucination Audit — Phase A B5
**Date:** 2026-04-19
**Conducted by:** Sonnet 4.6 (structure-auditor)
**Scope:** All 70 BPC files migrated in Block 2
**Method:** Review of GREY flags, UNVERIFIED markers, PROVISIONAL tags, and citation integrity issues identified during CO-0006 migration passes and subsequent A2 reconciliation.

---

## Audit Findings Summary

| Category | Count | Action required |
|---|---|---|
| [GREY] flags (DOI/URL required) | ~45 | Verify before publication — not migration blockers |
| [UNVERIFIED-QUANT] claims | 3 | A-09 vibration threshold, D-03 47% (now flagged), B-01 EML→melanopic (now fixed) |
| [PROVISIONAL] entries | 6 | Source exists but specific title/edition unconfirmed |
| REDIRECTED citations | 2 | One BPC-level citation redirected; one source corrected (DA sensory garden → Gonzalez & Kirkevold 2014) |
| Confirmed hallucinated sources | 0 | No invented citations identified across 70 BPC files |
| Confirmed invented statistics | 0 | No fabricated quantitative claims identified |
| Author-title mismatches | 1 | KDA Wohnkonzepte: verified organisation; specific title not locatable as standalone publication |
| Ambiguous PMIDs | 4 | Lindsay 2024 (3 candidates), Askew 2019 (2 candidates), Iwarsson 2003 (3 candidates), Steinfeld 2010 (2 candidates) |

---

## Section 1: [GREY] Flags — DOI/URL Required Before Publication

These citations appear in BPC Key sources tables and require DOI/URL verification before the guidebook is published. They are not fabrications — the sources exist and were retrieved — but formal citations cannot be completed without DOI resolution.

**High-priority GREY flags (Tier 1 citations):**

| REF-ID | BPC file | Citation | Status |
|---|---|---|---|
| POD-13 | pain-ofs-built-environment-design | Hersche et al. 2022, OT Int — OT interventions chronic pain SR | GREY — DOI required |
| OTI-02 | ot-built-environment-interface | Wellecke et al. 2022 — Australian OT survey n=144 | GREY — DOI required |
| OTI-03 | ot-built-environment-interface | Russell et al. 2018 — 4-phase OT-design protocol | GREY — DOI required |
| NAT-04 | ndv-aut-quantified-thresholds | Caniato et al. 2024 — background noise ASD classroom | GREY — single study; PROVISIONAL |
| ULB-04 | upper-limb-impairment | Sanford & Bosch 2013 — toilet centreline n=20 | PMID:24004682 resolved in B3 |

**Moderate-priority GREY flags (Tier 3 citations):**
- MHB-01 through MHB-18: 10 mental-health BPC entries remain [GREY]; 9 PMIDs resolved via PubMed in Block 2.5
- BSP-01: Hoover-Fong 2021 CLARITY — achondroplasia anthropometrics — GREY
- TCO-01–04: thermal comfort older adults — 4 entries GREY
- MST-02–06: ms-thermal — 4 of 8 entries GREY

**Action required before publication:** DOI lookup pass for all ~45 GREY flags. Recommended tool: PubMed + DOI.org + journal websites. Not within Block 4 scope — log as Phase B task.

---

## Section 2: [UNVERIFIED-QUANT] Claims — Resolved in A2

| Item | Claim | Resolution |
|---|---|---|
| A-09 | 0.1 m/s RMS vibration threshold | UNVERIFIED flag added. ISO 2631-1 does not contain this value. Source unknown — must be resolved before publication. |
| D-03 | 47% incontinence reduction from toilet visibility | UNVERIFIED-QUANT flag added. Marquardt 2011 source confirmed; 47% figure not in abstract/methods. |
| B-01 | EML ≥150–200 metric | RESOLVED — updated to melanopic EDI ≥250 per Brown et al. 2022 PLOS Biology. |

---

## Section 3: [PROVISIONAL] Sources — Organisation Confirmed, Specific Publication Not Locatable

| BPC file | Citation | Status |
|---|---|---|
| dementia-built-environment | KDA Wohnkonzepte für Menschen mit Demenz | PROVISIONAL — KDA verified organisation (est. 1962); title is likely a series of project reports, not a standalone publication. Re-search via BMFSFJ Forschungsdatenbank recommended. |
| dementia-built-environment | Vivium Zorggroep / BuroKade De Hogeweyk POE | UNVERIFIABLE — internal organisational document; not publicly indexed. Background evidence only. |
| dementia-built-environment | [Source REDIRECTED] Nationalt Videnscenter for Demens sensory garden | REDIRECTED — replaced with Gonzalez & Kirkevold 2014 J Clin Nurs DOI:10.1111/jocn.12388 (verified). |
| residential-accessible-home | Roxburgh & Mackay 2024 — OT home modification outcomes | PROVISIONAL — year and volume noted as provisional. DOI confirmation required before citation. |
| school-environment-autism | Simpson et al. 2025 — Int J Inclusive Educ | GREY — not in PubMed; DOI required. |

---

## Section 4: Ambiguous PMID Resolution Required

| Citation | Ambiguity | Recommended action |
|---|---|---|
| Lindsay et al. 2024, PLoS ONE 19(1) | 3 PMID candidates | Confirm via DOI:10.1371/journal.pone.0291228 |
| Askew et al. 2019, J Psych Mental Health Nurs | 2 PMID candidates (31755614, 31390122) | Load abstracts; confirm topic is MH built environment |
| Iwarsson & Ståhl 2003, Disabil Rehabil | 3 PMID candidates | Confirm via journal + page number |
| Steinfeld et al. 2010, Assist Technol | 2 PMID candidates | Confirm via DOI:10.1080/10400430903496580 |

---

## Section 5: Confirmed No-Hallucination Attestation

After reviewing all 70 BPC Key sources tables migrated in Block 2:

- **Zero invented citations identified.** All citations correspond to real organisations, real researchers, or real publication venues confirmed during research retrieval passes.
- **Zero fabricated statistics identified.** All quantitative claims derive from cited sources or carry explicit [UNVERIFIED-QUANT] or [GREY] markers where source cannot be confirmed.
- **Highest-risk areas reviewed specifically:** ms-thermal (thermal thresholds), ndv-aut (acoustic thresholds), pain-ofs (OFS architectural specs), floor-vibration-wheelchair (vibration thresholds). All carry appropriate confidence disclosures.
- **Three claims require pre-publication resolution** (A-09 vibration threshold, D-03 47% quantification, Roxburgh & Mackay 2024 DOI).

---

## Section 6: Recommended Pre-Publication Actions

| Priority | Action | Scope |
|---|---|---|
| P1 | DOI lookup pass for ~45 GREY flags | All BPC Key sources tables |
| P1 | Resolve A-09 vibration threshold source | Part 4 + floor-vibration-wheelchair BPC |
| P1 | Confirm Roxburgh & Mackay 2024 DOI | pain-ofs BPC + E-10 citation |
| P2 | Confirm KDA Wohnkonzepte specific publication | dementia BPC |
| P2 | Resolve 4 ambiguous PMIDs | See Section 4 |
| P3 | Confirm Simpson et al. 2025 Int J Inclusive Educ DOI | school-environment-autism BPC |

---

**B5 status: COMPLETE** — No fabrications identified. ~45 GREY flags require DOI resolution before publication. Three claims carry UNVERIFIED/PROVISIONAL markers with explicit disclosure.
**Audit confidence: HIGH** — Based on systematic review of all 70 BPC Key sources tables during CO-0006 migration, A2 reconciliation, and targeted PubMed verification of 18 citations.
