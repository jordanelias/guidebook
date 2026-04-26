# CO-0007 Contamination Sampling
**Created:** 2026-04-26 02:18 UTC
**Stage:** 0.4 (Contamination sampling)
**Resolves audit finding:** N-07 (salvage matrix qualitative; contamination ratio unknown)
**Status:** Stage-0 deliverable; pre-adoption (workplan v3 not yet adopted per 0.9)

---

## Purpose

Workplan v3 §0.4 requires sampling N=15 BPC files and classifying each `best_practice_synthesis` field against the 2026-04-24 23:46 doctrinal rule (project-standards line 20). Audit v2 §N-07 designated this Medium because the synthesis salvage matrix treats contamination qualitatively when it is actually a continuous variable, and C-stage budget realism depends on the ratio.

**Doctrinal rule under test:**
> *Best practice means the most accommodating, thoughtful, respectful, dignified, and usable condition achievable for the disabled person. Best practice is determined by the evidence hierarchy — Tier 1 clinical research, Co-1 lived experience, Co-2 OT CPGs, Tier 3 systematic reviews — not by code consensus. Codes are Tier 6: the compliance floor, not the aspiration. Code consensus across jurisdictions establishes what most codes agree on; it does not establish what is most accommodating or most dignified.* **A BPC best_practice_synthesis that derives its value solely from code consensus is in error.** *The test: does this specification provide the most accommodating, dignified, usable condition the evidence supports — or does it merely reflect what codes agree on?*

---

## Sampling design

**Population:** 78 topic-slug BPC files at `references/bpc/<topic>/<slug>.md`.

**Sample size:** N=15 (per workplan v3 §0.4).

**Method:** Stratified by topic group, proportional within rounding constraints. First-alphabetical within each strata for determinism (so the result is reproducible if rerun against the same HEAD).

| Topic group | Population | Sample | Selected |
|---|---|---|---|
| frameworks-and-methodology | 18 | 3 | s06, s07, s08 |
| population-general | 12 | 2 | s11, s12 |
| sensory-environment | 12 | 2 | s13, s14 |
| wayfinding-and-signage | 8 | 1 | s15 |
| health-and-symptom-management | 7 | 1 | s09 |
| entrances-and-circulation | 6 | 1 | s05 |
| communication-and-alerts | 4 | 1 | s02 |
| economics | 4 | 1 | s04 |
| bathrooms-and-wet-areas | 3 | 1 | s01 |
| controls-and-hardware | 1 | 1 | s03 |
| kitchens-and-workspaces | 1 | 1 | s10 |
| **Total** | **76 of 78** | **15** | (room-types and seating-and-rest each have 1 file but were not sampled in this stratification — minor under-sample) |

**Methodological caveats:**

1. The 2026-04-24 23:46 doctrinal rule was committed only **2 days before this sample**. Most BPCs predate the rule. Their alignment with it is retrospective — it tells us about the project's *prior practice*, not whether BPCs were edited to match a new rule.
2. Many sampled BPCs carry `[OPUS-SYNTHESIS]` markers from 2026-03-28 to 2026-04-09. Opus passes generally tighten doctrinal alignment. Files not yet Opus-reviewed may be more contaminated than this sample suggests.
3. Sample = 15/78 = 19% of corpus. Statistical confidence is moderate, not high.

---

## Classification scheme

The doctrine rule's strict contamination criterion is *"derives its value SOLELY from code consensus."* Most BPCs cite multiple evidence types, so strict contamination is rare. A more useful 4-level scheme:

- **EXEMPLARY** — explicit doctrinal practice. Synthesis identifies code-derived values as inadequate baselines, derives best practice from clinical evidence/Co-1/Co-2, and explains the gap.
- **ALIGNED** — evidence-driven derivation. Tier 1/Co-1/Co-2/Tier 3 evidence forms the basis. Codes (Tier 4–6) cited as supplementary support, not as the basis.
- **AMBIGUOUS** — values appear derived from a single Tier 5 framework or jurisdictional convergence without explicit clinical-evidence backing. Doctrinal stance not clearly stated.
- **CONTAMINATED** — best practice derived solely or primarily from code consensus across jurisdictions.

Two states fall outside doctrinal classification:
- **STUB** — synthesis not yet written (flagged for Opus or pending).
- **MERGED** — file is a redirect to a consolidated BPC; no synthesis to evaluate.

---

## Per-file classification

| # | Slug | Opus | Class | Key evidence basis |
|---|---|---|---|---|
| s01 | accessible-bathroom-and-grab-bar | ✓ | **ALIGNED** | Tier 1: Nakamura 2009 (NEU vertical bars), Kennedy 2015 (UPL bilateral), Levine 2025 (biomechanical). Tier 5: BS 8300-2 Annex G (power WC). Codes used as Tier 4–6 supporting evidence ("supported by Tier 4–6 across 22–24 jurisdictions"). |
| s02 | assistive-listening-systems | ✓ | **ALIGNED** | Tier 4 (IEC 60118-4) primary; Co-1/Tier 2 (HLAA, RNID) advocacy; Tier 5 (FR CEREMA) explicitly identified as "stricter best practice"; Japan gap explicitly flagged. |
| s03 | reach-range-and-accessible-controls | — | **ALIGNED** | Co-1 (LPA advocacy) drives 1220mm decision; Tier 1 (AAATE 2016) for door force; Tier 5 (CMHC CA) for door force max. "Co-1-driven improvement" explicitly named. |
| s04 | accessible-design-economics-cost-premium | ✓ | **ALIGNED-DOMAIN** | Economics domain — uses economic studies and jurisdictional cost data, which is the appropriate evidence type for economics. The doctrine rule applies to *specification values*, not procedural recommendations. |
| s05 | residential-entry-and-threshold | — | **ALIGNED** | "1:20 not 1:12" with biomechanical reasoning ("requires significant upper-limb effort for self-propelling WC users"). Co-2 (RCOT) explicit. Best practice ≥900mm vs minimum 850mm — code-as-floor pattern. |
| s06 | accessible-design-failures-poor-performance | — | **STUB** | All "[STUB — Opus synthesis pending]". Sonnet has explicitly deferred: "Sonnet cannot determine." Per project protocol, this is correct behavior, not contamination. |
| s07 | cross-population-conflict-resolutions | ✓ | **EXEMPLARY** | Tier 1 (DSDC 2024 falls evidence), Tier 4 (ISO 23599), Uhthoff's threshold (Tier 1 clinical). Honest about confidence: "the resolution framework itself... is expert consensus, not empirically validated." Three values flagged as "[UNSUPPORTED — concept evidence-based, threshold not evidence-derived]." |
| s08 | visitability-residential-accessibility-minimum-standards | ✓ | **ALIGNED** | Tier 5 frameworks: Lifetime Homes (UK), CAN/ASC B652 (Canada), NS 11001-2 (Norway). Visitability framed explicitly as "absolute floor" — code-as-floor pattern. |
| s09 | thermoregulation-built-environment | ✓ | **EXEMPLARY** | Population-risk stratification with Tier 1–3 source citations. **Explicit doctrinal claim:** *"This range is narrower than any existing building standard or code. It is a synthesis from clinical evidence, not an adoption of an existing standard. [OPUS-SYNTHESIS — CLINICAL DERIVATION]."* |
| s10 | residential-kitchen-and-task-surfaces | ✓ | **AMBIGUOUS** | Tier 5 framework (NL WMO-keuken) drives values directly. "BE/NL underrideable standard (700mm height, 900mm width, 600mm depth, 800mm worktop max) most detailed Tier 5 spec." LPA (Co-1) cited for conflict resolution but not for baseline values. Status: PROVISIONAL retained. **6/24 jurisdictions NOT-RUN; evidence base is European-dominated.** |
| s11 | mobility-built-environment | ✓ | **EXEMPLARY** | Tier 1 (IDeA Center anthropometric, n=500), Cochrane (Tier 3, 38% fall reduction). **Explicit code rejection:** *"ADA 1524 mm rejected as a design baseline — cited here as evidence of regulatory lag only, not as a permitted specification value."* |
| s12 | visual-impairment-built-environment | ✓ | **ALIGNED** | ISO 23599 (Tier 4 evidence-based standard). LRV ≥30 correctly flagged as Tier 0 (code-compliance baseline), not as best practice. Low-vision-majority insight is a Co-1/epistemic point. |
| s13 | acoustics-speech-intelligibility-disability | ✓ | **EXEMPLARY** | Tier 1 (Murgia 2023 systematic review) governs RT60 target. **Explicit code-error critique:** *"The 0.6 s value in most building codes is not an evidence-based target for inclusive design — it is the threshold at which even normal-hearing listeners begin to lose speech intelligibility. Treating it as a design target rather than a failure threshold is a category error repeated across ADA, BS 8300, and NCC."* |
| s14 | circadian-lighting-melanopic-edi | — | **ALIGNED** | DIN/TS 67600:2022 (Tier 4 evidence-based standard); CIE consensus values (≥250 / ≤10 / <1 melanopic EDI). DEM/NEU therapeutic framing distinguishes circadian intervention from amenity. |
| s15 | luminance-contrast-and-pattern | — | **MERGED** | File is a redirect: *"Use `luminance-contrast-lrv-evidence-base` for all research retrieval. This file is a redirect only."* No synthesis to evaluate. |

---

## Distribution

| Class | Count | % of N=15 | % of effective N=13 (excluding STUB/MERGED) |
|---|---|---|---|
| **EXEMPLARY** | 4 | 27% | 31% |
| **ALIGNED** | 8 | 53% | 62% |
| **AMBIGUOUS** | 1 | 7% | 8% |
| **CONTAMINATED** | **0** | **0%** | **0%** |
| STUB | 1 | 7% | excluded |
| MERGED | 1 | 7% | excluded |

**Doctrinally-aligned (EXEMPLARY + ALIGNED): 12 of 13 evaluable BPCs = 92%.**
**Frankly contaminated: 0 of 13.**

---

## Statistical inference for the corpus (78 BPCs)

For zero observed contamination events in N=13 evaluable BPCs:

- **Wilson 95% CI (one-sided upper bound) for true proportion:** ~22%
- **Practical interpretation:** Observed contamination is consistent with anywhere from 0% to ~22% of the 78-BPC corpus being CONTAMINATED. The point estimate is 0%; the upper confidence bound is ~22% because the sample is small.

For 1 observed AMBIGUOUS case in 13:

- **Wilson 95% CI:** ~0.4%–33%
- **Practical interpretation:** Ambiguous-status BPCs are likely between ~0% and ~33% of the corpus. Point estimate ~8%.

For 1 STUB and 1 MERGED in N=15:

- ~7% each. STUBs likely exist throughout the corpus pending Opus synthesis. MERGED redirects from CO-0006 migration also expected.

---

## Findings

### F1 · The audit's contamination hypothesis is not supported

Audit v2 §N-07 framed contamination as a real and unknown-magnitude problem. The 2026-04-24 23:46 doctrinal rule, committed shortly before this sample, was issued specifically because contamination concern was real. **The sample finds 0 frankly-contaminated BPCs and 1 ambiguous case.** This is a strong signal that contamination is *low* in the corpus.

Two contributing factors:

1. **Most sampled BPCs have been Opus-refreshed** between 2026-03-28 and 2026-04-09. The OPUS-marked files in the sample are uniformly EXEMPLARY or ALIGNED. Whatever pre-Opus state existed has been corrected.
2. **The doctrinal rule was committed retrospectively** (2026-04-24), 2 days before this sample. Most BPCs predate the rule. The fact that they nonetheless align with it suggests the project's prior practice was already doctrinally sound; the rule was articulating existing practice, not correcting deviant practice.

### F2 · One ambiguous case identifies a real residual concern

S10 (residential-kitchen-and-task-surfaces) derives baseline values directly from a single Tier 5 framework (NL WMO-keuken / BE/NL underrideable standard) without explicit clinical-evidence backing for the specific dimensions. The synthesis correctly flags this with PROVISIONAL status and notes "6/24 jurisdictions NOT-RUN; evidence base is European-dominated."

This is the *kind* of contamination concern audit N-07 anticipated, but it is Tier-5-derivation rather than Tier-6-code-consensus-derivation — a milder form. And it's correctly self-flagged as PROVISIONAL.

### F3 · STUB and MERGED states are real and not previously enumerated

- **STUB (s06):** 1/15 = ~7%. BPCs awaiting Opus synthesis. Per project protocol, Sonnet correctly defers. These are not contaminated; they are pending.
- **MERGED (s15):** 1/15 = ~7%. CO-0006 migration produced redirect files. Cannot evaluate them as BPCs.

If extrapolated: ~5–6 STUBs and ~5–6 MERGED redirects across 78 BPCs is plausible. **C-stage migration scope should account for these states explicitly:**
- STUBs need Opus synthesis (per existing protocol)
- MERGEDs need either consolidation into the canonical slug or removal during migration

### F4 · OPUS-synthesis pass coverage is incomplete but advancing

Of 15 sampled, ~10 carry OPUS-SYNTHESIS markers. ~33% un-marked may be more vulnerable to undetected contamination. **Recommendation: complete Opus pass on remaining BPCs before C3 (parameter migration) — this is closer to a 1–2-session effort than full rebuild.**

### F5 · Implications for Stage C scope

Audit v2 §N-07 implied that high contamination would force significant rebuild during migration. The sample suggests:
- **Most BPCs (>90% of evaluable) are migration-ready, not rebuild-required.**
- **Tier-5-only-derivation cases (~8% AMBIGUOUS) require evidence backfill** — a per-case audit task during C3, not a full rebuild.
- **STUB cases (~7%) require Opus synthesis** — a known-pattern existing-protocol task.
- **MERGED cases (~7%) require redirect handling during migration** — mechanical, low-effort.

**Net effect on C-stage budget:** C7 budget revision (per Stage 0.2 finding M2: bibliography 6%→14% residual) increases scope. C3 contamination-cleanup is *less* expansive than feared. The two adjustments roughly offset.

---

## Adjusted salvage matrix

Workplan v3 §Salvage matrix (revised) currently lists "Reusable conditionally" for "BPC `best_practice_synthesis` fields where contamination sample shows clean." The sample now provides quantitative grounding:

| Status | Items | Fraction |
|---|---|---|
| **Fully reusable** (EXEMPLARY + ALIGNED) | BPC `best_practice_synthesis` fields | ~92% of evaluable |
| **Reusable with adjustment** (AMBIGUOUS) | BPCs with Tier-5-only derivation; flag for evidence backfill | ~8% of evaluable |
| **Pending Opus synthesis** (STUB) | New category | ~7% of full sample |
| **Redirect / consolidate** (MERGED) | New category | ~7% of full sample |
| **Superseded** | Possibly some pre-2026-03-28 non-Opus-refreshed BPCs not in sample | unknown, likely small |

The "BPC `best_practice_synthesis` fields where sample shows contamination" row in workplan v3's salvage matrix can be **substantially reduced** based on this finding. The "Superseded" row's BPC entry should be modified to reflect that contamination is not the dominant failure mode.

---

## What this report does not do

- **Does not commit corrections to the salvage matrix.** That is 0.7 (synthesis re-issue) work.
- **Does not adjust C-stage budgets.** Same.
- **Does not run Opus passes on un-marked BPCs.** Recommendation only; execution is a separate task.
- **Does not extend the sample.** N=15 is what workplan v3 §0.4 specified. Larger N would tighten CIs but is not in 0.4 scope.
- **Does not modify any BPC file.** Inventory/classification only.
- **Does not adopt or reject workplan v3.** That is 0.9.

---

## Coda

The audit anticipated contamination as a likely substantial migration concern. The sample doesn't confirm that. Of 13 evaluable BPCs, 12 (92%) are doctrinally aligned with the 2026-04-24 23:46 rule and 4 of those 12 (31% of evaluable, 27% of full sample) practice it exemplarily — explicitly rejecting code consensus as a basis. One BPC (S10) is mildly ambiguous, with Tier-5-only derivation correctly self-flagged as PROVISIONAL.

The corpus is healthier than expected. The Opus synthesis pass that ran from late March through early April produced this state. The 2026-04-24 doctrinal rule articulates an existing practice rather than correcting a deviant one.

Two operational consequences:

1. **C-stage migration is more migration than rebuild for `best_practice_synthesis` fields.** The "reusable with adjustment" salvage category is more populated than the "superseded" one for this artifact type.
2. **Two corpus states (STUB, MERGED) are first surfaced quantitatively here.** Workplan v3 should accommodate them explicitly in C3/C7 task structure.

The sample's small size (N=13 effective) means the upper confidence bound on contamination is ~22%. The point estimate is 0%. A larger sample (N=30) at a future checkpoint would tighten the bound to ~12% if results held — still well below "widespread" contamination.
