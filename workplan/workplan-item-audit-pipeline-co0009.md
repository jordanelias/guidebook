# CO-0009 — Item Audit Pipeline
**Created:** 2026-05-05 19:04 UTC
**Revised:** 2026-05-05 19:45 UTC (v2 — post-review corrections)
**Model:** Sonnet 4.6 (audit) / Opus required for Phase 0 decisions and FDA skill design
**Status:** PROPOSED — requires decision record authoring before implementation
**Authority:** Audit session 2026-05-05 — full skill and DB audit against current repository
**Slots into:** C1 (schema), C2 (skills), C3 (per-item pre-pass)
**Supersedes:** Nothing. Extends CO-0008.

---

## 0. Two-Database Architecture (Reference)

The project has two SQLite databases with distinct roles:

| Database | Path | Role |
|---|---|---|
| Tracking DB | `data/guidebook.db` | Project state: gaps, connections, sessions, evidence sources, audit runs |
| Website DB | `data/db/guidebook.db` | Content: specifications, populations, conflict domains, rooms, economics |

All tables proposed in this workplan are in the **tracking DB** (`data/guidebook.db`) unless
explicitly noted otherwise. The website DB already has a `conflict` table (15 domain-level
records with IDs like `LIGHT-INT`, `ACOUSTIC-LVL`) from the C0 migration. The `conflicts`
table proposed here is different in purpose: it records per-item audit findings from
conflict-mapper. No namespace collision: website DB uses domain-code IDs; tracking DB uses
`CONF-NNNN` sequential IDs.

---

## 1. Problem Statement

The current project has no systematic per-item quality pipeline. Items are written (ISW) and
research is conducted (FDR, multilingual-research), but there is no structured mechanism to:

- Surface undocumented cross-item relationships before authoring
- Map population conflicts before writing specs that must resolve them
- Confirm that functional deficit scoping is correct before research is commissioned
- Assess economic framing at item level
- Route findings to the correct research skill with an auditable handoff

Without this, C3 (103 items) risks authoring atoms on incomplete or incorrectly scoped items,
generating rework later. The pipeline is a quality gate that runs per item before C3 atoms
are written.

---

## 2. Pipeline Architecture

```
WRAPPER: item-audit-pipeline
INPUT: item_code, session, skip_steps=[]

STEP 1  connection-discovery --mode spec      [Sonnet]
STEP 2  connection-discovery --mode evidence  [Sonnet] (skip if no BPC slug)
STEP 3  cross-population-conflict-mapper      [Sonnet/Opus]
STEP 4  content-gap-analyzer                 [Sonnet/Opus]
STEP 5  evidence-auditor                     [Sonnet/Opus]
STEP 6  functional-deficit-auditor           [Sonnet/Opus] ← NEW
STEP 7  economics-auditor                    [Sonnet]      ← NEW

CROSS-CUTTING: citation-miner inline (depth-1, relevance-gated) throughout steps 1–7

STEP 8  audit-consolidator                   [Sonnet]      ← NEW
        └── produces: research brief → references/audit-briefs/{item_code}_brief.md
            + updates item_audit_runs status=COMPLETE
```

Each step can be called individually. The wrapper orchestrates the sequence, tracks state
in `item_audit_runs`, and handles session boundaries.

**skip_steps semantics:** `skip_steps` accepts step numbers whose outputs are already in the
tracking DB from a prior run. "Skip" means "do not re-run; consolidator reads prior output
from SQLite." It does NOT mean "omit entirely." Skipping a step that has never been run for
this item causes the consolidator to produce an incomplete brief — the wrapper must warn and
abort rather than silently proceed.

**force_rerun semantics:** `force_rerun` accepts step numbers to re-run even if previously
complete. Use case: prior run used Sonnet, current run wants Opus output. Wrapper deletes
prior step outputs from SQLite (gaps with matching session+skill source, connections
similarly) before re-running. Mutually exclusive with `skip_steps` for the same step number.

**Conflict-mapper multi-run protocol:** Conflict-mapper has a ceiling of 3 domains per run.
For items with >3 active domains, the wrapper invokes conflict-mapper iteratively. Each run
logs its CONF-NNNN records to the tracking DB `conflicts` table. Before each subsequent run,
the wrapper reads existing conflicts for the item and passes already-resolved domains as
context. The consolidator aggregates all runs by querying `conflicts WHERE item_code = ?`.

---

## 3. Skills Inventory

### 3.1 Skills requiring modification

| Skill | Change | Severity |
|---|---|---|
| connection-discovery | Merge connection-scout; add --mode flag; add non-connection exit routing; add external mode; add SPECULATIVE→gap rule | MAJOR |
| cross-population-conflict-mapper | Write to tracking DB conflicts table (not archived MD files); update Feeds FROM reference | MODERATE |
| content-gap-analyzer | Add session-groupable output summary line | MINOR |
| evidence-auditor | Add SQLite write: EG for OVERCLAIMED/UNCERTAIN_REVIEW; AUDT for UNDISCLOSED-CONSENSUS/MARKER-STRATUM-MISMATCH | MODERATE |

### 3.2 Skills to create

| Skill | Model | Complexity |
|---|---|---|
| functional-deficit-auditor | Sonnet/Opus | HIGH — imports FDR ICF taxonomy; Opus for mechanism judgment |
| economics-auditor | Sonnet | MODERATE — checklist application; no Opus |
| audit-consolidator | Sonnet | MODERATE — pure collation from SQLite |
| item-audit-pipeline | Sonnet (wrapper) | HIGH — session boundary handling; state machine |

### 3.3 Skills to retire

| Skill | Disposition |
|---|---|
| connection-scout | Merged into connection-discovery; file moved to skills/deprecated/ |

---

## 4. Schema Requirements (Tracking DB only)

### 4.1 Decision records required before any schema work (A12 compliance)

IDs continue from D-0140 (current latest).

| Decision ID | A12 Category | Delegation | Summary |
|---|---|---|---|
| D-0141 | D-SCHEMA | DG-REVIEW | items table: migrate schemas/item.py to tracking DB |
| D-0142 | D-SCHEMA | DG-REVIEW | item_audit_runs table: pipeline state tracking per item |
| D-0143 | D-SCHEMA | DG-REVIEW | conflicts table (tracking DB): per-item audit findings |
| D-0144 | D-SCHEMA | DG-REVIEW | Gap categories CONF + AUDT: extend gaps CHECK constraint |
| D-0145 | D-SCHEMA | DG-REVIEW | citation_mining.deferred_reason column |
| D-0146 | D-OP | DG-REVIEW | Merge connection-scout → connection-discovery: deprecate scout |
| D-0147 | D-METH | DG-NON | functional-deficit-auditor: scope, ICF alignment, FDR trigger criteria |
| D-0148 | D-METH | DG-NON | economics-auditor: scope, boundary with economics-researcher |
| D-0149 | D-OP | DG-REVIEW | audit-consolidator: output contract, GitHub brief path convention |
| D-0150 | D-OP | DG-REVIEW | item-audit-pipeline: wrapper architecture, session boundary handling |

D-0141–D-0145: DG-REVIEW (D-SCHEMA default).
D-0146, D-0149, D-0150: DG-REVIEW with rationale — first-of-kind operations (default DG-AUTO upgraded).
D-0147, D-0148: DG-NON — new methodology (default for D-METH new methodology applies).

### 4.2 Migration 004 schema

#### items (tracking DB)

Pre-existing bug: `schemas/item.py` validator uses `^[A-K]-\d{2}$` — rejects `A-10b` and
any letter-suffix item codes. Fix regex to `^[A-K]-\d{2}[a-z]?$` in this migration before
populating. Do not use the existing Pydantic model unmodified.

```sql
CREATE TABLE items (
  item_code           TEXT PRIMARY KEY,          -- e.g. I-01, A-10b
  item_id             TEXT UNIQUE,               -- ITEM-NNNN formal ID (if assigned)
  category            TEXT NOT NULL,             -- A-K single letter
  name                TEXT NOT NULL,
  applicable_groups   TEXT,                      -- CSV: UPL,MOB,DEM
  bpc_source_slug     TEXT REFERENCES slugs(slug),
  status              TEXT DEFAULT 'draft'
                      CHECK(status IN ('draft','active','merged','retired')),
  created_at          TEXT NOT NULL,
  created_by_session  TEXT NOT NULL,
  updated_at          TEXT NOT NULL,
  updated_by_session  TEXT NOT NULL
);
CREATE INDEX idx_items_category ON items(category);
CREATE INDEX idx_items_slug ON items(bpc_source_slug);
```

`category_name` omitted — derivable from category letter; storing it creates drift risk.

#### item_audit_runs (tracking DB)

```sql
CREATE TABLE item_audit_runs (
  run_id              TEXT PRIMARY KEY,          -- {item_code}_{session_filename}
  item_code           TEXT NOT NULL REFERENCES items(item_code),
  session             TEXT NOT NULL,
  steps_complete      TEXT NOT NULL DEFAULT '[]', -- JSON array of completed step names
  steps_started       TEXT NOT NULL DEFAULT '[]', -- JSON array of started-not-complete
  status              TEXT NOT NULL DEFAULT 'IN-PROGRESS'
                      CHECK(status IN ('IN-PROGRESS','COMPLETE','HANDED-OFF')),
  spec_hash           TEXT,                      -- MD5 of item spec text at run start
  brief_path          TEXT,                      -- references/audit-briefs/{item_code}_brief.md
  created_at          TEXT NOT NULL,
  created_by_session  TEXT NOT NULL,
  updated_at          TEXT NOT NULL,
  updated_by_session  TEXT NOT NULL
);
CREATE INDEX idx_audit_runs_item ON item_audit_runs(item_code);
CREATE INDEX idx_audit_runs_status ON item_audit_runs(status);
```

`run_id` = `{item_code}_{session_filename}` — unique per item per session; no same-day
collision because session filenames are unique.

`steps_started`: written before each step begins. A step in `steps_started` but not
`steps_complete` signals mid-step failure. Wrapper re-runs that step; each step is idempotent
via INSERT OR IGNORE or dedup checks at the DB level.

`spec_hash`: MD5 of item spec text at run start. On resume, wrapper recomputes and compares.
Mismatch → warn user; prompt restart or continue with stale-state flag in brief.

#### conflicts (tracking DB)

```sql
CREATE TABLE conflicts (
  conflict_id         TEXT PRIMARY KEY,          -- CONF-NNNN sequential (tracking DB only)
  item_code           TEXT REFERENCES items(item_code),
  domain              TEXT NOT NULL,             -- same taxonomy codes as website DB
  pop_a               TEXT NOT NULL,
  pop_b               TEXT NOT NULL,
  status              TEXT NOT NULL
                      CHECK(status IN (
                        'RESOLVED-EVIDENCE','RESOLVED-CONSENSUS',
                        'RESOLUTION-PROPOSED','UNRESOLVED','MODE-S-ONLY'
                      )),
  resolution          TEXT,
  evidence            TEXT,
  gap_id              TEXT,                      -- populated after gap created; no FK constraint
  source_skill        TEXT NOT NULL DEFAULT 'cross-population-conflict-mapper',
  created_at          TEXT NOT NULL,
  created_by_session  TEXT NOT NULL,
  updated_at          TEXT NOT NULL,
  updated_by_session  TEXT NOT NULL
);
CREATE UNIQUE INDEX idx_conflicts_dedup
  ON conflicts(item_code, domain, pop_a, pop_b);  -- idempotency on re-run
CREATE INDEX idx_conflicts_status ON conflicts(status);
```

`gap_id` FK constraint intentionally omitted. For UNRESOLVED conflicts: insert gap first,
then insert conflict with gap_id populated — both in the same transaction.

**Pop pair ordering (symmetric dedup):** The dedup index treats `(UPL, MOB)` and `(MOB, UPL)`
as different conflicts. Wrapper must alphabetically order populations before insert
(pop_a < pop_b lexicographically). This is a Phase 1 implementation detail enforced by
the `add-conflict` CLI command, not a CHECK constraint (CHECK on `pop_a < pop_b` would
prevent insertion of any unordered pair).

Domain codes use the same values as the website DB conflict table (`LIGHT-INT`, `ACOUSTIC-LVL`,
etc.) for cross-reference consistency. Cross-DB FK not possible in SQLite — alignment is
by convention, not constraint.

#### Gap category expansion
Follows migration 002 recreation pattern. New categories: `CONF`, `AUDT`.
Full CHECK after expansion:
`'RP','SW','CR','ST','MX','CD','EC','EG','CI','DEC','CONF','AUDT'`

#### citation_mining column
```sql
ALTER TABLE citation_mining ADD COLUMN deferred_reason TEXT;
```

### 4.3 db.py CLI extensions required

| Command | Purpose |
|---|---|
| `add-conflict` | Insert conflict record; returns CONF-NNNN |
| `update-conflict` | Update status, resolution, gap_id |
| `conflicts` | Query (--item, --domain, --status, --summary) |
| `next-id conflicts` | Sequential CONF-NNNN |
| `add-audit-run` | Create item_audit_runs row |
| `update-audit-run` | Update steps_started, steps_complete, status, brief_path |
| `audit-runs` | Query (--item, --status) |
| `add-item` | Insert item row |
| `items` | Query items |
| `delete-connection` | Hard-delete by CON-ID (needed for data corrections) |

### 4.4 What writes where

| Pipeline step | Table(s) written | Gap category | ID format |
|---|---|---|---|
| connection-discovery (connection) | connections + connection_targets | — | CON-NNNN |
| connection-discovery (non-connection) | gaps | CR or SW | GAP-NNN |
| cross-population-conflict-mapper (any) | conflicts | — | CONF-NNNN |
| cross-population-conflict-mapper (UNRESOLVED) | gaps + conflict.gap_id | CONF | GAP-NNN |
| content-gap-analyzer | gaps | MX, RP, ST, CD | GAP-NNN |
| evidence-auditor (OVERCLAIMED, UNCERTAIN_REVIEW) | gaps | EG | GAP-NNN |
| evidence-auditor (UNDISCLOSED-CONSENSUS, MARKER-STRATUM-MISMATCH, UNSUPPORTED-MARKER, UNSTATED) | gaps | AUDT | GAP-NNN |
| evidence-auditor (CONFIRMED_STRATUM, UNDERCLAIMED) | brief only — not logged | — | — |
| functional-deficit-auditor (FDR trigger YES) | gaps | RP | GAP-NNN |
| functional-deficit-auditor (scope error) | gaps | AUDT | GAP-NNN |
| economics-auditor (missing content) | gaps | EC | GAP-NNN |
| economics-auditor (framing violation) | gaps | AUDT | GAP-NNN |
| citation-miner (relevant to current item) | citation_mining (mined) | — | slug+ref |
| citation-miner (not relevant) | citation_mining (deferred_reason set) | — | slug+ref |
| audit-consolidator | item_audit_runs (COMPLETE) + GitHub brief | — | run_id |

### 4.5 Items table population

Phase 1 must include a migration script to populate the items table from `versions/current/`.

Script: `scripts/migrate/migrate_items.py`
Source: grep `### [A-K]-\d{2}[a-z]? ` headings from spec file
Extract: item_code, name (heading text after code), applicable_groups (from **Applicable
Groups:** field), bpc_source_slug (from **Cross-reference:** slug if present)
Expected output: ~103 rows
Merged/retired items: identify from active change orders; set status accordingly

### 4.6 CI validators for new tables

Per CO-0008 rule: every new schema object gets a CI validator. Phase 1 Session 1b must
include:
- `scripts/validate_items.py` — validates items table (item_code format, status values)
- `scripts/validate_conflicts.py` — validates conflicts table (domain codes, status values)
- `scripts/validate_audit_runs.py` — validates run_id format, JSON arrays in steps fields
CI must pass before Phase 2 begins.

---

## 5. Data Management Principles

These govern the pipeline and any future extensions. They are normative.

### 5.1 SQLite is the single source of truth for actionable items
All findings that require action must be in the tracking DB before the session closes.
Prose in session files or GitHub markdown is secondary. A finding that exists only in
markdown is not tracked and will be lost.

### 5.2 Session is the primary run identifier
`created_by_session` is the primary grouping key. `run_id = {item_code}_{session}` anchors
the session to the item. Consolidator queries by session. No separate run_id namespace.

### 5.3 Gap categories map to resolving skills
The gap category is a routing code — wrong category = wrong routing = gap sits open.

| Category | Closed by |
|---|---|
| RP | multilingual-research / FDR / literature-review-planner |
| SW | item-specification-writer |
| CR | connection-discovery / ISW cross-reference |
| ST | structure-auditor / toc-editor |
| MX | content-gap-analyzer → multilingual-research |
| EC | economics-researcher |
| CD | ISW content development |
| EG | evidence-auditor → FDR |
| CONF | cross-population-conflict-mapper (resolution evidence run) |
| AUDT | item-specification-writer (scope or authoring correction) |
| CI | technical |
| DEC | workplan-orchestrator |

### 5.4 Conflicts are a separate entity from gaps (tracking DB)
A `conflicts` record is not a gap. RESOLVED conflicts need no gap. UNRESOLVED conflicts
generate a gap (CONF) linked via `conflict.gap_id`. The conflicts table carries
domain/population/resolution detail that the gaps table cannot hold.

The tracking DB `conflicts` table is distinct from the website DB `conflict` table.
Former: per-item pipeline audit findings. Latter: canonical domain-level resolution content.
Same domain taxonomy codes used in both for cross-reference consistency.

### 5.5 Citation-miner depth-1 is a data integrity rule
Mining discovered sources in the same session creates unauditable provenance chains.
Depth-1 enforced at wrapper level. `deferred_reason` makes deferrals auditable.

### 5.6 Evidence-auditor flag routing is a hard rule
CONFIRMED_STRATUM and UNDERCLAIMED: brief only, not logged to DB.
OVERCLAIMED and UNCERTAIN_REVIEW: → EG gap (evidence sufficiency issue).
UNDISCLOSED-CONSENSUS, MARKER-STRATUM-MISMATCH, UNSUPPORTED-MARKER, UNSTATED: → AUDT gap
(authoring correction needed — disclosure missing, marker wrong, stratum unstated).
Not subject to per-finding judgment.

### 5.7 The items table is the pipeline anchor
Every audit run FKs to an item_code. Enforces traceability and queryable audit history.

### 5.8 Economics-auditor never triggers economics-researcher inline
Auditor flags EC gaps. Researcher runs in a separate session against those gaps.

### 5.9 source_skill is a controlled vocabulary
Add to project-standards.md as a RULE. Controlled values for the pipeline:
`connection-discovery` · `cross-population-conflict-mapper` · `content-gap-analyzer` ·
`evidence-auditor` · `functional-deficit-auditor` · `economics-auditor` ·
`audit-consolidator` · `item-audit-pipeline` · `citation-miner`

### 5.10 New pipeline skills must declare an output contract in SKILL.md §Outputs
Required fields: tables written (tracking vs website DB), gap categories used,
source_skill value, citation-miner relevance filter, idempotency mechanism.

### 5.11 Gap deduplication: consolidator checks before logging
Gap IDs remain sequential (GAP-NNN). Consolidator checks for near-duplicates
(same item_code + category + overlapping description text) before creating a new gap.
On ambiguous match: surface to user for confirmation — do not auto-resolve.

### 5.12 The two-database boundary is permanent
Tracking DB content is project-operational. Website DB content is publication-facing.
Never migrate between them as a shortcut. If a tracking DB finding matures into website
content, that is a deliberate editorial act, not an automatic pipeline step.

---

## 6. Build Order and Session Estimates

### Phase 0 — Decision records · 2 sessions · Opus

Author D-0141 through D-0150. Batch 5 per session.
Verify delegation category for each against decision-protocol.md before authoring.
D-SCHEMA decisions: DG-REVIEW. D-OP/D-METH decisions: check delegation table.

**Done criterion:** All 10 decisions in decisions table, status ACTIVE.

### Phase 1 — Schema (migration 004) · 3 sessions · Sonnet

**Session 1a — Tables and DDL:**
- Write migration 004 SQL: items + item_audit_runs + conflicts tables
- Fix `schemas/item.py` validator regex to accept letter-suffix codes (A-10b)
- Run migration against tracking DB; verify schema_version increments
- CI must pass before 1b

**Session 1b — db.py CLI + validators:**
- Implement all 10 new db.py commands (§4.3)
- Write CI validators: validate_items.py, validate_conflicts.py, validate_audit_runs.py
- Unit test: add-conflict, add-audit-run, add-item, delete-connection
- CI must pass before 1c

**Session 1c — Items population + gap category expansion:**
- Write and run `scripts/migrate/migrate_items.py` (~103 items)
- Flag merged/retired items per active change orders
- Gap category expansion (migration recreation, follows 002 pattern): CONF + AUDT
- Update `schemas/gap.py` validator to include CONF and AUDT
- Commit tracking DB to GitHub
- CI must pass before Phase 2

**Done criterion:** schema_version = 4; ~103 items in items table; all db.py commands
functional; gap.py accepts CONF and AUDT; all CI validators pass.

**schema_version increment protocol (L-03):** Sessions 1a, 1b, and 1c constitute
migration 004 as three sub-files: 004a_tables.sql (items + item_audit_runs + conflicts),
004b_db_extensions.sql (db.py CI validators), 004c_gap_categories.sql (gap category
expansion + Pydantic updates). Only 004c executes `UPDATE db_meta SET value='4'` — at
the very end of Session 1c after CI passes. Sessions 1a and 1b do not touch db_meta.

### Phase 2 — Skill modifications · 2 sessions · Sonnet

**Session 1 — connection-discovery merge:**
- Merge connection-scout → connection-discovery
  - Add `--mode [spec|evidence|external]` flag
  - Add non-connection exit routing (gap CR or SW, not connection)
  - Absorb external mode (forward citations via Scholar Gateway/PubMed)
  - Absorb SPECULATIVE→gap rule from connection-scout §5 rule 3
- Move skills/connection-scout_SKILL.md → skills/deprecated/
- Test: run connection-discovery --mode spec and --mode evidence on I-01

**Session 2 — remaining skill updates:**
- Fix conflict-mapper: write to tracking DB conflicts table; remove archived MD references;
  update Feeds FROM to reference connection-discovery
- Update evidence-auditor: SQLite write per §4.4 flag routing (EG vs AUDT split)
- Update content-gap-analyzer: add session-groupable output summary line
- Test: conflict-mapper on 2-population item; evidence-auditor on A-01;
  content-gap-analyzer on B-01

**Done criterion:** All four modified skills produce correct tracking DB output. No
references to archived MD files remain in any skill file.

### Phase 3 — New skills: FDA + economics-auditor · 3–4 sessions

**Session 1 — FDA design (Opus session required):**
Design `skills/functional-deficit-auditor_SKILL.md`:
- Import ICF Tier A/B/C taxonomy from FDR SKILL.md
- Define 6-question audit checklist:
  1. Do listed Applicable Groups match ICF codes implied by the spec?
  2. Are any affected populations absent?
  3. Is claimed mechanism of action (e.g., Biomechanical FOR) correct and sufficient?
  4. Are threshold values tied to a specific population's functional limit?
  5. Is there a population for whom the item is inapplicable (over-inclusion)?
  6. FDR trigger: does evidence basis contain [THIN], "zero indexed studies," or rely solely
     on clinical reasoning for a threshold value?
- ICF codes outside FDR Tier A/B/C scope: flag as out-of-FDA-scope; note for manual OT review
- FDR trigger output: YES/NO + ICF scenario string (`d-code + population + environment`)

**Session 2 — FDA implementation + test:**
- Implement FDA against SKILL.md
- Test on I-01: expect AUDT gap for misplaced SCI thermal content

**Session 3 — economics-auditor design + implementation + test:**
- Write `skills/economics-auditor_SKILL.md` (6-item checklist):
  1. Retrofit cost note: present? evidenced or asserted?
  2. Capital cost indicator: flagged if cost-significant?
  3. Lifecycle framing: present where capital cost non-trivial?
  4. Economics volume linkage: cross-reference present?
  5. Cost-of-not-doing: documented consequence of omission?
  6. Framing compliance: no compliance-burden language, no single-source figures,
     jurisdiction-labelled data?
- Implement; test on I-01: expect EC gap for asserted-not-evidenced retrofit cost note

**Optional session 4:** Refinement if test runs reveal scope issues.

**Done criterion:** Both skills produce correct tracking DB output on I-01.

### Phase 4 — audit-consolidator + wrapper + cleanup · 3 sessions · Sonnet

**Session 1 — audit-consolidator:**
- Write `skills/audit-consolidator_SKILL.md`
- Implement; output to `references/audit-briefs/{item_code}_brief.md`
- Brief format: research actions table (skill + gap_id + priority + description),
  deferred citations table (slug + deferred_reason), new CON-IDs, GAP-IDs, CONF-IDs

**Session 2 — wrapper:**
- Write `skills/item-audit-pipeline_SKILL.md`
- Implement with: skip_steps semantics (skip-if-already-complete), conflict-mapper
  multi-run protocol (§2), steps_started/steps_complete state management,
  spec_hash staleness check, HANDED-OFF status on context pressure

**Session 3 — full pipeline test + CON-0251 cleanup:**
- Run full pipeline on I-01 (all 8 steps)
- Verify: item_audit_runs COMPLETE, brief at correct path, all expected findings in DB
- CON-0251 cleanup (requires delete-connection CLI from Phase 1):
  - `db.py delete-connection --con-id CON-0251`
  - `db.py add-gap --category RP --priority P2 --skill functional-deficit-auditor`
    `--section I-01`
    `--description "UPL+DEM compound: no indexed evidence for cognitive-physical compound`
    `hardware selection. FDR trigger: d440 + UPL+DEM compound → hardware operability"`
  Note: RP is the correct category — "no indexed evidence" is a research gap, not an
  authoring error. AUDT would be wrong routing.
- Commit tracking DB to GitHub

**Done criterion:** item-audit-pipeline runs end-to-end on I-01 without manual intervention.
CON-0251 deleted and re-logged correctly. Audit brief committed at correct path.

### Phase 5 — Integrate into C3 workflow · 1 session · Sonnet

Update `workplan/workplan-co0007-v4.md`:
- C2 sub-stages: add Phases 0–4 as C2.x entries
- C3 task list: add "run item-audit-pipeline" as first task per item
- Note: items with open RP or CONF gaps after pipeline run should have those gaps closed
  before C3 atom authoring begins, where feasible
- Budget table: reflect §7 revised figures
- Add C3 calibration note (§7)

**Done criterion:** workplan-co0007-v4.md updated and committed.

---

## 7. Budget Impact

| Phase | Sessions | Model | Confidence |
|---|---|---|---|
| Phase 0: Decision records | 2 | Opus | HIGH |
| Phase 1: Schema (3 sessions) | 3 | Sonnet | HIGH |
| Phase 2: Skill modifications | 2 | Sonnet | HIGH |
| Phase 3: New skills | 3–4 | Sonnet/Opus | MODERATE |
| Phase 4: Consolidator + wrapper | 3 | Sonnet | MODERATE |
| Phase 5: Workplan integration | 1 | Sonnet | HIGH |
| **Total pipeline build** | **14–15** | | |

**C3 per-item pipeline overhead:**

| Item complexity | Estimated sessions |
|---|---|
| Simple: ≤3 populations, BPC exists, few conflicts | ~0.5 |
| Median: ~5 populations, moderate BPC coverage | ~1.0 |
| Complex: 8+ populations, residential room scope, thin evidence | ~1.5 |

Range for 103 items: **45–137 sessions** (best to worst case).

This range is unvalidated. Before committing the full C3 budget, run the pipeline on 5 items
spanning complexity levels after Phase 4 completes and calibrate from observed data. Do not
treat 45–137 as a committed estimate until calibration is done.

**Revised C-stage budget (illustrative pending calibration):**

```
C1:       3–5 sessions    (unchanged)
C2:       10–14 + 14–15 pipeline build = 24–29 sessions
C3:       25–35 + 45–137 pipeline pre-pass = 70–172 sessions
C4–C11:   unchanged (~91–120 sessions)
──────────────────────────────────────────────────────────
C-stage:  188–326 sessions (was 121–177)
```

**Revised project total:** 231–369 sessions (was 188–253).
Upper bound reflects worst-case per-item complexity. Calibrate before treating as binding.

---

## 8. Immediate Next Actions

1. **Author D-0141 through D-0150** — Phase 0. Two Opus sessions. Hard gate on everything else.

2. **Migration 004** — Phase 1 (3 sessions). Requires Phase 0 complete.

3. **Skill modifications** — Phase 2. Requires Phase 1 complete.

4. **New skills + wrapper** — Phases 3–4. Requires Phase 2 complete.

5. **CON-0251 cleanup** — Phase 4 Session 3. Requires `delete-connection` CLI from Phase 1.
   Category: RP (research gap). Cannot be done before Phase 1.

6. **Workplan integration** — Phase 5. Requires Phase 4 complete.

7. **C3 calibration** — After Phase 4, before committing full C3 budget. Run pipeline on
   5 items across complexity range. Revise per-item estimate from observed data.

---

## 9. Long-Term Integrity Notes

### 9.1 The pipeline is a quality floor, not a quality ceiling
Running the pipeline surfaces all findable structural issues. Research gaps (RP, EC, CONF)
may remain open after the pipeline. The brief tells ISW what is known and unknown.
ISW authors from known evidence; unknown items carry explicit disclosure per A6.

### 9.2 Gap deduplication is the consolidator's responsibility
Gap IDs remain sequential (GAP-NNN). Consolidator checks for near-duplicates before logging.
On ambiguous match: surface to user for confirmation — do not auto-resolve.

### 9.3 Wrapper state must survive context loss and mid-step failure

Before each step: add step name to `steps_started`, commit.
After each step: add step name to `steps_complete`, commit.
On resume: any step in `steps_started` but not `steps_complete` → re-run from beginning.
Steps must be idempotent at DB level (INSERT OR IGNORE, dedup checks, UNIQUE constraints).
On resume: compare spec_hash. Mismatch → warn; prompt restart or continue with flag.
Session files are never used to determine pipeline state.

### 9.4 New pipeline skills must declare an output contract in SKILL.md §Outputs
Required: tables written (tracking vs website DB), gap categories used, source_skill value,
citation-miner relevance filter, idempotency mechanism.

### 9.5 The two-database boundary is permanent
Tracking DB: project-operational. Website DB: publication-facing. Never merge as shortcut.
Maturation of a tracking DB finding into website content is a deliberate editorial act.

### 9.6 Conflict content lives in two places by design
Tracking DB `conflicts` (CONF-NNNN): per-item audit findings.
Website DB `conflict` (domain codes): canonical 12-domain resolution content for the website.
Both use the same domain taxonomy codes. Not merged; not FK-linked (cross-DB FK impossible).
After C6: no parallel conflict records in markdown files. Website DB is canonical content
record; tracking DB is canonical audit record. C6 content migration goes to website DB only.

### 9.7 Multi-session staleness detection
`spec_hash` on item_audit_runs enables staleness detection. If item spec changes mid-audit,
wrapper detects on resume and prompts: restart (all findings re-evaluated) or continue
(stale-state flag in brief). Silent continuation is not permitted.

**Normalization before hashing:** Wrapper strips leading/trailing whitespace, normalises
line endings to `\n`, and removes any frontmatter timestamps before MD5. Without
normalisation, cosmetic edits (e.g., editor-injected line ending changes) trigger false
staleness alerts. Phase 4 implementation detail.

### 9.8 C3 budget commitment gate
Do not commit to the full C3 pipeline pre-pass budget before calibration data exists.
Run 5 items post-Phase 4. If median item ≤ 0.75 sessions: revise C3 downward.
If median item ≥ 1.25 sessions: flag for user decision on scope or sequencing.

---

*CO-0009 v2 — PROPOSED*
*Activation gate: D-0141 through D-0150 authored and status ACTIVE.*
*Budget gate: calibrate per-item estimate on 5 items after Phase 4 before committing full C3.*
