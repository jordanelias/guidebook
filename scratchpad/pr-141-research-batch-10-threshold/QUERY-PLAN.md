# Query plan — batch 10, the threshold pass. Priors written before execution.

Each row's `prior` is what goes into `log-search --prior-expectation` verbatim. Committed before
the first query runs. Engine `web` on every row: Step 1 of `multilingual-research_SKILL.md` says
retrieve from publication pages directly, so a general index is used to **locate** a publication
page and never as the evidence itself (T3 = navigation, never content).

**Order is deliberate.** Leg A first, because a freely-published statute is the only document class
in this batch I expect to reach in full; Leg B second, so the paywall attempts are recorded against
a batch that already has content rather than standing as its whole result; Leg C and D last,
because they are the ones whose value does not depend on reaching a number.

---

## Leg A — statutory codes, freely published (T6: `code` × `intrinsic`)

| # | Jur | Lang | Target | Query (verbatim) | Prior |
|---|---|---|---|---|---|
| 1 | JP | JA | national_fw | 高齢者、障害者等の移動等の円滑化の促進に関する法律 建築物移動等円滑化基準 傾斜路 勾配 e-Gov | `research_code_leads` 85, and it is a **falsifiable** row. The lead records that REF-00989 attributes three figures to this law — 12分の1, 1/15 outdoors, and 8分の１ for rises of 16cm or less — and that the law itself was never retrieved, so none was copied in (rule 5). Japanese law is published in full on e-Gov, so I expect the clause text itself. Prediction: all three figures are confirmed and no basis is stated for any of them. If they are not confirmed, the corpus has been holding a lived-experience assessment of a legal figure that is not what the law says, which is a larger finding than the value. |
| 2 | FR | FR | national_fw | arrêté accessibilité ERP pente rampe pourcentage Légifrance texte consolidé | Légifrance publishes consolidated text free. I expect 5% as the general maximum with tolerances at 8% and 10% conditioned on length — i.e. a rise-conditioned structure like the Flemish one, which would make Flanders less of an outlier than it currently looks. No stated basis. |
| 3 | GB | EN | national_fw | Approved Document M access to and use of buildings ramp gradient table gov.uk | AD M is Crown copyright and published free, unlike BS 8300 which it references. I expect a gradient/length table (1:20 to 1:12 by flight length) and an explicit pointer to BS 8300 for anything further — which makes AD M the reachable proxy for row 6's paywall, and I must record it as AD M's own figure, not as BS 8300's. |
| 4 | CA | EN | national_fw | National Building Code of Canada accessibility ramp slope 1:12 free view NRC | NRC offers free read-only access to the NBC. I expect 1:12 restated from the same North American lineage as ADA, which would be convergence by descent rather than independent agreement — and `v_value_independence` exists precisely because that reads as corroboration and is not. |
| 5 | AU | EN | national_fw | National Construction Code accessibility ramp gradient 1:14 ncc.abcb.gov.au | The NCC is free (registration-gated) and calls up AS 1428.1, which is not. I expect 1:14 — a figure no other jurisdiction in this corpus uses — and if it lands it is the strongest single disagreement the batch can produce. Registration may defeat retrieval; that is R14 RETRIEVAL FAILURE, not absence. |

## Leg B — the sold standards named in `research_code_leads` 84

| # | Jur | Lang | Target | Query (verbatim) | Prior |
|---|---|---|---|---|---|
| 6 | GB | EN | standard_eb | BS 8300-1:2018 section 10 ramp gradient clause text | Lead 84. Sold by BSI. I expect a catalogue page and a scope preview, no clause text. **The BSI catalogue page is already held against seven ref_ids** (batch 09 measured this) — it is a landing page for a standards family, so meeting it again is not a new identity and must not be cross-filed as one. Expect R14 RETRIEVAL FAILURE. |
| 7 | AU | EN | standard_eb | AS 1428.1:2021 clause 15 ramp gradient design for access and mobility | Lead 84. Sold by Standards Australia. Same shape as row 6. If row 5 reached the NCC, the figure is already in the corpus from a document I could actually read, and this row's value is confirming the citation chain, not the number. |
| 8 | JP | JA | standard_eb | JIS T 9251 規格票 傾斜 勾配 日本産業標準調査会 JISC 閲覧 | Lead 84 names JIS T 9251:2014 against ramp gradient. **I doubt the lead, and the doubt is the reason to run the row.** My recollection is that T 9251 is the tactile ground surface indicator standard rather than a ramp standard — `[UNVERIFIED]`, memory, and exactly the kind of claim this project does not act on unread. JISC offers free browsing, so it is testable rather than arguable. Prediction: the standard is retrievable AND is about a different parameter, which makes this row a **correction to lead 84** rather than an admission. R15 governs — a staged description is a hypothesis and gets re-described from the source. |
| 9 | ISO | EN | standard_eb | ISO 21542:2021 building construction accessibility usability built environment ramp gradient OBP | The only T4 (`standard_eb` × `international`) in reach, and one T4 alone satisfies §2.3 richness. ISO's Online Browsing Platform publishes terms and scope free, full clauses sold. I expect scope and definitions, not clause 24. If the gradient IS free-viewable this is the batch's cheapest admission — and per PRIORS that is a consequence, not the reason to run the row. |

## Leg C — the Flemish handbook's dated carrier (candidate 69)

| # | Jur | Lang | Target | Query (verbatim) | Prior |
|---|---|---|---|---|---|
| 10 | BE | NL | national_fw | Stedenbouwkundige verordening toegankelijkheid Vlaanderen artikel 19 helling hellingspercentage gepubliceerde tekst | **The route is the candidate's own, not one I chose.** Candidate 69 names its resolution explicitly: *"Resolve by retrieving a dated carrier (the Flemish Stedenbouwkundige verordening toegankelijkheid Art. 19 as published)"*. That is a dated Flemish decree, published free, and it carries the gradient table in a form that can be given a `--year`. Prediction: Art. 19 states the rise-conditioned table and does **not** carry the acceptability criterion, which is the handbook's own commentary — so the decree resolves the table and leaves the criterion still needing its own dated carrier. If no dated carrier is reached, the candidate stays PENDING-VERIFICATION and **no year is supplied** (§5(c)). R15: re-describe from the decree, and correct the candidate if the table differs. |

## Leg D — the Co-1 leg (R1; and the lived threshold, from the other side)

R1 is not satisfiable by a regulatory pass and must not be waived with `CO1-NOT-APPLICABLE` here:
the threshold question is exactly the one lived experience answers best, and batch 09 proved the
Co-1 leg is reachable in Japanese. Every route below is named in batch 09's own Owed list as a
Co-1/Co-2 target that exists and was not reached.

| # | Jur | Lang | Target | Query (verbatim) | Prior |
|---|---|---|---|---|---|
| 11 | JP | JA | co1 | DPI日本会議 障害者団体 スロープ 勾配 建築物移動等円滑化基準 意見 | The natural pairing for row 1: a Japanese DPO commenting on the Japanese statutory figure. I expect a position or consultation response arguing the legal gradient is insufficient — an inadequacy finding under R7 and the 2026-09-13 ruling, not a value. If it states a preferred maximum with its own warrant, that is the batch's most valuable admission. |
| 12 | FR | FR | co1 | APF France Handicap accessibilité pente rampe position dossier site apf-francehandicap.org | Batch 09 got vendors and compliance consultancies from a general query. Going at the publication site directly is the change. I expect position material framed on rights and enforcement rather than on a gradient, and a real chance of RETRIEVAL FAILURE behind site navigation rather than absence. |
| 13 | ES | ES | co1 | CERMI ONCE Fundación accesibilidad pendiente rampa silla de ruedas publicación guía | Same correction as row 12, same expectation. CERMI publishes extensively and indexes poorly. Prediction: documents exist, the general index does not surface them, and the honest R14 diagnosis is WRONG INDEX. |
| 14 | US | EN | co1 | Paralyzed Veterans of America accessible design ramp slope publication pva.org | Batch 09 logged this as zero-yield from a general query. PVA authors accessibility guidance and is a disabled-led membership organisation, so a zero from its own site is a much stronger claim than a zero from a search engine — and that is the point of re-running it at the source. |

---

## What this plan commits me to in advance

1. **Every number is traced to its warrant before admission.** If the warrant is another code, the
   source is evidence of that code's uptake, not of the value — grade the figure accordingly and
   say so in the extraction.
2. **Every execution is logged, zero-yield included**, with R14's four-way diagnosis stated:
   genuine absence / wrong index / query-shape failure / retrieval failure. A paywall is the fourth,
   never the first.
3. **Admission-first order when logging.** `log-search` refuses `--results-admitted` without
   `--admitted-ref-id` (H05) and `amend-search` takes only `--append-note`, so an admission decided
   after its search was logged is permanently edgeless. Batch 09 hit this and rebuilt its scratch to
   escape it. Build the scratch in admission-first order from the start.
4. **`add-source --pages` at admission, on every clause-cited document.** R3 reads
   `evidence_sources.pages`; `correct-source` has no value flag and `amend-source` refuses
   bibliographic fields, so a page locator cannot be added afterwards. This batch is clause-cited
   documents almost exclusively — getting this wrong means rebuilding the scratch.
5. **A relation `--quote` must come off persisted bytes, and there is no exemption.**
   `_write_relation_edge` calls `_verbatim(quote, from_ref_id)` and raises with no `exempt_reason`
   parameter (`scripts/db.py:4802`) — unlike `--claim-text`, which `--verbatim-exempt` can ledger.
   A standard that states its figure against a named reference therefore cannot be extracted unless
   the citing sentence itself was retrieved. Rows 3, 5 and 7 are the likely casualties: AD M and the
   NCC both call up a sold standard by name.
6. **Nothing is cross-filed against a landing page.** One address serving a standards family
   resolves to many ref_ids; R9a is now URL-aware and silent on those by design. Meeting the BSI or
   ISO catalogue page again is not meeting a held identity.

## The pre-state probe, run before any of the above

```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/audit/research_batch_dod.py \
  --session session_2026-09-17-research-batch-10-ramp-gradient-threshold
```

Run 2026-09-17 against a scratch copy: fires **exactly R1, R9a, R9b** and nothing else, which is
`workplan/2026-09-10-batch-06-runbook.md` Step 0's uncontaminated-id signature. Any other rule
firing on this id means it has been used; stop and pick another.

## What would move the cell, and why that is not the objective

Measured 2026-09-17 by calling `assess_cell.regulatory_richness` against the live value-supplying
set (REF-00987 T6/US, REF-00988 T5/DE) with one hypothetical row added:

| added to the live set | `regulatory_richness` |
|---|---|
| +1 T4 international (row 9) | **True** — ">=1 T4 international standard present" |
| +1 T5 national_fw, new jurisdiction (rows 6–8) | **True** — ">=2 T4-5 sources, distinct jurisdictions" |
| +1 T5 national_fw, **same** jurisdiction (DE) | False — below §2.3 richness |
| +1 T6 code, new jurisdiction (any one of rows 1–5) | False — below §2.3 richness |
| +2 T6 codes, two new jurisdictions (any two of rows 1–5) | **True** — ">=3 T6 codes from 3 distinct jurisdictions" |

**This contradicts lead 84's own note, and the machine wins.** Lead 84 says *"Retrieve ONE
jurisdiction's ramp clause and the cell becomes determinable."* One clause is enough only if it is
a T4 international standard or a T5 national framework from a jurisdiction other than DE. A single
new **statutory code** — the class Leg A is built from, and the class most likely to be
retrievable — does **not** flip it; two from two new jurisdictions do. The lead was written as a
hand-assigned claim about a computed fact, which is rule 8's anti-pattern, and a batch that
retrieved exactly one Japanese statute and stopped would have satisfied the lead and moved nothing.

Re-derive rather than trust this table — it is a hand-copied result inside a plan, which rule 7a is
exactly about. The probe:

```
python3 - <<'PY'
import sys, sqlite3; sys.path.insert(0,'scripts'); sys.path.insert(0,'scripts/assess')
import assess_cell as A
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
s = A.gather_sources(con, 3)
t45 = [r for r in s if r['tier'] in (4, 5)]; t6 = [r for r in s if r['tier'] == 6]
print(A.regulatory_richness(t45, t6))
print(A.regulatory_richness(t45 + [dict(tier=4, jurisdiction='INT')], t6))
print(A.regulatory_richness(t45, t6 + [dict(tier=6, jurisdiction='JP'),
                                       dict(tier=6, jurisdiction='FR')]))
PY
```

**The note that governs the reading.** Leg A alone reaching two jurisdictions flips this cell to
`provisional` with a Universal-Mode regulatory floor claim. That is a mechanical outcome of §2.3
and it is not an answer to the owner's question. §2.3's own falsification clause says it: *"It never
becomes a best-practice claim by more codes agreeing; only T1/Co-1/T2/Co-2 evidence can do that."*
A floor claim records what jurisdictions require. The threshold of acceptability — what a
wheelchair user can actually climb — is what REF-00989 speaks to and what Leg C's criterion names,
and neither reaches a determination while `gather_sources` gathers `claim` and `derived` only. That
gap is the owner's ACTION (2) of 2026-09-16, it is engine work rather than retrieval, and this
batch does not close it.
