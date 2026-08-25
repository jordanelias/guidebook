# S1 — RESEARCH STAGE smoke test log

Session: session_2026-08-25-pipeline-smoke-test-mobility
Agent: S1 (research stage)
Repo HEAD: ce33ef60b9d5247f3c2702ada545146c23bee8c5
data/guidebook.db sha256 at start: 30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf (matches expected 30a10669...)
Scratch DB: $SMOKE/s1-research.db (copied from canonical at session start)
Start time (UTC): 2026-08-25 18:16

---

## 1. Framing — mobility items, slugs, ICF/access-need frame

### 1.1 Item → slug status (query: items, slugs)

| item_code | name | bpc_source_slug | slug status |
|---|---|---|---|
| E-08 | Corridor Clear Width (≥1200 mm Minimum on All Primary Routes) | accessible-circulation-geometry | ACTIVE |
| E-11 | Automatic Sliding Entry and Internal Doors | threshold-door-hardware | ACTIVE |
| G-04 | Accessible Bathroom (Wet Room Configuration — Zero Threshold) | accessible-bathroom-and-grab-bar | ACTIVE |
| E-03 | Ramp Gradient (≤1:20 — MS Fatigue and Temporal Accessibility) | stair-ramp-threshold-biomechanics-accessibility | ACTIVE |
| B-08 | Matte, Low-Reflectance Floor Finishes (≤30 Gloss Units) | **NULL — no slug** | n/a |
| C-03 | Pattern Avoidance (Plain Flooring and Walls in Sensitive Environments) | luminance-contrast-lrv-evidence-base | ACTIVE |
| C-05 | Low LRV Differential at Adjacent Floor Materials (DEM Inverse Contrast Rule) | luminance-contrast-lrv-evidence-base | ACTIVE |
| C-06 | Plain, Low-Contrast Flooring Throughout (No Geometric Patterns) | luminance-contrast-lrv-evidence-base | ACTIVE |
| A-05 | Carpet in Corridors and Occupied Spaces (Where VIS Navigation Maintained) | room-acoustic-performance | ACTIVE |
| E-01 | Accessible Lift (1400×1100 mm Car, All Floors Served) | accessible-circulation-geometry | ACTIVE |
| E-04 | Accessible Parking (3600 mm Width, Covered, Closest to Entry) | accessible-circulation-geometry | ACTIVE |

**No `handrail` item exists.** Query `SELECT * FROM items WHERE lower(name) LIKE '%handrail%'` returns
0 rows. The nearest neighbours are `G-03` "Grab Bars in All Accessible Bathrooms" and `I-03`
"Bathroom (UPL Anti-Scald, Bilateral Grab Bars, One-Hand Operation)" — both bathroom-specific,
neither a corridor/stair/ramp handrail item. PROTOCOL's premise is confirmed: **a real mobility
batch cannot cite a handrail item because none exists; one must be created (new item_code under
category E, with a slug) before any handrail-specific evidence can be admitted.**

Note also `B-08` has no `bpc_source_slug` at all (NULL, not merely unresolved) — distinct defect
from "slug exists but STUB": there is no slug row to even check status on.

### 1.2 Item → axis → access_need → ICF frame (codes AND names, per CLAUDE.md §6)

Traced `item_axis_links → axes → access_need_axis_map → access_needs → access_need_icf` for all 12
mobility-relevant items (11 named + G-03 grab bars as the handrail-adjacent item). All resolve.
Representative chain for E-08 (corridor clear width):

- Axes: `AX-AMB` (Ambulant movement, partial) · `AX-BAL` (Balance & postural demand, weak) ·
  `AX-WHM` (Wheeled movement & transfer, full)
- `AX-WHM` → access need `A-REACH` (operating: "Be physically reachable...") and `A-SIZE`
  (environment_safety: "Fit the range of bodies present...") via `spans` relationship
- `AX-BAL` → `A-STABLE` (perceiving: "Hold the visual reference still...handrails...") via `primary`
- `A-REACH` ICF: e120 (confirmed), e150 (confirmed), e155 (confirmed)
- `A-STABLE` ICF: e150 (confirmed), e240 (confirmed)
- `A-SIZE` ICF: e115, e120, e150, e155 (all confirmed)

Full axis set touched by the 11 mobility items: AX-AMB, AX-BAL, AX-WHM, AX-REA, AX-STA, AX-VIS-L,
AX-SPR, AX-AUD, AX-VIS-N — all resolve to named access_needs (A-REACH, A-STABLE, A-SIZE,
A-PRECISION, A-EFFORT, A-NOSIGHT, A-STIMULUS, A-TRIGGER, A-NOSOUND, A-TACTILE) and each need has
`confirmed` ICF `e`-codes (environmental factors) in `access_need_icf`. **CLAUDE.md §6's mandated
frame (codes AND names) is mechanically producible for every mobility item that has a slug** — no
missing links found on this walk.

`AX-BAL`'s own `coverage_status` is `STUB` (the only STUB among the 9 axes touched; the rest are
ESTABLISHED) — worth flagging because balance is directly implicated in handrail research and its
axis is the least-developed one in the frame.

### 1.3 item_population_links — NOT the zero-row pre-synthesis state CLAUDE.md §6 describes

CLAUDE.md §6 says "Zero `item_population_links` on a slug is the correct pre-synthesis state, not
a defect" for slugs pending synthesis. In fact every one of the 11 named mobility items already
carries multiple populated `item_population_links` rows (MOB, BLIND, DEM, SCI, DEAF, BAR, MS, LPA,
DEAFBLIND, BRAIN, VES, COM, LMB, PAIN, AUT, NDV, MH — 5-13 populations per item, mix of `applies`
and `context_dependent`). This is not a contradiction of the ruling (which describes the
*permitted* zero state, not a mandated one) but it does mean **this slug set is past the "zero
pre-synthesis" state already** — these links pre-exist any synthesis this smoke test would run,
so a real batch here is adding evidence against an already-populated population frame, not
establishing one from scratch.

**FINDING (framing): PASS with one BLOCKING gap.** The ICF/access-need/axis frame is fully
mechanical and correct for 11 of the mobility items. The batch as scoped in PROTOCOL.md names
"handrails" as a subject and **no item_code exists for it** — this blocks framing a handrail
sub-batch entirely until an item is created. B-08's missing slug is a second, smaller gap (blocks
sourcing for that one item only, not the whole batch).

## 2. The clue store (`source_locators`, 875 rows) as batch driver

### 2.1 What it actually contains — column population census (canonical DB, read-only)

Query: `SELECT COUNT(*) FROM source_locators WHERE <col> IS NOT NULL AND <col> != ''` per column,
875 total rows.

| column | populated | % |
|---|---|---|
| doi | 448 | 51% |
| url | 396 | 45% |
| pmid | 129 | 15% |
| pmcid | 30 | 3% |
| isbn | 20 | 2% |
| issn | 295 | 34% |
| standard_number | 313 | 36% |
| doi_resolution_outcome | 415 | 47% |
| url_resolution_outcome | 71 | 8% |
| url_last_fetched | 52 | 6% |
| authors | 531 | 61% |
| pub_year | 531 | 61% |
| title | 531 | 61% (344 rows have NO title) |
| tier_claimed | 531 | 61% |
| jurisdiction | 490 | 56% (385 NULL) |
| used_in_bpcs | 56 | 6% |
| notes | 531 | 61% |

`status` is uniform: all 875 rows are `REFERENCE-ONLY` (none `PROMOTED`, none `RETIRED`).
`recovered_from`: 835 `corpus-pre-reset-2026-08-06`, 32 `references/global-reference-registry.md`,
8 `global-reference-registry.json` — this table is entirely backfill from a pre-reset corpus and a
registry dump, not something any live research session wrote a row into (no row's
`recovered_from` names a session).

**FINDING (LOCATION `source_locators.jurisdiction`): the jurisdiction column is not a clean
filterable field.** Distribution over all 875 rows:

| shape | count |
|---|---|
| NULL | 385 |
| `—` (em-dash placeholder) | 89 |
| clean 2–3 letter code (`^[A-Z]{2,3}$`) | 56 |
| URL string | 154 |
| other free-text/prose (findings, warnings, framework names, quantified claims) | 191 |

Of the 56 clean-code rows, the codes used are `INT`(26) `US`(15) `UK`(5) `NL`(4) `AU`(2) `NO`(1)
`IT`(1) `IN`(1) `NZ`(1) — an ad hoc set that does not match either the bucket-1 vocabulary in
PROTOCOL.md (UN/ISO/Canada/USA/UK/Germany/Norway/Sweden/Japan/Australia) or bucket-2
(EU/Singapore/New Zealand/Ireland/France/Spain/Portugal/Finland/Netherlands/South Korea) —
e.g. "US" vs "USA", "UK" present but no "Germany"/"Canada"/"Japan"/"Sweden" rows exist at all in
the clean set. Free text observed in the 191 "other" bucket includes verification flags
(`⚠ verify`, `[GREY — DOI required]`), quantified findings (`2cm threshold defeats 45.8%`),
theory names (`Restorative environment theory`), and cross-references (`See RET-14`) — this column
is being used as a general annotation field, not a jurisdiction tag, for roughly 44% of rows that
have anything in it at all.

By contrast `lang_jur_map` (70 rows, schema `language, jurisdiction, role, notes`) uses a clean
closed vocabulary of real ISO-ish 2-letter country codes (AR, AT, AU, BD, BE, BR, CA, CH, CL, CN,
CO, CR, DE, DK, ...). **There is no FK from `source_locators.jurisdiction` to
`lang_jur_map.jurisdiction`** (confirmed: `source_locators`'s CREATE TABLE has zero `REFERENCES`
clauses) — the clean vocabulary exists in the DB but is not enforced on the clue store.

### 2.2 Mobility relevance of the clue store

`used_in_bpcs` (populated on only 56/875 rows) is a free-text slug list, checked by substring
match against the 6 mobility slugs found in §1.1:

| slug | rows referencing it in `used_in_bpcs` |
|---|---|
| accessible-circulation-geometry | 2 |
| threshold-door-hardware | 1 |
| accessible-bathroom-and-grab-bar | 2 |
| stair-ramp-threshold-biomechanics-accessibility | **0** |
| luminance-contrast-lrv-evidence-base | **0** |
| room-acoustic-performance | 17 |

Rows carrying BOTH a clean jurisdiction code AND a mobility-slug tag in `used_in_bpcs`: **22 of
875** (2.5%), and 17 of those 22 are `room-acoustic-performance` (A-05's slug, arguably peripheral
to core mobility) rather than circulation/door/ramp/contrast. **Zero clue-store rows are jointly
jurisdiction-tagged and slug-tagged to the ramp/threshold-biomechanics or luminance-contrast
slugs** — for those two slugs the clue store currently offers nothing a jurisdiction-bucket filter
could find.

Title-keyword proxy search (344/875 rows have no title at all, so this undercounts): "door" 28,
"wheelchair" 13, "threshold" 8, "ramp" 5, "mobility" 5, "floor" 4, "stair" 2, "lift" 2,
**"handrail" 0, "corridor" 0, "elevator" 0, "parking" 0, "flooring" 0**.

### 2.3 Is there a tool to *select* leads for a batch?

`grep -n "def \|add_parser" scripts/db.py` shows subcommands touching `source_locators`: only
`add-locator` (write) exists. **No `list-locators`/`query-locators`/`select-locators` subcommand
exists anywhere in `scripts/db.py`.** The only callers of `source_locators` outside `db.py` and
`dbcore.py` are migrations (write-once, historical) and
`scripts/audit/validate_pydantic_schemas.py` / `scripts/audit/research_batch_dod.py` (both audit,
not selection) and two skill docs (`citation-miner_SKILL.md`, `research-log-manager_SKILL.md`),
neither of which is an executable selector.

**FINDING: ABSENT.** There is no mechanical way to select "mobility-relevant, bucket-1/2
jurisdiction leads" from the clue store — every count above required hand-written ad hoc SQL run
directly against the read-only canonical DB in this smoke test. The nearest existing surface is
`db.py add-locator` (write-only) plus raw `sqlite3`/Python queries. What would have to exist: a
`db.py list-locators --used-in-bpc <slug> --jurisdiction-bucket <1|2>` (or equivalent) read path,
and — prior to that — a cleanup/migration that stops the `jurisdiction` column doubling as a notes
field, or a separate clean jurisdiction column. Left unenforced: the **research** stage's own
"driver" role for the clue store (PROTOCOL.md: "the clue store, source_locators ... Driver") has
no mechanical support; a real batch would fall back to hand SQL against source_locators, which
CLAUDE.md's write-path section says should not happen for *writes* but does not prohibit for
*reads* — reads have no CLI path to avoid at all here.

### 2.4 `db.py add-locator` — exercised on scratch (`$SMOKE/s1-research.db`)

### 2.1 valid write
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s1-research.db python3 scripts/db.py add-locator --ref-id REF-00971 --title "Handrail grip diameter and fall arrest: a biomechanical review" --doi "10.9999/smoketest-s1-handrail" --pub-year 2021 --authors "Smoketest, A." --tier-claimed 2 --recovered-from "smoke-test-s1" --status REFERENCE-ONLY --used-in-bpcs "stair-ramp-threshold-biomechanics-accessibility" --session session_2026-08-25-pipeline-smoke-test-mobility`
STAGE     : research
EXIT      : 0   RUNTIME: <1s
READS     : scripts/db.py:899-909 (arg parser), scripts/db.py:2489-2531 (insert_locator), scripts/dbcore.py next_ref_id/check_vocab/stamp_for
WRITES    : $SMOKE/s1-research.db → source_locators.ref_id='REF-00971' (1 row)
EXAMINED  : 1 (the ref_id under write; insert_locator does a targeted duplicate/DOI lookup, not a table scan)
OUTPUT    : `{"ref_id": "REF-00971", "dry_run": false}`
FINDING   : PASS
LOCATION  : scripts/db.py:2489 insert_locator
NOTE      : add-locator works cleanly for a well-formed lead with a minted ref_id.

### 2.2 refusal — duplicate ref_id (identity collision)
INVOKED   : same command, `--ref-id REF-00971` again (already exists), different title/url
EXIT      : 1
OUTPUT    : `ValueError: REF-00971 already exists in source_locators. Use update-locator.`
FINDING   : PASS (correct refusal)
LOCATION  : scripts/db.py:2504
NOTE      : No `update-locator` subcommand actually exists in `scripts/db.py` (checked: only
  `add-locator` is registered) — the refusal message names a command that is ABSENT. A caller who
  hits this refusal and follows the instruction literally will fail a second time.

### 2.3 refusal — bad vocabulary (status)
INVOKED   : `--ref-id REF-00972 --status "UNVERIFIED"` (a valid value of a *different* column, `search_candidates.locator_status`, not of `source_locators.status`)
EXIT      : 1
OUTPUT    : `ValueError: insert_locator: source_locators.status does not accept 'UNVERIFIED'. The schema's own CHECK declares: ['PROMOTED', 'REFERENCE-ONLY', 'RETIRED']. Nothing was written.`
FINDING   : PASS
LOCATION  : scripts/dbcore.py:308 check_vocab → scripts/dbcore.py:272 check_values (reads the CHECK from sqlite_master, per CLAUDE.md §4's "vocabularies come from the schema" rule)
NOTE      : Refusal correctly names the schema-declared alternative set rather than a live-row sample.

### 2.4 refusal — duplicate identity via DOI (R9, case-folded)
INVOKED   : `--ref-id REF-00972 --doi "10.9999/SMOKETEST-S1-HANDRAIL"` (same DOI as 2.1's REF-00971, different case)
EXIT      : 1
OUTPUT    : `ValueError: DOI '10.9999/SMOKETEST-S1-HANDRAIL' is already held as REF-00971 in source_locators. R9: cross-file the existing ref_id, never mint a second identity for one source. Nothing was written.`
FINDING   : PASS
LOCATION  : scripts/db.py:2510-2521 (checks both source_locators and evidence_sources, case-folded via LOWER(TRIM(doi)))
NOTE      : Confirms the R9 duplicate-DOI refusal works at write time for `source_locators` itself
  — this is a *different* mechanism from the R9 duplicate **gate** (a post-hoc audit script) that
  CLAUDE.md §4/OD-5 says cannot see `source_locators`. See §10 of this log for that gate
  specifically; this write-time check is not the gate in question and does catch the case tested.

### 2.5 refusal — bad ref_id shape
INVOKED   : `--ref-id "RAP-04"` (a per-slug local label, not a global ref id)
EXIT      : 1
OUTPUT    : `ValueError: --ref-id 'RAP-04' is not a global reference id. Expected REF-NNNNN (or REF-VERIFIED-NNN / Co1-NN). Mint with dbcore.next_ref_id().`
FINDING   : PASS
LOCATION  : scripts/db.py:2497-2500; pattern scripts/dbcore.py:175 REF_ID_SHAPE
NOTE      : none

### 2.6 refusal — CHECK constraint, no identifier at all (R3-adjacent)
INVOKED   : `--ref-id REF-00972` with no doi/url/pmid/pmcid/isbn/issn/standard-number/title
EXIT      : 1
OUTPUT    : `sqlite3.IntegrityError: CHECK constraint failed: doi IS NOT NULL OR url IS NOT NULL OR pmid IS NOT NULL OR pmcid IS NOT NULL OR isbn IS NOT NULL OR issn IS NOT NULL OR standard_number IS NOT NULL OR title IS NOT NULL`
FINDING   : PASS, but the refusal is a raw SQLite traceback, not a curated ValueError like the other four.
LOCATION  : source_locators table CHECK (schema); surfaces via scripts/db.py:2529 conn.execute (uncaught)
NOTE      : Minor polish gap — `insert_locator` does not pre-validate "at least one identifier
  present" the way it pre-validates status/DOI/shape; it lets SQLite's own CHECK fail and leaks a
  bare IntegrityError with column-list SQL text instead of a `context: table.column` message in
  the house style of the other four refusals. Not blocking (it does refuse correctly) but
  inconsistent — LOCATION: scripts/db.py insert_locator (no pre-check before the final INSERT at
  line 2529).

### 2.7 no-FK-refusal case: source_locators has no FK columns to test
NOTE      : `source_locators`'s CREATE TABLE (read from sqlite_master) declares zero `REFERENCES`
  clauses on any column — `recovered_from`, `used_in_bpcs`, `jurisdiction` etc. are all free TEXT.
  There is therefore no "bad FK" refusal to trigger on this table; PROTOCOL's instruction to
  "trigger every refusal you can (bad FK, bad vocabulary, duplicate identity, missing R3 locator)"
  is only partially applicable to `add-locator` — bad-FK is N/A for this specific table by design
  (it is a lead index, not a table anchored to items/populations). The R3 "missing locator on a
  quantified value" refusal lives on `add-jurisdictional-value` (scripts/db.py:2383-2396), not on
  `add-locator` — tested separately would require that subcommand, out of scope for the clue-store
  write path itself; noted here rather than fabricated against the wrong command.
FINDING   : ABSENT (bad-FK case does not exist for this table — correctly so)

### 2.8 `dbcore.next_ref_id` — union high-water-mark behaviour
INVOKED   : `dbcore.next_ref_id(conn)` against scratch DB, compared with independent MAX queries over `source_locators` and `evidence_sources` separately
OUTPUT    :
```
next_ref_id: REF-00971
MAX(ref_id) in source_locators : 964
MAX(ref_id) in evidence_sources: 970
```
FINDING   : PASS
LOCATION  : scripts/dbcore.py:175-224 (ref_id_high_water / next_ref_id)
NOTE      : Confirms CLAUDE.md §4's claim exactly: source_locators tops out at REF-00964,
  evidence_sources at REF-00970, and next_ref_id correctly returns REF-00971 (970+1), not
  REF-00965 (964+1) — the union rule is real and matches the file's own worked numbers.

## 3. Search logging (R8) — `log-search`, `coverage`, frozen `upsert-*`

### 3.1 `upsert-coverage` / `upsert-language` are FROZEN write paths
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s1-research.db python3 scripts/db.py upsert-coverage --slug stair-ramp-threshold-biomechanics-accessibility --jurisdiction US --status SEARCHED --session session_...` (and the `upsert-language` equivalent)
EXIT      : 2 for both
OUTPUT    : `search_coverage is FROZEN as a historical artifact and no longer accepts writes.` /
  `search_languages is FROZEN as a historical artifact and no longer accepts writes.` — both point
  the caller at `log-search` and `workplan/search-coverage-completion-workplan.md`.
FINDING   : PASS (this is a correct, deliberate refusal — the tables are dead write paths by
  design; `SELECT COUNT(*) FROM search_coverage`/`search_languages` on the canonical DB show 0
  rows written since the freeze). PROTOCOL.md's task list names `upsert-coverage`/`upsert-language`
  alongside `log-search` as things to exercise; both do exist as subcommands but both refuse on
  purpose. Not a defect — the task instruction is simply out of date relative to the repo.
LOCATION  : scripts/db.py:290-330ish (freeze docstring + guard), redirect message text at ~line 300-319
NOTE      : `log-search` is the sole live write path for R8, confirmed.

### 3.2 `log-search` — real mobility query, zero-yield, logged verbatim
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s1-research.db python3 scripts/db.py log-search --slug stair-ramp-threshold-biomechanics-accessibility --language EN --query-text 'handrail diameter grip biomechanics fall arrest wheelchair ramp' --engine crossref --depth-method scoping --session session_2026-08-25-pipeline-smoke-test-mobility --jurisdiction US --target-tier 1 --target-evidence-type clinical --results-found 0 --results-screened 0 --results-admitted 0 --saturation-signal none --findings-note "..." --deferred-reason ""`
EXIT      : 0
WRITES    : search_executions.exec_id=29 (slug=stair-ramp-threshold-biomechanics-accessibility, jurisdiction=US, language=EN, results_found=0, deferred_reason='' [empty string, NOT NULL])
EXAMINED  : 1
OUTPUT    : `{"exec_id": 29, "slug": "...", "admitted": 0, "dry_run": false}`
FINDING   : PASS with a defect discovered as a side effect (see 3.3)
LOCATION  : scripts/db.py:336 log_search
NOTE      : R8's "keep the empties" requirement is mechanically honoured — a zero-yield,
  well-formed query becomes a row rather than being discarded.

### 3.3 DEFECT found via own usage — `--deferred-reason ""` (empty string) silently miscounts as deferred
By passing `--deferred-reason ""` explicitly (rather than omitting the flag) on 3.2's call, the
column was written as `''`, not `NULL`. `get_coverage_completeness()` (scripts/db.py:520-571) and
its callers filter with `deferred_reason IS NULL` / `IS NOT NULL` — SQLite's `IS NOT NULL` is TRUE
for `''`, so exec_id 29 was silently excluded from `jurisdictions_searched`/`languages_searched`
and counted in `searches_deferred_with_reason`, even though it was a real, executed, zero-yield
search with a genuine jurisdiction and query. Confirmed by direct query:
```
exec_id=29: deferred_reason='' , (deferred_reason IS NULL)=0, results_found=0, jurisdiction='US'
```
and by contrast: a second, otherwise-identical search logged **without** passing `--deferred-reason`
at all (exec_id 30) correctly raised `jurisdictions_searched` from 0 to 1.

FINDING   : FAIL (latent defect, low severity but real)
LOCATION  : scripts/db.py:336-410 `log_search` (no normalisation of `deferred_reason` — accepts
  `''` uncoerced) and scripts/db.py:520-571 `get_coverage_completeness` (uses `IS NULL`/`IS NOT
  NULL`, which does not treat `''` as absent). Also affects `scripts/audit/research_batch_dod.py`
  R6/R14 checks at lines ~387-395 and ~583-597, which use the identical `IS NULL`/`IS NOT NULL`
  predicate.
NOTE      : Low practical risk if every caller remembers to omit rather than empty-string the flag,
  but the CLI does not enforce that, and a scripted/wrapped caller (a skill script, a batch runner)
  that always passes `--deferred-reason "$X"` with `$X` sometimes empty would silently corrupt
  jurisdiction/language coverage counts for a real, completed search — exactly the "prose that
  contradicts the database" failure mode CLAUDE.md §2(b) is about, except the corruption originates
  in the write path itself rather than in a report. Cheap fix: `log_search` should coerce
  `deferred_reason=""` to `None` before writing (one line), matching the CHECK-vocab discipline
  already applied elsewhere in this file.

### 3.4 R14's three-way distinction (query-shape failure / wrong index / genuine absence) — schema support
`search_executions.findings_note` is free TEXT with no CHECK constraint and no companion
enum column. `scripts/audit/research_batch_dod.py` R14 (lines ~583-597) enforces only:
`results_found=0 AND deferred_reason IS NULL AND COALESCE(findings_note,'')=''` → FAIL. **It does
not parse or classify the content of `findings_note`** — any non-empty string satisfies R14,
including a string that says nothing about which of the three causes applies.

FINDING   : ABSENT (partial) — the distinction is EXPRESSIBLE (I wrote it into `findings_note` by
  hand in 3.2: "Query shape suspect... Not yet a genuine-absence claim...") but not STRUCTURED or
  MECHANICALLY VERIFIED. Nothing in the schema or the gate can tell "I searched broadly across two
  major indices and found nothing" (genuine-absence-leaning) apart from "this one narrow query in
  one engine returned nothing" (query-shape-leaning) apart from "I searched the wrong database for
  this evidence type" (wrong-index) except by a human re-reading free prose.
LOCATION  : table.column `search_executions.findings_note` (schema: scripts/migrations, no CHECK);
  gate: scripts/audit/research_batch_dod.py:583-597 (non-emptiness only)
NOTE      : What would have to exist for real mechanical support: either (a) an enum column
  `zero_yield_cause TEXT CHECK (... IN ('query_shape','wrong_index','genuine_absence'))` alongside
  `findings_note`, or (b) a battery of paired rows the gate could check for (e.g. a genuine-absence
  claim requires ≥2 `search_executions` rows for the same slug+item with `saturation_signal IN
  ('partial','saturated')` and different `engine` values before `findings_note` may assert absence)
  — this smoke test found no such requirement enforced anywhere. R14, as implemented, is a
  "did you write something" gate, not a "did you establish what you're claiming" gate. This is
  exactly the shape of failure mode (a) in CLAUDE.md §2 (a gate passing having examined the
  presence of text, not its truth) generalised from citations to search logs.

### 3.5 legitimate `--deferred-reason` use (control case)
INVOKED   : `log-search --slug stair-ramp-threshold-biomechanics-accessibility --language KO --jurisdiction KR --deferred-reason "Smoke test S1: deliberately not run..."` (query-text a placeholder, no results fields)
EXIT      : 0
WRITES    : search_executions.exec_id=31, deferred_reason NOT NULL/NOT empty
FINDING   : PASS
LOCATION  : scripts/db.py:336
NOTE      : Confirms the legitimate "deliberately not searched" path works and is distinct in kind
  from 3.3's accidental-empty-string case (this row has real prose in deferred_reason).

### 3.6 `coverage` read command
INVOKED   : `python3 scripts/db.py coverage --slug stair-ramp-threshold-biomechanics-accessibility` (before and after the 3.3 correction)
EXIT      : 0
OUTPUT (after correction, exec_id 30 added): `{"jurisdictions_searched": 1, "jurisdictions_required": 48, "languages_searched": 1, "languages_required": 19, "searches_deferred_with_reason": 1, "complete": false, "legacy_grid": {"jurisdictions": 0, "languages": 0, ...}}`
EXAMINED  : 3 rows in search_executions for this slug (29, 30, 31) at read time
FINDING   : PASS — `jurisdictions_required`/`languages_required` are correctly derived from
  `lang_jur_map` (48 jurisdictions, 19 languages), not hardcoded, matching CLAUDE.md's general
  "derive volatile facts" rule and the code's own comment about a prior 24-vs-48 hardcode bug.
LOCATION  : scripts/db.py:520-571
NOTE      : `legacy_grid` correctly reports 0/0 for this slug and is clearly labelled as unusable —
  good design, no defect.

## 4. Screening / staging — `add-candidate` (search_candidates), R7/R15

### 4.1 disposition vocabulary: schema CHECK vs live rows (CLAUDE.md §4's own worked example, re-verified)
INVOKED   : `dbcore.check_values(conn, 'search_candidates', 'disposition')` vs `dbcore.live_vocab(conn, 'search_candidates', 'disposition')` against canonical DB (read-only) and scratch
OUTPUT    :
```
canonical search_candidates rows: 60
disposition distribution: ADMITTED=1, MISCELLANEOUS=1, PENDING-VERIFICATION=55, REHOME=3
check_values (schema CHECK)  = {PENDING-VERIFICATION, REHOME, OUT-OF-SCOPE, ADMITTED, MISCELLANEOUS}
live_vocab   (sample of rows) = {PENDING-VERIFICATION, REHOME, ADMITTED, MISCELLANEOUS}   # no OUT-OF-SCOPE
```
FINDING   : PASS
LOCATION  : scripts/dbcore.py:272 check_values, :281 live_vocab, :308 check_vocab (uses check_values, not live_vocab)
NOTE      : Independently reproduces CLAUDE.md §4's claim exactly — `OUT-OF-SCOPE` is declared in
  the CHECK and unused in all 60 live rows. `check_vocab` (what `insert_search_candidate` actually
  calls) is schema-sourced, so it does NOT wrongly refuse `OUT-OF-SCOPE` — confirmed positively in 4.2.

### 4.2 add-candidate — valid writes (scratch)
INVOKED   : `add-candidate --exec-id 30 --found-under-slug stair-ramp-threshold-biomechanics-accessibility --disposition PENDING-VERIFICATION --title "Handrail diameter and grip force in older adults: a laboratory study" --locator "10.9999/smoketest-handrail-grip" --locator-status UNVERIFIED --tier-guess 1 --why-not-admitted "..." --session ...`
EXIT      : 0 → candidate_id=61
INVOKED   : same shape, `--disposition OUT-OF-SCOPE --title "Handrail marketing brochure..." --why-not-admitted "Commercial marketing material, not evidence..."`
EXIT      : 0 → candidate_id=62
FINDING   : PASS (both)
LOCATION  : scripts/db.py:2263 insert_search_candidate
NOTE      : `OUT-OF-SCOPE` writes successfully — the schema-CHECK-based refusal is correct and a
  live-row-sample-based refusal (which CLAUDE.md warns against) would have wrongly blocked this.

### 4.3 R15 mechanical support — confirmed real, not aspirational
INVOKED   : `add-candidate --disposition ADMITTED --locator-status UNVERIFIED ...` (premature admission)
EXIT      : 1
OUTPUT    : `ValueError: disposition=ADMITTED requires locator_status=RESOLVED. R15: a staged candidate description is a hypothesis, and admitting one whose locator was never resolved is how a guess becomes a fact.`
INVOKED   : same, `--locator-status RESOLVED` (correct path)
EXIT      : 0 → candidate_id=63
FINDING   : PASS
LOCATION  : scripts/db.py:2290-2294
NOTE      : R15 ("re-describe a hypothesis on resolution") has real, tested, working mechanical
  support at write time — this is not merely documented, it refuses.

### 4.4 further refusals exercised
- Bad disposition value `MAYBE` → `ValueError: ... does not accept 'MAYBE'. The schema's own CHECK declares: ['ADMITTED', 'MISCELLANEOUS', 'OUT-OF-SCOPE', 'PENDING-VERIFICATION', 'REHOME']` — EXIT 1, PASS. LOCATION scripts/dbcore.py:308.
- Bad `--exec-id 999999` (not a live search_executions row) → `ValueError: exec_id 999999 is not a live search_executions row. A candidate is something a SEARCH surfaced; log the search first...` — EXIT 1, PASS. LOCATION scripts/db.py:2273-2277. Named, not a bare FK error — good.
- Bad `--found-under-slug nonexistent-slug-xyz` → `ValueError: found_under_slug 'nonexistent-slug-xyz' is not in \`slugs\`.` — EXIT 1, PASS. LOCATION scripts/db.py:2278-2280.

EXAMINED (candidate-vocab check overall): 60 live rows read for the live_vocab comparison, 5
distinct add-candidate invocations against scratch DB, all producing the expected result.
FINDING (section overall): PASS — this is the cleanest-tested surface in the research stage so
far; every refusal PROTOCOL asked for (bad vocab, bad FK, R15 mechanism) is real and gives a
named, actionable error, not a bare traceback.

## 5. Citation mining — the headline test

### 5.0 Context that changes the reading of everything below
`SELECT COUNT(*) FROM evidence_sources` on the **canonical** DB = **10**. `SELECT COUNT(*) FROM
source_slug_links` = **10**, and every single one is `slug='room-acoustic-performance'`. **Zero**
evidence sources exist for ANY of the 6 mobility slugs identified in §1 — confirmed by
`SELECT COUNT(*) FROM source_slug_links WHERE slug IN (...)` = 0 for all five distinct mobility
slugs checked. `citation_mining` (10 rows) is entirely `room-acoustic-performance` too — a
mobility citation-mining test on **real** data is not possible; every mechanic below except 5.0
itself had to be exercised against either (a) the pre-existing room-acoustic-performance rows
(read-only) or (b) one synthetic `evidence_sources` row I filed on the scratch DB, clearly titled
`SMOKE-TEST SYNTHETIC ROW`, so `log-mining`/`is-mined` had something real to key on. **This alone
is close to the largest finding in this whole log: the mobility batch starts from a definitionally
empty evidence base, with citation mining having never been run on it once.**

### 5.1 Is there an executable retriever for backward mining (reference list) or forward mining (citing works)?
`find scripts -iname '*crossref*' -o -iname '*semanticscholar*' -o -iname '*citation*' -o -iname
'*openalex*'` returns only `scripts/audit/citation_mining_completeness.py` (an audit, not a
retriever) and `scripts/audit/reasoning_doc_citations_audit.py` (unrelated — audits reasoning-doc
citation hygiene, not evidence citations). `grep -rl 'api.crossref.org\|semanticscholar.org\|api
.openalex.org' scripts/ skills/` returns only `skills/citation-miner_SKILL.md` and
`skills/gap-driven-mining_SKILL.md` — **prose instructions telling a human/agent to call
`web_fetch` against those URLs by hand**, not a client. `scripts/resolve_dois.py` exists but does
DOI *resolution/verification* (PMID→DOI, title/author matching against CrossRef to confirm a
source's own identity) — it does not retrieve a reference list or a citing-works list for an
anchor.

**FINDING: ABSENT.** `citation_mining` (the table) IS what `skills/citation-miner_SKILL.md` §1/§2
say it is: **a hand-filled ledger of work done elsewhere** (via the general-purpose `WebFetch`/
`WebSearch` tools, narrated in `notes`), not the output of any executable retriever. Confirmed by
reading the 10 live rows: `notes` contains prose like *"Backward mining run via Crossref: 108
references listed, 64 carrying a DOI"* — a first-person narration of a manual fetch-and-read pass,
not a machine-generated log. `connections_produced` holds a raw JSON array of **DOI strings only**
(no titles, years, or verification status) — these are described in the same rows' own notes as
**not yet verified or admitted** ("NOT harvested into source_locators: section 6 widening is OD-5
and still open" — RAP-02/RAP-04; "5 cited DOIs are already held... FOUR are unconsumed
source_locators leads invisible to R9" — RAP-08).

**What would have to exist:** a small retrieval client — e.g. `scripts/research/crossref_client.py`
hitting `api.crossref.org/works/{doi}` for `.message.reference[]` (backward) and
`scripts/research/semantic_scholar_client.py` hitting
`api.semanticscholar.org/graph/v1/paper/DOI:{doi}/citations` (forward) — that writes its raw
output through `scripts/research/retrieval_log.py` (§7 below) BEFORE any human curation, the same
way `--verify-authors` works for bibliographic fields. **Stage left unenforced without this:**
`research` itself — R2's depth-2/3 requirement and the backward/forward split are currently
enforced only by a human remembering to do the fetch and being honest in `notes`; nothing catches
a session that skips forward mining and writes `forward=1` anyway (the CHECK on
`citation_mining.forward` only constrains it to 0/1, not to truth).

### 5.2 `citation_mining` table — what the 10 live rows actually record
Columns: `slug, local_ref_id, global_ref_id, doi, backward, forward, connections_produced, notes,
created_at, created_by_session, updated_at, updated_by_session, deferred_reason`. All 10 rows are
`room-acoustic-performance`. Direction coverage: 7 rows have `backward=1,forward=1` (RAP-01/02/03
/05/07/08... — full pairs), 3 rows (`RAP-F61/F69/F70`) have `backward=0,forward=1` with notes
*"BACKWARD mining still OWED for this anchor (R2)"* — i.e. **known, self-declared incomplete
mining**, honestly logged rather than hidden. `connections_produced` sizes range from `[]` (2 rows,
one honestly explained as *"cited-by is 0 because the paper is 2026 and has not accumulated
citations... Recorded so a later pass does not read the empty forward result as a defect"* — a
good example of R14-style absence-vs-not-yet discipline actually working in prose) up to 39 DOIs
(RAP-02). Two rows carry a `ROW RE-KEYED 2026-08-22` note documenting the exact
local-vs-global-ref-id drift bug CLAUDE.md's citation-miner-skill excerpt (§1 INLINE mode) warns
about — the drift happened once, was caught, and is now fixed in `db.py:201` per the skill's own
correction note, confirmed by reading the code (§0 above, `log_mining` docstring).

### 5.3 mechanical exercise (scratch DB)
INVOKED   : `add-source --ref-id REF-00972 ... --slug stair-ramp-threshold-biomechanics-accessibility --local-ref-id SMK-01 --session ...` (synthetic row, evidence-collection-stage table, used only to give citation_mining a real FK to key on — noted as a stage boundary crossing, necessary because the research-stage table depends on an evidence-collection-stage table having ≥1 row)
EXIT      : 0 → `{"ref_id": "REF-00972", "linked_slug": "stair-ramp-threshold-biomechanics-accessibility"}`

INVOKED   : `is-mined --slug stair-ramp-threshold-biomechanics-accessibility --ref REF-00972` (before)
OUTPUT    : `{"mined": false}`
FINDING   : PASS

INVOKED   : `log-mining --slug ... --ref REF-00972 --direction backward --connections '[]' --session ...`
EXIT      : 0 → `{"logged": true}`

INVOKED   : `is-mined ...` (after backward only)
OUTPUT    : `{"backward": 1, "forward": 0, "connections_produced": "[]"}`
FINDING   : PASS — correctly reports partial-mining state

INVOKED   : `log-mining --direction forward ...` then bad-direction test `--direction sideways`
EXIT      : 0 then 2 (argparse `choices` rejects it before reaching the DB layer)
OUTPUT    : `db.py log-mining: error: argument --direction: invalid choice: 'sideways' (choose from 'backward', 'forward')`
FINDING   : PASS

INVOKED   : `unmined --tier-max 3` (global, scratch)
OUTPUT    : lists the synthetic SMK-01 row (now fully mined, backward=1 forward=1 — so it
  should NOT appear as unmined; **checked — it correctly does not appear** in the head-40 output,
  which instead shows RAP-06/RAP-09/RAP-10, the genuinely-partial rows) — confirmed by re-reading
  the full output, not just the head.
EXAMINED  : 7 slug-linked Tier 1-3 sources (scratch DB total)
FINDING   : PASS

NOTE (5.3 overall): every `db.py` mechanic asked for in PROTOCOL — `log-mining`, `is-mined`,
`unmined` — works correctly and the direction/state bookkeeping (backward vs forward, partial vs
complete) is accurate. **The defect is not in this bookkeeping layer; it is that nothing upstream
of it can retrieve a real reference list or citing-works list (5.1), and that zero mobility rows
exist to book anything about (5.0).**

### 5.4 `gaps` / `gap_mining` / `unmined-gaps` / `add-gap-mining` / `update-gap-addressability`
Canonical DB: `gaps` = 5 rows, ALL `section='room-acoustic-performance'` — **zero gaps recorded
for any mobility slug**, consistent with 5.0. `gap_mining` = **0 rows** on the canonical DB (never
used yet, though the table and its five-outcome CHECK vocabulary, the closure-needs-discoveries
integrity CHECK, and the ≥20/≥10-char CHECKs on `gap_recategorized`/`deferred` notes are all live
and enforced — confirmed by table DDL).

DEFECT — `next_gap_id()` / `db.py next-id gaps` disagrees with the live naming convention:
INVOKED   : `python3 scripts/db.py next-id gaps` (scratch, before any write)
OUTPUT    : `{"next_id": "GAP-001"}`
All 5 live gap_ids are `GAP-B01-001, GAP-B01-002, GAP-B01-003, GAP-B01-004, GAP-B02-001` — a
batch-scoped `GAP-B{batch}-{seq}` scheme. `next_gap_id()`'s query is
`WHERE gap_id GLOB 'GAP-[0-9]*'` (scripts/db.py:139) — none of the 5 live ids match that glob
(the character after `GAP-` is `B`, not a digit), so the function silently falls through to the
`GAP-001` default every time, regardless of how many `GAP-B0N-NNN` ids already exist. No
collision resulted in this test only because `GAP-001` happens not to exist yet.
FINDING   : FAIL
LOCATION  : scripts/db.py:135-144 `next_gap_id()`
NOTE      : Same shape of defect as the `source_locators`/`evidence_sources` ref_id high-water
  mark bug CLAUDE.md §4 describes as "WRONG for weeks" — an allocator whose pattern has drifted
  from the table's real convention. Two sessions in the same untracked window minting gaps via
  `next-id gaps` would both get `GAP-001` and the second INSERT would fail on the `PRIMARY KEY`
  collision (loud, not silent) — better than the ref_id case, but the allocator itself is still
  wrong and should read the live prefix scheme rather than assuming unscoped `GAP-NNN`.

INVOKED   : `add-gap --category ST --priority P1 --description "SMOKE-TEST S1: no item_code exists for handrails..." --section stair-ramp-threshold-biomechanics-accessibility --session ...`
EXIT      : 0 → `gap_id: GAP-001` (confirms the defect above concretely — this mobility gap's id
  carries zero information about which batch/slug-family minted it, unlike every real gap)
FINDING   : PASS (write succeeded) / see DEFECT above for the id-shape problem

INVOKED   : `add-gap-mining --gap-id GAP-001 --search-strategy '{"strategies":[{"tool":"crossref","query":"handrail diameter grip biomechanics","candidates_returned":0}]}' --candidates-returned 0 --candidates-reviewed 0 --outcome null_result --check-method pubmed_cluster --notes "SMOKE-TEST S1: null result probe, not a real mining attempt." --session ...`
EXIT      : 0 → `{"gap_mining_id": 1}`
FINDING   : PASS

INVOKED   : `update-gap-addressability --gap-id GAP-001 --addressability NOT-ADDRESSABLE --session ...`
  (note: PROTOCOL/task text says `--mining-addressability`; the actual flag is `--addressability` —
  confirmed by argparse usage string; minor doc/task-text mismatch, not a tool defect)
EXIT      : 0 → `{"gap_id": "GAP-001", "mining_addressability": "NOT-ADDRESSABLE"}`
FINDING   : PASS

INVOKED   : `unmined-gaps` (scratch, after)
OUTPUT    : returns the 5 real gaps, correctly EXCLUDES GAP-001 now that it has a `gap_mining` row
  / non-NULL `mining_addressability`
EXAMINED  : 6 gaps total in scope
FINDING   : PASS

### 5.5 Audit scripts — `citation_mining_completeness.py`, `gap_mining_audit.py`
INVOKED   : `python3 scripts/audit/citation_mining_completeness.py` (canonical, read-only, default args)
EXIT      : 0
OUTPUT    :
```
DB: data/guidebook.db | Session scope: (all) | Tier scope: 1..2
Examined (slug-linked T1-2 sources in scope): 6
Outstanding (no citation_mining row): 0
VERDICT: CLEAN
Total in scope: 6 | Total with citation_mining row: 6 (100.0%)
```
EXAMINED  : 6 (printed explicitly, per CLAUDE.md §2(a) requirement)
FINDING   : PASS — real subject, not vacuous; VERDICT enum includes CLEAN vs NOTHING-IN-SCOPE
  as distinct outcomes per the script's own docstring, so a future mobility-scoped run that finds
  zero sources would correctly self-report NOTHING-IN-SCOPE rather than a false CLEAN.

INVOKED   : same, `GUIDEBOOK_DB_PATH=$SMOKE/s1-research.db ... --session session_2026-08-25-pipeline-smoke-test-mobility.md`
EXIT      : 0
OUTPUT    : `Examined (slug-linked T1-2 sources in scope): 1` / `VERDICT: CLEAN` /
  `(repo-wide, not this session: 7/7 T1-2 sources mined, 100.0%)`
FINDING   : PASS — correctly scoped to the one synthetic source this session added and separately
  reports the repo-wide figure without conflating the two.

INVOKED   : `python3 scripts/audit/gap_mining_audit.py` (canonical)
EXIT      : 0
OUTPUT    : `schema version: 64 | gaps rows: 5 | gap_mining rows: 0 | EXAMINED: 5 | FAILURES: 0 |
  INFORMATIONAL: 1 — 5 OPEN gaps with mining_addressability=NULL (triage backlog)` / `PASS.`
FINDING   : PASS — `EXAMINED: 5` printed explicitly; correctly flags the triage backlog as
  informational (not a failure), matching its own documented severity model.

INVOKED   : same against scratch (post GAP-001 write)
OUTPUT    : `gaps rows: 6 | gap_mining rows: 1 | EXAMINED: 7 | FAILURES: 0` (same informational note)
FINDING   : PASS

## 6. External reachability probes (1-2 calls each)

### 6.1 WebSearch
INVOKED   : `WebSearch(query="handrail diameter grip biomechanics wheelchair ramp gradient corridor clear width accessibility standard")`
EXIT      : n/a (tool call succeeded)
OUTPUT    : 9 result links (access-board.gov, dimensions.com, several commercial ADA-compliance blogs), plus a synthesized summary citing 1¼–2" handrail diameter, 34-38" height, 1:12 ramp gradient, 36" clear width. **No academic/CrossRef-indexed sources** — all US commercial/government grey-literature pages, consistent with WebSearch being "US-only" per its own tool description.
FINDING   : PASS (reachable), shape = general web results, US-skewed, no tier-1 academic content
LOCATION  : n/a (external)
NOTE      : Reasonable for grey-literature/T4-T6 regulatory-stratum leads (ADA text), useless on
  its own for T1/Co-1 evidence — matches the project's own doctrine that regulatory sources need
  separate handling (CLAUDE.md §6 tier system).

### 6.2 WebFetch (Crossref probe)
INVOKED   : `WebFetch(url="https://api.crossref.org/works/10.1044/2019_AJA-19-0010", prompt="Return the DOI, title, and the first 3 items in the reference list if present, verbatim.")` — this DOI is REF-00325/RAP-08, already in the live `citation_mining` table, chosen so the result is checkable against real prior work.
EXIT      : reachable
OUTPUT    : Correctly returned DOI, title ("Speech Perception in Classroom Acoustics by Children
  With Hearing Loss and Wearing Hearing Aids"), and 3 reference entries.
FINDING   : PASS (reachable) but with an important shape caveat — see 6.4.
LOCATION  : n/a (external)

### 6.3 Consensus / Scholar Gateway
INVOKED   : `mcp__Consensus__search(query="handrail diameter grip force fall risk older adults biomechanics")`
OUTPUT    : 10 real papers with DOIs, abstracts, citation counts — directly on-topic for the
  mobility/handrail batch (Gosine 2021, Kose 2020, Komisar 2021/2019/2018, Maki 1998, Reeves 2008,
  etc.) — several look like strong Tier-1 biomechanical candidates for a real handrail item once
  one exists (§1).
FINDING   : PASS (reachable), topical relevance high for this exact batch
INVOKED   : `mcp__Scholar_Gateway__semanticSearch(query="What is the biomechanical evidence for handrail grip diameter and fall risk reduction in older adults and wheelchair users?", topN=5)`
OUTPUT    : 5 passages with DOIs/journal metadata (Startzell 2000 stair-negotiation review,
  Slavens 2015 pediatric wheelchair biomechanics, Koontz 2018 grab bars, Hwangbo 2012 low-floor
  bus, Swan 2020 handrail perceptions in aged care).
FINDING   : PASS (reachable); confirms `citation-miner_SKILL.md` §0's own characterization —
  topically relevant passages, not a citation graph (none of these are framed as "cites/cited-by"
  relationships, consistent with the skill's warning not to use this for forward mining).

### 6.4 Direct curl reachability — Crossref, OpenAlex, Semantic Scholar (via Bash, proxy-routed)
INVOKED   :
```
curl -sS -m 20 -o /tmp/cr_test.json -w "HTTP_CODE:%{http_code}\n" "https://api.crossref.org/works/10.1044/2019_AJA-19-0010"
curl -sS -m 20 -o /tmp/oa_test.json -w "HTTP_CODE:%{http_code}\n" "https://api.openalex.org/works/doi:10.1044/2019_AJA-19-0010"
curl -sS -m 20 -o /tmp/ss_test.json -w "HTTP_CODE:%{http_code}\n" "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1044/2019_AJA-19-0010?fields=title,citations.title"
```
EXIT      : 0 for all three; HTTP_CODE:200 for all three
OUTPUT    :
- Crossref: full JSON, `"reference-count":52` on the message object (the real reference list is
  reachable, structured, and countable — NOT just a WebFetch-summarized 3-item excerpt as in 6.2).
- OpenAlex: full JSON work record (id, doi, title, publication_year, ids incl. pmid) — a second
  viable backward/identity-resolution source not currently used anywhere in this codebase (grep
  confirmed zero references to `openalex.org` outside this probe).
- Semantic Scholar: full JSON **with an actual `citations` array containing real paperId/title
  pairs** — e.g. "Phoneme Perception in Children With Bilateral Cochlear Implants or Hearing Aids
  in Quiet, Noise, and Reverberation" — this is exactly the forward-mining "cited by" data
  `citation-miner_SKILL.md` §0 says is the preferred forward-mining method, retrieved with a
  single unauthenticated curl call.
FINDING   : PASS (all three reachable, structured, and directly usable for both directions of
  citation mining)
LOCATION  : n/a (external) — confirms the "R10 re-retrieval" and citation-graph capability §5.1
  says is ABSENT as a checked-in script is NOT blocked by network/connector access. The barrier is
  entirely that nobody has written
  `scripts/research/{crossref,openalex,semantic_scholar}_client.py`; the raw capability exists and
  is trivially reachable, unauthenticated, from this exact sandboxed environment.
NOTE      : This directly strengthens the §5.1 ABSENT finding: it is not that a retriever is hard
  to build or blocked by the proxy — it plainly is neither. It simply does not exist yet as
  checked-in code; every mining pass currently goes through a human/agent manually driving
  WebFetch/curl and hand-summarizing into `citation_mining.notes`, which is exactly what the 10
  live rows show (§5.2).

## 7. Retrieval log — `scripts/research/retrieval_log.py`
### 7.1 `--help`
INVOKED   : `python3 scripts/research/retrieval_log.py --help`
OUTPUT    : `usage: retrieval_log.py [-h] --session SESSION [--verify-authors] [--backfill]`
FINDING   : PASS
NOTE      : The module's primary interface (`fetch(url, session, purpose)`) is a Python function
  meant to be imported by a caller that does real retrieval (`scripts/resolve_dois.py` does this
  — grep confirms `from retrieval_log import fetch` there); the CLI only exposes the
  after-the-fact `--verify-authors`/`--backfill` audit modes, not a way to fetch-and-log a single
  URL from the command line. Not a defect — matches its documented USE section — but worth noting
  for anyone expecting a CLI fetch command.

### 7.2 `fetch()` — persist a probe payload
INVOKED   :
```python
from retrieval_log import fetch   # GUIDEBOOK_RETRIEVAL_LOG redirected to $SMOKE/retrieval-log-test
                                    # (the real retrieval-log/ is git-tracked; PROTOCOL forbids
                                    # writing tracked files, so this run never touched it)
fetch('https://api.crossref.org/works/10.1044/2019_AJA-19-0010',
      session='session_2026-08-25-pipeline-smoke-test-mobility',
      purpose='S1 smoke test: probe payload persistence, REF-00325 DOI (already in citation_mining)')
```
EXIT      : 0
WRITES    : `$SMOKE/retrieval-log-test/session_2026-08-25-pipeline-smoke-test-mobility/1eb5a8b8f737a965.json` (11,444 bytes, the real Crossref response body) and `.../manifest.jsonl` (1 line: url, purpose, sha256, byte count, exit code, artefact name, UTC timestamp)
OUTPUT    : parsed JSON returned correctly (`title` field matched the real Crossref record)
FINDING   : PASS
LOCATION  : scripts/research/retrieval_log.py:117-135 `fetch()`
NOTE      : Confirms the mechanism CLAUDE.md §2(c) describes exactly: the artefact is written to
  disk BEFORE the caller sees the parsed return value, and the manifest line is a genuine sha256
  of what was actually received, not a claim. This is real, working infrastructure — the gap is
  that (per §5.1) nothing in the citation-mining path currently calls `fetch()` at all; the 10
  live `citation_mining` rows' `notes` are pure hand-narration with no artefact behind them the
  way a `retrieval-log/` manifest entry would be. `retrieval_log.fetch` and `citation_mining` are
  two pieces of real, correct, uncombined machinery.

### 7.3 `--verify-authors` — real session (canonical DB, read-only)
INVOKED   : `python3 scripts/research/retrieval_log.py --verify-authors --session session_2026-08-19-research-batch-01-room-acoustic-performance`
EXIT      : 0
OUTPUT    :
```
logged payloads: 5   DOI-bearing: 5
EXAMINED: 5
NO LOGGED RETRIEVAL for 5 source(s) — not verifiable offline: REF-00325, REF-00561, REF-00578, REF-00969, REF-00970
CLEAN — stored authors and asserted bibliographic fields match the retrieved payloads, byte-for-byte source.
```
FINDING   : PASS — and note this is NOT failure mode (a) despite superficially resembling it.
  `verify_authors()` (scripts/research/retrieval_log.py:240-318) scans ALL 10 `evidence_sources`
  rows (global, not scoped to `created_by_session`) and cross-checks each against whatever
  payloads happen to be logged under THIS session's manifest folder specifically. The 5
  "unlogged" ref_ids (REF-00325/561/578/969/970) are real — their retrievals were logged under
  the *later* `session_2026-08-22`/`session_2026-08-23` manifests (batch 2/3), not this one — and
  the tool says so explicitly rather than silently passing or silently failing on them. `EXAMINED`
  and the unlogged list are both printed, so a reader can tell exactly what "CLEAN" does and does
  not cover. Confirmed by cross-referencing `retrieval-log/session_2026-08-19.../manifest.jsonl`
  directly: its 5 URLs are for REF-00607/965/966/967/968, exactly the 5 counted as EXAMINED.
LOCATION  : scripts/research/retrieval_log.py:240-318
NOTE      : Good design worth calling out positively — this is the CLAUDE.md §2(a) discipline
  ("prove it had a subject") actually implemented, with the unverifiable set surfaced by name
  rather than folded into a green result.

### 7.4 `--verify-authors` — our smoke session
INVOKED   : `GUIDEBOOK_DB_PATH=$SMOKE/s1-research.db GUIDEBOOK_RETRIEVAL_LOG=$SMOKE/retrieval-log-test python3 scripts/research/retrieval_log.py --verify-authors --session session_2026-08-25-pipeline-smoke-test-mobility`
EXIT      : 0
OUTPUT    : `logged payloads: 1   DOI-bearing: 1 / EXAMINED: 1 / NO LOGGED RETRIEVAL for 10 source(s)... / CLEAN`
FINDING   : PASS — correctly found and verified the 1 payload persisted in 7.2 against the
  matching DOI now present in `evidence_sources` on the scratch DB (added in §5.3), and correctly
  listed the other 10 (9 pre-existing room-acoustic-performance rows + the synthetic REF-00972's
  own duplicate DOI check) as unverifiable offline from this session's log.
EXAMINED  : 1


## 8. Research-stage skills — read and mechanically checked

Method: for each skill, checked every script/table/column it names against the live repo (file
existence, `db.py` subcommand existence, schema column existence), and looked for raw hand-written
SQL, retired vocabulary, or stale stage ids. No corpus mining performed (per PROTOCOL §4).

### 8.1 `adversarial-research` — HAND-SQL, LIVE, NOT A FALSE ALARM
The skill's own "Required outputs (DB-enforced)" §§1-5 (lines 39-74) — the FIVE fields the skill
exists to force onto every gap closure — are specified as raw `UPDATE evidence_sources SET
prior_expectation=...`/`search_queries_used=...` (lines 45, 51) and `UPDATE gaps SET
confidence_interval=..., shift_conditions=...` / `named_dissenter=...` / `falsification_condition=...`
(lines 57-72). **Checked: `grep -n "prior_expectation\|search_queries_used\|confidence_interval\|
shift_conditions\|named_dissenter\|falsification_condition" scripts/db.py` returns ZERO matches.**
All six columns are real (confirmed via `PRAGMA table_info`), and there is no `update-gap` or
`update-source` subcommand in `db.py` at all (only `add-gap`, `close-gap`,
`update-gap-addressability`, `add-source` — none take these fields). **The skill's own central,
mandatory mechanism has no CLI writer and can only be satisfied by hand-written SQL against the
scratch DB** — the exact pattern CLAUDE.md's write-path section claims is closed ("every one of
those tables and columns now has a writer that REFUSES... Do not hand-write SQL against a table
the CLI can reach; if you find one it cannot, that is a coverage bug to fix"). This is that
coverage bug, live, for one of the highest-value tables in the research stage (adversarial
rigour).
FINDING   : FAIL (real, current, high-value)
LOCATION  : skills/adversarial-research_SKILL.md:39-74 (teaching); scripts/db.py (missing writer:
  no `--prior-expectation`/`--search-queries-used` on `add-source`, no `update-gap` subcommand at
  all for `confidence_interval`/`shift_conditions`/`named_dissenter`/`falsification_condition`)
NOTE      : By contrast the SAME file's "Population match record" section (lines 76-96) WAS fixed
  2026-08-25 to call `db.py add-population-match`, with a comment explicitly naming this exact
  history ("This block was hand-written SQL because db.py had no writer for this table -- the gap
  CLAUDE.md §4 names as where the 2026-08-19 fabrication entered. It has one now"). The fix pattern
  is proven and was applied to one part of this file but not the other three tables/six columns.
  For the mobility batch: any session running adversarial-research on a mobility gap closure hits
  this immediately — it is not an edge case, it is the skill's first required step.

### 8.2 `progressive-measurement` — same shape of defect, different table
"Required DB writes (per walk)" (lines 128-149) instructs raw `INSERT INTO spec_value_probes
(...) VALUES (...)`, `INSERT INTO evidence_sources (...) ON CONFLICT DO UPDATE...`, `INSERT INTO
source_slug_links (...) ON CONFLICT DO NOTHING`, and later `UPDATE items SET
pmp_empirical_ceiling=..., pmp_gap_signed=..., pmp_last_walk_at=... WHERE item_code=?`. **Checked:
`grep -n "spec_value_probes"` and `grep -n "pmp_empirical_ceiling\|pmp_gap_signed\|
pmp_last_walk_at"` against `scripts/db.py` both return ZERO matches.** `spec_value_probes` (the
walk's own core table) and all three `items.pmp_*` columns (confirmed real via
`PRAGMA table_info(items)` — CLAUDE.md's own item-schema excerpt in §4 lists them) have no CLI
writer whatsoever.
FINDING   : FAIL (real, current)
LOCATION  : skills/progressive-measurement_SKILL.md:128-149; scripts/db.py (no `spec_value_probes`
  writer, no `items.pmp_*` writer)
NOTE      : Same file already carries the 2026-08-25 fix pattern for ONE line
  (`evidence_population_match: use python3 scripts/db.py add-population-match`, with the identical
  "Hand SQL here bypasses the FK, vocabulary and MISMATCH-reason refusals" warning) — proving the
  author was aware of the general problem while writing this exact section, but did not extend the
  fix to `spec_value_probes` or `items.pmp_*` in the same edit. For the mobility batch: E-03 (ramp
  gradient) and E-08 (corridor clear width) are exactly the kind of numerical-spec items PMP exists
  to walk — this table is squarely in scope for the batch PROTOCOL describes.

### 8.3 The SAME stale boilerplate line, copy-pasted into 4 skills
`literature-review-planner_SKILL.md:12`, `multilingual-research_SKILL.md:12`,
`functional-deficit-researcher_SKILL.md:14`, `economics-researcher_SKILL.md:15` all carry the
byte-identical sentence: *"All slug lookups use `python3 scripts/db.py coverage {slug}`..."* — the
command is missing the required `--slug` flag. Confirmed by literal execution:
```
$ python3 scripts/db.py coverage stair-ramp-threshold-biomechanics-accessibility
usage: db.py coverage [-h] --slug SLUG
db.py coverage: error: the following arguments are required: --slug
EXIT 2
```
FINDING   : FAIL (low severity, cosmetic, but real and reproduced 4×)
LOCATION  : the 4 files/lines above; scripts/db.py:917-918 (`coverage` requires `--slug`)
NOTE      : Trivial to work around once noticed (add `--slug`), but a literal copy-paste from any
  of these four skills fails on the first command. Same root cause across all four — one shared
  "C2 overhaul 2026-05-05" boilerplate block, never corrected in any of its 4 copies.

### 8.4 `connection-discovery` — instructs writing directly to the CANONICAL DB, and nothing in the CLI would stop it
Lines 94, 209, 219, 253 all read `GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/db.py
{next-id connections | add-connection | connections}` — i.e. the skill's own example commands
point `GUIDEBOOK_DB_PATH` at the **canonical, committed file**, not a scratch copy, directly
contradicting CLAUDE.md's "Research writes go to a scratch copy first" instruction and §0 rule 3
("Never write `data/guidebook.db` directly... migrations only").

**This is not merely a bad example — I checked whether anything downstream would catch it, and
nothing does.** `scripts/dbcore.py` defines `is_canonical(path=None)` (line 65) whose own
docstring says *"Callers that must never touch the canonical file (CLAUDE.md rule 3: migrations
only) use this to refuse, rather than trusting that GUIDEBOOK_DB_PATH was set."* **`grep -rn
"is_canonical" scripts/ | grep -v __pycache__` shows it is called ONLY from `dbcore.py`'s own
`--selftest` block (lines 437-439) — zero callers in `scripts/db.py` itself, and zero callers in
`dbcore.connect()`, the function every `insert_*`/`add-*` writer in `db.py` goes through (confirmed:
`grep -n "is_canonical\|dbcore.connect(" scripts/db.py` shows 6 `connect()` call sites, 0
`is_canonical` checks).** `dbcore.db_path()` (line 51-59) defaults to the canonical file when
`GUIDEBOOK_DB_PATH` is unset at all. **The guard function that is supposed to be the CLI's defence
against exactly this mistake exists, is unit-tested in isolation, and is never wired into the
actual write path.** I did not execute the connection-discovery example commands against the
canonical DB (that would violate PROTOCOL §Hard-prohibitions 1) — this finding is from static
code reading, deliberately not a live reproduction, precisely because a live reproduction is the
risk being described.
FINDING   : FAIL (highest severity of anything in this log — not mobility-specific, but a live,
  general defect in the write-path safety CLAUDE.md §0/§4 present as settled)
LOCATION  : skills/connection-discovery_SKILL.md:94,209,219,253 (the instruction);
  scripts/dbcore.py:51-59 `db_path()` (defaults to canonical), :65-74 `is_canonical()` (defined,
  unit-tested, never called by a writer); scripts/db.py (every `insert_*`/`add-*` function calls
  `dbcore.connect()` with no canonical-path guard)
NOTE      : For the mobility batch specifically: connection-discovery is exactly the skill a
  session would run after finding a cross-item connection while researching mobility items (E-08
  circulation ↔ E-01 lift ↔ E-04 parking are natural CROSS-ITEM connection candidates) — so this
  is not a remote corner of the skill set, it is directly in the batch's path. Recommend, in order:
  (1) fix the 4 example lines to point at a scratch path, (2) wire `is_canonical()` into
  `dbcore.connect()` itself so the CLI refuses a non-dry-run write to the canonical file
  regardless of which skill or session set `GUIDEBOOK_DB_PATH` wrong, matching CLAUDE.md's stated
  guarantee rather than merely a convention several skills already violate.

### 8.5 `jurisdiction-tracker` — its own jurisdiction scope disagrees with the batch's bucket-1/2 scheme
`skills/jurisdiction-tracker_SKILL.md:31` declares 17 "Jurisdictions in scope (§4.7.3)": Germany,
Belgium, Norway, France, Brazil, Japan, Canada, Switzerland, Australia, UK, USA, EU, ISO, Singapore,
Sweden, Denmark, Finland. PROTOCOL.md's bucket scheme (sourced from
`workplan/2026-08-18-research-frame-proposal.md:420-424`, confirmed by direct read) is: **bucket 1**
= UN·ISO·Canada·USA·UK·Germany·Norway·Sweden·Japan·Australia; **bucket 2** =
EU·Singapore·New Zealand·Ireland·France·Spain·Portugal·Finland·Netherlands·South Korea; **bucket 3**
(explicitly lower priority) = Brazil·China·Italy·Denmark·Switzerland·Mexico·Austria·Belgium·
Colombia·Chile. The skill's list **mixes bucket 1, 2 and 3 members with no priority marking at
all** (Belgium/Brazil/Switzerland/Denmark are bucket-3, i.e. explicitly lower priority, sitting
undistinguished next to bucket-1 UK/Germany) **and omits UN (bucket 1) and New
Zealand/Ireland/Spain/Portugal/Netherlands/South Korea (all bucket 2) entirely.**
FINDING   : FAIL
LOCATION  : skills/jurisdiction-tracker_SKILL.md:31 vs
  workplan/2026-08-18-research-frame-proposal.md:420-424
NOTE      : A session running jurisdiction-tracker on the mobility batch as literally written would
  verify currency for a jurisdiction set that does not match the batch's own priority order and
  silently omits 7 of the 20 bucket-1/2 jurisdictions PROTOCOL.md specifies. This looks like the
  skill predates the 2026-08-18 bucket ruling and was never reconciled to it — the same "map
  predates a later owner ruling" shape CLAUDE.md §0 opens with, just not yet caught here.

### 8.6 `question-author` — correctly and prominently self-flags ABSENT (verified, not a new finding)
Already carries its own `⚠ INOPERATIVE` banner (lines 16-56), which I independently verified:
`SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'specif%'` on the canonical DB
returns only `specifications` (plural) and `specification_source_links` — **no table named
`specification` (singular)** exists, confirming the banner's claim exactly.
FINDING   : ABSENT (correctly self-documented; not research-stage in any case — `specifications`
  is the judgment-stage table per CLAUDE.md's own pipeline map, so this skill is mis-scoped to
  research to begin with)
LOCATION  : skills/question-author_SKILL.md:16-56 (banner, accurate); table check confirmed live
NOTE      : Good example of honest self-flagging; no action needed beyond what the file already says.

### 8.7 Remaining skills checked, no defect found
- **`multilingual-research`** (584 lines) — beyond the shared §8.3 boilerplate line, spot-checked
  its `db.py log-search` usage examples against the real CLI signature (matches); no hand-SQL found
  in the sampled sections; §0-style connector-availability framing consistent with
  `citation-miner_SKILL.md`.
- **`research-log-manager`** — correctly reflects the `upsert-coverage`/`upsert-language` freeze
  (line 98: *"`upsert-coverage` and `upsert-language` are gone"*) and correctly reflects the
  `author_display` tombstone/migration-063 authors-are-rows change. Cleanest-maintained skill
  checked in this batch.
- **`content-gap-analyzer`** (57 lines) — `add-gap` usage matches the real CLI; its own
  "Next GAP-ID: [GAP-NNN]" convention in the required output block is consistent with (i.e. shares
  the same stale assumption as) the `next_gap_id()` allocator defect found independently in §5.4.
- **`economics-researcher`**, **`functional-deficit-researcher`** — beyond the shared §8.3 line, no
  additional hand-SQL or dead-script references found in a full read.
- **`connection-discovery`** — beyond §8.4, its table/column usage (`connections`, `gaps`,
  `add-gap`, `next-id connections`, `update-connection --status CONSUMED`) all check out against
  the real schema and CLI.


## 9. Stage gates

### 9.1 `scripts/audit/research_protocol_audit.py`
INVOKED   : `python3 scripts/audit/research_protocol_audit.py` (no args; canonical DB, read-only)
EXIT      : 0
OUTPUT    : 9 checks, all `0` issues; `EXAMINED: 40`; "Audit clean."
EXAMINED  : 40 (= 5 gaps + 10 evidence_sources + 25 evidence_population_match + 0 search_languages,
  computed live from `COUNT(*)` on each table at run time — confirmed by independently querying
  all four tables: 5/10/25/0 = 40, matches exactly)
FINDING   : PASS — genuinely non-vacuous (40 real rows, not 0), and CHECK 7/8 (verified citations
  lacking `prior_expectation`/`search_queries_used`) both read `0` **because all 10 VERIFIED
  sources already have `prior_expectation` populated** — confirmed by direct query
  (`SELECT COUNT(*) FROM evidence_sources WHERE verification_status='VERIFIED' AND
  prior_expectation IS NOT NULL AND prior_expectation!=''` = 10 of 10). This corroborates §8.1: the
  only way those 10 rows got `prior_expectation` populated is the hand-SQL path the skill
  literally teaches, since `db.py` has no writer for that column — the audit is clean because
  someone already did the workaround the skill instructs, not because a CLI made it unnecessary.
LOCATION  : minor stale-comment defect at scripts/audit/research_protocol_audit.py:181-186 — the
  comment justifying the EXAMINED formula says "every one of them is presently empty (2026-08-06
  clean-room reset), so no combination could read as anything but zero," which is no longer true:
  `gaps`=5, `evidence_sources`=10, `evidence_population_match`=25 are all populated today. The
  CODE still computes EXAMINED correctly by live `COUNT(*)` (confirmed: 40 matches), so this is a
  stale-comment-only defect, not a functional one — flagged because CLAUDE.md §2(b) treats
  drifted documentation of DB state as the same failure class as drifted prose.
NOTE      : Zero of the 40 examined rows touch any mobility slug (all 10 evidence_sources / 25
  matches / 5 gaps are room-acoustic-performance, per §5.0/§5.4) — this gate will need a genuine
  re-run once mobility evidence exists; today it says nothing about mobility readiness.

### 9.2 `scripts/audit/pmp_audit.py`
INVOKED   : `python3 scripts/audit/pmp_audit.py`
EXIT      : 0
OUTPUT    : CHECKs 1-6 all `0`; CHECK 7 explicitly SKIPPED with a named reason ("items table does
  not carry spec_value_origin; drift detection requires reasoning-doc parsing (future work)");
  `ISSUES: 0` / `EXAMINED: 0`
EXAMINED  : **0** — printed explicitly, honestly, and confirmed real: `spec_value_probes` has 0
  rows on the canonical DB (consistent with §8.2's finding that the table has no CLI writer and,
  unlike `prior_expectation`, nobody appears to have hand-SQL'd it either).
FINDING   : VACUOUS — a textbook example of CLAUDE.md §2(a)'s failure mode (a), except caught
  honestly by the script itself rather than hidden: it prints `EXAMINED: 0` plainly instead of
  a bare "PASS". It does not, however, escalate to a distinct NOTHING-IN-SCOPE verdict the way
  `citation_mining_completeness.py` does (§5.5) — exit code is still 0, same as a real pass. Per
  CLAUDE.md's own text, `scripts/run_checks.py` is supposed to be the layer that "reports
  zero-subject passes as NOTHING-IN-SCOPE and escalates blocking-and-vacuous ones" — I did not
  independently verify `run_checks.py`'s registry-level handling of this specific script in this
  smoke test (out of the research-stage scope PROTOCOL assigned me); noting it as a gap between
  what the individual script prints and what a reader would need to not mistake this for a
  meaningful pass.
LOCATION  : scripts/audit/pmp_audit.py CHECK-count summation (0 subjects); root cause is §8.2's
  ABSENT `spec_value_probes` writer — this gate is vacuous because nothing can write to the table
  it audits.
NOTE      : Directly relevant to the mobility batch: E-03 (ramp gradient) and E-08 (corridor width)
  are exactly the numeric-spec mobility items PMP is meant to walk. A mobility batch running PMP
  today would get the same `EXAMINED: 0` "clean" result — not because mobility specs have been
  walked and passed, but because the walk mechanism has never been exercised by anyone, on any
  item, at all.

### 9.3 `scripts/audit/research_batch_dod.py --session session_2026-08-25-pipeline-smoke-test-mobility`
INVOKED   : as above (canonical DB — this session has admitted nothing to the canonical DB, so
  this is a legitimate read-only probe of "what would R1-R15 say about a batch that has done
  nothing yet")
EXIT      : 0 (informational; script does not exit nonzero on NON-COMPLIANT — confirmed by the
  exit code printed despite the "NON-COMPLIANT: 3 rule(s) unmet" verdict)
OUTPUT    : R1-R8, R10-R15 all PASS (all vacuously — "0 searches", "0 candidates", "0 zero-yield
  searches", etc., since this session hasn't logged anything against the canonical DB); **R1 FAILS
  outright** ("NO Co-1/Co-2 pass... Co-1 is CO-PRIMARY with T1 (CRPD Art 4.3)"); **R9a and R9b both
  report `NOTHING IN SCOPE`** explicitly (not PASS) because the session admitted no sources.
EXAMINED  : 0 for nearly every rule (correctly unstated as a blanket number — each rule states its
  own subject count inline, e.g. "0 searches targeted co1/co2 and 0 co1/co2 sources admitted")
FINDING   : PASS (tool works correctly) — and this is a good demonstration of the CLAUDE.md §2(a)
  discipline done right: most rules read PASS-with-zero-subjects (arguably should be
  NOTHING-IN-SCOPE too, same critique as 9.2), but **R9a/R9b explicitly print "NOTHING IN SCOPE"
  rather than PASS when their subject count is 0** — proving the codebase knows how to make this
  distinction (see the "SUBJECT COUNT FIRST" comment at scripts/audit/research_batch_dod.py:463-467
  documenting exactly this fix, dated 2026-08-23) and simply has not applied it uniformly to every
  rule in the same script.
NOTE      : R1's FAIL is a real, correct, useful finding for planning the mobility batch: **the
  batch MUST include a Co-1/Co-2 lived-experience retrieval pass from its first session**, per
  CRPD Art 4.3 co-primacy — it is not optional or deferrable to a later pass.

### 9.4 `scripts/audit/research_batch_dod.py --all`
INVOKED   : as above (canonical DB, all sessions)
EXIT      : 0
OUTPUT    : R1-R10, R12-R15 all PASS with real, non-zero subject counts (e.g. "R4: 25 population
  linkages produced across 28 searches"; "R7: 60 candidates for 431 screened; 2 harm/failure
  flagged"); **R9a: PASS — 10 admitted DOI(s) checked against the stash; none held under a
  different ref_id**; **R9b: PASS — 10 admitted ref_id(s) checked against the stash across 6
  identifier types; no collision**; R11 shown separately as `~ R11: 856 (baseline 856) —
  INHERITED DEBT, not a regression` (a third status, neither PASS nor FAIL, for a pre-existing
  count that this run neither fixed nor worsened); overall verdict **COMPLIANT**.
EXAMINED  : stated per-rule inline (see above); not vacuous — real counts throughout.
FINDING   : PASS
NOTE      : See §10 below — this run is the direct evidence for the CLAUDE.md OD-5 claim check.


## 10. The OD-5 / R9-duplicate-gate claim — checked against the code, precisely

**CLAUDE.md §4 says:** *"`source_locators` is a lead index of identifiers, not evidence... the R9
duplicate gate currently cannot see it, which is a known live defect (OD-5)."*

**Checked against `scripts/audit/research_batch_dod.py` directly. The claim is TRUE of one rule
and FALSE of two others in the same script, and the file's own comments date the fix:**

1. **`R9` itself (scripts/audit/research_batch_dod.py:428-442) — the claim is TRUE and current.**
   Its query (line 432-435) is:
   ```sql
   SELECT e.doi, COUNT(*) c FROM evidence_sources e WHERE e.doi IS NOT NULL AND e.doi <> ''
   AND e.doi IN (SELECT doi FROM evidence_sources WHERE doi IS NOT NULL AND doi <> '' ...)
   GROUP BY e.doi HAVING c > 1
   ```
   This joins `evidence_sources` against **itself only** — `source_locators` does not appear
   anywhere in the query. R9 genuinely cannot see the clue store, exactly as CLAUDE.md says.

2. **`R9a` (scripts/audit/research_batch_dod.py:444-486) and `R9b` (:488-512) — added 2026-08-23
   SPECIFICALLY to close this gap, and the code's own comment says so in as many words:**
   the block starting at line 444 is headed `# --- R9a / R9b: the stash R9 could not see (OD-5)
   ---------` and states *"R9 above compares evidence_sources against ITSELF. source_locators —
   835 held identifiers, 441 of them DOIs — was invisible to it... That is OD-5, and CLAUDE.md 4
   records it as a known live defect."* Then, immediately below, the actual queries:
   - R9a (line 472-475): `... FROM evidence_sources e JOIN source_locators sl ON
     LOWER(TRIM(sl.doi)) = LOWER(TRIM(e.doi)) WHERE ... AND sl.ref_id <> e.ref_id ...` — DOES join
     against `source_locators`, catching a source admitted under a different `ref_id` than the
     one the stash already holds for the same DOI.
   - R9b (line 495-501, widened 2026-08-23 per the comment at line 488): `... FROM
     evidence_sources e JOIN source_locators sl ON sl.ref_id = e.ref_id WHERE (<6-identifier-type
     mismatch OR>) ...` — checks all 6 identifier columns (`doi, pmid, pmcid, isbn, issn,
     standard_number`), not just DOI, reaching (per the comment) 751 of 835 stash rows (the 84
     rows carrying no identifier at all are correctly and explicitly out of reach, not silently
     folded into a pass).

   **Live-run confirmation (§9.4):** `research_batch_dod.py --all` on the canonical DB currently
   prints `R9a: PASS — 10 admitted DOI(s) checked against the stash; none held under a different
   ref_id` and `R9b: PASS — 10 admitted ref_id(s) checked against the stash across 6 identifier
   types; no collision` — i.e. **the gate DOES see `source_locators` today, and actively checked
   all 10 real evidence_sources rows against it.**

**CONCLUSION: CLAUDE.md §4's OD-5 sentence is STALE, not wrong-in-spirit.** It correctly describes
`R9` (still self-join-only, still genuinely blind to the stash) but its blanket phrasing — "the R9
duplicate gate ... cannot see it" — reads as describing the WHOLE duplicate-detection surface, and
that whole surface (R9 + R9a + R9b, run together by `research_batch_dod.py`, which is what a real
session's session-close actually invokes) closed this gap on 2026-08-23, two days before this
smoke test and confirmed still live on 2026-08-25. The narrower, still-true statement would be:
*"R9 itself is DOI-self-join-only and blind to source_locators; R9a/R9b, added 2026-08-23, cover
that blind spot across 6 identifier types and are what a batch's session-close DoD check actually
runs."*
FINDING   : the underlying mechanism is FIXED (PASS); the CLAUDE.md prose describing it is STALE
LOCATION  : scripts/audit/research_batch_dod.py:428-442 (R9, self-join, genuinely blind to
  source_locators — the part of the OD-5 claim that is still true); scripts/audit/research_batch_dod.py:444-486
  (R9a, joins source_locators on DOI); scripts/audit/research_batch_dod.py:488-512 (R9b, widened
  2026-08-23, joins source_locators on all 6 identifier columns); CLAUDE.md §4 (the sentence to
  correct — this is exactly the kind of drifted-prose-vs-database gap CLAUDE.md §2(b) itself warns
  about, found here in CLAUDE.md's own text about its own tooling)
NOTE      : For the mobility batch specifically: this means a real duplicate-identity check against
  the 875-row clue store (§2) IS mechanically available today via `research_batch_dod.py`'s R9a/R9b
  — a mobility session does not need to build new tooling to get stash cross-checking, only to
  actually admit sources and run the existing DoD gate at session close. This is a materially more
  optimistic finding than CLAUDE.md's current text suggests, and worth surfacing to the owner as a
  documentation fix (drop OD-5's "currently cannot see it" framing, or narrow it explicitly to R9).


## S1 SUMMARY

**Run integrity:** `data/guidebook.db` sha256 unchanged across the whole run (`30a1066...` at
start and end — verified). No tracked file touched except this log. All writes went to
`$SMOKE/s1-research.db` or `$SMOKE/retrieval-log-test/`. No evidence admitted anywhere; external
probes limited to 1-2 calls each per tool (§6).

### (a) Every skill/script/tool invoked, PASS/FAIL/VACUOUS/ABSENT/BLOCKED

| # | Invoked | Verdict |
|---|---|---|
| 1 | items/slugs/axes/access_needs/access_need_icf/access_need_axis_map/item_population_links queries (framing) | PASS, 1 BLOCKING gap (no handrail item) |
| 2 | `source_locators` column census + jurisdiction/mobility-relevance analysis | PASS (analysis); jurisdiction column FAIL (unusable as filter) |
| 2 | selector for clue-store leads (list/query-locators) | ABSENT |
| 2 | `db.py add-locator` — valid write | PASS |
| 2 | `db.py add-locator` — duplicate ref_id refusal | PASS |
| 2 | `db.py add-locator` — bad status vocab refusal | PASS |
| 2 | `db.py add-locator` — duplicate DOI (R9, case-folded) refusal | PASS |
| 2 | `db.py add-locator` — bad ref_id shape refusal | PASS |
| 2 | `db.py add-locator` — no-identifier CHECK refusal | PASS (uncurated traceback) |
| 2 | `db.py add-locator` — bad-FK case | ABSENT (N/A by design, no FK cols on this table) |
| 2 | `dbcore.next_ref_id` union high-water mark | PASS |
| 3 | `db.py upsert-coverage` / `upsert-language` | PASS (correctly FROZEN, redirects to log-search) |
| 3 | `db.py log-search` — real mobility zero-yield query | PASS |
| 3 | `db.py log-search` — `--deferred-reason ""` empty-string handling | FAIL (silently miscounts as deferred) |
| 3 | R14 3-way distinction (query-shape/wrong-index/genuine-absence) schema support | ABSENT (expressible in free text, not structured/verified) |
| 3 | `db.py log-search` — legitimate deferred-reason | PASS |
| 3 | `db.py coverage` | PASS |
| 4 | `db.py add-candidate` — disposition CHECK vs live-vocab (`OUT-OF-SCOPE`) | PASS |
| 4 | `db.py add-candidate` — valid writes incl. `OUT-OF-SCOPE` | PASS |
| 4 | `db.py add-candidate` — R15 (ADMITTED requires RESOLVED) | PASS |
| 4 | `db.py add-candidate` — bad disposition/exec_id FK/slug FK refusals | PASS |
| 5 | executable backward/forward citation retriever | ABSENT |
| 5 | `citation_mining` table contents (10 rows) | PASS (analysis) — confirms hand-filled ledger, zero mobility rows |
| 5 | `db.py add-source` (synthetic row, boundary test) | PASS |
| 5 | `db.py is-mined` / `log-mining` (backward, forward, bad-direction) | PASS |
| 5 | `db.py unmined` | PASS |
| 5 | `db.py next-id gaps` / `next_gap_id()` | FAIL (disconnected from live `GAP-B0N-NNN` scheme) |
| 5 | `db.py add-gap` / `add-gap-mining` / `update-gap-addressability` / `unmined-gaps` | PASS |
| 5 | `scripts/audit/citation_mining_completeness.py` | PASS |
| 5 | `scripts/audit/gap_mining_audit.py` | PASS |
| 6 | WebSearch | PASS (reachable) |
| 6 | WebFetch (Crossref) | PASS (reachable) |
| 6 | `mcp__Consensus__search` | PASS (reachable) |
| 6 | `mcp__Scholar_Gateway__semanticSearch` | PASS (reachable, topical-only, matches skill's own caveat) |
| 6 | curl → Crossref / OpenAlex / Semantic Scholar (raw reachability) | PASS (all 3, full structured JSON incl. real citations array) |
| 7 | `scripts/research/retrieval_log.py --help` | PASS |
| 7 | `fetch()` payload persistence | PASS |
| 7 | `--verify-authors` (real session, own session) | PASS |
| 8 | `adversarial-research` skill — required-outputs DB writers | FAIL (no CLI writer, 6 columns) |
| 8 | `progressive-measurement` skill — required DB writes | FAIL (no CLI writer, `spec_value_probes` + 3 `items.pmp_*`) |
| 8 | `literature-review-planner`/`multilingual-research`/`functional-deficit-researcher`/`economics-researcher` — shared `coverage {slug}` boilerplate | FAIL (missing `--slug`, cosmetic, ×4) |
| 8 | `connection-discovery` — `GUIDEBOOK_DB_PATH=data/guidebook.db` in examples + `is_canonical()` dead code | FAIL (highest severity) |
| 8 | `jurisdiction-tracker` — jurisdiction scope vs bucket-1/2 | FAIL |
| 8 | `question-author` | ABSENT (self-documented; also mis-scoped to research) |
| 8 | `research-log-manager`, `content-gap-analyzer`, remaining skill content | PASS |
| 9 | `scripts/audit/research_protocol_audit.py` | PASS (stale comment only) |
| 9 | `scripts/audit/pmp_audit.py` | VACUOUS (EXAMINED: 0) |
| 9 | `scripts/audit/research_batch_dod.py --session ...` | PASS (correctly shows R1 FAIL + R9a/R9b NOTHING-IN-SCOPE) |
| 9 | `scripts/audit/research_batch_dod.py --all` | PASS (COMPLIANT, real subjects throughout) |
| 10 | OD-5 / R9 duplicate-gate claim vs code | mechanism FIXED (R9a/R9b, 2026-08-23); CLAUDE.md prose STALE |

### (b) Ranked BLOCKERS for the mobility batch

1. **No `handrail` item_code/slug exists.** `items`/`slugs` tables — `SELECT * FROM items WHERE
   name LIKE '%handrail%'` = 0 rows. Nearest neighbours G-03/I-03 are bathroom-specific. Blocks
   framing any handrail-specific evidence until a new item is created (D-SCHEMA-adjacent decision).
2. **Zero admitted evidence for any mobility slug.** `evidence_sources`/`source_slug_links` — all
   10 live rows are `room-acoustic-performance`; `citation_mining`/`gaps` likewise 100%
   room-acoustic-performance. The mobility batch is a cold start on every axis, not an extension.
3. **No CLI writer for `adversarial-research`'s 5 required fields.**
   `evidence_sources.prior_expectation`/`search_queries_used`,
   `gaps.confidence_interval`/`shift_conditions`/`named_dissenter`/`falsification_condition` —
   `scripts/db.py` (grep confirms zero matches). Forces hand-SQL on the scratch DB for the
   protocol's own mandatory step, exactly the pattern CLAUDE.md's write-path section claims is
   closed.
4. **No CLI writer for `progressive-measurement`'s core table.** `spec_value_probes` (all
   columns) and `items.pmp_empirical_ceiling`/`pmp_gap_signed`/`pmp_last_walk_at` —
   `scripts/db.py` (zero matches). E-03/E-08 are exactly the numeric-spec items this walk exists
   for.
5. **`connection-discovery_SKILL.md:94,209,219,253` instructs writing to the canonical DB
   directly**, and `scripts/dbcore.py:65-74` `is_canonical()` — the guard meant to prevent
   exactly this — is defined, self-tested, and called by nothing in the actual write path
   (`scripts/db.py`'s `insert_*` functions all go through `dbcore.connect()`, which never checks
   it; `db_path()` at `scripts/dbcore.py:51-59` defaults to canonical when the env var is unset).
   Highest-severity finding in this log; not mobility-specific but directly in the batch's path
   (E-08/E-01/E-04 are natural connection-discovery candidates).
6. **No tool to select clue-store leads for a batch.** `scripts/db.py` has `add-locator` only, no
   read/select subcommand; `source_locators.jurisdiction` is unusable as a filter (only 56/875
   rows carry a clean 2-3-letter code, and even those don't match PROTOCOL's bucket-1/2
   vocabulary — no row uses "Germany"/"Canada"/"Japan"/"Sweden" cleanly); only 22/875 rows carry
   both a clean jurisdiction AND a mobility-slug tag, and 0 rows tag the ramp/threshold-biomechanics
   or luminance-contrast slugs at all.
7. **No executable backward/forward citation-mining retriever**, though the underlying APIs are
   trivially reachable (§6.4 confirms Crossref/OpenAlex/Semantic Scholar all return HTTP 200 with
   full structured JSON, including a real `citations` array, via plain unauthenticated `curl`).
   `citation_mining`'s 10 rows are a hand-narrated ledger, not tool output. Nothing in
   `scripts/research/` does this; `scripts/resolve_dois.py` is identity-resolution only.
8. **`next_gap_id()`/`db.py next-id gaps`** (`scripts/db.py:135-144`) mints `GAP-NNN` while every
   live gap uses `GAP-B0{n}-NNN` — the allocator is disconnected from the convention actually in
   use, same shape as the ref_id allocator bug CLAUDE.md §4 already documents as historically
   wrong.
9. **`jurisdiction-tracker_SKILL.md:31`'s jurisdiction scope disagrees with the batch's own
   bucket-1/2 priority order** (mixes bucket-3 members in undistinguished, omits 7 of 20 bucket-1/2
   jurisdictions) — a session following it literally would verify currency for the wrong set.
10. **`log_search`'s `deferred_reason=""` (empty string) is silently miscounted as a deferral**
    (`scripts/db.py:336-410`, `get_coverage_completeness` at `:520-571`) — low practical risk but
    real, and corrupts exactly the jurisdiction/language coverage counts a mobility batch would
    use to track progress against the bucket-1/2 requirement.
11. **R1 (Co-1/Co-2 lived-experience pass) currently FAILs** for a from-scratch batch
    (`research_batch_dod.py --session ...`) — must be the mobility batch's first research step,
    not an afterthought, per CRPD Art 4.3 co-primacy.

### (c) ABSENT — what would have to be built

- A `handrail` `item_code` + slug (content/schema decision, not tooling).
- `scripts/db.py list-locators`/`select-locators` (or equivalent read path) over `source_locators`,
  filterable by jurisdiction-bucket and `used_in_bpcs`/slug — plus either a data-cleanup migration
  that stops `jurisdiction` doubling as a notes field, or a new clean jurisdiction column with an
  FK to `lang_jur_map.jurisdiction`.
- `scripts/research/crossref_client.py` (backward: `api.crossref.org/works/{doi}` →
  `.message.reference[]`) and `scripts/research/semantic_scholar_client.py` (forward:
  `api.semanticscholar.org/graph/v1/paper/DOI:{doi}/citations`), both writing through
  `retrieval_log.fetch()` before any curation — confirmed technically trivial (§6.4), simply not
  written yet.
- CLI writers (`db.py` flags or a new subcommand) for: `evidence_sources.prior_expectation` /
  `search_queries_used`; `gaps.confidence_interval` / `shift_conditions` / `named_dissenter` /
  `falsification_condition`; `spec_value_probes` (all columns); `items.pmp_empirical_ceiling` /
  `pmp_gap_signed` / `pmp_last_walk_at`.
- The `update-locator` subcommand that `add-locator`'s own duplicate-ref_id refusal message names
  (scripts/db.py:2504) but that does not exist.
- A structured (enum or paired-evidence-requirement) mechanism for R14's
  query-shape/wrong-index/genuine-absence distinction — today it is free text checked only for
  non-emptiness (`scripts/audit/research_batch_dod.py:583-597`).
- `is_canonical()` wired into `dbcore.connect()` itself, so the CLI refuses a non-dry-run write to
  the canonical file regardless of which skill or session sets `GUIDEBOOK_DB_PATH` wrong.

End of S1 log.
