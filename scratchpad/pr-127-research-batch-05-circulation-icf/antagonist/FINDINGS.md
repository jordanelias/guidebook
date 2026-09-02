# Antagonist findings — batch 05

**Subject: the filed rows.** Not a plan, not a compliance census — `references/project-standards.md:638`
forbids those as adversarial subjects (*"a pass whose subject is a plan cannot be wrong about anything a
reader could check"*), and the previous batch's antagonist produced an 857-line census that was worth
nothing. Mechanic: blind-then-compare, against the retained payloads.

**Written up after the fact by the orchestrator**, from the agent's report and from the independent
re-verification of each finding. **The agent's own verbatim workings — every tool call, query and
intermediate result — are preserved at `transcripts/harness_6a6f63cd/subagents/`**, run 1 (killed by a
container restart) and run 2. This file is the reading; those are the record. The agent ran read-only and wrote nothing itself; this file exists
because rule 6 says a review surface must be on disk, and an empty `antagonist/` beside the agonist's
BRIEF.md and the tracer's LOG.md misrepresents what happened. **Every finding below was re-derived by
the orchestrator against the primary artefact before any data changed** — where the two disagreed, that
is recorded.

The first run of this pass was killed mid-flight by a container restart; a second run was given the
four threads it left open. Both are reflected here.

---

## P1 — resolved before anything reached canonical

### F1 · REF-00977 contains REF-00971 and REF-00784 as included studies

The brief instructed a reader to admit Kapsalis 2022 *"as context and **convergence**, not as an
anchor."* Counting a systematic review as convergent with two of its own included primaries is one line
of evidence counted three times.

Established from the review's own logged Crossref record, `1cfd192efd557b21.json`, 117 references:

- keys `e_1_3_3_43_1` … `e_1_3_3_90_1` are **exactly 48 entries** in strict first-author alphabetical
  order (Abu Tariah → … → Vredenburgh → Wretstrand)
- bounded **below** by the methods citations — 40 PRISMA/Moher, 41 US DoJ, 42 Hong/MMAT — and **above**
  by key 91, where the ordering restarts
- `e_1_3_3_56_1` = `10.3109/17483107.2010.509885` = **REF-00971** (Dutta part I)
- `e_1_3_3_71_1` = `10.1016/j.apmr.2010.01.009` = **REF-00784** (Koontz — the batch's declared anchor),
  adjacent to a second Koontz entry at key 70

**Scope is exactly two.** `10.3109/17483107.2010.549898` (REF-00972) appears nowhere in the 117
references, and REF-00974 post-dates the review. The agent's first run said *"three of eight sources are
in a containment relation"* — **that over-counted by one**, and the correction is the orchestrator's,
verified against the reference list.

**The finding behind the finding:** both containment DOIs were already in this batch's own
`citation_mining` row for ACG-08, written at 21:11. The mining ran, the list was stored, nobody read it
back, and the gate ran green over it.

**Acted on:** withdrawn the convergence reading, recorded on `REF-00977.verification_note`. Registered
as **D05-023** — nothing in the gate tests independence or containment at all.

### F2 · `REF-00978.co1_provenance` asserted a verification that did not happen

The field carrying a Co-1 source's CRPD Art 4.3 warrant ended: *"Provenance verified from the retrieved
report itself (p.2, p.28), not from a description of it."* Against `f07d3924aaec6708.pdf`:

- **p.2 is blank** but for the running header (`extract_text()` returns 34 characters, all header)
- **p.28 is survey question 40**, "How does this extra time cost affect you?"
- the real provenance is **p.3** and **p.10**
- **the charity registration number appears nowhere in the 29 pages** — it came from the exec-34 web
  description, which is precisely what the sentence denied

CLAUDE.md §2(c) in its purest form: a verification assertion that is itself the thing that failed. The
substance (disability-led) is true and is in the payload; the citation was not. **This was the
orchestrator's own error**, not the agonist's.

**Acted on:** replaced via `amend-source`, with p.10 and p.3 quoted directly, an explicit *"not in the
document"* for the charity number, and the Motability sponsorship that is on the report's face.

---

## P2 — fixed in this batch

### F3 · R7 filing gaps

Seven harm findings in the brief; four flagged rows.

| Brief | Exec | Was flagged | Outcome |
|---|---|---|---|
| H-1, H-3 | 39 | yes | — |
| H-2 | 38 | yes | — |
| H-5 | 37 | yes | — |
| **H-6, H-7** (Goodwin: egress + emergency-worker access; 71.0% in housing not meeting access needs) | **32** | **no** | flag raised, content filed |
| **H-4** (Marchiori: the level→any-slope step, plus the published 1:8 error) | 37 | flag yes, **content absent** | content filed |

H-4 is the most reusable single item in the batch and had no database home at all. R7 makes failure,
harm and inadequacy first-class evidence; leaving them in a brief is the by-product treatment R7 forbids.

**Acted on:** `amend-search --set-harm-finding` on exec 32 (monotonic — 0→1 only, since lowering would
erase a harm finding), plus both findings' content; H-4 appended to exec 37.

### F4 · Sponsorship unrecorded, and a ranking claim that was unsupported

On the face of the report: *"supported by the Motability Scheme"* (p.3); Motability Operations supplies
two of three pull-quotes and an About page (pp.9–10); Q29 *"Car — owned or leased"* **91%** (p.22); and
the top-ranked barrier at Q7 is **"A lack of appropriate parking available" 64%** (p.14) — the sponsor's
own domain. **The report publishes no methodology anywhere in 29 pages** — no sampling method, no
fieldwork dates, no per-question base, no weighting — so sponsor-channel recruitment can be neither
confirmed nor excluded.

The orchestrator's population-match note had asserted that self-selection *"does not affect the RANKING
of barriers against each other, which is what this source is admitted for."* A sample that is 91%
car-owning, recruited through a disabled-access charity co-branded with a car-lease scheme, is the most
plausible way to inflate that specific option. **Sustained.**

**Acted on:** filed as a **dissenting second population-match row** graded PROXY — the mechanic
DR-2026-08-19 §7 provides for exactly this — separating what survives (the in-building comparison,
56/41/41, between three options none of which is the sponsor's domain) from what does not (any use of
the whole-question ranking). Writing it exposed **D05-019**: the dissent was *unwritable*, because
`match_id` derived from session+ref+pop collided when the dissent came from the same session.

### F5 · The promoted lead's status was never moved

`source_locators` for REF-00784 still read `REFERENCE-ONLY` after the R9 cross-file, while the vocabulary
declares `PROMOTED` for exactly that transition and **881 of 881 rows had never used it**. The lead index
was saying "reference only, not evidence" about a ref_id carrying a full evidence row, a slug link and
two population matches.

Everything else about the cross-file was coherent — one ref_id, no duplicate identity, and the locator
correctly leaves `title`/`authors`/`pub_year`/`tier_claimed` NULL under rule 5.

**Acted on:** first `PROMOTED` in the table's history — which required writing `update-locator`
(**D05-020**), a command `insert_locator`'s own error message had been telling callers to use while it
did not exist.

---

## P3 — recorded

- **F6** · Three of the four flagged harm findings rested on abstract quotations with **no retained
  artefact**. The agent fetched all three from PubMed (PMIDs 20690862 / 21657823 / 40602232) and found
  every figure verbatim correct — a process gap, not a fidelity failure, but the batch's own claim that
  "no field was written from memory" could not be corroborated. **Acted on:** all three abstracts
  retained through `fetch()`; Marchiori's full text recovered via PMC10648130 after MDPI returned an
  Akamai block. Goodwin remains open (**D05-018**) — Wiley serves a Cloudflare interstitial to both OA
  endpoints and Unpaywall has no `url_for_pdf`.
- **F7** · exec 43 said *"4400+ **disabled** respondents"*. The report says "Over 4,400 **people**"; Q1
  (p.11) reports 88% completing as a disabled person. The population-match rows had it right; the exec
  row did not. **Acted on:** corrected in the row's own note.
- **F8** · `search_candidates` 73 still opens with the refuted *"6000+ respondents in 2023"*, with its
  correction below it. **Not changed, and the disagreement is recorded rather than resolved:** R15 asks
  that a staged guess not harden into fact, and leaving the guess legible beside what the source said is
  a stronger guarantee than erasing it. The agent read the ordering as a defect; the orchestrator holds
  that a hypothesis field and a warrant field take opposite correction rules, and only warrants get
  replaced.

---

## What the green gate does not see

`research_batch_dod.py` returned **COMPLIANT 17/17** over every finding above. Three structural blind
spots produced them, all registered:

1. **D05-021** — R7's harm count is *printed and never asserted*. Only `cand < screened//25` can fail
   it, so F3 was invisible by construction.
2. **D05-022** — R13 tests row **presence**, not soundness. It passed at 21:35 with 9/9; at 21:29
   REF-00978 had no match row and it would have failed. The gate is a race against the author, and it
   cannot see a match row whose stated rationale the payload contradicts (F4).
3. **D05-023** — **nothing tests independence or containment**, though `citation_mining` held the answer
   to F1 from 21:11. R2 passed on 3 rows for 9 anchors against a threshold of `9//4 = 2`.

---

## Attacked hard, could not break

A survived attack is a result, and these are stated so a later reader does not re-run them.

- **Co-1 is the right tier for REF-00978.** `governance/tier-system.md` §1 admits *"named-org …
  wheelchair-user … organisation outputs"*, and disability-led provenance is verified from the PDF itself
  (p.10: Euan MacDonald MBE, powerchair user, co-founded 2013). Tier 1 is **not** an over-claim: §1 is
  explicit that the tier number encodes claim-*type*, not quality. **The residual risk that stands** is
  claim-type — Co-1 anchors preference, dignity and self-determination claims, and this source is
  admitted for a prevalence ranking at the ● Full band with nothing on the row limiting it.
- **"Over 4,400" is correct** and is a whole-survey figure (p.3); no per-question base exists to
  contradict it. **`pub_year=2026` is correct** — p.1 reads "Published March 2026" (PDF `/CreationDate`
  D:20260312) despite the 2025 title.
- **The Goodwin Co-1 → T3 downgrade is correct.** No co-production, no DPO involvement, proxy voice; the
  only participation was that the survey was piloted by three people with mobility impairment.
- **Kapsalis's MMAT appraisal is confirmed** — T2 stands, independently of F1.
- **Marchiori's quoted figures are verbatim** in the retained full text, every one.
- **Goodwin H-6 and H-7 quotes are verbatim**, including "27.5 / 71.0 / 38.6 / 32.4 per cent",
  "85.1 per cent and 59.6 per cent", the emergency-worker sentence, and Participant 66's "without
  damaging walls" with the stated age band and limitation.
- **Dutta / King bylines are correct in both directions** (Dutta first on 509885, King first on 549898),
  confirmed against three payloads and PubMed.
- **REF-00972 and REF-00974 are genuinely independent of REF-00977.** Checked; they are not in it.
- **The Q7 "most-cited barrier" over-claim** was found independently by the agent — parking at 64% sits
  on p.14, past the page break, so a reader looking at options 1 and 2 alone sees 41 and 56 and stops.
  The orchestrator had already self-corrected it, with a 12-option enumeration matching the agent's
  digit-for-digit. **Worth noting that the correction landed *after* the DoD ran green.**
