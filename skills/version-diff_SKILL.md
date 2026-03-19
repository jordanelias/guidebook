---
name: version-diff
description: >
  Produce a semantic diff between two versions of the Accessible Built Environments Guidebook.
  Not a line diff — identifies changes in arguments, citations, framing, evidence stratification,
  and item codes. ALWAYS use this skill when asked to: compare guidebook versions, identify what
  changed, produce a change summary, assess whether revisions improved or regressed content,
  or track changes between editions.
  Trigger on: "compare versions", "what changed between", "version diff", "track changes",
  "was this an improvement", "revision comparison".
---

**Model:** Sonnet 4.6
**Intake:** both versions as section-aligned pre-chunked inputs. Not aligned → haiku-chunker Mode A on both first.

## Change Types
ADDED · REMOVED · REFRAMED · CITATION_CHANGED · STRATUM_CHANGED · CRITERIA_CHANGED · ITEM_CODE_CHANGED · STRUCTURAL

## Steps
1. Confirm section alignment. Flag sections present in one version only.
2. Per section: list all changes by type.
   - REFRAMED → note direction: toward social model (improvement) or toward medical model (regression)
   - CITATION_CHANGED → type (added/removed/substituted) + evidence quality direction
   - STRATUM_CHANGED → direction (upgrade/downgrade)
   - CRITERIA_CHANGED → old value · new value; flag departure from cited standard
3. Assess each change: IMPROVEMENT · REGRESSION · NEUTRAL · REQUIRES_REVIEW

## Output
| Section | Change Type | v(n) (summary) | v(n+1) (summary) | Assessment | Notes |

Summary: total changes · IMPROVEMENT: N · REGRESSION: N · NEUTRAL: N · REQUIRES_REVIEW: N
Net assessment: IMPROVED / REGRESSED / MIXED / NEUTRAL
Regressions requiring immediate attention: [list]
