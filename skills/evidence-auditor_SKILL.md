---
name: evidence-auditor
description: >
  Audit evidence stratification in accessibility guidebook sections — check whether confidence
  levels claimed match the actual evidence quality. ALWAYS use this skill when asked to: audit
  evidence claims, check if evidence is overclaimed, review evidence stratification, assess
  confidence ratings, check whether research quality matches stated conclusions, or verify
  evidence marker (●/○) accuracy.
  Trigger on: "evidence audit", "overclaiming check", "stratification review", "is this
  evidence strong enough", "confidence level check", "marker verification", "●/○ audit".
  DISTINCT from citation-verifier: this skill asks "does the confidence level match the evidence?"
  Citation-verifier asks "does the citation exist?"
  DISTINCT from evidence-marker: this skill assesses whether the stratum is correct.
  Evidence-marker classifies and places ●/○ markers.
---

**Intake:** ≤500 lines only. Full document → haiku-chunker first.
**Model:** Sonnet 4.6
**Output schema:** → `references/project-standards.md` (fields: claim_id, section, claim_text, source, claim_type, confidence, evidence_stratum, stratum_status)
**SelfCheck:** STRONG-stratum claims and ABSENT claims on contested topics → assess twice; divergence = UNCERTAIN_REVIEW

## Evidence Strata

**Model:** Sonnet 4.6 (extraction, marker counting) · Opus 4.6 (overclaiming judgment, evidence sufficiency)
**Opus routing:** Sonnet extracts markers and evidence tiers → Opus determines whether evidence supports claims.

Per §1.5 (Volume 1) — canonical hierarchy. Strata map to §1.5 tiers as follows:

| Stratum | Definition | §1.5 Tier(s) |
|---|---|---|
| STRONG | OT clinical research (intervention-tested) or lived experience research, replicated, aligned with §1.5 Tier 1 / Co-1 | 1, Co-1 |
| MODERATE | NGO/advocacy guidelines or OT clinical practice guidelines or systematic reviews with clear methodology | 2, 3 |
| EMERGING | Single international standard, single-jurisdiction regulatory source, or expert consensus only | 4, 5 |
| ABSENT | No empirical basis; design principle only; requires author caveat | — |

Note: a claim citing only a systematic review or RCT without OT clinical grounding is MODERATE, not STRONG. Lived experience evidence co-primary with OT research elevates confidence; its absence where feasible is a gap.

## Evidence Marker Verification Mode (v10.1 addition)

When run in marker verification mode (triggered by "marker verification" or "●/○ audit"), this skill cross-checks evidence markers against evidence strata:

| Marker | Expected stratum | Flag if mismatch |
|---|---|---|
| ● (evidence-based) | STRONG or MODERATE | 🔴 if stratum is ABSENT; 🟡 if stratum is EMERGING with single source |
| ○ (inferred) | EMERGING or ABSENT | 🟡 UPGRADEABLE if stratum is actually MODERATE or STRONG |

Additional marker checks:
- ● with no citation in evidence table → 🔴 UNSUPPORTED-MARKER
- ○ with evidence in BPC but not cited in item → 🟡 EVIDENCE-AVAILABLE (may warrant upgrade)
- ● citing only expert consensus or clinical reasoning → 🔴 MARKER-STRATUM-MISMATCH (should be ○)
- ○ citing a Tier 1–3 source that directly supports the value → 🔴 MARKER-STRATUM-MISMATCH (should be ●)

Output for marker verification mode:

| ID | Item | Sentence | Marker | Stratum | Flag | Action |
|---|---|---|---|---|---|---|

Summary: X markers verified — Y consistent / Z mismatches (W 🔴 / V 🟡)

## OFS/PAIN Expert Consensus Disclosure (v10.1 addition)

For OFS and PAIN populations: where evidence stratum is EMERGING or ABSENT and the specification derives from expert consensus only, the item must carry explicit disclosure:

`[EXPERT CONSENSUS — No OT clinical evidence for this specification value for {population}. Based on clinical reasoning from adjacent populations. Evidence gap logged: GAP-XXX]`

Flag any OFS or PAIN specification at EMERGING/ABSENT stratum without this disclosure as 🔴 UNDISCLOSED-CONSENSUS.

## Steps
1. Extract all empirical claims (exclude: definitions, procedural statements, pure standards citations). For each: text · location · stated stratum · cited source · evidence marker (● or ○ if present).
2. Propose stratum based on: source type per §1.5 hierarchy · independent replications · peer-review status · recency (flag pre-2000 sole evidence) · language coverage (single-language for cross-jurisdictional claim → flag) · presence/absence of OT clinical grounding · presence/absence of lived experience evidence.
3. Compare and flag:

| Result | Code |
|--------|------|
| Stated = proposed | ✅ CONFIRMED_STRATUM |
| Stated > evidence supports | 🔴 OVERCLAIMED |
| Stated < evidence supports | 🟡 UNDERCLAIMED |
| No stratum stated | ⚠️ UNSTATED |
| SelfCheck divergence | ⚠️ UNCERTAIN_REVIEW |
| Marker ≠ stratum (marker mode) | 🔴 MARKER-STRATUM-MISMATCH |

4. Output:

| ID | Section | Claim | Stated Stratum | Proposed | Status | Rationale | Action |

Claim objects (YAML) — one per flagged item.
Summary: X assessed — Y ✅ / Z 🔴 OVERCLAIMED / W ⚠️ UNSTATED / V ⚠️ UNCERTAIN_REVIEW · Overall: STRONG/ADEQUATE/WEAK/MIXED
