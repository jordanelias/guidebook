# The repair plan — consolidated, ordered, exhaustive

**Supersedes `WALK-REPAIR-PLAN.md` and its three amendments.** That file is the working record of how
this plan was arrived at, including what was withdrawn; this file is what an implementer follows.

**Code-level detail lives in two design documents and is not duplicated here:**
`logs/F6-code-fix-design.md` (2,203 lines — exact line numbers, current code, replacement code,
refusal sets, migration SQL) and `logs/F5-population-split-design.md` (the split's data resolution
and caller sweep). This document is the spine: what, in what order, why, and who decides.

**Scope discipline.** Everything here is code and wiring except §8, which is content and already
ruled. Nothing here is a new register, a new workplan file, or a new check — with **one** declared
exception (§5.2), whose burden of proof is met in place.

---

## 1. The ordering, and why it is this

```
P0.1 ─┬─ P0.2 (same commit)                     safety: nothing else runs first
      ├─ P0.3  hook misfiling
      ├─ P0.4  twelve retired codes in live skills
      └─ P0.6  §R8 rename + register entry  (owner-gated, whole, rename BEFORE entry)
                    │
              §8 POPULATION SPLIT  (content, ruled — must precede any cell write)
                    │
              P1.0  re-grain `specifications`  (owner-ruled; needs its parameter vocabulary)
                    │
P1.1 ──► P1.2 ──► P1.4 ──► ( P1.5 ∥ P1.8 ∥ P1.3′ ) ──► P1.7 ──► walk_e2e.sh
  │        │  ▲
  │        │  └── P1.2 must REQUIRE parameter_canonical — P1.0's key depends on it
  │        └──────────────────────────► P2.1  (needs P1.1's dedup only)
  └───────────────────────────────────► P2.2  (needs migration 066)

P3.x, P4.x — independent, any time.   P2.4 — deliberately last, no subject yet.
```

**The ordering claims, each with a reason** *(no count — §2(b): a hand-written number in a
derived document drifts the moment the list changes, and this one already did):*

- **P0.1 and P0.2 share a commit.** Wiring the canonical-write guard mechanically breaks the four
  skill lines that instruct the canonical path. Landing the guard alone turns those skills into
  runtime failures.
- **§8 precedes P1.3′ — but the reason weakened on 2026-08-26 and is restated honestly.** The
  original reason was that `specifications` is *keyed* on population, so a cell written before the
  split would be keyed on a code that will not exist. **P1.0 removes that key**, so the cost of
  getting it wrong drops from re-keying a determination — with its governing refs, convergence
  assessment and tier basis — to re-pointing junction rows. The ordering still holds, because a
  cross-reference asserted against a superseded code is a wrong statement about the book while it
  stands; it is no longer *categorically* worse, and this plan should not keep claiming it is.
- **P0.6 precedes the batch, not merely the walk.** `search_executions.query_text` already holds
  `AX-` in a live row: running a batch first writes new rows in retired vocabulary, into rendered
  search logs that sit under an `.ignore`d path where the sweep's own grep cannot see them.
- **P2.4 is last on purpose.** It needs ≥2 syntheses to have a subject and there are none. Building
  it now produces another gate that passes having examined nothing.

---

## 2. Phase 0 — Safety

### P0.1 · Wire the canonical-write guard
`dbcore.is_canonical()` exists solely to refuse writes to the committed database. Its only callers
are its own selftest (`dbcore.py:438-439`). `connect()` never calls it and `db_path()` **defaults to
canonical** when `GUIDEBOOK_DB_PATH` is unset. This is failure mode #1 in the instrument's own §12.4,
with the written mitigation unwired. Migrations need an explicit override; F6 specifies its shape.

### P0.2 · Repoint four skill lines (same commit as P0.1)
`connection-auditor_SKILL.md:185,192,199` and `connection-discovery_SKILL.md:219` instruct
`GUIDEBOOK_DB_PATH=data/guidebook.db` on **write** commands.

### P0.3 · The command log misfiles, third iteration, self-reinforcing
Two failing paths in `open_session()`: the fast path **cannot bootstrap** (a session's first call has
no prior line to match), and the fallback treats a session as closed the moment `sessions/<stem>.md`
exists — which rule 6 encourages writing early. Then it pins, because the wrong log now ends with
this session's id. **Live evidence: 56 of 82 lines in another session's frozen log are this
session's.** Fix is a third branch: write under the harness `session_id` when nothing matches — a
visibly foreign name, per the hook's own "a wrong answer must be loud". Two test cases owed.

### P0.4 · Twelve retired population codes are still taught by live skills
`validate_population.py:79` holds a complete `RETIRED_CROSSWALK` — `VIS→BLIND`, `UPL→LMB`,
`DBL→DEAFBLIND`, `NEU→BRAIN`, `PCS→BRAIN`, `OFS→COM`, `CFS→COM`, `MCAS→COM`, `POTS→COM`,
`LCOV→COM`, `SENS→NDV`, `EXH→TALL` — and it validates the **database**, not the skills. `VIS` is
absent from `populations` and taught by **12** live skill files; `OFS` by **10**.
`retired-vocabulary.yaml` has no entry for any of the twelve. **P0 because the mobility batch loads
exactly these skills**, `cross-population-conflict-mapper` among them.

### P0.5 · The split must not become the thirteenth un-swept retirement
Its caller sweep ships in the same change: `schemas/enums.py`, `validate_population.py`'s crosswalk,
`site/populations/mob.html`, the vetting surface (31 tokens), the pipeline dashboard (1), **the ten
live skills teaching `MOB`**, and `retired-vocabulary.yaml`.

### P0.6 · The §R8 demand-layer rename — and the register entry that must follow it
**Owner ruling 2026-08-26**, closing open decision 3: the rename executes **together with** a
`retired-vocabulary.yaml` entry, so the token is caught mechanically rather than by remembering.
Prose discipline against it failed four times in one session on 2026-08-25.

**Order is fixed and is the reverse of the intuitive one.** The register's own admission test 2 says
a token whose replacement has not landed *"is still describing live data correctly"* — so the entry
cannot precede the migration. Rename first, entry last, one change.

**Seven identifier entries, never the bare word.** `retired_vocabulary_audit.py:93-108` compiles
every mode with a `(?<![\w-])…(?![\w-])` boundary, so `token: axis` would match ordinary English
prose and nothing else — it cannot even reach `axis_code`. Flagging descriptive English is what §R8
explicitly forbids. The entries are `axes`, `axis_code`, `item_axis_links`, `population_axis_map`,
`access_need_axis_map`, `serves_axes`, `attaches_axes`.

**`AX-` cannot be expressed by this register at all** — all three match modes require a non-`[\w-]`
character after the token, so `AX-` never matches `AX-AMB`, and there is no prefix mode. Which forces
the scoping question: **the migration must state whether the 17 code values are re-minted.** If not,
`AX-*` is correct live data and goes to `deferred:` with that reasoning. If so, it is 288 live cells
(`GLOB`, 2026-08-26) — 249 in the four `axis_code` columns and **39 in free text**, the harder half.

**Why Phase 0 and not later.** `search_executions.query_text` already carries `AX-` in a live row, so
a batch run before the rename writes new rows in retired vocabulary — and rendered search logs live
under an `.ignore`d path, invisible to the sweep's own grep. Ledger entry:
`references/project-standards.md`, 2026-08-26. **Owner-gated and whole** — §R8 item 3's bar on
piecemeal execution stands; `validate_axes` (`check-registry.yaml:640`) and the registry itself are
callers.

---

## 3. Phase 1 — The forward walk

### P1.1 · `add-source` cannot make an honest admission
Four defects, one file, one migration (`065`). VERIFIED must set
`verification_disposition='CLOSED'` (blocking I1). `--scope` is missing entirely. `--evidence-type`
enforces no vocabulary — and the column has **no CHECK**, so the fix is a CHECK migration *then*
`dbcore.check_values()`, never a code list (that would be a rule-5 second home). `--verification-method`
offers two values blocking I4 rejects for VERIFIED rows and omits `direct-render`; F6 puts the I4
subset in **one** home, `dbcore.I4_ARTEFACT_METHODS`, imported by both writer and test.
**R9 dedup** must check both `evidence_sources` and the clue store, copying `insert_locator`'s
existing two-table check.

### P1.2 · `add-extraction` — a writer for `source_value_extractions`
The break. Zero live writers; two archived migrations wrote it and the clean-room reset took those
rows. Full refusal set from the table's own CHECKs, FK targets, and a **mandatory locator** (R3).

### P1.10 · Roots, or the extraction is invisible
`v_value_independence` counts only rows carrying `root_type` plus either `root_ref_id` or a
registered `root_id`. Without them the view still returns 0 and P1.2's stated purpose is unmet.
`external_root_registry` needs its own small writer. **Both tables must be added to
`dbcore.WRITABLE_TABLES` or `emit_batch_sql.py` silently drops the rows** — a trap worth naming.

### P1.0 · NEW, AND NOW FIRST IN PHASE 1 — re-grain `specifications`
**Owner ruling 2026-08-25.** The uniqueness key becomes the **judgment object alone**;
`population_code` is demoted from identity to cross-reference. Three N:N junctions land in the same
migration — specification↔**population**, specification↔**access need**, specification↔**ICF** —
because a determination written before they exist is unqualifiable.

**None of the three may be derived from another.** `access_need_icf` is 43 rows and **38 `e`, 3 `d`,
2 `b`** — overwhelmingly environmental-factor codes. A specification's ICF cross-reference is often
`b`/`d`, the person's functioning, which that table does not carry.

**The drop is clean, and only for now.** `specifications` holds 0 rows,
`specification_source_links` 0, and **no committed data migration INSERTs into either** — only the
baseline's DDL at `057_baseline:6823`. Rule 5's own drop test therefore passes: `population_code`
can be **dropped**, not NULLed forward, and migration 062's replay trap does not apply. **This
window closes the moment the first determination is written.**

**Also in this change:** amend R4's second sentence in `governance/research-contract.yaml:119`. It
reads *"Cells are (item x population)"* and is now superseded; a contract injected into every
session may not contradict its own first sentence.

**RESOLVED 2026-08-26 — the judgment object is the canonical parameter.** Owner ruling, selecting
from options put. `specifications` keys on the design parameter under determination, reusing
`source_value_extractions.parameter_canonical`; `items` is demoted to the Part-4 render rollup that
`conceptual-model.md:92` already calls it, **derived from** specifications rather than keyed by them.
So `item_code` is dropped from `specifications` alongside `population_code`, in this same migration.

**The schema already carries this grain one stage upstream.** `source_value_extractions` has
`parameter` **NOT NULL** with `parameter_canonical`, `population_code` and `item_code` all nullable —
parameter as identity, the rest as qualifiers. `specifications` inverts it and holds no parameter
column at all. And `v_value_independence`, the view feeding `convergence_assessment`, has grouped on
`COALESCE(parameter_canonical, parameter), population_code` since the baseline
(`057_baseline_2026-08-12.sql:6693-6701`) with **no `item_code` in it**; `idx_sve_slug_param` indexes
`(slug, parameter_canonical)`. Only `specifications` disagreed.

**Two obligations this creates, neither optional:**
- **A canonical-parameter vocabulary lands in or before this migration.** `parameter_canonical` has
  no CHECK, no registry table and no writer — its entire specification is a code comment at
  `schemas/source_value_extraction.py:89` (*"normalized for join (lowercase, hyphens)"*). Keying a
  determination on unconstrained free text makes "corridor clear width" and "clear corridor width"
  two determinations of one thing. Its home is a CHECK or a registry table, never a list in code
  (rule 5).
- **P1.2's `add-extraction` must REQUIRE `parameter_canonical`**, not honour the column's
  nullability, or an extraction can be written that no determination can join to.

**Also re-derived here:** `v_value_independence` still groups by `population_code`. Under the ruling
population is a cross-reference, so that view's grain moves in this change or an independence count
fragments across populations.

### P1.3′ · RESOLVED: `assess_cell` is the sole writer of stated/provisional/pending
The original plan proposed `db.py add-specification` with a `--state` flag. **Dropped.** F6
enumerated all ten cell conditions and five convergence conditions that blocking
`validate_evidence_state` enforces; a CLI that lets a session assert `--state stated` directly *is
the fabrication shape*. Instead: `assess_cell` writes `specification_source_links` in the same
transaction, and a narrow `add-specification` exists for `not_applicable` only.

### P1.4 · `assess_cell` is a hardcoded 7-cell pilot
`PILOT_CELLS:116-131` removed; `--item/--population/--slug` added; both live-data crashes fixed; ids
from DB max rather than `CELL_ID_BASE`.

### P1.4b · NEW DEFECT — `regulatory_stratum_only` is computed and never written
Found by F6, verified here. The value is computed at `assess_cell.py:310`, set at `:376`, reported
at `:415` — and **absent from the INSERT column list at `:565-571`**, which carries `code_floor_only`
and not it. The column exists (migration 027) with `DEFAULT 0`, so **every regulatory-stratum cell
would silently record 0**.

The sharp part is the code's own comment at `:608`, which condemns the old workaround for using
*"a fragile `tier_basis LIKE '%(regulatory_stratum_only)'` string match rather than the column test
that now exists"* — and then the INSERT never writes that column, leaving the fragile string suffix
appended at `:382` as the only surviving signal. **The right structure exists, the code names it as
right, and the write path does not use it.**

Consequence: `regulatory_stratum_only` gates amended invariant I3 — such a cell is never `stated`
and renders weak-band (○) only, flagged and caveated. With the column at 0, any consumer testing it
sees "not regulatory stratum" for every cell in the book.

### P1.5 · Unassessed sources must not anchor — via conditions 1 and 3 only
`evidence-methodology.md:127-132` puts *"for the target population"* in condition 1 (T1 clinical) and
condition 3 (Co-1), **not** in 2 (T2 synthesis) or 4 (Co-2 CPG). So:
`anchoring(recs, require_population_assessment=True)` for the T1 and Co-1 buckets only.
`directness.py` is unchanged — this is an additive rule, not a re-grading. And
`needs_population_assessment` (computed, aggregated, emitted, read by nothing) is finally consumed,
with an "anchors withheld pending assessment" line.

### P1.6 · `update-bpc --population`
`population` is whitelisted in `_BPC_META_COLS` and absent from argparse, so the first synthesis
write for any slug hits NOT NULL.

### P1.7 · The renderer must show the value
`grep -c "value" scripts/generate/spec_page.py` returns **0**. Query extended at `:73-88`, plus a
`value_cell()` renderer handling range / ≥ / ≤ / equal forms, a "no value recorded" warning on
`stated` cells, and a loud `[unit not recorded]`.

### P1.8 · The judgment writer must bind the value tuple
`assess_cell.py:561` binds literal `None, None, None`. Value derived from `--value-from-extraction`
ids, with refusals: governing-source-only, single unit, no conversion.

### P1.11 · Verification-method choices reconciled with I4
See P1.1; one home, imported by both sides.

---

## 4. Phase 2 — The backward and re-entrant edges

### P2.1 · `promote-mined-leads`
Re-measured by F6: **138 mining DOIs, 133 unheld**; artefacts **269 distinct DOIs, 256 unheld**, 27
no-DOI rows skipped. JSON key drift is real and documented (`author` vs `first_author`; year as
string vs int). Promote DOI, year, first author, `recovered_from`, `status='REFERENCE-ONLY'`;
**`title` stays NULL — `title_short` is truncated mid-word.**

### P2.2 · The determination↔synthesis comparator
Migration `066` adds `synthesis_determination_links`: a pointer plus a **witnessed**
`derivation_sha_at_synthesis`. That is the `data_migrations`-content-sha class — a witness of what
was true at a moment — not a rule-5 copy. CLI reads the sha from the row, never accepts it as an
argument. Comparator `scripts/audit/synthesis_determination_sync.py`.

### P2.3 · WITHDRAWN — category error
`supersession_check` records **literature currency for an anchor source** (`current_best`,
`superseded_by`, `refined_by`; `check_method IN ('pubmed_search', …)`), not judgment staleness. It is
untouched. Judgment-staleness propagation is **ABSENT** and is delivered by P2.2's witnessed sha.

### P2.4 · Cross-slug contradiction — deliberately deferred
No subject until `bpc_metadata` is non-empty.

### P2.5 · `connections.opus_reviewed` — DELETE, do not fix
Hardcoded 0 at `db.py:1374`, never settable, never read; `build_part05` filters on status only. No
reader, no data-migration INSERT, so it is droppable (migration `067`). **Recommend deletion** under
§1's symmetry rule — a field that looks like a safeguard and is not is worse than no field.
*Owner decision if Opus-review render gating is wanted instead.*

---

## 5. Phase 3 — Render truthfulness

### P3.1 · `room_page.py` — rewrite thin, do not patch
**Six** nonexistent objects, not two: `room`, `room_item`, `room_item_population`,
`room_dar_provision`, `room_conflict`, `specification` singular — at `:26, :29, :35, :44, :51, :66,
:75, :84` — plus `room_id` vs `room_code` and four phantom render columns. Rewrite against `rooms` +
`room_items`; delete the Template-3 matrix, DAR and conflict sections until those tables exist.

### 5.2 · The plan's ONE new check — declared, with its burden of proof met
`synthesis_determination_sync` (P2.2), registered **advisory** in battery `data`; promoted to
blocking when `bpc_metadata` is non-empty. *Burden of proof (§1): without it, a synthesis can cite a
determination that no longer says what the synthesis says it says, and nothing anywhere reports it.*

### P3.2 · `index.html:7` — derive the counts
"91 provisions, 661 evidence sources" against a live 93 / 10, plus per-category drift. §2(b) forbids
hand-written counts in derived documents.

### P3.3 · `register_integrity_check.py:430-431` prints "(DB cross-check on)" while that path never
executes. **P3.4** · `parts/` has no freshness fingerprint.

---

## 6. Phase 4 — Apparatus honesty

**P4.1** attestation window (`HEAD~1` locally vs whole-branch on CI) · **P4.2** jurisdiction
`check_vocab` — **members first, then the check, one change** (owner-ruled) · **P4.3** `next_gap_id`
format, and F6 makes it a shared `dbcore.next_gap_id` · **P4.4** runbook repairs at `:794`, `:830`,
`:856-864`, struck via dated corrections · **P4.5** Co-1 CLI flags **plus a DB arm** for the Co-1
rules · **P4.6** R8 ordering / no `update-search` writer.

**Two corrections to earlier findings, from F6's verification pass:**
- `adjudication_integrity.py`'s exit code **is not broken at HEAD** — a fixture run exits 1 on
  VERDICT FAIL. The earlier trace likely piped it. **Withdrawn.**
- `validate_evidence_state.py`'s `NameError` and retired-status bugs are **already fixed at HEAD**
  (diffed `038913b` vs HEAD). What remains of P4.5 is the Co-1 CLI flags and the missing DB arm —
  the Co-1 rules still scan a directory that does not exist, which is §2(a) vacuity.

---

## 7. The acceptance test

`walk_e2e.sh` (delivered in F6's design): **admit → grade → extract → judge → synthesise →
witness-link → render**, asserting that a specific value and its ref-id both appear on the rendered
page, and that the canonical database sha never moves.

**It fails by construction today. Passing it is the definition of Phase 1 done** — not a green check
battery, which is what the plan originally proposed and which would have reported success while the
page showed no number.

---

## 8. The population split — content, ruled, and sequenced

Owner ruling 2026-08-25: *"separate out into 'ambulatory' and 'wheelchair user' to start."* Design in
`logs/F5-population-split-design.md`. Footprint **33 rows**: 31 `item_population_links` (28 plain +
3 `with-upper-limb-involvement`, 28 items), 2 in the population-to-demand map (both `ALIAS`, holding
*"ambulant share"* and *"wheeled share"* since 21 July), **zero** evidence rows. One data migration,
no DDL, no `user_version` bump. **No FK to `populations` cascades** — all eleven are `NO ACTION` —
and `population_code` is under **no CHECK anywhere**.

Two constraints recorded in the ledger: `evidence_population_match.study_population` is free text
about the paper's own participants and is **never** fanned out; a link applying to both becomes two
links, and an unresolvable one is flagged, not guessed.

**"To start" is load-bearing.** Part-time wheelchair users and balance remain unrepresented and must
be named as a gap in any cell that turns on them.

---

## 9. Open owner decisions

| # | Decision | Blocking? |
|---|---|---|
| ~~1~~ | ~~The determination's grain~~ — **RULED 2026-08-25.** A specification keys from the judgment object and cross-references populations, access needs and ICF, all three modes. Population is demoted from identity to cross-reference. Adds **P1.0** below. | Resolved |
| ~~2~~ | ~~The split's code strings and fan-out~~ — **RULED 2026-08-25.** `AMB` / `WHEEL`; the 31 links fan out to 62. | Resolved |
| ~~3~~ | ~~The §R8 rename of the demand layer~~ — **RULED 2026-08-26.** Schema rename **plus** a `retired-vocabulary.yaml` entry, in that order. Adds **P0.6**. | Resolved |
| 4 | `opus_reviewed`: delete (recommended) or build render gating | No |
| 5 | P1.8's min/max aggregation rule as stated doctrine | Blocks P1.8 |
| 6 | Gap-id go-forward format; edit-form on the ratified DR; resurrecting the Template-3 room tables | No |
| 7 | Whether a freeze condition returns | No — deferred to a later DR |

## 10. What this plan recommends deleting rather than fixing

`connections.opus_reviewed` · `PILOT_CELLS` · `room_page.py`'s three fictional sections · the
runbook's dead companion-UPDATE block. Per CLAUDE.md §1, deleting is as cheap as adding and needs
evidence, not permission — the evidence is recorded against each.
