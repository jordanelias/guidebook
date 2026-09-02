# COMPLIANCE-CONTRACT — research batch 04, accessible circulation

**Author:** antagonist session (adversarial role, `references/project-standards.md:638` RULE, owner
directive 2026-08-19). **Phase 1 deliverable.**
**Derived:** 2026-09-01 against `data/guidebook.db` at `PRAGMA user_version = 65`,
sha256 `589eb30bf2af37d47ff73cff9fe0b18b4fc13b0be9db1a4d918afc6bb4487084`, on `main` @ `708948a`.

Every claim below carries the file:line, SQL, or command that produced it. **Nothing here is
recalled; everything is measured.** Where a governance document and the live code/database
disagree, the disagreement is marked **⚠ CONTRADICTION** and both sides are named — CLAUDE.md §2(b)
makes prose-that-contradicts-the-database one of the three real failure modes, so those are
findings in their own right, not footnotes.

**Re-derivation command for the volatile numbers in this file:**
```bash
python3 - <<'EOF'
import sqlite3,sys; sys.path.insert(0,'scripts'); import dbcore
con=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
for t in ('search_executions','search_candidates','evidence_sources','source_slug_links',
          'search_admissions','evidence_population_match','citation_mining',
          'evidence_source_authors','gaps','source_locators','economics_entries'):
    print(t, con.execute(f'select count(*) from {t}').fetchone()[0])
print('next_ref_id', dbcore.next_ref_id(con))
EOF
```

---

## 0. THE FIVE THINGS THAT WILL BREAK THIS BATCH

Ranked by measured likelihood. Each is expanded below with its derivation.

| # | Failure | Where it bites | §  |
|---|---|---|---|
| 1 | **The harness-injected contract orders a FORBIDDEN write.** `governance/research-contract.yaml` R12 hook still reads *"Code values -> jurisdictional_values"*, and that text is live in `.claude/settings.json` right now. D-0181 (2026-08-31, owner) forbids it. | Step 10 | §5.4 |
| 2 | **`author_fidelity` will examine ZERO of this batch's sources.** `retrieval-log/session_2026-09-01-research-batch-04-accessible-circulation/` holds 12 payloads and **no `manifest.jsonl`**, so `_logged_payloads()` returns `{}` and the check that exists *because of the 2026-08-19 fabrication* returns INDETERMINATE. | Steps 6–7 | §5.1 |
| 3 | **DR §12.1 step 7 orders a rule-5 dual write that the code refuses to make.** It says set `admitted_ref_ids='[…]'` and §12.4 names H03/H04 parity. H03/H04 were **DELETED 2026-08-24**; `log_search` deliberately does not write the column. | Step 7 | §5.2 |
| 4 | **`db.py` refuses a value the schema's own CHECK declares.** `--locator-status DEAD` is rejected. Reproduced below. | Step 4 | §2.7 |
| 5 | **`add-source` cannot write `notes`, so R3's `[UNVERIFIED-QUANT]` escape is unreachable from the CLI.** Only `--pages` can satisfy R3 for a T4–T6 source. | Step 7 | §2.4 |

---

## (a) THE EXACT WRITE VOCABULARY

Source: `SELECT sql FROM sqlite_master WHERE type='table' AND name=?` and
`PRAGMA table_info(...)` / `PRAGMA foreign_key_list(...)`, all under
`sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)`.

### a.0 ⚠ CONTRADICTION — `dbcore.check_values()` is BLIND to 8 of the columns this batch writes

`scripts/dbcore.py:348-349`:
```python
m = re.search(r"CHECK\s*\(\s*%s\s+IN\s*\(([^)]*)\)" % re.escape(column), row[0], re.I)
```
The regex demands `CHECK ( <col> IN (`. Every nullable-form constraint in this schema is written
`CHECK (<col> IS NULL OR <col> IN (...))` — the token after `CHECK (` is `IS`, not `IN`, so the
search never matches and `check_values()` returns the **empty set**.

Measured, `dbcore.check_values(con, table, column)`:

| Column | CHECK exists in DDL? | `check_values()` returns |
|---|---|---|
| `search_executions.depth_method` | plain form | `['scoping','systematic']` ✅ |
| `search_executions.backfill` | plain form | `['0','1']` ✅ |
| `search_candidates.disposition` | plain form | 5 values ✅ |
| `search_candidates.harm_finding` | plain form | `['0','1']` ✅ |
| `evidence_population_match.match_grade` | plain form | 4 values ✅ |
| `gaps.category` / `gaps.priority` | plain form | 12 / 3 values ✅ |
| `source_locators.status` | plain form | 3 values ✅ |
| `citation_mining.backward` / `.forward` | plain form | `['0','1']` ✅ |
| `evidence_sources.data_capture_status` | plain form | 4 values ✅ |
| `evidence_sources.citation_mining_status` | plain form | 4 values ✅ |
| **`search_executions.target_evidence_type`** | nullable form | **`[]`** ❌ |
| **`search_executions.target_scope`** | nullable form | **`[]`** ❌ |
| **`search_executions.mining_direction`** | nullable form | **`[]`** ❌ |
| **`search_executions.saturation_signal`** | nullable form | **`[]`** ❌ |
| **`search_candidates.locator_status`** | nullable form | **`[]`** ❌ |
| **`gaps.mining_addressability`** | nullable form | **`[]`** ❌ |
| **`evidence_sources.scope`** | nullable form | **`[]`** ❌ |
| **`evidence_sources.processing_blocked_reason`** | nullable form | **`[]`** ❌ |
| **`evidence_sources.verification_method`** | nullable form | **`[]`** ❌ |
| **`evidence_sources.verification_disposition`** | nullable form | **`[]`** ❌ |

**Consequence.** For every ❌ column, `dbcore.check_vocab()` (`scripts/dbcore.py:380-397`) falls
through to `live_vocab()` — *the live rows*. CLAUDE.md §4 says in terms: *"Live rows are a sample of
a vocabulary, never the vocabulary."* The module whose docstring claims to have fixed exactly this
(`dbcore.py:375-379`) is doing exactly this on ten columns. See §2.7 for the reproduced refusal.

**The vocabularies below are therefore transcribed from the DDL text, not from `check_values()`.**

### a.1 `search_executions` (STRICT)

FK: `slug → slugs.slug`.
NOT NULL: `slug`, `language`, `query_text`, `engine`, `depth_method`, `results_found` (dflt 0),
`results_screened` (dflt 0), `results_admitted` (dflt 0), `backfill` (dflt 0), `session`,
`executed_at`, `harm_finding` (dflt 0).

| Column | Permitted values (from the DDL) |
|---|---|
| `target_tier` | NULL, or integer 1–6 (`BETWEEN 1 AND 6`) |
| `target_evidence_type` | NULL, `clinical`, `sr_meta`, `standard_eb`, `national_fw`, `code`, `co1`, `co2`, `grey` |
| `target_scope` | NULL, `intrinsic`, `lower_control`, `high_control`, `national`, `international` |
| `depth_method` | **`scoping` \| `systematic` — nothing else** (no CHECK on NULL; NOT NULL) |
| `mining_direction` | NULL, `none`, `backward`, `forward`, `both` |
| `saturation_signal` | NULL, `none`, `partial`, `saturated` |
| `backfill` | `0` \| `1` |
| `terms_used` | NULL or `json_valid` |
| `admitted_ref_ids` | NULL or `json_valid` — **DO NOT WRITE, see §4.2** |

`engine` and `language` have **no CHECK at all**. Live `engine` values (a sample, not a
vocabulary): `consensus, crossref, manual, semanticscholar, source_locators, web`. Live `language`:
`DE, EN, IT, en` — note `en` and `EN` both present; R5 (`scripts/audit/research_batch_dod.py:377`)
compares `upper(language)`, so casing is tolerated there, but **use uppercase** (`db.py:993`).

### a.2 `search_candidates` (STRICT)

FKs: `exec_id → search_executions.exec_id`; `found_under_slug → slugs.slug`;
`suggested_slug → slugs.slug`.
NOT NULL: `found_under_slug`, `disposition`, `title`, `harm_finding` (dflt 0), `session`, `created_at`.

| Column | Permitted values |
|---|---|
| `disposition` | `REHOME` \| `MISCELLANEOUS` \| `PENDING-VERIFICATION` \| **`OUT-OF-SCOPE`** \| `ADMITTED` |
| `locator_status` | NULL \| `UNVERIFIED` \| `RESOLVED` \| **`DEAD`** |
| `tier_guess` | NULL, or integer 1–6 |
| `harm_finding` | `0` \| `1` |

`OUT-OF-SCOPE` is declared and has **zero live rows**; `DEAD` is declared and has zero live rows.
`OUT-OF-SCOPE` is safe (plain-form CHECK → `check_values` sees it). **`DEAD` is not — see §2.7.**

### a.3 `evidence_sources` (NOT STRICT — 90 columns)

**No FK inbound or outbound.** NOT NULL: only `data_capture_status` (dflt `'pending'`) and
`citation_mining_status` (dflt `'pending'`).

⚠ **`tier`, `evidence_type`, `verification_status`, `metadata_quality`, `source_type`,
`jurisdiction`, `co1_provenance` carry NO CHECK constraint.** `tier` is a bare INTEGER; the table
is not STRICT, so `tier='banana'` would be accepted by SQLite. The only guards are:

* `scripts/db.py:1081` — `--tier` is `type=int` (no `choices`), so any integer passes the CLI;
* `scripts/emit_data_migration.py:96` `RANGE_GUARDS = [("tier", 1, 6, ...)]` — **blocking at
  migration time**, matched on a bare `\btier\b`, so `target_tier` / `tier_guess` do not trip it;
* `scripts/emit_data_migration.py:66` `ENUM_GUARDS` for `doi_resolution_outcome`
  (`RESOLVED`|`NO-MATCH`|`REVERTED`) and `url_resolution_outcome`.

Columns with a real CHECK:

| Column | Permitted values |
|---|---|
| `scope` | NULL, `high_control`, `lower_control`, `national`, `international`, `intrinsic` |
| `data_capture_status` | `pending` \| `captured` \| `none-extractable` \| `deferred` |
| `citation_mining_status` | `pending` \| `mined` \| `deferred` \| `not-applicable` |
| `processing_blocked_reason` | NULL, `no-full-text`, `paywalled`, `no-doi`, `not-indexed`, `language`, `no-quantified-claims`, `superseded`, `out-of-scope`, `tier-not-required` |
| `verification_disposition` | NULL, `OPEN`, `CLOSED` |
| `verification_method` | NULL, `direct-render`, `co1-attestation`, `corroborated-not-retrieved`, `citing-bibliography`, `tool` |
| `verification_closure_reason` | NULL, `paywalled`, `print-only`, `access-denied-persistent`, `withdrawn`, `not-found-after-search`, `disputed-existence` |

⚠ **`verification_method` CHECK declares SIX values; `db.py:1100-1102` offers FOUR** — `direct-render`
is in the schema and absent from the CLI `choices`. A source that was actually fetched and read
(the strongest verification this project has) cannot be recorded as such through the documented
path. Report as a coverage bug; do not hand-write SQL to reach it (CLAUDE.md §4).

Live vocabulary (a **sample** of 10 rows — do not treat as the vocabulary):
`tier ∈ {1,2,3}`, `evidence_type ∈ {clinical, co1, sr_meta}`, `verification_status = {VERIFIED}`,
`metadata_quality = {COMPLETE}`, `doi_resolution_outcome = {RESOLVED}`, `source_type` all NULL.

### a.4 `source_slug_links`

FKs: `ref_id → evidence_sources.ref_id`; `slug → slugs.slug`. PK `(ref_id, slug)`.
NOT NULL: **all seven columns** — `ref_id`, `slug`, `local_ref_id`, `created_at`,
`created_by_session`, `updated_at`, `updated_by_session`. No CHECKs.
⚠ `insert_source_slug_link` (`db.py:2031`) uses **`INSERT OR IGNORE`** — a duplicate
`(ref_id, slug)` silently no-ops and the caller is told nothing. This is the exact pattern
`insert_evidence_source` denounces 90 lines above it (`db.py:1980-1985`).

### a.5 `search_admissions`

FKs: `exec_id → search_executions.exec_id`; `ref_id → evidence_sources.ref_id`. PK `(exec_id, ref_id)`.
NOT NULL: `exec_id`, `ref_id`. `created_at` / `created_by_session` nullable. No CHECKs.
**This is the sole home of an admission edge** (owner ruling 2026-08-24, `db.py:405-412`).

### a.6 `evidence_population_match`

FKs: `ref_id → evidence_sources.ref_id`; `gap_id → gaps.gap_id`.
NOT NULL: `source_ref`, `target_population`, `match_grade`, `created_at`, `created_by_session`.
⚠ **`source_ref` is NOT NULL and carries NO foreign key**; `ref_id` carries the FK and is nullable.
The two hold the same value. This is a live rule-5 dual home that cannot be dropped (committed data
migrations INSERT it — `db.py:2350-2353`). The CLI writes `source_ref` **from** `ref_id`; never
supply it separately.
⚠ **`target_population` is NOT NULL with NO foreign key to `populations`.** The only guard is
`db.py:2334` (`dbcore.exists(conn,'populations','population_code', ...)`) — i.e. **the CLI is the
only thing standing between this table and an invented population code.** Hand-written SQL would
land it silently.

| Column | Permitted values |
|---|---|
| `match_grade` | `EXACT` \| `PARTIAL` \| `PROXY` \| `MISMATCH` |

Live `populations.population_code` (23): `ADHD, ALL, AUT, BAR, BLIND, BRAIN, COM, DEAF, DEAFBLIND,
DEM, EPI, ID, LMB, LPA, MH, MOB, MOVE, MS, NDV, PAIN, SCI, TALL, VES`.

### a.7 `citation_mining`

FKs: `slug → slugs.slug`; `global_ref_id → evidence_sources.ref_id`. PK `(slug, local_ref_id)`.
NOT NULL: `slug`, **`local_ref_id`** (no default), `backward` (dflt 0), `forward` (dflt 0),
`connections_produced` (dflt `'[]'`), and all four audit columns.
`backward` / `forward` ∈ `{0,1}`.
⚠ **`local_ref_id` is NOT NULL and `log_mining` LOOKS IT UP from `source_slug_links`**
(`db.py:243-246`). If the source is not already linked to that slug, the lookup yields `None` and
the INSERT dies on NOT NULL. **`add-source --slug X --local-ref-id Y` must precede
`log-mining --slug X`.**
`doi` exists as a column but the writer's `doi` parameter was **removed 2026-08-24** (`db.py:207-211`)
— it is a copy reachable through `global_ref_id`, and 2 of 10 rows had already drifted by case.

### a.8 `evidence_source_authors`

FK: `ref_id → evidence_sources.ref_id`. PK `id` (AUTOINCREMENT). `UNIQUE(ref_id, position, role)`.
NOT NULL: `ref_id`, `position`, `is_corporate` (dflt 0), `role` (dflt `'author'`). No CHECKs.
Written only in the same transaction as the source (`db.py:2013-2024`); `insert_evidence_source`
**refuses a source with no authors** (`db.py:2007-2012`).

### a.9 `gaps`

No inbound FK from this batch except `evidence_population_match.gap_id`.
NOT NULL: `category`, `priority`, `status`, `description`, and all four audit columns (no defaults).

| Column | Permitted values |
|---|---|
| `category` | `RP` `SW` `CR` `ST` `MX` `CD` `EC` `EG` `CI` `DEC` `CONF` `AUDT` |
| `priority` | `P1` \| `P2` \| `P3` |
| `status` | any string matching `LIKE 'OPEN%'` **or** `LIKE 'CLOSED%'` |
| `mining_addressability` | NULL, `ADDRESSABLE`, `NOT-ADDRESSABLE`, `TRIAGE-NEEDED` |

⚠ `db.py next_gap_id()` (`db.py:2273`) selects `WHERE gap_id GLOB 'GAP-[0-9]*'`. The five live gaps
are `GAP-B01-001 … GAP-B02-001` — **none matches that GLOB**, so `add-gap` will mint **`GAP-001`**,
breaking the batch-scoped convention the previous two batches used. Mint the id yourself in the
established `GAP-B04-NNN` shape, or accept `GAP-001` deliberately and say so.

### a.10 `source_locators`

PK `ref_id`. **No foreign keys, and no audit columns at all** (`dbcore.stamp_for`, `dbcore.py:283`,
exists because of this). NOT NULL: `recovered_from` (dflt `'corpus-pre-reset-2026-08-06'`),
`status` (dflt `'REFERENCE-ONLY'`).
Table-level CHECK: **at least one of** `doi, url, pmid, pmcid, isbn, issn, standard_number, title`
must be non-NULL.

| Column | Permitted values |
|---|---|
| `status` | `REFERENCE-ONLY` \| `PROMOTED` \| `RETIRED` |

Live `recovered_from` values: `corpus-pre-reset-2026-08-06`, `global-reference-registry.json`,
`references/global-reference-registry.md`. **No CHECK** — but `--recovered-from` is *required*
(`db.py:906`), and `check_vocab` has no declared set for it so it falls to live vocab (3 values);
**a new provenance string will be REFUSED** by the same fall-through as §2.7. Use one of the three,
or report the coverage bug.

Current: **875 rows**, high-water `REF-00964`.

---

## (b) THE `scripts/db.py` WRITER SURFACE, AND WHAT IT REFUSES

Read from the argparse definitions in `main()` (`scripts/db.py:780-1290`) and the insert functions.
`R` = required.

### b.1 `log-search` → `search_executions` + `search_admissions` (`db.py:989-1036`, `log_search` at `db.py:336`)

**R:** `--slug --language --query-text --engine --depth-method --session`
**Optional:** `--jurisdiction --target-tier --target-evidence-type --target-scope --terms-used
--mining-direction --results-found --results-screened --results-admitted --admitted-ref-id
(repeatable) --saturation-signal --findings-note --harm-finding --deferred-reason --backfill --dry-run`

`choices=` enforced **in argparse** (fails before touching the DB):
`--depth-method {scoping,systematic}`; `--target-tier 1..6`;
`--target-evidence-type {clinical,sr_meta,standard_eb,national_fw,code,co1,co2,grey}`;
`--target-scope {intrinsic,lower_control,high_control,national,international}`;
`--mining-direction {none,backward,forward,both}`;
`--saturation-signal {none,partial,saturated}`.
⚠ `--harm-finding` and `--backfill` are `type=int` with **no `choices`** — `--harm-finding 7` passes
argparse and dies on the STRICT CHECK.

**Refusals (`db.py:369-382, 415-424`):**
1. `--admitted-ref-id` repeated → `ValueError` naming invariant **H07**.
2. `--results-admitted N` ≠ count of `--admitted-ref-id` → `ValueError` naming **H05**.
   (If `--results-admitted` is omitted, it is set to `len(ids)` automatically.)
3. Any `--admitted-ref-id` not present in `evidence_sources` → named `ValueError`, whole
   transaction rolls back including the execution row. **File the source first.**

**No `dbcore.check_vocab` call anywhere in `log_search`.** Vocabulary enforcement for this table is
argparse `choices` + the STRICT table CHECKs. That is adequate here.

⚠ **`admitted_ref_ids` is NOT written** (`db.py:394-396`, comment; `db.py:405-412`, rationale).
The junction is the sole home. See §4.2.

### b.2 `add-candidate` → `search_candidates` (`db.py:823-837`, `insert_search_candidate` at `db.py:2273`)

**R:** `--found-under-slug --disposition --title --session`
**Optional:** `--exec-id --suggested-slug --locator --locator-status --tier-guess --harm-finding
{0,1} --why-not-admitted --notes --dry-run`
⚠ `--disposition` and `--locator-status` have **no argparse `choices`** — they are checked at the DB
layer only.

**Refusals:**
1. `--exec-id` not a live `search_executions` row → named `ValueError` (`db.py:2283-2288`).
2. `--found-under-slug` not in `slugs` → `ValueError` (`db.py:2289`).
3. `--suggested-slug` not in `slugs` → `ValueError` (`db.py:2293`).
4. `disposition` outside the declared CHECK set → `ValueError` naming the set (`db.py:2295`).
5. `locator_status` outside the **live vocabulary** → `ValueError`. **Not the CHECK set.** §2.7.
6. **`disposition='ADMITTED'` requires `locator_status='RESOLVED'`** (`db.py:2299-2306`). This is a
   CLI-only rule; the schema does not encode it.

`candidate_id` auto-allocates as `MAX+1` (`db.py:2310`). Current max: 60 rows.

### b.3 `add-source` → `evidence_sources` + `evidence_source_authors` (+ optional `source_slug_links`)

(`db.py:1055-1118`, `insert_evidence_source` at `db.py:1866`)

**R:** `--ref-id --year --title --tier --session`, **and exactly one of `--author` (repeatable,
preferred) or `--authors`** (`db.py:1510-1514`).
**Optional:** `--doi --pmid --jurisdiction --evidence-type --lang-detected --lang-detection-method
--metadata-quality --verification-method --verified-by-tool --verification-status --url
--url-accessed --pages --doi-resolution-outcome --slug --local-ref-id --dry-run`

`choices=`: `--metadata-quality {COMPLETE, COMPLETE-STATUTORY, PMID-ONLY, GREY, AUTHOR-TITLE-ONLY}`;
`--verification-method {tool, corroborated-not-retrieved, co1-attestation, citing-bibliography}`;
`--verification-status {VERIFIED, UNVERIFIED}`.
**No `choices` on `--tier`, `--evidence-type`, `--doi-resolution-outcome`, `--jurisdiction`.**

**Refusals:**
1. `--ref-id` not matching `REF-\d{5}|REF-VERIFIED-\d{3}|Co1-\d{2,3}` → `ValueError`, with a special
   hint when the value looks like a per-slug local label (`db.py:1938-1950`).
2. Writer-retired author copies (`author_display`, `first_author_last`, `author_count`,
   `is_corporate_primary`, …) → `ValueError` (`db.py:1885-1893`, migration 063).
3. `verification_status='VERIFIED'` with no `--verification-method` → `ValueError` (D-0157).
4. `verification_method='tool'` with no `--verified-by-tool` → `ValueError` (invariant I4b).
5. `--ref-id` already in `evidence_sources` → `ValueError` (**not** `INSERT OR IGNORE`; `db.py:1980-1990`).
6. `--doi` already filed under another live ref_id → `ValueError` naming it (**R9 enforcement is a
   live DB query**, `db.py:1991-2000`). Comparison is `doi = ?` — **case-sensitive**, see §3-R9.
7. No authors → `ValueError` (`db.py:2007-2012`).
8. `--authors` display string it cannot parse without guessing → refused, not approximated
   (`parse_author_display`, `db.py:1829`).

**Auto-filled:** `verification_attempt_count=1`; for `UNVERIFIED`, `verification_disposition='OPEN'`.

**⚠ FIELDS THIS BATCH MAY NEED THAT NO SUBCOMMAND CAN WRITE (coverage bugs — report, do not
hand-write SQL):**

| Field | Why the batch needs it | Status |
|---|---|---|
| **`evidence_sources.notes`** | **R3's `[UNVERIFIED-QUANT]` flag lives here** (`research_batch_dod.py:336`). `_ES_COLS` *permits* it (`db.py:1917`) but **no `--notes` flag exists** and `main()` never populates it (`db.py:1515-1548`). | **UNREACHABLE** |
| `evidence_sources.article_number` | R3's other satisfier (`research_batch_dod.py:334`). Not in `_ES_COLS`, no flag. | UNREACHABLE |
| `evidence_sources.standard_number` | identity of a T4–T6 standard | UNREACHABLE |
| `evidence_sources.journal_name`, `volume`, `issue`, `publisher`, `isbn`, `issn`, `url_resolution_outcome`, `source_type`, `scope`, `subtype`, `co1_provenance`, `co1_source_type` | bibliographic identity | UNREACHABLE via CLI |
| `evidence_sources.verification_method='direct-render'` | the strongest verification available | in schema, **absent from CLI `choices`** |
| `evidence_population_match.match_id` | a **same-session dissenting grade** collides on the auto id (§b.4) | no flag |
| `source_locators.doi_resolution_outcome`, `url_resolution_outcome`, `url_last_fetched`, `jurisdiction` | | not in `insert_locator._COLS` |

**Net effect on R3:** for a tier ≥ 4 source, the only CLI-reachable satisfier is **`--pages`**.
DR §12.4 failure mode 5 predicted this ("R3 unsatisfiable via CLI for T4-T6"); the 2026-08-25
supersession note in the DR claims *"R3 … CAN now be satisfied through the CLI"*.
⚠ **CONTRADICTION — that supersession note is half true.** `--pages` landed; `--notes` and
`--article-number` did not. Measured: `grep -n "notes" scripts/db.py` shows no `p_as.add_argument("--notes")`.

### b.4 `add-population-match` → `evidence_population_match` (`db.py:839-849`, `insert_population_match` at `db.py:2318`)

**R:** `--ref-id --target-population --match-grade --session`
**Optional:** `--study-population --sample-size --mismatch-note --gap-id --dry-run`
No argparse `choices` on `--match-grade`.

**Refusals:**
1. `--ref-id` not in `evidence_sources` → `ValueError` (case-folded via `dbcore.fold_ref`).
2. `--target-population` not in `populations` → `ValueError`.
3. `match_grade` outside `{EXACT,PARTIAL,PROXY,MISMATCH}` → `ValueError` naming the set.
4. `match_grade='MISMATCH'` with no `--mismatch-note` → `ValueError`.

**DELIBERATELY NOT REFUSED:** a second row for the same `(ref_id, target_population)` — it prints a
NOTE to stderr and writes. DR-2026-08-19 §7: a dissenting adversarial grade lands as a second row
and divergent grades read as a contest (`db.py:2340-2349`).
⚠ **But the mechanic is unreachable within one session id.** `match_id` defaults to
`f"{session[:24]}-{ref}-{target_population}"` (`db.py:2358`) and is the PRIMARY KEY, with no
`--match-id` flag. Two grades of the same `(ref, pop)` under the same session string collide on the
PK. Since the antagonist and the orchestrator share
`session_2026-09-01-research-batch-04-…` (`[:24]` = `session_2026-09-01-resea`), **a Phase-2
dissenting grade cannot be filed by this CLI.** Coverage bug; flag it, do not route around it.

### b.5 `log-mining` → `citation_mining` (`db.py:812-820`, `log_mining` at `db.py:201`)

**R:** `--slug --ref --direction --connections --session`. `--direction` is `{backward, forward}`
only — **`both` and `none` are refused** (`_VALID_DIRECTIONS`, `db.py:186`), even though the
`search_executions.mining_direction` column accepts them. Call it twice for both.
Upserts on `(slug, global_ref_id)`, merging `connections_produced` order-preserving-deduplicated.
⚠ **No refusal exists for a missing `source_slug_links` row** — the `local_ref_id` lookup returns
`None` and the write dies on NOT NULL with a bare `IntegrityError`. See §a.7.

### b.6 `add-locator` → `source_locators` (`db.py:899-909`, `insert_locator` at `db.py:2499`)

**R:** `--ref-id --recovered-from --status --session`.
**Optional:** `--doi --pmid --pmcid --isbn --issn --url --standard-number --title --authors
--pub-year --tier-claimed --used-in-bpcs --notes --dry-run`

**Refusals:**
1. `--ref-id` not matching `REF_ID_SHAPE` → `ValueError` — and this one names the **correct** fix:
   *"Mint with `dbcore.next_ref_id()`"* (`db.py:2506-2508`).
2. `--ref-id` already in `source_locators` → `ValueError`.
3. `--status` outside `{REFERENCE-ONLY, PROMOTED, RETIRED}` → `ValueError`.
4. **Duplicate-identity:** the same DOI held under a different `ref_id` in **either**
   `source_locators` or `evidence_sources` → `ValueError` (`db.py:2513-2527`). Case-folded via
   `dbcore.norm_doi` — this is the refusal R9a/R9b detect after the fact.

### b.7 `add-gap` → `gaps` (`db.py:926-933`, `insert_gap` at `db.py:147`)

**R:** `--category --priority {P1,P2,P3} --description --session`. Optional `--skill --section --dry-run`.
`status` is hardcoded to `'OPEN'` (`db.py:1349`). `gap_id` from `next_gap_id()` — see §a.9 warning.
**No validation beyond the table CHECKs.** `--category` has no argparse `choices`.

### b.8 The R9 pre-check has no read subcommand

`db.py next-id` accepts only `{connections, gaps, terms, conflicts}` (`db.py:1330-1335`). **There is
no `next-id refs` and no `check-doi` subcommand.** The correct mint is `dbcore.next_ref_id(conn)`,
reachable only by importing the module.

---

## (c) THE SEVENTEEN RULES AND THEIR ENFORCEMENT POINTS

Enforcer: `scripts/audit/research_batch_dod.py`, function `audit()` (line 271).
Scope for a session run: `scope = " AND session = ?"`, rewritten per-table to
`" AND created_by_session = ?"` where that is the column.
**Exit 0 = COMPLIANT.** Registered as `research_dod` (`--all`, **advisory**) and
`research_dod_selftest` (**blocking**) — ⚠ **the per-session run is NOT a registered check.**
The batch's own definition-of-done is self-administered; that is precisely why an antagonist exists.

The docstring table (`research_batch_dod.py:30-88`) is **documentation, not the contract**
(line 25-27). `governance/research-contract.yaml` governs the *text*; the SQL below governs the
*pass*.

| Rule | Measures (exact predicate, line) | Literal token | Easiest way to fail it |
|---|---|---|---|
| **R1** | `co1` = COUNT search_executions WHERE `target_evidence_type IN ('co1','co2')` (L289); `co1_src` = COUNT evidence_sources WHERE `evidence_type IN ('co1','co2')`; `co1_waiver` = COUNT WHERE `findings_note LIKE '%CO1-NOT-APPLICABLE%'`. **Fails only if all three are 0.** Query-text hints are a *hint only* (L297). | `CO1-NOT-APPLICABLE:` in `findings_note` | Doing a lived-experience search but typing `--target-evidence-type grey` instead of `co1`. Text mentioning "lived experience" proves nothing. |
| **R2** | `admitted` = evidence_sources `tier BETWEEN 1 AND 3` this session; `mined_rows` = citation_mining this session (L317). Fails if `admitted>0 AND mined_rows==0`, **or** `mined_rows < max(1, admitted//4)` (`R2_MINING_PER_ANCHORS=4`, L153). `mining_direction<>'none'` is explicitly **not** evidence (L321-325). | — | Logging a chase as a search row and forgetting the `citation_mining` row. With 8 admissions you need **2** rows, not 1. |
| **R3** | evidence_sources WHERE `tier >= 4` AND `article_number` empty AND `pages` empty AND `notes NOT LIKE '%UNVERIFIED-QUANT%'` (L333-337). | `[UNVERIFIED-QUANT]` in `notes` — matched as bare substring `UNVERIFIED-QUANT` | Admitting any T4–T6 source. **`--notes` does not exist**, so `--pages` is the only CLI satisfier (§b.3). |
| **R4** | `total` = searches this session; `linked` = evidence_population_match this session (L360). Fails if `total>0 AND linked==0`. **Structural only** — v1 matched `"disabilit"`, v2 matched population codes and hit `COM` inside "accommodate" (L349-355). | — | Doing all the crossing in query text and none in rows. |
| **R5** | search_executions WHERE `upper(language) <> 'EN' AND target_evidence_type = 'grey'` (L377). | — | Targeting a German or Italian standards search as `grey`. Use `national_fw` / `standard_eb` / `code`. |
| **R6** | COUNT WHERE `deferred_reason IS NOT NULL AND results_found > 0` (L388). | — | Writing a finding into `deferred_reason` on a search that returned hits. |
| **R7** | `cand` = search_candidates this session; `screened` = SUM(`results_screened`); `expected = max(1, screened//25)` (`R7_SCREENED_PER_CANDIDATE=25`, L158). Fails if `total AND cand < expected` (L405). | — | Screening 200 results and staging 5 candidates: `expected` = 8. **`results_screened` is what sets the bill.** |
| **R8** | `MAX(exec_id) > COUNT(*)` **corpus-wide, unscoped** (L418). Currently `28 == 28`. | — | Any deleted or skipped `exec_id`. The migration must insert a contiguous run continuing from 28. A `--dry-run` that consumed an id, or a rolled-back scratch write, leaves a hole. |
| **R9** | DOIs appearing >1× in `evidence_sources` where at least one row is this session's (L432-436). | — | ⚠ **Comparison is `e.doi IN (SELECT doi …)` with no `LOWER()`.** SQLite TEXT `=` is case-sensitive, so `10.1044/…AJA-19-0010` and `…aja-19-0010` are two DOIs to R9 — the exact drift `dbcore.norm_doi` (L182-190) exists to fold. **Normalise DOIs to lowercase yourself.** |
| **R9a** | `evidence_sources e JOIN source_locators sl ON LOWER(TRIM(sl.doi))=LOWER(TRIM(e.doi)) WHERE sl.ref_id <> e.ref_id` (L471). **Also FAILS on `n_doi == 0`** — "NOTHING IN SCOPE" is a failure, not a pass (L481). | — | **Admitting only DOI-less grey/standards material fails R9a outright.** At least one admission must carry a DOI. |
| **R9b** | `JOIN source_locators sl ON sl.ref_id = e.ref_id` where any of `doi, pmid, pmcid, isbn, issn, standard_number` is populated in both and differs (L490-505). Also fails on `n_adm == 0`. | — | Minting a `ref_id` at or below the stash high-water mark (`REF-00964`) → collides with a held identifier. §(f). |
| **R10** | (a) `verification_status='VERIFIED'` AND no `doi`/`url`/`pmid`/`verified_by_tool` (L510); (b) `VERIFIED` AND `doi<>''` AND `doi_resolution_outcome NOT IN ('RESOLVED','NO-MATCH')` (L515). | `RESOLVED` / `NO-MATCH` in `doi_resolution_outcome` | Omitting `--doi-resolution-outcome`. Every VERIFIED DOI-bearing source fails. It **is** now settable on `add-source` (`db.py:1076`). |
| **R11** | `term_aliases WHERE COALESCE(notes,'')='' AND created_by_session = ?` (L538). | `[UNVERIFIED-TERMS]` (per contract text; the SQL only requires *non-empty* notes) | Adding any alias with an empty `notes`. **Passes trivially if the batch adds no aliases** — 0 rows in scope. |
| **R12** | `econ_words` = searches this session whose `findings_note` matches `%cost%`, `%grant%` or `%bcr%` (case-insensitive, L546-549); `econ_rows` = **`SELECT COUNT(*) FROM economics_entries`, corpus-wide and unscoped** (L552). Fails if `econ_words AND econ_rows < econ_words`. | `cost` / `grant` / `bcr` | **`economics_entries` holds 0 rows.** The word "cost" *anywhere* in *any* `findings_note` creates an immediate, unpayable debt. Note `%cost%` also matches **"costly", "costing"** — and `%grant%` matches nothing common, but `%bcr%` is safe. **Write no `findings_note` containing "cost".** |
| **R13** | For each `evidence_sources` row `tier BETWEEN 1 AND 3` this session, require `EXISTS(SELECT 1 FROM evidence_population_match WHERE ref_id = ?)` (L570-573). ⚠ **Joins on `ref_id`, NOT `source_ref`.** | — | A hand-written match row that populates only `source_ref` (the NOT NULL column) passes the schema and fails R13. The CLI writes both. |
| **R14** | COUNT WHERE `results_found = 0 AND deferred_reason IS NULL AND COALESCE(findings_note,'') = ''` (L590). | — | Any kept zero-yield search with no note. One empty note = one failure. |
| **R15** | `search_candidates WHERE disposition='ADMITTED' AND COALESCE(notes,'') NOT LIKE '%RESOLVED%'` (L607). | `RESOLVED` in **`notes`** (DR §12.1 step 7 uses `RESOLVED:` as the prefix) | ⚠ **Two different columns.** `db.py:2299` forces `locator_status='RESOLVED'` for an ADMITTED candidate; R15 reads **`notes`**. Setting the column and leaving notes empty fails. ⚠ **And `LIKE '%RESOLVED%'` also matches `UNRESOLVED`** — the opposite meaning satisfies the gate. Use the `RESOLVED:` prefix and never the word "unresolved" in a candidate note. |

**Baseline amnesty** (`check_baseline`, L168) applies **only in `--all` mode** (L636). A
`--session` run gets no forgiveness.

**Acceptance requires more than exit 0.** DR §12.3.1: *"every PASS line showing non-zero
subjects"*. R9a/R9b print theirs; R13's line prints the admission count and **must equal yours**.

---

## (d) STAGE BOUNDARIES, DERIVED

**The spine** (`governance/pipeline-contract.yaml:8-…` `stages:` list, and
`tools/pipeline_completeness.py:37` `STAGES`, which agree):
`base → research → evidence → judgment → synthesis → specification → render`.
The stage id is **`evidence`**, not `evidence-collection`; the display form is derived by
`stage_label()` (`pipeline_completeness.py:42`), never stored.

**Derivation of table → stage.** Per CLAUDE.md, *"Derive the table-to-stage assignment; do not read
one out of a document"*, and every pre-2026-08-27 bucket map is void. I derive from the two
authorities that postdate the ruling: CLAUDE.md's own stage-content table (owner-ruled 2026-08-27)
and each stage's `entry:`/`criteria:` in `governance/pipeline-contract.yaml`.

| Table | Stage | Derivation |
|---|---|---|
| `slugs`, `populations`, `items`, `terms`, `term_aliases`, `access_needs`, crossing maps | **base** | CLAUDE.md names these as substrate verbatim; contract `base.entry` = *"a vocabulary, registry or crossing map the downstream stages resolve codes against"*. |
| `search_executions` | **research** | CLAUDE.md research = *"What was searched…"*. |
| `search_candidates` | **research** | *"…screened…"*. |
| `citation_mining` | **research** | *"…and mined…"*. |
| `source_locators` | **research** | *"…plus the clue store."* `db.py:899` help text: *"Write a lead into the **clue store**"* — the phrase is the same. Corroborated by CLAUDE.md §4: *"a lead index of identifiers, not evidence"*. |
| `evidence_sources` | **evidence** | CLAUDE.md evidence = *"What was admitted, its identity, verification…"*; contract `evidence.entry` = *"sources discovered for the topic/slug under research"*. |
| `evidence_source_authors` | **evidence** | *"its identity"* — authors are the identity, and migration 063 made this its sole home. |
| `source_slug_links` | **evidence** | binds an admitted source to the slug; carries `local_ref_id`, the per-slug citation label. |
| `search_admissions` | **evidence** *(boundary object)* | *"What was **admitted**"*. It is the only table in this batch whose two FKs land in different stages (`exec_id→search_executions` = research; `ref_id→evidence_sources` = evidence). **It IS the research→evidence hand-off edge**, and therefore the pointer rule 5 describes. |
| `source_value_extractions` | **evidence** (produced) / **judgment** (consumed) | CLAUDE.md evidence ends *"…and extraction"*; the contract states `handoff-fanout-preserved` over this table inside stage `judgment`. Not written by this batch (0 rows). |
| `evidence_population_match` | **judgment** | CLAUDE.md judgment = *"Whether an extraction is sound and how it weighs — grading, **population matching**"*. |
| `gaps` | **base (my derivation, stated as such)** | ⚠ CLAUDE.md's substrate list does **not** name `gaps`. I place it in `base` because it is a registry other stages point *into* by FK (`evidence_population_match.gap_id → gaps.gap_id`) and holds no stage-specific process data. **This is an inference, not a ruling. Flag it rather than rely on it.** |

**Consequence the orchestrator must internalise: this batch spans THREE stages.** Research
(`search_executions`, `search_candidates`, `citation_mining`, `source_locators`), evidence
(`evidence_sources`, `evidence_source_authors`, `source_slug_links`, `search_admissions`) and
judgment (`evidence_population_match`). That is legitimate — `governance/pipeline-map.yaml`
established 2026-08-21 that a walk **re-enters** stages — but it means R13's grading is a *judgment*
act. **Do not let a judgment fact leak backwards into a research row.** In particular: a tier
verdict, a population grade, or a soundness assessment belongs in `evidence_sources.tier` /
`evidence_population_match`, never in `search_executions.findings_note` as the only record of it.

### d.1 Rule 5 applied to THIS batch — the forbidden second homes

| Fact | Sole home | Second home that must stay empty | Authority |
|---|---|---|---|
| Which sources a search admitted | `search_admissions` (edge rows) | **`search_executions.admitted_ref_ids`** | owner ruling 2026-08-24; `db.py:394-396`, `db.py:405-412`; H03/H04 deleted at `test_db_integrity.py:1019` |
| Who wrote a source | `evidence_source_authors` rows | `evidence_sources.author_display`, `first_author_last`, `first_author_first`, `author_count`, `is_corporate_primary` — **the writer raises `ValueError` if you pass any** | migration 063; `db.py:1885-1893` |
| A mined source's DOI | `evidence_sources.doi`, reached via `citation_mining.global_ref_id` | `citation_mining.doi` — parameter **removed** 2026-08-24 after 2 of 10 rows drifted by case | `db.py:207-211` |
| A source's per-slug label | `source_slug_links.local_ref_id` | `citation_mining.local_ref_id` — **looked up, never invented** | `db.py:237-246` |
| A graded source's ref id | `evidence_population_match.ref_id` | `evidence_population_match.source_ref` — NOT NULL, undroppable, **written from `ref_id` by the CLI so the two cannot disagree** | `db.py:2350-2356` |
| Bibliographic detail of a source carrying a `ref_id` | `evidence_sources` | any restatement in `economics_entries.source`, `case_studies.sources`, a note, or a candidate title | CLAUDE.md §4 (`add-source` deliberately exposes no `--year`/`--journal` for a ref_id-bearing entry) |
| The admission count | `COUNT(search_admissions)` | `search_executions.results_admitted` — a third store, **kept honest at write time (H05, `db.py:377-382`) and by the blocking corpus check (`test_db_integrity.py:1032`)**. It must equal, exactly. | |

**Pointer, not copy — the positive form.** A promoted `source_locators` lead keeps **the same
`ref_id`** in `evidence_sources`. That is not a dual home; it is the pipeline working, and R9a's
own comment says so (`research_batch_dod.py:451-455`: *"every DOI then held in both tables (4 of
them) carried the SAME ref_id in each"*). Minting a *new* ref_id for a held lead is the violation.

---

## (e) THE TRAPS THIS BATCH WILL HIT, RANKED

### e.1 — `author_fidelity` will examine zero of this batch's sources  ⬅ **fix before step 7**

Measured:
```
$ ls -a retrieval-log/session_2026-09-01-research-batch-04-accessible-circulation/
NFBUK_Access_for_Blind_People_in_Towns.doc   RNIB_Seeing_Streets_Differently_2021.pdf
NFBUK_Access_for_Blind_People_in_Towns.txt   RNIB_Seeing_Streets_Differently_2021.txt
RCOT_Adaptations_Without_Delay_2019.pdf      aota_home_mod_libpage.html
crossref_10.1080_10803548.2019.1567974.json  crossref_10.1155_2019_9717208.json
crossref_10.1177_0361198118787082.json       crossref_10.3141_2145-08.json
crossref_10.7139_2017.978-1-56900-459-3.json
                                       ← NO manifest.jsonl
```
`scripts/research/retrieval_log.py:159-177` `_logged_payloads()` reads **`manifest.jsonl` only**;
absent, it returns `{}`. `verify_authors()` (L240-250) then prints
`EXAMINED: 0` / `INDETERMINATE — a session with no logged retrievals cannot be verified offline.
That is the gap this module exists to close; it is not a pass.` and exits 1.

Batch 01, by contrast, has a manifest with `{"retrieved_at", "url", "purpose", "sha256", "bytes",
"exit", "artefact"}` per line, artefacts named `<sha16>.<ext>`.

**The check registered as `author_fidelity` is the direct remedy for the 2026-08-19 fabrication —
12 of 19 author rows naming non-authors, including the deletion of autistic community co-authors
from a Co-1 paper.** Shipping this batch with an unreadable retrieval log reproduces the exact
precondition of that failure: authors written from a payload that no offline tool can diff.

**Avoidance:** route every retrieval through `retrieval_log.fetch(url, session=S, purpose=...)`
(`retrieval_log.py:118`) so the manifest is written by the tool, or run
`python3 scripts/research/retrieval_log.py --session "$S" --backfill` after admission (L323) to
re-fetch Crossref for every DOI-bearing source — the manifest marks a backfill as such. **Do not
hand-write `manifest.jsonl`**; the sha256 is the point.

### e.2 — DR §12.1 step 7 orders a write the code refuses ⚠ **CONTRADICTION**

**Governance says (RATIFIED, and CLAUDE.md calls this instrument operative and *"meant to be
run"*):** DR-2026-08-19 §12.1 step 7 — *"in one transaction: UPDATE search_executions SET
results_screened=…, results_admitted=…, `admitted_ref_ids='[…]'` … The JSON array, the junction
rows and the count must agree exactly (H03/H04/H05, blocking)."* §12.4 failure mode 3 gives a
parity query over `json_array_length(COALESCE(admitted_ref_ids,'[]'))`.

**The database and the code say:**
* `test_db_integrity.py:1019` — *"H03/H04 **DELETED** 2026-08-24 — they policed a dual-write that no
  longer happens."*
* `test_db_integrity.py:980-986` — `admitted_ref_ids` removed from `EDGE_JSON`, *"the JSON column is
  no longer written… Deleted rather than left green."*
* `test_db_integrity.py:1061-1065` — the same removal from H07's tuple list, noted as *"A second
  reference, in the same file, missed by the first sweep."*
* `db.py:394-396` — `# admitted_ref_ids intentionally NOT written — search_admissions is the sole
  home (owner ruling 2026-08-24).`
* `schemas/search_execution.py:54` — `admitted_ref_ids: Optional[str] = None  # RETIRED - do not write`
* Live: 3 of 28 `search_executions` rows carry a non-NULL `admitted_ref_ids` — all pre-ruling.

**WHAT SURVIVES: H05 only**, and it is corpus-wide and blocking:
```sql
SELECT COUNT(*) FROM search_executions se
WHERE se.results_admitted != (SELECT COUNT(*) FROM search_admissions sa WHERE sa.exec_id = se.exec_id)
```
(`test_db_integrity.py:1026-1031`.) Currently 0 drift across 28 rows.

**Ruling for this batch: DO NOT WRITE `admitted_ref_ids`.** `log-search --admitted-ref-id` writes the
junction and sets `results_admitted` in the same transaction with H05/H07 enforced at write time
(`db.py:369-382`). Use it; do not "enrich" afterwards. If a search's admissions are only known after
the sources are filed, **log that search after the sources exist** — R8 forbids deleting a logged
search, not deferring one that has not been logged yet.

### e.3 — `governance/research-contract.yaml` R12 orders a forbidden write ⚠ **CONTRADICTION**

**Live, right now, injected into every session** (`python3 -c "import json;
print(json.load(open('.claude/settings.json'))['hooks']['SessionStart'][0]['hooks'][0]['command'])"`):
```
R12 Case studies -> case_studies. Economics -> economics_entries. Code
    values -> jurisdictional_values. Never leave them in prose notes.
```
Source: `governance/research-contract.yaml` rule R12 `hook:` field; the payload is **generated**
from it by `scripts/generate/research_contract_hook.py` and its parity is enforced by the
**blocking** `research_contract_sync` check.

**Forbidden by:** D-0181 / `decisions/DR-2026-08-31-strike-jurisdictional-values-clause.md`, "RATIFIED
ON CONTACT" under CLAUDE.md rule 0, restating the owner's 2026-08-12 **REFERENCE-ONLY** ruling. Its
own rationale names this exact hazard: *"the runbook walks the next batch into a forbidden write."*
Measured live state, confirming the ruling took effect and nothing has crept back:
`jurisdictional_values` = **109 rows**, and `value_text`, `value_numeric`, `unit`,
`is_code_minimum`, `source_section`, `notes` are **0 non-null of 109**.

**DR-2026-08-31 struck the runbook clause and did not sweep the contract**, which is the *caller* —
CLAUDE.md rule 4: *"A rename or removal is not done until the callers are swept… A sweep that stops
at the filename is not a sweep."* The clause is struck in `DR-2026-08-19` §12.1 step 10 (the
strikethrough and the STOP box are both present in the file); it is live in the harness injection.

**Ruling for this batch:** `jurisdictional_values` is **REFERENCE-ONLY**. It names *which document to
go and get*, never what it says. `db.py add-jurisdictional-value` exists and must not be called.
**Code and standard values are staged as LEADS in `search_candidates`** — DR §12.1 step 10 STOP box:
*"Code values are staged as leads in `search_candidates`, which is where D-1 puts them."* An
`[UNVERIFIED-QUANT]` marker is explicitly **not** a licence to write where writing is forbidden. A
prior session followed the struck clause, wrote 12 rows, and was caught by the blocking
`test_db_integrity` L02 cardinality parity (109 YAML records vs 121 table rows); migration
`data_20260821185514` retracts them.

Report the R12 hook text as a finding. **Do not edit `research-contract.yaml` inside this batch** —
that is a governance change, it would turn the blocking `research_contract_sync` red until
`--write` regenerates `settings.json`, and DR-2026-08-19 §7 forbids a pass from emitting anything
but data plus one session record.

### e.4 — the session-id trap: bare stem vs `.md`

**This repository has produced this failure four times** (DR §12.4 #4), and CLAUDE.md §7 records a
fifth variant. The rule, by surface:

| Surface | Form | Derivation |
|---|---|---|
| `search_executions.session` | **bare stem** | live rows: `session_2026-08-19-research-batch-01-…` (no `.md`) |
| `*.created_by_session` on every table | **bare stem** | live rows, all tables |
| `db.py --session` (all subcommands) | **bare stem** | it lands in those columns unchanged |
| `research_batch_dod.py --session` | **bare stem** | it compares against those columns |
| `sessions/LATEST`, `sessions/LATEST-RESEARCH` | **`.md`** | live: `session_2026-09-01-lens-architecture.md` |
| `emit_data_migration.py --session` | **`.md`** | DR §12.1 step 11 |
| `citation_mining_completeness.py --session` | **`.md`** | DR §12.1 step 12; check-registry `@SESSION@` from `LATEST-RESEARCH` |
| `retrieval_log.py --session` | **either** — `_session_stem()` strips `.md` (`retrieval_log.py:146-156`) | |

A stem/`.md` mismatch scopes a gate to nothing **and it passes green**. Check the `EXAMINED:` line
on every gate. `citation_mining_completeness` prints one of `OUTSTANDING` / `CLEAN` /
**`NOTHING-IN-SCOPE`** precisely so a pass cannot be confused with an abstention
(`citation_mining_completeness.py:32-36`).

**Both pointers currently name other sessions** — `LATEST` = `session_2026-09-01-lens-architecture.md`,
`LATEST-RESEARCH` = `session_2026-08-22-research-batch-02-room-acoustic-performance.md`. Both move at
close; the **blocking** `citation_mining_session` check keeps auditing batch 02 until
`LATEST-RESEARCH` moves.

Your session id for the DB, verbatim:
`session_2026-09-01-research-batch-04-accessible-circulation`

### e.5 — `GUIDEBOOK_DB_PATH` inline on every call

`dbcore.db_path()` resolves **at call time, not import time** (`dbcore.py:51-59`), *"because the
harness resets env between shells; a module-level constant captured at import would silently ignore
that and write the canonical file."* **`export` does not protect you.** Prefix every invocation:
```bash
GUIDEBOOK_DB_PATH=/tmp/claude-0/.../scratchpad/batch04.db python3 scripts/db.py ...
```
The backstop, added 2026-08-27: `dbcore.connect()` **refuses to open the canonical database
read-write at all**, dry-run included, with **no override** (`dbcore.py:97-122`). That covers every
path through `dbcore`. It does **not** cover a raw `sqlite3.connect('data/guidebook.db')` in an ad
hoc script — and a read opened read-write can still flip `journal_mode` and dirty the blob
(`dbcore.py:89-94`). **Every read you write yourself must be
`sqlite3.connect('file:<path>?mode=ro', uri=True)`.**

`sha256sum data/guidebook.db` must equal `589eb30b…4487084` at every checkpoint until
`migrate_db.py` runs. Step 0 recorded it at
`scratchpad/session_2026-09-01-research-batch-04-accessible-circulation/db-sha256-step0.txt`.

### e.6 — `db.py` refuses `--locator-status DEAD` (a schema-legal value)

Reproduced (read-only, `dbcore` only, no writes):
```
$ python3 -c "import sqlite3,sys; sys.path.insert(0,'scripts'); import dbcore
con=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
dbcore.check_vocab(con,'search_candidates','locator_status','DEAD','PROOF')"
ValueError: PROOF: 'DEAD' is not in the live vocabulary of search_candidates.locator_status,
which is ['RESOLVED', 'UNVERIFIED']. If this value is legitimately new, it is a doctrine change --
add it in a migration with its justification, not as a CLI argument.
```
The schema declares `CHECK (locator_status IS NULL OR locator_status IN ('UNVERIFIED','RESOLVED','DEAD'))`.
`DEAD` is legitimate and has zero live rows; §a.0 explains why `check_values()` cannot see it.
**Do not "add it in a migration."** The value already exists in the schema. If the batch needs to
record a dead locator, record the coverage bug and use `PENDING-VERIFICATION` +
`--why-not-admitted` instead. Same shape applies to `source_locators.recovered_from` (no CHECK; live
vocab of three strings) — a new provenance string will be refused.

### e.7 — R12's "cost" tripwire

`economics_entries` = **0 rows**, corpus-wide, and R12's denominator is unscoped
(`research_batch_dod.py:552`). One `findings_note` containing `cost` (or `costly`, `costing`),
`grant` or `bcr` creates an unpayable debt. DR §12.2 says the minimum-viable batch has *"**0
economics rows** (and therefore no cost/grant/bcr words in any note)"*. **Say "expenditure",
"capital outlay", "price".**

### e.8 — the emit-time guard scans the WHOLE batch file

`check_enum_guards` (`emit_data_migration.py:105-125`) **Form 2**: if the string
`doi_resolution_outcome` appears *anywhere* in the emitted SQL — it will, on every admission — the
guard then scans the **entire file** for any literal matching `'([A-Z][A-Z /-]{2,24})'` and refuses
if it is in
`{NOT-APPLICABLE, NOT APPLICABLE, N/A, NA, NONE, UNKNOWN, PENDING, NOT-CHECKED, UNRESOLVED}`.
**Blocking, not a warning.**

Cleared by inspection for this batch: `'PENDING-VERIFICATION'` and `'OUT-OF-SCOPE'` do **not** match
(the whole captured token is compared, and neither is in the set); `'UNVERIFIED'` is not in the set;
all `evidence_sources` status defaults are lowercase. **At risk:** any bare ALL-CAPS token in a
note, a `why_not_admitted`, a `deferred_reason` or a gap description — e.g. `notes='PENDING'`,
`why_not_admitted='UNKNOWN'`, `mismatch_note='N/A'`. Write those in prose.

`RANGE_GUARDS` (`emit_data_migration.py:96`) bounds a bare `\btier\b` to 1–6. `target_tier` and
`tier_guess` do not match `\btier\b` (underscore is a word character), so they are unaffected.

### e.9 — the emit walk's FK back-edge

`emit_batch_sql.py:49` walks `dbcore.WRITABLE_TABLES` (`dbcore.py:411-443`) and claims *"FK order: a
parent is always emitted before anything that references it"*. Measured against
`PRAGMA foreign_key_list`, **one back-edge exists**:
```
evidence_population_match.gap_id -> gaps.gap_id     [emitted at index 7; gaps at index 12]
```
So if this batch files a gap **and** points a population match at it, the migration inserts the
match before the gap. `migrate_db.py` computes a `PRAGMA foreign_key_check` delta inside the
transaction and rolls back on a new violation (DR §12.0 F5/F6 step 5).
**Avoidance:** either leave `--gap-id` NULL on every population match this batch writes, or file the
gap in a **separate, earlier** migration. Do not reorder `WRITABLE_TABLES` — that is apparatus
surgery inside a research batch.

### e.10 — `local_ref_id` must exist before mining

`log-mining` looks up `source_slug_links.local_ref_id` and writes it into a NOT NULL column
(`db.py:243-246`, §a.7). Order: `add-source --slug … --local-ref-id …` → then `log-mining`.

### e.11 — R8's append-only check is corpus-wide

`MAX(exec_id)` vs `COUNT(*)` over the **whole table**, currently `28 == 28`
(`research_batch_dod.py:418`). Every `exec_id` the scratch allocates must survive into the
migration. A `log-search` that raised after `cur.lastrowid` — e.g. an unknown `--admitted-ref-id`
— rolls back and does **not** consume an id (the whole transaction rolls back), so that is safe.
A scratch row later deleted by hand is not. **Never delete a `search_executions` row.**

### e.12 — do not read the reasoning doc yet

DR §12.4 #12: reading `references/bpc-reasoning/<slug>.md` before step 12 *"contaminates the
falsification design"*. Nothing in steps 1–11 needs it. **This binds the antagonist too**: my
Phase-2 blind re-grade is worthless if either of us has read the synthesis first.

---

## (f) THE `ref_id` ALLOCATION RULE

**What it actually computes.** `dbcore.next_ref_id(conn)` (`dbcore.py:263-270`) returns
`"REF-%05d" % (ref_id_high_water(conn) + 1)`, where `ref_id_high_water` (L232-260):

1. calls `ref_id_homes(conn)` (L220-229), which reads **`sqlite_master` + `PRAGMA table_info`** and
   returns **every table carrying a `ref_id` column** — derived from the schema, never listed in
   code, because a hardcoded pair *"was silently outside the mint"* for any new table and, worse,
   *"the loop swallowed `OperationalError` with `continue`, so after a table RENAME every home
   vanished, high water fell to 0, and `next_ref_id` minted `REF-00001` — on top of live data, with
   no error"*;
2. scans every non-NULL `ref_id` in every one of those tables against `REF-(\d{5})` — so
   `REF-VERIFIED-NNN` and `Co1-NN` are **recognised but never minted from** (`REF_ID_SHAPE`, L201);
3. **refuses** (raises) rather than returning 0 if no table carries a `ref_id` column at all.

Measured now, `dbcore.ref_id_homes(con)` = **12 tables**:
`economics_entries, evidence_population_match, evidence_source_authors, evidence_sources,
reference_stubs, search_admissions, source_locators, source_slug_links,
source_value_extractions, spec_value_probes, specification_source_links, supersession_check`.
`ref_id_high_water` = **970**. `next_ref_id` = **`REF-00971`**.

**Why the documented rule was wrong.** `source_locators` tops out at `REF-00964`;
`evidence_sources` at `REF-00970`. *"Mint above the `source_locators` high-water mark"* yields
`REF-00965` — **a live evidence row** (`REF-00965`, tier 1, `co1`, batch 01). The rule is the
**UNION** across every home. `dbcore._selftest()` (L471-481) builds exactly that shape and asserts
`REF-00971`.

⚠ **CONTRADICTION — the superseded rule is still the error message `add-source` prints.**
`scripts/db.py:1946-1949`:
> *"There is no allocator: **mint above the `source_locators` high-water mark**, or you will collide
> with a held identifier (CLAUDE.md §4)."*

and the explanatory comment at `db.py:1928` repeats it. CLAUDE.md §4 now says in terms: *"the rule
this file gave for weeks was **WRONG**."* The correct instruction is printed only by the *other*
writer — `insert_locator` at `db.py:2506-2508`: *"Mint with `dbcore.next_ref_id()`."* A session that
hits the `add-source` refusal and obeys its advice mints `REF-00965` and collides.

**What R9b does if the batch mints wrongly.** `research_batch_dod.py:490-508` joins
`evidence_sources e JOIN source_locators sl ON sl.ref_id = e.ref_id` and fails when any of
`doi, pmid, pmcid, isbn, issn, standard_number` is populated in both and differs case-insensitively:
> *"N ref_id(s) admitted by this batch collide with a HELD identifier in `source_locators` that
> identifies a DIFFERENT source — mint above the stash high-water mark."*

It reaches **751 of 875** stash rows (all six identifier types); the 84-ish rows with no identifier
at all *"cannot be adjudicated either way and are deliberately out of reach, not silently
included"*. And `R9b` **FAILS on `n_adm == 0`** — a batch that admits nothing does not get a pass here.
`insert_locator` (`db.py:2513-2527`) refuses the same collision at write time, case-folded, in both
`source_locators` and `evidence_sources`.

**Procedure for this batch.** Mint sequentially from `REF-00971` upward. Before each admission,
compute the mark from the scratch DB (which already contains everything canonical holds plus what
this batch has written):
```bash
GUIDEBOOK_DB_PATH=$SCRATCH python3 -c "
import sqlite3,sys; sys.path.insert(0,'scripts'); import dbcore
print(dbcore.next_ref_id(sqlite3.connect('file:'+__import__('os').environ['GUIDEBOOK_DB_PATH']+'?mode=ro',uri=True)))"
```
**If a DOI is already in `source_locators`, reuse that row's `ref_id` — do not mint.** That is the
promotion path R9a's comment describes as *"the pipeline WORKING"*.

---

## APPENDIX — further contradictions found, recorded but not actionable in this batch

1. **`governance/pipeline-contract.yaml` header says `status: PROPOSED`, `ratified: false`,
   `enforcement_level: 2`**, while CLAUDE.md calls it *"the single home of the stage ids"* under the
   heading *"THE MACHINE NOW ENFORCES THE SEVEN-STAGE SPINE"*. Its `spine:` field also still reads
   the pre-2026-08-27 four-hop chain `EvidenceSource → BPC entry → Specification → Item → render`,
   which contradicts the seven-stage `stages:` list **in the same file**.
2. **`tools/pipeline_completeness.py` renders "the five pipeline stages —
   research → evidence collection → judgment → synthesis → render"** at lines 682-684 and *"The five
   stages at a glance"* at line 694, while `STAGES` at line 37 declares seven with the id `evidence`.
   This is CLAUDE.md §2(b) inside the tool that enforces the spine. **The batch's DB change makes
   `tools/*.html` stale and `pipeline_completeness_fresh` is BLOCKING**, so
   `scripts/regenerate_derived.sh` will re-emit the wrong prose. Pre-existing; not caused by this
   batch; flag it rather than fix it mid-batch.
3. **`insert_source_slug_link` uses `INSERT OR IGNORE`** (`db.py:2034`) — the silent no-op that
   `insert_evidence_source` denounces at length 90 lines earlier (`db.py:1980-1985`). *"One file, one
   diff, two opposite doctrines"* is `log_search`'s own phrasing for this exact class.
4. **`FRAME.md` lists `E-12: identity=MOB · applicability=applies` twice** — a duplicate row in
   `item_taxonomy_links`. Substrate, not this batch's business, but it will inflate any count taken
   off that table.
5. **The per-session DoD run is not a registered check.** `governance/check-registry.yaml` registers
   `research_dod` as `--all` at level **advisory** and `research_dod_selftest` as blocking. Nothing
   in CI runs `--session "$S"`. The batch's definition-of-done is enforced only by the operator.

---

## PHASE 2 — standing by

I will not begin until the batch's rows are sent. I will attack the recorded case through the eight
named lenses of `references/project-standards.md:638` — **existence, fidelity, independence, tier,
population, contrary-finding, recognition by the population served, and query-shape** — recording
each finding as *claim-attacked / method / verdict / severity*, and recording **SURVIVED** claims as
well as SUSTAINED ones, because *"a zero-finding pass must be able to show what it attacked, or it is
indistinguishable from a pass that never ran."*

**I understand and will apply the blind-then-compare mechanic:** for **tier** and
**population-match** I will re-grade every admission independently and write my grades down
**before** looking at the author's, then diff. Send me the rows without the grades if you can; if
the grades are inline, I will grade from the source material first and timestamp my file before
opening yours.

**Budget:** one adversarial pass per research batch. A pass on a pass is forbidden.
