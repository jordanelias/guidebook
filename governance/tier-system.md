# Tier system — canonical definition

**Status:** OPERATIVE — 2026-05-25
**Source decision:** Owner directive 2026-05-25 ("t2>t3 this is enshrined") closing GAP-273 and resolving GAP-296.
**Supersedes:** drift between PI v10.14 line 138 implicit usage and `skills/guidebook-auditor_SKILL.md` §4.1 explicit ladder.

---

## 1. The ladder

The Guidebook's evidence tiers run T1–T6 with two parallel community-knowledge tracks (Co-1, Co-2). Outer ranks are not "higher quality" in a vacuum — they answer different questions. **Tier number reflects what kind of claim a source can anchor, not how good the source is.**

| Tier | Evidence character | Typical `evidence_type` | What it can anchor |
|---|---|---|---|
| **T1** | Primary research with intervention-level or biomechanical control on the parameter under design | `clinical`, occasionally `grey` for unpublished primary | Best-practice claims that turn on physiological / behavioural / biomechanical mechanism |
| **Co-1** | Disability-led lived-experience publications — DPOs, named-org Deaf / blind / wheelchair-user / mental-health / autism-organisation outputs; CRPD Art. 4.3 consultation outputs | `co1` | Best-practice claims that turn on user-stated preference, dignity, autonomy, or self-determined accommodation. Co-1 ranks alongside T1 because primary-research evidence and lived-experience evidence are non-substitutable on different claim types |
| **T2** | Community-consensus synthesis above primary studies but below international standards. Two streams: (a) systematic reviews / meta-analyses; (b) named-organisation evidence-based standards (DPO guidelines, professional-body standards) | `sr_meta`, `standard_eb`, occasionally `co2` for community-of-professional synthesis | Best-practice claims that turn on synthesised evidence across multiple primary studies, OR on professional-body / DPO position |
| **Co-2** | OT / professional-body CPGs (CAOT, AOTA, RCOT, COTEC, WFOT, national equivalents) | `co2` | Best-practice claims that turn on clinical-professional consensus on rehabilitation or activity-of-daily-living adaptation |
| **T3** | Clinical primary research at lower control level (cross-sectional, observational, qualitative, single-centre) plus grey-literature primary research | `clinical` (predominant), `grey`, occasionally `standard_eb` for specialised technical guidance | Supporting evidence for best-practice claims; rarely the sole basis |
| **T4** | International standards (ISO, IEC, CEN, BSI PAS, EN 81-70, EN 17210, etc.) — published by international bodies; legally significant within their adoption scope | `standard_eb` (predominant) | Code-baseline citations of international harmonisation; supporting evidence for best-practice claims if the standard itself rests on T1/T2 evidence |
| **T5** | National beyond-code frameworks — best-practice guidance issued by national bodies but not legally enforced (BS 8300, DIN 18040 draft, Boverket BBR advisories, national CPGs scoped to BE) | `national_fw` (predominant), `standard_eb` | Code-baseline citations at national best-practice tier; supporting evidence for best-practice claims if the framework rests on T1/T2 evidence |
| **T6** | Statutory code — legally enforceable national / sub-national accessibility code (ADA, AS 1428.1, NZS 4121, EN 81-70 when adopted as legal compliance, NZ Building Code D1/AS1, Approved Document M Vol 2, AS/NZS, GB 50763, MLIT barrier-free law, etc.) | `code` | **Code-baseline citations only.** Tier 6 establishes regulatory floor; it does NOT anchor best-practice claims. The convergence of multiple T6 codes on a value is convergence-not-evidence (see §3 below) |

## 2. sr_meta placement — T2, not T3

The decision: systematic reviews and meta-analyses sit at **Tier 2** alongside named-organisation evidence-based standards.

The reasoning, in declining priority:

1. **PI v10.14 line 138 reading.** Rule #9 step 5 enumerates "Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence" with T4 / T5 explicitly excluded ("Tier 4 international / Tier 5 national-recommended excluded at this step"). The natural reading positions T2 as the synthesis-tier above T3 primary clinical work and below international standards. SR / meta-analysis is the canonical example of synthesis above primary studies.
2. **Evidence-type homology.** T2's other occupants (`standard_eb` from named DPOs / professional bodies) are themselves synthesis-tier — they aggregate primary evidence into a consensus position. SR / meta-analysis aggregates primary evidence into a statistical consensus position. Same epistemic move, different machinery.
3. **Citation behaviour.** When a Guidebook claim cites both an SR and a primary clinical study, the SR is treated as the warrant-source and the primary study as one of the inputs the SR weighed. The warrant-source must rank above the input-source. SR > primary clinical.
4. **GRADE alignment.** The GRADE framework places systematic reviews / meta-analyses of RCTs at the top of the evidence-quality hierarchy. The Guidebook does not adopt GRADE wholesale (the Guidebook reads built-environment claims rather than treatment-effect claims), but the synthesis-above-primary principle is the same.

The four sr_meta rows previously sitting at T3 are migrated to T2 by `scripts/migrations/data_20260525070000_sr_meta_t2_canonicalization.sql`.

## 3. Best-practice ≠ convergence

A separate canonical clarification, surfaced 2026-05-25 during reverification scoping.

**The convergence-not-evidence trap.** A claim of the form "BS 8300, DIN 18040-1, Part M, and AS 1428.1 all specify X" is a **convergence claim across Tier 4–6 sources**. Convergence is informative — it tells us multiple jurisdictions adopted the same value. Convergence is NOT best-practice evidence — the jurisdictions could all be wrong together, or could all be reading from a single shared earlier source that itself rests on no evidence, or could all reflect pre-evidence regulatory floors that no jurisdiction has updated.

**The corridor-width worked example.** Multiple Tier 5/6 codes converge on 1800mm two-wheelchair-passing. Co-1/T2/T3 evidence (DSDG Bauman 2010, DeafScape Vaughn 2018, Cloete & Rout 2025) anchors 2440mm primary corridors. The 1800mm convergence describes the regulatory floor; the 2440mm Co-1/T2/T3 anchor describes best practice. Labelling 1800mm "preferred" or "best practice" because it converges across T5/T6 jurisdictions is the failure mode this section names.

**The implication for citation tiering.** Tier 4–6 citations are valid for code-baseline claims (this is the legal floor in jurisdiction X) and for jurisdiction-tracking work, but they do not — by themselves — anchor best-practice claims. Best-practice claims require T1, Co-1, T2, or Co-2 evidence appropriate to the claim type.

## 4. Code-currency check is part of citing T4–T6

When a BPC cites a T4–T6 source, the citation must additionally confirm that the cited edition is the **current legally-in-force edition** — not a superseded edition. Pre-existing supersession_check rows surface this for the supersession protocol; the same check applies inline to any new T4–T6 citation.

Worked example surfaced 2026-05-25: `accessible-circulation-geometry.md` cites DIN 18040-1:2010-10. The 2010 edition is still legally in force in Germany (referenced in MVV TB 2024/1 published August 2024), but draft revision E DIN 18040-1:2023-02 exists and DIN EN 17210:2021 has been published as the European harmonised accessibility standard. A reverification of the BPC must consider whether the 2010 citation should be retained, supplemented, or replaced.

## 5. evidence_quality marker mapping (unchanged)

`skills/guidebook-auditor_SKILL.md` §4.2 inline quality markers map to the canonical ladder:
- `●` confirmed evidence base: T1, T2 (sr_meta + standard_eb + co2), Co-1, Co-2
- `◐` policy or standards basis only, not primary evidence: T4, T5
- `○` grey literature, expert consensus, thin base, unconfirmed: T3 grey, `[EXPERT CONSENSUS]`, `[THIN BASE]`, `[UNSUPPORTED]`, T6 (code-floor)

## 6. Mapping back to legacy guidebook-auditor SKILL §4.1

The previous guidebook-auditor SKILL §4.1 had `[Tier 4]` = systematic review / meta-analysis. That mapping is **superseded**. SR / meta-analysis is `[Tier 2]` per this document. The SKILL file is amended in lock-step with this canonicalization.

## 7. Migration provenance

| Element | Source |
|---|---|
| Owner decision | 2026-05-25 directive "t2>t3 this is enshrined" |
| Migration | `scripts/migrations/data_20260525070000_sr_meta_t2_canonicalization.sql` |
| Gap closure | GAP-273 (CLOSED-FIXED), GAP-296 (CLOSED-FIXED) |
| Skill amendment | `skills/guidebook-auditor_SKILL.md` §4.1 |
| Session | `session_2026-05-23-bpc-rewrite-phase-b-closure` |
