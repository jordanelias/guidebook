# Tier system — canonical definition

**Status:** OPERATIVE — 2026-05-25; amended 2026-07-20 (§8–§10 added; §3 binary rule superseded).
**Source decision:** Owner directive 2026-05-25 ("t2>t3 this is enshrined") closing GAP-273 and resolving GAP-296; owner directive 2026-07-20 (weighted-strength anchoring) enshrined by `decisions/DR-2026-07-20-weighted-strength-anchor-model.md`, closing GAP-298 and GAP-299.
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
| **T6** | Statutory code — legally enforceable national / sub-national accessibility code (ADA, AS 1428.1, NZS 4121, EN 81-70 when adopted as legal compliance, NZ Building Code D1/AS1, Approved Document M Vol 2, AS/NZS, GB 50763, MLIT barrier-free law, etc.) | `code` | **Code-baseline citations.** Tier 6 establishes regulatory floor. ⚠ Superseded by §8 + Option A (2026-07-21): T6 anchors a **weak-band (○) "best practice as currently known"** claim, flagged code-derived; the convergence of multiple T6 codes on a value is convergence-not-evidence (see §3), retained as the weak-band honesty rule |

## 2. sr_meta placement — T2, not T3

The decision: systematic reviews and meta-analyses sit at **Tier 2** alongside named-organisation evidence-based standards.

The reasoning, in declining priority:

1. **PI v10.14 line 138 reading.** Rule #9 step 5 enumerates "Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence" with T4 / T5 explicitly excluded ("Tier 4 international / Tier 5 national-recommended excluded at this step"). The natural reading positions T2 as the synthesis-tier above T3 primary clinical work and below international standards. SR / meta-analysis is the canonical example of synthesis above primary studies.
2. **Evidence-type homology.** T2's other occupants (`standard_eb` from named DPOs / professional bodies) are themselves synthesis-tier — they aggregate primary evidence into a consensus position. SR / meta-analysis aggregates primary evidence into a statistical consensus position. Same epistemic move, different machinery.
3. **Citation behaviour.** When a Guidebook claim cites both an SR and a primary clinical study, the SR is treated as the warrant-source and the primary study as one of the inputs the SR weighed. The warrant-source must rank above the input-source. SR > primary clinical.
4. **GRADE alignment.** The GRADE framework places systematic reviews / meta-analyses of RCTs at the top of the evidence-quality hierarchy. The Guidebook does not adopt GRADE wholesale (the Guidebook reads built-environment claims rather than treatment-effect claims), but the synthesis-above-primary principle is the same.

The four sr_meta rows previously sitting at T3 are migrated to T2 by `scripts/migrations/data_20260525070000_sr_meta_t2_canonicalization.sql`.

**Scoping reviews and conceptual/framework papers are T3, not T2 (DR-2026-07-21).** `sr_meta` (T2) is reserved for *systematic* reviews and meta-analyses — a defined method with risk-of-bias appraisal and/or effect synthesis. A **scoping review** maps a literature without appraisal (a weaker synthesis) and anchors at **T3**; a peer-reviewed **conceptual/framework paper** (e.g. a design-index proposal such as ASPECTSS) is primary work, also **T3**. Relatedly (DR-2026-07-21): **national accessibility standards** (DIN 18040, BS 8300) and **professional-body design guides** (e.g. the RIBA/Habinteg Inclusive Housing Design Guide) sit at **T5** `national_fw` at the standard/guidance level — a specific provision only becomes T6 when cited as a legally-enforceable adopted code floor (the T5-vs-T6 split already drawn in §1's table).

## 3. Best-practice ≠ convergence

A separate canonical clarification, surfaced 2026-05-25 during reverification scoping.

**The convergence-not-evidence trap.** A claim of the form "BS 8300, DIN 18040-1, Part M, and AS 1428.1 all specify X" is a **convergence claim across Tier 4–6 sources**. Convergence is informative — it tells us multiple jurisdictions adopted the same value. Convergence is NOT best-practice evidence — the jurisdictions could all be wrong together, or could all be reading from a single shared earlier source that itself rests on no evidence, or could all reflect pre-evidence regulatory floors that no jurisdiction has updated.

**The corridor-width worked example.** Multiple Tier 5/6 codes converge on 1800mm two-wheelchair-passing. Co-1/T2/T3 evidence (DSDG Bauman 2010, DeafScape Vaughn 2018, Cloete & Rout 2025) anchors 2440mm primary corridors. The 1800mm convergence describes the regulatory floor; the 2440mm Co-1/T2/T3 anchor describes best practice. Labelling 1800mm "preferred" or "best practice" because it converges across T5/T6 jurisdictions is the failure mode this section names.

**The implication for citation tiering.** Tier 4–6 citations are valid for code-baseline claims (this is the legal floor in jurisdiction X) and for jurisdiction-tracking work.

> **⚠ Superseded 2026-07-20 by §8.** The original text here read *"they do not — by themselves — anchor best-practice claims. Best-practice claims require T1, Co-1, T2, or Co-2 evidence."* That binary is replaced by the **weighted-strength anchor model** (§8): a T4–T6-only claim *may* be stated, but is rendered at partial/weak strength with an explicit honesty flag. The convergence-not-evidence principle above is retained as the honesty rule for the weak band.

## 4. Code-currency check is part of citing T4–T6

When a BPC cites a T4–T6 source, the citation must additionally confirm that the cited edition is the **current legally-in-force edition** — not a superseded edition. Pre-existing supersession_check rows surface this for the supersession protocol; the same check applies inline to any new T4–T6 citation.

**Enforcement (Level 2 audit script, added 2026-05-25):** `scripts/audit/code_currency_audit.py` is the mechanical check. Per architecture v2.3 `<enforcement_spectrum>`, this rule is promoted from text rule (Level 1) to audit script (Level 2) because (a) it is mechanically checkable from `evidence_sources.tier` + `pub_year` + the new `code_currency_*` columns, and (b) drift was observably costly during the 2026-05-25 reverification scoping (DIN 18040-1:2010 and NZS 4121:2001 both surfaced as cases where edition currency required direct jurisdiction-source checks that no inline rule had previously required).

The audit fires per-tier age thresholds (T4: 7 years; T5/T6: 5 years) and lists rows for jurisdiction-tracker review. Suppression criteria documented in the audit script header:
- `code_currency_status IN ('VERIFIED-CURRENT','PERMANENT-FRAMEWORK')` with `code_currency_verified_at` within 365 days;
- OR `supersession_check` row with outcome in `{current_best, co1_addition_logged, refined_by}` within 365 days (any slug);
- OR `pub_year` within tier-specific freshness threshold.

`code_currency_status` enum: `VERIFIED-CURRENT`, `PERMANENT-FRAMEWORK` (foundational references like CRPD, ICF, WHO Child Growth Standards that do not revise on the same cadence), `SUPERSEDED-PENDING-REPLACEMENT`, `UNVERIFIED-CHECK-DEFERRED` (e.g., T6 codes flagged in MOB Pass-2 supersession audit as out-of-scope per DR-2026-05-24).

Worked example surfaced 2026-05-25: `accessible-circulation-geometry.md` cites DIN 18040-1:2010-10. The 2010 edition is still legally in force in Germany (referenced in MVV TB 2024/1 published August 2024), but draft revision E DIN 18040-1:2023-02 exists and DIN EN 17210:2021 has been published as the European harmonised accessibility standard. A reverification of the BPC must consider whether the 2010 citation should be retained, supplemented, or replaced. Counter-example same day: NZS 4121:2001 is 24 years old but remains the NZ Building Act §119 / D1/AS1 Acceptable Solution per NZ Ministry of Education March 2025 guidance; age does NOT predict supersession.

## 5. evidence_quality marker mapping

`skills/guidebook-auditor_SKILL.md` §4.2 inline quality markers map to the canonical ladder:
- `●` confirmed evidence base: T1, T2 (sr_meta + standard_eb + co2), **T3 clinical** (lower-control primary clinical research — confirmed primary evidence, lower control level), Co-1, Co-2
- `◐` policy or standards basis only, not primary evidence: T4, T5
- `○` grey literature, expert consensus, thin base, unconfirmed: T3 grey, `[EXPERT CONSENSUS]`, `[THIN BASE]`, `[UNSUPPORTED]`, T6 (code-floor)

The T3 split is deliberate: T3 holds two species (per §1) — lower-control *primary clinical* research and *grey-literature* primary research. The clinical species is confirmed primary evidence (just lower control) and maps to `●`; the grey species maps to `○`. The earlier version of this map listed only "T3 grey → ○" and left T3-clinical unplaced (R9-c).

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

## 8. Weighted-strength anchor model (2026-07-20)

Enshrined by `decisions/DR-2026-07-20-weighted-strength-anchor-model.md` per owner directive. **Supersedes the binary rule in §3** ("best-practice claims require T1/Co-1/T2/Co-2").

**Every tier can anchor a best-practice claim; the strength of the claim is weighted by the tier of its evidence.** The tiers exist so a reader can grade the confidence behind each proposal — not to gate whether a proposal may be stated. Three strength bands (the `●◐○` markers of §5, now with anchoring semantics):

| Band | Tiers | Anchoring behaviour |
|---|---|---|
| **● Full** | T1, Co-1, T2, Co-2, T3-clinical | Anchors outright (adjudicated evidence). |
| **◐ Partial** | T4, T5 | Anchors, rendered as *current standards practice* — flagged "standards basis, not primary evidence." |
| **○ Weak** | T3-grey, T6 (code-floor), expert-consensus / thin base | Anchors only a floor/convergence claim, rendered with the flag: *"best available given current regulation/practice, NOT academically adjudicated."* |

Convergence-not-evidence (§3) is retained as the honesty rule within the weak band. **Amended 2026-07-21 (owner directive, Option A; `decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md`):** a T4–T6-only determination *is* rendered as **weak-band (○) "best practice as currently known"** — best available given that nothing stronger says otherwise — always flagged weak/code-derived with the convergence-not-evidence caveat, never unflagged and never above the ○ band. This supersedes the prior wording ("never relabelled 'best practice'"): such a claim is now stated-and-flagged as weak-band best practice, not suppressed and not merely labelled "regulatory floor," when no stronger evidence exists. **Band assignment at determination level:** a cell whose entire basis is T4–T6 takes ○ even where T4/T5 sources are present; the ◐ "current standards practice" band in the table above applies to individual T4/T5 *citations* within an otherwise-anchored cell, and to source-level `●◐○` markers (§5), which are unchanged (DR-2026-07-21 §2.3).

## 9. Review-species tiering (closes GAP-298)

- **Systematic reviews / meta-analyses → T2** (`sr_meta`) — unchanged (§2).
- **Scoping reviews and narrative / literature reviews → T3** (`clinical`/`grey`, never `sr_meta`): they map breadth without graded critical-appraisal synthesis, so they are *supporting* (● band) but not a T2 synthesis anchor.
- **Rapid reviews → case-by-case:** T2 only if a systematic search + appraisal was retained; else T3 (default).

## 10. Practitioner / firm practice-stream (closes GAP-299)

Practitioner and firm design work (architects, accessibility consultants) is placed **by method, not authorship**, and sits **below Co-1 and Co-2 in authority**:
- Firm POE / measured study (outcome or cost data) → primary evidence at its method tier (T1/T3).
- Firm framework/index that genuinely synthesises evidence → T2-adjacent; else supporting (T3).
- Firm guidance/white-paper without method → T3-grey (○ weak).

**Role-appropriate-authority gate.** A firm/architect source can anchor a *descriptive/measured* claim (what was built, cost, measured) at its method strength, but **cannot anchor a functional-need claim** ("disabled people need X / X works because Y") on its own — that requires **Co-1** (lived experience) or **Co-2** (OT). A firm asserting a functional-need claim alone is flagged *"designer assertion, unadjudicated."* A dedicated `practice` (Co-3) encoding is defined in the DR; its audit representation is deferred to the audit rework.
