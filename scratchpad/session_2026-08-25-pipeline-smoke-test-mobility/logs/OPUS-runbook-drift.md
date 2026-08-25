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
