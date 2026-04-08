# Methodology — Evidence Hierarchy Mapping and Recommendation Strength Protocol

**Document:** `references/methodology-evidence-hierarchy-mapping.md`
**Created:** 2026-04-08 (Phase 1A, CO-0006)
**Model:** Opus 4.6
**Status:** DRAFT — pending project lead review

---

## 1. Purpose

This document establishes the methodological basis for the Guidebook's evidence hierarchy by mapping it to three established evidence-grading frameworks — GRADE, JBI, and SIGN — and documenting where and why the Guidebook departs from each. It provides:

- A crosswalk table linking each Guidebook evidence tier to its closest analogue in GRADE, JBI, and SIGN.
- A formal justification for the co-primary status of lived experience evidence (Co-1).
- A recommendation strength protocol calibrated for built environment specifications rather than clinical interventions.
- The relationship between evidence markers (● / ○) and recommendation strength.

This document is an internal methodological reference. It supports transparency and reproducibility. It is not guidebook prose and does not appear in any published volume.

---

## 2. The Domain Mismatch Problem

GRADE, JBI, and SIGN were designed for clinical medicine — specifically, to evaluate whether a health intervention causes a measurable patient outcome. Their hierarchies privilege randomised controlled trials (RCTs) because randomisation is the most reliable method of isolating causal effects of treatments on individuals.

Built environment specification operates in a fundamentally different domain:

- **The unit of analysis is a space, not a patient.** A corridor width, a door handle height, or an acoustic absorption target is not an intervention administered to a person. It is a spatial parameter that mediates interaction between a person's functional capacity and their physical environment.
- **Randomisation is structurally impossible for most built environment parameters.** One cannot randomise occupants to corridor widths in a double-blind trial. The evidence base is necessarily observational, quasi-experimental, participatory, or derived from ergonomic/anthropometric measurement.
- **The counterfactual is exclusion, not placebo.** In clinical research, the control group receives no treatment or a placebo. In built environment research, the counterfactual to an accessible specification is a specification that excludes — a barrier. The ethical framework is rights-based (CRPD), not equipoise-based.
- **Population heterogeneity is the design problem, not a confound.** Clinical hierarchies treat population variation as noise to be controlled. Accessible design treats it as the specification target. A range is not imprecision; it is the bridge between Tier 1 (population-level) and Tier 2 (person-specific co-design).

These differences mean that no clinical evidence framework can be adopted wholesale. The Guidebook's hierarchy is a purpose-built adaptation that draws on all three frameworks while departing from each where the domain requires it.

---

## 3. Framework Overviews

### 3.1 GRADE (Grading of Recommendations Assessment, Development and Evaluation)

GRADE classifies evidence certainty into four levels (High, Moderate, Low, Very Low) starting from study design and applying upgrade/downgrade criteria (risk of bias, inconsistency, indirectness, imprecision, publication bias; large effect, dose-response, plausible confounding). Recommendation strength is binary: strong or conditional (weak), determined by balancing certainty of evidence, balance of benefits/harms, patient values, and resource use.

**Strengths for this project:** Transparent upgrade/downgrade logic; explicit treatment of indirectness (relevant when applying clinical findings to spatial parameters); structured consideration of values and resources.

**Limitations for this project:** No pathway for qualitative evidence; no mechanism for rights-based obligations (CRPD mandates are not "conditional recommendations"); RCT primacy is irrelevant when RCTs are structurally impossible.

### 3.2 JBI (Joanna Briggs Institute)

JBI uses a broader evidence model than GRADE. It defines evidence as "the basis of belief; the substantiation or confirmation that is needed in order to believe that something is true" — explicitly extending beyond quantitative research. JBI maintains separate appraisal tools for experimental, quasi-experimental, observational, qualitative, text/opinion, and mixed-methods studies. Its ConQual approach grades confidence in qualitative synthesis findings. JBI's FAME framework (Feasibility, Appropriateness, Meaningfulness, Effectiveness) recognises that evidence of what works (effectiveness) is not the only evidence type relevant to practice.

**Strengths for this project:** Explicit inclusion of qualitative and experiential evidence; FAME framework maps well to built environment (feasibility = constructability; appropriateness = population fit; meaningfulness = lived experience; effectiveness = functional outcome); ConQual provides structured appraisal of qualitative synthesis.

**Limitations for this project:** JBI does not address rights-based obligations; its qualitative appraisal assumes researcher-conducted studies, not direct participatory input; no specific treatment of technical standards or regulatory codes as evidence types.

### 3.3 SIGN (Scottish Intercollegiate Guidelines Network)

SIGN grades evidence from 1++ (high-quality meta-analyses or RCTs with very low risk of bias) through 4 (expert opinion). Recommendation grades run A through D, with "good practice points" for recommendations based on clinical experience where no research evidence exists.

**Strengths for this project:** "Good practice points" concept translates well to the ○ (inferred specification) marker; explicit acknowledgment that expert consensus is a legitimate evidence basis when research is absent.

**Limitations for this project:** Same clinical-intervention assumptions as GRADE; no participatory evidence pathway; no mechanism for regulatory or standards-based evidence.

---

## 4. Crosswalk Table

| Guidebook tier | Description | GRADE analogue | JBI analogue | SIGN analogue | Notes on departure |
|---|---|---|---|---|---|
| **Tier 1** | OT intervention-tested clinical research | High–Moderate (depending on study design) | Experimental / quasi-experimental evidence | 1+ to 2+ | Closest mapping. Guidebook restricts to OT-relevant interventions; GRADE/JBI/SIGN do not filter by discipline. |
| **Co-1** | Lived experience / participatory design (CRPD Art. 4.3) | No analogue — GRADE excludes qualitative evidence from certainty ratings | Qualitative evidence (ConQual appraisal); Meaningfulness (FAME) | No analogue (nearest: level 4 expert opinion, but this mischaracterises lived experience) | **Major departure.** See §5. Co-1 is co-primary with Tier 1, not subordinate. No clinical framework grants this status. Justification is rights-based and epistemological, not methodological in the clinical sense. |
| **Tier 2** | NGO / DPO / advocacy guidelines | Very Low (expert opinion / non-analytic studies) | Text and opinion evidence | 4 | Clinical frameworks treat advocacy guidelines as lowest-quality evidence. Guidebook elevates them because DPOs are the closest proxy to aggregated lived experience when individual participatory research is unavailable. |
| **Co-2** | OT professional body CPGs (CAOT, AOTA, RCOT, COTEC, WFOT) | Varies — GRADE would appraise the CPG's own evidence basis | Expert opinion / text; or experimental if CPG cites primary research | 2– to 4 (depending on CPG basis) | CPGs are treated as Tier 3 with `[Tier 3 — CPG]` marker. They aggregate professional consensus, which is secondary to primary research but carries domain-specific validity. |
| **Tier 3** | Systematic reviews and meta-analyses | High (if well-conducted) | Systematic review evidence | 1++ to 1+ | Paradoxically lower than Tier 1 in the Guidebook. Reason: systematic reviews in built environment tend to review clinical outcomes, not spatial parameters. A systematic review of fall-prevention interventions may include grab bar studies but synthesises clinical effectiveness, not optimal grab bar dimensions. Indirectness downgrades the applicability. |
| **Tier 4** | International standards with evidence basis (ISO, IEC) | No analogue | No analogue | No analogue | Standards are not research. They are consensus-derived technical specifications. No clinical framework treats them as evidence. The Guidebook does because built environment practice treats standards as the primary specification source. Positioned below research evidence to prevent standards from overriding more direct population evidence. |
| **Tier 5** | National beyond-code frameworks | No analogue | No analogue | No analogue (nearest: good practice point) | Same logic as Tier 4. National frameworks (e.g., BS 8300, AS 1428) exceed statutory minimums and often encode accumulated professional knowledge. Below international standards because they are jurisdiction-specific. |
| **Tier 6** | Statutory codes (reference baseline only) | No analogue | No analogue | No analogue | Codes are legal floors, not evidence of optimal design. Included only as baseline reference. A specification that merely meets code is not evidence-based — it is compliance-based. |

### 4.1 Key Structural Differences

**Inversion of systematic reviews (Tier 3 below Tier 1):** In GRADE, systematic reviews of RCTs are the highest evidence level. In the Guidebook, they sit below direct OT intervention research because most available systematic reviews synthesise clinical outcomes (e.g., fall rates, independence scores) rather than spatial parameters (e.g., optimal corridor width, grab bar positioning). The leap from "grab bars reduce falls" (systematic review finding) to "grab bar shall be mounted at 850mm AFFL" (spatial specification) requires domain-specific OT research that systematic reviews rarely contain. Where a systematic review does directly address a spatial parameter, it functions at Tier 1 for that parameter.

**Standards and codes as evidence (Tiers 4–6):** Clinical frameworks have no analogue because clinical practice is not governed by building codes. The Guidebook must account for the fact that most practitioners will encounter standards before they encounter research. Positioning standards below research evidence prevents the common error of treating code compliance as best practice.

**No "Very Low" or "Level 4" equivalence for lived experience:** GRADE and SIGN would classify participatory design evidence at their lowest levels. The Guidebook rejects this classification. See §5.

---

## 5. Co-1 Justification — Lived Experience as Co-Primary Evidence

### 5.1 The Claim

Co-1 (lived experience / participatory design evidence) is co-primary with Tier 1 (OT intervention-tested clinical research). This means:

- Where Co-1 and Tier 1 evidence agree, the specification is well-supported.
- Where Co-1 and Tier 1 evidence conflict, neither automatically overrides. The conflict is escalated to evidence-auditor for adjudication, with the nature of the discrepancy documented.
- Where Tier 1 evidence is absent but Co-1 evidence exists, the specification proceeds with Co-1 as primary basis and an ○ marker (inferred) unless the Co-1 evidence is of sufficient quality and volume to warrant a ● marker.
- Where Co-1 evidence is absent but Tier 1 evidence exists, the specification proceeds on Tier 1 alone with a gap flag noting the absence of participatory validation.

### 5.2 Grounds

The co-primary status rests on three independent justifications — any one of which would be sufficient; together they are compelling.

#### 5.2.1 Legal-Normative Ground: CRPD Article 4.3

Article 4.3 of the Convention on the Rights of Persons with Disabilities requires States Parties to "closely consult with and actively involve persons with disabilities" in all decision-making processes concerning issues relating to them. General Comment No. 7 (2018) of the CRPD Committee elaborates that this obligation extends to "the design, implementation and monitoring of legislation, policies and programmes" — which includes design standards and building guidance.

The CRPD does not treat participation as a methodological nicety or a stakeholder engagement checkbox. It treats it as a right. A guidebook that claims alignment with the CRPD cannot relegate lived experience to the lowest evidence tier. Doing so would structurally ensure that the voices Article 4.3 mandates are heard could be overridden by any clinical study, however indirect its relevance to spatial design.

This is a normative argument, not a methodological one. It does not claim that lived experience is methodologically equivalent to a randomised trial. It claims that in a rights-based framework, the experiential knowledge of people who use spaces is not optional input — it is constitutive of what counts as good design.

#### 5.2.2 Epistemological Ground: Epistemic Privilege and Situated Knowledge

Disability studies scholarship (drawing on standpoint epistemology — Harding 1991, Collins 2000; and disability-specific applications — Charlton 1998, Oliver 1990) establishes that people with disabilities hold knowledge about their interaction with the built environment that is not accessible to non-disabled researchers or clinicians observing from outside that experience. This is not a claim of infallibility. It is a claim of epistemic access.

A wheelchair user navigating a bathroom transfer knows things about grab bar placement that a biomechanical study measuring force vectors does not capture — the fear of falling, the fatigue accumulation across a day, the adaptation strategies that make a theoretically suboptimal layout workable. An autistic person in a sensory environment knows whether a specification reduces distress in ways that a sound-level meter cannot measure.

JBI's FAME framework partially captures this through "Meaningfulness" — evidence about how people experience an intervention. But JBI still treats meaningfulness as subordinate to effectiveness. The Guidebook elevates it to co-primary because in built environment design, what the space feels like to the person using it is not a secondary consideration — it is the primary design criterion. A space that meets every measurable performance target but is experienced as hostile, frightening, or exhausting by its intended users has failed.

#### 5.2.3 Methodological Ground: Structural Absence of Direct Evidence

For many built environment specifications, no clinical trial exists and none is feasible. The question "What is the optimal bedroom layout for a person with ME/CFS who spends 18 hours per day in bed?" cannot be answered by an RCT. The population is too heterogeneous, the outcome measures too multi-dimensional, the environmental variables too numerous, and the ethical constraints on randomising severely ill people to suboptimal bedroom designs too obvious.

In these domains — and they constitute a substantial proportion of the Guidebook's specification scope — lived experience is not a weak substitute for unavailable research. It is the only form of direct evidence that exists. Relegating it to the lowest tier would mean that the specifications most in need of user input would be the specifications least informed by it.

SIGN's "good practice points" partially address this gap by legitimising recommendations based on clinical experience in the absence of research evidence. The Guidebook extends this logic: where no research evidence exists for a spatial parameter, the experience of people who live with that spatial parameter daily is the most direct evidence available.

### 5.3 Quality Appraisal for Co-1 Evidence

Co-primary status does not mean unappraised status. Co-1 evidence is subject to quality assessment:

| Quality dimension | Assessment method |
|---|---|
| **Credibility** | Does the account describe a plausible interaction between functional capacity and spatial parameter? Is the described experience consistent with known physiology/ergonomics? |
| **Transferability** | Is the experience described specific to a unique context, or does it describe a pattern likely shared across people with similar functional profiles? |
| **Dependability** | Is the source a single anecdote, a qualitative study, a DPO consultation, or a large-scale participatory design project? Volume and diversity of sources increase dependability. |
| **Confirmability** | Can the described experience be corroborated by other Co-1 sources, by Tier 1 research, or by physiological reasoning? |
| **CRPD alignment** | Was the evidence gathered through processes consistent with Article 4.3 (active involvement, not tokenistic consultation)? |

These dimensions adapt JBI's qualitative appraisal criteria for the built environment context.

### 5.4 Co-1 Pass Requirements

Per project-standards: BPC entries require Co-1 passes across at least 9 of 14 search languages before a best-practice claim is considered adequately grounded. This is the operational expression of co-primary status — Co-1 is not a supplementary check but a mandatory evidence-gathering phase with explicit coverage requirements.

---

## 6. Co-2 — OT Professional Body CPGs

OT clinical practice guidelines (CPGs) from AOTA, RCOT, CAOT, COTEC, OT Australia, and WFOT are classified as Tier 3 with a `[Tier 3 — CPG]` marker. This positions them:

- Below Tier 1 (direct OT intervention research) because CPGs synthesise and interpret evidence rather than generating it.
- At the same level as systematic reviews because CPGs typically conduct or incorporate systematic evidence reviews.
- Above Tier 4 (international standards) because CPGs carry clinical-professional authority specific to the populations the Guidebook addresses.

The `[Tier 3 — CPG]` marker ensures that CPGs are not conflated with academic systematic reviews. CPGs carry a stronger practice-relevance signal (they are written to guide practitioner decisions) but a weaker methodological-rigour signal (they may incorporate expert consensus alongside evidence review).

---

## 7. Recommendation Strength Protocol

### 7.1 Why GRADE's Binary Model Does Not Fit

GRADE uses a binary recommendation strength: strong ("we recommend") or conditional/weak ("we suggest"). This binary works for clinical interventions where the question is "should this treatment be offered?" In built environment specification, the question is "what value should this spatial parameter take?" — a continuous, not binary, decision.

A specification like "corridor width shall be ≥ 1200mm" is not a recommendation that corridors exist. It is a quantitative performance target. "Strong vs. conditional" does not capture the relevant distinction. The relevant distinction is between:

- A specification value derived from direct evidence about that parameter.
- A specification value inferred from adjacent evidence, clinical reasoning, or professional consensus.

### 7.2 The ● / ○ System

The Guidebook uses two evidence markers:

| Marker | Meaning | Basis |
|---|---|---|
| ● (filled circle) | Evidence-based specification | Directly supported by Tier 1–6 evidence addressing this specific parameter for this population |
| ○ (empty circle) | Inferred specification | Derived from clinical reasoning, expert consensus, analogy from adjacent parameters, or extrapolation from evidence for a different population. Gap disclosed. |

Every specification sentence carries one marker. Unmarked = error.

### 7.3 Mapping ● / ○ to Recommendation Frameworks

| Marker | GRADE analogue | JBI analogue | SIGN analogue |
|---|---|---|---|
| ● | Strong recommendation based on moderate-to-high certainty evidence | Recommendation based on evidence of effectiveness and/or meaningfulness | Grade A–C recommendation |
| ○ | Conditional recommendation based on low/very low certainty evidence | Recommendation based on expert opinion/consensus; or good practice point | Grade D or good practice point |

### 7.4 Strength Modifiers

Within the ● category, the Guidebook does not further stratify recommendation strength. The evidence tier of the supporting source is recorded in the BPC Key sources table and can be inspected, but the specification itself carries only ● or ○. This is a deliberate simplification. Practitioners need to know whether a specification is evidence-based or inferred. They do not need to know whether the evidence is Tier 1 or Tier 4 to implement the specification — that granularity serves the evidence auditor and future research prioritisation, not the design practitioner.

### 7.5 Tier Interaction with Markers

A specification can receive ● from any tier (Tier 1 through Tier 6) provided the evidence directly addresses the spatial parameter in question. A Tier 6 statutory code that specifies a minimum corridor width of 1000mm provides direct evidence for the parameter "corridor width" — the specification receives ● with Tier 6 cited. That same code does not provide evidence for optimal corridor width for two wheelchair users passing — a specification for that scenario derived by extrapolation receives ○.

The marker tracks directness of evidence, not tier. The tier tracks quality of the evidence source.

---

## 8. Three-Tier Design Hierarchy and Evidence Integration

The evidence hierarchy and recommendation strength protocol operate within the Guidebook's Three-Tier Design Hierarchy:

| Design tier | Evidence role | Marker expectation |
|---|---|---|
| **Tier 0** — Universal Design / Code Compliance | Population-agnostic, fixed values. Evidence from statutory codes (Tier 6) and international standards (Tier 4). All specifications at this level should be ●. | ● expected; ○ = gap requiring escalation |
| **Tier 1** — Population-Informed Inclusive Design | Ranges derived from population evidence. Evidence from Tier 1, Co-1, Tier 2–5. Median as default. | ● for well-evidenced populations; ○ acceptable with gap disclosure |
| **Tier 2** — Person-Specific Co-Design | OT assessment resolves position within Tier 1 range. Not a specification level — a handoff protocol. No evidence marker applies (the individual OT assessment is the evidence). | No marker — outside specification scope |

---

## 9. Handling Absent or Contradictory Evidence

### 9.1 Absent Evidence

When no evidence of any tier exists for a spatial parameter:

1. The specification is drafted from clinical reasoning and/or professional consensus.
2. It receives ○.
3. A gap item is raised: `[GAP: {parameter} — no evidence identified for {population}]`.
4. The BPC entry records the absence explicitly in the Co-1 pass summary.
5. Future research prioritisation uses the coverage matrix (Phase 2D, CO-0006) to identify systematic gaps.

### 9.2 Contradictory Evidence

When evidence from different tiers or different populations contradicts:

1. The contradiction is documented in the BPC entry.
2. Evidence-auditor adjudicates using the principle: higher-tier evidence addressing the same population and the same parameter governs.
3. If the contradiction is between populations (e.g., FMS thermal preference vs. MS/SCI thermal tolerance), it is a co-occurrence conflict — routed to Part 5 and resolved by harm-asymmetry analysis (per project-standards), not by evidence-tier ranking.
4. If Co-1 evidence contradicts Tier 1 evidence for the same population and parameter, the conflict is surfaced without resolution. Neither overrides. The specification notes both sources and the unresolved discrepancy.

### 9.3 Contradicted BPC Claims

Per project-standards: when functional-deficit-researcher (FDR) evidence contradicts a BPC best-practice claim, the original claim is not deleted. It is tagged `[CONTRADICTED BY FDR]` and routed to evidence-auditor for adjudication. This preserves the audit trail and prevents evidence loss.

---

## 10. Limitations and Transparency Commitments

### 10.1 Limitations

1. **No clinical framework validates Co-1 co-primary status.** The justification in §5 is rights-based and epistemological, not derived from GRADE, JBI, or SIGN methodology. Readers accustomed to clinical evidence hierarchies will find this departure significant.

2. **The ● / ○ binary is coarse.** It does not capture the difference between a specification supported by a well-designed quasi-experimental study (Tier 1) and one supported by a statutory code (Tier 6). This is a deliberate trade-off: practitioner usability over methodological granularity.

3. **Co-1 quality appraisal is not standardised.** The dimensions in §5.3 are adapted from JBI qualitative criteria, but no validated appraisal tool exists for participatory design evidence in the built environment domain. Appraisal is currently conducted by Opus synthesis, which carries reduced confidence when `opus_synthesis: false`.

4. **Tier placement of standards (Tiers 4–6) is a value judgment.** A jurisdiction where the statutory code exceeds international standards (e.g., Sweden's BBR/BFS) would see its code placed at Tier 5 or even Tier 4 rather than Tier 6. Tier assignment for standards should follow the evidence basis of the standard, not its legal status — but in practice the evidence basis of most building codes is opaque.

### 10.2 Transparency Commitments

1. Every specification carries ● or ○. No unmarked specifications.
2. Every ● specification cites at least one source with tier and REF-ID.
3. Every ○ specification discloses the gap and the basis for inference.
4. Every BPC entry records Co-1 pass status (languages searched, yield).
5. The coverage matrix (CO-0006 Phase 2D) identifies systematic evidence gaps across populations, topics, and jurisdictions.
6. This methodology document is versioned and updated when the evidence hierarchy changes.

---

## 11. Revision History

| Date | Change | Author |
|---|---|---|
| 2026-04-08 | Initial draft — Phase 1A, CO-0006 | Opus 4.6 |
