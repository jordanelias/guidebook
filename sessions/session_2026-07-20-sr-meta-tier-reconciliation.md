# Session — sr_meta tier reconciliation + evidence-base state review (2026-07-20)

Branch: `claude/evidence-base-state-slug-lz8up0`

## Ask

Owner: "Tell me the state of our current evidence base per slug, then continue your research work."

## Part 1 — State of the evidence base per slug (read-only)

Regenerated the per-slice audit from `data/guidebook.db` (`tools/evidentiary_audit.py`, data as of
2026-07-20). Headline (pre-work baseline):

- 862 source-instances (755 unique) across 70/82 slices; **12 empty**.
- Grades: A=8 · B=16 · C=21 · D=14 · E=11 · F=12.
- Tier profile: T1=127, **T2=100**, T3=259, T4=76, T5=147, T6=136.
- Risk clusters: **18 no-anchor** (11 code-floor + 7 supporting-only), 12 empty, 15 doubly-Anglophone-
  concentrated, 3 mono-jurisdiction.

Full per-slug table is the audit itself (`audits/evidentiary-base-audit.{md,csv,json}`).

## Part 2 — Research batch: complete the sr_meta → T2 canonicalization

**Finding.** The enshrined rule (`governance/tier-system.md` §2, owner directive 2026-05-25 "t2>t3 this is
enshrined") places systematic reviews / meta-analyses at **T2**. The 2026-05-25 migration
(`data_20260525070000_sr_meta_t2_canonicalization.sql`) re-tiered only rows already typed
`evidence_type='sr_meta'` (its WHERE clause). A corpus scan found **22 T3 rows whose title/subtitle
self-identify as reviews** — of which **13 are genuine systematic reviews / meta-analyses mis-typed as
`clinical`/`grey`** and therefore never reached by that migration.

**Scope discipline.** Held back the doctrinally-unresolved cases rather than guessing: **8 scoping reviews**
(REF-00006/00089/00090/00131/00341/00427/00522/00527) and **1 rapid review** (REF-00069) stay at T3;
logged **GAP-298 (DEC, OPEN)** asking the owner to decide whether scoping / rapid / narrative reviews anchor
best-practice claims and at what tier.

**Migration 1** — `data_20260720044407_...sr-meta-tier-reconciliation.sql`: re-tiered 13 rows T3→T2
`sr_meta`; logged GAP-298. Five verified independently before migrating (REF-00398 WebFetch MDPI PRISMA;
REF-00097 PMID 36082841; REF-00240 PMID 28990665; REF-00642 WebSearch 4-db/23-study SR; REF-00570 WebSearch
PubMed+Scopus/23-study SR).

**Adversarial pass** (fresh-context refuter briefed to refute — batch-5 discipline). Re-retrieved the
un-verified rows and **caught one real error**: **REF-00589 is a NARRATIVE literature review, not a
systematic review** — PubMed PMID 35695710 article_types `["Journal Article","Review"]`; true title
"Considerations of the built environment for autistic individuals: A review of the literature," Black MH et
al., Autism 2022;26(8):1904-1915. The DB subtitle "systematic review." was a mislabel (how it slipped the
filter). The other 12 all re-confirmed genuine SRs (REF-00227 PMID 33421589, REF-00607 PMID 39246212,
REF-00638 PMID 37947544, REF-00639 PMID 35996349 confirmed in this pass; REF-00611/00637/00256 by the
refuter).

**Migration 2 (compensating)** — `data_20260720045138_...sr-meta-tier-reconciliation.sql`: reverted
REF-00589 T2→T3 `clinical`, corrected its title/subtitle, folded it into GAP-298 (narrative-review species).

**Net result.** 12 genuine SRs re-tiered T3→T2 (`T2` 100→112; `sr_meta` 38→50). No-anchor slices **18→17**:
`floor-vibration-wheelchair-disability` gained its first best-practice anchor (REF-00398, the wheelchair-WBV
PRISMA SR) — flipped supporting-only/grade E → anchored/grade D. `PRAGMA foreign_key_check` /
`integrity_check` clean after each migration; audit regenerated.

## Doctrine clarification from owner (captured, not yet enshrined)

Mid-session the owner clarified the tier model: **all tiers can anchor a best-practice claim, weighted by
tier strength** — T1/T2/T3 full, T4/T5 partial, T6/grey weak — with T4–T6-only claims stated but **flagged**
"best given current practice, not academically adjudicated." This largely matches the existing `●◐○` map
(`tier-system.md` §5) but conflicts with §3's binary "only T1/Co-1/T2/Co-2 anchor" language and the audit's
`no-anchor` flag. Owner wants my written understanding reviewed **before** any doctrine/audit rework — so
this is **captured pending owner sign-off**, not enshrined. (My SR re-tier is consistent either way: SRs are
full-strength regardless of the reconciliation.)

## Open / handoff

- **GAP-298 (DEC, OPEN):** tier placement of scoping / rapid / narrative reviews (9 rows parked at T3).
- **Doctrine decision pending:** enshrine the weighted-strength anchor model + rework audit (owner reviewing
  my written understanding first).
- **Grey-literature re-classification — owner scoped "non-English subset first":** of ~40 grey-flagged rows,
  12 are non-English (REF-00032 sv, REF-00137 fi, REF-00875 ko, + 9 de/ja/nl) — several look like real
  peer-reviewed papers mis-tagged grey via English-metadata langdetect, per the `research-handoff-non-english.md`
  §5 finding. Next batch. (~24 English "DOI-required" grey rows deferred.) Also: stale `grey_flag=1` on the
  now-verified REF-00097 / REF-00240 to clear in that batch.
