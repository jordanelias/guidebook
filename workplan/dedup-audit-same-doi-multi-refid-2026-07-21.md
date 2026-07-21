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

## Execution status (2026-07-21)

**DONE — 16 confirmed same-work groups merged** (migration `data_20260721203616_…dedup-batch-16-clean`).
Per-case verified: matching first-author + title, tier-consistent. 18 duplicate rows superseded_by their
canonical, links repointed (2 redundant links dropped where the canonical already had the slug), rows
retained. **Distinct linked `ref_id`s 780 → 762.** Determinism + integrity clean. Canonicals:
REF-00901, REF-00134, REF-00030, REF-00223 (absorbed 3 twins), REF-00570, REF-00296, REF-00069,
REF-00542, REF-00007, REF-00202, REF-00033, REF-00301, REF-00395, REF-00393, REF-00488, REF-00090.

**HELD — 6 groups need per-case judgment, deliberately NOT merged mechanically:**
- **Tier-conflict (4)** — same work carried at *different tiers* across rows; merging forces a tier choice,
  which is an evidence-adjudication call, not a dedup: `10.1016/S0140-6736(14)61006-0` (Keall, T1 vs T3 —
  likely T1 RCT), `10.1016/j.msard.2022.104075` (Christogianni, T2 vs T3; note one row already unlinked),
  `10.1177/13623613221102753` (Black, T2 vs T3), `10.2196/69442` (Levine, T1 vs T3 + paraphrased title).
- **DOI-error (2)** — rows share a DOI but describe *different works* → not duplicates; one row has a
  wrong DOI to correct: `10.1016/j.buildenv.2021.108352` (REF-00171 "Accessible toilet failures" ≠ the
  Zallio IDEA paper), `10.1080/10400430903520280` (Steinfeld — article vs "Final Report" vs "standard",
  3 distinct outputs).

**Still to verify — 5 likely-legit container-DOI splits:** DIN standards `10.31030/1715500` `…/1803049`
`…/2853913`; Routledge book `10.4324/9781003564164`; ArchNet-IJAR `10.26687/…`. Confirm each `ref_id` is
a genuinely distinct part/chapter (keep) vs a sloppy dup (merge). Likely keep most.

## Next
1. **Resolve the 4 tier-conflict groups** — adjudicate the correct tier per `governance/tier-system.md`, set it on the canonical, then merge (same pattern).
2. **Fix the 2 DOI-error groups** — correct the wrong DOI on the mis-attributed row (do NOT merge).
3. **Verify the 5 container splits** — keep distinct parts; merge only true dups.
4. **Consider a small DR** on the shared-source model (one-row-many-links as canonical) so new ingests dedup on DOI by default and this stops recurring — the identity analogue of the convergence discipline.

## Guardrail
Do **not** bulk-merge on same-DOI alone. A shared DOI is strong evidence but not proof (container DOIs,
DOI-entry errors); each merge is a per-case judgment with a chosen canonical, and the superseded row is
retained, never deleted.
