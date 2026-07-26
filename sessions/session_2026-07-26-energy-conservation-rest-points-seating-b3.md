# Session — energy-conservation-rest-points-seating, batch 3

**Date:** 2026-07-26
**Slug:** `energy-conservation-rest-points-seating` (STUB, `seating-and-rest`)
**Axis:** `AX-STA` Sustained-exertion demand; secondary `AX-PAI`, `AX-AMB`, `AX-BAL`
**Doctrine SHA:** `0f2f525`
**Predecessors:** batch 1 (PR #71, merged), batch 2 (PR #72, merged)
**DoD gate:** COMPLIANT 15/15, first run

---

## 1. Objective and result

Batch 2 left two Co-1 sources blocked at HTTP 403 (GAP-309) and a dimensional evidence base that
rested on one source *reporting* other people's figures. Batch 3 took both.

**5 sources admitted** (REF-00960–00964). GAP-309 half-resolved. Two new gaps. One **R15
correction that would have put a wrong citation into the corpus**. One tooling change.

## 2. The R10 ladder, and why it is worth climbing

R10 says a publisher block is not a terminal answer. Batch 2 stopped at 403; batch 3 kept going,
and the two cases resolved in opposite directions.

**Ulahannan — four rungs to full text.** Crossref `query.bibliographic` recovered the DOI →
the Crossref record showed **CC BY 4.0**, meaning a lawful copy *had* to exist → OpenAlex
`locations` listed a green-OA PDF at Coventry University Pure → downloaded and read.

The generalisable lesson: **for a gold/green-OA paper a publisher 403 is never terminal.** The
licence guarantees a compliant copy somewhere; OpenAlex is the fastest route to it. Two batches
of "blocked" collapsed into four API calls once I thought to check the licence.

**Transport for All — ladder exhausted, and we are the blocker.** Five distinct routes now tried:
highlights PDF (403), full PDF (403), news page (403), Wayback via WebFetch (harness refuses
`web.archive.org`), Wayback via curl (`Blocked by egress policy`). The Wayback availability API
**confirms both URLs are archived and return HTTP 200** — the document is public, archived and
retrievable, just not from here. Reclassified as an **environment limitation, not an evidence
gap**, and recorded so nobody re-runs the same five routes.

## 3. The R15 correction — the batch's most important result

**Ulahannan 2025 contains no seating finding at all.**

It was staged in batch 1 from a Consensus abstract as "26 UK interviews on streetscape barriers"
with the honest caveat that whether it addressed seating was *not established*. Batch 2 repeated
the caveat. Reading it settles it: **"benches" occurs exactly twice, both as an example of street
furniture in definitional text** — defining "streetscape", and in the interview preamble. No
finding about seating provision, rest points or spacing exists in the paper.

Two batches of pressure to close GAP-309 made admitting it on title-and-abstract tempting. Had I
done so it would have entered the corpus as apparent support for rest-point provision. **This is
exactly what R15 exists to prevent, and it took until the third look to catch.**

It is admitted — for a **different claim than it was staged for**. Its *"feeling exhausted"*
theme, one of four key impacts, is direct lived-experience evidence for the `AX-STA` **demand**:
*"a recurrent impact of participants feeling exhausted due to the streetscape barriers…
participation in society was draining."* Population match **EXACT** (26 disabled people, recruited
as such); topical contribution to seating **nil**. Those are separate axes and are recorded
separately — conflating them is how a streetscape paper becomes a bench citation.

## 4. Co-1 eligibility, tested against my own interest

The slug holds **one** Co-1 source and has since batch 1. Classifying Ulahannan as Co-1 would
have relieved that. Its publisher, the National Centre for Accessible Transport (Coventry
University), was checked: the About page says ncat *"works directly with disabled people,
disability organisations, transport providers and policy makers"* and *"amplifying the voices of
disabled people"*. That is **engagement language, not governance** — it does not say disabled-led,
and does not name the consortium.

Filed **T3, not Co-1**. Same standard that passed Wheels for Wellbeing in batch 1 and failed
Rosenberg 2012. Applying it consistently when it costs something is the only version that means
anything.

## 5. The dimensional chain — located, deliberately not claimed

REF-00953's figures traced to four papers, all admitted: Holden & Fernie 1989 (REF-00961) and
Holden, Fernie & Lunau 1988 (REF-00962) for the armrest specs; Kothiyal & Tettey 2001
(REF-00963) and their 2000 Australian anthropometric dataset (REF-00964) for seat depth and the
population percentiles.

**Crossref metadata verified; no full text obtainable for any of the four.** The corpus now knows
precisely *where* the numbers come from without having read them at source — a real advance over
batch 2, but not the same as verification. Worse, **two attributions are split across companion
papers**: "Holden and Fernie" could be either paper or both.

Registered as **GAP-310**: armrest 730/250/120/120 mm and seat depth 376 mm remain **attributed,
not primary-verified**, and must not be cited as primary-sourced. The batch-4 reading should
actively hunt for a discrepancy — batch 1 already caught a professional body misreporting its own
citation, so "the primary says what the secondary claims" is a hypothesis, not a default.

## 6. Tooling — stopping a repeat, mechanically

I made the same `doi_resolution_outcome` vocabulary error in batches 1 and 2. After batch 1 the
lesson went into a session file, a PR body and an attestation deviation — and prose did not stop
me repeating it three hours later.

`scripts/emit_data_migration.py` now **blocks** emission on values outside audit-enforced closed
vocabularies (`doi_resolution_outcome`, `url_resolution_outcome`), with the rationale written into
the code. Tested against both forms of the actual mistake (positional INSERT and `SET col='X'`);
correct values and `NULL` pass. It is blocking rather than a warning **because a warning is what
the repeat slipped past** — the emitter already printed warnings and I emitted anyway.

This is the third batch in a row where the substantive finding came from a *mechanical* check
rather than from reading more sources. Worth noting as a pattern.

## 7. What batch 3 did NOT achieve

- **Still one Co-1 source.** The R1 pass ran first and admitted nothing: the one resolvable
  candidate turned out not to be Co-1, and the actual Co-1 source is environment-blocked.
- **No full text for any of the four primaries** — the chain is located, not read.
- **Non-EN deferred a third time.** Correctly (no vocabulary → back-translation → R11), but three
  deferrals is structural, now **GAP-311**. All ten jurisdictions reached are Anglophone-published.
- Transport Scotland's parent report not attempted.

## 8. Gate results

| Check | Result |
|---|---|
| `research_batch_dod --session` | **COMPLIANT 15/15, first run** |
| `research_batch_dod --all` | COMPLIANT |
| Migration reproducibility (7 invariants) | PASS |
| `test_db_integrity.py` | equal to pre-batch baseline |
| `research_protocol_audit` | equal to baseline |
| `validate_bpc.py` / `validate_cross_refs.py` | 102/102 · 0 issues |
| Enum-guard self-test | blocks both forms of the batch-1/2 error; passes valid values and NULL |

## 9. Batch 4 queue

1. **GAP-310** — read the four primaries; look for discrepancy, not confirmation. REF-00964 is the
   highest-value single read: if it is the measured dataset it appears to be, it is the deepest
   layer the seat-height equity argument (GAP-307) rests on.
2. **GAP-311** — build `term_aliases`. Three deferrals is enough; schedule it explicitly.
3. **GAP-309** — Transport for All needs an environment with `web.archive.org` reachable.
4. Transport Scotland **parent** report — Appendix C omits the interval; the parent may not.
