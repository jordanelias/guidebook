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

**RESOLVED — 4 of the 6 held groups merged after per-case adjudication** (migration
`data_20260721204803_…dedup-held-tierconflict`; 7 duplicate rows superseded; distinct linked 762 → 756):
- `10.1016/S0140-6736(14)61006-0` (**Keall**) — HIPI **RCT** (Lancet 2015) → **T1**; canonical REF-00373.
- `10.1016/j.msard.2022.104075` (**Christogianni**) — patient survey, **not** a standard → tier-fixed
  T2 `standard_eb` → **T3 clinical**; canonical REF-00254.
- `10.1016/j.buildenv.2021.108352` (**Zallio**) — NOT a DOI-error: REF-00171's own note confirms
  "Accessible toilet failures" is claim-framing of the same IDEA paper → **T3** merge; canonical REF-00136.
- `10.2196/69442` (**Levine**) — verified observational **biomechanical** study (motion capture/ANOVA,
  JMIR 2025 e69442), **not** an RCT → tier-fixed T1 → **T3 clinical**; canonical REF-00367.

**STILL HELD — 2 groups:**
- `10.1177/13623613221102753` (**Black**) — verified a **scoping review** (5 databases, 28 studies).
  Contested tier: the 07-20 pass set T2 `sr_meta`, but strict doctrine reserves `sr_meta` for *systematic*
  reviews/meta-analyses — a scoping review is arguably T3. Needs an owner/tier-doctrine ruling before merge.
- `10.1080/10400430903520280` (**Steinfeld**) — genuine DOI-error: 3 *distinct* outputs (journal article
  REF-00059 holds the DOI by PMID; "Final Report" REF-00060 and "International Comparison" REF-00192 are
  different works). Needs bibliographic verification of the correct DOIs — a correction, not a merge.

**The "5 container-DOI splits" hypothesis was WRONG (verified 2026-07-21).** None are distinct parts —
all are same-work duplicates:
- `10.31030/2853913` (**IEC 60118-4**, hearing-loop std, 3× all T4) — **MERGED** (canonical REF-00200;
  migration `data_20260721205113_…dedup-iec-clean`; distinct linked 756 → 754).
- **HELD — same-work dups with tier drift** (merging forces a tier choice on *foundational* sources →
  defer to a tier-doctrine pass, not an ad-hoc dedup call): `10.31030/1803049` (DIN 18040-2, 5×, T4/T6),
  `10.31030/1715500` (DIN 18040-1, 3×, T5/T6), `10.26687/archnet-ijar.v8i1.314` (ASPECTSS / Mostafa 2014
  framework paper, 5×, T2/T3), `10.4324/9781003564164` (RIBA/Habinteg Inclusive Housing Design Guide, 3×,
  T1/T2 — a design *guide*, so both tiers are likely wrong).

**Broader finding:** same-DOI duplication very often carries **tier drift** (the same source tiered
differently by different ingest passes). Deduping therefore repeatedly surfaces tier-consistency questions.
The held set below is really a **tier-doctrine consistency pass** (what tier is DIN 18040 / the ASPECTSS
index / a professional design guide?), not more dedup.

## Next
1. **Resolve the 4 tier-conflict groups** — adjudicate the correct tier per `governance/tier-system.md`, set it on the canonical, then merge (same pattern).
2. **Fix the 2 DOI-error groups** — correct the wrong DOI on the mis-attributed row (do NOT merge).
3. **Verify the 5 container splits** — keep distinct parts; merge only true dups.
4. **Consider a small DR** on the shared-source model (one-row-many-links as canonical) so new ingests dedup on DOI by default and this stops recurring — the identity analogue of the convergence discipline.

## Guardrail
Do **not** bulk-merge on same-DOI alone. A shared DOI is strong evidence but not proof (container DOIs,
DOI-entry errors); each merge is a per-case judgment with a chosen canonical, and the superseded row is
retained, never deleted.
