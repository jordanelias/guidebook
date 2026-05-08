<!-- DEPRECATED 2026-05-08 04:16 -->
> **⚠ DEPRECATED:** SUPERSEDED — Stage 0 audit. All 31 findings resolved and mapped in workplan-co0007-v4.md §Finding-resolution map. Historical reference only.

> **SUPERSEDED 2026-04-25 00:19** by `workplan/workplan-co0007-synthesis.md`.
>
> This audit workplan was drafted before the conversation surfaced the architectural shift to structured data and multi-modal navigation. It treats markdown as the deliverable form; the synthesis workplan treats markdown as interim and structured data as the long-term form. The audit-as-byproduct approach in the synthesis subsumes this audit.
>
> Retained in repo for traceability and partial reuse (triage method, evidence audit method, propagation thinking, pilot principle). Do not execute as written.

---

# CO-0007 Audit Workplan: Foundational Principles Alignment
**Created:** 2026-04-24 23:42
**Triggered by:** Bathroom turning space 1500mm identified as code-consensus value, not best practice
**Governing principles:** Core Doctrine rules 1–5 (enshrined 2026-04-24)

---

## Scope

Every asset in the project evaluated against the five foundational principles:

1. **Purpose:** Does it help people ask the right questions?
2. **Non-uniformity:** Does it acknowledge that disability populations are not uniform?
3. **Three-Tier Hierarchy:** Does it differentiate Universal Mode/1/2?
4. **Evidence Hierarchy:** Is the value derived from the correct evidence tier?
5. **Best Practice:** Does it provide the most accommodating, thoughtful, respectful, dignified, usable condition?

### Assets

| Asset | Count | Audit type |
|---|---|---|
| Part 4 item specifications | 92 | Full (every item) |
| BPC files (flat + per-slug) | ~78 | best_practice_synthesis + consensus findings |
| Spec-database records | 73 | Value source tracing |
| Appendix A tables | 20 | Value correctness |
| Skills (evidence-governing) | 5 | Methodology alignment |
| Parts 1–3 (framework text) | 3 | Language and framing |
| Parts 5–7 (conflicts, matrices) | 3 | Conflict resolution methodology |
| Opus divergence synthesis | 1 | Recommendations review |
| Connection register | 1 | Basis validity |
| Project standards | 1 | Internal consistency |

---

## Phase 0: Skill Modifications (change the tools first)
**Model:** Sonnet
**Sessions:** 2
**Rationale:** All subsequent audit work uses these skills. Fix the tools before fixing the outputs.

### 0A: multilingual-research_SKILL.md
- Rename "Consensus findings" → "Code convergence findings" (Tier 5–6 only)
- Add "Clinical evidence findings" table (Tier 1–3, Co-1, Co-2)
- Add mandatory synthesis prompts: functional variability, co-occurrence, tier differentiation
- Add three-gate synthesis check: [CODE-FLOOR-ONLY], [UNIFORMITY-ERROR], [CO-OCCURRENCE-ABSENT]
- Add "Questions for the designer" as mandatory BPC output section

### 0B: item-specification-writer_SKILL.md
- Add three mandatory sections to item format: Questions for the designer, Functional variability, Co-occurring conditions
- Reframe specification output: values serve the questions, not the other way around
- Add tier differentiation requirement to every measurable parameter
- Update best-practice derivation rule: most accommodating/dignified/usable, not code consensus
- Update population code guidance: comprehensive at Universal Mode, insight at Tier 1, step aside at Tier 2

### 0C: Supporting skills audit
- evidence-auditor: add [CODE-FLOOR-NOT-BP] check
- connection-scout: verify connection basis against corrected values
- critique-report-writer: add CO-0007 compliance criteria
- vol2-item-formatter: add formatting for new mandatory sections

---

## Phase 1: Triage (classify every item by risk)
**Model:** Sonnet
**Sessions:** 3–4
**Input:** Part 4 (92 items), full read
**Output:** `references/co0007-triage-matrix.md`

### Method
Read every item specification. For each, classify:

| Column | Values | Definition |
|---|---|---|
| measurable_value | Y/N | Does the item have a dimensional, performance, or threshold value? |
| value_source_tier | 1–6 / MIXED / NONE | What is the highest-tier evidence supporting the primary value? |
| code_floor_risk | HIGH/MED/LOW | Is the value potentially derived from code consensus rather than Tier 1–3 evidence? |
| functional_variability | PRESENT/ABSENT/PARTIAL | Does the spec discuss how the population varies for this parameter? |
| co_occurrence | PRESENT/ABSENT/PARTIAL | Does the spec discuss co-occurring conditions? |
| questions_for_designer | PRESENT/ABSENT | Does the spec guide the designer to ask the right questions? |
| tier_differentiation | PRESENT/ABSENT/PARTIAL | Does the spec differentiate Universal Mode/1/2 values? |
| risk_level | CRITICAL/HIGH/MEDIUM/LOW | Overall audit priority |

### Risk classification rules
- **CRITICAL:** measurable_value=Y AND code_floor_risk=HIGH AND functional_variability=ABSENT
- **HIGH:** measurable_value=Y AND (code_floor_risk≥MED OR functional_variability=ABSENT)
- **MEDIUM:** measurable_value=Y AND code_floor_risk=LOW AND functional_variability=PARTIAL
- **LOW:** measurable_value=N OR (all checks PRESENT)

### Predicted distribution (based on initial scan)
- CRITICAL: ~15 items (spatial dimensions, grab bars, controls)
- HIGH: ~20 items (sensory thresholds, thermal, additional spatial)
- MEDIUM: ~25 items (partial compliance, need enrichment)
- LOW: ~32 items (beyond-code items with no measurable value, MERGED markers)

---

## Phase 2: Evidence Audit (trace every value to its source)
**Model:** Sonnet (research) + Opus (judgment)
**Sessions:** 12–18
**Input:** CRITICAL and HIGH items from triage (~35 items)
**Output:** `references/co0007-evidence-audit/` (one file per item or batch)

### Per-item audit procedure

**Step 1: Extract claims**
- Current Part 4 specification value(s)
- BPC best_practice_synthesis claim
- BPC consensus findings row
- Spec-database record value
- Appendix A table value (if applicable)

**Step 2: Trace evidence**
- What tier is the current value from? Follow the citation chain.
- Does Tier 1–3 evidence exist for this parameter? (Web search if needed)
- Does Co-1 evidence exist? (Lived experience studies)
- What do the OT CPGs (Co-2) say?
- What is the full jurisdiction spread? (Not just consensus — all 46)

**Step 3: Assess**
- Is the current value the most accommodating/dignified/usable the evidence supports?
- Or is it a code floor being presented as best practice?
- What functional variability exists within the population for this parameter?
- How does co-occurrence affect the parameter?
- What questions should the designer be asking?

**Step 4: Verdict**
- [CONFIRMED]: value is evidence-supported best practice
- [CODE-FLOOR]: value matches code consensus but Tier 1–3 evidence supports a different value
- [UNIFORMITY-ERROR]: single value given for variable population
- [UPGRADE-NEEDED]: value is defensible but tier differentiation / variability / co-occurrence missing
- [RESEARCH-GAP]: no Tier 1–3 evidence exists; value is necessarily Tier 5–6 derived (acceptable with disclosure)

### Batching strategy (by parameter domain)
| Batch | Items | Sessions | Domain |
|---|---|---|---|
| 2A | E-01, E-06, E-08, E-12, G-04 | 2–3 | Turning space / clear floor |
| 2B | G-03, G-04 (grab bars), I-01 | 2 | Grab bars / transfer / dressing |
| 2C | H-01, H-02, H-03, H-04, H-05 | 2 | Controls / reach / force |
| 2D | E-03, E-04, E-05, E-07, E-11 | 2 | Ramps / parking / doors / slip |
| 2E | A-04, A-10, A-11, A-14 | 2 | Acoustics / hearing loop |
| 2F | B-01, B-02, B-05, B-10 | 2 | Lighting / visual alarms |
| 2G | C-04, C-05, D-08 | 1 | Contrast / signage |
| 2H | F-07, F-08, E-06 threshold | 1–2 | Thermal / threshold |
| 2I | Remaining HIGH items | 2–3 | Mixed |

---

## Phase 3: BPC Correction
**Model:** Sonnet (corrections) + Opus (synthesis rewrite where needed)
**Sessions:** 8–12
**Input:** Phase 2 verdicts
**Output:** Corrected BPC files committed to GitHub

### Per-item correction procedure

**For [CODE-FLOOR] verdicts:**
1. Rewrite best_practice_synthesis to derive from Tier 1–3 evidence
2. Rename "Consensus findings" rows to "Code convergence" in the BPC
3. Add "Clinical evidence" rows where Tier 1–3 data exists
4. Add functional variability paragraph
5. Add co-occurrence paragraph
6. Add synthesis gate confirmation

**For [UNIFORMITY-ERROR] verdicts:**
1. Add functional variability narrative to best_practice_synthesis
2. Describe the range of experience within the population for this parameter
3. Identify what drives variation (device type, strength, cognition, fatigue, co-occurrence)
4. State the Universal Mode value (widest reasonable range) vs Tier 1 range vs Tier 2 trigger

**For [UPGRADE-NEEDED] verdicts:**
1. Add missing sections (variability, co-occurrence, tier differentiation)
2. Value itself may be acceptable — enrich the surrounding context

**For [RESEARCH-GAP] verdicts:**
1. Add [RESEARCH-GAP: no Tier 1–3 evidence for this parameter] disclosure
2. State that current value is Tier 5–6 derived with appropriate confidence caveat
3. Flag for future research

### Batching
Batch by BPC file, not by item — a single BPC file may feed multiple items. Process the BPC once per file, correcting all items it feeds.

---

## Phase 4: Specification Rewrite
**Model:** Opus (narratives require cross-referential judgment)
**Sessions:** 15–20
**Input:** Corrected BPC files, Phase 2 evidence audit
**Output:** Corrected Part 4 item specifications committed to GitHub

### Per-item rewrite procedure

**Step 1: Correct values** where Phase 2 identified [CODE-FLOOR]
- Replace code-consensus value with evidence-supported best practice
- Add tier differentiation: Universal Mode value, Tier 1 range, Tier 2 trigger

**Step 2: Add "Questions for the designer"**
- What non-obvious considerations does this element require?
- What should the designer be thinking about?
- What circumstances change the answer?
- When should they consult an OT?
- What common assumptions are wrong?

**Step 3: Add "Functional variability"**
- Narrative describing the range of functional experience
- What drives variation for this specific parameter
- Concrete examples (not abstract categories)

**Step 4: Add "Co-occurring conditions"**
- Which conditions commonly co-occur
- How co-occurrence compounds the functional requirement
- Which co-occurrence patterns are most clinically significant

**Step 5: Update jurisdiction comparison table**
- Ensure the table shows the full range, not just consensus
- Flag where codes are behind the evidence
- Note which jurisdictions have adopted evidence-based values vs code-floor values

**Step 6: Opus cross-check**
- Verify internal consistency (description, specification, evidence basis, jurisdiction table)
- Verify cross-references still valid after value changes
- Verify conflict notes still accurate

### Batching
Same domain batches as Phase 2. Opus sessions handle 3–5 items each.

---

## Phase 5: Cross-Cutting Audit
**Model:** Opus
**Sessions:** 6–8

### 5A: Parts 1–3 Framework Text (2–3 sessions)
- Part 1: Does the introduction frame the guidebook as a questioning tool, not a prescription manual? Does it state that disability populations are not uniform? Does it explain co-occurrence?
- Part 2: Do population descriptions acknowledge within-population variability?
- Part 3: Does the methodology explain the evidence hierarchy correctly? Does it frame best practice as most accommodating/dignified, not code consensus?

### 5B: Parts 5–7 Conflict Resolution (2 sessions)
- Part 5: Do building-level conflict resolutions assume uniform populations?
- Parts 6–7: Do room matrices and conflict notes account for functional variability and co-occurrence?
- Are conflict resolution defaults based on harm asymmetry (correct) or population-averaging (incorrect)?

### 5C: Appendix A Tables (1 session)
- Do the 20 jurisdiction comparison tables present code values as context, not as best practice?
- Are they framed correctly: "this is what codes require; this is what the evidence supports"?

### 5D: Opus Divergence Synthesis (1 session)
- Do the 13 parameter-level syntheses apply the correct best-practice definition?
- The turning space synthesis (L101–105) already says "By device type" — verify this framing is applied consistently across all 13 parameters.

### 5E: Connection Register (1 session)
- Do connections (189 entries) still hold after value corrections?
- Any connections based on code-floor values that are now superseded?

---

## Phase 6: Propagation and Verification
**Model:** Sonnet
**Sessions:** 5–8

### 6A: Spec-database update (2 sessions)
For every corrected value, update the corresponding record in specification-database.json:
- Value field
- Source tier
- Functional variability flag
- Co-occurrence flag

### 6B: Cross-reference verification (1–2 sessions)
Run cross-reference resolver on all modified files. Verify:
- REF-IDs still resolve
- CON-IDs still valid
- Item cross-references still correct

### 6C: Appendix A update (1 session)
Update tables where values have changed. Reframe tables to distinguish code values from evidence-based best practice.

### 6D: Bibliography impact (1 session)
Any new sources added during Phase 2 evidence audit → add to bibliography-v11-draft.md.
Any sources reclassified (e.g., Tier 6 code used as Tier 1 evidence) → correct tier markers.

### 6E: Validation (1–2 sessions)
Run all three validators (validate_bpc.py, validate_cross_refs.py, check_thresholds.py).
Manual spot-check: select 10 items across risk levels, verify full propagation chain (BPC → spec-db → Part 4 → Appendix A).

---

## Phase 7: Skill Verification
**Model:** Sonnet
**Sessions:** 1–2

### 7A: Test the modified skills
Run the modified multilingual-research skill on one NEW slug (not previously researched) to verify:
- Synthesis produces clinical evidence findings table (not just code convergence)
- Best_practice_synthesis derives from Tier 1–3 evidence
- Functional variability and co-occurrence prompts produce useful output
- Questions for the designer are generated

### 7B: Run modified ISW on one item
Take one CRITICAL item that was corrected in Phase 4 and regenerate it from scratch using the modified ISW skill. Compare with the manually corrected version. Verify alignment.

---

## Summary

| Phase | Sessions | Model | Output |
|---|---|---|---|
| 0: Skill modifications | 2 | Sonnet | 5 modified skill files |
| 1: Triage | 3–4 | Sonnet | Triage matrix (92 items) |
| 2: Evidence audit | 12–18 | Sonnet + Opus | Evidence audit files (~35 items) |
| 3: BPC correction | 8–12 | Sonnet + Opus | Corrected BPC files |
| 4: Specification rewrite | 15–20 | Opus | Corrected Part 4 |
| 5: Cross-cutting audit | 6–8 | Opus | Parts 1–3, 5–7, Appendix A, connections |
| 6: Propagation + verification | 5–8 | Sonnet | Spec-db, bibliography, validators |
| 7: Skill verification | 1–2 | Sonnet | Test results |
| **Total** | **52–74** | | |

### Critical path
Phase 0 → Phase 1 → Phase 2 → Phase 3 + Phase 4 (parallel by batch) → Phase 5 → Phase 6 → Phase 7

Phase 0 must complete first (tools govern all downstream work).
Phase 1 must complete before Phase 2 (triage determines priority).
Phases 3 and 4 can run in parallel by batch (correct BPC then rewrite spec in same session).
Phase 5 can begin after Phase 4 batch 2A completes (spatial items inform framework text).
Phase 6 runs after all corrections committed.
Phase 7 is final validation.

### Decision points requiring human input
- Phase 1 triage results: confirm risk classifications before proceeding to Phase 2
- Phase 2 evidence audit: for items where Tier 1–3 evidence conflicts, human adjudicates
- Phase 4 specification rewrite: "Questions for the designer" sections need human review (are these the RIGHT questions?)
- Phase 5A: Part 1 reframing needs human approval (it changes the public-facing introduction)

### Estimated timeline
At 2 sessions per day: 26–37 working days.
At 3 sessions per day: 17–25 working days.
At mixed pace (some days intensive, some not): ~6–8 weeks.
