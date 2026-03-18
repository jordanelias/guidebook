---
name: economics-researcher
description: >
  Research, verify, and draft economics content for the guidebook's economics volume —
  covering construction cost data, government funding programmes, property value evidence,
  cost-benefit analysis, retrofit cost tables, professional audit fees, and economic
  arguments for accessible design. ALWAYS use this skill when asked to: find cost data,
  research grant programmes, draft economic arguments, verify cost claims, assemble cost
  intelligence tables, check funding programme details, or produce any numeric cost content.
  Trigger on: "cost data", "grant programme", "economic case", "retrofit cost", "cost-benefit",
  "funding", "property value", "cost table", "economic argument", "cost multiplier",
  "QS data", "construction economics", or any task involving numeric economic claims
  about accessible design. Always consult before producing any cost figure or funding detail.
---

**Model:** Sonnet 4.6 + web search (required for all funding programme verification)
**Input:** task specification + gap register item (if research-driven) + jurisdiction scope
**Output:** evidence brief (YAML) → draft section text → citation-verifier pass
**Source ceiling:** 20 sources per research run. Scope gate: max 3 jurisdictions per run.
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API
**Research log:** Call `research-log-manager CHECK` (slug format: `{topic}|ECON`) before any search. Call `research-log-manager LOG` after completing Step 6. Skipping either is an error.

---

## Scope Boundary

This skill covers economic evidence that architects, developers, and housing authorities need to make decisions. It does not cover:
- Product pricing or equipment market data
- Insurance or indemnity economics  
- Academic health economics outside built environment outcomes

For clinical economics of disability (healthcare cost modelling), hand off to multilingual-research.

---

## Source Hierarchy

Consult in order. Stop at the highest tier that resolves the question.

| Tier | Source type | Use for |
|---|---|---|
| E-1 | Peer-reviewed studies, systematic reviews | Cost-benefit ratios; property value uplift; ROI evidence |
| E-2 | Government programme data (official ministry/agency reports) | Grant maxima, eligibility, funding volumes |
| E-3 | National quantity surveyor bodies; construction cost indices | Unit cost ranges; cost multipliers |
| E-4 | Housing association and developer published data | Real project cost data |
| E-5 | Professional body guidance (RICS, AIQS, CIQS equivalents) | Cost benchmarks |
| E-6 | Independent think-tank and NGO reports | Systemic economic arguments |
| E-7 | Contractor or trade association data | Use only when E-1 through E-6 unavailable; flag tier explicitly |

Flag any claim resting solely on E-7 as `[PROVISIONAL — independent verification required]`.

---

## Framing Rules (non-negotiable)

These apply to all drafted text, regardless of what source material says:

1. **Positive case first.** Lead with the economic benefit of accessible design. Never open with cost-of-compliance framing.
2. **No compliance-burden language.** Never frame accessibility as a cost imposed by regulation. Frame as investment with documented return.
3. **Distinguish capital from lifecycle cost.** A higher capital cost with lower lifecycle cost must be presented as the full picture.
4. **No single-source cost claims.** Any specific cost figure must be corroborated by ≥2 independent sources, or flagged `[SINGLE SOURCE — verify before publication]`.
5. **Jurisdiction-explicit.** All cost data must name the jurisdiction and date. Do not aggregate across jurisdictions without noting the range and variance.
6. **No market-segment framing.** Do not frame disabled people as a "market" or "demographic opportunity." Frame as design quality serving everyone.

---

## Research Workflow

### Step 1 — Scope the task
Confirm: jurisdiction(s) · topic (cost / grant / ROI / retrofit / property value) · evidence tier floor required · publication risk level (high = requires E-1 or E-2 sources)

### Step 2 — Retrieve reference data
GET `references/economics-sources.md` from GitHub before searching. Do not re-verify what is already confirmed.

### Step 3 — Web search
Search for current data. Funding programmes and cost indices change annually. Treat any data >2 years old as requiring recency verification.

### Step 4 — Evidence brief
Produce in YAML before drafting any prose:

```yaml
economics_brief:
  topic: "[topic]"
  jurisdiction: "[jurisdiction]"
  date_retrieved: "[YYYY-MM-DD]"
  sources:
    - citation: "[author/org, year, title]"
      tier: E-[N]
      claim: "[specific claim supported]"
      verified: true/false
  draft_claim: "[proposed text for document]"
  flags: []
```

### Step 5 — Draft text
Write in the project prose register (soft imperative; ≤25 words per sentence; no preamble).  
All numeric claims carry inline citation. Unverified claims carry `[UNVERIFIED — source required]`.

### Step 6 — Citation-verifier handoff
Pass all new citations to citation-verifier before the evidence brief is closed.

---

## Standard Content Areas

Design-stage cost comparison · retrofit cost multipliers · government funding programmes · property value evidence · return on investment · systemic economic arguments (mandatory vs voluntary standards outcomes). Current verified data for each area in `references/economics-sources.md` — consult before searching.

---

## Citation Format

Author-year throughout. Government programme data: `[Agency/Ministry]. ([Year]). [Programme name]. [Government]. Retrieved [Month Year].` Flag all funding figures `[VERIFY ANNUALLY]` — maxima change by fiscal year.

---

## Escalation Triggers

Stop and confirm with user:

- Cost data varies by >50% across sources in the same jurisdiction — do not average; report the range and explain the variance
- A funding programme has been announced but not yet implemented — flag as `[PENDING IMPLEMENTATION — do not cite as current]`
- Source is a contractor, manufacturer, or industry body with a commercial interest in the claim — flag conflict of interest explicitly; seek independent corroboration

---

## Reference Files

`references/economics-sources.md` on GitHub — verified funding programme data, cost benchmarks, and ROI evidence. GET before any search. After verification: GET + SHA, append new entries, PUT back (Project Instructions §GitHub API).

> This reference file holds the jurisdiction-specific content (grant names, maxima, legislation references, cost tables) that changes over time. The skill body contains process rules only. Do not embed specific figures in this skill file.
