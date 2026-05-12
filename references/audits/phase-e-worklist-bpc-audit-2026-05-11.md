# Phase E Worklist — BPC Completeness Audit

**Audited:** 2026-05-11 · 83 BPC documents in `references/bpc/`
**Excludes:** 16 population-code orphans (`ALL-ENV`, `DBL`, `DEAF`, `DEM`, `MOB`, `NDV`, etc.) — already deleted from `bpc_metadata`; remaining as files for archival reference
**Method:** Score each BPC 0–7 across seven completeness dimensions

---

## Scoring rubric

| Dimension | Worth | Detection |
|---|---|---|
| Opus synthesis flag | 1 | `opus_synthesis: true` in metadata or `[OPUS-SYNTHESIS]` in header |
| Opus reasoning note substantive | 2 | `**Opus 4 note:**` field has >100 chars of actual reasoning, not "NONE" or placeholder |
| Best-practice synthesis substantive | 1 | Section exists with >200 chars of content |
| Consensus findings (≥3 rows) | 1 | At least 3 populated rows in consensus table |
| Key sources (≥5 entries) | 1 | At least 5 numbered REF-ID rows in key sources table |
| Citation mining run | 1 | Citation mining section has populated source rows |
| Functional-deficit pass (FDR) | 1 | Bottom-up findings table has populated rows |

The Opus reasoning note is weighted double because it captures the synthesis logic — *why this value, not the alternatives* — which is the actual unit of intellectual work the rewrite needs to produce.

---

## Score distribution

| Score | BPCs | Description |
|---|---|---|
| 7+/7 | 1 | Exemplar — fully complete |
| 6/7 | 1 | Nearly complete (missing one dimension) |
| 5/7 | 9 | Substantial; common gap is FDR or Key Sources |
| 4/7 | 7 | Has structure but reasoning trail thin |
| 3/7 | 15 | Skeleton populated; reasoning absent |
| 2/7 | 26 | Stub with citation mining placeholder |
| 1/7 | 14 | Stub only |
| 0/7 | 10 | Empty stub |

**Total Phase E work to bring all BPCs to score 7+: 82 BPCs × estimated 8–20h each = roughly 800–1,600 hours of synthesis work.** This is consistent with the workplan's overall 2,300h estimate for the full rewrite.

---

## Exemplars (use as models for rewrites)

1. **`accessible-bathroom-and-grab-bar`** (score 8/7) — the canonical example. 22KB, all sections populated, substantive Opus 4.6 synthesis note enumerating five specific refinements over the Sonnet draft with citations. **Read this first before any other BPC rewrite session.**

2. **`residential-kitchen-and-task-surfaces`** (score 6/7) — secondary model. 12KB, mostly complete, missing only the Opus reasoning trail.

---

## Recommended remediation order

The fastest path to comprehensive coverage is to tackle BPCs in score-descending order — closing the 5/7s first, then 4/7s, then expanding the 3/7 skeletons. Reasoning:

- **5/7 BPCs (9 docs)** already have most structure. They need an Opus synthesis note and a fully-populated synthesis section. Estimated 4–8h each → ~60h to close all nine.
- **4/7 BPCs (7 docs)** need reasoning trail + table completion. Estimated 6–10h each → ~50h.
- **3/7 BPCs (15 docs)** are skeletons; this is where citation-mining backward/forward becomes the biggest piece. Estimated 10–15h each → ~190h.
- Lower scores require both content authorship and reasoning. Roughly 12–20h each.

If a future synthesis session has only a few hours, it should pick from the 5/7 list:

### 5/7 BPCs — closest to complete

| Slug | Size | Missing |
|---|---|---|
| `accessibility-feature-market-value-uplift-framing` | 29KB | FDR pass not run; Opus reasoning note thin |
| `deaf-acoustic-built-environment` | 9KB | Key sources count low; FDR not run |
| `deaf-spatial-design` | 10KB | Consensus rows; key sources; FDR |
| `deafblind-built-environment-design` | 12KB | Consensus rows; key sources; FDR |
| `dementia-built-environment` | 10KB | Consensus rows; key sources; FDR |
| `mobility-built-environment` | 19KB | Consensus rows; key sources; FDR |
| `neurodivergent-built-environment` | 8KB | Consensus rows; key sources; FDR |
| `neurological-built-environment` | 7KB | Consensus rows; key sources; FDR |
| `visual-impairment-built-environment` | 6KB | Consensus rows; key sources; FDR |

Pattern: most of these are population-spanning BPCs (`*-built-environment`). They have Opus reasoning notes but lack the consensus tables and FDR passes that the topic-specific BPCs have. A single dedicated session per population could close all nine.

### Stubs (0–1/7) that need ground-up authorship

Eighteen BPCs are essentially placeholder files. Recommended to defer until structural BPCs are closed — they would benefit from the patterns established by completing the 5/7 group first.

---

## File-level issues

### Two duplicate slugs across paths

- **`cross-population-conflict-resolutions.md`** exists in two locations:
  - `references/bpc/cross-population/cross-population-conflict-resolutions.md` (11.8 KB)
  - `references/bpc/frameworks-and-methodology/cross-population-conflict-resolutions.md` (13.7 KB)

  The frameworks version is 16% larger. Likely the canonical one, but content comparison required before deciding.

- **`thermoregulation-built-environment.md`** also exists in two locations:
  - `references/bpc/health-and-symptom-management/thermoregulation-built-environment.md` (13.5 KB)
  - `references/bpc/thermoregulation-built-environment.md` (12.2 KB)

  The directory-level one (health-and-symptom-management) is slightly larger. Likely canonical given the consistent directory convention used elsewhere; the top-level file is probably an artifact of a refactor.

Both duplicates need to be reconciled — keep the canonical version, delete the other, update any `slugs.bpc_path` references in the database to match.

### sub-1KB files (placeholder-only)

These BPCs exist but contain only the template header + metadata:

| Slug | Size |
|---|---|
| `bariatric-turning-radius-built-environment` | ~2 KB |
| `school-environment-autism` | ~2 KB |
| `government-grant-programmes` | ~2 KB |
| `visual-alerting-and-wayfinding-light` | ~2 KB |

Treat these as Phase E priority 3 — placeholder structure exists, content needed.

---

## What this audit unblocks

1. **Targeted Phase E sessions.** Any future synthesis session can pick a specific 5/7 BPC and know exactly what to fill in. No more guessing what counts as "complete."
2. **Workplan effort calibration.** The 800–1,600h estimate gives the workplan's ~2,300h total credibility — Phase E alone is two-thirds of the remaining work.
3. **Exemplar pattern.** The `accessible-bathroom-and-grab-bar` Opus synthesis note structure — "*N refinements over the Sonnet draft: (1) ... (2) ..."* — can be lifted as the standard reasoning-trail format for every future synthesis.
4. **Duplicate file cleanup.** Two BPCs have ambiguous canonical paths; resolving these prevents future updates from forking the docs further apart.

---

## Suggested next sessions

| Session | Target | Estimated effort | Expected outcome |
|---|---|---|---|
| **E.1** | Resolve the two duplicate-slug files; align `slugs.bpc_path` | 1 h | Single canonical version of each |
| **E.2** | Close 5/7 BPCs by population family (e.g., all `*-built-environment`) | 8–10 h | 3 population-level BPCs upgraded to 7/7 |
| **E.3** | Establish the Opus reasoning-note pattern as a fragment template | 2 h | Reusable structure for all future syntheses |
| **E.4** | Sprint on 4/7 BPCs (7 docs) | 30–40 h | All 4/7 BPCs upgraded to 6+/7 |

The single highest-value next action is **E.3 — codify the Opus reasoning-note pattern as a reusable fragment**, since that compounds across every future BPC rewrite.

---

## Complete per-BPC scores

Full audit data with all scoring dimensions is preserved in `references/audits/bpc-completeness-audit-2026-05-11.json` for use by automated workplan tooling.
