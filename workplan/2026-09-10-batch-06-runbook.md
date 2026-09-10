# The batch-06 runbook — base → research → evidence → judgment → specification

Supersedes `decisions/DR-2026-08-19-research-restart-operative-instrument.md` §12.1, which
`workplan/2026-09-10-road-to-batch-06.md` (B2) found stale in three ways: step 4 said "No CLI;
scratch SQL" (`add-candidate` exists), step 7 ordered a hand-SQL companion UPDATE (`add-source`
now takes `--url`/`--pages`/`--doi-resolution-outcome` directly — the rehearsal below applies
cleanly with **zero** UPDATE statements, not one), and no step named `observe-term`, `add-term`,
`add-parameter`, `adjudicate-term` or the determination engine (`scripts/assess/assess_cell.py`),
none of which existed when §12.1 was written.

Every command below was executed for real, on a scratch copy of the canonical DB, and
`sha256sum data/guidebook.db` was identical before and after.

**Two "expected" blocks were NOT reproduced by the rehearsal that wrote them**, found by an
adversarial pass following this file literally on 2026-09-10 and corrected here: step 6a's insert
count (stated 23, the commands below yield 22 — row-delta and capture both), and HAZARD 4, whose
mechanism was stated backwards. Read an "expected" block as what the walk produced, and if yours
differs, trust yours and correct this file.

**This is a mechanics runbook, not a claim that batch 06's determination is believable.**
`workplan/2026-09-10-road-to-batch-06.md`'s HEADLINE is still true after this commit:
`assess_cell.gather_sources()` gathers by **slug**, not by `(ref_id, parameter_id)` — B4 is not
done here. Following every step below to the letter still anchors a `stated` cell on every source
linked to the slug, not on sources that actually extract the parameter under determination. Do not
read a COMPLIANT gate as a sound determination; it proves the DoD's 15+ mechanical rules, which is
a different claim.

## Conventions

- **Session id, two forms (CLAUDE.md §7).** The bare stem — `session_2026-09-10-batch-06` — is
  what every `--session` flag on `db.py`/`assess_cell.py` takes and what lands in `session` /
  `created_by_session` columns. The same id with `.md` appended —
  `session_2026-09-10-batch-06.md` — is what `emit_data_migration.py --session`,
  `citation_mining_completeness.py --session`, and the two pointer files
  (`sessions/LATEST`, `sessions/LATEST-RESEARCH`) take. **Passing the wrong form does not error —
  it scopes a gate to a session nothing was ever written under, and that gate passes green having
  examined nothing (CLAUDE.md §5a).** Decide both forms before step 0 and never retype them.
- **Scratch discipline.** `S=<scratchpad-dir>/batch06`. `cp data/guidebook.db "$S/walk.db"`; every
  `db.py`/`assess_cell.py` call below is prefixed `GUIDEBOOK_DB_PATH="$S/walk.db"` **inline** — the
  harness resets env between shell calls, so `export` alone does not protect a later call. Nothing
  below ever opens `data/guidebook.db` for write until the final, real step 6c.
- Slug used throughout: `accessible-circulation-geometry` (continuing coverage — workplan STOP
  CONDITION #5 says this needs no owner decision; a *new* slug would).

## Step 0 — pre-state (base)

```
S=<scratchpad>/batch06
SESS=session_2026-09-10-batch-06
mkdir -p "$S"
sha256sum data/guidebook.db                                  # record; must equal step 6c's PRE value
cp data/guidebook.db "$S/walk.db"
python3 scripts/audit/research_batch_dod.py --selftest        # SELFTEST: PASS, 19/19 (18 + R10b, this commit)
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/audit/research_batch_dod.py --session "$SESS"
```
**Expected:** `--selftest` prints `SELFTEST: PASS — gate rejected the corpus AND all 19 seeded
rules fired`. The empty-session probe exits 1 with **three** failures — `R1`, `R9a`, `R9b`, both
of the latter reading `NOTHING IN SCOPE` — not the single `R1` DR-2026-08-19 §12.1 claimed; R9a/R9b
did not exist when that line was written. Any *other* rule firing on an empty session means the
session id is contaminated (reused from a prior run) — stop and pick a new one.

## Step 1 — base: mint the parameter (THE SUBJECT, owner 2026-08-26)

A parameter is minted from a phrase a source already uses — `observe-term` requires an **admitted**
source, so step 1 borrows one already in the corpus (here `REF-00784`) purely to name the concept;
this source is not thereby claimed as evidence for the cell (that comes from step 2's own
admission and step 3's harvest on it).

```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py observe-term \
  --ref-id REF-00784 --surface-form "corridor clear width" --language EN \
  --locator "p.4" --context-quote "minimum clear width of the corridor measured between handrails" \
  --session "$SESS"
```
**Expected:** `{"observation_id": <N>, "created": true}`. **Set `OBS` from that JSON** — do not
re-query for it. There is no `sqlite3` CLI in this container (CLAUDE.md §4), and the value is
already in the output:
```
OBS=$(GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py observe-term ... | python3 -c \
  "import json,sys; print(json.load(sys.stdin)['observation_id'])")
```
Every later `$VAR` in this runbook is set the same way, from the JSON of the step that minted it:
`$TERM` from `add-term`'s `term_id`, `$PID` from `add-parameter`'s `parameter_id`, `$E` and `$N2`
from `log-search`'s `exec_id`, `$REF` from `next-id ref`'s `next_id`.

```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py add-term \
  --from-observation "$OBS" --canonical-en "corridor clear width" \
  --rationale "names a design parameter not yet in terms" --session "$SESS"
```
**Expected:** `{"term_id": "TERM-0NN", "canonical_en": "corridor clear width",
"adjudication_id": 1, "from_surface_form": "corridor clear width", "from_ref_id": "REF-00784",
"dry_run": false}`. `add-term` itself performs the NAMES-NEW adjudication — a second, separate
`adjudicate-term` call for this observation is refused (already adjudicated).

```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py add-parameter \
  --term-id "$TERM" --session "$SESS"
```
**Expected:** `{"parameter_id": 1, "term_id": "TERM-0NN", "canonical_en": "corridor clear width",
"status": "active", "provenance": "adjudicated", "adjudicated_by": 1, "outcome": "NAMES-NEW",
"dry_run": false}`. Record `parameter_id` — every later step keys on the integer, not the term id.

## Step 2 — research + evidence: search, admit, stage

```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py log-search \
  --slug accessible-circulation-geometry --language EN \
  --query-text "corridor clear width wheelchair" --engine pubmed --depth-method scoping \
  --session "$SESS" --target-tier 1 --target-evidence-type clinical --target-scope high_control \
  --prior-expectation "expect a handful of anthropometric studies" \
  --results-found 3 --results-screened 3 --results-admitted 0 --mining-direction none
```
**Expected:** `{"exec_id": <E>, "slug": "accessible-circulation-geometry", "admitted": 0,
"dry_run": false}`.

**Mint the ref_id — never by hand (CLAUDE.md §4).**
```
REF=$(GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py next-id ref | python3 -c "import json,sys;print(json.load(sys.stdin)['next_id'])")
```
**Expected:** `REF-NNNNN`, one past the live high-water mark. This is the fix landing in this same
commit (item 3) — before it, `next-id` offered only `{connections,gaps,terms,conflicts}` and
`add-source` refused any hand-picked id by *naming* `dbcore.next_ref_id(conn)` rather than a
command to run.

**⚠ RETRIEVE BEFORE YOU ADMIT. THIS IS THE STEP THE PROJECT HAS ALREADY FAILED.** On 2026-08-19
all five sources in the first research batch were stored with **invented co-authors** — including
the deletion of autistic community co-authors from a Co-1 paper whose Co-1 warrant *is* their
co-authorship. **Six gates passed it**, because each asked whether the author fields were
*populated*, never whether they were *true* (CLAUDE.md §5(c)). Nothing below detects that; the
retrieval log is what does.

**CORRECTED 2026-09-10 — the two commands this block carried do not exist.** `retrieval_log.py`
has no `--fetch`, no `--doi` and no `--ref-id`; its whole CLI is `--session` plus one of
`--verify-authors` / `--backfill` / `--reconstruct-manifest` (`retrieval_log.py:729-733`), and
`workplan/2026-08-20-provenance-walk-execution-plan.md:485` had already recorded *"`retrieval_log.py`
has **no fetch subcommand**"*. **Retrieval is a Python call, not a flag** — the module's own USE
block (`retrieval_log.py:31-38`) is the sanctioned form, and both forms below were executed on
2026-09-10 against the live corpus before being written here.

```
python3 - <<'PY'
import sys; sys.path.insert(0, 'scripts/research')
from retrieval_log import fetch
msg = fetch("https://api.crossref.org/works/<doi>", session="<SESS>",
            purpose="crossref metadata for <REF>")["message"]
print(msg["title"], [(a.get("family"), a.get("given")) for a in msg.get("author", [])])
PY
```
`fetch()` writes the raw bytes and a manifest line **before** it returns, so a caller cannot act on
one payload and log another. Persist FIRST, then take every bibliographic field from the bytes you
received — never from memory, never from a search-result snippet. After admission:
```
python3 scripts/research/retrieval_log.py --verify-authors --session "$SESS"
```
**`--session`, not `--ref-id`.** The pass is corpus-wide and offline: it diffs *every*
`evidence_sources` row against the payloads logged under that session, matched by DOI, and names
what it could not examine rather than passing over it. **A `VERIFIED` standing with no payload
behind it is the fabrication shape, and it passes R9a/R9b/R10 green.**

```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py add-source \
  --ref-id "$REF" --author "Smith|Jane" --year 2020 --title "..." --tier 1 \
  --doi "$DOI" --url "$URL" --evidence-type clinical --scope high_control \
  --metadata-quality COMPLETE --verification-status VERIFIED --verification-method tool \
  --verified-by-tool crossref --doi-resolution-outcome RESOLVED \
  --slug accessible-circulation-geometry --local-ref-id 1 --session "$SESS"
```
`$DOI` and `$URL` are the real values from the payload above. The placeholder `10.9999/...` this
example carried until 2026-09-10 was itself the defect being described: it admitted a fabricated
DOI as VERIFIED, and the gate passed it. Passing `--url` is also what makes the walk exercise the
`R10b` this same commit added — without it the runbook never tested its own new rule.
**Expected:** `{"ref_id": "REF-NNNNN", "linked_slug": "accessible-circulation-geometry",
"dry_run": false}`. **`--verification-status` is a CLI choice of `{VERIFIED,UNVERIFIED}` but the
column itself accepts NULL if the flag is omitted — always pass it.** Since this commit, omitting
it (or admitting a URL-bearing source with it left NULL) fails the gate's new `R10b`, which exists
because that exact condition is what wakes the scheduled `verify-urls` cron and pushes a DB blob to
`main` (workplan B3). No companion hand-SQL UPDATE is needed: `--url`, `--pages`, and
`--doi-resolution-outcome` are all real flags today.

```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py add-candidate \
  --exec-id "$E" --found-under-slug accessible-circulation-geometry \
  --disposition PENDING-VERIFICATION --title "..." --session "$SESS"
```
**Expected:** `{"candidate_id": "<N>", "dry_run": false}`. `--disposition` is live vocabulary off
the column's own CHECK — `ADMITTED|MISCELLANEOUS|OUT-OF-SCOPE|PENDING-VERIFICATION|REHOME`; a
value outside that set is refused with the CHECK spelled out, nothing written.

## Step 3 — evidence: harvest the concept AS THE SOURCE WRITES IT (D-0173)

```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py observe-term \
  --ref-id "$REF" --surface-form "clear passage width" --language EN \
  --locator "Table 2" --context-quote "clear passage width for a manual wheelchair user" \
  --session "$SESS"
```
**Expected:** `{"observation_id": <N2>, "created": true}`. Verbatim, unjudged — R11's "harvest at
evidence" half. `research_batch_dod.py`'s `R11-harvest` fails any admitted source with zero
`observed_terms` rows, so this step is not optional on a real batch.

## Step 4 — judgment: adjudicate the harvested phrase (D-0173)

```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py adjudicate-term \
  --observation-id "$N2" --outcome NAMES-EXISTING --term-id "$TERM" \
  --rationale "same concept as corridor clear width" --session "$SESS"
```
**Expected:** `{"adjudication_id": <N>, "outcome": "NAMES-EXISTING", "contested": false}`.
`--outcome` is live vocabulary from the column's own CHECK (`NAMES-NEW|NAMES-EXISTING|NOT-OURS|...`);
`NAMES-EXISTING`/`NAMES-NEW` require `--term-id`, refused otherwise. This is the crossing step
owner ruling 2026-08-27 assigns to judgment, not evidence — the phrase was only *recorded* at step
3; here it is decided.

**Also judgment: grade population-of-study vs population-served (R13).**
```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py add-population-match \
  --ref-id "$REF" --target-population MOB --study-population "manual wheelchair users n=30" \
  --match-grade EXACT --session "$SESS"
```
**Expected:** `{"match_id": "<session[:24]>-<ref>-<pop>", "dry_run": false}`. **`db.py:3435` truncates the
session to 24 chars** — e.g. `session_2026-09-10-batch-REF-00979-MOB`. Two sessions sharing a
24-char prefix produce ids that look identical; `db.py:3437-3441` suffixes on collision so nothing
is lost, but the id is not the plain template it appears to be.
`--target-population` is a `populations.population_code` (the identity lens; codes AND names, per
CLAUDE.md §6 — never bare axis codes). `db.py add-population-match` does **not** enforce
uniqueness on `(ref_id, population)` — that refusal is deliberately absent (CLAUDE.md §4); a
second, dissenting grade lands as a second row on purpose.

**Also research: the citation-mining pass R2 requires (a deferred one still counts).**
```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py log-mining \
  --slug accessible-circulation-geometry --ref "$REF" --direction backward \
  --deferred-reason "mining deferred to next pass" --session "$SESS"
```
**Expected:** `{"logged": true, "connections": 0, "dry_run": false}`.

**Also research: R1's Co-1 pass (a genuine, well-formed zero-yield satisfies it).**
```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/db.py log-search \
  --slug accessible-circulation-geometry --language EN \
  --query-text "wheelchair corridor width DPO lived experience" --engine web \
  --depth-method scoping --session "$SESS" --target-tier 1 --target-evidence-type co1 \
  --prior-expectation "expect little" --results-found 0 --results-screened 0 \
  --results-admitted 0 --mining-direction none \
  --findings-note "genuine absence in index searched"
```
**Expected:** `{"exec_id": <E2>, "slug": "accessible-circulation-geometry", "admitted": 0,
"dry_run": false}`. A zero-yield row with **no** `findings_note` fails R14 — the note is what
distinguishes "well-formed, nothing there" from "the query itself was broken."

## Step 5 — specification: the engine determines ONE cell

```
GUIDEBOOK_DB_PATH="$S/walk.db" python3 scripts/assess/assess_cell.py \
  --db "$S/walk.db" --emit-sql "$S/cell.sql" --parameter-id "$PID" \
  --slug accessible-circulation-geometry --identity MOB \
  --session "$SESS" --stamp "2026-09-10 00:00:00" --report-json "$S/cell.json"
```
**Expected (stdout):**
```
param 1×MOB      stated       basis=T1+CO1+T2   scale=population refs=6 rso=0 cfo=0 sha=<12 hex>

1 cell(s) determined; SQL artifact: <S>/cell.sql
REPLAY through emit_data_migration.py -> migrate_db.py, never by hand.
```
`--stamp` is an INPUT, never `now()` — the engine run twice on the same inputs must be byte-
identical (verified separately; not part of this walk). `cell.sql` holds 8 `INSERT`s: 1
`convergence_assessment` (synthesis), 1 `specifications` (specification), 6
`specification_source_links` (the junction — H01/H02 need both the JSON and the junction row per
entry, not just `governing_refs`).

**⚠ HAZARD — do not apply `cell.sql`.** `assess_cell.py` wrote those 8 rows straight into
`$S/walk.db` (the scratch DB it ran against). Step 6a's `emit_batch_sql` diffs that *same* scratch
DB against canonical, so `batch.sql` **already contains** every row `cell.sql` contains, alongside
everything steps 1-4 wrote. Feeding `cell.sql` into `emit_data_migration`/`migrate_db` as well is
a double-insert: reproduced in this commit's rehearsal, it fails
`UNIQUE constraint failed: convergence_assessment.convergence_id` on replay. `cell.sql` is a
by-product for eyeballing the engine's own SQL; discard it once `--report-json` and the printed
line have been read.

**⚠ HAZARD — no re-determination path.** `idx_spec_row_identity` is a UNIQUE index on
`specifications(parameter_id, COALESCE(identity_code,''), COALESCE(icf_code,''),
COALESCE(needs_code,''), COALESCE(medical_code,''))`. Running `assess_cell.py` a second time for
the *same* parameter × lens combination is refused **at engine time, at step 5** — not at apply
time. The engine does NOT re-emit: it prints a `REFUSING:` line naming the standing
`specification_id`, its state and the session that wrote it, exits 1, and **writes no `--emit-sql`
file at all**. Verified twice on 2026-09-10, including the real batch-07 shape (a fresh copy of the
post-migration DB, new session, new stamp). This file said the opposite until the adversarial pass
executed it. Batch 06 is the first determination of this cell; a batch 07 that revisits it needs a
supersede design (an owner decision this runbook does not make — workplan DELIBERATELY WAITING).

> **What changed on 2026-09-10, later the same day.** The refusal used to arrive as an uncaught
> `sqlite3.IntegrityError: UNIQUE constraint failed: index 'idx_spec_row_identity'` raised from
> inside the `specifications` INSERT — a stack trace naming an index rather than a cell, after the
> whole determination had been computed, telling the operator neither that the cell was already
> determined nor that there is nothing to do about it. `assess_cell.validate_cell_undetermined()`
> now asks the question from argv, before the gather, and the engine prints its refusals as
> sentences instead of tracebacks. **The outcome is unchanged** — same refusal, same exit 1, still
> no artifact, still nothing written — so every instruction in this runbook stands. Only the
> operator's view of it moved.

## Step 6 — apply: capture, migrate, gate, regenerate — in that order

**6a — capture the delta out of the scratch DB (not the engine's own file, per the hazard above).**
```
python3 scripts/research/emit_batch_sql.py \
  --scratch "$S/walk.db" --canonical data/guidebook.db --out "$S/batch.sql"
```
**Expected:** `Wrote <S>/batch.sql — 22 insert(s), 0 update(s)` (counts differ with different
inputs; what matters is that the file contains exactly one `specifications` insert and one
`convergence_assessment` insert — the step-5 rows, captured here and nowhere else). The per-table
breakdown is NOT printed: `emit_batch_sql.py:173` prints one summary line, and the breakdown is
written as `-- <table>: N insert(s)` comment lines INSIDE the output file. Read it there:
`grep '^-- ' "$S/batch.sql"`.

**6b — name the migration file. `--session` takes the `.md` form.**
```
python3 scripts/emit_data_migration.py \
  --session "$SESS.md" --summary "batch 06: accessible-circulation-geometry parameter x MOB" \
  --input "$S/batch.sql" --output-dir scripts/migrations
```
**Expected:** prints the new path, `scripts/migrations/data_<timestamp>_2026-09-10-batch-06.sql`.
Rehearse this against a throwaway `--output-dir` first if unsure; only point it at
`scripts/migrations` once ready to apply for real.

**6c — apply. This is the ONLY canonical write of the session (CLAUDE.md §3).**
```
python3 scripts/migrate_db.py --session "$SESS.md"
```
**No `GUIDEBOOK_DB_PATH` override — this is the one call in the whole walk that is meant to touch
`data/guidebook.db`.** Rehearse it first against a scratch copy of canonical. **The rehearsal
needs `GUIDEBOOK_MIGRATIONS_DIR` as well** — `migrate_db.py:42` reads the migrations directory
from it, so without it the rehearsal can only find a migration 6b has already written into the
repo, which contradicts 6b's own throwaway-directory advice:
```
cp data/guidebook.db "$S/replay.db"
GUIDEBOOK_DB_PATH="$S/replay.db" GUIDEBOOK_MIGRATIONS_DIR="$S/mig" \
  python3 scripts/migrate_db.py --session "$SESS.md"
```
Confirm `PRAGMA foreign_key_check` is empty and `sha256sum data/guidebook.db` is unchanged before
running it for real.
**Expected:** `Done. Schema at version <N>; 1 data migration(s) applied.`

**⚠ HAZARD — regenerate BEFORE the gate, not after.**
```
bash scripts/regenerate_derived.sh
```
Run this immediately after 6c and before step 7. `pipeline_completeness_fresh` and
`evidentiary_audit_fresh` are both **blocking** `--check` gates against the tools' own output
files; skipping this step or running it after the gate leaves those files stale against the DB
migrate_db.py just changed, and both go red on the very next check run.

## Step 7 — gate

```
python3 scripts/audit/research_batch_dod.py --session "$SESS"
```
**Expected:** all rules `PASS` (18 through this commit's start, **19** from here on: R10b is new)
ending `COMPLIANT — all research definition-of-done rules met.`, exit 0. Reproduced against this
commit's rehearsal:
```
R1..R15, R9a, R9b, R10b: PASS (19 of 19)
COMPLIANT — all research definition-of-done rules met.
```

```
python3 scripts/audit/citation_mining_completeness.py --session "$SESS.md"
```
**Expected:** `VERDICT: CLEAN` with `Examined (slug-linked T1-2 sources in scope): >0` — a
`--session` value without `.md` scopes this to nothing and passes vacuously green (CLAUDE.md §7).

```
python3 scripts/run_checks.py --changed-from origin/main
python3 scripts/run_checks.py --selftest
```
Both must pass before commit, per CLAUDE.md §1.

## Step 8 — record

Write `sessions/session_2026-09-10-batch-06.md` (create the directory entry if none exists —
CLAUDE.md §6). Point both pointer files at it, **with `.md`**:
```
printf '%s' 'session_2026-09-10-batch-06.md' > sessions/LATEST
printf '%s' 'session_2026-09-10-batch-06.md' > sessions/LATEST-RESEARCH
```
If the cell's `specification_id` lands in `references/bpc-reasoning/accessible-circulation-geometry.md`,
that touch is a rule-2 synthesis path and owes `attestations/bpc-reasoning_accessible-circulation-geometry.json`
against `schemas/attestation.schema.json` in the same commit — check whether one already exists
for this artifact before writing a second (the naming is one attestation file per artifact path,
updated via its `reattestation` log, never duplicated).

## Recap of hazards (CLAUDE.md-style, gathered in one place)

1. **Id form.** Bare stem in the DB and on every `db.py`/`assess_cell.py --session` flag; `.md` on
   `emit_data_migration --session`, `citation_mining_completeness --session`, and both pointer
   files. The wrong form does not error; it scopes a gate to nothing and it passes green.
2. **Discard the engine's `--emit-sql` file** once read. `emit_batch_sql` already captured those
   rows from the scratch DB the engine wrote into; replaying both collides on
   `UNIQUE constraint failed: convergence_assessment.convergence_id` (reproduced in this commit's
   rehearsal).
3. **`regenerate_derived.sh` runs after `migrate_db.py` and before the gate.** Either check run in
   the wrong order and `pipeline_completeness_fresh` / `evidentiary_audit_fresh` (both blocking) go
   red on a DB that is otherwise fine.
4. **There is no re-determination path.** `idx_spec_row_identity` refuses a second row for the
   same `parameter_id × lens` cell. A batch that revisits an already-determined cell needs a
   supersede design first — not a second `assess_cell.py` run.
