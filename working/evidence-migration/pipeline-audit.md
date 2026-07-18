# Full-chain pipeline audit — parameters → gathering → processing → grading → modes → lenses → website

*Grounded in `data/guidebook.db` and the repo, 2026-07-18. Every figure is a query result. This audit
supersedes the completeness framing in the migration plan's Part I.b where they conflict — notably, the
plan read `bpc_metadata.jurisdictions_searched = 0/82` as "no search done"; the substrate tables show that
is **false** (see Link 2).*

## The chain, and the shape of the problem

The project is an 11-link chain. Surveyed end-to-end, it has a characteristic and decisive shape:
**wide at the top (doctrine + gathering are near-complete), catastrophically narrow in the middle
(extraction → grading → modes are pilot-only), and a wide-but-hollow shell at the bottom (87 render pages,
7 with graded evidence behind them).** Everything downstream is *starved by the midstream grading
bottleneck*, and the corpus's English skew is *manufactured in the ingestion funnel, not the search*.

| # | link | completeness | methodological rigour | key evidence |
|---|---|---|---|---|
| 1 | Project parameters / doctrine | **~100%** | **very high** | S1–S8 + Part V·5 (this session); 7-tier reconciled; 25+ DR records; A10 |
| 2 | Gathering — language search | **~100%** (lang) / ~17% (juris) | high (systematic, multilingual) | `search_languages` 1539 = 19 langs × 81 slugs; `search_coverage` 3807 but 3152 NOT-RUN |
| 3 | **Ingestion / curation** | **the bias bottleneck** | verification high, funnel opaque | 14 langs returned results; corpus still 551:89 EN — skew is *downstream of search* |
| 4 | Processing — citation-mine / supersession | **~7–9%** | high where done | `citation_mining` 107/7 slugs; `supersession_check` 134/6 slugs |
| 5 | Extraction / value-derivation | **~1–4%** | **very high** where done | `source_value_extractions` **1 slug**; `spec_value_probes` **3 slugs** (PMP walks, strict-termination) |
| 6 | Grading — cell-state | **7/93 items (7.5%)** | very high | `evidence_cell_state` 11 cells; `convergence_assessment` 10; falsification conditions, `echo_of` |
| 7 | Modes — Universal/Population/**Person** | Univ/Pop partial; **Person ~0** | doctrine clear (DR-2026-07-13) | design_scale {pop 9, univ 2, **person 0**}; `items.pmp_delta` **2/93** |
| 8 | Lenses — multimodal presentation | **spec 100%, applied ~7%** | high (encodes anti-laundering) | `weighting_profile` 5 rows/4 audiences; applied only where cells exist |
| 9 | Website / render | **shell ~93%, evidence-backed ~7%** | render is non-canonical (S4) | `site/specs/*.html` **87**; only 7 items graded behind them |
| 10 | Connections / gaps / terms | active | systematic gap taxonomy | gaps 297 (**37 OPEN**); connections 273; terms 30 / aliases 880 |
| 11 | Governance / integrity | high; one stale | **the most rigorous link** | `data_migrations` 196; attestation CI stale (35-commit, non-blocking) |

---

## Link-by-link, with logic traced both directions

**Link 1 · Parameters / doctrine — complete, highest-rigour.** The constraint layer (seven-tier hierarchy,
three modes, top-down/bottom-up, CRPD/Kawa/A10, radical transparency) is extensively reconciled and ratified
(the `DR-2026-07-*` cluster: evidence-architecture-unification, person-mode-functional-capacity,
value-genealogy-and-derivation-handshake, integrity-protocol-three-modes). This session added S1–S8, the
Part V·5 ethics gate, and the transparency model. *Backward pull:* doctrine correctly constrains everything
below it — it is not the problem. *Forward:* it defines a target the midstream cannot yet meet.

**Link 2 · Gathering (search) — wide, and better than the flags claim.** `search_languages` holds **1539
rows = 19 languages × 81 slugs**: every slug received a ~19-language sweep. This **contradicts
`bpc_metadata.jurisdictions_searched = 0/82`** — the flag is decorative; the search happened. *Rigour:*
systematic and multilingual (PRISMA-shaped). *Gap:* `search_coverage` (slug × ~47 jurisdictions = 3807) is
**3152 NOT-RUN** — the *jurisdiction* sweep is ~17% run even though the *language* sweep is complete. Co-1
search attempted on only 231/3807 cells.

**Link 3 · Ingestion / curation — THE BIAS BOTTLENECK.** The multilingual search demonstrably surfaced
non-English literature at scale — 14 languages returned results (DE 109 hits, NO 82, JA 82, NL 76, FR 75,
ZH 74, IT 65, ES 58, SV 56, KO 54, PT 52, DA 52, FI 50) — yet `evidence_sources` is **551 EN : 89
non-EN**. *So the English skew is created here, in ingestion, not in search.* (Precise unique-source
attrition needs dedup — `results_count` double-counts a paper found for multiple slugs — but the direction
is unambiguous: search found much more non-English material than the corpus retained.) **Two hard sub-findings:**
(a) **5 Global-South languages returned zero across all 81 searches — Swahili, Indonesian, Hindi, Bengali,
Arabic** — a search-*reachability* blind spot (tooling/index/transliteration), not a curation choice; (b)
the ~35 registered-but-un-migrated sources from the L0 pass (several non-English) are part of the same
funnel. *This is the precise, actionable core of "bias management."*

**Link 4 · Processing — partial but rigorous.** `citation_mining` (107 rows, backward+forward, across **7
slugs**) and `supersession_check` (134 rows, **6 slugs**) match the `citation_mining_complete = 6/82` flag —
here the flags are honest. Deep, but pilot-scale.

**Link 5 · Extraction / value-derivation — pilot-only, very high rigour.** `source_value_extractions`
exists for **one slug** (room-acoustic); `spec_value_probes` (PMP walks with strict-termination logic,
`echo_of` provenance separating code-echoes from evidence roots) for **three** (room-acoustic,
circadian-lighting, school-environment-autism). Where done, this is the most methodologically sophisticated
work in the project. It is the **narrowest link** — the bottleneck's throat.

**Link 6 · Grading — 7/93 items.** `evidence_cell_state` = 11 cells / **7 items** (A-18, B-10, C-02, E-06,
E-08, E-12, G-03), with tier_basis, falsification conditions, `code_floor_only`, and single-axis convergence
assessments. Rigorous, tiny. *Forward starvation begins here:* modes, lenses, and render all depend on
graded cells, and there are seven.

**Link 7 · Modes — Person mode is absent.** design_scale = {population 9, universal 2, **person 0**};
`items.pmp_delta` set on **2/93**. The doctrine (Person = OT resolving position *within* the Population
range, DR-2026-07-13) is clear; the data isn't there. *Backward:* the OT lens (`weighting_profile` ot row)
is specified and waiting; *forward:* Person-Mode handoff cannot render.

**Link 8 · Lenses — the spec is complete and excellent; application waits on grading.** `weighting_profile`
(5 rows, 4 audiences) encodes the doctrine precisely: designer (aspiration-above-floor, DAR surfaced),
disabled_person ×2 (Co-1 visibility + solo-authorship limit always rendered; advocacy-brief with
instrument-status caveat), policymaker (floor-vs-anchor, **anti-laundering, convergence-is-not-evidence**),
ot (population range legible for person-mode resolution). This is a well-formed lens engine with **only 7
items to drive through it.**

**Link 9 · Website / render — wide shell, shallow fill.** 87 `site/specs/*.html` + `populations/` +
`rooms/`. The E-08 exemplar shows the target 12-facet, 4-door shape. But ~80 of 87 pages sit over ungraded
evidence. The render is declared non-canonical (S4), so this is not a rigour defect — it is a *fill* defect
inherited from Link 6.

**Link 10 · Connections / gaps / terms — active cross-cutting layer.** gaps 297 (**37 OPEN**; closed split
across SYSTEMIC 90 / SYNC 87 / FIXED 52 / FALSE-POSITIVE 26 / RESOLVED 5); connections 273 / targets 507; a
terminology layer (terms 30, term_item_links 50, aliases 880). Healthy and systematic.

**Link 11 · Governance / integrity — the most rigorous link, one stale check.** `data_migrations` 196
(migration-based writes enforced), a deep DR/attestation regime. The only defect is operational: the
`adherence_log_audit` CI check fails because ~35 `decisions_*`/`sessions_*` records are past their
re-attestation window (non-blocking; unrelated to content).

---

## Tracing the logic both directions — the two dominant forces

- **Forward starvation (top → bottom):** the grading throat (Link 5–6, ~7 items) starves Modes (Link 7),
  Lenses (Link 8), and Render (Link 9). The website *promises* a shape (E-08's 12 facets, 4 doors, 3 modes,
  5 lenses) that the evidence base can fill for 7.5% of items. **Nothing downstream can improve until the
  grading throat widens.**
- **Backward specification (bottom → top):** the render + lens layer is *fully specified* (E-08 exemplar,
  `weighting_profile`) and therefore acts as a precise **target that pulls** the midstream — we know exactly
  what a finished cell must produce. This is a strength: the bottleneck is not "we don't know what to build,"
  it's "we've only built it 7 times."
- **The bias funnel cuts across the chain:** Link 2 searched 19 languages; Link 3 ingested English-heavy;
  so Link 8's policymaker "jurisdiction-comparison" lens and Link 6's population cells are **under-fed with
  non-English / Global-South evidence** — a bias that originates mid-chain and propagates to the render.
- **Broken feedback loop:** `bpc_metadata` flags don't reflect the substrate tables (they understate
  gathering, don't see extraction/grading), so the project **cannot read its own state** — which is how the
  A-18 pilot's first draft mis-reported filled cells as gaps. Fixing the flags is a prerequisite for
  trusting any completeness number, including this audit's inputs.

---

## Where to focus (the user's hypothesis, confirmed and precisely targeted)

**1 · Evidence curation — widen the grading throat (Links 5–6).** The single highest-leverage action. 75+
slugs and 86 items are gathered but ungraded; the value-derivation → grading pipeline exists and is
rigorous but has run ~3 times. Everything downstream is starved by this. *Prerequisite (Stage −1 in the
plan): inventory each slug's existing substrate first* — search/citation/extraction — so grading builds on
it and doesn't redo it or mis-report it.

**2 · Data migration — make state legible and complete the funnel.** (a) **Reconcile the flags** against
the substrate tables so `bpc_metadata` tells the truth (gathering is done; grading isn't). (b) **Ingest the
non-English backlog** the search already surfaced (Link 3) + the L0 registered-but-un-migrated ~35. (c) Fix
the flagged data errors (the Devos-2019/REF-00571 mislink; four duplicate ANSI records) and apply the
jurisdiction-hygiene migration.

**3 · Bias management — attack the ingestion funnel, not the search.** The search is multilingual and broad;
the **curation** is where English wins. (a) Reconcile `search_languages` (1153 non-EN hits, 14 languages)
against `evidence_sources` (89 non-EN) and ingest the gap. (b) Investigate the **5 zero-result Global-South
languages** (SW/ID/HI/BN/AR) — tooling reachability vs genuine absence; state which. (c) Correct the
`lang_detected` mislabels (non-English standards tagged `en`). (d) Address the Co-1 skew (26/29 EN, 21/29
US+UK) as the most-skewed modality.

**One-line diagnosis:** *the project has gathered broadly and reasoned rigorously, but has only pushed ~7%
of items through the value-derivation → grading throat, and loses most of its non-English evidence in the
ingestion funnel — so the fix is throughput (curation/grading) + funnel repair (ingestion/bias) + state
legibility (flag reconciliation), not more doctrine or more search.*
