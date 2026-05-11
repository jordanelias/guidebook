# Session: Workplan consolidation + PI v10.8 staging
**session_start:** 2026-05-11 06:10 UTC (continuation of session_h post-close)
**session_close:** 2026-05-11 07:00 UTC
**PI version (live):** v10.6 (project settings still pending v10.8 deployment)
**PI version (repo):** v10.8 (committed but not yet deployed to live)
**Operative workplan (per v10.8):** `audits/bpc-rewrite-workplan-2026-05-11.md`

## Summary

Post-close follow-up to session_h. User decisively adopted BPC rewrite workplan as new operative plan and requested:
1. Update PI accordingly
2. Consolidate all active workplans into ONE authoritative document that supersedes all

Both done. PI v10.8 written and committed to repo at `governance/project-instructions-v10_8.md`. Master workplan extended with Appendix E (Supersession map) cataloguing all 54 files in `workplan/` by disposition. SUPERSEDED banners applied to 12 active workplan files; SUBORDINATE banners applied to 2 sub-protocol files that remain active under PI standing rules #7 and #8.

## Skills run

- (none formally invoked — governance/consolidation session, direct file operations)

## Deliverables committed

| File | Path | SHA | Action |
|---|---|---|---|
| PI v10.8 | `governance/project-instructions-v10_8.md` | a3bafb23199c | Created (22 KB, 276 lines) |
| PI deployment instructions | `decisions/PI-update-needed.md` | 058a49b3c9eb | Updated for v10.8 |
| Master workplan + supersession map | `audits/bpc-rewrite-workplan-2026-05-11.md` | e8a8350399e0 | Appendix E added (now 587 lines) |
| workplan-co0007-v4.md | `workplan/workplan-co0007-v4.md` | dba4ad7ffa29 | SUPERSEDED banner |
| workplan-reconciliation-2026-05-08.md | `workplan/...` | a9cd71c4f1ac | SUPERSEDED banner |
| workplan-item-audit-pipeline-co0009.md | `workplan/...` | abc17b045a8c | SUPERSEDED banner (now Phase F) |
| multilingual-search-remediation.md | `workplan/...` | 05236c9f8d4a | SUPERSEDED banner (now Phases B+C) |
| workplan-jurisdiction-sweep.md | `workplan/...` | a291c6f4df67 | SUPERSEDED banner (now Phase C) |
| evidence-expansion-2026-04-03.md | `workplan/...` | dcfea9d0d121 | SUPERSEDED banner (now Phase B) |
| website-preparation.md | `workplan/...` | 37af4ea15ee5 | SUPERSEDED banner (now Phase G) |
| co0008-scope-infrastructure-overhaul.md | `workplan/...` | a33ad61d25e4 | SUPERSEDED banner (now Phase A) |
| co0008-throughline-analysis.md | `workplan/...` | b233d46b95cb | SUPERSEDED banner |
| pi-update-co0008.md | `workplan/...` | 4bad50f05c7e | SUPERSEDED banner (PI v10.8) |
| pi-revision-co-paste-ready.md | `workplan/...` | d50abb295459 | SUPERSEDED banner (PI v10.8) |
| co0007-synthesis-workplan-2.md | `workplan/...` | 79f210a6f289 | SUPERSEDED banner |
| progressive-measurement-protocol.md | `workplan/...` | 989991fb538f | SUBORDINATE banner (PI rule #8) |
| research-protocol-adversarial.md | `workplan/...` | 63ef8b308bdc | SUBORDINATE banner (PI rule #7) |

**Total: 17 commits this session.**

## Workplan disposition summary (after consolidation)

| Disposition | Count | Files |
|---|---|---|
| OPERATIVE (single source of truth) | 1 | `audits/bpc-rewrite-workplan-2026-05-11.md` |
| SUBORDINATE (active sub-protocols under PI rules) | 3 | progressive-measurement-protocol, research-protocol-adversarial, hook-workplan-guidebook |
| SUPERSEDED (banner applied this session) | 12 | (per table above) |
| Already-DEPRECATED (banner applied prior to this session) | 6 | roadmap-2026-04-27, v10-5_2026-03-29, workplan-co0007-audit, workplan-co0007-synthesis, workplan-co0007-v3-amendments, workplan-co0007-v3 |
| HISTORICAL-COMPLETED (no banner — clearly dated handoffs) | ~20 | a1-a2, a4–a6, b1-*, co0007-stage-0_*, etc. |
| DECISION-SUPPORT (not workplans) | ~11 | placeholder-review-triage, gap-p1-reclassification, external-review-*, op*-adjudication, opus-synthesis-queue, struck-claim-research-attempt, economics-audit-research |
| **Total inventory** | **54** | All in `workplan/` |

## Next-session action required from user

**PI v10.8 deployment to live project settings.** Manual paste required. Until deployed:
- Live PI in claude.ai still on v10.6
- Bootstrap still references workplan-co0007-v4 as operative
- Standing rule #6 (canonical workplan) points to wrong file
- Bootstrap status block missing v10.8 evidence-base health metrics

Instructions in `decisions/PI-update-needed.md` (updated this session).

## YAML session-close block

```yaml
session_id: session_2026-05-11i-workplan-consolidation
session_close: 2026-05-11 07:00 UTC
deliverables_committed: 16 files
  - governance/project-instructions-v10_8.md (NEW)
  - decisions/PI-update-needed.md (UPDATED for v10.8)
  - audits/bpc-rewrite-workplan-2026-05-11.md (Appendix E added)
  - 14 workplan/*.md (SUPERSEDED or SUBORDINATE banners)
gaps_raised: 0
gaps_resolved: 0
skills_invoked: []
next_action: USER: deploy PI v10.8 to claude.ai live project knowledge per decisions/PI-update-needed.md
blockers:
  - PI v10.8 not yet deployed to live project settings; bootstrap will not pick up new operative workplan until deployed
workplan_state:
  operative: audits/bpc-rewrite-workplan-2026-05-11.md (587 lines, includes Appendix E supersession map)
  subordinate_protocols:
    - workplan/progressive-measurement-protocol.md (PI rule #8)
    - workplan/research-protocol-adversarial.md (PI rule #7)
    - workplan/hook-workplan-guidebook.md (PI hooks_status)
  superseded: 12 files banner-marked this session + 6 pre-existing
```
