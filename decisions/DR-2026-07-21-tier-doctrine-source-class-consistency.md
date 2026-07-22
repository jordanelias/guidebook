# DR-2026-07-21: Tier-doctrine consistency for four source classes (+ Steinfeld DOI-error)

- Status: **RATIFIED — owner directive 2026-07-21.** Surfaced by the same-DOI dedup batch
  (`workplan/dedup-audit-same-doi-multi-refid-2026-07-21.md`): the held groups can't be merged without
  first ruling the *tier* of the source, because the corpus tiers the same source differently across
  ingest passes. All five rulings ACCEPTED as proposed; the held-group merges/re-tiers and the Steinfeld
  DOI-fix are executed in migration `data_2026-07-21-…dedup-held-ratified`, and the §2 clarification is
  applied to `governance/tier-system.md`. (Was: PROPOSED — pending owner ratification.)
- Date: 2026-07-21
- Prepared by: Claude, on owner directive 2026-07-21 ("perform (i)").
- Affects (if ratified): the four held dedup groups + Black + Steinfeld; a short clarification to
  `governance/tier-system.md` on scoping reviews vs. systematic reviews, and on national accessibility
  standards vs. adopted code floors.
- Related: `governance/tier-system.md` (§2 tier definitions; §8 weighted-strength bands);
  `DR-2026-07-20-weighted-strength-anchor-model`; the dedup workplan; `DR-2026-07-13-…evidence-hierarchy`.

## Context — same-DOI dedup keeps surfacing tier drift

Deduping same-work rows repeatedly hit **tier disagreement between the duplicates** (the same source
tiered differently by different passes). Merging forces one tier, which is an evidence-doctrine call, not
a dedup — so six groups were held. Grounding query over the live corpus shows the *classes* are mostly
consistent already, which anchors the rulings below:

- **International technical standards** (ISO, IEC): **T4** — 14 ISO + 5 IEC rows, all T4. (Consistent.)
- **National frameworks** (`national_fw`): **T5** — 131 rows, all T5. (Consistent.)
- **Systematic reviews / meta-analyses** (`sr_meta`): **T2** — 56 rows, all T2. (Consistent.)
- **National accessibility *standards*** (DIN 18040, BS 8300, AS 1428): **inconsistent** — DIN spread
  across T3/T4/T5/T6; but BS 8300 sits predominantly at **T5** `national_fw`. This is the real gap.

## Decision — five rulings

1. **Scoping reviews are T3, not T2 (`sr_meta`).** `sr_meta` (T2) is reserved for *systematic* reviews
   and meta-analyses — a defined method with risk-of-bias appraisal and/or effect synthesis. A **scoping
   review** maps a literature without appraisal and is a weaker synthesis; it anchors at T3.
   → **Black** ("Considerations of the built environment for autistic individuals", verified a scoping
   review of 28 studies): re-tier T2 `sr_meta` → **T3**, then merge (canonical REF-00589, best metadata).

2. **National accessibility standards are T5 (`national_fw`) at the standard level.** DIN 18040 / BS 8300 /
   AS 1428 as *standards* are national recommended practice → **T5** (aligning with BS 8300's dominant
   treatment and the invariant `national_fw` = T5). The **exception**, preserved: where a citation is
   specifically to a provision **adopted as a mandatory code floor** (e.g. via the Technische
   Baubestimmungen), that instance is T6 `code` (weak-band convergence floor). The deduped canonical
   carries the **standard-level T5** unless the surviving citation is specifically the code-floor use.
   → **DIN 18040-2** and **DIN 18040-1** groups: normalize the canonical to **T5**, then merge.

3. **Peer-reviewed conceptual/framework papers are T3, not T2.** A framework-proposing primary paper
   (peer-reviewed, but not a synthesis) is T3, not `sr_meta`. → **ASPECTSS** (Mostafa 2014, "Architecture
   for Autism", ArchNet-IJAR — a design-index framework paper): re-tier the T2 rows → **T3**, then merge.

4. **Professional design guides are T5 (`national_fw`), not T1/T2.** A professional-body design guide is
   recommended practice, neither primary research (T1) nor systematic review (T2). → **RIBA/Habinteg/CAE
   Inclusive Housing Design Guide (2024)**: normalize to **T5**, then merge. (If the owner prefers the
   practitioner `practice`/Co-3 stream from `DR-2026-07-20`, that is the alternative; T5 is the pragmatic
   default.)

5. **Steinfeld is *partly* a DOI-error — 2 works, not 3 (corrected in execution, see v3).** DOI
   `10.1080/10400430903520280` / PMID 20402047 belongs to the journal article, which appears under **two
   ref_ids** — **REF-00059** ("Anthropometry and Standards for Wheeled Mobility") and **REF-00192** (same
   paper with its full subtitle "…An International Comparison") — so those two are the **same work and are
   merged** (REF-00192 → REF-00059). Only the IDEA Center **"Final Report" (REF-00060)** is a genuinely
   **distinct** work that had inherited the journal DOI → its DOI is nulled (NO-MATCH; a report with no
   DOI) and its audit trail restored via the report URL. (The v1 proposal wrongly called REF-00192 a third
   distinct output; the adversarial verification pass corrected this before merge.)

## Consequences if ratified
One dedup/re-tier migration resolving the six held groups (2 re-tiers to T3 for Black/ASPECTSS;
normalize DIN and the RIBA guide to T5; merge; Steinfeld DOI-null). A two-line clarification to
`tier-system.md` §2 (scoping-review ≠ systematic-review; national-standard-vs-code-floor). Distinct
linked sources drop further as the last twins merge. No source deleted (forward-only supersession).

## What would make this ACCEPTED
Owner confirms the five rulings — in particular (2)'s standard-vs-code-floor split and (4)'s T5-vs-Co-3
choice for professional design guides, the two genuine judgment calls. Rulings 1, 3, 5 are
doctrine-consistency corrections with little latitude.

## Revision history
- v1 (2026-07-21): initial proposal on owner directive, grounded in the live-corpus class tiering.
- v2 (2026-07-21): RATIFIED by owner. All five rulings accepted (incl. the standard-vs-code-floor split
  and the design-guide → T5 default). Held-group merges/re-tiers + Steinfeld DOI-fix executed; §2
  clarification applied to tier-system.md.
- v3 (2026-07-21): **adversarial-pass correction to ruling 5.** Verification (PMID 20402047) showed
  REF-00192 is the *same* journal article as REF-00059 (its full-subtitle form), not a third distinct
  output — so it was **merged** into REF-00059, not DOI-nulled. Only REF-00060 (the IDEA Center Final
  Report) is distinct; its DOI is nulled (NO-MATCH) and its audit trail restored via the report URL.
  Net: Steinfeld = 2 works, not 3. DB integrity returned to the main baseline (no net regression); the
  earlier DOI-null had transiently broken checks C01/C04, now resolved.
