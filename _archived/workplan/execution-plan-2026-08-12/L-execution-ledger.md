# Wave L — The execution ledger. **Before any wave executes, including Wave H.**

**Read `00-holistic-execution-plan.md` first.** **This wave has no precondition — it is the
precondition.**

**Owner requirement, 2026-08-11:** *an active logging of all work performed, complete with
specific notes about where any lines/values were changed, such that we have an active trail for
future work and auditing — and the logging must involve active interrogation of
interdependencies, tracing, orphaning, breaks, and deduplication/culling candidacy.*

**This is not a fifth register** (guardrail 3). It generalises `walk_harness.py`, whose verbatim
action log made the corridor-walk trial auditable, from one trial to every change. It discharges
W6.9 and W6.10 by making both mechanical rather than remembered.

**The governing rule: no change executes without a ledger entry, and the entry is written before
the change, not after.** An entry authored afterwards records what a session remembers; an entry
authored before records what it intended, and the delta between them is the finding.

---

## The design constraint no prior document resolved

**There is no `sessions` table in the database.** Re-derived: only `supersession_check` matches
`%session%`. Sessions are files under `sessions/`, and every `*_by_session` column is free text.
**So L3's "joins to `sessions`" is impossible as an FK** — it can only be a TEXT column validated
against `sessions/*.md` stems by a check.

### And a harder one: the write-path tension

CLAUDE.md §0 rule 4 says every DB write is a migration, and migrations are immutable once
committed. But a ledger entry is written **before** the change with `commit_sha` filled **after**.
**This needs an owner ruling before L1 lands.** Three options:

| | Mechanism | Cost | Guarantee |
|---|---|---|---|
| **(i)** *recommended* | **Two-migration pattern** — an intent migration INSERTs the entry with `commit_sha` NULL; a completion migration UPDATEs `commit_sha`/`executed_at`/`breaks` | 2 migrations per change; the emitter prints `UPDATE — check WHERE clause` warnings (non-blocking) | **Full.** Consistent with `--rebuild` and with the blocking reproducibility gate; no DR needed |
| (ii) | **Exempt table** — write directly, add `work_log` to `EXEMPT_TABLES` (`migration_reproducibility.py:63`) | cheap per entry | **Weaker**, and needs a DR per CLAUDE.md §4. Note W9.1's live lesson: `url_verification_runs` is already written outside migrations *without* exemption, and that apparatus is under an open ruling |
| (iii) | **YAML fallback** `workplan/work-log/WL-<session>.yaml` | cheapest | **Worst** — recreates the dual-store class Wave 7 spends itself removing. Recorded only so the choice is explicit |

**Recommend (i).** If it proves so heavy that sessions skip the ledger, the mechanism has failed
its own purpose — surface that early rather than letting it decay.

---

## L1 — The record shape and the `work_log` migration

**Schema state:** `user_version = 53`; latest is `053_locator_hierarchy.sql`. **This is
`054_work_log.sql`** — but note Wave 3 also proposes 054 for `locator_schemes`. **Whichever lands
first takes 054;** re-derive the free number at execution.

```sql
PRAGMA user_version = 54;
CREATE TABLE work_log (
    entry_id            TEXT PRIMARY KEY
                        CHECK (entry_id GLOB 'WL-[0-9][0-9][0-9][0-9]'),
    plan_item           TEXT NOT NULL,           -- wave item id; NEVER null (L1)
    session             TEXT NOT NULL,           -- sessions/<session>.md stem; no FK possible
    commit_sha          TEXT,                    -- filled after execution; forward-only
    intent_written_at   TEXT NOT NULL,           -- ISO 8601, BEFORE the change
    executed_at         TEXT,                    -- after; the gap is itself a signal
    migration_id        TEXT,                    -- joins data_migrations.migration_id; NOT an FK —
                                                 -- the row can be written BY that migration,
                                                 -- before its own ledger row exists
    changes             TEXT NOT NULL CHECK (json_valid(changes)),          -- block 2 LOCUS
    interdependency     TEXT NOT NULL CHECK (json_valid(interdependency)),  -- block 3
    tracing             TEXT NOT NULL CHECK (json_valid(tracing)),          -- block 4
    orphaning           TEXT NOT NULL CHECK (json_valid(orphaning)),        -- block 5a
    breaks              TEXT NOT NULL CHECK (json_valid(breaks)),           -- block 5b
    culling             TEXT NOT NULL CHECK (json_valid(culling)),          -- block 6
    supersedes          TEXT REFERENCES work_log(entry_id),
    loss_audit          TEXT,
    CHECK (supersedes IS NULL OR loss_audit IS NOT NULL),   -- W6.9 made mechanical
    CHECK (json_array_length(json_extract(interdependency,
           '$.unswept_and_unexplained')) = 0)               -- L1: MUST be empty
);
```

**The JSON-column convention has house precedent** — `weighting_profile.tier_weights` uses
`CHECK (json_valid(...))`.

**Block shapes** are exactly the plan's L1 YAML (`2026-08-12-resolution-plan.md:216-275`), with
`changes[].line` mandatory for file paths and `mechanism ∈ {data_migration, schema_migration,
direct_edit, registry_entry, regeneration, owner_decision}`. **SQLite cannot cheaply CHECK inside
JSON arrays** — put the enum in `schemas/work_log.py` (new; confirmed absent) and in
`test_db_integrity`.

**Two CHECKs are doing real work:** `supersedes` without `loss_audit` is rejected — that is W6.9
enforced by the database — and `unswept_and_unexplained` must be an empty array for the row to
exist at all.

---

## L2 — The five standing interrogations

**No separate artefact.** I1–I5 are the six JSON blocks' semantics. Encode the plan's table
(`:277-288`) verbatim into `schemas/work_log.py` docstrings and the `WORK-LOG.md` header **so the
questions travel with the record.**

| # | Interrogation | Answered wrong when |
|---|---|---|
| **I1** | **Interdependency.** What reads this, what writes it, and did the sweep *enumerate* or merely *count*? | A count is recorded and the members are not. A count cannot discharge CLAUDE.md §0 rule 5 |
| **I2** | **Tracing.** Can the affected value still be walked back to source, population and doctrine? | The walkback is asserted rather than run |
| **I3** | **Orphaning.** What now points at nothing? | Orphans are counted on the surface that changed, not on the surfaces that cited it |
| **I4** | **Breaks.** Which checks changed verdict — and, separately, which changed **subject count**? | Only verdicts are recorded. *A gate reporting zero may have examined zero* |
| **I5** | **Dedup / culling.** What did this make redundant, and did it re-implement something extant? | A new tool is written beside an existing one. The repository has paid twice |

---

## L3 — Where the ledger lives

- **Canonical store: the `work_log` table** (CLAUDE.md §2 — the DB is authoritative).
- **Generated, not transcribed, wherever the fact already exists.** `commit_sha`, `migration_id`,
  `executed_at` and `changes[].path` come from git and `data_migrations`; **only the four
  interrogation blocks are hand-authored.** A ledger that asks a session to retype what git
  already knows will be filled in wrongly and then trusted.
- **A generated `workplan/WORK-LOG.md`** via a new `scripts/generate/work_log_md.py`, on the
  `context_map.py` pattern — reverse-chronological, one row per entry, linking plan item →
  commit → migration → checks moved. **The table is what a query reads; the markdown is what a
  session reads.**
- **Forward-only.** An entry is never rewritten. A correction is a **new** entry with
  `supersedes:` and a `loss_audit:` block.

### The two registry entries

Conventions re-derived: a newly-wired check starts `advisory`; every check declares `basis:`;
`min_items:` is the vacuity floor.

```yaml
  - id: work_log_complete
    cmd: [python3, scripts/audit/work_log_complete.py]
    battery: data            # stdlib only — deliberately NOT `governance` (deps: [pydantic]),
                             # and see the :174 battery-line defect before trusting battery parsing
    kinds: [data, schema, tooling, governance]
    level: advisory
    basis: unattributed      # ratify via the Wave-L DR, then claim it
    cost: fast
    min_items: 1
    note: >-
      Every commit touching data/, scripts/, governance/ or schemas/ since the
      ledger epoch has a work_log entry whose plan_item resolves to a wave item
      and whose interdependency.unswept_and_unexplained is empty. LIMIT (L5):
      this proves entries exist and are structurally complete; whether an empty
      unswept list is TRUE or merely ASSERTED is not mechanically checkable.
      Prints EXAMINED: <n commits>.

  - id: work_log_fresh
    cmd: [python3, scripts/generate/work_log_md.py, --check]
    battery: render
    kinds: [data, schema, tooling, governance]
    level: advisory
    basis: render/render-freshness
    cost: fast
    min_items: 1
    note: >-
      workplan/WORK-LOG.md matches the work_log table, on the context_map_fresh
      pattern.
```

---

## L4 — Retrofit, bounded

**Do not backfill the repository's history.** The epoch is the first Wave-L commit. Three bodies
of work already carry ledger-shaped evidence and should be imported so the trail starts
non-empty rather than pristine-and-useless:

1. **The corridor-walk log** — `workplan/2026-08-12-pipeline-walk-trial-log.md` (3,875 lines;
   harness `scripts/tests/walk_harness.py`, 272 lines), action format
   `### [NNN] Stage X.Y — … <timestamp>`. Import with `plan_item: W6.1`.
   **Anomaly found: action `[006]` appears twice** (`:139` and `:149`). **So "105 actions" must be
   re-counted at import**, and the importer must handle duplicate ids — map to `WL-` ids 1:1 with
   a `source_action` field. The log's banner (`:1-12`) marks it NOT CONTENT — **carry that marker
   into the entries.**
2. **The W5.1 corrections, when they land** — the single best worked example of all five
   interrogations firing at once (I1: the shadow YAMLs; I2: value-vs-text walkback; I3: none;
   I4: the detector's WARN clearing *and* its EXAMINED count moving; I5: the YAMLs become
   redundant).
3. **Wave H itself** — the H3 four-class classification is the reference entry for I2.

---

## L5 — What the ledger is not

- **Not a substitute for attestations.** Attestations bind an *artifact* to doctrine; the ledger
  binds a *change* to its consequences. Synthesis-path commits still owe both.
- **Not a place for volatile totals.** Per R-17, `EXAMINED` counts and per-check verdicts are
  recorded **with the diff they were measured against**; suite totals are never recorded at all.
  **The `WORK-LOG.md` generator must never print suite totals.**
- **Not a gate on its own honesty.** `work_log_complete` can only check that entries exist and
  are structurally complete. **State that limit in the check's registry `note:`** — it is written
  into the entry above.

**Commit hygiene:** Wave-L commits touch `scripts/`, `schemas/`, `governance/check-registry.yaml`
and `workplan/` — **none is a synthesis path**, so no doctrine token is owed. **Unless** the
ratifying DR ships in the same commit: put the DR in `decisions/` in its **own** commit with
token and attestation.

---

## Ordered steps

1. **Owner ruling on the write path** — option (i), (ii) or (iii).
2. Emit `054_work_log.sql` (re-derive the free number) and `schemas/work_log.py`; run
   `migrate_db.py`, then `--rebuild` to confirm reproducibility.
3. Write `scripts/audit/work_log_complete.py` and `scripts/generate/work_log_md.py`.
   **Per W6.7, search first:** `grep -rn "work_log\|ledger" governance/check-registry.yaml
   scripts/` → **confirmed none exists at HEAD.** Record that search in WL-0001's
   `detector_search_command`.
4. Register both checks. `python3 scripts/run_checks.py --selftest` must stay green (C1b).
5. **The first entry is WL-0001, describing Wave L itself.**

## Verification
`PRAGMA user_version` → 54 · `run_checks.py --list` shows both checks active and advisory ·
`--selftest` green · `work_log_md.py --check` green after first generation.

## Falsifier
If the owner prefers no table, the YAML fallback replaces the DDL — recorded so the choice is
explicit rather than drifted into.

---

## Re-derivation notes

| Claim | Status |
|---|---|
| The ledger "joins to `sessions`" | **REVISED — no `sessions` table exists**; TEXT + check, not FK |
| `data_migrations` shape | **CONFIRMED** — `migration_id` PK, `applied_at`, `content_sha`, `applied_by_session`, `notes` |
| No existing ledger mechanism | **CONFIRMED** — zero hits at HEAD |
| The walk log is 105 actions | **REVISED** — action `[006]` is duplicated at `:139` and `:149`; re-count at import |
| JSON-column CHECK convention | **CONFIRMED** — `weighting_profile.tier_weights` precedent |
| The write-path tension | **NEW** — unresolved by the plan; three options above, ruling needed before L1 |
