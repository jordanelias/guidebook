# S4 — SYNTHESIS STAGE smoke test log

Agent: S4. Stage under test: `synthesis` per `governance/pipeline-contract.yaml`.
Scratch DB: `$SMOKE/s4-synthesis.db` (copy of committed `data/guidebook.db`, sha256
`30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf` at start).
Start time: 2026-08-25 18:17 UTC.

Synthesis tables per assignment: `bpc_metadata` (0), `item_bpc_links` (0), `connections`/
`connection_targets` (0/0), `conflicts` (0), `reasoning_doc_citations` (0), `weighting_profile` (5),
`citation_population_links` (0). Nearly all empty — treated as condition under test.

---
## 1. The 9-step synthesis procedure — `scripts/validate_reasoning.py`

### 1a. --help
INVOKED   : `python3 scripts/validate_reasoning.py --help`
STAGE     : synthesis
EXIT      : 0   RUNTIME: <1s
READS     : scripts/validate_reasoning.py (argparse)
WRITES    : NONE
EXAMINED  : n/a (help only)
OUTPUT    : usage with --slug/--con/--mode/--strict/--json
FINDING   : PASS
LOCATION  : scripts/validate_reasoning.py:268-276
NOTE      : Standard CLI surface. --strict is opt-in and off by default (see 1c).

### 1b. Ratified 9-step procedure — source
INVOKED   : (read only) `governance/pipeline-contract.yaml` synthesis.criteria[0];
             `scripts/validate_reasoning.py:54-64`
STAGE     : synthesis
EXIT      : n/a
READS     : governance/pipeline-contract.yaml (synthesis anchor: "PI rule #9 (9-step)");
             scripts/validate_reasoning.py:54-64 `NINE_STEPS`
WRITES    : NONE
EXAMINED  : 1 (the hardcoded NINE_STEPS list)
OUTPUT    : NINE_STEPS = ["Step 1 — Direction", "Step 2 — Per-population worst-case user",
             "Step 3 — Jurisdiction comparison", "Step 4 — Lowest-barrier code per population",
             "Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence",
             "Step 6 — Guidebook chosen value per population", "Step 7 — Rationale",
             "Step 8 — Trade-offs", "Step 9 — Cross-population conflict flag"]
FINDING   : PASS (the 9-step list is findable and lives in exactly one place)
LOCATION  : scripts/validate_reasoning.py:54-64
NOTE      : Steps 1-4 are Sonnet-tier facts, 5-9 are Opus-tier judgment (per code comment
             at :152-156, citing "standing rule #2" i.e. PI rule #2 Opus floor). This
             coupling matters for item 2 below.

### 1c. What the validator actually checks — structure, presence, or reasoning?
INVOKED   : code read, `scripts/validate_reasoning.py:88-187` (validate_bpc_doc)
STAGE     : synthesis
EXIT      : n/a
READS     : scripts/validate_reasoning.py:100-185
WRITES    : NONE
EXAMINED  : 1 function
OUTPUT    : Every check is a regex/string-presence test: header field regex
             (`^\*\*{field}:\*\*`), section-header regex (`^#{2,4}\s+{section}`), and for the
             B-section, `step_pat.search(block)` — literal substring/case-insensitive match of
             the step's LABEL TEXT (e.g. "Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3
             evidence") anywhere in the parameter block. There is no check that the content
             under a step heading says anything coherent, cites anything real, or reaches a
             defensible conclusion — a block containing the nine step headings verbatim with
             empty or nonsensical bodies passes with zero errors.
FINDING   : VACUOUS-BY-DESIGN (structure/presence only, never reasoning quality)
LOCATION  : scripts/validate_reasoning.py:147-151 (`step_pat.search(block)`), :102-104
             (header-field presence), :119-123 (section presence)
NOTE      : This is failure mode (a)/(c) hybrid: it is not that the check examines 0 subjects
             (it does examine real docs, EXAMINED:3 below), it is that "passing" only proves
             the document is well-FORMATTED, never that steps 5-9 (the Opus judgment steps)
             are true, cite real evidence, or were actually reasoned through. A fabricated
             synthesis with perfect headings is indistinguishable from a real one to this tool.

### 1d. Run against committed reasoning docs
INVOKED   : `python3 scripts/validate_reasoning.py --mode all`
STAGE     : synthesis
EXIT      : 0   RUNTIME: 0.057s
READS     : references/bpc-reasoning/*.md (glob), references/connection-reasoning/*.md (glob)
WRITES    : NONE
EXAMINED  : 3 (printed "EXAMINED: 3" — 2 templates skipped, 1 real doc:
             room-acoustic-performance.md)
OUTPUT    : |
  [ERROR] references/bpc-reasoning/room-acoustic-performance.md
          ERROR: Missing required header field: **BPC file**
          ERROR: Missing required header field: **BPC population**
          ERROR: Missing required header field: **Generated**
          ERROR: Status 'PILOT' not in ['COMPLETE', 'DRAFT', 'OPUS-PENDING']
          ERROR: Missing required section: 'A. Evidence inventory'  [... 8 more missing
                 sections through F. Provenance trail]
  Summary: 0 clean, 0 with warnings, 1 with errors, 2 skipped (templates)
  EXAMINED: 3
FINDING   : FAIL (errors present) but reported EXIT 0 — see 1e
LOCATION  : references/bpc-reasoning/room-acoustic-performance.md (Status: PILOT, predates
             the current template entirely — it is a Phase E.1 pilot doc using its own
             informal structure, not the A-F section scaffold the validator now expects)
NOTE      : The ONLY real BPC reasoning doc in the repo is for `room-acoustic-performance`
             (sensory-environment topic) — NOT a mobility slug. Every mobility slug in the
             PROTOCOL's item list (corridor width, ramp gradient, door thresholds, etc.) has
             ZERO reasoning doc. See 1f.

### 1e. --strict flag is required for the check to mean anything
INVOKED   : `python3 scripts/validate_reasoning.py --mode all --strict`
STAGE     : synthesis
EXIT      : 1   RUNTIME: <1s
READS     : same as 1d
WRITES    : NONE
EXAMINED  : 3
OUTPUT    : same errors as 1d, but process exit code 1
FINDING   : PASS (the --strict path correctly fails on real errors)
LOCATION  : scripts/validate_reasoning.py:330-331 (`if args.strict and err_files: return 1`)
NOTE      : Confirms `governance/check-registry.yaml:1125` note verbatim: "Without the flag it
             prints its errors and returns 0 by design... the unflagged invocation is a green
             tick that means nothing." The registry entry (id: validate_reasoning, line 1125)
             DOES pass --strict and is correctly RED today per its own note. BUT level is
             `advisory` (line 1128), not blocking — so a mobility batch that ships a reasoning
             doc with missing sections would show red on an advisory check, block nothing,
             and could still be merged. basis: synthesis/nine-step-synthesis — this is the
             ONLY mechanical tie from pipeline-contract.yaml's nine-step-synthesis criterion
             to enforcement, and it is non-blocking.

### 1f. Behavior when the doc does not exist (the mobility-slug case)
INVOKED   : `python3 scripts/validate_reasoning.py --slug corridor-clear-width` and
             `--slug ramp-gradient`
STAGE     : synthesis
EXIT      : 0   RUNTIME: <1s (both)
READS     : references/bpc-reasoning/corridor-clear-width.md (does not exist),
             references/bpc-reasoning/ramp-gradient.md (does not exist)
WRITES    : NONE
EXAMINED  : 0 — printed "No reasoning docs found in mode=all." (NOTHING-IN-SCOPE)
OUTPUT    : |
  ERROR: BPC reasoning doc not found: /home/user/guidebook/references/bpc-reasoning/corridor-clear-width.md
  No reasoning docs found in mode=all.
    Expected location: references/bpc-reasoning
    Expected location: references/connection-reasoning
  EXIT: 0
FINDING   : VACUOUS — exits 0 (success) when the named subject does not exist, both with and
             without --strict (the empty-files-list early return at :279-286 returns 0
             unconditionally, before the --strict/err_files check is ever reached)
LOCATION  : scripts/validate_reasoning.py:278-286 (`if not files: ... return 0`)
NOTE      : **This is failure mode (a) verbatim for the mobility batch specifically.** A
             mobility-slug BPC synthesis that never gets a reasoning doc written for it (or
             whose filename doesn't match the slug) passes `--strict` cleanly — the ERROR line
             goes to stderr but the exit code is still 0. There is no "required reasoning doc
             is missing" failure state; missing-entirely and correctly-validated-with-zero-hits
             both read as pass. Confirmed via the registry's own `min_items:1` note (line
             1131) which exists precisely because 0-examined would otherwise be a false green
             — but --slug bypasses the glob-based `min_items` framing entirely since it's a
             single-file lookup with its own early-return path.

## 2. `best_practice_synthesis` and the Opus floor

### 2a. `db.py update-bpc` on the scratch DB for a mobility slug
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s4-synthesis.db python3 scripts/db.py update-bpc
             --slug corridor-clear-width --session session_2026-08-25-s4-smoketest
             --bpc-complete 0 --dry-run`
STAGE     : synthesis
EXIT      : see below
READS     : bpc_metadata schema (scratch DB)
WRITES    : (dry-run — see below)
EXAMINED  : 1 slug
FINDING   : see below (run captured together with 2b)
LOCATION  : scripts/db.py update-bpc handler
NOTE      : see 2b for the actual invocation+output; folded together to avoid duplication.

### 2b. `update-bpc` CLI surface — no authorship/model field exists to set
INVOKED   : `python3 scripts/db.py update-bpc --help`; source read `scripts/db.py`
             (argparse block for `update-bpc`)
STAGE     : synthesis
EXIT      : 0
READS     : scripts/db.py (update-bpc argparse), data/guidebook.db schema for `bpc_metadata`
             (read via `sqlite_master`)
WRITES    : NONE
EXAMINED  : 1 (the update-bpc parser)
OUTPUT    : |
  usage: db.py update-bpc [-h] --slug SLUG --session SESSION
                          [--citation-mining-complete {0,1}] [--bpc-complete {0,1}]
                          [--search-complete {0,1}] [--pico-complete {0,1}]
                          [--evidence-state EVIDENCE_STATE]
                          [--supersession-check-complete {0,1}]
                          [--closure-definition-version {v1,v2}] [--dry-run]
FINDING   : ABSENT — confirmed no `--model`/`--author-tier`/`--opus-reviewed` flag exists.
LOCATION  : scripts/db.py (update-bpc arg parser)
NOTE      : Every flag is a completeness/state flag. There is nowhere on the write path to
             record which model tier authored the synthesis.

### 2c. `bpc_metadata` schema — no authoring-model column
INVOKED   : `sqlite3` (via Python) `SELECT sql FROM sqlite_master WHERE name='bpc_metadata'`
             against the committed `data/guidebook.db` (read-only)
STAGE     : synthesis
EXIT      : 0
READS     : data/guidebook.db (sqlite_master, read-only URI mode)
WRITES    : NONE
EXAMINED  : 1 table definition
OUTPUT    : |
  CREATE TABLE bpc_metadata (
      slug TEXT PRIMARY KEY REFERENCES slugs(slug), population TEXT NOT NULL,
      last_updated TEXT, jurisdictions_searched INTEGER DEFAULT 0,
      co1_pass_count INTEGER DEFAULT 0, evidence_state TEXT,
      pico_complete INTEGER ..., search_complete INTEGER ..., bpc_complete INTEGER ...,
      citation_mining_complete INTEGER ..., created_at TEXT NOT NULL,
      created_by_session TEXT NOT NULL, updated_at TEXT NOT NULL,
      updated_by_session TEXT NOT NULL, supersession_check_complete INTEGER ...,
      closure_definition_version TEXT ...)
FINDING   : ABSENT — no `model`, `author_model`, `model_tier`, or `opus_reviewed` column.
             `created_by_session`/`updated_by_session` store a session-id STRING
             (`session_YYYY-MM-DD...`), which encodes no model identity — a session id
             does not carry which model served that session (per `get_session` /
             `external_metadata.last_served_model` being a runtime fact, never written to
             this DB).
LOCATION  : bpc_metadata table definition (`scripts/migrations/057_baseline_2026-08-12.sql:64`
             — CREATE TABLE bpc_metadata)

### 2d. Contract's own admission
INVOKED   : (read only) `governance/pipeline-contract.yaml` synthesis.criteria[1]
STAGE     : synthesis
EXIT      : n/a
READS     : governance/pipeline-contract.yaml:113-117
WRITES    : NONE
EXAMINED  : 1
OUTPUT    : |
  - id: opus-routing
    kind: completeness
    criterion: "best_practice_synthesis is authored at the ratified capability floor
                (Opus-class), never by a lower tier (rule #2)."
    references: "PI rule #2; DR-2026-06-10-synthesis-model-floor"
    check: null
FINDING   : ABSENT (contract admits it explicitly: `check: null`)
LOCATION  : governance/pipeline-contract.yaml:113-117

### 2e. Searched for ANY mechanical enforcement elsewhere
INVOKED   : `grep -rniI "opus" scripts/ tools/ schemas/ governance/check-registry.yaml .github/`
             plus targeted follow-ups on `opus_reviewed`, `model_routing`,
             `scripts/decision_capture.py`
STAGE     : synthesis
EXIT      : 0
READS     : scripts/audit/pre_rehab_banner_audit.py (found: unrelated — checks a
             `[OPUS-SYNTHESIS*]` RETRACTION banner for one historical cohort, not
             authorship of new syntheses); `connections.opus_reviewed` column (found: exists,
             but `db.py add-connection` HARDCODES it to `0` at scripts/db.py:1374 and
             `update-connection` (scripts/db.py) has no flag to set it — so it can never be
             set to 1 through the sanctioned write path, and it is a connections-table field,
             not a bpc_metadata one, so irrelevant to BPC authorship even if it worked);
             `decisions.model_routing` (found: EXISTS, format `opus/150/synth` etc.,
             validated for REGEX FORMAT ONLY by `scripts/decision_capture.py` check C4 —
             governance/decision-protocol.md §7.3 — but this validates the `decisions` table
             (process/governance decisions), which has NO foreign key or join to
             `bpc_metadata` or any per-slug synthesis record. A decision about routing policy
             is not a synthesis-authorship record.)
WRITES    : NONE
EXAMINED  : grep matched ~15 files; 3 followed up in depth
OUTPUT    : `governance/decision-protocol.md §7.3`: "C4 model-routing format | ERROR |
             Matches §4.4 regex" — format only, never truth. §7.5 explicitly: "The validator
             enforces format... doctrine-recheck (A13) audits semantic correctness" (but A13
             audits DOCTRINE TEXT, not per-synthesis authorship — confirmed no A13 reference
             to bpc_metadata).
FINDING   : ABSENT
LOCATION  : No file. Nearest surfaces: governance/pipeline-contract.yaml:117 (`check: null`),
             scripts/decision_capture.py C4 (format-only, wrong table), schemas/attestation.schema.json
             (no model field — see 2f).

### 2f. Attestation schema — checked for an authoring-model field
INVOKED   : (read) `schemas/attestation.schema.json` (full file, 71 lines)
STAGE     : synthesis
EXIT      : n/a
READS     : schemas/attestation.schema.json
WRITES    : NONE
EXAMINED  : 1 schema (13 top-level properties)
OUTPUT    : Required properties: schema_version, session, artifact, doctrine_sha,
             rules_in_scope, per_rule_status, deviations, bias_direction,
             independent_reviewer_counterclaim, verdict. Optional: reattestation.
             `session` is a REGEX-PATTERNED STRING (`^session_\d{4}-\d{2}-\d{2}[a-z]?(-.*)?$`)
             — a human-readable label, not a model identifier. No `model`, `model_tier`, or
             `author_model` property exists anywhere in the schema.
FINDING   : ABSENT — confirmed by schema inspection, not inference.
LOCATION  : schemas/attestation.schema.json (entire file — the property is simply not there)

### 2g. Read the one existing DR-2026-06-10 attestation — it admits the gap itself
INVOKED   : (read) `attestations/decisions_DR-2026-06-10-synthesis-model-floor.json`
STAGE     : synthesis
EXIT      : n/a
READS     : attestations/decisions_DR-2026-06-10-synthesis-model-floor.json (the DR that
             established "Opus-class or above" AS a capability floor, not a brand pin)
WRITES    : NONE
EXAMINED  : 1 attestation
OUTPUT    : `independent_reviewer_counterclaim` field, verbatim: "An independent reviewer
             would object that 'capability floor' is unfalsifiable as stated — no benchmark
             defines 'Opus-class', so the floor collapses to 'whatever model is running'."
             The DR's own "Verification" section states: "This DR records an owner
             ratification; it makes no DB or evidence claim. Compliance with rule #11 is the
             attestation" — i.e. the ENTIRE enforcement mechanism for the Opus floor is a
             free-text attestation self-written by the same session whose model tier is under
             question, with no schema field to name that tier and no independent check of it.
FINDING   : ABSENT, and self-documented as unfalsifiable by the repository's own governing
             record.
LOCATION  : decisions/DR-2026-06-10-synthesis-model-floor.md ("Verification" section);
             attestations/decisions_DR-2026-06-10-synthesis-model-floor.json
             (`independent_reviewer_counterclaim`)
NOTE      : **Contract criterion `synthesis/opus-routing` is confirmed ABSENT end to end.**
             For a mobility batch: nothing stops a Sonnet-tier (or Haiku-tier) session from
             writing `bpc_metadata.bpc_complete=1` for corridor-clear-width, ramp-gradient,
             etc. and nothing downstream would ever detect it. **What a check would need:**
             (1) a `bpc_metadata.authored_by_model` (or `attestations` schema `model_tier`)
             column/property populated from a value the AUTHORING SESSION cannot self-report
             falsifiably — e.g. `external_metadata.last_served_model` per
             `get_session`/`mcp__Claude_Code_Remote__get_session`, captured at write time by
             the CLI itself (not typed by the agent) and stored alongside the bpc_metadata
             row or a matching decision record; (2) a CHECK/gate that reads that field and
             refuses `bpc_complete=1` unless the tier is in {opus, fable}; (3) a join from
             `bpc_metadata.slug` to whatever record carries that tier. None of the three
             exists today.

### 2h. `db.py update-bpc` on the scratch DB for a mobility slug — CRASH on first write
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s4-synthesis.db python3 scripts/db.py update-bpc
             --slug threshold-and-level-access --session session_2026-08-25-s4-smoketest
             --bpc-complete 1 [--dry-run]` (tried both dry-run and real; identical failure)
STAGE     : synthesis
EXIT      : 1 (unhandled Python traceback, not a clean CLI refusal)   RUNTIME: <1s
READS     : bpc_metadata schema (population TEXT NOT NULL); scripts/db.py:1759-1778
             (update_bpc_metadata — UPSERT: UPDATE if slug exists, else INSERT)
WRITES    : NONE (transaction rolled back on exception)
EXAMINED  : 1 slug (threshold-and-level-access — a real mobility/threshold slug present in
             `slugs`; there is no `corridor-clear-width` slug in the DB at all — checked
             `SELECT slug FROM slugs WHERE slug LIKE '%corridor%'` → 0 rows, so E-08 corridor
             width has no slug yet either, a second finding worth flagging to the batch owner)
OUTPUT    : |
  Traceback (most recent call last):
    File "/home/user/guidebook/scripts/db.py", line 1441, in main
      update_bpc_metadata(args.slug, data, ...)
    File "/home/user/guidebook/scripts/db.py", line 1779, in update_bpc_metadata
      conn.execute(f"INSERT INTO bpc_metadata ({cols}) VALUES ({ph})", ...)
  sqlite3.IntegrityError: NOT NULL constraint failed: bpc_metadata.population
FINDING   : FAIL — genuine coverage bug, not a designed refusal
LOCATION  : scripts/db.py:60-65 (`_BPC_META_COLS` whitelist DOES include `"population"`) vs.
             scripts/db.py:1039-1051 (`update-bpc` argparse block has NO `--population` flag
             at all) vs. scripts/db.py:1759-1778 (`update_bpc_metadata` INSERT branch, taken
             whenever the slug has no existing bpc_metadata row, which — since
             `bpc_metadata` is 0 rows in the committed DB today — is EVERY slug in the
             upcoming mobility batch).
NOTE      : **This is a real, reproducible bug the mobility batch will hit on its very first
             `update-bpc` call for any new slug**, because bpc_metadata starts at 0 rows.
             `population` is accepted by the internal whitelist and required by the schema,
             but the CLI gives no way to supply it — so the INSERT branch is dead code that
             can only ever raise. CLAUDE.md §4 claims "every one of those tables and columns
             now has a writer that REFUSES" (listing search_candidates,
             evidence_population_match, economics_entries, case_studies,
             jurisdictional_values, and add-source's doi/url/pages gap as the KNOWN
             exceptions) — `bpc_metadata` is not on that list, i.e. CLAUDE.md currently
             asserts this writer is COMPLETE. It is not: this is an uncaught exception, not a
             refusal message, and it blocks the very first synthesis write of the batch.
             Confirmed the UPDATE path (row pre-existing) works cleanly (2i) — only first-time
             creation is broken. **Practical workaround for the batch: seed the row via a
             migration that supplies `population`, then use `update-bpc` for all subsequent
             completeness-flag updates** — but that reintroduces exactly the "hand-written SQL
             against a table the CLI can't reach" pattern CLAUDE.md says is a coverage bug to
             fix, not a license to bypass.

### 2i. Control: `update-bpc` UPDATE path (row pre-seeded) works cleanly
INVOKED   : seeded one `bpc_metadata` row via direct SQL against the SCRATCH DB only (not
             `data/guidebook.db`; permitted — scratch is not the protected DB), then
             `GUIDEBOOK_DB_PATH=$SMOKE/s4-synthesis.db python3 scripts/db.py update-bpc
             --slug threshold-and-level-access --session session_2026-08-25-s4-smoketest
             --bpc-complete 1`
STAGE     : synthesis
EXIT      : 0   RUNTIME: <1s
READS     : bpc_metadata (scratch)
WRITES    : bpc_metadata.bpc_complete=1, updated_at, updated_by_session
             @ slug='threshold-and-level-access' (scratch DB only)
EXAMINED  : 1 row
OUTPUT    : `{"updated": true, "slug": "threshold-and-level-access", "fields": ["bpc_complete"]}`
             verified via read-only query: `[('threshold-and-level-access', 1,
             '2026-08-25 18:21', 'session_2026-08-25-s4-smoketest')]`
FINDING   : PASS (UPDATE branch only)
LOCATION  : scripts/db.py:1770-1778
NOTE      : Confirms 2h is specifically an INSERT/first-write gap, not a general breakage.

## 3. Reasoning documents

### 3a. Inventory (`ls`, not Grep — `.ignore` does not hide these paths, but confirm anyway)
INVOKED   : `ls -la references/bpc-reasoning/ references/connection-reasoning/`
STAGE     : synthesis
EXIT      : 0
READS     : references/bpc-reasoning/, references/connection-reasoning/ (directory listings)
WRITES    : NONE
EXAMINED  : 2 directories, 4 files total
OUTPUT    : bpc-reasoning/: `_template.md` (5281 bytes), `room-acoustic-performance.md`
             (41306 bytes). connection-reasoning/: `_template.md` (1322 bytes) only — NO
             real connection reasoning docs exist anywhere in the repo.
FINDING   : PASS (inventory obtained; not .ignore-hidden — these two directories are NOT in
             the `.ignore` cold-storage list, unlike `references/search-log/`)
LOCATION  : references/bpc-reasoning/, references/connection-reasoning/
NOTE      : **Exactly one real BPC reasoning doc exists in the whole repository, and it is
             for `room-acoustic-performance` (sensory-environment topic) — not a mobility
             slug.** No mobility slug (corridor width, ramp gradient, thresholds, lift,
             parking, flooring) has a reasoning doc. The mobility batch's synthesis stage
             starts from zero precedent.

### 3b. `scripts/audit/reasoning_doc_citations_audit.py`
INVOKED   : `python3 scripts/audit/reasoning_doc_citations_audit.py` (no --help path; script
             takes no flags)
STAGE     : synthesis
EXIT      : 0   RUNTIME: <1s
READS     : reasoning_doc_citations (committed DB, read-only URI), sqlite_master
WRITES    : NONE
EXAMINED  : 0 — script prints "EXAMINED: 0" itself
OUTPUT    : |
  Total rows: 0
  Table is empty (Phase E.1 has not begun for any BPC). No claim-level audit possible yet.
  [CHECK 0] Confirmed table + indexes + constraints present from migration 011.
  EXAMINED: 0
FINDING   : VACUOUS (honestly self-reported — the script itself prints EXAMINED:0 and exits
             0 rather than claiming a false pass; better-behaved than most checks in this
             repo on that count, but still a check that will pass on the entire mobility
             batch's reasoning docs unless something ELSE populates reasoning_doc_citations)
LOCATION  : scripts/audit/reasoning_doc_citations_audit.py:55-61
             (registry: governance/check-registry.yaml:1163-1176, level: advisory,
             basis: unattributed — not tied to any pipeline-contract.yaml criterion id)

### 3c. What the audit actually checks vs. what its own docstring claims
INVOKED   : full source read, `scripts/audit/reasoning_doc_citations_audit.py:1-171`
STAGE     : synthesis
EXIT      : n/a
READS     : scripts/audit/reasoning_doc_citations_audit.py (docstring lines 5-23 vs.
             function body lines 37-167)
WRITES    : NONE
EXAMINED  : 1 script
OUTPUT    : Docstring advertises 8 checks. CHECK 8 ("every BPC reasoning doc slug present in
             references/bpc-reasoning/ should have at least one row per parameter that the
             doc discusses ... this audit flags the row-side gap only") has NO corresponding
             code — the function body implements only CHECK 1 through CHECK 7 (lines 63-160);
             there is no "CHECK 8" print or query anywhere in `audit()`. It is a documented,
             advertised, un-implemented check.
FINDING   : FAIL (phantom check — docstring over-promises coverage the code does not deliver)
LOCATION  : scripts/audit/reasoning_doc_citations_audit.py:20-23 (docstring CHECK 8) vs.
             absence of any "CHECK 8" logic in :37-167 (the entire `audit()` function)
NOTE      : Independently of the phantom check, EVERY implemented check (1-7) only queries
             the `reasoning_doc_citations` TABLE — none of them parses the reasoning-doc
             prose (.md text) itself. The script never opens a `.md` file. This is confirmed
             structurally (no `Path.read_text`/`open()` call anywhere in the file — grep
             confirms zero file-read calls outside the DB connection).

### 3d. Live cross-check: does the ONE real reasoning doc's prose citations match evidence_sources?
INVOKED   : ad-hoc query — extracted all REF-\d{5} tokens from
             `references/bpc-reasoning/room-acoustic-performance.md` via regex, then looked
             each up in `evidence_sources` and `source_locators` on the committed
             (read-only) DB
STAGE     : synthesis (cross-stage read: synthesis prose vs. evidence-collection table)
EXIT      : 0
READS     : references/bpc-reasoning/room-acoustic-performance.md (full text, regex scan);
             evidence_sources.verification_status/.metadata_quality,
             source_locators.status — both on data/guidebook.db read-only
WRITES    : NONE
EXAMINED  : 11 distinct REF-ids cited in the doc's Section B synthesis reasoning
OUTPUT    : |
  REF-00325: ADMITTED  (evidence_sources VERIFIED/COMPLETE)
  REF-00335: LEAD-ONLY (source_locators REFERENCE-ONLY only)
  REF-00561: ADMITTED  (evidence_sources VERIFIED/COMPLETE)
  REF-00571: LEAD-ONLY
  REF-00576: LEAD-ONLY
  REF-00577: LEAD-ONLY
  REF-00578: ADMITTED  (evidence_sources VERIFIED/COMPLETE)
  REF-00580: LEAD-ONLY
  REF-00589: LEAD-ONLY
  REF-00726: LEAD-ONLY
  REF-00727: LEAD-ONLY
FINDING   : FAIL — 7 of 11 REF-ids (64%) cited as supporting evidence in the doc's
             per-population Section B synthesis table are LEAD-ONLY: present only in
             `source_locators`, which CLAUDE.md §4 states explicitly is "a lead index of
             identifiers, not evidence." They were never admitted to `evidence_sources`.
LOCATION  : references/bpc-reasoning/room-acoustic-performance.md:114-115,163,178,211 (NDV/AUT
             row cites REF-00727 "Marzi 2025... T1 primary" and REF-00726 "Marzi 2024...T1
             review" as flat Tier-1 evidence with a direct quote attributed to REF-00727,
             with no flag that either ref_id is unadmitted; DEAF row at :114 cites
             REF-00577/REF-00576 as "T1" alongside admitted REF-00578 with no distinction).
             One instance IS self-flagged: line 200, REF-00335, "pending citation-miner pass
             for rule-#10 eligibility" — proving the author/tooling CAN mark this state when
             it chooses to, making the other 6 unflagged LEAD-ONLY citations a real
             inconsistency, not a structural impossibility.
NOTE      : **This is a live, non-hypothetical instance of the CLAUDE.md §2(c) failure class
             moved one stage downstream, exactly as the task predicted.** Not fabrication —
             the papers appear to be real, correctly attributed, DOI-resolved leads — but
             synthesis-grade judgment (which RT60 value is "the guidebook chosen value," the
             actual best_practice_synthesis content) is being built on sources that skipped
             the evidence-collection admission stage entirely. No existing tool would ever
             catch this: `reasoning_doc_citations_audit.py` only reads a table that is empty
             for this doc (3b/3c); `validate_reasoning.py` only checks that section/step
             HEADINGS are present (1c), never that citations inside them resolve to admitted
             evidence. **For the mobility batch this is the single highest-value finding**:
             any mobility reasoning doc that cites `source_locators`-only REF-ids as if they
             were Tier 1/Tier 3 evidence will sail through every currently-wired synthesis
             check.

## 4. THE COMPARATIVE ANALYSIS TEST (headline item)

**Question:** do judgments (`specifications`) and syntheses (`best_practice_synthesis` /
`bpc_metadata` / reasoning docs) get compared against each other, and does either revise the
other?

### 4a. Surfaces checked
INVOKED   : reads of `scripts/audit/adjudication_integrity.py` (run below), `scripts/db.py`
             (add-supersession-check — run below), `skills/supersession-audit_SKILL.md`,
             `skills/connection-auditor_SKILL.md`, `skills/item-consolidation-analyzer_SKILL.md`,
             `skills/audit-consolidator_SKILL.md` (+ `scripts/audit_consolidator.py --help`),
             `skills/cross-population-conflict-mapper_SKILL.md`, `v_divergence` view def
             (sqlite_master), `supersession_check` table def + row count,
             `specifications`/`convergence_assessment`/`bpc_metadata` row counts,
             `conflicts` table def + row count, grep for `derivation_sha`/`propagat`/`stale`
STAGE     : synthesis (cross-referenced against judgment)
EXIT      : n/a (research pass)
READS     : see individual sub-items below
WRITES    : one real `supersession_check` row on the scratch DB (see 4e)
EXAMINED  : 4 skills, 3 scripts, 1 view, 4 table schemas, ~20 grep hits
FINDING   : mixed — see Q1/Q2/Q3 verdicts below
LOCATION  : see below

### 4b. `v_divergence` — the closest DB object to "compare judgment against synthesis"
INVOKED   : (read) `scripts/migrations/057_baseline_2026-08-12.sql` (CREATE VIEW v_divergence)
STAGE     : judgment/synthesis boundary
EXIT      : n/a
READS     : sqlite_master (view definition)
WRITES    : NONE
EXAMINED  : 1 view definition
OUTPUT    : `CREATE VIEW v_divergence AS SELECT ecs.*, ca.status AS convergence_status, ...
             FROM "specifications" ecs JOIN convergence_assessment ca ON ca.convergence_id =
             ecs.convergence_id WHERE ca.status = 'divergent';`
FINDING   : This view compares Tier1/Co-1 convergence WITHIN one `specifications` cell (a
             property of the judgment itself, stored via `convergence_assessment`), NOT a
             comparison between a `specifications` row and the `best_practice_synthesis` /
             `bpc_metadata` text that cites it. There is no join anywhere from
             `specifications` to `bpc_metadata` (they don't even share a key: specifications
             is keyed item_code×population_code; bpc_metadata is keyed slug×population — the
             only bridge, `item_bpc_links` (item_code, slug), has 0 rows). `specifications`,
             `convergence_assessment`, and `bpc_metadata` are ALL 0 rows on the committed DB,
             so `v_divergence` returns 0 rows unconditionally today regardless of logic.
LOCATION  : scripts/migrations/057_baseline_2026-08-12.sql (v_divergence, ~line 6562);
             item_bpc_links 0 rows (bridge table exists but unpopulated)

### 4c. `specifications.derivation_sha` — a staleness PRIMITIVE that exists but doesn't reach synthesis
INVOKED   : grep `derivation_sha` across scripts/ + governance/; read
             `scripts/generate/pilot_renderings.py:284-298` (sha_stale computation)
STAGE     : judgment → render (NOT judgment → synthesis)
EXIT      : n/a
READS     : scripts/assess/assess_cell.py:419 (writes derivation_sha = sha(item_code,
             population, governing_refs)); scripts/generate/pilot_renderings.py:284-298
             (recomputes the hash from CURRENT governing_refs and flags `sha_stale` if it no
             longer matches the stored value — i.e. detects when a `specifications` row's
             underlying evidence set has changed since the row was written)
WRITES    : NONE (read only)
EXAMINED  : 2 scripts
OUTPUT    : `c["sha_stale"] = hashlib.sha256(payload.encode()).hexdigest() != c["derivation_sha"]`
FINDING   : A real staleness-detection mechanism exists — but it operates entirely within the
             judgment stage's own record (a specifications row vs. its own governing_refs) and
             is consumed at RENDER time (pilot_renderings.py lives in scripts/generate/). It
             never reads or touches `bpc_metadata`, `references/bpc-reasoning/`, or any
             synthesis artifact. It cannot detect "this best_practice_synthesis cited a
             judgment that has since changed" because nothing records WHICH judgment a given
             synthesis cited in the first place (see 4b bridge-table gap).
LOCATION  : scripts/assess/assess_cell.py:419; scripts/generate/pilot_renderings.py:284-298

### 4d. `supersession_check` / supersession-audit skill — evidence staleness, not judgment staleness
INVOKED   : table schema read (already logged in item 1/this section);
             `skills/supersession-audit_SKILL.md` full read (241 lines); grep for
             "specifications"/"propagat"/"stale"/"invalidat" inside it
STAGE     : evidence-collection → synthesis (gates `bpc_metadata.supersession_check_complete`)
EXIT      : n/a
READS     : skills/supersession-audit_SKILL.md:1-241
WRITES    : NONE
EXAMINED  : 1 skill, 1 table schema
OUTPUT    : The skill audits whether a cited ANCHOR SOURCE (a paper/standard) has been
             superseded by newer literature — outcome recorded per (slug, ref_id), gating
             `bpc_metadata.supersession_check_complete`. Grep hits for "specifications" in
             this skill file: ZERO. It never reads or writes the `specifications` table and
             has no concept of a judgment determination being stale — only a CITED SOURCE
             being stale.
FINDING   : Answers a different question than Q3. It is source-level staleness (does a newer
             paper exist), not judgment-level staleness (has the determination changed).
LOCATION  : skills/supersession-audit_SKILL.md (whole file); supersession_check table
             (scripts/migrations/057_baseline_2026-08-12.sql)

### 4e. `db.py add-supersession-check` — refusal + success on scratch (mechanical exercise)
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s4-synthesis.db python3 scripts/db.py
             add-supersession-check --slug threshold-and-level-access --local-ref L-999
             --ref REF-99999 --tier 1 --evidence-type clinical --outcome current_best
             --search-strategy '{"tool":"pubmed","query":"test"}' --check-method
             pubmed_search --session session_2026-08-25-s4-smoketest` (FK refusal, REF-99999
             does not exist), then the same with `--ref REF-00325 --local-ref L-001`
             (real admitted anchor)
STAGE     : evidence-collection/synthesis boundary
EXIT      : refusal=1 (uncaught IntegrityError traceback), success=0
READS     : evidence_sources FK check (scratch)
WRITES    : refusal: NONE (transaction rolled back). Success:
             supersession_check row @ check_id='SUPCHK-1006421e7c00',
             slug='threshold-and-level-access', ref_id='REF-00325', outcome='current_best'
             (scratch DB only)
EXAMINED  : 1 write attempt each
OUTPUT    : refusal: `sqlite3.IntegrityError: FOREIGN KEY constraint failed`;
             success: `{"check_id": "SUPCHK-1006421e7c00", "dry_run": false}`
FINDING   : PASS (the FK refusal fires correctly), but again a raw traceback rather than a
             clean CLI error message — consistent with the pattern in 2h.
LOCATION  : scripts/db.py:2095 (add_supersession_check, FK-backed conn.execute)
NOTE      : Confirms the writer works and refuses correctly for THIS table — but this table
             answers evidence-staleness, not judgment-vs-synthesis comparison (see 4d).

### 4f. `connections`/connection-auditor — the closest thing to Q1, and it is agent-judgment, not machine
INVOKED   : full read `skills/connection-auditor_SKILL.md` (206 lines); grep for `.py`/script
             references inside it
STAGE     : synthesis (connections feed judgment/render)
EXIT      : n/a
READS     : skills/connection-auditor_SKILL.md:1-206 (esp. lines 120-148: action codes
             VERIFIED/PARTIAL/MISSING/CONTRADICTED)
WRITES    : NONE
EXAMINED  : 1 skill file
OUTPUT    : The skill's own instructions: "fetch the current item specification from GitHub
             via GraphQL and read it in full" then manually verify "No contradictions between
             the connection description and the spec text" and assign action code
             `CONTRADICTED` if the spec (RENDERED text on GitHub, not the `specifications` DB
             table) contradicts a CONSUMED connection. Grep for `.py`/script invocations in
             the file returns ONLY `scripts/db.py connections` / `update-connection` /
             `add-gap` query calls — no comparison script exists. The comparison step itself
             ("read it in full", "verify... no contradictions") is written as agent
             instructions, not as code.
FINDING   : ABSENT as a MECHANICAL tool. A comparison WORKFLOW exists (agent-run, manual
             judgment, Sonnet-class per the skill header) but no script performs it, and
             `connections` is 0 rows so it has never actually been exercised end to end.
LOCATION  : skills/connection-auditor_SKILL.md:120-148 (agent-instruction comparison, not
             code); no corresponding .py file exists anywhere in scripts/ or scripts/audit/.

### 4g. `conflicts` / cross-population-conflict-mapper — the closest thing to Q2, and it too is agent-judgment
INVOKED   : `conflicts` table schema + row count (already run); full read
             `skills/cross-population-conflict-mapper_SKILL.md` header (25 lines: purpose,
             model routing, chunk ceiling)
STAGE     : synthesis
EXIT      : n/a
READS     : conflicts table def (scripts/migrations/057_baseline_2026-08-12.sql);
             skills/cross-population-conflict-mapper_SKILL.md:1-25
WRITES    : NONE
EXAMINED  : 1 table (0 rows), 1 skill
OUTPUT    : `conflicts(item_code, domain, pop_a, pop_b, status, resolution, evidence, gap_id,
             source_skill DEFAULT 'cross-population-conflict-mapper', ...)`. Skill model
             routing: "Sonnet-class (retrieval/collation) · Opus-class or above (resolution
             synthesis + best-practice determination)" — this is exactly the mobility
             ramp-gradient-vs-rest-point / corridor-width-vs-DEM-wayfinding shape the task
             names, but it is filed by an AGENT running research and judgment, never computed
             by comparing two stored `best_practice_synthesis` records against each other.
             There is no script that, e.g., diffs bpc_metadata rows or reasoning docs across
             slugs/items looking for opposing chosen values.
FINDING   : ABSENT as a MECHANICAL tool; PRESENT as an agent-mediated skill + a table to
             record the outcome, currently unexercised (0 rows).
LOCATION  : skills/cross-population-conflict-mapper_SKILL.md (agent workflow only);
             `conflicts` table 0 rows (scripts/migrations/057_baseline_2026-08-12.sql)

### ── VERDICTS: the three comparative-analysis questions ──

**Q1 — Does anything compare a `specifications` determination against the
`best_practice_synthesis` that cites it, and flag disagreement?**
FINDING: **ABSENT.** Nearest surface: `v_divergence` (4b) — compares within-cell Tier1/Co-1
convergence, not judgment-vs-synthesis. `connection-auditor` (4f) compares a connection
against RENDERED spec text, not against the `specifications` DB table or a
`best_practice_synthesis`, and is an agent-judgment workflow, not code. No join even EXISTS
between `specifications` (keyed item_code×population) and `bpc_metadata` (keyed
slug×population) with live data — the bridge (`item_bpc_links`) is 0 rows. **What would have
to be built:** (1) populate `item_bpc_links`; (2) a script that, for each populated
`bpc_metadata`/reasoning-doc row, resolves its item(s) via `item_bpc_links`, pulls the
corresponding `specifications` row(s), and diffs the synthesis's stated chosen value against
the judgment's `value_min`/`value_max`/`state`; (3) a registry entry with a `basis:` pointing
at a pipeline-contract criterion (none currently names this). **Unenforced stage boundary:
judgment ↔ synthesis.**

**Q2 — Does anything compare two syntheses across slugs/items for contradiction (e.g. corridor
width for wheeled mobility vs. ambulant/DEM wayfinding)?**
FINDING: **ABSENT** as a mechanical tool. `cross-population-conflict-mapper` (4g) is the
designed answer to exactly this shape of question, and `conflicts` is its storage table — but
the skill is Sonnet/Opus agent research-and-judgment, invoked per-run on ≤3 conflict domains,
never machine-computed by comparing stored synthesis records. **What would have to be built:**
a script that walks all populated `bpc_metadata`/reasoning docs sharing an `item_code` (via
`item_bpc_links`) or a `domain`, extracts each synthesis's chosen value per population, and
flags pairs whose direction/value profile is not already recorded in `conflicts`. **Unenforced
stage boundary: synthesis ↔ synthesis (cross-slug).**

**Q3 — Does anything propagate a *changed* judgment back into a synthesis that already cited
it (staleness/supersession of a synthesis)?**
FINDING: **ABSENT.** The repository HAS a staleness primitive (`specifications.derivation_sha`,
4c) and it correctly detects when a judgment's own governing evidence has changed — but it is
consumed only at render time and never reaches `bpc_metadata` or the reasoning docs, because no
stored pointer exists from a synthesis record to the judgment(s) it drew on. `supersession_check`
(4d/4e) is the closest NAMED mechanism but audits source staleness (is a paper superseded), not
judgment staleness (has the determination changed), and writes only to
`bpc_metadata.supersession_check_complete`, a boolean gate, not a "your synthesis is now stale"
signal. **What would have to be built:** (1) a `bpc_metadata`/reasoning-doc column recording
which `specifications.derivation_sha` values it was authored against (a synthesis-side pointer,
the mirror of what `specifications` already does for its own evidence); (2) a check that
recomputes each cited judgment's current `derivation_sha` and flags the synthesis
`bpc_complete` state as stale if any diverge — the same pattern `pilot_renderings.py` already
uses for judgment-vs-evidence, just one hop further downstream. **Unenforced stage boundary:
judgment → synthesis (supersession propagation).**

**Net: all three comparative-analysis questions are ABSENT as mechanical capabilities.** Where
something exists, it is either (a) scoped one stage narrower than the question asks (within-cell
convergence, not cross-stage comparison), or (b) an agent-run skill requiring a human/Sonnet/Opus
session to manually read and judge, with no code performing the comparison and no registry entry
tying it to a pipeline-contract criterion. For the mobility batch this means: **two independently
synthesised mobility slugs (e.g. a ramp-gradient BPC and a corridor-width BPC) can reach directly
opposing conclusions about the same shared-space interaction and nothing will ever surface it
unless an agent happens to run cross-population-conflict-mapper and happens to look.**

## 5. Cross-slug findings and connections

### 5a. Real mobility connection — refusals provoked, then a clean write
INVOKED   : sequence of `python3 scripts/db.py add-connection ...` /
             `update-connection ...` / `delete-connection ...` calls against
             `$SMOKE/s4-synthesis.db`, targeting `item:E-03` (Ramp Gradient, ≤1:20,
             MS-fatigue-driven) and `item:E-10` (Rest Seating at Regular Intervals on All
             Accessible Routes) — a real energy-limiting-condition interaction per the
             protocol's example.
STAGE     : synthesis
EXIT      : mixed, see individual attempts below
READS     : items.item_code (E-03, E-10 confirmed to exist and be `active`); connections /
             connection_targets schema (CHECK constraints)
WRITES    : connections/connection_targets rows on scratch DB (CON-0001 bad-target row,
             CON-0002 clean row) — enumerated below
EXAMINED  : 2 items, 7 write attempts
FINDING   : see sub-rows
LOCATION  : scripts/db.py (add-connection/update-connection/delete-connection handlers)

| # | Attempt | Result | Note |
|---|---|---|---|
| R1 | `--confidence VERY-HIGH` (not in enum) | argparse rejects, EXIT 2, no DB touch | Clean refusal — caught before the DB layer. `db.py:1039` region, `choices=["HIGH","MODERATE","SPECULATIVE"]` |
| R2 | `--connection-type ENERGY-INTERACTION` (not in `CROSS-POPULATION/CROSS-ITEM/COMPOUND-INTERACTION/METHODOLOGY`) | `sqlite3.IntegrityError: CHECK constraint failed`, EXIT 1, raw traceback | Refuses correctly but via uncaught exception, not a clean CLI message — same pattern as 2h/4e |
| R3 | `--targets '["item:E-03","item:Z-99"]'` — Z-99 does not exist in `items` | **SUCCEEDED, EXIT 0** — CON-0001 written with `('CON-0001','item:Z-99')` in `connection_targets` | **REAL GAP**: `connection_targets.target` (scripts/migrations/057_baseline_2026-08-12.sql — CREATE TABLE connection_targets) is bare `TEXT NOT NULL`, no FK to `items.item_code`, no format check. A connection can permanently cite a phantom item and nothing refuses it. |
| R4 | `--con-id CON-0001` again (duplicate PK) | `sqlite3.IntegrityError: UNIQUE constraint failed: connections.con_id`, EXIT 1 | Clean refusal (again via traceback) |
| — | Clean write: CON-0002, targets `["item:E-03","item:E-10"]`, description names the MS-fatigue/energy-limiting mechanism | EXIT 0, `{"con_id": "CON-0002", "dry_run": false}` | Verified via read-only query: row present with both targets, status=PENDING |
| R5 | `update-connection --con-id CON-0002 --status APPROVED` (not in `PENDING/CONSUMED/CONSUMED-DEFERRED/CLOSED`) | `sqlite3.IntegrityError: CHECK constraint failed`, EXIT 1, raw traceback | Refuses correctly; note `update-connection`'s argparse has NO `choices=` on `--status` (unlike add-connection's confidence) — the CHECK constraint is the only backstop, and it fires late (post-string-formatting) |
| — | `update-connection --con-id CON-0002 --status CONSUMED` | EXIT 0 | Verified: `('CON-0002', 'CONSUMED', 0)` — status changed, `opus_reviewed` stayed 0 |
| R6 | `delete-connection --con-id CON-9999` (id that never existed) | **SUCCEEDED, EXIT 0** — `{"deleted": "CON-9999", "dry_run": false}` | **REAL GAP**: no existence check or rowcount verification before reporting success; a typo'd con_id in a delete call silently no-ops while reporting success |

### 5b. What reads `connections` downstream — reaches render unfiltered
INVOKED   : `grep -rn "FROM connections" scripts/ tools/` then read
             `scripts/generate_parts.py:245-267` (`build_part05`)
STAGE     : synthesis → render
EXIT      : n/a (code read)
READS     : scripts/generate_parts.py:245-267
WRITES    : NONE
EXAMINED  : 1 render function
OUTPUT    : |
  rows = conn.execute("SELECT con_id, connection_type, status, description FROM
  connections ORDER BY con_id").fetchall()
  applied = [r for r in rows if r[2] in ("CONSUMED", "CONSUMED-DEFERRED", "CLOSED")]
  ...
  md.append("## Applied connections\n")
  md.append(f"{len(applied)} connections have been consumed into item specs or
  deferred; full provenance renders with the specification detail in Part 4...")
FINDING   : **FAIL — an unreviewed connection CAN reach render.** `build_part05` (the
             function that generates Part 5 "Building-Level Co-Occurrence Resolution" of the
             actual book) selects on `status` alone. It applies NO filter on `opus_reviewed`
             — the field intended to record that Opus signed off on the connection before it
             counts as applied. Combined with 5c below (opus_reviewed can never be set to 1
             through the live write path), this means: **any connection an agent files with
             `add-connection` (opus_reviewed hardcoded 0) and then advances to CONSUMED with
             `update-connection` is IMMEDIATELY render-eligible** — CON-0002, written above by
             THIS smoke test with no Opus review of any kind, would render into Part 5 as an
             "applied" connection if this were the live DB.
LOCATION  : scripts/generate_parts.py:250-266 (build_part05); no `opus_reviewed` filter
             anywhere in the function or file (confirmed by grep, see 5c)

### 5c. `opus_reviewed` is dead — never settable, never read as a gate, anywhere in live code
INVOKED   : `grep -rn "opus_reviewed" --include="*.py" .` (repo-wide, including `_archived/`)
STAGE     : synthesis
EXIT      : n/a
READS     : all .py files, sqlite_master (connections schema, `opus_reviewed INTEGER NOT NULL
             DEFAULT 0`), schemas/connection.py (Pydantic model, `opus_reviewed: bool = False`)
WRITES    : NONE
EXAMINED  : whole-repo grep, 11 hits
OUTPUT    : Live hits: `scripts/db.py:1374` (`"opus_reviewed": 0` — hardcoded, add-connection
             has no flag to override it and `update-connection` cannot touch it either);
             `schemas/connection.py:35` (Pydantic default, unused as a gate);
             `scripts/audit/validate_pydantic_schemas.py:132` (a comment listing it, not code
             that reads its value). ALL other hits are in `_archived/scripts/convert/` and
             `_archived/scripts/migrate/` — one-time historical migration scripts, not live.
FINDING   : **ABSENT as a functioning control.** The column exists in the schema and the
             Pydantic model, giving the appearance that Opus review of a connection is
             tracked and gated — it is neither. Nothing in live code can ever write 1 to it,
             and nothing in live code (including the render path in 5b) ever reads it to
             decide anything.
LOCATION  : scripts/migrations/057_baseline_2026-08-12.sql (connections.opus_reviewed column
             definition, ~line 143); scripts/db.py:1374 (hardcoded write); no reader anywhere
NOTE      : **For the mobility batch: connection review is unenforced end to end.** A ramp
             gradient ↔ rest-seating connection (or any other mobility cross-item finding)
             can be filed, marked CONSUMED, and rendered into the actual book with zero
             record of any human or Opus-tier review ever having occurred — the schema field
             that was clearly designed to prevent exactly that is inert.

## 6. Weighting

### 6a. Read `weighting_profile` (5 rows) — what it actually is
INVOKED   : `SELECT * FROM weighting_profile` on committed DB, read-only
STAGE     : substrate → render (see 6b for why not synthesis)
EXIT      : n/a
READS     : weighting_profile (5 rows)
WRITES    : NONE
EXAMINED  : 5 rows
OUTPUT    : |
  designer / decision-frame        → foreground T1, CO1, conflict_notes, code_refs; delta=show
  disabled_person / representation-checking → foreground CO1, variability, co1_limit
  disabled_person / advocacy-brief → foreground delta, rights, evidence_strength, gaps
  policymaker / jurisdiction-comparison → foreground T4/T5/T6, delta, anti_laundering;
                                            delta=floor-vs-anchor
  ot / specialist-handoff          → foreground T1, ranges, person_mode_handoff; delta=clinical
FINDING   : PASS (table read successfully; schema is `PRIMARY KEY(audience, use_pattern)`,
             `tier_weights` a CHECK(json_valid) JSON blob)
LOCATION  : weighting_profile table (scripts/migrations/057_baseline_2026-08-12.sql:705)

### 6b. How a weighting profile enters synthesis — it does NOT; it's a render-stage concern
INVOKED   : grep `weighting_profile` across scripts/tools/governance (repo-wide); read
             `governance/evidence-architecture.md:166,170` (§I1/emphasis re-ranking)
STAGE     : render (not synthesis)
EXIT      : n/a
READS     : governance/evidence-architecture.md:166 ("Emphasis re-ranking (the
             `weighting_profile` mechanism...) chooses **which cells and columns are
             foregrounded** per audience; it can never move a rendering to a different row of
             this map."), :170 ("I1 — Tuple identity. Every rendering of a cell, in every
             register, carries the identical determination tuple. Different words, same
             facts.")
WRITES    : NONE
EXAMINED  : governance doctrine text (authoritative on this question) + grep confirming no
             live script reads `weighting_profile` at all (only `emit_data_migration.py`,
             which merely permits it as a writable table name for migrations, and 4
             governance docs)
OUTPUT    : Doctrine states explicitly and unambiguously that weighting_profile is a
             **presentation-layer foregrounding mechanism**, not a synthesis input. It affects
             which columns of an ALREADY-DETERMINED cell get emphasized per audience/register.
             It cannot change what the determination IS.
FINDING   : ANSWERED BY DOCTRINE, not by code — because no code consumes this table at all
             yet (grep finds zero readers outside the governance prose and the migration
             emitter's table whitelist). `bpc_metadata` has NO column pointing at a
             `weighting_profile` row (confirmed against the schema already read in item 2) —
             consistent with the doctrine, since a synthesis SHOULDN'T record "which profile
             it used" if weighting is purely a render-time reader concern applied after the
             fact, not a synthesis-time input. **This is architecturally sound as designed**
             — the question "does a synthesis record which profile it used" has the answer
             "no, and it shouldn't, because the profile is chosen by the READER's audience at
             render time, not by the AUTHOR at synthesis time." This is the one item-6
             sub-question where the answer is a clean, doctrinally-consistent "not
             applicable" rather than a gap.
LOCATION  : governance/evidence-architecture.md:166,170; bpc_metadata schema (item 2c) has no
             weighting_profile FK/pointer column, consistent with the design

### 6c. Can I1 (register-invariant) be tested with 0 syntheses? — NO, and the checker documents this itself
INVOKED   : `python3 scripts/audit/register_integrity_check.py` (default args — real
             committed DB, `working/pilot/pilot-renderings.html`), then
             `python3 scripts/audit/register_integrity_check.py --selftest` (the invocation
             actually wired into `governance/check-registry.yaml:1384`)
STAGE     : render, cross-checked against judgment (`specifications`)
EXIT      : 0 both times   RUNTIME: <1s each
READS     : working/pilot/pilot-renderings.html (a PILOT artifact — NOT the real book's
             rendered output — containing 15 hand/pilot-authored cells); data/guidebook.db
             (specifications table, read-only, via default `--db` = `GUIDEBOOK_DB_PATH` or
             `data/guidebook.db`)
WRITES    : NONE
EXAMINED  : 15 cells × 6 registers claimed in the PASS message; **0 specifications rows**
             actually available to cross-check against (verified independently — see below)
OUTPUT (plain run): `PASS: I1–I5 hold across 15 cells × 6 registers (DB cross-check on)`
OUTPUT (--selftest): 12 "FIRED" mutation-test lines (I1 tuple divergence, I3 RSO, I4/I5
             inflation, completeness-on-deletion, repr-leak, etc.), then
             `clean pass on untampered document: yes` then the same PASS line.
FINDING   : **VACUOUS, and independently reproduced.** I re-ran the exact `db_rows`
             population logic from `scripts/audit/register_integrity_check.py:140-156`
             directly against the committed DB: `SELECT ... FROM specifications` returns 0
             rows, so `db_rows = {}` — an EMPTY dict, which is Python-falsy. Both guard sites
             that gate the actual cross-check logic (`if db_path:` completeness loop at
             :159-166, and the per-cell `if db_rows:` block at :180-192) test `if db_rows:`
             or operate on the resulting empty structure — so **the DB→doc completeness check
             and the per-cell DB-value cross-check never execute a single comparison** on the
             real invocation. Yet the final print statement emits "(DB cross-check on)" based
             solely on `args.db` being a non-empty PATH STRING, not on whether `db_rows` ended
             up populated — so the message actively implies verification that did not happen.
FINDING   : PASS-BUT-MISLEADING — with an important mitigating fact: **the script's own
             author already documented exactly this vacuity**, verbatim, at
             scripts/audit/register_integrity_check.py:362-366: "specifications is 0 rows in
             the live corpus (pre-launch, unpopulated), so db_rows is always empty and
             set(db_rows) - set(cells) can never be non-empty — this sub-test would pass
             vacuously against the real DB no matter what gets deleted from the document." The
             fix applied is real but PARTIAL: `--selftest` copies the DB to a temp file,
             INJECTS one ghost `specifications` row matching the pilot doc's first cell, and
             mutation-tests that the completeness/cross-check logic correctly fires against
             THAT temp fixture. This proves the CHECKER'S LOGIC is not dead code. It does
             **not** fix the final `check(doc, db_path=args.db)` call in `main()` (the one
             whose PASS/FAIL determines the registry gate's exit code) — that call still runs
             against the real, empty, committed DB and is still vacuous in exactly the way
             the comment describes.
LOCATION  : scripts/audit/register_integrity_check.py:140-156 (db_rows population),
             :159-166 (DB→doc completeness, gated on falsy empty dict),
             :180-192 (per-cell DB cross-check, gated on falsy empty dict),
             :428-429 (misleading "(DB cross-check on)" label keyed to `args.db` truthiness,
             not to whether any row was actually compared),
             :362-366 (the author's own comment proving this is KNOWN, not accidental)
NOTE      : **Answers the item-6 headline question directly: I1 (and I2-I5) CANNOT be
             meaningfully tested against real synthesis output today, because there are 0
             `specifications` rows and 0 `bpc_metadata` rows to test.** The 15-cell PASS is
             entirely a statement about a hand-authored PILOT fixture
             (`working/pilot/pilot-renderings.html`), not the mobility batch's future output,
             and the part of the check that WOULD catch a real cell silently missing from a
             real render (`COMPLETENESS VIOLATION`) is proven-working only in `--selftest`'s
             temp-copy sandbox, never in the real invocation while `specifications` stays
             empty. **For the mobility batch: once real specifications rows exist, re-run
             `register_integrity_check.py` and confirm the printed cell count and "(DB
             cross-check on)" label correspond to actual comparisons — do not trust the label
             at face value until `specifications` is non-empty.** This is a lower-severity
             instance of failure mode (a) than the fully silent ones elsewhere in this log,
             specifically because the author already flagged it in-code — but the flag never
             reached the production code path, only the selftest path.
