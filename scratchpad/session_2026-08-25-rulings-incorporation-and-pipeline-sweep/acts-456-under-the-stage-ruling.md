# Acts 4, 5 and 6 interrogated under the stage ruling

**Owner ruling 2026-08-25:** `research → evidence collection → judgment → synthesis → render`,
plus §2.1 pointer discipline (never write the same fact into a second table) and §2.2 (each
stage's tables hold only that stage's data; anything earlier is reached by pointer).

Every figure below measured against `main` at `ce33ef6`. Commands in the session command log.

---

## THE FINDING THAT REFRAMES ALL THREE: a cross-stage VIEW *is* the pointer

Measured span of all 18 views. Four cross a stage boundary:

| View | Rows | Spans |
|---|---|---|
| `v_source_admission` | 10 | evidence-collection ← **research** |
| `v_item_provenance` | 0 | evidence-collection ← **judgment** |
| `v_source_reach_all` | 10 | evidence-collection ← **judgment** |
| `v_divergence` | 0 | judgment ← **synthesis** |

**A view that joins two stages on the shared reference ID is the owner's ruling implemented in
SQL.** *"You can call up information from any one so long as you point to the correct table and
column"* — that is a join. *"For rendering a citation, we point towards the evidence table for
that reference ID"* — that is `v_item_provenance`, exactly.

**So Act 6 is not merely wrong on empty-vs-dead grounds. It is DOCTRINALLY BACKWARDS.** The four
cross-stage views are the most doctrinally load-bearing objects in the schema, not the most
disposable. Dropping them removes the pointer infrastructure the ruling requires and forces the
next reader back to copying — which is the defect the whole PD series exists to remove.

`v_source_admission` is the sharpest case: PD-6's plan is to NULL
`evidence_sources.search_queries_used` *after redirecting readers to
`v_source_admission.query_text`*. Measured: that column holds **10 of 10 populated** — a RESEARCH
fact (the query) sitting on an EVIDENCE row, the exact §2.2 violation. The view is the pointer
that fixes it. **Dropping the view would destroy the remedy and leave the violation.**

---

## ACT 4 — the jobs are STAGE-PURE. The collision is bookkeeping, not doctrine.

Measured, every column the two jobs write to `evidence_sources`:

    resolve_dois.py   doi, doi_resolution_outcome, pmcid, metadata_quality,
                      verification_status, verification_method, verification_disposition,
                      verification_note, author_count_is_complete
    verify_urls.py    url_resolution_outcome, url_match_similarity,
                      verification_disposition, verification_method, verification_note

**Every one is evidence-collection content** — the ruling's own words for that stage are *"what
was admitted, its identity, VERIFICATION and extraction."* The jobs write evidence-collection
facts into evidence-collection tables. **No stage boundary is crossed and no fact is duplicated.**

*Correction to my earlier sweep summary: I reported `resolve_dois.py` INSERTing into
`source_locators`. It does not — `grep -n source_locators scripts/resolve_dois.py` returns
nothing. Had that been true it WOULD have been a cross-stage write (research clue store written
by an evidence-collection job) and Act 4 would carry a doctrinal charge as well as a gate one. It
does not.*

**What this changes about the owner's decision.** The choice is NOT "which option respects the
stage ruling" — both do. It is narrower and cheaper than I framed it:

- **Option (i), widen the exemption.** Defensible under the ruling: these are stage-pure writes by
  the stage's own authoritative writer, which is what DR-2026-05-28 already decided.
- **Option (ii), jobs emit migrations.** Buys nothing doctrinally. It changes the write MECHANISM,
  not the stage content, and adds bot-authored migration files to the append-only ledger forever.

**One genuine wrinkle worth the owner's attention.** `pipeline_runs` and `url_verification_runs`
are run ledgers — facts about the JOB, not about any source. Under the ruling they are not
evidence-collection content at all; they are infrastructure, the same class as `data_migrations`,
which the map already lists under substrate. If they were named as such, their exemption would
need no special pleading: **substrate ledgers are not stage data and were never subject to the
crossing rule.** That is a cleaner basis for (i) than "these two tables are special."

---

## ACT 5 — the stage ruling makes this a BETTER act than the one planned

Planned scope: migrate ~50 readers to `dbcore.connect`. That is hygiene. Under the ruling the
valuable question is different and sharper:

> **Does each reader cross a stage boundary by POINTER, or by reading a COPY?**

A reader that joins on `ref_id` (or through a cross-stage view) is compliant. A reader that reads
a stage-foreign column off a row — `evidence_sources.search_queries_used` rather than
`v_source_admission.query_text` — is consuming a copy and keeps that copy alive.

**Act 5 should therefore be re-scoped**: the sweep's unit of work is not "does this file import
dbcore" but "does this file reach across a stage by pointer". The connect() migration rides along
free, because you are already editing the query.

That also supplies the acceptance test the original Act 5 lacked: **no live reader selects a
stage-foreign column directly.** Measurable, and it fails today on `search_queries_used`.

---

## ACT 6 — REFUSED, and now on two independent grounds

1. **Empty ≠ dead** (established 2026-08-25). 8 of 11 return nothing because their SUBJECT tables
   are empty — `specifications`, `source_value_extractions`, `spec_value_probes`,
   `external_root_registry`. Deliverable tables awaiting judgment and synthesis.
2. **NEW, and stronger: the cross-stage views ARE the pointer mechanism.** Dropping them is
   dropping the thing the ruling mandates. `v_item_provenance` is the render→evidence citation
   pointer the owner described in words.

**The one remaining candidate is now clearly identified, and it is not in either protected class.**
`v_coverage_priority`: 7,208 rows, **research-stage only** (research + substrate), no cross-stage
pointer role, no empty-subject excuse, no reader. It is the only view whose deletion would remove
nothing the ruling requires. Even so it is a research-planning surface, and the owner's
cross-product ruling of the same day is exactly the shape it serves — so the honest verdict is
**hold, and let the cross-product frame decide whether it acquires a reader.**

---

## STAGE-CONTENT VIOLATIONS FOUND WHILE INTERROGATING (live, measured)

Not part of any act; surfaced by asking the phase question directly. Recorded so they are not
rediscovered.

| Fact | Lives in | Belongs to | Populated |
|---|---|---|---|
| `evidence_sources.search_queries_used` | evidence-collection | **research** | 10/10 — PD-6, has a remedy |
| `citation_mining.doi` | research | **evidence-collection** | 10 — PD-2, has a remedy |
| `source_locators.tier_claimed` | research (clue store) | **judgment** | 531 — EXEMPT, clue store |
| `search_candidates.tier_guess` | research | *its own* — a GUESS at screening time | 42 — legitimate, not a copy |
| `source_locators.used_in_bpcs` | research (clue store) | **render** | 56 — EXEMPT, clue store |

**Two are already queued with remedies. Two are inside the clue store and exempt by owner ruling
(§2.3) — the clue store may hold anything, because it exists to be copied OUT of. One is not a
violation at all:** `search_candidates.tier_guess` is a *guess made at screening time*, which is
research's own stage-specific fact, not a copy of the evidence tier. The ruling's test is whether
the fact is RESTATED from another table, not whether it resembles one.
