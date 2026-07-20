# Session — grey-literature audit, non-English subset (2026-07-20)

Branch: `claude/evidence-base-state-slug-lz8up0` (restarted from `main` after PR #32 merged)

## Ask

Owner: "check all of our grey literature to confirm if it actually grey or if it is just foreign
language academic" — scoped by owner to the **non-English subset first**.

## Method

Of ~40 grey-flagged rows in `evidence_sources`, 12 carry a non-English `lang_detected`. Pulled each and
verified the 3 that looked like real journal articles via a real retrieval call (WebSearch / PubMed).

## Findings

**3 peer-reviewed academic sources mis-tagged grey (reclassified grey → clinical, within Tier 3):**

- **REF-00032** — the **OTIS RCT *study protocol*** (Cockayne/Pighills/Fairhurst, F1000Research 2021,
  DOI 10.12688/f1000research.52313.1), multicentre NHS England. Not grey, not Swedish. Corrected:
  `evidence_type` grey→clinical, `lang` sv→en, `jurisdiction` INT→GB. **Held at T3, not upgraded to a T1
  results anchor** — it is a protocol (methodology, not outcomes). The exact stored title ("…a study
  protocol for a multicentre randomised controlled trial") is what flagged this; an earlier read of only
  the WebSearch summary had briefly mis-scoped it as a completed RCT.
- **REF-00137** — Zallio & Clarkson, "…A study of architectural design practice," *Building and
  Environment* 206:108352 (Elsevier, peer-reviewed), an ethnographic study of 26 professionals. Not grey,
  not Finnish. Corrected: grey→clinical, `lang` fi→en.
- **REF-00875** — Lee Yong-Min & Kwon Oh-Jung, POE research-trend analysis, *J. Korean Inst. of Interior
  Design* 20(3):41-48 (2011), peer-reviewed. **Genuinely non-English academic** (lang `ko` correct).
  Corrected: grey→clinical.

**Key result:** 2 of the 3 were not even foreign-language — English papers mislabeled `sv`/`fi` by
langdetect running on English catalogue metadata, *and* dumped in grey. Only REF-00875 was genuinely
non-English academic. This confirms the owner's hypothesis and the `research-handoff-non-english.md` §5
langdetect-mislabel finding, in both directions.

**9 rows confirmed genuinely grey (left as-is):** REF-00221 (JP DINF booklet), REF-00764 (JP campus page),
REF-00755 (DE federal service portal), REF-00760 (DE planning handbook), REF-00762 (NL clinical workbook),
REF-00763 (DE architects' trade magazine), REF-00834/00835/00837 (DE policy-evaluation reports). These are
institutional / non-journal sources — grey is correct.

## Integrity

`evidence_type='grey'` count 32 → 29. `PRAGMA foreign_key_check` / `integrity_check` clean. Audit regenerated
(all reclassifications are within Tier 3 — no tier-number change, so grade movement is minimal; the point was
correctness of source-type and language, not anchor counts).

## Doctrinal scope note

All three moves are grey (`○`) → clinical (`●`) **within Tier 3** — a source-type correction under existing
doctrine, independent of the pending weighted-strength anchor-model decision the owner is still reviewing.

## Handoff — owner escalated scope

Owner: "you may need to check every single reference for correctness." The spot-checks in this branch's work
(sr_meta mis-tiers, grey mis-tags, wrong language tags, mislabeled titles, one narrative review mislabeled as
systematic, one firm cost-study mis-tiered as statutory code) indicate **systematic metadata-correctness debt
across the 779 `evidence_sources`**. A full per-reference correctness sweep (re-retrieval + tier/type/language/
title/DOI/link verification) is the natural next effort — best run as a multi-agent workflow with adversarial
spot-checks (pending owner opt-in). English grey subset (~24 rows) and the tier-model decisions (GAP-298,
GAP-299 practice-stream, weighted-strength) remain open.
