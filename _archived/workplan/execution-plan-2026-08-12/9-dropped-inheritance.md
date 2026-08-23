# Wave 9 — The dropped inheritance

**Read `00-holistic-execution-plan.md` first.** **Precondition: L1 exists.**

Two ratified obligations and one gate that no wave carried. **W9.1 is on the critical path** —
it gates W5.6, which gates W5.1.

---

## W9.1 — The exemption DR that gates W5.6 · **OWNER**

### Objective
Extend DR-2026-05-28's job-owned exemption to `url_verification_runs` **before** W5.6 widens the
blocking reproducibility gate.

### The premise is harder than the plan states
`url_verification_runs` holds **5 rows** in the committed DB, is **created but never populated by
any migration** (`012_baseline` creates it; there is **zero** `INSERT INTO url_verification_runs`
across `scripts/migrations/`), and is **absent from `EXEMPT_TABLES`** at
`scripts/audit/migration_reproducibility.py:65` (which holds only `evidence_source_authors` and
`pipeline_runs`).

**So the widened gate fails immediately on landing — 5 committed vs 0 rebuilt — not "the next
time the cron runs."** The cron is live: `.github/workflows/verify-urls.yml` (bi-weekly,
`permissions: contents: write`, `GUIDEBOOK_DB_PATH: data/guidebook.db`, state-tracking declared
at `:11`, commit message built from the table at `:72-84`); the writer is `scripts/verify_urls.py`
(`:377` CREATE TABLE IF NOT EXISTS, `:429` INSERT OR REPLACE, `:483` UPDATE).

### The gate on the gate
`DR-2026-05-28…:83` — *"Adding a table to the job-owned exemption requires a new DR."* And
`migration_reproducibility.py:22-27` already names `verify-urls.yml` as an authoritative
outside-migrations writer.

### Draft DR

```markdown
# DR-2026-08-XX — Extend the job-owned table exemption to `url_verification_runs`

**Category:** D-OP · **Delegation:** DG-AUTO (executes an owner-set convention;
the convention itself was ratified in DR-2026-05-28)
**Status:** PROPOSED · **Requires:** owner sign-off (DR-2026-05-28 §3 makes
additions to the exemption list DR-gated)

## Decision
`url_verification_runs` is added to the job-owned table exemption list of
DR-2026-05-28 §3, alongside `evidence_source_authors` and `pipeline_runs`.

## Grounds
1. **Same class as `pipeline_runs`.** It is a run log written by a scheduled
   verification job — `scripts/verify_urls.py:377-495`, invoked by
   `.github/workflows/verify-urls.yml` — which commits the result directly:
   exactly the write pattern §3 sanctions. It holds 5 rows, none migration-borne.
2. **Without this exemption, W5.6 manufactures a permanently-red blocking gate.**
   The widened COUNT(*) comparison flags every legitimate cron write as
   irreproducible drift. The exemption must precede the widening.
3. **Staleness note.** The 5 rows, and `pipeline_runs`' 6, report against an
   `evidence_sources` table that is now empty: their counters describe a
   pre-reset corpus of 410 verified URLs and 225 resolved DOIs. The exemption
   sanctions the write pattern; it does not assert the rows are current.

## Execution
- `migration_reproducibility.py:65`: `EXEMPT_TABLES` gains `"url_verification_runs"`
  (the `:54` comment binds the list to this DR).
- `governance/check-registry.yaml`: both `migration_reproducibility` notes name
  three exempt tables, citing this DR.
- CLAUDE.md §4's exempt-table line is corrected on its next scheduled touch
  (derived map, not source of truth).

## Explicitly out of scope
The second candidate in locator-probes §3.1 — `evidence_sources`-by-DOI
enrichment — is NOT decided here. It is a content table, not a run log;
exempting it weakens the reproducibility contract on synthesis-bearing data and
needs its own ruling.

## Reversal
Remove the table from `EXEMPT_TABLES` and this list; any rows then present must
be re-emitted as a data migration, or the gate goes red — which would be the
gate working.
```

**The DR touches `decisions/` — a synthesis path. Doctrine token and attestation owed.**

---

## W9.2 — The frame's two missing vocabularies · **DG-NON-adjacent**

### The obligation, verbatim
`DR-2026-08-06-clean-room-evidence-reset.md:118-123`: the frame has two quarters with no canonical
table, and *"Building those two vocabularies is the first frame work after this reset."*
**No wave item existed. This is it.** Wave-3 class — cheapest while the corpus tables are empty.

### The plan's figures describe the pre-reset corpus, not HEAD

- **Live `jurisdictional_values.jurisdiction` (109 rows) is already clean-coded:** DE 20, GB 20,
  US 20, AU 18, ISO 13, FR 5, NO 5, EU 4, CA/CH/JP/SG 1 each. **No `UK`, no compounds** — but two
  non-country scheme values (`ISO`, `EU`) share the axis.
- **The DR's "UK 88 / GB 5 / GB-SCT 1 plus 12 compounds" is `evidence_sources.jurisdiction` in
  the *archived* corpus.** Re-verified there: `UK` 88, `GB` 5, `GB-SCT` 1, `INT` 174, NULL 79,
  `Multi` 4 — and **8 slash-compounds** (`AU/NZ`, `CA / INT`, `CN/INT`, `EU/UK`, `INT/ZA`,
  `UK/US`, `US/AU/INT`, `US/AU/SE/UK`). **"12 compounds" is not reproducible — it is 8 (+
  `GB-SCT`). REVISED.**
- **Free text still lives today** in `term_aliases.jurisdiction` (2,382 rows: 2,133 NULL, `UK` 7
  vs `US` 5 — **the UK/GB split is alive now**) and `lang_jur_map.jurisdiction` (70 rows, `UK` 1).
  **And one literal `'colloquial'` sits in `term_aliases.jurisdiction` — a mis-fielded value no
  document has recorded.**
- Languages: `term_aliases.language` is lowercase, `lang_jur_map.language` uppercase — the DR's
  casing split.

### DDL

```sql
CREATE TABLE jurisdictions (
    jurisdiction_code TEXT PRIMARY KEY,   -- ISO 3166-1 alpha-2, or 3166-2 ('GB-SCT')
    kind          TEXT NOT NULL CHECK (kind IN
                  ('national','subnational','supranational','standards_body')),
                  -- 'EU' → supranational; 'ISO' → standards_body: keeps the two live
                  -- non-country values without lying about their class
    label         TEXT NOT NULL,
    iso3166       TEXT,                   -- NULL for standards_body
    parent_code   TEXT REFERENCES jurisdictions(jurisdiction_code),  -- GB-SCT → GB
    in_frame      INTEGER NOT NULL DEFAULT 1 CHECK (in_frame IN (0,1)),  -- owner's ruling
    notes         TEXT,
    created_at TEXT NOT NULL, created_by_session TEXT NOT NULL
);
-- Compounds are NOT rows: a multi-jurisdiction source gets one row per
-- jurisdiction in a junction, ending the 'US/AU/SE/UK' class at the schema layer.

CREATE TABLE languages (
    language_code TEXT PRIMARY KEY
                  CHECK (language_code = lower(language_code)),  -- ends the case split
    label_en      TEXT NOT NULL,
    label_native  TEXT,
    in_frame      INTEGER NOT NULL DEFAULT 1 CHECK (in_frame IN (0,1)),
    notes         TEXT,
    created_at TEXT NOT NULL, created_by_session TEXT NOT NULL
);
```

Seed by data migration; add FKs from the free-text columns by table rebuild — **cheapest now
while the big tables are 0 rows.**

**Two things the owner must see:** vocabulary *content* (which jurisdictions are in frame) is
owner-only; and **normalising `UK` → `GB` touches `term_aliases`, 2,382 rows of frame data** —
use the W5.1 natural-key guard pattern, and re-field the `'colloquial'` row first.

**Falsifier:** the owner rules `ISO`/`EU` do not belong on the jurisdiction axis at all — then
`jurisdictional_values` needs a scheme split, a larger change. **Surface before executing.**

---

## W9.3 — The locator-probes Part 4 fix list, re-enumerated

From `workplan/2026-08-09-locator-hierarchy-and-enforcement-probes.md` Part 4 (`:364-386`).
**Five of eight are owner-gated — confirmed** (the register said four; the counting convention is
that item 5's gate is D-SCHEMA-by-class).

| # | Item | Status |
|---|---|---|
| 1 | Exemption ruling | **owner; LIVE** → W9.1. Note Part 4 names *two* candidates; W9.1 deliberately rules only the first |
| 2 | Promote `migration_reproducibility_deep` to blocking | **owner, after (1); LIVE.** Currently advisory. Carry the caveat: deep's volatile classifier once absorbed a real tamper whose only trace was a timestamp |
| 3 | Widen the blocking `COUNT(*)` | **owner, after (1); LIVE** = W5.6 |
| 4 | Pydantic model for `reasoning_doc_citations` | **DONE** |
| 5 | `CHECK` on `verification_status` | **owner (D-SCHEMA); register D4 ruled DEFER. The plan neither carries nor re-opens it — the silent drop is real.** Re-opened here as: propose-with-vocabulary-ratification, or record an explicit DEFER-with-date in the ledger |
| 6 | Correct migration 053's header numbers | **LIVE, ungated** — see below |
| 7 | `EXAMINED:` + fail-on-empty for probes E4/E6/E7 | **LIVE, ungated** |
| 8 | The R3 locator constraint on code values | **owner-DEFERRED**, deliberately, with an anti-academic-default rationale. Keep deferred; record it |

### Item 6, independently re-verified at the DB level
`scripts/migrations/053_locator_hierarchy.sql:22-23` states *"85 rows cite one level, 9 cite two,
3 cite three"* → **97 ≠ 109**. And the diagnosis is worse than an arithmetic slip: **exactly 24 of
109 rows carry a `§` in `standard_name`, so 85 is the count of rows with NO locator.** **The
committed sentence means the opposite of what it says.**

**Fix by follow-on header or DR — never by editing 053.** It is immutable, and §2.1 already
showed such edits are undetectable.

---

## W9.4 — The 23 ledger-only migrations and the hand-maintained cutoff

**Facts:** `data_migrations` = **314 rows**; `scripts/migrations/data_*.sql` = **292 files**;
**23 ledger ids match no file** — confirmed. Sample: `010_fk_integrity_2026-05-13`,
`011_reasoning_doc_citations_2026-05-13`,
`adversarial_research_ndv_aut_rt60_target_absence_2026-05-17`,
`author_a18_rt60_occupied_learning_listening_spaces_2026-05-18`,
`channel_2_url_verification_2026-05-12`, `correct_ref_00561_bettarello_2021_metadata`,
`cutover_evidence_sources_v2_2026-05-11`, `doi_resolution_outcome_backfill_2026-05-12`.

**Note the arithmetic trap: 314 − 292 = 22, not 23.** So either one filename matches a ledger id
it does not correspond to, or one file is unledgered. **The executing session must produce the
exact set-diff in both directions — not the subtraction.**

**The mechanism that makes this survivable:** `migrate_db.py:111`
`BASELINE_DATA_CUTOFF_TS = "20260515000000"` — a hand-maintained constant deciding which ledger
rows `--rebuild` expects files for. All 23 orphans should predate the 2026-05-15 baseline;
**verify each, because an orphan *after* the cutoff would make `--rebuild` and the ledger silently
disagree.**

**The dropped instruction this restores:** the commit-91 review said *"D2 should absorb F11 and
the 23 ledger-only migrations before it is ruled on"* — dropped by both the register and the plan.

**Options for D2:** (a) declare the 23 baseline-absorbed with a one-time DR listing them —
**recommended**; (b) synthesise stub files; (c) leave, with the cutoff documented in the DR.

**Risk:** none, until someone "fixes" the ledger by deleting rows. **The ledger is append-only;
the DR path is the only clean one.**

---

## W9.5 — Run PMP on turning space

### Why this item exists
**It changes D-A's framing.** D-A says *"no code path runs from N values to one."* The correct
finding is that **the Progressive Measurement Protocol exists for exactly this, has zero recorded
walks, and its auditor has no subject.**

### What a run concretely requires
- **The protocol is real** — `workplan/progressive-measurement-protocol.md`, 210 lines, and its
  direction table at `:36-50` **already contains the owner's parameter**: first row *"Turning
  radius / clear floor space | up | larger radius accommodates more devices."*
- **`spec_value_probes` = 0 rows.** Its DDL requires per row: `probe_id`, `walk_id`, `slug` (FK),
  `item_code` (FK), `spec_value_origin REAL NOT NULL`, `spec_unit NOT NULL`,
  `direction CHECK IN ('up','down')`, `population NOT NULL`,
  `claim_type CHECK IN ('minimum','maximum','target','range_low','range_high')`.
- **Three inputs:** **V₀** (the spec value in native units — post-reset there is no BPC value, so
  V₀ must come from a declared source with its class stated), **D = `up`**, and a claim type
  (likely `minimum`).
- **An anchor pair (slug, item_code)**, both FK-enforced. Candidate slugs exist —
  `bariatric-turning-radius-built-environment`,
  `manoeuvring-footprint-vs-turning-radius-methodology`. **Open sub-question: no `items` row names
  turning space.** Nearest are `E-12` and `K-03`. Either the owner accepts E-12 as the anchor, or
  a new item row is added first — **and per Wave H it must be a *category*: "Turning /
  Manoeuvring Space", with no number in the name.**
- **The walk:** outer phase ±20% proportional steps, refinement phase linear δ with bisection
  (`:56-107`), each step a logged search with sources, rows appended per step, a `phase='final'`
  row closing it. **Writes go through migrations.**
- **Wire the auditor.** `scripts/audit/pmp_audit.py` carries C1–C5 flags at `:161-168`. Note the
  Wave-H interaction: **its C1 is "items with numerical specs lacking any walk" — after H1 strips
  numbers from names, "items with numerical specs" must be defined by cells or jurisdictional
  values, not by names.**

### Two dependencies
**W9.5 depends on W7.4-ADOPT** — `db.py log-search` is the admission discipline the walk's search
steps need. And **V₀ selection can smuggle a determination in by the back door — the exact Wave-H
defect.** The ledger entry's I2 walkback must name V₀'s source and class **before the walk
starts.**

---

## W9.6 — DR-2026-08-06 §2's outstanding owner actions · **OWNER-ONLY, both**

**Re-verified read-only:**
- **The archive tag was never created.** `git ls-remote --tags origin` returns **only**
  `phase-a-complete-20260419`.
- **The branch exists** — `archive/pre-reset-corpus-2026-08-06` at
  `4fc6304e908a6441fdb0c0a08ff3d8606c2876c0`, whose commit message is *"governance: delete the
  watcher, fix the dispatcher it was watching [2026-08-06 18:03]"*.
- **It is unprotected** — `main` is the only protected branch of 36 (confirmed via the same API
  call as D-C).

**The owner actions, ready to run:**
```
git tag -a archive/pre-reset-corpus-2026-08-06 4fc6304 \
    -m "pre-reset corpus archive point, DR-2026-08-06 §2" && git push origin --tags
```
or a Settings ruleset protecting `archive/**` from deletion and force-push, which covers both.

**Record completion by a new dated line in the DR — decisions are forward-only, never rewritten.**

**Risk:** an unprotected archive branch is one force-push from silent loss. The in-tree copy at
`_archived/data/corpus-pre-reset-2026-08-06.db` (7.6 MB) mitigates the *data* loss but does not
preserve the *history* the branch holds.

**One housekeeping observation:** the working tree carries
`corpus-pre-reset-2026-08-06.db-shm` and `-wal` sidecar files (the `-wal` is 0 bytes). Harmless,
but **flag whether they were meant to be committed.**

**Falsifier:** the owner rules the in-tree copy sufficient and the ref-level archive redundant —
legitimate, but it must be a **recorded reversal** per the DR's own §5 convention.

---

## Re-derivation notes

| Claim | Status |
|---|---|
| `url_verification_runs` cron-written, 5 rows, absent from the exempt list | **CONFIRMED** |
| W9.1: gate goes red "next time the cron runs" | **REVISED — red immediately**, 5 vs 0 |
| DR-2026-08-06 §4.4's obligation | **CONFIRMED verbatim** at `:118-123` |
| "UK 88 / GB 5 / GB-SCT 1 plus 12 compounds" | **CONFIRMED but relocated** — it is the *archived* `evidence_sources`, not any live table; **and the compounds are 8, not 12** |
| Live `jurisdictional_values.jurisdiction` | **NEW — already clean-coded**; the vocabulary's first customers are `term_aliases` and `lang_jur_map` |
| A `'colloquial'` value in `term_aliases.jurisdiction` | **NEW** — recorded nowhere |
| Locator-probes Part 4 = 8 items, 5 owner-gated | **CONFIRMED** |
| Migration 053's "85/9/3 sums to 97 ≠ 109" | **CONFIRMED — and worse**: 24 of 109 carry `§`, so 85 is the *no-locator* count; the sentence inverts reality |
| `data_migrations` 314 rows, 23 ledger-only | **CONFIRMED** — but 314 − 292 = 22; run the set-diff both ways |
| `BASELINE_DATA_CUTOFF_TS` at `migrate_db.py:111` | **CONFIRMED** |
| PMP direction table contains the owner's parameter; `spec_value_probes` = 0 | **CONFIRMED** |
| No `items` row names turning space | **NEW** — anchor ruling required |
| Archive tag absent; branch at `4fc6304`; unprotected | **ALL CONFIRMED** |
