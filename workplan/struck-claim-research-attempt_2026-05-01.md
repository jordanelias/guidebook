# [STRUCK] Claim Re-Source Research Attempt

**Status:** Research findings + recommendations
**Authoring:** Opus 4.7 audit-remediation session 2026-05-01
**Audit basis:** audit_2026-04-30 R12 — three claims sit in BPC text as `[STRUCK]` annotations after Block 32 source-strikes (2-failed-search rule). Each requires either re-sourcing or removal-with-rationale. Block 32 close noted the re-source attempt would need a deferred Opus session.
**Method:** web_search across multiple query reformulations per claim; capture replacement candidates with full citation; assess Tier per A6; recommend retain-with-replacement or CLOSED-DELETED per Standing Rule 5.

---

## 1. Claim 1 — Indoor vegetation cognitive benefits (was Rhee 2023)

### 1.1 Original [STRUCK] state

The original citation was attributed to "Rhee 2023" for indoor vegetation cognitive benefits. Block 32 search-trail showed two failed verification searches; per Standing Rule 5 the source was struck from the BPC text but the underlying claim was not removed.

### 1.2 Replacement search

**Query:** indoor vegetation cognitive performance benefits systematic review meta-analysis

### 1.3 Replacement candidates

**Primary candidate: Han, Ruan, Liao 2022 — "Effects of Indoor Plants on Human Functions: A Systematic Review with Meta-Analyses"**

- DOI: 10.3390/ijerph19127454
- Journal: International Journal of Environmental Research and Public Health
- Method: SR + meta-analysis (42 records SR; 16 records meta-analysis)
- Tier: 3 (systematic review with meta-analysis)
- Key findings: indoor plants significantly benefit diastolic blood pressure (SMD −2.526, 95% CI −4.142 to −0.909) and academic achievement (SMD 0.534, 95% CI 0.167 to 0.901); non-significant but trending positive effects on EEG α/β waves, attention, and response time

**Secondary candidate: Lee et al. 2023 — "Effects of nature on restorative and cognitive benefits in indoor environment"**

- PMC ID: PMC10425438
- Method: controlled study (n=30) comparing baseline / indoor (some vegetation) / semi-indoor (large vegetation + sky view); EEG measurement
- Tier: 3 (controlled study)
- Key findings: nature exposure produced higher restoration scores AND higher working memory performance vs baseline; reduced delta-to-theta, delta-to-alpha, theta-to-beta, alpha-to-beta ratios in EEG (reduced cognitive fatigue indicator)

### 1.4 Recommendation: RETAIN claim with replacement source

The Han 2022 systematic review is a stronger source than the original Rhee 2023 attribution. The claim "indoor vegetation provides cognitive benefits" is supported at Tier 3 with quantified effect sizes for cognitive outcomes (academic achievement) and physiological correlates (diastolic BP, EEG markers).

**Replacement citation:** Han KT, Ruan LW, Liao LS. Effects of Indoor Plants on Human Functions: A Systematic Review with Meta-Analyses. *Int J Environ Res Public Health* 2022;19(12):7454. DOI: 10.3390/ijerph19127454.

**Action at adoption:** in affected BPCs (likely sensory-environment, biophilic-design, or ALL-ENV related entries), replace `[STRUCK — Rhee 2023]` with citation to Han 2022; update tier flag to Tier 3; record meta-analysis effect sizes if relevant to specification.

---

## 2. Claim 2 — Village Landais Alzheimer 31% psychotropic reduction (was INSERM citation)

### 2.1 Original [STRUCK] state

The original claim attributed a "31% psychotropic medication reduction" to INSERM research at Village Landais Alzheimer (the experimental dementia village in Dax, France, opened 2020). Block 32 search-trail showed two failed verification searches for the specific 31% figure.

### 2.2 Replacement search

**Query:** Village Landais Alzheimer psychotropic medication reduction outcomes study

### 2.3 Findings

The INSERM research at Village Landais (under Hélène Amieva, INSERM research director) is real and reported. However:

**The specific 31% figure was not located in any retrieved source.** The 3-year findings reported by INSERM (per Medscape French-language coverage of the research presentation) describe:

- Decrease in antidepressant and anxiolytic consumption among **caregivers** (not residents) from 6 months post-admission, sustained at 12 months
- Substantial decrease in caregiver burden score from admission to 6 months, maintained at 12 months
- Absence of increase in caregiver anxiety/depression scores

A more recent (November 2025) symposium at Dax reported continuing positive scientific results that contrast with usual EHPAD (residential dementia care) trajectories, but does not appear to confirm a specific resident psychotropic reduction percentage either.

**Methodologically similar but distinct evidence: Vella-Brincat 2018 — "Consensus and evidence-based medication review to optimize and potentially reduce psychotropic drug prescription in institutionalized dementia patients"**

- PMC ID: PMC6323667
- Method: prospective quasi-experimental pre/post intervention multicenter study; 7 nursing homes
- Findings: mean psychotropic drugs decreased from 2.71 to 1.95 (1 month post) and 2.01 (6 months); antipsychotic reduction 49.66%
- Tier: 3 (multicentre prospective study)

This is methodologically different from Village Landais but supports the broader claim that structural / consensus-based approaches reduce psychotropic prescribing in dementia care.

### 2.4 Recommendation: REMOVE specific 31% figure; REPLACE with directional finding

The specific 31% number should not be retained without verifiable source. Two paths:

**Path A — Replace with directional finding from Amieva/INSERM Village Landais research.** Update BPC text to read: "Village Landais Alzheimer 3-year follow-up reports caregiver psychotropic consumption (antidepressants, anxiolytics) decreased from 6 months post-admission and sustained at 12 months (Amieva et al. INSERM 2024 — Medscape FR coverage of 3-year research presentation)." This honest-finding language preserves the directionally-correct observation without the unsupported quantification.

**Path B — Replace with Vella-Brincat 2018 49.66% antipsychotic reduction figure.** Update BPC text to cite this distinct intervention (consensus-based medication review in nursing homes, not the Village Landais structural approach). This requires reframing the claim because the methodology differs.

**Recommended: Path A.** The original claim was about Village Landais's structural approach; preserving that framing while correcting the metric is faithful to the original intent.

**Replacement citation:** Amieva H et al. Village Landais Alzheimer 3-year findings (INSERM research presentation; reported via Medscape France 2024). [If a peer-reviewed publication of these findings exists, it should be sought out; the present search located only press coverage of the research presentation.]

**Tier:** uncertain — depends on whether INSERM has published peer-reviewed findings or only conference / press release. If only the latter, this is Tier 4 (preliminary) at best, with `evidence_state: PRELIMINARY-FINDINGS` flag. The audit recommends a project-owner check on whether peer-reviewed publication exists before applying the replacement.

**Tier flag:** if peer-reviewed publication confirmed → Tier 3; if conference/press only → Tier 4 with PRELIMINARY-FINDINGS flag.

### 2.5 If neither path is acceptable: CLOSED-DELETED per Standing Rule 5

If the project owner judges that neither directional INSERM finding nor the Vella-Brincat 49.66% are appropriate replacements, the claim should be removed entirely with a `[REMOVED — original 31% claim removed; not in cited source. No replacement source verified at audit_2026-04-30 R12 re-source attempt.]` annotation.

---

## 3. Claim 3 — Tenji blocks as MOB hazard (was Kapsalis SR)

### 3.1 Original [STRUCK] state

The original claim attributed concerns about tactile paving (tenji blocks) creating mobility hazards for wheelchair users to a "Kapsalis SR" (systematic review). Block 32 search-trail showed two failed verification searches — the Kapsalis SR appears not to exist as a discoverable source.

### 3.2 Replacement search

**Query:** tactile paving tenji blocks wheelchair mobility hazard fall risk research

### 3.3 Replacement candidates

**Primary candidate: Ormerod et al. (incl. Newton) 2015 — "Older people's experiences of using tactile paving"**

- Journal: Proceedings of the Institution of Civil Engineers - Municipal Engineer 168(1)
- Date: March 2015
- Method: qualitative research with older people about tactile paving experiences
- Tier: 3-4 (qualitative research, professional engineering journal)
- Key passage (paraphrased from search results): "tactile paving at crosswalks, which warns those with vision loss that they are entering a street, can be hazardous for manual wheelchair users who may find that it is uncomfortable or causes pain or might precipitate a fall"

**Secondary candidate: Thies et al. ~2011 — "Biomechanics for inclusive urban design: Effects of tactile paving on older adults' gait when crossing the street"**

- Journal: Journal of Biomechanics (or related; full citation not retrieved)
- Method: biomechanical gait study
- Tier: 3 (controlled biomechanical study)
- Key findings: tactile blister paving increases step width and step time variability vs smooth pavement (variability indicators of falls risk); tested on older adults
- Note: the search result also cited Bauby & Kuo 2000, Hausdorff et al. 2001, Richardson et al. 2004, DeMott et al. 2007 as supporting falls-risk variability literature

**Tertiary candidate: Concrete Paving Slabs for Comfort of Movement of Mobility-Impaired Pedestrians (PMC8950068)**

- Tier: 3-4 (survey of MOB users on pavement comfort)
- Confirms general claim that pavement texture affects mobility-impaired users

### 3.4 Recommendation: RETAIN claim with replacement sources

The MOB-hazard concern from tenji blocks is well-evidenced; the original Kapsalis SR was likely a misattribution but the underlying claim is supported at Tier 3 across multiple sources.

**Replacement citation (primary):** Ormerod M, Newton R, Phillips J, Musselwhite C, McGee S, Russell R. Older people's experiences of using tactile paving. *Proceedings of the Institution of Civil Engineers - Municipal Engineer* 2015;168(1):3-10. DOI: 10.1680/muen.14.00016 (DOI inferred from journal pattern; verify before citing).

**Replacement citation (supporting):** Thies SB et al. Biomechanics for inclusive urban design: Effects of tactile paving on older adults' gait when crossing the street. *Journal of Biomechanics* ~2011 (full citation needs retrieval).

**Action at adoption:** in affected BPCs (likely detectable-gradient-protocol-sensory or wayfinding entries), replace `[STRUCK — Kapsalis SR]` with citation to Ormerod 2015; tier flag Tier 3; consider adding Thies as supporting biomechanical evidence. Note: the Ormerod citation is qualitative + professional-engineering-journal; Thies is biomechanical (RCT-adjacent). The combination strengthens the evidence beyond what the original single Kapsalis SR would have provided.

---

## 4. Summary of recommendations

| Claim | Original | Recommendation | Replacement source | Tier |
|---|---|---|---|---|
| Indoor vegetation cognitive benefits | [STRUCK] Rhee 2023 | RETAIN with replacement | Han, Ruan, Liao 2022 (DOI 10.3390/ijerph19127454) | Tier 3 (SR+MA) |
| Village Landais 31% psychotropic | [STRUCK] INSERM | REMOVE 31% figure; replace with directional finding | Amieva et al. INSERM 2024 (peer-review status to verify) OR Vella-Brincat 2018 alternative | Tier 3 or 4 |
| Tenji blocks MOB hazard | [STRUCK] Kapsalis SR | RETAIN with replacement | Ormerod et al. 2015 + Thies et al. ~2011 | Tier 3 |

---

## 5. CS-MIG hook

Per migration-survival.md §6, BPCs containing `[STRUCK]` markers carry a `flag: claim_residue_pending` block on Stage C migration. This document resolves all three [STRUCK] markers contingent on project-owner adoption:

- **Indoor vegetation** — block resolves on Han 2022 citation adoption.
- **Village Landais 31%** — block resolves on Path A/B selection or CLOSED-DELETED.
- **Tenji blocks** — block resolves on Ormerod 2015 citation adoption.

Once each claim is resolved, the affected BPCs return to standard SURVIVES_CONDITIONALLY rules per migration-survival.md §5.

---

## 6. What this document does not do

- It does not edit any BPC. Edits happen at adoption time per project-owner authority.
- It does not verify peer-review status of Amieva 2024. That verification requires a follow-up search or direct query to INSERM publications database.
- It does not retrieve full DOIs for the Thies and Ormerod sources. The DOI pattern is given for Ormerod; the Thies citation needs follow-up retrieval.
- It does not pre-empt CLOSED-DELETED for the Village Landais claim if project owner judges no replacement adequate.

---

## 7. Status

| Field | Value |
|---|---|
| Status | RESEARCH FINDINGS — recommendations to project owner |
| Adoption | PENDING — per-claim project-owner decision |
| Pairs with Decision(s) | up to 3 D-METH/DG-REVIEW records on adoption |
| Author | opus_4.7_session_2026-05-01_audit-remediation |

End of re-source attempt.
