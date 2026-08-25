# S6 — SUBSTRATE, HOOKS, GATES AND THE WRITE PATH

Session: session_2026-08-25-pipeline-smoke-test-mobility
Agent: S6
Started: 2026-08-25 18:19 UTC
sha256(data/guidebook.db) BEFORE: 30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf
Scratch DB: $SMOKE/s6-substrate.db (copy of committed DB)

---

## 1. Dependency truth (CLAUDE.md §5 inversion)

### 1a. `.claude/hooks/ensure-deps.sh`
INVOKED   : `bash .claude/hooks/ensure-deps.sh`
STAGE     : substrate
EXIT      : 0   RUNTIME: 0.25s
READS     : `governance/check-registry.yaml` (`batteries:` block, lines 157-177) via inline
            `python3 -c "import yaml; d=yaml.safe_load(...)"`; falls back to literal
            `"pydantic jsonschema"` (script comment: "Fallback only if the registry could
            not be read") only if that parse fails — confirmed no second copy of the dep
            list exists outside this fallback string.
WRITES    : NONE (would `pip install` on a miss; none needed here)
EXAMINED  : 2 deps (union of `batteries:*.deps` = {pydantic, jsonschema}; PyYAML is not a
            declared dep of any battery — it's needed merely to parse the registry itself,
            and is Debian-managed/pre-installed per CLAUDE.md)
OUTPUT    : (silent — no MISSING, so the script's echo branches never fire; confirmed by
            reading the script: `[ -z "$MISSING" ] && exit 0` at line ~54)
FINDING   : PASS
LOCATION  : `.claude/hooks/ensure-deps.sh:36-45` (registry parse + union), `:47` (fallback
            literal, single second-home candidate, correctly gated to parse-failure only)
NOTE      : Confirmed — one home for the dep list (`governance/check-registry.yaml`
            `batteries:*.deps`), read live every session start, no drifted duplicate.
            pydantic 2.13.4, jsonschema 4.26.0 already present in this container (not
            installed by this run).

### 1b. requirements.txt vs registry batteries: block — disagreement audit
INVOKED   : `grep -n "^batteries:" -A 40 governance/check-registry.yaml`; `cat -n requirements.txt`
STAGE     : substrate
EXIT      : n/a (read-only greps)
READS     : `governance/check-registry.yaml:157-177`, `requirements.txt:1-9`
WRITES    : NONE
EXAMINED  : 7 batteries (syntax, structure, data, db_integrity, tests, schema, governance,
            attestation, research, render — 10 rows, `deps:` populated on 4 of them) vs 2
            requirements.txt package lines
FINDING   : FAIL (documents disagree — exactly as CLAUDE.md itself already says, confirmed
            independently)
LOCATION  : Disagreement 1 — `requirements.txt:9` pins `PyYAML==6.0.3`; no battery in
            `governance/check-registry.yaml:157-177` declares `PyYAML`/`yaml` as a `deps:`
            entry anywhere (only `pydantic` at :173-174,176 and `jsonschema` at :175-176 are
            declared). `requirements.txt` names a package the registry's own dependency
            contract never asks for.
            Disagreement 2 — `governance/check-registry.yaml:175` (`attestation`) and `:176`
            (`research`) both declare `jsonschema` as a dep; `requirements.txt:1-9` never
            mentions `jsonschema` at all — it is entirely absent from the second home.
NOTE      : Both disagreements are the ones CLAUDE.md's §5 box already names, confirmed by
            direct inspection with line numbers rather than taken on faith. `requirements.txt`
            is inert in this container (installing from it is explicitly forbidden — PyYAML
            pin conflicts with the Debian-managed 6.0.1) so the drift is latent, not currently
            harmful, but it is a second, disagreeing home for a fact rule 5 says should have one.

### 1c. Blocking/advisory count WITH deps present (`scripts/run_checks.py --all --explain`)
INVOKED   : `python3 scripts/run_checks.py --all --explain`
STAGE     : substrate
EXIT      : 1   RUNTIME: 40.5s
READS     : `governance/check-registry.yaml` (all 63 non-quarantined checks), entire repo
            tree per-check
WRITES    : NONE (checks are read-only in this mode; `render_audit_browser`,
            `test_graph_audit` etc. write only to their own tmp dirs)
EXAMINED  : 63 of 63 registered checks (4 quarantined, never selected — matches header
            "selected 63 of 63 registered checks (4 quarantined, never selected)")
OUTPUT    :
```
PASS: 49   FAIL: 6   NONE(NOTHING-IN-SCOPE): 8
FAILED: validate_pydantic_schemas (advisory), retired_vocabulary (advisory),
        attestation_presence (BLOCKING), validate_reasoning (advisory),
        test_verification_pipeline (advisory), context_map_fresh (advisory)
NOTHING-IN-SCOPE (8): validate_evidence_state, validate_verification_consistency,
  attestation_schema, attestation_verdict, population_integrity_audit, pmp_audit,
  reasoning_doc_citations_audit, check_rendered_docs
  BLOCKING and vacuous (4): validate_evidence_state, validate_verification_consistency,
  attestation_schema, check_rendered_docs
BLOCKING failures (1): attestation_presence
RESULT: FAIL
```
FINDING   : FAIL — but with a load-bearing qualifier (see NOTE)
LOCATION  : `attestation_presence` blocking failure detail (output lines 119-126 of my
            captured run): `CHECK 0: missing attestation for
            sessions/session_2026-08-25-pipeline-smoke-test-mobility.md (expected
            attestations/sessions_session_2026-08-25-pipeline-smoke-test-mobility.json)`
NOTE      : **CLAUDE.md's own table ("with pydantic: 0 blocking, 4 advisory -> PASS, 50
            green", stamped `d6ef7e9`, 2026-08-25) is itself now drifted** — confirmed via
            `git merge-base --is-ancestor d6ef7e9 HEAD` (true) and
            `git rev-list --count d6ef7e9..HEAD` = **36** intervening commits on the same
            calendar day, including the ACT 1–3/2a-2c write-path consolidation. This is
            failure mode (b) from CLAUDE.md §2, caught in the file meant to warn against it.
            Of my 6 FAILs: the 1 BLOCKING one (`attestation_presence`) is a **correct, working
            gate** reacting to this smoke-test session's own untracked
            `sessions/session_2026-08-25-pipeline-smoke-test-mobility.md` (created by the
            session harness before this agent's first Bash call — confirmed present in the
            very first `git status --short` of this run) lacking an attestation — exactly
            what rule §0.2 requires it to catch, not a dependency or repo-health defect. The
            5 advisory FAILs (`validate_pydantic_schemas`, `retired_vocabulary`,
            `validate_reasoning`, `test_verification_pipeline`, `context_map_fresh`) are
            pydantic-present, i.e. **not** the §5-documented dependency-absence failure mode —
            they are ordinary content/freshness drift accumulated across the 36 commits since
            the table was written, and are advisory so do not block. Net: **dependency
            presence claim is confirmed correct** (no blocking failure traces to a missing
            package); the specific 0-blocking/4-advisory figures are stale within the same day.


## 2. THE WRITE PATH, end to end, on the scratch (mobility shape)

Batch: 1 `source_locators` lead (ISO 21542:2021, ref REF-00971) + 1 `jurisdictional_values`
corridor-width code value for E-08 (Corridor Clear Width) in Canada (bucket-1), 920mm minimum
per NBC 2020 3.8.3.3(1).

### 2a. `db.py next-id` does NOT cover ref_id (confirms CLAUDE.md's own correction)
INVOKED   : `python3 scripts/db.py next-id --help`; `python3 scripts/db.py next-id`
STAGE     : substrate
EXIT      : 2 (usage error — missing required `entity`)
READS     : argparse choices `{connections,gaps,terms,conflicts}`
WRITES    : NONE
EXAMINED  : n/a
OUTPUT    : `next-id: error: the following arguments are required: entity` — and even with
            an entity, `ref_id` is not one of the four choices.
FINDING   : ABSENT — confirmed as documented: there is no `next-id ref_id` allocator.
LOCATION  : `scripts/db.py` (next-id subparser choices)
NOTE      : `dbcore.next_ref_id(conn)` is the real allocator (verified next). CLAUDE.md's
            §4 correction ("there is no ref_id allocator... the rule this file gave for
            weeks was WRONG") is accurate and current.

### 2b. `dbcore.next_ref_id` / `check_values` — direct verification
INVOKED   : inline Python importing `scripts.dbcore` against `$SMOKE/s6-substrate.db` (RO)
STAGE     : substrate
EXIT      : 0
READS     : `source_locators.ref_id`, `evidence_sources.ref_id` (dbcore.py:190-203, the
            `_MINTABLE` regex scan unioned across both tables)
WRITES    : NONE
EXAMINED  : union high-water mark across 2 tables
OUTPUT    : `next_ref_id: REF-00971` — one past CLAUDE.md's own measured
            `evidence_sources` top of REF-00970 (§4). Consistent.
            `check_values(jurisdictional_values, jurisdiction)` → `set()` (empty — no CHECK
            on this column; see 2f below, a genuine gap).
            `check_values(source_locators, status)` → `{'PROMOTED','REFERENCE-ONLY','RETIRED'}`
            (from the table's own CHECK, `dbcore.py:272-303`).
FINDING   : PASS
LOCATION  : `scripts/dbcore.py:206-213` (`next_ref_id`), `:272-303` (`check_values`)
NOTE      : Confirms rule 5 in the one place it's supposed to hold: no counter table, no
            hardcoded vocab list, both computed live from the schema/table state.

### 2c. `db.py add-locator` — write to scratch
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s6-substrate.db python3 scripts/db.py add-locator
            --ref-id REF-00971 --title "ISO 21542:2021 ..." --standard-number "ISO 21542:2021"
            --recovered-from smoke-test-s6 --status REFERENCE-ONLY --tier-claimed 4
            --notes "..." --session session_2026-08-25-pipeline-smoke-test-mobility [--dry-run]`
STAGE     : substrate
EXIT      : 0 (dry-run and real)   RUNTIME: <0.3s each
READS     : `source_locators` (existence + DOI-collision check across `source_locators` and
            `evidence_sources`, `scripts/db.py:2503-2521`), `check_vocab` on `status`
WRITES    : dry-run → NONE; real → `source_locators` 1 row, `ref_id='REF-00971'`
            (`scripts/db.py:2489-2531`, `insert_locator`)
EXAMINED  : 1 candidate ref_id checked for prior existence + DOI collision (none — no DOI
            given, so DOI-collision branch skipped)
OUTPUT    : `{"ref_id": "REF-00971", "dry_run": true}` then `{"ref_id": "REF-00971",
            "dry_run": false}`. First attempt failed loudly on `--tier-claimed T4` (wants
            int, not the `T4`-style tier label) — `argparse` usage error, exit 2, before
            touching the DB. Corrected to `--tier-claimed 4`.
FINDING   : PASS
LOCATION  : `scripts/db.py:2489-2531`
NOTE      : Dry-run/real symmetry held (same output shape, `dry_run` flag flipped, no
            partial write on the dry-run path — verified by reading `dbcore.connect`'s
            dry-run branch, which opens `:memory:` and copies schema rather than the real
            file). One real, minor usability trap: `--tier-claimed` takes a bare int
            (1-6), not the `T4`-style label used everywhere else in this codebase's prose
            and in `evidence_sources.tier` display — caught immediately by argparse, not
            silently coerced.

### 2d. `db.py add-jurisdictional-value` — write to scratch
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s6-substrate.db python3 scripts/db.py
            add-jurisdictional-value --item-code E-08 --jurisdiction CA
            --standard-name "NBC 2020 3.8.3.3" --value-numeric 920 --unit mm
            --is-code-minimum 1 --evidence-tier 6 --loc-section 3.8.3.3 --loc-clause "(1)"
            --notes "..." --session session_2026-08-25-pipeline-smoke-test-mobility [--dry-run]`
STAGE     : substrate
EXIT      : 0 (dry-run and real)
READS     : `items.item_code` existence check (`scripts/db.py:2373-2374`); R3 locator-or-
            `[UNVERIFIED-QUANT]` guard (`:2384-2394`); evidence_tier 1-6 range guard
            (`:2375-2382`, explicitly deferring to `emit_data_migration.py`'s RANGE_GUARDS
            as the one home of the band, rule 5 in the writer's own comment)
WRITES    : real → `jurisdictional_values` 1 row, `jv_id=110`
EXAMINED  : 1 item_code existence check (E-08 found active, `scripts/db.py` output
            confirmed by direct SELECT — E-08 = "Corridor Clear Width (≥1200 mm Minimum on
            All Primary Routes)", `status='active'`)
OUTPUT    : `{"jv_id": null, "dry_run": true}` / `{"jv_id": null, "dry_run": false}` —
            `jv_id` is an autoincrement PK not supplied by the caller, correctly returned
            as `None` (the CLI does not read back the assigned rowid; confirmed by direct
            SELECT that row 110 exists with the correct values).
FINDING   : PASS
LOCATION  : `scripts/db.py:2363-2400` (`insert_jurisdictional_value`)
NOTE      : R3 (quantified value needs a locator) worked as intended — I supplied
            `--loc-section`/`--loc-clause` and the write succeeded; omitting both while
            keeping `--value-numeric` would have been refused (not tested destructively
            here to avoid burning the one clean batch, but the guard code at
            `scripts/db.py:2387-2394` is unconditional and reads directly, so this is a
            code-verified rather than empirically-refused PASS on that specific branch).
            **Genuine gap found here, not a success**: unlike `insert_economics_entry`
            (which calls `dbcore.check_vocab` on `pillar` and `entry_type`),
            `insert_jurisdictional_value` never calls `check_vocab` (or any vocabulary
            check at all) on `jurisdiction`. See 2f.

### 2e. `scripts/research/emit_batch_sql.py` — delta capture, and what it does/doesn't see
INVOKED   : `python3 scripts/research/emit_batch_sql.py --scratch $SMOKE/s6-substrate.db
            --canonical data/guidebook.db --out $SMOKE/out/s6-batch.sql`; then two more
            runs on throwaway copies to empirically test UPDATE and DELETE handling.
STAGE     : substrate
EXIT      : 0 (real batch); 0 (UPDATE-of-pre-existing-row test); **1** (DELETE test —
            refuses, by design)
READS     : `PRAGMA user_version` on both DBs (schema-version match gate,
            `scripts/research/emit_batch_sql.py:96-101`); `dbcore.WRITABLE_TABLES` (single
            home for "which tables a session may write", moved into `dbcore.py` 2026-08-25
            per its own header comment — confirmed no second copy in this file); every
            row of every writable table in both DBs, keyed and ordered by the table's own
            declared PRIMARY KEY (`pk_columns`, `:75-77`)
WRITES    : NONE (opens both DBs read-only, `ro()` at `:52-53`)
EXAMINED  : 2 tables with a real delta (`source_locators`, `jurisdictional_values`); full
            `WRITABLE_TABLES` set walked for every run
OUTPUT    : `Wrote .../s6-batch.sql — 2 insert(s), 0 update(s)` for the real batch.
            Empirical UPDATE test (existing canonical row REF-00002's `notes` mutated in
            the scratch copy): correctly emitted
            `UPDATE "source_locators" SET "notes" = '...' WHERE "ref_id" = 'REF-00002';`
            alongside the unrelated insert — column-level diff, not whole-row.
            Empirical DELETE test (existing canonical row REF-00001 removed from the
            scratch copy): **refused entirely**, exit 1:
            `ERROR: 1 row(s) exist in the canonical DB but not in the scratch. The batch
            path is additive — this means the scratch was copied from a different base, or
            rows were deleted. Refusing to emit.` — printed the offending key
            (`source_locators: ('REF-00001',)`) to stderr, capped at 10.
FINDING   : PASS (both by design and empirically)
LOCATION  : `scripts/research/emit_batch_sql.py:92-152` (`emit`); `:130` (insert branch),
            `:137-144` (update branch, column-level diff via `changed = [c for c in cols
            if row[c] != c_rows[key][c]]`), `:146-150` (missing-row refusal — DELETEs are
            never rendered as SQL, the tool exits nonzero instead)
NOTE      : **Exactly matches CLAUDE.md's design description.** It DOES see UPDATEs (full
            column-level diff against canonical, keyed by PK) — this is not documented
            explicitly in CLAUDE.md's write-path prose and is worth stating plainly: a
            batch that both adds new rows AND edits pre-existing ones in the same scratch
            session is captured correctly in one pass. It does NOT see DELETEs as deletes —
            any row present in canonical but missing from the scratch aborts the entire
            emission with no partial output, by design ("research batch adds evidence... a
            mistake to surface, not to replay" — the tool's own docstring, lines 16-18).
            For a mobility batch this means: never delete a row in the scratch to "undo" a
            mistake — the emitter will refuse the whole batch. Correct forward-fix is to
            leave the row and compensate (matches CLAUDE.md rule 3's forward-only doctrine).

### 2f. GENUINE GAP — `jurisdictional_values.jurisdiction` has no enforced vocabulary anywhere
INVOKED   : `dbcore.check_values(conn,'jurisdictional_values','jurisdiction')` → `set()`;
            `dbcore.live_vocab(...)` → `{'CH','SG','GB','AU','US','JP','DE','FR','CA','ISO','NO','EU'}`;
            read of `scripts/db.py:2363-2400` (no `check_vocab` call on `jurisdiction`);
            read + run of `scripts/validate_jurisdiction.py`
STAGE     : substrate
EXIT      : 0 for `validate_jurisdiction.py` (PASS: 0 errors, 55 warnings, EXAMINED: 111)
READS     : `references/standards-registry.md` (111 YAML blocks), `data/sources/*.yaml`
            jurisdiction fields (`validate_source_jurisdictions`, lines 157-189) — **not**
            `jurisdictional_values` at all; confirmed via `grep -rln jurisdictional_values
            scripts tools` (no hit in `validate_jurisdiction.py`)
WRITES    : NONE
EXAMINED  : 111 registry blocks + N `data/sources/*.yaml` files. `jurisdictional_values`
            table rows: 0 (not this check's scope)
OUTPUT    : `validate_jurisdiction.py`'s own docstring: "GB rejected (must be UK)", and its
            code (`:180-183`) does exactly that — **for `data/sources/*.yaml` files only**.
            The live `jurisdictional_values` table already holds a `'GB'` row
            (`live_vocab` above) that this exact rule would reject if it were checked —
            and nothing checks it: not a table CHECK constraint (table DDL has no CHECK on
            `jurisdiction`), not the CLI writer (`insert_jurisdictional_value` never calls
            `dbcore.check_vocab` on this column, unlike `insert_economics_entry` which does
            call it on `pillar`/`entry_type`), not `validate_jurisdiction.py` (scoped to
            the markdown registry and `data/sources/*.yaml`, not the DB table).
FINDING   : FAIL (a real, unenforced dual-standard: "GB rejected" is doctrine but is
            structurally unreachable for this specific table)
LOCATION  : `governance/check-registry.yaml` — no check maps to
            `jurisdictional_values.jurisdiction`; `scripts/db.py:2363-2400` (writer, no
            vocab call); `scripts/validate_jurisdiction.py:157-189` (scope excludes this
            table); live data — `jurisdictional_values` rows with `jurisdiction='GB'`
            (confirmed present via `live_vocab`, exact row keys not extracted since this is
            a substrate-level finding, not evidence work)
NOTE      : **Blocker for the mobility batch.** Bucket 1 includes "UK" by name
            (`PROTOCOL.md`), and this table already contains a `GB` value that the
            project's own documented rule says must be `UK`. A batch writer typing `--
            jurisdiction GB` for a UK corridor-width value would succeed silently — no
            refusal, no warning, and no existing gate would ever catch it, because the one
            script that enforces "GB → UK" never looks at this table. This is a genuine
            "add the check" case under CLAUDE.md §1 ("nothing is added without naming what
            reads it" — inverted here: something already reads a rule that doesn't reach
            this table). Fix: either add a `dbcore.check_vocab` call in
            `insert_jurisdictional_value` sourced from `schemas.enums.JurisdictionCode`
            (rule-5-compliant: point at the existing enum, don't hardcode a new list), or
            extend `validate_jurisdiction.py` to scan the table.

### 2g. `scripts/emit_data_migration.py` — the session-id trap, tested both forms
INVOKED   : Ran twice with identical `--input`/`--summary`, differing only in `--session`:
            bare stem `session_2026-08-25-pipeline-smoke-test-mobility` vs `.md`-suffixed
            `session_2026-08-25-pipeline-smoke-test-mobility.md`
STAGE     : substrate
EXIT      : 0, both forms
READS     : `--input` SQL file; own `slugify_session()` (`scripts/emit_data_migration.py:664-673`)
WRITES    : one `.sql` file per run, into a scratch `--output-dir` (never
            `scripts/migrations/` — see cleanup below)
EXAMINED  : 2 forms of the same session id
OUTPUT    : Filenames: `data_20260825182449_2026-08-25-pipeline-smoke-test-mobility.sql`
            (bare) vs `data_20260825182450_2026-08-25-pipeline-smoke-test-mobility.sql`
            (`.md`) — **identical slug**, timestamp-only difference (1 second apart, real
            clock). Header line differs cosmetically:
            bare  → `-- Session:    session_2026-08-25-pipeline-smoke-test-mobility`
            `.md` → `-- Session:    session_2026-08-25-pipeline-smoke-test-mobility.md`
FINDING   : PASS, with a correction to the trap as CLAUDE.md frames it for THIS tool
            specifically
LOCATION  : `scripts/emit_data_migration.py:664-673` (`slugify_session` — strips a
            trailing `.md` AND a leading `session_` before slugifying, so both forms
            collapse to the same slug); `:770` (raw, un-normalized `args.session` echoed
            into the `-- Session:` comment header)
NOTE      : **Neither form fails loudly OR silently in a way that matters here** — both
            are accepted, and the file that ends up on disk (the part that matters:
            filename, and therefore migration_id) is identical either way. The only
            difference is cosmetic, in a comment line. I searched for a downstream
            consumer of that `-- Session:` comment (`grep -rn '"-- Session:'` and `grep -rn
            'Session:' scripts/`) and found none outside `emit_data_migration.py` itself —
            it is written for a human reader, not parsed by any check. **The trap CLAUDE.md
            warns about is real elsewhere** (§7: "session ids: bare stem in the DB, `.md`
            in pointers... getting it wrong scopes a gate to nothing and it passes green")
            — but it does not live in `emit_data_migration.py --session`, contrary to the
            task instructions' framing. It lives in `db.py`'s `stamp_for`/`created_by_session`
            column (bare stem, confirmed 2c/2d wrote `session_2026-08-25-pipeline-smoke-
            test-mobility` with no `.md`) versus `sessions/LATEST`/`LATEST-RESEARCH` (`.md`
            suffix, confirmed in §6 below) — two DIFFERENT tools that must agree with each
            other's convention, not one tool that silently mis-parses its own flag.

### 2h. `scripts/migrate_db.py` — apply to a throwaway, then standard `--rebuild` reproducibility
INVOKED   : (i) `GUIDEBOOK_DB_PATH=$SMOKE/migtest/throwaway.db
            GUIDEBOOK_MIGRATIONS_DIR=$SMOKE/migtest/migrations python3 scripts/migrate_db.py
            --dry-run --session ...` then the same without `--dry-run`, against a throwaway
            copy of `data/guidebook.db` plus a private copy of `scripts/migrations/` with my
            one new file added; (ii) the standard, generic reproducibility check:
            `python3 scripts/migrate_db.py --rebuild $SMOKE/out/rebuilt.db` against the REAL
            `scripts/migrations/` (no smoke content) and `python3
            scripts/audit/migration_reproducibility.py [--deep]`
STAGE     : substrate
EXIT      : 0 throughout
READS     : (i) `GUIDEBOOK_MIGRATIONS_DIR` (env-overridable — confirmed at
            `scripts/migrate_db.py:42-44`, no hardcoded path), the throwaway DB's current
            `schema_version` and `data_migrations` table (to compute pending); (ii)
            `scripts/migrations/*.sql` (8 schema + 32 data migrations applied, per rebuild
            output), `data/guidebook.db` (read-only, comparison target)
WRITES    : (i) throwaway.db only — never `data/guidebook.db`, confirmed by sha256 before
            and after (unchanged, see below); (ii) `$SMOKE/out/rebuilt.db` only
EXAMINED  : (i) 1 pending migration detected and applied, in a private migrations dir seen
            by nothing else; (ii) `migration_reproducibility.py` --deep: **66** tables
            walked row-for-row (`EXAMINED: 66`), non-deep mode: **7** core invariant counts
OUTPUT    :
            (i) dry-run: `Applying data_20260825182449_...sql... [DRY-RUN] Schema at
            version 64; 1 data migration(s) applied.` Real run: same minus `[DRY-RUN]`,
            confirmed by direct SELECT the new locator (REF-00971), the new
            jurisdictional_values row (jv_id=110, E-08/CA/920mm), and a
            `data_migrations` row (`applied_by_session='session_2026-08-25-pipeline-smoke-
            test-mobility'`, bare stem — matches what I passed) all landed in the
            throwaway.
            (ii) my own raw `sha256sum` of a plain `--rebuild` vs `data/guidebook.db`
            **differed** (`61171f0e...` vs `30a10669...`) — SQLite files are not
            byte-stable across independent builds even with identical logical content
            (page/freelist layout). The PROJECT'S OWN check is content-level, not
            byte-level, and is the one that matters:
            `migration_reproducibility.py` (non-deep): `PASS`, `schema_version`,
            `evidence_sources`, `citation_mining`, `source_slug_links`, `gaps`,
            `connections`, `items` all `committed==rebuilt`, `EXAMINED: 7`.
            `migration_reproducibility.py --deep`: `PASS`, "(64 tables identical, not
            listed)", 2 tables correctly reported `EXEMPT` (`evidence_source_authors`,
            `pipeline_runs` — job-owned per DR-2026-05-28, `scripts/audit/
            migration_reproducibility.py:65`), `EXAMINED: 66`.
FINDING   : PASS
LOCATION  : `scripts/migrate_db.py:42-44` (env-var path resolution, confirms no hardcoded
            `data/guidebook.db` write target when overridden), `scripts/audit/
            migration_reproducibility.py:65` (EXEMPT_TABLES, the one documented, correct
            exception to full reproducibility)
NOTE      : **The write path holds end to end on a genuinely mobility-shaped batch.**
            Important methodological note for future smoke runs: a raw `sha256sum` diff
            against a `--rebuild` output is NOT the right reproducibility test for this
            project (SQLite files legitimately differ byte-for-byte on unrelated rebuilds)
            — always defer to `scripts/audit/migration_reproducibility.py`, which is
            content-aware and already excludes the two job-owned tables. Confirms
            `data/guidebook.db` was never touched by any of this (see cleanup below).

### 2i. Cleanup
Deleted all emitted migration files from scratch (they were never written into the tracked
`scripts/migrations/` directory — confirmed via `git status --short scripts/migrations/`,
clean throughout):
  - `$SMOKE/out/migrations_bare/data_20260825182449_2026-08-25-pipeline-smoke-test-mobility.sql`
  - `$SMOKE/out/migrations_md/data_20260825182450_2026-08-25-pipeline-smoke-test-mobility.sql`
  - `$SMOKE/migtest/migrations/data_20260825182449_2026-08-25-pipeline-smoke-test-mobility.sql`
All three removed with `rm -f`; confirmed empty by a follow-up `find`.

**sha256(data/guidebook.db) mid-run: `30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf`
— unchanged from the run's start.**


## 3. `scripts/run_checks.py` — the full battery

### 3a. `--list`
INVOKED   : `python3 scripts/run_checks.py --list`
STAGE     : substrate
EXIT      : 0
READS     : `governance/check-registry.yaml` (whole `checks:` + `quarantine:` list)
WRITES    : NONE
EXAMINED  : 63 active + 4 quarantined = 67 registered checks
OUTPUT    : table of id/battery/level/kinds for all 63, plus a "QUARANTINED (registered,
            never selected)" section listing 4: `validate_db` (retired 2026-08-15),
            `adjudication_integrity`, `code_currency_audit`, `pre_rehab_banner_audit`
FINDING   : PASS
LOCATION  : `governance/check-registry.yaml`
NOTE      : Matches the header line from every run ("63 of 63 registered... 4
            quarantined, never selected").

### 3b. `--selftest`
INVOKED   : `python3 scripts/run_checks.py --selftest`
STAGE     : substrate
EXIT      : 0   RUNTIME: 0.69s
READS     : the registry's own structure (ids, kinds, batteries, bases) plus a fixed set
            of C4/C5/C6 fixture paths compiled into the selftest itself
WRITES    : NONE
EXAMINED  : registry coherence — 8 groups of assertions (C1-C8), ~46 individual checks
OUTPUT    : `SELFTEST: PASS — registry coherent, classifier and selector behave as
            documented.` Two informational notes worth keeping: "contract criteria with
            no check claiming them: 5 of 19" (`cross_stage/attestation-doctrine-binding`,
            `evidence-collection/discovery-provenance`, `judgment/convergence-independence`,
            `judgment/derivation-handshake`, `synthesis/opus-routing` — all §7 pipeline-
            contract coverage gaps, corroborated independently in §7 below) and "checks
            with a real floor: 32 of 63" / "no stated authority: 30 of 63".
FINDING   : PASS
LOCATION  : `scripts/run_checks.py` (selftest body, C1-C8)
NOTE      : **C7 "every contract basis resolves to a real criterion" PASSED** — confirms
            the 2026-08-25 stage-id rename to `evidence-collection` left no dangling old
            name. Cross-checked independently with `grep -n "basis:"
            governance/check-registry.yaml`: every `basis:` value uses current stage ids
            (`judgment/...`, `evidence-collection/evidence-verification-gate`,
            `research/...`, `synthesis/...`, `render/...`, `cross_stage/...`) — no
            occurrence of an old/retired stage spelling anywhere in the file.

### 3c. `--changed-from origin/main --explain` does NOT run the selftest — verified in code AND behaviourally
INVOKED   : `python3 scripts/run_checks.py --changed-from origin/main --explain`
STAGE     : substrate
EXIT      : 0   RUNTIME: 11.6s
READS     : `git diff --name-only origin/main...HEAD` (+ working-tree changes — 11 changed
            files at run time), `governance/check-registry.yaml` kinds classification
WRITES    : NONE
EXAMINED  : 27 of 63 checks selected (kind = synthesis, matched against changed paths
            `sessions/LATEST`, `sessions/session_2026-08-25-pipeline-smoke-test-mobility.md`
            — everything else classified `(unclassified)`, mostly this smoke-test's own
            scratchpad tree)
OUTPUT    : `RESULT: PASS — 18 check(s) green, 7 nothing-in-scope, 2 advisory failure(s)`.
            NOTHING-IN-SCOPE (7): validate_evidence_state, attestation_presence,
            attestation_schema, attestation_verdict, pmp_audit,
            reasoning_doc_citations_audit, check_rendered_docs — 4 of these BLOCKING and
            vacuous. NON-BLOCKING failures (2): retired_vocabulary (66 occurrences,
            EXAMINED: 26 files), validate_reasoning (EXAMINED: 3, missing required
            sections in a template-derived reasoning doc).
FINDING   : PASS (code claim verified both by reading and by behaviour)
LOCATION  : Code proof — `scripts/run_checks.py:395-396` (`if args.selftest: return
            selftest(reg)` — an early, unconditional return) is a wholly separate branch
            from the `--changed-from` handling at `:432-434` (`elif args.changed_from:
            paths = changed_paths(...)`). Passing `--changed-from` without `--selftest`
            never touches the `selftest()` function; there is no code path from one into
            the other in either direction.
NOTE      : **Live corroboration of exactly the failure mode CLAUDE.md's §5 box describes**
            (a rename passing `--changed-from` green while `--selftest`/CI's *Classify
            change* job would have caught a stale reference) — except here there is
            nothing stale to catch (3b confirmed C7 clean), so this run demonstrates the
            MECHANISM (the two paths really are disjoint) without reproducing the historical
            bug. Anyone relying on `--changed-from --explain` alone, as this smoke test's
            own local iteration loop did before this section, would never see a registry
            self-consistency regression — `--selftest` must be run separately after any
            rename, exactly as instructed.

### 3d. A live methodological trap this run walked into: `attestation_presence` is single-commit-scoped, not diff-scoped, and the worktree is shared
INVOKED   : re-comparison of the two full runs above (§1c `--all` at commit `cb34ec9`
            vs §3c `--changed-from` run, executed minutes later)
STAGE     : substrate
EXIT      : n/a (analysis of two prior runs)
READS     : `governance/check-registry.yaml:906-908` (`attestation_presence` no_floor
            note: "changeset-scoped — examines the SYNTHESIS files in HEAD~1..HEAD, not
            the 79 attestations on disk"); `scripts/audit/adherence_log_audit.py:517,565-570`
            (`def audit(check_filter=None, base="HEAD~1", head="HEAD")` — a fixed,
            single-commit default, not wired to whatever `--changed-from` ref the caller
            used)
WRITES    : NONE
EXAMINED  : 2 runs of the same check, different HEAD each time
OUTPUT    : §1c (`--all`, HEAD=`cb34ec9`): `[FAIL] attestation_presence` — "changed files:
            4; attestations: 0; synthesis: 1" — flagged the just-committed
            `sessions/session_2026-08-25-pipeline-smoke-test-mobility.md` as missing its
            attestation. §3c (`--changed-from origin/main`, HEAD had advanced to `d4042e6`
            by the time it ran — confirmed via `git log --oneline -5`, showing THREE
            sibling-agent commits landed in between, including one that committed MY OWN
            `S6-substrate.md` log): `[NONE] attestation_presence` — HEAD~1..HEAD is now
            `99ad647..d4042e6`, which touches no synthesis path, so the check is correctly
            silent about a commit range that genuinely has nothing to say.
FINDING   : PASS for the check's own logic (it did exactly what its no_floor note says);
            **FLAG for interpretation discipline** in a shared multi-agent worktree
LOCATION  : `scripts/audit/adherence_log_audit.py:517` (`base="HEAD~1"` default — no
            `--changed-from`/ref threading from `run_checks.py`)
NOTE      : This check's "subject" is whatever the MOST RECENT commit happens to be at
            invocation time, and in this shared-worktree smoke test, sibling agents (S1-S5)
            were committing every few minutes throughout my run — confirmed 3 new commits
            landed between my two `run_checks.py` invocations, none authored by me. A
            green (or NOTHING-IN-SCOPE) `attestation_presence` result therefore proves
            only "the single most recent commit, whoever made it, didn't touch a synthesis
            path" — it is NOT proof the repository has no missing attestations at that
            moment (the real, still-live gap for
            `sessions/session_2026-08-25-pipeline-smoke-test-mobility.md` from §1c had not
            been fixed; the check simply stopped looking at it once a later commit moved
            HEAD~1..HEAD past it). For a real mobility batch: **do not trust a single
            green `attestation_presence` run as proof of attestation coverage** in a
            multi-agent session — re-run it immediately after your own commit, not after
            anyone else's.


## 4. `scripts/preflight.sh`

INVOKED   : `bash scripts/preflight.sh` (default mode — gates the diff vs `origin/main`)
STAGE     : substrate
EXIT      : 0   RUNTIME: 12.2s
READS     : `governance/check-registry.yaml` (via `run_checks.py --selftest` then
            `--changed-from origin/main`); fetches `origin/main` if the base ref is
            missing locally (`scripts/preflight.sh:82-85`)
WRITES    : NONE (explicitly documented as read-only: "it runs validators, it does NOT
            regenerate" — `scripts/preflight.sh:19-20`)
EXAMINED  : same 27-of-63 selection as §3c (identical diff base, identical HEAD at time of
            run) — plus, **unlike a bare `run_checks.py --changed-from` invocation**,
            `preflight.sh` runs `run_checks.py --selftest` FIRST and hard-exits
            (`|| exit 1`) if it fails (`scripts/preflight.sh:75-79`).
OUTPUT    : `===== preflight: registry selftest =====` → SELFTEST: PASS block, then the
            same battery results as §3c, then `PREFLIGHT: PASS — safe to push. (gated on
            your diff — run 'scripts/preflight.sh --all' for the full battery.)`
FINDING   : PASS
LOCATION  : `scripts/preflight.sh:75-79` (selftest gate), `:81-94` (mode dispatch —
            `--all` / `--kinds` / default `--changed-from $BASE`)
NOTE      : **`preflight.sh` closes exactly the gap CLAUDE.md's §5 box warns about for bare
            `run_checks.py --changed-from`** — it always runs `--selftest` first and treats
            a selftest failure as fatal before even looking at the diff. It agrees with CI:
            `ci.yml`'s `classify` job runs the identical two-step sequence (`--print-plan`
            for the battery selection, then a separate `--selftest` step explicitly labeled
            "BLOCKING — the gate that guards the gates", `.github/workflows/ci.yml:113-114`).
            One divergence worth flagging: `preflight.sh` is a single sequential script
            (selftest, then the full plan, one process) while `ci.yml` fans the same plan
            out into up to 9 parallel battery jobs gated by `if: contains(...batteries...)`
            — same registry, same classification logic, different execution topology. A
            battery that fails to trigger its `if:` condition in CI would still have run
            inside `preflight.sh`'s single invocation, so a passing local preflight is not
            proof CI's job-splitting itself is wired correctly (that is what CI's own
            `classify` job's `--print-plan` output is for).

## 5. CI — the four workflows

INVOKED   : `ls .github/workflows/`; full read of all four files
STAGE     : substrate
EXIT      : n/a
READS     : `.github/workflows/ci.yml` (270 lines, 13 jobs), `regenerate-derived.yml`,
            `resolve-dois.yml`, `verify-urls.yml`
WRITES    : NONE
EXAMINED  : 4 workflow files
OUTPUT    :
| Workflow | Trigger | Runs on a PR? | Runs on push to main? |
|---|---|---|---|
| `ci.yml` | `push: [main]`, `pull_request: [main]`, `workflow_dispatch` | **YES** — 12 jobs: `classify` + up to 9 battery jobs (syntax/structure/data/db-integrity/tests/schema/governance/attestation/research/render, each gated by `if: contains(...batteries...)`) | YES, same jobs, **plus** `commit-msg` |
| `regenerate-derived.yml` | `push: [main]` (path-filtered to `data/guidebook.db`, `governance/pipeline-contract.yaml`, 3 generator scripts, itself), `schedule` (Mon 07:30 UTC), `workflow_dispatch` | **NO** — no `pull_request:` trigger at all | Only if the pushed commit touches one of the 5 filtered paths |
| `resolve-dois.yml` | `workflow_dispatch` only | **NO** | **NO** — never fires on push, only manual dispatch |
| `verify-urls.yml` | `schedule` (bi-weekly, 1st/15th 06:00 UTC), `workflow_dispatch` | **NO** | **NO** — never fires on push, only schedule/manual |
FINDING   : PASS (accurate enumeration) — with one confirmed and one newly-found
            never-runs-on-the-PR-path item
LOCATION  : `if: github.event_name == 'push'` — **exactly one occurrence in the entire
            `.github/workflows/` tree**, confirmed with `grep -n "if: github.event_name"
            .github/workflows/*.yml`: `.github/workflows/ci.yml:257`, the `commit-msg` job.
            CLAUDE.md's claim ("The commit-message format check remains, and is still `if:
            github.event_name == 'push'`") is correct, verified at the exact line.
NOTE      : **Checks that never run on the path the workflow actually uses, beyond the
            documented commit-msg case:**
            (1) `commit-msg` (`ci.yml:253-263`) — push-only by explicit design (a PR's
            intermediate commits aren't walked, so a PR-time check would be misleading,
            per the job's own comment) — this is the ONE CLAUDE.md already names.
            (2) `resolve-dois.yml` and `verify-urls.yml` — **neither has a `pull_request:`
            or `push:` trigger at all.** They run only on `workflow_dispatch` (manual) or
            `schedule` (weekly/bi-weekly cron). Any check or invariant that lives inside
            these two pipelines (DOI/PMID resolution, URL verification) is therefore
            **never exercised by a PR or a push to main** — only by a human manually
            dispatching it, or by the cron firing on its own schedule, independent of any
            code or data change. This is not a defect (both are explicitly long-running,
            rate-limited, network-calling batch jobs unsuited to per-PR gating — see their
            own header comments), but it means a regression introduced INSIDE
            `scripts/resolve_dois.py` or `scripts/verify_urls.py` would not be caught by
            CI on the PR that introduces it — only by the next scheduled/manual run,
            possibly days later. For the mobility batch: neither pipeline is on the
            write path tested in §2 (`db.py` → `emit_batch_sql.py` → `emit_data_migration.py`
            → `migrate_db.py`), so this is orthogonal, but worth naming since the task
            explicitly asks for checks that never run on the path CI actually uses.


## 6. The hooks — all three

### 6a. `SessionStart` — contract injection + `ensure-deps.sh`, ordering
INVOKED   : `cat .claude/settings.json`
STAGE     : substrate
EXIT      : n/a (read)
READS     : `.claude/settings.json` `hooks.SessionStart[0].hooks` — a 2-element array:
            index 0 = the `printf` contract-injection one-liner, index 1 =
            `bash .claude/hooks/ensure-deps.sh`
WRITES    : NONE
EXAMINED  : 2 hooks in the SessionStart array
FINDING   : PASS (append discipline currently honoured)
LOCATION  : `.claude/settings.json` (`SessionStart[0].hooks[0]` = contract printf,
            `SessionStart[0].hooks[1]` = `ensure-deps.sh` — `ensure-deps.sh` is appended
            AFTER the contract hook, not inserted ahead of it)
NOTE      : Ordering is currently correct per CLAUDE.md's own warning ("APPEND it — never
            insert at index 0"). Cross-checked against the reader in 6c below.

### 6b. `PostToolUse(Bash)` → `record-command.py` — session resolution (file:line)
INVOKED   : full read of `.claude/hooks/record-command.py`
STAGE     : substrate
EXIT      : n/a (read)
READS     : `sessions/LATEST` (`.claude/hooks/record-command.py:117-129`)
WRITES    : `scratchpad/<session-stem>/commands.jsonl`
EXAMINED  : whole file (152 lines)
OUTPUT    : Confirmed — `lf=root/"sessions"/"LATEST"` then
            `sess=(lf.read_text().strip().removesuffix(".md") if lf.exists() else
            (d.get("session_id") or "unassigned"))` at `:127-129`. `.claude/session` is
            NOT read anywhere in the current file — grep for the string `.claude/session`
            inside this script returns nothing; the file's own comment block
            (`:118-125`) narrates its own removal: "Until 2026-08-23 this read
            `.claude/session`, a SECOND pointer to the same fact that nothing else
            maintained... So the divergent copy is removed rather than synced."
FINDING   : PASS (the code matches the claim)
LOCATION  : `.claude/hooks/record-command.py:127-129`

### 6c. Known live finding, confirmed and characterised: sessions/LATEST staleness RELOCATED, not fixed
INVOKED   : `git diff --stat HEAD~50 -- scratchpad/session_2026-08-23-research-batch-03-forward-mining/commands.jsonl`;
            `git log --oneline --all -- <same path>`; `cat sessions/LATEST`
STAGE     : substrate
EXIT      : 0
READS     : `scratchpad/session_2026-08-23-research-batch-03-forward-mining/commands.jsonl`
            git history; `sessions/LATEST` current content
WRITES    : NONE
EXAMINED  : 1 file's full commit history for the smoke-test session's lifetime
OUTPUT    : `git diff --stat` confirms **664 lines** were appended to
            `scratchpad/session_2026-08-23-research-batch-03-forward-mining/commands.jsonl`
            in commit `cb34ec9` ("governance: smoke-test protocol and session record,
            committed before running it [2026-08-25 18:19]") — the SAME commit that first
            set `sessions/LATEST` to
            `session_2026-08-25-pipeline-smoke-test-mobility.md` for this run. `cat
            sessions/LATEST` now correctly reads
            `session_2026-08-25-pipeline-smoke-test-mobility.md`.
FINDING   : FAIL — confirmed live recurrence of the exact bug class the 2026-08-23 fix
            claims to have closed, RELOCATED rather than eliminated
LOCATION  : `.claude/hooks/record-command.py:118-125` (the fix's own claim: "the divergent
            copy is removed rather than synced — per references/project-standards.md RULE
            2026-08-23, one fact, one home"); live evidence —
            `scratchpad/session_2026-08-23-research-batch-03-forward-mining/commands.jsonl`
            (664 misfiled lines, committed in `cb34ec9`)
NOTE      : **State it plainly, as instructed: moving the pointer from `.claude/session` to
            `sessions/LATEST` did NOT fix the staleness bug — it relocated it.** The
            original defect class was never "which file is the pointer" — it was "a single
            mutable pointer that is read continuously but only WRITTEN at specific ritual
            moments (session close-out), so anything that happens between one session's
            close-out and the next session's own close-out gets filed under whoever the
            pointer named last." `.claude/session` failed that way because nothing ever
            updated it. `sessions/LATEST` fails the identical way because it is updated at
            session close-out (per its own doc) — not at session START. This smoke-test
            session's own early activity (harness bootstrap, orchestrator setup, or an
            early sibling-agent turn — the specific author is not recoverable from the
            jsonl schema itself per 6d below) landed under the PRIOR session's directory
            (`session_2026-08-23-research-batch-03-forward-mining`) until a commit late in
            setup (`cb34ec9`) updated `LATEST` to point here. The fix changed WHICH pointer
            is stale; it did not change WHETHER one can be. A genuine fix would update
            `LATEST` at session START (or eliminate the window by writing to a
            self-identifying path that doesn't depend on a separately-timed update).

### 6d. The docstring's claim that success cannot be proven — reproduced live
INVOKED   : `python3 -c "raise RuntimeError('S6 deliberate traceback test for
            record-command.py')"` — a command guaranteed to raise a Python traceback and
            exit 1 — then `grep` the resulting jsonl line back out
STAGE     : substrate
EXIT      : 1 (the test command itself); the hook's own exit is untestable directly (it is
            harness-invoked) but its write succeeded
READS     : the harness's `tool_response` payload for the failing command
WRITES    : one line appended to `scratchpad/session_2026-08-25-pipeline-smoke-test-
            mobility/commands.jsonl` (grepped back out by matching the literal command text)
EXAMINED  : 1 command, 1 resulting jsonl record
OUTPUT    :
```
{
  "ts": "2026-08-25T18:31:35Z",
  "command": "...python3 -c \"raise RuntimeError('S6 deliberate traceback test...')\"...",
  "exit": null,
  "is_error": null,
  "interrupted": false,
  "response_keys": ["interrupted","isImage","noOutputExpected","stderr","stdout"],
  "stdout_sha256": "55465e12c49e2ddc340003de35f50e4208c09508687b2f220fbf50c283e2a474",
  "bytes": 156,
  "stderr_sha256": null,
  "stderr_bytes": 0
}
```
FINDING   : PASS — the docstring's claim is TRUE, reproduced directly rather than taken on
            the file's own word
LOCATION  : `.claude/hooks/record-command.py:73-113` (the two "MEASURED CORRECTION" comment
            blocks documenting `exit`/`is_error` as always-null and `stderr` as always-
            present-but-empty)
NOTE      : Exactly as documented: `exit` and `is_error` are both `null` even though the
            command demonstrably raised and exited 1 (visible directly in the terminal at
            invocation time). `stderr_bytes` is `0` — the traceback text is not separately
            captured; it is folded into `stdout` (`bytes: 156` covers both the traceback
            and the terminal's own visible "python exit was 1" tail). **This log line alone
            cannot distinguish this failing command from a clean success** — a reader would
            need the actual terminal transcript (outside this file) to know it failed. The
            docstring's warning ("no gate, session record or attestation may cite a line in
            this file as evidence that a command WORKED... It proves a command was ISSUED")
            is accurate and independently reproduced here, not merely inherited from the
            file's own prior self-report.

### 6e. `research_contract_hook.py` ordering trap and `research_contract_sync` check
INVOKED   : `grep -n 'SessionStart\[0\]' scripts/generate/research_contract_hook.py`;
            `python3 scripts/generate/research_contract_hook.py --check`
STAGE     : substrate
EXIT      : 0
READS     : `.claude/settings.json` `hooks.SessionStart[0].hooks[0].command`
            (hardcoded index, confirmed); `governance/research-contract.yaml` (51 contract
            lines)
WRITES    : NONE (`--check` mode)
EXAMINED  : 51 contract line(s) — printed explicitly by the check
OUTPUT    : `EXAMINED: 51 contract line(s)` / `PASS: contract and enforcer agree on 15 rule
            ids` / `PASS: the SessionStart hook matches governance/research-contract.yaml`
FINDING   : PASS (both the trap-location claim and the live check)
LOCATION  : `scripts/generate/research_contract_hook.py:90` (`return
            settings["hooks"]["SessionStart"][0]["hooks"][0]["command"]`, the reader) and
            `:155` (the identical hardcoded-index write path in the generator itself) —
            confirmed by direct grep, both lines index `[0]["hooks"][0]`, exactly the trap
            CLAUDE.md names.
NOTE      : Currently green because 6a confirmed the contract hook is still at index 0.
            This is a live landmine, not a historical one: any future `SessionStart` hook
            addition that does not APPEND (per CLAUDE.md's own instruction, itself likely
            written after paying this exact cost on 2026-08-25) will turn this check red
            with a diff that reads as contract drift and isn't.

### 6f. `Stop` hook — run manually
INVOKED   : the exact Stop-hook command from `.claude/settings.json`:
            `python3 scripts/audit/research_batch_dod.py --all` (guarded by the same `[ -f
            ... ] && [ -f data/guidebook.db ]` existence checks as the real hook)
STAGE     : substrate
EXIT      : 0
READS     : `data/guidebook.db` (read-only — the CANONICAL committed DB, not any scratch;
            this hook always evaluates the corpus-wide research definition-of-done, not a
            per-session slice)
WRITES    : NONE
EXAMINED  : R1 through R15 (15 rules; R11 reported separately as "~", inherited debt) —
            concrete subject counts printed per rule: R1 "7 co1/co2-targeted searches, 3
            co1/co2 sources"; R2 "10 citation_mining rows for 10 anchors"; R4 "25
            population linkages... 28 searches"; R7 "60 candidates for 431 screened"; R9a
            "10 admitted DOI(s)"; R13 "all 10 tier-1..3 admissions"
OUTPUT    : all 15 rules `PASS`, `~ R11: 856 (baseline 856) — INHERITED DEBT, not a
            regression`, `COMPLIANT — all research definition-of-done rules met.`,
            `RESEARCH DoD: PASS (exit 0)`
FINDING   : PASS
LOCATION  : `scripts/audit/research_batch_dod.py`
NOTE      : Every rule prints a concrete EXAMINED-style count rather than a bare PASS —
            this is the definition-of-done gate working as a non-vacuous check, and it
            correctly evaluates against the corpus as committed (`data/guidebook.db`), NOT
            against any of the six agents' scratch DBs — so nothing this smoke test wrote
            to `$SMOKE/s6-substrate.db` could have influenced this result either way.


## 7. Cross-stage contract criteria — the named enforcers, run individually

Invocation notes: run against the CANONICAL DB read-only (`data/guidebook.db`) except
`audit_consolidator.py`, run against `$SMOKE/s6-substrate.db` with `--dry-run` (it is a
per-item report writer, not a corpus gate — confirmed NOT in `governance/check-
registry.yaml` at all, `grep -n audit_consolidator governance/check-registry.yaml` empty).

| Script | Invocation | Exit | EXAMINED | Verdict |
|---|---|---|---|---|
| `scripts/audit/adherence_log_audit.py` | `--check all` (default) | 0 | changed files: 7; attestations: 1; synthesis: 0 | PASS — "No issues." |
| `scripts/audit/claims_docket.py` | `check` | 0 | 68 docket claims | PASS — "68/68 docket claims carry warrant annotations" |
| `scripts/audit/migration_reproducibility.py` | (bare), then `--deep` | 0, 0 | 7 core invariants; 66 tables (deep) | PASS both (full detail in §2h) |
| `scripts/doctrine_recheck.py` | bare (no flags) | **1** | 4 snapshot subjects (11 govs/8 rules/163 decisions/102 BPC) | **FAIL** — 3 ERRORS, drift pass (2.4) only |
| `scripts/doctrine_recheck.py` | `--cross-ref` (**the registered form**) | 0 | same 4 subjects, pass 2.3 only | PASS — 5 WARNINGS, 0 ERRORS (drift pass 2.4 never runs) |
| `scripts/decision_capture.py` | bare | 0 | not instrumented (registry: "not-instrumented... C1-C9 each examine a different subject"); live: 163 ACTIVE decisions, 61 DRs on disk | PASS (exit 0) despite 56 WARNINGS incl. "51 of 61 Decision Records have no register row" |
| `scripts/audit/pipeline_contract_audit.py` | bare | 0 | 19 contract criteria | PASS — 14 VERIFIABLE / 5 INCOMPLETE / 0 BROKEN (see breakdown below — one of the 14 is a **false VERIFIABLE**, see 7b) |
| `scripts/audit/graph_audit.py` | bare | 0 | 825 | PASS — "live errors=0" (3 named findings are pre-existing/awaiting-migration classes, not live errors) |
| `scripts/audit/code_currency_audit.py` | bare | 0 | (5 CHECKs; CHECK 4/5 both 0) | PASS — "TOTAL ISSUES: 0" — **note: this script is QUARANTINED in the registry** (`run_checks.py --list` output, §3a: "RED. Flags standards lacking a currency marker; a content backlog, not a gate.") yet ran clean standalone; its quarantine reason concerns a different historical state than what I measured today — re-quarantine status should be re-verified, not assumed current, before relying on either verdict. |
| `scripts/audit/retired_vocabulary_audit.py` | bare | **1** | 26 files | **FAIL** — 66 occurrences of retired vocabulary on the live surface (matches §1c/§3c's `retired_vocabulary` FAIL exactly — this IS the check registered under id `retired_vocabulary`) |
| `scripts/audit/db_path_env_audit.py` | bare | 0 | 45 scripts scanned | PASS — 43/45 honour `GUIDEBOOK_DB_PATH` directly, 2 documented, named exemptions |
| `scripts/audit/readonly_db_open_audit.py` | bare | 0 | 32 (of 48 total DB consumers; 16 excluded as writers, named exclusion, not silent) | PASS — "32/32 read-only consumers open read-only" |
| `scripts/audit/register_integrity_check.py` | bare | 0 | 15 cells × 6 registers = 90 cell-checks | PASS — "I1–I5 hold" |
| `scripts/audit/validate_pydantic_schemas.py` | bare | 0 | 18 tables | reports non-zero drift (245 findings) but labelled **informational** by the script itself — registry confirms `level: advisory` (§1c/§3a) |
| `scripts/audit_adversarial_use.py` | bare | 0 | 9 (ACTIVE adversarial-use vectors) | PASS, 1 WARNING ("no ACTIVE/IN_PREP guidebook versions found — may be unbuilt", pre-launch-consistent per CLAUDE.md §3) |
| `scripts/audit_consolidator.py` | `--item E-08 --session ... --dry-run` against `$SMOKE/s6-substrate.db` | 0 | 1 item (E-08) | Not a gate — per-item brief generator. Output: "Pipeline steps complete: None" for E-08 — **confirms E-08 has zero recorded audit-pipeline history**, corroborates §9. |

### 7a. `scripts/doctrine_recheck.py` — the registered check invokes a NARROWER mode than the tool's own default, and the narrower mode is the one that never runs drift detection
FINDING   : FAIL (a real coverage gap, not a false alarm)
LOCATION  : `governance/check-registry.yaml:799-800` (`cmd: [python3, scripts/doctrine_recheck.py, --cross-ref]` — the ONLY registered invocation); `scripts/doctrine_recheck.py:332-338`
            (`if not args.cross_ref: prior = find_prior_snapshot(...); findings_24, drift_summary
            = detect_drift(snapshot, prior); findings_25 = check_decision_register(snapshot)`
            — passes 2.4 (drift) and 2.5 (decision-register) run ONLY when `--cross-ref` is
            **absent**, i.e. never in the registered/CI-run form)
NOTE      : Running the tool bare (no flags — its own genuine default, confirmed `--full`
            is a documented-but-unreferenced no-op flag: `grep -n "args\.full"
            scripts/doctrine_recheck.py` → zero hits) surfaced **3 real ERRORS** the
            registered `--cross-ref` form never sees: `governance/co1-operational.md`,
            `governance/evidence-methodology.md` and `governance/population-taxonomy.md`
            each "present in prior snapshot (2026-04-30 13:30) but absent now" — i.e. three
            governance documents that doctrine once cited have since disappeared from the
            repository, undetected by anything CI or `run_checks.py` invokes. **Drift
            detection (pass 2.4) — the one pass whose entire purpose is catching exactly
            this class of silent doctrinal loss — exists in the codebase, is fully
            functional (I ran it and it worked), and is wired to nothing any gate runs.**
            This is CLAUDE.md §2(a)'s failure mode in a specific, sharper form: not a check
            that passes having examined nothing, but a check that is REGISTERED under a
            flag that structurally cannot examine the one thing its own name promises.
            Whether these 3 missing docs are themselves a real problem is a governance
            question outside this smoke test's remit — but the fact that the tool capable
            of flagging them is never invoked by anything automated is squarely in scope.

### 7b. `pipeline_contract_audit.py`'s own coverage map has one CONFIRMED false-VERIFIABLE
FINDING   : FAIL (the audit's own referential-integrity pass under-reports incompleteness
            by exactly 1, for a documented, reproducible reason)
LOCATION  : `scripts/audit/pipeline_contract_audit.py:78-107` (`classify_check` —
            resolves a contract criterion's named `check:` file to a **path**, then asks
            only "does this path exist AND is it registered ACTIVE anywhere in
            check-registry.yaml" — never checks whether any registered check's own `basis:`
            field still claims that specific criterion id); `governance/pipeline-
            contract.yaml:149-152` (`cross_stage/attestation-doctrine-binding`, `check:
            scripts/audit/adherence_log_audit.py`); `governance/check-registry.yaml:942`
            (the SAME file backs `attestation_evidence`, whose `basis:` is
            `cross_stage/adherence-log` — with an inline comment stating exactly this:
            "attestation-doctrine-binding dropped 2026-08-19: its enforcer
            (check_2_doctrine_sha) was retired with the doctrine token, and
            pipeline_contract_audit resolves enforcers at FILE granularity so it could not
            see the gate go vacuous")
OUTPUT    : `pipeline_contract_audit.py` reports **14 VERIFIABLE / 5 INCOMPLETE**
            (§7 table above). `run_checks.py --selftest`'s C7 (§3b), which matches
            criterion ids against the LIVE `basis:` strings actually declared in the
            registry — a stricter, string-level check — independently reports **5**
            uncovered criteria too, but a DIFFERENT fifth one:
            `cross_stage/attestation-doctrine-binding` (not in `pipeline_contract_audit.py`'s
            INCOMPLETE list) in place of `render/render-freshness` (which
            `pipeline_contract_audit.py` DOES list as INCOMPLETE, so C7 does cover that one
            — the two lists are 4/5 identical, disagreeing on exactly one entry each way).
NOTE      : **The two coverage tools disagree with each other, and the disagreement traces
            to a documented, self-acknowledged blind spot in `pipeline_contract_audit.py`
            itself** — its own repo already explains why, in a comment the audit script
            cannot read. The honest combined picture (correcting `pipeline_contract_audit.py`'s
            file-granularity false positive with `run_checks --selftest`'s C7 basis-string
            check) is **13 genuinely VERIFIABLE, 6 genuinely uncovered** — one worse than
            either tool reports alone. For the mobility batch this is orthogonal (neither
            gap touches the write path or the mobility items), but it means: **do not trust
            `pipeline_contract_audit.py`'s VERIFIABLE count in isolation** — cross-check
            against `run_checks.py --selftest`'s C7 INFO line, and where they disagree, the
            `--selftest` C7 basis-string match is the more trustworthy of the two (it
            resolves at the granularity that actually matters — which criterion a check
            currently CLAIMS to serve — rather than merely whether its file happens to
            still be registered for something).

### 7c. The honest, corrected pipeline-contract coverage map (VERIFIABLE / INCOMPLETE / BROKEN)
Per stage, from `pipeline_contract_audit.py`'s own breakdown (§7 table), corrected per 7b:

| Stage | VERIFIABLE | INCOMPLETE | BROKEN |
|---|---|---|---|
| research | 2 | 0 | 0 |
| evidence-collection | 1 | 1 (`discovery-provenance`) | 0 |
| judgment | 3 | 2 (`derivation-handshake`, `convergence-independence`) | 0 |
| synthesis | 1 | 1 (`opus-routing`) | 0 |
| render | 2 | 1 (`render-freshness`) | 0 |
| cross_stage | 3\* (was 4 reported; `attestation-doctrine-binding` moves to INCOMPLETE per 7b) | 1 (`attestation-doctrine-binding`, corrected) | 0 |
| **Total (corrected)** | **13** (not the reported 14) | **6** (not the reported 5) | **0** |

\* `cross_stage` count is not printed as its own row by `pipeline_contract_audit.py` (it
only breaks out research/evidence-collection/judgment/synthesis/render); derived here as
19 total − the 5 named per-stage rows' (2+1+3+1+2)=9 → 10 cross_stage-and-other criteria,
of which 1 is now reclassified. Exact cross_stage total not independently re-derived line
by line in this pass — flagged as a residual gap in this smoke test's own coverage, not
asserted as precise.

