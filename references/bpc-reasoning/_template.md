# Reasoning: <slug>

<!--
Source template: audits/bpc-rewrite-workplan-2026-05-11.md §2
One file per slug. Located in references/bpc-reasoning/<slug>.md.
ACTIVE slugs only initially; MERGED/STUB slugs require redirect-only stubs.
Validates against scripts/validate_reasoning.py.
-->

**BPC file:** references/bpc/<topic>/<slug>.md
**BPC population:** <POP1, POP2, ...>
**Generated:** YYYY-MM-DD by session_<id>
**Status:** DRAFT | OPUS-PENDING | COMPLETE
**Opus session ref:** <session_id or N/A>

---

## A. Evidence inventory

### A.1 Sources formally linked to this slug (from source_slug_links)

| REF-ID | Local-ID | Authors | Year | Title | Tier | Evidence type | DOI/PMID | metadata_quality | verification_status | Read directly? | Date read | Method |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF-NNNNN | XYZ-NN | ... | ... | ... | N | clinical | 10.XXXX/... | COMPLETE | VERIFIED | YES | YYYY-MM-DD | web_fetch / PDF / DOI resolver |

### A.2 Sources cited in this BPC but NOT formally linked

List every author/title cited in the BPC markdown that lacks a corresponding `source_slug_links` row. Each must be either added to `source_slug_links` + `evidence_sources`, or struck from the BPC.

### A.3 Practitioner / secondary sources used during Tier 2 multilingual search

| Language | URL | Date accessed | Type (gov-summary / industry-blog / news / association / academic-press / etc.) | Used for claim | Verified against primary text? |
|---|---|---|---|---|---|

### A.4 Primary regulatory documents retrieved

| Jurisdiction | Instrument | Citation | URL/DOI | Date retrieved | Section(s) read |
|---|---|---|---|---|---|

### A.5 Gaps in the evidence inventory

For each gap: subject, why it matters, attempted resolutions, current status (OPEN / CLOSED-DELETED / CLOSED-RESOLVED), adversarial-protocol fields (confidence_interval, shift_conditions, named_dissenter, falsification_condition).

---

## B. Per-parameter reasoning (apply 9-step rule)

### B.1 Parameter: <name> (<units>)

**Step 1 — Direction**: LOWER-is-better | HIGHER-is-better | POPULATION-DEPENDENT (explain)

**Step 2 — Per-population worst-case user**:
- Population <POP1>: most-constrained user = <description>
- Population <POP2>: most-constrained user = <description>
- Cross-population conflict: <YES/NO>; if YES, log per-population entries below, do not reconcile inline

**Step 3 — Jurisdiction comparison (worst-case-point evaluation)**:

| Jurisdiction | Instrument | Scope | Structure type | Worst-case value | Direct-text verified? | Source REF-ID |
|---|---|---|---|---|---|---|

`Scope` column values: `statutory-code` | `national-framework` (Tier 5) | `international-standard` (Tier 4) | `national-recommended` | `provincial-local`. Tier 4 international standards (e.g., ISO 21542) and Tier 5 national frameworks (e.g., BS 8300-2 Annex G) are grouped with statutory codes for jurisdiction-comparison purposes only; they are NOT cited as independent evidence in Step 5.

**Step 4 — Lowest-barrier code per population**:
- For <POP1>: <jurisdiction> at <value>
- For <POP2>: <jurisdiction> at <value>

**Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence supporting or exceeding**:

| REF-ID | Tier | Evidence type | Citation | Key finding | Supports / Exceeds the lowest-barrier code? | Direct-text verified? |
|---|---|---|---|---|---|---|

**Step 6 — Guidebook chosen value per population**:
- <POP1>: <value> (rationale tag)
- <POP2>: <value> (rationale tag)

**Step 7 — Rationale**:

Historical context of permissive codes; clinical basis for chosen value. Where Sonnet inference is used, mark `[SONNET-INFERENCE]`; where Opus arbitration was applied, mark `[OPUS-DECISION session_<id>]`.

**Step 8 — Trade-offs**:

Cost; retrofit feasibility; named cross-population conflicts.

**Step 9 — Cross-population conflict flag**:

If <POP1> and <POP2> chosen values differ → QUEUE for `cross-population-conflict-resolutions` BPC. Otherwise → N/A.

### B.2 Parameter: <next parameter>...

---

## C. Synthesis claims that did NOT survive evidence review

For each retracted claim from the prior 2026-03-30 synthesis or this session's drafts:
- Original claim
- Source previously cited
- Why retracted (e.g., secondary source only, primary text retrieval failed, contradicted by Tier 1 evidence)
- Replacement claim or NO REPLACEMENT (gap)

---

## D. Cross-references

- BPC dependencies (other BPCs cited): <list with rationale>
- Items derived from this BPC: <list of item_codes>
- Connections involving this slug: <list of CON-NNNN>
- Gaps registered: <list of gap IDs>

---

## E. Adversarial protocol pass (per standing rule #7)

For every closed gap and every synthesis claim:
- Confidence interval
- Shift conditions (what evidence would shift CI up/down)
- Named dissenter (specific contrary view OR "NONE FOUND" with logged search queries)
- Falsification condition (specific finding that would invalidate)

---

## F. Provenance trail

- Every source's `derivation_chain` field populated
- Every Co-1 source's six required fields populated (A5 governance/co1-operational.md)
- Every synthesis decision tagged with Opus session ID
- `synthesis_attribution_required` populated for Co-1 sources where substantial synthesis occurred
