# 2026-08-12 — Adversarial review of commit #91, and a content walk on corridor width

**Status:** REVIEW — nothing in the repository was changed by this session other than the
documents it adds. No fix executed, no migration applied to the canonical DB, no promotion.
**Subject:** PR #91, merged at `356efda` — 13 commits, 8 files, +9,005 / −112.
**Method:** the audited document's own protocol (its Part 3) turned back on it — lens-separated,
default verdict REFUTED, CONFIRMED only on personal reproduction, four verdicts.
**Companions:** `workplan/2026-08-12-pipeline-walk-trial-log.md` (the complete action/IO log of
the trial, 3,865 lines) · `workplan/2026-08-12-pipeline-phase-state-map.md` (what the data looks
like at each phase and how it moves between them).
**Doctrine SHA:** `0f2f525`.

---

## Part 0 — What this review found, in one page

Commit #91 is a serious piece of work and most of it survives adversarial re-derivation. Of the
load-bearing measurements I re-ran, the great majority reproduced exactly, including the ones
that carry its biggest recommendations. **Its central conclusion is nonetheless wrong**, and the
trial is what shows it.

The audited document concludes: *"BREAK POINT: none. The row traversed all twelve stages… the
structure can carry content today, and that is the problem."*

I ran a real item — **E-08, Corridor Clear Width**, with the seven real code values the database
already holds — from stage 1 to stage 12, through the sanctioned write path. It did not
traverse. **It broke four times, and three of the four breaks are in the write path the audited
document names as the strongest component in the repository.**

| # | Break | Where |
|---|---|---|
| 1 | A migration that violates a foreign key is **committed, ledgered, and then reported as an error** | `migrate_db.py:161-183` |
| 2 | The word **"bootstrap"** appearing anywhere in a migration's comment header disables foreign-key enforcement for that migration | `migrate_db.py:174` |
| 3 | Any *other* failed migration **wedges the queue permanently** — every migration behind it is silently never attempted, and the documented remedy cannot run | `migrate_db.py:150-187` |
| 4 | **Stage 9 has no writer.** The only determination engine is a fixed-list pilot script that cannot complete a run | `scripts/assess/assess_cell.py` |

The audited walk did not find these because it wrote its rows directly into a scratch database.
Inserting a row into a table is not the same as the pipeline being able to produce it. Its own
§1.0b records the scope limit honestly — *"the walk did not exercise
`scripts/emit_data_migration.py`… the sanctioned write path itself remains untested end to
end"* — and the later §1.0f closes that gap with a **one-row payload in a table with no
downstream readers**, which is the happy path. Every break above is off the happy path.

The other headline: the trial surfaced **a wrong number in the canonical database today** —
`jurisdictional_values.value_numeric = 81.0 mm` for E-12 manoeuvring space, parsed out of the
standard designation **"EN 81-41"** in the value text. It was found in seconds by putting three
category-E items side by side, which is the one comparison nothing in the repository performs.

---

## Part 1 — The adversarial review

Verdict vocabulary is the audited document's own: **CONFIRMED / REFUTED / OVERSTATED /
UNVERIFIABLE**.

### 1.1 Factual lens — re-running the measurements

Every row below was re-executed on 2026-08-11 against `356efda`.

| # | Claim | Verdict | What I got |
|---|---|---|---|
| F1 | Deep comparison: 63 of 66 tables identical, 2 exempt, `slugs` timestamps-only, VERDICT PASS | **CONFIRMED** | Reproduced verbatim, including the `slugs` line |
| F2 | `test_db_integrity` 70/70 | **CONFIRMED** | `RESULTS: 70/70 checks passed` |
| F3 | 5 of 28 blocking checks declare a vacuity floor | **CONFIRMED** | 28 blocking; 5 with `min_items`, 23 without — which also confirms K10's "23" |
| F4 | 66 tables, 39 empty | **CONFIRMED** | 67 in `sqlite_master`, of which one is SQLite's internal `sqlite_sequence`; 39 empty |
| F5 | `deps:` declared in the registry, never read by `run_checks.py` | **CONFIRMED** | `grep -n deps scripts/run_checks.py` → nothing |
| F6 | The `governance` battery entry is malformed YAML — unquoted commas produce two junk keys and a truncated description | **CONFIRMED, precisely** | Parses to `{'deps': ['pydantic'], 'description': 'Decision protocol', 'doctrine recheck': None, 'adversarial-use.': None}` |
| F7 | `graph_audit.py:277` dereferences `None` on an empty `connections` table | **CONFIRMED** | `TypeError: 'NoneType' object is not subscriptable`, at line 277 |
| F8 | `session_pointer_resolvable` does not exist in the registry or in code | **CONFIRMED** | No hit anywhere under `governance/` or `scripts/`. CLAUDE.md §10 is wrong, as the handoff says |
| F9 | Three unguarded direct writers; seven of nine siblings import `_legacy_guard` | **CONFIRMED** | Exactly `session_2026_05_11g_replay.py`, `init_database.py`, `phase_jv_appendix_a.py`; 7 importers |
| F10 | `pip install -r requirements.txt` fails; `jsonschema` is omitted while the header claims only two dependencies | **CONFIRMED** | `ERROR: Cannot uninstall PyYAML 6.0.1, RECORD file not found` |
| F11 | "**345 SQL migrations** reproduce the committed database, in fifteen seconds" | **OVERSTATED** | 345 `.sql` files exist (53 schema + 292 data). The rebuild applies **331** — 42 schema + 289 data — because the baseline convention skips 11 pre-baseline schema files and 3 pre-cutoff data files. The reviewable replay set is 331, not 345 |
| F12 | `run_checks.py --all` → `PASS — 55 green, 9 advisory` | **SUPERSEDED BY ITS OWN COMMIT** | Now `56 green, 9 advisory`. The commit added `context_map_fresh`, which passes. The document states a total its own diff invalidates |
| F13 | The replay script's payload is "64 pre-reset rows", 45 KB | **CONFIRMED (approx.)** | 45,944 bytes; I count 66 insert/update operations across seven payload keys. The 88 in `source_slug_links_to_delete_orphans_pattern` is an 88-character *string*, not 88 rows — a natural miscount the document did not make |

**One additional factual finding of my own, not in the document.** The `data_migrations` ledger
holds **314 rows**, of which **23 correspond to no migration file at all** (e.g.
`cutover_evidence_sources_v2_2026-05-11`, `metadata_enrichment_columns_2026-05-12`). This is
direct evidence for §1.0c's own argument that 16 scripts have written the DB outside the
migration system — and it is a real qualification on that section's recommendation. If the
committed binary is retired on the grounds that "the SQL migrations are the reviewable form",
23 historical writes have no reviewable form; they survive only because migration 012's baseline
dump froze their effects. That should be said explicitly in the D2 package.

**And one hazard the document does not name.** `migrate_db.py:111` carries
`BASELINE_DATA_CUTOFF_TS = "20260515000000"`, a hand-maintained constant that must be refreshed
whenever a new baseline is committed. Which migrations replay is therefore decided by a literal
in code, reconciled against the baseline file by nobody. That is a dual representation of
exactly the class C11 catalogues, sitting inside the mechanism §1.0c proposes to make the sole
source of truth.

### 1.2 Method / logic lens

**M1 — "No break point" does not follow from the walk that was run. REFUTED.**
The claim is that a synthetic row traversed all twelve stages. It did — but stages 4, 5, 7, 8
and 9 were traversed by direct `INSERT` into a scratch database, not by the pipeline. The
document knows this and says so in a scope note, then draws a whole-structure conclusion from
it anyway, and that conclusion is the first line of the handoff. Part 3 is running the
trial that tests this claim; it broke four times.

**M2 — The "free today" window argument is sound in general and has a counter-example. OVERSTATED.**
The argument — every migration is cheapest with the tables empty — is correct for the two
migrations §1.0 names, and I verified both are constructible today. But **empty is not
neutral**, and the trial found the case that proves it: `assess_cell.py:426-429` computes the
next gap id as `max(existing)+1` with `default=0`, so with `gaps` at zero rows it returns
`GAP-1`, and `schemas/evidence_state.py:164-169` requires three or four digits. **The clean-room
reset broke the determination writer.** Before the reset the counter was in the three hundreds
and produced valid ids. The document's framing — empty state as pure opportunity — misses that
emptiness is also a state the code was never tested in, and the failure is invisible precisely
because nothing runs.

**M3 — The binary-retirement recommendation is well-argued and its blocker is understated. CONFIRMED with a caveat.**
§1.0c's case is strong and the measurements behind it reproduce. The caveat is F11 plus the 23
ledger-only migrations: after retiring the blob, the rebuilt DB is defined by 331 replayable
files plus a hand-maintained cutoff constant, and 23 historical writes exist only inside a
baseline dump. That is still far better than an opaque binary. It should be stated in the
proposal rather than discovered afterwards.

**M4 — §0.2 is titled for a stronger claim than it makes. OVERSTATED (presentational).**
The heading is "Correction log — what the antagonist pass **killed**", and the preamble says
"**Four** of this document's own first-draft proposals were killed". The table lists **eleven**
rows, of which four are FATAL, one REFUTED, and six OVERSTATED — that is, six were corrected,
not killed. The session record and handoff both then quote "eleven … corrected or killed",
which is right. The document's own front matter undersells and mislabels its best feature.

**M5 — Structural degradation in the deliverable itself. CONFIRMED.**
Heading levels are consistent as `### 2.1` … `### 2.9` for stages 1–9, then collapse: stage 10
onward emits bare `## (a) Tools, tables, methodology` and two `# STAGE 11` / `# STAGE 12` H1s
inside a document whose H1 is the title. In a 6,775-line document that is the difference between
a navigable outline and a wall.

### 1.3 Vacuity lens — applied to the commit's new apparatus

**V1 — `context_map_fresh` is honestly built and honestly registered. CONFIRMED.**
It passes at HEAD, it is advisory, it declares `min_items: 1`, and the registry note's
justification for that floor ("the subject is one file that always exists, so an empty subject
is a real failure and not a ratified-empty state") is exactly the distinction the repo
adjudicated on 2026-08-06. The three defects the commit message says were caught in the
generator before it shipped — the `HEAD` sha, `DELETE FROM` counted as a writer, set-iteration
key order — are all real classes of defect and all genuinely absent from the shipped file. This
is the best-executed part of the commit.

**V2 — `register_integrity_check` still reports `SELFTEST FAILED`. CONFIRMED, consistent with the document.**
`--all` shows `**SILENT — MUTATION MISSED**: COMPLETENESS: a whole cell section deleted`. The
document's correction log item 11 settles this by experiment as an empty subject rather than a
logic bug, and item 9 records that at HEAD no document is evaluated. Both hold. Worth noting
that the check therefore reports a red selftest on every run for a reason a reader cannot infer
from the output.

**V3 — `site_pages_fresh` lists `site/specs/e-08.html` as stale.** Confirmed, and directly
relevant: the corridor page in the repository does not match what the generator produces from
the current database.

### 1.4 Doctrine lens — the segments the session left unreviewed

The session record states that stage segments **1–3 and 7–9 were never doctrine-reviewed** and
should be assumed to carry similar defects. I ran that pass. It does not need to be inferred —
the trial exercised those exact stages, and the doctrinal defects are in the code, not the prose.

**D1 — Stage 8 is where doctrine is least defended, and the document understates it.**
`evidence_population_match.target_population` has no key. The document says so. What it does not
say is *what shape the un-keyed value takes*. I inserted `WHEELCHAIR-USERS-GENERALLY` and it was
accepted — a broad umbrella of precisely the kind `governance/functional-taxonomy.md` §3.3, the
2026-07-22 work-from-axes rule and `DR-2026-07-22-work-from-axes` prohibit. Worse, it is
**silently ignored** rather than rejected: `assess_cell.py:180` attributes a match by
`re.search(rf"\b{population}\b", target, re.I)`, so a string containing no population code
matches nothing and reads as *absent* rather than as *malformed*. The one column that most needs
the taxonomy's discipline is the only one that enforces none of it, and its failure mode is
invisibility.

**D2 — Stage 9's marker band has no renderer at all.** Covered in Part 3; the short form is
that Option A's flagged weak band `○` is required for a code-consensus determination, and the
rendered page carries no `●`, `◐` or `○` anywhere.

**D3 — Co-1 co-primacy: the document's finding is right and its remedy is available.**
`evidence_type='co1' ⇒ tier=1` has no CHECK. I confirm `validate_source_co1_fields()` scans
`data/sources/*.yaml`, which does not exist. The remedy is cheap and the document does not name
it: this is a one-line table CHECK, in the `D` enforcement rung the document itself proposes
adding to CLAUDE.md §2's spectrum. With `evidence_sources` at zero rows it is constructible
today with no backfill.

### 1.5 Cross-artefact consistency

| # | Finding | Verdict |
|---|---|---|
| X1 | `sessions/handoff-next-session.md` header still reads `HEAD at handoff: 804a4bf` and `PR: #91 (open)`; the final commit is `006a8e8` and the PR is merged | **CONFIRMED** — the handoff was edited by `006a8e8` without updating its own header |
| X2 | The session record cites `attestations/sessions_session_2026-08-11-structural-integrity-audit.json` | **CORRECT** — that is the file that shipped |
| X3 | The commit message for `006a8e8` says "doctrine passes complete"; the handoff it ships still lists "Doctrine-lens passes on stage segments 1–3 and 7–9" as outstanding | **NOT A CONTRADICTION** — the completed passes are on 4–6 and 10–12, and both texts say so. Reads as one on a skim; worth a clause |

---

## Part 2 — The questions the handoff raises

### 2.1 The one question it puts to the owner directly

> *"if the intent is that `site/` shows only determined cells and coverage lives elsewhere, the
> fix is wrong and the doctrine text needs amending instead."*

**The premise is false, so the question does not need answering as posed.** §1.0h says a
population linked to an item but holding no determination is "absent from the rendered table
entirely — not marked thin, not marked pending, not there."

I rendered E-08 with thirteen linked populations and determinations for two. **All thirteen
render**, in an `Applicable populations (13)` table drawn from `item_population_links`, each with
its applicability. LPA, BLIND, DEM and the rest are present on the page. They are absent from the
*determinations* table, which is correct — they have no determination.

So the erasure §1.0h names is not happening. What *is* happening is worse and different, and
Part 3 documents it: the determination that exists renders **without its value, without its
evidence marker, without its governing sources, and — for the pending cell — without its gap
link**. The populations survive; everything that would let a reader check the claim does not.

**Recommendation:** withdraw §1.0h as stated, keep its doctrinal reasoning, and re-aim it at the
four render gaps in Part 3.4. Do not amend the doctrine text; the doctrine is right and the
renderer is behind it.

### 2.2 The decision table (D1 / D2 / deep gate / binary DB)

The sequencing logic holds and I would not change it. Two amendments:

- **D2 should absorb F11 and the 23 ledger-only migrations** before it is ruled on. The
  exemption question is larger than `url_verification_runs`: it is "what fraction of this
  database's history exists as reviewable SQL", and the honest answer is 331 files plus a
  baseline dump plus a hand-maintained cutoff constant.
- **The deep-gate promotion should be paired with a fix to `migrate_db.py`'s FK handling**, not
  just with D2. Promoting `migration_reproducibility_deep` closes the *fabrication* hole. It does
  nothing about Break 1, where a foreign-key violation is committed and ledgered — because after
  that commit, the rebuilt DB and the committed DB agree. They agree on the bad row.

### 2.3 The two "free today" migrations

Both verified constructible. `evidence_population_match` is at 0 rows, so the FK on
`target_population` can be added with no backfill and no orphan sweep. `evidence_cell_state` is
at 0 rows, so a `doctrine_sha` column is free. **Do both.** The trial gives the population FK a
sharper justification than the document's: without it, the column accepts umbrellas that
doctrine prohibits, and they fail silently rather than loudly.

### 2.4 The three no-decision items

All three verified real (F5, F7, F9) and all three should ship. I would add a fourth of equal
cost and greater consequence: **`migrate_db.py`'s FK check must run before `commit()`, not
after.** It is a re-ordering of four lines.

---

## Part 3 — The corridor-width walk

Full action/IO log: `workplan/2026-08-12-pipeline-walk-trial-log.md`. Data-state-per-phase:
`workplan/2026-08-12-pipeline-phase-state-map.md`.

### 3.0 Method and evidentiary status

**This is a structural trial, not a research batch.** The values are copied from
`jurisdictional_values` rows the repository already holds for E-08; they were not independently
re-retrieved, no DOI was pre-checked, no locator re-verified. Under R3/R9/R10 **nothing in the
walk is admissible as evidence** and none of it may be promoted. `REF-9xxxx` are trial
identifiers in a scratch database.

The walk ran in a byte copy of the repository at
`/tmp/…/scratchpad/walk`, through `emit_data_migration.py` → `migrate_db.py`, the sanctioned
write path. 23 migrations were emitted. **The canonical clone was never written** —
`git status` clean throughout, verified at the end.

E-08 was chosen for reasons that are not arbitrary: it is a real item, it is the only exemplar
wired in `index.html`, and it carries seven real code values, every one `tier=6`,
`is_code_minimum=1`. That makes it the exact case where Option A bites.

### 3.1 The four breaks

**Break 1 — the foreign-key guard is a post-commit alarm.**
`migrate_db.py:161-183` runs: `PRAGMA foreign_keys = OFF` → `executescript(sql)` → insert the
ledger row → **`conn.commit()`** → `PRAGMA foreign_keys = ON` → `foreign_key_check` → raise. The
`except` calls `conn.rollback()`, which by then rolls back nothing.

Observed: a `search_admissions` row referencing a nonexistent source. Exit code 1, a traceback,
`ERROR: 1 new FK violations` — and `search_admissions` 0 → 1, `data_migrations` 318 → 319. The
operator is told the migration failed. The row is in the database and the ledger says it was
applied.

**Break 2 — the word "bootstrap" disables foreign-key enforcement.**
`migrate_db.py:174`: `is_bootstrap = "BOOTSTRAP" in body[:500].decode(...).upper()`. When true,
FK violations are downgraded from `ERROR` to `WARNING` and the migration is accepted with exit
code 0. `emit_data_migration.py` writes the session name and the `--summary` string into a
comment header inside those first 500 bytes. I re-submitted the identical violating insert,
changing only the summary wording to *"bootstrap the trial admissions table"*. It was accepted.
**Whether the database enforces referential integrity is decided by the prose a session types
into `--summary`.** It is documented nowhere and `emit_data_migration.py` does not warn.

**Break 3 — one failed migration voids every migration behind it.**
Twice, from two independent authoring mistakes. A migration that fails for any reason other than
an FK violation writes no ledger row, so it stays pending; `apply_data_migrations` iterates in
timestamp order and re-raises on the first failure. Four correct migrations behind it were
emitted, queued, and **never attempted**, while the transcript recorded apparent progress.

Two consequences. First, **the documented remedy cannot execute**: "fix forward with a new
compensating migration" is impossible when the compensating migration is queued behind the
failure. All three available escapes — delete the file, edit the file, hand-write the ledger row
— break a stated rule. I took the first, twice, and recorded it as a deviation. Second, the
error names the *wrong* migration: a session that emits a migration, runs the applier, and reads
an error about a file from two stages ago has every reason to think its own write is fine.

The asymmetry is the sharp part. **The failure mode that corrupts data lets the queue proceed;
the failure mode that writes nothing stops everything.**

**Break 4 — stage 9 has no writer.**
`scripts/assess/assess_cell.py` is the only determination engine. Its cells are a module-level
literal, `PILOT_CELLS`, holding seven hardcoded `(item, population, slug)` triples — so the
`item_bpc_links` bridge is never consulted, the slug is supplied by hand, and **E-08 × MOB
cannot be reached**. Then the run aborts anyway, on `GAP-1` (see M2).

*A correction to my own first pass:* I attributed the abort to the retired population code `NEU`
in `PILOT_CELLS[6]`. The traceback shows it dying at `PILOT_CELLS[0]` on the gap-id pattern. My
conclusion held and my mechanism was wrong — which is the failure the audited document's Part 3
§3.7 names as its main methodological lesson, recurring inside a review of that document, on the
first prediction I made without reading the traceback. The `NEU` entry is a real latent defect;
the run never reaches it.

### 3.2 What the render actually does

With the determinations hand-written (the only remaining route), `build_site.py --only E-08`
exits 0 and produces a page that gets several hard things right:

- all thirteen populations, with applicability;
- a determinations table carrying **State**, **Tier basis**, **Code floor only**, **Regulatory
  stratum only** and **Falsification condition** — so the Option A flag *does* have a reader,
  and it rendered `yes`;
- an honest-banner fallback where a determination has no governing sources.

And four things wrong:

| # | Missing | Why it matters |
|---|---|---|
| R1 | **The value.** The determinations table has no column for `value_min`/`value_max`/`value_unit`. `1200` and `1500` appear on the page only inside the free-text falsification condition, and inside the item's own title string | The number the pipeline exists to produce never reaches the page as a value |
| R2 | **The evidence marker.** No `●`, `◐` or `○` anywhere. Option A requires a T6-only determination to render at the flagged weak band `○`; `tier-system.md` §5 and CLAUDE.md §6 say unmarked is an error | The doctrinal band system has no renderer |
| R3 | **The gap link.** The DEAFBLIND cell renders `pending` with em-dashes. `GAP-901`, which it points to, does not appear, and neither does `[BEST-PRACTICE-PENDING]` | Doctrine requires the pending token plus a gap link |
| R4 | **The governing sources.** Seven refs in `governing_refs`; zero rows in `cell_source_links`; the renderer reads the junction, so the page states the determination has **no governing sources** | The honest banner makes a false statement — C11 confirmed, with the sting that the honesty mechanism is what misreports |

R4 deserves emphasis. `spec_page.py`'s own comment says the junction exists because the JSON
array meant "every page it produced cited nothing at all while presenting a confident
determination". The junction fixed the reader. Nothing fixed the writer, so the first real
determination reproduces the original defect through the new mechanism.

### 3.3 Trial B — turning radius and swept path

**These are not two opinions about one number. They are two measurement paradigms for one
demand.** A static turning circle is the diameter a chair rotates within, stationary. A swept
path is the envelope traced while moving through a turn, and varies with approach angle, speed,
device class and technique. A value from one is not commensurable with a value from the other
without stating which question is being asked.

**The schema knows this.** `source_value_extractions` carries `measurement_paradigm` with a
CHECK vocabulary including `static_turning_circle`, `swept_path_dynamic`, `static_clearance`
and `anthropometric_percentile`, plus `device_class`, `root_type`, `echo_of` and a `contested`
flag. This is the most sophisticated part of the data model.

**Nothing reads it.** I filed two T1 clinical sources, one per paradigm — 1500 mm static circle,
1830 mm dynamic swept path, same parameter, same population, same item. Then:

- `classify()` in `assess_cell.py` buckets sources by `tier` and `evidence_type` **and nothing
  else**. Grepping the whole file for `measurement_paradigm`, `device_class`, `claimed_value`,
  `contested` or `echo_of` returns only comments. The engine never opens
  `source_value_extractions` at all.
- Both sources land in `b["t1"]` and both become anchors. 1500 and 1830 are not reconciled,
  ranked or flagged — they are **counted**.
- `test_db_integrity` (blocking), `validate_evidence_state` and `pmp_audit` all pass with the
  contradiction in place. A single `GROUP BY` makes it visible: `n_values 2, n_paradigms 2,
  lo 1500.0, hi 1830.0, flagged_contested 0`.

### 3.4 Connecting the concepts, and testing them against each other

I recorded the real incompatibility as a connection: *a corridor built at E-08's 1200 mm minimum
cannot accommodate either turning value, so a wheelchair user can enter a compliant corridor and
be unable to turn around in it.*

- It stores as prose in `connections.description`. There is **no numeric representation** of
  "1200 < 1500" — no operator, no unit, nothing to evaluate.
- `connection_targets.target` is `TEXT NOT NULL` with **no foreign key**. I attached
  `item:E-99-DOES-NOT-EXIST` alongside the two real items and it was accepted.
- `references/connection-reasoning/` holds one file, `_template.md`, and zero real documents
  against a workplan target of 245.

**And nothing compares two items to each other.** The comparison axes that exist are:

| axis | mechanism | state |
|---|---|---|
| population × population, **within one item** | `conflicts` (`item_code`, `pop_a`, `pop_b`), `cross-population-conflict-mapper` skill, `references/conflict-matrices/*.md` | schema real; table **0 rows**; matrices are markdown, unlinked to the DB |
| one item over time | `spec_value_probes`, `progressive-measurement` skill, `pmp_audit.py` | schema real; table **0 rows** |
| one item across eight audit steps | `item_audit_pipeline.py` — signature `--item I-01`, strictly singular | wired; `item_audit_runs` **0 rows** |
| item × item | `connections.connection_type='CROSS-ITEM'` | **0 rows**, un-keyed target, no writer, no reasoning docs |
| item consolidation | `item-consolidation-analyzer` skill | merges/splits redundant items — a *taxonomy* operation, not value reconciliation |

`items.category` is used for grouping in renders and for the `A-01…K-NN` code space. **It is
never a comparison scope.**

**What that costs, measured.** One query putting E-04, E-08 and E-12 side by side returned:

```
E-12 | Entrance Landing and Manoeuvring Space… | ISO | 81.0 | mm
```

`value_text` reads *"Min. Platform (W×D): References EN 81-41; Notes: Defers to regional
standards"*. **The numeric extractor pulled `81` out of the standard designation "EN 81-41".**
A physically absurd millimetre value sits in the canonical database, presented as a
manoeuvring-space dimension, and the first cross-item comparison anyone ran found it.

A second observation from the same query, flagged for owner review rather than asserted as a
defect: E-12's six jurisdictional values are all **platform-lift** specifications (ADA §410 /
ASME A18.1, BS 6440, EN 81-41, AS 1735.12) while the item is named *Entrance Landing and
Manoeuvring Space for Power Wheelchair Users*. "Min. Platform (W×D)" for a lift is not
manoeuvring space. If that binding is wrong, E-12's values cannot be compared with E-08's as
like quantities at all.

**A third, which no process would surface.** E-08's own title asserts **≥1200 mm**.
`references/conflict-matrices/CORRIDOR-W.md` — an Opus disposition dated 2026-03-30 — rules that
DEAF signing pairs require **≥2440 mm** and directs that this be specified as **Universal Mode**.
Same parameter, factor of two, coexisting for over four months. The matrix is markdown; the item
title is a database string; no check reads both.

---

## Part 4 — How the tools understand best practice

This answers four questions directly, because the trial produced the evidence for them.

### 4.1 Do the tools distinguish code-derived best practice from academically-derived best practice?

**Yes, and the distinction is genuinely encoded — more carefully than most of the apparatus.**

`schemas/directness.py` models a source by its **grain** and a claim by its **design scale**, and
`scale_directness(grain, scale)` returns a conditioning verdict.
`scripts/audit/matrix_consistency.py` transcribes the doctrine table and diffs it against the
code, so the two cannot drift silently:

| source grain | universal | population | person |
|---|---|---|---|
| `code` (T4/T5/T6 — standards, national frameworks, codes) | **DIRECT** | **NON-ANCHORING** | **NON-ANCHORING** |
| `aggregate` (SR/meta-analysis; Co-2) | ADJACENT | **DIRECT** | DOWN-WEIGHTED |
| `specific` (T1 clinical; Co-1; grey) | ADJACENT | **DIRECT** | **DIRECT** |

That table is the answer in one object. **A code value is DIRECT evidence for a Universal-Mode
claim and NON-ANCHORING for a population claim.** A code tells you what a jurisdiction decided to
require of everyone; it does not tell you what any population needs. Academic and Co-1 evidence
is the reverse: DIRECT at population and person scale, merely ADJACENT at universal.

So no, they are not the same, and the model's reason is precise: not "codes are worse", but
**codes answer a different question**, and using one to answer the other is a grain mismatch.

Downstream, `assess_cell.py` carries this into the determination: a T4–T6-only basis sets
`regulatory_stratum_only = 1`, `code_floor_only = 1` where T6-only, and stamps
`tier_basis = 'T6-only(regulatory_stratum_only)'`. The `v_best_practice` view then excludes those
cells from best practice outright.

### 4.2 Is consensus the same as best practice?

**No — and this is the sharpest thing the doctrine says.**
`governance/mission-and-epistemics.md` §2, as amended 2026-07-21:

> *Convergence is informative (it tells us multiple jurisdictions adopted a value) but is not
> itself strong evidence: the jurisdictions may be wrong together, or reading from a shared
> pre-evidence floor that none has updated — which is exactly why the claim sits at the weak
> band, not why it is excluded.*

Seven jurisdictions agreeing is seven observations of **what regulators decided**, and if they
copied one another, or copied a common ancestor, it may be one observation wearing seven hats.
E-08 is a live illustration: 915, 1000, 1200, 1200, 1500, 1500 mm across seven codes is not
convergence at all — it is a 64% spread that the phrase "code consensus" would conceal.

The roles consensus does play are three, and they are different from each other:

1. **Regulatory convergence (T4–T6)** — the weak band `○`. Anchors "best practice as currently
   known", **only when flagged**, never unflagged and never above `○`.
2. **Synthesis consensus (T2)** — a systematic review or a named-organisation evidence-based
   standard. Full band `●`. The move is aggregating *primary evidence*, not aggregating
   *decisions*.
3. **Professional-clinical consensus (Co-2)** and **community consensus (Co-1
   `dpo_research` / `advocacy_position`)** — co-primary, full band, and by CRPD Art. 4.3 Co-1 is
   co-primary with T1, not subordinate to it.

The word "consensus" covers all four. The tier system's entire job is to keep them apart.

### 4.3 So how *will* the pipeline adjudicate turning radius against swept path?

**On the evidence of the trial: it will not, at three levels.**

1. **Paradigm.** The distinction is recorded in `measurement_paradigm` and read by nothing. Two
   T1 sources measuring different things are two anchors.
2. **Value.** `assess_cell.py:557-570` writes `value_min, value_max, value_unit` as
   `None, None, None`, unconditionally, and it is the only writer of `evidence_cell_state`.
   **There is no code anywhere in the repository that goes from N extracted values to one
   determined value.** The pipeline determines a *state* — `stated` / `provisional` / `pending` /
   `not_applicable`, on a tier basis — which is a real and carefully built judgement. It never
   determines a *number*. That step exists only as prose a human writes into the BPC synthesis,
   and as the parenthesis in the item's title.
3. **Cross-item.** Nothing compares two items (§3.4).

This is, I think, the most important structural fact the two trials establish, and it reframes
the audited document's governing question. "Does the structure work before content?" assumes the
structure's job is to carry a determination. For *state* it largely can. **For the value, there
is no stage** — not a broken one, an absent one. Twelve stages carry evidence to a judgement
about how well-evidenced a cell is, and then the number is written by hand.

Which is defensible! Value determination may be exactly the judgement that should stay human,
under the Opus floor. But if so it should be *named as a deliberate boundary* in the pipeline
contract, with the human step as a first-class stage that has an input contract, an acceptance
condition and an attestation — rather than appearing as three `None`s in a column list.

---

## Part 5 — Recommendations, in the order I would take them

**No decision required, and cheap:**

1. **Move the FK check before `commit()` in `migrate_db.py`.** Four lines. Closes Break 1.
2. **Delete the `is_bootstrap` prose bypass**, or key it to an explicit `--allow-fk-violations`
   flag that must be typed by a human. Closes Break 2.
3. **Give `migrate_db.py` a quarantine path** — `--skip <id>` recording an abandonment row, or a
   `migrations/failed/` directory — so a failed migration cannot void the queue behind it, and
   print `N migrations not attempted` when it aborts. Closes Break 3.
4. **Fix `next_gap_id`** to zero-pad to three digits. One line. Unblocks the determination writer.
5. The handoff's existing three: guard the three unguarded writers; wire `deps:`; fix the
   `graph_audit.py:277` crash. Plus repair the malformed `governance` battery YAML.

**Needs a decision, and the trial sharpens it:**

6. **The two free migrations** — population FK, doctrine binding. Do both now.
7. **A `CHECK` for Co-1 co-primacy** (`evidence_type='co1' ⇒ tier=1`), free at 0 rows.
8. **Render the value, the marker band, and the gap link** (R1–R3), and **make `assess_cell.py`
   write `cell_source_links`** (R4). These are implementing ratified doctrine.
9. **Rule on whether value determination is a machine stage or a human stage.** If human, write
   it into `governance/pipeline-contract.yaml` as a stage with an acceptance condition. This is
   the D-METH question the trials expose and it is upstream of most of the rest.
10. **Correct the E-12 ISO `81.0 mm` row**, and rule on whether E-12's platform-lift values
    belong to that item at all.
11. **Reconcile `CORRIDOR-W.md`'s ≥2440 mm against E-08's ≥1200 mm title.** Two stated values for
    one parameter, four months apart, neither aware of the other.

**Deferred, unchanged from the audited document's own sequencing:** branch protection alone in
its own window; the deep-gate promotion paired with D2 *and* with recommendation 1; the binary
retirement after D2.

---

## Residual uncertainty

- `[UNCERTAIN: whether E-12's jurisdictional values were always platform-lift specifications]` —
  I read the six rows and their `standard_name` fields; I did not trace the migration that
  wrote them or the session that decided the binding.
- `[UNCERTAIN: whether any renderer other than spec_page.py drops linked populations]` — §1.0h's
  claim is refuted for `spec_page.py`, which is the live generator for `site/specs/`. I did not
  test `population_page.py`, `room_page.py` or `generate_parts.py` against the same state.
- The 23 ledger-only `data_migrations` rows: I established that they exist and that they do not
  affect reproducibility. I did not trace what each one did.
- The trial's `state='stated'` for a T6-only cell is my reading of Option A as amended
  (a T4–T6-only determination *is* rendered as weak-band best practice rather than suppressed).
  If the owner reads it as `provisional`, R1–R4 are unaffected but the trial's stage-9 input is.

---

## Part 6 — Assessed against a real adjudication: swept path → corridor width

Added 2026-08-12 at owner direction. The owner put a substantive chain to the apparatus:

> *Wheelchair swept path is better than wheelchair turning radius. Wheelchair users do not turn
> in perfect circles. Following from that, different kinds of wheelchairs have different swept
> paths. Finally, the swept path of the wheelchair determines the ideal corridor width — a
> wheelchair user should be able to turn around in a corridor just like anyone else could.*

This is not one claim. It is four operations, and they fail against four different parts of the
apparatus. Assessing them is a better test of the tools than any synthetic walk, because it is
the actual work the project exists to do.

**A refinement that sharpens the assessment rather than softening the claim.** Turning around
*in a corridor* is a rotation, and its footprint depends on drive-wheel configuration — a
mid-wheel-drive power chair rotates near its own axis, a rear-wheel-drive chair sweeps a much
larger envelope, and a manual chair pivots differentially. So the governing paradigm is not
globally "swept path"; it is *the envelope of the manoeuvre the claim is about*. The schema
records `measurement_paradigm` as a property of the **source**. **There is no field anywhere for
the manoeuvre the claim concerns.** That absence is upstream of all four operations below.

### 6.1 Operation 1 — adjudicate one measurement paradigm over another

**What it requires:** a way to say "for this claim, a static turning circle is a less valid
measurement of the demand than a rotational sweep envelope", and a mechanism that acts on it.

| capability | state |
|---|---|
| record the paradigm | **YES** — `source_value_extractions.measurement_paradigm`, nine-value CHECK |
| record that two values are in tension | **YES** — `contested` flag; `echo_of` for derivative values |
| record which is *better* | **NO** — no ranking, no preference, no per-claim validity column |
| act on it in determination | **NO** — `classify()` buckets on `tier` and `evidence_type` only |

**The structural reason is worth stating precisely.** `schemas/directness.py` is the conditioning
layer, and it has exactly three dimensions:

1. **population-directness** ← `evidence_population_match.match_grade` — *was it measured on the
   people the claim serves?*
2. **value-directness** ← `reasoning_doc_citations.value_match` — *does the source actually say
   this number?*
3. **scale-directness** ← grain × claim scale — *is it the right kind of evidence for this scale
   of claim?*

The owner's argument is a **fourth dimension the model does not have: construct validity** —
*did the measurement measure the thing the claim is about?* A static-circle study and a
swept-path study are both `specific` grain at `population` scale, so `scale_directness` returns
**DIRECT for both**. Two T1 sources measuring different constructs are, to every tool in the
repository, two equally direct anchors.

**Verdict: representable as an annotation, inert as a judgement.** The paradigm can be recorded
and nothing consumes it. The trial demonstrated this — 1500 mm and 1830 mm both anchored, every
blocking gate green, `contested` at 0.

### 6.2 Operation 2 — different wheelchairs have different swept paths

**What it requires:** a determination stratified by device class.

`source_value_extractions.device_class` exists with a nine-value CHECK —
`manual_self_propelled`, `manual_attendant`, `power_chair`, `scooter`, `bariatric_manual`,
`bariatric_power`, `walker_rollator`, `mixed`, `not_device_scoped`. It is a good vocabulary and
it is exactly the right axis for this claim.

**It cannot reach a determination.** `evidence_cell_state` is keyed `UNIQUE(item_code,
population_code)`. There is no `device_class` column and no third key dimension. A cell can hold
one answer for `E-08 × MOB` and cannot hold "1830 mm for rear-wheel-drive power chairs, 1500 mm
for mid-wheel-drive, 1400 mm for manual".

The available escapes are all wrong:

- **Coin a population per device class.** A category error — a device is equipment, not a
  community — and precisely the umbrella-coining the 2026-07-22 work-from-axes rule and
  `governance/functional-taxonomy.md` §3.3 exist to prevent.
- **Use `design_scale`.** The trichotomy is `universal` / `population` / `person`. Device class
  sits *between* population (MOB is too coarse) and person (this is not individual OT
  co-design). **The Design Mode ladder has no rung for equipment-stratified specification**, and
  that is a doctrinal gap, not just a schema one.
- **Use the axis layer.** `AX-WHM` — "Wheeled movement & transfer", mechanism *"Turning,
  clearance, transfer geometry — independent and assisted"* — is `ESTABLISHED` and is the right
  concept. It is a single axis with no device stratification and `item_axis_links` carries only
  `strength_band` and a `mechanism_note`.

**Verdict: recordable at extraction, unrepresentable at determination.** This is the
phase 7 → 9 drop documented in the phase-state map, and it is the boundary where the owner's
second claim dies.

### 6.3 Operation 3 — swept path determines corridor width

**What it requires:** a value in one item derived from a value in another, with the dependency
recorded so that changing the upstream value invalidates the downstream one.

| capability | state |
|---|---|
| mark a *source-level* value as derived | **YES** — `source_value_extractions.root_type = 'derived_calculation'`, plus `root_ref_id`, `echo_of` |
| mark a *determination* as derived | **NO** — no such column on `evidence_cell_state` |
| record cell → cell or item → item dependency | **NO** — nothing anywhere |
| represent the relation itself (`E-08 ≥ f(swept_path)`) | **NO** — no formula, no operator, no unit algebra |
| invalidate downstream when upstream changes | **NO** — `derivation_sha` hashes `governing_refs + rule_version`, not upstream cells |

The only cross-item construct is `connections` typed `CROSS-ITEM`, whose `connection_targets.target`
is un-keyed `TEXT` (the trial inserted `item:E-99-DOES-NOT-EXIST` successfully), whose table
holds 0 rows, and whose reasoning corpus `references/connection-reasoning/` holds one template
and zero documents against a target of 245.

And no value would be computed regardless: `assess_cell.py` writes `value_min`, `value_max` and
`value_unit` as `None` unconditionally, and it is the only writer of `evidence_cell_state`.
**There is no arithmetic anywhere in this pipeline.**

**Verdict: entirely unrepresentable**, at every one of five levels.

### 6.4 Operation 4 — the premise that licenses the derivation

*"A wheelchair user should be able to turn around in a corridor just like anyone else could"* is
not an empirical finding. It is a **normative premise** — a parity claim — and it is what turns a
measured envelope into a specification. Without it, the swept path is a fact about chairs, not a
requirement about corridors.

The repository has exactly one column shaped to hold a statement like this:
**`access_needs.design_obligation`** — 17 rows of normative prose, e.g. *"Be perceivable and
operable without sight; text alternatives … never colour alone as a carrier of meaning."* That is
the right shape.

Two problems.

1. **There is no access-need code for space to manoeuvre.** The 17 codes are `A-AT`, `A-CALM`,
   `A-EFFORT`, `A-LOWLOAD`, `A-NOSIGHT`, `A-NOSOUND`, `A-NOSPEECH`, `A-PLAIN`, `A-PRECISION`,
   `A-REACH`, `A-SELFCARE`, `A-SIZE`, `A-STABLE`, `A-STIMULUS`, `A-TACTILE`, `A-TIME`,
   `A-TRIGGER`. `A-SIZE` is body size; `A-REACH` is reach. **Wheeled manoeuvring space has no
   access-need code at all** — it exists only as the axis `AX-WHM`.
2. **`access_needs` does not link to items.** The only tables carrying `need_code` are
   `access_needs`, `access_need_axis_map` and `access_need_icf`. The design obligation reaches an
   axis and an ICF anchor; it never reaches an item, a cell, or a rendered specification.

Compounding both: **there is no doctrine column anywhere in the database.** That is leg 4 of
`DR-2026-08-06 §1`'s four-leg promise, and commit #91 identified it correctly. The premise that
licenses this derivation is exactly the kind of thing that leg was meant to carry.

**Verdict: the right column shape exists, unattached to anything the claim touches.**

### 6.5 The doctrinal hazard the chain exposes

Suppose all four operations were implemented and the synthesis were performed. **What tier is the
resulting corridor width?**

Its input is a T1 measurement. Its derivation step is an argument. The tier system grades *how
well evidenced* a value is, and the marker bands are:

- **●** T1, Co-1, T2, Co-2, T3-clinical — "anchors outright (adjudicated evidence)"
- **◐** T4, T5 — "standards basis, not primary evidence"
- **○** T3-grey, T6, expert-consensus, thin base — "best available given current
  regulation/practice, NOT academically adjudicated"

A value **derived by sound argument from strong evidence** fits none of them. Rendering it `●`
overclaims — no one measured a corridor. Rendering it `○` misdescribes it — the band means grey
or thin, and this is neither. There is no band for *"strong evidence, plus a reasoning step that
is the project's own."*

**This is the most interesting thing the owner's chain exposes**, and it is not a bug in the
schema — it is an unfilled position in the doctrine. It is also unavoidable: a guidebook whose
stated purpose is "to get people to ask the right questions" will derive most of its
specifications this way, because primary studies measure people and chairs, not corridors. The
apparatus is built to grade *citations*. The project's actual product is *derivations from
citations*, and derivation has no tier.

### 6.6 Scorecard

| operation | represent | compute | check | render | invalidate |
|---|---|---|---|---|---|
| 1 · adjudicate paradigm | partial (annotation only) | **no** | **no** | **no** | **no** |
| 2 · stratify by device class | at extraction only | **no** | **no** | **no** | **no** |
| 3 · derive corridor width from swept path | **no** | **no** | **no** | **no** | **no** |
| 4 · attach the parity premise | shape exists, unlinked | n/a | **no** | **no** | **no** |

**The apparatus can carry the evidence for this chain and cannot carry the chain.** Every one of
the four operations is a *reasoning* step, and the twelve stages are built to move *citations*.
That is the honest answer to "does the structure work before content": for provenance and for
grading how well evidenced a cell is, largely yes. For the synthesis the guidebook exists to
publish, the stages do not exist yet.

### 6.7 What would close it, cheapest first

Each is constructible today because every table named is empty.

1. **A fourth directness dimension: construct-directness.** Add
   `source_value_extractions.claim_manoeuvre` (or, more generally, `claim_construct`) and a
   `construct_directness(source_paradigm, claim_construct)` function beside the existing three in
   `schemas/directness.py`, with its doctrine table transcribed into
   `matrix_consistency.py` so the two cannot drift. This is the operation-1 fix and it reuses a
   pattern the repo already executes well.
2. **A device-class dimension on determinations.** Either a third key column on
   `evidence_cell_state` or an explicit ruling that device stratification belongs at Person
   Mode. The second is cheaper and probably wrong — a rear-wheel-drive envelope is a population-
   level fact about a class of equipment, not an individual assessment.
3. **`evidence_cell_state.derived_from_cell_id` + `derivation_rule`**, with `derivation_sha`
   extended to hash upstream cell ids so a change upstream reddens the downstream cell. This is
   the operation-3 fix and it is the one that makes the guidebook's actual product auditable.
4. **An access-need code for wheeled manoeuvring space**, and a `need_code` link from
   `access_needs` to `items` — so `design_obligation` can reach a specification. Curated *from*
   `AX-WHM`, per the work-from-axes rule, not coined as an umbrella.
5. **A doctrine binding on determinations** — already recommended as Part 2.3, and the parity
   premise is the concrete case for it.
6. **An owner ruling on the tier of a derived value** (§6.5). This is D-DOCT, owner-only, and it
   gates the honest rendering of every specification the project will publish.

---

## Part 7 — Adversarial critique of Part 6, and the four-dimension adjudication

Added 2026-08-12 at owner direction, after the owner corrected a factual claim in §6.5. Part 6
is left standing above and corrected here rather than edited in place, per AQ5 — a document that
quietly absorbs its own corrections teaches the next session nothing.

### 7.1 Methodology critique of Part 6

**C1 — §6.5 inferred a doctrinal absence from a repository search. WRONG, and the error class is
one this repo has a rule against.**

§6.5 concluded that "a value derived by sound argument from strong evidence fits none of
[the bands]" and that "derivation has no tier". The owner states the marker scheme in fact
carries a **triangle for derived values, with the same fill scheme** — so ▲ / ◭ / △ parallel to
● / ◐ / ○, the fill carrying evidence strength and the shape carrying derivation.

I searched for `▲ △ ◭ ◮` and for the word "triangle" across `governance/`, `schemas/`,
`scripts/`, `decisions/`, `references/`, `skills/`, `versions/`, `parts/`, `_archived/`, `site/`
and `index.html`. **Zero hits.** The two "triangle" matches are unrelated (a three-way document
disagreement).

So the correct statement is not "doctrine has no band for derived values". It is:

> **The derived-value marker is doctrine with no repository presence.** No glyph, no column, no
> validator, no renderer, no mention in `tier-system.md` §5, `mission-and-epistemics.md` §136,
> `project-standards.md`, or any DR. CLAUDE.md §10 records that the PI is not API-writable and
> legitimately lags, and that `userPreferences-v*.md` lives in claude.ai and not in the repo —
> so an absence here was never evidence of an absence in doctrine.

I made exactly the inference the research contract's R14 prohibits: *a zero-yield search is
evidence of absence only if the query was well-formed and the index was right.* My query was
well-formed; my index was wrong. §6.5's conclusion — that the guidebook's actual product has no
honest rendering path — **survives**, but its cause changes completely, and with it the fix. It
is not a doctrinal gap to be ruled on. It is a **ratified marker that has never been
implemented**, which is a Class C defect and needs no owner decision at all.

**C2 — §6.4 asserted two absences that are both false. WRONG on the evidence already in the DB.**

I wrote that "there is no access-need code for wheeled manoeuvring space at all" and that
"`access_needs` does not link to items". Both are refuted by a two-hop join I did not attempt:

```sql
access_needs → access_need_axis_map → axes → item_axis_links → items
```

It resolves, and it resolves for exactly the items in question:

| need | axis | item | strength |
|---|---|---|---|
| `A-SIZE` | `AX-WHM` | **E-08** | full |
| `A-SIZE` | `AX-WHM` | **E-12** | full |
| `A-REACH` | `AX-WHM` | E-08 / E-12 | full |
| `A-REACH` | `AX-AMB` | E-08 | partial |
| `A-STABLE` | `AX-BAL` | E-08 | weak |

And `access_need_axis_map` annotates `A-SIZE spans AX-WHM` with the single word **`envelope`**.
That *is* the wheeled-manoeuvring-space concept, named, keyed, and already attached to corridor
width. Both join tables are populated (21 and 158 rows).

I searched `sqlite_master` for tables carrying `need_code`, found three, and concluded no path to
items existed — without checking whether any of those three reached items *through another
table*. That is a one-hop search reported as a reachability result.

**C3 — "There is no arithmetic anywhere in this pipeline" is wrong, and it dismissed the
repo's actual value-determination protocol in a subordinate clause.**

The **Progressive Measurement Probe** (`workplan/progressive-measurement-protocol.md`,
`skills/progressive-measurement_SKILL.md`, `spec_value_probes`, `probe_population_links`,
`scripts/audit/pmp_audit.py`, `DR-2026-05-10`) is a real value-determination protocol: take V₀,
an accessibility direction D, and a claim type; walk the value toward the more accessible end;
re-centre after each supported step; halt when evidence stops validating. **Its output is "the
empirically-supported range, not a single point"**, and the gap between the stated value and the
empirical ceiling is the finding it exists to surface. It is enforced at Level 2 by an audit that
flags any item asserting a numerical spec without a walk.

More pointedly for this assessment: **PMP's own direction table already contains the owner's
parameter.**

| Spec type | Direction | Rationale |
|---|---|---|
| Turning radius / clear floor space | `up` | larger radius accommodates more devices |

So the project has already reasoned about turning space, already decided that more is more
accessible, and already built the protocol that would establish the empirical range. What it has
not done is run it (`spec_value_probes` = 0 rows) or connect it to `evidence_cell_state` (no
column, no join). **The correct finding is not "no arithmetic exists" but "the value-determination
protocol exists, is unrun, and is unwired to the determination it should produce."**

**C4 — The scorecard inflates six observations into twenty. OVERSTATED (presentational).**

The §6.6 table is 4 operations × 5 capabilities, nearly all "no". But "cannot render" and
"cannot invalidate" are *entailments* of "cannot represent", not independent findings. Twenty
cells implies twenty observations where there are roughly six. Same defect in "unrepresentable at
five levels" (§6.3): those five are one missing concept — derivation — with five surface
manifestations.

**C5 — I under-credited `root_type`. OVERSTATED.**

§6.1 said the model has no construct-validity dimension. `source_value_extractions.root_type`
∈ `measurement_primary` / `participatory_finding` / `committee_assertion` /
`derived_calculation` / `untraced` **is construct validity in embryo** — it distinguishes a
measurement from a committee's assertion from a calculation. The accurate claim is narrower and
still holds: **it exists at extraction level and never reaches the conditioning layer**, because
`schemas/directness.py` conditions on grain × scale and `assess_cell.py` never opens the
extractions table.

**C6 — The drive-wheel refinement was load-bearing in the prose and unverified in fact.**

I flagged the kinematics claim as unverified, then wrote "that gap is upstream of everything
below". The structural point — nothing anywhere records *the manoeuvre a claim concerns* —
does not depend on the kinematics and should not have been hung on it. Restated: the paradigm
question is a property of the claim, and the schema records it only as a property of the source.

**What survives Part 6 unchanged:** §6.2 in full (device class dies at the
`UNIQUE(item_code, population_code)` boundary; the Design Mode ladder has no equipment rung);
§6.3's core (no cell→cell dependency, no invalidation on upstream change); §6.1's core (the
conditioning layer has no construct axis); and the trial evidence that two paradigms both
anchored with every gate green.

### 7.2 The adjudication as the owner frames it

> *Wheelchair swept path versus turning radius requires an understanding of category, access
> needs, potential to harm, equipment as they relate to one another. If conflicts or
> contradictions exist, then adjudication is required.*

This is a better decomposition than mine. Mine treated paradigm and device class and stopped.
The owner's names four dimensions and a trigger. Assessed:

| dimension | where it lives | populated? | reaches a determination? |
|---|---|---|---|
| **Category** | `items.category` (A–K); E-04, E-08, E-12 all category E | yes, 93 items | **no** — category is a grouping label, never a comparison scope (§3.4) |
| **Access needs** | `access_needs` (17 codes, `design_obligation`, `family`, `absorbs`) → axes → items | yes; `A-SIZE`/`AX-WHM` annotated `envelope`, `full` strength on E-08 and E-12 | **no** — the join reaches the *item*, never the *cell*; no determination reads it |
| **Potential to harm** | `access_stakes` — `safety-critical` ("Harm if violated"), `exclusion` ("Locks people out"), `friction` ("Degrades the experience"); carried per-need by `access_needs.typical_stakes` | **16 of 17 NULL.** Only `A-TRIGGER` is graded. `A-SIZE` and `A-REACH` — the two that reach corridor width — are both **NULL** | **no** |
| **Equipment** | `source_value_extractions.device_class`, nine-value CHECK | vocabulary yes, rows 0 | **no** — dies at phase 7→9 (§6.2) |
| **Adjudication on conflict** | `conflicts` (`item_code`, `pop_a`, `pop_b`, `status`), `cross-population-conflict-mapper`, `references/conflict-matrices/` | table 0 rows; 13 markdown matrices unlinked to the DB | **no row shape fits** — see below |

**The harm dimension is the one that would decide this adjudication, and it is the emptiest.**

A corridor too narrow to turn around in is not a comfort defect. Under the repository's own
three-value vocabulary it is **`exclusion` — "Locks people out"** — and arguably
`safety-critical`, since a user who cannot reverse in a corridor cannot self-evacuate. That
grading is what converts the owner's parity premise from a preference into a threshold: an
`exclusion`-stakes parameter must be specified at the accommodating end of the empirical range,
not at its median or its code floor.

`access_stakes` exists precisely to carry that judgement. `access_needs.typical_stakes` is the
column that would attach it to `A-SIZE`. **It is NULL.** So the dimension that would decide the
adjudication is present in the schema, ratified in vocabulary, and unpopulated exactly where the
question is being asked.

**The adjudication row shape does not exist.** `conflicts` is keyed `(item_code, pop_a, pop_b)` —
it can express *two populations disagreeing about one item*. The owner's conflict is none of
those shapes:

- swept path vs turning radius is **paradigm vs paradigm** within one item;
- power chair vs manual chair is **equipment vs equipment** within one population;
- E-08's 1200 mm vs E-12's turning envelope is **item vs item**.

All three would have to be forced into `pop_a`/`pop_b`, which is a category error, or into
`connections.description` free text with an un-keyed target. The repository has exactly one
conflict shape and the question generates three the shape cannot hold.

**Note also the live contradiction this framing exposes**, already recorded in §3.4:
`references/conflict-matrices/CORRIDOR-W.md` was **RECLASSIFIED — NOT A CONFLICT DOMAIN** on
2026-03-30, on the reasoning that width and sensory load are independent variables. That
disposition is correct on the axis it examined (DEAF width vs NDV/AUT sensory load) and it
retired the domain entirely — *"Remove from conflict domain table"*. The conflict the owner is
now raising is a different one on the same parameter, and the retirement means there is no open
domain to file it against. A conflict domain closed on one axis was closed for all axes.

### 7.3 Corrected closure list

Replacing §6.7. Ordered by cost, and re-scoped by what §7.1 corrected.

1. **Implement the derived-value triangle.** No longer an owner ruling — it is ratified doctrine
   with zero implementation. Needs: the glyph and fill semantics written into
   `governance/tier-system.md` §5 beside ●/◐/○; a `synthesis_method` column on
   `evidence_cell_state` (`direct` / `inferred` / `consensus`, the vocabulary
   `governance/armature_v4_resolutions.md:23` already specifies, together with its
   `inference_basis` companion for non-direct); and a renderer that emits it. Free today at 0 rows.
2. **Populate `access_needs.typical_stakes`.** 17 rows, three-value vocabulary, already ratified.
   This is the dimension that decides accommodating-end specification, and it is 94% empty.
   `A-SIZE` and `A-REACH` first, since they carry corridor width.
3. **Run PMP on turning space.** The protocol exists, the direction is already decided (`up`), the
   audit exists, and `spec_value_probes` is empty. This is the closest existing mechanism to the
   owner's synthesis and it has never been exercised.
4. **A construct/manoeuvre field on the claim**, plus lifting `root_type` into the conditioning
   layer as a fourth directness dimension — `construct_directness(source_paradigm,
   claim_manoeuvre)` beside the existing three, with its table transcribed into
   `matrix_consistency.py` so the two cannot drift.
5. **A device-class dimension on determinations**, or an explicit doctrinal ruling that
   equipment stratification sits at Population Mode with a sub-key. The Design Mode ladder
   currently has no rung for it and that is a doctrine gap, not a schema one.
6. **A conflict shape that is not population×population** — minimally `conflict_kind ∈
   {population, paradigm, equipment, item}` with a target pair that is FK-keyed per kind.
   Reopening `CORRIDOR-W` needs this.
7. **`evidence_cell_state.derived_from_cell_id` + `derivation_rule`**, with `derivation_sha`
   extended to hash upstream cell ids so an upstream change reddens the downstream cell.
8. **Wire `access_needs` to cells, not only to items** — the `design_obligation` prose is the
   normative premise, and it currently stops one hop short of the determination it should
   license.
