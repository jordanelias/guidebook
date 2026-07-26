# Session — energy-conservation-rest-points-seating, adversarial pass

**Date:** 2026-07-26
**Doctrine SHA:** `0f2f525`
**Prompted by:** owner — *"adversarial pass. you should be reading your sources btw."*
**Sources admitted:** 0 · **Errors found in my own batches 1–3:** 7
**DoD:** R1–R6, R8–R15 PASS; **R7 waived with reason** (§5)

---

## 1. The instruction was a correction, and it was right

Batch 3 admitted four primary sources on Crossref metadata alone, without reading them. I noticed
that was weak — I wrote it into the attestation as a deviation and into the PR body as something a
reviewer should question. Then I shipped it anyway.

**Logging a deviation is not a substitute for doing the work.** A disclosure is appropriate when a
limit is unavoidable; here it wasn't. All four papers were indexed in PubMed the whole time, with
abstracts carrying exactly the method detail I needed. The cost of reading them was three tool
calls.

## 2. Seven findings, all in my own record

**A1 — batch-2 prose overclaimed what had been read.** It said *"Six further sources were read…
Not one states a spacing figure."* Only REF-00953 was read in full text and REF-00954 fetched.
REF-00955–00959 were **abstract-only**, exactly as their own `verified_by_tool` fields record. The
structured data never lied; the narrative did. And the false claim is the *negative* one — an
abstract omitting a spacing figure doesn't establish the paper contains none.

**A2 — the same dataset admitted twice.** REF-00963 and REF-00964 are both Kothiyal & Tettey,
n=171, aged 65+, metropolitan Sydney: one study reported as a short data note (*Appl Ergon* 2000)
and a fuller treatment (*IJOSE* 2001). Batch 3 counted them as two sources.

**A3 — the 376 mm seat depth is circular.** REF-00953: *"Jean has a buttock to popliteal length of
376 mm… Kothiyal and Tettey recommend 376 mm… exactly right for Jean."* Both halves come from that
one dataset. It's one number twice, so "exactly right" is a tautology. **This is the batch-1
double-count error — which I caught in someone else's work — committed in mine.**

**A4 — REF-00961 under-tiered.** Adjustable seating rig, elderly inpatients, four iterated chair
shapes, outcome evaluation: intervention-level control on the parameter under design, i.e. a
genuine **T1 candidate** filed at T3. Deliberately **not promoted** — re-tiering upward on an
abstract is the inflation risk this pass exists to check.

**A5 — REF-00962 over-tiered.** No study, no participants, a discussion of requirements. Now
**grey-flagged** → weak band. Batch 3 filed it identically to A4's experiment, having read neither.

**A6 — my batch-3 R14 diagnosis was wrong.** I recorded that PubMed "thinly indexes late-1980s
ergonomics — a wrong-index result." All four were indexed, and the one record my query returned
**was one of my two targets**; I never checked the returned PMID against what I was hunting, then
blamed the index. R14 exists precisely to stop this: a wrong failure-diagnosis teaches the next
session to distrust a database that was working.

**A7 (GAP-312) — the equity harm's scope was never stated.** GAP-307 generalises from 171 Sydney
residents measured ~25 years ago, and the DVT/musculoskeletal consequence is REF-00953's inference
in its Discussion, not a measured outcome. The claim may well hold — direction of effect and
secular height trends both favour it — but batches 2–3 asserted it without any of that.

## 3. The generalisable one

A1 and A6 are one failure in two costumes: **a claim pitched at a confidence the retrieval didn't
support, with nothing to catch it.** The DoD gate checks that population grades exist, that empties
carry reasons, that mining rows are present. **Nothing compares a claim about source *content*
against the retrieval depth recorded on the rows it cites.** Registered as **GAP-313**.

That is the third consecutive batch where the substantive finding came from a mechanical check
rather than from more searching — and this time the check was a human telling me to read.

## 4. Access findings

Three of four primaries are **closed access**, no repository copy. The fourth is **bronze OA** —
free at publisher — and tandfonline still 403s here. Worth separating from batch 3's Ulahannan
rescue, which worked because that paper was **gold OA under CC BY with a repository copy**. Bronze
OA offers no fallback. **The OpenAlex route is licence-dependent, not general** — batch 3's write-up
implied otherwise.

## 5. R7 waiver — reasoned, not remediated

R7 expects ≥1 `search_candidates` row per screened batch. This pass screened seven records that
were **all already-admitted sources**; no off-slug or unverified material surfaced, so there is
nothing to stage. Creating a candidate row to move the counter is exactly the one-row gaming
`5a59aaf` hardened the gate against.

**Waived deliberately.** R1 and R4 were remediated in substance instead: R1 via the gate's in-band
`CO1-NOT-APPLICABLE` mechanism (a verification pass admits nothing, so no admission exists for a
Co-1 pass to precede), R4 via a genuinely new linkage (EPM-00953-B) recording the population
GAP-307 actually rests on.

## 6. What did NOT change

No source was removed, no tier promoted, no finding of batches 1–3 reversed. The substantive
positions hold: the need is evidenced and replicated; the 50 m interval has no located primary
basis; single-height seating excludes short users. What changed is **how strongly several of them
may be stated, and on whose bodies one of them rests.**

## 7. Queue

1. **GAP-310** — armrest dimensions still need the 1989 full text (closed access; try ILL or an
   institutional route).
2. **GAP-313** — consider a mechanical check for prose-vs-retrieval-depth drift.
3. **GAP-311** — `term_aliases`; four deferrals now.
4. **GAP-309** — Transport for All needs an environment reaching `web.archive.org`.
5. Open question for the owner, unchanged: is the **Co-1 definition** drawn too tightly? (ncat
   fails it; Wheels for Wellbeing passes.) DG-NON territory — proposed, not decided.
