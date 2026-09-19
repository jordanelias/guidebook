# Research batch 18 — the archive route, and what 1:12 was measured to be

**Session:** `session_2026-09-18-research-batch-18-archive-route-ramp-threshold`
**Slug:** `accessible-circulation-geometry` · **Parameter:** 3 (`ramp gradient`, TERM-001) × MOB
**Priors committed before the first query:** `4f053bc` (batch) and `9cf59e3` (per-query),
`scratchpad/<session>/priors.md` and `query-priors.md`
**Assignment:** GAP-028 taken together with GAP-016, as GAP-028's closing condition directs, and as
batch 17 handed forward: *"the next batch should plan that as a different kind of work rather than
re-run the same seven routes and record a second null."*

Derive every figure below. The commands sit beside the claims in the search log and the gaps.

---

## 1. The headline

**The 1:12 ramp gradient was measured before it was adopted, and the measurement found it
inadequate for close to half of the wheelchair users tested.**

REF-01005 — Steinfeld, Schroeder and Bishop, *Accessible buildings for people with walking and
reaching limitations*, HUD-PDR 397, 1979, ERIC `ED184280` — was retrieved in full (170 pp,
5,702,293 bytes, sha256 `5dd866a2…`), persisted, and read. Its ramp study:

- A purpose-built 40-foot ramp, adjustable slope, handrails both sides, 48-inch clear width.
- 124 disabled participants in phase 1. Slope stepped **1:12 → 1:16 → 1:20**, each step taken only
  by those who failed the one before.
- Success judged on distance, time, and **pulse recovery to within ten beats of resting**.
- **At 1:12, almost half the wheelchair users could not negotiate the full length; about a third
  could not travel even 5 feet. At 1:20, every wheelchair user completed the full 40 feet.**
- Its "Marginal Population" section: people with limitations of stamina, hemiplegics and
  quadriplegics *"all may have difficulty with ramps steeper than 1:20."*

**And the report was commissioned to improve the standard that carries 1:12.** Its own Foreword
says the six-report series was sponsored *"to accomplish the important task of making buildings
accessible to and usable by the physically handicapped through improving the American National
Standards Institute's A117 standard."*

That answers GAP-028's question — *is 1:12 anchored in measurement?* — with: **yes, and the
measurement did not support it.** Filed as **GAP-037**.

## 2. What this batch does NOT do, stated before anything else it does

**Parameter 3 × MOB is still undetermined. Determination gate 1 is still open. C10 still refuses.**

REF-01005 is admitted at **T3 grey**, by the **owner ruling of 2026-09-18** — *"I don't think 1979
work is great for today standards but it's great for historical grounding"* — recorded on contact
per rule 0 in `references/project-standards.md`.

**The ruling overrode my own reading, and that is worth stating plainly.** Read mechanically against
`governance/tier-system.md` §1, the study is a candidate for `clinical`/`high_control` → **T1**: the
parameter under design was experimentally manipulated, the outcome was physiological, n = 124. I was
about to take that reading. The ruling refuses it on **currency**, not on design quality — a
determination states what to build *now*, and 1979 measurements were taken on 1979 wheelchairs by
people trained in 1979 practice. The design facts are recorded on the row so the T3 is legible as a
ruling rather than as anyone's misreading.

**My pre-registered prior P3 predicted exactly this and it HELD**: *"I expect batch 18 to produce no
new anchoring-tier stated threshold that C10 would accept, at p ~ 0.65 … pre-1990
rehabilitation-engineering reports are T3 grey primary at best, not the T1/T2/Co-1 band the
determination needs."* The batch's falsification condition — that C10 accept a re-determination —
was **not** met, and I am recording that the prior survived rather than quietly dropping it.

## 3. The provenance chain, from bytes

REF-01005 page 163, §5 Ramps, is the load-bearing passage:

> *"Walter's findings for ramps are similar to ours. Both studies found a 1:16 slope for 20 feet to
> be accessible to at least 95 percent of the wheelchair users. Elmer (1957) found that a 1:8 ramp
> slope was maximum for wheelchair users. However, his sample was taken from wheelchair users at a
> pioneering rehabilitation-education center and the findings probably reflect the high standard of
> excellence in rehabilitation training that the subjects received as part of their program."*

And Table 13's footnote c: *"Based on research of others (Templer, 1977 and Walter, 1971)."*

So the chain has **three nodes and this project holds one**:

| Node | State after this batch |
|---|---|
| Elmer 1957 — found 1:8 max | Not retrieved. **Characterised by a primary source** rather than by a reference list, and dismissed there as an elite-trained sample. Candidate 110, re-described. |
| Walter / Disabled Living Foundation 1971 — 1:16 over 20 ft for ≥95% | **Record verified** (Open Library OL4653562M, 60 pp, London, *"studies directed by Felix Walter"*). Not retrieved. Candidate 109, re-described. |
| Steinfeld 1979 | **Held in full.** REF-01005. |
| Templer 1977 — named as a Table 13 warrant | **Newly staged**, candidate 115. |

**The Walter/Steinfeld convergence at 1:16 is currently ONE document counted once, not two.** It
rests on Steinfeld's testimony about Walter; Walter itself is unretrieved. Recording it as two
independent findings would be adversarial lens L3, and the extraction note says so.

## 4. Two errors of mine, both caught by gates, both recorded rather than smoothed

**(a) R5 — I used absence-of-DOI as a quality signal.** I logged the Dutch van der Voordt search as
`target_evidence_type='grey'` because the item has no DOI. That is the exact inference R5 exists to
forbid: non-indexation is an indexing fact, not an evidence-quality fact. **It is this batch's own
thesis turned against it** — I argued that DOI-keyed search structurally hides the pre-1990 layer
and then treated a missing DOI as weakness in the same breath. Corrected to `clinical`, with the
replaced value logged.

**(b) C04 — a completeness claim resting on a lookup nobody ran.** REF-01005 landed stamped
`metadata_quality='COMPLETE'` with no DOI, no Co-1 verification and **no recorded NO-MATCH**. The
blocking check caught it. I then actually queried Crossref — five unrelated items, no deposit — and
recorded `doi_resolution_outcome='NO-MATCH'` as **verified rather than assumed**.

**(c) I recorded an unfired query as a null — one batch after reading the record of the same
error.** Three Google Books queries returned **HTTP 429, daily quota exceeded**. They were never
asked. I wrote *"Google Books 0"* into the re-descriptions of candidates 109 and 110, which went
into a committed, immutable migration. **Batch 17 made the identical error on SafetyLit** — its
§9.4 retracts *"503 then empty"* — and I read that section while orienting, hours before repeating
its shape. Corrected: the queries are logged as an unfired instrument, both candidates carry
retractions, and **GAP-040** files the structural point, which is that nothing mechanises the
comparison between a zero-yield claim and the manifest status behind it.

**(d) I misread a 403 as a 200, and it made my finding sound worse than it was.** I wrote that
HathiTrust *"returned HTTP 200 carrying a Cloudflare interstitial — a false 200, the same shape
batch 17 found on JSTOR."* **The persisted status is 403.** A 403 is an honest refusal; a 200
carrying an interstitial is a *deceptive* success, which is the whole reason the JSTOR case was
worth recording. **I upgraded a mundane block into the more alarming class and reached for a
precedent that did not apply.** Corrected in the search log, in the owner-ruling record, and here.

**Both (c) and (d) were found by `author_fidelity`**, an advisory check that prints every non-2xx
in a session's manifest — i.e. by a check that reads what the session *retrieved* rather than what
it *said*. Neither was found by me re-reading my own work.

**A near-miss, not caught by any gate:** a web-search summary asserted Elmer 1957 was a
"University of Iowa Master's thesis" and **not one of its own returned links supported that**. It is
discarded, not recorded. REF-01005 says only *"a pioneering rehabilitation-education center"*, and
naming one would be invention — CLAUDE.md §5(c) in its natural habitat.

## 5. Machinery repaired, with the class each fix closes

| Fix | Class it closes |
|---|---|
| `add-source` gains `--source-type`, `--institution`, `--report-number`, `--series`, `--series-number`, `--publisher`, `--publisher-location`, `--book-title`, `--grey-flag`, `--grey-reason` | **The seventh capture-path blindness.** Every field that makes a REPORT citable was unreachable; REF-01005 landed with nine payload-supplied fields NULL under `COMPLETE`. GAP-038. |
| `--verbatim-exempt` threaded through to `_write_relation_edge` | **GAP-007, and the live defect was worse than the gap said.** `add-extraction` accepted the flag and never passed it on, so the refusal instructed the reader to use a flag that could not reach it. It bites exactly where evidence is oldest: `quote_in_artefacts` cannot decode a scanned PDF, so no microfiche-era quote can ever match. GAP-039. |
| `amend-search --set-target-evidence-type` | A misclassification the gate READS could only be answered by prose the gate does not read. Scoped to the one column that classifies intent rather than records history. |
| `governance/check-registry.yaml` batteries note | Prose caller asserting PDFs "route through --verbatim-exempt" — true of `--claim-text`, false of `--quote`, until this batch. Rule 7a's third shape. |

## 6. The instruments, and what they are worth

**ERIC is the finding, and the owner ruled it worth remembering** (recorded 2026-09-18). The pair
`api.ies.ed.gov/eric/?search=…` → `files.eric.ed.gov/fulltext/<ED-number>.pdf` reached in one step a
report that six batches of DOI-keyed searching never saw.

**But its precision is one-sided, and the same batch establishes both halves.** A *named-report*
lookup hit. A *topical* lookup for "wheelchair ramps" returned one off-slug school programme — ERIC
is an EDUCATION index and held this report because it was deposited there, not because it covers
built-environment research.

**`catalog.hathitrust.org` is known-bad for this purpose**: a Cloudflare *"Just a moment…"*
interstitial instead of results, persisted as evidence. **Nothing is concluded about what
HathiTrust holds.**

**Google Books is EXHAUSTED IN THIS ENVIRONMENT, not empty** — HTTP 429, daily quota. See §4(c).

**Untried and owed:** NTIS, and Jisc Library Hub Discover — which is where Walter 1971 would sit.

## 7. GAP-016 / REF-01002 — a predicted null, fired twice and stopped

P4 put archive-route failure at p ~ 0.8 and **pre-committed to two routes, then stopping**, so that
a second null would be scored as a prediction rather than banked as effort. ERIC: 0. Internet Archive
on the journal name: 0. **Two fired, stopped, GAP-016 and GAP-026 unmoved.** Batch 17 named what
would actually work and it remains true: a library or document-delivery route, which is not a search.

## 8. Gates

- `research_batch_dod --session` — **COMPLIANT, all 19 rules.** R1 and R5 failed first and were
  remediated by a real Co-1 pass and a real correction, not by waiver.
- `test_db_integrity` — **75/75**, after C04 was fixed. 21 checks passed having examined nothing,
  named in its own output; the denominator is what it is and is not banked as breadth.
- `run_checks.py --changed-from origin/main` — **PASS**. Re-derive the counts; they moved twice
  during this batch and a literal here would be wrong by the time it is read.
- `author_fidelity` — **INDETERMINATE, and it is the most useful result of the batch.** It caught
  two misrepresented retrievals (§4c, §4d). It reports INDETERMINATE rather than PASS because 12
  older sources have no logged retrieval at all and are not verifiable offline — a corpus-wide
  condition this batch neither caused nor fixed.
- `run_checks.py --selftest` — **PASS.**
- Derived outputs regenerated and `--check`-clean; context map regenerated.

## 9. What the next batch takes

1. **Mine REF-01005 backward.** Deferred depth-1 and **assigned**, not left to age. Its reference
   list is the index to the whole pre-1990 layer. **No Crossref deposit exists**, so the pass runs
   against the PDF bibliography (page indices 167+, OCR damaged), not an API — and any yield must
   name a screen from `governance/mining-screens.yaml`.
2. **Walter 1971** via Jisc Library Hub Discover. It is the one retrieval that would turn the 1:16
   convergence from one document into two.
3. **Templer 1977** (candidate 115) via ERIC, NTIS, TRID. Which Templer is load-bearing is
   **unresolved and must not be guessed**.
4. GAP-016 stays open and is **not a search**.

**Not attempted, and owed:** GAP-033 (term adjudication has never run — `term_adjudications` is
empty while `observed_terms` is not, and this batch added four more to the unadjudicated pile).
