# CO-0007 Stage 0.5 — Pre-Stage-A Doctrinal Decisions: Materials Package
**Created:** 2026-04-26 02:23 UTC
**Stage:** 0.5 (Pre-Stage-A doctrinal decisions)
**Resolves audit findings:** T-03 (Co-1 tier encoding), T-04 (sparse-evidence behavior), D-03 (Co-1 operational role)
**Status:** Decision materials — pending project-owner decisions
**Output expected after decisions:** `governance/pre-stage-a-decisions.md` (committed)

---

## Why this stage exists

Workplan v3 §0.5 stages three audit-flagged Critical/Medium decisions before Stage A begins because they shape the schema (B1) and validator (B2) design. Deferring them to A6 alone produces architectural incoherence. Audit v2 §Pre-adoption blockers names them as the doctrinal questions the owner must decide before Stage A starts.

This package presents each decision with:
- The question
- Current live-state evidence relevant to the decision
- Options with implications
- Cross-decision interactions
- A recommendation (Claude's judgment, not binding)

You decide. After you decide, I commit `governance/pre-stage-a-decisions.md` capturing your selections + rationale.

---

## Decision 1 · T-03 · Co-1 tier encoding

### The question

How is Co-1 represented in evidence-claim records? Three plausible schemas:

- **Option A · Single `tier` field with Co-1 as a Tier-1 marker.** Co-1 records use `tier: 1` plus some flag like `evidence_subtype: lived_experience`.
- **Option B · `tier` + `evidence_type` taxonomy.** Two fields: `tier: 1`, `evidence_type: clinical | co1 | co2 | sr_meta`. Schema accommodates Co-1 and Co-2 as parallel positions.
- **Option C · Co-1 as separate dimension.** `tier` ranges 1–6 for clinical evidence; `co_position` ranges Co-1, Co-2, none. Two parallel ladders, not a single hierarchy.

### Live-state evidence

Project-standards line 17 (committed 2026-04-24 23:46):
> *Tier 1 = OT intervention-tested clinical research; Co-1 = lived experience / participatory design (CRPD Art. 4.3, **co-primary with Tier 1**); Tier 2 = NGO/DPO/advocacy guidelines; Co-2 = OT professional body CPGs; Tier 3 = systematic reviews and meta-analyses; Tier 4 = international standards with evidence basis; Tier 5 = national beyond-code frameworks; Tier 6 = statutory codes (reference baseline only). OT body guidelines = Tier 3 with [Tier 3 — CPG] marker.*

Live spec-database (`references/specification-database.json`) uses `evidence_tier` as a single field. Sample records use values like `"Tier 1"`, `"Tier 4"`, `"Co-1"`. No schema documentation specifies allowed values. Co-1 currently appears as a string value in the same field — **Option A behavior** in implementation, but not formally schemaed.

Live BPC files use `Tier`-prefixed labels in body text (e.g., "Tier 1", "Co-1", "Tier 4–6") — informal natural-language tagging.

The doctrinal rule treats Co-1 as **co-primary with Tier 1**, not as Tier 1. Co-1 sits parallel to Tier 1 in the seven-tier formulation; the same applies to Co-2 parallel to Tier 2. The wording "co-primary with Tier 1" is structurally incompatible with Option A's "Co-1 IS Tier 1" encoding — these are semantically different claims.

### Options · implications

| Option | Schema simplicity | Doctrinal fidelity | Validator impact | Rendering distinction |
|---|---|---|---|---|
| A · single `tier` | Highest | Lowest — flattens "co-primary" into "is-1" | Validators read one field | Hard to distinguish clinical-T1 from Co-1-T1 in renders |
| B · `tier` + `evidence_type` | Moderate | High — preserves parallel-position semantics | Validators consult two fields; tier discipline straightforward | Easy: `evidence_type` drives icon/label |
| C · two-dimension | Low | Highest — explicitly two ladders | Validators must reason over two dimensions; combination logic non-trivial | Most expressive but most complex UI |

### Cross-decision interactions

- T-03 affects T-04 (sparse-evidence behavior). In Option A, "sparse Tier-1" includes sparse Co-1; in Options B/C, they're independent dimensions and a population could be Tier-1-thin but Co-1-rich, which has different implications.
- T-03 affects D-03 (Co-1 operational role). If Co-1 is its own dimension (Options B/C), Co-1 records are first-class artifacts that need their own authoring workflow. Option A might encourage treating Co-1 as a flag on Tier 1 records (lower visibility for Co-1 contribution).

### Recommendation

**Option B (`tier` + `evidence_type`).** Reasons:

1. **Doctrinally faithful** — preserves "co-primary with Tier 1" without flattening it.
2. **Operationally simple** — validators consult two fields, not two dimensions; queries straightforward.
3. **Renderable** — distinct icon/label per evidence_type lets readers see *what kind* of evidence backs a claim, which supports the project's questions-led, evidence-distinctions epistemic commitment.
4. **Compatible with current practice** — the live spec-database already uses string-value differentiation; this formalizes it.

Option C is doctrinally cleanest but operationally heaviest. Option A is operationally simplest but contradicts the doctrinal text.

### Cross-references

- B1 schema design adopts the chosen encoding.
- B2 evidence-tier-validator (Co-1-aware) reads the chosen encoding.
- A6 evidence methodology specifies authoring rules for each evidence_type.
- C2 builds the validator and rendering skills around the encoding.

---

## Decision 2 · T-04 · Sparse-evidence behavior

### The question

What does "best practice" mean when Tier 1–3 clinical evidence and Co-1 corpus are both sparse? Three options:

- **Option A · `[BEST-PRACTICE-PENDING]` marker with research-gap pointer.** Best practice not stated; a structured marker says "evidence sparse — see research gap GAP-NNN." Reader sees the gap explicitly.
- **Option B · Reduced-confidence best-practice category.** Best practice IS stated, with a structural distinction in rendering (e.g., "Provisional best practice" with confidence rating). Lower bar for evidence sufficiency, but the claim is made.
- **Option C · Doctrinal silence.** No best practice stated until corpus reaches threshold. The guidebook is honest about its silences.

### Live-state evidence

The doctrinal rule (project-standards line 20) defines best practice as derived from the evidence hierarchy. Sparse-evidence cases produce a logical gap: if best practice requires evidence and evidence is absent, what is best practice?

Live BPCs already exhibit all three behaviors:

- **STUB pattern** (per Stage 0.4 §F3): files like `accessible-design-failures-poor-performance.md` carry "[STUB — Opus synthesis pending]" — operationally close to **Option A**.
- **PROVISIONAL pattern**: files like `residential-kitchen-and-task-surfaces.md` carry "Status: PROVISIONAL retained" with synthesis present but evidence-base flagged as European-dominated — operationally close to **Option B**.
- **GAP pattern**: gap_register.md tracks GAP-079, GAP-CITE-01, GAP-LRP-01 etc. Some BPC areas are not synthesized at all — operationally close to **Option C**.

So the corpus already runs all three patterns inconsistently. The decision is which to canonicalize.

External yardstick (audit v2 §T-04): Cochrane practice distinguishes:
- *absence of evidence* (Option C — silence is honest)
- *evidence of absence* (best practice = "X does not work" — substantive claim)
- *primary evidence at non-clinical tier* (Co-1 alone, low-Tier surveys — Option B with explicit qualification)

Each warrants different output.

### Options · implications

| Option | User experience | Doctrinal honesty | Implementation | Risk |
|---|---|---|---|---|
| A · `[BEST-PRACTICE-PENDING]` | Reader sees: "we don't know yet — see GAP-NNN" | High — silence with traceability | Marker + gap-register cross-link; renderer treats as a state | Designers using guidebook find empty cells with no actionable advice |
| B · reduced-confidence | Reader sees: "Provisional [low confidence]: X" with caveat | Moderate — claim is made but flagged | Confidence field; renderer changes presentation | Doctrinal slip risk — provisional claims accumulate, become de facto authority |
| C · silence | Reader sees: nothing for that population/parameter | Highest — guidebook owns its limits | No marker; population/parameter intersection simply absent | Designers conclude population is "fine without provision" — silent harm |

### Cross-decision interactions

- T-04 + T-03: if `evidence_type` is a field (T-03 Option B), sparse-evidence behavior can vary by evidence_type. Sparse clinical with rich Co-1 might warrant Option B for that evidence_type. Sparse-everything warrants Option A or C.
- T-04 + D-03: if Co-1 is operationally co-author (D-03 Option Co-author), sparse cases might be filled by Co-1 drafting before being filled by clinical evidence — different from a Tier-1-only-sparse case.
- T-04 + C7 (bibliography residual): the 81 [GREY] sources in `bibliography-v11-draft.md` are a bibliography-side analog to BPS-side sparseness. Same disposition framework should apply (re-verify, deprecate, retain with marker).

### Recommendation

**Hybrid: Option A as default, Option B for evidence_type-specific cases when ≥1 evidence type is rich.**

Specifically:
- **`[BEST-PRACTICE-PENDING]` marker** for cells where Tier 1–3 *and* Co-1 are both sparse. Cross-link to gap-register entry. Renderer shows the gap visibly.
- **`provisional best practice` (with confidence flag)** for cells where one evidence dimension is rich but the other is sparse — e.g., strong Co-1 but no clinical RCT — and the claim is supported by the rich dimension alone.
- **No silence (Option C)** as default — silent intersections produce silent harm. If a specific parameter must be marked silent (e.g., legitimately no design implication for a population), it is an explicit "Not Applicable" state, not absence.

This is more complex than picking one option, but it matches the empirical pattern already in the corpus and is defensible to external critique because each cell's status is explicit.

### Cross-references

- A6 evidence methodology specifies the marker format and gap-link protocol.
- B1 schema includes `best_practice_status: stated | provisional | pending | not_applicable` field.
- B2 validators check the state machine (e.g., "pending" requires gap-register entry).
- C2 builds the marker tooling and renderer behavior.

---

## Decision 3 · D-03 · Co-1 operational role

### The question

Is Co-1 operationally **co-author** (drafting role on the work itself) or operationally **reviewer** (approval role on work drafted by others)?

The doctrine claims co-author. Audit v2 §D-03 (Critical) finds the operational structure delivers reviewer. The choice is to either:

- **Option Co-author** — operational structure changes to honor the doctrine. Co-1 collaborators draft sections, are named as authors, and have decision authority on at least some final outputs.
- **Option Reviewer** — mission language updates to honesty. Doctrine is rewritten to say "Co-1 is the project's primary review constituency" — defensible position but a different one.

### Live-state evidence

Live state shows the audit's finding: Co-1 is currently practiced as reviewer (approve/reject specific findings) in the OPUS-SYNTHESIS pattern. There is no live evidence of Co-1 drafting BPC sections. The Co-1 corpus is research evidence (Co-1 sources in tier-JSON) — Co-1 *as evidence type* is co-primary with Tier 1, but Co-1 *as collaborators* (people) is currently absent from drafting.

Audit v2 §D-03 cross-references co-design / participatory research literature: the five markers of co-authorship (vs. reviewer) are co-determination of research questions, co-curation of evidence, co-drafting of artifacts, named authorship credit, decision authority on final outputs.

The mission says "Co-1 lived experience / participatory design (CRPD Art. 4.3, co-primary with Tier 1)." The CRPD Art. 4.3 reference mandates *consultation with* and *active involvement of* persons with disabilities through their representative organizations. Active involvement is operationally co-author shaped, not reviewer shaped.

The audit's argument: the doctrine claims more than the operations deliver. The choice is fix the operations (Option Co-author) or fix the doctrine (Option Reviewer).

### Options · implications

| Option | Resourcing required | Mission language honesty | Project defensibility | Risk |
|---|---|---|---|---|
| Co-author | High — DPO partnerships, compensation, authorship credit infrastructure, recruitment | Doctrine and operations match | High — practice matches CRPD intent and co-design literature | Methodological-limit declaration if resourcing fails |
| Reviewer | Moderate — review honoraria, reviewer recruitment, decision authority on review-only items | Doctrine rewritten to match operations | Moderate — defensible as "Co-1 is project's review constituency" | Reduces audit D-03 from Critical to no longer a finding, but the project signals less ambition |

### Cross-decision interactions

- D-03 + T-03: if Co-1 is operational co-author, Co-1 records (interview transcripts, drafted sections) become first-class entity types in the schema (T-03 Option B/C accommodate this; Option A barely does).
- D-03 + T-04: if Co-1 is co-author, Co-1 drafting can fill sparse-evidence cells (T-04 Option B). If Co-1 is reviewer, sparse-evidence cells stay sparse until clinical evidence materializes.
- D-03 + A5: A5 "Co-1 co-author relationship" specification depends entirely on this choice. The phase becomes drafting-spec vs. review-spec.
- D-03 + C-stage budget: Co-1 drafting requires recruitment-to-readiness time before C4 (population migration) can start. C-stage is gated on Co-1 corpus per population if Option Co-author.

### Recommendation

**Decide based on resourcing realism, then commit to the language.**

Both options are defensible. The unacceptable state is the current ambiguity — doctrine claims one thing, operations deliver another.

- If **funding for DPO partnerships and per-collaborator compensation can be secured** (university affiliation, foundation funding, or direct project funding for ≥3 collaborators per priority population), choose **Option Co-author**. Update A5 to specify drafting compensation, authorship credit, and decision-authority list. Recruitment thread runs in parallel from A5 forward.

- If **funding cannot support drafting-stage involvement** at meaningful scale, choose **Option Reviewer**. Update mission language: "The guidebook is informed by Co-1 evidence and reviewed by Co-1 representatives at key checkpoints. Drafting is performed by [the project owner / Opus / specified parties]." This is honest. It also reduces the audit's most ethically-loaded finding to a non-finding.

The audit v2 explicitly says: *"Either is defensible; ambiguity is not."*

### Cross-references

- A5 produces operational spec + recruitment plan based on this choice.
- A1-A2 mission language reflects the choice.
- C3, C4, C6 phase tables show Drafting/Decision/Review per Co-1 role.
- B4 multi-pilot Co-1 role specified per the choice.

---

## Decision tree summary

```
T-03 Co-1 tier encoding:
  [ ] A. single `tier` field with Co-1 as Tier-1 marker
  [ ] B. `tier` + `evidence_type` (RECOMMENDED)
  [ ] C. Co-1 as separate dimension

T-04 Sparse-evidence behavior:
  [ ] A. `[BEST-PRACTICE-PENDING]` marker only
  [ ] B. reduced-confidence category only
  [ ] C. doctrinal silence only
  [ ] D. hybrid: A as default + B for evidence_type-rich cases (RECOMMENDED)

D-03 Co-1 operational role:
  [ ] Co-author (RECOMMENDED if resourcing supports — high doctrinal fidelity)
  [ ] Reviewer (RECOMMENDED if resourcing cannot support — high honesty)
  Rationale: ____________________________
  Resourcing assessment: __________________________
```

Plus open question:
- Does the recommendation set above (B + D + Co-author or Reviewer) cohere acceptably to the project's resourcing reality? If not, where does the package adjust?

---

## What this report does not do

- **Does not decide.** All three decisions are project-owner decisions per workplan v3.
- **Does not commit `governance/pre-stage-a-decisions.md`.** That file commits *after* you decide.
- **Does not draft mission language.** Mission language drafting happens in 0.6 (Provisional commit) and A1-A2 (canonical).
- **Does not estimate resourcing required for Option Co-author.** That is project-owner / external-funding work outside this report's scope.

---

## Awaiting decisions

When you decide, I will:

1. Write `governance/pre-stage-a-decisions.md` capturing your selections + your rationale.
2. Commit it to the repo (creating `governance/` directory).
3. Proceed to 0.6 (Provisional mission commit) using the T-04 and D-03 outcomes.
4. Note the T-03 outcome forward for B1 schema work.
5. Update the workplan v3 §What-this-workplan-does-not-solve list — three items move from "open" to "decided."

If you want adjustments to the recommendation rationales, or want any of the three decisions left open with a documented "decide later" disposition, that is also valid. The audit's central concern is no longer ambiguity, not undecided-and-tracked.
