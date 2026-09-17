# Batch 10 — the threshold of acceptability for ramp gradient (TERM-001, parameter 3) × MOB

**Session id:** `session_2026-09-17-research-batch-10-ramp-gradient-threshold`
**Branch:** `claude/batch-10-prep-04rjhv` · **PR** #141
**Cell:** `parameter_id 3` (TERM-001 `ramp gradient`) × identity lens `MOB`, slug
`accessible-circulation-geometry`

> **THIS RECORD IS CLOSED. THE BATCH RAN 2026-09-17.** It was prepared on branch
> `claude/batch-10-prep-04rjhv` (PR #141) and executed on `claude/research-preparation-joue00`
> (PR #143), after that session found and repaired the write path the batch runs on — `db.py
> log-search` could not accept a row at all. Four of the fourteen planned executions ran: Leg A
> rows 1–3 and Leg D row 11. Four sources admitted (REF-00990…REF-00993), six extractions, one
> Co-1 pass, one retrieval failure recorded as such. `research_batch_dod.py` reports COMPLIANT on
> all nineteen rules. The canonical DB moved exactly once, at the migration:
> `608626c7…` → `2db1d324…`. `sessions/LATEST` and `LATEST-RESEARCH` both move to this session,
> because it now holds research rows.
>
> **What did NOT run:** Leg B entirely (the four sold standards), Leg C (the Flemish dated
> carrier), and Leg D rows 12–14 (APF France Handicap, CERMI/ONCE, PVA). Those remain owed and
> are not deferred_reason material — they were simply not reached.

## Why this batch exists

The owner's statement of 2026-09-16 settles that dose-response evidence may be reasoned toward a
range as a **proxy**, and names the limit in the same breath: both admitted curves are monotonic
with no reported plateau, so "best outcomes therefore best range" resolves to 0°, which is not a
ramp. A ramp exists to change level, so the design question is the **maximum acceptable gradient**.
That needs a threshold of acceptability, and its ACTION (3) says where one comes from:

> The threshold half is a code value or an equivalent criterion, and `research_code_leads` names
> which documents to fetch but deliberately holds no values (2026-08-12 REFERENCE-ONLY ruling), so
> it must be retrieved.

`research_code_leads` 84 and 85 are those documents. Batch 10 retrieves them, together with the two
things batch 09 left explicitly owed that bear on the same question: the Flemish handbook's dated
carrier (candidate 69, which holds an acceptability *criterion* rather than a ceiling) and the
Co-1/Co-2 routes the general index did not reach.

## The correction this preparation starts from

**The batch-09 record's account of why the cell sits at `pending` is wrong, and designing against
it would have produced the wrong batch.** That record says `specification_id 3` is `pending` with
`refs=0` *"because `assess_cell.gather_sources()` gathers `figure_role IN ('claim','derived')` and
both Co-1 rows are `finding`"*. Measured on 2026-09-17 by calling the engine's own functions:

- `gather_sources(con, 3)` returns **two** rows, not zero — REF-00987 (T6, US, ADA 405.2) and
  REF-00988 (T5, DE, DGUV 6%), both graded `claim`.
- `regulatory_richness` on that set returns `(False, 'below §2.3 richness')`. One T5 and one T6
  clear none of the three clauses, so `determine()` never enters the branch that assigns
  `governing`, and `refs=0` follows from the unassigned variable.

The Co-1 findings genuinely do not reach the cell — that half is true, and the owner's ACTION (2)
about it is still owed. They are simply not the reason `refs=0`. The batch-09 record is corrected in
place in this change, with the struck clause left visible.

**The same error is in the corpus.** `research_code_leads` 84's note asserts *"Retrieve ONE
jurisdiction's ramp clause and the cell becomes determinable."* Against the measured richness rule
that is false for the most retrievable document class: a single new statutory code does not move the
cell. It is left uncorrected here on purpose — batch 10 retrieves the documents the lead names and
re-describes it from them under R15, and correcting it now on a probe and again after retrieval is
two writes where one will do.

## What was prepared

| Artifact | What it is |
|---|---|
| `scratchpad/pr-141-research-batch-10-threshold/PRIORS.md` | Six expectations, four surprises, six refusals. Committed before any query. |
| `scratchpad/pr-141-research-batch-10-threshold/QUERY-PLAN.md` | 14 executions in four legs, each with the prior that goes verbatim into `log-search --prior-expectation`. |
| `scratchpad/CURRENT` | Moved to this session's folder at OPEN, per the pointer trap. |
| this record | Open; closed when the batch runs. |

The two plan commits precede any execution in git history, which is what makes the R8 ordering
checkable rather than asserted — batch 09's own practice, and the reason it is done as two commits.

## The pre-state probe

```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/audit/research_batch_dod.py \
  --session session_2026-09-17-research-batch-10-ramp-gradient-threshold
```

Fires **exactly R1, R9a and R9b** and nothing else — `workplan/2026-09-10-batch-06-runbook.md`
Step 0's signature for an uncontaminated session id. `--selftest` passes 19/19 beforehand. Any
other rule firing on this id means it has been used; stop and pick another.

## The four legs, and what each is for

1. **Freely-published statutes** (JP e-Gov, FR Légifrance, GB Approved Document M, CA NBC, AU NCC).
   Government publishes law; standards bodies sell standards, so this is the only class expected to
   be reachable in full. `code` × `intrinsic` → T6 by `derive_tier`.
2. **The sold standards lead 84 names** (BS 8300-1, AS 1428.1, JIS T 9251, and ISO 21542 as the one
   T4 in reach). Expected to return catalogue pages, logged R14 **RETRIEVAL FAILURE** — never
   absence. Lead 84's JIS entry is additionally doubted on its face and the row is designed to
   correct the lead rather than to admit from it.
3. **The Flemish dated carrier**, by the route candidate 69 names for itself: the *Stedenbouwkundige
   verordening toegankelijkheid* Art. 19 as published. The handbook holds the acceptability
   criterion — *"Bij hellingen vormt de fysieke haalbaarheid van de (zelfstandige) rolstoelgebruiker
   het uitgangspunt"* — and is blocked on nothing but a date.
4. **The Co-1 leg** (DPI Japan, APF France Handicap, CERMI/ONCE, PVA), every one named in batch 09's
   Owed list as a target that exists and was not reached. R1 is not waivable here with
   `CO1-NOT-APPLICABLE`: the threshold is precisely what lived experience answers, and batch 09
   proved the Co-1 leg is reachable in Japanese.

## What execution will meet, recorded so it is not rediscovered

- **`add-source --pages` at admission is the only path to a page locator.** R3 reads
  `evidence_sources.pages`; `correct-source` takes no value flag and `amend-source` refuses
  bibliographic fields. This batch is clause-cited documents almost exclusively.
- **A relation `--quote` has no exemption.** `_write_relation_edge` calls `_verbatim(quote,
  from_ref_id)` and raises with no `exempt_reason` parameter (`scripts/db.py:4802`), unlike
  `--claim-text`, which `--verbatim-exempt` can ledger. A standard stating its figure against a
  named reference cannot be extracted unless the citing sentence itself was retrieved. AD M and the
  NCC both call up a sold standard by name, so this is likely to bite.
- **Log searches in admission-first order.** `log-search` refuses `--results-admitted` without
  `--admitted-ref-id` (H05) and `amend-search` takes only `--append-note`, so an admission decided
  after its search was logged is permanently edgeless. Batch 09 rebuilt its scratch to escape this.
- **Landing pages are not held identities.** One BSI or ISO catalogue address serves a standards
  family and resolves to many ref_ids; R9a is URL-aware and silent on those by design.

## The thing this batch will not do, stated before it can be claimed

Leg A reaching two jurisdictions flips this cell from `pending` to `provisional` with a
Universal-Mode regulatory floor claim. **That is a mechanical consequence of §2.3, not an answer to
the owner's question,** and §2.3's own falsification clause says so: *"It never becomes a
best-practice claim by more codes agreeing; only T1/Co-1/T2/Co-2 evidence can do that."* A floor
claim records what jurisdictions require. What a wheelchair user can actually climb is what
REF-00989 speaks to and what Leg C's criterion names, and neither reaches a determination while
`gather_sources` gathers `claim` and `derived` only. Closing that is the owner's ACTION (2) of
2026-09-16 — engine work, not retrieval — and batch 10 does not close it.

## Pre-state

```
sha256sum data/guidebook.db
```

~~`fdbb8612b5797c6ddcdc4660b6c35acf3564f3816cb2ef42ef269f98b559ec2f`~~ — **stale, and struck
2026-09-17.** Migration 085 (`085_column_vocabulary.sql`, one role one column name) landed hours
after this record was written and moved the blob to
`608626c70689b57573e897dae479f5fd1cb9d3fbe55e03b24766a82c24ec6bce`. A session trusting the recorded
string would have read a legitimate schema migration as contamination. **The instruction below is
what saved it, which is the reason it is written that way — re-derive the value now rather than
trusting either string in this paragraph, including the second one.**

Re-derive rather than trust that string. It must be unchanged when the batch begins, and must move
exactly once, at the migration.

## Addendum 2026-09-17 — the write path this batch needs was broken, and is repaired

The same migration that moved the sha broke `db.py log-search`, which is the only way R8 can be met
and the first command this batch runs. It raised `table search_executions has no column named
session`: 085 renamed that column to `created_by_session` and `executed_at` to `created_at`, and
both were spelled as string literals in the writer. `add-candidate` was broken identically
(`search_candidates.session`), which Leg C needs for candidate 69.

**Every gate was green over it.** 085's caller sweep was empirical — it ran the whole check battery
against a rebuilt DB — and no check WRITES a search execution, so nothing exercised the writer.
The repair and its falsifiable enforcement are recorded in
`sessions/session_2026-09-17-research-write-path-repair.md`; both commands are verified working
against a scratch copy. **Nothing in this batch's frame, priors or query plan changes** — the
richness table in `QUERY-PLAN.md` re-derives identically, and the pre-state probe still fires
exactly R1/R9a/R9b on this session id.

---

## What the batch found

### Row 1 — JP, the falsifiable row. **Prior partly falsified, and that is the result.**

Two of the three figures REF-00989 attributes to the Barrier-Free Law are confirmed in Cabinet
Order 379/2006 (`REF-00990`), Art. 19(2)(iv)ロ and (vii)ニ(2), which read
*勾配は、十二分の一を超えないこと。ただし、高さが十六センチメートル以下のものにあっては、八分の一を超えないこと。*

The third is not. **十五分の一 occurs ZERO times in the entire Cabinet Order.** It is in a
different instrument, retrieved in the same pass: MLIT Ordinance 114/2006 (`REF-00991`), the
**誘導基準** — the enhanced standard a building meets *voluntarily* to be certified — at
Art. 11(1)(vi)ロ, governing 敷地内の通路.

**So the corpus held a Co-1 assessment of "the legal figure" that silently merged two instruments
of different legal force.** 1/12 and 1/8 are mandatory; 1/15 is aspirational. REF-00989 calls 1/15
the outdoor figure: the domain is roughly right, the legal strength is not. **Nothing in Japanese
law requires 1/15 of anyone.** A determination built on the Co-1 reading would have overstated the
regulatory floor. The prior was also right that no warrant is stated — neither instrument gives any
basis for any figure.

### Row 2 — FR. **R14 RETRIEVAL FAILURE, not absence.**

Légifrance returns HTTP 403 to automated retrieval on every route (`/loda/id/`,
`/jorf/article_jo/`, `/jorf/id/`, `/download/pdf`), with a browser User-Agent. The ministry carrier
`accessibilite-batiment.fr` returns 200 but serves a byte-identical JS shell for every section. The
document was correctly identified on the first query; only the machine route is blocked. **Values
were seen through a reader tool and deliberately NOT filed** — a figure the corpus cannot check
against persisted bytes is the 2026-08-19 shape. Recorded as code lead 86, REFERENCE-ONLY.

### Row 3 — GB. **Prior confirmed, and the finding is structural.**

AD M (`REF-00992`) Table 1 does not state a ceiling; it conditions gradient on the **going** of a
flight: 10 m → 1:20, 5 m → 1:15, 2 m → 1:12, interpolating between. **The UK 1:12 buys 166 mm of
rise — about one step.** REF-00987 (ADA) and REF-00990 (JP) both state a flat 1:12 with no length
term in the same clause, so *a cross-jurisdiction table reading 1:12 = 1:12 = 1:12 would be false
three ways.* Filed as a claim at 1:20 with the 2 m row as a separate finding, so the engine cannot
gather the false convergence.

### Row 11 — JP Co-1. **Prior half right, and the half it got wrong matters.**

DPI Japan (`REF-00993`), a cross-disability DPO, assessing Japan against the CRPD Committee's 2022
Concluding Observations: *特に建物関係はバリアフリー法の義務基準が低く、移動等円滑化基準（義務基準）だけでは円滑な利用ができない* —
the mandatory standards are low against the IPC Accessibility Guide, and the mandatory standard
alone does not permit smooth use. **The people governed by REF-00990 say it is not enough.**

But the prior assumed a DPO commenting on the *gradient*. It does not: 勾配, スロープ and 傾斜 occur
**zero** times; the worked examples are toilets and parking bays. The extraction says so in its own
notes so no later reader over-reads it. **The gradient-specific Co-1 claim remains owed.**

## The thing this batch said it would not do, and did not do

Regulatory richness now clears — 3 T6 codes from 3 distinct jurisdictions (GB, JP, US). **That is
the mechanical consequence §2.3 predicted and not an answer to the owner's question**, and this
batch's own row 3 gives positive reason to distrust it: the engine's verdict says *"value-level
convergence unverified"*, and the AD M finding shows the apparent agreement at 1:12 is an artefact
of reading three differently-shaped rules as one number.

Determination 3 is **retired, not recomputed** (K02 fires correctly — `derivation_sha` hashes the
junction). Recomputing it would publish a regulatory floor claim as though it answered what a
wheelchair user can climb. Closing that gap is ACTION (2) of 2026-09-16 — engine work, not
retrieval — and it is still owed.

## What execution actually met, against what was predicted

The plan predicted the paywall casualties and got the mechanism right in one case and wrong in
another. It predicted `--quote` would bite on AD M — it did, and harder than expected: **no
extraction_relations edge involving AD M can ever exist**, because `--quote` has no exemption and
the PDF is compressed, so the 2 m row had to be filed as a `finding` rather than a `condition`.
Three write-path defects were found by running the batch and are repaired in PR #143: `add-source`
reporting a slug link it never wrote, the verbatim guard being unable to read CJK numerals (which
made *every* Japanese statutory value unfilable), and a refusal that fired after its own INSERT.

**Owed after this batch:** Leg B (four sold standards), Leg C (Flemish dated carrier), Leg D rows
12–14, the gradient-specific Co-1 claim, the IPC Accessibility Guide (candidate, named by
REF-00993 as its benchmark), the French arrêté (lead 86), and `update-code-lead` so R15 can be
discharged against lead 85 (GAP-005).
