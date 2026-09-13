# Batch 07 — priors, written BEFORE any query ran (R8)

Session: `session_2026-09-13-research-batch-07-corridor-width`
Cell: parameter 2 (`TERM-002 corridor width`) × identity lens `MOB`, slug
`accessible-circulation-geometry`.

**R8 is why this file exists.** A prior recorded after seeing results is a rationalisation, not a
prior (DR-2026-05-09). Each entry below is written now, before its query is executed. The
`--prior-expectation` passed to `db.py log-search` is copied from here verbatim, not re-composed
after the fact.

**R1 orders the pass:** Co-1 / T2 / Co-2 go FIRST, no exceptions (Co-1 is co-primary with T1 under
CRPD Art 4.3). Queries are numbered in execution order and the Co-1/Co-2/T2 leg is 1–3.

---

## Q1 — Co-1, lived experience / co-produced work on corridor width
Engine: pubmed · language EN · target tier 1 · target evidence type co1

PRIOR: Near-zero yield expected in PubMed specifically. Co-1 warrant is co-production, and
co-produced disability research on building dimensions is published in design, housing and DPO
grey venues rather than in a biomedical index. I expect 0–2 hits and expect that any hit will be
participants *tested* rather than co-producing, which does not meet the Co-1 warrant. If the yield
is 0 I must show by control query that the emptiness is about the venue, not the query shape (R14).

## Q2 — Co-2, OT professional-body guidance on passage/corridor width
Engine: web · language EN · target tier 2 · target evidence type co2

PRIOR: I expect professional-body material to exist (home-modification and access guidance is core
OT territory) but to cite regulatory dimensions rather than to measure them. So I expect a source
that is real and relevant but whose corridor-width figures are inherited from codes — which would
make it a regulatory-stratum echo, not an independent measurement. Expect 0–1 admissions.

## Q3 — T2, synthesis / systematic review on wheeled-mobility space requirements
Engine: pubmed · language EN · target tier 2 · target evidence type sr_meta

PRIOR: I expect 1–3 reviews on wheeled mobility space and manoeuvring requirements, most likely
anthropometric or ergonomic in framing. I expect at least one to be about turning space rather than
straight-corridor width, which would be off-parameter for this cell and belongs in
search_candidates as REHOME rather than admitted.

---

## Q4 — T1, anthropometric / biomechanical measurement of minimum passage width
Engine: pubmed · language EN · target tier 1 · target evidence type clinical

PRIOR: The corpus already holds REF-00784 (Koontz 2010), which measured exactly this. I expect this
query to re-surface it — a duplicate, which R9 says must be cross-filed rather than re-admitted, not
counted as a new find. Beyond it I expect 1–4 further studies, skewed toward wheelchair
anthropometry and occupied-footprint work.

## Q5 — T1, forward/backward mining on the admitted corridor-geometry anchors
Engine: crossref/pubmed · direction backward and forward (R2)

PRIOR: REF-00784, REF-00971 and REF-00972 are the corpus's corridor-geometry anchors. I expect
backward mining to surface the ANSI/ISO wheeled-mobility anthropometry literature and the
IDeA Center / Steinfeld work, and forward mining to surface citations in accessibility-standards
revision papers. I expect more yield backward than forward, because the anchors are 2010–2011 and
the field is small.

---

## What would make me wrong, recorded now so it is falsifiable

- If Q1 returns a genuinely co-produced corridor-width study, my "wrong venue" prior is wrong and
  Co-1 is reachable in PubMed for this parameter.
- If Q4 returns many high-control studies, my belief that this literature is thin and
  device-centred is wrong.
- If Q3's reviews state corridor widths directly rather than citing codes, then T2 can anchor this
  cell and my expectation that the cell rests on T1/T3 primary work is wrong.
