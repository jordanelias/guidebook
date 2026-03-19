---
name: evidence-auditor
description: >
  Audit evidence stratification in accessibility guidebook sections — check whether confidence
  levels claimed match the actual evidence quality. ALWAYS use this skill when asked to: audit
  evidence claims, check if evidence is overclaimed, review evidence stratification, assess
  confidence ratings, or check whether research quality matches stated conclusions.
  Trigger on: "evidence audit", "overclaiming check", "stratification review", "is this
  evidence strong enough", "confidence level check".
  DISTINCT from citation-verifier: this skill asks "does the confidence level match the evidence?"
  Citation-verifier asks "does the citation exist?"
---

**Intake:** ≤500 lines only. Full document → haiku-chunker first.
**Model:** Sonnet 4.6
**Output schema:** → `references/project-standards.md` (fields: claim_id, section, claim_text, source, claim_type, confidence, evidence_stratum, stratum_status)
**SelfCheck:** STRONG-stratum claims and ABSENT claims on contested topics → assess twice; divergence = UNCERTAIN_REVIEW

## Evidence Strata
Per §1.5 (Volume 1) — canonical hierarchy. Strata map to §1.5 tiers as follows:

| Stratum | Definition | §1.5 Tier(s) |
|---|---|---|
| STRONG | OT clinical research (intervention-tested) or lived experience research, replicated, aligned with §1.5 Tier 1 / Co-1 | 1, Co-1 |
| MODERATE | NGO/advocacy guidelines or systematic reviews with clear methodology | 2, 3 |
| EMERGING | Single international standard, single-jurisdiction regulatory source, or expert consensus only | 4, 5 |
| ABSENT | No empirical basis; design principle only; requires author caveat | — |

Note: a claim citing only a systematic review or RCT without OT clinical grounding is MODERATE, not STRONG. Lived experience evidence co-primary with OT research elevates confidence; its absence where feasible is a gap.

## Steps
1. Extract all empirical claims (exclude: definitions, procedural statements, pure standards citations). For each: text · location · stated stratum · cited source.
2. Propose stratum based on: source type per §1.5 hierarchy · independent replications · peer-review status · recency (flag pre-2000 sole evidence) · language coverage (single-language for cross-jurisdictional claim → flag) · presence/absence of OT clinical grounding · presence/absence of lived experience evidence.
3. Compare and flag:

| Result | Code |
|--------|------|
| Stated = proposed | ✅ CONFIRMED_STRATUM |
| Stated > evidence supports | 🔴 OVERCLAIMED |
| Stated < evidence supports | 🟡 UNDERCLAIMED |
| No stratum stated | ⚠️ UNSTATED |
| SelfCheck divergence | ⚠️ UNCERTAIN_REVIEW |

4. Output:

| ID | Section | Claim | Stated Stratum | Proposed | Status | Rationale | Action |

Claim objects (YAML) — one per flagged item.
Summary: X assessed — Y ✅ / Z 🔴 OVERCLAIMED / W ⚠️ UNSTATED / V ⚠️ UNCERTAIN_REVIEW · Overall: STRONG/ADEQUATE/WEAK/MIXED
