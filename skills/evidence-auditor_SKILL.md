---
name: evidence-auditor
description: >
  Audit evidence stratification in accessibility guidebook sections — check whether confidence
  levels claimed match the actual evidence quality. ALWAYS use this skill when asked to: audit
  evidence claims, check if evidence is overclaimed, review evidence stratification, assess
  confidence ratings, check whether research quality matches stated conclusions, or verify
  evidence marker (●/◐/○) accuracy.
  Trigger on: "evidence audit", "overclaiming check", "stratification review", "is this
  evidence strong enough", "confidence level check", "marker verification", "marker audit",
  "●/◐/○ audit", "●/○ audit".
  DISTINCT from citation-verifier: this skill asks "does the confidence level match the evidence?"
  Citation-verifier asks "does the citation exist?"
  DISTINCT from evidence-marker: this skill assesses whether the stratum is correct.
  Evidence-marker classifies and places ●/◐/○ markers.
---

**Intake:** ≤500 lines only. Full document → haiku-chunker first.
**Model:** Sonnet-class
**Output schema:** → `references/project-standards.md` (fields: claim_id, section, claim_text, source, claim_type, confidence, evidence_stratum, stratum_status)
**SelfCheck:** STRONG-stratum claims and ABSENT claims on contested topics → assess twice; divergence = UNCERTAIN_REVIEW

## Evidence Strata

**Model:** Sonnet-class (extraction, marker counting) · Opus-class (overclaiming judgment, evidence sufficiency)
**Opus routing:** Sonnet extracts markers and evidence tiers → Opus determines whether evidence supports claims.

Per `governance/tier-system.md` §1 (OPERATIVE — the canonical ladder). Strata map to the ladder as follows:

| Stratum | Definition | Tier(s) |
|---|---|---|
| STRONG | Primary research with intervention-level or biomechanical control on the parameter, or disability-led lived-experience research; replicated | T1, Co-1 |
| MODERATE | Systematic reviews / meta-analyses, named-organisation evidence-based standards, OT professional-body CPGs, or lower-control primary clinical research (cross-sectional, observational, qualitative, single-centre) | T2, Co-2, T3-clinical |
| EMERGING | International standards, national beyond-code frameworks, statutory code, grey-literature primary, or expert consensus only | T4, T5, T6, T3-grey |
| ABSENT | No empirical basis; design principle only; requires author caveat | — |

Note: systematic reviews and meta-analyses are **Tier 2, not Tier 3** (`tier-system.md` §2, owner directive 2026-05-25); scoping reviews and conceptual/framework papers are Tier 3 (§2, DR-2026-07-21). Lived-experience evidence is co-primary with primary research on the claim types it governs — non-substitutable, not merely confidence-elevating — and its absence where feasible is a gap.

## Evidence Marker Verification Mode (v10.1 addition)

When run in marker verification mode (triggered by "marker verification" or "marker audit" / "●/○ audit"), this skill cross-checks evidence markers against evidence strata. **The scheme is three markers, not two** (`governance/tier-system.md` §5, and §8 for the anchoring bands) — a ●/○-only audit is auditing a retired scheme:

| Marker | Meaning | Expected stratum / basis | Flag if mismatch |
|---|---|---|---|
| **●** | confirmed evidence base | STRONG or MODERATE — basis includes T1, Co-1, T2, Co-2 or T3-clinical | 🔴 if stratum is ABSENT; 🔴 if the basis is T4/T5 only (should be ◐); 🔴 if the basis is T6 / T3-grey / expert consensus only (should be ○) |
| **◐** | policy or standards basis only, not primary evidence | EMERGING, where the basis is T4 or T5 | 🔴 if the basis reaches T1/Co-1/T2/Co-2/T3-clinical (should be ●); 🔴 if the basis is T6 / T3-grey / consensus only (should be ○) |
| **○** | weak band — grey, expert consensus, thin base, code-floor | EMERGING on T6 / T3-grey / consensus, or ABSENT with caveat | 🟡 UPGRADEABLE if the stratum is actually MODERATE or STRONG |

Additional marker checks:
- Any spec sentence carrying **no** marker → 🔴 UNMARKED (unmarked is an error, per `tier-system.md` §5)
- ● with no citation in evidence table → 🔴 UNSUPPORTED-MARKER
- ○ with evidence in BPC but not cited in item → 🟡 EVIDENCE-AVAILABLE (may warrant upgrade)
- ● citing only expert consensus or clinical reasoning → 🔴 MARKER-STRATUM-MISMATCH (should be ○)
- ○ citing a T1 / Co-1 / T2 / Co-2 / T3-clinical source that directly supports the value → 🔴 MARKER-STRATUM-MISMATCH (should be ●)
- A determination whose **entire** basis is T4–T6 rendered above the weak band → 🔴 MARKER-STRATUM-MISMATCH (should be ○, flagged code-derived: `tier-system.md` §8 Option A, DR-2026-07-21 §2.3)

Output for marker verification mode:

| ID | Item | Sentence | Marker | Stratum | Flag | Action |
|---|---|---|---|---|---|---|

Summary: X markers verified — Y consistent / Z mismatches (W 🔴 / V 🟡)

## OFS/PAIN Expert Consensus Disclosure (v10.1 addition)

For OFS and PAIN populations: where evidence stratum is EMERGING or ABSENT and the specification derives from expert consensus only, the item must carry explicit disclosure:

`[EXPERT CONSENSUS — No OT clinical evidence for this specification value for {population}. Based on clinical reasoning from adjacent populations. Evidence gap logged: GAP-XXX]`

Flag any OFS or PAIN specification at EMERGING/ABSENT stratum without this disclosure as 🔴 UNDISCLOSED-CONSENSUS.

## Steps
1. Extract all empirical claims (exclude: definitions, procedural statements, pure standards citations). For each: text · location · stated stratum · cited source · evidence marker (●, ◐ or ○ if present).
2. Propose stratum based on: source type per the `governance/tier-system.md` §1 ladder · independent replications · peer-review status · recency (flag pre-2000 sole evidence) · language coverage (single-language for cross-jurisdictional claim → flag) · presence/absence of OT clinical grounding · presence/absence of lived experience evidence.
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

5. **SQLite write (actionable flags only):**

Log flagged findings that require action to the tracking DB. Do NOT log CONFIRMED_STRATUM
or UNDERCLAIMED (informational only — brief record only, no DB entry).

| Flag | Gap category | Rationale |
|---|---|---|
| OVERCLAIMED | EG | Evidence insufficient for stated confidence — research or reclassification needed |
| UNCERTAIN_REVIEW | EG | SelfCheck divergence — review or research needed to resolve |
| UNDISCLOSED-CONSENSUS | AUDT | Authoring error: disclosure missing — ISW correction needed |
| MARKER-STRATUM-MISMATCH | AUDT | Authoring error: wrong marker placed — ISW correction needed |
| UNSUPPORTED-MARKER | AUDT | Authoring error: ● with no citation — ISW correction needed |
| UNSTATED | AUDT | Authoring error: stratum not stated — ISW correction needed |

```bash
# EG gap (research/review needed)
python3 scripts/db.py add-gap \
  --category EG \
  --priority P2 \
  --description "[flag-code] [section]: [claim text truncated to 120 chars] — [action required]" \
  --skill evidence-auditor \
  --section [item_code or section_id] \
  --session [session-name]

# AUDT gap (authoring correction needed)
python3 scripts/db.py add-gap \
  --category AUDT \
  --priority P2 \
  --description "[flag-code] [section]: [claim text truncated to 120 chars] — [correction required]" \
  --skill evidence-auditor \
  --section [item_code or section_id] \
  --session [session-name]
```

After logging: run `python3 scripts/db.py gaps --status OPEN` to confirm insertion.
Commit DB to GitHub with message:
`evidence-auditor: [N] flags logged [item_code] [YYYY-MM-DD HH:MM]`
