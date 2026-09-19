# Batch 18 priors — recorded BEFORE the first query (R8, DR-2026-05-09)

**Session:** `session_2026-09-18-research-batch-18-archive-route-ramp-threshold`
**Slug:** `accessible-circulation-geometry` · **Parameter:** 3 (`ramp gradient`, TERM-001) x MOB
**Assignment:** GAP-028 taken together with GAP-016, as GAP-028's own closing condition directs
("a library or archive route, the same non-search work GAP-016 now needs, and the two should be
planned together"), and as batch 17 handed forward ("the next batch should plan that as a
different kind of work rather than re-run the same seven routes and record a second null").

## The question

**Is the 1:12 ramp gradient anchored in measurement, and where?**

Under the owner ruling of 2026-09-13, a finding that a code is insufficient supplies no value and
is still first-class evidence. So both answers are results, and I am committing to that symmetry
here rather than after seeing which one I get.

## Why this is a different instrument, not the same search again

Derive the claim, do not trust it:

    python3 - <<'PY'
    import sqlite3
    con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
    for r in con.execute("select engine, count(*) from search_executions "
                         "where slug='accessible-circulation-geometry' group by 1 order by 2 desc"):
        print(r)
    PY

Every engine on this slug to date is a citation index or a general web search. GAP-028's finding is
that the pre-1990 layer is *structurally* invisible to those: no DOI, no PubMed record, no Crossref
deposit. Batch 18 fires full-text archives and rehabilitation-literature indexes instead. Routes
never attempted on this slug: HathiTrust, Internet Archive / Open Library, ERIC, NARIC REHABDATA,
Google Books, and TRID used as a *search* surface rather than as a single record lookup.

## Named targets, from REF-00980's deposited reference list (GAP-028)

1. A 1957 study determining the specifications of wheelchair ramps.
2. A 1971 architectural movement study whose Part 3 is titled "Ramp gradients".
3. A 1979 accessible-buildings study.
4. A 1981 Dutch paper on accessibility by means of ramps.
5. A 1993 review of technical requirements for ramps, written as an RFP attachment.

## PRIOR EXPECTATIONS — committed, falsifiable, one per claim

**P1. Retrieval.** I expect **at least one** of the five named pre-1990 items to be locatable to a
bibliographic record (author, year, venue) through an archive route, at **p ~ 0.7**. I expect
**full text** for at least one at **p ~ 0.4** — lower, because these are institutional reports and
proceedings, and because batch 17 has already demonstrated this environment's retrieval ceiling.

**P2. The anchoring claim — this is the sharp one.** GAP-028 hypothesises the 1957/1971 work is
the measurement behind 1:12. I expect this to be **only partly true**, at **p ~ 0.6**: that the
empirical work exists and is real, but that the specific figure 1:12 entered the codes through a
*standards committee* rather than directly from a stated experimental result. Falsified if a
retrieved source states 1:12 (or 8.33%) as its own measured recommendation.

**P3. Yield for the determination.** I expect batch 18 to produce **no new anchoring-tier stated
threshold that C10 would accept**, at **p ~ 0.65**. Pre-1990 rehabilitation-engineering reports
are T3 grey primary at best under `governance/tier-system.md`, not the T1/T2/Co-1 band the
determination needs. **So I expect the determination to stay blocked, and I am saying so before
I search rather than after.** If that holds, the honest output of this batch is a provenance
finding about the code, not a determination.

**P4. REF-01002.** I expect the archive route to fail on it too, at **p ~ 0.8**. JAPR 26(2) 2009
is a paywalled journal issue with no deposit; archives index older and greyer material, not
recent commercial journals. **I am recording this so that a second null on REF-01002 is scored as
a predicted result and not dressed up as new work.** I will fire at most two REF-01002 routes,
both previously unattempted, and stop.

## Anti-rationalisation clauses

- **A yield is derived from a named, versioned screen** (owner rule, 2026-09-18 22:55). Any count
  of relevance in this batch cites a screen from `governance/mining-screens.yaml` by name and
  version, via `scripts/research/mining_screen.py`. No inline regex.
- **A retraction is held to the standard of the claim it retracts** (owner rule, same date). If I
  withdraw anything in this batch I re-derive the whole comparison, not the challenged part.
- **A staged candidate description is a HYPOTHESIS** (R15). Every candidate gets re-described from
  the source on resolution, and corrected if I over-claimed.
- **Zero-yield searches are kept** (R8/R14), with the query-shape / wrong-index / genuine-absence
  diagnosis stated for each.
- **Named dissenter.** The strongest case against this batch: the five named items are known only
  through *one* deposited reference list (REF-00980's), so their titles as I hold them are
  second-hand. If an archive record contradicts the title or year I am searching on, the reference
  list is the thing that was wrong, and I correct my target rather than my result.

**Falsification condition for the batch as a whole:** if I admit a source whose stated threshold
sits at an anchoring tier and C10 then accepts a re-determination of parameter 3 x MOB, P3 is
falsified and I say so in the session record in those words.
