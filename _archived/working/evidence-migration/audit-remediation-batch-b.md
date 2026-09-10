# Evidentiary-audit remediation — Batch B (WS1, anchor recovery)

*Executes Batch B of `workplan/evidentiary-base-research-plan-2026-07-19.md`. WS1 = give the 20 no-anchor
slices their first best-practice anchor (T1/Co-1/T2/Co-2). 2026-07-19.*

## Method note — why this is "discovery," not "citation mining"

The batch was prompted by a request to "perform citation mining to depth 3, focused on Tier 1-3 sources."
True citation mining (backward = CrossRef references, forward = OpenAlex cited-by) **could not run this
session**: `api.crossref.org`, `api.openalex.org`, and `api.semanticscholar.org` all return `403 CONNECT
tunnel failed` from the egress proxy (organization policy; the proxy README says report, don't route
around — same block documented in batch 9). Fabricating mined citations is the one forbidden move, so with
owner sign-off the work pivoted to **real discovery via the reachable tools** — PubMed MCP and Scholar
Gateway — recorded honestly as evidence-expansion / WS1 anchoring, **not** as `citation_mining` rows (that
table's method is reference-graph traversal, which was not performed).

## What this batch changed (3 migrations)

**Migration 1 — `data_20260719232404_...batch-b-anchor-recovery.sql`:**
- Ingested two T2 systematic reviews as the first anchors for **`circadian-lighting-melanopic-edi`**
  (was T3×5/T4×2/T5×3, 0 anchors → now 2 anchors):
  - `REF-00771` — Tan et al. 2022, *Sleep Medicine* 90:153-166, DOI `10.1016/j.sleep.2022.01.013`
    (PubMed PMID 35180479; article_types = Meta-Analysis + Systematic Review; 18 RCTs, GRADE).
  - `REF-00772` — Goudriaan et al. 2021, *Clinical Interventions in Aging* 16:909-937,
    DOI `10.2147/CIA.S297865` (PMID 34079240; Systematic Review of indoor **ambient** light in dementia
    care — the built-environment-relevant one).
- Relinked orphan `REF-VERIFIED-003` to `stair-ramp-threshold-biomechanics-accessibility` **— later
  reversed, see Migration 2.**

**Migration 2 — `data_20260719233002_...batch-b-adversarial-correction.sql` (the batch-5 discipline):**
An independent refuting reviewer (fresh context, briefed to break the batch) **REFUTED** the
`REF-VERIFIED-003` relink on two counts, both confirmed against the DB:
1. **Duplicate DOI.** `REF-VERIFIED-003` is the *same paper* (DOI `10.1371/journal.pone.0269657`,
   Rouvier et al. 2022) as pre-existing **`REF-00037`**, with a *contradictory* grade.
2. **Misattributed author.** `REF-VERIFIED-003`'s author was a corporate "Lalumiere," not Rouvier et al.
   Anchoring from it would promote fabricated metadata.

PubMed (PMID 35737733) confirms the paper is a Systematic Review → **T2/sr_meta**, so `REF-00037`'s stored
**T3/clinical was the erroneous grade**. Reconciliation: corrected `REF-00037` (T3/clinical → T2/sr_meta,
report → journal_article), re-homed the stair/ramp/threshold anchor onto the correctly-attributed
`REF-00037`, and marked `REF-VERIFIED-003` `superseded_by_ref_id = REF-00037`. Net: the slice still gains
its first T2 anchor, now from a correctly-attributed, deduped row.

**Migration 3 — `data_20260719233236_...batch-b-completeness.sql`:** set
`doi_resolution_outcome='RESOLVED'` (both DOIs confirmed to resolve via PubMed) and added
`evidence_source_authors` rows (verbatim from PubMed) for REF-00771/00772, so the batch introduces **no new
DB-integrity failure** (C02 restored to pass; DB integrity back to baseline 30/35).

Confirmed sources (Tan, Goudriaan) stood; the reviewer's only caveats were about *claim-writing* (both
reviews are honest about inconclusive circadian effects — don't overstate them as strong positive warrants).

## Verification

- Anchors: `circadian-lighting-melanopic-edi` 0→2; `stair-ramp-threshold-biomechanics-accessibility` 0→1.
- `PRAGMA foreign_key_check` / `integrity_check` clean after every migration.
- Migration reproducibility: all 7 core invariants match a from-scratch rebuild (`evidence_source_authors`
  exempt per DR-2026-05-28).
- Audit regenerated: `evidence_sources` 675→677, `source_slug_links` 753→756; grade C count 19→20.

## Finding surfaced (deferred, not fixed here) — corpus-wide duplicate DOIs

Reconciling the REF-00037/REF-VERIFIED-003 pair surfaced that **~27 other DOIs still have 2–5 *live*
(non-superseded) `evidence_sources` rows each** (e.g. `10.26687/archnet-ijar.v8i1.314` ×5,
`10.31030/1803049` ×5, `10.4324/9781003564164` ×3). This is a pre-existing data-integrity backlog, not
introduced here. It inflates instance counts and risks the same contradictory-grade problem just fixed.
Recommend a dedicated **duplicate-DOI reconciliation batch** (dedup by DOI, keep the correctly-attributed
row, supersede the rest) — it is judgment-heavy (touches multiple slices) and should get its own adversarial
pass.

## Next

Continue WS1 on the remaining no-anchor slices (7 more supporting-only †, then the 11 code-floor ‡).
When a session has working egress to CrossRef/OpenAlex, run true depth-3 `citation_mining` over the 273
Tier 1-3 DOI-bearing backlog.
