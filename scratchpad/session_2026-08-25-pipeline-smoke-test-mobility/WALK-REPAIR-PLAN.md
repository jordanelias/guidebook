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
