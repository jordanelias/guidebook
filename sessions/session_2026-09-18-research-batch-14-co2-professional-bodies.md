# Batch 14 — finishing the Co-2 pass, and two capture misses the author caught

**Session:** `session_2026-09-18-research-batch-14-co2-professional-bodies`
**Parameter:** 3 (TERM-001, ramp gradient) · **Slug:** `accessible-circulation-geometry`
**Priors:** `scratchpad/batch-14-co2-professional-bodies/PRIORS.md`, committed `6893397` before the first query.

---

## 1. Why this batch existed

Batch 13's own attestation, written against itself:

> R1 remains partly unrun after a batch named for it, and the next batch should start with WFOT,
> CAOT and Occupational Therapy Australia before anything else.

This is that batch. Derived before opening: 5 co2-targeted searches existed across AU/GB/UK/US, **no
INT search and no CA search had ever been run.**

## 2. Three professional bodies, three outcomes

| Body | Jurisdiction | Outcome |
|---|---|---|
| **CAOT** | CA | *OT Practice Document: Home Assessment and Modifications*, Spring 2024 — **read in full, 2 pages. Genuine absence.** |
| **OTA** | AU | *FAQ: Environmental and Home Modifications* — **admitted REF-00998**, and it states no gradient |
| **WFOT** | INT | **Weak evidence.** Site 403s; the archived resource index is a JavaScript shell |

**CAOT is the cleanest result.** A national OT professional body's practice document on home
modification: the word *ramp* occurs **once**, in a list of what an OT recommends — "bar grabs,
handrails, ramps, raised toilet seats" — and *gradient*, *slope*, *1:12* and *1:20* occur **zero
times**. Its companion fact sheet contains none of them either. **This is RCOT's *Adaptations without
Delay* result replicated in Canada**, and it is a full read, not a retrieval failure.

**WFOT is the honest weak point and is labelled as such.** The open-web query returned building-industry
pages and not one `wfot.org` result — a query-shape failure, not evidence about WFOT. The R10 ladder
reached the archived resources index (200, 103,053 bytes), whose text contains zero occurrences of
*ramp*, *gradient*, *accessib\**, *housing* or *built environment* — **but it is a navigation shell
with ~3,800 characters of extractable text, so its silence is a rendering fact as much as a content
fact.** Logged `saturation-signal: none`. WFOT remains the least-searched of the three.

## 3. The finding that changes what a reader should believe

REF-00998 states no gradient. What it states is a **scope limitation**:

> AS 1428.1:2021 provides the minimum design requirements for building work to enable access for
> people with disabilities in Class 2-9 buildings. **As such, it does not apply to Class 1 and 2
> buildings**, which are single dwellings (like houses) and those with multiple units (like
> apartments), respectively.

**REF-00997 — admitted last batch — recommends 1:14 and 1:8 for ramps at private homes and grounds
those figures in AS 1428.1.** The Australian professional body says AS 1428.1 does not reach private
homes. So the figure governing home ramps in that document is **borrowed from a standard that
formally excludes homes.** REF-00997 half-acknowledges this in its own words — *"even a ramp at a
private home is likely to be accessed by members of the public at times"* — which is a rationale for
borrowing, not a claim that it applies.

It changes no number: it supplies no value, and REF-00998 is T5, so it is not an anchoring-tier
finding either. **What it changes is what a reader should believe about the number.**

## 4. The tier call, made against the batch's interest again

Occupational Therapy Australia **is** the OT professional body, so Co-2 was genuinely live. Refused:
Co-2 in `governance/tier-system.md` means professional-body **clinical practice guidelines**, and an
FAQ page explaining an Australian Standard is not one — no clinical warrant, no consensus process, no
cited evidence. Admitting it Co-2 would have handed this batch the Co-2 source it was convened to find.

**Still zero Co-2 sources**, now across five jurisdictions and six searches.

## 5. Two capture misses, caught by the author mid-batch

Asked whether the other relevant concepts were being logged as intended, the answer was **no**.
Measured on batch 13: `observed_terms` 3, `search_candidates` 2, `evidence_population_match` 1,
`gaps` 1 — but **`research_code_leads` 0 and `economics_entries` 0.**

- **No code lead for AS 1428.1**, despite REF-00997's entire warrant resting on it. Six AS 1428.1
  leads exist from the 2026-09-02 restore, but none carries the ramp-gradient clause. Batches 09 and
  10 both filed leads; 13 filed none. **Fixed here:** leads 87 (AS 1428.1:2021 ramp gradients) and 88
  (Livable Housing Design Standard), both REFERENCE-ONLY with the paywall and the scope caveat recorded.
- **An economics finding left in prose.** The Foundations page states *"There is little research
  investigating the cost comparison between rampscaping, traditional ramps and lifts."* R12 sends that
  to `economics_entries`, not a note. **Fixed here:** ECON-001, `construction` / `research_gap`, filed
  with `--source` because the Foundations page is resolved OUT-OF-SCOPE and holds no ref_id. Filed
  forward rather than backdated: batch 13's migration is committed and rule 3 is fix-forward.

`economics_entries` held **0 rows** before this batch. The table existed and nothing had ever reached it.

## 6. The batch-13 lesson, applied

Batch 13's attestation recorded: *run the blocking batteries against the scratch DB before emitting,
not after applying.* Done here, and it paid twice:

- **K02** failed the moment extraction 36 existed — specification 6 could not account for it. Retired
  and re-determined **on scratch**, before any migration was written.
- **R3** failed because REF-00998 carried no pinpoint. The convention, derived from the eight existing
  regulatory-stratum rows, is that `evidence_sources.pages` holds a **locator**, not a page count —
  REF-00996, also a web page, carries a breadcrumb there. Fixed to `FAQ › How should AS1428.1 be applied?`
  before emitting.

Neither reached CI. Batch 13's two equivalents both did.

*Recorded against my own prior work:* **REF-00997's `pages` is `3`, the document's page count, not a
pinpoint.** It satisfies R3 mechanically and is weaker than every other regulatory row in the corpus.
Not corrected here — it is committed, and the value is unhelpful rather than false.

## 7. The determination

```
param 3×MOB   provisional   max 5 %   ·   max 1:20      spec 6 → 7, refs 8, extractions 26
```

Unchanged. REF-00998 supplies no value and does not anchor.

## 8. Owed after this batch

- **WFOT, properly.** Untried rungs: the members area, position statements as individually-linked
  PDFs, the WFOT Bulletin in a journal index. Candidate 87.
- **Livable Housing Design Standard** (lead 88) — the instrument that *does* cover private dwellings,
  named by OTA with a direct URL and not retrieved here. If it states a gradient for dwellings it is
  the first instrument in this corpus governing the setting a home ramp is actually in.
- **AS 1428.1:2021 ramp clause** (lead 87) — paywalled at Standards Australia, REFERENCE-ONLY.
- **AOTA ladder rungs** (candidate 85), **GAP-002** still open, **GAP-005** and **GAP-007** unfixed.
