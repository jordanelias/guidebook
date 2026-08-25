# Making the walk walk — the code-only repair plan

**Scope:** code and wiring only. Every item here passes CLAUDE.md §1's test — *"Code, checks,
scripts, dead tables and views: delete them. No owner gate. You need evidence, not permission."*
Nothing in this plan is doctrine, content, population taxonomy, jurisdiction inclusion, or item
identity. Those are tracked separately (`WAVE-H-SCOPE.md`, and the four DG-NON items in the session
record); two of the four are now ruled.

**Deliberately not in `workplan/`.** The standing 2026-08-19 RULE says a commissioned pass "may not
create or modify a workplan". This is the session scratchpad instead. It is a repair list, not a
plan-instrument, and it self-retires when the last box is ticked.

**Organised by EDGE, not by stage.** The owner's framing — *"walking properly in all directions"* —
is the correct one: this pipeline re-enters stages (`pipeline-map.yaml`, 2026-08-21), so a stage
that "works" in isolation can still leave the walk unable to come back round. The backward edges in
Phase 2 are where the worst of it is, and none of them appeared in the row counts.

---

## Phase 0 — Safety. Nothing else runs until this lands.

| # | Defect | Fix | Evidence |
|---|---|---|---|
| **P0.1** | `dbcore.is_canonical()` exists solely to refuse writes to the committed DB. Its only callers are its own selftest. `connect()` never calls it; `db_path()` **defaults to canonical** when `GUIDEBOOK_DB_PATH` is unset. | Call `is_canonical()` inside `connect()` and refuse a read-write open of the canonical file unless an explicit override is passed (migrations need one). | `dbcore.py:65-74`, `:83-101`, `:438-439` |
| **P0.2** | Two skills instruct `GUIDEBOOK_DB_PATH=data/guidebook.db` on **write** commands. | Repoint to a scratch path. | `connection-auditor_SKILL.md:185,192,199` · `connection-discovery_SKILL.md:219` |

This is failure mode **#1** in the instrument's own §12.4 list, with its written mitigation unwired.
It is the only defect here that can silently destroy the append-only ledger everything else rests
on. It is also perhaps two hours of work.

---

## Phase 1 — The forward walk: make one mobility cell reachable end to end

Ordered by dependency, not severity. Each unblocks the next.

**P1.1 — `add-source` cannot make an honest admission.**
Four gaps, one file: no `--scope` flag (column unreachable); `--verification-status VERIFIED` never
sets `verification_disposition='CLOSED'`, so every admission fails blocking `test_db_integrity` I1;
`--evidence-type` enforces no vocabulary though the correct list already sits at `db.py:1223`; and
R9 dedup checks `evidence_sources` only, not the clue store (`db.py:1992-2000`), while
`add-locator` checks both. *Must precede P2.1 — promoting 256 leads into a store the writer cannot
dedup against is how duplicates get made at scale.*

**P1.2 — `source_value_extractions` has no writer. This is the break.**
Specified in fourteen places, feeds `schemas/directness.py`, named in the pipeline contract, the
pipeline map, the context map and three governance documents, backs `v_item_extractions` and
`v_value_independence` — and no script, no CLI subcommand and no committed migration has ever
inserted a row. Add `db.py add-extraction`, with refusals on: FK to `evidence_sources` and `items`,
the column's own CHECK vocabulary, and a **mandatory locator** (R3 — a value without a locator is
the thing this table exists to prevent).
*Until this lands, convergence counts documents rather than values, which `evidence-methodology.md`
§3 expressly forbids, and `v_value_independence` returns 0 by construction.*

**P1.3 — `specifications` and `specification_source_links` have no CLI writer.**
The judgment stage cannot write its own output through the sanctioned path. Add
`db.py add-specification` and `add-spec-source-link`. Refusals must implement what
`validate_evidence_state.py` currently only detects after the fact: non-empty `governing_refs` for
`stated`/`provisional`; no `stated` on a `code_floor_only` / `regulatory_stratum_only` cell; T3-alone
capped at `provisional`. *Without `specification_source_links`, even a correct cell renders with no
visible sources.*

**P1.4 — `assess_cell.py` is a hardcoded 7-cell pilot.**
`PILOT_CELLS` at `:114-130`; argparse exposes only `--db`, `--emit-sql`, `--report-json`; it crashes
twice against live data. Take `--item` and `--population`, drop the hardcoded list, fix the crashes.

**P1.5 — Unassessed sources anchor a `stated` cell.**
`NOT_ASSESSED`, `PARTIAL` and `PROXY` all consolidate to `COND_DOWN_WEIGHTED`
(`directness.py:225-234`) and `anchoring()` admits all three (`assess_cell.py:248-250`, `:314`).
`evidence-methodology.md:127-132` puts *"for the target population"* in condition 1 (T1 clinical) and
condition 3 (Co-1) and **not** in 2 (T2 synthesis) or 4 (Co-2 CPG). So: `NOT_ASSESSED` disqualifies
anchoring **via conditions 1 and 3 only**. Do not generalise — a blanket ban wrongly demotes Tier 2
reviews and OT professional-body guidelines, which anchor on parameter relevance by design.
Also wire `needs_population_assessment`, which is computed at `:209`, aggregated at `:421-422`,
emitted at `:582`, and read by nothing — G2 mandates cap *and* flag; only the cap has consequence.

**P1.6 — `update-bpc` crashes on the first write for any slug.**
`population` is whitelisted in `_BPC_META_COLS` (`db.py:60-66`) and never exposed as a CLI flag
(`:1039-1052`), so the INSERT branch at `:1770-1778` hits NOT NULL. With `bpc_metadata` at 0 rows,
the mobility batch's *first* synthesis write raises an uncaught `IntegrityError`. Add
`--population`.

---

## Phase 2 — The backward and re-entrant edges

**This is the part the row counts cannot show, and the part the owner asked for.** A pipeline that
only runs forward cannot revise itself; every one of these is a path by which a later finding should
change an earlier record, and does not.

**P2.1 — Mining harvests leads and drops them. No promotion edge exists.**
`citation_mining.connections_produced` holds harvested DOIs as a JSON array. Measured: **138 distinct
DOIs harvested, 4 in the clue store, 134 stranded.** And `sessions/artifacts/` holds a real
May-2026 OpenAlex mobility pass — **272 DOIs, 16 in the store, 256 in neither store nor evidence.**
`connections_produced` is written only by data migrations and **read by no script in `scripts/` or
`tools/`.** It is write-only data.
Add `db.py promote-mined-leads`: read `connections_produced` (and, once, the `sessions/artifacts/`
files), dedup via P1.1's two-table check, write `source_locators` rows carrying `doi`, `pub_year`,
first author, `recovered_from` naming the artefact, `status='REFERENCE-ONLY'`, and **`title` NULL**
— `title_short` in those artefacts is truncated mid-word and must never be promoted as a title.
*Effect: R2's yield stops being a per-anchor checkbox and starts feeding the next frame.*

**P2.2 — Nothing compares a determination against the synthesis that cites it.**
Ten scripts touch both `specifications` and `bpc_metadata`; all are renderers, counters or schema
audits. No comparator exists. Add one check: for each synthesis, every determination it cites must
exist, and its value must match the live `specifications` row; divergence is a finding, not a silent
overwrite.

**P2.3 — Stale-synthesis propagation is BUILT and has never run.**
Correction to an earlier reading: `supersession_check` is not absent. It has a writer
(`db.py:1671 add_supersession_check`), a CLI subcommand, and a schema — and **0 rows**. This one
needs *running and wiring into the walk*, not building: when a judgment changes, dependent syntheses
must be marked stale. Cheapest item in Phase 2 by far.

**P2.4 — No cross-slug synthesis contradiction check.**
Genuinely absent. **Deliberately deferred:** it needs ≥2 syntheses to have a subject, and there are
0. Building it now produces another gate that passes having examined nothing — CLAUDE.md §2(a),
which this repository has produced four times. Revisit when `bpc_metadata` is non-empty.

**P2.5 — `connections.opus_reviewed` is dead, and unreviewed connections reach the book.**
Hardcoded to `0` on write (`db.py:1374`), never settable, never read. `generate_parts.py
build_part05` (`:250-266`) filters on `status` only, so a PENDING connection's description renders
verbatim in Part 5. Either make it settable *and* read as a render filter, or delete the column
under §1's symmetry rule. **Do not leave it as a field that looks like a safeguard and is not.**

---

## Phase 3 — Render truthfulness

| # | Defect | Location |
|---|---|---|
| **P3.1** | `room_page.py` queries `FROM room` and `room_item`; the live tables are `rooms` and `room_items`. Two wrong names, one file. | `room_page.py:26,29` |
| **P3.2** | `index.html` claims "91 provisions, 661 evidence sources" against a live 93 / 10, plus per-category drift. §2(b) forbids hand-written counts in derived documents. | `index.html:7` |
| **P3.3** | `register_integrity_check.py` prints "(DB cross-check on)" while that path never executes — `db_rows` is built from 0-row `specifications` and the per-cell block is gated `if db_rows:`. The author's own comment at `:362-366` admits it. | `register_integrity_check.py:430-431` |
| **P3.4** | `parts/` has no committed freshness fingerprint; the contract records `render-freshness` as `check: null` for it. | `pipeline-contract.yaml` |

---

## Phase 4 — Apparatus honesty. Real, none of it blocking.

- **P4.1** Attestation battery's window is `HEAD~1..HEAD` locally and the whole branch on CI, so
  `preflight.sh` cannot predict a blocking gate. Pass `run_checks.py`'s computed base to checks that
  accept one. (`adherence_log_audit.py:569`, `run_checks.py:147-161`, `ci.yml:220`)
- **P4.2** `insert_jurisdictional_value` makes no `check_vocab` call on `jurisdiction`. Land it in
  the **same change** as the ES/PT/FI enum members, members first — the enum is inert today, so a
  check landing alone would start refusing the batch's own targets.
- **P4.3** `next_gap_id()` mints `GAP-NNN`; every live gap is `GAP-B0n-NNN`. (`db.py:135-144`)
- **P4.4** Runbook repairs: `:794` calls a script deleted in the 2026-08-20 cull; `:856-864`
  instructs the `admitted_ref_ids` dual write the 2026-08-24 ruling abolished, citing two deleted
  checks; `:830` says "No CLI" where `add-candidate` exists.
- **P4.5** Co-1: add `--co1-provenance`; fix `validate_evidence_state.py:76-110`, which reads
  `data/sources/*.yaml` — **a directory that does not exist** — with a dormant `NameError`.
- **P4.6** R8 ordering: no `update-search` writer, so a search logged before screening cannot have
  its counts completed through the sanctioned path.

---

## Order, and why

```
P0  ─────────────────────────────────────────────► must be first; protects everything after it
     │
P1.1 ├─► P1.2 ─► P1.3 ─► P1.4 ─► P1.5            forward walk to one rendered cell
     │            │
     └─► P2.1     └─► P1.6                        P1.1 gates P2.1: dedup before promoting 256 leads
P2.3 ─────────────────────────────────────────────► cheap, independent, already built
P2.2, P2.5 ───────────────────────────────────────► after P1.3 gives them a subject
P3  ──────────────────────────────────────────────► independent; P3.1/P3.2 are minutes
P4  ──────────────────────────────────────────────► any time
P2.4 ─────────────────────────────────────────────► deliberately last; no subject until synthesis exists
```

**One test for the whole plan.** After P0 + P1, this must be possible on a scratch copy and produce
a rendered page carrying its sources:

```
one mobility source admitted → one value extracted with a locator →
one (item × population) cell written with governing_refs → one synthesis →
one rendered page showing the value AND the sources behind it
```

That is §4's acceptance criterion — *"One answered question, published"* — reduced to a mechanical
dry run. If it cannot be walked on scratch, Phase 1 is not finished, whatever the checks say.

**What this plan deliberately does not do:** it adds no new check to the registry, no new table, no
new register, and no workplan file. Every item is a repair to something that already exists or a
writer for a table that already exists. Where the honest answer is "delete it" (P2.5), that is
offered as the equal option — CLAUDE.md §1's symmetry rule, which is the whole reason this
repository is allowed to shrink.

---

# AMENDMENT — 2026-08-25, after adversarial review

The plan's **core diagnosis survived** the review. Its **acceptance test did not.** F4's closing
line is the fair one: *"Like the pipeline it repairs, it currently ends one column earlier than it
looks."* Every correction below is verified independently before being written here.

## A-1 — THE WALK DOES NOT COMPLETE. Phase 1 as written is insufficient.

I asserted that Phase 0 + Phase 1 makes this walkable:
*source admitted → value extracted → cell written → synthesis → rendered page showing value AND
sources.* **It does not, and the failure is at the last step.**

```
$ grep -c "value" scripts/generate/spec_page.py
0
```

**`spec_page.py` never selects and never renders the value tuple.** Its table carries state, tier
and sources — no value column. So even a perfect `specifications` row with `value_min`,
`value_max` and `value_unit` populated renders a page with **no value anywhere on it**. The
acceptance sentence I wrote is unsatisfiable by construction, and nothing in Phases 0–4 would have
caught it, because nothing in the plan reads the renderer.

Compounding it: `assess_cell.py:565-573` carries `value_min, value_max, value_unit` in its INSERT
column list and binds literal `None` for all three. So the only existing writer produces valueless
rows, and the only existing renderer could not show them if it did.

**Five additions, all Phase 1, none optional:**

| # | Addition | Why |
|---|---|---|
| **P1.7** | `spec_page.py` selects and renders the value tuple | Without it the walk cannot end |
| **P1.8** | The judgment writer (P1.3) takes and binds `--value-min/--value-max/--value-unit`; `assess_cell` stops binding `None` | Without it there is nothing to render |
| **P1.9** | P1.3's refusals must also cover **convergence assessment** (blocking `validate_evidence_state` demands one for `stated` AND `provisional`) and the **confidence flag** for `provisional` — or `assess_cell` is declared the sole sanctioned writer and P1.3 is dropped | Otherwise the first honest cell fails the blocking battery |
| **P1.10** | `add-extraction` (P1.2) must write `root_type` + `root_ref_id`, and `external_root_registry` needs a writer | `v_value_independence` counts only rows carrying those; without them it still returns 0 and P1.2's stated purpose is unmet |
| **P1.11** | `--verification-method` choices reconciled with blocking I4 | `corroborated-not-retrieved` and `citing-bibliography` are both offered and both rejected by I4 for VERIFIED rows; `direct-render` is missing |

**P1.9 is the one that matters most.** A green path that is unreachable while the gate stays red is
precisely the condition that produced the 2026-08-19 fabrication: the writer could not express what
the gate demanded, so someone wrote it by hand.

Also corrected: the regeneration step in this plan and in `WAVE-H-SCOPE.md` names
`regenerate_derived.sh`, **which does not touch `site/specs/`** — that is `build_site.py`, and its
freshness check is advisory.

## A-2 — P2.3 was a category error. Withdrawn and replaced.

I wrote that `supersession_check` is "built and has never run" and needs only wiring. **Wrong.**
Read from the schema:

```
outcome      CHECK(outcome IN ('current_best','superseded_by','refined_by',
                               'divergent_no_supersession','co1_addition_logged','pending'))
check_method CHECK(check_method IN ('pubmed_search', …))
```

That is **literature currency for an anchor source** — *is this source still the best available?* It
cannot express "a judgment changed, so the synthesis citing it is stale." S4's original verdict
(ABSENT) was right and I overturned it in the wrong direction by reading a table name instead of its
CHECK constraints — the exact error CLAUDE.md §4 warns about when it says vocabularies come from the
schema, not from the code or the name.

**Replacement:** judgment-staleness propagation is **ABSENT**. Build it on `derivation_sha`
(`assess_cell.py` already computes an identity hash per cell) plus the P2.2 comparator: when a
cell's `derivation_sha` changes, every synthesis citing that cell is flagged. `supersession_check`
keeps its own job and is not conscripted.

## A-3 — Factual corrections to my own findings

| Claim | Correction |
|---|---|
| "no committed migration ever inserted into `source_value_extractions`" | True of the **live tree only**. Two archived migrations do: `_archived/scripts/migrations/data_20260714210000_rap_rt60_extraction_substrate.sql` and `…_20260715050000_rap_rt60_general_genealogy.sql`. The table **has** held rows (the pilot's 8); the clean-room reset destroyed them. "Never written" was too strong — "no live writer, and its only rows were archived away" is right. |
| `connections_produced` "read by no script" | `db.py:194,230` reads and rewrites it. The true claim is narrower and still holds: **no promotion consumer** — nothing moves a harvested DOI into the clue store. |
| "134 stranded" | **133.** Two of the 138 are in `evidence_sources`. |
| `room_page.py` — two wrong table names | **Six** bad references: `room`, `room_item`, `room_item_population`, `room_dar_provision`, `room_conflict`, and `specification` singular, plus `room_id` vs `room_code` keys. The two-rename fix in P3.1 leaves it crashed. |
| "ten scripts touch both `specifications` and `bpc_metadata`" | **Eight.** |
| "13 of 19 contract criteria covered" | Not reproducible; independent measure is 14 named / 5 null. **Withdrawn pending a single agreed method.** |
| "two of the four DG-NON items are now ruled" | Two were answered in conversation; only the `icf_demands` one is in the ledger. The E-08/Wave H answer is recorded as a scope document, not as a ruling. |

## A-4 — Two internal contradictions in this plan

1. The closing paragraph says the plan *"adds no new check"* while **P2.2 says "Add one check."**
   The closing claim is wrong; P2.2 is the exception and should be stated as one, with §1's
   burden-of-proof met explicitly: *without it, a synthesis can cite a determination that no longer
   says what the synthesis says it says, and nothing reports it.*
2. **P1.1's evidence-type fix cited a list at `db.py:1223`.** `evidence_sources.evidence_type` has
   **no CHECK constraint**, so there is no schema vocabulary to derive — taking the code list would
   install a second home for a vocabulary (rule 5). The correct fix is a CHECK migration first, then
   `dbcore.check_values()`.

## A-5 — Dropped without a recorded deferral

From the S1–S6 traces, absent from the plan and now added to Phase 4 rather than silently lost:
`add-population-match` crashes on a same-session divergent grade (the very case CLAUDE.md §4 says
must land as a second row); `adjudication_integrity` never fails on its exit code;
`source_locators.jurisdiction` holds unusable values in 818 of 875 rows with **no reader at all** —
which is the filter a bucket-driven batch would run; and `spec_value_probes` / PMP writers are
absent while the skill teaches raw `INSERT`.

## What survives unchanged

P0 (the canonical-write guard, though "silently destroy" was dramatised — sha discipline and the CI
rebuild-compare would catch it), P1.1–P1.6 as *necessary* though not sufficient, P2.1, P2.2, P2.4's
deferral (justified: `bpc_metadata` is 0, and building a comparator now yields another vacuous
gate), P2.5, and the whole of Phase 3 and Phase 4. The edge-based organisation survives. The
diagnosis survives.

**The acceptance test does not, and that is the finding.** A plan whose success criterion cannot be
met, in a repository whose documented failure mode is gates that pass having examined nothing, would
have been executed to completion and declared done.

---

# AMENDMENT 2 — 2026-08-25, owner directive: fold the outstanding fixes into this plan

Two additions. The first is a live defect actively corrupting the provenance record; the second is a
sequencing consequence of the population ruling that this plan did not carry and would have got
wrong.

## P0.3 — The command-log hook misfiles, for the third time, and now pins itself

**Status: LIVE and SELF-REINFORCING.** Measured at the time of writing: of 82 lines in
`scratchpad/session_2026-08-25-rulings-incorporation-and-pipeline-sweep/commands.jsonl`, **56 are
this session's commands** — the misfile has overtaken that session's own frozen record. It grows by
one commit every turn. Full evidence in `HOOK-REGRESSION.md`.

**WHERE** `.claude/hooks/record-command.py`, `open_session()` — the derivation merged in PR #119.

**NOW** — two paths, both failing:

1. **Fast path.** Matches the harness `session_id` against the *last line* of each existing log.
   This session's own log carries **822 lines and zero `session_id` fields** (written under the
   pre-#119 schema), so it can never match. **The fast path also cannot bootstrap**: the first call
   of any new session has no prior line to match, by construction.
2. **Fallback.** `openp = [n for n in pads if not (root/"sessions"/f"{n}.md").exists()]`, then
   `openp[-1]`. **A session is treated as closed the moment its record file exists.** This session
   wrote `sessions/session_2026-08-25-pipeline-smoke-test-mobility.md` at *open* — which
   `CLAUDE.md` rule 6 explicitly encourages (*"commit the scratchpad at every natural break, not at
   session end"*) — so it is classified closed while still running, and the newest directory
   *without* a record wins instead.
3. **Then it pins.** That wrong log now ends with this session's `session_id`, so the fast path
   matches it on every subsequent call. The misfile becomes permanent and self-confirming.

**CHANGE** — make the harness `session_id` authoritative and the record file advisory, in this
order:

```
1. If a scratchpad dir already contains a line carrying THIS session_id  -> use it.      (unchanged)
2. Else if exactly one scratchpad dir has no sessions/<stem>.md          -> use it.      (unchanged)
3. Else write to scratchpad/<session_id>/commands.jsonl.                 (NEW: bootstrap)
```

Step 3 is the fix. A first call with nothing to match currently falls through to "newest without a
record", which is a *guess about which session is running*. Writing under the harness id instead is
a **visibly foreign directory name** — which the hook's own docstring already argues for: *"a wrong
answer must be loud."* A session that then writes its record can adopt the directory deliberately;
nothing has to infer it.

**REFUSALS/TESTS** Extend `scripts/tests/test_record_command_session.py` (added by #119) with the
two cases it does not cover: (a) a session whose record exists **while it is still running** —
the rule-6 case, which is the live failure; (b) a first call with **no prior line** carrying the
session id — the bootstrap case. Both currently resolve to another session's directory.

**BLAST RADIUS** The hook only. No table, no gate, no rendered surface. `#119`'s test file is the
one caller.

**RISK** Low to change, and **the risk of not changing it is the one that compounds**: every turn
writes another session's provenance into a frozen record, and `CLAUDE.md` §0.4 says a 0-row or
mis-keyed object is *unproven, not clean*.

**Note on the pattern, because it is the point.** This is the third iteration of one bug:
`.claude/session` went stale → `sessions/LATEST` went stale → the derivation now mis-classifies any
session that records itself early. Each fix corrected the mechanism it could see and left the
question underneath — *which session is running?* — answered by inference. The harness knows. Ask it.

**The misfiled lines are not moved.** Same reasoning as #119's own: re-attributing a frozen
append-only log by inference is how a provenance record becomes a guess. Each affected directory
gets the `commands-jsonl-WHERE.md` pointer #119 established.

## S-1 — SEQUENCING: the population split precedes the first cell write

Owner ruling 2026-08-25 splits `MOB` into **ambulatory** and **wheelchair user**. That is content
and tracked in the ledger, not here — but it imposes a hard ordering on this plan that was not
stated:

> **The split must land before P1.3 writes the first `specifications` row.**

`specifications` is keyed `(item_code, population_code)`. Every cell written before the split is
keyed on `MOB` and has to be re-keyed after — and re-keying a *determination* is a different and
much worse operation than re-pointing substrate, because a cell carries `governing_refs`, a
convergence assessment and a tier basis that were all reasoned against a population that no longer
exists.

Measured footprint of the split today: **33 rows** — 31 `item_population_links`, 2
`population_axis_map`, **zero** `evidence_population_match`, zero everywhere else. Every one of
those zero tables fills during the batch. The split is cheap exactly once, and this is the window.

Revised critical path:

```
P0.1 P0.2 P0.3  ──►  [MOB split lands]  ──►  P1.1 ─► P1.2 ─► P1.3 ─► P1.4 ─► P1.5
                          (content,                                    │
                           owner-ruled)                       P1.7 P1.8 ─► the value path
```

P1.1 and P1.2 have no population key and could technically precede the split; P1.3 onward cannot.
Ordering them all after it costs nothing and removes the chance of a half-migrated cell.
