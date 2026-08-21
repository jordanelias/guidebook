# Digesting the pilot reasoning document into leads

**Date:** 2026-08-21. **Session:** `session_2026-08-21-reasoning-doc-digestion`.
**Acting on:** owner directives D-1 (scaffolding/prose → leads) and D-2/D-2a (prose is never the
body) — recorded at §2c of `workplan/2026-08-20-provenance-walk-execution-plan.md`.

## The finding this uncovered, which is the point of the whole exercise

`references/bpc-reasoning/room-acoustic-performance.md` is not a stub. It is a 41 KB Pass-1 pilot
reasoning document authored 2026-05-15/17 containing, **in prose**:

- a **16-jurisdiction RT60 comparison table** with actual values (ANSI/ASA ≤ 0.6 s general and
  ≤ 0.3 s for hearing-aid/CI users under Footnote e; BB93 0.4–0.8 s and ≤ 0.4 s specially
  resourced; DIN 18041 target curve 0.4–0.8 s; UNI 11532-2 class A4 ≈ 0.5 s; and nine more);
- per-population worst-case-user statements for DEAF, NDV/AUT, DEM, NEU/PCS, OFS/PAIN and general;
- **Bettarello 2021 (REF-00561) recorded as proposing 0.4–0.7 s for autism-friendly spaces** —
  the very figure the 2026-08-21 adversarial pass "discovered" independently via OpenAlex;
- **Marzi 2025 (REF-00727) quoted verbatim** documenting the *absence* of autism-specific
  quantitative acoustic data — a first-class R7 absence finding;
- Iglehart 2020 (REF-00325) as the Tier-1 anchor for PMP-A18-001 strict termination at 0.30 s.

**The August 2026 research batch re-searched a question this project had already substantially
worked, and never read this document.** The 2026-08-06 clean-room reset removed every
`evidence_sources` row it cites, orphaning all 11 citations; the restart then proceeded as though
the slug were unexplored. Two of the 11 orphans are the OD-5 witnesses themselves (REF-00561,
REF-00578).

This is D-2 demonstrated rather than argued: reasoning held in prose was invisible to the pipeline
*and* to the researchers.

## What was written

**27 `search_candidates` leads** (`PENDING-VERIFICATION`, `exec_id` NULL — no search surfaced
these, a document did):
- 11 orphaned REF-ids, each with its held DOI and the doc's own tier guess carried forward **as a
  guess** (R15);
- 2 sources the doc names as never having had a REF-id at all (BrainXchange Canada; Lyngby-Taarbæk
  POE, both flagged "ref not yet linked");
- 12 standards to retrieve for A-18, one per jurisdiction;
- 2 entries that are not jurisdictions (the Nordic DK/NO/SE/FI composite; WELL Building Standard).

`jurisdictional_values` is **unchanged at 109 rows, 0 with a value** — see below.

## A mistake made and fixed forward, recorded because it is instructive

The first migration (`data_20260821185244`) wrote **12 rows carrying claimed values** into
`jurisdictional_values`, each marked `[UNVERIFIED-QUANT]`. That was wrong. Every file in the
table's YAML mirror carries a header recording an **owner ruling of 2026-08-12**: *"All claimed
values are cleared… it names which document to go and get, never what it says."* The marker did
not cure it — the ruling is about the table holding contents at all, not about confidence in them.

The blocking `test_db_integrity` L02 check caught it (109 YAML records vs 121 table rows), because
the write had no YAML mirror. `data_20260821185514` retracts the 12 rows and re-files their content
as leads, which is where D-1 places it anyway.

**Two lessons worth keeping.** A table that has been *emptied by ruling* looks identical to a table
that is *empty for want of data* — nothing in the schema distinguishes them, and the only record of
the ruling was a comment in a YAML header. And an `[UNVERIFIED-QUANT]` marker is not a licence to
write somewhere writing is forbidden.

## Vocabulary drift caught before it landed

The first draft used jurisdiction codes `AU-NZ`, `DK-NO-SE-FI` and `INT`. None is in this table's
established set (`AU CA CH DE EU FR GB ISO JP NO SG US`) and **every validator passed anyway**,
because — per D-4 — there is no `jurisdictions` table to validate against. The composites and the
non-jurisdiction were re-filed as leads; the remaining codes are ISO country codes consistent with
the existing scheme.

## What this does not do

No determination. No admission. No `evidence_sources` row. Every lead is `PENDING-VERIFICATION`
and every quantified figure carries `[UNVERIFIED-QUANT]`. The 11 orphans still cannot be admitted
while R9 is blind to `source_locators` — **OD-5 remains the blocker**, and it now blocks a
demonstrably larger body of work than when it was raised.

## Next

1. **OD-5.** It gates re-admission of the 11 orphans, which gates `reasoning_doc_citations`, which
   gates D-2.
2. **Read this document before the next search round.** The corrected-frame search proposed by the
   adversarial adjudication should be designed against what is already here, not from scratch.
3. **Create `jurisdictions` and `languages`** (D-4) before any further code-value work.
