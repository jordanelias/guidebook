# Batch 11 — the legs batch 10 did not reach, and the convergence that is real

**Session id:** `session_2026-09-17-research-batch-11-threshold-legs-bcd`
**Branch:** `claude/research-preparation-joue00` (restarted from main after PR #143 merged)
**Cell:** `parameter_id 3` (TERM-001 `ramp gradient`) × `MOB`, slug `accessible-circulation-geometry`

> **CLOSED.** Six searches, two sources admitted (`REF-00994`, `REF-00995`), three extractions,
> one candidate resolved, five registered. `research_batch_dod` COMPLIANT on all nineteen rules;
> `test_db_integrity` 71/71; `extraction_relations_integrity` CLEAN. Canonical DB moved once:
> `2db1d324…` → `8b6114fc…`. Priors were committed in `50c9b53`, before the first query ran.

## Order was reversed from batch 10, on purpose

Batch 10 followed its query plan and reached Co-1 last. **R1 says Co-1 first, no exceptions**, and
the contract outranks the plan. Co-1 ran first here. It also turned out to be the leg that yielded
nothing admissible — which is itself the finding, and which batch 10's ordering would have buried
again.

## What the Co-1 leg found: two well-formed zeroes, for different reasons

**PVA (US) — prior falsified.** I predicted PVA would restate the ADA 1:12. It publishes **no ramp
gradient guidance on its free surface at all**: three pages retrieved (HTTP 200, all persisted),
and across them `ramp` 0, `slope` 0, `gradient` 0, `1:12` 0. The image-guide page appears to hold
62 instances of "gradient"; **every one is a WordPress CSS preset**, checked individually rather
than trusted from a count. PVA's substantive guidance is in *Accessible Home Design, 2nd Edition* —
a sold book — and in a consultancy staffed by its own architects.

**APF France Handicap (FR) — prior confirmed on substance, wrong on mechanism.** Not a retrieval
failure: both pages returned 200. The content is simply rights-and-enforcement, not design
specification. `pente` 0, `rampe` 0. Its only numbers are Ifop survey statistics and a web-
accessibility score, each inspected individually — a bare "5 %" on a French accessibility page is
exactly what a careless pass files as a gradient.

> **France now has neither route.** Légifrance blocks the statutory text (batch 10, lead 86) and
> the national DPO does not publish the figure.

**The structural finding across both:** a major disabled-led organisation with on-staff architects
keeps its design expertise behind a book sale and a service. That is a reason Co-1 gradient
evidence is scarce, and **it is not the same thing as disabled people having no position on
gradient.** Registered as candidate 78, which is a purchase decision rather than another retrieval.

## The two admissions

### `REF-00994` — IPC Accessibility Guide, 4th ed. (T4, INT). **1:20 (5%) best practice.**

REF-00993 (DPI Japan) holds that Japan's mandatory standard is *low* against the IPC guide. This is
that guide, and **the complaint is now quantified**: IPC best practice is 1:20 (5%) where the
Japanese mandatory ceiling and the ADA both sit at 1:12 (8.33%) — a factor of 1.67. 1:14 (7.14%) is
accepted only for *secondary or ancillary* facilities. It states **no basis**: across 216 pages,
zero occurrences of "ISO", zero of "evidence", no named reference standard. It also defines a ramp
as usually having a running slope *greater than* 1:20 — below that it is a pathway.

### `REF-00995` — Besluit van de Vlaamse Regering, 5 juni 2009, art. 19 (T6, BE). **5% above 50 cm.**

The dated carrier candidate 69 named for itself. The table is confirmed band for band; **the
acceptability criterion is not in it** (`fysieke haalbaarheid` occurs zero times), exactly as batch
10 predicted — so candidate 69 resolves the table and leaves the criterion owed.

## The convergence that is real, against the one that was not

Batch 10 showed the three-way agreement at 1:12 to be an artefact of reading differently-shaped
rules as one number. This batch found the opposite case:

| Source | Governing figure for a full-height ramp |
|---|---|
| IPC Accessibility Guide (sports federation, international) | **1:20 (5%)** |
| Approved Document M (building regulator, GB) — 10 m flight | **1:20** |
| Flemish decree art. 19 (planning regulator, BE) — rise > 50 cm | **5%** |

Three bodies, no shared lineage, three different regulatory traditions, **one number**. Against
that, 8.3% appears in the Flemish table only for rises of 10–25 cm, and 1:8 in the Japanese order
only for rises ≤16 cm — the same short-rise-buys-steeper structure. **The ADA and Japanese flat
1:12 are the structural outlier: they permit 8.33% at any height.**

**And there is now a third rule shape.** US/JP condition on nothing, GB conditions on the *going*
of a flight, BE-VL conditions on the *rise* bridged — and the Flemish memorandum records that
switch as deliberate, away from the 1977 royal decree's length-based rule. No two of the three are
numerically comparable.

## Two documents caught contradicting themselves or the corpus

**Lead 84 is wrong.** It names `JIS T 9251:2014` against ramp gradient. The standard is
高齢者・障害者配慮設計指針－視覚障害者誘導用ブロック等の突起の形状・寸法及びその配列 — **the tactile
walking surface indicator standard**. Confirmed from the JSA's own preview PDF: 傾斜 0, 勾配 0,
スロープ 0. The [UNVERIFIED] recollection that prompted the row is now verified. **The correction
cannot be written to the lead** — no `update-code-lead` verb exists (GAP-005), so lead 84 keeps
telling the next reader that a tactile-paving standard carries a ramp gradient.

**The Flemish decree contradicts itself.** Its explanatory memorandum lists **five** gradient bands
including 7% for 25–35 cm; the normative article has **four** and merges 25–50 cm at 6.25%. A
researcher reading the *toelichting* — which sits above the article on the same official page —
would file a band that is not in force. Same shape as the REF-00989 error batch 10 found, this time
inside a single government document.

## Not done, and why

**The determination is still not recomputed.** Richness now clears on the strongest clause (≥1 T4
international present, via REF-00994) rather than on the weakest. That changes nothing: priors
refusal 3 committed in advance that clearing richness is mechanical and is not an answer to the
owner's question, and ACTION (2) of 2026-09-16 — letting Co-1 findings reach a cell — is engine
work that remains owed.

**Owed after this batch:** the Handboek acceptability criterion (candidate 79 — *the* highest-value
target left, and the only statement met anywhere in this corpus framed on what a wheelchair user
can physically do); ISO 21542 (candidate 80, now worth retrieving for *what it says* rather than to
unlock the cell); the West-Vlaanderen provincial rule (81); BS 8300 (82); the PVA book (78); CERMI/
ONCE and the DPI public comment, neither reached; and `update-code-lead` so lead 84 can be fixed.
