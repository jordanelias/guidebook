# OPUS — the runbook itself, audited against the repository it commands

Not delegated to a stage agent. CLAUDE.md's first instruction is *"Read
`decisions/DR-2026-08-19-research-restart-operative-instrument.md` first… It is RATIFIED and
operative: it carries the execution order, the runbook, and the acceptance criterion. It is meant
to be **run**, not consulted."* So the runbook is the pipeline's actual entry point, and nobody had
checked whether it still matches the code.

Method: extract every `scripts/**.py|.sh` path the instrument names and existence-check it; then
diff its §12.1 step-by-step instructions against the current `scripts/db.py` and
`scripts/tests/test_db_integrity.py`. All reads read-only; `data/guidebook.db` untouched.

---

## D-1 — Step 0 commands a script deleted five days ago (BLOCKING for the batch's first command)

`decisions/DR-2026-08-19-research-restart-operative-instrument.md:794`, inside **Step 0 — pre-state**:

```
python3 scripts/audit/table_connectivity.py                  # record 0 of 80
```

`scripts/audit/table_connectivity.py` does not exist. Deleted in `80a34d1`
*"governance: the cull, in its entirety — 6,716 LOC, 23 files, 15 registry entries [2026-08-20
19:45]"*.

The mobility batch's **first** step is a five-command pre-state block; the last of the five now
exits 127. The instrument carries no note of the retirement at that line.

Contrast with how the same instrument handles its *other* two removed scripts — both swept
correctly, in place:

- `scripts/audit/meta_work_freeze.py` — line 435 carries `**CORRECTION, same day:** that check has
  since been RETIRED and deleted.`
- `scripts/ci_helpers/check_doctrine_token.py` — line 602 records OD-10 item 4 removing it.

So the instrument's authors knew the sweep discipline and applied it twice. The cull of 2026-08-20
did not. **CLAUDE.md §0.4: "A rename or removal is not done until the callers are swept… A VIEW IS A
CALLER, and so is a skill."** A ratified runbook is a caller too — the one with the most readers.

## D-2 — Step 7 instructs the exact dual write the owner abolished on 2026-08-24 (rule 5)

`…instrument.md:861-864`, **Step 7 — admit**:

> Then, in one transaction: `UPDATE search_executions SET results_screened=…, results_admitted=…,
> **admitted_ref_ids='[…]'**`; `INSERT INTO search_admissions (exec_id, ref_id, …)`; … **The JSON
> array, the junction rows and the count must agree exactly (H03/H04/H05, blocking).**

Three things are now false at once:

1. **`admitted_ref_ids` is the dual home rule 5 exists to kill.** `scripts/db.py:394-396`:
   *"admitted_ref_ids intentionally NOT written — search_admissions is the sole home (owner ruling
   2026-08-24). Column retained because committed data migrations INSERT it and migrations are
   append-only."* And `scripts/db.py:409-416`: *"Until 2026-08-24 this dual-wrote the same fact…
   a parity check does not prevent that, it makes it survivable and therefore permanent. Nothing
   ever READ the JSON: it was write-only data guarded by a test."*
2. **H03/H04 are gone.** `scripts/tests/test_db_integrity.py:996`: *"H03/H04 DELETED 2026-08-24 —
   they policed a dual-write that no longer…"*. Only H05 survives
   (`test_db_integrity.py:1009`, "results_admitted equals the admission edge count"). The runbook
   cites two deleted checks as *blocking* justification for the write.
3. **The hand-SQL is unnecessary.** `db.py log-search` writes the junction itself
   (`scripts/db.py:428` `INSERT INTO search_admissions`) and takes `--admitted-ref-id`
   (repeatable), `--results-screened`, `--results-admitted`, refusing at `db.py:370-382` when the
   count disagrees with the id list or an id repeats. CLAUDE.md §4: *"Do not hand-write SQL against
   a table the CLI can reach."*

A session that runs the ratified runbook literally re-creates, by instruction, the redundancy the
codebase was changed to remove — and cites retired gates as its authority.

## D-3 — Step 4's "No CLI; scratch SQL" is stale (and teaches the fabrication-shaped habit)

`…instrument.md:830`: **"Step 4 — screen and stage (R7, R15). No CLI; scratch SQL."**

`scripts/db.py add-candidate` exists, with `--disposition` documented as *"Live vocabulary, derived
from the table; not a list in this file"* — i.e. the `dbcore.check_values()` discipline CLAUDE.md §4
requires, which hand-SQL cannot give you. ACT 2a/2b/2c (`9ed4664`, `5050256`, `fdb1623`) closed this
gap; the runbook still opens it.

Same shape at Step 7's *"the mandatory companion UPDATE, because `_ES_COLS` cannot carry these"*
(`doi_resolution_outcome`, `pages`, `url`). Measured: `db.py add-source` now accepts
`--doi-resolution-outcome`, `--pages`, `--url`, `--url-accessed`. CLAUDE.md §4 already states the
gap is closed and calls it *"the CAUSE, not the setting"* of the 2026-08-19 fabrication. **The
runbook is now the last document still teaching the cause.**

## D-4 — R8 ordering has no writer (unresolved, not merely stale)

Step 3 requires every query logged verbatim **before** screening, with
`results_screened`/`results_admitted` held at 0 until step 7. Step 7 then updates them.

There is no `update-search` / `update-execution` subcommand in `db.py` (full subcommand list
checked). `log_search` is an append-only `INSERT` (`db.py:405-407`), so re-logging fabricates a
second search row.

So the sanctioned path offers only two options, and R8 forbids one of them:

- log once **after** screening with final counts → violates R8's "log EVERY query verbatim BEFORE
  screening";
- log at 0, then hand-write the `UPDATE` → violates CLAUDE.md §4's no-hand-SQL rule and D-2 above.

Per CLAUDE.md §4, *"if you find [a table] the CLI cannot [reach], that is a coverage bug to fix, not
a licence to bypass."* This one is on the mandatory path of **every** admission in the mobility
batch, and it is the write H05 (blocking) audits.

---

## What this means for the mobility batch

The batch cannot be run from the instrument as written. Before it starts, four edits are owed to
`decisions/DR-2026-08-19-research-restart-operative-instrument.md` (lines 794, 830, 856-864) and one
coverage bug is owed to `scripts/db.py` (D-4). None is a doctrine change — every one of them is the
instrument catching up to rulings already made.

The pattern underneath is worth more than the four defects: **three of the four are the 2026-08-20
cull and the 2026-08-24 pointer-discipline ruling sweeping the code and not the runbook.** The
repository's own §0.4 predicts this exactly, and the runbook is the caller nobody greps for.

---

# PART 2 — the substrate the mobility batch would actually draw from

Same method: read-only queries against the committed DB, plus the enum and the validator that
claims to police jurisdictions. Prompted by the owner's stated plan — *"drawing from our first two
defined research buckets… using our clues table."* Both halves of that sentence turn out to be
mechanically blocked, for reasons no gate reports.

## D-5 — Bucket 1 and bucket 2 contain four jurisdictions the schema cannot represent

`schemas/enums.py::JurisdictionCode` has **27** members:
`AU BD BR CA CH CN DE DK EG EU FR ID IE IN ISO JP KE KR NG NL NO NZ SE SG UK US ZA`.

Buckets, from `workplan/2026-08-18-research-frame-proposal.md:422-424`:

| Bucket | Member not in the enum |
|---|---|
| 1 — UN · ISO · Canada · USA · UK · Germany · Norway · Sweden · Japan · Australia | **UN** |
| 2 — EU · Singapore · New Zealand · Ireland · France · **Spain** · **Portugal** · **Finland** · Netherlands · South Korea | **ES**, **PT**, **FI** |

A bucket-1 batch cannot record a UN instrument's jurisdiction; a bucket-2 batch cannot record
Spain, Portugal or Finland at all. The write would be refused (or, worse, coerced) at the point of
admission. This is decidable before the batch starts and is cheap to fix — but it must be an owner
decision, because jurisdiction inclusion is DG-NON doctrine (CLAUDE.md §1) and
`governance/jurisdiction-philosophy.md` §1.2 governs the canonical set.

## D-6 — `jurisdictional_values` holds 20 rows the project's own rule forbids, and the blocking check cannot see them

`scripts/validate_jurisdiction.py` implements the rule at two places —
`validate_jurisdiction.py:111-113` (`"Block {i+1}: 'GB' must be 'UK' per project convention"`) and
`validate_jurisdiction.py:182-184`. `GB` is correctly absent from the enum.

`jurisdictional_values` contains **20 rows with `jurisdiction='GB'`** — the third-largest
jurisdiction in the table, tied with DE and US.

They survive because **`validate_jurisdiction.py` never opens the database.** Its subjects are
`standards-registry.md` blocks and `data/sources/*.yaml`. Measured:

```
$ python3 scripts/validate_jurisdiction.py
PASS: 0 errors, 55 warnings
EXAMINED: 111
```

Blocking. Exit 0. `EXAMINED: 111` — a real, non-zero count, of the wrong subject.

**This is a third species of the CLAUDE.md §2(a) failure, and the most dangerous one.** §2(a)
guards against a gate that passes having examined *nothing*, and `run_checks.py` escalates
blocking-and-vacuous checks for exactly that. A gate that examines 111 of the wrong things defeats
that instrumentation completely: the count is honest, the check is green, and the data it is named
for has never been looked at. **`EXAMINED > 0` is not evidence that a check examined its subject.**

For the mobility batch this is direct: a `UK` query for corridor-width or ramp-gradient code values
silently misses 20 `GB` rows, and nothing anywhere reports the split.

## D-7 — No registered check reads `source_locators.jurisdiction`, and 818 of 875 values are not jurisdictions

Of 63 registered checks, exactly two open `source_locators` at all
(`scripts/audit/research_batch_dod.py`, `scripts/audit/validate_pydantic_schemas.py`) and neither
validates its `jurisdiction` column. What that column holds, measured over all 875 rows:

| Content | Rows | Example |
|---|---|---|
| `NULL` | 385 | |
| `'—'` (literal em dash) | 89 | |
| **a URL** | **154** | `REF-00095` → `https://www.abcb.gov.au/ncc` |
| **a slug name** | **67** | `REF-00057` → `mental-health-built-environment` |
| a jurisdiction-shaped code | 57 | incl. `MOHO`, which is not a jurisdiction |

**Bucket 1 filter returns 23 rows. Bucket 2 returns 5.** The clue store cannot be queried the way
the batch plan proposes to query it — not because the leads are missing, but because the selector
column holds four different kinds of thing.

Separately: 64 distinct clue-store leads match mobility keywords in `title` (corridor, doorway,
threshold, ramp, slope, floor, handrail, stair, wheelchair, mobility, gait, slip…). The leads
exist. The index over them does not.

## D-8 — Citation mining works, and then drops 134 of its 138 leads on the floor

This is the one that most directly threatens the owner's plan, because mining is *supposed* to be
what fills the clue store.

`citation_mining` holds 10 rows, all on `room-acoustic-performance`, and they are real work:
`backward=1` on 7, `forward=1` on all 10, with harvested DOIs in `connections_produced`. R2 is
being honoured. But `connections_produced` is a **JSON array inside a TEXT column**, and:

```
distinct DOIs harvested by mining : 138
present in source_locators (clue store) : 4
NOT in the clue store : 134
```

**97% of the yield of every backward and forward mining pass this project has run is stranded in a
JSON blob that no downstream stage reads.** The mining engine runs; its output never becomes a lead.

Note the exact shape: this is not a missing capability, it is a missing *edge*. Backward and forward
mining both execute and both record their harvest. What does not exist is the step that promotes a
harvested DOI into `source_locators` where R9 de-duplication, R10 re-retrieval and the next batch's
frame can reach it. Until that edge exists, "we would be using our clues table" and "we would mine
citations" are two disconnected activities.

## The good news, stated as plainly as the defects

- **29 `jurisdictional_values` rows already exist on mobility items** — `E-01` lift ×7, `E-03` ramp
  gradient ×8, `E-08` corridor clear width ×7, `G-04` wet room ×7. Correctly REFERENCE-ONLY:
  `value_text` and `value_numeric` are 0 non-null across all 109 rows, exactly as the 2026-08-12
  ruling requires. The batch starts with a real, doctrinally-clean lead set on four of its items.
- **All 10 admitted sources have a complete stage-1→stage-2 walk**: 1 slug link, 2–3 population
  matches, 1 search admission, and a mining row each. Research and evidence collection are not
  theoretical here; they have been run and they hold.

---

# PART 3 — the freeze that released on the wrong condition, and 256 mobility leads nobody can see

## D-9 — The apparatus freeze expired on a weaker condition than the one it was written with

The instrument's §2.2 froze new apparatus **"Until `evidence_sources` holds at least one admitted
source with a complete walk."** Its §5 states the freeze **"expires by its own terms the moment
`evidence_sources` is non-empty."** Those are not the same condition, and the enforcing check
implemented the second: `…instrument.md:435-441` records `meta_work_freeze` as retired because
*"its exit condition `evidence_sources >= 1` was met when the first batch landed."*

Measured today:

| | |
|---|---|
| `evidence_sources` | **10** — freeze released |
| `specifications` | **0** |
| `source_value_extractions` | **0** |
| `bpc_metadata` / `item_bpc_links` | **0** / **0** |
| `convergence_assessment` | **0** |

Not one walk is complete. All ten sources stop at the same place: each has 1 slug link, 2–3
population matches, 1 search admission and a mining row — and then nothing. **The gate released on
row-count in the first evidence table while §4's actual acceptance criterion — "One answered
question, published… rendered and readable as output, not as a row count and not as a green
check" — remains unmet.**

This is the cleanest available explanation of why apparatus work resumed immediately (ACTs 1–6 and
a consolidation plan on 2026-08-25 alone) and it is not a discipline failure by any session: **the
freeze's own release clause was satisfiable by exactly the kind of row-count success §4 was written
to reject.** The instrument diagnosed the loop precisely and then handed it a door.

*This is a finding, not a recommendation to re-freeze.* Whether the freeze should return is DG-NON
doctrine and the owner's call. What the smoke test establishes is that it will not return by itself,
and that "evidence_sources ≥ 1" must never again be used as a proxy for a walk.

## D-10 — 256 already-mined mobility leads are sitting in a directory ripgrep cannot see

The instrument's own §6 records the shape of this — *"~4,081 distinct DOIs are recoverable across
the repository. 397 are in the live `source_locators` store — under 10%… `sessions/` is hidden from
ripgrep by the root `.ignore`, so two-thirds of this project's identifier capital has been invisible
to every session that searched for it."* Nobody had measured the **mobility** slice. I did:

```
sessions/artifacts/2026-05-24-b11-mobility-backward-discoveries.json     89 DOIs
sessions/artifacts/2026-05-24-b11-mobility-forward-discoveries.json     184 DOIs
                                              distinct, combined:      272
   already in source_locators (the clue store):                         16
   already admitted (evidence_sources):                                  0
   NEW — in neither:                                                   256
```

Keyed by anchor: `MOB-01`, `MOB-02`, `MOB-05`, `MOB-10`, `MOB-11`, `MOB-12`. Record shape:

```json
{ "doi": "10.1080/17483107.2022.2111723", "year": 2022, "first_author": "Kapsalis",
  "title_short": "Disabled-by-design: effects of inaccessible urban public spaces on users of
                  mobility assistive devices – a systematic re", "in_evidence_sources": false }
```

Field coverage over the 319 mobility records: **291 carry `year`, 215 carry `first_author`, 0 carry
a full `title` or `authors`** — `title_short` is truncated mid-word, as the sample shows.

Three consequences for the batch, in order:

1. **The backward-and-forward citation mining the owner asked to test has already been run on
   mobility, in May 2026.** The anchor blocks carry `openalex_id`, `openalex_cited_by_count`,
   `citers_fetched`, `relevant_n`, `already_in_es_n`, `new_discovery_n` — a real forward-citation
   pass via OpenAlex, with its yield counted. The capability existed and was exercised.
2. **Its output never reached the clue store** — 16 of 272. This is D-8's stranded-yield defect
   again, one layer further out: mining harvests into artifacts and JSON columns, and nothing
   promotes a harvest into `source_locators` where R9, R10 and the next frame can reach it.
3. **`title_short` must never be promoted as `title`.** It is truncated. CLAUDE.md §2(c) — *"Never
   write a bibliographic field from memory when a payload is in hand"* — extends straightforwardly:
   never write one from a field you can see is truncated. The DOI, year and first-author are
   legitimate lead data; the title requires R10 re-retrieval. `source_locators` is defined as *"a
   lead index of identifiers, not evidence"*, so promoting identifiers is exactly its purpose.

**The single highest-value pre-batch action available is promoting those 256 leads into the clue
store** — with `doi`, `pub_year`, `authors` (first author only, marked), `recovered_from` naming the
artifact, `status='REFERENCE-ONLY'`, and `title` left NULL pending re-retrieval. That is one
migration, it adds no apparatus, and it turns "we would be using our clues table" from 64
keyword-matched leads into 320.

---

# PART 4 — found by being caught: the local gate does not predict CI

Not planned. This session's own commit `d4042e6` failed the blocking `attestation_presence` check
on CI while the local battery reported `PASS` on the identical sha. The gate was right — `sessions/`
is a synthesis path (CLAUDE.md §0.2) and I owed an attestation. What is worth recording is the
disagreement, because CLAUDE.md §5 instructs every session to gate its diff locally before pushing.

## D-11 — The attestation battery's window is one commit locally and the whole branch on CI

| | Local | CI |
|---|---|---|
| command | `run_checks.py --battery attestation --changed-from origin/main` | `run_checks.py --battery attestation --kinds … --github` |
| reported | `changed files:` *(absent)* → `[NONE] attestation_presence` → **PASS** | `changed files: 11; synthesis: 1` → `[FAIL] attestation_presence` → **FAIL** |

Mechanism, in three facts:

1. `scripts/audit/adherence_log_audit.py:569` — `--base` defaults to **`HEAD~1`**.
2. `governance/check-registry.yaml` invokes it with **no base**:
   `['python3','scripts/audit/adherence_log_audit.py','--check','presence']`. `run_checks.py`
   computes `changed_paths(base)` at `run_checks.py:147-161` for *selection* and never passes that
   base to the check it selected.
3. `.github/workflows/ci.yml:220-221` checks out with `fetch-depth: 0`. On a pull request that
   checkout resolves to the **merge ref**, whose `HEAD~1` is the base-branch tip — so `HEAD~1..HEAD`
   is the entire PR. In a local clone `HEAD~1` is simply the previous commit.

So the same default means two different things. The attestation gate audits **the last commit**
locally and **the whole branch** on CI. Any session that touches a synthesis path in one commit and
then makes a second commit gets a green local battery and a red CI — which is exactly the sequence
that produced this failure.

`.github/workflows/ci.yml:213-218` shows the risk was reasoned about and half-caught: the comment
justifies `fetch-depth: 0` precisely because *"a shallow checkout would scope the attestation gates
to nothing — a gate examining zero subjects while reporting PASS is this repo's signature failure."*
The fix is correct for CI and does nothing for the local path, where the same vacuity is reachable
by the ordinary act of making a second commit.

**Add this to the vacuous-gate family as a third species.** The census so far:

| Species | Example | Why the instrumentation misses it |
|---|---|---|
| Empty subject | 4 blocking checks reported `BLOCKING and vacuous` in this session's own run | Caught — `run_checks.py` escalates it by design |
| Wrong subject | `validate_jurisdiction`, `EXAMINED: 111`, never opens the DB (D-6) | `EXAMINED > 0` reads as coverage |
| Wrong window | `attestation_presence`, green locally, red on CI (D-11) | The count is right for the window; the window is wrong |

Only the first is instrumented. **`EXAMINED` answers "how many?" and never "of what?" or "over what
range?"** — and the two uninstrumented species are both live in this repository today.

*Smallest honest fix for D-11:* give the registry entry an explicit base, or have `run_checks.py`
pass its computed `--changed-from` base to checks that accept one. That is a code change, not
doctrine, and CLAUDE.md §1 says code needs evidence, not permission — the evidence is this PR.

---

# PART 5 — verifying the agents: one claim refined, one sharpened, one of my own withdrawn

## D-12 — "never assessed" and "assessed as partial" are the same grade, and both anchor

S3 reported that a cell reached `state='stated'` with none of its six governing sources assessed
for population applicability, and attributed it to `anchoring()` not excluding `COND_DOWN_WEIGHTED`.
The direction is right; the mechanism needs correcting, and the corrected version is the more
interesting finding.

**I first thought the bug was worse than S3 said, and I was wrong.** `schemas/directness.py:225`
reads `pop_full = population_directness in (POP_EXACT, None)` — `None` counted as a full population
match — which would mean an ungraded source anchors at full strength, exactly the thing R13 names:
*"No match row = silently claiming they are the same."* But `assess_cell.py:191-195` never passes
`None`:

```python
mg = population_match(conn, src["ref_id"], population)
if mg is not None:
    pop = population_directness_from_match_grade(mg)
else:
    pop = NOT_ASSESSED  # G2: applies but unassessed — never graded as EXACT
```

Guard G2 exists precisely to stop that collapse, and it works. **The `None`-is-full-match branch in
`consolidate()` is a latent hazard for any future caller, not a live defect.** Withdrawn as a
finding against the judgment stage; recorded here so the next reader does not re-raise it.

**What is live is one layer down.** `NOT_ASSESSED` is not in `ALL_POP_DIRECTNESS`
(`directness.py:98` = `{EXACT, PARTIAL, PROXY, MISMATCH}`), so at `directness.py:225-234` it fails
`pop_full` and falls to the same `return COND_DOWN_WEIGHTED` as `PARTIAL` and `PROXY`. Then
`assess_cell.py:248-250`:

```python
def anchoring(recs):
    """A source anchors only if its conditioning permits (§1.7): never NON-ANCHORING/DISCOUNTED."""
    return [r for r in recs if r["conditioning"] not in (COND_NON_ANCHORING, COND_DISCOUNTED)]
```

`COND_DOWN_WEIGHTED` anchors. And `down_weighted` (`assess_cell.py:298`) is used only to populate
the `down_weighted_sources` column of the record (`:353`, `:363`, `:460`) — **it never enters the
state decision.** So:

| Source's population standing | Conditioning | Anchors? | Distinguishable downstream? |
|---|---|---|---|
| Graded `EXACT` | `DIRECT` | yes | yes |
| Graded `PARTIAL` / `PROXY` | `DOWN-WEIGHTED` | **yes** | only in a record column |
| **Never graded at all** | `DOWN-WEIGHTED` | **yes** | only in a record column |
| Graded `MISMATCH` | `DISCOUNTED` | no | yes |

**"We looked and it partly fits" and "we never looked" produce identical anchoring behaviour.**
R13's warning is defended at the grading layer by G2 and then given up at the anchoring layer.

This is not a coding error — `anchoring()`'s docstring cites evidence-architecture §1.7 and
implements it exactly. It is a **doctrinal gap**: §1.7 was written about sources whose applicability
was *assessed and found partial*, and the same rule now silently governs sources whose applicability
was *never assessed*. Whether an unassessed source may anchor a `stated` cell is a judgement about
the book, so it is DG-NON and the owner's (CLAUDE.md §1). Naming it is mine.

For the mobility batch this is not hypothetical: `evidence_population_match` holds 25 rows against
10 sources on a single non-mobility slug. Every mobility source admitted in the coming batch begins
life `NOT_ASSESSED` — and, on today's rules, anchoring.

## D-13 — the fabrication proofing works, and the gates around it do not agree with it

S2 admitted a real mobility source end to end — Sanford, Story & Jones 1997, *Ramp Slope on People
with Mobility Impairments*, `10.1080/10400435.1997.10132293` — retrieved through
`retrieval_log.fetch()` with a byte-identical sha256 to an independent `curl`, and `--verify-authors`
returned CLEAN. **The specific machinery built after the 2026-08-19 fabrication does what it was
built to do.** That deserves to be said first and plainly, because it is the one part of this
pipeline that was designed in response to a real failure and then tested against one.

What it does not do is get that honest source through the pipeline's own downstream gates. On its
first write, three separate defects fire, none about sourcing honesty:

1. `evidence_sources.scope` has **no CLI writer** — no `--scope` flag, excluded from the column
   whitelist — so every `clinical` / `standard_eb` admission fails `adjudication_integrity.py`'s
   tier derivation.
2. `--verification-status VERIFIED` never sets `verification_disposition='CLOSED'` and no flag
   exists to set it, so every VERIFIED source fails **blocking** `test_db_integrity` check I1.
3. `--evidence-type` enforces no vocabulary, while the correct 8-value list already sits at
   `scripts/db.py:1223` serving a sibling command.

So a session that follows CLAUDE.md §4 exactly, sources honestly, and re-retrieves every locator
still needs a hand-written correction to pass CI on its first admission — which is precisely the
condition that produced the hand-SQL habit CLAUDE.md §4 now forbids. **The write path was closed
against fabrication and not re-opened against its own gates.**

S2 also reproduced **OD-5** directly rather than by reading about it: `add-source`'s DOI dedup
checks only `evidence_sources`, so a DOI already held as a lead in the 875-row clue store was
admitted under a second identity with no warning — while `add-locator`'s dedup correctly checks
both tables. The fix is asymmetric, and the unfixed half is the one on the admission path.

---

# PART 6 — the guard against rule 3, and an apparent contradiction that is not one

## D-14 — `is_canonical()` exists to enforce CLAUDE.md rule 3 and nothing calls it

CLAUDE.md §0.3 is the repository's hardest rule: **"Never write `data/guidebook.db` directly.
Migrations only."** `scripts/dbcore.py:65-74` implements the guard, and its docstring states the
purpose exactly:

```python
def is_canonical(path=None) -> bool:
    """True when the given path IS the committed database.

    Callers that must never touch the canonical file (CLAUDE.md rule 3: migrations
    only) use this to refuse, rather than trusting that GUIDEBOOK_DB_PATH was set.
    """
```

*"rather than trusting that GUIDEBOOK_DB_PATH was set."* That is the correct design, and the
correct reason. **Its only two callers are its own selftest** (`dbcore.py:438-439`). `connect()`
(`dbcore.py:83-101`) — the single door every `db.py` writer goes through since ACT 1 —
never calls it, and `db_path()` (`dbcore.py:51-59`) **defaults to the canonical file when
`GUIDEBOOK_DB_PATH` is unset.**

So the sequence is: forget the inline prefix on one call → `db_path()` returns the canonical file →
`connect()` opens it read-write → the write lands. No refusal fires.

This is not a hypothetical. It is failure mode **#1** in the instrument's own list
(`…instrument.md` §12.4): *"A `db.py` call lands on canonical — env resets between shell calls…
prefix inline; sha256 after every phase."* The mitigation offered is discipline plus a checksum
**after** the fact. The mechanical refusal was written, and left unwired.

**And two skills instruct the canonical path directly**, on write commands:

| Skill | Line | Command |
|---|---|---|
| `connection-auditor_SKILL.md` | 185, 192 | `db.py update-connection` |
| `connection-auditor_SKILL.md` | 199 | `db.py add-gap` |
| `connection-discovery_SKILL.md` | 219 | `db.py add-connection` |

all prefixed `GUIDEBOOK_DB_PATH=data/guidebook.db`. (Both files carry further occurrences on read
commands — `connections`, `next-id` — which are harmless now that `connect()` no longer sets
`journal_mode`, but they teach the habit.) An agent following these skills as written performs a
direct canonical write, and the guard designed to stop it is inert.

**This is the single most consequential defect the smoke test found**, because it is the one that
can silently destroy the append-only migration ledger that everything else in this repository
depends on. It needs no owner decision: CLAUDE.md §1 says code needs *evidence*, not permission, and
the evidence is `dbcore.py:438-439` being the entire caller list.

## D-15 — S1 and S2 appear to contradict each other on OD-5. They do not; they name different layers

S1 reports CLAUDE.md §4's OD-5 note ("the R9 duplicate gate currently cannot see `source_locators`")
is **stale**. S2 reports it **reproduced OD-5 live**, admitting a DOI already held as a lead with no
warning. Both are correct, and the reconciliation is the finding:

- **The gate sees it.** `scripts/audit/research_batch_dod.py:445-504` — R9a/R9b, added 2026-08-23 —
  join `source_locators` on DOI and on `ref_id` across six identifier types, and pass on the
  canonical DB today. `:445` even carries the note *"R9 above compares evidence_sources against
  ITSELF."*
- **The writer does not.** `scripts/db.py:1992-2000`, inside `add-source`:
  `SELECT ref_id FROM evidence_sources WHERE doi = ? AND COALESCE(superseded_by_ref_id,'') = ''`.
  `source_locators` is not in that query. `add-locator` (`db.py:2505-2508`) checks both.

So a duplicate against the clue store is **caught after it lands, by the definition-of-done gate,
rather than refused at write time.** That is precisely the arrangement `db.py` condemns in its own
comments (`db.py:362-368`): *"A gate that catches a bad write after it lands is strictly worse than
a write path that cannot make it."*

**Two corrections follow, one to the repository and one to CLAUDE.md.** CLAUDE.md §4's OD-5
sentence should be narrowed — the gate half closed on 2026-08-23. And the writer half is a
coverage bug of exactly the kind §4 tells you to fix rather than bypass. For the mobility batch this
is live and near-certain: 256 mobility DOIs are about to be promoted into the clue store (D-10), and
the very next `add-source` for a mobility slug will be checking for duplicates against the one table
that does not hold them.

---

# PART 7 — the reasoning document: S4's count corrected in both directions

S4 reported *"7 of 11 citations in the repo's only real reasoning doc cite `source_locators`-only
(unadmitted) sources as flat Tier-1/Tier-3 evidence."* The underlying finding is real and serious.
The count is wrong in both directions, and the correction matters because it changes what the defect
IS.

## D-16 — 8 of 11 are unadmitted; but one is flagged impeccably and five are not flagged at all

`references/bpc-reasoning/room-acoustic-performance.md` cites 11 distinct `REF-` ids. Checked
against the live DB:

```
admitted (evidence_sources) : 3   — REF-00325, REF-00561, REF-00578
leads only (source_locators): 8   — REF-00335, -00571, -00576, -00577, -00580, -00589, -00726, -00727
```

So **8**, not 7. But "flat Tier-1/Tier-3" does not survive contact with the text. Counting, per ref,
lines that carry a caveat token (`ineligible` / `pending` / `AUTHOR-TITLE-ONLY` / `rule-#10` /
`citation-miner pickup`) against lines that carry a tier label:

| ref | mentions | caveat lines | tier-labelled lines | reading |
|---|---|---|---|---|
| REF-00335 | 4 | **3** | 0 | **flagged correctly** |
| REF-00571 | 3 | 1 | 2 | mixed |
| REF-00576 | 2 | 0 | 2 | tier-labelled, unflagged |
| REF-00577 | 2 | 0 | 2 | tier-labelled, unflagged |
| REF-00589 | 2 | 0 | 2 | tier-labelled, unflagged |
| REF-00726 | 3 | 0 | 2 | tier-labelled, unflagged |
| REF-00727 | 4 | 0 | 2 | tier-labelled, unflagged |
| REF-00580 | 1 | 0 | 0 | passing mention |

**REF-00335 is the counter-example and it deserves to be read.** The document says of it:
*"pending citation-miner pass for rule-#10 eligibility"*, and later *"Co-supporting source REF-00335
(ANSI/ASA S12.60-2010) is AUTHOR-TITLE-ONLY and rule-#10-ineligible; logged for citation-miner
pickup."* That is the discipline working exactly as designed, written down, three times.

**And five refs in the same document get no such treatment.** REF-00726 and REF-00727 are cited as
`T1 review` and `T1 primary` and carry specific quantified claims — *"documented attentional
decrement for autistic participants at 55 dB(A) background where TD participants showed none"* —
with nothing marking them as never-admitted.

## Why the corrected version is the worse finding, not the milder one

If all eight were unflagged, the diagnosis would be "an author who did not know the rule." What the
document actually shows is **an author who knew the rule, applied it explicitly to one source, and
did not apply it to five others in the same file.** That is not ignorance; it is the predicted
behaviour of a rule enforced by attention rather than by machine — CLAUDE.md's opening argument
about why hooks exist: *"an agent must choose to load it, and attention degrades as context fills."*

And nothing mechanical can tell the two apart. `reasoning_doc_citations` — the table built for
precisely this cross-check, with `source_ref_id`, `claimed_value`, `value_match`, `claim_match`,
`source_section` — holds **0 rows**, and `scripts/audit/reasoning_doc_citations_audit.py` reports:

```
Total rows: 0
Table is empty (Phase E.1 has not begun for any BPC). No claim-level audit possible yet.
EXAMINED: 0
```

The verification apparatus is complete, correct, and empty. The document it exists to check is the
project's only real synthesis, and it is the §2(c) failure class — a confident citation nothing
verified — displaced one stage downstream from where §2(c) caught it in 2026-08-19.

**For the mobility batch this is the most likely way the whole thing goes wrong.** 256 mobility
leads are about to enter the clue store (D-10). Leads are cheap, plentiful, and carry `title`,
`pub_year` and `authors` fields that read exactly like evidence. The one existing reasoning document
demonstrates that a careful author, writing about a slug with real admitted evidence, still cited
five leads as tiered sources. A mobility synthesis drawing on a clue store 25× larger, with *no*
admitted mobility evidence to anchor it, will face that temptation on every claim.

*The smallest thing that would prevent it:* `reasoning_doc_citations` needs a CLI writer (S4 reports
it has none, and its skill teaches raw SQL), and the audit needs to read the document's `REF-` ids
directly rather than waiting for a table nobody can populate through the sanctioned path.
