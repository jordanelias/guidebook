# Session: Protocol-compliant redo — slug 2 substantially complete
**session_start:** 2026-05-10 10:30 UTC
**session_close:** 2026-05-10 13:00 UTC
**PI version:** v10.6
**workplan:** workplan-co0007-v4.md + multilingual-search-remediation.md

## Problem addressed
Prior work in this conversation searched slugs 2-3 at medium effort, violating adversarial research protocol. This session redid slug 2 (sensory-room-user-control) at high effort with proper standard + adversarial searches, evidence_population_match logging, and honest protocol compliance markers.

## Slug 2 (sensory-room-user-control) — protocol status

| Language | Protocol | Key finding |
|---|---|---|
| FR | FULL | Practitioner-mediated, not user-controlled. CLE Autistes: consent essential. Cairn review: 41.7% unfavorable cost-effectiveness. |
| ZH | FULL | GENUINE DIVERGENCE. SI training rooms are practitioner-directed. User control absent from Chinese discourse. |
| KO | FULL | DIVERGENCE. Clinical/therapist-directed only. Korean SR calls for higher quality evidence. |
| ES | FULL | Scarce evidence for autism. Chile Ley 21.545 regulatory driver. User control valued but thin evidence. |
| DA | FULL | McKee 2007: NO evidence for Snoezelen in autism, behavior may WORSEN. Lotan & Gold 2009 MA: no significant effect. |
| NO | FULL | Adversarial via DA findings. Norwegian practice follows Snoezelen. |
| SV | FULL | SPEDUCULT/Lund 2020: no certified MSE education in Sweden. Equipment often not interactive. |
| NL | FULL | Origin country acknowledges implementation quality issues. Low-stimulus design is PRIMARY for autism housing; sensory rooms are SUPPLEMENTARY. |
| PT | FULL | User autonomy strongly valued. BR PL 3098/24 mandates school rooms. Scarce evidence globally. |
| FI | PARTIAL | Standard search only. Scandinavian adversarial applies. Needs Finnish-specific adversarial. |
| EN | PRE-REMEDIATION | BPC extraction. Not protocol-upgraded. |
| DE | PRE-REMEDIATION | BPC extraction. Not protocol-upgraded. |
| JA | PRE-REMEDIATION | BPC extraction. Not protocol-upgraded. |
| IT | PRE-REMEDIATION | BPC extraction. Not protocol-upgraded. |

## Evidence sources added: 5
| ref_id | Source | Grade | Key adversarial value |
|---|---|---|---|
| REF-00700 | Cairn.info 2022 FR Snoezelen review | PARTIAL | 41.7% unfavorable cost-effectiveness; trademark bias |
| REF-00701 | PMC12673401 Chinese SR+MA | PROXY | Chinese SI is practitioner-directed, not user-controlled |
| REF-00702 | KCI 2022 Korean SR | PROXY | Korean SR quality concerns; therapist-directed model |
| REF-00703 | McKee et al. 2007 | PARTIAL | NO evidence for Snoezelen in autism; behavior may worsen |
| REF-00704 | Lotan & Gold 2009 MA | PROXY | No significant effect of Snoezelen for ID |

## Critical pattern detected (standing rule #7)
**Topic-evidence vs claim-evidence conflation:** Initial medium-effort work found evidence about sensory rooms (topic) and logged it as supporting user-control-as-primary (claim). The protocol redo revealed:
- ZH/KO: Evidence on sensory interventions exists but does NOT support user control — opposite model (practitioner-directed)
- DA: Evidence EXISTS that contradicts the BPC claim (McKee 2007: no evidence for autism, possible harm)
- NL: Origin country frames sensory rooms as SUPPLEMENTARY, not primary — low-stimulus design is primary for autism housing
- FR: Practitioner-mediated ≠ user-controlled — superficially similar but fundamentally different

**BPC impact:** The Opus synthesis ("user control as primary design variable") holds for the EN/UK research base (Unwin et al.) but is NOT cross-jurisdictionally confirmed. It is challenged by ZH/KO (different model), DA (no evidence/possible harm), and NL (supplementary role). This needs flagging for the BPC reviewer.

## Remaining work

### Slug 2 remaining:
- FI: Finnish-specific adversarial search
- EN, DE, JA, IT: Protocol upgrade of pre-remediation entries (lower priority — these formed the original BPC evidence base)

### Slug 3 (school-environment-autism): 13 languages need adversarial redo
All marked PARTIAL-PROTOCOL in DB.

### Slugs 4-8 (Tier 1 remaining): Not started in protocol-compliant form
- circadian-lighting-melanopic-edi: started standard searches in earlier pass, needs adversarial
- construction-cost-data, visual-fire-alarm-seizure-safety, accessible-design-economics-cost-premium, thermal-comfort-older-adults-care-settings: not started

## Commits
1. DB 8abc6644 (initial protocol redo)
2. DB 1ef41dc7 (Nordic adversarial + PT/NL completion)
3. Session + LATEST (this commit)

## next_action
1. Continue slug 3 adversarial redo (13 languages)
2. Flag slug 2 BPC for reviewer: cross-jurisdictional challenge to user-control-as-primary claim
3. Resume Tier 1 remaining slugs with protocol compliance from start
4. Standing rule #7 spot-check: owed — trace McKee 2007 or Lotan & Gold 2009 to specific BPC claim

## blockers
None. Context pressure forced handoff.
