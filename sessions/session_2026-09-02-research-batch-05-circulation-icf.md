# session_2026-09-02-research-batch-05-circulation-icf

**Research batch 05 · slug `accessible-circulation-geometry` · ICF-first frame · three agents**

Volatile figures below were derived from `data/guidebook.db` and
`retrieval-log/session_2026-09-02-research-batch-05-circulation-icf/manifest.jsonl`
after the migration applied, not carried from the working conversation.

---

## What this batch was for

Three jobs at once, at the owner's direction: **perform research**, **ensure compliance
with process**, **log the work**. Run as three agents — an **agonist** that retrieves and
vets before anything is written, an **antagonist** that attacks the filed rows, and a
**tracer** that records actions, errors, gaps and failures for audit.

The frame was pulled ICF-first for the first time, under D-0187: axes with codes AND
names, access needs, populations and their crossing maps. No item codes and no item
values entered the frame, and it declared its own two gaps (`slugs.serves_axes`
populated on 1 of 106 rows; no term↔slug link exists, so R11's `terms_used` cannot be
populated from the slug) rather than reading a generic frame as a scoped one.

## What landed

| | |
|---|---|
| `evidence_sources` | 9, one of them Co-1 |
| searches logged | 15, of which 5 carry a harm finding |
| candidates staged | 15 |
| population matches | 14, including one dissenting second row |
| citation-mining rows | 5 this batch, 15 in the table |
| leads promoted | 1 (the first `PROMOTED` in 881 locator rows) |
| payloads retained | 49, 4,626,254 bytes, one of them a PDF |
| schema | `user_version` 67, unchanged |

`research_batch_dod.py`: **COMPLIANT, 17/17**. `retrieval_log --verify-authors`:
**CLEAN on 8 examined**. `migrate_db.py --rebuild`: reproducible. All DB-derived outputs
regenerated and `--check`-clean.

## The findings that were worth the batch

**Circulation geometry is the most-cited in-building barrier disabled people report.**
Euan's Guide Access Survey 2025 (REF-00978, Co-1, over 4,400 respondents, 88% of them
disabled people), question 7, p.13–14: *"I could not get around the venue (e.g. lack of
lifts, narrow corridors, too little space or poor layout)"* — **56%**, against *"could
not get into the venue"* 41% and *"no access to a toilet that suits my requirements"*
41%. Second of twelve options overall, behind parking at 64%.

**The shoulder-load penalty is incurred by the existence of a slope, not by its
steepness.** Marchiori, Gagnon & Pradon 2023 (REF-00973), Table 3: shoulder
flexion/extension push-phase HIGH risk runs 12.2% level → 44.5% → 47.0% → 45.2% across
1:20, 1:16, 1:12. The authors' own reading: *"greater efforts are required to propulse
the wheelchair from the smallest slope (2.7°), but that this effort does not increase
further with the increasing slope."* A frame built from an item called "Ramp Gradient
(≤1:20)" would have gone looking for the difference between 1:20 and 1:12 and found the
wrong question.

**A published error, flagged.** That same paper's §2.2 says *"The four slopes greater
than 0° corresponded to slopes that increase from one unit of height to 20, 16, 12 and 8
units of length"* — four ratios for three slopes. arctan settles the mapping:
2.86°/3.58°/4.76° ⇒ 1:20/1:16/1:12. **1:8 is 7.13° and was never tested.** Anyone citing
this paper for a 1:8 result cites its error.

**Ramp *descent* outranks fast propulsion for shoulder load**, and the discourse is all
about ascent (REF-00974, abstract-level locator, ten able-bodied participants — the
ordering is the claim, not the newtons).

**A 49-record Japanese J-STAGE seam invisible to English engines**, including 2003 prior
art (REF-00976, admitted under R5: non-English peer-reviewed work is academic, and
non-indexation is an indexing fact).

## What went wrong, and was caught

**Three fabricated bibliographic fields were filed and passed every gate.** REF-00976
stored a title no payload asserts and a co-author given name three payloads contradict
(*Naoji* → *Toshiyuki*); REF-00973 stored a title bent toward the slug it was admitted
for. `--verify-authors` printed CLEAN over all three, because it compared **family names
only** and never looked at given names or at titles at all — CLAUDE.md §2(a) at field
granularity, inside the module written to prevent §2(c). It also indexed only Crossref's
single-work envelope, so three of eight sources reported as *"NO LOGGED RETRIEVAL — not
verifiable offline"* over payloads sitting on disk. `EXAMINED` went 5 → 8 on the same log
once fixed.

**The one disability-led source was screened out on a 404.** exec 34 logged a
*"Page not found"* page — 15,580 bytes containing no occurrence of *survey*,
*respondent*, *toilet* or *staff* — and then characterised the report's content from it,
as *"predominantly information provision, toilets and staff attitude rather than
circulation geometry"*, with *"6000+ respondents in 2023"* beside it. That sentence was
the reason nothing was admitted. R10 says a block is not a terminal answer and a 404 is
not either: the live report was one hop from the homepage, and its most-cited in-building
barrier is the slug's own subject. That the guess was directionally plausible about
toilets is luck, not method.

**A systematic review was about to be counted as convergence with two of its own included
studies.** REF-00977 (Kapsalis 2022) contains REF-00971 (Dutta part I) and REF-00784
(Koontz — the batch's declared anchor) among its 48 included studies. Established from
the review's own logged Crossref record: keys `e_1_3_3_43_1`–`e_1_3_3_90_1` are exactly
48 entries in first-author alphabetical order, bounded by the methods citations below and
by the restart of ordering above. **Those DOIs were in this batch's own `citation_mining`
row from 21:11.** The list was stored and never read back, and only an adversarial reader
caught it.

**My own errors, in order of seriousness.** (1) `REF-00978.co1_provenance` — the field
carrying the CRPD Art 4.3 warrant — ended *"verified from the retrieved report itself
(p.2, p.28), not from a description of it"*. p.2 is blank but for the running header,
p.28 is survey question 40, and the charity registration number the sentence carried
appears nowhere in the 29 pages: it came from the web description the sentence denied. A
verification assertion that is itself the thing that failed. (2) I recorded circulation
as *"the single most-cited barrier in the survey"* having read the two options beside
each other rather than all twelve; parking at 64% outranks it. Corrected on all three
affected rows and in the commit message, which had not been pushed. (3) A
population-match note claimed self-selection *"does not affect the RANKING of barriers"*
— unevidenced, and most likely wrong in a specific direction, since the survey is
supported by the Motability Scheme, 91% of respondents own or lease a car, and the
top-ranked barrier is parking.

## Writers that did not exist

Five gaps in `scripts/db.py`, each found by needing it:

- **`correct-source`** — no way to fix a bibliographic field. Deliberately has **no flag
  for the value**: the argument names *which* field to take, the logged payload supplies
  *what*. Every wrong field today was typed by a writer holding the payload, so a
  `--title` flag would rebuild the hole one level up.
- **`amend-search`** — R8 makes the search log append-only, and it must stay that way,
  but a note can be wrong. Appends after a dated marker; the original is never touched.
  Gains a **monotonic** harm flag: 0→1 completes an incomplete R7 record, 1→0 would erase
  a harm finding and is refused.
- **`resolve-candidate`** — R15 requires re-description from the source on resolution and
  had nothing to do it with. Appends rather than overwrites: R15 asks that a guess not
  harden into fact, and leaving the guess legible beside what the source said guarantees
  that better than erasing it.
- **`amend-source`** — corrects **judgement** fields, refusing every bibliographic column
  by name and pointing at `correct-source`. Replaces rather than appends, and that
  asymmetry is the point: a hypothesis field should show what was believed, a warrant
  field should not stay quotable once it is false. The replaced text goes to
  `metadata_integrity_detail` with the date and the reason.
- **`update-locator`** — which `insert_locator`'s own error message has told callers to
  use, while no such command existed.

**And the adversarial mechanic was unwritable.** `evidence_population_match.match_id`
derived as session+ref+pop, so a dissenting grade raised in the **same** session as the
grade it dissents from collided on the primary key — the id derivation quietly abolishing
the mechanic the comment six lines above it defends. DR-2026-08-19 §7's *"distinguished
by created_by_session"* held while adversarial passes were separate sessions; under the
agonist/antagonist format they are routinely the same one.

## What the green gate does not see

Recorded as defects rather than fixed here, because each needs its own change:

- **D05-021** — R7's harm count is printed and never asserted. Only
  `cand < screened//25` can fail it, so the exec-32 filing gap was invisible by
  construction.
- **D05-022** — R13 tests row **presence**, not soundness, and passes or fails on when
  the author happened to write the row.
- **D05-023** — **nothing tests independence or containment.** The gate ran green over a
  containment its own `citation_mining` table already held.

## Three writers that could not produce a compliant row

The batch gated COMPLIANT on all 17 research rules and then failed the repository's
own integrity battery, because moving `sessions/LATEST-RESEARCH` onto this session
re-scoped gates that had been passing vacuously against batch-02. Every failure was a
writer that could not produce a state its own checker accepts:

- **`insert_source` set `verification_disposition='OPEN'` on every VERIFIED row**, which
  D-0157 invariant I1 forbids outright — *"verification is finished or it did not
  happen."* This went unseen while `evidence_sources` held 0 rows and I1 was vacuous;
  this batch repopulated the table and all nine rows failed together. A default no row
  can satisfy is a trap, not a default. VERIFIED now defaults CLOSED.
- **`log_mining` never touched `citation_mining_status`**, so `test_db_integrity` C08's
  biconditional — `'mined'` iff a non-deferred mining row resolves to it — could not
  hold through the sanctioned path at all. It now sets the status, takes a
  `--deferred-reason`, and refuses a pass that is neither productive nor deferred,
  because a mining pass that found nothing and does not say why is indistinguishable
  from one that never ran.
- **`add-source` had no `--prior-expectation`**, the field
  `research_protocol_audit` CHECK 7 asks for on every verified citation. The flag now
  exists. **The nine rows in this batch are left failing that check and were not
  backfilled**: the field records what you expected the source to say *before reading
  it*, and a prior written afterwards is a post-hoc rationalisation wearing the field
  that exists to prevent one. Registered as D05-025.

R2 was closed properly rather than waived: REF-00784, the batch's declared T1 anchor,
was mined backward (12 DOIs from its Crossref record), and REF-00978 was marked
`not-applicable` with a reason — the Euan's Guide report carries no reference list,
bibliography or citation of any kind across its 29 pages, so backward mining has
nothing to walk. `not-applicable` rather than `pending` so a reader can tell *nothing to
mine* from *not yet mined*.

`metadata_integrity_audit` is advisory-red on this batch **by design**: nine rows carry
`metadata_integrity_status='CORRECTED'` because nine rows had metadata corrected. That
is an owner-review queue doing its job, recorded here (D05-028) so the red is not later
mistaken for drift and suppressed.

## Still open

`D05-001`/`D05-002` (the frame's declared gaps), `D05-004` (the command-log hook is
misfiling this session's own log into batch-04's directory), `D05-018` for Goodwin only
(Wiley serves a Cloudflare interstitial to both OA endpoints; Unpaywall has no PDF
location, so that source rests on a committed text file rather than a logged payload —
recorded on the row, because R10 says a block is not a terminal answer and this one is
not beaten yet), and `D05-021`–`D05-024` above.

`sessions/LATEST-RESEARCH` moves to this session, which closes **D05-006** — it had been
naming batch-02 while batch-03 was the newest session with research rows.

Full narrative in `scratchpad/pr-127-research-batch-05-circulation-icf/`:
`FRAME.md`, `agonist/BRIEF.md`, `antagonist/FINDINGS.md`, `tracer/LOG.md`, and
`DEFECT-REGISTER.md`, which is the single home of defect status.

`antagonist/FINDINGS.md` was written up after the fact by the orchestrator rather than by
the agent, which ran read-only and wrote nothing. That directory stood empty beside the
agonist's and the tracer's files until the omission was noticed — the pass that produced
the session's most valuable findings had no review surface, which is the exact failure
rule 6 names. It records what the agent claimed, what re-verification sustained, the one
place it over-counted, and the one place the orchestrator disagreed and why.
