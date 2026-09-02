# session_2026-09-01-research-batch-04-accessible-circulation

**Written late, on 2026-09-02.** The migration ledger has named this record since
`data_20260901205639` was applied and it did not exist. `emit_data_migration.py` does not
verify that a named session record exists, so nothing objected. That is defect **A-08 /
D04-025** and this file closes it.

**Outcome: the batch was researched and then NOT written.** No evidence row survives it.
What survives is material — two agonist briefs, 58 retrieval payloads, ~30 logged queries
in prose — and three corrections this record exists to make.

---

## 1. The correction that matters most: I misread §1.4, and then I broke it

Commit `befaa29` and the PR body both state:

> *"DR-2026-08-19 §1.4 wrote a quarantine for exactly this and never ran it — measured
> today, all 93 items were status=active and slugs.status=PROVISIONAL held zero rows. A
> rhetorical demotion left the containers standing."*

**§1.4 does not say that.** It is six CONDUCT rules for future sessions. It never
prescribes a change to `items.status`. Its rule 3 applies `PROVISIONAL` to *item-derived
slugs* and records *"zero rows currently use it"* as its own stated **baseline** — so zero
PROVISIONAL rows is consistent with the protocol having been **obeyed**, not evidence it
was skipped. The measurements were true; the inference drawn from them was not.

**And two of its rules bound this session:**

> **Rule 1.** *"A slug is authored from the ICF/access-need frame first; the item list may
> then be consulted to check coverage … never to supply one."*
> **Rule 2.** *"No value crosses. No numeric, dimension, threshold, range, or prescriptive
> clause from an item name … may appear in a `search_executions` row, a
> `search_candidates` row, an admitted source's fields, or a determination."*

`FRAME.md` was derived from `items`. Item values reached agonist queries — agonist-1 #8
carried *"22 newtons"* (I-01's "≤22 N"), agonist-2 #6 carried *"pendulum test value slip
resistance"* (E-07's "PTV ≥36"). **§1.4 was live and this session broke it**, then
described the breach as the instrument's failure.

**§1.4 rule 4 requires this be recorded, not hidden:** *"Provenance is recorded, not
hidden … The lead is auditable precisely so that a later reader can test whether it
anchored the result."* The crossings above are that record.

**The mitigating fact, which is real but smaller than the breach.** §12.1 step 2 of the
*same instrument* ordered the frame pulled from `items` — so the runbook and the
quarantine contradicted each other, and obeying one broke the other. That contradiction is
now resolved: the owner struck step 2 on 2026-09-02 (**D-0187**) and replaced it with an
ICF-first pull. It is an explanation of how the breach happened. It is not an excuse for
reporting the breach as a discovery.

## 2. "147 preserved DOI leads" is false

`citation_mining.connections_produced` holds **147 entries**, but **138 distinct** DOIs, of
which **134** are not already in `source_locators`. The 147 figure appears in commit
`befaa29`, in the PR body, and in the header of an immutable migration where it cannot be
edited. CLAUDE.md §2(b) — prose contradicting the database.

## 3. Smaller corrections

| Claim as committed | Truth |
|---|---|
| "one [DOI] under five" ref_ids | **two** are |
| the 08-31 command log "the prior session left untracked" | every line carried THIS session's id; this session misfiled it |
| REF-00037 carries "a third, different DOI" | a **second** |
| `empty-by-decision` "used by three checks" | **eleven** on main |
| "applying five owner rulings" | **four**; R-05 was recorded, not executed |
| "27 author rows in byline order" | NFBUK has no byline; `Bates\|David M` is credited **Editor** in the payload |
| "38,720 ED visits" | *"an **estimated** 38,720 ED weighted visits"* |
| "eight admissions", "~30 logged queries" | 8 `evidence_sources` + 27 author rows + 8 slug links. **Zero `search_executions`, zero `search_admissions`** were ever written; the queries exist only in markdown |

## 4. What the session did produce

- **The item-layer contamination was surfaced and ruled on.** Whatever the misreading, the
  owner's ruling of 2026-09-01 followed from what this batch demonstrated.
- **A corrupted identifier stash**: 32 DOIs under two or more `ref_id`s, with `doi` columns
  misaligned against bibliographic columns. It falsely blocked one clean admission.
- **Two agonists disclosed their own errors** — a guessed DOI that resolved to a different
  paper (payload kept, renamed `ERROR-NOT-A-SOURCE_*`), and a tool inventing a fifth author
  for Geoerg 2019, refuted against three independent payloads.
- **A defect register of 32 entries**, of which 14 came from the adversarial pass.

## 5. Pointers

`sessions/LATEST` moves to the 2026-09-02 record. **`LATEST-RESEARCH` does NOT move.** No
research reached the database, so pointing the blocking citation-mining gate at this
session would scope it to nothing and pass green — §7 trap 2, which this repository has
produced four times.
