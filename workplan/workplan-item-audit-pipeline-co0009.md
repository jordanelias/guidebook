# CO-0009 — Item Audit Pipeline
**Created:** 2026-05-05 19:04 UTC
**Model:** Sonnet 4.6 (audit) / Opus required for FDA + economics-auditor skill design
**Status:** PROPOSED — requires decision record authoring before implementation
**Authority:** Audit session 2026-05-05 — full skill and DB audit against current repository
**Slots into:** C1 (schema), C2 (skills), C3 (per-item pre-pass)
**Supersedes:** Nothing. Extends CO-0008.

---

## 1. Problem Statement

The current project has no systematic per-item quality pipeline. Items are written (ISW) and
research is conducted (FDR, multilingual-research), but there is no structured mechanism to:

- Surface undocumented cross-item relationships before authoring
- Map population conflicts before writing specs that must resolve them
- Confirm that functional deficit scoping is correct before research is commissioned
- Assess economic framing at item level
- Route findings to the correct research skill with an auditable handoff

Without this, C3 (91+ items) risks authoring atoms on incomplete or incorrectly scoped items,
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
        └── produces: research brief (GitHub MD) + item_audit_runs complete
```

Each step can be called individually. The wrapper orchestrates the sequence, tracks state
in `item_audit_runs`, and handles session boundaries.

---

## 3. Skills Inventory

### 3.1 Skills requiring modification

| Skill | Change | Severity |
|---|---|---|
| connection-discovery | Merge connection-scout; add mode flag; add non-connection exit routing | MAJOR |
| cross-population-conflict-mapper | Write to conflicts table (not archived MD files); update Feeds FROM reference | MODERATE |
| content-gap-analyzer | Add session-groupable output summary line | MINOR |
| evidence-auditor | Add SQLite write for flagged findings (category EG) | MODERATE |

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

## 4. Schema Requirements

### 4.1 Decision records required before any schema work (A12 compliance)

Ten D-SCHEMA decisions must be authored and approved before migration 004 is written.
All are DG-REVIEW (delegable with review) per decision-protocol.md category defaults.

| Decision | Summary |
|---|---|
| D-A | items table: migrate schemas/item.py to SQLite |
| D-B | item_audit_runs table: pipeline state tracking per item |
| D-C | conflicts table: structured conflict-mapper output (replaces MD files) |
| D-D | Gap categories CONF + AUDT: extend CHECK constraint |
| D-E | citation_mining.deferred_reason column: inline citation routing |
| D-F | Merge connection-scout → connection-discovery: deprecate connection-scout |
| D-G | functional-deficit-auditor: scope, model assignment, ICF alignment |
| D-H | economics-auditor: scope, boundary with economics-researcher |
| D-I | audit-consolidator: output contract, GitHub brief format |
| D-J | item-audit-pipeline: wrapper architecture, session boundary handling |

### 4.2 Migration 004 schema (after decisions approved)

#### items
```sql
CREATE TABLE items (
  item_code           TEXT PRIMARY KEY,
  item_id             TEXT UNIQUE,
  category            TEXT NOT NULL CHECK(category BETWEEN 'A' AND 'K'),
  category_name       TEXT NOT NULL,
  name                TEXT NOT NULL,
  applicable_groups   TEXT,              -- CSV: UPL,MOB,DEM
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

#### item_audit_runs
```sql
CREATE TABLE item_audit_runs (
  run_id              TEXT PRIMARY KEY,  -- {item_code}_{YYYY-MM-DD}
  item_code           TEXT NOT NULL REFERENCES items(item_code),
  session             TEXT NOT NULL,
  steps_complete      TEXT NOT NULL DEFAULT '[]', -- JSON array
  status              TEXT NOT NULL DEFAULT 'IN-PROGRESS'
                      CHECK(status IN ('IN-PROGRESS','COMPLETE','HANDED-OFF')),
  brief_path          TEXT,              -- GitHub path to audit brief MD
  created_at          TEXT NOT NULL,
  created_by_session  TEXT NOT NULL,
  updated_at          TEXT NOT NULL,
  updated_by_session  TEXT NOT NULL
);
CREATE INDEX idx_audit_runs_item ON item_audit_runs(item_code);
CREATE INDEX idx_audit_runs_status ON item_audit_runs(status);
```

#### conflicts
```sql
CREATE TABLE conflicts (
  conflict_id         TEXT PRIMARY KEY,  -- CONF-NNNN
  item_code           TEXT REFERENCES items(item_code),
  domain              TEXT NOT NULL,     -- 12-domain taxonomy
  pop_a               TEXT NOT NULL,
  pop_b               TEXT NOT NULL,
  status              TEXT NOT NULL
                      CHECK(status IN (
                        'RESOLVED-EVIDENCE','RESOLVED-CONSENSUS',
                        'RESOLUTION-PROPOSED','UNRESOLVED','MODE-S-ONLY'
                      )),
  resolution          TEXT,
  evidence            TEXT,
  gap_id              TEXT REFERENCES gaps(gap_id),
  source_skill        TEXT NOT NULL DEFAULT 'cross-population-conflict-mapper',
  created_at          TEXT NOT NULL,
  created_by_session  TEXT NOT NULL,
  updated_at          TEXT NOT NULL,
  updated_by_session  TEXT NOT NULL
);
CREATE INDEX idx_conflicts_item ON conflicts(item_code);
CREATE INDEX idx_conflicts_domain ON conflicts(domain);
CREATE INDEX idx_conflicts_status ON conflicts(status);
```

#### Gap category expansion (migration recreation pattern, follows 002)
New categories: CONF (conflict needing resolution evidence), AUDT (audit finding — authoring error)
Full CHECK: `'RP','SW','CR','ST','MX','CD','EC','EG','CI','DEC','CONF','AUDT'`

#### citation_mining column addition
```sql
ALTER TABLE citation_mining ADD COLUMN deferred_reason TEXT;
```

### 4.3 db.py CLI extensions required

| Command | Purpose |
|---|---|
| `add-conflict` | Insert conflict record |
| `update-conflict` | Update status/resolution |
| `conflicts` | Query conflicts (--item, --domain, --status) |
| `next-id conflicts` | Sequential CONF-NNNN |
| `add-audit-run` | Create item_audit_runs row |
| `update-audit-run` | Update steps_complete, status |
| `audit-runs` | Query by item_code or status |
| `add-item` | Insert item row |
| `items` | Query items |

### 4.4 What writes where — complete cross-reference map

| Pipeline step | Table written | Gap category | ID format |
|---|---|---|---|
| connection-discovery (connection) | connections + connection_targets | — | CON-NNNN |
| connection-discovery (non-connection gap) | gaps | CR or SW | GAP-NNN |
| cross-population-conflict-mapper (any) | conflicts | — | CONF-NNNN |
| cross-population-conflict-mapper (UNRESOLVED) | gaps (+ conflict FK) | CONF | GAP-NNN |
| content-gap-analyzer | gaps | MX, RP, ST, CD | GAP-NNN |
| evidence-auditor (flagged only) | gaps | EG | GAP-NNN |
| functional-deficit-auditor (FDR trigger) | gaps | RP | GAP-NNN |
| functional-deficit-auditor (scope error) | gaps | AUDT | GAP-NNN |
| economics-auditor (missing content) | gaps | EC | GAP-NNN |
| economics-auditor (framing violation) | gaps | AUDT | GAP-NNN |
| citation-miner (relevant) | citation_mining (mined) | — | slug+ref |
| citation-miner (not relevant) | citation_mining (deferred_reason) | — | slug+ref |
| audit-consolidator | item_audit_runs (COMPLETE) + GitHub brief | — | run_id |

Evidence-auditor CONFIRMED_STRATUM findings: brief only — not logged to DB.
CONFIRMED_STRATUM is not a gap; it does not need to be tracked.

---

## 5. Data Management Principles

These govern the pipeline and any future extensions. They are normative.

### 5.1 SQLite is the single source of truth for actionable items
All findings that require action (research, authoring, conflict resolution, audit correction)
must be in SQLite before the session closes. Prose descriptions in session files or GitHub
markdown are secondary — they explain, they do not govern. A finding that exists only in
markdown is not tracked and will be lost.

### 5.2 Session is the run identifier
`created_by_session` is the primary grouping key for all pipeline outputs. The consolidator
queries by session. No separate run_id table is needed for grouping — `item_audit_runs`
anchors the session to the item. Do not introduce a separate run_id namespace.

### 5.3 Gap categories map to resolving skills, not to finding types
The gap category is a routing code, not a classification. `RP` means "a research pass will
close this." `AUDT` means "an authoring correction will close this." A finding that generates
a gap must be assigned the category that correctly identifies which skill and which type of
work closes it. Wrong category = wrong routing = gap sits open indefinitely.

**Resolving skill by category:**

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
| AUDT | item-specification-writer (scope correction) |
| CI | technical |
| DEC | workplan-orchestrator |

### 5.4 Conflicts are a separate entity from gaps
A conflict record (CONF-NNNN) is not a gap. It describes a population opposition that may
or may not require research. RESOLVED conflicts need no gap. UNRESOLVED conflicts generate
a gap (category CONF) that routes to conflict-mapper for a resolution evidence run.
Do not collapse conflicts into gaps; the conflicts table carries analytical detail
(domain, pop_a, pop_b, resolution mechanism) that the gaps table cannot hold.

### 5.5 Citation-miner depth-1 rule is a data integrity rule, not a performance rule
Mining discovered sources in the same session creates circular dependency chains in the
evidence graph and makes provenance unauditable. Depth-1 is enforced at the wrapper level,
not just the skill level. `deferred_reason` on citation_mining makes this auditable.

### 5.6 Evidence-auditor CONFIRMED findings are not stored
Logging confirmed evidence to the DB creates noise that obscures actionable items. The
audit brief (GitHub MD) is the permanent record for confirmed findings. SQLite is for
open items only. This is the same principle as gaps: CLOSED gaps are retained (audit
trail) but CONFIRMED evidence never enters the gaps table.

### 5.7 The items table is the pipeline anchor
Every audit run must FK to an item_code in the items table. This enforces that:
(a) the item exists in structured form before audit begins,
(b) all findings are traceable to a specific item,
(c) the audit_runs table gives a complete history of which items have been audited
    and when — queryable without scanning GitHub session files.

### 5.8 Economics-auditor never triggers economics-researcher inline
Economics-auditor is a checklist. Economics-researcher is a full research run.
The auditor's output is a gap (category EC) flagging that economics content is needed.
Economics-researcher runs in a separate session against that gap. Inlining would make
the pipeline context-prohibitive for any item with economics gaps.

### 5.9 source_skill is a controlled vocabulary
All skills writing to connections or gaps must use the exact skill name from their SKILL.md
`name:` field. Free-text `source_skill` breaks queryability. Controlled values for the
pipeline (to be added to project-standards.md):

`connection-discovery` · `cross-population-conflict-mapper` · `content-gap-analyzer` ·
`evidence-auditor` · `functional-deficit-auditor` · `economics-auditor` ·
`audit-consolidator` · `item-audit-pipeline` · `citation-miner`

---

## 6. Build Order and Session Estimates

### Phase 0 — Decision records · 2 sessions · Opus
Author all 10 D-SCHEMA decision records (D-A through D-J).
Batch: 5 per session. Standard DG-REVIEW delegation.
No code written until decisions are authored.

**Done criterion:** All 10 decisions in decisions table with status ACTIVE.

### Phase 1 — Schema (migration 004) · 2 sessions · Sonnet
Session 1: items table + item_audit_runs + conflicts table + db.py CLI extensions.
Session 2: gap category expansion (migration recreation) + citation_mining.deferred_reason
           + Pydantic schema updates (gap.py validator, new conflict.py model).
CI must pass before Phase 2 begins.

**Done criterion:** schema_version = 4; all new tables queryable via db.py; validators pass.

### Phase 2 — Skill modifications · 2 sessions · Sonnet
Session 1: Merge connection-scout → connection-discovery (add mode flag, non-connection
           routing, external mode, SPECULATIVE→gap rule). Move connection-scout to
           skills/deprecated/.
Session 2: Fix conflict-mapper output (→ conflicts table, archived MD references removed).
           Update evidence-auditor (add EG gap logging). Update content-gap-analyzer
           (session-groupable output summary).

**Done criterion:** All four modified skills produce SQLite output against the new schema.
Test run: connection-discovery on I-01 (both modes); conflict-mapper on a 2-population item;
evidence-auditor on A-01; content-gap-analyzer on B-01.

### Phase 3 — New skills: FDA + economics-auditor · 3–4 sessions · Sonnet (Opus approval)
Session 1: functional-deficit-auditor SKILL.md design (Opus reviews ICF taxonomy import
           from FDR; approves audit checklist and FDR trigger criteria).
Session 2: functional-deficit-auditor implementation + test run on I-01.
Session 3: economics-auditor SKILL.md + implementation + test run on I-01.
Optional session 4: refinement pass if test runs reveal scope issues.

**Done criterion:** Both skills produce correct SQLite output on test item I-01.
FDA correctly identifies that I-01 SCI thermal content is misplaced (scope error → AUDT).
Economics-auditor correctly flags I-01 retrofit note as asserted-not-evidenced (→ EC).

### Phase 4 — audit-consolidator + wrapper · 3 sessions · Sonnet
Session 1: audit-consolidator SKILL.md + implementation.
Session 2: item-audit-pipeline wrapper SKILL.md + implementation.
Session 3: Full pipeline test run on I-01 (all 8 steps). Verify:
           - item_audit_runs status=COMPLETE after run
           - audit brief committed to GitHub
           - all expected gaps and connections in SQLite
           - CON-0251 cleaned up (delete misclassified connection, re-log as AUDT gap)
           - deferred citations catalogued with deferred_reason

**Done criterion:** item-audit-pipeline runs end-to-end on I-01 without manual intervention.
Consolidator produces a research brief that correctly routes:
  FDR trigger → RP gap
  Misplaced SCI content → AUDT gap
  Economics gap → EC gap

### Phase 5 — Integrate into C3 workflow · 1 session · Sonnet
Update workplan-co0007-v4.md:
- C3 task list: add "run item-audit-pipeline" as first task for each item
- Note: pipeline output (research brief) informs which RP/EC/CONF gaps must be closed
  before C3 atom authoring for that item
- C2 task list: add Phase 0–4 above as C2.x sub-stages

**Done criterion:** Updated workplan adopted; C2 session budget increased by 12–14 sessions.

---

## 7. Budget Impact

| Phase | Sessions | Model | Confidence |
|---|---|---|---|
| Phase 0: Decision records | 2 | Opus | HIGH |
| Phase 1: Schema | 2 | Sonnet | HIGH |
| Phase 2: Skill modifications | 2 | Sonnet | HIGH |
| Phase 3: New skills (FDA + economics-auditor) | 3–4 | Sonnet/Opus | MODERATE |
| Phase 4: Consolidator + wrapper | 3 | Sonnet | MODERATE |
| Phase 5: Workplan integration | 1 | Sonnet | HIGH |
| **Total** | **13–14** | | |

**C3 per-item overhead:** The pipeline adds ~0.5 sessions per item as a pre-pass.
For 91 items, this is 45–50 additional sessions. However, this replaces ad hoc
rework that would otherwise occur mid-C3 when scope errors and conflicts surface.
Net budget impact is neutral-to-positive: pipeline overhead is predictable; rework is not.

**Revised C-stage budget:**
```
C1:  3–5 sessions  (unchanged)
C2:  10–14 + 13–14 pipeline = 23–28 sessions
C3:  25–35 + 45–50 pre-pass = 70–85 sessions
C4–C11: unchanged
C-stage total: 166–228 sessions (was 121–177)
```

**Revised project total:** 201–271 sessions (was 188–253). Increase of ~13–18 sessions net
(pipeline build) + 45–50 sessions (C3 pre-pass overhead absorbed from rework reduction).

---

## 8. Immediate Next Actions

Priority order before C3 begins:

1. **Clean up CON-0251** — delete misclassified connection; re-log as gap category AUDT.
   Can be done in any session immediately, no schema dependency.

2. **Author D-A through D-J** — 10 decision records. Phase 0. Two Opus sessions.
   Nothing else in this workplan proceeds without these.

3. **Migration 004** — Phase 1. Two Sonnet sessions. Requires Phase 0 complete.

4. **Skill modifications** — Phase 2. Two Sonnet sessions. Requires Phase 1 complete.

5. **New skills** — Phases 3–4. Six to seven sessions. Requires Phase 2 complete.

6. **Workplan integration** — Phase 5. One session. Requires Phase 4 complete.

---

## 9. Long-Term Integrity Notes

### 9.1 The pipeline is a quality floor, not a quality ceiling
Running the pipeline does not mean an item is ready for C3 authoring. It means all
findable structural issues have been surfaced. Research gaps (RP, EC) may remain open
after the pipeline — those are addressed in separate research sessions. The pipeline
brief tells the ISW what is known and unknown before atom authoring begins. The ISW
authors atoms from the known evidence; unknown items carry explicit disclosure per
project-standards (evidence-state machine, A6).

### 9.2 Pipeline is idempotent by design
Running the pipeline twice on the same item should not produce duplicate findings.
Dedup is enforced by:
- connection-discovery: dedup load at Step 0 (existing CON-IDs)
- gaps: gap_id is deterministic from item+category+description hash (to be implemented)
- conflicts: dedup by (item_code, domain, pop_a, pop_b) unique constraint
- citation_mining: is-mined check before any mining

If a gap_id hash is not yet implemented, the consolidator must check for near-duplicate
gap descriptions before logging. This is a Phase 4 implementation detail.

### 9.3 Wrapper state must survive context loss
item_audit_runs.steps_complete is the ground truth for pipeline progress. If context
is lost mid-run, the next session reads item_audit_runs and resumes from the first
incomplete step. Session files are secondary. The wrapper must write steps_complete
after EACH step completes — not only at the end of the run.

### 9.4 New skills entering the pipeline must declare their output contract
Any future skill added to the pipeline must declare:
- Which tables it writes to
- Which gap categories it uses
- What its source_skill value is
- Whether it has a relevance filter for citation-miner
This declaration goes in the skill's SKILL.md §Outputs, not in prose.

### 9.5 The conflicts table is the authoritative conflict record from this point forward
The C6 conflict migration (conflicts.json → SQLite) produces the historical conflict
records. The pipeline produces new conflicts per item. Both live in the same conflicts
table. The migration populates item_code=NULL for historical conflicts not yet associated
with a specific item; the pipeline populates item_code for all new conflicts.
Do not maintain parallel conflict records in markdown files after C6.

---

*CO-0009 PROPOSED — not adopted until D-A through D-J authored and approved.*
*Author D-SCHEMA decision records to activate.*
