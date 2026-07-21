# Dedup audit — same-DOI, multiple `ref_id` (2026-07-21)

**Status:** Active workplan. Surfaced during Batch-1 careful checking (D/E remediation). Records a
data-model inconsistency and a scoped, per-case dedup queue. **1 confirmed twin fixed; the rest is a
reviewed batch, not a bulk merge.**

## The finding

The corpus mixes two representations of a source shared across slugs:
- **Correct (target) model — one row, many links:** one `evidence_sources` row linked to N slugs via
  `source_slug_links` (e.g. REF-00050 spans 6 slugs). This is what the audit's "unique sources" count
  assumes.
- **Divergent — many rows, one DOI:** the same DOI appears under multiple `ref_id`s. Where both rows
  are active, this is a dedup-discipline violation ("match on DOI… never create a twin") that **inflates
  the "unique sources" headline** and double-counts the source across slices.

**Convention for fixing (precedent: REF-VERIFIED-003 → REF-00037):** set `superseded_by_ref_id` on the
duplicate to the canonical `ref_id`, **repoint its `source_slug_links` to the canonical row**, and
**retain** the superseded row (forward-only; do not delete). Counts stay stable (evidence_sources
unchanged; links net-zero); distinct-linked `ref_id`s drop by one per merged twin.

## Classification of the 29 multi-`ref_id` DOIs

| Class | Count | Disposition |
|---|---|---|
| **Already resolved** (a member is superseded) | 1 | `10.1371/journal.pone.0269657` — none needed. |
| **Confirmed true twin — FIXED 2026-07-21** | 1 | `10.1155/2017/2865960` (REF-00454 → superseded_by REF-00407; link repointed). |
| **Likely-legitimate container-DOI split** | 5 | DIN standards `10.31030/1715500` `…/1803049` `…/2853913`; Routledge book `10.4324/9781003564164`; ArchNet-IJAR `10.26687/…`. Parts/chapters share a container DOI — **verify per-case, probably keep** (distinct parts are legitimately distinct sources). |
| **Live-dupe candidates** (same DOI, ≥2 active rows, not container) | 22 | Per-case: confirm same work, pick the best-metadata canonical, supersede the rest, repoint links, adversarial spot-check. |

**Live-dupe candidate DOIs (22):** `10.1002/14651858.CD013258.pub2`, `10.1016/S0140-6736(14)61006-0`,
`10.1016/j.buildenv.2021.108352`, `10.1016/j.dhjo.2022.101281`, `10.1016/j.ergon.2014.07.001`,
`10.1016/j.mayocp.2021.07.004`, `10.1016/j.msard.2022.104075`, `10.1044/2022_LSHSS-21-00181`,
`10.1080/10400430903520280`, `10.1108/arch-07-2023-0178`, `10.1136/bmjopen-2020-046647`,
`10.1177/13623613221102753`, `10.1177/13623613231180266`, `10.1177/1533317509334959`,
`10.1177/193758671100400207`, `10.1177/1937586717730338`, `10.1177/19375867211043546`,
`10.2196/60622`, `10.2196/69442`, `10.3233/wor-210997`, `10.3389/frdem.2025.1524425`,
`10.3390/ijerph192114279`.

## Recommended batch
1. **Verify the 5 container splits** — confirm each `ref_id` is a genuinely distinct part/chapter (keep) vs a sloppy dup (merge). Likely keep most.
2. **Per-case the 22 live-dupe candidates** — for each: confirm the rows are the same work (same DOI is strong but check for DOI-entry errors), choose the canonical (best/most-complete metadata, VERIFIED-2 preferred), supersede the rest + repoint links, adversarial spot-check a sample.
3. **Re-run the audit** — the "781/780 unique" headline drops by the number of merged twins; per-slice counts self-correct.
4. **Consider a small DR** on the shared-source model (one-row-many-links as the canonical representation) so new ingests dedup on DOI by default and this stops recurring — the same discipline the tier system applies to convergence, applied to identity.

## Guardrail
Do **not** bulk-merge on same-DOI alone. A shared DOI is strong evidence but not proof (container DOIs,
DOI-entry errors); each merge is a per-case judgment with a chosen canonical, and the superseded row is
retained, never deleted.
