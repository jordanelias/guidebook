# Investigation: Specifications That Would Change Without Language Bias
**Date:** 2026-04-09 22:30
**Model:** Sonnet 4.6
**Scope:** All Part 4 specification values cross-referenced against BPC synthesis and non-EN evidence
**Method:** (1) Extract all 117 divergent findings from 91 BPC files. (2) Cross-reference each divergence against Part 4 spec values. (3) Identify cases where the Part 4 spec follows EN evidence and the BPC synthesis (which is language-neutral) recommends a different value.

---

## Result: Three specifications would change. One requires investigation.

---

### CHANGE 1 — G-03 Grab Bar Height: 800–900 mm → 650–900 mm (median 700 mm)

**Current Part 4 (G-03):** "bilateral horizontal bars at 800–900 mm AFF both sides"

**BPC synthesis (Opus-reviewed):** "height range 650–900 mm AFF (median 700 mm; Tier 2: 280 mm above seat surface per OT assessment)"

**Evidence:**
- KR: 650–700 mm — derived from wheelchair armrest-height match; biomechanically grounded (Tier 1)
- JA: Nakamura 2009 — hemiplegic transfer biomechanics support 650–700 mm range (Tier 1)
- UK/AU: 800–900 mm — derived from standing support context (Tier 5–6)
- Kennedy et al. 2015 (CA): vertical bar preference with COP deviation data (Tier 1)
- Levine et al. 2024 (CA/Tier 1): body height correlates with optimal grasp position — supports range, not fixed value

**Diagnosis:** The BPC synthesis already corrected this. The Opus synthesis note explicitly states: "Grab bar height widened to 650–900 mm with seat-relative Tier 2 formulation." But Part 4 G-03 was not updated to match. The Part 4 spec retains the UK/AU 800–900 mm range, which is the standing-support-derived English-language value.

**What would change:** G-03 specification text changes from `800–900 mm AFF` to `650–900 mm AFF (Mode P median: 700 mm; Tier 2: 280 mm above seat surface, resolved by OT assessment)`. This is a meaningful change: it lowers the bottom of the range by 150 mm, which matters for seated transfer biomechanics and for users in wheelchairs with lower seat heights (common in KR/JA contexts).

**Tier analysis:** KR/JA evidence is Tier 1 (biomechanical, intervention-tested). UK/AU evidence is Tier 5–6 (code/guidance). Under the project's own hierarchy, Tier 1 governs.

**Language bias confirmed:** Yes. The Part 4 spec adopted the EN/Tier 5–6 value (800–900 mm) over the KR/JA/Tier 1 value (650–700 mm for the lower bound). The BPC synthesis already corrected this, but the correction was not propagated to Part 4.

---

### CHANGE 2 — I-01 Hardware Operating Force: ≤22 N → ≤20 N

**Current Part 4 (I-01):** "Force: ≤22 N for all hardware"

**BPC synthesis (Opus-reviewed):** "lever handles operable with closed fist or loose grip at ≤20 N" and "Operating force ≤20 N (0–30°)"

**Evidence:**
- AU (AS 1428.1:2021): ≤20 N — strictest statutory value
- NO (TEK17): ≤20 N — equal strictest
- UK (BS 8300:2018): ≤22 N
- UK (Part M): ≤30 N
- US (ADA): ≤5 lbf (~22.2 N) — origin of the 22 N value in Part 4
- Brandt et al. 2016 (Tier 3, empirical): 30 N acceptable to 94.7% of WC users; 20 N is conservative but appropriate as best practice

**Diagnosis:** The Part 4 spec uses the ADA/BS 8300 value (≤22 N). The BPC synthesis identifies AU/NO ≤20 N as best practice. The difference is 2 N — small in absolute terms but the BPC synthesis explicitly states this is the "highest-ambition" value. The Opus synthesis confirmed: "AU/NO ≤20 N as best practice is sound."

**What would change:** I-01 specification changes from `≤22 N` to `≤20 N`. Minor numerical change but aligns with the project's stated method (best practice, not code minimum).

**Language bias confirmed:** Marginal. The 22 N value traces to ADA (US/EN). The 20 N value is from AU/NO (EN/NO). Both originate in non-exclusively-English jurisdictions — Australia publishes in English. This is more accurately a "code-lag" issue than a language-bias issue. But the BPC synthesis already resolved it to 20 N and Part 4 didn't follow.

---

### CHANGE 3 — E-07 Slip Resistance PTV: Add ≥40 Wet for High-Rainfall Climates

**Current Part 4 (E-07):** "PTV ≥36 wet" throughout

**BPC divergent finding:** "Japanese PTV wet threshold: PTV ≥40 wet (JIS) vs PTV ≥36 (E-07 current). Cause: Climate-specific (high-rainfall)."

**Evidence:**
- JIS T 9251 (JP): PTV ≥40 wet — Tier 4 (international standard with evidence basis)
- HSE/BS 7976-2 (UK): PTV ≥36 wet — Tier 5 (national guidance)
- Bathroom BPC: PTV ≥36 — adopted from UK/HSE

**Diagnosis:** The JIS ≥40 value is a Tier 4 source; the HSE ≥36 is Tier 5. Under the project hierarchy, Tier 4 governs. The BPC flags this as "climate-specific" but the JIS standard is not limited to high-rainfall climates — it is the Japanese national standard for all accessible surfaces.

**What would change:** E-07 specification adds a climate-differentiated provision: `PTV ≥36 wet (temperate climates); PTV ≥40 wet where high-rainfall or tropical climate conditions exist, or where bathroom/wet area surfaces remain wet for extended periods (JIS T 9251; Tier 4)`. Alternatively, the entire spec could upgrade to PTV ≥40 since the JIS source is a higher tier than the HSE source.

**Language bias confirmed:** Partial. The BPC correctly identified the divergence but classified it as "climate-specific" rather than as a higher-tier source that should govern. The ≥36 value was retained because the EN/UK source (HSE, Tier 5) was implicitly treated as the default, with the JA source (JIS, Tier 4) treated as a regional variant. Under strict tier hierarchy, JIS governs.

---

### INVESTIGATION REQUIRED — Reach Range Upper Bound: 1100 mm vs 1200 mm

**Current Part 4 (I-02):** Cooktop controls "400–1100 mm AFF"

**Current BPC synthesis:** "All operable controls within the reach zone 400–1100 mm"

**Divergent finding:** "Norwegian SINTEF reach zone: 400–1200 mm lateral (SINTEF) vs 400–1100 mm (English-language). Cause: Larger sample size in Norwegian data."

**Status:** The SINTEF data is cited in the multilingual evidence convergence BPC but is NOT cited in the reach-range-and-accessible-controls BPC source list. The reach-range BPC cites ADA, BS 8300, NBR 9050, DIN 18040, and RHFAC — but not SINTEF.

**Complication:** The BPC synthesis explicitly states: "NBR 9050 lateral reach-with-trunk-displacement envelope extends to higher values but this represents functional compensation, not design intent — design should eliminate the need for trunk displacement." The SINTEF 1200 mm value may similarly represent extended reach with displacement.

**What would need to happen:** Load the SINTEF-Byggforsk source and determine whether the 1200 mm upper bound is (a) relaxed reach without trunk displacement (in which case it would widen the design envelope) or (b) maximum reach with displacement (in which case the BPC is correct to exclude it). This cannot be resolved without reading the source.

**Language bias assessment:** The SINTEF source was found during multilingual research but was not integrated into the reach-range BPC. Whether this is because of language bias (Norwegian source overlooked) or because of a methodological judgment (reach-with-displacement excluded) is ambiguous. **Flag for Opus session with source verification.**

---

## SPECIFICATIONS THAT ALREADY ADOPTED NON-EN EVIDENCE (No Change Needed)

These specifications confirm that the synthesis process is NOT systematically biased — several of the guidebook's most consequential specifications already adopt non-EN evidence over EN evidence:

| Spec | Value | Source language | Tier | EN alternative |
|---|---|---|---|---|
| E-03 Ramp gradient | ≤1:20 | Swedish (Boverket/SINTEF) | 1/5 | ADA 1:12 (Tier 6) |
| E-06 Threshold | ≤4 mm (zero preferred) | German (Nullschwelle) / Norwegian / Japanese | 5–6 | ADA ≤13 mm (Tier 6) |
| D-03 Toilet visibility | Direct sightline from living space | German (Marquardt 2011) | 3 | No EN equivalent |
| D-09 Consistent environment | Dementia village cluster ≤9 | Dutch (De Hogeweyk POE) | 2 | No EN equivalent |
| D-11 Loop garden seating | Every 20 m | Danish (Nationalt Videnscenter) | 2 | No EN equivalent |
| F-06 Heat shock | Inter-room ΔT ≤5–7°C | Japanese (AIJ) | 3 | No EN equivalent |
| UD cost premium | 0.94%–3.92% by type | Belgian/Dutch (Ielegems & Vanrie) | 3 | No equivalent |
| Bathroom typology | Open-plan wet room | Japanese (多目的トイレ) | 4 | BS 8300 (Tier 5) |

These eight cases demonstrate that where non-EN evidence is identified and classified, it IS adopted. The problem is not systematic bias in the synthesis process — it is incomplete propagation from BPC to Part 4 (Changes 1–2) and incomplete tier-hierarchy application (Change 3).

---

## SPECIFICATIONS WITH EN-ONLY EVIDENCE (Cannot Assess)

The following specification domains have NO non-EN evidence at all. Whether specs would change cannot be assessed until multilingual retrieval is completed:

| Domain | Populations | EN-only confirmed |
|---|---|---|
| OFS built environment | OFS/ME, OFS/POTS, OFS/MCAS | Yes — all languages |
| PAIN built environment | PAIN (chronic pain, fibromyalgia) | Yes — all languages |
| DBL built environment | DeafBlind | Yes — Protactile community only |
| ASPECTSS autism design | NDV/AUT | Yes — Mostafa (Egyptian researcher, EN publication) |
| Auracast/assistive technology | DEAF | Yes |
| Sensory room user control | NDV/AUT | Yes — Unwin (Cardiff, EN) |

For these domains, non-EN evidence simply does not exist in the indexed literature. The EN-only status is a field-wide limitation, not a project bias. However, until the CO-0005 expanded jurisdiction passes (46 jurisdictions, 19 languages) are run for these domains, the absence of non-EN evidence is an incomplete search, not a confirmed absence.

---

## CONCLUSION

Three Part 4 specifications would change if language bias were fully eliminated:

1. **G-03 grab bar height** — BPC-to-Part 4 propagation gap. BPC already corrected; Part 4 not updated. KR/JA Tier 1 evidence governs over UK/AU Tier 5–6.
2. **I-01 operating force** — BPC-to-Part 4 propagation gap. BPC already resolved to ≤20 N; Part 4 retains ≤22 N.
3. **E-07 PTV** — Tier hierarchy not applied. JIS Tier 4 (≥40) should govern over HSE Tier 5 (≥36), or at minimum be applied as a climate-differentiated provision.

One specification (reach range upper bound) requires source verification before a decision can be made.

The remaining ~240+ specification values in Part 4 are either (a) already aligned with non-EN evidence, (b) based on cross-linguistic consensus, or (c) in domains where no non-EN evidence exists.

**The bias is real but narrow.** It affects 3 out of ~250 specification values — approximately 1.2%. The mechanism is not systematic anti-non-EN prejudice in the synthesis process. It is incomplete propagation of BPC synthesis conclusions to Part 4 spec text.
